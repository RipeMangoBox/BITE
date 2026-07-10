#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import os
import re
import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import recover_overcompressed_pdfs as rec


DOWNLOAD_DIR = Path.home() / "Downloads" / "acm_sig_auto"


def rel(path: Path) -> str:
    return str(path.relative_to(rec.ROOT))


def logs() -> list[Path]:
    return [
        rec.REPORT_DIR / "pdf_compression_parallel16_20260702T010918.tsv",
        *sorted(rec.REPORT_DIR.glob("pdf_compression_retry_*.tsv")),
    ]


def filter_candidates(args: argparse.Namespace) -> list[rec.Candidate]:
    candidates = rec.load_severe(logs())
    if args.url_contains:
        candidates = [c for c in candidates if args.url_contains in c.source_url]
    if args.url_not_contains:
        candidates = [c for c in candidates if args.url_not_contains not in c.source_url]
    if args.start_after:
        paths = [rel(c.path) for c in candidates]
        if args.start_after in paths:
            candidates = candidates[paths.index(args.start_after) + 1 :]
    if args.limit:
        candidates = candidates[: args.limit]
    return candidates


def browser_urls(c: rec.Candidate, max_urls: int) -> list[str]:
    urls = rec.candidate_urls(c.source_url)
    scored: list[tuple[int, str]] = []
    for url in urls:
        score = 0
        lower = url.lower()
        if "dl.acm.org/doi/pdf/" in lower:
            score += 100
        if "openreview.net/pdf" in lower:
            score += 90
        if lower.split("?", 1)[0].endswith(".pdf"):
            score += 80
        if url == c.source_url:
            score += 10
        scored.append((score, url))
    scored.sort(reverse=True)
    out: list[str] = []
    seen: set[str] = set()
    for _score, url in scored:
        if url not in seen:
            seen.add(url)
            out.append(url)
    return out[:max_urls]


def snapshot(download_dir: Path) -> dict[Path, tuple[int, int]]:
    out: dict[Path, tuple[int, int]] = {}
    for path in download_dir.glob("*.pdf"):
        if path.is_file():
            st = path.stat()
            out[path.resolve()] = (st.st_size, st.st_mtime_ns)
    return out


def stable_changed_pdf(download_dir: Path, before: dict[Path, tuple[int, int]], opened_at: float) -> Path | None:
    candidates: list[Path] = []
    for path in download_dir.glob("*.pdf"):
        if not path.is_file():
            continue
        resolved = path.resolve()
        st = path.stat()
        old = before.get(resolved)
        if old is None or old != (st.st_size, st.st_mtime_ns) or st.st_mtime >= opened_at:
            candidates.append(path)
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    for path in candidates:
        try:
            size1 = path.stat().st_size
            time.sleep(0.4)
            size2 = path.stat().st_size
        except FileNotFoundError:
            continue
        if size1 == size2 and size2 > 1024:
            return path
    return None


def wait_for_download(download_dir: Path, before: dict[Path, tuple[int, int]], opened_at: float, wait: int) -> Path | None:
    deadline = time.time() + wait
    while time.time() < deadline:
        pdf = stable_changed_pdf(download_dir, before, opened_at)
        if pdf is not None:
            return pdf
        time.sleep(1.0)
    return None


def acm_doi_suffix(c: rec.Candidate) -> str:
    match = re.search(r"/doi/pdf/10\.1145/([^?#]+)", c.source_url)
    if match:
        return match.group(1)
    match = re.search(r"doi\.org/10\.1145/([^?#]+)", c.source_url)
    return match.group(1) if match else ""


def changed_since(path: Path, before: dict[Path, tuple[int, int]]) -> bool:
    resolved = path.resolve()
    st = path.stat()
    old = before.get(resolved)
    return old is None or old != (st.st_size, st.st_mtime_ns)


def find_acm_download(c: rec.Candidate, download_dir: Path, before: dict[Path, tuple[int, int]]) -> Path | None:
    suffix = acm_doi_suffix(c)
    if not suffix:
        return None
    escaped = re.escape(suffix)
    partial_pattern = re.compile(rf"^{escaped}(?: \(\d+\))?\.pdf\.(?:crdownload|part)$")
    if any(partial_pattern.match(p.name) for p in download_dir.iterdir() if p.is_file()):
        return None
    pattern = re.compile(rf"^{escaped}(?: \(\d+\))?\.pdf$")
    matches = [
        p
        for p in download_dir.glob("*.pdf")
        if p.is_file() and pattern.match(p.name) and changed_since(p, before)
    ]
    if not matches:
        return None
    matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    for path in matches:
        try:
            size1 = path.stat().st_size
            time.sleep(8.0)
            size2 = path.stat().st_size
        except FileNotFoundError:
            continue
        if size1 == size2 and size2 > 1024:
            return path
    return None


