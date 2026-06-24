---
title: "Test-Time Optimization of 3D Point Cloud LLM via Manifold-Aware In-Context Guidance and Refinement"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Test_Time_Optimization_of_3D_Point_Cloud_LLM_via_Manifold_Aware_In_Context_Guidance_and_Refinement.pdf
openreview_forum_id: qsra0EsUpe
aliases:
- PGLP
- TTO3PCLMACGR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过引入测试时数据流形结构构建KNN图，利用图邻居的文本描述作为上下文示例（in-context guidance），并结合图上标签传播（label propagation）对LLM输出的置信度进行平滑修正，从而提升分类与OOD检测的鲁棒性。"
primary_logic: "测试样本的歧义可通过其流形邻居的语义一致性来消解；将LLM推理从孤立样本扩展到局部邻域，并通过图传播机制校准置信度，可在不重新训练的情况下显著提升3D理解性能。"
claims:
- "提出的PGLLM框架在ModelNet40和ShapeNetCore的OOD检测任务中，平均AUROC分别达到85.9%和91.1%，显著超越所有基线方法。"
- "消融实验表明，同时使用in-context guidance与score propagation可获得最佳性能，二者具有互补和协同效应。"
- "提出的方法在仅使用低成本开源LLM（DeepSeek-V3）时，仍能以62.3%的平均分类准确率超越所有基于GPT-4的基线方法。"
- "ModelNet40 (OOD detection, MN1-MN3 average) 上 AUROC = 85.9"
---

# Test-Time Optimization of 3D Point Cloud LLM via Manifold-Aware In-Context Guidance and Refinement

