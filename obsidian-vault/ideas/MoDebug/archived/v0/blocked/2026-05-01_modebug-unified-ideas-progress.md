---
created: 2026-05-01T20:00
updated: 2026-05-11T20:55:00+08:00
title: MoDebug EventT2M-Era Progress And Local Artifact Route
status: blocked
tags:
  - MoDebug
  - unified
  - progress
  - EventProbe
  - PerceptGuide
related_notes:
  - "[[ideas/MoDebug/README]]"
  - "[[paperIDEAs/MoDebug/2026-05-06_modebug-backbone-migration-plan]]"
  - "[[2026-05-01_modebug-eventt2m-retrain-sanity-plan]]"
  - "[[ideas/MoDebug/blocked/README]]"
---

# MoDebug 统一叙事：并行 Idea 与进度推进

> [!warning] Historical Progress Record
> This note is retained as EventT2M-era progress provenance and as source material for the non-MLLM local motion semantic artifact route. It is no longer the active execution entrance. Current route comparison starts from [[paperIDEAs/MoDebug/2026-05-11_modebug-route-overview]].

> [!abstract] **当前定位**
> MoDebug 是一个围绕"多事件运动生成的 event-level failure"的研究项目。本文档中的 active 口径已被后续单思路路线 note 取代；保留的可复用思想是 **定位 + 修复 local motion semantic artifacts**，且默认不依赖 MLLM。
>
> 旧的分路线成稿计划、roadmap、exec-plan、evaluator-status、heldout-policy 已归档至 `archived/`。本文档是唯一的进度推进入口。

## 0. Current State 摘要

> [!abstract] **执行入口**
> 本节只保留当前决策、最短关键路径、人机分工和停止扩张条件。authoritative 的指标 / artifact / protocol 记录仍在 §3 与 §5；资产索引见 §4；历史变更记录见 §8；延后方向已移到 [[paperIDEAs/MoDebug/2026-05-01_modebug-spatiotemporal-extension-backlog]]。

### 0.1 当前决策（执行版）

| 项目                | 当前决策                                                                                    | 还不能写                                                     |
| ----------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| EventT2M backbone | 2026-05-11 `2ac5ea8` 后，`003245` epoch135 单样本 scale sanity 已恢复到 HumanML3D 量级；该记录仍是 diagnostic | 不把单样本 scale sanity 写成 final evaluator、backbone-selection evidence 或 full-level safety |
| Route status | 本文档不再是统一入口；local artifact non-MLLM 路线已拆为单独 note | 不继续在本文档里混写 cross-generator、negative-pair、ANTS-style 路线 |
| ChronAccRet 角色    | HumanML3D-E adapter + `train_bert_orig` sanity 已可用；保留为 ordering / omission evaluator 资产 | 不把约 `0.66-0.67` CAR 直接当真实 ordering failure rate          |
| EventProbe 主线     | 当前真正 go/no-go 压在 S7 → S8 → S10                                                          | 不用 FID / R-Precision 定义直接推出主 punchline                   |
| PerceptGuide 定位   | S2 / S4 先保留为 reward baseline 证据；S9 只有在 S8 给出 `method_direction_decision` 后才升级           | 不把 reward-side dev/test observation 写成 final improvement |
| unified evaluator | 明确 deferred，等 S7 / S8 / S10 后再判断                                                        | 不把未校准 automatic scorer 写成 unified final judge            |

### 0.1a Backbone 迁移决策（2026-05-06）

当前路线拆分见 [[paperIDEAs/MoDebug/2026-05-11_modebug-route-overview]]。本节只保留历史决策来源：

1. EventT2M-era versions 标记为 historical：保留 full-level reproducibility、reward-side、evaluator-side 和 failure-case 资产。
2. 新 active route 需要单独声明 claim、最小证据、evaluator role、artifact contract 和停止条件。
3. Local artifact 路线的核心是定位并修复本地 motion semantic artifacts，不依赖 MLLM；详见 [[paperIDEAs/MoDebug/2026-05-11_modebug-route-1-local-motion-semantic-artifact-debug-non-mllm]]。
4. Cross-generator、negative-pair training、ANTS-style adaptive failure-space 已拆成独立路线 note，不再混在本文档中推进。

### 0.2 最短关键路径

1. **先选当前路线**：从 [[paperIDEAs/MoDebug/2026-05-11_modebug-route-overview]] 的 Route-1/02/03/04 中确定本轮执行对象。
2. **再定义 route-specific evidence**：每条路线都必须记录 claim、artifact contract、evaluator role、`n/evaluable`、coverage 和 limitations。
3. **再回答归因问题**：不要把旧 EventT2M component inventory、M0_v2 geometry audit 或单样本 scale sanity 升级成机制结论。
4. **再跑小规模人工审核或校准**：只有当 automatic scorer 和人工判断对得上，才扩到正式评测。
5. **最后做投稿形态判断**：Route-2 + Route-3 是当前最强主线候选；Route-4 作为框架 / training-free branch；Route-1 作为 local diagnostic support。

### 0.3 Human / Machine 分工

| 具体动作 | 负责人 | 可并行 | 主要作用 |
| --- | --- | --- | --- |
| 先定第一轮只看哪些 baseline、哪些扰动方式、哪些 event bucket | human | 否 | 防止范围继续膨胀 |
| 把已有生成结果、自动评分和样本信息整理成同一张样本表 | machine | 是 | 给后续归因分析和人工审核提供统一入口 |
| 把 S3 的 trace 信息回连到这张样本表里的具体 case | machine | 是 | 让 S8 能分析“为什么错” |
| 只对选中的 case 补 G3、attention heatmap 和 motion packet | machine | 是 | 支撑 EventT2M 内部机制分析 |
| 先写清 omission / ordering / severity 的人工标注规则 | human | 是 | 避免人工审核时口径漂移 |
| 先看 20-40 个高分歧 case，确认可视化和标注规则是否靠谱 | human | 是 | 先排掉明显的伪信号和规则歧义 |
| 用同一批 case 启动小规模人工审核 | human + machine | 是 | 验证自动分数和人工判断是否能对齐 |

### 0.4 停止扩张条件

1. B1 第一轮 baseline 上限固定为 `MoGenTS + MoMask`；在三样本静态骨架 smoke 补齐之前，不再把 ReAlign / EasyTune / Motion-R1 / MoRL 加进主线。
2. S7 第一轮只看 `full_text vs drop_text` 和 `full_text vs shuffle_text`；`replace_text` 先只当参考，不拿来决定 go/no-go。
3. S7 第一轮主要看 `3 / 4 / 5plus` 事件数 bucket；`2` bucket 先只保留参考值。
4. 任何没有回连到具体样本行的 trace / heatmap / gradient artifact，都不能直接写进 S8 结论。
5. 小规模人工审核没有先跑稳之前，不扩到正式人工评测；如果标注规则或一致性不稳，先修规则和抽样。
6. S8 没明确给出 `method_direction_decision` 之前，S9 只能写成 baseline pilot，不能提前写成方法主线。

### 0.5 当前新增工具链（2026-05-06）

今天已经补上一个 **pretrained-only 人工审核 MVP**，目标原本是先把 “生成样本 -> 渲染视频 -> 人工审核 -> 本地记录” 这条链跑通。由于 EventT2M generated-motion backbone gate 已失败，这条链现在只保留为 legacy tooling / interface reference；不要继续用当前 EventT2M generated motions 扩人工审核样本。

已新增：

1. review manifest 脚本：`linkedCodebases/EventT2M-codes-main/src/run_pretrained_human_review_manifest.py`
2. 批量骨架视频渲染脚本：`linkedCodebases/EventT2M-codes-main/src/run_modebug_render_review_videos.py`
3. Gradio 审核 app：`linkedCodebases/EventT2M-codes-main/app_pretrained_human_review.py`

当前用途：

- 作为 legacy EventT2M 工具链参考，不再作为当前 S10a 输入源。
- machine 负责整理 manifest、渲染视频、提供审核界面和保存结果。
- human 只负责审核样本并写 judgment / notes。

推荐最小执行顺序：

1. 先把已有生成结果转成 review manifest。
2. 先渲染一个小 slice 的视频，确认视频链路没问题。
3. 先启动 Gradio，把人工审核流程跑通。
4. 再把 `HumanML3D-E test` 的全量生成与渲染作为长任务持续推进。

### 0.6 当前详细快照

> [!note] 读法
> 本小节保留详细 decision snapshot 便于复查；如果只看下一步执行，请优先阅读 §0.1-§0.4。

| 主题                           | 已证明 / 未证明                                                                                                                                                                            | 下个决策                                                                                                         | 风险 / 禁写                                                                                                                                                                                         |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| EventT2M backbone            | paper-native full-level 指标接近不自动等于 event-level correctness；2026-05-11 后 `003245` epoch135 单样本 scale sanity 已恢复 | 若重新使用 EventT2M，必须在新 active route 中记录当前 repo/data/ckpt/config/manifest/evaluator coverage | 单样本 scale sanity 是 `diagnostic`，不是 held-out final evaluator 或 backbone-selection evidence |
| ChronAccRet 数据域              | 已证明：pretrained+adapter 通过 <5pp gate；`train_bert_orig` retrain sanity 得到 CAR `0.6725`                                                                                                 | S7 使用时报告 coverage、evaluable、condition_pair、model_source、training_objective、role 和误差边界                        | `train_bert_orig` sanity 未开启 ChronAccRet 论文 event-enhanced / negative-training loss 或对应梯度路径，不能和论文 event-enhanced / negative-training 训练设置直接比较；也不能把约 `0.66-0.67` CAR 直接当真实 ordering failure rate |
| EventProbe 主 claim           | 未证明：full-level safety 与 event-level failure 弱相关 / 不相关 / tradeoff                                                                                                                     | S7 多 baseline diagnostic + S10 human calibration                                                             | 不能只用 FID/R-Precision 的定义推出主 punchline                                                                                                                                                           |
| Unified temporal evaluator   | 未开始独立实现；当前 S7/S10 是诊断与校准证据积累，不是已有统一 evaluator                                                                                                                                        | 先完成 S7/S8/S10，再决定是否需要将 TMR / ChronAccRet / human calibration 收敛成统一评估器                                        | 不把未校准 automatic scorer 写成 unified final judge                                                                                                                                                   |
| PerceptGuide reward baseline | 已证明：S2a/S2b 在 R_pres / `full_text vs drop_text` same-protocol dev gate 通过；S4 drop-only step-wise reward-side dev gate machine-pass。未证明：final guidance improvement、R_ord、hard-replace | S4 human review 后，只允许准备 S9a generic reward-gradient baseline；S9b targeted method 仍等 S8 method-direction gate | reward-side dev/test observation 不能写成 final；S2b no-event-mask 只有 1 seed；S4 不是 RL 也不是 held-out final evaluator                                                                                   |
| Reward / RL 边界               | S2/S4/S9 使用 reward signal，但当前不是 RL：无 policy optimization、无 value function、无 rollouts-based credit assignment                                                                         | 若未来引入 Motion-R1 / MoRL 式 RL，必须另开 step，写明 policy、reward、optimization objective 和 held-out evaluator           | 不把 supervised rank reward、step-wise discrimination 或 inference-time gradient guidance 称为 RL 结果                                                                                                  |
| S8→S9 方法方向                   | 未证明：当前 S2/S4 reward baseline 已由 S8 归因支持                                                                                                                                              | S8 后必须记录 `method_direction_decision`，再决定 S9 是否继续通用 reward gradient                                           | 若根因是 attention / embedding collapse，S9 应转向 targeted correction；通用 reward gradient 只保留 baseline 定位                                                                                               |
| 当前证据缺口                       | S3 已补 EventT2M pretrained 64-sample / 256-row per-head multi-step replay；automatic head filtering gate 未过；S4 已补 score-review packet但 motion visual review 未完成                        | S11 正式消融需补 no-event-mask 3 seeds；S8 归因仍需 S7 failure cases + G3 + human/visual review packet                  | 不得把 per-head trace、automatic head-filtering side signal 或 S4 reward-side score 写成 S8 attribution / final improvement claim                                                                      |

### 0.7 ICLR/ICML Plan Stress Test（2026-05-03）

> [!note] 读法
> 本节评估 **MoDebug plan 是否足以通向 ICLR/ICML 级别论文**，不是评价当前未完成进度是否可投稿。未完成的 S7/S8/S10/S11 是计划内前置条件，不应被当作当前结果缺陷；压力测试只记录后续计划必须满足的 reviewer gates。

**Plan verdict**：方向值得继续，计划的主线应收缩为 **EventProbe-first**：先完成 diagnostic + attribution + human calibration，再根据 S8→S9 的机制证据决定 PerceptGuide 是否升级为方法贡献。当前 plan 的关键优点是把 backbone hygiene、evaluator boundary、reward/evaluator separation 和 method-direction gate 都显式化；关键风险是如果 S8 不能产出清晰根因，PerceptGuide 只能保留为 baseline pilot。

