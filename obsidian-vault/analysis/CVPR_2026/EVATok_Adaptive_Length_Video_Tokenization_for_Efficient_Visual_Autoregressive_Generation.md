---
title: "EVATok: Adaptive Length Video Tokenization for Efficient Visual Autoregressive Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EVATok_Adaptive_Length_Video_Tokenization_for_Efficient_Visual_Autoregressive_Generation.pdf
project_link: null
code_link: null
aliases:
- EVATok
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过最大化代理奖励（权衡重建质量与令牌成本）为每个视频确定最优令牌分配（各时间块的令牌数），并利用轻量级路由器在训练和推理中预测该最优分配，实现内容自适应的可变长度标记化。
primary_logic: 内容自适应的令牌分配能够根据视频片段的运动复杂性、布局复杂性和重复性动态调整令牌数量，从而在更少的平均令牌消耗下实现更好的重建质量与下游生成性能。关键创新在于用代理奖励定义“最优分配”，并训练路由器避免每次暴力搜索，且最终标记器直接使用路由器分配训练以消除训练-推理差距。
claims:
- 在WebVid验证集上，路由器引导的最终标记器与固定均匀分配相比，节省29.6%的令牌，同时rFVD从63降至33，大幅改善。
- 在UCF-101上，路由器引导的最终标记器以24.4%的令牌节省实现持平的rFVD（13），且下游AR生成gFVD从98降至96（改善）。
- 系统级比较中，EVATok以774个标记（-24.4%）达到rFVD 9.7，并在UCF-101 class-to-video生成上用756个标记（-26.2%）达到gFVD 48，优于LARP（1024标记，gFVD 57）等先前SOTA。
- 质量-成本权衡曲线显示，最大代理奖励策略（max-proxy-reward）在所有预算水平上均优于固定均匀分配，且路由器分配紧跟最大代理奖励曲线，在未见过的UCF-101上依然有效。
---

# EVATok: Adaptive Length Video Tokenization for Efficient Visual Autoregressive Generation

> [!tip] 核心洞察
> 内容自适应的令牌分配能够根据视频片段的运动复杂性、布局复杂性和重复性动态调整令牌数量，从而在更少的平均令牌消耗下实现更好的重建质量与下游生成性能。关键创新在于用代理奖励定义“最优分配”，并训练路由器避免每次暴力搜索，且最终标记器直接使用路由器分配训练以消除训练-推理差距。

| 字段 | 内容 |
|------|------|
| 中文题名 | EVATok：自适应长度视频标记化以实现高效视觉自回归生成 |
| 英文题名 | EVATok: Adaptive Length Video Tokenization for Efficient Visual Autoregressive Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.12267) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | EVATok |
| Dataset | WebVid validation, UCF-101 reconstruction, UCF-101 class-to-video generation, K600 frame prediction |

> [!tip] 效果简介
> - WebVid validation 上，rFVD ↓ 33 (Router Final Tok.) vs 63 (Uniform Final Tok.) (-47.6%)；#rTokens 721 vs 1024 (-29.6%)。
> - UCF-101 reconstruction 上，rFVD ↓ 9.7 (EVATok 145M) vs 20 (LARP-L-Long 173M) (-51.5%)。
> - UCF-101 class-to-video generation 上，gFVD ↓ 48 (EVATok 633M AR) vs 57 (LARP-L-Long 632M AR) (-15.8%)。

## 概述

### 问题与瓶颈

视频自回归生成模型依赖将高维视频压缩为离散令牌序列。传统视频标记化对所有时间块分配**固定数量令牌**，忽略视频内容复杂度的剧烈差异：简单、静态或高度重复的片段消耗与动态、布局复杂片段相同的令牌预算，导致简单片段浪费令牌而复杂片段令牌不足。这一固定分配策略成为限制视频标记化效率与重建保真度的核心瓶颈。

### 核心思路

EVATok 提出**内容自适应的可变长度视频标记化**，核心逻辑是让令牌分配跟随视频内容复杂度动态调整——动态运动与复杂布局的时间块获得更多令牌，重复或简单块获得更少令牌。实现这一目标的关键创新在于：

1. **代理奖励（Proxy Reward）**：定义一个权衡重建质量与令牌成本的标量指标，将“最优令牌分配”形式化为最大化该奖励的搜索问题。
2. **路由器预测**：训练一个轻量级路由器（ViT-S）直接从视频预测最优分配，避免每次暴力搜索。
3. **消除训练-推理差距**：用路由器预测的分配从头训练最终标记器，使训练和推理使用完全一致的分配策略。

### 方法定位

EVATok 构建了一个四阶段框架（Figure 2）：
- **阶段1**：训练代理标记器，使其能在任意随机采样的令牌分配下重建视频。
- **阶段2**：用代理标记器为大量视频计算所有候选分配的代理奖励，选取最大化奖励的分配，构建 (视频, 最优分配) 数据集。
- **阶段3**：训练路由器预测最优分配。
- **阶段4**：用路由器指导的分配从头训练最终标记器。

在架构层面，EVATok 采用 **Q-Former 风格的1D可变长度标记器**（Figure 3）：根据分配确定各时间块的1D查询数量，通过因果注意力编码与矢量量化产生离散令牌，再解码重建视频帧。训练中引入 **V-JEPA2 表示对齐损失**和可选的 **VideoMAE 语义鉴别器**以提升感知质量。

### 主要结果

在 WebVid 验证集上，路由器引导的最终标记器相比固定均匀分配**节省29.6%令牌**（721 vs 1024），同时 rFVD 从63降至33（Table 1）。在 UCF-101 上，以**24.4%令牌节省**实现持平的 rFVD，下游自回归生成 gFVD 从98改善至96（Table 2）。

