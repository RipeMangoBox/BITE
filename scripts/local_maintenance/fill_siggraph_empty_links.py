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
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPER_LIST = ROOT / "obsidian-vault" / "paper_list.csv"
RUN_DIR = ROOT / "paperSources" / "sig_link_completion_20260629"
SIG2025_RECORDS = RUN_DIR / "papercopilot_sig2025_records.jsonl"
RAW_DIR = ROOT / "paperSources" / "siggraph_full_collect_20260624" / "raw"
REPORT_PATH = RUN_DIR / "fill_siggraph_empty_links_report.json"

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


def clean(text: object) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def read_rows() -> list[dict[str, str]]:
    with PAPER_LIST.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CSV_FIELDS:
            raise SystemExit(f"Unexpected paper_list header: {reader.fieldnames}")
        return [dict(row) for row in reader]


def write_rows(rows: list[dict[str, str]]) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = PAPER_LIST.with_name(f"{PAPER_LIST.name}.bak_sig_links_{timestamp}")
    shutil.copy2(PAPER_LIST, backup)
    tmp = PAPER_LIST.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(PAPER_LIST)
    return backup


def load_sig2025_records() -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    if not SIG2025_RECORDS.exists():
        return records
    with SIG2025_RECORDS.open(encoding="utf-8") as handle:
        for line in handle:
            rec = json.loads(line)
            key = norm_title(rec.get("title", ""))
            if not key:
                continue
            records[key] = {
                "paper_link": clean(rec.get("paper_link")),
                "status": clean(rec.get("status")),
                "session": clean(rec.get("session")),
                "source": str(SIG2025_RECORDS.relative_to(ROOT)),
            }
    return records


def schedule_url(venue: str, ssid: str, psid: str) -> str:
    if venue == "SIGGRAPH 2022":
        host = "https://s2022.conference-schedule.org"
    elif venue == "SIGGRAPH ASIA 2022":
        host = "https://sa2022.conference-schedule.org"
    else:
        return ""
    if not ssid or not psid:
        return ""
    return f"{host}/presentation/?id={ssid}&sess={psid}"


def load_2022_records() -> dict[tuple[str, str], dict[str, str]]:
    records: dict[tuple[str, str], dict[str, str]] = {}
    sources = [
        ("siggraph2022.json", "SIGGRAPH 2022"),
        ("siggraphasia2022.json", "SIGGRAPH ASIA 2022"),
    ]
    for filename, venue in sources:
        path = RAW_DIR / filename
        if not path.exists():
            continue
        for rec in json.loads(path.read_text(encoding="utf-8")):
            key = norm_title(rec.get("title", ""))
            if not key:
                continue
            doi = clean(rec.get("doi"))
            url_paper = clean(rec.get("url_paper"))
            official = schedule_url(venue, clean(rec.get("ssid")), clean(rec.get("psid")))
            paper_link = doi or url_paper or official
            records[(venue, key)] = {
                "paper_link": paper_link,
                "status": clean(rec.get("status")),
                "session": clean(rec.get("sess")),
                "source": str(path.relative_to(ROOT)),
            }
    return records


def load_collected_records() -> list[dict[str, str]]:
    path = ROOT / "paperSources" / "siggraph_full_collect_20260624" / "collected_records.jsonl"
    records: list[dict[str, str]] = []
    if not path.exists():
        return records
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            rec = json.loads(line)
            records.append(
                {
                    "venue": clean(rec.get("venue")).replace("_", " "),
                    "title": clean(rec.get("paper_title")),
                    "paper_link": clean(rec.get("doi")) or clean(rec.get("paper_link")) or clean(rec.get("paper_copilot_url")),
                    "status": clean(rec.get("status")),
                    "session": clean(rec.get("session")),
                    "source": str(path.relative_to(ROOT)),
                }
            )
    return records


def load_raw_records() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    source_venues = {
        "siggraph2022.json": "SIGGRAPH 2022",
        "siggraph2023.json": "SIGGRAPH 2023",
        "siggraph2024.json": "SIGGRAPH 2024",
        "siggraphasia2022.json": "SIGGRAPH ASIA 2022",
        "siggraphasia2023.json": "SIGGRAPH ASIA 2023",
        "siggraphasia2024.json": "SIGGRAPH ASIA 2024",
    }
    for filename, venue in source_venues.items():
        path = RAW_DIR / filename
        if not path.exists():
            continue
        for rec in json.loads(path.read_text(encoding="utf-8")):
            title = clean(rec.get("title"))
            if not title:
                continue
            paper_link = clean(rec.get("doi")) or clean(rec.get("url_paper")) or schedule_url(
                venue, clean(rec.get("ssid")), clean(rec.get("psid"))
            )
            records.append(
                {
                    "venue": venue,
                    "title": title,
                    "paper_link": paper_link,
                    "status": clean(rec.get("status")),
                    "session": clean(rec.get("sess")),
                    "source": str(path.relative_to(ROOT)),
                }
            )
    return records


def load_sig2025_record_list() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    if not SIG2025_RECORDS.exists():
        return records
    with SIG2025_RECORDS.open(encoding="utf-8") as handle:
        for line in handle:
            rec = json.loads(line)
            records.append(
                {
                    "venue": "SIGGRAPH 2025",
                    "title": clean(rec.get("title")),
                    "paper_link": clean(rec.get("paper_link")),
                    "status": clean(rec.get("status")),
                    "session": clean(rec.get("session")),
                    "source": str(SIG2025_RECORDS.relative_to(ROOT)),
                }
            )
    return records


def stripped_title_key(key: str) -> str:
    key = re.sub(r"^[a-z0-9]+ et al ", "", key)
    words = key.split()
    if len(words) > 4 and words[0].isalpha() and len(words[0]) <= 10:
        return " ".join(words[1:])
    return key


