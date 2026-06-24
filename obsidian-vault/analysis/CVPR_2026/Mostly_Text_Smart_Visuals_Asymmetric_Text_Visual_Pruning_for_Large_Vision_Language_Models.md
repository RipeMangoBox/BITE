---
title: "Mostly Text, Smart Visuals: Asymmetric Text-Visual Pruning for Large Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Mostly_Text_Smart_Visuals_Asymmetric_Text_Visual_Pruning_for_Large_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/LezJ/ATV-Pruning"
aliases:
- APATVWP
- MTSVATVPLVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 校准池中文本token与视觉token的选择策略——文本token对保证语言能力必不可少，而视觉token仅需少量关键子集即可维持视觉性能。
primary_logic: 文本路径对剪枝高度敏感，必须用文本token校准；视觉路径高度冗余，可容忍高达60%的非结构化稀疏度。基于此，提出非对称文本-视觉剪枝（ATV-Pruning）：保留所有文本token，并通过块自适应的视觉漂移从各层中选取少量显著视觉token，构建模态感知校准集，从而在保持性能的同时大幅剪枝。
claims:
- 文本路径使用文本校准池在60%稀疏度下SQA_img达61.58，而混合或视觉校准导致性能崩溃至35.85和11.1。
- 视觉路径在不同校准池下均保持>99.25%性能，甚至文本校准也能达到100.05%保留率。
- ATV-Pruning在LLaVA-NeXT 8B上50%稀疏度取得94.00%平均保留率，60%稀疏度取得77.01%，均优于所有基线。
- Avg. Retention (LLaVA-NeXT 8B, 50% sparsity) 上 Average Retention = 94.00%
---

# Mostly Text, Smart Visuals: Asymmetric Text-Visual Pruning for Large Vision-Language Models

> [!tip] 核心洞察
> 文本路径对剪枝高度敏感，必须用文本token校准；视觉路径高度冗余，可容忍高达60%的非结构化稀疏度。基于此，提出非对称文本-视觉剪枝（ATV-Pruning）：保留所有文本token，并通过块自适应的视觉漂移从各层中选取少量显著视觉token，构建模态感知校准集，从而在保持性能的同时大幅剪枝。

