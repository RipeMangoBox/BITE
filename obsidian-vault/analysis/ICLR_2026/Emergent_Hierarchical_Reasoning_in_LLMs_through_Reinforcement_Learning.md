---
title: "Emergent Hierarchical Reasoning in LLMs through Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Emergent_Hierarchical_Reasoning_in_LLMs_through_Reinforcement_Learning.pdf
project_link: https://tiger-ai-lab.github.io/Hierarchical-Reasoner/
code_link: null
openreview_forum_id: NlkykTqAId
aliases:
- HHACA
- EHRLTRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "对生成序列中战略规划tokens的优势函数进行放大（通过HICRA的α参数控制），从而将优化压力集中在高层策略上。"
primary_logic: "RL训练使LLM推理涌现出层次化结构：模型先巩固低层执行技能，然后主导性能提升的是高层战略规划的多样化和探索。HICRA通过识别并放大规划tokens的学习信号，更高效地推动这一战略探索过程，最终显著提升推理性能。"
claims:
- "HICRA在所有文本和多模态基准上始终优于GRPO基线，提升幅度高达+8.4 (AMC23) 和 +7.0 (MathVista)。"
- "RL训练显著减少高层规划与策略错误，而对低层执行错误的减少较小，证明战略规划是主要瓶颈。"
- "HICRA通过维持更高的语义熵来促进多样化的战略探索，这与更高的验证准确率强相关。"
- "规划tokens与高熵tokens并不等同，仅有不到10%的高熵tokens具有规划功能，凸显了基于功能识别的优越性。"
---

# Emergent Hierarchical Reasoning in LLMs through Reinforcement Learning

