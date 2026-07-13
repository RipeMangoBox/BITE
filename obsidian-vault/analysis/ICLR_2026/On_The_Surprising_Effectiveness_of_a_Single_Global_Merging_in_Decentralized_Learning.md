---
title: "On The Surprising Effectiveness of a Single Global Merging in Decentralized Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/On_The_Surprising_Effectiveness_of_a_Single_Global_Merging_in_Decentralized_Learning.pdf
project_link: https://paper-list.notion.site/ICLR-26-Oral-The-Grokking-Moment-in-Decentralized-Learning-On-The-Surprising-Effectiveness-of-A--2f43218102c0805d99d6e56d2934fac4
code_link: https://github.com/Raiden-Zhu/ICLR-2026-Grokking-in-Decentralized-Learning
openreview_forum_id: zrFnwRHuQo
aliases:
- DSSGFGM
- SESGMDL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通信调度的时间分配（将通信预算集中于训练后期）和最终执行一次全连接的全局模型合并。"
primary_logic: "极少量但非零的通信足以在整个训练过程中维持本地模型的跨初始化、跨分布的可合并性（mergeability）。结合损失景观的渐进锐化效应，全局合并后的模型能够实现与并行SGD相当的收敛速率，从而解释了单次全局合并为何能显著提升泛化性能。"
claims:
- "单次全局合并可显著提升严重通信限制和数据异构下的全局测试性能。"
- "有限但非零的通信在训练过程中维持了本地模型的全局可合并性，而完全无通信时模型不可合并。"
- "将通信预算集中在训练后期可一致地提升最终测试精度。"
- "全局合并后的去中心化SGD的收敛率可以匹配并行SGD，理论分析将模型差异部分重新解释为建设性组件。"
---

# On The Surprising Effectiveness of a Single Global Merging in Decentralized Learning

