---
title: "RL Squeezes, SFT Expands: A Comparative Study of Reasoning LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RL_Squeezes_SFT_Expands_A_Comparative_Study_of_Reasoning_LLMs.pdf
project_link: null
code_link: null
openreview_forum_id: N2lMNqJsBw
aliases:
- TLSLAF
- RSSECSRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "RL通过优化可验证奖励来重新分配概率质量，压缩错误的推理路径并集中功能于少数关键步骤；SFT通过模仿教师轨迹扩展正确的推理路径并使功能均匀分布。"
primary_logic: "RL和SFT以互补的方式影响推理过程：RL压缩错误轨迹和集中图功能，SFT扩展正确轨迹和分散功能，这解释了两阶段训练（SFT后接RL）的成功，并为数据构建和高效学习提供了新方向。"
claims:
- "RL显著减少了不正确轨迹的数量，而SFT增加了正确轨迹的数量。"
- "RL将节点访问频率、度和介数中心性的指数衰减率提升约2.5倍，而SFT将其降低至约三分之一。"
- "SFT+RL组合通过SFT扩展正确轨迹并随后由RL压缩错误轨迹，最大化Pass@1性能。"
- "AIME24, AIME25, AMC23 上 独特错误轨迹数量 = RL模型"
---

# RL Squeezes, SFT Expands: A Comparative Study of Reasoning LLMs

> [!tip] 核心洞察
> RL和SFT以互补的方式影响推理过程：RL压缩错误轨迹和集中图功能，SFT扩展正确轨迹和分散功能，这解释了两阶段训练（SFT后接RL）的成功，并为数据构建和高效学习提供了新方向。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RL压缩，SFT扩展：推理大语言模型的比较研究 |
| 英文题名 | RL Squeezes, SFT Expands: A Comparative Study of Reasoning LLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=N2lMNqJsBw) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | 推理路径分析框架（Trajectory-level and Step-level Analysis Framework） |
| Dataset | AIME24, AIME25, AMC23 |

> [!tip] 效果简介
> - AIME24, AIME25, AMC23 上，独特错误轨迹数量 为 RL模型，对比 Base模型，变化 显著减少，错误路径被压缩。
> - AIME24, AIME25, AMC23 上，独特正确轨迹数量 为 SFT模型，对比 Base模型，变化 明显增加，正确路径被扩展。
> - AIME24, AIME25, AMC23 上，指数衰减率β（频率/度/介数） 为 RL模型，对比 Base模型，变化 β显著增大（约2.5倍），功能集中于少步骤。

## 概要

现有推理大语言模型的主流训练范式遵循“监督微调（SFT）后接强化学习（RL）”的两阶段流程，但对该流程有效性的理解长期停留在准确率度量的表象层面，缺少对RL与SFT如何内在重塑推理过程的机制性认识。这一瓶颈导致当前训练策略的改进依赖于试错，而非基于因果关系的理性设计。

本文的核心洞察是：**RL与SFT以互补的方式影响推理过程**。RL通过优化可验证奖励来重新分配概率质量，压缩错误的推理路径，并将推理图的功能集中于少数关键步骤；SFT则通过模仿教师轨迹扩展正确的推理路径，并使功能均匀分布于更多步骤。这一“RL压缩，SFT扩展”的二元机制，从轨迹级和步骤级两个层面解释了两阶段训练的成功——SFT先扩展正确轨迹空间，RL随后压缩错误轨迹，从而最大化Pass@1性能。

为揭示上述机制，论文提出了一套**推理路径分析框架**，在轨迹级通过聚类识别独特推理路径，在步骤级构建推理图并量化节点频率、度和介数中心性的指数衰减率等拓扑度量。实验覆盖1.5B至14B规模的模型，在AIME24、AIME25、AMC23及HumanEval等数学与代码基准上一致表明：RL将图度量的指数衰减率提升约2.5倍（功能集中），SFT将其降低至约三分之一（功能分散）；RL显著减少独特错误轨迹数量，SFT则增加独特正确轨迹数量。这些发现为数据构建策略和高效学习路径的设计提供了新的方向。



