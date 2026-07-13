---
title: "Why DPO is a Misspecified Estimator and How to Fix It"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Why_DPO_is_a_Misspecified_Estimator_and_How_to_Fix_It.pdf
project_link: null
code_link: null
openreview_forum_id: btEiAfnLsX
aliases:
- WDIMEHFI
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "根本原因在于参数化策略类无法表达任意奖励函数，即 r* 不属于隐式奖励集合 R^β。DPO的投影结果会因偏好对计数 n_{s,a,a'} 的变化而剧烈波动，从而丧失与两阶段RLHF的等价性。通过引入位于策略梯度矩阵零空间中的辅助变量 δ，可以弥补流形的表达能力不足，使优化方向更接近RLHF解。"
primary_logic: "DPO在参数化策略下的等效性建立在一个错误设定的最大似然估计之上；其局部几何分析表明，隐式奖励流形的线性近似为策略对数梯度矩阵的列空间，而RLHF局部解则对应一个更广的等价类。基于这一洞察，AuxDPO通过添加受控的零空间自由度来修正DPO的投影方向，从而在理论和实验上缓解误设问题。"
claims:
- "DPO损失最小化等价于真实奖励函数 r* 到隐式奖励流形的加权KL投影（命题1），当 r* 不可实现时会导致误设估计。"
- "在一个3响应、1维参数的示例中，DPO因误设投影而导致偏好顺序反转和期望奖励下降（命题3），且对偏好对计数高度敏感。"
- "两阶段RLHF的局部二次近似导出一个与策略参数相关的奖励等价类，其最小范数代表恰好对应DPO的线性化隐式奖励（命题6/7），为AuxDPO提供了几何依据。"
- "AuxDPO在多个LLM对齐基准（RewardBench V2、MMLU-PRO）上，无论域内还是域外设置，均一致超越DPO、IPO和DPOP，证实了其实际价值。"
---

# Why DPO is a Misspecified Estimator and How to Fix It

> [!tip] 核心洞察
> DPO在参数化策略下的等效性建立在一个错误设定的最大似然估计之上；其局部几何分析表明，隐式奖励流形的线性近似为策略对数梯度矩阵的列空间，而RLHF局部解则对应一个更广的等价类。基于这一洞察，AuxDPO通过添加受控的零空间自由度来修正DPO的投影方向，从而在理论和实验上缓解误设问题。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DPO为何是一个错误设定的估计器及其修正方法 |
| 英文题名 | Why DPO is a Misspecified Estimator and How to Fix It |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=btEiAfnLsX) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | AuxDPO |
| Dataset | MMLU-PRO (ID), MMLU-PRO (OOD), RewardBench V2 (ID), RewardBench V2 (OOD) |

> [!tip] 效果简介
> - MMLU-PRO (ID) 上，Percentage change in mean accuracy vs. base policy 为 63.26% (AuxDPO)，对比 57.14% (DPO)，变化 +6.12%。
> - MMLU-PRO (OOD) 上，Percentage change in mean accuracy vs. base policy 为 14.28% (AuxDPO)，对比 8.16% (DPO)，变化 +6.12%。
> - RewardBench V2 (ID) 上，Percentage change in mean accuracy vs. base policy 为 66.72% (AuxDPO)，对比 56.01% (DPO)，变化 +10.71%。

## 概要

DPO（Rafailov et al., 2023）通过将偏好学习转化为策略优化问题，省去了两阶段RLHF中显式奖励建模的环节，但其理论等价性建立在表格策略类（即策略可表达任意概率分布）的前提之上。当策略由参数化模型（如LLM）表示时，该等价性不再成立。

