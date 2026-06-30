---
title: "StoryMotion v6.2 进度与裁决"
status: active
tags:
  - StoryMotion
  - Motion_Generation
  - experiment
  - status/active
aliases:
  - StoryMotion-v6.2
hypothesis: |
  StoryMotion 的核心目标是统一建模 storytelling 分镜中的 human motion 与 camera motion：两者共同决定叙事镜头，但又有可分离的动态规律。复用已验证的 Pulp-style Stage1 只是为了快速推进更核心的 Stage2 joint/completion 生成与可靠性诊断；v6.2 聚焦 human-camera coupling、可靠性错配、Stage1 tokenizer 质量和 Stage2 joint/completion 对比。
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]]"
created: 2026-06-29T00:00:00
updated: 2026-07-01T02:47:56+0800
---
## ICLR Abstract Draft

Storytelling is shaped not only by what a character does, but also by how the camera observes and stages that action. Human motion and camera motion are therefore coupled components of cinematic generation: a camera move should respond to character intent, spatial layout, and framing, while the character motion should remain meaningful even when the camera path changes. Existing motion-generation pipelines often generate these two streams separately, or evaluate camera control only under clean ground-truth human/root observations, leaving the joint storytelling structure under-modeled. We study this problem through StoryMotion, a unified framework for joint human-camera motion generation and completion.

Our key insight is that unified storytelling motion needs both shared structure and modality-specific freedom. Human and camera trajectories are related through framing, distance, viewpoint, and narrative timing, but they are not the same signal and should not be collapsed into a single undifferentiated motion stream. StoryMotion therefore asks whether a shared latent generator can learn cross-modal coordination while preserving the independent dynamics of human action and camera movement. In the current Pulp-style representation, this question becomes especially concrete: the camera latent includes relative distance to the human root, so camera completion can become structurally dependent on the quality of the observed or generated human branch.

StoryMotion treats joint human-camera generation as a modeling and evaluation problem rather than a code-level reuse exercise. The existing Stage1 tokenizer gives a practical starting point for Stage2 experiments, but the motivation is not to reproduce PulpMotion; it is to test whether human motion and camera motion can be generated, completed, and evaluated under one coherent storytelling contract. The current evidence supports a diagnostic conclusion rather than a final SOTA claim: source/quality-aware conditioning, generated-human-aware training, and camera-latent decoupling are necessary to turn unified human-camera generation from a clean-condition benchmark result into a robust generative system.

**ICLR-facing contribution boundary**：可以写成 task / protocol / diagnosis / repair direction；不能写成已经解决 robust human-camera generation，也不能把 tokenizer 收敛写成 Stage2 质量提升。

## 结论摘要

v6.2 是独立裁决版，不依赖读者先读 v6.1。核心更新是：camera reliability mismatch 成立；Stage1 tokenizer reconstruction 与 Stage2 joint/completion 进入统一口径；新 tokenizer 的 Stage2 official callback eval 已进入负面诊断表；E.T./DIRECTOR 只保留 StoryMotion/Pulp metric 下的有效 baseline/replay 结果；MoLingo human-only 与 separate AE no-z Stage2 已完成 5090 metric eval，但都只能作为负面闭环。2026-06-30 进一步确认 mixed-subset 不是单纯 eval 子集，而是旧 camera manifest 限制训练 cache 到 `29779/3279`；2026-07-01 已完成 MoLingo、separate AE no-z、separate VAE with-z 的 full mixed train 与 official eval，补到 `94050/10549` 后仍全部负面。

1. **根因不变**：camera latent 的 distance block 依赖逐帧 human/root world coordinate，`distance_feat = camera_translation - human_translation`；Stage2 又同步 denoise `concat([z_hum,z_cam])`，因此 observed human/root 偏差会不对称地污染 camera completion。
2. **C2 reliability 问题成立**：训练和 eval 中 hard observed replacement 加上 `obs_x0 + obs_mask` 条件，使模型学到 observed branch 完全可信，而不是按 source / quality 动态调信任。
3. **Stage1/Stage2 分口径整理**：Stage1 用 reconstruction/posthoc eval，Stage2 用 official callback 和同 split camera metric。
4. **新 tokenizer Stage2 是负面证据**：separate VAE pure/mixed、separate AE no-z mixed、GRFSQ longtrain pure/mixed、HFSQ pure/mixed 在 tokenizer-cache official eval 中明显劣于既有 StoryMotion/Pulp 行，说明 Stage1 reconstruction 收敛不能自动转化为 Stage2 generation 质量。
5. **E.T./DIRECTOR 不再以 official eval 为目标**：只保留同 split 的 Pulp/StoryMotion Stage2 camera metrics，不使用 DIRECTOR official 假设。

## StoryMotion 核心目标与贡献

这部分不是 ICLR paper 里的正式贡献写法，而是给我自己快速判断 StoryMotion 主线到底在做什么、哪些结果能讲、哪些只是诊断。

**一句话目标**：StoryMotion 想做的不是“复用 PulpMotion”或“再训练一个 text-to-motion 模型”，而是把 human motion 和 camera motion 作为 storytelling 分镜的两个核心运动层放进同一个可控生成闭环里，判断一个 unified latent generator 是否真的能同时学会动作语义、镜头轨迹、跨模态 coupling，以及两种运动各自的独立性。

