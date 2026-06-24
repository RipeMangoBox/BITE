---
title: "Quant Experts: Token-aware Adaptive Error Reconstruction with Mixture of Experts for Large Vision-Language Models Quantization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Quant_Experts_Token_aware_Adaptive_Error_Reconstruction_with_Mixture_of_Experts_for_Large_Vision_Language_Models_Quantization.pdf
project_link: null
code_link: null
aliases:
- QEQ
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将重要通道划分为token无关（全局）和token相关（局部）两组，采用混合专家（MoE）框架进行自适应误差补偿：共享专家处理全局误差，路由专家根据输入token动态处理局部误差。
primary_logic: 重要通道的出现频率分布不均：少数通道在大部分token中一致出现（token无关），而多数通道仅在特定token中出现（token相关），因此可分别使用低秩适配器建模全局和局部量化误差，并通过共同出现聚类将token相关通道分配给不同路由专家，实现token感知的自适应补偿。
claims:
- 在W4A6量化设置下，Qwen2VL-2B的QE平均准确率达到58.74，比MBQ的54.73提高4.01个百分点。
- 在Qwen2VL-72B模型上，W4A6量化下QE平均准确率提升5.09%，几乎匹配全精度性能。
- 消融实验表明，移除共享专家或路由专家都会导致一致性性能下降，随机路由或随机聚类的结果也显著差于QE提出的方法。
- 在不同模型系列（Qwen2VL 2B-72B, InternVL2 2B-8B）和量化设置（W4A6, W4A8, W3A16）上，QE一致性地超越现有静态和模态感知方法。
---

# Quant Experts: Token-aware Adaptive Error Reconstruction with Mixture of Experts for Large Vision-Language Models Quantization

> [!tip] 核心洞察
> 重要通道的出现频率分布不均：少数通道在大部分token中一致出现（token无关），而多数通道仅在特定token中出现（token相关），因此可分别使用低秩适配器建模全局和局部量化误差，并通过共同出现聚类将token相关通道分配给不同路由专家，实现token感知的自适应补偿。

| 字段 | 内容 |
|------|------|
| 中文题名 | Quant Experts：面向大型视觉-语言模型量化的标记感知自适应误差重建与混合专家 |
| 英文题名 | Quant Experts: Token-aware Adaptive Error Reconstruction with Mixture of Experts for Large Vision-Language Models Quantization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.24059) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Quant Experts (QE) |
| Dataset | Qwen2VL-2B, Qwen2VL-7B |

> [!tip] 效果简介
> - Qwen2VL-2B (W4A6) 上，Avg. (11 datasets) 58.74 vs 54.73 (MBQ) (+4.01)。
> - Qwen2VL-2B (W3A16) 上，Avg. (11 datasets) 59.29 vs 55.64 (AWQ) (+3.65)。
> - Qwen2VL-7B (W4A6) 上，Avg. (11 datasets) 65.70 vs 60.68 (MBQ) (+5.02)。

## 概述

大型视觉-语言模型（LVLM）在部署时面临显著的存储与计算压力，后训练量化（PTQ）是缓解该问题的关键手段。然而，现有 PTQ 方法普遍采用**静态识别与全局补偿重要通道**的策略，忽视了通道重要性在不同输入样本和不同 token 之间的动态变化。如图 2 和图 3 所示，重要通道的位置和出现频率在视觉 token 与文本 token 之间、甚至在同一序列的不同 token 之间差异显著——少数通道在大部分 token 中一致出现（token 无关），而多数通道仅在特定 token 中被激活（token 相关）。静态方法无法捕获这种 token 级变异，导致量化误差补偿不足，成为制约 LVLM 量化精度的核心瓶颈。

针对上述问题，本文提出 **Quant Experts (QE)**，一种**token 感知的自适应误差重建框架**。QE 的核心洞察在于：重要通道的出现频率分布极不均匀，因此可以将它们划分为 token 无关和 token 相关两组，分别建模。QE 采用**混合专家（MoE）架构**实现自适应补偿——**共享专家（Shared Expert）** 负责处理全局、token 无关的量化误差，而多个**路由专家（Routed Experts）** 根据输入 token 由轻量路由器动态选择，专精于不同 token 相关通道的局部误差模式。路由专家的分组并非随机，而是通过**共现聚类**将经常在同一 token 中共同出现的重要通道归入同一专家，使每个专家学习到紧凑且互补的误差补偿能力。

