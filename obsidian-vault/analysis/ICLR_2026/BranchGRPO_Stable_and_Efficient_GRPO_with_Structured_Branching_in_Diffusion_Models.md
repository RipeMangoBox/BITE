---
title: "BranchGRPO: Stable and Efficient GRPO with Structured Branching in Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/BranchGRPO_Stable_and_Efficient_GRPO_with_Structured_Branching_in_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- BranchGRPO
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "BranchGRPO把扩散GRPO的独立顺序rollout改造成共享前缀的树状分支rollout。"
primary_logic: "树叶终端奖励经路径概率融合回传到内部节点，再按深度归一化生成逐步骤优势用于裁剪GRPO更新。"
claims:
- "树状rollout在保持探索多样性的同时显著摊销去噪前缀计算。"
- "奖励融合和深度归一化缓解了扩散RL中终端奖励稀疏导致的信用分配问题。"
- "深度剪枝和混合ODE-SDE调度在HPSv2.1等指标上提升质量并减少训练时间。"
---

# BranchGRPO: Stable and Efficient GRPO with Structured Branching in Diffusion Models

> [!tip] 核心洞察
> 通过树状rollout结构，在保持探索多样性的同时，利用共享前缀摊销计算成本；通过路径概率融合和深度归一化，将稀疏的终端奖励转化为密集的逐步骤优势信号，实现更稳定、更高效的策略优化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | BranchGRPO：基于结构化分支的稳定高效扩散模型GRPO方法 |
| 英文题名 | BranchGRPO: Stable and Efficient GRPO with Structured Branching in Diffusion Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=T2nP2IQasd) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | BranchGRPO |
| Dataset | HPSv2.1 (FLUX.1-Dev) |

> [!tip] 效果简介
> - HPSv2.1 (FLUX.1-Dev) 上，HPS-v2.1 为 0.369，对比 0.360，变化 +0.009。
> - HPSv2.1 (FLUX.1-Dev) 上，PickScore 为 0.231，对比 0.227，变化 +0.004。
> - HPSv2.1 (FLUX.1-Dev) 上，ImageReward 为 1.625，对比 1.573，变化 +0.052。

## 概要

BranchGRPO是一种针对扩散模型GRPO（Group Relative Policy Optimization）训练的结构化改进方法。该方法通过将传统的顺序rollout重构为树状结构，在去噪过程中引入分支，共享前缀以摊销计算，并通过奖励融合与深度归一化将稀疏终端奖励转化为密集的逐步骤优势信号。实验表明，BranchGRPO在HPSv2.1图像对齐上比DanceGRPO提升高达16%的对齐分数，同时将每轮训练时间减少近55%；其混合变体BranchGRPO-Mix进一步将训练加速至DanceGRPO的4.7倍，且不降低对齐性能。

现有GRPO变体在扩散模型上存在两个根本瓶颈：

- **效率低下**：标准GRPO采用顺序rollout设计，每个轨迹需独立采样，复杂度为O(N·T)，导致大量计算冗余。如论文所述："Standard GRPO adopts a sequential rollout design, where each trajectory must be independently sampled under both the old and new policies. This incurs O(N · T ) complexity with denoising steps T and group size N, leading to significant computational redundancy"（Section 1 INTRODUCTION）。

- **奖励稀疏**：现有方法将单一终端奖励均匀分配给所有去噪步骤，忽略了中间状态的信息，导致不可靠的信用分配和高方差梯度。论文指出："Existing methods assign a single terminal reward uniformly across all denoising steps, neglecting informative signals from intermediate states. This uniform propagation leads to unreliable credit assignment and high-variance gradients"（Section 1 INTRODUCTION）。

## 核心方法与创新机理

BranchGRPO的核心创新体现在三个关键设计上：