> [!tip] 核心洞察
> 测试样本的歧义可通过其流形邻居的语义一致性来消解；将LLM推理从孤立样本扩展到局部邻域，并通过图传播机制校准置信度，可在不重新训练的情况下显著提升3D理解性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于流形感知上下文引导与优化的三维点云大语言模型测试时优化 |
| 英文题名 | Test-Time Optimization of 3D Point Cloud LLM via Manifold-Aware In-Context Guidance and Refinement |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=qsra0EsUpe); [GitHub](https://github.com/handsome999KK/PGLLM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Point-Graph LLM (PGLLM) |
| Dataset | ModelNet40 (OOD detection, MN1-MN3 average), ShapeNetCore (OOD detection, SN1-SN3 average), ModelNet40 (3D recognition), ModelNet40 (3D recognition with DeepSeek-V3) |

> [!tip] 效果简介
> - ModelNet40 (OOD detection, MN1-MN3 average) 上，AUROC 为 85.9，对比 80.0 (PointLLM)，变化 +5.9。
> - ShapeNetCore (OOD detection, SN1-SN3 average) 上，AUROC 为 91.1，对比 87.7 (PointLLM)，变化 +3.4。
> - ModelNet40 (3D recognition) 上，Average Accuracy 为 62.5，对比 60.9 (MiniGPT-3D)，变化 +1.6。

## 概述

### 问题瓶颈

现有三维多模态大语言模型（3D MLLM）在理解点云时面临一个关键瓶颈：**难以有效区分几何结构高度相似的三维形状**。当模型仅依赖单张独立点云进行推理时，类间混淆严重，导致分类与分布外（OOD）检测的可靠性不足。这一问题的根源在于，孤立样本的几何特征本身往往不具备足够的判别信息来消解语义歧义。

### 核心思路

本文提出 **Point-Graph LLM (PGLLM)**，一种无需重新训练的测试时优化框架。其核心洞察是：**测试样本的歧义可通过其流形邻居的语义一致性来消解**。具体而言，PGLLM 将 LLM 推理从孤立样本扩展到局部邻域，通过两个互补机制实现性能提升：

1. **流形感知的上下文引导（In-Context Guidance）**：利用预训练点云编码器构建 KNN 图，将查询样本在图上的近邻文本描述作为上下文示例，丰富第二阶段 LLM 的提示信息。
2. **基于图传播的分数细化（Score Refinement）**：引入标签传播算法，在图邻接结构上对 LLM 输出的置信度进行迭代平滑，校准初始预测。

### 方法定位

PGLLM 位于 **测试时优化（Test-Time Optimization）** 与 **上下文学习（In-Context Learning）** 的交叉点。与 PointLLM（Xu et al., 2024）、MiniGPT-3D（Tang et al., 2024）等直接使用单样本描述的方法不同，PGLLM 通过构建测试数据的流形图，将点云理解从“孤立推理”转变为“邻域协同推理”。在方法谱系上，它继承了图半监督学习中标签传播（Zhu & Ghahramani, 2002）的思想，并将其创造性地应用于 LLM 输出的后处理阶段。与 MCM（Ming et al., 2022）、NegLabel（Jiang et al., 2024a）等零样本 OOD 检测方法相比，PGLLM 不依赖额外的负标签或大规模预训练视觉-语言模型，而是充分利用测试数据自身的内在结构。

### 主要结果

PGLLM 在多个基准上取得了一致且显著的性能增益：

- **OOD 检测**：在 ModelNet40 和 ShapeNetCore 上，平均 AUROC 分别达到 **85.9%** 和 **91.1%**，较 PointLLM 基线分别提升 +5.9 和 +3.4 个百分点（Table 1）。
- **三维识别**：使用 GPT-4 时平均准确率达 **62.5%**；即使采用低成本开源模型 DeepSeek-V3，仍以 **62.3%** 的准确率超越所有基于 GPT-4 的基线方法（Table 3）。
- **消融实验**：同时启用上下文引导与分数传播可获得最佳性能，二者具有互补与协同效应——仅上下文引导使 OOD 检测 AUROC 从 80.4 提升至 83.0，仅分数传播使 FPR95 从 100.0 大幅降至 62.0，二者结合后达到最优（Table 4）。
- **真实场景泛化**：在 S3DIS 真实世界基准上，PGLLM 在 OOD 检测和识别任务上均展现出稳定的性能优势（Figure 4）。

### 局限与展望

PGLLM 的有效性依赖于初始 PointLLM 生成描述的基本质量；当上下文示例包含不准确信息时，第二阶段评分可能产生偏差。此外，当前框架假设点云类别集合是已知且固定的，如何扩展到完全开放集场景仍需探索。图构建与分数传播机制在大规模室外 LiDAR 点云上的计算效率，以及与参数高效微调（如 LoRA）的结合潜力，也是值得进一步研究的方向。

## 背景与动机

三维点云理解是自动驾驶、机器人导航与增强现实等应用的核心感知能力。随着多模态大语言模型（MLLM）的快速发展，将点云数据与语言模型结合以实现开放词汇的3D理解已成为新兴范式。然而，现有3D MLLM面临一个关键瓶颈：**几何结构相似的三维点云难以被有效区分，导致严重的类间混淆，单张独立点云的推理可靠性不足**。

具体而言，当前方法（如**PointLLM**（Xu et al., 2024）和**MiniGPT-3D**（Tang et al., 2024））通常采用两阶段流水线——先用3D编码器提取特征并生成文本描述，再将描述送入LLM进行推理。这种范式将每个测试样本视为孤立个体，忽视了测试数据内部固有的流形结构。当面对外观相似但类别不同的点云时，LLM缺乏足够的上下文信息来做出准确判断，尤其在分布外（OOD）检测任务中，模型难以可靠地区分已知类别与未知类别。

这一观察揭示了一个可操作的因果调节变量：**测试样本的歧义可通过其流形邻居的语义一致性来消解**。如果能够利用测试数据自身的几何相似性结构，将孤立样本的推理扩展为局部邻域的协同推理，就有可能在无需重新训练的前提下显著提升3D理解性能。

基于上述动机，本文提出**Point-Graph LLM（PGLLM）**框架，核心思路是将LLM推理从孤立样本扩展到局部邻域，通过图上标签传播机制校准置信度。具体而言，PGLLM利用预训练点云编码器构建KNN图以捕获测试数据的流形结构，将图上邻居的文本描述作为上下文示例引导LLM推理（上下文引导），并引入基于标签传播的分数细化机制对LLM输出的置信度进行平滑修正。这一设计使得模型能够在测试时动态利用数据内在结构，从而提升分类与OOD检测的鲁棒性。

## 核心创新

PGLLM的核心创新在于将3D点云大语言模型的推理从**孤立样本**扩展到**测试时数据流形**，通过两个互补的机制——**上下文引导（In-Context Guidance）**与**分数传播细化（Score Refinement）**——在不重新训练模型的前提下显著提升下游任务性能。

### 关键瓶颈与因果抓手

现有3D多模态大语言模型（如PointLLM、MiniGPT-3D）面临的核心瓶颈是：**几何结构相似的三维点云难以被有效区分**，导致类间混淆严重，单张独立点云的推理可靠性不足。PGLLM的因果抓手在于利用测试样本在特征空间中的流形结构：通过构建KNN图捕获样本间的视觉相似性，将邻居样本的语义信息作为上下文注入LLM推理，并利用图上的标签传播对LLM输出的置信度进行平滑修正。

### Changed Slots：相对于基线的关键差异

PGLLM相对于现有3D-LLM基线（以PointLLM为代表）的核心改动体现在两个关键环节：

**1. 第二阶段LLM输入构建方式（In-Context Guidance）**

- **基线做法**：仅使用查询样本自身的PointLLM描述作为提示，LLM在孤立上下文中进行推理。
- **PGLLM做法**：在查询描述的基础上，从KNN图中检索该样本的K个最近邻，将其文本描述作为上下文示例（in-context demonstrations）附加到第二阶段LLM的提示中（Section 3.2）。这些邻居描述提供了流形上的语义锚点，帮助LLM消解歧义。

**2. LLM输出的后处理（Score Refinement）**

- **基线做法**：直接使用LLM输出的类别分数或置信度作为最终预测。
- **PGLLM做法**：引入基于标签传播（Label Propagation）的分数细化机制，在图邻接结构上对LLM的初始输出分数进行迭代平滑。具体更新规则为：
  $$S_t = \alpha S_{t-1} \tilde{W} + (1-\alpha) S_0$$
  其中 $\tilde{W}$ 为对称归一化的邻接矩阵，$S_0$ 为LLM初始输出，$\alpha$ 控制平滑强度（Section 3.3）。该机制使得语义一致的邻居之间分数相互增强，抑制孤立噪声。

### 互补与协同效应

消融实验（Table 4）提供了决定性证据，表明上述两个机制具有**互补和协同效应**：

- 仅使用In-Context Guidance时，ModelNet40 OOD检测的AUROC从80.4提升至83.0，FPR95从100.0降至71.0；
- 仅使用Score Propagation时，FPR95从100.0大幅降至62.0；
- **同时启用两者**时，ModelNet40上AUROC达到85.9、FPR95降至52.1，ShapeNetCore上AUROC达到91.1、FPR95降至29.6，均显著优于单独使用任一机制。

### 支持集构建的灵活性

PGLLM在支持集构建上提供了两种模式（Section 4.1），增强了方法的适用性：

- **PGLLM^T（转导式）**：当测试数据分布可获取时，直接使用所有测试样本构建支持图，充分利用测试时信息；
- **PGLLM^O（归纳式）**：使用外部数据集Objaverse（随机采样100K样本）构建支持图，适用于测试样本在线到达的场景。

### 方法可移植性

值得注意的是，PGLLM并不依赖昂贵的闭源API。实验表明，当使用低成本开源LLM（DeepSeek-V3）作为第二阶段模型时，PGLLM仍以62.3%的平均分类准确率超越所有基于GPT-4的基线方法（Table 3），证明了该框架的通用性和实用性。

## 整体框架

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_qsra0EsUpe/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed framework for PGLLM. After encoding the 3D test samples, the framework feeds them into PointLLM for caption generation and uses them to construct a KNN graph. Initial answers are then synthesized via LLM inference. Subsequently, leveraging relational structures within the KNN graph, we introduce an answer iteration mechanism to optimize performance on downstream tasks*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_qsra0EsUpe/figures/012_Figure_7.jpg]]
*Figure 7: Demonstrations of PGLLM. We propose PGLLM, an efficient and potent framework that integrates 3D-LLMs with Large Language Models, where the text on a light yellow background indicates content generated by PointLLM. Furthermore, we demonstrate its operational mechanisms across 3D recognition, 3D OOD detection and 3D object captioning tasks*

