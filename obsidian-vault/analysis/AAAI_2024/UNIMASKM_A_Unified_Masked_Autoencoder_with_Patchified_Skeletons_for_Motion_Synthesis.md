---
title: "UNIMASKM: A Unified Masked Autoencoder with Patchified Skeletons for Motion Synthesis"
type: paper
paper_level: A
venue: AAAI
year: 2024
pdf_ref: paperPDFs/AAAI_2024/UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Motion_Synthesis.pdf
aliases:
- UM
- UNIMASKM
tags:
- AAAI_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将人体姿态分解为身体部件（补丁），并将不同任务统一为掩码重建问题，配合显式的掩码输入（告诉模型哪些关节被遮挡）以及课程学习策略，使得单一确定性模型能够灵活适应多种掩码模式，并利用姿态部件间的时空自注意力。
primary_logic: 将运动合成重新表述为掩码重建问题，通过姿态分解成补丁来增强模型对部分身体条件的适应能力，同时利用统一的自注意力机制同时捕捉时空关系，从而以高效、统一的方式在多项任务上达到或超越任务特定模型的水平。
claims:
- 在LaFAN1运动内插任务中，尤其在长过渡期（50和70帧），UNIMASK-M取得了最先进的性能。
- 在Human3.6M运动预测中，当观测序列有20%关节被遮挡时，UNIMASK-M在所有时间范围内均优于自回归模型（如SiMLPe、ST-DGCN）。
- 在运动完成任务中，与CrossViT相比，UNIMASK-M将MPJPE误差降低了12.54%。
- 移除姿态分解模块（PD）会导致运动内插性能下降。
---

# UNIMASKM: A Unified Masked Autoencoder with Patchified Skeletons for Motion Synthesis

> [!tip] 核心洞察
> 将运动合成重新表述为掩码重建问题，通过姿态分解成补丁来增强模型对部分身体条件的适应能力，同时利用统一的自注意力机制同时捕捉时空关系，从而以高效、统一的方式在多项任务上达到或超越任务特定模型的水平。

| 字段 | 内容 |
|------|------|
| 中文题名 | UNIMASKM：基于补丁化骨架的统一掩码自编码器用于运动合成 |
| 英文题名 | UNIMASKM: A Unified Masked Autoencoder with Patchified Skeletons for Motion Synthesis |
| 会议/期刊 | AAAI 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | UNIMASK-M |
| Dataset | Human3.6M, Human3.6M Motion Completion |

> [!tip] 效果简介
> - Human3.6M (20% occlusion) 上，MPJPE (mm) 74.5 @ 400ms, 120.5 @ 1000ms vs 86.8 @ 400ms, 129.1 @ 1000ms (MotionMixer) (-12.3 @ 400ms, -8.6 @ 1000ms)。
> - Human3.6M Motion Completion (90% future joints masked) 上，MPJPE reduction 12.54% lower than CrossViT vs CrossViT (adapted for completion) (-12.54% relative)。

## 概述

### 问题背景

人体运动合成涵盖运动预测、内插、完成等多个子任务。现有方法普遍存在两个结构性瓶颈：其一，方法设计高度任务特定，不同任务需训练独立模型，缺乏统一的建模框架；其二，姿态表征通常将整个人体骨架作为单一整体投影到公共空间，无法有效利用部分身体信息进行条件生成，对遮挡场景尤为敏感。

### 核心方法

UNIMASK-M 提出了一种统一的掩码自编码器框架，将各类运动合成任务重新表述为掩码重建问题。其关键创新在于**姿态补丁分解**：将人体骨架按肢体部件（腿、手臂、躯干等）拆分为补丁并独立编码为令牌序列，使模型能够以部分身体部件为条件进行灵活生成。配合显式的掩码嵌入和课程学习策略，单一确定性模型即可通过不同的掩码模式适应预测、内插、完成等多种任务，同时利用部件间的时空自注意力机制提升重建质量。

### 主要结果

- **运动内插**：在 LaFAN1 数据集上，UNIMASK-M 在长过渡期（50 帧和 70 帧）场景下取得最先进性能，显著优于 Oreshkin et al. (2022) 等任务特定方法。
- **遮挡鲁棒性**：在 Human3.6M 运动预测任务中，当观测序列有 20% 关节被遮挡时，UNIMASK-M 在所有时间范围内均优于自回归基线模型（如 **SiMLPe** (Guo et al., WACV 2023)、**ST-DGCN** (Ma et al., CVPR 2022)）。
- **运动完成**：相比 CrossViT，UNIMASK-M 将 MPJPE 误差降低 12.54%。
- **消融验证**：姿态分解模块和课程学习策略对性能提升均有显著贡献；移除姿态分解会导致内插性能下降，而课程学习相比预训练策略在预测和完成任务上平均 MPJPE 降低 0.89。

