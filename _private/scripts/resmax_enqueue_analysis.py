#!/usr/bin/env python3
"""Import downloaded resmax PDFs and enqueue the new analysis pipeline.

Reads `_private/resmax_downloads/manifest.jsonl`, selects completed PDFs,
uploads up to N papers through `/api/v1/import/pdf`, then enqueues each paper
through `/api/v1/pipeline/{paper_id}/run`.

Progress is persisted so the script is resumable.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests


def load_manifest(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def load_progress(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"items": {}, "updated_at": ""}
    return json.loads(path.read_text(encoding="utf-8"))


def save_progress(path: Path, payload: dict[str, Any]) -> None:
    payload["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def pick_done_records(
    manifest_rows: list[dict[str, Any]],
    progress: dict[str, Any],
    limit: int,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    items = progress.setdefault("items", {})
    for record in manifest_rows:
        if record.get("status") != "done":
            continue
        paper_id = record["paper_id"]
        state = items.get(paper_id, {})
        if state.get("pipeline_status") == "enqueued":
            continue
        if not Path(record["output_pdf"]).exists():
            continue
        selected.append(record)
        if len(selected) >= limit:
            break
    return selected


def import_pdf(session: requests.Session, base_url: str, pdf_path: Path, title: str, category: str) -> dict[str, Any]:
    url = f"{base_url.rstrip('/')}/api/v1/import/pdf?category={quote(category)}&is_ephemeral=false&title={quote(title)}"
    with pdf_path.open("rb") as handle:
        resp = session.post(url, files={"file": (pdf_path.name, handle, "application/pdf")}, timeout=300)
    resp.raise_for_status()
    return resp.json()


def enqueue_pipeline(session: requests.Session, base_url: str, paper_id: str) -> dict[str, Any]:
    url = f"{base_url.rstrip('/')}/api/v1/pipeline/{paper_id}/run"
    resp = session.post(url, timeout=120)
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="_private/resmax_downloads/manifest.jsonl")
    parser.add_argument("--progress", default="_private/resmax_downloads/analysis_progress.json")
    parser.add_argument("--base-url", required=True, help="ResearchFlow API base, e.g. http://127.0.0.1:8000")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--category", default="Resmax")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    progress_path = Path(args.progress)
    manifest_rows = load_manifest(manifest_path)
    progress = load_progress(progress_path)
    selected = pick_done_records(manifest_rows, progress, args.limit)

    session = requests.Session()
    session.trust_env = False
    for record in selected:
        paper_id = record["paper_id"]
        item = progress["items"].setdefault(paper_id, {})
        item["title"] = record.get("title", "")
        item["conf_year"] = record.get("conf_year", "")
        item["pdf_path"] = record.get("output_pdf", "")
        item["source_status"] = record.get("status", "")

        try:
            if not item.get("imported_paper_id"):
                imported = import_pdf(
                    session,
                    args.base_url,
                    Path(record["output_pdf"]),
                    record.get("title", ""),
                    f"{args.category}_{record.get('conf_year', 'Unknown')}",
                )
                item["import_response"] = imported
                item["imported_paper_id"] = imported["id"]
                item["import_status"] = "created"
                save_progress(progress_path, progress)

            if item.get("pipeline_status") != "enqueued":
                enq = enqueue_pipeline(session, args.base_url, item["imported_paper_id"])
                item["pipeline_response"] = enq
                item["pipeline_status"] = enq.get("status", "unknown")
                save_progress(progress_path, progress)
        except Exception as exc:  # noqa: BLE001
            item["error"] = f"{type(exc).__name__}:{str(exc)[:300]}"
            save_progress(progress_path, progress)


if __name__ == "__main__":
    main()
