import asyncio
import importlib.util
import json
from argparse import Namespace
from pathlib import Path
import sys


TOOL_ROOT = Path(__file__).resolve().parents[1] / "iclr26_batch" / "tools"

SCRIPT_PATH = TOOL_ROOT / "run_local_paper_analysis.py"
SPEC = importlib.util.spec_from_file_location("run_local_paper_analysis", SCRIPT_PATH)
local_analysis = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = local_analysis
SPEC.loader.exec_module(local_analysis)

BATCH_SCRIPT_PATH = TOOL_ROOT / "run_local_iclr26_batch.py"
BATCH_SPEC = importlib.util.spec_from_file_location("run_local_iclr26_batch", BATCH_SCRIPT_PATH)
local_batch = importlib.util.module_from_spec(BATCH_SPEC)
assert BATCH_SPEC and BATCH_SPEC.loader
sys.modules[BATCH_SPEC.name] = local_batch
BATCH_SPEC.loader.exec_module(local_batch)

PLAN_SCRIPT_PATH = TOOL_ROOT / "plan_iclr26_mineru_batches.py"
PLAN_SPEC = importlib.util.spec_from_file_location("plan_iclr26_mineru_batches", PLAN_SCRIPT_PATH)
plan_batches = importlib.util.module_from_spec(PLAN_SPEC)
assert PLAN_SPEC and PLAN_SPEC.loader
sys.modules[PLAN_SPEC.name] = plan_batches
PLAN_SPEC.loader.exec_module(plan_batches)


def test_split_markdown_keeps_order_and_overlap():
    text = (
        "# Paper\n\n"
        + "A" * 900
        + "\n\n## Method\n\n"
        + "B" * 900
        + "\n\n## Experiments\n\n"
        + "C" * 900
    )

    chunks = local_analysis.split_markdown(text, max_chars=1200, overlap_chars=100)

    assert len(chunks) >= 2
    assert [chunk.index for chunk in chunks] == list(range(1, len(chunks) + 1))
    assert all(chunk.total == len(chunks) for chunk in chunks)
    assert chunks[0].start == 0
    assert chunks[-1].end == len(text.strip())
    assert all(left.start < right.start for left, right in zip(chunks, chunks[1:]))


def test_parse_json_object_repairs_latex_escape():
    parsed = local_analysis.parse_json_object(
        r'{"formula":"\alpha + \beta"}',
        label="latex",
    )

    assert parsed["formula"] == r"\alpha + \beta"


def test_parse_json_object_does_not_double_valid_latex_escape():
    parsed = local_analysis.parse_json_object(
        r'{"formula":"\\alpha"}',
        label="valid_latex",
    )

    assert parsed["formula"] == r"\alpha"


def test_parse_json_object_uses_first_balanced_object():
    parsed = local_analysis.parse_json_object(
        'prefix {"ok": true} trailing {"ignored": true}',
        label="balanced",
    )

    assert parsed == {"ok": True}


def test_parse_json_object_skips_non_json_braces_before_object():
    parsed = local_analysis.parse_json_object(
        'Explanation: $a_{b}$, then JSON: {"ok": true}',
        label="latex_prefix",
    )

    assert parsed == {"ok": True}


def test_normalize_report_markdown_uses_obsidian_latex_delimiters():
    report = (
        "## 核心模块与公式推导\n\n"
        "行内公式 \\(x_t + \\alpha\\)，块级公式：\n"
        "\\[\\mathcal{L}=\\sum_t \\epsilon_t\\]\n"
    )

    normalized = local_analysis.normalize_report_markdown(report)

    assert "$x_t + \\alpha$" in normalized
    assert "$$\n\\mathcal{L}=\\sum_t \\epsilon_t\n$$" in normalized
    assert "\\(" not in normalized
    assert "\\)" not in normalized
    assert "\\[" not in normalized
    assert "\\]" not in normalized


def test_parse_json_object_closes_nested_truncated_part_payload():
    raw = (
        '{"part_id":"2/7","section_role":"experiments","method_evidence":['
        '{"claim":"a","section":"s","anchor":"a","confidence":0.9},'
        '{"claim":"truncated'
    )

    parsed = local_analysis.parse_json_object(raw, label="truncated_part")

    assert parsed["part_id"] == "2/7"
    assert parsed["section_role"] == "experiments"
    assert parsed["method_evidence"][0]["claim"] == "a"


