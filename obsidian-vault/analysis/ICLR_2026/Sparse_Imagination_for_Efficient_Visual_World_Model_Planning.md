---
title: "Sparse Imagination for Efficient Visual World Model Planning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Sparse_Imagination_for_Efficient_Visual_World_Model_Planning.pdf
project_link: null
code_link: null
openreview_forum_id: faxcxKINBC
aliases:
- SI
- SIEVWMP
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "推理阶段通过drop ratio p控制随机丢弃的token比例，从而调节计算量与规划性能之间的权衡。"
primary_logic: "ViT patch token存在高度冗余，随机丢弃大量token仍能保留足够的状态信息；且随机采样避免了基于静态重要性方法在动态规划中产生的“盲点”问题，使其在效率和鲁棒性上均优于复杂选取策略。"
claims:
- "在PushT环境中，50%的token丢弃使每次迭代规划时间从173秒降至82秒（减少52.6%），同时平均成功率保持在70.0%，接近全量token基线（75.0%）。"
- "简单随机采样在六个环境中平均规划成功率达66.7%，一致优于基于学习（LTRP 59.5%）、基于注意力（最高64.0%）和聚类合并（ATC 41.7%）等复杂token选取方法。"
- "在仅依赖视觉的Wall规划中，随机采样以58.3%成功率远超基于注意力重要性选取（21.7%），证明了静态重要性指标在动态任务中遭遇“盲点”的灾难性影响。"
- "即便丢弃50%的token，视觉token与真实状态之间的nHSIC值仍保持高水平，单个随机token的预测能力已可与CLS token媲美，表明状态信息高度分布在patch token中。"
---

# Sparse Imagination for Efficient Visual World Model Planning

> [!tip] 核心洞察
> ViT patch token存在高度冗余，随机丢弃大量token仍能保留足够的状态信息；且随机采样避免了基于静态重要性方法在动态规划中产生的“盲点”问题，使其在效率和鲁棒性上均优于复杂选取策略。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 用于高效视觉世界模型规划的稀疏想象 |
| 英文题名 | Sparse Imagination for Efficient Visual World Model Planning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=faxcxKINBC) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Sparse Imagination |
| Dataset | PushT (60 episodes), PointMaze (60 episodes), Meta-World (50 tasks × 15 trials), LIBERO-10 |

> [!tip] 效果简介
> - PushT (60 episodes) 上，成功率 (%) / 规划时间 (s/iter) 为 70.0% (Drop 50%) / 82 s/iter，对比 75.0% (Full) / 173 s/iter，变化 -5.0% 成功率 / -52.6% 时间。
> - PointMaze (60 episodes) 上，成功率 (%) 为 100.0% (Drop 50%)，对比 98.3% (Full)，变化 +1.7%。
> - Meta-World (50 tasks × 15 trials) 上，成功率 All (%) 为 47.73% (Drop 50%)，对比 48.80% (Full)，变化 -1.07%。

## 概要

视觉世界模型通过预测未来状态来指导机器人规划，但其推理过程需要处理ViT编码器产生的大量patch token，自注意力计算的二次复杂度成为限制规划效率的核心瓶颈。在PushT等任务中，使用全部token的基线方法（Full-Patch, **DINO-WM**, Zhou et al., 2024）单次规划迭代耗时高达173秒，难以满足实时机器人部署需求。

本文提出**Sparse Imagination（稀疏想象）**，其核心洞察是：ViT patch token存在高度冗余，随机丢弃大量token仍能保留足够的状态信息用于有效规划。与基于静态重要性指标（如注意力分数）的token选取策略不同，随机采样在每次MPC迭代中动态生成不同的dropout模式，从根本上避免了重要性方法在动态规划中产生的“盲点”问题——即关键运动区域被持续遮蔽导致规划失败。

方法层面，Sparse Imagination包含两个关键设计：**训练阶段**采用随机分组注意力策略，将token随机分入两组并限制注意力仅发生在组内，迫使世界模型学会处理任意稀疏子集；**推理阶段**则由用户指定drop ratio $p$，动态随机丢弃token，仅用保留的$(1-p)N$个token进行滚动预测与CEM优化。

实验覆盖8个仿真环境和2个真实世界机器人任务。主要结果如下：
- 在PushT环境中，50% token丢弃使规划时间从173秒降至82秒（减少52.6%），成功率保持在70.0%，仅略低于全量基线的75.0%。
- 在六个任务环境的综合对比中，简单随机采样以平均66.7%的规划成功率，一致优于基于学习的剪枝（LTRP 59.5%）、基于注意力重要性（最高64.0%）和聚类合并（ATC 41.7%）等复杂token选取方法。
- 在仅依赖视觉的Wall规划中，随机采样以58.3%成功率远超基于注意力重要性选取的21.7%，直观揭示了静态重要性指标遭遇盲点的灾难性后果。
- 在Meta-World 50任务和LIBERO-10基准上，50%丢弃率下的成功率与全量基线基本持平（分别仅下降1.07%和0%），同时规划时间显著缩短。
- 真实世界LeRobot PickPlace任务中，50%丢弃达到80%成功率，与全量基线持平，且较VLA-only基线提升20个百分点。

