---
title: "StoryMotion v7.14 Corrected Results"
status: active
hypothesis: |
  StoryMotion 的正式证据必须建立在一致的 PulpMotion feature、decode、split 与 official callback 契约上；受旧 local Stage1 错误影响的指标全部退出路线判断。
tags:
  - StoryMotion
  - Motion_Generation
  - metric
  - evidence
  - status/active
aliases:
  - StoryMotion-v7.14-Corrected-Results
source_notes:
  - "[[2026-07-09_storymotion-v7.12-metric-data]]"
  - "[[2026-07-03_storymotion-v7.3.1]]"
  - "[[2026-07-01_storymotion-v6.2-metric-data]]"
created: 2026-07-11T11:33:00+0800
updated: 2026-07-17T00:14:00+0800
---

# StoryMotion v7.14 Corrected Results

> [!abstract] 当前裁决
> 旧 local Stage1 使用 raw human199 + absolute camera9，且 official-eval adapter 对 human reconstruction 重复反归一化。由此得到的 v7.5–v7.13 local-tokenizer Stage1 指标及其衍生 Stage2 cache 结果不再用于路线判断。当前有效证据由 GT / official pretrained Pulp anchors、v7.14 corrected Stage1，以及基于 official pretrained Pulp cache 的 Stage2 实验组成。

## 1. Evidence Boundary

### 1.1 Excluded

- 所有使用 `pulpmotion_joint_*_199_9*` 或 separate `199_9` local checkpoint 的 Stage1 official metric。
- 所有由上述 checkpoint 构建 latent cache 后训练或评估的 Stage2 结果。
- 典型排除项：v7.12 separate AE/VAE/GRFSQ、v7.13 joint AE/VAE/HFSQ、Main A local joint-AE branch。
- 旧结果可保留为工程历史，但不能支持 joint-vs-separate、AE-vs-VAE 或 Stage2 architecture 结论。

### 1.2 Retained

- GT identity 与 official pretrained Pulp Stage1 anchors。
- v7.14 corrected joint AE/VAE：normalized human199 + official joint camera14，官方 joint decoder。
- 使用 official pretrained Pulp Stage1 cache 的 Stage2 full eval，包括 v6 clean unified、e2/e3、v7.13 matched symmetric、Main A official-AE cascade、oracle ladder 与 generated replay adaptation。
- 不同 split、训练预算或参数量的保留结果只能作方向证据；只有 matched A/B 才能作架构因果结论。

## 2. Data and Contract

| scope | samples | use | contract |
| --- | ---: | --- | --- |
| `ae_train_split` train | 162760 | v7.14 Stage1 train | normalized human199 + camera14 |
| official `pure_` test | 4053 | corrected Stage1 full eval | exact paired ids + official callbacks |
| official `mixed_` test | 10549 | retained Stage2 full eval | official pretrained Pulp cache |

Camera14 is `FOV2 + normalized camera-human distance3 + rotation6d + normalized camera velocity3`. Train has one human-longer sample and pure test has three; no camera-longer sample exists. Truncating the extra human tail before joint feature construction is equivalent to official fixed-length padding followed by the camera validity mask. Checked mismatch samples match official `get_feat` with max error `0`.

## 3. Corrected Stage1

Both models completed epoch `500`, step `636000`, batch `128`, non-causal temporal convolution, and the same `ae_train_split`.

| model | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| GT identity | -0.00 | 16.47 | 100.0% | -0.00 | 70.24 | 100.0% | 0.945 | 0.7% |
| official pretrained Pulp AE | 109.34 | **15.94** | 92.4% | 17.66 | 60.53 | 84.5% | 0.776 | **3.5%** |
| v7.14 corrected joint AE | **31.10** | 14.99 | **97.9%** | **0.48** | **69.46** | **99.5%** | **0.927** | 5.1% |
| v7.14 corrected joint VAE | 69.61 | 13.77 | 93.1% | 2.28 | 68.45 | 97.7% | 0.914 | 7.9% |

Decision:

- Corrected AE is the active local Stage1 tokenizer.
- It is stronger than the official pretrained anchor on distribution coverage and camera reconstruction, but still slightly weaker on TMR and Out.
- VAE is healthy after contract correction but consistently behind AE; no current evidence justifies its KL cost.
- The old near-zero HCov was a contract failure, not evidence that joint AE/VAE topology is intrinsically invalid.

Artifacts:

```text
/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage1/v7_14_official_contract_20260710/joint_ae_official_4090_gpu0_r2
/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage1/v7_14_official_contract_20260710/joint_vae_official_4090_gpu1_r2
/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage1/v7_14_official_contract_20260710
/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/v7_14_official_contract_stage1_20260710
```

Visualization audit: eight shared ids, `96` MP4, `24` NPZ, zero invalid MP4. Mean root-XY global error is `0.171` for AE and `0.365` for VAE.

The corrected viewer script has four evidence columns: `GT | official pretrained AE | v7.14 corrected joint AE | v7.14 corrected joint VAE`. The invalid v7.13 local-tokenizer rows are excluded. The service is intentionally left stopped for user-controlled launch:

```bash
cd /data/public/ripemangobox/Motion/StoryMotion
.venv-gradio/bin/python scripts/v714_corrected_stage1_gradio.py
```

Mac tunnel:

```bash
ssh -N -L 7863:127.0.0.1:7862 4090
```

### 3.1 Why Corrected AE/VAE Can Beat the Official AE

The result is not a uniform win: official pretrained AE still has better TMR (`15.94` vs `14.99`) and Out (`3.5%` vs `5.1%`) than corrected joint AE. The local models are stronger mainly on reconstruction-distribution metrics.

Plausible contributors, not yet isolated causal claims:

- v7.14 uses `162760` local Stage1 manifest rows and runs `500` epochs / `636000` updates；`94050` is the known official Stage2 cache row count, not a verified official AE training-set size. The released official AE does not disclose its train data, loss, update budget, or checkpoint-selection recipe, so data volume cannot currently explain the gap.
- v7.14 is a shallow `0.96M`-parameter SiLU convolutional AE with Smooth-L1 + velocity training on 64-frame crops；the active official Pulp AE is a deeper `3.20M`-parameter MARDM residual convolutional model with ReLU and nearest-upsample. Both are non-causal, joint human199+camera14, downsample-4, and latent `128+64`, but they are not architecture- or objective-matched.
- Joint camera14 exposes relative distance and FOV directly, making camera reconstruction substantially easier once the contract is correct.
- Better FDTMR/FDCLaTr/coverage can coexist with slightly worse text retrieval and framing, so the result does not prove a universally superior latent for Stage2.

Therefore Stage2 transfer, not Stage1 reconstruction alone, is the required promotion gate.

### 3.2 Retained Data-Quality Findings

The conservative v7.5 hygiene filter targeted the old `94050`-sample official Stage2 cache, not the `162760`-sample `ae_train_split` used by v7.14 Stage1. It is independent of the Stage1 feature/eval bug and remains valid only as a historical data audit:

| split | total | ignored | ignored % | review kept | clean-cache kept |
| --- | ---: | ---: | ---: | ---: | ---: |
| official-cache train | 94050 | 18368 | 19.53% | 16414 | 75682 |
| official-cache val | 10549 | 2150 | 20.38% | 1838 | 8399 |

The rules remove severe global drift, stationary-text/root-motion contradictions, and unsupported vertical outliers. They are conservative hygiene heuristics, not a final curation policy.

This clean cache never entered the v7.14 corrected Stage1 train or its formal eval. A historical `human_text` checkpoint did reference it for a +10k diagnostic fine-tune, but that branch was rejected and never became the corrected mainline. Its 1024-sample clean-val readout changed FTD from `370.06` to `463.14` and coverage from `0.263` to `0.205`, while TMR rose from `18.35` to `20.36`. Retain only the directional conclusion: the old filter is hygiene evidence, not evidence for the current `ae_train_split` and not a sufficient core method.

## 4. Retained Stage2 Evidence

All rows below use the official pretrained Pulp Stage1 cache and official `mixed_` full eval. They are valid Stage2 evidence but do not yet test the corrected v7.14 AE latent space.

### 4.0 Version and Contract Provenance

The official cache metadata identifies Pulp AE checkpoint `autoencoder/aemmardm-xgmj0yjj-325.ckpt`, `94050` train samples, latent order `concat([z_hum,z_cam])`, and official Pulp encode/decode. Thus v6 and the retained official-cache v7 rows do **not** have the later local raw199+camera9 or double-unnormalization bugs. Only v6 experiments that explicitly switched to a local tokenizer must be excluded.

Detailed historical v6 metrics are in [[2026-07-01_storymotion-v6.2-metric-data]].

