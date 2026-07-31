---
title: "StoryMotion v7.12 Clean Data, Reconstruction, and Metric Diagnosis"
status: superseded
hypothesis: |
  v7.12 keeps the v7.5 clean-data conclusion but updates the Stage1 tokenizer diagnosis: camera-side and caption F1 can improve strongly while human TMR-family coverage collapses. The current evidence points to a representation / metric-contract and joint-coupling problem, not to pure training loss alone.
tags:
  - StoryMotion
  - Motion_Generation
  - data_quality
  - reconstruction
  - experiment
  - status/superseded
aliases:
  - StoryMotion-v7.12
source_notes:
  - "[[2026-07-06_storymotion-v7.4-causal-asymmetry]]"
  - "[[2026-07-01_storymotion-v7.3.1-metric-data]]"
created: 2026-07-07T00:00:00+0800
updated: 2026-07-11T11:33:00+0800
---

# StoryMotion v7.12 Clean Data, Reconstruction, and Metric Diagnosis

> [!warning] Superseded evidence
> 本页包含受旧 raw human199 + camera9 训练契约和重复反归一化 eval 错误影响的历史结果，不再用于路线判断。有效结果见 [[2026-07-11_storymotion-v7.14-corrected-results]]；当前路线见 [[2026-07-11_storymotion-latest-roadmap]]。

> [!abstract] 当前裁决
> v7.5 不把“清洗数据”当作解决 StoryMotion 核心问题的充分方案。v7.12 进一步说明：camera-side reconstruction / caption F1 可以显著提升，但 human TMR-family 与 Out 仍然崩溃。当前判断应从“loss 是否更低”转向“official metric 契约、human embedding manifold、human-camera 联合约束是否匹配”。PulpMotion Stage1 当前没有滑窗切片，但 padding mask 正确；直接改成固定192帧滑窗会丢掉约91%的Stage1样本，不应作为下一步默认长训方案。

> [!note] Version note
> 文件名保留创建时的 v7.5 历史名；本页内容以正文和 frontmatter 的 v7.12 为准。

## 0. Data Scope Ledger

本页同时记录 data-cleaning 与 Stage1 tokenizer 实验，必须分清 `clean-mixed` 与 `original-mixed`：

| scope label | exact data | sample count used here | experiments in this note | fair-comparison rule |
| --- | --- | ---: | --- | --- |
| clean-mixed | v7.5 conservative clean cache `cache_mixed_full_clean_initial` | train `75682`, val `8399` | clean data filter, human_text clean fine-tune, clean-val reconstruction diagnosis | only compare against clean-cache controls |
| original paired full / pure official | unfiltered paired human/camera manifests; test ids exactly match official `pure_` | Stage1 paired test `4053`; official mixed anchor rows `10549` separately | Stage1 tokenizer train/eval/vis, official Pulp pretrained tokenizer upper bound | compare with original paired tokenizer rows; do not mix with clean-mixed fine-tune as direct ranking |
| original-mixed official Pulp pretrained | official pretrained Pulp Stage1 AE decoded by official evaluator | mixed `10549`, pure `4053` | upper-bound reference | mark as official pretrained upper bound, not StoryMotion retrain |

Therefore the human-stronger tokenizer and non-causal VAE ablations below are **not clean-mixed experiments**. They are original paired full Stage1 tokenizer ablations. The only clean-mixed experiment in this note is the conservative clean cache / human_text clean fine-tune line.

## 1. 问题定位

v7.4 的人工可视化发现两类问题混在一起：

- GT 本身存在明显漂移、动作与 human text 不符的样本。
- human_text / p2b 生成质量并没有接近 GT human，上限判断因此被污染。

v7.5 的最小目标不是证明新架构成功，而是拆开两个问题：

```text
data noise problem:
  obvious-bad GT samples -> contaminate training/eval/visual audit

representation problem:
  VAE / VQVAE / FSQ / HFSQ / GRFSQ reconstruction quality

generation problem:
  P(H | human_text) learns weak motion distribution even when data is cleaner
```

如果清洗后 human_text 仍不能稳定改善，则下一步不应继续无脑长训同一结构，而应回到 human generator / data objective / architecture 的核心改动。

## 2. 初步清洗规则

Script:

```text
linkedCodebases/StoryMotion/scripts/storymotion_v75_clean_filter.py
```

Remote artifact:

```text
/data/public/ripemangobox/Motion/StoryMotion/runs/quality/v7_5_initial_clean_conservative_20260707
```

Conservative ignore rules:

| rule | ignore criterion | rationale |
| --- | --- | --- |
| `severe_global_drift` | `root_disp > 6.0` or `root_path > 14.0` or `xy_span > 6.0` or `max_step > 3.0` | remove obviously unstable global motion |
| `stationary_text_root_drift` | stationary-like text and `root_disp > 1.2` or `root_path > 2.5` or `xy_span > 1.0` | text says standing/sitting/posing-like action, but root travels strongly |
| `large_vertical_span_without_text_support` | `z_span > 3.0` without jump/stair/climb/stand-up/squat cues | remove vertical outliers not supported by text |

Review-only rules are intentionally weaker and are not removed in the first clean cache:

| rule | review criterion |
| --- | --- |
| `large_motion_review` | `root_disp > 2.0` or `root_path > 5.0` or `xy_span > 2.0` |
| `stationary_motion_review` | stationary-like text and `root_disp > 0.8` or `root_path > 1.8` or `xy_span > 0.75` |

## 3. Cleaning Result

Clean cache:

```text
/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v7_5_clean_20260707/cache_mixed_full_clean_initial
```

| split | total | ignored | ignored % | review kept | review % | clean-cache kept |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| train | 94050 | 18368 | 19.53% | 16414 | 17.45% | 75682 |
| val | 10549 | 2150 | 20.38% | 1838 | 17.42% | 8399 |

The first stricter audit removed about 26-27%, which was judged too aggressive for this pass. The conservative pass still removes about 20%, so it should be treated as an initial hygiene filter, not a final dataset curation policy.

Current 12-sample audit decisions:

| decision | sample ids |
| --- | --- |
| keep | `2011_-4GsCEopbd4_00008_001_a`, `2011_-4GsCEopbd4_00017_000_a`, `2011_-EuO6OFypLo_00002_000_b`, `2011_-EuO6OFypLo_00020_000_a`, `2011_-RBjiJto4hc_00027_000_a`, `2011_-WW51YaWO-4_00007_000_a`, `2011_-WW51YaWO-4_00007_002_a` |
| review kept | `2011_-EuO6OFypLo_00002_000_a` |
| ignore | `2011_-MG8-wCvzpE_00002_000_a`, `2011_-MG8-wCvzpE_00002_001_a`, `2011_-UAElWXbk3I_00000_000_a`, `2011_-UAElWXbk3I_00000_001_a` |

## 4. Human Reconstruction Diagnosis

Scripts:

```text
linkedCodebases/StoryMotion/scripts/eval_stage1_human_tokenizer_posthoc.py
linkedCodebases/StoryMotion/scripts/eval_stage1_separate_tokenizers_posthoc.py
```

Eval subset: clean val ids from `cache_mixed_full_clean_initial/val.pt`, 8399 samples.

The old table of total loss / MSE / MPJFE / root MSE is intentionally removed from this note. Those values were useful for debugging reconstruction code, but they are not official StoryMotion / PulpMotion comparison metrics and can mislead readers into ranking tokenizers by a training-objective proxy.

