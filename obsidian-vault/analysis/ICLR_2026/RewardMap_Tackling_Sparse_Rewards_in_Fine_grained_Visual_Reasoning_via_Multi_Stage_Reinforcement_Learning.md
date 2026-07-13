---
title: "RewardMap: Tackling Sparse Rewards in Fine-grained Visual Reasoning via Multi-Stage Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RewardMap_Tackling_Sparse_Rewards_in_Fine_grained_Visual_Reasoning_via_Multi_Stage_Reinforcement_Learning.pdf
project_link: https://fscdc.github.io/RewardMap
code_link: null
openreview_forum_id: iRVbPxHNrX
aliases:
- RewardMap
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入包含详细信息（部分正确性）的奖励项，并依据地图难度和问题难度对奖励进行加权，配合从简单感知任务到复杂推理任务的多阶段课程训练，直接改变了训练过程中的奖励密度和优化路径。"
primary_logic: "通过构建易于产生密集奖励的冷启动数据集 REASONMAP-PLUS，并设计融合格式、正确性与细节奖励的困难感知加权函数，再以多阶段课程调度训练数据，可以在统一的强化学习框架内平滑地从视觉理解过渡到视觉推理，有效克服稀疏奖励瓶颈，稳定训练并提升 MLLMs 的细粒度视觉推理性能。"
claims:
- "REWARDMAP 在 REASONMAP 和 REASONMAP-PLUS 上显著优于所有 RL 和 SFT→RL 基线。"
- "消融实验证明难度感知奖励设计与多阶段课程设计各自有效，且组合使用效果最佳。"
- "REWARDMAP 在 SpatialEval 的 mazenav 子任务上将准确率从 19.60% 提升至 57.20%，展示了强大的空间推理迁移能力。"
- "训练奖励曲线显示 REWARDMAP 提供了比标准 RL 基线更密集且持续上升的奖励信号，缓解了奖励稀疏问题。"
---

# RewardMap: Tackling Sparse Rewards in Fine-grained Visual Reasoning via Multi-Stage Reinforcement Learning