PGLLM (Point-Graph LLM) 是一个在测试时对三维点云大语言模型进行优化的框架，其核心思路是将LLM推理从孤立样本扩展到局部邻域，利用测试数据的流形结构来校准模型输出。整个pipeline由五个顺序模块构成，形成“编码-描述-构图-上下文引导-分数传播”的级联流程，如 Figure 2 所示。

**3D特征编码与描述生成。** 框架首先使用冻结的预训练点云编码器 Point-BERT 对所有测试样本提取嵌入向量 $p_i$。随后，这些点云被送入 PointLLM（Xu et al., 2024），以默认提示 “What is this?” 生成每个样本的文本描述 $c_i$。这一阶段为后续的图构建和上下文引导提供了语义基础。

**KNN图构建。** 基于嵌入向量的余弦相似度，框架构建一个K近邻图 $G = (V, E)$。边权重矩阵 $W$ 的构造遵循公式：

$$W_{ij} = \begin{cases} e_{ij} & \text{if } e_{ij} \in \text{Top}_K(\{e_{ij}\}_{j=1}^{N_u}) \\ 0 & \text{otherwise} \end{cases}, \quad \text{s.t. } e_{ij} = \frac{\langle p_i, p_j \rangle}{\|p_i\| \cdot \|p_j\|}$$

