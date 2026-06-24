---
title: "OmniEVA: Embodied Versatile Planner via Task-Adaptive 3D-Grounded and Embodiment-aware Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/OmniEVA_Embodied_Versatile_Planner_via_Task_Adaptive_3D_Grounded_and_Embodiment_aware_Reasoning.pdf
openreview_forum_id: tkEmIJv1tB
aliases:
- OmniEVA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "任务自适应门控路由器（TAGR）根据任务上下文动态融合2D/3D特征，结合任务与具身感知 GRPO（TE-GRPO）将物理约束嵌入规划，从而同时提升几何推理的灵活性和计划的可执行性。"
primary_logic: "通过门控机制选择性注入3D位置编码，避免冗余计算，并在强化学习阶段逐步引入具身奖励课程，使模型自主学习生成符合空间感知和物理约束的序列，实现从基础推理到可靠执行的平滑过渡。"
claims:
- "TAGR 动态融合机制在四个3D基准上平均性能（58.7）超越硬编码融合（57.3）和无3D融合（42.9），验证了任务自适应注入的必要性。"
- "OmniEVA-Base 在7个2D/3D具身推理基准上达到最先进水平，相比先前最佳模型平均提升10.45个百分点。"
- "TE-GRPO 使 OmniEVA-ER 在 Where2Approach 和 Where2Fit 上将准确率分别提升28.95%和34.28%，并在真实机器人任务中成功率从5-6/10提升至8-9/10。"
- "OmniEVA-ER 对未见机械臂长度（72-105cm）的平均执行成功率达80.5%，远超基线42.3%，显示强具身泛化能力。"
---

# OmniEVA: Embodied Versatile Planner via Task-Adaptive 3D-Grounded and Embodiment-aware Reasoning

