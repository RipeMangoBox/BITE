---
title: "Dynamic Worlds, Dynamic Humans: Generating Virtual Human-Scene Interaction Motion in Dynamic Scenes"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Dynamic_Worlds_Dynamic_Humans_Generating_Virtual_Human_Scene_Interaction_Motion_in_Dynamic_Scenes.pdf
aliases:
- DH
- DWDHGVHSIMDS
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入动态场景感知导航和层次化经验记忆，使虚拟人能够实时感知场景变化，并检索过往经验以自适应调整运动。
primary_logic: 受世界模型启发的认知架构（视觉-记忆-控制）通过持续感知、经验检索和自适应条件融合，能够生成高质量的动态人-场景交互运动。
claims:
- Dyn-HSI在LINGO静态基准上达到FID 0.092，显著优于现有最佳方法。
- 在动态场景基准Dyn-LINGO上，Dyn-HSI的Pene.Value为39.19，远低于其他方法，表明其能有效避免穿透。
- 消融实验：移除动态场景感知导航导致轨迹相似度下降12.41%，穿透值增加12.88（静态）和9.40（动态）。
- 移除层次化经验记忆在分布外场景中使穿透值恶化96.86%，表明记忆对泛化至关重要。
---

# Dynamic Worlds, Dynamic Humans: Generating Virtual Human-Scene Interaction Motion in Dynamic Scenes