**Plan-level reviewer gates**：

1. EventProbe gate：S7 必须证明 full-level safety 与 event-level failure 在通过完整 `training / inference / eval` gate 的 replacement baselines 上存在稳定脱钩、弱相关或 tradeoff；EventT2M 只能在重新通过 generated-motion scale sanity 后作为 backbone column，否则只作 historical / diagnostic case。
2. Human calibration gate：S10 必须把 TMR / ChronAccRet 的 automatic side signals 校准到 human judgment；否则 evaluator stack 只能作 sampling / motivation，不能作主表 final evidence。
3. Attribution gate：S8 必须区分 cross-baseline failure pattern、EventT2M-specific mechanism 和不可外推机制；否则 failure attribution 只能是 case study。
4. Method gate：S9/S11 只有在 S8 给出明确 targeted mechanism 且 held-out / human eval 有提升时，才进入 ICLR/ICML 方法贡献；generic reward guidance 只能作为 baseline。

最近工作压力对应的 plan 检查点：

- [[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]]：当前只能作为反例和 historical reference；若要重新写入 S7 backbone column，必须先通过 generated-motion scale sanity。
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_AToM_Aligning_Text_to_Motion_Model_Event_Level_GPT4Vision_Reward|AToM]]：S10 必须让 MoDebug 的 evaluator / human calibration 更可控、更可复查；S8 必须提供 AToM reward alignment 之外的 failure attribution。
- [[paperAnalysis/Motion_Generation/ECCV_2024/2024_ChroAccRet_Chronologically_Accurate_Retrieval_for_Temporal_Grounding_of_Motion_Language_Models|ChronAccRet]]：ordering plan 不能只是复用 shuffle；S7/S10 需要给 generated-motion diagnostic 和 evaluator reliability boundary。
- [[paperAnalysis/Motion_Generation/AAAI_2026/2026_ReAlign_Bilingual_Text_to_Motion_Generation_via_Step_Aware_Reward_Guided_Alignment|ReAlign]] 与 [[paperAnalysis/Motion_Generation/ICLR_2026/2026_EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Generation|EasyTune]]：S9 若没有 S8-driven targeted correction，就不要写成方法贡献。
- [[paperAnalysis/Motion_Generation/ICLR_2026/2026_Motion_R1_Enhancing_Motion_Generation_Decomposed_CoT_RL_Binding|Motion-R1]] 与 [[paperAnalysis/Motion_Generation/arXiv_2026/2026_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generation|MoRL]]：若未来转方法论文，S11 必须证明 targeted correction 的收益不是更强 reasoning / reward framework 的自然替代。

**Plan consequence**：后续推进不应被“当前未完成所以不可投”干扰；真正的 go/no-go 在 S7/S8/S10。若 S8 attribution 有深度但 S9 方法不成立，EventProbe 单篇仍是有效路线；若 S8 attribution 不能闭合，则应降级为 workshop / diagnostic report，而不是硬推 PerceptGuide。

## 1. 核心叙事链路

```
event 增强数据集（贡献低，已有 HumanML3D-E）
  → failure 诊断 protocol（贡献中）
    → failure 根因归因（贡献中高，核心差异化）
      → 针对性方法改进（贡献中高，需具体设计）
```

这条链路的价值在于：诊断不只是描述 failure 分布，而是揭示根因；方法不是通用 reward guidance，而是针对归因发现的具体 failure mode 做修复。两者互相支撑，构成完整叙事。

Idea-A（EventProbe）覆盖链路前半段：诊断 + 归因。Idea-B（PerceptGuide）覆盖后半段：方法改进。如果合并成稿，链路完整；如果分投，各自也有独立价值。

## 2. 两条并行 Idea

### Idea-A: EventProbe — 事件级诊断与归因

**核心问题**：现有 full-level metrics 系统性漏掉多事件 motion generation 中的 omission、ordering violation 与 hard-negative semantic collapse。

**核心输出**：
1. 难度可控的 event-counterfactual diagnostic protocol（drop / hard-replace / shuffle）
2. Human-calibrated evaluator 可靠性边界
3. **Failure attribution analysis**（核心差异化）：omission 与 attention 分配、event embedding 坍缩、denoising trajectory 的关系

**不再作为独立贡献点**：scorer-selection leakage、cross-evaluator consistency——这些是实验卫生，不是贡献。

**Unified temporal evaluator 状态**：现在不启动独立实现。当前更合理的路径是先用 S7 建立多 baseline / 多 bucket 的 event-counterfactual 诊断表，用 S8 明确 failure attribution，用 S10 做 human calibration。只有当这些证据表明 TMR、ChronAccRet 和 human labels 能被稳定校准到同一 temporal reliability scale 时，才新增 unified temporal evaluator 任务；否则它只作为报告层面的 calibrated evaluator stack，而不是新的模型/指标贡献。

### Idea-B: PerceptGuide — 针对性方法改进

**核心问题**：现有 T2M 模型在多事件 prompt 下缺乏对子事件 presence/ordering 的边际敏感性。

**核心输出**：
1. Event-marginal reward model（对每个子事件的 counterfactual perturbation 有边际响应）
2. Masked-event perception loss（约束 reward 确实依赖目标 event）
3. Inference-time diffusion gradient correction（不改生成器参数）

**方法设计应由 Idea-A 的归因发现驱动**：如果归因发现 omission 的根因是 attention 分配不均，方法应针对 attention 做修正；如果根因是 event embedding 坍缩，方法应针对 embedding 做分离。通用 reward guidance 只是 baseline 方法。

**当前方法与归因驱动的分歧**：S2/S4 的 frozen TMR embedding + MLP reward head 是先行 baseline 路径，不是已经由 S8 归因支持的 targeted correction。S8 完成后必须执行一次方法方向 gate：若归因显示主要根因是 attention 分配、event embedding collapse 或 denoising trajectory 的特定失败模式，S9 需要重新设计为 targeted guidance；通用 reward-gradient 路线只能保留为 baseline 对照。

**Reward / RL 边界**：本文档中已经完成或排期的 reward step 都不是 RL。S2 是监督式 pairwise ranking / masked-event perception 训练；S4 是 step-wise 判别力诊断；S9 是 inference-time gradient guidance，不更新 policy，也没有 value function 或 rollout credit assignment。若未来要做 Motion-R1 / MoRL 式 RL，需要另开独立 step，并重新定义 policy、reward、optimization objective、sampling budget 和 held-out evaluator。

### 当前证据边界

1. EventT2M paper-native full-level hygiene 曾通过：released `hml3d.ckpt` 与论文 HumanML3D standard 和 HumanML3D-E condition2/3/4 指标接近，clean retrain 与 pretrained 同量级。2026-05-11 `2ac5ea8` 又恢复了 `003245` epoch135 单样本 scale sanity。两者仍只能作为 reproducibility / diagnostic 记录，不能证明 EventT2M 当前可作为 MoDebug final backbone 或 evaluator。
2. EventProbe 的核心 empirical claim 仍待 S7/S10 闭合：`full_level_safety` 与 event-level failure 的弱相关或不相关必须由多 baseline 诊断和 human calibration 支撑，不能仅由 FID/R-Precision 的定义推出。
3. `cross-evaluator safe-drop agreement = 73.32%` 和 `5plus = 63.75%` 是强 motivation / sampling signal，说明自动 evaluator 可能存在高事件数盲区；但在 human calibration 前，它不是 standalone final evaluator 结论。
4. PerceptGuide 的通用 reward-gradient 路线增量有限。S2/S4 只承担 reward probe / baseline 角色；S9 的 paper-level 方法差异化必须等 S8 归因结果决定，并需要显式记录 S8→S9 方法方向 gate。
5. S2 reward route 已通过 presence/omission 快速失败与 full-training gate：S2a/S2aa 在 5000/1000 子集上 3 seeds 的 same-protocol reward improvement 为 `+0.1643`，95% CI `[+0.1512, +0.1774]`；S2b 在完整 eligible split 上 3 seeds 的 val same-protocol reward improvement 为 `+0.2242`，95% CI `[+0.2134, +0.2351]`，test split observation improvement 为 `+0.1875`，95% CI `[+0.1742, +0.2008]`。该证据支持继续 R_pres / omission reward 路线到 S4，但仍是 `dev_metric` / observation，不能写成 final guidance improvement；replace/shuffle 在 S2b 中仍是 eval-only，不能作为 S4 go/no-go。
6. S2b no-event-mask loss ablation 目前只有 seed `20260502`，只能作为 shortcut diagnostic；若 S11 要把 masked-event perception loss 写成正式消融，必须补到 3 seeds。S3 已补 EventT2M pretrained 64-sample / 256-row per-head multi-step replay，但 automatic head filtering gate 未过；该产物是 S8-pre / human review input，不是归因结论。
7. S4 formal full run 已完成 machine gate：`reward_stepwise_gt_presence_full_text_vs_drop_text_paired_accuracy = 0.9389`，Wilson 95% CI `[0.9309,0.9461]`，`n_evaluable=3799`，role=`dev_metric`，used_for=`selection`。该结果只说明 S2b reward 对 EventT2M `cfg_predicted_x0` trajectory 有 drop-only 判别信号；human visual review 与 reward distribution review 前，不能写成 motion event correctness 或 guidance improvement。

## 3. 共享基础设施与 P0 Gates

### 3.1 数据域统一

| 组件          | 当前数据域                                                  | 目标数据域       | 行动                                                                                                                       |
| ----------- | ------------------------------------------------------ | ----------- | ------------------------------------------------------------------------------------------------------------------------ |
| Event-T2M   | HumanML3D-E                                            | HumanML3D-E | 已对齐                                                                                                                      |
| native TMR  | HumanML3D-E                                            | HumanML3D-E | 已对齐                                                                                                                      |
| ChronAccRet | HumanML3D-E adapter + `train_bert_orig` retrain sanity | HumanML3D-E | done：pretrained+adapter 可用；`train_bert_orig` sanity 已完成；不是论文 event-enhanced / negative-training retrain，不改变 evaluator 定位 |

ChronAccRet 数据域统一方案：
1. **最小方案**：写 adapter 将 HumanML3D-E event decomposition 转为 ChronAccRet 输入格式，在 official pretrained model 上直接推理。
2. **retrain sanity 方案**：用 HumanML3D-E adapter 数据按 ChronAccRet codebase 的 `train_bert_orig` 路径 retrain，作为数据域统一 sanity；该路径未开启 ChronAccRet 论文中的 event-enhanced / negative-training objective，也没有对应 event branch 的 loss/gradient 回传，因此不是论文 event-enhanced / negative-training 训练设置的 reproduction 或新的 paper contribution。
3. **判断标准**：先跑最小方案，比较指标差异。差异 < 5pp 则最小方案可用；否则 retrain 是必要修复项。
4. **当前结果**：pretrained+adapter ordering 和 omission 与旧 `humanml3d_subset` 记录差异均 < 5pp；`train_bert_orig` retrain sanity 后 CAR 小幅提升，但它只说明 adapter 数据可训练/可评估，不能和 ChronAccRet 论文 event-enhanced / negative-training 训练设置直接比较，也没有改变 ChronAccRet 在 MoDebug 中的 evaluator 角色。

### 3.2 P0 Gates

| Gate                                 | 状态                                                                        | 阻塞范围                                                                                                                                       |
| ------------------------------------ | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| P0-G1: EventT2M backbone reliability | reopened / failed for current generated-motion audit：Table 1 + Table 3 指标接近，但 released 与 `epoch_135` 单样本骨架量纲均异常 | 当前不能作为 MoDebug generated-motion backbone；下一步换 backbone 或先做 clean upstream sanity repair |
| P0-G2: ChronAccRet 数据域统一             | done：pretrained+adapter 通过 <5pp gate；`train_bert_orig` retrain sanity 已补充 | ChronAccRet 可作为 HumanML3D-E ordering / omission evaluator 资产；仍需报告 coverage、evaluable、condition_pair、model_source、training_objective 和 role |
| P0-G3: Reward-metric fairness        | active rule：held-out 分离已固定                                                | Idea-B 的 final claim                                                                                                                       |

### 3.3 EventT2M Backbone Decision

EventT2M retrain uncertainty 已重新打开。当前决策：

1. Keep this section as historical EventT2M decision provenance only.
2. Current revalidation record: [[paperIDEAs/MoDebug/2026-05-11_eventt2m-clean-4090-revalidation-log]].
3. 2026-05-11 after-fix diagnostic for HumanML3D-E sample `003245`: GT `joints_abs_mean=0.3901`; epoch135 generated `joints_abs_mean=0.4229`; `RESOLVED_NOISE_PREDICTION_TYPE sample`.
4. Role: `diagnostic` / `observation`; used_for=`sanity_recheck`; limitations=`single sample, not final evaluator, not backbone-selection evidence, not full-level safety`.
5. Drift: old_plan -> new_plan -> evidence -> affected_docs -> next_action = `treat 2026-05-06 scale abnormality as current blocker` -> `restore scale-sanity progress but keep evidence role bounded` -> `2ac5ea8 after-fix re-vis returns to HumanML3D scale on 003245` -> `this progress note; EventT2M revalidation log` -> `choose route-specific active evidence before reopening EventT2M-generated claims`.

