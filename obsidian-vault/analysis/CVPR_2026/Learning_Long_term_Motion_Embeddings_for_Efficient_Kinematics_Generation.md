---
title: Learning Long-term Motion Embeddings for Efficient Kinematics Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Learning_Long_term_Motion_Embeddings_for_Efficient_Kinematics_Generation.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Stracke_Learning_Long-term_Motion_Embeddings_for_Efficient_Kinematics_Generation_CVPR_2026_paper.html
project_link: https://compvis.github.io/long-term-motion
code_link: null
aliases:
- LTMELKG
- LLTMEEKG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过将稀疏轨迹与首帧图像编码到紧凑的长期运动嵌入（时间压缩64倍），在潜在运动空间中进行条件流匹配生成，从而将运动推理与外观解耦，大幅降低计算量。
primary_logic: 高度压缩的语义运动空间能够捕获全局运动学结构，支持稠密重建和灵活的条件生成；在此空间中学习生成模型，其效率比视频模型高数个数量级，且质量更优。
claims:
- 在 Poked 运动生成中，Ours 速度达 2500 timesteps/s，且在不同条件密度下均取得更低误差（Min, Mean, EPE），优于 Motion-I2V 等。
- 在 LIBERO 机器人任务上，Ours 成功率（79.6%/80.3%）大幅领先 ATM（60.4%）和 Tra-MoE（61.4%）。
- 与视频生成模型 Wan 和 Veo 3 相比，在样本匹配和时间匹配条件下，Ours 均获得更低的 Min MSE，且时间匹配下优势更为显著。
- 强时间压缩（至 64 倍）在保持重建保真度的同时，显著提升了运动生成质量和语义检索准确率。
---

# Learning Long-term Motion Embeddings for Efficient Kinematics Generation

> [!tip] 核心洞察
> 高度压缩的语义运动空间能够捕获全局运动学结构，支持稠密重建和灵活的条件生成；在此空间中学习生成模型，其效率比视频模型高数个数量级，且质量更优。

