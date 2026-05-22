# Formal Local Analysis Chain

This page documents the default ResearchFlow paper analysis chain in more
detail than the README overview. It explains what each stage does, which
reasoning settings are used, and why those settings are currently the default.

The current production profile was selected after a 100-paper ICLR 2026 batch
run:

- Completion: 100/100 papers reached `DONE`.
- Median note length: about 17k characters.
- Median end-to-end time: about 655 seconds per paper.
- API cost: about 0.067 USD per paper in the measured run.
- Image export: Obsidian embeds use `![[assets/...]]`; PDF embeds use
  `![[paperPDFs/...]]`.

## Pipeline

```text
PDF / MinerU output
  -> MinerU parse or cached parse reuse
  -> Markdown chunking
  -> chunk-level anchor extraction
  -> main analysis JSON
  -> section writers
  -> figure/table visual summary and placement
  -> vault export
  -> deterministic validation
```

## 1. Parse / Reuse

**Purpose.** Convert the source PDF into Markdown, figure/table metadata, and
image assets. If a compatible MinerU output already exists, the runner reuses it
instead of parsing the PDF again.

**Inputs.**

- `--pdf`: source PDF to parse.
- `--mineru-output`: existing single-paper MinerU output.
- `--mineru-output-root` plus `--require-existing-mineru-output`: normalized
  cache mode for batch runs.

**Outputs.**

- `parse/full.md`
- `parse/content_list.json` when available
- `parse/figures_tables.json`

**Reasoning effort.** None. This stage is deterministic local parsing.

**Why.** Parsing should not consume LLM budget, and idempotent reuse keeps batch
runs stable.

## 2. Chunk-Level Anchor Extraction

**Purpose.** Split parsed Markdown into chunks and extract grounded anchors:
method claims, experiment evidence, formula evidence, figure/table roles, and
open questions. This avoids asking one model call to summarize the whole paper
from scratch.

**Default settings.**

- `--chunk-chars 8000`
- `--overlap-chars 800`
- `--part-workers 2`
- `--part-thinking disabled`
- `--part-reasoning-effort high`

**Reasoning effort rationale.**

Chunk extraction is an evidence-harvesting stage, not the final synthesis
stage. Disabling thinking reduces latency and cost while still preserving
anchors, because each chunk has limited local context. `high` reasoning effort
is kept as the API-level quality hint for difficult chunks and repairs.

**Outputs.**

- `part_analysis/part_XXX.json`
- `part_analysis/part_XXX.raw.txt`

**Validation expectations.**

- Every chunk should produce a normalized part-analysis JSON.
- Empty or malformed outputs are repaired or replaced with source-visible local
  fallback anchors.

## 3. Main Analysis JSON

**Purpose.** Merge chunk anchors, compact paper context, and figure/table
metadata into a single verified analysis object. This is the main semantic
reasoning stage.

**Default settings.**

- `--thinking enabled`
- `--reasoning-effort high`
- Adaptive main context and token budgets enabled.

**Reasoning effort rationale.**

This stage decides the paper-level causal story: bottleneck, changed slot,
method logic, decisive evidence, limitations, and open questions. It has the
highest risk of semantic compression error, so thinking is enabled here.

**Outputs.**

- `analysis/main_analysis.json`
- `analysis/main_analysis.raw.txt`

**Validation expectations.**

- Required JSON fields are normalized.
- Malformed JSON is repaired.
- Key metrics and method terms from chunk evidence are preserved where possible.

## 4. Section Writers

**Purpose.** Generate the final report sections from verified analysis and
focused evidence. Each section receives the global analysis plus filtered
part/figure context.

**Default settings.**

- `--section-workers 1`
- `--writer-thinking disabled`
- `--writer-reasoning-effort high`

**Reasoning effort rationale.**

Writers should synthesize verified evidence rather than rediscover the paper.
Thinking is disabled to reduce latency and avoid over-generation. Section
workers are serialized by default because this gave strong prompt-cache reuse in
batch tests; the writer cache-hit median was about 0.60 with
`section_workers=1`.

Increasing `section_workers` can reduce wall time, but it should be tested
against cache hit rate, writer cost, and cross-section consistency before
becoming the default.

**Outputs.**

- `report/sections/<section>.md`
- `report/final_report.md`

## 5. Figure/Table Visual Summary and Placement

**Purpose.** Enrich selected MinerU figure/table items and place the most useful
ones into the note. The placement target is either `整体框架` or `实验与分析`.

**Default behavior.**

- Kimi is used for visual summary and placement when enabled.
- Caption-only fallback is available.
- `--max-note-images 6` keeps notes readable and avoids turning reports into
  image dumps.

**Reasoning effort.** Kimi visual calls run with thinking disabled. This is a
local relevance/routing task, not a paper-level reasoning task.

**Outputs.**

- `parse/figure_visual_summaries.json`
- `report/figure_placements.json`
- copied assets under `obsidian-vault/assets/figures/papers/...`

## 6. Vault Export

**Purpose.** Write the Obsidian analysis note, copy the source PDF into the
vault, and copy selected figure/table assets.

**Output conventions.**

- Notes: `obsidian-vault/analysis/<Venue_Year>/<Title>.md`
- PDFs: `obsidian-vault/paperPDFs/<Venue_Year>/<Title>.pdf`
- Images: `obsidian-vault/assets/figures/papers/<task_id>/figures/...`
- PDF embeds: `![[paperPDFs/...]]`
- Image embeds: `![[assets/...]]`

The image embed deliberately omits `../../`. Obsidian can resolve partial vault
paths, and the shorter vault-relative path is less fragile if users move or
reorganize note folders.

## 7. Deterministic Validation

The export validator currently checks:

- YAML frontmatter exists and required keys are present.
- OpenReview forum id matches when provided.
- Required report sections are present.
- PDF embed exists.
- Expected image embeds exist and use `![[assets/...]]`.
- Legacy image links such as `![...](../../assets/...)` are rejected.
- `PDF 文件：` labels are not emitted.
- Aliased wikilinks do not appear inside Markdown tables.
- fallback markers such as `待人工复核` do not remain in metadata or the top
  note summary.
- dangling numeric references are avoided outside formulas.
- note length is not obviously truncated.

Validation is structural. It does not prove that every claim is semantically
correct; semantic audits should be handled by sampling, LLM-as-judge checks, or
human review.

## Current Bottlenecks

Measured on the 100-paper ICLR 2026 run:

| Stage | Median wall time | Cost share | Cache behavior |
| --- | ---: | ---: | --- |
| part extraction | 78 s | about 35% | low median cache hit, parallelized |
| main analysis | 223 s | about 36% | very low cache hit |
| section writing | 234 s | about 29% | high cache hit with `section_workers=1` |

The highest-value next optimizations are:

1. Improve main-analysis prompt cacheability.
2. A/B test lower writer reasoning effort while holding main analysis fixed.
3. Improve part prompt fixed-prefix reuse without losing parallel throughput.

## Reproducible Command

```bash
python3 scripts/run_local_paper_analysis.py \
  --pdf "obsidian-vault/paperPDFs/<Venue_Year>/<Paper>.pdf" \
  --conf-year "<Venue_Year>" \
  --export-vault \
  --reasoning-effort high \
  --part-reasoning-effort high \
  --part-thinking disabled \
  --writer-reasoning-effort high \
  --writer-thinking disabled \
  --section-workers 1 \
  --thinking enabled
```
