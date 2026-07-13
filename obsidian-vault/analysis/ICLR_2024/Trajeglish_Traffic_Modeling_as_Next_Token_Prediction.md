---
title: "Trajeglish: Traffic Modeling as Next-Token Prediction"
type: paper
paper_level: A
venue: ICLR
year: 2024
pdf_ref: paperPDFs/ICLR_2024/Trajeglish_Traffic_Modeling_as_Next_Token_Prediction.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/trajeglish/
code_link: null
aliases:
- Trajeglish
tags:
- ICLR_2024
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "k-disks分词模板的词汇大小（控制离散化精度）和Transformer解码器中因果掩码策略（控制时间步内交互信息的暴露顺序）是影响生成质量的两个直接因果旋钮。"
primary_logic: "将多智能体轨迹视为离散运动标记序列，并采用GPT风格的编码器-解码器进行时间自回归和步内条件预测，既能利用大规模语言模型的序列建模能力，又能从数据中自然学习到智能体间的交互模式，这是实现高度逼真交通仿真的关键。"
claims:
- "在Waymo Sim Agents测试基准上，Trajeglish在真实感元指标上超越先前最佳方法3.3%，交互指标提升9.9%，是首个在该基准上使用离散序列建模的方法。"
- "k-disks分词方法在词汇量384时达到1.18厘米的期望离散化误差，远优于k-means（6.13厘米）和网格基线方法。"
- "在仅初始化一个时间步的全自主设定下，Trajeglish的碰撞率显著低于忽略时间步内交互的基线，验证了时间步内条件建模的必要性。"
- "将多智能体轨迹视为离散运动标记序列，并采用GPT风格的编码器-解码器进行时间自回归和步内条件预测，既能利用大规模语言模型的序列建模能力，又能从数据中自然学习到智能体间的交互模式，这是实现高度逼真交通仿真的关键。"
---

# Trajeglish: Traffic Modeling as Next-Token Prediction

> [!tip] 核心洞察
> 将多智能体轨迹视为离散运动标记序列，并采用GPT风格的编码器-解码器进行时间自回归和步内条件预测，既能利用大规模语言模型的序列建模能力，又能从数据中自然学习到智能体间的交互模式，这是实现高度逼真交通仿真的关键。