> [!tip] 核心洞察
> RL训练使LLM推理涌现出层次化结构：模型先巩固低层执行技能，然后主导性能提升的是高层战略规划的多样化和探索。HICRA通过识别并放大规划tokens的学习信号，更高效地推动这一战略探索过程，最终显著提升推理性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 强化学习驱动的大语言模型涌现层次推理 |
| 英文题名 | Emergent Hierarchical Reasoning in LLMs through Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=NlkykTqAId) · [Project](https://tiger-ai-lab.github.io/Hierarchical-Reasoner/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | HICRA (Hierarchy-Aware Credit Assignment) |
| Dataset | AIME24, AIME25, Math500, AMC23 |

> [!tip] 效果简介
> - AIME24 上，Pass@1 为 73.1，对比 68.5，变化 +5.4。
> - AIME25 上，Pass@1 为 65.1，对比 60.0，变化 +5.1。
> - Math500 上，Pass@1 为 89.0，对比 83.0，变化 +6.0。

## 概要

大语言模型在强化学习（RL）推理训练中涌现出层次化的推理结构：模型首先巩固低层的过程执行技能，随后学习瓶颈转移到高层战略规划的探索与掌握。然而，现有的RL算法（如GRPO）对所有token施加各向同性的优化压力，不区分token的层次功能，导致优化信号被稀释，高层策略探索效率低下。

针对这一瓶颈，本文提出**HICRA（Hierarchy-Aware Credit Assignment，层次感知信用分配）**算法。其核心因果调节机制是：对生成序列中战略规划token的优势函数进行放大（通过α参数控制），将优化压力集中在高层策略上，从而更高效地推动战略探索。

**核心发现：**
- RL训练使LLM推理涌现两阶段动态：阶段① 过程巩固（执行token的困惑度和token熵快速下降）；阶段② 战略规划探索（战略gram的语义熵持续上升，与验证准确率强相关）。
- 规划/策略类错误在RL训练中的减少幅度显著大于过程执行类错误，证明战略规划是主要性能瓶颈。
- HICRA通过维持更高的语义熵来促进多样化战略探索，在所有文本和多模态基准上始终优于GRPO基线，提升幅度高达+8.4（AMC23）和+7.0（MathVista）。
- 规划token与高熵token并不等同——不到10%的高熵token具有规划功能，凸显了基于功能识别而非简单熵值筛选的优越性。

**方法定位：** HICRA位于RL信用分配方法的改进线上，通过在GRPO框架内引入层次感知的优势调制，将优化目标分布从各向同性拉伸为各向异性，使概率质量集中在战略维度。其有效性依赖于基础模型的过程可靠性——当基础模型程序性技能不足时（如Llama-3.1-Instruct），策略放大可能失效。



### 大语言模型的推理瓶颈：从“能执行”到“会规划”

大语言模型（LLM）在数学推理、代码生成等复杂任务上取得了显著进展，但其推理能力的提升并非均匀分布。人类解决复杂问题时，天然地依赖一种层次化的认知结构：**高层战略规划**（如“这道题应该用反证法还是归纳法”）与**低层过程执行**（如“展开这个多项式并合并同类项”）。前者决定推理的方向与骨架，后者负责将策略转化为具体的计算步骤。

然而，当下的强化学习（RL）训练范式在优化LLM推理时，并未区分这两种功能层次。以GRPO为代表的算法将所有生成token一视同仁地分配信用信号，导致优化压力被大量低层执行token稀释，而真正决定推理成败的高层规划token获得的梯度更新不足。这种“各向同性”的优化策略，使得模型在RL训练的早期阶段主要巩固低层执行技能，随后才缓慢地将学习前沿转移到战略规划的探索与掌握上——这种两阶段动态本身揭示了层次化推理的涌现，但也暴露了现有RL算法效率低下的根本原因。

### 现有方法的缺口：熵正则化与高熵token放大的局限

针对上述问题，近期工作尝试通过**熵正则化**（Cheng et al., 2025）或在优势函数中对**高熵token**进行加权（Cheng et al. & Wang et al.）来鼓励模型探索。这些方法的共同假设是：高不确定性（高熵）的token对应着需要更多探索的关键决策点。

但这一假设存在根本性缺陷。大量证据表明，**规划token与高熵token并不等同**——仅有不到10%的高熵token实际承担规划功能（Figure 12, Figure 13）。绝大多数高熵token反映的是措辞层面的表达多样性，而非推理逻辑的战略选择。因此，无差别地对所有高熵token施加熵奖励或优势放大，不仅无法有效促进战略探索，反而可能导致序列长度失控增长（Figure 5），而准确率并未同步提升。

### 本文动机：识别并放大真正的规划信号

上述分析指向一个清晰的问题：**如何在不依赖熵等统计代理的情况下，直接识别模型生成序列中具有高层战略功能的token，并将RL的优化压力集中到这些token上？**

本文的核心动机正是回答这一问题。我们提出**HICRA（Hierarchy-Aware Credit Assignment）**，通过以下两个关键步骤实现层次感知的信用分配：

1. **自动识别规划token**：利用Strategic Grams管道，从训练数据中提取具有“演绎、分支、回溯”等战略功能的n-gram，作为高层规划token的功能代理（Section 2.1, Figure 6）。
2. **放大规划token的优势信号**：在GRPO框架下，对识别出的规划token施加优势放大（通过参数 $\alpha$ 控制），使策略梯度的目标分布从各向同性变为各向异性，概率质量集中在规划维度，从而更有力地推动战略探索（Section 3）。

这一设计直接针对RL训练中“优化信号被低层token稀释”的瓶颈，通过将信用分配与token的语义功能绑定，而非统计不确定性，实现了更高效、更精准的推理能力提升。



## 核心方法与创新机理

HICRA 的核心创新在于**识别并放大了 RL 训练中高层战略规划 tokens 的学习信号**，从而将优化压力从均匀分布转向对推理性能瓶颈的定向突破。

### 创新动机：层次化推理的涌现瓶颈

HICRA 的设计根植于一个关键发现：LLM 在 RL 推理训练中涌现出层次化结构，且学习瓶颈会随训练进程发生转移。具体而言，训练呈现两阶段动态（Figure 1, Figure 2）：

- **阶段一**：模型快速巩固低层过程技能（procedural consolidation），表现为执行 tokens 的困惑度急剧下降、token 级熵降低，模型对计算步骤的确定性显著增强。
- **阶段二**：学习前沿转移到高层战略规划（strategic planning），此时主导性能提升的是战略规划的多样化和探索，而非进一步的过程精度提升。

这一现象的因果证据来自错误类型分析（Figure 3）：RL 训练后，规划与策略错误（红色）的减少幅度显著大于其他过程性错误（灰色），证明**战略规划才是 RL 训练中真正的性能瓶颈**。然而，标准的 GRPO 算法对所有 tokens 施加各向同性的优化压力，不区分 tokens 的功能层次，导致优化信号被海量低层执行 tokens 稀释。

### 核心改进：层次感知的优势函数

HICRA 对 GRPO 的关键改动集中在**优势函数（Advantage）的计算方式**上。标准 GRPO 对所有 tokens 使用统一的组归一化奖励作为优势：

$$\hat{A}_{i,t} = R(\mathbf{q}, \mathbf{o}_i) - \frac{1}{G} \sum_{j=1}^{G} R(\mathbf{q}, \mathbf{o}_j)$$

HICRA 引入一个**规划 token 识别机制**，将序列中的 tokens 划分为规划 tokens（$t \in S_i$）和执行 tokens（$t \notin S_i$），并仅对规划 tokens 进行优势放大：

$$\hat{A}_{i,t}^{\mathrm{HICRA}} = \begin{cases} \hat{A}_{i,t} + \alpha \cdot |\hat{A}_{i,t}| & \mathrm{if~} t \in S_i \\ \hat{A}_{i,t} & \mathrm{if~} t \notin S_i \end{cases}$$

这一修改的巧妙之处在于其**双向调节**效果：对于成功轨迹（$\hat{A}_{i,t} > 0$），它放大规划 tokens 的正向信用；对于失败轨迹（$\hat{A}_{i,t} < 0$），它减轻规划 tokens 的惩罚。这鼓励模型在战略层面进行更大胆的探索，同时避免因探索失败而过度惩罚高层决策。

### 规划 Token 的识别：Strategic Grams 管道

HICRA 的另一个关键创新是**基于语义功能的规划 token 识别**，而非依赖统计不确定性。HICRA 使用 Strategic Grams（SGs）管道从训练数据中自动提取代表高层战略的 n-gram，这些 n-gram 承担三种逻辑功能：演绎推理（deduction）、分支探索（branching）和回溯修正（backtracing）（Figure 6）。

这一设计选择至关重要。实验表明，**规划 tokens 与高熵 tokens 并不等同**：虽然大多数规划 tokens 确实具有较高熵值，但反过来，仅有不到 10% 的高熵 tokens 具备规划功能（Figure 12, Figure 13）。这意味着基于熵的探索方法（如 Entropy Regularization 或 High-Entropy Advantage 基线）会将大量优化信号浪费在低层措辞变化上，而非真正的战略探索。HICRA 通过功能识别精准定位战略维度，从而实现了更高效的信用分配。

### 与基线的本质差异

| 方法 | 优势函数修改对象 | 修改方式 | 效果 |
|------|-----------------|---------|------|
| **GRPO** | 所有 tokens 统一 | 组归一化奖励 | 优化信号被稀释 |
| **Entropy Regularization** | 所有 tokens 统一 | 添加熵正则化损失 | 提高 token 级熵但未能提升准确率，序列长度失控（Figure 5） |
| **High-Entropy Advantage** | 仅高熵 tokens | 调制优势函数 | 大部分优化指向非规划的措辞变化 |
| **HICRA** | 仅规划 tokens | 优势放大（$+\alpha\|\hat{A}\|$） | 定向推动战略探索，语义熵与验证准确率强相关 |

HICRA 通过各向异性的目标分布将概率质量集中在规划 tokens 维度，本质上将策略梯度更新从“均匀探索”转变为“战略探索”。这一机制的有效性得到了 Placebo HICRA 实验的验证：使用随机 n-gram 替代 Strategic Grams 时，性能显著下降，证明规划 token 识别的必要性而非优势放大本身在起作用。



![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_NlkykTqAId/figures/002_Figure_1.jpg]]
*Figure 1: (Left) LLM reasoning mirrors a human-like hierarchical reasoning: high-level strategic planning and low-level procedural executions. (Right) Hierarchical reasoning emerges during RL training via a two-phase dynamic. Phase ① consolidates low-level skills, marked by a token-entropy drop in execution tokens. The learning frontier then shifts to Phase ②, where the model explores and masters high-level planning, marked by increased semantic diversity, sustained reasoning enhancement and length scaling*