Retained conclusion: the previous “VAE/VQVAE reconstruction is bad” impression must be split by tokenizer. Human VAE and separate GRFSQ were the stronger clean-val reconstruction candidates in the debug pass, while VQVAE / FSQ were weaker. This only says that some human tokenizers can reconstruct clean-val features; it does **not** prove that their decoded motion stays inside the TMR embedding manifold or that joint human-camera projection will be good.

## 4.1 Stage1 PulpMotion Data Audit

Code paths:

```text
/data/public/ripemangobox/Motion/StoryMotion/storymotion/training/joint_data.py
/data/public/ripemangobox/Motion/StoryMotion/storymotion/training/data.py
/data/public/ripemangobox/Motion/StoryMotion/scripts/train_storymotion_joint_tokenizer.py
```

Current behavior:

- `PairedPulpMotionHumanCameraDataset` loads one full human RIFKE sequence and one full camera trajectory by `sample_id`.
- If human and camera lengths disagree, both are truncated to the shared `min(length)`.
- `collate_human_camera_batch` zero-pads every batch to the batch maximum length and returns `lengths`.
- Stage1 train / posthoc eval uses `lengths` to build a frame mask; padding is excluded from reconstruction and velocity losses.
- `--seq-len` exists only for synthetic smoke data; real PulpMotion Stage1 has no `max_len`, `window`, `stride`, or `interval` slicing entrance.

Therefore the bad reconstruction / visual quality should **not** be attributed to unmasked padded frames. The real open question is whether full-sample variable length training is the right objective, not whether padding is contaminating the loss.

PulpMotion paired length distribution:

| split | paired | mean | p50 | p75 | p90 | p95 | max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| train | 36571 | 91.0 | 70 | 116 | 184 | 247 | 251 |
| test | 4053 | 92.1 | 71 | 117 | 188 | 249 | 251 |

50% overlap fixed-window simulation on train:

| window | stride | eligible samples | windows | windows / original |
| ---: | ---: | ---: | ---: | ---: |
| 96 | 48 | 12825 | 24148 | 0.66 |
| 128 | 64 | 7572 | 10910 | 0.30 |
| 160 | 80 | 4825 | 6813 | 0.19 |
| 192 | 96 | 3338 | 3338 | 0.09 |
| 196 | 98 | 3200 | 3200 | 0.09 |

Implication: directly replacing Stage1 training data with a fixed 192 / 196 frame sliding-window dataset is a bad default because it keeps only about 9% of samples. Even 96-frame windows discard about 65% of original clips and produce fewer training windows than the current sample count. If sliding windows are tested, the safer design is:

```text
keep all original full samples
+ add aligned human/camera overlap windows only for sufficiently long samples
+ run a short ablation before any full long train
```

## 4.2 Stage1 Joint / Separate Original-Mixed Full-Test Metrics

Script:

```text
linkedCodebases/StoryMotion/scripts/eval_stage1_joint_separate_tokenizers_posthoc.py
```

Remote metric artifacts:

```text
/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage1/v7_5_joint_separate_metrics_20260707
/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage1/official_recon_20260708
```

Eval set for StoryMotion retrained tokenizer rows: **original paired full / official pure** test, `4053` paired samples, `bs64`. The official metric eval reconstructs each sample at its real valid length, pads back to the official batch, then runs PulpMotion official callbacks. These are official metric readouts, not loss-selected claims. They are not clean-cache rows.

The official pretrained Pulp tokenizer rows are retained as upper-bound anchors. They are decoded by the official evaluator and should not be replaced by local self-retrain rows.

| experiment family | training data | topology / objective | official metric artifact | status |
| --- | --- | --- | --- | --- |
| official pretrained Pulp Stage1 AE | official original mixed tokenizer | official pretrained AE | existing official mixed/pure anchors | upper bound retained |
| self-trained Pulp Stage1 AE epoch325 | original Pulp mixed train | reconstructed local AE runner | `selftrained_pulp_ae_epoch325_pure4053_bs64.json` | useful negative reproduction |
| non-causal VAE original | original paired full | joint and separate VAE, original objective | `official_recon_20260708` | complete |
| human-stronger variants | original paired full | causal / non-causal ablations with branch reweighting | `official_recon_20260708` | historical evidence, not active visualization |
| v7.12 default separate tokenizers | original paired full `ae_train_split` | non-causal separate AE / VAE / GRFSQ, author default objective | `official_recon_20260709` | complete and active visualization |
| v7.13 default joint tokenizers | original paired full `ae_train_split` | non-causal joint AE / VAE / HFSQ, author default objective | `official_recon_20260709` | complete official eval |

Key official metric readouts:

| model | training data | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| official pretrained Pulp Stage1 AE | official original mixed tokenizer, pure eval | 109.34 | 15.94 | 92.4% | 17.66 | 60.53 | 84.5% | 0.776 | 3.5% |
| self-trained Pulp Stage1 AE epoch325 | original Pulp mixed train | 446.11 | 8.295 | 40.9% | 55.24 | 43.99 | 73.3% | 0.500 | 18.8% |
| joint VAE non-causal original | original paired full | 1250.40 | 8.443 | 0.7% | 110.66 | 45.89 | 65.7% | 0.533 | 20.4% |
| separate VAE non-causal original | original paired full | 1183.18 | 7.351 | 1.0% | 23.42 | 59.80 | 87.5% | 0.795 | 20.7% |
| separate AE v7.12 default | original paired full `ae_train_split` | 1239.97 | 8.044 | 1.0% | 22.90 | 61.03 | 83.4% | 0.930 | 20.8% |
| separate VAE v7.12 default | original paired full `ae_train_split` | 1219.41 | 9.223 | 1.1% | 15.14 | 63.57 | 89.8% | 0.928 | 20.8% |
| separate GRFSQ v7.12 default | original paired full `ae_train_split` | 1281.73 | 9.111 | 0.7% | 59.37 | 48.54 | 69.3% | 0.610 | 20.7% |
| joint AE v7.13 default | original paired full `ae_train_split` | 1190.17 | 8.096 | 0.9% | 33.57 | 58.55 | 80.3% | 0.852 | 20.8% |
| joint VAE v7.13 default | original paired full `ae_train_split` | 1232.87 | 8.736 | 0.8% | 44.00 | 54.64 | 75.7% | 0.775 | 20.5% |
| joint HFSQ v7.13 default | original paired full `ae_train_split` | 1467.24 | 10.852 | 0.3% | 116.20 | 36.19 | 51.4% | 0.447 | 20.8% |

Conclusion: the official metric problem is no longer a causal-GRFSQ-only issue. v7.12 improves camera-side metrics and F1 substantially, especially for separate VAE; v7.13 joint AE also recovers reasonable camera metrics. But all local retrained rows still leave FDTMR / HCov catastrophically worse than both official pretrained and the old self-trained AE. This is a human embedding / joint-coupling failure, not evidence that the pure loss table should be used for ranking.

## 4.3 Frame-Alignment Veto Check

DS Max flagged one missing one-vote-veto risk: human and camera could be frame-misaligned even if padding is masked correctly. Manifest rows have no timestamp fields; the current loader assumes same `sample_id` means frame-index alignment.

Direct projection audit on 32 conservative clean-val samples:

```text
decode GT human RIFKE -> 3D joints
project decoded joints through GT camera c2w + intrinsics
compare to dataset proj_joints visible pixels
```

Result:

| samples | visible xy MAE mean | visible xy MAE median | visible xy MAE p90 | visible fraction mean |
| ---: | ---: | ---: | ---: | ---: |
| 32 | 0.000074 px | 0.000067 px | 0.000130 px | 0.953 |

One sample had zero visible projected points, so its visible-pixel MAE is undefined. The rest are effectively exact. This strongly supports that the current decoded-human / camera / projection chain is frame-aligned. It does not explain the weak joint HFSQ / GRFSQ metrics.

## 4.4 Stage1 Loss Reweighting Patch and Retraining

Implementation patch:

```text
/data/public/ripemangobox/Motion/StoryMotion/storymotion/tokenizers/base.py
/data/public/ripemangobox/Motion/StoryMotion/storymotion/tokenizers/joint_human_camera.py
/data/public/ripemangobox/Motion/StoryMotion/scripts/train_storymotion_joint_tokenizer.py
/data/public/ripemangobox/Motion/StoryMotion/configs/stage1_loss/storymotion_stage1_human_stronger_v1.yaml
```

Design constraint: keep original PulpMotion Stage1 behavior when no YAML is provided. The old loss is still:

```text
human SmoothL1 recon
+ camera SmoothL1 recon
+ velocity_weight * (human velocity MSE + camera velocity MSE)
+ tokenizer regularizer
```

The new optional YAML adds branch-specific first-order and second-order temporal terms, inspired by ReactDance's reconstruction / velocity / acceleration split, without importing contact, relative-rotation, or bone-length terms whose semantics are not yet verified for StoryMotion's RIFKE + camera feature space.

Active v1 weights:

```yaml
stage1_loss:
  human_recon_weight: 2.0
  camera_recon_weight: 1.0
  human_velocity_weight: 1.0
  camera_velocity_weight: 0.25
  human_acceleration_weight: 0.25
  camera_acceleration_weight: 0.05
```

Masking answer for the current data loader:

- real Stage1 samples are full variable-length clips, not fixed max-length windows;
- batch padding is zero padding to the batch max length;
- `lengths` is used to mask reconstruction, velocity, acceleration, train validation, and posthoc metrics;
- therefore short clips are not trained as padded fake motion.

Rechecked train length distribution on `2026-07-07 16:00`:

| count | min | p10 | p25 | p50 | p75 | p90 | p95 | max |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 36571 | 9 | 37 | 46 | 70 | 116 | 184 | 247 | 251 |

Length proportions:

| condition | proportion |
| --- | ---: |
| `<64` frames | 44.56% |
| `<96` frames | 64.93% |
| `<128` frames | 79.30% |
| `<192` frames | 90.87% |
| `>=192` frames | 9.13% |

Training completed:

| machine / gpu | tokenizer | preset | data scope | run dir | status |
| --- | --- | --- | --- | --- | --- |
| 4090 gpu0 | pulp / AE | `pulpmotion_joint_ae_199_9_pulp192` | original-mixed | `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage1/v7_6_humanloss/joint_ae_pulp192_gpu0_20260707` | complete; best_top1 step `143000`; synced |
| 4090 gpu1 | VAE | `pulpmotion_joint_vae_199_9_pulp192` | original-mixed | `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage1/v7_6_humanloss/joint_vae_pulp192_gpu1_20260707` | complete; best_top1 step `143000`; synced |
| 5090 gpu0 | GRFSQ | `pulpmotion_joint_grfsq_199_9_pulp192` | original-mixed | `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage1/v7_6_humanloss/joint_grfsq_pulp192_gpu0_20260707` | complete; best_top1 step `142000`; synced |
| 5090 gpu3 | HFSQ | `pulpmotion_joint_hfsq_199_9_pulp192` | original-mixed | `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage1/v7_6_humanloss/joint_hfsq_pulp192_gpu3_20260707` | complete; best_top1 step `142000`; synced |

Environment notes:

- 4090 training env: `/home/ripemangobox/miniconda3/envs/director/bin/python`.
- 5090 training env: `/home/ripemangobox/miniconda3/envs/storymotion-director-cu128/bin/python`.
- 5090 initially missed the PulpMotion manifest JSONL files; they were synced from 4090 before restarting GRFSQ / HFSQ.

## 5. Clean Fine-Tune

Run:

```text
/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v7_5_clean_20260707/human_text_clean_ft10k_from_v74_final
```

Training setup:

- resume from v7.4 `human_text_full_e3like_82688_gate_snapshots/final_last/last.pt`
- clean cache: `cache_mixed_full_clean_initial`
- task: `human_text` only, `--task-probs 0 0 0 1`
- target: step `92688`, i.e. +10000 from step `82688`

Checkpoint status:

| checkpoint | official clean-val eval | FTD | coverage | TMR score | decision |
| --- | --- | ---: | ---: | ---: | --- |
| v7.4 final baseline | 1024 samples, 50 steps | 370.06 | 0.263 | 18.35 | clean validation reference |
| v7.5 clean fine-tune step85000 | 1024 samples, 50 steps | 381.47 | 0.235 | 21.39 | mixed: score improves, FTD / coverage worsen |
| v7.5 clean fine-tune final step92688 | 1024 samples, 50 steps | 463.14 | 0.205 | 20.36 | rejected as clean-data repair |

Interpretation: clean-data fine-tuning is not a distribution-quality win. It improves score-like retrieval alignment over the v7.4 clean baseline, but worsens FTD from `370.06` to `463.14` and coverage from `0.263` to `0.205`. Step85000 already showed the same direction in weaker form: FTD `381.47`, coverage `0.235`, TMR score `21.39`. The final checkpoint worsens further in FTD / coverage.

## 6. Current Working Decision

The final step92688 repeats and amplifies the step85000 warning pattern. The next step should be a larger methodological change, not another same-architecture clean fine-tune:

- keep the clean ignore list for future fair visual audits and training hygiene;
- do not claim clean data solves the core StoryMotion problem;
- use human VAE or separate GRFSQ as valid reconstruction backbones when needed;
- prioritize improving `P(H | human_text)` generation quality and the v7.4 human-first causal path, rather than treating VQVAE/FSQ reconstruction as the bottleneck.

Stage1-specific decision after the joint/separate metric audit:

- do not launch full fixed-window Stage1 long training yet;
- do not use 192 / 196 frame windows as a default because current PulpMotion Stage1 clips are mostly shorter;
- if a data-objective ablation is needed, test `full samples + long-sample overlap windows` first, preferably starting from VAE and GRFSQ because they bracket the current metric behavior;
- separate non-causal VAE, historical branch-reweighted variants, v7.12 default separate tokenizers, and v7.13 default joint tokenizers have now been trained / evaluated; the remaining open question is why visually plausible human recon remains badly scored by TMR-family metrics.

Estimated task durations under current infrastructure:

| task | expected time | note |
| --- | ---: | --- |
| Stage1 data handling audit | done, about 20 min | code path + length distribution + window simulation |
| full-test metric eval for 4 existing checkpoints | done, under 5 min on 4090 | joint VAE / GRFSQ / HFSQ and separate GRFSQ no-z |
| branch-reweighted tokenizer official eval | done, bs64 | retained as historical evidence |
| non-causal VAE official eval | done, bs64 | joint and separate VAE rows |
| v7.13 joint default official eval | done, bs64 | joint AE / VAE / HFSQ rows |
| Stage1 big-title recon visualization | done | active viewer now exposes original/default groups only |
| Gradio Stage1 tab sync/restart | done | 5090 service returned HTTP 200 after restart |
| implement full-sample + overlap-window dataset option | 1-2 h | should be gated by visual audit, not started blindly |
| short Stage1 window ablation | 1-3 h per model estimate | depends on selected window policy and epoch budget |
| full Stage1 long train | multi-hour per model | not justified until visual audit and short ablation support it |

## 8. DS Max Review

DS session: `6f71327f2391`.

DS Max verdict:

- The direction is reasonable, but the claim must be bounded.
- v7.5 only rejects a **short human_text-only clean fine-tune** as a core repair.
- It does not conclusively prove that data cleaning is useless, because no full same-architecture JOINT clean retrain was run.
- Under current constraints, full same-architecture JOINT clean fine-tune is lower priority than human-first / branch-separated architecture. If run later, it should be labeled as a control, not the main method.

Recommended wording:

> The clean human_text-only fine-tune improved alignment-like scores but degraded distributional quality. This does not conclusively reject data cleaning as a useful component, because the test was limited to one branch and short continuation training. However, given the v7.4 causal asymmetry hypothesis and practical constraints, v7.5 prioritizes architectural interventions over further same-architecture clean training. The clean cache is retained as hygiene, but cleaning alone is not treated as a sufficient repair. Any future full-JOINT clean fine-tune is a control, not a primary experiment.

Next action ranking:

| rank | action | role |
| ---: | --- | --- |
| 1 | design and test branch-separated / human-first architecture | primary next experiment |
| 2 | optional short full-JOINT clean fine-tune | control only, if GPU idle and explicitly approved |
| 3 | more human-only clean fine-tunes or VQVAE/FSQ debugging | deprioritized |

Second DS Max review for Stage1 data/window diagnosis:

```text
session_id: 1fcdf7f328c6
```

Verdict:

- The padding/mask and fixed-window conclusions are sound.
- The biggest missing one-vote-veto check was frame alignment between human and camera.
- After the 32-sample GT projection audit, frame alignment is no longer the leading explanation.
- Recommended priority remains: visual metric consistency first, then only a small data-objective ablation if needed.

## 7. Visual Audit Artifacts

Rendered samples: 8 clean kept / review-kept samples from the v7.4 manual audit set.

| render | data scope | path | samples | mp4 count | status |
| --- | --- | --- | ---: | ---: | --- |
| v7.4 final human_text | clean-mixed audit sample set | `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/v7_5_clean_audit_20260707/v74_final_human_text/std_cfg1.0_eta0.0` | 8 | - | done |
| v7.5 clean-final human_text | clean-mixed audit sample set | `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/v7_5_clean_audit_20260707/v75_clean_final_human_text/std_cfg1.0_eta0.0` | 8 | - | done |
| Stage1 causal original recon, big title | original-mixed | `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/v7_5_stage1_joint_separate_bigtitle_20260707` | 8 | 144 | done, synced to 4090 / 5090 Gradio |
| Stage1 non-causal VAE recon, big title | original paired full | `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/v7_7_stage1_noncausal_vae_bigtitle_20260707` | 8 | 144 | done, synced to 4090 / 5090 Gradio |
| Stage1 v7.12 non-causal default ae_train_split | original paired full `ae_train_split` | `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/v7_12_correct_fast_stage1_bigtitle_20260709` | 8 | 120 | active synced-row group |
| Stage1 Pulp AE official vs self-trained | official pretrained Pulp AE + local self-trained Pulp mixed epoch325 | `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/v7_13_pulp_ae_official_selftrained_stage1_bigtitle_20260709` | 8 | 96 | active synced-row group for last-frame distortion audit |

Stage1 Reconstruction concat layout:

```text
one row per concat video group:
causal original default
non-causal VAE original
```

For each sample, the tab exposes:

- `fixed_camera.mp4`
- `orbiting_camera.mp4`
- `camera_trajectory.mp4`

On `2026-07-07 15:59`, the Gradio script was updated again because the first Stage1 tab only exposed the three concat videos and did not let users inspect `vae` / `grfsq` / `hfsq` separately. On `2026-07-09`, the active Gradio view was narrowed to original/default visual groups, the v7.12 synced-row group was added, and the Pulp AE official-vs-self-trained synced-row group was added. The current tab keeps the concat videos and adds per-model subtabs:

```text
GT
joint VAE
joint GRFSQ
joint HFSQ
separate GRFSQ no-z
non-causal joint VAE original
non-causal separate VAE original
```

Stage1 rendered sample ids:

```text
2015_iL1JlXnbnt0_00000_000_a
2019_vcdDRblTOmM_00038_001_a
2016_4wPqQUl2y5A_00000_000_b
2012_FZ1f-u8RqBU_00008_000_a
2011_kk2HQ0hCGTE_00006_000_a
2016_4MTf0k1vqTk_00016_000_a
2012_OsJKdxPwZdk_00043_000_a
2011_d-kcczAff40_00007_000_a
```

Gradio:

```text
ssh -L 7863:127.0.0.1:7862 5090
http://127.0.0.1:7863
```

Runtime script:

```text
/tmp/v75_paired_audit_gradio.py
```

The Gradio app keeps the v7.4 paired audit tabs, adds `v7.5 Clean HumanText`, and now adds `Stage1 Reconstruction`. The active Stage1 groups are `Pulp AE official vs self-trained`, `causal original`, `non-causal VAE original`, and `non-causal default ae_train_split`; branch-reweighted visual groups are not exposed in the current viewer.

Pending before final close:

- Human visual audit of the Stage1 tab.

## 8. 2026-07-07 Stage1 Original-Mixed Completion Record

### 8.1 Human-Stronger Joint Tokenizers

All human-stronger rows are original paired full Stage1 tokenizer experiments, not clean-mixed cache experiments. They use the unfiltered PulpMotion paired train/test manifests and are therefore fair against §4.2 original paired tokenizer rows.

Run status:

| tokenizer | loss setting | data scope | run dir | checkpoint | sync status |
| --- | --- | --- | --- | --- | --- |
| joint AE | human stronger v1 | original-mixed | `runs/train/stage1/v7_6_humanloss/joint_ae_pulp192_gpu0_20260707` | best_top1 step `143000` | 4090 / 5090 synced |
| joint VAE | human stronger v1 | original-mixed | `runs/train/stage1/v7_6_humanloss/joint_vae_pulp192_gpu1_20260707` | best_top1 step `143000` | 4090 / 5090 synced |
| joint GRFSQ | human stronger v1 | original-mixed | `runs/train/stage1/v7_6_humanloss/joint_grfsq_pulp192_gpu0_20260707` | best_top1 step `142000` | 4090 / 5090 synced |
| joint HFSQ | human stronger v1 | original-mixed | `runs/train/stage1/v7_6_humanloss/joint_hfsq_pulp192_gpu3_20260707` | best_top1 step `142000` | 4090 / 5090 synced |

Posthoc metrics:

```text
runs/eval/stage1/official_recon_20260708
```

