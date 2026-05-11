"""Run a formal ICLR 2026 batch from a discovery manifest.

Batch policy:
  - PostgreSQL is the write target.
  - L2 is MinerU-only.
  - Failed papers are marked in the batch report, not downgraded to PyMuPDF.
  - Exported Markdown must be present on disk before the script succeeds.
"""

from __future__ import annotations

import argparse
import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any
from uuid import UUID

from sqlalchemy import func, or_, select, text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.config import settings
from backend.database import async_session
from backend.models.paper import Paper
from backend.services.ingest_workflow import IngestWorkflow
from backend.services.parse_service import parse_paper_pdf_mineru_only
from backend.services.vault_export_v6 import export_vault
from backend.utils.paper_naming import paper_file_slug
from backend.utils.sanitize import sanitize_filename


REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DISCOVERY = REPO_ROOT / "_private" / "iclr26_batch" / "manifests" / "discovered_pdfs.jsonl"
DEFAULT_CONTRACT = REPO_ROOT / "_private" / "iclr26_batch" / "contracts" / "batch_0001.md"
DEFAULT_VERIFY = REPO_ROOT / "_private" / "iclr26_batch" / "reports" / "batch_0001_verify.json"
DEFAULT_CHECKLIST = REPO_ROOT / "_private" / "iclr26_batch" / "reports" / "batch_0001_manual_review_checklist.md"
DEFAULT_PROGRESS = REPO_ROOT / "_private" / "iclr26_batch" / "reports" / "batch_0001_progress.jsonl"
DEFAULT_QUARANTINE = REPO_ROOT / "_private" / "iclr26_batch" / "quarantine" / "batch_0001_failed.jsonl"
DEFAULT_SNAPSHOT_MANIFEST = REPO_ROOT / "_private" / "iclr26_batch" / "snapshots" / "batch_0001_vault_manifest.txt"
TERMINAL_PROGRESS_STATUSES = {"succeeded", "needs_repair", "needs_l2_repair", "quarantined"}

CANARY_TITLES = {
    "Opponent Shaping in LLM Agents",
    "How NOT to benchmark your SITE metric: Beyond Static Leaderboards and Towards Realistic Evaluation.",
    "Flock: A Knowledge Graph Foundation Model via Learning on Random Walks",
    "3DSMT: A Hybrid Spiking Mamba-Transformer for Point Cloud Analysis",
    "DiffusionBlocks: Block-wise Neural Network Training via Diffusion Interpretation",
}
CANARY_IDS = {
    "d8d14098-7c88-4b22-b93c-e89703540ffb",
    "e7bdcb2e-34f4-4257-a7a9-cb582373753d",
    "86c8fa7c-7e04-4d85-b896-b3a320e2a1b2",
    "08b28ce0-d653-4dc0-99b7-bb42a5771876",
    "5239ba2c-740e-4569-9894-8685fda5d08e",
}

THEME_ORDER = [
    "llm_rl_agent",
    "benchmark_safety",
    "science_tabular_graph",
    "vision_3d",
    "optimization_training",
    "other",
]


@dataclass
class DiscoveryRow:
    title: str
    openreview_forum_id: str
    sha256: str
    size_bytes: int
    path: str
    source: str
    manifest_paper_id: str
    theme_bucket: str

    @property
    def abs_path(self) -> Path:
        return (REPO_ROOT / self.path).resolve()


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _theme_bucket(title: str) -> str:
    t = title.lower()
    if any(k in t for k in ("reinforcement learning", "rlhf", "reasoning", "language model", "agent", "llm")):
        return "llm_rl_agent"
    if any(k in t for k in ("benchmark", "security", "safety", "alignment", "leaderboard")):
        return "benchmark_safety"
    if any(k in t for k in ("molecular", "protein", "graph", "tabular", "bayesian", "knowledge graph", "conformation")):
        return "science_tabular_graph"
    if any(k in t for k in ("vision", "image", "video", "gaussian", "3d", "point cloud", "camera")):
        return "vision_3d"
    if any(k in t for k in ("optimization", "training", "gradient", "adam", "sgd", "diffusion")):
        return "optimization_training"
    return "other"


def _read_discovery(path: Path) -> list[DiscoveryRow]:
    rows: list[DiscoveryRow] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            raw = json.loads(line)
            if raw.get("conf_year") != "ICLR_2026":
                continue
            if not raw.get("openreview_forum_id"):
                continue
            title = raw.get("title_guess") or ""
            if not title:
                continue
            row = DiscoveryRow(
                title=title,
                openreview_forum_id=raw.get("openreview_forum_id") or "",
                sha256=raw.get("sha256") or "",
                size_bytes=int(raw.get("size_bytes") or 0),
                path=raw.get("path") or "",
                source=raw.get("source") or "unknown",
                manifest_paper_id=raw.get("manifest_paper_id") or "",
                theme_bucket=_theme_bucket(title),
            )
            if row.sha256 and row.path and row.abs_path.exists():
                rows.append(row)
    return rows


