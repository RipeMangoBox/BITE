---
title: "StoryMotion v7.15 Matched Stage2 Results"
status: invalidated
hypothesis: |
  A matched symmetric-vs-asymmetric Stage2 comparison can identify whether directed human-to-camera generation resolves human-camera denoising interference.
tags:
  - StoryMotion
  - Motion_Generation
  - experiment
  - stage2
  - status/invalidated
aliases:
  - StoryMotion-v7.15
source_notes:
  - "[[2026-07-11_storymotion-v7.14-corrected-results]]"
  - "[[2026-07-11_storymotion-v7.16-stage2-forensic-audit]]"
  - "[[2026-07-11_storymotion-latest-roadmap]]"
created: 2026-07-11T18:30:00+0800
updated: 2026-07-11T23:54:20+0800
---

# StoryMotion v7.15 Matched Stage2 Results

> [!warning] Invalidated evaluator evidence
> 本页保留 v7.15 的训练与历史 JSON，但其 official metrics 和 visual decode 使用了 official Pulp decoder 解码 local joint-AE latent。该 decoder-contract 错配可以在完全绕过 Stage2 时复现灾难指标，因此本页不能支持 topology、normalization 或 tokenizer suitability 结论。复查证据与新实验顺序见 [[2026-07-11_storymotion-v7.16-stage2-forensic-audit]]。

## Post-hoc Invalidation

v7.15 cache metadata 指向 v7.14 local joint AE checkpoint，而 evaluator 的 `model_dir` 指向 official Pulp autoencoder。两者 latent shape 都是 `192 × 75`，但 latent basis 和 decoder weights 不同。

在 pure-256 上，local AE 真实 cache latent 直接通过错误 official decoder 已得到 FDTMR `1787.38`、FDCLaTr `580.17`、Out `79.55%`。这与 v7.16 错误-decoder Stage2 的 `1815.54 / 590.34 / 79.74%` 几乎一致，证明旧“崩溃”指标主要由 evaluator 造成。

## Contract

| item | symmetric | asymmetric |
| --- | --- | --- |
| Stage1/cache | v7.14 corrected joint AE, 162760 train / 4053 pure eval | same |
| process | CondMDI diffusion | CondMDI diffusion |
| topology | one joint model | human-text then H2C |
| width | 416 | 288 + 288 |
| parameters | 86.65M | 41.96M + 41.96M = 83.92M |
| optimization | 50000 steps, batch 512, seed 17 | 50000 steps per branch, batch 512, seed 17 |
| sampler | 50-step DDIM, CFG 1.0 | same per branch |

Version provenance:

- code branch: `agent/fix-v714-official-feature-contract`
- training launcher: commit `4c83032`
- symmetric run: `symmetric_joint_w416_steps50000_seed17`
- asymmetric runs: `asymmetric_human_text_w288_steps50000_seed17` and `asymmetric_h2c_w288_steps50000_seed17`
- official metric files: `symmetric_joint_pure4053.json` and `asymmetric_composed_pure4053.json`

## Official Pure-4053 Results

| topology | FDTMR ↓ | TMR ↑ | HCov ↑ | FDCLaTr ↓ | CLaTr ↑ | CCov ↑ | F1 ↑ | Out ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| symmetric | 1714.96 | 0.00 | 0.12% | 536.76 | 6.95 | 4.22% | 0.070 | 77.9% |
| asymmetric | **1646.80** | 0.00 | 0.10% | **411.14** | **8.76** | 3.58% | **0.120** | 83.4% |

这些数字仅作为历史工件保留。由于两个 topology 都经过错误 decoder，它们不能建立架构 winner，也不能比较 failure severity。

## Visual Audit

Eight matched samples were rendered for both models, but the render path used the same wrong official decoder. The observed human-root and camera-path offsets therefore validate the decoder mismatch, not the Stage2 topology. These visuals are retained only as forensic artifacts and must not be used for architecture judgment.

Artifacts:

- `runs/eval/stage2/v7_15_matched_sym_asym_20260711/renders_symmetric/`
- `runs/eval/stage2/v7_15_matched_sym_asym_20260711/renders_asymmetric/`
- Gradio: `scripts/v715_matched_stage2_gradio.py`

## Historical Shared Failure Hypothesis

The corrected local-AE cache differs strongly from the official latent scale:

| cache | all std | human std | camera std |
| --- | ---: | ---: | ---: |
| official Pulp AE | 0.56 | 0.57 | 0.56 |
| v7.14 corrected joint AE | 1.75 | 1.91 | 1.35 |

z-normalization 缺失是 v7.15 的真实训练 contract 回归，但后续 v7.16 已正确恢复。它不再是旧灾难性 official 指标的首要解释；错误 decoder 才能直接复现该指标。以下内容仅保留当时推理链：

1. both Stage2 topologies fail despite different dependency graphs;
2. human and camera branches also have mismatched scales inside the corrected cache;
3. diffusion starts from a standard-normal prior while the local latent distribution is wider and non-zero-mean;
4. per-channel latent z-normalization existed in commit `0451a4d`, but the later trainer rewrite in `7c4cee3` removed that path from the active code.

## Superseding Core Experiments

本页原 P0 顺序已由 [[2026-07-11_storymotion-v7.16-stage2-forensic-audit#6. 更新后的三个核心实验]] 替代：

1. 修复 evaluator owning-decoder contract 与 joint-only checkpoint selection；
2. 用现有 ckpt 做 latent perturbation、单步 denoise 和 sampler closure；
3. 用正确 decoder 做 official/local AE/VAE 的严格 matched 10k learnability curve。

在这三个 gate 之前，不重跑 symmetric/asymmetric full A/B。
