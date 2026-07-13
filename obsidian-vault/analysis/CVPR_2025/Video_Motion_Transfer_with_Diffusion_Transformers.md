---
title: "Video Motion Transfer with Diffusion Transformers"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Video_Motion_Transfer_with_Diffusion_Transformers.pdf
project_link: null
code_link: null
aliases:
- VMTDT
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过优化DiT内部的跨帧注意力图并构建注意力运动流（AMF）作为损失函数，直接引导生成运动的匹配。此外，优化位置嵌入作为可调节的旋钮实现零样本迁移。"
primary_logic: "DiT的全局注意力机制天然适合提取帧间的运动线索，而无需专门的时序模块。通过构建基于软注意力加权的位移图并最小化与参考运动的差异，可以在免训练的条件下实现高质量的运动迁移。"
claims:
- "提出了注意力运动流（AMF）作为DiT运动迁移的引导信号。"
- "采用优化驱动的免训练策略，通过优化潜在表示或位置嵌入来迁移运动。"
- "DiTFlow在运动保真度（MF）上显著优于SMM、MOFT、MotionClone等基线方法。"
- "优化位置嵌入（ρ）实现零样本迁移，且对提示词保真度影响更小。"
---

# Video Motion Transfer with Diffusion Transformers

> [!tip] 核心洞察
> DiT的全局注意力机制天然适合提取帧间的运动线索，而无需专门的时序模块。通过构建基于软注意力加权的位移图并最小化与参考运动的差异，可以在免训练的条件下实现高质量的运动迁移。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于扩散变换器的视频运动迁移 |
| 英文题名 | Video Motion Transfer with Diffusion Transformers |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2412.07776) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DiTFlow |
| Dataset | DAVIS (50 videos) |

> [!tip] 效果简介
> - DAVIS (50 videos) 上，MF（所有提示的平均运动保真度） 为 0.785 (DiTFlow-5B)，对比 0.766 (SMM-5B)，变化 +0.019。
> - DAVIS (50 videos) 上，MF（所有提示的平均运动保真度） 为 0.726 (DiTFlow-2B)，对比 0.688 (SMM-2B)，变化 +0.038。

## 概要

视频运动迁移旨在将参考视频的运动模式迁移到新生成的视频内容中，同时保持对文本提示的语义忠实度。现有方法（如 **SMM** (Yatim et al., CVPR 2024)、**MOFT** (Xiao et al., CVPR 2025)、**MotionClone** (Zhang et al., CVPR 2025)）主要基于U-Net架构，依赖空间平均或局部偏差来提取运动线索，难以有效利用扩散变换器（DiT）的全局时空注意力，导致运动模式提取与内容解耦困难。

本文提出 **DiTFlow**——一种专为视频扩散变换器设计的免训练运动迁移方法。其核心洞察在于：DiT的全局注意力机制天然适合提取帧间的运动线索，无需专门的时序模块。DiTFlow通过以下机制实现高质量运动迁移：

1. **注意力运动流（AMF）**：从参考视频的DiT交叉帧注意力中提取包络位移图，作为运动模板。AMF位移图能准确捕捉真实运动方向，在CogVideoX-2B和CogVideoX-5B上分别达到0.857和0.734的补丁级余弦相似度。
2. **运动引导优化**：在去噪过程中，通过最小化参考AMF与生成AMF之间的L2距离，优化潜在表示或位置嵌入，直接引导生成运动的匹配。
3. **零样本迁移**：优化位置嵌入作为可调节的旋钮，实现一次优化后对新提示的零样本运动迁移，且对提示词保真度影响更小（图像质量仅下降0.3%，而优化潜在表示下降4.4%）。

在DAVIS数据集50个视频的评估中，DiTFlow在运动保真度（MF）上一致优于所有基线方法：DiTFlow-5B达到0.785，相比SMM的0.766提升1.9%；DiTFlow-2B达到0.726，相比SMM的0.688提升3.8%。人类评估进一步验证了DiTFlow在运动一致性和提示遵循度上的优势。

