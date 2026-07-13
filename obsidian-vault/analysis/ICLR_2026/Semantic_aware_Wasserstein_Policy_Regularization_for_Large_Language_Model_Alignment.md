---
title: "Semantic-aware Wasserstein Policy Regularization for Large Language Model Alignment"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Semantic_aware_Wasserstein_Policy_Regularization_for_Large_Language_Model_Alignment.pdf
project_link: null
code_link: https://github.com/aailab-kaist/WPR
openreview_forum_id: sUac3QDbAs
aliases:
- WPRW
- SAWPRLLMA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "采用考虑token空间几何结构的Wasserstein距离（具体为熵正则化Wasserstein距离/Sinkhorn距离）作为策略正则化项，使其能够基于自定义的语义成本矩阵自然地捕捉token间的语义接近程度。"
primary_logic: "通过将熵正则化最优传输问题转化为对偶形式，最优对偶变量可以被解释为每个token应受到的奖励惩罚。该惩罚可直接融入标准的逐token奖励优化框架（如PPO），从而在不显著改变算法流程、仅增加少量Sinkhorn迭代计算开销（约2.5%训练时间）的前提下，实现有效的语义感知策略对齐。"
claims:
- "在文本摘要TL;DR和对话生成HH-RLHF任务上，使用Wasserstein正则化的PPO（WPR）在GPT-4评估的胜率上一致且显著优于所有基于KL和f-散度的基线方法。"
- "WPR产生的token级惩罚与基于BERTScore测量的参考响应语义相似度之间的Pearson相关性，显著强于KL惩罚的相关性，说明其惩罚力度更好地反映了语义偏离。"
- "WPR训练出的模型在生成决策时，其top-10候选token的语义连贯性（以嵌入空间平均距离衡量）优于KL正则化模型，即候选集在语义上更紧凑、更一致。"
- "WPR所需的计算开销极小，通过k-NN和top-k截断后，Sinkhorn算法使每步训练时间仅比标准KL正则化增加约2.5%，整体训练时间相近。"
---

# Semantic-aware Wasserstein Policy Regularization for Large Language Model Alignment

