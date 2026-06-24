---
title: "Master Skill Learning with Policy-Grounded Synergy of LLM-based Reward Shaping and Exploring"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Master_Skill_Learning_with_Policy_Grounded_Synergy_of_LLM_based_Reward_Shaping_and_Exploring.pdf
openreview_forum_id: 1vXMfIYFZp
aliases:
- MSLPGSLBRSE
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过构建任务相关的抽象功能状态空间（AFS）将高维状态映射为低维的“功能状态”，并基于访问计数产生探索奖励；同时引入策略反馈驱动的动态权重β来平衡目标奖励与探索奖励，实现从过度探索到精准利用的平滑过渡。"
primary_logic: "将LLM生成的任务感知奖励与基于功能状态访问计数的结构化探索在策略优化过程中动态融合，形成一个策略反馈驱动的自增强循环：淘汰-扩展过滤机制高效搜索最优奖励-探索组合，策略继承避免重复训练，实现奖励塑造、探索与策略学习的协同进化。"
claims:
- "PoRSE在24个机器人任务中的23个上显著超越所有基线，在DoorCloseOutward、Kettle等困难任务上首次实现完美成功（MTS 1.000）。"
- "移除策略融合组件（θ_fusion）导致最大性能坍塌，Anymal任务MTS下降2783%，TwoCatch任务下降95%，表明策略继承与融合是框架保持稳定性的关键。"
- "在TwoCatch任务中，PoRSE通过动态奖励权重调整达到0.349的成功率，而Eureka和ROSKA几乎完全失败（MTS≈0），首次解决了该困难任务。"
- "消融实验证实，移除目标奖励（R_g）会使TwoCatch性能从0.349降至0.190，移除探索奖励（R_e）使BlockStack从0.753降至0.393，印证了两种奖励的互补必要性。"
---

# Master Skill Learning with Policy-Grounded Synergy of LLM-based Reward Shaping and Exploring

> [!tip] 核心洞察
> 将LLM生成的任务感知奖励与基于功能状态访问计数的结构化探索在策略优化过程中动态融合，形成一个策略反馈驱动的自增强循环：淘汰-扩展过滤机制高效搜索最优奖励-探索组合，策略继承避免重复训练，实现奖励塑造、探索与策略学习的协同进化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于策略引导的语言模型奖励塑造与探索协同的机器人技能学习 |
| 英文题名 | Master Skill Learning with Policy-Grounded Synergy of LLM-based Reward Shaping and Exploring |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=1vXMfIYFZp) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | PoRSE |
| Dataset | Pen (Bi-DexHands), TwoCatch (Bi-DexHands), BlockStack (Bi-DexHands), DoorCloseOutward (Bi-DexHands) |

> [!tip] 效果简介
> - Pen (Bi-DexHands) 上，MTS 为 1.000 ± 0.000，对比 Eureka: 0.634 ± 0.460; ROSKA: 0.111 ± 0.077，变化 +0.366 (vs Eureka)。
> - TwoCatch (Bi-DexHands) 上，MTS 为 0.349 ± 0.063，对比 Eureka: 0.001 ± 0.001; ROSKA: 0.000 ± 0.000，变化 首次解决该任务。
> - BlockStack (Bi-DexHands) 上，MTS 为 0.753 ± 0.210，对比 Eureka: 0.254 ± 0.119; ROSKA: 0.148 ± 0.154，变化 +0.499 (vs Eureka)。

## 概述

**核心瓶颈**：现有基于大语言模型（LLM）的奖励函数设计方法（如Eureka、ROSKA）过度聚焦于目标导向的奖励信号，忽略了对任务相关状态的主动探索，导致智能体在高自由度、稀疏奖励的机器人操作任务中频繁陷入局部最优。与此同时，通用的探索奖励（如基于原始状态的访问计数）与任务目标脱节，将大量计算资源浪费在与任务无关的状态空间探索上。

**核心方法**：本文提出**PoRSE**（Policy-grounded Reward Shaping and Exploring），通过构建**抽象功能状态空间**（Affordance State Space, AFS）将高维机器人状态映射为低维的“功能状态”，并基于该空间的访问计数生成任务相关的探索奖励。在此基础上，PoRSE引入**策略反馈驱动的动态权重β**来平衡目标奖励与探索奖励，并通过**淘汰-扩展过滤机制**（LEF）高效搜索最优的奖励-探索组合，同时利用策略继承避免重复训练，实现奖励塑造、探索与策略学习的协同进化。

**方法定位**：PoRSE处于LLM辅助奖励设计与结构化探索的交叉点。与仅优化目标奖励函数的Eureka（Ma et al., 2023）和ROSKA（Huang et al., 2025）不同，PoRSE同时优化目标奖励函数与AFS映射函数，并将探索奖励的权重纳入策略反馈闭环中进行动态调整。相比ROSKA中依赖贝叶斯优化确定策略融合比例的计算密集方案，PoRSE采用LLM辅助的LEF方法实现快速自适应。

**主要结果**：在Bi-DexHands和Isaac Gym的24个机器人技能学习任务中，PoRSE在23个任务上显著超越所有基线方法。在DoorCloseOutward、Kettle等困难任务上首次实现完美成功率（MTS = 1.000 ± 0.000），在TwoCatch任务上取得0.349的突破性成功率（Eureka和ROSKA几乎完全失败，MTS ≈ 0）。消融实验证实，移除策略融合组件导致Anymal任务性能下降2783%，移除探索奖励使BlockStack成功率从0.753降至0.393，验证了各组件在框架中的互补必要性。

