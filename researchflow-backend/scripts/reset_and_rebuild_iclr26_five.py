"""Reset and rebuild the formal ICLR26 five-paper batch from clean state.

Policy:
  - Keep canonical papers rows
  - Delete analysis/report/graph projections for the five target papers
  - Re-run MinerU-only L2 parse
  - Re-run force_reanalyze=True
  - Export vault
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from uuid import UUID

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text

from backend.config import settings
from backend.database import async_session
from backend.services.ingest_workflow import IngestWorkflow
from backend.services.parse_service import parse_paper_pdf_mineru_only
from backend.services.vault_export_v6 import export_vault

PAPER_IDS = [
    UUID("d8d14098-7c88-4b22-b93c-e89703540ffb"),
    UUID("e7bdcb2e-34f4-4257-a7a9-cb582373753d"),
    UUID("86c8fa7c-7e04-4d85-b896-b3a320e2a1b2"),
    UUID("08b28ce0-d653-4dc0-99b7-bb42a5771876"),
    UUID("5239ba2c-740e-4569-9894-8685fda5d08e"),
]


async def _reset_one(session, paper_id: UUID) -> None:
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


async def main() -> None:
    async with async_session() as session:
        for pid in PAPER_IDS:
            await _reset_one(session, pid)
        await session.commit()

    async with async_session() as session:
        for pid in PAPER_IDS:
            analysis = await parse_paper_pdf_mineru_only(session, pid)
            if not analysis or analysis.model_name != "mineru_only":
                raise RuntimeError(f"MinerU-only L2 failed for {pid}")
            if not analysis.extracted_figure_images:
                raise RuntimeError(f"MinerU-only L2 produced no figure images for {pid}")
            await session.commit()
            print(f"{pid} l2={analysis.id} figures={len(analysis.extracted_figure_images or [])}")

    async with async_session() as session:
        wf = IngestWorkflow(session)
        for pid in PAPER_IDS:
            out = await wf.run_for_existing_paper(pid, skip_enrich=True, force_reanalyze=True)
            await session.commit()
            print(out)

    async with async_session() as session:
        result = await export_vault(session, vault_dir=settings.obsidian_vault_dir)
        await session.commit()
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