**方法定位**：DiTFlow属于基于优化的免训练运动迁移范式，区别于需要训练的注入式方法。其核心贡献在于将运动引导信号从U-Net特征空间迁移至DiT的全局注意力空间，并通过优化位置嵌入实现零样本泛化。

**局限性**：生成质量受限于预训练模型能力，难以处理分布外复杂动作；运动迁移存在语义歧义性，可能将错误元素的运动映射到目标；AMF的成对计算导致内存消耗略高，但可通过分段长视频生成缓解。



### 视频运动迁移的核心挑战

视频生成领域的一个核心需求是：给定一段参考视频的运动模式，将其迁移到由任意文本提示描述的新内容上，生成外观完全不同但运动轨迹一致的新视频。这一任务被称为**运动迁移**（motion transfer），其本质困难在于如何将运动线索与视频内容精确解耦——既要忠实复现参考视频的时空动态，又要将运动正确地映射到新场景中语义对应的元素上。

### 现有方法的架构局限

当前主流的运动迁移方法几乎全部建立在**基于U-Net的视频扩散模型**之上。这些方法通过提取U-Net中间层的时空特征来表征运动，典型代表包括：

- **SMM**（Yatim et al., CVPR 2024）：利用时空扩散特征的零样本运动迁移；
- **MOFT**（Xiao et al., CVPR 2025）：从视频扩散特征中发现运动通道进行迁移；
- **MotionClone**（Zhang et al., CVPR 2025）：通过注意力损失实现运动克隆。

然而，U-Net架构存在一个根本性的瓶颈：其卷积归纳偏置导致空间平均化的特征表示，只能捕捉每个位置的局部偏差，**难以建模跨帧的长程对应关系**。这直接导致运动模式与内容的解耦不充分——在复杂场景中，基线方法常将运动错误地关联到语义不匹配的元素上（如将狗的奔跑映射到背景物体，而非目标动物）。

### 扩散变换器带来的新机遇与缺口

近年来，**扩散变换器**（Diffusion Transformer, DiT）逐渐取代U-Net成为视频生成的主流骨干（如CogVideoX系列）。DiT的核心优势在于其**全局自注意力机制**天然具备跨帧建模能力，理论上更适合提取帧间的运动对应关系。然而，现有的运动迁移方法全部针对U-Net设计，**无法直接迁移到DiT架构**——DiT缺乏U-Net特有的空间特征金字塔，其注意力图的结构和语义也与U-Net截然不同。

这一缺口意味着：尽管DiT的视频生成质量已显著超越U-Net，但在运动可控性方面，DiT用户反而缺乏有效的运动迁移工具。

### 本文动机

本文的核心动机正是填补上述缺口——**设计一种专为DiT架构定制的运动迁移方法**。具体而言，需要解决两个关键问题：

1. **如何从DiT的全局注意力中提取有效的运动表征**：DiT的交叉帧注意力天然编码了帧间补丁的对应关系，但需要将其转化为可优化的运动引导信号。
2. **如何在免训练的条件下实现高质量运动迁移**：训练一个专门的DiT运动迁移模型成本极高，因此需要一种优化驱动的免训练策略，与现有零样本运动迁移文献保持一致。

通过解决这两个问题，本文提出的DiTFlow方法旨在让DiT用户在享受更高生成质量的同时，获得不低于甚至超越U-Net方法的运动迁移能力。



## 核心方法与创新机理

DiTFlow 的核心创新在于将运动迁移从 U‑Net 架构迁移至视频扩散变换器（DiT），并围绕 DiT 的全局时空注意力机制重新设计了运动提取与引导范式。这一转变解决了两个关键瓶颈：**运动模式提取**与**内容‑运动解耦**。

### 瓶颈突破：从局部特征到全局注意力

现有运动迁移方法（如 **SMM**（Yatim et al., CVPR 2024）、**MOFT**（Xiao et al., CVPR 2025）、**MotionClone**（Zhang et al., CVPR 2025））均构建于 U‑Net 架构之上。U‑Net 的卷积归纳偏置使其倾向于空间局部平均或逐位置偏差计算，导致布局表征能力不足——在定性对比中，这些基线方法频繁将运动关联到错误元素（例如将狗的运动映射到背景，或将降落伞的形变映射到无关区域）。DiTFlow 认识到 **DiT 的全局交叉帧注意力天然适合提取帧间运动线索**，无需额外设计时序模块，从而实现了补丁级别的细粒度运动理解。