> [!tip] 核心洞察
> 通过门控机制选择性注入3D位置编码，避免冗余计算，并在强化学习阶段逐步引入具身奖励课程，使模型自主学习生成符合空间感知和物理约束的序列，实现从基础推理到可靠执行的平滑过渡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | OmniEVA：任务自适应3D锚定与具身感知的通用规划器 |
| 英文题名 | OmniEVA: Embodied Versatile Planner via Task-Adaptive 3D-Grounded and Embodiment-aware Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=tkEmIJv1tB); [Project](https://omnieva.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | OmniEVA |
| Dataset | Where2Place, VSI-bench, PACO-LVIS, RoboRefit |

> [!tip] 效果简介
> - Where2Place 上，Accuracy 为 74.95，对比 73.59 (RoboBrain2.0-32B)，变化 +1.36。
> - VSI-bench 上，Accuracy 为 57.17，对比 42.69 (RoboBrain2.0-32B)，变化 +14.48。
> - PACO-LVIS 上，Accuracy 为 21.01，对比 16.23 (RoboBrain2.0-32B)，变化 +4.78。

## 概述

**核心问题**：具身多模态大模型在从感知到规划的跨越中面临两个关键瓶颈。其一为**几何适应性差距**，现有方法或仅依赖2D输入导致空间感知不足，或采用硬编码方式静态注入3D信息，造成冗余计算与任务无关的干扰。其二为**具身约束差距**，规划过程通常忽略机器人自身的物理限制（如机械臂可达范围），导致生成的计划在语义上合理却无法实际执行。

**核心方法**：OmniEVA 提出两条互补的技术路径来解决上述瓶颈。在感知层面，**任务自适应门控路由器**（Task-Adaptive Gated Router, TAGR）根据任务指令和场景上下文，通过 Gumbel-Softmax 硬门控动态决定是否注入3D位置编码，仅在几何推理必要时激活空间特征，实现灵活性与效率的平衡。在规划层面，**任务与具身感知 GRPO**（Task- and Embodiment-aware GRPO, TE-GRPO）将物理可行性验证嵌入强化学习奖励函数，并通过渐进式课程调度逐步强调具身约束，使模型在保留任务语义的同时学会遵守物理限制。

**方法定位**：OmniEVA 属于具身视觉语言模型（Embodied VLM）范畴，采用“基础推理预训练 + 具身感知强化微调”的两阶段范式。其3D融合策略区别于 **Video-3D-LLM**（Zheng et al., 2025）的硬编码注入和 **3DRS**（Huang et al., 2025）的静态融合，转而采用任务自适应的动态门控；其具身约束融入机制则填补了 **RoboBrain2.0-32B**（Team et al., 2025a）等基线忽略物理可行性的空白。

**主要结果**：
- OmniEVA-Base 在7个2D/3D具身推理基准上达到最先进水平，相比先前最佳模型平均提升10.45个百分点（Figure 1, Table 2）。
- TAGR 动态硬门控融合在四个3D基准上平均得分58.7，显著优于无3D融合（42.9）和硬编码融合（57.3），验证了任务自适应注入的有效性（Table 1）。
- TE-GRPO 使 OmniEVA-ER 在 Where2Approach 和 Where2Fit 上准确率分别提升28.95%和34.28%（Figure 5），在真实机器人杂乱场景放置任务中成功率从5-6/10提升至9/10（Table 6）。
- 对未见机械臂长度（72–105cm），OmniEVA-ER 平均执行成功率达80.5%，远超基线的42.3%，展现出强具身泛化能力（Table 5）。

## 背景与动机

### 具身多模态大模型的现实需求

让机器人在开放世界中理解自然语言指令并自主执行复杂任务，是具身智能的核心目标。近年来，多模态大模型（MLLM）在视觉-语言推理上取得了显著进展，为机器人规划提供了新的范式。然而，将通用MLLM直接应用于具身场景时，面临两个根本性瓶颈。

### 瓶颈一：几何适应性差距

现有方法在处理3D空间信息时存在两难困境。纯2D输入方案（如**RoboBrain2.0-32B**，Team et al., 2025a）完全忽略深度几何结构，导致空间感知不足；而硬编码的静态3D注入方案（如**3DRS**，Huang et al., 2025；**Video-3D-LLM**，Zheng et al., 2025）则对所有任务无差别地融合3D特征，引入了大量冗余计算。实验表明，硬编码融合在四个3D基准上的平均性能仅为57.3，而无3D融合更是低至42.9（Table 1）。问题的本质在于：并非所有具身推理任务都需要精细的3D几何信息——例如，颜色识别和物体计数仅依赖2D视觉即可完成，而形状判断和空间关系推理则必须借助3D结构。

### 瓶颈二：具身约束差距

更关键的是，现有规划器在生成行动计划时，普遍忽略机器人自身的物理约束。一个语义上正确的计划——例如“将杯子放在桌面上”——可能在理论上完全合理，却因目标位置超出机械臂工作范围而无法执行。这种“理论可行、物理不可达”的鸿沟，使得规划结果在真实部署中频繁失败。在Where2Approach和Where2Fit等移动操作任务上，缺乏具身感知的模型准确率严重受限，而引入具身约束后准确率可分别提升28.95%和34.28%（Figure 5）。

### 本文动机

针对上述两大瓶颈，OmniEVA提出两条核心改进路径：

1. **任务自适应3D锚定**：设计门控路由器，根据任务上下文动态决定是否注入3D位置编码，在几何推理的灵活性与计算效率之间取得平衡。
2. **具身感知推理**：在强化学习微调阶段引入物理约束奖励，并通过课程调度逐步强调执行可行性，使模型从“会规划”平滑过渡到“能执行”。

这一设计使得OmniEVA在7个2D/3D具身推理基准上达到最先进水平，相比先前最佳模型平均提升10.45个百分点（Figure 1），并在真实机器人任务中将成功率从5-6/10提升至8-9/10（Table 6）。

## 核心创新

OmniEVA 针对具身多模态大模型的两大瓶颈——几何适应性差距与具身约束差距——提出了两个相互协同的关键创新。

### 创新一：任务自适应门控路由器（TAGR）

传统方法对 3D 信息的处理存在两极化问题：纯 2D 输入导致空间感知不足，而硬编码的静态 3D 注入则对所有任务无差别地引入冗余计算。TAGR 的核心突破在于将 3D 特征融合从“静态注入”转变为“任务驱动的动态决策”。

具体而言，TAGR 通过一个轻量级门控网络，根据任务指令的语义特征和场景的全局视觉描述，动态生成二值门控信号。该门控网络将指令编码 $V^{T}$ 与场景池化特征 $V_{\mathrm{avg}}^{I}$ 拼接后，经 MLP 生成门控 logits $V^{g} \in \mathbb{R}^{2}$，再通过 Gumbel-Softmax 实现硬门控，输出离散的 0/1 决策。当门控激活（$g=1$）时，从深度图导出的 patch 级 3D 位置编码被注入视觉令牌：$V_{\mathrm{hybrid}}^{I} = V^{I} + g \cdot V^{\mathrm{p}}$；否则模型仅使用 2D 特征，避免不必要的计算开销。

这一设计的因果效应在消融实验中得到了充分验证（Table 1）：硬门控动态集成在四个 3D 基准上平均得分 58.7，显著优于硬编码融合（57.3）和无 3D 融合（42.9），同时远超软门控（51.0）和交叉注意力融合（32.6）。软门控性能下降的原因在于，连续的权重系数破坏了位置编码的数值稳定性；而交叉注意力融合则在大幅增加计算量的同时导致 Scan2Cap 得分骤降约 50 点。这些对比表明，TAGR 的硬门控机制在保持几何推理能力的同时，有效避免了冗余 3D 信息对非空间任务的干扰。

进一步的分析（Figure 4）揭示了门控决策的语义一致性：形状相关提示（如“桌子是什么形状”）的 3D 激活概率高达 76.9%，而纯语义提示则保持较低的激活率，证明 TAGR 确实学会了根据任务的空间需求自主调节 3D 信息的利用程度。

### 创新二：任务与具身感知的强化微调（TE-GRPO）

传统规划器仅关注语义正确性，忽视机器人的物理约束，导致生成的计划“理论可行却无法执行”。TE-GRPO 将具身可行性直接嵌入强化学习的奖励函数中，使模型在优化过程中自主学习生成物理上可执行的计划。

TE-GRPO 引入了双奖励机制：任务奖励 $r_{i}^{\mathrm{task}}$ 衡量输出与任务目标的语义匹配度，具身奖励 $r_{i}^{\mathrm{embod}}$ 验证计划在给定机器人参数下的物理可行性。两者通过渐进式课程调度 $\lambda_t$ 融合为复合准确率奖励：

$$r_{i,t}^{\mathrm{acc}} = r_{i}^{\mathrm{task}} \cdot (\lambda_t \cdot r_{i}^{\mathrm{embod}} + (1 - \lambda_t))$$

其中 $\lambda_t$ 从 0 逐步增长至 1，使模型先在任务语义空间收敛，再逐步强调物理约束，实现从“理解任务”到“可执行规划”的平滑过渡。

这一创新的效果在移动操作任务上表现突出（Figure 5）：TE-GRPO 使 Where2Approach 和 Where2Fit 的准确率分别提升 28.95% 和 34.28%。移除具身奖励（w/o $r^{\mathrm{embod}}$）后成功率显著下降，证明具身约束的嵌入是不可或缺的。更关键的是，OmniEVA-ER 在未见机械臂长度（72–105cm）上的平均执行成功率达 80.5%，远超 OmniEVA-Base 的 42.3%（Table 5），显示出强大的具身泛化能力。在真实机器人杂乱场景放置任务中，OmniEVA-ER 的成功率从基线的 5–6/10 提升至 9/10（Table 6），验证了该方法在物理世界中的有效性。

### 创新间的协同关系

TAGR 与 TE-GRPO 并非孤立设计，而是形成互补闭环：TAGR 在感知层面提供任务自适应的空间理解，为规划提供精准的几何信息；TE-GRPO 在决策层面将物理约束注入规划过程，确保生成的动作序列在给定具身条件下可执行。两者共同实现了从“感知什么”到“如何执行”的端到端优化，使 OmniEVA 在 2D/3D 具身推理基准上平均超越先前最佳模型 10.45 个百分点（Figure 1, Table 2），并在目标导航任务中以 42.5 SPL（HM3D）刷新记录（Table 4）。

## 整体框架

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_tkEmIJv1tB/figures/003_Figure_2.jpg]]
*Figure 2: Model Architecture of OmniEVA. Left: The overall architecture of OmniEVA, featuring a novel task-adaptive gated router that dynamically incorporates 3D positional embeddings. Middle: Detailed implementation of the gated router module. Right: Illustrative examples of the gated router’s activation state across different tasks*