| 字段 | 内容 |
| ------- | ----------------------------------------------------- |
| 中文题名 | Trajeglish：基于下一个标记预测的交通建模 |
| 英文题名 | Trajeglish: Traffic Modeling as Next-Token Prediction |
| 会议/期刊 | ICLR 2024 |
| Links | [paper](https://arxiv.org/abs/2312.04535) · [Project](https://research.nvidia.com/labs/toronto-ai/trajeglish/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Trajeglish |
| Dataset | Waymo Open Motion Dataset Sim Agents Test |

> [!tip] 效果简介
> - 在 Waymo Sim Agents 测试基准上，Trajeglish 的真实感元指标较先前最佳方法提升 3.3%，交互指标提升 9.9%。
> - k-disks 分词在词汇量 384 时达到 1.18 厘米的期望离散化误差，显著优于 k-means 的 6.13 厘米。

## 概要

多智能体交通仿真面临一个双重挑战：既要捕捉每个智能体时间维度上的运动动力学，又要建模同一时间步内智能体之间的交互依赖性。主流方法通常将轨迹预测视为连续回归问题，或对每个智能体进行独立建模，难以在闭环仿真中同时保持场景的全局一致性和交互的真实感。

**Trajeglish** 提出了一种范式转换——将交通建模重新定义为**下一个标记预测**（next-token prediction）任务。其核心思路是：首先通过一种数据驱动的分词策略（k-disks）将连续轨迹以厘米级精度离散化为小词汇量的运动标记序列，然后使用一个类 GPT 的编码器-解码器 Transformer 对该多智能体离散序列进行建模。该模型在时间维度上自回归，并在每个时间步内通过因果掩码暴露已选动作，从而自然地学习智能体间的条件交互。

在 **Waymo Sim Agents 测试基准**上，Trajeglish 在真实感元指标上超越先前最佳方法 **3.3%**，交互指标提升 **9.9%**，成为该基准上首个基于离散序列建模的方法。分词层面，k-disks 在词汇量仅为 384 时即达到 **1.18 厘米**的期望离散化误差，远优于 k-means（6.13 厘米）和网格基线。在仅初始化一个时间步的全自主设定下，Trajeglish 的碰撞率显著低于忽略时间步内交互的基线，验证了步内条件建模对于闭环仿真的关键作用。



### 问题背景：闭环多智能体交通仿真

自动驾驶系统的安全验证依赖高保真的闭环交通仿真。其核心挑战在于生成**多智能体未来轨迹**，这些轨迹不仅需要在个体层面符合运动学约束，更必须在**场景层面保持全局一致性**——即所有智能体的行为要彼此协调、避免碰撞，并共同服从地图拓扑的约束。Waymo Sim Agents Benchmark 正是为此设立的标准化测试，通过“真实感元指标”（Realism Meta Metric）和“交互指标”（Interaction Metric）量化生成轨迹的逼真度。

### 现有方法缺口：连续回归与独立预测的局限

当前主流方法将轨迹建模为**连续空间中的回归问题**，或使用固定网格进行分词。这些方法存在两个结构性缺口：

1. **交互建模不足**：多数方法采用**独立边缘轨迹预测**，即每个智能体的轨迹被单独生成，缺乏对**时间步内交互依赖性**的显式建模。这意味着在同一时间步内，一个智能体的决策无法感知其他智能体正在做出的选择，导致生成的场景在交互层面失真，碰撞率偏高。

2. **表示与架构的割裂**：连续回归虽能保持轨迹精度，但难以与大规模序列模型（如 Transformer）的离散标记预测范式自然对接；而固定网格分词则在高维连续状态空间中引入过大的离散化误差，损失运动保真度。

### 核心瓶颈与本文动机

上述缺口指向一个根本瓶颈：**如何在多智能体闭环场景中，将连续高维轨迹高保真地离散化为低词汇量的离散序列，并有效建模时间步内的交互依赖性，同时维持场景的全局一致性。**

本文的动机正是打破这一瓶颈。作者观察到，自然语言处理领域的大规模序列建模（GPT 风格的自回归 Transformer）在捕捉长程依赖和复杂分布方面展现出了强大能力。如果将多智能体轨迹转化为离散运动标记序列，并将交互建模转化为**时间自回归 + 步内条件预测**的序列生成问题，就有望从数据中自然地学习到智能体间的交互模式，实现高度逼真的交通仿真。

这一思路直接催生了 **Trajeglish**：一个基于下一个标记预测的交通建模框架。其核心设计包括：
- **k-disks 分词器**：以厘米级精度将连续轨迹状态离散化为小词汇量的运动标记，解决连续到离散的高保真映射问题。
- **GPT 式编码器-解码器架构**：在时间维度上自回归地预测下一个动作标记，同时在每个时间步内通过**因果掩码**暴露已选动作，实现时间步内的交互条件建模。

这些设计使 Trajeglish 成为首个在 Waymo Sim Agents 基准上使用离散序列建模的方法，并在真实感元指标上超越先前最佳方法 3.3%，交互指标提升 9.9%（参见 Table 1）。



## 核心方法与创新机理

Trajeglish 的核心创新在于将多智能体交通建模彻底重构为一个**离散序列的下一个标记预测问题**，并围绕这一范式设计了两个紧密耦合的组件：数据驱动的轨迹分词策略与具备时间步内交互建模能力的自回归Transformer架构。这一设计直接回应了闭环仿真中的核心瓶颈——如何在保持场景全局一致性的前提下，对连续高维轨迹进行高保真离散化，并有效捕捉智能体在同一时间步内的相互依赖性。

### 从连续回归到离散分词：k-disks 模板优化

传统方法通常将轨迹预测建模为连续坐标的回归问题，或采用固定网格进行空间离散化。Trajeglish 提出了一种名为 **k-disks** 的迭代式离散分词策略，将智能体的状态转移映射到一个固定词汇量 $V$ 的离散运动标记集合中。

其关键设计在于分词模板的优化目标：在局部坐标系下，以**最小化角点距离**为准则，迭代地将连续状态 $s$ 映射到离散标记 $a_{i^*}$，即

$$f(\pmb{\mathscr{s}}_0, \pmb{\mathscr{s}}) = a_{i^*} = \arg\min_i d_{l,w}(\pmb{\mathscr{s}}_i, \mathrm{local}(\pmb{\mathscr{s}}_0, \pmb{\mathscr{s}}))$$

其中 $d_{l,w}$ 是考虑车辆长宽尺寸的角点距离度量。与 k-means 聚类等通用方法相比，k-disks 算法能够一致地采样到更优的模板集合：在词汇量 $|V|=384$ 时，k-disks 的期望离散化误差仅为 **1.18 厘米**，远优于 k-means 的 6.13 厘米以及网格基线方法（Table 2; Fig. 6; Appendix A.3）。这一精度水平使得离散化过程几乎不损失轨迹的物理保真度，为后续序列建模奠定了可靠基础。

### 从独立预测到时间步内条件建模：因果掩码解码器

在多智能体轨迹生成中，现有方法大多采用**独立边缘预测**策略，即各智能体的轨迹在给定场景上下文后相互独立地生成，忽略了同一时间步内智能体动作之间的耦合效应。Trajeglish 通过 Transformer 解码器中的**因果掩码机制**改变了这一范式。

具体而言，模型将联合似然分解为时间自回归形式，并在每个时间步内进一步按智能体顺序进行条件分解：

$$p(s_t^1, \ldots, s_t^N \mid s_{<t}, c) = \prod_{n=1}^{N} p(s_t^n \mid s_{<t}, s_t^{1:n-1}, c)$$

解码器的因果掩码确保智能体 $n$ 在预测当前动作时，可以“看到”同一时间步内已选定的智能体 $1$ 至 $n-1$ 的动作标记，从而实现了**时间步内的交互条件建模**（Sec 3.2; Eq. 2）。这一设计在架构层面将交互建模从“事后评估”提升为“生成过程的内在约束”。

实验证据有力地支持了这一创新的必要性：在全自主设定下（仅初始化一个时间步），具备时间步内条件建模的 Trajeglish 在车辆碰撞率上显著低于忽略该依赖的“no intra”基线（Fig. 9; Section 4.2）。同时，负对数似然评估表明，智能体确实从同一步内其他智能体的已选动作中获得了额外的预测能力（Fig. 10）。值得注意的是，当提供超过 4 个时间步的历史轨迹时，时间步内依赖的重要性显著下降，这解释了为何传统运动预测基准中这一问题长期被忽视（Section 4.3）。

### 架构层面的系统性重构

上述两项创新被统一在一个 **GPT 风格的编码器-解码器 Transformer** 架构中（Fig. 7; Sec 3.2）。编码器负责融合地图嵌入与智能体初始状态，生成场景上下文表示；解码器则在多智能体标记序列上执行下一个标记预测，时间维度自回归、智能体维度条件生成。这一架构选择使得模型能够自然地从大规模驾驶数据中学习交互模式，而无需显式设计交互规则或联合分布模型。

在训练策略上，Trajeglish 引入了**噪声分词增强**：通过 softmax 核分布采样添加噪声标记作为输入，而预测目标仍为最小距离标记（Sec A.2）。这一技巧缓解了教鞭强制训练与自回归采样之间的分布偏移问题，进一步提升了闭环仿真质量。

综上，Trajeglish 的创新并非单一技术点的改进，而是**表示层（k-disks 分词）、建模层（时间步内因果条件）与架构层（GPT 式序列建模）** 的协同重构，三者共同构成了一个完整的离散序列交通建模范式。



![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2312_04535/figures/015_Figure_15.jpg]]
*Figure 15: Tokenization method comparison Average corner distance for trajectories tokenized with a vocabulary of 384 with template sets derived using different methods*

