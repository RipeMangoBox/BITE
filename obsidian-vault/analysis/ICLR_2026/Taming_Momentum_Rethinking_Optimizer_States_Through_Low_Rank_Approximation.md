---
title: "Taming Momentum: Rethinking Optimizer States Through Low-Rank Approximation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Taming_Momentum_Rethinking_Optimizer_States_Through_Low_Rank_Approximation.pdf
openreview_forum_id: 9Q0dNBYeEY
aliases:
- LP
- TMROSTLRA
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "将动量矩阵分解为两个低秩矩阵的乘积（m = m_B · m_A），在保持优化动力学的同时压缩优化器状态。"
primary_logic: "指数移动平均（EMA）动量更新在数学上等价于通过在线梯度下降训练一个线性回归器，从而可以采用模型压缩技术来降低优化器的内存占用。"
claims:
- "EMA momentum updates are mathematically equivalent to training an online linear regressor with gradient descent."
- "LoRA-Pre decomposes the full momentum matrix into a compact low-rank subspace, reducing memory footprint."
- "LoRA-Pre achieves comparable or superior results using only 1/8 the rank of baseline methods, demonstrating remarkable rank efficiency."
- "C4 validation (60M) 上 perplexity (↓) = 32.57 (LoRA-Pre Adam)"
---

# Taming Momentum: Rethinking Optimizer States Through Low-Rank Approximation

