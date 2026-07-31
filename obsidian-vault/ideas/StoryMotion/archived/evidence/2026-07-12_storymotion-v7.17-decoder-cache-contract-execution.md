---
title: "StoryMotion v7.17 Decoder and Cache Contract Execution"
status: completed
hypothesis: |
  A valid Stage2 judgment requires both the owning decoder and the exact Stage1 encoder architecture; correcting only the decoder cannot rescue a checkpoint trained on a cache produced by the wrong causal encoder.
tags:
  - StoryMotion
  - Motion_Generation
  - experiment
  - audit
  - stage2
  - status/completed
aliases:
  - StoryMotion-v7.17
source_notes:
  - "[[2026-07-11_storymotion-v7.16-stage2-forensic-audit]]"
  - "[[2026-07-11_storymotion-latest-roadmap]]"
created: 2026-07-12T00:35:00+0800
updated: 2026-07-12T03:20:00+0800
---

# StoryMotion v7.17 Decoder and Cache Contract Execution

> [!abstract] Current decision
> 修复 decoder 后，旧 `last.pt + cached latent` 只能做故障取证，不能验证修复后的 Stage2。原因是旧 cache builder 还把 `is_causal=false` 的 v7.14 Stage1 checkpoint 重建成了 causal encoder。正式判断必须重建 non-causal cache；cache identity 通过后，再训练新的 matched 10k checkpoint。

## 1. 已确认的第二个 Contract Bug

v7.14 AE/VAE 的 `run_config.json` 都记录 `is_causal: false`。旧 `build_stage2_joint_tokenizer_latent_cache.py` 只从 preset 重建模型，未读取该字段，因此实际用 causal encoder 生成了 v7.15/v7.16 cache。causal 与 non-causal 权重 shape 相同，`load_state_dict` 不会报错，但前向语义不同。

在同一个 paired sample 上比较旧 cache 与 owning non-causal encoder：

| tokenizer | latent RMS difference |
| --- | ---: |
| joint AE | `0.54–0.61` |
| joint VAE | `0.69–0.82` |

输入侧 paired manifest feature 与 official Pulp feature 已对齐：human RMS difference 为 `0`，camera 约 `9e-9`。因此差异来自 encoder architecture，不是数据或 feature contract。

旧 cache 即使改用 owning decoder 做 identity，也仍明显失真：

| old cache identity | FDTMR ↓ | FDCLaTr ↓ | Out ↓ |
| --- | ---: | ---: | ---: |
| AE causal cache → non-causal AE decoder | 852.82 | 1.89 | 56.73% |
| VAE causal cache → non-causal VAE decoder | 718.27 | 5.13 | 77.93% |

这证明 decoder mismatch 与 cache encoder mismatch 是两个独立问题。旧 v7.16 loss 曲线描述的是错误 causal-encoded cache 的 learnability，不能外推到修正版 Stage1 latent。

## 2. 修复与最小闭环证据

远端代码分支：`agent/fix-v714-official-feature-contract`。

- commit `c02531c`：cache builder 读取 checkpoint `run_config.json` 的 `is_causal`；cache metadata 写入 `tokenizer_is_causal`；evaluator/render 按 cache metadata 加载 owning decoder；未知 source、缺失 checkpoint 或 architecture 不一致时 hard fail；增加 cache identity、perturbation 与 single-step eval source；joint-only checkpoint 自动按 `joint_loss` 选择。
- commit `d0be931`：增加 step `1k/3k/5k/10k` immutable snapshots；cache-only perturbation 可显式读取 train z-norm stats。

256 train / 256 val 修正版 smoke cache 与 owning non-causal encoder 的差异只剩 float16 量化：

| tokenizer | latent RMS difference | max absolute difference |
| --- | ---: | ---: |
| joint AE | `5.325e-4` | `0.00390625` |
| joint VAE | `4.508e-4` | `0.007658` |

正确 cache identity 的 pure-256 指标恢复到 Stage1 reconstruction 的合理量级：

| corrected cache identity | FDTMR ↓ | TMR ↑ | HCov ↑ | FDCLaTr ↓ | CLaTr ↑ | CCov ↑ | F1 ↑ | Out ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| joint AE | 52.27 | 16.42 | 100.0% | 1.01 | 70.97 | 100.0% | 0.9320 | 5.39% |
| joint VAE | 81.27 | 15.53 | 99.23% | 3.24 | 69.73 | 100.0% | 0.9154 | 6.28% |

z-norm round-trip 最大误差为 AE `2.38e-7`、VAE `4.77e-7`。显式 normalized perturbation 已在 32-sample smoke 上贯通 owning decoder 与 official metric callbacks。

