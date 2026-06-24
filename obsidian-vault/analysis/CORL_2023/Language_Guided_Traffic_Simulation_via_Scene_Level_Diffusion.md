---
title: "Language-Guided Traffic Simulation via Scene-Level Diffusion"
type: paper
paper_level: A
venue: CoRL
year: 2023
pdf_ref: paperPDFs/CORL_2023/Language_Guided_Traffic_Simulation_via_Scene_Level_Diffusion.pdf
project_link: https://github.com/NVlabs/CTG
aliases:
- LGTSSLD
tags:
- CORL_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将单智能体独立扩散模型升级为场景级联合建模，并引入大规模语言模型将自然语言查询转化为可微损失函数，从而在测试时通过迭代优化实现语言引导的可控生成。"
primary_logic: "利用预训练大语言模型的代码生成能力，将用户意图转换为可直接指导扩散模型采样过程的损失函数，避免了训练多模态模型的需要；同时通过空间-时间变压器联合建模所有智能体，实现真实交互。"
claims:
- "在8项不同规则设置中，CTG++在7项上实现了最低的失败率和场景级真实感偏差。"
- "与最强基线CTG相比，CTG++在所有8项设置中显著降低了失败率和场景级真实感偏差，且规则满足度相当或更优。"
- "移除相对几何边信息导致失败率上升（0.173→0.227），而使用场景中心坐标则导致失败率飙升至0.886，验证了智能体中心建模和交互编码的关键作用。"
- "nuScenes validation (GPT keep distance) 上 fail (失败率) = 0.173"
---

# Language-Guided Traffic Simulation via Scene-Level Diffusion