在 **Qwen2VL** 和 **InternVL2** 系列模型（2B–72B 参数规模）上的广泛实验表明，QE 在多种量化设置下一致性地超越现有静态和模态感知方法。在极具挑战性的 W4A6 量化下，Qwen2VL-2B 的平均准确率达到 **58.74**，比最强基线 MBQ 的 54.73 提升 **4.01 个百分点**；在 72B 大模型上，QE 的准确率提升高达 **5.09%**，几乎匹配全精度性能。消融实验进一步验证了共享专家与路由专家的互补必要性、自适应路由机制的有效性，以及共现聚类对专家划分的关键贡献。

## 背景与动机

大型视觉-语言模型（LVLMs）在跨模态理解与生成任务上展现了卓越能力，但其庞大的参数量和计算开销严重制约了实际部署。后训练量化（Post-Training Quantization, PTQ）通过将浮点权重和激活压缩为低比特整数表示，成为降低推理成本的主流技术路线。然而，当量化比特数降至4-bit权重与6-bit激活（W4A6）乃至更低时，模型性能会出现显著退化，其核心瓶颈在于**量化误差的补偿机制**。

现有的先进PTQ方法，如**SmoothQuant**（Xiao et al., ICML 2023）、**AWQ**（Lin et al., MLSys 2024）和**LQER**（Zhang et al., ICML 2024），均遵循“识别重要通道—补偿量化误差”的两阶段范式。它们通过在校准数据上静态分析权重矩阵的通道重要性，识别出对模型输出影响最大的“重要通道”（important channels），随后采用通道级缩放或低秩适配器进行全局误差补偿。**MBQ**（Li et al., CVPR 2025）进一步引入了模态感知的缩放策略，针对视觉和语言输入的不同敏感性分别处理。

尽管这些方法取得了显著进展，但它们共享一个根本性假设：**通道的重要性是静态的，可以在校准阶段一次性确定并全局适用**。这一假设在真实推理场景中并不成立。如图2所示，在Qwen2VL-2B的一个Transformer块中，不同模态（图像与文本）和不同token对应的输入激活值分布存在剧烈变化，重要通道的位置也随token动态迁移。更关键的是，图3的统计可视化揭示了一个此前未被充分认识的现象：少数通道在大部分token中持续被识别为重要（**token无关通道**），而大量通道仅在特定token中偶发性地重要（**token相关通道**）。静态全局方法（图3红色叉号标记）只能捕获前者，对后者的局部化、条件性误差几乎无能为力。

这一观测直接指向现有方法的**核心缺陷**：单一全局补偿策略无法建模量化误差在token维度的精细结构。当token相关通道在特定输入下被激活时，全局低秩适配器缺乏足够的表达能力来同时覆盖所有局部误差模式；而若简单增加适配器秩，又会引入冗余参数和过拟合风险。

针对上述瓶颈，本文提出**Quant Experts（QE）**，一种token感知的自适应量化误差重建框架。QE的核心思想是将重要通道按出现频率划分为token无关与token相关两组，并引入混合专家（Mixture of Experts, MoE）架构分别处理：**共享专家（Shared Expert）** 负责补偿全局、跨token一致的量化误差；**多个路由专家（Routed Experts）** 各自专精于一组共现模式相似的token相关通道，由轻量路由器根据输入token动态选择最优专家进行局部补偿。这一设计首次在LVLM量化中实现了从“静态全局补偿”到“动态token级自适应补偿”的范式转变。

## 核心创新

Quant Experts (QE) 的核心创新在于首次将**通道重要性的动态变化**作为量化误差补偿的关键控制维度，并据此设计了一套**token感知的自适应混合专家（MoE）框架**。与现有方法相比，QE 在以下四个关键设计槽位上实现了根本性转变。

### 从静态全局补偿到动静分离的通道分组

现有后训练量化方法（如 **LQER** (Zhang et al., ICML 2024)、**MBQ** (Li et al., CVPR 2025)）通常在校准数据上静态识别所有重要通道，并使用单一全局低秩适配器统一补偿量化误差。然而，QE 的观察揭示了这一策略的根本缺陷：重要通道的出现频率在不同 token 之间分布极不均匀——少数通道在大部分 token 中一致出现（token无关），而多数通道仅在特定 token 中出现（token相关）。

QE 据此将重要通道**划分为 token 无关和 token 相关两组**，分别建模。具体而言，对于每一层的权重矩阵，QE 首先在校准数据上统计每个通道被识别为“重要”的频率 $f_c$，随后依据频次阈值将通道分入两组（Algorithm 1）。这一动静分离策略使得后续的误差补偿能够针对两类通道的不同特性进行专门化处理，而非一刀切地使用全局方案。

### 从单一专家到共享-路由双轨混合专家

基于上述分组，QE 将误差补偿方案从“单一全局低秩适配器”升级为**共享专家（Shared Expert, SE）与路由专家（Routed Experts, REs）协同**的混合专家架构。

