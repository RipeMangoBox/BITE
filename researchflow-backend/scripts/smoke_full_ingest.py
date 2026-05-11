"""End-to-end smoke runner for promoted venue_papers.

Calls IngestWorkflow.enrich_and_prepare + deep_ingest for each given paper_id,
sequentially. Use this for the first CVPR 2025 batch validation:
  promote_venue_papers → smoke_full_ingest → spot-check vault.

Usage:
    python -m scripts.smoke_full_ingest <paper_id> [<paper_id> ...]
    python -m scripts.smoke_full_ingest --from-file paper_ids.txt
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import time
from uuid import UUID

from backend.database import async_session
from backend.services.ingest_workflow import IngestWorkflow

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


async def _run_reference_role(session, paper_id: UUID) -> dict:
    """Compatibility no-op.

    The smoke path now relies on IngestWorkflow.deep_ingest to run
    analysis_agent and write reference_role_map as a compatibility projection.
    """
    return {"skipped": "handled_by_analysis_agent", "paper_id": str(paper_id)}


async def run_one(paper_id: UUID) -> dict:
    async with async_session() as session:
        wf = IngestWorkflow(session)
        out = {"paper_id": str(paper_id)}
        t0 = time.monotonic()

        try:
            prep = await wf.enrich_and_prepare(paper_id)
            await session.commit()
            out["enrich"] = {k: prep.get(k) for k in ("status", "l2_figures",
                                                       "l2_formulas", "l2_tables",
                                                       "error") if k in prep}
        except Exception as e:
            await session.rollback()
            return {**out, "stage": "enrich", "error": str(e)[:300]}

        # The two-agent workflow writes reference_role_map from analysis_agent
        # during deep_ingest; keep this key in smoke output for old parsers.
        try:
            rr = await _run_reference_role(session, paper_id)
            await session.commit()
            out["reference_role"] = rr
        except Exception as e:
            await session.rollback()
            out["reference_role"] = {"error": str(e)[:200]}

        try:
            deep = await wf.deep_ingest(paper_id)
            await session.commit()
            out["deep"] = {
                "agents_run": deep.get("agents_run"),
                "report_sections": deep.get("report_sections"),
                "nodes_created": deep.get("nodes_created"),
                "edges_created": deep.get("edges_created"),
            }
        except Exception as e:
            await session.rollback()
            return {**out, "stage": "deep", "error": str(e)[:300]}

        out["duration_s"] = round(time.monotonic() - t0, 1)

    # discover_neighborhood needs a FRESH session — deep_ingest's many writes
    # leave the previous session in an error state on any partial failure
    # (synthesize_concepts, baseline_promoter, etc.). Reusing it triggers
    # "transaction has been rolled back" InvalidRequestError on any subsequent
    # query. Open a new session, scoped to this call only.
    async with async_session() as fresh_session:
        try:
            wf2 = IngestWorkflow(fresh_session)
            disc = await wf2.discover_neighborhood(
                paper_id, max_references=30, max_citations=20, max_related=10,
            )
            await fresh_session.commit()
            out["discover"] = {
                "candidates_created": disc.get("candidates_created"),
                "by_source": disc.get("by_source"),
            }
        except Exception as e:
            await fresh_session.rollback()
            out["discover"] = {"warning": str(e)[:200]}

    return out


async def main(paper_ids: list[str]) -> None:
    results = []
    for i, pid in enumerate(paper_ids, 1):
        try:
            uid = UUID(pid)
        except ValueError:
            logger.warning("[%d/%d] invalid UUID: %s", i, len(paper_ids), pid)
            continue
        logger.info("[%d/%d] Ingesting %s", i, len(paper_ids), pid)
        r = await run_one(uid)
        results.append(r)
        logger.info(" → %s", r)

    print("\n=== SUMMARY ===")
    ok = sum(1 for r in results if "error" not in r)
    failed = [r for r in results if "error" in r]
    print(f"OK: {ok}/{len(results)}   FAILED: {len(failed)}")
    for r in failed:
        print(f"  {r['paper_id']} [{r.get('stage', '?')}]: {r.get('error', '')[:200]}")


def _read_id_file(path: str) -> list[str]:
    out = []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith("#"):
                out.append(s)
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("paper_ids", nargs="*")
    parser.add_argument("--from-file", default=None)
    args = parser.parse_args()
    ids = list(args.paper_ids)
    if args.from_file:
        ids.extend(_read_id_file(args.from_file))
    if not ids:
        parser.error("Provide paper_ids or --from-file")
    asyncio.run(main(ids))
