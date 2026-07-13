---
title: "ReVideo: Remake a Video with Motion and Content Control"
type: paper
paper_level: A
venue: NeurIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/ReVideo_Remake_a_Video_with_Motion_and_Content_Control.pdf
project_link: https://mc-e.github.io/project/ReVideo/
code_link: null
aliases:
- ReVideo
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "三阶段训练（运动先验、解耦、去块）和时空自适应融合模块（SAFM）共同解耦内容保持与运动定制，使模型能分别遵循两种控制信号。"
primary_logic: "未编辑内容自带运动信息会淹没运动轨迹控制；必须通过将编辑区域与未编辑区域来自不同视频的数据构造实现解耦，并引入时间/空间自适应融合来重建和谐编辑结果。"
claims:
- "单分支控制模块或双分支联合训练均无法实现运动控制；运动先验训练虽能改善，但引入内容控制后仍退化。"
- "三阶段训练（包括解耦和去块微调）最终实现了内容与运动的协调控制，块效应消除。"
- "SAFM通过预测与时间步相关的权重图融合特征，比直接相加更准确地实现轨迹引导。"
- "ReVideo在定量评估中PSNR 32.85、文本对齐0.2304，均优于InsV2V等基线方法。"
---

# ReVideo: Remake a Video with Motion and Content Control

> [!tip] 核心洞察
> 未编辑内容自带运动信息会淹没运动轨迹控制；必须通过将编辑区域与未编辑区域来自不同视频的数据构造实现解耦，并引入时间/空间自适应融合来重建和谐编辑结果。