HICRA 的整体 pipeline 围绕一个核心洞察构建：RL 训练中的 LLM 推理会涌现出层次化结构，而性能瓶颈最终落在高层战略规划上。基于此，HICRA 将优化压力集中在规划 tokens 上，形成三个串联模块。

### 模块一：Strategic Grams 识别

该模块从训练数据中自动提取代表高层战略功能的 n-gram 集合。具体而言，**Strategic Grams (SGs)** 被定义为引导推理逻辑流的语义单元，主要承担三类逻辑操作：演绎（deduction）、分支（branching）和回溯（backtracing）。识别管道基于统计频率自动筛选这些 n-gram，作为规划 tokens 的功能代理。人工验证表明，86% 的 SGs 确实起到了引导推理流程或提出方案的作用；灵敏度分析进一步显示，随机删除 30% 的 SGs 后，训练动态曲线几乎不变，说明识别方法具有鲁棒性。

### 模块二：HICRA 优势计算

该模块以标准 GRPO 的组归一化优势为基础，对识别出的规划 tokens 进行差异化调制。GRPO 的优势定义为：

$$\hat{A}_{i,t} = R(\mathbf{q}, \mathbf{o}_i) - \frac{1}{G} \sum_{j=1}^{G} R(\mathbf{q}, \mathbf{o}_j)$$