### 关键旋钮：注意力运动流（AMF）作为引导信号

DiTFlow 的核心技术旋钮是 **注意力运动流（Attention Motion Flow, AMF）**。其因果机制如下：

1. **运动模板提取**：从参考视频的 DiT 交叉帧注意力图中，通过 argmax 操作计算每对帧之间的补丁位移矩阵 $\Delta_{i,j}$，构成运动模板 $\mathrm{AMF}(z_{\mathrm{ref}}) = \{ \Delta_{i,j} \mid i,j \in [1,F] \}$。该模板编码了参考视频中每个补丁的时空对应关系。

2. **可微引导**：在生成过程中，使用软注意力加权计算当前潜在表示的连续位移矩阵 $\tilde{\Delta}_{i,j}$，保留梯度通路。然后通过最小化 AMF 损失函数进行运动引导：
   $$\mathcal{L}_{\mathrm{AMF}}(z_{\mathrm{ref}}, z_t) = ||\mathrm{AMF}(z_{\mathrm{ref}}) - \mathrm{AMF}(z_t)||_2^2$$

这一设计的决定性证据来自位移图质量验证：AMF 位移图与真实运动方向的补丁级余弦相似度达到 **0.857**（CogVideoX‑2B）和 **0.734**（CogVideoX‑5B），显著优于基于潜在最近邻的传统位移计算方法。

### 优化策略创新：双轨可优化旋钮

DiTFlow 在优化目标上引入了两个可调节旋钮：

| 旋钮 | 基线做法 | DiTFlow 做法 | 效果 |
|------|---------|-------------|------|
| **运动引导信号** | 基于 U‑Net 特征的运动向量/通道 | 基于 DiT 全局注意力的 AMF | 补丁级运动精度，MF 提升 +0.019~+0.038 |
| **优化目标** | 仅优化潜在变量或特征匹配 | 同时支持优化潜在变量 $z_t$ 和位置嵌入 $\rho_t$ | 后者实现零样本迁移，提示词保真度仅下降 0.3%（vs $z_t$ 优化的 4.4%） |

位置嵌入优化的发现尤为关键：由于位置嵌入 $\rho$ 不影响生成语义，优化 $\rho$ 实现了 **运动与内容的显式解耦**。预优化后的 $\rho$ 可直接应用于任意新提示词，在无需重新优化的情况下生成符合参考运动模式的新视频，实现了真正的零样本运动迁移。

### 证据强度总结

- **高置信度**：AMF 引导机制在定量指标（MF 0.785 vs SMM 0.766）和人类评估中均一致优于所有基线，且对温度参数不敏感（$\tau=5$ 取得最佳平衡）。
- **中置信度**：零样本迁移的泛化边界尚未在极端分布外场景下充分验证；位置嵌入优化的解耦程度依赖于预训练模型的质量。
- **需注意**：AMF 的成对计算导致内存消耗略高于先前方法，这是精度提升的代价。



![[assets/figures/papers/paper_list_l28_Video_Motion_Transfer_with_Diffusion_Transformers/figures/001_Figure_1.jpg]]
*Figure 1: Overview of DiTFlow. We propose a motion transfer method tailored for video Diffusion Transformers (DiT). We exploit a training-free strategy to transfer the motion of a reference video (top) to newly synthesized video content with arbitrary prompts (bottom). By optimizing DiT-specific positional embeddings, we can also synthesize new videos in a zero-shot manner*

DiTFlow 提出了一种专为视频扩散变换器（DiT）设计的免训练运动迁移框架。其核心思想是：DiT 内部的全局交叉帧注意力天然编码了帧间补丁的对应关系，通过从中提取**注意力运动流（Attention Motion Flow, AMF）** 作为运动模板，并在去噪过程中以该模板为优化目标引导生成，即可将参考视频的运动模式迁移到任意文本提示描述的新内容上。