## 3. “旧 Last + Cache Eval”能判断什么

| check | 能否判断 decoder 修复正确 | 能否判断 Stage2 修复正确 |
| --- | --- | --- |
| 旧 cache → owning decoder identity | 能发现 decoder 选择是否生效，也发现了 cache encoder bug | 不能；cache 本身错误 |
| 旧 last → owning decoder full eval | 只能量化历史两类 bug 叠加后的残余 | 不能；last 在错误 cache 上训练 |
| 新 cache → owning decoder identity | 能验证 encoder/cache/reorder/mask/decoder 闭环 | 不能单独证明 denoiser/sampler |
| 新 cache 训练的新 snapshots → single-step/full sampler | 能 | 能按 denoiser与 sampler 层分解判断 |

因此，旧 last 不删除，但只保留为 forensic artifact。任何“joint tokenizer 不适合 Stage2”或“10k 已足够判死刑”的正式结论，都必须等待修正版 cache 上的新 10k 曲线。

## 4. 核心实验执行顺序

### Gate A：完整 Cache Contract

1. 完成 AE/VAE non-causal full cache：train `162760`、pure val `4053`。
2. metadata 必须包含 `tokenizer_is_causal: false`、checkpoint、preset、feature contract 与 latent order。
3. 各跑 pure-256 cache identity；必须复现本页 smoke 的 Stage1 量级。
4. 分别计算 train valid-frame per-channel z-norm stats，并验证 source cache hash 与 round-trip。

失败则停止，不启动 Stage2。

### Gate B：Tokenizer Local Continuity

对 AE/VAE 在 normalized latent 空间运行 `σ ∈ {0, 0.01, 0.02, 0.05, 0.1}` 的 cache perturbation，各自使用 owning decoder。记录 human、camera、framing 指标随 `σ` 的退化曲线。

若很小 `σ` 已出现灾难退化，优先修 Stage1 latent continuity；不把问题归因于 Stage2 topology。

### Gate C：Corrected Matched 10k

AE/VAE 使用相同 paired train/pure val IDs、width `416`、batch `512`、seed `17`、joint-only、cosine diffusion、学习率 `1e-4` 和 z-norm。保存 step `1k/3k/5k/10k`，按 `joint_loss` 选择 best。

每个 snapshot 补：

- held-out joint loss；
- fixed-`t` single-step predicted `z₀` decode；
- 50-step full sampler official pure-256 metrics；
- 固定 sample renders。

只有 held-out loss 与外部 decode 指标持续改善的分支才允许延长。10k 可作为当前 recipe 的 promotion gate，但不能再用旧 v7.16 曲线判定新 cache。

### Gate D：严格 Official Control 与 Topology

现成 official `pure_` train 只有 `36572`，official mixed cache train 为 `94050`，都不等于 paired train `162760`，不能冒充 matched control。需从同一 paired manifest 生成 official AE latent control，或明确降级为非严格参考。

只有 corrected symmetric baseline 通过后，才执行 human-text camera leakage 修复与 symmetric/asymmetric A/B。separate tokenizer、replay、editing 和更长 full run 继续后置。

## 5. 当前执行状态

- [x] owning decoder 与 cache architecture hard gate
- [x] corrected 256 cache identity
- [x] z-norm / perturbation execution smoke
- [x] task-specific checkpoint selection
- [x] diagnostic snapshots
- [x] full AE/VAE corrected cache build
- [x] same-manifest official AE control cache build
- [x] full-cache identity and perturbation curves
- [x] corrected official/AE/VAE matched 10k
- [x] single-step versus full-sampler decomposition

## 6. Full-Cache Gate Results

三条 full cache 的 train ID 顺序完全一致：`162760` samples，ID-list SHA256 为 `28bb1c70cb184374558a0360935f748117e7754f474edb3ff0b5a9f5b5e33379`。val 都是 `4053` samples，ID-list SHA256 为 `a6414865d9ab330fd559f6cf8a62bab7dc1ce4e4ba0dc4f301194c2c71f0eb21`。

Full-cache z-norm：

| latent | human std mean | camera std mean | all std mean | valid latent frames | round-trip max error |
| --- | ---: | ---: | ---: | ---: | ---: |
| official AE | 0.4626 | 0.7135 | 0.5462 | 4,896,032 | `2.38e-7` |
| joint AE non-causal | 1.1697 | 0.7706 | 1.0367 | 4,896,032 | `2.38e-7` |
| joint VAE non-causal | 1.1769 | 1.2088 | 1.1876 | 4,896,032 | `2.38e-7` |