HICRA 在此基础上对规划 tokens 进行优势放大：

$$\hat{A}_{i,t}^{\mathrm{HICRA}} = \begin{cases} \hat{A}_{i,t} + \alpha \cdot |\hat{A}_{i,t}| & \mathrm{if~} t \in S_i \\ \hat{A}_{i,t} & \mathrm{if~} t \notin S_i \end{cases}$$

其中 $\alpha$ 控制放大强度，$S_i$ 为轨迹 $i$ 中规划 tokens 的位置集合。这一设计的直观含义是：对成功轨迹（$\hat{A}_{i,t} > 0$）中的规划 tokens 给予更多正向信用，对失败轨迹（$\hat{A}_{i,t} < 0$）中的规划 tokens 则减轻惩罚。非规划 tokens 保持原始优势不变。

### 模块三：策略梯度更新

利用修改后的 HICRA 优势计算策略梯度，驱动模型参数更新：

$$\nabla \mathcal{I}(\theta) = \mathbb{E} \left[ \hat{A}_{i,t}^{\mathrm{HICRA}} \cdot \nabla \log \pi_{\theta}(o_{i,t} | \mathbf{q}, \mathbf{o}_{i,<t}) \right]$$

从目标分布视角看，标准策略梯度隐含的各向同性目标分布为 $\pi^{*}(o_{i,t} | \mathbf{q}, \mathbf{o}_{i,<t}) \propto \pi_{\theta_{old}}(o_{i,t} | \mathbf{q}, \mathbf{o}_{i,<t}) \exp(\hat{A}_{i,t})$，而 HICRA 通过放大规划 tokens 的优势项 $\exp(\hat{A}_{i,t})$，将目标分布拉伸为各向异性——概率质量集中在规划 tokens 维度上，从而促进战略探索。

### 输入输出流

整个 pipeline 的输入包括：训练问题集 $\{\mathbf{q}\}$、模型当前策略 $\pi_\theta$、以及预提取的 Strategic Grams 集合。每个训练步的流程为：

1. 模型采样生成多条轨迹 $\{\mathbf{o}_i\}$；
2. 根据 SGs 集合标记每条轨迹中的规划 token 位置 $S_i$；
3. 计算每条轨迹的奖励 $R(\mathbf{q}, \mathbf{o}_i)$ 和 GRPO 优势 $\hat{A}_{i,t}$；
4. 对规划 tokens 应用 HICRA 优势调制，得到 $\hat{A}_{i,t}^{\mathrm{HICRA}}$；
5. 计算策略梯度并更新模型参数。