整个 pipeline 由三个核心模块串联构成，输入输出流清晰：

**1. 注意力运动流提取模块**

给定一段参考视频，首先将其编码为潜空间表示 $z_{\text{ref}}$，并在时间步 $t=0$、空文本条件下送入 DiT 去噪网络。从 DiT 的某一中间 Transformer 块（5B 模型使用第 20 块，2B 模型使用第 15 块）提取所有注意力头的平均 Key 和 Query 特征，进而计算任意两帧 $i$ 与 $j$ 之间的交叉帧注意力图 $A_{i,j}^{\otimes}$。对该注意力图执行 argmax 操作，找到每个补丁在另一帧中的最匹配位置，构建补丁位移矩阵 $\Delta_{i,j}$。所有帧对的位移矩阵集合即构成参考视频的 AMF 运动模板：

$$\mathrm{AMF}(z_{\text{ref}}) = \{ \Delta_{i,j} \mid i,j \in [1,F] \}$$

这一模板显式刻画了参考视频中每个补丁的时空运动轨迹，是整个框架的“运动教师”。

**2. 运动引导优化模块**

在生成新视频的去噪过程中，对当前潜变量 $z_t$（或位置嵌入 $\rho_t$）进行迭代优化。具体而言，在每个去噪步，从 DiT 的同一 Transformer 块提取当前生成视频的软交叉帧注意力，通过温度参数 $\tau$ 控制的 softmax 得到平滑注意力图 $\tilde{A}_{i,j}^{\otimes}$，再以加权求和方式计算软位移矩阵 $\tilde{\Delta}_{i,j}$，保留梯度以支持反向传播。优化目标是最小化生成视频 AMF 与参考 AMF 之间的 L2 距离：

$$\mathcal{L}_{\text{AMF}} = \| \mathrm{AMF}(z_{\text{ref}}) - \mathrm{AMF}(z_t) \|_2^2$$

优化仅在去噪过程的前 20% 时间步内执行（共 5 步 Adam 优化，学习率从 0.002 线性衰减至 0.001），将运动约束注入生成过程，使输出视频的运动模式逐步逼近参考视频。

**3. 零样本迁移模块（可选）**

当优化目标从潜变量 $z_t$ 切换为位置嵌入 $\rho_t$ 时，运动信息与语义内容被解耦。预优化后的位置嵌入可作为“运动旋钮”保存下来，在后续生成中直接加载，配合任意新的文本提示即可零样本生成符合参考运动模式但内容完全不同的视频。实验表明，这一策略对提示保真度的影响极小（IQ 下降仅 0.3%，而优化 $z_t$ 下降 4.4%），实现了运动与内容的有效分离。

**输入输出流总结**：参考视频 → 潜空间编码 → DiT 块特征提取 → AMF 运动模板（离线计算一次）；文本提示 + 噪声潜变量（或预优化位置嵌入）→ 去噪过程 + AMF 引导优化 → 运动迁移后的生成视频。整个流程无需任何模型训练或微调，完全基于推理阶段的优化驱动。



DiTFlow 的核心流程由三个关键模块串联构成：注意力运动流（AMF）提取、运动引导优化、以及可选的零样本迁移。以下逐模块展开其公式化定义与变量含义。

### 注意力运动流（AMF）提取

AMF 的设计动机源于 DiT 的全局自注意力机制天然捕获帧间对应关系，无需额外时序模块。给定参考视频的潜变量 $z_{\mathrm{ref}}$，首先从前向扩散过程（$t=0$，空文本条件）的第 $n$ 个 DiT 块中提取平均后的键和查询：

$$\{Q, K\} \stackrel{n}{} \epsilon_\theta(z_{\mathrm{ref}}, \emptyset, 0, \rho)$$

随后计算帧 $i$ 与帧 $j$ 之间的交叉帧注意力图 $A_{i,j}^{\otimes}$，其中 $\tau$ 为温度参数，$d_k$ 为键的维度，$\sigma$ 为 softmax 函数：

$$A_{i,j}^{\otimes} = \sigma\left(\tau \frac{Q_i K_j^T}{\sqrt{d_k}}\right) \in \mathbb{R}^{S \times S}$$