1. **树状rollout结构**：将顺序rollout重构为树状结构，在指定分裂步将当前状态扩展为K个相关子节点，共享前缀以摊销计算成本，同时保持探索多样性。如论文所述："BranchGRPO replaces inefficient independent sequential rollouts with a branching structure, where scheduled split steps in the denoising process allow each trajectory to stochastically expand into multiple sub-trajectories while reusing shared prefixes"（Section 1 INTRODUCTION）。

2. **奖励融合与深度归一化**：通过路径概率软加权聚合叶子奖励到内部节点，并在每个深度内标准化聚合奖励，产生平衡的逐步骤优势信号。论文指出："BranchGRPO aggregates leaf rewards and propagates them backward with depth-wise normalization, producing finer-grained step-level advantages"（Section 1 INTRODUCTION）。

3. **剪枝策略**：引入宽度剪枝和深度剪枝，仅对选定的子集进行反向传播，不影响前向rollout和奖励评估。如论文所述："pruning strategies that cut gradient computation but leave forward rollouts and exploration unaffected"（Abstract）。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_T2nP2IQasd_BranchGRPO_St/figures/001_Figure_1.jpg]]

BranchGRPO的整体框架由以下核心模块组成：

1. **树状rollout构建**：在去噪过程中，于指定分裂步将当前状态扩展为K个相关子节点，共享前缀（Algorithm 1）。
2. **奖励融合**：通过路径概率软加权聚合叶子奖励到内部节点（Equation 3）。
3. **深度归一化**：在每个深度内标准化聚合奖励，产生平衡的逐步骤优势（Equation 4）。
4. **剪枝策略**：宽度剪枝（Parent-Top1或Extreme选择）和深度剪枝（滑动窗口跳过选定深度）（Section 3.4）。
5. **混合ODE-SDE调度**：保留所有分支步为SDE，滑动窗口确定额外SDE步，其余替换为ODE（Section 4.4）。

Figure 3展示了分支rollout过程、奖励融合和深度归一化与剪枝的整体流程。

### 5.1 反向SDE动力学

去噪动力学的反向SDE形式，其中ε_t控制随机性：

$$\mathrm { d } z _ { t } \ = \ \Big ( f _ { t } z _ { t } - \frac { 1 + \varepsilon _ { t } ^ { 2 } } { 2 } g _ { t } ^ { 2 } \nabla \log p _ { t } ( z _ { t } ) \Big ) \mathrm { d } t \ + \ \varepsilon _ { t } g _ { t } \mathrm { d } w _ { t }$$

### 5.2 分支采样（分裂步）

在分裂步生成K个相关子节点，使用共享噪声ξ_0和分支特定创新η_b，由相关性参数s控制：

$$z _ { i + 1 } ^ { ( b ) } = \mu _ { \theta } ( z _ { i } , t _ { i } ) \ + \ g _ { t _ { i } } \sqrt { h _ { i } } \xi _ { b } , \qquad \xi _ { b } = \frac { \xi _ { 0 } + s \eta _ { b } } { \sqrt { 1 + s ^ { 2 } } } , \quad b = 1 , \ldots , K$$

### 5.3 内部节点奖励融合

通过基于行为策略对数概率的软加权机制，将叶子奖励聚合到内部节点值，β为集中度参数：

$$\bar { r } ( n ) = \sum _ { \ell \in \mathcal { L } ( n ) } w _ { \ell } ^ { ( n ) } r _ { \ell } , \qquad w _ { \ell } ^ { ( n ) } = \frac { \exp ( \beta s _ { \ell } ) } { \sum _ { j \in \mathcal { L } ( n ) } \exp ( \beta s _ { j } ) } , s _ { \ell } = \log p _ { \mathrm { b e h } } ( \ell \mid n )$$

### 5.4 深度归一化

在每个深度d内标准化聚合奖励，产生平衡的逐步骤优势信号：

$$A _ { d } ( n ) = \frac { \bar { r } ( n ) - \mu _ { d } } { \sigma _ { d } + \epsilon } , \qquad \mu _ { d } = \mathrm { m e a n } _ { n \in \mathcal { N } _ { d } } \bar { r } ( n ) , \sigma _ { d } = \mathrm { s t d } _ { n \in \mathcal { N } _ { d } } \bar { r } ( n )$$

