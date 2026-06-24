---
title: "TreeGRPO: Tree-Advantage GRPO for Online RL Post-Training of Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/TreeGRPO_Tree_Advantage_GRPO_for_Online_RL_Post_Training_of_Diffusion_Models.pdf
openreview_forum_id: 3rZdp4TmUb
aliases:
- TreeGRPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将去噪过程构建为搜索树，通过前缀复用和分支探索提升样本效率，并利用奖励回溯计算每个步骤的特定优势，实现步骤级信用分配。"
primary_logic: "去噪轨迹共享前缀，适合采用树搜索进行高效探索，而树结构中的奖励回溯能够为每个边提供精细的优势信号，从而克服轨迹级方法的限制。"
claims:
- "TreeGRPO recasts the denoising process as a search tree."
- "TreeGRPO computes step-specific advantages via reward backpropagation."
- "Multi-child branching enables multiple policy updates per forward pass."
- "HPS-v2.1训练 (单奖励) 上 迭代时间 (s) = 72.0"
---

# TreeGRPO: Tree-Advantage GRPO for Online RL Post-Training of Diffusion Models

> [!tip] 核心洞察
> 去噪轨迹共享前缀，适合采用树搜索进行高效探索，而树结构中的奖励回溯能够为每个边提供精细的优势信号，从而克服轨迹级方法的限制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TreeGRPO：用于扩散模型在线RL后训练的树优势GRPO |
| 英文题名 | TreeGRPO: Tree-Advantage GRPO for Online RL Post-Training of Diffusion Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=3rZdp4TmUb); [Project](https://treegrpo.github.io) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | TreeGRPO |
| Dataset | HPS-v2.1训练 (单奖励), HPS-v2.1+ClipScore训练 (多奖励) |

> [!tip] 效果简介
> - HPS-v2.1训练 (单奖励) 上，迭代时间 (s) 为 72.0，对比 DanceGRPO: 173.5，变化 2.4× faster。
> - HPS-v2.1训练 (单奖励) 上，HPSv2.1↑ 为 0.3735，对比 所有对比方法 (见Table 1)，变化 优于所有基线。
> - HPS-v2.1+ClipScore训练 (多奖励) 上，迭代时间 (s) 为 79.2，对比 DanceGRPO: 184.0，变化 2.3× faster。

## 概述

扩散模型的对齐训练面临一个关键瓶颈：现有GRPO方法在每次策略更新时都需要采样完整的去噪轨迹，导致样本效率低下；同时，终止奖励被均匀归因到所有去噪步骤，缺乏细粒度的信用分配。**TreeGRPO** 通过将去噪过程重构为搜索树来解决这一问题——在SDE窗口进行分支探索多条候选轨迹，在ODE步骤复用共享前缀，并利用从叶节点向根部回溯的奖励传播机制，为每条边计算步骤特定的优势信号。

该方法的核心洞察在于：去噪轨迹天然共享前缀，适合采用树搜索进行高效探索；而树结构中的奖励回溯能够克服轨迹级方法的信用分配限制，提供精细的步骤级优势信号。由此，TreeGRPO在三个维度上改变了标准GRPO范式：**采样策略**从完整独立轨迹采样转向树结构分支采样，**信用分配**从轨迹级均匀奖励转向基于树结构的步骤级优势传播，**更新粒度**从每轨迹单次更新转向每个SDE窗口边的多次摊销更新。

实验表明，TreeGRPO在HPS-v2.1单奖励训练中实现**2.4倍**的迭代加速（72.0s vs. DanceGRPO 173.5s），在HPSv2.1和Aesthetic指标上均优于所有对比基线；在多奖励训练（HPS-v2.1+ClipScore）中保持**2.3倍**加速，ImageReward达到1.3426，优于MixGRPO的1.2056。该方法在效率-性能权衡空间中建立了更优的帕累托前沿（见 **Figure 1**），其框架结构如 **Figure 2** 所示。

## 背景与动机

扩散模型和流匹配模型在文本到图像生成领域取得了显著进展，但其输出分布与人类偏好之间仍存在系统性偏差。为弥合这一差距，研究者将生成模型的迭代去噪过程形式化为马尔可夫决策过程（MDP），并引入在线强化学习进行后训练。具体而言，去噪轨迹 $\tau = (s_0, a_0, \ldots, s_T)$ 被视作一个决策序列，目标是最大化终端奖励的期望：

$$\operatorname*{max}_{\theta} \mathbb{E}_{\tau \sim \pi_{\theta}} \big[ R(x_T, c) \big]$$

其中 $x_T$ 为最终生成的图像，$c$ 为文本条件。为支持策略梯度估计，确定性ODE采样需转换为保留边缘分布的等价SDE形式：

$$d \boldsymbol{x}_t = \left[ f_{\theta}(\boldsymbol{x}_t, t) + \frac{1}{2} \sigma^2(t) \nabla_{\boldsymbol{x}} \log p_{\theta}(\boldsymbol{x}_t \mid \boldsymbol{c}, t) \right] dt + \sigma(t) d \boldsymbol{W}_t$$

在此框架下，**DDPO**（Black et al., 2023）首次将策略梯度方法引入扩散模型对齐，但其样本效率低下，每个策略更新需采样完整去噪轨迹。**DPOK**（Fan et al., NeurIPS 2023）进一步将在线RL扩展到扩散模型，但同样受限于轨迹级更新的计算开销。

近期，GRPO（Group Relative Policy Optimization）系列方法被引入扩散模型对齐领域。**DanceGRPO**（Xue et al., 2025）、**FlowGRPO**（Liu et al., 2025）和**MixGRPO**（Li et al., 2025）等方法通过组内相对奖励进行策略优化，避免了对独立价值函数的需求。然而，这些方法共享两个核心瓶颈：

1. **样本效率低下**：每个策略更新都需要采样完整的独立去噪轨迹，大量计算被重复执行。尽管不同轨迹共享从初始噪声出发的早期去噪步骤，现有方法并未利用这种前缀冗余。

2. **粗粒度信用分配**：终止奖励被均匀归因到所有去噪步骤，缺乏对每一步决策质量的细粒度评估。这导致有效信号稀疏，策略优化效率受限。

上述瓶颈共同制约了训练效率与生成质量的帕累托前沿。本文的核心动机在于：**去噪轨迹天然共享前缀，适合采用树搜索进行高效探索；而树结构中的奖励回溯能够为每条边提供精细的优势信号，从而克服轨迹级方法的根本限制。**

## 核心创新

TreeGRPO 的核心创新在于将扩散模型的去噪过程重构为**树搜索**，从而同时解决现有 GRPO 方法的两大瓶颈：**样本效率低下**和**信用分配粗糙**。

### 瓶颈与因果机制

现有基于 GRPO 的扩散模型对齐方法（如 **DDPO** (Black et al., 2023)、**DanceGRPO** (Xue et al., 2025)）在每次策略更新时，都需要从随机噪声开始采样完整的去噪轨迹。这种“轨迹级”采样方式存在两个根本缺陷：

1. **样本效率瓶颈**：每条轨迹独立采样，去噪过程中共享的前缀计算被重复执行，导致大量冗余。
2. **信用分配粗糙**：终端奖励被均匀归因到所有去噪步骤，无法区分哪些步骤对最终质量贡献更大。

TreeGRPO 的因果洞察在于：**去噪轨迹天然共享前缀**（从同一初始噪声出发的轨迹在早期步骤高度相似），这恰好适合采用树结构进行高效探索；而树结构中的**奖励回溯**能够为每条边提供精细的优势信号，从而克服轨迹级方法的限制。

### 三个关键 Changed Slots

相对于基线方法，TreeGRPO 在三个相互关联的维度上进行了根本性改造：

| 维度 | 基线方法 | TreeGRPO | 机制 |
|------|---------|----------|------|
| **采样策略** | 完整独立轨迹采样 | 树结构分支采样 | ODE 步骤保持前缀复用；SDE 窗口创建分支，生成多条候选轨迹 |
| **信用分配** | 轨迹级均匀奖励 | 步骤级优势传播 | 叶节点奖励通过概率加权平均自底向上回溯到每条边 |
| **更新粒度** | 每个轨迹一次更新 | 每个 SDE 窗口边多次更新 | 多子分支摊销计算，单次前向传播支持多次策略更新 |

### 采样策略：从独立轨迹到树搜索

TreeGRPO 在固定的去噪时间范围内构建**稀疏搜索树**。具体而言，它在预定的 SDE 窗口内进行分支探索，而在窗口外的 ODE 步骤则保持确定性，从而复用共享前缀。这种设计的关键在于：

- **前缀复用**：从共享初始噪声开始，多个分支轨迹共享早期去噪步骤的计算，显著降低冗余。
- **SDE 窗口分支**：仅在选定的时间窗口内注入随机性（通过 SDE 形式），创建多条候选路径。窗口起始位置由截断几何分布采样（Eq. 7），偏向早期时间步。
- **多子分支摊销**：每个分支节点生成 $k$ 个子节点，单次前向传播即可获得多个策略更新所需的样本。

### 信用分配：从均匀奖励到边优势传播

TreeGRPO 的信用分配机制将树结构转化为精细的优势信号。流程如下：

1. **叶节点优势计算**：对于每个提示 $c$，将其对应的所有叶节点 $\ell \in \mathcal{L}(c)$ 的奖励分数进行组内标准化，得到叶优势：
   $$A_{\mathrm{leaf}}(\ell) = \frac{S^{(\ell)} - \mu_c}{\sigma_c}$$

2. **优势自底向上传播**：从叶节点向根节点回溯，父边 $e'$ 的优势由其所有子边优势的加权平均计算：
   $$A_{\mathrm{edge}}(e') = \sum_{e \in S(u)} w_u(e) A_{\mathrm{edge}}(e)$$
   其中权重 $w_u(e)$ 基于旧策略 $\pi_{\theta_{\mathrm{old}}}$ 下各子边的采样概率归一化得到。

3. **GRPO 更新**：最终使用基于每条边的优势进行 PPO 风格的裁剪替代损失优化（Eq. 12），仅对 SDE 窗口内的边进行更新。

这种设计的理论优势在于：加权平均结构将优势估计的方差降低了约 $\mathrm{ESS}$（有效样本量）倍，同时充当平滑正则化，惩罚具有高局部曲率的解。

### 方法定位

TreeGRPO 在方法谱系中处于 **GRPO 系列** 的延伸位置，与 DanceGRPO、FlowGRPO、MixGRPO 等同期工作共享“将 GRPO 应用于扩散模型”这一技术路线。但其根本差异在于：**它不改进 GRPO 的损失函数或奖励设计，而是重构了采样和信用分配的基础结构**——将去噪过程从“轨迹采样”升级为“树搜索”。这一范式转换使其在训练效率上获得 2.4× 的加速，同时在多项对齐指标上建立更优的 Pareto 前沿。

## 整体框架

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_3rZdp4TmUb/figures/004_Figure_2.jpg]]
*Figure 2: Introduction of TreeGRPO: Our framework optimizes the denoising process of diffusion/flow models by constructing search trees. Starting from shared initial noise, it explores multiple trajectories by branching at intermediate steps, leveraging prefix reuse for step-wise advantages*