### 我真正关心的问题

1. **统一生成是否值得做**：storytelling 中镜头与人物动作彼此影响但并不等价；如果 separate / replay / camera-only pipeline 已经很强，unified joint generator 必须证明它不只是更复杂，而是能带来更好的 human-camera consistency、可控性或泛化。
2. **camera 到底依赖什么**：当前 Pulp camera latent 不是纯 camera，它有 `camera_translation - human_translation` 这种 relative-distance contract；所以 camera 质量很可能被 decoded human/root 质量锁死。
3. **退化到底来自哪里**：不能只说“指标差”。要区分是 tokenizer latent 不好、Stage2 denoise 不好、observed branch reliability 不好、generated root condition mismatch，还是 eval protocol 不匹配。
4. **外部 baseline 能不能公平接入**：MoLingo、E.T./DIRECTOR 不能无脑套 HumanML / official setting；只有满足 Pulp 199 维 human contract、camera split contract、同一 metric contract，才算 StoryMotion baseline。
5. **Stage1 复用的边界是什么**：Pulp-style Stage1 是一个已验证的启动点，用来减少表示层不确定性并快速进入 Stage2；它不是 StoryMotion 的核心目标，也不应在 abstract 里被写成主要 novelty。

### 当前可以自信说的贡献

1. **把问题从泛泛的 joint generation 收缩到了具体 contract**：camera branch 的核心脆弱点不是抽象的“camera 难”，而是 relative-distance camera latent 与 human/root condition 强绑定。
2. **建立了同 split / 同 Stage2 / 同 callback 的裁决面**：human completion、camera completion、joint generation、replay baseline、P2a/P2b robustness 都能放在同一张表里比较，不再靠不同项目的数字拼接。
3. **证明了 reliability mismatch 是真实问题**：observed human/root 一旦从 clean GT 变成 noisy、missing 或 generated，camera completion 退化远大于 human completion；这说明 hard observed replacement 学到的是“盲信 observed branch”。
4. **划清了 baseline 边界**：MoLingo 只能作为 Pulp 199 in/out VAE human baseline 重做；E.T./DIRECTOR 只能作为 root-conditioned camera baseline 做 StoryMotion camera metrics，不能把 official HumanML/E.T. 假设直接搬进来。

### 当前不能对外包装成贡献的部分

- 不能说 unified joint generation 已经超过 Pulp stage1 mixed joint；当前 official callback 数字不支持。
- 不能说 tokenizer 收敛等同于 Stage2 质量提升；mixed camera MSE 仍高，更多是 tokenizer 诊断。
- 不能说 MoLingo 是有效 StoryMotion human baseline；它已完成合法 human-only Stage2/cache/eval contract，但 official metrics 明显坍塌。
- 不能说 E.T./DIRECTOR 已完成完整因果诊断；当前只有同 seed17/bs64 的 baseline/replay camera metric，shuffle/swap diagnostics 仍未整理。

### 对我自己的主线判断

StoryMotion 目前最有价值的不是某个单点指标，而是它把“human-camera joint generation 为什么退化”拆成了可验证的工程-表示-条件链条：

`Pulp camera latent contract -> Stage1 tokenizer quality -> Stage2 observed branch reliability -> generated/root condition mismatch -> official callback camera/joint degradation`

下一步如果要继续推进，优先级应是：

1. **generated-human-aware training**：训练时真的喂 generated human/root condition，而不是只留 `generated` 标签位。
2. **camera latent 解耦 ablation**：global camera / root-independent camera representation 必须作为强 ablation，验证 relative-distance contract 是否是硬瓶颈。
3. **Stage2 full eval 闭环**：MoLingo、separate AE no-z、separate VAE with-z 已完成 full mixed official eval；后续 joint GRFSQ 等新 tokenizer / stage2 run 仍必须进入同一 official callback 表，否则只算内部诊断。
4. **baseline adapter 清洁化**：MoLingo、E.T. 先过 Pulp contract，再谈正式 comparison。

## 当前核心裁决

### 已成立

- Stage2 human-camera coupling 的源码根因成立：camera distance 表示显式绑定 human/root。
- Reliability mismatch 成立：observed human/root 一旦变成 noisy、missing 或 generated，camera branch 退化远大于 human branch。
- P2a matched additive-noise 证明 camera completion 是脆弱支路；human completion 对 observed camera noise 相对稳健。
- separate VAE pure、GRFSQ longtrain pure/mixed、HFSQ pure/mixed 的 Stage2 official eval 显著退化，只能作为 tokenizer-to-Stage2 质量传递断裂的诊断证据。

### 未成立

- 不能声称 P2b 已解决 StoryMotion Stage2 coupling。
- 不能声称 MoLingo 是有效 human baseline；它已有合法 StoryMotion train/eval 结果，但指标坍塌。
- 不能声称 E.T./DIRECTOR 已完成完整因果诊断；当前只有 baseline/replay camera metric，shuffle-based diagnostics 仍未整理。
- 不能把 camera global-position 版本设为默认；默认版本仍是 Pulp 原生 relative-distance camera latent。
- 不能把 separate VAE / GRFSQ / HFSQ Stage2 写成 promoted baseline；当前 official callback 指标不支持。