大规模语言模型（LLM）在数学推理、代码生成等复杂任务上的能力近年来取得了显著进展。当前的主流训练范式通常采用两阶段策略：先通过监督微调（SFT）让模型模仿专家或教师模型的推理轨迹，再通过强化学习（RL）进一步优化模型，使其在可验证奖励信号（如答案正确性）的引导下提升推理准确率。这一范式已在多个前沿模型中展现出强大的性能。

然而，现有研究主要基于准确率度量（如Pass@k）来评估不同训练方法的有效性，缺少对RL和SFT如何内在重塑推理过程的理解。这种“黑箱”式的评估方式使得当前的两阶段训练策略在很大程度上依赖于试错：研究者并不清楚SFT和RL各自在推理的哪些维度上发挥作用，以及两者之间是否存在协同或拮抗效应。**该研究的核心瓶颈在于**：我们缺乏一个能够量化推理路径结构变化、揭示训练方法如何影响模型推理行为机制的分析框架。

具体而言，以下问题长期未得到充分回答：RL在优化奖励信号时，是仅仅让模型更频繁地选择已有的正确推理路径，还是从根本上改变了模型探索推理空间的方式？SFT在扩展正确推理轨迹的同时，是否也引入了冗余或次优的推理模式？两阶段训练（SFT后接RL）之所以有效，其内在机理是什么？回答这些问题不仅有助于理解现有方法的成功原因，更能为数据构建策略和高效学习算法提供理论指导。

针对上述缺口，该工作提出了一个系统的推理路径分析框架，从轨迹级（trajectory-level）和步骤级（step-level）两个粒度量化RL和SFT对推理过程的影响。其核心洞察是：RL和SFT以互补的方式重塑推理过程——**RL压缩错误的推理轨迹并将图功能集中于少数关键步骤，而SFT扩展正确的推理轨迹并使功能均匀分布于多个步骤**。这一发现为两阶段训练的成功提供了机制性解释，并为后续研究开辟了新的方向。

> **注意**：该研究主要在1.5B至14B参数规模的模型上进行分析，实验覆盖数学（AIME24、AIME25、AMC23）和代码（HumanEval）领域。更大规模模型及更广泛任务上的泛化性尚待进一步验证。



## 核心方法与创新机理

本研究的核心创新不在于提出新的训练算法或模型架构，而在于**构建了一个系统性的推理路径分析框架**，首次从轨迹级和步骤级两个层次，定量揭示了RL（强化学习）与SFT（监督微调）对推理大语言模型内在推理过程的**互补性重塑机制**。

### 关键洞察：RL压缩，SFT扩展

现有研究主要基于准确率度量评估训练方法，缺少对RL和SFT如何内在重塑推理过程的理解。本工作通过分析框架发现了一个核心因果机制：

- **RL通过优化可验证奖励来重新分配概率质量**，压缩错误的推理路径，并将图功能（如枢纽节点、高介数中心性节点）集中于少数关键步骤。
- **SFT通过模仿教师轨迹**，扩展正确的推理路径，并使功能均匀分布于更多步骤。

这一“压缩-扩展”的互补机制解释了当前两阶段训练策略（SFT后接RL）的成功：SFT首先扩展正确轨迹的多样性，随后RL压缩错误轨迹，二者协同最大化Pass@1性能。

### 方法创新：双层次分析框架

与以往仅关注最终准确率的工作不同，本研究提出了一个**推理路径分析框架**，包含两个互补的分析层次：

1. **轨迹级分析（Trajectory-level Analysis）**：对每个问题采样$M=256$个推理响应，使用基于字符n-gram的**chrF相似度**（$\mathrm{chrF}_{\beta} = (1 + \beta^2) \frac{\mathrm{CHRP} \cdot \mathrm{CHRR}}{\beta^2 \cdot \mathrm{CHRP} + \mathrm{CHRR}}$）和UPGMA层次聚类，识别独特正确/错误推理轨迹的数量变化，从而量化RL和SFT对推理路径多样性的影响。