信息论分析（nHSIC）和注意力探测实验进一步证实：即便丢弃50%的token，视觉token与真实状态之间的依赖关系仍保持高水平，单个随机token的预测能力已可与CLS token媲美，说明状态信息高度分布在patch token中，为稀疏规划提供了理论基础。

**方法谱系与定位**：Sparse Imagination属于基于模型的视觉规划方法，其世界模型继承自DINO-WM（Zhou et al., 2024）的ViT编码+Transformer预测框架，但在推理效率和鲁棒性上做出关键改进。相较于仅使用CLS token的单向量表示基线（Caron et al., 2021），稀疏想象保留了空间分布信息；相较于SmolVLA（Shukor et al., 2025）等纯策略方法，它通过规划显式优化未来轨迹。该方法可无缝替换全量规划，适用于基于采样的CEM规划器和基于梯度的MPC-GD规划器，并兼容多种自监督ViT编码器（MoCo-v3, MAE, DINOv3）。



### 视觉世界模型规划的效率瓶颈

基于模型的规划（model-based planning）已成为视觉机器人决策的重要范式。其核心思路是：利用世界模型（world model）在隐空间中模拟未来状态序列，并通过模型预测控制（MPC）迭代搜索最优动作。近年来，以 **DINO-WM**（Zhou et al., 2024）为代表的方法采用预训练ViT编码器提取图像的patch token作为世界模型的状态表示，在多种机器人任务上取得了优异的规划性能。

然而，这类方法面临一个根本性的效率瓶颈：ViT产生的patch token数量众多（例如DINO ViT-S/16在224×224图像上产生196个token），而世界模型中的自注意力计算复杂度随token数量呈二次增长。在MPC规划过程中，每个候选动作序列都需要完整的滚动预测，导致总计算量急剧膨胀。以PushT任务为例，全量token规划每次迭代耗时173秒（Table 2），这严重限制了其在实时机器人部署中的可行性。

### 现有加速方案的局限

针对视觉token冗余问题，已有研究探索了多种token压缩策略，大致可分为四类（Table 4）：

- **基于学习的剪枝**（如LTRP）：训练可学习的token选择模块，根据任务相关性动态保留token。
- **基于注意力重要性**（如Attention-Encoder, STAR, Attention-WM）：利用ViT编码器或世界模型内部的注意力分数作为token重要性的静态指标，保留高分token。
- **聚类合并**（如ATC）：将相似token聚类后合并，减少token总数。
- **固定模式采样**（如拉丁超立方采样LHS）：按空间均匀分布预先确定保留位置。

这些方法的共同假设是：存在一种“最优”的token子集，通过精心设计的选取策略可以在压缩计算的同时保持规划性能。然而，实验证据表明这一假设在动态规划场景下存在严重缺陷。

### 核心洞察：冗余性与盲点问题

本文通过系统性的信息论分析和消融实验，揭示了两条关键洞察：

**第一，ViT patch token存在高度冗余。** 通过归一化希尔伯特-施密特独立性准则（nHSIC）测量视觉token与环境真实状态之间的依赖关系，实验发现即使随机丢弃50%的token，nHSIC值仍保持高水平（Figure 7）。更令人惊讶的是，单个随机token的预测能力已可与全局CLS token相媲美（Figure 8）。这表明任务关键的状态信息并非集中在少数“重要”token上，而是高度分布在整个patch token集合中。

**第二，静态重要性选取在动态规划中产生灾难性的“盲点”。** 基于注意力分数等静态指标的方法倾向于反复保留相同的“重要”区域，同时系统性忽略其他区域。在MPC滚动过程中，被忽略的区域形成持久的观察盲点——世界模型无法感知这些区域内的物体运动，导致规划失败。在仅依赖视觉的Wall规划任务中，50% dropout下随机采样成功率为58.3%，而基于注意力重要性的方法骤降至21.7%（Section 5.4）。Figure 9直观展示了这一现象：在PushT任务中，重要性采样几乎完全遮蔽了蓝色球体的运动路径区域。

### 本文动机

上述发现指向一个反直觉的结论：在视觉世界模型规划中，**简单的随机token丢弃反而优于精心设计的重要性选取策略**。随机采样的核心优势在于其无偏的空间覆盖——每次MPC迭代动态生成新的随机mask，使得任何区域都有机会被观察到，从而天然避免了静态重要性方法固有的盲点问题。

