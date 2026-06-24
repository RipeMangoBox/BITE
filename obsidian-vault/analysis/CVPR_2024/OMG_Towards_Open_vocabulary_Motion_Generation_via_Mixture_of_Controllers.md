---
title: OMG Towards Open-vocabulary Motion Generation via Mixture of Controllers
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/OMG_Towards_Open_vocabulary_Motion_Generation_via_Mixture_of_Controllers.pdf
aliases:
- OOVMG
- OTOVMGMC
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用预训练-微调范式：先在大规模（超过 2000 万帧）无标签运动数据上训练大规模无条件扩散模型，再利用运动 ControlNet 将文本作为条件注入，其中的 Mixture-of-Controllers 块通过交叉注意力和文本词汇特定专家自适应地将子运动与 CLIP 文本嵌入对齐。
primary_logic: 利用 CLIP 文本嵌入与运动特征的交叉注意力自动识别各文本词汇对应的子运动区间，并通过可学习的专家混合（Mixture-of-Experts）实现精细的子运动控制，有效解决了开放词汇文本到运动的对齐难题。
claims:
- 在零样本 Mixamo 测试集上，预训练模型的 FID 大幅优于无预训练模型，且模型规模越大提升越显著。
- 移除 MoC 块中的交叉注意力、零初始化卷积或注意力掩码均会导致 FID 和 CLIP-score 明显下降，验证了每个组件的有效性。
- OMG 在 Mixamo 零样本集上取得最佳的 FID（1.164）和 CLIP-score（0.588），显著优于 MLD、MDM 等 SOTA 方法。
- OMG 在 HumanML3D 域内测试中 R-Precision 最高（0.784），在扩散模型中 FID 最低（0.381）。
---

# OMG Towards Open-vocabulary Motion Generation via Mixture of Controllers

> [!tip] 核心洞察
> 利用 CLIP 文本嵌入与运动特征的交叉注意力自动识别各文本词汇对应的子运动区间，并通过可学习的专家混合（Mixture-of-Experts）实现精细的子运动控制，有效解决了开放词汇文本到运动的对齐难题。

