#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag


ROOT = Path(__file__).resolve().parents[2]
RUN_DIR = ROOT / "paperSources" / "siggraph_full_collect_20260624"
RAW_DIR = RUN_DIR / "raw"
PAPER_LIST = ROOT / "obsidian-vault" / "paper_list.csv"
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

SOURCES = [
    ("siggraph2022.json", "SIGGRAPH 2022", 2022, "SIGGRAPH"),
    ("siggraph2023.json", "SIGGRAPH 2023", 2023, "SIGGRAPH"),
    ("siggraph2024.json", "SIGGRAPH 2024", 2024, "SIGGRAPH"),
    ("siggraphasia2022.json", "SIGGRAPH ASIA 2022", 2022, "SIGGRAPH ASIA"),
    ("siggraphasia2023.json", "SIGGRAPH ASIA 2023", 2023, "SIGGRAPH ASIA"),
    ("siggraphasia2024.json", "SIGGRAPH ASIA 2024", 2024, "SIGGRAPH ASIA"),
]

KESEN_SOURCES = [
    ("sig2022.html", "https://www.realtimerendering.com/kesen/sig2022.html"),
    ("sig2023.html", "https://www.realtimerendering.com/kesen/sig2023.html"),
    ("sig2024.html", "https://www.realtimerendering.com/kesen/sig2024.html"),
    ("siga2022Papers.htm", "https://www.realtimerendering.com/kesen/siga2022Papers.htm"),
    ("siga2024Papers.htm", "https://www.realtimerendering.com/kesen/siga2024Papers.htm"),
]

PAPER_ALTS = {"Author Preprint", "Author version", "Paper Abstract", "ACM DOI"}
PROJECT_ALTS = {"Paper Abstract", "Related Links"}
CODE_ALTS = {"Demo Program or Source Code"}
DATA_ALTS = {"Paper Data"}


