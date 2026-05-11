"""Backfill reference_role_map + paper_relations for historical L4 papers.

For each L4 paper that has no reference_role_map blackboard entry yet:
  1. Run analysis_agent on the paper and write compatibility blackboard items
  3. Run paper_relation_service.materialize_for_paper

Then run materialize_all once at the end so newly-added blackboard rows
also flow through to paper_relations (in case the per-paper call missed any).

Usage:
    python -m scripts.backfill_paper_relations              # all candidates
    python -m scripts.backfill_paper_relations --limit 10   # cap
    python -m scripts.backfill_paper_relations --only-materialize
        # skip the agent call; just re-materialize existing blackboard rows
"""

from __future__ import annotations

import argparse
import asyncio
import json as _json
import logging
import time
from uuid import UUID

from sqlalchemy import select, text as sa_text

from backend.database import async_session
from backend.models.agent import AgentBlackboardItem
from backend.models.paper import Paper
from backend.services.ingest_workflow import IngestWorkflow
from backend.services.paper_relation_service import (
    materialize_for_paper, materialize_all, _load_paper_index,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


SQL_PAPERS_NEEDING_RR = sa_text("""
    SELECT pa.paper_id
    FROM paper_analyses pa
    WHERE pa.level = 'l4_deep' AND pa.is_current
      AND pa.full_report_md IS NOT NULL
      AND pa.paper_id NOT IN (
        SELECT DISTINCT paper_id
        FROM agent_blackboard_items
        WHERE item_type = 'reference_role_map'
      )
    ORDER BY pa.paper_id
""")


async def backfill_one(session, workflow: IngestWorkflow, paper_id: UUID,
                       paper_index) -> dict:
    paper = (await session.execute(
        select(Paper).where(Paper.id == paper_id)
    )).scalar_one_or_none()
    if not paper:
        return {"paper_id": str(paper_id), "skipped": "no_paper"}

    t0 = time.monotonic()
    try:
        result = await workflow._run_analysis_agent(paper)
        await session.commit()
    except Exception as e:
        await session.rollback()
        return {"paper_id": str(paper_id), "agent_error": str(e)[:200]}

    # Now materialize paper_relations using the freshly-written blackboard row
    rel_stats = await materialize_for_paper(session, paper_id, paper_index=paper_index)
    await session.commit()
    rel_stats["agent_duration_s"] = round(time.monotonic() - t0, 1)
    rel_stats["analysis_agent"] = bool(result.get("analysis_truth") or result.get("reference_role_map"))
    return rel_stats


async def main(limit: int | None, only_materialize: bool) -> None:
    async with async_session() as session:
        if only_materialize:
            stats = await materialize_all(session)
            logger.info("materialize_all: %s", stats)
            return

        ids = (await session.execute(SQL_PAPERS_NEEDING_RR)).scalars().all()
        if limit:
            ids = ids[:limit]
        logger.info("Found %d papers needing analysis_agent relation backfill", len(ids))
        if not ids:
            stats = await materialize_all(session)
            logger.info("Nothing to backfill; materialize_all: %s", stats)
            return

        paper_index = await _load_paper_index(session)
        workflow = IngestWorkflow(session)

        results = []
        for i, pid in enumerate(ids, 1):
            try:
                r = await backfill_one(session, workflow, pid, paper_index)
            except Exception as e:
                r = {"paper_id": str(pid), "error": str(e)[:200]}
            results.append(r)
            logger.info("[%d/%d] %s", i, len(ids), r)

        # Final aggregate (catches any rows that materialize_for_paper missed)
        agg = await materialize_all(session)
        logger.info("=== DONE ===\nbackfill: %d papers\naggregate: %s",
                    len(ids), agg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--only-materialize", action="store_true",
                        help="Skip analysis_agent; just (re)materialize existing rows")
    args = parser.parse_args()
    asyncio.run(main(args.limit, args.only_materialize))