### 方法定位

UNIMASK-M 属于确定性掩码自编码器路线，与扩散模型（如 **MDM** (Tevet et al., 2022)）和条件变分自编码器（如 **U-CVAE** (Cai et al., ICCV 2021)）等方法形成互补——前者以高效的单次前向推理见长，后者在多样本生成方面具有优势。该框架为统一运动合成提供了一个简洁而有效的范式，但其确定性本质限制了多样化输出的能力，且当前验证范围局限于 Human3.6M 和 LaFAN1 两个数据集。

## 背景与动机

### 人体运动合成的任务碎片化困境

人体运动合成涵盖多种条件生成任务，包括**运动预测**（给定历史序列预测未来姿态）、**运动内插**（给定首尾关键帧填充中间过渡）和**运动完成**（从部分观测重建完整运动）。这些任务在动画制作、虚拟现实和机器人交互等应用中均有重要价值，但现有方法普遍采用**任务特定设计**：运动预测通常依赖自回归模型（如**SiMLPe** (Guo et al., WACV 2023)、**ST-DGCN** (Ma et al., CVPR 2022)），运动内插则需要双向推理架构（如Oreshkin et al., arXiv 2022），而运动完成又需专门的跨模态注意力机制（如**CrossViT**）。这种碎片化范式导致每个任务都需要单独训练模型，缺乏统一的框架支撑。

### 姿态条件建模的瓶颈：整体表征的局限

更深层的问题在于**姿态条件建模方式的固有限制**。现有方法通常将整个人体骨架作为一个整体投影到公共表征空间，这意味着条件输入必须是全骨架或全关节缺失的模式。当只有部分身体部件可见时——例如在遮挡场景下仅观测到上肢而腿部被遮挡——这些方法无法有效利用部分身体信息进行条件生成。这种“全或无”的条件范式对遮挡高度敏感，限制了模型在真实场景中的鲁棒性。

### 统一掩码重建范式的提出

针对上述双重瓶颈，UNIMASK-M 提出两个核心动机转变：

1. **任务统一**：将所有姿态条件运动合成任务重新表述为**掩码重建问题**——不同任务仅对应不同的掩码模式（预测=未来帧掩码，内插=中间帧掩码，完成=任意关节掩码），使得单一确定性模型能够灵活适应多种条件配置。

2. **姿态分解**：借鉴 ViT 将图像分解为补丁的思想，将人体骨架分解为**基于肢体的补丁**（腿、手臂、躯干等），独立投影为令牌序列。这种部件级分解使得模型能够以任意身体部件组合为条件进行生成，从根本上提升了对部分遮挡的鲁棒性，同时利用姿态部件间的时空自注意力捕捉运动关联。

## 核心创新

UNIMASK-M 的核心创新在于将人体运动合成重新表述为一个统一的掩码重建问题，并通过三个关键设计实现任务通用性与对部分身体条件的鲁棒性。

**1. 姿态补丁化分解（Pose Decomposition, PD）**

与以往将整个人体骨架作为单一整体投影到公共表征空间的方法不同，UNIMASK-M 提出将骨架分解为基于肢体的补丁（腿、手臂、躯干等），并独立线性投影为令牌序列。这一设计使得模型能够以部分身体部件为条件进行生成，从根本上增强了对遮挡场景和部分关键帧输入的适应能力。消融实验证实，移除 PD 模块会直接导致运动内插性能下降（LaFAN1 上 30 帧的 L2Q 从 0.57 升至 0.59，Table 5），验证了姿态分解对性能的因果贡献。

**2. 显式掩码嵌入与混合编码**

模型通过混合嵌入策略（Mixed Embeddings）将掩码信息显式地告知网络：为每个令牌叠加掩码嵌入（标记缺失补丁）、运动学嵌入（区分 5 个身体部件）以及正弦位置编码。这一设计使模型明确知晓哪些关节被遮挡，从而在推理时能够利用可见部件推断缺失区域，显著提升了遮挡鲁棒性。在 Human3.6M 运动预测任务中，当观测序列有 20% 关节被遮挡时，UNIMASK-M 在所有时间范围内均优于自回归基线（如 SiMLPe、ST-DGCN），400ms 处 MPJPE 为 74.5 mm，相比 MotionMixer 的 86.8 mm 降低 12.3 mm（Table 2）。

**3. 课程学习驱动的统一任务训练**

