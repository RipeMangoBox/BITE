---
title: "Shuffle-R1: Efficient RL framework for Multimodal Large Language Models via Data-centric Dynamic Shuffle"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Shuffle_R1_Efficient_RL_framework_for_Multimodal_Large_Language_Models_via_Data_centric_Dynamic_Shuffle.pdf
project_link: https://xenozlh.github.io/Shuffle-R1
code_link: null
openreview_forum_id: mYP33u1QBK
aliases:
- SR
- Shuffle-R1
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过动态优先级采样机制——对比度轨迹对选择（PTS）和基于优势的批次重组（ABS）——放大高信息量的梯度信号，抑制低质量轨迹的影响。这一机制直接控制梯度更新的来源和质量，从而实现更高效的RL训练。"
primary_logic: "RL训练中不同轨迹的学习信号质量存在根本性差异，静态均匀采样会稀释关键梯度。通过构建高对比度轨迹对并自适应重塑批次分布，能够将有限的模型更新资源集中到最有价值的梯度信号上，显著提升MLLM的推理能力和训练效率。"
claims:
- "PTS有效缓解了优势值坍塌，增加了大绝对优势值的比例。"
- "消融实验证明PTS和ABS各自及联合的贡献，联合使用达到最佳性能。"
- "Shuffle-R1在多个视觉推理基准上超越强RL基线，且训练效率更高。"
- "理论分析证明动态采样放大梯度的期望和范数，并引入正偏差，从而加速训练。"
---

# Shuffle-R1: Efficient RL framework for Multimodal Large Language Models via Data-centric Dynamic Shuffle