> [!tip] 核心洞察
> 指数移动平均（EMA）动量更新在数学上等价于通过在线梯度下降训练一个线性回归器，从而可以采用模型压缩技术来降低优化器的内存占用。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 驾驭动量：通过低秩近似重新思考优化器状态 |
| 英文题名 | Taming Momentum: Rethinking Optimizer States Through Low-Rank Approximation |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=9Q0dNBYeEY); [GitHub](https://github.com/mrflogs/LoRA-Pre) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | LoRA-Pre |
| Dataset | C4 validation (60M), C4 validation (130M), C4 validation (350M), C4 validation (1B) |

> [!tip] 效果简介
> - C4 validation (60M) 上，perplexity (↓) 为 32.57 (LoRA-Pre Adam)，对比 34.88 (GaLore Adam)，变化 -2.31。
> - C4 validation (130M) 上，perplexity (↓) 为 23.78 (LoRA-Pre Adam)，对比 25.36 (GaLore Adam)，变化 -1.58。
> - C4 validation (350M) 上，perplexity (↓) 为 16.36 (LoRA-Pre Adam)，对比 18.95 (GaLore Adam)，变化 -2.59。

## 概述

现代自适应优化器（如 **Adam**（Kingma & Ba, ICLR 2015）、**Muon**（Jordan et al., 2024））在训练大语言模型时，需为每个可训练参数维护一阶和二阶动量状态，导致优化器内存开销与模型参数量线性增长，成为模型扩展的显著瓶颈。本文的核心洞察在于揭示：指数移动平均（EMA）动量更新在数学上等价于通过在线梯度下降训练一个线性回归器——其优化目标为动量矩阵与当前梯度之间的Frobenius范数最小化：

$$
\operatorname*{min}_{m} L(m; g) = \frac{1}{2} \cdot \|m - g\|_F^2
$$

基于这一等价性，本文提出 **LoRA-Pre**（Low-Rank Approximation for Pre-training），将动量矩阵分解为两个低秩矩阵的乘积 $m = m_B \cdot m_A$（其中 $m_B \in \mathbb{R}^{p \times r}, m_A \in \mathbb{R}^{r \times q}, r \ll \min(p,q)$），将优化器状态压缩至低秩子空间。与现有低秩优化器（如 **GaLore**（Zhao et al., 2024））依赖周期性奇异值分解（SVD）重建子空间不同，LoRA-Pre 将动量维护从根本上重新表述为在线回归任务——在每一步通过牛顿法直接演化低秩因子，实现连续的子空间自适应，并推导出无需反向传播的闭式更新规则。

在方法定位上，LoRA-Pre 属于**优化器状态压缩**路线，区别于参数高效微调方法（如 **LoRA**（Hu et al., ICLR 2022）、**DoRA**（Liu et al., 2024））和稀疏低秩混合方法（如 **SLTrain**（Han et al., 2024））。其关键调控变量为低秩分解的秩 $r$ 和动量衰减系数 $\beta_1, \beta_2$。

主要实验结果：在 C4 数据集上预训练 60M 至 1B 参数的 Llama 模型时，LoRA-Pre Adam 在所有规模上均显著优于 GaLore Adam（困惑度降低 1.58–2.59 点）；在秩效率方面，LoRA-Pre Adam 在 130M 模型上以 rank=16 即可匹配 GaLore 在 rank=256 的性能，实现 **16 倍秩效率提升**。在 Llama-3.1-8B 和 Llama-2-7B 的数学推理微调任务（GSM8K、MATH-500）上，LoRA-Pre Adam 相较标准 LoRA 分别提升 5.68 和 12.73 个百分点。理论分析表明，LoRA-Pre Adam 收敛至由低秩近似误差和内在方差共同决定的稳态邻域，其收敛上界为：

$$
\min_{1\leq t\leq T} \mathbb{E}[\|\nabla f(\theta_t)\|^2] \leq \frac{C_{init}}{\sqrt{T}} + C_{noise} (\mathcal{E}_{bound} + \sigma_{total}^2)^2
$$

方法的主要局限包括：低秩近似引入的有界误差使优化器最终停在近似最优点而非精确最优点；对极端动量衰减参数敏感（$\beta \to 1$ 时可能导致训练不稳定）；当前压缩仅覆盖注意力层和 MLP 层参数，尚未扩展至模型全部可训练部分。

## 背景与动机

### 优化器状态的内存瓶颈

现代深度学习中，自适应优化器（如 **Adam** (Kingma & Ba, ICLR 2015)）已成为训练大规模模型的标准选择。这类优化器通过维护一阶动量 $m$ 和二阶动量 $v$ 来调整每个参数的更新方向和步长，从而显著提升收敛速度和训练稳定性。然而，这种性能优势伴随着高昂的代价：**优化器状态需要为每个可训练参数存储额外的动量矩阵，导致内存占用达到模型参数本身的2倍（Adam）甚至更多**。

在大语言模型（LLM）参数规模动辄达到数十亿乃至数千亿的当下，这一开销成为制约模型扩展性的核心瓶颈。具体而言，对于一个参数矩阵 $W \in \mathbb{R}^{p \times q}$，标准 Adam 需要存储同样形状的 $m$ 和 $v$ 矩阵，内存需求为 $2pq$ 个浮点数。当模型规模从 60M 扩展到 1B 以上时，优化器状态的内存占用急剧膨胀，使得在有限 GPU 显存下训练更大模型变得极为困难。

### 现有低秩优化方法的局限

为缓解这一瓶颈，研究者提出了多种内存高效优化策略，其中**低秩优化器**通过将优化器状态投影到低维子空间来压缩内存占用，成为一条有前景的技术路线。代表性工作包括：

- **GaLore** (Zhao et al., 2024)：周期性对梯度矩阵进行奇异值分解（SVD），将动量更新限制在主导奇异向量张成的低秩子空间内。
- **Low-Rank** (Kamalakara et al., 2022)：直接对优化器状态进行低秩分解。
- **SLTrain** (Han et al., 2024)：结合稀疏性与低秩约束的混合方法。

尽管这些方法在一定程度上降低了内存开销，但它们普遍存在一个**结构性缺陷**：**子空间重建的周期性本质**。以 GaLore 为例，它每隔若干步才重新计算一次 SVD 来确定低秩子空间，而在两次重建之间，动量更新被严格限制在固定的子空间内。这种离散的子空间切换机制带来了两个问题：

1. **信息损失累积**：在子空间未更新的区间内，梯度中可能包含超出当前子空间的重要方向，这些信息被系统性丢弃。
2. **重建频率的权衡困境**：频繁重建会增加计算开销，而稀疏重建则会加剧信息损失，二者难以兼顾。

### 核心洞见：从动量更新到在线回归

本文的核心突破源于一个被忽视的数学等价性：**指数移动平均（EMA）动量更新在数学上等价于通过在线梯度下降训练一个线性回归器**。具体地，标准的一阶动量更新：

$$m \gets \beta \cdot m + (1 - \beta) \cdot g$$

可以等价地表述为求解以下最小二乘问题：

$$\min_{m} L(m; g) = \frac{1}{2} \cdot \|m - g\|_F^2$$

这一等价性揭示了动量维护本质上是一个**在线回归任务**——优化器在每个训练步都在尝试“拟合”当前梯度 $g$，而动量 $m$ 正是该回归问题的在线解。

### LoRA-Pre 的设计动机

上述等价性自然引出一个关键问题：**既然动量维护是在线回归，我们能否借鉴模型压缩领域的成熟技术来压缩优化器状态？**

这正是 LoRA-Pre 的核心动机。借鉴 LoRA (Hu et al., ICLR 2022) 在模型微调中的低秩适配思想，LoRA-Pre 将完整的动量矩阵分解为两个低秩矩阵的乘积：

$$m = m_B \cdot m_A, \quad m_B \in \mathbb{R}^{p \times r}, \; m_A \in \mathbb{R}^{r \times q}, \; r \ll \min(p, q)$$

与 GaLore 等方法的根本区别在于：**LoRA-Pre 不是在固定子空间内更新动量，而是通过在线梯度流在每一步直接演化低秩因子 $m_B$ 和 $m_A$**。这种连续的子空间自适应机制消除了周期性重建的需要，从根本上避免了信息损失累积的问题。同时，通过推导因子矩阵的闭式更新规则（基于牛顿法），LoRA-Pre 无需反向传播即可高效更新优化器状态，保证了计算效率。

简言之，LoRA-Pre 的设计目标是在**保持优化动力学质量**的前提下，通过低秩参数化实现**优化器状态的内存压缩**，并以**连续的在线更新**替代离散的子空间重建，从而突破现有低秩优化器的性能瓶颈。

## 核心创新

LoRA-Pre 的核心创新在于将优化器动量的维护重新表述为一个**在线线性回归问题**，并在此基础上对动量矩阵实施**低秩压缩**。这一思路突破了传统低秩优化器（如 GaLore）需要周期性重建子空间、在投影梯度上累积误差的局限，转而通过每一步的在线梯度流直接演化低秩因子，实现连续的子空间适配。

### 关键等价性：EMA 即在线线性回归

LoRA-Pre 的出发点是一个数学等价性：优化器中指数移动平均（EMA）的动量更新，等价于对线性回归损失执行一步梯度下降。

具体而言，标准的一阶动量更新为：

$$m_t = \beta \cdot m_{t-1} + (1 - \beta) \cdot g_t$$

该更新可被重新解释为：以动量 $m$ 为优化变量、以当前梯度 $g$ 为目标、以 $1-\beta$ 为学习率，对如下 Frobenius 范数目标执行一步梯度下降：

$$\min_m L(m; g) = \frac{1}{2} \cdot \|m - g\|_F^2$$

这一等价性意味着，**动量维护本质上是一个持续接收新梯度样本、在线更新权重的线性回归器**。该视角为后续的低秩压缩提供了直接的优化框架：既然动量是线性回归器的权重，那么对权重进行低秩分解并在线优化其因子，就自然地实现了动量压缩。

### 核心变更点：三个关键模块的重新设计

基于上述等价性，LoRA-Pre 对优化器状态进行了三个关键槽位的变更，构成了其相对于全量优化器和传统低秩优化器的本质差异。

**变更槽位一：动量存储形式——从完整矩阵到低秩因子乘积**

标准优化器（如 Adam，Kingma & Ba, ICLR 2015）存储完整的动量矩阵 $m \in \mathbb{R}^{p \times q}$，内存开销与参数矩阵规模成正比。LoRA-Pre 将其分解为两个低秩矩阵的乘积：

$$m = m_B \cdot m_A, \quad m_B \in \mathbb{R}^{p \times r}, \; m_A \in \mathbb{R}^{r \times q}, \quad r \ll \min(p, q)$$

存储开销从 $O(pq)$ 降至 $O(r(p+q))$。与 GaLore（Zhao et al., 2024）在投影子空间内存储压缩动量不同，LoRA-Pre 的低秩分解直接作用于动量本身，而非投影后的梯度，从而避免了投影误差的累积。

**变更槽位二：动量更新规则——从 EMA 到基于牛顿法的闭式更新**

将动量分解为 $m = m_B m_A$ 后，在线线性回归的目标变为：

$$\min_{m_B, m_A} L(m_B, m_A; g) = \frac{1}{2} \cdot \|m_B m_A - g\|_F^2$$

LoRA-Pre 采用牛顿法对该目标进行优化，推导出因子矩阵的闭式更新规则（Theorem 3.1），无需自动微分：

$$m_B \gets (1 - \gamma_1) \cdot m_B + \gamma_1 \cdot g m_A^T (m_A m_A^T)^{-1}$$

$$m_A \gets (1 - \gamma_1) \cdot m_A + \gamma_1 \cdot (m_B^T m_B)^{-1} m_B^T g$$

其中 $\gamma_1$ 由原始动量衰减系数 $\beta_1$ 决定（$\gamma_1 = 1 - \beta_1$）。这两个更新规则保持了 EMA 的指数衰减形式，但将更新方向从“当前梯度”替换为“当前梯度在低秩子空间中的最优投影”。这意味着**每一步都在线调整低秩子空间**，而非像 GaLore 那样每隔若干步才用 SVD 重建一次子空间——后者会导致子空间滞后于梯度流形，产生有界但不可忽略的近似误差。

**变更槽位三：二阶动量参数化——保证逐元素正性**

Adam 的二阶动量 $v$ 存储平方梯度的 EMA，用于计算自适应学习率。直接对 $v$ 进行低秩分解 $v = v_B v_A$ 无法保证分解结果的逐元素非负性，可能导致学习率计算异常。LoRA-Pre 通过重新参数化解决此问题：

$$v = (v_B v_A)^{\circ 2}$$

其中 $\circ$ 表示 Hadamard 积（逐元素平方）。对应的优化目标变为：

$$\min_{v_B, v_A} L(v_B, v_A; g) = \frac{1}{2} \cdot \|v_B v_A - |g|\|_F^2$$

这一设计天然保证 $v$ 的所有元素非负，同时保持了低秩压缩的内存效率。

### 与基线方法的本质差异

上述三个变更槽位共同定义了 LoRA-Pre 相对于基线方法的独特优势：

- **相对于 GaLore**：GaLore 在投影子空间内执行优化，需要周期性计算 SVD 来更新投影矩阵，且投影后的梯度与真实梯度之间存在信息损失。LoRA-Pre 通过在线牛顿更新直接演化低秩因子，实现了**连续的子空间适配**，避免了周期重建带来的误差累积和计算开销。
- **相对于 LoRA 及其变体**：LoRA（Hu et al., ICLR 2022）低秩适配的是模型权重增量，而非优化器状态。LoRA-Pre 的低秩压缩作用于优化器内部的动量矩阵，可与任何基于动量的优化器（Adam、Muon 等）结合，在预训练和微调场景下均适用。
- **相对于传统低秩分解方法**：传统的“先分解、后优化”策略（如 Low-Rank，Kamalakara et al., 2022）在训练初期固定低秩结构，无法适应训练过程中梯度流形的演化。LoRA-Pre 的在线更新机制使低秩子空间随训练动态调整，在更低秩的条件下即可捕获动量结构。

### 方法谱系与知识库定位

LoRA-Pre 处于**内存高效优化器**与**低秩训练方法**的交叉地带。其设计同时汲取了以下线索：

| 线索来源 | 与 LoRA-Pre 的关系 |
|---|---|
| Adam（Kingma & Ba, ICLR 2015） | 提供了动量和自适应学习率的基本框架，LoRA-Pre 在此基础上压缩优化器状态 |
| Muon（Jordan et al., 2024） | 作为另一种全量优化器，LoRA-Pre 展示了对其动量状态的通用压缩能力 |
| GaLore（Zhao et al., 2024） | 同为低秩优化器，但采用投影策略；LoRA-Pre 通过在线回归避免了其子空间重建的局限性 |
| LoRA（Hu et al., ICLR 2022） | 提供了低秩分解的范式，但作用于模型权重而非优化器状态；LoRA-Pre 在微调实验中可与 LoRA 协同使用 |
| Fira（Chen et al., 2024） | 作为 GaLore 的改进版本，LoRA-Pre 在预训练中显著优于 Fira，论文归因于避免了投影梯度带来的误差累积 |
| ReLoRA（Lialin et al., 2024） | LoRA 的预训练扩展，LoRA-Pre 在预训练场景下提供了替代性的低秩优化路径 |
| SLTrain（Han et al., 2024） | 稀疏+低秩的混合方法，LoRA-Pre 展示了纯低秩压缩在优化器状态上的竞争力 |
| LORO（Mo et al., 2025） | 低秩流形约束优化方法，与 LoRA-Pre 的在线子空间适配形成互补视角 |
| rsLoRA / DoRA | LoRA 的改进变体，LoRA-Pre 在微调实验中与这些方法进行了公平对比并取得更优结果 |

### 证据强度与待验证点

- **等价性证明**：EMA 与线性回归的等价性基于直接的代数推导，置信度极高（0.95）。该等价性是整个方法的理论基础。
- **闭式更新规则**：牛顿法推导的更新规则具有严格的数学保证（Theorem 3.1），置信度极高（0.98）。但需注意，牛顿法在非凸目标上的收敛性依赖于初始化和步长选择，论文通过将 $\gamma_1$ 与 $\beta_1$ 耦合来规避这一问题。
- **秩效率声明**：LoRA-Pre 以 1/8 的秩匹配 GaLore 性能的声明来自消融实验（Figure 2），置信度较高（0.90）。该结论在 60M 和 130M 模型上得到验证，但在更大规模模型上的可扩展性仍需进一步检验。
- **理论收敛性**：论文提供了收敛上界（Theorem C.3），表明误差由低秩近似误差和内在方差共同决定，最终收敛到有界邻域内。该理论结果确认了低秩近似的固有局限——无法精确收敛到最优点，但在实践中该邻域足够小，不影响性能优势。

## 整体框架

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9Q0dNBYeEY/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of our LoRA-Pre method. In this work, we establish a novel connection: the exponential moving average (EMA) update for optimizer momentum is mathematically equivalent to training a linear regressor using online gradient descent. Leveraging this equivalence, we propose compressing the optimizer states (i.e., the momenta) using low-rank matrices to reduce the memory footprint. Finally, the closed-form update rules for these matrices without requiring backpropagation are given by Theorem 3.1*

LoRA-Pre 的核心设计思想是将优化器动量的维护重新表述为一个**在线回归问题**，从而将模型压缩领域的低秩分解技术引入优化器状态管理。其整体流程可概括为三个关键模块的协同运作。

### 模块一：低秩动量分解模块

传统优化器（如 Adam）需为每个参数矩阵 $W \in \mathbb{R}^{p \times q}$ 存储完整的动量矩阵 $m \in \mathbb{R}^{p \times q}$，这在模型规模增大时造成显著的内存瓶颈。LoRA-Pre 的核心操作是**存储形式的改变**：将一阶动量分解为两个低秩矩阵的乘积：

$$m = m_B \cdot m_A, \quad m_B \in \mathbb{R}^{p \times r},\; m_A \in \mathbb{R}^{r \times q},\; r \ll \min(p, q)$$

同样地，二阶动量被重新参数化为 $v = (v_B v_A)^{\circ 2}$，其中 $\circ$ 表示逐元素乘积，以确保二阶动量的逐元素正性。这一分解将优化器状态的内存复杂度从 $O(pq)$ 降至 $O(r(p+q))$，构成了整个方法的内存效率基础。

### 模块二：在线线性回归优化器

仅做静态分解会导致周期性子空间重建带来的误差累积。LoRA-Pre 的关键洞察在于：**指数移动平均（EMA）动量更新在数学上等价于使用在线梯度下降训练一个线性回归器**。具体而言，标准 EMA 更新 $m_t = \beta \cdot m_{t-1} + (1-\beta) \cdot g_t$ 等价于在每一轮优化如下目标：

$$\min_{m} L(m; g) = \frac{1}{2} \|m - g\|_F^2$$

基于这一等价性，LoRA-Pre 将动量维护重新定义为一个连续的在线回归任务——优化器在每一步接收新梯度 $g$ 时，不是直接对完整动量矩阵做 EMA，而是对低秩因子 $m_B$ 和 $m_A$ 进行在线更新，使其乘积 $m_B m_A$ 逼近当前梯度。这种**逐步子空间自适应**机制避免了 GaLore 等方法中周期性 SVD 重建带来的信息损失和误差累积。

### 模块三：无反向传播的闭式更新

为保证计算效率，LoRA-Pre 推导了解析的闭式更新规则，无需自动微分。利用牛顿法求解上述低秩回归目标，得到一阶动量因子的更新公式（Theorem 3.1）：

$$m_B \gets (1 - \gamma_1) \cdot m_B + \gamma_1 \cdot g m_A^T (m_A m_A^T)^{-1}$$

$$m_A \gets (1 - \gamma_1) \cdot m_A + \gamma_1 \cdot (m_B^T m_B)^{-1} m_B^T g$$

其中 $\gamma_1$ 是由动量衰减参数 $\beta_1$ 隐式决定的等效学习率。二阶动量因子 $v_B$、$v_A$ 遵循类似规则，仅将梯度 $g$ 替换为其绝对值 $|g|$。这些更新规则在形式上保留了 EMA 的结构——当前状态与梯度信息项的凸组合——但梯度项经过了低秩子空间内的投影变换。

### 输入输出流

整体 pipeline 的输入输出流如下：

1. **输入**：当前参数梯度 $g_t$（由前向/反向传播计算获得）。
2. **一阶动量更新**：利用闭式规则更新 $m_B$、$m_A$，隐式维护低秩动量 $m = m_B m_A$。
3. **二阶动量更新**：利用闭式规则更新 $v_B$、$v_A$，隐式维护 $v = (v_B v_A)^{\circ 2}$。
4. **参数更新**：使用标准 Adam（或 Muon）的参数更新公式，将低秩动量和二阶动量代入，计算最终的参数更新量 $\Delta \theta$。
5. **输出**：更新后的模型参数 $\theta_{t+1}$ 及优化器状态 $\{m_B, m_A, v_B, v_A\}$。

值得注意的是，LoRA-Pre 是一个**优化器包装器**，可应用于任何带有动量机制的优化器（如 Adam、Muon）。在预训练中，该方法作用于注意力层和 MLP 层的参数矩阵，其余参数仍使用标准优化器。

## 核心模块与公式推导

LoRA-Pre 的核心创新在于将动量维护重新表述为**在线线性回归任务**，并通过对动量矩阵的低秩分解来压缩优化器状态。整个方法围绕三个紧密耦合的模块构建。

### 模块一：EMA与在线线性回归的等价性

传统优化器（如 Adam）中，一阶动量通过指数移动平均（EMA）更新：

$$m_t = \beta_1 \cdot m_{t-1} + (1 - \beta_1) \cdot g_t$$

LoRA-Pre 揭示了一个关键的数学等价性：上述 EMA 更新等价于对如下最小二乘目标执行一步在线梯度下降：

$$\operatorname*{min}_{m} L(m; g) = \frac{1}{2} \cdot \|m - g\|_F^2$$

其中动量 $m$ 是被优化的参数，学习率为 $1 - \beta_1$，梯度为 $m_t - g$。这一等价性将动量维护从“状态累积”转变为“在线学习问题”，为后续引入模型压缩技术提供了理论基础。

### 模块二：低秩动量分解与闭式更新

基于上述等价性，LoRA-Pre 将完整动量矩阵 $m \in \mathbb{R}^{p \times q}$ 分解为两个低秩矩阵的乘积：

$$m = m_B \cdot m_A, \quad m_B \in \mathbb{R}^{p \times r},\; m_A \in \mathbb{R}^{r \times q},\; r \ll \min(p, q)$$

对应的优化目标变为：

$$\operatorname*{min}_{m_B, m_A} L(m_B, m_A; g) = \frac{1}{2} \cdot \|m_B m_A - g\|_F^2$$

通过牛顿法推导，得到因子矩阵的**闭式更新规则**（无需反向传播）：

$$m_B \gets (1 - \gamma_1) \cdot m_B + \gamma_1 \cdot g m_A^T (m_A m_A^T)^{-1}$$

$$m_A \gets (1 - \gamma_1) \cdot m_A + \gamma_1 \cdot (m_B^T m_B)^{-1} m_B^T g$$

其中 $\gamma_1$ 由动量衰减参数 $\beta_1$ 通过耦合策略确定。这些更新规则保留了 EMA 的指数衰减形式，同时仅在低秩子空间内演化因子矩阵，从而大幅降低内存占用。

### 模块三：二阶动量的正性保持低秩分解

对于二阶动量 $v$，LoRA-Pre 采用重新参数化策略以保证逐元素正性：

$$v = (v_B v_A)^{\circ 2}$$

其中 $\circ$ 表示 Hadamard 积。对应的优化目标为：

$$\operatorname*{min}_{v_B, v_A} L(v_B, v_A; g) = \frac{1}{2} \cdot \|v_B v_A - |g|\|_F^2$$

$v_B$ 和 $v_A$ 的更新规则与一阶动量类似，分别将 $g$ 替换为 $|g|$、$\gamma_1$ 替换为 $\gamma_2$。这种平方参数化天然保证了重构后的 $v$ 元素非负，避免了传统低秩分解可能导致的符号错误。

### 收敛性保证

LoRA-Pre Adam 的理论收敛上界为：

$$\min_{1\leq t\leq T} \mathbb{E}[\|\nabla f(\theta_t)\|^2] \leq \frac{C_{init}}{\sqrt{T}} + C_{noise} (\mathcal{E}_{bound} + \sigma_{total}^2)^2$$

该上界包含两项：第一项随时间衰减至零，第二项为常数项，由低秩近似的有界误差 $\mathcal{E}_{bound}$ 和梯度的内在方差 $\sigma_{total}^2$ 共同决定。这意味着 LoRA-Pre 最终会收敛到由近似误差决定的邻域内，而非精确最优点——这是低秩压缩方法的固有局限。

## 实验与分析

### 预训练性能：低秩优化器全面对比

LoRA-Pre 在 C4 数据集上对 60M 至 1B 规模的 Llama 模型进行预训练验证，所有实验设置严格遵循 **GaLore**（Zhao et al., 2024）的配置，包括相同的学习率搜索网格、缩放因子（0.25）和训练数据量，确保公平对比。如 Table 1 所示，LoRA-Pre Adam 在所有模型规模上均显著优于现有低秩优化器：

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9Q0dNBYeEY/figures/002_Table_1.jpg]]
*Table 1: Comparison with low-rank algorithms on pre-training various sizes of Llama models on the C4 dataset. We report the validation perplexity (↓) on a hold-out C4 test set. The best and secondbest performance within the low-rank optimizers are highlighted with bold and underline. ∗ denotes the results are reproduced by ourselves*

