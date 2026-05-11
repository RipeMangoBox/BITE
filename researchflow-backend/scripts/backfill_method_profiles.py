"""Backfill kb_node_profiles for method_nodes that have none.

Mirrors backfill_kb_profiles.py but for method_nodes:
  * Pulls each unprofiled method
  * Gathers up to 6 papers that use that method (via Paper.method_family match)
  * Builds a conservative deterministic profile from DB evidence
  * Persists short_intro_md + structured_json

The vault method page already prefers `kb_node_profiles.short_intro_md`
when present, so this immediately swaps the auto-skeleton for a real intro.

Usage:
    python -m scripts.backfill_method_profiles
    python -m scripts.backfill_method_profiles --batch-size 6
    python -m scripts.backfill_method_profiles --limit 20
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import re
import time
from uuid import UUID

from sqlalchemy import text as sa_text

from backend.database import async_session
from backend.models.kb import KBNodeProfile

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


SQL_UNPROFILED_METHODS = sa_text("""
    SELECT m.id, m.name, m.name_zh, m.type, m.maturity, m.domain, m.description
    FROM method_nodes m
    LEFT JOIN kb_node_profiles p
      ON p.entity_type = 'method_node' AND p.entity_id = m.id AND p.lang = 'zh'
    WHERE p.id IS NULL
    ORDER BY m.created_at DESC
""")


def _method_canonical(name: str) -> str:
    s = (name or "").strip()
    s = re.sub(r"\s*\(.*\)\s*$", "", s)
    return s.strip() or name


SQL_METHOD_PAPERS = sa_text("""
    SELECT p.id, p.title, p.venue, p.year,
           dc.delta_statement
    FROM papers p
    LEFT JOIN delta_cards dc ON dc.id = p.current_delta_card_id
    WHERE lower(p.method_family) = lower(:n_full)
       OR lower(p.method_family) LIKE lower(:n_prefix) || '%'
    LIMIT 6
""")


def _build_candidate(method_row, papers) -> dict:
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
        "name": method_row.name,
        "name_zh": method_row.name_zh,
        "node_type": "method",
        "method_type": method_row.type,
        "maturity": method_row.maturity,
        "domain": method_row.domain if (method_row.domain and not method_row.domain.startswith("__")) else None,
        "existing_description": (method_row.description or "")[:400],
        "connected_papers": connected,
        "evidence_count": len(connected),
    }


def _profile_from_candidate(candidate: dict) -> dict:
    name = (candidate.get("name") or "").strip()
    label = (candidate.get("name_zh") or name or "未命名方法").strip()
    connected = candidate.get("connected_papers") or []
    evidence_count = candidate.get("evidence_count") or len(connected)
    domain = candidate.get("domain") or candidate.get("method_type") or "研究方法"
    description = (candidate.get("existing_description") or "").strip()

    venues = []
    for paper in connected:
        venue = (paper.get("venue") or "").strip()
        if venue and venue not in venues:
            venues.append(venue)
    venue_text = "，主要来源：" + "、".join(venues[:3]) if venues else ""

    one_liner = f"{label} 是一个方法节点，目前由知识库中 {evidence_count} 篇论文支撑。"
    intro = f"{one_liner}{venue_text}"
    if description:
        intro += f"\n\n{description}"

    evidence_lines = []
    for paper in connected[:6]:
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
            "node_type": "method",
            "method_type": candidate.get("method_type"),
            "domain": candidate.get("domain"),
            "evidence_count": evidence_count,
        },
        "evidence_refs": [
            {
                "title": p.get("title"),
                "venue": p.get("venue"),
                "year": p.get("year"),
                "basis": "connected_papers",
            }
            for p in connected[:6]
        ],
    }


async def _persist(session, method_id: UUID, np: dict) -> None:
    profile = KBNodeProfile(
        entity_type="method_node",
        entity_id=method_id,
        lang="zh",
        one_liner=np.get("one_liner"),
        short_intro_md=np.get("short_intro_md"),
        detailed_md=np.get("detailed_md"),
        structured_json=np.get("structured_json"),
        evidence_refs=np.get("evidence_refs"),
        model_name="deterministic_profile",
        prompt_version="v1_two_agent_cleanup",
    )
    session.add(profile)


async def main(batch_size: int, limit: int | None, dry_run: bool) -> None:
    async with async_session() as session:
        methods = (await session.execute(SQL_UNPROFILED_METHODS)).fetchall()
        if limit:
            methods = methods[:limit]
        logger.info("Found %d unprofiled methods (batch=%d, dry=%s)",
                    len(methods), batch_size, dry_run)
        if not methods:
            return

        # Pre-load each method's papers (sync against method_family)
        per_method = []
        for m in methods:
            cname = _method_canonical(m.name)
            papers = (await session.execute(SQL_METHOD_PAPERS, {
                "n_full": m.name, "n_prefix": cname,
            })).fetchall()
            per_method.append((m, papers))

        total_persisted = 0
        for i in range(0, len(per_method), batch_size):
            batch = per_method[i:i + batch_size]
            t0 = time.monotonic()
            logger.info("Batch %d-%d / %d", i, i + len(batch), len(per_method))

            for m, _papers in batch:
                np = _profile_from_candidate(_build_candidate(m, _papers))
                if not dry_run:
                    await _persist(session, m.id, np)
                total_persisted += 1
            if not dry_run:
                await session.commit()
            logger.info("Batch %.1fs persisted=%d", time.monotonic() - t0, total_persisted)

        logger.info("=== DONE: persisted=%d/%d ===", total_persisted, len(methods))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--batch-size", type=int, default=6)
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    asyncio.run(main(args.batch_size, args.limit, args.dry_run))