## 背景与动机

### 机器人技能学习中的奖励设计困境

深度强化学习在机器人技能获取中的成功高度依赖奖励函数的质量。稀疏奖励（Sparse Rewards）仅提供任务完成的二值信号，在复杂操作任务中几乎无法提供有效学习梯度。人类专家手工设计的密集奖励函数（Human Expert-Designed Rewards）虽然能提供逐时间步的反馈，但其设计过程耗时且依赖领域知识，难以跨任务泛化。

近年来，基于大语言模型的自动化奖励设计方法取得了显著进展。**Eureka**（Ma et al., 2023）利用LLM根据任务描述和环境代码迭代生成奖励函数代码，通过强化学习反馈进行进化优化。**ROSKA**（Huang et al., 2025）进一步引入奖励-策略协同进化机制，利用历史策略知识避免每次迭代都从头训练。这些方法在中等难度任务上表现出色，但在高自由度、稀疏奖励的复杂任务中仍然面临严重瓶颈。

### 核心瓶颈：目标导向与探索的失衡

现有LLM奖励设计方法存在一个根本性缺陷：**过度聚焦于目标导向的奖励塑造，系统性地忽略了对任务相关状态的探索引导**。具体表现为：

1. **探索的盲目性**：Eureka和ROSKA仅优化目标奖励函数，智能体在高维状态空间中缺乏有效的探索方向，容易陷入局部最优。通用的好奇心驱动探索奖励（如基于状态访问计数的探索奖励）与任务目标无关，大量计算资源被浪费在无意义的状态探索上。

2. **探索-利用的静态失衡**：即使引入探索奖励，现有方法也缺乏根据策略学习进度动态调整探索与利用平衡的机制。固定权重导致训练早期探索不足或后期过度探索，策略无法收敛到最优解。

3. **奖励与探索的孤立优化**：目标奖励和探索奖励被作为独立组件分别设计，缺乏在策略优化过程中的协同进化。这种割裂导致两者无法形成互补增强效应。

### 本文动机：策略引导的奖励-探索协同进化

针对上述瓶颈，本文提出**PoRSE**（Policy-grounded Synergy of LLM-based Reward Shaping and Exploring），核心动机是实现三个层面的深度融合：

- **任务相关探索**：利用LLM自动构建抽象功能状态空间（Affordance State Space, AFS），将高维观测映射为与任务语义相关的低维“功能状态”，并基于访问计数产生任务感知的探索奖励，使探索方向与任务目标天然对齐。

- **策略反馈驱动的动态平衡**：引入策略性能反馈作为接地信号，通过LLM动态调整目标奖励与探索奖励的混合权重β，实现从训练早期的过度探索到训练后期的精准利用的平滑过渡。

- **奖励-探索-策略的协同进化**：将目标奖励函数优化、AFS映射函数优化和策略继承融合纳入统一的迭代优化循环，形成策略反馈驱动的自增强循环——更好的策略反馈引导LLM生成更精准的奖励和探索方案，更优的奖励-探索组合进一步推动策略提升。

通过上述设计，PoRSE旨在解决现有方法在困难机器人操作任务上的失败问题，首次实现Kettle、DoorCloseOutward等复杂任务上的完美成功率。

## 核心创新

### 瓶颈洞察：目标导向奖励的“探索盲区”

现有基于LLM的奖励设计方法（如 **Eureka** (Ma et al., 2023) 和 **ROSKA** (Huang et al., 2025)）的核心逻辑是：LLM生成候选奖励函数，通过策略训练反馈迭代筛选最优目标奖励。这一范式在中等复杂度任务上有效，但在高自由度、稀疏奖励场景下暴露出结构性缺陷——**智能体缺乏对任务相关状态的系统性探索引导**，极易陷入局部最优。通用探索奖励（如基于原始状态空间的计数奖励）虽能增加探索广度，却与任务目标脱节，大量计算资源浪费在无意义状态上。

PoRSE的切入点是：**将探索从“任务无关的随机扰动”升级为“任务感知的结构化搜索”**，并在策略优化过程中实现目标奖励与探索奖励的动态协同。

### 四个关键创新维度

#### 1. 抽象功能状态空间（AFS）与任务相关探索

PoRSE不再依赖原始高维状态空间的通用探索，而是让LLM自动构建一个低维的**抽象功能状态空间**（Affordance State Space, AFS）。LLM根据任务描述和环境代码，生成映射函数 $\mathbf{M}^n = \mathcal{LLM}(I_d, I_e)$，将高维状态 $\mathbf{S}$ 压缩为与任务完成逻辑相关的“功能状态” $\mathbf{S}_o$。基于该离散化空间中的访问计数，PoRSE计算好奇心驱动的探索奖励：

$$R_{\mathrm{e}}(s_o) = \frac{\lambda}{\sqrt{\sum_{t=1}^{T} \mathbb{I}(s_{o,d}^t = s_{o,d}^c)}}$$

其中 $\lambda = 0.01$。这一设计的因果机制是：**AFS将“探索”锚定在任务语义上**——智能体被激励去访问尚未充分探索的“功能状态”（如“门把手被抓住”、“水壶倾斜至特定角度”），而非漫无目的地扰动关节角度。消融实验印证了其必要性：移除探索奖励 $R_e$ 后，BlockStack任务的MTS从0.753骤降至0.393（Table 2）。

