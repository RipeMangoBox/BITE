---
title: "DIRECT: Dual-Frame Cinematographic Intent Transfer across Articulated Human Motions"
status: blocked_before_rect
hypothesis: |
  DIRECT recovers an actor/event-relative cinematographic program from a factual
  Human–Camera pair and re-executes it in the world frame for a different full
  Human motion. Source reconstruction is currently 0/25, so no Rect or A-series
  training is authorized.
tags:
  - DIRECT
  - paper/B
  - cinematographic_program
  - status/active
aliases:
  - DIRECT-Current
source_notes:
  - "[[DIRECT/2026-08-01_storymotion-multipair-data-training-plan]]"
  - "[[DIRECT/2026-07-31_storymotion-v11-actor-director-counterfactual-control]]"
  - "[[DIRECT/2026-08-01_storymotion-pulp-hml-stage1-data-mixing]]"
  - "[[StoryMotion/paper-boundary]]"
  - "[[StoryMotion-valid-metric-ledger]]"
created: 2026-08-03T14:30:39+08:00
updated: 2026-08-03T15:35:18+08:00
---

# DIRECT: Dual-Frame Cinematographic Intent Transfer across Articulated Human Motions

> [!important] Paper B identity
> **DIRECT: Dual-Frame Cinematographic Intent Transfer across Articulated Human
> Motions**。本文件夹只拥有Paper B文档；代码、配置、run与artifact仍位于StoryMotion
> 仓库，不创建DIRECT代码仓库。

> [!failure] 当前门禁
> `RV-25` source reconstruction为`0/25`。因此当前positive仍为`0`，不授权Rect-64、
> Rect-320、A-series或其他未单独定义的长训。下一步只能修复factual program extraction
> 与source reconstruction，再按冻结规则重新审计。

## 1. 当前研究边界

- `dual-frame`指actor／event-relative intent frame与world execution frame。
- 不得把HumanML3D Human与原Pulp world Camera直接组成positive。
- generated-H route没有合法re-execution target时，只能做推理分布测试。
- v11 Actor／Director反事实screen与Human-text Camera结果是前置诊断，不自动构成DIRECT
  方法闭环，也不改变StoryMotion mainline。

## 2. Canonical owners

- DIRECT program recovery、multi-pair、Rect与训练门禁：
  [[DIRECT/2026-08-01_storymotion-multipair-data-training-plan]]。
- Actor／Director反事实screen：
  [[DIRECT/2026-07-31_storymotion-v11-actor-director-counterfactual-control]]。
- Pulp–HumanML3D历史Stage1 mixing：
  [[DIRECT/2026-08-01_storymotion-pulp-hml-stage1-data-mixing]]。
- 两篇论文边界与单代码仓库合同：
  [[StoryMotion/paper-boundary]]。
- 已审计共享系统数字：[[StoryMotion-valid-metric-ledger]]；不得在DIRECT下复制
  第二份既有结果表。
- StoryMotion当前状态：[[StoryMotion/current|StoryMotion current]]。

## 3. 当前行动

1. 保留`RV-25=0/25`失败，不以target geometry或人工观感越过source gate。
2. 不启动Rect、A-series、HumanML3D规模扩展或未定义长训。
3. 若未来重开，只先提交program extraction／source reconstruction的新版本合同与审计。