这一框架的核心设计选择在于：**仅修改信用分配（优势函数），不引入额外的损失项或奖励塑形**，从而保持与 GRPO 训练流程的高度兼容性。



### 方法总览

HICRA 的核心设计围绕一个关键观察展开：RL 训练中，大语言模型的推理过程涌现出层次化结构——高层战略规划 tokens 与低层执行 tokens 在功能上分化，且性能提升的主要瓶颈从早期的过程可靠性巩固转移到后期的战略探索。然而，标准 GRPO 对所有 tokens 施加各向同性的优化压力，导致学习信号在大量低层 tokens 上被稀释。HICRA 通过识别规划 tokens 并对其优势函数进行定向放大，将优化压力集中到高层策略维度，从而更高效地推动战略探索。

### 核心模块

HICRA 由三个关键模块构成：

**模块一：Strategic Grams 识别管道**

该模块从训练数据中自动提取代表高层战略功能的 n-gram，作为规划 tokens 的功能代理。具体而言，Strategic Grams（SGs）被定义为引导推理逻辑流的语义单元，主要承担三类逻辑操作：（a）演绎推理（deduction），（b）分支探索（branching），（c）回溯修正（backtracing）。识别管道基于统计频率和语义功能进行筛选，人工验证表明 86% 的 SGs 确实承担引导推理流程或提出计划的功能。灵敏度分析进一步证实，随机删除 30% 的 SGs 后，训练动态曲线几乎不变，表明该识别方法具有鲁棒性。

**模块二：HICRA 优势计算**

在标准 GRPO 中，每个 token 的优势函数由组归一化奖励定义。HICRA 在此基础上对规划 tokens 进行优势放大：对于成功轨迹（$\hat{A}_{i,t} > 0$），放大规划 tokens 的正向信用；对于失败轨迹（$\hat{A}_{i,t} < 0$），则抑制其惩罚信号。非规划 tokens 的优势保持不变。

**模块三：策略梯度更新**

利用修改后的 HICRA 优势函数计算策略梯度，驱动模型参数更新。由于优势函数在规划 tokens 维度上被拉伸，由此产生的隐式目标分布呈各向异性，概率质量向战略维度集中，从而促进多样化的战略探索。

### 关键公式

**GRPO 优势函数**

$$\hat{A}_{i,t} = R(\mathbf{q}, \mathbf{o}_i) - \frac{1}{G} \sum_{j=1}^{G} R(\mathbf{q}, \mathbf{o}_j)$$

其中，$\hat{A}_{i,t}$ 表示第 $i$ 条轨迹中第 $t$ 个 token 的优势，$R(\mathbf{q}, \mathbf{o}_i)$ 为问题 $\mathbf{q}$ 下输出 $\mathbf{o}_i$ 的奖励，$G$ 为组内样本数。该优势通过组内奖励均值中心化实现归一化。

**HICRA 优势函数**

$$\hat{A}_{i,t}^{\mathrm{HICRA}} = \begin{cases} \hat{A}_{i,t} + \alpha \cdot |\hat{A}_{i,t}| & \mathrm{if~} t \in S_i \\ \hat{A}_{i,t} & \mathrm{if~} t \notin S_i \end{cases}$$

其中，$S_i$ 为第 $i$ 条轨迹中规划 tokens 的位置集合，$\alpha$ 为放大系数。当 token 属于规划 tokens 时，其优势被额外加上 $\alpha \cdot |\hat{A}_{i,t}|$——成功轨迹中正向优势被放大，失败轨迹中负向优势的绝对值被增加（即惩罚被抑制，因为 $|\hat{A}_{i,t}|$ 为正值，加到负值上使其更接近零）。这一设计的关键在于：它不改变优势的符号方向，而是调节其幅度，从而在不破坏优化方向的前提下集中学习压力。

**HICRA 策略梯度**

$$\nabla \mathcal{I}(\theta) = \mathbb{E} \left[ \hat{A}_{i,t}^{\mathrm{HICRA}} \cdot \nabla \log \pi_{\theta}(o_{i,t} | \mathbf{q}, \mathbf{o}_{i,<t}) \right]$$

