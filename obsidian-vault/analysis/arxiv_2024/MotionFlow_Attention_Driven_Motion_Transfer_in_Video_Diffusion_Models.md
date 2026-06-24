---
title: "MotionFlow: Attention-Driven Motion Transfer in Video Diffusion Models"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/MotionFlow_Attention_Driven_Motion_Transfer_in_Video_Diffusion_Models.pdf
aliases:
- MotionFlow
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/representation_self_supervised_transfer
core_operator: 交叉注意力图的对齐与引导
primary_logic: 利用预训练视频扩散模型中的交叉注意力图，可以独立于源视频的外观和场景布局，准确地捕获和迁移运动模式，从而以测试时优化的方式实现训练无关的运动迁移。
claims:
- MotionFlow 在文本相似度、运动保真度和时间一致性上均达到最优，且在用户研究中获得最高偏好。
- 交叉注意力引导的潜在更新是保证运动迁移成功的关键，消融实验证实了其不可或缺。
- MotionFlow 在 CLIP 文本相似度与运动保真度之间取得了更好的平衡，超越了所有对比方法。
- DAVIS 上 Text Similarity↑ = 0.322
---

# MotionFlow: Attention-Driven Motion Transfer in Video Diffusion Models

> [!tip] 核心洞察
> 利用预训练视频扩散模型中的交叉注意力图，可以独立于源视频的外观和场景布局，准确地捕获和迁移运动模式，从而以测试时优化的方式实现训练无关的运动迁移。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionFlow：基于注意力驱动的视频扩散模型运动迁移 |
| 英文题名 | MotionFlow: Attention-Driven Motion Transfer in Video Diffusion Models |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2412.05275) · [Project](https://motionflow-diffusion.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/representation_self_supervised_transfer |
| Method | MotionFlow |
| Dataset | DAVIS, User Study |

> [!tip] 效果简介
> - DAVIS 上，Text Similarity↑ 0.322；Motion Fidelity 0.940；Temporal Consistency 0.941。
> - User Study 上，Text Alignment Preference 0.42；Motion Alignment Preference 0.43；Motion Smoothness Preference 0.39。

## 概述

视频扩散模型在文本到视频生成领域取得了显著进展，但**无需训练的细粒度运动控制**仍然是一个核心瓶颈。现有方法大多依赖时间注意力特征匹配或模型微调，不仅需要额外的训练开销，还容易将源视频的外观和场景布局一并迁移到生成结果中，难以在保持运动一致性的同时实现大幅度的场景变化。

**MotionFlow** 提出了一种全新的解决思路：利用预训练视频扩散模型中的**交叉注意力图**作为运动载体，在测试时通过梯度引导优化潜在表示，实现完全无需训练的运动迁移。其核心洞见在于，交叉注意力图能够独立于源视频的外观和场景布局，精确地捕获物体的运动轨迹和空间动态，从而将运动模式“提取”出来，注入到任意编辑提示所描述的新场景中。

该方法在 DAVIS 数据集上取得了文本相似度 0.322、运动保真度 0.940、时间一致性 0.941 的综合最优结果，并在用户研究中以最高偏好比例（文本对齐 0.42、运动对齐 0.43、运动流畅度 0.39）显著超越 **DMT**（Yatim et al., CVPR 2024）、**VMC**（Jeong et al., CVPR 2024）、**MotionDirector**（Zhao et al., ECCV 2025）和 **Motion Inversion**（Wang et al., 2024）等基线方法。消融实验进一步证实，交叉注意力引导的潜在更新是运动迁移成功的关键——移除该机制将直接导致运动丢失或目标物体生成失败。

MotionFlow 的效果依赖于预训练模型注意力图的质量，在物体几何形状差异巨大时可能失效，且存在被滥用于生成欺骗性内容的伦理风险。

## 背景与动机

### 问题背景

文本到视频（T2V）扩散模型在生成高质量、语义一致的视频方面取得了显著进展，但如何在不依赖额外训练或微调的前提下实现对生成视频中运动模式的精细控制，仍然是一个开放难题。用户通常希望将一段参考视频中的运动动态迁移到新的文本提示所描述的场景中——例如将“奔跑的猎豹”的运动模式迁移到“行走的机器人”上——同时保持目标场景的外观和语义完整性。这一任务的核心挑战在于：运动信息与外观、场景布局高度耦合，现有方法难以在解耦运动的同时适应大幅度的场景变化。

### 现有方法缺口

当前的运动迁移方法大致可分为两类，但它们各自存在明显局限：

**基于微调的方法**，如 **MotionDirector**（Zhao et al., ECCV 2025）和 **VMC**（Jeong et al., CVPR 2024），通过对预训练模型进行额外训练或参数适配来实现运动定制。MotionDirector 采用双路径 LoRA 架构，VMC 则通过时间注意力适配进行运动定制。这类方法虽然能捕获特定运动模式，但需要针对每个运动样本进行训练，计算开销大，且难以泛化到未见过的运动类型。

**基于特征匹配的方法**，如 **DMT**（Yatim et al., CVPR 2024）和 **Motion Inversion**（Wang et al., 2024），试图从源视频中提取运动特征并在生成过程中进行匹配。DMT 依赖时空特征进行零样本运动迁移，Motion Inversion 则通过时间注意力层学习运动嵌入。然而，这些方法通常需要 DDIM 反演后的特征对齐，且运动特征的提取往往与源视频的外观和场景布局高度相关，导致在改变编辑提示中的场景时，可能将不需要的外观信息一并迁移。

### 核心瓶颈

上述方法的共同瓶颈在于：**预训练文本到视频模型缺乏无需训练的细粒度运动控制机制，现有方法难以在维持运动一致性的同时处理大幅度场景变化，且往往需要额外训练或微调**。具体而言，三个关键缺口亟待解决：

1. **训练依赖**：现有方法要么需要针对每个运动样本进行微调，要么依赖复杂的特征匹配流程，无法实现即插即用的运动迁移。
2. **外观-运动耦合**：运动特征的提取往往与源视频的外观和场景布局绑定，导致在改变场景时产生不需要的外观泄漏。
3. **场景适应性不足**：当编辑提示要求大幅改变场景布局时（如从“草地”变为“城市街道”），现有方法难以在保持运动一致性的同时生成语义正确的新场景。

### 本文动机

MotionFlow 的提出源于一个关键观察：**预训练视频扩散模型中的交叉注意力图天然地编码了运动主体的时空动态信息，且这种编码在很大程度上独立于外观和场景布局**。如 Figure 2 所示，交叉注意力图能够准确地定位运动主体在每一帧中的位置和形状变化，形成一种“运动签名”。这一发现暗示了一条全新的技术路径：通过操纵交叉注意力图，可以在不修改模型权重、不依赖源视频外观的前提下，实现运动模式的精确捕获和迁移。

基于此，MotionFlow 提出了一种**测试时优化**的运动迁移框架，核心思想是：利用 DDIM 反演从源视频中提取交叉注意力图作为运动引导信号，在生成过程中通过注意力损失函数更新噪声潜在表示，使生成视频的注意力分布与源视频对齐。这种方法无需任何训练或微调，且运动迁移独立于源视频的外观和场景布局，允许用户通过编辑提示自由改变目标场景。

## 核心创新

MotionFlow 的核心创新在于**将运动迁移问题重新定义为交叉注意力图的对齐与引导问题**，从而彻底绕过了现有方法对额外训练、微调或时空特征匹配的依赖。这一根本性转变体现在以下三个关键维度。

### 1. 运动表征的范式转换：从时空特征到交叉注意力图

现有运动迁移方法的运动特征来源存在根本性分歧。**DMT** (Yatim et al., CVPR 2024) 依赖时空特征进行零样本运动迁移，**VMC** (Jeong et al., CVPR 2024) 通过时间注意力适配实现运动定制，**MotionDirector** (Zhao et al., ECCV 2025) 和 **Motion Inversion** (Wang et al., 2024) 则分别借助双路径 LoRA 微调和时间注意力层嵌入来学习运动表示。这些方法的共同瓶颈在于：运动特征的提取过程与源视频的外观、场景布局深度耦合，导致在编辑提示要求大幅度场景变化时，不需要的外观信息会被一并迁移。

MotionFlow 的突破在于发现预训练视频扩散模型中的**交叉注意力图天然编码了运动动态信息**，且这一编码独立于外观和场景布局。如 Figure 2 所示，主体 token 的交叉注意力图能够准确追踪源视频中物体的运动轨迹，同时保持对编辑提示中全新场景描述的响应能力。这意味着运动迁移不再需要学习额外的运动表示——只需从交叉注意力图中提取运动模式，即可实现外观无关的运动迁移。

### 2. 推理模式的根本变革：从训练依赖到测试时优化

训练/推理模式的差异构成了 MotionFlow 与所有 baseline 方法之间最本质的分野。现有方法无一例外地引入了某种形式的训练负担：MotionDirector 和 VMC 需要微调模型权重，DMT 和 Motion Inversion 虽避免了微调，但仍需在 DDIM 反演后进行特征匹配或嵌入学习。这些训练步骤不仅增加了计算开销，还限制了方法对新视频和新运动的泛化能力。

MotionFlow 采用**纯粹的测试时优化策略**：在推理阶段，仅利用预训练模型的交叉注意力图进行梯度引导，通过损失函数优化潜在表示，无需任何预先训练或微调。具体而言，方法在每一步扩散过程中计算交叉注意力损失、自注意力损失和时间注意力损失的加权组合 $\mathcal{L}_{\mathrm{total}}$，并通过梯度下降更新噪声潜在表示 $z_{t}^{\prime} = z_{t} - \alpha_{t} \nabla_{z_{t}} \mathcal{L}_{\mathrm{total}}$。这一设计的因果机制在于：交叉注意力图的质量直接决定了运动迁移的精度，而测试时优化确保了该方法可以适配任意预训练视频扩散模型，无需针对特定模型重新训练。

### 3. 场景布局的解耦：运动与外观的彻底分离

场景布局依赖是制约现有方法实用性的关键瓶颈。当编辑提示要求将“在草地上奔跑的狗”迁移为“在月球表面跳跃的机器人”时，基于时空特征或微调的方法往往会将草地纹理、光照条件等源视频外观信息泄漏到生成结果中，导致运动迁移与场景编辑的目标相互冲突。

MotionFlow 通过交叉注意力图的引导机制实现了运动与场景布局的彻底解耦。如 Figure 4 所示，该方法既可以保持原始场景布局，也可以根据用户提供的文本提示大幅改变场景——从森林到沙漠、从白天到夜晚、从写实到卡通风格，运动模式始终保持一致。这一能力的根源在于：交叉注意力图仅编码了“物体在哪里、如何运动”的时空信息，而场景的语义内容完全由编辑提示通过扩散模型自身的生成能力来填充，两者在注意力空间中自然分离。

### 创新点的因果链条

上述三个创新维度构成了一个完整的因果链条：**交叉注意力图作为运动表征**（创新1）使得**无需训练的测试时优化**（创新2）成为可能，而这两者的结合又自然实现了**运动与场景布局的解耦**（创新3）。消融实验为这一因果链条提供了决定性证据：如 Figure 7 所示，移除交叉注意力引导的潜在更新后，反演的潜在表示要么丢失运动信息，要么完全无法生成目标物体，证实了交叉注意力引导是运动迁移成功的必要条件。

## 整体框架

MotionFlow 采用“先反演，后生成”的两阶段范式，在测试时利用预训练视频扩散模型中的交叉注意力图实现无需训练的运动迁移。其核心思想是：交叉注意力图能够独立于源视频的外观和场景布局，准确捕获运动主体的时空动态，从而将运动模式迁移到由编辑提示词指定的全新场景中。

### 两阶段流水线

**阶段一：DDIM 反演与注意力提取**

给定一段原始视频，MotionFlow 首先通过 DDIM 反演将其编码为噪声潜在序列，同时从 UNet 的特定层中提取交叉注意力图。注意力提取的目标层包括中间块、下采样的最后一个块以及上采样的第一个块，这些层的注意力图对运动主体的空间定位最为敏感。提取的注意力图随后通过自适应阈值转化为二元掩码，用于在生成阶段约束运动区域：

$$M_{s,f}^{t}[x,y] = \mathbb{I}\left( A_{s,f}^{t}[x,y] > \tau \max_{i,j} A_{s,f}^{t}[i,j] \right)$$

其中 $A_{s,f}^{t}$ 是时间步 $t$ 处、针对主体 token $s$ 和帧 $f$ 的交叉注意力图，$\tau$ 为自适应阈值（论文中设为 0.4）。

**阶段二：注意力引导的生成**

在生成阶段，MotionFlow 从反演得到的噪声潜在表示出发，使用用户提供的编辑提示词驱动扩散去噪过程。每一步去噪中，模型计算三个维度的注意力损失：

- **交叉注意力损失**：确保生成视频中运动主体的注意力集中在掩码区域内：

$$\mathcal{L}_{s,f} = 1 - \frac{M_{s,f} \cdot A_{s,f}}{A_{s,f}}$$

- **自注意力损失**：维持帧内空间结构的一致性。
- **时间注意力损失**：保证跨帧运动轨迹的时序连贯性。

三项损失加权组合为总损失：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{cross}} \mathcal{L}_{\mathrm{cross}} + \lambda_{\mathrm{self}} \mathcal{L}_{\mathrm{self}} + \lambda_{\mathrm{temporal}} \mathcal{L}_{\mathrm{temporal}}$$

