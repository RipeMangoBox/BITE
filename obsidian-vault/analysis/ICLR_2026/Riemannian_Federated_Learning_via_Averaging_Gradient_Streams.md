---
title: "Riemannian Federated Learning via Averaging Gradient Streams"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Riemannian_Federated_Learning_via_Averaging_Gradient_Streams.pdf
project_link: null
code_link: null
aliases:
- RFLAGS
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/large_scale_parallel_and_distributed
core_operator: "采用平均梯度流(AGS)的服务器聚合取代局部参数平均，通过向量传输将所有局部梯度映射到全局切空间进行线性平均，保留了线性分析特性；同时引入逆概率加权和基于频率的概率估计，纠正了随机部分参与的偏差。"
primary_logic: "通过向量传输将各Agent的随机梯度“流”回溯到全局切空间，平均后再回缩(Retraction)，避免了非线性聚集的复杂度；同时用估计的参与概率加权聚合保证期望无偏，从而在黎曼流形上实现对非IID和部分参与的联合处理。"
claims:
- "RFedAGS在PCA、HSP、FMC等多个任务的实验中一致优于现有的黎曼联邦学习算法。"
- "Theorem 2.1证明简单平均会收敛到错误目标，而AGS-AP保证聚合梯度的期望无偏，解决了部分参与下的目标偏差。"
- "在部分参与和非IID设置下，固定步长时算法拥有次线性/线性收敛速率(Theorem 3.4, 3.5)，为方法提供了坚实的理论保证。"
- "Theorem 3.6证明了用历史参与频率估计真实概率的高概率保证，使得无需预知概率即可实现收敛。"
---

# Riemannian Federated Learning via Averaging Gradient Streams

> [!tip] 核心洞察
> 通过向量传输将各Agent的随机梯度“流”回溯到全局切空间，平均后再回缩(Retraction)，避免了非线性聚集的复杂度；同时用估计的参与概率加权聚合保证期望无偏，从而在黎曼流形上实现对非IID和部分参与的联合处理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过平均梯度流进行黎曼联邦学习 |
| 英文题名 | Riemannian Federated Learning via Averaging Gradient Streams |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=oEtrDiFOFF) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/large_scale_parallel_and_distributed |
| Method | RFedAGS |
| Dataset | PCA (synthetic & CIFAR10), HSP (WordNet), FMC (PATHMNIST), LRMC (MovieLens 1M) |

> [!tip] 效果简介
> - PCA (synthetic & CIFAR10) 上，最优化间隙 (optimality gap) 为 RFedAGS，对比 RFedAvg, RFedSVRG, RFedProj，变化 RFedAGS收敛更快且达到更低的间隙。
> - HSP (WordNet) 上，到真实点的距离 为 RFedAGS，对比 RFedAvg, RFedSVRG，变化 RFedAGS距离更小，预测更准。
> - FMC (PATHMNIST) 上，黎曼距离 为 RFedAGS，对比 RFedAvg, RFedSVRG，变化 RFedAGS距离更小，均值估计更优。

## 概要

现有黎曼联邦学习方法（如RFedAvg、RFedSVRG、RFedProj）普遍依赖指数映射（exponential map）与并行传输（parallel transport）来实现服务器端的局部参数平均，但这些算子对许多黎曼流形缺乏闭式解，计算成本高昂。更关键的是，它们难以同时应对**客户端部分参与**与**非独立同分布（non-IID）数据**两个现实挑战，限制了在一般黎曼流形上的应用。本文从服务器聚合（server aggregation, SA）的核心瓶颈出发，提出**RFedAGS（Riemannian Federated Averaging Gradient Streams）**：利用向量传输（vector transport）将各客户端在局部更新过程中累积的随机梯度“流”映射至全局切空间，通过线性平均形成聚合方向，再利用回缩（retraction）更新全局模型。这一设计避免了非线性参数平均的复杂性，同时保留了欧氏空间中联邦平均（FedAvg）的线性分析特性。

针对部分参与导致的聚合梯度有偏问题，RFedAGS引入**逆概率加权聚合策略（AGS-AP）**：若真实参与概率已知，则以概率倒数加权可保证聚合梯度的期望无偏（Theorem 2.1）；当概率未知时，算法利用历史参与频率自适应估计各客户端的参与概率，并在理论上证明了该估计的高概率收敛性（Theorem 3.6）。相较已有方法，RFedAGS使用一般回缩和有界向量传输，降低了流形算子的假设强度，适用范围更广（Table 1）。

