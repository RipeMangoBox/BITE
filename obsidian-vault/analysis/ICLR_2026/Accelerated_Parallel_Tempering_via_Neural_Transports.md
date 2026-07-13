---
title: "Accelerated Parallel Tempering via Neural Transports"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Accelerated_Parallel_Tempering_via_Neural_Transports.pdf
project_link: null
code_link: null
aliases:
- APTA
- APTNT
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/probabilistic_methods
core_operator: "引入可学习的前向/后向加速器（正则化流、控制扩散、扩散模型），在相邻链之间构建更灵活的传输路径，从而增加有效分布重叠，加速参考分布与目标分布之间的通信。"
primary_logic: "通过将神经网络传输作为并行退火交换步骤的加速器，在保持PT渐近一致性的前提下，大幅提高往返行程率；同时，并行使用神经网络传输避免了单个神经采样器的计算负担和偏差问题。"
claims:
- "APT 显著提高了往返行程数（R）并保持渐近一致性，尤其在链数较少时优势更加明显。"
- "CMCD-APT 和 Diff-APT 的自由能估计方差和偏差明显低于传统 PT，且随着加速步数 K 增加进一步降低。"
- "加速交换的拒绝率可由对称 KL 散度控制，理论上保证 APT 的遍历性和 π-不变性。"
- "40-mode GMM-10 上 Round trips (R) = CMCD-APT (K=5) N=6: 1743; N=30: 6231"
---

# Accelerated Parallel Tempering via Neural Transports

> [!tip] 核心洞察
> 通过将神经网络传输作为并行退火交换步骤的加速器，在保持PT渐近一致性的前提下，大幅提高往返行程率；同时，并行使用神经网络传输避免了单个神经采样器的计算负担和偏差问题。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于神经传输的加速并行退火方法 |
| 英文题名 | Accelerated Parallel Tempering via Neural Transports |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=CODnlyYUli) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/probabilistic_methods |
| Method | Accelerated Parallel Tempering (APT) |
| Dataset | 40-mode GMM-10, DW-4 (8D), ManyWell-32 (32D) |

> [!tip] 效果简介
> - 40-mode GMM-10 上，Round trips (R) 为 CMCD-APT (K=5) N=6: 1743; N=30: 6231，对比 PT N=6: 17; N=30: 2803，变化 在少量链时提升两个数量级以上，大量链时仍接近翻倍。
> - 40-mode GMM-10 上，Compute-normalized round trips (CN-R) 为 CMCD-APT (K=1) N=6: 290.5; N=30: 2141.0，对比 PT N=6: 8.5; N=30: 1401.5，变化 考虑额外神经网络调用后仍显著优于 PT。
> - DW-4 (8D) 上，Round trips (R) 为 Diff-APT (K=5) N=5: 12456，对比 PT N=5: 2329，变化 约 5.3 倍提升。

## 概要

**问题瓶颈**：并行退火（Parallel Tempering, PT）通过多链在温度/平滑路径上交换样本实现多模态采样，但相邻退火分布之间常存在极小的密度重叠，导致交换接受率低下，需要大量平行链才能维持参考分布与目标分布间的有效通信。

**方法定位**：本文提出**加速并行退火**（Accelerated Parallel Tempering, APT），核心想法是在 PT 的相邻链交换步骤中引入可学习的神经传输（前向/后向加速器），构建更灵活的分布间传输路径，以提升重叠程度、降低交换拒绝率，同时保持经典 PT 的渐近一致性和 π‑不变性。APT 将正则化流（NF-APT）、可控蒙特卡洛扩散（CMCD-APT）与扩散模型（Diff-APT）统一纳入同一框架，通过 Metropolis-Hastings 校正避免了单独神经采样器常见的模式坍塌与偏差问题。

**核心结论**：
- APT 在保持渐近一致性的前提下，显著提高了往返行程率（round trips, R），尤其在链数较少的场景下优势明显。例如在 10 维 40‑模式 GMM 上，6 条链时 CMCD-APT (K=5) 的往返行程为 1743，而 PT 仅为 17；30 条链时 CMCD-APT 仍达到 6231，超出经典 PT 的理论上限（Table 1）。考虑神经网络额外计算开销后的计算归一化往返行程（CN-R）同样存在显著优势。
- 自由能估计实验（DW-4 与 ManyWell-32）表明，CMCD‑APT 与 Diff‑APT 的估计方差和偏差明显低于 PT，且随着加速步数 K 增加进一步降低（Figure 3）。
- 理论分析（Equation (4), Theorem 1）证明加速交换的拒绝率可由前向/后向路径测度间的对称 KL 散度控制，为训练目标设计提供了依据。