## Settings 与操作解释

| Setting                 | 核心目标                                                        | 核心实现 / 操作                                                                                                                                                 | 裁决                          |
| ----------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| SM-relative default     | 主 StoryMotion 对照；保持 Pulp 原始 tokenizer contract              | human latent 128 + camera relative-distance latent 64；camera decode 时由 `distance_feat + human/root` 还原 world camera                                       | 默认版本；公平但暴露 root 依赖          |
| SM-global-pos variant   | 验证 camera 直接预测 global position 是否能减少 human/root 硬依赖         | git copy 当前 v6.2 文档与代码状态后另起 variant；camera latent/cache 使用 global camera translation 或 global-position branch，不替换默认 relative-distance 版本                  | 待实验；只能作为 ablation           |
| P2a matched noise       | 定量证明 observed branch reliability 问题                         | 对 clean observed human/root 加 matched additive noise，评估 camera completion 退化斜率                                                                            | camera 是脆弱支路                |
| E.T. root-only adapter  | 外部 camera completion baseline                               | Pulp `caption_cam` + `smpl_raw["transl"] -> (T,3)` root condition + camera trajectory target；不使用 full SMPL/mesh；只跑 Pulp/StoryMotion Stage2 camera metrics | baseline/replay eval 完成；shuffle 诊断待整理 |
| MoLingo VAE adapter     | StoryMotion human completion baseline 的外部 human VAE 路线      | Pulp 199 in/out contract；human-only Stage2 已在 5090 GPU0 完成，`bs512`、`seed17` | official eval 完成但指标坍塌；不 promoted |

## 数据总表

### Stage1 全量 reconstruction / posthoc eval

这里分两种口径：GT/Pulp 是 official callback 或 identity/reference 口径；separate VAE/GRFSQ/HFSQ 是 Stage1 tokenizer reconstruction/posthoc 口径。Stage1 表只写 reconstruction metric，不把训练 loss 当成主指标；joint MSE 是 paired human-camera reconstruction MSE，即 human MSE 与 camera MSE 的平均。

#### GT / Pulp official callback reference

| model | split | task | samples | FDTMR↓ | TMR↑ | FDCLaTr↓ | CLaTr↑ | caption F1↑ | 口径 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| GT human | mixed | human | 10549 | 0.00 | 17.71 | - | - | - | full mixed GT-human TMR reference |
| Pulp Stage1 | pure | joint | 4053 | 109.34 | 15.94 | 17.66 | 60.53 | 0.776 | official autoencoder upper bound |
| Pulp Stage1 | mixed | joint | 10549 | 124.46 | 18.17 | 15.51 | 58.10 | 0.670 | official autoencoder upper bound |


### Stage2 joint / completion 对比

#### Official callback rows

| model | split | mode | samples | FDTMR↓ | TMR↑ | FDCLaTr↓ | CLaTr↑ | caption F1↑ | root in-frame↑ |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| GT human | mixed | human reference | 10549 | 0.00 | 17.71 | - | - | - | - |
| PulpMotion Stage2 | pure | joint/generation | 4053 | 419.24 | 21.69 | 90.62 | 38.90 | 0.520 | - |
| PulpMotion Stage2 | mixed | joint/generation | 10549 | 426.21 | 24.87 | 80.20 | 32.84 | 0.364 | - |
| StoryMotion v6 | pure | unified joint | 4053 | 137.12 | 21.25 | 91.47 | 44.46 | 0.594 | - |
| StoryMotion v6 | mixed | unified human | 10549 | 126.71 | 18.17 | - | - | - | - |
| StoryMotion v6 | mixed | unified camera | 10549 | - | - | 14.50 | 54.85 | 0.638 | - |
| StoryMotion v6 | mixed | unified joint | 10549 | 155.73 | 23.95 | 85.70 | 33.52 | 0.374 | - |
| E.T./DIRECTOR | mixed | camera completion, GT/root condition, seed17 | 10549 | - | - | 14.51 | 54.84 | 0.64 | 0.81 |
| E.T./DIRECTOR | mixed | camera replay, generated-human condition, seed17 | 10549 | - | - | 92.24 | 33.31 | 0.37 | 0.27 |

**Stage2 裁决**：clean GT/root camera completion 可以看起来很强，但 generated-human replay 明显退化；这支持 reliability mismatch，而不是支持“统一 joint generator 已解决 camera generation”。Pure/mixed 必须分开看：pure 上 StoryMotion human-side latent/full eval 较干净，mixed 上 camera/root condition mismatch 是主风险。

#### Completed tokenizer-cache official eval

口径说明：下表基于 tokenizer-cache validation 子集评估，pure 为 `4053` samples，mixed 为 `3279` samples；统一使用 `batch_size=64`、`seed=17`。它用于判断新 tokenizer 进入 Stage2 后的退化趋势，不与 full `10549` mixed official rows 做精确数值对比。

##### Pure split