> [!tip] 核心洞察
> 利用预训练大语言模型的代码生成能力，将用户意图转换为可直接指导扩散模型采样过程的损失函数，避免了训练多模态模型的需要；同时通过空间-时间变压器联合建模所有智能体，实现真实交互。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 语言引导的场景级扩散交通仿真 |
| 英文题名 | Language-Guided Traffic Simulation via Scene-Level Diffusion |
| 会议/期刊 | CoRL 2023 |
| Links | [paper](https://arxiv.org/abs/2306.06344); [GitHub](https://github.com/NVlabs/CTG) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CTG++ |
| Dataset | nuScenes validation (GPT keep distance), nuScenes validation (8 settings across runs) |

> [!tip] 效果简介
> - nuScenes validation (GPT keep distance) 上，fail (失败率) 为 0.173，对比 0.343 (CTG)，变化 -49.6%。
> - nuScenes validation (GPT keep distance) 上，rel real (场景级真实感偏差) 为 0.331，对比 0.342 (CTG)，变化 -0.011。
> - nuScenes validation (GPT keep distance) 上，rule (规则违反) 为 0.000，对比 0.000 (CTG)，变化 0。

## 概述

### 问题背景与瓶颈

交通仿真是自动驾驶系统闭环验证的关键工具，然而现有方法面临一个核心矛盾：**规则驱动仿真**依赖领域专家手工设计规则，缺乏真实感；**数据驱动仿真**虽能捕捉真实交互，但可控性不足，难以针对特定场景进行定向生成。当前最强基线 **CTG** 虽然首次将条件扩散模型引入交通生成，但其单智能体独立建模的方式无法捕获场景中多车之间的复杂交互，导致生成轨迹在闭环仿真中频繁出现碰撞、偏离道路等灾难性失效。此外，现有方法的控制接口——无论是手工编写的信号时序逻辑（STL）规则还是采样排序函数——都需要深厚的领域知识，普通用户难以灵活使用。

### 核心方法：CTG++

本文提出 **CTG++**，一个语言引导的场景级扩散交通仿真框架，其核心创新在于两个关键设计：

1. **场景级联合建模**：将单智能体独立扩散升级为场景级联合扩散，通过**空间-时间变压器（Spatio-Temporal Transformer）** 同时编码所有智能体的历史轨迹、相对几何关系（位置、朝向、速度差、距离）以及与向量化地图的交互，从而在生成过程中显式建模多车交互，大幅提升闭环仿真的稳定性和真实感。

2. **语言引导的可控生成**：利用预训练大语言模型 **GPT-4** 的代码生成能力，将用户的自然语言查询（如“车辆A应与车辆B保持10-30米距离”）自动转化为可微损失函数，在测试时通过**投影梯度下降**引导扩散模型的去噪采样过程，实现零样本、无需重新训练的可控生成。这一设计避免了训练多模态模型的高昂成本，同时为用户提供了无需领域专业知识的自然语言接口。

### 方法定位

在方法谱系中，CTG++ 处于**条件扩散生成模型**与**大语言模型辅助推理**的交叉点。与基于模仿学习的 **BITS** 及其优化变体 **BITS+opt** 相比，CTG++ 通过扩散模型的多步去噪机制保留了更强的多模态分布建模能力；与单智能体扩散基线 **CTG** 相比，CTG++ 的场景级架构和语言接口分别解决了交互建模缺失和控制接口僵化两个关键瓶颈。

### 核心结论

在 nuScenes 数据集上的闭环仿真实验表明，CTG++ 在 8 项不同规则设置中**全面超越**最强基线 CTG：在 GPT 生成的“保持距离”规则下，失败率从 0.343 降至 0.173（**降低 49.6%**），场景级真实感偏差从 0.342 降至 0.331。消融实验进一步揭示了方法有效性的因果机制：移除相对几何边信息导致失败率升至 0.227，而使用场景中心坐标替代智能体中心坐标则使失败率飙升至 0.886，验证了**智能体中心建模**和**交互编码**对闭环仿真鲁棒性的关键作用。定性结果表明，CTG++ 在满足查询约束的同时不会牺牲其他方面的质量（如保持车道、轨迹平滑性），而 CTG 则常因过度优化单一规则而引入碰撞或偏离道路。

## 背景与动机

### 问题背景

交通仿真在自动驾驶系统的开发与验证中扮演着关键角色，它为感知、预测和规划模块提供了安全、可复现且成本可控的测试环境。一个理想的交通仿真系统需要同时满足两个核心需求：**高保真的真实感**（生成的车辆轨迹与真实驾驶行为分布一致）和**灵活的可控性**（能够根据用户意图生成符合特定规则或场景的轨迹）。

### 现有方法缺口

现有方法在这两个维度上存在明显的权衡困境。基于模仿学习的方法（如 **BITS**）能够学习真实驾驶行为，但可控性依赖于手动设计的采样排序函数，难以灵活应对多样化的控制需求。基于条件扩散模型的方法（如 **CTG**）虽然通过可微损失函数引导实现了更灵活的可控生成，但其核心局限在于**单智能体独立建模**——每辆车单独生成轨迹，忽略了车辆之间的交互。这导致在施加规则约束时，轨迹可能满足单个智能体的规则，却牺牲了场景级的真实感（如出现碰撞、越界等不合理行为）。

更根本的瓶颈在于**控制接口的易用性**：现有方法要求用户具备领域专业知识，手工设计复杂的 Signal Temporal Logic (STL) 损失函数，这极大限制了非专家用户的使用。自然语言作为最直观的人机交互方式，在交通仿真中尚未被有效利用。

### 本文动机

针对上述缺口，CTG++ 的核心动机是**同时实现高保真场景级真实感与基于自然语言的灵活可控性**。具体而言，本文试图回答两个关键问题：（1）如何将单智能体扩散模型升级为**场景级联合建模**，使生成的轨迹天然包含多智能体交互？（2）如何利用大规模语言模型（LLM）的代码生成能力，将用户的自然语言查询**自动转化为可微损失函数**，从而绕过对领域专业知识的需求，同时避免训练昂贵的多模态模型？

## 核心创新

CTG++ 针对现有交通生成方法的根本瓶颈——无法同时提供高保真真实感与无需领域专业知识的灵活可控性——提出了两个关键创新点，构成了从“单智能体独立建模 + 人工规则”到“场景级联合建模 + 语言引导”的范式跃迁。

### 创新一：场景级联合扩散建模

**改变了什么**：将轨迹建模粒度从单智能体独立建模升级为场景级联合建模。此前的条件扩散基线（如 CTG）为每个交通参与者独立执行扩散去噪，本质上忽略了智能体之间的交互耦合。CTG++ 则一次性对所有场景内智能体的未来动作轨迹 $`\tau_a`$ 进行联合去噪，从根本上捕获了多智能体交互。

**如何实现**：设计了空间-时间 Transformer 架构，交替执行三种注意力机制：
- **时间注意力**：捕获每个智能体自身的时间动力学；
- **空间注意力（含相对几何编码）**：通过编码智能体间的相对位置、朝向、速度差和距离（公式 $`\mathbf{e}_{t}^{ij}`$），使得每个智能体在去噪过程中显式感知其他智能体的状态，从而建模交互；
- **地图注意力**：融合向量化地图环境（车道信息），使生成轨迹与道路结构一致。

这一架构的关键在于**智能体中心坐标系**与**相对几何边信息**的组合。消融实验（Table 2）给出了决定性证据：移除相对几何边信息导致失败率从 0.173 升至 0.227；而改用场景中心坐标系则导致失败率飙升至 0.886，充分验证了智能体中心建模对闭环仿真鲁棒性的关键作用。

### 创新二：基于大语言模型的语言引导控制

**改变了什么**：将控制接口从领域专家手工设计的 Signal Temporal Logic（STL）损失函数，替换为由 GPT-4 根据自然语言查询自动生成的可微 Python 损失函数。这从根本上消除了对领域专业知识的依赖，使非专家用户能够通过自然语言直接操控仿真。

**如何实现**：在测试时，将用户自然语言查询、预定义的辅助函数 API 以及少量示例一并传递给 GPT-4，GPT-4 生成对应的可微损失函数代码。该损失函数随后通过投影梯度下降在扩散去噪的每一步扰动预测均值（公式 $`p_{\theta}(\tau_a^{k-1} \vert \tau^k, \mathbf{c}) \approx \mathcal{N}(\tau_a^{k-1}; \mu + \Sigma^k \nabla_{\mu} \mathcal{I}(\mu), \Sigma^k)`$），引导采样过程生成符合查询意图的轨迹。

**核心洞察**：利用预训练大语言模型的代码生成能力，将用户意图转化为可直接指导扩散采样的损失函数，避免了训练多模态模型的需要。这一设计使得语言接口与场景级扩散模型解耦，既能灵活扩展新的查询类型（通过添加示例），又无需重新训练生成模型本身。

### 两个创新的协同效应

这两个创新并非孤立存在，而是产生了重要的协同效应。定性对比（Figure 4）显示，对于“车辆 A 始终保持与车辆 B 10-30 米距离”和“车辆 A 应与车辆 B 碰撞”等查询，CTG++ 和 CTG 的语言接口均能生成符合查询的轨迹，但 CTG++ 不会牺牲道路保持和平滑性等其他方面的真实感，而 CTG 则会出现碰撞或偏离道路的副作用。这表明**场景级联合建模提供的交互感知能力，使语言引导的生成在满足用户意图的同时，仍能维持场景级的一致性**——这是单智能体独立建模所无法实现的。

## 整体框架

CTG++ 的整体框架围绕一个核心瓶颈展开：**现有交通生成方法无法同时提供高保真真实感和无需领域专业知识的灵活可控性**。为解决这一问题，CTG++ 将单智能体独立扩散模型升级为场景级联合建模，并引入大规模语言模型将自然语言查询转化为可微损失函数，从而在测试时通过迭代优化实现语言引导的可控生成。

### 核心模块与数据流

框架由两大子系统串联而成，形成“语言意图→可微信号→场景级生成”的端到端管线：

1.  **GPT-4 损失函数生成器**：用户以自然语言描述期望的交通行为（如“车辆A应始终与车辆B保持10-30米距离”），GPT-4 结合预定义的 API 函数库和少量示例，自动生成一段 Python 可微损失函数代码。该损失函数编码了用户意图，无需人工设计信号时序逻辑（STL）规则，也无需训练多模态模型。
2.  **场景级条件扩散模型**：该模型以场景中所有智能体的历史轨迹和向量化高精地图为条件，联合生成所有智能体的未来动作轨迹。其核心是一个**空间-时间 Transformer 骨干网络**，交替执行以下注意力操作：
    - **时间注意力**：捕获每个智能体自身的时间动力学。
    - **空间注意力（含相对几何编码）**：通过编码智能体间的相对位置、朝向、速度差和距离，建模多智能体交互。
    - **地图注意力**：融合智能体与向量化车道环境的交互。
3.  **引导采样器**：在扩散模型的逆向去噪过程中，利用 GPT-4 生成的损失函数梯度扰动每一步的预测均值，使生成的轨迹逐步符合用户查询要求。采样器采用投影梯度下降策略，在满足约束的同时维持轨迹的真实感。

### 输入输出规范

- **输入**：
    - 自然语言查询（如“车辆A应与车辆B碰撞”）
    - 场景历史状态（所有智能体的过去轨迹）
    - 向量化高精地图（车道中心线等信息）
- **输出**：场景中所有智能体的未来动作轨迹序列，通过已知动力学模型可进一步推出完整状态序列（位置、速度、朝向）。

### 关键设计决策

框架的核心洞察在于**利用预训练大语言模型的代码生成能力**，将用户意图转化为可直接指导扩散模型采样过程的损失函数，避免了训练多模态模型的需要；同时通过**空间-时间 Transformer 联合建模所有智能体**，实现真实交互。图1给出了框架的总览示意（Figure 1）。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2306_06344/figures/001_Figure_1.jpg]]
*Figure 1: Overview of CTG++. A user query, predefined APIs, and examples are passed to GPT4, which generates a differentiable loss to guide CTG++ for query-compliant trajectories*

