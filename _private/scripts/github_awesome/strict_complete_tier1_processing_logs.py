#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse

from strict_complete_tier1_logs import (
    REPO_ROOT,
    ROOT,
    MetadataResolver,
    RepoStats,
    TIER1_PRIORITIES,
    TIER1_REPOS,
    IssueRecord,
    candidate_from_arxiv_meta,
    candidate_from_crossref,
    candidate_from_openalex,
    candidate_from_page,
    build_pdf_path,
    choose_final_candidate,
    clean_url,
    dedupe_issues,
    display_path,
    extract_arxiv_id,
    first_year,
    iso_now,
    load_issue_history,
    load_queue,
    merge_issue_history,
    normalize_arxiv_url,
    normalize_paper_link,
    normalize_spaces,
    paper_link_looks_actionable,
    parse_current_venue,
    pick_best_crossref,
    pick_best_openalex,
    project_link_invalid,
    read_csv_rows,
    render_issues_md,
    render_run_summary,
    repo_slug,
    save_state,
    ts_now,
    venue_needs_review,
    write_csv_rows,
    write_issue_history,
)


PROCESSING_ROOT = REPO_ROOT / "paperAnalysis" / "processing" / "github_awesome"
REPORT_ROOT = ROOT / "strict_reports_processing"
TITLE_SEARCH_CUTOFF_YEAR = 2024
GITHUB_RESERVED_OWNERS = {
    "about",
    "account",
    "codespaces",
    "collections",
    "contact",
    "customer-stories",
    "enterprise",
    "events",
    "explore",
    "features",
    "git-guides",
    "issues",
    "login",
    "marketplace",
    "new",
    "notifications",
    "orgs",
    "organizations",
    "pricing",
    "pulls",
    "search",
    "security",
    "settings",
    "site",
    "sponsors",
    "team",
    "teams",
    "topics",
    "trending",
}
GITHUB_RESERVED_REPOS = {
    "actions",
    "blob",
    "branches",
    "commit",
    "commits",
    "compare",
    "discussions",
    "forks",
    "issues",
    "labels",
    "milestones",
    "network",
    "packages",
    "projects",
    "pull",
    "pulls",
    "releases",
    "search",
    "security",
    "settings",
    "stargazers",
    "tags",
    "tree",
    "watchers",
    "wiki",
}


def lower_repo_slug(repo: str) -> str:
    return repo.replace("/", "__").lower()


def processing_log_for_repo(repo: str) -> Path:
    return PROCESSING_ROOT / lower_repo_slug(repo) / "analysis_log.csv"


def select_tasks(queue_path: Path, requested_repos: list[str]) -> tuple[list[str], list]:
    queue_lines, tasks = load_queue(queue_path)
    tier1 = [task for task in tasks if task.priority in TIER1_PRIORITIES and task.repo in TIER1_REPOS]
    if requested_repos:
        requested = {repo.lower() for repo in requested_repos}
        tier1 = [task for task in tier1 if task.repo.lower() in requested]
    return queue_lines, tier1


def canonical_repo_url(url: str) -> str:
    url = clean_url(normalize_spaces(url))
    if not url.startswith("http"):
        return ""
    parsed = urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.")
    parts = [part for part in parsed.path.split("/") if part]

    if host == "github.com":
        if len(parts) < 2:
            return ""
        owner = parts[0]
        repo = parts[1].removesuffix(".git")
        if owner.lower() in GITHUB_RESERVED_OWNERS or repo.lower() in GITHUB_RESERVED_REPOS:
            return ""
        return f"https://github.com/{owner}/{repo}"

    if host == "gitlab.com":
        if len(parts) < 2:
            return ""
        return f"https://gitlab.com/{parts[0]}/{parts[1].removesuffix('.git')}"

    if host == "huggingface.co":
        if len(parts) >= 3 and parts[0] in {"datasets", "spaces"}:
            return f"https://huggingface.co/{parts[0]}/{parts[1]}/{parts[2]}"
        if len(parts) >= 2 and parts[0] not in {"blog", "collections", "docs", "learn", "papers"}:
            return f"https://huggingface.co/{parts[0]}/{parts[1]}"
    return ""


def project_candidates_from_page(page: dict) -> list[str]:
    urls: list[str] = []
    final_url = normalize_spaces(page.get("final_url", ""))
    if final_url:
        urls.append(final_url)
    for value in (page.get("meta") or {}).values():
        value = normalize_spaces(str(value))
        if value.startswith("http"):
            urls.append(value)
    urls.extend(page.get("urls") or [])

    out: list[str] = []
    seen: set[str] = set()
    for raw_url in urls:
        canonical = canonical_repo_url(raw_url)
        if not canonical or canonical in seen:
            continue
        seen.add(canonical)
        out.append(canonical)
    return out