系统级比较中，EVATok 以774个重建令牌（-24.4%）在 UCF-101 上达到 rFVD 9.7，并在 class-to-video 生成任务上以756个令牌（-26.2%）达到 gFVD 48，优于先前最优的固定长度方法 **LARP**（1024令牌，gFVD 57）（Table 3）。在 K600 帧预测任务上，EVATok 以15.8%更少生成令牌取得最佳 gFVD 4.0（Table 4）。

质量-成本权衡曲线（Figure 4）表明，最大代理奖励策略在所有预算水平上均优于固定均匀分配，且路由器分配紧贴最优曲线，在未见过的 UCF-101 数据集上同样有效。消融实验（Table 5）证实 V-JEPA2 表示对齐和 VideoMAE 语义鉴别器对重建与生成质量均有显著贡献。

## 背景与动机

### 视频标记化的效率瓶颈

视觉自回归（AR）生成模型在视频合成领域展现出巨大潜力，但其核心依赖的离散标记化（tokenization）环节正面临日益突出的效率挑战。当前主流的视频标记器——无论是基于3D VAE的方案还是基于Q-Former的方案——普遍采用**固定长度标记化**策略：将视频沿时间维度划分为若干时间块（temporal block），并为每个块分配**相同数量**的离散令牌。这一“一刀切”的做法忽视了一个根本事实：视频片段的内容复杂度存在巨大差异。

具体而言，固定均匀分配导致两类系统性浪费：
- **简单/静态/重复片段**被过度编码，消耗了不必要的令牌预算；
- **动态/复杂/布局密集片段**则令牌不足，重建保真度受限。

这种错配在整体上表现为：在给定令牌总预算下，视频重建质量（以rFVD等指标衡量）远未达到最优；同时，冗余令牌又推高了下游AR生成模型的计算成本——因为生成模型需要逐令牌预测，令牌数量直接决定推理开销。

### 现有自适应方法的局限

学界已意识到固定长度标记化的低效问题，并提出了若干自适应方案，但均存在关键缺陷：

- **AdapTok** 采用mini-batch整数线性规划（ILP）确定令牌分配，但该方法优化的是批次级目标，可能与单个视频的全局最优分配存在偏差，且ILP求解本身引入额外计算开销。
- **ElasticTok** 及类似的**阈值搜索方法**（threshold-based assignment）基于LPIPS等重建误差指标，在推理时丢弃尾部令牌以实现可变长度。然而，这种“尾令牌丢弃”（tail-token-dropping）机制导致训练与推理阶段令牌角色不一致——训练时模型学习所有令牌的语义，推理时却截断尾部，造成严重的**训练-推理差距**（training-inference gap）。此外，丢弃策略需要先编码完整令牌序列再截断，并未真正减少编码阶段的计算量。

### 核心动机与研究问题

上述分析揭示了一个清晰的因果旋钮：**如果能够根据每个视频片段的内容复杂度，在标记化阶段就确定最优的令牌分配方案，就有可能在更少的平均令牌消耗下实现更好的重建质量和下游生成性能。** 这引出了三个必须解决的核心问题：

1. **如何定义“最优分配”？** 需要一个可量化的度量标准，同时兼顾重建质量与令牌成本，且能够在合理计算开销下评估。
2. **如何快速获取最优分配？** 对每个视频暴力搜索所有候选分配的计算复杂度为 $O(m^T)$（$m$ 为每块候选令牌数，$T$ 为时间块数），在实际应用中不可行。
3. **如何消除训练-推理差距？** 标记器在训练时若学习所有可能的分配，但在推理时仅使用特定分配，会导致性能下降；需要一种机制使训练与推理阶段的令牌分配保持一致。

EVATok正是围绕这三个问题展开，通过**代理奖励最大化**定义最优分配、**轻量级路由器**实现快速预测、以及**四阶段训练框架**消除训练-推理差距，构建了首个端到端的内容自适应视频标记化系统。

## 核心创新

EVATok 的核心创新在于将视频标记化从“固定长度均匀分配”范式转变为**内容自适应的可变长度标记化**，并通过一套四阶段框架高效实现该目标。其关键设计围绕以下四个 changed slots 展开。

### 1. 内容自适应的令牌分配策略（Router-predicted Adaptive Assignment）

传统视频标记化方法（如 LARP 及本文的固定均匀基线）对所有时间块分配相同数量的令牌，完全忽略视频片段间的运动复杂度、布局复杂性和时间冗余差异。这导致简单/静态/重复片段浪费令牌，而动态/复杂片段令牌不足，整体效率与保真度受限。

EVATok 的核心突破在于引入**路由器预测的内容自适应分配**：为每个视频的各个时间块动态确定令牌数量。路由器是一个轻量级 ViT-S 模型，将输入视频分类为最优令牌分配类别，在训练和推理中为标记器提供分配预测。这一设计的因果机制在于：动态/复杂内容获得更多令牌以保留细节，而重复/简单内容被分配最少令牌以节省预算，从而在更低的平均令牌消耗下实现更好的重建质量与下游生成性能。

**证据强度**：Table 1（row B2 vs A2）显示，在 WebVid 验证集上，路由器引导的最终标记器相比固定均匀分配节省 29.6% 令牌，同时 rFVD 从 63 降至 33。Figure 4 的质量-成本权衡曲线进一步证实，最大代理奖励策略在所有预算水平上均优于固定均匀分配，且路由器分配紧跟最优曲线，在未见过的 UCF-101 上依然有效。

### 2. 基于代理奖励最大化的最优分配确定（Proxy Reward Maximization）

如何为每个视频确定“最优”令牌分配是自适应标记化的核心难题。先前方法（如 AdapTok 的 mini-batch ILP，ElasticTok 的阈值搜索）依赖启发式规则，可能与全局最优及样本最优偏离。

EVATok 提出**代理奖励（Proxy Reward）** 作为统一的质量-成本度量：

