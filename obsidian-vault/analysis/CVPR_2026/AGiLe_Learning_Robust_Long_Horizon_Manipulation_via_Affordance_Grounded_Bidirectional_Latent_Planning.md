---
title: "AGiLe: Learning Robust Long-Horizon Manipulation via Affordance-Grounded Bidirectional Latent Planning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AGiLe_Learning_Robust_Long_Horizon_Manipulation_via_Affordance_Grounded_Bidirectional_Latent_Planning.pdf
project_link: "https://agile-long.github.io"
code_link: null
aliases:
- AGiLe
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: AGiLe通过双向潜在规划（后向规划器生成目标导向的子目标，前向评论家评估可达性）实现时间连贯性，并通过可供性锚定模块（以任务查询交叉注意力地过滤视觉特征）实现空间接地，两个旋钮联合解决了长程操作中的鲁棒性问题。
primary_logic: 将复杂的长程操作解耦为“做什么”（高层双向规划）和“怎么做”（可供性锚定执行）两个子问题。训练时通过前向评论家对后向规划器的知识蒸馏，将计划的一致性与可达性约束内化到规划器参数中，从而在推理时可丢弃评论家，在不增加计算开销的前提下获得时间鲁棒性。
claims:
- AGiLe在LIBERO-LONG基准上的平均成功率达到97.1%，相比前最好的方法LBP（88.6%）提升8.5%，并在10个任务中的7个上达到100%成功率。
- 消融实验表明，移除前向评论家使成功率从97.1%骤降至89.0%，移除可供性锚定模块则降至90.5%，验证了两个组件的关键性。
- 在真实世界6阶段长程任务中，基线LBP的性能随阶段增加急剧崩溃（任务3为5%，任务4为2%），而AGiLe保持显著更高的鲁棒性。
- LIBERO-LONG 上 Avg. Success (%) = 97.1
---

# AGiLe: Learning Robust Long-Horizon Manipulation via Affordance-Grounded Bidirectional Latent Planning