理论分析表明，在non‑IID与任意部分参与的设定下，RFedAGS在固定步长时拥有**次线性收敛速率**（非凸目标，Theorem 3.4），在满足黎曼PL条件时能够达到**线性收敛**（Theorem 3.5），收敛速度对数据异质性与参与概率估计误差具有显式的依赖刻画。实验覆盖主成分分析（PCA）、双曲空间嵌入预测（HSP）、黎曼流形均值估计（FMC）以及低秩矩阵补全（LRMC）等任务，RFedAGS在最优性间隙、黎曼距离和RMSE等指标上一致优于现有黎曼联邦学习基线（Figure 2–4, Table 3），且在消融研究中验证了加权聚合、频率估计概率和算法可扩展性等组件的有效性。

综上，RFedAGS通过将服务器聚合抽象为平均梯度流，实现了对非IID数据和部分参与的联合处理，为在一般黎曼流形上的联邦学习提供了一个高效且有理论保证的框架。



联邦学习在欧氏空间中的成功催生了将客户端数据约束在黎曼流形上的需求。当本地数据的生成模型自然存在于非欧几何结构——如正交性约束（Stiefel流形）、低秩矩阵（Grassmann流形）、双曲嵌入（Hyperboloid流形）或对称正定矩阵（SPD流形）——时，直接在黎曼流形上执行联邦优化能更好地保留数据的内在结构。形式上，包含$N$个客户端的黎曼联邦学习问题寻求全局解
$$
\operatorname*{arg\,min}_{x\in\mathcal{M}} F(x):=\frac{1}{N}\sum_{i=1}^{N} f_i(x),\quad f_i(x)=\mathbb{E}_{\xi\sim\mathcal{D}_i}[f_i(x;\xi)],
$$
其中$\mathcal{M}$为目标黎曼流形，$\mathcal{D}_i$为客户端$i$的局部数据分布。

最早的黎曼联邦算法（如RFedAvg和RFedSVRG）借鉴了欧氏联邦平均的范式：服务器在切空间中对局部模型参数进行平均（切线均值，TM），再利用指数映射$\operatorname{Exp}$将平均结果投影回流形。这一设计存在两个核心瓶颈。**其一，算子依赖性过强。** 指数映射、其逆以及并行传输在许多重要流形上缺乏闭式表达式，导致每次迭代的计算开销极高；实际实现中通常被迫使用牛顿迭代或截断展开来近似这些算子，进一步削弱了收敛结论的严密性（Table 1及Table 2给出了算子复杂度的对比）。**其二，对部分参与和数据异质性的支持严重不足。** 现有方法或假设全部客户端参与通信轮，或在随机均匀采样下直接进行等权平均，忽视客户端因网络延迟、电量差异等原因导致的异构参与概率。当部分客户端以不同概率随机参与，且本地数据呈non‑IID时，简单平均会收敛到一个重加权目标$\tilde{F}(x)$而非原始目标$F(x)$（Theorem 2.1, Equation (2.1)），从而产生不可忽略的目标偏移。RFedProj等基于投影算子的方案虽声称支持一般流形，但受限于紧致子流形，同样未提供部分参与下的收敛保证（Table 1）。

上述缺口的根本原因在于，**现有聚合策略在非线性流形上直接操作局部参数，丧失了欧氏平均的线性可加性**，致使引入参与概率校正的难度急剧上升。因此，亟需一种既避免昂贵指数映射、又能以线性方式融合梯度信息，同时可自然地纳入部分参与偏差校正的黎曼联邦学习范式。

本文的动机正是弥合这一空缺。我们提出**基于平均梯度流（Averaging Gradient Streams）的黎曼联邦学习算法RFedAGS**。其核心思路是：**不平均局部参数，而是将各客户端多步局部更新的梯度信息通过有界向量传输$\mathcal{T}$流回全局参数的切空间，在该线性空间内完成加权平均，最后仅需一次一般回缩$\mathsf{R}$便可将搜索点重新拉回流形**。该设计完全避开了指数映射及其逆，大幅降低了算子可用性假设。更重要的是，梯度流的线性聚合天然兼容逆概率加权：服务器利用历史参与频率估计每个客户端$i$的参与概率$q_t^i$，并以$\frac{1}{q_t^i N}$的权重对梯度进行重加权，使得聚合梯度的期望严格无偏于全局梯度（Theorem 2.1, Algorithm 1 Line 13‑14）。由此，RFedAGS能够在**非IID数据**和**任意部分参与**的联合设置下同时获得理论收敛保证（Theorem 3.4, 3.5, 3.6）与实验上的显著性能优势（Figure 2‑4, Table 3）。这一范式为将联邦学习扩展到更一般的流形和更实际的跨设备场景提供了系统性的解决方案。



## 核心方法与创新机理

该工作的核心瓶颈在于：现有黎曼联邦学习方法（如 RFedAvg、RFedSVRG、RFedProj）普遍依赖**指数映射与并行传输**进行服务器聚合，而许多流形上这些算子缺乏闭式表达，导致计算负担沉重；更重要的是，这些方法**无法同时处理客户端部分参与与非独立同分布数据**，限制了实际部署。RFedAGS 通过三个关键“插槽”的改动系统性地解决了上述问题，形成了如下创新轴心。

