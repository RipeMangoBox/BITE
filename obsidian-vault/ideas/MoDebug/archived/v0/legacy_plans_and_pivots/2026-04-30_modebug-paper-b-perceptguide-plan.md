---
created: 2026-04-30T18:00
updated: 2026-05-01T16:05:43+08:00
title: "Paper B (PerceptGuide): 感知增强的事件级推理期 Reward Guidance"
status: active
tags:
  - MoDebug
  - paper-plan
  - PerceptGuide
  - perception-augmented
  - reward-guidance
  - PAPO
  - inference-time
related_notes:
  - "[[2026-04-29_modebug-roadmap]]"
  - "[[2026-04-29_modebug-exec-plan]]"
  - "[[2026-04-29_modebug-heldout-eval-policy]]"
  - "[[2026-04-30_modebug-paper-a-eventprobe-plan]]"
---

# Paper B (PerceptGuide): 感知增强的事件级推理期 Reward Guidance

## 1. 定位与核心主张

**类型**：Method paper（event-marginal reward + inference-time correction）。

**核心主张**：

> PerceptGuide 训练 event-marginal reward model，使 reward 对每个子事件的 presence / ordering perturbation 有边际敏感性，而不是只依赖 full-text global semantics。该 reward 在 diffusion denoising 中做 inference-time gradient correction，不更新生成器参数，并用 held-out final evaluator 验证是否真正减少 omission / ordering failure。从 VLM 感知增强到 motion event masking 的迁移不是直接套用：motion 没有像素级 spatial locality，event boundary 隐式嵌入在连续 motion 中，masking 必须在 text-side event decomposition 上操作，而不能依赖 motion-side hard segmentation。

**与 Paper A 的边界**：A 的 corruption protocol、held-out policy、consistency checker 只作为 B 的负例来源和 evaluation hygiene，不是 B 的主贡献。B 的 novelty 必须落在 event-marginal reward sensitivity 与 inference-time correction 上。

**与最近邻工作的差异**：

- vs AToM (CVPR 2025)：AToM 用 GPT-4V 标注偏好 + DPO 后训练改模型参数；PerceptGuide 用 HumanML3D-E event annotation 自举训练 + 推理期 guidance，不改模型参数，不依赖 GPT-4V / human preference labels
- vs ReAlign/EasyTune (ICLR 2026)：它们是全局或 step-aware reward alignment / fine-tuning；PerceptGuide 必须证明 event-marginal reward 相比 global reward / ReAlign-style reward 有额外收益，并且 reward-side gain 能转化到 held-out evaluator。
- vs Motion-R1/MoRL (ICLR 2026 / arXiv 2026)：它们依赖 explicit reasoning / LLM-style motion generation；PerceptGuide 不引入 LLM reasoning chain，而是在 diffusion denoising 中对连续 motion latent 做 event-level correction。

## 2. Contribution List

- C1: **Event-marginal reward learning**。通过 `full_text` vs `masked/drop/replace/shuffle_text` 的 counterfactual contrast 训练 reward，使每个子事件的边际贡献可测；必须与 global reward / ReAlign-style reward 做对照。
- C2: **Masked-event perception loss**。用 full event decomposition 与 masked event decomposition 的 reward 差异约束 reward model，证明它确实依赖目标 event，而不是只学习 full-caption semantic prior。
- C3: **Inference-time diffusion correction**。在 denoising 中后期注入 event-level reward gradient，不更新生成器参数；先验证 `R_pres`，`R_ord` 只在 independent final evaluator 可用时进入主实验。
- C4: **Fair evaluation under reward-metric proximity**。held-out 在 B 中只是实验卫生要求，不是主贡献；reward scorer 不能同时作为同一 claim 的 final main-table evaluator，reward-side gain 不能单独写成 improvement。

## 3. 必做实验

### B-P0: Backbone retrain sanity gate

B 的 reward training 与 inference-time correction 都依赖 EventT2M backbone。B-EXP1 前必须先完成 clean upstream EventT2M retrain sanity：

1. 若 retrain 与 pretrained 指标接近，B 可以继续以 EventT2M pretrained 作为主 backbone，并在 appendix 报告 retrain sanity。
2. 若 retrain 与 pretrained 差异很大，B 必须优先使用 retrain checkpoint 或同时报告 pretrained/retrain 两套结果；不能只在 suspicious pretrained 上做 reward guidance。
3. 若单卡 batch 与官方 batch 不一致，只能写作 local retrain sanity，不可宣称完全复现官方训练。

### B-EXP1: Event-level reward model 训练

用 HumanML3D GT motion + counterfactual negatives 自举训练 event-level reward model。

- 正例：GT motion + 对应 event annotation
- 负例：`drop / aligned_replace / hard_replace / shuffle` corruption（复用 Paper A 的 protocol，但在 B 中只作为训练数据构造）
- 感知增强：full decomposition vs masked decomposition 的 reward 差异作为 perception loss
- 必做对照：global reward / ReAlign-style reward vs event-marginal reward
- 预估：2-3 周
- 与 Paper A 关系：**完全独立**，可与 A-EXP1 同时开始；A-EXP3 的 hard-negative 结果可选择性反馈给负例策略，但不阻塞

### B-EXP2: Reward discriminative signal pilot（Go/No-Go Gate）

在不同 denoising step 上测试 reward model 对 omission / hard-replace / shuffle perturbation 的判别力曲线。

- 输出：step-wise discriminative signal curve；`drop / hard_replace / shuffle` 分开报告
- 预估：1 周
- 前置：B-EXP1 完成
- **这是 Paper B 的 go/no-go gate**：paired accuracy 需满足 `reward_dev_pres_full_vs_drop_paired_acc >= 0.70`、`reward_dev_pres_hard_replace_paired_acc >= 0.65`，且 `95% CI` 下界大于 `0.5`；否则回退检查 perception loss 设计或 reward model 架构
- 与 Paper A 关系：**完全独立**

