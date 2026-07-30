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
7. Human/camera specialist callbacks are diagnostics of the same branch
   implementation, not unrelated precursor models. The v11 mainline reports
   Direct-H, Direct-C, and sequential Human-then-Camera, and keeps joint
   parallel disabled because evolving-H denoising is the removed failure axis.
   Do not train, evaluate, or gate v11 on joint parallel without separate user
   authorization. Historical C3 reports joint parallel; outside v11, cascade
   remains optional historical/root-cause attribution and uses the same
   checkpoint as parallel when invoked.
8. v8 candidates remain controls until they pass the preregistered Stage1
   root/yaw geometry gate. For human199, root-aligned MPJPE removes translation
   but retains heading error; never relabel it as local-pose quality without a
   yaw-aware attribution. Keep representation, data-curation, and Stage2
   backbone changes in separate experiment axes.
9. Data curation writes immutable raw, quarantine, and clean manifests with
   parent hashes and reason codes. A bad caption quarantines that pair, not all
   captions or the underlying motion by default.

## Current Default

The system default is the co-equal v11 C0-LAT and C0-GEO seed17 pair at Camera
optimizer `105K`. Both use the exact v9 Pulp-only non-causal Stage1 owner
`stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726`, with
`human128 + interaction16 + camera48`, its owning decoder/cache/train-only
statistics, and the frozen v9 Human `105K` teacher. C0-LAT uses latent flow;
C0-GEO keeps that flow objective and adds the calibrated Stage1-style decoded
Camera auxiliary. Neither is subordinate to the other.

The former mainline v8.1C C3-25 remains the primary system baseline; v7.14 is
the older representation comparator. Historical contracts retain their
original diagnostic eligibility fields. Promotion is a decision-layer event
and does not rewrite those immutable artifacts.

camera9 separate VAE is a control, not the default. camera14 separate results
must never be presented as camera14 joint results.

## Per-Host Stage1 Data Read Policy

On hosts `4090` and `5090`, the immutable Pulp source is
`/data/public/ripemangobox/Motion/datasets/pulpmotion-data` on that host's
`/data` HDD. On host `3090`, the local immutable copy is provisioned at
`/home/ripemangobox/Coding/Github/Motion/.storymotion-data/pulpmotion-data` and
is exposed after verification as
`/home/ripemangobox/Coding/Github/Motion/datasets/pulpmotion-data`.
`linked/pulpmotion-data` is only a workspace symlink. The presence of a partial
rsync tree is not a completion marker: host `3090` must not train or evaluate
from it until the full copy, ordered identities, file counts, and hashes have
been verified and the logical path has been atomically cut over.

Random-small-file Stage1 training must not read `smpl_rifke`, `traj`, or
`intrinsics` from a rotational disk. Use the same-host fast paths below:

- host `4090`: `/home/ripemangobox/storymotion_data_cache/pulpmotion_stage1_io_20260718`
  on the system NVMe;
- host `5090`: `/home/ripemangobox/storymotion_data_cache/pulpmotion_stage1_io_20260719`
  on the system SATA SSD. Despite legacy `nvme` text in some run or manifest
  names, this host is not NVMe-backed.
- host `3090`: the verified full local dataset at
  `/home/ripemangobox/Coding/Github/Motion/.storymotion-data/pulpmotion-data`
  on the system NVMe; no second Stage1 replica is required.

All three path families in one Stage1 manifest must resolve to the same fast
tier. A hybrid manifest or silent HDD fallback is forbidden. Before launch,
verify the target filesystem with `findmnt -T`, verify `180527` files in each
of `smpl_rifke`, `traj`, and `intrinsics`, preserve ordered sample IDs and
manifest hashes, and run a finite loader-throughput preflight. Rebuild a
missing replica only from that host's own immutable Pulp source; never edit the
source and never make one server depend on a cross-server copy.

This rule is specific to Stage1 random-small-file reads. Do not blindly move
Stage2 contiguous `.pt` caches or other sequential artifacts to `/home`;
select their storage tier from measured access behavior and record the exact
cache hashes in the run contract.

The `3090` workspace is
`/home/ripemangobox/Coding/Github/Motion/StoryMotion`. Replicate only the exact
checkpoint, owning decoder, cache, and normalization stats required by an
authorized local train/eval contract, using resumable rsync followed by hash
verification. Do not bulk-copy historical `runs/`, render outputs, or rendering
adaptation assets; add them later only for a concrete need. Once provisioned,
local execution must not depend on a live `4090` or `5090` mount or network
read.

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
