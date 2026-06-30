---
title: "StoryMotion 实验指标分类比较总表"
status: active
tags:
  - StoryMotion
  - Motion_Generation
  - experiment
  - metric
  - status/active
aliases:
  - StoryMotion-Metric-Comparison
hypothesis: |
  StoryMotion 的实验比较必须按 split、evaluation protocol、Stage1/Stage2 口径和 condition source 分组；不同口径不能混表宣称胜负。当前最可靠的结论是：Pulp-style relative camera latent 下，clean GT/root camera completion 可以很强，但 generated/noisy human/root condition 会显著污染 camera；多个新 tokenizer 即使 Stage1 reconstruction 可训练完成，也没有把质量传递到 Stage2 official metrics。
source_notes:
  - "[[2026-06-25_storymotion-v6]]"
  - "[[2026-06-25_storymotion-v6.1]]"
  - "[[2026-06-26_storymotion-progress-summary-0619-0626]]"
  - "[[2026-06-29_storymotion-v6.2]]"
  - "[[2026-07-01_storymotion-v6.2-metric-data]]"
created: 2026-06-30T19:25:00+0800
updated: 2026-07-01T02:47:56+0800
---

> [!abstract] TL;DR
> 5090 已完成 MoLingo human-only、separate AE no-z、separate VAE with-z 的 full mixed train 与 full mixed official eval；补到 `94050/10549` 后结论仍是负面，不能 promoted。mixed-subset 不是单纯 eval 缺 formal test，而是旧 camera manifest 只导出 `29779/3279` paired rows；full camera files 实际存在，full 评估已单独记录在 [[2026-07-01_storymotion-v6.2-metric-data]]。Stage1 official reconstruction metrics 已补全，deterministic separate AE 的 upper bound 很强，但 Stage2 official metrics 说明“Stage1 可重建”不等于“Stage2 可生成”。4090 GPU1 的 joint GRFSQ full 仍未纳入本轮闭环。

## 0. 可比性规则

| 分组 | 可比较对象 | 不可混表对象 | 使用方式 |
| --- | --- | --- | --- |
| full mixed official | `10549` samples、mixed split、Pulp/StoryMotion official callback、bs64 | tokenizer-cache `3279` subset、pure split、training loss | 主性能与外部 baseline 对照 |
| tokenizer-cache official | pure `4053` 或 mixed-subset `3279`、同 tokenizer cache、bs64、seed17 | full mixed `10549` 主表 | 判断新 tokenizer 进入 Stage2 后是否可用 |
| Stage1 reconstruction | posthoc reconstruction MSE、paired human-camera samples | Stage2 generated metrics | 判断 tokenizer 表示是否收敛，不直接宣称生成质量 |
| reliability eval | 同 run、同 split、改变 observed condition source/noise | clean-only main table | 判断 condition reliability，不宣称整体 SOTA |
| early experiments | 早期 V2-V5 探索、部分口径不统一 | 近期正式裁决表 | 只作为路线筛选和假设来源 |

## 0.1 mixed-subset 来源与补救状态

mixed-subset 的根因不是 formal eval 没跑，而是训练 cache 本身来自旧 paired camera manifest：human full mixed manifest 是 `94050/10549`，但旧 `agent2_pulpmotion_camera_mixed_*_manifest_full_20260621.jsonl` 只有 `29779/3279`。`PairedPulpMotionHumanCameraDataset` 按 `sample_id` 取 human/camera 交集，所以后续 tokenizer cache、Stage2 train 和 eval 都被限制到 `29779/3279`。

5090 上复查 `linked/pulpmotion-data/traj` 与 `intrinsics` 后，full mixed human 的 `94050/10549` sample 全部有 camera 文件；因此按“若训练使用 subset，则补 full train”的规则处理。新增 full camera manifest：

- `runs/train/stage1/manifests/agent2_pulpmotion_camera_mixed_train_manifest_full_20260630.jsonl`：`94050`
- `runs/train/stage1/manifests/agent2_pulpmotion_camera_mixed_test_manifest_full_20260630.jsonl`：`10549`

full-cache/full-train 与 full mixed official eval 已在 5090 完成，均使用新 full camera manifest；旧 subset 结果保留为早期/不公平对照：

