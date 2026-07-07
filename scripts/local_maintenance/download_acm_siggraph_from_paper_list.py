#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import csv
import html
import http.cookiejar
import json
import os
import re
import shutil
import subprocess
import time
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

import fitz
import requests

try:
    from playwright.async_api import async_playwright
except ModuleNotFoundError:  # pragma: no cover - runtime guidance
    async_playwright = None


ROOT = Path(__file__).resolve().parents[2]
PAPER_LIST = ROOT / "obsidian-vault" / "paper_list.csv"
PDF_ROOT = ROOT / "obsidian-vault" / "paperPDFs"
PROFILE_DIR = ROOT / "_private" / "browser_profiles" / "acm_chrome"
REPORT_DIR = ROOT / "_private" / "acm_download_reports"
QUEUE_DIR = ROOT / "_private" / "acm_download_queue"
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


@dataclass(frozen=True)
class WorkItem:
    index: int
    title: str
    venue: str
    doi: str
    pdf_url: str


def require_playwright() -> None:
    if async_playwright is None:
        raise SystemExit(
            "Python package 'playwright' is missing. Install it with:\n"
            "  python3 -m pip install --user playwright\n"
            "This script uses the system Google Chrome, so a Playwright browser download is not required."
        )


def read_rows() -> list[dict[str, str]]:
    with PAPER_LIST.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CSV_FIELDS:
            raise SystemExit(f"Unexpected paper_list header: {reader.fieldnames}")
        return [dict(row) for row in reader]


def write_rows(rows: list[dict[str, str]]) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = PAPER_LIST.with_name(f"{PAPER_LIST.name}.bak_acm_{timestamp}")
    shutil.copy2(PAPER_LIST, backup)
    tmp = PAPER_LIST.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(PAPER_LIST)
    return backup


def safe_slug(text: str, max_len: int = 180) -> str:
    text = re.sub(r"[^0-9A-Za-z]+", "_", text or "").strip("_")
    text = re.sub(r"_+", "_", text)
    return text[:max_len].rstrip("_") or "paper"


def norm_text(text: str) -> str:
    text = re.sub(r"[^0-9A-Za-z]+", " ", text or "")
    return re.sub(r"\s+", " ", text).strip().lower()


def compact_id(text: str) -> str:
    return re.sub(r"[^0-9A-Za-z]+", "", text or "").lower()


def title_similarity(left: str, right: str) -> float:
    left_key = norm_text(left)
    right_key = norm_text(right)
    if not left_key or not right_key:
        return 0.0
    return SequenceMatcher(None, left_key, right_key).ratio()


def title_token_overlap(expected: str, observed: str) -> float:
    expected_tokens = set(norm_text(expected).split())
    observed_tokens = set(norm_text(observed).split())
    if not expected_tokens or not observed_tokens:
        return 0.0
    return len(expected_tokens & observed_tokens) / max(1, len(expected_tokens))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def is_sig_graphics_row(row: dict[str, str]) -> bool:
    value = f"{row.get('venue', '')} {row.get('sort', '')}".upper()
    return any(key in value for key in ("SIGGRAPH", "SIGA", "TOG"))


def extract_acm_doi(row: dict[str, str]) -> str:
    text = " ".join(
        [
            row.get("paper_link") or "",
            row.get("project_link_or_github_link") or "",
        ]
    )
    match = re.search(r"(10\.1145/[0-9.]+)", text)
    return match.group(1) if match else ""


def pdf_path_for(title: str, venue: str) -> Path:
    return PDF_ROOT / venue.replace(" ", "_") / f"{safe_slug(title)}.pdf"


def is_valid_pdf(path: Path) -> tuple[bool, str]:
    if not path.exists() or not path.is_file():
        return False, "missing"
    try:
        with path.open("rb") as handle:
            if not handle.read(8).startswith(b"%PDF"):
                return False, "not_pdf_magic"
        with fitz.open(path) as doc:
            if doc.page_count < 1:
                return False, "zero_pages"
    except Exception as exc:
        return False, f"pdf_invalid:{type(exc).__name__}:{exc}"
    return True, "ok"