> [!tip] 核心洞察
> 通过构建易于产生密集奖励的冷启动数据集 REASONMAP-PLUS，并设计融合格式、正确性与细节奖励的困难感知加权函数，再以多阶段课程调度训练数据，可以在统一的强化学习框架内平滑地从视觉理解过渡到视觉推理，有效克服稀疏奖励瓶颈，稳定训练并提升 MLLMs 的细粒度视觉推理性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RewardMap：通过多阶段强化学习解决细粒度视觉推理中的稀疏奖励问题 |
| 英文题名 | RewardMap: Tackling Sparse Rewards in Fine-grained Visual Reasoning via Multi-Stage Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=iRVbPxHNrX) · [Project](https://fscdc.github.io/RewardMap) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | REWARDMAP |
| Dataset | REASONMAP (Short/Long), REASONMAP Overall (Short/Long), REASONMAP-PLUS (Weighted Acc.), 6-Average (Spatial/Fine-Grained/General) |

> [!tip] 效果简介
> - REASONMAP (Short/Long) 上，Weighted Accuracy 为 31.51% / 31.77%，对比 26.22% / 26.04% (RL baseline, Qwen2.5-VL-7B)，变化 +5.29% / +5.73%。
> - REASONMAP Overall (Short/Long) 上，Weighted Map Score 为 6.21 / 11.22，对比 5.52 / 9.52 (RL baseline, Qwen2.5-VL-7B)，变化 +0.69 / +1.70。
> - REASONMAP-PLUS (Weighted Acc.) 上，Weighted Accuracy 为 74.25%，对比 44.64% (RL baseline on R_train)，变化 +29.61%。

## 概要

### 问题：细粒度视觉推理中的稀疏奖励瓶颈

多模态大语言模型（MLLMs）在交通地图路线规划等细粒度视觉推理任务上面临一个关键瓶颈：标准强化学习（RL）通常仅依据最终答案的正确性提供二值的、稀疏的奖励信号。这种稀疏奖励导致策略优化时梯度方差高、收敛缓慢，MLLMs 难以通过 RL 有效习得长链推理能力。

### 核心方法：REWARDMAP

REWARDMAP 是一个多阶段强化学习框架，通过两个核心设计直接改变训练过程中的奖励密度和优化路径：

1. **困难感知奖励设计**：在基础的格式奖励（$R_{\text{format}}$）和正确性奖励（$R_{\text{correctness}}$）之外，引入细节奖励（$R_{\text{detail}}$）以提供部分正确性的密集反馈，并根据地图难度（$W_{\text{map}}$）和问题换乘次数（$W_{\text{question}}$）对奖励进行加权，形成 $R = W_{\text{difficulty}} (R_{\text{format}} + R_{\text{correctness}} + \alpha \times R_{\text{detail}})$ 的奖励函数。

2. **多阶段课程训练**：构建易于产生密集奖励的冷启动数据集 REASONMAP-PLUS，并按从简单感知任务（二值判断、计数）到复杂推理任务（路线规划）的顺序分阶段调度训练数据，在统一的 GRPO 强化学习框架内平滑过渡。

### 核心结论

- **主任务显著提升**：在 REASONMAP 基准上，REWARDMAP 将加权准确率从 RL 基线的 26.22%/26.04%（短/长问题）提升至 31.51%/31.77%，加权地图得分从 5.52/9.52 提升至 6.21/11.22（Table 1）。

- **密集奖励冷启动有效**：在 REASONMAP-PLUS 上，REWARDMAP 的加权准确率达 74.25%，远超 RL 基线的 44.64%（Table 1）；且纯 RL 冷启动（67.61%）优于 SFT→RL 流水线（60.53%），验证了无需依赖 SFT 即可有效冷启动（Table 4）。

- **泛化能力突出**：在 SpatialEval 的 mazenav 子任务上，REWARDMAP 将准确率从 19.60% 提升至 57.20%，展示了强大的空间推理迁移能力；在 6 个基准上的平均得分提升 3.47%（Table 2）。

- **方法组合有效且可泛化**：消融实验证实困难感知奖励与多阶段课程各自有效，组合使用效果最佳（Table 3）；方法在 Qwen2.5-VL-3B/7B 和 Kimi-VL 等多种模型规模与架构上均带来一致提升（Table 8–9）。

### 方法谱系与知识库定位

REWARDMAP 定位于 RL 微调 MLLMs 的方法族，其基线包括标准 GRPO（Shao et al., 2024）、REINFORCE++（Hu et al., 2025a）和 ReMax（Li et al., 2023）等 RL 算法，以及 SFT 和 SFT→RL 两阶段流程。与这些基线相比，REWARDMAP 的核心差异在于：

- **奖励函数**：从仅包含格式和正确性的稀疏奖励，变为融合细节奖励与困难感知加权的稠密奖励。
- **训练课程**：从单阶段随机混合数据，变为按任务类型和目标从感知到推理的多阶段调度。
- **冷启动策略**：从依赖 SFT 冷启动，变为利用 REASONMAP-PLUS 的密集奖励直接进行 RL 冷启动。

### 局限与开放问题

当前工作在交通地图领域得到充分验证，并在 ChartQA、Charxiv 等数据集上展示了初步扩展性，但尚未在大规模多样化结构化视觉推理基准上进行系统评估。多阶段训练和困难感知奖励设计引入了额外超参数（$\gamma$、$\beta$、$\alpha$），增加了调参成本。未来方向包括开发领域无关的细节奖励机制，以及将 REWARDMAP 与安全对齐技术结合，在提升推理能力的同时保证输出的可靠性与无害性。



### 细粒度视觉推理的挑战

多模态大语言模型（MLLMs）在通用视觉理解任务上已取得显著进展，但在需要精确定位、空间关系推理和多步逻辑推导的**细粒度视觉推理**任务上仍面临严峻挑战。以交通地图路线规划为典型场景：模型必须准确识别地图中的站点位置、线路连接关系，并在此基础上进行路径搜索与换乘规划。这类任务要求模型同时具备细粒度的视觉感知能力和结构化的逻辑推理能力，二者缺一不可。

### 强化学习中的稀疏奖励瓶颈

将强化学习（RL）应用于 MLLMs 的视觉推理训练时，一个核心瓶颈浮现：**奖励稀疏性**。标准 RL 训练流程通常仅在模型输出最终答案后给予二值奖励——正确则奖励 1，错误则奖励 0。在复杂的多步推理场景中，这种稀疏奖励导致策略梯度优化面临严重困难：当大多数采样轨迹的奖励为零时，GRPO 中的中心化优势函数 $\hat{A}_i$ 要么趋近于零（全部失败），要么极度偏斜（稀少的成功样本主导梯度），产生低信号或高方差的梯度，严重拖慢收敛速度。

### 现有方法的不足

针对上述瓶颈，现有工作主要存在以下局限：

- **奖励设计粗糙**：标准 RL 基线（如 GRPO、REINFORCE++、ReMax）仅使用格式奖励 $R_{\mathrm{format}}$ 和正确性奖励 $R_{\mathrm{correctness}}$，完全忽略了推理过程中的部分正确性信息。模型在接近正确答案但存在细节偏差时，无法获得任何正向反馈。
- **训练策略单一**：常见的 SFT→RL 两阶段流程依赖有监督微调进行冷启动，但 SFT 阶段本身不产生稠密奖励信号，且 RL 阶段仍使用稀疏奖励，冷启动效果有限。
- **缺乏难度感知**：训练数据通常随机混合，未考虑地图复杂度、问题换乘次数等难度因素，导致模型在简单任务上过度训练，而在困难任务上优化不足。

### 本文动机

为了系统性地解决上述问题，本文提出 **REWARDMAP** 框架。核心动机在于：**通过构建易于产生密集奖励的冷启动数据集，设计融合格式、正确性与细节奖励的困难感知加权函数，并配合多阶段课程调度训练数据，在统一的强化学习框架内平滑地从视觉理解过渡到视觉推理**。具体而言，REWARDMAP 包含两个关键创新：

1. **困难感知奖励设计**：在基本格式和正确性奖励之外，引入 $R_{\mathrm{detail}}$（部分正确的细节奖励），并根据地图难度 $W_{\mathrm{map}}$ 与问题换乘次数 $W_{\mathrm{question}}$ 对总奖励进行加权，使模型在困难任务上获得更强的优化信号。
2. **多阶段 RL 课程**：构建 REASONMAP-PLUS 数据集，按任务类型（二值判断 → 计数 → 规划）和目标（视觉理解 → 视觉推理）组织从易到难的训练课程，使模型逐步习得复杂推理能力。



## 核心方法与创新机理

REWARDMAP 针对细粒度视觉推理中标准强化学习的稀疏奖励瓶颈，提出了两个相互协同的**changed slots**，从根本上改变了策略优化的奖励密度与训练路径。

### 1. 困难感知的稠密奖励函数

标准 GRPO 基线仅使用二值的格式奖励与正确性奖励（$R_{\text{format}} + R_{\text{correctness}}$），导致大多数采样轨迹的奖励近似为零，优势函数 $\hat{A}_i$ 趋向于零或高度偏斜，产生低信号或高方差的梯度，收敛缓慢（Section 4.1）。

REWARDMAP 将奖励函数重构为：

$$R = W_{\text{difficulty}} \left( R_{\text{format}} + R_{\text{correctness}} + \alpha \times R_{\text{detail}} \right)$$

其中两个关键改动直接改变了优化信号的质量：

- **细节奖励 $R_{\text{detail}}$**：对答案中的部分正确项给予部分分数，打破了“全对或全错”的二值反馈，在模型产生部分正确推理时仍能获得正向梯度信号（Section 4.2）。
- **困难感知权重 $W_{\text{difficulty}} = W_{\text{map}} + W_{\text{question}}$**：$W_{\text{map}}$ 根据地图难度（简单/中等/困难）取离散值 $\gamma_e, \gamma_m, \gamma_h$；$W_{\text{question}}$ 根据规划问题是否需要换乘（换乘次数 ≥ 1）赋予 $\beta_1$ 或 $\beta_0$。该机制使困难样本的奖励幅度更大，引导策略在复杂场景中投入更多优化资源（Section 4.2, Algorithm 1）。

消融实验证实，仅添加困难感知奖励设计（无多阶段课程）即可在 REASONMAP 上将加权准确率提升约 2.86%/3.91%（短/长问题）（Table 3）。训练奖励曲线（Figure 4）显示，REWARDMAP 提供了比标准 RL 基线更密集且持续上升的奖励信号，直接验证了稀疏奖励问题的缓解。

### 2. 多阶段课程调度

标准 RL 训练采用单阶段随机混合数据，模型在训练初期即面对高难度推理任务，优化困难。REWARDMAP 引入多阶段课程调度器，遵循两个互补原则（Section 4.3）：

- **全局课程原则**：按任务类型（二值判断 → 计数 → 规划）和目标层次（视觉理解 → 视觉推理）将训练划分为不同阶段，实现从感知到推理的平滑过渡。
- **局部随机性原则**：每个阶段内对样本进行随机打乱，避免严格的确定性排序导致的过拟合。

与粗粒度的多阶段设计相比，REWARDMAP 的细粒度课程在 REASONMAP-PLUS 上带来额外提升（加权准确率 74.25% vs. 70.30%，Table 5），表明精细的阶段划分对性能至关重要。

### 3. 纯 RL 冷启动策略

传统流程依赖 SFT→RL 两阶段训练进行冷启动。REWARDMAP 利用 REASONMAP-PLUS（RPlus_train，2570 样本）中天然存在的密集奖励问题，直接进行 RL 冷启动，无需 SFT 阶段。消融实验显示，纯 RL 冷启动（67.61%）优于 SFT→RL 流水线（60.53%），验证了该策略的有效性（Table 4）。

### 协同效应

奖励设计与多阶段课程并非孤立改进。消融实验（Table 3）表明，单独启用任一组件均带来性能增益，但组合使用时效果最优——REASONMAP 加权准确率从基线 RL 的 26.22%/26.04%（短/长）提升至 REWARDMAP 的 31.51%/31.77%。奖励设计提供了稠密的优化信号，多阶段课程则确保模型在适当难度下逐步吸收这些信号，二者形成互补。

### 方法泛化性

REWARDMAP 在 Qwen2.5-VL-3B/7B 和 Kimi-VL 等不同模型规模与架构上均带来一致提升（Table 8–9），表明困难感知奖励与多阶段课程的设计不依赖于特定模型结构，具有较好的泛化能力。



![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_iRVbPxHNrX/figures/002_Figure_2.jpg]]
*Figure 2: Overview of REWARDMAP. The framework enhances fine-grained visual understanding and reasoning in MLLMs through reinforcement learning with Group Relative Policy Optimization (GRPO). It consists of two key components: (1) a difficulty-aware reward design (Section 4.2), which combines format, correctness, and detail rewards with difficulty-based weighting; and (2) a multi-stage RL curriculum (Section 4.3), which schedules training data from simple perception tasks to complex reasoning tasks, ensuring effective optimization tackling sparse rewards*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_iRVbPxHNrX/figures/001_Figure_1.jpg]]
*Figure 1: Overview of REASONMAP-PLUS. REASONMAP-PLUS comprises 4,018 questions from 5 extended question types and maps from 30 cities across 13 countries*