> [!tip] 核心洞察
> RL训练中不同轨迹的学习信号质量存在根本性差异，静态均匀采样会稀释关键梯度。通过构建高对比度轨迹对并自适应重塑批次分布，能够将有限的模型更新资源集中到最有价值的梯度信号上，显著提升MLLM的推理能力和训练效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Shuffle-R1：通过数据中心动态重组实现多模态大语言模型的高效强化学习框架 |
| 英文题名 | Shuffle-R1: Efficient RL framework for Multimodal Large Language Models via Data-centric Dynamic Shuffle |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=mYP33u1QBK) · [Project](https://xenozlh.github.io/Shuffle-R1) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Shuffle-R1 |
| Dataset | Geometry3K (Geo3K), K12, Six visual reasoning benchmarks (MathVerse, MathVision, MathVista, WeMath, HallBench, ChartQA) |

> [!tip] 效果简介
> - Geometry3K (Geo3K) 上，Accuracy 为 47.88 (Qwen-3B)，对比 42.64 (GRPO, Qwen-3B)，变化 +5.24。
> - Geometry3K (Geo3K) 上，Accuracy 为 55.89 (Qwen-7B)，对比 52.60 (GRPO, Qwen-7B)，变化 +3.29。
> - K12 上，Accuracy 为 62.22 (Qwen-3B)，对比 42.42 (Base Qwen-3B)，变化 +19.80。

## 概要

当前多模态大语言模型（MLLM）的强化学习（RL）训练面临一个核心瓶颈：**学习信号的质量分布极度不均**。标准训练范式对每条采样轨迹一视同仁，但实际中大量轨迹的优势值（Advantage）坍塌在零附近，无法提供有效的梯度更新方向；与此同时，能够产生非零梯度的“有效轨迹”比例随着训练进行持续下降，造成大量计算资源浪费。这两个现象——**优势值坍塌（Advantage Collapsing）**与**有效轨迹沉默（Rollout Silencing）**——共同导致RL训练效率低下，模型推理能力的提升受到严重制约。

针对这一问题，本文提出 **Shuffle-R1**，一个以数据为中心的动态强化学习框架。其核心洞察在于：不同轨迹所携带的学习信号存在根本性差异，通过动态识别并优先利用高信息量的梯度信号，可以显著提升训练效率。Shuffle-R1 包含两个关键模块：

- **对比度轨迹对选择（Pairwise Trajectory Sampling, PTS）**：从扩展的采样池中按“max-min”原则构建高对比度轨迹对，仅保留优势差距最大的配对参与梯度更新，有效缓解优势值坍塌。
- **基于优势的批次重组（Advantage-based Batch Shuffle, ABS）**：根据轨迹对的绝对优势之和计算重要性权重，通过多轮加权子采样重塑批次分布，使高价值样本获得更高的曝光率，从而抑制有效轨迹沉默。

在方法谱系上，Shuffle-R1 区别于传统的静态均匀采样范式（如 **GRPO**，Shao et al., 2024）和基于规则的预过滤方法，开创了一种**动态交互式采样范式**——训练过程中根据模型实时输出的优势信号自适应调整数据分布。与 **DAPO**（Yu et al., 2025）、**GSPO**（Zheng et al., 2025）等改进型RL算法相比，Shuffle-R1 从数据采样的角度切入，而非修改优化目标或重要性权重估计，具有更强的即插即用特性。

实验结果表明，Shuffle-R1 在多个视觉推理基准上实现了对强RL基线的显著超越。在 Geometry3K 数据集上，Shuffle-R1 在 Qwen-3B 上达到 47.88% 的准确率（GRPO 为 42.64%，提升 +5.24），在 Qwen-7B 上达到 55.89%（GRPO 为 52.60%，提升 +3.29）。在大规模 30k 联合训练实验中，Shuffle-R1-Qwen-7B 在六个代表性基准上的总平均准确率达到 64.7%，较基座模型提升 +7.3%。更重要的是，在训练效率方面，Shuffle-R1 仅需 GRPO 约一半的训练步数和约 60% 的总 GPU 时间即可达到相同精度，额外时间开销仅为 4%~7.7%。

消融实验证实了 PTS 和 ABS 的独立贡献与协同效应：PTS 单独使用带来 +3.57 的准确率提升，联合 ABS 进一步增加 +1.67。理论分析从梯度期望放大、梯度范数放大和正偏差引入三个角度，为动态采样的有效性提供了形式化支撑。该方法还展现出良好的通用性，成功扩展到 32B 参数模型、指代表达理解（REC）任务以及纯文本大语言模型。



### 多模态大语言模型RL训练的现状与瓶颈

强化学习（Reinforcement Learning, RL）已成为提升多模态大语言模型（MLLM）推理能力的关键范式。以GRPO（Shao et al., 2024）为代表的群体相对策略优化方法，通过采样多条轨迹并利用组内归一化的优势函数进行梯度更新，在视觉推理任务上取得了显著进展。然而，当前RL训练框架大多采用**静态采样范式**——对每个查询均匀采样固定数量的轨迹，所有轨迹平等地参与梯度更新，这一设计隐含地假设每条轨迹携带的学习信号质量是均等的。

本文揭示了这一假设背后的两个根本性瓶颈（**Figure 1**）：

1. **优势值坍塌（Advantage Collapsing）**：在标准RL训练中，绝大多数轨迹的优势值集中在零附近，形成高度集中的分布。这意味着大部分梯度更新信号微弱，真正具有大绝对优势值、能提供强有力学习信号的轨迹被淹没在噪声之中。模型难以从这些“平庸”的轨迹中高效学习。

2. **有效轨迹沉默（Rollout Silencing）**：随着训练的进行，能够产生非零梯度（即对策略更新有实际贡献）的轨迹比例持续下降。大量计算资源被浪费在无效轨迹的生成和评估上，训练效率严重受损。

这两个问题相互耦合：优势值坍塌导致优质梯度信号稀疏，而有效轨迹沉默则使得本就稀缺的信号进一步被稀释。静态采样范式无法区分学习信号的质量差异，成为制约MLLM推理能力提升和训练效率的隐性瓶颈。

### 现有范式的局限

为应对上述问题，部分工作尝试在采样阶段引入**基于规则的预过滤机制**（**Figure 2(b)**），例如仅保留格式正确或答案长度合理的轨迹。然而，这类方法依赖固定的启发式规则，无法动态适应模型训练状态的变化，且规则设计本身需要大量领域知识，难以泛化。

更根本的问题在于，无论是静态采样还是规则预过滤，都缺乏与模型训练过程的**动态交互**——它们无法根据当前模型的能力和梯度信号的质量，自适应地调整采样的优先级和批次的构成。这导致训练资源被低效分配，关键的学习信号被系统性地低估。

### 核心动机与分析洞察

本文的动机源于一个关键观察：**不同轨迹的学习信号质量存在根本性差异**。如**Figure 3**所示，增大rollout数量可以提升模型准确率，但不同难度的查询在训练过程中的准确率变化模式各异，产生的轨迹在多样性和质量上也存在显著差异。这暗示着，并非所有轨迹对学习的贡献是等价的——通过识别并优先利用那些携带高信息量梯度信号的轨迹，有望在相同甚至更少的计算资源下实现更高效的RL训练。

基于此，本文提出**数据中心动态重组（Data-centric Dynamic Shuffle）** 的核心思路：在RL训练的每个迭代中，通过动态优先级采样机制，放大高信息量的梯度信号，抑制低质量轨迹的影响，从而将有限的模型更新资源集中到最有价值的梯度信号上。这一思路催生了Shuffle-R1框架的两个关键模块——**对比度轨迹对选择（Pairwise Trajectory Sampling, PTS）** 和**基于优势的批次重组（Advantage-based Batch Shuffle, ABS）**，分别针对优势值坍塌和有效轨迹沉默这两个瓶颈进行精准干预。



## 核心方法与创新机理

Shuffle-R1 的核心创新在于将 RL 训练从**静态均匀采样**范式转变为**数据中心动态优先级采样**范式，通过两个紧密协作的模块——对比度轨迹对选择（PTS）和基于优势的批次重组（ABS）——直接控制梯度更新的来源和质量，从而系统性地解决 MLLM 强化学习训练中的两大瓶颈。

### 问题诊断：优势值坍塌与有效轨迹沉默

现有 MLLM 的 RL 训练（如 GRPO）面临两个此前未被充分探索的结构性问题：

- **优势值坍塌（Advantage Collapsing）**：训练批次中绝大多数轨迹的优势值集中在零附近（Figure 1a），导致梯度信号微弱，模型难以从大量样本中提取有效的学习信号。
- **有效轨迹沉默（Rollout Silencing）**：随着训练进行，产生非零梯度的轨迹比例持续下降（Figure 1b），大量计算资源被浪费在对模型更新无贡献的轨迹上。

这两个问题的根源在于静态采样范式无法区分学习信号的质量差异——无论轨迹携带的梯度信息丰富与否，都被一视同仁地用于参数更新（Figure 2a）。基于规则的预过滤方法（Figure 2b）虽然试图筛选高质量轨迹，但无法与训练过程中的模型状态动态交互，难以适应不断变化的学习需求。

### Changed Slot 1：轨迹采样策略——从均匀采样到对比度配对选择

**Baseline（GRPO）**：对每个查询采样 $N$ 条轨迹，全部用于梯度更新，不区分轨迹的信号质量。

**Shuffle-R1（PTS）**：采样 $2N$ 条轨迹，按 max-min 原则配对为 $N$ 对，仅保留前 $M = \alpha N$ 对高对比度轨迹参与后续更新。具体而言：

1. **扩展采样**：对每个查询生成 $2N$ 条轨迹，计算各自的优势值 $\hat{A}_i$。
2. **降序排列**：将 $2N$ 条轨迹按优势值降序排列：
   $$A_s = \{ \hat{A}_{(i)} \}_{i=1}^{2N}, \quad \hat{A}_{(1)} \geq \hat{A}_{(2)} \geq \cdots \geq \hat{A}_{(2N)}$$
3. **max-min 配对**：将最高优势轨迹与最低优势轨迹配对，次高与次低配对，依此类推，构建 $N$ 个高对比度轨迹对：
   $$P = \{ (o_{(i)}, o_{(2N-i+1)}) \}_{i=1}^{N}$$
4. **Top-k 筛选**：仅保留前 $M$ 对（$M = \alpha N$，$\alpha \in (0,1)$）用于梯度更新：
   $$P_v = \{ (o_{(i)}, o_{(2N-i+1)}) \}_{i=1}^{M}$$

这一设计的核心洞察在于：**正负样本之间的大优势差能够产生更强的梯度信号**。通过刻意将高奖励轨迹与低奖励轨迹配对，PTS 放大了批次内优势值的离散程度，有效缓解了优势值坍塌。Figure 5 的优势分布分析直接证实了这一点——PTS 使大批次中大幅值优势的比例显著增加。

消融实验进一步验证了配对策略的关键性（Table 5）：双向 max-min 对比采样显著优于仅选择最高优势（+max）、仅选择最低优势（+min）或随机选择策略，证明**对比配对本身**而非简单的样本筛选是性能提升的根本原因。

### Changed Slot 2：批次构建策略——从静态分组到自适应加权重组

**Baseline（GRPO）**：轨迹按原始采样顺序静态分组为批次，高价值和低价值样本在批次中具有相同的曝光频率。

**Shuffle-R1（ABS）**：在 PTS 筛选出的轨迹对基础上，根据每对轨迹的绝对优势之和计算重要性权重，进行多轮加权子采样与重组，形成自适应批次。具体而言：

1. **重要性权重计算**：对每个轨迹对 $p_j$，以其两条轨迹的绝对优势之和作为权重：
   $$W(p_j) = |\hat{A}_{j,1}| + |\hat{A}_{j,2}|$$
2. **归一化采样分布**：在批次内构建加权采样概率：
   $$\Phi(p_j) = \frac{W(p_j)}{\sum_{k=1}^{|B|} W(p_k)}$$
3. **多轮重组**：从原始批次中按 $\Phi$ 进行加权子采样，重复 $S$ 次 Shuffle，形成与原始批次等大小的重组批次。高权重轨迹对被采样的概率更高，从而在训练中获得更多曝光。

ABS 的关键作用在于缓解有效轨迹沉默：通过让高信息量轨迹对在批次中反复出现，模型将更多更新资源集中在能产生有效梯度的样本上。Figure 6(c) 显示 Shuffle-R1 在整个训练阶段维持了高 token 利用率，而 Figure 9 的对比实验表明，与离线优先经验回放（Prioritized Experience Replay）相比，在线的 ABS 避免了过拟合历史样本，在训练后期保持更好的性能。

### 理论支撑：梯度信号的放大与正偏差

Shuffle-R1 的设计不仅有经验验证，还有理论分析支撑。论文的三个命题（Proposition 1-3）从梯度期望、梯度范数和偏差角度证明了动态采样策略的有效性：

- **优势期望放大**：PTS 的对比配对使得参与更新的轨迹对的期望优势差大于均匀采样，从而放大了梯度更新的驱动力。
- **梯度范数放大**：ABS 的加权重组增加了批次内梯度的期望范数，加速了参数更新。
- **正偏差引入**：自适应采样引入了正偏差，使模型倾向于学习高奖励行为，进一步加速了收敛。

### 联合效应：1+1>2

PTS 和 ABS 并非孤立运作，而是形成互补的级联机制。PTS 负责从扩展的采样池中“提纯”出高对比度轨迹对，解决优势值坍塌；ABS 则在 PTS 的输出基础上“浓缩”批次，让高价值样本获得更多训练曝光，解决有效轨迹沉默。消融实验（Table 4）清晰展示了二者的协同效应：单独使用 PTS 将 Geo3K 准确率从 42.64% 提升至 46.21%（+3.57），叠加 ABS 后进一步达到 47.88%（+1.67），验证了联合设计的必要性。

### 效率优势：以更少的训练成本实现更强的性能

Shuffle-R1 的动态采样策略虽然引入了额外的计算开销（扩展采样和批次重组），但换来了训练效率的大幅提升。Figure 7 的 wall-clock 训练曲线显示，Shuffle-R1 在早期训练阶段即大幅领先 GRPO，仅需约一半的训练步数即可达到 GRPO 的最终性能，总 GPU 时间仅增加 4%~7.7%。这种“以少量额外计算换取显著加速收敛”的特性，使 Shuffle-R1 在实际部署中具有明显的效率优势。



![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_mYP33u1QBK/figures/004_Figure_4.jpg]]
*Figure 4: Overview of our proposed Shuffle-R1. After advantage calculation, we first conduct Pairwise Trajectory Sampling to obtain valuable trajectory pairs from original rollout pool, then perform Advantage-based Batch Shuffle to reshape the distribution of valid trajectories in a batch*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_mYP33u1QBK/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline comparison. (a) Static paradigm. (b) Rule-based pre-filter paradigm. (c) Dynamic paradigm can ‘interact’ with model during training*

