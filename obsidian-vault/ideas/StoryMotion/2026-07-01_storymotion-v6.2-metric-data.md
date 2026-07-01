---
title: "StoryMotion v6.2 Metric Data"
status: active
tags:
  - StoryMotion
  - Motion_Generation
  - experiment
  - metric
  - data
  - status/active
aliases:
  - StoryMotion-v6.2-Metric-Data
source_notes:
  - "[[2026-06-10_pulp-stage1-continuous-stage2-generator-formal]]"
  - "[[2026-06-29_storymotion-v6.2]]"
  - "[[2026-06-30_storymotion-experiment-metric-comparison]]"
created: 2026-07-01T02:47:56+0800
updated: 2026-07-01T14:08:43+0800
---

## 0. Fair Comparison Rules

本页是数据独立页，结论页只应通过 Obsidian 引用这里的表格。表内不使用 aliased wikilink，避免 `|` 破坏 Markdown table。

| group | fair comparison | do not mix as direct ranking | use |
| --- | --- | --- | --- |
| full mixed official | mixed split `10549` samples、Pulp/StoryMotion official callback、bs64、seed17 | mixed-subset `3279`、pure `4053`、training loss | 主性能、外部 baseline、recent v6/v6.2 对照 |
| pure official | pure split `4053` samples、同 callback | mixed full | 判断 pure 场景，不外推到 mixed |
| tokenizer-cache official | pure `4053` 或旧 mixed-subset `3279`、source-tokenizer-aware cache | full mixed official 主表 | 判断新 tokenizer 进入 Stage2 是否可用 |
| Stage1 reconstruction | frozen Stage1 reconstruction decoded 后跑 official metrics，或 feature-space MSE | Stage2 generated quality | 判断 tokenizer upper bound / 表示质量 |
| reliability eval | 同 run、同 split，只改变 observed human/root condition source 或 noise | clean-only main table | 判断 branch coupling / reliability mismatch |

旧 mixed-subset 不是“只在 eval 阶段没有 formal test”。复查结果是旧 paired camera manifest 只导出 `29779/3279` rows，导致训练 cache、Stage2 train 和 eval 都在 subset 上；full camera manifest 已补到 `94050/10549`，对应 full train / full eval 行已记录在本页。

## 1. Full Mixed Main Comparison

口径：full mixed test `10549` samples；Pulp/StoryMotion official callback；bs64；seed17。E.T./DIRECTOR 只作为 camera completion external baseline：GT/root condition 行与 clean camera completion 可比，generated-human replay 行是 reliability 诊断，不是完整 joint generation baseline。

