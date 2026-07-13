---
title: "SRPO: Self-Referential Policy Optimization for Vision-Language-Action Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SRPO_Self_Referential_Policy_Optimization_for_Vision_Language_Action_Models.pdf
project_link: null
code_link: "https://github.com/sii-research/siiRL"
huggingface_link: "https://huggingface.co/collections/Sylvest/srpo"
aliases:
- SSRPO
- SRPO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 自参照学习：利用当前训练批次中模型自身生成的成功轨迹作为参照标准，通过世界模型潜在表示度量失败轨迹的行为进展，为失败尝试分配逐步奖励。
primary_logic: 将任务无关的预训练世界模型潜在表示用于进展度量，使得奖励塑造具有跨环境泛化能力，无需依赖专家演示或手工任务分解，实现高效的自参照强化学习。
claims:
- SRPO在LIBERO基准上达到99.2%平均成功率，相对于one-shot SFT的48.9%基线提升103%
- SRPO在LIBERO-Plus扰动环境下总体成功率82.1，远超One-shot基线30.7，并超过全量SFT基线
- SRPO的进展奖励在Spearman相关性(0.998)、单调性(0.992)、分布分离度(MMD 0.615)等五项指标上全面优于像素级和ImageBind方法
- 去除自参照机制（使用固定专家轨迹）导致性能平台化且最终结果次优，需1.4倍训练步数
---

# SRPO: Self-Referential Policy Optimization for Vision-Language-Action Models

> [!tip] 核心洞察
> 将任务无关的预训练世界模型潜在表示用于进展度量，使得奖励塑造具有跨环境泛化能力，无需依赖专家演示或手工任务分解，实现高效的自参照强化学习。

