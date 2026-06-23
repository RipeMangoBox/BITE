---
name: paper-report
follows: rf-obsidian-markdown
description: Generates deep structured reports for single papers with formula derivation, pipeline module decomposition, experiment analysis, and recursive related work. Use when the user asks for a "deep report", "detailed paper analysis", or "公式推导" for a specific paper. Requires a PDF path or paper title as input.
---

# PaperReport — Deep Structured Paper Report

This skill is the user-facing spec for a deep single-paper report. In the
current local workflow, use it as the writing contract when a user asks for a
deep report, detailed paper analysis, or formula derivation.

A deep report is a compact linear narrative that a reader can scroll
top-to-bottom and finish with a complete understanding of the paper:
problem → core mechanism → formulas → experiments → position.

---

## Input

- A PDF path under `obsidian-vault/paperPDFs/` (preferred), OR
- A paper title already present in the knowledge base.

Useful upstream artifacts before this skill runs:
- A readable PDF or extracted paper text.
- Figure/table captions when available.
- Existing local analysis notes or related-work notes when available.

## Output

- A local Markdown report following the four-section structure below.
- If saved into the vault, place it under `obsidian-vault/analysis/` using the
  current repository naming convention.

---

## Section Spec (exactly 4 sections, in this order)

| # | section_type          | title             | length (chars) | must contain                                  |
|---|-----------------------|-------------------|----------------|-----------------------------------------------|
| 1 | `summary`             | 概要              | 150-250        | 问题 + 方法 + 主要结果 + 方法定位 |
| 2 | `method_mechanism`    | 核心方法与创新机理 | 1800-2800    | 唯一瓶颈 + changed slots + pipeline/机制 + 1-3 个关键公式 |
| 3 | `experiment_findings` | 实验与关键发现    | 1500-2400      | 主结果 + 指标对比表/图 + 消融 + 失败模式/适用边界 |
| 4 | `kb_positioning`      | 定位与知识库关联  | 500-900        | 方法族 + 与 baseline 的本质差异 + 后续方向 + facets |

Total length: 4500-7000 Chinese characters. Avoid repeating the same
bottleneck, formula, dataset fact, or metric across sections.

### Section 1 (summary) detailed format

```markdown
| 中文题名 | {title_zh} |
|----------|------------|
| 英文题名 | {title_en} |
| 会议/期刊 | {venue} ({acceptance_type}) |
| 链接 | [arXiv]({arxiv_url}) · [Code]({code_url}) ⭐{stars} · [Project]({project_url}) |
| 主要任务 | {tasks} |
| 主要 baseline | {baselines} |

> [!abstract] TL;DR
> 因为「{problem}」，作者在「{baseline}」基础上改了「{change}」，在「{benchmark}」上取得「{result}」

**关键性能**:
- {benchmark1}: {metric1} {value1} (vs {baseline}: +{delta})
- {benchmark2}: {metric2} {value2}
```

The current vault exporter renders metadata separately; the report section
itself should start with `## 概要` and stay short.

---

## Formula Derivation Rules (Section 2, CRITICAL)

The archived legacy Markdown fallback avoided formula derivation. This skill
does the **opposite** — formula derivation is a core deliverable of
`核心方法与创新机理`.

For each of the 2-3 most important modules:

```
### 模块 N: {名称}（对应框架图 {位置标注}）

**直觉**: 一句话为什么这样设计

**Baseline 公式** ({baseline_name}): $$L_{base} = \mathbb{E}[\dots]$$
符号: $\theta$ = ..., $A_t$ = ...   (only key symbols)

**变化点**: 为什么 baseline 不够 → 改了什么假设/项/权重

**本文公式（推导）**:
$$\text{Step 1}: \dots \quad \text{加入 X 项以解决 Y}$$
$$\text{Step 2}: \dots \quad \text{重归一化以保证 Z}$$
$$\text{最终}: L_{final} = \dots$$

**对应消融**: Table N 显示移除该项 ΔX%
```

Rules:
1. Always show the baseline formula first when one exists.
2. Each derivation step must explain WHY (not just WHAT) changed.
3. Tie every formula to the framework module and an ablation row.
4. Pick the 1-3 most important formulas — quality over quantity.

---

## Figure Placement Rules

The agent must:

1. Inspect the `figures_available` list passed in the prompt context (each
   entry has `label`, `semantic_role`, `caption`).
2. Use `{{FIG:xxx}}` markers ONLY for figures that exist in that list.
3. For each marker, output a `figure_placements` entry:
   ```json
   {"marker": "{{FIG:pipeline}}",
    "preferred_labels": ["Figure 1", "Figure 2"],
    "semantic_role": "pipeline",
    "section_hint": "framework_overview"}
   ```
4. Distribute markers across the narrative — never cluster all figures in
   one place, never dump them at the end.

Preferred markers when a matching figure exists:
- `method_mechanism` → motivation/problem figure and `{{FIG:pipeline}}` or `{{FIG:architecture}}`
- `experiment_findings` → `{{FIG:result}}` or a metric comparison table

Do not use sample galleries as filler. A split pipeline may use two figures.
For normal papers, keep the final note to roughly 3-6 figure/table embeds.

The Obsidian exporter (`vault_export_v6._resolve_figure_markers`) resolves
each marker by:
1. Looking up `preferred_labels` in the figure list (exact label match);
2. Falling back to `semantic_role` match;
3. Dropping the marker if nothing fits.

If the report has NO markers at all (legacy reports), figures are
auto-injected by `_autoinject_figures_by_role` at the end of the matching
section block — never as a "## 论文图表" trailer.

---

## Quality Checklist

Before finalizing the report, the agent should verify:

- [ ] Section 1 metadata table has venue, links, baselines.
- [ ] TL;DR is one因果sentence, not bullet points.
- [ ] Section 4 starts with a framework figure marker.
- [ ] Section 5 derives at least one formula from a baseline.
- [ ] Section 5 ties each formula to an ablation row.
- [ ] Section 6 has main results as a markdown table with Δ column.
- [ ] Section 7 names the parent method explicitly.
- [ ] Every `{{FIG:xxx}}` marker has a matching `figure_placements` entry.
- [ ] Total length 4000-7000 Chinese characters.