| model | phase | split | task | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | RootFrame↑ | MPJPE↓ | verdict |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| GT human | reference | mixed | human | 10549 | -0.00 | 17.71 | 100.0% | - | - | - | - | - | - | - | oracle human reference |
| Pulp official Stage1 recon | upper-bound | mixed | human | 10549 | 124.46 | 18.17 | 85.4% | - | - | - | - | - | - | - | frozen AE reconstruction upper bound |
| Pulp official Stage1 recon | upper-bound | mixed | camera | 10549 | - | - | - | 15.51 | 58.10 | 87.2% | 0.670 | - | - | - | frozen AE reconstruction upper bound |
| Pulp official Stage1 recon | upper-bound | mixed | joint | 10549 | 124.46 | 18.17 | 85.4% | 15.51 | 58.10 | 87.2% | 0.670 | 4.6% | - | - | Stage1 upper bound, not generated Stage2 |
| StoryMotion v6 unified | recent-main | mixed | human | 10549 | 126.71 | 18.17 | 84.6% | - | - | - | - | - | - | 0.088 | valid clean completion row |
| StoryMotion v6 unified | recent-main | mixed | camera | 10549 | - | - | - | 14.50 | 54.85 | 87.1% | 0.638 | - | - | 0.085 | valid clean completion row |
| StoryMotion v6 unified | recent-main | mixed | joint | 10549 | 155.73 | 23.95 | 36.4% | 85.70 | 33.52 | 62.8% | 0.374 | 7.9% | - | 0.194 | joint weaker than clean completion |
| Human specialist | recent-main | mixed | human | 10549 | 125.28 | 18.24 | 84.8% | - | - | - | - | - | - | 0.087 | single-task human baseline |
| Camera specialist | recent-main | mixed | camera | 10549 | - | - | - | 14.33 | 57.03 | 86.6% | 0.659 | - | - | 0.085 | single-task camera baseline |
| PulpMotion Stage2 no-Aux wz0 | baseline | mixed | joint | 10549 | 377.36 | 23.36 | 10.4% | 88.42 | 31.31 | 50.5% | 0.350 | 26.6% | - | - | Pulp official no-Aux rerun; generated joint baseline |
| PulpMotion Stage2 wz2 probe | inference-probe | mixed | joint | 10549 | 709.60 | 22.11 | 2.5% | 440.27 | 15.15 | 9.5% | 0.162 | 9.4% | - | - | projection CFG probe, not promoted |
| E.T./DIRECTOR root-only | external | mixed | camera | 10549 | - | - | - | 14.51 | 54.84 | 87.0% | 0.638 | - | 81.5% | 0.085 | clean GT/root condition strong |
| E.T./DIRECTOR replay | external-diagnostic | mixed | camera | 10549 | - | - | - | 92.24 | 33.31 | 62.8% | 0.375 | - | 27.3% | 0.194 | generated-human condition collapses |

读数：

- Pulp official Stage1 reconstruction 的 mixed joint upper bound 是 FDTMR `124.46`、FDCLaTr `15.51`、Out `4.6%`；它说明官方 AE 表示很强，但不是 generated Stage2。
- StoryMotion v6 clean human/camera completion 接近 Pulp official Stage1 upper bound；joint generation 明显弱于 completion，尤其 camera FDCLaTr `85.70`、F1 `0.374`。
- E.T./DIRECTOR clean GT/root camera 行与 StoryMotion clean camera 行同量级，但同样的 external camera baseline 在 generated-human replay 下退化到 FDCLaTr `92.24`、RootFrame `27.3%`。这支持 branch reliability 问题，不支持“clean camera completion 可外推到 generated-human condition”。

## 2. Pure Official Rows

Pure split 只与 pure 行比较，不与 full mixed 主表直接排名。

| model | phase | split | task | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | MPJPE↓ | verdict |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Pulp official Stage1 recon | upper-bound | pure | human | 4053 | 109.34 | 15.94 | 92.4% | - | - | - | - | - | - | pure Stage1 upper bound |
| Pulp official Stage1 recon | upper-bound | pure | camera | 4053 | - | - | - | 17.66 | 60.53 | 84.5% | 0.776 | - | - | pure Stage1 upper bound |
| Pulp official Stage1 recon | upper-bound | pure | joint | 4053 | 109.34 | 15.94 | 92.4% | 17.66 | 60.53 | 84.5% | 0.776 | 3.5% | - | pure Stage1 upper bound |
| StoryMotion v6 unified | recent-main | pure | human | 4053 | 111.14 | 16.00 | 91.9% | - | - | - | - | - | 0.082 | pure completion strong |
| StoryMotion v6 unified | recent-main | pure | camera | 4053 | - | - | - | 23.36 | 58.41 | 83.6% | 0.763 | - | 0.079 | pure completion strong |
| StoryMotion v6 unified | recent-main | pure | joint | 4053 | 137.12 | 21.25 | 46.4% | 91.47 | 44.46 | 61.3% | 0.594 | 6.9% | 0.195 | joint still weaker |
| PulpMotion Stage2 no-Aux | baseline | pure | joint | 4053 | 377.55 | 20.60 | 15.0% | 93.02 | 36.55 | 49.8% | 0.489 | 38.4% | - | generated joint baseline |
| PulpMotion Stage2 Aux | baseline | pure | joint | 4053 | 419.24 | 21.69 | 14.6% | 90.62 | 38.90 | 44.8% | 0.520 | 27.1% | - | generated joint baseline |