#### 2. 策略反馈驱动的动态奖励权重（IPG-LEF for β）

目标奖励与探索奖励之间存在天然张力：过度探索会延迟任务收敛，过度利用则导致过早陷入局部最优。PoRSE引入**策略反馈驱动的动态权重机制**：LLM根据实时策略性能反馈 $V(\theta)$ 建议混合系数 $\beta$，通过**淘汰-扩展过滤**（LEF）机制在并行训练中动态筛选最优组合：

$$R_{\mathrm{total}}^k = \beta * R_e^k + (2-\beta) R_g^k, \quad \beta \in [0,2]$$

LEF的核心逻辑是：在每轮迭代中，淘汰表现最差的 $\beta$ 候选，以存活的最佳组合为基础进行变异扩展，形成“淘汰-扩展”循环。这一机制实现了从早期“过度探索”到后期“精准利用”的平滑过渡。Figure 6的训练曲线表明，仅当采用适当的混合比例时，策略才能成功训练并达到更优性能；固定 $\beta$（PoRSE w/o R_ratio）导致PushBlock MTS从0.318降至0.243（Table 2）。

#### 3. 策略继承与快速融合（IPG-LEF for α）

ROSKA使用贝叶斯优化确定策略融合比例 $\alpha$，计算开销高昂。PoRSE将其替换为LLM辅助的LEF快速搜索：

$$\theta_f(\alpha) = \alpha \cdot \theta_{\mathrm{best}} + (1-\alpha) \cdot \theta_{\mathrm{random}}$$

其中 $\alpha_{\mathrm{new}} = \mathcal{LLM}(I_d, V(\theta))$，通过淘汰与变异策略动态调整。这一设计避免了贝叶斯优化的高昂采样成本，同时保留了策略继承的核心优势——**避免每轮从零训练**。消融实验揭示了其关键地位：移除策略融合（$\theta_{\mathrm{fusion}}$）造成最大性能坍塌，Anymal任务MTS下降2783%，TwoCatch下降95%（Table 16）。

#### 4. 奖励-探索-策略的协同进化循环

前述三个维度的创新并非孤立运作，而是通过**迭代协同优化**形成自增强循环：LLM同时优化目标奖励函数 $R_g$ 和AFS映射函数 $M$（Eq. 1, Eq. 5），LEF交替搜索 $\beta$ 和 $\alpha$，每轮迭代的优化结果作为下一轮LLM的反馈输入。这一设计使奖励塑造、探索引导与策略学习三者形成闭环——**更好的探索发现更优状态区域，更优状态反馈驱动更精准的奖励设计，更精准的奖励进一步加速策略收敛**。

### 与基线方法的本质差异

| 维度 | Eureka | ROSKA | PoRSE |
|------|--------|-------|-------|
| 优化目标 | 仅目标奖励 $R_g$ | 目标奖励+策略协同 | 目标奖励 $R_g$ + AFS映射 $M$ + 动态权重 $\beta$ + 融合比例 $\alpha$ |
| 探索机制 | 无任务相关探索 | 无任务相关探索 | LLM构建的AFS + 访问计数探索奖励 |
| 奖励平衡 | 固定权重 | 固定权重 | 策略反馈驱动的LEF动态 $\beta$ |
| 策略继承 | 无 | 贝叶斯优化 $\alpha$ | LEF快速搜索 $\alpha$ |

消融实验的鲁棒性验证进一步表明，即使使用随机组合的功能状态空间（PoRSE-AFS-Random），性能仍显著优于Eureka/ROSKA等基线（Table 4），说明IPG流程本身具有高鲁棒性——AFS的质量提升是“锦上添花”，而非“雪中送炭”式的脆性依赖。

## 整体框架

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_1vXMfIYFZp/figures/002_Figure_2.jpg]]
*Figure 2: Overview of PoRSE. It leverages LLMs to generate goal-oriented rewards while building an affordance mapping function for exploration bonuses. These rewards are dynamically combined to optimize policies. An iterative feedback loop continuously refines rewards and affordance state space, creating a co-evolutionary system*

PoRSE 的核心架构是一个**策略反馈驱动的自增强循环**，它将 LLM 生成的奖励函数、任务相关的结构化探索、以及动态的奖励-探索平衡机制耦合在一起，通过迭代优化实现三者协同进化。整体 pipeline 由五个关键模块构成，形成闭环：

### 1. LLM 奖励生成模块

框架的入口是 LLM 根据任务描述 $I_d$、环境代码 $I_e$、上一轮最佳目标奖励函数 $R_{g,best}^{n-1}$ 以及策略性能评估 $V(\pi)$，迭代生成新的目标导向奖励函数：

$$\mathbf{R}_g^n = \mathcal{LLM}(I_d, I_e, R_{g,best}^{n-1}, V(\pi)) \quad \text{(Eq. 1)}$$

每轮生成 $K=6$ 个候选奖励函数，通过从头训练策略并评估性能，选出最佳者进入下一轮迭代（Algorithm 1, Appendix A.1）。

### 2. 功能状态空间构建与探索奖励模块

这是 PoRSE 区别于 Eureka 和 ROSKA 的核心创新。LLM 同时生成一个映射函数 $\mathcal{M}^n$，将高维原始状态空间 $\mathbf{S}$ 压缩到低维的**抽象功能状态空间（Affordance State Space, AFS）** $\mathbf{S}_o$：

