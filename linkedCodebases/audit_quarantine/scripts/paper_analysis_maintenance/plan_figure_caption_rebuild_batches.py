#!/usr/bin/env python3
"""Plan batched figure/caption rebuilds for existing analysis notes.

The planner only writes manifests under artifacts/. It does not edit vault
Markdown. Rebuildable notes must have a completed formal analysis work
directory with parse, main-analysis, and final-report artifacts.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import shlex
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ANALYSIS_DIR = REPO_ROOT / "obsidian-vault" / "analysis"
DEFAULT_RUN_ROOT = REPO_ROOT / "_private" / "local_analysis_runs"
DEFAULT_OUT_ROOT = REPO_ROOT / "artifacts" / "figure_caption_rebuild_batches"


REQUIRED_RUN_FILES = (
    "manifest.json",
    "parse/figures_tables.json",
    "analysis/main_analysis.json",
    "report/final_report.md",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis-dir", default=str(DEFAULT_ANALYSIS_DIR))
    parser.add_argument("--run-root", default=str(DEFAULT_RUN_ROOT))
    parser.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT))
    parser.add_argument("--batch-size", type=int, default=25)
    parser.add_argument("--max-note-images", type=int, default=12)
    parser.add_argument("--figure-provider", choices=["none", "deepseek", "openai", "kimi"], default="deepseek")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--force", action="store_true", help="Pass --force to rebuild_figures_export.py commands")
    parser.add_argument("--limit", type=int, default=0, help="Limit rebuildable work dirs included in this plan")
    return parser.parse_args()


def now_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def canonical_note_paths(analysis_dir: Path) -> list[Path]:
    return sorted(path.resolve() for path in analysis_dir.glob("*/*.md") if path.is_file())


def complete_run_dir(path: Path) -> bool:
    return path.is_dir() and all((path / rel).exists() for rel in REQUIRED_RUN_FILES)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}
    return value if isinstance(value, dict) else {}


def note_path_from_run(run_dir: Path) -> Path | None:
    for rel in ("report/vault_export.json", "manifest.json"):
        data = load_json(run_dir / rel)
        note_path = str(data.get("note_path") or "").strip()
        if not note_path and isinstance(data.get("vault_export"), dict):
            note_path = str(data["vault_export"].get("note_path") or "").strip()
        if note_path:
            return Path(note_path).expanduser().resolve()
    return None


def complete_runs_by_note(run_root: Path) -> dict[Path, Path]:
    by_note: dict[Path, Path] = {}
    for run_dir in sorted(path for path in run_root.iterdir() if path.is_dir()):
        if not complete_run_dir(run_dir):
            continue
        note_path = note_path_from_run(run_dir)
        if note_path and note_path not in by_note:
            by_note[note_path] = run_dir.resolve()
    return by_note


def chunks(items: list[Path], size: int) -> list[list[Path]]:
    if size <= 0:
        raise SystemExit("--batch-size must be positive")
    return [items[index : index + size] for index in range(0, len(items), size)]


def command_for_batch(args: argparse.Namespace, batch_path: Path) -> list[str]:
    work_dirs = [line.strip() for line in batch_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "rebuild_figures_export.py"),
        *work_dirs,
        "--figure-provider",
        args.figure_provider,
        "--max-note-images",
        str(args.max_note_images),
        "--jobs",
        str(args.jobs),
        "--continue-on-error",
    ]
    if args.force:
        cmd.append("--force")
    return cmd


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    analysis_dir = Path(args.analysis_dir).expanduser().resolve()
    run_root = Path(args.run_root).expanduser().resolve()
    out_dir = Path(args.out_root).expanduser().resolve() / f"plan_{now_id()}"
    out_dir.mkdir(parents=True, exist_ok=False)

    notes = canonical_note_paths(analysis_dir)
    runs_by_note = complete_runs_by_note(run_root) if run_root.exists() else {}
    rebuildable_pairs = [(note, runs_by_note[note]) for note in notes if note in runs_by_note]
    missing_notes = [note for note in notes if note not in runs_by_note]
    if args.limit > 0:
        rebuildable_pairs = rebuildable_pairs[: args.limit]

    batch_paths: list[Path] = []
    commands: list[str] = []
    result_paths: list[Path] = []
    for index, batch in enumerate(chunks([run for _, run in rebuildable_pairs], args.batch_size), start=1):
        batch_path = out_dir / f"rebuild_batch_{index:04d}.txt"
        result_path = out_dir / f"batch_results_{index:04d}.json"
        batch_path.write_text("\n".join(str(path) for path in batch) + "\n", encoding="utf-8")
        batch_paths.append(batch_path)
        result_paths.append(result_path)
        commands.append(f"{shlex.join(command_for_batch(args, batch_path))} | tee {shlex.quote(str(result_path))}")

    rebuildable_rows = [
        {"note_path": str(note), "work_dir": str(run)}
        for note, run in rebuildable_pairs
    ]
    missing_rows = [{"note_path": str(note)} for note in missing_notes]
    write_csv(out_dir / "rebuildable_notes.csv", rebuildable_rows, ["note_path", "work_dir"])
    write_csv(out_dir / "needs_full_rerun_notes.csv", missing_rows, ["note_path"])
    (out_dir / "commands.sh").write_text(
        "#!/usr/bin/env bash\nset -euo pipefail\n\n" + "\n".join(commands) + ("\n" if commands else ""),
        encoding="utf-8",
    )
    manifest = {
        "analysis_dir": str(analysis_dir),
        "run_root": str(run_root),
        "canonical_notes": len(notes),
        "rebuildable_notes": len(rebuildable_pairs),
        "needs_full_rerun_notes": len(missing_notes),
        "batch_size": args.batch_size,
        "batch_count": len(batch_paths),
        "figure_provider": args.figure_provider,
        "max_note_images": args.max_note_images,
        "jobs": args.jobs,
        "force": args.force,
        "outputs": {
            "rebuildable_notes_csv": str(out_dir / "rebuildable_notes.csv"),
            "needs_full_rerun_notes_csv": str(out_dir / "needs_full_rerun_notes.csv"),
            "commands_sh": str(out_dir / "commands.sh"),
            "batch_files": [str(path) for path in batch_paths],
            "batch_result_files": [str(path) for path in result_paths],
        },
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