该图编码了点云之间的视觉相似性，边权重反映几何结构的邻近程度，是后续上下文检索和分数传播的结构基础。默认设置 $K=3$。

**上下文引导推理 (In-context Guidance)。** 对于每个查询样本 $x_i$，框架从图中检索其 $K$ 个最近邻，将这些邻居的文本描述作为上下文示例（in-context demonstrations）附加到第二阶段LLM的提示中。这一设计的因果机制在于：测试样本的歧义可通过其流形邻居的语义一致性来消解——当查询点云本身难以区分时，结构相似样本的描述为LLM提供了额外的判别线索。

**分数传播细化 (Score Refinement)。** LLM输出的初始类别置信度或OOD分数并非最终结果。框架引入基于标签传播的迭代平滑机制，在图邻接结构上对分数矩阵 $S$ 进行修正：

$$S_t = \alpha S_{t-1} \tilde{W} + (1-\alpha) S_0, \quad \tilde{W} = D^{-\frac{1}{2}} W D^{-\frac{1}{2}}, \quad D = \text{diag}(\sum_j W_{ij})$$

其中 $S_0$ 为LLM原始输出，$\tilde{W}$ 为对称归一化邻接矩阵，$\alpha=0.5$ 控制初始分数与传播分数的平衡，迭代次数 $T=5$。这一机制使得几何相似的样本倾向于获得一致的预测，有效抑制了孤立推理时的噪声波动。

**下游任务解码。** 针对不同任务，框架采用差异化的输出策略：对于三维识别，LLM输出类别分数经传播后取最大值；对于OOD检测，LLM输出标量置信度得分 $S(x_i)$，经传播后通过阈值 $\delta$ 判定：

$$\hat{y} = \begin{cases} \text{OOD} & \text{if } S(x_i) \le \delta, \\ \text{ID} & \text{otherwise}. \end{cases}$$

对于描述任务，则利用上下文示例对生成文本进行语义增强。

**支持集构建的两种模式。** 框架支持两种图构建模式：当测试数据分布可获取时，使用全部测试样本构建支持图（PGLLM$^T$，转导推理）；当测试数据不可预知时，使用外部数据集Objaverse的100K样本构建支持图（PGLLM$^O$，归纳推理）。后者的性能虽略低于前者，但仍保持了较强的泛化能力。

消融实验（Table 4）揭示了各模块的协同效应：单独使用in-context guidance可将ModelNet40 OOD检测的AUROC从80.4提升至83.0，单独使用score propagation可将FPR95从100.0降至62.0，而二者联合使用则达到最优的85.9 AUROC和52.1 FPR95，验证了上下文引导与分数传播的互补性。

## 核心模块与公式推导

PGLLM框架由三个核心模块串联构成：**3D特征编码与图构建**、**上下文引导推理（In-context Guidance）**、以及**分数传播细化（Score Refinement）**。各模块均运行于测试时，无需修改任何预训练模型参数。

### 3D特征编码与KNN图构建

给定一组测试点云样本 $\{x_i\}_{i=1}^{N_u}$，首先使用冻结的预训练点云编码器 $f_p$（Point-BERT）提取每个样本的嵌入向量 $p_i = f_p(x_i) \in \mathbb{R}^d$。随后，基于嵌入向量构建K近邻图 $G = (V, E)$，其中节点 $v_i$ 对应样本 $x_i$，边权重由余弦相似度定义并通过Top-K稀疏化得到对称邻接矩阵：