- **60M**：LoRA-Pre Adam 达到 32.57 的验证困惑度，较 GaLore Adam 的 34.88 降低 **2.31** 点。
- **130M**：困惑度 23.78，比 GaLore Adam（25.36）低 **1.58** 点。
- **350M**：困惑度 16.36，比 GaLore Adam（18.95）低 **2.59** 点。
- **1B**：困惑度 13.53，比 GaLore Adam（15.64）低 **2.11** 点。

LoRA-Pre Adam 与 LoRA-Pre Muon 在几乎所有规模上均占据最优或次优位置，证明了该方法跨优化器泛化的能力。值得注意的是，LoRA-Pre 避免了 **Fira**（Chen et al., 2024）因投影梯度导致的误差累积问题，这解释了其相对 Fira 的持续优势。

### 微调性能：数学推理任务上的评估

在 Llama-3.1-8B 和 Llama-2-7B 上使用 MetaMath100k 数据集进行微调，并在 GSM8K 和 MATH-500 上评估（Table 2），所有方法使用统一的秩=8、学习率=2e-5 等超参数：

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9Q0dNBYeEY/figures/003_Table_2.jpg]]
*Table 2: Results of memory-efficient fine-tuning methods. We compare our method with efficient fine-tuning methods including LoRA (Hu et al., 2022), rsLoRA (Kalajdzievski, 2023), and DoRA (Liu et al., 2024), and an efficient optimizer GaLore (Zhao et al., 2024). The models are fine-tuned on the MetaMath100k (Yu et al., 2024) dataset, and evaluated on GSM8K (Cobbe et al., 2021) and MATH-500 (Lightman et al., 2024). We highlight the best performance on Adam-like optimizer and Muon-like optimizer with bold*