async def _existing_canary_refs() -> set[str]:
    refs = set(CANARY_IDS)
    async with async_session() as session:
        result = await session.execute(
            select(Paper.source_ref, Paper.paper_link, Paper.title).where(
                or_(
                    Paper.title.in_(CANARY_TITLES),
                    Paper.id.in_([UUID(pid) for pid in CANARY_IDS]),
                )
            )
        )
        for source_ref, paper_link, title in result:
            if source_ref:
                refs.add(source_ref)
            if paper_link and "id=" in paper_link:
                refs.add(paper_link.rsplit("id=", 1)[-1])
            if title:
                refs.add(title)
    return refs


async def select_batch(rows: list[DiscoveryRow], limit: int) -> list[DiscoveryRow]:
    canary_refs = await _existing_canary_refs()
    eligible = [
        r for r in rows
        if r.title not in canary_refs
        and r.manifest_paper_id not in canary_refs
        and r.openreview_forum_id not in canary_refs
    ]
    selected: list[DiscoveryRow] = []
    used_sha: set[str] = set()

    for bucket in THEME_ORDER:
        bucket_rows = sorted(
            [r for r in eligible if r.theme_bucket == bucket and r.sha256 not in used_sha],
            key=lambda r: (
                0 if 1_500_000 <= r.size_bytes <= 12_000_000 else 1,
                r.size_bytes,
                r.title.lower(),
            ),
        )
        take = max(1, limit // len(THEME_ORDER))
        for row in bucket_rows[:take]:
            selected.append(row)
            used_sha.add(row.sha256)
            if len(selected) >= limit:
                return selected

    fallback = sorted(
        [r for r in eligible if r.sha256 not in used_sha],
        key=lambda r: (
            THEME_ORDER.index(r.theme_bucket) if r.theme_bucket in THEME_ORDER else 99,
            0 if 1_500_000 <= r.size_bytes <= 12_000_000 else 1,
            r.size_bytes,
            r.title.lower(),
        ),
    )
    for row in fallback:
        selected.append(row)
        used_sha.add(row.sha256)
        if len(selected) >= limit:
            break
    return selected


def write_contract(rows: list[DiscoveryRow], discovery_path: Path, contract_path: Path) -> None:
    contract_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# ICLR 2026 Batch 0001 Contract",
        "",
        "- batch_id: `iclr26_0001`",
        f"- generated_at: `{datetime.now(timezone.utc).isoformat()}`",
        f"- source_manifest: `{_rel(discovery_path)}`",
        "- selection_rule: ICLR_2026 rows with verified PDF path/sha256/size, non-empty OpenReview forum id, excluding 5 canary papers, theme-bucket interleaving, limit 25",
        f"- selected_count: `{len(rows)}`",
        "- write_target: PostgreSQL only",
        "- export_target: `obsidian-vault/paper/ICLR_2026/` plus local copied assets",
        "- L2_policy: MinerU-only; `model_name=mineru_only`, `parsers_used=['mineru']`, `formula_source=mineru`",
        "- review_policy: automatic full DB/export verification, then pause for human Markdown review",
        "- failure_policy: single-paper failure enters `needs_repair`, `needs_l2_repair`, or `quarantined`; no PyMuPDF formal fallback",
        "",
        "## Selected Papers",
        "",
        "| # | Theme | Title | OpenReview | SHA256 | Size | PDF path |",
        "|---|-------|-------|------------|--------|------|----------|",
    ]
    for i, row in enumerate(rows, 1):
        link = f"https://openreview.net/forum?id={row.openreview_forum_id}"
        lines.append(
            f"| {i} | {row.theme_bucket} | {row.title.replace('|', '/')} | [{row.openreview_forum_id}]({link}) | `{row.sha256}` | {row.size_bytes} | `{row.path}` |"
        )
    lines += [
        "",
        "## Gates",
        "",
        "- Preflight: all paper rows exist, PDFs resolve locally, OpenReview links exist, no duplicate title/sha conflict.",
        "- L2: current MinerU-only parse exists, figures/tables/images have labels and object keys, extracted figure image count > 0.",
        "- L4/report: current L4 and current 7-section report exist, analysis and writer blackboards exist, delta/evidence counts are non-zero.",
        "- Export: batch paper Markdown exists on disk under `paper/ICLR_2026/`, no unresolved figure/table markers, Links/Dataset non-empty, image refs point to copied local assets.",
        "",
    ]
    contract_path.write_text("\n".join(lines), encoding="utf-8")


