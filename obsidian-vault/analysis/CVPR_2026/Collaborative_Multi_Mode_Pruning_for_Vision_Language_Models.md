---
title: Collaborative Multi-Mode Pruning for Vision-Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Collaborative_Multi_Mode_Pruning_for_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/Wuzimeng/CoMP.git"
aliases:
- CMMPC
- CMMPVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 提出协作重要性度量（CIM）消除参数与 token 重要性之间的相互干扰，并引入多模式剪枝策略（MPS）根据剪枝代价、历史信息和随机探索自适应选择最优剪枝模式，实现参数与 token 的协同剪枝。
primary_logic: 视觉语言模型中的参数冗余与数据冗余是耦合的；只有同时优化两者的重要性评估并动态调度剪枝模式，才能在高剪枝率下突破性能瓶颈。
claims:
- 在 NLVR2 剪枝率 0.85 下，CoMP 测试准确率 76.08%，远超 UPop（62.10%）和 MADTP（72.57%），相对提升约 14 和 3.5 个百分点。
- CIM 模块单独带来 0.72% 的测试准确率提升，MPS 进一步带来 1.02% 提升，证明协同重要性度量和自适应模式选择的必要性。
- 在 COCO 图像文本检索上，CoMP 在 BLIP 上 R@1 提升 2.3%，在 CLIP 上提升 2.5%，显示方法跨架构通用。
- NLVR2 (visual reasoning) 上 Test Accuracy (%) = 76.08
---

# Collaborative Multi-Mode Pruning for Vision-Language Models