该梯度与标准策略梯度形式一致，区别仅在于将 $\hat{A}_{i,t}$ 替换为 $\hat{A}_{i,t}^{\mathrm{HICRA}}$。由于规划 tokens 上的优势被放大，梯度更新的主要分量集中在这些 tokens 对应的参数方向上。

### 从优势放大到战略探索

标准策略梯度隐含的目标分布为：

$$\pi^{*}(o_{i,t} | \mathbf{q}, \mathbf{o}_{i,<t}) \propto \pi_{\theta_{old}}(o_{i,t} | \mathbf{q}, \mathbf{o}_{i,<t}) \exp(\hat{A}_{i,t})$$

该分布在所有 token 维度上各向同性。HICRA 通过将 $\hat{A}_{i,t}$ 替换为 $\hat{A}_{i,t}^{\mathrm{HICRA}}$，使目标分布在规划 tokens 维度上被指数级拉伸，概率质量向战略维度集中。这等效于在策略空间中施加各向异性的探索压力，推动模型在高层策略层面进行更丰富的尝试。

### 与熵基方法的本质区别

HICRA 与熵正则化、高熵优势放大等方法的关键差异在于目标维度。熵正则化对所有 tokens 施加无差别的熵奖励，虽然提高了 token 级熵，但未能提升准确率，反而导致序列长度失控增长。高熵优势放大仅以统计不确定性为代理，但实验表明仅有不到 10% 的高熵 tokens 具有规划功能。HICRA 直接定位到规划 tokens 的语义功能，避免了在大量低层执行 tokens 上的无效探索。



## 实验与关键发现

### 主要结果：HICRA在文本与多模态推理上的全面增益

HICRA在所有测试的文本模型与基准上始终优于GRPO基线。Table 1汇总了核心结果，其中Qwen3-4B-Instruct-2507在AIME24上取得+5.4的提升（73.1 vs 68.5），AIME25上+5.1（65.1 vs 60.0）；Qwen3-4B-Base在Math500上提升+6.0（89.0 vs 83.0）；Qwen2.5-7B-Base在AMC23上增益最大，达+8.4（55.1 vs 46.7）。对于Qwen3-4B-Adaptive（No-Think）模型，HICRA同样在AIME24、AIME25和AMC23上分别取得+2.8、+3.3和+5.7的提升，表明该方法对具有不同推理风格的基座模型均有效。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_NlkykTqAId/figures/004_Table_1.jpg]]
*Table 1: Comparison of HICRA, GRPO, and Base models across various mathematical reasoning benchmarks. HICRA consistently outperforms all baselines across different base models, demonstrating the effectiveness of focusing optimization on strategic planning tokens*

多模态推理场景下，HICRA的优势同样显著。Table 3显示，在MiMO-VL-Instruct-2508上，HICRA在MathVista上取得+7.0的增益（80.7 vs 73.7），在MathVision上取得+6.1（48.9 vs 42.8）。这验证了层次化信用分配策略跨模态的泛化能力。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_NlkykTqAId/figures/039_Table_3.jpg]]
*Table 3: Comparison of HICRA, GRPO on multimodal reasoning benchmarks*

### 层次推理动态：战略规划是RL训练的主要瓶颈

Figure 3展示了RL训练过程中错误类型的演化：在所有模型上，**规划与策略错误**（红色）的减少幅度显著大于其他程序性错误（灰色）。这表明RL训练的主要收益来源于纠正高层战略故障，而非低层执行细节的打磨。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_NlkykTqAId/figures/007_Figure_3.jpg]]
*Figure 3: Training Dynamics of Error Types. Across all models, the number of Planning & Strategy errors (red) decreases more significantly than other procedural errors (gray), indicating that RL’s primary benefit comes from correcting high-level strategic faults*

这一发现与Figure 2揭示的两阶段动态一致。训练初期（阶段①），模型专注于程序性巩固——执行tokens的相对困惑度和token级熵急剧下降，反映模型对低层操作建立了高度确信。随后学习前沿转移到阶段②，模型开始探索并掌握高层规划，表现为战略gram的语义熵持续上升，同时验证准确率持续提升、推理链长度增长。

