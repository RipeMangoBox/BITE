---
title: "A Near-Optimal Best-of-Both-Worlds Algorithm for Federated Bandits"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Near_Optimal_Best_of_Both_Worlds_Algorithm_for_Federated_Bandits.pdf
aliases:
- NOBBWAFB
- FEDFTRL
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/learning_theory
core_operator: "将分布式通信带来的延迟建模为反馈延迟，并采用混合正则化器（hybrid regularizer）和截断损失估计器（truncated loss estimator）来对齐各智能体的动作概率分布。"
primary_logic: "通过截断损失估计器防止罕见臂的估计值爆炸，从而保持各智能体动作概率的近似一致；利用通信延迟的视角，将联邦学习问题转化为带延迟的赌博机问题，并采用FTRL框架实现随机与对抗环境下的统一最优性。"
claims:
- "FEDFTRL是首个在联邦赌博机中实现BOBW遗憾保证的算法"
- "在对抗环境下，FEDFTRL的个体遗憾界为O(√(KT/V) + √(C_T^P T log K))，优于先前工作的O(T^{2/3})"
- "在随机环境下，FEDFTRL的个体遗憾界为O(∑_{k≠k*} log T / (V Δ_k))，匹配下界"
- "合成数据集 上 平均累积遗憾 = FEDFTRL"
---

# A Near-Optimal Best-of-Both-Worlds Algorithm for Federated Bandits

> [!tip] 核心洞察
> 通过截断损失估计器防止罕见臂的估计值爆炸，从而保持各智能体动作概率的近似一致；利用通信延迟的视角，将联邦学习问题转化为带延迟的赌博机问题，并采用FTRL框架实现随机与对抗环境下的统一最优性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 联邦赌博机中一种近乎最优的“两全其美”算法 |
| 英文题名 | A Near-Optimal Best-of-Both-Worlds Algorithm for Federated Bandits |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Lkndkxeemx) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/learning_theory |
| Method | FEDFTRL |
| Dataset | 合成数据集, MovieLens数据集 |

> [!tip] 效果简介
> - 合成数据集 上，平均累积遗憾 为 FEDFTRL，对比 FEDEXP3, IND-FTRL, GOSSIP UCB, DRBB-bandit，变化 FEDFTRL outperforms all baselines。
> - MovieLens数据集 上，平均累积遗憾 为 FEDFTRL，对比 FEDEXP3, IND-FTRL, GOSSIP UCB, DRBB-bandit，变化 FEDFTRL significantly outperforms all baselines。

## 概述

联邦赌博机（federated bandits）面临的核心瓶颈是：现有算法无法在**随机环境**与**对抗环境**这两种截然不同的损失模式下同时取得近乎最优的遗憾保证，即缺乏“两全其美”（Best-of-Both-Worlds, BOBW）特性。本文提出的 **FEDFTRL** 算法是首个解决该问题的方案。

**核心结论**：FEDFTRL 在随机环境下实现了与最优下界匹配的个体遗憾界 $O(\sum_{k\neq k^*} \log T / (V \Delta_k))$，在对抗环境下实现了 $O(\sqrt{KT/V} + \sqrt{C_T^P T \log K})$ 的遗憾界，将此前对抗环境下最优的 $O(T^{2/3})$ 提升至 $O(T^{1/2})$ 量级。实验在合成数据集和 MovieLens 数据集上均验证了其超越现有基线（FEDEXP3、IND-FTRL、GOSSIP UCB、DRBB-bandit）的性能。

**方法定位**：FEDFTRL 的核心因果机制是将联邦学习中的去中心化通信延迟显式建模为反馈延迟参数 $C_t^P$，进而将问题转化为带延迟的赌博机。算法通过两个关键设计实现统一最优性：(1) **混合正则化器**——结合 Tsallis-INF 和负熵正则化项，使算法能同时适应随机与对抗环境；(2) **截断损失估计器**——对罕见臂的估计值进行截断，避免因分布式通信导致的概率分布发散，保持各智能体动作概率的近似一致性。此外，通过交换累积损失估计器和偏差记录集，算法修正了截断引入的偏差，确保全局共识。

