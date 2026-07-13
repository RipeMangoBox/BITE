---
title: "Non-Convex Federated Optimization under Cost-Aware Client Selection"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Non_Convex_Federated_Optimization_under_Cost_Aware_Client_Selection.pdf
project_link: null
code_link: null
aliases:
- ICRSICGMRGSE
- NCFOUCACS
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/large_scale_parallel_and_distributed
core_operator: "利用函数相似度δ（而非L_max）作为方差控制参数，并引入递归梯度（RG）技术进一步收紧误差界，从而在不增加全同步开销的前提下大幅降低通信和本地复杂度。"
primary_logic: "将不精确复合梯度方法（I-CGM）与基于SAGA的递归梯度估计器（RG-SAGA）相结合，首次实现了在仅依赖函数相似性δ的前提下，无需全同步、仅需部分客户端参与的通信与本地复杂度最优设计。"
claims:
- "SAGA估计器的方差界仅依赖于函数相似度δ，而非个体平滑性L_max（Lemma 4.1）"
- "递归梯度技术可将SAGA的误差界提升n_m倍（Corollary 5.3）"
- "I-CGM-RG-SAGA在Table 1中达到所有方法中最优的通信与局部复杂度"
- "在二次最小化与LIBSVM逻辑回归实验中，I-CGM-RG-SAGA在通信效率上始终最优（Figure 1, Figure 2）"
---

# Non-Convex Federated Optimization under Cost-Aware Client Selection

