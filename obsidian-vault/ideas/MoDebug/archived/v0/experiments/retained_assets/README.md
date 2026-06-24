---
title: "MoDebug Retained Assets 索引"
created: 2026-05-20T13:45:48+08:00
updated: 2026-05-20T13:45:48+08:00
type: retained_asset_index
tags:
  - MoDebug
  - retained_assets
  - evidence_hygiene
---

# MoDebug Retained Assets 索引

## 定位

`retained_assets/` 保存可溯源但不属于当前 active 方法结论的材料。这些材料可以作为数据、人工标注、cross-check 或 runtime 参考；不能直接写成 MoDebug 插件提升、generator propagation 结论或 final evaluator。

## 资产清单

| 路径 | 类型 | 保留原因 | 当前边界 |
|---|---|---|---|
| `soma_unified_30k_20260516/` | 数据构造与训练资产 | 有 30k manifest、split、转换、训练和 eval provenance | 不作为 MoDebug 插件效果证据 |
| `vlm_pilot_20260516/` | VLM/PoseFix cross-check pilot | 有可见动作、轨迹和边界失败记录 | 不作为 final evaluator 或精确 event grounding |
| `human_annotation_legacy/` | 旧人工标注 | 保留 human review 原始记录和标注事件 | 不合并进当前 active P1 结论 |
| `runtime_smoke_legacy/` | 运行环境 smoke | 保留 historical runtime readiness | smoke 不等于方法质量或效果 |
| `prompt_legacy/` | 旧 prompts | 保留 agent prompt provenance | 不作为实验结果 |

## 使用规则

1. 引用 retained asset 时必须说明 `role=retained_asset` 或 `legacy_reference`。
2. 不能把 retained asset 中的 metric 或人工判断升级成当前主线结论。
3. 若某个 retained asset 要重新进入 active，必须补齐新的 protocol、run provenance、coverage、n/evaluable、limitations，并写清楚与当前 full-text / full-motion plugin evaluation 的关系。
4. 历史 JSON/TSV 中保留旧路径是 provenance，不代表当前 active 目录仍采用旧路线。
