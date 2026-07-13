---
title: "AMPED: Adaptive Multi-objective Projection for balancing Exploration and skill Diversification"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AMPED_Adaptive_Multi_objective_Projection_for_balancing_Exploration_and_skill_Diversification.pdf
project_link: https://geonwoo.me/amped/
code_link: null
aliases:
- AAMOPBESD
- AMPED
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "AMPED uses PCGrad-style gradient surgery over exploration and diversity objectives, with combined entropy and RND exploration rewards, AnInfoNCE diversity reward, and an adaptive skill selector."
primary_logic: "During pretraining it projects conflicting exploration and diversity gradients before policy updates, then uses a SAC-based selector to choose useful skills for downstream fine-tuning."
claims:
- "AMPED explicitly targets gradient conflict between state coverage and skill separability in unsupervised skill pretraining."
- "The combined RND, AnInfoNCE, gradient surgery, and skill selector components yield the best aggregate URLB return reported in the note."
- "Ablations show disabling gradient surgery or other components reduces overall returns, with the largest gradient-surgery impact in Jaco."
---

# AMPED: Adaptive Multi-objective Projection for balancing Exploration and skill Diversification

> [!tip] 核心洞察
> 通过显式解决探索与多样性之间的梯度冲突，并结合自适应技能选择器，AMPED 能够同时实现高状态覆盖和强技能区分度，从而在下游任务中取得更优的微调性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AMPED：自适应多目标投影以平衡探索与技能多样性 |
| 英文题名 | AMPED: Adaptive Multi-objective Projection for balancing Exploration and skill Diversification |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=U8A5nGuw7M) · [Project](https://geonwoo.me/amped/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | AMPED (Adaptive Multi-objective Projection for balancing Exploration and skill Diversification) |
| Dataset | URLB (Walker, Quadruped, Jaco 12 tasks), URLB (Walker), URLB (Quadruped), URLB (Jaco) |

> [!tip] 效果简介
> - URLB (Walker, Quadruped, Jaco 12 tasks) 上，总回报和 为 6415，对比 APT: 6362, CIC: 5822, CeSD: 5596, BeCL: 5705, ComSD: 5099, DIAYN: 3747, DDPG: 4243, RND: 5461，变化 比 APT 高 53，比 CIC 高 593。
> - URLB (Walker) 上，总回报和 为 3036，对比 APT: 3112, CIC: 2904, CeSD: 2720, BeCL: 2831, ComSD: 2592, DIAYN: 1662, DDPG: 2499, RND: 2538，变化 第二，比 APT 低 76。
> - URLB (Quadruped) 上，总回报和 为 2824，对比 APT: 2767, CIC: 2345, CeSD: 2334, BeCL: 2337, ComSD: 2023, DIAYN: 2001, DDPG: 1308, RND: 2488，变化 最高，比 APT 高 57。

## 概要

AMPED (Adaptive Multi-objective Projection for balancing Exploration and skill Diversification) 是一种面向无监督技能预训练的新型方法，旨在同时最大化状态覆盖（探索）和技能区分度（多样性）。该方法的核心洞察在于：探索目标（最大化状态熵）与多样性目标（最大化技能间互信息）的梯度在更新过程中存在严重冲突，直接求和会导致相互干扰。AMPED 通过引入梯度手术（PCGrad）在每次更新前检测并移除冲突的梯度分量，并结合自适应技能选择器，实现了高状态覆盖与强技能区分度的统一。在 URLB (Unsupervised Reinforcement Learning Benchmark) 的 12 个下游任务上，AMPED 取得了最高的中位数、IQM、均值以及最小的最优性差距，总回报和（6415）超越所有基线方法。



无监督技能预训练的目标是在无外部奖励的情况下学习多样化的行为技能，以便在下游任务中快速微调。现有方法通常聚焦于以下两个目标之一：

- **探索（Exploration）**：最大化状态熵 $H(X) = -\mathbb{E}[\log p(X)]$，鼓励智能体广泛覆盖状态空间。代表性方法包括基于粒子熵的 APT (Liu & Abbeel, 2021b) 和基于随机网络蒸馏的 RND (Burda et al., 2019)。
- **技能多样性（Skill Diversification）**：最大化技能与状态之间的互信息 $I(X;Y) = D_{KL}(p_{X,Y} \| p_X p_Y)$，鼓励不同技能产生可区分的状态分布。代表性方法包括 DIAYN (Eysenbach et al., 2019)、CIC (Laskin et al., 2022)、BeCL (Yang et al., 2023) 和 CeSD (Bai et al., 2024)。

然而，同时优化这两个目标面临根本性挑战：探索目标鼓励智能体均匀覆盖所有状态，而多样性目标要求不同技能的状态分布彼此分离。如图 3 所示，CeSD 倾向于连续覆盖但技能区分度不足，BeCL 则强调分离但留下明显覆盖空白。这种梯度冲突导致两个目标相互干扰，难以同时达到最优。



## 核心方法与创新机理

AMPED 的核心创新可归纳为以下四点：

1. **梯度手术（PCGrad）**：在每次参数更新前，检测探索梯度与多样性梯度之间的冲突（即点积为负），并将冲突分量投影到正交补空间，确保两个梯度不会相互抵消。如图 4 所示，当多样性梯度（红色）与探索梯度（蓝色）冲突时，随机选择一个梯度投影到另一个的正交补上，用合成梯度（紫色）进行更新。

2. **组合探索奖励**：将粒子熵奖励与 RND 奖励线性组合：$r_{exploration}(s) = \alpha r_{entropy}(s) + \beta r_{rnd}(s)$，弥补单一探索信号在高维空间中的不足。

3. **各向异性 InfoNCE (AnInfoNCE)**：采用可学习对角矩阵 $\hat{\Lambda}$ 的对比损失来估计技能间互信息，相比标准 InfoNCE 能更有效地促进技能区分。

4. **自适应技能选择器**：在微调阶段引入基于 SAC (Haarnoja et al., 2018) 的技能选择器，采用 $\epsilon$-greedy 策略自适应选择最匹配当前任务的预训练技能，而非均匀随机采样。



![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_U8A5nGuw7M_AMPED_Adaptive_Multi-obj/figures/001_Figure_1.jpg]]
*Figure 1: Graphical scheme explaining our method, AMPED. (a) At initialization, the skills exhibit small coverage that are close to each other in the task space. (b) During skill pretraining, exploration and diversity objectives encourage skills to widen and repel each regions. (c) In fine-tuning, the skill selector identifies the skill best aligned with the target task at each step. (d) The selected skill is further adapted via extrinsic rewards to maximize performance on the target task.*

