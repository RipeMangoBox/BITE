#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import difflib
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import download_analysis_log_pdfs as base

ARXIV_ID_RE = re.compile(r"(\d{4}\.\d{4,5})")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Repair one 8-column analysis_log.csv by reusing existing PDFs, "
            "downloading missing ones, and updating corrected paper links."
        )
    )
    parser.add_argument("--log", required=True, help="Path to analysis_log.csv relative to repo root.")
    parser.add_argument("--repo", default="manual/single-log", help="Logical repo label used in reporting.")
    parser.add_argument("--workers", type=int, default=8, help="Concurrent download workers.")
    parser.add_argument(
        "--flush-every",
        type=int,
        default=24,
        help="Write the CSV after each completed chunk of this many unique paper tasks.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Resolve candidates without writing files.")
    return parser.parse_args()


def canonical_paper_link(url: str) -> str:
    normalized = base.normalize_paper_link(url)
    return normalized or base.normalize_spaces(url)


def looks_like_paper_link(url: str) -> bool:
    url = base.normalize_spaces(url).lower()
    if not url or url == "n/a":
        return False
    good_markers = (
        "arxiv.org",
        "openreview.net",
        "openaccess.thecvf.com",
        "aclanthology.org",
        "ieeexplore.ieee.org",
        "link.springer.com",
        "doi.org",
        ".pdf",
    )
    return any(marker in url for marker in good_markers)


def should_replace_paper_link(row: dict[str, str], candidate: str) -> bool:
    candidate = canonical_paper_link(candidate)
    current = base.normalize_spaces(row.get("paper_link", ""))
    project = base.normalize_spaces(row.get("project_link_or_github_link", ""))

    if not candidate or candidate.upper() == "N/A":
        return False
    if not looks_like_paper_link(candidate):
        return False
    if not current or current.upper() == "N/A":
        return True
    if base.normalize_paper_link(current) == base.normalize_paper_link(candidate):
        return False
    if current == project:
        return True
    if "github.com" in current.lower() and "github.com" not in candidate.lower():
        return True
    if not looks_like_paper_link(current) and looks_like_paper_link(candidate):
        return True
    return False


def update_link_from_existing_record(
    row: dict[str, str],
    existing: base.ExistingPdfRecord | None,
) -> bool:
    if existing is None:
        return False
    candidate = canonical_paper_link(existing.paper_link)
    if not should_replace_paper_link(row, candidate):
        return False
    row["paper_link"] = candidate
    return True


def chunks(items: list[base.DownloadTask], chunk_size: int) -> Iterable[list[base.DownloadTask]]:
    for start in range(0, len(items), chunk_size):
        yield items[start : start + chunk_size]


def fuzzy_normalize(text: str) -> str:
    text = (text or "").lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "", text)


def build_existing_pdf_id_index(pdf_files: list[Path]) -> dict[str, list[Path]]:
    mapping: dict[str, list[Path]] = defaultdict(list)
    for pdf in pdf_files:
        match = ARXIV_ID_RE.search(pdf.name)
        if match:
            mapping[match.group(1)].append(pdf)
    return mapping


def find_existing_pdf_match(
    row: dict[str, str],
    pdf_files: list[Path],
    pdf_id_index: dict[str, list[Path]],
    threshold: float = 0.72,
) -> tuple[Path | None, float, str]:
    title_key = fuzzy_normalize(row.get("paper_title", ""))
    if not title_key:
        return None, 0.0, ""

    best_path: Path | None = None
    best_score = 0.0
    reason = ""

    paper_link = row.get("paper_link", "")
    match = ARXIV_ID_RE.search(paper_link or "")
    if match:
        arxiv_id = match.group(1)
        candidates = pdf_id_index.get(arxiv_id, [])
        for candidate in candidates:
            score = difflib.SequenceMatcher(
                None, title_key, fuzzy_normalize(candidate.stem)
            ).ratio()
            if score > best_score:
                best_path = candidate
                best_score = score
                reason = "arxiv_id"

    if best_path is None:
        for candidate in pdf_files:
            score = difflib.SequenceMatcher(
                None, title_key, fuzzy_normalize(candidate.stem)
            ).ratio()
            if score > best_score:
                best_path = candidate
                best_score = score
                reason = "title"

    if best_path is None or best_score < threshold:
        return None, best_score, reason
    return best_path, best_score, reason


def resolve_missing_rows_from_local_pdfs(rows: list[dict[str, str]]) -> tuple[int, list[tuple[str, str, float, str]]]:
    pdf_root = base.REPO_ROOT / "paperPDFs"
    pdf_files = list(pdf_root.rglob("*.pdf"))
    pdf_id_index = build_existing_pdf_id_index(pdf_files)
    resolved = 0
    samples: list[tuple[str, str, float, str]] = []

    for row in rows:
        pdf_path = base.normalize_spaces(row.get("pdf_path", ""))
        if not pdf_path or base.pdf_file_looks_valid(base.REPO_ROOT / pdf_path):
            continue
        matched_path, score, reason = find_existing_pdf_match(row, pdf_files, pdf_id_index)
        if matched_path is None:
            continue
        row["pdf_path"] = matched_path.relative_to(base.REPO_ROOT).as_posix()
        base.advance_state_for_ready_pdf(row)
        resolved += 1
        if len(samples) < 5:
            samples.append((row.get("paper_title", ""), row["pdf_path"], score, reason))

    return resolved, samples