| model | mode | samples | FDTMR↓ | TMR↑ | FDCLaTr↓ | CLaTr↑ | caption F1↑ | root in-frame↑ | outscreen↓ | 裁决 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| separate VAE Stage2 | human completion | 4053 | 2012.64 | 0.00 | - | - | - | 0.11 | - | human-side official metric 明显退化 |
| separate VAE Stage2 | camera completion | 4053 | - | - | 581.95 | 9.14 | 0.02 | 0.11 | - | camera completion 不可 promoted |
| separate VAE Stage2 | joint/generation | 4053 | 2018.62 | 0.00 | 586.65 | 8.47 | 0.02 | 0.11 | 1.00 | 负面诊断 |
| separate GRFSQ longtrain Stage2 | human completion | 4053 | 1816.87 | 3.94 | - | - | - | 0.16 | - | human-side official metric 明显退化 |
| separate GRFSQ longtrain Stage2 | camera completion | 4053 | - | - | 832.14 | 11.45 | 0.07 | 0.15 | - | camera completion 不可 promoted |
| separate GRFSQ longtrain Stage2 | joint/generation | 4053 | 1803.40 | 3.88 | 818.95 | 11.26 | 0.07 | 0.15 | 0.76 | 负面诊断 |
| separate HFSQ Stage2 | human completion | 4053 | 2106.54 | 4.54 | - | - | - | 0.15 | - | human-side official metric 明显退化 |
| separate HFSQ Stage2 | camera completion | 4053 | - | - | 596.14 | 10.15 | 0.08 | 0.15 | - | camera completion 不可 promoted |
| separate HFSQ Stage2 | joint/generation | 4053 | 2100.08 | 4.51 | 581.47 | 9.90 | 0.08 | 0.15 | 0.79 | 负面诊断 |

##### Mixed split

| model | mode | samples | FDTMR↓ | TMR↑ | FDCLaTr↓ | CLaTr↑ | caption F1↑ | root in-frame↑ | outscreen↓ | 裁决 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| separate VAE with-z Stage2 | human completion | 3279 | 1274.72 | 7.08 | - | - | - | - | - | v6.2 human-global camera run；human-side 仍弱 |
| separate VAE with-z Stage2 | camera completion | 3279 | - | - | 118.77 | 38.08 | 0.47 | - | - | 已完成 official callback；弱于 Stage1 upper bound |
| separate VAE with-z Stage2 | joint/generation | 3279 | 1316.47 | 6.89 | 133.95 | 32.55 | 0.41 | - | - | 已完成但不构成提升 |
| separate GRFSQ longtrain Stage2 | human completion | 3279 | 1704.87 | 4.62 | - | - | - | 0.25 | - | 弱于既有 StoryMotion official rows |
| separate GRFSQ longtrain Stage2 | camera completion | 3279 | - | - | 589.93 | 19.54 | 0.12 | 0.24 | - | camera metric 仍明显退化 |
| separate GRFSQ longtrain Stage2 | joint/generation | 3279 | 1678.85 | 4.54 | 570.49 | 19.03 | 0.12 | 0.23 | 0.40 | 负面诊断 |
| separate HFSQ Stage2 | human completion | 3279 | 2245.73 | 7.77 | - | - | - | 0.22 | - | human-side official metric 明显退化 |
| separate HFSQ Stage2 | camera completion | 3279 | - | - | 783.52 | 21.11 | 0.11 | 0.22 | - | mixed camera 更弱 |
| separate HFSQ Stage2 | joint/generation | 3279 | 2235.91 | 7.74 | 770.02 | 21.13 | 0.12 | 0.22 | 0.66 | 负面诊断 |

**新 Stage2 裁决**：separate VAE pure、separate VAE mixed with-z、separate GRFSQ longtrain pure/mixed、separate HFSQ pure/mixed 的 Stage2 official callback 指标均远离既有 PulpMotion / StoryMotion / E.T. 有效行；它们证明 tokenizer-cache 可训练完成不等于下游 generation 可用。当前应把这些结果写成 tokenizer quality threshold 与 Stage2 传递风险，而不是新 baseline。separate VAE mixed with-z 的训练、official callback、TensorBoard 与可定位 run 目录已经完成；旧 no-z mixed 只有 `v5_stage1_separate_noz_cache_20260622/vae_mixed` cache，未找到匹配的 separate-no-z Stage2 generator checkpoint。

### P2a matched additive-noise

该表来自 v6.1 中已整理的 unified neutral bs64 eval。clean 行取 P0。

| observed noise std | camera FDCLaTr↓ | camera CLaTr↑ | camera CCov↑ | human FDTMR↓ | human TMR↑ | human HCov↑ |
| -----------------: | --------------: | ------------: | -----------: | -----------: | ---------: | ----------: |
|               0.00 |            14.8 |          55.6 |        0.866 |        126.7 |      18.17 |       0.846 |
|               0.05 |            22.0 |          53.2 |        0.856 |        126.7 |      18.13 |       0.845 |
|               0.10 |            51.9 |          48.7 |        0.802 |        126.6 |      18.02 |       0.845 |
|               0.15 |            96.9 |          43.5 |        0.701 |        126.9 |      17.83 |       0.842 |
|               0.30 |           216.8 |          33.0 |        0.467 |        131.7 |      16.85 |       0.811 |
|               0.50 |           303.0 |          25.7 |        0.310 |        154.7 |      14.94 |       0.729 |