$S$ 表示每帧的补丁（patch）数量。为构建运动模板，对 $A_{i,j}^{\otimes}$ 执行 argmax 操作，找到每个补丁 $(u,v)$ 在帧 $j$ 中的最大响应位置 $(u',v')$，形成补丁位移矩阵 $\Delta_{i,j}$：

$$\Delta_{i,j}[(u,v)] = (u' - u, v' - v)$$

将所有帧对的位移矩阵集合定义为注意力运动流：

$$\mathrm{AMF}(z_{\mathrm{ref}}) = \{ \Delta_{i,j} \ | \ i,j \in [1,F] \}$$

其中 $F$ 为总帧数。该集合构成了参考视频的完整运动模板。

### 运动引导优化

在生成视频的去噪过程中，对当前潜变量 $z_t$ 同样提取键和查询，计算软注意力图（保留梯度以支持反向传播）：

$$\tilde{A}_{i,j}^{\otimes} = \sigma\left(\tau \frac{\tilde{Q}_i \tilde{K}_j^T}{\sqrt{d_k}}\right)$$

基于软注意力图，通过加权和计算连续位移矩阵，避免 argmax 的不可导问题：

$$\tilde{\Delta}_{i,j}[(u,v)] = \sum_{(u',v')} \tilde{A}_{i,j}^{\otimes}[(u,v),(u',v')] \cdot (u' - u, v' - v)$$

运动引导的核心损失函数为参考 AMF 与当前生成 AMF 之间的逐元素 L2 距离：

$$\mathcal{L}_{\mathrm{AMF}}(z_{\mathrm{ref}}, z_t) = ||\mathrm{AMF}(z_{\mathrm{ref}}) - \mathrm{AMF}(z_t)||_2^2$$

优化目标为在去噪的前 $T_{\mathrm{opt}}$ 步内，对 $z_t$ 或位置嵌入 $\rho_t$ 进行 $K_{\mathrm{opt}}$ 步梯度更新，最小化 $\mathcal{L}_{\mathrm{AMF}}$。根据消融实验（Table 3(c)），Adam 优化器在运动保真度（MF）与图像质量（IQ）之间取得最佳平衡（MF 0.797, IQ 0.313）。

### 零样本迁移（可选）

当优化对象为位置嵌入 $\rho_t$ 时，由于位置嵌入不参与语义内容的编码，预优化的 $\rho_t$ 可与任意新提示组合，实现一次优化、多次生成的零样本迁移。Figure 7a 的定量结果表明，$\rho$ 优化的提示保真度下降仅为 -0.3%，远低于 $z_t$ 优化的 -4.4%，验证了运动与内容的有效解耦。



## 实验与关键发现

### 实验设置

所有实验基于CogVideoX-2B和CogVideoX-5B两个扩散变换器骨干。评估数据集取自DAVIS，选取50个视频，每个视频配3类提示（Caption、Subject、Scene），共150个运动-提示对。推理统一使用50步去噪；DiTFlow在前20%的去噪时间步内进行5步Adam优化，学习率从0.002线性衰减至0.001。AMF损失在CogVideoX-5B的第20个DiT块、2B的第15个块上计算。为公平比较，所有基线均采用相同的推理步数，并将SMM原本昂贵的DDIM反演替换为KV注入以加速。

评估指标分为两类：**图像质量（IQ）** 采用CLIPScore衡量提示保真度，**运动保真度（MF）** 通过tracklet一致性衡量生成视频与参考视频的运动相似度。基线方法包括：仅用提示词生成的Backbone（运动保真度下限）、注入参考视频KV注意力特征的Injection、基于时空扩散特征的**SMM**（Yatim et al., CVPR 2024）、从视频扩散特征发现运动通道的**MOFT**（Xiao et al., CVPR 2025）、以及通过注意力损失实现运动克隆的**MotionClone**（Zhang et al., CVPR 2025）。

### 主实验结果

Table 1汇总了DiTFlow与四个基线在两种骨干上的定量对比。在运动保真度（MF）指标上，DiTFlow在所有提示类别下均显著优于基线：