**主要结果**：在 GMM-10、DW-4（8 维）、ManyWell-32（32 维双阱系统，2¹⁶ 个模式）以及丙氨酸二肽（Alanine Dipeptide）上，不同 APT 变体均展现出比 PT 更优的往返行程与混合效率（更低的自相关时间 $\hat{\Lambda}_K$），并通过自由能估计与样本质量可视化验证了其可靠性与模式覆盖能力（Tables 1-4, Figures 1-7）。



并行退火（Parallel Tempering, PT）是采样多模态目标分布的核心方法，通过运行一系列温度递增的平行链并周期性地在相邻链间交换样本来增强对复杂空间的探索。传统 PT 的交换接受概率由相邻分布间的增量权重比决定，给出为
$$\alpha^n(x,x') := \min\left\{1, \frac{w^n(x')}{w^n(x)}\right\},\quad w^n(x) := \frac{\tilde{\pi}^n(x)}{\tilde{\pi}^{n-1}(x)}$$
（见式(1)–(2)），其中 $w^n(x)$ 本质上是相邻退火分布未归一化密度的 Radon-Nikodym 导数。当相邻分布重叠极小时，增量权重的高方差使接受率接近零，导致链间通信几近中断。为维持遍历性，通常必须大量增加平行链数目，这急剧推高计算成本并构成实际部署的主要瓶颈（Section 2.1）。

单独使用神经采样器（如正则化流、控制扩散或扩散模型）虽能灵活生成候选样本，却普遍面临系统性偏差与模式坍塌的风险，难以保证渐近一致性。例如，CMCD 和扩散采样器在脱离 Metropolis 校正时，自由能估计与期望计算均可能出现严重偏移（见 baseline description）。PT 具备严格的渐近一致性，可惜其通信效率受限于上述分布重叠问题——在仅有少数链的情况下，传统 PT 的往返行程数（round trips）极低，混合缓慢（Figure 1 右子图）。

针对这一缺口，本文提出加速并行退火（Accelerated Parallel Tempering, APT）框架。其核心动机是将可学习的前向/后向传输加速器嵌入 PT 的交换步骤，从而在不牺牲一致性的前提下大幅提高分布重叠与通信效率。具体而言，APT 将传统直接交换替换为加速路径交换（Algorithm 1, Section 3.2）：利用前向加速器从链 $n-1$ 的当前状态生成一条长度为 $K$ 的路径，利用后向加速器从链 $n$ 反向生成另一条路径，再根据路径加速增量权重 $w_K^n(x_{0:K})$（式(3)）计算 Metropolis-Hastings 接受率并交换路径端点。由于前向与后向路径测度间的对称 KL 散度上界
$$r(\mathbb{P}_K^{n-1}, \mathbb{Q}_K^n)^2 \leq \frac{1}{2}\,\mathrm{SKL}(\mathbb{P}_K^{n-1}, \mathbb{Q}_K^n)$$
控制加速交换的拒绝率（式(4), Theorem 1），通过最小化该对称 KL 训练加速器，可有效增加相邻链间的有效重叠，从而在不增加链数的前提下大幅提升往返行程数。与此同时，每一轮交换仍经过 Metropolis 校正，保证 APT 保持 PT 的 $\pi$-不变性与遍历性，避免了单独依赖神经采样器时的偏差和计算瓶颈。实验表明，在相同局部探索（单步 HMC）和相同退火路径条件下，APT 在链数极少时（如 N=6）可将往返行程数提升超过两个数量级（Table 1），并显著降低自由能估计的方差与偏差（Figure 3），为有限预算下采样复杂多模态分布提供了可行路径。



## 核心方法与创新机理

并行退火（PT）的效率瓶颈在于相邻退火链之间分布重叠极小，导致直接交换的接受率极低。传统做法依赖大量增加链数来维持通信，但这会显著提升计算负担。在该工作的框架中，作者通过将这种"直接交换"变更为**基于神经传输的加速交换**，从根本上改变了 PT 的通信机制。

### 关键变更：从直接交换到路径加速交换

标准 PT 的交换操作直接以样本点为基础，接受概率仅取决于相邻分布的增量权重比：
$$\alpha^n(x,x') := \min\left\{1, \frac{w^n(x')}{w^n(x)}\right\}, \quad w^n(x) := \frac{\tilde{\pi}^n(x)}{\tilde{\pi}^{n-1}(x)}.$$