UNIMASK-M 通过不同的掩码模式将运动预测、内插、完成等任务统一为重建问题，单一确定性模型即可处理多种任务。为提升模型在困难任务上的鲁棒性，训练采用课程学习策略：掩码概率 $p_m$ 从 0.85 逐步增加至 1。相比先预训练再微调的策略，课程学习使统一模型在预测和完成两项任务上的平均 MPJPE 降低 0.89（Table 4），验证了其有效性。

**4. 双向自注意力与 Delta 输出策略**

不同于自回归模型使用的因果掩码，UNIMASK-M 的 ViT 编码器-解码器采用标准双向自注意力，能够同时捕捉所有补丁令牌之间的时空关系，且被掩码的补丁在编码阶段不被丢弃。网络输出预测相对于插值参考运动的偏移量，最终结果为 $\mathbf{Y} = f_{\theta}(\mathbf{X}_{fill}) + \mathbf{X}_{ref}$，这一 Delta 策略为重建提供了稳定的基准。

综上，UNIMASK-M 通过姿态补丁化、显式掩码嵌入和课程学习三个 changed slots，在保持架构简洁的前提下，实现了单一模型在多任务上的统一高性能，并在遮挡条件下展现出显著优于任务特定模型的鲁棒性。

## 整体框架

UNIMASK-M 将各类人体运动合成任务统一为一个**掩码重建问题**，其核心思想源于将 ViT 的图像补丁分解策略迁移至人体姿态，并借鉴 MAE 的自监督重建范式。整个 pipeline 围绕“部分已知骨架 → 完整运动序列”这一条件生成逻辑展开，通过单一确定性模型适应预测、内插、完成等多种掩码模式，无需为不同任务设计独立的因果或双向结构。

### 输入输出流

给定一段人体运动序列 $\mathbf{X}$ 及其对应的二值掩码 $\mathbf{M}$（标记哪些关节已知、哪些待重建），模型的目标是根据已知关节 $\bar{\mathbf{X}_q} = \mathbf{X} \odot (1 - \mathbf{M})$ 重建被掩码的缺失部分 $\mathbf{X}_m = \mathbf{X} \odot \mathbf{M}$。

在进入主干网络之前，系统首先对已知输入进行插值填充得到 $\mathbf{X}_{fill}$，以提供一致的输入结构。随后，模型并不直接预测绝对姿态，而是采用**delta策略**：网络输出的是相对于参考运动 $\mathbf{X}_{ref}$ 的偏移量，最终预测由两者相加得到：

$$\mathbf{Y} = f_{\theta}(\mathbf{X}_{fill}) + \mathbf{X}_{ref}$$

这一策略使网络只需学习残差信号，显著降低了优化的难度。

### 核心模块串联

UNIMASK-M 的主干由五个紧密衔接的模块组成，形成“分解 → 嵌入 → 编码 → 解码 → 聚合”的完整链路：

1. **Pose Decomposition (PD) — 姿态分解**  
   将每一帧骨架 $\mathbf{p}_t$ 按人体先验拆分为 $L=5$ 个肢体补丁（腿、手臂、躯干），每个补丁独立线性投影为令牌。这与传统方法将整帧骨架作为单一条件向量的做法形成根本区别——补丁化使得模型能够以**部分身体部件**为条件进行生成，从而天然具备对遮挡和局部条件输入的鲁棒性。

2. **Mixed Embeddings — 混合嵌入**  
   为每个令牌注入三重结构信息（见 Figure 3）：
   - **掩码嵌入** $\mathbf{emb}_{mask}$：显式告知模型哪些补丁被遮挡，使模型学会区分已知与待重建区域；
   - **运动学嵌入** $\mathbf{emb}_{kin}$：$L$ 个可学习的空间参数，对应不同身体部件，赋予令牌“我是左臂还是右腿”的语义；
   - **正弦位置嵌入** $\mathbf{emb}_{pos}$：提供时空位置信息。

   三者相加得到 $\mathbf{emb}_{mix}$，使编码器和解码器同时掌握掩码状态与时空结构。

3. **ViT Encoder — 编码器**  
   采用标准 ViT 自注意力编码器处理**全部令牌**（包括被掩码的补丁）。与 MAE 仅在编码阶段丢弃掩码令牌不同，UNIMASK-M 在编码阶段保留掩码令牌，使其参与全局自注意力计算，从而让已知部件与待重建部件之间建立充分的时空交互。

4. **ViT Decoder — 解码器**  
   同样采用标准 ViT 自注意力解码器，从编码后的表征中重建完整的补丁令牌序列。整个编解码过程不使用因果掩码，支持双向注意力，使模型能够同时利用过去和未来的已知信息。

