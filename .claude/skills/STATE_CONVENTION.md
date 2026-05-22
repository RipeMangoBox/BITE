# Paper State Convention

Unified definitions for the `state` column in `paper_list.csv`. All skills must follow this convention.

## State flow

```
Wait → Downloaded → checked
  │        │
  │        ├→ too_large          (PDF cannot be parsed within local limits)
  │        └→ analysis_mismatch  (analysis/export validation failed)
  │
  ├→ Skip     (user manually excluded)
  └→ Missing  (download failed, PDF unavailable)
```

## Main pipeline states

| state | Meaning | Written by | Next action |
|-------|---------|------------|-------------|
| `Wait` | Newly collected candidate, waiting for download | collect (from-web / from-github-awesome) | Run download |
| `Downloaded` | PDF exists under `obsidian-vault/paperPDFs/` or a reviewed local path is registered in `pdf_path`; ready for the formal local analysis chain | download / import-local-pdfs / Zotero sync | Run analyze |
| `checked` | Structured analysis note exists under `obsidian-vault/analysis/`; when `--export-vault` is used, deterministic vault validation passed | analyze / reviewed batch consolidation | Ready for query / build index |

## Abnormal states (from analyze stage)

| state | Meaning | Written by | Recovery |
|-------|---------|------------|----------|
| `analysis_mismatch` | Analysis or vault export exists but validation failed: required sections/frontmatter/PDF embed/image embeds, table wikilink safety, fallback markers, numeric refs, or note length need review | analyze / audit / reviewed batch consolidation | Re-run analyze on this entry, or manually repair the note and set state to `checked` after validation |
| `too_large` | PDF cannot be parsed by the local MinerU/analysis environment within current size or resource limits | analyze / download repair | Manually compress, split, or replace the PDF, then set state back to `Downloaded` |

## Out-of-band states
| state | Meaning | Written by | Recovery |
|-------|---------|------------|----------|
| `Skip` | Manually filtered out, not processed | User (manual edit) | Set back to `Wait` if reconsidered |
| `Missing` | PDF unavailable after repeated download attempts | download (`papers-download-from-list`) | Retry later, or manually place PDF then set to `Downloaded` |

## Rules

1. Main pipeline moves forward only: `Wait → Downloaded → checked`.
2. `Skip` and `Missing` are set from `Wait`; `too_large` and `analysis_mismatch` are set from `Downloaded`.
3. Only the user may revert a state (e.g. `Missing → Wait`, `too_large → Downloaded`).
4. `scripts/run_local_paper_analysis.py` writes per-run `.state` files
   (`RUNNING`, `PLANNED`, `DONE`, `FAILED`) inside the analysis work directory.
   These are child-run states and must not be copied into `paper_list.csv`.
5. The formal analysis chain may start from `--pdf`, `--mineru-output`, or
   `--source-md`. Reusing MinerU output does not change the `paper_list.csv`
   state by itself.
6. `scripts/run_paper_list_analysis.py` keeps the source `paper_list.csv`
   unchanged by default and records per-row results under
   `obsidian-vault/batches/<run_id>/`. A manager may consolidate reviewed
   successes to `checked` after outputs and validation are confirmed.
7. Each skill only processes entries at its own input state:
   - download processes `Wait`
   - analyze processes `Downloaded`
   - build/query/index processes `checked`

## Field fallback values

| Field | Fallback | Notes |
|-------|----------|-------|
| venue | `arXiv YYYY` | For works not accepted by a venue but published on open platforms such as arXiv, e.g., `arXiv 2025` |
| project_link_or_github_link | `N/A` | Confirmed no open-source code or project page |
