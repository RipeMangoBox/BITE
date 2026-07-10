# RF OSS Release And Batch Analysis Fixes

Date: 2026-05-20

Scope:

- Keep ICLR analysis results private.
- Prepare the repository for a cleaned open-source snapshot.
- Make preprocessed MinerU outputs usable without adding MinerU paths to `obsidian-vault/paper_list.csv`.
- Clarify whether single-paper and `Downloaded` queue analysis should be scripted or agent-managed.

## Todo

- [x] A1. Record every release/batch fix here and tick items as they are completed.
- [x] A1. Keep private notes, release audit material, raw ICLR data, generated indexes, analysis notes, PDFs, and runtime logs under `_private/` or ignored vault paths.
- [x] A1. Remove public references to obsolete ICLR-only handoff/docs and old backend release surfaces, or move still-useful material into `_private/`.
- [x] A1. Update public docs/skills so non-ICLR usage and raw-copy cleanup assumptions are explicit.
- [x] A1. Check dependency paths after moving/removing obsolete content.
- [x] A1. Move scattered `_private` root planning/review/backup files into `_private/planning/`, `_private/reviews/`, and `_private/backups/`.
- [x] A1. Refresh `_private/PRIVATE_REGISTRY.md` as the current private workspace map.
- [x] A2. Add a dry-run/apply script to normalize `_private/iclr26_batch/mineru_outputs` from `batch_id/random_code/paper_dir` into `batch_id/paper_dir`.
- [x] A2. Add a dry-run/apply script to move `mineru_stdout.log`, `mineru_stderr.log`, and related command/log files from the random-code parent into the lifted paper directory.
- [x] A2. Add code support for locating normalized MinerU outputs from paper title and optional batch id, without adding a MinerU column to `paper_list.csv`.
- [x] A2. Update batch-analysis instructions so workers use normalized MinerU lookup before falling back to PDF parsing.
- [x] A2. Record incomplete MinerU directories that should not be treated as reusable parse outputs.
- [x] A3. Decide and document the robust path for single-paper analysis and `paper_list.csv` `Downloaded` queue analysis.
- [x] A3. Add a scripted queue runner if the existing chain should not rely on agent-only orchestration.
- [x] A3. Verify the new commands in dry-run/mock mode.

## Decisions

- Do not add MinerU mapping columns to `obsidian-vault/paper_list.csv`.
- Prefer deterministic private directory layout over per-row MinerU mapping.
- Raw packaging plan: copy the repository, then remove ignored content. This still requires a clean allowlist check before publishing.
- Single-paper analysis should stay in `scripts/run_local_paper_analysis.py`.
- `paper_list.csv` `Downloaded` queue analysis should get a thin scripted runner; agent-only orchestration is not robust enough for repeatable batch recovery.
- Existing private ICLR26 workflow remains supported through `_private/iclr26_batch/tools/run_local_iclr26_batch.py`, which supplies ICLR-specific defaults explicitly.
- Incomplete MinerU directories without `auto/` are failure evidence, not reusable cache entries.