REWARDMAP 是一个面向多模态大语言模型（MLLMs）的多阶段强化学习框架，旨在解决细粒度视觉推理任务中因二值化最终答案反馈导致的奖励稀疏瓶颈。框架以**分组相对策略优化（GRPO）** 为底层优化引擎，在此基础上引入两个协同模块：**困难感知奖励设计**与**多阶段课程调度器**，从而在统一的 RL 训练流程内实现从视觉理解到视觉推理的平滑过渡。

### 输入输出流与模块关系

整个 pipeline 的输入为视觉问题样本（交通地图图像与对应问题），输出为模型生成的推理轨迹与最终答案。训练流程如下：

1. **冷启动阶段**：模型直接在 REASONMAP-PLUS 数据集上进行 RL 训练，该数据集专门构造了易于产生密集奖励的问题（如二值判断、计数），无需依赖传统的监督微调（SFT）冷启动。这一设计使得策略网络从一开始就能接收到有意义的梯度信号，规避了 SFT→RL 流水线中可能出现的灾难性遗忘或分布偏移。

2. **困难感知奖励模块**：对模型生成的每条轨迹，该模块计算三项奖励信号：
   - $R_{\mathrm{format}}$：格式奖励，约束输出结构的规范性；
   - $R_{\mathrm{correctness}}$：正确性奖励，判断最终答案是否完全正确；
   - $R_{\mathrm{detail}}$：细节奖励，根据部分正确的答案项给予部分分数，提供稠密的中间反馈。

   三项奖励以加权和形式组合，并乘以困难感知权重 $W_{\mathrm{difficulty}}$，形成最终奖励：
   $$R = W_{\mathrm{difficulty}} ( R_{\mathrm{format}} + R_{\mathrm{correctness}} + \alpha \times R_{\mathrm{detail}} )$$
   其中 $W_{\mathrm{difficulty}} = W_{\mathrm{map}} + W_{\mathrm{question}}$，$W_{\mathrm{map}}$ 依据地图难度（easy/medium/hard）取离散权重 $\gamma_e, \gamma_m, \gamma_h$，$W_{\mathrm{question}}$ 依据规划问题是否涉及换乘取 $\beta_0$ 或 $\beta_1$。这一设计使困难样本获得更高的奖励尺度，引导策略优先攻克高价值问题。