def load_cookie_jar(cookie_file: Path) -> http.cookiejar.MozillaCookieJar:
    jar = http.cookiejar.MozillaCookieJar(str(cookie_file))
    try:
        jar.load(ignore_discard=True, ignore_expires=True)
    except Exception as exc:
        raise SystemExit(f"Failed to load Netscape cookies file {cookie_file}: {type(exc).__name__}: {exc}") from exc
    return jar


def http_session(cookie_file: Path) -> requests.Session:
    sess = requests.Session()
    sess.cookies = load_cookie_jar(cookie_file)
    sess.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
            ),
            "Accept": "application/pdf,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://dl.acm.org/",
        }
    )
    return sess


def download_http_one(item: WorkItem, cookie_file: Path, *, timeout: int) -> dict[str, object]:
    out_path = pdf_path_for(item.title, item.venue)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sess = http_session(cookie_file)
    fd, tmp_name = tempfile.mkstemp(prefix=out_path.name + ".", suffix=".part", dir=str(out_path.parent))
    Path(tmp_name).unlink(missing_ok=True)
    tmp_path = Path(tmp_name)
    try:
        with sess.get(item.pdf_url, allow_redirects=True, stream=True, timeout=timeout) as resp:
            content_type = (resp.headers.get("content-type") or "").lower()
            final_url = resp.url
            if resp.status_code >= 400:
                return {
                    "ok": False,
                    "title": item.title,
                    "venue": item.venue,
                    "doi": item.doi,
                    "url": item.pdf_url,
                    "note": f"http_{resp.status_code}:content_type={content_type}:final={final_url}",
                }
            total = 0
            with tmp_path.open("wb") as handle:
                for chunk in resp.iter_content(chunk_size=1024 * 256):
                    if not chunk:
                        continue
                    total += len(chunk)
                    if total > 120 * 1024 * 1024:
                        return {"ok": False, "title": item.title, "venue": item.venue, "doi": item.doi, "url": item.pdf_url, "note": "too_large"}
                    handle.write(chunk)
            ok, why = is_valid_pdf(tmp_path)
            if not ok:
                return {
                    "ok": False,
                    "title": item.title,
                    "venue": item.venue,
                    "doi": item.doi,
                    "url": item.pdf_url,
                    "note": f"{why}:content_type={content_type}:final={final_url}",
                }
            tmp_path.replace(out_path)
            return {
                "ok": True,
                "title": item.title,
                "venue": item.venue,
                "doi": item.doi,
                "url": item.pdf_url,
                "pdf_path": rel(out_path),
                "bytes": total,
            }
    except Exception as exc:
        return {"ok": False, "title": item.title, "venue": item.venue, "doi": item.doi, "url": item.pdf_url, "note": f"error:{type(exc).__name__}:{exc}"}
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except Exception:
            pass
        try:
            import os

            os.close(fd)
        except Exception:
            pass


def pdf_text_candidates(path: Path) -> list[str]:
    candidates: list[str] = []
    try:
        with fitz.open(path) as doc:
            metadata_title = (doc.metadata or {}).get("title") or ""
            if metadata_title.strip():
                candidates.append(metadata_title.strip())
            for page_index in range(min(2, doc.page_count)):
                text = doc.load_page(page_index).get_text("text") or ""
                if text.strip():
                    candidates.append(text[:5000])
                for raw_line in text.splitlines()[:60]:
                    line = re.sub(r"\s+", " ", raw_line).strip()
                    if len(line) >= 10 and re.search(r"[A-Za-z]", line):
                        candidates.append(line)
    except Exception:
        return candidates
    seen: set[str] = set()
    unique: list[str] = []
    for candidate in candidates:
        key = norm_text(candidate)[:240]
        if key and key not in seen:
            seen.add(key)
            unique.append(candidate)
    return unique