**主要结果**：理论分析给出了个体伪遗憾的严格上界（Theorem 1），实验在三种通信网络拓扑（完全图、网格图、RGG-0.5）上均显示 FEDFTRL 显著优于基线，且对拓扑参数 $C_t^P$ 的选择具有鲁棒性。

## 背景与动机

联邦赌博机（Federated Bandits）是分布式学习中的一个重要设定：V个智能体通过一个连通无向图进行通信，协作求解一个K臂赌博机问题。每个智能体在每轮独立选择臂并观测损失，目标是使所有智能体的个体后悔（相对于全局最优臂的期望累积损失差）尽可能小。然而，现有联邦赌博机算法在设计时通常只针对单一环境假设——要么假设损失由固定分布生成（随机环境），要么假设损失由对手自适应选择（对抗环境）。这就引出了核心瓶颈：**缺乏一种能在随机和对抗两种环境下同时取得近乎最优后悔保证的“两全其美”（Best-of-Both-Worlds, BOBW）算法**。

具体而言，在对抗环境下，已有联邦算法（如FEDEXP3）的个体后悔界为 $O(T^{2/3})$，远劣于单智能体对抗赌博机的最优 $O(\sqrt{T})$ 界；在随机环境下，虽然存在基于gossip通信或分布式逐次消除的算法（如GOSSIP UCB、DRBB-bandit），但它们无法在对抗环境下提供任何有意义的保证。这种“环境依赖”的设计缺口意味着，实际部署时若环境类型未知或动态变化，算法性能可能急剧恶化。

本文的动机正是填补这一缺口。核心洞察在于：**将去中心化通信带来的信息延迟显式建模为反馈延迟**，从而将联邦赌博机问题转化为一个带延迟的、具有特殊网络结构的赌博机问题。基于此，作者提出了FEDFTRL算法，其关键因果机制包括：(1) 采用**混合正则化器**（hybrid regularizer），结合Tsallis-INF和负熵正则化，这是BOBW单智能体算法（Zimmert & Seldin, 2020）的核心技术；(2) 引入**截断损失估计器**（truncated loss estimator），通过分母截断防止罕见臂的估计值爆炸，从而在分布式通信下维持各智能体动作概率的近似一致；(3) 设计**偏差记录与传播机制**，通过交换累积损失估计器和偏差记录集来修正截断引入的偏差，确保全局一致性。这一设计使得FEDFTRL成为首个在联邦赌博机中实现BOBW后悔保证的方法，在对抗环境下达到 $O(\sqrt{KT/V} + \sqrt{C_T^P T \log K})$ 的个体后悔界（优于先前工作的 $O(T^{2/3})$），在随机环境下达到 $O(\sum_{k\neq k^*} \log T / (V \Delta_k))$，匹配下界。

## 核心创新

FEDFTRL 的核心创新在于解决了联邦赌博机中一个根本性的瓶颈：现有算法无法同时在随机环境和对抗环境下取得近乎最优的遗憾保证。该工作通过三个关键的设计变更实现了这一“两全其美”（BOBW）的目标。

**因果机制与核心洞察**：作者将分布式通信带来的信息不同步问题建模为**反馈延迟**，从而将联邦学习问题转化为带延迟的赌博机问题。基于这一视角，核心洞察是：通过**截断损失估计器**防止罕见臂的估计值爆炸，从而保持各智能体动作概率的近似一致；同时利用**混合正则化器**在随机与对抗环境下实现统一最优性。

**关键变更的槽位（Changed Slots）**：

1.  **损失估计器**：从标准的无偏估计器 $\hat{\ell}_{v,t}(k) = \ell_{v,t}(k_{v,t}) \mathbb{I}(k=k_{v,t}) / x_{v,t}(k)$ 改为**截断估计器** $\tilde{\ell}_{v,t}(k) = \ell_{v,t}(k_{v,t}) \mathbb{I}(k = k_{v,t}) / \max\{x_{v,t}(k), 12V C_t^P \gamma_t\}$。这是实现概率一致性的关键：当某个臂的动作概率 $x_{v,t}(k)$ 过低时，分母被截断，防止该臂的损失估计值无限膨胀，从而避免智能体之间因估计方差过大而偏离共识。

