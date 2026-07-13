---
title: "Reenact Anything: Semantic Video Motion Transfer Using Motion-Textual Inversion"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/Reenact_Anything_Semantic_Video_Motion_Transfer_Using_Motion_Textual_Inversion.pdf
project_link: https://mkansy.github.io/reenact-anything/
code_link: null
aliases:
- MTI
- RASVMTUMTI
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "交叉注意力层的文本/图像嵌入 tokens（motion-text embedding）是控制生成视频运动的主要动因，通过优化这些 tokens 可迁移运动。"
primary_logic: "在图像到视频扩散模型中，外观主要从图像（潜在）输入中提取，而运动则主要通过交叉注意力中注入的文本/图像嵌入控制。利用这一解耦，可以冻结模型权重，仅优化嵌入来实现语义运动迁移。"
claims:
- "交换 CLIP 图像嵌入会改变生成视频的运动，表明嵌入直接影响运动"
- "运动文本嵌入膨胀（每帧不同 token）对运动迁移至关重要"
- "我们的方法在运动保真度上显著优于所有比较方法（Acc-Top-1 54% vs 最高 44%），且用户总体排名第一"
- "冻结模型权重可避免外观泄漏，同时保持预训练模型的泛化能力"
---

# Reenact Anything: Semantic Video Motion Transfer Using Motion-Textual Inversion