def title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def find_record_for_row(row: dict[str, str], records: list[dict[str, str]]) -> dict[str, str] | None:
    row_venue = clean(row.get("venue")).replace("_", " ")
    row_key = norm_title(row.get("paper_title", ""))
    row_keys = {row_key, stripped_title_key(row_key)}
    best: tuple[float, dict[str, str]] | None = None
    for rec in records:
        if clean(rec.get("venue")).replace("_", " ") != row_venue:
            continue
        rec_key = norm_title(rec.get("title", ""))
        if not rec_key:
            continue
        if rec_key in row_keys or any(candidate.endswith(" " + rec_key) for candidate in row_keys):
            return rec
        score = max(title_similarity(candidate, rec_key) for candidate in row_keys)
        if score >= 0.94 and (best is None or score > best[0]):
            best = (score, rec)
    return best[1] if best else None


def doi_from_pdf(row: dict[str, str]) -> str:
    pdf_path = clean(row.get("pdf_path"))
    if not pdf_path:
        return ""
    path = (ROOT / pdf_path).resolve()
    try:
        text = path.read_bytes()[:2]
    except OSError:
        return ""
    if text != b"%P":
        return ""
    try:
        import subprocess

        proc = subprocess.run(
            ["pdftotext", "-f", "1", "-l", "1", str(path), "-"],
            cwd=ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    matches = re.findall(r"https://doi\.org/10\.1145/[0-9.]+|10\.1145/[0-9.]+", proc.stdout)
    for match in matches:
        doi = match if match.startswith("https://doi.org/") else f"https://doi.org/{match}"
        if "XXXX" not in doi:
            return doi.rstrip(".,);")
    return ""


def is_sig_row(row: dict[str, str]) -> bool:
    text = f"{row.get('venue', '')} {row.get('sort', '')}".upper()
    return any(token in text for token in ("SIGGRAPH", "SIGA", "TOG"))


def fill_rows(rows: list[dict[str, str]], *, all_states: bool) -> tuple[list[dict[str, str]], dict[str, object]]:
    sig2025 = load_sig2025_records()
    records2022 = load_2022_records()
    all_records = load_sig2025_record_list() + load_collected_records() + load_raw_records()
    updates: list[dict[str, str]] = []
    unmatched: list[dict[str, str]] = []
    update_counts = Counter()

    for line_no, row in enumerate(rows, start=2):
        if (not all_states and row.get("state") != "Wait") or not is_sig_row(row):
            continue
        if clean(row.get("paper_link")):
            continue

        venue = clean(row.get("venue"))
        title = clean(row.get("paper_title"))
        key = norm_title(title)
        rec: dict[str, str] | None = None
        source_kind = ""
        if venue == "SIGGRAPH 2025":
            rec = sig2025.get(key)
            source_kind = "papercopilot_sig2025_ajax"
        elif venue in {"SIGGRAPH 2022", "SIGGRAPH ASIA 2022"}:
            rec = records2022.get((venue, key))
            source_kind = "papercopilot_2022_raw"

        pdf_doi = doi_from_pdf(row) if all_states else ""
        if pdf_doi:
            rec = {
                "paper_link": pdf_doi,
                "status": "",
                "session": "",
                "source": clean(row.get("pdf_path")),
            }
            source_kind = "pdf_first_page_doi"
        elif rec is None and all_states:
            rec = find_record_for_row(row, all_records)
            source_kind = "collected_or_raw_record" if rec else source_kind

        if not rec or not clean(rec.get("paper_link")):
            unmatched.append({"line": str(line_no), "venue": venue, "paper_title": title})
            continue

        before = dict(row)
        row["paper_link"] = clean(rec["paper_link"])
        if not clean(row.get("sort")):
            sort_parts = [venue, clean(rec.get("status")), clean(rec.get("session"))]
            row["sort"] = " / ".join(part for part in sort_parts if part)

        changed_fields = [name for name in CSV_FIELDS if row.get(name) != before.get(name)]
        for field in changed_fields:
            update_counts[field] += 1
        updates.append(
            {
                "line": str(line_no),
                "venue": venue,
                "paper_title": title,
                "paper_link": row["paper_link"],
                "source_kind": source_kind,
                "record_source": clean(rec.get("source")),
                "changed_fields": ",".join(changed_fields),
            }
        )

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_rows": len(updates),
        "updated_fields": dict(update_counts),
        "unmatched_rows": len(unmatched),
        "updates_by_venue": dict(Counter(item["venue"] for item in updates)),
        "updates_by_source_kind": dict(Counter(item["source_kind"] for item in updates)),
        "unmatched": unmatched,
        "sample_updates": updates[:20],
    }
    return rows, report


def remaining_empty_link_count(rows: list[dict[str, str]]) -> int:
    return sum(
        1
        for row in rows
        if row.get("state") == "Wait" and is_sig_row(row) and not clean(row.get("paper_link"))
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--all-states", action="store_true", help="Also fill legacy checked/Downloaded rows.")
    args = parser.parse_args()

    rows = read_rows()
    before_empty = remaining_empty_link_count(rows)
    rows, report = fill_rows(rows, all_states=args.all_states)
    after_empty = remaining_empty_link_count(rows)
    report.update(
        {
            "dry_run": args.dry_run,
            "all_states": args.all_states,
            "empty_wait_sig_paper_link_before": before_empty,
            "empty_wait_sig_paper_link_after": after_empty,
            "paper_list_backup": "",
        }
    )
    if report["updated_rows"] and not args.dry_run:
        backup = write_rows(rows)
        report["paper_list_backup"] = str(backup.relative_to(ROOT))

    RUN_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