### 范式转换：从静态采样到动态优先级

当前多模态大语言模型（MLLM）的强化学习（RL）训练普遍采用静态采样范式：对每个查询均匀采样固定数量的轨迹，全部用于梯度更新。这种策略隐含假设所有轨迹携带等量的学习信号，但实际训练中存在两个严重瓶颈：

- **优势值坍塌（Advantage Collapsing）**：绝大多数轨迹的优势值集中在零附近，导致优质梯度信号被淹没（图1a）。
- **有效轨迹沉默（Rollout Silencing）**：随着训练进行，产生非零梯度的轨迹比例持续下降，大量计算被浪费（图1b）。

Shuffle-R1 提出了一种**数据中心动态交互范式**（图2c），核心思想是：**在训练过程中根据轨迹的学习信号质量动态调整样本优先级**，将有限的模型更新资源集中到高信息量的梯度信号上。与静态范式（图2a）和基于规则的预过滤范式（图2b）不同，动态范式能够与模型状态实时交互，自适应地识别和放大有价值的训练样本。

### Pipeline 总览

Shuffle-R1 的整体流程如图4所示，包含两个串行的核心模块：

**模块一：对比度轨迹对选择（Pairwise Trajectory Sampling, PTS）**
1. 对每个查询采样 $2N$ 条轨迹（而非标准 GRPO 的 $N$ 条），计算每条轨迹的优势值 $\hat{A}_i$。
2. 将 $2N$ 条轨迹按优势值降序排列，采用 **max-min 配对原则**：将最高优势轨迹与最低优势轨迹配对，次高与次低配对，依此类推，构建 $N$ 个高对比度轨迹对。
3. 仅保留前 $M = \alpha N$ 对（$\alpha \in (0,1)$）用于后续梯度更新，过滤掉优势差距小的低信号对。

