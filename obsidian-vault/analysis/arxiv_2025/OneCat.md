---
title: OneCat
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/OneCat.pdf
project_link: https://onecat-ai.github.io/
code_link: https://github.com/kakaobrain/coyo-dataset
aliases:
- OneCat
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 在纯解码器中嵌入模态特定的混合专家（Modality-MoE）和多尺度自回归生成机制（SAA），配合定制教师全层隐藏状态蒸馏，消除对外部编码器和分词器的依赖。
primary_logic: 通过将多尺度视觉自回归生成与模态特定计算（MoE）直接融入LLM解码器，并在早期融合中利用蒸馏弥补视觉感知预训练不足，可实现高效且统一的多模态智能。
claims:
- OneCAT-3B 在理解基准上对标 Emu3 取得显著提升（TextVQA +9.2, ChartQA +12.6, AI2D +7.8），且激活参数更少。
- 去除 SAA 导致生成性能明显下降（GenEval：81.2→78.1, DPG：74.9→74.0），证明 SAA 对多尺度生成的关键作用。
- 全层隐藏状态蒸馏优于仅蒸馏视觉token（平均分 35.3 vs 34.8）和不用蒸馏（31.4），且定制教师优于直接使用 Qwen2.5-VL 教师。
- OneCAT-3B 在 GenEval (0.90) 和 DPG-Bench (84.53) 上达到统一模型新SOTA，并大幅领先 BAGEL 等混合架构（T2I速度约10倍）。
---

# OneCat

> [!tip] 核心洞察
> 通过将多尺度视觉自回归生成与模态特定计算（MoE）直接融入LLM解码器，并在早期融合中利用蒸馏弥补视觉感知预训练不足，可实现高效且统一的多模态智能。

