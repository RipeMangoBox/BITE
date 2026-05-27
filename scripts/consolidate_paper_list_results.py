#!/usr/bin/env python3
"""Reviewed consolidation from run_paper_list_analysis.py results to paper_list.csv."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "obsidian-vault" / "paper_list.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--results", required=True, help="results.jsonl from scripts/run_paper_list_analysis.py")
    parser.add_argument("--dry-run", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument(
        "--allow-failures",
        action="store_true",
        help="Also consolidate known failure_kind values to analysis_mismatch/too_large.",
    )
    return parser.parse_args()


def row_value(row: dict[str, str], *names: str) -> str:
    for name in names:
        value = str(row.get(name) or "").strip()
        if value:
            return value
    return ""


def paper_link_for_row(row: dict[str, str]) -> str:
    link = row_value(row, "paper_link", "pdf_url", "url")
    if link:
        return link
    forum_id = row_value(row, "openreview_forum_id", "forum_id")
    return f"https://openreview.net/forum?id={forum_id}" if forum_id else ""


def row_key(row: dict[str, str], line_no: int) -> str:
    return (
        paper_link_for_row(row)
        or row_value(row, "paper_title", "title")
        or row_value(row, "openreview_forum_id", "forum_id")
        or str(line_no)
    )


def load_results(path: Path) -> dict[str, str]:
    updates: dict[str, str] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record: dict[str, Any] = json.loads(line)
            key = str(record.get("row_key") or "")
            if not key:
                continue
            if record.get("status") == "done":
                updates[key] = "checked"
            elif record.get("status") == "failed":
                failure_kind = str(record.get("failure_kind") or "")
                if failure_kind in {"analysis_mismatch", "too_large"}:
                    updates[key] = failure_kind
    return updates


def main() -> None:
    args = parse_args()
    source = Path(args.source).expanduser().resolve()
    results = Path(args.results).expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"paper list not found: {source}")
    if not results.is_file():
        raise SystemExit(f"results file not found: {results}")

    updates = load_results(results)
    if not args.allow_failures:
        updates = {key: state for key, state in updates.items() if state == "checked"}

    with source.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise SystemExit(f"paper list has no header: {source}")
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    if "state" not in fieldnames:
        raise SystemExit("paper list must have a state column")

    changes: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=2):
        key = row_key(row, index)
        new_state = updates.get(key)
        if not new_state:
            continue
        old_state = (row.get("state") or "").strip()
        if old_state != "Downloaded":
            continue
        row["state"] = new_state
        changes.append({"line": str(index), "row_key": key, "old_state": old_state, "new_state": new_state})

    print(json.dumps({"source": str(source), "results": str(results), "dry_run": args.dry_run, "changes": changes}, ensure_ascii=False, indent=2))

    if args.dry_run or not changes:
        return

    with source.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
