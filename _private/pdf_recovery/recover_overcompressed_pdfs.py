#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html
import http.client
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
PAPER_ROOT = ROOT / "obsidian-vault" / "paperPDFs"
PAPER_LIST = ROOT / "obsidian-vault" / "paper_list.csv"
INDEX_JSONL = ROOT / "obsidian-vault" / "index" / "index.jsonl"
ACM_QUEUE_FILES = [
    ROOT
    / "obsidian-vault"
    / "batches"
    / "wait_pdf_unified_queue_20260630"
    / "edge_acm_download_queue_20260630.csv",
    ROOT
    / "obsidian-vault"
    / "batches"
    / "wait_pdf_unified_queue_20260630"
    / "wait_pdf_unified_queue_20260630.csv",
]
WORK_ROOT = ROOT / "_private" / "pdf_recovery_work"
BACKUP_ROOT = ROOT / "_private" / "pdf_overcompressed_backup"
REPORT_DIR = ROOT / "_private" / "pdf_recovery"
LIMIT_BYTES = 20 * 1024 * 1024
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
ARXIV_RE = re.compile(r"(?P<id>\d{4}\.\d{4,5})(?:v\d+)?")
FETCH_TIMEOUT = 180
FETCH_ATTEMPTS = 3


@dataclass
class Candidate:
    path: Path
    original_bytes: int
    compressed_bytes: int
    source_url: str
    title: str
    venue: str


def run(cmd: list[str], timeout: int = 180) -> tuple[int, str, str]:
    try:
        cp = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            cwd=ROOT,
        )
        return (
            cp.returncode,
            cp.stdout.decode("utf-8", "replace"),
            cp.stderr.decode("utf-8", "replace"),
        )
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout after {timeout}s"


def pdf_pages(path: Path) -> tuple[int | None, str]:
    rc, out, err = run(["pdfinfo", str(path)], timeout=120)
    if rc != 0:
        return None, err.strip()[:500]
    for line in out.splitlines():
        if line.startswith("Pages:"):
            try:
                return int(line.split(":", 1)[1].strip()), ""
            except ValueError:
                return None, f"bad Pages line: {line}"
    return None, "pdfinfo did not report page count"


def qpdf_ok(path: Path) -> tuple[bool, str]:
    rc, out, err = run(["qpdf", "--check", str(path)], timeout=180)
    msg = (out + err).strip()
    if rc == 0:
        return True, msg[:500]
    if rc == 3 and "ERROR" not in msg.upper():
        return True, msg[:500]
    return False, msg[:500]


def valid_pdf(path: Path) -> tuple[bool, int | None, str]:
    if not path.exists() or path.stat().st_size < 1024:
        return False, None, "missing or too small"
    with path.open("rb") as f:
        head = f.read(5)
    if head != b"%PDF-":
        return False, None, "missing PDF header"
    pages, msg = pdf_pages(path)
    if pages is None:
        return False, None, f"pdfinfo failed: {msg}"
    ok, qmsg = qpdf_ok(path)
    if not ok:
        return False, pages, f"qpdf failed: {qmsg}"
    return True, pages, ""