TreeGRPO 将扩散/流模型的去噪过程重构为一棵**稀疏搜索树**，在固定去噪时间步长 $T$ 上构建，核心设计围绕三个相互耦合的机制展开：前缀复用采样、步骤级信用分配、以及摊销策略更新。整个训练循环的伪代码见 **Algorithm 1**，框架示意图见 **Figure 2**。

### Pipeline 总览

TreeGRPO 的训练迭代由四个顺序模块构成，形成从采样到更新的闭环：

1. **Tree-Structured Sampler（树结构采样器）**  
   输入一个共享的初始噪声 $x_T$ 和文本提示 $c$，在预定时间窗口内执行 SDE 分支，在窗口外使用 ODE 保持确定性前缀。这棵树的每条边对应一个去噪步骤，每条从根到叶的路径是一条完整的生成轨迹。采样器输出所有叶节点图像及每条边的对数概率 $\log \pi_{\theta_{\text{old}}}(e)$。

2. **Leaf Advantage Calculation（叶节点优势计算）**  
   对每个提示 $c$ 下的叶节点集合 $\mathcal{L}(c)$，利用奖励模型 $R$ 计算标量奖励 $S^{(\ell)}$，然后在**提示组内**进行标准化，得到叶节点优势：
   $$A_{\text{leaf}}(\ell) = \frac{S^{(\ell)} - \mu_c}{\sigma_c}, \quad \ell \in \mathcal{L}(c)$$
   这一步将不同奖励模型的量纲统一为可比较的优势信号，同时消除了提示难度对优势幅度的干扰。