## 3. Stage1 Reconstruction And Ablation

### 3.1 Pulp Official Stage1 Three-Mode Reconstruction

口径：`runs/eval/pulpmotion_core_bs64_20260625/stage1/*_reconstruction_bs64.json`，frozen official autoencoder reconstruction decoded 后跑 official metrics。它是 Stage1 upper bound，不是 Stage2 generation。

| tokenizer | split | task | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | readout |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Pulp official Stage1 recon | pure | human | 4053 | 109.34 | 15.94 | 92.4% | - | - | - | - | - | human reconstruction strong |
| Pulp official Stage1 recon | pure | camera | 4053 | - | - | - | 17.66 | 60.53 | 84.5% | 0.776 | - | camera reconstruction strong |
| Pulp official Stage1 recon | pure | joint | 4053 | 109.34 | 15.94 | 92.4% | 17.66 | 60.53 | 84.5% | 0.776 | 3.5% | three-mode upper bound strong |
| Pulp official Stage1 recon | mixed | human | 10549 | 124.46 | 18.17 | 85.4% | - | - | - | - | - | human reconstruction strong |
| Pulp official Stage1 recon | mixed | camera | 10549 | - | - | - | 15.51 | 58.10 | 87.2% | 0.670 | - | camera reconstruction strong |
| Pulp official Stage1 recon | mixed | joint | 10549 | 124.46 | 18.17 | 85.4% | 15.51 | 58.10 | 87.2% | 0.670 | 4.6% | three-mode upper bound strong |

### 3.2 Source Tokenizer Official Reconstruction Upper Bounds

这些是 frozen Stage1 reconstruction 的 official metric，不是 Stage2 generated rows。no-z camera/joint 行使用 GT-z passthrough diagnostic，因此能读 camera semantic/framing upper bound，但不能说明 tokenizer 自己学会 z-depth。

| tokenizer | split | samples | task | FDTMR↓ | TMR↑ | FDCLaTr↓ | CLaTr↑ | F1↑ | Out↓ | z policy | Stage2 result |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| separate AE no-z | mixed-subset | 3279 | joint | 1360.39 | 10.524 | 2.71 | 66.26 | 0.878 | 20.3% | GT-z diagnostic | full mixed Stage2 still collapses |
| separate AE no-z | mixed-subset | 3279 | human | 1360.39 | 10.524 | - | - | - | - | GT-z diagnostic | full mixed Stage2 human weak |
| separate AE no-z | mixed-subset | 3279 | camera | - | - | 2.71 | 66.26 | 0.878 | - | GT-z diagnostic | full mixed Stage2 camera weak |
| separate VAE with-z | mixed-subset | 3279 | joint | 1364.23 | 10.505 | 4.75 | 64.87 | 0.842 | 20.0% | native 9D | full mixed Stage2 collapses |
| separate VAE with-z | mixed-subset | 3279 | human | 1364.23 | 10.505 | - | - | - | - | native 9D | full mixed Stage2 human weak |
| separate VAE with-z | mixed-subset | 3279 | camera | - | - | 4.75 | 64.87 | 0.842 | - | native 9D | full mixed Stage2 camera weak |
| MoLingo VAE no-z | mixed-subset | 3279 | joint | 1366.94 | 10.409 | 11.51 | 63.85 | 0.813 | 20.5% | GT-z diagnostic | human-only Stage2 weak |
| HFSQ wscale no-z | mixed-subset | 3279 | joint | 1467.92 | 6.690 | 67.60 | 47.73 | 0.585 | 18.9% | GT-z diagnostic | Stage2 weak |
| GRFSQ bs128 no-z | mixed-subset | 3279 | joint | 1359.42 | 8.309 | 140.01 | 45.10 | 0.592 | 19.8% | GT-z diagnostic | Stage2 weak |