> [!tip] 核心洞察
> 通过将熵正则化最优传输问题转化为对偶形式，最优对偶变量可以被解释为每个token应受到的奖励惩罚。该惩罚可直接融入标准的逐token奖励优化框架（如PPO），从而在不显著改变算法流程、仅增加少量Sinkhorn迭代计算开销（约2.5%训练时间）的前提下，实现有效的语义感知策略对齐。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向大语言模型对齐的语义感知Wasserstein策略正则化 |
| 英文题名 | Semantic-aware Wasserstein Policy Regularization for Large Language Model Alignment |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=sUac3QDbAs) · [GitHub](https://github.com/aailab-kaist/WPR) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Wasserstein Policy Regularization (WPR) |
| Dataset | TL;DR (TL;DR dataset), HH-RLHF (dialogue dataset) |

> [!tip] 效果简介
> - TL;DR (TL;DR dataset) 上，GPT-4 Win Rate (vs. SFT) 为 0.924 (WPR, Gemma-2B)，对比 0.848 (RKL, Gemma-2B); other divergences < 0.9，变化 +0.076 (vs RKL)。
> - TL;DR (TL;DR dataset) 上，GPT-4 Win Rate (vs. RKL) 为 0.608 (WPR, Gemma-2B)，对比 0.5 (RKL vs. itself); other divergences: α 0.592, χ² 0.592, JS 0.584 etc.，变化 +0.108。
> - HH-RLHF (dialogue dataset) 上，GPT-4 Win Rate (vs. SFT) 为 0.852 (WPR, Gemma-2B)，对比 0.812 (RKL, Gemma-2B)，变化 +0.040。

## 概要

现有基于人类反馈的强化学习（RLHF）已成为大语言模型对齐的主流范式，其标准做法是在最大化奖励的同时，通过KL散度或f-散度约束当前策略不偏离参考策略。然而，这些散度仅在相同索引处逐token比较概率值，完全忽略了token之间的语义相似性——语义相近的替代词与无关词被同等对待，限制了模型对齐的质量与生成多样性。

针对这一瓶颈，本文提出**语义感知Wasserstein策略正则化**（Wasserstein Policy Regularization, WPR）。核心思路是将熵正则化Wasserstein距离（Sinkhorn距离）作为策略正则化项，利用基于固定token嵌入欧氏距离构建的语义成本矩阵，自然捕捉token空间中的几何结构与语义邻近关系。通过对偶变换，最优传输问题的对偶变量可被解释为逐token的奖励惩罚，直接融入标准PPO优化框架，仅需增加少量Sinkhorn迭代计算开销（约2.5%训练时间）即可实现语义感知的策略对齐。

在文本摘要（TL;DR）和对话生成（HH-RLHF）任务上，WPR在GPT-4评估的胜率上一致且显著优于所有基于KL和f-散度的基线方法：相较反向KL正则化（RKL），WPR在TL;DR上胜率达0.608，在HH-RLHF上达0.616。机制分析表明，WPR产生的token级惩罚与基于BERTScore的语义相似度相关性显著强于KL惩罚，且其生成决策的top-10候选token在嵌入空间中语义更紧凑。方法在Gemma-2B、Gemma-7B和Qwen1.5-1.8B-Chat等多模型家族上均表现稳健，并在代码生成任务（APPS）上展现出良好的泛化能力。

### 大语言模型对齐中的策略正则化瓶颈

基于人类反馈的强化学习（RLHF）已成为将大语言模型（LLM）与人类偏好对齐的事实标准范式。其核心优化目标可形式化为：

$$\max_{\pi_\theta} \mathbb{E}_{\mathbf{x}\sim\mathcal{D}, \mathbf{y}\sim\pi_\theta}[ r(\mathbf{x},\mathbf{y}) ] - \beta D(\pi_\theta || \pi_{\mathrm{ref}})$$

其中 $r(\mathbf{x},\mathbf{y})$ 为奖励模型给出的标量奖励，$D(\pi_\theta || \pi_{\mathrm{ref}})$ 是当前策略 $\pi_\theta$ 与参考策略 $\pi_{\mathrm{ref}}$（通常由监督微调获得）之间的散度正则化项，$\beta$ 控制正则化强度。该正则化的设计初衷是防止策略在最大化奖励过程中过度偏离参考模型，从而保留预训练阶段习得的语言能力与知识。

现有RLHF实践（如Ouyang et al., 2022）几乎无一例外地采用**反向KL散度**作为 $D$，并将目标逐token分解为可被PPO优化的形式：

$$\mathbb{E}_{\mathbf{x}}\left[\sum_{n=1}^N \mathbb{E}_{y_n}\left[ R(\mathbf{x}, \mathbf{y}_{1:n}) - \beta \log \frac{\pi_\theta(y_n|\dots)}{\pi_{\mathrm{ref}}(y_n|\dots)} \right]\right]$$

其他f-散度（前向KL、Jensen-Shannon散度、α-散度、总变分距离、卡方散度等）也遵循相同的逐位置比较逻辑。

### 核心瓶颈：忽略token空间语义几何

上述所有散度共享一个根本性缺陷：**它们仅在相同索引位置比较两个策略的概率值，完全忽略了token之间的语义相似性**。Figure 1通过一个典型案例揭示了这一问题——当参考策略和两个学习策略在"delighted""happy""elated"等语义相近词与无关词之间分配概率时，KL散度和JS散度无法区分"将概率质量转移到近义词"与"转移到无关词"这两种截然不同的行为，而Wasserstein距离则能自然地捕捉这种语义接近程度。

这一缺陷的后果是双重的：
1. **对齐质量受限**：KL散度对语义上合理的词汇替换施加与无关替换同等的惩罚，过度约束了策略的探索空间，抑制了生成多样性。
2. **惩罚信号失准**：逐token的KL惩罚与生成响应的实际语义质量之间关联薄弱。实验证据表明，在TL;DR和HH-RLHF数据集上，KL惩罚与基于BERTScore测量的参考响应语义相似度之间的Pearson相关性仅为0.1734和0.0172，远低于本文方法（0.2160和0.1749，Table 7），说明KL惩罚未能有效反映语义偏离程度。

### 动机：引入最优传输视角

Wasserstein距离（Earth Mover's Distance）通过求解将一种概率分布传输为另一种的最小成本，天然地考虑了支撑空间（此处为token嵌入空间）的几何结构：

$$D_{\mathbb{W}}(\pi||\pi') = \min_{P \in U(\pi,\pi')} \langle P, C \rangle$$

其中成本矩阵 $C_{ij}$ 通常基于token嵌入的欧氏距离定义，$P$ 为联合传输计划。这使得Wasserstein距离能够区分"将概率质量转移到语义相邻token"与"转移到语义无关token"两种行为，前者产生较低的成本，后者产生较高的成本。

本文的核心动机即是将这一语义感知的距离度量引入RLHF的策略正则化框架，在保持与PPO兼容的前提下，使正则化惩罚能够反映token空间的真实语义几何，从而在约束策略偏离的同时保留合理的语义变体，最终提升对齐质量与生成多样性。

## 核心方法与创新机理

### 瓶颈洞察：从逐点比较到语义感知的策略约束

现有RLHF框架普遍采用KL散度或其f-散度变体作为策略正则化项。这些散度存在一个结构性缺陷：它们仅在**相同索引处**比较两个策略的token概率值，完全忽略了token之间的语义相似性。如图1所示，当参考策略π_ref将概率质量集中在“delighted”上，而学习策略π₁将其转移到语义相近的“happy”时，KL散度与JS散度均将其与转移到无关词“car”的π₂等同视之。这种“语义盲”特性导致正则化项无法区分语义上合理的分布偏移与真正的退化偏移，从而限制了模型对齐的质量上限和生成多样性。

### 方法开关：熵正则化Wasserstein距离作为语义感知正则项

针对上述瓶颈，本文提出**Wasserstein策略正则化（Wasserstein Policy Regularization, WPR）**，将策略约束从逐点概率比较升级为考虑token空间几何结构的**最优传输距离**。具体而言，WPR用熵正则化Wasserstein距离（Sinkhorn距离）替换标准RLHF目标中的KL散度：

$$D_{\tilde{\mathbf{W}}}(\pi_\theta \| \pi_{\mathrm{ref}}) := \min_{P \in U(\pi_\theta, \pi_{\mathrm{ref}})} \left\{ \langle P, C \rangle - \frac{1}{\lambda}\mathcal{H}(P) \right\}$$

