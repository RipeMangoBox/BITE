---
title: "OmniZip: Learning a Unified and Lightweight Lossless Compressor for Multi-Modal Data"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/OmniZip_Learning_a_Unified_and_Lightweight_Lossless_Compressor_for_Multi_Modal_Data.pdf
project_link: null
code_link: "https://github.com/adminasmi/OmniZip-CVPR2026"
aliases:
- OmniZip
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 在轻量级 RWKV 骨干中引入模态路由的混合专家（MoE）机制，通过对自回归预测模型的关键模块进行稀疏门控，使得模型能够在推理速度和多种模态的压缩效果之间取得最佳平衡。
primary_logic: 通过可逆的统一分词和模态感知的稀疏专家路由，可以让一个小型预测模型同时高效地处理多种模态的统计特性，无需针对每种模态部署不同的压缩器。
claims:
- OmniZip 在 CLIC-M、TouchandGo、enwik9、LibriSpeech 和 WikiSQL 数据集上的压缩效率分别比 gzip 高 42%、57%、62%、42% 和 53%。
- OmniZip 在 MacBook CPU 和 iPhone NPU 上达到约 1MB/s 的推理速度。
- CLIC-M 上 bits/Byte = 2.378 (OmniZip-M) / 2.273 (OmniZip-L)
- TouchandGo 上 bits/Byte = 1.338 (S) / 1.110 (M) / 0.987 (L)
---

# OmniZip: Learning a Unified and Lightweight Lossless Compressor for Multi-Modal Data

> [!tip] 核心洞察
> 通过可逆的统一分词和模态感知的稀疏专家路由，可以让一个小型预测模型同时高效地处理多种模态的统计特性，无需针对每种模态部署不同的压缩器。