def test_parse_json_object_closes_truncated_payload_after_array_comma():
    raw = (
        '{"part_id":"2","section_role":"experiments","experiment_evidence":['
        '{"claim":"a","table_or_figure":"Figure 8","metric":"LID","value":"2","confidence":0.9},'
    )

    parsed = local_analysis.parse_json_object(raw, label="truncated_array_comma")

    assert parsed["part_id"] == "2"
    assert parsed["experiment_evidence"][0]["table_or_figure"] == "Figure 8"


def test_parse_json_object_prefers_outer_researchflow_schema():
    raw = (
        '{"paper_metadata":{"title":"T","title_zh":"题","venue":null,"year":null},'
        '"analysis_truth":{"core_insight":"x"},'
        '"method":{"proposed_method_name":"m"},'
        '"experiments":{"main_results":[]},'
        '"formulas":[{"name":"truncated'
    )

    parsed = local_analysis.parse_json_object(raw, label="main_truncated")

    assert "paper_metadata" in parsed
    assert "analysis_truth" in parsed
    assert parsed["paper_metadata"]["title"] == "T"


def test_parse_json_object_drops_unfinished_array_item_field():
    raw = (
        '{"paper_metadata":{"title":"T"},'
        '"analysis_truth":{"core_insight":"x"},'
        '"method":{},'
        '"experiments":{},'
        '"formulas":[{"name":"first","latex":"x"}, {"name":'
    )

    parsed = local_analysis.parse_json_object(raw, label="unfinished_array_item")

    assert parsed["paper_metadata"]["title"] == "T"
    assert parsed["formulas"] == [{"name": "first", "latex": "x"}]


def test_resolve_llm_config_defaults_to_deepseek(monkeypatch):
    for key in ["OPENAI_MODEL", "OPENAI_BASE_URL", "OPENAI_API_KEY", "DEEPSEEK_API_KEY"]:
        monkeypatch.delenv(key, raising=False)
    args = Namespace(
        provider="deepseek",
        api_key_env="",
        model="",
        base_url="",
        temperature=0.1,
    )

    local_analysis.resolve_llm_config(args)

    assert args.api_key_env == "DEEPSEEK_API_KEY"
    assert args.model == "deepseek-v4-pro"
    assert args.base_url == "https://api.deepseek.com/v1"


def test_prompt_language_rule_requires_chinese_body_with_exceptions():
    assert "正文/分析内容必须使用简体中文" in local_analysis.MAIN_ANALYSIS_SYSTEM
    assert "正文内容必须使用" in local_analysis.WRITER_SYSTEM
    for term in ["caption", "formulas", "symbols"]:
        assert term in local_analysis.MAIN_ANALYSIS_SYSTEM
        assert term in local_analysis.WRITER_SYSTEM