### 3.4 Evaluator 栈（从旧 evaluator-status-summary 吸收）

| Evaluator           | 角色                                                  | 不能承担                                              |
| ------------------- | --------------------------------------------------- | ------------------------------------------------- |
| Event-T2M self eval | full-level safety（FID, R-Precision, matching score） | event-level judge                                 |
| native TMR          | omission / semantic side signal                     | formal ordering; duration; standalone final judge |
| ChronAccRet         | formal ordering evidence; omission cross-check      | duration; held-out human calibration              |
| AToM                | nearest-work reproduction reference                 | MoDebug 主 judge                                   |

旧 subset / side-signal 关键数值（详细 artifact 路径见 `blocked/legacy_eventt2m/2026-04-29_modebug-evaluator-status-summary.md`）：

| Canonical metric                                 | Evaluator                | Protocol                   | Value    | n / evaluable | Role                       | Used for      | Finding / limitation          |
| ------------------------------------------------ | ------------------------ | -------------------------- | -------- | ------------- | -------------------------- | ------------- | ----------------------------- |
| `tmr_gt_pres_full_vs_drop_paired_acc`            | native TMR               | omission dataset eval      | `0.7044` | `3799`        | `side_signal`              | `observation` | -                             |
| `tmr_gt_pres_full_vs_replace_paired_acc`         | native TMR               | omission dataset eval      | `0.8363` | `3799`        | `side_signal`              | `observation` | -                             |
| `chronaccret_gt_subset_ordering_car`             | ChronAccRet              | shuffle_text ordering      | `0.6474` | `2331/2333`   | `formal_ordering_evidence` | `observation` | -                             |
| `chronaccret_gt_subset_full_vs_drop_paired_acc`  | ChronAccRet              | omission_event             | `0.7300` | `2333`        | `cross_check`              | `observation` | -                             |
| `cross_evaluator_safe_drop_agreement`            | native TMR + ChronAccRet | safe-drop agreement        | `73.32%` | `1608`        | `diagnostic`               | `observation` | evaluator disagreement signal |
| `cross_evaluator_aligned_replace_agreement`      | native TMR + ChronAccRet | aligned-replace agreement  | `81.65%` | `1608`        | `diagnostic`               | `observation` | evaluator disagreement signal |
| `tmr_gt_hard_lexical_full_vs_replace_paired_acc` | native TMR               | hard-replace lexical pilot | `0.6523` | `512`         | `diagnostic`               | `observation` | easy-negative inflation risk  |

ChronAccRet HumanML3D-E 数据域更新：

> 注：以下 `pretrained+adapter` 指 official ChronAccRet pretrained `best_model_mt.pt` 直接跑 HumanML3D-E adapter 数据；`train_bert_orig retrain sanity` 指用同一 HumanML3D-E adapter train/val split 按 ChronAccRet codebase 的 `train_bert_orig` 路径训练 200 epoch 后的 checkpoint。`train_bert_orig` 使用 `model.noneg=True`，loader 虽生成 `shuffled_events`，但训练 forward 不会把 shuffled text 作为 chronological hard negative 加入 contrastive loss，也未开启 ChronAccRet 论文 event-enhanced / negative-training loss 或对应 event 分支梯度回传。因此该 sanity **不能**与论文 event-enhanced / negative-training 训练设置直接比较；两者都不是 held-out human evaluator。

| Record                                     | Value                                                                             |
| ------------------------------------------ | --------------------------------------------------------------------------------- |
| `chronaccret_hml3de_adapter_test_coverage` | test event-cache ids `4196/4196`; event groups `12515`; multi-event groups `7137` |
| Event-count buckets                        | `1=5378`, `2=4503`, `3=1835`, `4=536`, `5plus=263`                                |
| Artifact                                   | `linkedCodebases/ChronAccRet/data/humanml3de_adapter/adapter_manifest.json`       |
| Role / used_for                            | `diagnostic` / `observation`                                                      |
| Limitation                                 | adapter follows HumanML3D-E event cache, not raw `data_test.npy` row count        |

Condition pair 含义：

| Condition pair              | 比较双方                             | Reported value 含义                                                                    |
| --------------------------- | -------------------------------- | ------------------------------------------------------------------------------------ |
| `full_text vs shuffle_text` | 同一 motion 下，完整正确顺序文本 vs 事件顺序打乱文本 | CAR / paired accuracy：`score(motion, full_text) > score(motion, shuffle_text)` 的样本比例 |
| `full_text vs drop_text`    | 同一 motion 下，完整文本 vs 删除一个事件后的文本   | paired accuracy：模型更偏好完整文本的样本比例                                                       |
| `full_text vs replace_text` | 同一 motion 下，完整文本 vs 替换一个事件后的文本   | paired accuracy：模型更偏好完整文本的样本比例                                                       |

Pretrained+adapter eval（2026-05-02）：

| Canonical metric                                           | Model source                              | Protocol                                 | Condition pair            | Paired accuracy / CAR | n / evaluable | Artifact                                                                                        | Role                       | Limitations                                                   |
| ---------------------------------------------------------- | ----------------------------------------- | ---------------------------------------- | ------------------------- | --------------------- | ------------- | ----------------------------------------------------------------------------------------------- | -------------------------- | ------------------------------------------------------------- |
| `chronaccret_gt_hml3de_adapter_ordering_car`               | official pretrained `best_model_mt.pt`    | shuffle_text ordering                    | full_text vs shuffle_text | `0.6579`              | `2406/2408`   | `linkedCodebases/ChronAccRet/output/chronaccret_official_pretrained/hml3de_adapter_shuffle_eval/shuffle_event.yaml`   | `formal_ordering_evidence` | 2 degenerate multi-event samples skipped                      |
| `chronaccret_gt_hml3de_adapter_full_vs_drop_paired_acc`    | official pretrained `best_model_mt.pt`    | omission_event default target/distractor | full_text vs drop_text    | `0.7297`              | `2408/2408`   | `linkedCodebases/ChronAccRet/output/chronaccret_official_pretrained/hml3de_adapter_omission_eval/omission_event.yaml` | `cross_check`              | automatic evaluator, not held-out human calibration           |
| `chronaccret_gt_hml3de_adapter_full_vs_replace_paired_acc` | official pretrained `best_model_mt.pt`    | omission_event default replacement       | full_text vs replace_text | `0.8584`              | `2408/2408`   | `linkedCodebases/ChronAccRet/output/chronaccret_official_pretrained/hml3de_adapter_omission_eval/omission_event.yaml` | `cross_check`              | default length-matched distractor, not aligned-replace policy |

`train_bert_orig` retrain sanity（2026-05-03；no event-enhanced objective）：

| Canonical metric                             | Model source                                                          | Training setting                                                                        | Protocol              | Condition pair            | Paired accuracy / CAR | n / evaluable | Artifact                                                                                                                        | Role                                | Interpretation                                                                                                                                                                  |
| -------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------- | ------------------------- | --------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `chronaccret_gt_hml3de_retrain_ordering_car` | `output/chronaccret_hml3de_retrain_official_setting/best_model_mt.pt` | ChronAccRet codebase `train_bert_orig`, `model.noneg=True`, data_dir changed to HumanML3D-E adapter, 200 epochs; no event-enhanced / negative-training loss | shuffle_text ordering | full_text vs shuffle_text | `0.6725`              | `2406/2408`   | `linkedCodebases/ChronAccRet/output/chronaccret_hml3de_retrain_official_setting/hml3de_retrain_shuffle_eval/shuffle_event.yaml` | `diagnostic` / sanity | +1.46pp over pretrained+adapter CAR; only a HumanML3D-E adapter train/eval sanity. It is not comparable to ChronAccRet paper event-enhanced / negative-training setting because the corresponding loss and gradient path were not enabled |

### 3.5 Held-Out 分离规则（从旧 heldout-eval-policy 吸收）

硬规则：`reward scorer/protocol ≠ final main-table evaluator/protocol`

- 被用作 reward 的 scorer 只能报告为 dev_metric
- Final claim 必须来自未参与 tuning/selection/reward 的 evaluator 或 human calibration
- Held-out 是实验卫生，不是贡献点

## 4. 已完成资产（从旧 evaluator-status / exec-plan 吸收）

| 资产                             | Artifact 路径                                                                                                      | 状态                                          |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| TMR omission dataset eval      | `linkedCodebases/EventT2M-codes-main/logs/planb_tmr_native_omission_dataset_eval/`                               | done                                        |
| ChronAccRet ordering full eval | `linkedCodebases/ChronAccRet/output/chronaccret_official_pretrained/subset_eval/`                                                      | done                                        |
| ChronAccRet omission protocol  | `linkedCodebases/ChronAccRet/output/chronaccret_official_pretrained/omission_eval/`                                                    | done                                        |
| Safe-drop consistency          | `linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/`                                             | done                                        |
| Aligned-replace consistency    | `linkedCodebases/EventT2M-codes-main/logs/modebug_aligned_replace_eval/`                                         | done                                        |
| Hard-replace lexical pilot     | `linkedCodebases/EventT2M-codes-main/logs/modebug_hard_replace_eval/`                                            | done (512 rows)                             |
| Observation pool               | `linkedCodebases/EventT2M-codes-main/logs/modebug_observation_pool/`                                             | done (64 samples)                           |
| G1/G2 attention observation    | `linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/g1g2_condition_probe_64samples_step10/` | done (head-averaged only, per-head pending) |
| Event-T2M self eval            | 见 archived evaluator-status-summary                                                                              | done                                        |
| EventT2M retrain sanity        | `linkedCodebases/EventT2M-codes-main/logs/event/eval/retrain_sanity_20260502/`                                   | done：native full-level 训练卫生通过               |
| EventT2M condition sanity      | `linkedCodebases/EventT2M-codes-main/logs/event/eval/paper_condition_sanity_20260502/`                          | done：论文 Table 3 condition2/3/4 基本复现         |
| ChronAccRet HumanML3D-E adapter | `linkedCodebases/ChronAccRet/data/humanml3de_adapter/`                                                          | done：test event-cache coverage `4196/4196` |
| ChronAccRet pretrained+adapter ordering eval | `linkedCodebases/ChronAccRet/output/chronaccret_official_pretrained/hml3de_adapter_shuffle_eval/`                                   | done：`chronaccret_gt_hml3de_adapter_ordering_car` CAR `0.6579`, n/evaluable `2406/2408` |
| ChronAccRet pretrained+adapter omission eval | `linkedCodebases/ChronAccRet/output/chronaccret_official_pretrained/hml3de_adapter_omission_eval/`                                  | done：drop paired accuracy `0.7297`, replace paired accuracy `0.8584`, n/evaluable `2408/2408` |
| ChronAccRet HumanML3D-E `train_bert_orig` retrain sanity | `linkedCodebases/ChronAccRet/output/chronaccret_hml3de_retrain_official_setting/`                                                | done：ChronAccRet codebase `train_bert_orig`, HumanML3D-E adapter data, 200 epochs；未开启论文 event-enhanced / negative-training loss |
| ChronAccRet `train_bert_orig` CAR sanity eval | `linkedCodebases/ChronAccRet/output/chronaccret_hml3de_retrain_official_setting/hml3de_retrain_shuffle_eval/`                     | done：`chronaccret_gt_hml3de_retrain_ordering_car` CAR `0.6725`, n/evaluable `2406/2408`；not comparable to paper event-enhanced / negative-training setting |
| S2a/S2aa reward sanity probe | `/data/public/ripemangobox/Motion/EventT2M-codes/logs/modebug_reward_s2aa_probe_seed*_a5b928c/` | done + pass：3-seed val same-protocol reward improvement mean `+0.1643`, 95% CI `[+0.1512,+0.1774]` |
| S2b reward full training | `/data/public/ripemangobox/Motion/EventT2M-codes/logs/modebug_reward_s2b_full_seed*_8c53a87/` | done + pass：3-seed val same-protocol reward improvement mean `+0.2242`, 95% CI `[+0.2134,+0.2351]`；best checkpoints saved |

## 5. Exec 详细（GPT 可执行级别）

### S0: EventT2M Retrain Sanity

**状态**：done。native full-level 与 HumanML3D-E condition2/3/4 训练卫生通过。
**详细命令和协议**：见 [[2026-05-01_modebug-eventt2m-retrain-sanity-plan]]。
**结果摘要**：

