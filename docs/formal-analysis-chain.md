# Formal Local Analysis Chain

This page describes the default public-facing BITE analysis chain in more
detail than the README overview. MinerU is now integrated into the formal local
runner: existing parse outputs can be reused, but a separate MinerU batch phase
is no longer required before analysis.

## Overview

BITE's formal runner accepts a PDF, an existing MinerU output directory, or a
Markdown source:

- `--pdf` runs MinerU when no matching cached parse is available.
- `--mineru-output` reuses an existing parse directory.
- `--source-md` is reserved for tests and recovery work.

The same run then turns parsed paper evidence into structured analysis objects,
sectioned reports, figure/table-aware notes, and deterministic validation
records.

The current default note format is the v06 four-section chain:

- `概要`
- `核心方法与创新机理`
- `实验与关键发现`
- `定位与知识库关联`

This replaces the older seven-section format that separately expanded
background, innovation, framework, formulas, experiments, and method lineage.
The four-section chain is intentionally denser: it preserves source anchors and
method/experiment evidence while reducing repeated prose, duplicated caption
blocks, and non-core supplemental tables.

## Pipeline

```text
PDF batch
  -> MinerU parse or cached parse reuse
  -> Markdown chunking
  -> chunk-level anchor extraction
  -> main analysis JSON
  -> section writers
  -> figure/table visual summary and DeepSeek placement review
  -> vault export
  -> deterministic validation
```

## Quality and Cost Controls

The v06 chain lowers per-paper analysis cost without weakening the evidence
contract by moving repeated work into structured intermediate artifacts:

- chunk-level anchor extraction captures only grounded method, formula,
  experiment, figure/table, and limitation evidence;
- the main analysis JSON merges anchors before prose generation, so section
  writers receive compact verified context rather than the full paper text;
- section writers produce four focused body sections instead of the older
  seven-section report;
- figure/table placement uses a slot budget and defaults to
  `--max-note-images 6`, keeping only motivation, core method/pipeline, and
  key result/ablation visuals;
- deterministic validation catches structural export failures before notes are
  treated as usable knowledge-base entries.

For large downloaded queues, `scripts/run_paper_list_analysis.py` can safely
drive many independent child analyses. When model quota, MinerU I/O, and local
memory are sufficient, the recommended high-throughput setting is:

```bash
python3 scripts/run_paper_list_analysis.py \
  --source obsidian-vault/paper_list.csv \
  --state Downloaded \
  --jobs 50 \
  --export-vault \
  --max-note-images 6
```

If the provider starts rate limiting, or if local parsing becomes the bottleneck,
drop to `--jobs 10` or `--jobs 20` and rerun with the default resume behavior.

## Stage 0. MinerU Parse or Reuse

**Purpose.** Convert a source PDF into Markdown, figure/table metadata, and
image assets, or reuse an existing parse directory.

**Inputs.**

- a PDF under `obsidian-vault/paperPDFs/`
- an existing MinerU output directory via `--mineru-output`
- normalized MinerU cache roots such as `--mineru-output-root`

**Outputs.**

- parsed Markdown
- content lists when available
- figure/table metadata
- local MinerU image assets

**Properties.**

- deterministic local parsing
- no LLM budget consumption
- reusable across repeated analysis runs
- integrated into the formal analysis runner by default

## Stage 1. Chunk-Level Anchor Extraction

**Purpose.** Split parsed Markdown into chunks and extract grounded anchors:
method claims, experiment evidence, formula evidence, figure/table roles, and
open questions.

**Default settings.**

- `--chunk-chars 8000`
- `--overlap-chars 800`
- `--part-workers 2`
- `--part-thinking disabled`
- `--part-reasoning-effort max`

**Outputs.**

- `part_analysis/part_XXX.json`
- `part_analysis/part_XXX.raw.txt`

## Stage 2. Main Analysis JSON

**Purpose.** Merge chunk anchors, compact paper context, and figure/table
metadata into one verified analysis object.

