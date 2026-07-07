#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import time
import unicodedata
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPER_LIST = ROOT / "obsidian-vault" / "paper_list.csv"
RUN_DIR = ROOT / "paperSources" / "sig_coverage_20260629"
RECORDS_OUT = RUN_DIR / "crossref_tog_issues_2022_2026.jsonl"
REPORT_OUT = RUN_DIR / "append_tog_issues_crossref_report.json"
TOG_ISSN = "0730-0301"

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

ISSUES = [
    {"year": 2022, "volume": "41", "issue": "4", "label": "SIGGRAPH 2022 Journal Track", "from": "2022-07-01", "until": "2022-08-31"},
    {"year": 2022, "volume": "41", "issue": "6", "label": "SIGGRAPH Asia 2022 Journal Track", "from": "2022-11-01", "until": "2022-12-31"},
    {"year": 2023, "volume": "42", "issue": "4", "label": "SIGGRAPH 2023 Journal Track", "from": "2023-07-01", "until": "2023-08-31"},
    {"year": 2023, "volume": "42", "issue": "6", "label": "SIGGRAPH Asia 2023 Journal Track", "from": "2023-11-01", "until": "2023-12-31"},
    {"year": 2024, "volume": "43", "issue": "4", "label": "SIGGRAPH 2024 Journal Track", "from": "2024-07-01", "until": "2024-08-31"},
    {"year": 2024, "volume": "43", "issue": "6", "label": "SIGGRAPH Asia 2024 Journal Track", "from": "2024-11-01", "until": "2024-12-31"},
    {"year": 2025, "volume": "44", "issue": "4", "label": "SIGGRAPH 2025 Journal Track", "from": "2025-07-01", "until": "2025-08-31"},
    {"year": 2025, "volume": "44", "issue": "6", "label": "SIGGRAPH Asia 2025 Journal Track", "from": "2025-11-01", "until": "2025-12-31"},
    {"year": 2026, "volume": "45", "issue": "4", "label": "SIGGRAPH 2026 Journal Track", "from": "2026-07-01", "until": "2026-08-31"},
    {"year": 2026, "volume": "45", "issue": "6", "label": "SIGGRAPH Asia 2026 Journal Track", "from": "2026-11-01", "until": "2026-12-31"},
]


def norm_title(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii")
    text = text.lower().replace("&", "and")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def is_probable_existing_title(title_key: str, existing_titles: set[str]) -> bool:
    if not title_key:
        return False
    if title_key in existing_titles:
        return True
    tokens = title_key.split()
    if len(tokens) < 2:
        return False
    for existing in existing_titles:
        if len(existing.split()) < 2:
            continue
        if title_key in existing or existing in title_key:
            return True
    return False


def read_rows() -> list[dict[str, str]]:
    with PAPER_LIST.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CSV_FIELDS:
            raise SystemExit(f"Unexpected paper_list header: {reader.fieldnames}")
        return [dict(row) for row in reader]


def write_rows(rows: list[dict[str, str]]) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = PAPER_LIST.with_name(f"{PAPER_LIST.name}.bak_tog_crossref_{timestamp}")
    shutil.copy2(PAPER_LIST, backup)
    tmp = PAPER_LIST.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(PAPER_LIST)
    return backup


def fetch_issue(issue: dict[str, str | int]) -> list[dict[str, str]]:
    params = {
        "filter": f"issn:{TOG_ISSN},from-pub-date:{issue['from']},until-pub-date:{issue['until']}",
        "rows": "1000",
        "select": "DOI,title,container-title,volume,issue,published-print,published-online,issued,type",
    }
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "BITE local paper metadata audit (mailto:local@example.invalid)"},
    )
    with urllib.request.urlopen(request, timeout=60) as handle:
        data = json.load(handle)
    records: list[dict[str, str]] = []
    for item in data["message"]["items"]:
        if str(item.get("volume", "")) != str(issue["volume"]):
            continue
        if str(item.get("issue", "")) != str(issue["issue"]):
            continue
        titles = item.get("title") or []
        title = re.sub(r"\s+", " ", str(titles[0] if titles else "")).strip()
        doi = str(item.get("DOI") or "").strip()
        if not title or not doi:
            continue
        records.append(
            {
                "title": title,
                "doi": doi,
                "venue": f"TOG {issue['year']}",
                "year": str(issue["year"]),
                "volume": str(issue["volume"]),
                "issue": str(issue["issue"]),
                "track_label": str(issue["label"]),
                "source_url": url,
            }
        )
    return records


def collect_records() -> tuple[list[dict[str, str]], dict[str, int]]:
    all_records: list[dict[str, str]] = []
    issue_counts: dict[str, int] = {}
    for issue in ISSUES:
        records = fetch_issue(issue)
        key = f"{issue['volume']}({issue['issue']})"
        issue_counts[key] = len(records)
        all_records.extend(records)
        time.sleep(0.2)
    return all_records, issue_counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows = read_rows()
    records, issue_counts = collect_records()
    existing_titles = {norm_title(row.get("paper_title", "")) for row in rows if row.get("paper_title")}
    existing_links = {str(row.get("paper_link") or "").strip().lower() for row in rows if row.get("paper_link")}

    added: list[dict[str, str]] = []
    skipped = Counter()
    for rec in records:
        title_key = norm_title(rec["title"])
        doi_link = f"https://doi.org/{rec['doi']}"
        doi_lower = rec["doi"].lower()
        if is_probable_existing_title(title_key, existing_titles):
            skipped["title_or_short_title"] += 1
            continue
        if doi_lower in existing_links or doi_link.lower() in existing_links:
            skipped["doi"] += 1
            continue
        row = {
            "state": "Wait",
            "importance": "",
            "paper_title": rec["title"],
            "venue": rec["venue"],
            "project_link_or_github_link": "",
            "paper_link": doi_link,
            "sort": f"{rec['track_label']} / TOG {rec['volume']}({rec['issue']}) / Crossref ISSN {TOG_ISSN}",
            "pdf_path": "",
        }
        rows.append(row)
        added.append(row)
        existing_titles.add(title_key)
        existing_links.add(doi_lower)
        existing_links.add(doi_link.lower())

    with RECORDS_OUT.open("w", encoding="utf-8") as handle:
        for rec in records:
            handle.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "records_out": str(RECORDS_OUT.relative_to(ROOT)),
        "source": "Crossref works API filtered by ACM TOG ISSN 0730-0301 and client-filtered volume/issue",
        "issue_counts": issue_counts,
        "source_records": len(records),
        "added_rows": len(added),
        "skipped_existing": dict(skipped),
        "sample_added": added[:20],
        "paper_list_backup": "",
        "selection_rule": "ACM TOG volume/issue pairs associated with SIGGRAPH/SIGGRAPH Asia Journal Track from 2022 onward.",
    }
    if added and not args.dry_run:
        backup = write_rows(rows)
        report["paper_list_backup"] = str(backup.relative_to(ROOT))
    REPORT_OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
