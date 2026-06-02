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

## Branch Sync Policy

This branch is the canonical place for changes that should later appear in the
public `main` worktree. Make shared README, public docs, public assets, and
public workflow updates here first, then sync them to `main` after review.

Keep branch-specific and local-development material out of `main`:

- `_private/` local notes, archives, deployment notes, and operation history
- Obsidian workspace/runtime state
- provider-specific defaults or private model choices
- internal branch/worktree coordination notes

`AGENTS.md` itself is branch-specific. Do not blindly sync this file to
`main`; the public `main` copy should contain only project background and
public agent-facing guidance.

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
8. When prose needs to mention Markdown or Obsidian reserved characters such as
   `*`, `[`, `]`, `|`, or `#`, escape them with backslashes or wrap them in
   inline code so reading view does not reinterpret the text.
9. In Markdown tables, aliased Obsidian wikilinks are allowed only when the
   alias separator is escaped as `[[full/path\|abbr]]`; an unescaped `|`
   splits table columns. Outside tables, normal `[[full/path|abbr]]` links are
   fine.
10. Generated exports, snapshots, backups, local storage, and symlinks stay out
   of Git.
