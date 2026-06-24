---
title: "Attention Surgery: An Efficient Recipe to Linearize Your Video Diffusion Transformer"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Attention_Surgery_An_Efficient_Recipe_to_Linearize_Your_Video_Diffusion_Transformer.pdf
project_link: "https://qualcomm-ai-research.github.io/attention-surgery"
code_link: null
aliases:
- AS
- ASERLYVDT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/benchmarks_datasets_evaluation
core_operator: 通过将部分 token 保留完整 softmax 注意力作为全局时空锚点，其余 token 使用可学习的多项式核线性注意力，配合注意力蒸馏与轻量微调，可在预训练模型上以极低训练成本实现高效线性化；同时，基于块级变换复杂度的混合率优化进一步平衡表达力与效率。
primary_logic: 关键洞察在于：少量全局软注意力 token 足以维持视频的时空一致性与运动连贯性，而大部分 token 可以使用线性注意力显著降低计算复杂度，再通过逐层蒸馏和整体微调恢复生成质量。
claims:
- 在 Wan2.1 1.3B 中，超过 76% 的 Transformer 块计算量来自自注意力。
- Attention Surgery 合成的 15×R2 混合模型在 VBench 上得分 83.21，与原始 Wan2.1 83.10* 持平，且用户研究中无显著偏好差异。
- 整体手术耗时不足 0.4k GPU 小时，远低于从头训练所需的数十万 GPU 小时。
- "VBench 上 Total Score ↑ = 83.21 (Ours: 15×R2)"
---

# Attention Surgery: An Efficient Recipe to Linearize Your Video Diffusion Transformer