**读数**：observed human/root 噪声从 0 到 0.15 时，camera FDCLaTr 从约 `14.8` 升到约 `96.9`；human completion 在 observed camera noise 下基本稳定。这是 P2b 聚焦 camera reliability 的直接证据。

## MoLingo 状态

MoLingo 只接受 Pulp `smpl_rifke` 199 维 in/out contract 下重新训练和评估的结果。

2026-06-30 复查结论：历史 MoLingo human completion baseline 没有完成合法 StoryMotion Stage2 generator/cache contract。已在 5090 GPU0 补跑完成，配置为 `batch_size=512`、`seed=17`、`task_probs 0 1 0`，只训练 human completion；run 为 `runs/train/stage2/v6_2_molingo_human_seed17_20260630/human_only_b512`，cache 为 `runs/train/stage2/v6_2_molingo_human_seed17_cache_20260630/mixed_noz`。训练完成到 `50000/50000` step，最终 train loss 约 `0.01079`；official callback eval 覆盖 mixed-subset `3279` samples，FDTMR `2353.96`、TMR `4.466`、HCov `0.1%`、MPJPE `0.342`。

边界：这是 MoLingo human-only baseline，不是 camera 或 joint baseline。MoLingo 单路径 199D VAE 不能直接伪装成 192D human-camera joint tokenizer；当前采用的是已有 separate MoLingo VAE paired Stage1 checkpoint + human-only Stage2 的合法替代路径。完成结果很弱，只能写作“外部 human baseline 适配失败/负面闭环”，不能 promoted。

## PulpMotion Stage1 ablation 状态

2026-06-30 新增两个 Stage1 ablation，目标是回答 Pulp Stage2 的优势是否来自 Stage1 的联合表示，而不是来自 Stage2 本身：

| ablation | 机器/GPU | run | 当前状态 | 目的 |
| --- | --- | --- | --- | --- |
| Pulp separate AE no-z | 5090 GPU1 | `runs/train/stage1/separate/separate_ae_noz_mixed_bs128_seed17_500ep_gpu1_20260630` | Stage1 完成并完成 posthoc eval；best=last step `116500` | 去掉 KL/采样，只把 joint AE 改成 separate AE，隔离“联合表示 vs separate 表示” |
| Pulp joint VAE with-z KL | 5090 GPU1 | `runs/train/stage1/joint/joint_vae_wz_mixed_bs128_seed17_500ep_gpu1_20260630` | Stage1 完成并完成 posthoc eval；best step `110000`，last step `116500` | 在 Pulp human-camera joint Stage1 上加入与 VAE 相同量级的 `kl_weight=1e-5`，测试 KL 是否破坏/改善 Stage2 latent |

| ablation | ckpt | samples | total loss↓ | human MSE↓ | camera MSE↓ | KL loss | 当前读数 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pulp separate AE no-z | best_top1 / last | 3279 | 0.002174 | 0.001469 | 0.000933 | - | deterministic separate AE 没有坏；camera recon 接近 separate VAE no-z mixed |
| Pulp joint VAE with-z KL | best_top1 | 3279 | 0.007822 | 0.003893 | 0.008252 | 3.689679 | KL joint 版本 Stage1 recon 明显变差，不能直接当作更好 tokenizer |
| Pulp joint VAE with-z KL | last | 3279 | 0.007844 | 0.003877 | 0.008260 | 3.894135 | last 与 best 接近；KL 没有自动带来可用生成能力 |

separate AE no-z 已完成 Stage2：cache 为 `runs/train/stage2/v6_2_separate_ae_noz_seed17_cache_20260630/mixed_noz`，Stage2 run 为 `runs/train/stage2/v6_2_separate_ae_noz_seed17_20260630/mixed_b512`，5090 GPU1，`batch_size=512`，`seed=17`，`task_probs 1 1 1`。训练完成到 `50000/50000` step，最终 train loss 约 `0.05774`；official callback eval 覆盖 mixed-subset `3279` samples：human FDTMR `2018.28`、TMR `4.450`、HCov `0.1%`；camera FDCLaTr `623.87`、CLaTr `8.476`、CCov `0.8%`、F1 `0.074`；joint FDTMR `2031.69`、FDCLaTr `583.11`、Out `93.7%`。

当前根因判断：separate VAE / AE Stage2 很差，不优先解释成 eval bug。理由是 mixed with-z VAE 和 deterministic separate AE no-z 都已经用 source-tokenizer-aware official callback 跑完；Stage1 reconstruction 可以很强，但 Stage2 joint/camera 没保住 upper bound。这更像 Stage2 在新 latent geometry 上的分布学习和 human-camera coupling 迁移失败。Pulp 的非生成式 Stage1 反而好，是因为它的 latent 是 Stage2 原生训练/eval contract：确定性、联合编码、latent 分布稳定，且 camera branch 的 relative-distance contract 与 human/root 条件在同一个 encoder-decoder 中被共同组织。VAE 的 KL/采样会把 latent 推向 prior-friendly，但不保证对 diffusion Stage2 更友好；AE 去掉 KL/采样后仍失败，说明问题不只在 KL。

给 Pulp joint Stage1 加 KL 只能让训练目标“VAE-like”：有均值/方差参数化、KL 正则和可采样 latent。它不会自动变成高质量生成模型，也不会自动让 Stage2 更好。是否有帮助要看三个指标链：Stage1 recon 是否下降、latent 分布是否更平滑、Stage2 official callback 是否提升。