def load_sources() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    if PAPER_LIST.exists():
        with PAPER_LIST.open(newline="", errors="replace") as f:
            for row in csv.DictReader(f):
                path = (row.get("pdf_path") or "").strip()
                url = (row.get("paper_link") or "").strip()
                if path and url:
                    out.setdefault(path, {}).update(
                        {
                            "source_url": url,
                            "title": (row.get("paper_title") or "").strip(),
                            "venue": (row.get("venue") or "").strip(),
                        }
                    )
    if INDEX_JSONL.exists():
        with INDEX_JSONL.open(errors="replace") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                path = (obj.get("pdf_ref") or obj.get("pdf_path") or "").strip()
                url = (obj.get("paper_link") or "").strip()
                if path and url:
                    out.setdefault(path, {}).update(
                        {
                            "source_url": out.get(path, {}).get("source_url") or url,
                            "title": out.get(path, {}).get("title")
                            or (obj.get("title") or "").strip(),
                            "venue": out.get(path, {}).get("venue")
                            or " ".join(
                                str(x)
                                for x in [obj.get("venue") or "", obj.get("year") or ""]
                                if x
                            ),
                        }
                    )
    for queue_path in ACM_QUEUE_FILES:
        if not queue_path.exists():
            continue
        with queue_path.open(newline="", errors="replace") as f:
            for row in csv.DictReader(f):
                path = (row.get("target_pdf_path") or row.get("pdf_path") or "").strip()
                url = (
                    row.get("resolved_pdf_url")
                    or row.get("pdf_url")
                    or row.get("paper_link")
                    or row.get("source_url")
                    or ""
                ).strip()
                if path and url:
                    out.setdefault(path, {}).update(
                        {
                            "source_url": url,
                            "title": (row.get("paper_title") or out.get(path, {}).get("title") or "").strip(),
                            "venue": (row.get("venue") or out.get(path, {}).get("venue") or "").strip(),
                        }
                    )
    return out


def load_severe(logs: Iterable[Path]) -> list[Candidate]:
    sources = load_sources()
    handled: set[str] = set()
    handled_statuses = {
        "replaced",
        "page_mismatch",
        "no_safe_under_20MiB",
        "final_invalid",
        "skipped",
        "internal_error",
    }
    for recovery_log in sorted(REPORT_DIR.glob("pdf_recovery_*.tsv")):
        try:
            with recovery_log.open(newline="", errors="replace") as f:
                for row in csv.DictReader(f, delimiter="\t"):
                    if row.get("status") in handled_statuses and row.get("path"):
                        handled.add(row["path"])
        except Exception:
            continue
    by_path: dict[str, Candidate] = {}
    for log in logs:
        if not log.exists():
            continue
        with log.open(newline="", errors="replace") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                if row.get("status") != "replaced":
                    continue
                path_str = row.get("path", "")
                if not path_str:
                    continue
                if path_str in handled:
                    continue
                original = int(row["original_bytes"])
                compressed = int(row["new_bytes"])
                if compressed * 10 >= original:
                    continue
                current_path = ROOT / path_str
                if not current_path.exists() or current_path.stat().st_size * 10 >= original:
                    continue
                meta = sources.get(path_str, {})
                source_url = meta.get("source_url", "")
                if not source_url:
                    continue
                by_path[path_str] = Candidate(
                    path=current_path,
                    original_bytes=original,
                    compressed_bytes=compressed,
                    source_url=source_url,
                    title=meta.get("title", ""),
                    venue=meta.get("venue", ""),
                )
    return sorted(by_path.values(), key=lambda c: c.original_bytes, reverse=True)


def arxiv_pdf_url(url: str) -> str | None:
    if "arxiv.org" not in url:
        return None
    match = ARXIV_RE.search(url)
    if not match:
        return None
    return f"https://arxiv.org/pdf/{match.group('id')}.pdf"


def openreview_pdf_url(url: str) -> str | None:
    parsed = urllib.parse.urlparse(url)
    if "openreview.net" not in parsed.netloc:
        return None
    qs = urllib.parse.parse_qs(parsed.query)
    paper_id = (qs.get("id") or [""])[0]
    if not paper_id:
        return None
    return f"https://openreview.net/pdf?id={urllib.parse.quote(paper_id)}"


def doi_pdf_urls(url: str) -> list[str]:
    parsed = urllib.parse.urlparse(url)
    if "doi.org" not in parsed.netloc:
        return []
    doi = parsed.path.strip("/")
    if not doi:
        return []
    return [
        f"https://dl.acm.org/doi/pdf/{doi}",
        f"https://dl.acm.org/doi/pdf/{doi}?download=true",
        url,
    ]


def absolutize(base: str, link: str) -> str:
    url = urllib.parse.urljoin(base, html.unescape(link))
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            urllib.parse.quote(parts.path, safe="/:%"),
            urllib.parse.quote(parts.query, safe="=&?/:+,%"),
            parts.fragment,
        )
    )


