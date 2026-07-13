---
title: "Video-LaVIT: Unified Video-Language Pre-training with Decoupled Visual-Motional Tokenization"
type: paper
paper_level: A
venue: ICML
year: 2024
pdf_ref: paperPDFs/ICML_2024/Video_LaVIT_Unified_Video_Language_Pre_training_with_Decoupled_Visual_Motional_Tokenization.pdf
project_link: https://video-lavit.github.io
code_link: null
aliases:
- VL
- Video-LaVIT
tags:
- ICML_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "利用MPEG-4中的运动向量将视频分解为关键帧和运动信息，分别用独立的离散标记化器编码，以交替的“视觉-运动”令牌序列在LLM中进行自回归预训练。"
primary_logic: "通过解耦视觉语义与运动动态，以运动向量作为描述时间变化的紧凑代理，仅需少量额外标记即可显著增强视频理解与生成，同时保持与图像、文本的统一框架。"
claims:
- "视频中大部分内容在时间上高度冗余，可由运动向量刻画，因此可以进行高效标记化（Figure 1）。"
- "加入运动标记化后，零样本视频问答准确率显著提升，如MSVD-QA从70.7%提至73.2%（Table 2）。"
- "增强运动条件（EMC）对于恢复视频中的动态至关重要，去除后运动几乎消失（Figure 10）。"
- "仅需135个运动令牌即可在理解与生成任务上取得高性能，体现了方法的高效性（Table 7）。"
---

# Video-LaVIT: Unified Video-Language Pre-training with Decoupled Visual-Motional Tokenization

