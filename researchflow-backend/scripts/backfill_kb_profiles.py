"""Backfill kb_node_profiles for taxonomy_nodes that have none.

For existing taxonomy nodes (loaded by an earlier pipeline), synthesize a
conservative profile from each node plus papers attached via paper_facets.

Usage:
    python -m scripts.backfill_kb_profiles                  # all unprofiled nodes
    python -m scripts.backfill_kb_profiles --batch-size 8   # tune batch
    python -m scripts.backfill_kb_profiles --limit 30       # cap total nodes
    python -m scripts.backfill_kb_profiles --dry-run        # don't write DB
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import time
from typing import Any
from uuid import UUID

from sqlalchemy import text

from backend.database import async_session
from backend.models.kb import KBNodeProfile

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


SQL_UNPROFILED_NODES = text("""
    SELECT t.id, t.name, t.name_zh, t.dimension, t.description
    FROM taxonomy_nodes t
    LEFT JOIN kb_node_profiles p
      ON p.entity_type = 'taxonomy_node' AND p.entity_id = t.id AND p.lang = 'zh'
    WHERE p.id IS NULL
    ORDER BY t.dimension, t.name
""")

SQL_NODE_PAPERS = text("""
    SELECT p.id, p.title, p.venue, p.year, dc.delta_statement
    FROM paper_facets f
    JOIN papers p ON p.id = f.paper_id
    LEFT JOIN delta_cards dc ON dc.id = p.current_delta_card_id
    WHERE f.node_id = :node_id
      AND p.state NOT IN ('skip', 'archived_or_expired')
    ORDER BY p.year DESC NULLS LAST
    LIMIT 8
""")


def _node_to_candidate(node, papers: list[Any]) -> dict:
    """Build a synthetic candidate from DB evidence."""
    connected = []
    for p in papers:
        ds = (p.delta_statement or "").strip()
        if ds.lower().startswith("analysis of paper "):
            ds = ""
        connected.append({
            "title": (p.title or "")[:200],
            "venue": p.venue or "",
            "year": p.year,
            "claim": ds[:240] if ds else "",
        })
    return {
        "name": node.name,
        "name_zh": node.name_zh,
        "node_type": node.dimension,
        "existing_description": (node.description or "")[:400],
        "connected_papers": connected,
        "evidence_count": len(connected),
    }


def _profile_from_candidate(candidate: dict) -> dict:
    name = (candidate.get("name") or "").strip()
    label = (candidate.get("name_zh") or name or "未命名节点").strip()
    node_type = candidate.get("node_type") or "taxonomy"
    connected = candidate.get("connected_papers") or []
    evidence_count = candidate.get("evidence_count") or len(connected)
    description = (candidate.get("existing_description") or "").strip()

    venues = []
    for paper in connected:
        venue = (paper.get("venue") or "").strip()
        if venue and venue not in venues:
            venues.append(venue)
    venue_text = "，主要来源：" + "、".join(venues[:3]) if venues else ""

    one_liner = f"{label} 是一个 {node_type} 知识节点，目前由 {evidence_count} 篇论文支撑。"
    intro = f"{one_liner}{venue_text}"
    if description:
        intro += f"\n\n{description}"

    evidence_lines = []
    for paper in connected[:8]:
        title = (paper.get("title") or "").strip()
        claim = (paper.get("claim") or "").strip()
        if not title:
            continue
        suffix = f"：{claim}" if claim else ""
        evidence_lines.append(f"- {title}{suffix}")
    detailed = "## 支撑论文\n\n" + ("\n".join(evidence_lines) if evidence_lines else "暂无已连接论文。")

    return {
        "node_name": name,
        "one_liner": one_liner,
        "short_intro_md": intro,
        "detailed_md": detailed,
        "structured_json": {
            "profile_source": "deterministic_db_evidence",
            "node_type": node_type,
            "evidence_count": evidence_count,
        },
        "evidence_refs": [
            {
                "title": p.get("title"),
                "venue": p.get("venue"),
                "year": p.get("year"),
                "basis": "paper_facets",
            }
            for p in connected[:8]
        ],
    }


async def _persist_profile(session, node_id: UUID, np: dict, run_id: UUID | None) -> None:
    """Upsert a single kb_node_profiles row for a taxonomy node."""
    profile = KBNodeProfile(
        entity_type="taxonomy_node",
        entity_id=node_id,
        lang="zh",
        one_liner=np.get("one_liner"),
        short_intro_md=np.get("short_intro_md"),
        detailed_md=np.get("detailed_md"),
        structured_json=np.get("structured_json"),
        evidence_refs=np.get("evidence_refs"),
        generated_by_run_id=run_id,
        model_name="deterministic_profile",
        prompt_version="v1_two_agent_cleanup",
    )
    session.add(profile)


async def main(batch_size: int, limit: int | None, dry_run: bool) -> None:
    async with async_session() as session:
        nodes = (await session.execute(SQL_UNPROFILED_NODES)).fetchall()
        if limit:
            nodes = nodes[:limit]
        logger.info("Found %d unprofiled taxonomy nodes (batch=%d, dry=%s)",
                    len(nodes), batch_size, dry_run)
        if not nodes:
            return

        # Pre-load papers for every node so we batch the LLM calls
        node_with_candidates: list[tuple[Any, dict]] = []
        for n in nodes:
            papers = (await session.execute(SQL_NODE_PAPERS, {"node_id": str(n.id)})).fetchall()
            node_with_candidates.append((n, _node_to_candidate(n, papers)))

        total_persisted = 0

        for i in range(0, len(node_with_candidates), batch_size):
            batch = node_with_candidates[i:i + batch_size]
            t0 = time.monotonic()
            logger.info("Batch %d-%d / %d: deterministic profile build",
                        i, i + len(batch), len(node_with_candidates))

            run_id = None  # AgentRunner already created an AgentRun, but
            # the id isn't returned; leaving NULL is acceptable.

            persisted = 0
            for node, candidate in batch:
                np = _profile_from_candidate(candidate)
                if not dry_run:
                    await _persist_profile(session, node.id, np, run_id)
                persisted += 1

            if not dry_run:
                await session.commit()
            total_persisted += persisted
            logger.info("Batch done in %.1fs — persisted %d/%d profiles",
                        time.monotonic() - t0, persisted, len(batch))

        logger.info("=== DONE: persisted=%d total=%d ===",
                    total_persisted, len(node_with_candidates))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=6)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    asyncio.run(main(args.batch_size, args.limit, args.dry_run))
