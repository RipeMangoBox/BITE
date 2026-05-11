# ICLR 5k Reanalysis Contract

## Goal

Run the next ResearchFlow analysis wave from raw inputs, not from retired
Markdown outputs. PostgreSQL remains the only write target; Markdown/vault files
are regenerated projections.

## Current State Before Rerun

- `obsidian-vault/`, `paperAnalysis/`, and `paperCollection/` are intentionally
  empty entry points with README files only.
- Legacy generated outputs live under
  `_private/archives/past_versions/2026-05-09-current-analysis-retired-before-iclr5k-rerun/`.
- Raw inputs remain in `_private/resmax_downloads/{manifest.jsonl,pdfs/,meta/}`
  and `paperPDFs/`.

## Required Pipeline Shape

1. Import/select papers from the manifest or backend APIs.
2. Parse PDFs through the parse layer with MinerU attempted for score/L2+
   papers; image upload to LLMs remains disabled by default.
3. Run `analysis_agent` once per qualified paper to produce analysis truth and
   compatibility projections.
4. Materialize DeltaCard, evidence, graph assertions, taxonomy facets, method
   profiles, and paper-paper relations deterministically.
5. Run `writer_agent` after relation materialization. Writer context must include
   only latest verified blackboard items, selected evidence, text-only figure
   metadata, and deterministic lineage/facet context.
6. Export `obsidian-vault/` as the canonical human navigation surface with:
   - `paper/` per-paper reports
   - `00_Home/` overview
   - `dataset/`, `method/`, and `domain/` indexes
   - `assets/` and `paperPDFs/` for exported media/PDF copies

## Rerun Semantics

Default pipeline calls are idempotent and skip papers that already have current
L4 analysis. Full re-analysis batches must explicitly pass
`force_reanalyze=True` through `run_for_existing_paper()` or the worker task.
The comparison script `scripts/reanalyze_and_compare.py` does this by default.

## Module Requirements

`## 方法谱系与知识库定位` is no longer allowed to be a weak template. It must be
backed by deterministic context where available:

- direct baselines and method sources from `paper_relations`
- method family and parent method from `method_nodes`
- task/domain/dataset/modality/paradigm facets from `paper_facets`
- method profile summaries from `kb_node_profiles`
- changed slots and follow-up directions from verified analysis truth

If any of these are absent, the writer should state only the supported subset and
avoid fabricating a lineage.

## Export Policy

`obsidian-vault/` is the source of human-facing multi-dimensional navigation.
`paperCollection/` is a lightweight compatibility export only and must not be
used as the canonical dataset/method/domain index.