### 1. 服务器聚合方式：从参数平均到平均梯度流
**Baseline 做法**：RFedAvg、RFedSVRG 等采用**切线均值（TM）**，即服务器收集各客户端的局部参数，通过指数映射的逆将其映射到切空间平均，再经指数映射回展到流形。该过程是非线性的，且在多步局部更新下会放大漂移，尤其当数据分布差异大时，平均后的参数可能远离全局最优点（见 Figure 1 几何解释）。

**RFedAGS 做法**：服务器通过**平均梯度流（AGS）** 进行聚合。具体地，客户端在本地执行 SGD 时，每一步的随机梯度经由**向量传输**（`T`）累积到同一切方向，形成“梯度流”`ζ_{t,K}^i`；服务器仅需对这些梯度流加权平均，再用**一般回缩**（`R`）更新全局模型：
- **AGS‑RS（普通版本）**：`x_{t+1} = R_{x_t} (-(1/|S_t|) Σ_{j∈S_t} ζ_{t,K}^j)`
- **AGS‑AP（概率加权版本）**：`x_{t+1} = R_{x_t} (-ϖ Σ_{i∈S_t} (1/(p_i N)) ζ_{t,K}^i)`

**创新机制**：AGS 用**向量传输将局部的梯度信息拉回全局切空间**，再执行线性平均和回缩，避免了参数平均带来的非线性扭曲。该设计天然保留了线性分析特性，且对所用流形仅要求**一般回缩**与**有界向量传输**，摆脱了对指数映射的依赖（Table 1）。同时，它让局部更新步数 `K` 能直接转化为通信间隙的缩减，提升了收敛对局部计算量的利用效率（Figure 13）。

### 2. 部分参与处理：从等权平均到逆概率加权与可学习概率估计
**Baseline 做法**：现有方法对“部分参与”或无处理，或仅做等权重聚合（`1/|S_t|`），这在各客户端参与概率 `p_i` 不同的情况下会引入系统性偏差，使算法收敛到**错误的加权目标**（Theorem 2.1 证明，简单平均会收敛到 `arg min_x \tilde{F}(x) ≠ F(x)`）。

**RFedAGS 做法**：通过**逆概率加权**（AGS‑AP）实现期望无偏聚合。当真实参与概率 `p_i` 已知时，服务器用 `1/(p_i N)` 加权各客户端的梯度流，其期望严格等于全局梯度 `grad F(x)`（(AGS‑AP) 公式）。当 `p_i` 未知时，服务器利用**历史参与频率**估计 `q_t^i`，并用其取代 `p_i`：
- `q_t^i = (∑_{τ=1}^{t-1} 𝟙_{S_τ}(i)) / (t-1)`

**创新机制**：
- **理论保证**：即使使用估计的概率，仍能通过高概率界（Theorem 3.6）证明估计误差 `|1/q_t^i - 1/p_i| ≤ O(t^{-a/2})` 以高概率成立，从而维持收敛性。
- **实验验证**：使用频率估计的效果与使用真实概率几乎一致（Figure 8, Figure 9），且明显优于忽略概率差异的 AGS‑RS（Figure 6, Figure 7）。
- 这一设计首次在黎曼联邦学习中同时解决了**非独立同分布数据**和**任意部分参与**下的目标一致性难题。

### 3. 流形算子的泛化与收敛理论革新
**Baseline 做法**：依赖指数映射、并行传输等强算子，收敛分析受限于特定流形结构。

**RFedAGS 做法**：将分析框架建立在**一般回缩（Retraction）** 和**有界向量传输**之上（Assumption 3.1、3.5），仅需回缩满足 `L_g`-光滑性、向量传输满足范数有界性，而**不要求流形紧致或可逆指数映射**。这使算法适用于更广泛的黎曼流形。

在收敛性上，作者给出了**非凸/强凸**两种约定下**固定步长**或**衰减步长**的次线性/线性收敛速率：
- 非凸固定步长：`(1/T) Σ 𝔼[‖grad F(x_t)‖^2] ≤ O(1/(αKT) + α Q(K,B,α,ϖ))` (Theorem 3.4)
- 强凸（RPL条件）：`𝔼[F(x_T)] - F(x^*) ≤ (1-μϖKα)^{T-1} Θ(x₁) + (α/μ) Q(...)`，即**线性收敛**到包含数据异质、部分参与噪声的邻域 (Theorem 3.5)。

**误差项 `Q(·)`** 综合刻画了客户端漂移、概率估计误差、梯度噪声等各因素的耦合作用（Lemma D.5），为算法设计提供了清晰的消融线索。