- **Llama-3.1-8B**：LoRA-Pre Adam 在 GSM8K 上达到 76.44% 准确率，较标准 **LoRA**（Hu et al., ICLR 2022）的 70.76% 提升 **+5.68** 点；MATH-500 上为 17.66%，略高于 LoRA 的 17.06%。平均得分 47.05，为所有 Adam 类方法中最高。
- **Llama-2-7B**：LoRA-Pre Adam 在 GSM8K 上达到 57.35%，较 LoRA 的 44.62% 大幅提升 **+12.73** 点；但在 MATH-500 上为 6.94%，略低于 LoRA 的 7.34%（−0.40 点）。平均得分 32.15，仍为最优。

MATH-500 上的微弱劣势可能源于该任务对模型深层语义理解的要求更高，低秩压缩引入的有界近似误差在此场景下影响更为显著，但整体跨模型和跨任务的增益是稳健的。

### 秩效率消融：以极低秩匹配高秩基线

LoRA-Pre 的核心优势在于其动态子空间更新机制——每一步都通过在线梯度流调整低秩因子的主方向，从而在极低秩下保持对动量结构的有效捕捉。Figure 2 的秩效率对比清晰呈现了这一特性：

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9Q0dNBYeEY/figures/005_Figure_2.jpg]]
*Figure 2: Rank efficiency comparison across efficient optimization methods. Perplexity versus rank for 60M (left) and 130M (right) models, demonstrating LoRA-Pre’s superior performance at lower ranks compared to baseline methods*

