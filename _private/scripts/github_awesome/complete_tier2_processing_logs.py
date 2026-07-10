#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import quote_plus

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
PRIVATE_GITHUB_AWESOME_ROOT = REPO_ROOT / "_private" / "PaperBite" / "github_awesome"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(PRIVATE_GITHUB_AWESOME_ROOT) not in sys.path:
    sys.path.insert(0, str(PRIVATE_GITHUB_AWESOME_ROOT))

from strict_complete_tier1_logs import (
    MetadataResolver,
    build_pdf_path,
    first_year,
    normalize_paper_link,
    normalize_spaces,
    normalize_title_key,
    parse_current_venue,
    project_link_invalid,
    read_csv_rows,
    repo_slug,
    resolve_row,
    similarity,
    venue_needs_review,
)


PROCESSING_ROOT = REPO_ROOT / "paperAnalysis" / "processing" / "github_awesome"
COLLECT_ROOT = REPO_ROOT / "_private" / "PaperBite" / "github_awesome" / "collect_logs"
REPORT_ROOT = REPO_ROOT / "_private" / "PaperBite" / "github_awesome" / "tier2_completion"
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
PREPRINT_BASES = {
    "arxiv",
    "openreview",
    "unknown",
    "doi",
    "ieee",
    "springer",
    "technical report",
    "techrxiv",
}
GITHUB_REPO_RE = re.compile(r"https?://github\.com/([^/\s]+)/([^/\s#?]+)", re.I)
GITHUB_SEARCH_URL = "https://github.com/search?q={query}&type=repositories"
RESERVED_GITHUB_OWNERS = {
    "search",
    "orgs",
    "topics",
    "collections",
    "features",
    "marketplace",
    "login",
    "signup",
    "settings",
    "notifications",
    "apps",
    "pulls",
    "issues",
    "codespaces",
}
TIER2_REPOS = [
    "ChenHsing/Awesome-Video-Diffusion-Models",
    "weitianxin/Awesome-Agentic-Reasoning",
    "jxzhangjhu/Awesome-LLM-RAG",
    "cwchenwang/awesome-3d-diffusion",
    "ga642381/speech-trident",
    "weihaox/awesome-digital-human",
]


@dataclass
class RepoSummary:
    repo: str
    rows: int = 0
    collect_venue_synced: int = 0
    collect_project_synced: int = 0
    venue_updated_via_search: int = 0
    venue_year_filled_via_search: int = 0
    project_found_via_search: int = 0
    project_still_na: int = 0
    pdf_path_rewritten: int = 0


def write_csv_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: normalize_spaces(row.get(field, "")) for field in CSV_FIELDS})


def read_collect_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def canonical_repo_url(url: str) -> str:
    match = GITHUB_REPO_RE.match((url or "").strip())
    if not match:
        return ""
    owner, repo = match.groups()
    repo = repo.removesuffix(".git")
    if owner.lower() in RESERVED_GITHUB_OWNERS:
        return ""
    return f"https://github.com/{owner}/{repo}"


def has_valid_project(url: str) -> bool:
    cleaned = normalize_spaces(url)
    return bool(cleaned and cleaned != "N/A" and not project_link_invalid(cleaned))


def venue_is_better(current: str, candidate: str) -> bool:
    current = normalize_spaces(current)
    candidate = normalize_spaces(candidate)
    if not candidate or current == candidate:
        return False
    cur_base, cur_year = parse_current_venue(current)
    cand_base, cand_year = parse_current_venue(candidate)
    cur_preprint = cur_base.lower() in PREPRINT_BASES
    cand_preprint = cand_base.lower() in PREPRINT_BASES
    if cur_preprint and not cand_preprint:
        return True
    if not cur_year and cand_year:
        return True
    if cur_base and cand_base and normalize_title_key(cur_base) == normalize_title_key(cand_base) and not cur_year and cand_year:
        return True
    return False


def build_collect_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    lookup: dict[str, dict[str, str]] = {}
    for row in rows:
        keys = {
            normalize_paper_link(row.get("paper_link", "")),
            normalize_title_key(row.get("paper_title", "")),
        }
        for key in keys:
            if key:
                lookup[key] = row
    return lookup


def sync_from_collect(proc_rows: list[dict[str, str]], collect_rows: list[dict[str, str]], summary: RepoSummary) -> None:
    lookup = build_collect_lookup(collect_rows)
    for row in proc_rows:
        candidate = None
        for key in (
            normalize_paper_link(row.get("paper_link", "")),
            normalize_title_key(row.get("paper_title", "")),
        ):
            if key and key in lookup:
                candidate = lookup[key]
                break
        if candidate is None:
            continue
        candidate_venue = normalize_spaces(candidate.get("venue", ""))
        if venue_is_better(row.get("venue", ""), candidate_venue):
            row["venue"] = candidate_venue
            summary.collect_venue_synced += 1
        candidate_project = normalize_spaces(candidate.get("project_link_or_github_link", ""))
        if not has_valid_project(row.get("project_link_or_github_link", "")) and has_valid_project(candidate_project):
            row["project_link_or_github_link"] = candidate_project
            summary.collect_project_synced += 1
        candidate_paper = normalize_spaces(candidate.get("paper_link", ""))
        if candidate_paper and candidate_paper != "N/A" and row.get("paper_link", "") in {"", "N/A"}:
            row["paper_link"] = candidate_paper