2. **步骤级分析（Step-level Analysis）**：将推理响应分割为句子，通过嵌入（BGE-large-en-v1.5, $d=1024$）和K-means聚类（$K=2000$）构建**推理图**，节点代表语义相似的推理步骤，边编码步骤间的转移频率和语义距离。在此基础上，通过估计节点访问频率、度和介数中心性的**指数衰减率**$\beta$（$\log_{10} X(R) = \alpha - \beta R + \epsilon_R$），量化功能在推理步骤间的集中/分散程度。

### 关键发现与changed slots

本研究的核心发现揭示了RL和SFT在以下维度上的差异化影响：

| 分析维度 | RL的影响 | SFT的影响 |
|---------|---------|---------|
| 错误轨迹数量 | **显著减少**，错误路径被压缩 | 影响不显著 |
| 正确轨迹数量 | 影响不显著 | **明显增加**，正确路径被扩展 |
| 指数衰减率$\beta$（频率/度/介数） | **增大约2.5倍**，功能集中于少步骤 | **降至约1/3**，功能分散于多步骤 |
| 图拓扑结构 | 增加局部循环结构（G7, G8），反映回溯与验证 | 与RL类似地引入循环，但全局拓扑不同 |
| 全局图度量 | 保持较高模块性 | 降低模块性，提高全局效率和代数连通性 |

这些发现不仅解释了SFT+RL两阶段训练的有效性，还为数据构建和高效学习提供了新方向——例如，是否可以仅在功能步骤（如枢纽节点）上应用RL以进一步提升效率。



