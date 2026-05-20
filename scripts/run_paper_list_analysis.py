#!/usr/bin/env python3
"""Run formal analysis for rows in obsidian-vault/paper_list.csv.

This is a thin queue runner around scripts/run_local_paper_analysis.py. It keeps
paper_list.csv unchanged by default and writes per-paper results under
obsidian-vault/batches/<run_id>/.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "obsidian-vault" / "paper_list.csv"
DEFAULT_BATCH_ROOT = REPO_ROOT / "obsidian-vault" / "batches"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--state", default="Downloaded")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--shard-index", type=int, default=-1, help="Zero-based shard index for script-only parallel runs")
    parser.add_argument("--shard-count", type=int, default=0, help="Total shard count for script-only parallel runs")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--out-dir", default="")
    parser.add_argument("--analysis-output-root", default="", help="Output root passed to run_local_paper_analysis.py")
    parser.add_argument("--resume", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--mock-llm", action="store_true")
    parser.add_argument("--export-vault", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--conf-year", default="", help="Override venue/year folder. Defaults to venue column normalized as VENUE_YEAR.")
    parser.add_argument("--acceptance", default="unknown")
    parser.add_argument("--mineru-output-root", default="")
    parser.add_argument("--mineru-batch-id", default="")
    parser.add_argument("--require-existing-mineru-output", action="store_true")
    parser.add_argument("--extra-arg", action="append", default=[], help="Extra arg passed to run_local_paper_analysis.py; repeat as needed.")
    return parser.parse_args()


def now_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def venue_to_conf_year(venue: str) -> str:
    parts = str(venue or "").strip().split()
    if len(parts) >= 2 and parts[-1].isdigit() and len(parts[-1]) == 4:
        return "_".join(parts[:-1] + [parts[-1]]).replace("-", "_")
    return ""


def selected_rows(source: Path, state: str) -> list[dict[str, str]]:
    with source.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows: list[dict[str, str]] = []
        for index, row in enumerate(reader, start=2):
            if (row.get("state") or "").strip() != state:
                continue
            row["_csv_line"] = str(index)
            rows.append(row)
        return rows


def load_done(results_path: Path) -> set[str]:
    done: set[str] = set()
    if not results_path.exists():
        return done
    with results_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("status") == "done" and row.get("row_key"):
                done.add(str(row["row_key"]))
    return done


def row_key(row: dict[str, str]) -> str:
    return row.get("paper_link") or row.get("paper_title") or row.get("_csv_line", "")


def row_task_id(row: dict[str, str]) -> str:
    key = row_key(row) or "row"
    safe = "".join(ch if ch.isalnum() else "_" for ch in key).strip("_")
    safe = "_".join(part for part in safe.split("_") if part)
    return f"paper_list_l{row.get('_csv_line', 'unknown')}_{safe[:72]}"


def resolve_pdf_path(row: dict[str, str]) -> Path:
    raw = row.get("pdf_path") or ""
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path.resolve()


def command_for_row(args: argparse.Namespace, row: dict[str, str]) -> list[str]:
    pdf_path = resolve_pdf_path(row)
    conf_year = args.conf_year or venue_to_conf_year(row.get("venue", ""))
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "run_local_paper_analysis.py"),
        "--pdf", str(pdf_path),
        "--acceptance", args.acceptance,
        "--task-id", row_task_id(row),
    ]
    if row.get("paper_title"):
        cmd += ["--paper-title", row["paper_title"]]
    if row.get("paper_link"):
        cmd += ["--paper-link", row["paper_link"]]
    if conf_year:
        cmd += ["--conf-year", conf_year]
    if args.export_vault:
        cmd.append("--export-vault")
    if args.mock_llm:
        cmd.append("--mock-llm")
    if args.mineru_output_root:
        cmd += ["--mineru-output-root", args.mineru_output_root]
    if args.mineru_batch_id:
        cmd += ["--mineru-batch-id", args.mineru_batch_id]
    if args.require_existing_mineru_output:
        cmd.append("--require-existing-mineru-output")
    if args.analysis_output_root:
        cmd += ["--output-root", args.analysis_output_root]
    cmd.extend(args.extra_arg)
    return cmd


def main() -> None:
    args = parse_args()
    source = Path(args.source).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"paper list not found: {source}")

    run_id = args.run_id or now_id()
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else DEFAULT_BATCH_ROOT / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    results_path = out_dir / "results.jsonl"
    summary_path = out_dir / "summary.json"

    rows = selected_rows(source, args.state)
    if (args.shard_index >= 0) or args.shard_count:
        if args.shard_count <= 0:
            raise SystemExit("--shard-count is required when --shard-index is set")
        if args.shard_index < 0 or args.shard_index >= args.shard_count:
            raise SystemExit("--shard-index must be in [0, shard-count)")
        rows = [row for idx, row in enumerate(rows) if idx % args.shard_count == args.shard_index]
    if args.offset:
        rows = rows[args.offset:]
    if args.limit:
        rows = rows[:args.limit]

    completed = load_done(results_path) if args.resume else set()
    planned: list[dict[str, Any]] = []
    for row in rows:
        key = row_key(row)
        if key in completed:
            continue
        planned.append(row)

    manifest = {
        "run_id": run_id,
        "source": str(source),
        "state": args.state,
        "shard_index": args.shard_index,
        "shard_count": args.shard_count,
        "selected": len(rows),
        "planned": len(planned),
        "out_dir": str(out_dir),
        "analysis_output_root": args.analysis_output_root,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.dry_run:
        for row in planned:
            print(json.dumps({"row_key": row_key(row), "command": command_for_row(args, row)}, ensure_ascii=False))
        summary_path.write_text(json.dumps({**manifest, "status": "planned"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return

    counts = {"done": 0, "failed": 0, "skipped": 0}
    with results_path.open("a", encoding="utf-8") as results:
        for row in planned:
            key = row_key(row)
            started = time.monotonic()
            pdf_path = resolve_pdf_path(row)
            if not pdf_path.exists():
                record = {"row_key": key, "status": "failed", "error": f"missing pdf: {pdf_path}", "row": row}
            else:
                cmd = command_for_row(args, row)
                proc = subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True)
                status = "done" if proc.returncode == 0 else "failed"
                record = {
                    "row_key": key,
                    "status": status,
                    "returncode": proc.returncode,
                    "duration_seconds": round(time.monotonic() - started, 3),
                    "stdout_tail": proc.stdout[-4000:],
                    "stderr_tail": proc.stderr[-4000:],
                    "command": cmd,
                    "row": row,
                }
            counts[record["status"]] = counts.get(record["status"], 0) + 1
            results.write(json.dumps(record, ensure_ascii=False) + "\n")
            results.flush()

    summary = {**manifest, **counts, "results_path": str(results_path), "finished_at": datetime.now(timezone.utc).isoformat()}
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