**模块二：基于优势的批次重组（Advantage-based Batch Shuffle, ABS）**
1. 对 PTS 选出的轨迹对计算重要性权重 $W(p_j) = |\hat{A}_{j,1}| + |\hat{A}_{j,2}|$，即两条轨迹绝对优势之和。
2. 根据权重构建批次内的加权采样分布 $\Phi(p_j)$，进行 $S$ 轮加权子采样重组批次，使高价值样本获得更高的曝光频率。
3. 重组后的批次大小与原始批次保持一致，确保计算开销可控。

### 输入输出流

**输入**：查询 $q$ 和当前策略模型 $\pi_{\theta'}$。

**输出**：经过 PTS 筛选和 ABS 重组后的轨迹对批次，用于策略梯度更新。

**数据流**：
1. 策略模型对每个查询生成 $2N$ 条响应轨迹。
2. 奖励函数计算每条轨迹的标量奖励 $r_i$，经批次内均值-标准差归一化得到优势值 $\hat{A}_i$。
3. PTS 模块对优势值排序、配对、筛选，输出 $M$ 个有效轨迹对。
4. ABS 模块计算轨迹对权重，执行 $S$ 轮加权子采样，输出最终的重组批次。
5. 重组批次送入策略梯度优化器，使用带裁剪的 PPO 目标函数更新模型参数。

### 关键设计决策

- **采样比例 $\alpha = 0.5$**：在信号质量与计算效率间取得平衡。过低的 $\alpha$（如 0.25）丢弃过多样本，性能不足；过高的 $\alpha$（如 0.75）可能引入噪声轨迹。
- **Shuffle 次数 $S = 8$**：适度重复训练高质量样本有益于强化关键梯度信号，但 $S=16$ 时性能开始下降，表明过度重复会损害批次多样性。
- **双向对比配对**：max-min 配对策略显著优于仅选择最高优势（+max）、仅选择最低优势（+min）或随机选择策略（表5），证明构建高对比度轨迹对是缓解优势值坍塌的关键机制。

### 与基线的本质区别

与 GRPO 等静态采样方法相比，Shuffle-R1 的核心差异不在于优化目标函数，而在于**梯度信号的来源控制**：PTS 通过对比度筛选决定哪些轨迹参与更新，ABS 通过自适应批次重组决定各轨迹的曝光频率。这种数据中心的视角使得 Shuffle-R1 能够在不改变基础 RL 算法（如 PPO 裁剪目标）的前提下，显著提升训练效率和最终性能——在 Geometry3K 上仅需 GRPO 约 60% 的 wall-clock GPU 时间即可达到同等精度。



### 基础RL目标

Shuffle-R1建立在标准的带裁剪策略梯度目标之上。给定查询 $q$，从旧策略 $\pi_{\theta'}$ 采样 $N$ 条轨迹 $\{o_i\}_{i=1}^N$，优化目标为：

$$
\mathcal{I}(\theta) = \mathbb{E}_{q \sim \mathcal{D}, \{o_i\}_{i=1}^N \sim \pi_{\theta'}(\cdot|q)} \frac{1}{\sum_{i=1}^N |o_i|} \sum_{i=1}^N \sum_{t=1}^{|o_i|} \left\{ \min\left[ \gamma_t(\theta) \hat{A}_i, \operatorname{clip}\left( \gamma_t(\theta), 1-\epsilon, 1+\epsilon \right) \hat{A}_i \right] \right\}
$$

其中概率比 $\gamma_t(\theta)$ 和全局归一化优势 $\hat{A}_i$ 定义为：

$$
\gamma_t(\theta) = \frac{\pi_{\theta}(o_{i,t} | q, o_{i,<t})}{\pi_{\theta'}(o_{i,t} | q, o_{i,<t})}, \qquad \hat{A}_i = \frac{r_i - \mathrm{mean}(R)}{\mathrm{std}(R)}
$$

$\epsilon$ 为裁剪超参数，防止训练崩溃。该目标（Equation 1-2）构成后续所有改进的基准。

### 模块一：对比度轨迹对选择（PTS）

PTS旨在缓解**优势值坍塌**（Advantage Collapsing）——即大多数轨迹的优势集中在零附近，导致梯度信号微弱。其核心机制是通过构建高对比度轨迹对，放大有效学习信号。

**采样与配对流程**：

1. **扩展采样**：对每个查询采样 $2N$ 条轨迹（而非标准GRPO的 $N$ 条），计算优势后将它们降序排列：

   $$
   A_s = \{ \hat{A}_{(i)} \}_{i=1}^{2N}, \quad \text{where } \hat{A}_{(1)} \geq \hat{A}_{(2)} \geq \cdots \geq \hat{A}_{(2N)}
   $$

2. **Max-min配对**：将最高优势轨迹与最低优势轨迹配对，次高与次低配对，以此类推，构建 $N$ 个对比度轨迹对：

   $$
   P = \{ (o_{(i)}, o_{(2N-i+1)}) \}_{i=1}^N
   $$

   这种"最大-最小"配对原则确保每对内部存在较大的优势差距，从而产生更强的梯度对比信号。

3. **Top-k有效对选择**：仅保留前 $M$ 对（优势差距最大的对）参与梯度更新：

   $$
   P_v = \{ (o_{(i)}, o_{(2N-i+1)}) \}_{i=1}^M, \quad M = \alpha N, \quad \alpha \in (0, 1)
   $$

   其中 $\alpha$ 为采样保留比例。实验表明 $\alpha=0.5$ 取得最佳平衡——过低（0.25）性能不足，过高（0.75）可能引入噪声（Table 12）。

**关键设计动机**（Figure 3）：模型准确率随rollout数量增加而提升，且不同难度查询在训练中产生质量迥异的轨迹。PTS通过对比配对，将模型更新资源集中到信息量最大的轨迹对上。

### 模块二：基于优势的批次重组（ABS）

ABS旨在缓解**有效轨迹沉默**（Rollout Silencing）——即产生非零梯度的轨迹比例随训练持续下降，大量计算被浪费。ABS通过对PTS筛选出的轨迹对进行自适应加权重组，使高价值样本获得更高曝光率。

**重组流程**：

1. **重要性权重计算**：对每个轨迹对 $p_j$，计算其绝对优势之和作为重要性权重：

   $$
   W(p_j) = |\hat{A}_{j,1}| + |\hat{A}_{j,2}|
   $$

   该权重反映轨迹对提供梯度信号的强度——优势绝对值越大，梯度信息越丰富。

2. **归一化采样分布**：在批次内将权重归一化为采样概率：

   $$
   \Phi(p_j) = \frac{W(p_j)}{\sum_{k=1}^{|B|} W(p_k)}
   $$

3. **多轮加权子采样**：从原始批次中按 $\Phi$ 进行加权采样，形成子批次，重复 $S$ 次Shuffle后拼接为与原批次等大的重组批次。具体地，设子批次大小为 $T$，则 $S \times T = M \times G$（$G$ 为梯度累积步数），确保总样本量不变。

**与优先经验回放的区别**（Figure 9）：ABS是在线进行的，每次只对当前批次的轨迹对进行加权重组，避免了优先经验回放因重复训练历史高优先级样本而导致的过拟合问题。实验显示，直接应用优先经验回放在训练后期性能下降，而ABS持续保持优势。

### 两模块的协同

PTS和ABS形成级联管道（Figure 4）：PTS首先从扩展的rollout池中筛选出高对比度轨迹对，过滤低信号样本；ABS随后对筛选后的轨迹对进行自适应批次重组，优化计算资源分配。消融实验（Table 4）证实：PTS单独使用将Geo3K准确率从42.64%提升至46.21%（+3.57），联合ABS进一步提升至47.88%（额外+1.67），验证了两模块的互补性。



## 实验与关键发现

### 核心发现：两大训练瓶颈

Shuffle-R1 的出发点是对当前 MLLM 强化学习训练中两个被忽视的瓶颈进行系统诊断。如 **Figure 1** 所示，GRPO 等基线方法在训练过程中暴露出两个根本性问题：

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_mYP33u1QBK/figures/001_Figure_1.jpg]]
*Figure 1: (a) Advantage Collapsing, where most advantages concentrate near zero. (b) Rollout Silencing, where the ratio of rollouts with nonzero gradient consistently drops*

**优势值坍塌（Advantage Collapsing）**：绝大多数轨迹的优势值集中在零附近，导致梯度信号微弱，模型难以从大量样本中获取有效的学习方向。这意味着即使生成了大量轨迹，真正能驱动模型更新的信息量极为有限。

**有效轨迹沉默（Rollout Silencing）**：随着训练进行，能够产生非零梯度的轨迹比例持续下降。大量计算资源被浪费在无法贡献学习信号的轨迹上，训练效率呈递减趋势。

这两个问题共同指向一个核心症结：静态均匀采样范式无法区分学习信号的质量，优质梯度信号被低质量样本淹没。

### 主实验结果

#### Geometry3K 基准

**Table 1** 报告了在 Geometry3K 数据集上的主实验结果。在 Qwen2.5-VL-3B 基座模型上，Shuffle-R1 达到 **47.88%** 准确率，相比 GRPO（42.64%）提升 **+5.24 个百分点**，相比 DAPO（45.14%）提升 +2.74，相比 GSPO（43.16%）提升 +4.72。在 Qwen2.5-VL-7B 上，Shuffle-R1 以 **55.89%** 领先 GRPO（52.60%）**+3.29 个百分点**，同时超越 DAPO（54.48%）和 GSPO（53.30%）。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_mYP33u1QBK/figures/005_Table_1.jpg]]
*Table 1: Performance of Shuffle-R1 trained on Geometry3K dataset*

值得注意的是，基座模型 Qwen2.5-VL-3B 在 Geometry3K 上的初始准确率仅为 25.79%，Shuffle-R1 实现了 +22.09 的绝对提升，充分体现了 RL 训练的有效性。

#### K12 数据集

**Table 2** 展示了在 K12 数据集上的训练结果，验证了方法的跨数据鲁棒性。Qwen2.5-VL-3B 基座准确率为 42.42%，Shuffle-R1 将其提升至 **62.22%**（+19.80）。Qwen2.5-VL-7B 从 51.13% 提升至 **68.78%**（+17.65）。在 Math Avg.、HallBench、ChartQA 等域外基准上，Shuffle-R1 同样保持一致的领先优势，表明方法学到的推理能力具有良好的泛化性。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_mYP33u1QBK/figures/006_Table_2.jpg]]
*Table 2: Performance of Shuffle-R1 trained on K12 dataset*