$$W_{ij} = \begin{cases} e_{ij} & \text{if } e_{ij} \in \text{Top}_K(\{e_{ij}\}_{j=1}^{N_u}) \\ 0 & \text{otherwise} \end{cases}, \quad \text{s.t. } e_{ij} = \frac{\langle p_i, p_j \rangle}{\|p_i\| \cdot \|p_j\|}$$

其中 $e_{ij}$ 为样本 $i$ 与 $j$ 的余弦相似度，$\text{Top}_K(\cdot)$ 选取每个节点的 $K$ 个最大相似度邻居。该图编码了测试样本在特征流形上的局部几何结构，是后续上下文检索与分数传播的基础。

### 上下文引导推理（In-context Guidance）

对于每个查询样本 $x_i$，从图中检索其 $K$ 个最近邻 $\mathcal{X}_i = \{x_{i_1}, \dots, x_{i_K}\}$，并将这些邻居的文本描述 $\{c_{i_1}, \dots, c_{i_K}\}$ 作为上下文示例附加到第二阶段LLM的提示中。这些文本描述由PointLLM以一阶段方式生成（使用默认提示"This is an object of"）。第二阶段LLM据此输出初始的类别置信度分数或OOD标量分数，形成初始分数矩阵 $S_0$。

### 分数传播细化（Score Refinement）

为利用图中邻居的语义一致性校准初始预测，PGLLM引入基于标签传播的迭代平滑机制。定义对称归一化邻接矩阵 $\tilde{W} = D^{-\frac{1}{2}} W D^{-\frac{1}{2}}$，其中 $D = \text{diag}(\sum_j W_{ij})$ 为度矩阵。分数矩阵按以下规则迭代更新：

$$S_t = \alpha S_{t-1} \tilde{W} + (1-\alpha) S_0$$

其中 $\alpha \in [0,1]$ 控制图平滑与初始分数的平衡，$t = 1, \dots, T$ 为迭代步数。该公式的核心作用在于：每个样本的最终分数是其自身LLM输出与邻居LLM输出的加权融合，权重由流形上的视觉相似度决定。对于3D识别任务，$S_t$ 为类别分数矩阵；对于OOD检测任务，$S(x_i)$ 退化为标量置信度，最终通过阈值 $\delta$ 判定：

$$\hat{y} = \begin{cases} \text{OOD} & \text{if } S(x_i) \le \delta, \\ \text{ID} & \text{otherwise}. \end{cases}$$

消融实验（Table 4）证实，上下文引导与分数传播具有互补协同效应：单独使用上下文引导可将ModelNet40 OOD检测AUROC从80.4提升至83.0，单独使用分数传播可将FPR95从100.0降至62.0；二者联合使用时，ModelNet40上ACC达63.1、AUROC达85.9、FPR95降至52.1，均显著优于任一单独模块。

## 实验与分析

### 核心性能瓶颈与实验动机

现有3D多模态大语言模型（MLLM）在理解三维点云时面临一个根本性困难：几何结构相似的物体（如桌子和茶几、床头柜和梳妆台）在孤立推理时极易产生类间混淆。PointLLM等一阶段方法虽然能生成看似合理的描述，但其推理过程缺乏对测试样本间流形关系的利用，导致分类和分布外（OOD）检测的可靠性不足。PGLLM的核心假设是：**测试样本的歧义可以通过其流形邻居的语义一致性来消解**——如果某个样本的近邻在语义上高度一致，那么该样本的预测也应向邻居靠拢。

### 实验设置概要

实验覆盖三大任务：3D OOD检测、3D识别和3D描述。数据集包括ModelNet40（合成物体）、ShapeNetCore（合成物体）、Objaverse（大规模真实扫描）和S3DIS（真实室内场景）。所有方法使用相同的PointLLM-7B作为一阶段3D编码器和描述生成器，第二阶段LLM统一使用GPT-4（闭源）或DeepSeek-V3、Qwen3-VL-8B等开源模型进行公平比较。PGLLM有两种变体：**PGLLM^T**（使用测试集自身构建支持图，转导推理）和**PGLLM^O**（使用Objaverse的100K样本构建外部支持图，归纳推理）。默认超参数为K=3（KNN邻居数）、α=0.5（标签传播平滑系数）、T=5（传播迭代次数）。

### 主实验结果

#### 3D OOD检测

