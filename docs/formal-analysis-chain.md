# Formal Local Analysis Chain

This page describes the default public-facing ResearchFlow analysis chain in
more detail than the README overview. It clarifies where MinerU-based document
preparation ends and where ResearchFlow's structured analysis begins.

## Overview

ResearchFlow separates PDF preparation from semantic analysis:

- **Stage 0: MinerU preparation** converts batches of PDFs into reusable parsed
  assets.
- **Stage 1 onward: ResearchFlow analysis** consumes those parsed assets and
  turns them into structured evidence, verified analysis objects, sectioned
  reports, and vault notes.

This separation matters because MinerU parsing is an upstream document
preparation stage, while ResearchFlow is the downstream reasoning and knowledge
structuring stage.

## Pipeline

```text
PDF batch
  -> batch MinerU parse or cached parse reuse
  -> Markdown chunking
  -> chunk-level anchor extraction
  -> main analysis JSON
  -> section writers
  -> figure/table visual summary and DeepSeek placement review
  -> vault export
  -> deterministic validation
```

## Stage 0. Batch MinerU Preparation

**Purpose.** Convert source PDFs into Markdown, figure/table metadata, and
image assets before structured analysis starts.

**Inputs.**

- PDF batches under `obsidian-vault/paperPDFs/`
- existing MinerU output directories when available
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
- `--max-note-images 6` keeps notes readable

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

## Data Contract

ResearchFlow can start from any of these inputs:

- `--pdf`
- `--mineru-output`
- `--source-md`

For public batch workflows, the recommended pattern is:

```text
batch MinerU parse -> normalized MinerU outputs -> ResearchFlow analysis
```

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