| 字段 | 内容 |
|------|------|
| 中文题名 | 学习长期运动嵌入以实现高效运动学生成 |
| 英文题名 | Learning Long-term Motion Embeddings for Efficient Kinematics Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Stracke_Learning_Long-term_Motion_Embeddings_for_Efficient_Kinematics_Generation_CVPR_2026_paper.html) · [Project](https://compvis.github.io/long-term-motion) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Long-term Motion Embedding (LME) for Kinematics Generation |
| Dataset | LIBERO, Video Motion, Open-Domain Poked Motion |

> [!tip] 效果简介
> - LIBERO (robotics, ATM setup) 上，Success rate (%) 79.6 vs ATM 60.4 (+19.2)。
> - LIBERO (robotics, Tra-MoE setup) 上，Success rate (%) 80.3 vs Tra-MoE 61.4 (+18.9)。
> - Video Motion (Sample Matched) 上，Min MSE 27.08 vs Wan 28.67 (-1.59)。

## 概述

**问题瓶颈**：现有运动表示方法面临两难困境。光流与稀疏轨迹等低维表示缺乏泛化能力与语境聚合能力；像素空间视频生成虽能建模复杂动态，却与外观信息高度纠缠，计算成本极高，难以支撑高效的运动推理与可控生成。这一瓶颈限制了运动学生成在实际应用中的效率与可扩展性。

**核心思路**：本文提出**长期运动嵌入（Long-term Motion Embedding, LME）**，将稀疏跟踪轨迹与首帧视觉特征编码到一个时间压缩64倍的紧凑潜在运动网格中，在解耦外观与运动的语义空间内执行条件流匹配生成。这一设计使得运动推理与生成的计算量相比视频模型降低数个数量级，同时保持甚至提升运动质量。

**主要结论**：
- **效率与质量的双重优势**：在Poked运动生成任务中，本方法推理速度达2500 timesteps/s，在不同条件密度下均取得最低误差（Min、Mean、EPE），显著优于Motion-I2V等方法（Table 1）。
- **机器人策略学习的突破**：在LIBERO基准上，本方法成功率（79.6%/80.3%）大幅领先ATM（60.4%）和Tra-MoE（61.4%），验证了运动嵌入在长时域规划中的有效性（Table 2）。
- **与视频模型的对比优势**：在样本匹配与时间匹配两种公平协议下，本方法均以更低的Min MSE优于Wan和Veo 3，且时间匹配下优势更为显著（Table 3, Table 4）。
- **时间压缩的关键作用**：消融实验表明，将时间压缩比从4倍提升至64倍，在轻微牺牲重建保真度的前提下，显著提升了运动生成质量、推理吞吐量和潜在空间的语义检索准确率（Figure 4）。

**方法定位**：本方法位于运动表示学习与生成模型的交叉点，以高度压缩的语义运动空间作为核心表征，向上承接稀疏轨迹提取（如CoTracker3），向下支撑稠密轨迹重建、条件运动生成及下游策略学习，为高效运动学生成提供了新的范式。

## 背景与动机

### 运动建模的核心瓶颈

理解并生成场景中的运动是计算机视觉与机器人领域的核心挑战。运动表征的选择直接决定了推理效率、泛化能力和生成质量。当前主流方法在运动表征上陷入两难困境：

- **低维显式表征**（如稀疏轨迹、光流）虽然计算高效，但缺乏对全局运动语境的聚合能力，难以支撑复杂的语义推理与条件生成。这类方法通常只能处理局部的、短时的运动模式，泛化能力受限。
- **高维隐式表征**（如视频像素空间）虽然信息丰富，但将运动与外观深度纠缠，导致计算开销巨大。视频生成模型在处理运动推理任务时，需要为每一帧渲染完整的像素级外观，而其中大量计算被外观建模所消耗，并非运动本身。

这一瓶颈的本质在于：**现有运动表征未能在“语义紧凑性”与“重建保真度”之间找到恰当的平衡点**。过于低维则丧失语义结构，过于高维则被外观冗余所淹没。

### 现有方法的缺口

近期工作从不同方向尝试缓解上述矛盾。**Track2Act** 等方法直接基于稀疏轨迹进行条件预测，但受限于轨迹本身的稀疏性和局部性，难以捕获长时序的全局运动语义。**Motion-I2V**（Shi et al., SIGGRAPH 2024）将运动条件注入视频生成模型，通过像素空间渲染实现运动控制，然而其推理速度受制于视频模型的高昂计算成本。在机器人领域，**ATM**（Wen et al., arXiv 2023）和**Tra-MoE**（Yang et al., CVPR 2025）利用轨迹预测辅助策略学习，但它们的运动表征仍停留在显式轨迹层面，缺乏对运动空间的语义压缩。

与此同时，大规模视频生成模型（如 **Wan**，Team Wan et al., arXiv 2025；**Veo 3**，Google DeepMind, 2025）虽然在视觉质量上取得了显著进展，但将其直接用于运动推理任务时暴露出根本性的效率缺陷：这些模型在生成第一帧的时间内，实际所需的运动信息早已可以被更紧凑的表征所捕获（见 Figure 1）。

### 本文动机与核心思路

本文的核心假设是：**存在一个高度压缩的连续运动空间，能够解耦运动与外观，同时保留全局运动学结构和语义信息**。基于这一假设，本文提出学习一种**长期运动嵌入**（Long-term Motion Embedding, LME），其关键特性包括：

1. **极端时间压缩**：将长时序运动信息压缩至 64 倍，形成紧凑的潜在运动网格（$16 \times 16$），大幅降低后续生成模型的计算负担。
2. **运动-外观解耦**：通过仅依赖稀疏跟踪轨迹和首帧语义特征（DINO 特征），将运动推理与像素级外观生成完全分离。
3. **稠密重建能力**：尽管编码过程仅使用稀疏轨迹，潜在运动网格支持在任意空间查询点重建稠密运动轨迹，实现从稀疏到稠密的泛化。

在这一学习到的运动空间中，本文进一步引入**条件流匹配生成模型**，支持通过 Poke 条件或文本条件进行可控运动生成。由于生成过程在高度压缩的潜在空间中进行，其推理效率比视频生成模型高出数个数量级，同时运动生成质量更优——这一反直觉的结果源于压缩迫使潜在空间学习更具语义性的结构化表征。

## 核心创新

本文的核心创新在于提出了一种**高度压缩的长期运动嵌入（Long-term Motion Embedding, LME）**，并在此潜在运动空间中执行条件生成，从而将运动推理与外观表征彻底解耦。相较于现有方法，该方法在三个关键维度上实现了根本性改变：

### 1. 运动表示：从稀疏轨迹到压缩潜在运动网格

传统方法要么直接操作原始稀疏轨迹（如 **Track2Act**），要么依赖稠密光流或像素空间视频生成（如 **Motion-I2V**，Shi et al., SIGGRAPH 2024）。前者缺乏泛化能力和全局语境聚合，后者则与外观信息高度纠缠且计算代价高昂。

本文的核心替换在于：通过一个 VAE 将稀疏跟踪轨迹与首帧 DINO 特征编码为一个紧凑的连续潜在运动网格（尺寸 16×16），实现 **64 倍的时间压缩**。该潜在网格将连续帧的运动信息聚合为单一潜在张量，消除了时间维度上的冗余，同时保留了全局运动学结构。解码器可根据该网格和任意查询点重建稠密轨迹，实现了从稀疏输入到稠密输出的泛化能力。

这一表示层面的改变是后续所有效率和质量提升的因果杠杆——压缩的潜在空间大幅降低了生成模型的 token 数量，使训练和推理效率提升数个数量级。

### 2. 生成空间：从像素生成到潜在运动空间的条件流匹配

现有视频生成模型（如 **Wan**，Team Wan et al., arXiv 2025；**Veo 3**，Google DeepMind, 2025）在像素空间进行生成，必须同时建模外观和运动，计算开销巨大。显式轨迹预测方法则缺乏对运动分布的整体建模能力。

本文将在潜在运动空间中执行**条件流匹配（Conditional Flow Matching）**生成。具体而言，训练一个 transformer-based 向量场预测器 $v_\phi$，学习从噪声到运动嵌入 $\mathbf{z}$ 的连续归一化流，支持 Poke 条件或文本条件控制。由于潜在空间已高度压缩且与外观解耦，生成模型可以专注于运动语义的学习，在极低计算预算下产生多样且物理合理的运动假设。

### 3. 时间压缩策略：以语义性换取效率的临界设计

传统视频模型通常采用 4-8 倍的时间压缩，而本文直接将压缩比推至 64 倍。消融实验（Figure 4）揭示了这一激进设计背后的关键权衡：

- **生成质量与吞吐量**：在固定计算预算下，更强的压缩使运动生成质量和推理吞吐量单调提升。
- **重建保真度**：仅出现轻微的下降，表明潜在空间仍保留了足够的运动细节。
- **语义结构化**：kNN 检索准确率随压缩增强而提高，证明高度压缩迫使潜在空间学习更具语义性的运动表征。

这一发现构成了本文的核心洞察：**强时间压缩不仅未损害运动建模能力，反而通过强制语义聚合提升了潜在空间的结构化程度和下游任务的效率。**

### 方法谱系与知识库定位

本文处于“运动表征学习”与“高效生成模型”的交叉点。其直接对话的基线包括：

- **运动条件视频生成**：**Motion-I2V**（Shi et al., SIGGRAPH 2024）通过视频生成实现运动迁移，但受限于像素空间的计算开销。
- **轨迹预测策略**：**Track2Act**、**ATM**（Wen et al., arXiv 2023）、**Tra-MoE**（Yang et al., CVPR 2025）直接预测稀疏轨迹用于机器人控制，但缺乏对运动分布的全局建模。
- **大规模视频生成模型**：**Wan**、**Veo 3** 在像素空间进行通用视频生成，效率瓶颈显著。

本文的独特贡献在于：通过 VAE 压缩 + 潜在空间流匹配的组合，首次在运动生成任务上同时实现了**优于视频模型的生成质量**和**数个数量级的效率提升**（Table 1 中达到 2500 timesteps/s），并在机器人操作任务（LIBERO）上取得了大幅领先的成功率（79.6% vs. ATM 60.4%）。

## 整体框架

本文提出一种以**长期运动嵌入（Long-term Motion Embedding, LME）** 为核心的运动学生成框架。其根本设计动机在于：现有运动表示要么过于低维（如稀疏轨迹、光流），缺乏泛化能力和语境聚合；要么过于高维（如视频像素），与外观信息深度纠缠且计算代价高昂。LME 框架通过将运动推理与外观生成彻底解耦，在高度压缩的潜在运动空间中完成运动建模与生成，从而在效率与质量两个维度上同时取得突破。

### 三阶段流水线

整个框架由三个功能互补的模块串联构成，形成“提取—压缩—生成”的完整闭环：

**阶段一：轨迹提取（Tracker Trajectory Extraction）**
利用现成的稠密点跟踪器（如 CoTracker3）从视频中提取稀疏点轨迹。每条轨迹被表示为归一化网格上的 $(x, y)$ 坐标序列 $\mathbf{x}_i = ([x_0, y_0], \dots, [x_{T-1}, y_{T-1}])$，其中 $x, y \in [-1, 1]$。这一步将原始视频转化为与外观无关的纯运动信号，为后续压缩提供干净的输入。

**阶段二：运动空间学习（Motion Space VAE）**
这是框架的**核心创新**。一个变分自编码器将稀疏轨迹集合与首帧图像特征（如 DINO 特征图）联合编码为紧凑的潜在运动网格 $\mathbf{z}$，时间压缩因子高达 **64 倍**。该潜在网格是一个连续的运动表示，不保留显式的时间维度——连续帧的运动信息被聚合为单个张量。解码器则根据潜在网格 $\mathbf{z}$、首帧特征 $\mathbf{f}_0$ 和任意空间查询点的起始坐标，重建这些查询点在所有时间步的稠密轨迹。训练采用 ε-VAE 目标，同时优化 L1 重建损失、掩码重建损失和 KL 正则项。

这一设计的关键因果机制在于：**极端的时间压缩迫使潜在空间学习语义化的运动结构**，而非简单地记忆逐帧坐标变化。消融实验（Figure 4）证实，随着压缩因子从 4 增至 64，运动生成质量和推理吞吐量单调提升，kNN 检索准确率同步提高，而重建保真度仅轻微下降——这表明潜在空间的语义性随压缩增强而显著改善。

**阶段三：条件运动生成（Conditional Flow Matching Generator）**
在学到的潜在运动空间中训练一个基于 Transformer 的条件流匹配模型。该模型学习从噪声 $\mathbf{z}_0$ 到真实运动嵌入 $\mathbf{z}_1$ 的向量场 $\mathbf{v}_\phi(\mathbf{z}_t, \mathbf{c}, t)$，支持两种条件模式：
- **Poke 条件**：用户指定目标位置和时间步，模型生成连接起始点与目标点的合理运动轨迹；
- **文本条件**：通过自然语言描述控制运动语义。

对于机器人应用，框架额外附加一个**策略头（Policy Head）**，以生成的运动嵌入为输入直接输出机器人动作，充当逆动力学模块。策略头维护一个滚动运动规划窗口，在每一步根据新观测更新预测。

### 输入输出流

整体数据流可概括为：
- **输入**：视频帧序列（用于轨迹提取）或单帧图像 + 条件信号（Poke 坐标 / 文本）
- **中间表示**：稀疏轨迹 → 潜在运动网格 $\mathbf{z}$（64× 时间压缩）
- **输出**：任意查询点的稠密轨迹预测，或机器人动作序列

### 效率优势的根源

框架的效率优势源于两个架构决策的叠加效应：
1. **运动-外观解耦**：生成过程完全在低维潜在运动空间中进行，无需处理高分辨率像素；
2. **极端时间压缩**：64 倍压缩将长序列运动信息浓缩为单个潜在张量，使生成模型只需处理极少量 token。

这解释了为什么在 Poked 运动生成任务中，本方法推理速度可达 **2500 timesteps/s**（Table 1），且在与视频生成模型 **Wan** 和 **Veo 3** 的时间匹配对比中，性能优势急剧扩大（Table 4）——当视频模型刚生成第一帧时，LME 已完成多条合理运动轨迹的采样（Figure 1）。

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Stracke_Learning_Long/figures/001_Figure_1.jpg]]
*Figure 1: Our approach enables extremely efficient, goal-conditioned kinematics generation and semantic motion reasoning. We achieve this by learning a dense, temporally compressed motion space that allows goal-conditioned motion generation to be orders of magnitude faster than prior video models. While a video generative model has barely produced the first frame, our method can already generate multiple plausible motion trajectories connecting the start and goal, offering both speed and interpretability*

