"""Run MinerU-only L2 preprocessing for an ICLR 2026 PDF batch.

This script intentionally stops at L2. It does not run analysis agents, writer
agents, L4 materialization, vault export, or Markdown generation.
"""

from __future__ import annotations

import argparse
import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any
from uuid import UUID

from sqlalchemy import func, or_, select, text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.database import async_session
from backend.models.paper import Paper
from backend.services.parse_service import parse_paper_pdf_mineru_only
from backend.utils.sanitize import sanitize_filename


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = REPO_ROOT / "_private" / "iclr26_batch" / "reports"


@dataclass(frozen=True)
class BatchRow:
    batch_id: str
    title: str
    openreview_forum_id: str
    sha256: str
    size_bytes: int
    path: str
    source: str
    manifest_paper_id: str
    theme_bucket: str


def read_batch_manifest(path: Path) -> list[BatchRow]:
    rows: list[BatchRow] = []
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            raw = json.loads(line)
            missing = [k for k in ("batch_id", "title", "openreview_forum_id", "sha256", "path") if not raw.get(k)]
            if missing:
                raise SystemExit(f"{path}:{line_no} missing required field(s): {missing}")
            rows.append(BatchRow(
                batch_id=raw["batch_id"],
                title=raw["title"],
                openreview_forum_id=raw["openreview_forum_id"],
                sha256=raw["sha256"],
                size_bytes=int(raw.get("size_bytes") or 0),
                path=raw["path"],
                source=raw.get("source") or "resmax",
                manifest_paper_id=raw.get("manifest_paper_id") or raw["openreview_forum_id"],
                theme_bucket=raw.get("theme_bucket") or "other",
            ))
    return rows


def _append_jsonl(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, default=str) + "\n")


async def _find_existing_paper(session, row: BatchRow) -> Paper | None:
    title_sanitized = sanitize_filename(row.title)
    paper_link = f"https://openreview.net/forum?id={row.openreview_forum_id}"
    result = await session.execute(
        select(Paper).where(
            or_(
                func.lower(Paper.title_sanitized) == title_sanitized.lower(),
                Paper.source_ref == row.manifest_paper_id,
                Paper.paper_link == paper_link,
            )
        ).limit(1)
    )
    return result.scalar_one_or_none()


async def import_or_update_row(row: BatchRow) -> Paper:
    async with async_session() as session:
        paper_link = f"https://openreview.net/forum?id={row.openreview_forum_id}"
        existing = await _find_existing_paper(session, row)
        if existing:
            existing.venue = "ICLR"
            existing.year = 2026
            existing.category = "ICLR_2026"
            existing.paper_link = paper_link
            existing.pdf_path_local = row.path
            existing.source = existing.source or row.source
            existing.source_ref = existing.source_ref or row.manifest_paper_id
            existing.source_quality = "normal"
            await session.commit()
            await session.refresh(existing)
            return existing

        paper = Paper(
            title=row.title,
            title_sanitized=sanitize_filename(row.title),
            venue="ICLR",
            year=2026,
            category="ICLR_2026",
            state="enriched",
            pdf_path_local=row.path,
            paper_link=paper_link,
            source=row.source,
            source_ref=row.manifest_paper_id,
            source_quality="normal",
        )
        session.add(paper)
        await session.commit()
        await session.refresh(paper)
        return paper


def l2_gate(analysis) -> tuple[bool, list[str]]:
    if not analysis:
        return False, ["missing_l2"]
    problems: list[str] = []
    meta = (analysis.evidence_spans or {}).get("parse_metadata") or {}
    figures = analysis.extracted_figure_images or []
    if analysis.model_name != "mineru_only":
        problems.append("model_name_not_mineru_only")
    if meta.get("parsers_used") != ["mineru"]:
        problems.append(f"parsers_used_not_mineru_only:{meta.get('parsers_used')}")
    if meta.get("formula_source") != "mineru":
        problems.append(f"formula_source_not_mineru:{meta.get('formula_source')}")
    if not isinstance(figures, list) or not figures:
        problems.append("no_extracted_figure_images")
    else:
        for i, fig in enumerate(figures, 1):
            if not isinstance(fig, dict):
                problems.append(f"image_{i}_not_object")
                continue
            if not fig.get("label") and not fig.get("caption_label"):
                problems.append(f"image_{i}_missing_label")
            if not fig.get("object_key"):
                problems.append(f"image_{i}_missing_object_key")
            if not fig.get("caption") and not fig.get("source_path"):
                problems.append(f"image_{i}_missing_caption_or_source_path")
    return not problems, problems