### HICRA促进多样化战略探索

Figure 4直接对比了HICRA与GRPO的训练动态。HICRA在整个训练过程中维持了更高的语义熵，且该指标与验证准确率强相关。这表明HICRA通过放大规划tokens的信用分配，有效地促进了更丰富的战略探索，而非仅仅增加低层措辞的随机性。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_NlkykTqAId/figures/009_Figure_4.jpg]]
*Figure 4: HICRA improves GRPO Clip-Higher via more diverse strategic exploration*

Figure 11在MiMO-VL上的实验进一步巩固了这一结论：在该VLM上，token级熵在训练中急剧崩溃（从约0.85降至0.15），但语义熵保持高位且能预测验证准确率。尽管Pass@8在两种方法间趋于饱和且不可区分，语义熵曲线却揭示了HICRA持续的探索优势，这最终转化为更好的最终性能。

### 消融实验：规划token识别是关键

**Placebo HICRA**实验验证了SG识别管道的必要性。Table 1中，使用随机n-gram的Placebo HICRA在Qwen2.5-7B-Base上的效果显著低于真正的HICRA，证明仅放大任意tokens的优势函数无法带来增益——必须精确瞄准具有规划功能的语义单元。

**灵敏度分析**（Figure 7、Figure 8）表明SG识别方法具有鲁棒性：随机删除30%的Strategic Grams后，语义熵等训练动态曲线几乎保持不变，说明识别出的SG集合具有充分的冗余和代表性。

**与熵基方法的对比**（Figure 5）揭示了功能导向识别相对于统计不确定性导向的优越性。Entropy Regularization基线虽然提高了所有tokens的token级熵，但未能持续提升准确率，反而导致序列长度不受控制地增长。High-Entropy Advantage基线仅对高熵tokens调制优势函数，效果同样不理想。Figure 12和Figure 13解释了根本原因：虽然大多数规划tokens确实是高熵的（位于top 30%），但反向关系不成立——不到10%的高熵tokens具有规划功能。绝大多数高熵tokens仅反映了措辞层面的变化，分散在低层执行中，对战略探索无实质贡献。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_NlkykTqAId/figures/013_Figure_5.jpg]]
*Figure 5: HICRA vs. Entropy Regularization on Qwen2.5-7B-Base. While entropy regularization increases token-level entropy, it fails to consistently improve accuracy and leads to uncontrolled length scaling. In contrast, HICRA boosts semantic entropy, which strongly correlates with validation accuracy, demonstrating the superiority of targeted strategic exploration*

### 失败模式与边界条件

HICRA的有效性存在明确的边界条件：**它依赖于基座模型的过程可靠性**。Figure 14展示了HICRA在Llama-3.1-Instruct-8B上的失败案例。当基座模型的程序性技能不足时（该模型在RL训练初期表现出消失的优势和混乱的训练动态），对规划tokens的策略放大反而适得其反，语义熵趋势与Qwen模型相反。这一发现提示，HICRA适用于已具备基本执行能力的模型，其价值在于加速高层战略探索，而非弥补底层技能的缺失。



## 定位与知识库关联

### 1. 与基线方法的关系

HICRA 的核心基线是 **GRPO**（含 clip-higher 变体），后者对所有生成的 token 施加各向同性的优化压力，不区分 token 的功能层次。HICRA 在 GRPO 的优势函数上引入一个关键的修改槽位：对识别出的规划 token 放大优势（$+\alpha |\hat{A}_{i,t}|$），对非规划 token 保持不变。这一修改使策略梯度的隐含目标分布从各向同性变为各向异性，概率质量集中在高层战略维度，从而将优化信号从被稀释的全 token 空间重新聚焦到战略瓶颈上。

在探索性方法维度，HICRA 与两类基于熵的基线形成直接对比：

