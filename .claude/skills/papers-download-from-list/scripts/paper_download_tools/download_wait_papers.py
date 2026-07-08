#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Iterable, Optional

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None  # type: ignore[assignment]


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[4]
DEFAULT_SOURCE = REPO_ROOT / "obsidian-vault/paper_list.csv"
DEFAULT_OUT_ROOT = REPO_ROOT / "obsidian-vault/paperPDFs"
LOG_HEADER = [
    "state",
    "importance",
    "paper_title",
    "venue",
    "project_link_or_github_link",
    "paper_link",
    "sort",
    "pdf_path",
]
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


def sanitize_filename(text: str, max_len: int = 180) -> str:
    text = (text or "").strip()
    text = text.replace("&", " and ")
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" ", "_").replace("-", "_")
    text = re.sub(r"[<>:\"/\\|?*\x00-\x1F,]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_. ")
    return (text or "Untitled")[:max_len].rstrip("_")


def venue_slug(venue: str) -> str:
    venue = (venue or "").strip() or "Unknown"
    return sanitize_filename(venue)


def extract_year(venue: str) -> str:
    years = re.findall(r"(?:19|20)\d{2}", venue or "")
    return years[-1] if years else ""


def infer_pdf_url(link: str) -> str:
    link = (link or "").strip()
    if not link:
        return ""

    parsed = urllib.parse.urlsplit(link)
    host = parsed.netloc.lower()
    path = parsed.path

    if host == "arxiv.org":
        m = re.search(r"/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", path)
        if m:
            return f"https://arxiv.org/pdf/{m.group(1)}.pdf"

    if host.endswith("openreview.net"):
        query = urllib.parse.parse_qs(parsed.query)
        paper_id = (query.get("id") or [""])[0]
        if paper_id:
            return urllib.parse.urlunsplit((parsed.scheme or "https", parsed.netloc, "/pdf", f"id={paper_id}", ""))

    if path.lower().endswith(".pdf"):
        return link

    return ""


def target_pdf_path(row: list[str], out_root: Path) -> Path:
    padded = (row + [""] * len(LOG_HEADER))[: len(LOG_HEADER)]
    _, _, title, venue, _, _, _, pdf_path = padded
    if pdf_path.strip():
        path = Path(pdf_path.strip())
        return path if path.is_absolute() else REPO_ROOT / path

    year = extract_year(venue)
    prefix = f"{year}_" if year else ""
    return out_root / venue_slug(venue) / f"{prefix}{sanitize_filename(title)}.pdf"


def is_readable_pdf(path: Path) -> bool:
    try:
        if not path.is_file() or path.stat().st_size < 5000:
            return False
        with path.open("rb") as f:
            if f.read(4) != b"%PDF":
                return False
        if PdfReader is not None:
            reader = PdfReader(str(path))
            return len(reader.pages) > 0
        return True
    except Exception:
        return False


def download_pdf(url: str, dest: Path, timeout: int) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    if not is_readable_pdf(dest):
        dest.unlink(missing_ok=True)
        raise RuntimeError(f"downloaded file is not a readable PDF: {url}")


def load_rows(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return [row for row in csv.reader(f)]


def save_rows(path: Path, rows: Iterable[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow((row + [""] * len(LOG_HEADER))[: len(LOG_HEADER)])


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Download state=Wait papers from obsidian-vault/paper_list.csv.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="CSV queue path. Defaults to obsidian-vault/paper_list.csv.")
    parser.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT), help="PDF output root. Defaults to obsidian-vault/paperPDFs.")
    parser.add_argument("--limit", type=int, default=0, help="Maximum Wait rows to process. 0 means no limit.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned downloads without writing files or CSV updates.")
    parser.add_argument("--timeout", type=int, default=180, help="Download timeout in seconds.")
    args = parser.parse_args(argv)

    source = Path(args.source).expanduser()
    if not source.is_absolute():
        source = REPO_ROOT / source
    out_root = Path(args.out_root).expanduser()
    if not out_root.is_absolute():
        out_root = REPO_ROOT / out_root

    rows = load_rows(source)
    if not rows:
        print("[WARN] empty source CSV")
        return 0
    if rows[0][: len(LOG_HEADER)] != LOG_HEADER:
        raise SystemExit(f"Unexpected header in {source}: {rows[0]}")

    processed = 0
    downloaded = 0
    skipped = 0
    failed = 0

    for idx in range(1, len(rows)):
        row = (rows[idx] + [""] * len(LOG_HEADER))[: len(LOG_HEADER)]
        state, _, title, _, _, paper_link, _, _ = row
        if state.strip() != "Wait":
            rows[idx] = row
            continue
        if args.limit and processed >= args.limit:
            rows[idx] = row
            continue

        processed += 1
        dest = target_pdf_path(row, out_root)
        pdf_url = infer_pdf_url(paper_link)
        if not pdf_url:
            print(f"[SKIP] no supported PDF link for row {idx + 1}: {title}")
            skipped += 1
            rows[idx] = row
            continue

        if dest.is_file() and is_readable_pdf(dest):
            row[0] = "Downloaded"
            row[7] = repo_relative(dest)
            downloaded += 1
            print(f"[OK] already present: {row[7]}")
            rows[idx] = row
            continue

        print(f"[DOWNLOAD] {title}")
        print(f"  {pdf_url}")
        print(f"  -> {repo_relative(dest)}")
        if args.dry_run:
            rows[idx] = row
            continue
        try:
            download_pdf(pdf_url, dest, timeout=args.timeout)
        except Exception as exc:
            print(f"[ERROR] row {idx + 1}: {exc}")
            failed += 1
            rows[idx] = row
            continue

        row[0] = "Downloaded"
        row[7] = repo_relative(dest)
        downloaded += 1
        rows[idx] = row

    if not args.dry_run:
        save_rows(source, rows)

    print(f"Summary: processed={processed}, downloaded={downloaded}, skipped={skipped}, failed={failed}, dry_run={args.dry_run}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