这一设计在分布重叠极低时，接受率趋于零，导致链之间的信息传递几乎停滞。APT 保留了每条链的局部探索（仍为单步 HMC），但在通信阶段引入了**前向加速器**与**后向加速器**，分别在相邻链的当前样本之间生成长度为 $K$ 的路径。交换不再作用于单点，而是作用于整条路径的端点，其接受概率扩展为基于路径增量权重比：
$$w_K^n(x_{0:K}) := \frac{Z_n}{Z_{n-1}} \frac{\mathrm{d}\mathbb{Q}_K^n}{\mathrm{d}\mathbb{P}_K^{n-1}}(x_{0:K}).$$

其中 $\mathbb{P}_K^{n-1}$ 和 $\mathbb{Q}_K^n$ 分别为从前一链和当前链生成的前向/后向路径测度。这一变更是 APT 的核心**changed slot**：交换机制从"密度比判据"升级为"路径积分权重比判据"，从而在保持 Metropolis‑Hastings 框架的前提下，极大提升了路径间的重叠程度，显著降低交换拒绝率。Algorithm 1（Section 3.2）精确描述了该加速交换的流程。

### 理论保障：拒绝率受对称 KL 散度约束

APT 的遍历性与 $\pi$‑不变性并未因引入神经网络而丧失。Theorem 1（Section 3.2）证明了由 Algorithm 1 生成的马尔可夫链既是 $\pi$‑不变的也是遍历的。更进一步，加速交换的拒绝率可由前向/后向路径测度之间的对称 KL 散度定量控制：
$$r(\mathbb{P}_K^{n-1}, \mathbb{Q}_K^n)^2 \leq \frac{1}{2}\mathbb{P}_K^{n-1}[-\log w_K^n] + \frac{1}{2}\mathbb{Q}_K^n[\log w_K^n] =: \mathrm{SKL}(\mathbb{P}_K^{n-1}, \mathbb{Q}_K^n).$$

这意味着只要通过训练使加速器近似满足路径测度的互倒关系，即可有效压制拒绝率。换言之，**神经网络传输被用作提升分布重叠的工具，而 MH 校正则消除了训练偏差**，使得 APT 不会像纯神经采样器那样陷入模式坍塌或偏差积累。这一设计正是 APT 能够"保持渐近一致性并同时大幅加速"的根本原因。

### 实例化：三种加速器与消融验证

论文提供了三种具体的加速器实现：归一化流（NF‑APT）、控制扩散（CMCD‑APT）和扩散模型（Diff‑APT），它们均统一在最小化对称 KL 散度的训练目标下。在 40‑模态 GMM‑10 任务中（Table 1），当仅使用 6 条链时，基线 PT 的往返行程数（$R$）仅为 17，而 CMCD‑APT（$K=5$）达到 1743，提升超过两个数量级；即便考虑神经网络调用成本后的计算归一化指标 CN‑R，CMCD‑APT 仍然显著领先（290.5 vs 8.5）。消融实验进一步表明，$K$ 的增加单调提升原始 $R$，但可能影响计算归一化效率（Table 1，Figure 2），验证了加速步数是一个关键的效率调节旋钮。此外，在 DW‑4 和 ManyWell‑32 上的自由能估计实验中（Figure 3），APT 的方差和偏差均显著低于 PT，且随着 $K$ 增大而进一步改善，证实了加速路径带来的估计质量提升。

综上，APT 的核心创新在于**将神经传输作为并行退火中的"可学习通信路径"，在算法层面仅改变交换插槽，却在不牺牲渐近理论性质的前提下，将相邻链间的分布重叠问题转化为可优化的传输问题**。这一设计同时规避了单个神经采样器的偏差风险，为 PT 的效率瓶颈提供了原则性的解决方案。



![[assets/figures/papers/iclr26_0005_CODnlyYUli_Accelerated_Parallel_Tempering_via_Neural_Transp/figures/002_Figure_1.jpg]]
*Figure 1: (Left) An illustration of the local exploration and communication step for PT vs APT. (Middle) 1,000 samples of a Gaussian mixture model target obtained using PT vs APT with a standard Gaussian reference. See Appendix 6.1 for more details. (Right) Round trips for PT and APT with N = 6 chains over T = 100, 000 iterations of Algorithm 1*

Accelerated Parallel Tempering (APT) 的核心思路是在经典并行退火（PT）的局部探索步骤之后，将传统的直接交换替换为基于神经传输的加速交换。整个 pipeline 由五个模块串联构成，以下按算法执行顺序描述其输入输出流和模块关系。