def replace_from_download(c: rec.Candidate, downloaded: Path, dry_run: bool) -> dict[str, str]:
    path_rel = rel(c.path)
    row = {
        "status": "",
        "path": path_rel,
        "source_url": c.source_url,
        "original_logged_bytes": str(c.original_bytes),
        "overcompressed_bytes": str(c.compressed_bytes),
        "downloaded_bytes": str(downloaded.stat().st_size) if downloaded.exists() else "",
        "final_bytes": "",
        "method": "",
        "reason": "",
    }
    current_ok, current_pages, current_reason = rec.valid_pdf(c.path)
    if not current_ok or current_pages is None:
        row.update(status="skipped", reason=f"current pdf invalid: {current_reason}")
        return row

    ok_pdf, downloaded_pages, reason = rec.valid_pdf(downloaded)
    if not ok_pdf or downloaded_pages is None:
        row.update(status="download_invalid", reason=reason)
        return row
    if downloaded_pages != current_pages:
        row.update(status="page_mismatch", reason=f"current_pages={current_pages}; downloaded_pages={downloaded_pages}")
        return row

    work_dir = rec.WORK_ROOT / re.sub(r"[^A-Za-z0-9_.-]+", "_", path_rel)
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    best, method = rec.best_under_limit(downloaded, downloaded_pages, work_dir)
    if best is None:
        row.update(status="no_safe_under_20MiB", reason=method)
        return row

    final_size = best.stat().st_size
    row.update(final_bytes=str(final_size), method=method)
    if final_size > rec.LIMIT_BYTES:
        row.update(status="internal_error", reason="selected file exceeds limit")
        return row
    if dry_run:
        row.update(status="dry_run_ok", reason="not replaced")
        return row

    backup_path = rec.BACKUP_ROOT / path_rel
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    if not backup_path.exists():
        shutil.copy2(c.path, backup_path)

    tmp_replace = c.path.with_name(c.path.name + ".browser-recover-tmp")
    shutil.copy2(best, tmp_replace)
    ok_final, final_pages, final_reason = rec.valid_pdf(tmp_replace)
    if not ok_final or final_pages != current_pages:
        tmp_replace.unlink(missing_ok=True)
        row.update(status="final_invalid", reason=f"{final_reason}; pages={final_pages}")
        return row
    os.replace(tmp_replace, c.path)
    row.update(status="replaced", reason="ok")
    return row


def empty_row(c: rec.Candidate, status: str, reason: str) -> dict[str, str]:
    return {
        "status": status,
        "path": rel(c.path),
        "source_url": c.source_url,
        "original_logged_bytes": str(c.original_bytes),
        "overcompressed_bytes": str(c.compressed_bytes),
        "downloaded_bytes": "",
        "final_bytes": "",
        "method": "",
        "reason": reason,
    }


