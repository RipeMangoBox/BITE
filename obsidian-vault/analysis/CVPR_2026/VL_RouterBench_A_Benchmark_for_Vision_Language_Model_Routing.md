---
title: "VL-RouterBench: A Benchmark for Vision-Language Model Routing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VL_RouterBench_A_Benchmark_for_Vision_Language_Model_Routing.pdf
project_link: null
code_link: "https://github.com/LLaVA-VL/LLaVA-NeXT"
aliases:
- VR
- VL-RouterBench
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过软标签训练中的成本惩罚参数λ可以精细调节路由器在精度与成本之间的偏好，同时多模态融合方式（如归一化拼接）直接影响路由决策的准确性和成本效率。
primary_logic: 尽管当前最佳路由器（如RouterDC）以仅约最强单模型三分之一成本达到相近精度，证明了多模型路由的价值；但与Oracle相比仍有显著差距，表明通过改进跨模态表示和路由器架构存在大幅提升空间。
claims:
- RouterDC在Rank Score上达到74.59±1.05，而Oracle可达93.68，两者差距明显。
- 调节λ从0到∞可连续控制路由器精度–成本权衡，例如λ=100时MLP路由器的Avg. Acc.为77.49%，Avg. Cost为1.13 $/10K，相较最强单模型降低约58%的成本。
- 归一化拼接（Normalize-Concat）融合方式在Rank Score（74.05）上显著优于拼接（72.06）和加权平均（70.33）等其他融合方式。
- 文本和视觉编码器的维度越高，路由器的Rank Score表现越好；多模态融合优于纯文本或纯视觉路由器。
---

# VL-RouterBench: A Benchmark for Vision-Language Model Routing

> [!tip] 核心洞察
> 尽管当前最佳路由器（如RouterDC）以仅约最强单模型三分之一成本达到相近精度，证明了多模型路由的价值；但与Oracle相比仍有显著差距，表明通过改进跨模态表示和路由器架构存在大幅提升空间。