2.  **正则化器**：从单一正则化器（如 Tsallis-INF 或负熵）改为**混合正则化器** $F_t(x) = -2 \eta_t^{-1} (\sum_k \sqrt{x_k}) + \gamma_t^{-1} (\sum_k x_k (\log x_k - 1))$。该设计直接继承自单智能体 BOBW 算法（Zimmert & Seldin, 2020），其中平方根项（Tsallis-INF）负责在随机环境下实现对数级遗憾，负熵项负责在对抗环境下实现 $\sqrt{T}$ 级遗憾。在联邦场景下，两个学习率 $\eta_t$ 和 $\gamma_t$ 分别控制两类环境下的探索强度。

3.  **学习率调度**：从固定或简单衰减改为与网络拓扑参数 $C_t^P$ 耦合的复杂调度。$\eta_t^{-1} = 4\sqrt{Vt + 169 V^2 D}$ 和 $\gamma_t^{-1} = 8V \sqrt{C_t^P t / \log K + 36 D^2 (K-1)^{2/3} + 4 (C_t^P)^2}$。这里 $C_t^P = \frac{\min\{\log(Vt), \sqrt{V}\}}{1 - \sigma_2(P)} + 2 + D$ 量化了去中心化通信引起的延迟，其中 $\sigma_2(P)$ 是通信矩阵的第二大奇异值，$D$ 是网络直径。该设计使得算法能自适应网络拓扑的连通性。

4.  **通信方案**：从仅交换累积损失估计器改为交换**累积损失估计器加上偏差记录集 $A_v$**。这一变更源于截断估计器引入了有偏性，需要通过传播偏差记录来修正，确保全局一致性。

**证据强度**：论文声称 FEDFTRL 是“首个在联邦赌博机中实现 BOBW 遗憾保证的算法”（置信度 0.95）。在对抗环境下，个体遗憾界为 $O(\sqrt{KT/V} + \sqrt{C_T^P T \log K})$，显著优于先前工作 FEDEXP3 的 $O(T^{2/3})$（置信度 0.95）。在随机环境下，个体遗憾界为 $O(\sum_{k\neq k^*} \log T / (V \Delta_k))$，匹配下界（置信度 0.95）。实验在合成数据集和 MovieLens 数据集上验证了 FEDFTRL 优于所有基线（FEDEXP3, IND-FTRL, GOSSIP UCB, DRBB-bandit），且对拓扑参数 $C_t^P$ 的选择具有鲁棒性。

**失败模式与局限性**：该方法的假设限制了其适用范围：（1）要求存在唯一最优臂 $k^*$，未处理多最优臂场景；（2）通信图 $G$ 需为简单连通无向图，且通信矩阵 $P$ 需为双随机矩阵，这在动态或未知拓扑下不可用；（3）对抗环境下的遗憾界与下界之间仍存在差距（如 log 因子和网络拓扑依赖项），表明该方向的 BOBO 保证尚未达到信息论下界。

## 整体框架

FEDFTRL的整体框架围绕一个核心洞察构建：将联邦学习中的去中心化通信延迟建模为赌博机问题中的反馈延迟，从而将联邦赌博机问题转化为带延迟的赌博机问题。这一视角转换使得FEDFTRL能够利用FTRL（Follow-the-Regularized-Leader）框架和混合正则化器，同时处理随机环境和对抗环境。

**Pipeline与模块关系**：

1. **输入**：每个智能体 $v \in [V]$ 维护一个动作概率分布 $x_{v,t} \in \Delta([K])$，该分布由混合正则化器 $F_t(x) = -2 \eta_t^{-1} (\sum_k \sqrt{x_k}) + \gamma_t^{-1} (\sum_k x_k (\log x_k - 1))$ 生成。混合正则化器结合了Tsallis-INF正则化（平方根项）和负熵正则化，其核心作用是：在随机环境下，Tsallis-INF项提供对数级的遗憾保证；在对抗环境下，负熵项提供平方根级的遗憾保证。