Trajeglish 将多智能体交通仿真重新表述为**下一个标记预测**问题，整体架构由两个核心组件串联构成：一个数据驱动的轨迹离散分词器（k‑disks tokenizer）与一个 GPT 风格的编码器‑解码器 Transformer。系统的输入是场景上下文（高精地图与智能体历史状态），输出是未来 T 个时间步内所有智能体的离散运动标记序列，这些标记随后可通过渲染器恢复为连续轨迹。

### 输入输出流

模型在每一个仿真时间步接收三类信息：
1. **地图上下文**：由 VectorNet 风格的地图编码器将车道中心线、边界等多段线对象编码为固定长度的嵌入序列。
2. **智能体初始状态**：每个智能体的历史轨迹被转换为初始位姿，作为 Transformer 编码器的输入。
3. **已生成的动作标记**：当前时间步内已采样的其他智能体的离散动作标记，通过因果掩码暴露给解码器。

编码器将这些信息融合为统一的场景上下文表示。解码器在该上下文的基础上，按智能体顺序自回归地预测每个智能体在当前时间步的动作标记分布。预测出的离散标记通过渲染器 `r(·)` 还原为全局坐标系下的连续状态，并作为下一时间步分词器的基状态，实现**时间维度的自回归**滚动。

### 模块关系与数据流

