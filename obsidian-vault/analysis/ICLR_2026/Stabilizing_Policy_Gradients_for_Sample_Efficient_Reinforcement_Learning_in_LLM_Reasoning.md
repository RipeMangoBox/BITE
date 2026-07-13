---
title: "Stabilizing Policy Gradients for Sample-Efficient Reinforcement Learning in LLM Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Stabilizing_Policy_Gradients_for_Sample_Efficient_Reinforcement_Learning_in_LLM_Reasoning.pdf
project_link: null
code_link: null
openreview_forum_id: iIvPuXoDs1
aliases:
- CAPOC
- SPGSERLLR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "基于二阶曲率信息（Hessian和Fisher矩阵）的样本过滤机制：利用计算高效的近似模型估计每次更新可能导致的目标和策略分布偏移，拒绝那些引起过大幅度偏移的样本，从而充当局部的信任域约束。"
primary_logic: "利用对二阶优化几何的轻量级近似（last‑layer模型 + 稀疏梯度 + 方向曲率估计）可以实时追踪并预防策略更新中的不稳定移动；通过仅屏蔽少量（<8%）导致异常偏移的token，能够在不牺牲性能的前提下实现激进训练体制下的稳定学习，大幅提升样本效率。"
claims:
- "CAPO在激进更新体制下阻止了策略崩溃，而所有基线方法均发生灾难性失效。"
- "CAPO比标准保守GRPO少用30倍的样本（在MATH上）和9倍的样本（在TEST基准上）。"
- "CAPO的token拒识率峰值约8%，之后持续低于2%，干预极小。"
- "MATH 上 样本效率（达到指定准确度所需训练完成次数） = CAPO"
---

# Stabilizing Policy Gradients for Sample-Efficient Reinforcement Learning in LLM Reasoning

> [!tip] 核心洞察
> 利用对二阶优化几何的轻量级近似（last‑layer模型 + 稀疏梯度 + 方向曲率估计）可以实时追踪并预防策略更新中的不稳定移动；通过仅屏蔽少量（<8%）导致异常偏移的token，能够在不牺牲性能的前提下实现激进训练体制下的稳定学习，大幅提升样本效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 稳定策略梯度以实现大语言模型推理中的样本高效强化学习 |
| 英文题名 | Stabilizing Policy Gradients for Sample-Efficient Reinforcement Learning in LLM Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=iIvPuXoDs1) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Curvature-Aware Policy Optimization (CAPO) |
| Dataset | MATH, TEST (8个基准平均), MATH & TEST |

> [!tip] 效果简介
> - MATH 上，样本效率（达到指定准确度所需训练完成次数） 为 CAPO，对比 GRPO (保守体制)，变化 30× fewer completions。
> - TEST (8个基准平均) 上，样本效率 为 CAPO，对比 GRPO (保守体制)，变化 9× fewer completions。
> - MATH & TEST 上，训练稳定性（策略崩溃情况） 为 CAPO (无崩溃)，对比 GRPO, Dr.GRPO, REINFORCE (激进体制下均崩溃)，变化 CAPO 在基线崩溃后仍稳定学习。

## 概要

在大语言模型（LLM）的推理任务中，使用策略梯度方法进行强化学习微调已成为提升模型能力的核心技术路径。然而，这一范式面临一个根本性瓶颈：优化的非平稳性与梯度估计的高方差导致训练极易失稳。尤其在采用激进学习率和更小批量的高效训练体制下，包括 **GRPO**（Shao et al., 2024）、**Dr.GRPO**（Liu et al., 2025a）和 **REINFORCE**（Williams, 1992）在内的主流基线方法均会发生灾难性的策略崩溃，严重制约了样本效率的进一步提升。

针对这一问题，本文提出 **Curvature-Aware Policy Optimization (CAPO)**，一种基于二阶曲率信息的样本过滤机制。其核心洞见在于：利用对二阶优化几何的轻量级近似——通过仅对LLM最后一层构建梯度、Hessian和Fisher信息矩阵的近似模型，并借助方向曲率估计——可以实时追踪并预防策略更新中的不稳定移动。CAPO据此识别并屏蔽那些会引起目标函数和策略分布大幅偏移的样本，仅在满足局部信任域约束的子集上进行梯度更新，从而在激进训练体制下实现稳定学习。

实验结果表明，CAPO在数学推理基准上展现出显著的样本效率优势：在MATH数据集上，CAPO比标准保守体制下的GRPO少用约30倍的训练完成次数即可达到同等准确率；在涵盖8个基准的TEST平均结果上，样本效率提升约9倍。更重要的是，CAPO在基线方法全部崩溃的激进体制下维持了稳定学习，且其token级干预极小——拒识率峰值约8%，随后持续低于2%。方法还具有通用性：将曲率感知选择引入Dr.GRPO和REINFORCE同样能防止策略崩溃。此外，CAPO的执行时间开销不到总步长的3%，几乎不增加额外计算负担。