2. **动作选择与损失估计**：每个智能体根据 $x_{v,t}$ 采样臂 $k_{v,t}$，观察损失 $\ell_{v,t}(k_{v,t})$。然后使用**截断损失估计器** $\tilde{\ell}_{v,t}(k) = \ell_{v,t}(k_{v,t}) \mathbb{I}(k = k_{v,t}) / \max\{x_{v,t}(k), 12V C_t^P \gamma_t\}$ 计算所有臂的估计损失。截断的关键作用是防止罕见臂的估计值爆炸——在没有截断的情况下，当 $x_{v,t}(k)$ 极小时，无偏估计器 $\hat{\ell}_{v,t}(k)$ 会变得极大，导致各智能体的概率分布严重偏离，破坏分布式一致性。

3. **通信与累积损失更新**：每个智能体维护累积损失估计器 $\hat{L}_{v,t}^{obs}$ 和偏差记录集 $A_v$。在每轮通信中，智能体与邻居交换 $\{\hat{L}_{v,t}^{obs}, A_v\}$，然后通过加权平均更新：$\hat{L}_{v,t+1}^{obs} = \sum_{u:(u,v)\in E} P_{u,v} \hat{L}_{u,t}^{obs} + V \tilde{\ell}_{v,t}$。这里 $P$ 是双随机通信矩阵，缩放因子 $V$ 确保累积损失与单个智能体的损失尺度一致。偏差记录集 $A_v$ 用于修正截断估计器引入的偏差，确保全局一致性——这是FEDFTRL相比现有联邦赌博机算法的关键创新之一。

4. **通信延迟参数**：$C_t^P = \frac{\min\{\log(Vt), \sqrt{V}\}}{1 - \sigma_2(P)} + 2 + D$ 量化了由去中心化通信引起的延迟，其中 $\sigma_2(P)$ 是通信矩阵的第二大奇异值，$D$ 是通信图的直径。该参数同时出现在截断阈值和学习率调度中，是连接网络拓扑与算法性能的关键桥梁。

5. **学习率调度**：两个学习率 $\eta_t$ 和 $\gamma_t$ 分别控制Tsallis-INF和负熵正则化的强度，其设置依赖于 $V, t, D, C_t^P, K$。具体地，$\eta_t^{-1} = 4\sqrt{Vt + 169 V^2 D}$，$\gamma_t^{-1} = 8V \sqrt{C_t^P t / \log K + 36 D^2 (K-1)^{2/3} + 4 (C_t^P)^2}$。这种调度确保了在两种环境下都能达到近乎最优的遗憾界。

**输出**：每个智能体 $v$ 的个体伪遗憾 $R_T(v) = \mathbb{E}[\sum_{t=1}^T \bar{\ell}_t(k_{v,t})] - \min_{k\in[K]} \mathbb{E}[\sum_{t=1}^T \bar{\ell}_t(k)]$，其中 $\bar{\ell}_t(k) = \frac{1}{V} \sum_{v=1}^V \ell_{v,t}(k)$ 是所有智能体的平均损失。在对抗环境下，遗憾界为 $O(\sqrt{KT/V} + \sqrt{C_T^P T \log K})$；在随机环境下，遗憾界为 $O(\sum_{k\neq k^*} \log T / (V \Delta_k))$，其中 $\Delta_k$ 是次优臂与最优臂的差距。

**模块间的因果机制**：截断损失估计器防止罕见臂的估计值爆炸 → 保持各智能体动作概率的近似一致（Lemma 1保证任意两智能体的概率比不超过3/2）→ 使得FTRL分析中的Bregman散度项可控 → 最终实现两种环境下的统一最优性。通信延迟参数 $C_t^P$ 则通过影响截断阈值和学习率，将网络拓扑的复杂性吸收到遗憾界中。

## 核心模块与公式推导

FEDFTRL 的核心设计围绕三个关键模块展开：**混合正则化器**、**截断损失估计器**以及**基于延迟反馈的通信建模**。这三者协同工作，将联邦多智能体问题转化为带延迟的赌博机问题，从而在随机和对抗环境下同时获得近乎最优的遗憾保证。