| evidence family | version | Stage1 source | Stage2 run provenance |
| --- | --- | --- | --- |
| clean unified reference | v6.1/v6.2 | official Pulp AE cache | v6 CondMDI + diffusion full mixed eval |
| one-hot clean / reliability | v7.3.1 e2/e3 | same official cache | `v7_3_1/e2_*`, `v7_3_1/e3_onehot_task_reliability_20260705` |
| width-matched symmetric | v7.13 priority exp1 | same official cache | `v7_13_priority_20260710/exp1_symmetric_joint_width416_steps37500_seed17` |
| human-first + clean H2C | v7.13 Main A / priority exp2 | same official cache | human-text 30k + H2C mixed-p2b 50k |
| replay-adapted H2C | v7.13 priority exp3 | same official cache | exp2 H2C initialization + generated-H replay 10k |

### 4.1 Unified Baselines

| Stage2 | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | role |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| v6 clean unified | 155.73 | 23.95 | 36.4% | 85.70 | 33.5 | 62.8% | 0.374 | 7.9% | strongest retained clean symmetric reference |
| e2 one-hot clean | 208.81 | - | - | 147.53 | - | - | 0.228 | 11.6% | clean-source ablation |
| e3 one-hot reliability | 195.85 | - | - | 126.91 | - | - | 0.253 | 9.0% | schedule improvement over e2, still below v6 |
| v7.13 width-matched symmetric, 37.5k | 196.54 | 18.52 | 32.1% | 182.21 | 17.33 | 48.1% | 0.202 | 11.5% | parameter-width control; training budget still differs |

The shorter v7.13 symmetric control does not beat v6, and its optimization budget differs from the asymmetric pipelines. It is directional evidence against the claim that the current cascade is already superior, not a causal architecture verdict.

### 4.2 Asymmetry and Source Reliability

Artifact root:

```text
/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v7_13_priority_20260710
```

| version / condition | FDTMR↓ | HCov↑ | FDCLaTr↓ | CCov↑ | F1↑ | Out↓ | artifact / readout |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| v7.13 exp2: generated H + clean H2C | 532.49 | 4.8% | 266.46 | 23.7% | 0.199 | 10.3% | `exp2_generated_clean_mixed_full.json`; generated-source shift |
| v7.13 exp2: GT H + clean H2C | 124.45 | 85.3% | 28.03 | 79.8% | 0.567 | 6.1% | `exp2_gt_clean_mixed_full.json`; clean H2C capacity exists |
| v7.13 exp2: GT H + replay path | 124.45 | 85.3% | 307.47 | 20.8% | 0.219 | 29.6% | `exp2_gt_replay_mixed_full.json`; replay path is not clean-equivalent |
| v7.13 exp2: shuffled generated H + replay | 581.52 | 4.8% | 524.35 | 8.7% | 0.098 | 44.2% | `exp2_shuffled_generated_replay_mixed_full.json`; pairing matters |
| v7.13 exp3: generated H + replay-adapted H2C | 532.49 | 4.8% | 70.51 | 48.3% | 0.252 | 27.9% | `exp3_generated_replay_composed_mixed_full.json`; partial camera recovery |
| v7.13 exp3: GT H + replay-adapted H2C | 124.45 | 85.3% | 267.61 | 26.4% | 0.117 | 63.3% | `exp3_gt_clean_composed_mixed_full.json`; severe clean regression |

Decision:

- Current evidence favors symmetric unified Stage2 over the present independent human-first cascade.
- The primary cascade failure is generated-human covariate shift, not absence of clean H2C capacity.
- Generated replay adaptation is a partial distribution repair, not a solution: it improves generated-source FDCLaTr but damages framing and clean-source preservation.
- Any future replay method must report clean and generated buckets together.

## 5. Safe Claims

Can claim:

- Exact feature/decode contracts are decisive for human-camera tokenizer evaluation.
- Corrected joint AE provides a strong Stage1 reconstruction basis.
- Clean H2C capacity does not imply robustness to generated human sources.
- Current replay adaptation trades distribution recovery against framing and clean preservation.
- Current asymmetric cascade has no demonstrated advantage over symmetric unified Stage2.

Cannot claim:

- v7.14 corrected AE has improved Stage2; its Stage2 cache has not yet been trained and evaluated.
- Asymmetry is intrinsically worse; the fully matched corrected-AE A/B is still missing.
- Generated replay robustness or editing is solved.
- Old local-tokenizer Stage1/Stage2 metrics support architecture choices.
