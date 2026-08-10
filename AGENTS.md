# Agent Guide

Public agent-facing usage starts from [README.md](README.md) and
[.claude/skills/README.md](.claude/skills/README.md). Internal deployment notes
stay under `_private/`.

## Conditional Local Paper-KB Instructions

Read `.agent-guides/local-paper-kb.md` only when the user prompt explicitly
contains `本地知识库`, explicitly invokes `$research-brainstorm-from-kb`,
`$papers-query-knowledge-base`, another local-paper-KB skill, or a corresponding
`research-workflow` stage. Otherwise do not read that file.

## Conditional Agent Delegation

The following is a conditional rule and does not change behavior for other
model or reasoning configurations. Only when the current agent is
`gpt-5.6-sol` with `reasoning_effort` set to `xhigh` or `max`, it owns
high-level work such as decisions, supervision, and review. Delegate concrete
work, including code writing and execution, to `gpt-5.6-luna` with
`reasoning_effort=max`, and inspect each delegated result. If obvious errors or
major direction problems remain after two inspection rounds and requested
corrections, the `gpt-5.6-sol` agent must handle the work itself.

## StoryMotion Tasks

These rules apply directly to any task involving StoryMotion code, experiments,
metrics, runs, or research notes, even when the task starts outside the linked
codebase:

The project uses one code repository, `linkedCodebases/StoryMotion/`, for two
claim-isolated paper tracks. Do not create a separate DIRECT repository:

- StoryMotion is **StoryMotion: Preserving Human Motion Priors in Asymmetric
  Human–Camera Generation**.
- DIRECT is **DIRECT: Dual-Frame Cinematographic Intent Transfer across
  Articulated Human Motions**.
- Shared Stage1, decoders, evaluators, run harnesses, and metric infrastructure
  remain in StoryMotion. Paper questions, positive definitions, training
  authorization, artifact interpretation, tables, and claims remain separate.
- New StoryMotion and DIRECT run IDs use `sm_` and `direct_` prefixes,
  respectively. The one-time legacy namespace migration is owned by
  `obsidian-vault/ideas/StoryMotion/StoryMotion-folder-rename-map.md`: regular
  Markdown uses the mapped `sm_` identity, while that mapping retains old IDs,
  paths, hashes, and host migration state. Existing run IDs, checkpoints,
  artifact paths, historical artifact contents, and Actor–Director diagnostic
  semantics remain immutable and are not physically renamed.

1. The StoryMotion operational mainline is v11 C0-LAT at Camera optimizer
   `105K`; C0-GEO remains an audited objective alternate/control. They share
   the exact v9 Pulp-only non-causal Stage1 owner
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
   a different three-mode model. For the StoryMotion matched cascade, specialist
   independence means separate Stage2 weights, optimizers, and checkpoints; it
   does not authorize retraining Human/Camera-separate Stage1. The matched arm
   freezes the exact v9 Stage1 owner and first tests the H199 decode/re-encode
   interface without optimizer steps. A Camera-owned retrained Stage1 is an
   optional native-system comparison and requires separate authorization.
7. StoryMotion v11 C0-LAT seed17 is the default Stage2 system and parent for
   future ablations at Camera optimizer `105K`; C0-GEO seed17 remains fully
   audited but is not duplicated into future matrices by default. The author-side
   operational choice uses the prioritized main-table evidence and LAT's simpler
   objective/training contract. It does not imply statistically robust objective
   superiority: all six Camera geometry confidence intervals cross zero and the
   semantic/framing fields form a mixed Pareto. Historical run contracts and IDs
   retain their original diagnostic fields for provenance; promotion does not
   rewrite immutable artifacts. C3-25 retains its raw diagnostic ledger
   values as the former-mainline baseline. On human199, root-aligned MPJPE
   removes root translation but not heading; do not call it local-pose error
   without a yaw-aware attribution.
8. Data cleaning is versioned and reversible. Quarantine caption-motion pairs
   rather than deleting a whole motion when only one caption is wrong, retain
   immutable parent manifests and reason codes, and test cleaning separately
   from representation and generator changes.
9. The current matched available-data cohort Pulp Stage2 baseline uses the same
   complete materializable train/eval ID sets as StoryMotion Stage2
   (`162760/4053`); it is not a smaller experimental subset. It must declare
   `total_optimizer_steps=210000`, `halfway_checkpoint_step=105000`, and a
   concrete total exposure budget equal to optimizer steps times effective batch
   size. Progress heartbeats must record global step, epoch, exposures,
   throughput, ETA, data-wait/H2D/compute/checkpoint timing, GPU utilization,
   and memory so an I/O bottleneck is claimed only when measured data wait
   dominates while the GPU is idle. At the exact optimizer boundary 105000,
   atomically save an immutable checkpoint and reload-verify it. It must contain
   model and optimizer state, plus scheduler, scaler, or EMA state when used,
   RNG and sampler state, and contract/config/data/cache/code/host/device
   provenance. If configuration is wrong, progress is stalled, or the required
   halfway checkpoint is absent, preserve the old run as invalid provenance;
   create a new run ID and retrain from step zero. Do not patch or resume that
   run.