3. **多阶段课程调度器**：训练数据按全局课程原则分阶段组织——从简单感知任务（二值判断）到中等推理任务（计数），再到复杂规划任务（路径规划），对应从视觉理解到视觉推理的认知递进。每个阶段内部遵循局部随机性原则，对样本进行随机打乱而非严格按难度排序，避免确定性排序引入的过拟合偏差。

4. **GRPO 优化引擎**：在每个训练步中，对同一输入采样 $K$ 条轨迹，计算中心化优势函数 $\hat{A}_i = r_i - \frac{1}{K} \sum_{j=1}^{K} r_j$，并最大化策略梯度目标 $\max_{\theta} \mathcal{L}(\theta) = \sum_{i=1}^{K} \hat{A}_i \log \pi_{\theta}(y_i | x)$，推动模型向高奖励轨迹方向更新。

### 瓶颈突破机制

标准 GRPO 基线仅使用 $R_{\mathrm{format}} + R_{\mathrm{correctness}}$ 作为奖励，在复杂推理任务中绝大多数轨迹的 $r_i \approx 0$，导致优势函数 $\hat{A}_i$ 要么趋近于零（全错情况），要么高度偏斜（罕见正确情况），产生低信号或高方差的梯度，收敛缓慢。REWARDMAP 通过两条路径打破这一瓶颈：

- **奖励密集化**：$R_{\mathrm{detail}}$ 为部分正确的推理步骤提供非零反馈，使策略在完全正确之前就能获得方向性信号；
- **课程引导**：从易到难的数据调度确保训练初期策略能频繁获得正向奖励，建立稳定的优化基础，再逐步过渡到稀疏奖励的困难任务。

训练奖励曲线（Figure 4）直接验证了这一机制：REWARDMAP 的奖励轨迹（黄色曲线）不仅整体高于基线 RL（蓝色曲线），且呈现持续上升趋势，而基线奖励始终在低位波动，证实了奖励稀疏问题的有效缓解。



REWARDMAP 框架的核心由三个模块构成，协同解决细粒度视觉推理中的稀疏奖励瓶颈。

### 模块一：GRPO 优化引擎

REWARDMAP 采用**分组相对策略优化**（Group Relative Policy Optimization, GRPO）作为底层强化学习算法（Shao et al., 2024）。对于每个输入 $x$，模型采样 $K$ 条响应 $y_1, y_2, \dots, y_K$，每条响应获得标量奖励 $r_i$。GRPO 的核心在于使用组内中心化的优势函数替代传统的价值函数估计：

$$\hat{A}_i = r_i - \frac{1}{K} \sum_{j=1}^{K} r_j$$

$$\max_{\theta} \mathcal{L}(\theta) = \sum_{i=1}^{K} \hat{A}_i \log \pi_{\theta}(y_i | x)$$

其中 $\hat{A}_i$ 为第 $i$ 条响应的组内相对优势，$\pi_{\theta}$ 为策略模型。当奖励稀疏时（标准 RL 基线中多数 $r_i \approx 0$），优势函数 $\hat{A}_i$ 要么趋近于零（全部失败），要么高度偏斜（罕见正例），导致梯度信号弱或方差高，收敛缓慢。REWARDMAP 通过改进奖励函数和训练课程来改变这一局面。