| 字段 | 内容 |
|------|------|
| 中文题名 | OneCAT：统一的纯解码器自回归多模态理解与生成模型 |
| 英文题名 | OneCat |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2509.03498) · [Project](https://onecat-ai.github.io/) · [Code](https://github.com/kakaobrain/coyo-dataset) · [paper](https://arxiv.org/abs/2509.07295) |
| Topic | #topic/other_unclear |
| Method | OneCAT |
| Dataset | TextVQA, ChartQA, GQA, AI2D |

> [!tip] 效果简介
> - TextVQA 上，准确率↑ 73.9 (OneCAT-3B) vs 64.7 (Emu3) (+9.2)。
> - ChartQA 上，准确率↑ 81.2 (OneCAT-3B) vs 68.6 (Emu3) (+12.6)。
> - GQA 上，准确率↑ 63.1 (OneCAT-3B) vs 60.3 (Emu3) (+2.8)。

## 概要

多模态大模型在理解和生成任务上取得了显著进展，但主流系统通常依赖于外部视觉编码器（如 ViT）和视觉分词器。这种分离式设计带来了两个核心瓶颈：一是额外的编码器/分词器显著增加了推理延迟和参数开销；二是跨模态信息只能在晚期融合，限制了模型在单一架构内高效统一理解、生成与编辑的能力。

**OneCAT** 针对这一瓶颈提出了一个根本性的解决方案：构建一个**纯解码器（decoder-only）的自回归统一多模态模型**，在推理时完全消除对外部视觉编码器和视觉分词器的依赖。其核心洞察在于，通过将多尺度视觉自回归生成与模态特定计算直接融入 LLM 解码器，并在早期融合中利用定制教师的全层隐藏状态蒸馏来弥补视觉感知预训练的不足，可以实现高效且统一的多模态智能。

具体而言，OneCAT 在纯解码器架构中嵌入了三个关键设计：（1）**模态特异的混合专家（Modality-MoE）**，为文本、理解和生成 token 分别配备专用的 FFN 专家；（2）**多尺度自回归生成机制（Scale-Aware Adapter, SAA）**，使 LLM 能按尺度顺序逐步预测视觉 token；（3）**全层隐藏状态蒸馏**，利用定制 MLLM 教师模型的中间层特征来指导视觉理解能力的学习。

在实验验证方面，OneCAT-3B 在理解基准上显著超越同类统一模型 Emu3（TextVQA +9.2，ChartQA +12.6，AI2D +7.8），且激活参数更少。在生成任务上，OneCAT-3B 在 GenEval（0.90）和 DPG-Bench（84.53）上达到统一模型的新 SOTA。效率方面，OneCAT 的理解首 token 延迟比 Qwen2.5-VL-3B 降低 61%，文生图推理速度比混合架构 BAGEL 快约 10 倍。消融实验证实了 SAA 对多尺度生成的关键作用，以及全层蒸馏策略对理解性能的决定性贡献。

**方法定位**：OneCAT 属于编码器自由的统一多模态自回归模型，其核心创新在于将模态路由、多尺度生成和知识蒸馏深度融合进单一解码器，为高效统一的多模态智能提供了新的范式。

### 多模态大模型的架构分化与统一困境

当前多模态大模型（MLLM）在架构设计上呈现出明显的分化态势。以 **Qwen2.5-VL** 为代表的编码器基模型依赖外部视觉编码器（如 InternViT）将图像转化为视觉 token 后再送入语言模型，在理解任务上表现出色，但无法原生支持图像生成。另一方面，**Emu3**、**Chameleon** 等统一模型试图通过外部视觉分词器（VQ-VAE tokenizer）将图像离散化为视觉 token，与文本 token 一同进行自回归建模，从而同时支持理解与生成。然而，这种“离散化桥接”策略引入了两个根本性瓶颈：

1. **推理延迟高**：外部视觉编码器和分词器构成独立的前处理模块，在理解任务中增加首 token 延迟（TTFT）；在生成任务中，离散 token 的解码与重建过程进一步拖慢端到端推理。
2. **跨模态信息融合受限**：视觉信息在进入语言模型之前已被压缩为离散码本索引或固定长度的连续表征，早期细粒度视觉特征难以被语言模型直接利用，限制了需要精细视觉理解的任务（如 OCR、图表问答）的性能上限。

### 纯解码器架构的关键挑战

一个直观的改进方向是彻底移除外部视觉编码器和分词器，让原始图像直接通过简单的 Patch Embedding 进入纯解码器 Transformer，实现真正的“编码器自由”架构。然而，这一路径面临两个核心难题：

- **视觉感知预训练缺失**：语言模型解码器本身不具备视觉感知能力，直接输入原始像素级 patch 会导致理解性能大幅下降。如何在保留语言模型预训练能力的前提下，高效注入视觉理解能力，是一个关键的迁移学习问题。
- **多模态任务的计算冲突**：理解任务需要连续、高保真的视觉表征，而生成任务需要离散、可量化的视觉 token 以支持自回归采样。两种任务对视觉表征的需求截然不同，在共享的 Transformer 层中直接混合处理会导致任务间干扰。

### OneCAT 的统一动机

OneCAT 的核心动机在于回答一个根本性问题：**能否在不依赖任何外部视觉编码器或分词器的前提下，用一个纯解码器 Transformer 同时达到有竞争力的多模态理解、图像生成和图像编辑性能？**

为此，OneCAT 提出了两个关键创新方向：
- **模态特定的混合专家（Modality-MoE）**：在解码器的前馈网络层引入文本、理解、生成三组专家，让不同模态的 token 路由到各自专用的计算路径，从结构上缓解任务冲突。
- **定制教师全层蒸馏**：通过训练一个定制的 MLLM 教师模型，将其所有 Transformer 层的隐藏状态作为监督信号蒸馏到纯解码器学生模型中，以弥补视觉感知预训练的不足。

此外，OneCAT 将视觉生成建模为“下一尺度预测”（Next-Scale Prediction），与文本的“下一 token 预测”统一在同一个自回归框架内，并通过 Scale-Aware Adapter（SAA）增强多尺度特征提取能力。这一设计使得模型能够在一个纯解码器架构内无缝切换于理解、生成与编辑三种模态任务之间，为统一多模态智能提供了新的架构范式。

## 核心方法与创新机理

OneCAT 的核心创新在于**彻底移除了传统多模态系统对外部视觉编码器和视觉分词器的依赖**，将多模态理解、生成与编辑统一到一个纯解码器自回归 Transformer 中。这一设计通过三个关键机制实现：

**1. 模态特异的混合专家（Modality-MoE）前馈网络**

传统统一模型通常共享同一个前馈网络（FFN）处理所有模态的 token，而 OneCAT 在解码器内部引入了三个专用 FFN 专家：
- **Text FFN**：处理纯文本 token，保持语言理解能力
- **Und. FFN**：处理连续视觉 token（理解任务的图像 patch 嵌入、编辑任务的参考图像 token）
- **Gen. FFN**：处理离散视觉 token（多尺度自回归生成）

共享的注意力层保证了跨模态信息融合，而模态特定的 FFN 专家则让不同任务的计算路径各司其职，避免了单一 FFN 在多任务间的表示冲突（Section 3.1）。

**2. 多尺度自回归视觉生成（Next-Scale Prediction + SAA）**

区别于扩散模型或基于 VQ-VAE 的离散 token 生成，OneCAT 将视觉生成统一为“下一个尺度预测”范式：模型按预定义的尺度调度表（Table 13），自回归地预测从低分辨率到高分辨率的离散视觉 token。配合 **Scale-Aware Adapter（SAA）**，每个尺度拥有独立的低秩适配参数，增强了多尺度特征提取能力。消融实验表明，移除 SAA 后 GenEval 从 81.2 降至 78.1，DPG-Bench 从 74.9 降至 74.0（Table 12），验证了 SAA 对多尺度生成的关键作用。

**3. 定制教师全层隐藏状态蒸馏**

纯解码器架构缺乏视觉感知预训练，OneCAT 采用了一种深度特征级蒸馏策略：先训练一个由 InternViT + Qwen2.5 LLM 通过两层 MLP 连接的定制教师模型，然后在 Stage-1 中将学生模型所有 Transformer 层的隐藏状态与教师对齐，损失函数为：

$$\mathcal{L}_{\mathrm{Distill}} = \sum_{n=1}^{N} \mathrm{MSE}(\mathbf{h}_S^{(n)}, \mathbf{h}_T^{(n)})$$

总理解损失为 NTP 交叉熵与蒸馏损失的加权和：

$$\mathcal{L}_{\mathrm{Und}} = \mathcal{L}_{\mathrm{NTP}} + \lambda \mathcal{L}_{\mathrm{Distill}}, \quad \lambda=0.02$$

消融实验证实：全层隐藏状态蒸馏（平均分 35.3）显著优于仅蒸馏视觉 token（34.8）和不用蒸馏（31.4），且定制教师优于直接使用 Qwen2.5-VL 教师（35.3 vs 33.7）（Tables 9, 10, 15）。

**与基线方法的本质差异**

| 设计维度 | 基线方法（如 Emu3, Chameleon） | OneCAT |
|---------|------------------------------|--------|
| 视觉编码器 | 外部 ViT（如 InternViT） | 无，直接 Patch Embedding |
| 视觉分词器 | 外部 VQ-VAE（推理时必需） | 推理时无需分词器，仅训练时用多尺度 VAE 监督 |
| FFN 专家 | 单一共享 FFN 或通用 MoE | 模态特异 MoE（Text/Und/Gen） |
| 视觉生成范式 | 扩散模型或独立 NSP 解码器 | LLM 内统一的 next-scale prediction + SAA |
| 知识蒸馏 | 无蒸馏或仅输出 logits 蒸馏 | 定制教师全层隐藏状态 MSE 蒸馏 |

这些设计使 OneCAT-3B 在推理效率上获得数量级优势：理解任务首 token 延迟较 Qwen2.5-VL-3B 降低 61%（0.225s vs 0.583s），文生图推理时间较 BAGEL 降低 89%（2.85s vs 26.29s），图像编辑推理时间降低 90%（4.61s vs 46.44s）（Table 8）。

OneCAT 采用纯解码器（decoder-only）自回归架构，在单一 Transformer 内统一多模态理解、图像生成与图像编辑，**推理时无需任何外部视觉编码器或视觉分词器**。其核心设计围绕三个关键模块展开：模态特定的混合专家（Modality-MoE）、多尺度自回归生成机制（Scale-Aware Adapter, SAA），以及定制教师驱动的全层隐藏状态蒸馏。

### 推理流水线

Figure 3 展示了 OneCAT 的统一推理流水线。原始图像通过 **Patch Embedding** 直接转化为连续视觉 token，与文本 token 一同送入解码器。解码器内部采用 **Modality-MoE** 结构：注意力层为所有 token 共享，而前馈网络（FFN）则由三个模态特定专家组成——**Text FFN** 处理纯文本 token、**Und. FFN** 处理连续视觉 token（用于理解或编辑中的参考图像）、**Gen. FFN** 处理离散视觉 token（用于生成）。这种设计使模型能根据 token 类型动态路由计算，实现模态特异的特征提取，同时保持架构的统一性。

![[assets/figures/papers/OneCat_2509.03498_092170b29c9d/figures/003_Figure_3.jpg]]
*Figure 3: Inference pipeline of OneCAT, a decoder-only autoregressive unified model that seamlessly supports multimodal understanding, image generation and image editing*

对于视觉生成，OneCAT 将图像建模为多尺度离散 token 序列，按尺度从低到高自回归预测（next-scale prediction）。每个尺度通过 **Scale-Aware Adapter (SAA)** 进行低秩适配，增强多尺度特征提取能力。生成的离散 token 最终由预训练的多尺度 VAE 解码器重建为图像，推理时无需 VAE 编码器。对于图像编辑，参考图像同样经 Patch Embedding 转化为连续 token，与文本指令和生成 token 在解码器内交互，实现统一的编辑流程。

### 训练管线

训练分为三个阶段（Figure 5）：

![[assets/figures/papers/OneCat_2509.03498_092170b29c9d/figures/005_Figure_4.jpg]]
*Figure 4: Multimodal versatile attention mechanism. T denotes the text tokens. U denotes the continuous visual tokens for multimodal understanding or reference image tokens for image editing. Gi denotes the i-th scale discrete visual tokens for visual generation. Figure 5 Overview of the training pipeline. In Stage 1, we first prepare a teacher model by training a two-layer MLP to connect InternViT [19] and the Qwen2.5 LLM [105]. This teacher model is then used to perform understanding distillation for the Und. FFN and the Patch Embedding layer. Simultaneously, we perform generation pretraining to optimize the Gen. FFN. All other parameters of the LLM remain frozen to preserve its pretrained language...*

- **Stage 1（多模态预训练）**：首先训练一个定制教师模型（InternViT + 两层 MLP + Qwen2.5 LLM），然后冻结 LLM 主体参数，仅训练 Patch Embedding、Und. FFN 和 Gen. FFN。理解任务通过全层隐藏状态蒸馏损失 $\mathcal{L}_{\mathrm{Distill}} = \sum_{n=1}^{N} \mathrm{MSE}(\mathbf{h}_S^{(n)}, \mathbf{h}_T^{(n)})$ 对齐学生与教师模型，生成任务则直接优化 Gen. FFN。
- **Stage 2（统一中段训练）**：解冻全部参数，进行大规模多任务联合训练，平衡文本、理解和生成三种 token 比例。
- **Stage 3（统一监督微调）**：在高质量指令数据上进行微调，支持原生分辨率策略，生成图像边长扩展至 288–1776 像素。

### 关键设计决策

1. **早期融合（Early Fusion）**：解码器直接处理原始视觉 token，而非在后期通过交叉注意力注入视觉信息。消融实验（Figure 10, Table 14）表明，早期融合在性能上与晚期融合相当，但计算效率更高，因为避免了额外的编码器前向传播。

2. **定制教师蒸馏**：直接使用现成的 Qwen2.5-VL 作为教师会导致训练不稳定，而专门训练的定制教师（InternViT + MLP + Qwen2.5）在隐藏状态蒸馏下表现更优（平均得分 35.3 vs 33.7，Table 10）。全层蒸馏优于仅蒸馏视觉 token（35.3 vs 34.8）和完全不用蒸馏（31.4，Tables 9, 15）。

3. **多尺度生成调度**：OneCAT 使用预定义的尺度调度表（Table 13），例如 1:1 宽高比下通过 $K=13$ 个尺度生成 $1024 \times 1024$ 图像，低分辨率图像可通过截断调度表实现（如 $K=10$ 生成 $512 \times 512$）。去除 SAA 会导致生成性能显著下降（GenEval: 81.2→78.1, DPG: 74.9→74.0, Table 12），验证了多尺度适配的关键作用。

4. **推理效率优势**：由于消除了外部视觉编码器和分词器，OneCAT-3B 在理解任务的首 token 延迟（TTFT）上比 Qwen2.5-VL-3B 降低 61%（0.225s vs 0.583s），在文生图推理速度上比混合架构 BAGEL 快约 10 倍（2.85s vs 26.29s），在图像编辑上快约 10 倍（4.61s vs 46.44s）（Table 8）。

### 推理流水线架构

OneCAT 采用纯解码器架构，推理时无需任何外部视觉编码器或视觉分词器。原始图像经过 **Patch Embedding** 直接转化为连续视觉 token，与文本 token 一并送入统一的 Transformer 解码器处理。该解码器内部嵌入了 **Modality-MoE（模态混合专家）** 机制，包含三个专门的前馈网络（FFN）专家：**Text FFN** 处理文本 token、**Und. FFN** 处理用于多模态理解的连续视觉 token、**Gen. FFN** 处理用于视觉生成的离散视觉 token。注意力层在三种模态间共享，但不同任务采用不同的注意力掩码模式（Figure 4）。

### 视觉生成：多尺度自回归与 SAA

视觉生成采用 **Next-Scale Prediction（下一尺度预测）** 范式，将图像生成建模为按尺度顺序的自回归过程。给定 $K$ 个尺度的离散 token 序列 $R_{1:K}$，其对数似然分解为：

$$\log p_{\theta}(R_{1:K}) = \sum_{k=1}^{K} \log p_{\theta}(R_k \mid R_{1:k-1})$$

模型从最低分辨率尺度开始，逐尺度预测更高分辨率的离散 token，直至达到目标分辨率。不同宽高比采用预定义的尺度调度表（Table 13），例如 $1024 \times 1024$ 图像使用 $K=13$ 个尺度。

为增强多尺度特征提取能力，OneCAT 在 Gen. FFN 中引入 **Scale-Aware Adapter (SAA)**，为每个生成尺度提供低秩适配模块。消融实验证实，移除 SAA 导致 GenEval 从 81.2 降至 78.1，DPG-Bench 从 74.9 降至 74.0（Table 12），证明 SAA 对多尺度生成的关键作用。

### 视觉理解：全层隐藏状态蒸馏

OneCAT 的视觉理解能力通过 **定制教师模型的全层隐藏状态蒸馏** 获得。教师模型由预训练的 InternViT 与 Qwen2.5 LLM 通过两层 MLP 连接器构建，仅在图像-文本描述数据上训练连接器。

蒸馏损失定义为学生与教师所有 $N$ 层 Transformer 隐藏状态的均方误差：

$$\mathcal{L}_{\mathrm{Distill}} = \sum_{n=1}^{N} \mathrm{MSE}(\mathbf{h}_S^{(n)}, \mathbf{h}_T^{(n)})$$

视觉理解总损失为下一 token 预测交叉熵与蒸馏损失的加权和：

$$\mathcal{L}_{\mathrm{Und}} = \mathcal{L}_{\mathrm{NTP}} + \lambda \mathcal{L}_{\mathrm{Distill}}$$

其中 $\lambda=0.02$。消融实验表明，全层隐藏状态蒸馏（平均分 35.3）显著优于无蒸馏（31.4）和仅蒸馏输出 logits（Table 9），且定制教师优于直接使用 Qwen2.5-VL 教师（35.3 vs 33.7，Table 10）。

### 离散视觉分词：二值球面量化

多尺度 VAE tokenizer 使用 **Binary Spherical Quantization (BSQ)** 将连续特征量化为离散码。对于 $d$ 维特征向量 $x_{ij}$，量化操作为：

$$\mathcal{Q}(x_{ij}) = \frac{1}{\sqrt{d}} \operatorname{sign}\left(\frac{x_{ij}}{\|x_{ij}\|_2}\right)$$

该量化器将特征映射到单位超球面上的二值顶点，用于训练阶段的多尺度视觉监督。推理时仅使用 VAE 解码器将生成的离散 token 重建为图像，无需编码器。

### Classifier-Free Guidance

文本到图像生成时，最终 logits 为文本条件 logits 与无条件 logits 的线性组合：

$$\mathsf{L}_{\mathrm{final}} = \lambda_t \cdot \mathsf{L}_t + (1-\lambda_t) \cdot \mathsf{L}_{\emptyset}$$

其中 $\lambda_t=20$。图像编辑采用双重引导机制，先混合文本-参考图 logits 与纯文本 logits，再与无条件 logits 结合：

$$\mathsf{L}_c = \frac{\mathsf{L}_{t,i} + \lambda_i \cdot \mathsf{L}_t}{1+\lambda_i}, \quad \mathsf{L}_{\mathrm{final}} = \mathsf{L}_{\emptyset} + \lambda_t \cdot (\mathsf{L}_c - \mathsf{L}_{\emptyset})$$

其中 $\lambda_i=1$，$\lambda_t=3$。CFG 略微增加推理开销，但对生成质量有显著贡献。

## 实验与关键发现

### 核心实验结果

#### 多模态理解

OneCAT-3B 在多个理解基准上显著超越同属统一模型的 **Emu3**（Table 3）：TextVQA 73.9 vs 64.7（+9.2），ChartQA 81.2 vs 68.6（+12.6），AI2D 77.8 vs 70.0（+7.8），且 OneCAT 的激活参数量更少。与基于编码器的 SOTA 模型 **Qwen2.5-VL-3B** 相比，OneCAT-3B 在 TextVQA（73.9 vs 79.3）和 GQA（63.1 vs 65.8）上仍存在差距，但在 ChartQA（81.2 vs 81.9）上基本持平，并在 MMBench（78.8 vs 79.6）和 MME-P（1630 vs 1642）上接近。这表明纯解码器架构在消除外部视觉编码器后，通过蒸馏策略已能逼近编码器基模型的性能，但视觉感知的预训练不足仍是瓶颈。

![[assets/figures/papers/OneCat_2509.03498_092170b29c9d/figures/008_Table_3.jpg]]
*Table 3: Performance comparison across multiple multimodal understanding benchmarks. Higher scores are better, as indicated by the up-arrow (↑). A-LLM denotes the number of activated LLM parameters, while Vis. indicates the parameter count of the vision encoder or tokenizer for multimodal understanding. Chameleon [88] does not report the parameter count of its vision tokenizer. slash (/) denotes that models do not require a vision encoder or tokenizer for multimodal understanding. Best in bold, second best is underlined (across unified models)*

#### 视觉生成

在文本到图像生成上，OneCAT-3B 在 GenEval 达到 0.90，在 DPG-Bench 达到 84.53（Tables 5, 6），在统一模型中取得新 SOTA，并大幅领先混合架构 **BAGEL**。定性对比（Figure 6）显示 OneCAT 在复杂场景构图和文本-图像对齐上优于 **Janus-Pro-7B** 和 **GPT-4o**。

![[assets/figures/papers/OneCat_2509.03498_092170b29c9d/figures/010_Figure_6.jpg]]
*Figure 6: Prompts BAGEL-7B GPT-40 Janus-Pro-7B OneCAT-3B Figure 6 Text-to-Image comparison*

#### 图像编辑

在 ImgEdit-Bench 上，OneCAT-3B 总体得分 3.43（Table 7），在物体移除、背景调整、颜色调整、主体替换和风格迁移等任务上表现均衡。Figure 2 的定性展示进一步验证了其在感知任务（深度估计、姿态估计、分割、边缘检测）上的泛化能力。

![[assets/figures/papers/OneCat_2509.03498_092170b29c9d/figures/014_Table_6.jpg]]
*Table 6: Performance comparison on the DPG-Bench [34] benchmark. Best in bold, second best is underlined. Table 7 Comprehensive comparison on ImgEdit-Bench [107] showing performance across nine editing categories. Higher scores are better for all metrics. Best in bold, second best is underlined*

#### 推理效率

在 NVIDIA H800 上，OneCAT-3B 的理解首 token 延迟（TTFT）在 1792×1792 分辨率下仅 0.225s，比 **Qwen2.5-VL-3B** 的 0.583s 降低 61%（Table 8 Left）。文生图推理时间仅 2.85s，比 **BAGEL** 的 26.29s 快约 10 倍；图像编辑推理时间 4.61s vs 46.44s，快约 10 倍（Table 8 Right）。效率优势源于消除了外部视觉编码器和分词器的推理开销。

### 消融与分析

#### Scale-Aware Adapter (SAA) 的关键作用

移除 SAA 后，GenEval 从 81.2 降至 78.1，DPG-Bench 从 74.9 降至 74.0（Table 12），证明多尺度适配器对视觉生成质量至关重要。SAA 为每个生成尺度提供低秩适配，增强了模型对不同分辨率特征的分辨能力。

#### 蒸馏策略的决定性影响

全层隐藏状态蒸馏（MSE loss 对齐所有 Transformer 层）显著优于无蒸馏（平均分 35.3 vs 31.4）和仅蒸馏视觉 token（35.3 vs 34.8）（Tables 9, 15）。仅蒸馏输出 logits 效果最差，表明深层特征对齐是弥补纯解码器视觉感知不足的核心机制。使用定制教师模型（通过 MLP 连接 InternViT 和 Qwen2.5 LLM 训练）比直接使用 **Qwen2.5-VL** 作为教师更稳定且得分更高（平均 35.3 vs 33.7）（Table 10），说明教师与学生的架构匹配度对蒸馏效果有显著影响。

#### 训练数据配比的影响

在 Stage-2 统一中训练中，增加视觉生成 token 比例（从 10B 提升至 45B）持续提升 GenEval 和 DPG-Bench 分数（Table 11），表明多尺度自回归生成需要大规模生成数据的支撑。文本、理解和生成三种 token 的比例需通过超参数搜索平衡，以兼顾各任务性能。

![[assets/figures/papers/OneCat_2509.03498_092170b29c9d/figures/019_Figure_8.jpg]]
*Figure 8: Comparision of different distillation strategies and teachers for stage-1 training. Table 11 Effect of trained token ratio across text-only (T), understanding (U), and generation (G)*

#### 早期融合 vs 晚期融合

在理解任务中，早期融合（解码器直接处理视觉 token）与晚期融合（先编码再融合）性能相当，但计算效率更高（Figure 10, Table 14）。这验证了 OneCAT 的 Patch Embedding + 模态 MoE 设计在消除外部编码器的同时保持了竞争力。

### 失败模式与局限

1. **理解性能差距**：尽管蒸馏策略有效，OneCAT 在部分基准（如 TextVQA、GQA）上仍落后于专用视觉编码器模型，纯解码器的视觉感知预训练不足是根本瓶颈，可能需要更大规模数据或更强的教师信号。
2. **生成依赖 CFG**：生成质量部分依赖 Classifier-Free Guidance（文生图 $\lambda_t=20$，编辑 $\lambda_t=3$），略微增加了推理开销，并可能限制输出的多样性。
3. **固定尺度调度**：多尺度生成依赖预定义的尺度调度表（Table 13），在极端宽高比下灵活性受限。
4. **训练复杂度高**：三阶段训练管线涉及定制教师训练、多模态数据配比和梯度累积策略，对计算资源和工程调优要求较高。

## 定位与知识库关联

### 1. 与基线工作的关系

OneCAT 的核心定位是**纯解码器自回归统一多模态模型**，其设计直接回应了现有多模态系统对“外部视觉编码器”和“外部视觉分词器”的双重依赖。以下从架构范式、生成机制和训练策略三个维度梳理其与代表性基线的差异。

#### 1.1 架构范式：从“编码器-解码器”到“纯解码器”

传统多模态理解系统普遍依赖外部视觉编码器（如 ViT）将图像压缩为视觉 token 后再送入 LLM。**Qwen2.5-VL** 是该范式的 SOTA 代表，但其推理时需额外运行 ViT 前向传播，导致首 token 延迟显著增加（Table 8 左栏：1792×1792 分辨率下 TTFT 为 0.583s，OneCAT-3B 仅需 0.225s，降幅 61%）。

**Mono-InternVL** 率先探索了“编码器自由”的多模态理解路径，直接让 LLM 处理原始图像 patch，但其仍局限于理解任务，且未涉及生成能力。OneCAT 在此基础上进一步扩展：不仅去除了视觉编码器，还通过模态特定的混合专家（Modality-MoE）在同一解码器内同时支持理解、生成与编辑三种任务模式。

在统一多模态模型阵营中，**Janus-Pro** 采用解耦视觉编码的设计，为理解和生成分别维护独立的视觉处理路径。相比之下，OneCAT 的纯解码器方案实现了更彻底的架构统一——所有视觉 token（连续的理解 token 与离散的生成 token）共享注意力层，仅在 FFN 层通过三个模态特定专家（Text FFN、Und. FFN、Gen. FFN）进行差异化计算。

#### 1.2 生成机制：从扩散/分词器到自回归多尺度预测

视觉生成方面，**BAGEL** 代表了“混合 MoT + 扩散”的路线，其文生图推理需 26.29s（1024×1024），而 OneCAT-3B 仅需 2.85s（Table 8 右栏），速度提升约 9 倍。这一效率优势源于 OneCAT 将视觉生成统一为“下一个尺度预测”（next-scale prediction），完全在 LLM 解码器内完成，无需外部扩散模型或专门的 NSP 解码器。

**Emu3** 和 **Chameleon** 采用基于 VQ-VAE 的离散 token 方案，将图像量化为离散码本索引后再进行自回归生成。OneCAT 的关键差异在于：推理时无需运行 VQ-VAE 编码器（仅训练时使用 multi-scale VAE 作为监督信号），图像直接通过 Patch Embedding 输入，生成的多尺度离散 token 最终由 VAE 解码器重建为图像。这消除了推理阶段的外部分词器瓶颈。

**Show-o2** 同样追求统一多模态能力，但其具体架构细节在论文中未充分展开对比。OneCAT 在 GenEval 基准上达到 0.90 的 Overall 分数，在 DPG-Bench 上达到 84.53（Tables 5, 6），论文声称这是统一模型中的新 SOTA。

#### 1.3 训练策略：定制教师蒸馏与多任务平衡

OneCAT 的训练流水线引入了一个关键创新：**定制 MLLM 教师的全层隐藏状态蒸馏**。具体做法是先用 InternViT + 两层 MLP + Qwen2.5 LLM 构建教师模型，然后通过 MSE 损失将学生模型所有 Transformer 层的隐藏状态与教师对齐：

$$\mathcal{L}_{\mathrm{Distill}} = \sum_{n=1}^{N} \mathrm{MSE}(\mathbf{h}_S^{(n)}, \mathbf{h}_T^{(n)})$$

消融实验（Tables 9, 10, 15）表明，这一策略显著优于无蒸馏（平均分 35.3 vs 31.4）和仅蒸馏输出 logits（平均分 35.3 vs 34.8），且定制教师优于直接使用 Qwen2.5-VL 教师（平均分 35.3 vs 33.7）。这揭示了纯解码器架构在缺乏视觉感知预训练的情况下，通过深层特征蒸馏可以有效弥补视觉理解能力的不足。

### 2. 适用边界与局限

尽管 OneCAT 在统一架构和推理效率上取得了显著突破，其当前版本存在以下明确局限：

1. **理解性能仍有差距**：在部分理解基准上，OneCAT-3B 仍落后于专用视觉编码器模型。例如 TextVQA 上 OneCAT-3B 得分 73.9，而 Qwen2.5-VL-3B 达 79.3（Table 3）。论文指出这可能需要更大规模的数据或更强的蒸馏策略来弥补，但当前实验尚未验证这些扩展方案的有效性。

2. **训练流水线复杂度高**：三阶段训练（定制教师训练 → 统一中训练 → 统一 SFT）涉及大规模数据配比、多任务 token 比例控制和 uneven gradient accumulation 等工程技巧，对计算资源和调参经验要求较高。Table 1 显示 Stage 1-2 的理解样本量达 436M，生成样本量 52M，训练规模本身构成了一定的复现门槛。

3. **多尺度生成的刚性调度**：视觉生成依赖预定义的尺度调度表（Table 13），对于 1:1 宽高比使用 K=13 个尺度生成 1024×1024 图像，低分辨率通过截断调度表实现。这种固定调度在极端宽高比下可能受限，论文未提供动态调度或分辨率自适应机制的探索。

4. **对 Classifier-Free Guidance 的依赖**：生成和编辑任务中使用了 CFG 来提升质量（文生图 λ_t=20，编辑 λ_i=1, λ_t=3），这略微增加了推理开销（需同时计算条件和无条件 logits），且可能影响生成多样性。论文未系统分析不同 CFG 强度对质量-多样性权衡的影响。

### 3. 开放问题

论文的实验分析和设计选择揭示了以下值得进一步探索的方向：

1. **规模扩展的可持续性**：OneCAT 目前验证了 1.5B 和 3B 两个参数规模。纯解码器架构能否高效扩展到更大参数量（如 >7B）并保持多任务平衡，是一个开放问题。Table 11 显示增加生成 token 比例（10B → 45B）持续提升 GenEval 和 DPG 分数，暗示数据规模的扩展仍有红利，但模型参数规模的影响尚未被研究。

2. **跨模态扩展潜力**：论文框架的核心思想——将模态特定 MoE 与自回归多尺度预测融入 LLM 解码器——理论上可扩展到视频、语音等其他模态。但当前实验仅限于图像和文本，多模态间的注意力交互机制（Figure 4）是否能在更多模态下保持高效，需要进一步验证。

3. **早期融合 vs 晚期融合的深层机制**：论文在 Figure 10 和 Table 14 中对比了早期融合（解码器直接处理视觉 token）与晚期融合（类似传统编码器-解码器架构），发现早期融合在计算效率上更优且性能相当。但这一结论是否在更大规模模型和数据下仍然成立，以及早期融合是否对特定类型的视觉理解任务存在隐性劣势，尚不明确。

4. **蒸馏策略的极限**：全层隐藏状态蒸馏被证明是关键有效的，但 Table 15 显示仅蒸馏视觉 token 的效果有限（平均分 34.8 vs 35.3 的完整蒸馏）。这是否意味着视觉理解和语言能力之间存在深层耦合，仅靠视觉侧的蒸馏无法完全弥补？更大规模蒸馏数据能否进一步缩小与编码器基模型的差距？这些问题有待后续工作回答。

5. **生成质量与推理速度的进一步权衡**：当前 CFG 策略和固定的尺度调度是生成质量的重要保障，但也构成了推理开销的下限。如何在不依赖 CFG 或减少尺度数量的前提下保持生成质量，是实现更高效推理的关键挑战。

## 原文 PDF

![[paperPDFs/arxiv_2025/OneCat.pdf]]
