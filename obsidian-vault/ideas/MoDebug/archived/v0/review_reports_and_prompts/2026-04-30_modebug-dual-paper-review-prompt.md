---
created: 2026-04-30T00:00:00+08:00
updated: 2026-05-01T15:05:48+08:00
title: "MoDebug Dual Paper Review Prompt"
status: archived
tags:
  - MoDebug
  - review-prompt
  - archived
---

> [!warning] Archived
> This was a one-off review prompt. Do not use it as the current Paper A/B plan. Current entry is [[ideas/MoDebug/README]].

你是一位顶会论文审稿人级别的研究顾问。请对以下 MoDebug 项目的双论文定位重构方案做严格复查。

## 背景

MoDebug 原本定位为 "Event-Level Reward Guidance"，但经分析发现与现有工作（AToM CVPR 2025、ReAlign/EasyTune ICLR 2026、Motion-R1/MoRL ICLR 2026）撞车严重。现已拆分为两篇独立论文：

- **Paper A (EventProbe)**：多事件运动生成的反事实诊断与评估方法论
- **Paper B (PerceptGuide)**：感知增强的事件级推理期 Reward Guidance

两篇可并行推进、各自独立成文。

## 竞争格局（已知工作）

1. **AToM** (CVPR 2025)：GPT-4V 事件级偏好评分 → DPO/SLiC 微调。事件级奖励 + 后训练对齐。
2. **ReAlign** (AAAI 2026)：step-aware reward-guided alignment for diffusion motion generation。全局 reward + 推理期/后训练。
3. **EasyTune** (ICLR 2026)：step-aware differentiable reward fine-tuning + Self-refinement Preference Learning。全局 reward + 后训练。
4. **Motion-R1** (ICLR 2026)：Decomposed CoT Data Engine + GRPO。LLM-based，CoT 推理 + RL binding。
5. **MoRL** (arXiv 2026)：双头奖励 + Chain-of-Motion 测试时反思。LLM-based，理解+生成统一。
6. **Event-T2M** (ICLR 2026)：事件分解 + 运动感知检索编码 + 事件级交叉注意力 Conformer。MoDebug 的 generation backbone。
7. **EnergyMoGen** (CVPR 2025)：能量函数组合多概念动作生成。Compositional，但不做事件级时序。
8. **TransPhase** (NeurIPS 2025)：相位扩散多段运动生成。Compositional long-sequence。
9. **FlowMDM** (CVPR 2024)：Blended Positional Encodings 多段运动组合。
10. **InfiniDreamer** (ICCV 2025)：Segment Score Distillation 任意长运动。
11. **FineMotion** (ICCV 2025)：细粒度时空标注 dataset + benchmark。
12. **FineMoGen** (NeurIPS 2023)：细粒度时空混合注意力生成。

## 当前实验 artifact 数值

### Backbone Sanity (Event-T2M on HumanML3D-E)
- FID = 0.0497, R@3 = 0.8366（官方 ref: FID=0.0500, R@3=0.8470）

### TMR Omission
- N=3799, full>drop=0.7044, full>replace=0.8363
- 5plus bucket: drop=0.6611, replace=0.7573

### ChronAccRet Ordering
- full4068 CAR=0.6474, evaluable 2331/2333

### ChronAccRet Omission
- N=2333, full>drop=0.7300, full>replace=0.8551

### Safe-Drop Consistency (TMR × ChronAccRet)
- 1179/1608 = 73.32%, 5plus = 51/80 = 63.75%

### Aligned-Replace Consistency
- 1313/1608 = 81.65%, 5plus = 63/80 = 78.75%
- Coverage: vs TMR 42.33%, vs ChronAccRet 68.92%

### Lexical Hard-Replace Pilot
- TMR full>hard_replace = 0.652, 5plus = 0.556
- vs aligned-replace TMR 0.836, delta = -0.183

### G1/G2 Attention Observation
- 256 condition rows, 64 samples, 10240 attention records
- full normalized entropy mean = 0.9963
- condition-order peak match = 0.0523
- full-vs-replace abs peak shift mean = 82.68
- full-vs-shuffle abs peak shift mean = 57.18
- verdict: Gate A (localization) = weak/not passed; Gate B (corruption sensitivity) = mixed