### Stage1 official metric eval 补充

loss/MSE 只作为辅助诊断，主对比补充为 frozen Stage1 reconstruction 的 official callback metrics。no-z camera/joint 行使用 GT-z passthrough diagnostic，因此可读 camera semantic/framing upper bound，但不能说明 tokenizer 自己学会 z-depth。

| tokenizer | split | samples | task | FDTMR↓ | TMR↑ | FDCLaTr↓ | CLaTr↑ | caption F1↑ | outscreen↓ | 读数 |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| separate AE no-z | mixed-subset | 3279 | joint | 1360.39 | 10.524 | 2.71 | 66.26 | 0.878 | 20.3% | strongest Stage1 upper bound; Stage2 still fails |
| separate VAE with-z | mixed-subset | 3279 | joint | 1364.23 | 10.505 | 4.75 | 64.87 | 0.842 | 20.0% | strong Stage1, weak Stage2 |
| MoLingo VAE no-z | mixed-subset | 3279 | joint | 1366.94 | 10.409 | 11.51 | 63.85 | 0.813 | 20.5% | Stage1 ok, human-only Stage2 fails |
| HFSQ wscale no-z | mixed-subset | 3279 | joint | 1467.92 | 6.690 | 67.60 | 47.73 | 0.585 | 18.9% | quantized recon weaker |
| GRFSQ bs128 no-z | mixed-subset | 3279 | joint | 1359.42 | 8.309 | 140.01 | 45.10 | 0.592 | 19.8% | camera upper bound weak |

证据路径：`stage2/metrics/v6_2_stage1_official_recon_20260630` 和 `stage2/metrics/v6_2_separate_humanglobal_20260630/stage1_separate_vae_wz_mixed_*official_recon*.json`。

### mixed-subset 纠偏

2026-06-30 复查确认：mixed-subset 不是只在 eval 阶段少了 formal test，而是旧 paired camera manifest 只包含 `29779/3279`，导致 Stage1 paired training、Stage2 cache、Stage2 train/eval 全部落在 subset。full mixed human 的 `94050/10549` sample 实际都有 `traj` 与 `intrinsics` camera 文件；已新增 full camera manifest：

- `runs/train/stage1/manifests/agent2_pulpmotion_camera_mixed_train_manifest_full_20260630.jsonl`：`94050`
- `runs/train/stage1/manifests/agent2_pulpmotion_camera_mixed_test_manifest_full_20260630.jsonl`：`10549`

5090 上 MoLingo human-only、separate AE no-z、separate VAE with-z 的 full-cache/full-train 与 full mixed official eval 已完成：

| run | GPU | status |
| --- | ---: | --- |
| separate AE no-z full | 5090 GPU0 | train + full official eval 完成；negative |
| separate VAE with-z full | 5090 GPU1 | train + full official eval 完成；negative |
| MoLingo human-only full | 5090 GPU2 | train + full official eval 完成；negative |

指标数据独立存储在 [[2026-07-01_storymotion-v6.2-metric-data]]：

