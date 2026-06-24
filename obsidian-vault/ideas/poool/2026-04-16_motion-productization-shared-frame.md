---
created: 2026-04-16
updated: 2026-04-16
tags:
  - paper-idea
  - shared-frame
  - Motion_Generation
  - productization
  - agent
---
# 2026-04-16 动作生成落地化共享框架

> 这篇笔记只保留多篇“落地化 / product-ready / Agent 化”笔记共同复用的背景，不再在各篇主笔记里重复铺陈。

## 1. 共同问题框架

- **数据与评估层**：学术 benchmark 与真实用户 query、真实感知质量之间长期错位。
- **生成质量与物理层**：语义基本可对，但脚滑、漂浮、力量感不足、跨体型失真仍然常见。
- **控制接口层**：模型能被控制，不等于非专家能自然表达控制意图。
- **工作流集成层**：单次 demo 不等于可插入 Maya / Blender / 游戏引擎 / 虚拟人生产链。
- **持续对齐层**：部署后仍需要根据创作者偏好、业务规则和用户反馈持续修正。

## 2. 共同场景

- **游戏 / 影视 / 动画制作**：更关心“可编辑、可回溯、可迭代”而不是一次性最好看。
- **虚拟人 / XR / 实时交互**：更关心低延迟、稳定性、角色长期一致性。
- **Agent / Skill 化系统**：更关心 motion 是否能作为标准工具被上层规划器可靠调用。

## 3. 共同方法母题

- **评测重构**：从 FID / R-Precision 转向更贴近人类感知和真实业务约束的 judge 协议。
- **物理与质量增强**：不一定先做更大 backbone，也可以先做无 RL 的物理修正、质量蒸馏与后处理。
- **自然语言到结构化控制**：把模糊 prompt 解析为 DSL、slot、constraint 或 skill call。
- **Motion-as-a-Skill**：把生成、编辑、延长、评测、重定向统一封装成可组合接口。

## 4. 与现有笔记的分工

- [[2025-03-08|2025-03-08]]：宽口径 brainstorming 与 CCF-A 交叉技术池。
- [[2025-03-09_motion-llm-ideas|2025-03-09_motion-llm-ideas]]：聚焦 Motion+LLM / Motion+Agent 的真实缺口与跨模态迁移。
- [[2025-03-09_tencent-motion-topics|2025-03-09_tencent-motion-topics]]：把共享背景裁成腾讯课题 A/B 的选题版本。
- [[2026-03-13_motion-gen-deployment-gap|2026-03-13_motion-gen-deployment-gap]]：把共享背景进一步细化成“五层问题 → 五个研究题”。

## 5. 整理后的阅读顺序

1. 先读本文，建立统一的落地化问题框架。
2. 再读 [[2026-03-13_motion-gen-deployment-gap|2026-03-13_motion-gen-deployment-gap]]，看五层研究题如何拆开。
3. 若关心 LLM / Agent，读 [[2025-03-09_motion-llm-ideas|2025-03-09_motion-llm-ideas]]。
4. 若关心具体企业课题映射，读 [[2025-03-09_tencent-motion-topics|2025-03-09_tencent-motion-topics]]。