OmniEVA 的整体架构围绕一个核心设计展开：将任务自适应的 3D 空间锚定与具身感知的推理能力统一于单一规划器中。系统接收多模态输入——自然语言指令 $T$、RGB 图像序列（或视频帧）$\{I_1, I_2, ..., I_N\}$，以及可选的多视图深度图 $\{D_1, D_2, ..., D_N\}$，配合相机内参 $K$ 和外参 $M_i$ 以支持跨视图空间理解。输出为自回归生成的规划响应，直接用于下游机器人执行。

### 模块串联与数据流

整个 pipeline 由五个核心模块串联构成：

1.  **ViT Encoder**：将每帧 RGB 图像编码为视觉令牌 $V^I \in \mathbb{R}^{N \times H_p \times W_p \times d_v}$，其中 $d_v$ 为嵌入维度，$N$ 为帧数，$H_p \times W_p$ 为 patch 网格尺寸。

2.  **3D Positional Encoder**：从深度图生成 patch 级 3D 位置编码 $V^p$，为每个视觉令牌注入空间坐标信息。

3.  **Task-Adaptive Gated Router (TAGR)**：这是架构的关键创新。TAGR 接收指令 $T$（经 SentenceTransformer 编码为 $V^T$）和全局场景描述 $V_{\text{avg}}^I$（对 $V^I$ 做平均池化），通过 MLP 生成门控 logits $V^g \in \mathbb{R}^2$，再经 Gumbel-Softmax 输出硬门控信号 $g \in \{0, 1\}$。最终混合视觉令牌为：
    $$V_{\text{hybrid}}^I = V^I + g \cdot V^p$$
    当 $g=1$ 时注入 3D 位置编码，$g=0$ 时仅保留 2D 令牌。这种硬门控设计避免了软加权导致的数值不稳定问题（Table 1 显示硬门控平均得分 58.7，显著优于软门控的 51.0 和交叉注意力融合的 32.6）。

