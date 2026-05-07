"""Re-analyze papers with existing L4 analysis and compare old vs new results.

Usage:
    python scripts/reanalyze_and_compare.py [--paper-id UUID] [--limit N] [--dry-run]

Workflow:
    1. Snapshot current paper state (before)
    2. Run IngestWorkflow.run_for_existing_paper() — fresh analysis
    3. Snapshot new paper state (after)
    4. Diff and report improvements/regressions
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path
from datetime import datetime, timezone
from uuid import UUID

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("reanalyze_compare")


# ── Snapshot ────────────────────────────────────────────────────────

async def snapshot_paper(session, paper_id: UUID) -> dict:
    """Capture all pipeline outputs for a paper as a JSON-serializable dict."""
    from sqlalchemy import text

    snap = {"paper_id": str(paper_id), "snapshot_at": datetime.now(timezone.utc).isoformat()}

    # ── Paper metadata ──
    row = (await session.execute(text("""
        SELECT title, state, ring, role_in_kb, method_family,
               current_delta_card_id IS NOT NULL as has_dc,
               acceptance_type, cited_by_count
        FROM papers WHERE id = :pid
    """), {"pid": paper_id})).fetchone()
    if not row:
        return {"error": "not found", "paper_id": str(paper_id)}
    snap["title"] = row.title[:120]
    snap["state"] = row.state
    snap["ring"] = row.ring
    snap["role_in_kb"] = row.role_in_kb
    snap["method_family"] = row.method_family
    snap["has_delta_card"] = row.has_dc
    snap["acceptance_type"] = row.acceptance_type
    snap["cited_by_count"] = row.cited_by_count

    # ── L2 Parse ──
    row = (await session.execute(text("""
        SELECT prompt_version, schema_version,
               extracted_sections IS NOT NULL as has_secs,
               extracted_formulas IS NOT NULL as has_formulas
        FROM paper_analyses
        WHERE paper_id = :pid AND level = 'l2_parse' AND is_current = true
    """), {"pid": paper_id})).fetchone()
    snap["l2"] = {
        "has_sections": row.has_secs if row else False,
        "has_formulas": row.has_formulas if row else False,
        "prompt_version": row.prompt_version if row else None,
    }

    # ── L4 Deep ──
    row = (await session.execute(text("""
        SELECT prompt_version, schema_version, confidence,
               full_report_md IS NOT NULL as has_report,
               char_length(full_report_md) as report_len
        FROM paper_analyses
        WHERE paper_id = :pid AND level = 'l4_deep' AND is_current = true
    """), {"pid": paper_id})).fetchone()
    snap["l4"] = {
        "has_report": row.has_report if row else False,
        "report_len": row.report_len if row else 0,
        "prompt_version": row.prompt_version if row else None,
        "confidence": float(row.confidence) if row and row.confidence else None,
    }

    # ── Agent blackboard ──
    rows = (await session.execute(text("""
        SELECT item_type, count(*) as cnt, bool_or(is_verified) as any_verified
        FROM agent_blackboard_items
        WHERE paper_id = :pid
        GROUP BY item_type ORDER BY item_type
    """), {"pid": paper_id})).fetchall()
    snap["blackboard"] = {
        r.item_type: {"count": r.cnt, "any_verified": r.any_verified}
        for r in rows
    }

    # ── DeltaCards ──
    rows = (await session.execute(text("""
        SELECT status, publish_status, structurality_score,
               evidence_count, evidence_refs IS NOT NULL as has_refs,
               extraction_confidence, linkage_confidence, evidence_confidence
        FROM delta_cards WHERE paper_id = :pid ORDER BY created_at DESC
    """), {"pid": paper_id})).fetchall()
    snap["delta_cards"] = [
        {
            "status": r.status,
            "publish_status": r.publish_status,
            "structurality_score": float(r.structurality_score) if r.structurality_score else None,
            "evidence_count": r.evidence_count,
            "has_refs": r.has_refs,
            "extraction_confidence": float(r.extraction_confidence) if r.extraction_confidence else None,
            "linkage_confidence": float(r.linkage_confidence) if r.linkage_confidence else None,
            "evidence_confidence": float(r.evidence_confidence) if r.evidence_confidence else None,
        }
        for r in rows
    ]

    # ── Evidence units ──
    row = (await session.execute(text("""
        SELECT count(*) as total,
               count(*) FILTER (WHERE basis = 'experiment_backed') as experiment,
               count(*) FILTER (WHERE basis = 'text_stated') as text_stated,
               avg(confidence) as avg_conf
        FROM evidence_units WHERE paper_id = :pid
    """), {"pid": paper_id})).fetchone()
    snap["evidence"] = {
        "total": row.total,
        "experiment_backed": row.experiment,
        "text_stated": row.text_stated,
        "avg_confidence": round(float(row.avg_conf), 3) if row.avg_conf else None,
    }

    # ── Graph assertions ──
    row = (await session.execute(text("""
        SELECT count(*) as total,
               count(*) FILTER (WHERE status = 'published') as published,
               count(*) FILTER (WHERE status = 'candidate') as candidate
        FROM graph_assertions ga
        JOIN graph_nodes gn ON ga.from_node_id = gn.id
        WHERE gn.ref_table = 'delta_cards'
          AND gn.ref_id IN (SELECT id FROM delta_cards WHERE paper_id = :pid)
    """), {"pid": paper_id})).fetchone()
    snap["graph_assertions"] = {
        "total": row.total,
        "published": row.published,
        "candidate": row.candidate,
    }

    # ── Paper report ──
    row = (await session.execute(text("""
        SELECT count(*) as total, count(DISTINCT report_id) as reports,
               string_agg(section_type, ',' ORDER BY order_index) as sections
        FROM paper_report_sections prs
        JOIN paper_reports pr ON pr.id = prs.report_id
        WHERE pr.paper_id = :pid
    """), {"pid": paper_id})).fetchone()
    snap["paper_report"] = {
        "reports": row.reports or 0,
        "sections": row.sections or "",
        "section_count": len(row.sections.split(",")) if row.sections else 0,
    }

    # ── Taxonomy facets ──
    row = (await session.execute(text("""
        SELECT count(*) FROM paper_facets WHERE paper_id = :pid
    """), {"pid": paper_id})).scalar()
    snap["taxonomy_facets"] = row or 0

    return snap


# ── Diff ────────────────────────────────────────────────────────────

def diff_snapshots(before: dict, after: dict) -> dict:
    """Compare two snapshots and return a structured diff with scores."""
    if "error" in before or "error" in after:
        return {"error": "snapshot error", "before_error": before.get("error"), "after_error": after.get("error")}

    changes = {}
    scores = {"improvements": [], "regressions": [], "neutral": []}

    def _compare(path, old, new, threshold=0.0, higher_better=True):
        if old == new:
            return None
        if isinstance(old, (int, float)) and isinstance(new, (int, float)):
            delta = new - old
            pct = (delta / max(abs(old), 1)) * 100 if old else float('inf')
            change = {"old": old, "new": new, "delta": delta, "pct_change": round(pct, 1)}
            if abs(delta) > threshold or abs(pct) > 5:
                if (higher_better and delta > threshold) or (not higher_better and delta < -threshold):
                    scores["improvements"].append(f"{path}: {old} → {new} ({delta:+})")
                elif (higher_better and delta < -threshold) or (not higher_better and delta > threshold):
                    scores["regressions"].append(f"{path}: {old} → {new} ({delta:+})")
            else:
                scores["neutral"].append(f"{path}: {old} → {new}")
            return change
        return {"old": old, "new": new}

    b, a = before, after

    # State transitions
    changes["state"] = _compare("state", b.get("state"), a.get("state"))
    changes["ring"] = _compare("ring", b.get("ring"), a.get("ring"))

    # L4 report
    bl4, al4 = b.get("l4", {}), a.get("l4", {})
    changes["l4_report_len"] = _compare("report_length", bl4.get("report_len", 0), al4.get("report_len", 0),
                                         threshold=200, higher_better=True)
    changes["l4_confidence"] = _compare("l4_confidence", bl4.get("confidence") or 0, al4.get("confidence") or 0,
                                         threshold=0.05)

    # DeltaCard
    bdcs, adcs = b.get("delta_cards", []), a.get("delta_cards", [])
    if bdcs and adcs:
        bdc, adc = bdcs[0], adcs[0]
        changes["dc_structurality"] = _compare("structurality", bdc.get("structurality_score") or 0,
                                                adc.get("structurality_score") or 0, threshold=0.1)
        changes["dc_evidence_count"] = _compare("evidence_count", bdc.get("evidence_count", 0),
                                                 adc.get("evidence_count", 0), threshold=1, higher_better=True)
        changes["dc_status"] = _compare("dc_status", bdc.get("status"), adc.get("status"))
        changes["dc_publish_status"] = _compare("dc_publish", bdc.get("publish_status"), adc.get("publish_status"))

    # Evidence
    be, ae = b.get("evidence", {}), a.get("evidence", {})
    changes["evidence_total"] = _compare("evidence_total", be.get("total", 0), ae.get("total", 0),
                                          threshold=0, higher_better=True)
    changes["evidence_exp"] = _compare("evidence_exp_backed", be.get("experiment_backed", 0),
                                        ae.get("experiment_backed", 0), threshold=0, higher_better=True)
    changes["evidence_avg_conf"] = _compare("evidence_avg_conf", be.get("avg_confidence") or 0,
                                             ae.get("avg_confidence") or 0, threshold=0.05)

    # Graph assertions
    bg, ag = b.get("graph_assertions", {}), a.get("graph_assertions", {})
    changes["graph_assertions"] = _compare("graph_assertions", bg.get("total", 0), ag.get("total", 0),
                                            threshold=0, higher_better=True)
    changes["graph_published"] = _compare("graph_published", bg.get("published", 0), ag.get("published", 0),
                                           threshold=0, higher_better=True)

    # Report sections
    br, ar = b.get("paper_report", {}), a.get("paper_report", {})
    changes["report_sections"] = _compare("report_sections", br.get("section_count", 0),
                                           ar.get("section_count", 0), threshold=1)

    # Blackboard
    bb_items = set(b.get("blackboard", {}).keys()) | set(a.get("blackboard", {}).keys())
    for item_type in bb_items:
        bold = b.get("blackboard", {}).get(item_type, {})
        anew = a.get("blackboard", {}).get(item_type, {})
        if bold.get("count", 0) != anew.get("count", 0):
            changes[f"bb_{item_type}"] = _compare(f"bb_{item_type}", bold.get("count", 0),
                                                   anew.get("count", 0), threshold=0)

    # Compute overall score: +1 per improvement, -1 per regression
    changes["_score"] = len(scores["improvements"]) - len(scores["regressions"])
    changes["_improvements"] = scores["improvements"]
    changes["_regressions"] = scores["regressions"]
    changes["_neutral"] = scores["neutral"][:10]  # keep first 10

    return changes


# ── Re-analysis ─────────────────────────────────────────────────────

async def reanalyze_paper(session, paper_id: UUID) -> dict:
    """Run fresh analysis on a paper. Returns pipeline result dict."""
    from backend.services.ingest_workflow import IngestWorkflow

    workflow = IngestWorkflow(session)
    result = await workflow.run_for_existing_paper(paper_id)
    await session.commit()
    return result


# ── Main ────────────────────────────────────────────────────────────

async def main(args):
    from backend.database import async_session
    from sqlalchemy import text

    async with async_session() as session:
        # Find papers with existing L4 analysis
        if args.paper_id:
            paper_ids = [UUID(args.paper_id)]
        else:
            rows = (await session.execute(text("""
                SELECT p.id
                FROM papers p
                JOIN paper_analyses pa ON pa.paper_id = p.id
                    AND pa.level = 'l4_deep' AND pa.is_current = true
                    AND pa.full_report_md IS NOT NULL
                    AND length(pa.full_report_md) > 200
                ORDER BY p.year DESC NULLS LAST, p.title
                LIMIT :limit
            """), {"limit": args.limit})).fetchall()
            paper_ids = [r.id for r in rows]

        logger.info("Found %d papers with L4 analysis", len(paper_ids))
        if not paper_ids:
            logger.warning("No papers with L4 analysis found!")
            return

        results = {}
        summary = {"total": len(paper_ids), "improved": 0, "regressed": 0, "unchanged": 0, "errors": 0}

        for i, pid in enumerate(paper_ids, 1):
            logger.info("[%d/%d] Processing %s", i, len(paper_ids), pid)

            # 1. Snapshot BEFORE
            try:
                before = await snapshot_paper(session, pid)
                if "error" in before:
                    logger.warning("  Skip %s: %s", pid, before["error"])
                    continue
            except Exception as e:
                logger.error("  BEFORE snapshot failed: %s", e)
                continue

            logger.info("  %s | ring=%s state=%s l4=%d chars dc=%d eu=%d",
                        before.get("title", "?")[:40],
                        before.get("ring"), before.get("state"),
                        before.get("l4", {}).get("report_len", 0),
                        len(before.get("delta_cards", [])),
                        before.get("evidence", {}).get("total", 0))

            if args.dry_run:
                results[str(pid)] = {"before": before, "after": None, "diff": None}
                continue

            # 2. Re-analyze (fresh, not referencing old data)
            try:
                pipeline_result = await reanalyze_paper(session, pid)
                if "error" in pipeline_result:
                    logger.error("  Pipeline error: %s", pipeline_result["error"])
                    results[str(pid)] = {"before": before, "after": None,
                                         "error": pipeline_result["error"]}
                    summary["errors"] += 1
                    continue
            except Exception as e:
                logger.error("  Re-analysis failed: %s", e)
                try:
                    await session.rollback()
                except Exception:
                    pass
                results[str(pid)] = {"before": before, "after": None, "error": str(e)[:200]}
                summary["errors"] += 1
                continue

            # 3. Snapshot AFTER
            try:
                after = await snapshot_paper(session, pid)
            except Exception as e:
                logger.error("  AFTER snapshot failed: %s", e)
                after = {"error": str(e)[:200]}

            # 4. Diff
            diff = diff_snapshots(before, after)
            score = diff.get("_score", 0)
            if score > 0:
                summary["improved"] += 1
            elif score < 0:
                summary["regressed"] += 1
            else:
                summary["unchanged"] += 1

            results[str(pid)] = {
                "before": before,
                "after": after,
                "diff": diff,
            }

            # Print one-line status
            impr = len(diff.get("_improvements", []))
            regr = len(diff.get("_regressions", []))
            title_short = before.get("title", "?")[:50]
            logger.info("  → score=%+d | +%d -%d | %s", score, impr, regr, title_short)

        # ── Summary ──
        print("\n" + "=" * 80)
        print("RE-ANALYSIS COMPARISON SUMMARY")
        print("=" * 80)
        print(f"Papers processed: {summary['total']}")
        print(f"  Improved:  {summary['improved']}")
        print(f"  Regressed: {summary['regressed']}")
        print(f"  Unchanged: {summary['unchanged']}")
        print(f"  Errors:    {summary['errors']}")

        # Per-paper detail
        print("\n--- Per-paper scores ---")
        for pid_str, r in sorted(results.items(),
                                 key=lambda kv: kv[1].get("diff", {}).get("_score", -999),
                                 reverse=True):
            diff = r.get("diff", {})
            score = diff.get("_score", "?")
            title = r.get("before", {}).get("title", "?")[:60]
            improv = diff.get("_improvements", [])
            regress = diff.get("_regressions", [])
            err = r.get("error", "")
            status = f"ERROR: {err[:60]}" if err else f"+{len(improv)} -{len(regress)}"
            print(f"  [{score:+}] {status:20s} | {title}")

        # Save full results
        out_path = Path(__file__).resolve().parent / "reanalyze_results.json"
        # Convert UUID keys and non-serializable types
        out_data = {
            "summary": summary,
            "results": results,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out_data, f, ensure_ascii=False, default=str, indent=2)
        logger.info("Results saved to %s", out_path)

        return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Re-analyze papers and compare results")
    parser.add_argument("--paper-id", type=str, help="Single paper UUID to re-analyze")
    parser.add_argument("--limit", type=int, default=5, help="Max papers to process")
    parser.add_argument("--dry-run", action="store_true", help="Only snapshot, don't re-analyze")
    args = parser.parse_args()
    asyncio.run(main(args))
