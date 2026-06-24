---
created: 2026-04-16
updated: 2026-04-16
tags:
  - paper-idea
  - shared-frame
  - Motion_Generation
  - alignment
  - controllable-generation
---
# 2026-04-16 结构化对齐与多层控制共享框架

> 这篇笔记抽离“统一 MotionLLM / codebook 对齐 / body-part script / joint control / token-level operator”这些高频重合背景，让各篇笔记分别回到自己的独立角度。

## 1. 公共命题

- **统一表征不等于统一控制**：仅有 shared token space 仍不足以解决细粒度动作控制。
- **对齐需要分层**：sentence-level、event-level、body-part-level、joint-level 各自承担不同职责。
- **控制也需要分层**：全局文本负责“做什么”，结构化中间层负责“谁来做”，joint anchor 负责“怎么精确做”。
- **推理时算子有机会成为独立贡献**：token swap、guidance、stress test 不一定要绑死在训练范式里。

## 2. 共用分层图

`global text / plan -> time × body-part script -> sparse joint anchors -> motion tokens / full-body generation -> verifier / reflection`

这个分层图的价值不在于“更细”，而在于“只在必要处下钻到更细”。

## 3. 与现有笔记的分工

- [[2026-04-02_motion-unified-llm-open-source-survey|2026-04-02_motion-unified-llm-open-source-survey]]：开源项目与复现入口清单。
- [[2026-04-02_vq-codebook-motion-text-alignment-survey|2026-04-02_vq-codebook-motion-text-alignment-survey]]：对齐范式与 codebook 路线的证据库。
- [[2026-04-15_motion-multiple_level-control|2026-04-15_motion-multiple_level-control]]：层级控制接口的核心主张。
- [[2026-04-15_motion-token-swap-guidance|2026-04-15_motion-token-swap-guidance]]：token-level inference operator 的迁移设想。
- [[2026-04-15_motion-gen-high-dim-ideas-backbone|2026-04-15_motion-gen-high-dim-ideas-backbone]]：高维思想轴与低维实现图谱。
- [[2026-04-16_HY-Motion的若干不足，从点到面找问题|2026-04-16_HY-Motion的若干不足，从点到面找问题]]：模型级瓶颈诊断。

## 4. 研究切口拆分

- **表征与对齐**：shared token space、显式对齐损失、多粒度 supervision。
- **控制接口**：body-part script、joint anchor、uncertainty-aware arbitration。
- **推理时算子**：token perturbation、swap guidance、stress-test operator。
- **模型 critique**：把结构性缺口投射回具体 backbone，找最值得下手的瓶颈。

## 5. 整理后的阅读顺序

1. 先读本文，统一“对齐层级”和“控制层级”的总图。
2. 若想补证据库，读 [[2026-04-02_vq-codebook-motion-text-alignment-survey|2026-04-02_vq-codebook-motion-text-alignment-survey]]。
3. 若想看核心 hypothesis，读 [[2026-04-15_motion-multiple_level-control|2026-04-15_motion-multiple_level-control]]。
4. 若想找 inference-time 切口，读 [[2026-04-15_motion-token-swap-guidance|2026-04-15_motion-token-swap-guidance]]。
5. 若想回到具体模型诊断，读 [[2026-04-16_HY-Motion的若干不足，从点到面找问题|2026-04-16_HY-Motion的若干不足，从点到面找问题]]。