最后，通过梯度下降在每一步更新噪声潜在表示：

$$z_{t}^{\prime} = z_{t} - \alpha_{t} \nabla_{z_{t}} \mathcal{L}_{\mathrm{total}}$$

其中学习率 $\alpha_t$ 设为 5.0。这一潜在更新机制是 MotionFlow 成功的关键——消融实验证实，移除交叉注意力引导的潜在更新会导致生成视频中运动丢失或目标物体生成失败。

### 输入输出与模块关系

MotionFlow 的输入包括：一段原始视频（提供运动模式）和一个编辑提示词（指定目标场景和主体）。输出是一段新视频，其运动模式与源视频一致，但场景布局和外观完全由编辑提示词决定。

各模块的协作逻辑如下：DDIM 反演模块负责将视频压缩为潜在空间中的可优化表示；注意力提取模块从 UNet 中捕获运动主体的空间定位信息并生成掩码；引导生成模块则在去噪过程中以这些掩码为约束，通过梯度优化将运动模式“注入”到新场景中。整个流程无需任何模型训练或微调，仅依赖预训练模型（ZeroScope T2V）的推理能力，实现了真正的测试时运动迁移。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2412_05275/figures/003_Figure_3.jpg]]
*Figure 3: Overview of MotionFlow framework. Our invert-then-generate method operates in two main stages: (1) Inversion, where DDIM inversion is used to extract latent representations and cross-attention maps from the original video, generating target masks that capture the subject’s motion and spatial details; (2) Generation, where these masks and a text prompt guide the creation of a new video, aligning with the original video’s motion dynamics and spatial layout while adhering to the semantic content of the prompt*

