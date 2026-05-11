"""Verify current DB/export state for the five reanalysis target papers."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from sqlalchemy import text

from backend.config import settings
from backend.database import async_session
from backend.utils.paper_naming import paper_file_slug

PAPERS = {
    "AIREAI": "147942cd-6284-4aa7-bddf-a097b112e56f",
    "3DGEER": "08f8f231-d7ae-4127-a47d-a5ddb1fea800",
    "ADEPT": "8582023f-c0db-48e3-8411-b2b4e1441acc",
    "ACE": "a58dd10c-8e25-458e-b37c-1fb35a62eed3",
    "AC-Sampler": "c28f1e8c-dcaf-437c-afb4-805e6f6d1803",
}


async def main() -> None:
    vault_root = Path(settings.obsidian_vault_dir)
    if not vault_root.is_absolute():
        vault_root = Path(__file__).resolve().parents[1] / vault_root
    vault_root = vault_root.resolve()
    rows = []
    async with async_session() as session:
        for name, paper_id in PAPERS.items():
            l2 = (await session.execute(text("""
                SELECT id, extracted_formulas, extracted_tables,
                       extracted_figure_images, evidence_spans, created_at
                FROM paper_analyses
                WHERE paper_id = :pid AND level = 'l2_parse' AND is_current = true
                ORDER BY created_at DESC LIMIT 1
            """), {"pid": paper_id})).mappings().one_or_none()
            meta = (l2["evidence_spans"] or {}).get("parse_metadata") if l2 else {}
            meta = meta or {}

            report = (await session.execute(text("""
                SELECT pr.id, pr.report_version, pr.review_status, pr.created_at,
                       count(prs.id) AS section_count,
                       string_agg(prs.section_type, ',' ORDER BY prs.order_index) AS sections,
                       max(prs.body_md) FILTER (WHERE prs.section_type='core_innovation') AS core_innovation_md
                FROM paper_reports pr
                LEFT JOIN paper_report_sections prs ON prs.report_id = pr.id
                WHERE pr.paper_id = :pid AND pr.review_status = 'current'
                GROUP BY pr.id, pr.report_version, pr.review_status, pr.created_at
                ORDER BY pr.created_at DESC LIMIT 1
            """), {"pid": paper_id})).mappings().one_or_none()

            export_rows = (await session.execute(text("""
                SELECT pr.title_zh, p.title, p.title_sanitized, p.venue, p.year
                FROM papers p
                LEFT JOIN LATERAL (
                  SELECT title_zh FROM paper_reports
                  WHERE paper_id = p.id
                  ORDER BY (review_status='current') DESC, created_at DESC LIMIT 1
                ) pr ON true
                WHERE p.id = :pid
            """), {"pid": paper_id})).mappings().one()

            export_matches = []
            if vault_root.exists():
                expected_name = f"P__{paper_file_slug(export_rows['title'], export_rows['title_sanitized'])}.md"
                for path in vault_root.glob("paper/**/*.md"):
                    text_md = path.read_text(encoding="utf-8", errors="ignore")[:3000]
                    title_zh = str(export_rows["title_zh"] or "")
                    title_en = str(export_rows["title"] or "")
                    if (
                        (title_zh and title_zh in text_md)
                        or (title_en and title_en in text_md)
                        or paper_id in text_md
                        or path.name == expected_name
                    ):
                        export_matches.append(str(path.relative_to(vault_root.parent)))

            rows.append({
                "name": name,
                "paper_id": paper_id,
                "l2_id": str(l2["id"]) if l2 else None,
                "l2_created_at": str(l2["created_at"]) if l2 else None,
                "formula_count": len(l2["extracted_formulas"] or []) if l2 else 0,
                "table_count": len(l2["extracted_tables"] or []) if l2 else 0,
                "figure_rows_count": len(l2["extracted_figure_images"] or []) if l2 else 0,
                "parsers_used": meta.get("parsers_used"),
                "formula_source": meta.get("formula_source"),
                "mineru_available": meta.get("mineru_available"),
                "mineru_table_count": meta.get("mineru_table_count"),
                "mineru_formula_count": meta.get("mineru_formula_count"),
                "llm_image_upload_enabled": meta.get("llm_image_upload_enabled"),
                "current_report_id": str(report["id"]) if report else None,
                "current_report_version": report["report_version"] if report else None,
                "current_report_sections": report["sections"] if report else "",
                "current_report_section_count": report["section_count"] if report else 0,
                "core_innovation_prefix": (report["core_innovation_md"] or "")[:160] if report else "",
                "export_paths": export_matches,
            })
    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