| model | bs | samples | official metric status | output |
| --- | ---: | ---: | --- | --- |
| joint AE human stronger v1 | 64 | 4053 | complete | `joint_ae_human_stronger_pure4053_bs64.json` |
| joint VAE human stronger v1 | 64 | 4053 | complete | `joint_vae_human_stronger_pure4053_bs64.json` |
| joint GRFSQ human stronger v1 | 64 | 4053 | complete | `joint_grfsq_human_stronger_pure4053_bs64.json` |
| joint HFSQ human stronger v1 | 64 | 4053 | complete | `joint_hfsq_human_stronger_pure4053_bs64.json` |

Visualization:

```text
runs/visualizations/v7_6_stage1_humanloss_joint_bigtitle_20260707
```

Result: 8 samples, 144 mp4 files, `summary.json` written and synced to 4090 / 5090. This render is historical evidence and is not exposed in the current Gradio viewer.

### 8.2 Non-Causal VAE Ablation

Code updates:

- Added `is_causal` tokenizer construction control.
- YAML accepts both `is_causal` and the typo-compatible alias `is_casual`; internal field is `is_causal`.
- Default construction remains causal unless explicitly set otherwise.
- Non-causal configs:
  - `configs/stage1_loss/storymotion_stage1_noncausal_original_default.yaml`
  - `configs/stage1_loss/storymotion_stage1_noncausal_human_stronger_v1.yaml`
- Stage1 eval/render loaders read `run_config.json` so non-causal checkpoints are rebuilt with `is_causal: false`.

Run status:

| machine / gpu | tokenizer | loss | data scope | run dir | checkpoint / eval |
| --- | --- | --- | --- | --- | --- |
| 4090 gpu1 | joint VAE | original default, non-causal | original paired full | `runs/train/stage1/v7_7_noncausal_vae/joint_vae_original_gpu0_20260707` | best_top1 step `143000`; official eval complete |
| 4090 gpu0 | joint VAE | human stronger v1, non-causal | original paired full | `runs/train/stage1/v7_7_noncausal_vae/joint_vae_humanloss_gpu1_20260707` | best_top1 step `143000`; official eval complete |
| 4090 gpu1 | separate VAE | original default, non-causal | original paired full | `runs/train/stage1/v7_7_noncausal_vae/separate_vae_original_gpu0_20260707` | best_top1 step `143000`; official eval complete |
| 5090 gpu3 | separate VAE | human stronger v1, non-causal | original paired full | `runs/train/stage1/v7_7_noncausal_vae/separate_vae_humanloss_gpu3_20260707` | best_top1 step `143000`; official eval complete |

Official metric eval:

```text
runs/eval/stage1/official_recon_20260708
```

| model | bs | samples | official metric status | output |
| --- | ---: | ---: | --- | --- |
| joint VAE non-causal original | 64 | 4053 | complete | `joint_vae_noncausal_original_pure4053_bs64.json` |
| joint VAE non-causal human stronger v1 | 64 | 4053 | complete | `joint_vae_noncausal_human_stronger_pure4053_bs64.json` |
| separate VAE non-causal original | 64 | 4053 | complete | `separate_vae_noncausal_original_pure4053_bs64.json` |
| separate VAE non-causal human stronger v1 | 64 | 4053 | complete | `separate_vae_noncausal_human_stronger_pure4053_bs64.json` |

Completed official joint metrics:

| model | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| joint VAE non-causal original | 1250.40 | 8.443 | 0.7% | 110.66 | 45.89 | 65.7% | 0.533 | 20.4% |
| joint VAE non-causal human stronger v1 | 1281.96 | 8.685 | 0.9% | 149.72 | 40.55 | 55.9% | 0.497 | 20.2% |
| separate VAE non-causal original | 1183.18 | 7.351 | 1.0% | 23.42 | 59.80 | 87.5% | 0.795 | 20.7% |
| separate VAE non-causal human stronger v1 | 1211.04 | 8.414 | 0.9% | 27.46 | 58.69 | 87.2% | 0.795 | 20.7% |

Evaluation batch-size note:

- 4090 joint eval was attempted and completed at `bs64`; no bs48 fallback was needed.
- 5090 gpu0 ran the two separate VAE evals at `bs64`.
- Retrieval / embedding-backed metrics such as TMR can be batch-sensitive; official metric eval remains `bs64` unless OOM.

Visualization:

```text
runs/visualizations/v7_7_stage1_noncausal_vae_bigtitle_20260707
```

Result: 8 samples, 144 mp4 files, `summary.json` written and synced to 4090 / 5090. The current Gradio viewer exposes the original rows from this render only.

### 8.3 Non-Causal GRFSQ / HFSQ Human-Stronger Ablation

Run status:

| machine / gpu | tokenizer | loss | data scope | run dir | checkpoint / eval |
| --- | --- | --- | --- | --- | --- |
| 4090 gpu0 | joint GRFSQ | human stronger v1, non-causal | original paired full | `runs/train/stage1/v7_8_noncausal_fsq_humanloss/joint_grfsq_gpu0_20260708` | best_top1; official eval complete |
| 4090 gpu1 | joint HFSQ | human stronger v1, non-causal | original paired full | `runs/train/stage1/v7_8_noncausal_fsq_humanloss/joint_hfsq_gpu1_20260708` | best_top1; official eval complete |
| 4090 gpu0 | separate GRFSQ | human stronger v1, non-causal | original paired full | `runs/train/stage1/v7_8_noncausal_fsq_humanloss/separate_grfsq_gpu0_20260708` | best_top1; official eval complete |
| 4090 gpu1 | separate HFSQ | human stronger v1, non-causal | original paired full | `runs/train/stage1/v7_8_noncausal_fsq_humanloss/separate_hfsq_gpu1_20260708` | best_top1; official eval complete |

Official metric eval:

| model | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| joint GRFSQ non-causal human stronger v1 | 1301.26 | 8.743 | 0.6% | 159.97 | 29.80 | 45.4% | 0.343 | 20.5% |
| joint HFSQ non-causal human stronger v1 | 1385.16 | 7.051 | 0.1% | 116.82 | 30.73 | 44.0% | 0.327 | 11.8% |
| separate GRFSQ non-causal human stronger v1 | 1269.24 | 7.054 | 0.7% | 188.71 | 32.90 | 45.9% | 0.391 | 19.7% |
| separate HFSQ non-causal human stronger v1 | 1366.50 | 7.778 | 0.2% | 83.04 | 41.54 | 62.9% | 0.448 | 19.3% |

Interpretation: separate branches do not fix the human TMR-family collapse. Camera-side metrics improve for separate HFSQ relative to joint HFSQ, but GRFSQ worsens on FDCLaTr. This makes “camera branch alone causes the metric collapse” unlikely; the remaining conflict is between visually plausible human reconstruction and the TMR embedding metrics.

Visualization:

```text
runs/visualizations/v7_8_stage1_noncausal_fsq_humanloss_bigtitle_20260708
```

Result: 8 samples, 144 mp4 files, `summary.json` written. This render is retained as historical evidence and is not exposed in the current Gradio viewer.

### 8.4 Gradio State After Stage1 Recon Update

Gradio recon fix:

- The Stage1 Reconstruction tab has its own `Recon sample` dropdown, so recon data no longer depends on the v7.5 clean audit sample list.
- The concat tab is grouped as one concat video per row:
  - causal original default, trained on original paired full;
  - non-causal VAE original, trained on original paired full.