## 核心模块与公式推导

MotionFlow 的框架围绕一个“反演-生成”范式构建，其核心在于从预训练视频扩散模型中提取交叉注意力图，并利用这些注意力图引导生成过程。整个流程包含四个关键模块，彼此紧密协作，构成了运动迁移的完整链条。

### DDIM 反演

该方法首先对原始视频执行 DDIM 反演，将其编码为噪声潜在序列并提取中间表示。这一步骤为后续的注意力提取和引导生成提供了初始化的潜在空间轨迹，使得模型能够在保持原视频时间结构的前提下进行条件化编辑。

### 交叉注意力提取与掩码生成

从预训练 T2V 模型（ZeroScope）的 UNet 特定层中提取交叉注意力图是 MotionFlow 的核心操作。具体而言，注意力图从中间块、下采样的最后一个块和上采样的第一个块中提取。给定查询特征 $Q$、文本键 $K$ 和键的维度 $d$，交叉注意力图的计算公式为：

$$A^{t} = \operatorname{Softmax}(Q K^{\tau} / \sqrt{d})$$

这些注意力图捕捉了主体 token 在每一帧中的空间定位和运动轨迹，为运动迁移提供了独立于源视频外观的信号。

为了将连续的注意力分布转化为可操作的约束区域，MotionFlow 采用自适应阈值将注意力图二值化，生成二元掩码：

