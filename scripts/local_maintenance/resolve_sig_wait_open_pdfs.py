#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import tempfile
import threading
import time
import xml.etree.ElementTree as ET
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import quote, urlencode, urljoin, urlparse

import fitz
import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[2]
PAPER_LIST = ROOT / "obsidian-vault" / "paper_list.csv"
PDF_ROOT = ROOT / "obsidian-vault" / "paperPDFs"
REPORT_DIR = ROOT / "_private" / "sig_wait_resolve_20260701"
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
class Candidate:
    url: str
    source: str
    direct: bool = False


thread_local = threading.local()
arxiv_lock = threading.Lock()
last_arxiv_request = 0.0
crossref_lock = threading.Lock()
last_crossref_request = 0.0


def session() -> requests.Session:
    sess = getattr(thread_local, "session", None)
    if sess is None:
        sess = requests.Session()
        sess.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) BITE SIG PDF resolver/1.0",
                "Accept": "text/html,application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
        )
        thread_local.session = sess
    return sess


def read_rows() -> list[dict[str, str]]:
    with PAPER_LIST.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CSV_FIELDS:
            raise SystemExit(f"Unexpected paper_list header: {reader.fieldnames}")
        return [dict(row) for row in reader]


def write_rows(rows: list[dict[str, str]]) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = PAPER_LIST.with_name(f"{PAPER_LIST.name}.bak_resolve_sig_wait_{timestamp}")
    shutil.copy2(PAPER_LIST, backup)
    tmp = PAPER_LIST.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(PAPER_LIST)
    return backup


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def safe_slug(text: str, max_len: int = 180) -> str:
    text = re.sub(r"[^0-9A-Za-z]+", "_", text or "").strip("_")
    text = re.sub(r"_+", "_", text)
    return text[:max_len].rstrip("_") or "paper"