### 混合正则化器

FEDFTRL 使用的正则化器为：

$$F_t(x) = -2 \eta_t^{-1} \left( \sum_{k=1}^K \sqrt{x_k} \right) + \gamma_t^{-1} \left( \sum_{k=1}^K x_k (\log x_k - 1) \right)$$

- **变量含义**：$x$ 是臂上的概率分布（$K$ 维单纯形），$\eta_t$ 和 $\gamma_t$ 是时间相关的学习率，分别控制平方根项（Tsallis-INF 正则化）和负熵项（对数正则化）的强度。
- **设计动机**：Tsallis-INF 项（$-2\eta_t^{-1} \sum \sqrt{x_k}$）在对抗环境下提供 $O(\sqrt{T})$ 遗憾；负熵项（$\gamma_t^{-1} \sum x_k (\log x_k - 1)$）在随机环境下通过自界技术（self-bounding）提供对数遗憾。两者混合使得算法能在两种环境中自动适应，无需知晓环境类型。

### 截断损失估计器

标准无偏损失估计器为 $\hat{\ell}_{v,t}(k) = \ell_{v,t}(k_{v,t}) \mathbb{I}(k = k_{v,t}) / x_{v,t}(k)$，但在联邦设置中，由于通信延迟导致各智能体概率分布不一致，罕见臂的估计值可能爆炸。FEDFTRL 采用截断版本：

$$\tilde{\ell}_{v,t}(k) = \frac{\ell_{v,t}(k_{v,t}) \mathbb{I}(k = k_{v,t})}{\max\{x_{v,t}(k), 12V C_t^P \gamma_t\}}$$

- **变量含义**：$V$ 是智能体数量，$C_t^P$ 是通信延迟参数（见下文），$\gamma_t$ 是混合正则化器中负熵项的学习率。分母中的 $\max$ 操作确保当 $x_{v,t}(k)$ 过小时，估计值被截断在 $1/(12V C_t^P \gamma_t)$ 以下。
- **因果机制**：截断防止了因分布不一致导致的估计方差爆炸，从而维持各智能体动作概率的近似一致性（Lemma 1 证明任意两智能体对同一臂的概率比不超过 $3/2$）。这一一致性是后续遗憾分析的关键前提。

### 通信延迟参数

去中心化通信引入的延迟由以下参数量化：

$$C_t^P = \frac{\min\{\log(Vt), \sqrt{V}\}}{1 - \sigma_2(P)} + 2 + D$$

- **变量含义**：$P$ 是通信图 $G$ 上的双随机矩阵，$\sigma_2(P)$ 是其第二大奇异值（控制信息混合速度），$D$ 是图直径。$1/(1 - \sigma_2(P))$ 项刻画了 gossip 协议下信息传播的混合时间。
- **物理意义**：$C_t^P$ 衡量了智能体本地累积损失估计 $\hat{L}_{v,t}^{obs}$ 与全局平均 $\bar{L}_t$ 之间的最大偏差。Lemma 2 证明 $\|\hat{L}_{v,t}^{obs} - \bar{L}_t\|_\infty \leq 1/(12 \gamma_t)$，这一界保证了概率一致性。

### 累积损失更新与学习率调度

累积损失估计器的更新规则为：

$$\hat{L}_{v,t+1}^{obs} = \sum_{u:(u,v)\in E} P_{u,v} \hat{L}_{u,t}^{obs} + V \tilde{\ell}_{v,t}$$

- **变量含义**：$P_{u,v}$ 是双随机通信矩阵的元素，$\tilde{\ell}_{v,t}$ 是截断损失估计器。第一项是邻居加权平均（实现共识），第二项是缩放后的本地观测（缩放因子 $V$ 用于对齐全局平均损失的定义）。

学习率调度设计为：

$$\eta_t^{-1} = 4\sqrt{Vt + 169 V^2 D}, \quad \gamma_t^{-1} = 8V \sqrt{\frac{C_t^P t}{\log K} + 36 D^2 (K-1)^{2/3} + 4 (C_t^P)^2}$$

