---
title: "KinMo: Kinematic-aware Human Motion Understanding and Generation"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/KinMo_Kinematic_aware_Human_Motion_Understanding_and_Generation.pdf
project_link: https://andypinxinliu.github.io/KinMo
code_link: null
aliases:
- KinMo
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将人体运动按运动学树分解为六个组件（躯干、颈部、左臂、右臂、左腿、右腿），并构建由全局动作、组级描述、交互描述组成的层次化文本表示，通过运动推理器生成细粒度描述，再利用层次化文本‑运动对齐与粗‑细生成过程进行整合。
primary_logic: 通过从粗到精地融入多级运动学描述，可以显著缩小文本‑运动模态差距，提升检索和生成精度，并首次实现针对局部身体部位的细粒度编辑与轨迹控制。
claims:
- 在 HumanML3D 全部测试集上，KinMo 的文本‑运动检索 R@1 达到 9.05，远超 TMR 的 5.68。
- 在生成任务中，KinMo (HTMA) 将 FID 降至 0.039，优于 MoMask 的 0.045。
- 增加组级和交互级描述后，文本‑运动检索 R@1 从 3.67 提升至 7.58（加组级）和 9.05（加交互级）。
- 层次化文本‑运动对齐（完整层次）将 FID 降低到 0.044，明显优于平面基线。
---

# KinMo: Kinematic-aware Human Motion Understanding and Generation

