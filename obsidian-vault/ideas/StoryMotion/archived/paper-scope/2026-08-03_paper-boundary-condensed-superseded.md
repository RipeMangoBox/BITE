---
title: "StoryMotion / DIRECT Paper Boundary"
status: superseded_condensed
archived: 2026-08-03
hypothesis: |
  StoryMotion与DIRECT共享同一个StoryMotion代码仓库，但研究问题、训练边、
  artifact解释和论文claim必须分开管理。
tags:
  - StoryMotion
  - DIRECT
  - paper-boundary
  - status/active
aliases:
  - StoryMotion-DIRECT-Boundary
source_notes:
  - "[[StoryMotion/current]]"
  - "[[DIRECT/current]]"
  - "[[StoryMotion-valid-metric-ledger]]"
created: 2026-08-03T15:13:03+08:00
updated: 2026-08-03T15:13:03+08:00
---

# StoryMotion / DIRECT Paper Boundary

## 固定身份

- StoryMotion：**StoryMotion: Preserving Human Motion Priors in Asymmetric Human–Camera Generation**。
- Paper B：**DIRECT: Dual-Frame Cinematographic Intent Transfer across Articulated Human Motions**。
- 代码只使用`linkedCodebases/StoryMotion/`；不创建DIRECT代码仓库。
- StoryMotion文档位于`obsidian-vault/ideas/StoryMotion/`；Paper B文档位于
  `obsidian-vault/ideas/DIRECT/`。
- 正式数字继续由[[StoryMotion-valid-metric-ledger]]唯一维护，每条新证据必须标明
  `StoryMotion`、`Paper B DIRECT`或`shared baseline`。

## StoryMotion边界

StoryMotion研究能力保持式非对称扩展：

$$
p(H,C\mid T_H,T_C)=p_H(H\mid T_H)p_C(C\mid H,T_C).
$$

它只包含Direct-H、Direct-C和先固定Human再生成Camera的sequential composition。
Composition是两个条件分布的顺序调用，不是同步joint generator。StoryMotion可以包含Pulp Camera
坐标／文本修正作为次要数据贡献，但不包含Rect、HumanML3D跨配对、Camera program solver、
Actor–Director数据贡献或ViGen utility。

当前状态、实验闭环和可写claim分别见[[StoryMotion/current]]与
[[StoryMotion-iclr-reliability]]。

## Paper B边界

DIRECT研究从factual Human–Camera pair恢复dual-frame cinematographic program，并在不同完整
Human上重新执行。当前状态只见[[DIRECT/current]]。HumanML3D Human与原Pulp world Camera
不得直接组成positive；RV source reconstruction未通过前不得扩Rect或A-series。

## 历史快照

完整定位、两张内嵌SVG、竞品和claim边界已恢复到[[StoryMotion/paper-boundary]]；本页仅保留
精简替代期间的provenance，不再提供实验授权。
