"""Node profile generation and management.

Generates structured profiles for T/M/C/D/L/Lab nodes from DB evidence.
"""

import logging
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.kb import KBNodeProfile

logger = logging.getLogger(__name__)


async def generate_profile(
    session: AsyncSession,
    entity_type: str,
    entity_id: UUID,
    *,
    force_refresh: bool = False,
    lang: str = "zh",
) -> KBNodeProfile:
    """Generate or refresh a wiki-style profile for a KB node.

    Checks for an existing non-stale profile first (unless *force_refresh*).
    Gathers context from connected papers, edges, and evidence, then produces
    a conservative deterministic profile. The former node_profile agent is no
    longer an active ResearchFlow agent.

    Returns the saved / updated :class:`KBNodeProfile` row.
    """
    if not force_refresh:
        existing = await get_profile(session, entity_type, entity_id, lang=lang)
        if existing is not None and existing.staleness_trigger_count == 0:
            logger.debug(
                "Profile for %s/%s already fresh, skipping regeneration",
                entity_type, entity_id,
            )
            return existing

    # ── Gather context ──────────────────────────────────────────────────
    run_items = await _gather_node_context(session, entity_type, entity_id)

    result = _profile_from_context(entity_type, entity_id, run_items)

    # ── Persist ─────────────────────────────────────────────────────────
    profile = await get_profile(session, entity_type, entity_id, lang=lang)

    if profile is None:
        profile = KBNodeProfile(
            entity_type=entity_type,
            entity_id=entity_id,
            lang=lang,
            profile_kind="page",
        )
        session.add(profile)

    profile.one_liner = result.get("one_liner")
    profile.short_intro_md = result.get("short_intro_md")
    profile.detailed_md = result.get("detailed_md")
    profile.structured_json = result.get("structured_json")
    profile.evidence_refs = result.get("evidence_refs")
    profile.model_name = "deterministic_profile"
    profile.prompt_version = "v1_two_agent_cleanup"
    profile.staleness_trigger_count = 0
    profile.profile_version = (profile.profile_version or 0) + 1
    profile.review_status = "auto"

    await session.flush()
    logger.info(
        "Generated profile v%d for %s/%s",
        profile.profile_version, entity_type, entity_id,
    )
    return profile


async def increment_staleness(
    session: AsyncSession,
    entity_type: str,
    entity_id: UUID,
) -> int:
    """Increment the staleness trigger count on a node profile.

    Called when new evidence or edges are added that could change the
    profile content.  Returns the new trigger count (0 if no profile
    exists yet).
    """
    profile = await get_profile(session, entity_type, entity_id)
    if profile is None:
        return 0

    profile.staleness_trigger_count = (profile.staleness_trigger_count or 0) + 1
    await session.flush()
    logger.debug(
        "Staleness for %s/%s incremented to %d",
        entity_type, entity_id, profile.staleness_trigger_count,
    )
    return profile.staleness_trigger_count


async def refresh_stale_profiles(
    session: AsyncSession,
    *,
    threshold: int = 3,
    limit: int = 20,
) -> int:
    """Find and regenerate profiles whose staleness count >= *threshold*.

    Returns the number of profiles refreshed.
    """
    rows = (
        await session.execute(
            select(KBNodeProfile.entity_type, KBNodeProfile.entity_id, KBNodeProfile.lang)
            .where(KBNodeProfile.staleness_trigger_count >= threshold)
            .order_by(KBNodeProfile.staleness_trigger_count.desc())
            .limit(limit)
        )
    ).all()

    count = 0
    for row in rows:
        try:
            await generate_profile(
                session,
                row.entity_type,
                row.entity_id,
                force_refresh=True,
                lang=row.lang,
            )
            count += 1
        except Exception:
            logger.exception(
                "Failed to refresh profile for %s/%s",
                row.entity_type, row.entity_id,
            )

    logger.info("Refreshed %d / %d stale profiles", count, len(rows))
    return count


async def get_profile(
    session: AsyncSession,
    entity_type: str,
    entity_id: UUID,
    lang: str = "zh",
) -> KBNodeProfile | None:
    """Look up an existing profile by entity type/id and language."""
    return (
        await session.execute(
            select(KBNodeProfile).where(
                KBNodeProfile.entity_type == entity_type,
                KBNodeProfile.entity_id == entity_id,
                KBNodeProfile.lang == lang,
                KBNodeProfile.profile_kind == "page",
            )
        )
    ).scalar_one_or_none()


# ── Private Helpers ─────────────────────────────────────────────────────