基于这一洞察，本文提出**稀疏想象（Sparse Imagination）**框架，其核心思想是：训练世界模型适应任意稀疏token子集，并在推理阶段通过可控的随机dropout实现规划效率与性能之间的灵活权衡。该方法无需复杂的token选取模块，仅通过两个关键设计——随机分组注意力训练和推理时动态随机丢弃——即可在多个仿真和真实世界机器人任务上取得与全量token基线相近的成功率，同时将规划时间降低约50%。



## 核心方法与创新机理

### 创新动机：视觉世界模型规划的 token 冗余瓶颈

视觉世界模型（Visual World Model）在机器人规划中展现出强大的潜力，但其推理效率受制于 ViT 编码器产生的大量 patch token。以 **DINO-WM**（Zhou et al., 2024）为代表的全量 patch 规划范式，需要将所有 $N$ 个视觉 token 送入因果 Transformer 进行自注意力计算——这一过程的复杂度与 token 数量呈二次关系，成为实时部署的核心瓶颈。在 PushT 环境中，全量规划每次迭代耗时 173 秒，难以满足机器人实时控制的需求（Table 2）。

本文的核心洞察在于：**ViT patch token 中存在高度冗余**。信息论分析表明，即使随机丢弃 50% 的 token，视觉 token 与真实环境状态之间的归一化希尔伯特-施密特独立性准则（nHSIC）仍保持高水平（Fig. 7）；更令人惊讶的是，单个随机 token 的状态预测能力已接近全局 CLS token（Fig. 8）。这意味着状态信息高度分布在 patch token 中，而非集中在少数“重要”token 上——这为激进的 token 稀疏化提供了理论依据。

### 方法创新：推理时随机稀疏与训练时分组注意力

基于上述洞察，本文提出 **Sparse Imagination**，包含两个耦合的关键创新：

**Changed Slot 1：推理时 token 使用——从全量到随机稀疏**

基线方法（Full-Patch）在 MPC 规划的每次迭代中，将所有 $N$ 个 patch token 送入世界模型进行前向预测。Sparse Imagination 则引入一个由用户指定的 **drop ratio** $p \in [0, 1)$，在每次规划迭代时动态生成随机 mask，仅保留 $(1-p)N$ 个随机采样的 token 参与滚动预测与 CEM 优化（Fig. 1）。新的 dropout 模式在每次迭代中重新采样，确保空间覆盖的无偏性。

这一设计的精妙之处在于：**随机采样天然避免了基于静态重要性方法在动态规划中产生的“盲点”问题**。重要性采样方法（如基于注意力分数的 token 选取）倾向于反复保留相同的“重要”区域，却可能在物体运动路径上形成持续的信息空洞——世界模型无法观测物体运动，导致规划灾难性失败。在 Wall 环境的纯视觉规划中，随机采样以 58.3% 成功率远超基于注意力重要性选取的 21.7%（50% dropout），直观展示了盲点问题的严重性（Section 5.4）。

**Changed Slot 2：世界模型训练策略——从全量注意力到随机分组注意力**

标准世界模型训练使用全量自注意力，所有 token 可相互注意。然而，这样的模型在遇到推理时的稀疏 token 子集时会出现严重的分布偏移，预测误差显著增大（50% drop 时归一化 L2 误差达 0.036，见 Fig. 4）。

Sparse Imagination 提出 **随机分组注意力**（Randomized Grouped Attention）训练策略：在每次训练迭代中，将视觉 token 随机划分为两组，注意力被限制在组内进行（Fig. 2）。这迫使模型学会从任意稀疏子集中提取信息，而非依赖全量 token 的全局交互。消融实验表明，采用分组注意力训练的世界模型在 50% drop 时预测误差降至 0.016，远低于全量注意力训练的 0.036，并带来更高的规划成功率（Section 5.2, Fig. 4）。

### 创新效果：效率与性能的 Pareto 改进

Sparse Imagination 在多个维度上实现了对基线的实质性改进：

- **计算效率**：在 PushT 环境中，50% token 丢弃使每次迭代规划时间从 173 秒降至 82 秒（减少 52.6%），同时平均成功率保持在 70.0%，接近全量基线 75.0%（Table 1, Table 2）。在 Meta-World 的 50 个任务上，规划时间从 3.63 s/episode 降至 2.37 s/episode，成功率仅下降 1.07 个百分点（Table 3）。

- **方法简洁性优于复杂方案**：在六个环境的综合对比中，简单随机采样以平均 66.7% 的规划成功率，一致优于基于学习的剪枝（LTRP 59.5%）、基于注意力的选取（最高 64.0%）和聚类合并（ATC 41.7%）等复杂 token 选取方法（Table 4）。这一反直觉的结果印证了核心洞察：在高度冗余的视觉表征空间中，无偏随机覆盖比精心设计的静态重要性估计更鲁棒。

- **真实世界验证**：在 LeRobot PickPlace 真实机器人任务中，50% drop 的稀疏想象将 SmolVLA 策略的成功率从 60% 提升至 80%，同时规划延迟从 19.1 秒降至 10.4 秒（Fig. 5）。在 LIBERO-10 基准上，稀疏想象在成功率持平（33%）的情况下将规划时间减半。