CAPO将自身定位于策略梯度方法的稳定化改进，与TRPO等经典信任域方法共享约束更新幅度的思想，但通过轻量级的曲率近似避免了全参数二阶矩阵的物化，使其能够高效应用于大规模语言模型的RL微调场景。



### 大语言模型推理中的强化学习微调

大语言模型（LLM）在数学推理、代码生成等复杂任务上的能力提升，越来越依赖于强化学习（RL）进行策略微调。其核心思路是将LLM的自回归生成过程建模为一个序列决策问题：模型作为策略 $\pi_{\pmb\theta}$，在每个时间步选择下一个token作为动作，目标是最大化期望累计回报

$$J(\pmb\theta) = \mathbb{E}_{\tau \sim \pi_{\pmb\theta}} \Big[ \sum_{t=0}^{T} \gamma^{t} R(s_{t}, a_{t}) \Big]$$

其中轨迹 $\tau$ 由模型自回归生成，奖励 $R$ 通常来自基于规则的正确性验证或奖励模型。策略梯度方法（如 **REINFORCE**（Williams, 1992））通过以下梯度估计来优化该目标：

$$\nabla_{\pmb\theta} J(\pmb\theta) = \mathbb{E}_{\tau \sim \pi_{\pmb\theta}} \left[ \sum_{t=0}^{T} \gamma^{t} \nabla_{\pmb\theta} \log \pi_{\pmb\theta}(a_{t} \mid s_{t}) R(s_{t}, a_{t}) \right]$$

近年来，**GRPO**（Shao et al., 2024）等方法通过引入基于组内标准化的优势估计和KL正则化，在LLM推理任务上取得了显著进展。GRPO的核心优势估计为：

$$\hat{A}^{\mathrm{GRPO}}(s_{t}, a_{t}) = \frac{\hat{R}(\tau) - \bar{R}}{\hat{\sigma}_{R} + \varepsilon}$$

其中 $\bar{R}$ 和 $\hat{\sigma}_{R}$ 分别为同一提示词下多个生成轨迹的回报均值和标准差。这种设计通过组内对比减少了方差，但仍未从根本上解决策略梯度优化的核心困境。

### 核心瓶颈：非平稳优化与策略崩溃

尽管GRPO在保守的训练体制下（较小学习率、较大批处理规模）表现良好，但当尝试提高样本效率而采用更激进的更新体制时——即使用更高学习率和更小批处理规模——所有基线方法均遭遇**灾难性的策略崩溃**。

这一现象的深层原因在于LLM推理任务的RL微调面临两个相互交织的困难：

1. **优化的非平稳性**：LLM的自回归生成使得数据分布随策略更新而不断漂移，违反了监督学习中独立同分布的基本假设。每次策略更新后，模型生成的轨迹分布发生变化，导致后续梯度估计基于一个持续移动的目标。

2. **梯度估计的高方差**：在激进的学习率和小批量设置下，单次更新可能引起策略分布的剧烈偏移。这种偏移通过自回归过程的逐token累积效应被放大，使得模型迅速偏离有效策略空间，表现为准确率断崖式下降。

### 现有方法的局限

面对上述稳定性问题，现有方法主要依赖两种策略，但均存在根本性缺陷：

- **PPO裁剪**：通过对策略比率 $r_{\theta}(s_t, a_t)$ 施加裁剪约束 $\mathrm{clip}(r_{\theta}, 1-\epsilon, 1+\epsilon)$ 来限制单次更新幅度。然而，标准裁剪阈值（$\epsilon=0.2$）在激进体制下完全无法阻止崩溃；更激进的裁剪虽能提升稳定性，却严重损害最终性能，且这种权衡随训练步数增加而恶化（Figure 7）。

- **KL正则化**：通过在目标函数中加入 $\beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{base}})$ 惩罚项来约束策略偏离。但强正则化（$\beta=1.0$）虽能缓解不稳定，却显著降低了模型性能；更关键的是，KL正则化并未消除梯度的无界性，梯度范数仍可能将优化推向不稳定区域（Figure 8）。

这些方法的共同缺陷在于：它们都是**事后约束**——在梯度计算完成后才施加限制，而非在更新发生之前预判并阻止危险的参数移动。这导致它们在激进体制下要么约束不足（策略崩溃），要么约束过度（性能退化），无法同时实现高效与稳定。

### 本文动机：从曲率视角主动预防不稳定性

本文的核心洞察是：策略更新中的不稳定性并非随机现象，而是**可以在更新执行前通过二阶曲率信息进行预测和预防**的。具体而言，一次参数更新 $\Delta\pmb\theta$ 引起的目标函数变化和策略分布偏移，可以分别通过Hessian矩阵和Fisher信息矩阵进行二阶近似：

$$m_H(\Delta\pmb\theta) = \nabla_{\pmb\theta} J(\pmb\theta)^\top \Delta\pmb\theta + \frac{1}{2} \Delta\pmb\theta^\top H(\pmb\theta) \Delta\pmb\theta$$

