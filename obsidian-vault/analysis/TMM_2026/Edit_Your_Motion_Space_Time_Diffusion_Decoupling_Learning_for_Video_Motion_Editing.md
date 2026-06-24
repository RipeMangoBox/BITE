---
title: "Edit-Your-Motion: Space-Time Diffusion Decoupling Learning for Video Motion Editing"
type: paper
paper_level: A
venue: TMM
year: 2026
pdf_ref: paperPDFs/TMM_2026/Edit_Your_Motion_Space_Time_Diffusion_Decoupling_Learning_for_Video_Motion_Editing.pdf
aliases:
- EYM
- Edit-Your-Motion
tags:
- TMM_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过设计时空解耦两阶段学习策略（STL）和运动注意力模块（MA），在训练过程中分离时序与空间特征学习，并在推理时利用DDIM反演保留源视频外观，从而以单样本微调实现鲁棒的动作编辑。循环因果注意力（RCA）进一步增强了帧间一致性。"
primary_logic: "在单样本微调框架下，采用两阶段训练分别学习人体动作的时序特征和源视频的外观/背景特征，结合DDIM反演噪声初始化和运动注意力模块整合骨骼与外观特征，有效解耦动作与外观，使编辑后的视频既能跟随参考骨骼动作，又保持源视频人物和背景的一致性。"
claims:
- "DDIM反演能够在U-Net中保留源视频的大部分结构特征，确保视频外观一致性。"
- "时空两阶段学习策略（STL）通过先掩码背景学习时序特征，再全帧学习空间特征，显著提升特征提取能力。"
- "循环因果注意力（RCA）替代空间注意力，直接连接前后帧，提升视频一致性。"
- "消融实验显示移除RCA、MA或STL均导致PSNR和SSIM下降（如w/o STL PSNR降至20.24）。"
---

# Edit-Your-Motion: Space-Time Diffusion Decoupling Learning for Video Motion Editing

