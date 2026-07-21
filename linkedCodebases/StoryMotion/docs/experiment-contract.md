# StoryMotion Experiment Contract

This is the single operational boundary for Stage1, Stage2, evaluation, and
metric documentation. It consolidates the historical run-layout, Stage1
checkpoint preflight, cache metadata checks, bridge smoke, and official full
evaluation instead of replacing those tools.

## Where It Lives

Keep this contract in the StoryMotion source tree mirrored on the GPU hosts
because it governs StoryMotion code and runs. The BITE root `AGENTS.md` embeds
the mandatory core rules and points here for the detailed schema, so nested
AGENTS discovery is not required.

Each new run shares one `run_id` across the functional roots:

```text
runs/train/<stage>/<run_id>  # contract, checkpoint, cache, events, driver state
runs/eval/<stage>/<run_id>   # metrics and decoded numerical records
runs/vis/<stage>/<run_id>    # rendered media and render manifests
```

The `experiment_contract.json` and `manifest.json` live under the train root
and record all paths relative to the common `runs` root. Generated checkpoints,
caches, metrics, renders, and remote snapshots remain outside Git. Legacy
atomic `runs/stage1/<run_id>` and `runs/stage2/<run_id>` paths are read-only
compatibility inputs during migration; new runs must not create them.

## Stage Boundary

Stage1 owns the feature representation, encoder/decoder topology, causal flag,
latent dimensions/order, reconstruction checkpoint, and owning decoder. Stable
mainline representation values are asserted by
`storymotion/experiment_invariants.py`; they are not copied into every Stage2
run contract.

As of 2026-07-21, the selected decision mainline is v8.1C C3-25 seed17 and its
audited Unified-3 `105K` endpoint. The former Human global-slope threshold is
a non-blocking diagnostic; C3-25 records that diagnostic as passed while
retaining the raw `26.302 mm/100f` value. v7.14 and v7.38 remain reproducible
former-mainline comparators.

The main experimental unit is one Unified-3 checkpoint containing human,
camera, and joint tasks. Human-only and camera-only numbers are task-sliced
diagnostics of that checkpoint and its shared branch implementation. A
separately trained specialist cannot gate Unified-3 unless its implementation
or weights are actually shared and that linkage is recorded.

Stage2 owns a frozen Stage1 checkpoint, caches derived from that checkpoint,
train-only latent normalization, denoiser training, and sampling. Before use,
the following equalities must hold:

```text
parent Stage1 checkpoint SHA == cache tokenizer checkpoint SHA
z-norm source SHA            == Stage2 train-cache SHA
formal eval decoder          == parent owning decoder
```

The fixed feature contract, non-causal flag, dimensions, and latent order are
asserted when the tokenizer checkpoint is loaded, when the cache is built, and
when a mainline Stage2 cache is opened. Legacy or camera9 controls require the
explicit `--allow-nondefault-tokenizer-contract` opt-out and must be labeled as
controls in their metric rows. That opt-out only relaxes representation
identity; temporal causal tokenizers remain forbidden for every control,
training run, cache, and evaluation.

The only causal exception is an external, standalone native MotionStreamer
baseline. It lives outside `runs/stage1` and `runs/stage2`, names
`MotionStreamer` as `baseline_system`, and retains the owning causal tokenizer
and decoder. Its cache, checkpoint, and metrics cannot be consumed by, used to
gate, or be presented as an ablation of StoryMotion Unified-3. Its independent
contract records tokenizer and decoder hashes, `is_causal: true`, Pulp train
sample IDs, the 64-frame crop/window policy, optimizer steps, train batch size,
total sample exposures, and native evaluation protocol.

Train batch size and evaluation batch size are independent recorded fields.
Evaluation must also record its own seed, split, sample count, decode batch
size, sampler steps, eta, and CFG. `non-causal` means `is_causal: false` in
the checkpoint contract and cache metadata; a command-line label is not proof.

