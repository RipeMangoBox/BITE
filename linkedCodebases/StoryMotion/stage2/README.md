# StoryMotion Stage2 Evidence Index

This directory mirrors valid Stage2 evidence from:

```text
5090:/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/
```

It replaced an older local `analysis/`, `metrics/`, `renders/`, `sources/`, and
`training_logs/` layout whose render files used an incorrect skeleton path. Do
not use the removed legacy render tree for V3 claims.

## Reliability Tiers

| Tier | Directories | Use |
| --- | --- | --- |
| Formal full-test evidence | `p1_parallel_20260615/`, `pulpmotion_official_matrix_20260616/`, `v3_closure_20260616/full/`, `v3_closure_20260616/completion_ablation/`, `v3_closure_20260616/latent_block_gate/` | V3 metric tables and checkpoint-selection conclusions |
| Corrected render evidence | `joint_channel_gated_pulpmotion_fair_compare_20260615/`, `gpu3_obs_selfcond_best_pulpmotion_fair_compare_20260616/`, `v3_closure_20260616/*_pulpmotion_fair_compare/` | Render-level comparison, raw-skeleton gate, sample-level diagnostic only |
| PulpMotion baseline audit | `pulpmotion_official_baseline_20260613/`, `pulpmotion_official_matrix_20260616/` | Pulp official rerun matrix and local bugfix rerun notes |
| Diagnostic and sweep evidence | `bilateral_cfg_matrix_20260614/`, `joint_channel_gated_cfg_matrix_20260615/`, `gpu3_obs_selfcond_best_joint_channel_gated_matrix_20260616/`, `storymotion_p0_diag_20260613/`, `stage2_gated_diag_20260613/`, `stage2_mixed_condition_reliance_20260612/`, `stage2_multiseed_mixed_20260612/`, `stage2_posthoc_*`, `stage2_outlier_audit_fullval_20260612/`, `stage2_trimodal_latent_render_20260612/` | Mechanism probing and debugging; cite with scope and sample count |
| Smoke or early bridge checks | `bilateral_cfg_test/`, `stage2_official_bridge_smoke_20260613/`, `storymotion_official_full_eval_smoke_20260613/`, `stage2_official_eval_20260613/` | Integration validation only, not final metric conclusions |

## Formal V3 Anchors

| Question | Evidence path |
| --- | --- |
| Current StoryMotion joint/completion full metrics | `p1_parallel_20260615/indepdrop_*_full_cfg2.0_eta1.0.json` |
| PulpMotion 16/16 official matrix | `pulpmotion_official_matrix_20260616/full/*.json` |
| Long-training replacement probe | `v3_closure_20260616/full/*.json` |
| Human completion sampler/CFG ablation | `v3_closure_20260616/completion_ablation/*.json` |
| Whole camera-block dependency gate | `v3_closure_20260616/latent_block_gate/*.json` |
| Corrected render comparison | `*_pulpmotion_fair_compare*/manifest.json` plus per-sample `summary.json` |

## Notes

- `*.records.jsonl` files preserve per-sample provenance and sampler settings.
- Render conclusions are diagnostic because current fair-compare packages use two curated samples.
- Full metric conclusions require `evaluated_samples` to match the intended split: mixed full = 10549, pure full = 4053.
- 2026-06-17 Stage1 upper-bound and human completion dependency experiments are generated on 5090 first, then mirrored here after completion.