| Source / checkpoint            | Dataset / setting  | FID          | R@3          | Matching / MM-Dist | Role              |
| ------------------------------ | ------------------ | ------------ | ------------ | ------------------ | ----------------- |
| PDF Table 1 Event-T2M          | HumanML3D standard | `0.056±.002` | `0.842±.002` | `2.711±.005`       | paper reference   |
| Local released `hml3d.ckpt`    | HumanML3D standard | `0.04765`    | `0.8418`     | `2.7150`           | pretrained sanity |
| Best clean retrain `epoch_135` | HumanML3D standard | `0.04064`    | `0.8478`     | -                  | retrain sanity    |

| Source                      | HumanML3D-E condition | FID       | R@3      | Role              |
| --------------------------- | --------------------- | --------- | -------- | ----------------- |
| PDF Table 3                 | C2                    | `0.079`   | `0.824`  | paper reference   |
| Local released `hml3d.ckpt` | C2                    | `0.07883` | `0.8241` | pretrained sanity |
| PDF Table 3                 | C3                    | `0.137`   | `0.790`  | paper reference   |
| Local released `hml3d.ckpt` | C3                    | `0.14405` | `0.7868` | pretrained sanity |
| PDF Table 3                 | C4                    | `0.265`   | `0.767`  | paper reference   |
| Local released `hml3d.ckpt` | C4                    | `0.26238` | `0.7578` | pretrained sanity |

**结论**：released `hml3d.ckpt` 与论文 Table 1 / Table 3 指标接近，且 clean retrain 同量级；这只确认 EventT2M paper-native full-level hygiene。2026-05-11 scale-sanity repair 还原了单样本进度，但不能继续作为 MoDebug current backbone evidence。

### S1: ChronAccRet 数据域统一（最小方案）

**状态**：done。HumanML3D-E adapter 已生成并通过 loader / smoke / full eval。
**目标**：让 ChronAccRet 在 HumanML3D-E 数据上运行，消除数据域歧义。

Exec 步骤：
1. 读取 ChronAccRet 的 `event_texts` 输入格式（`linkedCodebases/ChronAccRet/` 下的 data loader）
2. 读取 HumanML3D-E 的 event decomposition 格式（`.tamr_hml3de_gt_events_test.json`）
3. 写 adapter 脚本：`linkedCodebases/ChronAccRet/scripts/hml3de_adapter.py`，将 HumanML3D-E event decomposition 转为 ChronAccRet 输入格式
4. 在 ChronAccRet official pretrained model 上用 adapter 数据跑 ordering eval 和 omission eval
5. 比较 pretrained+adapter 结果与原 `humanml3d_subset` 结果，记录差异
6. 用 ChronAccRet codebase `train_bert_orig` 路径在 HumanML3D-E adapter train/val split 上补 retrain sanity，并在 test split 上跑 CAR；该路径未开启论文 event-enhanced / negative-training objective，不用于和论文 event-enhanced / negative-training 训练设置对比

**执行结果**：

| Item | Result / artifact |
| --- | --- |
| Git archive | ChronAccRet HEAD `9b29a4591d9d888e135d719318554adee8f4a7e7`; tag `modebug-pre-hml3de-adapter-20260502-173022`; patch `artifacts/modebug/chronaccret_git_archive/chronaccret_uncommitted_20260502-173038.patch` |
| Adapter script | `linkedCodebases/ChronAccRet/scripts/hml3de_adapter.py` |
| Adapter data | `linkedCodebases/ChronAccRet/data/humanml3de_adapter/` |
| Test coverage | event-cache ids `4196/4196`; missing base annotations `0`; event groups `12515`; multi-event groups `7137` |
| Event-count buckets | `1=5378`, `2=4503`, `3=1835`, `4=536`, `5plus=263` |
| Loader smoke | ChronAccRet `TextMotionDataset` loads adapter test split; motion shape `224 x 263`; event fields readable |

| Eval | Model source | Canonical metric | Paired accuracy / CAR | n / evaluable | Artifact | Role |
| --- | --- | --- | --- | --- | --- | --- |
| Ordering eval | official pretrained + adapter | `chronaccret_gt_hml3de_adapter_ordering_car` | `0.6579` | `2406/2408` | `linkedCodebases/ChronAccRet/output/chronaccret_official_pretrained/hml3de_adapter_shuffle_eval/shuffle_event.yaml` | `formal_ordering_evidence` |
| Omission eval | official pretrained + adapter | `chronaccret_gt_hml3de_adapter_full_vs_drop_paired_acc` | `0.7297` | `2408/2408` | `linkedCodebases/ChronAccRet/output/chronaccret_official_pretrained/hml3de_adapter_omission_eval/omission_event.yaml` | `cross_check` |
| Omission eval | official pretrained + adapter | `chronaccret_gt_hml3de_adapter_full_vs_replace_paired_acc` | `0.8584` | `2408/2408` | `linkedCodebases/ChronAccRet/output/chronaccret_official_pretrained/hml3de_adapter_omission_eval/omission_event.yaml` | `cross_check` |
| Ordering eval | `train_bert_orig` retrain sanity on HumanML3D-E adapter | `chronaccret_gt_hml3de_retrain_ordering_car` | `0.6725` | `2406/2408` | `linkedCodebases/ChronAccRet/output/chronaccret_hml3de_retrain_official_setting/hml3de_retrain_shuffle_eval/shuffle_event.yaml` | `diagnostic` / sanity |

**完成标准**：done。pretrained+adapter 结果与旧 `humanml3d_subset` 记录 `chronaccret_gt_subset_ordering_car` value `0.6474` 和 `chronaccret_gt_subset_full_vs_drop_paired_acc` value `0.7300` 的差异均 < 5pp；`train_bert_orig` retrain sanity CAR `0.6725` 只作为数据域训练/评估 sanity，不把 ChronAccRet 升级为 held-out final evaluator，也不能和 ChronAccRet 论文 event-enhanced / negative-training 训练设置直接比较。
**预估**：done。
**并行**：与 S2a/S3/S7 并行。

### S2: B-EXP1 Reward Model Probe → Full Training

**状态**：S2a/S2aa done + pass；S2b done + pass。当前只支持 R_pres / omission reward 路线进入 S4。
**目标**：验证 event-marginal reward 是否能从 frozen TMR 表征中学到比原生余弦相似度更强的 event counterfactual 判别信号。
**定位**：frozen TMR encoder + MLP head 只是 cheap MVP/probe，不是已验证的运动 reward 范式，也不预设为最终方法贡献。S2 可并行推进，但在 S2a 通过和 S8 归因前不扩展为完整 PerceptGuide sprint。
**Reward design / RL 边界**：S2 是 supervised pairwise ranking reward model training，不是 RL。当前 reward design 只覆盖 R_pres / omission：正例为 `(motion, full_text)`，负例为 `(same_motion, drop_text)` 和 masked-event variant；loss 是 margin ranking + masked-event perception loss。R_ord、hard-replace 和其他扩展 reward 尚未进入训练目标。

#### S2-Pre: 数据清单 gate

启动训练前先写 manifest，记录以下字段，避免 split / corruption / evaluator 角色漂移：

1. 数据路径：
   - train motion: `linkedCodebases/EventT2M-codes-main/dataset/HumanML3D-E/data_train.npy`
   - val motion: `linkedCodebases/EventT2M-codes-main/dataset/HumanML3D-E/data_val.npy`
   - test motion: `linkedCodebases/EventT2M-codes-main/dataset/HumanML3D-E/data_test.npy`
   - train events: `linkedCodebases/EventT2M-codes-main/dataset/HumanML3D-E/.tamr_hml3de_gt_events_train.json`
   - val events: `linkedCodebases/EventT2M-codes-main/dataset/HumanML3D-E/.tamr_hml3de_gt_events_val.json`
   - test events: `linkedCodebases/EventT2M-codes-main/dataset/HumanML3D-E/.tamr_hml3de_gt_events_test.json`
2. split size、event-count bucket、corruption policy、n/evaluable、coverage。
3. role：S2/S4 输出一律标为 `dev_metric`；train/val 用于训练和选择，test 不参与 S2a 调参。
4. code/data version：EventT2M backbone、TMR encoder、ChronAccRet adapter manifest 的路径或 commit/tag。

#### S2a: 10 epoch sanity probe

Exec 步骤：
1. 构造 5000 个 train pairs 子集：
   - 正例：`(GT_motion, full_event_text)`。
   - 主训练负例只用 `drop_text`；`aligned_replace` / `shuffle_text` 如生成，仅作为 eval-only diagnostics，不参与 S2a/S2b pass/fail。
2. 同协议 baseline：
   - cosine baseline：`cosine_sim(motion_emb, text_emb)`。
   - optional linear/logistic head：只作为最小学习头对照，避免 MLP 容量解释不清。
3. MVP 架构：
   - 冻结 TMR motion/text encoder。
   - 输入：`concat(motion_embedding, text_embedding)`。
   - 输出：scalar reward score。
   - MLP 只做 2-3 layers，不引入 token-level cross-attention 或 step-aware 输入。
4. Loss：
   - `L_rank = max(0, 0.1 - (score(motion, full_text) - score(motion, drop_text)))`
   - `L_event_mask = max(0, 0.1 - (score(motion, full_text) - score(motion, mask_event_i_text)))`
   - `L = L_rank + 0.5 * L_event_mask`
   - 不在 S2a 默认加入 score norm 正则；若出现 score scale 漂移，再作为 debug 选项记录。
5. 训练配置：
   - Optimizer: AdamW, lr=`1e-4`, weight_decay=`0.01`
   - Batch size: `64`（单卡 3090）
   - Epochs: `10`
   - seeds: `3`
   - 训练脚本路径：`linkedCodebases/EventT2M-codes-main/src/train_reward_model.py`
6. 验证：
   - 在同一 val split / corruption policy / paired_acc protocol 下报告 MLP、cosine baseline、linear/logistic head 的 paired accuracy。
   - 主指标：`reward_dev_gt_pres_full_vs_drop_paired_acc`；replace/shuffle 指标只作 diagnostic-only observation，不参与 go/no-go。

**S2a Go/No-Go**：

1. 主通过标准：MLP 的 3 seeds 平均 paired_acc 必须显著高于同 protocol cosine baseline，mean improvement `>= 2pp` 且 improvement 的 `95% CI > 0`。
2. 历史参考：`tmr_gt_pres_full_vs_drop_paired_acc = 0.7044` 只作为旧 omission dataset eval 的 `side_signal` reference floor，不参与同协议统计检验。若 drop 主指标未通过，默认不进入 S2b；replace/shuffle 不能救回 gate，除非先加入对应训练目标并重设 go/no-go。
3. 若 S2a 失败：取消 S2b 完整训练，优先转向升级路径。

#### 2026-05-03 S2a/S2aa result

**结论**：presence/omission reward quick-fail gate 通过，可以继续 S2b；但只支持 R_pres / `full_text vs drop_text` 主线，不支持提前把 replace/shuffle 或 final guidance claim 写成已验证。

运行配置：

- date: `2026-05-03`
- code artifact: remote EventT2M repo commit `a5b928c`
- script: `/data/public/ripemangobox/Motion/EventT2M-codes/src/run_modebug_reward_s2a_probe.py`
- data source: HumanML3D-E `data_train.npy` / `data_val.npy`
- event source: `data_*.npy` text entry with longest decomposed list；`.tamr_hml3de_gt_events_train.json` / `.tamr_hml3de_gt_events_val.json` 记录在 manifest 中作为数据清单路径
- train rows: `5000`
- val rows: `1000`
- encoded motion rows per seed: `6000 = 5000 train + 1000 val`
- unique text embeddings per seed: about `30710`
- model: frozen TMR embeddings + MLP reward head, input `concat(motion_embedding, text_embedding)`, hidden dim `256`
- training: `10` epochs, batch size `64`, AdamW lr `1e-4`, rank loss uses `drop only`, replace/shuffle are eval-only
- role: `dev_metric`
- used_for: `selection`
- limitation: S2a deliberately excludes test split and full train split; it is a quick-fail probe, not full reward training or held-out final evaluation

Artifacts:

| Seed | Artifact path | Log | Status |
| --- | --- | --- | --- |
| `20260502` | `/data/public/ripemangobox/Motion/EventT2M-codes/logs/modebug_reward_s2aa_probe_seed20260502_a5b928c/s2a_summary.json` | `/data/public/ripemangobox/Motion/EventT2M-codes/logs/modebug_reward_s2aa_probe_seed20260502_a5b928c/s2aa_train.log` | `END status=0` |
| `20260503` | `/data/public/ripemangobox/Motion/EventT2M-codes/logs/modebug_reward_s2aa_probe_seed20260503_a5b928c/s2a_summary.json` | `/data/public/ripemangobox/Motion/EventT2M-codes/logs/modebug_reward_s2aa_probe_seed20260503_a5b928c/s2aa_train.log` | `END status=0` |
| `20260504` | `/data/public/ripemangobox/Motion/EventT2M-codes/logs/modebug_reward_s2aa_probe_seed20260504_a5b928c/s2a_summary.json` | `/data/public/ripemangobox/Motion/EventT2M-codes/logs/modebug_reward_s2aa_probe_seed20260504_a5b928c/s2aa_train.log` | `END status=0` |