### 模块二：困难感知奖励模块

该模块是解决稀疏奖励的核心。标准 RL 基线仅使用 $R_{\mathrm{format}} + R_{\mathrm{correctness}}$ 的二值奖励，而 REWARDMAP 引入了**细节奖励** $R_{\mathrm{detail}}$ 和**困难感知权重** $W_{\mathrm{difficulty}}$，构成稠密奖励函数：

$$R = W_{\mathrm{difficulty}} \left( R_{\mathrm{format}} + R_{\mathrm{correctness}} + \alpha \times R_{\mathrm{detail}} \right)$$

其中各奖励项的含义如下：
- **$R_{\mathrm{format}}$**：格式奖励，检查输出是否符合指定格式要求。
- **$R_{\mathrm{correctness}}$**：正确性奖励，判断最终答案是否完全正确。
- **$R_{\mathrm{detail}}$**：细节奖励，对答案中部分正确的条目给予部分分数，提供中间梯度信号。超参数 $\alpha$ 控制细节奖励的相对权重，消融实验表明 $\alpha = 0.5$ 时在 REASONMAP-PLUS 上获得最佳综合表现（Table 6）。

**困难感知权重** $W_{\mathrm{difficulty}}$ 由地图难度权重 $W_{\mathrm{map}}$ 和问题换乘权重 $W_{\mathrm{question}}$ 相加构成：

$$W_{\mathrm{difficulty}} = W_{\mathrm{map}} + W_{\mathrm{question}}$$

$$W_{\mathrm{map}} = \begin{cases} \gamma_e, & \text{map difficulty = easy} \\ \gamma_m, & \text{map difficulty = medium} \\ \gamma_h, & \text{map difficulty = hard} \end{cases}$$

$$W_{\mathrm{question}} = \begin{cases} \beta_0, & \text{transfer count = 0} \\ \beta_1, & \text{transfer count} \geq 1 \end{cases}$$

其中 $W_{\mathrm{map}}$ 根据地图的简单、中等、困难三个难度等级取离散权重 $\gamma_e, \gamma_m, \gamma_h$；$W_{\mathrm{question}}$ 根据规划问题是否需要换乘赋予不同权重 $\beta_0, \beta_1$。消融实验表明，适度的难度加权（如 $\gamma = (1.0, 1.2, 1.5)$ 或 $\beta = (0.0, 0.5)$）能有效提升性能，而权重趋于均匀时性能下降（Table 7）。

### 模块三：多阶段课程调度器

多阶段课程调度器控制训练数据的组织与投放顺序，使模型从简单感知任务平滑过渡到复杂推理任务。其设计遵循两个原则：

1. **全局课程原则**：按任务类型和目标难度进行粗到细的阶段划分。阶段顺序为：二值判断 → 计数 → 规划（按问题类型），同时从视觉理解逐步过渡到视觉推理（按目标任务）。这一全局排序确保模型先掌握基础感知能力，再学习复杂推理。

2. **局部随机性原则**：在每个阶段内部，避免严格的确定性排序，而是对训练样本进行随机打乱。这防止模型过拟合于特定的难度启发式指标，保持训练的泛化性。

消融实验证实了细粒度课程的必要性：粗粒度的多阶段设计（仅粗略划分阶段）在 REASONMAP-PLUS 上的加权准确率为 70.30%，而 REWARDMAP 的细粒度课程达到 74.25%（Table 5）。同时，仅添加困难感知奖励设计（无多阶段课程）即可在 REASONMAP 上将加权准确率提升约 2.86%/3.91%（短/长问题），而组合两个模块后达到最佳效果（Table 3），验证了两者的互补性。



## 实验与关键发现

### 瓶颈定位与评估基准

本工作聚焦于细粒度视觉推理中的核心瓶颈：标准强化学习（RL）仅依据最终答案提供二值、稀疏的奖励信号，导致策略优化时梯度方差高、收敛缓慢，多模态大模型（MLLMs）难以通过 RL 有效习得长链推理能力。为系统衡量这一瓶颈的缓解程度，实验在两个互补的基准上展开：

- **REASONMAP**：原始交通地图推理基准，包含短问题（S.）和长问题（L.）两个子集，训练集 R_train 仅 696 个样本，奖励信号天然稀疏。
- **REASONMAP-PLUS**：本研究扩展的数据集，包含 4,018 个问题，覆盖 5 种扩展题型和 13 个国家 30 个城市的地图，训练集 RPlus_train 含 2,570 个样本。其关键设计在于问题天然携带密集奖励信号（如部分正确的细节可得分），且难度从简单感知到复杂推理呈连续分布，为 RL 冷启动提供了理想条件。

此外，泛化能力在六个外部基准上评估，涵盖空间推理（SpatialEval）、细粒度视觉推理（ChartQA、Charxiv）和通用视觉任务（MME、MMBench、MMStar），以验证方法是否因过度适配交通地图域而损害通用能力。

### 主实验结果