Owning-decoder identity pure-256：

| latent | FDTMR ↓ | FDCLaTr ↓ | F1 ↑ | Out ↓ |
| --- | ---: | ---: | ---: | ---: |
| official AE | 157.25 | 30.71 | 0.7913 | 2.63% |
| joint AE non-causal | 52.27 | 1.01 | 0.9319 | 5.39% |
| joint VAE non-causal | 81.27 | 3.24 | 0.9154 | 6.28% |

Normalized latent perturbation pure-256：

| latent / σ | FDTMR ↓ | FDCLaTr ↓ | F1 ↑ | Out ↓ |
| --- | ---: | ---: | ---: | ---: |
| official AE / 0 | 166.36 | 30.25 | 0.7921 | 2.66% |
| official AE / .02 | 166.31 | 37.88 | 0.8047 | 2.81% |
| official AE / .05 | 166.43 | 114.11 | 0.6643 | 3.57% |
| joint AE / 0 | 55.18 | 1.10 | 0.9319 | 5.41% |
| joint AE / .02 | 63.94 | 7.91 | 0.8812 | 6.27% |
| joint AE / .05 | 121.11 | 94.14 | 0.4868 | 7.55% |
| joint VAE / 0 | 83.38 | 3.55 | 0.9154 | 6.40% |
| joint VAE / .02 | 101.17 | 14.18 | 0.8258 | 6.53% |
| joint VAE / .05 | 192.72 | 112.45 | 0.4875 | 8.60% |

结论：local latent 的 decoder 邻域比 official control 更脆，VAE 又弱于 AE；但 `σ≤.02` 没有出现 on-manifold identity 向灾难区间的瞬时坍塌，且 local 绝对指标仍优于 official control。因此 continuity 是风险与解释变量，不足以在 denoiser 训练前判死 joint tokenizer。Gate B 通过，进入 corrected matched 10k。

## 7. Corrected Matched 10k Early Curve

official AE 与 joint AE 已使用相同 train/val ID hashes、width `416`、batch `512`、seed `17`、joint-only task、z-norm 和 optimizer 启动。resolved checkpoint selection 都是 `joint_loss`，step `1000` immutable snapshots 已生成。

| latent | step 1k train joint loss | step 1k held-out joint loss |
| --- | ---: | ---: |
| official AE | 0.1636 | 0.1890 |
| joint AE non-causal | 0.2502 | 0.2740 |

corrected joint AE 的 held-out gap 为 official 的约 `1.45×`，明显小于旧错误 cache 曲线在 step 1k 的约三倍差距。这是 cache architecture bug 实质污染 Stage2 learnability 的直接证据。

三条 held-out joint loss 都在 5k 附近最低，10k 回升：

| latent | 1k | 3k | 5k | 10k |
| --- | ---: | ---: | ---: | ---: |
| official AE | 0.1891 | 0.1592 | **0.1552** | 0.1582 |
| joint AE non-causal | 0.2740 | 0.2122 | **0.1840** | 0.1985 |
| joint VAE non-causal | 0.2529 | 0.1913 | **0.1636** | 0.1730 |

因此 10k 足够判断当前 recipe 已进入泛化平台或轻微过拟合，不支持直接延长到 50k/93k。

## 8. Snapshot External Metrics

所有结果使用显式 `--checkpoint`，JSON 内的实际 step 与文件名一致。50-step sampler、pure-256：

| latent / step | FDTMR ↓ | TMR ↑ | HCov ↑ | FDCLaTr ↓ | CLaTr ↑ | CCov ↑ | F1 ↑ | Out ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| official / 1k | 350.30 | 13.58 | 59.1% | 148.63 | 21.87 | 70.0% | 0.262 | 27.0% |
| official / 3k | 342.25 | 14.80 | 67.1% | 177.86 | 21.47 | 70.7% | 0.284 | 17.7% |
| official / 5k | 338.54 | 16.07 | 67.1% | 175.71 | 21.35 | 69.8% | 0.272 | 21.6% |
| official / 10k | **318.30** | **16.76** | **70.6%** | **134.60** | **31.35** | **75.4%** | **0.419** | **10.7%** |
| joint AE / 1k | **524.09** | **11.76** | **51.3%** | **181.29** | **17.63** | **66.5%** | **0.228** | 43.4% |
| joint AE / 3k | 909.32 | 4.00 | 15.6% | 278.17 | 10.86 | 60.2% | 0.114 | **25.9%** |
| joint AE / 5k | 1202.88 | 5.22 | 2.7% | 346.48 | 6.14 | 46.4% | 0.098 | 33.2% |
| joint AE / 10k | 1134.51 | 5.36 | 6.3% | 284.23 | 14.04 | 62.9% | 0.153 | 19.9% |
| joint VAE / 1k | **927.81** | 5.82 | **18.4%** | **172.97** | **16.06** | **67.0%** | **0.166** | **32.4%** |
| joint VAE / 3k | 1222.00 | 5.02 | 2.1% | 292.77 | 12.83 | 57.9% | 0.157 | 33.3% |
| joint VAE / 5k | 1334.86 | 5.44 | 2.0% | 306.86 | 10.28 | 53.3% | 0.165 | 38.3% |
| joint VAE / 10k | 1155.15 | **7.62** | 3.9% | 266.51 | 14.17 | 65.4% | 0.148 | 28.1% |

