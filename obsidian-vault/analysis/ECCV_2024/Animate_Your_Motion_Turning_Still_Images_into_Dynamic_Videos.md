---
title: "Animate Your Motion: Turning Still Images into Dynamic Videos"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/Animate_Your_Motion_Turning_Still_Images_into_Dynamic_Videos.pdf
project_link: https://mingxiao-li.github.io/smcd/
code_link: null
aliases:
- SMCDS
- AYMTSIIDV
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过将运动集成模块（MIM）和双图像集成模块（DIIM）顺序地引入预训练的3D扩散UNet，并采用两阶段训练策略，协同地编码异构条件信号。"
primary_logic: "同时训练多模态条件集成模块会导致竞争干扰，而先训练运动模块再训练图像模块的顺序训练策略能够解耦两种信号的学习过程，从而大幅提升视频质量、运动精度和语义连贯性。"
claims:
- "两阶段训练是SMCD性能的关键：在GOT10K验证集上，两阶段训练的SMCD在FVD（335）、CLIP-SIM（29.16）、FFFDINO（0.85）和SR50（0.78）上均显著优于联合训练（FVD 385、CLIP-SIM 28.71、FFFDINO 0.83、SR50 0.69）。"
- "SMCD（集成MIM和DIIM）在视频质量和接地准确度上全面超越所有单独使用任一模块的变体，以及三种备选图像集成策略（ZC、CtrlNet、GCA）。"
- "定性结果显示SMCD在保持输入图像语义和精确执行运动轨迹方面具有明显优势，而基线模型（ModelScope、MS+MIM、GCA）则出现语义丢失或运动偏差。"
- "GOT10K validation 上 FVD = 335"
---

# Animate Your Motion: Turning Still Images into Dynamic Videos