| 字段 | 内容 |
|------|------|
| 中文题名 | VL-RouterBench：视觉语言模型路由基准 |
| 英文题名 | VL-RouterBench: A Benchmark for Vision-Language Model Routing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.23562) · [Code](https://github.com/LLaVA-VL/LLaVA-NeXT) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VL-RouterBench（视觉语言模型路由基准） |
| Dataset | VL-RouterBench |

> [!tip] 效果简介
> - VL-RouterBench (All Datasets) 上，Rank Score (↑) 74.23±0.22 (MLP + Soft Label λ=100) vs 68.88 (Strongest) (+5.35)；Avg. Acc. (%) / Avg. Cost ($/10K) 77.49±0.56 / 1.13±0.13 (MLP) vs 78.01 / 2.72 (Strongest) (精度-0.52% / 成本-58.5%)；Avg. Acc. (%) 78.09±1.17 (VLC) vs 78.01 (Strongest) (+0.08%)。

## 概要

视觉语言模型（VLM）的快速迭代使得“为每个输入选择最合适模型”的路由问题日益重要，但该领域长期缺乏统一、可复现的基准。**VL-RouterBench** 首次构建了覆盖14个数据集、30,540个样本、17个模型（15个开源+2个API）的系统性基准，从原始推理与评分日志中提取519,180个样本–模型对的质量矩阵和成本矩阵，并设计了从数据准备、路由器训练到评估的完整管道。

**核心瓶颈**在于：当前最佳路由器（如 **RouterDC**）虽能以仅约最强单模型三分之一成本（Avg. Cost $1.13 vs $2.72 per 10K）达到相近精度（Avg. Acc. 77.49% vs 78.01%），但与理想上界 **Oracle** 之间仍存在显著差距（Rank Score 74.59 vs 93.68），表明现有方法未能充分利用细粒度视觉线索和跨模态对齐信号。

**方法定位**上，VL-RouterBench 并非提出全新路由架构，而是提供了标准化的评估框架和可控的精度–成本权衡机制。其关键创新在于引入**指数衰减成本软标签策略**：通过超参数 $\lambda$ 连续调节路由器对低成本模型的偏好，公式化为

$$t_i^{(\lambda)}(j) = \frac{\mathbf{1}\{Y_{i,j}=1\} \cdot \exp(-\lambda \cdot C_{i,j})}{\sum_{j:Y_{i,j}=1} \exp(-\lambda \cdot C_{i,j})}$$

并结合归一化精度与成本的调和平均 **Rank Score** 作为统一评价指标。基准支持特征级路由器（KNN、MLP等）和端到端路由器（RouterDC、VLC等）的公平比较，且可扩展至新数据集和模型。

**主要结果**：在 $\lambda=100$ 设置下，MLP+软标签路由器的 Rank Score 达到 74.23，较 Strongest 基线（68.88）提升 5.35 分；端到端 VLC 路由器在 Avg. Acc. 上以 78.09% 超越最强单模型（78.01%）。消融实验揭示：归一化拼接融合（Normalize-Concat）显著优于普通拼接和加权平均，LXMERT 作为多模态骨干优于 VisualBERT 和单模态 BERT，且提高文本/视觉嵌入维度可有效提升路由性能。这些发现共同指向一个明确方向——**通过改进跨模态表示和路由器架构，VLM路由存在大幅提升空间**。

### 视觉语言模型部署中的路由困境

大规模视觉语言模型（VLM）的快速迭代使得模型选择成为部署中的核心难题。不同VLM在精度、成本和推理速度上呈现显著差异——以VL-RouterBench所覆盖的15个开源模型和2个API模型为例，参数量从数十亿到数百亿不等，单次推理成本可相差数倍，且没有任何单一模型能在所有视觉任务上同时取得最优精度与最低成本。实际部署中，用户往往只能“押注”一个最强模型（Strongest）或最便宜模型（Cheapest），前者带来不必要的推理开销，后者则可能因精度不足导致下游任务失败。

### 路由器的现有方案与关键缺口

模型路由（Model Routing）为上述困境提供了系统性的解决方案：通过学习一个轻量路由器，对每个输入样本动态选择最合适的模型，从而在精度与成本之间取得更优权衡。近年来，从基于特征级分类器（如KNN、MLP、线性分类器）到端到端训练的路由器（如**RouterDC** (Chen et al., 2024) 的双对比学习框架、**ZOOTER** (Lu et al., 2023) 的变换器微调策略、**VLC** (Sakota et al., 2024) 的LXMERT多模态分类），多种路由方法已在纯文本LLM路由中展现出潜力。

然而，将这些方法迁移到VLM路由场景时，存在两个关键缺口：

1. **缺乏统一、可复现的基准**。现有路由研究各自构建评估设置，数据集、模型池、成本模型和评价指标均不统一，导致方法间的公平比较几乎不可能，也阻碍了路由策略的系统性改进。
2. **跨模态路由信息利用不足**。现有路由器大多将多模态输入简单拼接或仅依赖单模态特征，未能充分利用细粒度视觉线索和跨模态对齐信号。这导致当前最佳路由器与理想Oracle之间存在明显的性能差距——如Table 2所示，RouterDC的Rank Score为74.59±1.05，而Oracle可达93.68，两者间有近20分的鸿沟。

### 本文动机与核心贡献

针对上述缺口，本文提出**VL-RouterBench**，一个面向VLM路由的系统性基准。其设计围绕三个核心目标：

- **标准化评估**：基于14个数据集、30,540个样本和17个VLM的推理日志，构建统一的精度-成本矩阵（共519,180个样本-模型对，总token量34,494,977），并采用Rank Score（归一化精度与成本的调和平均）作为单一排序指标，实现可复现的公平比较。
- **可控的精度-成本权衡**：引入指数衰减软标签训练策略，通过单一超参数λ连续调节路由器对精度与成本的偏好，使同一路由器架构可生成完整的Pareto前沿，满足不同部署场景的需求。
- **揭示改进空间**：通过系统消融实验，量化多模态融合方式、编码器维度和骨干架构对路由性能的影响，明确指出当前路由方法与Oracle之间的差距主要源于跨模态表示能力的不足，为后续研究提供了明确方向。

## 核心方法与创新机理

VL-RouterBench 的核心创新并非提出一种全新的路由器架构，而是构建了首个面向视觉语言模型（VLM）路由的统一、可复现基准，并引入了一套**精度–成本感知的软标签训练策略**，从根本上改变了路由器的训练目标与行为。

### 精度–成本感知软标签训练

传统路由器训练通常采用硬标签交叉熵损失，仅对“正确”模型给予概率质量，完全忽略不同正确模型之间的成本差异。VL-RouterBench 的**核心 changed slot**在于训练目标的重新设计：将路由问题形式化为带约束的多目标优化，并通过求解拉格朗日对偶问题，导出解析形式的**指数衰减软标签**。

具体而言，对于每个样本 $x_i$，软标签目标定义为：

$$t_i^{(\lambda)}(j) = \frac{\mathbf{1}\{Y_{i,j}=1\} \cdot \exp(-\lambda \cdot C_{i,j})}{\sum_{j:Y_{i,j}=1} \exp(-\lambda \cdot C_{i,j})}$$

其中 $Y_{i,j}=1$ 表示模型 $m_j$ 对样本 $x_i$ 回答正确，$C_{i,j}$ 为该模型在此样本上的推理成本（由输入/输出 token 数乘以对应单价计算）。该软标签仅在正确模型集合内分配概率质量，并通过指数衰减函数 $\exp(-\lambda C)$ 对高成本模型施加惩罚。路由器随后通过最小化软标签交叉熵损失进行训练：

$$\mathcal{L}_{\mathrm{soft}}(\theta;\lambda) = \frac{1}{|\mathcal{D}_{\mathrm{tr}}|} \sum_i \sum_j t_i^{(\lambda)}(j)(-\log \pi_\theta(m_j \mid x_i))$$

超参数 $\lambda \in [0, \infty)$ 是这一创新的**因果调节旋钮**：$\lambda=0$ 时软标签退化为正确模型间的均匀分布（仅追求精度）；$\lambda \to \infty$ 时软标签将全部概率质量集中于成本最低的正确模型（极端偏好低成本）。通过连续调节 $\lambda$，同一路由器可以在精度–成本平面上描绘出一条完整的 Pareto 前沿，实现从“最强精度”到“最低成本”的平滑可控权衡。

### 相较于 Baseline 的关键差异

| 维度 | 传统路由器训练 | VL-RouterBench 软标签策略 |
|------|---------------|--------------------------|
| 训练目标 | 硬标签交叉熵（仅区分正确/错误模型） | 软标签交叉熵（在正确模型内按成本加权） |
| 成本感知 | 无，训练阶段不感知推理成本 | 通过 $\lambda$ 参数化成本惩罚，训练阶段即内化权衡 |
| 权衡控制 | 固定策略，无法动态调节 | 单次训练后可通过 $\lambda$ 连续调节精度–成本偏好 |
| 理论依据 | 经验性设计 | 从拉格朗日对偶优化导出，具有解析最优性保证 |

这一软标签策略使得路由器在训练阶段就学会了“在多个能正确回答的模型中，优先选择成本更低的那个”——这正是路由系统的核心价值所在。实验证据表明，当 $\lambda=100$ 时，MLP 路由器以仅 $1.13 的 Avg. Cost（相比最强单模型的 $2.72 降低约 58.5%）达到 77.49% 的 Avg. Acc.，仅比最强单模型损失 0.52 个百分点精度（Table 2）。这种以极小精度代价换取大幅成本压缩的能力，直接源于软标签训练对成本信号的显式建模。

### 基准系统化设计的创新

除训练策略外，VL-RouterBench 在基准构建层面也做出了关键贡献：首次将 VLM 路由评估标准化为**数据准备–路由器训练–路由器评估**的完整管道（Figure 2），覆盖 14 个数据集、30,540 样本、17 个模型，并引入 Rank Score（归一化成本与精度的调和平均）作为单一排序指标，解决了此前路由研究缺乏统一评价标准的核心瓶颈。

VL-RouterBench 提出了一套完整的视觉语言模型路由评估管线，将路由问题形式化为一个带成本约束的精度最大化任务，并围绕三个核心模块构建：路由器数据准备（Router Data Preparation）、路由器训练（Router Training）和路由器评估（Router Evaluation），如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2754_https_arxiv_org_abs_2512_23562/figures/002_Figure_2.jpg]]
*Figure 2: We propose VL-RouterBench to systematically assess the overall performance of vision-language model routing strategies. The three diagrams on the left, middle, and right represent Router Data Preparation (Sec. 3.2), Router Training (Sec. 3.3), and Router Evaluation (Sec. 3.4), respectively*