AMPED 的训练流程分为两个阶段（如图 1 和图 2 所示）：

**预训练阶段**：智能体以随机采样的技能为条件，使用内在奖励（探索奖励 + 多样性奖励）进行优化。探索奖励和多样性奖励的梯度不直接求和，而是通过梯度手术机制平衡后再更新策略和值函数。

**微调阶段**：技能选择器根据任务反馈自适应选择技能，智能体使用下游任务的外在奖励进一步优化。



### 5.1 探索奖励

探索奖励由两部分组成：

- **粒子熵奖励**：基于 k 近邻估计的状态熵，$r_{entropy}(s) = \log(\sum_{l=1}^k R_{i,l,n})$，其中 $R_{i,l,n}$ 是第 $i$ 个状态到其第 $l$ 近邻的距离。
- **RND 奖励**：基于预测网络 $f_\theta$ 与固定随机目标网络 $f_{target}$ 之间的预测误差。

总探索奖励为：$r_{exploration}(s) = \alpha r_{entropy}(s) + \beta r_{rnd}(s)$。

### 5.2 多样性奖励

多样性奖励基于 AnInfoNCE 损失（Rusak et al., 2024）：

$$\mathcal{L}_{\mathrm{AINCE}}(f, \hat{\Lambda}) = -\mathbb{E}_{s,s^+,\{s_i^-\}}\left[\ln \frac{e^{-\|f(s^+)-f(s)\|_{\hat{\Lambda}}^2}}{e^{-\|f(s^+)-f(s)\|_{\hat{\Lambda}}^2} + \sum_{i=1}^M e^{-\|f(s_i^-)-f(s)\|_{\hat{\Lambda}}^2}}\right]$$

其中 $\hat{\Lambda}$ 是可学习的对角矩阵，用于学习各向异性的距离度量。如图 11 所示，AnInfoNCE 损失与两个高斯分布均值向量之间的欧氏距离呈正相关，因此能有效促进技能分布分离。

### 5.3 梯度手术（PCGrad）

对于探索梯度 $g_{explore}$ 和多样性梯度 $g_{diversity}$，如果检测到冲突（即 $g_{explore} \cdot g_{diversity} < 0$），则随机选择一个梯度投影到另一个的正交补上：