$$R_{\mathrm{proxy}} = w_q Q(\mathcal{E}_{\mathrm{proxy}}, x, a) - w_l L(a)$$

其中 $Q$ 为归一化重建质量（基于 LPIPS），$L(a)$ 为归一化令牌长度，$w_q/w_l$ 为偏好权重。最优分配通过在所有候选分配中最大化代理奖励选择：

$$a^* = \operatorname{argmax}_{a \in A} R_{\mathrm{proxy}}$$

这一设计的因果优势在于：代理奖励将离散的分配搜索转化为可比较的标量优化问题，且通过代理标记器（Stage 1 训练）直接评估每个分配的实际重建效果，避免了启发式方法的偏差。

**证据强度**：Figure 5 显示，最大代理奖励策略在质量-成本曲线上显著优于阈值搜索方法。Table 8 进一步揭示，虽然路由器 Top-1 准确率不高，但其代理奖励百分位数（Proxy Reward Percentile）很高，表明预测偏差对最终性能影响有限。

### 3. 消除训练-推理差距的最终标记器重训练（Final Tokenizer Retraining）

先前自适应标记化方法（如尾令牌丢弃）存在训练-推理角色不一致问题：训练时学习所有可能的分配，推理时仅使用部分分配，导致性能下降。

EVATok 通过**两阶段标记器训练**解决此问题：Stage 1 训练代理标记器（Proxy Tokenizer），能够根据任意随机采样的分配重建视频，用于评估分配质量和计算代理奖励；Stage 4 则使用路由器预测的分配**从头重新训练一个最终标记器**（Final Tokenizer），使其在训练和推理时使用完全一致的分配，消除训练-推理差距。

这一设计的关键在于：代理标记器承担“探索”角色（学习所有分配），最终标记器承担“利用”角色（仅学习路由器分配），两者分工明确。

**证据强度**：Table 1（row A2 vs A1, B2 vs B1）显示，在相同训练迭代下，最终标记器显著优于直接使用路由器分配的代理标记器，验证了消除训练-推理差距的必要性。

### 4. 视频语义增强训练目标（Video Semantic Alignment）

传统 VQGAN 损失主要关注像素级重建，对视频的时序一致性和语义保真度关注不足。EVATok 在标准 VQGAN 损失基础上增加两项视频语义增强：

- **表示对齐损失**（V-JEPA2）：使用预训练 V-JEPA2-L 特征对解码器中间层特征进行块级表示对齐：

$$\mathcal{L}_{\mathrm{align}} = -\frac{1}{N}\sum_{n=1}^{N} \sin \bigl( f_n^{\mathrm{dec},l}, \phi(f_n^{\mathrm{sem}}) \bigr)$$

- **VideoMAE 语义鉴别器**：在最终标记器训练中可选使用，以冻结的 VideoMAE-B 提供多层级感知反馈，改善视觉质量。

**证据强度**：Table 5 消融实验显示，移除 VideoMAE 语义鉴别器后，rFVD 从 13 恶化至 65，gFVD 从 98 恶化至 155；移除 V-JEPA2 表示对齐后，rFVD 升至 18，gFVD 升至 144；同时移除两者导致 rFVD 80, gFVD 230。值得注意的是，VideoMAE 鉴别器虽降低 PSNR/LPIPS 数值，但大幅改善了感知模糊和伪影（Figure 8），揭示了传统像素指标与感知质量的权衡。

### 创新点总结

EVATok 的四项核心创新形成一个完整的因果链条：**代理奖励**定义了“什么是最优分配”，**路由器**高效预测最优分配，**最终标记器重训练**消除训练-推理差距，**视频语义增强**提升重建的感知质量。这一组合使 EVATok 在 WebVid 上以 29.6% 令牌节省实现 rFVD 33（vs 均匀分配的 63），在 UCF-101 上以 24.4% 令牌节省达到 rFVD 9.7，并在下游 AR 生成中以更少令牌超越先前 SOTA（LARP: gFVD 57 vs EVATok: gFVD 48, -26.2% 令牌）。

## 整体框架

EVATok 采用四阶段训练框架，核心思路是**用代理奖励（proxy reward）量化每个视频在各候选令牌分配下的质量-成本权衡，并训练一个轻量路由器来预测最优分配，最终用该路由器引导的分配从头训练一个自适应长度标记器**。图 2 给出了四个阶段的整体流程。

### 阶段一：代理标记器训练

首先训练一个**代理标记器（proxy tokenizer）**，使其能够对任意随机采样的令牌分配 $a$ 完成视频重建。该标记器采用 Q-Former 风格的 1D 架构（图 3），输入视频经时空分块（3D patch embedding）后，根据给定的分配 $a$ 从对应时间块通过 2D 池化初始化可变数量的 1D 查询嵌入，再经因果注意力 Q-Former 编码器进行矢量量化，最后由 Q-Former 解码器重建视频帧。训练损失在标准 VQGAN 损失基础上，额外引入 V-JEPA2 语义表示对齐损失和码本利用熵损失：

$$ \mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{vqgan}} + \lambda \mathcal{L}_{\mathrm{align}} + \gamma \mathcal{L}_{\mathrm{entropy}} \tag{2} $$

其中 $\lambda=0.7$，$\gamma=0.02$。表示对齐损失通过最小化解码器中间层特征与 V-JEPA2 语义特征之间的负余弦相似度，提升重建的语义一致性（Eq. 1）。

### 阶段二：最优分配数据集策展

利用训练好的代理标记器，对数据集中每个视频在所有候选分配 $a \in A$ 上计算**代理奖励**：

$$ R_{\mathrm{proxy}} = w_q Q(\mathcal{E}_{\mathrm{proxy}}, x, a) - w_l L(a) \tag{3} $$

其中 $Q$ 为归一化重建质量（如 LPIPS），$L(a)$ 为归一化令牌长度，$w_q$ 和 $w_l$ 为偏好权重。对每个视频选择代理奖励最大的分配作为其最优分配：