def paper_page_scan_urls(row: dict[str, str]) -> list[str]:
    urls: list[str] = []
    paper_link = normalize_spaces(row.get("paper_link", ""))
    if paper_link and paper_link != "N/A":
        urls.append(paper_link)
        normalized_arxiv = normalize_arxiv_url(paper_link)
        if normalized_arxiv != paper_link:
            urls.append(normalized_arxiv)
        openreview_match = re.search(r"openreview\\.net/(?:pdf|forum)\\?id=([^&#]+)", paper_link, re.I)
        if openreview_match:
            urls.append(f"https://openreview.net/forum?id={openreview_match.group(1)}")
    return list(dict.fromkeys(urls))


def try_fill_project_link(row: dict[str, str], resolver: MetadataResolver) -> tuple[str, list[str]]:
    attempts: list[str] = []
    current = normalize_spaces(row.get("project_link_or_github_link", ""))
    if current and current != "N/A":
        return current, attempts
    for url in paper_page_scan_urls(row):
        attempts.append(f"page_scan:{url}")
        page = resolver.fetch_page_metadata(url)
        candidates = project_candidates_from_page(page)
        if candidates:
            return candidates[0], attempts
    return "N/A", attempts


def should_run_title_search(row: dict[str, str], arxiv_candidate_venue: str) -> bool:
    if not venue_needs_review(row.get("venue", "")):
        return False
    venue_year = first_year(row.get("venue", "")) or first_year(arxiv_candidate_venue) or first_year(row.get("paper_link", ""))
    if not venue_year:
        return True
    try:
        return int(venue_year) <= TITLE_SEARCH_CUTOFF_YEAR
    except ValueError:
        return True


def resolve_processing_row_fast(
    row: dict[str, str],
    resolver: MetadataResolver,
) -> tuple[dict[str, str], list[IssueRecord], dict[str, int]]:
    issues: list[IssueRecord] = []
    changes = {
        "venue_updated": 0,
        "venue_year_filled": 0,
        "paper_link_filled": 0,
        "importance_filled": 0,
        "pdf_path_filled": 0,
        "project_filled": 0,
        "state_changed": 0,
        "invalid_candidates": 0,
    }

    row = dict(row)
    row["state"] = normalize_spaces(row.get("state", "")) or "Wait"
    row["importance"] = normalize_spaces(row.get("importance", "")) or "Unrated"
    row["paper_title"] = normalize_spaces(row.get("paper_title", ""))
    row["venue"] = normalize_spaces(row.get("venue", ""))
    row["project_link_or_github_link"] = normalize_spaces(row.get("project_link_or_github_link", ""))
    row["paper_link"] = normalize_paper_link(normalize_spaces(row.get("paper_link", "")))
    row["sort"] = normalize_spaces(row.get("sort", ""))
    row["pdf_path"] = normalize_spaces(row.get("pdf_path", ""))

    if row["importance"] == "Unrated" and not normalize_spaces(row.get("importance", "")):
        changes["importance_filled"] += 1
    if not row["project_link_or_github_link"] or project_link_invalid(row["project_link_or_github_link"]):
        if row["project_link_or_github_link"] != "N/A":
            row["project_link_or_github_link"] = "N/A"
            changes["project_filled"] += 1

    if not row["pdf_path"]:
        row["pdf_path"] = build_pdf_path(row["sort"], row["venue"], row["paper_title"])
        changes["pdf_path_filled"] += 1

    arxiv_candidate = None
    oa_candidate = None
    cr_candidate = None
    page_candidate = None
    sources_used: list[str] = []

    if not row["paper_link"] and row["project_link_or_github_link"] not in {"", "N/A"}:
        project_page = resolver.fetch_page_metadata(row["project_link_or_github_link"])
        page_candidate = candidate_from_page(row, project_page, "project_link")
        if page_candidate and page_candidate.paper_link:
            row["paper_link"] = page_candidate.paper_link
            changes["paper_link_filled"] += 1

    if venue_needs_review(row["venue"]):
        arxiv_id = extract_arxiv_id(row["paper_link"])
        arxiv_meta = resolver.fetch_arxiv_metadata(arxiv_id) if arxiv_id else None
        if arxiv_meta:
            arxiv_candidate = candidate_from_arxiv_meta(arxiv_meta, row)
            if arxiv_candidate:
                sources_used.append(arxiv_candidate.source)
            doi = arxiv_meta.get("doi") or ""
            if doi:
                oa_item = resolver.fetch_openalex_by_doi(doi)
                if oa_item:
                    oa_candidate = candidate_from_openalex(oa_item, row["paper_title"])
                cr_item = resolver.fetch_crossref_by_doi(doi)
                if cr_item:
                    cr_candidate = candidate_from_crossref(cr_item, row["paper_title"])

        if not page_candidate and row["paper_link"] and row["paper_link"] != "N/A" and not paper_link_looks_actionable(row["paper_link"]):
            page_meta = resolver.fetch_page_metadata(row["paper_link"])
            page_candidate = candidate_from_page(row, page_meta, "paper_link")

        if should_run_title_search(row, arxiv_candidate.venue if arxiv_candidate else "") and not any(
            candidate and candidate.kind == "published" for candidate in (arxiv_candidate, oa_candidate, cr_candidate)
        ):
            best_oa = pick_best_openalex(row["paper_title"], resolver.search_openalex(row["paper_title"]))
            if best_oa:
                oa_candidate = candidate_from_openalex(best_oa, row["paper_title"])
            best_cr = pick_best_crossref(row["paper_title"], resolver.search_crossref(row["paper_title"]))
            if best_cr:
                cr_candidate = candidate_from_crossref(best_cr, row["paper_title"])

        resolved_venue, extra_sources, unresolved = choose_final_candidate(
            row,
            row["venue"],
            arxiv_candidate,
            oa_candidate,
            cr_candidate,
            page_candidate,
        )
        sources_used.extend(extra_sources)

        old_base, old_year = parse_current_venue(row["venue"])
        new_base, new_year = parse_current_venue(resolved_venue)
        if resolved_venue and resolved_venue != row["venue"]:
            if old_base and new_base and old_base.lower() == new_base.lower() and not old_year and new_year:
                changes["venue_year_filled"] += 1
            else:
                changes["venue_updated"] += 1
            row["venue"] = resolved_venue

        if (not first_year(row["venue"])) and row["state"] != "Skip":
            issues.append(
                IssueRecord(
                    timestamp=iso_now(),
                    issue_type="missing_venue_year",
                    title=row["paper_title"],
                    status="needs_review",
                    details=f"venue 仍缺少年份或未能确认最终 venue：{row['venue'] or 'Unknown'}",
                    attempted=list(dict.fromkeys(sources_used)) or ["arXiv API", "OpenAlex DOI/title search", "Crossref DOI/title search"],
                    resolved=False,
                )
            )

        if unresolved and row["state"] != "Skip":
            issues.append(
                IssueRecord(
                    timestamp=iso_now(),
                    issue_type="low_confidence_venue",
                    title=row["paper_title"],
                    status="needs_review",
                    details=f"venue 保守保留为 `{row['venue']}`，仍建议人工复核。",
                    attempted=list(dict.fromkeys(sources_used)) or ["arXiv API", "OpenAlex DOI/title search", "Crossref DOI/title search"],
                    resolved=False,
                )
            )

    return row, dedupe_issues(issues), changes