**REASONMAP 与 REASONMAP-PLUS 上的核心收益。** 如表 1 所示，以 Qwen2.5-VL-7B-Instruct 为基座模型，REWARDMAP 在所有微调模型中取得最优结果。在 REASONMAP 上，加权准确率从 RL 基线的 26.22% / 26.04%（S./L.）提升至 31.51% / 31.77%，绝对增益分别为 +5.29% / +5.73%；加权地图得分从 5.52 / 9.52 提升至 6.21 / 11.22。在 REASONMAP-PLUS 上，加权准确率从 RL 基线的 44.64% 跃升至 74.25%，提升幅度达 +29.61%，验证了密集奖励冷启动与困难感知奖励设计的协同效应。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_iRVbPxHNrX/figures/003_Table_1.jpg]]
*Table 1: Evaluations of reference models and fine-tuned models on REASONMAP and REASONMAP-PLUS. “S.” represents results for short questions, while “L.” denotes results for long questions. Bold indicates the best results among fine-tuned models, while underline represents the second best*

值得注意的是，REWARDMAP 训练的 7B 模型不仅大幅超越所有开源模型（包括 Qwen2.5-VL-72B-Instruct），在 REASONMAP-PLUS 上甚至超越了闭源模型 Seed1.5-VL，表明精心设计的 RL 训练流程可在参数效率上弥补规模差距。

**跨基准泛化能力。** 表 2 展示了六个外部基准上的评估结果。REWARDMAP 微调的 Qwen2.5-VL-7B 在六项基准平均得分上达到 72.27%，较基座模型（68.80%）提升 +3.47%，且在所有子类别（空间推理、细粒度视觉推理、通用任务）上均取得一致提升。其中，SpatialEval 上的提升最为显著（57.30% → 70.81%，+13.51%），尤其在 mazenav 子任务上准确率从 19.60% 飙升至 57.20%，表明交通地图领域的空间推理能力可有效迁移至其他空间推理场景。在通用基准（MME、MMBench、MMStar）上未见退化，排除了灾难性遗忘的风险。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_iRVbPxHNrX/figures/004_Table_2.jpg]]
*Table 2: Evaluation of reference models and fine-tuned models on various benchmarks. Bold indicates the best results among fine-tuned models, while underline represents the second best. †, ‡, $, ∗, § denote the results from the technical report or the official HuggingFace repository (see result sources in Appendix C.3), while all other results are obtained from our own experiments*

### 消融分析

消融实验围绕 REWARDMAP 的三个核心设计展开：困难感知奖励设计、多阶段课程调度、以及冷启动策略，结果汇总于表 3–7。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_iRVbPxHNrX/figures/006_Table_3.jpg]]
*Table 3: Ablation on reward design and multi-stage design of REWARDMAP. “S.” represents results for short questions, while “L.” denotes results for long questions*

**奖励设计与多阶段课程的独立贡献与互补性。** 表 3 的逐组件消融表明，在仅使用 R_train（696 样本）的稀疏奖励设定下，单独引入困难感知奖励设计即可将 REASONMAP 加权准确率提升 +2.86% / +3.91%（S./L.）；进一步叠加多阶段课程设计，准确率再提升至 30.64% / 31.51%。两者组合使用（即完整 REWARDMAP）达到最优，证实了奖励密度提升与训练难度调度之间存在正向交互——密集奖励为课程学习提供了更稳定的梯度信号，而课程调度则确保模型在适当难度下充分利用这些信号。

**纯 RL 冷启动 vs. SFT→RL 流水线。** 表 4 对比了三种训练策略：RL 基线仅用 R_train、RL 基线联合使用 RPlus_train + R_train、以及 SFT→RL 流水线。联合使用 RPlus_train 的纯 RL 训练在 REASONMAP-PLUS 上达到 67.61% 加权准确率，显著优于 SFT→RL 流水线的 60.53%。这一反直觉结果表明，在具备密集奖励信号的数据上，直接 RL 冷启动可避免 SFT 阶段可能引入的次优策略先验，使模型从初始阶段即探索更优的推理路径。完整 REWARDMAP 在此基础上进一步引入困难感知奖励和多阶段调度，将准确率推至 74.25%。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_iRVbPxHNrX/figures/007_Table_4.jpg]]
*Table 4: Ablation on REASONMAP-PLUS. “S.” represents results for short questions, while ^ { 6 6 } L . 2 denotes results for long questions*

**多阶段粒度的影响。** 表 5 比较了粗粒度多阶段（仅按任务类型分为三个阶段）与 REWARDMAP 的细粒度课程（按问题类型和目标任务的更细划分）。粗粒度设计在 REASONMAP-PLUS 上仅达到 70.30%，低于 REWARDMAP 的 74.25%，说明更精细的难度递进有助于模型在每个阶段内充分掌握当前技能后再进入下一阶段，避免跨度过大导致的优化不稳定。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_iRVbPxHNrX/figures/009_Table_5.jpg]]
*Table 5: Ablation on granularity of multi-stage design. “S.” represents results for short questions, while “L.” denotes results for long questions*