- **共享专家**负责 token 无关通道的全局误差补偿。这些通道在绝大多数 token 中都重要，因此其误差模式具有跨 token 的稳定性。QE 将这些通道的权重免于直接量化，转而使用基于白化 SVD 的低秩适配器 $\tilde{\mathbf{E}}_S^l = \mathbf{L}_{SA}^l \mathbf{L}_{SB}^l$ 重建全局量化误差，同时采用通道级缩放技术抑制激活量化误差。
- **路由专家**负责 token 相关通道的局部误差补偿。这些通道仅在特定 token 中出现，其误差模式高度依赖于输入。QE 为每组 token 相关通道分配一个专属的路由低秩适配器，通过对共享专家残差进行加权 SVD 初始化，使各专家专精于不同的局部误差模式。

最终，量化误差的重建由两者之和近似：
$$\tilde{\mathbf{E}}^l = \underbrace{\mathbf{L}_{SA}^l \mathbf{L}_{SB}^l}_{\tilde{\mathbf{E}}_S^l} + \underbrace{\mathbf{L}_{RA}^{l,i^*} \mathbf{L}_{RB}^{l,i^*}}_{\mathbf{E}_R^l(x^l)}$$

消融实验（Table 4）强有力地验证了这一双轨设计的必要性：移除共享专家（仅保留 REs）或移除路由专家（仅保留 SE）均导致一致性性能下降，证明两类专家在功能上互补——全局稳定性与局部自适应性缺一不可。

### 从随机分配到基于共现聚类的专家专精化

如何将 token 相关通道合理地分配给不同的路由专家，是 MoE 框架能否奏效的关键。QE 摒弃了随机分配，转而利用通道在 token 间的**共现模式**进行数据驱动的聚类。

具体做法是：首先构建共现指示矩阵 $\mathcal{O}^{l} \in \{0,1\}^{T \times (N_r k)}$，记录每个 token 相关通道在哪些 token 中被激活；随后计算通道间的归一化点互信息（NPMI）相似度：
$$\mathbf{S}_{i,j} = \frac{\log \frac{p(i,j)}{p(i)p(j)}}{-\log p(i,j)}$$
最后基于该相似度矩阵执行谱聚类，将具有强共现关系的通道分配至同一路由专家（Algorithm 2）。Figure 6 的 t-SNE 投影可视化证实，这种聚类方式有效地捕获了通道间的共现结构。

消融实验中，用随机聚类替代 NPMI 聚类导致性能明显下降（Table 4），证实了共现感知的通道划分对专家专精化的贡献。

### 从无选择机制到轻量级自适应路由

QE 引入了一个**轻量级路由器**，为每个输入 token 动态选择最合适的路由专家。路由器 $\mathbf{R}^l$ 根据输入 token 的绝对值预测每个路由专家的剩余误差大小，并选择预期误差最小的专家：
$$i^* = \arg\min_i (\mathbf{R}^l |x^l|)_i$$

这一设计使得误差补偿从“静态全局”跃迁为“token 级自适应”。与随机路由相比，自适应路由显著提升了精度（Table 4），证明路由器有效地为每个 token 匹配了专精于其误差模式的专家。可选的轻量级细化训练阶段（仅更新路由专家和路由器参数，采用回归损失与 KL 散度分类损失的加权组合）可进一步提升精度（Table 5）。

### 创新总结

QE 的四项核心创新——动静分离的通道分组、共享-路由双轨 MoE、共现聚类驱动的专家分配、以及自适应路由选择——形成了一个完整的因果链条：**因为**重要通道的出现频率在 token 间分布不均，**所以**需要将通道划分为 token 无关和 token 相关两组；**因为**两类通道的误差特性不同，**所以**需要共享专家与路由专家分别处理；**因为** token 相关通道具有共现模式，**所以**需要基于共现聚类分配专家；**因为**不同 token 的误差模式各异，**所以**需要路由器进行自适应选择。这一链条最终在多个模型系列和量化设置下转化为一致性的性能增益。

## 整体框架

Quant Experts (QE) 的整体设计围绕一个核心观察展开：在大视觉-语言模型（VLM）的线性层中，对量化误差贡献最大的“重要通道”并非均匀分布——少数通道在绝大多数 token 中一致出现（token 无关），而多数通道仅在特定 token 中偶发出现（token 相关）。基于这一发现，QE 构建了一个**混合专家（Mixture of Experts, MoE）**式的自适应误差补偿框架，将量化误差重建任务分解为全局补偿与局部动态补偿两部分。

### 框架总览

QE 的完整流程由四个核心模块串联而成：

