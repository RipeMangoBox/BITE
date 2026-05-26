# Agent Guide

Public agent-facing usage starts from [README.md](README.md) and
[.claude/skills/README.md](.claude/skills/README.md). Internal deployment notes
stay under `_private/`.

ResearchFlow is a local-first research workflow for structured paper analysis.
Its goal is to turn academic PDFs into machine-actionable evidence notes,
retrieval indexes, and downstream idea or review artifacts. PaperBite acts as
the upstream public evidence layer: it helps batch-prepare parsed paper assets,
while ResearchFlow focuses on structured analysis, retrieval, comparison, and
research decision support.

## Working Surface

- `obsidian-vault/paperPDFs/` stores source PDFs.
- `obsidian-vault/analysis/` stores structured local analysis notes.
- `obsidian-vault/index/` stores generated indexes and Obsidian navigation.
- `obsidian-vault/ideas/` stores local idea, focus, and review notes.

## Local Pipeline

```text
collect candidate papers / import local PDFs
  -> batch MinerU PDF parse
  -> structured paper analysis
  -> index
  -> query / ideate / focus / review / export
```

## Rules

1. Treat the local vault paths above as the current working surface.
2. Write only through the skill that owns the target output path.
3. Analysis language defaults to `zh` unless the request overrides it.
4. Pipeline steps are idempotent; already-completed steps should be skipped.
5. Planned analysis batches must declare goal, source, selection rule, budget,
   and output target before agents run.
6. Agents must preserve source anchors in notes, logs, and generated outputs.
7. Reports and profiles must be generated from available evidence, not new
   unsupported claims.
8. In Markdown tables, do not use aliased Obsidian wikilinks such as
   `[[full/path|abbr]]`; use plain text inside table cells and place full
   wikilinks in surrounding prose or frontmatter.
9. Generated exports, snapshots, backups, local storage, and symlinks stay out
   of Git.
