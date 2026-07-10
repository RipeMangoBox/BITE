#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
PAPER_TOOL_DIR = (
    REPO_ROOT
    / ".claude"
    / "skills"
    / "papers-download-from-list"
    / "scripts"
    / "paper_download_tools"
)
if str(PAPER_TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(PAPER_TOOL_DIR))

from search_download_by_info import (  # type: ignore[import-not-found]
    PaperSpec,
    choose_best_match,
    download_pdf,
    extract_arxiv_id,
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
class LogSummary:
    tag: str
    rows_scanned: int = 0
    repaired: int = 0
    paper_link_updated: int = 0
    still_missing: int = 0
    skipped_non_arxiv: int = 0


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def build_spec(row: dict[str, str]) -> PaperSpec:
    return PaperSpec(
        query=row.get("paper_title", "").strip(),
        title=row.get("paper_title", "").strip(),
        alias=row.get("paper_title", "").strip().split(":", 1)[0].strip(),
        arxiv_id=extract_arxiv_id(row.get("paper_link", "").strip()),
        paper_link=row.get("paper_link", "").strip(),
        project_link=row.get("project_link_or_github_link", "").strip() or "no",
        importance=row.get("importance", "").strip() or "B",
        category=row.get("sort", "").strip() or "Uncategorized",
        sort=row.get("sort", "").strip() or "Uncategorized",
        venue=row.get("venue", "").strip(),
        require_keywords=[],
    )


def repair_log(path: Path, tag: str, dry_run: bool) -> LogSummary:
    rows = read_rows(path)
    summary = LogSummary(tag=tag)
    for row in rows:
        if row.get("state") != "Missing":
            continue
        summary.rows_scanned += 1
        paper_link = (row.get("paper_link") or "").strip()
        title = (row.get("paper_title") or "").strip()
        if "arxiv.org" not in paper_link.lower() and not extract_arxiv_id(paper_link):
            summary.skipped_non_arxiv += 1
            summary.still_missing += 1
            continue

        spec = build_spec(row)
        try:
            paper, _reason = choose_best_match(spec)
        except Exception:
            paper = None

        if paper is None:
            summary.still_missing += 1
            continue

        dest = REPO_ROOT / row["pdf_path"]
        if not dry_run and not (dest.is_file() and dest.stat().st_size > 5000):
            try:
                download_pdf(paper, dest)
            except Exception:
                summary.still_missing += 1
                continue

        if row.get("paper_link", "").strip() != paper.abs_url:
            row["paper_link"] = paper.abs_url
            summary.paper_link_updated += 1
        row["state"] = "Downloaded"
        summary.repaired += 1

    if not dry_run:
        write_rows(path, rows)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Repair Tier 3 missing arXiv-like links and PDFs.")
    parser.add_argument("--targets", default="P13,P14", help="Comma-separated targets from P13,P14")
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
        summary = repair_log(path, tag, args.dry_run)
        summaries.append(summary)
        print(json.dumps(asdict(summary), ensure_ascii=False))
    print(json.dumps({"summary": [asdict(item) for item in summaries]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