1. **通道依赖划分（Channel Dependence Partitioning）**：从校准数据中统计每个通道被识别为“重要”的频率，将通道划分为 token 无关组和 token 相关组；对 token 相关通道进一步构建共现矩阵，通过归一化点互信息（NPMI）相似度进行谱聚类，形成 $N_r$ 个通道簇（Algorithm 1, Section 3.1 & 3.3）。

2. **共享专家（Shared Expert, SE）**：负责 token 无关重要通道的全局误差补偿。这些通道的对应权重被豁免于直接量化，转而使用基于白化 SVD 的低秩适配器 $\tilde{\mathbf{E}}_S^l = \mathbf{L}_{SA}^l \mathbf{L}_{SB}^l$ 进行重建；同时引入通道级缩放（channel-wise scaling）以抑制激活量化误差（Section 3.2, Algorithm 3）。

3. **路由专家（Routed Experts, REs）**：每个 token 相关通道簇分配一个专属的低秩适配器。各 RE 以 SE 重建后的残差 $\mathbf{E}_S^l = \mathbf{E}^l - \bar{\mathbf{L}}_{SA}^l \mathbf{L}_{SB}^l$ 为目标，通过加权 SVD 初始化，各自专精于特定的局部误差模式（Section 3.3, Algorithm 2）。

4. **路由器（Router）**：一个轻量级模块，根据输入 token 预估每个路由专家的剩余误差大小，选择预期误差最小的专家 $i^* = \arg\min_i (\mathbf{R}^l |x^l|)_i$，实现 token 级的自适应动态补偿（Section 3.1, Eq. 6）。

### 推理流程

在推理阶段，QE 的计算流程如图 Figure 5 所示：对于每个线性层的输入 token，共享专家提供恒定的全局误差补偿，路由器并行评估所有路由专家并激活最优者，最终该层的量化误差由共享专家与选定路由专家的低秩输出之和近似：

$$\tilde{\mathbf{E}}^l = \underbrace{\mathbf{L}_{SA}^l \mathbf{L}_{SB}^l}_{\tilde{\mathbf{E}}_S^l} + \underbrace{\mathbf{L}_{RA}^{l,i^*} \mathbf{L}_{RB}^{l,i^*}}_{\mathbf{E}_R^l(x^l)}$$

这一设计的重建目标是最小化补偿后的激活误差（Section 3.1, Eq. 4）：

$$\arg\min_{\tilde{\mathbf{E}}^l} \| (\mathbf{E}^l - (\tilde{\mathbf{E}}_S^l + \tilde{\mathbf{E}}_R^l(x^l))) x^l \|_F$$

### 可选细化阶段

在初始量化完成后，QE 支持一个可选的轻量级细化（Refinement）阶段。此阶段仅更新路由专家参数 $(\mathbf{L}_{RA}^l, \mathbf{L}_{RB}^l)$ 和路由器 $\mathbf{R}^l$，其余参数保持冻结，采用层式训练策略，联合优化回归损失 $\mathcal{L}_{\mathrm{reg}}$ 与 KL 散度分类损失 $\mathcal{L}_{\mathrm{cls}}$（Section 7.2, Eq. 11-15）。该细化阶段可进一步提升精度，但需要额外迭代和数据。

### 复杂度概要

QE 引入的额外计算和存储开销主要来自低秩适配器和路由器。Table 7 提供了线性层的复杂度分析，表明 QE 在保持推理加速的同时，以可控的额外参数实现了 token 感知的自适应补偿。在 NPU 上的实测加速比如 Table 8 所示，QE 量化的 Qwen2VL-7B 线性层在 prefill 阶段（序列长度 128）相对于 FP16 模型取得了显著加速。

### 补充图表

![[assets/figures/papers/paper_list_l2241_https_arxiv_org_abs_2602_24059/figures/004_Figure_4.jpg]]
*Figure 4: The framework of Quant Experts (QE). The token-independent channels are model by a shared expert, while token-dependent channels are captured by multiple routed experts. A lightweight low-rank adapter is implemented for each expert*

## 核心模块与公式推导

### 3.1 通道重要性建模与分区

QE 的核心观察是：重要通道的出现频率在不同 token 间分布极不均匀。为此，方法首先从校准数据中统计每个通道被识别为“重要”的频率，并据此将通道划分为两类。

**通道重要性权重向量**。对于线性层权重矩阵 $\mathbf{W}_f \in \mathbb{R}^{d_{out} \times d_{in}}$，定义基础通道重要性为每行绝对值的均值：

$$\mathbf{w} := \mathrm{Mean}_{row}(|\mathbf{W}_f|)$$

其中 $\mathbf{w} \in \mathbb{R}^{d_{in}}$ 反映各输入通道对输出的平均贡献强度。

