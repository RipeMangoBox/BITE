---
title: "MoDiffDec Revised Plan 2026-06-17"
status: active
hypothesis: "The current gap is dominated by target-space from-scratch RF quality, loss/evaluation mismatch, and missing pretrained target-space prior; strict PiD adaptation should keep RF in motion target space and use SAE/VAE latent only as condition."
created: 2026-06-17T23:20:00+08:00
updated: 2026-06-18T15:35:00+08:00
tags:
  - MoDiffDec
  - research_plan
  - diagnostic
source_papers:
  - "[[analysis/arxiv_2026/PiD_Fast_and_High-Resolution_Latent_Decoding_with_Pixel_Diffusion.md|PiD]]"
  - "[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation.md|MoLingo]]"
  - "[[analysis/ICLR_2026/COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High_Quality_Text_to_Motion_Generation.md|COME]]"
---

# MoDiffDec Revised Plan 2026-06-17

## 0. 结论先行

旧方案把失败主要归因到“feature-space loss 与 MPJPE 不一致”和“模型不够大”。现在要修正：

1. **P0 代码事实**：当前 auxiliary loss 的 `x0_pred` 公式错了。现有 RF 定义为 `x_t = t*x0 + (1-t)*eps`、`v = x0 - eps`，因此 clean-motion 估计应为 `x0_hat = x_t + (1-t)*v_pred`。旧代码用 `x_t - t*v_pred`，若 `v_pred` 正确，该式等于 `eps`，会把噪声的高通和速度强行对齐到真实 motion。
2. **P1 监督错位**：feature-space flow MSE 不能保证 joint-space MPJPE 好，尤其 272D 表示经非线性恢复到关节坐标后误差会被放大。
3. **P1 PiD 适配不完整**：PiD 的 RF/扩散目标在输出空间，latent 是条件。当前 MoDiffDec 这一点与 PiD 方向一致，但它从零训练 raw-motion RF transformer，没有 target-space pretrained motion prior，也没有 text prior 接入，因此不能声称忠实复现 PiD 的质量来源。
4. **低优先级假设**：MoLingo SAE 的 motion-text alignment 不足不能解释当前纯 reconstruction 差距，因为 CNN baseline 使用相同 SAE latent 仍达约 10 mm。

## 1. 已验证事实

- 远端代码：`/data/public/ripemangobox/Motion/MoLingo/mogen/models/motion_diff_decoder/` 与 `mogen/train_diff_decoder.py`。
- 当前 output space：normalized 272D HumanML3D raw motion features。
- 当前 condition：frozen SAE encoder latent `z [B,T/4,32]`，经 noise latent conditioning 和 sigma-aware gate 注入。
- Stage 1 不使用 text condition：`decoder(x_t, t, None, z_sigma, sigma)`。
- CNN SAE decoder baseline：MPJPE 约 10.0 mm。
- MoDiffDec 最佳：D1_v6 约 29.4 mm；D6 E200 约 30.2 mm；16/32/50 sampling steps 几乎无差异。
- D6 仍在 `traind6_gpu1` 训练中；E200 暂不支持“扩大模型即可解决”的判断。

## 2. 对用户四个怀疑的更新判断

| 怀疑点 | 当前判断 | 证据强度 | 行动 |
|---|---|---:|---|
| A. raw motion space vs latent rep | 当前实现确实是在 raw 272D feature space 做 RF；这符合 PiD 的 target-space RF 形式，但缺 pretrained prior。 | 中 | 主线做 SAE-conditioned raw RF + unconditioned control；latent-space RF 只作 LDM baseline。 |
| B. SAE motion-text alignment 不足 | 不能解释 Stage 1 reconstruction 差距。当前没有 text condition，CNN baseline 也用同一 SAE latent。 | 强反证 | 暂不作为 P0。 |
| C. VAE 是否更好 | 可作为后续变量。VAE latent 可能更 Gaussian，MoLingo 论文也显示 VAE FID 略优，但不能解释 29 mm vs 10 mm。 | 弱到中 | T0/T1 后再做。 |
| D. 不忠实 PiD 适配 | 是核心问题之一。当前缺 target-space pretrained diffusion prior，也没有 text prior。 | 强 | 方案中明确降级当前路线；只有接入 raw-space prior 才能称为 PiD-style adaptation。 |