$$m_F(\Delta\pmb\theta) = \frac{1}{2} \Delta\pmb\theta^\top \boldsymbol{F}(\pmb\theta) \Delta\pmb\theta \approx \bar{D}_{\mathrm{KL}}(\pi_{\pmb\theta} \| \pi_{\pmb\theta+\Delta\pmb\theta})$$

这意味着，如果我们能够**高效地估计这些曲率量**，就可以在参数更新前识别出那些会导致异常大幅偏移的样本，并将其从梯度估计中排除——从而充当一个局部的信任域约束。

基于这一动机，本文提出**Curvature-Aware Policy Optimization (CAPO)**，其核心思路是：构建一个计算高效的二阶曲率近似框架，在每次更新前评估候选样本引起的目标和策略偏移，仅接受满足信任域约束的子集进行梯度累积。这使得CAPO能够在激进的学习体制下保持稳定学习，同时仅屏蔽极少量的token（峰值约8%，随后降至2%以下），以最小的干预代价实现显著的样本效率提升。



## 核心方法与创新机理

CAPO（Curvature‑Aware Policy Optimization）的核心创新在于将**二阶曲率信息**引入策略梯度的样本筛选过程，从而在不改变底层RL目标函数的前提下，实现对策略更新的隐式信任域约束。与现有方法相比，其关键改变体现在以下方面：

### 1. 梯度估计的数据使用方式：从全量更新到曲率感知的样本掩蔽

标准GRPO（Shao et al., 2024）和REINFORCE（Williams, 1992）在每次更新中使用批处理中的**所有**样本进行梯度累积。然而，在激进训练体制（高学习率、小批量）下，这种全量更新极易导致策略崩溃——部分样本引起的目标和策略分布偏移过大，使优化进入不稳定区域。

CAPO改变了这一范式：它基于二阶曲率近似，对每个候选更新子集（如单个token）计算其引起的**目标偏移** $m_H$ 和**策略偏移** $m_F$，并仅接受满足局部信任域约束的子集进行梯度累积：

$$\delta_H \leq m_H(\Delta\psi_i) \leq \delta_H^{\text{high}}, \quad m_F(\Delta\psi_i) \leq \delta_F$$

这一机制本质上是一种**选择性样本掩蔽**：那些会导致过大幅度偏移的样本被拒绝参与梯度更新，从而在激进体制下充当隐式的信任域约束。实验表明，CAPO的token拒识率峰值仅约8%，之后持续低于2%（Figure 5），干预极小但效果显著——在MATH基准上，CAPO比标准保守GRPO少用**30倍**样本即可达到相同准确度（Figure 1, Figure 2）。

### 2. 计算高效的二阶曲率近似

直接计算完整参数空间的Hessian或Fisher信息矩阵在LLM规模下不可行。CAPO通过三个关键设计实现高效近似：

- **Last‑Layer模型**：仅对LLM最后一层的权重矩阵 $\psi$ 构建梯度、Hessian和Fisher近似（公式7‑9），将曲率估计限制在参数子空间内，避免全参数二阶张量的物化。
- **梯度稀疏性利用**：LLM解码通常依赖选择性采样（如top‑k、nucleus sampling），导致梯度天然稀疏——仅少数token具有非零梯度。CAPO利用这一结构显著降低计算复杂度。
- **方向曲率估计**：不显式构建曲率矩阵，而是通过内积运算直接估计更新方向 $\Delta\psi$ 上的目标偏移和策略偏移（公式10），将计算量从矩阵物化降为向量内积。

### 3. 优化器行为建模

CAPO在生成候选更新方向时，模拟了底层LLM优化器（Adam）的实际行为，利用Adam的矩估计（$\hat{p}_t$、$\hat{q}_t$）来规划步长 $\Delta\psi = \alpha \frac{\hat{p}_t}{\sqrt{\hat{q}_t} + \epsilon}$，而非使用简单的SGD步长表示。消融实验（Figure 6）表明，这一设计对方法的通用性至关重要：将曲率感知选择引入Dr.GRPO和REINFORCE时，只有基于Adam的步长表示能防止策略崩溃，而SGD表示在部分变体上失效。

### 4. 与现有信任域方法的本质区别

标准PPO裁剪（$\epsilon = 0.2$）和KL正则化（$\beta$惩罚）是GRPO中常用的稳定化技术，但实验表明它们无法在激进体制下同时实现稳定与高性能（Figure 7, Figure 8）：标准裁剪无法阻止崩溃，更强的裁剪或正则化虽能提升稳定性却显著降低性能。CAPO的曲率感知筛选则直接作用于**更新方向本身**，通过拒绝引起异常偏移的样本来预防不稳定，而非事后裁剪或惩罚，从而在稳定性和性能之间取得更优平衡。