**Token 级重要通道识别**。对于输入 token $x_t$，其重要通道集由 token 值与通道权重的逐元素乘积的绝对值决定：

$$\mathcal{C}_t = \mathrm{Top-}k(|x_t| \odot \mathbf{w})$$

该式表明，重要通道的判定同时取决于静态权重重要性和动态 token 激活值——这正是 token 感知量化的基础。

**通道分区**。统计每个通道 $c$ 在校准数据所有 token 中被识别为重要的频率：

$$f_c = k \times \frac{m_c}{\sum_{i=0}^{d_{in}} m_i}$$

其中 $m_c$ 为通道 $c$ 出现在前 $k$ 重要通道集中的 token 数量。根据频率阈值，通道被划分为：
- **Token 无关通道**：在绝大多数 token 中一致出现的高频通道，反映全局量化误差；
- **Token 相关通道**：仅在特定 token 中出现的低频通道，反映局部、条件化的误差模式。

### 3.2 量化误差重建目标

量化后的权重矩阵 $\mathbf{W}_q$ 与原始权重 $\mathbf{W}$ 之间存在误差 $\mathbf{E} = \mathbf{W} - \mathbf{W}_q$。QE 将此误差分解为全局分量和 token 条件分量，并用低秩适配器之和逼近：

$$\arg\min_{\tilde{\mathbf{E}}^l} \| (\mathbf{E}^l - (\tilde{\mathbf{E}}_S^l + \tilde{\mathbf{E}}_R^l(x^l))) x^l \|_F$$

其中 $\tilde{\mathbf{E}}_S^l$ 为共享专家重建的全局误差，$\tilde{\mathbf{E}}_R^l(x^l)$ 为路由专家根据输入 $x^l$ 动态重建的局部误差。目标是最小化重建残差对输入激活加权的 Frobenius 范数。

**低秩参数化**。两类专家均实现为低秩适配器：

$$\tilde{\mathbf{E}}^l = \underbrace{\mathbf{L}_{SA}^l \mathbf{L}_{SB}^l}_{\tilde{\mathbf{E}}_S^l} + \underbrace{\mathbf{L}_{RA}^{l,i^*} \mathbf{L}_{RB}^{l,i^*}}_{\mathbf{E}_R^l(x^l)}$$

共享专家 $\mathbf{L}_{SA}^l \in \mathbb{R}^{d_{out} \times r_s}$、$\mathbf{L}_{SB}^l \in \mathbb{R}^{r_s \times d_{in}}$ 对所有 token 恒定；路由专家 $\mathbf{L}_{RA}^{l,i} \in \mathbb{R}^{d_{out} \times r_r}$、$\mathbf{L}_{RB}^{l,i} \in \mathbb{R}^{r_r \times d_{in}}$ 由路由器根据当前 token 动态选择。

**路由器选择机制**。轻量级路由器 $\mathbf{R}^l$ 根据输入 token 预估每个路由专家的剩余误差，选择预期误差最小的专家：

$$i^* = \arg\min_i (\mathbf{R}^l |x^l|)_i$$

路由器以 token 绝对值作为输入，输出各专家的误差分数，分数越低表示该专家对当前 token 的补偿能力越强。

### 3.3 共享专家：全局误差补偿

共享专家负责处理 token 无关通道的量化误差。具体流程（Algorithm 3）：
1. **通道豁免**：将 token 无关通道对应的权重列免于直接量化，保留全精度；
2. **白化 SVD 初始化**：对豁免后的权重矩阵进行白化处理，再通过截断 SVD 获得低秩初始化 $\mathbf{L}_{SA}^l$、$\mathbf{L}_{SB}^l$，以减小激活分布偏移对低秩分解的影响；
3. **通道级缩放**：采用类似 SmoothQuant 的通道级缩放技术，将激活量化难度转移到权重侧，抑制激活量化误差。

共享专家重建后，残差误差 $\mathbf{E}_S^l = \mathbf{E}^l - \mathbf{L}_{SA}^l \mathbf{L}_{SB}^l$ 将交由路由专家进一步补偿。

### 3.4 路由专家：Token 条件误差补偿

**共现聚类**。token 相关通道在不同 token 间呈现协同出现模式。QE 通过构建共现矩阵捕捉这种关联：

$$\mathcal{O}_{t,i}^{l} = \mathbf{1}(c_i \in \mathcal{C}_r^{l} \cap \mathcal{A}_t^{l})$$

其中 $\mathcal{C}_r^{l}$ 为 token 相关通道集，$\mathcal{A}_t^{l}$ 为 token $t$ 的重要通道集。$\mathcal{O}^{l} \in \{0,1\}^{T \times (N_r k)}$ 记录了每个 token 相关通道在每个 token 上是否重要。