$$\mathbf{M}^n = \mathcal{LLM}(I_d, I_e, \mathcal{M}_{best}^{n-1}, V(\theta)) \quad \text{(Eq. 5)}$$

AFS 将状态按任务相关的功能语义（如“手与物体的相对位置”“关节是否到达极限”）离散化。基于 AFS 中的访问计数，计算好奇心驱动的探索奖励：

$$R_{\mathrm{e}}(s_o) = \frac{\lambda}{\sqrt{\sum_{t=1}^{T} \mathbb{I}(s_{o,d}^t = s_{o,d}^c)}}, \quad \lambda=0.01 \quad \text{(Eq. 3)}$$

该奖励与任务目标紧密对齐，避免了通用探索奖励（如 SimHash、LLMCount）在无意义状态上浪费计算资源的问题。

### 3. 动态奖励权重模块（LEF for β）

目标奖励 $R_g$ 与探索奖励 $R_e$ 通过动态系数 $\beta \in [0,2]$ 加权融合：

$$R_{\mathrm{total}}^k = \beta * R_e^k + (2-\beta) R_g^k \quad \text{(Eq. 6)}$$

LLM 根据策略训练反馈 $V(\theta)$ 建议 $\beta$ 值，随后采用**淘汰-扩展过滤机制（LEF）**：并行训练多个 $\beta$ 候选组合，淘汰性能最差者，将最优幸存者的 $\beta$ 作为基础进行变异扩展，生成新的候选集。该循环在每轮迭代中交替执行，高效搜索最优的奖励-探索平衡点。

### 4. 策略继承与融合模块（LEF for α）

为避免每轮从头训练带来的高昂计算开销，PoRSE 将上一轮最佳策略参数 $\theta_{\mathrm{best}}$ 与随机策略 $\theta_{\mathrm{random}}$ 按比例融合：

$$\theta_f(\alpha) = \alpha \cdot \theta_{\mathrm{best}} + (1-\alpha) \cdot \theta_{\mathrm{random}} \quad \text{(Eq. 7)}$$

与 ROSKA 采用贝叶斯优化确定 $\alpha$ 不同，PoRSE 使用 LLM 辅助的 LEF 方法动态调整 $\alpha$：$\alpha_{new} = \mathcal{LLM}(I_d, V(\theta))$，显著降低了计算开销。

### 5. 迭代协同优化循环

上述模块在 $N=5$ 轮迭代中交替运行（Figure 2, Algorithm 1）：
- **每轮内**：LLM 同时生成 $K$ 组目标奖励函数与 AFS 映射函数，通过 LEF 搜索最优 $\beta$ 和 $\alpha$ 组合；
- **跨轮次**：上一轮的最佳奖励函数、映射函数和策略参数作为下一轮的先验，通过策略继承避免重复训练。

**关键因果机制**：该闭环形成了一个正反馈循环——更好的探索奖励帮助策略发现更优行为，更优行为的反馈又指导 LLM 生成更精准的奖励函数和 AFS 映射，从而在奖励塑造、探索与策略学习之间实现协同进化。

**证据强度**：消融实验证实了各模块的必要性。移除策略融合（$\theta_{fusion}$）导致 Anymal 任务 MTS 下降 2783%（Table 16）；固定 $\beta$（PoRSE w/o R_ratio）使 PushBlock MTS 从 0.318 降至 0.243（Table 2）；固定 $\alpha$（PoRSE w/o $\theta_{ratio}$）使 TwoCatch MTS 从 0.349 降至 0.276（Table 2）。这些结果表明，动态的 $\beta$ 和 $\alpha$ 调整是框架保持稳定性和性能的关键瓶颈。

## 核心模块与公式推导

### 3.1 整体框架与迭代流程

PoRSE 的核心是一个策略反馈驱动的自增强循环，通过 $N=5$ 轮迭代实现奖励塑造、探索与策略学习的协同进化。每轮迭代包含以下关键步骤（见 Algorithm 1）：

1. **LLM 生成**：LLM 根据任务描述 $I_d$、环境代码 $I_e$、历史最佳奖励 $R_{g,best}^{n-1}$ 和策略评价 $V(\pi)$，生成 $K=6$ 组候选组合，每组包含目标导向奖励函数 $\mathbf{R}_g^n$ 和功能状态空间映射函数 $\mathbf{M}^n$。
2. **并行训练与淘汰**：对 $K$ 组组合并行训练策略，根据训练后策略的性能 $V(\theta)$ 淘汰低效组合，保留表现最优的组合作为下一轮扩展的基础。
3. **扩展与继承**：基于幸存的最优组合，通过 LLM 建议的变异生成新的候选 $\beta$ 值和 $\alpha$ 值，同时利用策略融合机制继承历史策略知识，避免从头训练。
4. **循环迭代**：重复淘汰-扩展过程，交替优化奖励-探索混合比例 $\beta$ 和策略融合比例 $\alpha$，直至完成 $N$ 轮。

### 3.2 LLM 奖励生成模块

PoRSE 继承了 Eureka 的 LLM 奖励生成范式，但将优化范围从单一目标奖励扩展至目标奖励与功能状态映射的联合生成。第 $n$ 轮迭代中，LLM 根据如下公式生成候选目标奖励函数：

$$
\mathbf{R}_g^n = \mathcal{LLM}(I_d, I_e, R_{g,best}^{n-1}, V(\pi)) \tag{1}
$$