> [!tip] 核心洞察
> 极少量但非零的通信足以在整个训练过程中维持本地模型的跨初始化、跨分布的可合并性（mergeability）。结合损失景观的渐进锐化效应，全局合并后的模型能够实现与并行SGD相当的收敛速率，从而解释了单次全局合并为何能显著提升泛化性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 关于去中心化学习中单次全局合并令人惊讶的有效性 |
| 英文题名 | On The Surprising Effectiveness of a Single Global Merging in Decentralized Learning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=zrFnwRHuQo) · [GitHub](https://github.com/Raiden-Zhu/ICLR-2026-Grokking-in-Decentralized-Learning) · [Project](https://paper-list.notion.site/ICLR-26-Oral-The-Grokking-Moment-in-Decentralized-Learning-On-The-Surprising-Effectiveness-of-A--2f43218102c0805d99d6e56d2934fac4) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Decentralized SGD with Sparse Gossip and Final Global Merging |
| Dataset | Tiny ImageNet, CIFAR-100 |

> [!tip] 效果简介
> - Tiny ImageNet 上，Global test accuracy 为 Decentralized SGD + final merge (AdamW)，对比 Local training alone，变化 显著提升 (见 Figure 1b)。
> - Tiny ImageNet 上，Global test accuracy 为 Decentralized AdamW + final merge，对比 FedAdamW，变化 性能相当。
> - CIFAR-100 上，Global test accuracy 为 后期通信窗口（窗口 15-18），对比 早期通信窗口（窗口 0-3），变化 后期窗口的最终准确率更高。

## 概要

### 问题背景与核心瓶颈

在大规模分布式机器学习中，去中心化学习（Decentralized Learning）通过点对点（peer-to-peer）通信替代传统的中心服务器架构，能够消除单点瓶颈并增强隐私保护。然而，当数据分布高度异构（如各 agent 持有不同的类别分布）且通信预算严重受限时，本地模型之间缺乏共识，导致全局泛化性能急剧下降。传统分析将这种模型差异视为有害噪声，认为其阻碍收敛，从而忽视了该差异可能被转化利用的潜力。

### 核心发现

本文揭示了一个令人惊讶的现象：**在训练结束时执行一次全连接的全局模型合并（global merging），即可显著提升去中心化学习的全局测试性能，甚至使去中心化 SGD 的收敛率匹配并行 SGD**。这一发现的核心机制包含两个层面：

1. **可合并性的维持**：极少量但非零的通信（例如每轮以 0.2 的概率与一个随机对等体交换参数）足以在整个训练过程中维持本地模型的“可合并性”（mergeability）——即全局平均模型在全局种群风险下不差于各本地模型的加权平均。完全无通信时，模型将不可合并，全局平均性能几乎为零（Figure 2c）。

2. **渐进锐化效应**：损失景观在训练过程中逐渐锐化，使得模型差异中与 Hessian 交互的部分转化为建设性因素。理论分析表明，当梯度与 Hessian 迹的交互项主导时，共识误差项 $U^{(t)}$ 可为负值，从而加速收敛（Proposition 2）。

### 方法定位

本文提出的方法可概括为**带稀疏通信与最终全局合并的去中心化 SGD**（Decentralized SGD with Sparse Gossip and Final Global Merging）。其核心调度策略是：将有限的通信预算集中于训练后期窗口，并在最后一步执行全连接全局平均（AllReduce）。该方法在方法谱系中处于以下位置：

- 与联邦学习（如 **FedAdamW**）相比：无需中心服务器，且最终性能相当（Figure C.1, C.2），但通信模式更灵活、鲁棒性更强。
- 与一次性联邦学习（**One-shot FedAdamW**）相比：后者仅在最后聚合一次，缺乏训练过程中的模型交互，性能显著劣于本文方法。
- 与经典去中心化 SGD（如 **D-PSGD**，Lian et al., 2017）相比：D-PSGD 在 IID 设定下包含最终合并，但未系统研究非 IID 下通信调度与可合并性的关系。
- 与通信高效的去中心化方法（如 **SCSP**，Aketi et al., 2021）相比：SCSP 采用梯度稀疏化和最终合并，但未揭示“后期集中通信”的独特优势。

### 主要结果概览

- **单次全局合并的效果**：在 Tiny ImageNet 上，32 agent 非 IID 设定（Dirichlet α = 0.1）下，去中心化 SGD + 最终合并使 CLIP ViT-B/32 和 ResNet-18 的全局测试准确率大幅提升（Figure 1a, 1b），性能与 FedAdamW 相当。
- **通信调度的影响**：将全连接通信窗口分配至训练后期（如窗口 15–18）一致地优于早期窗口（窗口 0–3），在 CIFAR-100 上最终准确率提升显著（Figure 2a, 2b）。
- **可合并性的关键条件**：非零通信是维持可合并性的必要条件；不同通信拓扑（随机图、环形图、指数图）和减少对等体数量（$R$ 值）均能保持可合并性，但性能随通信量降低而下降（Figure C.3）。
- **理论保证**：首次证明去中心化 SGD 的全局合并模型可达到与并行 SGD 相匹配的非凸收敛率 $\mathcal{O}\big(\frac{\sigma^2}{m\varepsilon^2} + \frac{1}{\varepsilon} + \sum U^{(t)}\big)$（Theorem 1, Table 1），其中 $U^{(t)}$ 项在渐进锐化假设下可为负。

### 局限与开放问题

当前验证主要限于视觉分类任务（CIFAR-100, Tiny ImageNet），在其他领域（如 NLP）及更复杂任务上的有效性尚待检验。理论分析依赖高阶平滑性和全局渐进锐化假设，实践中可能不完全满足。最终全局合并需要全连接通信，虽可通过多轮 gossip 近似（Figure C.6），但仍需额外开销。未来方向包括：设计自适应通信调度算法以自动维持关键共识边缘条件、将渐进锐化机制推广至异步及联邦学习场景、以及在实际地理分布式环境中的部署验证。

### 去中心化学习中的通信瓶颈

在去中心化学习中，多个 agent 各自持有本地数据，通过交替执行本地模型更新和对等通信来协作训练一个全局模型。与联邦学习依赖中心服务器进行全局聚合不同，去中心化学习仅依赖 agent 之间的稀疏对等通信（gossip），这使其在隐私敏感和通信受限的场景下具有天然优势。然而，当数据分布高度异构（non-IID）且通信预算极度有限时，模型之间难以形成共识，导致各本地模型在参数空间内逐渐发散，最终损害全局泛化性能。

传统分析将这种模型差异视为有害噪声——共识误差越大，收敛越慢。这一视角催生了大量致力于在训练全程维持低共识误差的方法，例如频繁的模型平均或梯度稀疏化。但这些方法在通信预算极度受限时往往力不从心：当每轮仅有少量 agent 以低概率交换参数时，共识误差的累积似乎不可避免。

### 现有方法缺口

现有去中心化学习范式存在两个关键盲点：

**盲点一：通信预算的均匀分配。** 大多数方法将有限的通信预算均匀地分布在训练的各个阶段。然而，训练早期的模型参数尚在快速变化，此时通信带来的收益可能远低于后期——当损失景观逐渐锐化、模型接近收敛区域时，微小的参数偏移即可能导致显著的性能损失。

**盲点二：最终全局合并的潜力被低估。** 联邦学习中的一次性聚合（one-shot aggregation）已被证明在数据异构时效果不佳，这导致研究者普遍认为去中心化场景下的单次全局合并同样无效。但这一直觉忽略了一个关键事实：去中心化训练中持续的稀疏通信——即使量极少——可能在训练全程维持了本地模型之间某种隐式的“可合并性”（mergeability），使得最终合并的效果远超预期。

### 核心动机

本文的出发点是对上述盲点的系统性质疑：

1. **通信预算是否应该集中于训练后期？** 如果后期通信对模型质量的边际收益更高，那么将预算从早期重新分配到后期应当能提升最终性能。
2. **单次全局合并是否真的无效？** 如果极低量的持续通信足以维持可合并性，那么在训练结束时执行一次全连接全局平均（AllReduce）可能带来显著的性能跃升。
3. **模型差异是否只能是有害的？** 从损失景观的角度看，适度的模型差异可能通过渐进锐化（progressive sharpening）效应为收敛提供额外动力，而非纯粹拖慢训练。

这些问题的回答不仅关乎对去中心化学习动力学的理解，更直接影响实际部署中的通信调度策略设计。

## 核心方法与创新机理

本工作的核心创新在于对去中心化学习中模型差异（model discrepancy）角色的重新定位，以及由此衍生的极简通信范式。传统方法将异构数据下有限通信产生的模型差异视为阻碍收敛的有害噪声，而本文通过理论分析和实验揭示了**该差异中蕴含的建设性成分**，并据此提出了一种“稀疏通信维持可合并性 + 单次全局合并释放泛化潜能”的框架。

### 创新一：模型差异从“噪声”到“建设性组件”的重新解释

这是本文最根本的认知转变。在标准分析中，去中心化SGD的共识误差 $\Xi_t$ 仅作为需要被压制的误差项出现，其存在会拖慢收敛。本文的理论分析（Theorem 1 和 Proposition 2）首次指出，在损失景观满足**渐进锐化**（progressive sharpening）的条件下，模型差异与Hessian的交互项 $U^{(t)}$ 可以为负：

$$U^{(t)} \triangleq \frac{1}{2}(\eta L_2 - 1)\nabla\mathcal{L}(\bar{\theta}^{(t)})^\top \nabla\mathrm{Tr}(\nabla^2\mathcal{L}(\bar{\theta}^{(t)})\Gamma^{(t)}) + O(\Xi_t^3) < 0$$

其中 $\Gamma^{(t)}$ 是模型间的协方差矩阵。当 $\eta > 1/L_2$ 且损失梯度与锐度梯度负相关（Assumption 4）时，$U^{(t)} < 0$ 成立。这意味着**适度的模型差异非但无害，反而通过隐式偏差（implicit bias）为平均模型提供了沿平滑梯度方向更新的额外加速**，使得去中心化SGD的收敛率可以匹配甚至超越并行SGD（Table 1）。

这一理论洞察直接解释了本文所有实证现象的根本原因：为何极少量通信就能维持可合并性（因为差异本身就是建设性的），以及为何最终一次合并就能释放出与频繁全局聚合相当的泛化性能。

### 创新二：通信调度的“后期集中 + 最终全连接合并”范式

基于上述理论，本文提出了与传统均匀通信截然不同的调度策略：

| 设计维度 | 传统做法 | 本文方案 | 理论依据 |
|---------|---------|---------|---------|
| **通信时间分配** | 训练全程均匀分布 | 集中于训练后期窗口 | 渐进锐化效应在后期更强，此时模型差异的建设性贡献最大 |
| **最终合并方式** | 无最终合并或仅靠稀疏gossip | 单次全连接全局平均（AllReduce） | 将整个训练过程积累的“可合并”模型一次性整合，释放泛化潜能 |
| **训练中通信量** | 每轮固定对等体通信 | 极低概率随机对等体通信（如 $R=0.2$） | 仅需维持“可合并性”的临界共识边缘条件（Equation 11），而非追求精确共识 |

实验验证了这一范式的有效性：在CIFAR-100上训练ResNet-18时，将全连接通信窗口从早期（窗口0-3）移至后期（窗口15-18），最终测试准确率获得一致且显著的提升（Figure 2a, 2b）。同时，即使训练过程中每轮仅以0.2的概率与一个随机对等体通信，最终单次全局合并仍能使模型性能从接近零提升至与FedAdamW相当的水平（Figure 1a, 1b; Figure C.1）。

### 创新三：揭示“可合并性”的临界通信条件

本文通过消融实验系统性地揭示了**完全无通信与极少量通信之间存在质的差异**：当通信概率降为零时，全局平均模型的性能始终接近零（Figure 2c橙色曲线），说明模型已不可合并；但只要存在非零的稀疏通信（如概率0.2），全局平均模型就能持续优于各局部模型（Figure 2c蓝色曲线），且最终合并后的性能大幅跃升。这一发现定义了去中心化学习中“可合并性”的相变边界，并由此导出了临界共识边缘条件（Equation 11），为实际部署中的通信预算分配提供了理论指导。

---

**证据强度说明**：Theorem 1和Proposition 2的理论结果依赖于高阶平滑性假设（Assumption 2）和渐进锐化假设（Assumption 4），后者在一般非凸景观中的普遍性尚需更广泛的实证验证。实验证据主要来自视觉分类任务（CIFAR-100, Tiny ImageNet），在其他领域和更大规模任务上的泛化性有待进一步确认。

本文提出的去中心化训练范式建立在**稀疏对等通信 + 单次全局合并**的极简流水线之上。其核心操作流程由四个顺序模块构成，模块间的输入输出关系直接体现了“以极小通信代价维持可合并性，最终一次性释放全局性能”的设计哲学。

### 流水线模块与数据流

**1. 本地 SGD 更新**

每个 agent $k$ 在其本地数据分布 $\mathcal{D}_k$ 上独立执行标准 SGD 或 AdamW 更新。该模块接收上一轮通信后的本地模型参数，输出更新后的局部模型 $\theta_k^{(t+1)}$。这是整个流水线中唯一涉及梯度计算的模块，计算成本与集中式训练中单个 worker 的本地更新完全一致。

**2. 稀疏对等通信**

在每个通信轮次，每个 agent 以概率 $R$（典型值 $R=0.2$）随机选择一个对等体，双方交换完整的模型参数。此模块的输入是各 agent 当前的局部模型，输出为经过参数平均后的混合模型。通信图在每一轮独立随机生成，其期望混合性质满足收缩条件：

$$\mathbb{E}_W \|\Theta W - \bar{\Theta}\|_F^2 \leq (1-p)\|\Theta - \bar{\Theta}\|_F^2$$

其中 $p$ 刻画了随机图的信息混合效率，随机拓扑可实现 $p = \Theta(1)$，在极低通信开销下仍能维持有效的共识收缩。

**3. 最终全局合并**

训练结束时，所有 agent 执行一次全连接通信（Ring-AllReduce），将所有本地模型参数进行全局平均，得到单一合并模型 $\bar{\theta} = \frac{1}{m}\sum_{k} \theta_k$。这一步是整个流水线的关键转折点：它利用训练全程积累的模型可合并性，以单次通信的代价将分布式训练的成果凝聚为统一的全局模型。

**4. 可合并性评估**

合并后的模型在全局测试分布上进行评估，采用平均全局测试准确率作为统一度量：

$$\overline{\mathrm{Acc}}(\{\theta_k^{(t)}\}_{k\in\mathcal{V}}) = \frac{1}{m}\sum_{k\in\mathcal{V}}\mathrm{Acc}(\theta_k^{(t)}), \quad \mathrm{Acc}(\cdot) \triangleq \frac{1}{m}\sum_{l\in\mathcal{V}}\mathbb{E}_{\xi_l\sim\mathcal{D}_l}\mathrm{Acc}(\cdot;\xi_l)$$

这一评估方式直接验证了可合并性条件——合并模型在全局种群风险下不差于原始局部模型的加权和：

$$\mathcal{L}\left(\sum_{k\in V} w_k\theta_k\right) \leq \sum_{k\in V} w_k\mathcal{L}(\theta_k)$$

### 通信调度的核心策略

流水线的关键创新不在于模块本身，而在于**通信预算的时间分配**。实验表明，将有限的全连接通信集中部署于训练后期窗口（而非均匀散布于整个训练过程），可一致地提升最终测试精度（Figure 2a, 2b）。在非窗口期，仅维持概率性的单对等体稀疏通信（$R=0.2$），其总通信成本为 $\mathcal{O}(m R P T + 2 m P)$，其中 $R \ll 2$，远低于联邦学习中每轮全连接的 $\mathcal{O}(2mPT)$。

### 与基线方法的架构差异

| 维度 | 联邦学习 (FedAdamW) | 一次性联邦学习 | 纯本地训练 | 本文方法 |
|------|---------------------|----------------|-----------|---------|
| 训练期通信 | 每轮全连接 | 无 | 无 | 稀疏随机对等体 |
| 最终合并 | 无需（已全局同步） | 单次全局平均 | 无 | 单次全局平均 |
| 模型差异角色 | 通过频繁同步消除 | 被忽略 | 自由发散 | 部分保留为建设性因素 |

这一流水线在 Tiny ImageNet 上使用 CLIP ViT-B/32 和 ResNet-18 的实验中，以远低于联邦学习的通信代价，取得了与之相当的全局测试精度（Figure C.1, C.2），验证了“稀疏通信维持可合并性 + 单次全局合并释放性能”这一极简范式的有效性。

### 关键模块设计

本文方法的核心由四个模块串联构成，形成“本地更新—稀疏对等通信—最终全局合并—可合并性评估”的闭环。

**本地 SGD 更新**：每个 agent $k$ 在其本地数据分布 $\mathcal{D}_k$ 上执行标准 SGD 或 AdamW 更新，独立优化局部目标。该模块是整个训练流程的基本计算单元，不涉及跨 agent 通信。

**稀疏对等通信**：在每轮训练中，每个 agent 以概率 $R$（典型值 0.2）随机选择一个对等体交换模型参数。这一概率化稀疏通信机制是维持模型可合并性的关键——实验表明，完全去除该通信（$R=0$）会导致全局平均模型性能几乎为零（Figure 2c 浅橙色曲线），而极低但非零的通信即可维持可合并性（Figure 2c 蓝线）。

**最终全局合并（AllReduce）**：训练结束时执行一次全连接通信，将所有本地模型参数进行全局平均。这是本文的核心操作，其通信成本为 $\mathcal{O}(mRP T + 2mP)$，其中 $R \ll 2$ 为每轮期望通信对等体数。若全连接通信不可行，可通过多轮 gossip 同步近似（见 Appendix C.3.4 及 Figure C.6）。

**可合并性评估**：通过两个指标评估合并后模型的泛化能力。Definition 1 定义平均全局测试准确率：

$$\overline{\mathrm{Acc}}(\{\theta_k^{(t)}\}_{k\in\mathcal{V}}) = \frac{1}{m}\sum_{k\in\mathcal{V}}\mathrm{Acc}(\theta_k^{(t)}), \quad \mathrm{Acc}(\cdot) \triangleq \frac{1}{m}\sum_{l\in\mathcal{V}}\mathbb{E}_{\xi_l\sim\mathcal{D}_l}\mathrm{Acc}(\cdot;\xi_l)$$

Definition 2 定义全局种群风险下的可合并性条件：若存在组合权重 $\{w_k\}_{k\in V} \in [0,1]$ 使得

$$\mathcal{L}\left(\sum_{k\in V} w_k\theta_k\right) \leq \sum_{k\in V} w_k\mathcal{L}(\theta_k)$$

则称本地模型集合 $\{\theta_k\}_{k\in V}$ 是全局可合并的。

### 核心公式与理论推导

**问题形式化**：去中心化学习的目标是最小化所有 agent 局部种群风险的平均：

$$\operatorname*{min}_{\theta}\left[\mathcal{L}(\theta) \triangleq \frac{1}{m}\sum_{k\in\mathcal{V}}\mathbb{E}_{\xi_k\sim\mathcal{D}_k}\mathcal{L}(\theta;\xi_k)\right]$$

**混合矩阵收缩假设**（Assumption 1）：令 $W$ 为随机通信图对应的混合矩阵，$\Theta$ 为所有本地模型参数矩阵，$\bar{\Theta}$ 为其均值。期望意义下混合操作以至少 $1-p$ 的因子减小模型差异：

$$\mathbb{E}_W \|\Theta W - \bar{\Theta}\|_F^2 \leq (1-p)\|\Theta - \bar{\Theta}\|_F^2$$

其中 $p$ 刻画通信图的混合效率，随机图可达 $p = \Theta(1)$。

**共识误差递归**（Lemma D.1）：单步去中心化 SGD 后期望共识误差 $\Xi_t$ 满足：

$$\mathbb{E}[\Xi_{t+1}^2] \leq (1 - \frac{p}{2})\Xi_t^2 + \frac{12(1-p)}{p}\eta^2(\phi_t^2 + \sigma^2)$$

该递归表明，共识误差在混合操作下以因子 $1-p/2$ 收缩，同时受梯度噪声 $\sigma^2$ 和异构性 $\phi_t^2$ 注入新误差。

**隐式偏差**（Proposition D.3）：平均模型 $\bar{\theta}^{(t)}$ 的更新可重写为沿平滑梯度方向移动：

$$\mathbb{E}_{\xi^{(t)}}[\bar{\theta}^{(t+1)}] = \bar{\theta}^{(t)} - \eta \cdot \mathbb{E}_{\epsilon^{(t)}\sim \mathcal{N}(0,\Gamma^{(t)})}[\nabla\mathcal{L}(\bar{\theta}^{(t)} + \epsilon^{(t)})] + \delta^{(t)}$$

其中 $\Gamma^{(t)}$ 为模型方差协方差矩阵，$\epsilon^{(t)}$ 为以该方差为尺度的扰动。这表明去中心化 SGD 隐式地在损失景观上执行了方差加权的平滑梯度下降。

**DSGD 收敛率**（Theorem 1）：达到 $\varepsilon$-稳定点所需的总步数为：

$$T = \mathcal{O}\Big(\frac{\sigma^2}{m\varepsilon^2} + \frac{1}{\varepsilon} + \sum_{t=0}^{T-1}U^{(t)}\Big)\cdot(\mathcal{L}(\theta^{(0)})-\mathcal{L}^\star)$$

其中辅助项 $U^{(t)}$ 捕捉模型差异对收敛的影响：

$$U^{(t)} \triangleq \frac{1}{2}(\eta L_2 - 1)\nabla\mathcal{L}(\bar{\theta}^{(t)})^\top \nabla\mathrm{Tr}(\nabla^2\mathcal{L}(\bar{\theta}^{(t)})\Gamma^{(t)}) + O(\Xi_t^3)$$

**渐进锐化假设**（Assumption 4）与 $U^{(t)}$ 的负性（Proposition 2）：若损失梯度与锐度梯度呈负相关：

$$\nabla\mathcal{L}(\theta)^\top \nabla\mathrm{Tr}(\nabla^2\mathcal{L}(\theta)\Sigma) < 0$$

且学习率满足 $\eta > 1/L_2$，则 $U^{(t)} < 0$。这意味着模型差异项可成为建设性因素，使 DSGD 的收敛率匹配甚至超越并行 SGD（Table 1）。该结论将传统分析中视为有害噪声的模型差异，重新解释为通过渐进锐化加速收敛的驱动因素。

**关键共识边缘条件**（Equation 11）：为确保 $U^{(t)}$ 的负性主导收敛，通信图参数 $p$ 需满足：

$$\frac{24(1-p)\eta^2}{p^2}(\phi^2+\sigma^2) < \min\{\frac{(\eta L_2-1)\gamma^*\mu_t}{2(\eta L_2+\frac{L_4}{24})\sqrt{m}L_1}, \sqrt{\frac{(\eta L_2-1)\gamma^*\mu_t}{2\Sigma_{\mathrm{high}}}}\}$$

该条件揭示了 $p$ 应随训练动态（通过 $\mu_t$ 反映损失景观几何变化）自适应调整——训练后期梯度范数减小、锐度效应增强，需更多通信维持共识边缘。这与实验发现“通信预算应集中于训练后期”一致（Figure 2a, 2b）。

> **证据强度说明**：Theorem 1 和 Proposition 2 的推导依赖高阶平滑性（Assumption 2，导数有界至 4 阶）和全局渐进锐化（Assumption 4），这些假设在深度网络实践中可能不完全满足，其经验验证目前仅限于视觉分类任务。$U^{(t)}$ 的负性在真实非凸景观中的行为仍需进一步实证检验。

## 实验与关键发现

### 4.1 通信调度的时间分配效应

本节考察通信预算在训练时间轴上的分配策略对最终性能的影响。实验将完整训练过程划分为连续的等长窗口，仅在特定窗口内激活全连接通信（AllReduce），其余阶段维持低通信的稀疏gossip（每轮以概率0.2随机选择1个对等体交换参数）。

**核心发现**：将全连接通信集中于训练后期窗口，可一致地提升最终全局测试准确率。在CIFAR-100上训练ResNet-18（16个agent，Dirichlet α=0.1），当全连接通信占总轮数1/10时（Figure 2a），后期窗口（窗口15-18）的最终准确率显著高于早期窗口（窗口0-3）；将全连接比例降至1/20时（Figure 2b），后期通信的优势依然保持。这一现象表明，**通信的价值在训练不同阶段是不均匀的**——后期通信对模型合并质量的贡献远大于前期。

### 4.2 单次全局合并的惊人有效性

Figure 1a和1b展示了本文最关键的实证发现：在Tiny ImageNet上，32个agent在高度非IID划分（Dirichlet α=0.1）下进行去中心化SGD训练，每轮仅以0.2概率与一个随机对等体通信，最终执行一次全连接全局合并（Ring-AllReduce）。结果显示：

- **CLIP ViT-B/32**（Figure 1a）：全局合并后模型准确率大幅跃升，接近FedAdamW（频繁中心聚合）的性能水平。
- **ResNet-18**（Figure 1b）：合并后准确率同样显著提升，远超纯本地训练基线。

**与联邦学习的对比**（Figure C.1, C.2）：在16和32个agent的设置下，去中心化AdamW+最终合并的性能与FedAdamW相当，且显著优于One-shot FedAdamW（仅在最后聚合一次）。这表明，**训练过程中的稀疏gossip通信是维持可合并性的关键**，单纯的一次性聚合无法达到同等效果。

Figure 1c可视化了全局合并前的损失景观，显示各本地模型位于同一宽阔盆地内的不同位置，这为线性插值合并的有效性提供了直观解释。

### 4.3 可合并性依赖于非零通信

Figure 2c通过对比实验揭示了可合并性的必要条件：

- **低通信（蓝线）**：每轮以0.2概率随机通信时，全局平均模型（浅蓝曲线）的测试性能始终高于各本地模型（深蓝曲线），表明模型在整个训练过程中保持可合并。
- **无通信（橙线）**：完全本地训练时，全局平均模型（浅橙曲线）的性能几乎为零，说明**零通信导致模型发散至不可合并的盆地**。

这一对比确立了"极少量但非零的通信"作为维持可合并性的临界条件。

### 4.4 通信拓扑与对等体数量的影响

消融实验（Figure C.3）评估了通信图结构的影响：

- **对等体数量R**（Figure C.3a）：减少每轮通信的对等体数量仍能保持可合并性，但性能随R降低而单调下降。
- **通信拓扑**（Figure C.3b）：随机图、环形图、指数图均能维持可合并性，其中指数图略优，这与理论分析中随机图能达到p=Θ(1)的混合效率一致。

### 4.5 超参数与初始化稳健性

Figure C.4的消融表明，最终全局合并的效果对以下因素具有稳健性：
- 批量大小（64 vs. 128）
- 学习率（5×10⁻⁴ vs. 1×10⁻⁴）
- 不同初始化方案

Figure C.5进一步验证了在不同数据异质性水平（α=0.1 vs. α=1.0）下，该方法在CIFAR-100和Tiny ImageNet上均表现有效。

### 4.6 最终合并的通信成本与近似方案

全连接全局合并的通信成本为O(2mP)（m个agent各发送和接收P个参数），在本文的去中心化设置中，总通信成本为O(mRPT + 2mP)，其中R≪2为每轮期望对等体数。实验（Figure C.6）表明，即使仅用**一轮基于拓扑的最终gossip合并**（而非全连接AllReduce），也能大幅提升测试准确率；5轮gossip近似可进一步逼近全连接合并的效果。这为带宽极度受限的场景提供了实用替代方案。

### 4.7 收敛率理论验证

Table 1比较了并行SGD与去中心化SGD（DSGD）在非凸设定下的收敛率。本文的Theorem 1证明，DSGD的全局合并模型可以达到与并行SGD匹配的收敛速率，关键在于辅助项U⁽ᵗ⁾在渐进锐化假设（Assumption 4）下为负，使得模型差异部分转化为建设性加速因子。Proposition 2给出了U⁽ᵗ⁾ < 0的充分条件：学习率η > 1/L₂且损失梯度与Hessian迹的梯度负相关。这一理论结果解释了为何去中心化训练配合最终合并能在实践中达到甚至超越中心化联邦学习的性能（如Figure C.1a中观察到的加速现象）。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_zrFnwRHuQo/figures/003_Table_1.jpg]]
*Table 1: Comparison of non-convex convergence rates for parallel SGD and DSGD, both run with m agents under non-IID data*