- **跨编码器泛化**：稀疏想象框架可扩展至 MoCo-v3、MAE、DINOv3 等不同自监督视觉编码器，50% drop 下均可匹配或超越各自的全量基线（Section 5.1），证明该方法的通用性。

### 局限与待解决问题

当前方法需要用户预先指定固定的 $p$ 值，无法根据任务难度或场景动态在线调整。附录中探索的不确定性感知自适应 dropout（Ada-Rand）在 Wall 环境中展示了潜力——自动达到 95.0% 成功率且平均 drop ratio 仅 26.1%（Table 9），但该方向仍处于初步阶段。此外，在极高稀疏度（$p > 70\%$）下成功率明显下降，表明信息保留与计算效率之间存在根本权衡。如何设计动态稀疏策略、将稀疏想象推广至扩散模型规划器等更广泛的视觉决策框架，是值得进一步探索的开放问题。



![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_faxcxKINBC/figures/001_Figure_1.jpg]]
*Figure 1: Sparse Imagination. Sparse imagination accelerates planning by performing model predictive control (MPC) rollouts on a random subset of visual tokens. A new dropout pattern is dynamically sampled at each MPC iteration, and both predictions and optimization for CEM are computed using only the selected patches to improve efficiency and robustness*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_faxcxKINBC/figures/002_Figure_2.jpg]]
*Figure 2: Randomized Grouped Attention Strategy. Our randomized grouping strategy used during training to generalize to arbitrary token subsets. Visual tokens are randomly partitioned into two groups, and attention is masked to occur only within the same spatial group. This trains the model to process sparse inputs effectively, and its necessity is shown in ablations*

Sparse Imagination 构建于基于视觉的世界模型规划范式之上，其核心流水线由四个关键模块串联而成：**冻结的 DINO ViT 编码器**、**因果 Transformer 世界模型**、**推理时 Token 随机丢弃模块**和 **MPC 规划器**。

### 模块构成与数据流

**冻结的 DINO ViT 编码器**负责将原始图像观测 $o_t$ 映射为高维视觉特征。与仅使用单个 CLS token 的简化方案不同，该编码器输出完整的 $N$ 个 patch token $\mathbf{z}_t = \{z_{t,1}, \dots, z_{t,N}\}$，保留了空间分布式的状态信息。编码器在训练和推理阶段均保持冻结，不参与梯度更新。

**因果 Transformer 世界模型** $f_\theta$ 接收历史视觉 token 序列和动作 $a_t$，自回归地预测下一帧的 latent token $\hat{\mathbf{z}}_{t+1}$。训练目标为最小化预测 token 与真实 token 之间的均方误差：

$$\mathcal{L}_{\mathrm{wm}} = \frac{1}{N} \sum_{i=1}^{N} ||\hat{z}_{t+1,i} - z_{t+1,i}||^2$$

为使世界模型能够泛化到任意稀疏 token 子集，训练阶段引入了**随机分组注意力**策略：将视觉 token 随机划分为两组，注意力计算被限制在各自组内进行，迫使模型学会在信息不完整的条件下进行预测。

**Token 随机丢弃模块**仅在推理时激活。在每个 MPC 迭代步，该模块根据用户指定的丢弃比例 $p \in [0, 1)$ 生成随机二值 mask，仅保留 $(1-p)N$ 个随机采样的 token 参与后续的前向滚动和优化计算。每次迭代都会重新采样 mask，确保空间覆盖的动态多样性。

**MPC 规划器**在稀疏 token 上执行滚动优化。给定目标状态特征 $z_g$，规划器通过交叉熵方法或策略引导采样生成候选动作序列，并利用世界模型在保留的 token 子集上模拟未来 $H$ 步的想象轨迹。最优动作序列通过最小化目标条件损失选取：

$$\mathcal{L}_{\mathrm{mpc}} = ||\hat{z}_{t+H} - z_g||^2$$

### 关键设计决策

框架的两项核心设计形成了因果闭环：**随机分组注意力训练**使世界模型具备处理任意稀疏子集的能力，而**推理时随机丢弃**则利用这一能力实现计算加速。这种“训练时适应稀疏，推理时施加稀疏”的策略，使得世界模型在 50% token 丢弃下预测误差仅为 0.016（归一化 L2），远低于标准全量注意力训练的 0.036，从而在规划成功率与计算效率之间取得有利权衡。

值得注意的是，随机采样策略的鲁棒性源于视觉 token 中状态信息的高度冗余——信息论分析表明，即便丢弃 50% 的 token，视觉 token 与真实状态之间的 nHSIC 值仍保持高水平，单个随机 token 的预测能力已可与 CLS token 媲美。这一特性解释了为何简单的随机丢弃能够在多个环境中一致优于基于学习、基于注意力或聚类合并等复杂 token 选取方法。



