---
title: InterMask 3D Human Interaction Generation via Collaborative Masked Modelling
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Modelling.pdf
aliases:
- I3HIGCMM
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入基于生成式掩蔽建模（generative masked modeling）的协同Token预测框架，结合保留时空结构的2D离散运动Token映射。
primary_logic: 将交互建模为离散2D标记的协同掩蔽与预测任务，使模型能够学习共同演化的人内时空注意力和人际跨注意力机制，从而精确生成同步且富有表现力的双人交互。
claims:
- InterMask采用2D离散运动Token图（相较于传统1D Token）显著降低了重建FID并提升了空间感知能力，其Recon FID为0.970（对比1D的3.146）。
- 移除时空注意力模块导致交互生成FID从5.154急剧上升至10.968，证明该模块对于生成复杂姿态与空间协调至关重要。
- 协同掩蔽建模相比逐人替代建模（FID 7.637）在交互保真度上具有显著优势（FID 5.154），同时保持了良好的文本对齐能力。
- "在InterHuman和InterX数据集上，InterMask均取得了最优的FID（InterHuman: 5.154 vs. in2IN 5.535; InterX: 0.399 vs. InterGen 5.207），验证了方法的有效性。"
---

# InterMask 3D Human Interaction Generation via Collaborative Masked Modelling

> [!tip] 核心洞察
> 将交互建模为离散2D标记的协同掩蔽与预测任务，使模型能够学习共同演化的人内时空注意力和人际跨注意力机制，从而精确生成同步且富有表现力的双人交互。

| 字段 | 内容 |
|------|------|
| 中文题名 | InterMask：基于协同掩码建模的3D人体交互生成 |
| 英文题名 | InterMask 3D Human Interaction Generation via Collaborative Masked Modelling |
| 会议/期刊 | ICLR 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | InterMask |
| Dataset | InterHuman, InterX |

> [!tip] 效果简介
> - InterHuman 上，FID 5.154 vs 5.535 (in2IN) (↓0.381)；Top-1 R-Precision 0.449 vs 0.449 (MoMat-MoGen) / 0.425 (in2IN) (持平/↑0.024)；MMDist 3.790 vs 3.790 (MoMat-MoGen) (持平)。
> - InterX 上，FID 0.399 vs 5.207 (InterGen) (↓4.808)；Top-1 R-Precision 0.403 vs 0.371 (InterGen) (↑0.032)。

## 概述

生成逼真且协调的3D双人交互是计算机视觉与图形学中长期存在的挑战。现有方法多基于扩散模型，逐步去噪生成运动序列，但此类框架难以精确捕捉两人之间精细的时空依赖关系，导致生成结果的真实感和交互协调性不足。针对这一瓶颈，本文提出**InterMask**——一种基于协同掩码建模（Collaborative Masked Modelling）的3D人体交互生成框架。

InterMask的核心思想是将双人交互建模为离散2D运动Token的协同掩蔽与预测任务。具体而言，该方法首先通过一个共享的VQ-VAE将每个个体的运动序列压缩为保留时空结构的2D离散Token图；随后，一个专用的**Inter-M Transformer**在生成式掩蔽建模框架下，对两人的Token进行协同预测。该Transformer内部集成了自注意力、共享时空注意力（建模人内依赖）以及交叉注意力（建模人际依赖）模块，使模型能够学习共同演化的人内与人际时空依赖关系，从而生成同步且富有表现力的双人交互。

在**InterHuman**和**InterX**两个基准数据集上，InterMask均取得了最优的生成保真度（FID分别为5.154和0.399），显著优于InterGen、in2IN等现有方法。消融实验进一步证实：2D Token图表示、时空注意力模块以及协同掩蔽建模策略，是性能提升的关键因素。此外，该方法在文本对齐、反应生成等任务上也展现出良好的能力。

## 背景与动机

### 问题背景

三维人体运动生成旨在根据文本描述合成自然、逼真的人体动作序列，在动画制作、虚拟现实和具身AI等领域具有广泛应用。随着单人运动生成技术的成熟，研究前沿已逐步转向**双人交互生成**——即同时生成两个个体的运动序列，且要求两者在空间和时间维度上高度协调。这一任务的核心挑战在于：交互不仅需要每个人保持高质量的独立姿态，还必须精确捕捉人际间的时空耦合关系，例如舞蹈中的同步性、拳击中的攻防时机、以及日常互动中的空间接近度。

### 现有方法及其瓶颈

当前主流的双人交互生成方法主要基于**扩散模型**（Diffusion Models）。典型工作包括：