5. **Pose Aggregation (PA) — 姿态聚合**  
   将解码后的补丁令牌按帧重新分组为 $\hat{\mathbf{E}}_{\mathbf{pose}}^{\bar{\alpha}} \in \mathbb{R}^{T \times L \cdot D}$，随后通过两层全连接网络（GELU 激活）将部件级表征融合为每帧的整体姿态表示 $\mathbf{E}_{\mathbf{pose}} \in \mathbb{R}^{T \times \hat{D}}$，最后投影回关节空间并与参考运动相加得到最终输出。

### 统一训练策略

为使单一模型同时胜任多种任务，UNIMASK-M 采用**课程学习**策略：训练过程中掩码概率 $p_m$ 从 0.85 逐渐增加至 1，逐步提升任务难度。消融实验表明，该策略在预测和完成两项任务上的平均 MPJPE 比“先预训练再微调”低 0.89 mm（Table 4），验证了渐进式难度递增对统一模型训练的有效性。在 Human3.6M 预测任务上，模型还额外引入了 DCT 编解码与时域 MLP（TempMLP）细化模块以提升性能（Figure 4），但该适配在 LaFAN1 等复杂运动数据上反而导致性能退化（L2Q 从 0.57 升至 0.68），说明 DCT 对周期性较弱的高动态运动并不适用。

> **注意**：本节对整体框架的描述基于论文方法论部分及 Figure 2/3 的架构说明。各模块的具体消融证据（如移除 PD 导致内插性能下降、补丁粒度 S3 最优等）将在后续实验分析章节详述。

![[assets/figures/papers/paper_list_l1819_UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Moti/figures/002_Figure_2.jpg]]
*Figure 2: UNIMASK-M architecture. Let a human motion X and its respective binary mask M. We first interpolate*

### 补充图表

![[assets/figures/papers/paper_list_l1819_UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Moti/figures/001_Figure_1.jpg]]
*Figure 1: Unified architecture for different human motion synthesis tasks. Green and purple skeletons denote a known skeleton joint, while light red and green represents our model prediction over a masked joint*

## 核心模块与公式推导

### 问题形式化与输出策略

UNIMASK-M 将各类姿态条件运动合成任务统一为掩码重建问题：给定已知运动 $\bar{\mathbf{X}_q} = \mathbf{X} \odot (1 - \mathbf{M})$，目标是重建被掩码的缺失关节 $\mathbf{X}_m = \mathbf{X} \odot \mathbf{M}$，其中 $\mathbf{M}$ 为二值掩码矩阵。

网络采用 **Delta-strategy** 输出策略，不直接预测绝对姿态，而是预测相对于插值参考运动的偏移量：

$$\mathbf{Y} = f_{\theta}(\mathbf{X}_{fill}) + \mathbf{X}_{ref}$$

其中 $\mathbf{X}_{fill}$ 是对已知关节进行线性插值后的完整序列，$\mathbf{X}_{ref}$ 为参考运动，$f_{\theta}(\mathbf{X}_{fill})$ 为网络预测的偏移量，最终输出 $\mathbf{Y}$ 为二者之和。该策略为输入提供了一致性基准，降低了直接重建完整运动的难度。

### 姿态分解模块（Pose Decomposition, PD）

姿态分解模块是 UNIMASK-M 的核心创新之一。该模块将人体骨架序列解构为基于肢体的补丁（patches），而非将整个姿态作为单一整体处理。具体而言，每个时刻的姿态 $\mathbf{p}_t$ 被分解为 $L$ 个身体部件（如腿、手臂、躯干），每个部件形成独立的补丁 $\hat{\mathbf{p}}_t$。随后，各补丁独立经过线性投影，展开为令牌序列 $\mathbf{E}$。

这种分解策略的关键因果机制在于：它允许模型以部分身体部件为条件进行生成，而非强制要求完整骨架或全关节掩码作为输入。当某些关节被遮挡时，模型仍可利用未遮挡部件的补丁信息进行推理，从根本上提升了遮挡鲁棒性。

### 混合嵌入策略（Mixed Embeddings）

为告知模型输入令牌的时空结构与掩码状态，UNIMASK-M 采用混合嵌入策略，为每个令牌叠加三种嵌入信息：

- **掩码嵌入** $\text{emb}_{mask}$：可学习的掩码令牌，显式标识哪些补丁被掩码，使模型明确知晓缺失区域；
- **运动学嵌入** $\text{emb}_{kin}$：$L=5$ 个空间可学习参数，分别对应不同身体部件，提供身体部件的身份信息；
- **位置嵌入** $\text{emb}_{pos}$：正弦位置编码，提供序列中的时空位置信息。