### 5.5 树边上的裁剪GRPO损失

应用于树边的标准裁剪GRPO目标，其中ρ_e是重要性采样比率，A(e)是边优势：

$$J ( \theta ) = \mathbb { E } \left[ \frac { 1 } { | \mathcal { E } | } \sum _ { e \in \mathcal { E } } \operatorname* { m i n } \big ( \rho _ { e } ( \theta ) A ( e ) , \mathrm { c l i p } ( \rho _ { e } ( \theta ) , 1 - \epsilon , 1 + \epsilon ) A ( e ) \big ) \right]$$

## 实验与关键发现

### 6.1 主要结果

Table 1展示了在FLUX.1-Dev骨干上的效率-质量比较：

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_T2nP2IQasd_BranchGRPO_St/figures/015_Table_1.jpg]]
*Table 1: Table 1: Efficiency–quality comparison. The best and second-best results in each column are highlighted in bold and underline, respectively. NFE denotes the number of function evaluations of the denoiser. For branching methods, we report the average per-sample NFE, computed as the total function evaluations in the tree divided by the number of final samples.*

| 方法 | HPS-v2.1 | PickScore | ImageReward | Unified Reward | 每轮训练时间 (秒) |
|------|----------|-----------|-------------|----------------|-------------------|
| DanceGRPO | 0.360 | 0.227 | 1.573 | 3.380 | 698 |
| BranchGRPO-DepthPruning | **0.369** | **0.231** | **1.625** | **3.404** | 314 (-55%) |
| BranchGRPO-Mix | 0.365 | 0.229 | 1.598 | 3.392 | 148 (-78.8%, 4.7×加速) |

Table 2展示了在SD3.5-M骨干上的泛化结果：BranchGRPO将GPU小时从2000减少到1460（-27%），同时提升所有对齐指标（HPS-v2.1: 0.323, PickScore: 23.58, ImageReward: 1.32, GenEval: 0.89）。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_T2nP2IQasd_BranchGRPO_St/figures/016_Table_2.jpg]]
*Table 2: Table 2: Generalization on SD3.5-M and integration into GRPO-style training pipelines. Branch-GRPO consistently improves alignment quality and training efficiency.*

### 6.2 消融研究

Figure 6展示了关键消融结果：

- **分支相关性**：中等分支相关性（s=4.0）取得最佳权衡，达到最高奖励和稳定收敛（Figure 6(a)）。
- **分裂位置**：早期分裂（0,3,6,9）促进更快的奖励增长；后期分裂延迟探索并产生较低奖励（Figure 6(b)）。
- **分裂密度**：更密集的分裂（0,3,6,9）加速早期训练；更稀疏的配置收敛更慢（Figure 6(c)）。
- **奖励融合**：路径加权融合（beta=1）比均匀平均（beta=0）提供更高且更稳定的奖励（Figure 6(d)）。
- **剪枝策略**：深度剪枝在最终奖励上优于宽度剪枝（Figure 6(e), Table 8）。
- **混合ODE-SDE**：混合方案实现最快速度（148s vs 289s for MixGRPO vs 469s for DanceGRPO），同时保持稳定快速的奖励增长（Figure 6(f)）。

### 6.3 缩放定律

Figure 7展示了分支rollout的缩放效应：更大的分支因子（K=2,3,4）和更多的分支步数（3,4,5个分裂点）一致地提高奖励，遵循清晰的缩放定律。

Table 4进一步验证了组大小缩放：在相似GPU小时下，BranchGRPO-Mix组大小81达到奖励0.387，显著优于DanceGRPO的0.360；组大小256达到0.404。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_T2nP2IQasd_BranchGRPO_St/figures/021_Table_4.jpg]]
*Table 4: Table 4: Here we use BranchGRPO-Mix. Under similar GPU-hours, BranchGRPO with group size 81 achieves a reward of 0.387, substantially outperforming Dance-GRPO (0.360).*