**关键超参数敏感性。** 表 6 显示细节奖励权重 α 取 0.5 时在 REASONMAP-PLUS 上获得最佳综合表现，α 过小（0.3）则细节奖励贡献不足，过大（0.7）则可能稀释格式与正确性奖励的引导作用。表 7 的困难感知权重消融表明，适度的难度区分（如 γ=(1.0, 1.2, 1.5) 或 β=(0.0, 0.5)）即可带来稳定增益；当权重趋于均匀时性能略有下降，但一旦建立清晰的难度区分，性能便保持稳定。这表明困难感知机制的核心价值在于提供差异化的优化信号，而非精确的权重数值。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_iRVbPxHNrX/figures/010_Table_6.jpg]]
*Table 6: Ablation on the hyperparameter α. “S.” represents results for short questions, while “L.” denotes results for long questions*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_iRVbPxHNrX/figures/011_Table_7.jpg]]
*Table 7: Ablation on the difficulty-aware weights. “S.” represents results for short questions, while “L.” denotes results for long questions*

### 训练动态分析

图 4 的训练奖励曲线为稀疏奖励缓解提供了直接证据。基线 RL（仅使用 R_train）的奖励曲线在训练过程中始终处于低位且波动剧烈，反映稀疏奖励下策略优化的困难。相比之下，REWARDMAP 的奖励曲线从训练初期即呈现更高的绝对值和更稳定的上升趋势，这得益于 RPlus_train 提供的密集奖励信号以及困难感知加权对有效样本的放大效应。该曲线直观验证了方法设计的核心动机：通过增加奖励密度和差异化加权，将 RL 优化从“稀疏信号中艰难搜索”转变为“密集信号中稳定攀升”。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_iRVbPxHNrX/figures/008_Figure_4.jpg]]
*Figure 4: Comparison of training rewards between baseline RL and REWARDMAP. The yellow curve denotes the reward trajectory of REWARDMAP, while the blue curve corresponds to the baseline RL trained solely on REASONMAP*

### 跨模型规模与架构的泛化性

表 8 和表 9 分别验证了 REWARDMAP 在不同模型规模和架构上的一致性收益。在 Qwen2.5-VL-3B 和 Qwen2.5-VL-7B 两个规模上，REWARDMAP 均带来显著提升，且 7B 模型的绝对增益更大，表明方法对模型容量具有良好的可扩展性。在 Kimi-VL-A3B-Instruct 架构上，REWARDMAP 同样将 REASONMAP 加权准确率从 12.76% / 12.33% 提升至 18.58% / 17.36%，证明方法不依赖于特定模型架构或预训练范式。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_iRVbPxHNrX/figures/012_Table_8.jpg]]
*Table 8: Evaluation of REWARDMAP across model scales. “S.” represents results for short questions, while “L.” denotes results for long questions. Effectiveness of REWARDMAP across Model Scales. We evaluate the effectiveness of RE-WARDMAP across different model scales. Due to training cost constraints, we adopt Qwen2.5- VL-3B-Instruct as the base model and compare the baseline RL with REWARDMAP. As shown in Table 8, REWARDMAP achieves the promising results, demonstrating its robustness and effectiveness*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_iRVbPxHNrX/figures/013_Table_9.jpg]]
*Table 9: Results on Kimi-VL (Kimi-VL-A3B-Instruct). “S.” represents results for short questions, while “L.” denotes results for long questions. Generalization of REWARDMAP across Model Architectures. We further trained Kimi-VL (Kimi-VL-A3B-Instruct) with the REWARDMAP pipeline using the training set from REASONMAP. As shown in Table 9, the model achieves substantial performance gains, demonstrating that our method generalizes beyond the Qwen2.5-VL series*

### 局限与失败模式

尽管 REWARDMAP 在交通地图域取得了显著收益，其当前验证范围仍主要局限于该领域。虽然 ChartQA、Charxiv 上的初步结果表明方法具备扩展潜力，但在大规模、多样化的结构化视觉推理基准（如复杂流程图、工程图纸、多模态科学图表）上的系统评估尚缺。此外，多阶段课程和困难感知奖励设计引入了 γ、β、α 等额外超参数，增加了调参成本，且最优配置可能随任务域变化而迁移——当前在交通地图上搜索得到的最优参数未必直接适用于其他结构化视觉域。



## 定位与知识库关联

### 问题定位：稀疏奖励瓶颈

在细粒度视觉推理任务中，标准强化学习训练面临的核心瓶颈是**奖励稀疏**。以交通地图路线规划为例，模型需要从复杂图像中提取站点、线路、换乘关系，并执行多步逻辑推理，但传统 RL 仅根据最终答案的正确性给出二值奖励（对/错）。这导致策略优化时梯度方差高、收敛缓慢——当大部分采样轨迹的奖励为零时，GRPO 中的中心化优势函数 $\hat{A}_i$ 要么趋近于零（全错），要么极度偏斜（偶发的正确样本），无法为策略提供有效的学习信号。

REWARDMAP 的因果调节点在于：**通过引入包含部分正确性信息的细节奖励，并依据任务难度对奖励进行加权，配合从简单感知到复杂推理的多阶段课程训练，直接改变了训练过程中的奖励密度和优化路径。**

### 方法谱系

REWARDMAP 建立在 GRPO 算法之上，其基线方法包括：