> [!tip] 核心洞察
> 通过解耦视觉语义与运动动态，以运动向量作为描述时间变化的紧凑代理，仅需少量额外标记即可显著增强视频理解与生成，同时保持与图像、文本的统一框架。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Video-LaVIT：解耦视觉-运动标记化的统一视频-语言预训练 |
| 英文题名 | Video-LaVIT: Unified Video-Language Pre-training with Decoupled Visual-Motional Tokenization |
| 会议/期刊 | ICML 2024 |
| Links | [paper](https://arxiv.org/abs/2402.03161) · [Project](https://video-lavit.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Video-LaVIT |
| Dataset | VQA v2, MSVD-QA, MSRVTT-QA, Perception Test |

> [!tip] 效果简介
> - VQA v2 上，Accuracy 为 80.3，对比 78.5 (LLaVA-1.5)，变化 +1.8。
> - MSVD-QA 上，Accuracy 为 73.2，对比 70.7 (Video-LLaVA)，变化 +2.5。
> - MSRVTT-QA 上，Accuracy 为 59.3，对比 59.2 (Video-LLaVA)，变化 +0.1。

## 概要

视频-语言预训练的核心瓶颈在于如何高效编码时空动态：现有方法要么忽视运动信息，要么使用3D编码器产生过长的标记序列并带来巨大计算开销，难以扩展到长视频。Video-LaVIT 的关键观察是，视频中大部分内容在时间上高度冗余，可由运动向量刻画（Figure 1）。基于此，该方法将视频解耦为关键帧和运动向量，分别用独立的离散标记化器编码，形成交替的“视觉-运动”令牌序列，在大型语言模型中进行统一自回归预训练。

在13个多模态基准测试上，Video-LaVIT 展现出极具竞争力的性能。图像理解方面，VQA v2 准确率达 80.3%（vs LLaVA-1.5 的 78.5%）；零样本视频问答中，MSVD-QA 准确率从 70.7% 提升至 73.2%；文本-视频生成方面，MSR-VTT 的 FVD 降至 188.36（vs VideoPoet 的 213），UCF-101 的 IS 提升至 44.26（vs 38.44）。消融实验证实，移除运动令牌后 MSVD-QA 准确率降至 68.4%，而仅需 135 个运动令牌即可在理解与生成任务上取得高性能，验证了该方法的高效性。

Video-LaVIT 的方法定位在于：以 MPEG-4 运动向量作为描述时间变化的紧凑代理，通过解耦视觉语义与运动动态，仅需少量额外标记即可显著增强视频理解与生成，同时保持与图像、文本的统一框架。

### 视频-语言预训练的核心瓶颈

多模态大语言模型在图像理解与生成上取得了显著进展，但将其能力扩展至视频领域仍面临根本性挑战。视频与静态图像的本质区别在于其蕴含丰富的**时间动态信息**——物体的运动、场景的切换、事件的演进。然而，现有视频-语言预训练方法在编码这些时空动态时陷入两难：

- **忽视运动信息**：部分方法将视频简单视为独立帧的集合，使用2D图像编码器逐帧提取视觉特征，完全丢失了帧间的时序关联。
- **3D编码器的代价**：为捕捉时间维度，另一类方法采用3D卷积或时空Transformer对视频片段进行联合编码。但这会产生极长的视觉标记序列，导致自注意力计算量随序列长度呈平方增长，难以扩展至长视频场景。

这一瓶颈的深层原因在于：视频数据在时间维度上存在**高度冗余性**。如Figure 1所示，相邻帧之间的大部分像素内容保持静态，真正发生变化的仅是局部运动区域。现有方法未能有效利用这一冗余特性，导致计算资源被大量浪费在重复编码静态背景上。

### 运动向量：被忽视的紧凑运动表征

本文的核心观察源于视频压缩领域的经典技术——**运动向量**。在MPEG-4等现代视频编码标准中，视频被分解为关键帧（I-frame）和描述帧间像素位移的运动向量。这些运动向量以极低的带宽代价，精确刻画了视频中的时间变化模式。

Video-LaVIT从这一观察出发，提出将视频解耦为**关键帧（视觉语义）** 和**运动向量（时间动态）** 两个独立通道，分别进行离散标记化。这一设计的因果逻辑在于：

1. **关键帧**承载场景的语义内容（物体、纹理、布局），可由成熟的图像标记器高效编码。
2. **运动向量**作为时间变化的紧凑代理，仅需少量离散令牌即可描述帧间动态，无需逐帧编码完整像素。

### 统一多模态预训练的缺失

除效率问题外，现有视频-语言模型还面临**模态割裂**的困境。图像理解、视频理解、文本生成通常由独立设计的模块处理，缺乏统一的表示框架。Video-LaVIT的目标是构建一个将视频、图像、文本统一为离散令牌序列的生成式预训练范式，使大语言模型能够在同一自回归目标下无缝处理所有模态。

### 方法概览与关键设计

基于上述动机，Video-LaVIT的核心架构（Figure 2）包含三个关键组件：

- **视频分解与标记化**：从MPEG-4压缩流中提取关键帧和运动向量，分别通过EVA-CLIP视觉编码器和时空VQ-VAE编码为离散令牌，形成交替的“视觉-运动”令牌序列。
- **视频去标记化**：通过以关键帧和运动向量为条件的3D U-Net扩散模型，将离散令牌恢复为连续像素视频。其中**增强运动条件（EMC）** 通过输入拼接和交叉注意力融入运动特征，是保证重建保真度的关键。
- **统一自回归预训练**：将视觉令牌、运动令牌与文本令牌拼接为多模态序列，在Llama 2 7B上进行下一令牌预测训练，支持视频/图像理解与生成的双向任务。

通过这种解耦设计，Video-LaVIT仅需**135个运动令牌**即可在理解与生成任务上取得高性能（Table 7），显著降低了视频编码的计算开销，同时保持与图像、文本模态的统一框架兼容性。

## 核心方法与创新机理

Video-LaVIT 的核心创新在于将视频从“密集像素帧序列”重新定义为“关键帧 + 运动向量”的**解耦表示**，并围绕这一表示构建了统一的视频-语言预训练框架。其关键创新点可归纳为三个相互耦合的 changed slots。

### 1. 解耦的视觉-运动标记化

传统视频-语言模型（如 Video-LLaVA、LLaMA-VID）通常均匀采样所有帧，用 2D 或 3D 视觉编码器将其转化为冗长的 token 序列，既未显式建模运动信息，又带来巨大的计算开销。Video-LaVIT 的突破口在于利用视频的时间冗余性：一个镜头内的主要语义可由单张关键帧承载，而帧间变化可由紧凑的运动向量描述（Figure 1）。

具体而言，视频被分解为**关键帧**（I-frame）和 **T 帧运动向量**（直接从 MPEG-4 压缩流中提取，无需昂贵的光流计算）。关键帧沿用 LaVIT 的图像 tokenizer（EVA-CLIP ViT-G/14）编码为离散视觉令牌；运动向量则通过一个**时空 VQ-VAE** 编码为离散运动令牌，其量化过程基于 L2 归一化距离查找码本中最近码字：

$$z_{i} = \arg\min_{j} \| l_{2}(\hat{z}_{i}) - l_{2}(c_{j}) \|_{2}$$

最终，视频被表示为一个交替的 `<visual, motion, ...>` 令牌序列。这一设计使视频的 token 数量大幅压缩——仅需 **135 个运动令牌**即可在理解与生成任务上取得高性能（Table 7），从根本上解决了 3D 编码器 token 序列过长的问题。

### 2. 运动感知的分步视频去标记化

将离散令牌恢复为连续视频帧时，Video-LaVIT 没有采用端到端的 3D 扩散模型直接生成，而是设计了**分步解码策略**：先由图像扩散模型根据视觉令牌生成关键帧，再由 **3D U-Net 去标记器** $g_V$ 以关键帧和运动令牌为条件，逐帧重建后续帧。

这里的关键创新是**增强运动条件（Enhanced Motion Conditioning, EMC）**：运动特征不仅作为 3D U-Net 的输入拼接，还通过交叉注意力层融入去噪过程。消融实验表明，仅使用运动向量作为输入条件而移除 EMC，重建视频中的动态几乎消失（Figure 10），证明 EMC 是恢复视频运动保真度的不可或缺组件。

对于长视频生成，Video-LaVIT 进一步引入**显式噪声约束**：将上一片段的末帧通过 DDIM 反演至中间噪声状态，作为下一片段关键帧生成的初始噪声：

$$x_{t+1} = \sqrt{\frac{\alpha_{t+1}}{\alpha_t}} x_t + \left( \sqrt{\frac{1}{\alpha_{t+1}} - 1} - \sqrt{\frac{1}{\alpha_t} - 1} \right) g_I(x_t, t, \hat{I})$$

这一约束显著改善了片段间的时间一致性（Figure 5），使自回归生成长视频成为可能。

### 3. 多模态序列的统一自回归预训练

Video-LaVIT 通过特殊分隔符（如 `[MOV]`、`[/MOV]`）区分视觉与运动模态，并将 `[视频/图像, 文本]` 的顺序进行交换，以支持**双向生成预训练**——即同一个 LLM（Llama 2 7B）既能从视频生成文本（理解），也能从文本生成视频令牌（生成）。训练目标为标准的下一个 token 预测：

$$p(y) = \sum_{y \in \mathcal{D}} \sum_{i=1}^{S} \log P_{\theta}(y_i | y_{<i})$$

关键的是，在统一预训练中加入运动令牌对图像理解性能的影响微乎其微（VQAv2 仅差 0.3%，Table 9），验证了解耦标记化能和谐地统一图像、视频与文本三种模态，而不会引发模态冲突。

**总结**：Video-LaVIT 的创新链条是——用运动向量作为时间动态的紧凑代理 → 解耦视觉与运动令牌 → 分步去标记化 + EMC 恢复运动 → 统一自回归预训练。这一设计使模型在仅使用 10M 视频片段训练的情况下，在 13 个多模态基准上取得了有竞争力的表现，尤其在视频生成 FVD 指标上显著优于使用 270M 数据训练的 VideoPoet（MSR-VTT FVD: 188.36 vs. 213, Table 4）。

![[assets/figures/papers/paper_list_l13_Video_LaVIT_Unified_Video_Language_Pre_training_with_Decoupled_Visual_Mo/figures/003_Figure_3.jpg]]
*Figure 3: Illustrations for video detokenization in Video-LaVIT. (a) Training pipeline for the video detokenizer, which aims to reconstruct the original video clip using one keyframe and the subsequent motion vectors. (b) Autoregressive inference for long video decoding*

Video-LaVIT 提出了一种解耦视觉-运动标记化的统一视频-语言预训练框架。其核心设计思路源于一个关键观察：视频中大部分内容在时间上高度冗余，这些冗余可由运动向量紧凑刻画（Figure 1）。基于此，该框架将视频分解为关键帧与运动向量两个正交分量，分别用独立的离散标记化器编码，最终以交替的“视觉-运动”令牌序列在大型语言模型中进行统一自回归预训练。

### 核心瓶颈与因果机制

现有视频-语言预训练方法面临一个根本性瓶颈：要么完全忽视运动信息，仅对均匀采样的帧进行2D编码；要么采用3D编码器联合建模时空信息，但这会产生过长的令牌序列并带来巨大的计算开销，难以扩展到长视频。Video-LaVIT 的因果调节旋钮在于：利用MPEG-4压缩过程中可直接提取的运动向量作为描述时间变化的紧凑代理，将视频的语义内容（关键帧）与动态变化（运动向量）解耦。这一解耦使得仅需少量额外运动令牌即可显著增强视频理解与生成能力，同时保持与图像、文本模态的统一框架。

### 整体Pipeline与模块关系

Video-LaVIT 的整体流程由三个核心阶段构成，各模块协同工作形成端到端的统一框架（Figure 2）：

**1. 视频分解与标记化（Tokenizer）**

视频首先被分解为单个关键帧（I-frame）和 T 帧运动向量。关键帧承载视频的主要语义内容，运动向量则刻画相邻帧间的像素位移。两者分别进入独立的标记化器：
- **关键帧标记器**：直接复用 LaVIT 预训练的图像标记器（基于 EVA-CLIP ViT-G/14），将关键帧转化为离散视觉令牌，继承已有的视觉码本和先验知识。
- **运动标记器**：采用时空 VQ-VAE 架构，将运动向量序列编码为离散运动令牌。运动向量通过寻找相邻帧间最佳宏块匹配来估计（Equation 1），随后经向量量化映射到码本中 L2 归一化距离最近的离散码字（Equation 2）。

视频最终被表示为交替的 `<visual, motion, visual, motion, ...>` 令牌序列。

**2. 视频去标记化（Detokenizer）**

去标记化采用分步解码策略：先由图像扩散模型根据视觉令牌恢复关键帧，再由 3D U-Net 架构的视频去标记器以关键帧和运动令牌为条件重建后续帧。3D U-Net 通过在原始 2D U-Net 的空间模块后插入时间卷积和注意力层实现。其中，增强运动条件（EMC）通过输入拼接和交叉注意力将运动特征融入去标记器，对恢复视频动态至关重要——消融实验表明，去除 EMC 后运动几乎消失（Figure 10）。去标记器的训练目标为 EDM 去噪扩散损失（Equation 3）。

**3. 统一生成式预训练**

多模态序列以特殊分隔符（如 `[MOV]`、`[/MOV]`）区分视觉与运动模态，并与文本令牌拼接。通过交换 `[视频/图像, 文本]` 的顺序，支持双向生成预训练。整个序列在 Llama 2 7B 上以标准的下一令牌预测目标进行自回归优化（Equation 5）。

### 长视频生成与时间一致性

对于长视频生成，框架引入显式噪声约束机制：将上一片段的末帧通过 DDIM 反演至中间噪声状态（Equation 4），作为下一关键帧生成的初始噪声。这一约束显著改善了片段间的时间一致性（Figure 5），使得自回归解码的视频片段能够平滑衔接。

### 方法优势与证据强度

- **高效性**：仅需 135 个运动令牌即可在理解与生成任务上取得高性能（Table 7），验证了运动向量作为紧凑时间代理的有效性。
- **统一性**：在统一预训练中加入运动令牌对图像理解性能影响微乎其微（VQAv2 仅差 0.3%，Table 9），证明解耦标记化能和谐地统一多模态。
- **竞争力**：在 13 个多模态基准上取得有竞争力的结果，零样本视频问答（MSVD-QA 73.2%，Table 2）和文本-视频生成（MSR-VTT FVD 188.36，Table 4）均达到领先水平。

### 已知局限

- 受限于 LLM 上下文窗口（4096）和预训练数据平均视频长度（约15秒），无法生成数分钟级别的长视频。
- 训练计算开销仍然较高，难以直接扩展至网络级视频数据。
- 长视频生成中不同片段的关键帧可能过于相似，因为训练数据场景变化较少，限制了多样化长视频的生成能力。

### 3.1 视频分解与标记化

Video-LaVIT的核心设计在于将视频解耦为**关键帧**（keyframe）与**运动向量**（motion vectors）两部分，分别进行离散标记化。这一设计基于一个关键观察：同一镜头内的视频帧在语义上高度冗余，其时间变化可由运动向量紧凑描述（Figure 1）。

**关键帧标记器**直接复用LaVIT（Jin et al., 2024）中预训练的图像标记器，将关键帧编码为离散视觉令牌，从而继承已有的视觉码本和先验知识。

**运动向量提取**利用MPEG-4压缩过程中可直接获取的运动向量，无需额外昂贵的稠密光流计算。对于相邻帧 $I_{t-1}$ 与 $I_t$，运动向量通过宏块匹配估计：

$$\vec{m}(p,q) = \arg\min_{i,j} \| I_t(p,q) - I_{t-1}(p-i, q-j) \|$$

其中 $(p,q)$ 为宏块位置，$(i,j)$ 为搜索范围内的位移候选。该过程可在CPU上高速完成（Wu et al., 2018）。

**运动标记器**采用时空VQ-VAE架构，将提取的运动向量序列编码为离散运动令牌。编码器输出的连续嵌入 $\hat{z}_i$ 通过L2归一化后，查找码本中距离最近的码字 $c_j$ 进行量化：

$$z_i = \arg\min_j \| l_2(\hat{z}_i) - l_2(c_j) \|_2$$

最终，一段视频被表示为交替的视觉-运动令牌序列：`⟨visual, motion, ...⟩`，作为LLM自回归预训练的监督信号（Figure 2）。

### 3.2 视频去标记化

视频去标记器 $g_V$ 负责将离散令牌序列恢复为连续像素空间中的视频帧。其采用**顺序解码策略**：先由图像扩散模型 $g_I$ 根据视觉令牌生成关键帧 $\hat{I}$，再以关键帧和运动令牌 $\hat{M}$ 为条件，通过3D U-Net生成后续帧。

**3D U-Net架构**是在2D U-Net的空间卷积和注意力层之后插入时间卷积和注意力层得到的3D变体（Figure 3(a)）。其训练目标采用EDM（Elucidating Diffusion Models）框架的去噪损失：

$$\mathbb{E}_{(X_0, \hat{I}, \hat{M}) \sim \mathcal{D}, \sigma, n} \left[ \lambda_{\sigma} \| g_V(X_0 + n, \sigma, \hat{I}, M) - X_0 \| \right]$$

其中 $X_0$ 为原始视频片段，$n$ 为随机噪声，$\sigma$ 为噪声水平，$\lambda_{\sigma}$ 为噪声相关的损失权重。

**增强运动条件（EMC）** 是去标记器中的关键设计：运动特征不仅作为输入与噪声视频拼接，还通过交叉注意力层注入3D U-Net的中间特征。消融实验表明，仅将运动向量作为输入条件而移除EMC，重建视频的动态几乎消失（Figure 10）。

**长视频解码的噪声约束**：自回归解码多个视频片段时，直接将上一片段末帧 $x_0^{\text{last}}$ 通过DDIM反演至中间噪声状态，作为下一片段关键帧生成的初始噪声：

$$x_{t+1} = \sqrt{\frac{\alpha_{t+1}}{\alpha_t}} x_t + \left( \sqrt{\frac{1}{\alpha_{t+1}} - 1} - \sqrt{\frac{1}{\alpha_t} - 1} \right) g_I(x_t, t, \hat{I})$$

该显式噪声约束显著改善了片段间的时间一致性（Figure 5, Figure 3(b)）。

### 3.3 统一生成式预训练

多模态序列由视觉令牌、运动令牌和文本令牌通过特殊分隔符（如 `[MOV]`, `[/MOV]`）组织而成。训练时交换 `[视频/图像, 文本]` 的顺序以支持双向生成（理解与生成）。整体优化目标为标准的自回归语言建模损失：

$$p(y) = \sum_{y \in \mathcal{D}} \sum_{i=1}^{S} \log P_{\theta}(y_i | y_{<i})$$

其中 $y$ 为多模态令牌序列，$S$ 为序列长度，$\theta$ 为LLM参数（Llama 2 7B）。该目标使模型在统一的next-token prediction框架下同时学习多模态理解和生成能力。

## 实验与关键发现

### 核心瓶颈与因果验证

Video-LaVIT的核心假设是：视频中的大部分内容在时间上高度冗余，可通过运动向量高效刻画（Figure 1）。这一假设构成了整套方法的基础——若运动向量不足以捕获关键动态，则解耦标记化将失效。实验围绕两个因果问题展开验证：（1）运动标记化是否真正提升了视频理解与生成？（2）解耦表示是否在统一多模态预训练中引入冲突？

**运动标记化的因果效应**：Table 6（左）的消融实验直接验证了因果链。移除运动令牌后，零样本视频问答准确率显著下降：MSVD-QA从73.2%降至68.4%（-4.8%），MSRVTT-QA从59.3%降至56.8%（-2.5%），ActivityNet-QA从47.9%降至44.9%（-3.0%）。这一致且显著的退化证明运动信息是视频理解的因果性因素，而非无关的辅助信号。在生成侧（Table 6右），移除运动令牌后FVD从188.36恶化至261.10（+38.6%），IS从44.26降至33.21（-25.0%），进一步证实运动令牌对生成质量的关键作用。

![[assets/figures/papers/paper_list_l13_Video_LaVIT_Unified_Video_Language_Pre_training_with_Decoupled_Visual_Mo/figures/011_Table_6.jpg]]
*Table 6: Ablation of proposed motion tokenization strategy in zeroshot video understanding (left) and generation (right)*

**增强运动条件（EMC）的因果角色**：Figure 10的消融揭示了运动令牌与去标记器之间的因果交互。当仅使用运动向量作为3D U-Net的输入条件（w/o EMC）时，重建视频的动态几乎消失，表明运动令牌本身携带的信息不足以独立驱动视频重建。EMC通过输入拼接和交叉注意力将运动特征融入去标记器，充当了“运动信息放大器”的角色——它将紧凑的运动令牌转化为可操作的时空先验。这一发现说明，解耦标记化的有效性不仅依赖于运动信息的提取，更依赖于去标记化阶段的信息融合设计。

**统一预训练的模态兼容性**：Table 9验证了在统一预训练中引入运动令牌是否损害图像理解。结果显示，VQAv2仅从80.3%降至80.0%（-0.3%），GQA从64.7%降至64.3%（-0.4%），差异在统计噪声范围内。这表明解耦标记化成功实现了模态间的和谐统一——运动令牌的加入未在LLM的表示空间中引入破坏性冲突。

### 运动令牌效率分析

Table 7揭示了运动令牌数量N的缩放行为。在N=0（无运动）到N=135之间，视频理解（MSVD-QA从68.4%升至73.2%）和生成（FVD从261.10降至188.36）均持续改善。但当N从135增至270时，性能趋于饱和（MSVD-QA 73.1%，FVD 188.01），表明135个令牌已能捕获视频中的关键运动信息。这一效率源于运动向量的紧凑性：MPEG-4压缩天然提取了宏块级位移，避免了学习冗余的像素级变化。与使用稠密光流或3D卷积的方法相比，Video-LaVIT以极小的令牌开销（135 vs. 数千个视觉令牌）实现了竞争力的性能。

![[assets/figures/papers/paper_list_l13_Video_LaVIT_Unified_Video_Language_Pre_training_with_Decoupled_Visual_Mo/figures/012_Table_7.jpg]]
*Table 7: Ablation of the number of motion tokens (denoted by N) in zero-shot video understanding (left) and generation (right)*

### 长视频生成与噪声约束

Figure 5的消融直接展示了式(4)中显式噪声约束的因果效应。在生成“a 360 shot of a sleek yacht...”的长视频时，无噪声约束的片段间出现明显的运动不连续（游艇位置跳跃），而施加噪声约束后片段过渡平滑。该机制的工作原理是：将上一片段的末帧通过DDIM反演至中间噪声状态，作为下一关键帧生成的初始噪声——这强制了片段边界的像素级一致性。

Table 5量化了长视频生成的性能：FVD为113.37，KVD为4.94，CLIPSIM为0.9621。但需注意，该评估仅基于2048个生成样本（EvalCrafter提示），且训练数据（WebVid-10M）平均视频长度约15秒，因此模型对更长视频的泛化能力仍需谨慎解读。

![[assets/figures/papers/paper_list_l13_Video_LaVIT_Unified_Video_Language_Pre_training_with_Decoupled_Visual_Mo/figures/009_Table_5.jpg]]
*Table 5: Zero-shot text-to-long video generation performance. It is evaluated on 2048 long videos (64 frames) generated using the prompts from EvalCrafter (Liu et al., 2023d)*

### 公平性与评估局限性

若干评估细节需要审慎对待：

1. **图像理解对比的不公平因素**：Table 1中LLaVA-1.5使用336分辨率输入，而Video-LaVIT未明确说明分辨率设置。更高的分辨率可能为LLaVA-1.5带来不公平优势，Video-LaVIT在VQAv2上仍领先1.8%的结果因此更加显著。

![[assets/figures/papers/paper_list_l13_Video_LaVIT_Unified_Video_Language_Pre_training_with_Decoupled_Visual_Mo/figures/004_Table_1.jpg]]
*Table 1: Image understanding performance (↑) on 8 benchmarks. Video-LaVIT achieves state-of-the-art results on most of the benchmarks. For convenience, SQAI denotes ScienceQA-IMG (Lu et al., 2022), and MMB denotes MMBench (Liu et al., 2023e). * indicates that there is some overlap with the training data. Note that only LLaVA-1.5 (Liu et al., 2023a) is reported with a higher image resolution of 336. The Video-LLaVA, LLaMA-VID and LLaVA-1.5 use Vicuna-1.5 (Chiang et al., 2023) as the language model*

2. **训练数据重叠**：Table 1中标*的数据集（如VQAv2、GQA）与预训练数据存在部分重叠，相应结果可能偏高，不宜作为严格零样本泛化的证据。

3. **GPT辅助评估的偏差**：视频问答采用GPT助手的相对评分（Score），该指标可能受助理偏好、提示设计等因素影响，与人类判断的一致性未经验证。

4. **生成对比中的数据不对称**：Table 4中VideoPoet等基线使用270M视频片段训练，而Video-LaVIT仅使用10M——在数据规模相差27倍的情况下，Video-LaVIT在MSR-VTT上FVD领先24.64（188.36 vs. 213），在UCF-101上IS领先5.82（44.26 vs. 38.44），这一结果反而强化了方法的高效性。

![[assets/figures/papers/paper_list_l13_Video_LaVIT_Unified_Video_Language_Pre_training_with_Decoupled_Visual_Mo/figures/007_Table_4.jpg]]
*Table 4: Zero-shot text-to-video generation performance. Video-LaVIT delivers competitive results against state-of-the-art models trained on more proprietary data, with data size reported in terms of the number of training video clips. The next best results are underlined*

5. **长视频评估的样本量不足**：2048个样本可能无法覆盖多样化的场景和运动模式，泛化性能的置信区间较宽。

### 权重初始化的稳健性

Table 10检验了视频去标记器对预训练权重的依赖。使用svd-img2vid-xt初始化和随机初始化相比，FVD仅从188.36轻微增加至192.41（+2.1%），IS从44.26降至42.80（-3.3%）。这表明运动向量的引导信号足够强，即使从零开始训练去标记器也能有效学习视频重建，降低了对大规模视频预训练模型的依赖。

### 失败模式与局限性

尽管整体性能强劲，以下失败模式值得关注：

1. **长视频多样性不足**：受限于WebVid-10M中场景变化较少的特性，长视频生成中不同片段的关键帧可能过于相似，缺乏叙事性的场景演进。

2. **快速运动与镜头切换**：运动向量在快速运动或镜头切换场景中可能失效——宏块匹配假设相邻帧间的位移较小，剧烈变化会破坏这一假设。论文未系统评估此类场景的性能。

3. **LLM上下文窗口瓶颈**：4096的上下文窗口限制了可处理的视频长度，无法生成数分钟级别的视频。这是架构层面的硬约束，而非训练数据的限制。

4. **训练计算开销**：尽管标记化效率高，但整体训练仍需大量计算资源，难以直接扩展至网络级视频数据（如数亿片段）。论文承认需进一步挖掘视频的时空冗余以降低成本。

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

现有视频-语言预训练面临一个根本性矛盾：**时空动态的高效编码**。主流方案可分为两个极端：

- **2D图像编码器策略**：如 **Video-LLaVA**（Lin et al., 2023）和 **LLaMA-VID**（Li et al., 2023f）采用均匀帧采样，将每帧独立编码为视觉令牌。这种策略**完全忽视了帧间运动信息**，将视频退化为一组静态图像的集合。
- **3D编码器策略**：使用3D卷积或时空注意力对整个视频立方体编码，虽能捕获动态，但产生的令牌序列长度随帧数线性增长，**计算开销巨大**，难以扩展到长视频。

Video-LaVIT 的切入点在于：视频中的大部分内容在时间上高度冗余，这种冗余可由运动向量紧凑描述（Figure 1）。因此，**瓶颈不在于是否建模运动，而在于如何以最小的令牌代价编码运动**。

### 2. 方法谱系中的位置

Video-LaVIT 属于**离散令牌统一多模态预训练**这一技术路线，其谱系可追溯至：

- **图像-文本统一预训练**：**BLIP-2**（Li et al., 2023c）和 **Flamingo**（Alayrac et al., 2022）建立了视觉编码器与LLM之间的桥梁，但仅处理静态图像。**LaVIT**（Jin et al., 2024）进一步将图像离散化为视觉令牌，实现图像-文本的统一自回归建模。Video-LaVIT 直接继承了 LaVIT 的图像令牌化器，将这一范式从图像推向视频。
- **视频生成中的运动建模**：**VideoPoet**（Kondratyuk et al., 2023）、**CogVideo**（Hong et al., 2023）和 **Make-A-Video**（Singer et al., 2023）代表基于扩散模型的视频生成路线，它们或隐式学习运动，或依赖昂贵的稠密光流。Video-LaVIT 的独特之处在于**将MPEG-4运动向量作为免费的副产品引入**，既非完全隐式，也非计算密集。

### 3. 关键设计差异：与基线的对比

以下从四个核心维度阐明 Video-LaVIT 与代表性基线的本质差异：

| 维度 | 基线方案 | Video-LaVIT |
|------|----------|-------------|
| **视频表示形式** | 均匀采样所有帧的2D/3D视觉标记，未显式建模运动 | 解耦为单个关键帧和T帧运动向量，交替形成视觉-运动标记序列（Section 3.1, Figure 2） |
| **运动信息提取与编码** | 未使用运动信息或使用昂贵的稠密光流 | 直接从MPEG-4压缩中提取运动向量，并用时空VQ-VAE编码为离散运动令牌（Section 3.1, Equation 1, Equation 2） |
| **视频去标记化与长视频一致性** | 3D扩散模型直接生成，无特定运动引导或片段间一致性机制 | 分步解码：先由图像扩散模型生成关键帧，再通过3D U-Net（增强运动条件）生成后续帧；长视频解码中引入从上一片段末帧反演的噪声约束以保持时间一致性（Section 3.2, Equation 3, Equation 4, Figure 5） |
| **多模态序列组织** | 视觉与文本令牌简单拼接 | 用特殊分隔符（如[MOV]，[/MOV]）区分视觉与运动模态，交换[视频/图像，文本]顺序以支持双向生成预训练（Section 3.3, Equation 5） |

### 4. 适用边界与局限

Video-LaVIT 的设计存在明确的适用边界：

- **视频长度限制**：受限于LLM上下文窗口（4096）和预训练数据集（WebVid-10M平均视频长度约15秒），**无法生成数分钟级别的长视频**。尽管噪声约束机制改善了片段间一致性，但场景变化能力受限于训练数据中有限的场景多样性。
- **训练计算开销**：尽管运动令牌高效（仅135个），但整体训练流程仍涉及多个模块（图像令牌化器、运动令牌化器、视频去标记器、LLM），**计算开销仍然较高**，难以直接扩展至网络级视频数据。
- **复杂编辑视频**：该方法假设视频来自同一镜头内的连续拍摄，**未明确处理镜头切换、转场效果**等复杂编辑场景。运动向量在镜头边界处可能失效。
- **数据规模劣势**：视频生成对比中，VideoPoet等基线使用远大于本工作的训练数据（270M vs 10M视频片段），Video-LaVIT 在数据受限下虽具竞争力，但数据规模的限制可能影响长尾场景的生成质量。

### 5. 开放问题

以下问题有待进一步探索：

1. **噪声约束的泛化**：当前的DDIM反演噪声约束（Equation 4）在场景变化平缓时有效，但如何推广至包含快速运动或剧烈镜头变化的视频？是否存在更鲁棒的片段间一致性机制？

2. **运动令牌数量的自适应选择**：消融实验表明N=135已足够（Table 7），但该最优值是否依赖于视频内容类型、长度或动作复杂度？能否设计内容自适应的运动令牌分配策略？

3. **多模态联合训练的模态冲突**：在更大规模且异构的多模态数据上联合训练，是否会引发模态冲突或灾难性遗忘？Table 9显示加入运动令牌对图像理解影响微乎其微（VQAv2仅差0.3%），但更大规模下的稳定性仍需验证。

4. **更轻量级的运动估计**：当前依赖MPEG-4压缩过程中的运动向量提取，是否存在更轻量级的在线运动估计方案，以进一步降低标记化成本，同时保持或提升运动表示质量？

5. **评估的公平性**：图像理解对比中，LLaVA-1.5采用了更高输入分辨率（336），部分数据集与训练数据存在重叠（标*），视频问答评估采用GPT助手相对评分，这些因素可能影响结论的稳健性，需在统一条件下进一步验证。

## 原文 PDF

![[paperPDFs/ICML_2024/Video_LaVIT_Unified_Video_Language_Pre_training_with_Decoupled_Visual_Motional_Tokenization.pdf]]