### 3.3 Feature-Space MSE / Loss Auxiliary

MSE/loss 只能做辅助诊断。它解释“训练 loss 看起来收敛”为什么不能直接等同 official metric：loss 在 normalized feature space 内，official metric 是 decoded human/camera 后的 TMR/CLaTr/projection/caption score。

| tokenizer | split | samples | step | total↓ | human MSE↓ | camera MSE↓ | joint MSE↓ | KL / code usage | readout |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| separate VAE no-z | mixed-subset | 3279 | 200000 | 0.001170 | 0.001486 | 0.000854 | - | - | feature MSE strong; not enough for Stage2 |
| separate AE no-z | mixed-subset | 3279 | 116500 | 0.002174 | 0.001469 | 0.000933 | - | - | deterministic separate AE reconstructs, Stage2 still fails |
| separate VAE with-z | mixed-subset | 3279 | 116500 | 0.004 | 0.002 | 0.002 | - | KL `2.696` | official upper bound strong; Stage2 still weak |
| Pulp joint VAE with-z KL | mixed-subset | 3279 | 110000 | 0.007822 | 0.003893 | 0.008252 | - | KL `3.689679` | KL joint recon weaker than deterministic AE |
| Pulp joint VAE with-z KL | mixed-subset | 3279 | 116500 | 0.007844 | 0.003877 | 0.008260 | - | KL `3.894135` | last similar to best |
| corrected joint VAE with-z | mixed full | 10549 | 144000 | 0.003617 | 0.001752 | 0.005145 | 0.003448 | KL `29.66` | Stage1 recon usable; Stage2 collapses |
| corrected joint GRFSQ with-z | mixed full | 10549 | 245000 | 0.009264 | 0.004162 | 0.292299 | 0.148231 | active `1000`, ppl `144.28` | mixed camera recon weak; Stage2 negative |
| corrected joint VAE with-z | pure | 4053 | 142000 | 0.001932 | 0.002537 | 0.000338 | 0.001438 | KL `3.05` | pure Stage1 clean |
| corrected joint GRFSQ with-z | pure | 4053 | 140000 | 0.003852 | 0.003944 | 0.002418 | 0.003181 | active `1000`, ppl `83.48` | pure Stage1 clean enough |
| separate GRFSQ longtrain | mixed-subset | 3279 | 406000 | 0.601149 | 0.007874 | 1.194424 | - | - | mixed camera feature MSE very weak |
| separate HFSQ | mixed-subset | 3279 | 115000 | 0.813651 | 0.022907 | 1.604395 | - | - | mixed camera feature MSE worse |

读数：

- `separate AE no-z` 同时有低 feature MSE 和很强 official reconstruction upper bound，但 Stage2 full mixed 仍 collapse；因此“loss 收敛”不能解释 Stage2 可生成。
- `corrected joint VAE with-z` mixed full Stage1 feature reconstruction 不差，但 Stage2 full mixed TMR 归零、Out 接近 `100%`；这指向 Stage2 对 latent geometry/contract 的适配失败，而不是单纯 Stage1 MSE 不收敛。
- `corrected joint GRFSQ with-z` pure Stage1 可用，但 mixed full camera MSE `0.292299` 明显偏高；它的 Stage2 比 joint VAE 略好，仍远离有效 camera/joint rows。

## 4. Full Mixed Official Eval 2026-07-01

口径：5090 上使用 `scripts/storymotion_official_full_eval.py` / source-tokenizer-aware eval，`batch_size=64`、`seed=17`、`num_steps=50`、`cfg_scale=1.0`、`eta=0.0`，full mixed test `10549` samples。