三者相加形成混合嵌入 $\text{emb}_{mix}$，注入编码器和解码器。该设计的核心价值在于：显式的掩码信息使模型能够区分“已知但被掩码”与“未知”的关节，从而在部分遮挡条件下做出更合理的推断。

### ViT 编码器-解码器架构

UNIMASK-M 采用标准 ViT 自注意力机制构建编码器和解码器。与典型 MAE 不同，编码器阶段**不丢弃被掩码的补丁令牌**，而是将所有令牌（包括被掩码的）一并输入编码器，利用双向自注意力同时捕捉所有补丁间的时空关系。解码器同样基于 ViT 自注意力，从编码后的表征中重建完整的补丁令牌序列。

这一设计使得单一确定性模型能够灵活适应不同的掩码模式（预测、内插、完成），无需为不同任务设计因果或双向结构的独立模型。

### 姿态聚合模块（Pose Aggregation, PA）

解码器输出的补丁令牌需重新组合为完整的姿态表示。姿态聚合模块首先将令牌按姿态重新分组为 $\hat{\mathbf{E}}_{\mathbf{pose}}^{\bar{\mathbf{\alpha}}} \in \mathbb{R}^{T \times L \cdot D}$，然后通过两层全连接网络（GELU 激活）将其投影为单一姿态表示 $\mathbf{E}_{\mathbf{pose}} \in \mathbb{R}^{T \times \hat{D}}$，融合各身体部件的信息。

### DCT 与时域 MLP 适配模块（Human3.6M 预测专用）

在 Human3.6M 运动预测任务上，UNIMASK-M 额外引入了两个适配模块以提升性能：

- **离散余弦变换（DCT）**：对输入运动序列进行 DCT 编码，将时域信号压缩到频域，利用人体运动的周期性先验；解码时通过逆 DCT（IDCT）恢复时域信号；
- **时域 MLP（TempMLP）**：由 $M$ 个全连接层、层归一化和残差连接组成的模块，用于平滑前缀序列到预测姿态的过渡，细化解码后的姿态序列。

需注意，这两个模块**仅在 Human3.6M 预测任务中使用**。在 LaFAN1 运动内插任务中，DCT 反而严重降低性能（L2Q 从 0.57 升至 0.68），因为该数据集的运动更复杂、周期性更低；TempMLP 则导致过拟合，对性能无助或有害。

### 补充图表

![[assets/figures/papers/paper_list_l1819_UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Moti/figures/004_Figure_3.jpg]]
*Figure 3: Mixed embedding strategy. The mixed embeddings are obtained by summing (i) a masking token to identify the masked patches*

![[assets/figures/papers/paper_list_l1819_UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Moti/figures/003_Figure_4.jpg]]
*Figure 4: Adaption of UNIMASK-M using DCT and TempMLP. First, we apply Discrete Cosine Transformation (DCT) and Inverted DCT (IDCT) to encode and decode the given motion. Additionally, we adopt a Temporal MLP (TempMLP) module to refine the predicted pose sequence through M blocks of fully connected layers (FC), Layer Normalization (LN) and a residual connection*

## 实验与分析

### 核心实验结果

UNIMASK-M 在多项运动合成任务上展现出竞争力或领先的性能，其关键优势体现在遮挡鲁棒性、长时程运动内插以及统一模型的多任务能力上。

**运动预测（Human3.6M）**：在标准预测设定下，UNIMASK-M 取得了具有竞争力的 MPJPE 结果。更重要的是，当观测序列有 20% 的关节被遮挡时，UNIMASK-M 在所有时间范围内均显著优于自回归基线模型。具体而言，在 400ms 和 1000ms 时间点，UNIMASK-M 的 MPJPE 分别为 74.5mm 和 120.5mm，相比 MotionMixer（Bouazizi et al., IJCAI 2022）的 86.8mm 和 129.1mm，分别降低了 12.3mm 和 8.6mm（Table 2）。这一结果直接验证了显式掩码嵌入与部件级补丁分解对部分观测条件的适应能力。

**运动内插（LaFAN1）**：UNIMASK-M 在长过渡期（50 帧和 70 帧）上取得了最先进的性能，明确优于 Oreshkin et al.（arXiv 2022）等方法（Table 3）。定性可视化（Figure 6）显示，UNIMASK-M 预测的运动轨迹（红色）比基线更接近真实轨迹（绿色），表明模型能够有效捕捉长时程的时空依赖关系。

