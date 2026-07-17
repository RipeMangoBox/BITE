# StoryMotion

StoryMotion keeps source code and generated experiment data in one project
root. The source tree is mirrored in BITE under `linkedCodebases/StoryMotion`;
large checkpoints, caches, evaluations, renders, and runtime logs remain on the
GPU hosts.

## Project Structure

```text
StoryMotion/
  configs/       # Versioned experiment and baseline configuration
  docs/          # Experiment contract and operational documentation
  linked/        # External code/data links such as PulpMotion
  scripts/       # Train, cache, evaluation, rendering, and migration entrypoints
  storymotion/   # Importable model and data implementation
  tests/         # Contract and regression tests

  runs/          # Canonical generated artifacts; three functional first-level roots
    train/
      stage1/<run_id>/  # Checkpoints, events, driver state, contract, manifest
      stage1/{manifests,stats}/  # Declared shared Stage1 inputs
      stage2/<run_id>/  # Checkpoints, per-run cache, driver state, contract, manifest
      stage2/shared/    # Explicitly shared Stage2 train-side assets
    eval/
      stage1/<run_id>/  # Metrics, records, decoded numerical diagnostics
      stage2/<run_id>/
      quality/          # Historical quality-only evidence without a run owner
      semantic_keyframe_mvp/
    vis/
      stage1/<run_id>/  # Rendered media and render manifests
      stage2/<run_id>/

  logs/          # Live logs plus archived inactive logs
  ops/           # Queues, launchers, registries, environment overlays, drivers
  archive/       # Migration manifests and inactive operational snapshots
```

For a normal experiment, the same `run_id` links train, eval, and vis.
`manifest.json` and `experiment_contract.json` live with the train artifacts
and record paths relative to the common `runs` root. Historical visualization-
only imports retain their source ID and do not imply that a matched train run
exists. A render-oriented subtree stays intact in `vis`; do not separate its
media files from the local render manifest.

Older `runs/stage1`, `runs/stage2`, `runs/legacy`, and
`runs/visualizations` paths are compatibility-only. New code must resolve paths
through `scripts/storymotion_run_layout.py`. Temporary compatibility links may
exist while an owning driver or historical reader is active, but they are not
canonical result categories. Therefore a host in transition may temporarily
show more than the three canonical first-level entries.

The checked migration entrypoint is
`scripts/migrate_storymotion_runs_three_root.py`. Run it independently on each
host, protect every active `run_id`, and keep the emitted JSON manifest under
`archive/migration-manifests`; never copy one host's artifacts over the other.

## Experiment Timeline

| Date | Stage | Event |
|------|-------|-------|
| Jun 10 | Stage1 | Pulp frozen tokenizer reconstructions (camera + human) |
| Jun 10 | Stage1 | Pulp latent combinations (sample_sources, per_sample_metrics) |
| Jun 11 | Stage2 | Training: pure split pilots, mixed full from-scratch (82688 steps) |
| Jun 11 | Stage2 | Cache build: `cache_mixed_full_nw0_20260611_2110` (10549 val) |
| Jun 12 | Stage2 | `branch_jh6ft`: resume +20k joint-heavy FT (total 102688 steps) |
| Jun 12 | Stage2 | Diagnostic eval batch: sampler smoke, gate, decomposition, outlier audit |
| Jun 13 | Stage2 | **Official full eval**: 6 jobs × 10549 samples, cfg=1.0 |
| Jun 13 | Stage2 | **P0 diagnostics**: CFG/eta/multi-step sweeps (1024-sample) |
| Jun 13 | Stage2 | PulpMotion official baseline rerun (10549 samples) |
| Jun 14 | Stage2 | Marathon: independent dropout FT (146k steps), full eval OOM at batch=128 |
| Jun 14 | Stage2 | **cfg=2.0/eta=1.0 full eval** (10549 samples, batch=64) — ✅ completed, 4 configs |

## Artifact Policy

- Generated checkpoints, caches, renders, logs, snapshots, and compatibility
  links stay out of Git.
- Align directory structure across hosts; never overwrite one host's artifact
  merely because the other host has the same run name.
- Move data by checked same-filesystem rename. Stop on every non-identical
  destination collision.
- Active run paths and delayed evaluator destinations remain frozen until the
  owning driver exits.
