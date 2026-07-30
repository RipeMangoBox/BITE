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

1. The StoryMotion system mainline is the co-equal v11 C0-LAT and C0-GEO
   `105K` endpoints. They share the exact v9 Pulp-only non-causal Stage1 owner
   (`human128 + interaction16 + camera48`), its owning decoder/cache/stats, and
   the frozen v9 Human `105K` teacher; only the Camera objective differs.
   v8.1C C3-25 is the former-mainline system baseline and v7.14 is the older
   representation comparator. camera9 separate is a control only; never merge
   camera14 separate and camera14 joint evidence.
   Temporal causal tokenizers are forbidden in every Stage1/Stage2 setting;
   constructors, checkpoint/cache loading, training, and evaluation must assert
   `is_causal is False`. Controls may change representation, not causality.
   The sole exception is a standalone native MotionStreamer baseline kept
   outside StoryMotion Stage1/Stage2 runs. It may retain MotionStreamer's
   causal tokenizer only when its contract names MotionStreamer as the owning
   system and decoder; it must not build, consume, or gate a StoryMotion cache,
   Unified checkpoint, or representation control.
2. Fixed legacy representation settings live in
   `storymotion/experiment_invariants.py`; v11 fixed boundaries additionally
   fail closed in its configuration validator and contract preflight. Do not
   replace either with manually typed per-run settings.
3. The run contract audits mutable boundaries: exact Stage1 checkpoint and
   owning-decoder hashes, train/eval cache hashes and sample identities,
   train-only z-normalization source, seed, train/eval batch sizes, split,
   sample count, and sampler.
4. A metric table mixing versions must include an explicit `version / run`
   column with a non-empty value in every row. If a matched comparison is not
   available, state the differing fields and restrict the conclusion.
5. Human completion in the asymmetric model is human-text-only. Camera
   completion consumes human latent plus camera text. The v11 mainline reports
   Direct-H, Direct-C, and sequential Human-then-Camera; evolving-H parallel
   denoising is the removed failure axis. v11 must not train, evaluate, or gate
   on joint parallel unless the user separately authorizes reopening that
   solver axis. Historical C3 reports joint parallel; cascade is optional
   historical/root-cause attribution only.
6. A specialist result is valid only as a task-sliced diagnostic of the same
   branch implementation used by Unified-3, or when its weights are explicitly
   transferred and verified. Do not train unrelated specialists as a gate for
   a different three-mode model.
7. StoryMotion v11 C0-LAT and C0-GEO seed17 are co-mainline Stage2 systems at
   Camera optimizer `105K`. Their selection is supported by audited pure4,053
   Direct-H, Direct-C, formal sequential, decoded geometry, physical
   diagnostics, and matched bootstrap evidence. LAT and GEO remain co-equal
   because their six Camera geometry confidence intervals cross zero and their
   semantic/framing fields form a mixed Pareto. Historical run contracts and
   IDs retain their original diagnostic fields for provenance; promotion does
   not rewrite immutable artifacts. C3-25 retains its raw diagnostic ledger
   values as the former-mainline baseline. On human199, root-aligned MPJPE
   removes root translation but not heading; do not call it local-pose error
   without a yaw-aware attribution.
8. Data cleaning is versioned and reversible. Quarantine caption-motion pairs
   rather than deleting a whole motion when only one caption is wrong, retain
   immutable parent manifests and reason codes, and test cleaning separately
   from representation and generator changes.

## StoryMotion Documentation Routing

One claim, metric, run state, or execution event has one canonical Markdown
owner. Links may summarize an owner, but may not reproduce a second table,
running log, or competing conclusion. Check the owner before creating a new
StoryMotion note.

| Canonical target | Sole responsibility | Do not put here |
| --- | --- | --- |
| `obsidian-vault/ideas/StoryMotion/current.md` | Current mainline, active decision, v8 hypothesis/gates, blockers, and links to the evidence owner | Per-step progress, stale ETA, full metric tables, historical narrative |
| `obsidian-vault/ideas/StoryMotion/StoryMotion-valid-metric-ledger.md` | Audited numeric results, mixed-version comparison tables, artifact/checkpoint/record hashes, and uncertainty | Unaudited runner messages, speculative root causes, deployment diary |
| `obsidian-vault/ideas/StoryMotion/version_family.md` | Version-family names, causal questions, unique interventions, completed Stage/steps, finalized milestones, invalidations, and bug provenance | Live priority, queue state, or a duplicate current-version matrix |
| `obsidian-vault/ideas/StoryMotion/StoryMotion-metric-computation-io.md` | Metric definitions, evaluator/decoder semantics, and I/O contracts | Run-specific outcome tables or policy decisions |
| `obsidian-vault/ideas/StoryMotion/2026-07-17_storymotion-v8-2333-data-curation-plan.md` | The complete v8.2333 curation contract, gate state, zero/nonzero counters, manifest lineage, and curation-only decisions | A separate progress page or representation/backbone conclusions |
| `obsidian-vault/ideas/StoryMotion/2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder.md` | Representation-generatability diagnostics, Stage2 screen/continue/stop gates, and the closed C3-25 mainline-selection provenance | Formal result tables after an eval closes |

Route incremental information in this order:

1. Before a run, write mutable provenance only in its
   `experiment_contract.json`; put the causal question and predeclared gate in
   the owning plan page.
2. During a run, write progress, ETA, worker output, and checkpoints only to
   the run manifest/logs under `runs/`. Do not make date-stamped vault progress
   notes or update `current.md` for a finite loss/step count.
3. At a screen, retain the auditable raw artifact in `runs/`, update just the
   owning plan's decision row, and label the result `screen` rather than formal
   evidence.
4. After a formal audit, add the exact result once to the metric ledger, then
   update `current.md` with a short current decision and `version_family.md` with a
   finalized event. Mixed-version tables must have a non-empty `version / run`
   value on every row.
5. When a plan is superseded or a deployment snapshot closes, move it (do not
   copy it) to `obsidian-vault/ideas/StoryMotion/archived/<axis>/`, update
   inbound links, and record the archive decision in `version_family.md`. Preserve
   evidence and hashes; never replace a retired page with a second live
   narrative or delete artifacts merely to simplify the vault.

New StoryMotion Markdown is justified only for a distinct causal axis or a
durable contract not owned by a page above. A daily status, a second progress
page, or a duplicate metric summary is not a distinct axis.

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