**问题瓶颈**：传统 PT 的交换接受概率为 $\alpha^n(x,x') := \min\left\{1, \frac{w^n(x')}{w^n(x)}\right\}$，其中 $w^n(x) := \frac{\tilde{\pi}^n(x)}{\tilde{\pi}^{n-1}(x)}$ 为相邻分布的增量权重（Equation 1, Equation 2）。当相邻退火分布重叠极小时，接受率趋近于零，导致参考分布与目标分布之间的往返通信几乎中断，必须大量增加平行链数量才能维持有效混合。

**因果机制**：APT 引入可训练的前向/后向加速器，在相邻链之间构建长度为 $K$ 的传输路径，将交换操作从单一样本扩展至完整路径，从而增大等效分布重叠、提高交换接受率。加速交换的接受概率基于路径的加速增量权重比：

$$
\alpha_K^n(x_{0:K}, x_{0:K}') = \min\left\{1, \frac{w_K^n(x_{0:K}')}{w_K^n(x_{0:K})}\right\}
$$

其中 $w_K^n(x_{0:K}) := \frac{Z_n}{Z_{n-1}} \frac{\mathrm{d}\mathbb{Q}_K^n}{\mathrm{d}\mathbb{P}_K^{n-1}}(x_{0:K})$ 为扩展至完整路径的增量权重（Equation 3）。理论上，拒绝率由前向/后向路径测度之间的对称 KL 散度的平方控制（Equation 4, Theorem 1），因此训练目标可直接设定为最小化相邻链加速器之间的 SKL。

---

### Pipeline 模块

**1. 局部探索（Local Exploration）**
- 输入：各链当前样本 $X_t^n$
- 操作：每条退火链独立执行一步局部 MCMC 更新（统一使用单步 HMC）
- 输出：更新后的样本（仍记为 $X_t^n$）
- 出处：Section 2.1, Algorithm 1 line 3

**2. 前向加速（Forward Acceleration）**
- 输入：链 $n-1$ 的当前状态 $X_t^{n-1}$
- 操作：使用前向加速器生成一条长度为 $K$ 的路径 $\vec{X}_{t,0:K}^{n-1}$，从 $\pi^{n-1}$ 向 $\pi^n$ 方向传输
- 输出：前向路径及其增量权重
- 出处：Algorithm 1 line 7

**3. 后向加速（Backward Acceleration）**
- 输入：链 $n$ 的当前状态 $X_t^n$
- 操作：使用后向加速器反向生成一条长度为 $K$ 的路径 $\overleftarrow{X}_{t,0:K}^{n}$，从 $\pi^n$ 向 $\pi^{n-1}$ 方向传输
- 输出：后向路径及其增量权重
- 出处：Algorithm 1 line 8

**4. 加速交换接受（Accelerated Swap Acceptance）**
- 输入：前向路径 $\vec{X}_{t,0:K}^{n-1}$ 与后向路径 $\overleftarrow{X}_{t,0:K}^{n}$ 的增量权重
- 操作：计算路径端点的加速增量权重比，以 Metropolis-Hastings 接受率决定是否交换端点样本
- 输出：交换决策及更新后的链状态
- 出处：Algorithm 1 lines 12-13, Section 3.2

**5. 自由能估计（Free Energy Estimation）**
- 输入：前向/后向路径的权重
- 操作：利用路径权重构造一致的自由能差估计量（Bennett acceptance ratio 类型）和归一化常数估计量
- 输出：自由能差 $\Delta F$ 的无偏/渐近一致估计
- 出处：Section 3.2, Proposition 1

---

### 关键设计选择

**并行使用 vs 独立采样**：APT 将神经传输作为交换加速器并行部署在多个退火链之间，而非依赖单个神经采样器独立产生样本。这一策略避免了 CMCD、扩散模型等神经采样器的模式坍塌和渐近偏差问题（Figure 4 提供了 DW-4 上的对比证据），同时通过 Metropolis 校正保障 $\pi$-不变性和遍历性（Section 3.2, Appendix B.1.1）。

**加速器多样性**：框架支持三类可互换的加速器——正则化流（NF-APT）、条件马尔可夫链扩散（CMCD-APT）和扩散模型（Diff-APT），分别在 5.1-5.3 节中给出具体的前向/后向参数化与增量权重公式。训练均以相邻链之间的对称 KL 散度为目标（Equation 4），而采样效率的直接优化仍是开放问题。