| 字段 | 内容 |
|------|------|
| 中文题名 | 主要文本、智能视觉：面向大型视觉语言模型的非对称文本-视觉剪枝 |
| 英文题名 | Mostly Text, Smart Visuals: Asymmetric Text-Visual Pruning for Large Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.16001) · [Code](https://github.com/LezJ/ATV-Pruning) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ATV-Pruning (Asymmetric Text-Visual Weight Pruning) |
| Dataset | Avg. Retention, MME, OKVQA |

> [!tip] 效果简介
> - Avg. Retention (LLaVA-NeXT 8B, 50% sparsity) 上，Average Retention 94.00% vs 92.67% (TAMP) (+1.33%)。
> - Avg. Retention (LLaVA-NeXT 8B, 60% sparsity) 上，Average Retention 77.01% vs 76.24% (SparseGPT) (+0.77%)。
> - MME (LLaVA-NeXT 8B, 50% sparsity) 上，MME Score 1801.51 vs 1742.80 (SparseGPT) (+58.71)。

## 概述

大型视觉语言模型（LVLM）的部署面临严重的计算与存储瓶颈，权重剪枝是缓解该问题的重要技术。现有剪枝方法（如**SparseGPT**、**Wanda**及多模态剪枝方法**TAMP**）在校准阶段普遍采用模态无关的策略，即不加区分地混合使用文本与视觉token来估计权重重要性。本文揭示了一个被忽视的关键瓶颈：**文本与视觉模态在剪枝敏感度上存在本质差异**——文本路径对校准token的选择高度敏感，而视觉路径则表现出极强的冗余容忍度。若使用混合或纯视觉token校准文本路径，在60%稀疏度下性能将严重退化（例如SQA_img从61.58骤降至35.85甚至11.1）；相反，视觉路径在不同校准池下均可保持99.25%以上的性能保留率，甚至用纯文本token校准也能达到100.05%（Tab. 1）。这一发现表明，**文本token对维持语言能力不可或缺，而视觉token仅需少量关键子集即可维持视觉性能**。

基于上述洞察，本文提出**ATV-Pruning（非对称文本-视觉剪枝）**，核心思想是构建模态感知的校准集：**保留全部文本token，同时通过块自适应策略从各Transformer层中选取少量显著视觉token**。具体而言，ATV-Pruning引入“视觉漂移”（visual drift）——即视觉token经过某个block前后表征的余弦距离——作为token显著性的度量信号，并根据每层的平均视觉漂移动态分配视觉token预算，从而在保持校准质量的同时大幅压缩视觉token数量。

在LLaVA-NeXT 8B模型上，ATV-Pruning在50%非结构化稀疏度下取得**94.00%的平均性能保留率**，优于TAMP（92.67%）和SparseGPT（92.08%）；在60%稀疏度下取得**77.01%的保留率**，同样领先所有基线方法（Tab. 2）。在Qwen2-VL 7B上，60%稀疏度下平均保留率达85.65%，验证了方法的跨模型泛化性。消融实验进一步证实：视觉漂移作为显著性信号优于注意力信号和多样性信号；块自适应预算分配对性能有稳定贡献；减少文本token比例始终损害性能（Fig. 5, Tab. 3）。在效率方面，ATV-Pruning的剪枝耗时仅99.6秒，显著快于SparseGPT（666.0秒）和TAMP（1418.4秒），仅比最快的Wanda慢约1.35倍（Tab. 4）。

**方法谱系与知识库定位**：ATV-Pruning属于**激活感知的权重剪枝**范畴，其重要性评分机制沿袭Wanda的权重幅度与输入激活范数乘积（Eq. 1），但创新性地将激活统计的估计对象从“所有token”替换为“模态感知校准集”。与TAMP等面向LVLM的剪枝方法相比，ATV-Pruning首次明确解耦了文本与视觉模态在校准中的角色，并引入块自适应视觉选择机制。该方法不依赖权重更新（区别于SparseGPT的Hessian近似），也不依赖跨模态统计对齐（区别于TAMP），在保持简洁性的同时实现了显著的性能增益。当前局限包括：视觉漂移计算引入约1.35倍额外前向开销；全局缩放因子α需针对不同模型手动设定；仅针对LLM骨干的线性层进行剪枝，未覆盖视觉编码器等模块。

## 背景与动机

### 大型视觉语言模型的部署瓶颈

大型视觉语言模型（LVLM）在视觉问答、图像描述等多模态任务上取得了显著进展，但其庞大的参数规模带来了高昂的推理延迟与显存占用，严重制约了实际部署。权重剪枝作为一种有效的模型压缩技术，通过移除冗余连接来降低计算和存储成本，已在纯语言模型（LLM）上得到广泛验证。然而，将剪枝技术直接迁移至LVLM面临一个根本性挑战：**文本与视觉两种模态在剪枝敏感度上存在本质差异**，而现有方法普遍忽视了这一模态异质性。

### 现有方法的统一缺陷：模态无关的校准池

当前主流的剪枝方法——无论是基于海森近似的**SparseGPT**，还是激活感知的**Wanda**，亦或是面向多模态设计的**TAMP**——在校准阶段均采用**模态无关（modality-agnostic）的校准池构建策略**。具体而言，这些方法将来自文本和视觉的所有token混合在一起，统一计算激活统计量以估计权重重要性分数。这种“一视同仁”的做法隐含了一个未经检验的假设：文本token和视觉token对剪枝的贡献是同质的。

然而，这一假设并不成立。如图1所示，文本与视觉的激活表征在表示空间中占据截然不同的聚类区域（t-SNE可视化），且两者导出的剪枝掩码呈现出广泛的IoU分布。这意味着，**用视觉token校准文本路径（或用文本token校准视觉路径）会产生显著偏离的剪枝决策**，从而在压缩过程中引入系统性误差。

### 模态敏感性差异的核心发现

为了解耦两种模态的剪枝敏感性，本文设计了**MoT探针（Modality-of-Token Probe）**架构（图2）：在每层Transformer块中，将QKV和FFN层复制为独立的文本通路和视觉通路，分别处理各自的token类型，从而独立评估各路径在不同校准池下的剪枝表现。

实验揭示了两个关键发现（表1）：

- **Finding A：文本路径对校准池高度敏感。** 文本路径使用文本校准池在60%稀疏度下，SQA_img准确率达61.58；而使用混合校准池或纯视觉校准池时，性能分别崩溃至35.85和11.1。在50%稀疏度下，文本校准池实现98.26%的平均保留率，远超混合校准池的87.67%。这说明文本token对于维持语言能力是**不可替代**的。

- **Finding B：视觉路径高度冗余且鲁棒。** 视觉路径在不同校准池下均保持超过99.25%的性能保留率，甚至在极端情况下使用纯文本校准也能达到100.05%的平均保留率。这表明视觉路径可容忍高达60%的非结构化稀疏度，且对校准token的来源不敏感。

### 研究动机与核心思路

上述发现揭示了一个清晰的因果机制：**文本路径对剪枝高度敏感，必须用文本token校准；视觉路径高度冗余，仅需少量关键视觉token即可维持性能。** 基于此，本文提出**非对称文本-视觉剪枝（ATV-Pruning）**：在校准池构建中采用非对称策略——**保留所有文本token以保证语言能力不退化，同时通过块自适应的视觉漂移机制从各层中选取少量显著视觉token**，从而在保持性能的前提下实现大幅剪枝。这一设计从根本上解决了模态无关校准池导致的文本侧退化问题，为LVLM的高效部署提供了新的技术路径。

## 核心创新

ATV-Pruning 的核心创新在于**将“模态无关”的校准池构建策略替换为“非对称文本-视觉感知”的校准池构建策略**，从而从根本上解决了现有 LVLM 剪枝方法中文本路径对剪枝高度敏感却被忽视的瓶颈。具体而言，该方法在以下三个关键环节上做出了改变：

### 1. 校准池构建：从模态无关到非对称模态感知

现有剪枝方法（如 SparseGPT、Wanda、TAMP）在校准池构建时采用模态无关策略，即混合使用所有多模态 token（文本 token + 视觉 token）来计算激活统计量，用于指导权重重要性评分。这种“一刀切”的做法掩盖了文本与视觉模态在剪枝敏感度上的本质差异。

ATV-Pruning 的核心洞察来自模态解耦探针实验（Figure 2, Table 1）：**文本路径对剪枝高度敏感**——在 60% 稀疏度下，若使用混合校准池或纯视觉校准池，SQA_img 性能从 61.58 崩溃至 35.85 和 11.1；而**视觉路径高度冗余**，在不同校准池下均保持 >99.25% 的性能保留率，甚至使用纯文本校准也能达到 100.05% 的保留率。

基于此，ATV-Pruning 提出**非对称校准集**：
$$S_{\mathrm{cal}} = \mathcal{T} \cup \mathcal{V}_{\mathrm{sub}}$$

其中 $\mathcal{T}$ 为**全部文本 token**（保证语言和推理能力的稳定），$\mathcal{V}_{\mathrm{sub}}$ 为通过块自适应策略筛选出的**显著视觉 token 子集**（仅保留对视觉理解关键的少量 token）。这一设计直接回应了 Finding A（文本路径需文本校准）和 Finding B（视觉路径冗余度高）的实证结论。

### 2. 视觉 token 选择：从无选择到块自适应显著性子集

在视觉 token 的选择策略上，基线方法（Wanda、SparseGPT）不对视觉 token 做任何筛选，TAMP 虽引入跨模态统计指导选择，但仍混合处理模态且缺乏层级粒度。ATV-Pruning 引入了**块自适应视觉选择**机制，包含三个关键设计：

- **显着性信号定义**：以视觉漂移（Visual Drift）——即 token $v$ 经过某 Transformer block 前后表征的余弦距离——作为显着性度量：
  $$s_{v} = 1 - \cos(\mathbf{X}_{\mathrm{in},v}, \mathbf{X}_{\mathrm{out},v})$$
  消融实验（Table 3）表明，该信号优于基于注意力权重的 ABS 信号和基于多样性的 DBS 信号。

- **块级预算动态分配**：计算每 block 的平均显着性 $\bar{s}$，并以此动态分配该 block 的视觉 token 预算：
  $$K = \lfloor \alpha \cdot \bar{s} \cdot n_{\mathrm{text}} \rfloor$$
  其中 $\alpha$ 为全局缩放因子。这使得视觉表征更新剧烈的层保留更多视觉 token（见 Figure A6 的可视化趋势），而去除块自适应性或固定预算均会导致性能下降（Table 3）。

- **Top-K 筛选**：在每个样本中以显着性为准则选取 Top-K 个最重要的视觉 token：
  $$\mathcal{V}_{\mathrm{sub}} = \mathrm{TopK}_v(\{s_{v}\}, K)$$

### 3. 激活统计估计对象：从全量 token 到模态感知子集

在权重重要性评分环节，ATV-Pruning 沿用 Wanda 的核心公式：
$$\mathbf{I}_{ij} = |\mathbf{W}_{ij}| \cdot \|\mathbf{X}_{j}\|_{2}$$

但关键区别在于：基线方法在整个校准批次的所有 token 上计算激活范数 $\|\mathbf{X}_{j}\|_{2}$，而 ATV-Pruning **仅在选定的模态感知校准集 $\mathcal{S}_{\mathrm{cal}}$ 上计算**。这意味着剪枝决策所依赖的激活统计量，其来源已从“模态无差别的全量 token”转变为“文本全量 + 视觉显著子集”的非对称组合，从而在剪枝过程中保护了文本路径的完整性。

### 创新总结

ATV-Pruning 的三个 changed slots 构成了一条因果链：**非对称校准池构建**（保留全部文本 token + 筛选显著视觉 token）→ **块自适应视觉选择**（以视觉漂移为信号动态分配预算）→ **模态感知激活统计估计**（仅在筛选后的子集上计算重要性分数）。这一链条使得 ATV-Pruning 在 LLaVA-NeXT 8B 上以 50% 稀疏度取得 94.00% 的平均保留率（超越最强基线 TAMP 的 92.67%），在 60% 稀疏度下取得 77.01%（超越 SparseGPT 的 76.24%），验证了非对称策略在保持文本能力的同时大幅剪枝视觉冗余的有效性。

## 整体框架

ATV-Pruning 的整体流程围绕一个核心矛盾展开：文本路径对剪枝高度敏感，而视觉路径高度冗余。基于此，方法将剪枝过程解耦为三个顺序执行的模块，形成“统计收集 → 校准集构建 → 权重剪枝”的流水线。

### 模块关系与数据流

1. **统计收集（前向传播）**：以原始多模态样本为输入，执行一次完整的前向传播，记录每个 Transformer 块中视觉 token 的输入与输出表征。此阶段不修改任何权重，仅为后续选择提供显着性信号。

2. **模态感知校准集构建**：利用前向传播收集的统计量，对每个块计算视觉 token 的显着性分数（视觉漂移）和块平均显着性，据此动态分配各块的视觉 token 预算，并选取 Top-K 显著视觉 token。最终校准集由**全体文本 token** 与**块自适应选出的视觉 token 子集**合并构成（Eq. 2）。

3. **激活感知权重剪枝**：在构建好的校准集上重新计算激活范数，结合权重幅度按 Wanda 重要性分数（Eq. 1）对所有线性层执行均匀非结构化剪枝，达到目标稀疏度。

### 关键设计决策

- **非对称性**：文本 token 全部保留，视觉 token 仅保留稀疏子集。这一决策源于敏感性分析的核心发现——文本路径使用非文本校准池会导致性能崩溃，而视觉路径即使仅用文本校准也能保持超过 99.25% 的性能（Tab. 1）。
- **块自适应性**：不同 Transformer 块的视觉信息更新强度不同，浅层通常处理低级特征、深层融合跨模态语义。通过块平均显着性动态分配预算（Eq. 6），使视觉 token 集中于信息更新剧烈的层，避免均匀分配造成的信号稀释。
- **效率优先**：整个流程仅需两次前向传播（一次统计收集、一次剪枝执行），剪枝耗时 99.6 秒，仅比最快的 Wanda 慢 1.35×，远优于 SparseGPT（666.0 秒）和 TAMP（1418.4 秒）（Tab. 4）。

### 伪代码概览

Algorithm 1 给出了完整的 ATV-Pruning 流程：遍历校准样本 → 前向传播收集视觉漂移 → 计算块平均显着性与预算 K → 选取 Top-K 视觉 token → 构建模态感知校准集 → 按 Wanda 重要性分数逐层剪枝。该流程将所有文本 token 与自适应视觉子集统一为校准集，驱动后续的权重重要性评估与裁剪。

### 补充图表

![[assets/figures/papers/paper_list_l768_https_arxiv_org_abs_2603_16001/figures/004_Figure_3.jpg]]
*Figure 3: Overview of ATV-Pruning; Color intensity reflects the degree of visual saliency. Blocks with higher visual saliency keep more salient visual tokens, with all text tokens*

## 核心模块与公式推导

ATV-Pruning 建立在激活感知权重剪枝框架 Wanda 之上，其核心创新在于构建模态感知的校准集，以替代传统模态无关的校准池。整个方法流程由三个关键模块串联而成：模态感知校准集构建、块自适应视觉选择、以及激活感知权重剪枝（Algorithm 1）。

### 权重重要性分数（Wanda 基础）

ATV-Pruning 沿用 Wanda 的权重重要性度量。对于线性层权重矩阵 $\mathbf{W}$，其元素 $\mathbf{W}_{ij}$ 的重要性由权重幅度与对应输入激活列范数的乘积决定：

$$\mathbf{I}_{ij} = |\mathbf{W}_{ij}| \cdot \|\mathbf{X}_{j}\|_{2}$$

其中 $\mathbf{X}_{j}$ 是第 $j$ 个输入激活通道在校准集上的 $\ell_2$ 范数。该分数同时捕获了权重的静态幅度和输入的动态激活规模，按目标稀疏度裁剪最低分权重即可完成剪枝。ATV-Pruning 的关键差异在于 $\|\mathbf{X}_{j}\|_{2}$ 的计算范围——仅在精心构建的模态感知校准集 $\mathcal{S}_{\mathrm{cal}}$ 上进行。

### 模态感知校准集构建

传统方法在校准批次的所有 token（文本+视觉）上统一计算激活统计，忽略了模态间剪枝敏感度的本质差异。ATV-Pruning 采用非对称策略，将校准集定义为全体文本 token 与块自适应选出的显著视觉 token 子集的并集：

$$\mathcal{S}_{\mathrm{cal}} = \mathcal{T} \cup \mathcal{V}_{\mathrm{sub}}$$

其中 $\mathcal{T}$ 为所有文本 token 位置的集合，$\mathcal{V}_{\mathrm{sub}}$ 为经块自适应策略筛选出的视觉 token 子集。这一设计的因果逻辑是：文本路径对剪枝高度敏感，必须保留全部文本 token 来校准；而视觉路径高度冗余，仅需少量关键视觉 token 即可维持性能。

### 块自适应视觉选择

视觉 token 的选择并非统一进行，而是根据每个 Transformer block 的视觉活动水平动态分配预算。该模块包含三个步骤：

**视觉漂移作为显着性信号。** 对于每个 block $b$ 和每个视觉 token $v$，定义其显着性为该 token 通过 block 前后表征的余弦距离（即视觉漂移）：

$$s_{v} = 1 - \cos(\mathbf{X}_{\mathrm{in},v}, \mathbf{X}_{\mathrm{out},v})$$

其中 $\mathbf{X}_{\mathrm{in},v}$ 和 $\mathbf{X}_{\mathrm{out},v}$ 分别是 token $v$ 进入和离开 block $b$ 时的隐藏表征。余弦距离越大，表明该 token 在此 block 中经历的表征更新越显著，对剪枝校准的信息量越大。

**块平均显着性。** 在校准集的所有视觉 token 上聚合显着性，得到该 block 的全局视觉活动水平：

$$\bar{s} = \frac{1}{|\mathcal{V}_{\mathrm{all}}|} \sum_{v \in \mathcal{V}_{\mathrm{all}}} s_{v}$$

**块级预算分配与 Top-K 选择。** 每个 block 的视觉 token 预算 $K$ 与块平均显着性和文本 token 数成正比，由全局缩放因子 $\alpha$ 调控：

$$K = \lfloor \alpha \cdot \bar{s} \cdot n_{\mathrm{text}} \rfloor$$

其中 $n_{\mathrm{text}}$ 为文本 token 数量。最后，以显着性为准则选取 Top-K 个视觉 token：

$$\mathcal{V}_{\mathrm{sub}} = \mathrm{TopK}_v(\{s_{v}\}, K)$$

该策略使视觉表征更新剧烈的 block 保留更多视觉 token，而视觉处理较浅的 block 仅保留少量 token，实现块自适应的预算分配。消融实验（Table 3）表明，去除块自适应性（固定每块预算）使平均保留率从 98.56% 降至 98.24%，随机选择则降至 97.50%，验证了视觉漂移信号和自适应分配的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l768_https_arxiv_org_abs_2603_16001/figures/002_Figure_2.jpg]]
*Figure 2: Modality decoupling via MoT probe. For each Transformer block, the QKV and FFN layers are replicated into visual and textual pathways, which process their respective token types. Independent pruning masks are derived for each pathway using activation statistics from text-only, image-only, or mixed calibration pools. This setup enables controlled comparison of modalityspecific pruning sensitivity*