#### 多基准综合评估

**Table 3** 在六个代表性视觉推理基准（MathVerse、MathVision、MathVista、WeMath、HallBench、ChartQA）上进行了全面对比。Shuffle-R1-Qwen-7B 以 **64.7** 的总平均准确率显著超越 Qwen2.5-VL-7B 基座（57.4，+7.3），并且超过了 GPT-4o（63.1）和 Claude-3.7（63.3）。在与 Vision-R1-7B（使用冷启动+RL）、R1-VL-7B（零样本RL）等同类 RL 训练模型的对比中，Shuffle-R1 同样表现最优。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_mYP33u1QBK/figures/007_Table_3.jpg]]
*Table 3: Model performance on representative visual reasoning benchmarks. Models marked with ∗ are evaluated using our own evaluation scripts with vLLM. †Vision-R1-7B used WeMath and MathVision as training data, its performance on these benchmarks are omitted. Best performance of RL-only models marked with Bold, second best with underline*

#### 30K 大规模联合训练

**Table 10** 展示了在 30K 样本（Geometry3K + K12 + MM-Eureka 联合）上的扩展实验。Shuffle-R1-Qwen-7B 在六个基准上的总平均准确率达到 **64.7**，相比 GRPO（61.5）提升 +3.2，相比 DAPO（63.0）提升 +1.7，相比 GSPO（61.6）提升 +3.1。这一结果证明方法在大规模数据场景下依然有效。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_mYP33u1QBK/figures/021_Table_10.jpg]]
*Table 10: Full 30k experiment on Qwen2.5-VL-7B. Highest accuracy marked in Bold*

