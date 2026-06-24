---
title: "MoDiffDec"
status: diagnostic
hypothesis: "PiD-style motion decoding should be tested as latent-conditioned target-space RF, not latent-space RF plus a frozen CNN decoder; current T0/T1 show that from-scratch raw RF remains far from the MoLingo CNN decoder."
created: 2026-06-16T00:00:00+08:00
updated: 2026-06-18T15:35:00+08:00
tags:
  - MoDiffDec
  - motion_generation
  - diagnostic
source_papers:
  - "[[analysis/arxiv_2026/PiD_Fast_and_High-Resolution_Latent_Decoding_with_Pixel_Diffusion.md|PiD]]"
  - "[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation.md|MoLingo]]"
  - "[[analysis/ICLR_2026/COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High_Quality_Text_to_Motion_Generation.md|COME]]"
---

# MoDiffDec

> [!warning] 当前状态
> 旧方案已降级为 diagnostic。T0/T1 已完成：修正 `x0_pred` 后的 raw-space RF 仍约 29.8 mm，加入 joint loss 后最佳约 26.1 mm，仍显著差于 MoLingo SAE CNN decoder 的约 10.0 mm。复核 PiD 后，旧的 `latent-space RF + frozen CNN decoder` 只能作为 LDM baseline；下一步 PiD 主线应是 `SAE/VAE latent 条件 + 272D motion target-space RF`，并配 unconditioned control。

## 入口

- 核心 plan 与实验结论：[[ideas/MoDiffDec/CORE_PLAN_AND_RESULTS_2026-06-18]]
- 最新交接：[[ideas/MoDiffDec/GPT_HANDOFF|GPT_HANDOFF]]
- 修订方案：[[ideas/MoDiffDec/plan/revised_plan_2026-06-17|revised_plan_2026-06-17]]
- 诊断矩阵：[[ideas/MoDiffDec/plan/diagnostic_matrix|diagnostic_matrix]]
- PiD/LDM 术语纠偏：[[ideas/MoDiffDec/plan/deepseek_pid_correction_2026-06-18|deepseek_pid_correction_2026-06-18]]
- DeepSeek 审查摘要：[[ideas/MoDiffDec/plan/deepseek_review_2026-06-17|deepseek_review_2026-06-17]]
- 实验索引：[[ideas/MoDiffDec/experiments/README|experiments]]

## 当前判断

当前实现不是严格意义上的 PiD-to-MoLingo 适配，而是一个从零训练的 conditional rectified-flow decoder：

1. 输出空间是 normalized 272D raw motion features，条件是 frozen MoLingo SAE latent。
2. Stage 1 训练没有 text condition；motion-text alignment 只通过 SAE latent 间接出现。
3. 没有继承 target-space pretrained motion diffusion prior。PiD 的核心质量来源是预训练 pixel diffusion prior，这一点当前缺失。
4. loss 主要在 272D feature space，评估在 22-joint MPJPE space。二者没有直接对齐。
5. `x0_pred` 公式错误已在 T0/T1 中修复并评估，但修复本身没有把 MPJPE 拉近到 CNN baseline；当前主瓶颈转向 raw-space RF 学习难度、joint-space checkpoint selection、以及缺 target-space pretrained prior。

因此，当前性能差不能直接说明“motion diffusion decoder 不可行”，但足以说明旧方案中的 D1-D7 扩模型矩阵不是下一步重点。需要避免一个术语错误：PiD 不是“在 latent space 训练 diffusion 再接 frozen decoder”，而是“以 latent 为条件，在输出空间训练扩散/RF decoder”。

## 目录结构

```text
MoDiffDec/
├── README.md
├── CORE_PLAN_AND_RESULTS_2026-06-18.md
├── GPT_HANDOFF.md
├── plan/
│   ├── revised_plan_2026-06-17.md
│   ├── diagnostic_matrix.md
│   ├── deepseek_pid_correction_2026-06-18.md
│   └── deepseek_review_2026-06-17.md
├── experiments/
│   ├── README.md
│   ├── evaluation_D1_vs_baseline.md
│   ├── experiment_plan_legacy.md
│   └── progress_legacy.md
├── handoff/
│   └── GPT_HANDOFF_2026-06-17.md
└── archive/
    └── legacy/
        ├── architecture_initial.md
        └── implementation_initial.md
```

## 下一步

1. 停止 raw-space from-scratch scaling 作为主线；T0/T1 已证明修 bug 和 joint loss 仍无法接近 CNN baseline。
2. 在任何新训练前加入 validation MPJPE 或 joint-space proxy 的 checkpoint selection。
3. 将旧 `T2_latent_rf_sae` 改名为 `LDM-baseline`，不再作为 PiD 主线。
4. 下一步核心训练是 `T2_sae_cond_raw_rf`：冻结 SAE encoder，用 SAE latent 条件化 272D target-space RF，并用 validation MPJPE 选 checkpoint。
5. 同时需要 `T3_uncond_raw_rf` 控制实验，量化 latent condition 的真实增益。
6. 若 T2-SAE 和 T3-uncond 都无法达到 16 mm 以内，应停止当前 from-scratch route，转向 MoLingo CNN decoder 改进或寻找 raw-space pretrained motion diffusion prior。
