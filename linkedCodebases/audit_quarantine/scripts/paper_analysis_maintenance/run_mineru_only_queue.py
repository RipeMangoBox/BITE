#!/usr/bin/env python3
"""Run MinerU parse only for a queue of PDFs.

This intentionally does not run LLM analysis and does not write analysis notes.
It produces per-paper parse artifacts under an output root so later repair or
full analysis can reuse the MinerU evidence.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_private" / "mineru_only_runs"
DEFAULT_REPORT_ROOT = REPO_ROOT / "artifacts" / "figure_caption_rebuild_batches"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import run_local_paper_analysis as runner  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue-csv", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--report-root", default=str(DEFAULT_REPORT_ROOT))
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--mineru-bin", default=runner.DEFAULT_MINERU_BIN)
    parser.add_argument("--mineru-backend", default="pipeline")
    parser.add_argument("--mineru-timeout", type=int, default=1800)
    parser.add_argument("--mineru-model-source", choices=["local", "huggingface", "modelscope"], default="local")
    parser.add_argument("--mineru-config", default=str(runner.DEFAULT_MINERU_CONFIG))
    parser.add_argument("--mineru-pipeline-cache", default=str(runner.MINERU_PIPELINE_CACHE))
    return parser.parse_args()


def now_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_rows(path: Path, *, offset: int, limit: int) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.DictReader(handle)]
    if offset > 0:
        rows = rows[offset:]
    if limit > 0:
        rows = rows[:limit]
    return rows


def task_id(row: dict[str, str], index: int) -> str:
    title = row.get("paper_title") or Path(row.get("pdf_path") or f"row_{index}").stem
    base = runner.safe_slug(title, max_len=72)
    return f"mineru_l{index:04d}_{base}"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def existing_parse_records(report_root: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for results_path in sorted(report_root.glob("mineru_only_*/results.jsonl")):
        try:
            lines = results_path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in lines:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if item.get("status") not in {"done", "skipped_existing"}:
                continue
            figures = Path(str(item.get("figures_tables") or ""))
            full_md = Path(str(item.get("full_md") or ""))
            if not figures.exists() or not full_md.exists():
                continue
            for key_name in ("note_path", "pdf_path"):
                key = str(item.get(key_name) or "").strip()
                if key and key not in records:
                    records[key] = item
    return records


def main() -> None:
    args = parse_args()
    runner.resolve_mineru_config(args)
    queue_csv = Path(args.queue_csv).expanduser().resolve()
    output_root = Path(args.output_root).expanduser().resolve()
    report_dir = Path(args.report_root).expanduser().resolve() / f"mineru_only_{now_id()}"
    report_root = Path(args.report_root).expanduser().resolve()
    report_dir.mkdir(parents=True, exist_ok=False)
    rows = load_rows(queue_csv, offset=args.offset, limit=args.limit)
    existing_records = {} if args.force else existing_parse_records(report_root)

    results: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=args.offset + 1):
        started = time.monotonic()
        pdf_path = Path(row.get("pdf_path") or "").expanduser().resolve()
        item_id = task_id(row, index)
        work_dir = output_root / item_id
        parse_dir = work_dir / "parse"
        raw_dir = parse_dir / "mineru_raw"
        figures_path = parse_dir / "figures_tables.json"
        full_path = parse_dir / "full.md"
        result: dict[str, Any] = {
            "status": "started",
            "index": index,
            "task_id": item_id,
            "note_path": row.get("note_path") or "",
            "pdf_path": str(pdf_path),
            "work_dir": str(work_dir),
        }
        try:
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF not found: {pdf_path}")
            existing = existing_records.get(str(row.get("note_path") or "").strip()) or existing_records.get(str(pdf_path))
            if existing:
                result.update({
                    "status": "skipped_existing_global",
                    "existing_work_dir": existing.get("work_dir", ""),
                    "figures_tables": existing.get("figures_tables", ""),
                    "full_md": existing.get("full_md", ""),
                })
            elif not args.force and figures_path.exists() and full_path.exists():
                result.update({"status": "skipped_existing", "figures_tables": str(figures_path), "full_md": str(full_path)})
            else:
                artifacts = runner.run_mineru_cli(
                    pdf_path=pdf_path,
                    output_dir=raw_dir,
                    mineru_bin=args.mineru_bin,
                    backend=args.mineru_backend,
                    timeout=args.mineru_timeout,
                    model_source=args.mineru_model_source,
                    config_path=runner.ensure_mineru_local_config(args),
                )
                markdown = artifacts.markdown_path.read_text(encoding="utf-8", errors="ignore")
                figures_tables = runner.extract_figures_tables(
                    artifacts.content_list_path,
                    source_root=artifacts.root,
                )
                runner.atomic_write_text(full_path, markdown)
                runner.atomic_write_json(figures_path, figures_tables)
                if artifacts.content_list_path:
                    target_content = parse_dir / "content_list.json"
                    target_content.write_bytes(artifacts.content_list_path.read_bytes())
                result.update({
                    "status": "done",
                    "mineru_root": str(artifacts.root),
                    "full_md": str(full_path),
                    "figures_tables": str(figures_path),
                    "figure_count": len(figures_tables),
                })
        except Exception as exc:  # noqa: BLE001
            result.update({"status": "failed", "error": str(exc)})
        result["duration_seconds"] = round(time.monotonic() - started, 3)
        results.append(result)
        with (report_dir / "results.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(result, ensure_ascii=False) + "\n")

    summary = {
        "queue_csv": str(queue_csv),
        "output_root": str(output_root),
        "report_dir": str(report_dir),
        "total": len(results),
        "done": sum(1 for item in results if item["status"] == "done"),
        "skipped_existing": sum(1 for item in results if item["status"] == "skipped_existing"),
        "skipped_existing_global": sum(1 for item in results if item["status"] == "skipped_existing_global"),
        "failed": sum(1 for item in results if item["status"] == "failed"),
        "results_jsonl": str(report_dir / "results.jsonl"),
    }
    write_json(report_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