- **InterGen**（Liang et al., 2024）：专为双人交互定制的扩散模型，通过条件机制联合生成两人运动。
- **ComMDM**：通过桥接两个单人生成扩散模型实现交互生成。
- **in2IN**（Ruiz-Ponce et al., 2024）：基于大语言模型（LLM）的交互生成扩展方法，在InterHuman数据集上达到SOTA。

然而，这些基于扩散模型的方法存在一个**核心瓶颈**：扩散模型的逐步去噪过程本质上是一种局部、迭代式的生成策略，难以精确捕捉两人交互中**长程、精细的时空依赖关系**。具体表现为：

1. **空间协调不足**：生成的两人动作可能出现肢体穿透、距离失当等问题。
2. **时间同步性差**：交互节奏（如舞蹈同步、攻防时机）与真实交互存在偏差。
3. **文本对齐弱**：对复杂交互描述的语义理解不够精确，导致生成结果与文本提示不一致。

这些问题在定量指标上表现为FID（Fréchet Inception Distance）偏高，在定性评估中则体现为交互真实感和协调性的不足。

### 本文动机

针对上述瓶颈，本文提出**InterMask**，核心动机是**从根本上改变交互生成的建模范式**——从扩散模型的逐步去噪转向**生成式掩蔽建模**（Generative Masked Modeling）。这一转变的直觉在于：

- 掩蔽建模通过**双向同时预测**所有被掩蔽的Token，能够以全局视角捕捉序列中的长程依赖，而非扩散模型的局部迭代。
- 将两人运动Token**协同掩蔽与预测**，使模型能够联合学习人内时空注意力（个体内部姿态协调）和人际跨注意力（个体间交互协调），从而生成同步且富有表现力的双人交互。

此外，为增强模型对时空结构的感知能力，InterMask引入**2D离散运动Token图**替代传统的1D序列Token，在保留时间维度的同时显式编码身体关节的空间布局，为协同掩蔽建模提供更丰富的结构先验。

## 核心创新

InterMask 的核心创新在于将双人交互生成从“逐步去噪的扩散范式”重构为“协同掩蔽建模的离散Token预测范式”，并通过**2D运动Token表示**与**协同Transformer架构**两个关键设计，系统性地解决了现有方法在精细时空依赖建模上的瓶颈。

### 1. 从1D序列到2D Token图：保留时空结构的运动表示

现有方法（如T2M、MDM、InterGen）普遍将运动序列压缩为**1D离散Token序列**，仅保留时间维度的依赖关系，丢失了身体关节之间的空间局部上下文。InterMask提出将个体运动通过共享的VQ-VAE编码为**2D离散Token图**，在时间和空间两个维度上同时保留结构信息，并通过2D卷积捕获身体局部上下文。

这一设计的因果效应在消融实验中得到了明确验证：将2D Token图替换为1D Token序列后，VQ-VAE的重建FID从**0.970**急剧恶化至**3.146**，MPJPE从**0.129**上升至**0.354**（Table 2）。这表明2D表示在保留精细运动细节和空间感知能力上具有决定性优势，为下游的交互生成提供了更高质量的离散表示基础。

### 2. 从扩散去噪到生成式掩蔽建模：双向协同预测

现有交互生成方法（如InterGen、ComMDM）基于扩散模型，通过逐步去噪生成运动，难以精确捕捉两人之间复杂的时空耦合关系。InterMask转而采用**生成式掩蔽建模（Generative Masked Modeling）**框架：训练阶段随机掩蔽部分Token，要求模型基于可见Token和文本条件双向预测被掩蔽的内容；推理阶段从全掩蔽状态出发，通过渐进式Token揭示（配合余弦调度和置信度重掩蔽）在固定20次迭代内生成完整交互序列。

这一框架的核心优势在于**协同性**——两个个体的Token被同时掩蔽、同时预测，模型被迫学习两人运动之间的联合分布。消融实验证实了这一点：将协同建模替换为“逐一生成”的替代建模策略后，交互FID从**5.154**上升至**7.637**（Table 3），证明协同预测对于生成协调一致的双人交互至关重要。

### 3. 协同Transformer中的三层注意力机制

Inter-M Transformer的架构设计直接服务于“人内-人际”双重依赖建模，每个Transformer块包含三个递进的注意力模块：

- **自注意力（Self-Attention）**：对拼接后的两人Token序列进行全局信息混合。
- **共享时空注意力（Shared Spatio-Temporal Attention）**：将注意力分解为空间注意力（同一时刻内的关节间依赖）和时间注意力（同一关节跨时间的演变），捕获个体内部的时空模式。
- **共享交叉注意力（Shared Cross Attention）**：在两个个体的Token之间建立直接的信息通道，显式建模人际交互依赖。