$$M_{s,f}^{t}[x,y] = \mathbb{I}\left( A_{s,f}^{t}[x,y] > \tau \max_{i,j} A_{s,f}^{t}[i,j] \right)$$

其中 $\tau$ 为阈值参数（实验中设为 0.4），$s$ 和 $f$ 分别表示主体 token 和帧索引。该自适应机制基于最大注意力权重动态调整阈值，确保在不同场景和运动模式下都能生成合理的运动区域掩码。

### 引导生成与潜在更新

在生成阶段，MotionFlow 通过三项注意力损失共同优化潜在表示，将运动约束注入扩散过程。交叉注意力损失确保生成视频的注意力集中在掩码区域内：

$$\mathcal{L}_{s,f} = 1 - \frac{M_{s,f} \cdot A_{s,f}}{A_{s,f}}$$

总损失由交叉注意力损失、自注意力损失和时间注意力损失加权组合而成：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{cross}} \mathcal{L}_{\mathrm{cross}} + \lambda_{\mathrm{self}} \mathcal{L}_{\mathrm{self}} + \lambda_{\mathrm{temporal}} \mathcal{L}_{\mathrm{temporal}}$$

其中自注意力损失和时间注意力损失分别约束空间结构一致性和帧间运动平滑性。最后，通过梯度下降在每一步更新噪声潜在表示（学习率 $\alpha_t = 5.0$）：