**问题形式化。** 给定一个样本 $x_i$，路由器 $R_\theta$ 输出一个模型选择分布 $\pi_\theta(\cdot \mid x_i)$，最终决策为：

$$R_{\theta,i} = \operatorname*{argmax}_{j} \pi_{\theta}(m_j \mid x_i)$$

训练目标联合最小化性能风险与期望成本：

$$\min_\theta \mathbb{E}[-Y_{i,R_{\theta,i}}] + \lambda \mathbb{E}[C_{i,R_{\theta,i}}]$$

其中 $Y_{i,j} \in \{0,1\}$ 表示模型 $j$ 对样本 $i$ 是否正确，$C_{i,j}$ 为推理该样本的货币成本（按输入/输出 token 计价，见 Eq. (3)），超参数 $\lambda \ge 0$ 控制精度与成本的权衡强度。

**模块一：路由器数据准备。** 该模块从 VLMEvalKit 的原始推理和评分日志中提取样本-模型对的质量矩阵 $Y$ 和成本矩阵 $C$，并按照 7:1:2 的比例划分训练/验证/测试集。整个基准覆盖 14 个数据集、30,540 个样本、15 个开源模型和 2 个 API 模型，共产生 519,180 条样本-模型记录，总 token 量达 34,494,977（见 Abstract 和 Section 4.1）。数据集的分布见 Figure 3，分为 General、STEM 和 Charts OCR 三个任务组。

