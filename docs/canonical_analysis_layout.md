# ResearchFlow Canonical Analysis Layout

## Current Version

Current derived analysis exports are intentionally empty until the full ICLR
5k+ reanalysis is regenerated from PostgreSQL. The current export entry points
remain stable for code and sync compatibility:

```text
obsidian-vault/
paperAnalysis/
paperCollection/
```

Backend paths resolve to that same vault:

```text
researchflow-backend/obsidian-vault -> ../obsidian-vault
researchflow-backend/paperAnalysis -> ../paperAnalysis
researchflow-backend/backend/config.py: obsidian_vault_dir = "../obsidian-vault"
```

`researchflow-backend/exports/obsidian-vault` is not a current vault. It may be
used as a temporary export location only when explicitly requested.

`obsidian-vault/` is the canonical human navigation/export surface. After the
5k+ run it must contain per-paper reports plus `00_Home/`, `dataset/`,
`method/`, and `domain/` indexes. `paperCollection/` is a secondary lightweight
compatibility export only; it is not the source of multi-dimensional navigation.

## Archived Versions

Past analysis exports live under:

```text
_private/archives/past_versions/
```

Current archived sets:

- `2026-05-09-current-analysis-retired-before-iclr5k-rerun/`
- `2026-05-03-remote-snapshot/`
- `2026-05-08-resmax-analysis-outputs/`
- `2026-05-09-backend-export-before-canonicalization/`
- `2026-05-09-current-vault-replaced-pages/`

These are read-only historical snapshots. Do not open them as the working
Obsidian vault and do not use them as source-of-truth writes.

## Raw Inputs

The resmax raw input layer remains in place:

```text
_private/resmax_downloads/manifest.jsonl
_private/resmax_downloads/pdfs/
_private/resmax_downloads/meta/
```

Generated resmax analysis outputs were moved to the archive registry. Raw PDFs
are large and should be synced separately from code and Markdown exports.
`paperPDFs/` remains an additional raw PDF library for non-resmax/manual
collections. Do not delete it during analysis-output cleanup.

## Sync Guidance

Routine code/Markdown sync should include:

- repository source files
- empty/current export entry points (`obsidian-vault/`, `paperAnalysis/`,
  `paperCollection/`)
- `_private/resmax_downloads/manifest.jsonl`

Routine sync should exclude:

- `_private/archives/past_versions/`
- `_private/resmax_downloads/pdfs/`
- `_private/resmax_downloads/meta/`
- `paperPDFs/` unless doing a raw-artifact sync
- `researchflow-backend/storage`
- `researchflow-backend/exports/`

Use a separate large-artifact sync job for raw PDFs, local object storage, and
archived snapshots.