### 方法架构

稀疏想象（Sparse Imagination）框架由四个核心模块构成：

1. **冻结的DINO ViT编码器**：将观测图像 $o_t$ 映射为 $N$ 个视觉latent patch token $z_t = \{z_{t,1}, \dots, z_{t,N}\}$。编码器在训练和推理阶段均保持冻结，仅作为特征提取器使用。

2. **因果Transformer世界模型** $f_\theta$：以历史视觉token和动作序列为输入，自回归地预测下一帧的latent token $\hat{z}_{t+1}$。其训练目标为最小化预测token与真实token之间的均方误差：

   $$\mathcal{L}_{\mathrm{wm}} = \frac{1}{N} \sum_{i=1}^{N} ||\hat{z}_{t+1,i} - z_{t+1,i}||^2$$

   其中 $\hat{z}_{t+1,i}$ 为第 $i$ 个预测latent token，$z_{t+1,i}$ 为对应的真实token。

3. **随机分组注意力训练策略**：为使世界模型在推理时能泛化到任意稀疏token子集，训练阶段将视觉token随机划分为两组，注意力计算被限制在组内进行。这一策略使模型学会在缺失部分token的情况下仍能做出准确预测，是稀疏想象成功的关键训练机制。消融实验表明，采用分组注意力训练的世界模型在50% token丢弃时预测误差仅为0.016（归一化L2误差），远低于标准全量注意力训练的0.036。

4. **Token随机丢弃模块（推理时）**：在规划阶段，按用户指定的丢弃比例 $p \in [0, 1)$ 生成随机mask，仅保留 $(1-p)N$ 个随机采样的token参与后续的滚动预测和优化。每次MPC迭代都会动态生成新的丢弃模式。

### 规划优化目标

稀疏想象采用模型预测控制（MPC）框架，通过目标条件损失评估候选动作序列的质量：

$$\mathcal{L}_{\mathrm{mpc}} = ||\hat{z}_{t+H} - z_g||^2$$

其中 $\hat{z}_{t+H}$ 为世界模型在候选动作序列下预测的第 $H$ 步（规划时域终点）的latent token，$z_g$ 为目标状态的特征表示。该损失衡量规划最终帧与目标状态在DINO特征空间中的差异。

### 关键设计决策

**随机采样优于重要性采样**：框架在推理阶段采用纯随机采样而非基于注意力分数或可学习剪枝的静态重要性方法。其核心依据在于：ViT patch token之间存在高度信息冗余，状态信息广泛分布在各token中。信息论分析（nHSIC）和注意力探测实验证实，即便丢弃50%的token，视觉token与真实状态之间的归一化HSIC值仍保持高水平，且单个随机token的预测能力已可与全局CLS token媲美。更重要的是，随机采样天然避免了静态重要性方法在动态规划中产生的“盲点”问题——即关键运动区域被系统性遮蔽导致世界模型无法观测物体移动。

**分组注意力训练的必要性**：随机分组注意力是使世界模型适应稀疏输入的关键训练策略。若采用标准全量注意力训练，模型在推理时遭遇token缺失会产生显著的分布偏移，导致预测误差急剧上升并最终损害规划成功率。



## 实验与关键发现

### 核心性能与效率权衡

Sparse Imagination 的核心主张是在保持规划性能的同时大幅降低推理计算量。实验覆盖了8个仿真环境和2个真实世界机器人任务（Figure 3），从简单导航到复杂灵巧操作，系统验证了这一权衡。

**Table 1** 汇总了不同丢弃率下的平均成功率。在10%-50%的适度丢弃区间，多数环境保持了与全量patch基线（Full-Patch, **DINO-WM** (Zhou et al., 2024)）相当的性能。以PushT为代表的高难度操作任务中，50%丢弃率下成功率为70.0%，而全量基线为75.0%；但规划时间从173秒/迭代降至82秒，减少了52.6%（Table 2）。PointMaze等较简单任务中，50%丢弃甚至实现了100%成功率，略超全量基线的98.3%。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_faxcxKINBC/figures/005_Table_1.jpg]]
*Table 1: Performance results (Mean Success Rate, %) across different environments with varying drop ratios*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_faxcxKINBC/figures/006_Table_2.jpg]]
*Table 2: Planning time and change compared to Full baseline for different environments at various drop ratios*

**Table 3** 展示了Meta-World 50项任务的规模化验证。50%丢弃率下总体成功率为47.73%，与全量基线的48.80%仅差1.07个百分点，但每episode规划时间从3.63秒降至2.37秒。值得注意的是，在Hard和Very Hard子集上，稀疏规划的性能下降更为明显，提示任务难度与可容忍的稀疏度之间存在负相关。

### 真实世界与VLA引导规划

