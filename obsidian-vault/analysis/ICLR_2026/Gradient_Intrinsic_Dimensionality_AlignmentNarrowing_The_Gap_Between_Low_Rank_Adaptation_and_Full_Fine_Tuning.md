---
title: "Gradient Intrinsic Dimensionality Alignment：Narrowing The Gap Between Low-Rank Adaptation and Full Fine-Tuning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Gradient_Intrinsic_Dimensionality_AlignmentNarrowing_The_Gap_Between_Low_Rank_Adaptation_and_Full_Fine_Tuning.pdf
project_link: null
code_link: null
aliases:
- RRP
- "RaLoRA / RaLoRA-Pro"
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "RaLoRA用熵基梯度内在维度估计来决定LoRA块对角结构和等效秩。"
primary_logic: "先逐层估计全微调梯度有效秩，再在固定参数预算下进行层内块分解和层间重要性重分配。"
claims:
- "固定低秩LoRA会压缩远高于预设秩的全微调梯度有效方向。"
- "RaLoRA通过块对角分解提高等效表达秩而不增加参数量。"
- "RaLoRA-Pro结合损失敏感性分配参数，在GLUE、GSM8K、HumanEval和图像分类任务上缩小与全微调差距。"
---

# Gradient Intrinsic Dimensionality Alignment：Narrowing The Gap Between Low-Rank Adaptation and Full Fine-Tuning

> [!tip] 核心洞察
> 表达力不仅取决于参数量，还取决于架构结构。通过将 LoRA 的秩与 GID 对齐，可以在不增加参数的情况下更有效地利用容量，从而缩小与全微调的差距。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 梯度内在维度对齐：缩小低秩适配与全量微调之间的差距 |
| 英文题名 | Gradient Intrinsic Dimensionality Alignment：Narrowing The Gap Between Low-Rank Adaptation and Full Fine-Tuning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=kObvnQ6pUx) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | RaLoRA / RaLoRA-Pro |
| Dataset | GLUE (T5-Base), MT-Bench (LLaMA-3.1-8B), GSM8K (LLaMA-3.1-8B), HumanEval (LLaMA-3.1-8B) |

> [!tip] 效果简介
> - GLUE (T5-Base) 上，平均分 为 87.24 (RaLoRA) / 87.23 (RaLoRA-Pro)，对比 82.08 (LoRA)，变化 +5.16 / +5.15。
> - MT-Bench (LLaMA-3.1-8B) 上，评分 (0-10) 为 6.38 (RaLoRA) / 6.72 (RaLoRA-Pro)，对比 6.15 (LoRA)，变化 +0.23 / +0.57。
> - GSM8K (LLaMA-3.1-8B) 上，准确率 (%) 为 72.25 (RaLoRA) / 73.01 (RaLoRA-Pro)，对比 67.78 (LoRA)，变化 +4.47 / +5.23。

## 概要

本文提出了一种基于梯度本征维度（Gradient Intrinsic Dimensionality, GID）对齐的参数高效微调方法，旨在解决LoRA（Low-Rank Adaptation）因固定低秩结构导致的性能瓶颈。作者首先通过熵基估计器量化全微调梯度的有效秩，发现其可达300，远超LoRA预设的固定秩（通常为8）。基于此观察，提出了两种方法：RaLoRA通过块对角分解将LoRA适配器的等效秩与GID对齐，在不增加参数量的情况下扩展表达力；RaLoRA-Pro进一步引入损失敏感性引导的层间参数重分配，实现层内几何结构与层间重要性的双重对齐。实验表明，RaLoRA和RaLoRA-Pro在GLUE、GSM8K、HumanEval、MT-Bench及图像分类任务上显著优于现有LoRA变体，大幅缩小了与全微调的差距。



**LoRA的梯度压缩本质**：LoRA将权重更新建模为低秩矩阵的乘积 $\Delta W = \frac{\bar{\alpha}}{r} B A$。其更新过程可近似为将全梯度 $G_t$ 投影到由 $B_t B_t^\top$ 和 $A_t^\top A_t$ 张成的低秩子空间（Equation (1)）。当全微调梯度的真实有效更新方向（即GID）远超LoRA秩 $r$ 时，这种投影会导致显著的信息损失。

**核心瓶颈**：全微调梯度的GID可达300（Figure 1(a)），而LoRA通常使用固定秩 $r=8$。这种失配是LoRA性能不及全微调的根本原因。现有改进方法（如AdaLoRA、DoRA、PiSSA等）虽在初始化或秩分配上有所优化，但均未直接解决秩结构与梯度本征维度对齐的问题。