Trajeglish 的 pipeline 可分解为以下模块，其连接关系如 Fig. 7 所示：

1. **k‑disks Tokenizer**（Sec 3.1）：将连续轨迹状态 `s` 转换为离散动作标记 `a_i`。分词过程以迭代方式进行：每一步以当前标记化状态为基，计算下一真实状态在局部坐标系下的相对位姿，并从固定的动作模板集合中选取角距离最小的标记。该模板集合在训练集上通过最小化期望离散化误差离线优化得到，词汇量 |V| 为 384 时，期望离散化误差仅 1.18 厘米，远优于 k‑means（6.13 厘米）和网格基线（Table 2, Fig. 6）。

2. **VectorNet Map Encoder**：将地图多段线对象编码为固定长度的嵌入序列，作为场景静态上下文的表示。

3. **Transformer Encoder**：接收地图嵌入与所有智能体的初始状态嵌入，通过自注意力融合为全局场景上下文表示。编码器**不对全局坐标框架等变**，也**不对智能体顺序置换等变**，这迫使模型从数据中学习空间关系与交互模式。

4. **Transformer Decoder with Causal Mask**（Sec 3.2）：在时间维度上自回归地生成每个时间步的动作标记序列。在单个时间步内，解码器通过因果掩码允许当前智能体关注**同一时间步内已做出决策的其他智能体**，从而显式建模时间步内的交互依赖性。这一设计直接对应联合似然的动态因式分解：

$$
\begin{aligned}
p(s_1^1, ..., s_1^N, ..., s_T^1, ..., s_T^N \mid c) = \prod_{t=1}^{T} \prod_{n=1}^{N} p(s_t^n \mid s_{1:t-1}^{1:N}, s_t^{1:n-1}, c)
\end{aligned}
$$

其中，智能体 n 在时间步 t 的状态不仅条件于所有智能体的历史轨迹，还条件于同一时间步内已采样的前 n‑1 个智能体的动作。这一因式分解保留了测试时的动态交互能力，是 Trajeglish 区别于独立边缘轨迹预测方法的核心机制。

5. **Heading Smoother（可选）**：一个轻量级后处理自回归 Transformer，从离散化轨迹中恢复更精确的原始航向角，以弥补分词过程对航向信息的损失（Sec A.5）。

### 训练策略的关键改进

在训练阶段，Trajeglish 采用一种**噪声分词增强**策略（Sec A.2）：输入给解码器的历史动作标记并非来自精确分词目标，而是从 softmax 核分布中采样得到，而预测目标仍为最小距离标记。这一设计使模型在训练期间即暴露于推理时可能出现的累积误差，增强了闭环滚动的鲁棒性。