---

## 文档 1: Paper A (EventProbe) Plan

### 定位
Evaluation methodology + diagnostic benchmark paper。

### 核心主张
> 现有 full-level metrics（FID, R-Precision）无法检测 event-level failure modes（omission, ordering violation）。我们提出 counterfactual corruption protocol + cross-evaluator consistency framework + held-out separation principle，系统化诊断多事件运动生成的 event-level failures，并在 4+ baselines 上发现此前未报告的 failure patterns。

### 与最近邻工作的差异
- vs AToM：AToM 用 GPT-4V 三维度评分，不做 evaluator 可靠性验证、不做 cross-evaluator consistency、不做 held-out separation。EventProbe 零额外标注成本、完全可复现。
- vs HumanML3D-E：提供 event annotation 和 event-level metrics，但不做 counterfactual corruption 诊断、不做跨 evaluator 一致性分析。
- vs FineMotion：做 fine-grained spatial-temporal annotation，但不做 event-level failure mode 诊断。

### Contribution List
- C1: Counterfactual corruption protocol（drop/replace/shuffle）
- C2: Cross-evaluator consistency framework（TMR × ChronAccRet × human/GPT-4V 三角验证）
- C3: Held-out separation principle（reward scorer ≠ final evaluator）
- C4: Multi-baseline diagnostic（4+ baselines 上的 failure pattern discovery）
- C5: 开源 evaluation toolkit

### 必做实验
- A-EXP1: 多 baseline 诊断（MLD, MDM, MotionDiffuse, Event-T2M），2-3 周
- A-EXP2: Evaluator leakage 实验（TMR 同时做 reward+eval vs ChronAccRet held-out），1 周
- A-EXP3: TMR-embedding hard-negative replace（验证 easy negative 膨胀），1 周
- A-EXP4: Human eval 三角验证（100-200 条，Fleiss kappa），2 周
- A-EXP5: Failure pattern 报告（跨 baseline 系统性 failure），与 A-EXP1 同步

### 已完成资产
- TMR omission N=3799, ChronAccRet ordering full4068, ChronAccRet omission N=2333
- safe-drop consistency 1608 rows, aligned-replace consistency 1608 rows
- held-out eval policy, hard-replace lexical pilot 512 rows
- condition manifest 256 rows, G1/G2 attention observation 10240 records

---

## 文档 2: Paper B (PerceptGuide) Plan

### 定位
Method paper（inference-time reward guidance）。

### 核心主张
> 我们提出感知增强的事件级 reward model 训练方法：通过 event masking 对比（full decomposition vs masked decomposition）的隐式感知损失，确保 reward model 对每个子动作敏感而非只依赖全局语义；在 diffusion denoising 过程中用事件级 gradient injection 实现 plug-and-play 的推理期修正，不改模型参数。

### 方法论来源
核心灵感来自 PAPO（Perception-Aware Policy Optimization）在 VLM 上的隐式感知损失，迁移到 motion generation 领域。

### 与最近邻工作的差异
- vs AToM：AToM 用 GPT-4V 标注偏好 + DPO 后训练改模型参数；PerceptGuide 用感知增强自举训练 + 推理期 guidance，不改模型参数，零外部标注
- vs ReAlign/EasyTune：它们是全局 reward + step-aware fine-tuning；PerceptGuide 是事件级 reward + 感知增强 + 不做 fine-tuning
- vs Motion-R1/MoRL：它们是 LLM-based CoT + GRPO；PerceptGuide 是 diffusion-based inference-time guidance，架构无关

### Contribution List
- C1: PAPO-style implicit perception loss for event-level reward model training
- C2: Event-level inference-time gradient injection with adaptive correction schedule
- C3: 三路 reward 设计（R_pres / R_ord / R_dur）
- C4: 在 held-out evaluation framework 下验证 guidance 效果

### 必做实验
- B-EXP1: Event-level reward model 训练（HumanML3D GT + counterfactual negatives + perception loss），2-3 周
- B-EXP2: Reward discriminative signal pilot（go/no-go gate，判别力 > 0.6），1 周
- B-EXP3: Guidance injection 实现（先 R_pres，限 3-4 event），2-3 周
- B-EXP4: 感知增强消融（no-PAPO vs PAPO），1 周
- B-EXP5: Held-out evaluation（reward ≠ final eval），1 周

