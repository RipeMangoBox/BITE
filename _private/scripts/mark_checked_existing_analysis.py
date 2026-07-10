#!/usr/bin/env python3
"""Advance Downloaded paper_list rows to checked when a vault note already exists."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-list", type=Path, default=Path("obsidian-vault/paper_list.csv"))
    parser.add_argument("--analysis-root", type=Path, default=Path("obsidian-vault/analysis"))
    parser.add_argument("--only-sig", action="store_true")
    parser.add_argument("--dry-run", action=argparse.BooleanOptionalAction, default=True)
    return parser.parse_args()


def is_sig(row: dict[str, str]) -> bool:
    haystack = " ".join(
        [
            row.get("venue", ""),
            row.get("sort", ""),
            row.get("pdf_path", ""),
        ]
    ).upper()
    return "SIGGRAPH" in haystack


def rel_pdf_path(value: str) -> str:
    value = str(value or "").strip().replace("\\", "/")
    value = re.sub(r"^\./", "", value)
    value = re.sub(r"^obsidian-vault/", "", value)
    return value


def collect_existing_pdf_refs(root: Path) -> dict[str, str]:
    refs: dict[str, str] = {}
    for note in root.rglob("*.md"):
        text = note.read_text(errors="ignore")
        for match in re.finditer(r"(?:pdf_ref:\s*|!\[\[)(?:obsidian-vault/)?(paperPDFs/[^]\n]+?\.pdf)", text):
            refs.setdefault(rel_pdf_path(match.group(1)), str(note))
    return refs


def main() -> None:
    args = parse_args()
    refs = collect_existing_pdf_refs(args.analysis_root)
    with args.paper_list.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise SystemExit("missing CSV header")
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    changes: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=2):
        if (row.get("state") or "").strip() != "Downloaded":
            continue
        if args.only_sig and not is_sig(row):
            continue
        pdf_rel = rel_pdf_path(row.get("pdf_path", ""))
        note = refs.get(pdf_rel)
        if not note:
            continue
        row["state"] = "checked"
        changes.append(
            {
                "line": str(index),
                "paper_title": row.get("paper_title", ""),
                "venue": row.get("venue", ""),
                "pdf_path": row.get("pdf_path", ""),
                "note": note,
            }
        )

    print(json.dumps({"dry_run": args.dry_run, "changes_count": len(changes), "changes_sample": changes[:30]}, ensure_ascii=False, indent=2))
    if args.dry_run or not changes:
        return

    with args.paper_list.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