def _contract_openreview_ids(contract_path: Path) -> list[str]:
    if not contract_path.exists():
        return []
    ids: list[str] = []
    for line in contract_path.read_text(encoding="utf-8").splitlines():
        match = re.search(r"\|\s*\d+\s*\|.*\|\s*\[([^\]]+)\]\(https://openreview\.net/forum\?id=", line)
        if match:
            ids.append(match.group(1))
    return ids


async def _find_existing_paper(session, row: DiscoveryRow) -> Paper | None:
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


async def import_rows(rows: list[DiscoveryRow]) -> list[dict[str, Any]]:
    imported: list[dict[str, Any]] = []
    async with async_session() as session:
        for row in rows:
            existing = await _find_existing_paper(session, row)
            paper_link = f"https://openreview.net/forum?id={row.openreview_forum_id}"
            if existing:
                existing.title = existing.title or row.title
                existing.title_sanitized = existing.title_sanitized or sanitize_filename(row.title)
                existing.venue = "ICLR"
                existing.year = 2026
                existing.category = "ICLR_2026"
                existing.paper_link = paper_link
                existing.pdf_path_local = row.path
                existing.source = existing.source or row.source or "resmax_manifest"
                existing.source_ref = existing.source_ref or row.manifest_paper_id or row.openreview_forum_id
                existing.source_quality = "normal"
                imported.append({
                    "paper_uuid": str(existing.id),
                    "status": "reused",
                    "title": existing.title,
                    "openreview_forum_id": row.openreview_forum_id,
                    "sha256": row.sha256,
                    "pdf_path_local": row.path,
                })
                continue
            paper = Paper(
                title=row.title,
                title_sanitized=sanitize_filename(row.title),
                venue="ICLR",
                year=2026,
                category="ICLR_2026",
                state="enriched",
                pdf_path_local=row.path,
                paper_link=paper_link,
                source=row.source or "resmax_manifest",
                source_ref=row.manifest_paper_id or row.openreview_forum_id,
                source_quality="normal",
            )
            session.add(paper)
            await session.flush()
            imported.append({
                "paper_uuid": str(paper.id),
                "status": "created",
                "title": paper.title,
                "openreview_forum_id": row.openreview_forum_id,
                "sha256": row.sha256,
                "pdf_path_local": row.path,
            })
        await session.commit()
    return imported


async def preflight(imported: list[dict[str, Any]]) -> dict[str, Any]:
    seen_titles: set[str] = set()
    seen_sha: set[str] = set()
    rows = []
    ok = True
    async with async_session() as session:
        for item in imported:
            paper = await session.get(Paper, UUID(item["paper_uuid"]))
            path = (REPO_ROOT / item["pdf_path_local"]).resolve()
            problems = []
            if not paper:
                problems.append("missing_paper_row")
            if not path.exists():
                problems.append("missing_pdf")
            if paper and not paper.paper_link:
                problems.append("missing_openreview_link")
            title_key = (paper.title if paper else item["title"]).strip().lower()
            if title_key in seen_titles:
                problems.append("duplicate_title_in_batch")
            seen_titles.add(title_key)
            if item["sha256"] in seen_sha:
                problems.append("duplicate_sha_in_batch")
            seen_sha.add(item["sha256"])
            ok = ok and not problems
            rows.append({**item, "problems": problems})
    return {"ok": ok, "rows": rows}


async def reset_current_outputs(session, paper_id: UUID) -> None:
    for sql in [
        "DELETE FROM paper_report_sections WHERE report_id IN (SELECT id FROM paper_reports WHERE paper_id = :pid)",
        "DELETE FROM paper_reports WHERE paper_id = :pid",
        "DELETE FROM agent_blackboard_items WHERE paper_id = :pid",
        "DELETE FROM agent_runs WHERE paper_id = :pid",
        "DELETE FROM reference_role_maps WHERE paper_id = :pid",
        "DELETE FROM paper_extractions WHERE paper_id = :pid",
        "DELETE FROM paper_facets WHERE paper_id = :pid",
        "DELETE FROM paper_relations WHERE source_paper_id = :pid OR target_paper_id = :pid",
        "DELETE FROM method_applications WHERE paper_id = :pid",
        "DELETE FROM evidence_units WHERE paper_id = :pid",
        "DELETE FROM delta_cards WHERE paper_id = :pid",
        "DELETE FROM paper_figures WHERE paper_id = :pid",
        "UPDATE paper_analyses SET is_current = false WHERE paper_id = :pid",
        "UPDATE papers SET current_delta_card_id = NULL, state = 'enriched', ring = NULL, role_in_kb = NULL WHERE id = :pid",
    ]:
        await session.execute(text(sql), {"pid": str(paper_id)})


