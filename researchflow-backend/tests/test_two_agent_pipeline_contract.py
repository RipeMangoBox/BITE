from backend.services.agent_runner import AgentRunner
from backend.services.context_pack_builder import ContextPackBuilder
from backend.services.ingest_workflow import IngestWorkflow

REPO_ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
inspect = __import__("inspect")


def test_active_agent_and_pack_contract_is_two_agent_only():
    assert set(AgentRunner.AGENT_PROMPTS) == {"analysis_agent", "writer_agent"}
    assert set(ContextPackBuilder.PACK_CONFIGS) == {"analysis_agent", "writer_agent"}
    assert "shallow_extractor" in AgentRunner.LEGACY_AGENT_PROMPTS
    assert "paper_report" in AgentRunner.LEGACY_AGENT_PROMPTS
    assert "deep_analyzer" in ContextPackBuilder.LEGACY_PACK_CONFIGS
    assert "paper_report" in ContextPackBuilder.LEGACY_PACK_CONFIGS


def test_analysis_projection_writes_materialization_compat_items_only():
    analysis = {
        "analysis_truth": {"core_insight": "truth"},
        "paper_essence": {
            "problem_statement": "problem",
            "core_claim": "claim",
            "method_summary": "method",
            "evidence_refs": [{"claim": "e", "confidence": 0.9}],
        },
        "method_delta": {
            "proposed_method_name": "M",
            "changed_slots": [{"slot_name": "objective", "is_novel": True}],
        },
        "reference_role_map": {"classifications": [], "anchor_baselines": []},
        "deep_analysis": {"method": {}, "experiment": {}, "formulas": {}},
        "graph_candidates": {"node_candidates": [], "edge_candidates": []},
        "kb_profiles": {"node_profiles": [], "edge_profiles": []},
    }

    projected = IngestWorkflow._analysis_projection(analysis)

    assert set(projected) == {
        "shallow_extract",
        "reference_role_map",
        "deep_analysis",
        "graph_candidates",
        "kb_profiles",
    }
    assert projected["shallow_extract"]["paper_essence"]["core_claim"] == "claim"
    assert projected["shallow_extract"]["method_delta"]["proposed_method_name"] == "M"
    assert projected["reference_role_map"] == analysis["reference_role_map"]
    assert projected["deep_analysis"] == analysis["deep_analysis"]


def test_no_disabled_agent_runtime_calls_remain():
    disabled = {
        "shallow_extractor",
        "reference_role",
        "deep_analyzer",
        "graph_candidate",
        "kb_profiler",
        "paper_report",
        "node_profile",
    }
    offenders = []
    for root in ("backend", "scripts"):
        for path in (REPO_ROOT / root).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            for name in disabled:
                if f'run_agent("{name}"' in text or f"run_agent('{name}'" in text:
                    offenders.append(f"{path.relative_to(REPO_ROOT)}:{name}")
                if f'build("{name}"' in text or f"build('{name}'" in text:
                    offenders.append(f"{path.relative_to(REPO_ROOT)}:{name}")
    assert offenders == []


def test_writer_pack_uses_latest_verified_items_and_lineage_context():
    writer_pack = ContextPackBuilder.PACK_CONFIGS["writer_agent"]
    assert "lineage_positioning_context" in writer_pack["paper"]
    assert writer_pack["run"] == ["ALL_VERIFIED"]

    text = (REPO_ROOT / "backend/services/context_pack_builder.py").read_text(
        encoding="utf-8"
    )
    assert ".order_by(AgentBlackboardItem.created_at.desc())" in text
    assert "seen_item_types" in text
    assert "Lineage Positioning Context" in text


def test_force_reanalyze_contract_is_explicit_only():
    sig = inspect.signature(IngestWorkflow.run_for_existing_paper)
    assert "force_reanalyze" in sig.parameters
    assert sig.parameters["force_reanalyze"].default is False

    deep_sig = inspect.signature(IngestWorkflow.deep_ingest)
    assert "force_reanalyze" in deep_sig.parameters
    assert deep_sig.parameters["force_reanalyze"].default is False

    script = (REPO_ROOT / "scripts/reanalyze_and_compare.py").read_text(
        encoding="utf-8"
    )
    assert "force_reanalyze=True" in script