- The metadata table now labels training data and expands `default velocity`:
  - causal original default: human/camera recon `1.0`; velocity preset is AE/VAE `1.0`, GRFSQ/HFSQ `0.5`; acceleration `0`.
  - non-causal VAE original: human/camera recon `1.0`; velocity `1.0`; acceleration `0`.
  - v7.12 non-causal default `ae_train_split`: human/camera recon `1.0`; velocity preset is AE/VAE `1.0`, GRFSQ `0.5`; acceleration `0`.
- Per-model subtabs include causal original and non-causal VAE original rows only.
- The synced-row viewer includes `causal original`, `non-causal VAE original`, and `non-causal default ae_train_split`. The v7.12 group shows GT plus separate AE / VAE / GRFSQ under one shared progress bar without physically concatenating mp4 files.
- Branch-reweighted visual groups are intentionally hidden from the active viewer; their run artifacts remain historical evidence only.
- 5090 Gradio returned HTTP 200 after the latest restart on `2026-07-09`; active script is `/tmp/v75_paired_audit_gradio.py`.

### 8.5 v7.12 Correct Fast Non-Causal Default Ablation

This run answers the follow-up question about using the author-style default Stage1 loss rather than the human-stronger loss. All three rows below are non-causal and use the original default objective on the ae_train_split paired data.

Run status:

| machine / gpu | tokenizer | loss | data scope | run dir | checkpoint / eval |
| --- | --- | --- | --- | --- | --- |
| 4090 gpu0 | separate AE | original default, non-causal | original paired full ae_train_split | `runs/train/stage1/v7_12_correct_fast_ae_train_split_20260708/separate_ae_4090_gpu0` | last checkpoint; official eval complete |
| 4090 gpu1 | separate VAE | original default, non-causal | original paired full ae_train_split | `runs/train/stage1/v7_12_correct_fast_ae_train_split_20260708/separate_vae_4090_gpu1` | last checkpoint; official eval complete |
| 5090 gpu0 | separate GRFSQ | original default, non-causal | original paired full ae_train_split | `runs/train/stage1/v7_12_correct_fast_ae_train_split_20260708/separate_grfsq_5090_gpu0` | last checkpoint; official eval complete |

Official metric eval:

```text
runs/eval/stage1/official_recon_20260709
```

| model | training data | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| separate AE v7.12 non-causal default | original paired full `ae_train_split` | 1239.97 | 8.044 | 1.0% | 22.90 | 61.03 | 83.4% | 0.930 | 20.8% |
| separate VAE v7.12 non-causal default | original paired full `ae_train_split` | 1219.41 | 9.223 | 1.1% | 15.14 | 63.57 | 89.8% | 0.928 | 20.8% |
| separate GRFSQ v7.12 non-causal default | original paired full `ae_train_split` | 1281.73 | 9.111 | 0.7% | 59.37 | 48.54 | 69.3% | 0.610 | 20.7% |

Interpretation:

- v7.12 default-loss separate VAE is the strongest retrained tokenizer row so far by camera-side official metrics, with FDCLaTr `15.14`, CLaTr `63.57`, CCov `89.8%`, and F1 `0.928`.
- The same row is still catastrophically bad on human metrics: FDTMR `1219.41` and HCov `1.1%`, versus old self-trained AE `446.11` / `40.9%` and official pretrained pure `109.34` / `92.4%`.
- F1 improvement does not contradict FDTMR / HCov collapse because F1 is a camera/caption-side metric. A cleaner camera trajectory can be easier to classify even when decoded human motion lands outside the TMR real-motion manifold.
- Out staying near `20.8%` says the generated/reconstructed human-camera pair still fails projection containment. The likely failure is joint coupling: separate branches can reconstruct camera well in isolation while still producing a human trajectory / camera pair whose visibility and timing are wrong.
- TMR is significantly worse relative to official pretrained (`15.94` -> `8-9`). Relative to the old self-trained AE, v7.12 VAE/GRFSQ are only slightly higher on TMR, but the simultaneous FDTMR and HCov collapse means those scores should not be read as healthy recovery.
- The evidence points to a metric-contract or representation-distribution issue: root/global normalization, RIFKE decode dynamics, valid-length handling, decoder boundary artifacts, or TMR encoder preprocessing can all move human embeddings off-manifold without strongly hurting camera caption F1.

Most useful next ablation: run official metrics on paired branch swaps: `GT human + v7.12 camera`, `v7.12 human + GT camera`, and `official pretrained human + v7.12 camera`. This isolates whether Out and TMR-family collapse come from the human decoder, camera decoder, or their synchronization.

Visualization:

```text
runs/visualizations/v7_12_correct_fast_stage1_bigtitle_20260709
```

Result: 8 samples, 120 mp4 files, `summary.json` written, synced to 4090 / 5090, registered in Gradio synced-row group `non-causal default ae_train_split`.

### 8.6 v7.13 Joint Default AE / VAE / HFSQ Training

This run starts the joint versions requested after the v7.12 separate-branch audit. The setup intentionally keeps the v7.12 data and objective口径: non-causal temporal backbone, original default objective, original paired full `ae_train_split`, `bs128`, `epochs=500`, `lr=5e-5`, val on official pure paired manifests.

Run status:

| machine / gpu | tokenizer | loss | data scope | run dir | checkpoint / eval |
| --- | --- | --- | --- | --- | --- |
| 4090 gpu0 | joint AE | original default, non-causal | original paired full `ae_train_split` | `runs/train/stage1/v7_13_joint_default_ae_train_split_20260709/joint_ae_4090_gpu0` | complete; `last.pt`, best steps through `636000`; official eval complete |
| 4090 gpu1 | joint VAE | original default, non-causal | original paired full `ae_train_split` | `runs/train/stage1/v7_13_joint_default_ae_train_split_20260709/joint_vae_4090_gpu1` | complete; `last.pt`, best steps through `636000`; official eval complete |
| 5090 gpu0 | joint HFSQ | original default, non-causal | original paired full `ae_train_split` | `runs/train/stage1/v7_13_joint_default_ae_train_split_20260709/joint_hfsq_5090_gpu0` | complete; `last.pt`, best steps through `632000`; official eval complete |

Notes:

- AE / VAE presets use `pulpmotion_joint_ae_199_9_pulp192` and `pulpmotion_joint_vae_199_9_pulp192`; HFSQ uses `pulpmotion_joint_hfsq_199_9_pulp192`.
- All three runs use `configs/stage1_loss/storymotion_stage1_noncausal_original_default.yaml`, so `is_causal=false`, human/camera recon weights are `1.0`, acceleration weights are `0`, and HFSQ keeps `velocity_weight=0.5`.
- Official eval uses the completed `last.pt` checkpoints and the same full-pure `4053` official callback口径 as the v7.12 rows.

Official metric artifacts:

```text
/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage1/official_recon_20260709/joint_ae_v7_13_default_pure4053_bs64.json
/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage1/official_recon_20260709/joint_vae_v7_13_default_pure4053_bs64.json
/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage1/official_recon_20260709/joint_hfsq_v7_13_default_pure4053_bs64.json
```

Completed official joint metrics:

| model | training data | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| joint AE v7.13 non-causal default | original paired full `ae_train_split` | 1190.17 | 8.096 | 0.9% | 33.57 | 58.55 | 80.3% | 0.852 | 20.8% |
| joint VAE v7.13 non-causal default | original paired full `ae_train_split` | 1232.87 | 8.736 | 0.8% | 44.00 | 54.64 | 75.7% | 0.775 | 20.5% |
| joint HFSQ v7.13 non-causal default | original paired full `ae_train_split` | 1467.24 | 10.852 | 0.3% | 116.20 | 36.19 | 51.4% | 0.447 | 20.8% |