### 4.8 已知局限

1. **任务范围**：实验仅覆盖视觉分类任务（CIFAR-100, Tiny ImageNet），尚未在NLP或其他领域验证。
2. **理论假设**：渐进锐化假设（Assumption 4）和四阶光滑性在实践中可能不完全满足，Proposition 2中η > 1/L₂的条件对深度网络的大学习率场景提出了约束。
3. **最终合并成本**：全连接AllReduce在极度受限的带宽环境下可能不适用；gossip近似虽有效，但需额外通信轮数。
4. **拓扑动态性**：未研究异步或动态变化网络拓扑下的可合并性维持。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_zrFnwRHuQo/figures/001_Figure.jpg]]
*Figure: (a) CLIP ViT-B/32 (b) ResNet-18 (w/o pretraining) (c) Landscape before final merging (d) A comparative illustration of federated, decentralized, and local training*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_zrFnwRHuQo/figures/002_Figure_2.jpg]]
*Figure 2: (a, b): Comparisons of global test accuracy (see Definition 1) in decentralized training of ResNet-18 on CIFAR-100 with AdamW, distributed across 16 agents with Dirichlet α = 0.1 (see details in Appendix C.1). Fully-connected communication (i.e., AllReduce) is activated only in specific windows, while low communication with one random peer with a probability of 0.2 is used elsewhere. (a): Fully-connected communication in 1/10 of total rounds. (b): Fully-connected communication in 1/20 of total rounds. In both, lighter bars show peak accuracy, darker bars show final accuracy. (c): Global test accuracy curves for local models and the globally averaged model (counterfactual) under persistent l...*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_zrFnwRHuQo/figures/010_Figure.jpg]]
*Figure: (a) Different Batch Sizes (b) Different Learning Rates Tiny ImagNet (m=16,alpha=0.1,random topology) (c) Different Initialization Schemes*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_zrFnwRHuQo/figures/011_Figure.jpg]]
*Figure: C.4: Global test accuracy (see Definition 1) of training ResNet-18 on Tiny ImageNet with decentralized AdamW, distributed across 16 agents with high heterogeneity (Dirichlet α = 0.1; see details in Appendix C.1). We evaluate the effects of different (a) batch sizes (64 vs. 128), (b) learning rates ( 5 \times \mathrm { i } \mathrm { \dot { 0 } ^ { - 4 } } \mathrm { v s . } 1 \times 1 0 ^ { - 4 } ) , and (c) different initialization schemes. (b) (c)*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_zrFnwRHuQo/figures/012_Figure.jpg]]
*Figure: C.5: Global test accuracy (see Definition 1) for ResNet-18 trained with decentralized AdamW across 32 agents under different levels of data heterogeneity (Dirichlet α = 0.1 (a, c) vs. α = 1.0 (b, d); see Appendix C.1). Results are reported on both CIFAR-100 (a, b) and Tiny ImageNet (c, d). (a) 1 Round Final Gossip Merging (b) 5 Rounds Final Gossip Merging (c) 1 Round Final Global Merging*