**需要人工验证的点**：CAPO的理论保证（Theorem 5.1）声称，当满足信任域约束时，聚合更新保证单调改进 $J(\pi_{\theta+\Delta\theta}) - J(\pi_\theta) \ge \omega - C\sqrt{\delta_F}$，其中 $C = \frac{2\gamma}{(1-\gamma)^2}\epsilon\sqrt{2}$。该定理的推导依赖于last‑layer模型假设和若干近似，其在完整LLM参数空间中的严格成立性需进一步验证。



CAPO (Curvature‑Aware Policy Optimization) 是一个面向 LLM 推理任务、以策略梯度 RL 微调为核心的样本高效训练框架。其设计目标是在激进训练体制（高学习率、小批次）下阻止策略崩溃，从而大幅提升样本效率。框架的整体管线由五个核心模块串联而成，形成“生成–估计–建模–筛选–更新”的闭环。

**1. 轨迹生成与优势估计**  
LLM 基于当前策略自回归生成响应序列，构成一批轨迹。对每条轨迹计算回报 $\hat{R}(\tau)$，随后在组内进行标准化以获得 GRPO 优势估计：
$$
\hat{A}^{\mathrm{GRPO}}(s_t, a_t) = \frac{\hat{R}(\tau) - \bar{R}}{\hat{\sigma}_{R} + \varepsilon}
$$
其中 $\bar{R}$ 和 $\hat{\sigma}_{R}$ 分别为组内轨迹回报的均值和标准差。该模块为下游梯度计算提供逐 token 的优势信号。

**2. Last‑Layer 曲率模型**  
为避免在全参数空间物化 Hessian 和 Fisher 信息矩阵的高昂代价，CAPO 仅对 LLM 最后一层的权重矩阵 $\psi$ 构建计算高效的曲率近似。具体而言，它利用稀疏梯度（由 top‑k / nucleus 采样引入的梯度稀疏性）分别估计模型梯度 $\tilde{g}(\psi)$、Hessian $\tilde{H}(\psi)$ 和 Fisher $\tilde{F}(\psi)$，从而将二阶几何信息压缩到低维子空间。

**3. 方向曲率估计**  
在不显式构建完整曲率矩阵的前提下，该模块通过内积运算直接估计候选更新方向上的目标偏移 $m_H(\Delta\psi)$ 和策略偏移 $m_F(\Delta\psi)$：
$$
m_H(\psi) = \tilde{g}(\psi)^\top \Delta\psi + \frac{1}{2} \Delta\psi^\top \tilde{H}(\psi) \Delta\psi, \quad
m_F(\psi) = \frac{1}{2} \Delta\psi^\top \tilde{F}(\psi) \Delta\psi
$$
这两个标量分别近似更新引起的目标函数变化和平均 KL 散度，是信任域筛选的核心判据。

**4. Adam 步长规划**  
CAPO 模拟底层 LLM 优化器（Adam）的实际行为，利用 Adam 的一阶/二阶矩估计生成候选参数更新方向 $\Delta\psi$。消融实验表明，匹配优化器行为（而非使用简单 SGD 步长表示）对于 Dr.CAPO 和 ReinCAPO 等扩展变体防止崩溃至关重要（Figure 6）。

**5. 信任域筛选与梯度更新**  
对每个 token 子集 $b_i$，计算其候选步长引起的曲率偏移，并施加局部信任域约束：
$$
\delta_H \leq m_H(\Delta\psi_i) \leq \delta_H^{\mathrm{high}}, \quad m_F(\Delta\psi_i) \leq \delta_F
$$
仅当子集同时满足目标下界和策略偏移上界时被接受；否则被掩蔽。接受部分进行梯度累积并执行参数更新。该机制在 token 级别运行，峰值拒识率约 8%，随后持续低于 2%（Figure 5），执行时间开销不到总步长的 3%（Table 1）。

整个框架的关键因果机制在于：通过轻量级二阶曲率近似实时监测每次更新的局部几何风险，主动拒绝那些会导致目标或策略分布剧烈偏移的样本，从而在激进训练体制下充当隐式的信任域约束。这一设计使得 CAPO 在 MATH 上仅需 GRPO（保守体制）1/30 的样本完成数即可达到同等准确度，在 TEST 基准上则仅需 1/9 的样本（Section 6.1, Figure 2）。



CAPO的核心思想是将二阶曲率信息引入策略梯度更新的样本筛选过程，从而在不牺牲性能的前提下实现激进训练体制下的稳定学习。整个方法围绕一个计算高效的曲率近似框架展开，包含以下关键模块。

### 4.1 Last‑Layer曲率模型

直接计算全参数空间的Hessian或Fisher信息矩阵（FIM）在LLM规模下不可行。CAPO采用**最后一层近似策略**：仅对LLM最后一层的权重矩阵 $\psi$ 构建曲率模型，其余参数 $\bar{\theta}$ 视为固定。这一选择基于两个现实考量：其一，最后一层直接决定输出分布，对策略偏移最为敏感；其二，LLM解码通常使用top‑k或nucleus采样等选择性采样方法，导致梯度天然稀疏——仅被采样的token具有非零梯度，这使得相关矩阵运算的复杂度大幅降低。