**模块二：路由器训练。** 为解决 Eq. (2) 中的多目标优化问题，VL-RouterBench 引入精度-成本感知的软标签策略。通过拉格朗日对偶推导出解析形式的软标签目标：

$$t_i^{(\lambda)}(j) = \frac{\mathbf{1}\{Y_{i,j}=1\} \cdot \exp(-\lambda \cdot C_{i,j})}{\sum_{j:Y_{i,j}=1} \exp(-\lambda \cdot C_{i,j})}$$

该软标签仅在正确回答的模型上分配非零概率，并通过指数衰减函数 $\exp(-\lambda C_{i,j})$ 对高成本模型施加惩罚。路由器通过最小化软标签交叉熵损失进行训练：

$$\mathcal{L}_{\mathrm{soft}}(\theta;\lambda) = \frac{1}{|\mathcal{D}_{\mathrm{tr}}|} \sum_i \sum_j t_i^{(\lambda)}(j)(-\log \pi_\theta(m_j \mid x_i))$$

调节 $\lambda$ 即可连续控制路由器的精度-成本偏好：$\lambda=0$ 时仅追求精度，$\lambda \to \infty$ 时退化为仅选择最便宜的正确模型（若无正确则选全局最便宜模型）。

**模块三：路由器评估。** 评估协议在测试集上同时测量三个指标：平均精度（Avg. Acc., %）、平均成本（Avg. Cost, $/10K 样本）和吞吐量（Throughput, #K tokens/s）。为综合排名，引入归一化成本 $C_{\mathrm{norm}}$ 与平均精度 $\bar{A}$ 的调和平均——Rank Score：

$$S(\beta) = \frac{(1+\beta) \cdot \bar{A} \cdot C_{\mathrm{norm}}}{\beta \cdot \bar{A} + C_{\mathrm{norm}}}$$

其中 $\beta$ 控制精度与成本的相对重要性（默认 $\beta=0.1$ 偏重精度）。此外，通过拟合不同 $\lambda$ 下路由器的精度-成本 Pareto 前沿（见 Figure 4），可直观比较各类方法在精度-成本平面上的权衡表现。

**输入输出流总结。** 整体管线以 VLMEvalKit 的推理日志为输入，经过质量/成本矩阵构建、软标签训练、多指标评估三个环节，最终输出路由器的 Rank Score 排名、精度-成本散点分布及 Pareto 前沿，形成从数据到决策的闭环评估体系。

### 路由决策的形式化

VL-RouterBench 将 VLM 路由定义为一个条件选择问题。给定一个样本 $x_i$，路由器参数化地输出一个模型选择分布 $\pi_{\theta}(\cdot \mid x_i)$，最终的路由决策为：

$$R_{\theta,i} = \operatorname*{argmax}_{j} \pi_{\theta}(m_j \mid x_i)$$

其中 $m_j$ 为候选 VLM 模型池中的第 $j$ 个模型。路由器的训练目标是一个带约束的多目标优化问题，联合最小化性能风险与期望成本：

$$\min_\theta \mathbb{E}[-Y_{i,R_{\theta,i}}] + \lambda \mathbb{E}[C_{i,R_{\theta,i}}]$$

这里 $Y_{i,j} \in \{0,1\}$ 表示模型 $m_j$ 在样本 $x_i$ 上是否正确，$C_{i,j}$ 为调用成本，超参数 $\lambda \ge 0$ 控制精度与成本之间的权衡强度。