**运动完成**：在 90% 未来关节被掩码的极端条件下，UNIMASK-M 相比 CrossViT 将 MPJPE 误差降低了 12.54%。这一结果凸显了姿态分解与掩码重建框架在处理严重信息缺失时的优势。

**统一模型的多任务能力**：通过课程学习策略训练的单一 UNIMASK-M 模型，在运动预测和完成两项任务上同时取得了优异表现。与统一基线 U-CVAE（Cai et al., ICCV 2021）相比，UNIMASK-M 在预测任务上 Top1 MPJPE 提升了 64.49%，在完成任务上提升了 88.12%。

### 消融实验与关键设计验证

消融实验系统性地验证了 UNIMASK-M 各核心组件的贡献，以及训练策略与任务适配模块的选择逻辑。

**姿态分解模块（PD）的必要性**：移除姿态分解模块（即不使用部件级补丁，将整个骨架作为单一令牌）会导致运动内插性能下降。在 LaFAN1 数据集上，30 帧过渡期的 L2Q 指标从 0.57 上升至 0.59（Table 5），证实了部件级分解对于利用局部身体信息和提升长时程合成质量至关重要。

**课程学习 vs. 预训练**：在统一模型训练中，采用课程学习策略（掩码概率 $p_m$ 从 0.85 逐渐增加至 1）比“先预训练再微调”的策略平均 MPJPE 低 0.89（Table 4）。这表明逐步增加任务难度能使模型更稳健地适应多种掩码模式，而非简单迁移预训练权重。

**DCT 与 TempMLP 的适用边界**：在 Human3.6M 预测任务中，引入离散余弦变换（DCT）与时域 MLP（TempMLP）的适配模块（Figure 4）有效提升了性能。然而，同样的设计在 LaFAN1 内插任务上却严重损害性能——使用 DCT 导致 L2Q 从 0.57 恶化至 0.68（Table 5）。论文将此归因于 LaFAN1 的运动更复杂、周期性更低，DCT 的频域压缩假设不再成立。此外，在 LaFAN1 上附加 TempMLP 会导致过拟合，对性能无益甚至有害。

**补丁粒度的选择**：不同补丁粒度（Figure 8）的实验表明，论文所采用的 S3 粒度（当前分解方式）在长期运动预测中优于更细（S1/S2）或更粗的粒度。在 1000ms 时间点，S3 的 MPJPE 为 112.10mm，优于 S1 的 114.06mm 和 S2 的 113.05mm。这验证了基于肢体的人体先验分解在平衡局部细节与全局结构方面的合理性。

### 失败模式与局限性分析

尽管 UNIMASK-M 在多项任务上表现优异，其设计与评估仍存在若干值得关注的局限：

1. **数据集泛化性未验证**：所有实验仅在 Human3.6M 和 LaFAN1 两个数据集上进行，未在更大规模或更具挑战性的数据集（如 AMASS、3DPW）上测试泛化能力。模型对不同运动风格、骨架拓扑的适应性尚不明确。

2. **确定性输出的固有限制**：UNIMASK-M 是一个确定性模型，无法生成多样化的运动样本。对于需要多模态输出（如给定相同关键帧生成不同风格过渡）的应用场景，该模型不适用。与扩散模型（如 MDM, Tevet et al., arXiv 2022）的推理速度对比也未考虑后者通过减少采样步数实现加速的潜力。

3. **补丁分解依赖人工先验**：当前的姿态分解策略基于人体肢体结构的人工定义，未探讨自动学习最优分割的可能性。对于包含手指、面部等更多身体部件的场景，该分解方式的可扩展性存疑。

4. **计算开销与长序列处理**：论文未报告 UNIMASK-M 在处理极长序列（例如超过 100 帧）时的计算开销和性能退化情况。ViT 架构的二次复杂度可能成为长序列应用的瓶颈。

5. **基线比较的公平性**：不同方法的计算平台、训练轮次等实现细节未统一，且部分基线（如 CrossViT）需适配到运动完成任务，其适配方式可能影响比较公平性。

### 补充图表

