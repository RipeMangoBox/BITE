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
- `obsidian-vault/index/paper_index.md`
- `obsidian-vault/index/_AllPapers.md`
- aggregate pages under:
  - `by_dataset/`
  - `by_method/`
  - `by_topic/`
  - `by_venue_year/`

The builder does not require the platform database.
`obsidian-vault/index/README.md` is a public placeholder for the generated
directory and should not be overwritten with local/private index contents.
Aggregate navigation entry files use explicit dimension names:
`by_topic/topic_index.md`, `by_method/method_index.md`,
`by_dataset/dataset_index.md`, and
`by_venue_year/venue_year_index.md`.
Venue and year navigation is merged into `venue_year` labels such as
`ICLR_2026`; the builder does not generate separate `by_venue/` or `by_year/`
indexes.
`by_topic/` uses coarse top-level research areas derived from `category`,
`topics`, `topic/...` tags, or path hints. Nested topic tags are intentionally
folded into their first segment so the navigation does not fragment.
`topic/<venue_year>` tags in analysis frontmatter are treated as venue/year
metadata, not research-topic taxonomy.
`by_method/` uses normalized method-family labels derived from method names,
tags, title, `core_operator`, and `primary_logic`. Exact per-paper method names
remain in `index.jsonl` under `methods` for precise search and comparison.
`by_dataset/` lists only dataset values that appear in at least two papers so
single-paper experiment slices do not dominate Obsidian navigation. The full
per-paper dataset field remains in `index.jsonl`. Dataset display values are
normalized to dataset names; parenthesized model, split, seed, resolution, and
other experiment-setting details are stripped.
Generated paper entries are nested Obsidian list items, not one-line entries
joined with punctuation separators. Each entry places the analysis note link on
the parent bullet and PDF/topics/method groups/methods/datasets on child
bullets.

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
{"title":"...","analysis_path":"obsidian-vault/analysis/...md","pdf_ref":"obsidian-vault/paperPDFs/...pdf","venue":"ICLR","year":2026,"venue_year":"ICLR_2026","topics":["..."],"methods":["..."],"method_groups":["..."],"datasets":["..."],"tags":["..."],"core_operator":"...","primary_logic":"...","paper_link":"...","project_link":"...","source":"analysis"}
```

The exact set of optional fields may grow, but the builder must keep records
usable when only `paper_list.csv` exists or only analysis notes exist.

When frontmatter is incomplete or inconsistent, the builder should fall back to
safe evidence in this order: explicit frontmatter, `paper_list.csv`, body
metadata tables / links, then path-derived venue/year/topic hints. It should
not require a valid `pdf_ref` when an analysis note otherwise has clear paper
evidence.
Notes under `obsidian-vault/analysis/test/` or similarly named test folders are
treated as local evaluation artifacts and excluded from the default paper index.

## Obsidian Markdown rule

Do not put aliased wikilinks such as `[[path|abbr]]` in Markdown tables. The
generated pages avoid tables and use lists with normal wikilinks instead.