在最后一层模型下，CAPO定义了三个核心量：

**模型梯度** $\tilde{g}(\psi)$：
$$\tilde{g}(\psi) = \mathbb{E}_{\tau \sim \pi_{\theta}} \left[ \sum_{t=0}^{T} \gamma^{t} A(s_{t}, a_{t}) (e_{a} - \pi_{\theta}(s_{t})) \otimes h_{\bar{\theta}}(s_{t}) \right]$$

其中 $A(s_t, a_t)$ 为优势函数，$e_a$ 为动作的one‑hot向量，$\pi_{\theta}(s_t)$ 为当前策略分布，$h_{\bar{\theta}}(s_t)$ 为最后一层之前的隐藏表示。该梯度通过外积形式表达，避免了在全参数空间上的显式展开。

**模型Hessian** $\tilde{H}(\psi)$：
$$\tilde{H}(\psi) = \mathbb{E}_{\tau \sim \pi \theta} \left[ \sum_{t=0}^{T} \gamma^{t} A(s,a) \Big( (e_{a} - \pi_{\theta}(s_{t})) (e_{a} - \pi_{\theta}(s_{t}))^\top - F(s_{t}) \Big) \otimes h_{\bar{\theta}}(s_{t}) h_{\bar{\theta}}(s_{t})^\top \right]$$

其中 $F(s_t)$ 是当前状态下策略的Fisher信息矩阵。该表达式捕获了目标函数在参数更新方向上的二阶曲率。

**模型Fisher** $\tilde{F}(\psi)$：
$$\tilde{F}(\psi) = \mathbb{E}_{\tau \sim \pi_{\theta}} \left[ \left( (e_{a_{t}} - \pi_{\theta}(s_{t})) (e_{a_{t}} - \pi_{\theta}(s_{t}))^\top \right) \otimes h_{\bar{\theta}}(s_{t}) h_{\bar{\theta}}(s_{t})^\top \right]$$

该矩阵近似了更新引起的策略分布变化，与KL散度存在二阶对应关系。

> **关键设计**：CAPO并不显式物化 $\tilde{H}(\psi)$ 和 $\tilde{F}(\psi)$，而是仅计算它们在候选更新方向 $\Delta\psi$ 上的**方向曲率**，即内积形式 $\Delta\psi^\top \tilde{H} \Delta\psi$ 和 $\Delta\psi^\top \tilde{F} \Delta\psi$。这通过向量‑雅可比积实现，计算开销远低于完整矩阵的构建。

### 4.2 目标偏移与策略偏移的量化

基于上述曲率模型，CAPO将每次候选更新引起的两个关键偏移量化为：

**目标偏移** $m_H$（基于二阶泰勒展开）：
$$m_H(\psi) = \tilde{g}(\psi)^\top \Delta\psi + \frac{1}{2} \Delta\psi^\top \tilde{H}(\psi) \Delta\psi$$

该量近似了目标函数 $J$ 在参数更新 $\Delta\psi$ 下的期望变化。一阶项 $\tilde{g}^\top \Delta\psi$ 捕获梯度方向上的改进，二阶项 $\frac{1}{2}\Delta\psi^\top \tilde{H} \Delta\psi$ 捕获曲率带来的修正。

**策略偏移** $m_F$（基于Fisher信息矩阵）：
$$m_F(\psi) = \frac{1}{2} \Delta\psi^\top \tilde{F}(\psi) \Delta\psi$$

该量近似了更新前后策略分布的平均KL散度 $\bar{D}_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\theta+\Delta\theta})$，是衡量策略变化幅度的核心指标。

### 4.3 Adam步长规划

CAPO需要模拟底层优化器的实际行为来生成候选更新方向 $\Delta\psi$。由于LLM训练通常使用Adam优化器，CAPO采用Adam的矩估计来规划步长：
$$\Delta\psi = \alpha \frac{\hat{p}_t}{\sqrt{\hat{q}_t} + \epsilon}$$

其中 $\hat{p}_t$ 和 $\hat{q}_t$ 分别是梯度的一阶矩和二阶矩的偏差校正估计，$\alpha$ 为学习率。消融实验（Figure 6）表明，使用与底层优化器匹配的步长表示对于保持稳定性至关重要：在Dr.CAPO和ReinCAPO等扩展变体上，SGD步长表示无法防止策略崩溃，而Adam表示则保持稳定。

### 4.4 信任域筛选与梯度更新

CAPO的核心操作机制是**token级信任域筛选**。对于每个批次收集的轨迹，CAPO将数据划分为不相交的子集 $b_i \subset B$（在token级实现中，每个子集对应一个token），对每个子集计算候选更新 $\Delta\psi_i$ 并评估其偏移量。接受条件为：

$$\delta_H \leq m_H(\Delta\psi_i) \leq \delta_H^{\text{high}}, \quad m_F(\Delta\psi_i) \leq \delta_F$$

