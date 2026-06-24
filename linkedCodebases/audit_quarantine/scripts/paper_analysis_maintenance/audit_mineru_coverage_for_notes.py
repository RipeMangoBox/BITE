#!/usr/bin/env python3
"""Audit PDF and MinerU coverage for existing analysis notes.

The script is read-only. It writes JSON/CSV artifacts that can feed a later
MinerU-only parsing queue.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_NOTES_CSV = REPO_ROOT / "artifacts" / "figure_caption_rebuild_batches" / "plan_20260609T074702Z" / "needs_full_rerun_notes.csv"
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "figure_caption_rebuild_batches"
SEARCH_ROOTS = (
    REPO_ROOT / "_private",
    REPO_ROOT / "obsidian-vault" / "batches",
    REPO_ROOT / "obsidian-vault" / "assets",
)

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import run_local_paper_analysis as runner  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notes-csv", default=str(DEFAULT_NOTES_CSV))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    return parser.parse_args()


def now_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_note_paths(path: Path) -> list[Path]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [Path(row["note_path"]).expanduser().resolve() for row in reader if row.get("note_path")]


def frontmatter_text(note: str) -> str:
    match = re.match(r"^---\n(.*?)\n---", note, flags=re.DOTALL)
    return match.group(1) if match else ""


def field_value(frontmatter: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", frontmatter, flags=re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip("\"'")


def note_title(note: str, frontmatter: str, note_path: Path) -> str:
    title = field_value(frontmatter, "title")
    if title:
        return title
    heading = re.search(r"^#\s+(.+?)\s*$", note, flags=re.MULTILINE)
    return heading.group(1).strip() if heading else note_path.stem


def infer_conf_year(note_path: Path, pdf_ref: str) -> str:
    if pdf_ref:
        parts = Path(pdf_ref).parts
        if len(parts) >= 2:
            return parts[-2]
    try:
        return note_path.parent.name
    except IndexError:
        return ""


def resolve_pdf(pdf_ref: str, conf_year: str) -> tuple[Path | None, dict[str, Any]]:
    return runner.resolve_existing_pdf_path(pdf_ref, conf_year=conf_year)


def mineru_key(value: str) -> str:
    return runner.mineru_match_key(value)


def complete_mineru_dirs(search_roots: tuple[Path, ...]) -> list[Path]:
    matches: list[Path] = []
    seen: set[Path] = set()
    for root in search_roots:
        if not root.exists():
            continue
        for content_path in root.rglob("*content_list*.json"):
            try:
                artifacts = runner.find_mineru_artifacts(content_path.parent)
            except Exception:  # noqa: BLE001
                try:
                    artifacts = runner.find_mineru_artifacts(content_path.parent.parent)
                except Exception:  # noqa: BLE001
                    continue
            if artifacts.content_list_path is None:
                continue
            path = artifacts.root.resolve()
            if path not in seen:
                seen.add(path)
                matches.append(path)
    return sorted(matches)


def find_mineru_matches(note_path: Path, title: str, pdf_path: Path | None, mineru_dirs: list[Path]) -> list[Path]:
    keys = {mineru_key(note_path.stem), mineru_key(title)}
    if pdf_path is not None:
        keys.add(mineru_key(pdf_path.stem))
    keys = {key for key in keys if key}
    matches: list[Path] = []
    for path in mineru_dirs:
        names = [path.name, path.parent.name]
        if len(path.parts) >= 3:
            names.append(path.parts[-3])
        path_keys = {mineru_key(name) for name in names if name}
        if any(a == b or a.startswith(b) or b.startswith(a) for a in keys for b in path_keys):
            matches.append(path)
    return sorted(set(matches))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    notes_csv = Path(args.notes_csv).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve() / f"mineru_coverage_{now_id()}"
    out_dir.mkdir(parents=True, exist_ok=False)

    note_paths = load_note_paths(notes_csv)
    mineru_dirs = complete_mineru_dirs(SEARCH_ROOTS)
    rows: list[dict[str, str]] = []
    queue_rows: list[dict[str, str]] = []
    counts: dict[str, int] = {
        "notes": len(note_paths),
        "complete_mineru_match": 0,
        "ambiguous_mineru_match": 0,
        "needs_mineru_pdf_available": 0,
        "missing_pdf_or_pdf_ref": 0,
    }
    for note_path in note_paths:
        note = note_path.read_text(encoding="utf-8", errors="ignore") if note_path.exists() else ""
        frontmatter = frontmatter_text(note)
        pdf_ref = field_value(frontmatter, "pdf_ref")
        title = note_title(note, frontmatter, note_path)
        conf_year = infer_conf_year(note_path, pdf_ref)
        pdf_path, pdf_resolution = resolve_pdf(pdf_ref, conf_year)
        matches = find_mineru_matches(note_path, title, pdf_path, mineru_dirs)
        if len(matches) == 1:
            status = "complete_mineru_match"
            counts[status] += 1
        elif len(matches) > 1:
            status = "ambiguous_mineru_match"
            counts[status] += 1
        elif pdf_path is not None:
            status = "needs_mineru_pdf_available"
            counts[status] += 1
            queue_rows.append({
                "note_path": str(note_path),
                "pdf_path": str(pdf_path),
                "conf_year": conf_year,
                "paper_title": title,
            })
        else:
            status = "missing_pdf_or_pdf_ref"
            counts[status] += 1
        rows.append({
            "status": status,
            "note_path": str(note_path),
            "paper_title": title,
            "pdf_ref": pdf_ref,
            "resolved_pdf": str(pdf_path or ""),
            "conf_year": conf_year,
            "mineru_matches": ";".join(str(path) for path in matches[:8]),
            "pdf_attempts": ";".join(str(item) for item in (pdf_resolution.get("attempts") or [])[:8]),
        })

    detail_csv = out_dir / "mineru_coverage_detail.csv"
    queue_csv = out_dir / "mineru_only_queue.csv"
    write_csv(
        detail_csv,
        rows,
        ["status", "note_path", "paper_title", "pdf_ref", "resolved_pdf", "conf_year", "mineru_matches", "pdf_attempts"],
    )
    write_csv(queue_csv, queue_rows, ["note_path", "pdf_path", "conf_year", "paper_title"])
    manifest = {
        **counts,
        "notes_csv": str(notes_csv),
        "mineru_dirs_indexed": len(mineru_dirs),
        "search_roots": [str(path) for path in SEARCH_ROOTS],
        "outputs": {
            "detail_csv": str(detail_csv),
            "mineru_only_queue_csv": str(queue_csv),
        },
    }
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