其中：
- $I_d$：任务的自然语言描述
- $I_e$：环境代码（API 定义、状态空间、动作空间）
- $R_{g,best}^{n-1}$：上一轮迭代中表现最优的目标奖励函数
- $V(\pi)$：当前策略的性能评价反馈（如任务成功率、累积回报等）

生成 $K$ 个候选奖励后，通过从头训练策略并评估性能来筛选最佳奖励：

$$
R_{g,best}^n = \operatorname{argmax}_{R_{g,k}^n \in \mathbf{R}_g^n} V(\mathcal{T}(R_{g,k}^n, \theta_0, T_{max})) \tag{2}
$$

其中 $\mathcal{T}$ 表示使用奖励函数 $R_{g,k}^n$ 从随机初始化策略 $\theta_0$ 训练 $T_{max}$ 步的过程，$V$ 为性能评价函数。

### 3.3 抽象功能状态空间与探索奖励

#### 3.3.1 功能状态空间构建

PoRSE 的核心创新在于引入**抽象功能状态空间**（Affordance State Space, AFS），将高维机器人状态 $s \in \mathcal{S}$ 映射到低维的“功能状态” $s_o \in \mathcal{S}_o$：

$$
\mathbf{M}^n = \mathcal{LLM}(I_d, I_e, \mathcal{M}_{best}^{n-1}, V(\theta)) \tag{5}
$$

映射函数 $\mathcal{M}$ 由 LLM 自动构建，其设计原则是仅保留与任务完成相关的状态维度。例如，在抓取任务中，AFS 可能仅包含末端执行器与目标物体的相对位置和距离，而忽略关节角度等无关信息。这种任务相关的降维使得探索奖励能够聚焦于有意义的状态区域，避免在无关节状态上浪费探索资源。

#### 3.3.2 基于访问计数的探索奖励

在 AFS 的基础上，PoRSE 对连续的功能状态空间进行离散化处理，得到离散功能状态 $s_{o,d}$。探索奖励基于状态访问次数的平方根倒数计算：

$$
R_{\mathrm{e}}(s_o) = \frac{\lambda}{\sqrt{\sum_{t=1}^{T} \mathbb{I}(s_{o,d}^t = s_{o,d}^c)}} \tag{3}
$$

其中：
- $s_{o,d}^c$：当前时刻的离散功能状态
- $\mathbb{I}(\cdot)$：指示函数，统计历史上访问该状态的次数
- $\lambda = 0.01$：探索奖励的缩放系数
- $T$：当前训练步数

该设计遵循经典的基于计数的好奇心探索范式：访问次数越少的状态获得越高的探索奖励，从而驱动策略探索未知的功能状态区域。与通用状态空间的计数探索不同，AFS 确保了探索奖励与任务目标的相关性。

### 3.4 动态奖励权重融合

#### 3.4.1 加权总奖励

PoRSE 通过动态系数 $\beta \in [0, 2]$ 加权融合探索奖励与目标奖励：

$$
R_{\mathrm{total}}^k = \beta \cdot R_e^k + (2 - \beta) R_g^k \tag{6}
$$

该设计的精妙之处在于：
- 当 $\beta > 1$ 时，探索奖励权重更高，策略倾向于探索未知状态
- 当 $\beta < 1$ 时，目标奖励权重更高，策略倾向于利用已有知识完成任务
- $\beta = 1$ 时，两者权重相等

#### 3.4.2 淘汰-扩展过滤机制（LEF）

$\beta$ 的优化采用**淘汰-扩展过滤**（Leverage-Elimination Filtering, LEF）机制，避免穷举搜索的计算开销：

1. **LLM 建议**：LLM 根据任务描述和当前策略性能 $V(\theta)$，建议一组候选 $\beta$ 值 $\mathbf{B}^n$。
2. **并行评估**：对每个候选 $\beta$ 值，使用对应的加权总奖励训练策略并评估性能。
3. **淘汰**：保留性能最优的 $\beta$ 值，淘汰其余候选。
4. **扩展**：基于最优 $\beta$ 值，通过 LLM 建议的变异策略生成 $J$ 个新的候选 $\beta$ 值。
5. **循环**：重复淘汰-扩展过程，动态调整探索与利用的平衡。

### 3.5 策略继承与融合

为减少每轮迭代中从头训练策略的计算开销，PoRSE 引入策略融合机制，将上一轮最优策略 $\theta_{\mathrm{best}}$ 与随机初始化策略 $\theta_{\mathrm{random}}$ 按比例混合：

$$
\theta_f(\alpha) = \alpha \cdot \theta_{\mathrm{best}} + (1 - \alpha) \cdot \theta_{\mathrm{random}} \tag{7}
$$

其中 $\alpha \in [0, 1]$ 为融合比例：
- $\alpha = 1$：完全继承上一轮最优策略
- $\alpha = 0$：完全随机初始化
- $0 < \alpha < 1$：在继承与探索之间折中

与 ROSKA 使用贝叶斯优化确定 $\alpha$ 不同，PoRSE 同样采用 LEF 方法动态调整 $\alpha$：

$$
\alpha_{new} = \mathcal{LLM}(I_d, V(\theta))
$$

LLM 根据训练反馈建议 $\alpha$ 值，通过淘汰-扩展循环快速搜索最优融合比例，避免了贝叶斯优化的高昂计算成本。消融实验（Table 1, Table 2）证实，移除策略融合组件（$\theta_{fusion}$）导致最大性能坍塌——Anymal 任务 MTS 下降 2783%，TwoCatch 任务下降 95%，表明策略继承与融合是框架保持稳定性的关键。