### 6.4 分布保真度

Section 3.1验证了分支rollout不损害多样性：在CLIP特征空间中，分支rollout与顺序rollout的分布几乎不可区分（KID=0.00022, MMD²=0.0149）；在Inception特征空间中同样接近（KID=0.0057, MMD²=0.0067）。

### 6.5 视频生成

Figure 8展示了在Wan2.1-1.3B上的视频生成结果：BranchGRPO生成更清晰、更连贯的帧，奖励曲线显示更快的收敛和更高的最终奖励。每轮训练时间从20分钟减少到8分钟（-60%）。

Table 13的vBench评估显示：BranchGRPO在美学质量（0.5190 vs 0.5178）、背景一致性（0.9659 vs 0.9647）、动态度（0.5000 vs 0.4992）和运动平滑度（0.9912 vs 0.9899）上均优于DanceGRPO，同时迭代时间从1352s降至493s。

### 6.6 人类偏好

Table 9(a)的人类偏好评估显示：BranchGRPO在48%的情况下被偏好，而DanceGRPO为33%（Flux基础模型为19%）。

### 6.7 公平性说明

- 所有GRPO相关的超参数在不同方法间保持一致。
- HPS-only训练会降低CLIP Score（提示遵循度），简单的多目标设置（HPS-v2.1 + CLIP Score）可以部分恢复CLIP Score，同时保持较高的HPS（Table 12）。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_T2nP2IQasd_BranchGRPO_St/figures/017_Table_3.jpg]]
*Table 3: Table 3: Prompt-conditioned diversity under different branching schedules (new).*

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_T2nP2IQasd_BranchGRPO_St/figures/024_Table_5.jpg]]
*Table 5: Table 5: Hyperparameter settings used in all experiments.*

## 定位与知识库关联

BranchGRPO建立在以下工作基础上：

- **扩散模型基础**：Ho et al., 2020 (Denoising Diffusion Probabilistic Models)、Lipman et al., 2022 (Flow Matching for Generative Modeling)、Liu et al., 2022 (Flow Straight and Fast)
- **RLHF基础**：Ouyang et al., 2022 (Training language models to follow instructions with human feedback)
- **GRPO基础**：Shao et al., 2024 (Group Relative Policy Optimization)
- **GRPO在视觉生成中的应用**：Liu et al., 2025a (Flow-GRPO)、Xue et al., 2025 (DanceGRPO)
- **树状rollout**：Li et al., 2025b (TreePO in LLMs)
- **混合ODE-SDE**：Li et al., 2025a (MixGRPO)

BranchGRPO的核心贡献在于将树状rollout结构引入扩散模型的GRPO训练，解决了顺序rollout的效率瓶颈和稀疏奖励的信用分配问题。该方法在多个骨干模型（FLUX.1-Dev, SD3.5-M, Qwen-Image, Wan2.1-1.3B）和任务（文本到图像、图像到视频）上验证了其有效性和泛化能力。

**局限性**：
- 分支调度和剪枝策略的选择会显著影响奖励稳定性，需要原则性的树设计。
- 奖励融合在不同加权方案下的偏差-方差权衡需要进一步的理论分析。
- HPS-only训练会降低CLIP Score，需要多目标设置来缓解。
- 在长时视频生成任务上的验证尚不充分。

**开放问题**：
- 如何设计自适应策略，根据样本难度或中间奖励动态调整分支因子、相关性或剪枝窗口？
- 分支框架能否自然迁移到其他生成范式，如基于扩散的LLM和多模态基础模型？
- 如何将BranchGRPO扩展到高分辨率、长时视频生成任务？
- 如何将BranchGRPO应用于机器人动作生成和具身视频生成学习？

## 原文 PDF

![[paperPDFs/ICLR_2026/BranchGRPO_Stable_and_Efficient_GRPO_with_Structured_Branching_in_Diffusion_Models.pdf]]