def extract_pdf_links(base: str, data: bytes) -> list[str]:
    text = data[:2_000_000].decode("utf-8", "replace")
    links: list[str] = []
    for pat in [
        r'href=["\']([^"\']+\.pdf(?:\?[^"\']*)?)["\']',
        r'content=["\']([^"\']+\.pdf(?:\?[^"\']*)?)["\']',
        r'(https?://arxiv\.org/(?:abs|pdf)/\d{4}\.\d{4,5}(?:v\d+)?(?:\.pdf)?)',
        r'(https?://openreview\.net/(?:forum|pdf)\?id=[^"\'>\s&]+)',
    ]:
        for m in re.finditer(pat, text, flags=re.I):
            links.append(absolutize(base, m.group(1)))
    seen = set()
    out = []
    for link in links:
        if link not in seen:
            seen.add(link)
            out.append(link)
    return out[:12]


def candidate_urls(url: str) -> list[str]:
    urls: list[str] = []
    for special in [arxiv_pdf_url(url), openreview_pdf_url(url)]:
        if special:
            urls.append(special)
    urls.extend(doi_pdf_urls(url))
    urls.append(url)
    seen = set()
    out = []
    for item in urls:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def fetch(url: str, timeout: int | None = None, attempts: int | None = None) -> tuple[bytes | None, str, str]:
    if timeout is None:
        timeout = FETCH_TIMEOUT
    if attempts is None:
        attempts = FETCH_ATTEMPTS
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/pdf,text/html;q=0.9,*/*;q=0.8",
        },
    )
    last = ""
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                content_type = resp.headers.get("Content-Type", "")
                final_url = resp.geturl()
                data = resp.read()
                return data, content_type, final_url
        except (urllib.error.URLError, TimeoutError, OSError, http.client.IncompleteRead) as exc:
            last = f"{type(exc).__name__}: {exc}"
            if attempt < attempts:
                time.sleep(2 * attempt)
    return None, "", last


def doi_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if "doi.org" not in parsed.netloc:
        return ""
    return parsed.path.strip("/")


def openalex_urls(source_url: str, title: str) -> list[str]:
    queries: list[str] = []
    doi = doi_from_url(source_url)
    if doi:
        queries.append(f"https://api.openalex.org/works/https://doi.org/{urllib.parse.quote(doi, safe='')}")
    if title:
        params = urllib.parse.urlencode({"search": title, "per-page": "3"})
        queries.append(f"https://api.openalex.org/works?{params}")

    out: list[str] = []
    for query in queries:
        data, _ctype, final = fetch(query, timeout=60)
        if data is None:
            continue
        try:
            obj = json.loads(data.decode("utf-8", "replace"))
        except Exception:
            continue
        works = obj.get("results") if isinstance(obj.get("results"), list) else [obj]
        for work in works:
            if not isinstance(work, dict):
                continue
            for loc_key in ["best_oa_location", "primary_location"]:
                loc = work.get(loc_key)
                if isinstance(loc, dict):
                    for key in ["pdf_url", "landing_page_url"]:
                        url = loc.get(key)
                        if url:
                            out.append(str(url))
            for loc in work.get("locations") or []:
                if isinstance(loc, dict):
                    for key in ["pdf_url", "landing_page_url"]:
                        url = loc.get(key)
                        if url:
                            out.append(str(url))
    seen = set()
    unique = []
    for url in out:
        if url not in seen and url != source_url:
            seen.add(url)
            unique.append(url)
    return unique[:12]


def download_pdf(source_url: str, out_path: Path, extra_urls: Iterable[str] = ()) -> tuple[bool, str]:
    queue = candidate_urls(source_url)
    queue.extend(extra_urls)
    seen = set(queue)
    errors: list[str] = []
    while queue:
        url = queue.pop(0)
        data, content_type, final_url = fetch(url)
        if data is None:
            errors.append(f"{url}: {final_url}")
            continue
        if data.startswith(b"%PDF-"):
            out_path.write_bytes(data)
            return True, final_url
        if "html" in content_type.lower() or b"<html" in data[:4096].lower():
            for link in extract_pdf_links(final_url, data):
                pdf_url = arxiv_pdf_url(link) or openreview_pdf_url(link) or link
                if pdf_url not in seen:
                    seen.add(pdf_url)
                    queue.append(pdf_url)
            errors.append(f"{url}: html no direct pdf yet")
        else:
            errors.append(f"{url}: non-pdf content-type={content_type}")
    return False, "; ".join(errors)[:1000]


def gs_compress(src: Path, dst: Path, resolution: int, jpegq: int) -> tuple[bool, str]:
    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.6",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        "-dDetectDuplicateImages=true",
        "-dCompressFonts=true",
        "-dSubsetFonts=true",
        "-dAutoRotatePages=/None",
        "-dDownsampleColorImages=true",
        "-dDownsampleGrayImages=true",
        "-dDownsampleMonoImages=true",
        "-dColorImageDownsampleType=/Bicubic",
        "-dGrayImageDownsampleType=/Bicubic",
        "-dMonoImageDownsampleType=/Subsample",
        f"-dColorImageResolution={resolution}",
        f"-dGrayImageResolution={resolution}",
        f"-dMonoImageResolution={max(resolution * 2, 300)}",
        f"-dJPEGQ={jpegq}",
        f"-sOutputFile={dst}",
        str(src),
    ]
    rc, _out, err = run(cmd, timeout=600)
    if rc != 0:
        return False, err.strip()[:500]
    return dst.exists(), "ok" if dst.exists() else "no output"


def best_under_limit(src: Path, expected_pages: int, work_dir: Path) -> tuple[Path | None, str]:
    if src.stat().st_size <= LIMIT_BYTES:
        return src, "original_under_20MiB"

    variants: list[tuple[str, Path]] = []
    notes: list[str] = []
    qpdf_path = work_dir / "lossless-qpdf.pdf"
    rc, _out, err = run(
        [
            "qpdf",
            "--object-streams=generate",
            "--compress-streams=y",
            "--recompress-flate",
            str(src),
            str(qpdf_path),
        ],
        timeout=240,
    )
    if rc == 0 and qpdf_path.exists():
        variants.append(("lossless-qpdf", qpdf_path))
        if qpdf_path.stat().st_size <= LIMIT_BYTES:
            ok_pdf, pages, reason = valid_pdf(qpdf_path)
            if ok_pdf and pages == expected_pages:
                return qpdf_path, f"lossless-qpdf; {qpdf_path.stat().st_size / 1024 / 1024:.2f}MiB"
            notes.append(f"lossless-qpdf: invalid {reason}; pages={pages}")
    else:
        try:
            qpdf_path.unlink()
        except FileNotFoundError:
            pass

    settings = [
        (600, 100),
        (600, 95),
        (450, 95),
        (360, 95),
        (300, 95),
        (260, 95),
        (240, 95),
        (220, 94),
        (200, 94),
        (200, 92),
        (180, 92),
        (180, 90),
        (160, 90),
        (144, 90),
    ]
    for resolution, jpegq in settings:
        out = work_dir / f"gs-{resolution}dpi-q{jpegq}.pdf"
        ok, msg = gs_compress(src, out, resolution, jpegq)
        if ok:
            variants.append((f"gs-{resolution}dpi-q{jpegq}", out))
        else:
            notes.append(f"gs-{resolution}-q{jpegq}: {msg}")

        valid_below: list[tuple[int, str, Path]] = []
        for name, path in variants:
            if not path.exists() or path.stat().st_size > LIMIT_BYTES:
                continue
            ok_pdf, pages, reason = valid_pdf(path)
            if ok_pdf and pages == expected_pages:
                valid_below.append((path.stat().st_size, name, path))
            else:
                notes.append(f"{name}: invalid {reason}; pages={pages}")
        if valid_below:
            valid_below.sort(reverse=True)
            size, name, path = valid_below[0]
            return path, f"{name}; {size / 1024 / 1024:.2f}MiB"

    return None, "; ".join(notes)[:1000] or "no variant under 20MiB"


def recover_one(c: Candidate, dry_run: bool) -> dict[str, str]:
    rel = c.path.relative_to(ROOT)
    row = {
        "status": "",
        "path": str(rel),
        "source_url": c.source_url,
        "original_logged_bytes": str(c.original_bytes),
        "overcompressed_bytes": str(c.compressed_bytes),
        "downloaded_bytes": "",
        "final_bytes": "",
        "method": "",
        "reason": "",
    }
    if not c.path.exists():
        row.update(status="skipped", reason="current pdf missing")
        return row
    current_ok, current_pages, current_reason = valid_pdf(c.path)
    if not current_ok or current_pages is None:
        row.update(status="skipped", reason=f"current pdf invalid: {current_reason}")
        return row

    work_dir = WORK_ROOT / re.sub(r"[^A-Za-z0-9_.-]+", "_", str(rel))
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    downloaded = work_dir / "downloaded.pdf"

    directish = any(
        marker in c.source_url
        for marker in ["arxiv.org", "openreview.net", "openaccess.thecvf.com"]
    ) or c.source_url.lower().split("?", 1)[0].endswith(".pdf")
    extra = [] if directish else openalex_urls(c.source_url, c.title)
    ok, msg = download_pdf(c.source_url, downloaded, extra_urls=extra)
    if not ok:
        row.update(status="download_failed", reason=msg)
        return row
    row["downloaded_bytes"] = str(downloaded.stat().st_size)

    ok_pdf, downloaded_pages, reason = valid_pdf(downloaded)
    if not ok_pdf or downloaded_pages is None:
        row.update(status="download_invalid", reason=reason)
        return row
    if downloaded_pages != current_pages:
        row.update(
            status="page_mismatch",
            reason=f"current_pages={current_pages}; downloaded_pages={downloaded_pages}",
        )
        return row

    best, method = best_under_limit(downloaded, downloaded_pages, work_dir)
    if best is None:
        row.update(status="no_safe_under_20MiB", reason=method)
        return row

    final_size = best.stat().st_size
    row.update(final_bytes=str(final_size), method=method)
    if final_size > LIMIT_BYTES:
        row.update(status="internal_error", reason="selected file exceeds limit")
        return row

    if dry_run:
        row.update(status="dry_run_ok", reason="not replaced")
        return row

    backup_path = BACKUP_ROOT / rel
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    if not backup_path.exists():
        shutil.copy2(c.path, backup_path)

    tmp_replace = c.path.with_name(c.path.name + ".recover-tmp")
    shutil.copy2(best, tmp_replace)
    ok_final, final_pages, final_reason = valid_pdf(tmp_replace)
    if not ok_final or final_pages != current_pages:
        try:
            tmp_replace.unlink()
        except FileNotFoundError:
            pass
        row.update(status="final_invalid", reason=f"{final_reason}; pages={final_pages}")
        return row
    os.replace(tmp_replace, c.path)
    row.update(status="replaced", reason="ok")
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="process at most N candidates")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--start-after", default="", help="resume after this relative PDF path")
    parser.add_argument("--url-contains", default="", help="only process candidates whose source URL contains this text")
    parser.add_argument(
        "--url-not-contains",
        action="append",
        default=[],
        help="skip candidates whose source URL contains this text; may be repeated",
    )
    parser.add_argument("--write-candidates", default="", help="write current candidate list to TSV and exit")
    parser.add_argument("--workers", type=int, default=1, help="number of concurrent recoveries")
    parser.add_argument("--fetch-timeout", type=int, default=180, help="per-URL network timeout in seconds")
    parser.add_argument("--fetch-attempts", type=int, default=3, help="per-URL network attempts")
    args = parser.parse_args()
    global FETCH_TIMEOUT, FETCH_ATTEMPTS
    FETCH_TIMEOUT = max(1, args.fetch_timeout)
    FETCH_ATTEMPTS = max(1, args.fetch_attempts)

    logs = [
        REPORT_DIR / "pdf_compression_parallel16_20260702T010918.tsv",
        *sorted(REPORT_DIR.glob("pdf_compression_retry_*.tsv")),
    ]
    candidates = load_severe(logs)
    if args.url_contains:
        candidates = [c for c in candidates if args.url_contains in c.source_url]
    for skipped_text in args.url_not_contains:
        if skipped_text:
            candidates = [c for c in candidates if skipped_text not in c.source_url]
    if args.start_after:
        paths = [str(c.path.relative_to(ROOT)) for c in candidates]
        if args.start_after in paths:
            candidates = candidates[paths.index(args.start_after) + 1 :]
    if args.limit:
        candidates = candidates[: args.limit]

    if args.write_candidates:
        out_path = ROOT / args.write_candidates
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "path",
                    "source_url",
                    "title",
                    "venue",
                    "original_bytes",
                    "compressed_bytes",
                    "current_bytes",
                ],
                delimiter="\t",
            )
            writer.writeheader()
            for c in candidates:
                writer.writerow(
                    {
                        "path": str(c.path.relative_to(ROOT)),
                        "source_url": c.source_url,
                        "title": c.title,
                        "venue": c.venue,
                        "original_bytes": c.original_bytes,
                        "compressed_bytes": c.compressed_bytes,
                        "current_bytes": c.path.stat().st_size if c.path.exists() else "",
                    }
                )
        print(f"[CANDIDATES] {len(candidates)} -> {out_path.relative_to(ROOT)}")
        return 0

    ts = time.strftime("%Y%m%dT%H%M%S")
    log_path = REPORT_DIR / f"pdf_recovery_{ts}.tsv"
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
    log_path.parent.mkdir(parents=True, exist_ok=True)
    WORK_ROOT.mkdir(parents=True, exist_ok=True)

    counts: dict[str, int] = {}
    with log_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        print(f"[RECOVERY] candidates={len(candidates)} dry_run={args.dry_run} log={log_path.relative_to(ROOT)}", flush=True)
        if args.workers <= 1:
            iterable = ((i, recover_one(c, args.dry_run), c) for i, c in enumerate(candidates, 1))
            for i, row, c in iterable:
                writer.writerow(row)
                f.flush()
                counts[row["status"]] = counts.get(row["status"], 0) + 1
                final = row.get("final_bytes")
                final_msg = f" -> {int(final)/1024/1024:.1f}MiB" if final else ""
                print(
                    f"[{i}/{len(candidates)}] {row['status']} {c.compressed_bytes/1024/1024:.1f}MiB{final_msg} "
                    f"{row['path']} :: {row['method'] or row['reason'][:160]}",
                    flush=True,
                )
        else:
            with ThreadPoolExecutor(max_workers=args.workers) as ex:
                futures = {ex.submit(recover_one, c, args.dry_run): c for c in candidates}
                for i, fut in enumerate(as_completed(futures), 1):
                    c = futures[fut]
                    try:
                        row = fut.result()
                    except Exception as exc:
                        row = {
                            "status": "exception",
                            "path": str(c.path.relative_to(ROOT)),
                            "source_url": c.source_url,
                            "original_logged_bytes": str(c.original_bytes),
                            "overcompressed_bytes": str(c.compressed_bytes),
                            "downloaded_bytes": "",
                            "final_bytes": "",
                            "method": "",
                            "reason": f"{type(exc).__name__}: {exc}",
                        }
                    writer.writerow(row)
                    f.flush()
                    counts[row["status"]] = counts.get(row["status"], 0) + 1
                    final = row.get("final_bytes")
                    final_msg = f" -> {int(final)/1024/1024:.1f}MiB" if final else ""
                    print(
                        f"[{i}/{len(candidates)}] {row['status']} {c.compressed_bytes/1024/1024:.1f}MiB{final_msg} "
                        f"{row['path']} :: {row['method'] or row['reason'][:160]}",
                        flush=True,
                    )
    print(f"[DONE] counts={counts} log={log_path.relative_to(ROOT)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