该管线的一个显著优势是**测试时可控性**：扩散模型本身仅需训练一次以学习真实交通分布，之后对于任意新的用户查询，只需调用 GPT-4 生成新的损失函数，即可在采样阶段实现零样本的灵活控制。

## 核心模块与公式推导

### 3.1 问题形式化与轨迹表示

CTG++ 将交通仿真建模为一个条件生成问题。场景中包含 $M$ 个智能体，每个智能体 $i$ 在时刻 $t$ 的状态定义为：

$$s_t^i = (x_t^i, y_t^i, v_t^i, \theta_t^i)$$

其中 $(x_t^i, y_t^i)$ 为二维位置，$v_t^i$ 为速度，$\theta_t^i$ 为朝向角。动作向量定义为加速度和横摆角速度：

$$a_t^i = (\dot{v}_t, \dot{\theta}_t)$$

模型仅预测动作轨迹 $\tau_a$，随后通过已知的运动学模型 $f$ 从初始状态 $s_0$ 递推得到状态轨迹 $\tau_s$。这一设计将物理可行性约束隐式地嵌入生成过程中。

场景级联合轨迹表示为所有智能体动作序列和状态序列的集合：

$$\tau := [\tau_{\mathfrak{r}_a}], \quad \tau_{\mathfrak{a}} := \begin{bmatrix} \tau_a^1 \\ \vdots \\ \tau_a^M \end{bmatrix}, \quad \tau_{\mathfrak{s}} := \begin{bmatrix} \tau_s^1 \\ \vdots \\ \tau_s^M \end{bmatrix}$$