Same-protocol dev metric:

| Seed       | Canonical metric                                 | Evaluator / scorer    | Protocol       | Condition pair         | Value    | n      | Role         | Used for  | Limitation                                           |
| ---------- | ------------------------------------------------ | --------------------- | -------------- | ---------------------- | -------- | ------ | ------------ | --------- | ---------------------------------------------------- |
| `20260502` | `tmr_cosine_dev_gt_pres_full_vs_drop_paired_acc` | frozen TMR cosine     | S2a val subset | full_text vs drop_text | `0.6870` | `1000` | `dev_metric` | baseline  | subset baseline, not historical side-signal protocol |
| `20260502` | `reward_dev_gt_pres_full_vs_drop_paired_acc`     | frozen TMR + MLP head | S2a val subset | full_text vs drop_text | `0.8590` | `1000` | `dev_metric` | selection | reward-side dev result only                          |
| `20260503` | `tmr_cosine_dev_gt_pres_full_vs_drop_paired_acc` | frozen TMR cosine     | S2a val subset | full_text vs drop_text | `0.6870` | `1000` | `dev_metric` | baseline  | subset baseline, not historical side-signal protocol |
| `20260503` | `reward_dev_gt_pres_full_vs_drop_paired_acc`     | frozen TMR + MLP head | S2a val subset | full_text vs drop_text | `0.8380` | `1000` | `dev_metric` | selection | reward-side dev result only                          |
| `20260504` | `tmr_cosine_dev_gt_pres_full_vs_drop_paired_acc` | frozen TMR cosine     | S2a val subset | full_text vs drop_text | `0.6870` | `1000` | `dev_metric` | baseline  | subset baseline, not historical side-signal protocol |
| `20260504` | `reward_dev_gt_pres_full_vs_drop_paired_acc`     | frozen TMR + MLP head | S2a val subset | full_text vs drop_text | `0.8570` | `1000` | `dev_metric` | selection | reward-side dev result only                          |

Aggregate go/no-go:

| Statistic | Value |
| --- | --- |
| Mean improvement over same-protocol cosine baseline | `+0.1643` |
| 95% CI of improvement | `[+0.1512, +0.1774]` |
| S2a criterion | pass: mean improvement `>= 0.02` and CI lower bound `> 0` |

Interpretation:

1. 只有 `6000` 个 motion embeddings 是预期结果：S2a 命令显式设定 `--max-train-samples 5000 --max-val-samples 1000`，预计算阶段只编码 train+val 子集，test split 不参与训练、选择或 quick-fail go/no-go。
2. 每个 seed 约 3 分钟完成是合理的：TMR encoder 冻结，只预计算 embedding；训练对象是小 MLP，`5000` train rows × `10` epochs × batch size `64`，约 `790` optimizer steps。
3. S2a 支持继续原方案的 R_pres / omission reward branch：frozen TMR embedding 中确实存在 MLP 可利用的 `full_text` vs `drop_text` 判别信号。
4. S2a 不支持直接扩展到 R_ord 或 hard-replace claim：replace/shuffle 在当前实现中是 eval-only，且不是训练 loss 的目标。S2b 若要覆盖 replace/shuffle，需要单独加入相应训练目标并重新记录 go/no-go。
5. S2a 不支持 final evaluator claim：reward scorer 被用于 selection，后续 S9/S11 的 final claim 必须走 held-out evaluator / human calibration。

#### S2b: full reward training

S2a 已通过，S2b 已在 4090 双卡完成 3-seed full training。当前结论只覆盖 R_pres / omission reward full training；replace/shuffle 只作为诊断列，除非显式加入训练 loss 和对应 go/no-go。

Exec 步骤：
1. 扩展到完整 train split，保留 val early stopping。
2. 仍以 frozen TMR + MLP 作为 baseline reward，不把它写成最终方法贡献。
3. 训练 50-100 epoch，early stopping on val paired_acc。
4. 记录与 cosine baseline 和 no event-mask loss 的差异；linear/logistic head 只作为后续可选 sanity，不列入本次 S2b 完成标准。
5. test split 只用于冻结配置后的报告，不用于选择超参。

**失败后的升级路径**：

1. 引入 noisy / step-aware reward input（ReAlign-like），专门服务 S4/S9 的 denoising step 判别。
2. 微调或重训 reward encoder（EasyTune/ReAlign-like），不再假设 frozen global TMR embedding 足够。
3. 若 S2a 通过但事件粒度仍不足，再考虑 PAPO/ZOMG 启发的 event-wise head 或更细粒度特征交互；这些不进入 S2a MVP。

#### 2026-05-03 S2b result

**结论**：S2b full training 通过。frozen TMR + MLP reward head 在完整 eligible split 上稳定超过同协议 cosine baseline，可以作为 S4 step-wise reward discriminative pilot 的 R_pres checkpoint。该结论不是 final guidance improvement，也不验证 R_ord / hard-replace。

运行配置：

- date: `2026-05-03`
- remote host: `4090`, dual RTX 4090
- code artifact: remote EventT2M repo commit `8c53a87`
- script: `/data/public/ripemangobox/Motion/EventT2M-codes/src/run_modebug_reward_s2a_probe.py`
- run_stage: `s2b`
- ablation_name: `full_rpres_main`
- data source: `/data/public/ripemangobox/Motion/datasets/HumanML3D/HumanML3D-E/data_train.npy` / `data_val.npy` / `data_test.npy`
- event source: `.tamr_hml3de_gt_events_train.json` / `.tamr_hml3de_gt_events_val.json` / `.tamr_hml3de_gt_events_test.json`
- selection: `min_events=2`, `max_train_samples=0`, `max_val_samples=0`, `max_test_samples=0`
- selected rows: train `18574/24546`, val `1152/1530`, test `3799/4646`
- selected event-count buckets: train `2=11250, 3=5064, 4=1648, 5plus=612`; val `2=675, 3=328, 4=112, 5plus=37`; test `2=1940, 3=1185, 4=435, 5plus=239`
- model: frozen TMR embeddings + MLP reward head, input `concat(motion_embedding, text_embedding)`, hidden dim `256`, dropout `0.1`
- training: `50` max epochs, batch size `64`, AdamW lr `1e-4`, weight decay `0.01`, margin `0.1`, `lambda_event_mask=0.5`, early stopping patience `8`
- rank loss corruption: `drop only`; replace/shuffle usage: `eval only`
- role: val metrics are `dev_metric` used_for=`selection`; test metrics are `dev_metric` used_for=`observation`
- limitation: reward scorer is trained/selected in this protocol; S9/S11 claims still require held-out evaluator / human calibration

Artifacts:

| Seed       | Artifact path                                                                                        | Checkpoints                                        | Status         |
| ---------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------- | -------------- |
| `20260502` | `/data/public/ripemangobox/Motion/EventT2M-codes/logs/modebug_reward_s2b_full_seed20260502_8c53a87/` | `s2b_best_checkpoint.pt`, `s2b_last_checkpoint.pt` | `END status=0` |
| `20260503` | `/data/public/ripemangobox/Motion/EventT2M-codes/logs/modebug_reward_s2b_full_seed20260503_8c53a87/` | `s2b_best_checkpoint.pt`, `s2b_last_checkpoint.pt` | `END status=0` |
| `20260504` | `/data/public/ripemangobox/Motion/EventT2M-codes/logs/modebug_reward_s2b_full_seed20260504_8c53a87/` | `s2b_best_checkpoint.pt`, `s2b_last_checkpoint.pt` | `END status=0` |

Same-protocol dev/test metric:

| Seed       | Best epoch | `tmr_cosine_dev_gt_pres_full_vs_drop_paired_acc` | `reward_dev_gt_pres_full_vs_drop_paired_acc` | Val improvement | `tmr_cosine_test_gt_pres_full_vs_drop_paired_acc` | `reward_test_gt_pres_full_vs_drop_paired_acc` | Test observation improvement |
| ---------- | ---------- | ------------------------------------------------ | -------------------------------------------- | --------------- | ------------------------------------------------- | --------------------------------------------- | ---------------------------- |
| `20260502` | `32`       | `0.6936`                                         | `0.9288`                                     | `+0.2352`       | `0.7041`                                          | `0.9016`                                      | `+0.1974`                    |
| `20260503` | `37`       | `0.6936`                                         | `0.9132`                                     | `+0.2196`       | `0.7041`                                          | `0.8947`                                      | `+0.1906`                    |
| `20260504` | `19`       | `0.6936`                                         | `0.9115`                                     | `+0.2179`       | `0.7041`                                          | `0.8787`                                      | `+0.1745`                    |

Aggregate go/no-go:

| Statistic                                                            | Value                                                         |
| -------------------------------------------------------------------- | ------------------------------------------------------------- |
| Val mean improvement over same-protocol cosine baseline              | `+0.2242`                                                     |
| Val 95% CI of improvement                                            | `[+0.2134, +0.2351]`                                          |
| Test observation mean improvement over same-protocol cosine baseline | `+0.1875`                                                     |
| Test observation 95% CI of improvement                               | `[+0.1742, +0.2008]`                                          |
| S2b criterion                                                        | pass: val mean improvement `>= 0.02` and CI lower bound `> 0` |

Diagnostic-only columns:

| Metric                                              | Mean / note                                    | Role                         | Limitation                                                                         |
| --------------------------------------------------- | ---------------------------------------------- | ---------------------------- | ---------------------------------------------------------------------------------- |
| `reward_test_gt_pres_full_vs_event_mask_paired_acc` | 3-seed mean `0.8771`, 95% CI `[0.8662,0.8879]` | `diagnostic` / `observation` | supports event-mask sensitivity check, not final evaluator                         |
| `reward_test_gt_pres_full_vs_replace_paired_acc`    | seed values `0.6489 / 0.6373 / 0.6152`         | `diagnostic` / `observation` | replace was eval-only and below cosine baseline; do not claim hard-replace success |
| `reward_test_gt_ord_full_vs_shuffle_paired_acc`     | seed values `0.5333 / 0.5157 / 0.5225`         | `diagnostic` / `observation` | shuffle was eval-only and near random; do not claim ordering reward                |

No event-mask loss ablation, single seed:

| Ablation          | Seed       | `lambda_event_mask` | Best epoch | `reward_dev_gt_pres_full_vs_drop_paired_acc` | `reward_test_gt_pres_full_vs_drop_paired_acc` | `reward_test_gt_pres_full_vs_event_mask_paired_acc` | Note                                                                                           |
| ----------------- | ---------- | ------------------- | ---------- | -------------------------------------------- | --------------------------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `full_rpres_main` | `20260502` | `0.5`               | `32`       | `0.9288`                                     | `0.9016`                                      | `0.8847`                                            | main setting                                                                                   |
| `no_event_mask`   | `20260502` | `0.0`               | `24`       | `0.9071`                                     | `0.8876`                                      | `0.8630`                                            | one-seed ablation only; suggests event-mask term helps, not enough for a formal ablation claim |

Formal ablation boundary:

| Candidate claim | Current evidence | Required before S11 formal claim |
| --- | --- | --- |
| Masked-event perception loss helps | one seed (`20260502`) no-event-mask comparison, lower dev/test/mask scores | rerun no-event-mask ablation for seeds `20260503` and `20260504`; report 3-seed mean, 95% CI, n/evaluable, role, and held-out evaluator behavior |
| Reward model handles hard-replace / ordering | diagnostic-only S2b replace/shuffle columns | add replace/shuffle to training objective and define a separate go/no-go before using them as method claims |

Interpretation:

1. S2b 支持继续原有 R_pres / omission reward branch，并将 best checkpoint 交给 S4 的 step-wise discriminative pilot。
2. Frozen TMR global embeddings 的能力上限在 presence/omission 上没有卡死 MLP head；MLP 显著超过同协议 cosine baseline。
3. replace/shuffle 诊断不支持提前扩展 claim：当前训练 loss 只使用 `drop_text`，replace/shuffle 只是观察列。
4. S2b test split 没参与训练或 early stopping，但仍属于 reward-side protocol observation；不能替代 S11 的 held-out evaluator / human calibration。

**完成标准**：S2a manifest、baseline comparison、3-seed val paired_acc 和 go/no-go 决策记录已完成；S2b full-train reward checkpoints 与 dev/test paired_acc 已完成；no-event-mask loss 目前仅记录 single-seed diagnostic，不能作为 S11 formal ablation，正式消融需补 3 seeds。
**预估**：done。
**并行**：与 S3/S7 并行。不依赖 EventT2M retrain（用 GT motion）。

### S3: Baseline Failure Attribution Infrastructure — Per-Head / Gradient / Trace Schema