> [!tip] 核心洞察
> 在单样本微调框架下，采用两阶段训练分别学习人体动作的时序特征和源视频的外观/背景特征，结合DDIM反演噪声初始化和运动注意力模块整合骨骼与外观特征，有效解耦动作与外观，使编辑后的视频既能跟随参考骨骼动作，又保持源视频人物和背景的一致性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Edit-Your-Motion：时空扩散解耦学习用于视频动作编辑 |
| 英文题名 | Edit-Your-Motion: Space-Time Diffusion Decoupling Learning for Video Motion Editing |
| 会议/期刊 | TMM 2026 |
| Links | [paper](https://arxiv.org/abs/2405.04496) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Edit-Your-Motion |
| Dataset | TikTok benchmark |

> [!tip] 效果简介
> - TikTok benchmark 上，L1 为 2.81E-05，对比 MagicAnimate (次优)，变化 显著降低。
> - TikTok benchmark 上，SSIM 为 0.813，对比 MagicAnimate (次优)，变化 显著提高。
> - TikTok benchmark 上，LPIPS 为 0.166，对比 MagicAnimate (次优)，变化 显著降低。

## 概述

视频动作编辑任务要求将源视频中的人物动作替换为参考骨骼序列所指定的动作，同时严格保持人物外观与背景的一致性。现有方法在该任务上存在一个根本瓶颈：在未见过的野外样本上普遍出现严重的鬼影和人体形变。其深层原因在于，这些方法未能有效解耦时空特征——前景人物的动作特征与背景外观特征在特征层面发生重叠，导致外观保持与动作对齐两个目标相互冲突。此外，依赖大规模预训练外观编码器和大量训练数据，使得现有方法难以快速适应新的域。

针对上述瓶颈，Edit-Your-Motion 提出了一套以**时空解耦**为核心机制的单样本微调框架。其核心洞察是：通过两阶段训练分别学习人体动作的时序特征和源视频的外观/背景空间特征，结合 DDIM 反演初始化和运动注意力模块整合骨骼与外观特征，可以有效解耦动作与外观，使编辑后的视频既能精确跟随参考骨骼动作，又能保持源视频人物和背景的一致性。

方法层面，Edit-Your-Motion 在三个关键设计上区别于现有工作：

- **外观保持机制**：不同于 MotionEditor（Tu et al., arXiv 2023）使用分割掩码在特征层解耦前景与背景、或 MagicAnimate（Xu et al., CVPR 2024）使用外观编码器，Edit-Your-Motion 采用 DDIM 反演初始化噪声以保留源视频的结构外观信息，并设计运动注意力模块（MA）融合骨骼与外观特征。
- **训练策略**：不同于 MotionEditor 的单阶段联合微调，Edit-Your-Motion 提出时空两阶段学习策略（STL）：第一阶段掩码背景，专注学习人体动作的时序特征；第二阶段全帧学习外观和背景的空间特征。
- **帧间一致性**：将标准空间注意力替换为循环因果注意力（RCA），直接连接当前帧的前一帧和后一帧以增强帧间依赖。

实验结果表明，Edit-Your-Motion 在 TikTok 基准和野外案例上均取得最优性能。在 TikTok 基准上，L1 误差降至 2.81E-05，FID-VID 降至 20.95；在野外案例上，PSNR 达到 23.03，SSIM 达到 0.846。消融实验证实，移除 STL 会使 PSNR 骤降至 20.24，移除 MA 则使 SSIM 降至 0.781，验证了时空解耦和运动注意力模块的关键作用。用户研究中，76.43% 的参与者偏好 Edit-Your-Motion 的文本对齐效果。

## 背景与动机

视频动作编辑旨在将源视频中的人物动作替换为参考骨骼序列所定义的目标动作，同时保持人物外观、背景及帧间一致性不退化。这一任务在虚拟人动画、短视频创作和广告制作等领域具有广泛的应用前景，但在技术上仍面临严峻挑战。

现有方法在处理训练分布内的样本时尚可接受，但在未见野外场景中普遍出现两类关键失败模式：**外观不一致**与**动作对齐失败**。具体表现为编辑后视频中出现显著鬼影、人体形变、背景抖动以及肢体错位等问题（Fig. 1）。其根本原因在于，当前主流方案未能有效解耦视频中的时空特征。一方面，基于外观编码器的方法（如 **MagicAnimate** (Xu et al., CVPR 2024)、**AnimateAnyone** (Hu, CVPR 2024)）依赖大规模预训练模型提取外观信息，但前景与背景特征在特征层高度重叠，导致外观保持与动作跟随之间产生冲突。另一方面，单样本微调方法（如 **MotionEditor** (Tu et al., arXiv 2023)）虽采用分割掩码在特征层解耦前景与背景，但其单阶段训练策略同时学习时序和空间特征，特征提取能力受限，难以在少量迭代中收敛到鲁棒解。

此外，现有方法对大型预训练外观编码器和海量训练数据的依赖，使得快速适应新域变得困难。在仅给定单个源视频的设定下，如何以轻量级微调实现外观与动作的彻底解耦，是视频动作编辑走向实用的核心瓶颈。

本文的动机正是针对上述缺口，提出一种时空扩散解耦学习框架 **Edit-Your-Motion**，通过以下思路从根本上缓解外观-动作冲突：在训练阶段，采用两阶段策略分别学习人体动作的时序特征和源视频的外观/背景空间特征；在推理阶段，利用DDIM反演保留源视频的结构外观信息，并设计运动注意力模块整合骨骼与外观特征。这一设计使得编辑后的视频既能精确跟随参考骨骼动作，又能保持源视频人物和背景的高度一致性。

## 核心创新

Edit-Your-Motion 的核心创新在于通过**时空解耦学习**从根本上解决了视频动作编辑中外观保持与动作对齐的冲突。与现有方法相比，其在以下三个关键维度上实现了机制性突破：

### 1. 外观保持机制：从特征编码到噪声反演

现有方法主要依赖两类策略保持源视频外观：**MotionEditor**（Tu et al., arXiv 2023）采用分割掩码在特征层解耦前景与背景，**MagicAnimate**（Xu et al., CVPR 2024）则使用大规模预训练外观编码器。然而，这两种方法在未见野外样本上均出现显著的鬼影和人体形变（Fig. 1），其根本原因在于前景与背景特征在特征层仍存在重叠，且对外观编码器的依赖限制了快速适应新域的能力。

Edit-Your-Motion 放弃了外观编码器范式，转而采用 **DDIM 反演**（DDIM Inversion）作为外观保持的核心机制。具体而言，对源视频进行 DDIM 反演得到的潜变量噪声，即使直接通过 U-Net 前向传播，仍能保留源视频的大部分结构特征（Fig. 3）。这一特性使得模型无需额外编码器即可在去噪生成过程中维持人物身份与背景一致性，从源头避免了外观特征与骨骼特征的冲突。

### 2. 训练策略：从单阶段联合学习到时空两阶段解耦

**MotionEditor** 采用单阶段微调，同时学习时序和空间特征。这种联合训练策略在数据有限时难以有效分离动作动态与外观静态信息，导致特征提取能力不足。

Edit-Your-Motion 提出了**时空两阶段学习策略**（Spatio-Temporal Two-Stage Learning Strategy, STL），通过分阶段训练显式解耦时序与空间特征学习：

- **第一阶段**：冻结空间注意力层，仅解冻时序注意力层和运动注意力模块（MA），同时对视频帧进行背景掩码（$v^{m} = v \cdot m$），迫使模型专注于学习人体动作的时序特征。
- **第二阶段**：去除背景掩码，解冻全部模块，使模型在已掌握动作动态的基础上学习外观和背景的空间特征。

消融实验（Table IV）定量验证了这一策略的关键作用：移除 STL（所有模块单阶段训练）导致 PSNR 从 23.03 骤降至 20.24，降幅远超其他模块的移除影响，表明时空解耦训练是模型性能的核心支柱。

### 3. 特征融合与帧间一致性：运动注意力与循环因果注意力

为缓解 ControlNet 提取的骨骼特征与 U-Net 空间特征之间的冲突，Edit-Your-Motion 设计了**运动注意力模块**（Motion Attention Module, MA）。该模块通过自注意力对骨骼特征建模（$z_{t}^{1} = Attention(Q^c, K^c, V^c)$），再通过交叉注意力将其与 U-Net 空间特征融合（$z_{t}^{2} = softmax(\frac{Linear(z_{t}^{1})(K^u)^T}{\sqrt{d}}) V^u$），最后经时序注意力增强帧间运动连贯性（Fig. 4）。消融实验表明，移除 MA 导致 PSNR 降至 21.36、SSIM 降至 0.781，验证了其在缓解特征冲突中的关键作用。

在帧间一致性方面，Edit-Your-Motion 用**循环因果注意力**（Recurrent Causal Attention, RCA）替代标准空间注意力。RCA 直接连接当前帧的前一帧和后一帧，其键（K）和值（V）由相邻帧特征拼接计算：$Q = W^Q z_{v_i}, K = W^K [z_{v_{i-1}}, z_{v_{i+1}}], V = W^V [z_{v_{i-1}}, z_{v_i}]$（Fig. 5），从而在空间特征传播过程中显式建立跨帧依赖。移除 RCA 后 PSNR 下降至 22.57、SSIM 降至 0.833，证实了其对视频一致性的贡献。

### 创新总结

上述三个 changed slots 形成了协同增效的闭环：DDIM 反演提供外观保真度的基础保障，STL 通过解耦训练使各模块各司其职，MA 和 RCA 则在特征层面分别解决骨骼-外观冲突与帧间一致性问题。这一设计使得 Edit-Your-Motion 仅需单样本微调（每阶段 300 次迭代）即可在未见野外场景中实现鲁棒的动作编辑，在 TikTok 基准和野外案例上均显著优于现有方法。

## 整体框架

![[assets/figures/papers/paper_list_l20_Edit_Your_Motion_Space_Time_Diffusion_Decoupling_Learning_for_Video_Moti/figures/002_Figure_2.jpg]]
*Figure 2: The overall pipeline of Edit-Your-Motion. We employ DDIM inversion to preserve the appearance of the source video and introduce motion attention module to resolve conflicts between skeleton and appearance features. Additionally, we replace spatial attention with recurrent causal attention to enhance inter-frame connections. Finally, to improve the feature extraction capabilities of each module, we design a spatio-temporal decoupling two-stage training strategy that requires only a fewer training iterations*

Edit-Your-Motion 的整体流程围绕一个核心洞察展开：视频动作编辑中外观保持与动作对齐的冲突，根源在于时空特征在特征层的重叠。为此，该方法构建了一条从源视频到编辑视频的完整管线，通过 DDIM 反演、运动注意力模块、循环因果注意力和时空解耦两阶段学习策略的协同，实现了单样本微调下的鲁棒动作编辑。

**输入与预处理。** 管线接收源视频与参考骨骼序列作为输入。源视频首先经过 DDIM 反演，被映射为潜变量噪声 $z^* = \mathrm{DDIM-inv}(\mathcal{E}(x))$。这一操作的关键作用在于：反演得到的噪声即使直接通过 U-Net，仍能保留源视频的大部分结构特征，从而为后续生成提供强外观先验。同时，参考骨骼通过骨骼偏移算法进行位置调整，以缓解编辑中常见的鬼影问题。

**特征提取与融合。** 管线的核心是运动注意力模块。ControlNet 从参考骨骼中提取运动特征，U-Net 从反演潜变量中提取空间外观特征，两者在 MA 中通过自注意力、交叉注意力和时序注意力的级联进行融合。具体而言，ControlNet 特征先经自注意力建模骨骼内部依赖，再通过交叉注意力与 U-Net 空间特征对齐，最后经时序注意力增强帧间运动连贯性。这一设计替代了 MotionEditor 等方法的双分支结构，以轻量方式缓解了骨骼与外观特征的冲突。

**帧间一致性增强。** 标准空间注意力仅作用于单帧内部，无法显式建模帧间依赖。Edit-Your-Motion 将其替换为循环因果注意力，RCA 的查询来自当前帧，而键和值分别由前一帧与后一帧拼接而成，使空间特征能够沿时间轴传播，从而提升整个生成视频序列的一致性。

**时空解耦两阶段训练。** 训练策略是该方法区别于现有工作的关键设计。第一阶段，冻结空间注意力层，仅解冻时序注意力层和运动注意力模块，同时对背景进行掩码处理，使模型专注于学习人体动作的时序特征。第二阶段，取消背景掩码，解冻全部模块，让模型学习外观和背景的空间特征。这种解耦避免了单阶段训练中时序与空间特征相互干扰的问题，消融实验表明，去除 STL 后 PSNR 从 23.03 降至 20.24，降幅显著。

**推理流程。** 推理时，源视频经 DDIM 反演得到初始潜变量，参考骨骼特征与外观特征通过运动注意力模块注入 U-Net 的去噪过程，最终生成既跟随参考动作、又保持源视频人物与背景一致性的编辑视频。

整个管线的模块关系可概括为：DDIM 反演提供外观锚点，运动注意力模块融合运动与外观特征，循环因果注意力保障帧间连贯性，时空两阶段学习策略确保各模块在少量迭代内获得充分的特征提取能力。

## 核心模块与公式推导

Edit-Your-Motion 的核心架构围绕三个关键模块展开：**运动注意力模块（MA）**、**循环因果注意力（RCA）** 和 **时空两阶段学习策略（STL）**。这些模块协同工作，在单样本微调框架下实现时空特征的有效解耦。

### 运动注意力模块（MA）

运动注意力模块的设计目标是缓解 ControlNet 提取的骨骼特征与 U-Net 空间特征之间的冲突。该模块由自注意力、交叉注意力和时序注意力三个子层组成（Fig. 4）。

模块首先对 ControlNet 输出的骨骼特征进行自注意力建模：

$$z_{t}^{1} = Attention(Q^c, K^c, V^c)$$

其中 $Q^c$、$K^c$、$V^c$ 均来自 ControlNet 的骨骼特征。随后，通过交叉注意力将骨骼特征与 U-Net 的空间特征进行融合：

$$z_{t}^{2} = softmax\left(\frac{Linear(z_{t}^{1})(K^u)^T}{\sqrt{d}}\right) V^u$$

这里 $K^u$ 和 $V^u$ 来自 U-Net 的空间特征，$d$ 为特征维度。这种设计使骨骼特征能够与空间特征进行匹配，从而在保留源视频外观的同时实现动作对齐。消融实验表明，移除 MA（直接将 ControlNet 特征输入 U-Net）会导致 PSNR 从 23.03 骤降至 21.36，SSIM 从 0.846 降至 0.781（Table IV），验证了该模块在缓解特征冲突中的关键作用。

### 循环因果注意力（RCA）

为增强视频帧间一致性，RCA 替代了标准的空间注意力机制。其核心思想是让当前帧直接感知前后帧的信息（Fig. 5）：

$$Q = W^Q z_{v_i}, \quad K = W^K [z_{v_{i-1}}, z_{v_{i+1}}], \quad V = W^V [z_{v_{i-1}}, z_{v_i}]$$

其中 $z_{v_i}$ 为当前帧特征，$z_{v_{i-1}}$ 和 $z_{v_{i+1}}$ 分别为前一帧和后一帧特征。键（K）由前后帧拼接而成，值（V）由前一帧和当前帧拼接而成。这种非对称设计使空间特征能够在整个视频序列中传播，从而提升时序一致性。消融实验中，移除 RCA（即保留标准空间注意力）导致 PSNR 从 23.03 降至 22.57，SSIM 从 0.846 降至 0.833（Table IV）。

### 时空两阶段学习策略（STL）

STL 是 Edit-Your-Motion 实现时空解耦的核心训练策略，分为两个阶段：

**第一阶段**聚焦于学习人体动作的时序特征。训练时对背景进行掩码处理：

$$v^{m} = v \cdot m$$

仅保留人体区域，并从掩码后的视频中提取骨骼：

$$v_{sk} = \mathrm{network}^{\mathrm{k}}(v^{m})$$

在此阶段，仅解冻时序注意力层和运动注意力模块的参数，优化目标为：

$$L = \mathbb{E}_{z_{t}^{m}, \epsilon \sim \mathcal{N}(0,1), t, p, f_{sk}, f_{v}} \left[ \left\| \epsilon - \epsilon_{\theta}^{unet}(z_{t}^{m}, t, p, f_{sk}) \right\|_{2}^{2} \right]$$

其中 $z_{t}^{m}$ 为掩码视频的潜变量，$p$ 为文本提示，$f_{sk}$ 为骨骼特征。

**第二阶段**不再遮挡背景，使模型学习外观和背景的空间特征。此阶段解冻所有模块参数，但训练迭代次数较少。消融实验表明，将两个阶段合并为单阶段训练（w/o STL）会导致 PSNR 降至 20.24，SSIM 降至 0.813（Table IV），证明解耦训练策略对特征提取能力的显著提升。

### 推理阶段的 DDIM 反演

推理时，对源视频进行 DDIM 反演以获取保留结构信息的初始潜变量：

$$z^{*} = \mathrm{DDIM-inv}(\mathcal{E}(x))$$

其中 $\mathcal{E}$ 为 VAE 编码器。如 Fig. 3 所示，DDIM 反演得到的噪声直接通过 U-Net 仍能保留源视频的大部分结构特征，这是外观一致性的基础。随后，骨骼特征和外观特征通过运动注意力模块注入 U-Net，实现视频动作编辑。此外，推理时还采用骨骼偏移算法（Algorithm 1）调整参考骨骼位置，以缓解鬼影现象。

## 实验与分析

### 主要结果

Edit-Your-Motion 在两个核心基准上均表现出显著优势：标准 TikTok 数据集和更具挑战性的未见野外视频。

**TikTok 基准（Table II）**：在 TikTok 数据集（340 条视频序列）上，Edit-Your-Motion 在所有像素级和感知级指标上均取得最优。具体地，L1 误差降至 $2.81 \times 10^{-5}$，SSIM 达到 0.813，LPIPS 降至 0.166，FID-VID 降至 20.95。与次优方法 **MagicAnimate**（Xu et al., CVPR 2024）相比，这些指标均实现了显著改善，表明该方法在标准人体动作编辑场景下能够更精准地保持外观并降低失真。

**未见野外视频（Table III, Table VI）**：在 80 条从 YouTube 收集的未见野外视频上，Edit-Your-Motion 同样展现出最强的鲁棒性。PSNR 达到 23.03，SSIM 达到 0.846，均优于 **AnimateAnyone**（Hu, CVPR 2024）等次优方法。在更细粒度的评估中（Table VI），文本对齐度（TA）达到 26.74，时序一致性（TC）达到 0.941，均显著超越 **MotionEditor**（Tu et al., arXiv 2023）等单样本编辑方法。LPIPS-N（0.092）和 LPIPS-S（0.363）的降低进一步验证了该方法在减少鬼影和保持外观一致性方面的优势。

**用户研究**：在人工评估中，Edit-Your-Motion 在文本对齐偏好率上达到 76.43%，远高于对比方法，表明其生成结果更符合人类对动作准确性和视觉质量的期望。

### 消融实验

为验证各模块的因果贡献，在未见野外数据上进行了系统消融（Table IV, Fig. 9）。

**循环因果注意力（RCA）**：移除 RCA（即回退为标准空间注意力）导致 PSNR 从 23.03 降至 22.57，SSIM 从 0.846 降至 0.833。这表明 RCA 通过直接建立当前帧与前后帧的显式连接，有效增强了帧间一致性，是提升视频连贯性的关键设计。

**运动注意力模块（MA）**：移除 MA（ControlNet 骨骼特征直接输入 U-Net）导致 PSNR 骤降至 21.36，SSIM 降至 0.781。这是所有单模块消融中性能下降最剧烈的，说明 MA 在缓解骨骼特征与外观特征冲突、实现动作对齐方面起着决定性作用。

**时空两阶段学习策略（STL）**：将所有模块合并为单阶段训练（w/o STL）导致 PSNR 降至 20.24，SSIM 降至 0.813。STL 的缺失不仅损害了动作对齐，也影响了外观保持，验证了时空解耦训练对于特征提取的必要性。

**STL 迭代次数敏感性（Table V）**：当两阶段微调迭代次数均为 300 时，PSNR 达到最高（23.03）。减少任一阶段的迭代次数均会导致性能下降，表明两阶段需要充分的独立学习才能实现最优解耦效果。

**文本提示与骨干网络（Fig. 9）**：分离消融显示，文本提示、RCA、STL、MA 各自独立贡献于最终性能。此外，使用 AnimateDiff 与 Stable Diffusion v1.5 作为骨干网络的对比表明，方法对骨干架构具有一定鲁棒性。

### 定性分析

**野外场景泛化（Fig. 6, Fig. 7）**：Edit-Your-Motion 在室内外多种场景（舞蹈、武术、太极等动作类型）下均能生成高质量编辑结果。与 **Follow-Your-Pose**（Ma et al., AAAI 2024）、**MotionDirector**（Zhao et al., arXiv 2023）、**Tune-A-Video**（Wu et al., ICCV 2023）等方法相比，该方法在动作对齐、背景一致性和人体外观保持三个维度上均表现出明显优势。其他方法在复杂背景下常出现人体形变或背景扭曲（Fig. 1 红框区域），而 Edit-Your-Motion 有效抑制了这些伪影。

![[assets/figures/papers/paper_list_l20_Edit_Your_Motion_Space_Time_Diffusion_Decoupling_Learning_for_Video_Moti/figures/007_Figure_6.jpg]]
*Figure 6: 0 6 12 Fig. 6. Some examples of motion editing results for Edit-Your-Motion in the unseen in-the-wild cases. Edit-Your-Motion not only adapts to both outdoor and indoor scenes but also facilitates motion editing for a variety of movements, such as dancing, wugong, and Tai Chi. TABLE I THE DIFFERENCE BETWEEN OTHER COMPARISON METHODS AND VIDEO MOTION EDITING*

**TikTok 数据集表现（Fig. 8）**：在标准 TikTok 基准上，Edit-Your-Motion 不仅实现了动作与外观的对齐，还保证了高帧间一致性，验证了方法在受控场景下的稳定性。

![[assets/figures/papers/paper_list_l20_Edit_Your_Motion_Space_Time_Diffusion_Decoupling_Learning_for_Video_Moti/figures/013_Figure_8.jpg]]
*Figure 8: Some examples of motion editing results for Edit-Your-Motion in TikTok dataset. Edit-Your-Motion not only aligns motion and appearance but also ensures a high inter-frame consistency. TABLE IV ABLATION STUDY OF RCA, MOTION ATTENTION MODULE AND STL IN UNSEEN IN-THE-WILD CASES. ”W/O RCA” INDICATES THAT SPATIAL ATTENTION IS NOT REPLACED. ”W/O MA” INDICATES THAT THE MOTION ATTENTION MODULE IS NOT UTILIZED AND CONTROLNET FEATURES ARE DIRECTLY INPUT INTO U-NET. ”W/O STL” INDICATES THAT ALL MODULES ARE TRAINED IN ONE TRAINING STAGE*

### 关键图表结论

| 图表 | 核心结论 |
|------|----------|
| **Table II** | 在 TikTok 基准上全面超越 MagicAnimate 等基于扩散的人体动画方法 |
| **Table III** | 在未见野外视频上 PSNR/SSIM 最优，验证单样本微调框架的泛化能力 |
| **Table IV** | MA 是性能最敏感的模块，STL 和 RCA 均对最终质量有显著贡献 |
| **Table V** | 两阶段各 300 次微调迭代为最优配置 |
| **Table VI** | 在文本对齐和时序一致性上显著超越 MotionEditor，用户偏好率达 76.43% |
| **Fig. 7** | 定性展示 Edit-Your-Motion 在动作对齐、背景和人体一致性上的综合优势 |
| **Fig. 9** | 可视化消融验证各模块独立贡献及骨干网络鲁棒性 |

### 失败模式与局限

论文未明确报告失败案例或局限性分析。从方法设计推断，潜在风险包括：DDIM 反演对源视频质量的依赖（低质量源视频可能导致外观信息丢失）；骨骼偏移算法（Algorithm 1）在极端姿态变化下的适用性有待验证；单样本微调虽然高效，但对全新动作类型的泛化边界尚不明确。上述推断需通过进一步实验验证。

### 补充图表

![[assets/figures/papers/paper_list_l20_Edit_Your_Motion_Space_Time_Diffusion_Decoupling_Learning_for_Video_Moti/figures/006_Figure.jpg]]

![[assets/figures/papers/paper_list_l20_Edit_Your_Motion_Space_Time_Diffusion_Decoupling_Learning_for_Video_Moti/figures/009_Table.jpg]]
*Table: II QUANTITATIVE COMPARISON OF MAGICANIMATE, ANIMATEANYONE, CHAMP AND OUR PROPOSED EDIT-YOUR-MOTION ON THE TIKTOK BENCHMARK. THE HIGHEST SCORE IS MARKED IN BOLD. TABLE III*

![[assets/figures/papers/paper_list_l20_Edit_Your_Motion_Space_Time_Diffusion_Decoupling_Learning_for_Video_Moti/figures/010_Table.jpg]]
*Table: QUANTITATIVE COMPARISON OF MAGICANIMATE, ANIMATEANYONE, CHAMP AND OUR PROPOSED EDIT-YOUR-MOTION ON IN-THE-WILD CASES. THE HIGHEST SCORE IS MARKED IN BOLD*

![[assets/figures/papers/paper_list_l20_Edit_Your_Motion_Space_Time_Diffusion_Decoupling_Learning_for_Video_Moti/figures/012_Table.jpg]]
*Table: V SENSITIVITY STUDY. IN THE UNSEEN DATA, THE PSNR VARIES UNDER DIFFERENT COMBINATIONS OF THE NUMBER OF TWO-STAGE FINE-TUNING OF THE STL*

![[assets/figures/papers/paper_list_l20_Edit_Your_Motion_Space_Time_Diffusion_Decoupling_Learning_for_Video_Moti/figures/014_Table.jpg]]
*Table: VI QUANTITATIVE COMPARISON AND USER STUDY OF FOLLOW-YOUR-POSE, MOTIONDIRECTOR, TUNE-A-VIDEO, MOTIONEDITOR AND OUR PROPOSEDEDIT-YOUR-MOTION ON IN-THE-WILD CASES. THE HIGHEST SCORE IS MARKED IN BOLD*

## 方法谱系与知识库定位

### 任务定位：视频动作编辑

Edit-Your-Motion 定位于**视频动作编辑**任务：给定一段源视频和一段参考骨骼序列，生成新视频，使其人物外观与源视频一致，而人体动作与参考骨骼对齐。这与现有主流方法在任务设定上存在关键差异（Table I）：**MagicAnimate**（Xu et al., CVPR 2024）和 **AnimateAnyone**（Hu, CVPR 2024）等依赖参考图像和骨骼序列进行人体图像动画，而非视频到视频的动作迁移；**Champ**（Zhu et al., arXiv 2024）引入3D SMPL参数进行精细化人体动画，但仍属于图像到视频的生成范式；**MotionEditor**（Tu et al., arXiv 2023）是单样本视频动作编辑方法，与本文任务设定最为接近。

### 与基线方法的核心差异

现有方法在未见野外样本上的失败根因在于**时空特征解耦不足**。**MagicAnimate** 依赖大型预训练外观编码器（如DINOv2）来保持人物外观，但编码器提取的全局外观特征与骨骼引导的局部动作特征在特征层发生重叠冲突，导致鬼影和人体形变（Fig. 1红框标注）。**MotionEditor** 采用双分支结构和分割掩码在特征层解耦前景与背景，但其单阶段微调策略同时学习时序和空间特征，未能有效分离动作与外观的学习过程，在野外场景中仍出现外观不一致。

Edit-Your-Motion 通过三个关键机制改变这一局面：

1. **外观保持机制的替换**：放弃外观编码器，改用 **DDIM反演**（DDIM Inversion）对源视频进行潜变量噪声初始化。反演得到的噪声直接通过U-Net仍能保留源视频的大部分结构特征（Fig. 3），从而在推理阶段自然保持外观一致性，避免了额外编码器带来的特征冲突。

2. **训练策略的重构**：提出**时空两阶段学习策略**（Spatio-Temporal Two-Stage Learning Strategy, STL）。第一阶段掩码背景，仅解冻时序注意力层和运动注意力模块，专注学习人体动作的时序特征；第二阶段不遮挡背景，让模型学习外观和背景的空间特征。这种解耦训练仅需每阶段300次微调迭代，显著降低了对大量训练数据的依赖。

3. **空间注意力的重新设计**：用**循环因果注意力**（Recurrent Causal Attention, RCA）替代标准空间自注意力。RCA通过拼接前一帧和后一帧的特征作为Key和Value（Eq. 9: $Q = W^Q z_{v_i}, K = W^K [z_{v_{i-1}}, z_{v_{i+1}}], V = W^V [z_{v_{i-1}}, z_{v_i}]$），显式建立帧间依赖，使空间特征在整个视频序列中传播，增强帧间一致性。

### 方法谱系中的位置

从技术路线看，Edit-Your-Motion 处于**单样本微调**与**扩散模型视频编辑**的交叉点。与 **Tune-A-Video**（Wu et al., ICCV 2023）这类单样本文本到视频调优方法相比，Edit-Your-Motion 面向的是动作编辑这一更具约束性的子任务。与 **Follow-Your-Pose**（Ma et al., AAAI 2024）和 **MotionDirector**（Zhao et al., arXiv 2023）等骨骼引导的文本到视频生成方法相比，Edit-Your-Motion 强调源视频外观的保持而非从文本生成全新视频。

在扩散模型的使用方式上，该方法借鉴了DDIM反演在图像编辑中保持结构的思路，并将其扩展到视频域，结合ControlNet的骨骼条件注入，形成“反演保持外观 + 骨骼引导动作”的编辑范式。

### 适用边界与局限

当前方法在以下条件下表现良好：
- 源视频包含清晰可见的单人主体，背景相对稳定；
- 参考骨骼序列与源视频人物的身体比例大致匹配（通过骨骼偏移算法 Algorithm 1 进行位置调整以缓解鬼影）；
- 动作类型覆盖舞蹈、武术、太极等多种运动（Fig. 6）。

论文未明确报告以下边界条件，需要在实际应用中注意：
- **多人场景**：方法设计基于单人骨骼提取和掩码，多人交互场景下的适用性未经验证；
- **极端视角或遮挡**：骨骼提取依赖人体姿态估计器，在严重遮挡或极端视角下骨骼质量下降可能导致编辑失败；
- **大幅外观变化**：如服装与训练分布差异极大的情况，DDIM反演保留结构特征的能力可能受限；
- **长视频编辑**：当前实验基于短视频片段（TikTok数据集340个序列，YouTube野外数据80个序列），长视频的时序一致性保持能力未经验证。

### 开放问题

论文明确指出的未来方向是将 Edit-Your-Motion 应用于动画、广告、短视频等多媒体领域，探索在更广泛场景下的泛化能力。此外，从方法设计的内在限制出发，以下问题值得进一步探索：

- **与3D人体先验的融合**：当前方法仅使用2D骨骼作为动作表征，引入SMPL等3D参数化模型（类似Champ的思路）可能提升对复杂三维旋转和遮挡的处理能力；
- **外观编辑的可控性**：DDIM反演在保持外观的同时也限制了对外观进行有意识编辑的空间，如何在保持身份一致性的前提下实现服装、发型等属性的可控修改；
- **计算效率**：单样本微调虽仅需300次迭代，但仍需针对每个源视频进行训练，实时或交互式应用场景下的效率优化是实用化的关键瓶颈。

## 原文 PDF

![[paperPDFs/TMM_2026/Edit_Your_Motion_Space_Time_Diffusion_Decoupling_Learning_for_Video_Motion_Editing.pdf]]