- **设计逻辑**：$\eta_t^{-1}$ 的 $O(\sqrt{Vt})$ 项主导对抗遗憾中的 $\sqrt{KT/V}$ 项；$\gamma_t^{-1}$ 的 $O(V\sqrt{C_t^P t / \log K})$ 项主导对抗遗憾中的 $\sqrt{C_T^P T \log K}$ 项，而常数项 $D^2(K-1)^{2/3}$ 和 $(C_t^P)^2$ 处理边界效应和网络拓扑依赖。

### 遗憾界公式

FEDFTRL 在两种环境下的个体遗憾界（Theorem 1）为：

**对抗环境**：
$$R_T(v) \leq 13\sqrt{KT/V} + 13\sqrt{C_T^P T \log K} + 156\sqrt{D} + 72 D (K-1)^{1/3} \log K + 24 C_T^P \log K$$

**随机环境**：
$$R_T(v) \leq \sum_{k\neq k^*} \frac{51\log T}{V\Delta_k} + \sum_{k\neq k^*} \frac{90 C_T^P}{\Delta_k \log K} + 56 D \sqrt{(K-1)\log K} + 11 C_T^P \log K + 2D$$

- **变量含义**：$K$ 是臂数，$T$ 是时间步，$\Delta_k$ 是臂 $k$ 与最优臂 $k^*$ 之间的平均损失差（随机环境）。第一项 $\sqrt{KT/V}$ 和 $\log T / (V\Delta_k)$ 分别匹配单智能体 FTRL 在对抗和随机环境下的最优率，但除以 $V$ 体现了联邦协作的加速效果。第二项 $\sqrt{C_T^P T \log K}$ 和 $C_T^P / (\Delta_k \log K)$ 是通信延迟的代价，其中 $C_T^P$ 包含网络拓扑依赖。常数项（如 $156\sqrt{D}$、$72 D (K-1)^{1/3} \log K$）来自截断估计器和边界处理，在 $T$ 主导时渐近可忽略。

**证据强度说明**：上述公式均直接取自论文第 4 节和 Theorem 1，置信度 1.0。学习率调度的具体数值（如 $169 V^2 D$ 中的常数 169）来自附录中 Lemma 1-8 的推导，但此处仅展示其结构形式，不推断未给出的推导细节。

## 实验与分析

![[assets/figures/papers/iclr26_0003_Lkndkxeemx_A_Near-Optimal_Best-of-Both-Worlds_Algorithm_for/figures/001_Table_1.jpg]]
*Table 1: Overview of best-known regret bounds for federated bandits. Here, P denotes the doubly stochastic communication matrix over the network G , and $\sigma _ { 2 }$ ( P ) is its second-largest singular value. We define $\begin{array} { r } { C _ { T } ^ { P } : = \frac { \operatorname* { m i n } \{ \log ( V T ) , \sqrt { V } \} } { 1 - \sigma _ { 2 } ( P ) } + 2 + D } \end{array}$ , where D is the diameter of G , capturing the dependence on the network topology. Let M denote the Laplacian matrix of G ; $\lambda _ { 2 }$ ( M ) is its second-smallest eigenvalue, and $d _ { \mathrm { m a x } }$ is the maximum node degree in G

**主要结果：遗憾界的理论保证与实验验证**

FEDFTRL是首个在联邦赌博机中实现“两全其美”（BOBW）遗憾保证的算法。其核心理论贡献体现在两个互补的遗憾界上：

*   **对抗环境**：个体遗憾界为 $R_T(v) \leq 13\sqrt{KT/V} + 13\sqrt{C_T^P T \log K} + 156\sqrt{D} + 72 D (K-1)^{1/3} \log K + 24 C_T^P \log K$。其中，主导项 $O(\sqrt{KT/V} + \sqrt{C_T^P T \log K})$ 显著优于先前联邦对抗算法FEDEXP3的 $O(T^{2/3})$ 界。
*   **随机环境**：个体遗憾界为 $R_T(v) \leq \sum_{k\neq k^*} \frac{51\log T}{V\Delta_k} + \sum_{k\neq k^*} \frac{90 C_T^P}{\Delta_k \log K} + 56 D \sqrt{(K-1)\log K} + 11 C_T^P \log K + 2D$。其主导项 $O(\sum_{k\neq k^*} \log T / (V \Delta_k))$ 匹配了该设置下的信息论下界。