$$g_{explore} \leftarrow g_{explore} - \frac{g_{explore} \cdot g_{diversity}}{\|g_{diversity}\|^2} g_{diversity}$$

如图 5 所示，在 URLB 环境中，梯度冲突比例极高：Walker 域为 $0.9997 \pm 0.0004$，Quadruped 域为 $0.9997 \pm 0.0006$，Jaco 域为 $0.7777 \pm 0.1256$，验证了梯度手术的必要性。

### 5.4 技能选择的理论分析

定理 1 给出了贪心技能选择器的样本复杂度界。定义 $\delta = \min_{i \neq j} d(\rho_{z_i}, \rho_{z_i})$ 为技能间状态占用分布的最小总变差距离，$\varepsilon = d(\rho, \rho_{z_\star})$ 为目标任务分布与最优技能分布之间的距离。若 $\Delta \equiv \delta - 2\varepsilon > 0$，则从 $n$ 条独立同分布轨迹中，贪心选择器选择次优技能的概率满足：

$$\mathrm{Pr}[\widehat{z} \neq z_\star] \leq 2^S H \exp\left(-\frac{n \Delta^2}{2}\right$$

其中 $S$ 是状态空间大小，$H$ 是技能数量。保证以置信度 $1-\eta$ 选择最优技能所需的最小轨迹数为：

$$n \geq \frac{2}{\Delta^2} (S \log 2 + \log H - \log \eta)$$



## 实验与关键发现

### 6.1 主要结果

在 URLB 的 12 个下游任务上，AMPED 取得了最高的聚合性能（Figure 8）。具体地，AMPED 在 IQM 上超越 BeCL 17.96%、CIC 15.02%、APT 9.73%、CeSD 20.91%、ComSD 35.01%。

Table 13 展示了各域的总回报和：

| 方法 | Walker | Quadruped | Jaco | 总计 |
|------|--------|-----------|------|------|
| **AMPED** | **3036** | **2824** | **555** | **6415** |
| APT | 3112 | 2767 | 483 | 6362 |
| CIC | 2904 | 2345 | 573 | 5822 |
| CeSD | 2720 | 2334 | 542 | 5596 |
| BeCL | 2831 | 2337 | 527 | 5705 |
| ComSD | 2592 | 2023 | 484 | 5099 |
| DIAYN | 1662 | 2001 | 76 | 3747 |
| DDPG | 2499 | 1308 | 436 | 4243 |
| RND | 2538 | 2488 | 435 | 5461 |

### 6.2 消融实验

Table 1 展示了各组件的贡献：

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_U8A5nGuw7M_AMPED_Adaptive_Multi-obj/figures/019_Table_1.jpg]]
*Table 1: Episode returns under component ablation. Ablating any single component, RND, AnInfoNCE loss, gradient surgery, or the skill selector, occasionally improves performance on individual tasks, yet yields degraded overall returns. AMPED (Ours) indicate the procedure including all of them; RND reward, AnInfoNCE, gradient surgery, and skill selector. The best result is shown in bold, and the second-best is underlined.*

| 消融组件 | Walker 变化 | Quadruped 变化 | Jaco 变化 |
|----------|------------|---------------|-----------|
| 移除 RND | -21.1% | -16.2% | -0.9% |
| 移除 AnInfoNCE | -5.7% | -2.4% | -16.5% |
| 禁用梯度手术 | -4.3% | -9.3% | -26.5% |
| 移除技能选择器 | +0.5% | -6.2% | -4.5% |

梯度手术在 Jaco 域上的影响最大（-26.5%），表明该域中梯度冲突的缓解对性能至关重要。RND 在 Walker 和 Quadruped 上贡献显著，但在 Jaco 上影响较小，这与 Jaco 域较低的梯度冲突比例一致。

### 6.3 可视化分析

在 Tree Maze 环境中（Figure 7），AMPED 同时实现了最高的状态覆盖和技能区分度，而 CeSD 和 BeCL 分别只优化了其中一个方面。Figure 12 进一步展示了随着技能数量从 5 增加到 25，AMPED 始终能填充整个迷宫并保持技能区域分离，而 DIAYN 和 BeCL 留下空白，CIC 和 ComSD 则出现重叠。

在 Square Maze 中（Figure 14），AMPED 的状态熵与 CIC 和 ComSD 相当，显著高于 BeCL 和 DIAYN；同时其互信息估计与 BeCL 和 DIAYN 相当，显著高于 CIC 和 ComSD，验证了 AMPED 在探索与多样性之间的平衡能力。