> [!tip] 核心洞察
> 同时训练多模态条件集成模块会导致竞争干扰，而先训练运动模块再训练图像模块的顺序训练策略能够解耦两种信号的学习过程，从而大幅提升视频质量、运动精度和语义连贯性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 动画化你的运动：将静态图像转化为动态视频 |
| 英文题名 | Animate Your Motion: Turning Still Images into Dynamic Videos |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2403.10179) · [Project](https://mingxiao-li.github.io/smcd/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Scene and Motion Conditional Diffusion (SMCD) |
| Dataset | GOT10K validation |

> [!tip] 效果简介
> - GOT10K validation 上，FVD 为 335，对比 385，变化 -50。
> - GOT10K validation 上，CLIP-SIM 为 29.16，对比 28.71，变化 +0.45。
> - GOT10K validation 上，FFFDINO 为 0.85，对比 0.83，变化 +0.02。

## 概要

**核心问题**：现有的文本到视频生成方法在引入额外控制信号时，通常孤立地使用语义条件（如初始帧图像）或运动条件（如边界框轨迹），难以在单一框架内同时提供丰富的场景语义与精确的运动轨迹。这种分离导致生成视频在语义一致性与运动精确性之间存在固有冲突——强化一方往往以牺牲另一方为代价。

**核心发现**：当同时训练多模态条件集成模块时，二者会产生竞争性干扰；而将运动模块与图像模块分阶段顺序训练，能够有效解耦两种信号的学习过程，从而大幅提升视频质量、运动精度和语义连贯性。这一发现构成了本文方法设计的基石。

**方法定位**：本文提出的**Scene and Motion Conditional Diffusion (SMCD)** 模型，以预训练的文本到视频扩散模型 **ModelScope**（Wang et al., arXiv 2023）为骨干，通过引入两个专用模块——运动集成模块（MIM）和双图像集成模块（DIIM）——并采用两阶段训练策略，首次实现了场景语义、物体运动轨迹与文本描述三类异构条件的协同编码。在方法谱系上，SMCD 属于基于扩散模型的可控视频生成范式，与 **TrackDiffusion**（Li et al., arXiv 2023）等运动控制方法形成直接对比。

**主要结果**：在 GOT10K 验证集上，SMCD 的两阶段训练方案相比联合训练在各项指标上均有显著提升：FVD 从 385 降至 335，CLIP-SIM 从 28.71 提升至 29.16，FFFDINO 从 0.83 提升至 0.85，SR50 从 0.69 提升至 0.78（Supplementary Table 1）。定性结果表明，SMCD 在保持输入图像语义和精确执行运动轨迹方面明显优于基线模型，而 ModelScope 及仅集成运动模块的变体则出现语义丢失或运动偏差（Fig. 3, Supplementary Fig. 2）。

**局限与开放问题**：模型仍存在物体颜色跨帧漂移、小物体生成失败、未整合相机约束等问题，后续工作需探索如何缓解自注意力导致的语义扩散、增强小尺度运动生成的精确性，以及引入相机参数实现更全面的运动定制。



文本到视频（T2V）生成领域近年来取得了显著进展，预训练扩散模型已能根据文本描述生成时序连贯的视频片段。然而，仅依赖文本提示难以实现对生成内容的精确控制——用户往往希望同时指定“画面中有什么”和“物体如何运动”。现有方法在处理这一需求时存在明显割裂：一类方法侧重于语义条件（如初始帧图像），能保留丰富的场景细节，但缺乏对物体运动轨迹的精确约束；另一类方法专注于运动条件（如边界框序列），能控制物体的位移路径，却容易丢失图像的语义一致性。这种“语义”与“运动”条件孤立使用的范式，构成了当前场景运动定制视频生成的核心瓶颈。

**ModelScope**（Wang et al., arXiv 2023）作为典型的预训练T2V扩散模型，仅接受文本条件，无法利用初始帧图像或物体轨迹信息。**TrackDiffusion**（Li et al., arXiv 2023）虽引入了边界框轨迹控制，但未整合初始帧的语义约束，导致生成视频在视觉内容上偏离用户意图。这些方法的共同缺陷在于：缺乏一个统一的框架，能够协同编码多模态异构条件信号，使生成的视频同时满足语义一致性与运动精确性的双重需求。

本文的动机正源于此：设计一种能够同时接受初始帧图像、边界框序列和文本描述作为条件输入的扩散模型，并通过有效的训练策略协调不同条件模块之间的学习过程，从而在保持高视频质量的前提下，实现精确的场景运动定制。



## 核心方法与创新机理

SMCD的核心创新在于**将异构条件信号的集成过程解耦为两个可顺序训练的模块**，从而解决了多模态条件在扩散模型中的竞争干扰问题。具体而言，SMCD相对于预训练的文本到视频扩散模型 **ModelScope**（Wang et al., arXiv 2023），引入了以下三个关键层面的创新：

### 1. 运动集成模块（MIM）：精确编码轨迹信号

ModelScope仅依赖文本条件控制视频生成，缺乏对物体运动轨迹的精确约束。SMCD引入了**运动集成模块（MIM）**，在每个UNet块中插入门控自注意力层，将边界框轨迹编码为位置令牌并与视觉令牌融合。具体地，对于每一帧 $f$ 中的每个物体 $i$，其边界框坐标 $b_{i,f}$ 经Fourier编码后与CLIP编码的类别标签 $f_{\mathrm{text}}(c_i)$ 通过MLP融合生成位置令牌 $s_{i,f}$：

$$s_{i,f} = \mathrm{MLP}(\mathrm{Fourier}(b_{i,f}), f_{\mathrm{text}}(c_i))$$

随后，位置令牌与视觉令牌拼接并通过门控自注意力层注入运动信息：

$$z_f = z_f + \tanh(\gamma) \cdot TS(\mathrm{SelfAttn}([z_f, s_{1,f}, ..., s_{N,f}]))$$

其中可训练参数 $\gamma$ 控制位置线索的影响强度，$TS$ 表示令牌选择操作，仅保留视觉令牌部分。

### 2. 双图像集成模块（DIIM）：渐进式语义保持

ModelScope不使用初始帧图像条件，导致生成视频的语义与输入图像不一致。SMCD提出**双图像集成模块（DIIM）**，通过两种互补机制将图像特征注入生成过程：

- **零初始化卷积层**：借鉴ControlNet的设计，将条件图像特征 $x_0$ 通过零卷积逐步融入视频特征，初始时不影响生成：
  $$z_f = z_f + \mathrm{ZeroConv}(x_0)$$

- **门控交叉注意力层**：通过可训练的门控参数 $\beta$ 强化图像条件的影响，ResNet适配特征维度：
  $$\hat{x}_0 = \mathrm{ResNet}(x_0); \quad z_f = z_f + \tanh(\beta) \cdot \mathrm{CrossAttn}(q(z_f), k(\hat{x}_0), v(\hat{x}_0))$$

消融实验（Table 4）证实：单独使用MIM会损害视频质量（FVD和CLIP-SIM下降），单独使用DIIM则带来显著提升，而两者组合达到最优性能——这一结果揭示了运动控制与语义保持之间存在天然的张力，需通过协同设计才能平衡。

### 3. 两阶段训练策略：解耦信号学习的竞争

**这是SMCD方法有效性的决定性因素。**若将MIM和DIIM同时端到端训练（联合训练），两种异构条件信号的学习会产生竞争干扰。SMCD提出两阶段训练策略：

1. **第一阶段**：冻结预训练UNet，仅训练MIM，使模型学会精确编码运动轨迹；
2. **第二阶段**：冻结MIM，训练DIIM和时序注意力层，使模型在保持运动控制能力的同时学习图像语义保持。

Supplementary Table 1的消融实验提供了强有力的证据：两阶段训练在GOT10K验证集上的FVD为335，CLIP-SIM为29.16，FFFDINO为0.85，SR50为0.78，全面优于联合训练的FVD 385、CLIP-SIM 28.71、FFFDINO 0.83和SR50 0.69。这种顺序训练策略确保了两个模块各司其职，避免信号冲突。

### 创新本质：从“多条件堆叠”到“条件解耦协同”

SMCD的核心洞察在于：**同时训练多模态条件集成模块会导致竞争干扰，而先训练运动模块再训练图像模块的顺序训练策略能够解耦两种信号的学习过程。** 这一设计哲学——通过训练顺序的编排而非复杂的损失函数设计来解决多模态条件冲突——是SMCD区别于现有方法（如TrackDiffusion，Li et al., arXiv 2023）的根本特征。



SMCD（Scene and Motion Conditional Diffusion）的整体框架旨在解决一个核心瓶颈：**如何将来自初始图像的丰富场景语义与来自边界框序列的精确运动轨迹，协同地注入到一个预训练的文本到视频扩散模型中，而避免两种异构条件信号在训练中产生竞争干扰**。

该框架以预训练的文本到视频扩散模型 **ModelScope**（Wang et al., arXiv 2023）为骨干网络，在其3D扩散UNet的基础上，顺序引入了两个专用条件集成模块，并通过两阶段训练策略解耦其学习过程。

**输入与输出流**

模型的输入由三类异构信号构成：
- **初始帧图像** $v_0$：提供整个视频的场景语义和视觉外观锚点。
- **物体轨迹** $O$：由一系列边界框坐标和对应的物体类别标签组成，定义了视频中每个物体的精确运动路径。
- **文本描述** $c$：提供全局语义上下文，例如“一头正在行走的河马”。

模型输出为一段视频序列 $V = \{v_1, v_2, ..., v_F\}$，该序列需同时满足三项约束：忠实保持初始帧的语义细节、精确执行给定的运动轨迹、以及维持时序连贯的视频质量。

**Pipeline 模块与数据流**

SMCD 的生成流程（参见 Figure 2）由以下模块串联构成：

1.  **VAE Encoder**：将输入图像 $v_0$ 和待去噪的视频帧编码至潜在空间，得到潜在表示 $Z_t$ 和图像特征 $x_0$。
2.  **3D Diffusion UNet（冻结的骨干网络）**：继承自 ModelScope 的预训练权重，在训练中保持冻结。其内部层负责处理空间自注意力（公式 $z_f = z_f + \mathrm{SelfAttn}(z_f)$）、文本交叉注意力（公式 $z_f = z_f + \mathrm{CrossAttn}(z_f, f_{\mathrm{text}}(c))$）和时序注意力（公式 $Z = Z + \mathrm{TempAttn}(Z)$），以维持基本的视频生成能力。
3.  **运动集成模块（MIM）**：在每个UNet块中引入**门控自注意力层**，专门处理物体轨迹 $O$。它首先通过MLP将Fourier编码的边界框坐标与CLIP编码的类别标签融合，生成位置令牌 $s_{i,f}$（公式 $s_{i,f} = \mathrm{MLP}(\mathrm{Fourier}(b_{i,f}), f_{\mathrm{text}}(c_i))$）；随后，在拼接的视觉令牌和位置令牌上执行门控自注意力（公式 $z_f = z_f + \tanh(\gamma) \cdot TS(\mathrm{SelfAttn}([z_f, s_{1,f}, ..., s_{N,f}]))$），通过可训练的零初始化门控标量 $\gamma$ 控制运动线索的注入强度。
4.  **双图像集成模块（DIIM）**：由两个互补的组件构成，负责将初始帧的语义细节注入生成过程：
    -   **零初始化卷积层（ZeroConv）**：将图像特征 $x_0$ 通过零卷积逐步融合到视频特征中（公式 $z_f = z_f + \mathrm{ZeroConv}(x_0)$），确保训练初期不扰动原始生成过程。
    -   **门控交叉注意力层（Gated Cross-Attention）**：通过可训练的门控标量 $\beta$ 进一步强化图像条件的影响（公式 $z_f = z_f + \tanh(\beta) \cdot \mathrm{CrossAttn}(q(z_f), k(\hat{x}_0), v(\hat{x}_0))$），其中 $\hat{x}_0$ 为经过ResNet适配的图像特征。
5.  **VAE Decoder**：将去噪后的潜在表示解码为最终的RGB视频。

**核心洞察：两阶段训练策略**

SMCD 框架的决定性设计在于其**两阶段训练策略**。若将MIM和DIIM进行端到端联合训练，两种异构条件信号会相互竞争，导致性能显著下降。消融实验（Supplementary Table 1）为该洞察提供了强证据：在GOT10K验证集上，两阶段训练的SMCD在FVD（335 vs. 385）、CLIP-SIM（29.16 vs. 28.71）、FFFDINO（0.85 vs. 0.83）和SR50（0.78 vs. 0.69）上全面优于联合训练。

该策略的具体实施为：
-   **第一阶段**：冻结预训练的UNet，仅训练**运动集成模块（MIM）**，使模型学会精确编码运动轨迹。
-   **第二阶段**：冻结已训练好的MIM，转而训练**双图像集成模块（DIIM）**和时序注意力层，使模型在已具备运动控制能力的基础上，进一步学习保持场景语义。

这种顺序训练范式解耦了运动信号和图像信号的学习过程，是SMCD能够同时实现高运动精度和高语义一致性的因果机制。在推理阶段，模型采用修改的无分类器引导策略（公式 $\hat{\varepsilon} = \varepsilon_{\theta}(Z_t, c, v_0, O) + \alpha \cdot (\varepsilon_{\theta}(Z_t, c, v_0, O) - \varepsilon_{\theta}(Z_t, \varnothing, v_0, O))$），通过引导标量 $\alpha$ 平衡条件与无条件评分估计，进一步提升生成质量。



### 基础骨干：3D扩散UNet的注意力层

SMCD构建于预训练的文本到视频扩散模型**ModelScope**（Wang et al., arXiv 2023）之上。其骨干网络是一个3D扩散UNet，包含三类核心注意力层，构成后续模块插入的基础架构：

**空间自注意力**（Spatial Self-Attention）在每一帧内对视觉令牌 $z_f$ 施加空间维度的自注意力，增强帧内视觉上下文编码：

$$z _ { f } = z _ { f } + \mathrm { S e l f A t t n } ( z _ { f } )$$

**文本交叉注意力**（Text Cross-Attention）通过交叉注意力将图像标题 $c$ 的文本语义 $f_{\mathrm{text}}(c)$ 集成到每一帧中：

$$z _ { f } = z _ { f } + \mathrm { C r o s s A t t n } ( z _ { f } , f _ { \mathrm { t e x t } } ( c ) )$$

**时序注意力**（Temporal Attention）在视频序列的不同帧之间整合上下文，确保时序连贯性：

$$Z = Z + { \mathrm { T e m p A t t n } } ( Z )$$

这三层构成了ModelScope处理空间语义、文本条件与时序一致性的基础框架，但该框架本身不支持运动轨迹和初始帧图像的直接条件注入。

---

### 运动集成模块（MIM）

MIM的目标是将边界框轨迹 $O = \{(b_{i,f}, c_i)\}$ 编码为可注入UNet的位置信号，其中 $b_{i,f}$ 表示物体 $i$ 在第 $f$ 帧的边界框坐标，$c_i$ 为物体类别标签。

**位置令牌生成**：首先通过MLP融合Fourier编码的边界框坐标与CLIP编码的类别标签，生成每个物体在每帧的位置令牌 $s_{i,f}$：

$$s _ { i , f } = \mathrm { M L P } ( \mathrm { F o u r i e r } ( b _ { i , f } ) , f _ { \mathrm { t e x t } } ( c _ { i } ) )$$

**门控自注意力注入**：将位置令牌 $s_{1,f}, ..., s_{N,f}$ 与视觉令牌 $z_f$ 拼接后执行自注意力，并通过可训练的门控标量 $\gamma$ 控制位置线索的影响强度：

$$z _ { f } = z _ { f } + \operatorname { t a n h } ( \gamma ) \cdot T S ( \mathrm { S e l f A t t n } ( [ z _ { f } , s _ { 1 , f } , . . . , s _ { N , f } ] ) )$$

其中 $TS(\cdot)$ 表示仅提取视觉令牌对应输出的切片操作。门控机制 $\tanh(\gamma)$ 使模型在训练初期可抑制位置信号的影响，逐步学习融合运动信息。

---

### 双图像集成模块（DIIM）

DIIM负责将初始帧图像 $v_0$ 的语义信息注入视频生成过程，由两个互补的子模块组成：

**零卷积层**（ZeroConv）：利用零初始化卷积将条件图像特征 $x_0$ 逐步融入视频特征，训练初期输出为零，避免干扰预训练权重：

$$z _ { f } = z _ { f } + \mathrm { Z e r o C o n v } ( x _ { 0 } )$$

**门控交叉注意力**（Gated Cross-Attention）：通过ResNet将图像特征 $x_0$ 适配为 $\hat{x}_0$，再以交叉注意力形式注入，并通过可训练门控标量 $\beta$ 调制影响强度：

$$\hat { x } _ { 0 } = \mathrm { R e s N e t } ( x _ { 0 } ) ; \quad z _ { f } = z _ { f } + \operatorname { t a n h } ( \beta ) \cdot \mathrm { C r o s s A t t n } ( q ( z _ { f } ) , k ( \hat { x } _ { 0 } ) , v ( \hat { x } _ { 0 } ) )$$

两个子模块协同工作：ZeroConv提供逐层渐进的特征融合，门控交叉注意力则强化图像条件在全局语义层面的引导。

---

### 训练目标与推理引导

**训练目标**：SMCD采用标准扩散模型的简单损失函数，预测添加到潜变量 $Z_t$ 中的噪声 $\epsilon_t$，条件于文本 $c$、初始帧 $v_0$ 和物体轨迹 $O$：

$$\mathcal { L } = \mathbb { E } _ { t , \epsilon _ { t } \sim \mathcal { N } ( 0 , 1 ) } [ | \epsilon _ { t } - \epsilon _ { \theta } ( Z _ { t } , c , v _ { 0 } , O ) | _ { 2 } ^ { 2 } ]$$

**推理引导**：推理时采用修改的无分类器引导，通过引导标量 $\alpha$ 结合条件与无条件评分估计：

$$\hat { \varepsilon } = \varepsilon _ { \theta } ( Z _ { t } , c , v _ { 0 } , O ) + \alpha \cdot ( \varepsilon _ { \theta } ( Z _ { t } , c , v _ { 0 } , O ) - \varepsilon _ { \theta } ( Z _ { t } , \varnothing , v _ { 0 } , O ) )$$

训练期间通过预定义概率随机丢弃文本条件 $c$，使模型同时学习条件与无条件分布。

---

### 两阶段训练策略

SMCD的核心洞察在于：**同时训练多模态条件集成模块会导致竞争干扰**。因此采用两阶段训练：

1. **第一阶段**：冻结预训练UNet，仅训练MIM，使模型学会将边界框轨迹编码为运动信号。
2. **第二阶段**：冻结MIM，训练DIIM和时序注意力层，使模型在保持运动控制能力的同时学会图像语义保持。

消融实验（Supplementary Table 1）验证了这一策略的决定性作用：两阶段训练的SMCD在GOT10K验证集上FVD达到335，显著优于联合训练的385；CLIP-SIM从28.71提升至29.16，SR50从0.69跃升至0.78。此外，交换MIM和DIIM注意力层的顺序对整体性能影响极小，表明架构具有良好的鲁棒性。



## 实验与关键发现

### 主实验结果

SMCD在GOT10K验证集上进行了系统评估，与**ModelScope**（Wang et al., arXiv 2023）和**TrackDiffusion**（Li et al., arXiv 2023）两个基线方法进行了对比。如Table 1所示，SMCD在视频质量指标FVD上显著超越两种对比方法，同时在地标准确度指标SR50上也取得了明显优势。具体而言，在GOT10K验证集上，SMCD取得了FVD 335、FFFDINO 0.85、SR50 0.783的成绩，而联合训练变体仅达到FVD 385、FFFDINO 0.83、SR50 0.69（Supplementary Table 1），这验证了所提出的两阶段训练策略的有效性。


![[assets/figures/papers/paper_list_l25_Animate_Your_Motion_Turning_Still_Images_into_Dynamic_Videos/figures/003_Table_1.jpg]]
*Table 1: Comparison with current methods on the validation split of GOT10K*

![[assets/figures/papers/paper_list_l25_Animate_Your_Motion_Turning_Still_Images_into_Dynamic_Videos/figures/008_Table_1.jpg]]
*Table 1: Ablation on training scheme and model design*

在图像集成策略的对比实验中（Table 2和Table 3），SMCD所采用的零卷积与门控交叉注意力组合方案（ZC+GCA）在两个数据集上均表现最优：在GOT10K上FVD为335，在YTVIS2021上FVD为329，且地标准确度接近真实视频的水平。定性对比（Fig. 3及Supplementary Fig. 2）进一步显示，基线模型（ModelScope、MS+MIM、GCA）在生成过程中出现语义丢失或运动轨迹偏差，而SMCD能够同时保持输入图像的复杂语义并精确执行给定的边界框运动轨迹。


![[assets/figures/papers/paper_list_l25_Animate_Your_Motion_Turning_Still_Images_into_Dynamic_Videos/figures/004_Table_2.jpg]]
*Table 2: Comparison between different image integration strategies on video quality, the results are reported on the validation splits of GOT10K and YTVIS2021*

![[assets/figures/papers/paper_list_l25_Animate_Your_Motion_Turning_Still_Images_into_Dynamic_Videos/figures/005_Table_3.jpg]]
*Table 3: Comparison between different image integration strategies on grounding accuracy*

### 消融实验

**模块贡献分析**（Table 4）：对MIM和DIIM两个核心模块的消融揭示了它们各自的作用机制。单独集成运动模块（MIM）会对视频质量产生负面影响，表现为FVD和CLIP-SIM指标的恶化；而单独集成双图像模块（DIIM）则能带来FVD和FFFDINO的显著提升。当两者组合使用时（即完整的SMCD），模型在语义一致性和运动控制两方面均达到最优，证实了两个模块的互补性。


![[assets/figures/papers/paper_list_l25_Animate_Your_Motion_Turning_Still_Images_into_Dynamic_Videos/figures/006_Table_4.jpg]]
*Table 4: Ablation on the impact of each component in SMCD on GOT10K val. set*

**训练策略消融**（Supplementary Table 1）：两阶段训练是SMCD性能的关键。在GOT10K验证集上，两阶段训练的SMCD在所有指标上均优于联合训练：FVD从385降至335（降低50），CLIP-SIM从28.71提升至29.16（+0.45），FFFDINO从0.83提升至0.85（+0.02），SR50从0.69提升至0.78（+0.09）。这一结果验证了核心洞察——先训练运动模块再训练图像模块的顺序策略能够解耦两种异构条件信号的学习过程，避免联合训练中的竞争干扰。

**架构鲁棒性验证**（Supplementary Table 1）：交换MIM和DIIM注意力层的顺序对整体性能影响极小，表明所提架构具有良好的鲁棒性。

### 失败模式分析

尽管SMCD在整体性能上表现出色，但仍存在若干已知局限：

1. **物体颜色漂移**（Supplementary Fig. 3）：自注意力层可能导致语义信息在物体内部扩散，造成颜色在不同帧间逐渐改变，例如火车头的颜色从蓝色渐变为红色。
2. **小物体忽略**（Supplementary Fig. 4）：当需要生成的空间区域很小时，预训练的视频扩散模型无法有效处理，导致小物体的运动生成失败。
3. **视频抖动**：受限于相机移动和低帧率，生成的视频可能出现不稳定性，影响视觉观感。
4. **相机约束缺失**：当前SMCD仅能控制对象运动，无法模拟相机移动，限制了更全面的视频控制能力。
5. **人物视频质量受限**：受骨干模型（ModelScope）能力的限制，高分辨率人物视频的生成质量仍有待提升。


## 定位与知识库关联

**SMCD** 立足于预训练文本到视频扩散模型 **ModelScope**（Wang et al., arXiv 2023）的肩部，将其从纯文本条件生成扩展为场景与运动双重条件驱动的定制化视频生成。其核心贡献并非重新设计扩散架构，而是在冻结的3D UNet骨干上植入两个轻量级条件集成模块——运动集成模块（MIM）和双图像集成模块（DIIM）——并通过两阶段训练策略解耦异构信号的学习过程。

在运动控制视频生成这一子领域，SMCD与 **TrackDiffusion**（Li et al., arXiv 2023）形成直接对比。TrackDiffusion同样面向多目标轨迹驱动的视频生成，但SMCD在GOT10K验证集上显著超越前者（Table 1），其优势源于两点：一是同时引入了初始帧图像条件以保持场景语义，而TrackDiffusion缺少这一约束；二是门控注意力机制提供了可调控的条件信号强度，避免运动信息对视觉质量的过度干扰。

**适用边界与能力定位**：SMCD适用于已知初始帧图像和目标边界框轨迹的定制化视频生成场景，如从单张静态图像出发，按指定路径驱动物体运动。其能力上限受限于预训练ModelScope骨干的生成质量——在高分辨率人物视频生成上表现有限。此外，当前框架仅控制对象运动，未整合相机参数，无法模拟镜头移动等全局运动效果。

**已知局限与失效模式**：
1. **物体颜色漂移**：自注意力层可能导致语义信息在物体内部扩散，造成跨帧颜色不一致（如火车头从蓝色渐变为红色），参见Supplementary Fig. 3。
2. **小物体忽略**：当目标边界框对应的空间区域过小时，预训练视频扩散模型难以有效生成该物体，参见Supplementary Fig. 4。
3. **视频抖动**：低帧率与相机移动耦合时，生成视频可能出现不稳定现象。
4. **人物视频质量受限**：受限于骨干模型能力，高质量人物视频生成仍是瓶颈。

**开放问题**：如何将相机参数纳入条件框架以实现更全面的运动定制？如何缓解自注意力导致的物体颜色漂移？如何增强模型对小物体运动生成的精确性？这些问题指向了场景运动定制视频生成从“对象级控制”向“全局场景控制”演进的关键路径。



## 原文 PDF

![[paperPDFs/ECCV_2024/Animate_Your_Motion_Turning_Still_Images_into_Dynamic_Videos.pdf]]