![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_N2lMNqJsBw/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our analysis. (Top) RL compresses incorrect trajectories, and SFT expands correct trajectories. (Bottom) RL concentrates functionality (e.g., hubs) in a small number of steps, and SFT distributes functionality more uniformly across many steps*

### 研究动机与核心问题

现有推理大语言模型（LLM）的训练范式普遍采用“监督微调（SFT）+ 强化学习（RL）”两阶段策略，但其有效性主要基于最终准确率度量来评估，缺乏对两种训练方法如何内在重塑推理过程的理解。换言之，RL和SFT各自在推理空间中施加了怎样的结构性改变，以及它们为何能协同工作，仍是一个开放问题。该研究的核心瓶颈在于：当前两阶段训练策略本质上依赖于试错，缺少对推理路径形成机制的过程级认知。

### 分析框架总览

为回答上述问题，本文提出一个**双层分析框架**，从轨迹级（Trajectory-level）和步骤级（Step-level）两个粒度量化推理路径的变化（Figure 1）。该框架不提出新的训练算法，而是构建一套可比较的度量体系，用于刻画Base、RL、SFT及SFT+RL四类模型在推理过程中的结构差异。

**轨迹级分析**关注完整推理响应的多样性：对每个问题从模型中采样多条推理轨迹，通过聚类识别独特的正确和错误推理路径，从而量化RL和SFT对推理空间“广度”的影响。

**步骤级分析**将推理过程抽象为图结构：将模型输出分割为句子，嵌入后聚类为节点，再根据句子间的转移关系构建推理图（Reasoning Graph）。在此基础上，通过节点访问频率、度分布、介数中心性等图度量指标的指数衰减率，以及全局拓扑特性（模块性、全局效率、代数连通度等），刻画RL和SFT对推理过程“深度”功能分布的影响。

### 核心发现

该框架揭示了RL和SFT以互补方式重塑推理过程的机制（Figure 1）：

- **RL压缩错误轨迹，集中功能于关键步骤**：RL通过优化可验证奖励，将概率质量从错误路径重新分配到正确路径，显著减少独特错误轨迹的数量；同时，RL使推理图中的节点访问频率、度和介数中心性的指数衰减率增大约2.5倍，表明功能（如枢纽节点）高度集中于少数关键推理步骤。

- **SFT扩展正确轨迹，使功能均匀分布**：SFT通过模仿教师轨迹，增加了独特正确轨迹的数量，扩展了正确推理路径的空间；同时，SFT将上述图度量的指数衰减率降低至约三分之一，表明功能更均匀地分散于多个推理步骤。

- **两阶段协同机制**：SFT+RL的组合策略恰好利用了这种互补性——SFT先扩展正确轨迹空间，为后续RL提供更丰富的优化基础；RL随后压缩错误轨迹并集中功能，最终最大化Pass@1性能。这一发现从推理结构层面解释了SFT后接RL这一经验策略有效性的内在原因。

### 方法谱系与知识库定位

本工作定位于推理过程分析与理解，而非提出新的训练方法。与直接优化准确率的主流训练研究不同，该框架借鉴了图论和复杂网络分析的工具（如指数衰减模型、图元分析、全局拓扑度量），将其应用于LLM推理过程的表征。在方法谱系上，它连接了三个方向：推理轨迹多样性分析（通过chrF聚类）、推理步骤的语义空间建模（通过句子嵌入和图构建）、以及图结构的功能度量（通过衰减率和拓扑指标）。这种跨学科的分析视角为理解RL和SFT的内在机制提供了新的概念工具，并指出了潜在的高效学习方向——例如，仅在功能步骤（枢纽节点或高介数中心步）上应用RL是否能进一步提升性能。



### 轨迹采样与聚类模块

研究对每个问题从Base、RL、SFT和SFT+RL模型采样$M=256$个推理响应（温度0.6），形成原始分析数据。轨迹级分析的核心在于识别独特推理路径：首先计算轨迹间的**chrF相似度**，其定义为字符n-gram精确率与召回率的加权调和平均：

$$\mathrm{chrF}_{\beta} = (1 + \beta^2) \frac{\mathrm{CHRP} \cdot \mathrm{CHRR}}{\beta^2 \cdot \mathrm{CHRP} + \mathrm{CHRR}}$$

其中CHRP和CHRR分别为字符级n-gram的精确率和召回率。基于该相似度，计算轨迹间距离$d_{i,j} = 1 - s_{i,j}$，随后采用**UPGMA层次聚类**并以相似度阈值60切割树状图，将语义相近的推理响应归入同一轨迹簇，从而区分独特正确轨迹与独特错误轨迹。

### 推理图构建模块

步骤级分析将推理响应按句子分割，通过**BGE-large-en-v1.5**嵌入模型将每个句子映射为$d=1024$维向量。在共享的句子嵌入空间中，对全体句子集合$S$执行**K-means聚类**（$K=2000$），每个簇的质心$c_i$构成推理图节点$v_i$。节点间距离定义为质心的欧氏距离：

$$d(v_i, v_j) = \|c_i - c_j\|_2$$

图的边由句子在原始推理轨迹中的相邻关系决定，边权重编码转移频率，边颜色编码节点距离。由于所有模型共享同一嵌入空间，该构建方式保证了不同训练方法下推理图结构的直接可比性。为控制噪声，后续对图进行稀疏化处理，每个节点仅保留欧氏距离最小的top-10或top-20条边。

### 指数衰减度量模块

推理图中节点的重要性度量（访问频率、度、介数中心性）按位次$R$排序后近似服从指数衰减规律：

$$X(R) \propto e^{-\lambda R}$$

其中$\lambda$为衰减速率。为量化该规律，采用对数-线性回归估计衰减率$\beta$：

$$\log_{10} X(R) = \alpha - \beta R + \epsilon_R, \quad \beta = \frac{\lambda}{\log 10}$$

$\beta$越大，表明图功能越集中于少数高排名节点（枢纽化）；$\beta$越小，则功能越均匀地分散于众多节点。该度量是本文刻画RL“压缩”与SFT“扩展”效应的核心定量指标。

### 全局拓扑度量模块

在稀疏化后的推理图上计算八种拓扑度量以刻画全局结构，其中包括：

- **介数中心性**：衡量节点在图中介导最短路径的重要性，定义为通过该节点的最短路径数占总最短路径数的比例：

$$\frac{1}{(|\mathcal{V}^l|-1)(|\mathcal{V}^l|-2)} \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$

其中$\sigma_{st}$为节点$s$到$t$的最短路径总数，$\sigma_{st}(v)$为经过$v$的最短路径数。

- **模块度**：衡量图划分成紧密子图的程度，Base模型呈现高模块度，而SFT和SFT+RL模型显著降低该值。

- **全局效率**与**代数连通度**：衡量图的整体信息传输效率，与Pass@1/Pass@k性能呈正相关。

此外，通过**图元分析**考察四节点连通非同构诱导子图（G3–G8）的比例分布，揭示RL增加局部循环结构（G7、G8）、减少无环结构（G3、G4）的微观模式。

### 模型间相似度度量

为量化不同训练阶段模型在节点访问模式上的相似程度，引入**对称平均绝对百分比误差**：

$$\mathrm{sMAPE} = \frac{100}{n} \sum_{t=1}^{n} \frac{|y_t - x_t|}{(|y_t| + |x_t|)/2}$$

其中$x_t$和$y_t$分别为两模型在第$t$个节点上的访问频率，$n$为节点总数。该度量用于验证RL和SFT对推理图功能分布的差异化塑造是否具有统计一致性。



## 实验与关键发现

### 轨迹级分析：RL压缩错误，SFT扩展正确

研究首先在轨迹层面量化RL与SFT对推理路径多样性的影响。对每个问题采样M=256条响应（温度0.6），通过chrF字符级相似度与UPGMA层次聚类（相似度阈值60）识别独特正确/错误轨迹簇。

核心发现：**RL显著减少错误轨迹数量，SFT显著增加正确轨迹数量**。如Figure 2所示，在1.5B模型上，无论从Base模型还是SFT模型出发应用RL，错误轨迹簇数均大幅下降；而从Base模型应用SFT，正确轨迹簇数明显上升。这一模式在7B模型的代码领域（HumanEval, Figure 3）同样成立，表明RL和SFT对推理路径的影响具有跨领域一致性。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_N2lMNqJsBw/figures/003_Figure_2.jpg]]
*Figure 2: Effect of RL and SFT on the Number of Unique Trajectories. The x-axis represents the number of correct clusters and the y-axis represents the number of incorrect clusters for trajectories before and after training of 1.5B models in Table 1. Plot shows the average across samples. See Appendix C.3 for complete results and for additional results Appendix C.4*