实验在合成数据集和MovieLens真实数据集上进行，覆盖了三种通信网络拓扑：完全图、网格图和随机几何图（RGG-0.5）。在两种数据集和所有拓扑下，FEDFTRL的平均累积遗憾均优于所有基线（FEDEXP3, IND-FTRL, GOSSIP UCB, DRBB-bandit）。这一结果验证了理论界，并表明算法对网络结构具有泛化能力。

**消融实验：对拓扑参数的鲁棒性**

敏感性分析（Figure 3和Figure 4）通过将算法中的拓扑参数 $C_t^P$ 乘以不同的缩放因子（0.1, 0.5, 1.0, 5.0, 10.0）来测试其鲁棒性。实验结果显示，在合成数据和MovieLens数据上，所有缩放因子的平均累积遗憾曲线高度接近，表明FEDFTRL对 $C_t^P$ 的精确取值不敏感。这降低了算法在实际部署中的调参成本，因为 $C_t^P$ 本身依赖于网络拓扑的谱性质（$1-\sigma_2(P)$）和直径 $D$，而这些参数在实践中难以精确估计。

**核心机制分析：截断估计器与混合正则化器的作用**

FEDFTRL成功的因果机制在于两个关键设计：

1.  **截断损失估计器**：$\tilde{\ell}_{v,t}(k) = \frac{\ell_{v,t}(k_{v,t}) \mathbb{I}(k = k_{v,t})}{\max\{x_{v,t}(k), 12V C_t^P \gamma_t\}}$。该估计器通过分母截断，防止了未被选中的“罕见臂”的估计损失值爆炸。这保持了各智能体动作概率 $x_{v,t}$ 的近似一致性（Lemma 1保证任意两智能体概率比不超过3/2），从而使得分布式通信带来的延迟可以被建模为可控的反馈延迟。
2.  **混合正则化器**：$F_t(x) = -2 \eta_t^{-1} (\sum_k \sqrt{x_k}) + \gamma_t^{-1} (\sum_k x_k (\log x_k - 1))$。该正则化器结合了Tsallis-INF（平方根项）和负熵项，分别用于在对抗和随机环境下实现最优的遗憾结构。通过动态调整两个学习率 $\eta_t, \gamma_t$，算法能够在两种环境之间自动适应。

**失败模式与开放性局限**

尽管取得了显著进展，FEDFTRL仍存在明确的理论与实践局限：

*   **理论差距**：对抗环境下的遗憾上界与已知下界之间仍存在差距，主要体现在对数因子和网络拓扑依赖项 $C_T^P$ 上。论文指出缩小这一差距是未来方向。
*   **假设限制**：算法假设存在唯一最优臂 $k^*$，且通信图 $G$ 为简单连通无向图，通信矩阵 $P$ 需为双随机矩阵。这些假设在真实动态网络中可能不成立。
*   **实验范围**：验证仅在合成数据和MovieLens上进行，未涉及更复杂的真实场景（如上下文赌博机或线性赌博机），其BOBW保证能否扩展到这些设置尚属开放问题。

**结论**：FEDFTRL通过截断估计器和混合正则化器，成功将联邦学习中的通信延迟转化为可处理的反馈延迟，首次在联邦赌博机中实现了理论与实验上的“两全其美”保证。其近乎最优的遗憾界和鲁棒的实验表现确立了新的基线，但理论差距和假设限制指明了未来工作的关键方向。

## 方法谱系与知识库定位

### 与基线方法的关系

FEDFTRL的核心贡献在于首次在联邦赌博机（federated bandits）设定中实现了“两全其美”（Best-of-Both-Worlds, BOBW）的遗憾保证，即算法在随机环境和对抗环境下均能达到近乎最优的遗憾界。在此之前，现有联邦赌博机算法存在根本性的能力分裂：