基于共现矩阵计算边缘概率和联合概率：

$$p(i) = \frac{1}{T} \sum_{t}^{T} \mathcal{O}_{t,i}^{l}, \quad p(i,j) = \frac{1}{T} \sum_{t}^{T} (\mathcal{O}_{t,i}^{l} \mathcal{O}_{t,j}^{l})$$

采用归一化点互信息（NPMI）量化通道间的共现强度：

$$\mathbf{S}_{i,j} = \frac{\log \frac{p(i,j)}{p(i)p(j)}}{-\log p(i,j)}$$

以 $\mathbf{S}$ 为相似度矩阵执行谱聚类，将 token 相关通道划分为 $N_r$ 组。每组通道共享相似的出现模式，由一个专属路由专家处理。

**专家初始化**。每个路由专家对共享专家的残差 $\mathbf{E}_S^l$ 进行加权 SVD 初始化，权重由对应通道簇的重要性决定，使各专家专精于其通道组的局部误差模式。

**推理流程**（Figure 5）：共享专家提供恒定的全局补偿；路由器根据当前 token 从 $N_r$ 个路由专家中动态选择最优者，实现 token 感知的自适应局部补偿。

### 补充图表

![[assets/figures/papers/paper_list_l2241_https_arxiv_org_abs_2602_24059/figures/005_Figure_5.jpg]]
*Figure 5: Illustration of the Inference Computation Process of QE*

![[assets/figures/papers/paper_list_l2241_https_arxiv_org_abs_2602_24059/figures/011_Figure_6.jpg]]
*Figure 6: Illustration of the Co-Occurrence-Based Clustering in a Transformer Block of Qwen2VL-2B. (a) Similarity matrix*

## 实验与分析

### 主要结果

QE 在多个模型系列、多种量化设置下一致性地超越现有静态和模态感知的量化方法。在 Qwen2VL-2B 的 W4A6 量化设置下，QE 在 11 个基准上的平均准确率达到 **58.74**，相比模态感知方法 **MBQ**（Li et al., CVPR 2025）的 54.73 提升了 **4.01 个百分点**，比基于低秩重构的 **LQER**（Zhang et al., ICML 2024）的 56.19 高出 2.55 个百分点（Table 1）。在仅权重量化的 W3A16 设置下，QE 同样以 59.29 的平均准确率超越 **AWQ**（Lin et al., MLSys 2024）的 55.64，增益达 3.65 个百分点。

![[assets/figures/papers/paper_list_l2241_https_arxiv_org_abs_2602_24059/figures/006_Table_1.jpg]]
*Table 1: Main results on the model of Qwen2VL-2B*

在更大规模的 Qwen2VL-7B 上，QE 的优势进一步扩大：W4A6 下平均准确率达到 65.70，比 MBQ 的 60.68 提升 5.02 个百分点（Table 9）。在 Qwen2VL-72B 上，QE 在 W4A6 量化下实现 5.09% 的准确率提升，几乎匹配全精度性能（Table 3）。跨模型架构的泛化性在 InternVL2 系列上得到验证：InternVL2-8B 的 W4A6 设置下，QE 以显著优势超越所有基线（Table 2）；InternVL2-2B 上同样保持一致的领先（Table 10）。

![[assets/figures/papers/paper_list_l2241_https_arxiv_org_abs_2602_24059/figures/008_Table_3.jpg]]
*Table 3: Main results of Qwen2VL-72B model (higher is better)*

![[assets/figures/papers/paper_list_l2241_https_arxiv_org_abs_2602_24059/figures/007_Table_2.jpg]]
*Table 2: Main results on the model of InternVL2-8B*

值得注意的是，QE 在纯语言基准 MMLU 上也表现出色，表明其 token 感知自适应补偿不仅适用于多模态场景，对纯语言推理同样有效（Table 11）。对视觉编码器与合并模块的量化实验进一步揭示，视觉编码器的量化对整体性能影响最大，而 QE 在这些模块上仍能保持稳健（Table 12）。

### 消融实验

消融实验系统验证了 QE 各组件的独立贡献（Table 4）。移除共享专家（仅保留路由专家）或移除路由专家（仅保留共享专家）均导致一致性性能下降，证实了两类专家互补的必要性——全局误差与局部 token 相关误差需要分别建模。用随机路由替代自适应路由机制，精度显著降低，证明路由器能有效为每个 token 选择最合适的专家。用随机聚类替代基于归一化点互信息（NPMI）的共现聚类来划分 token 相关通道，性能同样明显下降，验证了共现聚类对通道分组的关键作用。