其中 $\tau_a^i := [a_0^i \dots a_{T-1}^i]$，$\tau_s^i := [s_1^i \dots s_T^i]$。与单智能体独立建模的基线 CTG 不同，CTG++ 同时预测场景中所有智能体的轨迹，这是实现真实交互生成的核心前提。

### 3.2 场景级扩散模型

**前向扩散过程** 逐步向干净的联合动作轨迹 $\tau_a^0$ 添加高斯噪声，共 $K$ 步：

$$q(\tau_a^{1:K}|\tau_a^0) := \prod_{k=1}^K q(\tau_a^k|\tau_a^{k-1}) := \prod_{k=1}^K \mathcal{N}(\tau_a^k; \sqrt{1-\beta_k}\tau_a^{k-1}, \beta_k \mathbf{I})$$

其中 $\beta_k$ 为噪声调度参数，控制每步添加的噪声量。

**逆向去噪过程** 学习从纯噪声 $\tau_a^K$ 逐步恢复干净轨迹，条件于上下文信息 $\mathbf{c}$（包括历史轨迹和向量化地图）：

$$p_\theta(\tau_a^{0:K}|\mathbf{c}) := p(\tau_a^K) \prod_{k=1}^K p_\theta(\tau_a^{k-1}|\tau^k, \mathbf{c}) := p(\tau_a^K) \prod_{k=1}^K \mathcal{N}(\tau_a^{k-1}; \mu_\theta(\tau^k, k, \mathbf{c}), \Sigma_\theta(\tau^k, k, \mathbf{c}))$$

训练过程与 CTG 类似，但关键区别在于轨迹以场景级别采样，而非智能体级别——模型同时预测所有智能体的输出，从而捕获智能体间的交互依赖。

### 3.3 空间-时间 Transformer 骨干网络

为实现多智能体联合建模，CTG++ 设计了一个空间-时间 Transformer 架构（Figure 2, Figure A1），交替使用三种注意力机制：

**时间注意力** 首先沿时间维度对每个智能体的编码轨迹 $\mathbf{h}_t^i$ 施加自注意力，捕获各智能体自身的时间动力学。

**空间注意力与相对几何编码** 是交互建模的核心。智能体 $i$ 和 $j$ 在时刻 $t$ 的相对几何信息被编码为边特征 $\mathbf{e}_t^{ij}$：