Table 1展示了闭源LLM设置下的OOD检测结果。PGLLM^T在ModelNet40的三个子集（MN1-MN3）上平均AUROC达到**85.9%**，相比PointLLM直接推理的80.0%提升5.9个百分点；在ShapeNetCore的三个子集（SN1-SN3）上平均AUROC达到**91.1%**，较PointLLM的87.7%提升3.4个百分点。尤其值得注意的是，在最具挑战性的MN3子集上，PGLLM^T的AUROC从69.6%跃升至**80.1%**，FPR95从100.0%降至69.3%，表明流形引导机制对困难样本的改善尤为显著。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_qsra0EsUpe/figures/003_Table_1.jpg]]

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_qsra0EsUpe/figures/004_Table_1.jpg]]
*Table 1: Evaluation of 3D OOD detection on ModelNet40 and ShapeNetCore. Bold and underlined numbers denote the best and second-best results, respectively. Each ”MNx” or ”SNx” denotes the known class split and the rest are unknown. Table 2: Evaluation of 3D OOD detection on ModelNet40 and ShapeNetCore for open-sourced LLM*

Table 2进一步验证了方法在开源LLM上的可移植性。使用MiniGPT-3D作为一阶段模型、Qwen3-VL-8B作为第二阶段LLM时，PGLLM^T在ModelNet40 MN1上取得**92.4% AUROC**和53.0% FPR95，超越所有闭源基线。使用DeepSeek-V3时，PGLLM^T在ModelNet40平均AUROC仍达到**82.7%**，证明方法不依赖高端闭源API。

#### 3D识别

Table 3报告了ModelNet40上的3D识别结果。PGLLM^T使用GPT-4时平均准确率达到**62.5%**，超越MiniGPT-3D的60.9%和PointLLM的59.1%。更关键的是，当第二阶段LLM替换为低成本的DeepSeek-V3时，PGLLM^T仍取得**62.3%**的平均准确率，显著超越所有基于GPT-4的基线方法（最佳非PGLLM方法为53.1%），提升幅度达9.2个百分点。这一结果表明，流形引导和分数传播带来的增益远大于第二阶段LLM本身的能力差异。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_qsra0EsUpe/figures/006_Table_3.jpg]]
*Table 3: Comparison of results on 3D recognition (ModelNet40) and 3D captioning (Objaverse). Recognition performance is evaluated using two prompt types: an Instruction-type (I) prompt (“What is this?”) and a Completion-type (C) prompt (“This is an object of ”)*

#### 真实场景泛化

Figure 4展示了S3DIS真实室内场景上的结果。在3D OOD检测任务中，PGLLM^T（GPT-4）的AUROC达到**85.0%**，FPR95降至**65.0%**，显著优于PointLLM的78.0% AUROC和85.0% FPR95。在3D识别任务中，PGLLM^T同样保持领先。这表明基于特征相似性的KNN图构建策略能够有效迁移到与训练数据分布差异较大的真实场景。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_qsra0EsUpe/figures/007_Figure_4.jpg]]
*Figure 4: Results on real-world benchmark S3DIS. We report 3D OOD detection and 3D recognition tasks*

### 消融实验

Table 4系统分析了in-context guidance和score propagation两个核心组件的贡献。在ModelNet40上：

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_qsra0EsUpe/figures/008_Table_4.jpg]]
*Table 4: Ablation study on two datasets. ACC refers to the results of 3D recognition experiments, while AU-ROC and FPR95 correspond to the OOD detection experiments. Both AUROC and FPR95 represent averages across all subsets of the ModelNet40 and ShapeNetCore datasets. The • denotes in-context guidance derived through direct nearest-sample retrieval without graph*

- **仅使用in-context guidance**：AUROC从80.4%提升至83.0%（+2.6），FPR95从100.0%降至71.0%（-29.0），证明上下文示例能有效提供判别信息。
- **仅使用score propagation**：FPR95从100.0%大幅降至62.0%（-38.0），AUROC从80.4%提升至83.4%，表明图上的标签平滑本身就能显著抑制噪声预测。
- **同时启用两个组件**：AUROC达到**85.9%**，FPR95降至**52.1%**，识别准确率达到**63.1%**，均优于单独使用任一组件的效果，验证了两者的**互补与协同效应**。

