"""Backfill dataset paper_facets from current deep_analysis blackboard items.

Use this when existing current reports already mention datasets, but
paper_facets.dataset was missed because older materialization only read
`benchmark` and ignored `benchmark_name` / `dataset_name`.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from sqlalchemy import select

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.database import async_session
from backend.models.agent import AgentBlackboardItem
from backend.models.paper import Paper
from backend.models.taxonomy import PaperFacet, TaxonomyNode


def _dataset_names_from_deep(value_json: dict) -> list[str]:
    experiment = (value_json or {}).get("experiment") or {}
    results = experiment.get("main_results") or []
    out: list[str] = []
    seen: set[str] = set()
    for result in results[:12]:
        if not isinstance(result, dict):
            continue
        for key in ("dataset_name", "benchmark", "benchmark_name", "dataset"):
            name = (result.get(key) or "").strip()
            if name and name not in seen:
                seen.add(name)
                out.append(name)
    return out


async def _get_or_create_taxnode(session, name: str) -> TaxonomyNode:
    existing = (
        await session.execute(
            select(TaxonomyNode).where(
                TaxonomyNode.dimension == "dataset",
                TaxonomyNode.name == name,
            ).limit(1)
        )
    ).scalar_one_or_none()
    if existing:
        return existing

    node = TaxonomyNode(
        name=name[:200],
        dimension="dataset",
        description="Backfilled from deep_analysis.main_results",
        status="candidate",
    )
    session.add(node)
    await session.flush()
    return node


async def main() -> None:
    async with async_session() as session:
        papers = (
            await session.execute(
                select(Paper).where(
                    Paper.venue == "ICLR",
                    Paper.year == 2026,
                    Paper.source == "resmax_manifest",
                )
            )
        ).scalars().all()

        added = 0
        for paper in papers:
            bb = (
                await session.execute(
                    select(AgentBlackboardItem)
                    .where(
                        AgentBlackboardItem.paper_id == paper.id,
                        AgentBlackboardItem.item_type == "deep_analysis",
                    )
                    .order_by(AgentBlackboardItem.created_at.desc())
                    .limit(1)
                )
            ).scalar_one_or_none()
            if not bb or not bb.value_json:
                continue

            for ds_name in _dataset_names_from_deep(bb.value_json):
                node = await _get_or_create_taxnode(session, ds_name)
                exists = (
                    await session.execute(
                        select(PaperFacet).where(
                            PaperFacet.paper_id == paper.id,
                            PaperFacet.node_id == node.id,
                            PaperFacet.facet_role == "dataset",
                        ).limit(1)
                    )
                ).scalar_one_or_none()
                if exists:
                    continue
                session.add(PaperFacet(
                    paper_id=paper.id,
                    node_id=node.id,
                    facet_role="dataset",
                    source="deep_analysis_backfill",
                ))
                added += 1

        await session.commit()
        print(f"dataset_facets_added={added}")


if __name__ == "__main__":
    asyncio.run(main())
