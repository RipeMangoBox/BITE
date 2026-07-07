#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPER_LIST = ROOT / "obsidian-vault" / "paper_list.csv"
RUN_DIR = ROOT / "paperSources" / "sig_coverage_20260629"
SOURCE = RUN_DIR / "crossref_siga2025_conference_papers.jsonl"
REPORT = RUN_DIR / "append_siga2025_crossref_report.json"

CSV_FIELDS = [
    "state",
    "importance",
    "paper_title",
    "venue",
    "project_link_or_github_link",
    "paper_link",
    "sort",
    "pdf_path",
]


def norm_title(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii")
    text = text.lower().replace("&", "and")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def read_rows() -> list[dict[str, str]]:
    with PAPER_LIST.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CSV_FIELDS:
            raise SystemExit(f"Unexpected paper_list header: {reader.fieldnames}")
        return [dict(row) for row in reader]


def write_rows(rows: list[dict[str, str]]) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = PAPER_LIST.with_name(f"{PAPER_LIST.name}.bak_siga2025_{timestamp}")
    shutil.copy2(PAPER_LIST, backup)
    tmp = PAPER_LIST.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(PAPER_LIST)
    return backup


def load_source() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    with SOURCE.open(encoding="utf-8") as handle:
        for line in handle:
            rec = json.loads(line)
            title = str(rec.get("title") or "").strip()
            doi = str(rec.get("doi") or "").strip()
            if not title or not doi:
                continue
            records.append({"title": title, "doi": doi})
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows = read_rows()
    source_records = load_source()
    existing_titles = {norm_title(row.get("paper_title", "")) for row in rows if row.get("paper_title")}
    existing_links = {str(row.get("paper_link") or "").strip().lower() for row in rows if row.get("paper_link")}

    added: list[dict[str, str]] = []
    skipped = Counter()
    for rec in source_records:
        title_key = norm_title(rec["title"])
        doi_key = rec["doi"].lower()
        if title_key in existing_titles:
            skipped["title"] += 1
            continue
        if doi_key in existing_links:
            skipped["doi"] += 1
            continue
        row = {
            "state": "Wait",
            "importance": "",
            "paper_title": rec["title"],
            "venue": "SIGGRAPH ASIA 2025",
            "project_link_or_github_link": "",
            "paper_link": rec["doi"],
            "sort": "SIGGRAPH ASIA 2025 / Conference Paper / Crossref ACM 10.1145/3757377",
            "pdf_path": "",
        }
        rows.append(row)
        added.append(row)
        existing_titles.add(title_key)
        existing_links.add(doi_key)

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "source": str(SOURCE.relative_to(ROOT)),
        "source_records": len(source_records),
        "added_rows": len(added),
        "skipped_existing": dict(skipped),
        "venue": "SIGGRAPH ASIA 2025",
        "selection_rule": "Crossref records with DOI prefix 10.1145/3757377.* and container-title Proceedings of the SIGGRAPH Asia 2025 Conference Papers",
        "sample_added": added[:20],
        "paper_list_backup": "",
    }
    if added and not args.dry_run:
        backup = write_rows(rows)
        report["paper_list_backup"] = str(backup.relative_to(ROOT))

    RUN_DIR.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