其中成本矩阵$C$基于固定token嵌入空间中的欧氏距离构建，$\lambda$为熵正则化强度。这一设计使正则化项能够**自然地捕捉token间的语义接近程度**：将概率质量迁移到语义相近的token（如“delighted”→“happy”）仅产生较小的传输成本，而迁移到无关token则产生高成本，从而形成语义感知的策略约束。

### 核心洞察：对偶变量作为可集成的逐token惩罚

WPR的关键创新在于揭示了熵正则化最优传输问题的**对偶形式**与RLHF优化之间的深层联系。通过将Sinkhorn距离写为对偶问题：

$$\max_{\phi,\psi} \sum_i \phi_i[\pi_\theta]_i + \sum_j \psi_j[\pi_{\mathrm{ref}}]_j - \frac{1}{\lambda}\sum_{i,j}\exp(\lambda(\phi_i+\psi_j - C_{ij}))$$

并利用Sinkhorn-Knopp算法迭代求解，最优对偶变量$\phi^*$可以被解释为**每个token应受到的奖励惩罚**。**定理2**证明，WPR的RLHF目标可等价转化为标准奖励最大化形式：

$$\mathcal{T}_{\bar{W}}(\pi_\theta; \pi_{\mathrm{ref}}) = \mathbb{E}_{\mathbf{x},\mathbf{y}}\left[ \sum_n \left(R(\mathbf{x}, \mathbf{y}_{1:n}) - \beta \phi^*_{y_n} \right) \right] + \mathcal{C}$$

其中$\phi^*_{y_n}$充当逐token的语义感知惩罚，常数$\mathcal{C}$可忽略。这一转化意味着WPR可以**无缝融入标准的PPO优化流程**——仅需将KL惩罚项$\beta \log(\pi_\theta / \pi_{\mathrm{ref}})$替换为$-\beta \phi^*_{y_n}$，无需改动强化学习算法的其余部分。

### 工程实现：双截断Sinkhorn算法的轻量集成

为将上述理论框架落地到LLM的大词汇表场景，WPR引入两个关键截断策略：
- **k-NN截断（k₁=512）**：在预计算成本矩阵时，每个token仅保留与其嵌入空间中最邻近的k₁个token的传输成本，其余设为无穷大。
- **Top-k截断（k₂=128）**：在Sinkhorn迭代中，将策略分布压缩到概率最高的k₂个token加一个虚拟token，大幅降低传输矩阵规模。

这些设计使WPR的训练时间仅比标准KL正则化**增加约2.5%**，同时保持了Sinkhorn迭代的数值收敛性（Figure 7）。

### 与基线的关键差异总结

| 设计维度 | 标准RLHF（RKL） | WPR（本文） |
|---------|----------------|------------|
| 正则化散度类型 | 反向KL散度 | 熵正则化Wasserstein距离（Sinkhorn距离） |
| 逐token惩罚形式 | $\beta \log(\pi_\theta / \pi_{\mathrm{ref}})$ | $-\beta \phi^*_{y_n}$（依赖于token空间几何） |
| 距离计算基础 | 仅比较相同索引上的概率值 | 基于固定token嵌入欧氏距离构建成本矩阵$C$ |
| 语义感知能力 | 无（语义盲） | 有（通过成本矩阵捕捉token间语义关系） |
| 计算开销 | 基准 | 每步训练时间增加约2.5% |

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_sUac3QDbAs/figures/008_Figure_3.jpg]]
*Figure 3: Overview of RLHF with Wasserstein Policy Regularization. (a) Standard RLHF with a policy regularization penalty. (b) Our proposed Wasserstein policy regularization, where the penalty is computed from the optimal dual variables obtained via the Sinkhorn-Knopp algorithm*

WPR 的整体管线在标准 RLHF 三阶段流程的基础上，将策略正则化项从 KL 散度替换为熵正则化 Wasserstein 距离（Sinkhorn 距离），并通过对偶变换将其转化为可嵌入 PPO 训练循环的逐 token 惩罚。图 3 给出了标准 RLHF 与 WPR 的对比概览。

**管线模块与数据流**

1. **监督微调（SFT）**：在人工标注的高质量数据上微调预训练大语言模型，得到初始参考策略 $\pi_{\mathrm{ref}}$。该策略同时提供固定的 token 嵌入空间，用于后续构建语义成本矩阵。

2. **奖励模型训练**：基于人类偏好比较数据训练奖励模型 $r(\mathbf{x}, \mathbf{y})$，为策略优化提供逐序列的标量奖励信号。

3. **PPO 训练循环（含 WPR 惩罚）**：这是方法的核心执行阶段，包含以下子步骤：
   - **响应生成**：当前策略 $\pi_\theta$ 根据提示 $\mathbf{x}$ 自回归生成完整响应 $\mathbf{y} = (y_1, \dots, y_N)$。
   - **Wasserstein 惩罚计算**：对每个生成步 $n$，将 $\pi_\theta(\cdot|\mathbf{x}, \mathbf{y}_{1:n-1})$ 与 $\pi_{\mathrm{ref}}(\cdot|\mathbf{x}, \mathbf{y}_{1:n-1})$ 之间的 Sinkhorn 距离转化为最优对偶变量 $\phi^*_{y_n}$，作为该 token 的语义感知惩罚。具体计算由截断 Sinkhorn-Knopp 算法完成（见下文）。
   - **奖励修正**：将原始奖励与惩罚合并为修正后的逐 token 奖励 $\tilde{R}(\mathbf{x}, \mathbf{y}_{1:n}) = R(\mathbf{x}, \mathbf{y}_{1:n}) - \beta \phi^*_{y_n}$（其中 $R$ 仅在序列末步非零）。
   - **优势估计与策略更新**：基于修正奖励计算广义优势估计（GAE），并更新策略网络和价值网络参数。