## 核心模块与公式推导

### 3.1 运动空间 VAE：从稀疏轨迹到密集运动网格

本方法的核心在于学习一个高度压缩的长期运动嵌入（Long-term Motion Embedding，LME），其设计目标是将稀疏点轨迹与场景外观解耦，压缩为紧凑的潜在表示。该模块由一个变分自编码器（VAE）实现，包含编码器 $\mathcal{E}_\theta$ 与解码器 $\mathcal{D}_\theta$ 两部分。

**输入表示。** 一条轨迹被定义为一组归一化坐标序列，坐标值映射到 $[-1, 1]$ 区间：

$$\mathbf{x}_i = \left( [x_0, y_0], \dots, [x_t, y_t], \dots, [x_{T-1}, y_{T-1}] \right)$$

编码器接收一组稀疏轨迹 $\{(\mathbf{x}_{i,t})_{t \in \mathbf{t}}\}_{i \in \mathcal{I}}$ 以及首帧特征图 $\mathbf{f}_0$（例如 DINO 特征），将其映射为一个潜在运动网格 $\mathbf{z}$：

$$\mathcal{E}_\theta : \left( \{(\mathbf{x}_{i,t})_{t \in \mathbf{t}}\}_{i \in \mathcal{I}}, \mathbf{f}_0 \right) \mapsto \mathbf{z}$$

