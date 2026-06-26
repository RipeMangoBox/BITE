from pathlib import Path
from types import SimpleNamespace

import pytest
try:
    import fitz
except ImportError:  # pragma: no cover - optional dependency
    fitz = None

from scripts import run_local_paper_analysis as runner


def _args(tmp_path, **overrides):
    values = {
        "vault_root": str(tmp_path / "vault"),
        "vault_note_dir": "",
        "vault_asset_root": str(tmp_path / "vault" / "assets" / "figures" / "papers"),
        "paper_pdf": "",
        "pdf": "",
        "conf_year": "ICLR_2026",
        "openreview_forum_id": "abc123",
        "paper_link": "https://openreview.net/forum?id=abc123",
        "acceptance": "accepted",
        "theme_bucket": "",
        "max_note_images": 0,
        "topic_assignments": "",
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def _analysis(**overrides):
    values = runner.mock_json("main")
    values.update(overrides)
    return values


def _report():
    return "\n\n".join(
        f"## {title}\n\n{title} body. " + "This section contains enough content for validation. " * 4
        for title, _ in runner.SECTION_SPECS
    )


def test_resolve_existing_pdf_path_uses_explicit_external_search_root(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    external_root = tmp_path / "external" / "pdfs"
    pdf = external_root / "ICLR_2026" / "Paper__abc123.pdf"
    pdf.parent.mkdir(parents=True)
    pdf.write_bytes(b"%PDF-1.4\n")
    monkeypatch.setattr(runner, "REPO_ROOT", repo)

    resolved, info = runner.resolve_existing_pdf_path(
        "/old/worktree/pdfs/ICLR_2026/Paper__abc123.pdf",
        conf_year="ICLR_2026",
        search_roots=[external_root],
    )

    assert resolved == pdf.resolve()
    assert str(pdf) in info["attempts"]


def test_resolve_existing_pdf_path_uses_env_search_roots(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    external_root = tmp_path / "external" / "pdfs"
    pdf = external_root / "ICLR_2026" / "Paper__abc123.pdf"
    pdf.parent.mkdir(parents=True)
    pdf.write_bytes(b"%PDF-1.4\n")
    monkeypatch.setattr(runner, "REPO_ROOT", repo)
    monkeypatch.setenv("RF_PDF_SEARCH_ROOTS", str(external_root))

    resolved, info = runner.resolve_existing_pdf_path(
        "/old/worktree/pdfs/ICLR_2026/Paper__abc123.pdf",
        conf_year="ICLR_2026",
    )

    assert resolved == pdf.resolve()
    assert str(pdf) in info["attempts"]


def test_export_to_vault_requires_existing_pdf(tmp_path):
    args = _args(tmp_path, paper_pdf=str(tmp_path / "missing.pdf"))

    with pytest.raises(FileNotFoundError, match="Vault export requires an existing PDF"):
        runner.export_to_vault(
            args,
            task_id="paper1",
            title="Paper One",
            work_dir=tmp_path,
            analysis=_analysis(),
            report=_report(),
            figures_tables=[],
            progress_path=tmp_path / "progress.jsonl",
        )


def test_export_to_vault_uses_resolved_pdf_and_validates(tmp_path):
    pdf = tmp_path / "source.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")
    args = _args(tmp_path, paper_pdf=str(pdf))

    out = runner.export_to_vault(
        args,
        task_id="paper1",
        title="Paper One",
        work_dir=tmp_path,
        analysis=_analysis(),
        report=_report(),
        figures_tables=[],
        progress_path=tmp_path / "progress.jsonl",
    )

    assert out["pdf_ref"] == "paperPDFs/ICLR_2026/Paper_One.pdf"
    assert out["validation"]["ok"] is True
    note = (tmp_path / "vault" / "analysis" / "ICLR_2026" / "Paper_One.md").read_text(encoding="utf-8")
    assert "openreview_forum_id: abc123" in note
    assert (tmp_path / "vault" / out["pdf_ref"]).exists()


def test_export_to_vault_uses_lowercase_arxiv_slug(tmp_path):
    pdf = tmp_path / "source.pdf"
    pdf.write_bytes(b"%PDF-1.4\n")
    args = _args(tmp_path, paper_pdf=str(pdf), conf_year="arXiv_2025")

    out = runner.export_to_vault(
        args,
        task_id="paper1",
        title="Paper One",
        work_dir=tmp_path,
        analysis=_analysis(),
        report=_report(),
        figures_tables=[],
        progress_path=tmp_path / "progress.jsonl",
    )

    assert out["pdf_ref"] == "paperPDFs/arxiv_2025/Paper_One.pdf"
    assert (tmp_path / "vault" / "analysis" / "arxiv_2025" / "Paper_One.md").exists()


def test_frontmatter_tags_use_venue_and_real_topic_tags_only():
    tags = runner.topic_tags_for_frontmatter(
        "#topic/iclr_2026 #topic/vision_multimodal_applications "
        "#topic/vision_multimodal_applications/vision_models_multimodal",
        "iclr_2026",
    )

    assert tags == [
        "ICLR_2026",
        "topic/vision_multimodal_applications",
        "topic/vision_multimodal_applications/vision_models_multimodal",
    ]


def test_frontmatter_tags_use_workshop_venue_slug():
    assert runner.topic_tags_for_frontmatter("", "CVPR_Workshop_2024") == ["CVPRW_2024"]


def test_render_info_table_includes_project_link_from_source_links():
    analysis = _analysis(source_links=[
        {"label": "Project", "url": "https://ripemangobox.github.io/ReactDance."},
    ])

    table = runner.render_info_table(
        title="ReactDance",
        conf_year="ICLR_2026",
        openreview_forum_id="FvMyAMbbX0",
        paper_link="https://openreview.net/forum?id=FvMyAMbbX0",
        acceptance="accepted",
        analysis=analysis,
        report="",
        topic_text="#topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal",
    )

    assert "[paper](https://openreview.net/forum?id=FvMyAMbbX0)" in table
    assert "[Project](https://ripemangobox.github.io/ReactDance)" in table
    assert "#topic/iclr_2026" not in table
    assert "#topic/vision_multimodal_applications/vision_models_multimodal" in table


def test_extract_source_links_finds_project_page_bare_url():
    links = runner.extract_source_links(
        "Extensive experiments. Project page: https://ripemangobox.github.io/ReactDance."
    )

    assert links == [{"label": "Project", "url": "https://ripemangobox.github.io/ReactDance"}]


def test_structured_main_context_keeps_key_spans_and_skips_references():
    markdown = "\n\n".join([
        "# Paper",
        "Abstract. " + "abstract signal. " * 200,
        "## 1 Introduction\n" + "intro motivation. " * 250,
        "## 2 Related Work\n" + "related citation. " * 300,
        "## 3 Method\n" + "method pipeline unique mechanism. " * 260,
        "## 4 Experiments\n" + "experiment table metric ablation. " * 260,
        "## 5 Conclusion\n" + "conclusion limitation boundary. " * 180,
        "## Acknowledgments\n" + "grant agency. " * 200,
        "## References\n" + "reference item. " * 500,
    ])

    context = runner.main_paper_context(markdown, max_chars=12_000, mode="structured")

    assert len(context) <= 12_000
    assert "Section Headings" in context
    assert "method pipeline unique mechanism" in context
    assert "experiment table metric ablation" in context
    assert "conclusion limitation boundary" in context
    assert "grant agency" not in context
    assert "reference item" not in context


def test_compact_main_context_preserves_existing_head_tail_behavior():
    markdown = "A" * 20_000 + "\nMIDDLE\n" + "Z" * 20_000

    context = runner.main_paper_context(markdown, max_chars=12_000, mode="compact")

    assert context.startswith("A" * 100)
    assert context.endswith("Z" * 100)
    assert "middle omitted in main merge prompt" in context


def test_adaptive_budget_does_not_raise_structured_main_context():
    args = _args(
        Path("/tmp"),
        adaptive_tokens=True,
        adaptive_long_chunk_count=11,
        adaptive_long_markdown_chars=144_000,
        adaptive_long_chars_per_page=4_500,
        adaptive_extreme_chunk_count=15,
        adaptive_extreme_markdown_chars=216_000,
        adaptive_extreme_pages=45,
        adaptive_long_part_max_tokens=8192,
        adaptive_long_main_max_tokens=12288,
        adaptive_extreme_main_max_tokens=16384,
        adaptive_long_main_context_chars=54_000,
        part_max_tokens=16384,
        main_max_tokens=16384,
        writer_max_tokens=8192,
        main_context_chars=18_000,
        main_context_mode="structured",
    )

    budget = runner.apply_adaptive_token_budget(
        args,
        markdown_chars=120_000,
        chunk_count=19,
        page_count=None,
    )

    assert budget["profile"] == "extreme"
    assert budget["after"]["main_context_chars"] == 18_000
    assert budget["after"]["main_context_mode"] == "structured"


def test_frontmatter_metadata_falls_back_when_main_analysis_fields_empty():
    analysis = {
        "paper_metadata": {
            "title": "EUBRL: Epistemic Uncertainty Directed Bayesian Reinforcement Learning",
            "title_zh": "",
        },
        "method": {"proposed_method_name": ""},
        "analysis_truth": {"core_insight": "", "causal_knob": "", "real_bottleneck": ""},
        "experiments": {"main_results": []},
    }

    frontmatter = runner.render_frontmatter(
        title="EUBRL: Epistemic Uncertainty Directed Bayesian Reinforcement Learning",
        conf_year="ICLR_2026",
        pdf_ref="paperPDFs/ICLR_2026/EUBRL.pdf",
        analysis=analysis,
        theme_bucket="",
        acceptance="accepted",
    )

    assert 'core_operator: ""' not in frontmatter
    assert 'primary_logic: ""' not in frontmatter
    assert 'paradigm: ""' not in frontmatter
    assert "EUBRL" in frontmatter


def test_validate_vault_note_acceptance_unknown_is_not_fallback_marker():
    sections = "\n\n".join(
        f"## {title}\n\nEnough content."
        for title, _ in runner.SECTION_SPECS
    )
    note = f"""---
title: Paper One
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Paper_One.pdf
acceptance: unknown
tags:
- status/analyzed
core_operator: operator
primary_logic: logic
claims:
- claim
paradigm: paradigm
openreview_forum_id: abc123
---

# Paper One

{sections}

![[assets/figures/papers/paper1/figures/fig1.png]]
*Figure 1: Comparison to prior methods [4] [15] [33] [67].*

## 原文 PDF

![[paperPDFs/ICLR_2026/Paper_One.pdf]]
"""

    validation = runner.validate_vault_note(
        note,
        pdf_ref="paperPDFs/ICLR_2026/Paper_One.pdf",
        openreview_forum_id="abc123",
        copied_figures=[{"item_id": "fig1", "note_image_path": "assets/figures/papers/paper1/figures/fig1.png"}],
        figure_placements=[{"item_id": "fig1", "section": "实验与分析"}],
        max_images=12,
    )

    assert validation["checks"]["no_fallback_metadata_markers"] is True
    assert validation["fallback_markers"] == []
    assert validation["checks"]["no_dangling_numeric_refs"] is True
    assert validation["dangling_numeric_refs"] == []


def test_validate_vault_note_missing_selected_image_is_nonfatal():
    sections = "\n\n".join(
        f"## {title}\n\n" + ("Enough content. " * 20)
        for title, _ in runner.SECTION_SPECS
    )
    note = f"""---
title: Paper One
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Paper_One.pdf
project_link:
code_link:
tags:
- ICLR_2026
core_operator: operator
primary_logic: logic
claims:
- claim
---

# Paper One

{sections}

## 原文 PDF

![[paperPDFs/ICLR_2026/Paper_One.pdf]]
"""

    validation = runner.validate_vault_note(
        note,
        pdf_ref="paperPDFs/ICLR_2026/Paper_One.pdf",
        copied_figures=[{"item_id": "fig1", "note_image_path": "assets/figures/papers/paper1/figures/fig1.png"}],
        figure_placements=[{"item_id": "fig1", "section": "实验与分析"}],
        max_images=12,
    )

    assert validation["checks"]["image_embeds_present"] is False
    assert validation["ok"] is False
    assert validation["fatal_ok"] is True
    assert "image_embeds_present" in validation["nonfatal_checks"]


def test_parser_defaults_do_not_enable_kimi_or_figure_llm():
    parser = runner.build_parser()
    args = parser.parse_args(["--source-md", "paper.md"])

    assert args.kimi_repair is False
    assert args.kimi_check_repair is False
    assert args.figure_provider == "none"


def test_resolve_figure_llm_config_uses_gpt_env(monkeypatch):
    monkeypatch.setenv("gpt_OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("gpt_OPENAI_MODEL", "gpt-test")
    monkeypatch.setenv("gpt_OPENAI_BASE_URL", "https://example.test/v1")
    args = SimpleNamespace(
        figure_provider="openai",
        figure_model="",
        figure_base_url="",
        figure_api_key_env="",
        figure_temperature=0.1,
    )

    runner.resolve_figure_llm_config(args)

    assert args.figure_api_key_env == "gpt_OPENAI_API_KEY"
    assert args.figure_model == "gpt-test"
    assert args.figure_base_url == "https://example.test/v1"


@pytest.mark.asyncio
async def test_figure_provider_none_uses_caption_fallback(tmp_path):
    args = SimpleNamespace(
        resume=False,
        force=False,
        mock_llm=False,
        figure_provider="none",
        figure_visual_summary_max_items=8,
    )
    work_dir = tmp_path / "work"
    (work_dir / "parse").mkdir(parents=True)
    progress_path = work_dir / "progress.jsonl"
    figures_tables = [
        {
            "item_id": "fig1",
            "type": "figure",
            "label": "Figure 1",
            "caption": "Figure 1: Method overview.",
        }
    ]

    enriched, usage = await runner.enrich_figure_visual_summaries(
        args,
        figures_tables=figures_tables,
        work_dir=work_dir,
        progress_path=progress_path,
    )

    assert usage["provider"] == "none"
    assert enriched[0]["visual_summary_provider"] == "caption_fallback"
    assert enriched[0]["visual_summary"] == "Method overview"
    assert "figure_visual_summaries_skipped" in progress_path.read_text(encoding="utf-8")


def test_extract_figures_tables_preserves_page_zero_for_content_list_v2(tmp_path):
    content_path = tmp_path / "content_list_v2.json"
    image_path = tmp_path / "images" / "fig1.jpg"
    image_path.parent.mkdir(parents=True)
    image_path.write_bytes(b"jpg")
    content_path.write_text(
        """
[
  [
    {
      "type": "image",
      "content": {
        "image_source": {"path": "images/fig1.jpg"},
        "image_caption": [{"type": "text", "content": "Figure 1: Overview."}]
      },
      "bbox": [10, 20, 110, 160]
    }
  ]
]
""".strip(),
        encoding="utf-8",
    )

    figures = runner.extract_figures_tables(content_path, source_root=tmp_path)

    assert len(figures) == 1
    assert figures[0]["page"] == 0
    assert figures[0]["label"] == "Figure 1"


def test_extract_figures_tables_preserves_each_source_in_same_page_subfigure_cluster(tmp_path):
    content_path = tmp_path / "content_list.json"
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    for name in ("a.jpg", "b.jpg", "c.jpg"):
        (image_dir / name).write_bytes(b"jpg")
    content_path.write_text(
        """
[
  {"type": "chart", "img_path": "images/a.jpg", "chart_caption": [], "bbox": [100, 100, 200, 200], "page_idx": 0},
  {"type": "chart", "img_path": "images/b.jpg", "chart_caption": ["Figure 2: Main result."], "bbox": [205, 100, 305, 200], "page_idx": 0},
  {"type": "chart", "img_path": "images/c.jpg", "chart_caption": ["(a) detail"], "bbox": [310, 100, 410, 200], "page_idx": 0}
]
""".strip(),
        encoding="utf-8",
    )

    figures = runner.extract_figures_tables(content_path, source_root=tmp_path)

    assert len(figures) == 3
    if fitz is None:
        assert [figure["source_path"] for figure in figures] == [
            str((image_dir / "a.jpg").resolve()),
            str((image_dir / "b.jpg").resolve()),
            str((image_dir / "c.jpg").resolve()),
        ]
        assert all("full_region_source" not in figure for figure in figures)
        return

    doc = fitz.open()
    page = doc.new_page(width=612, height=792)
    page.draw_rect(fitz.Rect(36, 72, 160, 240), color=(1, 0, 0), fill=(1, 0.8, 0.8))
    page.draw_rect(fitz.Rect(180, 72, 304, 240), color=(0, 1, 0), fill=(0.8, 1, 0.8))
    page.draw_rect(fitz.Rect(324, 72, 448, 240), color=(0, 0, 1), fill=(0.8, 0.8, 1))
    origin_pdf = tmp_path / "paper_origin.pdf"
    doc.save(origin_pdf)
    doc.close()
    (tmp_path / "paper_middle.json").write_text(
        """
{
  "pdf_info": [
    {
      "page_size": [612, 792],
      "para_blocks": [
        {"type": "image", "bbox": [36, 72, 160, 240]},
        {"type": "chart", "bbox": [180, 72, 304, 240]},
        {"type": "chart", "bbox": [324, 72, 448, 240]}
      ]
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )
    (tmp_path / "paper_model.json").write_text(
        """
{
  "pdf_info": [
    {
      "page_info": {"width": 734.4, "height": 950.4}
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )
    content_path.rename(tmp_path / "paper_content_list.json")
    content_path = tmp_path / "paper_content_list.json"
    content_path.write_text(
        """
[
  {"type": "chart", "img_path": "images/a.jpg", "chart_caption": [], "bbox": [43.2, 86.4, 192.0, 288.0], "page_idx": 0},
  {"type": "chart", "img_path": "images/b.jpg", "chart_caption": ["Figure 2: Main result."], "bbox": [216.0, 86.4, 364.8, 288.0], "page_idx": 0},
  {"type": "chart", "img_path": "images/c.jpg", "chart_caption": ["(a) detail"], "bbox": [388.8, 86.4, 537.6, 288.0], "page_idx": 0}
]
""".strip(),
        encoding="utf-8",
    )

    figures = runner.extract_figures_tables(content_path, source_root=tmp_path)

    assert len(figures) == 1
    assert figures[0]["label"] == "Figure 2"
    assert figures[0]["cluster_size"] == 3
    assert figures[0]["cluster_bbox"] == [43.2, 86.4, 537.6, 288.0]
    assert len(figures[0]["source_paths"]) == 3
    assert figures[0]["full_region_source"] == "pdf_crop"
    crop_path = figures[0]["source_path"]
    assert crop_path.endswith(".jpg")
    assert (tmp_path / "images" / "rf_full_regions").exists()
    assert all(source.endswith(".jpg") for source in figures[0]["source_paths"])
    assert Path(crop_path).exists()


def test_extract_figures_tables_full_region_crop_falls_back_when_crop_fails(tmp_path, monkeypatch):
    content_path = tmp_path / "paper_content_list.json"
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    for name in ("a.jpg", "b.jpg"):
        (image_dir / name).write_bytes(b"jpg")
    content_path.write_text(
        """
[
  {"type": "chart", "img_path": "images/a.jpg", "chart_caption": [], "bbox": [100, 100, 200, 200], "page_idx": 0},
  {"type": "chart", "img_path": "images/b.jpg", "chart_caption": ["Figure 3: Ablation."], "bbox": [205, 100, 305, 200], "page_idx": 0}
]
""".strip(),
        encoding="utf-8",
    )
    origin_pdf = tmp_path / "paper_origin.pdf"
    if fitz is not None:
        doc = fitz.open()
        doc.new_page(width=612, height=792)
        doc.save(origin_pdf)
        doc.close()
    else:
        origin_pdf.write_bytes(b"%PDF-1.4\n")
    (tmp_path / "paper_middle.json").write_text(
        '{"pdf_info": [{"page_size": [612, 792], "para_blocks": []}]}',
        encoding="utf-8",
    )
    (tmp_path / "paper_model.json").write_text(
        '{"pdf_info": [{"page_info": {"width": 1700, "height": 2200}}]}',
        encoding="utf-8",
    )
    monkeypatch.setattr(runner, "write_full_region_crop", lambda **kwargs: None)

    figures = runner.extract_figures_tables(content_path, source_root=tmp_path)

    assert len(figures) == 2
    assert [figure["source_path"] for figure in figures] == [
        str((image_dir / "a.jpg").resolve()),
        str((image_dir / "b.jpg").resolve()),
    ]
    assert all("full_region_source" not in figure for figure in figures)


def test_normalize_markdown_full_region_image_refs_collapses_subfigures(tmp_path):
    source_root = tmp_path
    full = tmp_path / "images" / "rf_full_regions" / "full.jpg"
    full.parent.mkdir(parents=True)
    full.write_bytes(b"jpg")
    figures = [{
        "full_region_source": "pdf_crop",
        "source_path": str(full),
        "source_paths": [
            str(tmp_path / "images" / "a.jpg"),
            str(tmp_path / "images" / "b.jpg"),
        ],
    }]
    markdown = "\n".join([
        "before",
        "![](images/a.jpg)  ",
        "(a) first",
        "![](images/b.jpg)  ",
        "(b) second",
        "after",
    ])

    normalized = runner.normalize_markdown_full_region_image_refs(
        markdown,
        figures,
        source_root=source_root,
    )

    assert normalized.count("![](") == 1
    assert "![](images/rf_full_regions/full.jpg)" in normalized
    assert "![](images/a.jpg)" not in normalized
    assert "![](images/b.jpg)" not in normalized
    assert "(a) first" in normalized
    assert "(b) second" in normalized


def test_normalize_markdown_full_region_image_refs_inserts_when_markdown_has_table_text(tmp_path):
    source_root = tmp_path
    full = tmp_path / "images" / "rf_full_regions" / "table.jpg"
    full.parent.mkdir(parents=True)
    full.write_bytes(b"jpg")
    figures = [{
        "full_region_source": "pdf_crop",
        "source_path": str(full),
        "source_paths": [
            str(tmp_path / "images" / "a.jpg"),
            str(tmp_path / "images" / "b.jpg"),
        ],
        "caption": "(a) Results on CIFAR-10. (b) Results on FFHQ-64.",
        "raw_items": [
            {"caption": "(a) Results on CIFAR-10."},
            {"caption": "(b) Results on FFHQ-64."},
        ],
    }]
    markdown = "\n".join([
        "before",
        "(a) Results on CIFAR-10.",
        "<table><tr><td>EDM + Neon</td></tr></table>",
        "(b) Results on FFHQ-64.",
        "<table><tr><td>EDM + Neon</td></tr></table>",
        "after",
    ])

    normalized = runner.normalize_markdown_full_region_image_refs(
        markdown,
        figures,
        source_root=source_root,
    )

    assert normalized.count("![](images/rf_full_regions/table.jpg)") == 1
    assert normalized.index("![](images/rf_full_regions/table.jpg)") < normalized.index("(a) Results on CIFAR-10.")


def test_fallback_figure_placements_prioritizes_full_region_clusters():
    figures_tables = [
        {
            "item_id": f"table_{index}",
            "type": "table",
            "label": f"Table {index}",
            "caption": "Benchmark result table.",
            "cluster_size": 1,
        }
        for index in range(1, 5)
    ] + [
        {
            "item_id": "full_region_1",
            "type": "figure",
            "label": "Figure 5",
            "caption": "Figure 5: Scaling result panels.",
            "cluster_size": 3,
            "full_region_source": "pdf_crop",
        },
        {
            "item_id": "full_region_2",
            "type": "figure",
            "label": "Figure 6",
            "caption": "Figure 6: Additional benchmark result panels.",
            "cluster_size": 2,
            "full_region_source": "pdf_crop",
        },
    ]

    placements = runner.fallback_figure_placements(figures_tables, max_images=3)

    assert [item["item_id"] for item in placements[:2]] == ["full_region_1", "full_region_2"]
    assert all(item["section"] == "实验与分析" for item in placements[:2])


def test_image_block_wraps_unwrapped_caption_latex_only():
    block = runner.image_block({
        "label": "Figure 1",
        "caption": (
            r"Figure 1: latent state \mathbf { X } compared with $y_{t}$ "
            r"and C_d = \frac { a } { b }."
        ),
        "note_image_path": "assets/figures/papers/paper1/figures/001_figure.png",
    })

    assert r"$\mathbf { X }$" in block
    assert r"$y_{t}$" in block
    assert r"$$y_{t}$$" not in block
    assert r"$C_d = \frac { a } { b }$" in block
    assert r"$C_$d" not in block


def test_wrap_caption_math_keeps_latex_delimiter_expression_together():
    wrapped = runner._wrap_caption_math(r"Use \left ( x + y \right ) for alignment.")

    assert r"$\left ( x + y \right )$" in wrapped
    assert r"$\left$" not in wrapped
    assert r"$\right$" not in wrapped


def test_ensure_referenced_figure_placements_keeps_explicit_sample_figure():
    report = "\n\n".join([
        "## 方法论拆解\n\nThe method is summarized in Fig. 2.",
        "## 实验与分析\n\nThe sampled examples are shown in Fig. 1.",
    ])
    copied_figures = [
        {
            "item_id": "fig2",
            "type": "figure",
            "label": "Figure 2",
            "caption": "Figure 2: Method overview.",
        },
        {
            "item_id": "fig1",
            "type": "figure",
            "label": "Figure 1",
            "caption": "Figure 1: Sample dataset images.",
        },
    ]

    placements = runner.ensure_referenced_figure_placements(
        [{"item_id": "fig2", "section": "方法论拆解", "reason": "method figure"}],
        report=report,
        copied_figures=copied_figures,
        max_images=2,
    )

    assert [item["item_id"] for item in placements] == ["fig2", "fig1"]
    assert placements[1]["section"] == "实验与分析"


def test_extract_figures_tables_does_not_invent_numbered_labels_from_empty_subcaptions(tmp_path):
    content_path = tmp_path / "content_list.json"
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    for name in ("a.jpg", "b.jpg"):
        (image_dir / name).write_bytes(b"jpg")
    content_path.write_text(
        """
[
  {"type": "chart", "img_path": "images/a.jpg", "chart_caption": [], "bbox": [50, 50, 140, 140], "page_idx": 3},
  {"type": "chart", "img_path": "images/b.jpg", "chart_caption": ["(a) ablation"], "bbox": [145, 50, 235, 140], "page_idx": 3}
]
""".strip(),
        encoding="utf-8",
    )

    figures = runner.extract_figures_tables(content_path, source_root=tmp_path)

    assert len(figures) == 2
    assert [figure["label"] for figure in figures] == ["Figure", "Figure"]
    assert [figure["caption"] for figure in figures] == ["", "(a) ablation"]
    assert [figure["cluster_size"] for figure in figures] == [2, 2]


def test_extract_figures_tables_does_not_cluster_unknown_page_items(tmp_path):
    content_path = tmp_path / "content_list.json"
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    for name in ("a.jpg", "b.jpg"):
        (image_dir / name).write_bytes(b"jpg")
    content_path.write_text(
        """
[
  {"type": "chart", "img_path": "images/a.jpg", "chart_caption": [], "bbox": [50, 50, 140, 140]},
  {"type": "chart", "img_path": "images/b.jpg", "chart_caption": [], "bbox": [145, 50, 235, 140]}
]
""".strip(),
        encoding="utf-8",
    )

    figures = runner.extract_figures_tables(content_path, source_root=tmp_path)

    assert len(figures) == 2
    assert [item["cluster_size"] for item in figures] == [1, 1]


def test_extract_figures_tables_keeps_simple_single_table_compatible(tmp_path):
    content_path = tmp_path / "content_list.json"
    image_path = tmp_path / "images" / "table1.png"
    image_path.parent.mkdir(parents=True)
    image_path.write_bytes(b"png")
    content_path.write_text(
        """
[
  {
    "type": "table",
    "content": {
      "image_source": {"path": "images/table1.png"},
      "table_caption": ["Table 1: Main results."]
    },
    "bbox": [20, 40, 220, 260],
    "page_idx": 4
  }
]
""".strip(),
        encoding="utf-8",
    )

    figures = runner.extract_figures_tables(content_path, source_root=tmp_path)

    assert figures == [{
        "label": "Table 1",
        "type": "table",
        "caption": "Table 1: Main results.",
        "source_path": str(image_path.resolve()),
        "source_paths": [str(image_path.resolve())],
        "page": 4,
        "bbox": [20.0, 40.0, 220.0, 260.0],
        "cluster_size": 1,
        "raw_items": [{
            "type": "table",
            "page": 4,
            "bbox": [20.0, 40.0, 220.0, 260.0],
            "caption": "Table 1: Main results.",
            "label": "Table 1",
            "source_path": str(image_path.resolve()),
        }],
    }]