**输入输出总览**：整个 APT 循环以 $N$ 条链的当前样本为输入，依次执行局部探索与前向/后向加速，仅在加速交换步骤产生跨链数据流，最终输出更新后的链样本及可选的自由能估计。框架保持了经典 PT 的两阶段结构（局部更新 + 通信交换），仅在通信阶段以路径级传输替换了直接样本交换。



### 加速交换机制

并行退火（PT）的瓶颈在于相邻退火分布之间重叠极小，导致直接交换样本的接受率过低。APT 在传统 PT 的局部探索与交换步骤之间插入了一对**前向 / 后向加速器**，在相邻链之间构造长度为 $K$ 的传输路径，交换路径端点而不是原始样本，从而大幅度提高交换接受率和混合速度。

APT 的一次迭代包含以下关键模块（Algorithm 1）：

- **局部探索**：每条链独立执行一步局部 MCMC 更新（本文统一使用单步 Hamiltonian Monte Carlo，HMC），保证各链的边缘分布保持 $\pi^n$‑不变性。
- **前向加速**：利用前向加速器 $T^n$（或更一般的随机传输）从链 $n-1$ 的当前状态出发，生成一条长度为 $K$ 的前向路径 $x_{0:K}$；该路径对应的测度为 $\mathbb{P}_K^{n-1}$。
- **后向加速**：利用后向加速器从链 $n$ 的当前状态反向生成一条长度为 $K$ 的后向路径 $x'_{0:K}$；该路径对应的测度为 $\mathbb{Q}_K^n$。
- **加速交换接受**：计算两条路径的**加速增量权重**比值，以 Metropolis‑Hastings 接受率决定是否交换路径的端点；若接受，则链 $n-1$ 的下一样本变为 $x'_K$，链 $n$ 变为 $x_K$。
- **自由能估计**：利用前向 / 后向路径的权重构造一致的自由能差估计量（Proposition 1），用于后续分析而不引入额外偏差。

此设计使得 APT 在保持 PT 渐近一致性的前提下，通过增加相邻链分布的有效重叠，显著提升往返行程数 $R$（尤其在少链条件下优势明显，Table 1），同时并行使用神经传输避免单个神经采样器的模式坍塌和偏差问题。

### 关键公式与变量含义

**1. 增量权重（incremental weight）**  
$$ w^n(x) := \frac{\tilde{\pi}^n(x)}{\tilde{\pi}^{n-1}(x)} $$  
其中 $\tilde{\pi}^n$ 表示未归一化的退火目标密度，$x$ 是样本点。该比值是相邻分布之间未归一化的 Radon–Nikodym 导数，传统 PT 的交换接受概率即由该比值决定。

**2. 加速增量权重（accelerated incremental weight）**  
$$ w_K^n(x_{0:K}) := \frac{Z_n}{Z_{n-1}} \frac{\mathrm{d}\mathbb{Q}_K^n}{\mathrm{d}\mathbb{P}_K^{n-1}}(x_{0:K}) $$  
将权重概念从单点扩展到完整路径。其中 $\mathbb{P}_K^{n-1}$ 是前向加速器产生的路径测度，$\mathbb{Q}_K^n$ 是后向加速器产生的路径测度，$Z_n/Z_{n-1}$ 是归一化常数之比。该权重用于加速交换的接受率计算。

**3. 加速交换接受概率**  
$$ \alpha_K^n\bigl(x_{0:K},\,x'_{0:K}\bigr) = \min\!\left\{1,\; \frac{w_K^n(x'_{0:K})}{w_K^n(x_{0:K})}\right\} $$  
取 1 与两个路径的加速增量权重之比的最小值。与传统 PT 类似，但当 $K>0$ 时权重被定义在路径空间上，导致接受概率通常远高于直接交换。

**4. 对称 KL 散度控制交换拒绝率**  
$$ r(\mathbb{P}_K^{n-1},\,\mathbb{Q}_K^n)^2 \,\leq\, \frac12\,\mathbb{P}_K^{n-1}\bigl[-\log w_K^n\bigr] + \frac12\,\mathbb{Q}_K^n\bigl[\log w_K^n\bigr] \,\equiv\, \mathrm{SKL}(\mathbb{P}_K^{n-1},\,\mathbb{Q}_K^n) $$  
交换的拒绝率由前向 / 后向路径测度之间的**对称 KL 散度**的平方所控制。这一不等式为训练加速器提供了直接目标：最小化相邻链路径测度的对称 KL 散度（即最小化上述右端），即可系统性地降低交换拒绝率、提升通信效率。