**状态**：partial machine-complete / machine-pending / human-pending；EventT2M pretrained per-head multi-step replay 与 metrics-only human review packet 已完成，G3 与 S7-aligned failure trace 未完成。
**目标**：建立跨 S7 baselines 的 failure attribution infrastructure：统一 baseline / case trace schema，并为可插桩模型记录 per-head attention、multi-step denoising signals 和 gradient sensitivity。S3 的产物服务于 S8 的跨 baseline 归因和 S9 的 method-direction gate，而不是只为 EventT2M 内部补日志。

Exec 步骤：
1. 定义统一 attribution trace schema：
   - 必需字段：`baseline_id`, `model_source`, `checkpoint`, `sample_id`, `event_count_bucket`, `condition_pair`, `corruption_policy`
   - 结果字段：`evaluator`, `canonical_metric`, `success_failure_label`, `n/evaluable`, `role`, `limitations`
   - 可选白盒字段：`attention_trace`, `denoising_step_trace`, `gradient_sensitivity`, `token_event_alignment`
2. 对 S7 所有 baseline 生成 Tier-0 baseline failure trace：
   - 优先覆盖通过 B1 的 MoGenTS / MoMask；EventT2M 只在重新通过 generated-motion sanity 后加入 backbone column
   - 所有 failure / success cases 必须能回连到 S7 diagnostic table
3. 对可插桩模型生成 Tier-1 white-box attribution trace：
   - 保存 per-head attention weights，而不是只保存 head-averaged attention
   - 保存 multi-step denoising trace，避免只看 step 10
   - 记录 event token 与 event span 的 alignment
4. 对 EventT2M 实现 G3 frozen-forward gradient sensitivity：
   - 在 `sample_motion()` 的窄作用域中局部启用 gradient（绕过 `@torch.no_grad()`）
   - 计算 event condition 对 latent / motion frames 的 gradient mass
   - 输出：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/g3_gradient_sensitivity/`
   - 该结果是 EventT2M case study，不自动外推为所有 baseline 的通用机制
5. 初步 sanity：
   - 检查 failure cases 与 success cases 是否都有 trace
   - 检查每个 baseline 的 coverage、缺失原因和白盒可用性

**2026-05-05 machine-complete 子任务**：
- 本地 synthetic instrumentation smoke passed：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/s3_preflight_synthetic_smoke_20260505/smoke_summary.json`。
- 本地 real per-head smoke completed：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/s3_preflight_real_004965_step2_perhead_20260505/`，4 condition rows，`has_per_head_metrics=true`。
- 本地 EventT2M pretrained 64-sample total / 256-condition-row per-head multi-step replay completed：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/s3_perhead_64samples_step10_20260505/`；`observations.jsonl` 为 256 rows，shape `[2, 8, 25, 11]`，每条 attention record 含 8 heads，所以 `n_samples_total=64`、`n_conditions=4`、`n_condition_rows=256`、`attention_records=10240`，但不是 `64 samples per head`。Analyzer 输出 `has_per_head_metrics=true`，automatic head-filtering verdict 为 `fail_raw_attention_filtering_gate`。
- S3 metrics-only human review queue completed：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/s3_perhead_64samples_step10_20260505/s3_human_review_packet_metrics_only_20260505.json`；该 packet 只排队 low-entropy / high-mass candidate heads，不包含 raw attention tensor heatmap 或 motion render。

**machine-pending / 未完成子任务**：
- `MP-S3-001`：补 G3 frozen-forward gradient sensitivity；当前缺少可复查 scalar target 与输出 schema，完成前不能写 gradient-based attribution。状态：post-closeout deferred / blocked-by-spec，不是正在排队运行。
- `MP-S3-002`：如需真正 heatmap，重跑 S3 instrumentation 并保存 raw attention tensor 或导出可视化；当前 artifact 只保存 per-head metric summaries。状态：post-closeout deferred / blocked-by-human-review-scope，不是正在排队运行。
- `MP-S3-003`：等 S7 产生 failure/success cases 后，将 S3 trace 回连到 S7 diagnostic table；完成前不能写 S8 failure correlation。

**human-pending / 未完成子任务**：
- `HP-S3-001`：人工审核 per-head attention heatmap / generated motion packet，确认低熵 head 是否是语义对齐、固定位置伪影、padding/tokenization 伪影，还是不可解释噪声。
- `HP-S3-002`：人工审查 metrics-only queue 中的 candidate heads 是否值得重跑 raw heatmap / motion render。

**完成标准**：生成跨 baseline 的 Tier-0 failure trace manifest；对通过 B1 的 replacement baselines 记录 attribution coverage、可插桩性、缺失原因和 limitations。EventT2M per-head / G3 只能作为 model-specific diagnostic，不是当前必需 backbone 产物。
**证据边界**：2026-05-05 per-head replay 只说明 EventT2M white-box trace 产物可生成；automatic head-filtering gate 未过，不能支撑 S8 attribution claim。EventT2M 的 per-head / G3 结果只能支持 EventT2M-specific mechanism claim；跨 baseline 归因 claim 必须来自 S7-aligned failure traces，并报告每个 baseline 的 attribution coverage。若其他 baseline 只有 black-box trace，S8 只能写作 cross-baseline failure pattern，不能写作 shared internal mechanism。
**预估**：1-2 周。
**并行**：与 S7/S4 并行；S7 的 case schema 是 S3 manifest 的源。

### S4: B-EXP2 Reward Discriminative Pilot (Go/No-Go)

**状态**：machine gate pass / human-pending。2026-05-03 4090 preflight 发现远端仓库没有独立 S4 runner；2026-05-05 已在本地实现 `src/run_modebug_reward_s4_stepwise_pilot.py`，并用 remote S2b full seed `20260502` artifact 完成 4-row sanity 与 3799-row formal full run。
**目标**：验证 reward model 在不同 denoising step 上的判别力。
**定位**：reward-guided diffusion diagnostic，不是 RL。S4 只检查 S2b reward 是否能在 denoising trajectory 上形成可用判别信号，不更新 generator 参数。

Exec 步骤：
1. 用 route-approved generated motions 生成 test split 样本；若使用 EventT2M，必须引用当前 revalidation log 和本轮 active protocol
2. 在每个 denoising step 上提取 `cfg_predicted_x0` motion feature state；不把 denoiser hidden state 或 noisy `prev_sample` 直接喂给 reward head
3. 对每个 `cfg_predicted_x0` 先做 EventT2M inverse transform，再经 TMR motion encoder 得到 256-d motion embedding；S2b `RewardHead` 只接收 `(TMR motion embedding, TMR text embedding)`
4. 主线只用 reward model 对 `full_text` vs `drop_text` 打分；`replace_text` / `shuffle_text` 只作为 diagnostic-only 曲线另表报告
5. 绘制 step-wise discriminative signal curve

**Go/No-Go 标准**：
- 主 gate 只使用 R_pres / omission：`reward_stepwise_gt_presence_full_text_vs_drop_text_paired_accuracy >= 0.70`，且 `95% CI` 下界 > `0.5`。这是 S4 step-wise dev metric，不复用 S2b 的 `reward_dev_gt_pres_full_vs_drop_paired_acc` 名称。
- `full_text vs replace_text` 和 `full_text vs shuffle_text` 只作为 diagnostic-only observation，不参与 S4 pass/fail；S2b 训练 loss 没有使用 replace/shuffle，因此不能用 hard-replace threshold 判断当前 checkpoint 是否通过。
- 如果主 gate 不通过：回退检查 perception loss 设计、step-wise reward input 或 reward model 架构。
- 如果需要把 hard-replace / ordering 纳入后续 gate：必须先加入对应训练目标，重新记录 train/val/test protocol、canonical metric、n/evaluable、role 和 go/no-go。

**2026-05-05 machine-complete 子任务**：
- S4 runner implemented：`linkedCodebases/EventT2M-codes-main/src/run_modebug_reward_s4_stepwise_pilot.py`；不更新 generator，不做 policy optimization。
- S4 smoke passed using local S2b smoke checkpoint：`linkedCodebases/EventT2M-codes-main/logs/modebug_reward_s4_stepwise_smoke_predx0_20260505/`。
- Remote S2b full seed `20260502` artifacts fetched to `artifacts/remote4090/modebug_s2b_full_seed20260502_8c53a87/`。
- S4 4-row sanity with full S2b seed `20260502` passed：`linkedCodebases/EventT2M-codes-main/logs/modebug_reward_s4_stepwise_full_seed20260502_sanity4_20260505/`，final step `reward_stepwise_gt_presence_full_text_vs_drop_text_paired_accuracy=1.0`，`n_evaluable=4`，role=`dev_metric`。
- S4 formal full run completed locally：`linkedCodebases/EventT2M-codes-main/logs/modebug_reward_s4_stepwise_full_seed20260502_20260505/`；`s4_step_rows.jsonl` 为 37990 rows，`state_kind=cfg_predicted_x0`，`n_evaluable=3799` final-step primary metric `reward_stepwise_gt_presence_full_text_vs_drop_text_paired_accuracy=0.9389`，Wilson 95% CI `[0.9309,0.9461]`，chance baseline `0.5`，role=`dev_metric`，used_for=`selection`。
- S4 posthoc audit completed：`linkedCodebases/EventT2M-codes-main/logs/modebug_reward_s4_stepwise_full_seed20260502_20260505/s4_posthoc_audit_20260505.json`；该 audit 明确 `cfg_predicted_x0` 是 CFG 合成后的 x0，并记录 replace/shuffle 只作 diagnostic observation。
- S4 score-review packet completed：`linkedCodebases/EventT2M-codes-main/logs/modebug_reward_s4_stepwise_full_seed20260502_20260505/s4_human_review_packet_scores_20260505.json`；该 packet 排队 final-step drop failures / near-margin / high-confidence successes，但不含 motion render。

**machine-pending / 未完成子任务**：
- `MP-S4-001`：若 human review 需要可视化，补 selected sample motion export / render runner；当前 S4 runner 只保存 score rows 和 provenance，不保存 rendered motion。

**human-pending / 未完成子任务**：
- `HP-S4-001`：人工抽查 denoising steps 的 generated motion / TMR embedding 是否合理，尤其检查 early-step OOD 与 final-step 高分但视觉缺失 dropped event 的样本。
- `HP-S4-002`：人工审核 reward score 分布和 failure cases；human review 前，S4 只能写作 reward-side diagnostic。

**预估**：machine gate done；human review pending。
**前置**：S2b checkpoint 已完成；优先使用 seed `20260502` 的 `s2b_best_checkpoint.pt`，并用另外两个 seed 做 sanity。

### S5: EventT2M Backbone 结果判读

**状态**：reopened / current generated-motion backbone blocked。
**Exec**：已比较 released pretrained、clean retrain checkpoint 和论文 Table 1 / Table 3 指标。因当前本地 `src/eval.py` 追加 retrieval YAML 导出且耗时无关，standard sanity 使用 `src/eval_native_only.py` 跑 native metrics；condition sanity 使用 paper condition2/3/4 配置。详细表格见 [[2026-05-01_modebug-eventt2m-retrain-sanity-plan#2026-05-02 Result]]。
**结论**：旧的 full-level reproducibility gate 不足以证明当前 generated-motion backbone 可用。2026-05-11 `003245` epoch135 单样本 scale sanity 已恢复到 HumanML3D 量级，但仍不能替代 route-specific S7/S8/S10 evidence。下一步应在新的单思路路线 note 中定义 EventT2M 的具体角色、协议和证据边界。

### S6: ChronAccRet 数据域统一结果判读

**状态**：done。
**Exec**：

| Comparison | HumanML3D-E adapter metric / value | Old subset metric / value | Difference | Gate |
| --- | --- | --- | --- | --- |
| Ordering | `chronaccret_gt_hml3de_adapter_ordering_car` = `0.6579` | `chronaccret_gt_subset_ordering_car` = `0.6474` | `< 5pp` | pass |
| Omission drop | `chronaccret_gt_hml3de_adapter_full_vs_drop_paired_acc` = `0.7297` | `chronaccret_gt_subset_full_vs_drop_paired_acc` = `0.7300` | `< 5pp` | pass |

**结论**：ChronAccRet HumanML3D-E pretrained+adapter 最小方案可用；`train_bert_orig` retrain sanity 使 CAR 从 `0.6579` 小幅提升到 `0.6725`，但该训练未开启论文 event-enhanced / negative-training loss 或对应梯度回传，只能作为数据域 sanity，不改变 ChronAccRet 在 MoDebug 中的定位。后续使用 ChronAccRet 时必须同时报告 adapter manifest coverage、evaluable 数、condition_pair、model_source、training_objective、role 和 limitations。
**S7 使用边界**：ChronAccRet 的 ordering CAR 约 `0.66-0.67`，不能直接当作真实 ordering failure rate。S7 若报告 generated motions 的 ordering violation 比例，必须同时报告 evaluator accuracy / confidence interval / human calibration 状态；human calibration 前只能写作 automatic ordering side evidence 或 formal ordering evidence with evaluator limitations。
**预估**：done。

### S7: 多 Baseline 诊断

**状态**：partial machine-complete / machine-pending / human-pending；S7 component eval 的 EventT2M/TMR/ChronAccRet 资产已存在，但完整 multi-baseline orchestrator 与 modern baseline generated-motion manifests 仍未补齐。
**目标**：在 historical anchors 和 modern baselines 上跑 event-counterfactual diagnostic protocol。
**核心验证**：EventProbe 的主 punchline 不是"FID 按定义不测 event correctness"，而是量化 full-level safety 与 human-calibrated event failure 在哪些 baseline、event bucket、corruption 难度下弱相关、不相关或出现 tradeoff。

**当前执行收缩（S7-min）**：
- 第一轮 baseline 上限：MoGenTS 与 MoMask；MotionGPT 只作二线 fallback。
- 第一轮 condition 只锁 `full_text vs drop_text` 和 `full_text vs shuffle_text`。
- 第一轮 bucket 主看 `3 / 4 / 5plus`；`2` bucket 只保留为参考列。
- 完成 `S7-min` 前，不扩到 ReAlign / EasyTune / Motion-R1 / MoRL。

Exec 步骤：
1. Baseline 列表（按可用性排序）：
   - MoGenTS（完整 training / inference / eval，本地 checkpoint 与 joints outputs 齐全）
   - MoMask（完整 training / inference / eval，本地 checkpoint 与 joints outputs 齐全）
   - MotionGPT（第二梯队 fallback）
   - DART（范式偏控制 / SMPL，暂不进第一轮）
2. 对每个 baseline：用 HumanML3D-E test split 生成 motion → 跑 TMR omission + ChronAccRet ordering + full-level safety；完整 multi-baseline table 还需要 baseline ckpt/source、prompt adapter、motion format / length protocol、generated-motion manifest 和 evaluator coverage
3. 按 event-count bucket（2/3/4/5plus）报告
4. 记录 full-level metrics 与 event-level failure 的相关性，分开报告 automatic side signals 与 human-calibrated failure rates

**S7 规格前置 / DS review 要求**：
- 每个 baseline 必须先通过完整链路 gate：`training_entry`、`inference_entry`、`eval_entry` 都存在；只提供 inference / weights、只做 retrieval 或只做 editor 的 repo 不能进入 backbone 表。
- 每个 baseline 必须先记录 checkpoint/source repo、commit 或 release tag、prompt adapter、motion format、length protocol、sampling seed、generated-motion manifest、evaluator coverage 与 limitations。
- ChronAccRet / TMR 输出在 human calibration 前只能写作 automatic side signal 或带 evaluator limitations 的 formal ordering evidence；S7 的 event-side failure signals pending human calibration，不能直接写成真实 failure rate。

**2026-05-05 machine-complete 子任务**：
- S7 diagnostic inventory generated locally：`artifacts/modebug/s7_diagnostic_inventory_20260505/s7_diagnostic_inventory.json`；统一收录 EventT2M / TMR / ChronAccRet component results 与 baseline inventory，明确 `diagnostic_inventory_only` 边界，不把 component eval 静默升级成 final table。
- EventT2M/TMR omission dataset eval 已存在并可复用：`linkedCodebases/EventT2M-codes-main/logs/planb_tmr_native_omission_dataset_eval/summary.json`；`num_samples=3799`，`tmr_native_full_vs_drop_paired_accuracy=0.7044`，`tmr_native_full_vs_replace_paired_accuracy=0.8363`。这是 automatic side signal，不是 held-out final evaluator。
- Generation observation condition manifest 已存在并验证通过：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/condition_manifest_summary.json`；`sample_count=64`，`condition_rows=256`，4 个 condition 齐全，`fixed_seed_complete=true`。
- Aligned-replace manifest + TMR eval + TMR/ChronAccRet consistency 已存在并可复用：`linkedCodebases/EventT2M-codes-main/logs/modebug_aligned_replace_eval/`；`manifest_rows=1608`，TMR `full>replace paired_accuracy=0.8358`，TMR/ChronAccRet aligned-replace agreement `0.8165`。
- Hard-replace lexical pilot 已存在并可复用：`linkedCodebases/EventT2M-codes-main/logs/modebug_hard_replace_eval/tmr_hard_replace_summary.json`；`scored_rows=512`，TMR `full>replace paired_accuracy=0.6523`，相对 old aligned-replace accuracy `-0.1835`，支持 easy-negative inflation 风险。
- Safe-drop consistency summary 已存在并可复用：`linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/summary.json`；safe-drop agreement `0.7332`，`5plus` bucket agreement `0.6375`。

