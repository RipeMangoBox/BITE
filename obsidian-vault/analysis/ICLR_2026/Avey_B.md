---
title: Avey-B
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Avey_B.pdf
project_link: null
code_link: null
aliases:
- AB
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "用双向注意力无关的分片检索和神经压缩替代Transformer自注意力编码。"
primary_logic: "Avey-B把长序列切成分片，用ranker检索相关分片，经神经压缩器和解耦静态动态处理器建模上下文。"
claims:
- "解耦静态和动态参数化避免了Avey原耦合相似度权重的反转效应。"
- "行求和归一化稳定动态层的余弦相似度混合并提升下游表现。"
- "神经压缩模块把目标分片和top-k检索分片压回固定长度，大幅提高吞吐量。"
- "Avey-B在句子分类、token分类、问答和检索任务上超过多个Transformer编码器基线。"
---

# Avey-B

> [!tip] 核心洞察
> 通过将序列划分为固定大小的分片（split），利用排序器（ranker）检索最相关的k个分片，再通过神经处理器（neural processor）进行上下文建模，使得计算复杂度与序列长度N呈线性关系（O(N)），而非二次关系。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Avey-B：面向编码器架构的双向注意力无关模型 |
| 英文题名 | Avey-B |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=kQ9j5RY8ff) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Avey-B |
| Dataset | SC（句子分类）, TC（token分类）, QA（问答）, IR（信息检索） |

> [!tip] 效果简介
> - SC（句子分类） 上，平均准确率 为 88.78（base），对比 87.14（BERT base），变化 +1.64。
> - TC（token分类） 上，平均F1 为 93.59（base），对比 89.82（BERT base），变化 +3.77。
> - QA（问答） 上，平均F1 为 62.45（base），对比 57.65（BERT base），变化 +4.80。

## 概要

Avey-B 是一种面向编码器（encoder-only）架构的双向注意力无关模型，由 Hammoud & Acharya 在 Avey（Hammoud & Acharya, 2025）自回归架构的基础上改造而来。该模型通过解耦静态与动态参数化、引入行归一化相似度分数以及神经压缩模块，在保持线性计算复杂度的同时，在句子分类、token分类、问答和信息检索等判别式任务上持续超越 BERT、RoBERTa、ModernBERT 和 NeoBERT 等 Transformer 基线模型。实验表明，Avey-B 在序列长度 N=96K 时吞吐量比 ModernBERT 快 3.38 倍，比 NeoBERT 快 11.63 倍，且其吞吐量衰减指数 α≈0.44，远小于 ModernBERT 的 α≈0.77 和 NeoBERT 的 α≈0.81。



Transformer 编码器的自注意力机制在序列长度上具有二次时间与内存复杂度，严重限制了长上下文场景下的实际部署效率。尽管 ModernBERT（Warner et al., 2025）通过 RoPE、FlashAttention（Dao et al., 2022）和交替全局/局部注意力等技术提升了效率，NeoBERT（Breton et al., 2025）通过深度-宽度重平衡优化了架构，但这些模型仍然受限于自注意力的二次复杂度，在超长序列（如 96K token）上难以高效运行。

Avey（Hammoud & Acharya, 2025）提出了一种注意力无关的自回归架构，通过排序器（ranker）检索最相关的分片（split）并使用神经处理器（neural processor）进行上下文建模，实现了线性复杂度。然而，Avey 的原始设计存在三个关键问题：(1) 静态权重与输入相关的余弦相似度逐元素相乘的耦合参数化方式会导致反转效应（inversion effects），即与当前 token 高度相似的 token 反而贡献更少；(2) 缺乏稳定的归一化机制；(3) 仅支持单向（自回归）上下文。Avey-B 针对这些问题进行了系统性改进。



## 核心方法与创新机理

Avey-B 的核心创新包括以下三点：

1. **解耦静态与动态参数化（Decoupled Static/Dynamic Parameterization）**：将 Avey 中耦合的静态权重与输入相关相似度解耦为交替的静态层和动态层。静态层仅使用学习到的线性变换，动态层仅使用余弦相似度，避免了耦合参数化中的反转效应和表示冗余。

2. **行求和归一化（Row-wise Sum Normalization）**：在动态层中，将每个位置的余弦相似度分数除以该位置所有分数的总和（divide-by-sum），稳定训练并持续提升下游任务性能。

3. **神经压缩模块（Neural Compression Module）**：在排序器中引入可学习的线性投影，将目标分片与其 top-k 检索分片拼接后的 (k+1)S 个 token 压缩回 S 个 token，在几乎不损失效果的前提下大幅提升吞吐量（4.37×）。