### 3.6 协同优化循环

PoRSE 的完整优化流程可概括为以下协同进化循环：

1. **奖励-探索协同生成**：LLM 同时生成目标奖励函数 $R_g$ 和 AFS 映射函数 $\mathcal{M}$，实现奖励塑造与探索策略的联合设计。
2. **动态权重搜索**：通过 LEF 机制搜索最优 $\beta$，平衡探索与利用。
3. **策略继承搜索**：通过 LEF 机制搜索最优 $\alpha$，平衡继承与探索。
4. **交替优化**：在 $N=5$ 轮迭代中交替优化 $\beta$ 和 $\alpha$，形成策略反馈驱动的自增强循环。

消融实验（Table 2）证实交替优化的必要性：若固定策略融合比例 $\alpha$（PoRSE w/o $\theta_{ratio}$），TwoCatch 任务 MTS 从 0.349 降至 0.276；若固定奖励融合比例 $\beta$（PoRSE w/o $R_{ratio}$），PushBlock 任务 MTS 从 0.318 降至 0.243。

## 实验与分析

### 主实验结果

PoRSE在24个机器人技能学习任务中的23个上取得了最优性能，验证了策略引导的奖励-探索协同机制的有效性。Figure 3和Figure 4分别展示了中等难度和困难操作任务上的MTS（Maximum Training Success）对比。

**中等难度操作任务**：在15个中等难度操作任务中，PoRSE在所有任务上均优于基线方法。在Pen、DoorOpenOutward、BottleCap、Franka等5个任务上达到完美成功率（MTS 1.000 ± 0.000），相比人类专家设计的密集奖励函数（Human）提升1.6%–3.5%。在GraspAndPlace任务上，PoRSE达到MTS 0.984，比Human基线（0.785）提升25.3%。相比之下，**Eureka**（Ma et al., 2023）在Pen任务上仅获得0.634 ± 0.460，**ROSKA**（Huang et al., 2025）仅获得0.111 ± 0.077，表明纯目标导向的LLM奖励设计在需要探索的任务上存在严重瓶颈。

**困难操作任务**：在8个困难操作任务上，PoRSE在所有任务上均取得最优结果，并在DoorCloseOutward和Kettle两个任务上首次实现完美成功（MTS 1.000 ± 0.000），而Eureka分别仅获得0.553和0.742，ROSKA和Sparse Rewards几乎完全失败。在TwoCatchUnderarm任务上，PoRSE达到0.349 ± 0.063，这是该困难任务首次被成功解决——Eureka仅0.001 ± 0.001，ROSKA为0.000 ± 0.000。在BlockStack任务上，PoRSE达到0.753 ± 0.210，远超Eureka（0.254 ± 0.119）和ROSKA（0.148 ± 0.154），提升幅度分别达196%和409%。

**运动控制任务**：在Anymal四足机器人任务上，PoRSE达到MTS -0.012 ± 0.012，相比Human基线（-0.021 ± 0.026）提升约42%，而Eureka仅为-0.276 ± 0.497，表现出严重的不稳定性。

Table 5和Table 6提供了所有任务上各方法的完整MTS均值和标准差。Figure 7的HNS（Human Normalized Score）对比进一步确认：PoRSE在23/24个任务上超越所有基线方法。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_1vXMfIYFZp/figures/012_Table_5.jpg]]
*Table 5: MTS performance comparison on moderate-difficulty tasks. MTS (mean ± std) showing PoRSE’s superiority over baselines in manipulation and locomotion tasks*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_1vXMfIYFZp/figures/013_Table_6.jpg]]
*Table 6: MTS performance comparison on hard manipulation tasks. Results demonstrate PoRSE’s breakthroughs in hard skill learning tasks where existing methods fail completely*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_1vXMfIYFZp/figures/014_Figure_7.jpg]]
*Figure 7: HNS score comparison across 24 robotic tasks. PoRSE significantly outperformed other methods in 23 (all 24) robot skill learning tasks, achieving the best experimental results*

### 消融实验

消融实验系统性地验证了PoRSE各组件和优化策略的必要性。Table 1和Table 2报告了架构组件和优化策略的消融结果。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_1vXMfIYFZp/figures/009_Table_2.jpg]]
*Table 2: The MTS results show that both the architectural components and optimization strategy contribute to the final performance*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_1vXMfIYFZp/figures/008_Table_1.jpg]]
*Table 1: The MTS results show that both the architectural components and optimization strategy contribute to the final performance*

**目标奖励与探索奖励的互补性**：移除目标导向奖励函数（PoRSE w/o R_g）后，TwoCatch任务MTS从0.349骤降至0.190，BlockStack从0.753降至0.328，表明目标奖励对精度任务至关重要。移除探索奖励（PoRSE w/o R_e）后，BlockStack MTS从0.753降至0.393，PushBlock从0.318降至0.306，验证了AFS探索机制对需要广泛状态探索的任务不可或缺。两种奖励缺一不可，印证了框架设计的互补性。

**策略融合的关键作用**：移除策略融合组件（PoRSE w/o θ_fusion）导致最严重的性能坍塌。Anymal任务MTS下降2783%（从-0.012降至-0.346），TwoCatch下降95%（从0.349降至0.018），Franka从0.957降至0.671。这表明策略继承与融合机制是框架保持训练稳定性和避免从头训练高昂成本的核心。

