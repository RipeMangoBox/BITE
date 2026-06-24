#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[2]
RUN_DIR = ROOT / "paperSources" / "siggraph_full_collect_20260624"
PAPER_LIST = ROOT / "obsidian-vault" / "paper_list.csv"
PDF_ROOT = ROOT / "obsidian-vault" / "paperPDFs"
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
TARGET_VENUES = {
    "SIGGRAPH 2022",
    "SIGGRAPH 2023",
    "SIGGRAPH 2024",
    "SIGGRAPH ASIA 2022",
    "SIGGRAPH ASIA 2023",
    "SIGGRAPH ASIA 2024",
}


def safe_slug(text: str, max_len: int = 180) -> str:
    text = re.sub(r"[^0-9A-Za-z]+", "_", text or "").strip("_")
    text = re.sub(r"_+", "_", text)
    return text[:max_len].rstrip("_") or "paper"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def is_valid_pdf(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        return False
    try:
        with path.open("rb") as handle:
            if not handle.read(8).startswith(b"%PDF"):
                return False
        with fitz.open(path) as doc:
            return doc.page_count > 0
    except Exception:
        return False


def resolve_pdf(raw: str) -> Path | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute():
        path = ROOT / path
    return path


def read_rows() -> list[dict[str, str]]:
    with PAPER_LIST.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CSV_FIELDS:
            raise SystemExit(f"Unexpected paper_list header: {reader.fieldnames}")
        return [dict(row) for row in reader]


def write_rows(rows: list[dict[str, str]]) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = PAPER_LIST.with_name(f"{PAPER_LIST.name}.bak_{timestamp}")
    shutil.copy2(PAPER_LIST, backup)
    tmp = PAPER_LIST.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(PAPER_LIST)
    return backup


def main() -> None:
    rows = read_rows()
    before = Counter()
    after = Counter()
    updated = 0
    already_valid = 0
    missing_by_venue = defaultdict(int)
    new_by_venue = defaultdict(int)
    for row in rows:
        venue = row.get("venue", "")
        if venue not in TARGET_VENUES:
            continue
        before[(venue, "rows")] += 1
        old = resolve_pdf(row.get("pdf_path", ""))
        if old and is_valid_pdf(old):
            already_valid += 1
            after[(venue, "valid_pdf")] += 1
            continue
        target = PDF_ROOT / venue.replace(" ", "_") / f"{safe_slug(row.get('paper_title', ''))}.pdf"
        if is_valid_pdf(target):
            row["pdf_path"] = rel(target)
            if row.get("state") != "checked":
                row["state"] = "Downloaded"
            updated += 1
            new_by_venue[venue] += 1
            after[(venue, "valid_pdf")] += 1
        else:
            missing_by_venue[venue] += 1
    backup = write_rows(rows) if updated else ""
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "paper_list_backup": rel(backup) if backup else "",
        "updated_rows": updated,
        "already_valid_rows": already_valid,
        "new_downloaded_by_venue": dict(new_by_venue),
        "missing_pdf_by_venue": dict(missing_by_venue),
        "valid_pdf_by_venue": {venue: after[(venue, "valid_pdf")] for venue in sorted(TARGET_VENUES)},
        "note": "The prior downloader was terminated after 1475/1476 tasks because the final request hung; this sync reports PDFs actually present and readable on disk.",
    }
    path = RUN_DIR / f"download_sync_report_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"report": rel(path), **report}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