Cache train/validation files must be built from their declared manifests and
must not be reused after changing tokenizer checkpoint, feature contract,
causal flag, latent order, or sample IDs. The contract stores the cache hashes;
the evaluator artifact stores or references the same metadata. The audit also
compares the cache metadata's tokenizer checkpoint path with the declared
parent Stage1 checkpoint; matching dimensions or a default preset alone are
not sufficient cache provenance.

A same-shape candidate tokenizer that is used only for a Stage2 diagnostic
must add a `representation` object with `diagnostic_only: true`,
`promotion_eligible: false`, and a non-empty `purpose`. It remains a control
until an explicit audited selection decision is recorded; structural cache
checks alone never promote it. Its diagnostic cache must repeat
`diagnostic_only: true`, `promotion_eligible: false`, and the same non-empty
purpose.

Promotion is a decision-layer event, not a reason to rewrite immutable
artifacts. C3-25's historical run ID and contracts retain their original
`diag`, `diagnostic_only: true`, and `promotion_eligible: false` fields as
execution provenance. New caches and runs created after the C3-25 mainline
decision must use the selected mainline representation contract and must not
inherit those historical eligibility fields.

For a curated-data control, the manifest is immutable and additionally records
its parent-manifest SHA, caption/pair identity, quarantine reason, scorer and
checkpoint hashes, threshold version, and whether the action affects one
caption-motion pair or the underlying motion. Representation, curation, and
Stage2-backbone changes require separate run IDs.

## Required JSON Shape

All non-empty strings and SHA256 values below are required. Counts and batch
sizes are positive integers. Additional fields are allowed.

```json
{
  "schema_version": 1,
  "stage": "stage2",
  "version": "v7.x",
  "run_id": "descriptive_run_id",
  "tasks": ["human", "camera", "joint"],
  "generation_modes": ["completion", "parallel"],
  "data": {
    "train_manifest": "path",
    "train_split": "split",
    "train_samples": 1,
    "train_sample_ids_sha256": "64 lowercase hex characters",
    "eval_manifest": "path",
    "eval_split": "split",
    "eval_samples": 1,
    "eval_sample_ids_sha256": "64 lowercase hex characters"
  },
  "parent_stage1": {
    "version": "v7.14",
    "run_id": "run_id",
    "checkpoint": "path",
    "checkpoint_sha256": "64 lowercase hex characters",
    "owning_decoder": "path",
    "owning_decoder_sha256": "64 lowercase hex characters"
  },
  "cache": {
    "train_path": "path",
    "train_sha256": "64 lowercase hex characters",
    "eval_path": "path",
    "eval_sha256": "64 lowercase hex characters",
    "tokenizer_checkpoint_sha256": "64 lowercase hex characters",
    "z_norm_source_train_sha256": "64 lowercase hex characters"
  },
  "train": {"seed": 17, "batch_size": 64},
  "eval": {
    "seed": 17,
    "batch_size": 64,
    "decode_batch_size": 64,
    "sample_count": 4053,
    "sampler": {"steps": 50, "eta": 0.0, "cfg_scale": 1.0}
  }
}
```

For active StoryMotion evaluations, `completion` covers Direct-H and Direct-C,
and `parallel` covers joint generation. `cascade` is not a required evaluation
or promotion mode. A run may add it only for an explicitly declared historical
or root-cause attribution question; such a diagnostic remains non-gating and
must use the same Unified checkpoint as the parallel path.

For Stage1, replace `parent_stage1` and `cache` with `model` and `checkpoint`:

```json
{
  "model": {
    "feature_contract": "pulpmotion_official_normalized_human199_joint_camera14",
    "is_causal": false,
    "human_dim": 199,
    "camera_dim": 14,
    "human_latent_dim": 128,
    "camera_latent_dim": 64,
    "latent_order": "human128+camera64"
  },
  "checkpoint": {
    "path": "path",
    "sha256": "64 lowercase hex characters",
    "owning_decoder": "path",
    "owning_decoder_sha256": "64 lowercase hex characters"
  }
}
```