## 定位与知识库关联

### 与现有范式的边界关系

本文提出的方法位于**联邦学习**、**去中心化学习**与**模型合并**三条研究脉络的交汇点，但其核心贡献在于揭示了一个被现有工作长期忽视的简单事实：在去中心化训练的末端执行一次全连接全局合并，即可在严重通信受限且数据高度异构的条件下获得与中心化联邦学习相当的性能。

**与联邦学习的对比**。标准联邦学习（如 **FedAdamW**）依赖中心服务器在训练全程频繁执行全局聚合，通信开销为 $\mathcal{O}(2mPT)$，其中 $m$ 为 agent 数量，$P$ 为参数量，$T$ 为总通信轮次。本文的去中心化方案将通信成本降至 $\mathcal{O}(mRPT + 2mP)$，其中 $R \ll 2$ 为每轮期望对等体数量（Section 4.3）。在 Tiny ImageNet 上，去中心化 AdamW + 最终合并的性能与 FedAdamW 相当（Figure C.1, C.2），但通信开销大幅降低。与之相对，一次性联邦学习（**One-shot FedAdamW**）仅在最后聚合一次，完全省略中间通信，其性能远逊于本文方法——这恰好印证了本文的核心发现：极少量但非零的中间通信对维持模型的可合并性至关重要。