### 成本矩阵构建

单样本调用成本 $C_{i,j}$ 基于公开云平台 Together.ai 的定价标准，由输入和输出的 token 数量与对应单价线性组合计算：

$$C_{i,j} = n_{i,j}^{\mathrm{in}} \cdot c_j^{\mathrm{in}} + n_{i,j}^{\mathrm{out}} \cdot c_j^{\mathrm{out}}$$

其中 $n_{i,j}^{\mathrm{in}}$、$n_{i,j}^{\mathrm{out}}$ 分别为模型 $m_j$ 处理样本 $x_i$ 时消耗的输入和输出 token 数，$c_j^{\mathrm{in}}$、$c_j^{\mathrm{out}}$ 为对应单价。所有模型的定价基于模型参数量估算，确保跨模型成本比较的透明性和可复现性（见 Table 1）。

### 精度–成本感知软标签策略

这是本工作的核心方法创新。传统路由器使用硬标签（仅对正确模型赋予概率 1）进行训练，无法在训练阶段显式建模成本偏好。VL-RouterBench 提出从 Lagrangian 优化问题中推导出解析形式的软标签目标，将精度–成本权衡直接编码到训练信号中。

软标签 $t_i^{(\lambda)}(j)$ 仅对正确回答样本的模型分配非零概率，并通过成本衰减函数 $g_\lambda(\cdot)$ 调节权重：

$$t_i^{(\lambda)}(j) = \frac{\mathbf{1}\{Y_{i,j}=1\} \cdot g_{\lambda}(C_{i,j})}{\sum_{j:Y_{i,j}=1} g_{\lambda}(C_{i,j})}$$

实际采用指数衰减函数 $g_\lambda(c) = \exp(-\lambda \cdot c)$，得到最终软标签形式：

$$t_i^{(\lambda)}(j) = \frac{\mathbf{1}\{Y_{i,j}=1\} \cdot \exp(-\lambda \cdot C_{i,j})}{\sum_{j:Y_{i,j}=1} \exp(-\lambda \cdot C_{i,j})}$$

$\lambda$ 的作用机制清晰：$\lambda=0$ 时所有正确模型等权，路由器仅追求精度；$\lambda \to \infty$ 时软标签退化为仅选择最低成本正确模型，趋近 Cheapest 行为。这一设计使路由器在训练阶段即可通过调节单一超参数连续控制精度–成本偏好，无需后处理重排或阈值调节。

训练损失为软标签与路由器输出分布之间的交叉熵：

$$\mathcal{L}_{\mathrm{soft}}(\theta;\lambda) = \frac{1}{|\mathcal{D}_{\mathrm{tr}}|} \sum_i \sum_j t_i^{(\lambda)}(j)(-\log \pi_\theta(m_j \mid x_i))$$

### 评估指标：Rank Score

为将精度和成本统一为单一排序指标，VL-RouterBench 采用归一化成本 $C_{\mathrm{norm}}$ 与平均精度 $\bar{A}$ 的加权调和平均：

$$S(\beta) = \frac{(1+\beta) \cdot \bar{A} \cdot C_{\mathrm{norm}}}{\beta \cdot \bar{A} + C_{\mathrm{norm}}}$$

其中 $\beta$ 控制精度对成本的相对权重，默认 $\beta=0.1$ 偏重精度。归一化成本 $C_{\mathrm{norm}}$ 将原始平均成本线性映射到 $[0,1]$ 区间，使得与精度在同一尺度上可比。该指标同时惩罚低精度和高成本，能够有效区分仅追求精度或仅追求成本的路由器。

### 管道模块概览

整个基准由三个顺序模块构成（见 Figure 2）：

1. **路由器数据准备**：从 VLMEvalKit 提取各模型在各数据集上的推理和评分日志，构建样本–模型对的质量矩阵 $Y$ 和成本矩阵 $C$，并按数据集分层划分训练/验证/测试集。
2. **路由器训练**：使用上述软标签损失训练特征级路由器（如 MLP、Linear）或端到端路由器（如 RouterDC、VLC），通过调节 $\lambda$ 控制精度–成本权衡。
3. **路由器评估**：在测试集上测量平均精度、平均成本和吞吐量，计算 Rank Score，并拟合精度–成本 Pareto 前沿以可视化不同工作点的权衡关系。

