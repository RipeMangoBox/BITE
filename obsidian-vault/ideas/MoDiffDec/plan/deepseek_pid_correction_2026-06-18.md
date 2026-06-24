---
title: "DeepSeek PiD Correction 2026-06-18"
status: active
hypothesis: "PiD-to-motion should be defined as latent-conditioned target-space RF; latent-space RF plus a frozen CNN decoder is an LDM-style baseline, not the PiD mainline."
created: 2026-06-18T15:35:00+08:00
updated: 2026-06-18T15:35:00+08:00
tags:
  - MoDiffDec
  - PiD
  - diagnostic
  - DeepSeek
source_papers:
  - "[[analysis/arxiv_2026/PiD_Fast_and_High-Resolution_Latent_Decoding_with_Pixel_Diffusion.md|PiD]]"
  - "[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation.md|MoLingo]]"
---

# DeepSeek PiD Correction 2026-06-18

> [!abstract] 结论
> 用户对旧 T2 的质疑成立。PiD 不是“在 latent space 做 diffusion，再交给 frozen CNN decoder 解码”；PiD 是“以 latent 为条件，在输出空间做 diffusion/RF，并用这个生成模型替代或增强确定性 decoder”。因此旧 `T2_latent_rf_sae` 只能作为 LDM-style baseline，不能作为 PiD 主线。

## Correct Definition

| Term | Correct meaning in this project |
|---|---|
| PiD-style decoder | `z` is condition; RF/diffusion target is motion output space, e.g. 272D motion features or joints. |
| LDM-style baseline | RF/diffusion target is latent `z`; frozen CNN decoder maps `z_hat` to motion. |
| Current T0/T1 | Latent-conditioned raw-motion RF, but from scratch and without target-space pretrained prior. |

## Direct Answers

1. **PiD 用于 RF 阶段还是 SAE 阶段？**
   PiD 不训练 SAE 阶段本身。SAE/VAE 提供 latent condition；RF/扩散模型作为生成式 decoder 在 motion target space 中训练。

2. **T0/T1 是否是在 SAE decoder 上微调？**
   不是。T0/T1 冻结 SAE encoder，训练独立 `MotionDiffDecoder`。SAE CNN decoder 不参与 T1 推理，除非作为 direct reconstruction baseline。

3. **旧 T2 是否符合 PiD？**
   不符合。旧 T2 是 latent-space denoising + frozen CNN decoder，属于 LDM baseline。它可以作为对照，但不能证明 PiD-style motion decoding。

## Revised Core Experiments

| ID | Role | Setup | Decision |
|---|---|---|---|
| T2-SAE | Main PiD-style diagnostic | 272D raw-motion RF conditioned on frozen SAE latent; checkpoint by validation MPJPE. | If ≤16 mm or >5 mm better than T3, continue. |
| T3-uncond | Control | Same RF but no SAE/VAE latent condition. | Quantifies whether latent condition matters. |
| T4-LDM | Non-PiD baseline | SAE latent-space RF plus frozen CNN decoder. | Use only if comparing to LDM-style decoding. |
| T5-VAE | Condition-latent comparison | Matched VAE direct decoder baseline, then VAE-conditioned raw RF. | Use VAE only if matched gain >5 mm. |

## Visualization Requirement

For reconstruction visualization, always compare:

| Method | Why |
|---|---|
| Ground truth | Reference motion. |
| SAE direct reconstruction | Current deterministic decoder upper bound. |
| VAE direct reconstruction | Matched condition-latent baseline if VAE is considered. |
| T1 joint raw RF | Current best corrected raw RF result. |
| Future T2-SAE and T3-uncond | Required to inspect whether latent conditioning changes failure modes. |

## Risk

The largest remaining risk is that SAE/VAE latent contains enough information for deterministic reconstruction but is still not an effective condition for target-space RF from scratch. The clean test is not more model scaling; it is the matched T2-SAE vs T3-uncond comparison with validation MPJPE selection.
