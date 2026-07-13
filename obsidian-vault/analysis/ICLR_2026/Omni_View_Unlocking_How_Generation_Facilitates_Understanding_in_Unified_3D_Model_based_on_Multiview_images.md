---
title: "Omni-View: Unlocking How Generation Facilitates Understanding in Unified 3D Model based on Multiview images"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Omni_View_Unlocking_How_Generation_Facilitates_Understanding_in_Unified_3D_Model_46bff9ed5dad.pdf
project_link: "https://openai.com/index/hello-gpt-4o"
code_link: "https://github.com/AIDC-AI/Omni-View"
aliases:
- OV
- Omni-View
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 联合训练理解模型与生成模型（纹理模块+几何模块），通过自回归生成和深度/姿态估计任务迫使模型学习几何和时空表示，从而直接提升三维场景理解性能。
primary_logic: “生成促进理解”：通过双模块架构（纹理模块处理外观合成，几何模块处理深度和姿态），利用共享的多模态自注意力，将生成过程中习得的几何约束和时空一致性注入理解模型，实现理解与生成能力的协同增长。
claims:
- Omni-View 在 VSI-Bench 上平均得分 55.4，超过所有现有方法，表明生成能力显著增强空间推理。
- 与微调的 BAGEL-7B 相比，在 SQA3D 上 EM 提升 2 点，在 ScanQA 上 CIDEr 提升 7.5，验证了所提架构和训练策略的有效性。
- 消融实验表明，几何模块的引入显著提升了需要相对位置信息的任务（如相对距离），纹理模块的自回归生成提升了时空建模任务（如外观顺序）。
- 生成任务（新颖视图合成和场景生成）达到领先水平，PSNR 和 SSIM 最高，LPIPS 最低，且保持理解性能不降。
---

# Omni-View: Unlocking How Generation Facilitates Understanding in Unified 3D Model based on Multiview images

> [!tip] 核心洞察
> “生成促进理解”：通过双模块架构（纹理模块处理外观合成，几何模块处理深度和姿态），利用共享的多模态自注意力，将生成过程中习得的几何约束和时空一致性注入理解模型，实现理解与生成能力的协同增长。