def _profile_from_context(entity_type: str, entity_id: UUID, run_items: dict) -> dict:
    metadata = run_items.get("node_metadata") or {}
    papers = run_items.get("connected_papers") or []
    edges = run_items.get("connected_edges") or []

    name = metadata.get("name") or metadata.get("name_zh") or str(entity_id)
    label = metadata.get("name_zh") or name
    node_type = metadata.get("node_type") or entity_type
    evidence_count = len(papers)

    venues: list[str] = []
    for paper in papers:
        venue = (paper.get("venue") or "").strip()
        if venue and venue not in venues:
            venues.append(venue)
    venue_text = "，主要来源：" + "、".join(venues[:3]) if venues else ""

    one_liner = f"{label} 是一个 {node_type} 知识节点，目前由 {evidence_count} 篇论文支撑。"
    intro = f"{one_liner}{venue_text}"
    if metadata.get("one_liner"):
        intro += f"\n\n{metadata['one_liner']}"

    paper_lines = []
    for paper in papers[:10]:
        title = (paper.get("title") or "").strip()
        if not title:
            continue
        suffix_parts = [str(v) for v in (paper.get("venue"), paper.get("year")) if v]
        suffix = f" ({', '.join(suffix_parts)})" if suffix_parts else ""
        paper_lines.append(f"- {title}{suffix}")

    edge_lines = []
    for edge in edges[:10]:
        relation = edge.get("relation_type") or "related_to"
        target = edge.get("target_type") or edge.get("source_type") or "node"
        edge_lines.append(f"- {relation}: {target}")

    detailed_parts = ["## 支撑论文\n", "\n".join(paper_lines) if paper_lines else "暂无已连接论文。"]
    if edge_lines:
        detailed_parts.extend(["\n\n## 关联关系\n", "\n".join(edge_lines)])

    return {
        "one_liner": one_liner,
        "short_intro_md": intro,
        "detailed_md": "".join(detailed_parts),
        "structured_json": {
            "profile_source": "deterministic_db_evidence",
            "entity_type": entity_type,
            "node_type": node_type,
            "paper_count": evidence_count,
            "edge_count": len(edges),
        },
        "evidence_refs": {
            "papers": [
                {
                    "paper_id": p.get("paper_id"),
                    "title": p.get("title"),
                    "venue": p.get("venue"),
                    "year": p.get("year"),
                }
                for p in papers[:10]
            ],
            "edges": edges[:10],
        },
    }


async def _gather_node_context(
    session: AsyncSession,
    entity_type: str,
    entity_id: UUID,
) -> dict:
    """Build run_items dict with node metadata, connected papers, and edges.

    This populates node_metadata, connected_papers, and connected_edges for
    deterministic profile rendering.
    """
    import json

    from backend.models.kb import GraphEdgeCandidate, GraphNodeCandidate

    run_items: dict = {}

    # ── Node metadata ───────────────────────────────────────────────────
    # Try graph_node_candidates first (staging area)
    node_row = (
        await session.execute(
            select(
                GraphNodeCandidate.name,
                GraphNodeCandidate.name_zh,
                GraphNodeCandidate.node_type,
                GraphNodeCandidate.one_liner,
                GraphNodeCandidate.evidence_refs,
            ).where(
                GraphNodeCandidate.promoted_entity_type == entity_type,
                GraphNodeCandidate.promoted_entity_id == entity_id,
            )
            .limit(1)
        )
    ).first()

    if node_row:
        run_items["node_metadata"] = {
            "name": node_row.name,
            "name_zh": node_row.name_zh,
            "node_type": node_row.node_type,
            "one_liner": node_row.one_liner,
            "evidence_refs": node_row.evidence_refs,
        }
    else:
        # Fallback: construct minimal metadata from entity_type
        run_items["node_metadata"] = {
            "entity_type": entity_type,
            "entity_id": str(entity_id),
        }

    # ── Connected edges ─────────────────────────────────────────────────
    edge_rows = (
        await session.execute(
            select(
                GraphEdgeCandidate.source_entity_type,
                GraphEdgeCandidate.target_entity_type,
                GraphEdgeCandidate.relation_type,
                GraphEdgeCandidate.slot_name,
                GraphEdgeCandidate.one_liner,
                GraphEdgeCandidate.confidence_score,
            ).where(
                (
                    (GraphEdgeCandidate.source_entity_type == entity_type)
                    & (GraphEdgeCandidate.source_entity_id == entity_id)
                )
                | (
                    (GraphEdgeCandidate.target_entity_type == entity_type)
                    & (GraphEdgeCandidate.target_entity_id == entity_id)
                )
            )
            .where(GraphEdgeCandidate.status != "rejected")
            .order_by(GraphEdgeCandidate.confidence_score.desc().nullslast())
            .limit(30)
        )
    ).all()

    run_items["connected_edges"] = [
        {
            "source_type": e.source_entity_type,
            "target_type": e.target_entity_type,
            "relation_type": e.relation_type,
            "slot_name": e.slot_name,
            "one_liner": e.one_liner,
            "confidence": e.confidence_score,
        }
        for e in edge_rows
    ]

    # ── Connected papers ────────────────────────────────────────────────
    paper_ids_from_nodes = (
        await session.execute(
            select(GraphNodeCandidate.paper_id)
            .where(
                GraphNodeCandidate.promoted_entity_type == entity_type,
                GraphNodeCandidate.promoted_entity_id == entity_id,
                GraphNodeCandidate.paper_id.isnot(None),
            )
            .limit(10)
        )
    ).scalars().all()

    from backend.models.paper import Paper

    if paper_ids_from_nodes:
        papers = (
            await session.execute(
                select(Paper.id, Paper.title, Paper.venue, Paper.year)
                .where(Paper.id.in_(paper_ids_from_nodes))
            )
        ).all()
        run_items["connected_papers"] = [
            {
                "paper_id": str(p.id),
                "title": p.title,
                "venue": p.venue,
                "year": p.year,
            }
            for p in papers
        ]
    else:
        run_items["connected_papers"] = []

    return run_items
