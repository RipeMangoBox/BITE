#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import tempfile
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import parse_qs, quote, urljoin, urlparse, urlunparse

import fitz
import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[2]
RUN_DIR = ROOT / "paperSources" / "siggraph_full_collect_20260624"
PAPER_LIST = ROOT / "obsidian-vault" / "paper_list.csv"
PDF_ROOT = ROOT / "obsidian-vault" / "paperPDFs"
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
TARGET_VENUES = {
    "SIGGRAPH 2022",
    "SIGGRAPH 2023",
    "SIGGRAPH 2024",
    "SIGGRAPH ASIA 2022",
    "SIGGRAPH ASIA 2023",
    "SIGGRAPH ASIA 2024",
}

BAD_PDF_HINTS = (
    "supplement",
    "supp",
    "slides",
    "presentation",
    "poster",
    "video",
    "dataset",
    "data.zip",
    "appendix",
)


@dataclass(frozen=True)
class Candidate:
    url: str
    source: str
    direct: bool = False


def norm_title(text: str) -> str:
    text = re.sub(r"\$([^$]+)\$", r"\1", text or "")
    text = text.replace("–", "-").replace("—", "-").replace("’", "'")
    text = text.replace("‐", "-").replace("‑", "-")
    text = re.sub(r"[^0-9a-zA-Z]+", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def title_similarity(left: str, right: str) -> float:
    left_key = norm_title(left)
    right_key = norm_title(right)
    if not left_key or not right_key:
        return 0.0
    return SequenceMatcher(None, left_key, right_key).ratio()


def title_tokens_contained(expected: str, observed: str) -> bool:
    expected_tokens = set(norm_title(expected).split())
    observed_tokens = set(norm_title(observed).split())
    if not expected_tokens or not observed_tokens:
        return False
    return len(expected_tokens & observed_tokens) / max(1, len(expected_tokens)) >= 0.72


def pdf_title_candidates(path: Path) -> list[str]:
    candidates: list[str] = []
    try:
        with fitz.open(path) as doc:
            metadata_title = (doc.metadata or {}).get("title") or ""
            if metadata_title.strip():
                candidates.append(metadata_title.strip())
            if doc.page_count:
                text = doc.load_page(0).get_text("text") or ""
                full_page = re.sub(r"\s+", " ", text).strip()
                if full_page:
                    candidates.append(full_page[:3000])
                added = 0
                for raw_line in text.splitlines()[:40]:
                    line = re.sub(r"\s+", " ", raw_line).strip()
                    if len(line) >= 12 and re.search(r"[A-Za-z]", line):
                        candidates.append(line)
                        added += 1
                        if added >= 8:
                            break
    except Exception:
        return candidates
    out: list[str] = []
    seen: set[str] = set()
    for item in candidates:
        key = norm_title(item)
        if key and key not in seen:
            seen.add(key)
            out.append(item)
    return out


def pdf_title_matches(path: Path, expected_title: str) -> tuple[bool, str]:
    candidates = pdf_title_candidates(path)
    if not candidates:
        return True, "title_unchecked"
    scored = [(candidate, title_similarity(expected_title, candidate), title_tokens_contained(expected_title, candidate)) for candidate in candidates]
    if any(score >= 0.62 or contained for _, score, contained in scored):
        return True, "title_match"
    return False, "title_mismatch:" + " | ".join(candidate for candidate, _, _ in scored[:3])


def safe_slug(text: str, max_len: int = 180) -> str:
    text = re.sub(r"[^0-9A-Za-z]+", "_", text or "").strip("_")
    text = re.sub(r"_+", "_", text)
    return text[:max_len].rstrip("_") or "paper"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_record_links() -> dict[tuple[str, str], dict[str, object]]:
    path = RUN_DIR / "collected_records.jsonl"
    if not path.exists():
        return {}
    out: dict[tuple[str, str], dict[str, object]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        out[(str(rec.get("venue") or ""), norm_title(str(rec.get("paper_title") or "")))] = rec
    return out


def read_rows() -> list[dict[str, str]]:
    with PAPER_LIST.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CSV_FIELDS:
            raise SystemExit(f"Unexpected paper_list header: {reader.fieldnames}")
        return [dict(row) for row in reader]


def write_rows(rows: list[dict[str, str]]) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = PAPER_LIST.with_name(f"{PAPER_LIST.name}.bak_{timestamp}")
    shutil.copy2(PAPER_LIST, backup)
    tmp = PAPER_LIST.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(PAPER_LIST)
    return backup


def resolve_pdf_path(raw: str) -> Path | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute():
        path = ROOT / path
    return path


def is_valid_pdf(path: Path, *, expected_title: str = "") -> tuple[bool, str]:
    if not path.exists() or not path.is_file():
        return False, "missing"
    try:
        with path.open("rb") as handle:
            head = handle.read(8)
        if not head.startswith(b"%PDF"):
            return False, "not_pdf_magic"
        with fitz.open(path) as doc:
            if doc.page_count < 1:
                return False, "zero_pages"
    except Exception as exc:
        return False, f"pdf_invalid:{exc}"
    if expected_title:
        ok, why = pdf_title_matches(path, expected_title)
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
    arxiv_id = match.group(1)
    return f"https://arxiv.org/pdf/{arxiv_id}.pdf"


def google_drive_download(url: str) -> str:
    parsed = urlparse(url)
    if "drive.google.com" not in parsed.netloc.lower():
        return url
    match = re.search(r"/file/d/([^/]+)", parsed.path)
    if match:
        return f"https://drive.google.com/uc?export=download&id={match.group(1)}"
    qs = parse_qs(parsed.query)
    if "id" in qs:
        return f"https://drive.google.com/uc?export=download&id={qs['id'][0]}"
    return url


def github_raw(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc.lower() != "github.com":
        return url
    parts = parsed.path.strip("/").split("/")
    if len(parts) >= 5 and parts[2] == "blob":
        user, repo, _, branch = parts[:4]
        rest = "/".join(parts[4:])
        return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{rest}"
    return url


def normalize_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    url = url.replace(" ", "%20")
    url = arxiv_pdf(url)
    url = google_drive_download(url)
    url = github_raw(url)
    parsed = urlparse(url)
    if "dropbox.com" in parsed.netloc.lower():
        query = parse_qs(parsed.query)
        query["dl"] = ["1"]
        flat = "&".join(f"{quote(k)}={quote(v[0])}" for k, v in query.items())
        url = urlunparse(parsed._replace(query=flat))
    return url


def skip_url_reason(url: str) -> str:
    u = url.lower()
    if not u:
        return "empty_url"
    if "doi.org/10.1145" in u or "dl.acm.org/doi" in u:
        return "acm_doi_not_open_pdf"
    if any(hint in u for hint in ("youtube.com", "youtu.be", "vimeo.com")):
        return "video_url"
    if u.endswith((".zip", ".tar", ".gz", ".mp4", ".mov")):
        return "non_pdf_asset"
    return ""


def is_direct_pdfish(url: str) -> bool:
    u = url.lower()
    return (
        "arxiv.org/pdf/" in u
        or "openreview.net/pdf" in u
        or u.endswith(".pdf")
        or ".pdf?" in u
        or "/pdf/" in u
        or "export=download" in u
    )


def candidate_score(candidate: Candidate) -> int:
    u = candidate.url.lower()
    score = 30
    if "arxiv.org/pdf/" in u:
        score += 100
    if candidate.source.startswith("meta"):
        score += 70
    if is_direct_pdfish(u):
        score += 50
    if any(word in u for word in ("paper", "preprint", "main")):
        score += 15
    if any(hint in u for hint in BAD_PDF_HINTS):
        score -= 50
    return score


def unique_candidates(items: list[Candidate]) -> list[Candidate]:
    seen: set[str] = set()
    out: list[Candidate] = []
    for item in sorted(items, key=candidate_score, reverse=True):
        url = normalize_url(item.url)
        if not url or url in seen:
            continue
        seen.add(url)
        out.append(Candidate(url=url, source=item.source, direct=item.direct or is_direct_pdfish(url)))
    return out


def links_for_row(row: dict[str, str], rec: dict[str, object] | None) -> list[Candidate]:
    candidates: list[Candidate] = []
    for key in ("paper_link", "project_link_or_github_link"):
        value = (row.get(key) or "").strip()
        if value:
            candidates.append(Candidate(value, f"csv:{key}", direct=is_direct_pdfish(value)))
    if rec:
        for key in ("paper_link", "paper_copilot_url", "doi", "project_link_or_github_link"):
            value = str(rec.get(key) or "").strip()
            if value:
                candidates.append(Candidate(value, f"record:{key}", direct=is_direct_pdfish(value)))
        kesen = rec.get("kesen") if isinstance(rec.get("kesen"), dict) else {}
        for key in ("paper_links", "project_links"):
            for value in kesen.get(key, []) or []:
                candidates.append(Candidate(str(value), f"kesen:{key}", direct=is_direct_pdfish(str(value))))
    return unique_candidates(candidates)


def extract_pdf_candidates(html: str, base_url: str) -> list[Candidate]:
    soup = BeautifulSoup(html, "html.parser")
    candidates: list[Candidate] = []
    meta_names = {"citation_pdf_url", "dc.identifier", "eprints.document_url"}
    for meta in soup.find_all("meta"):
        name = (meta.get("name") or meta.get("property") or "").strip().lower()
        content = (meta.get("content") or "").strip()
        if content and (name in meta_names or "pdf" in name):
            candidates.append(Candidate(urljoin(base_url, content), f"meta:{name}", direct=True))
    for a in soup.find_all("a"):
        href = (a.get("href") or "").strip()
        if not href:
            continue
        text = a.get_text(" ", strip=True).lower()
        joined = urljoin(base_url, href)
        low = joined.lower()
        if (
            ".pdf" in low
            or "arxiv.org/abs/" in low
            or "arxiv.org/pdf/" in low
            or "openreview.net/pdf" in low
            or "download" in low and "pdf" in (low + " " + text)
        ):
            candidates.append(Candidate(joined, "html:a", direct=is_direct_pdfish(joined)))
    for raw in re.findall(r"https?://[^\"'<>\\s]+", html):
        raw = raw.rstrip(").,;")
        low = raw.lower()
        if ".pdf" in low or "arxiv.org/abs/" in low or "arxiv.org/pdf/" in low:
            candidates.append(Candidate(raw, "html:raw", direct=is_direct_pdfish(raw)))
    return unique_candidates(candidates)


thread_local = threading.local()


def session() -> requests.Session:
    sess = getattr(thread_local, "session", None)
    if sess is None:
        sess = requests.Session()
        sess.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) BITE/1.0",
            "Accept": "text/html,application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })
        thread_local.session = sess
    return sess


def download_pdf(url: str, out_path: Path, *, timeout: int, expected_title: str = "") -> tuple[bool, str]:
    reason = skip_url_reason(url)
    if reason and reason != "acm_doi_not_open_pdf":
        return False, reason
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_name = tempfile.mkstemp(prefix=out_path.name + ".", suffix=".part", dir=str(out_path.parent))
    Path(tmp_name).unlink(missing_ok=True)
    tmp_path = Path(tmp_name)
    try:
        with session().get(url, timeout=timeout, stream=True, allow_redirects=True) as resp:
            content_type = (resp.headers.get("Content-Type") or "").lower()
            if resp.status_code >= 400:
                return False, f"http_{resp.status_code}"
            with tmp_path.open("wb") as handle:
                total = 0
                for chunk in resp.iter_content(chunk_size=1024 * 256):
                    if not chunk:
                        continue
                    total += len(chunk)
                    if total > 80 * 1024 * 1024:
                        return False, "too_large"
                    handle.write(chunk)
            if "pdf" not in content_type:
                ok, why = is_valid_pdf(tmp_path, expected_title=expected_title)
                if not ok:
                    return False, f"not_pdf:{content_type or why}"
            ok, why = is_valid_pdf(tmp_path, expected_title=expected_title)
            if not ok:
                return False, why
            tmp_path.replace(out_path)
            return True, "downloaded"
    except Exception as exc:
        return False, f"error:{type(exc).__name__}:{exc}"
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except Exception:
            pass
        try:
            import os

            os.close(tmp_fd)
        except Exception:
            pass


def fetch_landing(url: str, *, timeout: int) -> tuple[list[Candidate], str]:
    reason = skip_url_reason(url)
    if reason:
        return [], reason
    try:
        resp = session().get(url, timeout=timeout, allow_redirects=True)
        content_type = (resp.headers.get("Content-Type") or "").lower()
        if resp.status_code >= 400:
            return [], f"http_{resp.status_code}"
        if "pdf" in content_type or resp.content[:8].startswith(b"%PDF"):
            return [Candidate(resp.url, "landing:response_pdf", direct=True)], "response_pdf"
        if "text/html" not in content_type and "application/xhtml" not in content_type and "<html" not in resp.text[:500].lower():
            return [], f"not_html:{content_type}"
        return extract_pdf_candidates(resp.text, resp.url), "html"
    except Exception as exc:
        return [], f"error:{type(exc).__name__}:{exc}"


def process_row(index: int, row: dict[str, str], rec: dict[str, object] | None, *, timeout: int) -> dict[str, object]:
    title = row["paper_title"]
    venue = row["venue"]
    out_path = PDF_ROOT / venue.replace(" ", "_") / f"{safe_slug(title)}.pdf"
    if out_path.exists():
        ok, why = is_valid_pdf(out_path, expected_title=title)
        if ok:
            return {"index": index, "ok": True, "title": title, "venue": venue, "pdf_path": rel(out_path), "source": "existing_target", "note": why}

    attempts: list[dict[str, str]] = []
    for candidate in links_for_row(row, rec):
        reason = skip_url_reason(candidate.url)
        if reason:
            attempts.append({"url": candidate.url, "source": candidate.source, "result": reason})
            continue
        if candidate.direct:
            ok, note = download_pdf(candidate.url, out_path, timeout=timeout, expected_title=title)
            attempts.append({"url": candidate.url, "source": candidate.source, "result": note})
            if ok:
                return {"index": index, "ok": True, "title": title, "venue": venue, "pdf_path": rel(out_path), "source": candidate.source, "url": candidate.url, "attempts": attempts}
            continue
        extracted, note = fetch_landing(candidate.url, timeout=timeout)
        attempts.append({"url": candidate.url, "source": candidate.source, "result": f"landing:{note}", "extracted": str(len(extracted))})
        for pdf_candidate in extracted[:8]:
            reason = skip_url_reason(pdf_candidate.url)
            if reason:
                attempts.append({"url": pdf_candidate.url, "source": pdf_candidate.source, "result": reason})
                continue
            ok, pdf_note = download_pdf(pdf_candidate.url, out_path, timeout=timeout, expected_title=title)
            attempts.append({"url": pdf_candidate.url, "source": pdf_candidate.source, "result": pdf_note})
            if ok:
                return {"index": index, "ok": True, "title": title, "venue": venue, "pdf_path": rel(out_path), "source": pdf_candidate.source, "url": pdf_candidate.url, "attempts": attempts}
    return {"index": index, "ok": False, "title": title, "venue": venue, "attempts": attempts, "note": attempts[-1]["result"] if attempts else "no_candidates"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows = read_rows()
    records = load_record_links()
    tasks: list[tuple[int, dict[str, str], dict[str, object] | None]] = []
    for index, row in enumerate(rows):
        if row.get("venue") not in TARGET_VENUES:
            continue
        existing = resolve_pdf_path(row.get("pdf_path", ""))
        if existing:
            ok, _ = is_valid_pdf(existing, expected_title=row.get("paper_title", ""))
            if ok:
                continue
        rec = records.get((row["venue"], norm_title(row["paper_title"])))
        tasks.append((index, row, rec))
    if args.limit:
        tasks = tasks[: args.limit]

    print(json.dumps({"event": "planned", "tasks": len(tasks), "dry_run": args.dry_run}, ensure_ascii=False))
    if args.dry_run:
        for _, row, rec in tasks[:20]:
            print(json.dumps({
                "title": row["paper_title"],
                "venue": row["venue"],
                "candidates": [c.__dict__ for c in links_for_row(row, rec)[:8]],
            }, ensure_ascii=False))
        return

    results: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        future_map = {
            executor.submit(process_row, index, row, rec, timeout=args.timeout): index
            for index, row, rec in tasks
        }
        for done, future in enumerate(as_completed(future_map), 1):
            result = future.result()
            results.append(result)
            if done % 25 == 0 or result.get("ok"):
                print(json.dumps({
                    "event": "progress",
                    "done": done,
                    "total": len(tasks),
                    "ok": sum(1 for x in results if x.get("ok")),
                    "last_ok": bool(result.get("ok")),
                    "title": str(result.get("title", ""))[:80],
                    "note": result.get("note", ""),
                }, ensure_ascii=False), flush=True)

    updated = 0
    for result in results:
        if not result.get("ok"):
            continue
        row = rows[int(result["index"])]
        row["pdf_path"] = str(result["pdf_path"])
        if row.get("state") != "checked":
            row["state"] = "Downloaded"
        updated += 1
    backup = write_rows(rows) if updated else ""

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_path = RUN_DIR / f"download_report_{timestamp}.json"
    failures_path = RUN_DIR / f"download_failures_{timestamp}.csv"
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "planned": len(tasks),
        "downloaded": updated,
        "paper_list_backup": rel(backup) if backup else "",
        "result_counts": dict(Counter("ok" if item.get("ok") else str(item.get("note") or "failed") for item in results)),
        "results": results,
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    with failures_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["venue", "paper_title", "note", "attempts"])
        writer.writeheader()
        for item in results:
            if item.get("ok"):
                continue
            writer.writerow({
                "venue": item.get("venue", ""),
                "paper_title": item.get("title", ""),
                "note": item.get("note", ""),
                "attempts": json.dumps(item.get("attempts", []), ensure_ascii=False),
            })
    print(json.dumps({
        "event": "complete",
        "planned": len(tasks),
        "downloaded": updated,
        "report": rel(report_path),
        "failures": rel(failures_path),
        "paper_list_backup": rel(backup) if backup else "",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