- 在 **130M** 模型上，LoRA-Pre Adam 以 **rank=16** 即可匹配 GaLore 在 **rank=256** 下的性能，实现了 **16 倍**的秩效率提升。
- 在 **60M** 模型上同样观察到显著的低秩优势，LoRA-Pre 在各秩设置下均稳定优于 GaLore。

Figure 3 进一步展示了 LoRA-Pre Muon 在不同秩设置下的训练动态，即使在受限秩条件下，模型仍能快速适应并收敛，验证了“连续子空间自适应”相较于 GaLore 类方法“周期性子空间重建”的机制优势——后者在重建间隔内子空间固定，导致优化方向与真实动量主方向逐渐偏离。

### Muon 优化器变体消融

Table 3 对比了完整 Muon、无动量 Muon、GaLore Muon 和 LoRA-Pre Muon 的预训练困惑度：

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9Q0dNBYeEY/figures/007_Table_3.jpg]]
*Table 3: Results of pre-training using different efficient Muon optimizers*

- LoRA-Pre Muon 在所有规模上均显著优于其他高效 Muon 变体：60M 上达到 30.76，较第二名提升 **3.54** 点；130M 上 23.05，提升 **1.80** 点；350M 上 16.97，提升 **0.43** 点。
- 值得注意的是，无动量 Muon 性能急剧下降，这反证了动量状态在优化中的关键作用，而 LoRA-Pre 在压缩动量的同时成功保留了其优化动力学信息。

