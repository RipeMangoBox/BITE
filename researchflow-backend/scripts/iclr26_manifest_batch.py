"""Import and run a small deterministic ICLR 2026 batch from resmax manifest.

Workflow:
  1. Select 5 ICLR 2026 papers from manifest with a deterministic rule.
  2. Verify local PDF existence, size, and sha256 against manifest.
  3. Idempotently map/import them into papers.
  4. Optionally run force_reanalyze=True through the 2-agent pipeline.
  5. Optionally export vault and emit DB/vault verification JSON.

Default selection rule:
  - conf_year == ICLR_2026
  - status == done
  - local output_pdf exists
  - sha256 and size_bytes match
  - cover these theme buckets in order:
      llm_rl_agent, benchmark_safety, science_tabular_graph, vision_3d, other
  - within each bucket prefer moderate PDFs (1.5MB-9MB), then title sort
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from dataclasses import dataclass
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
from backend.services.vault_export_v6 import export_vault
from backend.utils.paper_naming import paper_file_slug
from backend.utils.sanitize import sanitize_filename

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "_private" / "resmax_downloads" / "manifest.jsonl"
DEFAULT_THEME_ORDER = [
    "llm_rl_agent",
    "benchmark_safety",
    "science_tabular_graph",
    "vision_3d",
    "other",
]
DEFAULT_TARGET_TITLES = [
    "Opponent Shaping in LLM Agents",
    "How NOT to benchmark your SITE metric: Beyond Static Leaderboards and Towards Realistic Evaluation.",
    "Flock: A Knowledge Graph Foundation Model via Learning on Random Walks",
    "3DSMT: A Hybrid Spiking Mamba-Transformer for Point Cloud Analysis",
    "DiffusionBlocks: Block-wise Neural Network Training via Diffusion Interpretation",
]


@dataclass
class ManifestPaper:
    title: str
    paper_id: str
    openreview_forum_id: str
    output_pdf: str
    sha256: str
    size_bytes: int
    conf_year: str
    status: str
    theme_bucket: str

    @property
    def pdf_path(self) -> Path:
        return REPO_ROOT / self.output_pdf


def _theme_bucket(title: str) -> str:
    t = title.lower()
    if any(k in t for k in ("reinforcement learning", "rlhf", "reasoning", "language model", "agent")):
        return "llm_rl_agent"
    if any(k in t for k in ("benchmark", "security", "safety", "alignment")):
        return "benchmark_safety"
    if any(k in t for k in ("molecular", "protein", "graph", "tabular", "bayesian", "knowledge graph")):
        return "science_tabular_graph"
    if any(k in t for k in ("vision", "image", "video", "gaussian", "3d", "point cloud")):
        return "vision_3d"
    return "other"


def _read_manifest() -> list[ManifestPaper]:
    rows: list[ManifestPaper] = []
    with MANIFEST_PATH.open(encoding="utf-8") as f:
        for line in f:
            raw = json.loads(line)
            if raw.get("conf_year") != "ICLR_2026" or raw.get("status") != "done":
                continue
            output_pdf = raw.get("output_pdf") or ""
            if not output_pdf:
                continue
            row = ManifestPaper(
                title=raw.get("title") or "",
                paper_id=raw.get("paper_id") or "",
                openreview_forum_id=raw.get("openreview_forum_id") or "",
                output_pdf=output_pdf,
                sha256=raw.get("sha256") or "",
                size_bytes=int(raw.get("size_bytes") or 0),
                conf_year=raw.get("conf_year") or "",
                status=raw.get("status") or "",
                theme_bucket=_theme_bucket(raw.get("title") or ""),
            )
            if row.title and row.paper_id and row.openreview_forum_id:
                rows.append(row)
    return rows


def _verify_pdf(row: ManifestPaper) -> dict[str, Any]:
    path = row.pdf_path
    exists = path.exists()
    stat_size = path.stat().st_size if exists else None
    sha = None
    if exists:
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "exists": exists,
        "size_match": exists and stat_size == row.size_bytes,
        "sha256_match": exists and sha == row.sha256,
        "actual_size_bytes": stat_size,
        "actual_sha256": sha,
    }


def _eligible(rows: list[ManifestPaper]) -> list[ManifestPaper]:
    out = []
    for row in rows:
        verify = _verify_pdf(row)
        if verify["exists"] and verify["size_match"] and verify["sha256_match"]:
            out.append(row)
    return out


def select_batch(rows: list[ManifestPaper], titles: list[str] | None = None, limit: int = 5) -> list[ManifestPaper]:
    if titles:
        by_title = {r.title: r for r in rows}
        selected = [by_title[t] for t in titles if t in by_title]
        if len(selected) != len(titles):
            missing = [t for t in titles if t not in by_title]
            raise SystemExit(f"Missing manifest titles: {missing}")
        return selected[:limit]

    rows = _eligible(rows)
    moderate = [r for r in rows if 1_500_000 <= r.size_bytes <= 9_000_000]
    selected: list[ManifestPaper] = []
    used_titles: set[str] = set()
    for bucket in DEFAULT_THEME_ORDER:
        candidates = sorted(
            [r for r in moderate if r.theme_bucket == bucket and r.title not in used_titles],
            key=lambda r: (r.size_bytes, r.title.lower()),
        )
        if not candidates:
            continue
        selected.append(candidates[0])
        used_titles.add(candidates[0].title)
        if len(selected) == limit:
            return selected
    fallback = sorted(
        [r for r in moderate if r.title not in used_titles],
        key=lambda r: (DEFAULT_THEME_ORDER.index(r.theme_bucket) if r.theme_bucket in DEFAULT_THEME_ORDER else 99,
                       r.size_bytes, r.title.lower()),
    )
    for row in fallback:
        selected.append(row)
        if len(selected) == limit:
            break
    return selected


async def _find_existing_paper(session, row: ManifestPaper) -> Paper | None:
    title_sanitized = sanitize_filename(row.title)
    paper_link = f"https://openreview.net/forum?id={row.openreview_forum_id}"
    result = await session.execute(
        select(Paper).where(
            or_(
                func.lower(Paper.title_sanitized) == title_sanitized.lower(),
                Paper.source_ref == row.paper_id,
                Paper.paper_link == paper_link,
            )
        ).limit(1)
    )
    return result.scalar_one_or_none()


async def import_manifest_rows(session, rows: list[ManifestPaper]) -> list[dict[str, Any]]:
    imported: list[dict[str, Any]] = []
    for row in rows:
        existing = await _find_existing_paper(session, row)
        if existing:
            imported.append({
                "paper_uuid": str(existing.id),
                "status": "reused",
                "manifest_paper_id": row.paper_id,
                "title": row.title,
                "openreview_link": f"https://openreview.net/forum?id={row.openreview_forum_id}",
                "pdf_path_local": row.output_pdf,
            })
            if existing.pdf_path_local != row.output_pdf:
                existing.pdf_path_local = row.output_pdf
            if not existing.paper_link:
                existing.paper_link = f"https://openreview.net/forum?id={row.openreview_forum_id}"
            if not existing.source:
                existing.source = "resmax_manifest"
            if not existing.source_ref:
                existing.source_ref = row.paper_id
            if not existing.category:
                existing.category = "ICLR_2026"
            if not existing.venue:
                existing.venue = "ICLR"
            if not existing.year:
                existing.year = 2026
            continue

        paper = Paper(
            title=row.title,
            title_sanitized=sanitize_filename(row.title),
            venue="ICLR",
            year=2026,
            category="ICLR_2026",
            state="enriched",
            pdf_path_local=row.output_pdf,
            paper_link=f"https://openreview.net/forum?id={row.openreview_forum_id}",
            source="resmax_manifest",
            source_ref=row.paper_id,
            source_quality="normal",
        )
        session.add(paper)
        await session.flush()
        imported.append({
            "paper_uuid": str(paper.id),
            "status": "created",
            "manifest_paper_id": row.paper_id,
            "title": row.title,
            "openreview_link": paper.paper_link,
            "pdf_path_local": row.output_pdf,
        })
    return imported


async def run_reanalysis(paper_ids: list[str]) -> list[dict[str, Any]]:
    results = []
    for paper_id in paper_ids:
        async with async_session() as session:
            workflow = IngestWorkflow(session)
            result = await workflow.run_for_existing_paper(UUID(paper_id), force_reanalyze=True)
            await session.commit()
            results.append(result)
    return results


async def collect_db_verification(paper_ids: list[str]) -> list[dict[str, Any]]:
    sql = text("""
        SELECT
          p.id AS paper_id,
          p.title,
          p.title_sanitized,
          p.paper_link,
          p.pdf_path_local,
          pa.id AS l2_id,
          pa.extracted_formulas,
          pa.extracted_tables,
          pa.extracted_figure_images,
          pa.evidence_spans,
          pr.id AS report_id,
          pr.report_version,
          prs.section_count,
          prs.section_titles,
          COALESCE(rel.rel_count, 0) AS relation_count,
          COALESCE(facet.facet_count, 0) AS facet_count,
          COALESCE(ma.method_count, 0) AS method_count,
          COALESCE(kb.profile_count, 0) AS kb_profile_count
        FROM papers p
        LEFT JOIN LATERAL (
          SELECT id, extracted_formulas, extracted_tables, extracted_figure_images, evidence_spans
          FROM paper_analyses
          WHERE paper_id = p.id AND level = 'l2_parse' AND is_current = true
          ORDER BY created_at DESC
          LIMIT 1
        ) pa ON true
        LEFT JOIN LATERAL (
          SELECT id, report_version
          FROM paper_reports
          WHERE paper_id = p.id AND review_status = 'current'
          ORDER BY created_at DESC
          LIMIT 1
        ) pr ON true
        LEFT JOIN LATERAL (
          SELECT
            COUNT(*) AS section_count,
            string_agg(title, ' || ' ORDER BY order_index) AS section_titles
          FROM paper_report_sections
          WHERE report_id = pr.id
        ) prs ON true
        LEFT JOIN LATERAL (
          SELECT COUNT(*) AS rel_count
          FROM paper_relations
          WHERE source_paper_id = p.id OR target_paper_id = p.id
        ) rel ON true
        LEFT JOIN LATERAL (
          SELECT COUNT(*) AS facet_count
          FROM paper_facets
          WHERE paper_id = p.id
        ) facet ON true
        LEFT JOIN LATERAL (
          SELECT COUNT(*) AS method_count
          FROM method_applications
          WHERE paper_id = p.id
        ) ma ON true
        LEFT JOIN LATERAL (
          SELECT COUNT(*) AS profile_count
          FROM kb_node_profiles
          WHERE entity_type = 'paper' AND entity_id = p.id
        ) kb ON true
        WHERE p.id = :paper_id
    """)
    rows_out: list[dict[str, Any]] = []
    async with async_session() as session:
        for paper_id in paper_ids:
            row = (await session.execute(sql, {"paper_id": paper_id})).mappings().one()
            meta = (row["evidence_spans"] or {}).get("parse_metadata") or {}
            rows_out.append({
                "paper_id": str(row["paper_id"]),
                "title": row["title"],
                "paper_link": row["paper_link"],
                "pdf_path_local": row["pdf_path_local"],
                "l2_exists": row["l2_id"] is not None,
                "formula_count": len(row["extracted_formulas"] or []),
                "table_count": len(row["extracted_tables"] or []),
                "figure_count": len(row["extracted_figure_images"] or []),
                "parsers_used": meta.get("parsers_used"),
                "formula_source": meta.get("formula_source"),
                "llm_image_upload_enabled": meta.get("llm_image_upload_enabled"),
                "current_report_id": str(row["report_id"]) if row["report_id"] else None,
                "current_report_version": row["report_version"],
                "current_report_section_count": row["section_count"] or 0,
                "current_report_section_titles": row["section_titles"] or "",
                "relation_count": row["relation_count"],
                "facet_count": row["facet_count"],
                "method_count": row["method_count"],
                "kb_profile_count": row["kb_profile_count"],
            })
    return rows_out


def _find_export_paths(vault_root: Path, paper_id: str, title: str, title_sanitized: str) -> list[str]:
    expected_name = f"P__{paper_file_slug(title, title_sanitized)}.md"
    matches: list[str] = []
    for path in vault_root.glob("paper/**/*.md"):
        if path.name == expected_name:
            matches.append(str(path.relative_to(vault_root)))
            continue
        text_md = path.read_text(encoding="utf-8", errors="ignore")[:4000]
        if paper_id in text_md or title in text_md:
            matches.append(str(path.relative_to(vault_root)))
    return matches


async def collect_vault_verification(paper_ids: list[str]) -> dict[str, Any]:
    vault_root = Path(settings.obsidian_vault_dir)
    if not vault_root.is_absolute():
        vault_root = (BACKEND_ROOT / vault_root).resolve()
    paper_rows = []
    async with async_session() as session:
        for paper_id in paper_ids:
            row = (await session.execute(
                text("SELECT id, title, title_sanitized FROM papers WHERE id = :pid"),
                {"pid": paper_id},
            )).mappings().one()
            paper_rows.append(row)

    paper_exports = []
    for row in paper_rows:
        paths = _find_export_paths(vault_root, str(row["id"]), row["title"], row["title_sanitized"])
        pdf_ref_exists = False
        image_refs_exist = True
        matched_path = None
        if paths:
            matched_path = vault_root / paths[0]
            body = matched_path.read_text(encoding="utf-8", errors="ignore")
            pdf_match = re.search(r"\[\[paperPDFs/([^\]]+\.pdf)\]\]", body)
            if pdf_match:
                pdf_ref_exists = (vault_root / "paperPDFs" / Path(pdf_match.group(1)).name).exists()
                if not pdf_ref_exists:
                    pdf_ref_exists = (vault_root / pdf_match.group(1)).exists()
            for asset_rel in re.findall(r"!\[\[[^\]]*assets/([^\]]+)\]\]", body):
                if not (vault_root / "assets" / asset_rel).exists():
                    image_refs_exist = False
        paper_exports.append({
            "paper_id": str(row["id"]),
            "title": row["title"],
            "export_paths": paths,
            "pdf_ref_exists": pdf_ref_exists,
            "image_refs_exist": image_refs_exist,
        })

    index_summary = {}
    for rel in ["00_Home", "dataset", "method", "domain"]:
        base = vault_root / rel
        if not base.exists():
            index_summary[rel] = {"exists": False, "file_count": 0}
            continue
        md_files = list(base.rglob("*.md"))
        index_summary[rel] = {"exists": True, "file_count": len(md_files)}
    return {"vault_root": str(vault_root), "papers": paper_exports, "indexes": index_summary}


async def run_export() -> dict[str, Any]:
    async with async_session() as session:
        return await export_vault(session, vault_dir=settings.obsidian_vault_dir)


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--run", action="store_true", help="Run force reanalysis after import")
    parser.add_argument("--export", action="store_true", help="Run vault export after ingest")
    parser.add_argument("--verify", action="store_true", help="Emit DB/vault verification JSON")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--titles-json",
        default="",
        help="Optional JSON array of titles to use instead of the default deterministic selector.",
    )
    args = parser.parse_args()

    manifest_rows = _read_manifest()
    titles = json.loads(args.titles_json) if args.titles_json else DEFAULT_TARGET_TITLES
    selected = select_batch(manifest_rows, titles=titles, limit=args.limit)

    selection = []
    for row in selected:
        verify = _verify_pdf(row)
        selection.append({
            "theme_bucket": row.theme_bucket,
            "title": row.title,
            "paper_id": row.paper_id,
            "openreview_forum_id": row.openreview_forum_id,
            "output_pdf": row.output_pdf,
            "size_bytes": row.size_bytes,
            "sha256": row.sha256,
            "verify": verify,
        })

    result: dict[str, Any] = {
        "selection_rule": {
            "mode": "fixed_titles" if titles else "theme_bucket_plus_moderate_pdf",
            "titles": titles,
            "limit": args.limit,
        },
        "selected": selection,
    }

    if args.dry_run:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    async with async_session() as session:
        imported = await import_manifest_rows(session, selected)
        await session.commit()
    result["imported"] = imported

    paper_ids = [row["paper_uuid"] for row in imported]

    if args.run:
        result["pipeline_results"] = await run_reanalysis(paper_ids)

    if args.export:
        result["export_result"] = await run_export()

    if args.verify:
        result["db_verification"] = await collect_db_verification(paper_ids)
        result["vault_verification"] = await collect_vault_verification(paper_ids)

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