| run | GPU | cache target | train target | status |
| --- | ---: | --- | --- | --- |
| separate AE no-z full | 5090 GPU0 | `v6_2_separate_ae_noz_seed17_fullcache_20260630/mixed_noz_full` | `v6_2_separate_ae_noz_seed17_fulltrain_20260630/mixed_b512_full` | train + full official eval complete; negative |
| separate VAE with-z full | 5090 GPU1 | `v6_2_separate_vae_wz_seed17_fullcache_20260630/mixed_full` | `v6_2_separate_vae_wz_seed17_fulltrain_20260630/mixed_b512_full` | train + full official eval complete; negative |
| MoLingo human-only full | 5090 GPU2 | `v6_2_molingo_human_seed17_fullcache_20260630/mixed_noz_full` | `v6_2_molingo_human_seed17_fulltrain_20260630/human_only_b512_full` | train + full official eval complete; negative |

Full mixed official metric rows are stored in [[2026-07-01_storymotion-v6.2-metric-data]].

![[2026-07-01_storymotion-v6.2-metric-data#Full Mixed Official Eval 2026-07-01]]

## 1. 近期主表与新闭环

这些行是目前最接近论文主比较的结果。`mixed-subset` 只用于新 tokenizer / MoLingo 的 3279-sample cache 闭环，不能与 full mixed 精确数值比较，只能判断数量级和失败趋势。

| model                   | phase       | split        | task   | samples |  FDTMR↓ |  TMR↑ |  HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ |   F1↑ |  Out↓ | RootFrame↑ | MPJPE↓ | verdict                             |
| ----------------------- | ----------- | ------------ | ------ | ------: | ------: | ----: | -----: | -------: | -----: | ----: | ----: | ----: | ---------: | -----: | ----------------------------------- |
| GT human                | reference   | mixed        | human  |   10549 |  -0.000 | 17.71 | 100.0% |        - |      - |     - |     - |     - |          - |      - | oracle only                         |
| StoryMotion v6 unified  | recent-main | mixed        | human  |   10549 |  126.71 | 18.17 |  84.6% |        - |      - |     - |     - |     - |          - |  0.088 | valid main row                      |
| StoryMotion v6 unified  | recent-main | mixed        | camera |   10549 |       - |     - |      - |    14.50 |  54.85 | 87.1% | 0.638 |     - |          - |  0.085 | valid main row                      |
| StoryMotion v6 unified  | recent-main | mixed        | joint  |   10549 |  155.73 | 23.95 |  36.4% |    85.70 |  33.52 | 62.8% | 0.374 |  7.9% |          - |  0.194 | valid main row                      |
| Camera specialist       | recent-main | mixed        | camera |   10549 |       - |     - |      - |    14.33 |  57.03 | 86.6% | 0.659 |     - |          - |  0.085 | single-task baseline                |
| Human specialist        | recent-main | mixed        | human  |   10549 |  125.28 | 18.24 |  84.8% |        - |      - |     - |     - |     - |          - |  0.087 | single-task baseline                |
| E.T./DIRECTOR root-only | external    | mixed        | camera |   10549 |       - |     - |      - |    14.51 |  54.84 | 87.0% | 0.638 |     - |      81.5% |  0.085 | clean GT/root strong                |
| E.T./DIRECTOR replay    | external    | mixed        | camera |   10549 |       - |     - |      - |    92.24 |  33.31 | 62.8% | 0.375 |     - |      27.3% |  0.194 | generated-human condition collapses |
| MoLingo human-only      | external    | mixed-subset | human  |    3279 | 2353.96 | 4.466 |   0.1% |        - |      - |     - |     - |     - |      14.9% |  0.342 | completed; weak human baseline      |
| separate AE no-z        | stage2-new  | mixed-subset | human  |    3279 | 2018.28 | 4.450 |   0.1% |        - |      - |     - |     - |     - |       8.2% |  0.389 | negative transfer                   |
| separate AE no-z        | stage2-new  | mixed-subset | camera |    3279 |       - |     - |      - |   623.87 |  8.476 |  0.8% | 0.074 |     - |       9.0% |  0.388 | negative transfer                   |
| separate AE no-z        | stage2-new  | mixed-subset | joint  |    3279 | 2031.69 | 5.084 |   0.0% |   583.11 |  9.728 |  1.0% | 0.070 | 93.7% |       9.3% |  0.385 | negative transfer                   |

**读数**：

- E.T./DIRECTOR root-only 与 StoryMotion clean camera completion 在 clean GT/root condition 下同量级，但 replay 退化到 FDCLaTr `92.24`，说明 clean camera completion 不能外推到 generated-human condition。
- MoLingo human-only 已完成合法 Stage2/cache/eval contract；full mixed FDTMR `2396.07`、HCov `0.04%`，不构成有效 human baseline。
- separate AE no-z 的 Stage1 reconstruction 可接受，但 Stage2 official rows 与 VAE/GRFSQ/HFSQ 一样坍塌；full mixed eval 仍是负面，说明 deterministic AE 并没有解决 tokenizer-to-Stage2 传递问题。
- separate VAE with-z 的 full mixed eval 明显弱于旧 mixed-subset 读数，尤其 joint camera FDCLaTr `885.36`、Out `99.0%`；subset 结果不能外推为有效 baseline。

## 2. 新 tokenizer 进入 Stage2 的 official 负面对照

同类实验集中在本表。pure 和 mixed-subset 分开看；它们共同用于判断 tokenizer-cache Stage2 是否可用，不与 full mixed 主表精确比较。

| model | phase | split | task | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | RootFrame↑ | MPJPE↓ | verdict |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| separate VAE no-z | stage2-tokenizer | pure | human | 4053 | 2012.64 | 0.000 | 0.0% | - | - | - | - | - | 10.9% | 0.250 | negative |
| separate VAE no-z | stage2-tokenizer | pure | camera | 4053 | - | - | - | 581.95 | 9.136 | 4.7% | 0.017 | - | 10.8% | 0.250 | negative |
| separate VAE no-z | stage2-tokenizer | pure | joint | 4053 | 2018.62 | 0.000 | 0.0% | 586.65 | 8.473 | 5.0% | 0.018 | 99.7% | 10.6% | 0.249 | negative |
| separate GRFSQ | stage2-tokenizer | pure | human | 4053 | 1816.87 | 3.936 | 0.0% | - | - | - | - | - | 15.7% | 0.229 | negative |
| separate GRFSQ | stage2-tokenizer | pure | camera | 4053 | - | - | - | 832.14 | 11.45 | 0.2% | 0.069 | - | 15.4% | 0.230 | negative |
| separate GRFSQ | stage2-tokenizer | pure | joint | 4053 | 1803.40 | 3.876 | 0.0% | 818.95 | 11.26 | 0.2% | 0.068 | 75.8% | 15.4% | 0.229 | negative |
| separate HFSQ | stage2-tokenizer | pure | human | 4053 | 2106.54 | 4.541 | 0.0% | - | - | - | - | - | 14.8% | 0.236 | negative |
| separate HFSQ | stage2-tokenizer | pure | camera | 4053 | - | - | - | 596.14 | 10.15 | 1.9% | 0.079 | - | 15.3% | 0.238 | negative |
| separate HFSQ | stage2-tokenizer | pure | joint | 4053 | 2100.08 | 4.514 | 0.0% | 581.47 | 9.902 | 1.9% | 0.078 | 79.3% | 14.9% | 0.236 | negative |
| separate VAE with-z | stage2-tokenizer | mixed-subset | human | 3279 | 1274.72 | 7.076 | 0.6% | - | - | - | - | - | - | 0.234 | negative |
| separate VAE with-z | stage2-tokenizer | mixed-subset | camera | 3279 | - | - | - | 118.77 | 38.08 | 49.9% | 0.472 | - | - | 0.154 | negative |
| separate VAE with-z | stage2-tokenizer | mixed-subset | joint | 3279 | 1316.47 | 6.889 | 0.2% | 133.95 | 32.55 | 44.7% | 0.415 | 39.4% | - | 0.237 | negative |
| separate GRFSQ | stage2-tokenizer | mixed-subset | human | 3279 | 1704.87 | 4.620 | 0.1% | - | - | - | - | - | 24.7% | 0.235 | negative |
| separate GRFSQ | stage2-tokenizer | mixed-subset | camera | 3279 | - | - | - | 589.93 | 19.54 | 3.1% | 0.119 | - | 23.9% | 0.235 | negative |
| separate GRFSQ | stage2-tokenizer | mixed-subset | joint | 3279 | 1678.85 | 4.537 | 0.1% | 570.49 | 19.03 | 3.6% | 0.117 | 40.4% | 23.4% | 0.234 | negative |
| separate HFSQ | stage2-tokenizer | mixed-subset | human | 3279 | 2245.73 | 7.768 | 0.0% | - | - | - | - | - | 22.2% | 0.235 | negative |
| separate HFSQ | stage2-tokenizer | mixed-subset | camera | 3279 | - | - | - | 783.52 | 21.11 | 0.6% | 0.115 | - | 22.1% | 0.235 | negative |
| separate HFSQ | stage2-tokenizer | mixed-subset | joint | 3279 | 2235.91 | 7.745 | 0.0% | 770.02 | 21.13 | 0.9% | 0.118 | 65.9% | 22.1% | 0.235 | negative |

**读数**：

- VAE with-z mixed 是这些 source tokenizer Stage2 中相对没那么差的一组，但仍显著低于 StoryMotion/Pulp clean rows。
- AE no-z 没有比 VAE/GRFSQ/HFSQ 改变结论：separate deterministic tokenizer 进入 Stage2 后，camera/joint 仍失去 coverage、framing 和 semantic alignment。
- 这些行的价值是证明 Stage2 对 latent geometry/contract 极敏感，不是提供新 baseline。

## 3. Stage1 reconstruction 与 ablation

Stage1 表只说明 tokenizer reconstruction/posthoc eval，不说明 generation quality。loss/MSE 只作为辅助诊断；主读数改用官方 metric callback 评估 frozen Stage1 reconstruction upper bound。no-z camera/joint 使用 GT-z passthrough diagnostic，因此 camera 语义/构图指标可比较，但不能说明 tokenizer 学会了 z-depth。

### 3.1 official reconstruction metric

| tokenizer | split | samples | task | FDTMR↓ | TMR↑ | FDCLaTr↓ | CLaTr↑ | caption F1↑ | outscreen↓ | z policy | verdict |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| separate AE no-z | mixed-subset | 3279 | joint | 1360.39 | 10.524 | 2.71 | 66.26 | 0.878 | 20.3% | GT-z diagnostic | best Stage1 upper bound; Stage2 still fails |
| separate AE no-z | mixed-subset | 3279 | human | 1360.39 | 10.524 | - | - | - | - | GT-z diagnostic | human recon upper bound ok |
| separate AE no-z | mixed-subset | 3279 | camera | - | - | 2.71 | 66.26 | 0.878 | - | GT-z diagnostic | camera recon upper bound strong |
| separate VAE with-z | mixed-subset | 3279 | joint | 1364.23 | 10.505 | 4.75 | 64.87 | 0.842 | 20.0% | native 9D | strong Stage1, weak Stage2 |
| separate VAE with-z | mixed-subset | 3279 | human | 1364.23 | 10.505 | - | - | - | - | native 9D | human recon upper bound ok |
| separate VAE with-z | mixed-subset | 3279 | camera | - | - | 4.75 | 64.87 | 0.842 | - | native 9D | camera recon upper bound strong |
| MoLingo VAE no-z | mixed-subset | 3279 | joint | 1366.94 | 10.409 | 11.51 | 63.85 | 0.813 | 20.5% | GT-z diagnostic | Stage1 ok, human-only Stage2 fails |
| HFSQ wscale no-z | mixed-subset | 3279 | joint | 1467.92 | 6.690 | 67.60 | 47.73 | 0.585 | 18.9% | GT-z diagnostic | quantized recon weaker |
| GRFSQ bs128 no-z | mixed-subset | 3279 | joint | 1359.42 | 8.309 | 140.01 | 45.10 | 0.592 | 19.8% | GT-z diagnostic | camera upper bound weak |

### 3.2 feature-space MSE / loss auxiliary

| model | split | samples | step | total↓ | human MSE↓ | camera MSE↓ | KL | verdict |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| separate VAE no-z | mixed | 3279 | 200000 | 0.001170 | 0.001486 | 0.000854 | - | 当前 mixed reconstruction 最强之一 |
| separate VAE with-z | mixed | 3279 | 116500 | 0.004 | 0.002 | 0.002 | 2.696 | official upper bound strong；Stage2 仍弱 |
| separate AE no-z best | mixed | 3279 | 116500 | 0.002 | 0.001 | 0.001 | - | deterministic separate recon ok |
| joint VAE with-z KL best | mixed | 3279 | 110000 | 0.008 | 0.004 | 0.008 | 3.690 | KL joint recon weak |
| separate GRFSQ longtrain | mixed | 3279 | 406000 | 0.601149 | 0.007874 | 1.194424 | - | mixed camera 仍受限 |
| separate HFSQ | mixed | 3279 | 115000 | 0.813651 | 0.022907 | 1.604395 | - | mixed camera 更差 |

**读数**：

- AE no-z 的 official reconstruction upper bound 很强，camera CLaTr `66.26`、caption F1 `0.878`，甚至高于 separate VAE with-z 的 `64.87` / `0.842`；但 Stage2 official eval 仍坍塌，因此问题不只是 KL/采样导致的 reconstruction failure。
- joint VAE with-z KL 的 Stage1 recon 明显差，不能当作“给 Pulp joint Stage1 加 KL 就会更适合 diffusion”的证据。

## 4. Reliability / observed condition 对照

本表只比较 camera completion 对 observed human/root condition 的可靠性。它回答“能不能相信 observed branch”，不回答 joint generation 整体 SOTA。

| model | phase | split | task | samples | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | RootFrame↑ | MPJPE↓ | condition |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| P0 neutral | reliability | mixed | camera | 10549 | 14.50 | 54.85 | 87.1% | 0.638 | - | 0.085 | clean GT human/root |
| P0 noise 0.05 | reliability | mixed | camera | 10549 | 22.0 | 53.2 | 85.6% | - | - | - | observed human/root noisy |
| P0 noise 0.10 | reliability | mixed | camera | 10549 | 51.9 | 48.7 | 80.2% | - | - | - | observed human/root noisy |
| P0 noise 0.15 | reliability | mixed | camera | 10549 | 96.87 | 43.54 | 70.1% | 0.503 | 78.1% | 0.086 | observed human/root noisy |
| P0 noise 0.30 | reliability | mixed | camera | 10549 | 216.79 | 32.96 | 46.7% | 0.360 | 73.1% | 0.088 | observed human/root noisy |
| P0 noise 0.50 | reliability | mixed | camera | 10549 | 303.0 | 25.7 | 31.0% | - | - | - | observed human/root noisy |
| P2b v1 clean | reliability | mixed | camera | 10549 | 88.84 | 27.82 | 62.2% | 0.327 | 39.7% | 0.085 | clean GT human/root |
| P2b v1 noise 0.05 | reliability | mixed | camera | 10549 | 28.24 | 42.47 | 77.8% | 0.473 | 67.6% | 0.085 | observed human/root noisy |
| P2b v1 noise 0.15 | reliability | mixed | camera | 10549 | 30.36 | 40.73 | 77.7% | 0.458 | 68.9% | 0.086 | observed human/root noisy |
| P2b v1 noise 0.30 | reliability | mixed | camera | 10549 | 46.84 | 38.96 | 75.0% | 0.442 | 64.6% | 0.088 | observed human/root noisy |
| P2b v1 noise 0.50 | reliability | mixed | camera | 10549 | 66.38 | 34.56 | 70.2% | 0.397 | 61.7% | 0.092 | observed human/root noisy |
| P2b v2 clean-preserve | reliability | mixed | camera | 10549 | 46.08 | 43.74 | 75.7% | 0.499 | 72.8% | 0.085 | clean-preserving attempt |

**读数**：

- P2a/P0 随 human/root noise 快速退化，std `0.15` 已从 FDCLaTr `14.50` 到 `96.87`。
- P2b v1 对 noisy condition 明显更稳，但 clean condition 从 `14.50` 退化到 `88.84`，不能作为主解法。
- P2b v2 clean-preserve 改善 clean 退化，但仍不回到 P0 clean；reliability 方向成立，配方未完成。

## 5. 早期实验与近期实验分界

| 时段 | 实验族 | 主要指标/现象 | 当前地位 |
| --- | --- | --- | --- |
| early V2-V4 | branch-mask / inpainting / controlled coupling | text noise 对 completion 影响小；observed branch zero/shuffle/noise 影响大；joint text shuffle 会显著降低语义指标 | 形成 C2 reliability 与 text-routing 诊断 |
| early V4-V5 | task ratio / joint-heavy / camera-heavy | 禁用 human-only 或强推 camera-heavy 会破坏 human/root 锚点；camera/joint 不稳定 | 排除训练捷径 |
| early V5 | source tokenizer VAE/HFSQ/GRFSQ + Z-score/geo loss | 多组 official human/camera metrics 坍塌 | 排除“直接替换 Stage1” |
| early V5 | screen projection containment | Out 可压低到约 `0.50%`，但 FDCLaTr `350.09`、F1 `17.44%`，后续 NaN | 排除主线路，只保留为 bounded loss 未来方向 |
| recent V6 | unified vs specialists | unified camera/human completion 与 specialists 接近；joint 仍弱 | 当前 main baseline |
| recent V6.1 | P2a/P2b | P2a 定位 camera fragile；P2b noisy condition 有效但 clean/generative condition 失败 | reliability mismatch 成立，修复未完成 |
| recent V6.2 | E.T./DIRECTOR root-only | clean GT/root camera 强，generated-human replay 弱 | 外部 camera baseline + reliability 证据 |
| recent V6.2 | MoLingo human-only | full mixed FDTMR `2396.07`、HCov `0.04%` | 完成但不 promoted |
| recent V6.2 | separate AE no-z / VAE / GRFSQ / HFSQ Stage2 | full mixed 仍坍塌；Stage1 可训练不代表 Stage2 official metrics 可用 | tokenizer-to-Stage2 传递风险成立 |

## 6. Stage1 tokenizer visualization

已在 5090 GPU3 生成统一 Stage1 tokenizer reconstruction 可视化，输出路径为：

- `runs/visualizations/stage1_tokenizers_20260630/manifest.json`

覆盖 `4` 个 mixed-test sample、`5` 个 tokenizer：`separate_ae_noz`、`separate_vae_wz`、`separate_hfsq_wscale_noz`、`separate_grfsq_bs128_noz`、`molingo_vae_noz`。每个 sample/model 写出 `fixed_camera.mp4`、`orbiting_camera.mp4`、`camera_trajectory.mp4` 和 `rifke_joints_projection.npz`；加上 manifest 共 `73` 个文件。该可视化用于检查 Stage1 frozen reconstruction，不用于宣称 Stage2 generation 质量。

## 7. 当前裁决

1. **主线有效行**：StoryMotion v6 unified / specialists / E.T. root-only clean camera rows 可以作为 clean-condition comparison，但必须注明 GT/root condition。
2. **主线风险**：E.T. replay、P2a noise、P2b clean drop 一致说明 generated/noisy human/root condition 是 camera completion 的关键风险。
3. **tokenizer 结论**：separate AE no-z、VAE、GRFSQ、HFSQ 均不能 promoted；它们是 Stage1-to-Stage2 contract failure 证据。
4. **MoLingo 结论**：合法 human-only Stage2 eval 已完成；full mixed 结果仍太弱，不能作为有效 external human baseline。
5. **论文表述边界**：不能写“unified 已解决 robust human-camera generation”，只能写“建立了统一协议、发现并量化了 reliability mismatch，并排除了若干 tokenizer/训练捷径”。

## 8. 证据路径

- session log: `/home/ripemangobox/.codex/sessions/2026/06/30/rollout-2026-06-30T13-49-11-019f1713-09e8-7712-8d35-bffba1f1b25c.jsonl`
- final eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_final_eval_20260630`
- seed17 tokenizer / E.T. eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_seed17_eval_20260630`
- VAE human-global eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_separate_humanglobal_20260630`
- Stage1 official recon eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_stage1_official_recon_20260630`
- Stage1 tokenizer visualization: `/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations/stage1_tokenizers_20260630`
- full mixed camera manifests: `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage1/manifests/agent2_pulpmotion_camera_mixed_*_manifest_full_20260630.jsonl`
- full-train logs: `/data/public/ripemangobox/Motion/StoryMotion/logs/v6_2_fulltrain_20260630`
- full mixed official eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_fulltrain_eval_20260701`
- Stage1 ablation eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_resume_20260629/pulp_stage1_ablation_eval`
- v6 native baseline: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_p0_native_20260625`
- reliability eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_p2b_robustness_20260628`