def _l2_gate_from_analysis(analysis) -> tuple[bool, list[str]]:
    problems = []
    if not analysis:
        return False, ["missing_l2"]
    meta = (analysis.evidence_spans or {}).get("parse_metadata") or {}
    figs = analysis.extracted_figure_images or []
    if analysis.model_name != "mineru_only":
        problems.append("model_name_not_mineru_only")
    if meta.get("parsers_used") != ["mineru"]:
        problems.append(f"parsers_used_not_mineru_only:{meta.get('parsers_used')}")
    if meta.get("formula_source") != "mineru":
        problems.append(f"formula_source_not_mineru:{meta.get('formula_source')}")
    if not isinstance(figs, list) or not figs:
        problems.append("no_extracted_figure_images")
    else:
        for i, fig in enumerate(figs, 1):
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


async def backfill_paper_figures_for_paper(session, paper_id: UUID) -> None:
    row = (await session.execute(text("""
        SELECT extracted_figure_images
        FROM paper_analyses
        WHERE paper_id = :pid AND level = 'l2_parse' AND is_current = true
        ORDER BY created_at DESC LIMIT 1
    """), {"pid": str(paper_id)})).scalar_one_or_none()
    if not isinstance(row, list):
        return
    for fig in row:
        if not isinstance(fig, dict) or not fig.get("object_key"):
            continue
        label = (fig.get("label") or fig.get("caption_label") or f"Figure {fig.get('figure_num') or 1}")[:64]
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


async def l4_report_gate(session, paper_id: UUID) -> dict[str, Any]:
    row = (await session.execute(text("""
        SELECT
          p.id AS paper_id,
          p.title,
          p.state,
          l4.id AS l4_id,
          pr.id AS report_id,
          COALESCE(sec.section_count, 0) AS section_count,
          COALESCE(analysis_bb.cnt, 0) AS analysis_blackboard_count,
          COALESCE(writer_bb.cnt, 0) AS writer_blackboard_count,
          COALESCE(dc.dc_count, 0) AS delta_count,
          COALESCE(ev.ev_count, 0) AS evidence_count,
          COALESCE(pf.fig_count, 0) AS paper_figure_count
        FROM papers p
        LEFT JOIN LATERAL (
          SELECT id FROM paper_analyses
          WHERE paper_id = p.id AND level = 'l4_deep' AND is_current = true
          ORDER BY created_at DESC LIMIT 1
        ) l4 ON true
        LEFT JOIN LATERAL (
          SELECT id FROM paper_reports
          WHERE paper_id = p.id AND review_status = 'current'
          ORDER BY created_at DESC LIMIT 1
        ) pr ON true
        LEFT JOIN LATERAL (
          SELECT COUNT(*) AS section_count
          FROM paper_report_sections WHERE report_id = pr.id
        ) sec ON true
        LEFT JOIN LATERAL (
          SELECT COUNT(*) AS cnt FROM agent_blackboard_items
          WHERE paper_id = p.id AND item_type IN (
            'analysis_truth', 'shallow_extract', 'reference_role_map',
            'deep_analysis', 'graph_candidates', 'kb_profiles'
          )
        ) analysis_bb ON true
        LEFT JOIN LATERAL (
          SELECT COUNT(*) AS cnt FROM agent_blackboard_items
          WHERE paper_id = p.id AND item_type = 'paper_report'
        ) writer_bb ON true
        LEFT JOIN LATERAL (
          SELECT COUNT(*) AS dc_count FROM delta_cards WHERE paper_id = p.id
        ) dc ON true
        LEFT JOIN LATERAL (
          SELECT COUNT(*) AS ev_count FROM evidence_units WHERE paper_id = p.id
        ) ev ON true
        LEFT JOIN LATERAL (
          SELECT COUNT(*) AS fig_count FROM paper_figures WHERE paper_id = p.id
        ) pf ON true
        WHERE p.id = :pid
    """), {"pid": str(paper_id)})).mappings().one()
    problems = []
    if not row["l4_id"]:
        problems.append("missing_current_l4")
    if not row["report_id"]:
        problems.append("missing_current_report")
    if row["section_count"] != 7:
        problems.append(f"report_sections_not_7:{row['section_count']}")
    if row["analysis_blackboard_count"] < 6:
        problems.append(f"analysis_blackboard_incomplete:{row['analysis_blackboard_count']}")
    if row["writer_blackboard_count"] < 1:
        problems.append("missing_writer_blackboard")
    if row["delta_count"] < 1:
        problems.append("missing_delta")
    if row["evidence_count"] < 1:
        problems.append("missing_evidence")
    return dict(row) | {"ok": not problems, "problems": problems}