### B-EXP3: Guidance injection 实现 + 实验

在 Event-T2M 上实现推理期 gradient injection。

- 先只开 R_pres，限制在 3-4 event 样本（5plus bucket evaluator consistency 不足）
- 同时记录 full-level safety（FID/R-Precision delta）和 event-side evidence
- 不写"架构无关"强 claim；当前最多写为可插拔到 diffusion T2M backbone，并优先在 Event-T2M 上验证。若能补一个额外 diffusion baseline，再扩展 claim。
- 预估：2-3 周
- 前置：B-EXP2 通过 go/no-go gate
- 与 Paper A 关系：**完全独立**

### B-EXP4: 感知增强消融

感知增强与 reward 形态消融。

- 必做：global reward / ReAlign-style reward vs event-marginal reward；no perception loss vs masked-event perception loss；reward-side gain vs held-out gain；`R_pres` only vs `R_pres + R_ord`（若 ordering final evaluator 可用）
- 输出：证明 perception loss 与 event-marginal design 是 reward model 质量的关键因素
- 预估：1 周
- 前置：B-EXP3 完成
- 与 Paper A 关系：**完全独立**

### B-EXP5: Held-out evaluation

用 held-out framework 验证 guidance 效果。这里的 `held-out` 是 scorer/protocol role separation，不只是数据 split。

- 如果 reward 用 TMR，final eval 用 ChronAccRet + human eval
- 如果 reward 用 ChronAccRet，final eval 用 TMR + human eval
- 如果 reward-side 提升但 held-out 不提升，只能写成 reward hacking / development result，不能写 main-table improvement
- held-out rule 不作为贡献点；它只是防止 reward 与 metric 过近造成不公平对比的最低要求
- 预估：1 周
- 前置：B-EXP3 完成
- 与 Paper A 关系：**弱依赖**——B-EXP5 最好等 A-EXP2（evaluator leakage）结论决定 reward/held-out 分配，但 B 可用默认分配（TMR 做 reward, ChronAccRet 做 held-out）独立进行

## 4. 与 Paper A 的资产复用

| 方向 | 复用内容 |
|------|---------|
| A → B | corruption protocol 代码、TMR/ChronAccRet scoring pipeline、held-out eval policy、condition manifest；这些是 training/evaluation hygiene，不是 B 的 novelty |
| B → A | 如果 B 先完成 guidance 实验，A 可在 failure pattern 中加入"guidance 前后的 failure pattern 变化"作为 case study |
| 共享 | HumanML3D-E、Event-T2M checkpoint、observation pool（64 samples）、condition manifest（256 rows） |

## 5. Timeline

| 阶段        | 任务                                     | 预估    | 可否与 Paper A 并行 |
| --------- | -------------------------------------- | ----- | -------------- |
| Week 1-3  | B-EXP1 reward model 训练                 | 2-3 周 | 可并行 A-EXP1/2/3 |
| Week 3-4  | B-EXP2 discriminative pilot (go/no-go) | 1 周   | 可并行 A-EXP5     |
| Week 4-7  | B-EXP3 guidance injection              | 2-3 周 | 可并行 A-EXP4     |
| Week 7-8  | B-EXP4 perception ablation             | 1 周   | 可并行 A 写作       |
| Week 7-8  | B-EXP5 held-out evaluation             | 1 周   | 可并行 A 写作       |
| Week 8-10 | 写作                                     | 2 周   | 可并行 A 写作       |

## 6. 独立成文条件

如果 B 进度快于 A，B 可以独立成文，只需要：

1. B 自己在 related work 中描述 held-out separation principle（1-2 段，不需要引用 Paper A）
2. B 自己跑 TMR + ChronAccRet cross-check 作为 evaluation（复用已有代码和数据）
3. B 的 evaluation section 自包含地描述 corruption protocol（1-2 段即可）

**B 独立成文不会削弱 A**，因为 A 的核心贡献是 human-calibrated diagnostic benchmark + failure atlas。B 只复用 A 风格的 protocol hygiene，不把 evaluation toolkit 或 held-out rule 写成自己的主贡献。

## 7. Go/No-Go Gates

| Gate | 条件 | 失败退路 |
|------|------|---------|
| B-GATE-1 | B-EXP2 paired accuracy: `reward_dev_pres_full_vs_drop_paired_acc >= 0.70`, `reward_dev_pres_hard_replace_paired_acc >= 0.65`, `95% CI` 下界 > `0.5` | 回退检查 perception loss 设计；如果仍不通过，考虑换 reward model 架构。阈值基于当前 `tmr_gt_pres_full_vs_drop_paired_acc = 0.7044` 作为 reference floor |
| B-GATE-2 | B-EXP3 full-level safety delta < 5% FID 退化 | 降低 guidance weight；如果仍退化，限制 guidance 只在最后 30% denoising steps |
| B-GATE-3 | B-EXP5 held-out evaluator 有正向提升 | 如果 reward-side 提升但 held-out 不提升，说明 evaluator leakage，需要换 held-out evaluator 或加入 human eval |

## 8. 当前禁写

1. 不把 PerceptGuide 写成 evaluator paper。
2. 不把 corruption protocol、consistency checker、held-out policy 写成 B 的主贡献。
3. 不写"架构无关"强 claim，除非至少在 Event-T2M 外再验证一个 diffusion baseline。
4. 不写 reward-side metric gain 等于 final improvement；必须过 held-out final evaluator。