### Go/No-Go Gates
- B-GATE-1: reward discriminative signal > 0.6
- B-GATE-2: full-level safety delta < 5% FID 退化
- B-GATE-3: held-out evaluator 有正向提升

---

## 并行/串行依赖关系

### 可完全并行（A 和 B 互不阻塞）
- A-EXP1 与 B-EXP1：完全独立
- A-EXP2 与 B-EXP1：完全独立
- A-EXP3 与 B-EXP1：完全独立；A-EXP3 结果可选择性反馈给 B-EXP1 负例策略
- A-EXP5 与 B-EXP2：完全独立
- A-EXP4 与 B-EXP3：完全独立

### B 对 A 的弱依赖
- B-EXP5 最好等 A-EXP2 结论（决定 reward/held-out 分配），但 B 可用默认分配独立进行

### 独立成文条件
- A 完全不依赖 B
- B 独立成文需要：自己描述 held-out separation principle + 自己跑 TMR/ChronAccRet cross-check + evaluation section 自包含描述 corruption protocol
- B 独立成文不会削弱 A

---

## 复查要求

请从以下维度严格复查，给出具体判断和修改建议：

### 1. 定位复查
- Paper A 定位为 evaluation methodology paper，在 ICLR/NeurIPS/CVPR 的接收概率如何？纯 evaluation paper 的接收标准是什么？当前 contribution 是否足够？
- Paper B 定位为 method paper，与 AToM/ReAlign/EasyTune/Motion-R1 的差异是否足够清晰？PAPO → motion 的迁移是否有足够的 novelty？
- 两篇论文的 novelty 空间是否真的不重叠？是否存在 reviewer 认为"这是同一个工作拆成两篇"的风险？

### 2. 竞争格局复查
- 是否遗漏了重要的竞品？特别是 2025-2026 年的 event-level / compositional / reward-guided motion generation 工作。
- Paper A 的 "counterfactual corruption protocol" 是否真的没有人做过？是否有 NLP/CV 领域的类似方法论可以被 reviewer 引用来质疑 novelty？
- Paper B 的 "PAPO-style perception loss" 从 VLM 迁移到 motion 是否有技术障碍？迁移的 non-trivial 程度是否足够？

### 3. 实验设计复查
- A-EXP1 的 baseline 选择是否合理？是否应该加入 Motion-R1 或 MoRL 作为 LLM-based baseline？
- A-EXP2 的 evaluator leakage 实验设计是否能真正证明 leakage？是否需要更严格的实验设计？
- B-EXP2 的 go/no-go gate 阈值 0.6 是否合理？依据是什么？
- B-EXP1 的 reward model 架构选择（TMR-based vs contrastive learning vs 其他）是否需要在 plan 中明确？
- 5plus bucket 的 evaluator consistency 不足（63.75%），是否应该在 Paper A 中作为 limitation 还是作为 finding？

### 4. 时间线复查
- 两篇论文的 timeline 是否现实？特别是 A-EXP1 需要跑 4 个 baseline 的 inference + scoring，2-3 周是否足够？
- B-EXP1 的 reward model 训练 2-3 周是否包含了架构搜索和调参时间？
- 如果 B-GATE-1 不通过，fallback 的时间成本是多少？

### 5. 过度表述 / 不足表述检查
- 两篇论文的 claim 是否有过度表述的地方？
- 是否有重要的 limitation 没有被提及？
- "首次在 motion generation 领域显式提出 held-out separation principle" 这个 claim 是否成立？是否有其他领域的先例？

### 6. 串行策略复查
- "先 A 后 B" 的串行策略是否最优？是否有更好的策略？
- 如果 B 先完成，B 独立成文的条件是否充分？是否会被 reviewer 质疑 evaluation 不够严格？
- 两篇论文投同一个会议是否有风险？是否应该错开投稿？

### 输出格式

1. 先给一个 verdict table：Claim / Verdict / Confidence / Problem / Suggested Fix
2. 再列最多 8 条严重问题，按 high / medium / low 排序
3. 最后给出"如果只能改 3 件事，改哪 3 件"的优先级建议
