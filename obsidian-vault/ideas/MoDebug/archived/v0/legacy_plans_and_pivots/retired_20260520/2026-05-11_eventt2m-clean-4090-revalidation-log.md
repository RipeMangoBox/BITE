---
created: 2026-05-11T13:55:00+08:00
updated: 2026-05-12T17:35:00+08:00
title: EventT2M Clean 4090 Revalidation Log
status: active
tags:
  - MoDebug
  - EventT2M
  - 4090
  - clean-setup
  - revalidation
related_notes:
  - "[[paperIDEAs/MoDebug/2026-05-11_modebug-route-2-cross-generator-failure-mechanism]]"
  - "[[2026-05-01_modebug-eventt2m-retrain-sanity-plan]]"
---

# EventT2M Clean 4090 Revalidation Log

## Purpose

Revalidate EventT2M as a possible event-conditioned MoDebug backbone without modifying the existing 4090 repo.

## Isolation Rule

Initial clean-clone attempts should not modify:

```text
/data/public/ripemangobox/Motion/EventT2M-codes
```

Use independent clean setup directories only, for example:

```text
/data/public/ripemangobox/Motion/EventT2M-codes-clean-20260511-r2
```

2026-05-11 update: the current task explicitly requested fixing the original EventT2M repo if that was the more suitable path. The local original repo was used for the released-checkpoint legacy run because it had the released HumanML3D checkpoint. The 4090 original repo was then used for latest-progress re-visualization and enhanced-prompt visualization because HumanML3D / HumanML3D-E data are available under `/data/public/ripemangobox/Motion/datasets`.

## Current Remote State

Recorded on 2026-05-11:

| Item | Value |
| --- | --- |
| existing repo | `/data/public/ripemangobox/Motion/EventT2M-codes` |
| existing repo head | `2ac5ea8` after fast-forward |
| existing repo branch | `main` |
| existing repo status | untracked `.codex/` and `artifacts/` |
| GPU state | two RTX 4090 cards visible |

Local code repo:

| Item | Value |
| --- | --- |
| repo | `/data/Life Me/ResearchWY Vault/linkedCodebases/EventT2M-codes-main` |
| fixed commits | `636bee8`, `1677fce`, `ddcc4c8`, `148295d`, `2ac5ea8` |
| remote sync | pushed to `origin/main`; 4090 HEAD is `2ac5ea8` |
| unrelated dirty files | preserved and not committed: `dataset/HumanML3D-E`, attention-analysis scripts, debug runners, pending assets |

## Official Availability

Official source:

- repo: [tjswodud/EventT2M-codes](https://github.com/tjswodud/EventT2M-codes)
- README: [readme.md](https://github.com/tjswodud/EventT2M-codes/blob/main/readme.md)

README-level resources:

| Resource | README availability | Active trust status |
| --- | --- | --- |
| source code | public GitHub repo | available in principle; 4090 GitHub network currently blocked |
| TMR submodule | public GitHub submodule | must initialize in clean repo |
| HumanML3D-E | Google Drive file | must download and verify |
| pretrained EventT2M ckpts | Google Drive folder | must download and verify |
| deps | OneDrive link | must download and verify |
| raw HumanML3D / KIT-ML | upstream HumanML3D instructions | must prepare or symlink with provenance |

## Attempt Log

| Date | Target | Command family | Result | Role |
| --- | --- | --- | --- | --- |
| 2026-05-11 | `/data/public/ripemangobox/Motion/EventT2M-codes-clean-20260511` | full `git clone` | failed: GitHub 443 connection timed out after about 135s | setup blocker |
| 2026-05-11 | `/data/public/ripemangobox/Motion/EventT2M-codes-clean-20260511-r2` | shallow recursive `git clone --depth 1 --recursive` | stopped after hanging on GitHub clone; no old repo modification | setup blocker |
| 2026-05-11 | local original EventT2M repo | `sample_motion.yaml` x0 sampling fix + legacy M0 runner | committed as `636bee8`; default epsilon sampling produced invalid hundreds-scale joints, fixed x0 sampling produced HumanML3D-scale joints | diagnostic code fix |
| 2026-05-11 | 4090 original EventT2M repo | `git fetch` via SSH, then HTTPS fetch + fast-forward merge | SSH fetch hung; HTTPS fetch succeeded; remote HEAD is `636bee8` | remote sync |
| 2026-05-11 | 4090 original EventT2M repo | HumanML3D-E `003245` epoch135 re-vis before config-order fix | GT normal; generated skeleton hundreds-scale abnormal because `sample_motion.yaml` did not actually override default epsilon | obsolete diagnostic |
| 2026-05-11 | local original EventT2M repo | Hydra defaults order fix in `sample_motion.yaml` | committed as `2ac5ea8`; moves `_self_` after imported defaults so `model.noise_scheduler.prediction_type=sample` takes effect | diagnostic code fix |
| 2026-05-11 | 4090 original EventT2M repo | fast-forward to `2ac5ea8` + HumanML3D-E `003245` epoch135 re-vis | resolved config reports `RESOLVED_NOISE_PREDICTION_TYPE sample`; generated skeleton returns to HumanML3D scale | diagnostic cross-check |
| 2026-05-11 | 4090 original EventT2M repo | enhanced prompt 18x5 visualization | 90/90 generated; 90 MP4; 90 static plots; synced back to vault | diagnostic visualization |

## 4090 Latest-Progress Re-Vis

Inputs:

| Item | Value |
| --- | --- |
| repo | `/data/public/ripemangobox/Motion/EventT2M-codes` |
| head | `2ac5ea8` |
| data file | `/data/public/ripemangobox/Motion/datasets/HumanML3D/HumanML3D-E/data_test.npy` |
| data dir | `/data/public/ripemangobox/Motion/datasets/HumanML3D/HumanML3D` |
| checkpoint | `logs/event/runs/eventt2m_clean_hml3d_retrain_seed1/checkpoints/epoch=135.ckpt` |
| previous result dir | `artifacts/modebug_eventt2m_epoch135_revis_20260511` |
| after-fix result dir | `artifacts/modebug_eventt2m_epoch135_revis_20260511_after_config_fix` |
| fetched vault copy | `artifacts/remote4090/modebug_eventt2m_epoch135_revis_20260511_after_config_fix` |

Resolved config after `2ac5ea8`:

```text
RESOLVED_NOISE_PREDICTION_TYPE sample
RESOLVED_SAMPLE_PREDICTION_TYPE epsilon
```

`sample_motion()` branches on `model.noise_scheduler.prediction_type`, so `sample` is the required x0-compatible path.

Result for HumanML3D-E sample `003245` after the config-order fix:

| Source | Joint abs mean | Min | Max | Root x span | Root z span |
| --- | ---: | ---: | ---: | ---: | ---: |
| GT | `0.3901` | `-0.3615` | `2.0130` | `0.0075` | `0.0467` |
| epoch135 generated | `0.4229` | `-0.7392` | `1.9033` | `0.0608` | `0.1869` |

Obsolete pre-fix result:

| Source | Joint abs mean | Min | Max | Root x span | Root z span |
| --- | ---: | ---: | ---: | ---: | ---: |
| epoch135 generated before `2ac5ea8` | `28.8915` | `-191.0240` | `125.7057` | `54.4010` | `44.9228` |

Interpretation: the earlier epoch135 scale failure was caused by a Hydra defaults ordering bug: the `model: event_final` default was overriding `sample_motion.yaml` back to epsilon. After `2ac5ea8`, the same `003245` diagnostic returns to HumanML3D scale. This removes the immediate scale-sanity blocker for this single diagnostic sample, but it is still `diagnostic` / `observation`, not backbone-selection evidence, full-level safety, or held-out final evaluator evidence.

## Enhanced Prompt EventT2M Visualization

Target manifest:

```text
artifacts/modebug_battery_m0_v2_20260508/m0_gt_paired_fixed_repeat_20260510_generation_manifest.tsv
```

Result artifacts in the vault:

| Artifact | Value |
| --- | --- |
| result dir | `artifacts/modebug_battery_m0_v2_20260508/results/eventt2m` |
| geometry audit | `results/eventt2m/geometry_audit.csv` |
| trace summary | `results/eventt2m/trace_summary.jsonl` |
| run manifest | `results/eventt2m/run_manifest.json` |
| videos | `results/eventt2m/videos/` |
| static plots | `results/eventt2m/static_plots/` |
| by-model index | `artifacts/modebug_battery_m0_v2_20260508/by_model/eventt2m/` |

Audit summary:

| Field | Value |
| --- | ---: |
| prompts | 90 |
| generated OK | 90 |
| MP4 videos | 90 |
| static plots | 90 |
| raw-tier trace summary dirs | 62 |
| role | `diagnostic` |
| used_for | `observation` |

Limitations:

- Earlier 2026-05-11 enhanced-prompt outputs before the config-order fix should be treated as obsolete because they used the wrong effective sampling path.
- Use the fixed outputs as a fourth-model visualization / diagnostic column only.
- Do not use them as `backbone_selection`, `final_eval`, FID/R-Precision evidence, or formal ordering evidence.

## Archived Legacy M0 v2 Diagnostic Run

Target battery:

```text
artifacts/modebug_battery_m0_v2_20260508/archived_legacy_m0_v2_20260510/m0_v2_generation_manifest.tsv
```

Command family:

```bash
PYTHONPATH=. /home/ripemangobox/miniconda3/envs/event-t2m/bin/python \
  src/run_modebug_m0_legacy_eventt2m.py \
  --manifest "/data/Life Me/ResearchWY Vault/artifacts/modebug_battery_m0_v2_20260508/archived_legacy_m0_v2_20260510/m0_v2_generation_manifest.tsv" \
  --result-dir "/data/Life Me/ResearchWY Vault/artifacts/modebug_battery_m0_v2_20260508/archived_legacy_m0_v2_20260510/results/eventt2m" \
  --device cpu \
  --step-num 10 \
  --render-videos
```

Result artifacts:

| Artifact | Value |
| --- | --- |
| result dir | `artifacts/modebug_battery_m0_v2_20260508/archived_legacy_m0_v2_20260510/results/eventt2m` |
| geometry audit | `results/eventt2m/geometry_audit.csv` |
| trace summary | `results/eventt2m/trace_summary.jsonl` |
| run manifest | `results/eventt2m/run_manifest.json` |
| videos | `results/eventt2m/videos/` |
| raw motions | `results/eventt2m/native_outputs/raw_263/` |
| joints | `results/eventt2m/native_outputs/joints/` |

Audit summary:

| Field | Value |
| --- | ---: |
| prompts | 90 |
| generated OK | 90 |
| mp4 videos | 90 |
| static plots | 90 |
| raw-tier trace summary dirs | 42 |
| role | `diagnostic` |
| used_for | `observation` |

Sampling fix evidence:

| Config | Raw 263 abs mean | Joint abs mean | Interpretation |
| --- | ---: | ---: | --- |
| default epsilon sampling smoke | 106.383 | 97.166 | invalid scale; hundreds-scale joints |
| fixed x0 sampling smoke | 0.310 | 1.102 | HumanML3D-scale finite skeleton |

The fixed run uses:

```text
model.noise_scheduler.prediction_type=sample
model.denoiser.stage_dim=256*4
```

Limitations:

- The archived legacy M0 v2 battery is synthetic and has no paired GT motion distribution.
- These results are diagnostic observations, not FID/R-Precision or held-out final evaluator evidence.
- Event decomposition for this legacy run is rule-split from prompt text, not a manually verified event list.

## Gradio Integration

Gradio was updated to load four models by default:

```text
motiongpt,momask,mogents,eventt2m
```

Launch command:

```bash
cd "/data/Life Me/ResearchWY Vault"
PORT=7862 bash MoDebug_gradio.sh
```

Verified local URL:

```text
http://127.0.0.1:7862/
```

Current UI status:

- `MoDebug_gradio.sh` defaults to `m0_gt_paired_fixed_repeat_20260510_battery.tsv`, `m0_gt_paired_fixed_repeat_20260510_generation_manifest.tsv`, `gt_reference_map_gt_paired_20260510.tsv`, and `results/`.
- `motiongpt`, `momask`, `mogents`, and `eventt2m` first-prompt videos all resolve locally.
- Verified URL: `http://127.0.0.1:7862/`.

Remote logs:

```text
/data/public/ripemangobox/Motion/EventT2M-codes/logs/remote4090/eventt2m_clean_20260511_setup.log
/data/public/ripemangobox/Motion/EventT2M-codes/logs/remote4090/eventt2m_clean_20260511_clone2.log
```

## Revalidation Gates

2026-05-12 update: the clean retrain checkpoint passed the 4090 numeric geometry gate under fixed x0 sampling, a 10-sample MP4 rendering subset passed after exposing an explicit `ffmpeg` path and forcing the HuggingFace text encoder to use the local offline cache, and the official released `hml3d.ckpt` was uploaded to 4090 and passed the same core gate family. Checkpoint provenance is no longer a blocker for the official HumanML3D checkpoint. A direct fixed-caption same-seed event-list sensitivity gate was then run on the official checkpoint for four HumanML3D-E samples with `full`, `blank`, `drop`, and reverse-order `shuffle` event lists. The `blank` and `drop` variants changed the generated motion for all `4/4` samples while preserving finite HumanML3D-scale geometry and `16/16` MP4/static renders. Reverse-order `shuffle` was weak: `3/4` samples were numerically identical to `full`, and `1/4` showed only a small nonzero difference. The event-list input path is therefore no longer unproven, but EventT2M should currently be treated as an event-presence / omission-sensitive candidate rather than a strong ordering-sensitive mechanism probe.

## Remaining Gate Terms

`event-list input path` means the actual code path from a user-provided event list to the model's conditioning tensors. For EventT2M, the caption alone is not enough evidence, because the architecture also accepts `decomposed_text`. To trust EventT2M as an event-conditioned backbone, we need to show that changing only the event list while keeping the caption, length, seed, checkpoint, and sampler fixed changes the generated motion or trace in a plausible way. The minimum gate is: original event list vs blank event list vs dropped event vs shuffled event list, with the same prompt and seed, plus geometry sanity and qualitative review. The 2026-05-12 official-checkpoint gate satisfies the direct-path existence test for event presence / omission because `blank` and `drop` both produced nonzero motion changes on `4/4` samples under a fixed caption and seed. It does not yet establish strong order sensitivity because reverse-order `shuffle` was zero-difference on `3/4` samples and only weakly nonzero on `1/4`.

`checkpoint provenance` means knowing exactly which weights were evaluated: source, path, hash, training lineage, and load result. On 2026-05-12, local `linkedCodebases/EventT2M-codes-main/checkpoints/pretrained/HumanML3D/hml3d.ckpt` was uploaded to remote `/data/public/ripemangobox/Motion/EventT2M-codes/checkpoints/pretrained/HumanML3D/hml3d.ckpt`, size `187M`, sha256 `a8525a54b6ca89666bb1a25e2bcaa1cd4f62e0ba8ca1112e3f73b296e752b5c9`. The checkpoint loads in original `src/sample_motion.py`, the M0 GT-paired numeric gate, and a native `src/eval.py` test loop. The clean retrain `epoch=135.ckpt` remains diagnostic evidence, not the official pretrained checkpoint.

| Gate | Status | Evidence |
| --- | --- | --- |
| repo provenance | pass for current 4090 repo | `/data/public/ripemangobox/Motion/EventT2M-codes @ 2ac5ea8`; archive labels include `eventt2m-full-gate-before-20260511`, `eventt2m-official-ckpt-before-upload-20260512`, and `eventt2m-official-native-eval-smoke-20260512` |
| data availability | pass for gate run | manifest `artifacts/modebug_battery_m0_v2_20260508/m0_gt_paired_fixed_repeat_20260510_generation_manifest.tsv`; HumanML3D dir `/data/public/ripemangobox/Motion/datasets/HumanML3D/HumanML3D` |
| official checkpoint availability | pass | remote `checkpoints/pretrained/HumanML3D/hml3d.ckpt`, size `187M`, sha256 `a8525a54b6ca89666bb1a25e2bcaa1cd4f62e0ba8ca1112e3f73b296e752b5c9`; successful load in `src/sample_motion.py`, M0 numeric gate, and native eval loop |
| clean retrain checkpoint availability | pass | `logs/event/runs/eventt2m_clean_hml3d_retrain_seed1/checkpoints/epoch=135.ckpt`; sha256 `184a2b4958d493bc74f2f4e935c05c3600f1946c806c6622d85977a41b8214d4` |
| generated-motion numeric geometry | pass for clean retrain and official checkpoint fixed-x0 runs | clean retrain 90/90 generated OK; official `hml3d.ckpt` 90/90 status `ok`, finite_rate all `1.0`, static plots 90/90 |
| old failure localization | pass | forced old epsilon sampling reproduces hundreds-scale / tens-scale abnormal spans on the same checkpoint/data |
| video rendering | pass for fixed-x0 subset and native official sample | clean retrain subset: 10/10 generated OK, 10 MP4, 10 static plots; official `src/sample_motion.py`: 3/3 MP4 and 3/3 static PNG |
| native sample_motion visualization | pass for clean retrain and official checkpoint | clean retrain native videos at `artifacts/remote4090/remote4090_eventt2m_native_vis_20260512/native_sample_125000/videos` were manually judged reasonable by the user; official checkpoint native run produced 3/3 finite HumanML3D-scale samples and videos |
| native eval smoke | pass for native test loop; retrieval sidecar asset gap remains | `src/eval.py` with official `hml3d.ckpt`, `model.metrics.enable_mm_metric=false`, batch 64 x 1, saved native metrics; the later retrieval exporter fails on missing TMR KIT feature `kick_high_left02_poses.npy`, which is not a generation/checkpoint gate |
| event-conditioned sanity | partial pass | direct event-list path is active for blank/drop perturbations on official `hml3d.ckpt`; reverse-order shuffle sensitivity is weak, and manual review is still unrecorded |

Metric records:

| Record | Value |
| --- | --- |
| date | 2026-05-11T21:31:32+08:00 |
| artifact_path | `artifacts/remote4090/remote4090_eventt2m_full_gate_20260511_bundle/` |
| evaluator | `modebug_m0_v2_geometry_trace_audit` |
| protocol | `eventt2m_full_gate_20260511 fixed x0 numeric-only 18x5 M0 GT-paired battery` |
| motion_source | EventT2M clean retrain `epoch=135.ckpt` on 4090 GPU1 with fixed x0/sample `prediction_type` |
| condition_pair | `full/drop`, `full/replace`, `full/shuffle`, `full/repeat` |
| n/evaluable | 90/90 |
| coverage | 18 GT-paired base cases x 5 conditions; static plots rendered; videos tracked separately |
| role | `diagnostic` |
| used_for | observation |
| limitations | Numeric and static-plot gate only; not held-out final evaluator evidence; event-list input sensitivity not yet proven |

| Record | Value |
| --- | --- |
| date | 2026-05-12T12:38:49+08:00 |
| artifact_path | `artifacts/remote4090/remote4090_eventt2m_video_subset_offline_20260512/` |
| evaluator | `modebug_m0_v2_geometry_trace_audit` |
| protocol | `eventt2m fixed x0 video subset offline cache with explicit ffmpeg` |
| motion_source | EventT2M clean retrain `epoch=135.ckpt` on 4090 GPU1 with fixed x0/sample `prediction_type`; ckpt sha256 `184a2b4958d493bc74f2f4e935c05c3600f1946c806c6622d85977a41b8214d4` |
| condition_pair | `full/drop`, `full/replace`, `full/shuffle`, `full/repeat` |
| n/evaluable | 10/10 |
| coverage | 2 GT-paired base cases x 5 conditions; 10 MP4 videos and 10 static plots rendered |
| role | `diagnostic` |
| used_for | observation |
| limitations | Video/rendering smoke only; not held-out final evaluator evidence; event-list input sensitivity not yet proven; this specific record used the clean retrain checkpoint rather than the official released checkpoint |

| Record | Value |
| --- | --- |
| date | 2026-05-12T12:50:07+08:00 |
| artifact_path | `artifacts/remote4090/remote4090_eventt2m_native_vis_20260512/` |
| evaluator | `native_sample_motion_geometry_and_render_smoke` |
| protocol | EventT2M original repo `src/sample_motion.py` default prompt, clean retrain checkpoint, fixed x0/sample sampling |
| motion_source | 4090 `/data/public/ripemangobox/Motion/EventT2M-codes @ 2ac5ea8`, clean retrain `epoch=135.ckpt` via symlink `artifacts/eventt2m_native_vis_20260512/ckpt_epoch135.ckpt` |
| condition_pair | none; original native visualization prompt only |
| n/evaluable | 3/3 |
| coverage | default `configs/sample_motion.yaml` prompt, `repeats=3`, length 199; 3 native `.npz`, 3 static PNG, 3 MP4 |
| role | `diagnostic` |
| used_for | observation |
| limitations | Native visualization smoke only; not MoDebug prompt battery; not event-list sensitivity evidence; not official released checkpoint evidence |

| Record | Value |
| --- | --- |
| date | 2026-05-12T13:20:00+08:00 |
| artifact_path | `artifacts/remote4090/remote4090_eventt2m_native_vis_20260512/native_sample_125000/videos` |
| evaluator | `manual_visual_review_by_user` |
| protocol | Clean retrain native `src/sample_motion.py` default prompt videos |
| motion_source | 4090 `/data/public/ripemangobox/Motion/EventT2M-codes @ 2ac5ea8`, clean retrain `epoch=135.ckpt` via symlink `artifacts/eventt2m_native_vis_20260512/ckpt_epoch135.ckpt` |
| condition_pair | none; original native visualization prompt only |
| n/evaluable | 3/3 |
| coverage | User visual review of 3 native MP4 videos under `native_sample_125000/videos` |
| role | `diagnostic` |
| used_for | observation |
| limitations | Manual video sanity only; not event-list sensitivity evidence; not held-out final evaluator evidence; clean retrain, not official released checkpoint |

| Record | Value |
| --- | --- |
| date | 2026-05-12T13:20:00+08:00 |
| artifact_path | `artifacts/remote4090/remote4090_eventt2m_official_gate_20260512/` and `artifacts/remote4090/remote4090_eventt2m_official_gate_20260512_eval_update/` |
| evaluator | `checkpoint_provenance_and_load_smoke` |
| protocol | Upload local official `hml3d.ckpt` to 4090 and verify size, sha256, and successful load in original EventT2M scripts |
| motion_source | local `linkedCodebases/EventT2M-codes-main/checkpoints/pretrained/HumanML3D/hml3d.ckpt` -> remote `checkpoints/pretrained/HumanML3D/hml3d.ckpt`; sha256 `a8525a54b6ca89666bb1a25e2bcaa1cd4f62e0ba8ca1112e3f73b296e752b5c9`; remote repo `2ac5ea88319884b2c8289cade7236cb37dacadfb` |
| condition_pair | none |
| n/evaluable | 1/1 checkpoint |
| coverage | File present on 4090, size `187M`; loaded by `src/sample_motion.py`, `src/run_modebug_m0_legacy_eventt2m.py`, and native `src/eval.py` test loop |
| role | `diagnostic` |
| used_for | observation |
| limitations | Provenance/load gate only; does not prove event-list input sensitivity or final model quality |

| Record | Value |
| --- | --- |
| date | 2026-05-12T13:20:25+08:00 |
| artifact_path | `artifacts/remote4090/remote4090_eventt2m_official_gate_20260512/eventt2m_official_gate_20260512/native_sample_132018/` |
| evaluator | `native_sample_motion_geometry_and_render_smoke` |
| protocol | EventT2M original repo `src/sample_motion.py` default prompt, official `hml3d.ckpt`, fixed x0/sample sampling |
| motion_source | official remote `checkpoints/pretrained/HumanML3D/hml3d.ckpt`, sha256 `a8525a54b6ca89666bb1a25e2bcaa1cd4f62e0ba8ca1112e3f73b296e752b5c9`; repo `2ac5ea88319884b2c8289cade7236cb37dacadfb` |
| condition_pair | none; original native visualization prompt only |
| n/evaluable | 3/3 |
| coverage | default `configs/sample_motion.yaml` prompt, `repeats=3`, length 199; 3 native `.npz`, 3 static PNG, 3 MP4 |
| role | `diagnostic` |
| used_for | observation |
| limitations | Native visualization smoke only; not MoDebug prompt battery; not event-list sensitivity evidence |

| Record | Value |
| --- | --- |
| date | 2026-05-12T13:22:11+08:00 |
| artifact_path | `artifacts/remote4090/remote4090_eventt2m_official_gate_20260512_eval_update/eventt2m_official_gate_20260512/fixed_x0_official_m0_gt_numeric/` |
| evaluator | `modebug_m0_v2_geometry_trace_audit` |
| protocol | `official hml3d.ckpt fixed x0 numeric-only 18x5 M0 GT-paired battery` |
| motion_source | official remote `checkpoints/pretrained/HumanML3D/hml3d.ckpt`, sha256 `a8525a54b6ca89666bb1a25e2bcaa1cd4f62e0ba8ca1112e3f73b296e752b5c9`; repo `2ac5ea88319884b2c8289cade7236cb37dacadfb`; fixed x0/sample `prediction_type` |
| condition_pair | `full/drop`, `full/replace`, `full/shuffle`, `full/repeat` |
| n/evaluable | 90/90 |
| coverage | 18 GT-paired base cases x 5 conditions; static plots 90/90; condition counts 18 each for `full`, `drop`, `replace`, `shuffle`, `repeat` |
| role | `diagnostic` |
| used_for | observation |
| limitations | Numeric/static gate only; not held-out final evaluator evidence; event-list input sensitivity not yet proven |

| Record | Value |
| --- | --- |
| date | 2026-05-12T13:26:36+08:00 |
| artifact_path | `artifacts/remote4090/remote4090_eventt2m_official_gate_20260512_eval_update/eventt2m_official_gate_20260512/native_eval_smoke_132624/hydra_run/metrics.json` |
| evaluator | `eventt2m_native_eval_loop_smoke` |
| protocol | `src/eval.py` with official `hml3d.ckpt`, `model.metrics.enable_mm_metric=false`, `data.test_batch_size=64`, `+trainer.limit_test_batches=1`, `model.metrics.replicate_times=1` |
| motion_source | official remote `checkpoints/pretrained/HumanML3D/hml3d.ckpt`, sha256 `a8525a54b6ca89666bb1a25e2bcaa1cd4f62e0ba8ca1112e3f73b296e752b5c9`; repo `2ac5ea88319884b2c8289cade7236cb37dacadfb` |
| condition_pair | none; native test dataloader |
| n/evaluable | 64/64 native test samples in 1 batch |
| coverage | Native diffusion test loop completed and saved `metrics.json`: FID mean `0.5718`, R_precision_top_1 mean `0.625`, R_precision_top_2 mean `0.796875`, R_precision_top_3 mean `0.875`; diversity is `-1` because one smoke batch is below diversity sample count |
| role | `diagnostic` |
| used_for | observation |
| limitations | Smoke-scale metric only; after native metrics save, `src/eval.py` retrieval exporter fails because TMR KIT feature file `third_packages/TMR/datasets/motions/guoh3dfeats/KIT/3/kick_high_left02_poses.npy` is absent; do not treat this as final evaluator evidence |

| Record | Value |
| --- | --- |
| date | 2026-05-12T17:29:00+08:00 |
| artifact_path | `artifacts/remote4090/remote4090_eventt2m_event_list_sensitivity_gate_20260512/` |
| evaluator | `eventt2m_direct_event_list_sensitivity_gate` |
| protocol | official `hml3d.ckpt`, fixed caption / length / seed, variants `full`, `blank`, `drop`, reverse-order `shuffle`, with MP4/static rendering |
| motion_source | official remote `checkpoints/pretrained/HumanML3D/hml3d.ckpt`, sha256 `a8525a54b6ca89666bb1a25e2bcaa1cd4f62e0ba8ca1112e3f73b296e752b5c9`; repo `2ac5ea88319884b2c8289cade7236cb37dacadfb`; `CUDA_VISIBLE_DEVICES=1`; fixed x0/sample `prediction_type` |
| condition_pair | `full/blank`, `full/drop`, `full/shuffle` |
| n/evaluable | `16/16` variants across `4/4` HumanML3D-E samples |
| coverage | sample ids `004965`, `008463`, `001969`, `003245`; `16/16` finite joints, `16/16` static plots, `16/16` MP4 videos |
| role | `diagnostic` |
| used_for | observation |
| limitations | Direct input-path gate only; not held-out final evaluator evidence; reverse-order shuffle is weak (`3/4` zero-diff, `1/4` small nonzero), so ordering sensitivity is not yet promoted |

Numeric summary:

| Run | n/evaluable | Joint abs mean median | Mean joint step median | Root x span median | Root z span median | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| fixed x0 / sample | 90/90 | `0.7366` | `0.0353` | `1.2655` | `1.8043` | HumanML3D-scale finite skeletons |
| official hml3d.ckpt fixed x0 / sample | 90/90 | `0.7156` | `0.0348` | `1.2479` | `1.5829` | HumanML3D-scale finite skeletons |
| forced old epsilon | 90/90 | `30.1633` | `47.1277` | `74.3639` | `76.4352` | invalid scale; reproduces old inference failure |

Event-list sensitivity summary:

| Variant vs `full` | n/evaluable | Finite / render status | Joint diff median | L2 diff median | Interpretation |
| --- | ---: | --- | ---: | ---: | --- |
| `blank` | `4/4` | `16/16` finite joints; `4/4` MP4 and `4/4` static plots OK | `0.1415` | `23.4071` | event-list removal changes generation on all tested samples |
| `drop` | `4/4` | `16/16` finite joints; `4/4` MP4 and `4/4` static plots OK | `0.1292` | `19.1008` | target-event removal changes generation on all tested samples |
| reverse-order `shuffle` | `4/4` | `16/16` finite joints; `4/4` MP4 and `4/4` static plots OK | `0.0000` | `0.0000` | order perturbation is weak: `3/4` zero-diff, `1/4` small nonzero (`joint_diff_l2=0.6104`) |

Native `sample_motion.py` summary:

| Run | n/evaluable | Joint abs mean range | Mean joint step range | Root x span range | Root z span range | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| clean retrain original repo default prompt | 3/3 | `0.5816-0.6698` | `0.0437-0.0469` | `0.6314-0.7580` | `2.1042-2.7027` | HumanML3D-scale finite skeletons; MP4/static rendering works; user judged videos reasonable |
| official hml3d.ckpt original repo default prompt | 3/3 | `0.6620-0.7343` | `0.0332-0.0411` | `0.9216-1.6428` | `1.8428-2.3313` | HumanML3D-scale finite skeletons; MP4/static rendering works |

Diagnosis:

```text
same data + same epoch135 checkpoint + fixed x0/sample inference -> HumanML3D-scale geometry
same data + same epoch135 checkpoint + forced old epsilon inference -> large-scale abnormal geometry
```

This localizes the prior numerical-scale failure primarily to the inference sampling configuration, specifically treating an x0/sample checkpoint as epsilon during sampling. It does not implicate the HumanML3D data or the epoch135 clean retraining checkpoint as the first-order cause of the old scale anomaly.

The video-rendering failure was environmental, not a motion-data failure. The first render attempt failed because the event-t2m environment did not expose `ffmpeg` on PATH and Matplotlib `FFMpegWriter.isAvailable()` was false. The 2026-05-12 rerun passed after using the cached DistilBERT assets offline and providing:

```text
--ffmpeg-path /home/ripemangobox/miniconda3/envs/MoPa/bin/ffmpeg
TRANSFORMERS_OFFLINE=1
HF_DATASETS_OFFLINE=1
```

EventT2M has passed the core non-event-list gates for diagnostic use: official checkpoint provenance/load, fixed-x0 numeric geometry, native visualization/rendering, old sampling-failure localization, and a native `src/eval.py` test loop. The direct event-list path is now also proven active for event presence / omission under the official checkpoint. It remains partially gated because manual review of the new 16 MP4 perturbation set is not yet recorded and reverse-order `shuffle` did not show strong order sensitivity on this 4-sample gate. A separate retrieval-protocol sidecar asset gap remains, but it is not the same as the EventT2M generation gate.

| Gate | Current status / evidence |
| --- | --- |
| official released checkpoint provenance | passed for `hml3d.ckpt`: size, sha256, and load records above |
| native eval smoke | native test loop passed and saved metrics; full `src/eval.py` exits nonzero only after the later retrieval exporter hits missing TMR KIT feature assets |
| video rendering | passed for 10-sample subset and original `sample_motion.py` default prompt; rerun full 90-sample MP4 only if needed for review assets |
| event-conditioned sanity | partially passed: `blank` and `drop` change generation on `4/4` official-checkpoint samples with fixed caption/seed; reverse-order `shuffle` is weak (`3/4` zero-diff, `1/4` small nonzero), so treat EventT2M as presence / omission-sensitive but not yet a strong ordering probe |

## Next Actions

1. Record manual review for the `16` fetched MP4 videos under `artifacts/remote4090/remote4090_eventt2m_event_list_sensitivity_gate_20260512/videos/`, especially whether `blank` / `drop` edits visibly suppress the target event and whether sample `001969` is the only order-sensitive case.
2. Use the official released HumanML3D checkpoint as the active EventT2M candidate for future presence / omission conditioning diagnostics; keep clean retrain `epoch135` as diagnostic cross-check evidence.
3. If ordering-sensitive EventT2M evidence is still needed, add stronger order perturbations or trace-side attention export rather than assuming reverse-order sensitivity from the current 4-sample gate.
4. Do not promote EventT2M into active MoDebug ordering claims or replace MotionGPT as the first mechanism probe until the new videos are manually reviewed and the ordering-sensitivity expectation is clarified. If retrieval metrics are needed later, repair the missing TMR KIT feature asset separately.