| 字段 | 内容 |
|------|------|
| 中文题名 | OmniZip：学习统一的轻量级多模态数据无损压缩器 |
| 英文题名 | OmniZip: Learning a Unified and Lightweight Lossless Compressor for Multi-Modal Data |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.22286) · [Code](https://github.com/adminasmi/OmniZip-CVPR2026) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | OmniZip |
| Dataset | CLIC-M, TouchandGo, enwik9, LibriSpeech |

> [!tip] 效果简介
> - CLIC-M 上，bits/Byte 2.378 (OmniZip-M) / 2.273 (OmniZip-L) vs 3.947 (gzip) (-40% (M) / -42% (L))。
> - TouchandGo 上，bits/Byte 1.338 (S) / 1.110 (M) / 0.987 (L) vs 2.298 (gzip) (-42% (S) / -52% (M) / -57% (L))。
> - enwik9 上，bits/Byte 1.370 (S) / 1.009 (M) / 0.980 (L) vs 2.590 (gzip) (-47% (S) / -61% (M) / -62% (L))。

## 概要

现实世界天然是多模态的——图像、文本、语音、基因序列等数据类型在统计特性上差异巨大。然而，现有无损压缩技术长期处于“分而治之”的状态：经典通用压缩器（如 gzip、zstd）在多模态场景下压缩效率有限，而专用压缩器（如 PNG、FLAC）或基于学习的方案（如 L3C、tszip）又仅针对单一模态设计，导致实际部署中需要维护多套压缩系统，软硬件成本高昂。近年来，基于大语言模型（LLM）的多模态压缩器（如 **P2LLM**、**Deletang et al.** 的 Llama3/RWKV 方案）虽展现出跨模态潜力，但其庞大的参数量和计算开销使得在边缘设备上实时运行几乎不可能。

**核心瓶颈**由此清晰浮现：多模态无损压缩亟需一种既能有效处理异构数据统计特性，又足够轻量、可在消费级设备上实时运行的方法。

OmniZip 正是针对这一瓶颈提出的统一轻量级方案。其核心洞察在于：通过**可逆的统一分词**与**模态感知的稀疏专家路由**，可以让一个小型预测模型同时高效地捕获多种模态的统计规律，而无需为每种模态部署独立压缩器。具体而言，该方法在轻量级 RWKV 骨干网络中引入模态路由的混合专家（MoE）机制——在自回归预测模型的关键模块（上下文建模和前馈网络）中施加稀疏门控，使模型在推理速度与多模态压缩效果之间取得最佳平衡。

在跨 7 个模态、16 个数据集的综合评测中，OmniZip 展现出显著优势：在 CLIC-M（图像）、TouchandGo（触觉）、enwik9（文本）、LibriSpeech（语音）和 WikiSQL（数据库）上，其压缩效率分别比 gzip 高出 42%、57%、62%、42% 和 53%。同时，OmniZip 在 MacBook CPU 和 iPhone NPU 上均可达到约 1MB/s 的推理速度，验证了其轻量级设计在边缘设备上的实用性。

**方法定位**：OmniZip 属于“学习型统一无损压缩器”这一新兴类别。与基于 LLM 的方案相比，它以数百倍小的模型规模实现了可竞争甚至更优的压缩效率；与经典通用压缩器相比，它在所有测试模态上均取得大幅领先。该方法在方法谱系中处于**轻量级自回归预测 + 稀疏模态路由**的交汇点，为多模态数据的高效统一压缩提供了新的技术路径。

### 多模态无损压缩的现实需求

现实世界的数据天然是多模态的——图像、文本、语音、基因序列、数据库记录等以不同统计特性共存。无损压缩作为信息存储与传输的基础技术，长期依赖针对单一模态设计的专用算法：**PNG**、**FLIF**、**JPEG-XL** 服务于图像，**FLAC** 服务于语音，**gzip**、**bzip2**、**zstd** 等通用工具虽能处理多种格式，却无法充分捕捉各模态的内在结构。这种“一种模态一个压缩器”的格局带来两个直接后果：软件栈的维护成本随模态数量线性增长，且边缘设备上部署多个压缩引擎会挤占本已紧张的存储与计算资源。

### 现有学习型方法的缺口

近年来，基于深度学习的无损压缩取得了显著进展。以 **L3C**、**DLPR** 为代表的图像压缩器，以及 **tszip** 等文本压缩器，在各自领域超越了传统算法。然而，这些方法仍遵循“单模态单模型”范式，缺乏跨模态的统一处理能力。另一条路线是借助大语言模型（LLM）的通用序列建模能力实现多模态压缩，如 **P2LLM** 和 **Deletang et al.** 基于 Llama3/RWKV 的工作。但这类方案的计算开销巨大——LLM 的参数量动辄数亿乃至数十亿，推理速度难以达到实时要求，在 MacBook CPU 或手机 NPU 等边缘平台上几乎不具备可用性。

### 核心瓶颈

上述现状揭示了一个清晰的瓶颈：**现有学习型无损压缩方法要么针对单一模态设计，需要部署多个压缩器，增加了软硬件成本；要么基于大语言模型，计算开销巨大，难以在边缘设备上实时运行。** 因此，多模态无损压缩急需一种既轻量又能有效处理异构数据的方法。

### 本文动机与核心思路

OmniZip 正是针对这一瓶颈而提出。其设计哲学是：**通过可逆的统一分词和模态感知的稀疏专家路由，让一个小型预测模型同时高效地处理多种模态的统计特性，无需针对每种模态部署不同的压缩器。** 具体而言，OmniZip 在轻量级 RWKV 骨干中引入模态路由的混合专家（MoE）机制，对自回归预测模型的关键模块进行稀疏门控，使模型在推理速度和多种模态的压缩效果之间取得最佳平衡。最终，OmniZip 在 CLIC-M、TouchandGo、enwik9、LibriSpeech 和 WikiSQL 等数据集上分别比 gzip 提高了 42%、57%、62%、42% 和 53% 的压缩效率，同时在 MacBook CPU 和 iPhone NPU 上达到约 1MB/s 的推理速度，验证了“轻量统一压缩”这一技术路线的可行性。

## 核心方法与创新机理

OmniZip 的核心创新在于通过**可逆的统一分词**与**模态感知的稀疏专家路由**，让一个小型预测模型（基于 RWKV 骨干）同时高效处理多种模态的统计特性，打破了现有学习型无损压缩器“一种模态一个模型”的范式。

### 关键瓶颈与因果杠杆

现有学习型无损压缩方法面临两难：单模态压缩器（如 **PNG**、**FLAC**、**L3C**）需要为每种数据类型部署独立模型，软硬件成本高；而基于大语言模型的多模态压缩器（如 **P2LLM**、**Deletang et al.** 的 Llama3/RWKV 方案）虽然覆盖多模态，但计算开销巨大，难以在边缘设备上实时运行。OmniZip 的因果杠杆在于：在轻量级 RWKV 骨干中引入模态路由的混合专家（MoE）机制，对自回归预测模型的关键模块进行稀疏门控，从而在推理速度和跨模态压缩效果之间取得最佳平衡。

### 相对于基线的三大 Changed Slots

**1. 分词策略：从单一模态分词到模态统一分词**

基线方法通常为不同模态采用独立的分词策略——文本用 BPE，图像用像素值，语音缺乏统一方案。OmniZip 将多模态数据可逆地映射到统一的令牌空间，并通过添加模态前缀和模态掩码来区分数据类型。具体而言，数据被归为三大类：图像类（自然图像、医学图像、触觉数据）、文本类（自然语言、基因序列、数据库）、语音类。对于图像类数据，每个像素通道被独立映射为 0–255 的整数令牌；文本类数据使用字节级别的令牌；语音数据则通过 8-bit 量化映射到统一空间。模态掩码 $M_{\mathrm{image}}$ 通过二元掩码限制输出概率只出现在对应模态的合法令牌上，进一步提升压缩效率。

**2. 上下文建模：从标准 Time Mixing 到模态路由 Time Mixing**

RWKV 的标准 Time Mixing 模块对所有输入令牌使用相同的变换。OmniZip 在 Time Mixing 的 V 投影上引入模态路由 MoE，而 K 和 R 层保持共享。路由器为每个令牌 $x_i$ 计算专家分数 $g_{i,e} = \mathrm{softmax}(x_i W_g)_e$，然后选取 top-k 专家进行加权：

$$\mathbf{V}(x_i) = \sum_{e \in \mathrm{top-}k} \hat{g}_{i,e} \cdot e(x_i)$$

这种设计使得不同模态的令牌在上下文建模时能够激活不同的专家子网络，而共享的 K/R 层保留了跨模态的通用时序建模能力。消融实验（Table 6）证实，仅在 V 层应用路由优于同时对 K/V 或 R/K/V 应用路由。

**3. 前馈模块：从标准 MLP 到模态路由 MoE 前馈**

OmniZip 将 RWKV 中的标准多层感知机替换为基于 MoE 的模态路由前馈模块。每个专家是一个小型 MLP，隐藏层因子设为 2×（原大 MLP 的一半），从而在引入模态特异性的同时控制计算量。该模块与上下文路由 MoE 协同工作，构成 Figure 3 所示的完整 OmniZip 块。

### 辅助创新：重参数化训练策略

除了上述三个核心 changed slots，OmniZip 还采用了重参数化训练策略：训练时在模型中添加额外分支以增强容量，推理时将这些分支合并回主结构，从而在不影响推理速度的前提下提升模型性能。这一策略贯穿于模型的多个组件中，是 OmniZip 在保持轻量化的同时获得高压缩效率的重要支撑。

### 训练目标设计

总损失函数包含三项：

$$\mathcal{L} = -\sum q \log p + \lambda \frac{1}{T} \sum_{j=1}^{T} \left( \log \sum_{t=1}^{N} e^{x_{i,t}} \right)^2 + \mu \left[ \mathbb{CV}^2 \left( \sum_{j=1,e} g_{i,e} \right) + \mathrm{CV}^2 \left( \sum_{\mathrm{load}} \mathbb{I}(g_{i,e} > 0) \right) \right]$$

第一项为标准交叉熵损失，驱动预测概率逼近真实分布；第二项 Z-loss 稳定路由器输出的数值范围；第三项负载均衡损失通过专家重要性的变异系数和令牌分配数量的变异系数，防止少数专家被过度使用。λ 和 μ 为超参数，平衡各项的贡献。

### 创新总结

OmniZip 的本质创新在于：将多模态无损压缩问题转化为“在统一令牌空间中进行模态感知的自回归预测”问题。通过模态路由 MoE 在上下文建模和前馈处理两个关键环节注入模态特异性，使得一个参数量仅为 4.8M–38M 的轻量模型（Table 2）能够在图像、文本、语音、基因序列、数据库等多种模态上同时超越专用压缩器和通用压缩器 gzip（压缩效率提升 30%–62%），并在 MacBook CPU 和 iPhone NPU 上达到约 1MB/s 的推理速度。

OmniZip 的整体设计遵循“统一分词 → 自回归概率预测 → 熵编码”的经典无损压缩范式，但其核心创新在于将这一流程从单一模态推广到多模态，并通过轻量级的混合专家（MoE）机制实现模态感知的建模。

### 三阶段压缩流水线

如 Figure 2 所示，OmniZip 的压缩流程由三个串联模块构成：

![[assets/figures/papers/paper_list_l906_https_arxiv_org_abs_2602_22286/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed OmniZip framework. Diverse data is first converted into a unified, fully reversible token space. A predictive model then estimates each token’s contextual probability, followed by arithmetic coding to generate the bitstream*

1.  **模态统一分词器**：将图像、文本、语音等异构数据可逆地映射到一个统一的令牌空间 $\{x_1, x_2, \dots, x_n\}$。该分词器按数据特性将输入归为三类——图像类、文本类和语音——并为每个令牌添加模态前缀和模态掩码，确保解码时能无损还原原始数据（Section 3.2）。
2.  **基于 RWKV 的预测模型**：以自回归方式估计每个令牌 $x_i$ 在给定上文 $\boldsymbol{x}_{<i}$ 时的条件概率分布 $p(x_i \mid \boldsymbol{x}_{<i})$。该模型以轻量级 RWKV-7 为骨干，并在其 Time Mixing 和前馈模块中引入模态路由 MoE，使模型能根据输入模态动态激活不同的专家子网络（Section 3.3 & 3.4）。
3.  **算术编码器**：根据预测模型输出的概率分布，对令牌序列进行熵编码，生成最终的压缩比特流。理论码长下界由熵 $H(p) = \mathbb{E}\left[\sum_{i=1}^n -\log_2 p(x_i \mid \boldsymbol{x}_{<i})\right]$ 给出（Section 3）。

### 核心设计决策

- **主干选择**：在文本压缩任务上对比了 Transformer、Mamba、RWKV-7 等架构后，RWKV-7 以 1.910 bits/Byte（0.2M 参数）和 2292 KB/s 的推理速度（MacBook CPU）在效率与速度之间取得最佳平衡（Table 1），因此被选为预测模型的骨干。
- **模态路由 MoE**：这是实现多模态统一建模的关键。OmniZip 在 RWKV-7 的 Time Mixing 模块中对 V 投影施加稀疏专家路由，同时在前馈模块中用 MoE 替代标准 MLP。路由器为每个令牌 $x_i$ 计算专家分数 $g_{i,e} = \mathrm{softmax}(x_i W_g)_e$，并仅激活 top-k 个专家，其输出加权求和为 $\mathbf{V}(x_i) = \sum_{e \in \mathrm{top-}k} \hat{g}_{i,e} \cdot e(x_i)$（Section 3.3）。这一设计使模型对图像类、文本类、语音类令牌自动激活不同的专家组合，无需手动切换压缩器。
- **训练策略**：采用重参数化训练，在训练时引入额外分支以增强模型容量，推理前将其合并，不增加推理开销（Section 3.1）。总损失函数 $\mathcal{L}$ 由交叉熵、Z-loss 和负载均衡损失三部分加权组成，以确保专家利用率均衡（Section 3.5）。

![[assets/figures/papers/paper_list_l906_https_arxiv_org_abs_2602_22286/figures/003_Table_1.jpg]]
*Table 1: Comparison for model backbone selection. Models are evaluated using text lossless compression. Inference speed is measured on the MacBook Pro CPU, with a batch size of 128*

### 模型变体

OmniZip 提供了 S（4.8M 参数，3.88M MACs）、M（38M 参数，18.2M MACs）和 L 三种规模（Table 2），以适配不同算力平台。在 MacBook CPU 和 iPhone NPU 上均可达到约 1 MB/s 的推理速度（Abstract），验证了其在边缘设备上的实用性。

OmniZip 的核心架构由三个紧密协同的模块构成：模态统一分词器、基于 RWKV 的预测模型（嵌入模态路由 MoE），以及算术编码器。其压缩目标是最小化实际码长与理论下界之间的差距，该下界由预测概率分布的熵给出。

### 3.1 无损压缩的形式化目标

给定输入序列 $\{x_1, x_2, ..., x_n\}$，预测模型输出每个令牌 $x_i$ 在上下文 $\boldsymbol{x}_{<i}$ 下的条件概率 $p(x_i | \boldsymbol{x}_{<i})$。算术编码器据此将序列编码为比特流，其期望码长的理论下界为交叉熵：

$$H(p) = \mathbb{E}\left( \sum_{i=1}^{n} -\log_2 p(x_i | \boldsymbol{x}_{<i}) \right)$$

该公式定义了无损压缩的终极优化目标：预测模型对下一个令牌的概率估计越准确，实际压缩码率越接近该熵界。

### 3.2 模态统一分词器

传统压缩器为不同模态设计独立的编码策略，而 OmniZip 将所有模态的数据可逆地映射到统一的令牌空间。具体而言，数据被归为三类——图像类、文本类和语音——每种模态通过专用的可逆变换产生令牌序列，并附加模态前缀以标识来源。在预测阶段，通过二元掩码 $M_{\text{image}}$ 将输出概率限制在当前模态的有效令牌子集上：

$$p_{\text{image}}(x_i | \boldsymbol{x}_{<i}) = \mathrm{softmax}\left( o(x_i | \boldsymbol{x}_{<i}) \odot M_{\text{image}} \right)$$

这一设计消除了跨模态的无效概率分配，直接提升压缩效率。

### 3.3 模态路由上下文学习

OmniZip 以轻量级 RWKV-7 为骨干，将其标准 Time Mixing 模块中的 V 投影替换为模态路由的混合专家（MoE）机制。对于输入令牌 $x_i$，可学习的路由器计算其分配给专家 $e$ 的分数：

$$g_{i,e} = \mathrm{softmax}(x_i W_g)_e = \frac{\exp(x_i W_{g,e})}{\sum_{e'=1}^{E} \exp(x_i W_{g,e'})}$$

选取 top-$k$ 个专家后，对路由分数重新归一化得到 $\hat{g}_{i,e}$，最终输出为选中专家输出的加权和：

$$\mathbf{V}(x_i) = \sum_{e \in \mathrm{top-}k} \hat{g}_{i,e} \cdot e(x_i)$$

K 和 R 层保持共享，不参与路由。这一稀疏激活设计使得不同模态的令牌在上下文建模时自然分流到不同专家，在保持模型总参数量可控的同时，每个令牌仅激活部分参数，从而实现模态感知的高效序列建模。

### 3.4 模态路由前馈模块

标准 RWKV 中的前馈网络（MLP）被替换为基于 MoE 的模态路由前馈模块。每个专家是一个小型 MLP，其隐藏层扩展因子为 2×，仅为原始大 MLP 的一半。路由机制与上下文学习模块一致，同样采用 top-$k$ 稀疏激活。该设计进一步增强了模型对不同模态非线性变换的适配能力。

### 3.5 训练损失函数

训练时的总损失函数由三部分组成：

$$\mathcal{L} = -\sum q \log p + \lambda \frac{1}{T} \sum_{j=1}^{T} \left( \log \sum_{t=1}^{N} e^{x_{i,t}} \right)^2 + \mu \left[ \mathbb{CV}^2 \left( \sum_{j=1,e} g_{i,e} \right) + \mathrm{CV}^2 \left( \sum_{\text{load}} \mathbb{I}(g_{i,e} > 0) \right) \right]$$

- 第一项为标准的交叉熵损失，驱动预测概率逼近真实分布。
- 第二项为 Z-loss，通过惩罚 log-sum-exp 的平方来稳定路由器输出的数值范围，防止 logits 漂移。
- 第三项为负载均衡损失，包含两部分：专家重要度（路由分数之和）的变异系数平方 $\mathbb{CV}^2$，以及令牌分配计数（路由分数大于零的指示函数之和）的变异系数平方。该项鼓励路由器均匀利用所有专家，避免少数专家过载而其余闲置。

此外，OmniZip 采用重参数化训练策略：训练时在模型中增加额外分支以提升容量，推理前将这些分支合并回主干，从而在不增加推理开销的前提下提升模型性能。

## 实验与关键发现

### 核心性能：多模态压缩效率

OmniZip 在图像、文本、语音等 7 种模态的 16 个数据集上进行了全面评估。与通用压缩器 **gzip** 相比，OmniZip 在所有模态上均实现了显著提升：在自然图像数据集 CLIC-M 上，OmniZip-L 达到 2.273 bits/Byte，较 gzip 的 3.947 bits/Byte 降低 42%；在触觉图像数据集 TouchandGo 上，OmniZip-L 达到 0.987 bits/Byte，降幅达 57%；在文本数据集 enwik9 上，OmniZip-L 达到 0.980 bits/Byte，降幅达 62%；在语音数据集 LibriSpeech 上，OmniZip-L 达到 3.810 bits/Byte，降幅达 42%；在数据库数据集 WikiSQL 上，OmniZip-L 达到 0.787 bits/Byte，降幅达 53%（Table 3、Table 4）。

在图像类数据集上，OmniZip-S（4.8M 参数）即已超越 gzip 约 30%，例如在 Kodak 上达到 3.307 bits/Byte（gzip 为 4.349 bits/Byte），在 TouchandGo 上达到 1.338 bits/Byte（gzip 为 2.298 bits/Byte）。随着模型规模增大，OmniZip-M 和 OmniZip-L 进一步拉大与经典压缩器的差距，并在多数数据集上接近或超越专用压缩器如 **PNG**、**FLIF**、**JPEG-XL** 以及基于学习的压缩器 **L3C**、**DLPR** 等（Table 3）。

### 模型规模与效率权衡

Figure 4 展示了基于学习的多模态压缩器在模型参数量与压缩效率之间的权衡关系。OmniZip 系列模型（S/M/L）位于左下角区域，表明其在较小参数量下即可获得较低的 bits/Byte。相比之下，基于大语言模型的方法（如 **P2LLM**、**Deletang et al.** 的 Llama3 变体）虽然在某些模态上压缩率更优，但参数量通常高出数个数量级，难以部署在边缘设备上。

![[assets/figures/papers/paper_list_l906_https_arxiv_org_abs_2602_22286/figures/008_Figure_4.jpg]]
*Figure 4: Comparison of learning-based lossless compressors across multi-modal datasets. The x-axis shows the model size (in millions of parameters), and the y-axis indicates compression efficiency (bits/Byte, lower is better). Models closer to the lower-left corner achieve better compression with fewer parameters. The dashed orange line represents the performance baseline of gzip*

### 推理速度与跨平台部署

OmniZip 的轻量化设计使其在多种硬件平台上均可达到实用级别的推理速度。在 MacBook Pro CPU 上，OmniZip-S 的压缩速度约为 1 MB/s 量级；在 iPhone 17 Pro 的 NPU 上同样达到约 1 MB/s；在 NVIDIA A100 GPU 上则可通过批处理进一步提升吞吐量（Figure 5）。具体而言，Table 1 显示 RWKV-7 骨干网络（0.2M 参数）在 MacBook CPU 上可达 2292 KB/s，而 3.2M 参数版本为 856 KB/s，验证了 RWKV 架构在轻量级自回归建模中的速度优势。

### 消融实验

#### 核心组件消融

Table 5 对 OmniZip 的四个关键设计进行了消融：模态统一分词、模态路由上下文学习、模态路由前馈网络、重参数化训练策略。依次移除各组件后，各模态代表数据集上的压缩性能均出现明显下降，验证了每个组件的必要性。其中，模态路由机制（包括上下文路由和前馈路由）的移除导致性能退化最为显著，表明模态感知的稀疏专家分配是实现多模态统一压缩的核心。

![[assets/figures/papers/paper_list_l906_https_arxiv_org_abs_2602_22286/figures/011_Table_5.jpg]]
*Table 5: Ablations on all our proposals: modality-unified tokenization, modality-routing contextual learning, modality-routing feedforward, and reparameterization training. Compression performance (bits/Byte) is evaluated on representative dataset from each modality, and the inference speed is measured on a MacBook CPU with a batch size of 128. The chosen configuration is colored in orange*

#### 上下文路由策略消融

Table 6 对比了在 Time Mixing 模块中对不同投影层应用路由的效果。实验表明，仅在 V 投影上应用路由（同时保持 K 和 R 层共享）可获得最优的压缩性能与参数效率平衡。同时对 K/V 或 R/K/V 应用路由反而导致性能下降，可能源于过度的稀疏化破坏了 RWKV 原有的时序建模能力。

![[assets/figures/papers/paper_list_l906_https_arxiv_org_abs_2602_22286/figures/012_Table_6.jpg]]
*Table 6: Ablations on modality-routing contextual learning. Routing is applied to all blocks with 4 experts and top-k=2. We report the total parameters and parameters activated per token. Compression performance (bits/Byte) is evaluated on representative dataset from each modality, and the inference speed is measured on a MacBook CPU with a batch size of 128. The chosen configuration is colored in orange*

#### 路由配置消融

Table 7 探索了路由模块的配置参数，包括路由应用的层数、专家数量和 top-k 值。结果表明，适度的专家数量（如 4 个专家，top-k=2）在压缩性能和推理速度之间取得了最佳平衡。过多的专家或过大的 top-k 会增加每令牌的激活参数量，拖慢推理速度，而压缩收益边际递减。

![[assets/figures/papers/paper_list_l906_https_arxiv_org_abs_2602_22286/figures/013_Table_7.jpg]]
*Table 7: Ablations on the configurations of the two modality-routing modules (e.g., routed blocks, expert count, top-k). We report the total parameters and parameters activated per token. Compression performance (bits/Byte) is evaluated on representative dataset from each modality, and the inference speed is measured on a MacBook CPU with a batch size of 128. The chosen configuration is colored in orange*

### 专家利用率分析

Figure 6 展示了 OmniZip-S 在不同模态下各层路由模块的专家使用分布。结果显示，不同模态在上下文学习模块和前馈模块中呈现出差异化的专家偏好模式：例如图像类数据倾向于激活某些特定专家，而文本类数据则偏好另一些专家。这种模态特异的专家利用模式验证了模态路由 MoE 机制的有效性——路由器确实学会了根据输入模态动态分配计算资源，而非退化为均匀使用所有专家。

### 调整后的压缩性能

考虑到部分对比方法（尤其是基于大语言模型的方法）模型规模远大于 OmniZip，Table 9 和 Table 10 提供了计入模型存储开销后的调整压缩性能。即使在此公平比较下，OmniZip 仍展现出竞争力，进一步验证了轻量级设计在多模态无损压缩场景中的实用价值。

### 实验注意事项

需要指出，论文中的主要结果以 bits/Byte 单次报告，未提供多次运行的置信区间或标准差，统计显著性无法直接判断。部分基线结果由作者复现（以 † 标记），可能存在实现差异带来的偏差。此外，推理速度测量虽覆盖多种硬件，但未提供详细的功率或能耗分析，实际部署的总成本评估需进一步验证。

## 定位与知识库关联

### 1. 方法沿革与基线关系

OmniZip 处于**轻量级学习型无损压缩**与**多模态统一建模**的交叉点。其核心竞争对象可分为三类：

**经典通用压缩器**（gzip、bzip2、zstd）：这类方法依赖手工设计的统计模型（如 LZ77/LZ78、Burrows-Wheeler 变换），无需训练即可跨模态工作，但缺乏对数据语义的深层理解。OmniZip 在全部测试模态上均显著超越 gzip（压缩效率提升 30%–62%），证明学习型方法在统一框架下可获得跨模态的统计建模优势。

**模态专用学习型压缩器**：图像领域有 **DLPR**、**L3C** 等基于像素概率建模的方法，以及 **P2LLM** 等基于大语言模型（LLM）的图像压缩器；文本领域有 **tszip**；语音领域有 **FLAC**。这些方法在各自模态上表现优异，但需为每种模态部署独立模型，增加了软硬件维护成本。OmniZip 以单一模型覆盖 7 种模态，在多数基准上与专用方法持平或更优（如 TouchandGo 上 OmniZip-M 的 1.110 bits/Byte 优于多数专用图像压缩器），同时避免了多模型部署的复杂性。

**基于 LLM 的多模态压缩器**：**Deletang et al.** 探索了 Llama3、RWKV 等预训练大模型在跨模态压缩中的潜力。这类方法虽具备强大的上下文建模能力，但参数量动辄数十亿，推理速度难以满足边缘设备实时需求。OmniZip 的关键区分点在于：以轻量级 RWKV-7 为骨干（最小变体仅 4.8M 参数），通过**模态路由混合专家（MoE）机制**在保持小模型体积的同时获得跨模态建模能力，在 MacBook CPU 和 iPhone NPU 上达到约 1 MB/s 的推理速度，填补了“轻量”与“多模态”之间的空白。

### 2. 核心机制与知识贡献

OmniZip 的方法论贡献可解构为三个相互耦合的模块：

1. **模态统一分词器（Modality-Unified Tokenizer）**：将图像类、文本类、语音三类数据可逆映射到统一令牌空间，通过模态前缀和模态掩码（$p_{\text{image}}(x_i|\boldsymbol{x}_{<i}) = \mathrm{softmax}(o(x_i|\boldsymbol{x}_{<i}) \odot M_{\text{image}})$）限制输出分布范围，在保证无损可逆的前提下提升编码效率。这是多模态统一压缩的基础设施。

2. **模态路由上下文学习（Modality-Routing Contextual Learning）**：在 RWKV-7 的 Time Mixing 模块中对 V 投影施加 MoE 路由（$\mathbf{V}(x_i) = \sum_{e \in \text{top-}k} \hat{g}_{i,e} \cdot e(x_i)$），K 和 R 层保持共享。消融实验（Table 6）表明，仅对 V 层路由优于同时对 K/V 或 R/K/V 路由，说明在保持核心时序建模共享的同时，仅在值投影上引入模态特异性即可获得最佳压缩性能。

3. **模态路由前馈模块（Modality-Routing Feedforward）**：将标准 MLP 替换为 MoE 结构，每个专家为隐藏因子 2× 的小型 MLP（原始大 MLP 的一半），通过稀疏激活控制每令牌计算量。

训练阶段采用重参数化策略（Figure 8），在训练时增加额外分支以提升模型容量，推理时合并分支以保持速度。总损失函数 $\mathcal{L}$ 包含交叉熵、Z-loss 和负载均衡损失（专家重要性的 $\mathbb{CV}^2$ 与令牌分配的 $\mathrm{CV}^2$），确保专家利用的均衡性。

### 3. 适用边界与局限

**已验证的适用范围**：OmniZip 在 7 种模态（自然图像、医学图像、触觉数据、自然文本、基因序列、数据库、语音）的 16 个数据集上得到验证，覆盖了从视觉到结构化数据的典型场景。

**已知局限**：
- 论文未讨论在**视频、3D 点云等时序/空间密集模态**上的泛化能力，这些模态的统计特性与现有三类分组存在本质差异。
- 模态分组依赖**预定义的三大类别**，对于完全未见的新模态（如高光谱图像、分子图），路由机制能否自适应扩展尚未验证。
- 实验未提供**多次运行的置信区间或标准差**，部分基线结果由作者复现（†标记），存在实现偏差风险。
- 未涉及**隐私保护或安全压缩**（如对抗样本鲁棒性）的讨论。
- 训练数据规模有限，未在更大语料（如全量 Wikipedia）上验证扩展性。

**开放问题**：
- 能否设计**动态模态发现机制**，使模型在推理时自动识别并适应新模态，而无需重新训练？
- 在**更严格的嵌入式约束**（如 MCU 级设备，内存 < 1MB）下，当前 MoE 路由的开销是否仍可接受？
- 模态路由的专家专业化现象（Figure 6 显示不同模态确实激活不同专家）是否暗示可以**按需卸载**非活跃专家以进一步压缩模型体积？

## 原文 PDF

![[paperPDFs/CVPR_2026/OmniZip_Learning_a_Unified_and_Lightweight_Lossless_Compressor_for_Multi_Modal_Data.pdf]]