> [!tip] 核心洞察
> 关键洞察在于：少量全局软注意力 token 足以维持视频的时空一致性与运动连贯性，而大部分 token 可以使用线性注意力显著降低计算复杂度，再通过逐层蒸馏和整体微调恢复生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 注意力手术：一种高效线性化视频扩散Transformer的方法 |
| 英文题名 | Attention Surgery: An Efficient Recipe to Linearize Your Video Diffusion Transformer |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.24899) · [Project](https://qualcomm-ai-research.github.io/attention-surgery) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/benchmarks_datasets_evaluation |
| Method | Attention Surgery |
| Dataset | VBench, VBench-2.0, User Study, On-mobile Efficiency |

> [!tip] 效果简介
> - VBench 上，Total Score ↑ 83.21 (Ours: 15×R2) vs 83.10 (Wan2.1 1.3B reproduced*) (+0.11)。
> - VBench-2.0 上，Total Score ↑ 55.1 (Ours: 15×R2) vs 56.0 (Wan2.1 1.3B) (-0.9)。
> - User Study (562 comparisons) 上，Preference % 31.0% Ours / 39.7% No preference vs 29.3% Wan2.1 1.3B (无显著整体偏好差异)。

## 概述

视频扩散Transformer（Video Diffusion Transformer, VDT）在生成高质量视频方面展现出强大能力，但其核心组件——自注意力机制的二次复杂度（$O(N^2d)$）——已成为实际应用的主要效率瓶颈。以 **Wan2.1 1.3B**（Wan et al., 2025）为例，Transformer 块内超过 **76%** 的计算量消耗在自注意力操作上，这严重制约了长序列、高分辨率视频生成的效率，尤其是在移动端等资源受限场景。

针对这一瓶颈，本文提出 **Attention Surgery**，一种高效的“手术式”框架，能够在预训练视频扩散模型上以极低的训练成本实现注意力机制的线性化。其核心思想是：**少量全局 softmax 注意力 token 足以维持视频的时空一致性与运动连贯性，而大部分 token 可以使用线性注意力显著降低计算复杂度**，再通过逐层蒸馏和整体微调恢复生成质量。

方法上，Attention Surgery 将流程解耦为三个阶段：（1）**注意力蒸馏**——对每个 Transformer 块独立训练可学习的多项式核特征映射，使其输出逼近原始 softmax 注意力；（2）**异质块率选择优化**——基于各块蒸馏误差与计算成本，在给定计算预算下求解多选择背包问题，为不同深度分配差异化的软/线性 token 混合率；（3）**轻量微调**——在蒸馏完成后对整个模型进行少量迭代微调，恢复细节与整体生成质量。

实验表明，Attention Surgery 合成的 **15×R2 混合模型**在 VBench 上得分 **83.21**，与原始 Wan2.1 1.3B 的复现结果（83.10）持平；在 **562 组用户研究中**，用户对手术模型与原始模型无显著偏好差异（31.0% vs. 29.3%，39.7% 无偏好）。整个“手术”过程耗时不足 **0.4k GPU 小时**，远低于从头训练所需的数十万 GPU 小时，在 Snapdragon8-Gen4 移动端上实现了约 **6 倍**的推理加速。

在方法谱系上，Attention Surgery 属于**后训练线性化**路线，区别于从零训练线性注意力模型（如 **Mamba**、**RWKV**）或对预训练模型进行全量微调的方案。它借鉴了线性注意力中核技巧的思想（Katharopoulos et al., 2020），但通过引入**可学习多项式核**与**值蒸馏损失**（$\mathcal{L}_{\mathrm{vd}}$）增强表达能力，并以**异质块率分配**替代均匀混合策略，在效率与质量之间取得更优平衡。当前方法在 Wan2.1 1.3B 上验证，对其他视频 DiT 架构（如 CogVideoX、HunyuanVideo）及更大规模模型的迁移性尚待研究；其采用的双向注意力设计也尚未与因果注意力结合，因此在自回归长视频生成场景中注意力成本仍随帧数增长。

## 背景与动机

### 视频扩散 Transformer 的效率瓶颈

视频扩散模型（Video Diffusion Models, VDMs）近年来在文本到视频生成领域取得了显著进展，但其核心架构——基于 Transformer 的扩散主干网络（Diffusion Transformer, DiT）——面临一个根本性的效率瓶颈：**自注意力机制的二次计算复杂度**。在标准的 softmax 自注意力中，每个 token 需要与序列中的所有 token 进行交互，其计算复杂度为 $O(N^2 d)$，其中 $N$ 为 token 数量（帧数 × 每帧 token 数），$d$ 为特征维度。对于高分辨率、长时域的视频生成任务，$N$ 可轻易达到数万甚至数十万量级，导致单次前向传播的计算量和内存开销急剧膨胀。

这一瓶颈在实际模型中表现得尤为突出。以 **Wan2.1 1.3B**（Wan et al., 2025）为例，在 Transformer 块内部，**超过 76% 的计算量消耗在自注意力操作上**。这意味着即便模型的其他组件（如前馈网络、归一化层）已高度优化，自注意力仍然是制约推理速度和部署可行性的绝对主导因素。对于移动端部署等资源受限场景，这一开销使得实时视频生成几乎不可行。

### 现有线性化方法的局限

针对注意力机制的二次复杂度问题，研究者提出了多种线性化方案。其中最具代表性的是基于**核技巧（kernel trick）** 的线性注意力（Katharopoulos et al., 2020），其核心思想是将 softmax 中的指数核替换为可分解的特征映射 $\phi(\cdot)$，从而将计算顺序从 $(QK^\top)V$ 重排为 $Q(K^\top V)$，实现 $O(N d^2)$ 的线性复杂度。然而，这类方法在视频扩散模型中面临两个关键挑战：

1. **表达能力不足**：线性注意力舍弃了 softmax 的指数归一化特性，在建模长程依赖和精确的 token 间交互时存在固有劣势。直接替换全部自注意力层会导致生成质量显著下降，表现为时空一致性受损、运动连贯性减弱。

2. **从头训练成本高昂**：若要将线性注意力集成到视频 DiT 中，传统方法需要从头开始预训练整个模型。对于 Wan2.1 1.3B 这类规模的模型，从头训练需要**数十万 GPU 小时**的计算资源，使得大多数研究团队难以承担探索成本。

### 核心动机与关键洞察

本文的核心动机在于回答一个关键问题：**能否在不从头训练的前提下，将预训练视频 DiT 中的自注意力高效地线性化，同时保持生成质量？**

作者的关键洞察是：**并非所有 token 都需要完整的 softmax 注意力**。在视频生成中，少量全局 softmax 注意力 token 足以充当“时空锚点”，维持视频的时空一致性与运动连贯性；而大部分 token 可以使用计算高效的线性注意力来处理。这一洞察催生了**混合注意力机制（hybrid attention）** 的设计：将 token 分为两组——一组保留完整 softmax 注意力（按混合率 $R$ 均匀下采样），另一组采用可学习的多项式核线性注意力。

基于此，本文提出 **Attention Surgery（注意力手术）** 框架，通过三个核心模块实现高效线性化：

- **注意力蒸馏（Attention Distillation）**：以预训练模型的 softmax 注意力输出为教师信号，逐层训练线性注意力的特征映射参数，使其模拟原始注意力的行为。
- **异质块率优化（Heterogeneous Block-Rate Optimization）**：不同 Transformer 块对注意力的敏感度不同，通过求解多选择背包问题，在给定计算预算下为每个块分配最优的混合率。
- **轻量微调（Lightweight Fine-tuning）**：在蒸馏和混合率选择完成后，对完整模型进行少量迭代的端到端微调，恢复因注意力替换而丢失的细节信息。

整个“手术”过程仅需**不足 0.4k GPU 小时**，相比从头训练的数十万 GPU 小时，效率提升三个数量级以上。这一框架使得在预训练模型上探索注意力机制的线性化成为一项低成本、可复现的操作，为视频扩散模型的实际部署开辟了新路径。

## 核心创新

Attention Surgery 的核心创新在于将预训练视频扩散 Transformer (VDM) 中的标准 softmax 自注意力，以极低的训练成本转换为高效的混合注意力机制，而非从头训练新模型。其关键设计围绕三个“changed slots”展开，共同构成一个完整的手术式线性化框架。

### 1. 混合注意力机制：全局锚点与线性主体

标准 softmax 自注意力对所有 token 执行 $O(N^2d)$ 的密集交互，这是视频生成的主要计算瓶颈——在 Wan2.1 1.3B 中，超过 76% 的 Transformer 块计算量源于此。Attention Surgery 提出一种**混合注意力** (Hybrid Attention) 策略，将输入 token 解耦为两个子集：

- **软注意力 token $T_S$**：按混合率 $R$ 对全序列进行均匀下采样，保留完整的 softmax 注意力计算。这些 token 充当全局时空锚点，维持视频的时空一致性与运动连贯性。
- **线性注意力 token $T_L$**：其余 token 使用线性注意力，通过核技巧将计算复杂度降至 $O(Nd^2)$。

混合注意力的统一形式为：

$$\hat{y}_i = \frac{\sum_{j \in T_S} \exp(q_i k_j^\top / \sqrt{D} - c_i) v_j + \phi_q(q_i) \left(\sum_{j \in T_L} \phi_k(k_j)^\top v_j\right)}{\sum_{j \in T_S} \exp(q_i k_j^\top / \sqrt{D} - c_i) + \phi_q(q_i) \left(\sum_{j \in T_L} \phi_k(k_j)^\top\right)}$$

这一设计的核心洞察在于：少量全局软注意力 token 足以锚定视频的关键时空结构，而大部分 token 可以使用线性注意力大幅降低计算量，从而在表达力与效率之间取得平衡。

### 2. 可学习多项式核：超越固定特征映射

传统线性注意力通常依赖固定的特征映射（如 **elu-based** 核，Katharopoulos et al., 2020），表达能力有限。Attention Surgery 引入**可学习的多项式特征映射** $\phi$，将输入 $x$ 映射为多项式展开形式：

$$\phi(\boldsymbol{x}) = [(\psi_1(\boldsymbol{x}))^1, (\psi_2(\boldsymbol{x}))^2, \ldots, (\psi_P(\boldsymbol{x}))^P]^\intercal \in \mathbb{R}^{P \times D'}$$

其中 $\psi$ 由轻量 MLP 实现。实验表明，**2 层 MLP + 2 次多项式展开**在效率与效果间取得最佳平衡，每个转换块仅增加约 2.4M 参数。这一设计使线性注意力分支具备更强的拟合能力，能够更好地逼近原始 softmax 注意力的行为。

### 3. 三阶段手术式训练管线

Attention Surgery 将线性化过程解耦为三个独立阶段，以极低的训练成本（总计不足 0.4k GPU 小时）完成从预训练模型到混合模型的转换：

- **逐块注意力蒸馏**：对每个 Transformer 块独立训练 $\phi_q$、$\phi_k$，使其混合注意力输出逼近教师模型的 softmax 注意力。蒸馏损失包含两种形式——注意力得分匹配损失 $\mathcal{L}_{\mathrm{ad}}$（对数形式，增强数值稳定性）和值蒸馏损失 $\mathcal{L}_{\mathrm{vd}}$（直接匹配输出值的 L1 距离）。消融实验表明，值蒸馏损失能带来更丰富的运动信息（如 20×R8 配置下，Dynamic Degree 从 37.5 提升至 66.1）。

- **异质块率选择优化**：不同 Transformer 块的注意力模式复杂度各异，统一使用相同混合率并非最优。该方法将块率选择建模为**多选择背包问题**：在给定计算预算 $\beta$ 下，基于每块的蒸馏误差 $e_{ir}$ 和计算成本 $c_{ir}$，为每个块选择最优混合率 $r$，以最小化累计误差。实验证明，异质策略在多个计算预算下均持续优于同质基线。

- **轻量整体微调**：在蒸馏和块率选择完成后，对完整 DiT 模型进行少量迭代（数百次）的微调，恢复因注意力替换而丢失的细节与整体生成质量。定性结果显示，低混合率模型在蒸馏后即可获得较好的重建效果，而微调能显著缩小与原始模型的质量差距。

这三个阶段的协同设计，使得 Attention Surgery 能够在保持与原始 Wan2.1 1.3B 模型相当的生成质量（VBench 总分 83.21 vs 83.10，用户研究无显著偏好差异）的同时，实现约 6× 的移动端推理加速。

## 整体框架

Attention Surgery 的整体设计围绕一个核心观察展开：在 Wan2.1 1.3B 这类视频扩散 Transformer 中，自注意力计算消耗了 Transformer 块内超过 76% 的算力，而其中大量 token 间的交互对最终生成质量的贡献并非同等重要。基于此，该方法提出了一种“手术式”的线性化方案——在不从头训练的前提下，将预训练模型中的全量 softmax 注意力替换为混合注意力，并通过极低成本的蒸馏与微调恢复生成质量。

### 三阶段流水线

整个框架被解耦为三个顺序执行且相互解耦的阶段，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l838_https_arxiv_org_abs_2509_24899/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the attention distillation for the proposed attention surgery method. The example illustrates token separation with a hybridization rate of 3*

1. **注意力蒸馏阶段（Attention Distillation）**  
   对预训练 DiT 的每一个 Transformer 块进行独立蒸馏。该阶段仅训练两个轻量特征映射函数 $\phi_q$ 和 $\phi_k$，以最小化学生混合注意力输出与教师 softmax 注意力输出之间的差异。蒸馏过程逐块进行，块与块之间完全独立，无需跨层交互，从而大幅降低了训练复杂度和内存占用。

2. **块级混合率选择优化（Block-Rate Selection Optimization）**  
   在完成逐块蒸馏后，每个块在不同混合率 $R$ 下会产生不同的蒸馏误差 $e_{ir}$ 和计算成本 $c_{ir}$。该阶段将这一问题形式化为多选择背包问题：在给定的整体计算预算 $\beta$ 约束下，为每个块选择一个混合率，使得所有块的累计蒸馏误差最小化。这一异质块率选择策略使得浅层和深层可以根据各自对误差的敏感度采用不同的混合率，从而在效率与质量之间取得更优平衡。

3. **轻量微调（Lightweight Fine-tuning）**  
   在确定每个块的混合率并完成蒸馏后，对整个 DiT 架构进行少量迭代（通常仅数百步）的微调。该阶段使用中等规模的 prompt-视频对数据集，旨在恢复因注意力替换而丢失的细节纹理与整体生成质量。Figure 4 的定性结果表明，仅靠蒸馏不足以弥合质量差距，而轻量微调能显著缩小这一差距。

### 输入输出流

- **输入**：预训练视频扩散 Transformer 模型（如 Wan2.1 1.3B）及其标准 softmax 自注意力权重。
- **处理**：通过上述三阶段流水线，将原始的全 softmax 注意力块逐步替换为混合注意力块——其中部分 token 保留 softmax 注意力作为全局时空锚点，其余 token 使用可学习多项式核的线性注意力。
- **输出**：一个线性化/混合注意力版本的 DiT 模型，在 VBench 上可达到与原始模型相当的生成质量（15×R2 配置下 VBench 总分 83.21 vs. 原始 83.10*），同时大幅降低计算开销。

### 关键设计决策

- **逐块独立蒸馏**：避免了端到端蒸馏所需的大量计算资源，使整个手术过程的总训练成本控制在 0.4k GPU 小时以内。
- **异质块率选择**：不同 Transformer 块对注意力近似的敏感度差异显著（Figure 3），统一混合率会导致某些块过度压缩或浪费算力，异质选择策略在所有预算条件下均优于同质基线（Table 5）。
- **可学习多项式核**：相比传统的 elu 固定特征映射，采用 2 层 MLP 配合 2 次多项式展开的 $\phi$ 变换，在仅增加约 2.4M 参数/块的情况下，显著提升了线性注意力的表达能力（Table 7）。

这一框架的整体优势在于其**低成本可迁移性**：无需修改预训练模型的主体结构，无需大规模重新训练，即可将任意基于 softmax 注意力的视频 DiT 转化为高效的混合注意力版本。

### 补充图表

![[assets/figures/papers/paper_list_l838_https_arxiv_org_abs_2509_24899/figures/001_Figure_1.jpg]]
*Figure 1: Left: Impact of the proposed method components: attention distillation and hybrid attention. The linear/hybrid models are obtained within fewer than 0.4k GPU-hours. Prompt: “An astronaut flying in space, Van Gogh style.”. Right: Compute growth comparison between Wan2.1 1.3B flash attention blocks and of attention surgery on FLOPs (top) and Snapdragon8-Gen4 mobile latency (bottom)*

## 核心模块与公式推导

### 3.1 问题定义与标准自注意力

视频扩散Transformer（DiT）的每一层可形式化为：

$$T _ { l } ( x ) = f _ { l } { \big ( } A _ { l } ( x ) + x { \big ) }$$

其中 $A_l$ 为自注意力操作，$f_l$ 为前馈网络。标准 softmax 自注意力的计算方式为：

$$A _ { l } ( x ) = y = \operatorname { s o f t m a x } \left( \frac { q k ^ { \top } } { \sqrt { D } } \right) v$$

其计算复杂度为 $O(N^2d)$，其中 $N$ 为 token 数量，$d$ 为特征维度。在 Wan2.1 1.3B 模型中，Transformer 块内超过 76% 的计算量消耗在自注意力上，这构成了视频生成效率的核心瓶颈。

### 3.2 混合注意力机制

Attention Surgery 的核心创新在于提出混合注意力机制，将 token 集合 $T = \{1, \dots, N\}$ 解耦为两类：**softmax token** $T_S$ 和**线性 token** $T_L = T \setminus T_S$。

softmax token 按混合率 $R$ 进行均匀下采样：$T_S = \{\bar{i} \in \bar{T} \mid i \bmod R = 1\}$。混合注意力的输出定义为：

$$\hat { y } _ { i } = \frac { \sum _ { j \in T _ { S } } \exp \left( q _ { i } k _ { j } ^ { \top } / \sqrt { D } - c _ { i } \right) v _ { j } + \phi _ { q } ( q _ { i } ) \left( \sum _ { j \in T _ { L } } \phi _ { k } ( k _ { j } ) ^ { \top } v _ { j } \right) } { \sum _ { j \in T _ { S } } \exp \left( q _ { i } k _ { j } ^ { \top } / \sqrt { D } - c _ { i } \right) + \phi _ { q } ( q _ { i } ) \left( \sum _ { j \in T _ { L } } \phi _ { k } ( k _ { j } ) ^ { \top } \right) }$$

其中 $c_i$ 为数值稳定项。该公式的关键设计在于：对 $T_S$ 中的 token 保留完整 softmax 注意力以维持全局时空一致性，对 $T_L$ 中的 token 则使用线性注意力（通过核技巧实现 $O(Nd^2)$ 复杂度）。

线性注意力的基础形式利用核技巧将注意力计算重排为：

$$y _ { i } = \frac { \phi ( q _ { i } ) \sum _ { j = 1 } ^ { N } \phi ( k _ { j } ) ^ { \top } v _ { j } } { \phi ( q _ { i } ) \sum _ { j = 1 } ^ { N } \phi ( k _ { j } ) ^ { \top } }$$

### 3.3 可学习多项式核特征映射

为增强线性注意力的表达能力，Attention Surgery 采用可学习的多项式核特征映射，替代传统 ELU 固定映射（Katharopoulos et al., 2020）：

$$\phi ( \boldsymbol { x } ) = [ ( \psi _ { 1 } ( \boldsymbol { x } ) ) ^ { 1 } , ( \psi _ { 2 } ( \boldsymbol { x } ) ) ^ { 2 } , \ldots , ( \psi _ { P } ( \boldsymbol { x } ) ) ^ { P } ] ^ { \intercal } \in \mathbb { R } ^ { P \times D ^ { \prime } }$$

其中 $\psi_p(\cdot)$ 为小型 MLP 的第 $p$ 个输出通道，$P$ 为多项式展开的最高次数。实验表明，2 层 MLP 配合 2 次多项式展开在效率与效果间取得最佳平衡，每块仅增加约 2.4M 参数。

### 3.4 注意力蒸馏

注意力蒸馏阶段对每个 Transformer 块独立进行，训练 $\phi_q$、$\phi_k$ 以模拟教师模型的 softmax 注意力输出。蒸馏损失包含两个互补的损失函数。

**注意力得分蒸馏损失** 采用对数形式以增强数值稳定性：

$$\mathcal { L } _ { \mathrm { a d } } = \log \Big ( 1 + \big \| e ^ { q _ { i } k _ { j } ^ { \top } } - \phi _ { q } ( q _ { i } ) \phi _ { k } ( k _ { j } ) ^ { \top } \big \| _ { 2 } ^ { 2 } \Big )$$

**值蒸馏损失** 直接匹配混合注意力输出与教师 softmax 注意力输出的 L1 距离：

$$\mathcal { L } _ { \mathrm { v d } } = \| y - \hat { y } \| _ { 1 }$$

消融实验表明，值蒸馏损失相较于注意力得分蒸馏损失能带来更丰富的运动信息（例如 20×R8 配置下 Dynamic Degree 从 37.5 提升至 66.1），这是因为直接匹配输出值能更好地保留视频中的动态特征。

### 3.5 异质块率选择优化

不同 Transformer 块对注意力近似的敏感度不同。Attention Surgery 将块率选择建模为多选择背包问题，在给定计算预算 $\beta$ 下最小化累计蒸馏误差：

$$\operatorname* { m i n } _ { \{ z _ { i r } \} } \sum _ { i = 1 } ^ { B } \sum _ { r \in { \mathcal R } } e _ { i r } z _ { i r } \quad \mathrm { s . t . } \sum _ { i = 1 } ^ { B } \sum _ { r \in { \mathcal R } } c _ { i r } z _ { i r } \leq \beta , \ \sum _ { r \in { \mathcal R } } z _ { i r } = 1 \forall i , \ z _ { i r } \in \{ 0 , 1 \}$$

其中 $B$ 为总块数，$\mathcal{R}$ 为候选混合率集合，$e_{ir}$ 为第 $i$ 块在混合率 $r$ 下的蒸馏误差，$c_{ir}$ 为对应的计算成本。该优化使不同块可根据自身特性选择不同的混合率，在相同计算预算下持续获得优于同质配置的 VBench 总分。

### 3.6 轻量微调

蒸馏和块率选择完成后，对完整 DiT 模型进行少量迭代（数百次）的微调，使用中等规模的 prompt/视频数据对来恢复蒸馏过程中丢失的细节与整体生成质量。整个 Attention Surgery 流程的总训练成本不足 0.4k GPU 小时，远低于从头训练所需的数十万 GPU 小时。

### 补充图表

![[assets/figures/papers/paper_list_l838_https_arxiv_org_abs_2509_24899/figures/003_Figure_3.jpg]]
*Figure 3: Per-block distillation error (top-left) and compute implications of*

![[assets/figures/papers/paper_list_l838_https_arxiv_org_abs_2509_24899/figures/004_Figure_4.jpg]]
*Figure 4: Sample qualitative video frames from hybrid models with varying numbers of hybrid blocks (15, 20, 25) and hybrid rates (2, 4, 8). For each configuration, the left frame shows the result after layer-wise attention distillation, and the right frame shows the result after 1,000 fine-tuning iterations. Prompt: A man is reading a book sitting on the cloud*

## 实验与分析

### 核心定量结果：质量持平，效率大幅提升

论文的核心主张是：**Attention Surgery 能够在保持生成质量与原始模型无显著差异的前提下，将视频扩散 Transformer 中自注意力的计算开销降低数倍。** 主要证据来自 VBench 基准与用户研究。

- **VBench 总分**：在 Wan2.1 1.3B 上，最优混合配置 `15×R2` 的 VBench 总分为 **83.21**，与作者复现的原始 Wan2.1\* 得分 **83.10** 持平（+0.11，Table 1）。该配置意味着 15 个 Transformer 块被替换为混合注意力，且混合率为 2（即每 2 个 token 中保留 1 个做完整 softmax 注意力）。
- **用户研究**：在 562 组盲法配对比较中，`15×R2` 模型获得 31.0% 的偏好，原始 Wan2.1 获得 29.3% 的偏好，另有 39.7% 的比较无偏好差异（Table 2）。**无显著整体偏好差异**，进一步支撑了“质量不可区分”的结论。
- **移动端实测效率**：在 Snapdragon8-Gen4 平台上，Attention Surgery 的混合块在生成 7.5 秒视频时，相比 Wan2.1 1.3B 的 Flash Attention 块**快约 6 倍**（Fig. 1 右）。这直接验证了线性化对端侧部署的收益。

![[assets/figures/papers/paper_list_l838_https_arxiv_org_abs_2509_24899/figures/006_Table_1.jpg]]
*Table 1: Comparisons with SOTA efficient video diffusion*

### 消融实验：三个关键组件的因果作用

#### 1. 注意力蒸馏是质量恢复的基石

Table 3 直接对比了有无注意力蒸馏时混合/线性模型的 VBench 总分：

![[assets/figures/papers/paper_list_l838_https_arxiv_org_abs_2509_24899/figures/008_Table_3.jpg]]
*Table 3: VBench scores comparison of linear/hybrid models with and without attention distillation*

- 纯线性模型 `15×Linear`：无蒸馏时 VBench 仅 **59.7**，蒸馏后跃升至 **78.9**（+19.2）。
- 混合模型 `20×R8`：无蒸馏时 **77.3**，蒸馏后 **80.0**（+2.7）。

**结论**：注意力蒸馏对于纯线性模型是“雪中送炭”，对于混合模型则是“锦上添花”——混合率越低（线性 token 越多），蒸馏的增益越显著。Fig. 6 的定性示例也佐证了这一点：无蒸馏的 `15×Linear` 几乎完全丧失运动连贯性，而蒸馏后恢复了合理的时空结构。

#### 2. 值蒸馏损失优于注意力得分蒸馏损失

Table 6 对比了两种蒸馏目标：

![[assets/figures/papers/paper_list_l838_https_arxiv_org_abs_2509_24899/figures/010_Table_6.jpg]]
*Table 6: Comparison of distillation loss types, as measured by VBench scores*

- 注意力得分蒸馏（$\mathcal{L}_{\text{ad}}$）：匹配 softmax 注意力权重的对数形式。
- 值蒸馏（$\mathcal{L}_{\text{vd}}$）：直接匹配注意力输出值的 L1 距离。

以 `20×R8` 为例，值蒸馏的 **动态程度（Dynamic Degree）** 为 **66.1**，远高于注意力得分蒸馏的 **37.5**，且 VBench 总分也更高（80.0 vs 77.3）。这表明**值蒸馏能更好地保留视频中的运动信息**，而单纯匹配注意力图容易导致动作趋于静态。

#### 3. 异质块率选择持续优于同质配置

Table 5 展示了在多个计算预算约束下，异质块率选择策略（即不同块使用不同混合率 R）与同质策略的对比。**在所有预算条件下，异质策略的 VBench 总分均边际优于同质基线。** 这验证了 Fig. 3 中观察到的现象：不同块的蒸馏误差和计算成本差异显著，一刀切的混合率无法最优利用计算预算。

![[assets/figures/papers/paper_list_l838_https_arxiv_org_abs_2509_24899/figures/011_Table_5.jpg]]
*Table 5: Impact of the proposed heterogeneous block-rate selection strategy under different budget constraints. Our method consistently leads to marginally better total VBench score*

#### 4. 可学习多项式核的复杂度权衡

Table 7 消融了 $\phi$ 变换的复杂度（MLP 层数与多项式阶数 P）：

![[assets/figures/papers/paper_list_l838_https_arxiv_org_abs_2509_24899/figures/012_Table_7.jpg]]
*Table 7: VBench total scores for various hybrid architectures with different complexities of the learnable ϕ transformation, varying in MLP depth and polynomial degree*

- **2 层 MLP + 2 阶多项式**在效率与效果间取得最佳平衡，每个转换块仅增加约 **2.4M** 参数。
- 继续增加 MLP 深度或多项式阶数带来的 VBench 增益微乎其微，但计算开销显著上升。

### 效率-质量权衡曲线

Fig. 5 绘制了不同混合配置下 DiT 总 FLOPs 百分比与 VBench 分数的关系（分辨率 320×480 和 480×832）：

![[assets/figures/papers/paper_list_l838_https_arxiv_org_abs_2509_24899/figures/005_Figure_5.jpg]]
*Figure 5: The total DiT FLOPs percentages versus the VBench score of original Wan2.1 1.3B model compared to various hybrid configurations or 320×480 (left) and 480×832 (right) resolutions*

- `15×R2` 配置在 **约 60% 的原始 FLOPs** 下达到与原始模型相当的 VBench 分数。
- 更激进的配置（如 `25×R8`）可将 FLOPs 降至 **约 40%**，但 VBench 分数下降约 2-3 点。
- 在 480×832 高分辨率下，效率优势更加明显，因为自注意力的二次复杂度在高分辨率时占比更大。

### 失败模式与局限性

1. **低混合率下的运动退化**：当混合率 R 较大（如 R=8）或混合块数较多时，视频的动态程度和运动连贯性会下降。Fig. 4 的定性结果显示，`25×R8` 在蒸馏后立即出现明显伪影，微调虽能部分恢复，但仍弱于低混合率配置。
2. **VBench-2.0 上的微弱劣势**：在更新的 VBench-2.0 基准上，`15×R2` 总分为 **55.1**，略低于原始 Wan2.1 的 **56.0**（-0.9，Table 4）。这表明新基准可能对某些维度（如细粒度运动质量）更敏感，但差距仍在可接受范围内。
3. **高分辨率微调依赖教师模型**：论文提到高分辨率微调使用了 Wan2.1 14B 生成的合成数据，这引入了额外的计算与数据准备成本，且该依赖关系在正文实验中未做消融。
4. **未覆盖因果注意力**：当前方法基于双向注意力，尚未结合因果注意力，因此在自回归长视频生成中注意力成本仍随帧数增长（尽管增速低于二次复杂度）。

![[assets/figures/papers/paper_list_l838_https_arxiv_org_abs_2509_24899/figures/009_Table_4.jpg]]
*Table 4: A quantitative comparison on VBench-2.0 benchmark*

### 补充图表

![[assets/figures/papers/paper_list_l838_https_arxiv_org_abs_2509_24899/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative illustration of impact of attention distillation on two hybrid architecture instances (15×Linear and 20×R8). Prompt: ”A playful golden retriever bounds through a sunlit meadow, its fur gleaming in the warm afternoon light.”*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

**Attention Surgery** 的核心动机源于视频扩散 Transformer（VDM）中自注意力机制的二次复杂度瓶颈：在 **Wan2.1 1.3B**（Wan et al., 2025）中，超过 76% 的 Transformer 块计算量消耗在自注意力上。该方法并非从头训练一个高效模型，而是以后训练（post-training）方式对预训练 VDM 进行“手术式”改造，其方法定位可从以下几条谱系理解：

- **相对于标准 Softmax 自注意力（Vaswani et al., 2017）**：Attention Surgery 将均匀的全量 softmax 注意力替换为“混合注意力”——对按混合率 $R$ 均匀下采样的 token 子集 $T_S$ 保留完整 softmax，其余 token $T_L$ 使用线性注意力。这一设计直接回应了原始注意力 $O(N^2d)$ 的扩展性问题，同时保留了少量全局 softmax token 作为时空锚点以维持视频的时空一致性。

- **相对于线性注意力（Katharopoulos et al., 2020）**：经典线性注意力使用固定的 ELU 特征映射实现核技巧，复杂度降为 $O(Nd^2)$。Attention Surgery 在此基础上做了两处关键改进：(1) 将固定特征映射替换为**可学习的多项式核特征映射** $\phi(\boldsymbol{x}) = [(\psi_1(\boldsymbol{x}))^1, \ldots, (\psi_P(\boldsymbol{x}))^P]^\intercal$，通过 2 层 MLP 与 $P$ 次多项式展开增强表达能力；(2) 并非全量替换，而是与 softmax token 混合，形成**混合注意力机制**。消融实验表明，纯线性模型（15×Linear）在 VBench 上仅得 59.7 分，而经注意力蒸馏后跃升至 78.9 分，验证了可学习特征映射与蒸馏策略对线性注意力表达力的补偿作用。

- **相对于其他高效视频扩散模型**：论文在 VBench 上将 Attention Surgery 与现有高效方法进行了系统对比（Table 1）。15×R2 混合模型取得 83.21 的总分，与复现的原始 Wan2.1（83.10）持平，且用户研究（562 组对比）显示无显著偏好差异。这表明该方法在保持生成质量的同时实现了实质性的效率提升——在 Snapdragon8-Gen4 移动端上，单个块的延迟降低约 6×。

### 2. 适用边界与前提条件

Attention Surgery 的有效性依赖以下前提，这些也构成了其适用边界：

- **预训练 VDM 可用性**：该方法假设已有一个训练完备的 softmax 注意力 VDM 作为教师模型。当前验证限于 Wan2.1 1.3B 架构，对其他 DiT 架构（如 CogVideoX、HunyuanVideo）或不同参数规模的迁移性尚待研究。

- **双向注意力假设**：当前框架采用双向（非因果）注意力，适用于一次性生成固定长度视频的场景。在自回归长视频生成中，因果注意力机制下注意力成本仍随帧数增长（尽管增速低于二次），尚未实现真正的 RNN 式恒定成本。

- **高分辨率微调的数据依赖**：高分辨率（480×832）微调阶段依赖教师模型（Wan2.1 14B）生成的合成视频数据，这引入了额外的计算与数据准备成本，限制了完全自监督的端到端部署。

### 3. 局限性与已知失效模式

- **架构迁移未验证**：所有实验均在 Wan2.1 1.3B 上完成。该方法的核心组件（逐层蒸馏、异质块率选择、可学习多项式核）是否适用于不同架构设计（如不同的归一化策略、注意力头数、时空分离方式）仍需验证。

- **低混合率下的初始质量下降**：Figure 4 的定性消融显示，在仅经蒸馏而未微调时，低混合率（如 R=8）模型的生成质量明显劣于高混合率（R=2）模型。轻量微调可显著缩小这一差距，但微调迭代次数与数据量的最优配置仍需针对不同场景调整。

- **VBench-2.0 上的轻微退化**：在 VBench-2.0 基准上，15×R2 模型总分 55.1，略低于原始 Wan2.1 的 56.0（-0.9）。这表明在更细粒度的视频质量评估维度上，混合注意力可能在某些子维度存在可感知的退化，需进一步分析具体失分维度。

### 4. 开放问题与后续工作方向

论文明确指出了以下开放问题：

1. **线性注意力与因果注意力的融合**：如何将线性注意力与因果注意力结合，构建注意力成本不随视频长度增长的 RNN 式视频扩散模型，是实现无限长视频生成的关键挑战。

2. **跨架构泛化**：该方法能否推广到其他基于 DiT 的图像/视频生成模型（如 CogVideoX、HunyuanVideo），以及不同参数规模（如 14B 级别）下的表现如何，是工程落地的重要问题。

3. **大规模下的最优混合策略**：在更大规模或更高分辨率下，混合注意力的最优混合率 $R$ 与异质块选择策略是否会发生变化？当前的多选择背包优化框架提供了形式化工具，但其在大规模空间的扩展性尚待验证。

4. **值蒸馏损失的机理理解**：消融实验（Table 6）表明，值蒸馏损失 $\mathcal{L}_{\mathrm{vd}}$ 相比注意力得分蒸馏损失 $\mathcal{L}_{\mathrm{ad}}$ 能带来显著更丰富的运动信息（Dynamic Degree: 66.1 vs 37.5），但其深层原因——值空间蒸馏是否更好地保留了 token 间的协同运动模式——仍需进一步的理论分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/Attention_Surgery_An_Efficient_Recipe_to_Linearize_Your_Video_Diffusion_Transformer.pdf]]