| 字段 | 内容 |
|------|------|
| 中文题名 | Omni-View：探究生成如何促进基于多视角图像的统一三维模型中的理解 |
| 英文题名 | Omni-View: Unlocking How Generation Facilitates Understanding in Unified 3D Model based on Multiview images |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=pDu6u9cnEB) · [Code](https://github.com/AIDC-AI/Omni-View) · [Project](https://openai.com/index/hello-gpt-4o) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Omni-View |
| Dataset | SQA3D, ScanQA, VSI-Bench, Re10k |

> [!tip] 效果简介
> - SQA3D (test) 上，EM 59.2 vs 57.2 (BAGEL-7B-FT) (+2.0)。
> - ScanQA (val) 上，CIDEr 103.0 vs 95.5 (BAGEL-7B-FT) (+7.5)。
> - VSI-Bench 上，整体平均得分 55.4 vs 48.4 (SpatialMLLM-4B) (+7.0)。

## 概要

三维场景理解与生成长期被视为两个独立任务：理解模型依赖显式的三维输入（如点云、体素），而生成模型则专注于纹理合成，缺乏对三维空间关系的显式度量。这种割裂导致统一的多模态模型在空间推理、相对距离判断等任务上表现受限——仅靠纹理生成不足以构建完整的几何认知。

Omni-View 的核心洞察是“生成促进理解”：通过将生成过程拆解为纹理与几何两个独立模块，让模型在合成新颖视图的同时显式地估计深度图和相机姿态，从而将生成过程中习得的几何约束与时空一致性注入理解模型，实现两种能力的协同增长。

具体而言，Omni-View 在统一基线 **BAGEL-7B** 的基础上做出四项关键改动：
1. **双模块生成架构**：纹理模块负责外观合成，几何模块负责深度与相机姿态估计，两者通过共享的多模态自注意力机制交互。
2. **自回归生成框架**：采用 Diffusion Forcing 与稠密到稀疏（D2S）的参考图像课程，强制模型学习时序依赖关系。
3. **显式几何监督**：引入深度噪声 MSE 损失与相机姿态 Huber 损失，并将理解模型特征通过交叉注意力注入几何模块。
4. **两阶段训练**：阶段一联合训练理解与生成，阶段二冻结理解模型，用 RGB-Depth-Pose 联合学习精调生成模型。

实验表明，Omni-View 在空间推理基准 **VSI-Bench** 上以平均 55.4 分排名第一，显著超过现有方法；在 **SQA3D** 上 EM 提升 2 点，在 **ScanQA** 上 CIDEr 提升 7.5。消融实验进一步验证：纹理模块的自回归生成使外观顺序任务提升 4.1 点，几何模块使相对距离等任务显著改善，而 D2S 训练策略对理解性能的贡献超过类似 Ross3D 的视觉重建方法。同时，Omni-View 在新颖视图合成与场景生成任务上取得了最高的 PSNR 和 SSIM，且保持理解性能不降，证实了“生成促进理解”范式的有效性。

三维场景理解是实现具身智能与环境交互的核心能力，要求模型能够同时处理多视角图像、理解空间关系并回答复杂查询。近年来，多模态大语言模型（MLLM）在二维视觉推理上取得了显著进展，但在三维场景理解中仍面临根本性瓶颈：**统一多模态模型缺乏显式的几何度量和时空建模能力，仅依靠纹理生成不足以完全理解三维空间关系**。

现有工作大致分为两类。一类是任务特定的三维理解模型，如 **SpatialMLLM-4B** 和 **VG-LLM-4B**，它们针对单一任务设计，缺乏跨任务的泛化能力。另一类方法直接使用三维点云或体素作为输入，如 **Video3DLLM**（Zheng et al., 2025）和 **LLaVA-3D**（Zhu et al., 2025），虽然利用了几何先验，但依赖昂贵的3D传感器数据，限制了实际部署的灵活性。基于多视图图像的统一模型 **BAGEL-7B-FT**（Deng et al., 2025）试图弥合这一差距，但其生成模块仅包含为RGB图像设计的纹理生成组件，缺少对深度、相机姿态等几何信息的显式建模，导致空间推理能力不足。

本文的核心洞察是 **“生成促进理解”**：通过将生成模型拆分为纹理模块与几何模块，利用自回归生成和深度/姿态估计任务迫使模型学习几何约束和时空一致性，并将这些从生成中习得的表示注入理解模型，实现理解与生成能力的协同增长。Omni-View 正是基于这一思想，在 BAGEL 的基础上引入双模块生成架构与两阶段训练策略，首次在多视图图像的统一框架下验证了生成能力对三维理解的促进作用。

## 核心方法与创新机理

Omni-View 的核心创新在于通过**“生成促进理解”**的机制，首次在统一多模态模型中显式引入几何与时空约束，从而突破现有方法在三维场景理解中的瓶颈。其关键设计围绕**双模块生成架构**与**两阶段训练策略**展开。

### 1. 双模块生成架构：纹理与几何的解耦

与基线模型 **BAGEL**（Deng et al., 2025）仅包含单一纹理生成模块不同，Omni-View 将生成模型拆分为两个功能独立的模块：

- **纹理模块**：负责外观合成，基于参考图像、文本描述和目标相机姿态，通过流匹配（flow matching）自回归地生成新颖视图的 RGB 图像。
- **几何模块**：负责几何重建，从纹理模块的潜在输出和理解模型的中间特征中，同时估计新颖视图的深度图和相机内外参。

这一解耦设计的因果机制在于：纹理模块专注于外观和时序建模，而几何模块则迫使模型学习显式的三维空间关系。消融实验证实，分离两个模块（相较于共享参数的统一架构）能显著提升理解性能——纹理模块使外观顺序（Appr. Order）任务提升 4.1 点，几何模块则显著改善相对距离（Rel. Dist.）等需要位置信息的任务。

### 2. 几何监督的显式注入

Omni-View 在训练中引入了明确的几何估计任务，这是相较于 BAGEL 等无几何监督方法的根本性改变。几何模块的损失函数由深度噪声 MSE 损失和相机姿态 Huber 损失共同构成：

$$L_{geo} = ||F_{dep} - N_{dep}||_2 + ||\hat{g} - g_{gt}||_{\epsilon}$$

同时，理解模型的特征通过交叉注意力机制注入几何模块，使理解过程中习得的语义信息能够直接指导几何推理。这种设计使得生成过程中习得的几何约束能够反向促进理解模型的空间推理能力。

### 3. 自回归生成与稠密到稀疏训练策略

为强化时空建模能力，Omni-View 采用**自回归生成框架**配合 **Diffusion Forcing** 机制，并设计了**稠密到稀疏（Dense-to-Sparse, D2S）**的参考图像课程学习策略：训练初期提供全部参考图像，随后逐步减少参考帧数量，迫使模型学习时序依赖关系。

消融实验表明，自回归生成（相较于无生成训练）使绝对距离（Abs. Dist.）任务提升 5.8 点，外观顺序提升 4.4 点。D2S 策略对理解性能的提升至关重要，其效果显著超过 **Ross3D** 中采用的随机掩码视觉重建方法。

### 4. 两阶段训练：理解与生成的协同优化

Omni-View 采用两阶段训练策略，实现理解与生成的协同增长：

- **阶段一**：联合训练理解模型、纹理模块和几何模块，采用 D2S 课程策略，使生成任务中习得的几何和时空表示直接促进理解能力。
- **阶段二**：冻结理解模型，使用 RGB-Depth-Pose（RGBDP）联合学习精调生成模型。虽然阶段二未进一步提升理解性能，但将场景生成 PSNR 从 21.44 提升至 22.93，验证了联合几何学习对生成质量的有效性。

### 5. 创新总结

Omni-View 的创新本质在于：通过**双模块架构**将纹理生成与几何估计解耦，利用**自回归生成和 D2S 训练**注入时空约束，再通过**共享多模态自注意力**将这些生成过程中习得的几何与时空表示注入理解模型，最终实现“生成促进理解”的协同效应。这一设计使 Omni-View 在不依赖三维场景输入的条件下，在 VSI-Bench 空间推理基准上达到 55.4 的平均得分，超越所有现有方法。

Omni-View 的整体框架以 BAGEL 的统一多模态理解-生成架构为基础，将其扩展至基于多视角图像的三维场景。如图 1 所示，系统由**理解模型**和**生成模型**两大组件构成，而生成模型又被进一步拆分为两个功能专一的模块：**纹理模块**和**几何模块**。这种“理解-生成”双体架构的核心设计理念是“生成促进理解”——通过让生成模型显式地学习几何与时空约束，并将这些约束通过特征交互注入理解模型，从而实现两类能力的协同增长。

**理解模型**负责执行三维场景或空间理解任务，包括问答、定位和推理。它接收多视图图像和文本查询作为输入，并输出中间特征供几何模块使用。

**纹理模块**承担新颖视图合成任务。它基于参考图像、文本描述和目标相机姿态，采用流匹配的自回归生成框架预测目标视图的 RGB 图像。其前向过程可表示为：

$$F_{tex} = TextureModule([LM\text{-}Head(\tau(T_{des})); [\varepsilon(I_{ref}); N_{tex}] + r])$$

其中 $F_{tex}$ 为预测的图像噪声，$T_{des}$ 为文本描述，$I_{ref}$ 为参考图像，$N_{tex}$ 为随机输入噪声，$r$ 为普吕克射线编码提供的相机姿态信息。

**几何模块**从纹理模块的潜在输出和理解模型的特征中，同时估计新颖视图的深度图和相机内外参：

$$[F_{dep}; \hat{g}] = GeometryModule([F_{tex}; N_{dep}; q_{cam}], F_{und})$$

其中 $F_{dep}$ 为预测的深度噪声，$\hat{g}$ 为估计的相机参数，$F_{und}$ 为理解模型提供的中间特征，通过交叉注意力机制注入几何模块。

三个模块通过共享的多模态自注意力机制进行信息交换，纹理模块习得的外观合成能力与几何模块习得的深度/姿态估计能力共同反哺理解模型，从而提升其空间推理性能。训练采用两阶段策略：阶段一联合训练三个模块并采用稠密到稀疏的参考图像课程，阶段二冻结理解模型以 RGB-Depth-Pose 联合学习精调生成模型。

![[assets/figures/papers/paper_list_l54_https_openreview_net_forum_id_pDu6u9cnEB/figures/001_Figure_1.jpg]]
*Figure 1: Architecture of Omni-View. Building upon Bagel (Deng et al., 2025), Omni-View consists of an understanding model and a generation model. The generation model is further composed of two specialized modules: one for texture and one for geometry. Trained via a two-stage process, Omni-View shows high effectiveness in scene understanding and novel view synthesis. Crucially, it unlocks the benefits of its generative capabilities to enhance the model’s understanding performance*

### 理解模型 (Understanding Model)

理解模型是 Omni-View 的基础骨干，基于 **BAGEL** (Deng et al., 2025) 构建。它接收多视图图像和文本查询，负责执行三维场景或空间理解任务，包括问答、定位和推理。在 Omni-View 的架构中，理解模型不仅输出文本回答，还产生中间特征 $F_{und}$，该特征通过交叉注意力机制注入几何模块，为几何估计提供语义和空间上下文。

### 纹理模块 (Texture Module)

纹理模块负责新颖视图的外观合成。它采用基于流匹配 (Flow Matching) 的自回归生成框架，并配合 **Diffusion Forcing** 技术进行训练。其核心机制是将文本描述、参考图像编码和随机噪声融合，并通过普吕克射线编码 (Plücker-Ray Encoding) 注入相机姿态信息。

纹理模块的前向过程可形式化为：

$$F_{tex} = \text{TextureModule}([\text{LM-Head}(\tau(T_{des})); [\varepsilon(I_{ref}); N_{tex}] + r])$$

其中：
- $T_{des}$ 为目标视图的文本描述，$\tau$ 为文本编码器，$\text{LM-Head}$ 将其映射到模型隐空间。
- $I_{ref}$ 为参考图像集合，$\varepsilon$ 为图像编码器。
- $N_{tex}$ 为随机采样的输入噪声。
- $r$ 为普吕克射线编码，用于提供目标视图的相机姿态信息。普吕克射线编码定义为 $\boldsymbol{r}_{i,j} = (o \times d, d)$，其中 $o$ 和 $d$ 分别表示射线的原点和方向，$(i, j)$ 为像素坐标。
- $F_{tex}$ 为纹理模块预测的图像噪声。

纹理模块的损失函数为标准均方误差：

$$L_{tex} = ||F_{tex} - N_{tex}||_2$$

### 几何模块 (Geometry Module)

几何模块是 Omni-View 区别于 BAGEL 等纯纹理生成模型的关键创新。它从纹理模块的潜在输出和理解模型的特征中，同时估计新颖视图的深度图和相机内外参。

几何模块的前向过程为：

$$[F_{dep}; \hat{g}] = \text{GeometryModule}([F_{tex}; N_{dep}; q_{cam}], F_{und})$$

其中：
- $F_{tex}$ 为纹理模块的潜在输出，提供外观合成的中间表示。
- $N_{dep}$ 为深度噪声，用于流匹配去噪。
- $q_{cam}$ 为可学习的相机查询 (learnable camera query)，用于估计相机姿态。
- $F_{und}$ 为理解模型产生的中间特征，通过交叉注意力注入几何模块，提供语义指导。
- $F_{dep}$ 为预测的深度噪声。
- $\hat{g}$ 为预测的相机内外参。

几何模块的损失函数由两部分组成：

$$L_{geo} = ||F_{dep} - N_{dep}||_2 + ||\hat{g} - g_{gt}||_{\epsilon}$$

其中第一项为深度噪声的均方误差损失，第二项为相机姿态的 Huber 损失 ($||\cdot||_{\epsilon}$)，$g_{gt}$ 为真实相机参数。

### 理解模型损失

理解模型采用标准的下一个 token 预测损失进行训练：

$$L_{und} = -\sum_{i=1}^{T} \log P_{\theta}(y_i | y_{<i})$$

其中 $y_i$ 为第 $i$ 个目标 token，$T$ 为序列长度，$\theta$ 为模型参数。

### 模块协同机制

Omni-View 的核心设计在于纹理模块与几何模块的分离。消融实验表明，将两个模块分离（而非共享参数的统一模块）显著提升了三维理解性能：纹理模块的自回归生成提升了时空建模任务（如外观顺序提升 4.1 点），几何模块的引入则显著增强了需要相对位置信息的任务（如相对距离）。这种“生成促进理解”的机制，通过共享的多模态自注意力，将生成过程中习得的几何约束和时空一致性注入理解模型，实现理解与生成能力的协同增长。

![[assets/figures/papers/paper_list_l54_https_openreview_net_forum_id_pDu6u9cnEB/figures/031_Figure_4.jpg]]
*Figure 4: Architecture of understanding model and texture module*

![[assets/figures/papers/paper_list_l54_https_openreview_net_forum_id_pDu6u9cnEB/figures/032_Figure_5.jpg]]
*Figure 5: Architecture of geometry module in two stages*

## 实验与关键发现

### 核心实验结果

Omni-View 在三维场景理解、空间推理和生成任务上均展现出显著优势，验证了“生成促进理解”的核心假设。

**三维场景理解。** 在 SQA3D 测试集上，Omni-View 的 Exact Match (EM) 达到 59.2，相比微调后的统一基线模型 **BAGEL-7B-FT**（Deng et al., 2025）提升 2.0 点，且超越所有不依赖三维点云输入的 MLLM 方法（如 SpatialMLLM-4B 的 55.9）。在 ScanQA 验证集上，CIDEr 得分达到 103.0，较 BAGEL-7B-FT 的 95.5 提升 7.5 点，较 SpatialMLLM-4B 提升 11.2 点。值得注意的是，Omni-View 仅以多视角图像为输入，其性能已与使用三维场景输入的 **Video3DLLM**（Zheng et al., 2025）和 **LLaVA-3D**（Zhu et al., 2025）相当，表明生成模块习得的几何与时空表示有效弥补了显式三维输入的缺失。

**空间推理。** 在 VSI-Bench 空间推理基准上，Omni-View 以 55.4 的平均得分排名第一，显著超越 SpatialMLLM-4B（48.4）和 VG-LLM-4B 等任务特定模型。该基准涵盖房间尺寸估计、外观顺序判断、物体相对距离等子任务，Omni-View 的全面领先表明其空间推理能力并非局限于单一维度。

**生成任务。** 在 Re10k 数据集上，Omni-View 在新颖视图合成（单视图输入）和场景生成两项任务中均取得最高 PSNR 和 SSIM，以及最低 LPIPS。具体而言，新颖视图合成 PSNR 达 23.22（Voyager-13B 为 23.12），场景生成 PSNR 达 23.12（Voyager-13B 为 22.93）。生成质量的提升并未以牺牲理解为代价，体现了双模块架构的协同优势。

### 消融研究

消融实验系统性地揭示了各设计选择的因果贡献。

**生成模块结构分离。** Table 4 显示，将生成模型拆分为独立的纹理模块和几何模块（相较于共享参数的统一架构）显著提升了三维理解性能。纹理模块的引入使外观顺序（Appr. Order）任务提升 4.1 点，几何模块则显著改善了依赖相对位置信息的任务（如相对距离 Rel. Dist.）。这证实了两类生成信号对理解能力具有互补且不可相互替代的增益。

**自回归生成机制。** Table 5 表明，在阶段一训练中引入自回归生成（相较于仅训练理解模型）显著提升了时空相关任务：绝对距离（Abs. Dist.）提升 5.8 点，外观顺序提升 4.4 点。这一发现直接支持了核心因果链条——自回归生成迫使模型学习时序依赖，从而增强时空建模能力。

**稠密到稀疏（D2S）训练策略。** Table 6 对比了 D2S 策略与固定所有参考图像及随机掩码（类似 **Ross3D** 的视觉重建方法，Wang et al., 2025a）的效果。D2S 显著提升理解性能，且效果优于随机掩码方案，验证了逐步减少参考信息的课程学习策略对强迫模型内化几何与外观规律的关键作用。

**阶段二训练。** Table 7 显示，阶段二（冻结理解模型，仅精调生成模型）虽未进一步提升理解性能，但将场景生成 PSNR 从 21.44 提升至 22.93，确认了 RGB-Depth-Pose 联合学习的有效性。这一阶段的收益集中于生成质量，实现了理解与生成的解耦优化。

### 失败模式与局限性

尽管整体表现优异，Omni-View 在以下方面存在明显局限：

1. **定位能力待验证。** 论文明确指出模型的 grounding 能力仍有待评估，这限制了其在需要精确物体定位的下游任务中的直接应用。
2. **长距离生成能力不足。** 生成模型目前缺乏长距离世界生成能力，在大基线运动的室外场景中，生成结果易出现伪影，相机控制精度和帧间纹理一致性需进一步改进。
3. **几何预测精度受限。** 几何模块的训练数据为合成深度图，其在实际场景中的几何预测精度可能不够精确，这从深度估计可视化结果（Figure 中室内场景优于室外场景）中可得到印证。
4. **训练稳定性问题。** 阶段二训练中，几何损失权重 λ_geo 的调节可能影响训练稳定性，论文将此列为开放问题。

### 关键图表结论

- **Table 1** 与 **Table 2**：Omni-View 在不使用三维输入的方法中全面领先，且空间推理能力（VSI-Bench 55.4）显著超越所有现有 MLLM。
- **Table 3**：生成质量达到领先水平，且理解性能不降，验证了双模块架构的协同设计。
- **Table 4–6**：纹理模块与几何模块的分离、自回归生成、D2S 训练策略各自对特定类型的理解任务产生可量化的增益，且增益方向与理论预期一致。
- **Figure 6**（激活图对比）：Omni-View 与 BAGEL-FT 的激活图差异直观展示了生成训练对理解模型内部表示的重塑效应。

![[assets/figures/papers/paper_list_l54_https_openreview_net_forum_id_pDu6u9cnEB/figures/002_Table_1.jpg]]
*Table 1: Evaluation of 3D scene understanding. “–” indicates the number is not available for us. Bold and underline denote the best and second-best models without 3D scene input, respectively. For ScanRefer, the content in “()” indicates results without proposal refinement (Zhang et al., a)*

![[assets/figures/papers/paper_list_l54_https_openreview_net_forum_id_pDu6u9cnEB/figures/005_Table_4.jpg]]
*Table 4: Ablation on modules in the generation model. The gray row denotes that, in this experiment, both the texture module and the geometry module use the same architecture and parameters*

> **手动验证提示**：部分基线方法（如 SpatialMLLM-4B、VG-LLM-4B）的引用信息在分析数据中缺失，建议核对原文参考文献后补充。

![[assets/figures/papers/paper_list_l54_https_openreview_net_forum_id_pDu6u9cnEB/figures/006_Table_5.jpg]]
*Table 5: Ablation on the autoregressive generation in stage 1. “None” means we only train understanding model in this experiment*

## 定位与知识库关联

### 1. 基线关系与差异化贡献

Omni-View 直接构建于统一多模态模型 **BAGEL**（Deng et al., 2025）之上，其核心差异化在于将 BAGEL 中单一的 RGB 纹理生成模块拆分为纹理与几何两个独立模块，并引入自回归生成框架与稠密到稀疏（D2S）的参考图像课程策略。这一改动并非简单的结构扩展，而是通过几何监督（深度图估计、相机姿态估计）将显式的三维空间约束注入原本仅依赖外观建模的统一框架，从而实现了“生成促进理解”的核心洞察。

在与任务特定三维理解模型的对比中，Omni-View 展现出统一架构的竞争力。在不依赖三维场景输入（如点云、体素）的方法中，Omni-View 在 SQA3D 测试集上以 59.2 EM 超越 **SpatialMLLM-4B** 达 3.3 点，在 ScanQA 验证集上以 103.0 CIDEr 超越 **SpatialMLLM-4B** 达 11.2 点（Table 1）。即使与使用三维输入的 **Video3DLLM**（Zheng et al., 2025）和 **LLaVA-3D**（Zhu et al., 2025）相比，Omni-View 也取得了可比的性能，表明其从多视角图像中习得的几何表征已能部分弥补显式三维输入的缺失。

在生成能力方面，Omni-View 在 Re10k 数据集上的新颖视图合成（PSNR 23.22）和场景生成（PSNR 23.12）均超越了任务特定的场景生成模型 **Voyager-13B**（Huang et al., 2025），且未牺牲理解性能。这验证了双模块架构在理解与生成任务间的正向迁移效应。

### 2. 适用边界与局限

尽管 Omni-View 在室内场景理解与生成上表现突出，其适用边界受以下因素制约：

- **定位能力未充分验证**：论文明确指出现有评估尚未覆盖精细的三维定位任务，该能力有待进一步检验。
- **几何精度受限于合成数据**：几何模块的训练依赖合成深度图，其在实际场景中的几何预测精度可能不足，这限制了模型在需要精确度量（如机器人抓取、精密测量）场景中的直接部署。
- **大基线运动下的生成退化**：在相机运动幅度较大的室外场景中，生成结果易出现伪影，相机控制精度和帧间纹理一致性显著下降。这表明当前的自回归生成框架和普吕克射线编码（Plücker-Ray encoding）在处理大视差时的鲁棒性不足。
- **长距离世界生成能力缺失**：模型目前缺乏生成长序列、大范围三维场景的能力，这受限于自回归生成的误差累积和训练数据的场景规模。

### 3. 开放问题

论文和实验分析揭示了以下待解决的关键问题：

1. **相机控制的精细化**：如何开发更精确的相机控制机制，以应对大基线运动的室外场景？当前基于普吕克射线编码的姿态条件化方式在极端视角变化下可能不足以提供充分的几何约束。
2. **长序列生成的帧间一致性**：自回归生成框架在长序列中面临纹理漂移和几何不一致的累积误差，如何提高帧间纹理一致性是一个开放挑战。
3. **阶段二训练的稳定性**：消融实验暗示阶段二的 RGB-Depth-Pose 联合学习可能存在训练不稳定问题，能否通过降低几何损失权重（$\lambda_{geo}$）来改善收敛性值得探索。
4. **强化学习的潜在增益**：论文提出强化学习可能进一步提升三维视觉定位和长距离生成性能，这指向了将理解与生成任务纳入序贯决策框架的研究方向。

### 4. 知识库定位

Omni-View 处于**统一多模态理解与生成**和**三维场景表征学习**的交叉点。其方法论贡献可定位于以下知识脉络：

- **统一多模态模型谱系**：继承自 BAGEL 的理解-生成一体化范式，但首次将几何估计作为生成任务的一部分显式建模，为后续统一模型引入更多三维先验提供了可复用的架构模板。
- **自回归三维生成**：将 Diffusion Forcing 与 D2S 课程策略结合，为三维场景的自回归生成提供了新的训练范式，其“从稠密到稀疏”的参考图像调度策略可迁移至其他需要时序建模的三维生成任务。
- **多任务互促学习**：通过共享的多模态自注意力机制，验证了纹理合成、深度估计、相机姿态估计和理解任务间的正向迁移，为多任务三维基础模型的训练策略设计提供了实证依据。

## 原文 PDF

![[paperPDFs/ICLR_2026/Omni_View_Unlocking_How_Generation_Facilitates_Understanding_in_Unified_3D_Model_46bff9ed5dad.pdf]]
