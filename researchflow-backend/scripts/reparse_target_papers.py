"""Re-run L2 parse for the five reanalysis target papers."""

from __future__ import annotations

import asyncio
from uuid import UUID

from backend.database import async_session
from backend.services.parse_service import parse_paper_pdf

PAPER_IDS = [
    "147942cd-6284-4aa7-bddf-a097b112e56f",
    "08f8f231-d7ae-4127-a47d-a5ddb1fea800",
    "8582023f-c0db-48e3-8411-b2b4e1441acc",
    "a58dd10c-8e25-458e-b37c-1fb35a62eed3",
    "c28f1e8c-dcaf-437c-afb4-805e6f6d1803",
]


async def main() -> None:
    async with async_session() as session:
        for paper_id in PAPER_IDS:
            analysis = await parse_paper_pdf(session, UUID(paper_id))
            await session.commit()
            if analysis is None:
                print(f"{paper_id}: failed")
                continue
            meta = (analysis.evidence_spans or {}).get("parse_metadata", {})
            print(
                f"{paper_id}: l2={analysis.id} "
                f"formulas={len(analysis.extracted_formulas or [])} "
                f"tables={len(analysis.extracted_tables or [])} "
                f"figures={len(analysis.extracted_figure_images or [])} "
                f"parsers={meta.get('parsers_used')} "
                f"formula_source={meta.get('formula_source')} "
                f"llm_image_upload={meta.get('llm_image_upload_enabled')}"
            )


if __name__ == "__main__":
    asyncio.run(main())