async def backfill_paper_figures_for_paper(paper_id: UUID) -> int:
    async with async_session() as session:
        row = (await session.execute(text("""
            SELECT extracted_figure_images
            FROM paper_analyses
            WHERE paper_id = :pid AND level = 'l2_parse' AND is_current = true
            ORDER BY created_at DESC LIMIT 1
        """), {"pid": str(paper_id)})).scalar_one_or_none()
        if not isinstance(row, list):
            return 0
        count = 0
        for fig in row:
            if not isinstance(fig, dict) or not fig.get("object_key"):
                continue
            label = (fig.get("label") or fig.get("caption_label") or f"Figure {fig.get('figure_num') or count + 1}")[:64]
            await session.execute(text("""
                INSERT INTO paper_figures (
                    paper_id, label, type, semantic_role, page_num, bbox,
                    object_key, public_url, caption, description,
                    width, height, size_bytes, extraction_method
                )
                VALUES (
                    :paper_id, :label, :type, :semantic_role, :page_num, CAST(:bbox AS jsonb),
                    :object_key, :public_url, :caption, :description,
                    :width, :height, :size_bytes, :extraction_method
                )
                ON CONFLICT (paper_id, label) DO NOTHING
            """), {
                "paper_id": str(paper_id),
                "label": label,
                "type": (fig.get("type") or "figure")[:16],
                "semantic_role": (fig.get("semantic_role") or "other")[:32],
                "page_num": fig.get("page_num"),
                "bbox": json.dumps(fig.get("bbox")) if fig.get("bbox") is not None else None,
                "object_key": fig.get("object_key")[:500],
                "public_url": fig.get("public_url"),
                "caption": (fig.get("caption") or "")[:8000],
                "description": (fig.get("description") or "")[:8000],
                "width": fig.get("width"),
                "height": fig.get("height"),
                "size_bytes": fig.get("size_bytes"),
                "extraction_method": (fig.get("extraction_method") or "mineru")[:32],
            })
            count += 1
        await session.commit()
        return count


async def preprocess_one(row: BatchRow) -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    paper = await import_or_update_row(row)
    pdf_path = (REPO_ROOT / row.path).resolve()
    result: dict[str, Any] = {
        "batch_id": row.batch_id,
        "paper_id": str(paper.id),
        "title": row.title,
        "openreview_forum_id": row.openreview_forum_id,
        "pdf_path": row.path,
        "started_at": started.isoformat(),
    }
    if not pdf_path.exists():
        result.update({"status": "failed", "problems": ["missing_pdf"]})
        return result

    analysis = None
    last_problems: list[str] = []
    for attempt in range(1, 3):
        async with async_session() as session:
            try:
                analysis = await parse_paper_pdf_mineru_only(session, paper.id)
                ok, problems = l2_gate(analysis)
                await session.commit()
                last_problems = problems
                result[f"attempt_{attempt}"] = {
                    "ok": ok,
                    "problems": problems,
                    "figure_count": len(analysis.extracted_figure_images or []) if analysis else 0,
                }
                if ok:
                    figure_rows = await backfill_paper_figures_for_paper(paper.id)
                    completed = datetime.now(timezone.utc)
                    result.update({
                        "status": "succeeded",
                        "completed_at": completed.isoformat(),
                        "duration_seconds": round((completed - started).total_seconds(), 3),
                        "figure_count": len(analysis.extracted_figure_images or []),
                        "paper_figures_backfilled": figure_rows,
                    })
                    return result
            except Exception as exc:
                await session.rollback()
                last_problems = [str(exc)[:300]]
                result[f"attempt_{attempt}"] = {"ok": False, "error": str(exc)[:300]}
    completed = datetime.now(timezone.utc)
    result.update({
        "status": "failed",
        "completed_at": completed.isoformat(),
        "duration_seconds": round((completed - started).total_seconds(), 3),
        "problems": last_problems,
    })
    return result


async def main_async(args: argparse.Namespace) -> None:
    manifest = Path(args.batch_manifest)
    rows = read_batch_manifest(manifest)
    if not rows:
        raise SystemExit(f"No rows in {manifest}")
    batch_id = args.batch_id or rows[0].batch_id
    if any(row.batch_id != batch_id for row in rows):
        raise SystemExit("Manifest contains multiple batch_id values; pass the matching --batch-id explicitly")

    report_dir = Path(args.report_dir)
    progress_path = report_dir / f"mineru_preprocess_batch_{batch_id.rsplit('_', 1)[-1]}_progress.jsonl"
    summary_path = report_dir / f"mineru_preprocess_batch_{batch_id.rsplit('_', 1)[-1]}_summary.json"
    if not args.resume:
        progress_path.parent.mkdir(parents=True, exist_ok=True)
        progress_path.write_text("", encoding="utf-8")

    completed_ids = set()
    if args.resume and progress_path.exists():
        with progress_path.open(encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                raw = json.loads(line)
                if raw.get("status") in {"succeeded", "failed"} and raw.get("openreview_forum_id"):
                    completed_ids.add(raw["openreview_forum_id"])

    results: list[dict[str, Any]] = []
    for index, row in enumerate(rows, 1):
        if row.openreview_forum_id in completed_ids:
            print(f"[{index}/{len(rows)}] SKIP {row.openreview_forum_id} {row.title[:80]}", flush=True)
            continue
        print(f"[{index}/{len(rows)}] MinerU L2 {row.openreview_forum_id} {row.title[:80]}", flush=True)
        result = await preprocess_one(row)
        results.append(result)
        _append_jsonl(progress_path, result)
        print(f"  status={result['status']} duration={result.get('duration_seconds')}s", flush=True)

    all_progress: list[dict[str, Any]] = []
    if progress_path.exists():
        with progress_path.open(encoding="utf-8") as f:
            all_progress = [json.loads(line) for line in f if line.strip()]
    succeeded = [r for r in all_progress if r.get("status") == "succeeded"]
    failed = [r for r in all_progress if r.get("status") == "failed"]
    summary = {
        "batch_id": batch_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "batch_manifest": str(manifest),
        "selected_count": len(rows),
        "processed_count": len(all_progress),
        "succeeded_count": len(succeeded),
        "failed_count": len(failed),
        "progress_path": str(progress_path),
        "failed": failed,
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, default=str))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-manifest", required=True)
    parser.add_argument("--batch-id", default="")
    parser.add_argument("--report-dir", default=str(DEFAULT_REPORT_DIR))
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