解码器则根据查询点 $\{\mathbf{x}_{j,0}\}_{j \in \mathcal{I}}$、潜在网格 $\mathbf{z}$ 和首帧特征 $\mathbf{f}_0$，重建任意空间位置的稠密轨迹：

$$\mathcal{D}_\theta : \left( \{\mathbf{x}_{j,0}\}_{j \in \mathcal{I}}, \mathbf{z}, \mathbf{f}_0 \right) \mapsto \{(\hat{\mathbf{x}}_{j,t})_{t \in \mathbf{t}}\}_{j \in \mathcal{I}}$$

**轨迹 Token 化与位置编码。** 每条轨迹坐标经傅里叶特征嵌入后，通过 MLP 得到 token 表示：

$$\mathrm{tok}(\mathbf{x}_{i,t}) = \mathrm{MLP}\left( [\mathcal{F}(x_t) \mid \mathcal{F}(y_t)] \right)$$

为注入时空位置信息，采用 3D 旋转位置嵌入（3D RoPE），将起始位置 $(x_0, y_0)$ 和时间 $t$ 分别编码后拼接：

$$\mathrm{PE}(\mathbf{x}_{i,t}) = \mathbf{R}(x_0) \mid \mathbf{R}(y_0) \mid \mathbf{R}(t)$$