本文的核心发现是：**DPO本质上求解了一个统计误设的估计问题**。具体而言，DPO损失的最小化等价于将真实奖励函数 $r^*$ 以加权KL散度的方式投影到策略类所诱导的隐式奖励流形 $\mathcal{R}^\beta$ 上（命题1）。当 $r^*$ 不在此低维流形内——即奖励函数“不可实现”时——该投影严重依赖于偏好数据的采样频率 $n_{s,a,a'}$，可能导致偏好顺序反转、期望奖励下降等失效模式（命题3，Figure 2）。

基于这一洞察，本文提出 **AuxDPO**：在DPO的sigmoid项中引入辅助变量 $\delta$，并通过规范项强制 $\delta$ 位于策略梯度矩阵的零空间中，从而弥补隐式奖励流形的表达能力不足（Figure 1, Figure 3）。该方法在局部线性近似的框架下，将优化方向修正至更接近两阶段RLHF的解。

实验表明，AuxDPO在MMLU-PRO和RewardBench V2上，无论是域内（ID）还是域外（OOD）设置，均一致超越DPO、IPO（Azar et al., 2023）和DPOP（Pal et al., 2024）。以Llama3.1-8B为例，AuxDPO在RewardBench V2的OOD设置下相对基策略提升32.44%，而DPO仅提升14.31%（Table 1）。



### 两阶段RLHF与DPO的等价性承诺

大语言模型对齐的标准范式是两阶段RLHF：先训练一个奖励模型来捕捉人类偏好，再通过强化学习微调策略以最大化该奖励，同时约束策略与参考模型之间的KL散度。这一过程形式化为

$$
\max_{\pi} \mathbb{E}_{s \sim \rho, a \sim \pi(\cdot|s)} [r_{\phi}(s,a)] - \beta D_{\mathrm{KL}}(\pi(\cdot|s) || \pi_{\mathrm{ref}}(\cdot|s)),
$$

其中 $\beta$ 控制KL惩罚的强度。两阶段流程在工程上繁琐且不稳定，因此**DPO**（Rafailov et al., 2023）的提出具有里程碑意义：它声称在表格策略类下，可以直接从偏好数据中优化策略，而无需显式训练奖励模型或执行RL。DPO的核心构件是**隐式奖励函数**

$$
r_{\theta}^{\beta}(s, a) := \beta \log \frac{\pi_{\theta}(a \mid s)}{\pi_{\theta_0}(a \mid s)},
$$

它由当前策略 $\pi_\theta$ 与基策略 $\pi_{\theta_0}$ 的对数比直接导出。在表格情形下，最优策略与潜奖励之间存在闭式关系，DPO因此被认为与两阶段RLHF等价。

### 参数化策略下的误设问题

然而，当策略类为参数化（即非表格）时，这一等价性不再成立。本文揭示了一个根本性的瓶颈：**DPO隐含地求解了一个错误设定的统计估计问题**。真实奖励函数 $r^*$ 往往无法被策略所诱导的隐式奖励流形 $\mathcal{R}^\beta$ 所表达——即 $r^* \notin \mathcal{R}^\beta$。此时，DPO损失的最小化等价于将 $r^*$ 以加权KL散度的方式投影到该低维流形上：

$$
r_{\theta_{\text{DPO}}}^{\beta} = \arg\min_{r \in \mathcal{R}^{\beta}} \sum_{s,a,a'} n_{s,a,a'} \, d_{\text{KL}}\big( p_{s,a,a'}^{\text{BTL}}(r^*) \,\|\, p_{s,a,a'}^{\text{BTL}}(r) \big),
$$

其中 $n_{s,a,a'}$ 是偏好对 $(s, a, a')$ 在数据中的出现频次。这一投影的致命缺陷在于：**它严重依赖于偏好数据的采样频率**。当 $n_{s,a,a'}$ 的分布发生变化时，投影结果会剧烈波动，导致偏好顺序反转、期望奖励下降等失效模式。在一个3响应、1维参数的示例中（Figure 2），DPO因误设投影而将偏好顺序完全颠倒，且对偏好对计数高度敏感。

### 局部几何分析与现有方法的不足

对隐式奖励流形在基策略附近做一阶泰勒展开，可以揭示其局部线性结构：

$$
r_{\theta}^{\beta} \approx \beta \nabla \log \pi_{\theta_0}(a \mid s)^\top (\theta - \theta_0).
$$

这意味着隐式奖励的局部变化被限制在策略对数梯度矩阵 $A_{\theta_0}$ 的列空间中。相比之下，两阶段RLHF的局部二次近似导出了一个更广的**奖励等价类** $R_{\text{eq}}^\beta(\theta^*)$：所有能产生相同最优策略 $\pi_{\theta^*}$ 的奖励函数构成的集合。DPO的投影只能触及该等价类中的一个特定点（即最小Mahalanobis范数代表），而无法覆盖整个等价类。

现有的改进方法如**IPO**（Azar et al., 2023）和**DPOP**（Pal et al., 2024）虽然针对DPO的某些失效模式进行了修补，但均未从统计估计误设的根本原因入手，因此无法系统性地解决投影方向偏差的问题。

### 本文动机

基于上述洞察，本文提出**AuxDPO**，其核心思路是：通过在DPO损失中引入位于 $A_{\rho,\theta_0}$ 零空间中的辅助变量 $\delta$，弥补隐式奖励流形的表达能力不足，使优化方向更接近两阶段RLHF的真实解。这一设计从几何上修正了DPO的错误投影，将KL投影推入正确的奖励等价类中。



## 核心方法与创新机理

本文的核心创新在于从**统计估计的误设（misspecification）**角度重新审视DPO，并基于局部几何洞察提出**AuxDPO**算法，通过引入受控的辅助自由度来修正DPO的投影偏差。

### 根本瓶颈的重新定位：从等价性到误设估计

DPO的原始推导依赖于表格策略类下奖励与策略之间的闭式等价关系：

$$ \pi_{\theta^*}(a | s) = \frac{1}{Z^*(s)} \pi_{\theta_0}(a | s) \exp(r^*(s, a) / \beta) $$

然而，当策略类为参数化（非表格）时，这一等价性不再成立。本文指出，**DPO本质上是在求解一个错误设定的最大似然估计问题**：真实奖励函数 $r^*$ 往往无法被策略参数所诱导的隐式奖励流形 $\mathcal{R}^\beta$ 所表达。DPO损失最小化等价于将 $r^*$ 以加权KL散度的方式投影到该低维流形上（命题1）：

$$ r_{\theta_{DPO}}^{\beta} = \arg\min_{r \in \mathcal{R}^{\beta}} \sum_{s,a,a'} n_{s,a,a'} d_{KL}\big( p_{s,a,a'}^{\mathrm{BTL}}(r^*) || p_{s,a,a'}^{\mathrm{BTL}}(r) \big) $$

该投影的权重由偏好数据的采样频率 $n_{s,a,a'}$ 决定，导致DPO的解对偏好对计数高度敏感，可能引发**偏好反转**和**期望奖励下降**等失效模式。

### 局部几何洞察：RLHF等价类与DPO线性化

为理解DPO偏离两阶段RLHF解的根本原因，本文对RLHF目标在基策略 $\pi_{\theta_0}$ 附近进行局部二次近似：

$$ J(\theta; r^*) \approx \mathbb{E}_{\rho, \pi_{\theta_0}}[r^*(s,a)] + (\theta - \theta_0)^\top A_{\rho,\theta_0} r^* - \frac{\beta}{2} (\theta - \theta_0)^\top F_{\rho,\theta_0} (\theta - \theta_0) $$

其中 $A_{\rho,\theta_0}$ 为加权对数梯度矩阵，$F_{\rho,\theta_0}$ 为Fisher信息矩阵。由此可导出RLHF最优参数的一阶条件：

$$ A_{\rho,\theta_0} r^* = \beta F_{\rho,\theta_0} (\theta^* - \theta_0) $$

这一条件揭示了一个关键结构：**所有满足 $A_{\rho,\theta_0} r = \beta F_{\rho,\theta_0} (\theta - \theta_0)$ 的奖励向量构成RLHF等价类 $R_{eq}^\beta(\theta)$**，它们诱导相同的策略参数 $\theta$。而DPO的隐式奖励流形局部线性近似为 $A_{\theta_0}^\top$ 的列空间 $\mathcal{C}(A_{\theta_0}^\top)$，其最小Mahalanobis范数代表恰好对应DPO的线性化隐式奖励（命题7）。这意味着**DPO只能到达隐式奖励流形上的点，而RLHF解则位于更广的等价类中**——当 $r^*$ 不可实现时，DPO的投影方向必然偏离RLHF解。

### 核心机制：辅助变量补偿零空间自由度

基于上述几何洞察，真实奖励 $r^*$ 与DPO最优隐式奖励 $r_{\theta^*}^\beta$ 之间的差异必然位于 $A_{\rho,\theta_0}$ 的零空间 $\mathcal{N}(A_{\rho,\theta_0})$ 中。AuxDPO的核心创新在于**显式引入辅助变量 $\delta$ 来搜索该零空间**，从而补偿隐式奖励流形的表达能力不足。

具体而言，AuxDPO在DPO的sigmoid logit中注入辅助变量：

$$ r_{\theta}^{\beta}(s, a_w) - r_{\theta}^{\beta}(s, a_l) + \delta(s, a_w) - \delta(s, a_l) $$

并通过惩罚项强制 $\delta$ 位于 $A_{\rho,\theta_0}$ 的零空间：

$$ \lambda \left\| \frac{1}{2n}\sum_{i=1}^{n} \left( \delta_w \nabla \log \pi_{\theta_0}(a_w^{(i)} \mid s^{(i)}) + \delta_l \nabla \log \pi_{\theta_0}(a_l^{(i)} \mid s^{(i)}) \right) \right\|^2 $$

其中 $\lambda > 0$ 为控制零空间约束强度的超参数。完整的经验AuxDPO损失为：

$$ \mathcal{L}_{\mathcal{D}}(\theta, \delta) = -\frac{1}{n}\sum_{i=1}^{n} \log \sigma\left(r_{\theta}^{\beta}(s^{(i)}, a_w^{(i)}) - r_{\theta}^{\beta}(s^{(i)}, a_l^{(i)}) + \delta(s^{(i)}, a_w^{(i)}) - \delta(s^{(i)}, a_l^{(i)})\right) + \lambda \left\| \frac{1}{2n}\sum_{i=1}^{n} \left( \delta_w \nabla \log \pi_{\theta_0}(a_w^{(i)} \mid s^{(i)}) + \delta_l \nabla \log \pi_{\theta_0}(a_l^{(i)} \mid s^{(i)}) \right) \right\|^2 $$

### 与基线方法的关键差异

与DPO相比，AuxDPO的改动集中在两个slot：

| 改动项 | DPO（基线） | AuxDPO（本文） |
|--------|------------|----------------|
| 奖励差异项 | $r_{\theta}^{\beta}(s, a_w) - r_{\theta}^{\beta}(s, a_l)$ | $r_{\theta}^{\beta}(s, a_w) - r_{\theta}^{\beta}(s, a_l) + \delta_w - \delta_l$ |
| 额外约束项 | 无 | $\lambda \| A_{\rho,\theta_0} \delta \|^2$，强制 $\delta$ 位于零空间 |

与IPO和DPOP等改进方法不同，AuxDPO并非通过修改损失函数形式或添加正则化来缓解特定失效模式，而是**从误设估计的几何本质出发，系统性地扩展了优化空间**，使投影方向能够被推入正确的RLHF等价类。这一设计使得AuxDPO在理论上更接近两阶段RLHF的解，并在实验中一致超越了DPO、IPO和DPOP。



本文的核心贡献在于揭示DPO的参数化误设本质，并基于此提出AuxDPO修正框架。整体pipeline可概括为“诊断—几何建模—修正”三步。

**问题诊断：DPO是误设估计器。** 在表格策略类下，DPO与两阶段RLHF等价；但当策略类为参数化（非表格）时，真实奖励函数 $r^*$ 往往无法被策略诱导的隐式奖励流形 $\mathcal{R}^\beta$ 所实现。论文证明（命题1），DPO损失最小化等价于将 $r^*$ 以加权KL散度的方式投影到该低维流形上：
$$r_{\theta_{DPO}}^{\beta} = \arg\min_{r \in \mathcal{R}^{\beta}} \sum_{s,a,a'} n_{s,a,a'} d_{KL}\big( p_{s,a,a'}^{\mathrm{BTL}}(r^*) || p_{s,a,a'}^{\mathrm{BTL}}(r) \big)$$
该投影严重依赖于偏好数据的采样频率 $n_{s,a,a'}$，当 $r^* \notin \mathcal{R}^\beta$ 时，DPO退化为一个无理论保证的误设估计器，可能导致偏好反转和期望奖励下降（命题3）。

**几何建模：局部线性化揭示修正空间。** 在基策略 $\pi_{\theta_0}$ 附近对隐式奖励做一阶泰勒展开，得到局部线性近似：
$$r_{\theta}^{\beta}(s,a) \approx \beta \nabla \log \pi_{\theta_0}(a|s)^\top (\theta - \theta_0)$$
这意味着隐式奖励流形的局部结构为策略对数梯度矩阵 $A_{\theta_0}$ 的列空间 $\mathcal{C}(A_{\theta_0}^\top)$。另一方面，对RLHF目标做局部二次近似，可导出奖励等价类 $\mathcal{R}_{eq}^\beta(\theta)$ ——所有能诱导同一最优策略参数 $\theta$ 的奖励函数集合。关键的几何洞察（命题7）是：DPO的线性化隐式奖励恰好是该等价类中具有最小马氏范数的代表元，而真正的RLHF解可能位于等价类中的其他位置。两者之间的差距位于 $A_{\rho,\theta_0}$ 的零空间中。

**AuxDPO修正：引入零空间辅助变量。** 基于上述几何洞察，AuxDPO在DPO的sigmoid项中引入辅助变量 $\delta \in \mathbb{R}^{2n}$（每个偏好对持有两个标量），并联合优化 $\theta$ 和 $\delta$：
$$\mathcal{L}_{\mathcal{D}}(\theta, \delta) = -\frac{1}{n}\sum_{i=1}^{n} \log \sigma\left(r_{\theta}^{\beta}(s^{(i)}, a_w^{(i)}) - r_{\theta}^{\beta}(s^{(i)}, a_l^{(i)}) + \delta_w - \delta_l\right) + \lambda \left\| \frac{1}{2n}\sum_{i=1}^{n} \left( \delta_w \nabla \log \pi_{\theta_0}(a_w^{(i)}|s^{(i)}) + \delta_l \nabla \log \pi_{\theta_0}(a_l^{(i)}|s^{(i)}) \right) \right\|^2$$
其中惩罚项 $\lambda \|A_{\rho,\theta_0} \delta\|^2$ 强制 $\delta$ 位于 $A_{\rho,\theta_0}$ 的零空间，确保辅助变量仅在“不可表达”的方向上提供额外自由度，从而将KL投影的方向推入RLHF等价类。

**模块关系与数据流总结：**
1. **策略模型 $\pi_\theta$**：参数化语言模型，输出条件概率分布。
2. **隐式奖励计算**：通过 $r_{\theta}^{\beta}(s,a) = \beta \log(\pi_{\theta}(a|s)/\pi_{\theta_0}(a|s))$ 将策略差异转化为标量奖励。
3. **辅助变量 $\delta$**：每个偏好对持有两个标量，扩展奖励空间的表达能力，弥补隐式流形的维度不足。
4. **AuxDPO损失与联合训练**：在DPO的二元交叉熵损失中加入 $\delta$ 差异项，并施加零空间惩罚，联合优化 $\theta$ 和 $\delta$。

该框架的核心优势在于：不改变基础模型架构，仅在损失函数层面引入可控的自由度，以理论驱动的方式修正DPO的误设投影方向。



### DPO的统计实质：加权KL投影

DPO的根本问题在于它隐含地求解了一个错误设定的统计估计问题。当策略类为参数化（非表格）时，真实奖励函数 $r^*$ 往往无法被策略所诱导的隐式奖励流形 $\mathcal{R}^\beta$ 实现。此时，DPO损失最小化等价于将 $r^*$ 以加权反向KL散度的方式投影到该低维流形上：

$$r_{\theta_{\text{DPO}}}^{\beta} = \arg\min_{r \in \mathcal{R}^{\beta}} \sum_{s,a,a'} n_{s,a,a'} d_{\mathrm{KL}}\big( p_{s,a,a'}^{\mathrm{BTL}}(r^*) \| p_{s,a,a'}^{\mathrm{BTL}}(r) \big)$$

其中 $n_{s,a,a'}$ 是偏好对 $(s, a, a')$ 的采样计数，$p^{\mathrm{BTL}}$ 为Bradley-Terry偏好概率。该投影严重依赖于偏好数据的采样频率，当 $r^* \notin \mathcal{R}^\beta$ 时，DPO的解不具备任何理论保证——可能导致偏好顺序反转或期望奖励下降。

### 隐式奖励流形的局部线性结构

隐式奖励函数定义为策略对数比：

$$r_{\theta}^{\beta}(s, a) := \beta \log \frac{\pi_{\theta}(a \mid s)}{\pi_{\theta_0}(a \mid s)}$$

在基策略 $\pi_{\theta_0}$ 附近进行一阶泰勒展开，得到其局部线性近似：

$$r_{\theta}^{\beta} \approx \beta \nabla \log \pi_{\theta_0}(a \mid s)^\top (\theta - \theta_0)$$

这意味着隐式奖励流形 $\mathcal{R}^\beta$ 的局部线性近似为策略对数梯度矩阵 $A_{\theta_0}$ 的列空间 $\mathcal{C}(A_{\theta_0}^\top)$。DPO的投影被限制在这个低维子空间内，表达能力不足是误设的几何根源。

### RLHF目标的局部二次近似与奖励等价类

两阶段RLHF的目标函数在基策略附近的二阶近似为：

$$J(\theta; r^*) \approx \mathbb{E}_{\rho, \pi_{\theta_0}}[r^*(s,a)] + (\theta - \theta_0)^\top A_{\rho,\theta_0} r^* - \frac{\beta}{2} (\theta - \theta_0)^\top F_{\rho,\theta_0} (\theta - \theta_0)$$

其中 $A_{\rho,\theta_0}$ 是加权对数梯度矩阵，$F_{\rho,\theta_0}$ 是Fisher信息矩阵。由一阶最优条件可得最优策略参数的闭式关系：

$$\theta^* = \theta_0 + \frac{1}{\beta} F_{\rho,\theta_0}^\dagger A_{\rho,\theta_0} r^*$$

由此定义RLHF奖励等价类——所有能诱导出相同最优策略参数 $\theta$ 的奖励向量集合：

$$\mathcal{R}_{\text{eq}}^{\beta}(\theta) = \{ r \in \mathbb{R}^m : A_{\rho,\theta_0} r = \beta F_{\rho,\theta_0} (\theta - \theta_0) \}$$

关键洞察在于：该等价类中具有最小Mahalanobis范数的代表元恰好是DPO隐式奖励的局部线性化 $r_{\theta}^{\beta} = \beta A_{\theta_0}^\top (\theta - \theta_0)$。这揭示了DPO的解与RLHF最优解之间的差距恰好位于 $A_{\rho,\theta_0}$ 的零空间中。

### AuxDPO：引入零空间自由度修正投影

基于上述几何洞察，AuxDPO在DPO的sigmoid项中引入辅助变量 $\delta \in \mathbb{R}^{2n}$（每个偏好对持有两个标量），并强制 $\delta$ 位于 $A_{\rho,\theta_0}$ 的零空间，从而扩展奖励空间的表达能力。经验AuxDPO损失为：

$$\mathcal{L}_{\mathcal{D}}(\theta, \delta) = -\frac{1}{n}\sum_{i=1}^{n} \log \sigma\left(r_{\theta}^{\beta}(s^{(i)}, a_w^{(i)}) - r_{\theta}^{\beta}(s^{(i)}, a_l^{(i)}) + \delta(s^{(i)}, a_w^{(i)}) - \delta(s^{(i)}, a_l^{(i)})\right) + \lambda \left\| \frac{1}{2n}\sum_{i=1}^{n} \left( \delta_w \nabla \log \pi_{\theta_0}(a_w^{(i)} \mid s^{(i)}) + \delta_l \nabla \log \pi_{\theta_0}(a_l^{(i)} \mid s^{(i)}) \right) \right\|^2$$

其中：
- **奖励差异项**：在原始 $r_{\theta}^{\beta}(s, a_w) - r_{\theta}^{\beta}(s, a_l)$ 基础上增加 $\delta_w - \delta_l$，弥补流形表达能力不足；
- **零空间惩罚项**：$\lambda \|A_{\rho,\theta_0} \delta\|_2^2$ 强制辅助变量位于策略梯度矩阵的零空间，确保优化方向更接近RLHF解；
- **联合优化**：同时对策略参数 $\theta$ 和辅助变量 $\delta$ 进行最小化，$\lambda > 0$ 为控制零空间约束强度的超参数。

该设计的核心机制是：真实奖励 $r^*$ 与DPO最优隐式奖励 $r_{\theta^*}^{\beta}$ 的差值恰好属于 $A_{\rho,\theta_0}$ 的零空间，即 $r^* = r_{\theta^*}^{\beta} + \delta$，其中 $\delta \in \mathcal{N}(A_{\rho,\theta_0})$。AuxDPO通过显式搜索该零空间方向，将DPO的错误投影推入正确的RLHF等价类。



## 实验与关键发现

### 主实验结果

论文在三个不同规模的模型（Llama3.1-8B、Llama3.2-1B、Qwen3-0.6B）上评估了AuxDPO与DPO（Rafailov et al., 2023）、IPO（Azar et al., 2023）和DPOP（Pal et al., 2024）的性能。所有方法使用相同的训练数据（UltraFeedback的二进制化版本）和相同的基准模型，在域内（ID）和域外（OOD）两种设置下进行测试。评估基准为MMLU-PRO和RewardBench V2，指标为相对于基准策略的准确率百分比变化。

**表1** 汇总了各方法在三个模型上的表现。以Llama3.1-8B为例，AuxDPO在所有四个设置上均取得最优结果：

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_btEiAfnLsX/figures/004_Table_1.jpg]]
*Table 1: Algorithm comparison. Values show percentage change in mean accuracy relative to the base policy, across MMLU-PRO and REWARDBENCH V2 under in-domain (ID) and out-of-domain (OOD) settings. Best gains are in bold, second-best are underlined. Accuracies which degrade from the base policy are marked in red*

- **MMLU-PRO (ID)**：AuxDPO提升63.26%，DPO提升57.14%（**+6.12%**）
- **MMLU-PRO (OOD)**：AuxDPO提升14.28%，DPO提升8.16%（**+6.12%**）
- **RewardBench V2 (ID)**：AuxDPO提升66.72%，DPO提升56.01%（**+10.71%**）
- **RewardBench V2 (OOD)**：AuxDPO提升32.44%，DPO提升14.31%（**+18.13%**）

在RewardBench V2的OOD设置上，AuxDPO相对DPO的增益尤为显著（+18.13%），表明其缓解误设问题后对分布外偏好的泛化能力更强。在Llama3.2-1B和Qwen3-0.6B上，AuxDPO同样在多数设置下取得最优或次优结果。值得注意的是，DPO在某些OOD设置下出现准确率退化（表中以红色标记），而AuxDPO未出现此类退化现象。

**表2** 给出了Llama3.1-8B在MMLU-PRO各学科上的详细准确率。在OOD设置下，AuxDPO的总体准确率为39.26%，DPO为27.06%；在ID设置下，AuxDPO为51.95%，DPO为46.60%。AuxDPO在大多数子学科上领先，且未出现任何学科上的性能退化，这与理论分析中DPO因误设投影导致偏好反转的预测一致。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_btEiAfnLsX/figures/005_Table_2.jpg]]
*Table 2: correct answer. We use ULTRAFEEDBACK (Cui et al., 2024) as our training dataset. Specifically, its pre-processed and binarized version (Dong et al., 2024), which generates higher-quality reward models (Wang et al., 2024a; Xiong et al., 2024; Banerjee and Gopalan, 2024). Table 2: Per-subject accuracies (top 10 subjects alphabetically) and overall win-rates across baseline (Llama3.1- 8B) and preference optimization methods. For each method, two settings are shown: OOD (cross-domain transfer) and ID (in-domain learning), along with the reported results. In each row, the best accuracy is shown in bold, and the second-best is underlined. Accuracies which degrade from the base policy are marked i...*