### 超参数敏感性分析

Table 4 展示了动量衰减参数 β₁ 和 β₂ 对 LoRA-Pre Adam 在 60M 模型上的影响。方法在标准 Adam 默认值附近（β₁=0.9, β₂=0.95）表现稳定，验证了论文提出的参数耦合策略的有效性——β 直接决定了隐式学习率 γ = 1−β，从而控制低秩因子的更新步长。然而，当 β 趋近于 1 时，γ 趋近于 0，低秩因子几乎停止更新，导致训练不稳定。这一敏感性提示在实际部署中应避免使用过大的动量衰减系数。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_9Q0dNBYeEY/figures/008_Table_4.jpg]]
*Table 4: Sensitivity Analysis of Momentum Parameters $\beta$ . . We report the validation perplexity on the 60M model. The method exhibits stability around the default settings derived from standard Adam ( $\beta _ { 1 }$ = 0 . 9 , $\beta _ { 2 }$ = 0 . 9 5 ) ). Extreme values ( $\boldsymbol { \mathrm { e . g . , } } \beta \to$ 1 ) ) cause the implicit $\gamma$ to vanish, leading to training instability

### 失败模式与局限性

1. **近似误差的有界性**：理论收敛分析（Theorem C.3）表明，LoRA-Pre 的收敛上界包含由低秩近似误差和内在方差决定的常数项，意味着优化器最终会停在真实最优点的某个邻域内，而非精确收敛。这在 MATH-500 等需要精细语义建模的任务上可能表现为性能瓶颈。