> [!tip] 核心洞察
> 将复杂的长程操作解耦为“做什么”（高层双向规划）和“怎么做”（可供性锚定执行）两个子问题。训练时通过前向评论家对后向规划器的知识蒸馏，将计划的一致性与可达性约束内化到规划器参数中，从而在推理时可丢弃评论家，在不增加计算开销的前提下获得时间鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | AGiLe：通过可供性锚定的双向潜在规划实现鲁棒长程操作 |
| 英文题名 | AGiLe: Learning Robust Long-Horizon Manipulation via Affordance-Grounded Bidirectional Latent Planning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_AGiLe_Learning_Robust_Long-Horizon_Manipulation_via_Affordance-Grounded_Bidirectional_Latent_Planning_CVPR_2026_paper.html) · [Project](https://agile-long.github.io) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | AGiLe |
| Dataset | LIBERO-LONG |

> [!tip] 效果简介
> - LIBERO-LONG 上，Avg. Success (%) 97.1 vs 88.6 (LBP) (+8.5%)；#Perfect Tasks (100% success) 7/10 vs 未报告（LBP最高可能为部分任务，但无数据） (明显领先)。

## 概述

长程操作任务要求机器人在长时间跨度内顺序执行多个子任务，其核心瓶颈在于**时间鲁棒性**与**空间鲁棒性**的双重缺失。时间维度上，预测误差随规划步数累积，导致计划在时序延伸中崩溃；空间维度上，高层抽象计划难以可靠地接地到连续感知-动作空间，形成规划与执行之间的鸿沟。

针对上述瓶颈，本文提出 **AGiLe**——一个通过**可供性锚定的双向潜在规划**实现鲁棒长程操作的新框架。AGiLe 的核心思路是将复杂的长程操作解耦为“做什么”与“怎么做”两个子问题：**双向潜在规划器**（后向规划器生成目标导向的子目标序列，前向评论家评估其可达性）负责维持时序连贯的计划生成；**可供性锚定模块**（以任务查询通过交叉注意力过滤视觉特征）负责将抽象子目标接地到像素级视觉可供性，从而驱动精确的低层动作执行。训练时，前向评论家的可达性知识通过联合优化被蒸馏到规划器参数中，使得推理阶段可以丢弃评论家，在不增加计算开销的前提下获得时间鲁棒性。

在 **LIBERO-LONG** 长程操作基准上，AGiLe 取得 **97.1%** 的平均成功率，相较此前最好的方法 **LBP**（Liu et al., ICML 2025）的 88.6% 提升 **8.5 个百分点**，并在 10 个任务中的 7 个上达到 100% 成功率。消融实验进一步验证：移除前向评论家使成功率骤降至 89.0%，移除可供性锚定模块则降至 90.5%，确认了两个组件的关键性。在真实世界 6 阶段长程任务中，基线 LBP 的性能随阶段增加急剧崩溃，而 AGiLe 保持了显著更高的鲁棒性，验证了方法从仿真到现实的迁移能力。

## 背景与动机

长程操作（long-horizon manipulation）是机器人学习中最具挑战性的问题之一。与短程技能不同，长程任务要求智能体在数百个时间步内顺序完成多个子任务，例如“打开抽屉→取出物品→放置到指定位置”。这种多阶段特性引入了两个相互交织的核心瓶颈：

**时间鲁棒性缺失**：现有方法通常采用自回归规划，即从当前状态逐步预测未来子目标序列。然而，预测误差会随规划步数累积，导致计划在长程推进中逐渐偏离目标——这一现象被称为“计划崩溃”（plan collapse）。即使单个子目标的预测误差很小，在数十步的链式传播后也会使最终计划失去意义。

**空间鲁棒性缺失**：高层规划器通常在抽象潜在空间中生成子目标表示，但这些抽象向量必须被“接地”（grounding）到连续的感知-动作空间才能执行。现有方法多采用简单的全局池化或向量拼接来融合高层计划与视觉特征，缺乏结构化的对齐机制。这导致规划与执行之间存在显著的语义鸿沟：规划器“知道要做什么”，但执行器“不知道该看哪里”。

以当前先进方法 **LBP**（Latent Backward Planning, Liu et al., ICML 2025）为例，它通过后向潜在规划生成从目标到当前状态的子目标序列，在一定程度上缓解了前向规划的误差累积问题。然而，LBP 仅依赖单一的后向规划器，缺乏对计划可执行性的显式验证，且直接将计划向量与视觉特征拼接后送入策略网络，未能有效解决空间接地问题。在真实世界的6阶段长程任务中，LBP 的性能随阶段增加急剧崩溃——任务3的成功率仅为5%，任务4仅为2%——充分暴露了上述两个瓶颈的严重性。

AGiLe 的核心动机正是针对这两个缺口：**在时间维度上引入双向验证机制，在空间维度上引入可供性锚定机制，从而联合提升长程操作的鲁棒性**。其核心洞察在于将复杂的长程操作解耦为“做什么”（高层双向规划）和“怎么做”（可供性锚定执行）两个子问题，并通过训练时的知识蒸馏将计划的一致性与可达性约束内化到规划器参数中，使推理时无需额外计算开销即可获得时间鲁棒性。

## 核心创新

AGiLe 的核心创新在于将长程操作任务解耦为两个正交但互补的子问题，并通过两项关键设计分别解决：**双向潜在规划**（Bidirectional Latent Planning）解决时间鲁棒性，**可供性锚定**（Affordance Grounding）解决空间鲁棒性。

### 创新一：双向潜在规划 —— 时间鲁棒性的因果旋钮

长程操作的根本瓶颈之一是预测误差随规划步数累积导致的计划崩溃（时间鲁棒性缺失）。现有方法如 **LBP**（Liu et al., ICML 2025）仅采用后向潜在规划，生成从目标到当前状态的子目标序列，但缺乏对计划可执行性的显式验证——规划器可能生成一个在隐空间中看似合理、但实际无法执行的子目标序列。

AGiLe 引入了一个**前向评论家**（Forward Critic）$\mathcal{V}_{\mathrm{fwd}}$ 作为闭环验证器。该评论家是一个 MLP 前向模型，输入任意候选子目标 $\mathbf{z}_i$ 和当前状态编码 $\mathbf{z}_0$，预测最终目标 $\mathbf{z}_g$。其核心机制通过三个损失函数实现联合优化：

- **后向模仿损失** $\mathcal{L}_{\mathrm{backward}}$：最小化预测子目标序列与专家序列的余弦距离（Equation 1）。
- **前向真实一致性损失** $\mathcal{L}_{\mathrm{fwd\_gt}}$：确保专家的真实子目标能预测到最终目标（Equation 2）。
- **前向预测一致性损失** $\mathcal{L}_{\mathrm{fwd\_pred}}$：确保规划器生成的子目标 $\hat{\mathbf{z}}_i$ 也能预测到最终目标（Equation 3）。

三者的联合目标为：

$$\mathcal{L}_{\mathrm{planner}} = \mathcal{L}_{\mathrm{backward}} + \lambda_c (\mathcal{L}_{\mathrm{fwd\_gt}} + \mathcal{L}_{\mathrm{fwd\_pred}})$$

这一设计的**核心洞察**在于知识蒸馏：联合优化将评论家对计划可达性和动态一致性的知识内化到规划器参数中。其直接后果是，**推理时可完全丢弃评论家**，仅用后向规划器生成计划，在不增加任何计算开销的前提下获得时间鲁棒性。消融实验（Table 2）验证了这一设计的决定性作用：移除前向评论家后，LIBERO-LONG 平均成功率从 97.1% 骤降至 89.0%。

### 创新二：可供性锚定 —— 空间鲁棒性的接地机制

长程操作的第二个瓶颈是规划-执行鸿沟（空间鲁棒性缺失）：高层抽象计划（隐向量序列）需要可靠地接地到连续感知-动作空间，但直接将计划向量与视觉特征拼接或全局池化后送入策略网络（如 LBP 的做法）缺乏结构化的接地机制，导致模型难以在复杂场景中定位任务相关区域。

AGiLe 提出**可供性锚定模块**，将复杂视觉运动问题解耦为“看哪里”（可供性锚定）和“做什么”（动作生成）两个子问题。其核心操作是**多头交叉注意力**（Multi-Head Cross-Attention）：

$$\mathbf{A}, \mathbf{f}_{\mathrm{temp}} = \mathrm{CrossAttn}(\mathrm{Query}=\mathbf{q}_{\mathrm{task}}, \mathrm{Key}=\mathbf{V}_{\mathrm{seq}}, \mathrm{Value}=\mathbf{V}_{\mathrm{seq}})$$

其中，$\mathbf{q}_{\mathrm{task}}$ 是由规划器生成的子目标序列与初始状态融合而成的任务查询向量，$\mathbf{V}_{\mathrm{seq}}$ 是视觉编码器提取的当前观测特征图序列。注意力权重矩阵 $\mathbf{A}$ 本质上构成了一张**像素级可供性图**（affordance map），显式标定视觉空间中与当前子任务相关的区域；参与后的特征 $\mathbf{f}_{\mathrm{attended}}$ 则隔离了无关视觉噪声，仅保留任务相关信息。

这一设计的因果效应在消融实验中同样得到验证：移除可供性锚定模块（改用全局平均池化和拼接）使成功率从 97.1% 降至 90.5%（Table 2）。

### 创新三：两阶段训练范式

与 LBP 的单阶段端到端训练不同，AGiLe 采用两阶段训练策略（Section 4.5）：第一阶段训练双向规划器并冻结其参数；第二阶段端到端训练可供性锚定模块和基于 DDPM 的策略解码器。这种解耦设计使得规划器能够专注于学习时间连贯的子目标序列，而执行模块则专注于学习从可供性特征到低层动作的映射，避免了联合训练中的优化冲突。

### 与 Baseline 的核心差异总结

| 设计维度 | LBP（Liu et al., ICML 2025） | AGiLe（本文） |
|---------|---------------------------|-------------|
| 规划方向与一致性 | 仅后向潜在规划，无执行验证 | 双向规划：后向规划器 + 前向评论家联合训练，知识蒸馏内化可达性约束 |
| 计划执行接地 | 计划向量与视觉特征直接拼接/池化 | 可供性锚定：任务查询通过交叉注意力生成像素级可供性图，隔离噪声 |
| 训练范式 | 单阶段端到端训练 | 两阶段训练：规划器冻结后训练执行模块 |

这两项创新——双向规划提供的**时间鲁棒性**和可供性锚定提供的**空间鲁棒性**——联合构成了 AGiLe 在 LIBERO-LONG 基准上达到 97.1% 平均成功率（超越 LBP 8.5 个百分点）并在 10 个任务中的 7 个上实现 100% 成功率的因果基础。

## 整体框架

AGiLe 的整体框架围绕一个核心解耦思想构建：将长程操作任务拆分为“做什么”的高层规划与“怎么做”的低层执行，并分别通过**双向潜在规划**和**可供性锚定**两个模块加以解决。Figure 2 展示了完整的端到端流程。

![[assets/figures/papers/paper_list_l2247_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_AGiLe_Learning_Ro/figures/002_Figure_2.jpg]]
*Figure 2: The Overview of AGiLe Framework. (1) Bidirectional Latent Planning: A pre-trained DecisionNCE encodes the initial observation to*

### 输入与编码

系统接收多模态上下文 $c$，包括语言指令 $l$ 和初始观测 $I_0$。预训练的 **DecisionNCE 编码器**将这些输入映射到统一的隐空间，分别产生初始状态隐向量 $\mathbf{z}_0$ 和目标隐向量 $\mathbf{z}_g$。这一共享隐空间是后续规划与执行模块协同工作的基础。

### 高层规划：双向潜在规划器

**后向规划器** $P_{\text{back}}$ 由初始预测器 $P_{\text{init}}$ 和递归 Transformer $P_{\text{recursive}}$ 组成，以自回归方式从目标 $\mathbf{z}_g$ 向当前状态 $\mathbf{z}_0$ 生成子目标序列 $\mathbf{Z}_{\text{plan}} = \{\hat{\mathbf{z}}_1, \hat{\mathbf{z}}_2, \dots, \hat{\mathbf{z}}_K\}$。**前向评论家** $\mathcal{V}_{\text{fwd}}$ 是一个 MLP，它从任意候选子目标 $\mathbf{z}$ 和当前状态 $\mathbf{z}_0$ 预测最终目标，用于评估生成计划的可达性与目标一致性。关键在于，前向评论家仅在训练时参与联合优化，通过知识蒸馏将可达性约束内化到规划器参数中，推理时即可丢弃，不增加计算开销。

### 低层执行：可供性锚定与扩散策略

规划器生成的隐子目标序列与 $\mathbf{z}_0$ 融合，形成任务特定的 **Query** $\mathbf{q}_{\text{task}}$。同时，**视觉编码器** $E_{\text{vis}}$ 将当前观测 $I_t$ 处理为保留空间结构的视觉特征图 $\mathbf{F}_{\text{vis}}$。**可供性锚定模块**（Multi-Head Cross-Attention）以 $\mathbf{q}_{\text{task}}$ 为 Query、视觉特征序列为 Key/Value，计算交叉注意力权重，生成任务相关的参与视觉特征 $\mathbf{f}_{\text{attended}}$——这一过程将抽象的子目标“接地”到像素级视觉可供性上，明确告诉策略“看哪里”。

最后，$\mathbf{f}_{\text{attended}}$ 与机器人本体感知状态 $\mathbf{p}_t$ 拼接后，作为条件输入**基于 DDPM 的策略解码器** $\pi_\theta$，通过迭代去噪生成精确的低层动作序列，完成“怎么做”的执行。

### 训练范式

AGiLe 采用两阶段训练策略：第一阶段联合训练双向规划器并冻结参数；第二阶段端到端训练可供性锚定模块和扩散策略解码器。这种解耦设计使得规划器的目标一致性约束与策略的视觉-动作映射可以分别优化，同时保持模块间的信息流动。

> **需人工验证**：当前证据未明确说明两阶段训练中，规划器训练是否依赖专家子目标序列的标注，以及第二阶段训练时规划器是否完全不接收执行反馈。

## 核心模块与公式推导

AGiLe 框架的核心由两个关键创新组成：**双向潜在规划器（Bidirectional Latent Planner）** 和 **可供性锚定模块（Affordance Grounding Module）**，分别解决长程操作中的时间鲁棒性与空间鲁棒性问题。

### 双向潜在规划器

规划器包含两个协同优化的组件：

- **后向规划器（Backward Planner）** $P_{\text{back}}$：由初始预测器 $P_{\text{init}}$ 和递归 Transformer $P_{\text{recursive}}$ 组成，以预训练的 DecisionNCE 编码器提供的统一隐空间为基础，自回归地从最终目标 $\mathbf{z}_g$ 向当前状态 $\mathbf{z}_0$ 生成子目标序列 $\hat{\mathbf{z}}_1, \dots, \hat{\mathbf{z}}_K$。
- **前向评论家（Forward Critic）** $\mathcal{V}_{\text{fwd}}$：一个 MLP 实现的前向模型，接收任意候选子目标 $\mathbf{z}$ 和当前状态 $\mathbf{z}_0$，预测其对应的最终目标。评论家仅在训练阶段使用，推理时可丢弃。

规划器的训练目标由三个损失函数联合构成：

**后向模仿损失**：最小化预测子目标序列与专家序列之间的余弦距离：

$$\mathcal{L}_{\mathrm{backward}} = \sum_{i=1}^{K} \mathcal{L}_{\mathrm{cosine}}(\hat{\mathbf{z}}_i, \mathbf{z}_i)$$

**前向一致性损失（真实专家子目标）**：确保专家的真实子目标能够可靠地预测到最终目标：

$$\mathcal{L}_{\mathrm{fwd}\_\mathrm{gt}} = \sum_{i=1}^{K} \mathcal{L}_{\mathrm{cosine}}(\mathcal{V}_{\mathrm{fwd}}(\mathbf{z}_i, \mathbf{z}_0), \mathbf{z}_g)$$

**前向预测损失**：强制生成的子目标同样能够预测到最终目标，将评论家的可达性知识蒸馏到规划器参数中：

$$\mathcal{L}_{\mathrm{fwd}\_\mathrm{pred}} = \sum_{i=1}^{K} \mathcal{L}_{\mathrm{cosine}}(\mathcal{V}_{\mathrm{fwd}}(\hat{\mathbf{z}}_i, \mathbf{z}_0), \mathbf{z}_g)$$

三者组合为规划器的联合训练目标：

$$\mathcal{L}_{\mathrm{planner}} = \mathcal{L}_{\mathrm{backward}} + \lambda_c (\mathcal{L}_{\mathrm{fwd}\_\mathrm{gt}} + \mathcal{L}_{\mathrm{fwd}\_\mathrm{pred}})$$

其中 $\lambda_c$ 为平衡系数。该联合优化的核心假设是：通过前向预测损失，评论家对计划可达性和动态一致性的判断被内化到规划器参数中，从而在推理时无需运行评论家即可获得时间鲁棒的规划能力。

### 可供性锚定模块

该模块将抽象的子目标计划转化为像素级的视觉可供性，实现空间接地。其核心是一个多头交叉注意力（Multi-Head Cross-Attention）层：

$$\mathbf{A}, \mathbf{f}_{\mathrm{temp}} = \mathrm{CrossAttn}(\mathrm{Query}=\mathbf{q}_{\mathrm{task}}, \mathrm{Key}=\mathbf{V}_{\mathrm{seq}}, \mathrm{Value}=\mathbf{V}_{\mathrm{seq}})$$

其中：
- $\mathbf{q}_{\mathrm{task}}$ 为任务查询向量，由规划器产生的子目标序列与当前状态 $\mathbf{z}_0$ 融合而成，封装了“要完成什么”的任务意图；
- $\mathbf{V}_{\mathrm{seq}}$ 为视觉编码器 $E_{\text{vis}}$ 从当前观测中提取的视觉特征序列，保留了空间对应关系；
- $\mathbf{A}$ 为注意力权重矩阵，可解释为像素级的可供性图（affordance map），指示“在哪里操作”；
- $\mathbf{f}_{\mathrm{temp}}$ 为参与后的视觉特征，经进一步处理得到 $\mathbf{f}_{\mathrm{attended}}$，作为后续动作生成的视觉条件。

### 动作扩散策略解码器

策略解码器 $\pi_\theta$ 采用条件去噪扩散概率模型（DDPM），以可供性锚定后的视觉特征 $\mathbf{f}_{\mathrm{attended}}$ 和机器人本体感知状态 $\mathbf{p}_t$ 为条件，生成低层动作序列。其训练目标为标准的噪声预测 MSE：

$$\mathcal{L}_{\mathrm{action}} = \mathbb{E}_{t,k,a_t,\epsilon,c}\left[ || \epsilon - \epsilon_\theta \big( a_t^k, k, \mathrm{concat}(\mathbf{f}_{\mathrm{attended}}, \mathbf{p}_t) \big) ||^2 \right]$$

其中 $k$ 为扩散步数索引，$\epsilon$ 为标准高斯噪声，$\epsilon_\theta$ 为去噪网络（实现为多块残差 MLP），$a_t^k$ 为第 $k$ 步加噪后的动作序列。

### 两阶段训练范式

AGiLe 采用两阶段训练策略：**第一阶段**联合训练双向规划器（后向规划器 + 前向评论家），训练完成后冻结规划器参数；**第二阶段**端到端训练可供性锚定模块和扩散策略解码器，规划器仅用于推理生成子目标序列。这种解耦设计使得规划器的可达性知识在冻结后稳定地服务于执行阶段，同时避免了联合微调可能带来的优化冲突。

### 补充图表

![[assets/figures/papers/paper_list_l2247_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_AGiLe_Learning_Ro/figures/001_Figure_1.jpg]]
*Figure 1: The Difference between AGiLe and Existing Methods. AGiLe achieves both temporal and spatial robustness by employing bidirectional latent planning combined with affordance grounding, thereby enhancing the robustness of long-horizon manipulation tasks*

## 实验与分析

### 核心性能对比

AGiLe 在 LIBERO-LONG 基准上取得 **97.1%** 的平均成功率，相较前最佳方法 **LBP** (Liu et al., ICML 2025) 的 88.6% 提升 **+8.5%**（Table 1）。更关键的是，在 10 个多阶段长程任务中，AGiLe 有 **7 个达到 100% 成功率**，展现出高度稳定的任务完成能力，而非仅在部分任务上偶发高分。Table 1 同时报告了其他基线方法的结果，均引自原始论文以保证可比性；为减少训练方差，AGiLe 和 LBP 的结果均取每个任务最优 3 个检查点的平均性能。

![[assets/figures/papers/paper_list_l2247_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_AGiLe_Learning_Ro/figures/004_Table_1.jpg]]
*Table 1: Comparison on the LIBERO-LONG benchmark. We report the average success rate (%) over 10 rollouts for each multi-stage task. To ensure a fair comparison and mitigate training variance, all results for both AGiLe and the LBP baseline [27] are calculated by averaging the performance of the top-3 saved checkpoints for each task. Baseline results for other methods are sourced from their respective original publications. Bold indicates the best performance in each column*

这一性能跃升的因果根源在于 AGiLe 同时解决了两个瓶颈：**时间鲁棒性**（预测误差随规划步数累积导致计划崩溃）和**空间鲁棒性**（高层抽象计划无法可靠接地到连续感知-动作空间）。双向潜在规划通过前向评论家验证子目标可达性，将一致性与可达性约束内化到规划器参数中；可供性锚定模块则以任务查询交叉注意力过滤视觉特征，生成像素级任务相关表征，隔离无关区域的噪声干扰。

### 消融实验：两个关键组件的因果验证

Table 2 的消融结果直接量化了各组件的独立贡献：

- **移除前向评论家**（仅用后向模仿损失训练规划器）：成功率从 97.1% **骤降至 89.0%**。这表明单纯的后向规划缺乏对计划可执行性的显式验证，生成的子目标序列虽在语义上接近专家，但在动态上不可达，导致执行阶段频繁崩溃。前向评论家提供的知识蒸馏是时间鲁棒性的核心来源。
- **移除可供性锚定模块**（用全局平均池化和拼接代替交叉注意力接地）：成功率降至 **90.5%**。这验证了直接将计划向量与全局视觉特征融合无法有效建立任务-场景的空间对应关系，规划与执行之间的接地鸿沟依然存在。多头交叉注意力机制通过显式计算任务查询与视觉特征图的对齐，为策略提供了结构化的“看哪里”引导。

两组消融的下降幅度均显著（约 7-8 个百分点），且彼此独立作用于时间维度和空间维度，共同构成了 AGiLe 性能优势的充分条件。

### 真实世界验证：长程鲁棒性的压力测试

在真实世界 4 个 6 阶段长程操作任务中（Figure 4），AGiLe 展现出随阶段数增加仍能维持高鲁棒性的能力。相比之下，基线 LBP 的性能随阶段增加急剧崩溃：在任务 3 中仅剩 5%，任务 4 中降至 2%。这一对比直接暴露了仅依赖后向规划的脆弱性——随着任务阶段增多，累积的预测误差和接地失败使执行几乎必然偏离轨道。AGiLe 的双向验证和可供性锚定机制有效抑制了这种级联退化。

![[assets/figures/papers/paper_list_l2247_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_AGiLe_Learning_Ro/figures/007_Figure_4.jpg]]
*Figure 4: Real-world validation. Stage-wise average score (10 rollouts) for AGiLe (Ours) vs. LBP (Baseline) on 4 real-world longhorizon manipulation tasks. AGiLe demonstrates significantly higher robustness and less performance degradation as the number of sequential stages increases*

### 失败模式与局限

尽管 LIBERO-LONG 上 7/10 任务达到 100% 成功率，剩余 3 个任务的非完美表现提示了模型在特定场景下的失败模式。结合论文报告的局限性，可能的失败来源包括：

1. **规划冻结导致的适应性不足**：当前两阶段训练范式下，规划器在第一阶段冻结后无法根据执行反馈动态调整计划。当环境出现训练分布外的扰动或物体位姿偏移时，预生成的子目标序列可能不再适用，而策略缺乏在线修正机制。
2. **开放世界泛化未验证**：AGiLe 在 LIBERO-LONG 的受控场景中表现优异，但对于未见物体类别、显著视觉语义变化的大域偏移场景，其鲁棒性尚待检验。可供性锚定模块依赖视觉编码器提取的特征质量，域偏移可能导致任务查询与视觉特征的对齐失效。

### 重要图表结论

- **Table 1**：AGiLe 在 LIBERO-LONG 上以 97.1% 平均成功率显著超越 LBP（88.6%），10 个任务中 7 个达到满分。
- **Table 2**：消融实验证实前向评论家（贡献约 8.1 个百分点）和可供性锚定（贡献约 6.6 个百分点）均为性能的关键支撑。
- **Figure 4**：真实世界 6 阶段任务中，AGiLe 保持高鲁棒性，而 LBP 在后期阶段性能崩溃至接近零，验证了双向规划与可供性接地在长程场景下的不可替代性。

### 补充图表

![[assets/figures/papers/paper_list_l2247_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_AGiLe_Learning_Ro/figures/003_Figure_3.jpg]]
*Figure 3: Left: The real-world setup; Right: Visualizations of the sub-task stages of 4 real-world long-horizon manipulation tasks*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

AGiLe 的直接前身与主要对比基线是 **LBP**（Latent Backward Planning，Liu et al., ICML 2025）。LBP 首次提出在预训练的隐空间（DecisionNCE）中进行后向规划，从目标状态自回归地生成子目标序列，以缓解长程任务中前向预测误差累积导致的“计划崩溃”。然而，LBP 在两个关键维度上存在结构缺陷：

- **时间鲁棒性缺失**：LBP 仅依赖后向模仿损失来训练规划器，缺乏对生成计划的可执行性验证。这意味着规划器可能生成在隐空间中“看起来合理”但实际不可达的子目标序列，当执行步数增加时，预测误差逐步放大，导致计划与真实状态之间出现不可恢复的漂移。
- **空间鲁棒性缺失**：LBP 将规划产生的隐向量与视觉特征进行全局池化拼接后直接送入策略网络，缺少结构化的接地机制。这种“扁平化”融合使高层抽象计划难以精确对应到像素级的视觉上下文，在需要精细空间推理的操作任务中产生规划-执行鸿沟。

AGiLe 对 LBP 的改进并非简单的增量修补，而是从两个正交维度进行了结构性增强：

1. **双向潜在规划**：在保留后向规划器的基础上，引入前向评论家（Forward Critic）作为计划验证器。前向评论家以任意子目标和当前状态为输入，预测最终目标，从而评估子目标序列的目标一致性。关键创新在于训练策略——通过联合优化后向模仿损失与前向一致性损失（含真实专家子目标和生成子目标两条路径），将评论家的可达性知识蒸馏到规划器参数中。这使得推理时可以丢弃评论家，在不增加计算开销的前提下获得时间鲁棒性。

2. **可供性锚定**：将计划编码为任务查询（Task Query），通过多头交叉注意力与视觉特征图交互，生成像素级的注意力权重图（即可供性图），实现“看哪里”与“做什么”的解耦。这种机制使抽象子目标能够精确地接地到当前观测中的任务相关区域，同时隔离与任务无关的视觉噪声。

从方法演进的角度看，AGiLe 将 LBP 的单向规划扩展为“生成-验证”闭环，将 LBP 的扁平融合升级为注意力驱动的结构化接地，本质上是在规划的时间一致性与执行的空间精度两个维度上同时填补了 LBP 的空白。

### 2. 在更广知识库中的定位

AGiLe 处于长程操作策略学习的交叉地带，涉及三个活跃的研究脉络：

- **基于规划的操作策略**：与分层强化学习中的子目标生成方法（如 HIRO、HRL）和基于模型的规划方法（如 Dreamer 系列）共享“先规划后执行”的范式。但 AGiLe 的区别在于：规划发生在预训练的语义隐空间中，而非原始状态空间；规划方向为后向（从目标回溯），而非传统的前向展开；且规划器与执行器解耦训练，避免了端到端分层训练的不稳定性。

- **语言引导的操作策略**：与 RT-2、SayCan、CLIPort 等利用语言指令引导操作的方法同属语言条件策略范畴。AGiLe 的独特贡献在于将语言指令编码为隐空间中的目标向量，并通过双向规划将其展开为可执行的子目标序列，而非直接将语言映射为动作。这种“语言→目标→计划→动作”的级联分解，使 AGiLe 在长程任务中具有更好的时间扩展性。

- **可供性驱动的操作**：与 Where2Act、Affordance Diffusion 等显式建模可供性的方法共享“先定位后操作”的思想。AGiLe 的创新在于将可供性锚定与隐空间规划深度耦合——可供性图不是从静态场景中独立预测的，而是以任务查询为条件的动态生成，使“看哪里”与“要达成什么子目标”紧密关联。

### 3. 适用边界

AGiLe 的设计假设决定了其适用范围：

- **任务类型**：适用于具有明确多阶段结构的长程操作任务，每个阶段有可定义的子目标。对于单阶段任务或子目标边界模糊的任务，双向规划的优势可能无法充分体现。
- **环境特性**：假设观测空间与演示数据分布相对稳定。当前方法未针对大规模域偏移（如全新物体类别、剧烈光照变化）进行验证。
- **数据需求**：依赖专家演示数据来训练规划器和策略解码器，且需要预训练的 DecisionNCE 编码器提供共享隐空间。在演示数据稀缺或隐空间质量不足的场景下，性能可能显著下降。
- **推理约束**：两阶段框架中规划器在训练后冻结，推理时无法根据执行反馈动态调整计划。这意味着 AGiLe 本质上是开环规划+闭环执行的混合架构，而非完全的闭环规划。

### 4. 局限与开放问题

**已确认的局限**：

- **静态规划**：规划器冻结且独立训练，无法在执行过程中根据环境变化或执行偏差实时调整子目标序列。这限制了 AGiLe 在高度动态或随机环境中的适应性。
- **泛化未验证**：在开放世界中，对于未见物体类别和显著视觉域偏移的泛化能力尚未经过系统测试。当前评估仅限于 LIBERO-LONG 基准和受控的真实世界设置。
- **两阶段解耦的代价**：规划器与执行器的分离训练虽然简化了优化，但也切断了执行反馈对规划的信息回流。这种信息隔离可能限制了系统在需要精细协调规划与执行的复杂任务上的性能上限。

**开放问题**：

- **端到端联合优化**：是否可能实现规划器与执行器的端到端联合训练，同时保持训练的稳定性？在线规划精修（online plan refinement）机制能否使规划器从执行反馈中实时学习，实现真正的闭环规划？
- **开放世界扩展**：如何将 AGiLe 扩展到更通用的开放世界环境？这需要解决隐空间编码器对域偏移的鲁棒性、可供性锚定模块对全新物体类别的泛化能力，以及规划器对未见任务结构的适应能力。
- **更紧耦合的范式**：两阶段解耦训练是否限制了规划与执行之间的信息流动？是否存在一种更紧耦合的范式（如联合训练+知识蒸馏的变体），能在保持训练稳定性的同时提升数据效率？
- **规划粒度的自适应**：当前子目标数量 K 是固定的超参数。是否可以让模型自适应地决定所需的规划步数，以应对不同复杂度的任务？

## 原文 PDF

![[paperPDFs/CVPR_2026/AGiLe_Learning_Robust_Long_Horizon_Manipulation_via_Affordance_Grounded_Bidirectional_Latent_Planning.pdf]]