消融实验揭示了各模块的因果贡献：移除时空注意力模块导致FID从5.154飙升至**10.968**；移除交叉注意力模块使FID升至**11.246**（Table 3）。这表明时空注意力对于生成高质量个体姿态与运动节奏不可或缺，而交叉注意力是捕获人际空间协调（如距离、朝向、接触时机）的关键机制。

### 4. 创新总结

| 创新维度 | 基线方案 | InterMask方案 | 因果证据 |
|---------|---------|--------------|---------|
| 运动Token表示 | 1D序列Token | 2D Token图（时空结构保留） | Recon FID: 0.970 vs 3.146 (Table 2) |
| 生成框架 | 扩散模型（逐步去噪） | 生成式掩蔽建模（双向协同预测） | 协同 vs 逐一: FID 5.154 vs 7.637 (Table 3) |
| 人际建模 | 条件拼接/桥接网络 | 协同Transformer（时空注意+交叉注意） | 移除时空注意: FID 10.968; 移除交叉注意: FID 11.246 (Table 3) |
| 推理方式 | 多步迭代去噪 | 渐进式Token揭示（20次迭代） | 配合余弦调度与置信度重掩蔽 |

这些创新并非孤立存在，而是形成了完整的因果链条：2D Token图提供了保留时空结构的高保真离散表示，协同掩蔽建模迫使模型学习联合分布，而三层注意力架构为捕获人内演化与人际协调提供了结构化的信息通道。三者的协同作用使InterMask在InterHuman（FID 5.154）和InterX（FID 0.399）两个数据集上均取得了最优的交互生成质量。

## 整体框架

InterMask 采用两阶段生成范式，将双人 3D 交互建模为离散 Token 的协同掩蔽与预测任务。整个 pipeline 由四个核心模块串联构成：**2D Motion VQ-VAE Encoder**、**Learnable Codebook C**、**Inter-M Transformer** 和 **2D Motion VQ-VAE Decoder**，辅以冻结的 CLIP 文本编码器提供条件信号。

### 阶段一：运动离散化