两阶段训练（SFT+RL）的互补机制由此得到解释：SFT先扩展正确推理路径的多样性，为后续RL提供更丰富的正确轨迹池；随后RL压缩错误路径，将概率质量集中于高奖励轨迹，从而最大化Pass@1性能。

### 步骤级分析：RL集缩功能，SFT分散功能

为深入理解训练方法如何重塑推理过程的内在结构，研究构建**推理图**：将模型输出分割为句子，通过BGE-large-en-v1.5嵌入（d=1024）后以K-means（K=2000）聚类定义节点，在共享嵌入空间中跨模型比较图属性。

#### 指数衰减率β：功能集中度的量化指标

推理图中节点访问频率、度、介数中心性随位次R近似服从指数衰减：

$$X(R) \propto e^{-\lambda R}$$

通过对数-线性回归估计衰减率 $\beta = \lambda / \log 10$：

$$\log_{10} X(R) = \alpha - \beta R + \epsilon_R$$

$\beta$ 越大，表明图功能越集中于少数高排名节点（枢纽步骤）；$\beta$ 越小，则功能越均匀分布于多步骤。

**Figure 6的核心结论**：在AIME24/25和AMC23三个数学基准上，RL使$\beta$增至约2.5倍，而SFT使$\beta$降至约1/3。这意味着RL将推理功能压缩至少数关键步骤，SFT则将功能扩展至更多步骤。HumanEval代码领域（Figure 6底部）呈现完全一致的趋势，验证了发现的鲁棒性。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_N2lMNqJsBw/figures/015_Figure_6.jpg]]
*Figure 6: Exponential Decay Rate for Visitation Frequency, Degree, and Betweenness Centrality. Box plots show the estimated exponential decay rate β for the (Top), computed across all problems in AIME24, AIME25, and AMC23 for the 1.5B models in Table 1; and for the (Bottom), computed across all problems in HumanEval for the 7B models in Table 1. See Figure 26 for complete results*

