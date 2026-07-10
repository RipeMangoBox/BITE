#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.download_analysis_log_pdfs import (
    ARXIV_ID_RE,
    iter_special_url_variants,
    normalize_spaces,
)


LOG_TARGETS = {
    "P13": REPO_ROOT
    / "paperAnalysis"
    / "processing"
    / "github_awesome"
    / "soraproducer__awesome-human-interaction-motion-generation"
    / "analysis_log.csv",
    "P14": REPO_ROOT
    / "paperAnalysis"
    / "processing"
    / "github_awesome"
    / "sun-haoyuan23__awesome-rl-based-reasoning-mllms"
    / "analysis_log.csv",
}
FIELDS = [
    "state",
    "importance",
    "paper_title",
    "venue",
    "project_link_or_github_link",
    "paper_link",
    "sort",
    "pdf_path",
]


@dataclass
class RetrySummary:
    tag: str
    attempted: int = 0
    repaired: int = 0
    arxiv_direct_fixed: int = 0
    still_missing: int = 0


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def arxiv_pdf_candidates(url: str) -> list[str]:
    match = ARXIV_ID_RE.search(url or "")
    if not match:
        return []
    arxiv_id = match.group("id")
    return [
        f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        f"https://arxiv.org/pdf/{arxiv_id}",
    ]


def build_candidates(row: dict[str, str]) -> list[str]:
    seen: set[str] = set()
    candidates: list[str] = []
    for url in arxiv_pdf_candidates(row.get("paper_link", "")):
        norm = normalize_spaces(url)
        if norm and norm not in seen:
            seen.add(norm)
            candidates.append(norm)
    for raw in (row.get("paper_link", ""), row.get("project_link_or_github_link", "")):
        for url in iter_special_url_variants(normalize_spaces(raw)):
            if url and url not in seen:
                seen.add(url)
                candidates.append(url)
    return candidates


def maybe_normalize_arxiv_link(row: dict[str, str], source_url: str) -> None:
    match = ARXIV_ID_RE.search(source_url or row.get("paper_link", ""))
    if not match:
        return
    row["paper_link"] = f"https://arxiv.org/abs/{match.group('id')}"


def direct_download_pdf(candidate: str, dest: Path, timeout: int) -> bool:
    response = requests.get(
        candidate,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
        },
        timeout=timeout,
        allow_redirects=True,
    )
    response.raise_for_status()
    data = response.content
    content_type = (response.headers.get("Content-Type") or "").lower()
    if "application/pdf" not in content_type and not data.startswith(b"%PDF"):
        return False
    if len(data) < 5000:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return True


def retry_log(path: Path, tag: str, dry_run: bool, timeout: int) -> RetrySummary:
    rows = read_rows(path)
    summary = RetrySummary(tag=tag)
    for row in rows:
        if row.get("state") != "Missing":
            continue
        summary.attempted += 1
        dest = REPO_ROOT / row["pdf_path"]
        repaired = False
        for candidate in build_candidates(row):
            if dry_run:
                repaired = True
                maybe_normalize_arxiv_link(row, candidate)
                break
            try:
                ok = direct_download_pdf(candidate, dest, timeout)
            except Exception:
                ok = False
            if ok:
                row["state"] = "Downloaded"
                maybe_normalize_arxiv_link(row, candidate)
                summary.repaired += 1
                if "arxiv.org/pdf/" in candidate:
                    summary.arxiv_direct_fixed += 1
                repaired = True
                break
            time.sleep(0.2)
        if not repaired:
            summary.still_missing += 1

    if not dry_run:
        write_rows(path, rows)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retry Tier 3 missing PDFs with direct sequential URLs.")
    parser.add_argument("--targets", default="P13,P14", help="Comma-separated targets from P13,P14")
    parser.add_argument("--timeout", type=int, default=30, help="Per-request timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Do not write CSVs or download PDFs.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    requested = [part.strip().upper() for part in args.targets.split(",") if part.strip()]
    summaries = []
    for tag in requested:
        path = LOG_TARGETS.get(tag)
        if path is None:
            raise SystemExit(f"unknown target: {tag}")
        summary = retry_log(path, tag, args.dry_run, args.timeout)
        summaries.append(summary)
        print(json.dumps(asdict(summary), ensure_ascii=False))
    print(json.dumps({"summary": [asdict(item) for item in summaries]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