综上，RFedAGS 的创新本质是**用“梯度流聚合”取代“参数平均”**，通过**向量传输将局部分布式梯度映射到同一切空间线性平均**，再以**回缩保证流形约束**；同时**引入可学习的参与概率逆加权**，使聚合在部分参与下保持无偏。这三个插槽的联动，使得该方法成为**首个在不依赖指数映射的前提下，兼顾非独立同分布数据与任意部分参与的黎曼联邦学习算法**，并获得了覆盖多种设定下的收敛保证。



![[assets/figures/papers/iclr26_0015_oEtrDiFOFF_Riemannian_Federated_Learning_via_Averaging_Grad/figures/001_Table_1.jpg]]
*Table 1: Summary of existing algorithms and the proposed RFedAGS*

![[assets/figures/papers/iclr26_0015_oEtrDiFOFF_Riemannian_Federated_Learning_via_Averaging_Grad/figures/005_Figure_1.jpg]]
*Figure 1: (a)-(b) diagrams of (TM) and (AGS-RS) where K = 2 , , two agent participate in communication, and $g _ { i }$ ( x ) denotes the local stochastic gradient of agent i at x. (c) (AGS) v.s. (TM) on $\begin{array} { r } { \operatorname* { m i n } _ { x \in \{ x \in \mathbb { R } ^ { 5 0 } : x ^ { T } x = 1 \} } F ( x ) = - { \frac { 1 } { 2 } } ( { \frac { 1 } { 6 0 } } \sum _ { j = 1 } ^ { 6 0 } ( x ^ { T } Z _ { 1 , j } Z _ { 1 , j } ^ { T } x + x ^ { T } Z _ { 2 , j } Z _ { 2 , j } ^ { T } x ) ) } \end{array}$

RFedAGS 的整体设计遵循“服务器广播全局模型—客户端局部更新并累积梯度流—服务器加权聚合”的循环流水线，其关键创新在于用**平均梯度流（Averaging Gradient Streams, AGS）**的线性操作取代传统基于指数映射和切空间平均的非线性参数聚合，并通过**逆概率加权**校正随机部分参与的偏差，从而在一般黎曼流形上联合处理非独立同分布数据与任意参与模式。整个框架由五个主要模块串联构成，输入为初始全局模型 $x_1 \in \mathcal{M}$ 和各客户端本地数据分布，输出为逐轮更新后的全局模型 $x_t$。

### 1. 全局模型广播
每一通信轮次 $t$ 开始时，服务器将当前全局参数 $x_t \in \mathcal{M}$ 发送给被选中的参与子集 $\mathcal{S}_t$（Algorithm 1 第 2 行）。广播操作本身不涉及流形运算，仅传递参数向量，从而通信代价与欧氏空间联邦学习相当。

### 2. 局部随机梯度更新与梯度流累积
每个选中的客户端 $i \in \mathcal{S}_t$ 收到 $x_t$ 后，在流形上执行 $K$ 步局部随机梯度下降（Algorithm 1 第 6–8 行）。具体而言，第 $k$ 步先计算局部随机梯度 $g_{t,k}^i$，然后通过**一般回缩算子**$\mathrm{R}$ 更新参数：
$$x_{t,k+1}^i = \mathrm{R}_{x_{t,k}^i}(-\alpha_t\, g_{t,k}^i),$$
保证更新后参数仍位于流形上。与此同时，客户端利用**有界向量传输**$\mathcal{T}$ 将每一步的梯度传输到初始点 $x_t$ 的切空间 $\mathrm{T}_{x_t}\mathcal{M}$ 并累加，形成“**梯度流**”（gradient stream）：
$$\zeta_{t,K}^i = \sum_{k=1}^{K} \mathcal{T}_{x_{t,k}^i \to x_t}(g_{t,k}^i).$$
该累积操作将局部多步更新转化为切空间中的一个单一方向，使得后续服务器端的线性平均成为可能，且避免了在服务器端进行昂贵且非线性的并行传输与指数映射（Algorithm 1 第 9 行）。

### 3. 参与概率估计
为补偿不同客户端因非均匀采样带来的聚合偏差，服务器需获取每个客户端的参与概率。若真实概率 $p_i$ 未知，则服务器利用历史轮次中的参与记录进行在线估计（Algorithm 1 第 13 行）：
$$\mathfrak{q}_t^i = \sum_{\tau=1}^{t-1} \mathbb{I}_{\mathcal{S}_\tau}(i), \qquad q_t^i = \frac{\mathfrak{q}_t^i}{t-1},$$
用频率 $q_t^i$ 近似真实 $p_i$。理论分析表明，该近似误差以高概率随时间衰减（Theorem 3.6），为算法在未知环境下的收敛提供了保障。