- **对抗环境算法**：以FEDEXP3为代表，其个体遗憾界为$O(T^{2/3})$，远未达到最优的$O(\sqrt{T})$量级。
- **随机环境算法**：如GOSSIP UCB和DRBB-bandit，仅针对随机环境设计，在对抗环境下性能崩溃。
- **独立基线**：IND-FTRL（每个智能体独立运行FTRL，无通信协作）作为消融基线，用于量化通信带来的增益。

FEDFTRL通过三项关键设计突破这一分裂：**混合正则化器**（hybrid regularizer）结合了Tsallis-INF和负熵正则化，**截断损失估计器**（truncated loss estimator）防止罕见臂的估计值爆炸，以及将**分布式通信延迟建模为反馈延迟**，从而将联邦学习问题转化为带延迟的赌博机问题。这些设计共同使得FEDFTRL在对抗环境下达到$O(\sqrt{KT/V} + \sqrt{C_T^P T \log K})$的个体遗憾界（较FEDEXP3的$O(T^{2/3})$有本质提升），在随机环境下达到$O(\sum_{k\neq k^*} \log T / (V \Delta_k))$，匹配已知下界。

### 适用边界

FEDFTRL的有效性依赖于一组明确的假设条件：

1. **网络拓扑**：通信图$G$需为简单连通无向图，且通信矩阵$P$为双随机矩阵（doubly stochastic matrix）。算法性能通过参数$C_t^P = \frac{\min\{\log(Vt), \sqrt{V}\}}{1 - \sigma_2(P)} + 2 + D$量化网络拓扑的影响，其中$\sigma_2(P)$是$P$的第二大奇异值，$D$是图的直径。敏感性分析（Figure 3和Figure 4）表明算法对$C_t^P$的选择具有鲁棒性，但该参数本身对网络结构敏感。
2. **环境假设**：在随机环境下，要求存在唯一最优臂$k^*$，未覆盖多最优臂场景。对抗环境下的遗憾界虽为$O(\sqrt{T})$，但与下界之间仍存在$\log$因子和网络拓扑依赖项的差距（如$156\sqrt{D} + 72 D (K-1)^{1/3} \log K + 24 C_T^P \log K$等附加项）。
3. **通信成本**：每轮期望通信成本为$O(K)$，与智能体数量$V$无关，但通信内容需交换累积损失估计器和偏差记录集$A_v$，增加了单次通信的负载。

### 局限与开放问题

**已知局限**：
- 唯一最优臂假设限制了在非平稳或存在多个等效最优臂场景下的应用。
- 对抗遗憾上界与下界之间的差距尚未完全闭合，主要体现在$\log$因子和网络拓扑依赖项（如$D$和$C_T^P$）上。
- 实验仅在合成数据和MovieLens数据集上进行，未在更多真实场景（如推荐系统、医疗等）中验证泛化能力。

**开放问题**：
- 如何将FEDFTRL推广到存在多个最优臂的场景？这可能需要重新设计正则化器或分析框架。
- 如何处理时变或未知的网络拓扑？当前算法假设拓扑静态且已知，实际联邦学习场景中节点可能动态加入或退出。
- 能否将BOBW保证扩展到更复杂的设定，如线性赌博机（linear bandits）或上下文赌博机（contextual bandits）？这需要解决高维动作空间下的通信与估计问题。
- 如何进一步缩小对抗环境下遗憾上界与下界之间的差距？当前分析中的常数项和$\log$因子可能通过更精细的证明技术（如改进的Bregman散度分析）得到优化。

**需手动验证的点**：FEDFTRL在对抗环境下的遗憾界与下界之间的具体差距量级（如$\log K$因子的指数）需要查阅最新的信息论下界结果进行确认，本文未提供明确的下界表达式。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Near_Optimal_Best_of_Both_Worlds_Algorithm_for_Federated_Bandits.pdf

![[paperPDFs/ICLR_2026/A_Near_Optimal_Best_of_Both_Worlds_Algorithm_for_Federated_Bandits.pdf]]