在LIBERO-10和真实世界LeRobot任务中，稀疏想象与预训练VLA策略（**SmolVLA** (Shukor et al., 2025)）结合，展现了规划对策略的增强效应（Figure 5）。在LIBERO-10上，50%丢弃的稀疏规划将SmolVLA独立执行的成功率从29%提升至33%，与全量规划持平，同时规划延迟减半。在真实世界PickPlace任务中，稀疏规划（50%丢弃）达到80%成功率，显著高于VLA-only的60%，且与全量规划持平。Drawer任务中，稀疏规划将成功率从60%提至70%。

这些结果表明，VLA策略提供的候选动作序列质量是规划成功的关键前提；稀疏想象则在不增加计算负担的前提下，通过滚动验证筛选出更优的动作，有效弥补了开环策略的不足。

### 与复杂Token选取方法的全面对比

**Table 4** 是本文最具区分度的实验：将简单随机采样与四类token选取策略进行对比，包括固定采样（Fixed）、拉丁超立方采样（LHS）、基于学习的剪枝（LTRP）、基于注意力的选取（Attention-Encoder、STAR、Attention-WM）以及聚类合并（ATC）。所有方法共享相同的预训练世界模型和CEM规划超参数，仅改变token选取/保留机制。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_faxcxKINBC/figures/011_Table_4.jpg]]
*Table 4: The average planning success rate (%) achieved by various token dropout and merging methods under different drop ratios. Our results suggest that no method achieves significantly superior performance compared to the Random sampling. “Fixed” is excluded for Granular and Rope because they only use CEM, making “Random” and “Fixed” strategies equivalent. For the “Fixed” variant in Granular and Rope tasks, the Avg. is computed by reusing the drop ratios of the corresponding “Random” setting*

关键发现是：**随机采样以66.7%的平均成功率一致优于所有复杂方法**。LTRP仅59.5%，注意力类方法最高64.0%（Attention-WM），聚类合并ATC仅41.7%。这一反直觉结果揭示了两个深层机制：
1. 基于静态重要性（如注意力分数）的方法在动态规划中会产生**盲点**——被判定为“不重要”的区域在特定动作序列下可能恰好是关键物体运动路径所在，导致世界模型无法观测状态变化（Figure 9）。
2. 随机采样通过每轮重新采样，保证了无偏的空间覆盖，利用token信息的高度冗余性维持了状态表征质量。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_faxcxKINBC/figures/023_Figure_9.jpg]]
*Figure 9: Visualization Example of the Blind Spot Problem. Both images show 60% token dropout masks in PushT: (a) Random sampling and (b) an importance-based method (Attention-Encoder). In the importance-based case, the blue ball’s path toward any direction to solve the task is almost entirely covered by masked patches, creating a persistent blind spots where the world model cannot observe the object’s movement and thus fails to plan correctly. Random sampling, by contrast, spreads retained tokens more uniformly, making such task-relevant regions less likely to be systematically ignored*

### 盲点问题的决定性证据

盲点问题的量化分析提供了因果解释。在仅依赖视觉的Wall规划中，50%丢弃率下随机采样成功率为58.3%，而基于注意力重要性的选取骤降至21.7%——差距高达36.6个百分点。Figure 9直观展示了这一现象：重要性采样将PushT中蓝色方块的运动路径大面积遮蔽，形成持久盲区；而随机采样的mask均匀分布，保留了路径上的关键token。

进一步的“反证”实验强化了这一结论：在PointMaze中，刻意保留“最不重要”的50% token仍能达到63.7%成功率，而保留“最重要”token为79.2%——两者差距远小于预期，说明重要性排序本身在动态任务中并不可靠。

### 信息论分析：Token冗余的实证基础

Figure 7和Figure 8从信息论角度解释了随机采样有效的根本原因。通过归一化希尔伯特-施密特独立性准则（nHSIC）度量视觉token与真实环境状态的相关性：

$$\operatorname{nHSIC}(X,Y) = \frac{\widehat{\mathrm{HSIC}}(X,Y)}{\sqrt{\widehat{\mathrm{HSIC}}(X,X) \widehat{\mathrm{HSIC}}(Y,Y)}}$$

实验表明，即便丢弃50%的token，nHSIC值仍保持在高水平，与全量token的依赖度接近。Figure 8的注意力探测实验进一步揭示：**单个随机token的预测能力已可与CLS token媲美**（尽管方差较大），证明状态信息高度分布在patch token中，而非集中于特定位置。这解释了为何随机子集足以支撑有效规划。

### 分组注意力训练的消融贡献

**Figure 4** 的消融实验表明，随机分组注意力训练策略是稀疏想象成功的关键使能技术。采用标准全量注意力训练的世界模型在50%丢弃时归一化L2预测误差为0.036，而分组注意力训练降至0.016——误差减少超过一半。这一差距直接转化为规划成功率的显著提升：分组注意力训练的世界模型在各丢弃率下均优于全量注意力训练的对照模型。