$$ a^* = \operatorname{argmax}_{a \in A} R_{\mathrm{proxy}} \tag{4} $$

由此构建 (视频, 最优分配) 的分类数据集，用于后续路由器训练。实验中使用 WebVid-10M 的 100k 视频片段，每个片段为 16×128×128，候选分配空间为 $5^4=625$（4 个时间块，每块 5 种令牌数选择）。

### 阶段三：路由器训练

在策展数据集上训练一个轻量级 ViT-S 路由器，将输入视频分类为对应的最优令牌分配类别。路由器在训练和推理时均为标记器提供分配预测，避免了每次暴力搜索 $O(m^T)$ 的计算开销。

### 阶段四：最终标记器训练

**从头训练最终自适应标记器**，训练过程中由路由器为每个输入视频预测令牌分配，标记器直接根据该分配初始化 1D 查询数量。这与阶段一代理标记器（训练时学习所有可能分配，推理时仅用部分分配）形成关键区别——最终标记器的训练和推理使用完全一致的分配机制，**消除了训练-推理差距**。此阶段还可选引入 VideoMAE 语义鉴别器，以冻结的 VideoMAE-B 提供多层级感知反馈，进一步改善视觉质量（尽管会略微降低 PSNR/LPIPS 等像素指标）。

### 关键设计决策

**可变长度实现机制**：与先前方法（如 ElasticTok、AdapTok）采用的“尾令牌丢弃”策略不同，EVATok 在 1D 查询初始化阶段即根据分配确定查询数量，查询长度固定且角色明确，避免了丢弃带来的训练/推理角色不一致及额外计算开销。

**训练-推理一致性**：表 1 的直接对比（A2 vs A1, B2 vs B1）表明，在相同训练迭代下，最终标记器显著优于直接使用路由器分配推理的代理标记器，验证了消除训练-推理差距的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l868_https_arxiv_org_abs_2603_12267/figures/002_Figure_2.jpg]]
*Figure 2: Four-stage framework for adaptive video tokenizer training. Stage 1 trains a proxy tokenizer to reconstruct videos under all candidate assignments. Stage 2 applies the proxy tokenizer to compute proxy rewards for all candidate assignments across videos (Videos, Optimal Assignments)from a dataset. It identifies the assignments with maximum proxy rewards to curate a classification dataset of videos and their optimal Max-proxy-reward Block4assignments. Stage 3 trains a router on the curated dataset to predict the optimal assignments for videos. Stage 4 trains the final tokenizer Block1from scratch, with the router determining the assignment for each input video during training*

## 核心模块与公式推导

EVATok 的核心架构围绕**内容自适应的可变长度视频标记化**展开，由四个关键模块协同工作：1D可变长度标记器、代理奖励机制、轻量级路由器以及训练-推理差距消除策略。以下逐一剖析其设计逻辑与关键公式。

---

### 1D 可变长度视频标记器

传统视频标记器对所有时间块分配固定数量的令牌，忽略内容复杂度的差异。EVATok 的标记器采用 **Q-Former 风格的 1D 架构**，其核心创新在于：**1D 查询的数量在初始化阶段即根据给定的令牌分配方案确定，而非事后丢弃尾部令牌**。

具体流程如下（参见 Figure 3）：
1. **3D Patch Embedding**：输入视频经时空下采样和分块后，生成 3D 特征嵌入。
2. **1D Query Initialization**：根据分配方案 $a = (k_1, k_2, \dots, k_T)$（$T$ 为时间块数，$k_t$ 为第 $t$ 块的令牌数），从对应时间块的 3D 特征通过 2D 池化生成相应数量的 1D 查询嵌入。总令牌长度 $L(a) = \sum_{t=1}^{T} k_t$。
3. **Q-Former Encoder**：通过自注意力和交叉注意力（带有时序因果掩码，确保时间因果性）编码 1D 查询，随后矢量量化为离散令牌。
4. **Q-Former Decoder**：从离散令牌通过因果解码重建 3D 特征，最终线性投影并重塑为视频帧。