3. **Advantage Propagation（优势传播）**  
   从叶节点自底向上，通过概率加权平均将优势信号传播到树中的每一条边。对于父节点 $u$ 的入边 $e'$，其优势由所有子边优势加权求和得到：
   $$A_{\text{edge}}(e') = \sum_{e \in S(u)} w_u(e) \, A_{\text{edge}}(e)$$
   其中权重 $w_u(e)$ 由旧策略在子边上的采样概率归一化确定：
   $$w_u(e) = \frac{\pi_{\theta_{\text{old}}}(e)}{\sum_{e' \in S(u)} \pi_{\theta_{\text{old}}}(e')}$$
   这一传播机制使得树中每一条边——包括那些未直接通向最终叶节点的内部边——都获得了一个细粒度的步骤级优势估计。

4. **GRPO Update（策略更新）**  
   利用传播后的边优势 $A_{\text{edge}}(e)$，在所有 SDE 窗口 $\mathcal{W}$ 内的边集合 $\mathcal{E}_t$ 上执行 PPO 风格的裁剪替代损失优化：
   $$\mathcal{L}_{\text{GRPO}}(\theta) = -\sum_{t \in \mathcal{W}} \sum_{e \in \mathcal{E}_t} \min\Bigl( r_t(e;\theta) A_{\text{edge}}(e), \, \text{clip}(r_t(e;\theta), 1-\epsilon, 1+\epsilon) A_{\text{edge}}(e) \Bigr)$$
   其中 $r_t(e;\theta) = \pi_\theta(e) / \pi_{\theta_{\text{old}}}(e)$ 为重要性采样比率。

### 关键设计决策

**SDE 窗口分支策略**是连接采样效率与信用分配的核心。TreeGRPO 并非在所有时间步都进行分支，而是仅在随机采样的 SDE 窗口内注入噪声创建多条子轨迹，其余步骤保持 ODE 确定性。窗口起始位置 $i$ 从截断几何分布中采样：
$$\mathrm{Pr}[i] = \frac{(1 - r) r^i}{1 - r^{T - w}}, \qquad i = 0, 1, ..., T - w - 1$$
参数 $r \in (0, 1)$ 控制对早期时间步的偏好程度。这一设计使得**前缀复用**成为可能：多个候选轨迹共享 SDE 窗口之前的确定性前缀，大幅减少了冗余的神经网络前向传播。

**多子分支摊销**进一步提升了更新密度。在每个 SDE 窗口内，一个节点可以分出 $k$ 个子分支，这意味着单次前向传播能够为多条边产生训练信号——与基线方法每条轨迹仅产生一次更新形成鲜明对比。

### 多奖励扩展

当使用多个奖励模型（如 HPS-v2.1 和 ClipScore）时，TreeGRPO 采用**优势加权求和**而非直接奖励相加。具体而言，为每个奖励模型独立计算叶节点优势 $A_1, A_2$，然后按预设权重（如 0.8:0.2）线性组合：
$$A = \sum_i w_i A_i$$
组合后的优势同样通过树结构自底向上传播，确保多目标信号在步骤级别得到平衡分配。消融实验表明，这种加权方式在各项指标上优于直接奖励相加。

### 数据流总结

整个 pipeline 的数据流是单向闭环的：**共享噪声 → 树结构采样（SDE 分支 + ODE 前缀）→ 叶节点奖励评估 → 自底向上优势传播 → 边级 GRPO 更新 → 更新后的策略用于下一轮采样**。这一设计从根本上改变了 GRPO 在扩散模型中的信用分配方式——从轨迹级均匀归因转变为基于树结构的步骤级差异化信号。

## 核心模块与公式推导

TreeGRPO 将扩散/流模型的去噪过程重构为一棵搜索树，通过**前缀复用**提升样本效率，并利用**奖励回溯**实现步骤级信用分配。其核心由四个模块串联构成，对应算法流程 Algorithm 1。

### 1. 树结构采样器

采样器从共享初始噪声 $x_T$ 出发，在固定的去噪时间步上构建稀疏搜索树。关键设计是**SDE窗口分支**：仅在预先调度的时间窗口内使用随机微分方程进行分支探索，窗口之外则使用常微分方程保持确定性前缀，从而复用共享计算。

窗口起始时间步 $i$ 从一个截断几何分布中采样：

$$ \mathrm{Pr}[i] = \frac{(1 - r) r^i}{1 - r^{T - w}}, \qquad i = 0, 1, ..., T - w - 1 \tag{7} $$

其中 $T$ 为总去噪步数，$w$ 为窗口宽度，参数 $r$ 控制分布偏向早期时间步的程度（$r$ 越小越偏向早期）。在每个窗口内，从当前节点出发采样 $k$ 条子路径（分支因子 $k$），每条边对应一个动作 $a_t$，其对数概率 $\log \pi_{\theta}(a_t \mid s_t, c)$ 被记录用于后续策略更新。

### 2. 叶节点优势计算

对于每个提示 $c$ 下的叶节点集合 $\mathcal{L}(c)$，每个叶节点 $\ell$ 对应一条完整轨迹，其终端图像 $x_0^{(\ell)}$ 由奖励模型评估得到标量奖励 $S^{(\ell)} = R(x_0^{(\ell)}, c)$。叶节点优势通过组内标准化计算：

$$ A_{\mathrm{leaf}}(\ell) = \frac{S^{(\ell)} - \mu_c}{\sigma_c}, \quad \ell \in \mathcal{L}(c) \tag{9} $$

其中 $\mu_c$ 和 $\sigma_c$ 分别为该提示下所有叶节点奖励的均值和标准差。这一标准化操作消除了不同提示间奖励量纲的差异，使优势信号在提示间可比。

### 3. 优势传播

优势从叶节点自底向上传播到树中每条边。对于节点 $u$，其入边 $e'$ 的优势等于其所有子边优势的加权平均：

$$ A_{\mathrm{edge}}(e') = \sum_{e \in S(u)} w_u(e) \, A_{\mathrm{edge}}(e) \tag{11} $$

其中 $S(u)$ 为节点 $u$ 的所有子边集合，权重 $w_u(e)$ 由旧策略 $\pi_{\theta_{\mathrm{old}}}$ 下各子边的采样概率归一化得到：

$$ w_u(e) = \frac{\pi_{\theta_{\mathrm{old}}}(e)}{\sum_{e' \in S(u)} \pi_{\theta_{\mathrm{old}}}(e')} \tag{10} $$

这一传播机制使得树中每条边——无论是否直接通向叶节点——都能获得一个精细的优势信号，从而支持步骤级的信用分配。从方差角度，该加权平均将优势估计的方差降低约 $\mathrm{ESS}$（有效样本量）倍：$\mathrm{Var}(\hat{A}_{\mathrm{tree}}) \approx \sigma_{\mathrm{env}}^2 / \mathrm{ESS}$。

### 4. GRPO 更新

获得每条边的优势后，TreeGRPO 使用 PPO 风格的裁剪替代损失进行策略优化。损失函数在 SDE 窗口内的所有边上求和：

$$ \mathcal{L}_{\mathrm{GRPO}}(\theta) = -\sum_{t \in \mathcal{W}} \sum_{e \in \mathcal{E}_t} \min\Bigl( r_t(e;\theta) A_{\mathrm{edge}}(e), \ \mathrm{clip}(r_t(e;\theta), 1-\epsilon, 1+\epsilon) A_{\mathrm{edge}}(e) \Bigr) \tag{12} $$

其中 $\mathcal{W}$ 为所有 SDE 窗口的时间步集合，$\mathcal{E}_t$ 为时间步 $t$ 处的边集合，$r_t(e;\theta) = \pi_{\theta}(e) / \pi_{\theta_{\mathrm{old}}}(e)$ 为概率比，$\epsilon$ 为裁剪阈值。由于一棵树中同一窗口内的多条子边共享前缀计算，**多子分支实现了每次前向传播的多次策略更新**（摊销计算），这是 TreeGRPO 训练效率显著优于逐轨迹采样方法的核心原因。

### 多奖励扩展

在多奖励训练场景下，TreeGRPO 为每个奖励模型独立计算叶节点优势 $A_1, A_2$，然后通过加权求和得到合并优势 $A = \sum_i w_i A_i$（例如 HPSv2.1 与 ClipScore 按 0.8:0.2 加权），再将合并优势按上述传播机制回传到树结构中。这种**优势加权求和**策略相比直接奖励相加，在各指标上实现了更好的平衡（详见 Table 2 消融）。

## 实验与分析

### 主实验：单奖励训练

**设置**：以 HPS-v2.1 作为唯一奖励模型进行 RL 后训练，使用 SD3.5-M 作为基座模型，在四个奖励指标（HPSv2.1、ImageReward、Aesthetic、ClipScore）上评估，同时记录单次迭代时间作为效率指标。对比基线包括 DDPO（Black et al., 2023）、DanceGRPO（Xue et al., 2025）、MixGRPO（Li et al., 2025）以及未微调的 SD3.5-M。

**结果**（Table 1）：TreeGRPO 在所有对齐指标上均优于所有基线方法，同时在效率上形成显著差距——迭代时间仅 72.0 秒，而 DanceGRPO 需 173.5 秒（2.4× 加速），DDPO 需 166.1 秒，MixGRPO 需 145.4 秒。具体而言，TreeGRPO 的 HPSv2.1 达到 0.3735，Aesthetic 达到 6.5094，均领先于全部对比方法。效率提升的核心机制在于**前缀复用**：树结构使得多条轨迹共享去噪前缀，避免了对相同中间状态的重复计算。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_3rZdp4TmUb/figures/005_Table_1.jpg]]
*Table 1: Train on HPS-v2.1 reward model and Eval on four reward models. Here are the comparison results for overhead and performance*