def norm_title(text: str) -> str:
    text = re.sub(r"\$([^$]+)\$", r"\1", text or "")
    text = text.replace("–", "-").replace("—", "-").replace("’", "'")
    text = text.replace("‐", "-").replace("‑", "-")
    text = re.sub(r"[^0-9a-zA-Z]+", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def normalize_title_display(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def safe_slug(text: str, max_len: int = 180) -> str:
    text = re.sub(r"[^0-9A-Za-z]+", "_", text or "").strip("_")
    text = re.sub(r"_+", "_", text)
    return text[:max_len].rstrip("_") or "paper"


def prefer_link(old: str, new: str, *, paper: bool = False) -> str:
    old = (old or "").strip()
    new = (new or "").strip()
    if not old:
        return new
    if not new:
        return old
    if paper:
        old_score = link_score(old)
        new_score = link_score(new)
        if new_score > old_score and not old.lower().startswith("https://arxiv.org"):
            return new
    return old


def link_score(url: str) -> int:
    u = (url or "").lower()
    if "arxiv.org/abs/" in u or "arxiv.org/pdf/" in u:
        return 80
    if u.endswith(".pdf") or ".pdf?" in u or "/pdf/" in u:
        return 70
    if "doi.org/" in u:
        return 55
    if "dl.acm.org/" in u:
        return 50
    if u:
        return 40
    return 0


def first_nonempty(*values: str) -> str:
    for value in values:
        value = (value or "").strip()
        if value:
            return value
    return ""


def parse_kesen_pages() -> dict[str, dict[str, object]]:
    by_title: dict[str, dict[str, object]] = {}
    for filename, base_url in KESEN_SOURCES:
        path = RAW_DIR / filename
        if not path.exists() or path.stat().st_size < 1000:
            continue
        soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "html.parser")
        for dt in soup.find_all("dt"):
            title_tag = dt.find("b")
            title = normalize_title_display(title_tag.get_text(" ", strip=True) if title_tag else dt.get_text(" ", strip=True))
            key = norm_title(title)
            if not key:
                continue
            links: list[dict[str, str]] = []
            for a in dt.find_all("a"):
                href = a.get("href")
                if not href:
                    continue
                img = a.find("img")
                alt = normalize_title_display(img.get("alt") if img else "")
                links.append({
                    "alt": alt,
                    "href": urljoin(base_url, href),
                    "text": normalize_title_display(a.get_text(" ", strip=True)),
                })
            entry = {
                "kesen_title": title,
                "kesen_page": base_url,
                "links": links,
                "paper_links": [x["href"] for x in links if x["alt"] in PAPER_ALTS],
                "project_links": [x["href"] for x in links if x["alt"] in PROJECT_ALTS],
                "code_links": [x["href"] for x in links if x["alt"] in CODE_ALTS],
                "data_links": [x["href"] for x in links if x["alt"] in DATA_ALTS],
            }
            by_title[key] = entry
    return by_title


def load_records(kesen: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for filename, venue, year, conf in SOURCES:
        source_path = RAW_DIR / filename
        rows = json.loads(source_path.read_text(encoding="utf-8"))
        for item in rows:
            title = normalize_title_display(item.get("title", ""))
            if not title:
                # PaperCopilot SIGA 2023 has one blank-title record; keep it out of
                # paper_list.csv until a reliable title source is available.
                continue
            key = norm_title(title)
            dedupe_key = (venue, key)
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            k = kesen.get(key, {})
            doi = normalize_title_display(item.get("doi", ""))
            url_paper = normalize_title_display(item.get("url_paper", ""))
            k_papers = list(k.get("paper_links") or [])
            k_projects = list(k.get("project_links") or [])
            k_codes = list(k.get("code_links") or [])
            paper_link = first_nonempty(*(k_papers[:1] or [""]), doi, url_paper)
            project_or_code = first_nonempty(*(k_codes[:1] or [""]), *(k_projects[:1] or [""]))
            status = normalize_title_display(item.get("status", ""))
            sess = normalize_title_display(item.get("sess", ""))
            sort_parts = [p for p in [status, sess] if p]
            records.append({
                "paper_title": title,
                "venue": venue,
                "year": year,
                "conference": conf,
                "paper_link": paper_link,
                "project_link_or_github_link": project_or_code,
                "sort": " / ".join(sort_parts),
                "status": status,
                "session": sess,
                "doi": doi,
                "paper_copilot_url": url_paper,
                "url_sess": normalize_title_display(item.get("url_sess", "")),
                "keywords": normalize_title_display(item.get("keywords", "")),
                "authors": normalize_title_display(item.get("author", "")),
                "affiliation": normalize_title_display(item.get("aff", "")),
                "ssid": normalize_title_display(item.get("ssid", "")),
                "psid": normalize_title_display(item.get("psid", "")),
                "source_json": filename,
                "kesen": k,
            })
    return records


def read_csv() -> list[dict[str, str]]:
    with PAPER_LIST.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CSV_FIELDS:
            raise SystemExit(f"Unexpected paper_list header: {reader.fieldnames}")
        return [dict(row) for row in reader]


def write_csv(rows: list[dict[str, str]]) -> Path:
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


def merge_records(records: list[dict[str, object]], rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], dict[str, object]]:
    by_title: dict[str, dict[str, str]] = {}
    for row in rows:
        key = norm_title(row.get("paper_title", ""))
        if key and key not in by_title:
            by_title[key] = row

    added = 0
    updated = Counter()
    unchanged = 0
    for rec in records:
        key = norm_title(str(rec["paper_title"]))
        row = by_title.get(key)
        if row is None:
            pdf_path = f"obsidian-vault/paperPDFs/{str(rec['venue']).replace(' ', '_')}/{safe_slug(str(rec['paper_title']))}.pdf"
            row = {
                "state": "Wait" if str(rec.get("paper_link") or "").strip() else "",
                "importance": "",
                "paper_title": str(rec["paper_title"]),
                "venue": str(rec["venue"]),
                "project_link_or_github_link": str(rec.get("project_link_or_github_link") or ""),
                "paper_link": str(rec.get("paper_link") or ""),
                "sort": str(rec.get("sort") or ""),
                "pdf_path": "",
            }
            rows.append(row)
            by_title[key] = row
            added += 1
            continue

        before = dict(row)
        if not row.get("paper_link", "").strip():
            row["paper_link"] = str(rec.get("paper_link") or "")
        else:
            row["paper_link"] = prefer_link(row.get("paper_link", ""), str(rec.get("paper_link") or ""), paper=True)
        if not row.get("project_link_or_github_link", "").strip():
            row["project_link_or_github_link"] = str(rec.get("project_link_or_github_link") or "")
        if not row.get("sort", "").strip():
            row["sort"] = str(rec.get("sort") or "")
        if not row.get("venue", "").strip():
            row["venue"] = str(rec["venue"])
        if row != before:
            for name in CSV_FIELDS:
                if row.get(name) != before.get(name):
                    updated[name] += 1
        else:
            unchanged += 1

    report = {
        "records": len(records),
        "added": added,
        "updated_fields": dict(updated),
        "unchanged_existing_records": unchanged,
    }
    return rows, report


def main() -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    kesen = parse_kesen_pages()
    records = load_records(kesen)
    rows = read_csv()
    before_count = len(rows)
    rows, merge_report = merge_records(records, rows)
    backup = write_csv(rows)

    with (RUN_DIR / "collected_records.jsonl").open("w", encoding="utf-8") as handle:
        for rec in records:
            handle.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

    source_counts = Counter(str(rec["venue"]) for rec in records)
    status_counts = Counter(f"{rec['venue']}::{rec.get('status') or ''}" for rec in records)
    link_counts = {
        "with_paper_link": sum(bool(str(rec.get("paper_link") or "").strip()) for rec in records),
        "with_project_or_code": sum(bool(str(rec.get("project_link_or_github_link") or "").strip()) for rec in records),
        "with_kesen_match": sum(bool(rec.get("kesen")) for rec in records),
    }
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "paper_list_backup": str(backup.relative_to(ROOT)),
        "paper_list_rows_before": before_count,
        "paper_list_rows_after": len(rows),
        "source_counts": dict(source_counts),
        "status_counts": dict(status_counts),
        "link_counts": link_counts,
        "merge": merge_report,
        "notes": [
            "SIGGRAPH Asia 2023 Ke-Sen page was not available in cached raw files; records rely on PaperCopilot JSON.",
            "CSV has one project/code column, so collected_records.jsonl preserves separated Ke-Sen paper/project/code/data links.",
            "Blank-title source records are excluded from paper_list.csv rather than fabricated.",
        ],
    }
    (RUN_DIR / "merge_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