async def run_one(paper_id: str, progress_path: Path) -> dict[str, Any]:
    pid = UUID(paper_id)
    result: dict[str, Any] = {"paper_id": paper_id, "status": "started", "events": []}

    async with async_session() as session:
        await reset_current_outputs(session, pid)
        await session.commit()
        result["events"].append("reset_current_outputs")

    analysis = None
    for attempt in range(1, 3):
        async with async_session() as session:
            try:
                analysis = await parse_paper_pdf_mineru_only(session, pid)
                ok, problems = _l2_gate_from_analysis(analysis)
                await session.commit()
                result["events"].append({
                    "l2_attempt": attempt,
                    "ok": ok,
                    "problems": problems,
                    "figure_count": len(analysis.extracted_figure_images or []) if analysis else 0,
                })
                if ok:
                    async with async_session() as s2:
                        await backfill_paper_figures_for_paper(s2, pid)
                        await s2.commit()
                    break
            except Exception as exc:
                await session.rollback()
                result["events"].append({"l2_attempt": attempt, "error": str(exc)[:300]})
        analysis = None

    if not analysis:
        result["status"] = "needs_l2_repair"
        _append_jsonl(progress_path, result)
        return result

    async with async_session() as session:
        workflow = IngestWorkflow(session)
        pipeline = await workflow.run_for_existing_paper(
            pid,
            skip_enrich=True,
            force_reanalyze=True,
        )
        await session.commit()
        result["pipeline"] = pipeline

    deep_phase = ((result.get("pipeline") or {}).get("phases") or {}).get("deep_ingest") or {}
    if deep_phase.get("status") == "needs_repair":
        result["status"] = "needs_repair"
        result["l4_report_gate"] = {
            "ok": False,
            "problems": [deep_phase.get("reason", "deep_ingest_needs_repair")],
            "missing": deep_phase.get("missing", []),
        }
        _append_jsonl(progress_path, result)
        return result

    async with async_session() as session:
        gate = await l4_report_gate(session, pid)
        result["l4_report_gate"] = gate
        result["status"] = "succeeded" if gate["ok"] else "needs_repair"

    _append_jsonl(progress_path, result)
    return result


def _append_jsonl(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, default=str) + "\n")