#### 消融验证

- **聚类参数稳健性**：改变K-means聚类数（K=1000, 3000）、使用余弦距离或更换嵌入模型，RL增加$\beta$、SFT减少$\beta$的趋势均保持一致（Figure 32）。
- **图稀疏化**：保留每节点top-10或top-20最近边后，RL仍提高$\beta$，SFT仍降低$\beta$（Figure 33）。

#### 全局拓扑度量

Figure 8对比了八种图度量在Base、RL、SFT、SFT+RL模型间的差异：

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_N2lMNqJsBw/figures/024_Figure_8.jpg]]
*Figure 8: Comparison of eight graph metrics across Base, RL, SFT, and SFT+RL models. Values are averaged across different model sizes in Table 1 and three datasets, AIME24, AIME25, and AMC23. For details on the eight metrics, see Appendix D.3. See Figure 31 for results by model size*

- **Base模型**的推理图呈现高模块性、低全局效率、低代数连通性，表明推理过程高度模块化但信息流动受限。
- **SFT和SFT+RL模型**则表现出低模块性、高全局效率、高代数连通性，说明推理图结构更加整合、信息传递更高效。
- 全局效率与代数连通性与Pass@1/Pass@k正相关，模块性则呈负相关，提示这些图度量可能作为推理性能的代理指标。

#### 局部结构：图元分析

Figure 9展示了四节点图元（G3–G8）的比例分布。RL训练后，无环子图（G3、G4）比例下降，而含环结构（G7、G8）比例上升。这表明RL引入了回溯与验证等局部循环推理模式，与现有关于RL促进自我纠错能力的观察一致。值得注意的是，尽管RL和SFT在局部均产生循环结构，二者在全局拓扑上却截然不同——RL趋向功能集中，SFT趋向功能分散。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_N2lMNqJsBw/figures/026_Figure_9.jpg]]
*Figure 9: Graphlets (G3–G8). (a) 4-node graphlet motifs and (b) their proportions averaged across all models in Table 1 and datasets (AIME24, AIME25, AMC23). Arrows indicate the change in proportion after RL*

### 失败模式与局限性

1. **规模限制**：分析仅覆盖1.5B至14B参数模型，更大规模模型上的功能集缩/分散规律是否持续尚待验证。
2. **领域泛化**：实验集中于数学与代码领域，自然语言推理等更广泛任务中的图结构变化有待探索。
3. **构建敏感性**：推理图构建依赖句子分割、嵌入和聚类参数选择，节点语义的可解释性受嵌入质量和聚类数影响。
4. **RL变体未覆盖**：探索奖励、迭代式RL等变体对推理图结构的潜在影响未被纳入当前分析框架。

### 补充图表

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_N2lMNqJsBw/figures/002_Table_1.jpg]]
*Table 1: Comparison of Model Variants. We evaluate Base, RL, SFT, and SFT + RL models across three sizes, 1.5B, 7B, and 14B. See Appendix B.1 for detailed model specifications*



## 定位与知识库关联

### 分析框架的定位与创新性

本研究提出的**推理路径分析框架**（Trajectory-level and Step-level Analysis Framework）并非一种新的训练方法或模型架构，而是一种**诊断性分析工具**，旨在揭示强化学习（RL）和监督微调（SFT）如何以不同方式重塑大语言模型的推理过程。该框架的核心创新在于将推理行为的分析从传统的准确率度量提升到**轨迹级**和**步骤级**的结构化表征层面，从而捕捉训练方法对推理路径的因果性影响。

在轨迹级，框架通过**chrF字符级相似度**和**UPGMA层次聚类**识别独特正确/错误推理轨迹的聚类数量（Section 3.1），直接量化RL和SFT对推理路径多样性的影响。在步骤级，框架将推理响应分割为句子，使用**BGE-large-en-v1.5**嵌入后通过**K-means聚类**（K=2000）构建共享语义空间中的推理图（Section 4.1），并通过指数衰减率β、图拓扑度量（模块性、全局效率、代数连通性等）和graphlet分析来刻画推理步骤的功能分布与结构特征。