def recanonicalize_pdf_path(row: dict[str, str]) -> bool:
    old_rel = normalize_spaces(row.get("pdf_path", ""))
    new_rel = build_pdf_path(row.get("sort", ""), row.get("venue", ""), row.get("paper_title", ""))
    if old_rel == new_rel:
        return False

    old_abs = REPO_ROOT / old_rel if old_rel else None
    new_abs = REPO_ROOT / new_rel
    if old_abs and old_abs.exists() and not new_abs.exists():
        new_abs.parent.mkdir(parents=True, exist_ok=True)
        old_abs.replace(new_abs)
    row["pdf_path"] = new_rel
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="对 Tier 1 processing analysis_log.csv 做严格补全与 project 开源扫描。")
    ap.add_argument("--queue", default=str(ROOT / "collect_priority_queue.md"), help="优先级队列文件路径")
    ap.add_argument("--repo", action="append", default=[], help="只处理指定 repo，可重复传入")
    ap.add_argument("--limit", type=int, default=0, help="每个 repo 只处理前 N 条，用于小范围验证")
    ap.add_argument("--dry-run", action="store_true", help="只输出运行结果，不落盘")
    args = ap.parse_args()

    queue_path = Path(args.queue)
    _queue_lines, tasks = select_tasks(queue_path, args.repo)
    if not tasks:
        raise SystemExit("未找到可处理的 Tier 1 repo。")

    resolver = MetadataResolver()
    run_stamp = ts_now()
    report_dir = REPORT_ROOT / run_stamp
    if not args.dry_run:
        report_dir.mkdir(parents=True, exist_ok=True)

    repo_reports: list[tuple[str, RepoStats, int]] = []

    for task in tasks:
        slug = repo_slug(task.repo)
        processing_csv = processing_log_for_repo(task.repo)
        if not processing_csv.exists():
            raise SystemExit(f"processing analysis_log.csv 不存在: {display_path(processing_csv)}")

        rows = read_csv_rows(processing_csv)
        repo_dir = ROOT / slug
        run_dir = repo_dir / run_stamp
        if not args.dry_run:
            repo_dir.mkdir(parents=True, exist_ok=True)
            run_dir.mkdir(parents=True, exist_ok=True)

        updated_rows: list[dict[str, str]] = []
        current_issues: list[IssueRecord] = []
        stats = RepoStats(rows=len(rows))

        selected_rows = rows[: args.limit] if args.limit and args.limit > 0 else rows
        stats.rows = len(selected_rows)
        for index, row in enumerate(selected_rows, start=1):
            new_row, issues, changes = resolve_processing_row_fast(row, resolver)

            project_before = normalize_spaces(new_row.get("project_link_or_github_link", ""))
            project_after, project_attempts = try_fill_project_link(new_row, resolver)
            if project_before in {"", "N/A"} and project_after not in {"", "N/A"}:
                new_row["project_link_or_github_link"] = project_after
                changes["project_filled"] += 1

            if recanonicalize_pdf_path(new_row):
                changes["pdf_path_filled"] += 1

            updated_rows.append(new_row)
            current_issues.extend(issues)
            stats.venue_updated += changes["venue_updated"]
            stats.venue_year_filled += changes["venue_year_filled"]
            stats.paper_link_filled += changes["paper_link_filled"]
            stats.importance_filled += changes["importance_filled"]
            stats.pdf_path_filled += changes["pdf_path_filled"]
            stats.project_filled += changes["project_filled"]
            stats.state_changed += changes["state_changed"]
            stats.invalid_candidates += changes["invalid_candidates"]
            if any(changes.values()):
                stats.changed_rows += 1
            if index % 50 == 0 or index == len(selected_rows):
                print(f"[progress] {task.repo}: {index}/{len(selected_rows)}")

        deduped_current_issues = dedupe_issues(current_issues)
        issues_jsonl = repo_dir / "issues.jsonl"
        history = load_issue_history(issues_jsonl) if issues_jsonl.exists() else []
        merged_history = merge_issue_history(history, deduped_current_issues)
        unresolved_total = sum(1 for issue in merged_history if not issue.resolved)
        stats.unresolved = unresolved_total

        if not args.dry_run:
            final_rows = updated_rows + rows[len(selected_rows) :]
            write_csv_rows(run_dir / "processing_output.csv", final_rows)
            write_csv_rows(processing_csv, final_rows)
            write_issue_history(issues_jsonl, merged_history)
            render_issues_md(repo_dir / "issues.md", task, merged_history, str(run_dir.relative_to(ROOT)))
            render_run_summary(run_dir / "strict_completion_processing_summary.md", task.repo, stats, merged_history, processing_csv)
            save_state(
                repo_dir / "task_state.json",
                {
                    "repo": task.repo,
                    "priority": task.priority,
                    "direction": task.direction,
                    "selected_at": iso_now(),
                    "source_mode": "strict_completion_tier1_processing",
                    "latest_run": str(run_dir),
                    "row_count": len(updated_rows + rows[len(selected_rows) :]),
                    "issue_count_current_run": len(deduped_current_issues),
                    "issue_count_total": len(merged_history),
                    "canonical_csv": str(processing_csv),
                },
            )

        repo_reports.append((task.repo, stats, unresolved_total))
        print(
            f"[strict-processing] {task.repo}: rows={len(updated_rows + rows[len(selected_rows):])} "
            f"changed={stats.changed_rows} project_filled={stats.project_filled} unresolved={unresolved_total}"
        )

    if not args.dry_run:
        lines = [
            "---",
            'title: "Tier 1 Processing Strict Completion Report"',
            f"created: {iso_now()}",
            f"updated: {iso_now()}",
            "type: github_awesome_strict_completion_report",
            "tags:",
            "  - github-awesome",
            "  - strict-completion",
            "  - tier1",
            "  - processing-log",
            "---",
            "",
            "# Tier 1 Processing 严格补全报告",
            "",
            "| Repo | Rows | Changed | Venue Updated | Venue Year Filled | Paper Link Filled | Project Link Filled | Pdf Path Filled | Unresolved |",
            "|------|------|---------|---------------|-------------------|-------------------|---------------------|-----------------|------------|",
        ]
        for repo, stats, unresolved in repo_reports:
            lines.append(
                f"| `{repo}` | {stats.rows} | {stats.changed_rows} | {stats.venue_updated} | "
                f"{stats.venue_year_filled} | {stats.paper_link_filled} | {stats.project_filled} | "
                f"{stats.pdf_path_filled} | {unresolved} |"
            )
        lines.append("")
        (report_dir / "tier1_processing_strict_completion_report.md").write_text("\n".join(lines), encoding="utf-8")

    if args.dry_run:
        print("Dry-run mode enabled; processing logs, issues, and state were not modified.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
