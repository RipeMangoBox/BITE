#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html
import re
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_ROOT = REPO_ROOT / "_private" / "PaperBite" / "github_awesome" / "readme_snapshots"
PROCESSING_ROOT = REPO_ROOT / "paperAnalysis" / "processing" / "github_awesome"
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

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
TITLE_CELL_RE = re.compile(r"\[\*\*(.*?)\*\*\]\(([^)]+)\)")
DOUBLE_BRACKET_LINK_RE = re.compile(r"\[\[([^\]]+)\]\(([^)]+)\)\]")
ARXIV_YEAR_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/([0-9]{2})([0-9]{2})\.[0-9]{4,5}", re.I)


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def clean_markdown_text(text: str) -> str:
    value = html.unescape(text or "")
    value = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", value)
    value = re.sub(r"<br\s*/?>", " ", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    value = value.replace("\\|", "|")
    return normalize_spaces(value)


def normalize_title_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", clean_markdown_text(title).lower())


def sanitize_sort(text: str) -> str:
    value = clean_markdown_text(text)
    value = value.replace("&", " and ")
    value = re.sub(r"[^A-Za-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "Uncategorized"


def infer_year_from_link(url: str) -> str:
    match = ARXIV_YEAR_RE.search(url or "")
    if not match:
        return ""
    return f"20{match.group(1)}"


def pick_preferred_link(raw_text: str, preferred_tokens: Iterable[str]) -> str:
    links = [(clean_markdown_text(label), url.strip()) for label, url in LINK_RE.findall(raw_text)]
    for token in preferred_tokens:
        token_lower = token.lower()
        for label, url in links:
            if token_lower in label.lower():
                return url
    return ""


def parse_markdown_table_line(line: str) -> list[str] | None:
    if not line.lstrip().startswith("|"):
        return None
    parts = [part.strip() for part in line.strip().strip("|").split("|")]
    if len(parts) < 5:
        return None
    return parts


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    ensure_parent(path)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def build_row(
    *,
    title: str,
    venue: str,
    project_url: str,
    paper_url: str,
    sort_value: str,
) -> dict[str, str]:
    return {
        "state": "Wait",
        "importance": "",
        "paper_title": clean_markdown_text(title),
        "venue": normalize_spaces(venue),
        "project_link_or_github_link": project_url or "N/A",
        "paper_link": paper_url.strip(),
        "sort": sanitize_sort(sort_value),
        "pdf_path": "",
    }


def parse_soraproducer() -> tuple[list[dict[str, str]], dict[str, int]]:
    source = (
        SNAPSHOT_ROOT
        / "soraproducer__Awesome-Human-Interaction-Motion-Generation"
        / "README.snapshot.md"
    )
    lines = source.read_text(encoding="utf-8").splitlines()

    in_motion_block = False
    current_section = ""
    rows: list[dict[str, str]] = []
    seen_titles: set[str] = set()
    section_counts: dict[str, int] = {}

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## Human Interaction Motion Generation"):
            in_motion_block = True
            current_section = ""
            continue
        if in_motion_block and stripped.startswith("## Human Interaction Datasets"):
            break
        if not in_motion_block:
            continue
        if stripped.startswith("### "):
            current_section = clean_markdown_text(stripped[4:])
            continue
        if not current_section:
            continue
        if stripped.startswith("|:") or stripped.startswith("| Title"):
            continue

        cells = parse_markdown_table_line(line)
        if cells is None:
            continue

        title_cell, venue_cell, year_cell, code_cell, project_cell = cells[:5]
        title_match = TITLE_CELL_RE.search(title_cell)
        if not title_match:
            continue

        title = clean_markdown_text(title_match.group(1))
        paper_url = title_match.group(2).strip()
        title_key = normalize_title_key(title)
        if not title_key or title_key in seen_titles:
            continue

        venue_name = clean_markdown_text(venue_cell)
        year = clean_markdown_text(year_cell)
        if venue_name in {"-", ""}:
            venue = f"arXiv {year}" if year else "arXiv"
        else:
            venue = f"{venue_name} {year}".strip()

        project_url = pick_preferred_link(project_cell, ("project",)) or pick_preferred_link(
            code_cell, ("github", "code")
        )
        rows.append(
            build_row(
                title=title,
                venue=venue,
                project_url=project_url,
                paper_url=paper_url,
                sort_value=current_section.replace(" Motion Generation", ""),
            )
        )
        seen_titles.add(title_key)
        section_key = sanitize_sort(current_section.replace(" Motion Generation", ""))
        section_counts[section_key] = section_counts.get(section_key, 0) + 1

    return rows, section_counts


def parse_sun_haoyuan() -> tuple[list[dict[str, str]], dict[str, int]]:
    source = (
        SNAPSHOT_ROOT
        / "Sun-Haoyuan23__Awesome-RL-based-Reasoning-MLLMs"
        / "README.snapshot.md"
    )
    lines = source.read_text(encoding="utf-8").splitlines()

    in_papers_block = False
    current_section = ""
    rows: list[dict[str, str]] = []
    seen_titles: set[str] = set()
    section_counts: dict[str, int] = {}

    bullet_re = re.compile(r"^\*\s+\[(\d{4})\]\s+\[[^\]]+\]\s+\[(.+?)\]\(([^)]+)\)(.*)$")

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## Papers (Sort by Time of Release)"):
            in_papers_block = True
            current_section = ""
            continue
        if in_papers_block and stripped.startswith("## Benchmarks and Datasets"):
            break
        if not in_papers_block:
            continue
        if stripped.startswith("### "):
            current_section = clean_markdown_text(stripped[4:])
            continue
        if not current_section or not stripped.startswith("* "):
            continue

        match = bullet_re.match(stripped)
        if not match:
            continue

        date_token, title_raw, paper_url, tail = match.groups()
        title = clean_markdown_text(title_raw)
        title_key = normalize_title_key(title)
        if not title_key or title_key in seen_titles:
            continue

        year = f"20{date_token[:2]}"
        inferred_year = infer_year_from_link(paper_url)
        if inferred_year:
            year = inferred_year
        venue = f"arXiv {year}"

        project_url = pick_preferred_link(tail, ("project",)) or pick_preferred_link(
            tail, ("code", "github")
        )
        rows.append(
            build_row(
                title=title,
                venue=venue,
                project_url=project_url,
                paper_url=paper_url,
                sort_value=f"RL_MLLM_{current_section}",
            )
        )
        seen_titles.add(title_key)
        section_key = sanitize_sort(f"RL_MLLM_{current_section}")
        section_counts[section_key] = section_counts.get(section_key, 0) + 1

    return rows, section_counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate repo-local analysis logs for Tier 3 GitHub awesome repos.")
    parser.add_argument(
        "--targets",
        default="soraproducer,sun",
        help="Comma-separated targets: soraproducer,sun",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requested = {part.strip().lower() for part in args.targets.split(",") if part.strip()}
    summaries: list[str] = []

    if "soraproducer" in requested:
        rows, section_counts = parse_soraproducer()
        out = (
            PROCESSING_ROOT
            / "soraproducer__awesome-human-interaction-motion-generation"
            / "analysis_log.csv"
        )
        write_rows(out, rows)
        summaries.append(
            f"soraproducer rows={len(rows)} sections={dict(sorted(section_counts.items()))} out={out.relative_to(REPO_ROOT)}"
        )

    if "sun" in requested or "sun-haoyuan23" in requested:
        rows, section_counts = parse_sun_haoyuan()
        out = (
            PROCESSING_ROOT
            / "sun-haoyuan23__awesome-rl-based-reasoning-mllms"
            / "analysis_log.csv"
        )
        write_rows(out, rows)
        summaries.append(
            f"sun-haoyuan23 rows={len(rows)} sections={dict(sorted(section_counts.items()))} out={out.relative_to(REPO_ROOT)}"
        )

    if not summaries:
        raise SystemExit("No valid targets requested.")

    for summary in summaries:
        print(summary)


if __name__ == "__main__":
    main()