**因果旋钮**：通过熵估计器逐层量化GID，并据此自适应调整LoRA适配器的秩结构——RaLoRA采用块对角分解扩展等效秩，RaLoRA-Pro进一步结合损失敏感性进行层间参数重分配——从而在固定参数预算下使适配容量与优化景观的结构复杂度对齐。



## 核心方法与创新机理

1. **熵基GID估计器**：提出基于奇异值分布熵的有效秩度量 $\operatorname{erank}(G_l) = \exp\left(-\sum_{i=1}^n p_i \log p_i\right), p_i = \sigma_i / \sum \sigma_j$（Equation (3)），作为GID的稳健估计。相比阈值基SVD方法（Equation (2)），该方法无需手动调参，且对超参数不敏感（Table 7）。

2. **RaLoRA：层内GID对齐**：将LoRA矩阵分解为 $n_l$ 个块对角子块，等效秩扩展为 $n_l \times r$，参数数不变。块数由 $e_l = \lfloor \log_2(\operatorname{erank}(G_l)/r) \rfloor, n_l = 2^{e_l}$ 确定（Equation (4)），受 $n_{\max}$ 约束。

3. **RaLoRA-Pro：双重对齐**：在RaLoRA的层内GID对齐基础上，引入损失敏感性引导的层间参数重分配。重要性得分定义为 $\operatorname{I}(W_l) = \operatorname{avg}(|W_l \odot G_l|)$（Equation (5)），归一化后按比例分配秩 $r_l = \left[P_{\text{total}} \cdot \alpha_l / \sqrt{d_{\text{in}}^l + d_{\text{out}}^l}\right]$（Equation (8)），实现层内与层间双对齐。



![[assets/figures/papers/iclr26_0001_kObvnQ6pUx_Gradient_Intrinsic_Dimensionality_AlignmentNarro/figures/001_Figure_1.jpg]]

Figure 2 展示了所提方法与标准LoRA的对比概览：

- **RaLoRA**：通过熵基估计器计算每层GID，据此将LoRA的 $B, A$ 矩阵分解为 $n_l$ 个并行子块，每个子块为独立的低秩对 $(B_p, A_p)$。块对角结构使等效秩提升至 $n_l \times r$，而参数量保持 $r(d_{\text{in}} + d_{\text{out}})$ 不变。

- **RaLoRA-Pro**：在RaLoRA基础上，额外计算每层的重要性得分 $\operatorname{I}(W_l)$，基于归一化重要性 $\alpha_l$ 在层间重分配参数预算。最终每层获得自适应秩 $r_l$ 和块数 $n_l$，实现双重对齐。



### 5.1 熵基GID估计器

**阈值基方法**（Equation (2)）：$\operatorname{rank}(G) = \max\{ i \mid \sigma_i > \varepsilon \}$，对阈值 $\varepsilon$ 敏感。

**熵基有效秩**（Equation (3)）：
$$\operatorname{erank}(G_l) = \exp\left(-\sum_{i=1}^n p_i \log p_i\right), \quad p_i = \frac{\sigma_i}{\sum_{j=1}^n \sigma_j}$$

该度量基于归一化奇异值分布的香农熵，对奇异值分布的形状敏感而非绝对值，因此更稳健。

### 5.2 RaLoRA块对角分解

**块数确定**（Equation (4)）：
$$e_l = \left\lfloor \log_2\left(\frac{\operatorname{erank}(G_l)}{r}\right) \right\rfloor, \quad n_l = 2^{e_l}, \quad \text{s.t.} \quad 1 \leq n_l \leq n_{\max}$$

当 $n_l = 1$ 时，RaLoRA退化为标准LoRA。随着 $n_l$ 增加，RaLoRA在主导方向上的精度与更广泛的表达力之间进行自适应权衡（Appendix C.1）。

**近似误差分析**（Appendix C.2）：
- LoRA的极小Frobenius范数误差：$E_{\text{LoRA}} = \sum_{i=r+1}^{\min(m,n)} \sigma_i^2$（Equation (24)）
- RaLoRA的总近似误差：$E_{\text{RaLoRA}} = \sum_{p \neq q} \lVert \Delta W_{p,q} \rVert_F^2 + \sum_{p=1}^{n_l} \lVert \Delta W_{p,p} - B_p A_p \rVert_F^2$（Equation (28)）

RaLoRA牺牲了对全局主导奇异方向的保真度，但通过并行学习异构子空间获得了更广泛的表达力。

### 5.3 RaLoRA-Pro损失敏感性引导重分配

**重要性得分**（Equation (5)）：$\operatorname{I}(W_l) = \operatorname{avg}(|W_l \odot G_l|)$，衡量权重矩阵与梯度逐元素乘积的平均值。