def test_resolve_llm_config_deepseek_ignores_openai_model_endpoint(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("DEEPSEEK_MODEL", raising=False)
    monkeypatch.delenv("DEEPSEEK_BASE_URL", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "fallback-key")
    monkeypatch.setenv("OPENAI_MODEL", "kimi-k2.6")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.kimi.com/coding/v1")
    args = Namespace(
        provider="deepseek",
        api_key_env="",
        model="",
        base_url="",
        temperature=0.1,
    )

    local_analysis.resolve_llm_config(args)

    assert args.api_key_env == "OPENAI_API_KEY"
    assert args.model == "deepseek-v4-pro"
    assert args.base_url == "https://api.deepseek.com/v1"


def test_deepseek_reasoning_only_for_reasoner_models():
    assert local_analysis.deepseek_uses_reasoning("deepseek-reasoner")
    assert not local_analysis.deepseek_uses_reasoning("deepseek-chat")


def test_batch_force_retries_failed_rows_but_skips_completed():
    assert local_batch.should_skip_existing_status("done", force=True, backfill_vault=False)
    assert not local_batch.should_skip_existing_status("failed", force=True, backfill_vault=False)
    assert local_batch.should_skip_existing_status("failed", force=False, backfill_vault=False)


def write_fake_mineru_output(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "paper.md").write_text("# Paper\n\ncontent", encoding="utf-8")
    (root / "paper_content_list.json").write_text("[]", encoding="utf-8")


def test_batch_discovers_direct_mineru_output(tmp_path):
    out = tmp_path / "mineru_outputs" / "iclr26_0009" / "abc123"
    write_fake_mineru_output(out)
    args = Namespace(mineru_output_root=str(tmp_path / "mineru_outputs"))
    row = local_batch.BatchRow(
        batch_id="iclr26_0009",
        title="T",
        openreview_forum_id="abc123",
        path=str(tmp_path / "paper.pdf"),
    )

    discovered = local_batch.discover_mineru_output(args, row)

    assert discovered == out.resolve()


def test_batch_discovers_forum_id_across_batch_dirs(tmp_path):
    out = tmp_path / "mineru_outputs" / "other_batch" / "abc123"
    write_fake_mineru_output(out)
    args = Namespace(mineru_output_root=str(tmp_path / "mineru_outputs"))
    row = local_batch.BatchRow(
        batch_id="iclr26_0009",
        title="T",
        openreview_forum_id="abc123",
        path=str(tmp_path / "paper.pdf"),
    )

    discovered = local_batch.discover_mineru_output(args, row)

    assert discovered == out.resolve()


def test_batch_does_not_reuse_incomplete_mineru_output(tmp_path):
    out = tmp_path / "mineru_outputs" / "iclr26_0009" / "abc123"
    out.mkdir(parents=True)
    (out / "paper.md").write_text("# Paper\n\ncontent", encoding="utf-8")
    args = Namespace(mineru_output_root=str(tmp_path / "mineru_outputs"))
    row = local_batch.BatchRow(
        batch_id="iclr26_0009",
        title="T",
        openreview_forum_id="abc123",
        path=str(tmp_path / "paper.pdf"),
    )

    assert local_batch.discover_mineru_output(args, row) is None


def batch_args_for_source_selection(tmp_path: Path, mineru_output_root: Path) -> Namespace:
    return Namespace(
        output_root=tmp_path / "runs",
        env_file=tmp_path / ".env",
        mineru_output_root=str(mineru_output_root),
        mineru_bin="mineru",
        mineru_backend="pipeline",
        mineru_timeout=1800,
        mineru_model_source="local",
        mineru_config=tmp_path / "mineru.json",
        mineru_pipeline_cache=tmp_path / "cache",
        chunk_chars=18000,
        overlap_chars=1500,
        part_workers=2,
        provider="deepseek",
        temperature=0.1,
        part_max_tokens=4096,
        main_max_tokens=8192,
        writer_max_tokens=8192,
        main_context_chars=36000,
        adaptive_tokens=True,
        adaptive_long_chunk_count=11,
        adaptive_long_markdown_chars=144000,
        adaptive_long_chars_per_page=4500,
        adaptive_long_part_max_tokens=8192,
        adaptive_long_main_max_tokens=12288,
        adaptive_long_main_context_chars=54000,
        adaptive_extreme_chunk_count=15,
        adaptive_extreme_markdown_chars=216000,
        adaptive_extreme_pages=45,
        adaptive_extreme_main_max_tokens=16384,
        vault_root=tmp_path / "vault",
        vault_asset_root=tmp_path / "vault" / "assets",
        max_note_images=6,
        model="",
        base_url="",
        api_key_env="",
        mock_llm=False,
        dry_run=False,
        force=False,
        export_vault=True,
        resume=True,
        kimi_check_repair=True,
    )


def test_batch_build_single_args_prefers_existing_mineru_output(tmp_path):
    mineru_root = tmp_path / "mineru_outputs"
    out = mineru_root / "iclr26_0009" / "abc123"
    write_fake_mineru_output(out)
    row = local_batch.BatchRow(
        batch_id="iclr26_0009",
        title="T",
        openreview_forum_id="abc123",
        path=str(tmp_path / "paper.pdf"),
    )

    single_args = local_batch.build_single_args(batch_args_for_source_selection(tmp_path, mineru_root), row)

    assert single_args.mineru_output == str(out.resolve())
    assert single_args.pdf is None
    assert single_args.paper_pdf == str(row.pdf_path)


def test_batch_detects_fatal_provider_balance_errors():
    assert local_batch.is_fatal_provider_error("Error code: 402 - Insufficient Balance")
    assert local_batch.is_fatal_provider_error("{'message': 'Insufficient Balance'}")
    assert not local_batch.is_fatal_provider_error("MinerU failed with exit code 1")


def test_resolve_llm_config_kimi_uses_moonshot_env_and_adds_v1(monkeypatch):
    monkeypatch.setenv("MOONSHOT_API_KEY", "test-key")
    monkeypatch.setenv("MOONSHOT_MODEL", "kimi-k2.6")
    monkeypatch.setenv("MOONSHOT_BASE_URL", "https://api.kimi.com/coding")
    args = Namespace(
        provider="kimi",
        api_key_env="",
        model="",
        base_url="",
        temperature=0.1,
    )

    local_analysis.resolve_llm_config(args)

    assert args.api_key_env == "MOONSHOT_API_KEY"
    assert args.model == "kimi-k2.6"
    assert args.base_url == "https://api.kimi.com/coding/v1"
    assert args.temperature == 0.6


def test_resolve_writer_llm_config_defaults_to_deepseek(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    args = Namespace(
        writer_provider="deepseek",
        writer_api_key_env="",
        writer_model="",
        writer_base_url="",
    )

    local_analysis.resolve_writer_llm_config(args)

    assert args.writer_api_key_env == "DEEPSEEK_API_KEY"
    assert args.writer_model == "deepseek-v4-pro"
    assert args.writer_base_url == "https://api.deepseek.com/v1"


def test_resolve_kimi_llm_config_uses_moonshot_env(monkeypatch):
    monkeypatch.setenv("MOONSHOT_API_KEY", "test-key")
    monkeypatch.setenv("MOONSHOT_MODEL", "kimi-k2.6")
    monkeypatch.setenv("MOONSHOT_BASE_URL", "https://api.kimi.com/coding")
    args = Namespace(kimi_api_key_env="", kimi_model="", kimi_base_url="")

    local_analysis.resolve_kimi_llm_config(args)

    assert args.kimi_api_key_env == "MOONSHOT_API_KEY"
    assert args.kimi_model == "kimi-k2.6"
    assert args.kimi_base_url == "https://api.kimi.com/coding/v1"


def test_ensure_mineru_local_config_uses_latest_snapshot(tmp_path):
    cache = tmp_path / "models--opendatalab--PDF-Extract-Kit-1.0"
    old_snapshot = cache / "snapshots" / "old"
    new_snapshot = cache / "snapshots" / "new"
    old_snapshot.mkdir(parents=True)
    new_snapshot.mkdir(parents=True)
    config_path = tmp_path / "mineru.json"
    old_snapshot.touch()
    new_snapshot.touch()
    args = Namespace(
        mineru_config=str(config_path),
        mineru_model_source="local",
        mineru_pipeline_cache=str(cache),
    )

    resolved = local_analysis.ensure_mineru_local_config(args)

    payload = json.loads(resolved.read_text(encoding="utf-8"))
    assert payload["models-dir"]["pipeline"] == str(new_snapshot)


def test_ensure_mineru_local_config_keeps_existing_config(tmp_path):
    config_path = tmp_path / "mineru.json"
    config_path.write_text('{"models-dir":{"pipeline":"/existing"}}\n', encoding="utf-8")
    args = Namespace(
        mineru_config=str(config_path),
        mineru_model_source="local",
        mineru_pipeline_cache=str(tmp_path / "missing"),
    )

    resolved = local_analysis.ensure_mineru_local_config(args)

    assert resolved == config_path.resolve()
    assert json.loads(resolved.read_text(encoding="utf-8"))["models-dir"]["pipeline"] == "/existing"


def test_mock_local_pipeline_writes_file_contract(tmp_path):
    source_md = tmp_path / "sample.md"
    source_md.write_text(
        "# Sample Paper\n\n"
        + "Abstract text.\n\n"
        + "## Method\n\n"
        + "M" * 1300
        + "\n\n## Experiments\n\n"
        + "E" * 1300,
        encoding="utf-8",
    )
    output_root = tmp_path / "runs"
    args = local_analysis.build_parser().parse_args([
        "--source-md",
        str(source_md),
        "--output-root",
        str(output_root),
        "--task-id",
        "sample_task",
        "--mock-llm",
        "--chunk-chars",
        "1200",
        "--overlap-chars",
        "100",
        "--part-workers",
        "2",
    ])

    result = asyncio.run(local_analysis.run_pipeline(args))
    work_dir = Path(result["work_dir"])

    assert result["status"] == "done"
    assert (work_dir / ".state").read_text(encoding="utf-8").strip() == "DONE"
    assert (work_dir / "parse" / "full.md").exists()
    assert (work_dir / "parse" / "chunks" / "index.json").exists()
    assert len(list((work_dir / "part_analysis").glob("part_*.json"))) == result["chunk_count"]
    assert (work_dir / "analysis" / "main_analysis.json").exists()
    assert (work_dir / "report" / "final_report.md").exists()

    manifest = json.loads((work_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "done"
    assert manifest["part_analysis_count"] == result["chunk_count"]


def test_dedupe_caption_prefix():
    assert local_analysis.dedupe_caption_prefix("Figure 1", "Figure 1: Figure 1: overview") == "overview"
    assert local_analysis.dedupe_caption_prefix("Table 1", "Table 1: results") == "results"
    assert local_analysis.dedupe_caption_prefix("Figure 24", "(b) NB (c) FLIPD Figure 24: Estimated LID") == "Estimated LID"


def test_fallback_figure_placements_do_not_use_sample_figure_as_framework():
    figures = [
        {"item_id": "item_001", "label": "Figure 1", "type": "figure", "caption": "Few samples from Gaussian (IDR) dataset."},
        {"item_id": "item_002", "label": "Table 1", "type": "table", "caption": "Summary of our experiments."},
        {"item_id": "item_003", "label": "Figure 3", "type": "figure", "caption": "LID estimates calculated using NB."},
    ]

    placements = local_analysis.fallback_figure_placements(figures, max_images=2)

    assert {"item_id": "item_001", "section": "整体框架", "reason": "caption indicates a framework or method overview"} not in placements
    assert all(item["section"] == "实验与分析" for item in placements)
    assert placements[0]["item_id"] == "item_002"


def test_normalize_figure_placements_filters_unknown_and_duplicates():
    figures = [
        {"item_id": "item_001", "label": "Table 1", "type": "table", "caption": "Summary."},
        {"item_id": "item_002", "label": "Figure 3", "type": "figure", "caption": "Results."},
    ]
    parsed = {
        "placements": [
            {"item_id": "missing", "section": "实验与分析", "reason": "bad"},
            {"item_id": "item_001", "section": "实验与分析", "reason": "summary"},
            {"item_id": "item_001", "section": "整体框架", "reason": "duplicate"},
            {"item_id": "item_002", "section": "unknown", "reason": "bad"},
        ]
    }

    placements = local_analysis.normalize_figure_placements(parsed, figures, max_images=3)

    assert placements == [{"item_id": "item_001", "section": "实验与分析", "reason": "summary"}]


def test_topic_text_for_note_prefers_root_and_subtopic(monkeypatch):
    monkeypatch.setattr(local_analysis, "load_topic_assignments", lambda: {
        "abc": {
            "root_id": "vision_multimodal_applications",
            "root_label": "Vision / Multimodal Applications",
            "subtopic_id": "vision_models_multimodal",
            "subtopic_label": "Vision Models & Multimodal",
        }
    })
    assert local_analysis.topic_text_for_note("abc", "ICLR_2026") == "#topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal"


def test_topic_text_for_note_falls_back_to_conf_year_tag(monkeypatch):
    monkeypatch.setattr(local_analysis, "load_topic_assignments", lambda: {})

    assert local_analysis.topic_text_for_note("missing", "ICLR_2026") == "#topic/iclr_2026"


def test_compose_vault_note_writes_topic_tags_to_table_and_frontmatter():
    note = local_analysis.compose_vault_note(
        title="Sample Paper",
        conf_year="ICLR_2026",
        pdf_ref="",
        openreview_forum_id="abc",
        theme_bucket="vision",
        analysis={
            "analysis_truth": {"core_insight": "x"},
            "paper_metadata": {},
            "method": {"proposed_method_name": "M"},
            "experiments": {"main_results": []},
        },
        report="## 概述\n\n正文",
        copied_figures=[],
        max_images=0,
        topic_text="#topic/root #topic/root/sub",
    )

    assert "- topic/root" in note
    assert "- topic/root/sub" in note
    assert "| Topic | #topic/root #topic/root/sub |" in note


def test_assemble_section_report_joins_sections():
    report = local_analysis.assemble_section_report(["## 概述\n\nA", "## 背景与动机\n\nB"])
    assert "## 概述" in report
    assert "## 背景与动机" in report


def test_estimate_cost_usd_known_model():
    cost = local_analysis.estimate_cost_usd("deepseek-v4-pro", 100000, 20000)
    assert cost is not None
    assert cost > 0


def test_part_max_tokens_default_allows_ds_max_reasoning_budget():
    args = local_analysis.build_parser().parse_args(["--source-md", "sample.md", "--mock-llm"])

    assert args.part_max_tokens >= 8192


def test_default_chunk_size_keeps_ds_max_part_prompts_smaller():
    args = local_analysis.build_parser().parse_args(["--source-md", "sample.md", "--mock-llm"])

    assert args.chunk_chars <= 8000
    assert args.overlap_chars <= 800


def test_writer_defaults_to_deepseek_without_changing_analysis_provider():
    args = local_analysis.build_parser().parse_args(["--source-md", "sample.md", "--mock-llm"])

    assert args.provider == "deepseek"
    assert args.writer_provider == "deepseek"
    assert args.kimi_repair
    assert args.kimi_check_repair


def test_batch_forwards_kimi_check_repair_flag(tmp_path):
    pdf = tmp_path / "paper.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")
    rel_pdf = pdf.relative_to(local_batch.REPO_ROOT) if pdf.is_relative_to(local_batch.REPO_ROOT) else pdf
    args = local_batch.build_parser().parse_args([
        "--batch-manifest", "manifest.jsonl",
        "--no-kimi-check-repair",
    ])
    row = local_batch.BatchRow(
        batch_id="b001",
        title="Sample Paper",
        openreview_forum_id="abc123",
        path=str(rel_pdf),
    )

    single_args = local_batch.build_single_args(args, row)

    assert not args.kimi_check_repair
    assert not single_args.kimi_check_repair


def test_batch_reads_completed_status_ledger(tmp_path):
    ledger = tmp_path / "status.jsonl"
    ledger.write_text(
        '{"openreview_forum_id":"done1","analysis_status":"completed"}\n'
        '{"openreview_forum_id":"pending1","analysis_status":"pending"}\n',
        encoding="utf-8",
    )

    assert local_batch.completed_statuses_from_ledger(ledger) == {"done1": "done"}


def test_planner_selects_rows_without_sha():
    rows = [
        plan_batches.PaperRow(
            title=f"Paper {idx}",
            openreview_forum_id=f"id{idx}",
            sha256="",
            size_bytes=2_000_000 + idx,
            path=f"paper_{idx}.pdf",
            source="status",
            manifest_paper_id="",
            theme_bucket="other",
        )
        for idx in range(3)
    ]

    selected = plan_batches.select_next_batch(rows, set(), 3)

    assert [row.openreview_forum_id for row in selected] == ["id0", "id1", "id2"]


def test_mock_pipeline_includes_usage_summary(tmp_path):
    source_md = tmp_path / "sample.md"
    source_md.write_text("# Sample Paper\n\n## Method\n\nM" * 500 + "\n\n## Experiments\n\nE" * 500, encoding="utf-8")
    output_root = tmp_path / "runs"
    args = local_analysis.build_parser().parse_args([
        "--source-md", str(source_md),
        "--output-root", str(output_root),
        "--task-id", "sample_usage_task",
        "--mock-llm",
    ])
    result = asyncio.run(local_analysis.run_pipeline(args))
    manifest = json.loads((Path(result["work_dir"]) / "manifest.json").read_text(encoding="utf-8"))
    assert "usage" in manifest
    assert manifest["usage"]["total_tokens_est"] == 0


def test_part_analysis_fallback_contains_open_question():
    fb = local_analysis.part_analysis_fallback("part_002", "nonsense output", "invalid json")
    assert fb["part_id"] == "part_002"
    assert fb["section_role"] == "fallback_unparsed_chunk"
    assert fb["open_questions"]


def test_part_schema_is_minimal_anchor_set():
    schema = local_analysis.part_schema()

    assert "reference_evidence" not in schema
    assert set(schema) == {
        "part_id",
        "section_role",
        "method_evidence",
        "experiment_evidence",
        "formula_evidence",
        "figure_table_roles",
        "open_questions",
    }


def test_empty_part_fallback_extracts_chunk_anchors():
    chunk_text = (
        "## 3.4 THIN MANIFOLDS\n\n"
        "The ESS algorithm behaves as expected and maintains the correct estimate.\n\n"
        "$$x = r \\sin \\theta$$\n\n"
        "Figure 6: LID estimates for the Moon (IDR) dataset using ESS.\n"
    )

    fb = local_analysis.part_analysis_fallback("part_002", "{}", "empty json", chunk_text)

    assert fb["section_role"] == "3.4 THIN MANIFOLDS"
    assert fb["method_evidence"]
    assert fb["formula_evidence"][0]["latex"] == r"x = r \sin \theta"
    assert fb["figure_table_roles"][0]["label"] == "Figure 6"


def test_appendix_figure_table_chunk_uses_local_anchor_extraction():
    chunk_text = (
        "## B.4 THIN MANIFOLDS\n\n"
        "![](a.jpg)\nFigure 17: Results for moon dataset for different algorithms.\n"
        "![](b.jpg)\nFigure 18: Results for funnel dataset for different algorithms.\n"
        "![](c.jpg)\nFigure 19: Results for spiral dataset for different algorithms.\n"
        "![](d.jpg)\nFigure 20: Per-method results for various sample sizes.\n"
    )

    assert local_analysis.is_appendix_figure_table_chunk(chunk_text)
    parsed = local_analysis.local_anchor_part_analysis("part_009", chunk_text)
    assert parsed["part_id"] == "part_009"
    assert len(parsed["figure_table_roles"]) == 4
    assert parsed["experiment_evidence"][0]["table_or_figure"] == "Figure 17"
    assert parsed["open_questions"] == []


def test_mock_pipeline_exports_obsidian_note_with_assets(tmp_path):
    source_md = tmp_path / "sample.md"
    source_md.write_text(
        "# Sample Paper\n\n"
        + "## Method\n\n"
        + "M" * 1300
        + "\n\n## Experiments\n\n"
        + "E" * 1300,
        encoding="utf-8",
    )
    source_pdf = tmp_path / "sample.pdf"
    source_pdf.write_bytes(b"%PDF-1.4\n%mock\n")
    figure = tmp_path / "figure.jpg"
    figure.write_bytes(b"fake-image")
    output_root = tmp_path / "runs"
    vault_root = tmp_path / "vault"
    asset_root = vault_root / "assets" / "figures" / "papers"
    args = local_analysis.build_parser().parse_args([
        "--source-md",
        str(source_md),
        "--paper-title",
        "Sample Paper: Test Case",
        "--paper-pdf",
        str(source_pdf),
        "--output-root",
        str(output_root),
        "--task-id",
        "sample_task",
        "--mock-llm",
        "--chunk-chars",
        "1200",
        "--overlap-chars",
        "100",
        "--export-vault",
        "--vault-root",
        str(vault_root),
        "--vault-asset-root",
        str(asset_root),
        "--openreview-forum-id",
        "abc123",
        "--theme-bucket",
        "llm_rl_agent",
    ])

    # parse already ran in this mock test, so inject a deterministic MinerU item
    result = asyncio.run(local_analysis.run_pipeline(args))
    work_dir = Path(result["work_dir"])
    figures_path = work_dir / "parse" / "figures_tables.json"
    figures_path.write_text(
        json.dumps([
            {
                "label": "Figure 1",
                "type": "figure",
                "caption": "Few samples from Gaussian (IDR) dataset.",
                "source_path": str(figure),
            }
        ]),
        encoding="utf-8",
    )
    analysis = json.loads((work_dir / "analysis" / "main_analysis.json").read_text(encoding="utf-8"))
    report = (work_dir / "report" / "final_report.md").read_text(encoding="utf-8")
    export_info = local_analysis.export_to_vault(
        args,
        task_id="sample_task",
        title="Sample Paper: Test Case",
        work_dir=work_dir,
        analysis=analysis,
        report=report,
        figures_tables=json.loads(figures_path.read_text(encoding="utf-8")),
    )

    note_path = Path(export_info["note_path"])
    note = note_path.read_text(encoding="utf-8")
    assert note_path == vault_root / "paper" / "ICLR_2026" / "Sample_Paper_Test_Case.md"
    assert (vault_root / "paperPDFs" / "ICLR_2026" / "Sample_Paper_Test_Case.pdf").exists()
    assert (asset_root / "sample_task" / "figures" / "001_Figure_1.jpg").exists()
    assert "type: paper" in note
    assert "pdf_ref: paperPDFs/ICLR_2026/Sample_Paper_Test_Case.pdf" in note
    assert "[paper](https://openreview.net/forum?id=abc123)" in note
    assert "![Figure 1](../../assets/figures/papers/sample_task/figures/001_Figure_1.jpg)" not in note
    assert "![[paperPDFs/ICLR_2026/Sample_Paper_Test_Case.pdf]]" in note


def test_render_info_table_prefers_chinese_title_from_analysis():
    table = local_analysis.render_info_table(
        title="Bayesian Ensemble for Sequential Decision-Making",
        conf_year="ICLR_2026",
        openreview_forum_id="abc123",
        analysis={
            "paper_metadata": {
                "title": "Bayesian Ensemble for Sequential Decision-Making",
                "title_zh": "用于序列决策的贝叶斯集成",
            },
            "method": {"proposed_method_name": "Bayesian Ensemble (BE)"},
            "experiments": {"main_results": [{"benchmark": "Neural Testbed d=2"}]},
        },
    )

    assert "| 中文题名 | 用于序列决策的贝叶斯集成 |" in table
    assert "| 英文题名 | Bayesian Ensemble for Sequential Decision-Making |" in table


def test_preserve_core_metric_terms_restores_metric_from_part_analysis():
    analysis = {
        "experiments": {
            "main_results": [
                {
                    "benchmark": "Neural Testbed d=2",
                    "metric": "遗憾改进",
                    "proposed": "ensemble+(BEB)",
                    "baseline": "ensemble+",
                    "delta": "37.0%",
                }
            ]
        }
    }
    part_results = [
        {
            "experiment_evidence": [
                {
                    "claim": "On Neural Testbed d=2, ensemble+(BEB) improves over ensemble+.",
                    "metric": "regret improvement",
                    "value": "37.0%",
                    "table_or_figure": "Figure 3",
                }
            ]
        }
    ]

    repaired = local_analysis.preserve_core_metric_terms(analysis, part_results)

    assert repaired["experiments"]["main_results"][0]["metric"] == "regret improvement"


def test_normalize_main_analysis_fills_required_sections():
    parsed = {"paper_metadata": {"title": "T"}}

    normalized = local_analysis.normalize_main_analysis("Fallback Title", parsed)

    assert normalized["paper_metadata"]["title"] == "T"
    assert "analysis_truth" in normalized
    assert normalized["experiments"]["main_results"] == []
    assert normalized["open_questions"] == []


def test_section_prompt_uses_focused_context_not_full_part_dump():
    analysis = local_analysis.normalize_main_analysis("T", {"paper_metadata": {"title": "T"}})
    part_results = []
    for index in range(12):
        part_results.append({
            "part_id": f"part_{index:03d}",
            "section_role": "Experiments" if index % 2 == 0 else "Appendix",
            "experiment_evidence": [{"claim": f"result {index}", "table_or_figure": "Table 1"}] if index % 2 == 0 else [],
            "method_evidence": [{"claim": f"method {index}"}],
            "formula_evidence": [],
            "figure_table_roles": [],
            "open_questions": [],
            "_meta": {"usage": {"prompt_tokens_est": 123}},
        })
    figures = [
        {"item_id": "item_001", "label": "Table 1", "type": "table", "caption": "Summary results."},
        {"item_id": "item_002", "label": "Figure 1", "type": "figure", "caption": "Few samples from dataset."},
    ]

    prompt = json.loads(local_analysis.build_section_prompt(
        section_title="实验与分析",
        section_goal="写实验",
        analysis=analysis,
        part_results=part_results,
        figures_tables=figures,
    ))

    assert "part_analyses" not in prompt
    assert "focused_part_analyses" in prompt
    assert len(prompt["focused_part_analyses"]) <= 8
    assert all("_meta" not in part for part in prompt["focused_part_analyses"])
    assert prompt["focused_figures_tables"][0]["item_id"] == "item_001"


def test_visual_summary_parser_args_exist():
    args = local_analysis.build_parser().parse_args(["--source-md", "sample.md", "--mock-llm"])

    assert args.figure_visual_summary_max_items > 0
    assert args.figure_visual_summary_max_tokens > 0