4.  **LLM Backbone**：接收混合视觉令牌和文本令牌，自回归生成响应。视觉令牌在馈入 LLM 前通过投影层对齐到文本嵌入空间。

5.  **TE-GRPO Reward Module**（仅在第三阶段强化微调时激活）：评估模型输出的任务完成度 $r^{\text{task}}$ 和具身可行性 $r^{\text{embod}}$，通过渐进课程调度系数 $\lambda_t$ 将二者融合为复合奖励：
    $$r_{i,t}^{\text{acc}} = r_i^{\text{task}} \cdot (\lambda_t \cdot r_i^{\text{embod}} + (1 - \lambda_t))$$
    最终奖励为格式奖励与准确率奖励之和：$r_{i,t} = r^{\text{format}} + r_{i,t}^{\text{acc}}$。

### 三阶段训练范式

OmniEVA 采用递进式三阶段训练策略（Figure 3）：

-   **阶段一：TAGR 预训练**。在 3D 推理数据上训练门控路由器，损失函数为交叉熵与 KL 散度正则项的组合：$\mathcal{L}_{\psi, \theta}^{\text{total}} = \mathcal{L}_{\psi, \theta}^{\text{CE}} + \alpha \cdot \mathcal{L}_{\psi}^{\text{KL}}$，使门控行为稳定收敛。

-   **阶段二：监督微调（SFT）**。混合通用具身推理数据与定制具身任务数据，构建广泛的推理基础。

-   **阶段三：任务与具身感知强化微调（TE-GRPO）**。引入任务奖励和具身执行奖励，通过 $\lambda_t$ 从 0 到 1 的渐进课程调度，使模型从语义正确逐步过渡到物理可行，实现从基础推理到可靠执行的平滑过渡。

### 设计逻辑

TAGR 的全局门控决策基于一个关键洞察：并非所有任务都需要 3D 空间信息。Figure 4 的分析证实，形状相关提示触发 3D 激活的概率高达 76.9%，而纯语义任务则很少激活。这种按需注入的策略在保证几何推理精度的同时，避免了冗余计算。TE-GRPO 则通过将物理约束（当前主要考虑机械臂长度）嵌入奖励函数，解决了规划理论可行却无法执行的核心瓶颈——Table 5 显示 OmniEVA-ER 对未见臂长（72–105cm）的平均执行成功率达 80.5%，远超基线的 42.3%。

## 核心模块与公式推导

OmniEVA 的架构围绕两个核心创新模块展开：**任务自适应门控路由器（TAGR）** 解决几何适应性差距，**任务与具身感知 GRPO（TE-GRPO）** 弥合具身约束差距。以下详述其关键设计与公式。