> [!tip] 核心洞察
> 通过从粗到精地融入多级运动学描述，可以显著缩小文本‑运动模态差距，提升检索和生成精度，并首次实现针对局部身体部位的细粒度编辑与轨迹控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | KinMo：面向运动学的人体运动理解与生成 |
| 英文题名 | KinMo: Kinematic-aware Human Motion Understanding and Generation |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](https://andypinxinliu.github.io/KinMo) · [paper](https://arxiv.org/abs/2411.15472) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | KinMo |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D (all test set) 上，R@1 (Text-motion retrieval) 9.05 (KinMo RoBERTa) vs 5.68 (TMR) (+3.37)。
> - HumanML3D (dissimilar subset) 上，R@1 (Text-motion retrieval) 57.73 (KinMo RoBERTa) vs 47.00 (TMR) (+10.73)。
> - HumanML3D (small batches) 上，R@1 (Text-motion retrieval) 72.88 (KinMo RoBERTa) vs 67.16 (TMR) (+5.72)。

## 概要

**核心问题**：现有文本-运动学习方法仅依赖全局动作描述，导致文本与运动模态之间存在显著模糊性——一段“挥手”的文本可能对应数十种运动姿态，而模型无法捕捉局部肢体运动与细粒度运动学动态，从根本上限制了理解与生成的能力。

**核心方法**：KinMo 提出一种运动学感知的层次化框架。它将人体运动按运动学树分解为六个组件（躯干、颈部、左臂、右臂、左腿、右腿），构建由全局动作、组级描述、交互描述组成的三级文本表示，并通过运动推理器自动生成细粒度描述，再利用层次化文本-运动对齐与粗-细生成过程进行整合。

**核心洞察**：通过从粗到精地融入多级运动学描述，可以显著缩小文本-运动模态差距——组级描述解决“哪个部位在动”的歧义，交互级描述解决“部位之间如何配合”的歧义，从而系统性地提升检索精度和生成质量，并首次实现对局部身体部位的细粒度编辑与轨迹控制。

**主要结果**：
- 在 HumanML3D 全部测试集上，KinMo 的文本-运动检索 R@1 达到 **9.05**，远超强基线 TMR 的 5.68（Table 1）。
- 在生成任务中，KinMo 将 FID 降至 **0.039**，优于 MoMask 的 0.045（Table 2）。
- 消融实验表明，增加组级描述使 R@1 从 3.67 提升至 7.58，再增加交互级描述进一步提升至 9.05（Table 4）；层次化文本-运动对齐将生成 FID 从 0.051 降至 0.044（Table 5）。
- 在轨迹控制任务中，KinMo 对骨盆轨迹的 FID 为 **0.103**，远低于 MDM 的 0.544（Table 11）。

**方法定位**：KinMo 属于文本-运动联合学习的方法谱系，其核心贡献在于将运动学先验结构化为可学习的层次文本表示。与仅使用全局文本的 **TMR**、基于扩散的 **MDM**、基于掩码的 **MoMask** 等基线相比，KinMo 在不改变骨干生成器（MoMask）的前提下，通过注入运动学感知的层次语义实现了显著的性能提升。



### 文本驱动人体运动理解的模态鸿沟

从自然语言描述中理解和生成三维人体运动，是构建具身智能与数字人交互系统的核心能力。近年来，基于文本-运动联合嵌入空间的对齐方法以及扩散/掩码生成模型，在全局动作的检索与生成上取得了显著进展。然而，现有范式普遍依赖单一的全局动作描述来桥接文本与运动两种模态，这构成了一个根本性的瓶颈：**全局描述与细粒度肢体运动之间存在天然的语义模糊性**。

具体而言，一个全局动作描述——“一个人向前走并挥动右手”——无法精确刻画躯干的朝向、左臂的摆动幅度、双腿的交替节奏，以及挥手动作与步态之间的时序协调关系。当前的文本-运动学习方法（如 **TEMOS**、**TMR**、**MoMask**）仅从这类全局描述中学习跨模态映射，导致模型无法捕捉局部身体部位的运动学动态，从而在以下两个层面暴露出能力缺口：

1.  **检索的语义粗糙性**：当多个运动序列共享相似的全局语义（如“行走”），但在肢体细节上存在显著差异时，基于全局嵌入的检索难以区分这些细粒度变化，召回精度受限。
2.  **生成的不可控性**：生成模型缺乏对局部肢体运动的显式建模能力，无法根据文本指令精确编辑特定身体部位的动作，更无法实现对单个关节（如骨盆）的轨迹级控制。

### 核心动机与解决思路

本文的核心动机在于**通过引入运动学先验来缩小文本与运动模态之间的细粒度语义鸿沟**。我们观察到，人体运动本质上遵循运动学树的层次结构——躯干、颈部、四肢等组件既具有独立的运动模式，又通过关节连接产生协同交互。然而，这一结构化的先验知识在现有的文本-运动对齐与生成框架中几乎未被利用。

为此，我们提出 **KinMo**，其核心思想是**将人体运动按运动学树分解为六个基本组件（躯干、颈部、左臂、右臂、左腿、右腿），并构建与之对应的层次化文本表示**。这一表示包含三个粒度级别：全局动作描述、组级肢体描述，以及组间交互描述。通过从粗到精地融入多级运动学语义，KinMo 旨在实现三个关键突破：

-   **细粒度运动理解**：使模型能够区分“行走时大幅度摆臂”与“行走时手臂紧贴身侧”等局部差异，从而显著提升文本-运动检索的精度。
-   **可控运动生成**：赋予生成模型对特定身体部位进行文本驱动编辑的能力，并首次实现对单关节轨迹的显式控制。
-   **模态对齐的因果性改善**：通过层次化文本编码与粗-细生成过程，使文本条件信号与运动生成过程在多个语义粒度上对齐，从根本上缓解全局描述带来的模糊性。

简言之，KinMo 的核心洞察在于：**将运动学结构显式地注入文本-运动学习框架，是突破当前全局描述瓶颈、实现细粒度运动理解与生成的关键路径**。



## 核心方法与创新机理

KinMo 的核心创新在于将人体运动从传统的全局关节表示重新组织为**面向运动学组（Kinematic Group）的层次化表示**，并通过**多级文本描述**与**层次化跨模态对齐**来系统性地缩小文本-运动模态差距。这一设计直接回应了现有方法仅依赖全局动作描述所导致的模糊性瓶颈——全局文本无法捕捉局部肢体的细粒度运动学动态，从而限制了理解与生成的精度。

### 从全局运动到运动学组表示

传统方法（如 **TEMOS**、**TMR**、**MoMask**）将人体运动视为所有关节位置、旋转和速度的扁平向量，文本与运动之间的对齐发生在全局嵌入层面。KinMo 改变了这一范式：它将人体运动按运动学树分解为六个基本组件——**躯干（Torso）、颈部（Neck）、左臂（Left Arm）、右臂（Right Arm）、左腿（Left Leg）、右腿（Right Leg）**——并为每个组件定义了三个层次的运动表示：

- **组位置** $ \mathbf{P}_g(t) = \frac{1}{|J_g|} \sum_{j \in J_g} \mathbf{p}_j(t) $：组内所有关节的平均位置；
- **组角度与组速度** $ \Theta_g(t) = \{ \mathbf{r}_j(t) \mid j \in J_g \}, \quad \mathbf{V}_g(t) = \frac{1}{|J_g|} \sum_{j \in J_g} \mathbf{v}_j(t) $：组内关节的旋转集合与平均速度；
- **组间交互表示**：两组之间的相对位置 $ \Delta \mathbf{P}_{g,h} $、连接关节角度 $ \Delta \boldsymbol{\Theta}_{g,h} $ 和相对速度 $ \Delta \mathbf{V}_{g,h} $。

该表示是现有表示的线性变换，可无损还原，因此兼容现有运动生成与检索架构。与 **ParCo** 将身体简单分为上下半身的两部分分解不同，KinMo 的六组运动学分解更精细地对应了人体的自然运动学结构，消融实验（Table 3）证实 6 组分解在生成对齐度上显著优于 2 组分解。

### 从单一全局文本到层次化运动学描述

现有数据集的文本标注仅包含全局动作描述 $ T_c $（如“一个人向前走并挥手”），无法为局部肢体运动提供监督。KinMo 构建了一套自动标注管线来生成**层次化文本**：

1. **关键帧提取与位姿描述**：利用 **PoseScript** 对运动序列的关键帧生成逐帧位姿文本；
2. **LLM 自动标注**：通过两阶段提示策略，将关键帧位姿描述输入 GPT-4o/4o-mini，生成**组级描述** $ T_g $（描述每个运动学组的行为）和**交互级描述** $ T_i $（描述组间的协调关系，如“左手与右腿的交替摆动”）；
3. **运动推理器（Motion Reasoner）**：微调 LLaMA-3，使其在推理时仅根据全局动作描述 $ T_c $ 自动推断并生成 $ T_g $ 和 $ T_i $，从而在测试时无需额外的细粒度文本标注。

这一文本层次化策略是因果旋钮的核心——消融实验（Table 4）表明，在全局描述基础上增加组级描述，文本-运动检索 R@1 从 3.67 跃升至 7.58；再增加交互级描述，进一步提升至 9.05。

### 从平面编码到层次化文本-运动对齐（HTMA）

传统方法使用单一 Transformer 编码器直接编码全部文本，忽略了不同粒度描述之间的语义依赖关系。KinMo 提出了**层次化文本-运动对齐（HTMA）**，其核心是一个带有跨注意力机制的层次化编码器：

- 首先编码全局动作文本：$ \mathbf{h}_{\mathbf{c}} = E_{c} \big( \mathrm{emb}(T_{c}) \big) $；
- 然后以全局编码为条件，通过跨注意力编码组级文本：$ \mathbf{h_{g}} = E_{g} \bigl( \mathbf{CrossAttn} ( \mathbf{emb}(T_{g}), \mathbf{h_{c}} ) \bigr) $；
- 交互级文本同理，以组级编码为条件进行编码。

每一层级的文本嵌入与对应的运动嵌入通过 InfoNCE 对比损失 $ \mathcal{L}_{\mathrm{NCE}} $ 进行对齐，形成从粗到精的语义对齐层次。消融实验（Table 5）证实，完整的层次化对齐将生成 FID 从 0.051 降至 0.044，且全局→组→交互的跨注意力顺序在检索任务中取得了最佳的 R@1（9.05，Table 9）。

### 从一次性生成到粗-细三步生成

**MoMask** 等骨干生成器一次性生成所有运动 tokens。KinMo 将生成过程重构为**粗-细三步**：先生成初始 tokens（条件为全局嵌入 $ \mu_c $），再基于组级嵌入 $ \mu_g $ 生成中间 tokens，最后基于交互级嵌入 $ \mu_i $ 生成最终 tokens。生成器权重共享，但每一步的条件信号来自 HTMA 的不同层次。这一设计不仅提升了生成质量，还显著加快了训练收敛速度（Figure 10）。

### 首次实现局部身体部位的细粒度编辑与轨迹控制

由于 KinMo 的运动表示和文本描述均以运动学组为粒度，它首次使模型能够针对特定身体部位进行**文本驱动的运动编辑**（如“将左臂改为上举”）和**关节轨迹控制**（如指定骨盆的运动路径）。轨迹控制通过 ControlNet 架构实现，CNN 空间编码器处理目标关节位置信息，复制生成器将其注入生成过程。在骨盆轨迹控制任务上，KinMo 将 FID 从 MDM 的 0.544 降至 0.103（Table 11），实现了数量级的提升。



KinMo 的整体框架围绕一个核心思想构建：**将人体运动按运动学树分解为六个独立组件，并构建与之对应的层次化文本描述，通过从粗到精的多级对齐与生成过程，显著缩小文本与运动之间的模态差距**。该框架由四个关键模块串联而成，形成一条从运动表示、数据标注、文本‑运动对齐到条件生成与控制的完整流水线。

### 运动学组表示

框架的输入是原始的人体关节点运动数据。KinMo 不再直接使用基于关节点位置、旋转和速度的原始表示，而是将人体关节按运动学树重新组织为六个基本组（Figure 2 左侧）：

![[assets/figures/papers/paper_list_l1890_KinMo_Kinematic_aware_Human_Motion_Understanding_and_Generation/figures/002_Figure_2.jpg]]
*Figure 2: KinMo Framework. Left: We extract pose descriptions of the keyframes and feed them into an LLM to produce group- and interaction-level descriptions, which generate KinMo dataset together with original motion sequences and global action texts. Right: We apply encoders with the same architecture (brown) to process the features of global action, group-level descriptions, and interaction-level descriptions extracted from a pretrained model (blue: emb). The cross-attention layer (purple) is employed to combine embeddings of different levels to enable hierarchical representation learning, with contrastive learning at each level for modality alignment*

$$
G = \{\text{Torso}, \text{Neck}, \text{Left Arm}, \text{Right Arm}, \text{Left Leg}, \text{Right Leg}\}
$$

对每个运动学组 $g$，提取三类特征（Sec. 3.1）：

- **组位置**：组内所有关节的平均位置 $\mathbf{P}_g(t) = \frac{1}{|J_g|} \sum_{j \in J_g} \mathbf{p}_j(t)$
- **组角度**：组内各关节的旋转集合 $\Theta_g(t) = \{ \mathbf{r}_j(t) \mid j \in J_g \}$
- **组速度**：组内所有关节的平均速度 $\mathbf{V}_g(t) = \frac{1}{|J_g|} \sum_{j \in J_g} \mathbf{v}_j(t)$

此外，还显式建模**组间交互关系**，包括两组之间的相对位置、连接关节角度和相对速度（Eq. 3）。这一运动学组表示是现有表示（如 HumanML3D 原始特征）的线性变换，可以无损地正向和反向转换，保证了与现有方法的兼容性。

### 层次化文本标注流水线

与运动学组表示相对应，KinMo 构建了一个三层级文本描述体系（Figure 2 左侧）：

1. **全局动作描述** $T_c$：原始 HumanML3D 数据集中的整体动作文本。
2. **组级描述** $T_g$：针对六个运动学组的局部肢体运动描述。
3. **交互级描述** $T_i$：描述组间协调关系的文本。

为自动生成后两级描述，KinMo 设计了一个**两阶段 LLM 标注流水线**（Sec. 3.2）：首先利用 PoseScript 提取关键帧的位姿描述，然后将这些位姿描述与全局动作文本一起输入 GPT-4o/4o-mini，通过精心设计的提示模板（Table 13）生成高质量的组级和交互级运动文本。标注质量经过人工评估验证，Bad Response Rate 作为质量控制指标（Table 7）。

![[assets/figures/papers/paper_list_l1890_KinMo_Kinematic_aware_Human_Motion_Understanding_and_Generation/figures/014_Table_7.jpg]]
*Table 7: Evaluation Results of KinMo detailed descriptions. Bad Response Rate (BRR) is assessed by BRR = items with score\<5 total items*

### 层次化文本‑运动对齐（HTMA）

框架的核心是层次化文本‑运动对齐模块（Figure 2 右侧）。该模块采用基于 Transformer 的变分编码器架构，通过**跨注意力机制**逐步融入不同层级的语义信息（Sec. 3.3）：

1. 首先编码全局动作描述：$\mathbf{h}_{\mathbf{c}} = E_{c} \big( \mathrm{emb}(T_{c}) \big)$
2. 以全局编码为条件，通过跨注意力编码组级描述：$\mathbf{h_{g}} = E_{g} \bigl( \mathbf{CrossAttn} ( \mathbf{emb}(T_{g}), \mathbf{h_{c}} ) \bigr)$
3. 类似地，以组级编码为条件编码交互级描述，得到 $\mathbf{h_i}$

运动侧采用镜像架构，同样按全局→组级→交互级的顺序编码。在每一层级，文本和运动嵌入通过**InfoNCE 对比损失**进行对齐（Eq. 7），同时结合 KL 散度损失和运动重建损失构成整体训练目标。这种层次化对齐策略使得模型能够捕捉从粗粒度动作到细粒度肢体运动的完整语义。

### 运动推理器与粗‑细生成

在推理阶段，用户通常只提供全局动作描述。KinMo 引入一个**运动推理器**——基于 LLaMA-3 微调的语言模型——根据全局动作描述自动推断并生成组级和交互级描述（Figure 3 右侧，Sec. 4）。推理器通过下一 token 预测损失训练（Eq. 8），使得生成过程无需人工提供细粒度描述。

![[assets/figures/papers/paper_list_l1890_KinMo_Kinematic_aware_Human_Motion_Understanding_and_Generation/figures/003_Figure_3.jpg]]
*Figure 3: Motion Retrieval and Generation. Left: Overview of Text-to-Motion Retrieval, where we compute the similarity matrix defined between text and motion embeddings. Here, we present a batch of three samples with an example. To retrieve the most similar motion to the 2nd text*

生成过程采用**粗‑细三步策略**（Sec. 4.2）：以扩展的 MoMask 作为骨干生成器，首先以全局文本嵌入 $\mu_c$ 为条件生成初始运动 tokens；然后将这些 tokens 重新输入生成器，以组级嵌入 $\mu_g$ 为条件生成中间 tokens；最后以交互级嵌入 $\mu_i$ 为条件生成最终运动 tokens。生成器权重共享，三个层级使用相同的 logit 分类损失函数进行训练。

### 轨迹控制与编辑扩展

在基础生成框架之上，KinMo 通过**ControlNet 架构**实现了对特定关节的轨迹控制（Figure 9，Sec. 5.4）。该模块使用 CNN 空间编码器处理目标关节的轨迹位置信息，将其作为条件输入到可训练的控制生成器网络中，通过全局绝对位置损失（Eq. 11）进行优化，实现了对局部身体部位（如骨盆）运动轨迹的精确引导。同时，通过组合全局、组级和交互级的控制信号，KinMo 首次支持针对特定身体部位的细粒度运动编辑（Table 10）。

### 数据流总览

整个框架的数据流可以概括为：**原始关节点运动 → 运动学组表示** 与 **全局动作文本 → 运动推理器 → 层次化文本描述** 两条支线，在 **HTMA 编码器** 中通过层次化跨注意力对齐，最终汇入 **掩码运动生成器** 完成粗‑细生成，并可选择性地接入 **ControlNet** 实现轨迹控制或局部编辑。这一设计使得 KinMo 在统一的框架下同时支持文本‑运动检索、运动生成、局部编辑和轨迹控制四项任务。



KinMo 的核心由三个层次化模块构成：运动学组表示、层次化文本‑运动对齐（HTMA）以及粗‑细生成过程。以下按管线顺序梳理关键公式与变量含义。

### 运动学组表示

原始人体运动被按运动学树分解为六个组件：躯干（Torso）、颈部（Neck）、左臂（Left Arm）、右臂（Right Arm）、左腿（Left Leg）、右腿（Right Leg）。对每个组 $g$ 定义三种特征：

**组位置**（Group Position）为组内所有关节坐标的均值：

$$\mathbf{P}_g(t) = \frac{1}{|J_g|} \sum_{j \in J_g} \mathbf{p}_j(t)$$

其中 $J_g$ 表示组 $g$ 包含的关节集合，$\mathbf{p}_j(t)$ 为关节 $j$ 在时刻 $t$ 的三维位置。

**肢段角度与组速度**（Limb Angles and Group Velocity）同时捕捉局部旋转与整体运动快慢：

$$\Theta_g(t) = \{ \mathbf{r}_j(t) \mid j \in J_g \}, \quad \mathbf{V}_g(t) = \frac{1}{|J_g|} \sum_{j \in J_g} \mathbf{v}_j(t)$$

$\mathbf{r}_j(t)$ 为关节 $j$ 的旋转表示，$\mathbf{v}_j(t)$ 为其速度。

**组间交互表示**（Group‑Interaction Representations）建模两组 $g$ 与 $h$ 之间的相对位置、连接关节角度及相对速度：

$$\begin{bmatrix} \Delta \mathbf{P}_{g,h}(t) \\ \Delta \boldsymbol{\Theta}_{g,h}(t) \\ \Delta \mathbf{V}_{g,h}(t) \end{bmatrix} = \begin{bmatrix} \mathbf{P}_h(t) - \mathbf{P}_g(t) \\ \boldsymbol{\Theta}_{h \cap g}(t) \\ \mathbf{V}_h(t) - \mathbf{V}_g(t); \mathbf{v}_{h \cap g}(t) \end{bmatrix}$$

该表示是已有运动表示的线性变换，可无损转换回原始关节表示，因此能无缝嵌入现有文本‑运动对齐框架。

### 层次化文本‑运动对齐（HTMA）

HTMA 编码器以层次化跨注意力逐步融合多级文本语义。给定全局动作描述 $T_c$、组级描述 $T_g$ 和交互级描述 $T_i$，编码过程为：

**全局动作编码**：

$$\mathbf{h}_{\mathbf{c}} = E_{c} \big( \mathrm{emb}(T_{c}) \big)$$

$E_c$ 为 Transformer 编码器，$\mathrm{emb}$ 为预训练文本嵌入层（如 RoBERTa）。

**组级编码**以全局编码为条件，通过跨注意力注入全局语义：

$$\mathbf{h_{g}} = E_{g} \bigl( \mathbf{CrossAttn} ( \mathbf{emb}(T_{g}), \mathbf{h_{c}} ) \bigr)$$

交互级编码同理，以组级编码为条件进一步融合。运动侧编码器采用相同架构，形成对称的层次化潜在空间。

**对比对齐损失**使用 InfoNCE 拉近匹配的文本‑运动嵌入对：

$$\mathcal{L}_{\mathrm{NCE}} = \frac{-1}{2N} \sum_{T} \sum_{i} \left( \log \frac{\exp S_{ii} / \tau}{\sum_{j} \exp S_{ij} / \tau} + \log \frac{\exp S_{ii} / \tau}{\sum_{j} \exp S_{ji} / \tau} \right)$$

其中 $S$ 为文本与运动嵌入的余弦相似度矩阵，$\tau$ 为温度系数。总损失还包含 KL 散度、跨模态嵌入相似度及运动重建损失的加权和（继承自 TMR）。

### 运动推理器与粗‑细生成

**运动推理器**（Motion Reasoner）基于微调的 LLaMA‑3，以全局动作 $T_c$ 为条件自回归生成组级和交互级描述，训练损失为标准下一 token 预测交叉熵：

$$\mathcal{L}_{reasoner} = - \sum_{i = 1}^{N} y_i \log (\hat{y}_i | T_c, T_{< i})$$

**粗‑细生成过程**以扩展的 MoMask 为骨干，分三步逐步注入层次文本条件：

1. 以全局嵌入 $\mu_c$ 为条件生成初始运动 tokens；
2. 将初始 tokens 重新输入生成器，以组级嵌入 $\mu_g$ 为条件生成中间 tokens；
3. 以交互级嵌入 $\mu_i$ 为条件生成最终 tokens。

生成器在三阶段中共享权重，均使用相同的 logit 分类损失重建运动 tokens。消融实验表明，该粗‑细过程显著加速训练收敛并提升生成质量。

### 轨迹控制模块

轨迹控制采用 ControlNet 架构：以 CNN 空间编码器处理目标关节的绝对位置轨迹，将其作为条件注入可训练复制生成器。训练损失为掩码全局绝对位置误差：

$$\mathcal{L}_{\mathrm{control}} = \mathbb{E}\left[ \frac{\sum_i \sum_j m_{ij} || R(\hat{\mathbf{x}}_0)_{ij} - R(\mathbf{x}_0)_{ij} ||_2^2}{\sum_i \sum_j m_{ij}} \right]$$

其中 $m_{ij}$ 为关节掩码，$R(\cdot)$ 提取全局绝对位置，$\hat{\mathbf{x}}_0$ 与 $\mathbf{x}_0$ 分别为预测和真实运动。该模块首次实现了对局部身体部位（如骨盆）的细粒度轨迹控制。

### 补充图表

![[assets/figures/papers/paper_list_l1890_KinMo_Kinematic_aware_Human_Motion_Understanding_and_Generation/figures/017_Figure_9.jpg]]
*Figure 9: Motion Trajectory Control. We adopt a ControlNet architecture to condition the generator with the provided trajectory of the target joint during the generation. We utilize a CNN encoder to process the spatial position information and feed it as the input condition into the control generator network*



## 实验与关键发现

### 核心实验设置

KinMo 的实验围绕文本‑运动检索、文本‑运动生成、运动编辑和轨迹控制四个任务展开，所有实验均基于 HumanML3D 数据集的标准训练/验证/测试划分。检索评估沿用 TMR 的设置，采用四种难度递减的协议：(a) All——完整测试集；(b) All with threshold——相似度阈值 0.8 过滤；(c) Dissimilar subset——100 对 sBERT 嵌入差异显著的样本；(d) Small batches——小批量检索。生成评估采用 R-Precision (Top-1/2/3)、FID、MM-Dist、Diversity 和 MModality 等标准指标，每个指标重复评估 20 次并报告 95% 置信区间。用户研究采用单盲设计，评估者在不知晓方法来源的情况下对 80 段视频的 Realness、T2M Alignment 和 Overall Impression 打分。

### 文本‑运动检索：运动学层次描述显著缩小模态差距

Table 1 展示了 HumanML3D 上的文本‑运动检索结果。KinMo (RoBERTa) 在全部测试集上取得 R@1 = 9.05，远超强基线 TMR 的 5.68（提升 +3.37）。在更具挑战性的 Dissimilar subset 上，KinMo 的 R@1 达到 57.73，较 TMR 的 47.00 提升 +10.73；在 Small batches 协议下，R@1 达到 72.88，较 TMR 的 67.16 提升 +5.72。这一结果验证了核心因果机制：**运动学层次描述通过从粗到精地注入组级和交互级语义，有效缩小了文本‑运动模态间的模糊性**。

![[assets/figures/papers/paper_list_l1890_KinMo_Kinematic_aware_Human_Motion_Understanding_and_Generation/figures/005_Table_1.jpg]]
*Table 1: Text-to-motion retrieval benchmark on HumanML3D. Evaluation protocols with decreasing difficulty from (a) to (d)*

消融实验（Table 4）进一步揭示了各层次描述的贡献：仅使用全局动作描述时，R@1 仅为 3.67；增加组级描述后提升至 7.58；再增加交互级描述后进一步提升至 9.05。这一递进增益表明，局部肢体运动学和组间交互关系的信息对于消除文本‑运动匹配中的歧义至关重要。

![[assets/figures/papers/paper_list_l1890_KinMo_Kinematic_aware_Human_Motion_Understanding_and_Generation/figures/010_Table_4.jpg]]
*Table 4: Effect of Additional Descriptions for Text-Motion Alignment. Different strategies for incorporating descriptions generated by Motion Reasoner on motion- and text-retrieval tasks*

### 文本‑运动生成：层次对齐与粗‑细生成协同提升质量

Table 2 展示了生成任务的对比结果。KinMo (HTMA) 在 FID 上达到 0.039，优于 MoMask 的 0.045（降低 -0.006）；R-Precision Top-1 达到 0.532，优于 MoMask 的 0.521（提升 +0.011）。在用户研究（Figure 5）中，KinMo 在 Realness、T2M Alignment 和 Overall Impression 三个维度上均优于对比方法。

![[assets/figures/papers/paper_list_l1890_KinMo_Kinematic_aware_Human_Motion_Understanding_and_Generation/figures/006_Table_2.jpg]]
*Table 2: Comparison of text-to-motion generation on HumanML3D. For each metric, we repeat the evaluation 20 times and report the average with 95% confidence interval. The right arrow (→) indicates that the closer the result is to real motion, the better*

![[assets/figures/papers/paper_list_l1890_KinMo_Kinematic_aware_Human_Motion_Understanding_and_Generation/figures/007_Figure_5.jpg]]
*Figure 5: User Study. We generate 80 videos for each method to assess Realness, T2M Alignment, and Overall Impression*

消融实验揭示了两个关键设计的作用：
- **层次化文本‑运动对齐（HTMA）**：Table 5 显示，完整的层次跨注意力对齐将 FID 从平面基线的 0.051 降至 0.044。此外，Figure 10 表明 HTMA 可以显著加速训练收敛，同时获得更好的生成结果。
- **粗‑细生成过程**：Figure 10 显示，先生成初始 tokens（基于 μ_c），再逐步基于 μ_g 和 μ_i 精炼的粗‑细流程，相比一次性生成能够持续提升生成质量。

![[assets/figures/papers/paper_list_l1890_KinMo_Kinematic_aware_Human_Motion_Understanding_and_Generation/figures/011_Table_5.jpg]]
*Table 5: Effect of Hierarchical Text-Motion Alignment. Comparisons are conducted for Motion Generator with RQ base layer*

![[assets/figures/papers/paper_list_l1890_KinMo_Kinematic_aware_Human_Motion_Understanding_and_Generation/figures/018_Figure_10.jpg]]
*Figure 10: Ablation for Motion Generation Process. Our coarse-to-fine procedure helps to improve the motion generation quality. Hierarchical Text-Motion Alignment can significantly speed up the training process with better generation results and text-motion alignment*

Table 3 的公平对比进一步表明，将运动分解为 6 个运动学组（而非 ParCo 的 2 个上下半身分解）可以进一步提升生成对齐度（FID 0.050 vs. 其他分解策略）。

![[assets/figures/papers/paper_list_l1890_KinMo_Kinematic_aware_Human_Motion_Understanding_and_Generation/figures/008_Table_3.jpg]]
*Table 3: Comparisons with other methods. Motion Generation with CLIP-embed additional texts as conditions of MoMask*

### 运动编辑与轨迹控制：首次实现局部身体部位的细粒度操控

KinMo 首次实现了针对局部身体部位的细粒度编辑与轨迹控制。Table 10 展示了运动编辑结果：在联合控制全局动作（G）、组级（J）和交互级（I）描述的条件下，KinMo 的编辑结果 FID 达到 0.086，与未编辑的 MoMask 基线（0.080）接近，表明编辑操作未显著损害运动质量。

Table 11 展示了轨迹控制结果：在仅控制骨盆轨迹（无测试时优化）的条件下，KinMo 的 FID 达到 0.103，远优于 MDM 的 0.544（降低 -0.441），验证了 ControlNet 架构在关节轨迹控制上的有效性。

### 失败模式与局限性

尽管 KinMo 在整体上表现优异，但仍存在以下失败模式：
- **短时过渡遗漏**：当文本描述包含大量短时过渡时，方法偶尔会遗漏某些步骤（Figure 12），这可能是由于运动推理器在生成细粒度描述时未能完整捕捉所有瞬时变化。
- **低质量描述退化**：运动推理器生成不准确的组级或交互级描述时，会降低生成性能。Table 7 的标注评估显示了描述质量的分布，低分描述的存在构成了性能的潜在瓶颈。
- **刚性体假设局限**：在部分身体部位内部发生显著非刚性变形（如肘部大幅屈伸）时，刚性体假设可能失效，影响重建精度。
- **编辑/控制架构灵活性**：编辑和轨迹控制依赖于冻结或复制的骨干网络，可能局限了端到端学习的灵活性。

### 补充图表

![[assets/figures/papers/paper_list_l1890_KinMo_Kinematic_aware_Human_Motion_Understanding_and_Generation/figures/019_Table_9.jpg]]
*Table 9: Cross-Attention Order of Descriptions for Text-Motion Retrieval*



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

现有文本‑运动学习方法（如 TEMOS、TMR、MDM、MoMask）的核心瓶颈在于**仅依赖全局动作描述**进行跨模态学习。这一范式导致文本与运动模态之间存在显著的语义模糊性：全局描述（如“一个人向前走并挥手”）无法捕捉局部肢体运动的细粒度动态，例如左右臂的非对称动作、腿部的步态细节或躯干的旋转幅度。这种信息缺失直接限制了系统在理解（检索）与生成两个方向上的精度上限。

KinMo 的核心洞察是：**通过按人体运动学树将运动分解为六个组件（躯干、颈部、左臂、右臂、左腿、右腿），并构建由全局动作、组级描述、交互描述组成的层次化文本表示，可以显著缩小文本‑运动模态差距**。这一分解使得模型首次能够对局部身体部位进行显式建模，从而支撑检索精度的跃升、生成质量的改善，以及此前方法无法实现的细粒度编辑与轨迹控制。

### 2. 方法沿革与关键差异

KinMo 建立在多条技术路线之上，其关键改进点可通过以下维度进行定位：

| 维度 | 先前方法 | KinMo 的改进 |
|------|----------|-------------|
| **运动表示** | 基于关节点位置、旋转和速度的原始表示（TMR、MoMask） | 按六个运动学组（Torso, Neck, Left Arm, Right Arm, Left Leg, Right Leg）组织的组位置、组角度、组速度及组间交互表示（Sec. 3.1） |
| **文本描述层次** | 仅全局动作文本 $T_c$（HumanML3D、TMR） | 全局动作 $T_c$ + 运动推理器生成的组级描述 $T_g$ + 交互级描述 $T_i$（Sec. 3.2 & Sec. 4） |
| **文本编码方式** | 单一 Transformer 编码器直接编码全部文本（ACTOR 等） | 层次化跨注意力编码器（HTMA），先编码全局动作，再以全局编码为条件逐步融入组级和交互级信息（Sec. 3.3） |
| **生成流程** | 一次性生成所有运动 tokens（MoMask） | 粗‑细三步生成：先生成初始 tokens（条件 $\mu_c$），再生成中间 tokens（条件 $\mu_g$），最后生成最终 tokens（条件 $\mu_i$）（Sec. 4.2） |
| **条件信号** | CLIP 文本嵌入作为生成条件（MoMask） | 层次对齐后的文本嵌入 $\mu_c, \mu_g, \mu_i$ 作为条件（Sec. 4.2） |
| **局部控制能力** | 无局部编辑/轨迹控制能力（MDM、MoMask） | 首次实现针对特定运动学组的细粒度编辑（Table 10）和关节轨迹控制（Table 11） |

**与 ParCo 的对比**：ParCo 同样采用基于部位的分解策略，但其仅将人体分为上半身和下半身两个部分。KinMo 的六组运动学分解（Table 3）在生成对齐度上显著优于二分解方案，验证了更细粒度的运动学分组对语义建模的增益。

**与 FG-MDM 的对比**：FG-MDM 探索了细粒度控制，但 KinMo 通过层次化文本‑运动对齐和粗‑细生成过程，在 FID 和 R-Precision 上均取得更优结果（Table 2），且首次将控制能力扩展到交互级描述（Table 10 中的 C+G+I 配置）。

### 3. 适用边界与局限

尽管 KinMo 在多个基准上取得显著提升，其方法存在以下适用边界和已知局限：

1. **短时过渡遗漏**：当文本描述包含大量短时过渡动作时，方法偶尔会遗漏某些步骤（Figure 12）。这表明层次化文本生成和粗‑细生成流程在处理高密度动作序列时可能出现信息压缩损失。

2. **低质量描述的退化效应**：运动推理器（微调 LLaMA-3）生成的组级和交互级描述质量直接影响下游性能。当推理器产生不准确的描述时，生成质量会出现退化（论文明确指出此局限，但未提供具体量化退化程度——该点需手动验证）。

3. **刚性体假设的失效边界**：组位置和组角度的计算基于运动学组内关节的刚性体假设。当身体部位内部发生显著非刚性变形（如肘部大幅屈伸导致上臂和下臂的相对关系剧烈变化）时，该假设可能失效。论文通过关键帧分割进行缓解，但在极端姿态下仍可能影响重建精度。

4. **编辑与控制架构的灵活性限制**：运动编辑和轨迹控制依赖于冻结或复制的骨干网络（ControlNet 架构），这可能限制了端到端学习的灵活性，且在分布外控制信号下可能出现生成质量下降。

### 4. 开放问题与未来方向

1. **大规模数据扩展**：自动提示优化（LLM + 人评估）的标注管线目前应用于约 44K 序列的 HumanML3D 数据集。如何将该管线扩展到更大规模的运动数据集（如 KIT-ML 的扩展版本或互联网规模的运动数据），同时保持标注质量，是一个尚未探索的问题。

2. **刚性体假设的严格验证**：在存在显著关节内弯曲的运动类型（如体操、舞蹈、格斗）中，刚性体假设的失效程度及其对检索和生成性能的影响尚未被严格量化验证。

3. **实时轨迹控制**：当前轨迹控制依赖 ControlNet 架构，论文未报告其推理延迟。轨迹控制能否在无需测试时优化的前提下扩展到实时应用（如交互式角色动画）仍是一个开放问题。

4. **语义对齐指标与人类判断的相关性**：论文提出了 HTMA‑S 等语义对齐指标，但这些自动指标与人类对编辑质量的主观判断之间的相关性尚未被系统研究。

5. **低质量描述的量化退化**：运动推理器生成质量对下游任务性能的具体量化退化曲线（如描述准确率与 FID 的函数关系）未被刻画，这对实际部署中的容错设计至关重要。



## 原文 PDF

![[paperPDFs/ICCV_2025/KinMo_Kinematic_aware_Human_Motion_Understanding_and_Generation.pdf]]