def extract_project_queries(title: str) -> list[str]:
    cleaned = normalize_spaces(title)
    if not cleaned:
        return []
    prefix = cleaned.split(":", 1)[0].strip()
    queries: list[str] = []
    if prefix and prefix != cleaned and 2 <= len(prefix) <= 48:
        queries.append(prefix)
        if "-" in prefix:
            queries.append(prefix.replace("-", " "))
    else:
        first_token = cleaned.split()[0].strip(",:;()[]{}")
        # Only search GitHub for distinctive method tags; skip generic prose titles.
        if 2 <= len(first_token) <= 30 and re.search(r"[A-Z].*[A-Z]|[\d_-]", first_token):
            queries.append(first_token)
            if "-" in first_token or "_" in first_token:
                queries.append(first_token.replace("-", " ").replace("_", " "))
    seen: set[str] = set()
    deduped: list[str] = []
    for query in queries:
        key = normalize_title_key(query)
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(query)
    return deduped


def candidate_repo_score(title: str, repo_url: str) -> float:
    repo_path = repo_url.split("github.com/", 1)[-1]
    owner, repo = repo_path.split("/", 1)
    repo_name = repo.replace("-", " ").replace("_", " ")
    prefix = normalize_spaces(title.split(":", 1)[0])
    score = max(similarity(title, repo_name), similarity(prefix, repo_name), similarity(title, owner))
    repo_key = normalize_title_key(repo_name)
    prefix_key = normalize_title_key(prefix)
    title_key = normalize_title_key(title)
    if prefix_key and prefix_key in repo_key:
        score = max(score, 0.97)
    if repo_key and repo_key in title_key and len(repo_key) >= 5:
        score = max(score, 0.95)
    return score


def github_repo_urls_from_text(text: str) -> list[str]:
    seen: set[str] = set()
    urls: list[str] = []
    for owner, repo in GITHUB_REPO_RE.findall(text or ""):
        url = canonical_repo_url(f"https://github.com/{owner}/{repo}")
        if not url or url in seen:
            continue
        seen.add(url)
        urls.append(url)
    return urls


def search_github_repos(resolver: MetadataResolver, query: str, cache: dict[str, list[str]]) -> list[str]:
    key = normalize_title_key(query)
    if key in cache:
        return cache[key]
    try:
        text, _ = resolver.fetch_text(GITHUB_SEARCH_URL.format(query=quote_plus(query)))
    except Exception:
        cache[key] = []
        return []
    repo_urls = []
    seen: set[str] = set()
    for match in re.findall(r'href="(/[^"/]+/[^"/]+)"', text):
        repo_url = canonical_repo_url(f"https://github.com{match}")
        if not repo_url or repo_url in seen:
            continue
        seen.add(repo_url)
        repo_urls.append(repo_url)
        if len(repo_urls) >= 5:
            break
    cache[key] = repo_urls
    time.sleep(0.2)
    return repo_urls


def search_project_link(
    row: dict[str, str],
    resolver: MetadataResolver,
    github_cache: dict[str, list[str]],
) -> str:
    if has_valid_project(row.get("project_link_or_github_link", "")):
        return normalize_spaces(row["project_link_or_github_link"])

    candidate_urls: list[str] = []
    for url in (row.get("paper_link", ""), row.get("project_link_or_github_link", "")):
        cleaned = normalize_spaces(url)
        if not cleaned or cleaned == "N/A" or not cleaned.startswith("http"):
            continue
        page = resolver.fetch_page_metadata(cleaned)
        candidate_urls.extend(github_repo_urls_from_text(page.get("final_url", "")))
        candidate_urls.extend(github_repo_urls_from_text(" ".join(page.get("urls", []))))

    best_direct = ""
    best_direct_score = 0.0
    for candidate in candidate_urls:
        score = candidate_repo_score(row["paper_title"], candidate)
        if score > best_direct_score:
            best_direct = candidate
            best_direct_score = score
    if best_direct and best_direct_score >= 0.95:
        return best_direct

    queries = extract_project_queries(row["paper_title"])
    for idx, query in enumerate(queries):
        results = search_github_repos(resolver, query, github_cache)
        if not results:
            continue
        scored = sorted(
            ((candidate_repo_score(row["paper_title"], url), url) for url in results),
            reverse=True,
        )
        best_score, best_url = scored[0]
        threshold = 0.97 if idx == 0 else 0.985
        if best_score >= threshold:
            return best_url

    return "N/A"