Trajeglish 由两个核心组件构成：一个将连续轨迹离散化为运动标记的**分词策略**，以及一个在多智能体标记序列上进行下一个标记预测的**自回归 Transformer 架构**。以下分别阐述这两个模块的设计逻辑与关键公式。

### 1. k-disks 分词器

#### 1.1 设计动机

传统轨迹建模通常采用连续回归或固定网格离散化，前者难以捕获多模态分布，后者在厘米级精度下会导致词汇量爆炸。k-disks 分词器的核心思想是：将轨迹表示为一系列相对位移的离散标记，通过优化一组固定的状态转移模板，在极小词汇量（如 384）下实现厘米级离散化精度。

#### 1.2 分词与渲染公式

给定智能体上一时刻的全局状态 $\boldsymbol{s}_0$（包含位置 $x, y$ 和航向角 $\theta$）以及当前时刻的真实全局状态 $\boldsymbol{s}$，分词器 $f$ 将状态转移映射为离散动作标记 $a_{i^*}$：

$$f(\boldsymbol{s}_0, \boldsymbol{s}) = a_{i^*} = \arg\min_i \; d_{l,w}\big(\boldsymbol{s}_i,\; \text{local}(\boldsymbol{s}_0, \boldsymbol{s})\big)$$

其中：
- $\text{local}(\boldsymbol{s}_0, \boldsymbol{s})$ 将 $\boldsymbol{s}$ 转换到以 $\boldsymbol{s}_0$ 为原点的局部坐标系中；
- $\boldsymbol{s}_i$ 是词汇表中第 $i$ 个模板状态（同样定义在局部坐标系下）；
- $d_{l,w}(\cdot, \cdot)$ 是**角点距离**（corner distance），计算两个车辆包围盒四个角点之间的平均距离，用于更精确地衡量位移差异。

对应的**渲染器** $r$ 将离散标记还原为全局状态：

$$r(\boldsymbol{s}_0, a_i) = \hat{\boldsymbol{s}} = \text{global}(\boldsymbol{s}_0, \boldsymbol{s}_i)$$

其中 $\text{global}(\cdot, \cdot)$ 将局部模板状态 $\boldsymbol{s}_i$ 根据 $\boldsymbol{s}_0$ 的位姿变换回全局坐标系。

#### 1.3 迭代分词过程

完整轨迹的分词是迭代进行的：将上一时刻的分词状态 $\hat{\boldsymbol{s}}_{t-1}$ 作为新的基状态 $\boldsymbol{s}_0$，对下一真实状态 $\boldsymbol{s}_t$ 执行 $f(\hat{\boldsymbol{s}}_{t-1}, \boldsymbol{s}_t)$，得到动作标记 $a_t$。这一过程确保了离散化误差不会跨时间步累积——因为每次分词都以已离散化的状态为基准。

#### 1.4 模板优化

k-disks 通过迭代最小角距离算法（Algorithm 1）从训练数据中采样模板集，而非使用 k-means 聚类。实验表明，在词汇量 $|V|=384$ 时，k-disks 的期望离散化误差仅为 **1.18 厘米**，远优于 k-means 的 6.13 厘米和网格基线方法（Table 2, Fig. 6）。

### 2. 自回归 Transformer 架构

#### 2.1 联合分布分解

Trajeglish 建模的核心是 $N$ 个智能体在 $T$ 个未来时间步上的联合状态分布 $p(\boldsymbol{s}_1^1, ..., \boldsymbol{s}_T^N \mid c)$，其中 $c$ 为场景上下文（地图、初始状态等）。该联合分布被分解为时间自回归与步内条件的形式：

$$\begin{aligned}
p(s_1^1, ..., s_T^N \mid c) = &\prod_{t=1}^{T} \prod_{n=1}^{N} p\big(s_t^n \mid s_1^1, ..., s_{t-1}^N, \; s_t^1, ..., s_t^{n-1}, \; c\big)
\end{aligned}$$