**训练目标。** VAE 遵循 ε-VAE 训练范式，损失函数由三部分组成：L1 自编码重建损失、掩码重建损失（增强对稀疏观测的鲁棒性）以及 KL 正则项，以约束潜在空间的分布：

$$\mathcal{L} = \frac{1}{|\mathcal{T}|} \sum_{i \in \mathcal{I}} \| \mathcal{D}_\theta (\mathbf{x}_{i,0}; \mathbf{z}, \mathbf{f}_0) - \mathbf{x}_i \|_1 + \text{masked recon. term} + \beta D_{KL}(q_\theta \| p)$$

解码后的查询 token 通过一个小型 MLP 投影回 $(x, y)$ 坐标空间，得到指定查询位置的运动预测。该 VAE 实现了 **64 倍时间压缩**——将连续 $t_c$ 帧聚合为单个无时间维度的潜在表示，这是后续生成效率的关键瓶颈突破。

### 3.2 条件流匹配生成器

在获得紧凑的运动潜在空间后，本方法在该空间中训练一个条件流匹配模型，以学习从噪声到运动嵌入的向量场。生成器以文本或 Poke 条件作为控制信号，实现可控的运动合成。

**流匹配目标。** 模型 $\mathbf{v}_\phi$ 学习预测一个时变向量场，驱动样本从先验分布 $p_0$（噪声）流向数据分布 $p_1$（运动嵌入）：

$$\mathcal{L}_{\mathrm{FM}}(\phi) = \mathbb{E}_{t \sim \mathcal{U}(0,1)} \mathbb{E}_{\mathbf{z}_0, \mathbf{z}_1 \sim p_0, p_1} \left[ \| \mathbf{v}_\phi(\mathbf{z}_t, \mathbf{c}, t) - \mathbf{v}_t^* \|_2^2 \right]$$

其中 $\mathbf{z}_t$ 是沿概率路径插值的噪声潜在变量，$\mathbf{c}$ 为条件特征，$\mathbf{v}_t^*$ 为真实流场。

**实现细节。** $\mathbf{v}_\phi$ 具体实现为一个基于 Transformer 的去噪器，输入包括噪声潜在变量 $\mathbf{z}_t$、标量时间步 $t$ 以及条件特征 $\mathbf{c}$。在 Poke 条件设置下，目标 Poke 位置和时间步通过傅里叶嵌入编码（与式 (3) 类似），Poke 起始位置则使用 RoPE 编码（式 (4)）。首帧特征 $\mathbf{f}_0$ 提供场景上下文信息，确保生成的运动与场景语义一致。