**Wasserstein 惩罚计算模块的内部流程**

该模块是 WPR 区别于标准 KL 正则化的关键。其输入为当前策略分布 $\pi_\theta$ 和参考策略分布 $\pi_{\mathrm{ref}}$，输出为逐 token 的对偶惩罚 $\phi^*$。具体步骤为：

- **成本矩阵预计算**：利用参考策略的固定 token 嵌入，基于欧氏距离构建完整的 $d \times d$ 成本矩阵 $C$（$d$ 为词表大小）。为降低后续计算开销，对每个 token 仅保留其 $k_1$ 个最近邻的成本值（nearest-$k_1$ 截断），其余置为无穷大。
- **top-$k_2$ 截断**：在每次 Sinkhorn 迭代前，将 $\pi_\theta$ 和 $\pi_{\mathrm{ref}}$ 的概率质量截断到各自 top-$k_2$ 的 token 上，并引入一个虚拟 token 吸收剩余概率质量，从而将传输问题的维度从 $d$ 压缩至 $k_2+1$。
- **Sinkhorn-Knopp 迭代**：在截断后的分布上执行约 10 次迭代，得到缩放向量 $\mathbf{u}, \mathbf{v}$，进而通过 $\boldsymbol{\phi}^* = -\frac{1}{\lambda}\log(\mathbf{u})$ 提取最优对偶变量作为惩罚。

**计算开销**

上述截断策略使 WPR 的额外计算开销极为有限：在 Gemma-2B 上，每步训练时间仅比标准 KL 正则化增加约 2.5%（生成和反向传播时间不变，仅惩罚计算从 0.005 h/千步增至 0.117 h/千步）。但 GPU 显存占用约增加 15 GB，主要来自成本矩阵的存储。

> **手动验证提示**：关于显存增加的具体数值（15 GB）以及跨模型规模的显存缩放特性，原文仅在 Gemma-2B 上报告，更大模型上的显存开销需进一步确认。

### 瓶颈与核心思想

现有RLHF策略正则化方法（如KL散度及各类f-散度）在逐token比较策略分布时，仅在相同索引处比较概率值，完全忽略了token之间的语义相似性。这导致模型无法区分语义相近的替代词与完全无关的词，从而限制了策略对齐的质量与生成多样性。WPR的核心洞察在于：引入考虑token嵌入空间几何结构的**熵正则化Wasserstein距离（Sinkhorn距离）**作为策略正则化项，使其能够基于自定义的语义成本矩阵自然地捕捉token间的语义接近程度。

更关键的是，通过将熵正则化最优传输问题转化为对偶形式，最优对偶变量可以被解释为每个token应受到的**奖励惩罚**。该惩罚可直接融入标准的逐token奖励优化框架（如PPO），从而在不显著改变算法流程的前提下实现语义感知的策略对齐。

### 核心公式推导链路

#### 1. 基础定义：Wasserstein距离与Sinkhorn距离

给定两个token概率分布 $\pi$ 和 $\pi'$，以及定义在token嵌入空间上的成本矩阵 $C$（其中 $C_{ij}$ 表示token $i$ 与token $j$ 之间的语义距离），Wasserstein距离定义为最优传输问题的最小成本：

$$D_{\mathbb{W}}(\pi||\pi') := \min_{P \in U(\pi,\pi')} \mathbb{E}_{(y,y')\sim P}[c(y,y')] = \min_{P} \langle P, C \rangle$$

其中 $U(\pi,\pi')$ 是边缘分布为 $\pi$ 和 $\pi'$ 的所有联合分布（传输计划）的集合。该距离直接计算将分布 $\pi$ “搬运”到 $\pi'$ 所需的最小语义成本，因此能够区分“语义相近的替换”与“语义无关的替换”。

由于精确Wasserstein距离在大词汇表上计算代价过高，WPR采用**熵正则化Wasserstein距离**（Sinkhorn距离）：

$$D_{\tilde{\mathbf{W}}}(\pi||\pi') := \min_{P \in U(\pi,\pi')} \left\{ \langle P,C\rangle - \frac{1}{\lambda}\mathcal{H}(P) \right\}$$

其中 $\mathcal{H}(P) = -\sum_{i,j} P_{ij}(\log P_{ij} - 1)$ 为传输计划的熵，$\lambda > 0$ 控制正则化强度。熵正则化使最优传输问题变得光滑，从而可通过高效的Sinkhorn-Knopp算法迭代求解。

#### 2. 从KL正则化到Wasserstein正则化

标准RLHF目标为最大化期望奖励同时约束策略不偏离参考策略 $\pi_{\mathrm{ref}}$：

$$\max_{\pi_\theta} \mathbb{E}_{\mathbf{x}\sim\mathcal{D}, \mathbf{y}\sim\pi_\theta}[ r(\mathbf{x},\mathbf{y}) ] - \beta D(\pi_\theta || \pi_{\mathrm{ref}})$$