**归一化重要性**（Equation (6)）：$\alpha_l = I_l / \sum_{k=1}^N I_k$

**总参数预算**（Equation (7)）：$P_{\text{total}} = \sum_{l=1}^N \left(\sqrt{d_{\text{in}}^l + d_{\text{out}}^l}\right) r_{\text{ref}}$

**重分配秩**（Equation (8)）：
$$r_l = \left[\frac{P_{\text{total}} \cdot \alpha_l}{\sqrt{d_{\text{in}}^l + d_{\text{out}}^l}}\right], \quad \text{s.t.} \quad r_{\min} \leq r_l \leq r_{\max}$$

GID与Fisher Information的相关性分析（Table 8）显示，两者Pearson相关系数最高仅0.277，表明它们捕捉优化景观的不同方面，验证了双重对齐策略的必要性。



## 实验与关键发现

### 6.1 自然语言理解（GLUE）

Table 1 展示了在T5-Base上微调的结果：

![[assets/figures/papers/iclr26_0001_kObvnQ6pUx_Gradient_Intrinsic_Dimensionality_AlignmentNarro/figures/004_Table_1.jpg]]
*Table 1: Result of fine-tuning T5-Base using full fine-tuning and different LoRA variants on the five subsets of GLUE benchmark. On GSM8K, RaLoRA reaches 72.25, resulting in a +4.47 improvement over vanilla LoRA and recovering 75.6% of the FFT performance. The performance of RaLoRA on MT-Bench is also highly competitive, matching the strongest baseline (i.e., MoRA) while being significantly more stable. These results suggest that RaLoRA aligns the rank of LoRA with the corresponding GID, enhancing intra-layer expressiveness significantly without increasing the number of parameters.*

| 方法 | 平均分 | 相比LoRA提升 |
|------|--------|-------------|
| LoRA | 82.08 | - |
| RaLoRA | 87.24 | +5.16 |
| RaLoRA-Pro | 87.23 | +5.15 |

在QNLI和MRPC上，RaLoRA和RaLoRA-Pro甚至超越了全微调（全微调QNLI: 93.19, MRPC: 84.56；RaLoRA: 93.36, 84.74）。

### 6.2 自然语言生成（NLG）

Table 2 展示了在LLaMA-3.1-8B-Base上的结果：

![[assets/figures/papers/iclr26_0001_kObvnQ6pUx_Gradient_Intrinsic_Dimensionality_AlignmentNarro/figures/005_Table_2.jpg]]
*Table 2: Performance of LLaMA-3.1-8B-Base fine-tuned with full fine-tuning and various LoRA variants on MT-Bench, GSM8K, and HumanEval. All methods use comparable trainable parameters, with LoRA rank and reference rank $r _ { \mathrm { r e f } }$ in equation 7 set to 8.*

| 方法 | MT-Bench | GSM8K | HumanEval |
|------|----------|-------|-----------|
| 全微调 | 5.88 | 73.69 | 51.63 |
| LoRA | 6.15 | 67.78 | 43.09 |
| RaLoRA | 6.38 | 72.25 | 48.78 |
| RaLoRA-Pro | 6.72 | 73.01 | 48.37 |

- RaLoRA在HumanEval上达到48.78，相比LoRA提升+5.69，将差距缩小66.6%。
- RaLoRA-Pro在GSM8K上达到73.01，恢复全微调性能的88.5%。
- RaLoRA-Pro在MT-Bench上达到6.72，甚至超过全微调（5.88）。

### 6.3 图像分类

Table 3 展示了在CLIP-ViT-B/16上的结果（7数据集平均）：

![[assets/figures/papers/iclr26_0001_kObvnQ6pUx_Gradient_Intrinsic_Dimensionality_AlignmentNarro/figures/006_Table_3.jpg]]
*Table 3: Results of CLIP-ViT-B/16 on image classification tasks using different LoRA variants. Note that zero-shot results are reported following (Wang et al., 2024c).*

| 方法 | 平均准确率 |
|------|-----------|
| LoRA | 89.08 |
| RaLoRA | 90.53 |
| RaLoRA-Pro | 90.66 |

RaLoRA-Pro相比LoRA提升1.58%。

### 6.4 消融研究

**秩估计策略对比**（Table 7）：熵基GID估计器在GSM8K上达到72.25±0.59，在HumanEval上达到48.78±1.61，一致优于阈值基方法。阈值法在HumanEval上随 $\varepsilon$ 变化性能波动超2.2点。

