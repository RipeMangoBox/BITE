# analysis_chain_v1_20260522

## Role

Current optimized paper-analysis chain candidate for default use.

## Git Reference

- Starting base: `3ce08a7 feat: finalize local paper analysis chain`
- Relevant commits before local edits:
  - `f528439 perf: align formal analysis defaults with cache profile`
  - `5c97160 feat: add writer reasoning ab controls`
  - `7ac25e8 docs: align paper state convention with formal analysis chain`
  - `1da1ce4 fix: dedupe direct mineru cache matches`

## Updates

- Cache-oriented defaults: part analysis thinking disabled, writer thinking disabled, main analysis keeps strong reasoning.
- Section writer defaults to serial execution to preserve prompt-cache reuse; `--section-workers` can still be raised for latency/cost A/B.
- Writer reasoning A/B controls available through batch runner.
- MinerU direct cache matching deduplicated.
- Isolated vault export fixed: omitted `--vault-asset-root` now defaults to `<vault-root>/assets/figures/papers`.
- Batch runner supports named variants, per-variant output/vault roots, and `--jobs` local child-process parallelism.
- Batch runner now propagates title/path fields from both `paper_list.csv`-style and ICLR status-ledger-style rows, derives OpenReview links from `openreview_forum_id`, and passes forum id to vault export.
- Lineage/knowledge-positioning prompts now request verified baseline citations such as `**MPGD** (He et al., CVPR 2023)` when the source provides author/year/venue metadata.

## Validation

- 8-paper image-standard run completed: `_private/analysis_chain_eval/analysis_chain_eval_20260522_imgstd_8x4/`.
- Result: 8/8 completed, 0 failures, 8 vault notes, 8 PDFs, 48 assets, 0 missing embeds.
- Estimated API cost for that run: `$0.512557`.
- Structural old/new check on 6 shared notes found no embed regressions; current notes were longer or richer on 4/6 and shorter on 2/6, requiring manual review.
- User review direction on 2026-05-22: new chain is significantly better overall after the requested metadata/citation handling.

## Adoption Policy

Promote as default after manual review confirms no unacceptable regressions in the 8-paper test outputs. If a future strict A/B finds quality regression, keep only non-semantic safety fixes and do not adopt the prompt/default changes.