$$\mathbf{e}_{t}^{ij} = \phi_{\mathrm{r}}\left(\left[\mathbf{R}_{0}^{i^{\intercal}}\left(\Delta x_{0,t}^{ij}, \Delta y_{0,t}^{ij}\right), \cos(\Delta\theta_{0,t}^{ij}), \sin(\Delta\theta_{0,t}^{ij}), v_{t}^{j}\cos(\Delta\theta_{0,t}^{ij}) - v_{0}^{i}, v_{t}^{j}\sin(\Delta\theta_{0,t}^{ij}), d_{t}^{i,j}\right]\right)$$

该编码包含：智能体 $i$ 坐标系下的相对位置偏移、相对朝向角的正余弦值、速度差在 $i$ 坐标系下的投影、以及智能体间的欧氏距离 $d_t^{i,j}$。使用智能体中心坐标系（而非场景中心坐标系）是保证闭环仿真鲁棒性的关键设计——消融实验证实，切换为场景中心坐标将导致失败率从 0.173 飙升至 0.886。

空间注意力的查询、键、值通过融合编码轨迹与相对几何信息构建：

$$\mathbf{q}_{t}^{i} = \mathbf{W}^{Q^{\mathrm{global}}}\mathbf{h}_{t}^{i}, \quad \mathbf{k}_{t}^{ij} = \mathbf{W}^{K^{\mathrm{global}}}\left[\mathbf{h}_{t}^{j}, \mathbf{e}_{t}^{ij}\right], \quad \mathbf{v}_{t}^{ij} = \mathbf{W}^{V^{\mathrm{global}}}\left[\mathbf{h}_{t}^{j}, \mathbf{e}_{t}^{ij}\right]$$

**地图注意力** 随后对每个智能体独立施加，键和值来自智能体中心的向量化地图编码，使模型能够感知车道结构等环境约束。

**门控融合机制** 最终通过可学习的门控单元融合环境聚合特征 $\mathbf{m}_t^i$ 与中心智能体特征 $\mathbf{h}_t^i$：

$$\mathbf{g}_{t}^{i} = \mathrm{sigmoid}\left(\mathbf{W}^{\mathrm{gate}}\left[\mathbf{h}_{t}^{i}, \mathbf{m}_{t}^{i}\right]\right), \quad \hat{\mathbf{h}}_{t}^{i} = \mathbf{g}_{t}^{i} \odot \mathbf{W}^{\mathrm{self}}\mathbf{h}_{t}^{i} + (1 - \mathbf{g}_{t}^{i}) \odot \mathbf{m}_{t}^{i}$$

这种门控设计允许模型灵活地平衡自身动力学与交互/环境信息。

### 3.4 语言引导的可控生成

**GPT-4 损失生成器** 是 CTG++ 实现自然语言接口的核心模块。给定用户查询、预定义的辅助函数 API 以及少量示例，GPT-4 自动生成一个可微的 Python 损失函数，将用户意图编码为数值优化目标。Figure 3 展示了生成碰撞损失函数的提示示例。

**引导采样** 在测试时的每个去噪步骤中，利用损失函数 $\mathcal{I}$ 的梯度扰动预测均值 $\mu$，实现查询符合的生成：

$$p_{\theta}(\tau_a^{k-1} \vert \tau^k, \mathbf{c}) \approx \mathcal{N}(\tau_a^{k-1}; \mu + \Sigma^k \nabla_{\mu} \mathcal{I}(\mu), \Sigma^k)$$

该过程通过投影梯度下降实现，在保持生成轨迹真实感的同时，逐步引导其满足用户指定的规则。与 CTG 需要领域专家手工设计信号时序逻辑损失函数不同，CTG++ 的控制接口完全由 LLM 自动构建，大幅降低了使用门槛。

## 实验与分析

### 评估设置与指标

实验在 nuScenes 数据集上进行：所有模型在训练集上训练，在验证集随机选取的 100 个场景上评估。仿真仅考虑移动车辆，闭环仿真时长为 10 秒，重规划频率为 2 Hz。评估采用四个核心指标：

- **fail（失败率）**：遭遇碰撞或驶离道路的智能体百分比，衡量闭环稳定性。
- **rule（规则违反）**：违反指定规则（如距离、速度、碰撞等）的智能体百分比，衡量可控性。
- **real（智能体级真实感）**：纵向加速度幅值、横向加速度幅值和加加速度的分布与真实数据的 Wasserstein 距离均值，衡量单智能体行为真实感。
- **rel real（场景级真实感偏差）**：相对于无条件生成场景的真实感偏差，衡量引入控制后场景整体真实感的保持程度。