### 主实验：多奖励训练

**设置**：同时使用 HPS-v2.1 和 ClipScore 两个奖励模型（比例 4:1），通过优势加权求和（权重 0.8:0.2）而非直接奖励相加来合并多奖励信号。对每个奖励模型分别计算叶子优势 $A_1, A_2$，加权求和后沿树结构反向传播。

**结果**（Table 2）：TreeGRPO 在迭代时间上保持 2.3× 加速（79.2 秒 vs DanceGRPO 的 184.0 秒），同时在 ImageReward 上达到 1.3426，显著优于 MixGRPO 的 1.2056（+0.1370）。HPSv2.1（0.364）和 Aesthetic（6.4237）同样领先。DanceGRPO 在 ClipScore 上略高（0.375 vs 0.367），但整体 Pareto 前沿 TreeGRPO 占优。优势加权求和策略相比直接奖励相加，在各项指标间实现了更好的平衡，验证了多奖励场景下信用分离传播的有效性。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_3rZdp4TmUb/figures/006_Table_2.jpg]]
*Table 2: Train on HPS-v2.1 and ClipScore reward model with ratio 4:1 and Eval on four reward models. Here are the comparison results for overhead and performance*

### Pareto 前沿与效率-性能权衡

Figure 1 以归一化奖励分数 $(r - r_{sd3.5}) / (r_{max} - r_{sd3.5})$ 为纵轴、单 GPU 归一化挂钟时间为横轴，展示了各方法的效率-性能权衡。TreeGRPO 在所有奖励维度上建立了**严格占优的 Pareto 前沿**——即在相同或更短训练时间内，达到更高的对齐质量。这一优势源于树搜索的指数级样本效率：$k$ 分支、$d$ 层深度的树结构在一次前向传播中生成 $k^d$ 条轨迹，而传统方法仅生成一条。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_3rZdp4TmUb/figures/003_Figure_1.jpg]]
*Figure 1: The proposed TreeGRPO achieves the best pareto performance across the rewards and training efficiency, where the single-GPU runtime is the normalized wall-clock time. In (a), following the normalized metrics in RL domains (Mnih et al., 2013), the nromalized reward scores here is calculated by ( r - r _ { s d 3 . 5 } ) / ( r _ { m a x } - r _ { s d 3 . 5 } ) , where the r _ { m a x } in the HPS, ImageReward, Asethetic, ClipScore reward models are {1.0, 2.0, 10.0, 1.0} respectively*