$$z_{t}^{\prime} = z_{t} - \alpha_{t} \nabla_{z_{t}} \mathcal{L}_{\mathrm{total}}$$

这一测试时优化机制是 MotionFlow 实现训练无关运动迁移的关键——消融实验证实，移除交叉注意力引导的潜在更新会导致生成视频中运动丢失或目标物体生成失败（Figure 7）。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2412_05275/figures/002_Figure_2.jpg]]
*Figure 2: Motivation. Visualization of cross-attention maps for the subject tokens, showing how MotionFlow captures and transfers motion dynamics from the original video, ensuring accurate subject motion while adhering to new edit prompts*

## 实验与分析

### 定量评估与基准对比

我们采用 DAVIS 数据集进行定量评估，从文本相似度（Text Similarity）、运动保真度（Motion Fidelity）和时间一致性（Temporal Consistency）三个维度衡量各方法的性能。

**Table 1** 汇总了 MotionFlow 与现有方法的定量对比结果。MotionFlow 在文本相似度上达到 **0.322**，运动保真度达到 **0.940**，时间一致性达到 **0.941**，在所有三项指标上均超越对比基线。这表明，通过交叉注意力图捕获运动模式，MotionFlow 能够在保持与编辑文本高度语义对齐的同时，忠实地保留源视频的运动动态，并维持生成视频帧间的时序连贯性。