| model | phase | split | task | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | RootFrame↑ | MPJPE↓ | verdict |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| MoLingo human-only | full-train | mixed | human | 10549 | 2396.07 | 4.112 | 0.04% | - | - | - | - | - | 12.1% | 0.344 | negative; full train does not rescue human baseline |
| separate AE no-z | full-train | mixed | human | 10549 | 2147.78 | 5.547 | 0.03% | - | - | - | - | - | 6.0% | 0.385 | negative |
| separate AE no-z | full-train | mixed | camera | 10549 | - | - | - | 676.56 | 2.794 | 1.00% | 0.084 | - | 6.2% | 0.384 | negative |
| separate AE no-z | full-train | mixed | joint | 10549 | 2157.12 | 5.669 | 0.00% | 662.84 | 3.074 | 1.11% | 0.094 | 95.5% | 6.9% | 0.387 | negative; joint generation collapses |
| separate VAE with-z | full-train | mixed | human | 10549 | 1823.40 | 0.000 | 0.05% | - | - | - | - | - | 8.2% | 0.294 | negative; TMR score collapsed |
| separate VAE with-z | full-train | mixed | camera | 10549 | - | - | - | 841.65 | 3.884 | 0.69% | 0.099 | - | 7.5% | 0.295 | negative |
| separate VAE with-z | full-train | mixed | joint | 10549 | 1863.90 | 0.000 | 0.00% | 885.36 | 3.785 | 0.39% | 0.057 | 99.0% | 7.9% | 0.297 | negative; worse than mixed-subset trend |
| joint VAE with-z | full-train | mixed | human | 10549 | 2176.30 | 0.000 | 0.06% | - | - | - | - | - | 1.9% | 0.237 | negative; Stage2 human collapsed |
| joint VAE with-z | full-train | mixed | camera | 10549 | - | - | - | 959.07 | 3.108 | 0.05% | 0.075 | - | 1.9% | 0.236 | negative; camera collapsed |
| joint VAE with-z | full-train | mixed | joint | 10549 | 2250.73 | 0.000 | 0.00% | 989.53 | 3.016 | 0.01% | 0.052 | 100.0% | 1.9% | 0.235 | negative; worst joint row |
| joint GRFSQ with-z | full-train | mixed | human | 10549 | 1598.73 | 9.887 | 0.02% | - | - | - | - | - | 16.5% | 0.218 | negative; better than joint VAE but still weak |
| joint GRFSQ with-z | full-train | mixed | camera | 10549 | - | - | - | 580.22 | 5.846 | 3.24% | 0.091 | - | 16.4% | 0.218 | negative |
| joint GRFSQ with-z | full-train | mixed | joint | 10549 | 1648.84 | 10.164 | 0.01% | 663.60 | 5.790 | 2.15% | 0.086 | 99.6% | 16.2% | 0.218 | negative; does not rescue joint source-tokenizer Stage2 |

## 5. Mixed-Subset To Full Readout

这张表只比较同一实验族的趋势，不把 subset 与 full 当作公平排名。结论是：旧 mixed-subset 结果不是“eval 少跑 formal test”造成的偶然缺口；补 full train/full eval 后，MoLingo、separate AE no-z、separate VAE with-z 仍不能 promoted。

