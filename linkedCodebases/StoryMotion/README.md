# StoryMotion Mirror — Local Artifact Index

Remote origin: `5090:/data/public/ripemangobox/Motion/StoryMotion/`

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

## Directory Structure

```
stage1/                          # PulpMotion frozen tokenizer (Jun 10)
  pulp_combinations/             # Latent combination analysis (CSV, JSON, MD)
  reconstructions/               # Decode → skeleton/camera renders
    camera/                      # 20 MP4 camera trajectory videos
      gt/, concate/, camera_trajectory/
    human/                       # 120 MP4 renders (fixed/orbiting/camera_traj)
      gt/, concate/, vae/, vqvae/
    summary.json

stage2/                          # CondMDI branch-mask inpainting (Jun 11-14)
  analysis/                      # Summary docs + eval scripts (14 files)
    stage2_completed_summary_20260612.{json,md}
    stage2_5090_analysis.md
    trimodal_evaluation_plan.md
    run_stage2_*.py              # 9 diagnostic eval scripts
  sources/                       # PulpMotion reference configs + paper (5 files)
  training_logs/                 # Training logs + cache metadata (mixed/pure splits)

  metrics/                       # === All numerical results (JSON/JSONL/CSV) ===
    official_full_10549/         # StoryMotion 6-job × 10549 full eval (cfg=1.0)
    pulp_baseline/               # PulpMotion official baseline (10549 samples)
    p0_diagnostics/              # CFG/eta/multi-step sweep results (1024-sample)
    marathon/                    # 2026-06-14 marathon (training + partial full eval)
    bilateral_cfg_matrix/        # Bilateral CFG grid eval (24 configs)
    bilateral_cfg_test/          # Bilateral CFG smoke test
    bridge_smoke/                # Official metric bridge integration test
    gated_diagnostics/           # Gated diagnostic results
    joint_decomposition/         # Joint mode per-sample decomposition
    condition_reliance_mixed/    # Mixed split condition reliance gates
    condition_reliance_pure_best/# Pure split best-model condition reliance
    condition_reliance_pure_step/# Pure split step-condition reliance
    multiseed_mixed/             # Multi-seed mixed eval
    per_sample_stats/            # Per-sample statistics
    posthoc_mixed/               # Post-hoc mixed eval
    posthoc_pure/                # Post-hoc pure eval
    outlier_audit/               # Full-val outlier audit
    official_eval_early/         # Early official eval (pre-P0)
    sampler_decode_smoke/        # Sampler decode smoke (JSON results only)
    sampler_decode_stress/       # Sampler stress test (JSON results only)

  renders/                       # === All visualization (PNG / MP4) ===
    bilateral_cfg/               # 42 MP4 + 18 PNG bilateral CFG renders (7 configs)
    decode_smoke/                # 3 PNG decoded skeleton smoke test
    trimodal_latent/             # 5 PNG trimodal (human+camera) latent renders
    sampler_smoke/               # 9 PNG sampler decode renders (3 checkpoints × 3 tasks)
    sampler_stress/              # 10 PNG sampler stress renders (text/visible interventions)
    outlier_audit_plots/         # 2 PNG diagnostic plots (loss CDF + zmax vs task)
```

## NOT in this mirror (on 5090 only)

- Checkpoint files (`*.pt`, ~1.2 GB each): `branch_jh6ft`, `independent_dropout_ft`
- Full cache file: `cache_mixed_full_nw0_20260611_2110/val.pt` (312 MB)
- Training tensorboard logs