- **Entropy Regularization**（Cheng et al., 2025）：在 GRPO 上对所有 token 均匀添加熵正则化损失。实验表明，该方法虽能提高 token 级熵，但未能提升准确率，反而导致序列长度不受控制地增长（Figure 5），说明无差别的熵奖励是低效的。
- **High-Entropy Advantage**（Cheng et al. & Wang et al.）：仅对高熵 token 调制优势函数，以统计不确定性作为探索的代理信号。HICRA 的关键区分在于：规划 token 与高熵 token 并不等同——仅有不到 10% 的高熵 token 具有规划功能（Figure 12, D.2.2）。高熵 token 大量分布在低层执行的措辞变化中，而规划 token 是稀疏的战略骨架（Figure 13）。HICRA 通过基于功能的 Strategic Grams 识别管道，精准定位后者，因此在语义熵提升和最终准确率上均优于基于熵的代理方法。

此外，论文还设置了 **Placebo HICRA** 基线——将优势放大应用于随机 n-gram 而非 Strategic Grams。该基线效果显著低于真正的 HICRA（Table 1, Qwen2.5-7B-Base），直接验证了规划 token 识别（而非简单的优势扰动）是性能提升的必要条件。

在更广泛的 RL for reasoning 谱系中，论文将 HICRA 与 **ORZ**（Hu et al., 2025）和 **SimpleRL**（Zeng et al., 2025）等同期工作并置，但未提供与这些方法的直接实验对比。

### 2. 适用边界与失效条件

HICRA 的有效性存在明确的边界条件，其核心前提是**基础模型的过程可靠性**（procedural reliability）。当基础模型在低层执行技能上已经具备一定能力时，RL 训练的瓶颈自然转移到高层战略规划，HICRA 的聚焦放大机制才能发挥正向作用。反之，当基础模型的程序性技能严重不足时，战略放大可能适得其反。

这一边界条件在 Llama-3.1-Instruct-8B 上得到了清晰的验证（Figure 14, D.2.3）：在该模型上，HICRA 未能提供优势，语义熵趋势与 Qwen 系列相反，表明当模型尚未完成 Phase ① 的过程巩固时，强行放大规划 token 的信号无法产生正向效果。论文针对该模型额外引入了动态过滤机制以处理消失优势问题，但效果仍不理想。

从领域范围看，当前验证主要局限于数学推理（AIME24/25、Math500、AMC23、Minerva、Olympiad）和多模态数学推理（MathVista、MathVision）。对代码生成、代理工具使用等更广泛的推理任务的泛化性尚未验证。

### 3. 局限与开放问题

**已知局限：**

1. **依赖预定义 Strategic Grams**：SG 识别管道基于统计频率自动提取，可能与训练任务绑定，未实现完全自适应的层次发现。低频但重要的战略表述可能被遗漏。
2. **过程可靠性前提**：如前所述，HICRA 对基础模型的能力有隐性要求，缺乏对异质基础模型的自适应机制。
3. **领域泛化未验证**：实验局限于数学推理，层次推理原理在其他领域的适用性有待检验。
4. **α 参数的敏感性**：优势放大的幅度由超参数 α 控制，论文未系统报告 α 的敏感性分析或自适应调节策略。

**开放问题：**

1. **跨领域泛化**：如何将层次推理原理推广到代码生成、代理工具使用等更广泛的领域？这些领域中“规划 token”的定义和识别方式可能需要根本性的调整。
2. **自适应层次发现**：如何设计模型感知的层次方法，根据基础模型的过程可靠性自动决定是否以及如何施加层次化的信用分配？能否实现完全无监督的层次结构发现，无需预定义 Strategic Grams？
3. **语义熵作为通用度量**：论文表明语义熵与验证准确率强相关，且在 Pass@8 饱和时仍能揭示 HICRA 的持续探索优势（Figure 11, MiMO-VL）。语义熵是否可以作为更通用的探索质量度量指标，指导 RL 训练的早停或超参数选择？
4. **规模化行为**：两阶段动态（先过程巩固，后战略探索）在更大规模模型上是否依然成立？模型规模是否会影响两个阶段的相对时长和转换时机？



## 原文 PDF

![[paperPDFs/ICLR_2026/Emergent_Hierarchical_Reasoning_in_LLMs_through_Reinforcement_Learning.pdf]]