| 字段      | 内容                                                                                                                      |
| ------- | ----------------------------------------------------------------------------------------------------------------------- |
| 中文题名    | ReVideo：通过运动和内容控制重制视频                                                                                                   |
| 英文题名    | ReVideo: Remake a Video with Motion and Content Control                                                                 |
| 会议/期刊   | NeruIPS 2024                                                                                                            |
| Links   | [paper](https://arxiv.org/abs/2405.13865) · [Project](https://mc-e.github.io/project/ReVideo/)                           |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method  | ReVideo                                                                                                                 |
| Dataset | Local Video Editing Test Set                                                              |

> [!tip] 效果简介
> - Local Video Editing Test Set 上，PSNR 为 32.85，对比 29.77 (InsV2V)，变化 +3.08。
> - Local Video Editing Test Set 上，Text Alignment (CLIP score) 为 0.2304，对比 0.2022 (InsV2V)，变化 +0.0282。

## 概要

**ReVideo** 提出了一种在视频局部区域同时控制内容与运动的编辑方法。其核心挑战在于：未编辑区域本身携带稠密的视觉外观与帧间运动信息，扩散模型倾向于从这些区域推断编辑区域的运动，从而忽略用户指定的稀疏轨迹控制，导致内容编辑与运动定制无法协调工作。

为解决这一耦合问题，ReVideo 设计了三阶段训练策略与时空自适应融合模块（SAFM）。三阶段训练通过运动先验学习、数据解耦训练和去块微调，逐步将内容保持与运动定制分离；SAFM 则根据编辑掩码和时间步预测融合权重图，自适应地组合内容与运动条件特征，而非简单相加。

在定量评估中，ReVideo 的 PSNR 达到 32.85，文本对齐（CLIP score）为 0.2304，均优于 InsV2V 等基线方法。消融实验进一步证实：SAFM 相比直接求和融合能实现更准确的轨迹引导，移除时间自适应会导致编辑边界伪影，而仅微调 Key/Value 嵌入可在消除块效应的同时保持局部运动控制精度。

该方法的主要局限在于：当基础模型 SVD 的生成先验不足时，编辑质量受限；长视频编辑存在误差累积；尚未针对动态遮挡和复杂交互场景进行专门优化。

视频编辑技术正从全局风格迁移走向精细化、局部化的控制。用户不仅希望替换画面中的特定物体（内容编辑），更希望精确指定该物体的运动轨迹（运动编辑）。然而，现有方法在这两个维度上存在明显的耦合困境。

**核心瓶颈在于未编辑区域的“信息淹没”效应。** 在局部视频编辑中，未编辑区域天然携带稠密的视觉纹理与帧间运动信息。当扩散模型同时接收用户指定的稀疏轨迹控制信号和未编辑区域的丰富运动线索时，模型倾向于从后者推断编辑区域的运动，导致用户提供的轨迹控制被实质性忽略。Figure 3 的玩具实验清晰地揭示了这一现象：无论是单分支控制模块还是双分支联合训练，运动控制条件均无法生效（“the motion condition has no control effect”）；即使引入运动先验训练改善了部分控制能力，一旦加入内容控制信号，运动控制精度再次退化（“the control accuracy is weakened and affected by the unedited content”）。

这一耦合问题的根源在于控制信号的竞争关系。内容条件（如修改后的首帧）和运动条件（如稀疏轨迹）通过同一控制分支注入时，模型缺乏机制来区分编辑区域与未编辑区域的信号来源。未编辑区域的自带运动信息实质上构成了一个“隐式运动条件”，其强度远超用户提供的稀疏轨迹，形成信号淹没。

**现有方法存在明确缺口。** 以 **InsV2V** 为代表的文本驱动编辑方法仅能控制语义内容，无法精确指定运动；**AnyV2V** 通过首帧编辑传播的方式同样缺乏对运动轨迹的显式建模；商业工具 **Pika** 虽支持区域重生成，但在添加新物体时运动一致性不足（Figure 13 展示了其向天空添加飞机时的失败案例）。这些方法的共同缺陷在于：它们要么完全放弃运动控制，要么将内容与运动控制隐式地耦合在一起，无法实现解耦的、协调的局部编辑。

**本文的核心动机在于实现内容与运动的协同解耦控制。** ReVideo 旨在让用户在指定编辑区域的同时，既能通过修改首帧定义新内容，又能通过绘制稀疏轨迹直观地定义运动模式。实现这一目标的关键挑战并非设计更强的控制编码器，而是从根本上打破未编辑内容对运动控制的干扰——这需要从训练数据构造、训练策略到特征融合机制的协同设计。

## 核心方法与创新机理

ReVideo 的核心创新在于系统性地解决了局部视频编辑中**内容控制与运动控制的耦合问题**。其根本瓶颈在于：未编辑区域本身携带稠密的视觉与帧间运动信息，扩散模型在生成时天然倾向于从中推断编辑区域的运动，从而“淹没”用户指定的稀疏轨迹控制信号。ReVideo 通过三个紧密协同的机制实现了内容保持与运动定制的解耦。

### 1. 三阶段解耦训练策略

ReVideo 采用从粗到精的三阶段训练，逐步建立独立的内容与运动控制能力：

- **第一阶段（运动先验训练）**：仅使用运动轨迹条件训练控制模块，使模型初步获得遵循轨迹生成运动的能力。Toy 实验（Figure 3）表明，若不经过此阶段，无论是单分支还是双分支控制结构，运动条件均“无控制效果”（motion condition has no control effect）。
- **第二阶段（解耦训练）**：核心创新在于**数据构造策略的彻底改变**——将训练样本中的编辑区域与未编辑区域分别取自两个不同的视频，通过掩码拼合（$V = V_1 \cdot M + V_2 \cdot (1 - M)$）。这一设计迫使模型无法从周围内容推断编辑区域的运动，从而真正学会依赖运动轨迹条件。Figure 3 的 Toy experiment 4 证实，经过此阶段后模型“消除了块效应，并保留了对未编辑内容与运动定制的联合控制”。
- **第三阶段（去块微调）**：针对解耦训练可能引入的编辑边界块效应，仅微调控制模块和 SVD 基模型中时序自注意力层的 Key/Value 嵌入（$W_k$、$W_v$）。Figure 7 消融实验显示，若微调整个控制模块反而会降低局部运动控制精度，而仅微调 Key/Value 嵌入则能在消除伪影的同时保持控制能力。

### 2. 时空自适应融合模块（SAFM）

SAFM 替代了朴素方法中直接相加条件特征的融合方式，其设计直指耦合问题的本质：**不同扩散采样步对内容与运动条件的依赖程度不同**。SAFM 通过编辑掩码 $M$ 和时间步 $t$ 预测一个融合权重图 $\Gamma$，再以此权重融合内容编码器 $E_c$ 与运动编码器 $E_m$ 的输出：

$$\mathbf{f}_c = E_c(\mathbf{c}_{con}) \cdot \mathbf{r} + E_m(\mathbf{c}_{mot}) \cdot (1 - \mathbf{r}), \quad \mathbf{r} = \mathcal{H}(\mathbf{M}, t)$$

Figure 7 的消融证实，SAFM 相比直接求和“实现了更准确的轨迹引导”；若移除时间自适应（即不区分不同采样步的 $\Gamma$），则编辑区域边界会产生明显伪影。Figure 5 右侧可视化了不同时间步下 $\Gamma$ 的分布，直观展示了模型如何在去噪早期依赖运动控制、后期侧重内容保持。

### 3. 与基线方法的差异总结

| 改进维度 | 基线做法 | ReVideo 做法 |
|---------|---------|-------------|
| 内容-运动耦合处理 | 简单联合训练，直接相加特征 | 三阶段解耦训练 + SAFM 自适应融合 |
| 训练数据构造 | 标准视频数据 | 双视频掩码拼合解耦 |
| 条件融合方式 | 直接求和编码特征 | 基于掩码和时间步预测权重图融合 |

这些创新使 ReVideo 在定量评估中 PSNR 达到 32.85（InsV2V 为 29.77），文本对齐得分 0.2304（InsV2V 为 0.2022），并在人类评估中以 59.1% 的整体偏好率显著领先（Table 1）。

![[assets/figures/papers/paper_list_l51_ReVideo_Remake_a_Video_with_Motion_and_Content_Control/figures/005_Figure_5.jpg]]
*Figure 5: The architecture of our proposed spatiotemporal adaptive fusion module (left), and the visualization of fusion weight Γ at different timesteps (right)*

![[assets/figures/papers/paper_list_l51_ReVideo_Remake_a_Video_with_Motion_and_Content_Control/figures/001_Figure_1.jpg]]
*Figure 1: The capability of our method to locally modify video content and motion. This ability can also be easily extended to multi-area editing. The motion control is labeled in colorful lines in videos*

ReVideo 的整体 pipeline 围绕一个核心矛盾展开：在局部视频编辑中，未编辑区域携带的稠密视觉与帧间运动信息会淹没用户指定的稀疏轨迹控制信号，导致内容编辑与运动定制无法协调工作。为解决这一问题，ReVideo 在预训练的图像到视频扩散模型 SVD 之上，构建了一套从数据构造、训练策略到条件融合的完整控制链路。

**输入与输出。** 系统接收三组控制信号：（1）修改后的首帧，用于指定编辑区域的**内容**，并通过广播机制传播到后续帧；（2）未编辑区域的**原始内容**，需在生成过程中保持一致；（3）编辑区域内用户绘制的**轨迹线**，作为运动控制条件。输出为一段局部区域内容被替换、运动遵循轨迹的完整视频。

**核心模块关系。** pipeline 由四个关键组件串联而成：

- **Content Encoder ($E_c$)** 与 **Motion Encoder ($E_m$)**：分别将内容条件 $\mathbf{c}_{con}$ 和运动条件 $\mathbf{c}_{mot}$ 编码为特征表示。内容条件基于修改后的首帧，运动条件来自稀疏轨迹采样（详见附录 Figure 8 的轨迹采样流程）。

- **SAFM（Spatiotemporal Adaptive Fusion Module，时空自适应融合模块）**：接收两个编码器的输出，根据编辑掩码 $\mathbf{M}$ 和扩散时间步 $t$ 预测一个权重图 $\mathbf{r} = \mathcal{H}(\mathbf{M}, t)$，并通过加权融合得到统一的条件特征：
  $$\mathbf{f}_c = E_c(\mathbf{c}_{con}) \cdot \mathbf{r} + E_m(\mathbf{c}_{mot}) \cdot (1 - \mathbf{r})$$
  这一设计的核心动机在于：编辑区域内部需要运动控制主导，而边界区域需要内容保持主导。SAFM 在不同时间步和空间位置自适应地分配权重，从而在解耦内容保持与运动定制的过程中实现和谐过渡（Figure 5 右侧可视化了不同时间步下融合权重 $\Gamma$ 的变化）。

- **Control Module**：是 UNet 编码器的一份拷贝，负责将 SAFM 输出的融合特征注入 SVD 的去噪过程。其注入方式遵循朴素控制模块的特征加和公式（Equation 4），但条件特征 $\mathbf{f}_c$ 已经过 SAFM 的自适应融合处理。

- **SVD Base Model**：作为预训练的图像到视频生成先验，接收参考图像条件 $\mathbf{c}_I$ 和来自 Control Module 的控制信号，通过 EDM 预处理参数化的去噪网络 $F_\theta$ 逐步从噪声潜变量 $\mathbf{z}_t$ 恢复干净潜变量 $\hat{\mathbf{z}}_0$：
  $$\Phi_\theta(\mathbf{z}_t, t, \mathbf{c}_I; \sigma) = c_{skip}(\sigma) \mathbf{z}_t + c_{out}(\sigma) F_\theta(c_{in}(\sigma) \mathbf{z}_t, t, \mathbf{c}_I; c_{noise}(\sigma))$$

**三阶段训练的数据流与控制流。** 上述模块并非通过单次联合训练获得，而是经历三个阶段逐步解耦：

1. **运动先验训练（Stage 1）**：仅使用运动条件训练 Control Module，使模型初步建立对轨迹控制的响应能力。此时内容条件尚未引入，避免了未编辑区域的运动信息干扰。

2. **解耦训练（Stage 2）**：关键的数据构造策略在此阶段引入——训练样本中编辑区域与未编辑区域来自**两个不同视频**（$\mathbf{V} = \mathbf{V}_1 \cdot \mathbf{M} + \mathbf{V}_2 \cdot (1 - \mathbf{M})$），强制模型学习从解耦的信号中分别提取运动与内容控制，而非依赖未编辑区域自带的运动信息。SAFM 在此阶段被训练以自适应融合两类条件。

3. **去块训练（Stage 3）**：由于解耦训练中编辑区域与未编辑区域来自不同视频，生成结果可能在边界出现块效应。此阶段仅微调 Control Module 和 SVD 基模型中时序自注意力层的 Key/Value 嵌入（$W_k$、$W_v$），在消除块伪影的同时保留前两阶段建立的运动控制能力。消融实验表明，若在此阶段微调整个 Control Module，局部运动控制精度会退化（Figure 7）。

**与基线方法的差异。** 相比于 InsV2V 等方法的简单联合训练和直接特征相加，ReVideo 的核心差异在于：通过解耦的数据构造打破未编辑区域运动信息对轨迹控制的淹没效应，并通过 SAFM 在时空维度上自适应融合两类条件，而非静态地将编码特征求和。这一设计使得单个 Control Module 即可紧凑地承载内容与运动的联合控制。

### 基础扩散框架

ReVideo 以 Stable Video Diffusion（SVD）作为基础生成模型。SVD 是一个预训练的图像到视频扩散模型，其核心去噪过程在潜空间中进行。给定噪声潜变量 $\mathbf{z}_t$、时间步 $t$ 和参考图像条件 $\mathbf{c}_I$，模型预测干净潜变量 $\hat{\mathbf{z}}_0$：

$$\hat{\mathbf{z}}_0 = \Phi_\theta(\mathbf{z}_t, t, \mathbf{c}_I)$$

其中 $\Phi_\theta$ 采用 EDM 预处理参数化：

$$\Phi_\theta(\mathbf{z}_t, t, \mathbf{c}_I; \sigma) = c_{skip}(\sigma) \mathbf{z}_t + c_{out}(\sigma) F_\theta(c_{in}(\sigma) \mathbf{z}_t, t, \mathbf{c}_I; c_{noise}(\sigma))$$

训练目标为去噪分数匹配损失：

$$\mathbb{E}_{\mathbf{z}_0, t, \mathbf{n} \sim \mathcal{N}(0, \sigma^2)} \left[ \lambda_\sigma || \Phi_\theta(\mathbf{z}_0 + \mathbf{n}, t, \mathbf{c}_I) - \mathbf{z}_0 ||_2^2 \right]$$

### 控制模块与特征注入

为实现局部视频编辑，ReVideo 在 SVD 基础上增加一个控制模块，该模块是 UNet 编码器的副本。编辑任务涉及三种控制信号：编辑区域的内容修改（通过修改首帧并广播实现）、未编辑区域的内容保持，以及编辑区域内的运动轨迹控制。

朴素的特征注入方式是将内容条件 $\mathbf{f}_c$ 和运动条件 $\mathbf{f}_m$ 编码后直接相加，再通过零卷积 $\mathcal{Z}(\cdot)$ 注入到基础模型的中间特征中：

$$\mathbf{y}_c = \mathcal{F}(\mathbf{z}_t, t, \mathbf{c}_{ref}; \boldsymbol{\Theta}) + \mathcal{Z}(\mathcal{F}(\mathbf{z}_t + \mathcal{Z}(\mathbf{f}_c), t, \mathbf{c}_{ref}; \boldsymbol{\Theta}_c))$$

然而，这种直接求和的融合方式在局部编辑场景下存在根本性问题：未编辑区域本身携带稠密的视觉与帧间运动信息，扩散模型天然倾向于从中推断编辑区域的运动，导致用户指定的稀疏轨迹控制信号被淹没。

### 时空自适应融合模块（SAFM）

为解决内容与运动控制的耦合问题，ReVideo 提出了时空自适应融合模块（SAFM），其核心思想是根据编辑掩码 $\mathbf{M}$ 和时间步 $t$ 预测一个融合权重图 $\mathbf{r}$，以此自适应地融合内容编码器 $E_c$ 和运动编码器 $E_m$ 的输出：

$$\mathbf{f}_c = E_c(\mathbf{c}_{con}) \cdot \mathbf{r} + E_m(\mathbf{c}_{mot}) \cdot (1 - \mathbf{r}), \quad \mathbf{r} = \mathcal{H}(\mathbf{M}, t)$$

其中 $\mathbf{r}$ 是一个与时空位置相关的权重图，由一个小型网络 $\mathcal{H}$ 根据编辑掩码和扩散采样时间步预测得到。该设计的直觉在于：扩散模型在不同采样步骤中对内容和运动条件的依赖程度不同——早期步骤更需要运动轨迹的结构性引导，后期步骤则更关注内容细节的保持。通过时间自适应的权重预测，SAFM 能够在不同去噪阶段动态调整两种条件的融合比例。

消融实验证实了 SAFM 的有效性：相比于直接相加特征融合，SAFM 实现了更准确的轨迹引导（Figure 7）。若移除时间自适应（即不区分不同采样步骤的 $\mathbf{r}$），编辑区域边界会出现明显的块状伪影。

### 三阶段训练策略

训练策略是 ReVideo 实现内容-运动解耦的另一关键。三阶段训练从粗到细逐步建立控制能力：

1. **运动先验训练**：仅使用运动条件训练控制模块，使模型初步建立对轨迹信号的响应能力。
2. **解耦训练**：核心创新在于数据构造策略——将训练样本 $V$ 的编辑区域与未编辑区域分别取自两个不同的视频：$V = V_1 \cdot M + V_2 \cdot (1 - M)$。这迫使模型无法从未编辑区域推断编辑区域的运动，必须依赖显式的运动轨迹条件。此阶段同时引入内容控制，实现两种条件的初步解耦。
3. **去块训练**：解耦训练后编辑边界可能出现块效应。此阶段仅微调控制模块和基础模型 SVD 中时序自注意力层的 Key/Value 嵌入（$W_k$ 和 $W_v$），在消除块伪影的同时保持已建立的局部运动控制能力。消融实验表明，若在此阶段微调整个控制模块，局部运动控制精度会下降（Figure 7）。

## 实验与关键发现

### 核心瓶颈验证：内容与运动控制的耦合

ReVideo 的核心动机源于一个关键发现：在局部视频编辑中，未编辑区域本身携带的稠密视觉与帧间运动信息会“淹没”用户指定的稀疏轨迹控制信号，导致运动定制完全失效。作者通过一系列玩具实验（Figure 3）系统性地验证了这一耦合问题：

- **Toy experiment 1**：采用单分支控制模块（Figure 2 结构 A），内容条件正常工作，但运动条件“完全没有控制效果”（the motion condition has no control effect）。
- **Toy experiment 2**：改用双分支结构（Figure 2 结构 B），运动控制仍然无效（motion control is still ineffective），说明问题不在于分支数量，而在于条件融合机制本身。
- **Toy experiment 3**：引入运动先验的两阶段训练（先训练运动控制，再加入内容控制），运动控制能力有所改善，但引入内容控制后“控制精度被削弱并受到未编辑内容的影响”（the control accuracy is weakened and affected by the unedited content）。

这一系列实验揭示了问题的因果链条：扩散模型在去噪过程中，未编辑区域提供的帧间运动信息远强于稀疏轨迹信号，导致模型倾向于从上下文推断编辑区域的运动，而非遵循用户指定的轨迹。这是 ReVideo 方法设计的核心瓶颈。

### 定量评估

Table 1 汇总了 ReVideo 与基线方法的定量对比。在局部视频编辑测试集上，ReVideo 在 PSNR 指标上达到 32.85，显著优于 InsV2V 的 29.77（+3.08），表明编辑后的视频在像素级保真度上具有明显优势。在文本对齐（CLIP score）方面，ReVideo 取得 0.2304，优于 InsV2V 的 0.2022（+0.0282），说明编辑结果与目标描述的语义一致性更高。

![[assets/figures/papers/paper_list_l51_ReVideo_Remake_a_Video_with_Motion_and_Content_Control/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison between our ReVideo and other related works. We employ automatic metrics ( i . e . , , CLIP [33] score, PSNR) and human evaluation to evaluate the performance*

在人类评估中，ReVideo 在“整体质量”（Overall）和“编辑目标达成度”（Editing Target）两个维度上均获得最高偏好率（59.1%），验证了其编辑效果在主观感知上的优势。与商业方法 Pika 相比，ReVideo 在文本对齐和人类评估上具有明显优势，尽管 Pika 在一致性指标上表现相近。

### 消融研究

Figure 7 展示了三个关键消融实验的视觉结果：

**SAFM 与直接求和的对比**：将时空自适应融合模块（SAFM）替换为直接求和的特征融合方式后，编辑区域的轨迹引导精度显著下降。这验证了 SAFM 通过预测与时间步相关的权重图 $\mathbf{r} = \mathcal{H}(\mathbf{M}, t)$ 进行自适应融合的必要性——直接求和无法区分不同扩散采样阶段对内容与运动条件的需求差异。

**时间自适应的作用**：移除 SAFM 中的时间自适应机制（即不区分不同采样步的融合权重 $\Gamma$），会导致“编辑区域边界产生不理想的伪影”（not distinguishing $\Gamma$ in different sampling steps leads to unsatisfactory artifacts at the boundary of the editing area）。这表明扩散模型在早期和晚期采样步对内容与运动条件的依赖程度不同，时间自适应是边界和谐的关键。

**去块微调策略**：在第三阶段微调整个控制模块会“降低局部运动控制能力”（the local motion control capability is degraded），而仅微调时序自注意力层中的 Key/Value 嵌入（$W_k$ 和 $W_v$）则能在消除块伪影的同时保持运动控制精度。这一发现表明，块伪影主要源于时序层的不协调，而非空间特征提取层的问题。

### 视觉对比与扩展能力

Figure 6 展示了 ReVideo 与 InsV2V、AnyV2V、Pika 的视觉编辑效果对比。ReVideo 在同时修改局部内容并施加轨迹运动控制的任务上表现出明显优势，而基线方法要么无法遵循运动轨迹，要么在编辑区域边界产生不自然的过渡。

Figure 12 进一步展示了 ReVideo 处理长视频的能力，在包含 90 帧的 9 秒视频上仍能保持稳定的编辑效果，表明方法具有一定的时序扩展性。

![[assets/figures/papers/paper_list_l51_ReVideo_Remake_a_Video_with_Motion_and_Content_Control/figures/014_Figure_12.jpg]]
*Figure 12: The ability of our ReVideo to extend the number of editing frames. The results demonstrate the performance of our ReVideo in processing a 9-second video containing 90 frames*

### 失败模式与局限

尽管 ReVideo 在局部运动与内容联合控制上取得了突破，论文也明确指出以下局限：

1. **基础模型先验不足**：当 SVD 基础模型对特定场景的生成先验不足时，编辑区域的再生质量受限。这是扩散模型编辑方法的共性瓶颈。
2. **长视频误差累积**：虽然 Figure 12 展示了 90 帧编辑能力，但论文承认长视频编辑存在误差累积问题，尚未系统解决。
3. **复杂交互场景未优化**：方法尚未针对动态遮挡和复杂物体交互场景进行专门优化，这些场景下内容与运动的解耦可能面临更大挑战。

需要手动验证的是：论文未报告在极端运动幅度或高度非刚性变形场景下的定量表现，这些场景的实际编辑质量需要进一步评估。

![[assets/figures/papers/paper_list_l51_ReVideo_Remake_a_Video_with_Motion_and_Content_Control/figures/004_Figure_4.jpg]]
*Figure 4: The data construction strategy for decoupling training and editing results from this stage*

![[assets/figures/papers/paper_list_l51_ReVideo_Remake_a_Video_with_Motion_and_Content_Control/figures/012_Figure_11.jpg]]
*Figure 11: Tuning W _ { k } and W _ { v } in control module Tuning W _ { k } and W _ { v } in control module and base model Figure 11: The necessity of fine-tuning key embedding and value embedding in the base model, i.e., SVD*

## 定位与知识库关联

### 任务定位：局部视频编辑中的内容与运动解耦控制

ReVideo 瞄准的是**局部视频编辑**任务，其核心挑战在于同时控制编辑区域的内容（修改第一帧并广播）和运动（用户指定的稀疏轨迹）。该任务涉及三类条件信号：编辑内容、未编辑区域内容、以及编辑区域内的运动条件。与全局视频编辑或仅基于文本的区域重生成不同，ReVideo 要求模型在保持未编辑区域不变的约束下，精确遵循用户指定的运动轨迹。

### 方法谱系与关系

ReVideo 以 **SVD（Stable Video Diffusion）** 作为预训练基础模型，利用其高质量视频生成先验，在此基础上添加控制模块实现编辑目标。其方法设计可置于以下谱系中：

- **基于文本指导的视频编辑**：如 **InsV2V**（论文中标注为 [10]），通过文本描述驱动编辑，但缺乏精确的空间-运动控制能力。ReVideo 在定量评估中以 PSNR 32.85 显著优于 InsV2V 的 29.77，文本对齐得分 0.2304 也高于后者的 0.2022（Table 1），表明轨迹引导的显式控制优于纯文本隐式控制。

- **基于首帧编辑的视频生成**：如 **AnyV2V**（论文中标注为 [25]），通过编辑第一帧并传播到后续帧实现视频编辑。ReVideo 在此基础上增加了用户交互式的运动轨迹控制，将编辑从纯内容修改扩展到内容与运动的联合定制。

- **基于文本的区域重生成**：如 **Pika**（论文中标注为 [1]），支持局部区域编辑但依赖文本描述。ReVideo 在文本对齐和人类评估上均优于 Pika（Table 1），且 Pika 在添加新物体时存在失败案例（Figure 13），说明纯文本驱动难以精确控制运动。

- **轨迹引导的视频生成**：论文引用了交互友好的轨迹线作为运动控制信号（[52, 47]），但 ReVideo 的独特贡献在于将轨迹控制与局部内容编辑解耦，而非简单地将轨迹作为全局生成条件。

### 核心技术贡献的因果机制

ReVideo 的方法设计围绕一个核心瓶颈展开：**未编辑区域本身携带稠密的视觉与帧间运动信息，扩散模型倾向于从中推断编辑区域的运动，从而淹没用户指定的稀疏轨迹控制**。这一耦合问题的因果链条如下：

1. **问题根因**：在局部编辑中，未编辑内容提供了强烈的视觉和运动先验。当模型同时接收内容条件（修改后的首帧）和运动条件（轨迹线）时，未编辑区域的信息通过扩散模型的时空注意力机制“泄漏”到编辑区域，导致运动控制失效。

2. **解耦训练策略**：为解决上述耦合，ReVideo 采用三阶段训练策略（Figure 3）：
   - **阶段一（运动先验训练）**：仅在运动条件下训练，建立轨迹控制能力。
   - **阶段二（解耦训练）**：引入内容条件，但关键创新在于**训练数据构造**——将编辑区域与未编辑区域来自两个不同视频，通过掩码拼合（$V = V_1 \cdot M + V_2 \cdot (1 - M)$，Figure 4）。这迫使模型无法从未编辑区域推断编辑区域的运动，从而实现内容保持与运动定制的解耦。
   - **阶段三（去块微调）**：解耦训练后编辑边界可能出现块效应。此阶段仅微调控制模块和基础模型（SVD）中时空自注意力层的 Key/Value 嵌入（$W_k$, $W_v$），在消除块伪影的同时保持局部运动控制能力（Figure 7, Figure 11）。

3. **时空自适应融合模块（SAFM）**：SAFM 通过预测与编辑掩码 $M$ 和时间步 $t$ 相关的融合权重图 $\Gamma$（Equation 5: $\mathbf{f}_c = E_c(\mathbf{c}_{con}) \cdot \mathbf{r} + E_m(\mathbf{c}_{mot}) \cdot (1 - \mathbf{r})$, $\mathbf{r} = \mathcal{H}(\mathbf{M}, t)$），在扩散采样的不同时间步和不同空间位置自适应地融合内容与运动特征（Figure 5）。消融实验证明，SAFM 相较于直接求和特征融合能实现更准确的轨迹引导；移除时间自适应则导致编辑边界伪影（Figure 7）。

### 适用边界与局限

ReVideo 的能力边界受以下因素制约：

- **基础模型生成先验不足**：当 SVD 对特定场景或物体的生成质量较差时，编辑区域的再生质量会受限。这是所有基于预训练扩散模型的编辑方法的共性局限。
- **长视频编辑误差累积**：尽管 ReVideo 展示了处理 90 帧视频的能力（Figure 12），长视频编辑仍存在误差累积问题，逐帧传播的误差可能随时间放大。
- **动态遮挡与复杂交互未专门优化**：当前方法未针对编辑区域与其他物体的动态遮挡、复杂物理交互等场景进行专门设计，在这些情况下的鲁棒性有待验证。
- **不规则编辑区域的泛化性**：虽然 ReVideo 在矩形编辑区域上训练，但展示了对不规则区域的鲁棒性（Figure 9），然而这一泛化能力的边界（如极端形状、多区域复杂交互）尚未充分探索。

### 开放问题

1. **基础模型先验增强**：如何在不显著增加计算成本的前提下，提升基础模型在生成先验不足场景下的编辑质量？可能的路径包括引入轻量级适配器或检索增强生成。
2. **长视频一致性**：如何设计更有效的时间一致性机制以减少长视频编辑中的误差累积？滑动窗口策略或层次化时间建模可能提供解决思路。
3. **语义增强的运动控制**：当前运动控制仅依赖轨迹线，能否结合文本提示辅助描述编辑区域的语义内容（如“旋转的风车”），实现更丰富的编辑效果？
4. **高维运动控制扩展**：能否将 2D 轨迹控制扩展到 3D 轨迹或更复杂的运动模式（如周期性运动、弹性形变），以支持更广泛的应用场景？
5. **动态场景鲁棒性**：如何使方法在存在动态遮挡、光照变化等复杂场景下保持稳定的编辑质量？可能需要引入显式的场景理解模块或物理先验。

## 原文 PDF

![[paperPDFs/NEURIPS_2024/ReVideo_Remake_a_Video_with_Motion_and_Content_Control.pdf]]