## StoryMotion / DIRECT Documentation Routing

One claim, metric, run state, or execution event has one canonical Markdown
owner. Links may summarize an owner, but may not reproduce a second table,
running log, or competing conclusion. StoryMotion notes live under
`obsidian-vault/ideas/StoryMotion/`; Paper B notes live under
`obsidian-vault/ideas/DIRECT/`. Check the owner before creating a new note.

| Canonical target | Sole responsibility | Do not put here |
| --- | --- | --- |
| `obsidian-vault/ideas/StoryMotion/current.md` | StoryMotion current mainline, active decisions, blockers, and links to each evidence owner | DIRECT queue, per-step progress, stale ETA, full metric tables, historical narrative |
| `obsidian-vault/ideas/DIRECT/current.md` | Paper B DIRECT current state, blockers, and links to its evidence owners | StoryMotion mainline selection, duplicate shared metrics, or StoryMotion code ownership |
| `obsidian-vault/ideas/StoryMotion/StoryMotion-valid-metric-ledger.md` | The single repository-level owner for audited numeric results, with explicit StoryMotion, DIRECT, or shared-baseline identity, plus artifact/checkpoint/record hashes and uncertainty | A second DIRECT ledger, unaudited runner messages, speculative root causes, deployment diary |
| `obsidian-vault/ideas/StoryMotion/version_family.md` | Version-family names, causal questions, unique interventions, completed Stage/steps, finalized milestones, invalidations, and bug provenance | Live priority, queue state, or a duplicate current-version matrix |
| `obsidian-vault/ideas/StoryMotion/paper-boundary.md` | Formal paper titles, single-repository policy, contribution boundary, cross-paper reuse, and anti-crosswire rules | Run progress, metric tables, or paper-specific experiment queues |
| `obsidian-vault/ideas/StoryMotion/StoryMotion-iclr-reliability.md` | StoryMotion claim-evidence gaps, matched specialist contract, reliability priorities, and stop/degrade conditions | DIRECT program transfer, Rect/HumanML3D queues, or DIRECT training authorization |
| `obsidian-vault/ideas/DIRECT/2026-08-01_storymotion-multipair-data-training-plan.md` | Paper B DIRECT program recovery, multi-pair construction, training order, gates, and degrade conditions | StoryMotion mainline selection or capability-preserving framework claims |
| `obsidian-vault/ideas/StoryMotion/StoryMotion-metric-computation-io.md` | Metric definitions, evaluator/decoder semantics, and I/O contracts | Run-specific outcome tables or policy decisions |
| `obsidian-vault/ideas/StoryMotion/archived/data/2026-07-17_storymotion-v8-2333-data-curation-plan.md` | Read-only v8.2333 curation contract, gate state, counters, manifest lineage, and curation provenance | New training authorization, live progress, or representation conclusions |
| `obsidian-vault/ideas/StoryMotion/archived/diagnostics/2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder.md` | Read-only representation-generatability diagnostics and closed C3-25 selection provenance | Current StoryMotion queue or formal result tables |

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
4. After a formal audit, add the exact result once to the shared metric ledger,
   then update the owning paper's `current.md` with a short decision and
   `version_family.md` with a finalized event. Mixed-version tables must have a
   non-empty `version / run` value on every row.
5. When a plan is superseded or a deployment snapshot closes, move it (do not
   copy it) to the owning paper folder's `archived/<axis>/`, update
   inbound links, and record the archive decision in `version_family.md`. Preserve
   evidence and hashes; never replace a retired page with a second live
   narrative or delete artifacts merely to simplify the vault.

New StoryMotion or DIRECT Markdown is justified only for a distinct causal axis
or a durable contract not owned by a page above. A daily status, a second
progress page, or a duplicate metric summary is not a distinct axis.

Detailed commands and schemas are in:

- `linkedCodebases/StoryMotion/AGENTS.md`
- `linkedCodebases/StoryMotion/docs/experiment-contract.md`

The scope includes `obsidian-vault/ideas/StoryMotion/`,
`obsidian-vault/ideas/DIRECT/`,
`_private/*storymotion*`, and StoryMotion run directories on remote machines.

## Branch Sync Policy

This branch is the canonical place for changes that should later appear in the
public `main` worktree. Make shared README, public docs, public assets, and
public workflow updates here first, then sync them to `main` after review.

Keep branch-specific and local-development material out of `main`:

- `_private/` local notes, archives, deployment notes, and operation history
- `.agent-guides/local-paper-kb.md` branch-specific local paper-KB instructions
- Obsidian workspace/runtime state
- provider-specific defaults or private model choices
- internal branch/worktree coordination notes

`AGENTS.md` itself is branch-specific. Do not blindly sync this file to
`main`; the public `main` copy should contain only project background and
public agent-facing guidance.

## General Artifact Hygiene

Generated exports, snapshots, backups, local storage, and symlinks stay out of
Git.
