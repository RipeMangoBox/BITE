"""Backfill analysis_agent relation projections + baseline promotion
for the 4 CVPR 2025 smoke papers that missed the new path."""
import asyncio
import time
from uuid import UUID

from sqlalchemy import select

from backend.database import async_session
from backend.models.paper import Paper
from backend.services.ingest_workflow import IngestWorkflow
from backend.services.paper_relation_service import materialize_for_paper
from backend.services.baseline_promoter import promote_for_paper


IDS = [
    "4a7f90e4-a93f-4ba7-a05d-61b8c2cdc0fb",
    "a40f3ec1-4ada-48d6-a412-816131d91ba4",
    "fbfe19bf-44e3-49a0-a231-eeed0b196727",
    "5a8b159d-d6b4-4be3-aea0-2388cdae9752",
]


async def run_one(pid: str) -> dict:
    async with async_session() as s:
        paper_id = UUID(pid)
        paper = (await s.execute(
            select(Paper).where(Paper.id == paper_id)
        )).scalar_one_or_none()
        if not paper:
            return {"pid": pid, "skipped": "no_paper"}

        workflow = IngestWorkflow(s)
        try:
            analysis = await workflow._run_analysis_agent(paper)
            await s.commit()
        except Exception as e:
            await s.rollback()
            return {"pid": pid, "agent_err": str(e)[:200]}

        rel = await materialize_for_paper(s, paper_id)
        await s.commit()
        bp = await promote_for_paper(s, paper_id)
        await s.commit()
        return {
            "pid": pid,
            "analysis_agent": bool(analysis.get("analysis_truth") or analysis.get("reference_role_map")),
            "rel": rel,
            "bp": bp,
        }


async def main() -> None:
    for pid in IDS:
        t0 = time.monotonic()
        r = await run_one(pid)
        print(f"[{pid[:8]}] in {round(time.monotonic() - t0, 1)}s -> {r}")


if __name__ == "__main__":
    asyncio.run(main())