![[assets/figures/papers/paper_list_l2241_https_arxiv_org_abs_2602_24059/figures/009_Table_4.jpg]]
*Table 4: Ablation study results on Qwen2VL-2B model*

超参数分析揭示了性能对重要通道数量和专家数量的敏感性。重要通道数 $k$ 从 4 增至 32 时性能稳步提升，但 $k=64$ 时性能饱和甚至略微下降，表明过多通道会稀释对真正关键通道的聚焦（Table 13）。路由专家数量 $N_r$ 从 2 增至 8 带来持续增益，进一步增加则收益递减且内存开销增大（Table 6）。

![[assets/figures/papers/paper_list_l2241_https_arxiv_org_abs_2602_24059/figures/016_Table_6.jpg]]
*Table 6: Impact of the number of routed experts on the performance of Qwen2VL-2B under the W4A6 quantization setting*

![[assets/figures/papers/paper_list_l2241_https_arxiv_org_abs_2602_24059/figures/021_Table_13.jpg]]
*Table 13: Impact of the number of important channels on the performance of Qwen2VL-2B under the W4A6 quantization setting*

可选的细化训练阶段能进一步释放 QE 的潜力（Table 5）。在 Qwen2VL-2B W4A6 设置下，仅更新路由专家和路由器参数，MMMU 基准从 33.78 提高至 36.89，其他基准亦有不同程度提升。该细化采用层式训练，仅使用回归损失和 KL 散度分类损失，计算开销极低。

![[assets/figures/papers/paper_list_l2241_https_arxiv_org_abs_2602_24059/figures/013_Table_5.jpg]]
*Table 5: Ablation study of Refinement on Routed Experts*

### 效率分析

QE 引入的额外计算和存储开销是可控的。复杂度分析（Table 7）表明，路由专家的低秩适配器仅引入与秩 $r$ 成线性关系的额外参数和计算量。在 NPU 上的实测加速比（Table 8）显示，Qwen2VL-7B 线性层在 prefill 阶段（序列长度 $s=128$）相比 FP16 模型可实现显著加速，加速比随输入/输出通道维度变化，验证了量化方法在实际硬件上的部署效益。

![[assets/figures/papers/paper_list_l2241_https_arxiv_org_abs_2602_24059/figures/014_Table_7.jpg]]
*Table 7: Complexity analysis of the linear layer in QE method*

![[assets/figures/papers/paper_list_l2241_https_arxiv_org_abs_2602_24059/figures/015_Table_8.jpg]]
*Table 8: NPU speedup ratios of QE for Qwen2VL-7B linear layers compared with the fp16 model, measured during the prefill stage with a sequence length of s=128. “IC” and “OC” denote the input and output channel dimensions, respectively*

### 局限与失败模式

尽管 QE 在多个基准上表现优异，但仍存在若干局限。首先，通道重要性划分依赖于校准数据集，不同数据集可能导致不同的通道分组，进而影响最终性能。其次，在极端低比特设置（如 3-bit 权重加低比特激活）下，QE 与全精度之间仍存在不可忽视的差距。此外，路由机制引入的动态选择对批处理效率的影响在资源极度受限的边缘设备上可能需要进一步优化。当前实验仅覆盖 Qwen2VL 和 InternVL2 两种 VLM 架构，对其他流行模型（如 LLaVA、BLIP）的泛化性有待验证。方法主要针对线性层的权重量化设计，尚未扩展到注意力计算和 KV 缓存等其他模块。

## 方法谱系与知识库定位

### 与现有量化方法的差异化定位

**Quant Experts (QE)** 针对大视觉-语言模型（VLM）的后训练量化（PTQ），在“重要通道识别与误差补偿”这一关键环节上，与现有方法形成了清晰的演进关系。

**静态全局补偿范式**是此前的主流。**SmoothQuant**（Xiao et al., ICML 2023）通过通道级缩放系数平滑激活异常值，实现全局统一的量化难度迁移；**AWQ**（Lin et al., MLSys 2024）基于激活感知的通道重要性进行权重缩放，但仅处理权重量化。这些方法的核心假设是：重要通道的分布模式在校准数据上是稳定的，因此一组固定的缩放系数或补偿参数即可覆盖所有输入。然而，QE 的观测实验（Figure 2-3）揭示了一个被忽视的事实：重要通道的位置和出现频率在不同 token（图像 token 与文本 token，以及 token 内部）之间呈现显著动态变化，静态全局方法无法捕获这种 token 级变异。

**模态感知方法**向前迈进了一步。**MBQ**（Li et al., CVPR 2025）识别到视觉和语言模态对量化的敏感度不同，并按模态分别设计缩放策略。但 QE 进一步指出，即使在同一模态内部，不同 token 的重要通道模式也存在差异——模态感知策略仍是一种粗粒度的静态分组。