**不同秩配置**（Table 4）：RaLoRA在所有秩设置（r=8,16,32,64）下一致优于LoRA。RaLoRA-Pro在高秩下一致优于LS-LoRA。

![[assets/figures/papers/iclr26_0001_kObvnQ6pUx_Gradient_Intrinsic_Dimensionality_AlignmentNarro/figures/010_Table_4.jpg]]
*Table 4: Performance comparison of LoRA, LS-LoRA, RaLoRA, and RaLoRA-Pro on MT-Bench, GSM8K, and HumanEval under different rank configurations.*

**最大扩展因子 $n_{\max}$**（Table 5）：最优 $n_{\max}$ 与任务相关——GSM8K在 $n_{\max}=16$ 时最佳，MT-Bench和HumanEval随 $n_{\max}$ 增大而提升。

![[assets/figures/papers/iclr26_0001_kObvnQ6pUx_Gradient_Intrinsic_Dimensionality_AlignmentNarro/figures/011_Table_5.jpg]]

**秩范围消融**（Table 6）：RaLoRA-Pro中秩范围(4,16)在GSM8K上最优，更宽范围(4,32)在MT-Bench和HumanEval上更优。

**GID与Fisher Information相关性**（Table 8）：Pearson相关系数最高0.277，表明两者捕捉优化景观的不同方面。

**LoRA+GID参数效率**（Table 9）：仅用GID分配秩的LoRA+GID在GSM8K上达到75.41（LoRA(r=200)为74.12），验证了GID对齐的有效性。

**与非LoRA PEFT方法对比**（Table 10）：RaLoRA-Pro在GSM8K上达到73.01，远超(IA)^3（66.62）和FourierFT（52.71）。(IA)^3和FourierFT在Code-Feedback上无法收敛。

**与HiRA对比**（Table 11）：RaLoRA在HumanEval上达到48.78，优于HiRA（45.73）。

### 6.5 GID分析

Figure 3 展示了层间GID热力图和训练动态：
- 估计的GID范围在30–1000之间，与先前发现一致（全微调梯度秩比标准LoRA设置大30–100倍）。
- 平均GID与任务复杂度相关：WizardLM（≈404）、Code-Feedback（≈269）、MetaMathQA（≈178）。
- 训练过程中GID先快速增长后趋于稳定。



## 定位与知识库关联

本文方法属于参数高效微调（PEFT）领域中基于LoRA的改进路线。与现有方法的关系如下：

| 方法 | 核心思想 | 与本文关系 |
|------|---------|-----------|
| LoRA (Hu et al., 2022) | 低秩矩阵分解 | 基础方法，本文改进对象 |
| AdaLoRA (Zhang et al., 2023b) | 基于SVD重要性得分的自适应秩分配 | RaLoRA-Pro的损失敏感性策略受其启发 |
| MELoRA (Ren et al., 2024) | 迷你集成低秩适配器 | RaLoRA的块对角分解受其启发 |
| DoRA (Liu et al., 2024a) | 权重分解为幅度和方向 | 正交改进方向 |
| PiSSA (Meng et al., 2024) | 主奇异分量初始化 | 正交改进方向 |
| MoRA (Jiang et al., 2024) | 高秩更新 | 对比基线 |
| HiRA (未明确引用) | Hadamard积高秩 | 对比基线 |

本文的核心贡献在于首次将梯度本征维度（GID）的概念引入LoRA适配器设计，并提出了熵基估计器作为通用工具。该估计器与大多数现有LoRA变体正交，可作为插件工具用于广泛的PEFT方法。

**局限性**：
- 熵基GID估计器的有效性目前仍是经验性的，需要更广泛的理论分析。
- 仅探索了熵基估计器的三种具体应用（RaLoRA、RaLoRA-Pro和LoRA+GID）。
- 未在多模态大语言模型（MLLM）基准上进行评估。

**开放问题**：
- 熵基GID估计器的严格理论分析是什么？
- 如何将熵基估计器与更多现有LoRA变体（如DoRA、PiSSA）及非LoRA PEFT方法（如Adapter、Prefix Tuning）集成？
- RaLoRA和RaLoRA-Pro在多模态任务上的表现如何？
- GID在训练过程中的动态变化如何影响最优秩分配策略？是否可以在训练过程中动态调整秩？
- RaLoRA-Pro中的损失敏感性计算是否对噪声敏感？是否有更稳健的层重要性度量？



## 原文 PDF

![[paperPDFs/ICLR_2026/Gradient_Intrinsic_Dimensionality_AlignmentNarrowing_The_Gap_Between_Low_Rank_Adaptation_and_Full_Fine_Tuning.pdf]]
