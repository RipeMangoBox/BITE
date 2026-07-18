---
title: "StoryMotion Current Version"
status: active
hypothesis: |
  corrected v7.14 is the implementation Stage1 mainline and v7.38 L0 clean
  105K is the only formal Stage2 mainline. v8 remains a candidate family: its
  Stage1 gains are diagnostic until a prospective promotion gate is passed.
tags:
  - StoryMotion
  - version
  - stage1
  - stage2
  - status/active
aliases:
  - StoryMotion-Current-Version
source_notes:
  - "[[history]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[2026-07-17_storymotion-v8-yaw-quality-nonar-diffusion]]"
  - "[[2026-07-17_storymotion-v8-3-data-curation-plan]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
created: 2026-07-12T14:30:00+08:00
updated: 2026-07-18T15:20:00+08:00
---

# StoryMotion Current Version

> [!abstract] 当前裁决
> corrected v7.14 camera14 joint AE 仍是 Stage1 implementation mainline，v7.38 L0 clean `105K` 仍是唯一 Stage2 formal mainline。v8.1A、v8.1B、v8.2 都显著改善了 human Stage1 geometry；原始 promotion gate 无一通过。v8.1A 仅通过 amended **non-promotion** screen，v8.1B 与 v8.2 分别有 severe camera regression 与 camera center-translation regression。它们不替换 v7.14/v7.38，也不授权 promotion-bearing cache。

精确数值、四个时长 bin、bootstrap、artifact/checkpoint hash 只见 [[StoryMotion-valid-metric-ledger#18.1.1 v8 endpoint：与 corrected v7.14 的完整同脚本比较]]。

## 1. 固定主线与解释边界

- **Stage1 implementation mainline**：corrected v7.14，normalized human199 + official camera14、non-causal、human128 + camera64，以及 owning local decoder。
- **Stage2 formal mainline**：v7.38 L0 clean `105K`，只能支持“已完成其 contract 下的 formal eval”，不能自动支持 decoded visual quality 或跨-seed promotion claim。
- **v8 family**：candidate controls。原始 Stage1 root/yaw geometry gate 是 promotion 前置条件；后验 amended screen 不能追溯替代它。
- **v7.47 official-AE isolation**：四个 `105K` profile execution 已结束，但 raw JSON/records 仍在 runner overlay，未能 audit；返回的 SHA 不是性能结果。

## 2. 当前决策板

| version / run | 要回答的问题 | 当前状态 | 当前允许行动 | 证据 owner |
| --- | --- | --- | --- | --- |
| v7.14 / `joint_ae_official_4090_gpu0_r2` | corrected local tokenizer 是否作为 implementation baseline 可用 | implementation mainline；long human geometry 仍是已知风险 | 保持为 control，不把它写成长程 quality pass | metric ledger、metric I/O |
| v7.38 / `v7_38_l0_clean_105k_seed17` | Unified-3 的 `105K` formal reference 是什么 | 唯一 Stage2 formal mainline | 作为 `105K` comparator；不把 free-generation paired geometry 单独当 hard gate | metric ledger |
| v7.47 / `v7_47_official_ae_unified_matched_seed17_4090g0_20260717` | official AE 是否改变 matched Stage2 learnability | execution complete，formal audit pending raw artifact recovery | 恢复 runner overlay artifacts 后审计与比较 | metric ledger、history |
| v8.1A / `v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717` | geometry loss 是否使 human199 表征更适合生成 | amended non-promotion screen pass；不具 promotion status | 仅走 diagnostic-only D0→30K→条件性105K ladder | v8 page、generatability ladder |
| v8.1B / `v8_1b_residual_ae_yaw001_root003_seed17_4090g0_20260717` | residual AE 是否带来可归因增益 | completed_no_promotion；short-bin camera severe regression | 先做 Stage1 camera root-cause；不训 Unified | v8 page、generatability ladder |
| v8.2 / `v8_2_human200_joint_ae_yaw001_root003_seed17_4090g1_20260717` | integration-free human200 是否值得保留 | completed_no_promotion；camera translation severe regression | 先拆解 layout/stats/joint optimization；不训 Unified | v8 page、generatability ladder |
| v8.3 / `clean_manifest_ablation` | pair-level curation 是否改善 Stage2 prior | preregistered, not started；无 promoted representation | 保持 gate closed，所有计数为 `0` | curation plan |
| v8.4-A/B / `motion_mamba_ldm` / `transphase_control` | 新 non-AR backbone 是否改善生成 | not started | 仅在 representation promotion 后进入 matched backbone axis | v8 page |

## 3. 不可变的评测边界

- Human completion 是 human-text-only；camera completion 消费 GT/observed human latent + camera text；joint attribution 必须从同一 Unified checkpoint 同时报 parallel 与 human-first cascade。
- 所有 StoryMotion Stage1/Stage2/cache/load/eval 均断言 `is_causal=false`；standalone native MotionStreamer 是唯一外置例外，不能进入 StoryMotion cache 或 gate。
- formal development split 是 pure4053，已被多轮开发使用；最终 treatment 锁定后仍需独立 frozen final test。
- 任意混版本指标表都必须有非空 `version / run` 列。数值、records、evaluator/decoder provenance 的唯一 owner 是 [[StoryMotion-valid-metric-ledger]]；指标定义的唯一 owner 是 [[StoryMotion-metric-computation-io]]。

## 4. 近期顺序

1. 恢复并审计 v7.47 raw artifacts；这是一条已完成训练的 matched representation control。
2. 对 v8.1A 先完成 diagnostic-only cache preflight、latent/decoder robustness 与 `10K` trajectory screen；`30K` 只和 v7.36 A30 比，`105K` 才和 v7.38 L0 比。
3. 对 v8.1B/v8.2 做 camera root-cause short diagnostics，不用完整 Unified training 遮蔽已知 Stage1 failure。
4. v8.3、v8.4 继续被 prospective promotion gate 阻断。

完整的实验层级、停止规则、实用 regression margin 与记录方式见 [[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]。

## 5. 阅读与增量路由

- 当前决策：本页。
- 已审计数字：[[StoryMotion-valid-metric-ledger]]。
- 版本事实与已关闭事件：[[history]]。
- v8 hypothesis、gate、version matrix 与 candidate conclusion：[[2026-07-17_storymotion-v8-yaw-quality-nonar-diffusion]]。
- v8.3 curation contract 与进度：[[2026-07-17_storymotion-v8-3-data-curation-plan]]。
- 表征可生成性与 Stage2 stop/continue ladder：[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]。

run 中的 ETA、step、worker output 和 checkpoint 仅进入 remote run manifest/log；formal audit 后才依次进入 metric ledger、本页和 history。根目录 `AGENTS.md` 定义完整 owner/archival policy。