### 训练效率分析

Shuffle-R1 不仅在最终性能上领先，在训练效率方面同样展现出显著优势。

**Figure 6(a-b)** 显示，Shuffle-R1 在训练和验证准确率上始终高于 GRPO，且在大约一半的训练步数时即可达到 GRPO 完整训练的最终性能。**Figure 7** 的 wall-clock 训练曲线进一步证实：Shuffle-R1 在训练早期阶段大幅领先 GRPO，达到相同准确率仅需 GRPO 约 **60% 的总 GPU 时间**，节省约 40% 的计算开销。

**Figure 6(c)** 展示了 token 利用率指标，Shuffle-R1 在所有训练阶段均维持较高的 token 利用率，而 GRPO 的利用率随训练进行持续衰减——这直接印证了有效轨迹沉默问题的缓解效果。

**Figure 6(d)** 量化了额外时间开销：Shuffle-R1 的总 GPU 时间相比 GRPO 仅增加 **4% ~ 7.7%**，换来的却是显著的性能提升和更快的收敛速度。

### 消融实验

#### PTS 与 ABS 的独立贡献

**Table 4** 分别验证了两个核心模块的有效性。在 Geometry3K 上，仅添加 PTS 将准确率从 GRPO 基线的 42.64% 提升至 **46.21%**（+3.57）；进一步叠加 ABS 后达到 **47.88%**（额外 +1.67）。这证明 PTS 通过缓解优势值坍塌提供了主要增益，而 ABS 在此基础上通过优化批次组成进一步释放潜力。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_mYP33u1QBK/figures/014_Table_4.jpg]]
*Table 4: Ablation on effectiveness of PTS and ABS*

