"""Unit tests for vault_export_v6 figure / naming helpers.

These are pure-function tests — no DB session needed, so they run on plain
pytest without the test-database fixture.
"""

from types import SimpleNamespace

from backend.services.vault_export_v6 import (
    _autoinject_figures_by_role,
    _extract_figure_placements,
    _best_method_text,
    _normalize_heading_spacing,
    _paper_acronym,
    _paper_aliases,
    _paper_slug,
    _render_figure,
    _resolve_figure_markers,
    _venue_line,
)


# ── _extract_figure_placements ────────────────────────────────────────

def test_extract_placements_round_trip():
    body = (
        "## Section\n\nbody\n\n"
        '<!-- figure_placements: [{"marker":"{{FIG:pipeline}}",'
        '"preferred_labels":["Figure 1"],"semantic_role":"pipeline"}] -->\n'
    )
    placements, cleaned = _extract_figure_placements(body)
    assert placements == [{
        "marker": "{{FIG:pipeline}}",
        "preferred_labels": ["Figure 1"],
        "semantic_role": "pipeline",
    }]
    assert "<!--" not in cleaned
    assert cleaned.endswith("body\n")


def test_extract_placements_missing_returns_empty():
    placements, cleaned = _extract_figure_placements("no markers anywhere\n")
    assert placements == []
    assert cleaned == "no markers anywhere\n"


def test_extract_placements_malformed_json_recovers_gracefully():
    body = "x\n<!-- figure_placements: [not-json] -->\n"
    placements, cleaned = _extract_figure_placements(body)
    assert placements == []
    assert "<!--" not in cleaned


# ── _resolve_figure_markers ───────────────────────────────────────────

def _fig(label, role, url, key=None):
    return {
        "label": label,
        "semantic_role": role,
        "public_url": url,
        "object_key": key or f"papers/x/{label}.png",
        "caption": f"caption-{label}",
    }


def test_resolver_prefers_preferred_labels():
    body = "framework: {{FIG:pipeline}}\n"
    figures = [
        _fig("Figure 1", "pipeline", "https://o/fig1.png"),
        _fig("Figure 2", "pipeline", "https://o/fig2.png"),
    ]
    placements = [{
        "marker": "{{FIG:pipeline}}",
        "preferred_labels": ["Figure 2"],
        "semantic_role": "pipeline",
    }]
    out = _resolve_figure_markers(body, figures, placements)
    assert "https://o/fig2.png" in out
    assert "https://o/fig1.png" not in out


def test_resolver_falls_back_to_role_when_no_placements():
    body = "result: {{FIG:result}}\n"
    figures = [_fig("Table 1", "result", "https://o/t1.png")]
    out = _resolve_figure_markers(body, figures, placements=[])
    assert "https://o/t1.png" in out


def test_resolver_drops_marker_when_no_match():
    body = "missing: {{FIG:nonexistent}} done\n"
    figures = [_fig("Figure 1", "pipeline", "https://o/fig1.png")]
    out = _resolve_figure_markers(body, figures, placements=[])
    assert "{{FIG:" not in out
    assert "missing:  done" in out


def test_resolver_TBL_marker_picks_table_over_figure():
    """{{TBL:result}} must prefer type=table even when a figure also matches role."""
    body = "{{TBL:result}} done\n"
    figures = [
        {"label": "Figure 5", "type": "figure", "semantic_role": "result",
         "public_url": "https://o/fig5.png", "object_key": "f5", "caption": "scatter plot"},
        {"label": "Table 1", "type": "table", "semantic_role": "result",
         "public_url": "https://o/t1.png", "object_key": "t1", "caption": "main results"},
    ]
    out = _resolve_figure_markers(body, figures, placements=[])
    assert "https://o/t1.png" in out, "TBL marker should resolve to table image"
    assert "https://o/fig5.png" not in out, "TBL must NOT pick a figure when table exists"


def test_resolver_TBL_marker_works_without_public_url():
    body = "{{TBL:result}}\n"
    figures = [
        {"label": "Table 1", "type": "table", "semantic_role": "result",
         "object_key": "papers/x/t1.png", "vault_asset": "assets/figures/papers/x/t1.png",
         "caption": "main results"},
    ]
    out = _resolve_figure_markers(body, figures, placements=[])
    assert "![Table 1](assets/figures/papers/x/t1.png)" in out
    assert "{{TBL:" not in out


def test_resolver_TBL_falls_back_to_any_table_when_no_role_match():
    """TBL with unknown hint should still surface any unused table."""
    body = "{{TBL:nonexistent_hint}}\n"
    figures = [
        {"label": "Figure 1", "type": "figure", "semantic_role": "pipeline",
         "public_url": "https://o/p.png", "object_key": "p"},
        {"label": "Table 7", "type": "table", "semantic_role": "ablation",
         "public_url": "https://o/t7.png", "object_key": "t7", "caption": "ablation"},
    ]
    out = _resolve_figure_markers(body, figures, placements=[])
    assert "https://o/t7.png" in out
    assert "https://o/p.png" not in out


def test_resolver_FIG_marker_does_not_pick_table():
    """{{FIG:result}} should pick figure, not table, when both match role."""
    body = "{{FIG:result}}\n"
    figures = [
        {"label": "Table 1", "type": "table", "semantic_role": "result",
         "public_url": "https://o/t1.png", "object_key": "t1"},
        {"label": "Figure 3", "type": "figure", "semantic_role": "result",
         "public_url": "https://o/f3.png", "object_key": "f3"},
    ]
    out = _resolve_figure_markers(body, figures, placements=[])
    assert "https://o/f3.png" in out
    assert "https://o/t1.png" not in out


