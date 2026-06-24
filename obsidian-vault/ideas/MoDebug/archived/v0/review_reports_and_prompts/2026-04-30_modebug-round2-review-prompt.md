---
created: 2026-04-30T00:00:00+08:00
updated: 2026-05-01T15:05:48+08:00
title: "MoDebug Round 2 Review Prompt"
status: archived
tags:
  - MoDebug
  - review-prompt
  - archived
---

> [!warning] Archived
> This was a one-off review prompt. Do not use it as the current Paper A/B plan. Current entry is [[ideas/MoDebug/README]].

你是一位顶会论文审稿人级别的研究顾问。上一轮你对 MoDebug 双论文定位重构方案提出了 8 条问题和 3 条优先修改建议。我们已经逐条评估并执行了修改。请复查修改是否到位。

---

## 上一轮意见评估与处理

### 采纳并已修改（5 条）

**High 1：A-EXP2 "evaluator leakage" 设计不成立**
- 你的意见：仅比较已有 scorer rows 只能证明 scorer disagreement，不能证明 reward hacking / evaluator leakage。
- 评估：完全正确。
- 修改：A-EXP2 已重写为 **scorer-selection leakage** 实验。新设计：用 TMR 作为 dev optimizer（选择 reward 权重/负例策略/样本），然后用 ChronAccRet + human eval 做 held-out 检查。如果 B 的 guidance 输出可用，补做真正的 reward-optimization leakage。预估从 1 周改为 1-2 周。

**High 3：human validation 必须是核心证据**
- 你的意见：TMR × ChronAccRet consistency 只有 73.32%/63.75%，说明 evaluator 本身不稳，human eval 必须是核心而非附录。
- 评估：完全正确。
- 修改：A-EXP4 从"附录级补充"提升为**核心证据**。描述改为"核心证据，不是附录"，样本量从 100-200 扩大到 200-300，增加 per-bucket 拆分和 evaluator 不稳定区域的 targeted sampling。Timeline 从 2 周改为 2-3 周。

**Medium 5："零额外标注成本"表述矛盾**
- 你的意见：Paper A 同时计划 human eval，不能声称 annotation-free。
- 评估：完全正确。
- 修改：C1 措辞改为"核心 protocol 在 HumanML3D-E event annotation 之上无需额外标注；最终可靠性验证使用小规模 human calibration set（200-300 条）"。vs AToM 的差异描述也同步修改。

**Medium 6：R_dur 不该进 Paper B 核心 contribution**
- 你的意见：duration 没有正式 evaluator，不应承诺。
- 评估：完全正确。
- 修改：C3 从"三路 reward（R_pres / R_ord / R_dur）"改为"双路 reward（R_pres / R_ord）"，R_dur 标注为 later extension。

**Medium 7：B-GATE-1 > 0.6 阈值太随意**
- 你的意见：建议改成 AUC / paired accuracy + CI。
- 评估：正确。
- 修改：B-GATE-1 改为"paired accuracy: drop ≥ 0.70, hard-replace ≥ 0.65, 95% CI 下界 > 0.5"，并注明阈值基于当前 TMR omission baseline（full>drop=0.7044）作为 reference floor。

### 部分采纳（2 条）

**High 2：Paper B novelty 被 ReAlign/EasyTune/AToM 压缩**
- 你的意见：PerceptGuide 必须证明不是"PAPO loss + guidance 的组合改名"。
- 评估：方向正确。
- 修改：Paper B 核心 claim 重写为更尖锐的表述："event-marginal reward model trained by masked-event counterfactual sensitivity, used only for plug-and-play inference correction under held-out temporal evaluation"。新增 non-trivial 迁移说明：motion 无像素级 spatial locality，event boundary 隐式嵌入在连续 motion 中，masking 策略需要在 text-side event decomposition 上操作而非 motion-side 切分。
- 未完全采纳的部分：你建议的一句话表述太长，我保持了可读性但收窄了 claim。

**Medium 4：baseline list 需要更强**
- 你的意见：应加入 AToM/ReAlign/EasyTune/Motion-R1/MoRL。
- 评估：方向正确，但 Motion-R1/MoRL 是 LLM-based，无法跑 corruption protocol。
- 修改：A-EXP1 baseline 说明中新增"如果 AToM/ReAlign/EasyTune 有公开 checkpoint 或 generation output，加入对比；Motion-R1/MoRL 为 LLM-based 架构，无法直接跑 corruption protocol，在 related work 中做 qualitative comparison"。

### 不采纳（1 条）

**Low 8：投稿策略要错开**
- 你的意见：同一会议同时投 A/B 容易被识别为 salami slicing。
- 评估：这是投稿策略建议，不是文档修改。当前 plan 已写"各自独立成文"，投稿顺序由实验进度决定，不在文档中锁定。

### 额外修复

**Roadmap 旧叙事残留**
- 你指出 roadmap §2 仍写"当前只保留一条正式主线：inference-time reward guidance"，与双论文框架冲突。
- 修改：§2 Fixed Scope 改为"当前双主线并行推进"，分别描述 Paper A 和 Paper B 的主线。

---

## 复查要求

请检查以下 3 点：

1. **修改是否到位**：上述 7 条修改是否真正解决了你指出的问题？是否有修改不彻底或引入新问题的地方？
2. **遗漏检查**：修改后的方案是否还有你上一轮没提到但现在发现的新问题？
3. **优先级确认**：你上一轮的"只改 3 件事"建议是否都已覆盖？如果还有未覆盖的，请指出。

输出格式：
- 每条修改给一个 verdict（到位 / 部分到位 / 未到位）
- 如果有新问题，按 high / medium / low 排序
- 最后给出"当前方案是否可以进入实验执行阶段"的判断