def update_pdf_path(row: dict[str, str], summary: RepoSummary) -> None:
    canonical = build_pdf_path(row.get("sort", ""), row.get("venue", ""), row.get("paper_title", ""))
    if row.get("pdf_path", "") != canonical:
        row["pdf_path"] = canonical
        summary.pdf_path_rewritten += 1


def should_search_venue(row: dict[str, str]) -> bool:
    current_venue = normalize_spaces(row.get("venue", ""))
    if not venue_needs_review(current_venue):
        return False
    base, year = parse_current_venue(current_venue)
    year = year or first_year(row.get("paper_link", ""))
    if base.lower() in {"doi", "openreview", "technical report", "unknown"}:
        return True
    if year and year.isdigit() and int(year) <= 2024:
        return True
    return False


def process_repo(
    repo: str,
    resolver: MetadataResolver,
    github_cache: dict[str, list[str]],
    dry_run: bool,
    limit: int,
) -> RepoSummary:
    slug = repo_slug(repo)
    slug_lower = slug.lower()
    processing_csv = PROCESSING_ROOT / slug_lower / "analysis_log.csv"
    collect_csv = None
    for candidate in sorted(COLLECT_ROOT.glob("*.auto.csv")):
        if candidate.name[: -len(".auto.csv")].lower() == slug_lower:
            collect_csv = candidate
            break
    if collect_csv is None:
        raise SystemExit(f"collect log not found for {repo}")

    rows = read_csv_rows(processing_csv)
    collect_rows = read_collect_rows(collect_csv)
    if limit > 0:
        selected = rows[:limit]
        remaining = rows[limit:]
    else:
        selected = rows
        remaining = []

    summary = RepoSummary(repo=repo, rows=len(selected))
    sync_from_collect(selected, collect_rows, summary)

    for index, row in enumerate(selected, start=1):
        original_venue = normalize_spaces(row.get("venue", ""))
        if should_search_venue(row):
            updated_row, _issues, _changes = resolve_row(row, resolver)
            new_base, new_year = parse_current_venue(updated_row.get("venue", ""))
            old_base, old_year = parse_current_venue(original_venue)
            if normalize_spaces(updated_row.get("venue", "")) != original_venue:
                if old_base and new_base and normalize_title_key(old_base) == normalize_title_key(new_base) and not old_year and new_year:
                    summary.venue_year_filled_via_search += 1
                else:
                    summary.venue_updated_via_search += 1
            row.update(updated_row)

        if not has_valid_project(row.get("project_link_or_github_link", "")):
            found = search_project_link(row, resolver, github_cache)
            if has_valid_project(found):
                row["project_link_or_github_link"] = found
                summary.project_found_via_search += 1
            else:
                summary.project_still_na += 1

        update_pdf_path(row, summary)
        if index % 50 == 0 or index == len(selected):
            print(f"[progress] {repo}: {index}/{len(selected)}")

    final_rows = selected + remaining
    if not dry_run:
        write_csv_rows(processing_csv, final_rows)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Complete Tier 2 processing analysis logs with venue/project metadata.")
    parser.add_argument("--repo", action="append", default=[], help="Only process the specified repo; repeatable.")
    parser.add_argument("--limit", type=int, default=0, help="Only process the first N rows per repo.")
    parser.add_argument("--dry-run", action="store_true", help="Do not write CSV files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    requested = {repo.lower() for repo in args.repo}
    repos = [repo for repo in TIER2_REPOS if not requested or repo.lower() in requested]
    if not repos:
        raise SystemExit("No Tier 2 repos matched the request.")

    resolver = MetadataResolver()
    github_cache: dict[str, list[str]] = {}
    run_stamp = time.strftime("%Y%m%d_%H%M%S")
    report_dir = REPORT_ROOT / run_stamp
    summaries: list[RepoSummary] = []

    for repo in repos:
        summary = process_repo(repo, resolver, github_cache, args.dry_run, args.limit)
        summaries.append(summary)
        print(
            f"[done] {repo}: rows={summary.rows} collect_venue={summary.collect_venue_synced} "
            f"collect_project={summary.collect_project_synced} venue_search={summary.venue_updated_via_search} "
            f"venue_year={summary.venue_year_filled_via_search} project_search={summary.project_found_via_search} "
            f"project_still_na={summary.project_still_na}"
        )

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "summary.json").write_text(
        json.dumps([asdict(item) for item in summaries], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[summary] {report_dir / 'summary.json'}")
    if args.dry_run:
        print("[summary] dry-run mode; CSV files were not modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