### 4. 加权服务器聚合与全局模型更新
服务器收集到本轮所有参与客户端的梯度流 $\zeta_{t,K}^i$ 后，采用**逆概率加权**方式聚合，再用回缩算子更新全局模型：
$$x_{t+1} = \mathrm{R}_{x_t}\!\left(-\varpi \sum_{i \in \mathcal{S}_t} \frac{1}{\hat{q}_t^i N}\, \zeta_{t,K}^i\right),$$
其中 $\hat{q}_t^i$ 在实际运行中可以是真实概率 $p_i$ 或估计值 $q_t^i$（Algorithm 1 第 14 行，对应模式 AGS‑AP）。期望意义下，该聚合等价于全部 $N$ 个客户端梯度流的无偏平均，确保算法始终解决原始的全局优化问题 $\min_{x\in\mathcal{M}} F(x)$，而不像简单平均（AGS‑RS）那样收敛到一个错误的重加权目标（Theorem 2.1）。

上述聚合过程全程只涉及**切空间内的线性平均与一次回缩**，没有空间交错的非线性操作，因此复杂度与欧氏 FedAvg 处于同一量级（Table 2）。同时，算法对流形的要求仅为配备**一般回缩**和**有界向量传输**（Table 1），可以涵盖球面、Grassmann 流形、双曲空间等常见黎曼流形，避免了对指数映射及其逆的依赖。

### 5. 模块间的输入输出流
综合而言，RFedAGS 的一条完整数据流可以概括为：
- **服务器**：维护 $x_t \in \mathcal{M}$，每轮输出全局参数广播给若干客户端；接收各客户端的梯度流 $\zeta_{t,K}^i$ 与概率估计 $q_t^i$；输出更新后的 $x_{t+1}$。
- **客户端**：接收全局模型，本地执行 $K$ 步 SGD 并生成梯度流，再将其与当前概率估计（若需由客户端发送参与标识）一并上传。
- **核心优势**：该流水线通过“切空间线性聚合 + 逆概率加权”解耦了流形非线性和参与偏差，使得在非独立同分布数据和任意部分参与下，算法仍具备次线性/线性收敛速率（Theorem 3.4, 3.5），同时在 PCA、HSP、FMC 等多个任务上一致优于现有黎曼联邦学习基线（Figure 2–4）。



现有黎曼联邦学习方法（RFedAvg、RFedSVRG等）普遍依赖指数映射与并行传输实现模型参数平均，不仅面临许多流形上无闭式解的计算负担，且无法同时应对 **部分参与** 与 **非IID数据** 的双重挑战。RFedAGS 通过两个关键设计打破上述瓶颈：(1) 用**向量传输的平均梯度流**取代局部参数平均，保留切空间内的线性结构；(2) 引入**逆概率加权**与**基于历史频率的概率估计**，在期望层面消除部分参与引入的目标偏移。以下按模块拆解核心公式与其作用。

### 全局目标与切空间线性化
黎曼联邦学习旨在求解流形 $\mathcal{M}$ 上的分布式优化问题
$$\underset{x\in\mathcal{M}}{\arg\min}\; F(x):=\frac{1}{N}\sum_{i=1}^N f_i(x),\quad f_i(x)=\mathbb{E}_{\xi\sim\mathcal{D}_i}[f_i(x;\xi)] \tag{1.1}$$
其中 $f_i$ 为 Agent $i$ 的局部期望损失，$N$ 为总 Agent 数。RFedAGS 不直接平均局部模型（非线性聚集），而是将各 Agent 的**局部随机梯度序列**通过向量传输 $\mathrm{T}$ 回溯至全局参数的同一切空间，再在该线性空间中完成聚合与回缩 $\mathrm{R}$，从而保持操作的可线性化。

### 局部梯度流构建
每一轮 $t$，被选中的 Agent $i$ 收到全局模型 $x_t$，执行 $K$ 步局部 SGD：
1. **回缩保持流形**：每一步用回缩 $\mathrm{R}$ 确保更新后的参数仍在流形上。
2. **向量传输累积**：每一步的随机梯度通过有界向量传输 $\mathrm{T}$ 映射到当前点的切空间，并累加为 **梯度流** 向量 $\zeta_{t,K}^i$（见 Algorithm 1 第9行）。该步骤的实质是将 $K$ 步局部更新的总「推动量」压缩为切空间中的一个方向，避免了直接同步高维模型参数。

梯度流的构造使得服务器端可以像处理欧氏梯度一样进行加权平均，而不涉及非线性流形运算。

### 服务器聚合：AGS‑RS 与 AGS‑AP
服务器使用回缩 $\mathrm{R}$ 将聚合方向拉回流形，形成两种聚合模式：
- **简单平均（AGS‑RS）**：  
  $$x_{t+1} = \mathrm{R}_{x_t}\!\left( - \frac{1}{|S_t|} \sum_{j\in S_t} \zeta_{t,K}^j \right) \tag{AGS‑RS}$$
- **逆概率加权（AGS‑AP）**：  
  $$x_{t+1} \gets \mathsf{R}_{x_t}\!\left( -\varpi \sum_{i\in S_t} \frac{1}{p_i N} \zeta_{t,K}^i \right) \tag{AGS‑AP}$$