Interpretation:

- Joint AE is the best v7.13 joint default row by FDTMR and camera-side metrics, but it still has HCov `0.9%` and Out `20.8%`.
- Joint HFSQ gets the highest local TMR score (`10.852`) but has the worst FDTMR (`1467.24`) and weak camera metrics, so it is not a recovery.
- Switching from separate to joint default branches does not fix the core failure: human TMR-family coverage remains near zero and projection Out stays around `20%`.

Visualization:

```text
runs/visualizations/v7_13_joint_default_stage1_bigtitle_20260710
```

Result: 8 samples, 120 mp4 files, `summary.json` written on 5090, registered in Gradio synced-row group `non-causal joint default ae_train_split`. The group uses the same 8 pure sample ids as the v7.12 separate default visualization, so `GT | joint AE | joint VAE | joint HFSQ` can be compared directly against the v7.12 `GT | separate AE | separate VAE | separate GRFSQ` group.

## 8.1 Main A Human-First Launch

Decision after v7.13: do not treat Stage1 retrain as the blocking main line. The v7.12 / v7.13 tokenizer results are useful negative controls, but they do not provide a clean causal answer to joint-vs-separate because the local tokenizer recipe is not an author-exact Pulp Stage1 reproduction. Main A now freezes the Stage1 latent contract per tokenizer and tests explicit human-first Stage2 composition:

```text
H = P(H | human text)
C = P(C | H, camera text, source quality)
JOINT = concat(H, C)
```

Implementation updates on `2026-07-10`:

- 5090 and 4090 StoryMotion code surfaces were synchronized for the Main A scripts, `build_stage2_joint_tokenizer_latent_cache.py`, and `v75_paired_audit_gradio.py`.
- `build_stage2_joint_tokenizer_latent_cache.py` now supports `--sidecar-source direct`, because the old official mixed Stage2 cache has only `94050` train ids and does not cover the `162760` public-core ids in `ae_train_split`.
- Direct sidecar mode reads `caption_cam_clip/token` and `caption_char_clip/token`, concatenates them into the 1024-dim text condition, and derives the 75-frame latent valid mask from paired sequence lengths.
- Smoke cache builds passed for `v7.13 joint AE` and `v7.12 separate VAE`, both producing `z [N,192,75]`, `text [N,1024]`, and `valid [N,75]`.
- Stage2 training batch size is set to `512` for Main A, because official Pulp config uses `128` per GPU while prior StoryMotion Stage2 experiments commonly used `512`; cache construction still uses `128`.

Launched jobs:

| host / GPU | tokenizer label | current pipeline | output root / log |
| --- | --- | --- | --- |
| 4090 GPU0 | official Pulp AE | existing official cache -> `human_text` Stage2 bs512 -> H2C `mixed-p2b` bs512 | `runs/train/stage2/v7_13_mainA_20260710/official_ae_*_bs512_4090_gpu0`; `/tmp/v7_13_mainA_official_ae_4090_gpu0_bs512.log` |
| 4090 GPU1 | v7.13 joint AE default | direct cache build -> `human_text` Stage2 bs512 -> H2C `mixed-p2b` bs512 | `runs/train/stage2/v7_13_mainA_20260710/v7_13_joint_ae_*_bs512_4090_gpu1`; `/tmp/v7_13_mainA_joint_ae_4090_gpu1_bs512.log` |
| 5090 GPU0 | v7.12 separate VAE default | direct cache build -> `human_text` Stage2 bs512 -> H2C `mixed-p2b` bs512 | `runs/train/stage2/v7_13_mainA_20260710/v7_12_separate_vae_*_bs512_5090_gpu0`; `/tmp/v7_13_mainA_separate_vae_5090_gpu0_bs512.log` |

### 8.1.1 Main A 4090 Eval and Visualization Verdict

Both 4090 pipelines completed `human_text` and H2C training. Official-callback eval and the 8-sample visualization audit completed on `2026-07-10`. The official Pulp AE branch uses official `mixed_` test with `10549` samples; the locally trained v7.13 joint AE cache matches `pure_` test with `4053` samples. The two tokenizer rows therefore diagnose transfer health but are not a strict architecture ranking against each other.

Eval artifacts:

```text
/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v7_13_mainA_20260710/official_ae_human_text_mixed_full_last.json
/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v7_13_mainA_20260710/official_ae_joint_composed_mixed_full_last.json
/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v7_13_mainA_20260710/v7_13_joint_ae_human_text_pure4053_last.json
/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v7_13_mainA_20260710/v7_13_joint_ae_joint_composed_pure4053_last.json
```

| Stage1 contract / eval split | task | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| official Pulp AE / `mixed_` | human text | 10549 | 529.61 | 17.55 | 4.8% | - | - | - | - | - |
| official Pulp AE / `mixed_` | composed joint | 10549 | 532.49 | 17.71 | 4.8% | 524.13 | 8.61 | 9.8% | 0.103 | 37.1% |
| v7.13 local joint AE / `pure_` | human text | 4053 | 2245.14 | 0.00 | 0.0% | - | - | - | - | - |
| v7.13 local joint AE / `pure_` | composed joint | 4053 | 2245.15 | 0.00 | 0.0% | 655.76 | 7.26 | 0.4% | 0.031 | 99.4% |

The final official-AE composed eval initially OOMed during SMPL decode. Adding decode-only micro-batching and rerunning with sampling batch `32` and decode batch `8` completed all `10549` samples without changing the sampling path.

Visualization artifacts:

```text
/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v7_13_mainA_20260710/renders_official_ae_mixed_last/std_cfg2.0_eta0.0
/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v7_13_mainA_20260710/renders_v7_13_joint_ae_pure4053_last/std_cfg2.0_eta0.0
```

Each directory contains 8 shared sample ids, both `human_text` and composed `joint` tasks, PNG trajectory summaries, skeleton MP4s, concatenated MP4s, and `render_summary.json` (`57` files per directory). The renderer completed with `ok: true`. Visual inspection agrees with the official metrics: predicted human-root and camera trajectories are displaced from GT, and the local joint-AE branch shows the more extreme failure. Visualization is complete, but the quality gate fails.

#### Architecture verdict

The current evidence does **not** show an advantage for asymmetric Main A over the symmetric unified Stage2. On the same official Pulp AE latent contract and `mixed_` full evaluator, the earlier symmetric unified joint anchor recorded in [[ideas/StoryMotion/archived/v6/2026-06-25_storymotion-v6.1|StoryMotion v6.1]] is substantially better:

| architecture | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | Out↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| symmetric unified joint anchor | 155.73 | 23.95 | 36.4% | 85.70 | 33.5 | 62.8% | 7.89% |
| asymmetric Main A, official AE composed joint | 532.49 | 17.71 | 4.8% | 524.13 | 8.61 | 9.8% | 37.1% |

This is strong negative directional evidence, not yet a clean causal rejection of asymmetry: the historical symmetric checkpoint and Main A do not have a fully matched seed, optimization budget, and parameter allocation. What is already rejected is the present implementation recipe—independent `P(H | human text)` followed by H2C trained with `mixed-p2b` and evaluated on generated H. It does not preserve the symmetric baseline's human distribution, camera distribution, or framing.

