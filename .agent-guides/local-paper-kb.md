# Local Paper-KB Agent Guide

> Branch-specific instructions. This file is not part of the public `main`
> agent guidance and is read only through the conditional route in the root
> `AGENTS.md`.

## Scope and activation

BITE is a local-first workflow for turning academic PDFs into structured
evidence notes, retrieval indexes, comparisons, ideas, reviews, and exports.
PaperBite is the upstream public evidence layer; BITE manages the local paper
analysis and research-decision workflow.

Read this guide only when the user prompt explicitly contains `本地知识库`,
explicitly invokes `$research-brainstorm-from-kb`,
`$papers-query-knowledge-base`, another local-paper-KB skill, or a corresponding
`research-workflow` stage. StoryMotion experiment progress and metric routing
remain governed by the resident StoryMotion rules in the root `AGENTS.md`.

## Working surface

Paths are relative to the repository root containing the local vault:

- `obsidian-vault/paperPDFs/` stores source PDFs.
- `obsidian-vault/analysis/` stores structured local analysis notes.
- `obsidian-vault/index/` stores generated indexes and Obsidian navigation.
- `obsidian-vault/ideas/` stores local research ideas, focus notes, and reviews.
- `obsidian-vault/paper_list.csv` stores the unified paper inventory when present.
- `obsidian-vault/batches/` stores batch inputs and reports.

The index layer is optional for direct queries but is the fast filter and
navigation layer when present. Analysis notes are the primary evidence layer;
PDFs are local source material linked from those notes.

## Pipeline and state

```text
collect candidate papers / import local PDFs
  -> download when needed
  -> integrated analysis chain
     (MinerU parse/reuse -> structured analysis -> vault export)
  -> optional index refresh
  -> query / ideate / focus / review / audit / export
```

Use the owning skill for each stage. The normal paper state moves forward as
`Wait → Downloaded → analysised → checked`:

- `Downloaded` means a verified PDF exists under `paperPDFs/` or a reviewed
  local path is registered.
- `analysised` means the structured analysis note and deterministic export
  validation exist; content-quality review is still pending.
- `checked` is reserved for the later content-quality review.

Pipeline steps are idempotent; skip already-completed steps. Before a planned
analysis batch runs, declare its goal, source, selection rule, budget, and output
target. Preserve source anchors in notes, logs, and generated outputs. Reports
and profiles must be generated from available evidence rather than unsupported
claims. Analysis language defaults to `zh` unless the user requests otherwise.

## Skill routing

- `papers-collect-from-web` and `papers-collect-from-github-repo` add candidate
  rows to the unified paper inventory.
- `papers-download-from-list` downloads and repairs local PDFs.
- `papers-batch-analyze` runs the integrated paper analysis chain in declared
  batches.
- `papers-build-index` refreshes `obsidian-vault/index/` after analysis batches
  or when the user asks for an index rebuild.
- `papers-query-knowledge-base` searches and compares local analysis notes.
- `research-brainstorm-from-kb` creates structured idea notes grounded in the
  local analysis corpus.
- `papers-audit-metadata-consistency` audits paper metadata and note structure.
- `notes-export-share-version` exports notes for external sharing.
- `rf-obsidian-markdown` applies the local Obsidian Markdown conventions when a
  vault Markdown artifact is generated or edited.
- `research-workflow` is the unified entry point for these collect, download,
  analyze, build, query, ideate, audit, and export stages.

## Local analysis and index schema

Analysis notes normally live under
`obsidian-vault/analysis/<Topic>/<Venue_Year>/` or a flat venue folder. Their
frontmatter may include `title`, `venue`, `year`, `tags`, `aliases`, `pdf_ref`,
`core_operator`, `primary_logic`, and optional `claims`. Do not invent legacy
frontmatter fields such as `category`, `modalities`, or `frontier` for the
current schema.

When present, `obsidian-vault/index/index.jsonl` is the fast filter layer. The
navigation layer uses `by_topic/`, `by_method/`, `by_dataset/`, and
`by_venue_year/`; use structured `venue`, `year`, and `venue_year` fields for
venue/year filtering. Do not reference the legacy `by_venue/` or `by_year/`
navigation paths.

Use `core_operator` and `primary_logic` for method summaries, then use the
note's TL;DR summary and key-performance evidence for comparisons. Local notes
and PDFs may be linked with Obsidian wikilinks in prose or lists. External
papers and projects use standard Markdown links.

## Obsidian Markdown rules for the local KB

- Never put an aliased Obsidian wikilink such as `[[path|abbr]]` inside a
  Markdown table; the pipe is a table delimiter. Use short plain text in the
  table and put the complete wikilink in surrounding prose, a list, or
  frontmatter.
- Escape or inline-code Markdown/Obsidian reserved characters such as `*`,
  `[`, `]`, `|`, and `#` when prose needs to mention them literally.
- Keep generated indexes and exports under their owning output paths. Do not
  hand-edit generated index pages when the owning build skill can regenerate
  them.
- Generated exports, snapshots, backups, local storage, and symlinks stay out
  of Git.