> [!tip] 核心洞察
> 视觉语言模型中的参数冗余与数据冗余是耦合的；只有同时优化两者的重要性评估并动态调度剪枝模式，才能在高剪枝率下突破性能瓶颈。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向视觉语言模型的协作多模式剪枝 |
| 英文题名 | Collaborative Multi-Mode Pruning for Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.02956) · [Code](https://github.com/Wuzimeng/CoMP.git) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Collaborative Multi-Mode Pruning (CoMP) |
| Dataset | NLVR2, COCO image-text retrieval |

> [!tip] 效果简介
> - NLVR2 (visual reasoning) 上，Test Accuracy (%) 76.08 vs 72.57 (MADTP) (+3.51%)。
> - NLVR2 (visual reasoning, pruning 0.8) 上，Test Accuracy (%) 79.62 vs 77.61 (MADTP) (+2.01%)。
> - COCO image-text retrieval (BLIP, pruning 0.7) 上，Image-to-Text R@1 (%) 76.2 vs 73.9 (MADTP) (+2.3%)。

## 概述

视觉语言模型（VLM）在推理时面临双重计算瓶颈：Transformer 架构固有的参数冗余，以及视觉与语言模态引入的大量 token 冗余。标准 Transformer 块的计算复杂度为 $O(N^2 D + N D^2)$，其中 $N$ 为序列长度，$D$ 为特征维度——两项分别对应 token 和参数带来的开销。现有剪枝方法要么仅压缩参数（如 UPop、M-Pruning），要么仅剪枝 token（如 MADTP、STP），未能同时利用两种模态的冗余。更关键的是，参数重要性度量与 token 重要性度量之间存在**固有矛盾**：低重要性 token 会干扰参数重要性的估计，而被剪枝的参数仍会通过注意力机制影响 token 重要性排序（Figure 2, Figure 5）。简单联合剪枝（SJP）虽然同时进行两种剪枝，但未消除这一跨模式干扰，导致高剪枝率下性能显著退化。

本文提出 **Collaborative Multi-Mode Pruning (CoMP)**，核心洞察在于：VLM 中的参数冗余与数据冗余是**耦合的**——只有同时优化两者的重要性评估并动态调度剪枝模式，才能在高剪枝率下突破性能瓶颈。CoMP 包含两个关键模块：

- **协作重要性度量（CIM）**：通过 token 加权的参数重要性（CIP）和自纠正的 token 重要性（CIT），消除参数与 token 重要性之间的相互干扰。
- **多模式剪枝策略（MPS）**：定义五种剪枝模式（视觉参数、语言参数、跨模态参数、视觉 token、语言 token），基于剪枝代价、历史信息和随机探索，自适应选择每一步的最优剪枝模式。

在 NLVR2 视觉推理任务上，剪枝率 0.85 时 CoMP 测试准确率达 **76.08%**，远超参数剪枝基线 UPop（62.10%）和 token 剪枝基线 MADTP（72.57%），相对提升约 14 和 3.5 个百分点（Table 1）。在 COCO 图像文本检索上，CoMP 在 BLIP 上 R@1 提升 2.3%，在 CLIP 上提升 2.5%，显示方法跨架构通用（Table 2）。消融实验表明，CIM 单独贡献 0.72% 准确率提升，MPS 进一步贡献 1.02%，验证了协同重要性度量和自适应模式选择的必要性（Table 4）。方法代码已开源（https://github.com/Wuzimeng/CoMP.git）。

## 背景与动机

### 视觉语言模型的计算瓶颈

视觉语言模型（VLMs）如 BLIP、CLIP 和 LLaVA 在图像文本检索、视觉问答、视觉推理等跨模态任务上取得了显著进展。然而，这些模型通常基于 Transformer 架构，其计算复杂度为 $O(N^2 D + N D^2)$，其中 $N$ 为序列长度，$D$ 为特征维度。随着模型规模和数据量的增长，高昂的计算开销严重制约了 VLMs 在实际场景中的部署效率。

为缓解这一问题，模型剪枝成为重要的加速手段。现有剪枝方法主要沿两个独立方向发展：

- **参数剪枝（Parameter Pruning）**：移除模型中冗余的权重参数，如结构化稀疏方法 **UPop** 和基于掩码的参数剪枝 **M-Pruning**。
- **Token 剪枝（Token Pruning）**：在推理时动态丢弃不重要的视觉或文本 token，如 **MADTP**、**STP** 和 **Turbo**。

这两种模式分别针对模型的参数冗余和数据冗余，但现有工作始终将它们视为相互独立的优化路径。

### 单一模式剪枝的根本局限

尽管参数剪枝和 token 剪枝各自有效，但 VLMs 中的参数冗余与数据冗余本质上是耦合的。如图 2 所示（参见 Figure 2），在 BLIP 视觉编码器的第 10 层，对参数重要性贡献最大的 token 与注意力机制下最重要的 token 之间重叠度不足 30%；同时，在第 2 层中，75% 的最不重要参数仍然高度影响 token 重要性排序。这揭示了两个深层矛盾：

1. **低重要性 token 干扰参数重要性估计**：标准结构化参数重要性度量（扩展的 Wanda 方法）以均匀方式聚合所有 token 的输入范数：
   $$S_{i,:}^p = \frac{1}{d} \sum_{j=1}^d |W_{i,j}| \cdot ||X_{:,i}||_2$$
   其中冗余 token 的特征与关键 token 的特征被同等对待，导致参数重要性评分被噪声污染。

2. **被剪枝的参数仍影响 token 重要性排序**：token 重要性通常基于最大注意力值计算：
   $$S_i^t = \mathrm{Norm}(\sum_{n=1}^N \max_{h=1,2,\ldots,H} A_{h,n,i})$$
   但当部分注意力头已被参数剪枝掩码置零后，Softmax 的平坦化效应会扰乱剩余 token 的相对重要性排序（参见 Figure 5），使得基于未纠正注意力的 token 剪枝决策偏离最优。

### 简单联合剪枝的失效

一个直观的想法是将参数剪枝和 token 剪枝直接联合执行，即**简单联合剪枝（Simple Joint Pruning, SJP）**——或顺序进行、或同时进行两种剪枝。然而，上述两种重要性度量之间的固有矛盾使得 SJP 效果不佳：参数重要性评估受冗余 token 干扰，而 token 重要性评估又被已剪枝的参数所误导。在高剪枝率下，这种相互干扰会迅速累积，导致性能显著劣于单一模式剪枝（参见 Figure 1 中 SJP 与 CoMP 的对比）。

### 本文动机

综上，现有方法存在三个关键缺口：

- **度量不一致**：参数重要性度量与 token 重要性度量各自独立设计，未考虑跨模式干扰。
- **模式割裂**：参数剪枝和 token 剪枝缺乏协同调度机制，无法在渐进式剪枝过程中动态选择最优剪枝模式。
- **高剪枝率瓶颈**：当剪枝率超过 0.7 时，单一模式或简单联合剪枝的性能急剧下降，亟需新的协作机制突破瓶颈。

基于上述分析，本文提出 **协作多模式剪枝（Collaborative Multi-Mode Pruning, CoMP）**，核心思路是：消除参数与 token 重要性之间的相互干扰，并设计自适应模式调度策略，使两种剪枝模式协同工作而非彼此对抗。

## 核心创新

CoMP 的核心创新在于首次系统性地识别并解决了视觉语言模型（VLM）剪枝中参数剪枝与 token 剪枝之间的**相互干扰问题**，并据此设计了一套协作剪枝框架。其创新点可归纳为两个紧密耦合的 changed slots：**协作重要性度量（CIM）** 与 **多模式剪枝策略（MPS）**。

### 问题洞察：参数与 Token 重要性的耦合矛盾

现有剪枝方法或局限于单一模式（仅参数或仅 token），或简单地将二者联合，却忽视了两者在重要性评估层面的内在冲突。如 Figure 2 的实证分析所示，在 BLIP 视觉编码器的第 10 层，对参数重要性贡献最大的 token 与 token 重要性排序靠前的 token 重叠度不足 30%（Figure 2a）；同时，在第 2 层，约 75% 的最不重要参数仍然高度影响 token 重要性排序（Figure 2b）。这意味着：

- **低重要性 token 会干扰参数重要性的准确估计**：冗余 token 携带的噪声信号通过输入范数传播到参数重要性分数中。
- **被剪枝的参数仍会扭曲 token 重要性排序**：参数剪枝后，冗余注意力头产生的平坦 softmax 分布会扰乱 token 间的相对重要性（Figure 5b）。

这种双向干扰使得简单的联合剪枝（如 SJP）效果不佳，甚至在高剪枝率下劣于单独 token 剪枝。

### Changed Slot 1：协作重要性度量（CIM）

CIM 针对上述双向干扰，分别从参数侧和 token 侧进行重要性度量的修正，形成闭环协作。

**Token 加权参数重要性（CIP）**：标准的结构化参数重要性度量（扩展 Wanda）基于权重幅值与输入特征范数的乘积：

$$S_{i,:}^p = \frac{1}{d} \sum_{j=1}^d |W_{i,j}| \cdot ||X_{:,i}||_2 \quad \text{(Eq. 3)}$$

该公式对每个 token 的输入特征等权对待，未区分 token 的重要性差异。CIP 引入归一化的 token 重要性分数 $\omega_n$ 作为加权系数，将输入范数修正为 token 加权的形式：

$$S_{i,:}^{\prime p} = \frac{1}{d} \sum_{j=1}^d |W_{i,j}| \cdot \left(\sum_{n=0}^N \omega_n \cdot X_{n,i}^2\right)^{\frac{1}{2}}; \quad \omega_0=1; \quad \omega_n = \frac{S_n^t}{\sum_{n=1}^N S_n^t}, n>1 \quad \text{(Eq. 4)}$$

其中 CLS token（$n=0$）保持权重为 1，其余 token 按其重要性分数归一化后加权。这有效抑制了低重要性 token 对参数重要性估计的干扰。

**自纠正 Token 重要性（CIT）**：标准 token 重要性基于最大注意力值计算：

$$S_i^t = \mathrm{Norm}\left(\sum_{n=1}^N \max_{h=1,2,\ldots,H} A_{h,n,i}\right) \quad \text{(Eq. 6)}$$

当参数剪枝掩蔽冗余注意力头后，softmax 的均匀化会破坏 token 间的相对重要性秩（Figure 5b）。CIT 将参数剪枝掩码 $\hat{M}^p$ 直接作用于注意力矩阵，在重要性计算前纠正注意力分布：

$$\hat{\mathbf{A}} = \mathbf{A} \odot \hat{M}^p \quad \text{(Eq. 7)}$$

然后用修正后的 $\hat{\mathbf{A}}$ 替换 $\mathbf{A}$ 代入 Eq. 6 计算 token 重要性。如 Figure 5c 所示，该方式在逐步抑制冗余头的同时保持了正确的 token 重要性排序。

消融实验证实了 CIM 两个子模块的独立贡献：仅使用 CIP 带来 0.39% 的测试准确率提升，仅使用 CIT 带来 0.41% 提升，二者结合效果最佳（Table 5 Top）。完整 CIM 模块单独贡献 0.72% 的准确率增益（Table 4）。

### Changed Slot 2：多模式剪枝策略（MPS）

传统方法在剪枝过程中采用固定顺序或同时进行参数和 token 剪枝，无法根据模型状态动态调整剪枝重点。MPS 将剪枝建模为五种模式的序贯决策问题：视觉参数剪枝（$B_v^p$）、语言参数剪枝（$B_l^p$）、跨模态参数剪枝（$B_c^p$）、视觉 token 剪枝（$B_v^t$）、语言 token 剪枝（$B_l^t$），并在渐进式剪枝的外循环中动态选择最优模式。

**剪枝代价驱动的模式选择**：MPS 定义每种模式的剪枝代价为验证准确率变化与 FLOPs 变化的比值：

$$r = \frac{\Delta val\_acc}{\Delta FLOPs} \quad \text{(Eq. 8)}$$

该代价反映了各模式在当前阶段的“性价比”——代价越低，说明以较小的性能损失换取了较大的计算量缩减。MPS 每 $I$ 步评估一次所有模式的代价，并选择代价最低的模式执行下一轮剪枝。消融显示，仅此成本感知切换（CAS）即带来 0.78% 的准确率提升（Table 5 Bottom）。

**随机探索与历史信息精炼**：为避免贪婪选择陷入局部最优，MPS 引入基于时间间隔的随机探索机制。每种模式被随机选中的概率由其距离上次执行的时间间隔 $I_m$ 决定：

$$I_m = T - \mathcal{T}_m, \quad \rho_m = \mathrm{Softmax}(I_m / \tau) \quad \text{(Eq. 9)}$$

其中 $\tau=5$ 为温度系数，探索比率 $\rho=0.2$。该设计确保长时间未被选中的模式有机会被重新评估，避免过早锁定次优模式。消融表明，随机探索（RE）独立贡献 0.6% 的准确率提升（Table 5 Bottom），且 $\rho$ 在 0.2–0.3 时性能最佳（Table D）。

**历史信息衰减更新**：为平衡历史经验与当前反馈，MPS 使用指数移动平均更新模式代价，并引入线性衰减因子 $\lambda$：

$$\mathcal{R}_m^{\mathrm{cur}} = \lambda \mathcal{R}_m^{\mathrm{pre}} + (1-\lambda) r, \quad \lambda = \max\left(\lambda_0 - \frac{\lambda_0}{I_{\mathrm{max}}}(I_m - 1), 0\right) \quad \text{(Eq. 10)}$$

其中 $\lambda_0=0.4$，$I_{\mathrm{max}}=5$。当某模式长时间未执行时，$\lambda$ 衰减至 0，历史信息完全让位于当前反馈，避免过时信息误导决策。历史信息（HI）机制在消融中亦贡献正面效果（Table 5 Bottom）。Figure 6 的可视化对比显示，带优先级精炼的 MPS 模式切换轨迹更加稳定且多样化。

完整 MPS 模块单独贡献 1.02% 的准确率提升（Table 4），高于 CIM 的 0.72%，表明自适应模式调度对高剪枝率性能至关重要。

### 创新协同：从独立优化到闭环协作

CIM 与 MPS 的协同体现在两个层面：**微观层面**，CIM 在每次剪枝迭代中消除参数与 token 重要性度量的相互干扰，为剪枝决策提供更可靠的重要性排序；**宏观层面**，MPS 利用 CIM 提供的准确重要性信号，动态评估各模式的剪枝代价并选择最优路径。Figure 3 清晰展示了这一嵌套循环结构——内循环执行带掩码的前向传播与 CIM 修正，外循环由 MPS 调度模式切换。

这种闭环设计使得 CoMP 在高剪枝率下展现出显著优势：在 NLVR2 剪枝率 0.85 时，CoMP 测试准确率达 76.08%，远超参数剪枝基线 UPop（62.10%）和 token 剪枝基线 MADTP（72.57%），相对提升分别约 14 和 3.5 个百分点（Table 1）。在 COCO 图像文本检索上，CoMP 在 BLIP 上 R@1 提升 2.3%，在 CLIP 上提升 2.5%（Table 2），验证了方法的跨架构通用性。

## 整体框架

CoMP 通过**嵌套循环**实现参数与 token 的协同渐进剪枝，其核心由两个模块构成：内循环中的**协作重要性度量（CIM）** 负责消除跨模式干扰，外循环中的**多模式剪枝策略（MPS）** 负责动态调度剪枝模式。

### 框架结构

如图 Figure 3 所示，CoMP 的完整 pipeline 分为内外两层：

![[assets/figures/papers/paper_list_l743_https_arxiv_org_abs_2604_02956/figures/004_Figure_3.jpg]]
*Figure 3: Framework overview of CoMP. (a) CoMP performs collaborative parameter and token pruning in nested loops. In the inner loop, input tokens are processed with partially masked parameters. The CIM module mitigates interference of progressive parameter pruning on token importance, and then suppresses the impact of redundant tokens for parameter importance. In the outer loop, the MPS module periodically selects the optimal pruning mode, whose corresponding threshold is adjusted to increase pruning ratio. (b) Given the full VLMs, CoMP compresses them by adaptively pruning parameters in different modalities, while enabling real-time token pruning during inference*

- **内循环（协作剪枝）**：输入 token 在部分被掩码的参数下进行前向传播。CIM 模块首先利用**自纠正 token 重要性（CIT）** 将参数剪枝掩码 $\hat{M}^p$ 作用于注意力矩阵 $\mathbf{A}$，得到修正后的注意力 $\hat{\mathbf{A}} = \mathbf{A} \odot \hat{M}^p$（式 7），以消除被剪枝参数对 token 重要性排序的干扰；随后，基于修正后的 token 重要性分数，对输入特征进行加权，计算**token 加权的参数重要性** $S_{i,:}^{\prime p}$（式 4），从而抑制冗余 token 对参数重要性估计的污染。这一双向纠正机制是 CoMP 突破简单联合剪枝瓶颈的关键。

- **外循环（模式调度）**：MPS 维护五种剪枝模式——视觉参数剪枝、语言参数剪枝、跨模态参数剪枝、视觉 token 剪枝、语言 token 剪枝——并周期性地选择最优模式执行。每次模式选择基于三个机制：
  1. **成本感知切换（CAS）**：计算各模式的剪枝代价 $r = \Delta val\_acc / \Delta FLOPs$（式 8），选择代价最低的模式；
  2. **历史信息（HI）**：通过指数移动平均 $\mathcal{R}_m^{\mathrm{cur}} = \lambda \mathcal{R}_m^{\mathrm{pre}} + (1-\lambda) r$（式 10）平滑代价估计，衰减因子 $\lambda$ 从 $\lambda_0=0.4$ 线性衰减至 0，避免过时信息误导；
  3. **随机探索（RE）**：以概率 $\rho=0.2$ 随机选择模式，模式被选中的概率由距上次执行的时间间隔 $I_m$ 经 Softmax 计算（式 9），防止陷入局部最优。

### 输入输出流

完整 VLM 模型作为输入，CoMP 在渐进剪枝过程中对视觉编码器、语言编码器及跨模态层的参数和 token 进行自适应压缩。剪枝后的模型在推理时可实时执行 token 剪枝，同时保持被剪枝参数的掩码固定。对于 LLaVA 风格的架构，CoMP 将剪枝集中在占总体 FLOPs 95% 以上的 LLM 部分，包括视觉 token、语言 token 和参数的协同剪枝（见 Figure A）。

### 关键设计动机

框架设计的根本驱动力来自实证发现（Figure 2）：在 BLIP 视觉编码器中，对参数重要性贡献最大的 token 与 token 重要性排名靠前的 token 重叠度不足 30%；同时，75% 的最不重要参数仍对 token 重要性有显著影响。这种**参数与 token 重要性度量之间的固有矛盾**使得简单联合剪枝难以奏效，而 CoMP 通过 CIM 的双向纠正和 MPS 的自适应调度，系统性地解决了这一瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l743_https_arxiv_org_abs_2604_02956/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of different pruning modes for VLMs, with accuracy on NLVR2. For (i) parameter and (ii) token pruning, distinct modalities are simultaneously pruned under a unified ratio adjustment. For (iii) simple joint pruning, parameter and token pruning are conducted either sequentially or simultaneously without mitigating their inherent inconsistency. For (iv) our proposed CoMP, distinct pruning modes collaborate and only the optimal one is conducted at each stage in the progressive pruning process*

![[assets/figures/papers/paper_list_l743_https_arxiv_org_abs_2604_02956/figures/015_Figure.jpg]]
*Figure: A. Illustration of extending CoMP to the LLaVA-style architecture. We perform pruning in the LLM component, including pruning of vision tokens, language tokens and parameters, since this part accounts for more than 95% of the overall FLOPs*

## 核心模块与公式推导

CoMP 框架由两个核心模块构成：**协作重要性度量（CIM）** 负责消除参数与 token 重要性评估之间的相互干扰；**多模式剪枝策略（MPS）** 负责在渐进式剪枝过程中自适应选择最优剪枝模式。以下逐一推导其关键公式与机理。

### 3.1 剪枝掩码的统一形式

CoMP 对参数和 token 分别维护二进制剪枝掩码：

$$M^p = \mathbb{I}(S^p > \theta^p), \quad M^t = \mathbb{I}(S^t > \theta^t) \quad \text{(Eq. 1)}$$

其中 $S^p$、$S^t$ 分别为参数和 token 的重要性分数，$\theta^p$、$\theta^t$ 为可学习阈值。参数剪枝后的前向传播为：

$$Z = \phi(X W_{in} \odot M^p) W_{out} + X \quad \text{(Eq. 2)}$$

$\phi$ 为激活函数，$\odot$ 表示逐元素乘法。该形式同时适用于 FFN 和 MHA 子层，区别仅在于掩码 $M^p$ 映射到的结构维度（FFN 的通道或 MHA 的头）。

### 3.2 协作重要性度量（CIM）

CIM 包含两个子模块：**token 加权的参数重要性（CIP）** 和 **自纠正的 token 重要性（CIT）**，分别解决低重要性 token 干扰参数重要性估计、以及被剪枝参数扰乱 token 重要性排序这两个瓶颈。

#### 3.2.1 Token 加权的参数重要性（CIP）

基础的结构化参数重要性度量（扩展 Wanda）为：

$$S_{i,:}^p = \frac{1}{d} \sum_{j=1}^d |W_{i,j}| \cdot \|X_{:,i}\|_2 \quad \text{(Eq. 3)}$$

其中 $W_{i,j}$ 为权重矩阵第 $i$ 行第 $j$ 列的元素，$X_{:,i}$ 为输入特征第 $i$ 通道的激活向量，$d$ 为输出维度。该公式对所有 token 的激活值等权求和，未区分 token 本身的重要性。

CIP 引入 token 重要性分数作为加权因子：

$$S_{i,:}^{\prime p} = \frac{1}{d} \sum_{j=1}^d |W_{i,j}| \cdot \left(\sum_{n=0}^N \omega_n \cdot X_{n,i}^2\right)^{\frac{1}{2}} \quad \text{(Eq. 4)}$$

其中 $\omega_0 = 1$（CLS token 保持原权重），对于 $n > 1$：

$$\omega_n = \frac{S_n^t}{\sum_{n=1}^N S_n^t}$$

$S_n^t$ 为第 $n$ 个 token 的重要性分数。该加权机制使低重要性 token 对参数重要性估计的贡献被抑制，从而更准确地反映参数对关键信息的处理能力。

#### 3.2.2 自纠正的 token 重要性（CIT）

基础 token 重要性基于最大注意力值：

$$S_i^t = \mathrm{Norm}\left(\sum_{n=1}^N \max_{h=1,2,\ldots,H} A_{h,n,i}\right) \quad \text{(Eq. 6)}$$

其中 $A$ 为注意力矩阵，$H$ 为注意力头数，$\mathrm{Norm}$ 为归一化操作。当部分参数被剪枝后，冗余注意力头产生平坦的 softmax 分布，扰乱 token 重要性排序（见 Figure 5）。

![[assets/figures/papers/paper_list_l743_https_arxiv_org_abs_2604_02956/figures/006_Figure_5.jpg]]
*Figure 5: Illustration of interference between parameter pruning and token importance. (a) Without pruning, token1 is more important than token2. (b) Baseline pruning method masks redundant head1 by Eq. (2), flattens softmax, and distorts ranks of token importance. (c) By masking with Eq. (7), head1 is gradually suppressed without disrupting correct ranks of token importance*

CIT 将参数剪枝掩码直接作用于注意力矩阵以纠正该干扰：

$$\hat{\mathbf{A}} = \mathbf{A} \odot \hat{M}^p \quad \text{(Eq. 7)}$$

其中 $\hat{M}^p$ 为参数剪枝掩码在注意力头维度上的对应映射。随后使用 $\hat{\mathbf{A}}$ 替代原 $\mathbf{A}$ 代入 Eq. (6) 计算 token 重要性。该操作在逐步抑制冗余头的同时，保持了正确的 token 重要性秩次（Figure 5c）。

### 3.3 多模式剪枝策略（MPS）

MPS 定义五种剪枝模式：$\mathcal{B} = \{B_v^p, B_l^p, B_c^p, B_v^t, B_l^t\}$，分别对应视觉参数、语言参数、跨模态参数、视觉 token、语言 token 的剪枝。核心机制是**基于代价感知的模式选择**。

#### 3.3.1 剪枝代价定义

每次模式切换时，MPS 在验证集上评估当前模式的剪枝代价：

$$r = \frac{\Delta val\_acc}{\Delta FLOPs} \quad \text{(Eq. 8)}$$

$r$ 为验证准确率变化与 FLOPs 变化的比值，反映该模式在当前阶段的“性价比”。$r$ 越小，说明以较少精度损失换取较大计算量削减，模式越优。

#### 3.3.2 模式选择概率

为避免陷入局部最优，MPS 以概率 $\rho$ 进行随机探索，以概率 $1-\rho$ 选择历史代价最低的模式。随机探索时，各模式被选中的概率由其距上次执行的时间间隔决定：

$$I_m = T - \mathcal{T}_m, \quad \rho_m = \mathrm{Softmax}(I_m / \tau) \quad \text{(Eq. 9)}$$

$T$ 为当前总步数，$\mathcal{T}_m$ 为模式 $m$ 上次执行的步数，$\tau$ 为温度系数（默认 $\tau=5$）。间隔越久的模式被随机选中的概率越高，保证所有模式获得充分探索。

#### 3.3.3 代价的指数移动平均更新

为避免过时信息误导决策，MPS 使用带衰减的 EMA 更新各模式代价：

$$\mathcal{R}_m^{\mathrm{cur}} = \lambda \mathcal{R}_m^{\mathrm{pre}} + (1-\lambda) r \quad \text{(Eq. 10)}$$

$$\lambda = \max\left(\lambda_0 - \frac{\lambda_0}{I_{\mathrm{max}}}(I_m - 1), 0\right)$$

$\lambda_0 = 0.4$，$I_{\mathrm{max}} = 5$。衰减因子 $\lambda$ 随模式距上次执行间隔 $I_m$ 线性递减至 0：间隔越久，历史信息的权重越低，当前反馈 $r$ 的权重越高。这确保了长期未执行的模式能以最新代价重新参与竞争。

### 3.4 模块间协作机制

CIM 与 MPS 以内-外循环方式协同工作（Figure 3a）。内循环中，输入 token 经过部分掩码的参数处理，CIM 同时计算 token 加权的参数重要性和自纠正的 token 重要性。外循环中，MPS 周期性评估各模式代价并选择下一剪枝模式，相应阈值 $\theta$ 被更新以提升剪枝率。消融实验（Table 4）表明：在 NLVR2 剪枝率 0.8 下，单独移除 CIM 导致测试准确率下降 0.72%，单独移除 MPS 导致下降 1.02%，验证了两模块在高剪枝率下不可替代的协同作用。

> **注意**：上述公式均来自原论文 Eq. (1)–(10)，变量含义与原文一致。关于 CIM 内部 CIP 与 CIT 的独立贡献（分别提升 0.39% 和 0.41%）以及 MPS 内部 CAS、RE、HI 组件的细粒度消融，详见 Table 5。

### 补充图表

![[assets/figures/papers/paper_list_l743_https_arxiv_org_abs_2604_02956/figures/005_Figure_4.jpg]]
*Figure 4: Illustration of the CIM module. (a) adopts token-weighted input norm for parameter importance. (b) applies parameter pruning mask to the attention weight matrix for token importance*

![[assets/figures/papers/paper_list_l743_https_arxiv_org_abs_2604_02956/figures/003_Figure_2.jpg]]
*Figure 2: (a) At*

## 实验与分析

### 核心实验设计

本文在视觉推理（NLVR2）、图文检索（Flickr30K / COCO）、图像描述（COCO Captioning）、视觉问答（VQAv2）以及多模态大语言模型（LLaVA-v1.5-7B）等任务上系统评估 CoMP。所有实验均在 2 块 NVIDIA A800 GPU 上完成，基线方法均使用原论文开源代码复现。剪枝率统一定义为整体 FLOPs 减少比例，参数剪枝与 token 剪枝在该预算下由 MPS 模块自适应分配。

### 视觉推理任务主结果（NLVR2）

Table 1 报告了 BLIP 模型在 NLVR2 上不同剪枝率下的开发集/测试集准确率与 GFLOPs。CoMP 在中低剪枝率（≤0.6）下与最优基线持平，而在高剪枝率（≥0.7）下显著拉开差距：

![[assets/figures/papers/paper_list_l743_https_arxiv_org_abs_2604_02956/figures/007_Table_1.jpg]]
*Table 1: Comparison of Dev./Test Acc. (%) and GFLOPs by various pruning methods for BLIP on NLVR2 with distinct pruning ratios for the visual reasoning task. ‘P’, ‘T’, ‘J’ and ‘C’ denote parameter pruning, token pruning, joint pruning and collaborative pruning, respectively. ‘SJP’ stands for the simple joint pruning baseline. The best results are highlighted in bold*

- 剪枝率 0.85：CoMP 测试准确率 **76.08%**，远超 UPop（62.10%）和 MADTP（72.57%），相对提升分别约 14 和 3.5 个百分点。
- 剪枝率 0.80：CoMP 测试准确率 **79.62%**，较 MADTP（77.61%）提升 2.01 个百分点。
- 简单联合剪枝基线 SJP 在 0.85 剪枝率下仅 63.09%，表明未经协同设计的联合剪枝反而劣于单一模式剪枝，验证了跨模式干扰的存在及其严重性。

### 图文检索与描述任务主结果

Table 2（上半部分）展示了 BLIP 和 CLIP 在 Flickr30K 与 COCO 图文检索任务上的性能。在剪枝率 0.7 下：

![[assets/figures/papers/paper_list_l743_https_arxiv_org_abs_2604_02956/figures/008_Table_2.jpg]]
*Table 2: (Top) Comparison of R@1/5 (%) and GFLOPs for BLIP/CLIP on Flickr30K and COCO for the image-text retrieval task. (Bottom) Comparison of CIDEr and SPICE on COCO for the image captioning task and Test-dev/std accuracy (%) on VQAv2 for the visual question answering task as well as GFLOPs, based on BLIP. ‘*’ indicates GFLOPs during inference by our re-implementation, which were not reported in the original works. The best results are highlighted in bold*

- BLIP 在 COCO Image-to-Text R@1 上达到 **76.2%**，较 MADTP（73.9%）提升 2.3 个百分点。
- CLIP 在 Flickr30K Image-to-Text R@1 上达到 **79.0%**，较 MADTP（76.5%）提升 2.5 个百分点，验证方法跨架构通用性。

Table 2（下半部分）的图像描述任务中，CoMP 在 CIDEr 和 SPICE 指标上均优于所有对比方法；VQAv2 上 CoMP 在 Test-dev 和 Test-std 准确率上同样取得最优。但作者指出 VQAv2 缺少独立验证集，限制了 MPS 中基于验证损失的评估机制，可能削弱了该任务上的增益。

### 多模态大语言模型结果（LLaVA-v1.5-7B）

Table 3 报告了 LLaVA-v1.5-7B 在 6 个常用基准上的平均性能与 TFLOPs。CoMP 在剪枝率 0.7 下平均得分 **63.2**，显著优于 Turbo（60.1）和 MADTP（61.5），且逼近部分训练感知方法。值得注意的是，CoMP 仅进行一轮 SFT，而训练感知方法（† 标注）通常需要完整微调，这表明协作剪枝在 LLM-based VLM 上同样有效。但当前实验未探索更充分的微调设置和更大规模模型，该方向的扩展性仍需进一步验证。

![[assets/figures/papers/paper_list_l743_https_arxiv_org_abs_2604_02956/figures/009_Table_3.jpg]]
*Table 3: Comparison of performance and TFLOPs by various pruning methods on LLaVA-v1.5-7B with distinct pruning ratios on 6 commonly-used benchmarks. The ‘Average’ column summarizes the average score across all tasks. ‘†’ indicates that supervised fine-tuning is involved. The best results are highlighted in bold and the second-best results are underlined*

### 消融实验：CIM 与 MPS 的独立贡献

Table 4 在 NLVR2 剪枝率 0.8 下对两大模块进行消融：

![[assets/figures/papers/paper_list_l743_https_arxiv_org_abs_2604_02956/figures/011_Table_4.jpg]]
*Table 4: Ablation results of CIM and MPS on NLVR2 dataset at a pruning ratio of 0.8*

- 移除 CIM（仅保留 MPS）：测试准确率下降 **0.72%**。
- 移除 MPS（仅保留 CIM）：测试准确率下降 **1.02%**。
- 同时移除两者（退化为简单联合剪枝）：准确率大幅下降。

这证明协作重要性度量和自适应模式选择对高剪枝率性能均不可或缺，且 MPS 的调度能力贡献略大于 CIM 的度量修正。

### 细粒度消融：CIM 内部机制

Table 5（上半部分）进一步拆解 CIM：

![[assets/figures/papers/paper_list_l743_https_arxiv_org_abs_2604_02956/figures/012_Table_5.jpg]]
*Table 5: (Top) Effect of CIP and CIT in CIM. CIP and CIT are token-weighted parameter importance and self-corrected token importance, respectively. (Bottom) Effect of CAS, RE and HI in MPS. CAS, RE and HI indicates pruning cost-aware mode shifting, random exploration and historical information, respectively. All experiments are conducted on NLVR2 at a pruning ratio of 0.8*

- 仅使用 token 加权的参数重要性（CIP）：提升 **0.39%**。
- 仅使用自纠正 token 重要性（CIT）：提升 **0.41%**。
- 二者结合（完整 CIM）：提升 **0.72%**，效果近似可加，说明参数侧与 token 侧的干扰是独立且互补的。

### 细粒度消融：MPS 内部组件

Table 5（下半部分）对 MPS 的三个关键组件进行消融：

- 成本感知模式切换（CAS）：单独贡献 **0.78%**，是 MPS 中最关键的机制。
- 随机探索（RE）：单独贡献 **0.60%**，有效避免模式选择陷入局部最优。
- 历史信息（HI）：单独贡献正面，但与 CAS 结合时增益更显著。

超参数敏感性分析（Table D–G）进一步揭示：

- 随机探索比率 ρ 在 **0.2–0.3** 时性能最佳，过小（ρ=0）易陷入局部最优，过大（ρ=0.5）导致不稳定。
- 衰减因子 λ₀=**0.4**、I_max=**5** 在历史信息利用与当前反馈间取得最优平衡。

### 实际推理延迟与加速比

Table C 报告了 BLIP-NLVR2 在剪枝率 0.85 下的实际推理延迟。CoMP 在 GFLOPs 减少 85% 的同时，单张图像推理延迟从 32.1ms 降至 **8.7ms**，加速比 **3.7×**，优于 MADTP（3.1×）和 UPop（2.8×）。这得益于 MPS 在参数剪枝与 token 剪枝间的动态平衡——token 剪枝直接缩短序列长度，对自注意力计算量的降低是二次方的。

### 模式切换行为可视化

Figure 6 展示了 MPS 在 NLVR2 剪枝率 0.8 下的模式选择轨迹。带优先级精炼（priority refinement）的 MPS 在早期阶段频繁探索多种模式，随后逐渐收敛到以视觉参数剪枝和视觉 token 剪枝为主的稳定策略；而不带优先级精炼的版本模式切换杂乱，最终收敛到次优组合。Figure C 进一步量化了各模式对总 FLOPs 减少的贡献分布，验证了 MPS 的自适应分配能力。

![[assets/figures/papers/paper_list_l743_https_arxiv_org_abs_2604_02956/figures/010_Figure_6.jpg]]
*Figure 6: Visualization of pruning mode shifting in MPS with (w/) and without (w/o) priority refinement on NLVR2 at 0.8 pruning ratio. Colored points represent the next selected mode at each stage*

### 跨框架正交性验证

Table J 将 CoMP 的 CIM+MPS 与不同参数剪枝框架（UPop、Isomorphic Pruning）结合，结果表明 CoMP 的协作策略与底层参数剪枝框架正交，均可带来一致的性能提升。这为 CoMP 作为通用剪枝调度层的推广提供了实证支持。

### 稳定性与泛化性

Table H 在 5 个随机种子下对比 CoMP 与 MADTP 的均值和标准差：CoMP 在 NLVR2 测试准确率和 COCO R@1 上均表现出更小的方差，说明 MPS 中的历史信息机制有效平滑了剪枝过程中的随机波动。Table I 的零样本视频文本检索（MSR-VTT）实验中，CoMP 同样优于 MADTP，验证了跨任务泛化能力。

### 已知局限与失败模式

1. **VQAv2 增益受限**：该任务无独立验证集，MPS 的模式选择依赖验证损失近似，可能导致次优调度。
2. **MPS 额外评估成本**：每次模式切换需在验证集上重新评估剪枝代价，对大规模数据集引入额外开销。作者指出可通过采样缓解，但未给出具体方案。
3. **中等剪枝率优势不明显**：在剪枝率 ≤0.6 时，CoMP 与 token-only 剪枝方法的性能差距较小，方法的核心价值集中在高剪枝率场景。
4. **LLM-based VLM 探索不充分**：LLaVA 实验仅进行一轮 SFT，更大规模模型和更充分微调设置下的表现有待验证。
5. **与 token 合并技术的结合**：当前方法仅做 token 丢弃，未与 token 合并等更激进的冗余消除技术联合优化，该方向的潜力尚未释放。

## 方法谱系与知识库定位

### 1. 问题定位：从单模式剪枝到协作剪枝

视觉语言模型（VLM）的推理成本由 Transformer 的二次计算复杂度 $O(N^2D + ND^2)$ 主导，其中 $N$ 为 token 序列长度，$D$ 为特征维度。现有剪枝方法沿两条独立路径发展：**参数剪枝**（parameter pruning）通过移除冗余权重减少 $D$，而 **token 剪枝**（token pruning）通过丢弃非信息性 token 压缩 $N$。然而，这两类方法均局限于单一模式，未能利用两种模式间的互补冗余。

CoMP 的核心发现是：参数冗余与 token 冗余并非独立，而是**深度耦合**的。具体而言，存在两个方向的干扰：
- **低重要性 token 干扰参数重要性估计**：在计算参数重要性时，冗余 token 的输入特征会稀释关键 token 的贡献，导致重要性排序失真。
- **被剪枝的参数仍影响 token 重要性排序**：参数剪枝后，冗余注意力头产生的平坦 softmax 分布会扰乱 token 重要性的正确秩（见 Figure 5）。

这一洞察将问题从“分别剪枝”重新定义为“协作剪枝”，即需要同时优化两者的重要性评估并动态调度剪枝模式。

### 2. 基线谱系与 CoMP 的定位

CoMP 的实验对比覆盖了以下方法类别，构成完整基线谱系：

| 类别 | 代表方法 | 机制 | 局限性（在 CoMP 视角下） |
|------|----------|------|--------------------------|
| 纯参数剪枝 | **UPop**、**M-Pruning** | 基于权重幅值或梯度的重要性度量，结构化移除参数 | 忽略 token 冗余；参数重要性受冗余 token 干扰 |
| 纯 token 剪枝 | **MADTP**、**STP** | 基于注意力分数的 token 重要性排序与丢弃 | 忽略参数冗余；被剪枝参数仍影响 token 排序 |
| 简单联合剪枝 | **Turbo**、**SJP** | 同时或顺序执行参数与 token 剪枝 | 未解决两种重要性度量间的相互干扰，联合效果不佳 |
| 训练感知方法 | LLaVA 上的 SFT 基线 | 剪枝后进行监督微调恢复性能 | 需要额外训练成本；未从剪枝策略层面优化 |

CoMP 相对于这些基线的**方法论增量**体现在三个层面：
1. **协作重要性度量（CIM）**：通过 token 加权参数重要性（CIP）和自纠正 token 重要性（CIT），首次显式建模并消除跨模式干扰。
2. **多模式剪枝策略（MPS）**：将剪枝建模为模式选择问题，通过成本感知、历史信息和随机探索动态调度五种剪枝模式。
3. **渐进式剪枝框架**：在嵌套循环中逐步提升剪枝率，使参数与 token 剪枝在统一调度下协同演进。

### 3. 适用边界与泛化性

**已验证的适用场景：**
- **架构**：BLIP、CLIP、LLaVA-v1.5-7B，覆盖 dual-encoder 和 LLM-based VLM 两种主流架构。
- **任务**：视觉推理（NLVR2）、图像文本检索（Flickr30K、COCO）、图像描述（COCO）、视觉问答（VQAv2）、零样本视频文本检索（MSR-VTT）。
- **剪枝率区间**：0.5–0.85，在高剪枝率（≥0.7）下优势显著。

**跨架构泛化证据：**
- 在 BLIP 的 COCO 检索任务上，CoMP 的 R@1 提升 2.3%；在 CLIP 上提升 2.5%，显示方法对 dual-encoder 架构的通用性（Table 2）。
- 在 LLaVA-v1.5-7B 的 6 个常用基准上，CoMP 在平均分数上优于所有对比方法（Table 3），验证了向 LLM-based VLM 的扩展能力。
- CoMP 可与不同参数剪枝框架（UPop、Isomorphic Pruning）结合，表现出一致的性能增益（Table J），说明 CIM 和 MPS 是正交于具体剪枝框架的增强模块。

**已知局限：**
- **验证集依赖**：MPS 在每次模式切换时需在验证集上重新评估剪枝代价，对大数据集引入额外计算开销。虽可通过采样缓解，但仍需权衡。
- **中等剪枝率优势有限**：在剪枝率 ≤0.6 时，CoMP 与 MADTP 等 token 剪枝基线的性能差距不明显，说明协作剪枝的增益主要集中在高压缩率场景。
- **VQAv2 性能受限**：VQAv2 无单独验证集，无法充分使用 MPS 的验证评估机制，可能限制了该任务上的性能增益。
- **LLM-based VLM 探索不充分**：对 LLaVA 的实验仅进行了一轮 SFT，未探索更充分的微调设置以及更大规模模型（如 LLaVA-1.6、GPT-4V 系列）的扩展性。
- **与激进 token 压缩技术的结合**：方法尚未与 token 合并（token merging）等更激进的 token 减少技术深度结合，联合优化潜力待进一步研究。

### 4. 开放问题

1. **MPS 评估成本优化**：如何进一步降低 MPS 的额外评估成本，使其适用于更大规模数据或更频繁的模式切换？可能的路径包括基于梯度信号的代理指标替代验证集评估，或使用轻量级性能预测器。

2. **更大规模 LLM-based VLM 的适配**：在最新的多模态 LLM（如 LLaVA-1.6、GPT-4V 及其后续）上，CoMP 的协作剪枝策略是否依然有效？LLaVA 风格架构中 LLM 部分占整体 FLOPs 的 95% 以上（Figure A），vision token、language token 和参数的协同剪枝在更大规模模型上是否会出现新的干扰模式？

3. **理论最优的模式分配**：参数剪枝和 token 剪枝的最终比例分配是否存在理论最优解？当前 MPS 通过在线成本感知动态决定，但能否根据任务特性和模型结构预先推导全局最佳划分？这涉及压缩率-精度帕累托前沿的理论刻画。

4. **协作重要性度量的跨技术推广**：CIM 的核心思想——消除不同压缩模式间的相互干扰——能否推广到其他模型压缩技术？例如，在量化中，低重要性 token 的激活值分布是否也会干扰量化参数的选取？在知识蒸馏中，被剪枝的参数是否仍影响软标签的质量？

5. **极高剪枝率下的能力坍塌**：当剪枝率极高时（如 >0.9），模型能力是否存在坍塌点？Figure C 显示不同剪枝模式对 FLOPs 减少的贡献分布，但未揭示性能坍塌的临界条件。如何预测并规避该坍塌点是部署高压缩率模型的关键问题。

6. **与训练感知方法的深度融合**：当前 CoMP 主要在后训练（post-training）剪枝框架下工作，与 SFT 等训练感知方法的结合仅在 LLaVA 实验中初步探索。协作剪枝策略与微调的联合优化（如剪枝模式调度与训练步数的协同）可能进一步释放性能潜力。

## 原文 PDF

![[paperPDFs/CVPR_2026/Collaborative_Multi_Mode_Pruning_for_Vision_Language_Models.pdf]]