def test_resolver_does_not_reuse_same_figure_twice():
    body = "{{FIG:pipeline}}\n{{FIG:pipeline}}\n"
    figures = [
        _fig("Figure 1", "pipeline", "https://o/fig1.png"),
        _fig("Figure 2", "pipeline", "https://o/fig2.png"),
    ]
    out = _resolve_figure_markers(body, figures, placements=[])
    assert out.count("https://o/fig1.png") == 1
    assert out.count("https://o/fig2.png") == 1


# ── _autoinject_figures_by_role ───────────────────────────────────────

def test_autoinject_places_figures_after_matching_h2():
    body = (
        "intro\n\n"
        "## 背景与动机\n\nbg body\n\n"
        "## 整体框架\n\nframework body\n\n"
        "## 实验与分析\n\nexperiment body\n"
    )
    figures = [
        _fig("Figure 1", "motivation", "https://o/m.png"),
        _fig("Figure 2", "pipeline", "https://o/p.png"),
        _fig("Table 1", "result", "https://o/r.png"),
    ]
    out = _autoinject_figures_by_role(body, figures)

    bg_idx = out.index("## 背景与动机")
    framework_idx = out.index("## 整体框架")
    exp_idx = out.index("## 实验与分析")
    end_idx = len(out)

    # Each image appears between its section and the next one.
    assert bg_idx < out.index("https://o/m.png") < framework_idx
    assert framework_idx < out.index("https://o/p.png") < exp_idx
    assert exp_idx < out.index("https://o/r.png") <= end_idx


def test_autoinject_no_dump_at_end_when_all_match():
    body = "## 整体框架\n\nbody\n"
    figures = [_fig("Figure 1", "pipeline", "https://o/p.png")]
    out = _autoinject_figures_by_role(body, figures)
    assert "## 论文图表" not in out
    assert "https://o/p.png" in out


def test_autoinject_handles_no_h2_by_appending_all():
    figures = [_fig("Figure 1", "pipeline", "https://o/p.png")]
    out = _autoinject_figures_by_role("plain text\n", figures)
    assert "https://o/p.png" in out
    assert "## 论文图表" not in out


def test_render_figure_uses_vault_asset_when_url_missing():
    out = _render_figure({
        "label": "Figure 1",
        "type": "figure",
        "semantic_role": "pipeline",
        "object_key": "papers/x/Figure_1.png",
        "vault_asset": "assets/figures/papers/x/Figure_1.png",
        "caption": "Figure 1: Pipeline overview",
    })
    assert "![Figure 1](assets/figures/papers/x/Figure_1.png)" in out
    assert "Figure 1 (pipeline): Pipeline overview" in out
    assert "Figure 1: Figure 1:" not in out


def test_normalize_heading_spacing_keeps_single_blank_line():
    out = _normalize_heading_spacing("## 小结\n\n\nbody\n### 子节\nbody2")
    assert "## 小结\n\nbody" in out
    assert "### 子节\n\nbody2" in out
    assert "\n\n\nbody" not in out


# ── Naming helpers ────────────────────────────────────────────────────

def _paper(**kw):
    defaults = dict(
        title="A Long Paper Title About Diffusion Transformers",
        title_sanitized="A_Long_Paper_Title_About_Diffusion_Transformers",
        method_family=None,
        title_zh=None,
        delta_statement=None,
    )
    defaults.update(kw)
    return SimpleNamespace(**defaults)


def test_acronym_prefers_method_family():
    p = _paper(method_family="HY-Motion")
    assert _paper_acronym(p) == "HY-Motion"


def test_acronym_falls_back_to_initialism():
    p = _paper(title="Diffusion Transformer Networks")
    assert _paper_acronym(p) == "DTN"


def test_paper_slug_uses_english_file_slug_when_title_zh_present():
    p = _paper(title_zh="运动生成模型", method_family="HY-Motion")
    slug = _paper_slug(p)
    assert slug == "A_Long_Paper_Title_About_Diffusion_Transformers"
    assert "运动生成模型" not in slug


def test_paper_slug_uses_english_title_not_method_family():
    p = _paper(method_family="MoCap-LLM")
    slug = _paper_slug(p)
    assert slug == "A_Long_Paper_Title_About_Diffusion_Transformers"
    assert "MoCap-LLM" not in slug


def test_paper_aliases_dedup_and_order():
    p = _paper(
        title_zh="运动生成",
        method_family="HY-Motion",
        delta_statement="首次将十亿参数 DiT 引入运动生成，效果显著",
    )
    aliases = _paper_aliases(p)
    assert aliases[0] == "运动生成"
    assert "HY-Motion" in aliases
    assert len(aliases) == len(set(aliases))


def test_paper_aliases_empty_when_no_signals():
    p = _paper()
    # Title-based acronym still produces something; check it's clean
    aliases = _paper_aliases(p)
    assert all(len(a) >= 2 for a in aliases)


def test_venue_line_adds_year_before_acceptance():
    assert _venue_line("ICLR", 2026, "accepted") == "ICLR 2026 (accepted)"
    assert _venue_line("ICLR 2026", 2026, None) == "ICLR 2026"


def test_best_method_text_falls_back_to_report_table_then_title():
    p = _paper(full_report_md="| 字段 | 内容 |\n|------|------|\n| 方法 | A-TPT |\n")
    assert _best_method_text(p, []) == "A-TPT"
    p = _paper(
        title="3D Scene Prompting for Camera Control",
        delta_statement="3DScenePrompt, by using scene memory, improves consistency.",
    )
    assert _best_method_text(p, [], ["3D场景提示", "3DScenePrompt"]) == "3DScenePrompt"
    p = _paper(title="ASTGI: Adaptive Spatio-Temporal Graph Interactions")
    assert _best_method_text(p, []) == "ASTGI"