其中 $\delta_H$ 为目标改进的下界（防止退化更新），$\delta_H^{\text{high}}$ 为目标改进的上界（防止过激更新），$\delta_F$ 为策略偏移的上界（充当信任域半径）。只有同时满足这三个条件的子集才被纳入梯度累积和参数更新。

这一机制在概念上等价于token掩码：引起过大偏移的token被拒绝参与梯度估计。实验表明，CAPO的token拒识率峰值约8%，随后持续低于2%（Figure 5），干预极小但效果显著。

### 4.5 单调改进保证

CAPO的理论基础由以下定理支撑（Theorem 5.1）：

$$J(\pi_{\theta+\Delta\theta}) - J(\pi_{\theta}) \ge \omega - C \sqrt{\delta_F}, \quad C = \frac{2\gamma}{(1-\gamma)^2} \epsilon \sqrt{2}$$

其中 $\omega$ 为接受子集的目标改进下界，$C$ 为与折扣因子 $\gamma$ 和策略变化上界 $\epsilon$ 相关的常数。该定理表明，当聚合更新的期望改进 $\omega$ 超过惩罚项 $C\sqrt{\delta_F}$ 时，CAPO保证策略性能的单调改进。这为信任域筛选提供了理论保障：通过控制策略偏移 $m_F \leq \delta_F$，CAPO在每次更新中维持了可证明的改进下界。



## 实验与关键发现

### 核心发现：样本效率与训练稳定性的双重突破

CAPO的核心价值在于解决了LLM推理强化学习中的一个根本矛盾：激进更新体制（高学习率、小批量）能提升样本效率，但会导致策略崩溃；保守体制虽稳定，却牺牲了效率。实验结果表明，CAPO成功打破了这一困境。

**样本效率的量化提升**：在MATH数据集上，CAPO达到与标准保守GRPO相同准确度所需的训练完成次数减少了30倍（Figure 1, Figure 2）。在涵盖8个基准的TEST套件上，这一优势为9倍（Section 6.1）。这意味着在相同的计算预算下，CAPO能以远少于基线方法的样本量达到同等或更优的推理性能。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_iIvPuXoDs1/figures/003_Figure_2.jpg]]
*Figure 2: Comparison with baseline methods on policy gradient stability. While the setup with more aggressive updates makes all methods more sample-efficient, it also leads the baselines to policy collapse. In contrast, CAPO prevents collapse and achieves up to 30× greater sample efficiency than GRPO under aggressive updates*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_iIvPuXoDs1/figures/001_Figure_1.jpg]]
*Figure 1: Accuracy on MATH dataset from different RL methods. CAPO (ours) achieves 30× greater sample efficiency under an aggressive (A) update regime (higher learning rate, smaller batch size), whereas GRPO suffers policy collapse*

**训练稳定性的决定性证据**：Figure 2展示了最具说服力的对比。在激进更新体制下，所有基线方法——包括标准GRPO（Shao et al., 2024）、Dr.GRPO（Liu et al., 2025a）和REINFORCE（Williams, 1992）——均发生灾难性策略崩溃，准确率骤降至接近零的水平。而CAPO在相同条件下不仅避免了崩溃，还持续稳定学习，在基线方法完全失效后仍保持有效的策略改进。

### 稳定性机制的可视化验证

Figure 3从优化动态的角度解释了CAPO为何能保持稳定。该图展示了训练过程中不同方法的策略偏移估计（$m_F$）和目标偏移估计（$m_H$）。不稳定方法表现出大幅、突发的方向曲率尖峰，这些尖峰直接对应着策略分布的剧烈跳变。相比之下，CAPO通过token级的信任域约束，将全局（批次级）的偏移维持在平滑且可控的范围内，从机制层面验证了Theorem 5.1的单调改进保证。

### 消融实验：方法的通用性与关键设计选择

**曲率感知选择的通用性**：Figure 4表明，将CAPO的曲率感知选择机制引入Dr.GRPO和REINFORCE（分别称为Dr.CAPO和ReinCAPO），同样能防止策略崩溃。这说明该机制不依赖于特定的策略梯度目标函数，而是作为一种通用的稳定化模块发挥作用。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_iIvPuXoDs1/figures/009_Figure_4.jpg]]
*Figure 4: Evaluation of extended versions of RL methods with curvature-aware selection. Incorporating curvature-aware selection consistently improves the base methods, preventing policy collapse and demonstrating the broader applicability of our approach across different policy optimization objectives*

**优化器模型的关键作用**：Figure 6的消融实验揭示了Adam步长规划的必要性。对于CAPO本身，使用Adam或SGD表示的性能相近。但对于Dr.CAPO和ReinCAPO，仅使用Adam表示才能防止策略崩溃；SGD表示下的变体在训练中期出现剧烈性能下降。这一发现表明，匹配底层LLM优化器（Adam）的步长行为是保证扩展方法鲁棒性的关键设计选择。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_iIvPuXoDs1/figures/013_Figure_6.jpg]]
*Figure 6: Ablation study of the optimizer model. For CAPO, both representations yield similar performance, whereas for Dr.CAPO and ReinCAPO, only the Adam-based representation prevents policy collapse, indicating that matching the optimizer provides a more robust choice across setups*