## 3. 新路线

### Phase A: 修正当前实现并得到干净基线

目标：先确认当前失败是否被 auxiliary-target bug 放大。

- 修复 `decoder_trainer.py` 中 auxiliary loss 的 clean estimate：
  ```python
  x0_pred = x_t + (1 - t).view(-1, 1, 1) * v_pred
  ```
- 保持 D1_v6 其他设置不变：`p_clean=0.1`、`freq_loss_weight=0.3`、`velocity_loss_weight=0.1`。
- 重跑 T0，不再扩 D6/D7。
- 成功阈值：T0 MPJPE ≤ 20 mm 说明 bug 是重大贡献因素；若仍 > 25 mm，说明缺 joint loss / 缺先验仍占主导。

### Phase B: 对齐训练目标与评价指标

目标：判断 feature-space RF 是否缺少必要的几何监督。

- 在正确 `x0_pred` 上加入可微 joint-space loss：
  - `joints_pred = recover_from_local_position_batched(x0_pred * std + mean, 22)`
  - `joints_gt = recover_from_local_position_batched(motion_gt * std + mean, 22)`
  - MPJPE / joint velocity loss 只作用于 `x0_pred`，不得作用于 `v_pred` 或 `eps_pred`。
- 先跑小规模 gradient smoke，确认 recover 函数可微、loss finite、grad norm 正常。
- 成功阈值：T1 MPJPE ≤ 14 mm 才说明 raw-space MoDiffDec 有继续价值。

### Phase C: 严格 PiD-style 诊断

目标：判断 SAE latent 条件是否能让 target-space RF 成为有效生成式 decoder。

- T2-SAE：冻结 SAE encoder，RF 仍在 normalized 272D motion feature space 中预测 velocity，SAE latent 只作为条件注入。
- T3-uncond：完全相同的 RF 架构、loss、schedule、sampling steps 和 validation MPJPE selector，但移除 SAE/VAE latent 条件。
- 成功阈值：T2-SAE 达到 ≤ 16 mm，或至少比 T3-uncond 好 > 5 mm。
- 旧 latent-space RF + frozen CNN decoder 改名为 T4-LDM baseline；它可以回答“latent-space denoising 是否更容易”，但不能作为 PiD 主线证据。

### Phase D: 只有在前面通过后才讨论 SAE/VAE 与 text condition

目标：避免把低优先级变量和 P0/P1 问题混在一起。

- VAE vs SAE：在 T2-SAE/T3-uncond 之后替换 frozen encoder condition，先报告 matched VAE direct decoder baseline，再跑 VAE-conditioned raw RF，判断 VAE 是否比 SAE-conditioned raw RF 降 > 5 mm。
- text condition：只有进入 T2M 生成或 reconstruction 已接近 baseline 时再加。当前纯重建阶段不应把 text alignment 当作主要解释。

### Phase E: PiD 忠实适配的条件

若继续声称 PiD-style adaptation，必须满足：

1. RF/扩散目标必须在 motion target space，而不是 latent space 后接 frozen CNN decoder。
2. 最好有 target-space pretrained motion diffusion prior。MoLingo generator 是 latent-space generator，不是 raw-motion target-space prior，不能直接作为 raw decoder warm start。
3. raw-space prior 可来自 MDM / MotionDiffuse / ReMoDiffuse 类直接在 motion features 或 joint space 训练的模型；需要把其 text condition 改造成 SAE/VAE latent condition。
4. 若没有可接入 prior，本文应命名为 “conditional rectified-flow motion decoder”，不能把失败或成功归因到完整 PiD 本身。

## 4. 暂停项

- 暂停继续扩 D6/D7 作为主路线。
- 暂停 T2M 集成。
- 暂停 “SAE text alignment 不足” 相关训练，直到 reconstruction 任务接近 CNN baseline。
- 暂停 DMD2/LCM 蒸馏；当前质量未达 teacher 级别，蒸馏无意义。

## 5. 判停标准

若 T2-SAE 不比 T3-uncond 好 > 5 mm 且二者都不能把 MPJPE 降到 16 mm 以内，则停止当前 MoDiffDec 路线。此时最合理的结论是：在没有 target-space pretrained motion diffusion prior 的条件下，从零训练 raw-motion conditional RF decoder 无法竞争 MoLingo CNN decoder。
