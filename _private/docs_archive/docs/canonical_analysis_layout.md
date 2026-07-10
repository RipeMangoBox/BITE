# ResearchFlow Canonical Analysis Layout

## Current Version

Current derived analysis exports are generated from PostgreSQL. The current
export entry points remain stable for code and sync compatibility:

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

`obsidian-vault/` is the canonical human navigation/export surface. It should
contain per-paper reports plus `00_Home/`, `dataset/`, `method/`, and `domain/`
indexes when exports are present. `paperCollection/` is a secondary lightweight
compatibility export only; it is not the source of multi-dimensional navigation.

## Archived Versions

Past analysis exports live under:

```text
_private/archives/past_versions/
```

These are read-only historical snapshots. Do not open them as the working
Obsidian vault and do not use them as source-of-truth writes.

## Raw Inputs

Raw input layers live outside the public repository, typically under
`_private/`, object storage, or `paperPDFs/`. Raw PDFs and parser artifacts are
large and should be synced separately from code and Markdown exports.

## Sync Guidance

Routine code/Markdown sync should include:

- repository source files
- empty/current export entry points (`obsidian-vault/`, `paperAnalysis/`,
  `paperCollection/`)

Routine sync should exclude:

- `_private/archives/past_versions/`
- `_private/` raw parser/download artifacts
- `paperPDFs/` unless doing a raw-artifact sync
- `researchflow-backend/storage`
- `researchflow-backend/exports/`

Use a separate large-artifact sync job for raw PDFs, local object storage, and
archived snapshots.