**machine-pending / 未完成子任务**：
- `MP-S7-001`：补单一 S7 orchestrator，把通过 B1 的 replacement baselines、ChronAccRet ordering/omission、full-level safety 和 evaluator coverage 汇成统一 per-baseline table。
- `MP-S7-002`：补外部 modern baselines 的 full-loop eligibility record、generated-motion manifest、checkpoint/source、prompt adapter、motion format / length protocol、sampling seed、evaluator coverage。
- `MP-S7-003`：若要把 AToM / ReAlign 等纳入同表，需要先验证本地 linked codebase 的 checkpoint 可用性与 MoDebug prompt/protocol 对齐，而不是直接复用仓库存在性。

**human-pending / 未完成子任务**：
- `HP-S7-001`：human calibration 前，不能把 current TMR / ChronAccRet disagreement 或 bucket 差异写成真实 failure rate 或主表 final evidence。

**完成标准**：per-baseline per-bucket diagnostic table。
**预估**：2-3 周。
**前置**：S5 done；下一步受各 baseline 代码/ckpt 可用性影响。

### S8: Failure Attribution — Omission/Ordering 归因

**状态**：blocked by S3 + S7 部分结果。
**目标**：对 failure cases 做 attention/gradient 归因，回答"为什么 fail"。

**当前执行收缩（S8-min）**：
- 第一问：是否存在 cross-baseline failure pattern。
- 第二问：通过 B1 的 replacement backbone 是否存在可复查 mechanism signal；EventT2M white-box trace 只作 historical / model-specific diagnostic。
- G3 / raw heatmap / motion packet 只在 `S7-aligned selected cases` 上跑；未回连到 S7 case table 的 artifact 不进入 S8 claim。
- 若 `S8-min` 只能支撑 failure pattern 而不能支撑 internal mechanism，优先保 EventProbe 单篇，不强推 S9 targeted contribution。

Exec 步骤：
1. 从 S7 结果中提取 TMR omission failure/success cases（full_vs_drop 判错/判对样本），并同步提取 ChronAccRet ordering failure/success cases；每类都记录 evaluator role、coverage、human calibration 状态和 limitations
2. 从 S3 的 attribution traces 中，按 baseline 分层分析 failure cases vs success cases：所有 baseline 使用 Tier-0 failure trace；可插桩 baseline 额外使用 per-head / multi-step / gradient traces
3. 区分 cross-baseline failure pattern、EventT2M-specific mechanism 和可迁移 targeted correction 证据
4. 对可插桩模型输出：failure-attention correlation table + failure-gradient correlation table
5. **关键问题**：omission failure 是否与 attention 分配缺失相关？ordering failure 是否与 attention peak 时序错位相关？这些发现是跨 baseline pattern，还是只存在于特定 backbone？
6. 若出现不属于当前 event-level 主线的扩展证据，只记录为非主线候选，不自动转入 S9 方法设计

**S8 alignment criteria / DS review 要求**：
- `aligned failure/success trace` 至少要求同一 `sample_id` / prompt family、同一 corruption policy、同一 condition_pair、同一 evaluator schema、同一 motion length protocol、可追溯 generated-motion manifest 和可复查 seed / decoding protocol。
- black-box baseline 只进入 Tier-0 failure trace；只有保存了 white-box trace 的 baseline 才能进入 internal mechanism claim。
- S3 per-head replay 在 S7-aligned case table 产生前只能作 S8-pre review input；G3 未完成前不能写 gradient correlation table。
- S8 unblock trigger：S8 只能在 S7 至少产出 MoGenTS / MoMask 的 S7-aligned generated-motion manifest 与 failure/success labels 后启动；最小 batch 要覆盖 TMR omission `full_text vs drop_text` 和 ChronAccRet ordering `full_text vs shuffle_text` 两类 condition_pair，且每类至少 100 个可复查 generated-motion cases 或记录达不到 100 的 coverage blocker。
- G3 dependency clarification：这里的 G3 指 S3 的 EventT2M frozen-forward gradient sensitivity artifact。S8 可以先做 Tier-0 black-box failure pattern table，但任何 `failure-gradient correlation` 或 EventT2M internal mechanism claim 必须等 G3 artifact 完成。

**完成标准**：failure attribution report，包含 per-head + multi-step attention artifact、gradient sensitivity artifact、failure/success correlation 数值和可视化；旧 G1/G2 64-sample step-10 head-averaged observation 只能作为 routing evidence，不能单独支撑 attention attribution claim。
**外推边界**：black-box baseline 只能支持 failure pattern / evaluator correlation；white-box trace 才能支持 internal mechanism claim。S8 必须在结论中标明每个机制是 cross-baseline、model-specific，还是尚不可判定。
**预估**：1-2 周。
**前置**：S3 + S7 部分结果。

### S9: B-EXP3 Inference-Time Reward Guidance / Targeted Correction

**状态**：blocked by S4 pass + S8→S9 方法方向 gate.
**目标**：在 EventT2M 上实现推理期 reward guidance baseline；若 S8 给出明确根因，再转为 targeted correction。
**定位**：S9 当前不是 RL training；默认不更新 generator 参数。generic reward gradient 只是 baseline pilot，paper-level 方法贡献必须来自 S8 驱动的 targeted correction。

Exec 步骤：
1. 实现 inference-time reward gradient injection：
   - 在 denoising loop 的指定 step range 内，计算 reward model 对当前 latent 的梯度
   - 用梯度更新 latent（不更新模型参数）
   - 超参：guidance weight λ_g, step range [t_start, t_end], gradient clipping
2. 先只开 R_pres（omission reward），限制在 3-4 event 样本
3. 同时记录 full-level safety（FID/R-Precision delta）和 event-side evidence
4. 如果 S8 的归因发现了具体 failure mode，设计针对性的 guidance 策略（而不只是通用 reward gradient）
5. **Hard gate**：S8 必须明确记录根因类型、证据 artifact、correlation / effect size、limitations 和 `method_direction_decision`，并说明证据来自 cross-baseline pattern 还是 EventT2M-specific white-box trace。若根因指向 attention、event embedding collapse 或 denoising trajectory failure，S9 必须转向对应 targeted correction；通用 reward-gradient 只能保留为 baseline。

S8→S9 方法方向 gate：

| S8 attribution finding | S9 action |
| --- | --- |
| no clear targeted failure mechanism | keep generic reward gradient as baseline-only pilot; do not frame as main contribution |
| omission correlates with attention under-allocation / head specialization failure | design attention-targeted correction or attention reweighting before paper-level S9 |
| omission correlates with event embedding collapse | design event embedding separation / contrastive correction before paper-level S9 |
| ordering correlates with temporal attention peak mismatch | design ordering-aware step/temporal guidance; do not reuse R_pres checkpoint as ordering method |

**完成标准**：guidance 前后的 event-side + full-level metrics 对比；paper-level S9 方法 claim 需要引用 S8 的 `method_direction_decision`，否则只能写作 generic reward-gradient baseline pilot。
**预估**：2-3 周。
**前置**：S4 pass；S5 已完成；S8 attribution report 必须先给出 `method_direction_decision`。在 S8 完成前，只允许运行 R_pres reward-gradient baseline pilot，不允许把通用 reward gradient 写成 paper-level 方法路线。

### S10: Human Eval

**状态**：blocked by S7 + S8。
**目标**：200-300 条 targeted human calibration，作为 evaluator 可靠性的 anchor。
**定位**：S10 是 EventProbe 的核心证据，不是附录。cross-evaluator inconsistency 只能决定优先标注哪些样本；final event-level reliability claim 必须由 human-TMR / human-ChronAccRet agreement 和 per-bucket human accuracy 支撑。

**当前执行收缩（S10a pilot）**：
- 先做 60-80 条小规模人工审核，其中 `>=50%` 是自动评分分歧大的样本。
- 先把 omission / ordering / severity 的人工标注规则写清楚，再决定是否扩到 200-300 条正式人工评测。
- 若这轮小规模审核里人工口径不稳，或自动分数和人工判断对不上，就先修规则和抽样，不扩表。
- 2026-05-06 已补上 `pretrained-only` 的人工审核 MVP 工具链：review manifest、视频渲染脚本、Gradio 审核 app；下一步是先跑一个小 slice，把流程走通。

Exec 步骤：
1. 从 S7 + S8 结果中选样本：high-disagreement cases 占 50%+，覆盖 4 个 baseline × 多 event bucket
2. 标注维度：omission（是否遗漏子动作）、ordering（子动作顺序是否正确）、severity（1-3 级）
3. 输出：human-TMR agreement, human-ChronAccRet agreement, per-bucket human accuracy