值得注意的是，**Figure 6** 进一步揭示了各方法在 CLIP 文本相似度与运动保真度之间的权衡关系。散点图显示，MotionFlow 在这两个通常相互制约的指标之间取得了更优的平衡——其他方法往往在追求高运动保真度时牺牲文本对齐，或反之。MotionFlow 之所以能突破这一瓶颈，关键在于其运动迁移独立于源视频的外观和场景布局，从而允许编辑文本自由改变场景内容，而不会对运动保真度造成明显损害。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2412_05275/figures/006_Figure_6.jpg]]
*Figure 6: Evaluation. CLIP text similarity versus Motion Fidelity scores for each baseline. Our method exhibits a better balance between these two metrics*

### 用户研究

为验证主观感知质量，我们进行了用户研究，邀请参与者从文本对齐度、运动对齐度和运动流畅度三个维度对不同方法的生成视频进行偏好选择。**Table 1** 的用户偏好数据显示，MotionFlow 在三项指标上分别获得了 **0.42**、**0.43** 和 **0.39** 的偏好比例，均显著高于其他方法。**Figure 8** 展示了用户研究中使用的典型问卷界面，参与者需同时观看多个生成视频并做出综合判断。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2412_05275/figures/007_Table_1.jpg]]
*Table 1: Quantitative Comparisons and User Study Quantitative comparisons for Text Similarity, Motion Fidelity, and Temporal Consistency Scores. User preferences for text alignment to edit prompt, motion alignment to the original video, and motion smoothness of the generated video for DMT, MotionDirector, VMC, Motion Inversion, and MotionFlow*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2412_05275/figures/009_Figure_8.jpg]]
*Figure 8: An example question used in the user study. Participants were asked to evaluate multiple videos based on motion fidelity, motion smoothness, and text fidelity*

用户研究结果与定量指标高度一致，进一步证实了交叉注意力引导策略在感知层面的有效性——生成的视频不仅数值上更优，在人类观察者眼中也更具运动自然性和文本一致性。

### 消融实验：交叉注意力引导的关键作用

为验证交叉注意力引导的潜在更新（latent updates）对运动迁移的决定性作用，我们进行了消融实验。**Figure 7** 对比了有无该模块的生成结果。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2412_05275/figures/008_Figure_7.jpg]]
*Figure 7: Ablation study on latent updates. Without latent updates guided by cross-attention, inverted latents may fail to preserve motion or generate the intended subject. Please see Supplementary Material for full videos*

实验结果表明，移除交叉注意力引导的潜在更新后，反演得到的潜在表示在生成阶段无法有效保留运动信息，甚至导致目标物体生成失败。具体而言，缺少引导时，扩散模型的去噪过程会偏离源视频的运动轨迹，使生成视频中的主体丧失原有的运动模式或完全消失。这一消融实验直接证实了以下因果机制：**交叉注意力图的对齐与引导是保证运动迁移成功不可或缺的组件**，仅靠 DDIM 反演提取的潜在表示不足以在生成过程中维持运动一致性。

### 定性结果分析

**Figure 4** 展示了 MotionFlow 在多种场景和运动类型下的定性结果。该方法能够成功处理从简单到复杂、从单体运动到多体运动的广泛迁移任务。更重要的是，MotionFlow 既可以在生成视频中保持源视频的场景布局，也可以根据用户提供的编辑文本大幅度改变场景——例如，将“在草地上奔跑的狗”转换为“在雪地中奔跑的狼”，而运动模式保持高度一致。

**Figure 5** 提供了与 **DMT**（Yatim et al., CVPR 2024）、**MotionDirector**（Zhao et al., ECCV 2025）、**Motion Inversion**（Wang et al., 2024）和 **VMC**（Jeong et al., CVPR 2024）的定性对比。可视化结果显示，基线方法在处理大幅度场景变化时往往出现运动失真或主体外观残留，而 MotionFlow 由于将运动特征来源从时间注意力特征或微调权重转向交叉注意力图，能够更干净地解耦运动与外观，从而生成更准确、更自然的运动迁移效果。

### 失败模式与局限性