这一分解的关键性质是：**当前时间步 $t$ 内，智能体 $n$ 的动作不仅依赖于过去所有时间步的动作，还依赖于同一时间步内已采样的其他智能体的动作**（$s_t^1, ..., s_t^{n-1}$）。这为多智能体交互建模提供了结构化的条件依赖。

#### 2.2 编码器-解码器设计

模型采用 GPT 风格的编码器-解码器 Transformer（Fig. 7）：

- **编码器**：接收两类输入——(1) 通过 **VectorNet 地图编码器**（Gao et al., 2020）将地图多段线编码为固定长度嵌入序列；(2) 智能体的初始状态嵌入。编码器输出场景上下文表示。需注意，编码器**不对全局坐标系具有等变性**，也**不对智能体顺序具有置换等变性**，这要求模型从数据中学习空间关系。

- **解码器**：在自回归生成过程中，解码器接收已生成的动作标记序列，并通过**因果掩码**控制注意力范围。具体而言，解码器在预测智能体 $n$ 在时间步 $t$ 的动作时，可以关注：(1) 所有过去时间步的所有智能体动作；(2) 当前时间步 $t$ 内智能体 $1$ 到 $n-1$ 的已选动作。但**不能**关注当前时间步内尚未生成的智能体动作，以此保证推理时的因果性。

#### 2.3 训练策略

训练时采用**噪声分词增强**（Sec A.2）：输入给解码器的动作标记并非精确分词结果，而是从 softmax 核分布中采样的噪声标记，而预测目标仍为最小距离标记。这一策略增强了模型对推理时累积误差的鲁棒性。此外，可选的**航向平滑器**（Heading Smoother, Sec A.5）作为后处理模块，从分词轨迹中恢复更精确的原始航向角。



## 实验与关键发现

### 主结果：Waymo Sim Agents 基准

Trajeglish 在 Waymo Open Motion Dataset (WOMD) Sim Agents 测试基准上取得最优结果，其真实感元指标（Realism meta metric）达到 0.5339，较先前最佳方法提升 3.3%。交互指标（Interactive metrics）达到 0.5811，提升幅度达 9.9%（Table 1）。该方法是该基准上首个采用离散序列建模的模型，超越了包括 **Wayformer**（Nayakanti et al., 2022）、**MTR+++**（Shi et al., 2023）和 **Joint-Multipath++**（Varadarajan et al., 2021）在内的多个成熟运动预测模型。


![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2312_04535/figures/008_Table_1.jpg]]
*Table 1: WOMD Sim Agents Test*

### 分词策略消融

k-disks 分词模板在词汇量 |V|=384 时达到 1.18 厘米的期望离散化误差，显著优于 k-means 的 6.13 厘米和网格基线（Table 2; Fig. 6）。k-disks 通过迭代最小角距离优化模板集，使离散化误差接近厘米级保真度，且训练集与验证集上的标记频率分布高度一致（Fig. 5），表明模板未过拟合训练数据。


![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2312_04535/figures/005_Figure_5.jpg]]
*Figure 5: Token frequency We plot the frequency that each token appears in the validation and training sets. Note that we sort the tokens by their frequency for each class individually for the ID. Increasing the vocabulary size increases the resolution but also results in a longer tail. The distribution of actions on the training set and validation set match closely*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2312_04535/figures/006_Figure_6.jpg]]
*Figure 6: K-means vs. k-disks We plot the average discretization error for multiple template sets sampled from k-means and k-disks with $\vert$ V $\vert = \bar { 3 }$ 8 4 . Alg. 1 consistently samples better template sets than k-means

### 时间步内交互建模消融

为验证时间步内条件建模的必要性，论文设计了“no intra”基线：保持相同架构，但调整解码器掩码，使其不关注当前时间步内已采样的其他智能体动作。