![[assets/figures/papers/paper_list_l1819_UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Moti/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of MPJPE error in 3D human motion forecasting for Human3.6M dataset. Here, bold denotes the best result at each time-horizon*

![[assets/figures/papers/paper_list_l1819_UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Moti/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison of MPJPE error in 3D human motion forecasting when the observed sequence has 20% joints occluded in Human3.6M dataset*

![[assets/figures/papers/paper_list_l1819_UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Moti/figures/009_Table_3.jpg]]
*Table 3: Quantitative evaluation of human motion inbetweening on LAFAN1 dataset. A lower score is better. Here, bold indicates the best result. Note that we trained a different model for the 50 and 70 transition frames for both (Oreshkin et al. 2022) and ours*

![[assets/figures/papers/paper_list_l1819_UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Moti/figures/011_Table_4.jpg]]
*Table 4: MPJPE error of UNIMASK-M in Human3.6M dataset under different training masking probabilities*

![[assets/figures/papers/paper_list_l1819_UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Moti/figures/012_Table_5.jpg]]
*Table 5: Performance of our UNIMASK-M under different configurations in the inbetweening task and the LaFan1 dataset (Harvey et al. 2020a)*

![[assets/figures/papers/paper_list_l1819_UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Moti/figures/013_Figure_8.jpg]]
*Figure 8: MPJPE millimeter error of the motion forecasting task of UNIMASK-M under different patch granularity*

![[assets/figures/papers/paper_list_l1819_UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Moti/figures/006_Figure_5.jpg]]
*Figure 5: Comparison of the motion forecasting task. Predicted skeletons are shown in red and blue*

![[assets/figures/papers/paper_list_l1819_UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Moti/figures/008_Figure_6.jpg]]
*Figure 6: Visual comparison of the inbetweening task with (Oreshkin et al. 2022) . We show the predicted motion trace for both (Oreshkin et al. 2022) (top row) and our UNIMASK-M (bottom row). The results show that our predicted trace (red) is closer to the ground-truth trace (green)*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

UNIMASK-M 的核心设计动机源于对现有运动合成方法两大瓶颈的突破：**任务特异性** 与 **条件刚性**。围绕这两个瓶颈，其与各基线的关系可归纳为以下几条线索。

#### 1.1 从任务特异性到统一建模

在 UNIMASK-M 之前，人体运动合成的主要范式是为每个子任务单独设计模型架构与训练策略：

- **运动预测** 领域的主流方法采用自回归或因果卷积结构，仅利用历史帧预测未来帧。代表性基线包括 **SiMLPe**（Guo et al., WACV 2023）、**ST-DGCN**（Ma et al., CVPR 2022）、**MotionMixer**（Bouazizi et al., IJCAI 2022）以及 **Mao et al.**（Mao, Liu, and Salzmann, ECCV 2020）。这些模型在完整观测条件下表现良好，但天然无法处理内插或完成等需要双向上下文的任务。
- **运动内插** 任务则由 **Oreshkin et al.**（arXiv 2022）和 **Duan et al.**（arXiv 2021）等方法主导，它们通常依赖特定的双向架构设计，无法直接迁移至预测场景。
- **运动完成** 任务中，**CrossViT**（原文未提供完整引用信息，需手动核实）利用跨模态注意力机制填补缺失关节，但其条件方式仍以全骨架为投影单元。
- 唯一尝试统一多任务的基线是 **U-CVAE**（Cai et al., ICCV 2021），采用条件变分自编码器框架。然而，U-CVAE 的统一性建立在将整个人体姿态作为单一条件投影到公共表征空间之上，这限制了其对部分身体信息的利用能力。

UNIMASK-M 的突破在于将上述所有任务重新表述为**掩码重建问题**：通过不同的掩码模式（预测 = 掩码未来帧；内插 = 掩码中间帧；完成 = 掩码任意关节），单一确定性模型即可覆盖全部任务。这一思想直接借鉴了掩码自编码器（MAE）在图像领域的成功经验，并将其适配到人体骨架这一结构化数据上。与 U-CVAE 相比，UNIMASK-M 不仅统一了任务，更通过姿态分解实现了对部分身体条件的精细利用，从而在统一性上更进一步。

#### 1.2 从整体投影到部件级条件

现有方法（包括上述所有基线）的一个共同假设是：输入条件必须是完整骨架或整个关节的缺失。当面对部分关节遮挡时，这些方法缺乏显式的处理机制，只能将整个关节视为缺失或存在。

UNIMASK-M 通过 **姿态分解模块（Pose Decomposition, PD）** 从根本上改变了这一范式。PD 将人体骨架分解为肢体补丁（腿、手臂、躯干），每个补丁独立投影为令牌。这一设计的直接效果是：
- 模型可以以**部分身体部件**为条件进行生成，而非必须依赖全骨架；
- 遮挡不再需要以整个关节为单位处理，而是可以精确到部件级别；
- 通过显式的掩码嵌入（`emb_mask`）告知模型哪些补丁被遮挡，模型对遮挡的鲁棒性显著提升。

这一改进在 Human3.6M 20% 关节遮挡实验中得到了直接验证：UNIMASK-M 在所有时间范围内均优于自回归基线（Table 2），且移除 PD 会导致运动内插性能下降（L2Q 从 0.57 升至 0.59，Table 5），证实了部件级分解的因果作用。

#### 1.3 与扩散模型的差异

**MDM**（Tevet et al., arXiv 2022）代表了运动合成领域的另一条技术路线——扩散模型。MDM 能够生成多样化的运动样本，这是其相对于确定性模型的天然优势。UNIMASK-M 作为确定性模型，单次前向传播只能产生唯一输出，无法满足需要多样输出的应用场景。论文中虽提及与 MDM 的速度对比，但仅比较了推理阶段的前向传播次数，未考虑扩散模型通过减少采样步数可能达到的速度提升，因此该对比的公平性需要谨慎看待。

### 2. 方法适用边界

UNIMASK-M 的适用边界由其核心设计选择所界定：

**确定性输出的局限。** 模型采用 Delta-strategy（$\mathbf{Y} = f_{\theta}(\mathbf{X}_{fill}) + \mathbf{X}_{ref}$）和单次前向传播，输出是确定性的。对于需要多样运动样本的任务（如运动生成、交互式动画创作），这一特性是根本性限制，而非可通过微调解决的问题。

**补丁粒度的先验依赖。** PD 模块的分解方式（5 个身体部件：双腿、双臂、躯干）基于人类先验知识。消融实验（Figure 8）表明，当前粒度 S3 在长期运动中优于更细或更粗的划分，但这一最优性可能仅适用于当前数据集和任务分布。论文未探讨自动学习最优分割的可能性，也未验证该分解在包含手指、面部等更多关节的骨架上的适用性。

**数据集的局限性。** 所有实验仅在 Human3.6M 和 LaFAN1 两个数据集上进行。Human3.6M 为室内受控环境下的单人动作，LaFAN1 虽包含更复杂的运动但规模有限。在 AMASS、3DPW 等更大规模、更具挑战性的数据集上的泛化能力尚未验证。

**序列长度的未探明边界。** 论文未讨论模型在处理极长序列（例如超过 100 帧）时的计算开销和性能退化情况。ViT 自注意力的二次复杂度可能在此场景下成为瓶颈。

**任务特定适配的成本。** 尽管核心架构统一，但在 Human3.6M 预测任务上仍需额外引入 DCT 编解码和 TempMLP 模块才能达到竞争性能。更值得注意的是，DCT 在 LaFAN1 上反而严重损害性能（L2Q 从 0.57 升至 0.68，Table 5），TempMLP 则导致过拟合。这表明“统一架构”在实际部署中仍需要任务特定的适配选择，并非完全即插即用。

### 3. 局限与开放问题

基于上述分析，UNIMASK-M 的局限性和由此衍生的开放问题可归纳如下：

**局限 1：生成多样性的缺失。** 确定性架构无法产出多样化的运动样本。对于需要“一对多”映射的场景（如给定相同关键帧生成不同风格的内插），UNIMASK-M 存在根本性不足。一个自然的延伸方向是将掩码重建框架与扩散或 VAE 等生成式方法结合，在保持统一性的同时引入多样性。

**局限 2：补丁分解的静态性。** 当前 PD 模块的分解方式是固定且基于先验的。开放问题包括：能否将分解扩展至更多身体部件（如手指、面部）？能否设计动态调整补丁粒度的机制，使模型根据任务或运动类型自适应地选择分解方式？能否完全抛弃人工先验，让模型自动学习最优的部件分割？

**局限 3：跨模态扩展的未验证性。** UNIMASK-M 当前仅处理纯运动数据。该框架能否自然延伸到其他输入模态（如文本描述、场景几何）条件化的运动合成任务？掩码重建的范式是否同样适用于多模态条件融合？这些问题尚无答案。

**局限 4：效率与性能的权衡。** 论文提出了 UNIMASK-M-light 这一更浅的变体以提升效率，但未系统报告其在更多任务上相对于全量模型的性能损失。在实时应用场景下，这一权衡需要更全面的量化分析。

**局限 5：评估基准的单一性。** 当前评估仅覆盖 Human3.6M 和 LaFAN1，缺乏在更多样化数据集上的验证。特别是，在包含人与物体交互、多人场景或野外环境的数据上，UNIMASK-M 的性能和鲁棒性仍是未知数。

**开放问题：极长序列与计算复杂度。** ViT 自注意力的二次复杂度在处理超长运动序列时可能成为计算瓶颈。是否存在更高效的注意力机制或序列压缩策略，能够在保持统一框架优势的同时降低计算开销？

## 原文 PDF

![[paperPDFs/AAAI_2024/UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Motion_Synthesis.pdf]]