| 字段 | 内容 |
|------|------|
| 中文题名 | SRPO: 面向视觉-语言-动作模型的自参照策略优化 |
| 英文题名 | SRPO: Self-Referential Policy Optimization for Vision-Language-Action Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.15605) · [Code](https://github.com/sii-research/siiRL) · [HuggingFace](https://huggingface.co/collections/Sylvest/srpo) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SRPO (Self-Referential Policy Optimization) |
| Dataset | LIBERO, LIBERO-Plus, Progress Reward Benchmark, Real-robot Progress Reward |

> [!tip] 效果简介
> - LIBERO 上，Average Success Rate (%) 99.2 (Online SRPO on OpenVLA*-One) vs 48.9 (OpenVLA*-One, one-shot SFT) (+50.3)。
> - LIBERO-Plus (with augmented data) 上，Total Success Rate (%) 82.1 (Online SRPO) vs 30.7 (OpenVLA*-One) (+51.4)。
> - Progress Reward Benchmark 上，Spearman Correlation (SC) 0.998 (SRPO) vs 0.125 (Pixel-level) / 0.957 (ImageBind) (substantially higher)。

## 概要

视觉-语言-动作（VLA）模型的强化学习（RL）微调是提升机器人策略性能的关键路径，但现有方法面临一个根本瓶颈：**奖励稀疏**。主流框架如GRPO仅依赖二值结果信号——成功得1、失败得0——完全浪费了失败轨迹中蕴含的丰富行为进展信息，导致训练效率低下、样本利用率极低。

SRPO（Self-Referential Policy Optimization）提出了一种**自参照范式**来破解这一瓶颈。其核心思想是：利用当前训练批次中模型自身生成的成功轨迹作为参照标准，通过预训练世界模型的潜在表示来度量失败轨迹的行为进展，从而为每一次失败尝试分配密集的进展感知奖励。这一设计消除了对外部专家演示或手工任务分解的依赖，使奖励塑造具有跨环境和跨任务的泛化能力。

**方法定位**：SRPO属于基于GRPO的VLA强化学习路线，但对其奖励信号密度和进展度量方式两个关键槽位进行了根本性改造——将稀疏二值结果奖励替换为基于自参照世界模型潜在表示的密集进展奖励。与依赖外部参照（专家轨迹、手工过程奖励模型）的方法不同，SRPO的“自参照”特性使其无需任何任务特定工程即可实现高效训练。

**核心结论**：
- 在LIBERO基准上，SRPO以仅200步在线RL达到**99.2%**的平均成功率，相对于one-shot SFT基线（48.9%）提升**103%**（Table 1）。
- 在LIBERO-Plus扰动环境下，SRPO总体成功率达**82.1**，远超one-shot基线（30.7），并超越全量SFT基线，展现出强泛化能力（Table 2）。
- SRPO的进展奖励在Spearman相关性（0.998）、单调性（0.992）、分布分离度等五项指标上全面优于像素级和ImageBind方法（Table 3），验证了潜在世界表示用于进展度量的有效性。
- 消融实验证实，去除自参照机制（改用固定专家轨迹）导致性能平台化且需1.4倍训练步数；去除聚类组件则后期性能增益显著降低（Figure 10），表明批次内动态参照和聚类表示是方法的关键设计要素。



### 1. VLA 策略强化学习的奖励稀疏瓶颈

视觉-语言-动作（VLA）模型通过在多样化机器人数据上的大规模预训练，展现了强大的任务泛化能力。然而，将 VLA 模型部署到具体操作任务时，仅依靠监督微调（SFT）往往难以获得鲁棒的行为策略。强化学习（RL）为策略的持续改进提供了自然的范式，但现有 VLA 强化学习方法面临一个核心瓶颈：**奖励稀疏**。

当前主流方法——如基于 GRPO 的 **SimpleVLA-RL**（Li et al., 2025）、**RIPT-VLA**（Tan et al., 2025）、**RLinf**（Zang et al., 2025）以及基于 PPO 的 **VLA-RL**（Lu et al., 2025）——普遍仅依赖二值结果奖励（成功为 1，失败为 0）。这种稀疏信号带来了两个严重后果：

- **学习信号匮乏**：失败轨迹中蕴含的丰富行为信息——策略在哪些步骤取得了进展、在何处偏离了正确方向——被完全丢弃，导致训练效率低下。
- **探索效率低下**：在复杂长时域任务中，随机探索碰巧成功的概率极低，策略难以获得任何正向反馈，形成恶性循环。

### 2. 现有奖励塑造方法的局限

为缓解奖励稀疏问题，研究者尝试引入过程奖励建模（Process Reward Modeling, PRM）来为中间步骤提供密集信号。然而，这些方法存在根本性缺陷（Figure 1）：

- **外部参照依赖**：需要人工标注的专家演示或手工设计的任务分解（如 **TGRPO**, Chen et al., 2025b），这在大规模多任务场景中成本高昂且难以扩展。
- **泛化能力不足**：基于像素级世界模型（如 **World-Env**, Xiao et al., 2025）的进展度量对光照、视角等感知变化高度敏感，且需要针对特定领域重新训练，缺乏跨环境泛化能力。

这些方法本质上仍是“外部参照”（External-Referential）范式——需要从策略外部引入参照标准来衡量进展，因而无法摆脱对人工设计或领域特定训练的依赖。

### 3. 核心动机：从外部参照到自参照

本文的核心洞察在于：**模型在当前训练批次中生成的成功轨迹，本身就可以作为衡量失败尝试进展的天然参照标准**。这一“自参照”（Self-Referential）范式将奖励塑造从外部依赖中解放出来，使得模型能够从自身的成功经验中学习如何评估进展。

然而，实现这一范式面临一个关键技术挑战：如何在缺乏任务特定知识的情况下，鲁棒地度量两条轨迹之间的“行为进展”？直接比较原始像素或关节角度会因视角变化、动作风格差异等因素而失效。本文的解决方案是利用**预训练世界模型的潜在表示**——这些表示在大规模机器人视频数据上习得，能够捕捉与任务进展相关的语义信息，同时抑制感知层面的噪声。

基于上述动机，本文提出了 **SRPO（Self-Referential Policy Optimization）**——一个面向 VLA 模型的自参照策略优化框架，通过在预训练世界模型的潜在空间中度量行为进展，为失败轨迹分配密集的进展感知奖励，从而高效利用所有采样轨迹进行策略优化。



## 核心方法与创新机理

### 问题瓶颈：稀疏奖励导致失败轨迹信息浪费

现有视觉-语言-动作（VLA）模型的强化学习微调方法——包括基于GRPO的**SimpleVLA-RL**（Li et al., 2025）、**RIPT-VLA**（Tan et al., 2025）、**RLinf**（Zang et al., 2025）以及基于PPO的**VLA-RL**（Lu et al., 2025）——普遍采用稀疏二值结果奖励：任务成功则得1，失败则得0。这种设计在机器人操作场景中造成严重的奖励稀疏问题：失败轨迹中蕴含的行为进展信息——例如机械臂是否接近了目标物体、抓取是否接近成功——被完全丢弃，导致训练信号极度匮乏，学习效率低下。

### 核心思路：自参照进展奖励

SRPO的核心创新在于将奖励信号从“外部参照”转变为“自参照”。其关键洞察是：**当前训练批次中模型自身生成的成功轨迹，天然构成了衡量进展的最佳参照标准**。基于这一思想，SRPO为失败轨迹分配密集的进展奖励，而非简单的零值惩罚，从而充分利用每一次交互经验。

具体而言，SRPO通过两个关键组件实现这一转变：

**1. 基于世界模型潜在表示的进展度量**

SRPO不依赖原始像素或域特定微调，而是利用在大规模机器人视频数据上预训练的世界模型编码器（V-JEPA 2）提取观测序列的共享潜在表示：

$$h_i = \mathcal{W}(o_{0:T}^{(i)})$$

在该潜在空间中，轨迹间的L2距离能够鲁棒地反映行为相似性。这一设计使得进展度量具有跨环境和跨任务的泛化能力，克服了传统像素级世界模型需要逐域训练的局限。

**2. DBSCAN聚类与自参照奖励计算**

对于批次内收集的成功轨迹表征集合$S$，SRPO使用DBSCAN聚类获取代表中心：

$$C = \mathrm{DBSCAN}(S)$$

对于失败轨迹，计算其表征到最近聚类中心的最小L2距离：

$$d_i = \operatorname*{min}\{\|h_i - h_j\|^2 \mid h_j \in C\}$$

最终进展奖励通过归一化和激活函数映射到$(0,1)$区间：

$$g_i = \begin{cases} 1.0 & \text{成功轨迹} \\ \phi\left(\frac{d_i - \bar{d}}{\sigma_d}\right) & \text{失败轨迹} \end{cases}$$

其中$\phi$为sigmoid激活函数，$\bar{d}$和$\sigma_d$为批次内失败轨迹距离的均值和标准差。这一设计使得失败轨迹越接近成功轨迹的行为模式，获得的奖励越高，从而为策略优化提供密集且有序的学习信号。

### Changed Slots：与传统GRPO的差异

| 维度 | 基线方法（GRPO系列） | SRPO |
|------|---------------------|------|
| 奖励信号密度 | 稀疏二值结果奖励 | 基于自参照世界模型潜在表示的密集进展奖励 |
| 进展度量与参照方式 | 无进展度量，仅用最终结果 | 利用预训练世界模型潜在表示计算L2距离并DBSCAN聚类，生成自参照进度奖励 |

### 与手工过程奖励方法的本质区别

与**TGRPO**（Chen et al., 2025b）等需要手工设计任务特定过程奖励的方法不同，SRPO的进展奖励完全自动生成，无需依赖专家演示或任务分解。与**World-Env**（Xiao et al., 2025）等使用世界模型作为仿真器进行规划的方法不同，SRPO将世界模型用作表示空间中的度量工具，而非生成未来状态。这一设计选择使得SRPO具有更强的泛化性：同一套进展奖励机制可无缝应用于不同任务，无需任何任务特定调整。

### 自参照机制的关键性：消融证据

消融实验验证了自参照设计的必要性。当移除自参照机制、改用固定专家轨迹作为参照标准时，训练出现性能平台化，最终成功率显著低于完整SRPO，且需要约1.4倍的训练步数才能达到收敛（Figure 10）。进一步移除聚类组件、仅使用单条最近成功轨迹作为参照时，初期收敛速度相似，但后期性能增益显著降低。这表明，DBSCAN聚类通过捕获成功轨迹的多模态分布，为失败轨迹提供了更鲁棒的进展估计，是SRPO性能优势的重要来源。



SRPO（Self-Referential Policy Optimization）的整体设计围绕一个核心瓶颈展开：**现有VLA强化学习方法仅依赖稀疏的二值成功信号，浪费了失败轨迹中丰富的进展信息**。SRPO通过引入“自参照”范式，将当前训练批次中策略自身生成的成功轨迹作为参照标准，利用预训练世界模型的潜在表示度量失败轨迹的行为进展，从而为失败尝试分配密集的进展奖励。

### 核心因果机制

框架的关键因果链路可概括为：**自参照成功轨迹 → 世界模型潜在编码 → 聚类中心计算 → 进展距离度量 → 密集奖励生成 → 策略优化**。具体而言：

1. **自参照参照系构建**：传统方法（如GRPO）依赖外部固定的成功标准或手工设计的进程奖励模型，而SRPO直接使用同一训练批次内策略自身生成的成功轨迹作为参照。这一设计消除了对外部专家演示或任务特定工程的依赖，使奖励塑造与策略能力同步进化。

2. **世界模型潜在表示**：SRPO采用在大规模机器人视频数据上预训练的V-JEPA 2世界模型编码器 $\mathcal{W}$，将每条轨迹的观测序列 $o_{0:T}^{(i)}$ 映射为潜在表示 $h_i$（Eq. 2）。该表示具有跨场景的迁移能力，克服了像素级世界模型需要逐域微调的泛化局限。

3. **进展度量与奖励生成**：对批次内的成功轨迹表征集合 $S$ 进行DBSCAN聚类，获得代表中心 $C$（Eq. 3）。失败轨迹的进展奖励 $g_i$ 由其表征到最近聚类中心的归一化L2距离决定（Eq. 4-5），成功轨迹直接获得奖励1.0。

4. **策略优化**：基于GRPO风格的组归一化优势估计和裁剪替代目标进行策略更新（Eq. 6-8），同时引入KL正则化约束策略偏离参考模型的程度。

### 管道模块与数据流

SRPO的完整管道包含五个核心模块，数据流从策略推演到参数更新形成闭环：

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| **预训练VLA骨干（OpenVLA\*）** | 基础策略模型，接受视觉观测和语言指令，输出动作序列 | 第三人称图像 $o_t$、语言指令 $l$ | 动作 $a_t$ |
| **世界模型编码器（V-JEPA 2）** | 提取观测序列的共享潜在世界表示 | 轨迹观测序列 $o_{0:T}^{(i)}$ | 潜在表征 $h_i$ |
| **DBSCAN聚类** | 对批次内成功轨迹表征进行聚类，获取代表中心 | 成功轨迹表征集合 $S$ | 聚类中心 $C$ |
| **进展奖励计算器** | 基于失败轨迹到最近聚类中心的距离计算进展奖励 | 失败轨迹表征 $h_i$、聚类中心 $C$ | 进展奖励 $g_i$ |
| **SRPO策略优化器** | 使用GRPO风格的优势估计与裁剪目标进行策略更新 | 轨迹奖励 $g_i$、动作对数概率 | 更新后的策略参数 $\theta$ |

管道以**单次演示监督微调（one-shot SFT）**为起点，随后进入在线强化学习阶段：策略在环境中推演生成轨迹批次，世界模型编码器提取潜在表示，进展奖励计算器为每条轨迹分配奖励，最终通过SRPO优化器更新策略参数。这一闭环设计使得奖励信号密度从二值跃升为连续进展值，显著提升了失败轨迹的信息利用率。

### 与基线方法的关键差异

相较于现有VLA强化学习方法，SRPO在两个关键维度上实现了范式转变：

- **奖励信号密度**：GRPO及其VLA变体（SimpleVLA-RL、RIPT-VLA、RLinf等）仅使用稀疏二值结果奖励；SRPO通过自参照世界模型潜在表示生成密集进展奖励，将失败轨迹从“无信息”转变为“部分进展信号”。

- **进展度量与参照方式**：TGRPO虽引入了任务特定进展奖励，但依赖手工设计的进程分解；SRPO利用任务无关的预训练世界模型潜在表示，无需任何任务特定工程即可度量行为进展，且参照标准来自策略自身而非外部专家。

### 补充图表

![[assets/figures/papers/paper_list_l2421_https_arxiv_org_abs_2511_15605/figures/001_Figure_1.jpg]]
*Figure 1: Overview of Self-Referential Policy Optimization (SRPO). Existing approaches for Vision-Language-Sparse Reward Dense RewardExpert Trajectory Action (VLA) reinforcement learning face significant limitations: (a) methods like GRPO rely solely on sparse External-Referential outcome rewards, providing limited learning signal, while (b) hand-crafted process reward modeling (PRM) r=0requires costly external demonstrations and task-specific engineering. In contrast, our SRPO framework Self-Referential introduces a self-referential paradigm that leverages (i) in-batch successful trajectories and (ii) latent world representations to construct progress-wise rewards, enabling efficient utilization of...*



SRPO 的核心架构由四个功能模块串联构成，形成“轨迹收集 → 世界表征提取 → 自参照进展奖励计算 → 策略优化”的闭环。以下按数据流顺序展开各模块及其关键公式。

### 1. 轨迹采样与观测生成

策略 $\pi_{\boldsymbol{\theta}}$ 以语言指令 $l$ 和第三人称视觉观测 $o_t$ 为条件，在环境状态 $z_t$ 下采样动作 $a_t$，环境返回下一状态 $z_{t+1}$，迭代产生完整轨迹：

$$o_t = O(z_t), \quad a_t \sim \pi_{\theta}(\cdot|o_t,l), \quad z_{t+1} \sim E(\cdot|z_t,a_t) \tag{1}$$

其中 $O$ 为观测函数，$E$ 为环境转移函数。每个训练批次收集 $M$ 条轨迹 $\{\tau^{(i)}\}_{i=1}^{M}$，按任务成功与否划分为成功集 $S$ 和失败集 $F$。

### 2. 世界模型潜在表征提取

SRPO 的关键创新在于使用预训练世界模型 $\mathcal{W}$ 将每条轨迹的观测序列 $o_{0:T}^{(i)}$ 压缩为统一的潜在向量 $h_i$：

$$h_i = \mathcal{W}(o_{0:T}^{(i)}) \tag{2}$$

$\mathcal{W}$ 基于 V-JEPA 2（Assran et al., 2025），在大规模机器人视频数据上预训练，其潜在空间具有任务无关的行为相似性度量能力。这一设计使进展度量能够跨场景泛化，无需针对特定任务微调。

### 3. 自参照进展奖励计算

**聚类参照中心。** 对批次内成功轨迹的潜在表征 $S = \{h_i \mid \tau^{(i)} \in S\}$ 执行 DBSCAN 聚类，获取代表中心集合 $C$：

$$C = \mathrm{DBSCAN}(S) \tag{3}$$

DBSCAN 的优势在于无需预设聚类数目，能自适应发现成功轨迹的多模态分布（例如同一任务存在多种可行解）。

**距离度量。** 对每条失败轨迹 $i \in F$，计算其潜在表征到最近聚类中心的 L2 距离：

$$d_i = \min(\{\|h_i - h_j\|^2 \mid h_j \in C\}) \tag{4}$$

**进展奖励映射。** 成功轨迹直接获得奖励 1.0；失败轨迹根据归一化距离通过激活函数 $\phi$（文中采用 sigmoid）映射到 $(0,1)$ 区间：

$$g_i = \begin{cases} 1.0 & \text{for success trajectory} \\ \phi\left(\frac{d_i - \bar{d}}{\sigma_d}\right) & \text{for failed trajectory} \end{cases} \tag{5}$$

其中 $\bar{d}$ 和 $\sigma_d$ 为批次内失败轨迹距离的均值和标准差。这一归一化使奖励在批次内具有相对可比性——距离聚类中心越近的失败轨迹获得越高的进展奖励，从而为“接近成功”的尝试提供密集学习信号。

**“自参照”的含义。** 参照标准 $C$ 来自当前训练批次中模型自身生成的成功轨迹，而非外部专家演示或手工设计的子任务分解。随着训练推进，策略能力提升，成功轨迹的质量和多样性同步增长，参照标准也随之自适应演化。

### 4. SRPO 策略优化目标

SRPO 采用 GRPO 风格的组内优势估计与裁剪目标进行策略更新。

**概率比与优势。** 对每条轨迹 $i$ 的每个时间步 $t$，计算新旧策略的概率比：

$$r_{i,t}(\theta) = \frac{\pi_{\theta}(a_t^{(i)}|o_t^{(i)},l)}{\pi_{\theta_{\text{old}}}(a_t^{(i)}|o_t^{(i)},l)} \tag{6}$$

优势估计在轨迹粒度上进行组归一化：$\hat{A}_i = \frac{g_i - \mu_g}{\sigma_g}$，其中 $\mu_g$ 和 $\sigma_g$ 为批次内 $M$ 条轨迹奖励的均值和标准差（见 Eq. 9）。这意味着优势信号完全由自参照进展奖励驱动，而非逐时间步的即时奖励。

**裁剪替代目标。** 最终优化目标为带裁剪的替代损失与 KL 正则化之和：

$$\mathcal{L}_{\mathrm{SRPO}}(\boldsymbol{\theta}) = \mathbb{E}_{t,i} \left[ \min\left(r_{i,t}(\theta) \hat{A}_i, \ \text{clip}(r_{i,t}(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_i\right) \right] + \beta D_{\mathrm{KL}}(\pi_{\theta} \parallel \pi_{\text{ref}}) \tag{8}$$

其中 $\pi_{\text{ref}}$ 为参考策略（通常为 SFT 初始化策略），$\beta$ 控制 KL 惩罚强度，防止策略偏离过远。

### 5. 模块间的因果链路

上述四个模块形成清晰的因果链：世界模型编码器 $\mathcal{W}$ 的质量决定了潜在空间中行为相似性度量的可靠性；DBSCAN 聚类决定了参照中心的代表性和覆盖度；进展奖励映射 $\phi$ 决定了失败轨迹学习信号的密度和区分度；最终 SRPO 优化目标将进展奖励转化为策略改进的梯度方向。消融实验（Figure 10）验证了这一链路中每个环节的必要性：移除自参照机制（使用固定专家轨迹）导致性能平台化，移除聚类组件（使用单条最近成功轨迹）则显著降低后期性能增益。

### 补充图表

![[assets/figures/papers/paper_list_l2421_https_arxiv_org_abs_2511_15605/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the SRPO method. During policy rollout, both successful and failed trajectories are collected in the Rollout Reference Set. For each trajectory, we employ a world model pre-trained on large-scale robotics video data (Assran et al., 2025) as an encoder to extract latent world representations. Behavioral Optimizationsimilarity is modeled as the L2 distance between trajectory embeddings in this space to yield progress-wise rewards. These rewards are subsequently used for advantage estimation and policy optimization under KL regularization*



## 实验与关键发现

### 核心结果：LIBERO基准性能突破

SRPO在LIBERO基准上实现了从稀疏奖励基线到近乎完美性能的跨越。如表1所示，基于one-shot SFT初始化的在线SRPO（OpenVLA*-One + SRPO）在四个任务套件的平均成功率达到**99.2%**，相比仅使用one-shot SFT的基线（48.9%）提升了**103%**的相对幅度。这一结果将VLA强化学习在LIBERO上的表现推向了新高度——仅需200步在线RL交互，SRPO便从单条演示的监督微调起点收敛至接近饱和的性能。

更值得关注的是SRPO在输入模态上的公平性优势。表1中，多数基线方法使用了额外模态输入：**SimpleVLA-RL**（Li et al., 2025）和**RLinf**（Zang et al., 2025）同时使用第三人称视觉(T)、腕部图像(W)、本体感知(P)和深度(D)；**TGRPO**（Chen et al., 2025b）使用T+W+P+I。SRPO仅使用第三人称视觉和语言指令（T+I），却在所有套件上超越了这些多模态基线，表明其性能增益并非来自信息优势，而是源自自参照奖励机制对学习信号的根本性改善。

离线SRPO同样展现了强大的提升能力：在one-shot SFT基础上，离线SRPO的平均成功率提升达**↑43.6%**，将多个套件的成功率从不足50%推升至80%以上。

### 泛化鲁棒性：LIBERO-Plus扰动环境

LIBERO-Plus基准通过引入7种扰动维度（光照、纹理、相机视角、目标物体外观、背景、干扰物、初始状态分布）来测试策略的泛化能力。表2的结果揭示了SRPO的鲁棒性优势：

- **零样本泛化**：在线SRPO在零样本设置下（未使用增强数据训练）达到**70.9%**的总成功率，相比one-shot基线（30.7%）提升**↑40.2**个百分点。
- **数据增强后性能**：使用增强数据训练的在线SRPO达到**82.1%**的总成功率，不仅远超one-shot基线，还**超越了全量SFT基线**（OpenVLA*-Full的73.0%），表明自参照RL学到的策略比在更多演示上做行为克隆更具泛化性。
- **离线SRPO**在增强数据设置下同样达到**71.1%**，相比one-shot基线提升**↑40.4**个百分点。

这一结果的核心含义是：SRPO通过自参照进展奖励，使策略在探索过程中学到的是对任务进展的深层理解，而非对训练场景的过拟合，从而在未见过的视觉和物理扰动下保持鲁棒。

### 进展奖励质量验证

SRPO的核心创新在于用世界模型潜在表示度量行为进展。表3通过五项定量指标系统评估了这一进展奖励的质量：

| 指标 | 像素级方法 | ImageBind | **SRPO（本文）** |
|------|-----------|-----------|-----------------|
| Spearman相关性 (SC) ↑ | 0.125 | 0.957 | **0.998** |
| 单调性 (Mono) ↑ | — | — | **0.992** |
| MMD ↑ | — | — | **0.615** |
| JS散度 ↑ | — | — | **0.348** |
| 标准化均值差 (SMD) ↑ | — | — | **1.290** |

SRPO在所有五项指标上均取得最优。Spearman相关性**0.998**表明进展奖励与真实时间步序几乎完美单调相关；单调性**0.992**意味着奖励曲线极少出现倒退；MMD和JS散度的高值说明成功与失败轨迹的进展分布在潜在空间中具有显著分离度，使得奖励信号能够有效区分不同程度的进展。

定性可视化（Figure 3）进一步揭示了不同方法的本质差异：像素级方法对光照和纹理变化过度敏感，产生噪声奖励；ImageBind方法在机器人急动时出现锯齿状波动；SRPO的奖励曲线呈现平滑单调的物理合理趋势——在抓取暂停时奖励出现合理的小幅回落（Figure 9a），而失败轨迹的奖励则停滞在低值区间（Figure 9b），无法攀升至成功水平。

![[assets/figures/papers/paper_list_l2421_https_arxiv_org_abs_2511_15605/figures/006_Figure_3.jpg]]
*Figure 3: Comparison of progress estimation methods in simulated (a-c) and real-world (d-f) environments. Our SRPO reward (a,d) provides monotonic and physically plausible progress estimation. Pixel-level rewards (b,e) show sensitivity to perceptual changes, while ImageBind rewards (c,f) exhibit erratic trends from jerky motions*

真实机器人数据集上的验证（Table 4）显示，SRPO在5个真实操作任务上的平均Spearman相关性达到**0.989**，保持了与仿真环境一致的进展度量质量，证明了世界模型潜在表示跨域泛化的有效性。

![[assets/figures/papers/paper_list_l2421_https_arxiv_org_abs_2511_15605/figures/015_Table_4.jpg]]
*Table 4: Progress Reward Benchmark results on realrobot datasets. Our method maintains strong performance across all tasks and metrics, demonstrating robust generalization to diverse real-world manipulation tasks*

### 训练效率与策略行为分析

Figure 5展示了SRPO与标准GRPO的训练效率对比。在LIBERO-Long和LIBERO-Object套件上，SRPO的收敛速度显著快于仅使用稀疏结果奖励的GRPO，验证了密集进展奖励对样本效率的提升。

端执行器轨迹可视化（Figure 6, 7）揭示了SRPO学到的策略行为特征：相比全量SFT策略的保守轨迹，SRPO在线RL策略展现出更丰富的探索行为——在“将碗放在柜子顶部”任务中，SRPO策略的末端执行器轨迹覆盖了更大的动作空间，表明自参照奖励鼓励了更广泛的有效探索，而非仅模仿演示中的单一路径。

![[assets/figures/papers/paper_list_l2421_https_arxiv_org_abs_2511_15605/figures/009_Figure_6.jpg]]
*Figure 6: Action space comparison of end-effector trajectories between (a) full-shot supervised fine-tuning (SFT) and (b) SRPO online reinforcement learning (RL) policies*

### 消融实验：自参照与聚类的必要性

Figure 10的消融实验揭示了两个关键设计选择的作用：

- **去除自参照机制（w/o Referential）**：使用固定的专家成功轨迹替代自参照，导致性能出现平台化——训练初期有提升，但最终收敛结果显著低于完整SRPO，且需要约**1.4倍**的训练步数才能达到次优水平。这表明自参照机制（使用当前模型自身生成的成功轨迹作为参照）对于持续的性能增长至关重要，因为随着策略改进，成功轨迹的质量也在提升，形成正向循环；固定专家轨迹则无法适应策略的进化。

- **去除聚类组件（w/o Cluster）**：仅使用单条最近成功轨迹计算进展奖励，初期收敛速度与完整方法相似，但后期性能增益显著降低。这说明DBSCAN聚类通过捕捉成功轨迹的多模态分布（同一任务可能存在多种成功方式），为失败轨迹提供了更鲁棒的进展度量基准。

### 超参数敏感性

Figure 11展示了奖励函数中进展项权重α的敏感性分析。α控制着进展奖励与结果奖励的平衡：α=0时退化为纯稀疏结果奖励（GRPO），性能最差；α=0.8时达到最优性能；α=1.0（仅使用进展奖励，无结果奖励）性能次之。这一趋势验证了同时考虑进展感知与结果正确性的必要性——纯粹的进展奖励可能鼓励策略在任务空间中“移动”但未必完成目标，而结果奖励提供了最终的校正信号。

### 失败模式与局限性

尽管SRPO在LIBERO上取得了99.2%的平均成功率，仍需注意以下局限：

1. **真实机器人验证仅限离线RL**：真实世界实验采用离线强化学习范式，在线部署的安全性未经验证。从仿真到真实机器人的在线迁移仍面临安全探索的挑战。

2. **世界模型表示的泛化边界**：进展奖励的质量依赖V-JEPA 2在大规模机器人视频上的预训练质量。对于与预训练分布差异较大的新场景（如特殊光照、非标准机器人形态），潜在表示的有效性需要进一步验证。

3. **精细操作的限制**：SRPO仅使用第三人称视觉输入，缺乏腕部相机等精细感知。对于需要毫米级精度的操作任务，仅靠全局视角的进展度量可能不足以提供足够的反馈信号。

4. **超参数α的任务依赖性**：α的最优值（0.8）是在LIBERO基准上调定的，不同任务可能需要不同的进展-结果平衡权重，这限制了零样本部署的便捷性。

### 补充图表

![[assets/figures/papers/paper_list_l2421_https_arxiv_org_abs_2511_15605/figures/003_Table_1.jpg]]
*Table 1: Performance comparison on LIBERO benchmark. We evaluate mainstream VLA foundation models and RL-based methods. OpenVLA* incorporates action chunking and parallel decoding on the basis of OpenVLA. Policy Input notation: T (Thirdview), I (Instrcution), P (Proprio), W (Wristimage), D (Depth). Our approach, built upon one-shot SFT, achieves state-of-the-art results on LIBERO benchmark, with ↑ indicating performance gains over the one-shot baseline*

![[assets/figures/papers/paper_list_l2421_https_arxiv_org_abs_2511_15605/figures/004_Table_2.jpg]]
*Table 2: Robustness Evaluation on LIBERO-Plus Benchmark. OpenVLA-OFT+ refers to the OpenVLA-OFT model that has been trained on the LIBERO-Plus dataset. Our method, SRPO, applied to a one-shot SFT policy, not only significantly outperforms its base model but also surpasses the full-shot SFT baseline in all 7 dimensions, demonstrating superior generalization capability. The ↑ indicates performance gains over the One-shot SFT base model*

![[assets/figures/papers/paper_list_l2421_https_arxiv_org_abs_2511_15605/figures/005_Table_3.jpg]]
*Table 3: Progress Reward Benchmark Results. Our method achieved a better level than the baseline in all 5 indicators*

![[assets/figures/papers/paper_list_l2421_https_arxiv_org_abs_2511_15605/figures/007_Figure_4.jpg]]
*Figure 4: Training performance comparison using different progress reward formulations. Our SRPO-based reward enables stable and efficient learning, consistently outperforming both baselines*

![[assets/figures/papers/paper_list_l2421_https_arxiv_org_abs_2511_15605/figures/008_Figure_5.jpg]]
*Figure 5: Training efficiency comparison between SRPO and GRPO: (a) LIBERO-Long, (b) LIBERO-Object*

![[assets/figures/papers/paper_list_l2421_https_arxiv_org_abs_2511_15605/figures/013_Figure_10.jpg]]
*Figure 10: Ablation study on Object suite. We compare our SRPO method against its ablated variants. Removing the referential component (w/o Referential) leads to significant performance drop, while removing the clustering component (w/o Cluster) slows down convergence*

![[assets/figures/papers/paper_list_l2421_https_arxiv_org_abs_2511_15605/figures/014_Figure_11.jpg]]
*Figure 11: Performance comparison with different α values in the reward function. The results demonstrate that α = 0.8 achieves the best performance, followed by*



## 定位与知识库关联

### 1. 在VLA强化学习谱系中的位置

SRPO解决的核心问题是**VLA（视觉-语言-动作）模型在线强化学习中的奖励稀疏瓶颈**。现有VLA-RL方法主要沿两条技术路线演进：

**路线一：基于GRPO的稀疏奖励方法。** GRPO（Shao et al., 2024）作为组归一化策略优化框架，在LLM对齐中取得成功后，被多项工作引入VLA领域。SimpleVLA-RL（Li et al., 2025）、RIPT-VLA（Tan et al., 2025）、RLinf（Zang et al., 2025）均采用GRPO框架，但仅依赖二值成功信号作为奖励。这类方法的根本局限在于：失败轨迹被完全浪费，训练信号密度极低，导致样本效率低下。

**路线二：手工进度奖励方法。** TGRPO（Chen et al., 2025b）尝试引入任务特定的进度奖励，但需要手工设计任务分解和专家演示作为参照。VLA-RL（Lu et al., 2025）基于PPO框架，同样面临奖励设计依赖领域知识的困境。World-Env（Xiao et al., 2025）使用世界模型作为RL模拟器，但需要额外训练特定于任务的世界模型。

SRPO的关键创新在于**将参照系从外部专家轨迹转向模型自身生成的成功轨迹**，同时利用**任务无关的预训练世界模型潜在表示**进行进展度量。这一设计使SRPO同时规避了稀疏奖励的信息浪费和手工奖励工程的泛化局限。

### 2. 技术继承与差异化

SRPO在三个层面继承了现有工作并做出关键改变：

**策略优化框架：继承GRPO。** SRPO采用GRPO的概率比计算、组归一化优势估计和KL正则化（Eq. 6-8），但将奖励信号从稀疏二值结果奖励替换为基于自参照世界模型潜在表示的密集进展奖励。这一替换改变了优化动力学：GRPO仅在轨迹结束时获得学习信号，SRPO则为失败轨迹提供连续的进展反馈。

**世界模型编码器：继承V-JEPA 2。** 使用在大规模机器人视频数据上预训练的V-JEPA 2（Assran et al., 2025）作为世界模型编码器$\mathcal{W}$，提取观测序列的潜在表示（Eq. 2）。与传统像素级世界模型不同，V-JEPA 2的潜在表示具有跨环境泛化能力，这是SRPO进展奖励能够跨任务一致有效的关键。

**训练流水线：继承SiiRL。** 基于SiiRL（Wang et al., 2025c）构建训练框架，采用先监督微调后在线RL的流水线。SRPO的独特之处在于仅需每条任务一个演示（one-shot SFT）即可启动RL训练，而多数方法依赖全量SFT初始化。

### 3. 适用边界与局限

**已验证的适用场景：**
- 桌面操作任务（LIBERO基准的四个套件，共20+任务）
- 扰动泛化场景（LIBERO-Plus的7类扰动，包括光照、纹理、物体位置等变化）
- 真实机器人操作（离线RL范式下的5类任务）

**已知局限：**

1. **在线部署安全性未验证。** 真实机器人实验采用离线RL范式，利用预收集的轨迹数据进行训练。在线真实机器人训练的安全约束（如碰撞避免、力限制）尚未在SRPO框架中解决。

2. **世界模型表示的泛化边界不明确。** 进展奖励的质量依赖于V-JEPA 2在大规模视频数据上的预训练质量。对于与预训练分布差异显著的场景（如非刚性物体操作、动态环境），潜在表示是否能保持单调进展度量需要进一步验证。

3. **感知模态的局限性。** SRPO仅使用第三人称视觉和语言指令，缺乏腕部相机、触觉等精细感知输入。对于需要精确力控或遮挡严重的精细操作任务，当前输入模态可能不足以支持准确的进展评估。

4. **超参数敏感性。** 进展奖励权重$\alpha$需要针对不同任务调整（消融实验显示$\alpha=0.8$最优，Figure 11），表明进展感知与结果正确性之间的平衡可能不具有跨任务一致性。

### 4. 未解决的问题

1. **稀疏成功初始阶段的有效性。** 自参照机制依赖批次内存在成功轨迹作为参照。在训练初期或极难任务中，成功轨迹可能极为稀少甚至缺失，此时DBSCAN聚类和进展奖励的可靠性需要验证。论文未报告成功轨迹比例低于某阈值时的行为。

2. **多模态输入与多任务扩展。** SRPO能否整合腕部图像、深度图、本体感知等多模态输入以提升进展度量的精度？在多任务联合训练场景下，世界模型潜在表示是否能保持任务间的可分离性？

3. **更细粒度的子任务奖励分解。** 当前进展奖励是轨迹级别的标量，未能区分不同子任务阶段的进展。潜在世界表示是否能支持子任务级别的自动分解和分层奖励塑造，是一个开放问题。

4. **安全约束下的在线训练。** 如何在不牺牲探索效率的前提下，将SRPO扩展到带安全约束的在线真实机器人训练，是实际部署的关键挑战。



## 原文 PDF

![[paperPDFs/CVPR_2026/SRPO_Self_Referential_Policy_Optimization_for_Vision_Language_Action_Models.pdf]]