| 字段 | 内容 |
|------|------|
| 中文题名 | OMG：通过控制器混合实现开放词汇运动生成 |
| 英文题名 | OMG Towards Open-vocabulary Motion Generation via Mixture of Controllers |
| 会议/期刊 | CVPR 2024 |
| Links | [Project](https://tr3e.github.io/omg-page) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | OMG (Open-vocabulary Motion Generation) |
| Dataset | HumanML3D, Mixamo |

> [!tip] 效果简介
> - HumanML3D (域内) 上，R-Precision ↑ 0.784 ± .002 vs 0.778 (MotionGPT) (+0.006)；FID ↓ 0.381 ± .008 vs 0.116 (T2M-GPT, 最佳), 0.473 (MLD, 扩散类最佳) (较扩散类最佳 +0.092 (但弱于 T2M-GPT))。
> - Mixamo (零样本) 上，FID ↓ 1.164 ± .009 vs 1.229 (MLD) (-0.065)；CLIP-score ↑ 0.588 ± .002 vs 0.552 (MotionGPT) (+0.036)；Diversity → 2.632 ± .021 vs 2.665 (Real), 2.594 (MDM) (与真实分布接近)。

## 概述

**问题瓶颈**：现有文本到运动生成方法高度依赖有限的配对文本-运动数据集，在训练未见的开放词汇文本提示下常常失败或产生不真实的动作，缺乏对复杂、抽象动作描述的泛化能力。

**核心思路**：OMG 采用预训练-微调范式，先在大规模（超过 2000 万帧）无标签运动数据上训练无条件扩散模型以学习丰富的运动先验，再通过运动 ControlNet 将文本作为条件注入。其中的关键模块——混合控制器块（Mixture-of-Controllers, MoC）利用 CLIP 文本嵌入与运动特征的交叉注意力自动识别各文本词汇对应的子运动区间，并通过可学习的专家混合实现精细的子运动控制，有效解决了开放词汇文本到运动的对齐难题。

**方法定位**：OMG 属于基于扩散模型的文本驱动运动生成方法，在预训练策略、条件注入方式和文本-运动对齐机制三个关键设计点上与已有方法形成差异。与 MDM（Tevet et al., ICLR 2023）、MLD、MotionDiffuse 等主流方法相比，OMG 的核心创新在于将大规模无条件预训练与可插拔的 ControlNet 式条件微调相结合，并通过 MoC 块实现词汇级别的细粒度控制。

**主要结果**：
- **零样本泛化**：在 Mixamo 零样本测试集上，OMG 取得最佳的 FID（1.164）和 CLIP-score（0.588），显著优于 MLD、MDM 等 SOTA 方法。
- **域内表现**：在 HumanML3D 域内测试中，OMG 的 R-Precision 最高（0.784），在扩散模型中 FID 最低（0.381）。
- **消融验证**：预训练对零样本 FID 的提升显著，且模型规模越大效果越明显；MoC 块中的交叉注意力、零初始化卷积和注意力掩码均对性能有重要贡献；增加专家池大小可进一步降低 FID。

**局限与展望**：OMG 仍受限于训练数据的运动流形，无法生成超出分布的运动类型；未显式建模子运动的时序顺序和物理合理性；当前仅关注人体躯干，尚未覆盖面部、手部等精细部位。

## 背景与动机

### 文本驱动运动生成的现状与瓶颈

人类运动生成是计算机视觉与图形学中的核心问题，其目标是根据给定的控制信号合成逼真的人体动作序列。在众多控制模态中，自然语言文本因其直观性和灵活性而成为最具吸引力的交互方式。近年来，基于扩散模型（diffusion models）和自回归模型（autoregressive models）的文本驱动运动生成方法取得了显著进展，代表性工作包括 **MDM**（Tevet et al., ICLR 2023）、**MLD**、**MotionDiffuse** 和 **T2M-GPT** 等。这些方法在 HumanML3D 等标准基准上展现了令人印象深刻的生成质量。

然而，现有方法存在一个根本性的瓶颈：**它们高度依赖有限的配对文本-运动数据集进行训练**。以广泛使用的 HumanML3D 数据集为例，其仅包含约 15,000 个文本-运动对，文本词汇的多样性和动作类别的覆盖范围极为有限。这种数据约束导致两个直接后果：

1. **泛化能力不足**：当面对训练中未见的开放词汇（open-vocabulary）文本提示时，现有模型常常产生语义不匹配或物理不真实的动作。例如，对于包含抽象描述（如“像猫一样伸展”）或细粒度动作组合（如“跆拳道回旋踢”）的提示，模型难以准确捕捉其运动特征。
2. **文本-运动对齐粗糙**：主流方法通常采用单一的交叉注意力（cross-attention）或 FiLM 层将文本条件注入运动生成主干，缺乏对文本中不同词汇所对应子运动（sub-motion）的精细化区分与控制能力。

### 零样本运动生成的尝试与不足

针对上述问题，一些工作尝试利用 CLIP 等视觉-语言模型实现零样本（zero-shot）运动生成。例如，**MotionCLIP** 通过 VAE 将运动映射到 CLIP 空间以实现文本驱动的生成，**MAA** 则采用文本-姿态对齐策略进行零样本迁移。然而，这些方法的生成质量与文本一致性仍远逊于域内（in-domain）监督训练的方法，在复杂动作和长文本场景下尤为明显。其根本原因在于，CLIP 空间的对齐是全局且粗糙的，无法有效处理文本中多个语义单元与运动时序片段的细粒度对应关系。

### 本文的核心动机

本文的核心动机源于一个关键洞察：**大规模无标签运动数据蕴含着丰富的动作先验，而 CLIP 文本嵌入与运动特征的交叉注意力机制可以自动识别各文本词汇对应的子运动区间**。基于此，本文提出 OMG（Open-vocabulary Motion Generation）方法，采用“预训练-微调”（pretrain-then-finetune）范式，将问题分解为两个互补的子任务：

- **预训练阶段**：在超过 2000 万帧的无标签运动数据上训练大规模无条件扩散模型（参数规模最高达 1B），使其学习到涵盖广泛动作类别和风格的运动流形（motion manifold）先验。
- **微调阶段**：引入运动 ControlNet 和混合控制器（Mixture-of-Controllers, MoC）块，冻结预训练主干，通过可训练的副本网络注入文本条件。MoC 块利用交叉注意力确定各文本词汇对应的子运动范围，并通过可学习的专家混合（Mixture-of-Experts）实现词汇特定的精细控制，从而有效解决开放词汇文本到运动的对齐难题。

这一设计使得 OMG 能够在仅使用 HumanML3D 训练集进行微调的情况下，对零样本的开放词汇文本提示生成高质量且语义一致的运动，显著突破了现有方法在泛化能力上的局限。

## 核心创新

OMG 的核心创新在于通过**预训练-微调范式**与**混合控制器（Mixture-of-Controllers, MoC）**两大支柱，系统性地解决了现有文本到运动生成方法在开放词汇场景下的泛化瓶颈。其关键创新点可归纳为以下三个维度的“changed slots”：

### 1. 预训练策略：从配对数据到大规模无标签运动先验

**Baseline 现状**：现有方法（如 MDM、MLD、MotionDiffuse 等）通常依赖随机初始化，并直接在有限的配对文本-运动数据集（如 HumanML3D）上训练条件生成模型。这导致模型对训练集未见过的文本描述泛化能力极弱。

**OMG 的创新**：采用先预训练后微调的两阶段范式。第一阶段在**超过 2000 万帧**的无标签运动数据上预训练一个无条件扩散模型，模型规模最高可达 **1B 参数**（OMG-Giant）。该阶段仅学习运动本身的分布先验，不涉及任何文本条件，从而充分利用海量无标签数据（详见 Sec. 3.1, Figure 6a）。

**因果机制**：预训练为模型注入了丰富的运动流形知识——包括物理合理性、运动多样性和时序连贯性。消融实验（Figure 6a）表明，预训练模型在零样本 Mixamo 测试集上的 FID 显著优于无预训练模型，且模型规模越大，优势越明显。这验证了“大规模运动先验是开放词汇泛化的必要条件”这一核心假设。

### 2. 条件注入方式：从直接注入到 ControlNet 残差控制

**Baseline 现状**：传统方法通常直接在扩散模型主干网络中注入文本条件，例如通过 FiLM 层或交叉注意力（如 MDM），这导致条件信号与运动生成过程深度耦合，难以在微调阶段保护预训练先验。

**OMG 的创新**：提出**运动 ControlNet（Motion ControlNet）**，冻结预训练的无条件去噪器主干，引入一个可训练的副本网络，并通过**零初始化卷积**将文本条件以残差形式注入（详见 Sec. 3.2, Figure 3）。零初始化卷积确保微调初期条件分支输出为零，从而保护预训练权重免受早期有害梯度的干扰。

**因果机制**：这种“冻结主干 + 可训练副本 + 零初始化残差连接”的设计，使得微调过程既能充分利用预训练先验，又能灵活适应文本条件。消融实验（Table 3）显示，移除零初始化卷积会导致 FID 和 CLIP-score 均显著恶化，证明了该设计对训练稳定性和最终性能的关键作用。

### 3. 文本-运动对齐机制：从单一注意力到词汇级专家混合

**Baseline 现状**：现有方法的文本-运动对齐通常采用单一的交叉注意力或简单 MLP，将所有文本词汇的信息等权融合，无法区分不同词汇对应的子运动区间和运动特性。

**OMG 的创新**：设计**混合控制器块（MoC）**，实现词汇级别的精细子运动控制。其核心机制包含三个紧密协作的组件：

- **交叉注意力融合**：通过文本嵌入与运动特征的交叉注意力，自动识别每个文本词汇对应的子运动时空范围，生成注意力掩码 $\mathbf{M}$（Eq. 3, Sec. 3.2）。
- **词汇特定专家混合**：维护一个包含 $K$ 个专家的参数池，通过门控网络 $\mathcal{G}$ 为每个文本词汇动态混合出专属的控制器参数 $\mathbf{e}^{(i)}$（Eq. 4-5, Sec. 3.2）。
- **掩码残差注入**：将专家输出与注意力掩码逐元素相乘，确保每个文本词汇仅控制其对应的子运动区域，生成条件残差 $\mathbf{r}_i$（Eq. 6, Sec. 3.2）。

**因果机制**：MoC 块通过“注意力定位子运动范围 + 专家混合适配词汇特性 + 掩码确保空间精度”的三步流水线，实现了从粗糙文本-运动对齐到**词汇级精细控制**的跃迁。消融实验（Table 3）表明，移除交叉注意力、零初始化卷积或注意力掩码中的任一组件，均导致 FID 和 CLIP-score 明显下降。此外，增加专家池大小 $K$ 可进一步降低 FID（Figure 6b），验证了多专家机制对适应开放词汇中多样运动特征的必要性。

### 创新总结

OMG 的三项核心创新形成了一条完整的因果链：**大规模无标签预训练**提供了泛化所需的运动先验，**ControlNet 残差注入**保护了该先验在微调中不被破坏，**MoC 词汇级控制**则实现了对开放词汇文本的精准对齐。三者协同作用，使得 OMG 在零样本 Mixamo 测试集上取得了最佳的 FID（1.164）和 CLIP-score（0.588），显著优于 MLD、MDM 等 SOTA 方法（Table 2, Sec. 4.2）。

## 整体框架

OMG 采用**预训练-微调（pretrain-then-finetune）**两阶段范式，将开放词汇文本到运动的生成任务拆解为运动先验学习与文本条件注入两个解耦的子问题。整体流程如 Figure 2 所示：

![[assets/figures/papers/paper_list_l1851_OMG_Towards_Open_vocabulary_Motion_Generation_via_Mixture_of_Controllers/figures/002_Figure_2.jpg]]
*Figure 2: Method overview. We train our OMG model in two stages. First, we leverage large-scale unlabeled motion data to pretrain an unconditional diffusion model with up to 1B parameters (Sec. 3.1). Then, we adopt a conditional fine-tuning scheme called motion ControlNet to condition the pre-trained diffusion model on text prompts (Sec. 3.2). During inference, the pre-trained unconditional denoiser and the fine-tuned conditional denoiser are combined with classifier-free guidance, generating realistic motions with zero-shot text inputs*

**第一阶段：无条件运动扩散预训练。** 在超过 2000 万帧的无标签运动数据上训练一个大规模无条件扩散模型（无条件去噪器），最大参数量达 1B（OMG-Giant）。该阶段仅学习运动的分布先验，不涉及任何文本条件，其核心目标是确保生成动作的逼真性与多样性。

**第二阶段：条件微调。** 冻结预训练的无条件去噪器，引入**运动 ControlNet**——包含预训练 Transformer 层的可训练副本与**混合控制器块（Mixture-of-Controllers, MoC）**。MoC 块接收 CLIP 文本编码器提取的词汇级嵌入，通过交叉注意力将文本语义与运动特征融合，并利用文本词汇特定的专家混合生成控制残差，以零初始化卷积的方式注入冻结的主干网络，从而在不破坏预训练先验的前提下实现精细的文本条件控制。

**推理阶段。** 结合无条件去噪器与条件去噪器的输出，通过无分类器引导（classifier-free guidance，引导强度 $s=4.5$）生成最终运动：

$$\hat{\mathbf{x}}^{(0)} = (1 - s) \cdot \mathcal{D}_u(\mathbf{x}^{(t)}, t) + s \cdot \mathcal{D}_c(\mathbf{x}^{(t)}, t, \mathbf{c})$$

**关键模块关系与数据流：**

1. **无条件扩散去噪器**（DiT 骨干 + 旋转位置嵌入）：预训练阶段在滑动随机窗口（最大长度 $L=300$，帧率 30）的无标签运动序列上，以简单扩散损失 $\mathcal{L}_{simple}$ 结合速度损失 $\mathcal{L}_{vel}$ 与足部接触损失 $\mathcal{L}_{foot}$（权重均为 30）进行训练，学习丰富的运动先验。

2. **CLIP 文本编码器**：将输入文本提示编码为词汇级嵌入序列与 eos 嵌入，作为 MoC 块的条件输入。

3. **运动 ControlNet**：微调阶段的核心适配器，包含冻结的预训练层与可训练副本。其内部的 MoC 块执行以下操作：
   - 通过交叉注意力 $\mathbf{f}' = \mathbf{f} + \mathrm{softmax}(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d}})\mathbf{V}$ 将文本信息融入运动特征，同时注意力矩阵 $\mathbf{A}$ 经 sigmoid 锐化（$\gamma=24$，$\beta=0.25$）生成注意力掩码 $\mathbf{M}$，自动确定每个文本词汇对应的子运动范围；
   - 门控网络 $\mathcal{G}$ 根据文本词汇嵌入计算混合权重 $\omega^{(i)} = \mathrm{softmax}(\mathcal{G}(\mathcal{E}(\mathbf{c}_i)))$，从 $K$ 个专家池参数中加权混合得到词汇特定专家参数 $\mathbf{e}^{(i)} = \sum_{j}^{K} \omega_j^{(i)} \mathbf{e}_j$；
   - 专家输出与注意力掩码逐元素相乘，生成第 $i$ 个文本词汇的控制残差 $\mathbf{r}_i = \mathbf{M}_{*,i} \circ \mathcal{F}(\mathbf{f}' | \mathbf{e}^{(i)})$，实现子运动级别的精细调控。

**输入输出规范：** 输入为任意长度的开放词汇文本提示，输出为对应的人体运动序列（基于 SMPL 骨架）。模型支持四种规模配置：OMG-Base（88M）、OMG-Large（201M）、OMG-Huge（405M）、OMG-Giant（1B），详见 Table 1。

## 核心模块与公式推导

OMG 采用两阶段范式：**无条件扩散预训练** 与 **运动 ControlNet 条件微调**。下面依次阐述两个阶段的核心模块及关键公式。

### 3.1 无条件扩散去噪器

预训练阶段的核心是一个基于 **Diffusion Transformer (DiT)** 骨干的大规模无条件扩散模型。与传统 DiT 的唯一区别在于，OMG 使用 **旋转位置嵌入 (rotary positional embedding)** 来编码时序位置。模型以滑动随机窗口方式处理运动序列，窗口最大长度 $L=300$，帧率设为 30。

**简单扩散损失**：无条件去噪器 $\mathcal{D}_u$ 的目标是从加噪运动 $\mathbf{x}^{(t)}$ 中预测干净运动 $\mathbf{x}$：

$$
\mathcal{L}_{simple} = \mathbb{E}_{\mathbf{x}, t, \epsilon} [\lambda_t \|\mathbf{x} - \mathcal{D}_u(\mathbf{x}^{(t)}, t)\|_2^2]
\tag{1}
$$

其中 $\lambda_t$ 为时间步 $t$ 相关的损失权重。

**联合训练损失**：为提升生成运动的物理合理性，在简单扩散损失基础上加入速度损失 $\mathcal{L}_{vel}$ 和足部接触损失 $\mathcal{L}_{foot}$ 作为正则化项：

$$
\mathcal{L} = \mathcal{L}_{simple} + \lambda_{vel} \mathcal{L}_{vel} + \lambda_{foot} \mathcal{L}_{foot}
\tag{2}
$$

两项正则化权重均设为 30。

### 3.2 运动 ControlNet 与混合控制器块

微调阶段引入 **运动 ControlNet**，其核心设计是：冻结预训练 Transformer 层的参数，并行引入一个可训练的副本，并通过 **混合控制器块 (Mixture-of-Controllers, MoC)** 将文本条件注入。ControlNet 中的卷积参数采用 **零初始化**，以在训练初期保护可训练副本免受有害梯度噪声的影响。

MoC 块是文本-运动对齐的关键模块，其内部流程如下：

**1. 交叉注意力融合**：以运动特征 $\mathbf{f}$ 生成 Query $\mathbf{Q}$，以 CLIP 文本嵌入生成 Key $\mathbf{K}$ 和 Value $\mathbf{V}$，通过交叉注意力将文本语义注入运动特征：

$$
\mathbf{f}' = \mathbf{f} + \mathrm{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d}}\right)\mathbf{V}
\tag{3}
$$

其中 $d$ 为特征维度。注意力矩阵 $\mathbf{A}$ 同时用于生成 **注意力掩码**，以确定每个文本词汇对应的子运动区间：

$$
\mathbf{M}_{*,i} = \mathrm{sigmoid}\left(\gamma(\mathbf{A}_{*,i} - \beta \max(\mathbf{A}_{*,i}))\right)
$$

掩码锐度 $\gamma=24$，阈值系数 $\beta=0.25$。

**2. 文本词汇特定专家混合**：MoC 维护一个含 $K$ 个专家的参数池 $\{\mathbf{e}_j\}_{j=1}^{K}$。对于第 $i$ 个文本词汇，通过门控网络 $\mathcal{G}$ 动态计算混合权重：

$$
\omega^{(i)} = \mathrm{softmax}\left(\mathcal{G}(\mathcal{E}(\mathbf{c}_i))\right)
\tag{5}
$$

其中 $\mathcal{E}(\mathbf{c}_i)$ 为第 $i$ 个文本词汇的 CLIP 嵌入，门控网络 $\mathcal{G}$ 为三层全连接网络。该词汇的专家参数由 $K$ 个专家池参数的加权和得到：

$$
\mathbf{e}^{(i)} = \sum_{j}^{K} \omega_j^{(i)} \mathbf{e}_j
\tag{4}
$$

**3. 条件残差生成**：将融合后的运动特征 $\mathbf{f}'$ 与词汇特定专家参数 $\mathbf{e}^{(i)}$ 输入函数 $\mathcal{F}$，再与注意力掩码 $\mathbf{M}_{*,i}$ 逐元素相乘，得到第 $i$ 个文本词汇对应的控制残差：

$$
\mathbf{r}_i = \mathbf{M}_{*,i} \circ \mathcal{F}(\mathbf{f}' \mid \mathbf{e}^{(i)})
\tag{6}
$$

所有词汇的控制残差汇总后注入 ControlNet 的可训练副本，实现对子运动的精细控制。

### 3.3 推理：无分类器引导

推理阶段，OMG 通过无分类器引导融合无条件与条件去噪器的输出：

$$
\hat{\mathbf{x}}^{(0)} = (1 - s) \cdot \mathcal{D}_u(\mathbf{x}^{(t)}, t) + s \cdot \mathcal{D}_c(\mathbf{x}^{(t)}, t, \mathbf{c})
\tag{7}
$$

其中 $\mathcal{D}_c$ 为条件去噪器，$\mathbf{c}$ 为文本条件，引导强度 $s=4.5$。这一机制在保持运动真实性与多样性的同时，强化了生成结果与文本提示的一致性。

### 补充图表

![[assets/figures/papers/paper_list_l1851_OMG_Towards_Open_vocabulary_Motion_Generation_via_Mixture_of_Controllers/figures/004_Figure_3.jpg]]
*Figure 3: Motion ControlNet (top) freezes the parameters of the pre-trained transformer layer and combines a trainable copy of the layer with the proposed Mixture-of-Controllers (bottom) block. The MoC block first fuses the text features and motion features and simultaneously determines the sub-motion ranges for each text token with the cross-attention mechanism. Then it performs finegrained control of sub-motions with text-token-specific experts*

## 实验与分析

### 核心瓶颈与实验动机

现有文本到运动生成方法（如 **MLD**、**MDM**、**MotionDiffuse**）高度依赖有限的配对文本-运动数据集（如 HumanML3D），导致在训练未见的开放词汇文本提示下常常产生不真实的动作，缺乏对复杂、抽象动作描述的泛化能力。OMG 的核心实验设计围绕两个关键问题展开：（1）大规模无标签运动数据的预训练能否为开放词汇泛化提供有效先验？（2）所提出的 Mixture-of-Controllers（MoC）块能否实现精细的文本-运动对齐？

### 实验设置

**数据集与评估协议**：预训练阶段使用超过 2000 万帧的无标签运动数据（来自多个 mocap 源，重定向至 SMPL 骨架，详见 Table A）。微调阶段统一使用 HumanML3D 训练集，域内评估在 HumanML3D 测试集上进行，零样本泛化评估在 Mixamo 测试集上进行（Table B）。所有定量评估均运行 20 次，报告平均值与 95% 置信区间，确保统计可靠性。

**模型规模配置**：OMG 提供四个规模变体——OMG-Base（88M）、OMG-Large（201M）、OMG-Huge（405M）、OMG-Giant（1B），具体架构配置见 Table 1。推理时采用无分类器引导（引导强度 $s=4.5$），结合无条件与条件去噪器输出：

$$\hat{\mathbf{x}}^{(0)} = (1 - s) \cdot \mathcal{D}_u(\mathbf{x}^{(t)}, t) + s \cdot \mathcal{D}_c(\mathbf{x}^{(t)}, t, \mathbf{c})$$

**对比方法**：涵盖了基于扩散（**MDM** (Tevet et al., ICLR 2023)、**MLD**、**MotionDiffuse**）、自回归（**T2M-GPT**）、VAE（**MotionCLIP**）、语言模型（**MotionGPT**）和零样本对齐（**MAA**）等多种范式的 SOTA 方法。对已有方法的结果尽量引用原文或公开实现。

### 主要结果

**域内性能（HumanML3D）**：如 Table 2 所示，OMG 在 R-Precision 上达到 **0.784 ± .002**，为所有方法中最高，超越了 MotionGPT 的 0.778，表明其对域内文本的语义理解能力最强。在 FID 指标上，OMG 取得 **0.381 ± .008**，在扩散类模型中为最佳（MLD 为 0.473），但弱于基于离散表征的自回归方法 T2M-GPT（0.116）。这一差距源于扩散模型与自回归模型在运动生成范式上的本质差异，但 OMG 在扩散模型类别中已显著缩小了与自回归方法的距离。

**零样本泛化（Mixamo）**：这是 OMG 的核心优势场景。在 Mixamo 零样本测试集上，OMG 取得最佳 FID **1.164 ± .009**，显著优于 MLD（1.229）和 MDM（1.477），证明预训练策略有效缓解了域偏移问题。在 CLIP-score 上，OMG 达到 **0.588 ± .002**，超越 MotionGPT（0.552），表明生成的开放词汇动作与文本语义高度一致。Diversity 指标为 2.632 ± .021，与真实分布（2.665）最为接近，说明模型在保持多样性的同时并未牺牲保真度。

**定性对比**：Figure 5 展示了 OMG 与基线方法在复杂动作描述（如"He performs spin kick with taekwondo skills"）上的生成对比，OMG 生成的动作在文本一致性和运动质量上均优于此前 SOTA 方法。Figure 4 进一步展示了模型对从单一短语到长自然句子的多样化未见提示的泛化能力。

### 消融实验

**预训练与模型规模的影响**：Figure 6a 揭示了决定性的因果证据——在 Mixamo 零样本测试集上，有预训练的模型在所有规模下均显著优于无预训练模型，且模型规模越大，性能提升越明显。这一结果表明，大规模无标签运动数据中蕴含的丰富动作先验是开放词汇泛化的关键瓶颈，仅靠有限的配对数据无法习得。

**专家池大小的影响**：Figure 6b 显示，增加 MoC 块中的专家池大小 $K$ 可进一步降低 FID。这表明多专家机制能够适应开放词汇中多样化的运动特征，每个文本词汇可以通过专家混合获得更精准的子运动控制参数。

**MoC 块组件有效性**：Table 3 的消融实验验证了 MoC 块中每个技术设计的必要性。移除交叉注意力、零初始化卷积或注意力掩码均导致 FID 和 CLIP-score 明显下降。零初始化卷积在训练初期保护可训练副本免受有害梯度噪声的影响，而注意力掩码（由 $\gamma=24$ 和 $\beta=0.25$ 控制）则确保每个文本词汇仅关注其对应的子运动区间，避免全局干扰。

### 失败模式与局限性

尽管 OMG 在开放词汇运动生成上取得了显著进展，但实验和论文讨论揭示了以下关键失败模式：

1. **运动空间受限**：OMG 仍依赖于训练数据的运动流形，无法生成超出训练数据分布的运动（如飞行、瑜伽、游泳等）。这是预训练-微调范式的固有限制。

2. **精细控制不足**：MoC 块未显式建模子运动的时序顺序和包含关系，难以处理精确控制任务（如拾取物体、到达目标）。当前方法仅实现了文本词汇到子运动区间的软对齐，缺乏对运动序列结构的显式建模。

3. **物理合理性欠缺**：未显式考虑物理动力学约束，生成的运动会存在物理不真实的情况（如滑步）。联合训练损失中的速度损失（$\mathcal{L}_{vel}$）和足部接触损失（$\mathcal{L}_{foot}$）仅提供了有限的几何正则化，无法替代真正的物理仿真。

4. **生成长度限制**：虽然支持任意长度生成，但实际生成长度受数据集最大长度限制（滑动随机窗口最大长度 $L=300$，帧率 30fps），无法实现无限时长的连贯运动。

5. **全身动态缺失**：当前仅关注人体躯干运动，未对面部、眼睛、手指甚至脚趾等精细部位进行建模，限制了在需要全身表现力场景中的应用。

### 关键图表索引

- **Table 2**：HumanML3D 和 Mixamo 测试集上的全面定量对比，展示 OMG 在域内和零样本场景下的综合性能。
- **Table 3**：MoC 块组件消融实验，验证交叉注意力、零初始化卷积和注意力掩码的必要性。
- **Figure 6**：预训练、模型规模和专家池大小的定量消融，揭示大规模预训练和专家混合对零样本泛化的因果贡献。
- **Figure 5**：与基线方法的定性对比，直观展示 OMG 在复杂动作描述上的文本一致性和运动质量优势。
- **Figure 7**：模型规模和 MoC 组件的定性可视化，展示更大模型对域外运动特征的理解能力以及技术设计对文本对齐的改善效果。

![[assets/figures/papers/paper_list_l1851_OMG_Towards_Open_vocabulary_Motion_Generation_via_Mixture_of_Controllers/figures/008_Table_2.jpg]]
*Table 2: Comparison of text-to-motion generation on HumanML3D [20] and Mixamo [1] test set. We ran all the evaluations 20 times, with the average reported alongside a 95% confidence interval. The right arrow → means the closer to real motion the better. Bold and underline indicate the best and the second best result. The term (Zero-shot) implies that the dataset contains unseen open-vocabulary texts*

![[assets/figures/papers/paper_list_l1851_OMG_Towards_Open_vocabulary_Motion_Generation_via_Mixture_of_Controllers/figures/010_Table_3.jpg]]
*Table 3: Quantitative evaluation on MoC block. The damping performance of the three variants of our model highlights the effectiveness of our MoC block technical designs*

![[assets/figures/papers/paper_list_l1851_OMG_Towards_Open_vocabulary_Motion_Generation_via_Mixture_of_Controllers/figures/007_Figure_6.jpg]]
*Figure 6: Quantitative evaluation on pre-training, model size, and expert pool size. (a) Models w pre-training show consistently improved performance over w/o pre-training, and w pre-training models, which benefit from large-scale motion data, improve with increasing model size. (b) Larger expert pool sizes improve the performance*

![[assets/figures/papers/paper_list_l1851_OMG_Towards_Open_vocabulary_Motion_Generation_via_Mixture_of_Controllers/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative evaluation on model sizes (a) and MoC block (b). Models with larger sizes effectively comprehend richer outof-domain motion features to present better motion expressions. Besides, our technical designs effectively improve the alignment with the input texts*

### 补充图表

![[assets/figures/papers/paper_list_l1851_OMG_Towards_Open_vocabulary_Motion_Generation_via_Mixture_of_Controllers/figures/003_Table_1.jpg]]
*Table 1: Sizes and architectures of our 4 models*

![[assets/figures/papers/paper_list_l1851_OMG_Towards_Open_vocabulary_Motion_Generation_via_Mixture_of_Controllers/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results generated by our model given various unseen text prompts. Our model effectively captures the motion characteristics from either a single phrase or longer natural sentences*

![[assets/figures/papers/paper_list_l1851_OMG_Towards_Open_vocabulary_Motion_Generation_via_Mixture_of_Controllers/figures/006_Figure.jpg]]

![[assets/figures/papers/paper_list_l1851_OMG_Towards_Open_vocabulary_Motion_Generation_via_Mixture_of_Controllers/figures/013_Figure.jpg]]
*Figure: A. User Study. We show the average quality rates and the average alignment rates of the compared methods, which indicate human evaluation of both motion quality and text-motion consistency respectively*

![[assets/figures/papers/paper_list_l1851_OMG_Towards_Open_vocabulary_Motion_Generation_via_Mixture_of_Controllers/figures/001_Figure_1.jpg]]
*Figure 1: Our Open-vocabulary Motion Generation (OMG) approach is capable of generating high-quality motions in response to unseen text prompts*

![[assets/figures/papers/paper_list_l1851_OMG_Towards_Open_vocabulary_Motion_Generation_via_Mixture_of_Controllers/figures/012_Table.jpg]]
*Table: A. The details of unlabeled motion datasets used at the pretraining stage. Table B. We use HumanML3D training set at the fine-tuning stage and HumanML3D and Mixamo test set for evaluation*

## 方法谱系与知识库定位

### 1. 领域瓶颈与OMG的因果突破

现有文本到运动生成方法的根本瓶颈在于：它们高度依赖有限的配对文本-运动数据集进行训练，导致在遇到训练未见的开放词汇文本提示时，常常产生不真实的动作或完全失败。这一瓶颈的因果根源是模型缺乏对复杂、抽象动作描述的泛化能力，而非简单的模型容量不足。

OMG 的核心因果旋钮（causal knob）是**预训练-微调范式下的条件注入机制重构**：
1. **预训练阶段**：在大规模（超过2000万帧）无标签运动数据上训练参数规模达1B的无条件扩散模型，学习丰富的运动先验；
2. **微调阶段**：冻结预训练主干，引入可训练的 Motion ControlNet 副本与 Mixture-of-Controllers (MoC) 块，通过交叉注意力和文本词汇特定专家自适应地将子运动与 CLIP 文本嵌入对齐。

这一设计的核心洞察在于：利用 CLIP 文本嵌入与运动特征的交叉注意力自动识别各文本词汇对应的子运动区间，并通过可学习的专家混合（Mixture-of-Experts）实现精细的子运动控制，有效解决了开放词汇文本到运动的对齐难题。

### 2. 与基线方法的范式对比

| 方法 | 范式 | 文本条件注入方式 | 零样本泛化能力 |
|------|------|------------------|----------------|
| **MDM** (Tevet et al., ICLR 2023) | 基于扩散 | 主干内直接注入文本条件 | 受限 |
| **MLD** | 基于潜在扩散 | 潜在空间条件注入 | 受限 |
| **MotionDiffuse** | 文本驱动扩散 | 主干内条件注入 | 受限 |
| **T2M-GPT** | 基于离散表征的自回归 | 自回归条件生成 | 受限 |
| **MotionCLIP** | VAE + CLIP 空间 | CLIP 空间对齐 | 部分支持 |
| **MAA** | 文本-姿态对齐 | 零样本对齐 | 部分支持 |
| **MotionGPT** | 运动-语言联合预训练 | 语言模型条件生成 | 部分支持 |
| **OMG** | 预训练-微调扩散 | ControlNet + MoC 残差注入 | **强** |

OMG 与上述方法的本质差异在于**条件注入的架构位置和机制**：基线方法通常在扩散模型主干中直接注入文本条件（如通过 FiLM 或交叉注意力），而 OMG 冻结预训练主干，通过 ControlNet 副本以残差方式注入条件。这一设计保护了预训练阶段学到的丰富运动先验不被微调阶段的有限配对数据破坏。

### 3. 关键设计槽位对比

| 设计槽位 | 基线做法 | OMG 做法 | 证据锚点 |
|----------|----------|----------|----------|
| 预训练策略 | 随机初始化或仅使用配对数据训练 | 在超过2000万帧无标签运动数据上预训练1B参数无条件扩散模型 | Sec. 3.1, Figure 6a |
| 条件注入方式 | 主干内直接注入（FiLM/交叉注意力） | 冻结主干 + 可训练 ControlNet 副本 + MoC 块残差注入 | Sec. 3.2, Figure 3 |
| 文本-运动对齐 | 单一交叉注意力或简单 MLP | MoC 块：交叉注意力确定子运动范围 + K 个专家池混合实现精细控制 | Sec. 3.2, Table 3 |

### 4. 适用边界

OMG 在以下场景中表现出显著优势：
- **开放词汇零样本运动生成**：在 Mixamo 零样本测试集上，OMG 取得最佳 FID（1.164）和 CLIP-score（0.588），显著优于 MLD、MDM 等 SOTA 方法（Table 2）。
- **域内文本-运动对齐精度**：在 HumanML3D 域内测试中，OMG 的 R-Precision 最高（0.784），在扩散模型中 FID 最低（0.381）（Table 2, Section 4.2）。
- **大规模预训练收益**：预训练模型的 FID 大幅优于无预训练模型，且模型规模越大提升越显著（Figure 6a）。

### 5. 局限性与开放问题

尽管 OMG 在开放词汇运动生成上取得了突破，但仍存在以下局限：

1. **运动空间受限**：OMG 仍依赖于训练数据的运动流形，无法生成超出训练数据分布的运动（如飞行、瑜伽、游泳等）。这是当前数据驱动方法的共性瓶颈。

2. **精细控制不足**：未显式建模子运动的时序顺序和包含关系，难以处理精确控制任务（如拾取物体、到达目标）。MoC 块的交叉注意力可以定位子运动区间，但缺乏对时序结构的显式建模。

3. **物理合理性欠缺**：未显式考虑物理动力学约束，生成的运动会存在物理不真实的情况（如滑步）。这源于扩散模型仅学习运动数据的统计分布，而非物理规律。

4. **最大长度限制**：虽然支持任意长度生成，但实际生成长度受数据集最大长度限制（滑动窗口 L=300，帧率 30），无法实现无限时长的连贯运动。

5. **全身动态缺失**：当前仅关注人体躯干运动，未对面部、眼睛、手指甚至脚趾等精细部位进行建模。

基于上述局限，该领域的开放问题包括：
- 如何利用物理引擎或强化学习在条件生成模型中引入物理合理性约束？
- 如何建模子运动的时序顺序和包含关系以实现精确的细粒度控制？
- 如何将生成能力扩展至数据分布外的运动类别？
- 如何实现无长度上限的连贯运动生成？
- 如何将方法扩展至全身动态（包括面部、手部等）的逼真生成？

## 原文 PDF

![[paperPDFs/CVPR_2024/OMG_Towards_Open_vocabulary_Motion_Generation_via_Mixture_of_Controllers.pdf]]