| experiment | old mixed-subset row | full mixed row | readout |
| --- | --- | --- | --- |
| MoLingo human-only human | `3279` samples, FDTMR `2353.96`, TMR `4.466`, HCov `0.1%` | `10549` samples, FDTMR `2396.07`, TMR `4.112`, HCov `0.04%` | full train does not improve baseline quality |
| separate AE no-z human | `3279` samples, FDTMR `2018.28`, TMR `4.450`, HCov `0.1%` | `10549` samples, FDTMR `2147.78`, TMR `5.547`, HCov `0.03%` | still negative |
| separate AE no-z camera | `3279` samples, FDCLaTr `623.87`, CLaTr `8.476`, F1 `0.074` | `10549` samples, FDCLaTr `676.56`, CLaTr `2.794`, F1 `0.084` | still far from valid camera rows |
| separate AE no-z joint | `3279` samples, FDTMR `2031.69`, FDCLaTr `583.11`, Out `93.7%` | `10549` samples, FDTMR `2157.12`, FDCLaTr `662.84`, Out `95.5%` | joint remains collapsed |
| separate VAE with-z human | `3279` samples, FDTMR `1274.72`, TMR `7.076`, HCov `0.6%` | `10549` samples, FDTMR `1823.40`, TMR `0.000`, HCov `0.05%` | full mixed is worse |
| separate VAE with-z camera | `3279` samples, FDCLaTr `118.77`, CLaTr `38.08`, F1 `0.472` | `10549` samples, FDCLaTr `841.65`, CLaTr `3.884`, F1 `0.099` | subset optimism does not transfer |
| separate VAE with-z joint | `3279` samples, FDTMR `1316.47`, FDCLaTr `133.95`, Out `39.4%` | `10549` samples, FDTMR `1863.90`, FDCLaTr `885.36`, Out `99.0%` | full joint fails decisively |

## 6. Stage2 Branch Coupling Evidence

### 6.1 P2a Matched Noise

口径：StoryMotion v6 P0 clean camera completion 与 matched additive-noise eval；同 mixed full `10549`，只改变 observed human/root noise。human completion 对 observed camera noise 的退化远小于 camera completion 对 observed human/root noise 的退化，因此耦合方向是不对称的。

| observed human/root noise std | camera FDCLaTr↓ | camera CLaTr↑ | camera CCov↑ | camera F1↑ |
| ---: | ---: | ---: | ---: | ---: |
| 0.00 | 14.50 | 54.85 | 87.1% | 0.638 |
| 0.05 | 22.02 | 53.15 | 85.6% | 0.625 |
| 0.10 | 51.89 | 48.66 | 80.2% | 0.573 |
| 0.15 | 96.87 | 43.54 | 70.1% | 0.503 |
| 0.30 | 216.79 | 32.96 | 46.7% | 0.360 |
| 0.50 | 303.00 | 25.68 | 31.0% | 0.278 |

### 6.2 P2b Reliability Attempts

P2b v1 对 noisy condition 有效，但 clean condition 退化；P2b v2 clean-preserve 部分修复 clean drop，但仍未回到 P0 clean。

| model | condition | samples | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | RootFrame↑ | MPJPE↓ | verdict |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| P0 neutral | clean GT human/root | 10549 | 14.50 | 54.85 | 87.1% | 0.638 | - | 0.085 | clean baseline |
| P0 noise 0.15 | observed human/root noisy | 10549 | 96.87 | 43.54 | 70.1% | 0.503 | 78.1% | 0.086 | camera fragile |
| P0 noise 0.30 | observed human/root noisy | 10549 | 216.79 | 32.96 | 46.7% | 0.360 | 73.1% | 0.088 | camera fragile |
| P2b v1 clean | clean GT human/root | 10549 | 88.84 | 27.82 | 62.2% | 0.327 | 39.7% | 0.085 | clean drop too large |
| P2b v1 noise 0.15 | observed human/root noisy | 10549 | 30.36 | 40.73 | 77.7% | 0.458 | 68.9% | 0.086 | noisy condition improved |
| P2b v1 noise 0.30 | observed human/root noisy | 10549 | 46.84 | 38.96 | 75.0% | 0.442 | 64.6% | 0.088 | noisy condition improved |
| P2b v2 clean-preserve | clean GT human/root | 10549 | 46.08 | 43.74 | 75.7% | 0.499 | 72.8% | 0.085 | better than v1 clean, still below P0 |

### 6.3 Latent Diagnostic Evidence

这些是 early Stage2 latent diagnostics，不是 official metric；它们用来证明分支条件被使用、sampler 与 one-step 训练目标有 mismatch。