对比基线包括：**CTG**（基于条件扩散的最强基线，单智能体独立建模，使用人工设计的 STL 损失函数进行引导）、**BITS**（基于双层模仿学习的基线，通过采样排序函数实现可控性）、**BITS+opt**（BITS 的变体，在输出动作轨迹上施加与 CTG++ 相同的损失函数优化）。公平性保障方面，BITS+opt 与 CTG++ 在引导时使用完全相同的损失函数。

### 主实验结果

**Table 1** 展示了 CTG++ 与各基线在 GPT 生成规则和 STL 规则下的定量对比。核心发现如下：

在 8 项不同规则设置中，CTG++ 在 7 项上实现了最低的失败率和场景级真实感偏差。以 GPT 生成的“保持距离”规则为例，CTG++ 的失败率为 0.173，而最强基线 CTG 为 0.343，降幅达 49.6%；场景级真实感偏差从 0.342 降至 0.331。值得注意的是，CTG++ 在实现更低失败率的同时，规则满足度（rule=0.000）与 CTG 持平。

在 STL 规则下的对比同样显著。以“速度限制”规则为例（Figure A2），CTG++ 不仅实现了更低的规则违反，还避免了 CTG 中出现的车辆间碰撞。在“目标速度”规则下（Figure A3），虽然 CTG 在速度满足度上略优，但其导致车辆与横穿车辆碰撞并驶离道路，而 CTG++ 保持了闭环稳定性。在“无碰撞”规则下（Figure A4），CTG++ 与 BITS+opt 均完美满足规则，但 BITS+opt 生成了高度曲折、不真实的轨迹作为满足规则的代价，而 CTG++ 保持了轨迹的平滑性和真实感。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2306_06344/figures/009_Figure.jpg]]
*Figure: (a) CTG++ speed limit (0.037) (b) CTG speed limit (0.041)*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2306_06344/figures/010_Figure.jpg]]
*Figure: A2: Qualitative comparison between CTG++ and CTG under speed limit STL rule (the numbers in parentheses represent rule violations). CTG++ achieves lower rule violation than CTG. Besides, CTG involves collision between the blue vehicle and the green vehicle. (a) CTG++ target speed (0.213) (b) CTG target speed (0.163) Figure A3: Qualitative comparison between CTG++ and CTG under target speed STL rule (the numbers in parentheses represent rule violations). Although CTG achieves a bit better target speed rule satisfaction, it involves a vehicle collides with crossing vehicles and then goes off-road*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2306_06344/figures/011_Figure.jpg]]
*Figure: (a) CTG++ no collision (0) (b) BITS+opt no collision (0)*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2306_06344/figures/013_Figure.jpg]]
*Figure: (a) CTG++ stop sign + no off-road (0, 0) (b) CTG stop sign + no off-road (0.732, 0)*

**Table 3** 进一步提供了三次运行下的均值与标准差对比。CTG++ 在所有 8 项设置中均显著优于 CTG——失败率和场景级真实感偏差的差值均大于两者标准偏差之和，验证了结果的统计显著性和可复现性。

### 消融实验

**Table 2** 的消融实验揭示了 CTG++ 两个关键设计选择的因果作用：

- **移除相对几何边信息（CTG++ no edge）**：将式 (3) 中的边特征 $\mathbf{e}_{t}^{ij}$ 替换为零向量，失败率从 0.173 升至 0.227。这验证了智能体间相对位置、朝向、速度差和距离的显式编码对交互建模和闭环稳定性的关键作用。Figure 5 的注意力可视化进一步佐证：无边信息时，蓝色车辆未能有效关注交互车辆，导致碰撞。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2306_06344/figures/007_Figure_5.jpg]]
*Figure 5: Darker red means higher attention by the blue vehicle. Without edge information, CTG++ no edge results in a collision (in ☆)*

- **使用场景中心坐标（CTG++ scene）**：以场景中心坐标系替代智能体中心坐标系，失败率急剧飙升至 0.886，严重损害性能。这证实了智能体中心坐标系对于闭环仿真的鲁棒性——在智能体自身参考系中建模运动，避免了场景级坐标下因远距离数值不稳定导致的生成质量崩溃。

### 语言接口的定性分析

