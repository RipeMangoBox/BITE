# Agent Guide

Public agent-facing usage starts from [README.md](README.md) and
[.claude/skills/README.md](.claude/skills/README.md). Internal deployment notes
stay under `_private/`.

BITE is a local-first research workflow for structured paper analysis.
Its goal is to turn academic PDFs into machine-actionable evidence notes,
retrieval indexes, and downstream idea or review artifacts. PaperBite acts as
the upstream public evidence layer: it provides reusable structured paper
assets, while BITE focuses on local analysis, retrieval, comparison, idea
generation, and research decision support.

## Working Surface

- `obsidian-vault/paperPDFs/` stores source PDFs.
- `obsidian-vault/analysis/` stores structured local analysis notes.
- `obsidian-vault/index/` stores generated indexes and Obsidian navigation.
- `obsidian-vault/ideas/` stores local idea, focus, and review notes.

## StoryMotion Tasks

These rules apply directly to any task involving StoryMotion code, experiments,
metrics, runs, or research notes, even when the task starts outside the linked
codebase:

1. The mainline tokenizer is corrected v7.14 camera14 joint AE: normalized
   human199 plus official camera14, non-causal, human128 plus camera64, and the
   owning local decoder. camera9 separate is a control only; never merge
   camera14 separate and camera14 joint evidence.
   Temporal causal tokenizers are forbidden in every Stage1/Stage2 setting;
   constructors, checkpoint/cache loading, training, and evaluation must assert
   `is_causal is False`. Controls may change representation, not causality.
2. Fixed representation settings live as code assertions in
   `storymotion/experiment_invariants.py`. Do not repeat them as manually typed
   per-run configuration.
3. The run contract audits mutable boundaries: exact Stage1 checkpoint and
   owning-decoder hashes, train/eval cache hashes and sample identities,
   train-only z-normalization source, seed, train/eval batch sizes, split,
   sample count, and sampler.
4. A metric table mixing versions must include an explicit `version / run`
   column with a non-empty value in every row. If a matched comparison is not
   available, state the differing fields and restrict the conclusion.
5. Human completion in the asymmetric Unified-3 model is human-text-only.
   Camera completion consumes human latent plus camera text. Joint generation
   must compare parallel and human-first cascade schedules from the same
   unified implementation/checkpoint whenever attribution requires it.
6. A specialist result is valid only as a task-sliced diagnostic of the same
   branch implementation used by Unified-3, or when its weights are explicitly
   transferred and verified. Do not train unrelated specialists as a gate for
   a different three-mode model.

Detailed commands and schemas are in:

- `linkedCodebases/StoryMotion/AGENTS.md`
- `linkedCodebases/StoryMotion/docs/experiment-contract.md`

The scope includes `obsidian-vault/ideas/StoryMotion/`,
`_private/*storymotion*`, and StoryMotion run directories on remote machines.

## Local Pipeline

```text
collect candidate papers / import local PDFs
  -> download when needed
  -> integrated analysis chain
     (MinerU parse/reuse -> structured analysis -> vault export)
  -> optional index refresh
  -> query / ideate / focus / review / export
```

Paper state advances as `Wait → Downloaded → analysised → checked`:
`analysised` means that the structured note and deterministic export validation
exist, while `checked` is reserved for a later content-quality review.

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