分组注意力的核心机制在于：训练时强制token只能在随机划分的组内交互，迫使模型学会从任意稀疏子集中提取信息，而非依赖全量token间的密集交互模式。

### 编码器泛化性验证

稀疏想象框架对视觉骨干网络具有良好的泛化性。在PointMaze任务上，50%丢弃率下MoCo-v3编码器达到96.7%成功率（匹配全量基线96.7%），DINOv3达到98.3%（匹配全量基线98.3%），MAE编码器甚至以75.0%超越全量基线的68.3%。这表明token冗余并非DINO特有属性，而是自监督ViT特征空间的普遍特性。

### 规划器泛化性验证

**Table 8** 验证了稀疏想象在基于梯度的MPC-GD规划器上的有效性。在PointMaze环境中，50%丢弃率下成功率为94.0%，与全量基线持平；Wall环境中50%丢弃率为88.0%，与全量基线的94.0%相比仅有小幅下降。这证明稀疏想象不依赖于特定的采样型规划器，可推广至更广泛的MPC框架。

### 自适应稀疏度的初步探索

**Table 9** 报告了不确定性感知自适应dropout（Ada-Rand）的可行性研究。在Wall环境中，该方法自动达到95.0%成功率，同时平均drop ratio仅26.1%——在性能超越固定50%丢弃的同时使用了更少的token。这一结果展示了在线自适应sparsity的潜力，但方法仍处于初步阶段，需要用户预先指定不确定性阈值等超参数。

### 失败模式与局限性

1. **极高稀疏度下的性能骤降**：当丢弃率超过70%时，多数环境成功率明显下滑（Table 1），表明信息保留与计算效率之间存在根本性权衡，无法无限度压缩。
2. **复杂任务中的累积误差**：Meta-World的Hard/Very Hard子集上，50%丢弃的性能下降幅度大于简单任务，提示长时域、高精度操作对状态信息完整性更为敏感。
3. **固定丢弃率的刚性**：当前方法需要用户预先指定p值，无法根据任务难度或场景动态调整。Ada-Rand的初步结果虽然积极，但距离实用化仍有距离。
4. **聚类方法的低效**：**Table 7** 显示，token聚类合并方法（如ATC）不仅成功率低（41.7%），规划时间反而长于dropout方法——聚类本身的计算开销抵消了token减少带来的加速收益。
5. **盲点问题的根本局限**：随机采样虽然避免了盲点，但并未从根本上解决重要性采样方法的缺陷。如何结合静态重要性与随机探索，仍是一个开放问题。



## 定位与知识库关联

### 1. 方法脉络与基线关系

**稀疏想象**（Sparse Imagination）的核心贡献在于提出了一种推理阶段的视觉token随机丢弃策略，使基于ViT的世界模型在模型预测控制（MPC）规划中实现大幅加速。该方法建立在以下关键基线之上：

- **DINO-WM全量patch规划基线**（Zhou et al., 2024）：使用DINO ViT提取的全部$N$个patch token作为世界模型的状态表征，通过因果Transformer进行前向预测和MPC滚动优化。该方法规划性能优异，但自注意力计算复杂度与token数呈二次关系，成为实时部署的核心瓶颈。

- **CLS-Token基线**（Caron et al., 2021; Zhou et al., 2024）：仅使用DINO的全局CLS token作为单向量状态表征。虽然计算效率极高，但实验表明其规划成功率显著低于patch级表征，说明CLS token无法充分捕获任务所需的空间细节信息。

- **SmolVLA策略基线**（Shukor et al., 2025）：预训练的视觉-语言-动作（VLA）策略直接执行，无额外规划步骤。在复杂操作任务中，该基线可作为稀疏想象的策略引导源，也可作为独立对比基线。

稀疏想象与上述方法的关系是**互补增强**而非替代：它保留了DINO-WM的patch级表征能力，通过随机丢弃冗余token实现计算加速；同时可与VLA策略结合，在策略引导下进行稀疏规划，进一步提升复杂任务的成功率。

### 2. 方法谱系中的定位：token选取策略

稀疏想象的核心设计选择——随机采样——在与多类token选取/压缩方法的系统对比中展现了独特优势。这些方法分为四大类（Table 4）：

- **随机采样族**：包括每轮重采样的随机策略（Random）、固定mask的采样（Fixed）、以及拉丁超立方采样（LHS）。实验表明，每轮动态重采样是关键，Fixed策略因缺乏多样性而性能下降。

- **基于学习的剪枝**：如**LTRP**（learned token reduction policy），通过学习token重要性进行选择性保留。平均规划成功率59.5%，显著低于随机采样的66.7%。

- **基于注意力的重要性选取**：包括基于编码器注意力（Attention-Encoder）、基于世界模型注意力（Attention-WM）、以及**STAR**方法。这些方法利用注意力分数作为token重要性的静态指标，在六个环境中的平均成功率在63.0%–64.0%之间，均未超越随机采样。