给定两个个体的运动序列 $\{\mathbf{m}_p\}_{p \in \{a, b\}}$，其中 $\mathbf{m}_p \in \mathbb{R}^{N \times J \times d}$ 表示 $N$ 帧、$J$ 个关节、$d$ 维特征的时序数据，首先通过一个共享权重的 **2D Motion VQ-VAE Encoder** 将每个个体的运动独立编码为 2D 潜在表示。该编码器采用 2D 卷积层沿时间和空间维度同时下采样，将原始运动从 $(N, J, d)$ 压缩为 $(n, j, d')$ 的特征图，完整保留了人体的时空结构（见 Figure 7）。

随后，特征图中的每个向量通过查找 **Learnable Codebook C** 进行矢量量化，被替换为码本中最近邻向量的索引，得到 2D 离散 Token 图 $\{t_a, t_b\}$。这一设计的核心优势在于：相较于传统 1D 序列 Token（仅保留时间维度），2D Token 图显式维护了身体关节的空间布局，使模型能够通过 2D 卷积捕获局部身体上下文。消融实验证实，该设计将 VQ-VAE 重建 FID 从 1D 的 **3.146** 大幅降至 **0.970**，MPJPE 从 0.354 降至 0.129（Table 2），为下游生成提供了高保真的离散表示基础。

训练 VQ-VAE 的总损失函数为：

$$\mathcal{L}_{vqvae} = \mathcal{L}_{vq} + \lambda_{vel} \mathcal{L}_{vel} + \lambda_{fc} \mathcal{L}_{fc} + \lambda_{bl} \mathcal{L}_{bl}$$

其中 $\mathcal{L}_{vq} = \| \mathbf{m}_p - \hat{\mathbf{m}}_p \|_1 + \beta \| \tilde{\mathbf{t}}_p - \mathrm{sg}(\mathbf{t}_p) \|_2^2$ 为基础 VQ 损失（L1 重建损失与加权承诺损失），后续三项分别为速度损失、脚部接触损失和骨骼长度损失，共同约束运动学合理性。

### 阶段二：协同掩蔽生成

获得两个个体的 2D Token 图后，将其分别展平为一维序列，拼接后送入 **Inter-M Transformer** 进行协同掩蔽建模。该 Transformer 采用生成式掩蔽建模（Generative Masked Modeling）框架，而非主流的扩散模型范式——其核心差异在于：扩散模型依赖逐步去噪的多步迭代，而掩蔽建模在训练时随机掩蔽部分 Token，要求模型从双向上下文同时预测所有被掩蔽位置，天然适合捕获全局依赖。

Inter-M Transformer 的每个 Block 由三个注意力模块级联构成（Figure 2(c)）：

![[assets/figures/papers/paper_list_l1782_InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Model/figures/002_Figure_2.jpg]]
*Figure 2: Overview of InterMask. (a) Individual motions are quantized through vector quantization*

1. **Self-Attention**：标准缩放点积注意力 $\mathrm{Attn}(\mathbf{Q},\mathbf{K},\mathbf{V}) = \mathrm{softmax}(\mathbf{Q}\mathbf{K}^{\top}/\sqrt{\tilde{d}})\mathbf{V}$，实现 Token 间的通用交互。

2. **Shared Spatio-Temporal Attention**：将注意力拆分为空间注意力（同一时刻内不同关节 Token 相互关注）和时间注意力（同一关节位置跨时间关注），显式建模人内时空依赖。消融实验表明，移除此模块导致交互生成 FID 从 **5.154** 急剧恶化至 **10.968**（Table 3），证明其对复杂姿态与空间协调的关键作用。

3. **Shared Cross Attention**：在两个个体的 Token 序列间建立人际交叉注意力，捕获交互双方的空间协调与动作同步。移除此模块后 FID 升至 **11.246**（Table 3），验证了人际依赖建模的必要性。

文本条件通过冻结的 **CLIP 文本编码器** 提取嵌入，经自适应层归一化（AdaLN-mod）注入 Transformer 的每一层，驱动生成过程与文本描述对齐。

训练时，掩蔽策略采用两阶段设计（Figure 8）：第一阶段以概率 $p_r$ 进行随机掩蔽或以 $1-p_r$ 进行交互掩蔽；第二阶段对第一阶段预测的 Token 施加 Step Unroll Masking。训练目标为掩蔽位置上的交叉熵损失：

$$\mathcal{L}_{mask} = \sum_{\tilde{t}_k = [\mathrm{MASK}]} -\log p_{\theta}(t_k | \tilde{t}, c)$$

### 推理流程

推理采用渐进式 Token 揭示策略（Figure 3）。初始时两个个体的 Token 序列完全掩蔽 $\{t_a(0), t_b(0)\}$，Inter-M Transformer 在 $I$ 次迭代中逐步预测所有 Token。每次迭代使用余弦调度 $\gamma(\tau_i) = \cos(\frac{\pi \tau_i}{2})$ 控制保留 Token 的数量，并基于置信度分数对低置信度 Token 进行重掩蔽，结合无分类器引导增强文本对齐。最终，预测的 Token 图经码本解量化后，由 **2D Motion VQ-VAE Decoder** 解码为两个个体的完整运动序列 $\{\mathbf{m}_a, \mathbf{m}_b\}$。

![[assets/figures/papers/paper_list_l1782_InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Model/figures/003_Figure_3.jpg]]
*Figure 3: Inference process. Starting from completely masked token sequences of both individuals*

### 与替代方案的对比

为验证协同建模的必要性，作者设计了替代建模方案（Figure 10）：训练时仅更新一个体的嵌入而条件于另一个体，推理时交替预测和重掩蔽每个个体的 Token。该方案 FID 为 **7.637**，显著劣于协同建模的 **5.154**（Table 3），证实了同时预测双方 Token 对于生成协调交互的不可替代性。

## 核心模块与公式推导

InterMask 的核心架构由两个阶段级联构成：**2D 运动 VQ-VAE** 负责将个体运动压缩为离散 Token 图，**Inter-M Transformer** 在此基础上以协同掩码建模方式生成双人交互序列。以下逐一展开关键模块及其公式。

### 2D 运动 VQ-VAE

该模块的目标是将单人的运动序列映射到一个保留时空结构的二维离散表示。给定运动序列 $\mathbf{m}_p \in \mathbb{R}^{N \times J \times d}$（$N$ 帧、$J$ 个关节、$d$ 维特征），编码器通过 2D 卷积下采样得到潜在表示 $\tilde{\mathbf{t}}_p \in \mathbb{R}^{n \times j \times d'}$，随后在可学习码本 $\mathcal{C}$ 中查找最近邻向量进行量化，得到离散 Token 图 $\mathbf{t}_p$。

训练 VQ-VAE 的核心损失函数为：

$$
\mathcal{L}_{vq} = \| \mathbf{m}_p - \hat{\mathbf{m}}_p \|_1 + \beta \| \tilde{\mathbf{t}}_p - \mathrm{sg}(\mathbf{t}_p) \|_2^2 \tag{1}
$$

其中第一项为 L1 重建损失，第二项为加权承诺损失（$\beta$ 为权重系数），$\mathrm{sg}(\cdot)$ 表示停止梯度算子。

为提升运动重建的物理合理性，总损失进一步加入三项几何约束：

$$
\mathcal{L}_{vqvae} = \mathcal{L}_{vq} + \lambda_{vel} \mathcal{L}_{vel} + \lambda_{fc} \mathcal{L}_{fc} + \lambda_{bl} \mathcal{L}_{bl} \tag{2}
$$

其中速度损失 $\mathcal{L}_{vel}$ 约束相邻帧关节位移的一致性，脚部接触损失 $\mathcal{L}_{fc}$ 抑制脚部滑动，骨骼长度损失 $\mathcal{L}_{bl}$ 保持肢体比例恒定。各损失的具体定义见附录 C Equation (10)。

**消融证据**：Table 2 显示，采用 2D Token 图（相较于传统 1D 序列 Token）使 VQ-VAE 重建 FID 从 3.146 降至 0.970，MPJPE 从 0.354 降至 0.129，验证了保留空间维度对运动重建质量的关键作用。

### Inter-M Transformer

Inter-M Transformer 以生成式掩码建模（Generative Masked Modeling）方式协同预测两人的运动 Token。其每个 Transformer Block 由三个注意力子模块级联构成：

1. **自注意力（Self-Attention）**：对拼接后的 Token 序列执行标准缩放点积注意力：
   $$
   \mathrm{Attn}(\mathbf{Q},\mathbf{K},\mathbf{V}) = \mathrm{softmax}(\mathbf{Q}\mathbf{K}^{\top}/\sqrt{\tilde{d}})\mathbf{V} \tag{4}
   $$

2. **共享时空注意力（Shared Spatio-Temporal Attention）**：将注意力分解为空间维度和时间维度。空间注意力使每个 Token 仅与同一时间实例内的其他空间 Token 交互，时间注意力使每个 Token 仅与同一空间位置跨时间的 Token 交互。这一设计显式建模了人内时空依赖。

3. **共享交叉注意力（Shared Cross Attention）**：在两人的 Token 之间建立人际依赖，使模型能够学习交互协调性。

文本条件通过冻结的 CLIP 文本嵌入注入，采用自适应层归一化（AdaLN-mod）方式调节 Transformer 各层的归一化参数。

**训练目标**：对掩码位置的 Token 最小化负对数似然：
$$
\mathcal{L}_{mask} = \sum_{\tilde{t}_k = [\mathrm{MASK}]} -\log p_{\theta}(t_k | \tilde{t}, c) \tag{8}
$$
其中 $\tilde{t}$ 为掩码后的 Token 序列，$c$ 为文本条件。

训练时采用两阶段掩码策略：第一阶段以概率 $p_r$ 执行随机掩码或以 $1-p_r$ 执行交互掩码，第二阶段对第一阶段预测结果进行逐步展开掩码（Step Unroll Masking）。掩码比例由余弦调度控制：
$$
\gamma(\tau_i) = \cos\left(\frac{\pi \tau_i}{2}\right) \in [0,1] \tag{3}
$$
其中 $\tau_i$ 从均匀分布采样。

**消融证据**：Table 3 表明，移除时空注意力模块使交互生成 FID 从 5.154 急剧上升至 10.968；移除交叉注意力模块使 FID 升至 11.246。Table 4 显示将随机掩码概率 $p_r$ 设为 0.8 可在交互生成（FID 5.154）与反应生成（FID 2.991）之间取得最佳平衡。

### 推理过程

推理从完全掩码的 Token 序列 $\{t_a(0), t_b(0)\}$ 出发，在 $I$ 次迭代中渐进式揭示 Token。每轮迭代中，模型预测所有掩码位置的概率分布，根据置信度保留部分 Token 并重新掩码其余位置，保留比例由余弦调度控制。最终将预测的 Token 图经 VQ-VAE 解码器还原为运动序列 $\{\mathbf{m}_a, \mathbf{m}_b\}$。整个过程固定为 20 次迭代，无需扩散模型的多步去噪。

### 补充图表

![[assets/figures/papers/paper_list_l1782_InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Model/figures/011_Figure_7.jpg]]
*Figure 7: Detailed illustration of the 2d discrete motion token map construction. The 2d encoder, consisting of 2d convolutional layers, downsamples the input motion from*

![[assets/figures/papers/paper_list_l1782_InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Model/figures/012_Figure_8.jpg]]
*Figure 8: Illustration of the two-stage masking technique used during training of the Inter-M Transformer. For stage 1, we either apply Random Masking with a probability of*

![[assets/figures/papers/paper_list_l1782_InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Model/figures/017_Figure_10.jpg]]
*Figure 10: Overview of the Alternative Modeling approach, where we predict the tokens of one person at a time. (a) During training, only the embeddings of one individual*

## 实验与分析

### 主实验结果

InterMask 在两个主流双人交互数据集上均取得了最优的生成质量。Table 1 报告了 InterHuman 和 InterX 测试集上的定量评估结果。

![[assets/figures/papers/paper_list_l1782_InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Model/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation on the InterHuman and InterX test sets. ± indicates a 95% confidence interval and → means the closer to ground truth the better. Bold face indicates the best result, while underscore refers to the second best*

在 **InterHuman** 数据集上，InterMask 的 **FID 达到 5.154**，优于此前最优方法 in2IN 的 5.535（↓0.381），也显著领先于基于扩散模型的 InterGen（FID 8.303）和检索增强的 MoMat-MoGen（FID 7.110）。在文本对齐指标上，InterMask 的 **Top-1 R-Precision 为 0.449**，与 MoMat-MoGen 持平，优于 in2IN 的 0.425；**MMDist 为 3.790**，同样与 MoMat-MoGen 持平，优于 InterGen 的 4.398。Diversity 指标上，InterMask 取得 13.899，与真实数据的 14.060 最为接近，表明其生成结果在保持高保真度的同时未牺牲多样性。

在 **InterX** 数据集上的优势更为显著：InterMask 的 **FID 为 0.399**，相较于 InterGen 的 5.207 大幅降低（↓4.808），**Top-1 R-Precision 为 0.403**，优于 InterGen 的 0.371。这一跨数据集的泛化能力验证了协同掩码建模框架的有效性。

所有评估指标均基于 20 次独立运行的平均值，并报告了 95% 置信区间。对比方法均使用官方实现或公开模型权重，确保公平性。

### 消融实验

消融实验围绕两个核心模块展开：运动 VQ-VAE 的 Token 表示设计（Table 2）和 Inter-M Transformer 的注意力机制设计（Table 3）。

![[assets/figures/papers/paper_list_l1782_InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Model/figures/007_Table_2.jpg]]
*Table 2: Ablation Study results on InterHuman test set to verify key components of the proposed Motion VQ-VAE. Bold face indicates the best result*

![[assets/figures/papers/paper_list_l1782_InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Model/figures/008_Table_3.jpg]]
*Table 3: Ablation Study results on the InterHuman test set to verify key components of the proposed Inter-M Transformer. Bold face indicates the best result*

**2D Token 图 vs 1D Token 序列。** Table 2 显示，将运动表示为 2D Token 图（保留时空结构）相较于传统 1D Token 序列，使 VQ-VAE 的重建 FID 从 3.146 降至 **0.970**，MPJPE 从 0.354 降至 **0.129**。这一改进的关键在于 2D 卷积能够捕获身体关节间的局部空间上下文，而非将运动简单展平为时间序列。定性结果（Figure 11）进一步显示，1D Token 序列会导致重建动作模糊和关节漂移，而 2D Token 图能更精确地保留肢体位置和运动细节。

**注意力模块的必要性。** Table 3 报告了对 Inter-M Transformer 各组件的消融结果。完整模型的交互生成 FID 为 5.154。**移除时空注意力模块**后，FID 急剧上升至 **10.968**（↑5.814），证明该模块对于捕获人内时空依赖、生成复杂姿态与空间协调至关重要。**移除交叉注意力模块**使 FID 升至 **11.246**（↑6.092），验证了人际依赖建模的必要性——缺乏交叉注意力时，模型无法有效协调两人的相对位置和动作时序。定性对比（Figure 12）显示，无时空注意力时生成的动作僵硬且缺乏协调性，无交叉注意力时两人动作各自独立、缺乏交互语义。

**协同建模 vs 替代建模。** 论文还比较了协同掩码建模与“逐一生成”（Alternative Modeling）策略。后者在训练和推理阶段交替预测两人的 Token，FID 为 7.637，显著劣于协同建模的 5.154。这表明同时考虑两人的全局上下文对于生成连贯交互至关重要。

**掩码策略的平衡。** Table 4 探索了随机掩码概率 $p_r$ 的影响。$p_r=0.8$ 时在交互生成（FID 5.154）与反应生成（FID 2.991）之间取得最佳平衡。过高的随机掩码会削弱模型学习交互模式的能力，而过低则限制了生成多样性。

### 失败模式与局限性

尽管整体性能优异，InterMask 仍存在以下已知局限：

1. **身体穿透问题。** 当输出骨架转换为 SMPL 网格时，可能出现两人身体相互穿透的情况（Figure 14 第一行）。这是因为当前训练仅在骨架层面进行，未引入网格级碰撞约束。未来可探索在训练中加入网格转换及抗穿透损失。

![[assets/figures/papers/paper_list_l1782_InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Model/figures/021_Figure_14.jpg]]
*Figure 14: Examples of Limitations of our method. The first row shows body penetration when converted from output skeleton to SMPL mesh. The second row shows implicit bias towards dancing*

2. **数据集隐性偏差。** 模型可能继承训练数据的偏见，例如在文本提示未明确要求舞蹈时错误生成舞蹈动作（Figure 14 第二行）。这一问题的根源在于数据集中舞蹈类交互占比较高，模型倾向于将交互泛化为舞蹈模式。

3. **序列长度限制。** 由于 Token 图的尺寸固定，当前方法仅支持最长约 10 秒的运动序列。处理更长序列需要重新设计 Token 表示，例如采用可变维度 Token 图或层次化建模策略。

### 用户研究

为验证生成结果的感知质量，论文在 Amazon Mechanical Turk 上进行了用户研究（Figure 5），仅选用高信誉评估者（Master 资格、>97% 任务批准率、>1000 次已批准任务）。评估者需在 InterMask 与 InterGen 的生成结果中选择更符合文本描述且交互更自然的一方。结果显示，InterMask 在交互质量和文本一致性上均获得显著偏好，进一步支持了定量指标的优势。

![[assets/figures/papers/paper_list_l1782_InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Model/figures/006_Figure_5.jpg]]
*Figure 5: User Study comparing our Inter-Mask and InterGen (Liang et al., 2024)*

### 补充图表

![[assets/figures/papers/paper_list_l1782_InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Model/figures/018_Figure_11.jpg]]
*Figure 11: Qualitative results for the ablation study on Motion VQ-VAE to verify the proposed 2D token map*

![[assets/figures/papers/paper_list_l1782_InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Model/figures/019_Figure_12.jpg]]
*Figure 12: Qualitative results for the ablation study on Inter-M Transformer to verify contributions of the proposed Attention modules*

## 方法谱系与知识库定位

### 1. 问题定位：从单人扩散到协同掩蔽建模

InterMask 的核心贡献在于将 3D 人体交互生成从**扩散模型的逐步去噪范式**迁移到**生成式掩蔽建模（Generative Masked Modeling）**框架。已有方法大致分为三条技术路线：

- **单人扩散模型的桥接扩展**：**ComMDM** 通过桥接两个预训练的单人扩散模型（如 **MDM**）实现交互生成。该方法依赖条件特征拼接或桥接网络来协调两个个体的运动，但本质上仍将交互视为两个独立生成过程的耦合，难以精确捕捉人际间的精细时空依赖。

- **专为双人交互定制的扩散模型**：**InterGen** (Liang et al., 2024) 是其中的代表性工作，直接在交互数据上训练扩散模型。然而，扩散模型的逐步去噪过程在建模长程、双向的时空依赖时存在固有局限，导致生成结果的交互协调性和真实感不足。

- **检索增强与 LLM 扩展方法**：**MoMat-MoGen** 引入检索机制辅助生成；**in2IN** 则基于 LLM 扩展交互生成能力，在 InterHuman 数据集上取得了 InterMask 出现前的 SOTA 结果（FID 5.535）。

InterMask 的关键洞察在于：将交互建模为**离散 2D Token 的协同掩蔽与预测任务**，使模型能够通过共享时空注意力（人内依赖）和交叉注意力（人际依赖）机制，一次性学习两个个体运动的共同演化关系。这一范式转换直接回应了扩散模型在交互建模中的瓶颈——逐步去噪难以保证双向时空一致性。

### 2. 方法谱系中的关键设计选择

InterMask 相对于上述基线方法，在三个关键维度上做出了差异化设计：

**（1）运动 Token 表示：从 1D 序列到 2D Token 图**

传统方法（包括 InterGen 等扩散模型）通常将运动序列编码为 1D Token 序列，仅保留时间维度的结构。InterMask 引入 2D 离散运动 Token 图，通过 2D 卷积同时保留时间和空间（身体关节局部上下文）两个维度的结构信息。消融实验（Table 2）提供了决定性证据：2D Token 图的重建 FID 为 0.970，而 1D Token 图高达 3.146；MPJPE 从 0.354 降至 0.129。这表明 2D 表示显著提升了运动 VQ-VAE 的空间感知能力和重建精度，为下游交互生成奠定了更高质量的离散表示基础。

**（2）生成框架：从扩散去噪到掩蔽生成**

InterMask 采用生成式掩蔽建模替代扩散模型的逐步去噪过程。训练时，模型学习从部分掩蔽的 Token 序列中双向预测缺失 Token；推理时，采用渐进式 Token 揭示策略，通过余弦调度和置信度重掩蔽机制，在固定迭代次数（20 次）内完成生成。这一设计的关键优势在于：掩蔽建模天然支持双向上下文推理，而扩散模型的因果/逐步去噪在捕捉人际间的对称依赖关系时存在结构性劣势。

**（3）个体间交互建模：协同 Transformer 架构**

InterMask 的 Inter-M Transformer 包含三个核心注意力模块：
- **自注意力**：捕获 Token 间的通用依赖；
- **共享时空注意力**：分解为空间注意力（同一时刻内不同关节 Token 的交互）和时间注意力（同一关节跨时间的运动演化），建模人内依赖；
- **共享交叉注意力**：建模人际依赖，使两个个体的 Token 能够直接交互。

消融实验（Table 3）验证了各模块的必要性：移除时空注意力模块导致 FID 从 5.154 急剧上升至 10.968；移除交叉注意力模块使 FID 升至 11.246。协同建模（FID 5.154）相比替代的“逐一生成”建模（FID 7.637）在交互保真度上具有显著优势。这证明协同 Transformer 架构是 InterMask 性能的核心驱动力。

### 3. 适用边界与局限

InterMask 在以下场景中展现出显著优势：

- **文本条件交互生成**：在 InterHuman 和 InterX 数据集上均取得最优 FID（InterHuman: 5.154 vs. in2IN 5.535; InterX: 0.399 vs. InterGen 5.207），同时保持领先的文本对齐能力（Top-1 R-Precision 0.449 与 MoMat-MoGen 持平）。
- **反应生成**：给定一个人的运动序列，生成另一个人的合理反应。InterMask 通过保持参考个体 Token 不掩蔽、仅预测另一人 Token 的方式，自然支持该任务。
- **生成多样性**：掩蔽建模的随机掩蔽策略（$p_r=0.8$ 时取得交互与反应生成的最佳平衡）提供了天然的多样性控制机制。

然而，方法存在明确的适用边界和局限：

- **序列长度限制**：由于 Token 图采用固定尺寸设计，当前方法仅支持最长约 10 秒的运动序列。处理更长序列需要重新设计可变维度 Token 图或层次化建模方案。

- **身体穿透问题**：当输出骨架转换为 SMPL 网格时可能出现身体穿透。这是因为训练目标中未包含网格级物理约束，仅在 VQ-VAE 阶段使用了骨骼长度等几何损失。未来可探索在训练中直接引入网格转换及抗穿透损失。

- **数据集隐性偏差**：模型可能继承训练数据的偏见，例如在文本提示未明确要求舞蹈时错误生成舞蹈动作（Figure 14 第二行展示了这一失败案例）。这一问题在仅使用文本条件的情况下难以通过损失函数直接解决。

### 4. 开放问题

基于 InterMask 的局限和方法谱系中的空白，以下开放问题值得后续工作关注：

1. **长序列交互生成**：能否通过可变维度 Token 图、层次化 VQ-VAE 或时序分块策略，在保持协同建模优势的同时支持任意长度的交互生成？这需要在表示灵活性与模型复杂度之间取得平衡。

2. **物理约束的端到端集成**：如何高效地将网格转换约束（如穿透检测、接触力）嵌入生成过程，避免后处理时的身体穿透？这涉及可微分物理模拟与生成模型的深度耦合。

3. **数据集偏见的主动缓解**：如何在训练阶段识别并抑制数据集偏见，而不依赖额外的文本标注或人工审核？可能的路径包括对抗性数据增强、偏见感知的损失重加权等。

4. **推理效率的保持**：随着数据集规模增大（如 InterX 比 InterHuman 更大更多样），掩蔽生成模型在推理速度（20 次迭代）和内存消耗上相对扩散模型（通常需要更多去噪步骤）已具有优势。但如何在模型容量扩展时保持这一优势，仍需进一步研究。

5. **多人与物体交互的泛化**：当前方法聚焦于两人交互。将协同掩蔽建模框架扩展到多人（>2）或人-物交互场景，需要重新设计 Token 组织方式和注意力机制，以应对指数级增长的交互依赖关系。

## 原文 PDF

![[paperPDFs/ICLR_2025/InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Modelling.pdf]]