2. **极端 β 值的不稳定性**：当 β→1 时，隐式学习率消失，低秩因子无法有效更新，训练可能发散。虽然默认设置下表现稳定，但这一敏感性限制了超参数搜索的灵活性。

3. **压缩覆盖范围有限**：当前 LoRA-Pre 仅应用于注意力层和 MLP 层的参数，其余参数仍使用标准优化器，尚未实现全模型优化器状态压缩。

### 待验证问题

- 在更大规模（7B、13B 以上）的预训练中，LoRA-Pre 的秩效率和性能优势是否能够保持，目前缺乏实验证据。
- 是否存在更优的低秩因子初始化策略或秩的自适应调整机制，以进一步提升收敛速度和稳定性，论文未作探讨。
- 该方法对非动量类型优化器（如纯 SGD）的扩展性仍为开放问题。

## 方法谱系与知识库定位

### 方法谱系

LoRA-Pre 处于低秩优化器与参数高效训练两条技术路线的交汇处。传统上，降低优化器内存开销的路径可大致分为两类：一类是对模型参数或梯度直接施加低秩约束的**参数高效方法**，另一类是对优化器状态本身进行压缩的**状态高效方法**。LoRA-Pre 属于后者，但其核心洞察——动量 EMA 更新与在线线性回归的等价性——使其在方法论上区别于现有工作。

#### 与参数高效方法的对比

参数高效方法通过限制可训练参数规模来间接降低优化器内存。**LoRA** (Hu et al., ICLR 2022) 将权重更新分解为低秩适配器，但优化器仍需维护适配器参数的完整动量状态。**ReLoRA** (Lialin et al., 2024) 将 LoRA 扩展至预训练场景，通过周期性合并适配器并重置优化器状态来维持低秩约束，但合并操作引入离散的子空间切换，可能导致信息丢失。**SLTrain** (Han et al., 2024) 结合稀疏与低秩结构，但同样未直接压缩优化器状态本身。LoRA-Pre 与这些方法的本质区别在于：它不限制模型参数或梯度的表达空间，而是直接压缩优化器内部维护的动量矩阵，因此理论上可与任何参数高效方法正交叠加。

#### 与状态高效方法的对比

状态高效方法直接压缩优化器的一阶和二阶动量。**GaLore** (Zhao et al., 2024) 是这条路线上的代表性工作，它周期性地对梯度矩阵进行 SVD 分解，将动量投影到主导奇异向量张成的子空间中。这一策略存在两个瓶颈：其一，SVD 的计算开销随矩阵规模增长；其二，周期性子空间重建导致动量在投影间产生误差累积。**Fira** (Chen et al., 2024) 作为 GaLore 的改进变体，尝试通过保持梯度投影的连续性来缓解误差累积，但分析表明其仍受限于投影梯度的近似误差。

LoRA-Pre 通过根本性的视角转换突破了上述限制：它将动量维护重新表述为在线回归任务，使低秩因子通过梯度流在每一步连续演化，避免了周期性子空间切换带来的信息损失。这一设计使其在秩效率上获得显著优势——在 130M 模型上，LoRA-Pre Adam 以 rank=16 即可匹配 GaLore 在 rank=256 下的性能，实现了 16 倍的秩效率提升。

#### 与不同优化器基底的适配