> [!tip] 核心洞察
> 受世界模型启发的认知架构（视觉-记忆-控制）通过持续感知、经验检索和自适应条件融合，能够生成高质量的动态人-场景交互运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | 动态世界中的动态人类：动态场景下虚拟人-场景交互运动生成 |
| 英文题名 | Dynamic Worlds, Dynamic Humans: Generating Virtual Human-Scene Interaction Motion in Dynamic Scenes |
| 会议/期刊 | arXiv 2026 |
| Links |  [paper](https://arxiv.org/abs/2601.19484)|
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Dyn-HSI |
| Dataset | LINGO, Dyn-LINGO, Dyn-Trumans, User Study |

> [!tip] 效果简介
> - LINGO (static) 上，FID↓ 0.092 vs ≈0.283 (Trumans) (-67.45%)；Traj. sim.↑ 90.01% vs N/A (LINGO: lower) (Best)；Goal. err.↓ N/A vs LINGO (-96.36%)。
> - Dyn-LINGO (dynamic) 上，Pene.Value↓ 39.19 vs N/A (LINGO: higher) (Significantly lower)。
> - Dyn-Trumans (OoD dynamic) 上，Pene.Value↑ over static +5.74% vs +96.86% (w/o memory) (Robust to OoD)。

## 概述

### 研究问题与瓶颈

现有的人-场景交互（Human-Scene Interaction, HSI）运动生成方法普遍将场景视为静态背景，依赖固定的全局场景占用信息作为输入。这一假设在真实动态环境中会迅速失效——当场景中的物体发生移动、旋转或出现/消失时，虚拟人无法感知这些变化，导致严重的穿透现象和交互失败。这一瓶颈的根本原因在于：传统方法缺乏对场景动态性的持续感知能力，也无法从过往经验中检索适配当前情境的运动先验。

### 核心方案

本文提出 **Dyn-HSI**，一种受世界模型启发的认知架构，将人-场景交互生成重新构建为“视觉-记忆-控制”三层体系：

- **视觉模块（Dynamic Scene-Aware Navigation）**：使虚拟人能够持续感知场景变化，基于局部体素占用信息动态预测下一步位置，并输出置信度分数以评估预测可靠性。
- **记忆模块（Hierarchical Experience Memory）**：存储和检索噪声运动数据，实现上下文感知的运动启动（context-aware motion priming），为扩散模型提供更优的初始化先验。
- **控制模块（HSI Diffusion Model with Condition Adapter）**：通过自适应条件适配器动态调节场景、轨迹、文本、目标等多模态条件的融合权重，生成高质量的人-场景交互运动序列。

三者以自回归方式协同工作：视觉模块感知变化并规划轨迹，记忆模块检索经验并初始化运动，控制模块生成最终交互动作，形成闭环的感知-记忆-生成流水线。

### 方法定位

Dyn-HSI 在方法谱系上属于**自回归运动扩散模型**，但与现有工作存在三个关键差异：

| 设计维度 | 现有方法 | Dyn-HSI |
|---------|---------|---------|
| 场景处理 | 静态全局占用作为固定输入（如 **LINGO** (Jiang et al., SIGGRAPH Asia 2024)、**Trumans** (Jiang et al., CVPR 2024)） | 每步动态更新的局部占用，配合场景变化检测 |
| 条件融合 | 固定或拼接的条件权重（如 **SceneDiffuser** (Huang et al., CVPR 2023)） | 基于任务属性自适应的条件权重（Condition Adapter） |
| 运动初始化 | 随机高斯噪声 | 从层次化经验记忆中检索的上下文感知运动先验 |
| 轨迹规划 | 预定义路径或无置信度的A*搜索 | 基于Transformer的迭代预测，附带置信度分数 |

### 主要结果概览

在静态场景基准 LINGO 上，Dyn-HSI 的 FID 达到 0.092，较现有最佳方法 Trumans（≈0.283）降低 67.45%；轨迹相似度达 90.01%，目标误差较 LINGO 降低 96.36%。

在动态场景基准 Dyn-LINGO 上，Dyn-HSI 的穿透值（Pene.Value）为 39.19，远低于其他方法，验证了动态场景感知导航的有效性。在分布外动态场景 Dyn-Trumans 上，Dyn-HSI 的穿透值仅增加 5.74%，而移除层次化经验记忆后恶化 96.86%，表明记忆模块对泛化至关重要。

用户研究中，Dyn-HSI 的文本对齐评分达 4.87/5.00，较 LINGO（≈3.42）提升 42.39%。

### 局限与开放问题

Dyn-HSI 的推理速度仍不理想，主要瓶颈来自动态场景感知导航的迭代预测（消融版本速度接近 MotionDiffuse）。当前动态场景为手工模拟，未能完全捕捉真实世界的复杂性（如细微物体运动、拥挤场景）。训练完全依赖静态数据集 LINGO，缺乏大规模动态交互数据可能限制极限场景下的性能。如何在不牺牲动态感知能力的前提下加速推理、以及如何扩展到更复杂的真实世界动态场景，是未来工作的关键方向。

## 背景与动机

### 问题背景：静态世界假设的局限

虚拟人-场景交互（Human-Scene Interaction, HSI）运动生成是计算机图形学与具身AI交叉领域的核心问题，其目标是根据文本指令或目标位置，生成虚拟人在3D场景中自然移动并与物体交互的运动序列。近年来，基于扩散模型的方法在该领域取得了显著进展，如**LINGO**（Jiang et al., SIGGRAPH Asia 2024）、**Trumans**（Jiang et al., CVPR 2024）和**SceneDiffuser**（Huang et al., CVPR 2023）等，能够在静态场景中生成高质量的人体运动。

然而，现有方法存在一个根本性的瓶颈：**它们将场景视为静态不变的**。这些方法的输入是固定的全局场景占据表示，在整个运动生成过程中不会更新。当场景发生动态变化时——例如一把椅子被移走、一扇门被关上、或一个障碍物突然出现——这些方法无法感知变化，导致虚拟人出现严重的行为错误：穿透已移动的物体、与场景发生碰撞、或无法到达新的目标位置。

### 现有方法的缺口

具体而言，现有HSI方法面临三个关键缺口：

1. **缺乏动态感知能力**：现有方法（如LINGO、Trumans）使用静态体素占据作为固定输入，无法持续感知环境变化。当场景物体移动或消失时，虚拟人仍按照原始场景规划路径，导致穿透和交互失败。

2. **缺乏经验积累与回忆机制**：现有方法对每个新场景从头开始生成运动，无法利用过往经验来加速推理或提升质量。在分布外（Out-of-Distribution, OoD）场景中，由于缺乏可参考的历史经验，生成质量急剧下降。

3. **条件融合缺乏自适应性**：HSI生成通常依赖多种条件信号（文本、场景、轨迹、目标位置），但现有方法采用固定权重或简单拼接的方式融合这些条件，无法根据任务属性动态调整各条件的重要性。

### 本文动机：从世界模型视角重新思考HSI

受认知科学中世界模型（World Model）概念的启发，本文提出一个核心洞察：**一个能够持续感知、记忆和自适应控制的认知架构，是解决动态场景下HSI生成问题的关键**。具体而言，虚拟人应当具备：

- **视觉能力**：持续感知场景变化，实时更新对环境的理解；
- **记忆能力**：积累并检索过往的运动经验，实现上下文感知的运动启动；
- **控制能力**：根据当前任务自适应地融合多模态条件，生成高质量的运动序列。

基于这一洞察，本文提出**Dyn-HSI**，一个面向动态场景的虚拟人-场景交互运动生成框架。Dyn-HSI通过自回归运动扩散模型，将视觉-记忆-控制三个模块有机整合，使虚拟人首次能够在动态环境中实时调整运动，避免穿透并保持高质量的交互。

## 核心创新

Dyn-HSI 的核心创新在于将传统静态场景假设下的人-场景交互（HSI）生成范式，重构为一套**受世界模型启发的认知架构**（Vision–Memory–Controller），使虚拟人能够实时感知动态环境变化、检索过往经验并自适应调整运动策略。这一架构转变直接解决了现有方法在动态场景中因缺乏场景感知和记忆能力而导致的穿透、轨迹偏离和交互失败等瓶颈问题。

具体而言，Dyn-HSI 在以下四个关键维度上实现了相对于现有方法的根本性变革：

### 1. 场景处理：从静态全局占用到动态局部感知

现有方法（如 **LINGO**（Jiang et al., SIGGRAPH Asia 2024）、**Trumans**（Jiang et al., CVPR 2024））将场景视为固定的全局占用网格（static global occupancy），在整个生成过程中保持不变。Dyn-HSI 引入了**动态场景感知导航**（Dynamic Scene-Aware Navigation）模块，每步以角色骨盆为中心构建局部占用网格 $S_{local}$，并检测场景变化 $\Delta S^i$，实现逐帧更新的动态场景表示（Section 3.3, Fig. 3）。这一设计使虚拟人能够感知场景中物体的移动、出现或消失，从而在导航和交互中做出实时响应。

### 2. 初始化策略：从随机噪声到上下文感知的运动启动

传统扩散模型在运动生成时从随机高斯噪声开始采样，缺乏对当前场景和任务上下文的先验引导。Dyn-HSI 设计了**层次化经验记忆**（Hierarchical Experience Memory），按动作、细粒度动作变体和场景上下文三个层级存储带噪运动表征。在推理时，系统根据当前任务属性检索最匹配的记忆表征，将其作为扩散模型的启动噪声（Section 3.4），实现了上下文感知的运动初始化（context-aware motion priming）。这一机制在分布外场景中尤为关键——消融实验表明，移除记忆模块后，分布外场景的穿透值恶化 96.86%（Table 3）。

### 3. 条件融合：从固定权重到自适应任务感知

现有方法通常采用固定的或简单拼接的条件权重来融合场景、文本、轨迹等多模态条件。Dyn-HSI 的 **HSI 扩散模型**中嵌入了**条件适配器**（Condition Adapter），通过 MLP 从文本特征 $T_f$ 中学习任务属性，并通过 Softmax 生成四个自适应权重系数 $[\mathbf{R}_1, \mathbf{R}_2, \mathbf{R}_3, \mathbf{R}_4]$，分别控制场景、轨迹、文本和目标条件的重要性（Section 3.5, Eq. 4）。这种自适应加权机制使模型能够根据具体任务动态调整对各条件的依赖程度，例如在“走到沙发前坐下”任务中自动增强目标条件的权重。消融实验证实，移除条件适配器使 FID 增加 0.178，MPJPE 增加 0.034（Section 4.5）。

### 4. 轨迹规划：从预定义路径到置信度感知的迭代预测

现有方法依赖预定义路径或基于 A* 算法的确定性规划，缺乏对路径质量的置信度评估。Dyn-HSI 采用基于 Transformer 解码器的迭代预测框架，在输出下一步位置 $P_{i+1}$ 的同时给出置信度分数 $C_{i+1}$（Section 3.3, Eq. 1）。置信度通过软目标进行训练，软目标由预测轨迹与真值轨迹的误差指数衰减得到，损失函数为 BCE（Eq. 2）。这一设计使系统能够识别导航不确定性较高的区域，为后续的运动生成提供可靠性信号。

### 创新总结

上述四个维度的变革并非孤立存在，而是通过**自回归生成循环**（Autoregressive Generation Loop）有机整合：动态场景感知导航提供置信度感知的轨迹规划，层次化经验记忆为扩散模型提供上下文感知的启动噪声，条件适配器根据任务属性自适应融合多模态条件，最终在统一的认知架构下实现动态场景中高质量的人-场景交互运动生成。

## 整体框架

Dyn-HSI 是一个面向文本驱动的动态人-场景交互运动生成的自回归运动扩散模型框架。其核心设计受世界模型启发的认知架构（视觉-记忆-控制）驱动，使虚拟人能够持续感知场景变化、检索过往经验，并自适应地生成高质量的交互运动。整体框架由三个关键模块构成：

1. **动态场景感知导航（Dynamic Scene-Aware Navigation）**：作为视觉模块，负责持续感知环境变化，检测场景中的动态事件，并基于当前人体位置和局部场景占用信息，通过 Transformer 解码器迭代预测下一步位置及其置信度。
2. **层次化经验记忆（Hierarchical Experience Memory）**：作为记忆模块，以三层递进结构（动作层、细粒度动作变化层、场景上下文层）存储噪声运动表示，实现上下文感知的运动启动，为扩散模型提供信息丰富的初始化。
3. **HSI 扩散模型与条件适配器（HSI Diffusion Model with Condition Adapter）**：作为控制模块，在扩散去噪过程中生成人-场景交互运动，并通过条件适配器根据任务属性自适应调节场景、轨迹、文本和目标条件的权重。

### 输入输出流

框架的输入包括：文本描述、动态 3D 场景的体素化表示 $S_t \in \{0,1\}^{L_s \times W_s \times H_s}$、目标位置，以及初始人体姿态。输出为人体运动序列 $\{M_i\}_{i=1}^{L_m}$，其中 $M_i \in \mathbb{R}^{J \times 3}$ 表示第 $i$ 帧的关节点位置。

### 自回归生成循环

Dyn-HSI 采用自回归方式将长序列运动分段生成。每个生成片段以前一段的最后两帧作为条件，确保运动的时间连续性。在每一步中，流程如下：

1. **动态场景感知导航**接收当前人体位置 $P_i$、文本特征 $T_f^i$、目标特征 $G_f^i$、局部场景占用 $S_f^i$ 以及场景变化信息 $\Delta_S^i$，通过 Transformer 解码器输出下一步位置 $P_{i+1}$ 和置信度 $C_{i+1}$：
   $$P_{i+1}, C_{i+1} = \text{Decoder}(P_i, [T_f^i; G_f^i; S_f^i; \Delta_S^i])$$
2. **层次化经验记忆**根据当前场景上下文和文本条件检索最匹配的噪声运动表示，作为扩散模型的初始化，替代传统的随机高斯噪声。
3. **HSI 扩散模型**在条件适配器生成的自适应权重 $[R_1, R_2, R_3, R_4]$ 引导下，融合场景、轨迹、文本和目标条件进行去噪，生成当前片段的交互运动：
   $$[R_1, R_2, R_3, R_4] = \text{Softmax}(\text{MLP}(T_f))$$
4. 生成的片段拼接到整体序列中，并将最后两帧作为下一轮的条件，进入下一个自回归循环。

### 训练目标

框架的联合训练损失为：
$$\mathcal{L} = \mathcal{L}_{motion} + \lambda_t \mathcal{L}_{traj} + \lambda_c \mathcal{L}_{conf}$$

其中 $\mathcal{L}_{motion}$ 为运动重建的 L2 损失，$\mathcal{L}_{traj}$ 为轨迹预测的 L2 损失，$\mathcal{L}_{conf}$ 为置信度估计的二元交叉熵损失。这种联合优化确保了运动生成精度、轨迹规划合理性和置信度估计的可靠性三者之间的平衡。

> **注意**：图 2 展示了 Dyn-HSI 的完整架构概览，包括三个核心模块及其数据流关系；图 3 详细描绘了动态场景感知导航模块的内部架构。关于各模块的具体实现细节，请参见后续章节。

### 补充图表

![[assets/figures/papers/paper_list_l1700_Dynamic_Worlds_Dynamic_Humans_Generating_Virtual_Human_Scene_Interaction/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Dyn-HSI. Dyn-HSI is an autoregressive motion diffusion model capable of iteratively generating human–scene interaction motions. It consists of three components: (1) dynamic scene-aware navigation, (2) hierarchical experience memory, and (3) HSI diffusion model*

## 核心模块与公式推导

### 3.1 问题形式化与数据表示

Dyn-HSI 将文本驱动的动态人-场景交互生成形式化为自回归运动扩散问题。给定文本描述 $T$、目标位置 $G$ 和动态 3D 场景序列 $\{S_t\}_{t=1}^{T}$，模型需要生成与场景变化相适应的人体运动序列。

**人体运动表示**：一段长度为 $L_m$ 的运动序列表示为 $\{M_i\}_{i=1}^{L_m}$，其中每帧 $M_i \in \mathbb{R}^{J \times 3}$ 包含 $J$ 个关节点的 3D 位置坐标。

**动态场景表示**：时刻 $t$ 的场景被体素化为三维占用网格 $S_t \in \{0,1\}^{L_s \times W_s \times H_s}$，其中 1 表示该体素被物体占据。场景随时间变化，要求模型持续感知并调整行为。

### 3.2 自回归运动扩散框架

Dyn-HSI 采用自回归生成策略（Section 3.2），将长运动序列分割为固定长度的片段逐段生成。每个片段的条件输入包括：前一片段最后两帧的运动状态、文本嵌入 $T_f$、目标特征 $G_f$、当前场景特征 $S_f$ 以及由导航模块预测的轨迹 $Traj$。这一设计使模型能够根据已生成的运动历史和实时场景状态迭代产生后续运动。

### 3.3 动态场景感知导航模块

该模块是 Dyn-HSI 的“视觉”组件，核心创新在于**检测场景变化并自适应预测下一步位置及置信度**（Section 3.3）。

**局部占用网格**：在每个时间步，以角色骨盆为中心、与角色朝向对齐构建局部占用网格 $S_{local}$，实现场景信息的动态更新。这一设计使模型仅关注角色周围的即时环境，而非整个静态场景。

**轨迹预测公式**（Eq. 1）：

$$P_{i+1}, C_{i+1} = Decoder(P_i, [T_f^i; G_f^i; S_f^i; \Delta_S^i])$$

其中：
- $P_i$ 为当前位置，$P_{i+1}$ 为预测的下一位置
- $C_{i+1}$ 为预测置信度，衡量该步预测的可靠性
- $T_f^i$ 为文本特征，$G_f^i$ 为目标特征，$S_f^i$ 为场景特征
- $\Delta_S^i$ 为场景变化特征，显式编码动态事件
- $Decoder$ 为 Transformer 解码器，以自回归方式迭代预测

**训练损失**（Eq. 2）：

$$\mathcal{L}_{traj} = \mathbb{E}[\| Traj - \hat{\epsilon}_\theta \|_2^2], \quad \mathcal{L}_{conf} = BCE(C_{GT} - C_{Pre})$$

- $\mathcal{L}_{traj}$：预测轨迹与真值轨迹的 L2 重建损失
- $\mathcal{L}_{conf}$：置信度损失，采用二元交叉熵。软目标置信度定义为 $C_{GT} = \exp(-\|Traj - \hat{\epsilon}_\theta\|_2)$，使模型学会在轨迹误差大时输出低置信度

### 3.4 层次化经验记忆模块

该模块是 Dyn-HSI 的“记忆”组件，存储带噪声的运动表示以实现上下文感知的运动启动（Section 3.4）。记忆库按三层递进组织：
1. **动作层**：存储不同动作类别的噪声运动
2. **细粒度动作变化层**：存储同一动作的不同变体
3. **场景上下文层**：存储不同场景条件下的动作执行方式

**存储相似度评分**（Eq. 3）：

$$\mathbf{S}_s = \alpha_s \cdot \mathbf{Sim}_{scene} + \beta_s \cdot \mathbf{Sim}_{joints} + \gamma_s \cdot \mathbf{Sim}_{text}$$

其中 $\mathbf{Sim}_{scene}$、$\mathbf{Sim}_{joints}$、$\mathbf{Sim}_{text}$ 分别为场景、关节运动和文本的多模态相似度，$\alpha_s$、$\beta_s$、$\gamma_s$ 为加权超参数。当相似度超过阈值时，当前运动被存入记忆库；检索时则根据相似度返回最匹配的噪声运动作为扩散模型的初始化，替代传统的高斯噪声初始化。

### 3.5 HSI 扩散模型与条件适配器

该模块是 Dyn-HSI 的“控制”组件，核心创新在于**条件适配器**（Condition Adapter）根据任务属性自适应调节各条件的重要性（Section 3.5）。

**条件权重学习**（Eq. 4）：

$$[\mathbf{R}_1, \mathbf{R}_2, \mathbf{R}_3, \mathbf{R}_4] = Softmax(MLP(T_f))$$

其中 $\mathbf{R}_1$ 至 $\mathbf{R}_4$ 分别为场景、轨迹、文本、目标四个条件的注意力权重，由文本特征 $T_f$ 通过 MLP 和 Softmax 生成。这一设计使模型能够根据任务描述自动判断哪些条件更关键——例如，“走到沙发旁坐下”可能更依赖场景和目标条件，而“绕开移动的椅子”则更依赖轨迹和场景变化条件。

**运动生成损失**（Eq. 5）：

$$\mathcal{L}_{motion} = \mathbb{E}[\| X_0 - \epsilon_\theta(X_t, T_f, G_f, S_f, Traj) \|_2^2]$$

其中 $X_0$ 为真实运动，$X_t$ 为加噪后的运动，$\epsilon_\theta$ 为去噪网络。

**总训练损失**（Eq. 6）：

$$\mathcal{L} = \mathcal{L}_{motion} + \lambda_t \mathcal{L}_{traj} + \lambda_c \mathcal{L}_{conf}$$

联合优化运动生成精度、轨迹规划和置信度估计，$\lambda_t$ 和 $\lambda_c$ 为平衡超参数。

### 3.6 推理流程

推理时，Dyn-HSI 按以下步骤运行（Section 3.2）：
1. **导航预测**：动态场景感知导航模块基于当前状态预测下一位置和置信度
2. **记忆检索**：层次化经验记忆根据当前上下文检索匹配的噪声运动作为初始化
3. **条件融合**：条件适配器根据文本特征计算各条件的权重
4. **运动生成**：扩散模型在加权条件的引导下生成运动片段
5. **自回归迭代**：使用生成片段的最后两帧作为下一片段的条件，重复上述过程直至到达目标位置

### 补充图表

![[assets/figures/papers/paper_list_l1700_Dynamic_Worlds_Dynamic_Humans_Generating_Virtual_Human_Scene_Interaction/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of Dynamic Scene-Aware Navigation*

## 实验与分析

### 1. 静态场景下的运动生成质量与轨迹精度

Dyn-HSI在静态基准LINGO上进行了全面评估，与**LINGO**（Jiang et al., SIGGRAPH Asia 2024）、**Trumans**（Jiang et al., CVPR 2024）、**AMDM**（Wang et al., CVPR 2024）、**HUMANISE**（Wang et al., NeurIPS 2022）和**SceneDiffuser**（Huang et al., CVPR 2023）等方法对比。核心结论如下：

- **运动质量（FID↓）**：Dyn-HSI达到0.092，较次优方法Trumans的约0.283降低67.45%，表明生成运动的分布与真实数据高度一致（Table 1）。
- **轨迹相似度（Traj. sim.↑）**：Dyn-HSI达到90.01%，在所有方法中最佳，验证了动态场景感知导航模块对路径规划的精准性（Table 1）。
- **目标误差（Goal. err.↓）**：Dyn-HSI较LINGO降低96.36%，说明虚拟人能够准确到达指定目标位置（Table 1, text）。
- **穿透值（Pene.Value↓）**：Dyn-HSI为26.01，最大穿透值较LINGO降低50.24%，证明即使在静态场景下，其动态感知机制也能有效避免人-场景穿透（Table 2, Section 4.3）。

![[assets/figures/papers/paper_list_l1700_Dynamic_Worlds_Dynamic_Humans_Generating_Virtual_Human_Scene_Interaction/figures/004_Table_1.jpg]]
*Table 1: Comparisons to SoTA methods on the LINGO [25] dataset. “↑” denotes that higher is better*

![[assets/figures/papers/paper_list_l1700_Dynamic_Worlds_Dynamic_Humans_Generating_Virtual_Human_Scene_Interaction/figures/005_Table_2.jpg]]
*Table 2: Static Scene Evaluation is conducted on the LINGO [25] dataset. Dynamic Scene Evaluation is conducted on the Dyn-LINGO. “↓” denotes that lower is better. “w/o” denotes “without” and indicates ablation variants. We report the best and the second-best results in Red cells and blue cells*

**因果归因**：上述优势源于条件适配器（Condition Adapter）对场景、轨迹、文本和目标条件的自适应加权（Section 3.5, Eq. 4），以及层次化经验记忆（Hierarchical Experience Memory）提供的上下文感知运动启动（Section 3.4），使扩散模型在去噪过程中获得更精准的条件引导。

### 2. 动态场景下的穿透避免与分布外泛化

为验证对动态场景的适应能力，论文构建了两个动态评估基准：Dyn-LINGO（基于LINGO场景手动添加动态变化）和Dyn-Trumans（基于Trumans场景的分布外动态环境）。

- **动态场景穿透（Dyn-LINGO, Pene.Value↓）**：Dyn-HSI为39.19，远低于其他方法（Table 2）。基线方法因将场景视为静态，在动态障碍物出现时产生严重穿透。
- **分布外泛化（Dyn-Trumans, Pene.Value变化）**：完整Dyn-HSI的穿透值仅比静态场景增加5.74%，而移除层次化经验记忆的消融版本恶化96.86%，最大穿透值增加2463（Table 3）。这表明记忆模块存储的多样化运动经验对未见场景的泛化至关重要。

![[assets/figures/papers/paper_list_l1700_Dynamic_Worlds_Dynamic_Humans_Generating_Virtual_Human_Scene_Interaction/figures/007_Table_3.jpg]]
*Table 3: Out-of-Distribution Dynamic Scene Evaluation is conducted on the Dyn-Trumans benchmark. “↓” denotes that lower is better. “w/o” denotes “without” and indicates ablation variants. We report the best and the second-best results in Red cells and blue cells*

**因果机制**：动态场景感知导航模块通过局部占用网格（local occupancy grid）持续检测场景变化，并利用Transformer解码器迭代预测下一步位置和置信度（Section 3.3, Eq. 1），使虚拟人能够实时调整轨迹。层次化经验记忆则从动作、动作变体和场景上下文三个层级检索相似经验，为扩散模型提供合理的运动先验，避免在陌生环境中产生随机性导致的穿透。

### 3. 消融实验：各模块的因果贡献

消融实验系统性地验证了三个核心组件的必要性（Table 2, Table 3, Section 4.5）：

- **移除动态场景感知导航（w/o Nav.）**：
  - 轨迹相似度下降12.41%（Table 1），表明导航模块对路径规划精度有决定性影响。
  - 静态场景穿透值增加12.88，动态场景穿透值增加9.40（Table 2），说明即使场景未变化，动态感知机制也能优化人-场景空间关系。
- **移除层次化经验记忆（w/o Mem.）**：
  - 分布外场景穿透值恶化96.86%（Table 3），是各消融中退化最严重的指标，证明记忆模块是泛化能力的核心支撑。
  - 最大穿透值增加2463，表明缺乏经验引导时模型在陌生场景中会产生灾难性穿透。
- **移除条件适配器（w/o Cond.）**：
  - FID增加0.178，MPJPE增加0.034（Section 4.5），说明固定权重无法适应不同任务对条件的差异化需求。
  - 在分布外数据上退化更为严重，验证了自适应加权对鲁棒性的贡献。

**证据强度**：上述消融结果均通过定量指标验证，置信度高。穿透值的剧烈变化（如96.86%的恶化）表明记忆模块的因果效应显著且不可替代。

### 4. 用户研究：感知质量验证

用户研究从四个维度评估生成结果的主观质量（Fig. 5）：

![[assets/figures/papers/paper_list_l1700_Dynamic_Worlds_Dynamic_Humans_Generating_Virtual_Human_Scene_Interaction/figures/008_Figure_5.jpg]]
*Figure 5: User study results. The higher score indicates better performance*

- **文本对齐分数（1-5）**：Dyn-HSI获得4.87，较LINGO的约3.42提升42.39%，表明生成的运动与文本描述高度一致。
- **运动质量、轨迹质量、人-场景交互质量**三个维度上，Dyn-HSI均显著优于所有基线方法。

**分析**：用户研究弥补了自动指标可能无法完全捕捉的感知质量（如运动自然度、交互合理性），与FID、穿透值等客观指标形成交叉验证，增强了结论的可信度。

### 5. 效率分析：速度与质量的权衡

Table 4报告了推理效率对比：

- Dyn-HSI的推理速度慢于部分基线方法，主要瓶颈来自动态场景感知导航的迭代预测过程（每步需重新计算局部占用网格和Transformer解码）。
- 移除导航模块的消融版本（w/o Nav.）速度接近**MotionDiffuse**，表明扩散模型本身的采样速度并非主要瓶颈。
- 质量指标（FID、穿透值）的显著提升表明，当前的速度代价换取了动态场景适应能力，但推理效率仍是实际部署的制约因素。

### 6. 失败模式与局限性

基于实验结果和论文自述，Dyn-HSI的主要失败模式包括：

- **高度复杂动态场景下的穿透**：动态场景为手工模拟，未能覆盖真实世界中的细微物体运动或拥挤场景。在连续快速变化的场景中，局部占用网格的更新频率可能不足，导致穿透或行为错误。
- **分布外场景的边缘案例**：尽管记忆模块大幅提升了泛化能力，但在与训练数据差异极大的场景中，检索到的运动先验可能不匹配，导致运动不自然或目标未达成。
- **推理速度瓶颈**：动态场景感知导航的迭代预测和扩散模型的逐步去噪共同导致推理速度不理想，限制了实时应用场景。
- **超参数敏感性**：条件适配器的权重学习依赖MLP结构，损失函数中的$\lambda_t$和$\lambda_c$、记忆相似度中的$\alpha_s$、$\beta_s$、$\gamma_s$等超参数需手动调节，可能在新任务上需要重新调优。

### 7. 实验公平性说明

- **训练数据一致性**：所有模型均在相同静态数据集（LINGO）上训练，Dyn-HSI通过架构设计实现动态泛化，而非依赖额外的动态训练数据。
- **评估基准公平性**：动态场景基准（Dyn-LINGO, Dyn-Trumans）使用相同的场景数据和变化条件评估所有方法，基线方法的失败源于其对静态场景的固有假设。
- **推理时间对比**：Dyn-HSI的额外时间开销主要来自导航模块的迭代预测，消融版本的速度对比表明这一开销未被不公平地隐藏于其他模块。

### 补充图表

![[assets/figures/papers/paper_list_l1700_Dynamic_Worlds_Dynamic_Humans_Generating_Virtual_Human_Scene_Interaction/figures/009_Figure_6.jpg]]
*Figure 6: Visual results compared with existing methods. The left side provides a detailed description of the dynamic conditions within the scene. The green box zooms in on the details captured by our approach, while the red boxes highlight errors made by other methods. Green arrows indicate the goal positions*

![[assets/figures/papers/paper_list_l1700_Dynamic_Worlds_Dynamic_Humans_Generating_Virtual_Human_Scene_Interaction/figures/010_Figure_7.jpg]]
*Figure 7: Qualitative examples from the ablation study on the Dynamic Scene-Aware Navigation. The bottom-left shows the top-down trajectory paths of both methods*

![[assets/figures/papers/paper_list_l1700_Dynamic_Worlds_Dynamic_Humans_Generating_Virtual_Human_Scene_Interaction/figures/011_Figure_8.jpg]]
*Figure 8: Qualitative examples from the ablation study on the Hierarchical Experience Memory*

![[assets/figures/papers/paper_list_l1700_Dynamic_Worlds_Dynamic_Humans_Generating_Virtual_Human_Scene_Interaction/figures/012_Table_4.jpg]]
*Table 4: Efficiency analysis compared with SoTA methods. “↑” denotes that higher is better. “↓” denotes that lower is better. “w/o” denotes “without” and indicates ablation variants. We report the best and the second-best results in Red cells and blue cells*

## 方法谱系与知识库定位

### 1. 核心瓶颈与因果机制

现有的人-场景交互（HSI）运动生成方法普遍将场景视为**静态刚体**，这构成了该领域的核心瓶颈。具体而言，**LINGO**（Jiang et al., SIGGRAPH Asia 2024）、**Trumans**（Jiang et al., CVPR 2024）等基于体素占用的方法，以及 **SceneDiffuser**（Huang et al., CVPR 2023）、**AMDM**（Wang et al., CVPR 2024）等基于可支付性地图或扩散模型的方法，均假设场景在交互过程中保持不变。当场景中出现动态事件（如移动障碍物、门开关）时，这一假设直接导致虚拟人穿透场景物体或交互目标失效。**HUMANISE**（Wang et al., NeurIPS 2022）虽引入语言条件，但同样未解决场景动态性。

Dyn-HSI 的因果杠杆在于**引入动态场景感知导航和层次化经验记忆**，使虚拟人能够实时感知场景变化，并检索过往经验以自适应调整运动。其核心洞察是：受世界模型启发的“视觉-记忆-控制”认知架构，通过持续感知、经验检索和自适应条件融合，能够生成高质量的动态人-场景交互运动。

### 2. 方法架构定位

Dyn-HSI 是一个**自回归运动扩散模型**，由三个关键模块构成：

| 模块 | 角色 | 与现有工作的关系 |
|------|------|-----------------|
| **动态场景感知导航** | 视觉模块：持续感知场景变化，预测下一步位置及置信度 | 替代了 LINGO/Trumans 的静态全局占用输入，引入逐步更新的局部占用网格和场景变化检测（Section 3.3, Fig. 3） |
| **层次化经验记忆** | 记忆模块：存储噪声运动数据，实现上下文感知的运动启动 | 替代了传统扩散模型的随机高斯噪声初始化，从动作、细粒度变化、场景上下文三个层级检索经验（Section 3.4） |
| **HSI 扩散模型 + 条件适配器** | 控制模块：生成交互运动，自适应调节多模态条件权重 | 替代了固定或拼接的条件权重，通过 MLP 从文本特征学习场景、轨迹、文本、目标的注意力权重（Section 3.5, Eq. 4） |

自回归生成循环将运动序列分段生成，使用前一段最后两帧作为条件，与 **MotionDiffuse** 等非自回归方法形成对比。

### 3. 关键方法槽位变更

Dyn-HSI 在以下四个关键槽位上对现有范式进行了根本性修改：

- **场景处理**：从“静态全局场景占用作为固定输入”变为“逐步更新的动态局部占用 + 场景变化检测”（证据锚点：Section 3.3, Fig. 3）
- **条件融合**：从“固定或拼接的条件权重”变为“基于任务属性的自适应条件权重”（证据锚点：Section 3.5, Eq. 4）
- **初始化**：从“随机高斯噪声”变为“来自层次化经验记忆的上下文感知运动启动”（证据锚点：Section 3.4）
- **轨迹规划**：从“预定义路径或无置信度的 A* 算法”变为“基于 Transformer 的迭代预测 + 置信度评分”（证据锚点：Section 3.3, Eq. 1-2）

### 4. 适用边界与局限

**适用边界**：
- 输入为文本描述 + 动态 3D 场景，输出为虚拟人运动序列
- 训练完全依赖静态数据集（LINGO），但架构具备向动态场景的泛化能力
- 当前动态场景为手工模拟构建（Dyn-LINGO, Dyn-Trumans），未完全代表真实世界的复杂性

**已知局限**（需手动验证具体数值）：
1. **推理速度瓶颈**：主要来自动态场景感知导航的迭代预测和扩散模型的慢速采样。消融版本（无导航）速度接近 MotionDiffuse，表明导航模块是主要开销来源（Table 4）
2. **动态场景覆盖不足**：手工模拟的动态场景无法捕捉细微物体运动、拥挤场景等复杂情况，在高度复杂或连续变化的环境中可能出现穿透或行为错误
3. **训练数据限制**：完全依赖静态数据集训练，缺乏大规模动态交互数据，可能导致极限场景下的性能下降
4. **超参数敏感性**：条件适配器等组件的超参数（如 $\lambda_t$, $\lambda_c$, $\alpha_s$, $\beta_s$, $\gamma_s$）需要手动调参，对任务变化可能不够鲁棒

### 5. 开放问题

1. **推理加速**：如何在不牺牲动态感知能力的前提下减少导航模块的开销？是否可能通过蒸馏或预测性缓存加速迭代预测？
2. **复杂动态扩展**：框架能否扩展到多移动物体、人群交互或非刚性物体变化等更复杂的真实世界动态？
3. **记忆自适应学习**：层次化经验记忆的存储策略（相似度阈值 $\tau_l$、容量 $k$）和超参数能否根据任务自动学习调整，而非手工设定？
4. **动态数据构建**：能否通过自监督或合成数据扩增构建大规模动态人-场景交互训练集，以弥补当前仅依赖静态数据训练的不足？
5. **记忆更新策略**：当新任务或场景频繁变化时，记忆更新与检索如何平衡效率与多样性，避免生成模式坍塌？

## 原文 PDF

![[paperPDFs/arxiv_2026/Dynamic_Worlds_Dynamic_Humans_Generating_Virtual_Human_Scene_Interaction_Motion_in_Dynamic_Scenes.pdf]]