加速器的具体实现（正则化流 NF‑APT、条件马尔可夫链扩散 CMCD‑APT、扩散模型 Diff‑APT）均通过参数化路径测度并最小化对应的对称 KL 散度来训练，详见表 1 与 Section 5；其增量权重的具体形式依赖于所选传输类型（例如 NF‑APT 的增量权重还包含 Jacobian 行列式项，CMCD‑APT 则基于正向/反向转移密度之积）。但这些细节不在本节展开，本节仅聚焦 APT 框架的通用核心公式。



## 实验与关键发现

并行退火（PT）的效率瓶颈在于相邻退火分布间重叠极小，导致交换接受率很低，需大量增加平行链才能维持通信。APT 通过引入可学习的前向/后向神经网络加速器（正则化流、控制扩散、扩散模型）在相邻链间构建更灵活的传输路径，直接扩大有效分布重叠，显著提升往返行程数（R）并保持渐近一致性。以下主要结果涵盖四类合成基准与一个分子体系，消融实验系统剥离加速步数、加速器类型的影响，最后总结已知局限与需要人工校验的边界条件。

### 主结果：往返通信效率与采样质量大幅提升

在 40-模态 10 维高斯混合模型（GMM-10）上，**CMCD-APT 在极少链数时将通信效率提高两个数量级以上**。N=6 链时，PT 仅实现 R=17，而 CMCD-APT（K=5）达到 R=1 743；N=30 链时，二者分别为 2 803 和 6 231（Table 1）。即使考虑额外神经网络调用，按计算归一化往返行程（CN-R）衡量，CMCD-APT（K=1）在 N=6 时达到 290.5，仍远超 PT 的 8.5。**Diff-APT 在高维及离散对称体系上优势突出**：8 维 DW-4 簇目标中，Diff-APT（K=5）在 N=5 链下实现 R=12 456，约对应 PT（R=2 329）的 5.3 倍（Table 4）；32 维 ManyWell-32 上，CMCD-APT（K=5）在 N=5 时 R=2 878，而 PT 仅 550（Table 3）。在丙氨酸二肽体系中，**CMCD-APT（K=5）将积分自相关时间 Λ̂_K 从 PT 的 3.38 降至 3.09**，同时 R 从 199 提升至 627，表明分子构象空间的混合更快（Table 2）。

![[assets/figures/papers/iclr26_0005_CODnlyYUli_Accelerated_Parallel_Tempering_via_Neural_Transp/figures/003_Table_1.jpg]]
*Table 1: PT versus APT with different acceleration methods, targeting a 40-mode Gaussian Mixture model (GMM-10) target in 10 dimensions and standard Gaussian reference using N = 6, 10, 30 parallel chains for T = 1 0 0 , 000 iterations. For each method, we report the round trips (R), round trips per target evaluation, denoted as compute-normalised round trips (CN-R), the number of neural network evaluations per parallel chain every iteration (Neural Calls), and $\Lambda _ { K }$ estimated using N = 3 0 chains ( $\hat { \Lambda } _ { K }$ )

![[assets/figures/papers/iclr26_0005_CODnlyYUli_Accelerated_Parallel_Tempering_via_Neural_Transp/figures/064_Table_3.jpg]]
*Table 3: PT versus APT with different acceleration methods, targeting ManyWell-32 in 32 dimensions and standard Gaussian reference using N = 5, 10, 30 parallel chains for T = 1 0 0 , 000 iterations. For each method, we report the round trips (R), round trips per target evaluation, denoted as computenormalised round trips (CN-R), the number of neural network evaluations per parallel chain every iteration (Neural Calls), and $\Lambda _ { K }$ estimated using N = 30 chains ( $\hat { \Lambda } _ { K }$ )

![[assets/figures/papers/iclr26_0005_CODnlyYUli_Accelerated_Parallel_Tempering_via_Neural_Transp/figures/065_Table_4.jpg]]
*Table 4: PT versus APT with different acceleration methods, targeting DW-4 in 8 dimensions and standard Gaussian reference using N = 5, 10, 30 parallel chains for T = 100, 000 iterations. For each method, we report the round trips (R), round trips per target evaluation, denoted as computenormalised round trips (CN-R), the number of neural network evaluations per parallel chain every iteration (Neural Calls), and $\Lambda _ { K }$ estimated using N = 3 0 chains ( $\hat { \Lambda } _ { K }$ )