**与去中心化 SGD 的关系**。**D-PSGD**（Lian et al., 2017）在 IID 设定下包含最终全局合并，但未系统研究其在非 IID、极端通信受限场景下的行为。**SCSP**（Aketi et al., 2021）采用梯度稀疏化与最终合并，但关注点在于压缩而非通信调度。本文的独特之处在于**将通信调度的时间分配作为核心因果调控变量**：通过将有限的通信预算集中于训练后期窗口，并仅在最后一步执行全连接合并，即可获得与全程密集通信相当的性能（Figure 2a, 2b）。

**与模型合并文献的差异**。现有模型合并工作（如权重平均、线性模式连接性研究）通常假设模型在同一初始化附近训练，或依赖复杂的对齐算法。本文表明，在去中心化训练中，即使各 agent 从不同初始化出发、数据分布高度异构（Dirichlet $\alpha = 0.1$），仅需极低概率的随机对等体通信（每轮以 0.2 概率选择一个随机对等体），即可在整个训练过程中维持模型的**全局可合并性**（Definition 2），使得最终一次简单平均即可产生高性能的全局模型。

### 适用边界与条件

本文方法的有效性依赖于以下关键条件，超出这些边界时需谨慎对待：

1. **非零通信的必要性**。当完全去除所有中间通信（纯本地训练）时，全局平均模型的性能几乎为零（Figure 2c 浅橙色曲线），表明可合并性完全依赖于那极少量的稀疏通信。通信概率 $p$ 与模型性能之间存在单调关系：降低每轮对等体数量 $R$ 仍可保持可合并性，但性能随之下降（Figure C.3a）。

