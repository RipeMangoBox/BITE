---
title: "MoDebug 实验资产总览"
created: 2026-05-17T16:36:06+08:00
updated: 2026-05-20T13:45:48+08:00
type: experiment_index
tags:
  - MoDebug
  - experiments
  - evidence_hygiene
---

# MoDebug 实验资产总览

这个目录只存放 MoDebug 可复查实验资产。当前整理后的原则是：`active/` 只放后续实验可以继续使用的干净基础；`retained_assets/` 保存可溯源但不回答当前主线问题的材料；旧路线结论进入 `archived/` 或 legacy 区，不作为当前方法证据。

## 当前 Active 实验

| 实验目录 | 当前角色 | 可继续使用的证据 | 不可写成的结论 |
|---|---|---|---|
| `active/full_text_full_motion_plugin_eval_20260520/` | 主线实验骨架 | `B` vs `B+MoDebug` 的 full-text / full-motion paired protocol、待填输入和评估槽位 | 目前还没有实测结果，不能宣称插件提升 |
| `active/p1_text_pressure_20260516/` | P1 文本侧压力轴 | 10 个 P1 sample、30 个 decomposed event、30 条 single-event prompt；CLIP / DistilBERT / T5 / Qwen 的 full-vs-single text embedding diagnostic；P1 generator/motion 缺失报告 | 不能宣称 generator propagation、motion event satisfaction 或方法提升；不能用旧 M0 proxy 填补 P1 缺口 |

## Retained Assets

| 目录 | 保留原因 | 当前角色 | 边界 |
|---|---|---|---|
| `retained_assets/soma_unified_30k_20260516/` | 有数据构造、split、转换和训练 provenance | 数据/训练资产参考 | 不作为 MoDebug 插件效果证据 |
| `retained_assets/vlm_pilot_20260516/` | 有 VLM/PoseFix 切片检查记录 | motion-side cross-check 参考 | 不作为 final evaluator，不提供精确 event boundary |
| `retained_assets/human_annotation_legacy/` | 保留旧人工标注原始记录 | legacy human review reference | 不合并进当前 active 结论 |
| `retained_assets/runtime_smoke_legacy/` | 保留历史 runtime smoke | infrastructure reference | smoke 不等于方法效果 |
| `retained_assets/prompt_legacy/` | 保留旧 agent prompt | prompt provenance | 不作为实验结论 |

## 证据保留标准

保留在 `active/` 的结果必须满足：

1. 有明确 `date`、`experiment_path`、`protocol`、`evaluator`、`data_source`、`n/evaluable`、`coverage`、`role`、`used_for` 和 `limitations`。
2. 结论能直接服务当前路线：full-text / full-motion plugin evaluation，或 P1 text-pressure 支撑。
3. 不把 diagnostic、cross_check、side signal、raw attention、VLM sidecar 或旧 proxy 写成 final evaluator。

降级到 `retained_assets/` 的结果满足：

1. 有可追溯 artifact 或人工记录；
2. 但不回答当前 `B` vs `B+MoDebug` 插件评估问题；
3. 或者只适合作为数据构造、cross-check、legacy annotation、runtime readiness。

从 active 结论中移除的内容包括：

1. 旧 M0 generator trace proxy 与 motion geometry/static panel 结论；
2. 混合 P1/M0 的 summary 和图表；
3. 无法作为当前主线证据的旧 route notes；
4. 缺 evaluator、protocol、coverage 或 limitations 的实验判断。

## 阅读顺序

1. 先读 [[ideas/MoDebug/active/full_text_full_motion_plugin_eval/README|主线方案]]。
2. 再读 `active/full_text_full_motion_plugin_eval_20260520/README.md`，按槽位填入后续实验。
3. 如果需要 P1 文本压力轴，读 `active/p1_text_pressure_20260516/README.md` 和 `results/file_map.md`。
4. 如果需要历史资产，只读 `retained_assets/README.md` 和对应资产 README，不把它们合并为当前方法结果。

## 当前下一步

后续实验应优先填充 `active/full_text_full_motion_plugin_eval_20260520/`：

```text
full text + baseline B -> full motion_B
full text + baseline B + MoDebug -> full motion_B+MoDebug
paired full-motion evaluation
```

P1 只用于提供文本侧压力轴和缺失清单。真正进入方法 claim 前，必须有完整 motion paired evidence。