def process_acm_batch(
    batch: list[rec.Candidate],
    args: argparse.Namespace,
    browser: str,
    download_dir: Path,
) -> list[tuple[rec.Candidate, dict[str, str]]]:
    before = snapshot(download_dir)
    opened: list[rec.Candidate] = []
    for c in batch:
        urls = browser_urls(c, 1)
        if not urls:
            continue
        subprocess.Popen(
            [browser, f"--profile-directory={args.profile_directory}", "--new-tab", urls[0]],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        opened.append(c)
        time.sleep(args.delay_after_open)

    found: dict[str, Path] = {}
    deadline = time.time() + args.wait
    while time.time() < deadline and len(found) < len(opened):
        for c in opened:
            key = rel(c.path)
            if key in found:
                continue
            path = find_acm_download(c, download_dir, before)
            if path is not None:
                found[key] = path
        time.sleep(1.0)

    rows_by_key: dict[str, tuple[rec.Candidate, dict[str, str]]] = {}
    future_map = {}
    with ThreadPoolExecutor(max_workers=max(1, args.compress_workers)) as executor:
        for c in batch:
            key = rel(c.path)
            downloaded = found.get(key)
            if downloaded is None:
                rows_by_key[key] = (c, empty_row(c, "download_timeout", "timeout in ACM batch"))
                continue
            future_map[executor.submit(replace_from_download, c, downloaded, args.dry_run)] = (c, downloaded)
        for future in as_completed(future_map):
            c, downloaded = future_map[future]
            key = rel(c.path)
            try:
                row = future.result()
            except Exception as exc:
                row = empty_row(c, "exception", f"{type(exc).__name__}: {exc}")
            if not args.keep_downloads:
                downloaded.unlink(missing_ok=True)
            rows_by_key[key] = (c, row)

    rows: list[tuple[rec.Candidate, dict[str, str]]] = []
    for c in batch:
        key = rel(c.path)
        rows.append(rows_by_key[key])
    return rows


def run(args: argparse.Namespace) -> int:
    download_dir = Path(args.download_dir).expanduser()
    download_dir.mkdir(parents=True, exist_ok=True)
    rec.WORK_ROOT.mkdir(parents=True, exist_ok=True)
    browser = args.browser or shutil.which("microsoft-edge") or shutil.which("microsoft-edge-stable")
    if not browser:
        raise SystemExit("microsoft-edge not found")

    candidates = filter_candidates(args)
    timestamp = time.strftime("%Y%m%dT%H%M%S")
    log_path = rec.REPORT_DIR / f"pdf_recovery_browser_{timestamp}.tsv"
    fields = [
        "status",
        "path",
        "source_url",
        "original_logged_bytes",
        "overcompressed_bytes",
        "downloaded_bytes",
        "final_bytes",
        "method",
        "reason",
    ]
    counts: dict[str, int] = {}
    with log_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        print(f"[BROWSER-RECOVERY] candidates={len(candidates)} log={rel(log_path)}")
        index = 0
        while index < len(candidates):
            if args.batch_size > 1 and args.url_contains in {"dl.acm.org", "doi.org"}:
                batch = candidates[index : index + args.batch_size]
                batch_rows = process_acm_batch(batch, args, browser, download_dir)
                for c, row in batch_rows:
                    index += 1
                    writer.writerow(row)
                    handle.flush()
                    counts[row["status"]] = counts.get(row["status"], 0) + 1
                    final = row.get("final_bytes")
                    final_msg = f" -> {int(final) / 1024 / 1024:.1f}MiB" if final else ""
                    print(
                        f"[{index}/{len(candidates)}] {row['status']} "
                        f"{c.compressed_bytes / 1024 / 1024:.1f}MiB{final_msg} {row['path']} :: "
                        f"{row['method'] or row['reason'][:160]}",
                        flush=True,
                    )
                continue

            c = candidates[index]
            index += 1
            row: dict[str, str] | None = None
            opened_urls = browser_urls(c, args.url_attempts)
            if not opened_urls:
                row = empty_row(c, "no_url", "no browser url")
            for opened_url in opened_urls:
                before = snapshot(download_dir)
                opened_at = time.time()
                subprocess.Popen(
                    [browser, f"--profile-directory={args.profile_directory}", "--new-tab", opened_url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                time.sleep(args.delay_after_open)
                downloaded = wait_for_download(download_dir, before, opened_at, args.wait)
                if downloaded is None:
                    row = empty_row(c, "download_timeout", f"timeout url={opened_url}")
                    continue
                row = replace_from_download(c, downloaded, args.dry_run)
                if not args.keep_downloads:
                    downloaded.unlink(missing_ok=True)
                if row["status"] != "download_invalid":
                    break
            assert row is not None
            writer.writerow(row)
            handle.flush()
            counts[row["status"]] = counts.get(row["status"], 0) + 1
            final = row.get("final_bytes")
            final_msg = f" -> {int(final) / 1024 / 1024:.1f}MiB" if final else ""
            print(
                f"[{index}/{len(candidates)}] {row['status']} "
                f"{c.compressed_bytes / 1024 / 1024:.1f}MiB{final_msg} {row['path']} :: "
                f"{row['method'] or row['reason'][:160]}",
                flush=True,
            )
    print(f"[DONE] counts={counts} log={rel(log_path)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--url-contains", default="")
    parser.add_argument("--url-not-contains", default="")
    parser.add_argument("--start-after", default="")
    parser.add_argument("--download-dir", default=str(DOWNLOAD_DIR))
    parser.add_argument("--browser", default="")
    parser.add_argument("--profile-directory", default="Profile 1")
    parser.add_argument("--wait", type=int, default=90)
    parser.add_argument("--delay-after-open", type=float, default=1.0)
    parser.add_argument("--url-attempts", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--compress-workers", type=int, default=1)
    parser.add_argument("--keep-downloads", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
