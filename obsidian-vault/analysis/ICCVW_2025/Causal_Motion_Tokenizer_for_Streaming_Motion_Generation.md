---
title: Causal Motion Tokenizer for Streaming Motion Generation
type: paper
paper_level: A
venue: ICCVW
year: 2025
pdf_ref: paperPDFs/ICCVW_2025/Causal_Motion_Tokenizer_for_Streaming_Motion_Generation.pdf
project_link: null
code_link: null
aliases:
- CMTSMG
tags:
- ICCVW_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用因果卷积的运动分词器与记忆令牌机制，使模型能够基于已生成的运动上下文自回归地生成下一段运动，同时通过代码掩盖和双层训练增强长序列处理能力。
primary_logic: 将残差向量量化与因果卷积结合，构建因果运动表示空间，使得每一帧的编码只受过去帧影响，从而支持流式推理；同时利用掩码Transformer和残差Transformer实现文本到运动令牌的高效生成，无需全局重处理。
claims:
- MotionStream在HumanML3D运动合成基准上的过渡平滑性指标PJ为0.05、AUJ为0.38，显著优于FlowMDM（PJ 0.06, AUJ 0.51）和其他基线。
- 相比于无记忆令牌的变体，MotionStream的过渡FID从3.45降至2.56，验证了记忆令牌对过渡平滑的贡献。
- 在文本到运动生成上，MotionStream达到R-Precision Top1 0.522，与最先进模型MoMask（0.521）持平，同时保持低FID 0.057。
- HumanML3D (运动合成) 上 FID (Subsequence) = 0.13 ± 0.02
---

# Causal Motion Tokenizer for Streaming Motion Generation