Figure 4 展示了语言引导的轨迹生成定性对比。对于“车辆 A 应始终与车辆 B 保持 10-30 米距离”和“车辆 A 应与车辆 B 碰撞”的查询，CTG++ 和 CTG 的语言接口均能生成符合查询的轨迹。然而，CTG 在满足查询的同时牺牲了其他方面（如保持行驶在道路上和平滑性），而 CTG++ 的场景级联合建模有效避免了这种“满足规则但破坏真实感”的权衡。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2306_06344/figures/004_Figure_4.jpg]]
*Figure 4: Generated trajectories for query “vehicle A should always keep within 10-30m from vehicle B” and “vehicle A should collide with vehicle B”, respectively. The collision and offroad locations are marked in ☆ and △. For both CTG++ and CTG, our language interface generate query compliant trajectories. However, CTG++ does not sacrifice other aspects like keeping on-road and smoothness while CTG does*

### 失败模式与局限性

尽管 CTG++ 在多数设置下表现优异，仍存在以下局限：

1. **复杂地图交互查询的失败**：语言接口目前无法处理需要车辆-地图精细交互的命令（如“车辆 A 和 B 依次移动到最右车道然后在下一个路口右转”），因为结构化地图信息未显式传递给 LLM，使其无法推理复杂的几何约束。

2. **LLM 概念理解偏差**：GPT-4 偶尔会错误理解某些驾驶概念（例如“cut in”），导致生成的损失函数逻辑与用户意图存在偏差。这类错误目前需要人工检查才能发现。

3. **推理速度瓶颈**：单次场景级扩散采样耗时约 1 分钟，限制了实时或大规模交互式仿真的应用。加速方向包括蒸馏、缩减扩散步数或引入一致性模型。

4. **新查询类型的人工成本**：框架目前通过少量示例扩展功能，但需要为每种新类型的复杂查询人工设计额外的辅助函数和样例，尚未实现完全自动化的零样本泛化。

### 补充图表

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2306_06344/figures/005_Table_1.jpg]]
*Table 1: Quantitative results of CTG++ and the baselines under GPT-generated rules and STL rules*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2306_06344/figures/012_Figure.jpg]]
*Figure: A4: Qualitative comparison between CTG++ and BITS+opt under no collision STL rule (the numbers in parentheses represent rule violations). Both methods satisfies the rule perfectly as no collision happens. However, BITS+opt have highly curvy, unrealistic trajectories as the cost of satisfying the rule. (a) CTG++ no off-road (0) (b) CTG no off-road (0) Figure A5: Qualitative comparison between CTG++ and CTG under no off-road STL rule (the numbers in parentheses represent rule violations). Both methods satisfies the rule perfectly as no off-road happens. However, CTG lead to multiple collisions among the pink vehicle and vehicles that are stationary*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2306_06344/figures/006_Table_2.jpg]]
*Table 2: Ablation study of CTG++ features*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2306_06344/figures/015_Table_3.jpg]]
*Table 3: Quantitative results (mean with standard deviation of three runs) of CTG++ and the strongest baselines CTG under GPT-generated rules and STL rules. We highlight the winning method that is significantly better than the other (i.e., if the values of the two methods differ by at least the sum of their standard deviations)*

## 方法谱系与知识库定位

### 问题瓶颈与核心因果杠杆

现有交通场景生成方法面临一个根本性两难：基于规则的仿真器（如 CARLA、SUMO）能提供精确控制但缺乏真实感；数据驱动的行为克隆或生成模型（如 TrafficSim、BITS）能产生高保真轨迹，但可控性严重依赖领域专家手工设计的信号时序逻辑（STL）规则，且无法通过自然语言进行直观交互。**CTG++** 的核心因果杠杆在于将这一“真实感-可控性”权衡解耦为两个正交模块——场景级联合扩散建模负责真实交互，大语言模型代码生成负责灵活控制——从而在不牺牲真实感的前提下，首次实现了基于自然语言的零样本可控交通生成。

### 方法演进脉络与基线对比

**CTG++** 的直接前身是 **CTG**（Conditional Traffic Generation），后者首次将条件扩散模型引入交通仿真，通过分类器引导实现 STL 规则下的可控生成。然而 CTG 存在三个结构性缺陷：(1) 对场景中每个智能体独立建模，忽略了多智能体交互导致的级联效应；(2) 引导损失函数需由领域专家针对每种新规则手工编写，扩展成本高昂；(3) 缺乏面向非专家用户的自然语言接口。