![[2026-07-01_storymotion-v6.2-metric-data#Full Mixed Official Eval 2026-07-01]]

日志路径：`logs/v6_2_fulltrain_20260630`；full official eval 路径：`stage2/metrics/v6_2_fulltrain_eval_20260701`。旧 mixed-subset rows 保留为早期/不公平对照，不能与 full mixed `10549` official rows 直接宣称胜负。4090 GPU1 的 joint GRFSQ full 仍未纳入本轮闭环。

### Stage1 visualization

已生成 unified Stage1 tokenizer reconstruction 可视化：`runs/visualizations/stage1_tokenizers_20260630/manifest.json`。覆盖 `4` 个 mixed-test sample、`5` 个 tokenizer：`separate_ae_noz`、`separate_vae_wz`、`separate_hfsq_wscale_noz`、`separate_grfsq_bs128_noz`、`molingo_vae_noz`。每个 sample/model 有 `fixed_camera.mp4`、`orbiting_camera.mp4`、`camera_trajectory.mp4` 和 `rifke_joints_projection.npz`，总计 `73` 个文件。

## E.T./DIRECTOR 状态

### 已完成

- 5090 隔离 clone 已建立：`/data/public/ripemangobox/Motion/baselines/DIRECTOR_storymotion_20260626`
- Pulp data view 已建立：`/data/public/ripemangobox/Motion/baselines/data/director_pulp_mixed`
- root-only camera completion adapter 训练 ckpt 已完成，包括 original、caption shuffle、char shuffle。
- 该 adapter 的 human condition 只使用 `smpl_raw["transl"]` 导出的 `(T,3)` root / center trajectory，不是 full character mesh 或 original E.T. reproduction。
- 2026-06-30 GPU3/GPU2 已完成 StoryMotion/Pulp camera metric seed17 rerun：GT/root condition baseline 与 generated-human replay 都有 full mixed `10549` samples，`batch_size=64`、`seed=17`、`noise_seed=17`。

### 未完成

- caption-shuffle、char/root-shuffle 的同 split 诊断还没有整理进正式对照表。
- 不进行 E.T./DIRECTOR official eval；因此不需要 `checkpoints/clatr-e100.ckpt`，也不需要用 Pulp split CLaTr checkpoint 强行替代。

**正式表述**：E.T./DIRECTOR-inspired root-only camera completion adapter training and StoryMotion/Pulp camera baseline/replay eval are completed; shuffle-based causal diagnostics are still pending.

### E.T. 适配复查

E.T. 不能做“无脑数据替换”。必须满足以下 contract 才能写成 StoryMotion baseline：

1. **输入 contract**：`char` / `char_raw` 只来自 Pulp `smpl_raw["transl"]` 派生的 `(T,3)` root / center trajectory，并记录是否 world coordinate、是否 centered、是否与 camera trajectory 同帧率同长度。
2. **输出 contract**：输出是 camera trajectory，不是 full character-camera generation；若只预测 translation，就不能声称恢复 camera rotation / full 6-DoF。
3. **文本 contract**：camera text 优先 `caption_cam`；human text 只能作为可选条件或诊断，不应混成 original E.T. character-aware full setting。
4. **metric contract**：本项目只采用 Pulp/StoryMotion Stage2 camera metrics；它不是 E.T. official eval，也不需要 E.T. official CLaTr checkpoint。
5. **诊断 contract**：至少跑 original、caption shuffle、char/root shuffle 或 fixed-caption/fixed-root，证明模型真的使用 camera text 与 human root 条件。

## 进度状态

| 模块                      | 状态               | 当前裁决                                             |
| ----------------------- | ---------------- | ------------------------------------------------ |
| C1 源码根因                 | 完成               | camera latent 硬依赖 decoded human/root             |
| C2 reliability          | 完成               | observed branch 被训练成完全可信                         |
| P2a matched noise       | 完成               | camera 对 observed human/root noise 极敏感           |
| Stage1 tokenizer full eval | 完成 | VAE reconstruction 最强；GRFSQ/HFSQ mixed camera 质量不足 |
| Stage2 tokenizer-cache official eval | 完成 | VAE/GRFSQ/HFSQ separate rows 只保留为负面诊断 |
| Stage2 full mixed official eval | 完成 | MoLingo、separate AE no-z、separate VAE with-z 均仍为负面；4090 GPU1 joint GRFSQ full 除外 |
| SM-global-pos variant   | Stage1 已启动       | 只作 ablation；默认仍是 relative distance               |
| MoLingo VAE             | Stage2 human-only training + official eval 完成 | FDTMR `2353.96`、HCov `0.1%`；只作负面 external human baseline |
| Pulp separate AE no-z ablation | Stage1 + Stage2 + official eval 完成 | Stage1 recon 可接受，但 Stage2 human/camera/joint 坍塌，只作负面诊断 |
| Pulp joint VAE KL ablation | Stage1 + posthoc eval 完成 | mixed camera MSE `0.008252`；KL joint 版本 Stage1 明显弱于 AE/VAE no-z |
| E.T./DIRECTOR           | seed17 baseline/replay eval 完成 | shuffle causal diagnostics 待整理                  |

### 2026-06-30 新完成 eval

| 实验                                             | 样本    | 状态  | 当前裁决                                               |
| ---------------------------------------------- | ----- | --- | -------------------------------------------------- |
| separate VAE pure Stage2 official callback     | 4053  | 完成  | pure joint/camera 均明显退化，只作负面诊断                     |
| separate VAE mixed with-z Stage2 official callback | 3279 | 完成 | 5090 `v6_2_separate_vae_wz_seed17_20260630/mixed_b512`；official callback 与 TensorBoard 已同步候选 |
| GRFSQ longtrain pure Stage2 official callback  | 4053  | 完成  | pure joint/camera 均明显退化，只作负面诊断                     |
| GRFSQ longtrain mixed Stage2 official callback | 3279  | 完成  | 弱于既有有效 StoryMotion/Pulp 行，只作负面诊断                   |
| HFSQ pure Stage2 official callback             | 4053  | 完成  | joint/camera 均明显退化，只作负面诊断                          |
| HFSQ mixed Stage2 official callback            | 3279  | 完成  | mixed camera 与 joint 退化更明显                         |
| E.T./DIRECTOR camera baseline seed17           | 10549 | 完成  | clean GT/root condition camera metric 仍强           |
| E.T./DIRECTOR generated-human replay seed17    | 10549 | 完成  | replay 退化明显，支持 reliability mismatch                |
| MoLingo human-only Stage2 official callback    | 3279  | 完成 | FDTMR `2353.96`、TMR `4.466`、HCov `0.1%`；合法但很弱，不 promoted |
| Pulp separate AE no-z Stage1 ablation          | 3279  | 完成 | total `0.002174`，human MSE `0.001469`，camera MSE `0.000933`；metadata/TensorBoard/eval JSON 已同步到 4090，不同步 ckpt |
| Pulp joint VAE KL Stage1 ablation              | 3279  | 完成 | best total `0.007822`，human MSE `0.003893`，camera MSE `0.008252`；metadata/TensorBoard/eval JSON 已同步到 4090，不同步 ckpt |
| Pulp separate AE no-z Stage2 official callback | 3279  | 完成 | human FDTMR `2018.28`；camera FDCLaTr `623.87`；joint Out `93.7%`；负面诊断 |
| MoLingo human-only full mixed official callback | 10549 | 完成 | FDTMR `2396.07`、TMR `4.112`、HCov `0.04%`；full train 仍失败 |
| Pulp separate AE no-z full mixed official callback | 10549 | 完成 | human FDTMR `2147.78`；camera FDCLaTr `676.56`；joint Out `95.5%`；负面诊断 |
| separate VAE with-z full mixed official callback | 10549 | 完成 | human FDTMR `1823.40`、TMR `0.000`；joint FDCLaTr `885.36`、Out `99.0%`；负面诊断 |

**读数边界**：这些完成状态只说明 official callback eval 产物齐全。它们支持 tokenizer-to-Stage2 质量传递风险，不支持 promoted baseline 或 SOTA claim。

## 下一步

1. **结构性解耦应成为主线候选**：重定义 camera latent，减少 `camera_translation - human_root_translation` 的硬绑定；或显式拆成 `human/root -> camera` 的因子化模型。
2. **generated-human-aware training 才能继续 reliability 路线**：训练时真实喂 generated human/root condition，而不是只设置 reserved label。
3. **E.T. baseline 只走 StoryMotion 路径**：用 Pulp/StoryMotion Stage2 camera metrics 整理 original 与 shuffle/swap 诊断；不再等待 official E.T. CLaTr。
4. **MoLingo 暂停 promoted baseline 叙事**：合法 human-only eval 已完成但明显失败；除非重做 adapter/训练目标，否则不再作为有效 human baseline。
5. **global camera Stage1 只作 ablation**：该 run 不改变默认 relative-distance StoryMotion setting。

## 证据路径

- v6.1 整理源文档：`obsidian-vault/ideas/StoryMotion/2026-06-25_storymotion-v6.1.md`
- DIRECTOR adapted clone：`/data/public/ripemangobox/Motion/baselines/DIRECTOR_storymotion_20260626`
- DIRECTOR Pulp data view：`/data/public/ripemangobox/Motion/baselines/data/director_pulp_mixed`
- Global camera Stage1 ablation：`/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage1/stage1_global_camera_c2w_rot6d_vae_500ep_gpu0_20260629`
- 4090 GRFSQ longtrain Stage1 pure：`/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage1/separate/longtrain_separate_grfsq_noz_pure_500ep_gpu0_20260629`
- 4090 GRFSQ longtrain Stage1 eval：`/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_resume_20260629/grfsq_longtrain_stage1_eval`
- Stage1 separate tokenizer legacy eval：`/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage1/separate_5090_v5_20260622/summary.json`
- Stage2 joint/completion official comparison：`/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_resume_20260629/core_eval_comparison_with_gt_pulp_et_molingo_20260629.json`
- 2026-06-30 seed17 bs64 VAE/GRFSQ/HFSQ/E.T. official eval：`/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_seed17_eval_20260630`
- 2026-06-30 separate VAE mixed with-z Stage2：`/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v6_2_separate_vae_wz_seed17_20260630/mixed_b512`
- 2026-06-30 separate VAE mixed no-z cache-only evidence：`/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v5_stage1_separate_noz_cache_20260622/vae_mixed`
- 2026-06-30 MoLingo Stage1-only evidence：`/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage1/molingo_pulp199_vae_mixed_500ep_gpu1_20260629b`
- 2026-06-30 MoLingo human-only Stage2 run：`/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v6_2_molingo_human_seed17_20260630/human_only_b512`
- 2026-06-30 MoLingo human-only Stage2 cache：`/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v6_2_molingo_human_seed17_cache_20260630/mixed_noz`
- 2026-06-30 Pulp separate AE no-z Stage1 ablation：`/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage1/separate/separate_ae_noz_mixed_bs128_seed17_500ep_gpu1_20260630`
- 2026-06-30 Pulp joint VAE KL Stage1 ablation：`/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage1/joint/joint_vae_wz_mixed_bs128_seed17_500ep_gpu1_20260630`
- 2026-06-30 Pulp Stage1 ablation posthoc eval：`/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_resume_20260629/pulp_stage1_ablation_eval`
- 2026-06-30 Pulp separate AE no-z Stage2 cache：`/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v6_2_separate_ae_noz_seed17_cache_20260630/mixed_noz`
- 2026-06-30 Pulp separate AE no-z Stage2 training：`/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v6_2_separate_ae_noz_seed17_20260630/mixed_b512`
- 2026-06-30 MoLingo + separate AE final official eval：`/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_final_eval_20260630`
- 2026-06-30 分类比较总表：[[2026-06-30_storymotion-experiment-metric-comparison]]
- 2026-07-01 full mixed metric data：[[2026-07-01_storymotion-v6.2-metric-data]]
- 2026-07-01 full mixed official eval：`/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_fulltrain_eval_20260701`

2026-07-01 02:47 CST 已补充 full mixed train/eval 完成状态、独立 metric data note 和两个结论页的 Obsidian 嵌入引用。仍需补的是 E.T./DIRECTOR shuffle/swap causal diagnostics 的正式整理，以及 4090 GPU1 joint GRFSQ full 完成后的同口径 metric eval。