> [!tip] 核心洞察
> 在图像到视频扩散模型中，外观主要从图像（潜在）输入中提取，而运动则主要通过交叉注意力中注入的文本/图像嵌入控制。利用这一解耦，可以冻结模型权重，仅优化嵌入来实现语义运动迁移。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Reenact Anything：基于运动文本反演的语义视频运动迁移 |
| 英文题名 | Reenact Anything: Semantic Video Motion Transfer Using Motion-Textual Inversion |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](https://arxiv.org/abs/2408.00458) · [Project](https://mkansy.github.io/reenact-anything/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | motion-textual inversion |
| Dataset | Something-Something V2 subset (10 classes, 100 videos), Something-Something V2 subset |

> [!tip] 效果简介
> - Something-Something V2 subset (10 classes, 100 videos) 上，Acc-Top-1 为 54%，对比 3% (SVD)，变化 +51%。
> - Something-Something V2 subset 上，User overall rank (lower is better) 为 1.367，对比 2.822 (SVD)，变化 -1.455。
> - Something-Something V2 subset 上，Cos-Sim 为 0.696，对比 0.370 (SVD)，变化 +0.326。

## 概要

**问题瓶颈**：现有视频运动控制方法依赖稀疏信号（文本、轨迹、边界框）或空间特征对齐，难以表达复杂运动语义。文本难以精确描述运动，而基于空间特征的运动迁移方法要求源视频与目标图像空间对齐，容易注入参考视频的结构信息，造成外观泄漏。

**核心洞察**：在图像到视频扩散模型中，外观主要由图像（潜在）输入决定，而运动则通过交叉注意力中注入的文本/图像嵌入控制。这一解耦特性意味着：冻结模型权重、仅优化嵌入 tokens，即可在不泄漏外观的前提下实现语义运动迁移。

**方法定位**：本文提出 **motion-textual inversion**（运动文本反演），在预训练的图像到视频扩散模型（**Stable Video Diffusion**, Blattmann et al., 2023a）基础上，将单帧 CLIP 图像嵌入替换为可学习的运动文本嵌入 $\mathbf{m}^*$，并通过扩散损失在参考视频上优化。通过交叉注意力膨胀（每帧使用不同 token 集合，共 $(F+1) \times N$ 个 tokens），实现高时序粒度的运动表达。方法完全冻结模型权重，避免外观泄漏，同时保持预训练模型的泛化能力。

**主要结果**：在 Something-Something V2 子集（10 类，100 视频）上，运动保真度 Acc-Top-1 达 **54%**，显著优于所有对比方法（最高 44%），相较无运动输入的 SVD 基线（3%）提升 51 个百分点；用户总体排名第一（1.367 vs. 基线 2.822）。定性上，方法支持全身、面部、相机、手工等多种运动类型的跨域迁移，即使物体不对齐也能产生语义匹配的运动。

**局限性**：方法受限于预训练模型的先验，无法迁移模型未见过的复杂运动；对空间精细运动（如手指打字）效果不佳；每个运动需约 1 小时优化时间（A100 GPU）；在复杂运动或大域差距场景中失败率较高，对象运动的 Acc-Top-1 仅 36%。

### 视频运动迁移的核心挑战

将一段参考视频中的运动迁移到全新的目标图像上，是视频生成领域的一个基础性问题。其核心挑战在于：**如何从参考视频中提取纯粹的运动语义，同时完全摒弃其外观信息，并将该运动施加到外观截然不同的目标对象上**。现有方法在这一问题上面临两个关键瓶颈。

**瓶颈一：运动控制信号的表达能力不足。** 当前主流的运动控制方法依赖于稀疏的显式信号——文本描述、关键点轨迹或边界框——来指定目标运动。这些信号虽然直观，但难以捕捉复杂运动中的精细语义。例如，“一个人踉跄地走路”这一动作所包含的步态节奏、身体摆动幅度和不稳定感，很难用简单的轨迹或文本完整描述。这使得基于显式信号的方法在面对复杂运动时，往往只能生成粗糙的近似结果。

**瓶颈二：基于空间特征的运动迁移方法存在外观泄漏和不对齐失效。** 另一类方法尝试从参考视频中提取空间特征（如光流或深度图）来指导生成。这类方法要求源视频与目标图像在空间结构上高度对齐，当物体形状、姿态或类别差异较大时，迁移会严重退化。更致命的是，空间特征不可避免地携带参考视频的结构信息，导致“外观泄漏”——目标生成视频中会出现参考视频的视觉特征（如人腿结构出现在袋鼠身上），破坏了运动迁移的语义纯粹性。

### 图像到视频扩散模型中的外观-运动解耦

图像到视频（I2V）扩散模型的最新进展为上述问题提供了新的解决思路。这类模型以一张图像作为输入，生成一段以该图像为首帧的动态视频。通过观察 SVD 等预训练 I2V 模型的行为，研究者发现了一个重要的**因果解耦现象**：

- **外观由图像输入主导。** 如图 2 所示，即使文本提示指定马的颜色为“粉色”，I2V 模型仍然生成与输入图像一致的白马视频。这表明，模型的外观信息主要从图像潜变量输入中提取，而非从文本/图像嵌入中获得。

- **运动由交叉注意力中的嵌入控制。** 如图 3 所示，交换两段视频的 CLIP 图像嵌入会导致生成视频的运动发生交换：真实马的嵌入编码了“行走”运动，而玩具马的嵌入编码了“无物体移动的相机运动”。这一现象直接证明，注入到交叉注意力层的文本/图像嵌入 tokens 是控制生成视频运动的主要动因。

这一解耦意味着：**如果能够冻结模型权重，仅优化注入的嵌入 tokens，就有可能在保持预训练模型泛化能力的同时，实现纯粹的运动迁移，从根本上避免外观泄漏。**

### 本文的核心动机

基于上述观察，本文提出 **motion-textual inversion（运动文本反演）**——一种在冻结的预训练 I2V 扩散模型中，通过优化一组文本/图像嵌入 tokens 来编码参考视频运动语义的方法。该方法的核心洞见在于：

- 将运动表示为一组可学习的嵌入 tokens（称为 motion-text embedding），而非显式的空间信号或模型权重更新。
- 通过扩散损失直接在参考视频上优化这些 tokens，使其捕获视频中的语义运动。
- 在推理时，将优化后的运动文本嵌入与任意目标图像一起送入冻结模型，生成运动匹配的视频。

这种设计从根本上解决了外观泄漏问题（模型权重冻结，无法存储参考视频外观），同时利用预训练模型的强大先验实现了跨域、跨物体的语义运动迁移。

## 核心方法与创新机理

本文的核心创新在于提出 **motion-textual inversion**：一种在冻结的图像到视频扩散模型中，仅通过优化一组文本/图像嵌入 tokens 来编码并迁移参考视频运动语义的方法。相较于现有方法，其关键改变体现在以下三个层面。

### 1. 嵌入来源：从静态 CLIP 嵌入到可学习的运动文本嵌入

在基线模型 **Stable Video Diffusion (SVD)**（Blattmann et al., 2023a）中，生成视频的运动由单个预训练的 CLIP 图像嵌入 token $e$ 控制——该 token 对所有帧广播，且不经过任何针对运动的学习。本文将其替换为一组可学习的运动文本嵌入 $\mathbf{m}^*$，共包含 $(F+1) \times N$ 个 tokens（默认 $F=14, N=5$，即 75 个 tokens），并通过扩散损失直接优化：

$$\mathbf{m}^* = \underset{\mathbf{m}}{\arg\min} \ \mathbb{E}_{(\mathbf{x}_0, \mathbf{c}) \sim p_{\mathrm{data}}, (\boldsymbol{\sigma}, \mathbf{n}) \sim p(\boldsymbol{\sigma}, \mathbf{n})} \left[ \lambda_\sigma \| D_\theta(\mathbf{x}_0 + \mathbf{n}; \boldsymbol{\sigma}, \mathbf{m}, \mathbf{c}) - \mathbf{x}_0 \|_2^2 \right]$$

这一设计将运动控制从“模型权重中隐式编码”转变为“嵌入空间中显式优化”，为后续的帧级粒度控制奠定了基础。

### 2. 帧级嵌入粒度：从广播式到每帧独立 tokens

SVD 的空间交叉注意力使用同一个 token 广播至所有帧，导致时序运动粒度极为粗糙。本文提出**交叉注意力膨胀（Cross-Attention Inflation）**，将嵌入结构拆分为两个维度：

- **空间交叉注意力**：每帧使用不同的 $N$ 个 tokens（共 $F \times N$），使模型能在不同时间步关注不同的运动特征。
- **时间交叉注意力**：所有帧共享 $N$ 个 tokens，保持时序一致性。

消融实验（Fig. 7, Table 4）表明，这一膨胀是运动迁移质量的决定性因素：仅增加 token 数 $N$ 已有改善，但最大的增益来自**每帧使用不同的 tokens**（$F' = F + 1 = 15$ 时效果最优）。在 $F'=15$ 的设置下，token 维度 $N$ 对结果影响不大，进一步印证了“跨帧区别”才是关键。

### 3. 模型权重学习：从微调到完全冻结

现有运动迁移方法通常需要修改或微调扩散模型权重。例如 **MotionDirector**（Zhao et al., 2024）使用 LoRA 学习模型权重来捕获运动，**MotionClone**（Ling et al., 2024）依赖稀疏时序注意力权重。这些方法面临外观泄漏的风险——模型权重可能“记住”参考视频的结构信息，导致迁移时参考物体的特征（如人腿）出现在目标物体（如袋鼠）上。

本文的方法保持预训练 SVD 模型**完全冻结**，仅优化嵌入 tokens。这一设计基于两个关键观察（Fig. 2, Fig. 3）：
- 图像输入（潜在表示）主导生成视频的外观；
- 文本/图像嵌入 tokens 主导生成视频的运动。

通过将运动信息完全隔离在嵌入空间中，该方法从根本上避免了外观泄漏，同时保留了预训练模型的泛化能力——支持跨域（真实↔卡通）、跨物体（人↔动物）的运动迁移。

### 与基线方法的核心差异总结

| 改变槽位 | SVD 基线 | 本文方法 | 动机 |
|---------|---------|---------|------|
| 嵌入来源 | 单个 CLIP 图像嵌入 $e$，无学习 | 可学习运动文本嵌入 $\mathbf{m}^*$，通过扩散损失优化 | 将运动控制从模型权重解耦至嵌入空间 |
| 帧级粒度 | 相同 token 广播至所有帧 | 空间注意力每帧独立 tokens，时间注意力共享 tokens | 提升时序运动粒度，支持复杂运动 |
| 权重学习 | 预训练权重，无运动适配 | 模型完全冻结，仅优化嵌入 | 避免外观泄漏，保留泛化能力 |

> **证据强度说明**：上述三个 changed slots 均有 Fig. 4（框架图）、Fig. 7/Table 4（消融实验）和 Section 3.2.1/3.4.2（方法描述）的直接支撑，置信度均为 0.95。定量评估（Table 1）显示本文方法在运动保真度 Acc-Top-1 上达到 54%，显著优于最佳对比方法（44%），为上述创新提供了实证验证。

![[assets/figures/papers/paper_list_l26_Reenact_Anything_Semantic_Video_Motion_Transfer_Using_Motion_Textual_Inv/figures/004_Figure_4.jpg]]
*Figure 4: Method overview. The baseline image-to-video difusion model, Stable Video Difusion [Bla mann et al. 2023a] in our case, inputs the first frame in two places: as image (latent) concatenated with the noisy video and as image embedding (some other image-to-video difusion models may input text embeddings here instead). We propose to replace the image embedding e (shown in red in the inference block) with a learned motion-text embedding m∗ (green). The motion-text embedding is optimized directly with a regular difusion model loss on one given motion reference video $\mathbf { x } _ { 0 }$ while keeping the difusion model frozen. For best results, the motion-text embedding is inflated prior to opti...*

Reenact Anything 的核心 pipeline 围绕“运动文本嵌入”（motion-text embedding）的优化与推理展开，全程保持预训练图像到视频扩散模型权重冻结。整体流程分为两个阶段：**运动嵌入学习阶段**和**目标图像推理阶段**（Fig. 4）。

### 关键观察与设计动机

方法设计基于对图像到视频扩散模型的两个关键观察（Section 3.2）：

1. **图像输入主导外观**（Fig. 2）：在 I2VGen-XL 等模型中，即使文本指定“粉色”，输入白马图像仍生成白色马匹视频。这表明外观信息主要从图像潜在输入中提取，而非文本/图像嵌入。
2. **嵌入影响运动**（Fig. 3）：在 Stable Video Diffusion（SVD）中，交换真实马匹与玩具马的 CLIP 图像嵌入会导致输出视频的运动发生交换——真实马的嵌入编码了行走运动，玩具马的嵌入编码了无物体运动的相机运动。这表明交叉注意力中注入的嵌入 tokens 直接控制生成视频的运动。

基于上述观察，论文提出核心洞察：**外观与运动在图像到视频扩散模型中存在隐式解耦**——外观从图像潜在输入中提取，运动则主要通过交叉注意力中的文本/图像嵌入控制。因此，只需优化嵌入 tokens 即可实现运动迁移，无需修改模型权重。

### 运动嵌入学习阶段

给定一段运动参考视频 $\mathbf{x}_0$，目标是学习一组可优化的运动文本嵌入 $\mathbf{m}^*$，使其能够编码该视频的语义运动。

1. **嵌入初始化**：将预训练 SVD 中原本使用的单个 CLIP 图像嵌入 token $\mathbf{e}$ 替换为一组可学习的 tokens $\mathbf{m}$。在优化前，$\mathbf{m}$ 被膨胀为 $(F+1) \times N$ 个 tokens，其中 $F$ 为帧数，$N$ 为每帧 token 数（默认 $F=14, N=5$，共 75 个 tokens）。
2. **扩散损失优化**：冻结 SVD UNet 的所有权重，将运动文本嵌入 $\mathbf{m}$ 与参考视频的第一帧图像条件 $\mathbf{c}$ 一同送入去噪器，使用标准扩散去噪损失进行优化：
   $$\mathbf{m}^*=\underset{\mathbf{m}}{\arg\min}\mathbb{E}_{(\mathbf{x}_0,\mathbf{c})\sim p_{\mathrm{data}}(\mathbf{x}_0,\mathbf{c}),(\boldsymbol{\sigma},\mathbf{n})\sim p(\boldsymbol{\sigma},\mathbf{n})}[\lambda_\sigma ||D_\theta(\mathbf{x}_0+\mathbf{n};\boldsymbol{\sigma},\mathbf{m},\mathbf{c})-\mathbf{x}_0||_2^2]$$
   该损失仅反向传播至嵌入参数 $\mathbf{m}$，模型权重 $\theta$ 保持不变（Section 3.3, Eq. 3）。

通过冻结模型权重，方法从根本上避免了外观泄漏——模型权重无法存储参考视频的外观信息，从而保证运动迁移时外观完全由目标图像决定（Section 3.2.1）。

### 交叉注意力膨胀机制

标准 SVD 在交叉注意力中使用单个 token 广播至所有帧，限制了时序运动粒度。为此，方法引入**交叉注意力膨胀**（Cross-Attention Inflation, Section 3.4, Fig. 5）：

- **空间交叉注意力**：使用每帧不同的 token 集合（$F \times N$ 个 tokens），使不同帧可以关注不同的嵌入信息，获得更高的时序运动粒度。
- **时间交叉注意力**：使用所有帧共享的 $N$ 个 tokens，保持时序一致性。

膨胀后的交叉注意力计算为 $\mathrm{Attention}(Q,K,V)=\mathrm{softmax}(\frac{QK^T}{\sqrt{d_a}})V$，其中 $Q$ 来自视频特征，$K,V$ 来自运动文本嵌入。膨胀使得前景/背景等不同空间位置可以动态关注不同 tokens，从而更精细地编码运动语义（Fig. 5b）。

### 目标图像推理阶段

学习完成后，将优化好的运动文本嵌入 $\mathbf{m}^*$ 与任意目标图像一起送入膨胀后的 SVD 模型进行推理。目标图像同时作为图像潜在输入（与噪声视频拼接）和图像嵌入条件（与 $\mathbf{m}^*$ 共同注入交叉注意力），生成与参考视频运动语义匹配的新视频（Fig. 4 推理模块）。

### 消融验证

消融实验证实了交叉注意力膨胀的关键作用（Fig. 7, Table 4）：
- 仅增加 token 数 $N$ 已有一定改善，但最大的性能提升来自**每帧使用不同 tokens**（$F'=F+1=15$）。
- 在 $F'=15$ 的设置下，token 维度 $N$ 的具体取值对结果影响不大，表明帧级独立 token 是核心因果因素。

### 3.1 扩散模型基础

方法建立在连续时间扩散框架之上。给定数据分布 $p_{\mathrm{data}}(\mathbf{x}_0, \mathbf{c})$，其中 $\mathbf{x}_0$ 为干净视频，$\mathbf{c}$ 为条件信号，去噪器 $D_\theta$ 的训练目标为去噪得分匹配损失：

$$\mathbb{E}_{(\mathbf{x}_0,\mathbf{c})\sim p_{\mathrm{data}}(\mathbf{x}_0,\mathbf{c}),(\sigma,\mathbf{n})\sim p(\sigma,\mathbf{n})}[\lambda_\sigma ||D_\theta(\mathbf{x}_0+\mathbf{n};\sigma,\mathbf{c})-\mathbf{x}_0||_2^2]$$

其中 $\sigma$ 为噪声水平，$\mathbf{n}$ 为高斯噪声，$\lambda_\sigma$ 为噪声水平相关的权重系数。去噪器的参数化形式为：

$$D_\theta(\mathbf{x};\sigma)=c_{\mathrm{skip}}(\sigma)\mathbf{x}+c_{\mathrm{out}}(\sigma)F_\theta(c_{\mathrm{in}}(\sigma)\mathbf{x};c_{\mathrm{noise}}(\sigma))$$

这里 $F_\theta$ 为实际神经网络（UNet），$c_{\mathrm{skip}}$、$c_{\mathrm{out}}$、$c_{\mathrm{in}}$、$c_{\mathrm{noise}}$ 为与 $\sigma$ 相关的缩放系数，用于改善训练动态。实际扩散过程在潜空间中进行，此处为清晰起见省略了编解码器细节。

### 3.2 运动文本反演（Motion-Textual Inversion）

核心创新在于将运动表示为可学习的文本/图像嵌入 tokens，而非修改模型权重。给定一个运动参考视频 $\mathbf{x}_0$，方法冻结预训练的图像到视频扩散模型 $D_\theta$，仅优化一组嵌入向量 $\mathbf{m}$，称为运动文本嵌入（motion-text embedding）：

$$\mathbf{m}^*=\underset{\mathbf{m}}{\arg\min}\ \mathbb{E}_{(\mathbf{x}_0,\mathbf{c})\sim p_{\mathrm{data}}(\mathbf{x}_0,\mathbf{c}),(\boldsymbol{\sigma},\mathbf{n})\sim p(\boldsymbol{\sigma},\mathbf{n})}[\lambda_\sigma ||D_\theta(\mathbf{x}_0+\mathbf{n};\boldsymbol{\sigma},\mathbf{m},\mathbf{c})-\mathbf{x}_0||_2^2]$$

该公式与标准扩散损失形式一致，但梯度仅回传至 $\mathbf{m}$，模型参数 $\theta$ 保持不变。这一设计的关键因果机制在于：在 SVD 等图像到视频模型中，外观信息主要通过图像潜变量输入（与噪声视频拼接）传递，而运动信息则主要通过交叉注意力层注入的嵌入 tokens 控制（Fig. 2, Fig. 3 提供了这一解耦的实证观察）。冻结模型权重从根本上避免了外观泄漏——模型无法将参考视频的外观信息编码进自身参数中。

### 3.3 交叉注意力膨胀（Cross-Attention Inflation）

SVD 基线仅使用单个 CLIP 图像嵌入 token 作为交叉注意力的 key 和 value，该 token 被广播至所有时空位置。这种设计严重限制了运动表达的时序粒度。本方法将其扩展为多 token 机制，交叉注意力操作定义为：

$$\mathrm{Attention}(Q,K,V)=MV=\mathrm{softmax}\left(\frac{QK^T}{\sqrt{d_a}}\right)V$$

其中 $Q$ 为来自视频特征的 queries，$K$ 和 $V$ 为来自嵌入 tokens 的 keys 和 values，$d_a$ 为注意力维度，$M$ 为注意力图。

膨胀策略包含两个维度（Fig. 5, Fig. 10）：

1. **Token 维度膨胀**：将单 token 扩展为 $N$ 个 token（默认 $N=5$），使不同空间位置（如前景与背景）可动态关注不同 token。
2. **时序膨胀**：空间交叉注意力使用每帧不同的 token 集合（共 $F \times N$ 个 token，$F=14$ 帧），而非将所有帧广播相同 token。时间交叉注意力则使用跨帧共享的 $N$ 个 token。

最终运动文本嵌入的总 token 数为 $(F+1) \times N = 75$（额外 $+1$ 来自 CLIP 图像嵌入的全局 token）。消融实验（Fig. 7, Table 4）表明，每帧独立 token 是运动迁移质量提升的最关键因素——仅增加 $N$ 已有改善，但跨帧区分带来的增益远大于此。

## 实验与关键发现

### 核心实验设置

本方法基于 **Stable Video Diffusion (SVD)**（Blattmann et al., 2023a）的 14 帧版本构建，使用 Adam 优化器和 SVD 的默认引导尺度。运动文本嵌入默认配置为 $N=5$ 个 token 每帧，共 $F=14$ 帧，总计 $(F+1) \times N = 75$ 个可学习 token。定量评估在 Something-Something V2 数据集的 10 个类别子集上进行，每个类别选取一个参考视频，共 100 个测试视频。用户研究规模为 27 人。

### 主实验结果

**Table 1** 汇总了与基线方法的定量对比。评估维度分为两类：图像外观保持（CLIP-Avg、CLIP-1st、用户排名）和视频运动保真度（Acc-Top-1、Acc-Top-5、Cos-Sim、用户排名）。

![[assets/figures/papers/paper_list_l26_Reenact_Anything_Semantic_Video_Motion_Transfer_Using_Motion_Textual_Inv/figures/006_Table_1.jpg]]
*Table 1: antitative evaluation. We compare our method to Stable Video Difusion [Bla mann et al. 2023a] (baseline, no motion input), VideoComposer [Wang et al. 2024d], MotionClone [Ling et al. 2024], and MotionDirector [Zhao et al. 2024]. The best performing method per column is marked in bold*

在运动保真度上，本方法在所有指标上均取得最优：
- Acc-Top-1 达到 **54%**，远超 SVD 基线的 3%（+51%），也显著优于次优方法 MotionClone 的 44%。
- Cos-Sim 达到 **0.696**，SVD 基线仅为 0.370（+0.326）。
- 用户运动保真度排名为 **1.367**（越低越好），SVD 基线为 2.822。

在外观保持上，本方法同样表现最佳：
- CLIP-Avg 为 0.779，CLIP-1st 为 0.884，用户外观排名为 1.811。

用户研究中，本方法在 75% 的情况下被投票为运动保真度最佳，78% 的情况下被投票为整体任务完成度最佳。

**Table 3** 按运动类别（相机运动/对象运动）进一步细分。本方法在相机运动上表现尤为突出，但在对象运动上的 Acc-Top-1 仅为 36%，表明复杂对象运动仍是一个挑战。

![[assets/figures/papers/paper_list_l26_Reenact_Anything_Semantic_Video_Motion_Transfer_Using_Motion_Textual_Inv/figures/017_Table_3.jpg]]
*Table 3: antitative evaluation aggregated by motion category (camera/object). As in Table 1, we compare our method to Stable Video Difusion [Bla mann et al. 2023a] (baseline, no motion input), VideoComposer [Wang et al. 2024d], MotionClone [Ling et al. 2024], and MotionDirector [Zhao et al. 2024]. The first value in each cell corresponds to camera motions and the second to object motions. The best performing method per column is marked in bold*

定性对比（**Fig. 6**、**Fig. 13**、**Fig. 14**）展示了全身重演、面部重演和相机运动三类场景。SVD 基线因缺乏运动输入，生成的视频运动与参考视频几乎无关；VideoComposer 依赖密集运动矢量，在跨域场景中容易失败；MotionClone 和 MotionDirector 在部分案例中能产生相似运动，但外观泄漏问题明显（如参考视频的结构特征出现在生成结果中）。本方法在保持目标图像外观的同时，更准确地复现了参考运动的语义。

### 消融实验

消融实验（**Fig. 7**、**Fig. 15**、**Table 4**）系统验证了运动文本嵌入膨胀（cross-attention inflation）的关键作用。

![[assets/figures/papers/paper_list_l26_Reenact_Anything_Semantic_Video_Motion_Transfer_Using_Motion_Textual_Inv/figures/019_Table_4.jpg]]
*Table 4: antitative results for our ablation. Here, we compare various se ings for the dimensions of the motion-text embedding. Table (a) shows the overall scores aggregated over all motion categories, whereas (b) shows the scores aggregated by the motion category of the motion reference videos, where the first value in each cell corresponds to camera motions and the second to object motions. The best performing method per column is marked in bold. (a) Overall*

核心发现：**每帧使用不同 token（$F'=F+1=15$）是性能提升的最大动因**。仅增加 token 维度 $N$（从 1 到 5）已有一定改善，但将相同 token 广播到所有帧时，模型无法捕捉时序细粒度运动。当同时启用每帧不同 token 和 $N=5$ 时，运动迁移质量显著跃升。

**Table 4** 的定量消融确认了这一结论：在 $F'=15$ 条件下，$N$ 从 1 增加到 5 对整体指标影响不大，说明每帧独立 token 才是决定性因素。这一结果与因果机制一致——空间交叉注意力使用每帧不同的 token 集合（$F \times N$ tokens），使模型能够在不同时间步关注不同的运动语义，而时间交叉注意力使用共享的 $N$ tokens 保持时序一致性。

### 失败模式分析

**Fig. 8** 系统展示了三类典型失败案例：

1. **预训练模型先验限制**：当目标图像与参考视频的对象类型差异过大时，SVD 的先验可能导致身份变化（如头部转动时面部特征改变）。该方法无法迁移模型未见过的复杂运动（如后空翻）。

2. **结构泄漏**：尽管冻结模型权重，部分案例中仍出现参考视频的结构特征泄漏（如袋鼠腿上出现类人腿部特征）。这表明单纯冻结权重不足以完全消除外观信息的隐式传递。

3. **空间精细运动丢失**：对于手指打字等空间精细运动，迁移效果不佳，目标对象（如恐龙）未能展现对应的精细动作。**Table 5** 按运动类型汇总了性能表现，进一步印证了空间精细运动是当前方法的薄弱环节。

![[assets/figures/papers/paper_list_l26_Reenact_Anything_Semantic_Video_Motion_Transfer_Using_Motion_Textual_Inv/figures/024_Table_5.jpg]]
*Table 5: Summary of motion types by performance*

此外，**Fig. 20** 揭示了失败重建导致迁移失败的连锁问题：当优化后的运动文本嵌入无法准确重建参考运动时，后续对新目标图像的迁移也必然失败。这表明嵌入优化的收敛质量是运动迁移成功的前提条件。

### 运动风格与语义特性

**Fig. 16** 展示了运动风格迁移能力：学到的运动文本嵌入不仅存储粗略的运动类别，还保留了运动风格（如马的平稳小跑 vs. 颠簸慢跑）。即使在极端跨域场景（船、汽车、麦片盒），运动风格的本质仍得以保持。

**Fig. 17** 验证了方法的语义运动特性：将同一运动文本嵌入应用于水平翻转的输入图像时，生成结果保持语义一致（动物朝其面向方向移动并低头），而非简单复制空间轨迹。这证实了嵌入捕获的是语义运动而非像素级空间位移。

### 评估公平性说明

定量评估存在以下局限：仅覆盖 10 个运动类别，每个类别一个参考视频，可能无法代表所有运动类型；定性结果采取多抽样选优策略，论文报告约 1/10 的运动能对超过一半的目标图像产生良好迁移，成功率因人而异；用户研究规模有限（27 人），可能引入主观偏差；论文使用了未公开的内部数据集进行定性展示。

### 补充图表

![[assets/figures/papers/paper_list_l26_Reenact_Anything_Semantic_Video_Motion_Transfer_Using_Motion_Textual_Inv/figures/005_Figure_5.jpg]]
*Figure 5: (b) Inflated SVD (Ours): By introducing more tokens in the token dimension (𝑁 ), every spatial and temporal location can dynamically a end to diferent tokens, e.g., diferent tokens for the foreground vs. background. For the spatial cross-a ention, we use diferent tokens per frame, resulting in diferent keys and values per frame. This enables a higher temporal granularity of the motion. Fig. 5. High-level visualization of our motion-text embedding and cross-a ention inflation. The SVD [Bla mann et al. 2023a] UNet is composed of several levels of blocks, shown in gray, that have similar structure. We visualize the sub-blocks of level 𝑖 and their cross-a ention maps in more detail. Our inflate...*

## 定位与知识库关联

### 核心问题与现有方法的瓶颈

视频运动迁移的核心挑战在于，如何将一段参考视频中的运动语义提取出来，并注入到全新的目标图像中，生成外观来自目标图像、运动来自参考视频的新视频。现有方法在解决这一问题时面临两个根本性瓶颈：

**运动信号的表达能力不足。** 主流的运动控制手段依赖稀疏信号——文本描述（如"向前走"）只能表达粗粒度的运动类别，轨迹（trajectories）和边界框（bounding boxes）则局限于物体位移的二维投影，难以捕捉肢体协调、面部微表情、相机运镜等复杂运动语义。这使得基于这些信号的方法在需要精确运动复现的场景中表现乏力。

**空间对齐假设导致外观泄漏。** 基于空间特征的运动迁移方法（如通过光流或注意力图进行特征扭曲）隐含地要求参考视频与目标图像在空间结构上对齐。当物体形状、姿态或类别差异较大时，这种对齐会崩溃；更严重的是，这类方法容易将参考视频的结构信息（如人体轮廓、物体边缘）泄漏到生成结果中，产生"鬼影"或身份混淆。

### 本方法的定位与核心洞察

**Reenact Anything** 提出了 **motion-textual inversion（运动文本反演）**，将运动迁移问题重新定义为嵌入空间的优化问题。其核心洞察来自对图像到视频（I2V）扩散模型中外观与运动解耦的观察：

- **外观由图像输入主导。** 在 I2V 模型中，目标图像通过潜在空间拼接（latent concatenation）注入去噪 UNet，直接约束生成视频的视觉内容。实验表明，即使文本提示指定"粉色马"，模型仍会从白色马的输入图像生成白色马（Fig. 2），证明图像输入对外观的控制力远强于文本。
- **运动由交叉注意力中的嵌入控制。** 交换不同视频的 CLIP 图像嵌入（如真马与玩具马），会导致生成视频的运动发生互换（Fig. 3），说明交叉注意力层中注入的文本/图像嵌入 tokens 是运动的主要控制旋钮。

基于这一解耦，该方法提出：**冻结预训练 I2V 模型的所有权重，仅优化一组可学习的文本嵌入 tokens（称为 motion-text embedding），使其在扩散损失下重建参考视频的运动，然后将优化后的嵌入与任意目标图像组合，生成运动匹配的新视频。** 这一策略从根本上避免了外观泄漏——因为模型权重不变，参考视频的外观信息无法被编码进模型参数。

### 与相关工作的关系

**与 Textual Inversion 的关系。** 该方法在概念上继承了个性化图像生成中的 textual inversion（Gal et al., 2023）思想——通过优化嵌入 tokens 来捕获新概念。但关键区别在于：textual inversion 优化的是"外观概念"，而本方法优化的是"运动概念"；此外，本方法引入了帧级嵌入膨胀（cross-attention inflation），使嵌入具备时序粒度，这是标准 textual inversion 所不具备的。

**与基于扩散模型的运动迁移方法的对比：**

- **Stable Video Diffusion (SVD)**（Blattmann et al., 2023a）：作为本方法的基座模型，SVD 本身无运动输入机制，仅从单张图像生成视频，运动由随机种子和模型先验决定。本方法可视为在 SVD 上添加了一个可学习的运动控制接口，而不修改模型本身。
- **VideoComposer**（Wang et al., 2024d）：使用密集运动矢量（motion vectors）作为运动条件，属于显式空间信号。其优势在于运动控制精确，但需要参考视频的运动矢量作为输入，且对跨域物体（如人与动物）的对齐敏感。本方法隐式编码语义运动，无需空间对齐，在跨域场景中更具鲁棒性，但在空间精细运动（如手指动作）上不如显式方法。
- **MotionClone**（Ling et al., 2024）：通过提取并复用稀疏时序注意力权重来表示运动，属于隐式运动表示。与本方法类似，它也不依赖空间对齐。但 MotionClone 的注意力权重提取依赖于对参考视频的 DDIM 反演，过程复杂且可能累积误差；本方法直接优化嵌入，流程更简洁。
- **MotionDirector**（Zhao et al., 2024）：面向文本到视频（T2V）模型，通过 LoRA 微调模型权重来捕获运动。与本方法的核心区别在于：MotionDirector 修改模型权重，存在外观泄漏风险；且面向 T2V，需要文本提示来指定外观，而本方法面向 I2V，外观由目标图像直接提供，控制更直观。

### 方法适用边界与局限

**受限于预训练模型的先验。** 本方法完全依赖冻结的 SVD 模型的生成能力。对于模型训练数据中未见过或罕见的运动（如后空翻、复杂舞蹈），优化后的嵌入无法引导模型生成合理结果。此外，SVD 自身的质量缺陷（如身份一致性保持不佳、物体变形）会直接传递到迁移结果中。

**结构泄漏仍可能发生。** 尽管冻结模型权重大幅降低了外观泄漏，但在某些情况下，优化后的嵌入仍会携带参考视频的结构信息。例如，将人的走路运动迁移到袋鼠时，袋鼠的后腿可能呈现人腿的形态特征（Fig. 8）。这是因为嵌入优化过程中，模型可能将部分结构信息编码为运动的"载体"。

**空间精细运动迁移困难。** 对于需要精确空间定位的运动（如手指打字、精细操作），该方法表现不佳。这是因为嵌入 tokens 通过交叉注意力作用于全局特征，缺乏像素级的空间约束能力。消融实验表明，即使增加 tokens 数量，对此类运动的改善也有限（Table 4 中对象运动的 Acc-Top-1 仅 36%）。

**计算开销大。** 每个参考运动需要约 1 小时的优化时间（A100 80GB GPU），无法实时应用。这是逐例优化（per-instance optimization）方法的固有局限。

**损失函数的语义盲区。** 使用简单的 MSE 损失优化嵌入，可能导致模型倾向于将像素放在"大致正确"的位置，而非生成语义正确的运动。例如，对于"推"的动作，模型可能生成物体移动的结果，但运动方式并非真正的"推"。

### 开放问题与未来方向

1. **语义感知的损失函数。** 能否引入动作识别模型（如 VideoMAE、TimeSformer）的特征距离作为感知损失，替代或补充 MSE 损失，使优化目标与运动语义更对齐？

2. **消除逐例优化。** 能否训练一个预测网络（如基于参考视频的编码器），直接输出运动文本嵌入，将优化过程替换为单次前向推理？这需要构建大规模的运动-嵌入配对数据集。

3. **架构泛化性。** 当前方法基于 SVD 的 UNet 架构和交叉注意力机制。对于基于 Diffusion Transformer（DiT）的新一代视频生成模型，嵌入 tokens 的注入方式和膨胀策略需要重新设计。

4. **长视频支持。** SVD 仅支持 14 帧生成，运动嵌入的帧级 token 数量与帧数线性相关。扩展到更长视频需要解决嵌入规模增长和时序一致性问题。

5. **嵌入空间的正则化。** 优化后的嵌入可能偏离原始 CLIP 嵌入空间分布，导致与目标图像的嵌入不兼容。通过正则化约束嵌入保持在 CLIP 流形内，可能改善迁移质量和泛化性。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/Reenact_Anything_Semantic_Video_Motion_Transfer_Using_Motion_Textual_Inversion.pdf]]
