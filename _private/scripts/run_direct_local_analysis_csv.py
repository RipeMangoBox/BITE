#!/usr/bin/env python3
"""Run run_local_paper_analysis.py directly for a small CSV sample."""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import re
import subprocess
import sys
import time
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--resume", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--omit-links", action="store_true", help="Do not pass paper/source links to avoid link-level existing-note collisions.")
    parser.add_argument("--extra-arg", action="append", default=[])
    return parser.parse_args()


def slug(value: str, fallback: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    return (text[:96] or fallback)


def venue_to_conf_year(venue: str) -> str:
    text = re.sub(r"\s+", "_", venue.strip().upper())
    return text


def row_key(row: dict[str, str], index: int) -> str:
    return row.get("paper_link") or row.get("paper_title") or str(index)


def command_for(args: argparse.Namespace, row: dict[str, str], index: int) -> list[str]:
    pdf = Path(row["pdf_path"])
    if not pdf.is_absolute():
        pdf = REPO / pdf
    cmd = [
        sys.executable,
        str(REPO / "scripts" / "run_local_paper_analysis.py"),
        "--task-id",
        f"sig_p2_36k_l{index}_{slug(row_key(row, index), str(index))}",
        "--pdf",
        str(pdf),
        "--paper-title",
        row.get("paper_title", ""),
        "--conf-year",
        venue_to_conf_year(row.get("venue", "")),
        "--export-vault",
        "--vault-root",
        "obsidian-vault",
        "--output-root",
        args.output_root,
        "--max-note-images",
        "6",
        "--experiment-label",
        args.run_id,
    ]
    if not args.omit_links and row.get("paper_link"):
        cmd += ["--paper-link", row["paper_link"]]
    if not args.omit_links and row.get("project_link_or_github_link"):
        cmd += ["--source-link", row["project_link_or_github_link"]]
    cmd.extend(args.extra_arg)
    return cmd


def run_one(args: argparse.Namespace, row: dict[str, str], index: int) -> dict:
    started = time.monotonic()
    cmd = command_for(args, row, index)
    record = {"row_key": row_key(row, index), "paper_title": row.get("paper_title", ""), "pdf_path": row.get("pdf_path", ""), "command": cmd}
    try:
        proc = subprocess.run(cmd, cwd=REPO, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        child_status = ""
        child_reason = ""
        try:
            parsed = json.loads(proc.stdout.strip() or "{}")
            child_status = str(parsed.get("status") or "")
            child_reason = str(parsed.get("reason") or "")
        except Exception:
            pass
        status = "done" if proc.returncode == 0 else "failed"
        if proc.returncode == 0 and child_status == "skipped":
            status = "skipped_existing"
        record.update(
            {
                "status": status,
                "child_status": child_status,
                "child_reason": child_reason,
                "returncode": proc.returncode,
                "duration_seconds": round(time.monotonic() - started, 3),
                "stdout_tail": proc.stdout[-8000:],
                "stderr_tail": proc.stderr[-8000:],
            }
        )
    except Exception as exc:
        record.update(
            {
                "status": "failed",
                "error_type": type(exc).__name__,
                "error": str(exc),
                "duration_seconds": round(time.monotonic() - started, 3),
            }
        )
    return record


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = REPO / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    results_path = out_dir / "results.jsonl"
    done_keys = set()
    if args.resume and results_path.exists():
        for line in results_path.read_text().splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            if item.get("status") == "done":
                done_keys.add(item.get("row_key"))

    with Path(args.source).open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if args.limit:
        rows = rows[: args.limit]

    pending = [(i + 2, row) for i, row in enumerate(rows) if row_key(row, i + 2) not in done_keys]
    manifest = {"run_id": args.run_id, "source": args.source, "out_dir": str(out_dir), "jobs": args.jobs, "count": len(rows), "pending": len(pending), "extra_arg": args.extra_arg}
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))

    with results_path.open("a", encoding="utf-8") as out:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
            futures = [executor.submit(run_one, args, row, index) for index, row in pending]
            for future in concurrent.futures.as_completed(futures):
                record = future.result()
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                out.flush()
                print(json.dumps({"status": record.get("status"), "paper_title": record.get("paper_title"), "duration_seconds": record.get("duration_seconds")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