LoRA-Pre 的通用性体现在它可适配多种动量型优化器。论文验证了两种基底：
- **Adam** (Kingma & Ba, ICLR 2015)：将一阶动量 $m$ 分解为 $m_B m_A$，二阶动量 $v$ 重新参数化为 $(v_B v_A)^{\circ 2}$ 以保证逐元素正性。
- **Muon** (Jordan et al., 2024)：将 LoRA-Pre 的低秩压缩机制应用于 Muon 的动量状态，形成 **LoRA-Pre Muon**。

实验表明，LoRA-Pre Muon 在所有模型规模（60M 至 350M）上均优于其他高效 Muon 变体（GaLore Muon、无动量的 Muon），验证了方法的跨优化器泛化能力。

#### 与低秩流形方法的对比

**LORO** (Mo et al., 2025) 提出在低秩流形上约束优化轨迹，但其优化过程本身仍依赖完整的状态存储。LoRA-Pre 与之互补：它提供了一种在低秩流形上高效维护优化器状态的方法，而非约束优化轨迹的几何结构。

### 适用边界

1. **动量依赖**：LoRA-Pre 的核心机制建立在动量 EMA 更新与线性回归的等价性之上，因此仅适用于维护一阶/二阶动量的优化器（如 Adam、Muon 及其变体）。对于纯 SGD 或无动量自适应方法，该框架无法直接迁移。

2. **参数覆盖范围**：当前实现仅对注意力层和 MLP 层的参数应用 LoRA-Pre 压缩，其余参数（如嵌入层、LayerNorm 参数）仍使用标准优化器。这一设计选择意味着实际内存节省比例受模型架构中非压缩参数占比的影响。

3. **秩的敏感性**：低秩因子的秩 $r$ 是内存效率与近似精度之间的直接调节旋钮。消融实验表明，LoRA-Pre 在极低秩下（如 rank=16）仍能保持竞争力，但存在一个临界阈值，低于该阈值时低秩近似误差将主导优化动力学。

### 局限与开放问题

#### 已识别的局限

1. **有界近似误差**：低秩分解引入的近似误差使优化器状态与真实动量之间存在有界偏差。理论收敛分析（Theorem C.3）表明，最终收敛会停在由低秩近似误差 $\mathcal{E}_{bound}$ 和内在梯度方差 $\sigma_{total}^2$ 共同决定的邻域内，而非精确最优点。收敛上界形式为：

   $$\min_{1\leq t\leq T} \mathbb{E}[\|\nabla f(\theta_t)\|^2] \leq \frac{C_{init}}{\sqrt{T}} + C_{noise} (\mathcal{E}_{bound} + \sigma_{total}^2)^2$$

   其中第一项随时间衰减，第二项为常数残差。这意味着低秩压缩在理论上以牺牲渐进收敛精度换取内存效率。

2. **动量参数敏感性**：LoRA-Pre 将动量衰减参数 $\beta$ 与更新步长 $\gamma$ 通过耦合策略关联（$\gamma_1 = 1-\beta_1, \gamma_2 = 1-\beta_2$）。在标准 Adam 默认值（$\beta_1=0.9, \beta_2=0.95$）附近表现稳定，但极端值（$\beta \to 1$）会导致隐式步长 $\gamma$ 趋近于零，低秩因子更新近乎停滞，引发训练不稳定。这意味着超参数调优空间受到比标准优化器更强的约束。

3. **大规模验证缺失**：现有实验覆盖的最大模型规模为 1B 参数（预训练）和 8B 参数（微调）。在更大规模（如 13B、70B 及以上）的预训练场景中，LoRA-Pre 的秩效率和性能优势是否保持，尚未得到验证。

#### 开放问题

1. **非动量优化器的扩展**：EMA 与线性回归的等价性是 LoRA-Pre 的理论基石。是否可以通过建立其他优化器组件（如自适应学习率的累积梯度范数）与在线学习目标的联系，将低秩压缩范式推广至更广泛的优化器家族？

2. **自适应秩策略**：当前 LoRA-Pre 在整个训练过程中使用固定的秩 $r$。考虑到训练不同阶段动量矩阵的谱特性可能变化（初期梯度方向分散，后期趋于稳定），是否存在基于在线谱估计的自适应秩调整策略，在训练早期使用较高秩捕捉多样梯度方向，后期降低秩以节省内存？

3. **初始化策略优化**：低秩因子 $m_B, m_A$ 的初始化方式直接影响早期训练的收敛速度。当前实现使用随机初始化，是否有更优的初始化策略（如利用首批梯度的 SVD 结果）能够加速早期收敛并提升稳定性？

4. **与其他压缩技术的正交性**：LoRA-Pre 压缩优化器状态，而 GaLore 压缩梯度，LoRA 压缩参数更新。这三者在压缩对象上互不重叠，理论上可叠加使用。但三者的相互作用——特别是低秩梯度投影与低秩动量维护之间的信息瓶颈叠加效应——尚未被系统研究。

5. **理论紧致性**：当前收敛上界中的常数项 $C_{noise}$ 与低秩近似误差 $\mathcal{E}_{bound}$ 的具体依赖关系尚未被精细刻画。更紧致的理论分析可能揭示秩 $r$ 与可达收敛精度之间的定量 trade-off，为实际部署中的秩选择提供理论指导。

## 原文 PDF

![[paperPDFs/ICLR_2026/Taming_Momentum_Rethinking_Optimizer_States_Through_Low_Rank_Approximation.pdf]]