在ShapeNetCore上趋势一致，同时启用两个组件时AUROC达到91.1%、FPR95降至29.6%。

Figure 5分析了KNN邻居数量K对OOD检测性能的影响。ModelNet40在**K=7**时AUROC达到峰值，ShapeNetCore在**K=4**时达到峰值。K值过小会导致上下文信息不足，K值过大则会引入语义不相关的噪声邻居，两者都会损害性能。这一差异反映了两个数据集在类内多样性和类间相似性上的不同特性。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_qsra0EsUpe/figures/010_Figure_5.jpg]]
*Figure 5: Different number of K-values for 3D OOD detection on two datasets*

### 失败模式与局限性

定性分析揭示了几个典型失败模式：

1. **上下文噪声干扰**：当查询样本的PointLLM描述相对准确，但其K近邻的描述包含不准确信息时，第二阶段LLM的评分可能被误导，产生偏差预测（Fig. 15）。这表明in-context guidance的有效性高度依赖邻居描述的质量。

2. **小规模数据集的描述任务受限**：3D目标描述（captioning）任务的性能受限于测试数据规模。当支持图节点数较少时，可用的上下文示例有限，描述优化效果不明显。

3. **在线场景性能退化**：动态图扩展实验表明，当测试样本完全在线到达且顺序不佳时，PGLLM的AUROC从全量图构建的89.6%降至**86.8%**。虽然仍优于基线，但性能差距说明图结构的完整性对流形引导至关重要。

4. **一阶段描述质量依赖**：方法的有效性建立在PointLLM生成描述的基本质量之上。若一阶段描述严重错误（如将椅子误述为桌子），则其作为邻居的上下文示例时可能传播错误信息，使分数传播机制失效。

### 关键图表结论总结

| 图表 | 核心发现 |
|------|----------|
| Table 1 | PGLLM^T在ModelNet40和ShapeNetCore的OOD检测中分别达到85.9%和91.1%平均AUROC，全面超越所有基线 |
| Table 3 | 使用低成本DeepSeek-V3时以62.3%准确率超越所有GPT-4基线，证明方法增益远超LLM能力差异 |
| Table 4 | In-context guidance和score propagation具有互补协同效应，联合使用获得最佳性能 |
| Figure 5 | K值选择需适配数据集特性，ModelNet40最优K=7，ShapeNetCore最优K=4 |
| Figure 4 | 方法在S3DIS真实场景上保持显著优势，验证了跨域泛化能力 |

### 补充图表

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_qsra0EsUpe/figures/013_Table_5.jpg]]
*Table 5: For each distinct out-of-distribution (OOD) subset partition on the ShapeNetCore, the categories residing within a given subset are designated as in-distribution (ID), whereas categories from all other subsets are considered entirely OOD*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_qsra0EsUpe/figures/015_Table_6.jpg]]

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_qsra0EsUpe/figures/016_Table_7.jpg]]
*Table 7: For each distinct out-of-distribution (OOD) subset partition on the ModelNet40, the categories residing within a given subset are designated as in-distribution (ID), whereas categories from all other subsets are considered entirely OOD*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_qsra0EsUpe/figures/017_Table_8.jpg]]

## 方法谱系与知识库定位

### 问题定位与核心瓶颈

现有的3D多模态大语言模型（MLLM）在理解三维点云时面临一个关键瓶颈：难以有效区分几何结构相似但语义不同的三维物体，导致严重的类间混淆。具体而言，当单张独立点云被送入LLM进行推理时，模型缺乏足够的上下文来消解视觉歧义，推理可靠性不足。这一问题在三维识别和分布外（OOD）检测任务中尤为突出——现有方法如**PointLLM**（Xu et al., 2024）和**MiniGPT-3D**（Tang et al., 2024）虽能生成基本的3D描述，但直接基于单样本描述进行推理时，性能上限受限于孤立推理范式。

### 方法谱系与关系

PGLLM处于3D MLLM测试时优化与流形学习的交叉点。其方法谱系可沿以下维度展开：

**上游依赖：3D编码与描述生成。** PGLLM建立在冻结的预训练点云编码器（Point-BERT）和第一阶段LLM（PointLLM-7B）之上，利用它们为每个测试样本提取嵌入向量和文本描述。这一设计与**Point-Bind LLM**（Guo et al., 2023）、**3D-LLM**（Hong et al., 2023）、**ShapeLLM**（Qi et al., 2024a）等3D LLM共享相似的一阶段编码-描述范式，但PGLLM的关键创新在于不修改这些上游模块，而是在测试时通过图结构对其进行增强。