**动态权重调整的必要性**：固定奖励融合比例β（PoRSE w/o R_ratio）破坏了探索-利用平衡，PushBlock MTS从0.318降至0.243，BlockStack从0.753降至0.296。固定策略融合比例α（PoRSE w/o θ_ratio）同样导致性能下降，TwoCatch MTS从0.349降至0.276。Figure 6的训练曲线进一步证实：仅采用适当的β混合比例（通过LEF机制动态搜索）才能成功训练策略，纯目标奖励（β=0）或纯探索奖励（β=2）均导致完全失败。

**AFS机制的有效性**：Table 3对比了PoRSE与LLMCount（使用通用计数探索而非任务相关AFS）的性能。PoRSE在所有六个代表性操作任务上大幅领先：Pen任务从0.412提升至1.000，TwoCatch从0.000提升至0.349，BlockStack从0.140提升至0.753。这验证了LLM自动构建的任务相关功能状态空间远优于任务无关的通用探索。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_1vXMfIYFZp/figures/010_Table_3.jpg]]
*Table 3: MTS comparative results of PoRSE and LLMCount baselines across six representative manipulation tasks. PoRSE achieves apparent improvement in task success rates*

**IPG流程的鲁棒性**：Table 4显示，即使使用随机组合的功能状态空间（PoRSE-AFS-Random），性能仍显著优于Eureka和ROSKA等基线，表明IPG的淘汰-扩展过滤和策略融合流程本身具有高鲁棒性，不完全依赖最优AFS设计。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_1vXMfIYFZp/figures/011_Table_4.jpg]]
*Table 4: MTS Performance Comparison of PoRSE-AFS-Random and Baseline Methods on Representative Manipulation Tasks (mean ± standard deviation)*

### 失败模式与局限性

尽管PoRSE在绝大多数任务上取得突破，Switch任务上所有方法（包括PoRSE）仍然完全失败。该任务涉及极度稀疏的奖励信号和高维动作空间，当前的AFS构建和探索奖励机制仍不足以有效引导策略探索。

LLM输出不稳定性是另一个实际限制。即使使用相同提示，LLM生成的奖励函数和映射函数代码质量仍存在波动，可能产生不可执行的代码。虽然通过代码正确性测试过滤了无效输出，但LLM的固有随机性仍可能引入额外方差，影响结果的一致性和可复现性。

奖励函数和探索策略的可解释性有限，依赖于LLM内部知识，可能继承训练数据中的偏见。在实际部署中，这可能导致难以诊断的失败模式。

### 关键图表结论

- **Figure 3/4**：PoRSE在中等和困难操作任务上全面超越Eureka、ROSKA等基线，在DoorCloseOutward、Kettle等任务上首次实现完美成功。
- **Figure 6**：动态β调整至关重要，单一奖励模式（纯目标或纯探索）完全失效，验证了LEF机制搜索最优混合比例的必要性。
- **Table 1/2**：策略融合组件（θ_fusion）的移除导致最严重的性能坍塌（Anymal下降2783%），是框架稳定性的核心保障。
- **Table 3**：任务相关AFS探索远优于通用计数探索（LLMCount），是PoRSE性能优势的关键来源。
- **Table 5/6**：完整MTS数据表明PoRSE在24个任务中的23个上取得最优，困难任务上实现多项从零到一的突破。

### 补充图表

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_1vXMfIYFZp/figures/025_Table_16.jpg]]
*Table 16: Performance drop (%) of each ablation compared with the full PoRSE framework*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_1vXMfIYFZp/figures/016_Table_7.jpg]]
*Table 7: MTS Comparison of LLMCount and PoRSE methods, PoRSE method achieved higher MTS on 23 tasks*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_1vXMfIYFZp/figures/017_Table_8.jpg]]
*Table 8: MTS Comparison of SimHash and PoRSE methods, PoRSE method achieved higher MTS in 8 robot skill learning tasks*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_1vXMfIYFZp/figures/018_Table_9.jpg]]
*Table 9: Performance Comparison of PoRSE-GPT-4o-mini with Baselines on Representative Tasks*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

PoRSE 处于基于大语言模型（LLM）的奖励设计这一研究脉络中，其直接前驱是 **Eureka**（Ma et al., 2023）和 **ROSKA**（Huang et al., 2025）。Eureka 首次将 LLM 引入奖励函数代码的迭代生成，利用进化搜索和策略反馈来优化目标导向的奖励函数，但其核心局限在于**完全忽略了对任务相关状态的探索**——在高自由度、稀疏奖励任务中，仅凭目标奖励无法引导智能体穿越广阔的无效状态空间。ROSKA 在此基础上引入了奖励与策略的协同进化，利用历史策略知识避免每次迭代都从头训练，但其探索机制仍依赖通用策略的随机性，缺乏任务结构化的探索引导。

PoRSE 的核心突破在于**将探索从“通用附加项”提升为与目标奖励对等的第一性组件**。具体而言，PoRSE 与 Eureka/ROSKA 的关键差异体现在三个维度：