- **聚类合并方法**：如**ATC**（adaptive token clustering），将相似token合并。平均成功率仅41.7%，表明合并操作可能破坏了对规划至关重要的空间细节。

一个关键的因果发现是：在仅依赖视觉的Wall规划任务中，基于注意力重要性选取的方法在50% dropout下成功率骤降至21.7%，而随机采样保持58.3%。这揭示了**静态重要性指标的“盲点”问题**——在动态规划中，被判定为“不重要”的区域可能恰好是任务执行的关键路径（Figure 9），导致世界模型无法观测物体运动，规划彻底失败。

### 3. 训练策略的独特贡献：随机分组注意力

稀疏想象的成功不仅依赖推理时的随机丢弃，更关键的是训练阶段的**随机分组注意力**策略（Figure 2）。该策略将视觉token随机分入两组，注意力仅允许在组内计算，迫使世界模型学习在任意稀疏子集上进行预测。

消融实验（Figure 4）表明：
- 使用分组注意力训练的世界模型在50% drop时预测误差仅0.016（归一化L2），远低于标准全量注意力训练的0.036。
- 这一预测精度的提升直接转化为更高的规划成功率，验证了“训练时引入稀疏性”对于“推理时利用稀疏性”的必要性。

值得注意的是，分组注意力训练并未损害全量patch的预测质量——在LPIPS指标上，分组训练的全量预测与标准训练相当甚至更优（Table 10），说明该方法是一种无损的泛化增强策略。

### 4. 适用边界与局限

**已验证的适用范围**：
- 基于DINO ViT（含DINOv3）、MoCo-v3、MAE等多种自监督视觉编码器的世界模型（Section 5.1），50% drop下均可匹配或超越各自全量基线。
- 基于采样的CEM规划器和基于梯度的MPC-GD规划器（Table 8），表明框架对规划器类型具有鲁棒性。
- 从简单状态控制（PointMaze）到复杂操作（Meta-World, LIBERO-10）再到真实机器人（LeRobot PickPlace/Drawer）的多层次任务。

**已知局限**：
- **固定dropout比例**：当前方法需要用户预先指定drop ratio $p$，无法根据任务难度或场景动态在线调整。附录中探索的不确定性感知自适应dropout（Ada-Rand）在Wall环境自动达到95.0%成功率且平均drop ratio仅26.1%（Table 9），但该方向仍处于初步阶段。
- **极高稀疏度下的性能衰减**：当drop比例超过70%时，规划成功率明显下降，表明信息保留与计算效率之间存在根本权衡，无法无限度压缩。
- **视觉骨架泛化性**：实验主要围绕ViT架构的自监督编码器展开，对CNN、多模态编码器等替代骨架的验证尚不充分。
- **盲点问题的根本解决**：随机采样通过无偏覆盖规避了盲点，但并未从根本上解决重要性采样方法的缺陷。如何结合静态重要性与随机探索仍是一个开放问题。

### 5. 开放问题与未来方向

1. **自适应稀疏策略**：能否设计一种根据状态不确定性或预测难度动态调整dropout比率的机制，在维持鲁棒性的前提下进一步压缩计算？初步的自适应实验（Ada-Rand）已展示潜力，但需要更系统的探索。

2. **跨框架推广**：稀疏想象的思想——在推理时动态随机丢弃冗余表征——能否推广到扩散模型规划器、分层规划、离线强化学习等更广泛的视觉决策框架？

3. **表征冗余的普适性**：token信息高度冗余的结论在其他自监督特征空间（如DINOv2、MAE）以及多模态token中是否一致成立？需要更系统的信息论分析。

4. **极高稀疏度缓解**：针对70%以上drop率下性能骤降的问题，能否引入知识蒸馏、渐进式dropout或辅助预测头等技术来扩展有效稀疏范围？

5. **混合采样策略**：重要性采样方法的盲点问题是否有更系统的补救方案，例如通过不确定性校准的混合采样、或基于任务上下文的动态重要性估计？

### 6. 知识库定位总结

稀疏想象在视觉世界模型规划领域占据了一个独特且实用的位置：它证明了**简单的随机策略在效率-鲁棒性权衡上优于复杂的确定性方法**。这一发现挑战了“更智能的token选取必然带来更好性能”的直觉，其深层原因在于ViT patch token中状态信息的高度冗余分布（nHSIC分析，Figure 7）以及静态重要性在动态任务中的根本缺陷。

该方法可作为视觉MPC规划的标准加速模块，与现有世界模型框架（如DINO-WM）和策略引导方法（如VLA）无缝集成，为实时机器人部署提供了即插即用的效率提升方案。



## 原文 PDF

![[paperPDFs/ICLR_2026/Sparse_Imagination_for_Efficient_Visual_World_Model_Planning.pdf]]