2. **通信拓扑的鲁棒性**。随机图、环形图、指数图等多种拓扑均能维持可合并性，其中指数图略优（Figure C.3b）。这一鲁棒性意味着方法不依赖于特定的网络结构。

3. **优化器与超参数的稳健性**。方法在使用 AdamW 优化器、不同学习率（$5 \times 10^{-4}$ 与 $1 \times 10^{-4}$）、不同批量大小（64 与 128）以及不同初始化方案下均表现稳健（Figure C.4）。

4. **数据异质性的影响**。方法在 Dirichlet $\alpha = 0.1$（高度异构）和 $\alpha = 1.0$（中度异构）下均有效（Figure C.5），但在极端异构场景下的边界行为仍需进一步验证。

5. **最终合并的实现方式**。虽然理论分析假设全连接全局合并（AllReduce），但实验表明即使仅用一轮基于拓扑的最终 gossip 合并（而非全连接），也能大幅提升测试准确率（Figure C.6）。这为带宽极度受限的场景提供了近似方案，但需额外通信轮次来逼近全局平均。

### 局限性与待验证假设

**任务与领域的局限性**。现有实验全部在视觉分类任务（CIFAR-100、Tiny ImageNet）上进行，使用 ResNet-18 和 CLIP ViT-B/32 作为骨干网络。方法在 NLP、语音、强化学习等领域的有效性尚未验证，在大规模语言模型上的表现也是开放问题。