### 任务自适应门控路由器（TAGR）

TAGR 的核心思想是：并非所有任务都需要 3D 空间信息。对于纯语义问答，注入 3D 位置编码反而引入冗余噪声。TAGR 通过一个可学习的门控机制，根据任务指令和场景上下文动态决定是否激活 3D 特征注入。

**门控决策流程**：首先将自然语言指令 $T$ 编码为潜向量：

$$V^{T} = \mathrm{SentenceTransformer}(T)$$

同时对视觉编码器输出的多帧视觉令牌 $V^{I} \in \mathbb{R}^{N \times H_{\mathrm{p}} \times W_{\mathrm{p}} \times d_{v}}$ 进行全局平均池化，得到场景描述符：

$$V_{\mathrm{avg}}^{I} = \mathrm{AvgPooling}(V^{I}, \mathrm{dim}=0,1,2)$$

将任务编码与场景描述符拼接后，送入一个小型 MLP 生成门控 logits：

$$V^{g} = \mathbf{MLP}_{\psi}(\mathbf{Concatenate}([V^{T}, V_{\mathrm{avg}}^{I}])) \in \mathbb{R}^{2}$$

**硬门控机制**：为避免软加权导致的位置编码数值不稳定，TAGR 采用 Gumbel-Softmax 实现硬门控，输出离散的 0 或 1：

$$g = \mathrm{GumbelSoftmax}(V^{g}, \tau) \in \{0, 1\}$$

最终混合视觉令牌为：

$$V_{\mathrm{hybrid}}^{I} = V^{I} + g \cdot V^{\mathrm{p}}$$

其中 $V^{\mathrm{p}}$ 为从深度图生成的 patch 级 3D 位置编码。当 $g=1$ 时注入 3D 信息，$g=0$ 时仅保留 2D 令牌。消融实验（Table 1）证实，硬门控动态集成在四个 3D 基准上平均得分 58.7，显著优于软门控（51.0）和交叉注意力融合（32.6）。

**门控训练正则**：为防止门控退化（始终激活或始终关闭），训练损失中加入 KL 散度正则项：

$$\mathcal{L}_{\psi, \theta}^{\mathrm{total}} = \mathcal{L}_{\psi, \theta}^{\mathrm{CE}} + \alpha \cdot \mathcal{L}_{\psi}^{\mathrm{KL}}$$

其中 $\psi$ 为门控 MLP 参数，$\theta$ 为其余模型参数。该正则项约束门控激活概率接近先验分布，保持决策多样性。

### 任务与具身感知 GRPO（TE-GRPO）

TE-GRPO 在强化学习微调阶段引入双重奖励信号，将物理约束嵌入规划过程。

**奖励分解**：对每个输出 $o_i$，定义两类奖励：

$$r_{i}^{\mathrm{task}} = \mathrm{EvalTask}(q, o_i), \quad r_{i}^{\mathrm{embod}} = \mathrm{EvalExec}(q, o_i)$$

- $r_{i}^{\mathrm{task}} \in [0,1]$：衡量输出语义是否满足任务目标（如目标位置是否正确）。
- $r_{i}^{\mathrm{embod}} \in \{0,1\}$：验证规划动作在给定具身约束下是否可执行（如目标点是否在机械臂可达范围内）。

**渐进式具身课程**：直接联合优化两项奖励可能导致训练不稳定。TE-GRPO 引入课程调度系数 $\lambda_t$，从 0 逐步增长至 1，使模型先学会完成语义任务，再逐步强调物理可行性：

$$r_{i,t}^{\mathrm{acc}} = r_{i}^{\mathrm{task}} \cdot (\lambda_t \cdot r_{i}^{\mathrm{embod}} + (1-\lambda_t))$$

当 $\lambda_t = 0$ 时，仅优化任务奖励；当 $\lambda_t = 1$ 时，具身奖励完全生效——只有同时满足语义正确性和物理可行性的输出才能获得完整奖励。

**最终奖励**：结合格式奖励与准确率奖励：

$$r_{i,t} = r_{i}^{\mathrm{format}} + r_{i,t}^{\mathrm{acc}}$$

