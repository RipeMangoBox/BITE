---
title: "Lance 后先验遗忘审计与 HSI 几何接口"
type: research-memo
date: 2026-06-17
status: draft
tags:
  - motion-generation
  - scene-awareness
  - hsi
  - multimodal-control
  - research-planning
---

# Lance 后先验遗忘审计与 HSI 几何接口

## 核心判断

如果他已经基于 [[analysis/arxiv_2026/Lance_Unified_Multimodal_Modeling_by_Multi-Task_Synergy.md|Lance]] / Lancer 做过若干独立 condition-to-motion 原型，下一步不该继续堆 condition，而是先证明两件事：

1. 多个 condition 合并后，旧能力没有被新能力遗忘或压制。
2. HSI 不是又一个 prefix token，而是会改变 root、接触、碰撞和失败状态的几何约束接口。

本轮只谈 HSI。HHI/HPI/多 NPC 不进入当前设计。

一句话：**先做 ability-interference audit，再做 scene-required HSI smoke test。两者没过之前，memory、CoC、RL、数据扩增都后置。**

## 参考工作定位

主线参考只需要这些：

- [[analysis/arxiv_2026/Lance_Unified_Multimodal_Modeling_by_Multi-Task_Synergy.md|Lance]]：当前 backbone 与多任务训练顺序参照。
- [[analysis/arxiv_2025/OmniMotion_Multimodal_Motion_Generation_with_Continuous_Masked_Autoregression.md|OmniMotion]]、[[analysis/arxiv_2025/OmniMotion-X_Versatile_Multimodal_Whole-Body_Motion_Generation.md|OmniMotion-X]]、[[analysis/arxiv_2026/AnyMo_Scaling_Any-Modality_Conditional_Motion_Generation_with_Masked_Modeling.md|AnyMo]]：多模态 motion generation 的能力边界参照；其中 AnyMo/OmniHuMo 当前公开形态更像数据集与处理工具，不是可直接复用的完整训练/推理代码库。
- [[analysis/AAAI_2025/MotionCraft_Crafting_Whole_Body_Motion_with_Plug_and_Play_Multimodal_Controls.md|MotionCraft]]：冻结主干、zero-init 控制分支、控制能力解耦参照。
- [[analysis/arxiv_2026/Dynamic_Worlds_Dynamic_Humans_Generating_Virtual_Human_Scene_Interaction_Motion_in_Dynamic_Scenes.md|Dyn-HSI]]：HSI 接口参照，重点是 local occupancy、trajectory confidence、condition adapter，而不是替换 motion trunk。
- [[analysis/ICLR_2024/UniHSI_Unified_Human_Scene_Interaction_via_Prompted_Chain_of_Contacts.md|UniHSI]]：CoC 接触链参照，只在 sit / lie / reach / open-door 等接触顺序任务后置使用。
- [[analysis/arxiv_2026/FLAME_Adaptive_Mixture-of-Experts_for_Continual_Multimodal_Multi-Task_Learning.md|FLAME]]、[[analysis/ICLR_2026/Avoid_Catastrophic_Forgetting_with_Rank_1_Fisher_from_Diffusion_Models.md|R1-EWC]]：如果合并后发生遗忘，再作为 router/参数约束参照。

非主线：[[analysis/arxiv_2024/Morph_A_Motion-free_Physics_Optimization_Framework_for_Human_Motion_Generation.md|Morph]] 是物理后验/精炼参照，不能替代 HSI 几何条件建模；[[analysis/arxiv_2026/MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generation.md|MoRL]] 和 [[analysis/arxiv_2026/CLAW_Composable_Language_Annotated_Whole_body_Motion_Generation.md|CLAW]] 属于后训练/数据扩增，不影响当前 adapter 设计。

## 必须实验 1：能力干扰审计

独立 condition 成功不等于统一模型成功。先把现有 Lancer 原型固定成一张回归表，测合并后每条能力的保留率和支配关系。

最小集合：

- 单条件：T2M、S2G、M2D、trajectory/reference。
- 双条件：text+traj、speech+traj、music+traj。
- 三条件：text+audio+traj 或 text+music+traj。至少要有一个三条件 case，否则看不出真实 router/adapter 冲突。
- 空条件或普通语言能力：如果 Lancer 仍保留 LLM 能力，检查 motion tuning 是否损伤原能力。