- **全自主设定下的碰撞率**：当仅初始化一个时间步时，Trajeglish 的碰撞率显著低于“no intra”基线，且该优势在车辆类别上尤为突出（Fig. 9）。随着初始化历史步数增加（≥4步），两者差距缩小，说明时间步内交互在缺乏历史信息时最为关键。
- **负对数似然分析**：在预测某智能体下一动作时，模型通过条件化同时间步内已选动作获得预测能力增益，且该增益随智能体顺序后移而累积（Fig. 10）。


![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2312_04535/figures/010_Figure_9.jpg]]
*Figure 9: Full Autonomy Collision Rate Vehicle collision rate is shown on top and pedestrian collision rate is shown on bottom. From left to right, we seed the scene with an increasing number of initial actions from the recorded data. Trajeglish models the log data statistics significantly better than baselines when seeded with only an initial timestep, as well as with longer initialization*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2312_04535/figures/011_Figure_10.jpg]]
*Figure 10: Intra-Timestep Conditioning We plot the negative log-likelihood (NLL) when we vary how many agents choose an action before a given agent within a given timestep. As expected, when the context length increases, intra-timestep interaction becomes much less important to take into account*

### 部分控制与全自主评估

在部分控制场景下，Trajeglish 的 minADE 指标随初始化历史步数增加而改善。当仅提供单步初始化时，考虑时间步内交互的模型与“no intra”基线之间存在显著性能差距；随初始化步数增至 4 步以上，两者趋于收敛（Fig. 8; Fig. 18）。这表明时间步内交互建模的核心价值在于稀疏历史条件下的闭环仿真。


![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2312_04535/figures/009_Figure_8.jpg]]
*Figure 8: Partial control ADE Left shows the ADE for the vehicles selected for evaluation under partial control, but for rollouts where the agents are fully autonomous. Right shows the ADE for the same vehicles but with all other agents on replay. When agents controlled by Trajeglish go first in the permutation order, they behave similarly to the no intra model. When they go last, they utilize the intra-timestep information to produce interaction more similar to recorded logs, achieving a lower ADE*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2312_04535/figures/020_Figure_18.jpg]]
*Figure 18: Full Autonomy minADE As we seed the scene with a longer initialization, the no-intra model and our model converge to similar values, and all models improve. When initialized with only a single timestep, the performance gap between models that take into account intra-timestep interaction and models that do not is significant*

### 分词误差与碰撞率

语义分词性能分析显示，k-disks 分词后的碰撞率与原始数据分布高度一致（Fig. 16），验证了离散化过程未引入额外的碰撞偏差，为闭环仿真中的碰撞评估提供了可靠基础。


![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2312_04535/figures/016_Figure_16.jpg]]
*Figure 16: Semantic Tokenization Performance We plot the probability that the bounding box of an agent has non-zero overlap with another agent in the scene for each timestep. The collision rate for the raw data is shown in black*

### 训练效率与数据规模

Trajeglish 的训练数据规模（以 token 数计）与自然语言数据集可比（Table 5），训练效率分析表明模型在约 1B token 后性能仍持续提升（Table 6; Fig. 11），暗示进一步扩展数据规模可能带来额外增益。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2312_04535/figures/012_Figure.jpg]]

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2312_04535/figures/014_Figure_14.jpg]]
*Figure 14: K-disk expected discretization error Average corner distance for each of the k-disk vocabularies of sizes 128, 256, 384, and 512*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2312_04535/figures/021_Figure_19.jpg]]
*Figure 19: Partial control collision rate We plot the collision rate as a function of rollout time when the traffic model controls only one agent while the rest are on replay. We expect this collision rate to be higher than the log collision rate since the replay agents do not react to the dynamic agents. We note that the collision rate decreases significantly just by placing the agent last in the order, showing that the model learns to condition on the actions of other agents within a single timestep effectively. Figure 20: Context Length We plot the negative log-likelihood (NLL) when we vary the context length at test-time relative to the NLL at full context. Matching with intuition, while pedestria...*




## 定位与知识库关联

### 方法定位与核心差异