该设计使模型在保留任务语义理解能力的同时，自主学习遵守物理约束。Figure 5 的消融实验表明，加入具身奖励后 Where2Approach 和 Where2Fit 准确率分别提升 28.95% 和 34.28%；移除 $r^{\mathrm{embod}}$ 后成功率显著下降，验证了具身约束嵌入的必要性。

### 训练流水线

上述模块嵌入三阶段训练范式（Figure 3）：
1. **TAGR 预训练**：在 3D 推理数据上训练门控路由器，学习何时激活 3D 注入。
2. **监督微调（SFT）**：在混合具身推理数据集上微调全模型，建立广泛推理基础。
3. **强化微调（RFT）**：使用 TE-GRPO 进行策略优化，通过渐进课程将物理约束内化至规划行为。

## 实验与分析

### 核心瓶颈验证：TAGR动态融合的必要性

OmniEVA的核心创新之一是通过任务自适应门控路由器（TAGR）解决几何适应性差距。Table 1的消融实验直接验证了这一设计的必要性：在SQA3D、ScanQA、Scan2Cap、ScanRefer四个3D基准上，TAGR采用的**硬门控动态3D集成**取得了平均58.7的最高分，显著优于硬编码融合（57.3）和无3D融合（42.9）。对比之下，软门控替代方案（51.0）由于位置编码的数值稳定性问题，在所有基准上均表现下降；交叉注意力融合方法（32.6）则导致性能大幅退化——在SQA3D上下降约6个点，在Scan2Cap上更是骤降约50个点。这组对比揭示了关键因果机制：3D信息并非越多越好，**任务自适应的选择性注入**才是平衡空间感知精度与计算效率的核心杠杆。


![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_tkEmIJv1tB/figures/005_Table_1.jpg]]
*Table 1: Results of Different 3D-Integration Methods. To ensure a fair comparison and isolate the impact of 3D integration, models were trained exclusively on the training splits of the SQA3D, ScanQA, Scan2Cap, and ScanRefer datasets. This experimental setup is consistent with prior work like Video-3D-LLM and 3DRS*

Figure 4进一步从语义层面揭示了门控机制的学习行为。通过将提示嵌入聚类为语义类别，分析显示**形状相关提示**触发了最高的3D激活概率（76.9%），而纯语义或关系推理类提示的激活率显著降低。这表明TAGR学会了根据任务的空间需求自主决定是否调用3D几何信息，而非机械地全盘接受或拒绝。

### 2D/3D具身推理全面领先

OmniEVA-Base在7个2D/3D具身推理基准上达到最先进水平，相比先前最佳模型RoboBrain2.0-32B平均提升**10.45个百分点**（Table 2, Figure 1）。具体而言：


![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_tkEmIJv1tB/figures/002_Figure_1.jpg]]
*Figure 1: Performance Comparison across 2D and 3D Embodied Reasoning Benchmarks*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_tkEmIJv1tB/figures/007_Table_2.jpg]]
*Table 2: 2D General Reasoning Benchmarks and In-house Benchmarks. Hurst et al. (2024), Team et al. (2025b), Zhang et al. (2024b), Li et al. (2024), Zhu et al. (2025), Bai et al. (2025), Yuan et al. (2024a), Azzolini et al. (2025), Luo et al. (2025), Yang et al. (2025a), Team et al. (2025a)*

**2D具身推理**（Table 2）：在VSI-bench上取得最大增幅（+14.48），RoboRefit上提升+21.21，验证了模型在复杂空间推理和物体重定位任务上的优势。在PACO-LVIS（+4.78）和Where2Place（+1.36）上也保持领先，但Where2Place的增益相对较小，可能因为该任务对3D几何的依赖度较低，TAGR的门控优势未能充分发挥。

**3D场景理解**（Table 3）：OmniEVA-Base在SQA3D（62.9 EM）、ScanQA（30.6 EM）、Scan2Cap（94.6 CIDEr）上均超越专用3D LLM，包括Video-3D-LLM和3DRS。特别值得注意的是ScanRefer视觉锚定任务：OmniEVA-Base仅使用文本输入输出、无需外部检测器或任务专用头，即达到**55.8**（IoU@0.25），远超此前最佳结果44.4。这证明TAGR注入的3D位置编码足以支撑精确的空间指代理解。

**目标导航**（Table 4）：在HM3D ObjectNav上，OmniEVA-Base取得74.2 SR和42.5 SPL，超越UniNavid（37.1 SPL）等专用导航方法。SPL（Success weighted by Path Length）的提升尤其关键，表明模型不仅能够到达目标，还能规划更高效的路径。