### 消融实验：树结构配置

Table 3 系统研究了分支因子 $k$、深度 $d$ 和树数量对性能的影响，固定有效前向步数（NEF）为 10。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_3rZdp4TmUb/figures/007_Table_3.jpg]]
*Table 3: Ablation on sample tree structure. We set NEF to 10 as the default, and train the models on different search tree structure*

**核心发现**：
- **$k=3, d=3$（单棵树）** 在 HPSv2.1（0.3735）和 Aesthetic（6.5094）上达到最佳平衡，迭代时间 70.0 秒，被确定为默认配置。
- 较浅但更宽的结构（$k=5, d=2$）在 Aesthetic 上略高（6.5459），但 HPSv2.1 下降至 0.3703，且时间增至 86.7 秒。
- 多棵树配置（Tree#2）未带来显著增益，反而增加了计算开销。这表明**单棵适当配置的树**已能充分探索去噪空间，额外的并行树结构边际收益递减。

### 消融实验：推理采样策略

Table 4 比较了四种推理时的采样策略，其中随机窗口策略的参数 $r$ 控制几何分布的偏置程度（$r$ 越小，越偏好早期时间步的窗口选择）。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_3rZdp4TmUb/figures/008_Table_4.jpg]]
*Table 4: Ablation of inference strategies during sampling. Notes. ?? is the ratio parameter in randome window. The smaller ?? will choose the frontier noise step to expand search tree in a larger probability*