official external metrics 随训练总体改善；local AE/VAE 则出现 loss 下降而 decoded human manifold 恶化。joint AE 的最佳 external checkpoint 是 1k，不是 loss 最低的 5k；VAE 从 1k 起已经不可用。AE 明确优于 VAE，但当前 local 两条都不通过 Stage2 promotion gate。

## 9. Single-Step Versus Sampler

使用 step-5k checkpoint，在固定 `t` 上执行一次 `q(z_t) → predicted z₀ → owning decoder`：

| latent / t | FDTMR ↓ | HCov ↑ | FDCLaTr ↓ | F1 ↑ | Out ↓ |
| --- | ---: | ---: | ---: | ---: | ---: |
| official / 100 | 173.06 | 98.8% | 65.71 | 0.599 | 4.1% |
| official / 500 | 183.97 | 98.4% | 84.46 | 0.533 | 4.3% |
| official / 900 | 317.07 | 72.7% | 132.96 | 0.398 | 5.1% |
| joint AE / 100 | 646.07 | 55.8% | 184.93 | 0.399 | 16.4% |
| joint AE / 500 | 831.80 | 24.6% | 236.79 | 0.275 | 15.4% |
| joint AE / 900 | 602.77 | 43.9% | 214.48 | 0.211 | 15.4% |
| joint VAE / 100 | 775.02 | 39.0% | 164.02 | 0.342 | 19.6% |
| joint VAE / 500 | 849.29 | 22.7% | 212.17 | 0.247 | 21.1% |
| joint VAE / 900 | 650.46 | 43.8% | 209.07 | 0.177 | 29.6% |

local latent 在低噪声 `t=100` 的单步 predicted `z₀` 已明显离开 human manifold；50-step sampler 又进一步放大误差。根因不是单一 sampler accumulation，而是 **local latent geometry 与当前 START_X/MSE denoising objective 的失配，外加迭代累积**。

## 10. Final Decision and Next Core Experiments

> [!success] 10k 判断边界
> 10k 足够拒绝“当前 non-causal joint AE/VAE + per-channel z-norm + CondMDI START_X/MSE recipe”，也足够停止直接延长与 asymmetric full run。它不足以证明所有 joint tokenizer 天生不适合 Stage2，因为 Stage1 reconstruction、small-noise continuity 和方向性 shuffle evidence 均通过，失败首次出现在 learned single-step predicted `z₀`。

核心实验重新排序：

1. **P0：无长训练的 off-manifold residual audit。** 对 official/local step-5k 的 predicted `z₀-z₀` 比较 branch covariance、Mahalanobis norm、temporal spectrum 与 decoder-sensitive directions；确认 per-channel z-norm 未处理的相关结构。
2. **P0：local AE 线性 geometry control。** human/camera 分支分别做 train-covariance whitening或低秩 prior alignment，decode 前精确逆变换；只跑 1k/3k。若 HCov 曲线恢复，证明问题主要是 latent geometry，而不是 joint representation本身。
3. **P0：prediction-target control。** 在同一 local AE cache 上比较 START_X 与 epsilon/v-style target；仍用 1k/3k external snapshots 作 kill gate。不要先改 topology。
4. **P1：Stage1 diffusion-friendly regularization。** 仅当线性/target controls 给出正信号，再训练 prior-aligned或 noise-regularized joint AE；必须同时守住现有 identity reconstruction。
5. **P1：separate AE。** 作为 representation-entanglement对照，而不是默认替代方案；使用胜出的 Stage2 target。

human-text leakage、symmetric/asymmetric、replay 与 editing 全部继续后置。旧错误-cache human-text checkpoint 不用于正式 leakage 结论；必须在胜出的 diffusion-friendly latent/target contract 上重新训练后再测。