### 6.4 超参数敏感性

Table 14 和 Table 15 分别展示了投影比例和技能数量的影响。默认投影比例在三个域上均取得最高总回报，优于极端比例 $p=0.0$ 和 $p=1.0$。默认 16 个技能在 Quadruped 和 Jaco 上表现最佳，在 Walker 上与 32 个技能版本相当。

### 6.5 公平性说明

- 所有基线均使用官方实现或公开代码库复现，并采用相同的评估协议（Agarwal et al., 2021）。
- URLB 实验使用 10 个随机种子，消融实验使用 3 个随机种子，报告均值 ± 标准差。
- CeSD 的官方超参数无法复现其报告性能，且方差较大。
- AMPED 的预训练时间（约 13.5 小时）与基线方法相当，未引入显著额外计算开销。

### 补充图表

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_U8A5nGuw7M_AMPED_Adaptive_Multi-obj/figures/040_Table_2.jpg]]
*Table 2: Performance comparison under extreme α and β settings. α and β control the relative weight of entropy-based and RND rewards. AMPED (Ours) result are computed as return (mean ± standard deviation) over 10 random seeds, while each α or β configuration is evaluated using three random seeds. The best result is shown in bold, and the second-best is underlined.*

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_U8A5nGuw7M_AMPED_Adaptive_Multi-obj/figures/041_Table_3.jpg]]
*Table 3: Hyperparameter search results for α and $\beta$ . Results reflect single-run returns for each modified configuration, except for AMPED. The best result is shown in bold, and the second-best is underlined.*

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_U8A5nGuw7M_AMPED_Adaptive_Multi-obj/figures/042_Table_4.jpg]]
*Table 4: Fine-tuning returns under different skill-selection regimes. “Single-Skill” reports the average return across fine-tuning each pretrained skill individually; “Oracle Best Skill” denotes the highest return achieved by the single best skill. Results are computed over three random seeds and reported as mean ± standard deviation. The best result is shown in bold, and the second-best is underlined.*

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_U8A5nGuw7M_AMPED_Adaptive_Multi-obj/figures/043_Table_5.jpg]]
*Table 5: Number of unique skills used per task. Results are computed over three random seeds and reported as mean ± standard deviation.*



## 定位与知识库关联

AMPED 综合了无监督强化学习中三类方法的原理：

- **数据驱动方法**：基于粒子熵的探索（APT, Liu & Abbeel, 2021b）
- **知识驱动方法**：基于预测误差的探索（RND, Burda et al., 2019）
- **能力驱动方法**：基于互信息的技能发现（CIC, Laskin et al., 2022; BeCL, Yang et al., 2023; CeSD, Bai et al., 2024）

与 CeSD 的关键区别在于：CeSD 的多样性正则化在技能状态分布不再重叠时失效（其奖励 $r_i^{reg} = \frac{1}{|\mathbb{S}_i^{pe} - \mathbb{S}_i^{clu}| + \lambda}$ 趋于零），而 AMPED 的 AnInfoNCE 损失随分布距离单调增加。与 ComSD 的区别在于：AMPED 显式解决探索与多样性梯度之间的冲突，而非简单加权求和。

**局限性**：
- 总奖励仍使用启发式线性组合 $r_{total} = r_{diversity} + \alpha r_{entropy} + \beta r_{rnd}$，需要手动调整超参数 $\alpha$ 和 $\beta$。
- PCGrad 不保证保留原始目标，仅保证收敛到帕累托集（Liu et al., 2021）。
- 梯度冲突的程度高度依赖于任务：Jaco 域的冲突比例远低于 Walker 和 Quadruped。
- 技能数量是固定的超参数，在不同环境下并非最优。
- 技能选择器在稀疏奖励场景下学习困难，其价值估计不稳定，导致次优选择。

**开放问题**：
- 如何设计自适应机制来动态调整 $\alpha$ 和 $\beta$，避免手动调参？
- 如何将梯度手术扩展到更多目标（如三个以上）的优化场景？
- 如何根据环境特性自动确定最优技能数量？
- 如何改进技能选择器以在稀疏奖励场景下更稳定地学习？
- 环境结构如何影响探索-多样性梯度交互，以及如何使 AMPED 适应不同环境？



## 原文 PDF

![[paperPDFs/ICLR_2026/AMPED_Adaptive_Multi_objective_Projection_for_balancing_Exploration_and_skill_Diversification.pdf]]