Trajeglish 在交通建模方法谱系中占据一个独特位置：它是首个在 Waymo Sim Agents 基准上将多智能体轨迹生成建模为**离散序列的下一个标记预测**任务的工作。与现有方法相比，Trajeglish 在两个关键维度上做出了根本性改变：

1. **轨迹表示**：现有方法普遍采用连续回归（如 **Wayformer** (Nayakanti et al., 2022)、**MTR+++** (Shi et al., 2023)、**Joint-Multipath++** (Varadarajan et al., 2021)）或固定网格分词。Trajeglish 提出 k-disks 迭代最小角距离离散分词，将厘米级精度的连续轨迹映射到仅 384 个词汇量的离散标记空间，期望离散化误差仅 1.18 厘米，远优于 k-means（6.13 厘米）和网格基线（Table 2; Fig. 6）。

2. **交互建模**：现有方法多采用独立边缘轨迹预测，缺乏时间步内的条件依赖。Trajeglish 在 GPT 式编码器-解码器 Transformer 中引入因果掩码策略，允许智能体在同一步内利用其他智能体已选动作进行条件预测（Sec 3.2; Eq. 2），从而保留了动态因子分解的全似然结构，支持测试时的动态交互。

### 与基线方法的关系

在 Waymo Sim Agents 测试基准上，Trajeglish 在真实感元指标上达到 0.5339，超越先前最佳方法 3.3%；交互指标达到 0.5811，提升 9.9%（Table 1）。对比的基线包括：

- **Wayformer (Identical/Diverse)** (Nayakanti et al., 2022)：基于连续回归的联合预测模型
- **MTR+++ / MTRE\*** (Shi et al., 2023)：基于连续回归的运动预测模型
- **Joint-Multipath++** (Varadarajan et al., 2021)：联合多路径预测模型
- **MVTA / MVTE\***：基于连续回归的预测模型
- **Constant Velocity**：简单运动学基线

Trajeglish 的离散序列建模范式与上述连续回归方法形成根本性对立，其性能优势主要来源于：(1) k-disks 分词的高保真离散化；(2) 时间步内因果条件建模带来的交互一致性。

### 适用边界与局限

1. **历史上下文依赖性**：分析表明，当提供超过 4 个时间步的历史信息时，时间步内依赖的重要性显著降低（Sec 4.3）。这意味着在传统运动预测基准的设置下，Trajeglish 的核心优势（步内交互建模）可能被削弱。

2. **全自主设定下的碰撞率**：在仅初始化一个时间步的全自主设定下，Trajeglish 的碰撞率显著低于忽略时间步内交互的基线（Fig. 9），验证了步内条件建模的必要性。但碰撞率仍随 rollout 时长增加而上升，表明长时域一致性仍是挑战。

3. **架构非等变性**：编码器对全局坐标系的选择不具有等变性，对智能体顺序也不具有排列等变性（Sec 3.2），这可能影响模型在场景旋转或智能体重排时的泛化能力。

4. **训练数据规模依赖**：Fig. 11 提示模型性能可能随训练数据量增加而持续提升，但具体缩放规律尚不明确。

### 开放问题

- 模型性能如何随数据集规模（超过 10 亿标记）继续缩放？
- 训练策略中的超参数（如噪声分词强度、温度参数）如何系统性地影响采样质量？
- 离散分词策略能否推广到更复杂的动作空间（如包含加速度、转向角速度的更高维状态）？
- 因果掩码中的智能体排序策略对交互建模质量的影响是否可进一步优化？

### 知识库定位

Trajeglish 将 GPT 风格的序列建模范式成功迁移到多智能体交通仿真领域，其核心贡献在于证明了**小词汇量离散分词 + 时间步内因果条件建模**的组合可以有效解决高维连续轨迹的交互生成问题。该方法桥接了自然语言处理中的下一个标记预测范式与自动驾驶中的多智能体轨迹生成，为后续研究开辟了将大规模语言模型架构直接应用于物理世界交互建模的技术路径。



## 原文 PDF

![[paperPDFs/ICLR_2024/Trajeglish_Traffic_Modeling_as_Next_Token_Prediction.pdf]]
