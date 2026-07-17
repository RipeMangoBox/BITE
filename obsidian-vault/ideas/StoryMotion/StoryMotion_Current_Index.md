---
title: "StoryMotion Current Index"
status: active
tags:
  - StoryMotion
  - index
  - status/active
aliases:
  - StoryMotion-Current
created: 2026-07-12T12:20:00+0800
updated: 2026-07-17T18:25:00+0800
---

# StoryMotion Current Index

> [!abstract] Current surface
> 根目录只保留唯一当前叙事、history、canonical metrics、metric computation 和操作入口。旧 roadmap、loss 草稿与执行页位于 `archived/evidence/`，不再作为默认决策入口。

## Current Version

- [[version|唯一当前版本叙事、三模式公平比较与 P0-G 状态]]
- [[history|Version history and reliability table]]
- [[2026-07-16_storymotion-v739-v741-core-experiment-decision|唯一 active GPU、ETA 与 train-to-formal execution ledger]]
- [[2026-07-17_storymotion-fixed300-offline-ar-motionstreamer-v746-deployment|fixed-300、offline AR、MotionStreamer 与 official-AE Unified 四卡部署]]
- [[2026-07-17_storymotion-v8-yaw-quality-nonar-diffusion|v8 yaw-stable Stage1、data curation 与 non-AR diffusion 方案]]
- [[2026-07-17_storymotion-v8-3-data-curation-plan|v8.3 data-curation preregistered plan]]
- [[2026-07-17_storymotion-v8-3-data-curation-progress|v8.3 zero-progress and execution gate]]

## Canonical Metrics

- [[2026-07-12_storymotion-valid-metric-ledger|Valid metric ledger]]
- [[2026-07-09_storymotion-metric-computation-io|Metric computation and IO contract]]

## Operations

- [[StoryMotion_Gradio_Render|Gradio and rendering guide]]

## StoryMotion++

- [[2026-07-13_storymotion-plusplus-phase-adaptive-relational-guidance|StoryMotion++ 方法提案（非当前执行计划）]]
- 当前边界：v7.38 L0 clean 105k 仍是唯一 formal E0 mainline。v8.0已把v7.14长序列退化定位为yaw-velocity积分主导；v8.1A/B正在4090 GPU0训练，v8.2 human200正在GPU1训练，三条都还没有pure4053 endpoint结果，不能覆盖v7.14/v7.38。v8.3仅完成plan/progress预注册，因v8.2 endpoint ETA晚于当日22:00而保持零进度。MotionLab-MFT semantic/distribution胜L0但world-root退化；MoMask-Pulp三阶段训练已完成但formal adapter未闭合。representation、data cleaning与non-AR backbone必须分轴，三模式全面非劣、独立 seeds 与 blind study 均未闭环。

## Evidence Boundary

- 所有 active 指标只使用 `pure_`；
- v6 official-latent rows remain historical pure anchors；
- v5–v7.13 local-tokenizer rows require contract review before reuse；
- v7.15/v7.16 local Stage2 results are forensic because of wrong decoder and wrong causal cache；
- v7.17 is the corrected same-manifest pure diagnostic；
- v7.18–v7.25 保留为 collapse root-cause diagnostics；v7.30 已用 full-covariance 完成三 seed closure，v7.34 是当前 prompt-global Unified-3 screening evidence；
- v7.36/v7.38 是当前 asymmetric Unified-3 formal evidence；v7.39/v7.41 的 N64 与 latent rows 仅作 screening；v7.40 已有 formal pure4053，但因 broad regression 不晋级，不能覆盖 v7.38 mainline；
- archive中的文档可用于追溯，不应覆盖 [[version]] 与 canonical ledger。