当 $D$ 为KL散度时，可将其逐token分解为对数概率比，形成可被PPO优化的奖励惩罚形式：

$$\mathbb{E}_{\mathbf{x}}\left[\sum_{n=1}^N \mathbb{E}_{y_n}\left[ R(\mathbf{x}, \mathbf{y}_{1:n}) - \beta \log \frac{\pi_\theta(y_n|\dots)}{\pi_{\mathrm{ref}}(y_n|\dots)} \right] \right]$$

此处 $R(\mathbf{x}, \mathbf{y}_{1:n})$ 在最终token处为奖励模型输出，其余位置为0。

WPR的核心替换：将上述目标中的KL散度替换为**熵正则化Wasserstein距离**，得到：

$$\mathbb{E}_{\mathbf{x}\sim\mathcal{D}}\left[\sum_{n=1}^N \mathbb{E}_{y_n}\left[ R(\mathbf{x}, \mathbf{y}_{1:n}) \right] - \beta \sum_{n=1}^N D_{\tilde{\mathbf{W}}}^{\lambda}( \pi_\theta || \pi_{\mathrm{ref}} )\right]$$

#### 3. 对偶形式与惩罚的导出（关键转化）

熵正则化最优传输问题具有对偶形式：

$$\max_{\phi,\psi} \sum_i \phi_i[\pi_\theta]_i + \sum_j \psi_j[\pi_{\mathrm{ref}}]_j - \frac{1}{\lambda}\sum_{i,j}\exp(\lambda(\phi_i+\psi_j - C_{ij}))$$

其中 $\phi, \psi \in \mathbb{R}^d$ 为对偶变量（$d$ 为词汇表大小）。该对偶问题的拉格朗日形式为：

$$\mathcal{L}(P^{(n)},\boldsymbol{\phi},\boldsymbol{\psi}):=\sum_{i=1}^{d}\sum_{j=1}^{d}\left(P_{ij}^{(n)}C_{ij}+\frac{1}{\lambda}P_{ij}^{(n)}(\log P_{ij}^{(n)}-1)\right)+\sum_{i=1}^{d}\phi_i([\pi_\theta]_i-\sum_{k=1}^{d}P_{ik}^{(n)})+\sum_{j=1}^{d}\psi_j([\pi_{\mathrm{ref}}]_j-\sum_{k=1}^{d}P_{kj}^{(n)})$$

通过Sinkhorn-Knopp算法迭代求解矩阵缩放问题，可获得最优对偶变量。具体地，最优解由缩放向量 $\mathbf{u}, \mathbf{v}$ 给出：

$$P^{(n)*} = \mathrm{diag}(\mathbf{u}) \exp(-\lambda C) \mathrm{diag}(\mathbf{v}), \quad \boldsymbol{\phi}^* = -\frac{1}{\lambda}\log(\mathbf{u}), \quad \boldsymbol{\psi}^* = -\frac{1}{\lambda}\log(\mathbf{v})$$

**Theorem 2（等价奖励形式）**：熵正则化Wasserstein约束的RLHF目标可等价转化为标准奖励最大化问题：

$$\mathcal{T}_{\bar{W}}(\pi_\theta; \pi_{\mathrm{ref}}) = \mathbb{E}_{\mathbf{x},\mathbf{y}}\left[ \sum_n (R(\mathbf{x}, \mathbf{y}_{1:n}) - \beta \phi^*_{y_n} ) \right] + \mathcal{C}$$

其中 $\phi^*_{y_n}$ 是生成token $y_n$ 对应的最优对偶变量，充当**逐token的语义感知惩罚**；常数 $\mathcal{C}$ 与策略参数无关，在优化中可忽略。

这一转化的关键意义在于：**WPR的惩罚项在形式上与KL惩罚（$-\beta \log(\pi_\theta/\pi_{\mathrm{ref}})$）完全一致，均为逐token的标量惩罚，因此可直接嵌入现有PPO训练流程**，无需修改优势估计或策略梯度计算模块。

### 高效计算模块：双截断Sinkhorn算法

WPR的计算瓶颈在于每步生成后需对每个token位置求解Sinkhorn距离。为降低计算复杂度，WPR采用两种截断策略：

- **最近邻截断（nearest-$k_1$）**：在预计算成本矩阵 $C$ 时，仅保留每个token嵌入空间中距离最近的 $k_1$ 个token，其余位置设为无穷大。这使成本矩阵变为稀疏矩阵。
- **Top-$k_2$ 截断**：在Sinkhorn-Knopp迭代中，仅保留每个分布中概率最大的 $k_2$ 个token，并将剩余概率质量分配给一个虚拟token。这使每次迭代的矩阵运算规模从 $d \times d$ 降至 $k_2 \times k_2$。

完整计算流程如**Algorithm 1**所示：对每个生成位置 $n$，输入当前策略分布 $\pi_\theta$ 和参考策略分布 $\pi_{\mathrm{ref}}$，经过top-$k_2$截断后，在截断后的成本矩阵上执行Sinkhorn-Knopp迭代（默认10次），输出最优对偶变量 $\phi^*$ 作为该位置的惩罚向量。