其中：$S_t$ 为当前参与 Agent 集合，$p_i$ 为 Agent $i$ 的真实参与概率，$\varpi$ 为全局步长。AGS‑RS 等价于在不知道 $p_i$ 时对各参与方平等对待，但会隐性改变优化目标；AGS‑AP 则通过逆概率加权保证 **聚合方向在期望下无偏**，使算法真正求解原始问题 (1.1)。

### 无偏聚合的期望推导
假设局部梯度流 $\zeta_{t,K}^i$ 的方向逼近局部真实梯度 $\mathrm{grad} f_i(x)$，则 AGS‑AP 的聚合量满足
$$\mathbb{E}_{S_t}\!\left[ \sum_{i\in S_t} \frac{1}{p_i N} \,\mathrm{grad} f_i(x) \right] = \mathrm{grad} F(x) \tag{2.1}$$
这一等式源于对采样指示器 $\mathbb{I}_{S_t}(i)$ 的期望：$\mathbb{E}[\mathbb{I}_{S_t}(i)] = p_i$。它直接证明：虽然每轮仅有部分 Agent 参与，加权和（除以 $p_i N$ 而非 $|S_t|$）的期望正好等于全局全参与梯度。因此，使用 AGS‑AP 的 RFedAGS 在期望意义上避免了简单平均（AGS‑RS）所导致的 **目标偏移**（即收敛到重加权问题而非原问题）。

### 参与概率的在线估计
实际中 $p_i$ 往往未知，RFedAGS 采用历史频率估计：
$$\mathfrak{q}_t^i = \sum_{\tau=1}^{t-1} \mathbb{I}_{S_\tau}(i),\qquad q_t^j = \frac{\mathfrak{q}_t^j}{t-1}$$
服务器每轮用 $q_t^i$ 替代 $p_i$ 执行 (AGS‑AP)。估计误差随轮次衰减：存在常数 $\mathcal{G}$ 使高概率满足 $\big|\frac{1}{q_t^i}-\frac{1}{p_i}\big| \le \mathcal{G}\,t^{-a/2}$（Theorem 3.6）。这一界控制了因概率估计不准而引入的额外漂移项，并最终嵌入到收敛分析中的复合误差项 $Q(K,B,\alpha,\varpi)$（详见 Lemma D.5），保障了算法在有限样本下的次线性/线性收敛速率（Theorem 3.4, 3.5）。

### 模块协作的因果链路
上述模块构成一条闭合的因果链：
1. **向量传输与梯度流** 将流形上的非线性平均化为切空间线性平均 → 降低计算复杂度并兼容任意回缩；
2. **逆概率加权** 矫正部分参与带来的期望偏差 → 保证算法求解原目标；
3. **频率估计** 使算法在不预知 $p_i$ 时仍能维持无偏性，且估计误差通过高概率界引入收敛准则 → 使理论保证具有实际可操作性。

整个设计使得 RFedAGS 在一次通信轮次内以 $\mathcal{O}(d p N)$ 的服务器计算代价（Table 2），同时处理 **非凸/强凸目标、非IID 数据分布、任意部分参与** 三种实际困难，并在 PCA、HSP、FMC 等实验中一致优于现有黎曼联邦学习算法（Figure 2‑4）。



## 实验与关键发现

RFedAGS 在四个具有不同流形结构的标准基准上进行了评估：主成分分析 (PCA, 球面 $\mathbb{S}^{d-1}$)、双曲空间上的最短路径预测 (HSP, 庞加莱球 $\mathbb{B}^d$)、黎曼流形上的均值计算 (FMC, 对称正定矩阵流形 $\mathrm{Sym}^+(d)$) 和低秩矩阵补全 (LRMC, 格拉斯曼流形 $\mathrm{Gr}(d, r)$)。所有实验均采用非独立同分布 (non-IID) 数据划分和部分代理参与的设置，以检验算法在真实联邦场景下的有效性。基线包括现有黎曼联邦方法 RFedAvg、RFedSVRG 和 RFedProj，它们依赖指数映射与并行传输，仅能处理完整参与或均匀部分参与。

### 主结果