**Default settings.**

- `--thinking enabled`
- `--reasoning-effort max`

**Outputs.**

- `analysis/main_analysis.json`
- `analysis/main_analysis.raw.txt`

## Stage 3. Section Writers

**Purpose.** Generate final report sections from verified analysis and focused
evidence.

**Default settings.**

- `--section-workers 1`
- `--writer-thinking disabled`
- `--writer-reasoning-effort max`

**Outputs.**

- `report/sections/<section>.md`
- `report/final_report.md`

## Stage 4. Figure/Table Summary and Placement

**Purpose.** Enrich selected MinerU figure/table items and place the most
useful ones into the note.

**Default behavior.**

- DeepSeek is the default figure/table placement reviewer.
- Caption-only visual summaries are used with DeepSeek; image-capable visual
  summaries are available through `openai` or `kimi`.
- Caption/placement fallback is available only for explicit offline runs
  (`--figure-provider none`) or mock runs.
- `--max-note-images 6` keeps notes readable and prevents supplemental figure
  dumps from dominating the final note.

**Outputs.**

- `parse/figure_visual_summaries.json`
- `report/figure_placements.json`
- copied assets under `obsidian-vault/assets/figures/papers/...`

## Stage 5. Vault Export

**Purpose.** Write the Obsidian analysis note, copy the source PDF into the
vault, and copy selected figure/table assets.

**Output conventions.**

- Notes: `obsidian-vault/analysis/<Venue_Year>/<Title>.md`
- PDFs: `obsidian-vault/paperPDFs/<Venue_Year>/<Title>.pdf`
- Images: `obsidian-vault/assets/figures/papers/<task_id>/figures/...`
- Frontmatter keeps `title`, `type`, `paper_level`, `venue`, `year`,
  `pdf_ref`, `project_link`, `code_link`, `aliases`, `tags`, `core_operator`,
  `primary_logic`, and `claims`.
- `project_link` and `code_link` are present with `null` values when unknown.
- `Links` table entries use `[paper](...)` for the paper page/PDF URL; arXiv
  should not be duplicated as a separate display label when it points to the
  same paper identity.
- PDF embeds: `![[paperPDFs/...]]`
- Image embeds: `![[assets/...]]`
- Figure/table captions escape Obsidian reserved `<` characters as `\<`.

## Stage 6. Deterministic Validation

The export validator checks:

- YAML frontmatter exists and required keys are present
- required report sections are present
- PDF embed exists
- expected image embeds exist and use `![[assets/...]]`
- aliased wikilinks do not appear inside Markdown tables
- image captions do not contain unescaped `<`
- fallback markers do not remain in metadata or the top summary
- note length is not obviously truncated

Validation is structural. It does not prove semantic correctness; semantic
audits should be handled by sampling, LLM-as-judge checks, or human review.

A successful deterministic export advances a queued paper from `Downloaded`
to `analysised`. The later semantic/content-quality review is a separate gate
that promotes `analysised` to `checked`; the analysis runner must not collapse
these two guarantees into one state.

## Data Contract

BITE can start from any of these inputs:

- `--pdf`
- `--mineru-output`
- `--source-md`

For public batch workflows, the recommended pattern is:

```text
paper_list.csv Downloaded rows -> run_paper_list_analysis.py -> per-row formal analysis runs
```

If you already have normalized MinerU outputs, pass `--mineru-output-root` to
reuse them. Use `--require-existing-mineru-output` only for controlled
maintenance runs where accidental re-parsing should fail.

## Reproducible Command

```bash
python3 scripts/run_local_paper_analysis.py \
  --pdf "obsidian-vault/paperPDFs/<Venue_Year>/<Paper>.pdf" \
  --conf-year "<Venue_Year>" \
  --export-vault \
  --reasoning-effort max \
  --part-reasoning-effort max \
  --part-thinking disabled \
  --writer-reasoning-effort max \
  --writer-thinking disabled \
  --section-workers 1 \
  --thinking enabled
```