| diagnostic | sample scope | key numbers | readout |
| --- | ---: | --- | --- |
| cross-swap nearest-source | Stage1 branch controllability | pass rate `1.000`; self A/B MPJPE `0.1979 / 0.2511` | Stage1 branch 可控，但不等于 Stage2 generated quality |
| visible-branch reliance | mixed visible shuffle | camera delta `+1.1016`; human delta `+1.3672` | completion 不是只靠 text shortcut |
| Mode B camera-latent causal gate | `4096` samples | base human median `0.003662`; camera zero / shuffle / matched-noise median `0.216638 / 0.314891 / 0.774336` | Mode B 依赖 camera latent；未分解 distance / motion 子切片 |
| joint sampler re-eval | `1024` samples | teacher-forced `0.016472`; 1-step `0.292046`; 20-step `0.617884`; 50-step `0.740053` | one-step x0 objective 与 recursive sampler 存在 mismatch |
| full generated eval | `10549` records per job | `branch_jh6ft` joint: r_fpd `0.450`, Out `7.48%`, TMR `18.72`, CLaTr `23.70`, F1 `0.284` | generated eval 可跑通；joint 语义仍弱 |

## 7. Joint Branch Visualization 2026-07-01

| scope | manifest | samples | outputs | note |
| --- | --- | ---: | ---: | --- |
| Stage1 joint tokenizer recon | `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/stage1/v6_2_joint_stage1_20260701_rerun/manifest.json` | 4 | 61 files | mixed/pure 各 2 个 sample；GT、joint VAE、joint GRFSQ；fixed/orbit/camera projection + concat |
| Stage2 joint VAE qualitative vis | `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/stage2/v6_2_joint_stage2_20260701_rerun/joint_vae_wz_mixed_full/stage2/vis/v4/concat/cfg_h1_c1_seed17_best_eval/v4_4x3_text_global_camera_manifest.json` | 2 | 6 videos | source-tokenizer-aware 4x3 qualitative vis；`joint` / `human_completion` / `camera_completion` |
| Stage2 joint GRFSQ qualitative vis | `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/stage2/v6_2_joint_stage2_20260701_rerun/joint_grfsq_wz_mixed_full/stage2/vis/v4/concat/cfg_h1_c1_seed17_best_eval/v4_4x3_text_global_camera_manifest.json` | 2 | 6 videos | source-tokenizer-aware 4x3 qualitative vis；probe `failed=0` |

## 8. Evidence Paths

- session log: `/home/ripemangobox/.codex/sessions/2026/06/30/rollout-2026-06-30T13-49-11-019f1713-09e8-7712-8d35-bffba1f1b25c.jsonl`
- Pulp Stage1 official recon: `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/pulpmotion_core_bs64_20260625/stage1`
- Pulp Stage2 official rerun: `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/pulpmotion_official_baseline_20260613` and `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/pulpmotion_core_bs64_20260625/stage2`
- StoryMotion v6 native baseline: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_p0_native_20260625`
- StoryMotion v6 pure baseline: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_pure_dualcol_20260625`
- seed17 tokenizer / E.T. eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_seed17_eval_20260630`
- Stage1 official recon eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_stage1_official_recon_20260630`
- full mixed official eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_fulltrain_eval_20260701`
- joint full mixed official eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_joint_fulltrain_eval_20260701`
- joint Stage1 posthoc eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_joint_stage1_recon_eval_20260701`
- Stage1 ablation eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_resume_20260629/pulp_stage1_ablation_eval`
- P2a matched noise eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_p2a_matched_noise_20260625`
- P2b reliability eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_p2b_robustness_20260628` and `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_p2b_v2_clean_preserve_20260628`
- Stage1 tokenizer visualization: `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/stage1/stage1_tokenizers_20260701_rerun`
- joint Stage1 visualization: `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/stage1/v6_2_joint_stage1_20260701_rerun`
- joint Stage2 visualization: `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/stage2/v6_2_joint_stage2_20260701_rerun`
- full camera manifests: `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage1/manifests/agent2_pulpmotion_camera_mixed_*_manifest_full_20260630.jsonl`