**核心发现**：
- **$r=0.5$** 提供最佳综合性能，HPSv2.1 达 0.3735，ImageReward 达 1.3294。
- $r=0.3$（偏好早期分支）在 Aesthetic 上最优（6.6067），但文本对齐指标下降，表明**早期去噪步骤的探索更有利于美学质量**。
- $r=0.7$（偏好后期分支）在 HPSv2.1 上表现较好（0.3715），说明**后期步骤的探索更有利于文本-图像对齐**。
- 移位窗口策略（Shift）在所有指标上均不如随机策略，证明随机化窗口位置对探索多样性至关重要。

### 失败模式与局限性

1. **超参数敏感性**：分支因子 $k$、深度 $d$、窗口大小和随机参数 $r$ 的最优设置因任务而异。当前采用固定值，在跨任务泛化时可能未达到全局最优。例如，$r=0.3$ 和 $r=0.7$ 分别在美学和对齐上占优，说明不存在普适的最佳配置。

2. **内存开销**：树结构采样在训练期间增加了内存占用（需同时维护多条分支轨迹的中间状态），文中未提供详细的内存对比数据。对于资源受限场景，这可能成为瓶颈。

3. **任务范围限制**：当前验证仅限于扩散/流模型的图像生成任务，尚未扩展到计算更密集的视频生成或 3D 生成领域。在这些场景下，树结构的额外内存开销可能更加突出。