> [!tip] 核心洞察
> 将残差向量量化与因果卷积结合，构建因果运动表示空间，使得每一帧的编码只受过去帧影响，从而支持流式推理；同时利用掩码Transformer和残差Transformer实现文本到运动令牌的高效生成，无需全局重处理。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向流式运动生成的因果运动分词器 |
| 英文题名 | Causal Motion Tokenizer for Streaming Motion Generation |
| 会议/期刊 | ICCVW 2025 |
| Links | [paper](https://www.openaccess.thecvf.com/content/ICCV2025W/I-HFM/papers/Jiang_Causal_Motion_Tokenizer_for_Streaming_Motion_Generation_ICCVW_2025_paper.pdf) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MotionStream |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D (运动合成) 上，FID (Subsequence) 0.13 ± 0.02 vs FlowMDM: 0.29 ± 0.01 (-55.2%)；AUJ (Transition) 0.38 ± 0.03 vs FlowMDM: 0.51 ± 0.01 (-25.5%)。
> - HumanML3D (文本到运动) 上，R-Precision Top1 0.522 ± 0.003 vs MoMask: 0.521 ± 0.002 (+0.1%)；FID 0.057 ± 0.003 vs MoMask: 0.045 ± 0.002 (+26.7% (higher))；MMDist 2.903 ± 0.010 vs MoMask: 2.958 ± 0.008 (-1.9%)。

## 概要

**问题瓶颈**：现有非流式运动生成方法在处理多段连续运动时，通常采用拼接或插值进行后处理，难以实现平滑过渡，且无法实时响应连续文本输入。这一限制严重制约了其在机器人控制、交互动画等需要低延迟流式生成的场景中的应用。

**核心洞察与因果机制**：MotionStream 的核心设计在于将**因果卷积**与**残差向量量化（RVQ）**结合，构建因果运动表示空间。在该空间中，每一帧的编码仅依赖于过去帧，从而天然支持流式推理，无需全局重处理。在此基础上，通过**掩码Transformer**和**残差Transformer**的双Transformer方案，实现从文本描述到多层运动令牌的高效生成。

**方法定位**：MotionStream 属于基于 VQ-VAE 的离散运动令牌生成范式，与 **MoMask** 等强基线共享残差量化与掩码建模的思路。其关键差异化在于：(1) 将标准1D卷积替换为1D因果卷积；(2) 引入代码掩盖与双重轮次训练增强分词器鲁棒性；(3) 设计记忆令牌机制，以前一段运动的结尾帧作为条件指导下一段生成，实现片段间无缝过渡；(4) 采用交叉注意力替代特征拼接进行文本条件注入。

**主要结果**：在 HumanML3D 运动合成基准上，MotionStream 的过渡平滑指标 PJ 为 0.05、AUJ 为 0.38，显著优于 **FlowMDM**（PJ 0.06, AUJ 0.51）。在文本到运动生成任务上，R-Precision Top1 达到 0.522，与 **MoMask**（0.521）持平，同时维持较低的 FID（0.057）。消融实验证实，代码掩盖和记忆令牌是过渡平滑性的关键贡献因素——移除记忆令牌后过渡 FID 从 2.56 升至 3.45，移除代码掩盖后子序列 FID 从 0.13 退化至 1.56。此外，MotionStream 支持约 0.2 秒延迟的实时流式生成。

**局限与待验证方向**：当前方法仅限于描述性动作输入，对高层级指令的支持不足；模型范围限于人体运动，缺乏面部和手部细节表现。文中声称的实时延迟性能（约0.2秒）未在实验结果表格中直接呈现，建议读者根据实际部署环境进行验证。



### 问题背景：非流式运动生成的瓶颈

在机器人控制、交互式动画和实时叙事驱动等应用中，系统需要根据连续输入的文本指令实时生成自然、平滑的人体运动序列。然而，现有运动生成方法大多采用非流式（offline）范式，面临两个核心瓶颈：

**拼接与插值的过渡不自然。** 主流方法通常为每段独立文本生成独立的运动片段，再通过后处理拼接（stitching）或插值（interpolation）将它们连接起来。这种方式难以保证片段间的物理一致性和运动平滑性，容易在过渡处产生抖动、滑步或不自然的姿态跳变。

**无法实时响应连续输入。** 部分方法尝试在一次推理中处理多段文本以生成完整运动序列，但随着文本数量增加，计算延迟线性增长，无法满足实时流式场景的响应需求。Figure 2 直观展示了这一困境：传统拼接/插值方案（2.a）和单次多文本推理方案（2.b）在延迟和过渡质量上均存在明显短板，而流式方案（2.c）则能在保持低延迟的同时实现无缝过渡。

### 因果运动表示的根本缺失

上述问题的深层原因在于：现有运动分词器（motion tokenizer）在编码运动序列时，每一帧的编码可以同时“看到”过去和未来的帧，即采用非因果（non-causal）的时空建模方式。这导致两个后果：

1. **无法支持自回归流式推理。** 当模型需要基于已生成的运动上下文逐段生成后续运动时，非因果编码器要求重新处理全局序列，破坏了流式生成的因果一致性。
2. **过渡信息未被显式建模。** 片段间的过渡区域缺乏专门的表示和生成机制，完全依赖后处理手段进行弥补。

因此，构建一个因果的运动表示空间——使得每一帧的编码仅受过去帧影响——成为实现流式运动生成的关键前提。

### 本文动机

针对上述缺口，本文提出 **MotionStream**，核心动机包括：

- **构建因果运动分词器。** 将残差向量量化（Residual Vector Quantization, RVQ）与因果卷积（causal convolution）结合，使得运动编码器天然遵循时间因果性，每一帧的令牌编码仅依赖当前及历史帧，从而支持逐段自回归的流式推理，无需全局重处理。

- **引入记忆令牌机制。** 在生成下一段运动时，将前一段运动的结尾帧作为“记忆令牌”（Memory Tokens）显式注入生成过程，使模型能够感知并延续先前的运动上下文，从根本上解决片段间过渡不自然的问题。

- **保持文本到运动生成质量。** 在实现流式能力的同时，通过掩码Transformer和残差Transformer的双Transformer方案，确保单段文本到运动生成的质量不退化，达到与现有最先进方法（如MoMask）相当甚至更优的水平。

简言之，MotionStream 旨在将运动生成从“离线拼接”范式推进到“因果流式”范式，使模型能够根据连续文本输入实时生成平滑、连贯的运动序列。



## 核心方法与创新机理

MotionStream 的核心创新在于将**因果运动分词器**与**记忆令牌机制**结合，首次在运动生成领域实现了真正的流式推理能力。相比于现有的非流式方法（如 MoMask、FlowMDM），MotionStream 不需要对多段运动进行后处理拼接或插值，而是通过自回归的方式，基于已生成的运动上下文逐段生成连续运动，从根本上解决了过渡平滑性问题。

### 关键设计变更点

**1. 因果卷积替代标准卷积**

MoMask 等基线方法使用标准 1D 卷积构建运动分词器，编码时每一帧可以“看到”未来帧的信息，导致分词器无法支持流式推理。MotionStream 将编码器和解码器中的卷积层全部替换为 **1D 因果卷积**（Sec. 3.1），确保每一帧的潜在表示仅依赖于当前及过去帧。这一变更使得分词器输出的运动令牌天然具备时间因果性，为后续的流式生成提供了表示空间的基础。

**2. 双重轮次训练与代码掩盖**

常规 RVQ 训练通常仅使用量化层 dropout 来增强鲁棒性。MotionStream 引入了**双重轮次训练（Double Round Training）**和**代码掩盖（Code Masking）**策略（Sec. 3.1）。代码掩盖在训练过程中随机遮蔽部分基础层令牌，迫使模型学习从残缺的令牌序列中重建完整运动。消融实验（Table 3）表明，移除代码掩盖后，运动合成子序列 FID 从 0.13 急剧退化至 1.56，过渡 FID 从 2.56 升至 4.59，证实了该机制对模型稳健性的决定性作用。

**3. 记忆令牌实现无缝过渡**

现有方法（如 MoMask 配合插值）在处理多段运动时依赖后处理来平滑过渡，缺乏对运动上下文的显式建模。MotionStream 提出**记忆令牌（Memory Tokens）**机制（Sec. 3.2）：将前一个运动片段的结尾帧作为条件令牌输入掩码 Transformer，指导下一段运动的生成。消融实验（Table 3）显示，移除记忆令牌使过渡 FID 从 2.56 上升至 3.45，验证了该机制对过渡平滑性的显著贡献。

**4. 交叉注意力替代特征拼接**

在文本条件注入方式上，MoMask 采用 CLIP 池化特征与运动令牌的直接拼接。MotionStream 改用**交叉注意力（Cross-Attention）**机制，将文本条件与 CLIP 编码器的最后隐藏层进行交互（Sec. 3.2）。消融实验（Table 4）表明，交叉注意力（CA）相比特征拼接（C）在文本到运动生成的 FID 上从 0.088 降至 0.057，说明更细粒度的文本-运动对齐有助于提升生成质量。

综上，MotionStream 通过上述四个关键设计变更，构建了一个端到端的流式运动生成框架。其核心洞察在于：因果卷积保证了表示空间的时序因果性，记忆令牌提供了跨片段的条件依赖，而代码掩盖和交叉注意力则分别增强了训练的鲁棒性和文本对齐的精度。这些创新共同使得 MotionStream 能够在约 0.2 秒的延迟下实现实时流式生成，同时保持与最先进非流式方法（如 MoMask）相当的文本到运动生成质量。



MotionStream 的整体 pipeline 围绕“因果运动分词器 + 双 Transformer 生成”两条主线构建，目标是实现从连续文本流到无缝运动序列的流式生成。其核心设计逻辑是：**将运动生成问题转化为离散令牌的自回归预测问题，并强制令牌的编码过程满足因果约束**，从而在推理时无需全局重处理即可逐段产出平滑过渡的运动。

### 模块关系与数据流

系统由三个关键模块串联构成，数据流方向为“原始运动 → 离散令牌 → 文本条件生成 → 运动重建”：

1. **因果运动分词器 (Causal Motion Tokenizer)**：负责将原始运动序列压缩为多层离散令牌，并通过因果卷积确保每一帧的编码仅依赖过去帧。该模块采用编码器-解码器结构，内部集成了残差向量量化 (RVQ)，共 6 层量化，每层码本大小为 1024。
2. **掩码 Transformer (Mask Transformer)**：以文本描述为条件，基于 BERT 风格的掩码建模预测基础层运动令牌。在流式场景下，它利用前一个运动片段的结尾帧作为**记忆令牌 (Memory Tokens)**，为下一段生成提供上下文锚点，实现片段间的因果过渡。
3. **残差 Transformer (Residual Transformer)**：接收已生成的基础层令牌及前序残差层令牌，逐层预测对应文本的后续残差令牌，完成从粗到细的运动令牌重建。

推理时，文本流依次输入，掩码 Transformer 和残差 Transformer 自回归地生成当前片段的运动令牌，分词器解码器再将这些令牌还原为连续运动序列。由于编码器本身是因果的，且记忆令牌机制传递了片段间的上下文，整个过程天然支持流式输出，无需后处理插值或拼接。

### 关键设计选择

- **因果卷积替代标准卷积**：编码器和解码器中的 1D 卷积均沿时间维度施加因果掩码，使潜在表示 $z_i$ 仅依赖于 $\{x_1, \dots, x_i\}$。这是流式推理的根基——若使用标准卷积，当前帧的编码会“窥视”未来帧，导致训练-推理不一致。
- **代码掩盖与双层训练**：在分词器训练阶段随机掩盖部分输入帧的代码，迫使模型从残缺上下文中重建运动。这一机制提升了模型对长序列和不完整输入的稳健性，消融实验表明移除代码掩盖会使子序列 FID 从 0.13 退化至 1.56。
- **记忆令牌机制**：流式生成时，前一片段的最后若干帧被编码为记忆令牌，作为当前片段掩码 Transformer 的附加条件。这为过渡区域提供了显式的运动上下文，使过渡 FID 从无记忆令牌时的 3.45 降至 2.56。
- **交叉注意力条件注入**：文本条件通过交叉注意力与 CLIP 编码器的最后隐藏层交互，而非简单的特征拼接。消融实验显示，交叉注意力在 FID 上优于拼接方案 (0.057 vs 0.088)。

### 与基线方法的架构差异

相比于强基线 MoMask（同样采用 RVQ + 掩码 Transformer 的范式），MotionStream 的架构变更集中在三个“槽位”：

| 组件 | MoMask | MotionStream |
|------|--------|--------------|
| 卷积类型 | 标准 1D 卷积 | 1D 因果卷积 |
| 分词器训练 | 常规 RVQ + 量化 dropout | 双层轮次训练 + 代码掩盖 |
| 过渡处理 | 无记忆令牌，依赖后处理插值 | 记忆令牌自回归过渡 |

这些变更使得 MotionStream 在保持文本到运动生成质量与 MoMask 持平（R-Precision Top1 0.522 vs 0.521）的同时，获得了流式生成能力和显著更优的过渡平滑性。

### 整体框架图引导

系统整体架构可参照 **Figure 1**（方法概览）与 **Figure 4**（双 Transformer 方案概览）。因果运动分词器的内部结构详见 **Figure 3**，其中展示了编码器-解码器中因果卷积的堆叠方式以及 RVQ 的逐层量化流程。流式生成的延迟优势与现有方法的范式对比则在 **Figure 2** 中呈现，MotionStream 在 V100 上可达约 0.2 秒的生成延迟，且延迟随文本提示数线性增长，而拼接/插值方法则需等待全部文本输入后统一处理。

![[assets/figures/papers/paper_list_l21_https_www_openaccess_thecvf_com_content_ICCV2025W_I_HFM_papers_Jiang_Cau/figures/001_Figure_1.jpg]]
*Figure 1: Method overview: MotionStream consists of a motion tokenizer V (Sec. 3.1) a Mask Transformer (Sec. 3.2) and a Residual Transformer (Sec. 3.3). MotionStream is capable of producing seamless and dynamic motions driven by narrative descriptions*



MotionStream 由三个核心模块构成：因果运动分词器（Causal Motion Tokenizer）、掩码Transformer（Mask Transformer）和残差Transformer（Residual Transformer），三者协同实现从连续文本到流式运动的因果生成。

### 因果运动分词器

运动分词器 $V$ 采用编码器-解码器结构。编码器 $\mathcal{E}_m$ 沿时间维度施加1D因果卷积，将 $L$ 帧原始运动序列转换为 $L$ 个潜在向量，确保每一帧的编码仅取决于当前及过去帧，杜绝未来信息泄露。解码器 $\mathcal{D}_m$ 同样配备因果卷积，从离散令牌重建连续运动序列。

潜在向量随后进入残差向量量化（Residual Vector Quantization, RVQ）模块。与传统单层矢量量化不同，RVQ 通过多层递进式量化逐步细化表示。量化函数为：

$$z_i = Q(\hat{z}^i) := \arg\min_{z_k \in Z} \|\hat{z}_i - z_k\|_2$$

该式将第 $i$ 个潜在向量 $\hat{z}^i$ 映射到可学习码本 $Z$ 中欧氏距离最近的条目 $z_k$。MotionStream 采用6层RVQ，每层码本大小为1024，逐层量化残差，最终得到多层因果运动令牌。

分词器训练中引入两项关键策略：**代码掩盖（Code Masking）** 在训练时随机掩盖部分令牌，迫使模型学习鲁棒的上下文推理能力；**双重轮次训练（Double Round Training）** 则分两阶段优化，先预训练基础层，再联合微调全部残差层，增强长序列建模稳定性。

### 掩码Transformer

掩码Transformer 负责从文本描述预测基础层运动令牌 $x^{1:L}_0$。其采用BERT风格的掩码建模范式：输入序列中部分令牌被替换为 `[MASK]`，模型基于可见令牌和文本条件预测被掩盖位置的真实令牌。损失函数为负对数似然：

$$\mathcal{L}_{\mathrm{mask}} = \sum_{\tilde{x}_k^0=[\mathrm{MASK}]} -\log p_\theta(x_k^0 | \tilde{x}^0, w_s)$$

其中 $\tilde{x}^0$ 为部分掩盖的基础层令牌序列，$w_s$ 为文本嵌入。文本条件通过交叉注意力注入：CLIP文本编码器的最后隐藏层特征与Transformer中间表示进行交叉注意力计算，替代传统特征拼接方式。

为实现流式生成中的平滑过渡，掩码Transformer引入**记忆令牌（Memory Tokens）** 机制：将前一个运动片段的最后若干帧对应的运动令牌作为条件拼接到当前输入中，使模型能够基于已生成的运动上下文自回归地生成下一段运动，无需后处理插值或拼接。

### 残差Transformer

残差Transformer 以已生成的基础层令牌和前序残差层令牌为条件，逐层预测后续残差层的离散令牌。其损失函数为：

$$\mathcal{L}_{\mathrm{res}} = \sum_{k=1}^K \sum_{i=1}^L -\log p_\phi(x_i^k | x_i^{1:k-1}, w_s, k)$$

其中 $x_i^k$ 为第 $k$ 层残差量化中第 $i$ 帧的令牌，$x_i^{1:k-1}$ 表示前 $k-1$ 层已生成的令牌序列，$w_s$ 为文本嵌入，$k$ 为层指示符。值得注意的是，第 $k$ 层预测层与第 $k+1$ 层运动令牌嵌入层之间共享参数，简化架构的同时利用了层间特征连续性。

### 关键公式汇总

| 公式 | 变量含义 | 作用 |
|------|----------|------|
| $z_i = Q(\hat{z}^i)$ | $\hat{z}^i$：潜在向量；$Z$：可学习码本；$z_k$：码本条 | 将连续潜在表示量化为离散令牌 |
| $\mathcal{L}_{\mathrm{mask}}$ | $\tilde{x}^0$：掩盖后基础层令牌；$w_s$：文本嵌入 | 训练掩码Transformer预测基础层令牌 |
| $\mathcal{L}_{\mathrm{res}}$ | $x_i^k$：第$k$层第$i$帧令牌；$K$：残差层数；$L$：序列长度 | 训练残差Transformer逐层预测残差令牌 |

### 补充图表

![[assets/figures/papers/paper_list_l21_https_www_openaccess_thecvf_com_content_ICCV2025W_I_HFM_papers_Jiang_Cau/figures/003_Figure_3.jpg]]
*Figure 3: The architecture of MotionStream’s motion tokenizer, V, detailed in Sec. 3.1. It showcases the Residual Vector Quantization (RVQ) framework employed by the tokenizer, which includes both an encoder and a decoder equipped with causal convolutions. This design enables the effective encoding and decoding of motion data, ensuring temporal coherence and continuity in the generated motions*

![[assets/figures/papers/paper_list_l21_https_www_openaccess_thecvf_com_content_ICCV2025W_I_HFM_papers_Jiang_Cau/figures/004_Figure_4.jpg]]
*Figure 4: Method overview: In addition to the motion tokenizer, a dual transformer scheme is proposed to accurately predict causal motion tokens from the given textual inputs, effectively translating complex textual descriptions into corresponding dynamic motions*



## 实验与关键发现

### 评估设置与基线

实验主要基于 **HumanML3D** 数据集，评估涵盖两个任务维度：**运动合成**（Motion Composition）与**文本到运动生成**（Text-to-Motion）。运动合成任务关注多段运动拼接后的子序列质量与过渡平滑性，文本到运动生成则沿用标准协议，采用 R-Precision、FID、MMDist、Diversity 等指标。基线包括扩散模型方法 **FlowMDM**、**DoubleTake**、**MultiDiffusion**、**DifCollage**，以及基于掩码和残差 Transformer 的强基线 **MoMask**。所有方法均在相同评估器下进行比较，非流式方法的插值/拼接后处理均按官方实现适配。

### 运动合成：过渡平滑性与子序列质量

Table 1 给出了 HumanML3D 上的运动合成对比。MotionStream 在子序列质量指标上取得最优：**FID 为 0.13**，相比 FlowMDM 的 0.29 降低了约 55%，显著优于所有扩散基线。过渡平滑性方面，MotionStream 的 **PJ 达到 0.05**、**AUJ 为 0.38**，均优于 FlowMDM（PJ 0.06, AUJ 0.51）和 MoMask 的插值变体（PJ 0.07, AUJ 0.53）。这一结果直接验证了因果运动分词器在流式生成中无需后处理插值即可实现平滑过渡的核心优势。

![[assets/figures/papers/paper_list_l21_https_www_openaccess_thecvf_com_content_ICCV2025W_I_HFM_papers_Jiang_Cau/figures/005_Table_1.jpg]]
*Table 1: Comparison of motion composition on HumanML3D [17] dataset. The arrows (→) indicate that closer to Real is desirable. Bold and underline indicate the best and the second best result on text-to-motion task*

值得注意的是，MoMask 原生的非流式生成在子序列 FID 上表现尚可（0.16），但过渡指标（PJ 0.07, AUJ 0.53）明显劣于 MotionStream，说明仅靠后处理插值难以弥合片段间的语义连续性缺口。

### 文本到运动生成：与强基线的对比

Table 2 展示了文本到运动生成任务的结果。MotionStream 在 **R-Precision Top1 上达到 0.522**，与当前最优模型 MoMask（0.521）持平；**MMDist 为 2.903**，略优于 MoMask 的 2.958。这表明因果约束并未损害生成运动与文本的语义对齐质量。

![[assets/figures/papers/paper_list_l21_https_www_openaccess_thecvf_com_content_ICCV2025W_I_HFM_papers_Jiang_Cau/figures/006_Table_2.jpg]]
*Table 2: Comparison of text-to-motion on HumanML3D [17]. The empty MModality indicates Real motion is deterministic. The arrows (→) indicate that closer to Real is desirable. Bold and underline indicate the best and the second best result on text-to-motion task*

在 FID 指标上，MotionStream 为 0.057，略高于 MoMask 的 0.045（+26.7%）。这一差距可能源于因果卷积对单段运动重建精度的轻微限制——编码器只能依赖过去帧信息，缺乏未来帧的全局视野。但考虑到 MotionStream 同时具备流式生成能力，这一权衡是可接受的。

### 消融研究：关键设计的因果验证

消融实验（Table 3 及 Table 4）系统验证了三个核心设计的作用：

![[assets/figures/papers/paper_list_l21_https_www_openaccess_thecvf_com_content_ICCV2025W_I_HFM_papers_Jiang_Cau/figures/008_Table_4.jpg]]
*Table 4: Ablation Study on the Token Compression Factor R and condition injection architecture in the Mask Transformer Applied on the HumanML3D Dataset*

**代码掩盖（Code Masking）**：移除代码掩盖后，运动合成子序列 FID 从 0.13 急剧退化至 1.56，过渡 FID 从 2.56 升至 4.59。这表明在训练阶段随机掩盖部分运动令牌，是提升模型对不完整上下文鲁棒性的关键机制，直接支撑了流式场景下基于已生成片段进行自回归预测的能力。

**记忆令牌（Memory Tokens）**：移除记忆令牌后，过渡 FID 从 2.56 升至 3.45，证实了将前一段运动的结尾帧作为条件注入下一段生成，是平滑过渡的核心因果通路。记忆令牌的作用机制在于：它为掩码 Transformer 提供了显式的运动上下文锚点，使新生成的片段在起始帧处与历史运动保持连续。

**令牌压缩因子与条件注入架构**（Table 4）：压缩因子 $R=2$ 在 FID 上表现最优（0.057），优于 $R=1$（0.102）和 $R=4$（0.095），说明适度的时序压缩在计算效率与重建质量间取得平衡。条件注入方式上，**交叉注意力（CA）** 相比特征拼接（C）将 FID 从 0.088 降至 0.057，验证了通过交叉注意力将文本特征与运动令牌进行细粒度交互的有效性。

### 延迟性能与流式优势

Figure 2 展示了不同方法的生成延迟随文本提示数量变化的趋势。在 V100 机器上，MotionStream 的延迟增长近乎线性且斜率平缓，单次生成延迟约 0.2 秒。相比之下，需要全局重处理的非流式方法（如拼接/插值方案）在多段文本下延迟急剧上升。这一结果从系统效率角度佐证了因果运动分词器在实时流式场景中的工程价值。

![[assets/figures/papers/paper_list_l21_https_www_openaccess_thecvf_com_content_ICCV2025W_I_HFM_papers_Jiang_Cau/figures/002_Figure_2.jpg]]
*Figure 2: Motion Generation Approaches and Latency Performance Overview. (1) Generation latency versus number of text prompts on a V100 machine. (2.a) Generation of individual motions from separate text prompts, combined via stitching or interpolation. (2.b) Approach processing multiple texts in a single inference step to generate a whole motion sequence. (2.c) Approach to generate continuous motion from consecutive text inputs without post-processing stitching*

### 局限与待验证点

当前评估集中在 HumanML3D 数据集的人体运动领域，模型对动物等多骨骼结构的泛化能力尚未验证。此外，所有实验基于描述性动作文本，对高层叙事指令的响应能力缺乏定量评估。消融实验中记忆令牌的贡献在过渡 FID 上虽有显著改善（2.56 vs 3.45），但绝对数值仍偏高，说明长序列过渡的视觉平滑性仍有提升空间，这一结论需要用户研究进一步佐证。

### 补充图表

![[assets/figures/papers/paper_list_l21_https_www_openaccess_thecvf_com_content_ICCV2025W_I_HFM_papers_Jiang_Cau/figures/007_Table.jpg]]



## 定位与知识库关联

### 运动分词器：从标准VQ-VAE到因果残差量化

MotionStream的运动分词器直接继承自基于残差向量量化（RVQ）的离散运动表示范式，其最直接的强基线为 **MoMask**（Guo et al.，ECCV 2024），后者同样采用多层RVQ将运动序列量化为多尺度离散令牌。两者的关键分叉点在于**卷积类型**：MoMask使用标准1D卷积，编码器在时间维度上具有全局感受野，每一帧的潜在表示可依赖未来帧信息；MotionStream则将编码器与解码器中的1D卷积全部替换为**因果卷积**（Sec. 3.1），强制每一帧的编码仅依赖当前及过去帧，从而构建出因果运动令牌空间。这一改动使得分词器天然支持流式推理——新到达的运动帧无需重新编码历史序列，仅需增量计算即可获得离散表示。

在训练策略上，MotionStream在常规RVQ训练（含量化层dropout）的基础上引入两项增强：**代码掩盖**（Code Masking）与**双重轮次训练**（Double Round Training）。代码掩盖在训练时随机将部分运动令牌替换为掩码令牌，迫使分词器学习从上下文推断缺失片段，显著提升了模型对不完整输入的鲁棒性。消融实验（Table 3）表明，移除代码掩盖后，运动合成子序列FID从0.13急剧退化至1.56，过渡FID从2.56升至4.59，证实了该机制对长序列建模稳健性的关键作用。双重轮次训练则通过分阶段优化编码器-解码器与量化码本，缓解了RVQ训练中常见的码本坍塌问题。

### 文本到运动生成：掩码建模与残差预测的因果适配

在生成侧，MotionStream采用双Transformer架构——掩码Transformer（Mask Transformer）与残差Transformer（Residual Transformer），这一设计同样与MoMask的生成范式高度对齐。核心差异在于**记忆令牌**（Memory Tokens）机制的引入：在流式生成场景中，前一个运动片段的结尾帧被编码为记忆令牌，作为掩码Transformer的条件输入，指导下一个片段的生成。这一设计使得片段间过渡无需后处理插值或拼接，而是通过自回归生成自然衔接。消融实验显示，移除记忆令牌后过渡FID从2.56升至3.45，验证了其对过渡平滑性的显著贡献。

文本条件的注入方式也发生了变化：MoMask采用CLIP池化特征与运动令牌特征拼接的方式，而MotionStream改用**交叉注意力**（Cross-Attention）直接作用于CLIP文本编码器的最后隐藏层（Sec. 3.2）。Table 4的消融表明，交叉注意力（CA）相比特征拼接（C）在FID上有所提升（0.057 vs 0.088），说明细粒度的文本-运动对齐对流式生成更为关键。

### 运动合成：与扩散模型基线的定位差异

在运动合成（motion composition）任务上，MotionStream与基于扩散模型的方法形成鲜明对比。**FlowMDM**（扩散模型基线）采用去噪扩散过程生成运动，在合成多段运动时需依赖后处理插值或拼接，导致过渡区域出现不自然的抖动。Table 1数据显示，FlowMDM的过渡AUJ为0.51，而MotionStream仅为0.38（越低越平滑），过渡PJ也从0.06降至0.05。**DoubleTake**、**MultiDiffusion**、**DifCollage**等扩散类方法同样面临类似瓶颈——它们或需要全局重处理，或无法在生成过程中利用已生成片段的上下文。MotionStream的因果分词器与记忆令牌机制从根本上规避了这一问题：历史运动信息已编码在因果令牌流中，新片段生成时无需访问完整历史序列。

### 适用边界与局限

MotionStream的流式能力建立在因果卷积的严格时间约束之上，这带来了明确的适用边界：

1. **输入模态限制**：当前方法仅处理描述性动作文本输入（如“人向前走并挥手”），无法处理高层级叙事指令（如“他感到悲伤”）。这限制了其在端到端故事驱动动画生成中的应用，需要额外的高层语义解析模块。

2. **骨骼结构泛化**：模型在HumanML3D和BABEL数据集上训练，两者均基于SMPL-H人体骨骼拓扑。论文明确指出，当前工作范围限于人体运动，不包括动物等多样化骨骼结构，且缺乏面部表情和手部手势的细节表现。这需要手动验证——论文未提供跨骨骼泛化的实验证据。

3. **实时延迟边界**：尽管论文声称支持约0.2秒延迟的实时流式生成，但该数据未在实验表格中系统报告（仅在摘要和引言中提及），且未与基线方法在相同硬件条件下进行延迟对比。Figure 2的延迟曲线提供了部分佐证，但缺乏详细的硬件配置与测量协议说明，该指标需要手动验证。

### 开放问题与后续方向

论文明确指出的开放问题包括：

- **高层指令的集成**：如何扩展输入模态以包括抽象和叙事驱动的指令，使模型能理解“他犹豫了一下，然后转身离开”这类复合语义？
- **多骨骼结构支持**：如何将因果运动分词器泛化至四足动物、鸟类等非人体骨骼拓扑，同时保持流式生成的时间一致性？
- **细粒度运动增强**：如何提升面部表情和手部手势的生成精度，使流式运动生成适用于高保真虚拟人交互场景？
- **硬件效率优化**：在保持因果约束的前提下，能否通过令牌压缩因子（Table 4显示R=2最优）的进一步优化或模型量化，将延迟降至更低以满足嵌入端设备需求？

从知识库定位角度看，MotionStream填补了“流式文本驱动运动生成”这一细分领域的方法空白——现有工作要么牺牲过渡平滑性换取实时性（拼接/插值类方法），要么追求生成质量但无法流式推理（扩散模型类方法）。其因果分词器与记忆令牌的组合为后续工作提供了可复用的技术组件，但叙事理解、跨骨骼泛化和细粒度控制仍是待解决的关键瓶颈。



## 原文 PDF

![[paperPDFs/ICCVW_2025/Causal_Motion_Tokenizer_for_Streaming_Motion_Generation.pdf]]
