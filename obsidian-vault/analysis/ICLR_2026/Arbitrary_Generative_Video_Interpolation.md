---
title: "Arbitrary Generative Video Interpolation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Arbitrary_Generative_Video_Interpolation.pdf
openreview_forum_id: eKGkb4cFRe
aliases:
- AGVI
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过连续时间戳感知的旋转位置嵌入（Timestamp-aware RoPE, TaRoPE）调制时间维度位置信息，使模型能生成任意时刻的中间帧；配合外观-运动解耦条件策略，提升长时序段间的时空一致性。"
primary_logic: "将视频帧插值任务转化为归一化时间戳[0,1]上的连续帧生成问题，利用时间RoPE的位置依赖性赋予模型对任意时刻的感知能力；同时将长序列分解为段，通过外观一致性引导和运动令牌注入，维持段间平滑过渡。"
claims:
- "ArbInterp 在多尺度插值（2× 至 32×）的 FVD、LPIPS 及 VBench 一致性指标上全面超越现有方法。"
- "TaRoPE 对时间戳的精确控制显著优于无时间戳注入或仅用 MLP AdaLN 的方法。"
- "外观-运动解耦条件策略在提升时空一致性的同时，降低了约 40% 的计算开销。"
- "分段训练和三阶段训练策略使模型在有限资源下达到最优性能。"
---

# Arbitrary Generative Video Interpolation

