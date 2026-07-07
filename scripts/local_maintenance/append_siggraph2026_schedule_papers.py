#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag


ROOT = Path(__file__).resolve().parents[2]
PAPER_LIST = ROOT / "obsidian-vault" / "paper_list.csv"
RUN_DIR = ROOT / "paperSources" / "sig_coverage_20260629"
PDF_SOURCE = RUN_DIR / "SIGGRAPH-2026-TECHNICAL-PAPERS-CONDITIONALLY-ACCEPTED-PAPERS.pdf"
RECORDS_OUT = RUN_DIR / "sig2026_schedule_records.jsonl"
REPORT_OUT = RUN_DIR / "append_siggraph2026_schedule_report.json"
SCHEDULE_BASE = "https://s2026.conference-schedule.org/"

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
    backup = PAPER_LIST.with_name(f"{PAPER_LIST.name}.bak_sig2026_{timestamp}")
    shutil.copy2(PAPER_LIST, backup)
    tmp = PAPER_LIST.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(PAPER_LIST)
    return backup


def first_title_link(row: Tag, ssid: str) -> Tag | None:
    link = row.select_one("td.title-speakers-td > a")
    if link:
        return link
    for candidate in row.find_all("a", href=True):
        if f"id={ssid}" in candidate["href"]:
            return candidate
    return None


def extract_session_title(soup: BeautifulSoup, psid: str) -> str:
    for row in soup.find_all("tr"):
        if row.get("psid") != psid:
            continue
        classes = set(row.get("class") or [])
        ssid = row.get("ssid", "")
        if "presentation-row" not in classes or ssid in {"", "none"}:
            continue
        link = row.select_one(".presentation-title a") or row.find("a")
        if link:
            return clean_text(link.get_text(" ", strip=True))
    return ""


def parse_schedule_records() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for path in sorted(RUN_DIR.glob("sig2026_snippet_*.html")):
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
        date = date_match.group(1) if date_match else ""
        soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
        session_title_cache: dict[str, str] = {}
        for row in soup.find_all("tr"):
            ssid = row.get("ssid", "")
            if not re.fullmatch(r"(papers|paperstog)_\d+", ssid):
                continue
            if ssid in seen_ids:
                raise SystemExit(f"Duplicate schedule id in snippets: {ssid}")
            seen_ids.add(ssid)
            psid = row.get("psid", "")
            link = first_title_link(row, ssid)
            title = clean_text(link.get_text(" ", strip=True) if link else "")
            if not title:
                raise SystemExit(f"Missing title for schedule id {ssid} in {path.name}")
            href = urljoin(SCHEDULE_BASE, link.get("href", "")) if link else ""
            if psid not in session_title_cache:
                session_title_cache[psid] = extract_session_title(soup, psid)
            track = "Journal/ACM TOG Track" if ssid.startswith("paperstog_") else "Conference Track"
            authors = [
                clean_text(a.get_text(" ", strip=True))
                for a in row.select(".author .presenter-name a")
                if clean_text(a.get_text(" ", strip=True))
            ]
            start = row.select_one(".start-time")
            end = row.select_one(".end-time")
            image = row.select_one("img.representative-img")
            records.append(
                {
                    "paper_id": ssid,
                    "psid": psid,
                    "title": title,
                    "venue": "SIGGRAPH 2026",
                    "track": track,
                    "date": date,
                    "start_utc": start.get("utc_time", "") if start else "",
                    "end_utc": end.get("utc_time", "") if end else "",
                    "session_title": session_title_cache[psid],
                    "paper_link": href,
                    "authors": "; ".join(authors),
                    "representative_image": urljoin(SCHEDULE_BASE, image.get("src", "")) if image else "",
                    "source_file": str(path.relative_to(ROOT)),
                }
            )
    return records


def load_pdf_ids() -> set[str]:
    if not PDF_SOURCE.exists():
        return set()
    text = subprocess.check_output(["pdftotext", str(PDF_SOURCE), "-"], text=True)
    return set(re.findall(r"^(?:papers|paperstog)_\d+", text, flags=re.MULTILINE))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows = read_rows()
    existing_titles = {norm_title(row.get("paper_title", "")) for row in rows if row.get("paper_title")}
    existing_links = {clean_text(row.get("paper_link", "")).lower() for row in rows if row.get("paper_link")}

    records = parse_schedule_records()
    pdf_ids = load_pdf_ids()
    schedule_ids = {record["paper_id"] for record in records}

    added: list[dict[str, str]] = []
    skipped = Counter()
    for rec in records:
        title_key = norm_title(rec["title"])
        link_key = rec["paper_link"].lower()
        if title_key in existing_titles:
            skipped["title"] += 1
            continue
        if link_key and link_key in existing_links:
            skipped["link"] += 1
            continue
        sort = "SIGGRAPH 2026 / Technical Papers / Official Schedule / " + rec["track"]
        if rec["session_title"]:
            sort += " / " + rec["session_title"]
        row = {
            "state": "Wait",
            "importance": "",
            "paper_title": rec["title"],
            "venue": rec["venue"],
            "project_link_or_github_link": "",
            "paper_link": rec["paper_link"],
            "sort": sort,
            "pdf_path": "",
        }
        rows.append(row)
        added.append(row)
        existing_titles.add(title_key)
        if link_key:
            existing_links.add(link_key)

    RUN_DIR.mkdir(parents=True, exist_ok=True)
    with RECORDS_OUT.open("w", encoding="utf-8") as handle:
        for rec in records:
            handle.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "source_schedule_snippets": [
            str(path.relative_to(ROOT)) for path in sorted(RUN_DIR.glob("sig2026_snippet_*.html"))
        ],
        "source_conditional_pdf": str(PDF_SOURCE.relative_to(ROOT)) if PDF_SOURCE.exists() else "",
        "records_out": str(RECORDS_OUT.relative_to(ROOT)),
        "schedule_records": len(records),
        "schedule_track_counts": dict(Counter(record["track"] for record in records)),
        "schedule_ids": len(schedule_ids),
        "conditional_pdf_ids": len(pdf_ids),
        "overlap_pdf_schedule_ids": len(pdf_ids & schedule_ids),
        "pdf_ids_not_in_schedule": sorted(pdf_ids - schedule_ids),
        "schedule_ids_not_in_pdf": sorted(schedule_ids - pdf_ids),
        "added_rows": len(added),
        "skipped_existing": dict(skipped),
        "sample_added": added[:20],
        "paper_list_backup": "",
        "selection_rule": (
            "Official SIGGRAPH 2026 Linklings schedule rows under Technical Paper filter "
            "with ssid matching papers_* or paperstog_*; PDF-only ids are reported but not "
            "added because the PDF has ids without titles."
        ),
    }
    if added and not args.dry_run:
        backup = write_rows(rows)
        report["paper_list_backup"] = str(backup.relative_to(ROOT))

    REPORT_OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