## 实验与关键发现

### 核心结果：路由精度–成本权衡

VL-RouterBench 在 14 个数据集、30,540 个样本、17 个模型（15 开源 + 2 API）上评估了 13 种路由方法。核心发现是：当前最优路由器 **RouterDC** 以仅约最强单模型三分之一的成本，达到了相近的精度，但与 Oracle 上界之间仍存在显著差距，表明跨模态路由存在大幅提升空间。

**Table 2** 汇总了各路由器的综合表现。Oracle 作为理想上界，Rank Score 高达 93.68，而最强学习型路由器 RouterDC 的 Rank Score 为 74.59±1.05，两者差距约 19 个百分点。这一差距的根源在于：当前路由器未能充分利用细粒度视觉线索和跨模态对齐信号。

在精度–成本的具体权衡上：
- **MLP + 软标签（λ=100）** 达到平均精度 77.49%±0.56，平均成本 1.13 $/10K，相较最强单模型（精度 78.01%，成本 2.72 $/10K）仅损失 0.52% 精度，却节省了约 58.5% 的成本。
- **VLC**（基于 LXMERT 的端到端路由器）在精度上表现最佳，达到 78.09%±1.17，甚至略超最强单模型的 78.01%，但成本为 2.50 $/10K，节省幅度有限。

**Figure 1** 的精度–成本散点图直观展示了这一格局：RouterDC、VLC、MLP 三个顶级路由器的运行点均位于单模型 Pareto 前沿的左上方，但距离 Oracle 仍有明显距离。

### 软标签 λ 的调控作用

软标签训练中的成本惩罚参数 λ 是实现精度–成本可控权衡的关键旋钮。**Figure 4** 展示了不同 λ 下各路由器在精度–成本平面上的 Pareto 前沿：

- λ=0 时，软标签退化为对所有正确模型均匀分配概率，路由器追求最高精度，成本较高。
- λ 增大时，低成本正确模型获得更高软标签权重，路由器向低成本方向移动。
- λ→∞ 时，路由器退化为仅选择最便宜模型，精度大幅下降。

**Table 2** 中 MLP 路由器在不同 λ 下的表现量化了这一趋势：λ=0 时精度 79.25%、成本 2.32 $/10K；λ=100 时精度 77.49%、成本 1.13 $/10K；λ=∞ 时精度降至 59.32%、成本仅 0.47 $/10K。附录 Tables A3–A8 提供了各 λ 值下按数据集细分的完整结果。

### 多模态融合与骨干网络消融

**Table 3** 的融合方法消融表明，**归一化拼接（Normalize-Concat）** 在 Rank Score 上达到 74.05，显著优于普通拼接（72.06）和加权平均（70.33）。这一结果揭示：在将文本和视觉嵌入拼接前先进行归一化，可有效缓解模态间尺度不匹配对路由决策的干扰，是提升跨模态路由性能的关键设计选择。

**Table 4** 的端到端骨干网络消融进一步验证了多模态建模的必要性：
- **LXMERT** 作为骨干时 Rank Score 最高（71.36），优于 VisualBERT（65.32）。
- 纯文本 BERT-base 仅达 64.55，纯视觉 ViT 表现更差。
- 这表明有效的跨模态融合对路由决策至关重要，单模态信息不足以捕捉 VLM 路由所需的细粒度质量信号。

**Figure 5** 和 **Section 5.3** 进一步显示，提高文本和视觉编码器的嵌入维度可有效提升路由器 Rank Score，印证了高维表示对捕获路由相关特征的价值。

### 失败模式与泛化分析

**附录 Figure A3** 按路由难度分层分析了各路由器的精度分布。当样本的正确模型数量 |Sᵢ| 较小时（即只有少数模型能正确回答），路由难度高，所有路由器的精度均显著下降，与 Oracle 的差距最大。这暴露了当前路由器的核心失败模式：在模型间质量差异微妙的困难样本上，路由器难以精确判别最优模型。

**附录 Table A2** 的分布外（OOD）泛化实验表明，路由器在训练集外数据集上的 Rank Score 普遍下降，但相对排序基本保持。RouterDC 在 OOD 设置下仍维持领先，但绝对性能的下降说明当前路由器对训练分布存在一定依赖，对新增数据集或模型池变化的鲁棒性仍需提升。

### 多成本约束框架

