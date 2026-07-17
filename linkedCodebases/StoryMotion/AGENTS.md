# StoryMotion Agent Contract

Read [docs/experiment-contract.md](docs/experiment-contract.md) before running,
evaluating, comparing, or documenting a StoryMotion experiment.

## Required Workflow

1. New runs use `scripts/storymotion_run_layout.py` and share one run id across
   `runs/train`, `runs/eval`, and `runs/vis`. Legacy atomic run directories are
   read-only evidence.
2. Fixed tokenizer/latent settings are code assertions in
   `storymotion/experiment_invariants.py`; do not restate them per run.
   Temporal causality is never an ablation: every Stage1/Stage2 path asserts
   `is_causal is False`, including nondefault controls.
   A standalone native MotionStreamer baseline is the only exception. Keep it
   outside StoryMotion Stage1/Stage2 runs, preserve its owning causal tokenizer
   and decoder, and never use its cache or weights in Unified-3 or a StoryMotion
   representation control.
3. Record mutable run provenance in `experiment_contract.json`. Audit it after
   cache construction and before formal evaluation.
4. Stage1 checkpoint loading additionally runs
   `scripts/storymotion_stage1_contract_harness.py`; Stage2 evaluation retains
   the existing bridge smoke and official full evaluator.
5. Do not promote metrics until their version, run, split, sample count,
   checkpoint, seed, train/eval batch sizes, cache contract, and sampler are
   attributable from the contract and evaluator artifact.
6. Run the Markdown audit before editing a canonical metric ledger. A table
   mixing versions must contain an explicit `version / run` provenance column;
   a prose-only mapping is insufficient for new or edited mixed-version rows.
7. Modify Unified-3 directly. Human/camera specialist callbacks are diagnostics
   of the same unified checkpoint and branch code, not unrelated precursor
   models. Parallel/cascade attribution uses the same unified checkpoint.
8. v8 candidates remain controls until they pass the preregistered Stage1
   root/yaw geometry gate. For human199, root-aligned MPJPE removes translation
   but retains heading error; never relabel it as local-pose quality without a
   yaw-aware attribution. Keep representation, data-curation, and Stage2
   backbone changes in separate experiment axes.
9. Data curation writes immutable raw, quarantine, and clean manifests with
   parent hashes and reason codes. A bad caption quarantines that pair, not all
   captions or the underlying motion by default.

## Current Default

The default tokenizer is the corrected v7.14 camera14 joint AE: normalized
human199 plus official camera14, non-causal, `human128 + camera64`, human-first
Stage2 cache order, and the owning local decoder. The Stage1 joint encoder saw
paired human-camera inputs; record this coupling whenever interpreting a
Stage2 branch-independence experiment.

camera9 separate VAE is a control, not the default. camera14 separate results
must never be presented as camera14 joint results.

## Change Discipline

- Preserve existing user edits and remote artifacts.
- Change only the contract, runner, evaluator, or note needed by the task.
- Fixed causal/feature/latent settings fail through code assertions. Mutable
  cache hashes, owning decoder, split, sample count, and z-norm source fail
  through the run/eval harness.
- A different train batch size and eval batch size is allowed, but both must be
  recorded. Never silently infer one from the other.
- A native MotionStreamer baseline contract must record the causal flag,
  owning tokenizer/decoder hashes, Pulp sample identities, crop/window policy,
  optimizer-step count, batch size, and total sample exposures. Its metrics are
  native-system baseline evidence, not a StoryMotion causal ablation.