4. **奖励模型依赖性**：所有实验基于特定的预训练奖励模型（HPS-v2.1、ClipScore 等），TreeGRPO 的性能优势依赖于这些奖励模型的质量和与人类偏好的对齐程度。若奖励模型存在系统性偏差，树结构的信用分配可能放大该偏差。

## 方法谱系与知识库定位

### 问题定位与核心瓶颈

扩散/流模型的对齐后训练中，现有的在线RL方法普遍面临两个相互关联的效率瓶颈。其一，**样本效率低下**：典型方法（如DDPO (Black et al., 2023)、DPOK (Fan et al., NeurIPS 2023)）在每个策略更新周期都需要从初始噪声开始采样完整的去噪轨迹，轨迹之间完全独立，无法复用中间计算结果。其二，**信用分配粗糙**：由于仅能获得终端奖励信号，这些方法将奖励均匀归因到所有去噪步骤，忽视了不同步骤对最终生成质量贡献的异质性。DanceGRPO (Xue et al., 2025)、FlowGRPO (Liu et al., 2025) 和 MixGRPO (Li et al., 2025) 等后续工作虽然引入了GRPO（Group Relative Policy Optimization）的组内相对优势机制，但本质上仍沿用了“完整独立轨迹采样 + 轨迹级均匀奖励”的范式，未能从根本上解决上述瓶颈。

TreeGRPO的核心洞察在于：**去噪轨迹天然共享前缀**——从同一初始噪声出发的轨迹在前若干步完全一致，仅在后续步骤因随机扰动而分叉。这一结构特性使得去噪过程天然适合采用树搜索进行高效探索，而树结构中的奖励回溯机制能够为每条边提供精细的优势信号，从而克服轨迹级方法的根本限制。

### 方法谱系中的关键改进

TreeGRPO相对于现有GRPO系列方法的改进，可归纳为三个相互耦合的维度：

**采样策略：从独立轨迹到树结构分支。** 基线方法对每个提示采样多条完全独立的去噪轨迹，计算开销与轨迹数线性增长。TreeGRPO将去噪过程重构为搜索树：在SDE（随机微分方程）窗口内进行分支探索，生成多个候选子轨迹；在ODE（常微分方程）步骤保持确定性前缀，所有分支共享计算。这一设计使得单次前向传播即可生成多条轨迹，实现了**摊销计算**（amortized computation）。具体而言，通过截断几何分布随机选择SDE窗口的起始时间步（Eq. 7），TreeGRPO在固定去噪时间范围内构建稀疏搜索树，分支仅发生在预设的SDE窗口内。