> [!tip] 核心洞察
> 将不精确复合梯度方法（I-CGM）与基于SAGA的递归梯度估计器（RG-SAGA）相结合，首次实现了在仅依赖函数相似性δ的前提下，无需全同步、仅需部分客户端参与的通信与本地复杂度最优设计。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 成本感知客户端选择下的非凸联邦优化 |
| 英文题名 | Non-Convex Federated Optimization under Cost-Aware Client Selection |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=FnaDv6SMd9) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/large_scale_parallel_and_distributed |
| Method | I-CGM-RG-SAGA (Inexact Composite Gradient Method with Recursive Gradient SAGA estimator) |
| Dataset | EMNIST (6-layer Residual CNN, heterogeneous Dirichlet α=0.1), CIFAR10 (ResNet18, Quadratic minimization with non-convex log-sum penalty (synthetic), LIBSVM logistic regression with nonconvex regularizer (mushrooms, duke) |

> [!tip] 效果简介
> - EMNIST (6-layer Residual CNN, heterogeneous Dirichlet α=0.1) 上，Validation accuracy (100 outer iterations) 为 86.2% (I-CGM-RG-SAGA)，对比 85.6% (FedAvg)，变化 +0.6%。
> - CIFAR10 (ResNet18, heterogeneous Dirichlet α=0.1) 上，Validation accuracy (100 outer iterations) 为 76.1% (I-CGM-RG-SAGA) / 77.0% (I-CGM-RG-SVRG)，对比 74.3% (FedAvg) / 72.3% (Scaffold)，变化 +2.8% over FedAvg (SAGA), +4.7% over Scaffold (SVRG)。
> - Quadratic minimization with non-convex log-sum penalty (synthetic) 上，Communication efficiency (target accuracy) 为 I-CGM-RG-SAGA most efficient，对比 I-CGM-RG-SVRG, Scaffold, FedAvg, SABER-partial, SABER-full, GD，变化 substantially fewer communication rounds。

## 概要

现有联邦非凸优化算法在通信与局部计算复杂度上高度依赖**周期性全同步**（如基于SARAH的方法）或**个体平滑度常数**$L_{\max}$（如SAG/SAGA类），导致在异构网络与大系统设定下成本难以控制，不同策略间的比较也无法做到公平。为突破这一瓶颈，本文通过引入**函数间平均相似度**$\delta$ 替代个体平滑度作为方差控制参数，并融合**不精确复合梯度方法（I-CGM）**、**SAGA梯度估计器**以及**递归梯度（RG）技术**，提出了 **I-CGM-RG-SAGA** 方法。该方法的核心贡献在于首次实现了**仅依赖函数相似性 $\delta$**、**无需全同步**且**仅需部分客户端参与**的通信与局部复杂度最优设计，显著压缩了对全同步和个体光滑性假设的依赖。

关键因果链条如下：
- **SAGA估计器**的方差上界仅取决于平均相似度 $\delta$，而不需要每个客户端的平滑常数（Lemma 4.1），这使得在异构环境下仍能保持低方差；
- **递归梯度（RG）技术**作为通用工具，对条件无偏估计器进行加权历史信息融合，可将SAGA的误差界再收紧 $n_m$ 倍（Corollary 5.3），从而进一步降低总复杂度；
- **I-CGM框架**允许子问题不精确求解，配合几何分布的随机局部步数机制，在客户端1局部光滑性 $L_1$ 的辅助下，避免了固定大量局部步数带来的计算浪费。

理论复杂度对比（Table 1）显示，I-CGM-RG-SAGA 的总通信成本上界为 $\mathcal{O}(C_A n_m + C_R (\Delta_1 + \sqrt{n_m}\delta_m) F^0 / \varepsilon^2)$，在所有同类一阶方法中取得最优。实验方面，在合成非凸对数‑和惩罚二次最小化问题（Figure 1）、LIBSVM 逻辑回归任务（Figure 2）中，该方法在通信效率上始终领先于 Scaffold、SABER、FedAvg 等基线；在 EMNIST（6层Residual CNN，异构Dirichlet划分）和 CIFAR10（ResNet18）的100轮通信内，验证精度分别达到 $86.2\%$ 和 $76.1\%$，较 FedAvg 提升 $+0.6\%$ 和 $+2.8\%$（Table J.2, J.4）。消融研究进一步表明，方法在**零全梯度初始化**下仍可收敛，关键参数 $\lambda$ 与 $\beta$ 的经验最优值与理论推导一致，且通信复杂度随客户端数 $n_m$ 呈 $\sqrt{n_m}$ 增长而非线性增长，验证了理论界（Figure J.3–J.6）。

目前方法尚存在若干局限：① 依赖固定的委托客户端（客户端1）来执行局部复合梯度更新，若移除该假设而采用随机客户端选择，平滑常数将由 $\Delta_1$ 退化为 $\Delta_{\max}$，复杂度常数会升高（此替代方案已在文中讨论，但未实验验证）；② 仅针对确定性一阶oracle设计，未覆盖随机小批量、零阶或高阶信息版本；③ 未引入通信压缩（量化或稀疏化），直接应用压缩将破坏梯度估计器的方差界，需重新设计。因此，在更一般的随机梯度与压缩通信设置下，维持当前最优复杂度仍是开放问题。部分实验结论（如全同步对比）依赖合成数据，在多任务真实分布上的相对优势强度宜由后续研究进一步确认。

联邦学习中的非凸优化问题广泛存在于现代深度学习任务中，但通信瓶颈与客户端异构性使得高效分布式训练更具挑战。一方面，标准联邦平均（FedAvg）及其变体虽支持部分客户端参与，却缺乏方差缩减机制，导致收敛缓慢；另一方面，基于方差缩减的方法（如 Scaffold、MimeMVR、SABER、SCAFFNEW 等）虽能加速收敛，但其通信或局部计算复杂度高度依赖两种成本高昂的设计元素：（1）周期性**全同步**（full participation），例如 SARAH 类方法在每轮内层循环中都需所有客户端参与，极大增加实际系统开销；（2）依赖**个体平滑度常数** $L_{\max}$（单个客户端梯度 Lipschitz 常数）而非全局函数间的**相似度** $\delta$，使得局部计算量随客户端差异增大而急剧膨胀。这些方法在非凸设定下的复杂度界无法实现通信与局部计算的最优折衷，并且由于缺乏统一的成本感知客户端选择模型，不同研究难以进行公平对比。

造成这一瓶颈的根本原因在于：现有梯度估计器（如 SAG、SAGA、SVRG、SARAH）的方差界要么需要全同步来维持低误差，要么不得不引入 $L_{\max}$ 或对客户端数量 $n$ 的线性依赖，而在大规模异构网络中，$L_{\max}$ 通常远大于函数相似度 $\delta$。因此，一个核心挑战是：**能否设计一种联邦优化算法，在仅需部分客户端参与的随机选择策略下，利用 $\delta$（而非 $L_{\max}$）来控制方差，从而同时显著降低通信轮次和局部计算量，且无需任何周期性的全同步？**

本文的动机正是填补这一缺口。我们首先引入一个简洁的成本感知客户端选择模型，将**任意选择**（A‑CSS，成本 $C_A$）与**随机选择**（R‑CSS，成本 $C_R$）统一在同一框架下，使得通信复杂度和局部复杂度可以被公平比较。在该模型中，我们提出一种**不精确复合梯度方法 I‑CGM**，作为算法骨架，并结合两大核心技术：（1）**SAGA 估计器**，其方差界仅受函数相似度 $\delta$ 约束（而非 $L_{\max}$），且通过增量更新避免全同步（Lemma 4.1）；（2）**递归梯度 (RG) 技术**，一种通用的条件无偏估计增强机制，可将 SAGA 的累积误差界进一步收紧 $n_m$ 倍（Corollary 5.3）。此外，局部子问题采用**几何分布随机步数的复合梯度法**求解，使不精确条件在期望意义上成立（Lemma 3.4）。最终形成的 **I‑CGM‑RG‑SAGA** 算法在 Table 1 中展示了所有对比方法中最优的通信与局部复杂度界，其核心常数仅包含委托客户端的光滑度 $\Delta_1$ 和参与客户端子集的相似度 $\sqrt{n_m}\,\delta_m$，无需 $L_{\max}$ 且全程无需全同步。这一设计为在成本感知的联邦环境中实现高效非凸优化提供了新的理论基础，也在合成实验（Figure 1）和真实数据（Figure 2）中验证了其通信效率的领先优势。

## 核心方法与创新机理

本工作的核心创新围绕四个关键维度（梯度估计、子问题求解、复杂度依赖常数、全同步需求）对现有联邦非凸优化进行了根本性重构，形成了 I‑CGM‑RG‑SAGA 算法。通过将递归梯度（RG）技术与 SAGA 方差缩减深度结合，并以委托客户端与函数相似度 $\delta$ 取代个体平滑性依赖，该方法在不增加全同步开销的前提下，于通信和局部计算两个复杂度上均达到现有方法中的最优水平（Table 1）。

### 1. 梯度估计器：以 $\delta$‑依赖的 RG‑SAGA 替代 $L_{\max}$ 或全同步依赖的估计器
- **基线局限**：SCAFFOLD 的 SAG 方差界隐含依赖个体平滑度 $L_{\max}$，SARAH 类方法（SABER）需要周期性全同步，SVRG 虽可部分参与但误差界含 $1/p_B$ 放大因子，难以同时实现低通信与低局部计算。
- **提出设计**：
  - 首先分析 **SAGA 估计器**，证明其累积方差仅由函数相似度 $\delta$ 控制，与 $L_{\max}$ 无关（Lemma 4.1）。
  - 进一步引入 **递归梯度（RG）** 技术：`g^{t+1} = (1-β) g^t + β G^t + ∇f_{S_t}(x^{t+1}) - ∇f_{S_t}(x^t)`，将 SAGA 的误差界额外收紧 $n_m$ 倍（Corollary 5.3，相比直接 SAGA 提升 $n_m$ 因子）。
- **效果**：通信复杂度主导项从 $L_{\max}/\varepsilon^2$ 降至 $(\Delta_1 + \sqrt{n_m}\delta_m)/\varepsilon^2$（Table 1），在函数相似度高的场景（如 mushrooms 中 $\delta \ll L_1$）通信轮次锐减数个数量级（Figure 2）。

### 2. 子问题求解器：以几何随机局部步数取代固定局部步数 $K$
- **基线方法**：多数算法（FedAvg、SCAFFOLD 等）使用固定局部 GD 步数 $K$，无法从理论上保证子问题不精确条件，且调参依赖人工经验。
- **提出方案**：采用带 **几何随机终止** 的局部复合梯度法，每轮局部步数 $K_t \sim \text{Geom}(p)$。利用客户端 1 的 $L_1$‑光滑性，证明该随机步数满足 I‑CGM 所要求的不精确条件（Lemma 3.4），期望局部步数为 $\mathcal{O}(1/p) = \mathcal{O}(L_1/(\lambda - \Delta_1))$。
- **优势**：自适应平衡局部计算与通信，无需预设 $K$；实验显示过大 $p$（$p=0.5$）损害效率，而 $p=0.05$ 与 $p=0.005$ 性能相近但计算更少（Figure J.2），验证了随机终止机制的鲁棒性。

### 3. 复杂度依赖常数：以 $\Delta_1$ 和 $\delta$ 取代 $L_{\max}$ 和 $n$
- **基线瓶颈**：SCAFFOLD、SABER 等方法的复杂度中含有 $L_{\max}$ 或 $n$ 因子，当个体函数极度异构或客户端总数极大时效率急剧退化。
- **提出改进**：将问题重构为复合形式 $f = f_1 + h_1$，并引入委托客户端 1。复杂度分析中不再出现 $L_{\max}$，而是依赖 $h_1$ 的光滑度 $\Delta_1$ 和函数相似度 $\delta$（Assumption 2.2）。经 RG‑SAGA 进一步优化后，通信复杂度为 $\mathcal{O}\big(C_A n_m + C_R (\Delta_1 + \sqrt{n_m}\delta_m) F^0 / \varepsilon^2\big)$（Theorem F.7），在 Table 1 中列出的 11 种方法中唯一同时实现最优通信与局部复杂度。
- **意义**：理论常数与实际数据分布中的函数相似性紧密对应，使算法在异构环境下获得坚实的效率保证，而非仅依赖最坏情况的 $L_{\max}$。

### 4. 初始全同步需求：从必须到完全免除
- **基线要求**：SARAH 类方法（SABER‑full）每次外循环需全客户端参与，SABER‑partial 仍需以全梯度初始化；标准 CGM 同样依赖精确全梯度启动。
- **提出方案**：I‑CGM‑RG‑SAGA 从 $t_0=0$ 即可仅用部分客户端（任意 $m$ 个）启动，无需任何全同步（Lemma G.1）。算法只需一次广播初始点，之后所有通信轮次均为部分参与。
- **优势**：消除了高成本的冷启动全同步，降低了系统初始化与动态重组的门槛，并在消融实验中验证了无全梯度初始化的正常收敛（Figure J.1）。

上述四个方面的协同创新使 I‑CGM‑RG‑SAGA 在仅依赖函数相似度 $\delta$ 的条件下，实现了无需全同步、部分参与、且通信与局部复杂度均达最优的联邦非凸优化，从根本上突破了现有方法依赖 $L_{\max}$ 或周期性全同步的瓶颈。

I-CGM-RG-SAGA 以不精确复合梯度方法（I-CGM）为外层骨架，将分布式目标 $f(\mathbf{x}) = \frac{1}{n} \sum_{i=1}^n f_i(\mathbf{x})$ 变形为 $f_1(\mathbf{x}) + \frac{1}{n}\sum_{i=1}^n h_i(\mathbf{x})$（其中 $h_i = f_i - f_1$）的复合形式，从而利用委托客户端 $f_1$ 的 $L_1$‑光滑性（$\|\nabla f_1(\mathbf{x}) - \nabla f_1(\mathbf{y})\| \leq L_1 \|\mathbf{x} - \mathbf{y}\|$, Assumption 2.3）。每轮迭代由三个协同模块构成：

* **梯度估计器（RG‑SAGA）** – 以递归梯度方式融合 SAGA 缓存更新。每个客户端 $i$ 维护局部梯度缓存 $\mathbf{b}_i^t$，服务器聚合后得到 $\mathbf{b}^t$（Eq. (10)），并构造 SAGA 估计器 $\mathbf{G}^t$（Eq. (SAGA)）。递归混合 $\mathbf{g}^{t+1} = (1-\beta)\mathbf{g}^t + \beta\mathbf{G}^t + \nabla f_{S_t}(\mathbf{x}^{t+1}) - \nabla f_{S_t}(\mathbf{x}^t)$（Eq. (RG)）进一步压低误差界。该估计器的方差仅依赖全局函数相似度 $\delta$（Assumption 2.2），无需个体光滑常数 $L_{\max}$（Lemma 4.1）；递归机制额外将误差界缩小 $n_m$ 倍（Corollary 5.3）。
* **局部子问题求解器（Local CGM with Geometric Stopping）** – 给定梯度方向 $\mathbf{g}^t$ 与正则化参数 $\lambda$，求解近端子问题（见 Eq. (I‑CGM)）：
  $$\mathbf{x}^{t+1} \approx \arg\min_{\mathbf{x}} \Big\{ f_1(\mathbf{x}) + h_1(\mathbf{x}^t) + \langle \mathbf{g}^t - \nabla f_1(\mathbf{x}^t), \mathbf{x} - \mathbf{x}^t \rangle + \frac{\lambda}{2} \|\mathbf{x} - \mathbf{x}^t\|^2 \Big\}.$$
  求解在选中客户端 $S_t$ 本地以复合梯度法完成，步数 $K_t \sim \mathrm{Geom}(p)$ 随机化（Lemma 3.4）。选择 $p = (\lambda - \Delta_1)/(8(L_1 + \lambda))$ 即可满足不精确条件，保证子问题精度不影响整体收敛速率（Theorem 3.1）。
* **全局状态更新与聚合** – 客户端仅回传局部梯度差分（如 $\nabla f_i(\mathbf{x}^t), \nabla f_i(\mathbf{x}^{t+1})$ 及缓存增量），服务器据此更新 $\mathbf{b}^t$、$\mathbf{G}^t$ 和 $\mathbf{g}^{t+1}$，形成下一轮方向，无需额外全同步轮次（$t_0=0$ 时算法仍收敛，见 Lemma G.1 与 Figure J.1）。

**模块间数据流**：每通信轮 $t$，服务器选择客户端子集 $S_t$（大小 $m$），发送当前点 $\mathbf{x}^t$ 与方向 $\mathbf{g}^t$（必要时附带缓存摘要）；各客户端利用本地数据及 $f_1$ 的梯度信息执行随机步数的局部复合梯度下降，产生 $\mathbf{x}^{t+1}$ 并回传必要差分；服务器聚合后得到 $\mathbf{x}^{t+1}$ 和更新后的梯度估计，驱动下一轮迭代。该流程将梯度估计误差、子问题不精确性与通信成本解耦，最终通信与本地复杂度仅由 $\Delta_1, \delta, \sqrt{n_m}\delta_m$ 等常数控制（Table 1），首次在非凸联邦优化中同时实现了无需全同步的最优通信与本地效率（Section 6）。

**整体框架：不精确复合梯度方法 (I‑CGM)**  
I‑CGM 将联邦优化问题重写为复合形式，并允许子问题不精确求解。其核心迭代为

$$
\mathbf{x}^{t+1} \approx \arg\min_{\mathbf{x}\in\mathbb{R}^d} \Bigl\{
f_1(\mathbf{x}) + h_1(\mathbf{x}^t) + \bigl\langle \mathbf{g}^t - \nabla f_1(\mathbf{x}^t),\, \mathbf{x} - \mathbf{x}^t \bigr\rangle + \frac{\lambda}{2}\|\mathbf{x} - \mathbf{x}^t\|^2 \Bigr\},
$$

其中 $f_1$ 为委托客户端（客户端 1）的局部函数，$h_1 = f - f_1$，$\mathbf{g}^t$ 是全局梯度 $\nabla f(\mathbf{x}^t)$ 的近似，$\lambda > \Delta_1$（$\Delta_1$ 为 $h_1$ 的光滑性常数）。该近端子问题将函数减小的估计与梯度近似绑定；当 $\mathbf{g}^t$ 精确时退化为标准复合梯度法 (CGM)。

**关键假设：函数相似度 $\delta$ 取代个体光滑性 $L_{\max}$**  
传统方法依赖 $\max_i L_i$，而本文利用全局函数差异的平均二阶矩，即

$$
\frac{1}{n}\sum_{i=1}^n \bigl\|\nabla h_i(\mathbf{x}) - \nabla h_i(\mathbf{y})\bigr\|^2 \le \delta^2 \|\mathbf{x} - \mathbf{y}\|^2,
$$

其中 $h_i = f - f_i$。结合 $f_1$ 的 $L_1$‑光滑性，复杂度常数从 $L_{\max}$ 降至 $\Delta_1$ 与 $\delta$。

**模块一：SAGA 估计器——无全同步的方差缩减**  
SAGA 使用客户端历史梯度的增量更新，避免周期性全同步。梯度估计器定义为

$$
\mathbf{G}^t =
\begin{cases}
\nabla f(\mathbf{x}^t), & t = 0,1,\\[4pt]
\mathbf{b}_{S_t}^t - \mathbf{b}_{S_t}^{t-1} + \mathbf{b}^{t-1}, & t \ge 2,
\end{cases}
$$

其中 $S_t$ 为随机抽取的 $m$ 个客户端子集，$\mathbf{b}^t$ 为聚合梯度近似，更新规则为

$$
\mathbf{b}^t = \mathbf{b}^{t-1} + \frac{1}{n_m}\bigl[\nabla f_{S_t}(\mathbf{x}^t) - \mathbf{b}_{S_t}^{t-1}\bigr],\qquad n_m = \frac{n}{m}.
$$

**Lemma 4.1** 证明该估计器的累积方差仅依赖 $\delta$ 和 $m$，与个体 $L_i$ 无关，从而在异构网络下获得紧得多的界。

**模块二：递归梯度 (RG) 技术——进一步收紧误差界**  
RG 将历史梯度近似与条件无偏估计 $\mathbf{G}^t$ 以混合系数 $\beta$ 组合：

$$
\mathbf{g}^{t+1} = (1-\beta)\mathbf{g}^t + \beta\mathbf{G}^t + \nabla f_{S_t}(\mathbf{x}^{t+1}) - \nabla f_{S_t}(\mathbf{x}^t).
$$

该形式统一了 SARAH、ZEROSARAH 和 STORM 的特例，并在 SAGA 或 SVRG 基础上使累积误差界额外缩小 $n_m$ 倍（Corollary 5.3）：

$$
\sum_{t=0}^{T} \Sigma_t^2 \lesssim \frac{q_m}{m} G_1^2 + \frac{1}{n}\sum_{t=2}^{T-1} G_t^2 + n_m \delta_m^2 \sum_{t=1}^{T} \chi_t^2,
$$

其中 $\delta_m^2 = \frac{q_m}{m}\delta^2$，$q_m = \frac{n-m}{n-1}$。可见噪声由 $\sqrt{n_m}\delta_m$ 而非 $L_{\max}$ 主导。

**模块三：局部子问题求解与几何停止规则**  
为满足不精确条件，子问题 (I‑CGM) 在客户端 1 上以局部 CGM 求解，步数 $K_t$ 服从几何分布 $\mathrm{Geom}(p)$，$p = \frac{\lambda - \Delta_1}{8(L_1 + \lambda)}$（Lemma 3.4）。这使得局部复杂度可控，且无需每轮解到高精度。

**总体收敛与复杂度界**  
将 I‑CGM 的泛化误差界 (Theorem 3.1)

$$
\sum_{t=1}^{T} \|\nabla f(\mathbf{x}^t)\|^2 + (\lambda+\Delta_1)^2 \sum_{t=1}^{T} \|\mathbf{x}^t-\mathbf{x}^{t-1}\|^2 \le \frac{12(\lambda+\Delta_1)^2}{\lambda-\Delta_1}F^0 + \Bigl(\frac{12(\lambda+\Delta_1)^2}{(\lambda-\Delta_1)^2}+4\Bigr)\sum_{t=0}^{T-1}\hat{\Sigma}_t^2 + 4\sum_{t=0}^{T-1}e_t^2
$$

与 RG‑SAGA 的方差界结合，即得到 I‑CGM‑RG‑SAGA 的总通信成本上界（Table 1）：

$$
\text{Communication complexity} = \mathcal{O}\Bigl( C_A n_m + C_R \frac{(\Delta_1 + \sqrt{n_m}\,\delta_m) F^0}{\varepsilon^2} \Bigr),
$$

其中 $C_A$、$C_R$ 分别为每轮激活和传输成本，$F^0$ 为初始函数值差。该界在无需全同步、仅需部分客户端参与的前提下，达到了所有现有方法中的最优量级，且常数仅依赖 $\Delta_1$ 与 $\delta$。

## 实验与关键发现

### 主要结果

实验覆盖四类任务：带有非凸 log‑sum 惩罚的合成二次极小化、LIBSVM 数据集上的非凸正则化逻辑回归、以及异构数据划分下的 EMNIST 和 CIFAR10 图像分类。所有基线方法（FedAvg、Scaffold、SABER‑full/‑partial、SCAFFNEW、MimeMVR、CE‑LGD、FedDyn、FedRed 等）均进行了超参数全面调优，控制变量方法统一引入阻尼因子 $q$ 以稳定训练（常见于 Yin et al., 2025），且局部计算量按期望计入总复杂度，保证公平比较。

#### 合成二次极小化与 LIBSVM 任务

在二次极小化（Figure 1）与 LIBSVM 逻辑回归（Figure 2）上，以通信轮次为横轴、梯度范数或精度为纵轴进行效率对比。**I‑CGM‑RG‑SAGA** 在所有对比中展现了最优的通信效率：

![[assets/figures/papers/iclr26_0015_FnaDv6SMd9_Non-Convex_Federated_Optimization_under_Cost-Awa/figures/004_Figure_1.jpg]]
*Figure 1: Comparisons of different algorithms for solving the quadratic minimization problems with non-convex log-sum penalty. I-CGM-RG-SAGA (ours) I-CGM-RG-SVRG (ours) I1 Scaffold FedAvg ? SABER-full SABER-partial Scaffnew Figure 2: Comparisons of different algorithms on two LIBSVM datasets using logistic loss with non-convex regularizer*

![[assets/figures/papers/iclr26_0015_FnaDv6SMd9_Non-Convex_Federated_Optimization_under_Cost-Awa/figures/003_Figure_2.jpg]]
*Figure 2: + I-CGM-RG-SVRG (ours) Scaffold I-CGM-RG-SAGA (ours) FedAvg SABER-partial SABER-full GD*

- 在 mushrooms 数据集上（Figure 2 left），函数相似度参数 $\delta$ 远小于客户端 1 的局部光滑常数 $L_1$，本方法相比 FedAvg、Scaffold、SABER 等方法所需通信轮次呈数量级减少。I‑CGM‑RG‑SVRG 同样高效，但优势略逊于 SAGA 版本。
- 在 duke 数据集上（Figure 2 right），$\delta$ 与 $L_1$ 相接近，算法间的差距缩小，然而 I‑CGM‑RG‑SAGA 仍维持最好性能，验证了其依赖 $\delta$ 而非 $L_{\max}$ 带来的增益。
- 二次极小化实验（Figure 1）中，Scaffold 的局部复杂度与集中式 GD 相当，因其依赖个体平滑性 $L_{\max}$，而本方法通过利用函数相似性明显降低了局部开销，通信‑精度曲线显著优于所有基线。

这些结果与理论总结表 Table 1 吻合：I‑CGM‑RG‑SAGA 的通信复杂度上界为 $\mathcal{O}\big(C_A n_m + C_R \frac{(\Delta_1 + \sqrt{n_m}\delta_m) F^0}{\varepsilon^2}\big)$，在所有对比方案中达到最小项。

![[assets/figures/papers/iclr26_0015_FnaDv6SMd9_Non-Convex_Federated_Optimization_under_Cost-Awa/figures/001_Table_1.jpg]]
*Table 1: Summary of efficiency guarantees (in BigO-notation) for finding an ε-stationary point. I-CGM-RG-SAGA achieves the best communication and local complexities. For the precise description of the problem classes, notations, as well as the discussions of the methods, see Appendix D*

#### 神经网络任务

在异构 Dirichlet ($\alpha=0.1$) 划分的 EMNIST 和 CIFAR10 上，以 100 轮外迭代的验证准确率进行评估。

- EMNIST（6 层残差 CNN）：I‑CGM‑RG‑SAGA 取得 86.2% 的准确率，超越 FedAvg（85.6%）、Scaffold（85.9%）和 SABER‑full（85.3%）。I‑CGM‑RG‑SVRG 紧随其后（86.0%）。
- CIFAR10（ResNet18）：I‑CGM‑RG‑SVRG 以 77.0% 领先，I‑CGM‑RG‑SAGA 为 76.1%，分别比 FedAvg（74.3%）和 Scaffold（72.3%）高出 2.8% 和 4.7%。

理论上，RG‑SAGA 的方差界（Corollary 5.3）不依赖于个体 $L_{\max}$，仅由相似度 $\delta_m$ 控制，这使得其在高度异质的联邦场景下既能保证收敛速度又可降低通信与局部计算需求，实际性能与理论预期高度一致。

### 消融实验

*（以下消融均基于二次极小化任务，详见 Figure J.1‑J.6）*

**初始全同步需求（$t_0=0$）**  
I‑CGM‑RG‑SAGA 在完全不进行全梯度初始化的条件下仍能良好收敛，表明算法对初始全同步没有硬性依赖（Figure J.1）。这一性质源自 RG‑SAGA 估计器的增量更新结构，使方法可以在零知识冷启动下运行，避免了 SABER‑full 等必须周期全同步的开销。

**局部步数参数 $p$**  
随机局部步数 $K_t\sim\mathrm{Geom}(p)$ 对通信效率影响显著。当 $p$ 较大（$p=0.5$）时，平均局部步数过高，损害通信效率；$p=0.05$ 与 $p=0.005$ 精度相近，但后者进一步降低了局部计算成本（Figure J.2）。因此，适中的 $p$（与 Lemma 3.4 中 $p=(\lambda-\Delta_1)/(8(L_1+\lambda))$ 一致）可在不牺牲收敛性的前提下节约局部算力。

**正则化参数 $\lambda$**  
$\lambda$ 过大或过小均导致收敛明显恶化。最优 $\lambda$ 与理论预测 $\Delta_1+\sqrt{n_m}\delta_m$ 高度吻合（Figure J.3），验证了该方法对子问题惩罚系数的理论设置。

**RG 混合参数 $\beta$**  
递归梯度中的混合系数 $\beta$ 在 $[0.05, 0.5]$ 区间内表现良好，与理论最优值 $1/n_m=0.1$ 相符（Figure J.4）。过小的 $\beta$ 削弱了无偏估计的引入，过大的 $\beta$ 放大了估计方差，两者皆损害收敛速度。

**通信‑计算成本比 $C_A/C_R$**  
随着通信成本 $C_A$ 与局部计算成本 $C_R$ 之比增大，I‑CGM‑RG‑SAGA 的性能保持稳定，而 I‑CGM‑RG‑SVRG 出现性能退化（Figure J.5）。这一现象归因于 SVRG 的方差界含有 $1/p_B$ 因子，而 SAGA 的递归界更紧，对客户端子采样带来的波动更鲁棒。

**通信复杂度随 $n_m$ 的增长**  
实验表明，通信复杂度随 $n_m$（每轮客户端选择数）按约 $\sqrt{n_m}$ 增长，而非线性增长（Figure J.6）。这直接验证了 Corollary 5.3 和 Table 1 中通信上界对 $\sqrt{n_m}\delta_m$ 的依赖性。

### 局限与失败模式

尽管 I‑CGM‑RG‑SAGA 在通信、局部复杂度及实验性能上均占优，以下情境下其效果会削弱甚至失效：

1. **委托客户端假设**：当前设计和复杂度分析依赖一个可靠的委托客户端（客户端 1）享有较小的 $\Delta_1$。若移除该假设而改用随机客户端选择，则光滑性常数须替换为 $\Delta_{\max}$，通信与局部复杂度常数项将增大，丧失部分最优性。如何通过更精细的分析恢复接近 $\Delta_1$ 的常数仍是开放问题。

2. **SAG 估计器的固有局限**：与 SAGA 不同，SAG 估计器无法仅依赖 $\delta$ 获得方差界，必须引入个体光滑度 $L_{\max}$（已在附录 I 中证明）。因此，若用 SAG 替代 SAGA，理论界和实际性能均会退化，无法重现现有优势。

3. **超参数敏感性**：消融显示 $\lambda$ 和 $p$ 选择不当会显著损害收敛（Figure J.3, J.2）。在没有先验知识时，最优 $\lambda$ 依赖于未知常数 $\Delta_1+\sqrt{n_m}\delta_m$，这可能增加实际部署中的调参负担。

4. **深度网络中的不稳定性**：在所有神经网络实验中，控制变量方法（包括本方法）均额外引入了阻尼因子 $q$ 以增强经验性能，否则原始 SAGA/RG 更新在深层残差网络上可能出现震荡或发散。这表明在高度非凸且参数空间巨大的模型中，递归梯度估计的方差控制仍然需要辅助稳定手段，其单独作用的效果有限。

5. **通信压缩与随机 oracles**：当前未对客户端与服务器间传输信息量进行约束。若引入量化、稀疏化等压缩操作，SAGA 增量更新及 RG 递归结构的误差传播特性将发生根本变化，需要重新设计梯度估计器。同样，在仅能访问随机梯度（小批量）的场景下，理论收敛性尚未建立，需要进一步研究。

综上，I‑CGM‑RG‑SAGA 在异构联邦优化中实现了通信与局部复杂度的当前最优，且实验验证了其理论与实际高效性；但上述场景下的退化风险和开放挑战为未来工作指明了方向。

![[assets/figures/papers/iclr26_0015_FnaDv6SMd9_Non-Convex_Federated_Optimization_under_Cost-Awa/figures/022_Table_3.jpg]]
*Table 3: Table J.2: Comparisons of validation accuracy for different optimizers used in the multi-classification task for the EMNIST dataset within 100 outer iterations*

![[assets/figures/papers/iclr26_0015_FnaDv6SMd9_Non-Convex_Federated_Optimization_under_Cost-Awa/figures/034_Table_5.jpg]]
*Table 5: Table J.3: Hyper-parameters of the considered optimizers used in the multi-classification task for the CIFAR10 dataset*

![[assets/figures/papers/iclr26_0015_FnaDv6SMd9_Non-Convex_Federated_Optimization_under_Cost-Awa/figures/012_Figure_11.jpg]]
*Figure 11: Figure J.3: Comparisons of different λ used I-CGM-RG-SAGA for solving the quadratic minimization problems with non-convex log-sum penalty*

## 定位与知识库关联

本节梳理所提方法 I‑CGM‑RG‑SAGA 在联邦优化算法谱系中的定位，阐明其与现有基线方法的本质差异、适用边界、内在局限与尚未解决的开放问题。所有结论均基于正文与附录中的理论分析、消融实验和数值比对，不引入未经验证的推测。

### 1. 在联邦优化谱系中的定位与基线关系

I‑CGM‑RG‑SAGA 是一种“不精确复合梯度方法 + 递归梯度 SAGA 估计器”的联邦优化算法，其主干框架 I‑CGM（Inexact Composite Gradient Method）将分布式非凸最小化重新表述为以客户端 1 为“委托节点”的复合优化问题（Section 3）。在此基础上，梯度估计器、子问题求解器与复杂度依赖常数三个关键模块发生了根本性替换，从而在不需要周期性全同步的前提下，将通信与本地复杂度降至现有方法的最优水平（Table 1）。

**与主要基线的结构性差异**  
我们在 verified_analysis 的 `changed_slots` 中提取了四个决定算法能力的“插槽”，并在此将其与代表性基线对比，以刻画谱系关系：

1. **梯度估计器**：从传统的 SARAH（SABER‑full / SABER‑partial）、SAG（Scaffold）、SVRG 或无控制的局部 GD，演化为 **RG‑SAGA**。SAGA 本身基于客户端历史梯度的增量更新，其方差界仅依赖于函数相似度 $\delta$（而非个体平滑度 $L_{\max}$，Lemma 4.1）；叠加递归梯度（RG）后，误差界进一步收紧 $n_m$ 倍（Corollary 5.3），且无需像 SVRG 那样的全梯度快照或 SARAH 那样的周期性全同步。这一组合在实现上类似于 ZEROSARAH 的结构（Section 5），但分析中不依赖 $L_{\max}$，而是充分利用 $\delta$ 的“集体平滑”特性。

2. **子问题求解器**：基线方法通常采用固定局部步数 $K$ 或未指定终止条件；本框架引入 **Local CGM with Geometric Stopping**，即每个外循环的局部迭代步数 $K_t\sim\mathrm{Geom}(p)$（Lemma 3.4），且 $p$ 的选择显式依赖于委托客户端的平滑度 $L_1$ 和正则化参数 $\lambda$，从而在理论上保证子问题的不精确性不会破坏全局收敛速率（Theorem 3.1）。

3. **复杂度依赖常数**：几乎所有基线（如 FedAvg、Scaffold、SABER、GD）的通信或本地复杂度均依赖 $L_{\max}$、$n$ 或 $\Delta_{\max}$（最大个体差异）。I‑CGM‑RG‑SAGA 首次将复杂度控制在 $\Delta_1$（委托客户端与全局函数的差异度）与 $\sqrt{n_m}\,\delta_m$ 的量级（Table 1 通信复杂度 $\mathcal{O}\!\left(C_A n_m + C_R \frac{(\Delta_1 + \sqrt{n_m}\delta_m)F^0}{\varepsilon^2}\right)$），在统计学意义上只需“一个较好的客户端”和函数的平均相似度，而不必要求所有客户端光滑。

4. **初始全同步需求**：多数方法（如 CGM、SABER‑full、部分 SARAH 变体）需要至少一次全客户端全梯度计算才能启动；I‑CGM‑RG‑SAGA 在 $t_0=0$ 时（即完全无全梯度初始化）依然保持收敛（Appendix G, Lemma G.1，Figure J.1），从工程上排除了全同步这一昂贵约束。

上述结构性替换表明，I‑CGM‑RG‑SAGA 并非简单的组合，而是通过“委托节点 + 函数相似度 $\delta$ 驱动的方差控制 + 递归修正”这一因果机制，开辟了一条独立于 SARAH 系、SAG 系和传统 FedAvg 系的新路径。在谱系中，它处于 **利用函数相似度且支持部分客户端参与** 的分支，且是目前该分支中通信与本地复杂度均为最优的代表（Table 1）。实验部分（二次合成问题、LIBSVM、EMNIST、CIFAR10）也一致表明，其在通信效率上全面优于 Scaffold、FedAvg、SABER‑partial、SABER‑full 等基线，尤其在 $\delta$ 远小于 $L_1$ 的场景（如 mushrooms 数据集）优势达数个数量级（Figure 2）。

### 2. 适用边界

尽管理论与实验均指向所提方法的强性能，但其有效性建立在若干显式或隐式条件之上，这些条件构成了方法的适用边界，同时也是与基线比较时必须考虑的公平性前提。

- **委托客户端假设**：框架要求存在一个特殊的客户端 1，其本地函数 $f_1$ 满足 $L_1$‑光滑，且其与全局函数的差异度 $\Delta_1$ 较小。这是通信复杂度从 $L_{\max}$ 降至 $\Delta_1$ 的关键。若 $\Delta_1$ 本身很大（即客户端 1 与其他函数相似度低），则复杂度优势缩减；若通过随机选择消除委托假设，则常数退化到 $\Delta_{\max}$，失去对 $\delta$ 的精细利用（正文 Section 8 提及这一 trade‑off）。

- **函数相似度 $\delta$ 的量级**：方差缩减的效果直接受 $\delta$ 控制。当 $\delta\ll L_1$（例如 mushrooms 数据集）时，通信轮数呈数量级优势；而当 $\delta$ 与 $L_1$ 可比较（如 duke 数据集）时，增益缩小。此时本方法的通信效率仍最优，但与其他先进方法（如 MimeMVR、Scaffold）的差距取决于常数因子与调参。

- **非凸性与一阶 oracle**：所有理论限于非凸光滑目标（可能带有非凸正则项，如 log‑sum penalty），且梯度 oracle 为确定性一阶。对于随机小批量梯度（常见于深度学习实践），论文未给出保证；在 CIFAR10 / EMNIST 实验中虽表现良好（R‑G‑SAGA 精度略低于 R‑G‑SVRG，但通信效率优势仍然显著），但理论上的方差传播尚未封闭。

- **局部子问题求解的超参数**：几何分布的参数 $p$ 直接控制每次外循环的局部计算量。过大（如 $p=0.5$）会损害通信效率，过小虽节省计算但可能导致不精确性条件无法及时满足（Figure J.2）。该参数需根据问题条件离线选优，缺乏自适应机制。

- **通信成本模型**：复杂度分析采用 $C_A$（每轮激活成本）与 $C_R$（每轮数据传输成本）的抽象模型，并未结合具体网络条件（如延迟、带宽）。因此，在极高延迟的广域网中，全同步开销可能远比公式预测严重，但也可能因通信压缩的缺失而未能充分反映实际收益。

- **与 SVRG 变体的对比**：I‑CGM‑RG‑SVRG 同样是所提系列的一员，其方差界也仅依赖 $\delta$（Lemma 4.3），但受限于全梯度快照的频率 $p_B$，导致当 $C_A/C_R$ 比率增大时性能下降（Figure J.5），而 RG‑SAGA 在不同比率下保持稳定。因此，在通信预算受限但允许少量全梯度时，SVRG 变体可能仍有竞争力，但在严格限制全同步的场景中 SAGA 变体是更优选择。

### 3. 方法局限与已知失效模式

论文本身在附录与结论中明确承认了若干局限，另有一些可从理论与实验中推断的失效模式。

1. **委托单点依赖**：必须指定或随机选择一客户端作为 $f_1$，分析用 $\Delta_1$ 替代 $L_{\max}$ 优化复杂度，但若该客户端性能退化（例如其数据分布极端异质），$\Delta_1$ 可能接近甚至超过 $L_{\max}$，此时理论上不再优于依赖 $L_{\max}$ 的方法，实验上也可能出现通信效率下降。论文指出随机选择可移除该假设，但代价是回到 $\Delta_{\max}$。

2. **仅支持确定性一阶 oracle**：梯度估计器 SAGA 和 RG 的无偏性与方差界基于精确梯度计算。当引入随机抽样（小批量）时，额外的噪声会引入与批量大小相关的方差项，可能导致 RG‑SAGA 的误差界不再仅依赖 $\delta$。尚无理论指出该情况下复杂度的退化形式。

3. **通信压缩不兼容**：当前设计假设客户端与服务器之间传输完整梯度向量，未限制信息量。一旦引入量化、稀疏化或有损压缩，梯度估计器的无偏性可能被破坏（或偏离条件无偏），局部 CGM 的不精确性条件也需要重新校准。这构成与通信高效联邦学习（如 signSGD、1‑bit 压缩方法）的直接集成鸿沟。

4. **SAG 估计器的理论劣势**：尽管 SAG 与 SAGA 形似，但附录 I 已证明，SAG 在不依赖 $L_{\max}$ 的前提下无法获得与 SAGA 同阶的方差界，因此将 SAG 插入本框架不能得到复杂度最优结果。这说明方差缩减技术的选择对最终保证至关重要，也表明方法向 SAG 的简单推广是无效的。

5. **无自适应正则化参数**：λ 的选择与 $\Delta_1$、$\sqrt{n_m}\,\delta$ 强相关（Figure J.3 显示过大或过小均恶化收敛）。目前需要根据问题相关的先验常数设定，缺乏在线调整的机制，这对于真实异构场景是一大局限。

6. **客户端数量与相似度的缩放**：通信复杂度的主要项含 $\sqrt{n_m}\,\delta_m$，当客户端数 $n$ 极大而每轮采样数 $m$ 固定时，$n_m$ 增大，理论上复杂度仅以 $\sqrt{n_m}$ 增长，且图 J.6 实验验证了该缩放趋势；但若 $n$ 极大、数据高度异质（$\delta$ 可能随之增大），整体效率仍会恶化，此时需要更深入的聚类或分层策略，而论文未涉及。

### 4. 开放问题与未来方向

基于上述边界与局限，论文指出了若干亟待探索的方向，这里将其归纳并稍作延伸。

1. **多个委托客户端的推广**：当前框架仅利用一个委托客户端，是否可以通过选择多个“高质量”客户端（例如一部分具有小 $\Delta_i$ 和低通信代价的设备）构建分布式子问题求解器，进一步降低通信或局部复杂度？这需要在理论端重新定义复合分解，并分析方差控制如何适应多代理结构。

2. **随机一阶 oracle 的理论保障**：将所提估计器（SAGA、RG）与 SGD 式局部更新结合，并在非凸场景下推导收敛界，是通往实际深度学习落地的关键。目前已知 FedAvg 等缺乏方差缩减的方法在异质性下易发散，此方向若能成功，可同时获得 δ 驱动的加速与小批量的可扩展性。

3. **带通信压缩的算法协同设计**：若将传输压缩嵌入 I‑CGM，估计器的偏差‑方差特性将改变；需研究如何利用递归梯度的校正作用抵消压缩噪声，或设计新的压缩‑估计联合优化框架。可能的路线包括：将压缩视为额外的一类不精确性，纳入 I‑CGM 的误差项 $e_t$，再分析由此引发的复杂度损失是否可控。

4. **移除委托假设的精细分析**：随机客户端选择可摆脱 $\Delta_1$ 依赖，但直接得到 $\Delta_{\max}$ 常过大。能否通过对客户端分布建模（如将客户端按相似度分群）给出更紧凑的界限，使复杂度仍能以 $\Delta_{\text{avg}}$ 或 $\delta$ 主导，是保留通用性同时降低常数的重要问题。此外，如何在动态参与和节点退出场景中维护 SAGA 的增量更新表，也是实际部署中不可回避的挑战。

5. **与其他联邦方法的理论统一**：论文为不同客户端选择策略赋予了统一的成本模型（信息复杂度意义上的“方法”定义，见 Appendix C），但尚未系统性地将现有方法映射到该模型中并比较其复杂度下界。建立这样的下界框架，可明确 I‑CGM‑RG‑SAGA 所达到的最优性是否本质，以及还有多少改进空间。

综上所述，I‑CGM‑RG‑SAGA 在非凸联邦优化谱系中以其独特的“委托节点 + 函数相似度 $\delta$ + 递归梯度”设计占据了通信‑本地复杂度的前沿，但其适用性紧密依赖于委托客户端的质量、函数相似度的量级以及精确一阶 oracle 的设定，未来围绕随机梯度、通信压缩和去中心化委托的扩展，将决定该系列方法能否成长为通用联邦学习基础设施。

## 原文 PDF

![[paperPDFs/ICLR_2026/Non_Convex_Federated_Optimization_under_Cost_Aware_Client_Selection.pdf]]