![[assets/figures/papers/paper_list_l768_https_arxiv_org_abs_2603_16001/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of the divergent statistical characteristics across different modalities, manifesting as: (a) activation representation: the textual and visual activations occupy distinct clustered regions in the representation space (t-SNE visualization); and (b) pruning importance: the pruning masks derived from the text-only and visual-only calibration data exhibit a broad IoU distribution (taking 50% sparsity level as an example)*

## 实验与分析

### 6.1 实验设置

**模型与数据。** 主实验在 LLaVA-NeXT (8B) 上进行，并在 Qwen2-VL (7B)、LLaVA-OneVision 和 Qwen2.5-VL 上验证泛化性。所有方法使用相同的 128 个 ShareGPT4V 样本进行校准，评估使用 lmms-eval 统一协议，覆盖 9 个基准（包括 MME、MMBench、SQA_img、OKVQA、VizWiz 等）。剪枝应用于 LLM 骨干中所有线性层的均匀非结构化稀疏度。

**基线方法。** 对比三类代表性剪枝方法：
- **SparseGPT**：基于海森近似的剪枝方法，通过局部权重更新最小化输出误差；
- **Wanda**：激活感知剪枝基线，使用权重幅度与输入激活范数计算重要性分数，无需权重更新；
- **TAMP**：面向 LVLM 的多模态剪枝基线，利用跨模态统计指导校准 token 选择（但仍混合处理模态）。

### 6.2 主实验结果

**Table 2** 报告了各方法在 50% 和 60% 非结构化稀疏度下的性能对比。ATV-Pruning 在两个稀疏度级别上均取得最优平均保留率：

- **50% 稀疏度**：ATV-Pruning 平均保留率达 **94.00%**，超过最强基线 TAMP（92.67%）1.33 个百分点。在 MME 基准上，ATV-Pruning 取得 1801.51 分，比 SparseGPT（1742.80）高出 58.71 分。
- **60% 稀疏度**：ATV-Pruning 平均保留率 **77.01%**，优于 SparseGPT（76.24%）和 TAMP（75.49%）。在 OKVQA 上，ATV-Pruning（11.13）比 TAMP（6.73）高出 4.40 个百分点，差距尤为显著。
- **跨模型泛化**：在 Qwen2-VL (7B) 60% 稀疏度下，ATV-Pruning 取得 85.65% 平均保留率，超过 SparseGPT（85.30%）。**Table A6** 进一步验证了在 LLaVA-OneVision 和 Qwen2.5-VL 上的优势。

![[assets/figures/papers/paper_list_l768_https_arxiv_org_abs_2603_16001/figures/010_Table_2.jpg]]
*Table 2: Table A6. Additional pruning results for LLaVA-OneVision and Qwen2.5-VL at 60% unstructured sparsity, serving as an extension of “Table 2”. Best results are highlighted in green*

**关键趋势**：随着稀疏度从 50% 升至 60%，所有方法的性能均显著下降，但 ATV-Pruning 的退化幅度最小——这表明非对称校准策略在极端稀疏度下具有更强的鲁棒性。

### 6.3 消融实验

#### 6.3.1 全局缩放因子 α 的影响

**Figure 4** 展示了 α 在 [0, 8] 范围内的性能变化。当 α ∈ [0.5, 2] 时，性能保持稳定；α = 0（仅文本校准）已优于 Wanda，但加入少量视觉 token（α > 0）进一步提升性能。当 α > 4 时，过多视觉 token 稀释了文本校准信号，导致性能下降。这表明存在一个适中的视觉 token 预算区间，验证了“视觉冗余、文本敏感”的核心洞察。

#### 6.3.2 视觉 token 选择策略

**Table 3** 系统比较了不同视觉 token 选择策略（控制总视觉 token 数相同）：
- **视觉漂移（cosine distance）** 作为显着性信号优于注意力信号（ABS）和多样性信号（DBS），验证了基于表征变化的显着性度量更有效。
- 去除块自适应性（固定每块预算）导致平均保留率从 98.56% 降至 98.24%；随机选择进一步降至 97.50%，说明自适应预算分配和显着性引导的选择缺一不可。

#### 6.3.3 文本 token 的必要性

**Figure 5** 显示，在校准中减少文本 token 保留比例始终损害性能，即使在保留 80% 文本 token 时已有明显退化。这直接证明了文本 token 对剪枝稳定性不可或缺——与 Finding A（文本路径对校准池高度敏感）完全一致。

### 6.4 效率分析

**Table 4** 对比了各方法的剪枝耗时（LLaVA-NeXT 8B, 50% 稀疏度）：
- ATV-Pruning 耗时 **99.6 秒**，仅为 SparseGPT（666.0 秒）的 1/6.7、TAMP（1418.4 秒）的 1/14.2；
- 相比 Wanda（73.6 秒）仅慢 1.35×，但平均性能提升 1.33 个百分点；
- 这得益于 ATV-Pruning 仅需一次额外前向传播收集视觉漂移统计，无需 SparseGPT 的迭代权重更新或 TAMP 的复杂跨模态统计。

### 6.5 失败模式与局限

1. **额外前向开销**：视觉漂移统计收集引入约 1.35× 的额外前向传播（相比 Wanda），在极大规模模型上可能成为瓶颈。
2. **α 需手动调节**：LLaVA-NeXT 使用 α = 1，Qwen2-VL 使用 α = 1.5，缺乏自动适应机制——不同模型的视觉冗余度差异需要人工搜索。
3. **剪枝范围受限**：仅针对 LLM 骨干的线性层，未覆盖视觉编码器、投影层等模块，可能留下进一步压缩空间。
4. **结构化剪枝探索不足**：虽在 **Table A5** 中验证了半结构化剪枝（2:4/4:8）的有效性，但未深入探索块剪枝或通道剪枝等更硬件友好的模式。
5. **极端稀疏度退化**：60% 稀疏度下平均保留率降至 77.01%，部分基准（如 OKVQA）性能损失较大，说明非对称策略在极高稀疏度下仍有改进空间。

### 补充图表

![[assets/figures/papers/paper_list_l768_https_arxiv_org_abs_2603_16001/figures/003_Table_1.jpg]]
*Table 1: Sensitivity analysis of both modality pathways across different calibration token sources, benchmarks, and sparsity*

![[assets/figures/papers/paper_list_l768_https_arxiv_org_abs_2603_16001/figures/005_Table_2.jpg]]
*Table 2: Comparison results with state-of-the-art approaches on nine benchmarks under unstructured, uniform pruning. The official metric for each benchmark and average performance retention (denoted as Average) across all benchmarks, are reported to evaluate the performance of pruned models. Best results are highlighted in green*

![[assets/figures/papers/paper_list_l768_https_arxiv_org_abs_2603_16001/figures/006_Table_3.jpg]]
*Table 3: Discussion on selection strategy of visual tokens. All methods select the same total number of visual tokens for calibration. “Adaptive” indicates whether the visual-token budget is dynamically distributed across blocks. Our default configuration achieves the best overall retention*

![[assets/figures/papers/paper_list_l768_https_arxiv_org_abs_2603_16001/figures/007_Figure_4.jpg]]
*Figure 4: Ablation study about global scaling factor*

![[assets/figures/papers/paper_list_l768_https_arxiv_org_abs_2603_16001/figures/008_Table_4.jpg]]
*Table 4: Pruning efficiency analysis, on LLaVA-NeXT (8B) at 50% sparsity. Time (s): wall-clock pruning time in seconds; Rel. time: pruning time relative to Wanda; Gain (pp): average performance gain in percentage points (pp), taken from Tab. 2*

![[assets/figures/papers/paper_list_l768_https_arxiv_org_abs_2603_16001/figures/009_Figure_5.jpg]]
*Figure 5: Effect of textual token selection under varied retained ratios during calibration, with the default visual token subset of ATV-Pruning. Removing text tokens consistently harms the performance, highlighting their necessity for stable pruning*

![[assets/figures/papers/paper_list_l768_https_arxiv_org_abs_2603_16001/figures/011_Figure.jpg]]
*Figure: A6. Trend of ATV-Pruning’s block-wise Visual Drift and Adaptive Token Allocation on LLaVA-NeXT (8B) with $\alpha = 1$.0. The left y-axis measures the average visual drift per block. The right y-axis indicates the corresponding average number of visual tokens selected per sample. The trend illustrates the blockadaptive nature of our method: more tokens are retained in layers where visual representations undergo significant updates*

## 方法谱系与知识库定位

**剪枝方法谱系中的位置。** ATV-Pruning 属于**数据驱动的一次性权重剪枝**（data-driven one-shot weight pruning）范式，其核心剪枝算子直接继承自 **Wanda**（激活感知剪枝，通过权重幅度与输入激活列范数计算重要性分数 $`\mathbf{I}_{ij} = |\mathbf{W}_{ij}| \cdot \|\mathbf{X}_{j}\|_{2}`$），无需迭代权重更新。与 Wanda 的关键分岔点在于**校准池的构建策略**：Wanda 及更早的 **SparseGPT**（基于海森近似的剪枝方法）均为模态无关的校准范式，将多模态 token 混合处理；**TAMP** 虽面向 LVLM 引入跨模态统计指导校准 token 选择，但仍未解耦文本与视觉模态的剪枝敏感度差异。ATV-Pruning 的本质贡献是将“校准池构建”从模态无关升级为**非对称模态感知**——保留全部文本 token 作为语言能力的锚点，同时通过块自适应视觉漂移机制仅选取少量显著视觉 token，从而在保持 Wanda 级剪枝效率的前提下大幅提升高稀疏度下的性能。

**适用边界与约束。** 该方法的设计与验证聚焦于以下边界条件：(1) **模型架构**：面向 LVLM 的 LLM 骨干网络（如 LLaVA-NeXT、Qwen2-VL、LLaVA-OneVision、Qwen2.5-VL），剪枝仅作用于 LLM 骨干的线性层，视觉编码器等模块未被纳入剪枝范围；(2) **剪枝模式**：主要验证了无结构化均匀稀疏度剪枝，附录中虽展示了半结构化剪枝（2:4/4:8）的可行性，但未深入探索其他结构化剪枝模式；(3) **校准数据**：所有方法统一使用 128 个 ShareGPT4V 样本进行校准，评估采用 lmms-eval 统一协议；(4) **超参数依赖**：全局缩放因子 $`\alpha`$ 需要针对不同模型手动设定（LLaVA-NeXT 使用 $`\alpha=1`$，Qwen2-VL 使用 $`\alpha=1.5`$），缺乏自动适应机制。

**局限性与开放问题。** 首先，ATV-Pruning 为收集视觉漂移统计信息引入了额外的前向传播开销，约为 Wanda 的 1.35 倍（99.6 秒 vs 73.7 秒），虽然仍远优于 SparseGPT 的 666.0 秒和 TAMP 的 1418.4 秒，但进一步降低该延迟仍是工程优化方向。其次，全局缩放因子 $`\alpha`$ 的手动调参限制了方法在不同模型间的即插即用性，设计自适应的 $`\alpha`$ 调整策略是一个值得探索的方向。此外，非对称策略目前仅针对文本-视觉双模态设计，是否可扩展到涉及视频、音频等其他模态的多模态模型尚待验证。最后，将 ATV-Pruning 与量化、视觉 token 剪枝等压缩技术结合能否产生叠加效益，以及在更大规模模型（>30B）上的泛化性，均为论文未覆盖的开放问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/Mostly_Text_Smart_Visuals_Asymmetric_Text_Visual_Pruning_for_Large_Vision_Language_Models.pdf]]