#### 对比配对策略的关键性

**Table 5** 对比了 PTS 的 max-min 配对策略与其他采样方式的差异。仅选择最高优势轨迹（+max）、仅选择最低优势轨迹（+min）或随机选择，性能均显著低于双向 max-min 对比采样。这一结果验证了高对比度轨迹对设计的必要性——正负样本的梯度对比是放大有效学习信号的核心机制。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_mYP33u1QBK/figures/015_Table_5.jpg]]
*Table 5: Ablation on rationality of PTS and ABS*

#### 关键超参数分析

**Figure 8** 和 **Table 12** 系统探索了采样比例 α 和 Shuffle 次数 S 的影响：

- **采样比例 α**：α=0.5 取得最佳平衡。α=0.25 时保留轨迹过少，信息量不足；α=0.75 时可能引入低质量轨迹的噪声，性能反而下降。
- **Shuffle 次数 S**：S=8 最优。S=4 时高价值样本曝光不足；S=16 时性能开始下降，表明过度重复训练高质量样本会损害批次多样性，导致过拟合。

#### 与优先经验回放（PER）的对比

**Figure 9** 将 ABS 与传统的优先经验回放进行了对比。PER 在训练初期有一定效果，但后期性能明显落后于 ABS。原因在于 PER 基于历史经验进行采样，容易过拟合早期的高奖励样本；而 ABS 的在线自适应重组机制能够持续适应模型能力的变化，更有效地缓解有效轨迹沉默。

### 扩展实验

#### 模型规模扩展

**Table 6** 将方法扩展到 Qwen2.5-VL-32B 巨型模型。Shuffle-R1-32B 在六个基准上的总平均准确率达到 **69.1**，证明了方法对大规模模型的有效性。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_mYP33u1QBK/figures/017_Table_6.jpg]]
*Table 6: Extension experiments on Qwen2.5-VL-32B*

#### 任务类型扩展

**Table 7** 展示了在 Referring Expression Comprehension（REC）任务上的迁移效果。在 RefCOCOg 测试集上，Shuffle-R1 达到 **86.07** 准确率，验证了方法在非数学推理任务上的适用性。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_mYP33u1QBK/figures/018_Table_7.jpg]]
*Table 7: Extension experiments on Referring Expression Comprehension task*

**Table 8** 将方法应用于纯文本 LLM（Qwen2.5-Math-1.5B）。在 MATH500 基准上，Shuffle-R1 达到 **71.0** 准确率，相比 GRPO 提升显著。这表明 PTS 和 ABS 的数据中心设计理念具有跨模态的通用性。

#### 与更多 RL 算法的兼容性

**Table 11** 展示了 Shuffle-R1 与 RLOO 和 REINFORCE++ 的结合效果。在 Geometry3K 上，Shuffle-R1 框架叠加这些算法后均取得一致的性能提升，证明该方法作为通用训练框架的灵活性。

### 理论支撑

Shuffle-R1 的实验效果得到了严格的理论分析支持。三个命题（详见原文 Proposition 1-3）分别证明：

1. **优势期望放大**：动态采样提高了批次内优势值的期望，使梯度更新方向更加明确。
2. **梯度范数放大**：高对比度轨迹对增加了梯度的范数，加速参数更新。
3. **正偏差引入**：自适应采样引入了有界的正偏差，有助于模型更快地偏向高奖励行为。

这些理论结果与 **Figure 5** 的优势分布可视化相互印证：PTS 使大批次中大幅值优势的比例显著增加，直接验证了优势值坍塌的缓解效果。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_mYP33u1QBK/figures/008_Figure_5.jpg]]
*Figure 5: Advantage distribution in a training batch of GRPO and our framework*

### 公平性说明

所有实验在以下方面保证了对比的公平性：
- 使用相同的训练数据、基座模型（Qwen2.5-VL-3B/7B/32B）和 EasyR1 框架
- 超参数（学习率 1e-6、温度 1.0 训练/0.5 评估、全局批大小 128、rollout 批大小 512）保持一致
- 评估使用相同的外部评估器 Gemini-2.0-Flash-001，报告 8 次运行的 pass@1 平均准确率
- 扩展实验（32B、REC、纯文本 LLM）均采用与主实验相同的设置



## 定位与知识库关联

### 核心贡献与差异化定位

Shuffle-R1 的核心贡献在于将“数据中心动态优先级采样”引入 MLLM 的强化学习训练流程。不同于现有方法在固定采样范式下优化损失函数或奖励设计，Shuffle-R1 通过两个互补的模块——**对比度轨迹对选择（PTS）** 和 **基于优势的批次重组（ABS）**——直接控制梯度更新的来源和质量。这一设计源于对 RL 训练中两个被忽视现象的观察：**优势值坍塌**（大多数优势集中在零附近，优质梯度信号被淹没）和 **有效轨迹沉默**（产生有效梯度的轨迹比例随训练进行而持续下降）。

### 与现有 RL 训练范式的关系