def norm_title(text: str) -> str:
    text = (text or "").replace("’", "'").replace("–", "-").replace("—", "-")
    text = re.sub(r"[^0-9A-Za-z]+", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def title_similarity(left: str, right: str) -> float:
    left_key = norm_title(left)
    right_key = norm_title(right)
    if not left_key or not right_key:
        return 0.0
    return SequenceMatcher(None, left_key, right_key).ratio()


def token_overlap(expected: str, observed: str) -> float:
    expected_tokens = set(norm_title(expected).split())
    observed_tokens = set(norm_title(observed).split())
    if not expected_tokens or not observed_tokens:
        return 0.0
    return len(expected_tokens & observed_tokens) / len(expected_tokens)


def target_path(row: dict[str, str]) -> Path:
    return PDF_ROOT / row["venue"].replace(" ", "_") / f"{safe_slug(row['paper_title'])}.pdf"


def resolve_path(raw: str) -> Path | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute():
        path = ROOT / path
    return path


def pdf_title_candidates(path: Path) -> list[str]:
    out: list[str] = []
    try:
        with fitz.open(path) as doc:
            metadata_title = (doc.metadata or {}).get("title") or ""
            if metadata_title.strip():
                out.append(metadata_title.strip())
            if doc.page_count:
                text = doc.load_page(0).get_text("text") or ""
                full = re.sub(r"\s+", " ", text).strip()
                if full:
                    out.append(full[:3000])
                for raw_line in text.splitlines()[:45]:
                    line = re.sub(r"\s+", " ", raw_line).strip()
                    if len(line) >= 12 and re.search(r"[A-Za-z]", line):
                        out.append(line)
    except Exception:
        return out
    seen: set[str] = set()
    unique: list[str] = []
    for item in out:
        key = norm_title(item)[:240]
        if key and key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def title_matches_pdf(path: Path, title: str) -> tuple[bool, str]:
    candidates = pdf_title_candidates(path)
    if not candidates:
        return True, "title_unchecked"
    best = max((max(title_similarity(title, item), token_overlap(title, item)) for item in candidates), default=0.0)
    return (best >= 0.62), f"title_score:{best:.2f}"


def is_valid_pdf(path: Path, *, expected_title: str = "") -> tuple[bool, str]:
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
    if expected_title:
        ok, why = title_matches_pdf(path, expected_title)
        if not ok:
            return False, why
    return True, "ok"


def arxiv_pdf(url: str) -> str:
    parsed = urlparse(url)
    if "arxiv.org" not in parsed.netloc.lower():
        return url
    match = re.search(r"/(?:abs|html|pdf)/([^/?#]+)", parsed.path)
    if not match:
        return url
    arxiv_id = match.group(1).removesuffix(".pdf")
    return f"https://arxiv.org/pdf/{arxiv_id}.pdf"


def normalize_url(url: str) -> str:
    url = (url or "").strip().replace(" ", "%20")
    if not url:
        return ""
    return arxiv_pdf(url)


def is_direct_pdfish(url: str) -> bool:
    low = url.lower()
    return "arxiv.org/pdf/" in low or "openreview.net/pdf" in low or low.endswith(".pdf") or ".pdf?" in low


def skip_download_reason(url: str) -> str:
    low = url.lower()
    if not low:
        return "empty_url"
    if "dl.acm.org/doi" in low or "doi.org/10.1145" in low:
        return "acm_doi_queue"
    if any(host in low for host in ("youtube.com", "youtu.be", "vimeo.com")):
        return "video_url"
    if low.endswith((".zip", ".tar", ".gz", ".mp4", ".mov")):
        return "non_pdf_asset"
    return ""


def unique_candidates(candidates: list[Candidate]) -> list[Candidate]:
    seen: set[str] = set()
    out: list[Candidate] = []
    for item in candidates:
        url = normalize_url(item.url)
        if not url or url in seen:
            continue
        seen.add(url)
        out.append(Candidate(url=url, source=item.source, direct=item.direct or is_direct_pdfish(url)))
    return out


def row_link_candidates(row: dict[str, str]) -> list[Candidate]:
    out: list[Candidate] = []
    for key in ("paper_link", "project_link_or_github_link"):
        value = (row.get(key) or "").strip()
        if value:
            out.append(Candidate(value, f"csv:{key}", direct=is_direct_pdfish(value)))
    return unique_candidates(out)


def extract_landing_candidates(html: str, base_url: str) -> tuple[list[Candidate], list[str]]:
    soup = BeautifulSoup(html, "html.parser")
    candidates: list[Candidate] = []
    dois: list[str] = []
    for match in re.findall(r"10\.1145/[0-9.]+", html):
        if match not in dois:
            dois.append(match)
    for meta in soup.find_all("meta"):
        name = (meta.get("name") or meta.get("property") or "").strip().lower()
        content = (meta.get("content") or "").strip()
        if content and ("pdf" in name or name in {"citation_pdf_url", "dc.identifier"}):
            candidates.append(Candidate(urljoin(base_url, content), f"meta:{name}", direct=True))
    for a in soup.find_all("a"):
        href = (a.get("href") or "").strip()
        if not href:
            continue
        text = a.get_text(" ", strip=True).lower()
        joined = urljoin(base_url, href)
        low = joined.lower()
        if ".pdf" in low or "arxiv.org/abs/" in low or "arxiv.org/pdf/" in low or "openreview.net/pdf" in low or ("download" in low and "pdf" in text):
            candidates.append(Candidate(joined, "html:a", direct=is_direct_pdfish(joined)))
    for raw in re.findall(r"https?://[^\"'<>\\s]+", html):
        raw = raw.rstrip(").,;")
        low = raw.lower()
        if ".pdf" in low or "arxiv.org/abs/" in low or "arxiv.org/pdf/" in low:
            candidates.append(Candidate(raw, "html:raw", direct=is_direct_pdfish(raw)))
    return unique_candidates(candidates), dois


def fetch_landing(url: str, *, timeout: int) -> tuple[list[Candidate], list[str], str]:
    reason = skip_download_reason(url)
    if reason == "acm_doi_queue":
        doi = re.search(r"10\.1145/[0-9.]+", url)
        return [], [doi.group(0)] if doi else [], reason
    if reason:
        return [], [], reason
    try:
        resp = session().get(url, timeout=timeout, allow_redirects=True)
        ctype = (resp.headers.get("content-type") or "").lower()
        if resp.status_code >= 400:
            return [], [], f"http_{resp.status_code}"
        if "pdf" in ctype or resp.content[:8].startswith(b"%PDF"):
            return [Candidate(resp.url, "landing:response_pdf", direct=True)], [], "response_pdf"
        if "html" not in ctype and "<html" not in resp.text[:500].lower():
            return [], [], f"not_html:{ctype}"
        candidates, dois = extract_landing_candidates(resp.text, resp.url)
        return candidates, dois, "html"
    except Exception as exc:
        return [], [], f"error:{type(exc).__name__}:{exc}"


def download_pdf(url: str, out_path: Path, *, timeout: int, expected_title: str) -> tuple[bool, str]:
    reason = skip_download_reason(url)
    if reason:
        return False, reason
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=out_path.name + ".", suffix=".part", dir=str(out_path.parent))
    Path(tmp_name).unlink(missing_ok=True)
    tmp = Path(tmp_name)
    try:
        with session().get(url, timeout=timeout, stream=True, allow_redirects=True) as resp:
            ctype = (resp.headers.get("content-type") or "").lower()
            if resp.status_code >= 400:
                return False, f"http_{resp.status_code}"
            total = 0
            with tmp.open("wb") as handle:
                for chunk in resp.iter_content(chunk_size=256 * 1024):
                    if not chunk:
                        continue
                    total += len(chunk)
                    if total > 100 * 1024 * 1024:
                        return False, "too_large"
                    handle.write(chunk)
            ok, why = is_valid_pdf(tmp, expected_title=expected_title)
            if not ok:
                return False, f"{why}:content_type={ctype}"
            tmp.replace(out_path)
            return True, f"downloaded:{total}"
    except Exception as exc:
        return False, f"error:{type(exc).__name__}:{exc}"
    finally:
        try:
            tmp.unlink(missing_ok=True)
        except Exception:
            pass
        try:
            import os

            os.close(fd)
        except Exception:
            pass