消融实验（Table 6）验证了各截断参数的关键性：$k_2$ 从128降至64会导致性能下降，而Sinkhorn迭代次数从10降至5则严重损害性能（vs RKL胜率降至0.328），说明充分收敛的Sinkhorn迭代对获得有效惩罚至关重要。最终，整套WPR方案使每步训练时间仅比标准KL正则化增加约2.5%。

## 实验与关键发现

### 核心结果：WPR在所有基准上一致超越KL及f-散度基线

WPR的核心主张——语义感知的正则化能带来更好的对齐质量——在文本摘要和对话生成两个主流RLHF基准上得到了严格验证。Table 1报告了在Gemma-2B模型上，以GPT-4评估的胜率作为主要指标的系统性比较。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_sUac3QDbAs/figures/009_Table_1.jpg]]
*Table 1: Comparison of win rates for policy regularization with various divergences, compared to SFT and RKL-regularized PPO on the TL;DR and the HH-RLHF datasets with the Gemma-2B model*

**文本摘要（TL;DR）**：WPR相对于SFT基线的胜率达到**0.924**，显著高于反向KL正则化（RKL）的0.848，以及所有其他f-散度方法（均低于0.9）。当以RKL为直接对手进行两两比较时，WPR的胜率为**0.608**，意味着在语义感知正则化下训练的模型生成的摘要，在60.8%的情况下被GPT-4判定优于标准RLHF训练的模型。相比之下，表现最好的f-散度替代方案（α-散度和χ²散度）的胜率仅为0.592。

**对话生成（HH-RLHF）**：WPR的优势同样稳健。相对于SFT的胜率为**0.852**（RKL为0.812），相对于RKL的胜率为**0.616**。这表明语义感知的正则化在需要维持多轮对话连贯性和有用性的场景下，同样能产生一致的质量提升。

**跨模型和跨任务泛化**：WPR的优势并非局限于特定模型规模或家族。在Gemma-7B上（Table 2），WPR相对于RKL-7B的胜率为0.532，相对于SFT-7B的胜率为0.924，均保持领先。在Qwen1.5-1.8B-Chat上（Table 3），WPR相对于RKL的胜率为0.560，相对于SFT的胜率为0.752，进一步验证了方法的模型架构无关性。在代码生成任务APPS上（Table 5），使用CodeGemma-7B时，WPR的pass@1率达到**8.79**，远超RKL的6.72和SFT的4.47，证明语义感知正则化能有效泛化至代码对齐场景。在多轮对话综合评估MT-Bench上（Table 4），WPR得分**4.272**，在所有f-散度方法中最高（RKL为3.932）。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_sUac3QDbAs/figures/013_Table_5.jpg]]
*Table 5: Performance comparison on APPS with the CodeGemma-7B model*

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_sUac3QDbAs/figures/010_Table_2.jpg]]
*Table 2: Win rates on TL;DR with Gemma-7B. ‘-2B’ compares to the 2B models in Table 1, and ‘-7B’ to the 7B baselines. Table 3: Win rates on HH-RLHF with Qwen1.5-1.8B-Chat*

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_sUac3QDbAs/figures/011_Table_3.jpg]]

### 机制验证：WPR惩罚确实编码了语义信息

WPR的核心机制假设是：基于Wasserstein距离的对偶惩罚能够捕捉token间的语义相似性，从而在训练中施加更合理的约束。三项互补的实证分析支持了这一假设。

**惩罚-语义相关性**：Table 7报告了逐token的负惩罚值与下游生成响应的BERTScore之间的Pearson相关系数。在TL;DR上，WPR惩罚的相关性为**0.2160**，显著高于KL惩罚的0.1734；在HH-RLHF上，这一差距更为悬殊——WPR为**0.1749**，而KL仅为0.0172。这说明WPR的惩罚力度与生成质量的语义度量更为一致：当模型倾向于生成语义偏离参考的token时，Wasserstein惩罚会施加更强的约束，而KL惩罚对此不敏感。

**候选token的语义连贯性**：Table 8量化了模型在生成决策时，top-10候选token在嵌入空间中的平均欧氏距离。WPR训练出的模型在两个数据集上均表现出更紧凑的候选集：TL;DR上为**3.593**（RKL为3.781），HH-RLHF上为**3.584**（RKL为3.690）。更小的平均距离意味着模型倾向于在语义上更连贯的替代词之间进行选择，而非在无关token间跳跃，这正是语义感知正则化期望诱导的行为。

**训练动态中的惩罚一致性**：Figure 5显示，在整个训练过程中，归一化的KL惩罚与Wasserstein惩罚呈现强正相关（r=0.917），表明两者在宏观趋势上一致。然而，局部存在显著差异——这些差异正是WPR捕捉到KL所忽略的语义信息的关键窗口。

### 消融研究：各组件的必要性与敏感性

Table 6的系统消融揭示了WPR各设计选择的贡献。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_sUac3QDbAs/figures/014_Table_6.jpg]]
*Table 6: Ablation study of WPR on $\mathrm { T L } ; \mathrm { D R }$

**成本函数的选择**：将默认的L2距离替换为余弦相似度后，性能进一步提升（vs SFT: 0.932, vs RKL: 0.644）。这表明语义相似度的度量方式是可优化的，且WPR框架对不同的成本定义具有良好的兼容性。