**干预的极小性**：Figure 5显示，CAPO的token拒识率峰值约8%，之后迅速降至并维持在2%以下。这说明信任域筛选机制仅在训练初期的不稳定阶段进行有意义的干预，随后几乎不干扰正常学习过程。Table 1进一步证实，CAPO的执行时间开销不到总步长的3%（总步长135.84秒中仅占3.99秒），其中最主要的子模块“更新Adam矩估计”占2.46%。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_iIvPuXoDs1/figures/010_Table_1.jpg]]
*Table 1: Breakdown of the execution time of CAPO. CAPO contributes less than 3% of the total step time, resulting in minimal overhead relative to standard training*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_iIvPuXoDs1/figures/008_Figure_5.jpg]]
*Figure 5: Token rejection rate under CAPO. It maintains a low rejection rate over training, stabilizing learning with minimal intervention*

### 与现有稳定化技术的对比

实验系统比较了CAPO与两种常用的策略梯度稳定化技术：PPO裁剪和KL正则化。

**PPO裁剪的局限性**（Figure 7）：标准裁剪比（$\epsilon=0.2$）无法防止激进体制下的策略崩溃。更激进的裁剪比（$\epsilon=0.02$或$0.002$）虽能改善稳定性，但以牺牲整体性能为代价，且这种权衡在更大的KL裁剪阈值$t$下更加严重。CAPO则在无需此类妥协的情况下同时实现了稳定性和高性能。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_iIvPuXoDs1/figures/014_Figure_7.jpg]]
*Figure 7: Effect of “PPO clipping” on GRPO stability. Standard clipping (ϵ = 0.2) fails to prevent collapse, while more aggressive ratios improve stability but reduce overall performance, with the trade-off becoming more severe as t increases*

**KL正则化的不足**（Figure 8）：强KL正则化（$\beta=1.0$）减少了不稳定性，但严重降低了准确率。更重要的是，Figure 8右图揭示了KL正则化的一个深层问题：它产生了无界的梯度范数（在裁剪前），这些异常大的梯度可能将优化推入不稳定区域。CAPO通过直接约束更新方向上的曲率偏移，从根本上避免了这一问题。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_iIvPuXoDs1/figures/015_Figure_8.jpg]]
*Figure 8: Effect of KL regularization on GRPO stability. (Left) Accuracy on the MATH dataset under different levels of KL regularization. Stronger regularization ( $\beta$ = 1 . 0 ) reduces instability but degrades performance. (Right) Maximum gradient norms (before clipping), averaged across seeds. KL regularization produces unbounded gradients that may drive the optimization into unstable regions*

### 曲率估计的可靠性

Table 5报告了Fisher方向曲率估计（$\hat{m}_F$）与估计策略变化（$\bar{D}_{\mathrm{KL}}$）之间的Spearman相关性。在token级别，GRPO和CAPO更新的相关系数分别为0.622和0.459；在全局级别，相关性进一步提升。这一结果验证了last‑layer曲率模型虽为近似，但确实捕捉到了真实策略偏移的关键信号，为信任域筛选提供了可靠依据。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_iIvPuXoDs1/figures/019_Table_5.jpg]]
*Table 5: Spearman correlations $\rho$ between Fisher directional curvature estimates $\hat { m } _ { F }$ and the estimated policy change $\bar { D } _ { \mathrm { K L } } ( \dot { \pi } _ { \pmb { \theta } }$ | | $\pi _ { \pmb { \theta } + \Delta \pmb { \theta } }$ ) We report correlations for both GRPO and CAPO updates. The results indicate that the estimates $\hat { m } _ { F }$ maintain a consistent monotonic relationship with the true policy shift across algorithms, reliable identifying the scale of the policy shifts

### 需要手动验证的局限

以下几点源于分析中的推断，建议对照原文确认：实验仅在数学推理任务（MATH系列）上评估，未涉及代码生成或常识推理等任务类型；所用模型规模未明确超过70B参数，更大规模模型上的可扩展性证据不足；CAPO的多个阈值（$\delta_H$、$\delta_H^{high}$、$\delta_F$）需手动调整，论文未提供自动化设定方法。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_iIvPuXoDs1/figures/016_Table_2.jpg]]
*Table 2: Training Hyperparameters*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_iIvPuXoDs1/figures/017_Table_3.jpg]]

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_iIvPuXoDs1/figures/018_Table_3.jpg]]
*Table 3: Hyperparameters for the standard (conservative) and aggressive regimes. Table 4: Curvature-aware masking thresholds for CAPO, Dr.CAPO and ReinCAPO*



## 定位与知识库关联

### 与现有RL微调方法的关系

CAPO并非提出新的策略优化目标，而是为现有策略梯度方法引入一种**通用的、基于二阶曲率感知的样本选择机制**。其核心定位是**稳定器**而非替代品。