**理论假设的实践差距**。理论分析的核心——渐进锐化假设（Assumption 4）要求损失梯度与 Hessian 迹的梯度负相关（$\nabla\mathcal{L}(\theta)^\top \nabla\mathrm{Tr}(\nabla^2\mathcal{L}(\theta)\Sigma) < 0$），且学习率需满足 $\eta > 1/L_2$。这些高阶平滑性条件在实际深度网络中可能不完全满足，且 $L_2$（Hessian 的 Lipschitz 常数）难以精确估计。Proposition 2 中 $U^{(t)} < 0$ 的结论依赖于忽略 $\mathcal{O}(\Xi_t^3)$ 高阶项，当共识误差 $\Xi_t$ 较大时该近似可能失效。

**通信成本的隐藏假设**。最终全局合并需要全连接通信（$\mathcal{O}(2mP)$），在 agent 数量极大或带宽极度受限的场景下可能成为瓶颈。虽然可通过多次 gossip 近似（Figure C.6），但这引入了额外的通信-精度权衡，且最优近似轮次与网络拓扑的关系尚未理论化。

**动态环境的未覆盖**。所有实验均假设静态网络拓扑和同步通信。在 agent 动态加入/退出、异步更新、或通信链路时变等实际部署条件下，方法的鲁棒性尚未被研究。

### 开放问题

1. **自适应通信调度**。如何设计算法通过监测训练动态（如梯度范数 $\mu_t$ 的变化）自动调整通信预算，以满足式 (11) 中的关键共识边缘条件？这需要在不依赖全局信息的去中心化设定中估计景观几何量。

2. **渐进锐化机制的泛化**。渐进锐化效应能否推广到其他分布式优化场景（如异步 SGD、联邦学习的局部更新阶段）以提供额外加速？这需要验证 Assumption 4 在不同优化动力学下的普适性。

3. **局部更新步数与混合速率的联合优化**。在实际大规模深度学习任务中，如何最优地权衡局部更新步数 $H$ 与通信图的混合属性 $p$？式 (11) 提供了理论指导，但将其转化为可操作的超参数选择策略仍需工程探索。

4. **跨领域与真实部署验证**。将实验从视觉分类扩展到更广泛任务，并在真实地理分布式环境中验证方法的实用性，是推动该方向落地的关键步骤。

## 原文 PDF

![[paperPDFs/ICLR_2026/On_The_Surprising_Effectiveness_of_a_Single_Global_Merging_in_Decentralized_Learning.pdf]]