### 3.3 策略头（机器人应用）

在 LIBERO 机器人任务中，模型维护一个长度为 $T$ 步的滚动运动规划。策略头以生成的运动嵌入为输入，输出机器人动作，本质上充当逆动力学模块。预测结果在每个新观测到达后更新，实现长时域闭环规划。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Stracke_Learning_Long/figures/002_Figure_2.jpg]]
*Figure 2: Our approach to learn a dense motion space. Sparse tracker trajectories and the start frame are encoded into a latent motion grid, which enables dense reconstruction at arbitrary spatial query points. The model jointly attends over trajectory tokens and frame features, producing temporally consistent, spatially dense motion predictions*

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Stracke_Learning_Long/figures/003_Figure_3.jpg]]
*Figure 3: Model architecture to generate motion space. We train a conditional flow matching model that learns a vector field over latent motion grids. We condition on either pokes [7] or text prompts, enabling controllable and semantically coherent motion synthesis in the learned motion space. The frame*

## 实验与分析

### 核心定量结果

论文在三个差异化场景中验证了长期运动嵌入（LME）的有效性：开放域 Poke 条件运动生成、机器人操作策略学习、以及与视频生成模型的分布级对比。

**Poke 条件运动生成（Table 1）。** 在从单帧出发、以稀疏点击（Poke）为条件预测未来轨迹的任务中，LME 在所有条件密度下均取得最低误差，同时推理速度达到 **2500 timesteps/s**，显著快于 Motion-I2V（Shi et al., SIGGRAPH 2024）等基线。具体而言，在 1 个 Poke 条件下，Min MSE 为 41.0，EPE 为 0.5；当条件密度增至 Dense 时，Min MSE 降至 30.4，EPE 为 1.1。Track2Act 仅支持终点条件，因此仅在 Dense 条件下报告结果，其 Min MSE 为 32.5，EPE 为 1.4，均劣于 LME。这一结果验证了核心论断：在高度压缩的潜在运动空间中执行条件生成，既能保持精度，又能获得数量级的效率增益。

**机器人操作策略学习（Table 2）。** 在 LIBERO 基准上，LME 生成的轨迹嵌入作为策略头的条件输入，在 ATM（Wen et al., arXiv 2023）和 Tra-MoE（Yang et al., CVPR 2025）两套评估协议下分别取得 **79.6%** 和 **80.3%** 的成功率，较对应基线提升 **+19.2** 和 **+18.9** 个百分点。该实验严格遵循基线的训练与评估设置，排除了数据或超参数差异的干扰。性能飞跃表明，运动嵌入所捕获的长期运动学结构对下游决策具有强迁移价值——策略头无需从原始像素或稀疏轨迹中重新学习运动表征。

**与视频生成模型的对比（Table 3, Table 4）。** 为公平评估效率优势，论文设计了两种对比协议：
- **样本匹配（Sample Matched）**：双方各采样 8 次。LME 的 Min MSE 为 **27.08**，优于 Wan（28.67）和 Veo 3（36.18）。此时 LME 模型规模远小于视频模型，属于对 LME 不利的设置，但仍取得领先。
- **时间匹配（Time Matched）**：双方在相同墙钟时间内采样。LME 的 Min MSE 降至 **21.29**，而 Wan 升至 64.20，差距扩大至 **-42.91**。这直接归因于 LME 在 64 倍时间压缩下极低的单次推理成本。

### 消融实验：时间压缩的关键作用

Figure 4 展示了时间压缩因子对系统性能的系统性影响。在固定计算预算下，压缩因子从 4 增至 64 时：

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Stracke_Learning_Long/figures/004_Figure_4.jpg]]
*Figure 4: Temporal compression enables our model to generate plausible motions more efficiently. Under a fixed compute budget, both motion generation quality and inference throughput improve substantially with stronger compression (left), with only a minor reduction in reconstruction fidelity (middle). We attribute these gains to the reduced token count, which improves training efficiency, and to an increasingly semantic latent structure, as evidenced by higher kNN retrieval accuracy (right)*

1. **运动生成质量与推理吞吐量单调提升**。压缩程度越高，生成模型所需处理的 token 数越少，训练和推理效率同步改善。
2. **重建保真度仅轻微下降**。这说明 VAE 能够在极高压缩比下保留足够的运动学信息以支持稠密轨迹重建。
3. **kNN 检索准确率持续提高**。这表明强压缩迫使潜在空间学习更具语义性的结构化表征，而非记忆表面运动模式。