- **PCA（合成数据与 CIFAR-10）**：在最优性间隙指标上，RFedAGS 收敛更快且最终间隙显著低于所有基线 (Figure 2)。球形流形上局部参数平均 (TM) 在高异质性下会漂移至局部解，而 RFedAGS 通过将梯度流回传至全局切空间进行线性平均，有效抑制了代理漂移 ($\text{confidence}=0.95$)。
- **HSP (WordNet)**：RFedAGS 的预测点与真实点的黎曼距离小于 RFedAvg 和 RFedSVRG，验证了其在双曲几何下的泛化能力 (Figure 3, $\text{confidence}=0.95$)。
- **FMC (PATHMNIST)**：在 $\mathrm{Sym}^+(d)$ 上估计多个数据点的黎曼均值时，RFedAGS 的距离曲线始终低于对比算法，且随通信轮次增加优势更明显 (Figure 4, $\text{confidence}=0.95$)。
- **LRMC (MovieLens 1M)**：最佳配置 ($K=16, r=7$) 下 RFedAGS 取得 RMSE $7.468\times10^{-1}$，与集中式方法 LRBFGS ($7.382\times10^{-1}$) 差距很小，说明分布式梯度流聚合可逼近集中式矩阵补全性能 (Table 3, $\text{confidence}=0.9$)。该点需手动验证更详细的调参报告。

![[assets/figures/papers/iclr26_0015_oEtrDiFOFF_Riemannian_Federated_Learning_via_Averaging_Grad/figures/010_Figure_2.jpg]]
*Figure 2: PCA: RFedAGS consistently performs better than the competing methods across both synthetic and real datasets. (a)*

![[assets/figures/papers/iclr26_0015_oEtrDiFOFF_Riemannian_Federated_Learning_via_Averaging_Grad/figures/012_Figure_3.jpg]]
*Figure 3: HSP with WordNet dataset. Here “primate” is the test sample (true point)*

![[assets/figures/papers/iclr26_0015_oEtrDiFOFF_Riemannian_Federated_Learning_via_Averaging_Grad/figures/014_Figure_4.jpg]]
*Figure 4: FMC with PATHMNIST dataset: RFedAGS consistently performs better than RFedAvg and RFedSVRG*

![[assets/figures/papers/iclr26_0015_oEtrDiFOFF_Riemannian_Federated_Learning_via_Averaging_Grad/figures/044_Table_3.jpg]]
*Table 3: The best RMSE scores (lower is better) on testing set for different subspace dimension r and different number of local update K. Here the scalar a . b c $d _ { k }$ denotes a.bcd $\times$ 1 $0 ^ { k }$*

### 消融分析

- **聚合模式选择 (AGS-AP vs. AGS-RS)**：在非 IID MNIST 的 PEC 任务上，标准等权平均 (AGS-RS) 收敛至一个错误的重加权目标，而逆概率加权 (AGS-AP) 则解决了原始问题，间隙降低一个数量级以上 (Figure 6, 7, $\text{confidence}=0.95$)。
- **参与概率估计**：用历史参与频率估计 $q_t^i$ 代替真实概率 $p_i$ 时，RFedAGS 的性能与已知真实概率的情况几乎一致 (Figure 8, 9, $\text{confidence}=0.9$)，验证了 Theorem 3.6 的高概率保证在实际中成立。
- **数据异质性影响**：随标签不平衡程度加剧，所有算法性能均下降，但 RFedAGS 的退化幅度更小，且在相同异质性水平下仍保持领先 (Figure 10, 12, $\text{confidence}=0.9$)。
- **局部迭代步数 $K$**：增大 $K$ 可加速收敛 (Figure 11, 13)，但 $K$ 过大时误差项 $Q(K,\cdots)$ 中的代理漂移分量上升，与理论界一致 (Theorem 3.4)。在 LRMC 上 $K=30$ 较 $K=1$ 的收敛轮次减少约 80%。
- **可扩展性**：固定每代理样本数时，增加代理数量或流形维度，RFedAGS 的收敛性能呈线性加速趋势，表明聚合梯度流具有良好的缩放性质 (Figure 16, $\text{confidence}=0.85$，该消融细节在部分描述中需进一步核实)。

### 失败模式与局限

1. **时间不变参与假设**：理论分析基于 $p_i$ 恒定的统计模型 (Assumption 2.1)，无法直接处理时变参与场景（如设备在线时长动态变化）。
2. **极小参与概率的退化**：对 $p_i \ll 1/N$ 的代理，概率估计误差界中的 $G$ 因子较大 (Assumption 3.8)，导致逆权重 $1/q_t^i$ 方差激增，可能损害收敛。
3. **每步向量传输开销**：每轮局部迭代均需执行向量传输 $\mathcal{T}$，在部分流形上计算成本较高，且限制了无法定义一致有界传输 ($\Upsilon$) 的流形上的应用。
4. **紧致性假设**：收敛分析要求所有迭代点位于可完全回缩的紧致子流形内，无界流形（如双曲空间）上的保证有待加强。
5. **大规模深度学习未验证**：当前实验限于中小规模矩阵或向量优化，高维张量流形（如 product manifold）上的联邦深度学习任务尚待探索。

### 重要图表结论