#### Next three core experiments, in priority order

| priority | experiment | causal question | success / kill criterion |
| ---: | --- | --- | --- |
| 1 | matched-contract symmetric vs asymmetric A/B | Does factorization itself help when Stage1, train ids, seed, steps, sampler, parameter budget, and evaluator are held fixed? | Asymmetric must improve FDTMR, FDCLaTr, and Out without losing TMR / coverage; otherwise stop claiming architectural advantage. |
| 2 | H-source oracle ladder for the frozen H2C | Is the composed failure caused mainly by H generation or by H2C sensitivity? Evaluate the same H2C checkpoint with GT H, official-AE reconstructed H, current generated H, and shuffled H on identical sample ids. | If GT / reconstructed H works but generated H fails, prioritize source-shift robustness; if all fail, replace the H2C objective / backbone before more joint training. |
| 3 | true generated-H replay adaptation | Does exposure to the actual frozen human generator distribution repair the cascade? Build offline generated-H latents for training ids, fine-tune H2C with explicit clean / generated source labels, and compare against current synthetic `mixed-p2b` at matched budget. | Continue only if generated-H JOINT improves materially while clean-H camera completion regresses less than 10%. |

Priority 1 supplies the missing architecture-only answer. Priority 2 is the fastest root-cause experiment. Priority 3 is the smallest targeted repair justified only if Priority 2 identifies generated-H covariate shift.

Naming note: no distinct `v7.13 separate VAE` checkpoint was found on disk. The launched separate-VAE control uses the latest default separate VAE available under `v7_12_correct_fast_ae_train_split_20260708`.

### 8.1.2 Stage1 / Stage2 Feature-Contract Correction

Verdict: v7.13 local AE / VAE / GRFSQ Stage1 used raw RIFKE human199 plus absolute-pose camera9, while official PulpMotion uses normalized human199 plus FOV2, normalized human-relative distance3, rotation6d, and normalized camera velocity3. The mismatch affects Stage1 weights and every Stage2 cache built from them. A separate eval adapter also unnormalized raw human reconstruction twice; therefore prior local-tokenizer human / Out official rows are invalid. Official-pretrained Stage2 rows are unaffected.

Implemented and verified:

- new Stage1 presets use the exact official normalized `199+14` contract; one pure-test sample matches official `dataset.get_feat` with max error `0` for both branches;
- Stage1 official eval now decodes normalized `199+14` jointly, while legacy raw199 checkpoints are normalized exactly once before SMPL decode;
- Stage2 cache build requires an explicit feature contract and rejects mismatched checkpoints; source-tokenizer Stage2 eval uses the matching official joint decoder;
- real-batch AE forward / backward passed on `[2,85,199] + [2,85,14]`.

The first AE / VAE launch did not complete training: both exited during validation before writing a checkpoint because one sample had human length `157` and camera / intrinsics length `130`, and the official relative-distance feature was computed before common-timeline truncation. Process exit was therefore not experiment completion.

The loader now truncates raw human, camera pose, and intrinsics to their common valid length before constructing normalized `199+14` features. Verification covers all `4053` pure-test samples plus `1628` evenly sampled train rows; the original failing sample matches official features with max error `0` after truncation.

Corrected retraining started on free 4090 GPUs. The initial `_r1` throughput was only about `6.3 step/s` with 8 workers and would require about 28 hours, so it was stopped at about 0.35% progress. The effective `_r2` runs use 24 workers per GPU:

```text
runs/train/stage1/v7_14_official_contract_20260710/joint_ae_official_4090_gpu0_r2
runs/train/stage1/v7_14_official_contract_20260710/joint_vae_official_4090_gpu1_r2
```

Both `_r2` runs completed epoch `500`, step `636000`. Final best validation loss is `0.01553` for AE and `0.01482` for VAE. Corrected official pure-4053 eval completed with the official camera14 joint decoder:

| model | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| official pretrained Pulp AE | 109.34 | 15.94 | 92.4% | 17.66 | 60.53 | 84.5% | 0.776 | 3.5% |
| v7.14 corrected joint AE | **31.10** | 14.99 | **97.9%** | **0.48** | **69.46** | **99.5%** | **0.927** | 5.1% |
| v7.14 corrected joint VAE | 69.61 | 13.77 | 93.1% | 2.28 | 68.45 | 97.7% | 0.914 | 7.9% |

The corrected AE is the active local Stage1 choice. It beats the official pretrained anchor on FDTMR, human coverage, and all reported camera metrics, while remaining slightly worse on TMR and Out. VAE is healthy after contract correction but is consistently behind AE; the earlier near-zero human coverage was caused by the feature/eval contract errors, not by joint AE/VAE topology alone.

```text
runs/eval/stage1/v7_14_official_contract_20260710/joint_ae_pure4053.json
runs/eval/stage1/v7_14_official_contract_20260710/joint_vae_pure4053.json
runs/visualizations/v7_14_official_contract_stage1_20260710
```

Visualization completed on the same eight v7.13 audit ids with layout `GT | v7.14 AE | v7.14 VAE`: `96` MP4 and `24` NPZ files, with `0` invalid MP4. Across these samples, mean root-XY global reconstruction error is `0.171` for AE and `0.365` for VAE, supporting the full-eval AE preference.

## 9. GRFSQ / HFSQ Temporal Implementation Answer

GRFSQ / HFSQ do use temporal modeling in the StoryMotion tokenizer backbone, but not inside the scalar quantizer itself.

Implementation facts:

- `JointHumanCameraGRFSQVAE`, `JointHumanCameraHFSQVAE`, `SeparateHumanCameraGRFSQVAE`, and `SeparateHumanCameraHFSQVAE` inherit encoder/decoder structure from `_JointHumanCameraAE`.
- `_make_encoder` uses temporal `Conv1d` blocks with stride `downsample=4`.
- `_make_decoder` uses `ConvTranspose1d` upsampling followed by temporal `Conv1d`.
- `is_causal=True` defaults to left-padded `CausalConv1d`; `is_causal=False` uses symmetric padding.
- `GroupedResidualFSQ` / `HierarchicalFSQ` quantize each downsampled temporal latent position over grouped feature dimensions. They are not temporal attention / transformer modules.
- The current ledger now includes both causal GRFSQ/HFSQ and non-causal GRFSQ/HFSQ human-stronger rows; non-causal separate branches did not recover the human TMR-family metrics.

## 10. Last-Frame Recon Distortion Diagnosis

Last-frame recon distortion diagnosis:

- The distortion is already present in saved `rifke_joints.npz`, before Gradio or mp4 playback.
- GT videos do not show comparable final-frame shape changes.
- Single-sample recon rendering does not batch-pad and does not use the training mask, so the observed final-frame artifact is not caused by batch padding mask mechanics.
- The issue is most consistent with tokenizer decoder boundary behavior / sequence-end handling. The current decoder uses temporal convs and transposed-conv upsampling, then truncates to `target_len`; the final frame has boundary context that differs from interior frames.
- Length modulo `downsample` is not the sole trigger: bad final jumps appear even when frame count is divisible by 4.
- Practical next diagnostic: compare final-frame error before and after a decoder-end handling change, or evaluate/report metrics with an optional last-frame exclusion diagnostic to quantify the boundary contribution.