这一消融揭示了方法设计的因果链条：时间压缩并非简单的效率取舍，而是通过减少 token 数量提升训练效率、同时诱导语义潜在结构形成的双重增益机制。

### 定性分析

Figure 5 展示了从单帧生成老鹰飞行的多种合理运动假设，说明学习到的运动空间具有表达多样、物理一致的复杂运动的能力。Figure 6 进一步展示了路径寻找、旋转运动等多种运动推理能力，证明模型捕获了语义运动结构并能泛化至不同运动模式。Figure 7 展示了 LIBERO 回放中的轨迹预测，模型向前预测 16 步轨迹，策略头据此选择动作，并在每次新观测后更新预测，支撑长时域规划。

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Stracke_Learning_Long/figures/005_Figure_5.jpg]]
*Figure 5: Example of multiple plausible motion hypotheses for the flight of an eagle, generated by our model from a single start frame. Our model produces diverse, physically coherent motions even in complex natural scenes, illustrating the expressiveness of the learned motion space*

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Stracke_Learning_Long/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative examples demonstrating diverse motion reasoning capabilities. These results highlight that the model captures semantic motion structure and generalizes to varied motion regimes*

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Stracke_Learning_Long/figures/009_Figure_7.jpg]]
*Figure 7: LIBERO rollout samples. Our track predictor forecasts tracks 16 steps ahead (visualized), enabling long-horizon planning. A policy head conditions on these predictions to select the next actions, with predictions updated after every new observation*

### 需要人工验证的边界

分析材料未提供明确的失败模式讨论或系统性的错误分析。以下问题需读者结合原文进一步确认：该方法对跟踪器（如 CoTracker3）质量的依赖程度——稀疏轨迹错误是否会在运动嵌入中累积？运动空间能否处理含有剧烈摄像机运动或遮挡的场景？运动嵌入与外观生成模型结合时的保真度如何？在未见过的物体类别或复杂人-物交互场景下的泛化表现如何？

### 补充图表

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Stracke_Learning_Long/figures/006_Table_1.jpg]]
*Table 1: Poked Motion Generation. We compare against other methods that were trained on general video data and predict an explicit motion representation for multiple time steps. We report metrics for different conditioning densities to assess how well these models perform under varying levels of uncertainty. Track2Act [6] is end frame conditional, which is why we only report numbers for the dense case. Our approach outperforms other models while also being significantly faster*

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Stracke_Learning_Long/figures/008_Figure.jpg]]
*Figure: (a) Turn on the stove and put the moka pot on it (b) Put the yellow-and-white mug in the microwave and close it*

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Stracke_Learning_Long/figures/010_Table_3.jpg]]
*Table 3: Samples Matched: We sample k = 8 times from each model and track the generated videos to report our distributional metrics as well as conditioning adherence with EPE. This is an unfavorable setting for us, as our model is much smaller. Still, we outperform the video while being orders of magnitude faster*

![[assets/figures/papers/paper_list_l20_https_openaccess_thecvf_com_content_CVPR2026_html_Stracke_Learning_Long/figures/011_Table_4.jpg]]
*Table 4: Time Matched: Setup similar to Tab. 3 but now matching wall clock time for sampling. Our performance lead increases drastically due to the efficiency of our approach*

## 方法谱系与知识库定位

### 1. 核心瓶颈与因果调节变量

现有运动推理与生成方法面临一个根本性的表示瓶颈：低维表示（如稀疏轨迹、光流）缺乏泛化所需的语境聚合能力，无法捕获全局运动学结构；高维表示（如视频像素）则与外观信息高度纠缠，导致计算代价高昂且难以进行语义层面的运动操控。本文的核心因果调节变量在于**运动表示的空间**——通过将稀疏轨迹与首帧图像编码到时间压缩 64 倍的连续潜在运动网格中，该方法将运动推理与外观生成彻底解耦，从而在潜在运动空间中实现高效的条件生成。

这一设计形成了清晰的因果链：高度压缩的语义运动空间 → 捕获全局运动学结构 → 支持稠密重建与灵活条件生成 → 生成效率比视频模型高数个数量级，且质量更优。该因果链在消融实验中得到验证：时间压缩因子从 4 增至 64 时，运动生成质量和推理吞吐量单调提升，kNN 检索准确率同步提高，表明潜在空间的语义性随压缩增强而增强（Figure 4）。