def _load_progress(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Cannot resume: invalid progress JSONL at {path}:{line_no}: {exc}") from exc
            if isinstance(raw, dict):
                rows.append(raw)
    return rows


def _resume_state(path: Path) -> tuple[list[dict[str, Any]], set[str]]:
    by_paper: dict[str, dict[str, Any]] = {}
    for row in _load_progress(path):
        paper_id = row.get("paper_id")
        if paper_id and row.get("status") in TERMINAL_PROGRESS_STATUSES:
            by_paper[paper_id] = row
    return list(by_paper.values()), set(by_paper)


def _vault_root() -> Path:
    vault = Path(settings.obsidian_vault_dir)
    if not vault.is_absolute():
        vault = (BACKEND_ROOT / vault).resolve()
    return vault


def _find_export_path(vault: Path, title: str, title_sanitized: str) -> Path | None:
    expected = f"P__{paper_file_slug(title, title_sanitized)}.md"
    path = vault / "paper" / "ICLR_2026" / expected
    if path.exists():
        return path
    matches = list((vault / "paper" / "ICLR_2026").glob(expected)) if (vault / "paper" / "ICLR_2026").exists() else []
    return matches[0] if matches else None


def _asset_refs(body: str) -> list[str]:
    refs = re.findall(r"!\[[^\]]*\]\(([^)]+assets/figures/[^)]+)\)", body)
    refs.extend(re.findall(r"!\[\[([^\]]*assets/figures/[^\]]+)\]\]", body))
    return refs


def _asset_exists(note_path: Path, ref: str, vault: Path) -> bool:
    ref = ref.strip()
    if ref.startswith("http://") or ref.startswith("https://"):
        return True
    raw = Path(ref)
    candidates = [note_path.parent / raw, vault / raw]
    if ref.startswith("../"):
        candidates.append((note_path.parent / raw).resolve())
    return any(p.exists() for p in candidates)


async def verify_batch(imported: list[dict[str, Any]], run_results: list[dict[str, Any]], export_result: dict[str, Any]) -> dict[str, Any]:
    vault = _vault_root()
    paper_checks = []
    async with async_session() as session:
        for item in imported:
            pid = item["paper_uuid"]
            row = (await session.execute(text("""
                SELECT
                  p.id, p.title, p.title_sanitized, p.paper_link, p.pdf_path_local,
                  l2.model_name, l2.extracted_figure_images, l2.evidence_spans,
                  l4.id AS l4_id,
                  pr.id AS report_id,
                  COALESCE(sec.section_count, 0) AS section_count,
                  COALESCE(facet.facet_count, 0) AS facet_count,
                  COALESCE(ds.dataset_count, 0) AS dataset_count,
                  COALESCE(pf.fig_count, 0) AS paper_figure_count,
                  COALESCE(ev.ev_count, 0) AS evidence_count,
                  COALESCE(dc.dc_count, 0) AS delta_count,
                  COALESCE(abb.analysis_count, 0) AS analysis_blackboard_count,
                  COALESCE(wbb.writer_count, 0) AS writer_blackboard_count
                FROM papers p
                LEFT JOIN LATERAL (
                  SELECT model_name, extracted_figure_images, evidence_spans
                  FROM paper_analyses
                  WHERE paper_id = p.id AND level = 'l2_parse' AND is_current = true
                  ORDER BY created_at DESC LIMIT 1
                ) l2 ON true
                LEFT JOIN LATERAL (
                  SELECT id FROM paper_analyses
                  WHERE paper_id = p.id AND level = 'l4_deep' AND is_current = true
                  ORDER BY created_at DESC LIMIT 1
                ) l4 ON true
                LEFT JOIN LATERAL (
                  SELECT id FROM paper_reports
                  WHERE paper_id = p.id AND review_status = 'current'
                  ORDER BY created_at DESC LIMIT 1
                ) pr ON true
                LEFT JOIN LATERAL (
                  SELECT COUNT(*) AS section_count FROM paper_report_sections WHERE report_id = pr.id
                ) sec ON true
                LEFT JOIN LATERAL (
                  SELECT COUNT(*) AS facet_count FROM paper_facets WHERE paper_id = p.id
                ) facet ON true
                LEFT JOIN LATERAL (
                  SELECT COUNT(*) AS dataset_count
                  FROM paper_facets pf JOIN taxonomy_nodes tn ON tn.id = pf.node_id
                  WHERE pf.paper_id = p.id AND tn.dimension = 'dataset'
                ) ds ON true
                LEFT JOIN LATERAL (
                  SELECT COUNT(*) AS fig_count FROM paper_figures WHERE paper_id = p.id
                ) pf ON true
                LEFT JOIN LATERAL (
                  SELECT COUNT(*) AS ev_count FROM evidence_units WHERE paper_id = p.id
                ) ev ON true
                LEFT JOIN LATERAL (
                  SELECT COUNT(*) AS dc_count FROM delta_cards WHERE paper_id = p.id
                ) dc ON true
                LEFT JOIN LATERAL (
                  SELECT COUNT(*) AS analysis_count FROM agent_blackboard_items
                  WHERE paper_id = p.id AND item_type IN (
                    'analysis_truth', 'shallow_extract', 'reference_role_map',
                    'deep_analysis', 'graph_candidates', 'kb_profiles'
                  )
                ) abb ON true
                LEFT JOIN LATERAL (
                  SELECT COUNT(*) AS writer_count FROM agent_blackboard_items
                  WHERE paper_id = p.id AND item_type = 'paper_report'
                ) wbb ON true
                WHERE p.id = :pid
            """), {"pid": pid})).mappings().one()

            meta = (row["evidence_spans"] or {}).get("parse_metadata") or {}
            figs = row["extracted_figure_images"] or []
            note = _find_export_path(vault, row["title"], row["title_sanitized"])
            export_problems = []
            links_ok = False
            dataset_ok = False
            no_markers = False
            image_refs_exist = False
            asset_dir_exists = (vault / "assets" / "figures" / "papers" / pid).exists()
            body = ""
            if note and note.exists():
                body = note.read_text(encoding="utf-8", errors="ignore")
                links_ok = bool(re.search(r"\| Links \|.*openreview\.net|\[paper\]\(https://openreview\.net", body, re.IGNORECASE))
                dataset_match = re.search(r"\| Dataset \|\s*([^|]+)\|", body)
                dataset_value = dataset_match.group(1).strip() if dataset_match else ""
                dataset_ok = bool(dataset_value and dataset_value not in {"—", "-", "N/A", "待补充", "未知"})
                no_markers = "{{FIG:" not in body and "{{TBL:" not in body
                refs = _asset_refs(body)
                image_refs_exist = bool(refs) and all(_asset_exists(note, ref, vault) for ref in refs)
            else:
                export_problems.append("markdown_not_written_to_disk")

            if note and "Unknown_" in note.as_posix():
                export_problems.append("unknown_path")
            if note and "ICLR_2025" in note.as_posix():
                export_problems.append("iclr_2025_path_pollution")
            if not links_ok:
                export_problems.append("links_missing_openreview")
            if not dataset_ok:
                export_problems.append("dataset_empty")
            if not no_markers:
                export_problems.append("unresolved_fig_tbl_marker")
            if not image_refs_exist:
                export_problems.append("image_refs_missing_or_uncopied")
            if not asset_dir_exists:
                export_problems.append("asset_dir_missing")

            db_problems = []
            if row["model_name"] != "mineru_only":
                db_problems.append("l2_model_not_mineru_only")
            if meta.get("parsers_used") != ["mineru"]:
                db_problems.append("l2_parsers_used_not_mineru_only")
            if meta.get("formula_source") != "mineru":
                db_problems.append("l2_formula_source_not_mineru")
            if not figs:
                db_problems.append("l2_no_figures")
            if not row["l4_id"]:
                db_problems.append("missing_l4")
            if not row["report_id"]:
                db_problems.append("missing_report")
            if row["section_count"] != 7:
                db_problems.append(f"sections_not_7:{row['section_count']}")
            if row["delta_count"] < 1:
                db_problems.append("missing_delta")
            if row["evidence_count"] < 1:
                db_problems.append("missing_evidence")
            if row["analysis_blackboard_count"] < 6:
                db_problems.append("analysis_blackboard_incomplete")
            if row["writer_blackboard_count"] < 1:
                db_problems.append("writer_blackboard_missing")

            paper_checks.append({
                "paper_id": pid,
                "title": row["title"],
                "db_ok": not db_problems,
                "export_ok": not export_problems,
                "db_problems": db_problems,
                "export_problems": export_problems,
                "export_path": _rel(note) if note else None,
                "l2": {
                    "model_name": row["model_name"],
                    "parsers_used": meta.get("parsers_used"),
                    "formula_source": meta.get("formula_source"),
                    "figure_count": len(figs) if isinstance(figs, list) else 0,
                    "paper_figure_count": row["paper_figure_count"],
                },
                "l4_report": {
                    "section_count": row["section_count"],
                    "delta_count": row["delta_count"],
                    "evidence_count": row["evidence_count"],
                    "facet_count": row["facet_count"],
                    "dataset_count": row["dataset_count"],
                },
            })

    succeeded = [p for p in paper_checks if p["db_ok"] and p["export_ok"]]
    needs_repair = [p for p in paper_checks if p["db_ok"] and not p["export_ok"]]
    failed_db = [p for p in paper_checks if not p["db_ok"]]
    return {
        "batch_id": "iclr26_0001",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "vault_root": str(vault),
        "export_result": export_result,
        "selected": len(imported),
        "l2_passed": sum(1 for p in paper_checks if not any(x.startswith("l2_") for x in p["db_problems"])),
        "l4_report_passed": sum(1 for p in paper_checks if p["db_ok"]),
        "exported_pages": sum(1 for p in paper_checks if p["export_path"]),
        "succeeded_papers": [{"paper_id": p["paper_id"], "title": p["title"], "export_path": p["export_path"]} for p in succeeded],
        "needs_repair_papers": [{"paper_id": p["paper_id"], "title": p["title"], "problems": p["db_problems"] + p["export_problems"]} for p in needs_repair + failed_db],
        "quarantined_papers": [],
        "run_results": run_results,
        "paper_checks": paper_checks,
        "must_fix_link_issues": [
            {"paper_id": p["paper_id"], "title": p["title"], "db": p["db_problems"], "export": p["export_problems"]}
            for p in paper_checks if p["db_problems"] or p["export_problems"]
        ],
        "acceptable_risks": [
            "DS/DeepSeek text agents do not inspect image pixels; figure quality still requires human visual review.",
            "Dataset facet extraction is agent-derived and should be checked in manual Markdown review.",
        ],
    }


def write_checklist(verify: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Batch 0001 Manual Review Checklist",
        "",
        "- batch_id: `iclr26_0001`",
        f"- verify_report: `{_rel(DEFAULT_VERIFY)}`",
        "- review_scope: exported Markdown pages listed below",
        "",
        "## Review Items",
        "",
    ]
    for paper in verify.get("paper_checks", []):
        mark = "PASS" if paper["db_ok"] and paper["export_ok"] else "CHECK"
        lines += [
            f"### {mark} {paper['title']}",
            "",
            f"- paper_id: `{paper['paper_id']}`",
            f"- export_path: `{paper.get('export_path')}`",
            f"- db_problems: `{paper.get('db_problems')}`",
            f"- export_problems: `{paper.get('export_problems')}`",
            "- Check wrong-paper contamination.",
            "- Check Dataset row is meaningful.",
            "- Check no unresolved placeholders or figure/table markers.",
            "- Check figure/table references match surrounding text.",
            "",
        ]
    path.write_text("\n".join(lines), encoding="utf-8")


async def export_and_verify(imported: list[dict[str, Any]], run_results: list[dict[str, Any]]) -> dict[str, Any]:
    async with async_session() as session:
        export_result = await export_vault(session, vault_dir=settings.obsidian_vault_dir)
        await session.commit()
    vault = _vault_root()
    DEFAULT_SNAPSHOT_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    if vault.exists():
        files = sorted(p.relative_to(vault).as_posix() for p in vault.rglob("*") if p.is_file())
        DEFAULT_SNAPSHOT_MANIFEST.write_text("\n".join(files) + "\n", encoding="utf-8")
    verify = await verify_batch(imported, run_results, export_result)
    DEFAULT_VERIFY.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_VERIFY.write_text(json.dumps(verify, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    write_checklist(verify, DEFAULT_CHECKLIST)
    with DEFAULT_QUARANTINE.open("w", encoding="utf-8") as f:
        for paper in verify.get("quarantined_papers", []):
            f.write(json.dumps(paper, ensure_ascii=False) + "\n")
    return verify


async def main_async(args: argparse.Namespace) -> None:
    discovery_path = Path(args.discovery_manifest)
    rows = _read_discovery(discovery_path)
    selected = await select_batch(rows, args.limit)
    if not selected:
        raise SystemExit("No eligible ICLR_2026 PDFs found for batch_0001")
    contract_path = Path(args.batch_contract)
    if args.resume and contract_path.exists():
        contract_ids = _contract_openreview_ids(contract_path)
        selected_ids = [row.openreview_forum_id for row in selected]
        if contract_ids and contract_ids != selected_ids:
            raise SystemExit("Cannot resume: current selected papers differ from the existing batch contract")
    else:
        write_contract(selected, discovery_path, contract_path)

    result: dict[str, Any] = {
        "batch_id": "iclr26_0001",
        "selected": [
            {
                "title": r.title,
                "openreview_forum_id": r.openreview_forum_id,
                "sha256": r.sha256,
                "size_bytes": r.size_bytes,
                "path": r.path,
                "theme_bucket": r.theme_bucket,
            }
            for r in selected
        ],
        "contract": _rel(contract_path),
    }
    if args.contract_only:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    imported = await import_rows(selected)
    result["imported"] = imported
    pf = await preflight(imported)
    result["preflight"] = pf
    if not pf["ok"]:
        DEFAULT_VERIFY.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        raise SystemExit(f"Preflight failed; wrote {DEFAULT_VERIFY}")

    progress_path = Path(args.progress_path)
    if args.resume:
        run_results, completed_paper_ids = _resume_state(progress_path)
        progress_path.parent.mkdir(parents=True, exist_ok=True)
        progress_path.touch(exist_ok=True)
        print(
            f"Resume enabled: loaded {len(run_results)} completed paper result(s) from {_rel(progress_path)}",
            flush=True,
        )
    else:
        progress_path.parent.mkdir(parents=True, exist_ok=True)
        progress_path.write_text("", encoding="utf-8")
        run_results = []
        completed_paper_ids: set[str] = set()

    new_papers_processed = 0
    for i, item in enumerate(imported, 1):
        if item["paper_uuid"] in completed_paper_ids:
            print(f"[{i}/{len(imported)}] SKIP {item['paper_uuid']} {item['title'][:90]}", flush=True)
            continue
        if args.max_new_papers is not None and new_papers_processed >= args.max_new_papers:
            print(
                f"Reached --max-new-papers={args.max_new_papers}; stopping before remaining unprocessed papers",
                flush=True,
            )
            break
        print(f"[{i}/{len(imported)}] {item['paper_uuid']} {item['title'][:90]}", flush=True)
        res = await run_one(item["paper_uuid"], progress_path)
        run_results.append(res)
        new_papers_processed += 1
        print(f"  status={res['status']}", flush=True)

    verify = await export_and_verify(imported, run_results)
    print(json.dumps({
        "batch_id": verify["batch_id"],
        "selected": verify["selected"],
        "l2_passed": verify["l2_passed"],
        "l4_report_passed": verify["l4_report_passed"],
        "exported_pages": verify["exported_pages"],
        "needs_repair": verify["needs_repair_papers"],
        "quarantined": verify["quarantined_papers"],
        "verify_report": _rel(DEFAULT_VERIFY),
        "manual_review_checklist": _rel(DEFAULT_CHECKLIST),
        "next_action": "wait_for_human_markdown_review",
    }, ensure_ascii=False, indent=2))

    missing_md = [p for p in verify["paper_checks"] if "markdown_not_written_to_disk" in p["export_problems"]]
    if missing_md:
        raise SystemExit("Markdown export missing for at least one paper; stopping before any further batch.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-contract", default=str(DEFAULT_CONTRACT))
    parser.add_argument("--discovery-manifest", default=str(DEFAULT_DISCOVERY))
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--mineru-only", action="store_true")
    parser.add_argument("--stop-before-human-review", action="store_true")
    parser.add_argument("--contract-only", action="store_true")
    parser.add_argument("--progress-path", default=str(DEFAULT_PROGRESS))
    parser.add_argument("--resume", action="store_true", help="Skip terminal paper results already recorded in the progress JSONL.")
    parser.add_argument("--max-new-papers", type=int, default=None, help="When resuming, process at most this many not-yet-recorded papers.")
    args = parser.parse_args()
    if not args.mineru_only:
        raise SystemExit("Formal ICLR26 batch requires --mineru-only")
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