**GRPO**（Shao et al., 2024）是CAPO的直接基底。CAPO优化与GRPO相同的代理目标（Equation 3），但通过信任域筛选改变了梯度估计的数据使用方式：GRPO使用批次中所有样本进行更新，而CAPO仅在接受曲率约束的子集上累积梯度。在标准保守训练体制下，GRPO本身是稳定的；CAPO的价值在于**解锁激进体制**——当学习率提高、批次缩小以追求样本效率时，GRPO会因梯度估计的高方差和非平稳优化而崩溃，CAPO则通过拒绝引起大幅目标偏移或策略偏移的token来维持稳定。

**Dr.GRPO**（Liu et al., 2025a）和**REINFORCE**（Williams, 1992）作为替代RL方法，同样面临激进体制下的崩溃问题。CAPO的方法具有**跨目标函数的通用性**：将曲率感知选择机制嵌入Dr.GRPO和REINFORCE（分别得到Dr.CAPO和ReinCAPO），同样能防止策略崩溃（Figure 4）。这表明曲率感知选择是一种**与具体优化目标解耦的稳定化技术**，可推广至不同的策略梯度变体。

与标准信任域方法（如TRPO、PPO）的关系值得特别说明。CAPO本质上是实现了一种**局部的、隐式的信任域约束**，但与标准方法存在关键差异：
- **PPO裁剪**：标准裁剪（ε=0.2）在激进体制下无法防止GRPO崩溃；更激进的裁剪比（ε=0.02, 0.002）虽能改善稳定性，但会显著降低性能，且这种权衡随KL裁剪阈值t增大而恶化（Figure 7）。
- **KL正则化**：更强的KL惩罚（β=1.0）能减少不稳定性，但同样以降低峰值性能为代价；更重要的是，KL正则化产生的梯度范数无界，可能将优化推向不稳定区域（Figure 8右侧）。

CAPO通过**直接作用于样本层面**的曲率过滤，在稳定性和性能之间取得了更好的平衡，避免了全局约束带来的性能退化。

### 适用边界与局限

**已验证的有效范围：**
- **任务类型**：数学推理（MATH系列基准，包括MATH-500和8个TEST基准）。CAPO在这些任务上展示了30倍（MATH）和9倍（TEST）的样本效率提升，且在所有激进体制下均未出现策略崩溃。
- **模型规模**：实验基于Qwen2.5-7B-Instruct（约70亿参数），未涉及更大规模模型。
- **训练长度**：100个梯度步的训练调度，未验证更长训练周期下的行为。

**已知局限：**
1. **阈值依赖**：CAPO需要手动设定三个信任域阈值（δ_H, δ_H^high, δ_F），这些阈值需根据任务和训练体制单独调整，缺乏自适应机制。
2. **任务泛化性未验证**：仅评估了数学推理任务，在代码生成、常识推理、对话等任务上的有效性未知。
3. **曲率近似的精度边界**：计算模型基于last‑layer近似（仅对LLM最后一层权重矩阵建模梯度和曲率），忽略了更深层参数的二阶效应，可能低估某些更新引起的分布偏移。当深层参数对策略变化贡献显著时，这种近似可能不够保守。
4. **优化器模型的敏感性**：消融实验（Figure 6）表明，对于Dr.CAPO和ReinCAPO等扩展变体，必须使用Adam步长表示才能保持稳定；单纯的SGD步长表示不足以防止崩溃。这意味着曲率模型需要**匹配底层LLM优化器**，限制了其即插即用的便捷性。

### 开放问题

1. **可扩展性**：CAPO在更大规模模型（如>70B参数）和更长训练调度下是否仍能保持有效？曲率近似和信任域筛选的计算开销是否会随模型规模非线性增长？

2. **自适应阈值**：曲率感知选择的阈值是否可以依据优化理论自适应调节？例如，能否根据曲率估计的历史统计动态调整δ_F，使其在不同训练阶段自动适配？

3. **计算模型的深度扩展**：将曲率模型从last‑layer扩展至更多层（如最后几层或全参数空间的结构化近似）是否能进一步提升稳定性，同时保持计算可行性？这涉及与K‑FAC等结构化二阶方法的潜在结合。

4. **与自然梯度的融合**：CAPO的信任域方法是否可与自然梯度或K‑FAC等已有近似二阶方法结合？自然梯度直接利用Fisher信息矩阵进行参数更新，而CAPO利用Fisher和Hessian的定向曲率进行样本筛选，二者在理论上互补。

5. **跨任务泛化**：CAPO在非数学推理任务（如代码生成、长文本问答）上的表现如何？不同任务的奖励信号特性和策略分布差异可能影响曲率估计的准确性和筛选机制的有效性。



## 原文 PDF

![[paperPDFs/ICLR_2026/Stabilizing_Policy_Gradients_for_Sample_Efficient_Reinforcement_Learning_in_LLM_Reasoning.pdf]]