**信用分配：从轨迹级均匀奖励到步骤级优势传播。** 基线方法将终端奖励视为整条轨迹的统一信号，无法区分各步骤的贡献差异。TreeGRPO利用树结构实现细粒度信用分配：首先对每个提示的叶子节点计算组内标准化优势（Eq. 9），然后自底向上通过概率加权平均将叶子优势传播到每条边（Eq. 11）。这一机制使得每个去噪步骤都能获得特定的优势信号，而非被动接受均匀分配。

**更新粒度：从每轨迹一次到每边多次。** 由于树结构在SDE窗口内产生多条分支边，单次前向传播可生成多个可优化的决策点。TreeGRPO基于每条边的优势计算PPO风格的裁剪替代损失（Eq. 12），实现了比轨迹级方法更密集的策略更新。多子分支设计使得每次前向传播能够支撑多次策略更新，进一步提升了样本效率。

### 理论支撑与有效性机制

TreeGRPO的效率提升具有明确的理论基础。从方差缩减角度看，树结构中加权平均的优势估计器，其方差与有效样本量（ESS）成反比（Var(Â_tree) ≈ σ²_env / ESS），这意味着分支探索天然降低了优势估计的噪声。从优化景观角度看，加权平均操作等价于平滑正则化：最大化加权平均优势实际上优化的是E_{a~π}[Q(s_t, a)] ≈ Q(s_t, μ_a) + ½ Tr(Σ_π ∇²_a Q(s_t, a))，即在追求高期望回报的同时，偏好周围区域鲁棒的解，抑制高局部曲率的脆弱策略。

### 适用边界与局限

**超参数敏感性。** TreeGRPO引入了分支因子k、树深度d、SDE窗口大小及随机窗口参数r等多个新超参数。消融实验表明，最优配置（k=3, d=3, 单棵树, r=0.5）在HPSv2.1和美学分数上达到最佳平衡，但这些参数的最优设置可能因任务和奖励模型而异。当前采用固定值，尚未开发自适应调度策略。r参数的选择尤为关键：较小值（0.3）使窗口偏向早期时间步，有利于美学质量；较大值（0.7）偏向后期时间步，有利于文本对齐——这一权衡暗示了任务特异性调参的必要性。

**计算资源权衡。** 虽然TreeGRPO在迭代时间上实现了2.3–2.4×的加速（单奖励训练72.0s vs DanceGRPO 173.5s；多奖励训练79.2s vs DanceGRPO 184.0s），但树结构分支在训练期间增加了内存占用。文中未提供详细的内存对比数据，这一维度的资源消耗需手动验证。

**验证范围有限。** 当前工作仅在扩散/流模型的图像生成任务上进行了验证，使用的预训练模型为SD3.5-Medium，奖励模型为HPS-v2.1、ImageReward、Aesthetic和ClipScore。框架向计算更密集的视频生成或3D生成任务的扩展性尚未得到实证检验。

### 开放问题

1. **自适应树结构调度**：如何根据训练阶段、提示难度或奖励信号的统计特性，动态调整分支因子、窗口大小和树深度，以在探索充分性与计算开销之间实现自适应平衡？

2. **价值函数引导的树剪枝**：是否可以集成学习到的价值函数，在树展开过程中进行早期剪枝，仅保留高潜力分支，进一步降低计算开销？这将使框架从“固定结构搜索”转向“自适应搜索”。

3. **跨模态扩展**：该框架在视频生成（时序一致性约束下的长序列去噪）和3D生成（多视图一致性约束）等更复杂领域的适用性如何？树结构设计是否需要针对这些领域的特定结构先验进行调整？

4. **多奖励融合的优化**：当前多奖励训练采用固定的优势加权求和（0.8:0.2），是否存在更优的自适应权重分配策略，以在不同训练阶段或不同提示类型下动态平衡多个奖励目标？

## 原文 PDF

![[paperPDFs/ICLR_2026/TreeGRPO_Tree_Advantage_GRPO_for_Online_RL_Post_Training_of_Diffusion_Models.pdf]]