**自由能估计质量同样得到本质改善**。Figure 3 显示 DW-4 和 ManyWell-32 上 CMCD‑APT、Diff-APT（K≥1）的自由能差 ΔF 箱线图方差显著小于 PT，且随加速步数 K 增大偏差进一步降低；与之对比，PT 估计量存在明显偏差与大方差。样本质量比较（Figure 4）表明，**单独的神经采样器（CMCD、Diffusion）会出现模式坍塌或权重偏差，而 APT 系列方法因保留了 Metropolis 校正，始终能恢复正确的模式权重，且与基准 PT（60 链）生成的原子间距分布高度一致**。在 ManyWell-32 的定性验证中，CMCD-APT（Figure 5）和 Diff-APT（Figure 6）经 1 000 步连续采样即可产生与独立真实样本（Figure 7）视觉一致的阱间分布，表明加速传输未牺牲遍历性。

![[assets/figures/papers/iclr26_0005_CODnlyYUli_Accelerated_Parallel_Tempering_via_Neural_Transp/figures/005_Figure_3.jpg]]
*Figure 3: Estimates of ∆F for DW4 and ManyWell-32 by PT, CMCD-APT ( K = 1 , 2 , 5 ) and Diff-APT ( K = 0 , 1 , 2 , 5 ) using 1,000 samples. Each box consists of 30 estimates. The black dashed lines denote the reference constant $\Delta$ F ≈ 29.660 estimated with PT using 60 chains and 100,000 samples and $\Delta$ F ≈ 164.696 from Midgley et al. (2023) for ManyWell-32

![[assets/figures/papers/iclr26_0005_CODnlyYUli_Accelerated_Parallel_Tempering_via_Neural_Transp/figures/009_Figure_4.jpg]]
*Figure 4: Interatomic distance d _ { i j } of 5,000 samples by CMCD, CMCD-APT, Diffusion, Diff-APT with 30 chains, K = 1 , 2 , 5 on DW4. We take 100,000 samples by PT with 60 chains as ground truth*

综上，APT 在保持 PT 渐近一致性的前提下，同时实现了更大的往返行程数、更小的自相关时间、更准确且低方差的自由能估计，并避免了单独神经采样器的偏差，这些提升在链数较少时尤为显著，缓解了原瓶颈对链数的严重依赖。

### 消融实验：加速步数与加速器类型的影响

**加速步数 K 单调提升原始往返行程数 R，但计算归一化往返行程 CN-R 可能因神经网络调用增多而下降**（Table 1, Figure 2）。例如 CMCD-APT 在 N=30 时，K 从 1 增至 5，R 由 3 433 升至 6 231，而 CN-R 则从 2 141.0 降至 1 038.5（Table 1）。高维情况下 Diff-APT 的增益更为明显：Figure 2 显示维度 d 从 2 增至 100，Diff-APT 的往返速率相对 PT 的提升随 d 增大，且 K 较大时优势维持，表明神经传输能更有效地对抗维数灾难造成的分布重叠消失。

**不同加速器在不同体系上的计算‑效率权衡有所差异**。NF-APT 在 GMM-10 上 N=6 时达到 R=194、CN-R=97.0，为一次流映射下的低成本方案；CMCD-APT 在同等计算预算下通常获得更高的 CN-R（Table 1）；Diff-APT 在 DW-4 上原始 R 最高（Table 4）。剥离传输加速的变体 Diff-PT（K=0）在多数情况下仅略优于 PT 或持平，说明 **主要增益来源于可学习的传输映射，而非退火路径的选择**（Table 1, Table 4）。

### 局限与已知失败模式

尽管 APT 在多数基准上表现优异，但存在以下明确局限，需要在实际部署中加以校验：

1. **离线训练依赖**：前向/后向加速器需额外训练，训练目标为对称 KL 散度最小化。该目标与最终往返效率之间的关系仅在理论上保证拒绝率的上界（Equation (4)），但尚未被完全表征，在某些能量景观下可能出现训练良好但加速效果不明显的脱节，需对特定任务进行手动验证。
2. **基准范围有限**：当前实验仅覆盖合成多模态分布（GMM、MW-32、DW-4）和简单分子（丙氨酸二肽），未在大规模生成模型、离散变量空间或真实物理系统中验证。对这些更复杂的应用场景，加速映射的学习是否会引入难以诊断的数值问题仍属未知。
3. **极端多模态时的链数需求**：对于具有极大 log-Sobolev 常数或极深阱的分布，即便使用加速交换，APT 仍可能需要较多平行链才能建立有效通信。此时神经传输的优势可能被削弱，链数‑效率的权衡需要根据具体实例重新评估。

上述局限性提示：当将 APT 从基准推广至全新问题时，应优先检查往返行程数与自由能估计的一致性，谨慎解读仅基于训练损失得出的表现预期。