**截断参数的影响**：减少最近邻截断参数k1（512→256）或熵正则化系数λ（100→10）仅导致性能轻微下降，说明方法对这些参数具有一定的鲁棒性。然而，减少top-k2截断（128→64）会带来更明显的性能损失，表明在Sinkhorn迭代中保留足够多的概率质量对获得有效的对偶变量至关重要。

**Sinkhorn收敛性的关键作用**：最关键的发现是，将Sinkhorn迭代次数从10降至5会导致性能崩溃——相对于RKL的胜率骤降至**0.328**。Figure 7验证了在Gemma-2B的实际训练中，Sinkhorn算法的收敛指标稳定下降，表明充分的迭代对于获得准确的对偶变量不可或缺。这一发现强调了WPR的有效性并非来自近似计算本身，而是来自充分收敛后对语义结构的精确捕捉。

**计算开销的精确分解**：Table 15提供了每1000训练步的墙钟时间分解。生成（0.769小时）和反向传播（3.707小时）是共享的固定开销。惩罚计算部分，RKL仅需0.005小时，而WPR需要0.117小时。总体而言，WPR的每步训练时间仅比标准KL正则化增加约**2.5%**，整体训练时间相近。但需注意，Table 16显示WPR的GPU显存占用约增加15GB（对于Gemma-2B），这在资源受限环境中可能构成瓶颈。

### 失败模式与局限性

尽管WPR在主要基准上表现优异，仍需注意以下边界条件：

1. **β超参数仍需手动搜索**：Table 10显示不同任务和散度方法的最优β值差异显著（WPR在TL;DR上为0.01，在HH-RLHF上为0.005），增加了调参负担。Figure 4的敏感性分析表明WPR在较宽β范围内均优于SFT基线，但最优值仍需针对每个任务单独确定。

2. **成本矩阵的静态性**：当前实现使用固定的、预训练的SFT模型嵌入构建成本矩阵，未在训练过程中更新。Table 12的消融显示，切换策略骨干或嵌入空间会影响性能，说明成本矩阵的质量对WPR的有效性有直接影响。

3. **跨tokenizer泛化未验证**：方法依赖策略模型的tokenizer构建语义空间，若需利用不同tokenizer的嵌入，需构建非平凡的跨token对齐，这在当前框架中尚未解决。

4. **仅在PPO框架下验证**：所有实验均基于PPO风格的RLHF，尚未在DPO等RL-free方法上验证WPR对偶惩罚思想的适用性。

## 定位与知识库关联

### 1 核心瓶颈与因果机制

当前基于人类反馈的强化学习（RLHF）在策略正则化环节存在一个被广泛忽视的结构性缺陷：主流的KL散度及其变体（f-散度族）在逐token施加惩罚时，仅比较相同索引位置上的概率值，完全忽略了词汇表中token之间的语义几何关系。这意味着，当一个token被替换为语义高度相近的同义词时，KL散度会施加与替换为无关词等量的惩罚，从而错误地压制了合理的语义多样性。

本文提出的**语义感知Wasserstein策略正则化（Wasserstein Policy Regularization, WPR）** 直接针对上述瓶颈，其因果调节旋钮是：将策略正则化项从逐点概率比替换为考虑token嵌入空间几何结构的**熵正则化Wasserstein距离（Sinkhorn距离）**。该距离以预训练token嵌入间的欧氏距离构建成本矩阵 $C$，通过最优传输自然地捕捉token间的语义接近程度。

其核心洞察在于对偶性的利用：熵正则化最优传输问题的对偶形式产生一组最优对偶变量 $\phi^*$，这些变量可被严格解释为每个token应受到的奖励惩罚。通过**Theorem 2**的等价变换，WPR目标被重写为标准奖励最大化问题，其中 $\phi^*_{y_n}$ 直接作为逐token的惩罚项融入奖励信号，从而无需修改PPO等标准RL算法的核心流程。

### 2 在RLHF方法谱系中的位置

WPR属于**基于PPO的RLHF策略正则化方法的改进分支**，其直接对话对象是KL散度和f-散度族的正则化方案。

**基线方法体系**（均在同一PPO框架下进行公平对比，超参数 $\beta$ 经网格搜索调优）：

| 方法 | 正则化散度 | 在谱系中的角色 |
|------|-----------|---------------|
| **RKL-regularized RLHF** | 反向KL散度 | RLHF的事实标准基线（Ouyang et al., 2022） |
| **FKL-regularized RLHF** | 前向KL散度 | 模式覆盖型变体 |
| **JS-regularized RLHF** | Jensen-Shannon散度 | 对称化f-散度变体 |
| **α-divergence-regularized RLHF** | α-散度（α=0.5） | 介于KL与RKL之间的插值 |
| **TV-regularized RLHF** | 总变分距离 | 非对称距离度量 |
| **χ²-regularized RLHF** | 卡方散度 | 对尾部敏感的正则化 |
| **SFT** | 无正则化 | 仅监督微调的初始策略 |

WPR与上述方法的**本质差异**在于三个维度：

1. **正则化散度类型**：从逐点概率比（KL/f-散度）切换为考虑token间几何距离的Wasserstein距离（Sinkhorn距离），对应Eq. (8) vs Eq. (10)。
2. **逐token惩罚形式**：从 $\beta \log(\pi_\theta / \pi_{\text{ref}})$ 切换为基于最优对偶变量的语义感知惩罚 $-\beta \phi^*_{y_n}$，对应Eq. (8) vs Eq. (15)及Theorem 2。
3. **距离计算基础**：从无空间概念的概率值比较，切换为基于固定token嵌入欧氏距离构建成本矩阵 $C$ 并计算Sinkhorn距离。