| 维度 | Eureka | ROSKA | PoRSE |
|------|--------|-------|-------|
| 优化对象 | 仅目标奖励函数 $R_g$ | 目标奖励 + 策略继承 | 目标奖励 $R_g$ + 功能状态映射 $\mathcal{M}$ + 融合权重 $\beta, \alpha$ |
| 探索机制 | 无任务相关探索 | 策略随机性（隐式） | LLM 构建的抽象功能状态空间（AFS）+ 访问计数奖励 |
| 策略继承 | 无 | 贝叶斯优化确定 $\alpha$ | LEF 快速动态调整 $\alpha$ |

另一个重要的对比基线是 **LLMCount**，它代表了“通用探索奖励 + LLM 目标奖励”的朴素组合——使用 SimHash 对整个状态空间做通用计数探索，而非 PoRSE 中 LLM 自动构建的任务相关 AFS。消融实验（Table 3）表明，PoRSE 在所有六个代表性操作任务上均大幅超越 LLMCount：Pen 任务从 0.412 提升至 1.000，TwoCatch 从 0.000 提升至 0.349，BlockStack 从 0.140 提升至 0.753。这一差距揭示了**任务相关探索与通用探索之间的质变鸿沟**——在高维状态空间中，通用计数将大量计算资源浪费在与任务无关的状态上，而 AFS 将探索导向任务相关的功能状态，使奖励信号与策略目标形成闭环。

### 2. 适用边界

PoRSE 在以下条件下展现出显著优势：

- **高自由度操作任务**：Bi-DexHands 灵巧手环境中的 24 个任务覆盖了从简单抓取到复杂双手协调的广泛难度谱系。PoRSE 在 23/24 个任务上取得最优 HNS 分数（Figure 7），尤其在 DoorCloseOutward、Kettle 等困难任务上首次实现完美成功率（MTS 1.000），而 Eureka 和 ROSKA 在这些任务上的 MTS 分别仅为 0.553 和 0.000。
- **稀疏奖励场景**：TwoCatch 任务代表了极度稀疏奖励的挑战——智能体需要双手协调接住空中飞行的物体，目标奖励仅在成功接住时触发。Eureka 和 ROSKA 在该任务上几乎完全失败（MTS ≈ 0），而 PoRSE 通过 AFS 探索奖励达到 0.349 的成功率，首次实现了该任务的可行解。
- **需要探索-利用动态平衡的任务**：Figure 6 的训练曲线表明，固定的 $\beta$ 值（纯目标奖励或纯探索奖励）均导致训练失败，只有通过 IPG 流程动态搜索到合适的 $\beta$ 区间时，策略才能成功收敛。这印证了 PoRSE 的 LEF 机制在自动发现任务特定的探索-利用平衡点方面的关键作用。

PoRSE 的适用边界同样明确：

- **极端困难任务仍存在失败**：在 Switch 等需要复杂子任务分解的长序贯任务上，PoRSE 与所有基线方法一样完全失败，表明当前框架在极度稀疏奖励和高维动作空间下的探索能力仍有上限。
- **依赖 LLM 输出质量**：LLM 生成奖励函数和 AFS 映射函数时存在固有的输出不稳定性——即使相同提示也可能产生质量差异或不可执行代码。论文通过代码正确性测试缓解了这一问题，但 LLM 输出的波动仍可能引入额外方差。
- **Sim-to-Real 差距未验证**：当前实验全部在仿真环境（Isaac Gym、Bi-DexHands）中进行，未涉及实际物理机器人的部署验证。

### 3. 局限与开放问题

**已识别的局限**：

1. **LLM 输出不稳定性**：奖励函数和 AFS 映射函数的生成质量依赖于 LLM 的内部知识，可能继承训练数据中的偏见。论文采用代码正确性测试作为过滤机制，但无法从根本上消除 LLM 输出的方差。
2. **可解释性有限**：LLM 生成的奖励规则和功能状态映射缺乏显式的语义解释，难以分析智能体具体学到了什么行为模式。
3. **计算开销**：尽管 LEF 机制比贝叶斯优化更高效，但每轮迭代仍需并行训练多个奖励-探索组合（$K=6$），总训练轮数为 90,000 epochs，对计算资源有一定要求。

**开放问题**：

1. **视觉感知的集成**：当前 AFS 构建依赖仿真环境中的底层状态信息（如物体位置、关节角度），如何将轻量级视觉语言模型（如 CLIP、Grounding DINO）集成到 AFS 构建流程中，实现从原始 RGB-D 感知数据直接动态提取任务相关状态，是向真实世界部署的关键一步。
2. **元学习自适应调度**：$\beta$ 和 $\alpha$ 的交替优化目前依赖手工设定的迭代调度（$N=5$ 轮，每轮固定搜索步数）。能否通过元学习根据任务特性自动调整搜索策略，减少超参数依赖？
3. **不确定性量化**：当 LLM 对奖励规则的置信度较低时（如面对新颖或语义模糊任务），如何量化不确定性并动态调整探索强度，以避免策略在错误奖励信号引导下振荡？
4. **分层强化学习扩展**：PoRSE 能否扩展到分层强化学习架构（HRL），通过 AFS 在不同抽象层级上引导子任务探索，以解决 Switch 等需要子任务分解的复杂长序贯任务？
5. **在线自适应**：在实际物理机器人上进行长期部署时，环境动态可能发生变化，如何实现 AFS 的在线自适应更新，使探索奖励始终保持与当前任务目标的相关性？

## 原文 PDF

![[paperPDFs/ICLR_2026/Master_Skill_Learning_with_Policy_Grounded_Synergy_of_LLM_based_Reward_Shaping_and_Exploring.pdf]]