> [!tip] 核心洞察
> 将视频帧插值任务转化为归一化时间戳[0,1]上的连续帧生成问题，利用时间RoPE的位置依赖性赋予模型对任意时刻的感知能力；同时将长序列分解为段，通过外观一致性引导和运动令牌注入，维持段间平滑过渡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 任意生成式视频插值 |
| 英文题名 | Arbitrary Generative Video Interpolation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=eKGkb4cFRe); [Project](https://mcg-nju.github.io/ArbInterp-Web/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ArbInterp |
| Dataset | MultiInterpBench (2× interpolation), MultiInterpBench (8× interpolation), MultiInterpBench (16× interpolation), MultiInterpBench (32× interpolation) |

> [!tip] 效果简介
> - MultiInterpBench (2× interpolation) 上，FVD ↓ 为 44.9，对比 57.2 (DynamiCrafter, best prior)，变化 -12.3。
> - MultiInterpBench (8× interpolation) 上，FVD ↓ 为 33.0，对比 56.3 (DynamiCrafter)，变化 -23.3。
> - MultiInterpBench (16× interpolation) 上，FVD ↓ 为 28.4，对比 49.7 (DynamiCrafter)，变化 -21.3。

## 概述

现有生成式视频帧插值（VFI）方法受限于固定帧率生成范式，只能输出预设数量的中间帧，无法灵活调整帧率或时长，且缺乏对连续运动场细粒度建模的能力。针对这一瓶颈，本文提出 **ArbInterp**，一个支持任意时间戳与任意长度插值的生成式 VFI 框架。

ArbInterp 的核心思路是将视频帧插值转化为归一化时间戳 $[0,1]$ 上的连续帧生成问题。为此，作者设计了 **时间戳感知的旋转位置嵌入（Timestamp-aware RoPE, TaRoPE）**，以连续时间戳替代传统帧索引作为时间位置信息，赋予模型对任意时刻的感知能力。对于长序列插值，ArbInterp 将其分解为逐段生成，并通过 **外观-运动解耦条件策略** 维持段间时空一致性：前一段的末尾帧提供外观约束，运动语义提取器（Motion Semantic Extractor, MSE）从前序帧中提取运动令牌注入生成过程，实现外观一致与运动连贯的并行控制。

实验表明，ArbInterp 在多尺度插值（2× 至 32×）上全面超越现有方法：在 MultiInterpBench 基准上，2× 插值的 FVD 降至 44.9（此前最佳 DynamiCrafter 为 57.2），8× 插值 FVD 降至 33.0（此前最佳 56.3），16× 和 32× 插值同样保持领先。在 256× 极端插值场景下，FVD 进一步降至 242.3，显著优于对比方法。消融实验证实 TaRoPE 对时间戳的精确控制能力（运动平滑度 0.9817 vs 无时间戳注入的 0.9637），以及外观-运动解耦策略在提升一致性的同时降低约 40% 计算开销的优势。三阶段训练策略（基础插值→连续性学习→联合微调）使模型在有限资源下达到最优性能。

## 背景与动机

### 视频帧插值的核心挑战

视频帧插值（Video Frame Interpolation, VFI）旨在从给定的起始帧和结束帧之间生成中间帧，是视频处理中的基础任务。传统方法通常采用光流估计与运动补偿的策略，通过显式建模像素级运动场来合成中间帧。然而，这类方法在面对大运动、遮挡和非线性形变时，往往会产生模糊、伪影或结构扭曲。

近年来，生成式模型——特别是基于扩散的框架——为VFI带来了新的可能性。生成式VFI通过数据驱动的方式隐式学习运动分布，能够在复杂场景下生成更逼真的细节。然而，现有生成式方法存在一个根本性的瓶颈：**它们被设计为只能生成固定数量的中间帧**。例如，LDMVFI和DynamiCrafter等方法在训练时预设了固定的插值倍数（如2×或8×），推理时无法灵活调整帧率或时长。这意味着用户无法指定“在0.3秒处插入一帧”或“将视频放慢至32倍”，而必须在训练和推理之间保持严格一致的时间结构。

这一限制的深层原因在于，现有方法缺乏对**连续运动场细粒度建模**的能力。它们将时间维度视为离散的帧索引序列，而非一个可任意采样的连续变量。当需要长时序插值时（如32×或256×），直接扩展模型会面临自注意力复杂度 $O(N^2)$ 的爆炸性增长，导致计算资源不可承受。

### 现有方法的缺口

具体而言，现有生成式VFI方法存在以下三个关键缺口：

1. **固定插值范式**：如图1所示，传统方法要求训练和推理的插值倍数严格匹配。一旦训练了8×模型，就无法生成16×的插值结果。这种刚性限制使得模型无法适应实际应用中灵活多变的帧率需求。

2. **时间位置感知缺失**：大多数方法将中间帧视为等间距的序列，不区分第k帧和第k+1帧在时间轴上的精确位置。当需要生成非均匀时间戳的帧（如仅生成0.3和0.7时刻的帧）时，模型缺乏对连续时间坐标的感知能力。

3. **长序列段间一致性不足**：在处理超长插值（如256×）时，现有方法通常采用分段生成策略，但段与段之间缺乏有效的条件注入机制。直接拼接相邻段往往导致运动不连贯、外观跳变或闪烁伪影。

### ArbInterp的动机与核心思路

针对上述缺口，ArbInterp提出了一种**将视频帧插值重新定义为连续时间戳生成问题**的范式。其核心洞察是：如果将归一化时间戳 $t \in [0,1]$ 作为连续变量，模型就可以在任意时刻生成中间帧，从而彻底打破固定插值倍数的限制。

为实现这一目标，ArbInterp引入了两个关键机制：

- **时间戳感知旋转位置嵌入（Timestamp-aware RoPE, TaRoPE）**：通过在时间维度的旋转位置编码中注入归一化连续时间戳 $t_k = (k-1)/(N-1)$，使DiT自注意力层能够感知每一帧在连续时间轴上的精确位置。这使得模型可以生成任意时刻的中间帧，而不仅仅是等间距的固定序列。

- **外观-运动解耦条件策略**：针对长序列生成，ArbInterp将视频分解为多个段，并通过两个并行的条件通路维持段间一致性——前一段的末尾帧作为外观条件直接输入编码器，确保视觉连贯性；同时利用运动语义提取器（MSE）从前序帧中提取运动令牌，注入DiT交叉注意力层，维持运动连续性。这一解耦设计不仅提升了时空一致性，还降低了约40%的计算开销。

通过这些设计，ArbInterp将VFI从“固定倍数生成”转变为“任意时刻、任意长度的连续帧生成”，为灵活可控的视频插值开辟了新的技术路径。

## 核心创新

ArbInterp 的核心创新在于将视频帧插值从固定帧数生成重新定义为**连续时间戳上的任意帧生成问题**，并围绕这一范式转换设计了两个关键 changed slots：时间戳感知的旋转位置嵌入（TaRoPE）与外观-运动解耦条件策略。

### 问题瓶颈与因果抓手

现有生成式视频帧插值方法（LDMVFI、TRF、GI、DynamiCrafter 等）只能生成固定数量的中间帧，无法灵活调整帧率或时长。其根源在于这些方法将时间位置编码为离散的帧索引，模型在训练时绑定于特定帧长，缺乏对连续运动场细粒度建模的能力。

ArbInterp 的因果抓手（causal knob）是 **TaRoPE**：将归一化连续时间戳 $t_k \in [0,1]$ 作为时间维度的位置信息注入 DiT 的自注意力机制，使模型能感知并生成任意时刻的中间帧。配合**外观-运动解耦条件策略**，将长序列分解为段，通过外观一致性引导和运动令牌注入维持段间平滑过渡，从而在任意插值长度下保持时空一致性。

### Changed Slot 1：时间位置编码 —— 从离散帧索引到连续时间戳

**Baseline 做法**：普通时间 RoPE 以帧索引（绝对位置）作为位置信息，公式为 $\tilde{\mathbf{z}}_k = \mathrm{RoPE}(\mathbf{z}_k, k) = \mathbf{z}_k e^{i\theta_k}$，其中 $\theta_k = k\theta_{\mathrm{base}}$。模型在固定帧长下训练，无法泛化到不同帧数的插值场景。

**ArbInterp 做法**：TaRoPE 将第 $k$ 帧的时间戳归一化为连续值 $t_k = \frac{k-1}{N-1}$，约束 $1 \leq k \leq N$，使任意长度视频的帧位置均映射到 $[0,1]$ 区间。这一设计使 DiT 自注意力中的位置依赖关系从"第几个潜在帧"转变为"处于首尾帧之间的相对时刻"，赋予模型对任意时间戳的精确感知能力。

**证据强度**：消融实验（Table 2）显示，TaRoPE 在运动平滑度上显著优于无时间戳注入的 Vanilla baseline（Motion Smooth. 0.9817 vs 0.9637），且 Figure 11 的定性对比表明 TaRoPE 能精确生成与指定时间戳对应的帧，而其他注入方式（如 MLP AdaLN）则出现时间错位。

### Changed Slot 2：长序列段间条件注入 —— 从简单拼接/交叉注意力到外观-运动解耦

**Baseline 做法**：直接分段生成不考虑段间一致性，或使用简单的潜在拼接（Latent Conditioning）将前一段末尾帧的潜在变量拼接到当前段输入，或通过交叉注意力（Cross-Attention Conditioning）注入前一段信息。这些方法将外观和运动信息混合传递，计算开销大且难以精细控制时空一致性。

**ArbInterp 做法**：提出外观-运动解耦条件策略（Figure 4(c)），将段间条件分为两条独立路径：
- **外观条件**：前一段的末尾帧作为前缀帧直接输入编码器，通过潜在空间的特征共享强制外观一致性；
- **运动条件**：通过运动语义提取器（Motion Semantic Extractor, MSE）从前 $N$ 帧提取运动令牌，注入各 DiT 块的交叉注意力层，实现运动连贯性控制。

MSE 的结构（Figure 9）为：先用时序增强的 CLIP 提取时空特征，再通过 Q-Former 将特征压缩为固定数量的运动令牌。这一设计将运动信息从外观中解耦，使两条路径可并行优化。

**证据强度**：Table 2 显示，该策略在主体一致性（Subject Consist. 0.9441）和背景一致性（Background Consist. 0.9628）上均优于潜在拼接和交叉注意力方案，同时推理步时间从 4.4s 降至 2.6s，**计算效率提升约 40%**。消融实验进一步表明，移除运动信息（w/o Motion）导致时间闪烁指标恶化（Temporal Flick. 0.9549 vs 0.9624），移除外观信息（w/o Appearance）导致主体一致性下降（0.9297 vs 0.9441），验证了两条路径的独立贡献。

### 辅助创新：分段与分层插值策略

为应对长序列插值中自注意力 $O(N^2)$ 的复杂度瓶颈，ArbInterp 引入了分段插值（Segment-by-Segment）和分层插值（Hierarchical）策略（Figure 3）。分段策略将长序列切分为多个短段依次生成，分层策略则先预测中间关键帧再分段生成，将复杂度降至 $O(N^2/M)$。这些策略与 TaRoPE 和外观-运动解耦条件协同工作，使模型在有限计算资源下支持 32× 乃至 256× 的极高速插值。三阶段训练策略（Table 4）进一步验证了分阶段学习（先学基本插值，再学连续性，最后联合微调）的必要性：完整三阶段训练的 FVD₃₂ₓ 为 319.9，而仅用第三阶段直接训练则为 401.6。

### 创新边界与局限

需要指出，当前 ArbInterp 仅以首尾帧作为条件输入，未使用文本或其他语义条件，限制了生成的可控性。此外，模型基于 Wan2.1 1.3B 参数规模，训练数据为 5 万视频片段，在极端复杂场景下的质量上限可能受约束。段间的绝对一致性仍受生成随机性影响，尚未达到理论最优。这些局限为后续将文本引导整合进连续时间戳框架、以及在更大规模数据上验证提供了明确方向。

## 整体框架

![[assets/figures/papers/iclr26_0010_eKGkb4cFRe_Arbitrary_Generative_Video_Interpolation/figures/002_Figure_2.jpg]]
*Figure 2: Overall architecture of ArbInterp. Our framework enables arbitrary-length interpolation with continuous timestamps using Timestep-aware Rotary Position Embedding (TaROPE). Additionally, we introduce an appearance-motion decoupling conditioning strategy to enhance the performance of long-term interpolation. This strategy ensures appearance consistency via prefix frame guidance and enforces motion continuity through motion tokens*

ArbInterp 的整体 pipeline 围绕一个核心范式展开：**将视频帧插值重新定义为归一化时间戳上的连续帧生成问题**。给定起始帧 $\mathbf{x}_0$、结束帧 $\mathbf{x}_1$ 以及任意时间戳列表 $\mathbf{T} = [0, t_1, \dots, t_n, 1]$（其中 $t_i \in (0,1)$ 可任意指定），模型直接生成对应的中间帧序列：

$$[\mathbf{x}_{t_1}, \dots, \mathbf{x}_{t_n}] = \mathrm{ArbInterp}(\mathbf{x}_0, \mathbf{x}_1, \mathbf{T})$$

这一范式打破了传统 VFI 方法只能生成固定数量、固定位置中间帧的限制，使帧率和插值长度完全可控。

### 模块关系与数据流

整体架构（Figure 2）由以下关键模块串联而成，数据流自上而下贯通：

1. **条件注入（Token Replace）**：首尾帧经 VAE 编码为潜在表示后，直接替换噪声序列中对应位置的纯噪声令牌。这一操作为扩散模型的去噪过程提供了硬性边界条件，确保生成结果在端点处与输入严格一致。

2. **时间戳感知旋转位置嵌入（TaRoPE）**：每个潜在帧被赋予其在 $[0,1]$ 区间内的连续时间戳 $t_k = (k-1)/(N-1)$ 作为时间位置信息，替代传统 RoPE 中以帧索引为单位的离散位置编码。TaRoPE 调制 DiT 自注意力层中的时间维度位置编码，使模型能够感知任意时刻帧的相对位置，从而生成与该时间戳精确对应的中间帧。

3. **DiT 去噪骨干**：采用流匹配（Flow Matching）训练范式，损失函数为预测速度向量与真实速度向量的 L2 损失：

   $$\mathcal{L} = \| \mathbf{v}_n - u_{\theta}(\mathbf{z}^n, n, \mathbf{y}) \|^2, \quad \mathbf{v}_n = \epsilon^n - \mathbf{z}$$

   其中 $\mathbf{z}^n$ 为第 $n$ 个噪声步的潜在状态，$\mathbf{y}$ 为条件信息。去噪过程从纯高斯噪声出发，经 UniPC 调度器以 50 步、timestep shift 5.0 的设置逐步恢复干净潜在。

4. **外观-运动解耦条件注入（长序列场景）**：当插值帧数超过单段容量（>21 帧）时，长序列被分解为多个段进行分段生成。段间一致性通过两条并行通路维持：
   - **外观通路**：将前一段的末尾帧作为“前缀帧”直接输入 VAE 编码器，与当前段的首帧在潜在空间中拼接，强制外观一致性。
   - **运动通路**：运动语义提取器（MSE）从前序 $N$ 帧中提取时空特征，经时间增强的 CLIP 和 Q-Former 压缩为固定数量的运动令牌，注入 DiT 各块的交叉注意力层，引导当前段继承前序运动模式。

   这种解耦设计相比直接潜在拼接或交叉注意力注入，在提升时空一致性的同时降低了约 40% 的计算开销。

### 插值策略分级

针对不同插值比例，ArbInterp 采用三级策略（Figure 3），将自注意力复杂度从 $O(N^2)$ 降至 $O(N^2/M)$（$M$ 为段数）：

- **直接插值**：短距离插值（≤21 帧）时，一次性生成所有中间帧。
- **分段插值**：中等长度插值时，将序列切分为多个段依次生成，段间通过外观-运动解耦条件衔接。
- **分层插值**：超长序列（如 32× 插值）时，先预测 $t=0.5$ 处的中位帧，再以该帧为界将序列分为两段分别生成，递归降低单次生成负担。

### 训练策略

模型采用三阶段渐进训练：第一阶段学习基本插值能力（固定帧数），第二阶段引入连续时间戳和分段训练以泛化至任意长度，第三阶段联合微调外观-运动解耦条件模块。消融实验（Table 4）表明，完整三阶段训练的 FVD₃₂ₓ 为 319.9，显著优于仅进行第三阶段训练的 401.6，验证了渐进式训练对复杂长序列插值的必要性。

## 核心模块与公式推导

### 3.1 问题形式化与生成范式

ArbInterp 将视频帧插值重新定义为连续时间戳上的生成问题。给定首帧 $\mathbf{x}_0$、末帧 $\mathbf{x}_1$ 以及归一化时间戳列表 $\mathbf{T} = [0, t_1, \dots, t_n, 1]$（其中 $t_i \in [0,1]$），模型直接生成对应时刻的中间帧：

$$[\mathbf{x}_{t_1}, \dots, \mathbf{x}_{t_n}] = \mathrm{ArbInterp}(\mathbf{x}_0, \mathbf{x}_1, \mathbf{T}) \tag{1}$$

这一范式将插值从“固定帧数生成”解放为“任意时刻采样”，使得帧率控制和时长伸缩成为时间戳选择的自然结果。

### 3.2 流匹配训练框架

模型采用流匹配（Flow Matching）作为生成基础。对于去噪时间步 $n \in [0,1]$，训练时仅对非条件帧（即排除首帧 $\mathbf{z}_1$、末帧 $\mathbf{z}_t$ 及前缀帧 $\mathbf{z}_2$）添加高斯噪声：

$$\mathbf{z}_i^n = n \cdot \boldsymbol{\epsilon}_i^n + (1 - n) \cdot \mathbf{z}_i, \quad 2 \leq i \leq t-1$$

去噪网络 $u_\theta$ 预测速度向量，训练目标为预测速度与真实速度的 L2 损失，且仅计算非条件帧位置：

$$\mathcal{L} = \sum_{i=1}^{t} \mathbf{m}_i \odot \| \mathbf{v}_n - u_{\theta}(\mathbf{z}^n, n, \mathbf{y}) \|^2, \quad \mathbf{v}_n = \boldsymbol{\epsilon}^n - \mathbf{z} \tag{2}$$

其中 $\mathbf{m}_i$ 为非条件帧掩码，$\mathbf{y}$ 为条件信息。该设计确保条件帧的潜在表示始终被真实值替换（Token Replace），仅对中间帧进行去噪学习。

### 3.3 时间戳感知旋转位置嵌入（TaRoPE）

#### 3.3.1 从绝对位置到连续时间戳

传统时间 RoPE 以帧索引 $k$ 作为绝对位置，对第 $k$ 个潜在帧 $\mathbf{z}_k$ 施加旋转：

$$\tilde{\mathbf{z}}_k = \mathrm{RoPE}(\mathbf{z}_k, k) = \mathbf{z}_k e^{i\theta_k}, \quad \theta_k = k \cdot \theta_{\mathrm{base}} \tag{3}$$

这种设计将位置信息固化在序列索引上，使得模型只能生成训练时见过的固定帧数，无法泛化到任意长度或任意时刻的插值。

TaRoPE 的核心创新在于将位置信息从离散索引替换为归一化连续时间戳。对于包含 $N$ 帧的视频，第 $k$ 帧的时间戳定义为：

$$t_k = \frac{k - 1}{N - 1}, \quad \mathrm{s.t.}\ 1 \leq k \leq N \tag{5}$$

此时首帧 $t_1 = 0$，末帧 $t_N = 1$，中间帧均匀分布在 $[0,1]$ 区间。训练时，模型学习的是时间戳与帧内容的连续映射关系；推理时，只需指定任意 $t \in [0,1]$，即可生成对应时刻的帧。这一设计是 ArbInterp 实现“任意时刻插值”的关键因果机制——时间 RoPE 的位置依赖性被重新校准为连续函数，而非离散查找表。

#### 3.3.2 分段训练与分层插值策略

为支持长序列生成并控制自注意力复杂度，ArbInterp 采用分段训练策略：每次采样 1 至 19 帧中间帧，最大时间跨度 2 秒，使模型在有限资源下学习连续时间戳映射。推理时根据目标帧数选择策略：

- **直接插值**：短序列（≤21 帧）直接一次生成。
- **分段插值**：长序列分解为多个子段，逐段生成，段间通过外观-运动解耦条件（见 3.4 节）维持一致性。
- **分层插值**：超长序列（>21 帧）先预测 $t=0.5$ 处关键帧 $\mathbf{x}_{0.5}$，再以该帧为界生成两个子段。该策略将自注意力复杂度从 $O(N^2)$ 降至 $O(N^2/M)$（$M$ 为段数）。

### 3.4 外观-运动解耦条件注入

长序列分段生成的核心瓶颈在于段间时空一致性。直接拼接前段末尾帧作为条件（潜在拼接）会引入外观噪声；交叉注意力注入则计算开销大且运动信息易丢失。ArbInterp 提出外观-运动解耦条件策略，将一致性维护拆分为两个并行通道：

- **外观条件**：将前一段的末尾帧作为前缀帧直接输入编码器，通过 Token Replace 将其真实潜在替换噪声潜在，强制后续生成匹配该帧的外观。
- **运动条件**：通过运动语义提取器（Motion Semantic Extractor, MSE）从前 $N$ 帧提取运动令牌。MSE 首先使用时序增强 CLIP 提取时空特征（在 CLIP 特征上添加时序嵌入，并扩展自注意力感受野至所有帧），再通过 Q-Former 将特征压缩为固定数量的运动令牌。这些令牌注入 DiT 各块的交叉注意力层，引导运动连贯性。

消融实验（Table 2）表明，该策略在 Subject Consist.（0.9441 vs 0.9297 移除外观）、Temporal Flick.（0.9624 vs 0.9549 移除运动）上均有显著提升，且推理步时从 4.4s（潜在拼接）降至 2.6s，效率提升约 40%。

## 实验与分析

### 多尺度插值主结果

ArbInterp 在 MultiInterpBench（覆盖 552 个帧对，来自 DAVIS、SNU-FILM、XTEST）上，于 2×、8×、16×、32× 四个插值比例下全面超越现有方法。Table 1 记录的核心指标如下：

![[assets/figures/papers/iclr26_0010_eKGkb4cFRe_Arbitrary_Generative_Video_Interpolation/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison with the state-of-the-art methods on MultiInterpBench. The boldfaced and underlined colors indicate the best and second best performing methods, respectively. ↑ indicates higher is better, ↓ indicates lower is better (applied to individual metrics in the header). though effective, this method significantly increases computational overhead during both training and inference. Alternatively, another simple approach is to inject prior segment information through cross-attention (Figure 4(b)). While efficient, this approach yields weaker appearance consistency compared to direct latent concatenation (Zhang et al., 2024)*

- **2× 插值**：FVD 降至 44.9，较此前最优的 DynamiCrafter（57.2）降低 12.3。
- **8× 插值**：FVD 降至 33.0，较 DynamiCrafter（56.3）降低 23.3。
- **16× 插值**：FVD 降至 28.4，较 DynamiCrafter（49.7）降低 21.3。
- **32× 插值**：FVD 降至 28.4，较此前最优的 LDMVFI（39.7）降低 11.3。

在 LPIPS、FID、CLIPimg 及 VBench 的七项一致性指标（主体一致性、背景一致性、时间闪烁、运动平滑度等）上，ArbInterp 同样取得最优或次优结果。这表明该方法在不同插值密度下均能保持高保真度和时空连贯性。

**256× 极端插值泛化**：在额外收集的 10 个视频上评估 256× 插值时（Table 3），ArbInterp 的 FVD 为 242.3，显著低于此前最优的 ArbInterp-SVD（385.0），降幅达 142.7。这一结果验证了 TaRoPE 的连续时间建模能力即使在高倍率、超出训练分布的场景下仍能有效泛化。

![[assets/figures/papers/iclr26_0010_eKGkb4cFRe_Arbitrary_Generative_Video_Interpolation/figures/014_Table_3.jpg]]
*Table 3: Quantitative comparison with the state-of-the-art methods on 256x interpolation*

### 消融实验

Table 2 系统拆解了核心设计的作用，主要发现如下：

![[assets/figures/papers/iclr26_0010_eKGkb4cFRe_Arbitrary_Generative_Video_Interpolation/figures/008_Table_2.jpg]]
*Table 2: Ablation study on key designs of ArbInterp*

**时间戳注入方式**：
- TaRoPE（Ours）在运动平滑度上达到 0.9817，而无时间戳注入的 Vanilla 基线仅为 0.9637。仅使用 MLP AdaLN 注入时间戳的方法同样不及 TaRoPE。
- 定性对比（Figure 11）进一步显示，TaRoPE 能精确生成与指定时间戳对应的中间帧，而基线方法在相同时间戳下出现明显的时序错位或运动模糊。

**外观-运动解耦条件策略**：
- 完整策略（Ours）在主体一致性（0.9441）、背景一致性（0.9628）和时间闪烁（0.9624）上均领先于潜在拼接条件（Latent Cond.）和交叉注意力条件（CrossAttn）。
- 移除运动信息（w/o Motion）导致时间闪烁降至 0.9549，运动平滑度下降；移除外观信息（w/o Appearance）使主体一致性降至 0.9297。这表明运动令牌对时序连贯性尤为关键，而外观条件主要约束段间主体一致性。
- 计算效率方面，该策略将单步推理时间从潜在拼接的 4.4 秒降至 2.6 秒，加速约 40%。

**训练阶段策略**：
Table 4 验证了三阶段训练的必要性。仅进行第三阶段（直接学习任意时间戳插值）时，FVD₃₂ₓ 为 401.6；依次加入第一阶段（固定帧数插值基础训练）和第二阶段（段间连续性训练）后，FVD₃₂ₓ 逐步降至 319.9，VBench 也从 0.819 提升至 0.8324。这证明先学基本插值、再学连续性、最后联合微调的策略能在有限资源下达到最优性能。

![[assets/figures/papers/iclr26_0010_eKGkb4cFRe_Arbitrary_Generative_Video_Interpolation/figures/016_Table_4.jpg]]
*Table 4: Ablation study on different training stages*

### 定性分析

**时空一致性**（Figure 5）：在时间戳 0.25、0.5、0.75 处，ArbInterp 生成的中间帧在主体姿态、纹理细节和背景稳定性上均优于 DynamiCrafter 和 LDMVFI，后者在快速运动区域出现明显的伪影和形变。

**外观-运动解耦效果**（Figure 6）：直接分段预测（a）在段间衔接处出现主体跳变和纹理不连续；加入解耦条件后（b），段间过渡平滑，主体外观保持一致。

![[assets/figures/papers/iclr26_0010_eKGkb4cFRe_Arbitrary_Generative_Video_Interpolation/figures/010_Figure_6.jpg]]
*Figure 6: Visual comparison of appearance-motion decoupling conditioning strategies. (a) is produced by direct segment-by-segment prediction. (b) is the result with our proposed strategy. Figure 7: Visualization of independently predicted intermediate frames at different timestamps*

**运动迁移验证**（Figure 10）：通过编辑首帧外观但保留运动令牌，生成的视频保持了原始运动模式，证实运动语义提取器（MSE）成功将运动信息与外观解耦。

### 失败模式与局限

1. **极端复杂场景**：模型基于 Wan2.1 1.3B 参数、仅 5 万视频片段训练，在包含剧烈遮挡、大幅度相机运动或细粒度纹理的场景中，生成质量可能出现退化。此点需在更大规模实验中进一步验证。
2. **段间绝对一致性**：尽管外观-运动解耦策略显著改善了段间过渡，但生成过程的随机性仍可能导致段边界处的微小外观偏移，尚未达到理论最优。
3. **缺乏语义条件**：当前模型仅以首尾帧为输入，无文本或其他语义引导，限制了可控性和复杂语义推理能力。

## 方法谱系与知识库定位

### 与现有方法的谱系关系

ArbInterp 的提出根植于视频帧插值（VFI）从确定性方法向生成式方法的演进脉络。传统基于光流的 VFI 方法（如 RIFE、AMT）在遮挡、大运动等场景中容易产生伪影，而生成式方法通过扩散模型建模帧间分布，天然具备更强的场景补全能力。然而，现有生成式 VFI 方法普遍存在一个结构性瓶颈：**只能生成固定数量的中间帧，无法灵活调整帧率或时长**。LDMVFI 基于潜在扩散模型执行固定比例的插值；TRF 通过时间回放框架实现生成，但同样受限于预设的帧数；GI 和 DynamiCrafter 虽然具备一定的生成灵活性，但其插值比例仍由训练时的帧间隔决定，缺乏对连续运动场细粒度建模的能力。

ArbInterp 的核心突破在于将 VFI 任务重新定义为**归一化时间戳 [0,1] 上的连续帧生成问题**。这一范式转换使模型不再受限于离散的帧索引，而是以任意时间戳列表作为输入，生成对应时刻的中间帧。与上述方法相比，ArbInterp 在以下维度形成了明确的差异化优势：

- **插值灵活性**：支持从 2× 到 256× 乃至理论上的无限长度插值，而 LDMVFI、TRF 等方法仅能处理训练时见过的固定比例。
- **时间感知精度**：通过时间戳感知旋转位置嵌入（TaRoPE），模型能精确感知每个帧在连续时间轴上的相对位置，而非仅依赖离散帧索引。
- **长序列一致性**：外观-运动解耦条件策略将长序列分解为段，通过注入前段末尾帧的外观信息和运动令牌，维持段间平滑过渡，这是现有方法未系统解决的问题。

在消融实验中，ArbInterp-SVD 作为变体使用交叉注意力注入前段信息（而非外观-运动解耦），其性能在 256× 插值下 FVD 为 385.0，显著弱于 ArbInterp 的 242.3（Table 3），表明解耦条件策略对长序列一致性的贡献不可替代。

### 适用边界与条件约束

尽管 ArbInterp 在灵活性和一致性上取得了显著进展，其适用边界受到以下因素的制约：

**输入条件限制**。当前模型仅以首尾帧作为输入条件，未使用文本描述、语义标签或其他模态信息。这意味着模型对场景语义的理解完全依赖视觉信号的隐式学习，在需要精确语义控制（如“保持人物身份不变但改变动作”）时能力受限。Figure 10 展示了运动解耦的初步效果——通过编辑首帧外观但保留运动令牌，可生成运动一致的新视频，但这一能力仍局限于外观层面的迁移，缺乏对高层语义的显式操控。

**模型与数据规模约束**。ArbInterp 基于 Wan2.1 1.3B 参数规模的生成模型构建，训练数据仅为 5 万视频片段（Appendix B.2）。在极端复杂场景（如快速运动、严重遮挡、多物体交互）下，模型的质量上限可能受限于此规模。Table 1 中 32× 插值的 FVD 为 28.4，虽优于所有对比方法，但绝对数值仍表明生成质量存在提升空间。

**段间一致性的理论边界**。尽管分段和分层策略将自注意力复杂度从 O(N²) 降至 O(N²/M)，有效支持了长序列生成，但段间的绝对一致性仍受生成随机性的影响。外观-运动解耦条件通过注入前段末尾帧和运动令牌缓解了这一问题，但无法完全消除段边界处的微小抖动。Table 2 中 Temporal Flick. 指标为 0.9624，虽优于消融变体，但距离理论最优仍有差距。

### 局限与开放问题

**局限一：语义可控性缺失**。当前框架未整合文本引导或其他语义条件，限制了生成的可控性。在需要指定中间帧语义内容（如“第 0.5 秒时人物应举起右手”）的场景中，模型无法响应此类指令。这是 ArbInterp 从“插值工具”迈向“可控生成工具”的关键障碍。

**局限二：复杂语义推理能力不足**。由于仅依赖视觉信号学习，模型对物理规律、因果关系等复杂语义的推理能力有限。在涉及物体遮挡-重现、非刚性变形等场景时，中间帧可能出现物理不合理的结果，这一问题在 256× 极高速插值下尤为突出（Table 3，FVD 242.3 虽最优但绝对质量有限）。

**局限三：计算资源与泛化性的权衡**。三阶段训练策略（Table 4）被证明对性能至关重要——仅使用 Stage 3 的 FVD₃₂ₓ 为 401.6，而完整三阶段降至 319.9。然而，该策略需要 20,000 步训练和 8 块 GPU（Appendix B.2），计算代价较高。在更大规模数据集和更大模型上是否能持续提升性能，以及如何平衡训练代价与收益，仍待验证。

**开放问题**：

1. **文本引导的高效整合**：如何将文本条件注入 TaRoPE 调制的时间表示中，使模型能根据语义指令生成特定时刻的中间帧？这需要设计新的条件融合机制，而非简单地将文本交叉注意力附加到现有架构。

2. **TaRoPE 的跨任务推广**：连续时间戳感知的位置编码思路能否推广至其他需要连续位置建模的视频生成任务，如可变帧率视频预测、时间超分辨率等？这涉及验证 TaRoPE 作为一种通用时间表示范式的潜力。

3. **运动语义提取器的通用化**：外观-运动解耦中的运动语义提取器（MSE）通过时间增强 CLIP 和 Q-Former 将前序帧的运动信息压缩为固定数量的令牌。这一模块能否进一步抽象为更通用的运动先验，服务于跨域风格迁移、运动重定向等下游任务？Figure 10 的初步实验表明这一方向具有可行性，但需要更系统的验证。

4. **规模扩展的收益边界**：在更大规模的数据集（如百万级视频片段）和更大模型（如 10B+ 参数）上，ArbInterp 的复杂场景性能是否会出现质变？还是说，当前架构的瓶颈在于时间表示本身，而非模型容量？这需要系统的扩展实验来回答。

## 原文 PDF

![[paperPDFs/ICLR_2026/Arbitrary_Generative_Video_Interpolation.pdf]]