### 具身感知训练的因果效应

TE-GRPO的消融实验（Figure 5）揭示了具身约束融入的因果作用。在Where2Approach和Where2Fit两个移动操作任务上，加入具身奖励（$r^{\text{embod}}$）使准确率分别飙升**28.95%**和**34.28%**。移除具身奖励后，模型虽然保持了任务语义的正确性，但在物理可行性上显著退化。渐进式课程调度$\lambda_t$从0到1的平滑过渡，使模型在保留语义理解的同时逐步学会遵守物理约束——这一机制在Section 3.3.3中有详细描述，但Figure 5的结果是其有效性的直接证据。


![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_tkEmIJv1tB/figures/010_Figure_5.jpg]]
*Figure 5: Ablation Results of the proposed TE-GRPO Method on Local Mobile-Manipulation Tasks*

### 具身泛化：从仿真到真实世界

Table 5展示了OmniEVA-ER对未见机械臂长度的强泛化能力。在72-105cm的臂长范围内，OmniEVA-ER的平均执行成功率达到**80.52%**，远超OmniEVA-Base的42.32%和RoboBrain2.0-7B的18.37%。值得注意的是，即使在训练中未见过的105cm臂长上，OmniEVA-ER仍保持75.7%的成功率，而基线模型降至29.3%。这验证了TE-GRPO并非简单记忆特定实施例，而是学习了**可迁移的物理约束推理能力**。


![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_tkEmIJv1tB/figures/011_Table_5.jpg]]
*Table 5: Results of Different Embodiment Execution Success Rate*

真实世界实验（Table 6）进一步验证了这一结论。在杂乱环境抓取（Cluttered Pick）和放置（Cluttered Place）任务上，OmniEVA-ER的成功率从基线的5-6/10提升至**8-9/10**。但在约束导航（Constrained Navigation）任务上，两个版本表现接近（8-9/10），这是因为导航任务对机械臂物理约束的依赖度较低，TE-GRPO的具身奖励优势无法充分体现——这反而从反面印证了具身感知训练的针对性。

### 失败模式与局限性

尽管整体表现优异，分析揭示了几个值得关注的边界：

1. **全局门控的粒度限制**：当前TAGR采用全局门控决策，对于包含多重空间需求的复杂场景（如同时需要理解物体形状和空间关系的指令），可能无法细粒度地处理异质区域。Table 1中ScanRefer上硬门控与硬编码融合的差距（55.8 vs 54.4）相对较小，暗示在需要精细空间指代的任务中，全局门控的信息瓶颈开始显现。

2. **具身约束的覆盖范围**：Table 5和Table 6仅考虑了机械臂长度这一维度。当面对自由度、安装高度、传感器视野等更广泛的物理参数变化时，模型的泛化性有待扩展。Table 5中105cm臂长上OmniEVA-ER的成功率（75.7%）已出现下降趋势，提示极端实施例可能触及当前表征的边界。

3. **动态环境与长时域规划的未验证风险**：所有实验均在静态或准静态场景下进行。在动态环境和长时域任务中，模型的规划一致性与安全性尚未得到充分验证，这构成了从实验室到真实部署的关键缺口。
## 方法谱系与知识库定位

### 核心瓶颈与设计动机

OmniEVA 的提出源于具身多模态大模型面临的两大结构性瓶颈：

1. **几何适应性差距**：现有方法或仅依赖 2D 输入导致空间感知不足，或采用硬编码方式静态注入 3D 信息，在不需要几何推理的任务中引入冗余计算和噪声。消融实验（Table 1）表明，硬编码 3D 融合（平均 57.3）虽优于无 3D 融合（42.9），但仍低于任务自适应方案（58.7），验证了静态注入的局限性。

2. **具身约束差距**：规划过程忽略机器人物理约束（如机械臂长度），导致生成的计划在语义上正确但物理上无法执行。OmniEVA-Base 在未见机械臂长度上的平均执行成功率仅 42.3%，而引入具身感知训练后提升至 80.5%（Table 5），直接量化了这一差距。

### 方法谱系定位

OmniEVA 处于**2D 具身推理大模型**与**3D 视觉-语言模型**的交汇处，其设计同时回应了两类基线方法的不足：