**静态采样范式（GRPO 等）**：GRPO（Shao et al., 2024）采用均匀采样策略，对每条轨迹赋予相同的更新权重。Shuffle-R1 的实验表明，这种“一刀切”的方式导致大量低质量轨迹稀释了关键梯度信号。在 Geometry3K 数据集上，Shuffle-R1 仅需约 GRPO 一半的训练步数即可达到同等精度，实际 GPU 时间节省约 40%（Fig.7）。

**基于规则的预过滤范式**：部分工作尝试在训练前通过规则筛选高质量样本，但这类方法无法适应训练过程中模型能力的动态变化。Shuffle-R1 的 PTS 模块在每个训练步在线构建高对比度轨迹对，使采样策略随模型状态自适应调整。

**序列级重要性采样方法**：DAPO（Yu et al., 2025）和 GSPO（Zheng et al., 2025）等改进算法在损失函数层面引入了重要性权重或序列级优化。Shuffle-R1 与这些方法正交——它不修改损失函数形式，而是改变哪些样本参与更新。在 Geometry3K 和 K12 数据集上，Shuffle-R1 均显著优于 DAPO 和 GSPO（Table 1, Table 2），表明数据层面的优化与算法改进可以互补。

**优先经验回放（PER）**：ABS 模块与离线 PER 有相似之处，但关键区别在于 ABS 是在线进行的——每轮对当前批次内轨迹对进行加权子采样，而非维护历史经验池。实验表明，直接应用 PER 会在训练后期导致过拟合历史样本，而在线 ABS 有效避免了这一问题（Fig.9）。

### 方法谱系中的位置

Shuffle-R1 可被定位为 **数据驱动 RL 训练效率优化** 这一新兴方向的开创性工作。其方法论贡献体现在三个层面：

1. **问题定义层面**：首次系统性地识别并量化了 MLLM 的 RL 训练中“优势值坍塌”和“有效轨迹沉默”两个瓶颈，为后续研究提供了明确的优化目标。

2. **机制设计层面**：提出的 max-min 对比配对策略（PTS）和基于绝对优势的批次重组（ABS）构成了一个通用的数据采样框架。理论分析（Proposition 1-3）证明该框架能够放大梯度的期望和范数，并引入正偏差以加速训练。

3. **可扩展性层面**：该方法展现出良好的跨任务、跨模型和跨模态泛化能力——在 Qwen2.5-VL-32B 巨型模型、Referring Expression Comprehension 任务以及纯文本 LLM（Qwen2.5-Math-1.5B）上均取得一致提升（Table 6-8）。

### 适用边界与局限性

尽管 Shuffle-R1 在多个基准上展现出显著优势，其适用边界仍需审慎界定：

1. **超参数敏感性**：PTS 的采样比例 α 和 ABS 的 Shuffle 次数 S 对性能有显著影响。消融实验表明，α=0.5 和 S=8 在 Geometry3K 上取得最优平衡，但过低（α=0.25）会导致信号不足，过高（α=0.75, S=16）可能引入噪声或损害多样性（Table 12, Fig.8）。这意味着在不同任务和模型规模上可能需要手动调优。

2. **任务覆盖范围有限**：当前实验主要集中在视觉推理任务（数学推理、图表理解）上。在视频理解、复杂视觉问答等更广泛的多模态任务上的有效性尚待验证。此外，大规模数据集（如 30k 联合训练）上的实验仅覆盖 7B 模型规模。

3. **长期训练稳定性未充分探索**：动态采样策略引入的正偏差（Proposition 3）在短期加速训练，但长期训练是否会导致模型过度乐观或探索不足仍需深入研究。当前实验的训练步数相对有限，未观察到明显的性能退化，但更大规模、更长周期的训练可能暴露潜在问题。

4. **对奖励函数设计的依赖**：PTS 和 ABS 的有效性依赖于优势估计的质量，而优势估计又取决于奖励函数的设计。当前实验采用简单的格式奖励（权重 0.1）和准确率奖励（权重 0.9）的加权组合。在更复杂的奖励结构（如过程奖励、细粒度奖励）下，对比度采样的有效性需要进一步验证。

### 开放问题与未来方向

1. **自适应超参数调整**：能否设计一种机制，使 α 和 S 随训练进度自动调整？例如，在训练初期使用较大的 α 以加速探索，后期减小 α 以聚焦高质量样本。

2. **与算法改进的深度融合**：Shuffle-R1 的数据采样策略与 DAPO、GSPO 等算法改进是正交的。将二者结合能否产生叠加增益？这需要系统的实验验证。

3. **推广到更广泛的 RL 方法**：PTS 和 ABS 的设计基于 GRPO 的群体归一化优势框架。能否将其思想适配到 PPO、TRPO 等更一般的策略梯度方法，或扩展到离线 RL 场景？

4. **与模型架构改进的协同**：本方法的数据中心理念与记忆增强、世界模型等架构改进方向是否存在协同效应？将动态优先级采样与结构化推理能力相结合，可能进一步推动多模态推理的边界。

5. **理论收敛性分析**：Proposition 3 揭示了动态采样引入正偏差，但该偏差对策略梯度收敛性的长期影响尚未给出严格的收敛性保证。建立完整的理论分析框架将是重要的后续工作。



## 原文 PDF

![[paperPDFs/ICLR_2026/Shuffle_R1_Efficient_RL_framework_for_Multimodal_Large_Language_Models_via_Data_centric_Dynamic_Shuffle.pdf]]