def arxiv_search(title: str, *, delay: float, timeout: int) -> tuple[Candidate | None, str]:
    global last_arxiv_request
    with arxiv_lock:
        wait = last_arxiv_request + delay - time.time()
        if wait > 0:
            time.sleep(wait)
        last_arxiv_request = time.time()
        query = 'ti:"' + title.replace('"', "") + '"'
        url = "https://export.arxiv.org/api/query?" + urlencode({"search_query": query, "start": 0, "max_results": 5})
        try:
            resp = requests.get(url, timeout=timeout, headers={"User-Agent": "BITE SIG PDF resolver/1.0"})
        except Exception as exc:
            return None, f"arxiv_error:{type(exc).__name__}:{exc}"
    if resp.status_code >= 400:
        return None, f"arxiv_http_{resp.status_code}"
    try:
        root = ET.fromstring(resp.content)
    except Exception as exc:
        return None, f"arxiv_xml_error:{type(exc).__name__}:{exc}"
    ns = {"a": "http://www.w3.org/2005/Atom"}
    best: tuple[float, str, str] = (0.0, "", "")
    for entry in root.findall("a:entry", ns):
        found_title = re.sub(r"\s+", " ", entry.findtext("a:title", default="", namespaces=ns)).strip()
        found_id = entry.findtext("a:id", default="", namespaces=ns).strip()
        score = max(title_similarity(title, found_title), token_overlap(title, found_title))
        if score > best[0]:
            best = (score, found_title, found_id)
    if best[0] >= 0.86 and best[2]:
        return Candidate(arxiv_pdf(best[2]), f"arxiv:title_search:{best[0]:.2f}", direct=True), "arxiv_match"
    return None, f"arxiv_no_match:{best[0]:.2f}:{best[1][:120]}"