- **Table 1** 横向对比了现有黎曼 FL 算法的五大特性：RFedAGS 是唯一支持部分参与、非 IID 数据、一般回缩和有界向量传输的方法，且不限于紧致子流形。
- **Figure 1** 几何展示 (TM) 与 (AGS-RS) 的差异：前者直接平均局部参数导致脱离流形均值，后者通过切空间线性平均保留信息，实验验证 AGS-RS 相较 TM 在简单任务上即可获得更低误差。
- **Table 2** 计算复杂度表明 RFedAGS 在服务器端仅增加 $dpN$ 的向量传输和概率估计开销，与 RFedAvg 处于同一量级，而局部计算代价与 RFedAvg 相当。
- **Figure 2–4, Table 3** 作为主结果图，联合证明了平均梯度流框架在球面、双曲、SPD 和格拉斯曼流形上的普适优势。
- **Figure 13** 揭示了 $K$ 的消融：$K$ 增大带来的收益逐步递减，存在一个依赖任务异质性的最优区间，过大 $K$ 将因代理漂移主导而停滞。



## 定位与知识库关联

现有黎曼联邦学习方法联合处理部分参与和非IID数据的能力存在根本性断裂。**RFedAvg**、**RFedSVRG** 等基线依赖指数映射与并行传输实施服务器端的切线均值聚合，不仅要求流形具备闭式表达，而且将服务器更新耦合于局部模型的欧氏平均，当各Agent的数据分布异构时会收敛到错误目标（Theorem 2.1）。**RFedProj** 虽采用投影算子，但仍限于紧子流形，且三者均未提供对任意参与模式的通用处理，导致实际部署受限。

**RFedAGS** 切入这一断裂点的因果机制有二：（1）用**平均梯度流**（AGS）取代局部参数平均，通过向量传输将各Agent的局部随机梯度追踪到全局切空间后线性混合，再利用一般回缩更新全局模型，既规避了非线性聚合的几何复杂性，又使算法适用于更广泛的流形（Table 1, Assumption 3.1）；（2）引入**逆概率加权**聚合（AGS‑AP），用估计的参与概率 $q_t^i$ 代替真实 $p_i$ 来缩放局部梯度流，保证聚合梯度的期望无偏（Eq. 2.1），从而使优化目标恢复到原始全局问题，而非部分参与诱导的加权变体。这两个核心变更将黎曼联邦学习从“参数空间平均”范式推向“切空间梯度流线性平均”范式。

与基线的定量对比显示，RFedAGS 在 PCA、HSP、FMC 等任务上一致收敛更快且达到更低的优化间隙或距离（Figure 2‑4），在 LRMC 上的 RMSE（7.468e‑1）接近集中式最优方法（7.382e‑1，Table 3）。消融实验进一步验证：简单平均（AGS‑RS）会收敛到错误的重加权目标，而 AGS‑AP 则还原原始问题（Figure 6‑7）；用历史参与频率估计概率的表现几乎等价于使用真实概率，证实了无先验知识下的可行性（Figure 8‑9, Theorem 3.6）。

尽管 RFedAGS 拥有次线性/线性收敛的理论保证（Theorem 3.4, 3.5），其适用边界严格受限于若干假设与分析框架：
- 时间**不变的参与概率**（Assumption 2.1）排除了时变参与情景，实际系统中节点可用性往往是动态的；
- 逆概率加权的误差界依赖于**概率估计的精度**（$G$ 因子，Assumption 3.8），当部分 Agent 参与概率极低时，估计误差会放大梯度流的方差，导致性能退化；
- 算法在**每步局部更新均需向量传输**，对于无高效传输算子的流形会增加可观的计算与通信开销（Table 2 的 LICpA 项包含 $\\mathbf{v}(K-1)$）；
- 收敛分析要求迭代点始终位于一个**紧致、完全可回缩的集合**内（Assumption 3.5 及相关定义），而在无界流形上该假设可能失效；
- 当前实验仅覆盖**中小规模问题**，在流形上的大规模深度学习联邦场景尚未探索。

据此，若干开放问题直接指向该方法的未来演进：
1. 能否将收敛保证推广到**时变参与概率模型**，使 RFedAGS 适应真实动态网络？
2. 如何将**动量或方差缩减技术**（如 SVRG）融入平均梯度流框架，以进一步抵消 Agent 漂移和随机梯度噪声？
3. 在**异质计算预算**下，是否存在针对局部更新步数 $K$ 的理论最优值，或可设计自适应调度策略？
4. 算法在**更高维或更复杂流形**（例如自然语言处理中采用的双曲空间）上的行为与局限性亟需检验。
5. 是否能设计**完全避免向量传输**的、流形无关的聚合策略，从而从根本上降低对几何算子的依赖？

上述局限与开放问题共同界定了 RFedAGS 在黎曼联邦学习方法谱系中作为**首个同时支持非IID和部分参与的通用框架**的历史地位，也为其后续改进提供了明确的验证路径。



## 原文 PDF

![[paperPDFs/ICLR_2026/Riemannian_Federated_Learning_via_Averaging_Gradient_Streams.pdf]]