与 CTG 的独立建模不同，**BITS** 采用双层模仿学习框架，通过采样排序函数实现可控性。其变体 **BITS+opt** 在输出动作轨迹上施加与 CTG++ 相同的损失函数进行优化。然而，BITS 系列方法本质上仍是对单智能体策略的独立优化，缺乏对场景级交互的显式建模。

**CTG++** 在三个维度上实现了代际跨越：

| 维度 | CTG | CTG++ | 改进机制 |
|------|-----|-------|----------|
| 轨迹建模粒度 | 单智能体独立建模 | 场景级联合建模所有智能体 | 空间-时间Transformer捕获交互 |
| 控制接口 | 领域专家手工编写STL损失 | GPT-4根据自然语言自动生成可微损失 | 少量示例提示下的代码生成 |
| 架构设计 | U-Net或单智能体Transformer | 空间-时间Transformer交替注意力 | 相对几何编码+门控融合 |

### 关键消融发现与机制验证

消融实验（Table 2）揭示了两项决定性机制：

1. **相对几何边信息的关键作用**：当将空间注意力中的相对几何编码 $\mathbf{e}_{t}^{ij}$ 替换为零向量时，失败率从 0.173 上升至 0.227。这表明模型不仅需要知道其他智能体的存在，更需要精确的相对位置、朝向、速度差和距离信息来维持闭环仿真中的稳定性。Figure 5 的注意力可视化进一步证实，缺少边信息时蓝色车辆无法有效关注潜在冲突车辆，导致碰撞。

2. **智能体中心坐标系的鲁棒性优势**：使用场景中心坐标替代智能体中心坐标导致失败率飙升至 0.886，几乎完全丧失仿真能力。这一现象的根本原因在于：扩散模型在场景中心坐标系下需要对绝对位置进行精确预测，而智能体中心坐标系将问题转化为相对运动预测，大幅降低了学习难度和误差传播风险。

### 适用边界与已知局限

**适用场景**：CTG++ 在以下条件下表现最优：(1) 移动车辆间的交互场景（当前不支持行人、自行车等其他交通参与者）；(2) 中等规模场景（nuScenes 验证集随机选取的 100 个场景，10 秒仿真时长）；(3) 规则类型为相对距离保持、碰撞/避免、速度限制、目标路径点等可转化为可微损失函数的查询。

**已知局限**：

1. **复杂地图推理能力缺失**：语言接口目前无法处理需要理解地图拓扑结构的命令（如“车辆A和B依次移动到最右车道然后在下一个路口右转”），因为车道、路口、停止线等结构化地图信息未显式传递给 LLM。这是当前框架最根本的能力边界。

2. **LLM 理解偏差**：GPT-4 偶尔会错误理解某些驾驶概念（例如“cut in”），导致生成的损失函数逻辑有偏差。目前缺乏自动检测和修正这些语义错误的机制。

3. **推理效率瓶颈**：单次场景级扩散采样耗时约 1 分钟（100 步去噪），限制了实时或大规模交互式仿真的应用。这是场景级联合建模带来的固有计算代价。

4. **扩展成本**：虽然语言接口避免了手工编写损失函数，但为每种新型复杂查询仍需人工设计额外的辅助函数和少量示例，无法实现完全的零样本泛化。

### 开放问题与未来方向

1. **结构化地图信息的 LLM 注入**：如何将向量化地图（车道拓扑、路口结构、停止线位置）高效地编码为 LLM 可理解的提示格式，使其能推理复杂的几何约束和交通规则？

2. **损失函数的自动验证与修正**：能否引入一个验证-修正循环，自动检测 GPT-4 生成损失函数中的逻辑错误（如未考虑水平移动、忽略边界条件），并利用错误信号进行迭代修正？

3. **扩散模型加速**：能否通过蒸馏、缩减扩散步数、引入一致性模型或使用更高效的采样策略（如 DPM-Solver）将场景级采样时间从分钟级降至秒级？

4. **多模态输入扩展**：如何将框架推广到多模态输入（如事故报告文本+现场图像），以生成更逼真的碰撞重建场景？这需要解决视觉特征与语言指令的融合问题。

5. **更大规模场景验证**：当前实验限于 nuScenes 的 100 个验证场景，在更大规模、更高密度、更多样化的交通场景（如 Waymo Open Dataset、交互路口）上的泛化能力有待验证。

## 原文 PDF

![[paperPDFs/CORL_2023/Language_Guided_Traffic_Simulation_via_Scene_Level_Diffusion.pdf]]