- **RL (GRPO)**（Shao et al., 2024）：使用分组相对策略优化的标准 RL 训练，奖励函数仅包含格式奖励 $R_{\text{format}}$ 和正确性奖励 $R_{\text{correctness}}$，是 REWARDMAP 的直接对比基线。
- **RL (REINFORCE++)**（Hu et al., 2025a）和 **RL (ReMax)**（Li et al., 2023）：作为替代 RL 算法的对比基线，验证 REWARDMAP 的改进并非源于特定优化器选择。
- **SFT**：仅使用有监督微调在 REASONMAP-PLUS 上训练，无 RL 阶段。
- **SFT→RL**：先 SFT 后 RL 的两阶段流程，是 RL 冷启动的常见做法，RL 阶段使用基本格式和正确性奖励。

与上述基线相比，REWARDMAP 在三个关键设计维度上做出了改变：

| 设计维度 | 基线做法 | REWARDMAP 做法 |
|---------|---------|---------------|
| 奖励函数 | $R_{\text{format}} + R_{\text{correctness}}$ | $W_{\text{difficulty}} \times (R_{\text{format}} + R_{\text{correctness}} + \alpha \times R_{\text{detail}})$ |
| 训练课程 | 单阶段随机混合训练 | 多阶段课程：全局按任务类型和目标排序，局部保持随机 |
| 冷启动策略 | SFT 或直接 RL | 使用 REASONMAP-PLUS 的密集奖励问题进行 RL 冷启动 |

其中，$W_{\text{difficulty}} = W_{\text{map}} + W_{\text{question}}$，$W_{\text{map}}$ 根据地图难度（easy/medium/hard）取离散权重 $\gamma_e, \gamma_m, \gamma_h$，$W_{\text{question}}$ 根据规划问题是否涉及换乘赋予 $\beta_0$ 或 $\beta_1$。细节奖励 $R_{\text{detail}}$ 对答案中的部分正确项给予分数，形成稠密的中间反馈。

### 知识库定位与适用边界

**适用场景**：REWARDMAP 的核心设计——困难感知奖励与多阶段课程——适用于需要长链推理、且可定义部分正确性度量的结构化视觉理解任务。论文在交通地图领域进行了充分验证，并在 SpatialEval 的 mazenav 子任务上展示了空间推理迁移能力（准确率从 19.60% 提升至 57.20%），在 ChartQA、Charxiv 等数据集上也有初步扩展结果。

**适用条件**：
1. 任务存在可量化的“部分正确性”维度（如路线规划中的站点匹配数、计数任务中的部分正确项），这是 $R_{\text{detail}}$ 有效的前提。
2. 训练数据可按难度分层组织，支持从感知到推理的课程调度。
3. 基模型具备基本的视觉理解能力，RL 训练在此基础上进行微调。

**不适用或需谨慎使用的场景**：
- 纯开放式生成任务，难以定义结构化的部分正确性奖励。
- 任务难度无法预先标注或估算的场景，困难感知权重难以设定。
- 训练数据量过小（REWARDMAP 使用了 696 + 2,570 样本），课程划分可能导致各阶段数据不足。

### 关键证据强度

消融实验提供了清晰的因果证据链（Table 3）：
- 仅添加困难感知奖励设计，REASONMAP 短/长问题加权准确率分别提升约 2.86%/3.91%。
- 叠加多阶段课程后，进一步提升至 30.64%/31.51%。
- 完整 REWARDMAP（奖励设计 + 课程）达到最优 31.51%/31.77%。

冷启动策略消融（Table 4）表明，直接使用 REASONMAP-PLUS 进行 RL 冷启动（67.61%）优于 SFT→RL 流水线（60.53%），验证了纯 RL 冷启动的有效性。训练奖励曲线（Figure 4）直观展示了 REWARDMAP 提供比基线 RL 更密集且持续上升的奖励信号。

方法泛化性得到多维度验证：在 Qwen2.5-VL-3B/7B 不同规模（Table 8）和 Kimi-VL 不同架构（Table 9）上均带来一致提升。

### 局限与开放问题

**已知局限**：
1. **领域验证范围有限**：当前工作主要在交通地图领域进行系统验证，虽然展示了初步扩展性，但尚未在大规模、多样化的结构化视觉推理基准上进行全面评估。
2. **超参数敏感性**：困难感知奖励设计引入了 $\gamma$（地图难度权重）、$\beta$（换乘权重）、$\alpha$（细节奖励系数）等额外超参数。消融实验显示 $\alpha=0.5$ 时最优（Table 6），$\gamma=(1.0,1.2,1.5)$ 或 $\beta=(0.0,0.5)$ 达到较优性能（Table 7），但最优配置可能随任务变化，增加了调参成本。

**开放问题**：
1. **领域无关的奖励机制**：能否开发不依赖领域知识的细节奖励和困难感知机制，使 REWARDMAP 可直接应用于图表理解、流程图解析等更广泛的结构化视觉域？这需要解决“部分正确性”的通用定义问题。
2. **安全对齐的整合**：REWARDMAP 的框架如何与安全对齐技术结合？密集奖励可能引导模型产生格式正确但内容不可靠的输出，需要在提升推理能力的同时保证输出的可靠性和无害性。
3. **课程设计的自动化**：当前多阶段课程依赖人工定义的任务类型排序（二值判断 → 计数 → 规划），能否基于模型在训练过程中的表现动态调整课程难度？



## 原文 PDF

![[paperPDFs/ICLR_2026/RewardMap_Tackling_Sparse_Rewards_in_Fine_grained_Visual_Reasoning_via_Multi_Stage_Reinforcement_Learning.pdf]]