![[assets/figures/papers/paper_list_l868_https_arxiv_org_abs_2603_12267/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of 1D variable-length video tokenizer for EVATok. The input video is spatio-temporally patchified into 3D embeddings. According to a given assignment a, 1D variablelength query embeddings are initialized from these 3D embeddings. After Q-Former encoding and quantization, 1D discrete tokens are produced. Finally, 3D queries are initialized to reconstruct the video frames from the 1D tokens*

这种“初始化即确定长度”的设计，使得每个 1D 令牌的角色在训练和推理中保持一致，避免了丢弃策略带来的训练-推理角色不一致问题。

---

### 视频语义对齐损失

为提升重建的语义一致性，标记器在训练中引入了与预训练语义编码器的表示对齐损失。具体使用 **V-JEPA2-L** 作为冻结的语义编码器，对解码器中间层特征进行块级对齐：

$$
\mathcal{L}_{\mathrm{align}} = -\frac{1}{N}\sum_{n=1}^{N} \sin \bigl( f_n^{\mathrm{dec},l}, \phi(f_n^{\mathrm{sem}}) \bigr) \tag{1}
$$

其中：
- $f_n^{\mathrm{dec},l}$ 为解码器第 $l$ 层的第 $n$ 个块特征；
- $f_n^{\mathrm{sem}}$ 为 V-JEPA2 编码器对应位置的语义特征；
- $\phi(\cdot)$ 为可学习的线性投影层，用于对齐维度；
- $\sin(\cdot,\cdot)$ 实际为余弦相似度（原文记为 sin，实为余弦相似度损失）。

标记器的完整训练损失为：

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{vqgan}} + \lambda \mathcal{L}_{\mathrm{align}} + \gamma \mathcal{L}_{\mathrm{entropy}} \tag{2}
$$

其中 $\mathcal{L}_{\mathrm{vqgan}}$ 为标准 VQGAN 损失（重建 + 感知 + 对抗 + 码本损失），$\lambda = 0.7$ 为对齐损失权重，$\gamma = 0.02$ 为码本利用熵损失权重，后者用于防止码本坍塌。

---

### 代理奖励与最优分配搜索

如何为每个视频找到“最优”令牌分配？EVATok 的核心洞察是：**用代理标记器评估分配的质量-成本权衡，并通过最大化代理奖励来定义最优分配**。

**代理奖励**的定义为：

$$
R_{\mathrm{proxy}} = w_q \cdot Q(\mathcal{E}_{\mathrm{proxy}}, x, a) - w_l \cdot L(a) \tag{3}
$$

其中：
- $\mathcal{E}_{\mathrm{proxy}}$ 为阶段 1 训练的代理标记器；
- $x$ 为输入视频；
- $a$ 为候选分配方案；
- $Q(\cdot)$ 为归一化的重建质量度量（如 LPIPS，经 min-max 归一化至 $[0,1]$）；
- $L(a)$ 为归一化的令牌总长度；
- $w_q$ 和 $w_l$ 为偏好权重，控制质量与成本的权衡。

**最优分配**则通过在所有候选分配中最大化代理奖励获得：

$$
a^* = \operatorname{argmax}_{a \in \mathcal{A}} R_{\mathrm{proxy}} \tag{4}
$$

其中 $\mathcal{A}$ 为所有候选分配的集合。在默认设置中，每个时间块的令牌数从 5 个离散选项中选择（如 $T=4$ 时，$|\mathcal{A}| = 5^4 = 625$）。

这种基于代理奖励的搜索策略，在质量-成本权衡曲线上显著优于启发式阈值搜索方法（Figure 5），因为后者仅基于 LPIPS 阈值丢弃尾部令牌，无法全局优化分配。

---

### 轻量级路由器

暴力搜索最优分配的计算复杂度为 $O(m^T)$（$m$ 为每块候选数，$T$ 为时间块数），在推理时不可行。EVATok 通过训练一个**轻量级路由器**来解决此问题。

路由器采用 **ViT-S** 架构，将输入视频分类为最优令牌分配类别。训练数据来自阶段 2 策展的 (视频, 最优分配) 对：在 WebVid-10M 的 100k 视频子集上，用代理标记器计算所有候选分配的代理奖励，选取奖励最大的分配作为标签。

路由器的预测质量通过**代理奖励百分位数**（Proxy Reward Percentile）衡量，而非简单的 top-1 准确率：

$$
\mathcal{P} = \frac{\mathbb{E}_x(R_{\mathrm{proxy}}(a_{\mathrm{eval}},x)) - \mathbb{E}_x(R_{\mathrm{proxy}}(a_{\mathrm{worst}},x))}{\mathbb{E}_x(R_{\mathrm{proxy}}(a_{\mathrm{best}},x)) - \mathbb{E}_x(R_{\mathrm{proxy}}(a_{\mathrm{worst}},x))} \times 100\% \tag{8}
$$

该指标评估路由器预测的分配在最优与最差代理奖励区间中的相对位置。实验表明，虽然路由器的 top-1 准确率较低，但百分位数较高，说明预测偏差对最终性能影响有限（Table 8）。

---

### 训练-推理差距消除

代理标记器在阶段 1 训练时学习了所有候选分配下的重建能力，但在推理时仅使用路由器预测的单一分配，存在性能差距。EVATok 通过**阶段 4 重新训练最终标记器**来消除这一差距：在训练和推理中均使用路由器预测的分配，使标记器始终在一致的分配下工作。

实验验证了这一设计的必要性：在相同训练迭代数下，最终标记器显著优于直接使用路由器分配的代理标记器（Table 1，行 A2 vs A1，B2 vs B1）。

此外，最终标记器的训练可选择性地引入 **VideoMAE 语义鉴别器**，以冻结的 VideoMAE-B 提供多层级感知反馈。虽然这会降低 PSNR/LPIPS 等像素级指标，但显著减轻了模糊和伪影，提升了感知质量（Figure 8）。

## 实验与分析

### 核心结果：重建与生成效率的全面提升

EVATok 的核心主张——内容自适应的可变长度令牌化能够在显著节省令牌的同时提升重建与生成质量——在多个基准和任务上得到了系统验证。

**WebVid 验证集上的重建性能**（Table 1）：在 400k 迭代的公平训练条件下，路由器引导的最终标记器（Router Final Tok.）相比固定均匀分配基线（Uniform Final Tok.），将平均重建令牌数从 1024 降至 721，节省 **29.6%** 的令牌，同时 rFVD 从 63 大幅降至 **33**（-47.6%），LPIPS 保持可比（0.1068 vs. 0.1032）。这一结果表明，自适应分配不仅没有牺牲重建质量，反而通过将有限令牌预算集中于复杂片段，实现了更优的时序一致性。

**UCF-101 上的跨域泛化**（Table 2）：路由器仅在 WebVid 子集上训练，在未见过（unseen）的 UCF-101 上，其引导的最终标记器仍以 **24.4%** 的令牌节省（重建）和 **27.7%** 的令牌节省（生成）超越固定均匀分配基线。重建 rFVD 持平（13 vs. 13），下游 AR 生成的 gFVD 从 98 降至 **96**，证明自适应分配策略具有良好的泛化性，且节省的令牌直接转化为下游生成任务的效率提升。

**系统级 SOTA 比较**（Table 3, Table 4）：在与先前最优方法 **LARP**（固定 1024 令牌）的直接对比中，EVATok 以更少的令牌取得全面优势：
- UCF-101 重建：774 令牌（-24.4%）下 rFVD 达 **9.7**，优于 LARP-L-Long 的 20（173M 参数）；
- UCF-101 class-to-video 生成：756 令牌（-26.2%）下 gFVD 达 **48**，优于 LARP 的 57（632M AR 模型）；
- K600 帧预测：862 令牌（-15.8%）下 gFVD 达 **4.0**，优于 LARP 的 5.1。

这些结果构成了 EVATok 效率优势的强证据链：令牌节省幅度在 15.8% 至 29.6% 之间，而质量指标（rFVD, gFVD）均持平或显著改善，排除了“以质量换效率”的简单妥协解释。

### 质量-成本权衡曲线的决定性证据

Figure 4 展示了不同分配策略在 WebVid 和 UCF-101 上的质量-成本权衡曲线，这是验证自适应分配核心逻辑的关键证据：

![[assets/figures/papers/paper_list_l868_https_arxiv_org_abs_2603_12267/figures/004_Figure_4.jpg]]
*Figure 4: Quality-cost trade-off curves for different assignment strategies. By adaptively assigning token budgets to different temporal blocks across various videos, our max-proxy-reward strategy (green series) achieves superior performance under various overall budgets compared to the typical fixed uniform token assignment approach (red series). The router-based assignment (blue series) delivers performance close to that of the max-proxy-reward strategy on both WebVid and UCF datasets (the latter unseen during router training)*

- **最大代理奖励策略**（max-proxy-reward，绿色曲线）在所有预算水平上均显著优于固定均匀分配（红色曲线），证明通过代理奖励优化令牌分配能够系统性地提升质量-成本 Pareto 前沿；
- **路由器分配**（蓝色曲线）紧密跟随最大代理奖励曲线，在未见过的 UCF-101 上同样保持接近最优的性能，验证了路由器能够有效学习代理奖励所定义的最优分配模式；
- 在 WebVid 上，路由器分配在相同 rFVD 下可节省高达 **56%** 的令牌；在 UCF-101 上，节省幅度达 **42%**，表明视频数据中的时间冗余为自适应分配提供了巨大的效率空间。

Figure 5 进一步将最大代理奖励策略与启发式**阈值搜索方法**（threshold-based assignment）进行对比：阈值搜索虽优于均匀分配，但其质量-成本曲线始终低于最大代理奖励策略。这证明了基于代理奖励的全局优化相比基于局部 LPIPS 阈值的启发式丢弃具有本质优势——后者的贪婪决策无法考虑令牌分配的时间块间依赖关系。

![[assets/figures/papers/paper_list_l868_https_arxiv_org_abs_2603_12267/figures/009_Figure_5.jpg]]
*Figure 5: Quality-cost curve: threshold based vs. max-proxyreward vs. uniform assignment. While threshold-based assignment improves rFVD against uniform assignment, it underperforms our max-proxy-reward strategy*

### 消融研究：关键设计组件的作用

Table 5 的消融实验揭示了两个关键训练增强的必要性：

![[assets/figures/papers/paper_list_l868_https_arxiv_org_abs_2603_12267/figures/010_Table_5.jpg]]
*Table 5: Ablation study for video representation alignment and video semantic discriminator. Removing either design will lead to degradation in rFVD and downstream gFVD*

| 配置 | rFVD ↓ | gFVD ↓ |
|------|--------|--------|
| 完整 EVATok（路由器引导） | 13 | 96 |
| 移除 VideoMAE 语义鉴别器 | 65 | 155 |
| 移除 V-JEPA2 表示对齐 | 18 | 144 |
| 同时移除两者 | 80 | 230 |

移除 VideoMAE 语义鉴别器导致 rFVD 从 13 恶化至 65（+400%），gFVD 从 96 升至 155（+61%）；移除 V-JEPA2 表示对齐导致 rFVD 升至 18（+38%），gFVD 升至 144（+50%）。两者同时移除时性能崩溃（rFVD 80, gFVD 230），表明表示对齐和语义鉴别器对自适应令牌化场景下的重建与生成质量具有互补且关键的作用。

值得注意的是，VideoMAE 鉴别器虽然大幅改善 rFVD 和 gFVD，但会**降低 PSNR/LPIPS 等像素级指标**（Figure 8 定性对比）。论文明确指出这是一种权衡：鉴别器减轻了模糊和伪影，提升了感知质量，但像素空间指标的退化可能对某些强调 PSNR 的应用场景不利。这是该设计的一个已知局限性。

### 训练-推理差距的消除

Table 1 的行间对比（A2 vs. A1, B2 vs. B1）验证了四阶段框架中 Stage 4（最终标记器）的必要性：在相同训练迭代（400k）下，使用路由器分配的最终标记器始终优于直接使用路由器分配的代理标记器（Stage 1）。例如，Router Final Tok. 的 rFVD 为 33，而 Router Proxy Tok. 为 36。这一差距源于代理标记器在训练时学习了所有候选分配，但推理时仅使用路由器预测的特定分配，导致训练-推理分布不匹配。Stage 4 通过使用路由器分配从头训练最终标记器，使训练和推理的分配完全一致，消除了这一差距。

![[assets/figures/papers/paper_list_l868_https_arxiv_org_abs_2603_12267/figures/005_Table_1.jpg]]
*Table 1: Final tokenizer validation on WebVid. The tokenizers are trained for 400k iterations. With the router, final tokenizers achieve comparable LPIPS and better rFVD with 29.6% saving in token length (row A2 vs. B2 and row A2+ vs. B2+). Final tokenizers outperform proxy tokenizers with the same training efforts (row A2 vs. A1, B2 vs. row B1), showing the importance of bridging the training-inference gap for variable-length tokenizers*

### 路由器准确率与代理奖励百分位数

Table 8 揭示了一个重要的实践洞察：路由器的 top-1 分配准确率并不高（预测的分配通常不精确命中代理奖励最高的分配），但其**代理奖励百分位数**（proxy reward percentile）表现良好，且在 UCF-101 上泛化有效。这意味着路由器的预测偏差通常落在代理奖励的高分位区间，对最终性能影响有限。这一发现降低了路由器精确分类的要求，使得轻量级 ViT-S 路由器足以胜任分配预测任务。

![[assets/figures/papers/paper_list_l868_https_arxiv_org_abs_2603_12267/figures/019_Table_8.jpg]]
*Table 8: Accuracy vs. proxy reward percentile for the router assignment. In terms of accuracy. the assignments predicted by the router do not usually hit the top1 or top5 highest proxy reward assignments. However, in terms of proxy reward percentile, the router assignments achieve good results, and generalize to unseen dataset (UCF-101) well*

### 图像自适应令牌化的有限收益

Table 9 和 Figure 12 显示，在 ImageNet 256×256 图像重建上，自适应令牌化节省 19.9% 令牌但 rFID 略有恶化。然而，下游 AR 生成的 FID 仍受益。这表明**视频特有的时间冗余**是自适应分配的主要受益来源——不同时间块之间的内容复杂度差异远大于图像内部的空间差异，因此按时间块分配令牌的收益远高于按空间区域分配。

![[assets/figures/papers/paper_list_l868_https_arxiv_org_abs_2603_12267/figures/020_Figure_12.jpg]]
*Figure 12: Image tokenization quality-cost trade-off curve. On ImageNet 256 × 256 reconstruction, the improvements of maxproxy-reward assignment can be marginal compared to uniform assignment*

![[assets/figures/papers/paper_list_l868_https_arxiv_org_abs_2603_12267/figures/021_Table_9.jpg]]
*Table 9: Image final tokenizer validation. For ImageNet*

### 失败模式与待验证边界

1. **暴力搜索的计算瓶颈**：当前 Stage 2 的最优分配搜索复杂度为 $O(m^T)$（$T$ 为时间块数，$m$ 为每块候选令牌数），在 $T=4, m=5$ 时（625 种组合）尚可接受，但扩展到更多时间块或更细粒度候选集时计算成本急剧上升。论文提出自回归近似搜索作为未来方向，但尚未实现。

2. **中小规模数据集的验证局限**：实验主要在 UCF-101、K600 和 WebVid 10M 子集上进行，尚未验证该方法在更大规模、高分辨率或长时程视频上的有效性。

3. **生成任务的覆盖范围有限**：下游生成仅覆盖 class-to-video 和帧预测，未涉及复杂的文本到视频生成，也未验证文本条件对自适应分配的影响。

4. **VideoMAE 鉴别器的指标退化**：虽提升感知质量，但 PSNR/LPIPS 的退化可能限制其在像素精度敏感场景的应用。

5. **偏好权重的静态设定**：代理奖励中的 $w_q/w_l$ 需人工设定，缺乏根据输入内容或用户偏好动态调整的机制。

### 补充图表

![[assets/figures/papers/paper_list_l868_https_arxiv_org_abs_2603_12267/figures/006_Table_2.jpg]]
*Table 2: Final tokenizer validation on UCF. The final tokenizer with router beats the fixed uniform assignment baseline in both reconstruction and downstream AR generation, while saving 24.4% and 27.7% token length separately*

![[assets/figures/papers/paper_list_l868_https_arxiv_org_abs_2603_12267/figures/007_Table_3.jpg]]
*Table 3: System-level comparison for tokenizers and downstream generation models. EVATok achieves superior performances in UCF-101 video reconstruction, downstream class-to-video generation and K600 frame prediction, while saving 24.4% tokens in reconstruction and 26.2% tokens in UCF class-to-video generation*

![[assets/figures/papers/paper_list_l868_https_arxiv_org_abs_2603_12267/figures/008_Table_4.jpg]]
*Table 4: K600 frame prediction comparison. In similar settings, EVATok performs the best with 15.8% less generated tokens*

## 方法谱系与知识库定位

### 问题定位：从固定长度到内容自适应的视频标记化

视频自回归生成的主流范式依赖离散标记器将视频压缩为1D令牌序列，再交由GPT类模型进行生成。在此框架下，**标记器的压缩效率直接决定了下游生成模型的计算开销与生成长度**。传统方法对所有视频片段分配固定数量的令牌，其核心假设是每个时空块的信息量均等。然而，真实视频在时间维度上存在显著的冗余差异：静态背景、重复动作或简单布局的片段仅需极少令牌即可重建，而剧烈运动、复杂纹理或场景切换的片段则需要更多令牌来保留细节。

这一“均匀分配”范式构成了当前视频标记化的隐性瓶颈——简单片段浪费令牌，复杂片段令牌不足，整体效率与保真度双双受限。**EVATok** 正是针对这一瓶颈，将核心问题重新表述为：**如何为每个视频的时间块自适应地分配令牌数量，使得在给定总令牌预算下最大化重建质量与下游生成性能**。

### 方法谱系：固定分配、启发式自适应与代理奖励最优化的演进

#### 固定长度基线

最直接的基线是 **Fixed Uniform Assignment**，即所有时间块分配相同数量的令牌。该方法在 **LARP**（先前最优的固定长度视频标记化系统，AR生成）等工作中被采用，通常以1024个令牌编码16帧视频。其优势在于实现简单、训练稳定，但完全忽视了内容差异性，成为EVATok的主要对比对象。

#### 启发式自适应方法的尝试

在EVATok之前，已有工作探索自适应令牌分配：

- **AdapTok**：采用mini-batch整数线性规划（ILP）确定每个视频的令牌分配，试图在批次内实现质量-成本的平衡。然而，mini-batch ILP的优化目标是批次平均性能，而非每个视频的个体最优，可能偏离全局最优分配。
- **ElasticTok**：采用基于阈值的搜索方法，通过设定LPIPS阈值丢弃尾部令牌。类似的 **Threshold-based assignment** 在EVATok的消融研究中被作为启发式基线：根据LPIPS值判断哪些尾部令牌对重建贡献较小并予以丢弃。

这些启发式方法虽然比均匀分配有所改进，但存在两个根本性局限：（1）分配策略基于局部启发式准则（如单帧LPIPS），缺乏对全局质量-成本权衡的系统建模；（2）通常采用“尾令牌丢弃”机制，导致训练时标记器学习所有可能的令牌位置，而推理时仅使用部分令牌，造成训练-推理角色不一致，引入额外性能差距。

#### EVATok的核心推进：代理奖励最大化与路由器预测

EVATok的方法论突破体现在三个层面：

**（1）代理奖励作为全局优化目标。** 不同于启发式准则，EVATok定义了代理奖励 $R_{\mathrm{proxy}} = w_q Q(\mathcal{E}_{\mathrm{proxy}}, x, a) - w_l L(a)$，其中 $Q$ 为归一化重建质量（基于LPIPS），$L$ 为归一化令牌长度，$w_q$ 和 $w_l$ 为偏好权重。这一标量奖励函数将质量-成本权衡显式建模为可优化的目标，使得最优分配的选择成为可求解的最大化问题：$a^* = \operatorname{argmax}_{a \in A} R_{\mathrm{proxy}}$。

**（2）路由器预测替代暴力搜索。** 直接暴力搜索最优分配的复杂度为 $O(m^T)$（$m$ 为每块候选令牌数，$T$ 为时间块数），在推理时不可行。EVATok通过训练一个轻量级ViT-S路由器，将分配选择转化为分类任务，在推理时直接预测最优分配，避免了每次推理的搜索开销。

**（3）消除训练-推理差距。** 与尾令牌丢弃方法不同，EVATok在初始化1D查询时即根据分配确定查询数量，查询长度固定且角色明确。更重要的是，EVATok用路由器预测的分配重新训练最终标记器（Stage 4），使训练和推理使用完全一致的分配策略，从根本上消除了代理标记器（Stage 1）因训练时学习所有可能分配而推理时仅用部分分配所导致的性能差距。

### 适用边界与局限

**技术边界：**

- **时间冗余是主要受益来源。** 实验表明，在图像标记化（ImageNet 256×256）上，自适应分配的提升有限甚至小幅恶化（Figure 12），说明EVATok的核心优势源于视频特有的时间冗余。对于缺乏显著时间差异的视频（如固定机位拍摄的静态场景），自适应分配的收益可能减弱。
- **计算成本与搜索复杂度。** 当前暴力搜索最优分配的复杂度为 $O(m^T)$，在Stage 2的策展阶段需对所有候选分配进行代理奖励评估。对于更多时间块（$T$ 增大）或更细粒度的候选集（$m$ 增大），计算成本急剧上升。论文提出未来可探索自回归近似搜索以降至 $O(T^2)$，但该方案尚未验证。
- **偏好权重的静态设定。** 代理奖励中的 $w_q$ 和 $w_l$ 需人工设定，缺乏根据输入视频或用户偏好动态调整的机制。不同应用场景对质量-成本的权衡需求可能不同，静态权重限制了灵活性。

**实验覆盖边界：**

- **数据集规模有限。** 实验主要在中小规模数据集上进行：WebVid-10M子集（100k视频用于策展）、UCF-101、K600。尚未验证该方法在更大规模、高分辨率或长时程视频（如分钟级视频）上的有效性。
- **生成任务类型受限。** 下游生成目前仅覆盖类到视频生成（class-to-video）和帧预测（frame prediction），未涉及复杂的文本到视频生成（text-to-video），也未验证条件控制信号对自适应分配的影响。
- **代理标记器质量的依赖性。** 路由器的训练数据来自代理奖励标记器的输出，代理标记器自身的质量可能影响“最优分配”的真实性。若代理标记器在某些分配下重建质量评估不准确，则策展的标签可能存在偏差。

**指标层面的权衡：**

- VideoMAE语义鉴别器虽然显著改善感知质量（减少模糊和伪影），但会降低PSNR/LPIPS等像素级指标。对于强调PSNR的应用场景（如医学影像、工业检测），这一权衡可能不利。

### 开放问题

1. **跨模态与跨架构泛化。** 自适应长度令牌化方案能否扩展到连续VAE令牌和扩散模型中？当前设计深度绑定离散VQGAN框架，其核心思想（代理奖励引导的分配优化）是否适用于其他生成范式尚待验证。

2. **大规模文本-视频条件下的表现。** 在更大规模的文本-视频数据上，内容自适应令牌化能否保持或扩大优势？文本条件可能改变视频片段的信息重要性分布，路由器是否需要条件感知的扩展？

3. **动态偏好调整机制。** 如何实现 $w_q/w_l$ 的实时动态调整，使用户或下游任务能够根据需求灵活控制质量-成本平衡？这可能需要将偏好权重作为路由器或标记器的条件输入。

4. **高效最优分配搜索。** 自回归近似最优分配搜索能否在不损失性能的前提下大幅降低Stage 2的策展成本？这对于将EVATok扩展到更长视频（更多时间块）至关重要。

5. **高帧率与高分辨率场景。** 当时间块数量大幅增加（如高帧率视频）或空间分辨率显著提升时，现有路由器架构（ViT-S）是否依然高效？可能需要层次化或级联的路由器设计。

6. **语义编码器的正交性。** 不同预训练语义编码器（V-JEPA2、VideoMAE等）的搭配对最终性能的影响是否正交？当前消融仅验证了各组件的必要性，但未探索不同语义特征的最优组合策略。

## 原文 PDF

![[paperPDFs/CVPR_2026/EVATok_Adaptive_Length_Video_Tokenization_for_Efficient_Visual_Autoregressive_Generation.pdf]]