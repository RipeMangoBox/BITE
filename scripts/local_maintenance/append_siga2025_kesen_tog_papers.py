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
SOURCE = RUN_DIR / "kesen_siga2025Papers.md"
RECORDS_OUT = RUN_DIR / "kesen_siga2025_records.jsonl"
REPORT_OUT = RUN_DIR / "append_siga2025_kesen_tog_report.json"

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


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def read_rows() -> list[dict[str, str]]:
    with PAPER_LIST.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CSV_FIELDS:
            raise SystemExit(f"Unexpected paper_list header: {reader.fieldnames}")
        return [dict(row) for row in reader]


def write_rows(rows: list[dict[str, str]]) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = PAPER_LIST.with_name(f"{PAPER_LIST.name}.bak_siga2025_kesen_{timestamp}")
    shutil.copy2(PAPER_LIST, backup)
    tmp = PAPER_LIST.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(PAPER_LIST)
    return backup


def extract_first_link(chunk: str, image_label: str) -> str:
    pattern = (
        r"\[!\[Image\s+\d+:\s+"
        + re.escape(image_label)
        + r"\]\([^)]+\)\]\((https?://[^)]+)\)"
    )
    match = re.search(pattern, chunk)
    return clean_text(match.group(1) if match else "")


def parse_records() -> list[dict[str, str]]:
    text = SOURCE.read_text(encoding="utf-8")
    start = text.find("## 3D Reconstruction")
    if start < 0:
        raise SystemExit("Could not locate first SIGA 2025 topic section in Ke-Sen source")
    body = text[start:]
    starts = list(re.finditer(r"\*\*(?P<title>[^*\n]+?)\*\*\[!\[Image\s+\d+:\s+ACM DOI\]", body))
    records: list[dict[str, str]] = []
    for idx, match in enumerate(starts):
        chunk = body[match.start() : starts[idx + 1].start() if idx + 1 < len(starts) else len(body)]
        tag = re.search(r"\(\*\*(SIG/TOG|SIG|TOG)\*\*\)", chunk)
        doi = extract_first_link(chunk, "ACM DOI")
        abstract = extract_first_link(chunk, "Paper Abstract")
        preprint = extract_first_link(chunk, "Author Preprint")
        code = extract_first_link(chunk, "Demo Program or Source Code")
        records.append(
            {
                "title": clean_text(match.group("title")),
                "track_marker": tag.group(1) if tag else "",
                "doi": doi,
                "paper_abstract": abstract,
                "author_preprint": preprint,
                "code": code,
                "source": str(SOURCE.relative_to(ROOT)),
            }
        )
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--include-sig",
        action="store_true",
        help="Also import SIG conference-track rows. Default imports only SIG/TOG and TOG.",
    )
    args = parser.parse_args()

    rows = read_rows()
    records = parse_records()
    selected_markers = {"SIG/TOG", "TOG"} if not args.include_sig else {"SIG/TOG", "SIG", "TOG"}
    selected = [rec for rec in records if rec["track_marker"] in selected_markers]

    existing_titles = {norm_title(row.get("paper_title", "")) for row in rows if row.get("paper_title")}
    existing_links = {clean_text(row.get("paper_link", "")).lower() for row in rows if row.get("paper_link")}
    added: list[dict[str, str]] = []
    skipped = Counter()
    for rec in selected:
        title_key = norm_title(rec["title"])
        link = rec["doi"] or rec["author_preprint"] or rec["paper_abstract"]
        link_key = link.lower()
        if title_key in existing_titles:
            skipped["title"] += 1
            continue
        if link_key and link_key in existing_links:
            skipped["link"] += 1
            continue
        row = {
            "state": "Wait",
            "importance": "",
            "paper_title": rec["title"],
            "venue": "SIGGRAPH ASIA 2025",
            "project_link_or_github_link": rec["code"],
            "paper_link": link,
            "sort": f"SIGGRAPH ASIA 2025 / Technical Papers / Ke-Sen / {rec['track_marker']}",
            "pdf_path": "",
        }
        rows.append(row)
        added.append(row)
        existing_titles.add(title_key)
        if link_key:
            existing_links.add(link_key)

    with RECORDS_OUT.open("w", encoding="utf-8") as handle:
        for rec in records:
            handle.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "source": str(SOURCE.relative_to(ROOT)),
        "records_out": str(RECORDS_OUT.relative_to(ROOT)),
        "source_records": len(records),
        "source_marker_counts": dict(Counter(rec["track_marker"] for rec in records)),
        "selected_markers": sorted(selected_markers),
        "selected_records": len(selected),
        "added_rows": len(added),
        "skipped_existing": dict(skipped),
        "sample_added": added[:20],
        "paper_list_backup": "",
        "selection_rule": (
            "Ke-Sen SIGGRAPH Asia 2025 papers page, whose header says ACM permission and "
            "defines SIG/TOG as conditionally accepted Journal Paper, SIG as Conference Paper, "
            "and TOG as selected ACM TOG Paper. Default import excludes SIG because ACM "
            "10.1145/3757377 Crossref already covers the conference proceedings."
        ),
    }
    if added and not args.dry_run:
        backup = write_rows(rows)
        report["paper_list_backup"] = str(backup.relative_to(ROOT))

    REPORT_OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
