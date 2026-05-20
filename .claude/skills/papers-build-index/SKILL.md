---
name: papers-build-index
follows: rf-obsidian-markdown
status: export-only
description: Builds/refreshes `obsidian-vault/index/index.jsonl` and Obsidian navigation pages from `obsidian-vault/paper_list.csv` when present, enriched by `obsidian-vault/analysis/` frontmatter when available. Use after completed analysis batches or when users ask to rebuild the local paper index.
---

# Build Index

## What this skill does

Regenerates the local paper index under `obsidian-vault/index/`.

Inputs:

1. `obsidian-vault/paper_list.csv` when present. This is the paper inventory.
2. `obsidian-vault/analysis/**/*.md` frontmatter when present. This is evidence and enrichment, not a required database.

Outputs:

- `obsidian-vault/index/index.jsonl`
- `obsidian-vault/index/_AllPapers.md`
- aggregate pages under:
  - `by_dataset/`
  - `by_method/`
  - `by_topic/`
  - `by_venue/`
  - `by_year/`

The builder does not require the platform database.

## When to run

Batch analysis calls this automatically after completed batches so the local
index reflects newly analyzed papers. Users can also run it manually after
editing `paper_list.csv` or analysis note frontmatter.

```bash
python3 .claude/skills/papers-build-index/scripts/build_paper_index.py
```

Expected output:

```text
[OK] papers: ...
[OK] output: .../obsidian-vault/index
```

## Index contract

Each `index.jsonl` line is one paper record with stable, retrieval-oriented
fields:

```json
{"title":"...","analysis_path":"obsidian-vault/analysis/...md","pdf_ref":"obsidian-vault/paperPDFs/...pdf","venue":"ICLR","year":2026,"topics":["..."],"methods":["..."],"datasets":["..."]}
```

The exact set of optional fields may grow, but the builder must keep records
usable when only `paper_list.csv` exists or only analysis notes exist.

## Obsidian Markdown rule

Do not put aliased wikilinks such as `[[path|abbr]]` in Markdown tables. The
generated pages avoid tables and use lists with normal wikilinks instead.