def collect_work(rows: list[dict[str, str]], *, limit: int = 0, skip_doi_suffixes: set[str] | None = None) -> list[WorkItem]:
    skip_doi_suffixes = skip_doi_suffixes or set()
    work: list[WorkItem] = []
    for index, row in enumerate(rows):
        if (row.get("state") or "").strip().lower() != "wait":
            continue
        if not is_sig_graphics_row(row):
            continue
        doi = extract_acm_doi(row)
        if not doi:
            continue
        doi_suffix = doi.split("/", 1)[-1]
        doi_suffix_id = compact_id(doi_suffix)
        if (
            doi_suffix in skip_doi_suffixes
            or doi_suffix_id in skip_doi_suffixes
            or any(doi_suffix_id.endswith(skip) for skip in skip_doi_suffixes)
        ):
            continue
        out_path = pdf_path_for(row["paper_title"], row["venue"])
        ok, _ = is_valid_pdf(out_path)
        if ok:
            continue
        work.append(
            WorkItem(
                index=index,
                title=row["paper_title"],
                venue=row["venue"],
                doi=doi,
                pdf_url=f"https://dl.acm.org/doi/pdf/{doi}",
            )
        )
        if limit and len(work) >= limit:
            break
    return work


def write_queue(args: argparse.Namespace) -> None:
    rows = read_rows()
    work = collect_work(rows, limit=args.limit)
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    html_path = QUEUE_DIR / f"acm_siggraph_wait_queue_{timestamp}.html"
    tsv_path = QUEUE_DIR / f"acm_siggraph_wait_queue_{timestamp}.tsv"

    with tsv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["venue", "title", "doi", "pdf_url", "target_pdf_path"])
        for item in work:
            writer.writerow([item.venue, item.title, item.doi, item.pdf_url, rel(pdf_path_for(item.title, item.venue))])

    rows_html = []
    for i, item in enumerate(work, 1):
        rows_html.append(
            "<tr>"
            f"<td>{i}</td>"
            f"<td>{html.escape(item.venue)}</td>"
            f"<td>{html.escape(item.title)}</td>"
            f"<td><code>{html.escape(item.doi)}</code></td>"
            f"<td><a href=\"{html.escape(item.pdf_url)}\" target=\"_blank\" rel=\"noreferrer\">PDF</a></td>"
            f"<td><code>{html.escape(rel(pdf_path_for(item.title, item.venue)))}</code></td>"
            "</tr>"
        )
    html_path.write_text(
        "\n".join(
            [
                "<!doctype html>",
                "<meta charset=\"utf-8\">",
                "<title>ACM SIGGRAPH PDF Queue</title>",
                "<style>",
                "body{font-family:system-ui,sans-serif;max-width:1200px;margin:24px auto;padding:0 16px;line-height:1.4}",
                "table{border-collapse:collapse;width:100%;font-size:14px}",
                "td,th{border:1px solid #ddd;padding:6px;vertical-align:top}",
                "th{background:#f6f6f6;text-align:left;position:sticky;top:0}",
                "code{font-size:12px}",
                "</style>",
                "<h1>ACM SIGGRAPH PDF Queue</h1>",
                f"<p>Total links: {len(work)}. Log in with a normal browser, then open PDF links and save downloads into a single folder.</p>",
                "<table>",
                "<thead><tr><th>#</th><th>Venue</th><th>Title</th><th>DOI</th><th>Link</th><th>Target</th></tr></thead>",
                "<tbody>",
                *rows_html,
                "</tbody></table>",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps({"event": "queue_written", "items": len(work), "html": rel(html_path), "tsv": rel(tsv_path)}, ensure_ascii=False))


def score_pdf_for_item(path: Path, item: WorkItem) -> tuple[int, str]:
    stem_id = compact_id(path.stem)
    doi_suffix = item.doi.split("/", 1)[-1]
    doi_suffix_id = compact_id(doi_suffix)
    title_id = compact_id(item.title)
    if doi_suffix_id and doi_suffix_id in stem_id:
        return 120, "filename_doi"
    if title_id and title_id[:40] in stem_id:
        return 90, "filename_title"

    best_score = 0
    best_reason = "no_match"
    for candidate in pdf_text_candidates(path):
        candidate_id = compact_id(candidate)
        if doi_suffix_id and doi_suffix_id in candidate_id:
            return 110, "text_doi"
        similarity = title_similarity(item.title, candidate)
        overlap = title_token_overlap(item.title, candidate)
        score = int(max(similarity * 100, overlap * 95))
        if score > best_score:
            best_score = score
            best_reason = f"text_title:{similarity:.2f}:{overlap:.2f}"
    return best_score, best_reason


def import_folder(args: argparse.Namespace) -> None:
    rows = read_rows()
    work = collect_work(rows, limit=0)
    by_doi_suffix: dict[str, WorkItem] = {}
    for item in work:
        suffix = compact_id(item.doi.split("/", 1)[-1])
        if suffix and suffix not in by_doi_suffix:
            by_doi_suffix[suffix] = item
    folder = Path(args.folder).expanduser().resolve()
    if not folder.exists():
        raise SystemExit(f"Folder does not exist: {folder}")
    pdfs = sorted(path for path in folder.rglob("*.pdf") if path.is_file())
    if args.limit:
        pdfs = pdfs[: args.limit]
    print(json.dumps({"event": "scan", "pdfs": len(pdfs), "work_items": len(work), "folder": str(folder)}, ensure_ascii=False))

    used_items: set[int] = set()
    results: list[dict[str, object]] = []
    for pdf in pdfs:
        ok, why = is_valid_pdf(pdf)
        if not ok:
            results.append({"ok": False, "source": str(pdf), "note": why})
            continue
        stem_id = compact_id(pdf.stem)
        direct_item = by_doi_suffix.get(stem_id)
        if direct_item and direct_item.index not in used_items:
            best: tuple[int, str, WorkItem | None] = (125, "filename_exact_doi_suffix", direct_item)
        else:
            best = (0, "no_match", None)
            for item in work:
                if item.index in used_items:
                    continue
                score, reason = score_pdf_for_item(pdf, item)
                if score > best[0]:
                    best = (score, reason, item)
        score, reason, item = best
        if item is None or score < args.min_score:
            results.append({"ok": False, "source": str(pdf), "score": score, "note": reason})
            continue
        out_path = pdf_path_for(item.title, item.venue)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if not args.dry_run:
            if args.copy:
                shutil.copy2(pdf, out_path)
            else:
                shutil.move(str(pdf), out_path)
            rows[item.index]["state"] = "Downloaded"
            rows[item.index]["pdf_path"] = rel(out_path)
        used_items.add(item.index)
        results.append(
            {
                "ok": True,
                "source": str(pdf),
                "score": score,
                "reason": reason,
                "title": item.title,
                "venue": item.venue,
                "pdf_path": rel(out_path),
            }
        )

    updated = sum(1 for item in results if item.get("ok"))
    backup = ""
    if updated and not args.dry_run:
        backup = rel(write_rows(rows))
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_path = REPORT_DIR / f"acm_manual_import_{timestamp}.json"
    report_path.write_text(
        json.dumps(
            {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "folder": str(folder),
                "dry_run": args.dry_run,
                "updated": updated,
                "paper_list_backup": backup,
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps({"event": "import_complete", "updated": updated, "dry_run": args.dry_run, "report": rel(report_path), "paper_list_backup": backup}, ensure_ascii=False))


def download_http(args: argparse.Namespace) -> None:
    rows = read_rows()
    work = collect_work(rows, limit=args.limit)
    cookie_file = Path(args.cookie_file).expanduser().resolve()
    if not cookie_file.exists():
        raise SystemExit(f"Cookie file does not exist: {cookie_file}")
    print(json.dumps({"event": "planned", "tasks": len(work), "jobs": args.jobs, "cookie_file": str(cookie_file)}, ensure_ascii=False))
    if args.dry_run:
        for item in work[:20]:
            print(json.dumps(item.__dict__, ensure_ascii=False))
        return
    if not work:
        return

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        future_map = {executor.submit(download_http_one, item, cookie_file, timeout=args.timeout): item for item in work}
        for done, future in enumerate(as_completed(future_map), 1):
            item = future_map[future]
            result = future.result()
            results.append(result)
            if result.get("ok"):
                rows[item.index]["state"] = "Downloaded"
                rows[item.index]["pdf_path"] = str(result["pdf_path"])
            print(
                json.dumps(
                    {
                        "event": "progress",
                        "done": done,
                        "total": len(work),
                        "ok": sum(1 for r in results if r.get("ok")),
                        "last_ok": bool(result.get("ok")),
                        "title": item.title[:100],
                        "note": result.get("note", ""),
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )

    updated = sum(1 for result in results if result.get("ok"))
    backup = rel(write_rows(rows)) if updated else ""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_path = REPORT_DIR / f"acm_cookie_download_{timestamp}.json"
    report_path.write_text(
        json.dumps(
            {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "planned": len(work),
                "downloaded": updated,
                "paper_list_backup": backup,
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps({"event": "complete", "planned": len(work), "downloaded": updated, "report": rel(report_path), "paper_list_backup": backup}, ensure_ascii=False))


def sync_existing(args: argparse.Namespace) -> None:
    rows = read_rows()
    updated = 0
    synced: list[dict[str, str]] = []
    for row in rows:
        if (row.get("state") or "").strip().lower() != "wait":
            continue
        if not is_sig_graphics_row(row):
            continue
        if not extract_acm_doi(row):
            continue
        out_path = pdf_path_for(row["paper_title"], row["venue"])
        ok, why = is_valid_pdf(out_path)
        if not ok:
            continue
        row["state"] = "Downloaded"
        row["pdf_path"] = rel(out_path)
        updated += 1
        synced.append({"title": row["paper_title"], "venue": row["venue"], "pdf_path": row["pdf_path"], "note": why})
        if args.limit and updated >= args.limit:
            break
    backup = ""
    if updated and not args.dry_run:
        backup = rel(write_rows(rows))
    print(json.dumps({"event": "sync_existing_complete", "updated": updated, "dry_run": args.dry_run, "paper_list_backup": backup, "synced": synced[:20]}, ensure_ascii=False))


def browser_batch(args: argparse.Namespace) -> None:
    rows = read_rows()
    skip = {compact_id(value) for value in args.skip_doi_suffix}
    work = collect_work(rows, limit=args.limit, skip_doi_suffixes=skip)
    download_dir = Path(args.download_dir).expanduser().resolve()
    download_dir.mkdir(parents=True, exist_ok=True)
    print(json.dumps({"event": "planned", "tasks": len(work), "download_dir": str(download_dir)}, ensure_ascii=False))
    if args.dry_run:
        for item in work[:20]:
            print(json.dumps(item.__dict__, ensure_ascii=False))
        return
    if not work:
        return

    before = {path.resolve() for path in download_dir.glob("*.pdf")}
    url_file = QUEUE_DIR / "latest_browser_batch_urls.txt"
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    url_file.write_text("\n".join(item.pdf_url for item in work) + "\n", encoding="utf-8")

    browser = (
        args.browser
        or shutil.which("microsoft-edge")
        or shutil.which("microsoft-edge-stable")
        or shutil.which("google-chrome")
        or shutil.which("google-chrome-stable")
    )
    if not browser:
        raise SystemExit("microsoft-edge/google-chrome not found")

    for done, item in enumerate(work, 1):
        subprocess.Popen([browser, "--new-tab", item.pdf_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(json.dumps({"event": "opened", "done": done, "total": len(work), "title": item.title[:100], "url": item.pdf_url}, ensure_ascii=False), flush=True)
        time.sleep(args.delay)

    print(json.dumps({"event": "waiting_for_downloads", "seconds": args.wait}, ensure_ascii=False), flush=True)
    deadline = time.time() + args.wait
    while time.time() < deadline:
        partials = list(download_dir.glob("*.crdownload")) + list(download_dir.glob("*.part"))
        if not partials and len([p for p in download_dir.glob("*.pdf") if p.resolve() not in before]) >= max(1, min(len(work), args.expect or len(work))):
            break
        time.sleep(2)

    cmd_args = argparse.Namespace(
        folder=str(download_dir),
        limit=0,
        min_score=args.min_score,
        copy=False,
        dry_run=args.import_dry_run,
    )
    import_folder(cmd_args)


async def open_login_page(args: argparse.Namespace) -> None:
    require_playwright()
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            str(PROFILE_DIR),
            channel="chrome",
            headless=False,
            accept_downloads=True,
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto(args.url, wait_until="domcontentloaded", timeout=60000)
        print(f"Opened Chrome with persistent profile: {PROFILE_DIR}")
        print("Log in to ACM in that browser. Return here and press Enter after a PDF page is accessible.")
        await asyncio.to_thread(input)
        await context.close()


async def download_one(context, item: WorkItem, *, timeout_ms: int) -> dict[str, object]:
    out_path = pdf_path_for(item.title, item.venue)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    page = await context.new_page()
    try:
        async with page.expect_download(timeout=timeout_ms) as download_info:
            await page.goto(item.pdf_url, wait_until="domcontentloaded", timeout=timeout_ms)
        download = await download_info.value
        tmp_path = out_path.with_suffix(out_path.suffix + ".part")
        await download.save_as(str(tmp_path))
        ok, why = is_valid_pdf(tmp_path)
        if not ok:
            tmp_path.unlink(missing_ok=True)
            return {"ok": False, "title": item.title, "venue": item.venue, "url": item.pdf_url, "note": why}
        tmp_path.replace(out_path)
        return {
            "ok": True,
            "title": item.title,
            "venue": item.venue,
            "doi": item.doi,
            "url": item.pdf_url,
            "pdf_path": rel(out_path),
        }
    except Exception as exc:
        response = None
        try:
            response = await page.goto(item.pdf_url, wait_until="domcontentloaded", timeout=timeout_ms)
            content_type = response.headers.get("content-type", "") if response else ""
            parsed = urlparse(page.url)
            note = f"no_download:{type(exc).__name__}:final={parsed.netloc}{parsed.path}:content_type={content_type}"
        except Exception as second_exc:
            note = f"error:{type(exc).__name__}:{exc}; retry_error:{type(second_exc).__name__}:{second_exc}"
        return {"ok": False, "title": item.title, "venue": item.venue, "url": item.pdf_url, "note": note}
    finally:
        await page.close()


async def run_download(args: argparse.Namespace) -> None:
    rows = read_rows()
    work = collect_work(rows, limit=args.limit)
    print(json.dumps({"event": "planned", "tasks": len(work), "profile": str(PROFILE_DIR)}, ensure_ascii=False))
    if args.dry_run:
        for item in work[:20]:
            print(json.dumps(item.__dict__, ensure_ascii=False))
        return
    require_playwright()
    if not work:
        return

    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            str(PROFILE_DIR),
            channel="chrome",
            headless=args.headless,
            accept_downloads=True,
        )
        results: list[dict[str, object]] = []
        for done, item in enumerate(work, 1):
            result = await download_one(context, item, timeout_ms=args.timeout * 1000)
            results.append(result)
            if result.get("ok"):
                row = rows[item.index]
                row["state"] = "Downloaded"
                row["pdf_path"] = str(result["pdf_path"])
            print(
                json.dumps(
                    {
                        "event": "progress",
                        "done": done,
                        "total": len(work),
                        "ok": sum(1 for r in results if r.get("ok")),
                        "last_ok": bool(result.get("ok")),
                        "title": item.title[:100],
                        "note": result.get("note", ""),
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
        await context.close()

    updated = sum(1 for result in results if result.get("ok"))
    backup = write_rows(rows) if updated else ""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_path = REPORT_DIR / f"acm_siggraph_download_{timestamp}.json"
    report_path.write_text(
        json.dumps(
            {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "planned": len(work),
                "downloaded": updated,
                "paper_list_backup": rel(backup) if backup else "",
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "event": "complete",
                "planned": len(work),
                "downloaded": updated,
                "report": rel(report_path),
                "paper_list_backup": rel(backup) if backup else "",
            },
            ensure_ascii=False,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    login = sub.add_parser("login", help="Open a persistent Chrome profile for manual ACM login")
    login.add_argument("--url", default="https://dl.acm.org/")

    download = sub.add_parser("download", help="Download ACM SIGGRAPH PDFs using the logged-in profile")
    download.add_argument("--limit", type=int, default=5)
    download.add_argument("--timeout", type=int, default=60)
    download.add_argument("--headless", action="store_true")
    download.add_argument("--dry-run", action="store_true")

    queue = sub.add_parser("queue", help="Write a manual ACM download queue for a normal browser")
    queue.add_argument("--limit", type=int, default=50)

    import_cmd = sub.add_parser("import-folder", help="Import manually downloaded ACM PDFs back into paper_list.csv")
    import_cmd.add_argument("--folder", required=True)
    import_cmd.add_argument("--limit", type=int, default=0)
    import_cmd.add_argument("--min-score", type=int, default=78)
    import_cmd.add_argument("--copy", action="store_true", help="Copy PDFs instead of moving them")
    import_cmd.add_argument("--dry-run", action="store_true")

    http_cmd = sub.add_parser("download-http", help="Download ACM PDFs with cookies exported from a normal browser")
    http_cmd.add_argument("--cookie-file", required=True, help="Netscape cookies.txt exported from the logged-in browser")
    http_cmd.add_argument("--limit", type=int, default=5)
    http_cmd.add_argument("--jobs", type=int, default=2)
    http_cmd.add_argument("--timeout", type=int, default=60)
    http_cmd.add_argument("--dry-run", action="store_true")

    browser_cmd = sub.add_parser("browser-batch", help="Open ACM PDF URLs in the normal browser and import downloaded PDFs")
    browser_cmd.add_argument("--download-dir", required=True)
    browser_cmd.add_argument("--limit", type=int, default=20)
    browser_cmd.add_argument("--delay", type=float, default=2.5)
    browser_cmd.add_argument("--wait", type=int, default=180)
    browser_cmd.add_argument("--expect", type=int, default=0)
    browser_cmd.add_argument("--min-score", type=int, default=78)
    browser_cmd.add_argument("--browser", default="")
    browser_cmd.add_argument("--skip-doi-suffix", action="append", default=[])
    browser_cmd.add_argument("--import-dry-run", action="store_true")
    browser_cmd.add_argument("--dry-run", action="store_true")

    sync_cmd = sub.add_parser("sync-existing", help="Mark Wait ACM rows as Downloaded when the expected PDF already exists")
    sync_cmd.add_argument("--limit", type=int, default=0)
    sync_cmd.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()
    if args.command == "login":
        asyncio.run(open_login_page(args))
    elif args.command == "download":
        asyncio.run(run_download(args))
    elif args.command == "queue":
        write_queue(args)
    elif args.command == "import-folder":
        import_folder(args)
    elif args.command == "download-http":
        download_http(args)
    elif args.command == "browser-batch":
        browser_batch(args)
    elif args.command == "sync-existing":
        sync_existing(args)


if __name__ == "__main__":
    main()