此外，Avey-B 移除了 Avey 上下文器中的自回归掩码，允许每个 token 同时关注左右上下文，实现双向编码。



![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_kQ9j5RY8ff_Avey-B/figures/001_Figure_1.jpg]]
*Figure 1: (a) Avey’s Coupled Parametrization (b) Avey-B’s Decoupled Parametrization Figure 1: A simple illustration of coupled (a) and decoupled (b) parameterizations ( e _ { i } = embedding i; s _ { i j } = cosine similarity score between e _ { i } and e _ { j } ; ni = neuron i , n _ { i } ^ { ( d ) } = neuron i in dynamic layer d ; n _ { i } ^ { ( s ) } = neuron i in static layer s; and w _ { i j } = weight corresponding to e _ { i } or n _ { i } ^ { ( d ) } used in the weighted sum of n _ { j } or n _ { j } ^ { ( s ) } , respectively).*

Avey-B 的整体框架由以下模块组成：

1. **排序器（Ranker）**：将输入序列划分为等长分片（split），每个分片包含 S 个 token。使用 MaxSim 算子（Khattab & Zaharia, 2020）计算每个目标分片与所有其他分片的相关性，选择 top-k 个最相关分片，并通过行归一化分数加权后拼接。

2. **神经压缩器（Neural Compressor）**：将目标分片与其 top-k 检索分片拼接后的 (k+1)S 个 token 通过可学习线性投影压缩回 S 个 token，并添加残差连接以提升稳定性。

3. **神经处理器（Neural Processor）**：对每个压缩后的分片进行多层处理，每层包含三个子模块：
   - **增强器（Enricher）**：逐位置神经网络，将 token 嵌入从 d 维扩展到 m 维，并分为头部（bypass 到融合器）和尾部（送入上下文器）。
   - **上下文器（Contextualizer）**：嵌入级神经网络，在动态层中使用余弦相似度实现 token 间交互，在静态层中使用学习到的线性变换。
   - **融合器（Fuser）**：将 bypassed 的头部特征与上下文化后的尾部特征拼接，投影回模型嵌入维度 d。



### 5.1 增强器变换

增强器是一个逐位置神经网络，将输入嵌入 X 从 d 维扩展到 m 维：

$$ \mathbf{Z} = \sigma(\mathbf{XU} + \mathbf{b}) \quad \text{(Equation 1)} $$

其中 σ 为激活函数（ReLU2），U 为可学习投影矩阵。

### 5.2 Avey 上下文器（耦合参数化）

Avey 的原始上下文器将学习到的交叉嵌入矩阵 V 与输入相关的余弦相似度矩阵逐元素相乘：