def main() -> None:
    args = parse_args()
    log_path = (base.REPO_ROOT / args.log).resolve()
    if not log_path.exists():
        raise SystemExit(f"log not found: {log_path}")

    rows = base.read_csv_rows(log_path)
    for row in rows:
        base.ensure_row_defaults(row)

    loaded = base.LoadedLog(
        spec=base.LogSpec(batch="MANUAL", repo=args.repo, target_log=log_path, collect_log=None),
        rows=rows,
    )
    loaded_logs = [loaded]
    stats: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    log_key = base.rel_path(log_path)

    path_rewrites = base.canonicalize_pdf_paths(loaded_logs, dry_run=args.dry_run)
    if path_rewrites.get(log_key):
        stats[log_key]["pdf_path_canonicalized"] += path_rewrites[log_key]
    base.write_loaded_logs(loaded_logs, dry_run=args.dry_run)

    pre_local_resolved = 0
    pre_local_samples: list[tuple[str, str, float, str]] = []
    if not args.dry_run:
        pre_local_resolved, pre_local_samples = resolve_missing_rows_from_local_pdfs(rows)
        if pre_local_resolved:
            stats[log_key]["resolved_from_local_fuzzy_match_pre"] += pre_local_resolved
            base.write_loaded_logs(loaded_logs, dry_run=False)

    link_index, title_index = base.scan_existing_pdf_index()

    # Pre-pass: if another log already has a valid PDF and better paper link, inherit it.
    inherited_links = 0
    for row in rows:
        existing = None
        for key in (base.row_link_key(row), base.row_title_key(row)):
            if key and key in link_index:
                existing = link_index[key]
                break
            if key and key in title_index:
                existing = title_index[key]
                break
        if existing and update_link_from_existing_record(row, existing):
            inherited_links += 1
    if inherited_links:
        stats[log_key]["paper_link_inherited"] += inherited_links

    tasks = base.build_download_tasks(loaded_logs, link_index, title_index, stats)
    total_tasks = len(tasks)
    chunk_size = max(args.workers, args.flush_every)

    print(f"[INFO] log: {base.rel_path(log_path)}")
    print(f"[INFO] rows: {len(rows)}")
    print(f"[INFO] unique missing-paper tasks after dedupe: {total_tasks}")

    for chunk_index, chunk in enumerate(chunks(tasks, chunk_size), start=1):
        print(f"[INFO] processing chunk {chunk_index} with {len(chunk)} tasks")
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_map = {
                executor.submit(base.execute_download_task, task, args.dry_run): task
                for task in chunk
            }
            for future in concurrent.futures.as_completed(future_map):
                task = future_map[future]
                outcome = future.result()
                row_indices = [
                    ref.row_index for ref in task.row_refs if ref.log_path == loaded.spec.target_log
                ]
                for row_index in row_indices:
                    row = rows[row_index]
                    row["pdf_path"] = outcome.pdf_path
                    if outcome.success:
                        base.advance_state_for_ready_pdf(row)
                        if outcome.reused_existing:
                            stats[log_key]["reused_from_task_dest"] += 1
                        elif outcome.downloaded:
                            stats[log_key]["downloaded_now"] += 1
                        elif outcome.dry_run:
                            stats[log_key]["dry_run_resolvable"] += 1

                        candidate = canonical_paper_link(outcome.source_url)
                        if should_replace_paper_link(row, candidate):
                            row["paper_link"] = candidate
                            stats[log_key]["paper_link_corrected"] += 1
                    else:
                        if row.get("state") not in {"checked", "Skip"}:
                            row["state"] = "Missing"
                        stats[log_key]["marked_missing"] += 1

                if outcome.success and not args.dry_run:
                    record = base.ExistingPdfRecord(
                        title=task.title,
                        paper_link=canonical_paper_link(outcome.source_url),
                        pdf_path=outcome.pdf_path,
                        source_log="runtime",
                        state="Downloaded",
                    )
                    for key in task.link_keys:
                        link_index[key] = record
                    for key in task.title_keys:
                        title_index[key] = record

        base.write_loaded_logs(loaded_logs, dry_run=args.dry_run)

    local_resolved = 0
    local_samples: list[tuple[str, str, float, str]] = []
    if not args.dry_run:
        local_resolved, local_samples = resolve_missing_rows_from_local_pdfs(rows)
        if local_resolved:
            stats[log_key]["resolved_from_local_fuzzy_match"] += local_resolved
            base.write_loaded_logs(loaded_logs, dry_run=False)

    print(f"[INFO] stats for {log_key}: {dict(stats[log_key])}")
    for title, pdf_path, score, reason in pre_local_samples:
        print(f"[INFO] local fuzzy pre-match ({reason}, {score:.3f}): {title} -> {pdf_path}")
    for title, pdf_path, score, reason in local_samples:
        print(f"[INFO] local fuzzy match ({reason}, {score:.3f}): {title} -> {pdf_path}")


if __name__ == "__main__":
    main()