### 2. 方法演进脉络与基线关系

**轨迹预测与运动条件生成**：早期工作如 **Track2Act** 直接基于稀疏轨迹进行端帧条件预测，但受限于显式轨迹空间的表达能力。**Motion-I2V**（Shi et al., SIGGRAPH 2024）将运动条件注入视频生成管线，通过像素空间生成实现运动控制，但计算开销巨大且运动与外观仍然耦合。本文方法在运动表示层面进行了根本性重构——将稀疏轨迹提升为连续潜在运动网格，使生成过程完全在低维语义空间中进行，从而在 Poked 运动生成任务上以 2500 timesteps/s 的速度显著超越 Motion-I2V，且在不同条件密度下均取得更低的 Min、Mean 和 EPE 误差（Table 1）。

**机器人策略学习**：**ATM**（Wen et al., arXiv 2023）和 **Tra-MoE**（Yang et al., CVPR 2025）分别代表了基于轨迹的机器人策略学习范式。ATM 直接利用轨迹预测进行动作规划，Tra-MoE 则引入多领域轨迹预测策略。本文方法在完全遵循两者训练与评估设置的条件下，在 LIBERO 基准上分别取得 79.6%（vs ATM 60.4%）和 80.3%（vs Tra-MoE 61.4%）的成功率，提升幅度达 19.2 和 18.9 个百分点（Table 2）。这一显著差距的核心原因在于：长期运动嵌入通过 64 倍时间压缩聚合了全局运动语境，使策略头能够基于更丰富的运动语义进行决策，而非依赖局部轨迹片段。

**视频生成模型**：与 **Wan**（Team Wan et al., arXiv 2025）和 **Veo 3**（Google DeepMind, 2025）等大型视频生成模型的对比尤为关键。在样本匹配（Sample Matched）设置下，本文方法以更小的模型规模取得更低的 Min MSE（27.08 vs Wan 28.67, Veo 3 36.18）；在时间匹配（Time Matched）设置下，优势急剧扩大（21.29 vs Wan 64.20），充分验证了在潜在运动空间中生成比在像素空间中生成具有根本性的效率优势（Table 3, Table 4）。

### 3. 方法适用边界

**对跟踪器质量的依赖**：该方法以现成跟踪器（如 CoTracker3）提取的稀疏轨迹作为输入，因此跟踪器在遮挡、运动模糊或剧烈光照变化下的失效会直接传导至运动嵌入的质量。当前论文未提供跟踪器鲁棒性的系统消融，这一依赖程度需要进一步验证。

**场景适用范围**：运动空间 VAE 的训练基于大规模视频数据中的轨迹统计，其泛化能力受限于训练分布。对于含有剧烈摄像机运动、长时间完全遮挡或非刚性形变的场景，潜在运动网格是否仍能保持稠密重建的精度尚不明确。

**与外观生成的衔接**：该方法将运动与外观解耦是其效率优势的来源，但也意味着完整的视频合成需要额外的外观生成模块。论文未讨论运动嵌入如何与外观生成模型（如扩散模型或神经渲染管线）对接，这是一个待解决的关键接口问题。

### 4. 开放问题

1. **跨类别泛化**：长期运动嵌入在未见过的物体类别或复杂人-物交互场景下的泛化能力如何？运动空间的语义结构是否具有类别无关的普适性？

2. **多模态条件融合**：当前方法支持 Poke 和文本条件，但两种条件的融合机制及其在冲突条件下的行为未充分探索。如何实现更精细的多模态运动控制？

3. **闭环策略的稳定性**：在机器人任务中，策略头以生成的运动嵌入为输入进行动作选择。滚动规划（rolling motion plan）机制在长时间跨度下的误差累积特性需要更系统的分析。

4. **运动空间的可解释性**：kNN 检索准确率的提升暗示潜在空间具有语义结构，但该空间的具体几何性质和可操控维度尚未被系统刻画。是否存在对应于特定运动原语（如旋转、平移、形变）的可解释潜在方向？

5. **与物理仿真的结合**：生成的运动轨迹是否满足物理约束（如刚体运动学、碰撞避免）？将物理先验融入运动空间学习或作为后处理约束可能进一步提升生成质量。

## 原文 PDF

![[paperPDFs/CVPR_2026/Learning_Long_term_Motion_Embeddings_for_Efficient_Kinematics_Generation.pdf]]
