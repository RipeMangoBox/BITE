---
title: "AutoQD: Automatic Discovery of Diverse Behaviors with Quality-Diversity Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AutoQD_Automatic_Discovery_of_Diverse_Behaviors_with_Quality_Diversity_Optimization.pdf
openreview_forum_id: FNnJIf4ymV
aliases:
- AutoQD
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将手工BD替换为基于占用度量的自动生成嵌入：用随机傅里叶特征近似占用度量间的最大均值差异（MMD），再通过校准加权PCA提取低维描述符。"
primary_logic: "通过随机傅里叶特征将策略的占用度量嵌入到有限维向量空间，使得欧氏距离近似MMD距离，从而无需领域知识即可自动捕捉有意义的行为差异，为QD优化提供高质量描述符。"
claims:
- "AutoQD能够自动生成行为描述符，无需人工设计。"
- "该方法利用随机傅里叶特征近似策略占用度量之间的MMD，创建反映行为差异的嵌入。"
- "将嵌入的低维投影作为CMA-MAE的行为描述符，实现QD优化。"
- "通过交替进行QD优化与描述符更新，逐步精炼行为空间。"
---

# AutoQD: Automatic Discovery of Diverse Behaviors with Quality-Diversity Optimization

> [!tip] 核心洞察
> 通过随机傅里叶特征将策略的占用度量嵌入到有限维向量空间，使得欧氏距离近似MMD距离，从而无需领域知识即可自动捕捉有意义的行为差异，为QD优化提供高质量描述符。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AutoQD：质量多样性优化的自动多样化行为发现 |
| 英文题名 | AutoQD: Automatic Discovery of Diverse Behaviors with Quality-Diversity Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=FNnJIf4ymV); [GitHub](https://github.com/conflictednerd/autoqd-code) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | AutoQD |
| Dataset | Ant, Swimmer, BipedalWalker |

> [!tip] 效果简介
> - Ant 上，GT QD Score (×10^4) 为 361.43 ± 2.17，对比 182.58 ± 2.53 (RegularQD)，变化 +178.85。
> - Ant 上，qVS 为 60.23 ± 9.4，对比 39.35 ± 3.99 (RegularQD)，变化 +20.88。
> - Swimmer 上，GT QD Score (×10^4) 为 21.31 ± 4.57，对比 11.09 ± 0.08 (RegularQD)，变化 +10.22。

## 概述

质量多样性（Quality-Diversity, QD）优化旨在发现一组既高性能又行为多样的策略集合。然而，现有QD算法的核心瓶颈在于**行为描述符（Behavioral Descriptors, BDs）必须由人工手工设计**——这要求研究者对任务有深入的领域知识，且预先定义的行为空间往往限制了探索范围，难以发现未预见的行为模式。

AutoQD 提出了一种**基于理论保证的自动行为描述符生成方法**，核心思路是：将策略的占用度量（occupancy measure）通过随机傅里叶特征（Random Fourier Features, RFF）嵌入到有限维向量空间，使嵌入向量间的欧氏距离近似策略占用度量之间的最大均值差异（Maximum Mean Discrepancy, MMD），从而无需领域知识即可自动捕捉有意义的行为差异。随后，通过校准加权PCA（cwPCA）将高维嵌入投影为低维描述符，直接供给CMA-MAE等QD优化器使用。整个流程交替进行QD优化与描述符更新，逐步精炼行为空间。

在六个标准连续控制任务（Ant、HalfCheetah、Hopper、Swimmer、Walker2d、BipedalWalker）上的实验表明，AutoQD在多数环境中显著优于手工设计描述符的RegularQD以及基于自编码器学习描述符的Aurora等基线方法。以Ant环境为例，AutoQD的GT QD Score达到361.43×10⁴，较RegularQD（182.58×10⁴）提升约98%；质量加权多样性指标qVS也从39.35提升至60.23。同时，AutoQD发现的策略集合在面对环境动力学参数变化（摩擦系数、质量缩放）时展现出更强的鲁棒性。

值得注意的是，该方法也存在局限性：在HalfCheetah等环境中发现的策略多样性虽高但平均质量较低，出现了“滑动”等低效行为；学习到的描述符不一定对应人类可解释的简单维度，而是捕捉复杂的混合行为因素。这些现象揭示了自动描述符与QD优化器之间更深层的交互机制，值得进一步研究。

## 背景与动机

### 质量多样性优化与行为描述符瓶颈

质量多样性（Quality-Diversity, QD）优化旨在同时发现高性能且行为各异的策略集合，其核心在于定义一个行为描述符（Behavioral Descriptor, BD）空间来区分策略的行为差异。现有的QD算法普遍依赖人工设计的BDs——例如在机器人运动任务中手工定义脚步接触模式或关节角度范围——这带来了两个根本性限制：

1. **领域知识依赖**：设计有效的BDs需要专家对任务行为空间的深刻理解，这在复杂或陌生领域中难以满足。
2. **探索空间受限**：手工BDs预设了行为差异的维度，可能遗漏未预见但有价值的行为模式，限制了QD算法的探索潜力。

### 现有自动描述符方法的不足

为摆脱对手工BDs的依赖，近期工作尝试从数据中自动学习行为表示。代表性方法如Aurora及其变体LSTM-Aurora通过自编码器学习状态表示作为描述符，但其存在固有缺陷：

- **状态重构的间接性**：自编码器以重构状态为目标，学习到的表示不一定直接反映策略行为差异，缺乏理论保证。
- **训练不稳定性**：自编码器需要定期重新训练，表示空间随训练过程漂移，影响QD优化的稳定性。

### 本文动机：从占用度量直接嵌入行为

本文的核心洞察在于：**策略的行为差异本质上由其占用度量（Occupancy Measure）的分布差异所刻画**。占用度量 $\rho^{\pi}(\mathbf{s},\mathbf{a}) = (1-\gamma) \sum_{t=0}^{\infty} \gamma^{t} P(S_{t}=\mathbf{s}, A_{t}=\mathbf{a}|\pi)$ 描述了策略 $\pi$ 下状态-动作对的折扣访问概率，是策略行为的充分统计量。因此，若能直接度量策略占用度量之间的分布差异，就能获得有理论依据的行为表示。

基于此，AutoQD提出了一种无需领域知识的自动行为描述符生成方法：利用随机傅里叶特征（Random Fourier Features, RFF）将策略的占用度量嵌入到有限维向量空间，使得嵌入向量间的欧氏距离近似最大均值差异（Maximum Mean Discrepancy, MMD），从而捕捉有意义的行为差异。这一嵌入随后通过校准加权PCA（cwPCA）降维，直接作为CMA-MAE等QD优化器的行为描述符，实现端到端的自动多样化行为发现。

## 核心创新

AutoQD 的核心创新在于**将手工设计的行为描述符替换为基于占用度量的自动生成嵌入**，从而消除了 QD 算法对领域知识的依赖。这一创新通过三个紧密耦合的模块实现：

### 1. 基于占用度量的策略嵌入

传统 QD 方法依赖人工定义的行为描述符（如脚步接触模式），这限制了探索空间并需要大量领域知识。AutoQD 的关键突破在于直接利用策略的**占用度量**（occupancy measure）来表征行为差异。占用度量定义为策略 $\pi$ 下状态-动作对的折扣访问概率：

$$\rho^{\pi}(\mathbf{s},\mathbf{a}) = (1-\gamma) \sum_{t=0}^{\infty} \gamma^{t} P(S_{t}=\mathbf{s}, A_{t}=\mathbf{a}|\pi)$$

为了在有限维空间中比较不同策略的占用度量，AutoQD 引入**随机傅里叶特征**（Random Fourier Features）来近似高斯核，从而将占用度量嵌入到有限维向量空间。在该空间中，嵌入向量之间的欧氏距离近似于占用度量间的**最大均值差异**（MMD），无需领域知识即可自动捕捉有意义的行为差异。具体而言，策略 $\pi$ 的嵌入 $\psi^{\pi}$ 通过以下方式计算：

$$\psi^{\pi} = \frac{1}{n} \sum_{j=1}^{n} (1-\gamma) \sum_{t=0}^{T} \gamma^{t} \phi(\mathbf{s}_t^{j}, \mathbf{a}_t^{j})$$

其中 $\phi(\mathbf{s},\mathbf{a})$ 是 $D$ 维随机傅里叶特征映射。该方法具有理论保证：嵌入距离以高概率近似真实 MMD 距离。

### 2. 校准加权 PCA 提取低维描述符

高维策略嵌入（如 $D=100$）无法直接作为 QD 优化的行为描述符。AutoQD 通过**校准加权 PCA**（cwPCA）将高维嵌入投影到低维空间（$k \ll D$）：

$$\text{desc}(\pi) = A \psi^{\pi} + b$$

其中 $A \in \mathbb{R}^{k \times D}$ 和 $b \in \mathbb{R}^k$ 通过对存档中策略的嵌入执行加权 PCA 获得。cwPCA 的两个关键设计是：
- **适应度加权**：根据策略的适应度对嵌入进行加权，使主成分偏向高性能策略的行为维度；
- **校准**：将投影后的描述符缩放到 $[-1, 1]$ 范围内，确保与 CMA-MAE 的网格划分兼容。

### 3. 交替优化与描述符更新

AutoQD 不采用固定描述符，而是**交替进行 QD 优化与描述符精炼**：
1. 使用当前描述符通过 CMA-MAE 发现多样化策略并更新存档；
2. 基于扩展后的存档重新执行 cwPCA，更新描述符投影参数。

这种交替机制使行为空间随策略集合的增长逐步精炼，形成正向反馈循环。

### 与基线方法的本质差异

| 维度 | 基线方法 | AutoQD |
|------|----------|--------|
| **行为描述符生成** | 手工设计或自编码器学习状态重构 | 基于占用度量的自动嵌入 + cwPCA 投影 |
| **策略表示** | 直接使用策略参数或状态编码 | 随机傅里叶特征嵌入，欧氏距离近似 MMD |
| **描述符更新** | 固定或定期重训练自编码器 | 定期基于存档嵌入的校准加权 PCA |

与 Aurora 等基于自编码器的方法相比，AutoQD 的嵌入具有理论支撑（MMD 近似保证），且无需训练神经网络，计算开销更低。与 RegularQD 相比，AutoQD 完全消除了手工设计描述符的需求，能够发现未预见的行为模式。

## 整体框架

![[assets/figures/papers/iclr26_0011_FNnJIf4ymV_AutoQD_Automatic_Discovery_of_Diverse_Behaviors/figures/001_Figure_1.jpg]]
*Figure 1: Overview of AutoQD. Left: Policy parameters are sampled from a CMA-ES instance and evaluated in the environment. The collected trajectories are embedded via a random Fourier features map ϕ to produce the policy embedding ψπ, which is then projected to a low-dimensional descriptor using the affine map Aψπ + b. The policy is added to the archive based on its return J(π) and descriptors desc(π), and CMA-ES updates its distribution based on the improvement made to the archive. Right: Periodically, embeddings from the archive are used to update A and b via cwPCA*

![[assets/figures/papers/iclr26_0011_FNnJIf4ymV_AutoQD_Automatic_Discovery_of_Diverse_Behaviors/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed policy embedding. Each policy $\pi _ { i }$ induces an occupancy measure $\rho ^ { \pi _ { i } }$ over state-action pairs. From sampled trajectories, a feature map ϕ embeds the policies into a vector space. Theorem 1 guarantees that the Euclidean distance between embeddings approximates the Maximum Mean Discrepancy (MMD) between the corresponding occupancy measures

AutoQD 围绕一个核心闭环展开：**自动生成行为描述符 → QD 优化 → 更新描述符**。该闭环将传统 QD 算法中依赖领域知识的手工描述符替换为基于策略占用度量（occupancy measure）的理论驱动嵌入，从而无需人工设计即可发现多样化行为。

### 三阶段流水线

AutoQD 的每次迭代由三个模块串联构成：

1. **策略嵌入（Policy Embedding）**  
   对于每个待评估的策略 $π$，在环境中采样 $n$ 条轨迹，利用随机傅里叶特征（Random Fourier Features, RFF）映射 $φ$ 将状态-动作对编码为 $D$ 维向量，再按折扣因子 $γ$ 加权求和，得到策略嵌入向量：
   $$ψ^π = \frac{1}{n} \sum_{j=1}^{n} (1-γ) \sum_{t=0}^{T} γ^{t} φ(s_t^j, a_t^j)$$
   该嵌入的核心性质是：两个策略嵌入之间的欧氏距离近似其占用度量间的最大均值差异（MMD），从而在无领域知识的前提下捕捉有意义的行为差异。

2. **行为描述符投影（cwPCA）**  
   将高维嵌入 $ψ^π$ 通过仿射变换降维为低维行为描述符：
   $$\text{desc}(π) = A ψ^π + b$$
   其中投影矩阵 $A ∈ ℝ^{k×D}$ 和偏置 $b ∈ ℝ^k$ 由**校准加权 PCA（cwPCA）** 在档案中所有策略的嵌入上计算得出。cwPCA 对标准 PCA 做了两处关键修改：以策略适应度加权，使高性能策略对描述符空间的影响更大；将投影后各轴校准到 $[-1, 1]$ 范围，以适配 CMA-MAE 的边界约束。

3. **QD 优化（CMA-MAE）**  
   将当前描述符函数 $\text{desc}$ 作为行为空间划分依据，调用 CMA-MAE 多实例进化策略进行搜索。CMA-MAE 在行为空间中维护多个 CMA-ES 实例，每个实例负责一个行为区域，通过采样、评估、更新档案的方式并行探索，最终产出覆盖多样化行为的高质量策略集合。

### 交替更新机制

AutoQD 并非一次性生成描述符后固定使用，而是采用**交替优化**策略：

- **QD 阶段**：使用当前描述符函数运行 CMA-MAE，将新发现的高质量策略加入档案。
- **描述符精炼阶段**：基于扩展后的档案重新执行 cwPCA，更新投影参数 $A$ 和 $b$，使行为描述符随搜索进展自适应演化。

这一交替机制使得行为空间的划分能够持续适配新发现的行为模式，逐步从粗糙的行为区分过渡到精细的多样性刻画。图 1 展示了从策略参数采样、轨迹收集、RFF 嵌入、cwPCA 投影到 CMA-MAE 优化的完整数据流。

### 输入输出规范

- **输入**：环境交互接口（状态-动作空间）、QD 档案容量、描述符维度 $k$、RFF 维度 $D$、采样轨迹数 $n$。
- **输出**：一个包含多样化高性能策略的档案，每个策略附带其在当前描述符空间中的坐标。
- **关键中间产物**：策略嵌入向量 $ψ^π$（$D$ 维）和行为描述符投影矩阵 $(A, b)$，后者随迭代更新。

> **注意**：上述流程中，RFF 嵌入的随机权重在初始化时采样一次后保持不变，不参与后续更新，这是保证嵌入空间稳定性和 MMD 近似理论成立的前提。

## 核心模块与公式推导

AutoQD 由三个核心模块构成：**策略嵌入（Policy Embedding）**、**行为描述符投影（cwPCA）** 和 **QD优化（CMA-MAE）**，三者交替迭代，逐步精炼行为空间。

### 策略嵌入模块

该模块将策略的占用度量嵌入到有限维向量空间，使得欧氏距离近似最大均值差异（MMD），从而无需领域知识即可捕捉行为差异。

**占用度量** 定义为策略 $\pi$ 下状态-动作对的折扣访问概率：

$$\rho^{\pi}(\mathbf{s},\mathbf{a}) = (1-\gamma) \sum_{t=0}^{\infty} \gamma^{t} P(S_{t}=\mathbf{s}, A_{t}=\mathbf{a}|\pi)$$

**随机傅里叶特征映射** 用于近似高斯核，将状态-动作对映射为 $D$ 维向量：

$$\phi(\mathbf{s},\mathbf{a}) = \sqrt{\frac{2}{D}} \left[ \cos(\mathbf{w}_1^T[\mathbf{s};\mathbf{a}] + \mathbf{b}_1), \dots, \cos(\mathbf{w}_D^T[\mathbf{s};\mathbf{a}] + \mathbf{b}_D) \right]$$

其中 $\mathbf{w}_i \sim \mathcal{N}(0, \sigma^{-2}I)$，$\mathbf{b}_i \sim \text{Uniform}(0, 2\pi)$，$\sigma$ 为核宽度参数。

**实际策略嵌入** $\psi^\pi$ 使用全部轨迹的折扣加权平均，以降低方差：

$$\psi^{\pi} = \frac{1}{n} \sum_{j=1}^{n} (1-\gamma) \sum_{t=0}^{T} \gamma^{t} \phi(\mathbf{s}_t^{j}, \mathbf{a}_t^{j})$$

其中 $n$ 为轨迹数量，$T$ 为截断长度，$\gamma$ 为折扣因子。该嵌入的期望与占用度量的期望嵌入一致，但利用了所有采集到的转移数据。

**理论保证**：定理1证明，$\psi^\pi$ 间的 $\ell_2$ 距离以高概率逼近占用度量间的真实 MMD 距离，误差随样本量 $n$ 指数衰减。

### 行为描述符投影模块（cwPCA）

将高维嵌入 $\psi^\pi$ 通过仿射变换投影到低维描述符空间（$k \ll D$）：

$$\text{desc}(\pi) = A \psi^{\pi} + b$$

参数 $A \in \mathbb{R}^{k \times D}$、$b \in \mathbb{R}^k$ 通过**校准加权PCA（cwPCA）** 从存档策略的嵌入中导出：

- **加权PCA**：按策略适应度加权嵌入后再执行PCA，使高性能策略对主成分方向贡献更大
- **校准**：将各输出轴缩放到 $[-1, 1]$ 范围，适配 CMA-MAE 的边界要求

描述符在优化过程中定期更新（如在第 20、50、100、200、300 代），实现行为空间的逐步精炼。

### QD优化模块（CMA-MAE）

使用 CMA-MAE 多实例进化策略，基于当前描述符 $\text{desc}(\pi)$ 搜索多样性高质量策略集合，并更新存档。所有方法统一使用 Toeplitz 矩阵参数化策略以降低参数量。

## 实验与分析

### 主实验结果

AutoQD 在六个标准连续控制任务上与五种基线方法进行了系统对比，包括使用手工描述符的 RegularQD、基于自编码器的 Aurora 及其 LSTM 变体、以及非 QD 方法 DvD-ES 和 SMERL。所有 QD 方法均采用 CMA-MAE 作为优化器，并使用 Toeplitz 矩阵参数化策略以保证公平性。评估指标包括基于真实行为描述符的 GT QD Score、Vendi Score（VS）和质量加权 Vendi Score（qVS），其中 VS 和 qVS 通过独立的大规模 RFF 嵌入核矩阵计算，避免信息泄露。

在 Ant 环境中，AutoQD 的 GT QD Score 达到 $361.43 \times 10^4$，相比 RegularQD 的 $182.58 \times 10^4$ 提升了约 98%；qVS 也从 39.35 提升至 60.23。在 Swimmer 中，QD Score 从 $11.09 \times 10^4$ 提升至 $21.31 \times 10^4$。在 BipedalWalker 中，AutoQD 的 QD Score 达到 $6.09 \times 10^4$，优于所有基线（最优基线 LSTM-Aurora 为 $3.36 \times 10^4$）。HalfCheetah 环境中，AutoQD 的 QD Score 为 $30.78 \times 10^4$，高于 RegularQD 的 $24.91 \times 10^4$，但提升幅度相对较小。完整结果见 Table 1。

![[assets/figures/papers/iclr26_0011_FNnJIf4ymV_AutoQD_Automatic_Discovery_of_Diverse_Behaviors/figures/003_Table_1.jpg]]
*Table 1: Comparison of AutoQD and baseline methods across six environments. Each environment is evaluated using GT QD Score (QD) reported in units of 104 for readability, qVS, and VS metrics. Reported values are the mean ± standard error over evaluations with three different random seeds. Higher values indicate better performance for all metrics*

值得注意的是，HalfCheetah 中 AutoQD 的 VS 较高而 qVS 较低，表明发现了大量多样化但平均质量偏低的策略——消融分析确认了其中包含"滑动"等低效行为模式。Walker2d 中 AutoQD 排名第二，落后于 RegularQD，分析显示其描述符过度关注底部关节，忽略了上肢协调等更复杂的行为差异。

### 鲁棒性分析：动态环境适应

为验证 AutoQD 发现的行为多样性在环境参数变化时的实用价值，实验在 BipedalWalker 中分别改变摩擦系数（0 到 6）和质量缩放因子（0.5 到 3.0），测试各算法种群中最佳策略的适应能力。

如 Figure 3 所示，AutoQD 在摩擦变化下维持最高平均回报（200-280），Aurora 紧随其后，而 SMERL 在约 110 处趋于平稳，RegularQD 和 DvD-ES 表现较差。质量变化下趋势类似。Table 2 的 AUC 指标量化了这一优势：AutoQD 在摩擦变化中取得 1429.66，在质量变化中取得 295.65，均为所有方法中最高。

![[assets/figures/papers/iclr26_0011_FNnJIf4ymV_AutoQD_Automatic_Discovery_of_Diverse_Behaviors/figures/004_Figure_3.jpg]]
*Figure 3: Performance of the best policy found by each algorithm under changing friction (left) or mass scale (right). The shaded regions represent the standard error across 32 evaluation seeds*

进一步分析种群层面的适应能力，Figure 4 统计了不同成功阈值下能够适应摩擦变化的策略数量。在严格阈值 $p=0.9$ 下，AutoQD 种群中成功适应的策略数量持续多于所有基线方法，说明其发现的行为多样性直接转化为更强的群体鲁棒性。

### 消融实验

**描述符维度的影响**：在 BipedalWalker 上，将行为描述符维度 $k$ 从 1 增加到 4，QD Score 和 Vendi Score 均单调提升，但平均适应度（Mean Objective）下降（Figure 10）。这表明更高维的描述空间能捕捉更丰富的行为差异，但可能引入低质量策略。

**RFF 嵌入维度的影响**：RFF 嵌入维度对性能影响较小（Figure 9）。即使仅使用 10 维特征，AutoQD 仍保持竞争力，说明随机傅里叶特征映射对维度选择具有较好的鲁棒性。

![[assets/figures/papers/iclr26_0011_FNnJIf4ymV_AutoQD_Automatic_Discovery_of_Diverse_Behaviors/figures/021_Figure_9.jpg]]
*Figure 9: Ablating RFF embedding dimension on BipedalWalker. The plot report mean values over 3 random seeds with bars indicating standard errors*

**轨迹数量的影响**：使用 2、5、10 条轨迹估计行为描述符仅带来微小性能差异（Table 9），QD Score 从 $5.99 \times 10^4$ 略微提升至 $6.12 \times 10^4$，表明嵌入估计对轨迹数量不敏感。

**适应度加权的作用**：校准加权 PCA 中的适应度加权在某些情况下可能产生反作用（如过度强调次优局部行为），但消融实验显示加权与不加权版本的 GT QD Score 相同（均为 $17.74 \times 10^4$），差异主要体现在 Vendi Score 上（Table 3）。

**描述符稳定性**：AutoQD 的行为描述符极其稳定。Figure 11 显示，对 400 个策略分配的描述符方差通常比 Aurora 等方法低数个数量级，这源于 RFF 嵌入的确定性特性，而非自编码器训练中的随机性。

![[assets/figures/papers/iclr26_0011_FNnJIf4ymV_AutoQD_Automatic_Discovery_of_Diverse_Behaviors/figures/025_Figure_11.jpg]]
*Figure 11: Distribution of variances of BDs assigned to 400 policies by different methods’ descriptor function*

### 失败模式与局限

1. **低质量多样性**：在 HalfCheetah 中，AutoQD 发现了大量多样化但性能低下的策略（如"滑动"行为），导致 qVS 偏低。这说明自动描述符可能将行为差异与性能优化解耦过度。

2. **行为覆盖偏差**：在 Walker2d 中，描述符过度聚焦于底部关节的运动模式，忽略了上肢协调等更复杂的行为维度，导致发现的策略集合在真实行为空间中的覆盖不完整。

3. **最大适应度不足**：AutoQD 的纯优化能力不及 SMERL 等有监督 RL 方法，在个别任务中最大适应度较低。这是因为 AutoQD 依赖 QD 优化而非专门的奖励最大化训练。

4. **可解释性缺失**：学习到的描述符不一定对应人类可解释的简单维度（如步态类型），而是捕捉复杂的混合行为因素。这限制了用户对行为空间的理解和控制。

## 方法谱系与知识库定位

### 与基线方法的差异根源

AutoQD 与现有 QD 方法的根本分歧在于**行为描述符（BD）的生成机制**，这一差异决定了各自的能力边界。

**RegularQD** 依赖手工设计 BD（如 Ant 的脚部接触模式），这要求研究者预判哪些行为维度有意义。其优势在于描述符高度可解释、与任务语义对齐；劣势是搜索空间被先验知识刚性约束，无法发现未预见的行为模式。AutoQD 移除了这一人工瓶颈，将 BD 生成自动化，但其代价是描述符不再对应人类可理解的简单维度。

**Aurora** 与 **LSTM-Aurora** 通过自编码器从状态（或完整轨迹）中学习低维表示作为 BD。这一路径同样无需手工设计，但存在两个结构性弱点：(1) 自编码器以重构误差为目标，学到的表示未必捕获行为差异——两个视觉上不同的轨迹可能被映射到相近的编码；(2) 训练需要大量数据且不稳定。AutoQD 以占用度量的 MMD 近似替代重构目标，从理论上保证嵌入空间中的欧氏距离反映行为分布的真实差异（Theorem 1），避免了自编码器表示与行为语义脱节的风险。

**DvD-ES** 与 **SMERL** 并非严格 QD 方法。DvD-ES 通过进化策略联合优化性能与多样性，但没有显式行为空间，无法按行为维度系统探索。SMERL 基于强化学习训练技能条件策略，用判别器奖励鼓励多样性，其优势在于纯优化能力强（在某些任务中最大适应度更高），但需要大量 RL 预训练，且多样性受限于判别器的分辨能力。AutoQD 作为黑盒 QD 方法，无需 RL 预训练即可直接进行质量-多样性联合搜索。

### 适用边界

AutoQD 的有效性建立在两个核心假设之上：

1. **占用度量能区分有意义的行为差异**。当环境的状态-动作空间本身包含足够信息来刻画行为变化时（如 MuJoCo 连续控制任务），RFF 嵌入能有效捕捉这些差异。但在状态空间信息贫瘠或行为差异主要体现在时序模式（而非状态-动作分布）的场景中，该方法可能失效。

2. **低维线性投影足以保留主要行为变异**。cwPCA 假设行为差异集中在嵌入空间的前 k 个主成分方向。当行为多样性需要更高维度才能表达时（消融实验显示增大 k 可提升 QD score 和 Vendi score），低维投影会丢失信息。目前 k 的选择依赖人工设定，缺乏自适应机制。

从实验结果看，AutoQD 在 Ant、Swimmer、BipedalWalker 等环境中显著优于所有基线，但在 HalfCheetah 和 Walker2d 中暴露出结构性局限。

### 已知局限与失效模式

**多样性与质量的失衡**。在 HalfCheetah 中，AutoQD 发现了高度多样的策略（VS 指标领先），但平均质量较低（qVS 落后），出现大量“滑动”等低效行为。这说明 cwPCA 中的适应度加权机制在某些情况下未能有效抑制低质量策略对描述符空间的污染——当低质量策略恰好占据行为空间的“间隙”位置时，它们会被保留并继续引导搜索偏离高质量区域。

**行为空间的局部过拟合**。在 Walker2d 中，AutoQD 过度关注底部关节的行为变化，忽略了上肢协调等更复杂的行为模式。这表明 RFF 嵌入可能对某些状态维度的变化更敏感（如与地面接触的关节），导致描述符空间被局部行为特征主导，形成隐式的“注意力偏差”。

**描述符的可解释性缺失**。与 RegularQD 的手工 BD 不同，AutoQD 学习到的描述符是 RFF 嵌入的线性组合，难以映射回人类可理解的行为维度（如“跳跃”、“爬行”等步态类型）。这在需要行为语义解释的应用场景中构成障碍。

**纯优化能力的上限**。AutoQD 的最终策略质量受限于 CMA-MAE 的黑盒优化效率。在有监督 RL 方法（如 SMERL）能充分利用梯度信息的场景中，AutoQD 的最大适应度可能不及这些方法。将自动描述符与基于梯度的 QD 方法（如 PGA-ME）结合是尚未探索的方向。

### 开放问题

1. **描述符维度的自适应选择**。当前 k 为固定超参数。能否在搜索过程中动态调整维度，或在 cwPCA 中引入基于方差的自动截断机制？

2. **适应度加权的条件性作用**。消融实验显示加权与否差异不显著（Table 3），但在 HalfCheetah 等环境中加权可能反作用——过度强调当前高性能策略会压缩行为空间，导致过早收敛。如何自适应调节加权强度？

3. **与梯度 QD 方法的集成**。AutoQD 的嵌入机制理论上可与任何 QD 优化器解耦。将其与 PGA-ME 等梯度方法结合，能否同时获得高质量的自动描述符和高效的策略搜索？

4. **扩展到部分可观测与动态观察空间**。当前方法假设完全可观测的固定维度状态-动作空间。在视觉观察或部分可观测环境中，如何定义有意义的占用度量等价物？

5. **缓解行为模式的过早收敛**。能否引入类似 Novelty Search 的显式新颖性奖励，或通过灭绝机制定期清除行为空间中的低质量“孤岛”，防止它们固化描述符方向？

## 原文 PDF

![[paperPDFs/ICLR_2026/AutoQD_Automatic_Discovery_of_Diverse_Behaviors_with_Quality_Diversity_Optimization.pdf]]