**核心创新：测试时流形感知。** PGLLM的独特贡献是将LLM推理从孤立样本扩展到局部邻域。具体而言，它通过三个关键机制实现这一扩展：
1. **KNN图构建**：基于嵌入余弦相似度构建K近邻图，边权重反映样本的视觉相似性，权重矩阵定义为 $W_{ij} = \begin{cases} e_{ij} & \text{if } e_{ij} \in \text{Top}_K(\{e_{ij}\}_{j=1}^{N_u}) \\ 0 & \text{otherwise} \end{cases}$，其中 $e_{ij} = \frac{\langle p_i, p_j \rangle}{\|p_i\| \cdot \|p_j\|}$。
2. **上下文引导（In-context Guidance）**：从图中检索查询样本的K近邻，将其文本描述作为上下文演示加入第二阶段LLM的提示中，使模型能参考流形邻居的语义信息进行推理。
3. **分数传播细化（Score Refinement）**：利用标签传播算法在图结构上平滑LLM输出的类别置信度或OOD分数，更新规则为 $S_t = \alpha S_{t-1} \tilde{W} + (1-\alpha) S_0$，其中 $\tilde{W} = D^{-\frac{1}{2}} W D^{-\frac{1}{2}}$。

**与基线方法的关系。** 在OOD检测任务上，PGLLM与VLM零样本检测基线形成对比：**MCM**（Ming et al., 2022）、**NegLabel**（Jiang et al., 2024a）、**ZLaP**（Kalantidis et al., 2024）、**GSP**（Chen et al., 2025）等方法依赖视觉-语言对齐进行零样本判别，但未利用测试样本间的流形结构。PGLLM通过图传播机制补充了这一缺失的维度。在3D识别任务上，PGLLM与直接使用GPT-4的PointLLM和MiniGPT-3D相比，通过上下文引导和分数细化的协同作用获得显著增益。

### 适用边界与局限

**数据依赖性。** 方法的有效性依赖于初始PointLLM生成描述的基本质量——若一阶段描述严重错误，上下文引导可能失效。此外，当查询样本的描述相对准确但上下文示例包含不准确信息时，第二阶段评分可能产生偏差。3D目标描述（Captioning）任务的性能也受限于测试数据规模，在小规模数据集上表现可能受限。

**图构建的敏感性。** KNN邻居数量K对性能有影响：ModelNet40 OOD检测在K=7时达到峰值，ShapeNetCore在K=4时达到峰值，表明最优K值具有数据集依赖性。虽然方法支持动态图扩展策略，但当测试样本完全在线到达且顺序不佳时，性能相比全量图构建有适度下降（AUROC从89.6降至86.8）。

**类别集合假设。** 当前框架假设点云类别集合是已知且固定的，这限制了其在完全开放集（open-world）3D理解任务中的直接应用。支持集构建也面临选择：使用测试集自身（PGLLM^T）可获得最佳性能但需要测试数据分布已知，使用外部数据集Objaverse（PGLLM^O）虽更通用但性能略低。

### 开放问题

1. **上下文示例的智能选择**：如何为上下文示例设计更智能的检索策略（如考虑示例多样性、标签信息、任务相关性）以进一步提升上下文学习效果？
2. **大规模场景扩展**：图构建与分数传播机制能否扩展到更大规模的点云场景（如室外LiDAR点云）且保持计算效率？当前KNN图的构建复杂度随测试样本数平方增长。
3. **与参数高效微调的融合**：能否将当前的测试时优化框架与参数高效的微调方法（如LoRA）结合，在标注数据稀缺时获得进一步增益？
4. **开放集泛化**：如何将固定类别集合的假设松弛为开放集场景，使框架能处理训练时未见过的物体类别？
5. **多模态融合深度**：当前方法仅在文本空间进行上下文引导，是否可以将图结构信息直接注入LLM的视觉编码或注意力机制中，实现更深层的多模态流形感知？

## 原文 PDF

![[paperPDFs/ICLR_2026/Test_Time_Optimization_of_3D_Point_Cloud_LLM_via_Manifold_Aware_In_Context_Guidance_and_Refinement.pdf]]