def crossref_doi(title: str, *, delay: float, timeout: int) -> tuple[str, str]:
    global last_crossref_request
    url = "https://api.crossref.org/works?" + urlencode({"query.title": title, "rows": 3})
    with crossref_lock:
        wait = last_crossref_request + delay - time.time()
        if wait > 0:
            time.sleep(wait)
        last_crossref_request = time.time()
        try:
            resp = session().get(url, timeout=timeout, headers={"User-Agent": "BITE paper resolver (mailto:local@example.com)"})
        except Exception as exc:
            return "", f"crossref_error:{type(exc).__name__}:{exc}"
    if resp.status_code >= 400:
        return "", f"crossref_http_{resp.status_code}"
    try:
        items = resp.json().get("message", {}).get("items", [])
    except Exception as exc:
        return "", f"crossref_json_error:{type(exc).__name__}:{exc}"
    best: tuple[float, str, str] = (0.0, "", "")
    for item in items:
        found_title = " ".join(item.get("title") or [])
        doi = item.get("DOI") or ""
        score = max(title_similarity(title, found_title), token_overlap(title, found_title))
        if score > best[0]:
            best = (score, doi, found_title)
    if best[0] >= 0.90 and best[1]:
        return best[1], f"crossref_match:{best[0]:.2f}"
    return "", f"crossref_no_match:{best[0]:.2f}:{best[2][:120]}"