![[assets/figures/papers/paper_list_l28_Video_Motion_Transfer_with_Diffusion_Transformers/figures/004_Table_1.jpg]]
*Table 1: Metrics evaluation. We compare DiTFlow across 3 different caption setups (Caption, Subject, Scene) and against 4 baselines. We consistently score first or second in all metrics for almost all scenarios, advocating the quality of our motion transfer. Performance is consistent across two backbones with 5B and 2B parameters respectively. Best results are in bold and second best are underlined*

- **CogVideoX-5B**：DiTFlow的MF达到0.785（All），较最强基线SMM的0.766提升1.9个百分点。SMM在Subject提示下表现明显下降（MF仅0.741），而DiTFlow保持稳定。
- **CogVideoX-2B**：DiTFlow的MF达到0.726（All），较SMM的0.688提升3.8个百分点，相对优势更大。

在图像质量（IQ）方面，DiTFlow与基线持平或略优，表明运动迁移并未以牺牲内容保真度为代价。Table 1中DiTFlow在绝大多数场景下排名第一或第二。

Figure 4的定性对比揭示了DiTFlow的优势根源：基于U-Net的基线方法（SMM、MOFT、MotionClone）由于空间平均或仅考虑各位置的偏差，往往将运动关联到错误元素（例如将狗的运动映射到背景）；而DiTFlow利用DiT的全局时空注意力，能够精确定位每个补丁的运动，使运动元素的空间位置和尺寸匹配正确。

Figure 5展示了DiTFlow在多种条件下的定性结果：改变提示词可完全改变场景外观，同时保持运动一致性；即使在运动元素的位置和尺寸发生剧烈变化的情况下（如右下角示例），运动仍被正确映射到对应元素。

### 人类评估

Figure 6展示了人类评估结果。评估者从运动一致性和提示遵循度两个维度对生成样本进行Likert-5评分。DiTFlow在两个维度上均一致优于MOFT和SMM，验证了定量指标的可靠性。

### 零样本迁移

DiTFlow支持两种优化模式：优化潜在表示 $z_t$ 或优化位置嵌入 $\rho$。Figure 7a对比了两种模式的零样本效果——使用预优化的表示在新提示下直接生成，无需重新优化。优化 $\rho$ 的零样本迁移对提示保真度影响极小（IQ仅下降0.3%），而优化 $z_t$ 的零样本迁移导致IQ下降4.4%。原因在于位置嵌入不参与语义编码，优化 $\rho$ 能更好地解耦运动与内容。Figure 7b的定性示例展示了一次优化后切换提示词仍能保持目标运动模式的效果。

![[assets/figures/papers/paper_list_l28_Video_Motion_Transfer_with_Diffusion_Transformers/figures/011_Figure_7.jpg]]
*Figure 7: a lab coat on a field” “Shark chasing fish in ocean” “Zoom into a lion standing on a cliff looking towards us” (b) Qualitative evaluation Figure 7. Zero-shot performance. In (a), we quantify zeroshot effectiveness. We compare performance by optimizing each prompt (Optimized) or using pre-optimized representations with new prompts (Zero-shot). Overall, optimizing ρ allows for better preservation of IQ. This results in better zero-shot disentanglement when changing the prompt, as shown in (b)*

### 消融实验

Table 2和Table 3报告了系统的消融分析：

![[assets/figures/papers/paper_list_l28_Video_Motion_Transfer_with_Diffusion_Transformers/figures/008_Table_2.jpg]]
*Table 2: Ablation studies. We investigate our inference setups. In (a), we highlight that early blocks in DiTs contribute more to motion. In (b) and (c), we show that DiTFlow performance can be further boosted by increasing computational power*

![[assets/figures/papers/paper_list_l28_Video_Motion_Transfer_with_Diffusion_Transformers/figures/012_Table_3.jpg]]
*Table 3: Further ablations on CogVideoX-5B*

