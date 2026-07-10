#!/usr/bin/env python3
"""Resumable local PDF downloader for resmax conference slices.

Reads `_private/huggingface/resmax/accepted_index.csv`, filters rows by
`conf_year`, and downloads PDFs to a local directory while maintaining:

- `manifest.jsonl`: one record per paper with latest status
- `progress.json`: aggregate counters for quick inspection

Designed for large batches that must support stop/resume without redoing
completed downloads.
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import hashlib
import json
import random
import re
import time
from collections import Counter
from pathlib import Path
from typing import Any

import httpx


MIN_PDF_SIZE = 50 * 1024
DEFAULT_CONCURRENCY = 2
DEFAULT_TIMEOUT = 180
STATUS_DONE = "done"
STATUS_FAILED = "failed"
STATUS_PENDING = "pending"
STATUS_SKIPPED = "skipped"
MAX_RETRIES_PER_URL = 4


def slugify(text: str, limit: int = 180) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    text = re.sub(r"[^\w\s\-.]", "_", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"_+", "_", text).strip("._")
    return text[:limit] or "untitled"


def stable_suffix(row: dict[str, str]) -> str:
    raw = f"{row.get('paper_id', '')}::{row.get('title', '')}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def candidate_urls(row: dict[str, str]) -> list[str]:
    urls: list[str] = []
    arxiv_id = (row.get("arxiv_id") or "").strip()
    pdf_url = (row.get("pdf_url") or "").strip()
    forum_id = (row.get("openreview_forum_id") or "").strip()

    if arxiv_id:
        base_id = re.sub(r"v\d+$", "", arxiv_id)
        urls.append(f"https://arxiv.org/pdf/{base_id}.pdf")
    if pdf_url and "openreview.net" not in pdf_url and pdf_url not in urls:
        urls.append(pdf_url)
    if forum_id:
        or_url = f"https://openreview.net/pdf?id={forum_id}"
        if or_url not in urls:
            urls.append(or_url)
    if pdf_url and pdf_url not in urls:
        urls.append(pdf_url)
    return urls


def output_paths(root: Path, row: dict[str, str]) -> tuple[Path, Path]:
    conf_year = row["conf_year"]
    title_slug = slugify(row.get("title", ""), limit=80)
    suffix = stable_suffix(row)
    stem = f"{title_slug}__{suffix}"
    pdf_path = root / "pdfs" / conf_year / f"{stem}.pdf"
    meta_path = root / "meta" / conf_year / f"{stem}.json"
    return pdf_path, meta_path


def load_manifest(manifest_path: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    if not manifest_path.exists():
        return records
    with manifest_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            records[record["paper_id"]] = record
    return records


def write_manifest(manifest_path: Path, records: dict[str, dict[str, Any]]) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        json.dumps(records[key], ensure_ascii=False, sort_keys=True)
        for key in sorted(records.keys())
    ]
    manifest_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def write_progress(progress_path: Path, rows: list[dict[str, str]], records: dict[str, dict[str, Any]]) -> None:
    by_conf = Counter(row["conf_year"] for row in rows)
    paper_ids = {row["paper_id"] for row in rows}
    by_status = Counter(
        record.get("status", STATUS_PENDING)
        for pid, record in records.items()
        if pid in paper_ids
    )
    downloadable = sum(1 for row in rows if candidate_urls(row))
    payload = {
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_rows": len(rows),
        "downloadable_rows": downloadable,
        "by_conf_year": dict(sorted(by_conf.items())),
        "by_status": dict(sorted(by_status.items())),
        "done": by_status.get(STATUS_DONE, 0),
        "failed": by_status.get(STATUS_FAILED, 0),
        "pending": by_status.get(STATUS_PENDING, 0),
        "skipped": by_status.get(STATUS_SKIPPED, 0),
    }
    progress_path.parent.mkdir(parents=True, exist_ok=True)
    progress_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_rows(csv_path: Path, conf_years: set[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            conf_year = (row.get("conf_year") or "").strip()
            if conf_year not in conf_years:
                continue
            rows.append(row)
    return rows


async def fetch_pdf(
    client: httpx.AsyncClient,
    urls: list[str],
) -> tuple[bytes | None, str | None, str | None]:
    last_error: str | None = None
    for url in urls:
        for attempt in range(MAX_RETRIES_PER_URL):
            try:
                response = await client.get(url)
                if response.status_code == 429:
                    wait_s = min(20 * (attempt + 1), 120) + random.random() * 2
                    last_error = f"rate_limited:{url}"
                    await asyncio.sleep(wait_s)
                    continue
                response.raise_for_status()
                data = response.content
                if len(data) < MIN_PDF_SIZE:
                    last_error = f"too_small:{len(data)}:{url}"
                    break
                if not data.startswith(b"%PDF-"):
                    last_error = f"not_pdf:{url}"
                    break
                return data, url, None
            except Exception as exc:  # noqa: BLE001
                last_error = f"{type(exc).__name__}:{str(exc)[:160]}"
                if attempt < MAX_RETRIES_PER_URL - 1:
                    await asyncio.sleep(min(4 * (attempt + 1), 20) + random.random())
    return None, None, last_error


def ensure_seed_records(rows: list[dict[str, str]], records: dict[str, dict[str, Any]], output_root: Path) -> None:
    for row in rows:
        paper_id = row["paper_id"]
        pdf_path, meta_path = output_paths(output_root, row)
        existing = records.get(paper_id)
        if existing:
            old_pdf = Path(existing.get("output_pdf", ""))
            if existing.get("status") == STATUS_DONE and old_pdf.exists():
                continue
            existing["output_pdf"] = str(pdf_path)
            existing["output_meta"] = str(meta_path)
            if "candidate_urls" not in existing or not existing["candidate_urls"]:
                existing["candidate_urls"] = candidate_urls(row)
            if existing.get("status") in {"downloading", STATUS_FAILED}:
                existing["status"] = STATUS_PENDING
            continue
        urls = candidate_urls(row)
        status = STATUS_PENDING if urls else STATUS_SKIPPED
        error = "" if urls else "no_downloadable_url"
        records[paper_id] = {
            "paper_id": paper_id,
            "conf_year": row["conf_year"],
            "title": row.get("title", ""),
            "pdf_url": row.get("pdf_url", ""),
            "arxiv_id": row.get("arxiv_id", ""),
            "openreview_forum_id": row.get("openreview_forum_id", ""),
            "output_pdf": str(pdf_path),
            "output_meta": str(meta_path),
            "candidate_urls": urls,
            "status": status,
            "error": error,
            "size_bytes": 0,
            "sha256": "",
            "downloaded_url": "",
            "updated_at": "",
        }


async def download_all(
    rows: list[dict[str, str]],
    records: dict[str, dict[str, Any]],
    output_root: Path,
    manifest_path: Path,
    progress_path: Path,
    concurrency: int,
    limit: int,
) -> None:
    todo: list[dict[str, str]] = []
    for row in rows:
        record = records[row["paper_id"]]
        if record["status"] == STATUS_DONE and Path(record["output_pdf"]).exists():
            continue
        if record["status"] == STATUS_SKIPPED:
            continue
        todo.append(row)

    if limit > 0:
        todo = todo[:limit]

    sem = asyncio.Semaphore(concurrency)

    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=DEFAULT_TIMEOUT,
        headers={"User-Agent": "ResearchFlow-ResmaxDownloader/1.0"},
        trust_env=False,
    ) as client:
        async def run_one(row: dict[str, str]) -> None:
            paper_id = row["paper_id"]
            record = records[paper_id]
            pdf_path = Path(record["output_pdf"])
            meta_path = Path(record["output_meta"])
            urls = record["candidate_urls"]

            async with sem:
                record["status"] = "downloading"
                record["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                write_manifest(manifest_path, records)
                write_progress(progress_path, rows, records)

                data, used_url, error = await fetch_pdf(client, urls)
                if not data:
                    record["status"] = STATUS_FAILED
                    record["error"] = error or "unknown_error"
                    record["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    write_manifest(manifest_path, records)
                    write_progress(progress_path, rows, records)
                    return

                pdf_path.parent.mkdir(parents=True, exist_ok=True)
                meta_path.parent.mkdir(parents=True, exist_ok=True)
                tmp_path = pdf_path.with_suffix(".pdf.part")
                tmp_path.write_bytes(data)
                tmp_path.replace(pdf_path)

                checksum = hashlib.sha256(data).hexdigest()
                record["status"] = STATUS_DONE
                record["error"] = ""
                record["size_bytes"] = len(data)
                record["sha256"] = checksum
                record["downloaded_url"] = used_url or ""
                record["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

                meta_payload = {
                    "paper_id": paper_id,
                    "title": row.get("title", ""),
                    "conf_year": row.get("conf_year", ""),
                    "downloaded_url": used_url,
                    "sha256": checksum,
                    "size_bytes": len(data),
                    "candidate_urls": urls,
                }
                meta_path.write_text(
                    json.dumps(meta_payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                write_manifest(manifest_path, records)
                write_progress(progress_path, rows, records)

        await asyncio.gather(*(run_one(row) for row in todo))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv",
        default="_private/huggingface/resmax/accepted_index.csv",
    )
    parser.add_argument(
        "--conf-year",
        action="append",
        dest="conf_years",
        default=[],
        help="Repeatable, e.g. --conf-year NeurIPS_2025 --conf-year ICLR_2026",
    )
    parser.add_argument(
        "--output-root",
        default="_private/resmax_downloads",
    )
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()

    conf_years = set(args.conf_years or ["NeurIPS_2025", "ICLR_2026"])
    csv_path = Path(args.csv)
    output_root = Path(args.output_root)
    manifest_path = output_root / "manifest.jsonl"
    progress_path = output_root / "progress.json"

    rows = load_rows(csv_path, conf_years)
    records = load_manifest(manifest_path)
    ensure_seed_records(rows, records, output_root)
    write_manifest(manifest_path, records)
    write_progress(progress_path, rows, records)

    if args.prepare_only:
        return

    asyncio.run(
        download_all(
            rows=rows,
            records=records,
            output_root=output_root,
            manifest_path=manifest_path,
            progress_path=progress_path,
            concurrency=args.concurrency,
            limit=args.limit,
        )
    )


if __name__ == "__main__":
    main()