**低秩误差补偿**提供了另一条路径。**LQER**（Zhang et al., ICML 2024）使用单一全局低秩适配器重建量化误差矩阵，避免了直接量化重要通道带来的信息损失。QE 继承了这一低秩补偿的思想，但将单一的全局适配器扩展为混合专家（MoE）框架：共享专家（SE）处理 token 无关的全局误差，多个路由专家（REs）根据输入 token 动态处理局部误差。这一设计的关键洞察在于：重要通道的出现频率分布极不均匀——少数通道在大多数 token 中一致出现（token 无关），而多数通道仅在特定 token 中出现（token 相关）。因此，用统一的低秩适配器同时处理两类通道，会迫使模型在全局一致性和局部特异性之间做出折衷。

### 方法适用边界

QE 的当前设计存在以下明确边界：

1. **模型架构边界**：实验覆盖了 Qwen2VL（2B-72B）和 InternVL2（2B-8B）两个 VLM 系列，对其他流行的 VLM 架构（如 LLaVA、BLIP-2、MiniGPT-4）的泛化性尚未验证。这些架构在视觉编码器选择、跨模态融合机制上的差异可能影响通道重要性分布模式，进而影响 QE 的分组策略有效性。

2. **量化模块边界**：QE 主要针对 Transformer 线性层的权重量化设计，尚未扩展到注意力计算中的 Q/K/V 投影、KV 缓存量化或视觉编码器的卷积层。Table 12 的消融表明，对视觉编码器和合并模块进行量化会引入额外精度损失，QE 在这些模块上的补偿策略仍有待探索。

3. **比特宽度边界**：主要实验集中在 W4A6、W4A8 和 W3A16 设置。在更极端的低比特场景（如 W3A4 或 W2A8），量化误差的规模和分布可能超出当前低秩适配器的重建能力，性能与全精度的差距仍然显著。

4. **校准数据依赖性**：通道重要性划分依赖于校准数据集（论文使用 ShareGPT4V 增强的 COCO Caption 中随机抽取的 128 组图文对）。不同领域或分布的校准数据可能导致不同的通道分组结果，进而影响量化模型在下游任务上的表现。这种依赖性在跨领域迁移场景中尤为值得关注。

### 局限性与开放问题

**计算与存储开销**：QE 引入的路由专家和路由器虽然设计为轻量级（Table 7 提供了复杂度分析），但在批量推理场景中，动态专家选择可能影响计算流水线的规整性。Table 8 展示了在 NPU 上相对于 FP16 的加速比，但在极资源受限的边缘设备上，额外的存储（多组低秩矩阵）和路由计算仍需审慎评估。

**路由机制的鲁棒性**：当前路由器基于对每个专家剩余误差的预估进行硬选择（top-1 路由），消融实验（Table 4）表明随机路由会显著降低精度，验证了路由机制的关键作用。然而，硬路由在批处理时可能导致不同 token 激活不同专家，降低硬件利用率。是否可以采用 top-2 软路由或负载均衡策略，在精度和效率之间取得更好平衡，是一个开放问题。

**超参数自动化**：重要通道数量 $k$ 和路由专家数量 $N_r$ 目前需手动调节。消融实验（Table 13, Table 6）表明 $k$ 从 4 增至 32 持续提升性能，但 $k=64$ 时性能饱和甚至略微下降；$N_r$ 从 2 增至 8 带来持续增益，进一步增加则收益递减。能否设计数据驱动的方法（如基于验证集性能的自动搜索或基于通道重要性分布的启发式规则）自动确定这些超参数，是提升方法易用性的关键。

**跨模态与跨任务泛化**：QE 的 token 感知自适应补偿框架的核心思想——识别并分别处理全局一致和局部变化的误差模式——在理论上具有通用性。该方法能否推广到纯语言模型（如 LLaMA 系列）的量化、单模态视觉模型（如 ViT）的量化，甚至语音-语言多模态模型，是一个值得探索的方向。此外，在更大规模模型（>100B）上，通道重要性的分布模式是否遵循类似的规律，也需要进一步验证。

**与其他压缩技术的协同**：QE 的低秩适配器结构天然适合与混合精度量化、结构化稀疏剪枝等技术结合。例如，是否可以对不同专家分配不同的量化比特宽度，或对路由专家进行结构化剪枝以进一步减少参数，这些协同优化方向可能带来额外的效率增益。

## 原文 PDF

![[paperPDFs/CVPR_2026/Quant_Experts_Token_aware_Adaptive_Error_Reconstruction_with_Mixture_of_Experts_for_Large_Vision_Language_Models_Quantization.pdf]]