记录三类数：

- `retention`：合并模型相对独立模型掉多少。
- `dominance`：强条件加入后，弱条件是否被无视。
- `source`：退化来自 tokenizer、shared trunk、adapter、router、采样策略还是数据 replay。

判定：

- 如果旧能力明显退化，先做 replay / zero-init adapter / router isolation / R1-EWC，不要接 HSI。
- 如果某个 condition 永远赢，先解决 dominance，再谈多模态 HSI。
- 如果 retention 和 dominance 都可接受，再进入 HSI smoke test。

## 必须实验 2：HSI 几何 smoke test

HSI 不是“scene caption -> motion”。它首先是可行动作空间约束：哪里能走、哪里不能穿、目标是否可达、何时接触。

最小接口只保留四个量：

- local occupancy around pelvis/root。
- goal / target token。
- contact / affordance hint。
- geometry validator。

先不加 memory，不加复杂 CoC，不加 RL。任务选能暴露几何依赖的 case：

- walk-to-chair。
- sit。
- avoid-obstacle。
- walk-through-narrow-gap。

必做负控：

- `scene-off`：去掉场景输入。
- `scene-shuffle`：换错场景。
- `target-shuffle`：换错目标。
- `obstacle-move`：移动障碍或椅子。

通过标准不要只看观感，至少要有这些信号：

- scene-shuffle 后穿透率、goal error、contact failure 明显上升。
- obstacle-move 后 root trajectory 和身体朝向随场景改变。
- contact hint 改变后，接触关节或接触时刻改变。
- 正常 scene case 的运动质量没有因为几何约束而崩。

如果负控不改变结果，说明模型没用 scene；此时上 [[analysis/ICLR_2024/UniHSI_Unified_Human_Scene_Interaction_via_Prompted_Chain_of_Contacts.md|UniHSI]]、[[analysis/arxiv_2026/MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generation.md|MoRL]] 或 [[analysis/arxiv_2024/Morph_A_Motion-free_Physics_Optimization_Framework_for_Human_Motion_Generation.md|Morph]] 都只是在给错误系统补妆。

## 通过后的下一步

只有前两步都过，再扩展：

- 用 [[analysis/arxiv_2026/Dynamic_Worlds_Dynamic_Humans_Generating_Virtual_Human_Scene_Interaction_Motion_in_Dynamic_Scenes.md|Dyn-HSI]] 的 trajectory confidence 暴露“不可靠规划”，而不是让 decoder 硬编。
- 用 [[analysis/arxiv_2026/Dynamic_Worlds_Dynamic_Humans_Generating_Virtual_Human_Scene_Interaction_Motion_in_Dynamic_Scenes.md|Dyn-HSI]] 的 condition adapter 调节 text / goal / scene / traj 权重。
- 在接触顺序明确的任务上，再接 [[analysis/ICLR_2024/UniHSI_Unified_Human_Scene_Interaction_via_Prompted_Chain_of_Contacts.md|UniHSI]] 的 CoC。
- 用 [[analysis/arxiv_2024/Morph_A_Motion-free_Physics_Optimization_Framework_for_Human_Motion_Generation.md|Morph]] 做物理后验或评估补强，但不要把它当 HSI 建模。
- 后训练和数据扩增再看 [[analysis/arxiv_2026/MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generation.md|MoRL]] / [[analysis/arxiv_2026/CLAW_Composable_Language_Annotated_Whole_body_Motion_Generation.md|CLAW]]。

多模态 + HSI 回测时，关键冲突是 geometry priority：

- speech/music 的节奏不能让人穿墙。
- trajectory/reference 不能压过 obstacle avoidance。
- text 说 sit，但目标椅子不可达时，模型应该暴露失败或改规划，而不是生成表面像坐下的穿模动作。

## 给对方的一针见血版本

当前最有价值的贡献不是“给 Lance 再扩一个 HSI 模态”，而是证明：

1. Lancer 的多 condition motion 能力合并后不遗忘。
2. HSI 在 scene-off / scene-shuffle / target-shuffle / obstacle-move 负控下确实改变轨迹、接触和失败状态。
3. scene-required case 中，geometry priority 高于 audio / trajectory / reference 的局部拟合。

这三条成立，后面再谈 memory、CoC、RL、物理后验和大规模数据扩增才有意义。