$$ \mathbf{c}(\mathbf{Z}_t) := \mathbf{Z}_{tl} \odot \sigma\Big( (\mathbf{V} \odot \mathcal{N}(\mathbf{Z}_{tr}) \mathcal{N}(\mathbf{Z}_{tr})^{\top}) \mathbf{Z}_{tr} + \mathbf{b}' \Big) \quad \text{(Equation 2)} $$

这种耦合方式会导致反转效应：当某个 token 与当前 token 高度相似时，其对应的权重可能被强制降低。

### 5.3 Avey-B 解耦参数化

Avey-B 将静态和动态计算解耦为交替的层：

**静态层**：仅使用学习到的交叉嵌入矩阵 V 进行线性变换：

$$ \mathbf{c}_{\mathrm{static}}(\mathbf{Z}) = \sigma(\mathbf{V} \mathbf{Z}_{\mathrm{tr}} + \mathbf{b}^{(s)}) \quad \text{(Section 4.2)} $$

**动态层**：从右半部分嵌入计算余弦相似度矩阵：

$$ \mathbf{S} = \mathcal{N}(\mathbf{Z}_{\mathrm{tr}}) \mathcal{N}(\mathbf{Z}_{\mathrm{tr}})^{\top} \quad \text{(Section 4.2)} $$

**行求和归一化**：将相似度矩阵的每一行归一化，使行内元素之和 ≤ 1：

$$ \widetilde{\mathbf{S}}_{i,j} = \frac{\mathbf{S}_{i,j}}{\sum_{j=1}^{C} \mathbf{S}_{i,j} + \varepsilon} \quad \text{(Section 4.2)} $$

**动态层输出**：使用行随机相似度矩阵混合嵌入：

$$ \mathbf{c}_{\mathrm{dyn}}(\mathbf{Z}) = \sigma(\widetilde{\mathbf{S}} \mathbf{Z}_{\mathrm{tr}} + \mathbf{b}^{(d)}) \quad \text{(Section 4.2)} $$

### 5.4 融合器输出

将 bypassed 头部 Z_h 与上下文化尾部 c(Z_t) 拼接，通过可学习投影矩阵 O 投影回嵌入维度 d：

$$ f(\mathbf{Z}) = [\mathbf{Z}_h \parallel \mathbf{c}(\mathbf{Z}_t)] \mathbf{O} \quad \text{(Equation 3)} $$

### 5.5 神经压缩器

通过可学习矩阵 P 将拼接后的 (k+1)S 个 token 线性压缩为 S 个 token：

$$ \widehat{\mathbf{X}} = \mathbf{P} \mathbf{X}_{\mathrm{cat}} \quad \text{(Equation 8)} $$

### 5.6 复杂度分析

Avey-B 的神经处理器计算复杂度与序列长度 N 呈线性关系：总处理成本为 (N/S) × S² = NS = O(N)。然而，排序器需要计算所有分片对之间的 MaxSim 分数，渐近复杂度仍为 O(N² d)。



## 实验与关键发现

### 6.1 主要效果结果

Avey-B 在 FineWeb 300BT 子集上预训练了 180B token（约为 ModernBERT 的 1/11），在多个基准上取得了显著提升：

| 基准 | 指标 | Avey-B base | BERT base | ModernBERT base | NeoBERT medium |
|------|------|-------------|-----------|-----------------|----------------|
| SC（句子分类） | 平均准确率 | 88.78 | 87.14 | - | 85.36 |
| TC（token分类） | 平均 F1 | 93.59 | 89.82 | 92.78 | 88.20 |
| QA（问答） | 平均 F1 | 62.45 | 57.65 | - | 55.67 |
| IR（信息检索） | 平均 NDCG@10 | 78.53 | 73.08 | 72.54 | 56.72 |

*Table 2: Effectiveness results for several encoders at different scales (M = Medium).*


![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_kQ9j5RY8ff_Avey-B/figures/003_Table_2.jpg]]
*Table 2: Effectiveness results for several encoders at different scales (M = Medium).*

Avey-B base 在 TC 和 IR 上甚至超过了所有大型 Transformer 编码器（如 ModernBERT large、RoBERTa large）。

### 6.2 长上下文鲁棒性

在 NIAH-1（Needle-in-a-Haystack）基准上，Avey-B 从 1k 到 96k token 保持近恒定准确率，仅下降 3-4 个百分点：

| 模型 | 1k | 4k | 8k | 16k | 32k | 64k | 96k |
|------|----|----|----|-----|-----|-----|-----|
| Avey-B base | 79.41 | 79.41 | 79.41 | 79.41 | 79.41 | 79.41 | 75.72 |
| Avey-B large | 79.69 | 79.69 | 79.69 | 79.69 | 79.69 | 79.69 | 76.06 |
| ModernBERT base | 67.74 | 70.67 | 70.67 | OOM | OOM | OOM | OOM |
| NeoBERT medium | 79.65 | 74.73 | OOM | OOM | OOM | OOM | OOM |

*Table 14: Needle-in-a-haystack (NIAH-1) accuracy across sequence lengths from 1k to 96k for several encoders at different scales (M = Medium; OOM = Out-of-Memory).*

### 6.3 吞吐量与延迟

Avey-B 在吞吐量衰减方面表现出显著优势：

- **吞吐量幂律衰减模型**：$T(N) \propto N^{-\alpha}$
  - Avey-B-torch-compile: α ≈ 0.44
  - ModernBERT-sys-optimized: α ≈ 0.77
  - NeoBERT-sys-optimized: α ≈ 0.81

- **延迟幂律模型**：$L(N) \propto N^{\beta}$
  - Avey-B-torch-compile: β ≈ 0.68
  - ModernBERT-sys-optimized: β ≈ 1.17
  - NeoBERT-sys-optimized: β ≈ 1.20

在 N=96K 时，Avey-B 的吞吐量比 ModernBERT 快 3.38 倍，比 NeoBERT 快 11.63 倍。

### 6.4 消融研究

| 消融设置 | SC Δ | TC Δ | QA Δ | IR Δ |
|----------|------|------|------|------|
| 移除行归一化 | -3.55% | -0.87% | -7.65% | -15.33% |
| 移除解耦参数化 | -1.43% | -2.12% | -2.53% | -7.40% |
| 移除神经压缩器 | +0.23% | +0.14% | -2.68% | -1.56% |
| 移除残差连接 | -3.38% (平均) | - | - | - |
| 完全移除排序器 | -7.46% (平均) | - | - | - |