尽管 MotionFlow 在多数场景下表现优异，但其效果高度依赖预训练文本到视频模型（ZeroScope）的交叉注意力图质量。当注意力图噪声较大或定位不精确时，运动迁移的保真度会显著下降。此外，在物体几何形状差异巨大的情况下——例如将“圆形球体的滚动”迁移到“扁平长方体的滑动”——运动迁移可能会失效，因为交叉注意力图难以在形态差异过大的物体间建立有意义的运动对应关系。

最后，该方法存在被滥用于生成深度伪造或欺骗性内容的潜在伦理风险，需要在实际部署中建立相应的防范措施。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2412_05275/figures/005_Figure_5.jpg]]
*Figure 5: Comparison. Qualitative comparison of our method, MotionFlow, with DMT [37], MotionDirector [43], Motion Inversion [33] and VMC [12]*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2412_05275/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative Results. MotionFlow can successfully transfer a wide variety of motion types, ranging from single to multiple motions and from simple to complex motion patterns. Additionally, it can either maintain the original scene layout or significantly alter it based on the user-provided text prompt. Please refer to the supplementary material where the actual videos are provided*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2412_05275/figures/001_Figure_1.jpg]]
*Figure 1: MotionFlow is a training-free method that leverages attention for motion transfer. Our method can successfully transfer a wide variety of motion types, ranging from simple to complex motion patterns*

## 方法谱系与知识库定位

### 与现有方法的差异化定位

MotionFlow 的核心贡献在于提出了一种**训练无关的测试时运动迁移范式**，这与当前主流的运动迁移/定制方法形成了根本性的路径分异。现有方法可大致归为两类：一类依赖微调或额外训练来适配运动模式，另一类则通过时空特征匹配实现零样本迁移。MotionFlow 在两者之间开辟了第三条道路——利用预训练模型已有的交叉注意力图作为运动载体，通过测试时优化实现迁移，既不修改模型权重，也不依赖源视频的外观特征。

具体而言，与以下代表性工作的差异体现在：

- **DMT**（Yatim et al., CVPR 2024）：该方法通过时空特征匹配实现零样本文本驱动的运动迁移，但其运动特征提取依赖时空特征，容易受源视频外观和场景布局的影响，导致不希望的场景元素被一并迁移。MotionFlow 改用交叉注意力图作为运动特征来源，实现了运动信息与外观、场景布局的解耦，使得在编辑提示中大幅度改变场景成为可能。

- **VMC**（Jeong et al., CVPR 2024）：该方法通过时间注意力层的适配实现运动定制，本质上仍需要对模型进行一定程度的参数调整。MotionFlow 完全避免了这一步骤，仅通过交叉注意力引导的潜在更新即可完成迁移，在保持预训练模型完整性的同时降低了计算开销。

- **MotionDirector**（Zhao et al., ECCV 2025）：采用双路径 LoRA 进行运动定制，需要针对每个运动模式进行独立的微调训练。MotionFlow 的测试时优化策略无需任何预先训练，对新的运动模式具有即时的泛化能力。

- **Motion Inversion**（Wang et al., 2024）：通过时间注意力层学习运动嵌入，同样属于需要训练的方法范畴。MotionFlow 的注意力提取与引导机制不涉及任何可学习参数的引入。

### 方法谱系中的位置

从技术路线的演进来看，MotionFlow 处于**注意力机制在视频生成中应用深化**的关键节点。其方法论基础可追溯至以下几条研究脉络：

1. **扩散模型中的注意力操控**：在图像编辑领域，Prompt-to-Prompt 等工作已证明交叉注意力图可以有效地控制生成内容的空间布局。MotionFlow 将这一思想从静态图像拓展到动态视频，并进一步揭示了交叉注意力图在**时序维度上天然编码了运动信息**这一关键发现（见 Figure 2 的动机可视化）。