**附录 Table A1** 探索了同时考虑推理成本和显存占用的多成本路由框架。结果显示，引入额外成本维度后，路由器的精度–综合成本权衡仍然有效，但不同路由器对多成本约束的敏感度存在差异，这为实际部署中的多目标路由优化提供了初步参考。

![[assets/figures/papers/paper_list_l2754_https_arxiv_org_abs_2512_23562/figures/001_Figure_1.jpg]]
*Figure 1: Overall performance comparison on VL-RouterBench. The xaxis and y-axis are Average Cost (Avg. Cost, $/10K samples) and Average Accuracy (Avg. Acc., %), respectively. Gray dots denote the performance of single models at different costs, and “Strongest” and “Cheapest” mark the baselines that use only the strongest or the cheapest model. The gray dashed curve depicts the Pareto frontier fitted from these single-model points (only models near the frontier are shown for clarity). “1st RouterDC”, “2nd VLC”, and “3rd MLP” indicate the top three routers by Rank Score. Points closer to the upper left reflect a better accuracy–cost trade-off. The results show that even advanced routers still have a n...*

![[assets/figures/papers/paper_list_l2754_https_arxiv_org_abs_2512_23562/figures/008_Table_3.jpg]]
*Table 3: Performance comparison of different fusion methods on MLP with λ = 100. The best and second-best results are highlighted in bold and underlined, respectively. Other settings are the same as in Table 2. Results are presented as mean and standard deviation across 5 independent trials*

![[assets/figures/papers/paper_list_l2754_https_arxiv_org_abs_2512_23562/figures/009_Table_4.jpg]]
*Table 4: Performance comparison of different backbones on VLC using λ = 100. The best and second-best results are highlighted in bold and underlined, respectively. Other settings are the same as in Table 2. Results are presented as mean and standard deviation across 5 independent trials*

![[assets/figures/papers/paper_list_l2754_https_arxiv_org_abs_2512_23562/figures/007_Figure_5.jpg]]
*Figure 5: Performance comparison of different text and visual encoders paired on MLP with λ = 100. The brackets indicate the dimension of the encoder’s output embedding. Other settings are the same as in Table 2*

![[assets/figures/papers/paper_list_l2754_https_arxiv_org_abs_2512_23562/figures/012_Table.jpg]]
*Table: A1. Performance comparison of top routers on VL-RouterBench under multi-cost framework. Other settings are the same as in Tab. 2*

## 定位与知识库关联

### 1. 路由范式定位：从LLM路由到多模态VLM路由

VL-RouterBench 的工作建立在语言模型路由（LLM routing）的研究谱系之上，但将其系统性地拓展到视觉语言模型的跨模态场景。在LLM领域，已有路由方法主要分为两类：

- **特征级路由器（Feature-level routers）**：通过预训练的文本编码器提取样本表征，再训练轻量分类器进行模型选择。典型代表包括 **KNN**、**PRkNN**、**OVR**、**K-means**、**Linear** 和 **MLP**。这类方法的核心假设是：语义相似的问题适合由同一模型回答。
- **端到端路由器（End-to-end routers）**：在路由训练过程中同时更新编码器参数，使表征更适配路由任务。代表性工作包括 **CosineCls** 和 **RouterDC**，其中 RouterDC 采用双对比学习框架；以及 **ZOOTER**和 **VLC**，后者基于 LXMERT 多模态骨干进行微调。

VL-RouterBench 的贡献在于：将这些路由范式从纯文本域迁移至视觉语言域，并揭示了**跨模态融合质量是VLM路由性能的关键瓶颈**。实验表明，多模态路由器（如 VLC 的 Rank Score 71.36）显著优于纯文本路由器（如 BERT 骨干的 64.55），而不同融合策略之间也存在显著差异——归一化拼接（Normalize-Concat）的 Rank Score 达 74.05，远超普通拼接（72.06）和加权平均（70.33）（Table 3, Table 4）。

### 2. 训练策略谱系：从硬标签到成本感知软标签

传统路由方法（包括上述所有基线）通常采用硬标签训练，即仅对“正确”模型分配概率1，损失函数为标准的交叉熵。这一策略忽略了两个关键事实：（1）一个样本可能被多个模型正确回答；（2）不同模型的推理成本差异巨大。

VL-RouterBench 提出的**精度-成本感知软标签策略**（Section 3.3, Eq. 5-7）改变了这一范式。其核心机制是：通过拉格朗日优化推导出解析形式的软标签目标——