**2D 具身推理基线**：以 **RoboBrain2.0-32B**（Team et al., 2025）为代表的大规模具身模型在多个 2D 基准上取得了先前最优性能，但缺乏 3D 空间感知能力。OmniEVA-Base 在 7 个 2D/3D 具身推理基准上平均超越 RoboBrain2.0-32B 达 10.45 个百分点（Figure 1, Table 2），其中在 VSI-bench 上提升最为显著（+14.48），在 RoboRefit 上提升 +21.21，表明 3D 注入对空间推理任务具有关键增益。

**3D 融合基线**：**Video-3D-LLM**（Zheng et al., 2025）和 **3DRS**（Huang et al., 2025）代表了静态 3D 注入范式，在 SQA3D 和 Scan2Cap 上分别达到 58.6 和 86.1。OmniEVA-Base 在相同基准上取得 62.9（+2.3）和 94.6（+8.5），且无需外部检测器或任务专用头即可在 ScanRefer（w/o annotation）上达到 55.8（IoU@0.25），显著超过此前最优的 44.3（Table 3）。这表明任务自适应门控不仅提升了性能，还降低了系统复杂度。

**目标导航基线**：**UniNavid**（Zhang et al., 2024）在 HM3D ObjectNav 上达到 37.1 SPL。OmniEVA-Base 以 42.5 SPL 超越该基线（Table 4），并在 MP3D 上也取得最优，证明动态 3D 注入对导航任务的空间推理同样有效。

**空间推理基线**：**RoboPoint**（Yuan et al., 2024）作为专门的空间推理方法，在具身场景中提供了参照。OmniEVA 通过统一的动态融合框架在多个空间推理任务上实现了更优或可比性能。

### 关键设计决策与消融证据

**硬门控 vs. 软门控与交叉注意力**：TAGR 采用 Gumbel-Softmax 硬门控（输出 0 或 1），而非软加权或交叉注意力融合。Table 1 的消融显示，硬门控（平均 58.7）显著优于软门控（51.0）和交叉注意力（32.6）。交叉注意力在 Scan2Cap 上性能骤降约 50 点，论文归因于位置编码的数值稳定性问题——连续加权破坏了 3D 位置编码的几何结构。

**门控决策的可解释性**：Figure 4 的语义聚类分析显示，形状相关提示词触发的 3D 激活概率最高（76.9%），而纯语义或颜色类提示词激活率较低，验证了 TAGR 确实学到了任务相关的选择性注入策略，而非随机行为。

**具身奖励的必要性**：TE-GRPO 消融（Figure 5）表明，加入具身奖励 $r^{\mathrm{embod}}$ 后，Where2Approach 和 Where2Fit 准确率分别提升 28.95% 和 34.28%；移除具身奖励后成功率显著下降。渐进式课程调度 $\lambda_t$ 从 0 到 1 逐步强调物理可行性，使模型在保留任务语义的同时学会遵守物理约束。

### 适用边界与局限

1. **全局门控的粒度限制**：当前 TAGR 对整条指令做出全局 0/1 决策，无法处理包含多重空间需求的复杂场景。例如，“找出红色杯子并放到桌子左边”中，颜色识别不需要 3D，而空间关系推理需要。patch 级门控策略是未来方向。

2. **具身参数的覆盖范围**：TE-GRPO 目前仅将机械臂长度纳入具身约束，未考虑自由度、安装高度、传感器视野等更广泛的物理参数。在更复杂的机器人形态上的泛化性有待验证。

3. **动态环境与长期规划**：模型在静态或准静态场景中表现优异，但在高不确定性和长时域任务中的规划一致性与安全性尚未充分验证，可能面临累积误差和计划退化问题。

### 开放问题

- 如何设计 patch 级门控策略，使模型能对场景中不同区域施加差异化的 3D 注入强度？
- 在具身感知训练中纳入更多物理参数（如关节限位、基座高度、末端执行器类型）能否进一步增强跨实施例的鲁棒性？
- 模型在复杂动态环境和长时域任务中的规划一致性如何保证？是否需要引入显式的世界模型或不确定性量化机制？

## 原文 PDF

![[paperPDFs/ICLR_2026/OmniEVA_Embodied_Versatile_Planner_via_Task_Adaptive_3D_Grounded_and_Embodiment_aware_Reasoning.pdf]]