2. **DDIM 反演与可控生成**：基于 DDIM 反演的编辑方法通常依赖反演轨迹的精确重建。MotionFlow 的创新在于，它不追求完美重建，而是将反演作为提取中间表示（交叉注意力图和潜在表示）的工具，随后通过注意力引导损失主动偏离原始反演轨迹，实现受控的运动迁移。

3. **测试时优化范式**：与需要训练的方法相比，MotionFlow 的测试时优化策略在灵活性和部署便捷性上具有明显优势，但代价是推理时需要额外的梯度计算步骤。这使其更适用于对灵活性要求高、但对实时性要求不极端的应用场景。

### 适用边界与局限

尽管 MotionFlow 在多个维度上展现了优势，其适用边界受以下因素制约：

**方法固有的依赖瓶颈**：MotionFlow 的运动迁移质量高度依赖预训练 T2V 模型交叉注意力图的质量。当预训练模型（本文使用 ZeroScope）对特定提示词或运动模式的注意力定位不精确、噪声较大时，提取的二元掩码将无法准确捕获运动主体的空间轨迹，导致迁移失败或运动失真。这一依赖关系意味着，MotionFlow 的性能上限由底层预训练模型决定，随着更强 T2V 模型的发布，该方法的效果有望自然提升，但反之亦然。

**几何差异的容忍度**：虽然 MotionFlow 可以实现大幅度的场景变化（如将奔跑的狗替换为奔跑的马），但当源视频主体与目标主体在几何形状上差异巨大时（例如从细长物体到球形物体），交叉注意力图所编码的空间轨迹可能无法直接适配新的主体形态，导致运动迁移出现不自然的扭曲。这一局限源于交叉注意力图的 2D 空间本质——它捕获的是像素级的运动轨迹，而非 3D 语义级的运动模式。

**多主体交互的未探索区域**：当前方法主要针对单一运动主体的场景进行验证。对于视频中存在多个运动主体且它们之间存在复杂交互（如追逐、碰撞、遮挡）的情况，交叉注意力图如何分离不同主体的运动模式、如何处理主体间的注意力重叠，仍是未解决的问题。

**计算开销**：测试时优化需要在每一步去噪过程中计算梯度并更新潜在表示，相比纯前向推理的方法增加了计算负担。虽然避免了训练成本，但在需要快速批量处理的场景下可能成为瓶颈。

### 伦理与滥用风险

MotionFlow 的运动迁移能力在带来创作便利的同时，也引入了潜在的滥用风险。该方法可以将真实视频中的运动模式迁移到任意编辑提示描述的主体上，这意味着恶意使用者可能利用真实人物的运动视频生成虚假的、具有欺骗性的内容（如深度伪造）。论文明确指出了这一伦理问题，并呼吁建立相应的防范措施，但未提出具体的技术性防护机制。

### 开放问题

基于上述分析，以下开放问题值得后续研究关注：

1. **注意力图的鲁棒性增强**：当预训练模型的注意力图质量不足时，能否通过注意力图的后处理或自监督优化来提升运动捕获的准确性，而非完全依赖底层模型的能力？

2. **多主体运动解耦**：如何将交叉注意力引导机制扩展到多主体场景，实现不同运动模式的独立捕获与迁移？这可能需要引入主体级别的注意力分离策略或实例分割引导。

3. **3D 运动表征的引入**：将 2D 交叉注意力图提升为 3D 运动表征（如结合深度信息或神经辐射场），能否解决几何差异过大时的迁移失败问题？

4. **轻量化与加速**：是否存在更高效的注意力引导策略（如仅在关键去噪步骤进行引导、使用近似的梯度计算），以降低测试时优化的计算开销，使其更接近实时应用的需求？

5. **长视频与高分辨率拓展**：当前方法在标准分辨率短视频上验证，将其拓展到更长时序和更高分辨率时，注意力图的内存占用和计算复杂度将显著增长，需要探索分块处理或层次化注意力引导策略。

## 原文 PDF

![[paperPDFs/arxiv_2024/MotionFlow_Attention_Driven_Motion_Transfer_in_Video_Diffusion_Models.pdf]]