## 定位与知识库关联

APT 的底层仍然是并行退火（PT）框架：每个退火链独立执行局部探索（单步 HMC），链间通过随机交换通信。与传统 PT 的区别仅在于**交换机制**——标准 PT 直接交换相邻链的当前样本，接受概率为

$$
\alpha^n(x,x') := \min\!\left\{1,\ \frac{w^n(x')}{w^n(x)}\right\},
\quad w^n(x) := \frac{\tilde{\pi}^n(x)}{\tilde{\pi}^{n-1}(x)} ;
$$

APT 则在前向/后向神经加速器上生成长度为 $K$ 的路径，交换路径端点，接受概率由**加速增量权重** $w_K^n(x_{0:K})$ 决定。这一替换等价于扩展了交换的路径空间，因而理论上只要合理设计加速器，就能增加相邻链的有效重叠、提高往返行程率，同时保留 PT 的渐近一致性和遍历性（Theorem 1）。

### 与已有基线的关系及剥离证据

- **Standard PT（主要基线）**：在相同链数、相同 HMC 局部探索和相同的退火路径下对比。表 1 显示，当链数 $N=6$ 时，标准 PT 在 GMM-10 上的往返行程数（R）仅为 17，而 CMCD-APT（$K=5$）达到 1743，对少量链的通信效率提升超过两个数量级；$N=30$ 时仍有近翻倍的增益。计算归一化往返行程（CN-R）在扣除额外神经网络开销后依然显著更好。
- **Diff-PT（$K=0$）**：使用扩散定义的退火路径（无传输加速）作为对比，目的是剥离路径选择本身的影响。图 2/表 1 显示 Diff-PT 的增益明显小于真正的 APT，说明通信加速主要来自神经传输，而非更优的退火路径。
- **纯粹神经采样器（CMCD、Diffusion）**：单独使用时面临模式坍塌或分布偏差。图 4 在 DW-4 上表明，CMCD 和 Diffusion 产生的分子间距离分布与 PT 真值存在系统性偏差，而 CMCD-APT 和 Diff-APT（$K\ge1$）经过 Metropolis-Hastings 校验后对模式权重的恢复与真值一致。这证实 APT 通过 MH 校正规避了单样本神经采样器的偏差问题。

### 适用边界与已知局限

1. **训练成本与 mAP 解耦**：所有 APT 变体需要额外离线训练前向/后向加速器。训练目标（对称 KL 散度）虽能理论控制拒绝率（式 4），但其与最终混合性能（如往返行程率）的定量关系尚未完全建立，因此无法保证训练最优直接等价于采样最优。
2. **验证场景受限**：当前实验均在合成分布（GMM、MW-32、DW-4）和小分子丙氨酸二肽上进行。在大规模生成模型、物理/化学领域真实后验或高维结构化问题中，未提供经验证据。
3. **极端模态下的退化风险**：当目标分布具有极大 log-Sobolev 常数时，相邻退火分布间的固有重叠极低，即便使用加速器也可能需要大量平行链才能维持有效通信。论文自身指出 APT 仍可能面临链数膨胀的需求，说明神经传输的补偿能力有限。
4. **加速步数 $K$ 的折衷**：消融实验（Table 1, Figure 2）显示，增大 $K$ 单调提升原始往返行程数，但计算归一化往返行程（CN-R）会因神经网络调用次数增加而下降；最优 $K$ 需按具体算力权衡。

### 未决问题与拓展方向

- **在线训练策略**：能否在采样进行中持续更新传输映射，实现"采样即训练"，从而提升在局部探索分布漂移下的自适应能力？
- **更直接的优化目标**：是否可直接以 APT 的 MH 接受率或链间混合指标作为损失函数，替代当前使用的对称 KL 散度，以获得对采样效率更精确的优化？
- **非连续与非欧空间的扩展**：当前 APT 要求前向/后向加速器定义在连续路径空间上（NF、SDE 离散化），其在离散变量、图结构或非欧几里德空间中的适用性尚属开放，是否可借由连续松弛或跳跃过程搬运？
- **鲁棒性判据与混合式策略**：在何种条件下应回退至标准 PT 以避免神经传输训练失败引入的额外计算？发展判定准则并构建自适应调度（例如仅在高层链启用加速）可能是实用的补充。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Accelerated_Parallel_Tempering_via_Neural_Transports.pdf

![[paperPDFs/ICLR_2026/Accelerated_Parallel_Tempering_via_Neural_Transports.pdf]]