- **引导块选择**（Table 2a）：DiT的早期块（如第20块）对运动引导贡献更大，选择中间偏前的块可获得最佳MF。
- **去噪步数**（Table 2b）：将引导覆盖的去噪步数比例从20%提升至40%，MF从0.785提升至0.813，但计算成本相应增加。
- **优化步数**（Table 2c）：优化步数从5步增至10步，MF从0.785提升至0.803，表明更多优化迭代可进一步提升运动迁移效果。
- **温度参数 $\tau$**（Table 3a）：$\tau=5$ 时取得MF 0.799与IQ 0.317的最佳平衡，且方法对温度不敏感。
- **优化器选择**（Table 3b）：Adam优化器在运动迁移和图像质量之间取得最佳平衡（MF 0.797，IQ 0.313）。

### AMF位移图验证

Figure 8通过下蹲动作的可视化验证了AMF的有效性。将潜在空间最近邻方法（Figure 8c）与AMF位移图（Figure 8d）对比：最近邻方法产生噪声极大的位移，帧间内容匹配差；AMF位移图准确捕捉到人物向下的运动（黄色）和相机平移的向右运动（红色）。定量上，AMF位移图与真实运动方向的补丁级余弦相似度在CogVideoX-2B上达到0.857，在5B上达到0.734。

![[assets/figures/papers/paper_list_l28_Video_Motion_Transfer_with_Diffusion_Transformers/figures/014_Figure_8.jpg]]
*Figure 8: Displacement maps of squat motion. We visualise the displacement map between frames (a) and (b) computed on latents. The displacements are mapped to colours according to the colour wheel arrows shown. Taking the latent nearest neighbour [14] in (c) results in very noisy displacements with poor matching of content between frames. The AMF displacement in (d) captures the downwards (yellow) motion of the person and rightwards (red) motion of the panning camera better*

### 失败模式与局限性

DiTFlow的生成质量受限于预训练模型的能力边界。当参考视频包含超出预训练分布的复杂动作（如后空翻）时，运动迁移效果显著下降——这是扩散模型先验不足导致的根本性限制。

运动迁移本身存在语义歧义性：AMF仅编码了帧间的纯几何位移，未关联语义方向。当参考视频中存在多个运动元素时，DiTFlow可能将错误元素的运动映射到目标元素（例如将参考视频中狗的运动模式映射到生成视频的飞机上）。如何显式关联语义方向以约束运动迁移，是待解决的重要开放问题。

此外，AMF的成对帧计算导致内存消耗略高于先前方法，但可通过分段生成长视频来缓解。

### 补充图表

![[assets/figures/papers/paper_list_l28_Video_Motion_Transfer_with_Diffusion_Transformers/figures/005_Figure.jpg]]
*Figure: Caption “Dog running between poles in an agility course” Subject “Bear running in a garden” Scene*

![[assets/figures/papers/paper_list_l28_Video_Motion_Transfer_with_Diffusion_Transformers/figures/006_Figure.jpg]]
*Figure: “Leopard running up a snowy hill in a forest”*

![[assets/figures/papers/paper_list_l28_Video_Motion_Transfer_with_Diffusion_Transformers/figures/013_Figure.jpg]]
*Figure: (a) Frame i (c) Latent nearest neighbour*

![[assets/figures/papers/paper_list_l28_Video_Motion_Transfer_with_Diffusion_Transformers/figures/016_Table_4.jpg]]
*Table 4: Dataset snippet. Sample of DAVIS videos chosen with associated prompts from each category described in Section 5*



## 定位与知识库关联

### 与基线方法的关系

DiTFlow 的核心定位是**首个专为视频扩散变换器（DiT）设计的免训练运动迁移方法**。现有运动迁移方法均基于 U-Net 架构，其运动提取机制无法直接适配 DiT 的全局时空注意力结构，这是 DiTFlow 试图解决的根本瓶颈。

与主要基线方法的差异体现在三个关键维度：