### 与现有方法的关系

本工作处于推理过程分析与训练方法理解这一研究方向的交汇处。现有研究主要依赖**准确率**（如Pass@1、Pass@k）来评估RL和SFT的效果，但缺乏对“如何”和“为什么”这些方法起作用的机制性理解。该框架填补了这一空白，提供了以下关键洞察：

- **RL的“压缩”机制**：RL通过优化可验证奖励，将概率质量从错误推理路径重新分配到少数正确路径上，表现为错误轨迹聚类数量的显著减少（Figure 2）和推理图节点访问频率、度、介数中心性的指数衰减率β约**2.5倍的增大**（Figure 6），即功能集中于少数关键步骤。
- **SFT的“扩展”机制**：SFT通过模仿教师轨迹，增加正确推理路径的多样性，表现为正确轨迹聚类数量的明显增加（Figure 2）和β的显著减小（约至**1/3**），即功能分散于更多步骤。
- **两阶段训练的互补性**：SFT+RL组合通过SFT先扩展正确轨迹空间，再由RL压缩错误轨迹，最大化最终性能，这从机制层面解释了当前主流训练策略的成功原因。

### 适用边界

该分析框架的适用范围受以下因素约束：

1. **模型规模**：分析覆盖1.5B至14B参数规模的模型（Qwen2.5-Math系列和DeepSeek-R1-Distill-Qwen系列），更大规模模型（如70B+）上的推理图结构特性是否遵循相同规律尚待验证。
2. **任务领域**：实验集中在**数学推理**（AIME24、AIME25、AMC23）和**代码生成**（HumanEval）两个领域。尽管在代码领域的图度量趋势与数学领域一致（Figure 37），但该框架在自然语言推理、多跳问答等更广泛任务上的泛化性仍需进一步探索。
3. **训练范式**：分析聚焦于标准的RL（基于可验证奖励的强化学习）和SFT（基于教师轨迹的监督微调），未涵盖RL中的探索奖励、迭代式RL、基于过程奖励的RL等变体对推理图结构的潜在影响。
4. **图构建参数**：推理图的构建依赖于句子分割策略、嵌入模型选择（BGE-large-en-v1.5）和聚类数K=2000。消融实验表明，改变K值（1000、3000）、使用余弦距离或更换嵌入模型时，RL增加β而SFT减少β的趋势保持稳健（Figure 32），图稀疏化（保留top-10或top-20最近边）后趋势同样一致（Figure 33），但节点语义的可解释性仍受聚类质量和嵌入空间对齐程度的影响。

### 局限与开放问题

**已知局限**：
- 分析仅揭示了RL和SFT对推理图结构的**统计性影响**（如β的变化、拓扑度量的差异），但未建立图度量与推理性能之间的直接因果关系。
- 推理图的构建是后验的，无法在训练过程中实时指导模型优化。
- 未区分不同难度或类型的问题对推理图结构的差异化影响。

**开放问题**（源自分析发现）：
1. **高效学习策略**：仅在功能步骤（如枢纽节点或高介数中心步）上应用RL是否能进一步提升推理性能并实现高效学习？这指向一种基于图结构重要性的选择性训练策略。
2. **探索奖励的机制**：RL中的探索奖励机制是仅仅防止推理图的过度压缩（即维持一定的路径多样性），还是能像SFT一样真正扩展推理结构？这需要将探索奖励作为独立变量纳入分析框架。
3. **图度量作为过程奖励**：是否可以将图度量（如枢纽节点和中心节点的识别）作为过程奖励信号整合到RL训练中？这要求建立图度量与推理正确性之间的实时映射。
4. **因果性确定**：图拓扑度量与推理性能之间的因果关系如何确定？能否通过直接优化这些度量（如最大化全局效率、最小化模块性）来指导训练，而不仅仅是事后观察相关性？



## 原文 PDF

![[paperPDFs/ICLR_2026/RL_Squeezes_SFT_Expands_A_Comparative_Study_of_Reasoning_LLMs.pdf]]