$$t_i^{(\lambda)}(j) = \frac{\mathbf{1}\{Y_{i,j}=1\} \cdot \exp(-\lambda \cdot C_{i,j})}{\sum_{j:Y_{i,j}=1} \exp(-\lambda \cdot C_{i,j})}$$

该公式仅对正确回答的模型赋予非零概率，并以指数衰减函数 $\exp(-\lambda C_{i,j})$ 惩罚高成本模型。超参数 $\lambda$ 构成一个**连续可调的精度-成本权衡旋钮**：$\lambda=0$ 时等价于均匀软标签（仅追求精度），$\lambda \to \infty$ 时退化为仅选择最廉价正确模型（类似 Cheapest 基线）。

这一设计使得同一路由器架构可以产出整条 Pareto 前沿（Figure 4），而非单一工作点。例如，MLP 路由器在 $\lambda=100$ 时达到 Rank Score 74.23，平均精度 77.49% 的同时将成本降至 1.13 \$/10K（相较最强单模型降低成本约 58.5%）（Table 2）。

### 3. 评估体系定位：从单维度到多维度联合评价

现有LLM路由工作通常仅报告精度或胜率，缺乏对成本的系统性考量。VL-RouterBench 引入的 **Rank Score** 评价指标（Eq. 11）将归一化成本与平均精度通过调和平均结合：

$$S(\beta) = \frac{(1+\beta) \cdot \bar{A} \cdot C_{\mathrm{norm}}}{\beta \cdot \bar{A} + C_{\mathrm{norm}}}$$

其中 $\beta=0.1$ 默认偏重精度。这一设计使得不同路由器可在统一的精度-成本平面上进行公平比较，而非仅凭单一维度排序。

### 4. 适用边界与已知局限

**适用边界**：
- 基准覆盖 14 个数据集、30,540 样本、15 个开源模型和 2 个 API 模型，任务类型涵盖通用VQA、STEM推理和图表OCR三类（Figure 3），对当前主流VLM能力空间有较好覆盖。
- 路由器训练和评估均基于固定模型池和静态数据集划分，适用于离线批量路由场景。

**明确局限**（需人工验证的边界）：
- **输入模态限制**：当前基准仅支持单图像样本，未扩展到多图像输入或多轮对话场景。这限制了其在真实多模态对话系统（如视觉对话、多图推理）中的适用性。
- **评价维度限制**：评估依赖规则化的正确性判断（如精确匹配或选择题答案比对），未涵盖开放式生成质量、主观偏好等更复杂的评价维度。
- **泛化能力未充分验证**：路由器仅在训练集内的模型和数据上评估。对新增模型（如新发布的开源VLM）或分布偏移数据（OOD）的泛化能力，仅在附录 Table A2 中做了初步探索（在3个held-out数据集上测试），但系统性研究仍然缺失。
- **部署效率分析不完整**：吞吐量测量受限于路由器具体实现，未系统对比不同部署环境（如不同GPU、批处理策略）下的延迟和资源消耗。

### 5. 开放问题与后续工作方向

基于当前方法-性能差距和局限分析，以下方向值得后续探索：

1. **细粒度跨模态路由**：当前最佳路由器（RouterDC, Rank Score 74.59）与 Oracle（93.68）之间仍有显著差距（Table 2）。论文明确指出，这一差距暗示通过利用更细粒度的视觉区域特征和文本结构信息，以及建模VLM内部层间行为，存在大幅提升空间。

2. **动态模型池适应**：能否通过主动学习或在线更新机制，让路由器在模型池变化（新模型加入、旧模型退出、模型版本更新）时无需完全重训练即可适应？

3. **多成本约束路由**：当前路由仅考虑API调用成本（基于token计费）。实际部署中还需考虑显存占用、推理延迟、并发吞吐等资源约束。如何设计支持多成本维度的路由决策框架仍是一个开放问题。

4. **开放式任务评价**：对于开放式视觉问答、图像描述生成等主观性强的任务，如何设计有效的路由评价指标（超越简单的规则化正确性判断）？

5. **多图像与交互式场景扩展**：将基准扩展至多图像输入（如视频理解、多图对比）和交互式场景（如多轮视觉对话），是推动VLM路由走向实际应用的关键一步。

## 原文 PDF

![[paperPDFs/CVPR_2026/VL_RouterBench_A_Benchmark_for_Vision_Language_Model_Routing.pdf]]