### 消融与失败模式分析

论文未提供独立的消融实验章节，但通过理论分析和示例揭示了DPO的核心失败模式：

**偏好反转与计数敏感性**：在3响应、1维参数的示例（命题3）中，当真实奖励函数 $r^*$ 不在隐式奖励流形 $\mathcal{R}^\beta$ 内时，DPO的加权KL投影结果严重依赖于偏好对计数 $n_{s,a,a'}$。具体地，DPO学到的隐式奖励近似为 $r_\theta^\beta \approx [\alpha, -\alpha, 0]$，导致对响应 $a_1$ 和 $a_2$ 的偏好顺序与真实奖励 $r^*$ 给出的顺序完全相反。这一反转的原因是：隐式奖励流形在局部被近似为策略对数梯度矩阵的列空间 $\mathcal{C}(A_{\theta_0}^\top)$，其维度远低于完整奖励空间，DPO被迫将 $r^*$ 投影到该低维流形上，而投影方向由偏好数据的采样频率加权决定。

**期望奖励下降**：在同一示例中，DPO优化后的策略在真实奖励函数下的期望奖励低于基准策略，表明误设投影不仅改变了偏好排序，还导致策略质量的实际退化。

AuxDPO通过引入位于 $A_{\rho,\theta_0}$ 零空间中的辅助变量 $\delta$，扩展了奖励空间的表达能力，使优化方向能够偏离DPO的强制投影路径，从而将解推向RLHF等价类 $\mathcal{R}_{eq}^\beta(\theta^*)$。超参数 $\lambda$ 控制零空间约束的强度，需要在表达能力和数值稳定性之间权衡。

### 局限性

实验仅在有限规模模型（≤8B）和两个基准上验证，未在大规模生产级模型上测试。此外，AuxDPO引入的辅助变量数量与训练偏好对数量成正比（$2n$），当数据集规模较大时会增加计算和内存开销，且 $\lambda$ 需手动调节。理论分析依赖大 $\beta$ 假设下的局部线性近似，在全局行为和实际微调场景（$\beta$ 通常较小）中的适用性有待进一步验证。



## 定位与知识库关联

### 与直接偏好优化方法的谱系关系

AuxDPO 的核心动机源于对 DPO（**DPO**, Rafailov et al., 2023）在参数化策略类下统计误设问题的系统性诊断。DPO 的理论等价性建立在表格策略类的闭式关系之上——最优策略可表示为 $\pi_{\theta^*}(a|s) \propto \pi_{\theta_0}(a|s) \exp(r^*(s,a)/\beta)$，从而允许将偏好学习重写为仅依赖策略的损失函数。然而，当策略类为参数化模型（如神经网络）时，这一等价性不再成立：真实的奖励函数 $r^*$ 往往无法被策略所诱导的隐式奖励流形 $\mathcal{R}^\beta$ 所表达。

本文通过命题1揭示了 DPO 的统计本质——其损失最小化等价于将真实奖励函数 $r^*$ 以加权 KL 散度的方式投影到隐式奖励流形上：
$$r_{\theta_{DPO}}^{\beta} = \arg\min_{r \in \mathcal{R}^{\beta}} \sum_{s,a,a'} n_{s,a,a'} d_{KL}\big(p_{s,a,a'}^{\mathrm{BTL}}(r^*) || p_{s,a,a'}^{\mathrm{BTL}}(r)\big)$$
该投影的权重由偏好数据的采样频率 $n_{s,a,a'}$ 决定，这意味着 DPO 的解会随偏好对计数的变化而剧烈波动，从而丧失与两阶段 RLHF 的等价性。在3响应、1维参数的示例中（命题3），DPO 因误设投影而导致偏好顺序反转和期望奖励下降，显式地展示了这一失效模式。

相较于后续的改进方法，**IPO**（Azar et al., 2023）和 **DPOP**（Pal et al., 2024）主要从损失函数设计或正则化角度缓解 DPO 的特定失效现象，但未从统计估计的根本机制上解决问题。AuxDPO 的独特贡献在于：通过局部几何分析揭示了隐式奖励流形的线性近似为策略对数梯度矩阵 $A_{\theta_0}$ 的列空间，而 RLHF 局部解则对应一个更广的等价类 $R_{eq}^\beta(\theta) = \{r : A_{\rho,\theta_0} r = \beta F_{\rho,\theta_0} (\theta - \theta_0)\}$。基于这一洞察，AuxDPO 在 DPO 的 sigmoid 项中引入位于 $A_{\rho,\theta_0}$ 零空间中的辅助变量 $\delta$，从而扩展了奖励空间的表达能力，使优化方向更接近 RLHF 解。

### 适用边界与理论局限

AuxDPO 的理论分析主要依赖于大 $\beta$ 条件下的局部线性近似——即策略仅允许在基策略附近局部偏离。该近似下的核心结论包括：RLHF 目标的局部二次近似导出了最优策略参数与潜奖励的闭式关系 $\theta^* = \theta_0 + (1/\beta) F_{\rho,\theta_0}^\dagger A_{\rho,\theta_0} r^*$，以及 DPO 的线性化隐式奖励恰好是 RLHF 等价类中最小马氏范数代表（命题7）。然而，当 $\beta$ 较小、策略偏离较远时，高阶误差的影响尚未得到理论刻画，全局行为的适用性需要进一步验证。

当前分析框架建立在 Bradley-Terry 偏好模型之上。若真实偏好生成过程偏离 BTL 假设（例如存在非传递性偏好或上下文依赖），DPO 的误设结论和 AuxDPO 的修正机制可能不再成立。此外，AuxDPO 引入的辅助变量数量与训练偏好对数量（$2n$）成正比，当数据集规模较大时会增加额外的计算和内存开销，且超参数 $\lambda$ 需要手动调节以平衡零空间约束的强度。

### 开放问题

1. **非 BTL 偏好模型下的推广**：在一般偏好模型下，DPO 的误设特点如何变化？AuxDPO 框架能否自然地推广到更广泛的偏好结构？
2. **自适应正则化策略**：能否设计一种更加自适应的正则化机制，使得辅助变量 $\delta$ 的作用强度根据数据分布自动调整，而非依赖固定的超参数 $\lambda$？
3. **高阶误差的影响**：局部线性近似中的高阶误差在非大 $\beta$ 的实际微调场景下对 AuxDPO 的性能影响有多大？是否需要引入二阶修正？
4. **非光滑策略类的适用性**：当策略类为更复杂的非光滑模型（例如离散提示学习或基于检索的策略）时，该几何框架是否仍然有效？
5. **与两阶段 RLHF 的系统权衡**：AuxDPO 相比两阶段 RLHF 在资源消耗和最终策略质量上的权衡如何？目前缺乏系统的计算开销对比实验。
6. **大规模模型验证**：当前实验仅在有限规模的模型（≤8B）和两个基准（MMLU-PRO、RewardBench V2）上进行，未在大规模生产级模型上验证方法的可扩展性。



## 原文 PDF

![[paperPDFs/ICLR_2026/Why_DPO_is_a_Misspecified_Estimator_and_How_to_Fix_It.pdf]]