## Harness Sequence

```bash
python3 scripts/storymotion_run_layout.py init --stage stage2 --run-id RUN_ID --parent-stage1-run STAGE1_RUN
python3 scripts/storymotion_experiment_harness.py audit-contract runs/train/stage2/RUN_ID/experiment_contract.json
python3 scripts/storymotion_stage1_contract_harness.py --help
python3 scripts/storymotion_official_bridge_smoke.py --help
python3 scripts/storymotion_official_full_eval.py --help
python3 scripts/storymotion_experiment_harness.py audit-eval runs/train/stage2/RUN_ID/experiment_contract.json runs/eval/stage2/RUN_ID/joint.json
python3 scripts/storymotion_experiment_harness.py audit-doc PATH_TO_LEDGER.md
```

Run the contract audit after cache creation and before the official evaluator.
Fixed representation errors fail earlier through code assertions. The bridge
smoke checks tensor/key compatibility; the full
evaluator remains the source of official decoded metrics. `audit-eval` rejects
an artifact whose task, split, sample IDs/count, seed, batch sizes, or sampler
differs from the declared run boundary, and independently asserts the fixed
tokenizer representation contract recorded by the cache.

## Metric Table Provenance

Every edited mixed-version metric table needs a `version / run` column and a
non-empty value in every data row. Also state split and evaluated sample count
in the table or its immediately surrounding text. If a perfectly matched
comparison does not exist, say which fields differ and restrict the conclusion
accordingly; do not format it as a controlled ablation.

Never merge camera14 separate and camera14 joint under one camera14 label.
Likewise, distinguish Stage1 reconstruction, Stage2 identity, completion, and
joint-generation metrics.

## Required Decoded Geometry Metrics

Distribution and text-alignment metrics do not substitute for decoded
geometry. A formal artifact is incomplete when a task-applicable metric below
is missing; missing values are not interpreted as either pass or failure.

Stage1 reconstruction must report, on valid frames from the exact ordered eval
IDs and the owning decoder:

- human root-aligned MPJPE, global MPJPE, root ADE, root FDE, and integrated
  yaw geodesic error;
- camera-center ADE, camera-center FDE, and camera-rotation geodesic error;
- the same metrics in valid-length bins `1-64`, `65-128`, `129-192`, and
  `193+`, plus the overall aggregate.

Root-aligned MPJPE removes root translation but does not align heading. Do not
interpret it as local-pose-only quality without a yaw-aware attribution.

Stage2 human, camera, and joint artifacts must record the same applicable
decoded quantities alongside TMR/CLaTr distribution, semantics, and coverage.
Their interpretation depends on the task:

- For free text-to-motion human or joint generation, a single paired ground
  truth is only one valid realization. Paired MPJPE and trajectory error are
  mandatory diagnostics, not standalone hard gates. A selection claim based
  on paired geometry must pre-register Best-of-K or another multi-realization
  protocol.
- For camera completion, paired Cam-ADE/Cam-FDE and rotation error are
  mandatory diagnostics. They are hard gates only when the declared task is
  paired trajectory recovery rather than one-to-many camera generation.
- For temporal completion or inpainting with a held-out ground-truth region,
  MPJPE and Cam-ADE over the masked region are valid hard gates.
- Joint generation additionally reports projection/framing quantities such as
  out-of-screen rate when they are defined by the task. Human-only generation
  must not fail because a joint-only projection metric is absent.

Free-generation promotion also needs no-reference physical diagnostics where
available, including foot contact/skating, acceleration or jerk, bone-length
consistency, and root-speed/path distributions, followed by a blind render
review. Geometry rows retain the exact `version / run`, checkpoint and owning
decoder hashes, split, sample count, IDs, seed, sampler, and decode batch size.