def process_row(index: int, row: dict[str, str], args: argparse.Namespace) -> dict[str, object]:
    title = row["paper_title"]
    out_path = target_path(row)
    existing = resolve_path(row.get("pdf_path", "")) or out_path
    ok, why = is_valid_pdf(existing, expected_title=title)
    if ok:
        return {"index": index, "ok": True, "title": title, "venue": row["venue"], "pdf_path": rel(existing), "source": "existing", "note": why}

    attempts: list[dict[str, str]] = []
    acm_dois: list[str] = []
    candidates = row_link_candidates(row)

    for candidate in list(candidates):
        if candidate.direct:
            ok, note = download_pdf(candidate.url, out_path, timeout=args.timeout, expected_title=title)
            attempts.append({"url": candidate.url, "source": candidate.source, "result": note})
            if ok:
                return {"index": index, "ok": True, "title": title, "venue": row["venue"], "pdf_path": rel(out_path), "source": candidate.source, "url": candidate.url, "attempts": attempts}
        extracted, dois, note = fetch_landing(candidate.url, timeout=args.timeout)
        attempts.append({"url": candidate.url, "source": candidate.source, "result": f"landing:{note}", "extracted": str(len(extracted)), "dois": ",".join(dois[:3])})
        acm_dois.extend(doi for doi in dois if doi.startswith("10.1145/"))
        for pdf_candidate in extracted[:8]:
            ok, pdf_note = download_pdf(pdf_candidate.url, out_path, timeout=args.timeout, expected_title=title)
            attempts.append({"url": pdf_candidate.url, "source": pdf_candidate.source, "result": pdf_note})
            if ok:
                return {"index": index, "ok": True, "title": title, "venue": row["venue"], "pdf_path": rel(out_path), "source": pdf_candidate.source, "url": pdf_candidate.url, "attempts": attempts}

    acm_dois = sorted(set(acm_dois))
    if acm_dois:
        return {"index": index, "ok": False, "title": title, "venue": row["venue"], "note": "acm_doi_queue", "acm_dois": acm_dois, "attempts": attempts}

    arxiv_candidate, arxiv_note = arxiv_search(title, delay=args.arxiv_delay, timeout=args.timeout)
    attempts.append({"url": "", "source": "arxiv:title_search", "result": arxiv_note})
    if arxiv_candidate:
        ok, note = download_pdf(arxiv_candidate.url, out_path, timeout=args.timeout, expected_title=title)
        attempts.append({"url": arxiv_candidate.url, "source": arxiv_candidate.source, "result": note})
        if ok:
            return {"index": index, "ok": True, "title": title, "venue": row["venue"], "pdf_path": rel(out_path), "source": arxiv_candidate.source, "url": arxiv_candidate.url, "attempts": attempts}

    if not args.skip_crossref:
        doi, crossref_note = crossref_doi(title, delay=args.crossref_delay, timeout=args.timeout)
        attempts.append({"url": "", "source": "crossref:title_search", "result": crossref_note})
        if doi.startswith("10.1145/"):
            acm_dois.append(doi)
    else:
        attempts.append({"url": "", "source": "crossref:title_search", "result": "crossref_skipped"})

    acm_dois = sorted(set(acm_dois))
    if acm_dois:
        return {"index": index, "ok": False, "title": title, "venue": row["venue"], "note": "acm_doi_queue", "acm_dois": acm_dois, "attempts": attempts}
    return {"index": index, "ok": False, "title": title, "venue": row["venue"], "note": attempts[-1]["result"] if attempts else "no_candidates", "attempts": attempts}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--arxiv-delay", type=float, default=1.0)
    parser.add_argument("--crossref-delay", type=float, default=1.5)
    parser.add_argument("--skip-crossref", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows = read_rows()
    tasks = [
        (index, row)
        for index, row in enumerate(rows)
        if (row.get("state") or "").strip() == "Wait" and "SIGGRAPH" in (row.get("venue") or "")
    ]
    if args.limit:
        tasks = tasks[: args.limit]
    print(json.dumps({"event": "planned", "tasks": len(tasks), "jobs": args.jobs, "dry_run": args.dry_run}, ensure_ascii=False), flush=True)
    if args.dry_run:
        for _, row in tasks[:20]:
            print(json.dumps({"venue": row["venue"], "title": row["paper_title"], "links": [item.__dict__ for item in row_link_candidates(row)]}, ensure_ascii=False))
        return

    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        future_map = {executor.submit(process_row, index, row, args): index for index, row in tasks}
        for done, future in enumerate(as_completed(future_map), 1):
            result = future.result()
            results.append(result)
            if result.get("ok"):
                row = rows[int(result["index"])]
                row["state"] = "Downloaded"
                row["pdf_path"] = str(result["pdf_path"])
            if done % 10 == 0 or result.get("ok"):
                print(
                    json.dumps(
                        {
                            "event": "progress",
                            "done": done,
                            "total": len(tasks),
                            "ok": sum(1 for item in results if item.get("ok")),
                            "acm_queue": sum(1 for item in results if item.get("note") == "acm_doi_queue"),
                            "last_ok": bool(result.get("ok")),
                            "title": str(result.get("title", ""))[:100],
                            "note": result.get("note", ""),
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )

    updated = sum(1 for item in results if item.get("ok"))
    backup = write_rows(rows) if updated else None
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_path = REPORT_DIR / f"sig_wait_resolve_report_{timestamp}.json"
    acm_queue_path = REPORT_DIR / f"sig_wait_acm_doi_queue_{timestamp}.csv"
    failures_path = REPORT_DIR / f"sig_wait_unresolved_{timestamp}.csv"

    with acm_queue_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["paper_list_line", "venue", "paper_title", "doi", "pdf_url", "target_pdf_path", "source_note"])
        writer.writeheader()
        for item in results:
            for doi in item.get("acm_dois", []) or []:
                writer.writerow(
                    {
                        "paper_list_line": int(item["index"]) + 2,
                        "venue": item.get("venue", ""),
                        "paper_title": item.get("title", ""),
                        "doi": doi,
                        "pdf_url": f"https://dl.acm.org/doi/pdf/{doi}",
                        "target_pdf_path": rel(target_path(rows[int(item["index"])])),
                        "source_note": item.get("note", ""),
                    }
                )
    with failures_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["paper_list_line", "venue", "paper_title", "note", "attempts"])
        writer.writeheader()
        for item in results:
            if item.get("ok") or item.get("note") == "acm_doi_queue":
                continue
            writer.writerow(
                {
                    "paper_list_line": int(item["index"]) + 2,
                    "venue": item.get("venue", ""),
                    "paper_title": item.get("title", ""),
                    "note": item.get("note", ""),
                    "attempts": json.dumps(item.get("attempts", []), ensure_ascii=False),
                }
            )
    report_path.write_text(
        json.dumps(
            {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "planned": len(tasks),
                "downloaded": updated,
                "paper_list_backup": rel(backup) if backup else "",
                "counts": dict(Counter("ok" if item.get("ok") else str(item.get("note") or "failed") for item in results)),
                "report": rel(report_path),
                "acm_queue": rel(acm_queue_path),
                "failures": rel(failures_path),
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
                "planned": len(tasks),
                "downloaded": updated,
                "paper_list_backup": rel(backup) if backup else "",
                "report": rel(report_path),
                "acm_queue": rel(acm_queue_path),
                "failures": rel(failures_path),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