**与DPO等RL-free方法的关系**：本文方法严格基于PPO风格的RLHF框架，尚未验证在直接偏好优化（DPO）等隐式策略约束方法上的适用性。这是当前方法谱系中的一个明确边界——WPR的对偶惩罚机制依赖于显式的策略分布与参考分布之间的最优传输计算，如何将其思想推广至DPO的隐式奖励重参数化框架，是论文明确指出的开放问题。

### 3 关键技术组件与计算特性

WPR在标准PPO训练循环中插入了一个**Wasserstein惩罚计算模块**（Algorithm 1），其核心是双截断的Sinkhorn-Knopp算法：

- **k1-NN截断**：在预计算成本矩阵时，每个token仅保留与其嵌入空间中最邻近的 $k_1=512$ 个token的成本值，其余置为无穷大，将成本矩阵稀疏化。
- **top-k2截断**：在Sinkhorn迭代中，将策略分布截断为概率最高的 $k_2=128$ 个token加一个虚拟token（吸收剩余概率质量），将传输问题的维度从完整词汇表（通常数万维）压缩至 $k_2+1$ 维。

这种设计使得每步训练的额外时间开销仅约**2.5%**（相较于标准KL正则化），但GPU显存占用增加约**15GB**（以Gemma-2B为基准），在资源受限环境中可能构成实际约束。

### 4 实验证据强度与泛化边界

**决定性证据**：

- 在文本摘要TL;DR和对话生成HH-RLHF两个任务、Gemma-2B/Gemma-7B/Qwen1.5-1.8B-Chat三个模型家族上，WPR在GPT-4评估的胜率上一致且显著优于所有KL和f-散度基线（Table 1-3）。核心数据：TL;DR上WPR vs RKL胜率0.608，HH-RLHF上0.616。
- WPR产生的token级惩罚与BERTScore测量的参考响应语义相似度之间的Pearson相关性显著强于KL惩罚（Table 7：TL;DR上0.2160 vs 0.1734；HH-RLHF上0.1749 vs 0.0172），直接验证了惩罚力度的语义感知能力。
- WPR训练出的模型在生成决策时，top-10候选token在嵌入空间中的平均距离更小（Table 8：TL;DR上3.593 vs 3.781；HH-RLHF上3.584 vs 3.690），表明候选集语义更紧凑、更一致。
- 在代码生成任务APPS上，WPR（CodeGemma-7B）的pass@1率从RKL的6.72提升至8.79（Table 5），展示了向代码对齐任务的泛化能力。

**消融揭示的关键依赖**：

- Sinkhorn迭代次数从10降至5会导致性能崩溃（vs RKL胜率降至0.328），说明充分收敛的Sinkhorn算法对获得有效惩罚至关重要（Table 6, Figure 7）。
- 成本函数从L2距离切换为余弦相似度可进一步提升性能（vs SFT胜率0.932, vs RKL胜率0.644），表明语义相似度度量方式仍有优化空间（Table 6）。
- top-k2截断参数 $k_2=128$ 在概率质量捕获与计算开销间取得平衡，继续增大至256未带来明显增益（Table 13）。

### 5 适用边界与已知局限

1. **框架依赖**：仅验证于PPO风格的RLHF，未涉及DPO等RL-free方法。
2. **成本矩阵静态性**：使用固定的、预训练的SFT模型token嵌入构建成本矩阵，未在训练过程中更新或学习，可能无法适应策略分布漂移后的语义空间变化。
3. **跨tokenizer障碍**：成本矩阵依赖策略模型的tokenizer，若希望利用不同tokenizer的嵌入（如更大模型或异构模型），需要构建非平凡的跨token对齐机制。
4. **超参数敏感性**：$\beta$ 仍需针对每个任务手动搜索，增加了调参负担。
5. **资源开销**：尽管时间开销仅增加2.5%，但GPU显存增加约15GB（Gemma-2B），在资源受限环境中可能受限。
6. **规模泛化未充分验证**：成本矩阵和Sinkhorn迭代参数仅在特定tokenizer和模型尺寸（2B-7B）上验证，泛化至更大模型或不同tokenizer时可能需要调整截断参数和嵌入空间。

### 6 开放问题

1. **向DPO框架的推广**：如何将对偶惩罚思想迁移至DPO的隐式奖励重参数化，实现语义感知的隐式策略约束？
2. **自适应正则化强度**：是否可以开发无需手动调优的 $\beta$ 机制，将Wasserstein距离自然融入更稳定的优化目标？
3. **跨tokenizer语义迁移**：如何支持不同tokenizer嵌入空间之间的最优传输，使WPR能利用来自更大或异构模型的语义知识？
4. **可学习成本矩阵**：是否可以通过微调或轻量级网络动态学习成本矩阵 $C$，使其随模型训练适应性地捕捉语义？
5. **更大规模验证**：WPR在7B+模型上的缩放特性，以及在RLHF不同阶段（如奖励建模期间）使用Wasserstein距离的潜力。

## 原文 PDF

![[paperPDFs/ICLR_2026/Semantic_aware_Wasserstein_Policy_Regularization_for_Large_Language_Model_Alignment.pdf]]