**预估**：2-3 周。
**前置**：S7 + S8。

### S11: Perception Ablation + Held-Out Eval

**状态**：blocked by S9。
**Exec**：
1. Ablation: global reward vs event-marginal reward; no perception loss vs masked-event perception loss
2. Held-out: 如果 reward 用 TMR，final eval 用 ChronAccRet + human eval；反之亦然
3. 如果 reward-side 提升但 held-out 不提升，只能写 development result
4. Masked-event perception loss 默认写作消融 / shortcut check；除非它在 held-out evaluator 和 human eval 上带来额外提升，否则不写成独立方法贡献

**预估**：1-2 周。
**前置**：S9。

### S12: 成稿形式决策 + 写作

**状态**：blocked by S10 + S11。
**决策标准**：见 §7。
**预估**：2-3 周。

## 6. 进度总表

| Step | 任务 | 前置 | 预估 | 并行关系 | 状态 |
|------|------|------|------|---------|------|
| S0 | EventT2M backbone reliability | — | reopened | — | restored for single-sample scale sanity; still diagnostic only |
| S1 | ChronAccRet 数据域统一 | — | done | 与 S2a/S3/S7 并行 | done：HumanML3D-E adapter 可用 |
| S2a | B-EXP1 reward sanity probe | — | done | 与 S3/S7 并行 | done + pass：3-seed frozen TMR MLP > same-protocol cosine baseline |
| S2b | B-EXP1 reward full training | S2a pass | done | 与 S3/S7 并行 | done + pass：3-seed full eligible split，R_pres / omission reward checkpoint 已保存 |
| S3 | Baseline failure attribution infrastructure | S7 schema partial | 1-2 周 | 与 S7/S4 并行 | partial：EventT2M pretrained per-head multi-step replay + metrics-only review queue done；G3 + raw heatmap/render + S7-aligned traces + human review pending |
| S4 | B-EXP2 step-wise reward go/no-go | S2b checkpoint | human review pending | 与 S3 并行 | machine gate pass：formal full run `0.9389`, Wilson 95% CI `[0.9309,0.9461]`, `n=3799`; reward-side diagnostic only |
| S5 | EventT2M backbone 结果判读 | S0 | reopened | — | diagnostic scale sanity restored on `003245`; active route evidence still required |
| S6 | ChronAccRet 统一结果判读 | S1 | done | — | done：adapter/旧 subset 差异 < 5pp |
| S7 | 多 baseline 诊断 | B1 replacement smoke | 2-3 周 | 与 S4 并行 | pending：EventT2M component assets 仅作 diagnostic inventory；MoGenTS / MoMask manifest 与统一 orchestrator pending |
| S8 | Failure attribution: 归因分析 | S3 + S7 部分 | 1-2 周 | waits for S3/S7 | blocked |
| S9 | B-EXP3 inference-time reward guidance / targeted correction | S4 pass + S8→S9 方法方向 gate | 2-3 周 | S9a only after S4 pass；S9b after S8 method_direction_decision | blocked |
| S10 | Human eval | S7 + S8 | 2-3 周 | 与 S9 并行 | blocked |
| S11 | Ablation + held-out eval | S9 | 1-2 周 | 与 S10 并行 | blocked |
| S12 | 成稿决策 + 写作 | S10 + S11 | 2-3 周 | — | blocked |

### 关键路径

```
B1 (MoGenTS / MoMask replacement smoke) ──→ S7 (多baseline) ──→ S8 (归因) ──→ S10 (human eval) ──→ S12
                                                                                          ↑
S2a (reward probe done) ──→ S2b (reward full train done) ──→ S4 (drop-only go/no-go) ──→ S9a generic reward-guidance baseline only
                                                        ↑                                  │
S3 (baseline attribution trace + optional model-specific traces) ──→ S8 (归因 + method_direction_decision) ──→ S9b S8-gated targeted correction ──→ S11 ─────────┘
                                                        │
```

### 当前可立即并行推进

1. **先把 replacement smoke 跑通**：优先补 MoGenTS / MoMask 三样本 static skeleton smoke 和 full-loop eligibility manifest。
2. **只对选中的 case 补归因材料**：只在已经进样本总表的 case 上补 trace 回连、G3、heatmap 和 motion packet；没回连到样本行的材料不进 S8。
3. **先把小规模人工审核跑通**：先写规则，再用 high-disagreement case 组 60-80 条 pilot packet。今天已经补了 pretrained-only 人工审核 MVP 脚本链，下一步是先跑一个 slice。
4. **S4 人工复核继续保留，但降为支线**：它仍有用，但不再和 S7/S8/S10 主路径抢优先级。

## 7. 成稿形式决策标准（S12 时判断）

当前默认收缩路线：**EventProbe 单篇优先**。PerceptGuide 只有在 S8→S9 形成明确 targeted mechanism，且 S11 held-out / human eval 提升后，才作为 ICLR/ICML 方法贡献进入合并论文或单独方法论文。

| 条件 | 成稿形式 |
|------|---------|
| Idea-A failure attribution 有深度 + Idea-B guidance 有效 | 合并为一篇完整论文：诊断→归因→方法 |
| Idea-A 有深度但 Idea-B guidance 失败 | Idea-A 单独投（diagnostic + attribution paper） |
| Idea-B guidance 有效但 Idea-A attribution 浅 | Idea-B 单独投（method paper，evaluation section 自包含） |
| 两个都有深度且体量足够 | 分投两篇 |
| 两个都不够深 | 合并为 workshop / short paper |

## 8. Drift Notes

- 2026-05-11 v14: restored EventT2M scale-sanity progress after `2ac5ea8`. HumanML3D-E `003245` epoch135 after-fix generated joints returned to HumanML3D scale (`joints_abs_mean=0.4229`, GT `0.3901`) with resolved `prediction_type=sample`. Role remains `diagnostic` / `observation`; do not promote it into final evaluator, backbone-selection evidence, or full-level safety.
- 2026-05-06 v13: historical pre-revalidation scale-sanity blocker. This row is retained only as drift provenance; use v14 and [[paperIDEAs/MoDebug/2026-05-11_eventt2m-clean-4090-revalidation-log]] for the current statement.
- 2026-05-06 v12: supplemented a pretrained-only human-review MVP toolchain under `linkedCodebases/EventT2M-codes-main/`: `src/run_pretrained_human_review_manifest.py`, `src/run_modebug_render_review_videos.py`, and `app_pretrained_human_review.py`. This does not close full S7 multi-baseline diagnostics; it is the working entry for S10a small-scale human review.
- 2026-05-06 v11: after DS + multi-agent execution review, this note was reorganized into an execution-first entrance. Added current decisions / shortest critical path / human-machine split / hard stop rules; narrowed the immediate path to `S7-min -> S8-min -> S10a pilot`; moved the time-space parallel-control idea to [[paperIDEAs/MoDebug/2026-05-01_modebug-spatiotemporal-extension-backlog]]. No experimental conclusion changed in this re-organization.
- 2026-05-05 v10: executed the remaining safe machine-only S7 work instead of starting new training: generated `artifacts/modebug/s7_diagnostic_inventory_20260505/s7_diagnostic_inventory.json` to unify EventT2M / TMR / ChronAccRet component results and local baseline inventory under an explicit diagnostic-only boundary. No new S3 G3/heatmap run and no S9 pilot run were started.
- 2026-05-05 v9: re-audited remaining machine-only scope after S4 closeout. Corrected the earlier over-conservative stop: S7 still has machine-complete EventT2M/TMR/ChronAccRet component eval assets that can be reused for table closure without human intervention, but there is still no reason to start new S3 G3/heatmap jobs or S9 pilot runs. Reframed S7 from pure plan-ready to partial machine-complete; remaining machine work is orchestrator/table closure and baseline manifest completion, not fresh training.
- 2026-05-05 v8: S4 formal full run completed and posthoc audited. Final-step `reward_stepwise_gt_presence_full_text_vs_drop_text_paired_accuracy=0.9389`, Wilson 95% CI `[0.9309,0.9461]`, `n_evaluable=3799`, role=`dev_metric`, used_for=`selection`; machine gate pass but human visual/reward distribution review remains pending. S4 runner was tightened to require `prediction_type=sample`, score CFG-combined `cfg_predicted_x0`, use structured event rows, and record future-run provenance / CI / chance baseline. S3 metrics-only review packet was prepared, but raw heatmap/render and G3 remain pending. S7/S8 remain blocked/spec-stage until S7-aligned failure/success traces exist.
- 2026-05-05 v7: DS + multi-agent review confirmed S4/S7 plan-ready and S8 blocked status, with corrections: S4 must score TMR embeddings from `cfg_predicted_x0`, not raw denoising latents; S7 full table needs baseline ckpt/source + generated-motion manifest; S8 must include both TMR omission and ChronAccRet ordering failure/success cases. Implemented S3 per-head artifact path and S4 step-wise runner. S3 EventT2M pretrained per-head replay completed but automatic head-filtering gate failed, so it is S8-pre/human-review input only. S4 smoke and 4-row full-checkpoint sanity passed; formal full run started in tmux `modebug_s4_full_seed20260502_20260505`.
- 2026-05-04 v6: moved delayed non-mainline extension material to final section only; remote4090 S4/S7/S8 parallel preflight completed. S4 lacks an executable step-wise reward pilot runner; S7 lacks a single orchestrator and misses remote artifacts; S8 remains blocked by S3 + S7. A S3 attention-trace tmux attempt failed before experiment start because `logs/modebug_observation_pool/manifest.jsonl` is absent on remote, so no metric result should be recorded from this attempt. Preflight logs are archived under `artifacts/remote4090/modebug_remote4090_preflight_20260503/`.
- 2026-05-03 v5: corrected stress-test scope from current-progress verdict to plan-level reviewer gates; avoid treating unfinished S7/S8/S10/S11 as rejection evidence before execution.
- 2026-05-03 v4: incorporated user review + multi-agent/DeepSeek stress test; non-mainline extension moved behind S8 gate; S3 reframed as baseline attribution trace infrastructure; reward steps marked non-RL; unified temporal evaluator deferred until S7/S8/S10 evidence; ICLR/ICML plan route narrowed to EventProbe-first.
- 2026-05-03 v3: corrected stale S4 gate: pass/fail now only R_pres / `full_text vs drop_text`; replace/shuffle diagnostic-only; S9 now gated by S8 method-direction decision; no-event-mask remains one-seed diagnostic until S11 3-seed ablation.
- 2026-05-03 v2: S2b completed on 4090 with 3 seeds and full eligible split; S4 became ready at the research-plan level with S2b checkpoints; detailed metrics remain authoritative in §5 S2b.
- 2026-05-03 v1: S2a/S2aa quick-fail probe passed; S2b started as R_pres / omission reward full training only; replace/shuffle kept eval-only.
- 2026-05-02 v3: S2 split into S2a quick-fail probe and conditional S2b full training; same-protocol cosine baseline became mandatory.
- 2026-05-02 v2: ChronAccRet HumanML3D-E adapter completed and `train_bert_orig` retrain sanity added; sanity retrain did not use paper event-enhanced / negative-training objective and did not change evaluator role.
- 2026-05-02 v1: EventT2M S0/S5 backbone hygiene closed; pretrained/retrain full-level metrics became sanity assets rather than blockers.
- 2026-05-01 v2: unified narrative changed to diagnosis -> attribution -> targeted method; non-mainline extension retained only as S8-dependent candidate.
- 2026-05-01 v1: old two-paper split changed to parallel ideas with paper form decided at S12.

## 9. 禁写规则

1. 不写"已有完美 event-level evaluator"
2. 不写"AToM 已作为 MoDebug temporal judge"
3. 不写"MotionPatches 是当前 scorer / judge"
4. 不写"duration 已覆盖"
5. 不写 reward-side metric gain 等于 final improvement
6. 不把 held-out 分离写成贡献点
7. 不把 cross-evaluator consistency 写成独立贡献点
8. 不使用裸 metric shorthand（如 `drop = 0.73`）；必须使用 canonical metric name + evaluator + n + role
9. 不把当前 S2/S4/S9 reward-guided experiments 写成 RL，除非新增 policy optimization / rollout objective / generator update 证据
10. 不把 EventT2M-only white-box attribution 外推成跨 baseline 共享机制
11. 不把 unified temporal evaluator 写成已实现；S7/S8/S10 完成前只能写 evaluator stack / calibration plan

## 10. Backlog Link

> [!warning] 非当前主线
> 时间-空间并行控制已从主线执行入口移出，保留为 backlog note：
> [[paperIDEAs/MoDebug/2026-05-01_modebug-spatiotemporal-extension-backlog]]
>
> 只有在 S8 产出与 joint-level attention / omission 相关的稳定机制证据后，它才重新进入 active plan。