*Table 10: Ablations of Avey-B, removing one component at a time while holding all others fixed.*

关键发现：
- 行归一化对 IR 和 QA 至关重要，移除后分别下降 15.33% 和 7.65%。
- 解耦参数化在所有任务上均带来提升，IR 提升最大（7.40%）。
- 神经压缩器在 QA 和 IR 上带来提升，但在 SC 和 TC 上有轻微下降（约 0.2%）。
- 排序器是核心组件，完全移除导致平均下降 7.46%。

### 6.5 设计选择分析

- **排序器方向**：单向排序器在 SC、TC、QA、IR 上均持续优于双向排序器，QA F1 从 51.07 降至 36.51（Δ=-14.56）。
- **层排列模式**：交错 S→D→... 模式在 SC、TC、QA 上取得最强平均性能。
- **归一化方案**：除求和归一化（divide-by-sum）在 SC、TC、QA 上优于 softmax、scaled softmax 和 RMS norm。
- **最优超参数**：N=2048, S=256, k=3, 掩码率 20%。

### 6.6 公平性说明

- Avey-B 在 FineWeb 300BT 子集上预训练了 180B token，而 ModernBERT 在数万亿 token 上预训练，Avey-B 的预训练数据量约为 ModernBERT 的 1/11。
- Avey-B base（165M 参数）在 TC 和 IR 上甚至超过了所有大型 Transformer 编码器。
- NeoBERT medium（约 250M 参数）是唯一公开可用的 NeoBERT 版本，与 Avey-B base（165M）和 large（391M）比较时规模不匹配。
- 所有模型在 10 个随机种子上报告中位数分数，Avey-B 的跨种子标准差通常低于 1.06（large），表明结果稳定。

### 补充图表

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_kQ9j5RY8ff_Avey-B/figures/002_Table_1.jpg]]
*Table 1: Design and masked language modeling (MLM) choices.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_kQ9j5RY8ff_Avey-B/figures/006_Table_3.jpg]]
*Table 3: A comparison of all the evaluated encoders across different dimensions.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_kQ9j5RY8ff_Avey-B/figures/007_Table_4.jpg]]
*Table 4: Effectiveness results comparing unidirectional vs. bi-directional rankers.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_kQ9j5RY8ff_Avey-B/figures/008_Table_5.jpg]]
*Table 5: Effectiveness results across different static (S) and dynamic (D) layering patterns.*




## 定位与知识库关联

Avey-B 属于注意力无关（attention-free）编码器架构，其方法谱系可追溯至：

1. **ColBERT（Khattab & Zaharia, 2020）**：引入 MaxSim 算子，用于计算分片间的相关性。
2. **Avey（Hammoud & Acharya, 2025）**：提出排序器+神经处理器的自回归架构，Avey-B 在此基础上进行双向化改造。
3. **gMLP（Liu et al., 2021）**：Avey-B 的静态层学习到的交叉嵌入投影矩阵呈现 Toeplitz-like（近似平移不变）结构，与 gMLP 类似。

与现有 Transformer 编码器的关键区别：
- **BERT（Devlin et al., 2019）**：使用全自注意力，复杂度 O(N²)。
- **RoBERTa（Liu et al., 2019）**：优化 BERT 预训练，仍使用全自注意力。
- **ModernBERT（Warner et al., 2025）**：使用 RoPE、FlashAttention、交替全局/局部注意力，复杂度仍为 O(N²)（但通过 FlashAttention 优化常数）。
- **NeoBERT（Breton et al., 2025）**：深度-宽度重平衡，仍使用自注意力。
- **Avey-B**：通过排序器+神经处理器实现线性复杂度 O(N)，在长序列场景下具有显著效率优势。

**局限性**：
- Avey-B 的渐近复杂度仍为 O(N² d)，因为排序器需要计算所有分片对之间的 MaxSim 分数。
- 神经压缩器在 SC 和 TC 上带来轻微的性能下降（约 0.2%）。
- Avey-B 目前没有融合内核实现（如 FlashAttention），仅使用 torch.compile 优化。
- 预训练数据量（180B token）显著少于 ModernBERT（数万亿 token）。
- 论文未提供 Avey-B 在生成任务上的评估。

**开放问题**：
- Avey-B 在更大的预训练数据量下性能是否会进一步提升？
- 能否扩展到多模态场景？
- 排序器能否通过近似最近邻搜索（如 HNSW）进一步加速？
- Avey-B 在生成任务上的表现如何？



## 原文 PDF

![[paperPDFs/ICLR_2026/Avey_B.pdf]]