- **运动引导信号**：现有方法依赖 U-Net 的空间平均特征或逐位置偏差来提取运动线索。**SMM**（Yatim et al., CVPR 2024）从时空扩散特征中提取运动向量，**MOFT**（Xiao et al., CVPR 2025）通过发现运动通道来迁移运动，**MotionClone**（Zhang et al., CVPR 2025）使用注意力损失实现运动克隆。这些方法均受限于 U-Net 的局部感受野，导致运动与错误元素关联（Figure 4）。DiTFlow 则利用 DiT 的交叉帧全局注意力构建注意力运动流（AMF），实现对每个补丁的细粒度时空运动捕获。

- **优化目标**：基线方法通常仅优化潜在变量或进行特征匹配。DiTFlow 同时提供两条优化路径：优化潜在表示 $z_t$ 或优化位置嵌入 $\rho_t$，最小化参考 AMF 与生成 AMF 之间的 L2 距离 $\mathcal{L}_{\mathrm{AMF}} = ||\mathrm{AMF}(z_{\mathrm{ref}}) - \mathrm{AMF}(z_t)||_2^2$。

- **零样本迁移能力**：SMM 等方法需要为每个新提示重新执行昂贵的 DDIM 反演和优化。DiTFlow 通过优化位置嵌入 $\rho$ 实现一次优化后对多个新提示的零样本迁移，且对提示保真度的影响显著更小（$\rho$ 优化仅导致 -0.3% 的图像质量下降，而 $z_t$ 优化为 -4.4%，Figure 7a）。

定量对比上，DiTFlow 在 DAVIS 数据集 50 个视频的运动保真度（MF）指标上一致优于所有基线：DiTFlow-5B 达到 0.785，相比最佳基线 SMM-5B 的 0.766 提升 +0.019；DiTFlow-2B 达到 0.726，相比 SMM-2B 的 0.688 提升 +0.038（Table 1）。人类评估同样表明 DiTFlow 在运动一致性和提示遵循度上均优于 MOFT 和 SMM（Figure 6）。

### 适用边界与局限

DiTFlow 的有效性受以下边界条件约束：

1. **预训练模型能力上限**：作为免训练方法，DiTFlow 的生成质量完全受限于底层 DiT 模型的分布覆盖范围。对于分布外（OOD）的复杂身体动作（如后空翻），预训练模型缺乏相应的运动先验，导致迁移失败。这是方法本身的根本性局限，而非实现细节问题。

2. **运动语义歧义性**：AMF 提取的是纯几何运动模式，未与特定语义方向显式关联。当参考视频包含多个运动对象时，可能将错误元素的运动映射到目标对象上（例如将狗的视频中的场景元素运动映射到飞机上）。这是一个开放问题，需要引入语义约束机制来显式关联运动来源与目标。

3. **计算开销**：AMF 的成对帧计算导致内存消耗略高于 U-Net 基线方法。具体而言，CogVideoX-2B 生成 21 帧视频约需 4 分钟（基线 3.5 分钟），5B 模型约需 8 分钟（基线 5 分钟）。论文指出可通过分段长视频生成缓解此问题，但未提供具体实现和验证。

4. **引导块选择依赖经验**：消融实验表明早期 DiT 块（如第 20 块对 5B 模型）对运动引导更有效（Table 2a），但这一选择依赖经验调参，缺乏理论指导。不同模型架构可能需要不同的块选择策略。

### 开放问题

1. **语义-运动显式关联**：如何将特定语义方向（如“狗到飞机”）显式关联，以约束运动迁移编辑，避免运动来源与目标对象之间的混淆？这是提升运动迁移可控性的关键方向。

2. **OOD 运动泛化**：如何改进方法以处理超出预训练分布的高度复杂身体运动（如后空翻）？可能的路径包括引入少量运动先验知识或与运动捕捉数据结合，但这些方案会牺牲免训练的优势。

3. **长视频生成扩展**：论文提及分段生成可缓解内存压力，但未验证分段间的运动一致性能否保持。长视频场景下的运动连续性是一个需要进一步探索的工程问题。

4. **多对象运动解耦**：当参考视频包含多个独立运动对象时，AMF 将所有运动编码为统一流场。如何解耦并选择性迁移特定对象的运动，是提升方法实用性的重要方向。



## 原文 PDF

![[paperPDFs/CVPR_2025/Video_Motion_Transfer_with_Diffusion_Transformers.pdf]]
