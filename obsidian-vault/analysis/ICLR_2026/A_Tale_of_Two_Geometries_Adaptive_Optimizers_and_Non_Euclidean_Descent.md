---
title: "A Tale of Two Geometries: Adaptive Optimizers and Non-Euclidean Descent"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Tale_of_Two_Geometries_Adaptive_Optimizers_and_Non_Euclidean_Descent.pdf
project_link: null
code_link: null
aliases:
- WSPSA1
- TTGAONED
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "引入自适应光滑性（Λ_ℋ(f)）和自适应梯度方差（σ_ℋ）作为更强的结构化假设，分别催化加速收敛和维度无关收敛。"
primary_logic: "自适应优化器与归一化最速下降虽然都能利用非欧几何，但它们依赖的光滑性/噪声概念不同；自适应光滑性和自适应方差虽然更严格，却能换取加速率和维度无关的收敛保证，揭示了自适应性与几何之间的深层联系。"
claims:
- "非凸设置下，自适应优化器的收敛速度由自适应光滑性 Λ_ℋ(f) 控制，达到最优 Õ(T⁻¹/⁴)。"
- "利用自适应光滑性，带 Nesterov 动量的自适应优化器可在凸情形实现加速收敛 O(T⁻²)，而 ℓ∞ 标准光滑性下所有算法的最坏收敛阶为 Ω(T⁻¹)。"
- "自适应梯度方差使归一化最速下降（NSD）获得与维度无关的收敛上界。"
- "在标准梯度方差假设下，signGD（ℓ∞-NSD）的收敛下界明确依赖于维度 d，证明维度无关速率不可达到。"
---

# A Tale of Two Geometries: Adaptive Optimizers and Non-Euclidean Descent

> [!tip] 核心洞察
> 自适应优化器与归一化最速下降虽然都能利用非欧几何，但它们依赖的光滑性/噪声概念不同；自适应光滑性和自适应方差虽然更严格，却能换取加速率和维度无关的收敛保证，揭示了自适应性与几何之间的深层联系。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 两种几何的故事：自适应优化器与非欧几里得下降 |
| 英文题名 | A Tale of Two Geometries: Adaptive Optimizers and Non-Euclidean Descent |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=iaoAKDRAJQ) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | 统一自适应优化器框架（Well-Structured Preconditioner Set, Algorithm 1） |
| Dataset |  |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

自适应优化器（如 Adam、Shampoo、Lion）在深度学习实践中表现优异，但其加速行为和维度无关性难以用标准光滑性和标准梯度方差假设解释。本文揭示：这一困境源于**标准光滑性假设无法刻画非欧几何下自适应优化器收敛的精细结构**。为此，文章引入两个更具表达力的结构化假设——**自适应光滑性 Λ_ℋ(f)** 和**自适应梯度方差 σ_ℋ**，分别催化加速收敛和维度无关收敛。

核心结论：
- **方法统一**：通过定义良构前置条件集 (well‑structured preconditioner set) ℋ，将 AdaGrad、Adam、Shampoo、Lion、Muon 等优化器归入统一框架（Algorithm 1），其本质是归一化最速下降 (NSD) 的推广。
- **加速收敛**：利用自适应光滑性，带 Nesterov 动量的自适应优化器在凸设定下实现 **Õ(T⁻²)** 加速速率（Theorem 4.3），而 ℓ∞ 标准光滑性下的最坏收敛阶仅为 **Ω(T⁻¹)**。
- **维度无关收敛**：自适应梯度方差使 NSD 获得与维度无关的上界（Theorem 4.5）；相反，在标准梯度方差下 signGD（ℓ∞‑NSD）的下界明确依赖维度 **d**（Theorem 4.7），证明维度无关性是自适应方差假设带来的本质改进。
- **非凸保证**：在非凸设定下，收敛速度由自适应光滑性 Λ_ℋ(f) 控制，达到最优速率 **Õ(T⁻¹/⁴)**（Theorems D.2, D.7, D.8）。

方法定位：本文属于理论分析工作，不引入新优化器，而是通过**替换光滑性假设和方差假设**（从标准 L、σ 到自适应 Λ_ℋ、σ_ℋ）更精准地刻画已有自适应算法的收敛性质。实验部分需另行查阅以验证理论与实践的吻合度。



自适应优化器（如 Adam、Lion、Muon）在实践中凭借其适应梯度结构的能力取得了巨大成功，但关于它们为何有效、收敛速度能否突破标准光滑性假设给出的障碍，一直缺少清晰的统一理论。问题的核心在于：**标准光滑性（$L_{\|\cdot\|}(f)$）和标准梯度方差假设建立在固定的范数结构之上，而自适应方法天然地在迭代过程中动态改变度量，这种“非欧几里得下降”的行为无法被传统光滑性概念所刻画**。在标准假设下，即使使用 Nesterov 动量，凸情形的最坏收敛率也被下界 $\Omega(T^{-1})$ 限制，而提升到加速率 $O(T^{-2})$ 需要更强的结构化条件。

已有工作通常将自适应优化器理解为某种归一化最速下降（NSD）的近似，在不同范数下对应不同具体算法（例如 SignGD 对应 $\ell_\infty$‑NSD，Lion 被视为其等价形式，Muon 则在矩阵谱范数下工作）。若沿着这条思路前进，NSD 的收敛速率由所选矩阵 $\mathbf{H}$ 诱导的范数光滑性 $L_{\|\cdot\|_{\mathbf{H}}}(f)$ 控制（见公式 (2)）。但对一个前置条件集 $\mathcal{H}$ 中的不同矩阵，这些系数可能差异极大；直接最小化不同 $\mathbf{H}$ 下的 NSD 速率，就能自然得到自适应光滑性的雏形。例如，对于对角线矩阵族，有

$$
\inf_{\substack{\mathrm{diagonal}\,\mathbf{H}\succeq 0\\ \mathrm{Tr}(\mathbf{H})\le 1}} L_{\|\cdot\|_{\mathbf{H}}}(f)
$$

这一量值就是对角线自适应光滑性 $L_{\mathrm{diag}}(f)$ 的来源，它比全局 ℓ∞ 光滑性更精细。这说明**自适应优化器实际上在寻找一个“最有利的局部度量”，使得在该度量下目标函数的光滑性尽可能小**。前述观察构成了本文提出**自适应光滑性 $\Lambda_\mathcal{H}(f)$**（Definition 2.4）的动机：将上述下确界形式化为一个统一的结构假设，衡量在 $\mathcal{H}$ 约束下能达到的最佳光滑程度。

对应地，随机梯度的噪声结构也可以被自适应度量更精确地控制。传统梯度方差 $ \sigma^2 $ 与维度 $d$ 同时出现在收敛界中，导致维度依赖性；而**自适应梯度方差 $\sigma_\mathcal{H}$**（Definition 4.1）刻画了在 $\mathcal{H}$ 的几何下噪声的尺度。这意味着，如果实际噪声结构恰好与前置条件集的几何兼容，就可以获得与维度无关的收敛保证。这一思想直接回应了一个现有关键缺口：Jiang et al. (2025) 虽然在 SignGD 上获得了类似维度无关的结果，但其噪声假设更强且仅限于特定算法；本文需要用一个更弱、更一般的概念统一处理各种自适应方法。

由此，本文的核心动机可以概括为两个待验证的猜想：(1) 自适应光滑性是否足够强、并且在实际中仍然成立，从而催生加速自适应算法；(2) 自适应梯度方差能否一般地解释归一化最速下降（以至于更多自适应优化器）的维度无关性质。如果这些猜想成立，那就能建立起**“几何—光滑性/方差—收敛率”的三角对应**，为自适应优化器的设计提供超越启发式动机的理论基础。



## 核心方法与创新机理

现有优化理论中，标准光滑性（$L_{\|\cdot\|}(f)$）和标准梯度方差（$\sigma_{\|\cdot\|_*}$）假设无法刻画非欧几何下自适应优化器的加速行为与维度无关收敛。该工作的核心突破在于引入一对更具表达力的结构化假设——**自适应光滑性**（Adaptive Smoothness，$\Lambda_{\mathcal{H}}(f)$）和**自适应梯度方差**（Adaptive Gradient Variance，$\sigma_{\mathcal{H}}$）——它们分别催化加速收敛与维度无关的收敛，并揭示出自适应性与几何之间的深层联系。

### 假设层面的关键槽位改变

相对以 NSD (Normalized Steepest Descent)、SignGD、Lion、Muon 等为代表的基线，该工作改变了两个核心假设槽位：

| 槽位 | 基线取值 | 创新取值 |
|------|----------|----------|
| **光滑性假设** | 标准光滑性 $L_{\|\cdot\|_{\mathcal{H}}}(f)$ | 自适应光滑性 $\Lambda_{\mathcal{H}}(f) = \min_{H\in\mathcal{H},\, \mathrm{Tr}(H)\le 1} L_{\|\cdot\|_{H}}(f)$ （Definition 2.4, Eq (5)） |
| **梯度方差假设** | 标准梯度方差 $\sigma_{\|\cdot\|_{\mathcal{H},*}}$ | 自适应梯度方差 $\sigma_{\mathcal{H}}$ （Definition 4.1, Proposition B.11） |

**自适应光滑性**定义为允许所有合法前置条件矩阵 $H$ 的最低光滑性：  

$$
\Lambda_{\mathcal{H}}(f) := \min_{H\in\mathcal{H},\, \mathrm{Tr}(H)\le 1} L_{\|\cdot\|_{H}}(f),
$$
  
本质上是对目标函数非欧结构的更精细测量——它总是大于或等于标准光滑性，但能换取更强的收敛保证。**自适应梯度方差**是其对偶概念，刻画梯度噪声在非欧几何下的自适应散射程度，并有上界 $\sigma_{\mathcal{H}}^2 \le \operatorname{Tr}(P_{\mathcal{H}}(\Sigma))$（Proposition B.10）。

### 理论催化与决定性的证据

两项改变直接催化了三类此前无法获得的理论保证：

1. **非凸最优速率**：在自适应光滑性下，通用自适应优化器（Algorithm 1）达到 $\tilde{O}(T^{-1/4})$，匹配非凸优化的信息论下界（Theorem D.2 等）。标准光滑性无法给出此类与几何相关的精细速率。

2. **凸设置下的加速**：利用 Nesterov 加速方案，自适应优化器在 $\Lambda_{\mathcal{H}}(f)$ 下获得  
   
$$
\mathbb{E}[f(\bar{x}_T)-f(x^*)] = \tilde{O}\!\left(\frac{\Lambda_{\mathcal{H}}(f) D^2 \log^2 d + d\sqrt{\epsilon}D}{T^2} + \frac{\sigma_{\mathcal{H}} D \log d}{\sqrt{T}}\right),
$$
  
   即确定项速率 $\tilde{O}(T^{-2})$（Theorem 4.3）。与之对照，在 $\ell_\infty$ 标准光滑性下，所有算法的下界为 $\Omega(T^{-1})$——自适应光滑性突破了这一屏障。

3. **维度无关收敛与不可达性下界**：在自适应方差假设下，NSD 获得与维度无关的上界（Theorem 4.5）；而在标准梯度方差下，signGD（$\ell_\infty$-NSD）的下界明确依赖维度 $d$（$\min_t \|\nabla f(x_t)\|_1$ 包含 $d^{1/4}$ 因子，Theorem 4.7），证明维度无关速率不可达到。这就从正反两面确立了自适应方差作为维度无关收敛的必要概念。

### 统一框架的视角

所有这些保证均建立在 **well‑structured preconditioner set** $\mathcal{H}$ 的统一框架上（Algorithm 1）。通过选取不同的 $\mathcal{H}$（对角、全矩阵、谱范数等），该框架恢复 AdaGrad、Adam、Shampoo/ASGO、Muon 等常见自适应优化器；同时将自适应光滑性与自适应方差嵌入同一套分析语言，使得不同优化器间的收敛差异归结为几何量 $\Lambda_{\mathcal{H}}(f)$ 和 $\sigma_{\mathcal{H}}$ 的大小。

综上，核心创新不是新算法，而是**将自适应优化器的理论从“经验快”推向“可证明快且维度无关”的两个新概念**，它们强制性更强，却换来了加速率和维度无关性，解开了自适应行为与非欧几何之间的深层对偶关系。



![[assets/figures/papers/iclr26_0004_iaoAKDRAJQ_A_Tale_of_Two_Geometries_Adaptive_Optimizers_and/figures/002_Figure_1.jpg]]
*Figure 1: Here we demonstrate the duality between the supremum of the primal norms and the infimum of the corresponding dual norms for any well-structured preconditioner set H. In particular, we consider $\mathcal { H }$ = {all diagonal PSD matrices}, in which case \| $\cdot$ \|$_ { \mathcal { H } }$ = \| $\cdot$ \|$_ { \infty }$ and \| $\cdot$ \|$_ { \mathcal { H } , * }$ = \| $\cdot$ \|$_ { 1 }$ Left figure: the \| $\cdot$ \|$_ { \infty }$ -unit ball (black square) in the primal space is the intersection of all \| $\cdot$ \|$_ { H ^ { - } }$ unit ball (colored ellipses) for $\pmb { H } \in \mathcal { H }$ with $\mathrm { T r } ( { \cal$ H } ) $\le$ 1 , that is, \| $\cdot$ \|$_ { \infty }$ is the supremum of all such primal \|...

该工作提出一个统一的元算法（Algorithm 1），将几乎所有主流自适应优化器（AdaGrad、Adam、full‑matrix AdaGrad、one‑sided Shampoo/ASGO 等）归约为同一个 **良构前置条件集（well‑structured preconditioner set）** $$\mathcal{H}$$ 下的自适应梯度下降。框架的核心是：不再为每一种优化器单独分析，而是保留 $$\mathcal{H}$$ 所诱导的几何结构，把“自适应”理解为在 $$\mathcal{H}$$ 上对梯度外积的投影与预处理。正是这个统一的 pipeline，使后续能够通过引入 **自适应光滑性** $$\Lambda_{\mathcal{H}}(f)$$ 和 **自适应梯度方差** $$\sigma_{\mathcal{H}}$$ 来刻画加速与维度无关收敛，从而跳出标准光滑性和标准方差假设的瓶颈。

### 输入、前置条件集与输出

- **输入**：初始点 $$\mathbf{x}_0$$，学习率 $$\eta$$，动量参数 $$\beta$$（相当于 EMA 衰减系数），随机梯度 oracle $$\nabla f_t(\mathbf{x}_t)$$，以及一个良构前置条件集 $$\mathcal{H}$$（如全体对角半正定矩阵、全体半正定矩阵等），它定义了“允许的预处理矩阵”的集合。
- **目标输出**：经过 $$T$$ 步迭代后的参数 $$\mathbf{x}_T$$ 或平均点，以及每一步的预处理矩阵 $$\mathbf{V}_t$$。

### 四个核心模块

1. **前置条件集定义与几何语义**（Algorithm 1 的 implicit 前提）  
   给定 $$\mathcal{H}$$，立即得到两个对偶范数（Definition 2.1）：  
   $$\| \mathbf{x} \|_{\mathcal{H}} := \sup_{\mathbf{H} \in \mathcal{H}, \operatorname{Tr}(\mathbf{H}) \le 1} \| \mathbf{x} \|_{\mathbf{H}}, \qquad \| \mathbf{x} \|_{\mathcal{H},*} := \inf_{\mathbf{H} \in \mathcal{H}, \operatorname{Tr}(\mathbf{H}) \le 1} \| \mathbf{x} \|_{\mathbf{H},*}$$  
   它们分别对应“最不利”和“最有利”的加权 $$\ell_2$$ 范数。当 $$\mathcal{H}$$ 为所有对角矩阵时，$$\|\cdot\|_{\mathcal{H}}$$ 退化为 $$\|\cdot\|_\infty$$，其对偶范数退化为 $$\|\cdot\|_1$$（式 (4)），这直接编码了 ℓ∞‑NSD（即 SignGD/Lion 等）的几何。

2. **梯度外积累积**（Algorithm 1 lines 4–6）  
   在每一步 $$t$$，利用当前随机梯度 $$\mathbf{g}_t$$ 更新累积矩阵 $$\mathbf{M}_t$$：  
   $$\mathbf{M}_t = \beta \mathbf{M}_{t-1} + (1-\beta)\, \mathbf{g}_t \mathbf{g}_t^\top \quad\text{（EMA 形式）}$$  
   或采用等价的累积和/加权和形式。$$\mathbf{M}_t$$ 是后续构造预处理矩阵的“原料”，其本质是梯度二阶矩的在线估计。

3. **前置条件投影**（Algorithm 1 line 7）  
   通过投影算子 $$P_{\mathcal{H}}$$ 将 $$\mathbf{M}_t + \epsilon \mathbf{I}$$ 映射到合法预处理矩阵空间：  
   $$\mathbf{V}_t = P_{\mathcal{H}}(\mathbf{M}_t + \epsilon \mathbf{I}),$$  
   其中 $$P_{\mathcal{H}}(\mathbf{A}) = \arg\min_{\mathbf{H} \in \mathcal{H}} \langle \mathbf{A}, \mathbf{H}^{-1} \rangle + \operatorname{Tr}(\mathbf{H})$$（Lemma B.2）。  
   这一步是算法统一性的关键技术点：对于对角 $$\mathcal{H}$$，$$P_{\mathcal{H}}$$ 退化为逐坐标取逆平方根（产生 Adam 的逐坐标自适应步长）；对于全体 PSD 矩阵，$$P_{\mathcal{H}}$$ 等价于矩阵平方根逆（给出 full‑matrix AdaGrad）；对于矩阵结构 $$\mathcal{H}$$（如 Shampoo），则产生 Kronecker 因子预处理。投影操作确保了 $$\mathbf{V}_t$$ 始终保持在 $$\mathcal{H}$$ 内，并继承了来自梯度的自适应信息。

4. **自适应参数更新**（Algorithm 1 line 8）  
   $$\mathbf{x}_{t+1} = \mathbf{x}_t - \eta \,\mathbf{V}_t^{-1} \mathbf{g}_t.$$  
   该步骤形式上仍是梯度下降，但梯度被 $$\mathbf{V}_t^{-1}$$ 预处理，实现了对几何的自适应。对确定的 $$\mathcal{H}$$，更新可视为一种“归一化最速下降”的推广：当 $$\mathbf{V}_t$$ 仅依赖当前梯度（而非历史）时，退化为 NSD；引入历史信息后，便获得自适应优化器的典型行为。

### 管道如何服务于新假设

整个 pipeline 的核心价值在于，它将自适应优化器的分析转化为对 **$$\mathcal{H}$$‑范数下的光滑性与噪声** 的讨论。  
- **自适应光滑性**定义为 $$\Lambda_{\mathcal{H}}(f) := \min_{\mathbf{H} \in \mathcal{H}, \operatorname{Tr}(\mathbf{H}) \le 1} L_{\|\cdot\|_{\mathbf{H}}}(f)$$（Definition 2.4）。它比标准光滑性更强（更严格），却允许在凸情形下通过 Nesterov 动量达到加速率 $$\tilde{O}(\Lambda_{\mathcal{H}} D^2 / T^2)$$（Theorem 4.3），并在非凸情形达到 $$\tilde{O}(\sqrt{\Lambda_{\mathcal{H}} \Delta_0 / T})$$。  
- **自适应梯度方差** $$\sigma_{\mathcal{H}}$$（Definition 4.1）与 $$\Lambda_{\mathcal{H}}$$ 对偶，它刻画了梯度噪声在 $$\mathcal{H}$$ 诱导几何下的“最不利”尺度。基于此，归一化最速下降可获得与维度无关的收敛上界（Theorem 4.5）。

在上述管道中，$$\mathcal{H}$$ 的选择直接决定了 $$\Lambda_{\mathcal{H}}$$ 和 $$\sigma_{\mathcal{H}}$$ 的大小，从而控制收敛速度。当 $$\mathcal{H}$$ 为全体对角矩阵时，$$\Lambda_{\mathrm{diag}} \le L_{\mathrm{diag}}$$，且往往远小于标准全局光滑常数，于是加速项可以获得实质改善；而若仍沿用标准梯度方差假设，则 SignGD 的下界会显式依赖维度 $$d$$（Theorem 4.7），这恰恰说明自适应方差假设对于获得维度无关保证是必要的。  
综上，统一框架不仅集成了现有算法，更通过“自适应光滑性”和“自适应方差”这两个结构假设，建立了自适应优化器与几何之间的深层因果联系。



自适应优化器的理论核心建立在两个可分离但互补的几何概念上：**自适应光滑性**（adaptive smoothness）与**自适应梯度方差**（adaptive gradient variance）。两者分别控制着算法的确定性与随机性收敛行为，并通过统一的前置条件集（well‑structured preconditioner set ℋ）将各种自适应优化器（如 Adam、SignGD、Shampoo）纳入同一分析框架。

### 前置条件集与诱导范数

给定一个良结构的前置条件集 ℋ（如全体对角半正定矩阵、全体半正定矩阵等），定义其诱导范数
$$
\| \mathbf{x} \|_{\mathcal{H}} := \sup_{\mathbf{H} \in \mathcal{H}, \operatorname{Tr}(\mathbf{H}) \le 1} \| \mathbf{x} \|_{\mathbf{H}} .
\tag{1}
$$
它的对偶范数则取遍所有可行 H 的下确界：
$$
\| \cdot \|_{\mathcal{H},*} = \inf_{\mathbf{H} \in \mathcal{H}, \operatorname{Tr}(\mathbf{H}) \le 1} \| \cdot \|_{\mathbf{H},*} .
\tag{Lemma 2.2}
$$
对 ℋ={对角 PSD}，这一对偶关系退化为 ℓ∞ 与 ℓ1 之间的熟悉关系：
$$
\sup_{\text{对角 } \mathbf{H}\succeq 0, \operatorname{Tr}(\mathbf{H})\le 1} \| \cdot \|_{\mathbf{H}} = \| \cdot \|_{\infty}, \qquad
\inf_{\text{对角 } \mathbf{H}\succeq 0, \operatorname{Tr}(\mathbf{H})\le 1} \| \cdot \|_{\mathbf{H},*} = \| \cdot \|_{1}.
\tag{4}
$$

统一算法（Algorithm 1）分别在这类前置条件集上执行：
1. 累积梯度外积  $\mathbf{M}_t$（累计、EMA 或加权和）；
2. 通过投影算子  $\mathbf{V}_t = P_{\mathcal{H}}(\mathbf{M}_t + \varepsilon \mathbf{I}_d)$  提取自适应前置矩阵，其中
   $$
   P_{\mathcal{H}}(\mathbf{M}) = \arg\min_{\mathbf{H}\in\mathcal{H}} \langle \mathbf{M}, \mathbf{H}^{-1} \rangle + \operatorname{Tr}(\mathbf{H}) ;
   $$
3. 利用 $\mathbf{V}_t^{-1} \mathbf{g}_t$ 驱动参数更新。
该算法通过切换 ℋ 即可恢复 AdaGrad、Adam、AdaGrad‑Norm、full‑matrix AdaGrad、单侧 Shampoo/ASGO 等主流自适应优化器。

### 自适应光滑性：加速收敛的几何原因

传统光滑性 $L_{\|\cdot\|_{\mathbf{H}}}(f)$ 约束梯度在单个矩阵加权范数下的利普希茨常数。**自适应光滑性**则考虑整个 ℋ 中“最有利”的 H：
$$
\Lambda_{\mathcal{H}}(f) := \min_{\mathbf{H}\in\mathcal{H}, \operatorname{Tr}(\mathbf{H})\le 1} L_{\|\cdot\|_{\mathbf{H}}}(f) = \min_{\mathbf{H}\in\mathcal{H}, \forall\mathbf{x},\, -\mathbf{H}\preceq \nabla^2 f(\mathbf{x})\preceq\mathbf{H}} \operatorname{Tr}(\mathbf{H}) .
\tag{5}
$$
直观上，$\Lambda_{\mathcal{H}}(f)$ 衡量损失函数在几何 ℋ 下的**最紧二阶边界**。当 ℋ 为全体 PSD（及其约束）时，它退化为 Hessian 迹，比起普适的 ℓ∞‑光滑性更加精确。

这一概念直接进入收敛率：对于非凸目标，算法在自适应光滑性下可达 $\tilde{O}(\Lambda_{\mathcal{H}}(f)/T)^{\frac12}$ 的形式，等价于最优速率 $\tilde{O}(T^{-1/4})$（Theorems D.2, D.7, D.8）。更重要的是，在凸情形中结合 Nesterov 加速，自适应光滑性催生出**加速率** $O(T^{-2})$：
$$
\mathbb{E}[f(\bar{\mathbf{x}}_T) - f(\mathbf{x}^*)] = \tilde{O}\Big( \frac{\Lambda_{\mathcal{H}}(f) D^2 \log^2 d + d\sqrt{\varepsilon} D}{T^2} + \frac{\sigma_{\mathcal{H}} D \log d}{\sqrt{T}} \Big),
\tag{Theorem 4.3}
$$
而传统的 ℓ∞‑光滑性下所有算法的最坏收敛阶仅为 Ω(T⁻¹)，因此自适应光滑性揭示了自适应优化器能够**利用 Hessian 几何实现根本加速**的机理。

### 自适应梯度方差：维度无关收敛的噪声结构

与之平行的随机概念是**自适应梯度方差** σ_ℋ（Definition 4.1），它通过考查梯度噪声在几何 ℋ 中的投影来量化随机梯度的波动大小，满足上界 $\sigma_{\mathcal{H}}^2 \le \operatorname{Tr}(P_{\mathcal{H}}(\Sigma))$。在弱噪声假设（标准光滑性 + 自适应方差）下，归一化最速下降（NSD）可直接得到**与维度无关**的收敛上界：
$$
\mathbb{E} \frac{1}{T} \sum_{t=0}^{T-1} \|\nabla f(\mathbf{x}_t)\|_{\mathcal{H},*} \le \frac{\Delta_0}{\eta T} + \frac{2\eta}{\alpha} L_{\|\cdot\|}(f) + \frac{2\sigma_{\mathcal{H}}}{\alpha T} + 2\sigma_{\mathcal{H}}\sqrt{\alpha},
\tag{Theorem 4.5}
$$
其中决定性的噪声项仅由 σ_ℋ 控制，不显含维度 d。这说明只要梯度噪声在几何 ℋ 下“自适应地集中”，NSD 就能摆脱维数灾难。

反观标准梯度方差假设，signGD（亦即 ℓ∞‑NSD）会显式地受到维度惩罚：
$$
\mathbb{E}\big[\min_{t\in[T]} \|\nabla f(\mathbf{x}_t)\|_1\big] = \min\!\Big\{e^{-2}5^{-\frac14}(d L \Delta_0 \sigma^2)^{\frac14} T^{-\frac12},\; e^{-2}5^{-\frac12}\sigma\Big\},
\tag{Theorem 4.7}
$$
这组结果共同说明：**自适应方差正是实现维度无关收敛的必要结构条件**，而自适应光滑性则是获得加速率的结构条件。两套几何概念互补，构成了自适应优化器非欧收敛理论的基石。



## 实验与关键发现

本文为一篇纯理论分析工作，未包含数值实验。论文的核心贡献在于通过引入自适应光滑性 $\Lambda_{\mathcal{H}}(f)$ 和自适应梯度方差 $\sigma_{\mathcal{H}}$，建立了自适应优化器及归一化最速下降法在非欧几里得几何下的收敛理论。以下总结其主要分析结论。

**主要收敛结果**

1. **非凸情形下的标准收敛率**  
   在非凸随机优化设定下，自适应优化器（Algorithm 1）的收敛率由自适应光滑性 $\Lambda_{\mathcal{H}}(f)$ 控制，达到 $\tilde{O}(T^{-1/4})$，匹配不可退化的下界（[analysis_truth]）。该结果突破了仅使用标准光滑性 $L_{\|\cdot\|_{\mathcal{H}}}(f)$ 时的限制，说明自适应光滑性是对一类自适应算法收敛行为更精确的刻画。

2. **Nesterov 加速下的加速率**  
   在凸函数并且满足自适应方差假设时，引入 Nesterov 动量的自适应优化器（Algorithm 2）将收敛率提升至  
   
$$
\mathbb{E}[f(\bar{x}_T)-f(x^*)]=\tilde{O}\!\left(\frac{\Lambda_{\mathcal{H}}(f)D^2\log^2 d + d\sqrt{\epsilon}D}{T^2} + \frac{\sigma_{\mathcal{H}} D \log d}{\sqrt{T}}\right),
$$
  
   其中加速项由自适应光滑性决定，实现了 $O(T^{-2})$ 的确定性衰减，超越了仅依靠标准光滑性时的 $\Omega(T^{-1})$ 最坏下界。

3. **自适应方差带来的维度无关上界**  
   当仅考虑梯度噪声的自适应方差 $\sigma_{\mathcal{H}}$ 时，归一化最速下降（NSD）可以获得与维度无关的收敛上界（Theorem 4.5）：
   
$$
\mathbb{E}\frac{1}{T}\sum_{t=0}^{T-1}\|\nabla f(\mathbf{x}_t)\|_{\mathcal{H},*} \le \frac{\Delta_0}{\eta T} + \frac{2\eta}{\alpha} L_{\|\cdot\|}(f) + \frac{2\sigma_{\mathcal{H}}}{\alpha T} + 2\sigma_{\mathcal{H}}\sqrt{\alpha}.
$$
  
   该上界不显式依赖于维度 $d$，而仅取决于标准光滑性和自适应方差。

4. **标准方差假设下的维度依赖下界**  
   若仅假设标准梯度方差 $\sigma^2$，则 $l_\infty$-NSD（即 SignGD）的收敛下界显式依赖于维度 $d$（Theorem 4.7）：
   
$$
\mathbb{E}\big[\min_{t\in[T]}\|\nabla f(\mathbf{x}_t)\|_1\big] = \min\!\left\{e^{-2}5^{-\frac14}(d L \Delta_0 \sigma^2)^{\frac14} T^{-\frac12},\; e^{-2}5^{-\frac12}\sigma\right\},
$$
  
   表明维度无关加速在标准方差假设下不可达，从而突显出自适应方差假设的必要性。

**图示结论**

正文中的 Figure 1 针对对角正定矩阵构造的预条件子集合 $\mathcal{H}$，可视化了对偶范数之间的联系：$\sup_{\mathbf{H}\in\mathcal{H},\,\operatorname{Tr}(\mathbf{H})\le1}\|\cdot\|_{\mathbf{H}} = \|\cdot\|_\infty$ 由椭圆交集描述，而 $\inf_{\mathbf{H}\in\mathcal{H},\,\operatorname{Tr}(\mathbf{H})\le1}\|\cdot\|_{\mathbf{H},*} = \|\cdot\|_1$ 由椭圆并集描述。该图直观揭示了 $l_\infty$ 与 $l_1$ 范数作为加权 $l_2$ 范数极值的几何本质，为引入自适应光滑性及理解自适应优化器对非欧几何的利用提供了几何直觉。

需要指出，上述结论均为理论推导，文中未通过仿真或真实数据实验进行数值验证。对自适应光滑性与方差假设在实践中的可达性、及其他潜在失效模式的分析，需后续实验补充。



## 定位与知识库关联

### 1. 论文在优化理论中的坐标

本文的核心理论贡献位于**自适应优化器收敛理论**与**非欧几何下降分析**的交汇点。它试图回答一个长期未解的问题：当自适应优化器（如 Adam、AdaGrad）与归一化最速下降（NSD）被视为同一类预处理梯度方法时，它们各自依赖的光滑性和噪声结构有何不同？这一根本差异如何导出截然不同的收敛保证？

论文通过引入两个新的结构化假设——**自适应光滑性**（$\Lambda_{\mathcal{H}}(f)$）和**自适应梯度方差**（$\sigma_{\mathcal{H}}$）——为对比自适应优化器与 NSD 提供了统一的理论语言。这一框架揭示了一条清晰的因果链路：

- **自适应光滑性** $\Lambda_{\mathcal{H}}(f)$ 是加速收敛的催化剂：它使得带 Nesterov 动量的自适应优化器（Algorithm 2）在凸情形达到 $\tilde{O}(T^{-2})$ 的加速率，而标准 $\ell_{\infty}$ 光滑性下所有算法的最坏收敛阶仅为 $\Omega(T^{-1})$。
- **自适应梯度方差** $\sigma_{\mathcal{H}}$ 是维度无关收敛的催化条件：它使 NSD 获得与维度无关的上界（Theorem 4.5），而标准梯度方差假设下 signGD（$\ell_{\infty}$‑NSD）的收敛下界明确依赖于维度 $d$（Theorem 4.7），证明了维度无关收敛在弱假设下不可及。

这一区分构成了论文知识贡献的瓶颈：自适应优化器与 NSD 虽然共享相同的预处理几何 $\mathcal{H}$，但它们收敛理论所依赖的光滑性和噪声概念是**不可互换**的。自适应光滑性和自适应方差是更强的假设，但换取的是加速率和维度无关性——这种“假设换取收敛速度”的权衡，正是自适应优化实际优势的理论根源。

### 2. 与基线方法的关系：统一框架下的分化

论文通过**良构预处理集合**（well-structured preconditioner set）的统一形式将多种优化器纳入同一算法框架（Algorithm 1），使其关系变得透明。

**基线方法类型**：

| 方法 | 几何实现 | 梯度更新形式 | 在框架中的角色 |
|------|----------|-------------|---------------|
| **归一化最速下降（NSD）** | 任意范数 $\|\cdot\|_{\mathbf{H}}$ | $x_{t+1} = x_t - \eta \cdot \arg\min_{\|d\|_{\mathcal{H}}\le 1} \langle d, g_t \rangle$ | 标准非欧下降基线，依赖标准光滑性 $L_{\|\cdot\|_{\mathbf{H}}}(f)$ |
| **signGD** | $\ell_{\infty}$ 范数（对角 $\mathcal{H}$ 族取上确界） | $x_{t+1} = x_t - \eta \cdot \operatorname{sign}(g_t)$ | NSD 在 $\ell_{\infty}$ 下的实例，对照 Adam |
| **Lion** | 同上（$\ell_{\infty}$‑NSD 加符号动量） | 动量累积 + 符号操作 | 被视为 $\ell_{\infty}$‑NSD 的动量变体 |
| **Muon** | 矩阵谱范数（矩阵 $\mathcal{H}$ 族） | 基于矩阵范数的最速下降 | 被视为矩阵谱范数下 NSD 的实例 |
| **AdaGrad / Adam / Shampoo** | 不同 $\mathcal{H}$ 族（对角线/全矩阵/克罗内克因子） | $x_{t+1} = x_t - \eta \mathbf{V}_t^{-1} g_t$，其中 $\mathbf{V}_t = P_{\mathcal{H}}(\mathbf{M}_t + \epsilon \mathbf{I})$ | 统一框架中自适应优化器的具体实例 |

**关键转换关系**：

从 Algorithm 1 的更新 $x_{t+1} = x_t - \eta \mathbf{V}_t^{-1} g_t$（其中 $\mathbf{V}_t = P_{\mathcal{H}}(\mathbf{M}_t + \epsilon \mathbf{I})$ 是梯度外积 $\mathbf{M}_t$ 在 $\mathcal{H}$ 上的投影）可以看出，自适应优化器与 NSD 的核心区别在于**信息累积深度**：

- **NSD** 仅适应当前梯度 $g_t$ 的方向，相当于 $\mathbf{M}_t = g_t g_t^\top$ 的特例；
- **自适应优化器** 累积历史梯度外积（累计/EMA/加权），形成数据驱动的预处理矩阵。

这解释了论文 Abstract 的核心综述判断：“自适应优化器仅当适应当前梯度时退化为 NSD”。一旦引入历史积累，它们便进入由自适应光滑性控制的收敛体制，与 NSD 的标准光滑性体制分离。

### 3. 理论创新：改变了什么？

论文在两个关键假设上做了“升级”，构成了分析体系的核心变化：

**变化一：光滑性假设的强化**

- **基线值**：标准相对光滑性 $L_{\|\cdot\|_{\mathcal{H}}}(f)$ ——定义为满足 $\|\nabla f(x) - \nabla f(y)\|_{\mathcal{H},*} \le L_{\|\cdot\|_{\mathcal{H}}}(f) \cdot \|x-y\|_{\mathcal{H}}$ 的最小常数。该假设是 NSD 收敛分析的标准入口（NSD convergence rate under general H）。
- **本文值**：自适应光滑性 $\Lambda_{\mathcal{H}}(f) := \min_{\mathbf{H} \in \mathcal{H}, \operatorname{Tr}(\mathbf{H}) \le 1} L_{\|\cdot\|_{\mathbf{H}}}(f)$（Definition 2.4, Eq (5)）——
  在所有满足迹约束的预处理矩阵诱导的范数中，取光滑性参数的最小值。该定义在公式层面等价于 $\Lambda_{\mathcal{H}}(f) = \min_{\mathbf{H} \in \mathcal{H},\ \forall x, -\mathbf{H} \preceq \nabla^2 f(x) \preceq \mathbf{H}} \operatorname{Tr}(\mathbf{H})$，即寻找以最小迹支配 Hessian 谱的预处理矩阵。
- **因果效果**：$\Lambda_{\mathcal{H}}(f)$ 直接催化了加速收敛——在非凸情形达到 $\tilde{O}(T^{-1/4})$ 的最优速率（Theorems D.2, D.7, D.8），在凸情形通过 Nesterov 加速达到 $O(T^{-2})$。这意味着自适应光滑性假设的强度换取了一阶收敛阶数的提升。

**变化二：噪声假设的结构化**

- **基线值**：标准梯度方差 $\sigma_{\|\cdot\|_{\mathcal{H},*}}$ ——典型形式为 $\mathbb{E}\|\nabla f(x;\xi) - \nabla f(x)\|_{\mathcal{H},*}^2 \le \sigma^2$。在此假设下，signGD 的收敛下界明确依赖于维度 $d$（Theorem 4.7：$\mathbb{E}[\min_t \|\nabla f(x_t)\|_1] = \min\{e^{-2}5^{-1/4}(d L \Delta_0 \sigma^2)^{1/4} T^{-1/2}, e^{-2}5^{-1/2}\sigma\}$），维度灾难根源已被定位。
- **本文值**：自适应梯度方差 $\sigma_{\mathcal{H}}$（Definition 4.1）——可以理解为梯度噪声在预处理几何 $\mathcal{H}$ 下的结构化度量。Proposition B.11 给出其上界 $\sigma_{\mathcal{H}}^2 \le \operatorname{Tr}(P_{\mathcal{H}}(\Sigma))$，其中 $\Sigma$ 是梯度协方差矩阵，$P_{\mathcal{H}}$ 是向 $\mathcal{H}$ 的投影。
- **因果效果**：$\sigma_{\mathcal{H}}$ 使 NSD 的收敛界与维度解耦（Theorem 4.5）。这是对标准噪声假设的严格强化：自适应方差不是简单的标量方差上界，而是通过预处理几何过滤了噪声的维度膨胀效应。

### 4. 适用边界与局限

论文在理论和实证层面存在若干需要手动验证的弱信号：

**假设的严格性**：

自适应光滑性 $\Lambda_{\mathcal{H}}(f)$ 要求函数 $f$ 的 Hessian 在所有点处能够被某个迹约束的 $\mathbf{H} \in \mathcal{H}$ 统一支配（$-\mathbf{H} \preceq \nabla^2 f(x) \preceq \mathbf{H}$）。这一条件比标准光滑性更强，在 Hessian 谱剧烈波动或非平稳的深度学习损失景观中是否成立，论文未提供实验验证。类似地，自适应梯度方差 $\sigma_{\mathcal{H}}$ 的结构化依赖于梯度协方差与预处理几何的相容性——当真实噪声结构恰好与 $\mathcal{H}$ 失配时，维度无关界可能退化。

**与 follow-up 工作的理论缺口**：

论文在 Appendix A 中指出，Jiang et al. (2025) 在更窄的噪声假设下为 signGD 获得了类似 Theorem 4.5 的维度无关结果，但该假设比本文的自适应方差更强。此外，Frans et al. (2025) 将自适应优化器视为矩阵白化修正，并经验性地展示了其优于精确谱归一化（NSD）的性能。这些工作从不同角度触碰了同一问题，但未能在统一框架下明确解释“何时自适应优化器优于 NSD”——本文的理论提供了触发这一优势的条件（自适应光滑性/方差假设成立时），但缺少将条件映射到实际训练任务特征的桥梁。

**实验验证的缺失**：

已验证分析显示论文的主实验、消融和公平性说明均为空——这意味着本文是纯理论论文，不包含经验验证。所有声称的收敛速率和维度无关性均为纸面推导结果。在缺乏实验证据的情况下，自适应光滑性和自适应方差假设在实际优化问题中的饱和程度、以及加速率和维度无关性在有限步迭代中是否可观测，均需独立验证才能确认。

### 5. 开放问题与后续方向

基于论文的理论体系，以下问题构成自然的延伸空间：

1. **加速-噪声缺口**：Theorem 4.3 的收敛界中，加速项由 $\Lambda_{\mathcal{H}}(f) D^2 / T^2$ 控制，而噪声项仍为 $\sigma_{\mathcal{H}} D / \sqrt{T}$。这表明在随机设置中，Nesterov 加速的优势仅体现在光滑性主导项，噪声项未获得加速。能否设计一种同时加速噪声项的算法，或在自适应方差假设下证明 $\tilde{\Omega}(1/\sqrt{T})$ 的下界，是一个理论缺口。

2. **自适应方差的结构依赖性**：$\sigma_{\mathcal{H}}$ 的上界涉及梯度协方差的投影 $\operatorname{Tr}(P_{\mathcal{H}}(\Sigma))$。当 $\mathcal{H}$ 为对角矩阵族时，$\sigma_{\mathcal{H}}$ 只惩罚噪声的逐坐标方差；而当 $\mathcal{H}$ 为全矩阵族时，它受到谱结构的更强约束。这一观察提示：不同的 $\mathcal{H}$ 选择可能导致 $\sigma_{\mathcal{H}}$ 量级差异巨大，进而影响维度无关界的实际有效性。该方向尚无系统性研究。

3. **非凸前沿的 Acceleraion**：论文在非凸设置下仅给出了标准收敛阶 $\tilde{O}(T^{-1/4})$，未讨论加速可能性。自适应光滑性是否能在非凸情形催化超一阶收敛，是与凸情形加速理论的天然对偶问题。

4. **与 Muon/Lion 的实证连接**：论文将 Lion 和 Muon 分别定位为 $\ell_{\infty}$‑NSD 和矩阵谱范数 NSD 的等价形式，但未提供两者在自适应光滑性/方差下的理论对比。鉴于 Muon 在近期大模型训练中的成功，理解其矩阵几何是否天然具有更小的 $\Lambda_{\mathcal{H}}(f)$ 或 $\sigma_{\mathcal{H}}$，可能为实践者提供有操作性的理论指导。

**证据强度总结**：论文的核心理论声明（加速收敛、维度无关界）均有高置信度（0.95–1.0）的定理证明支撑，但所有结论均未经验证地映射到实际优化任务。在将该理论框架作为深度学习优化设计的决策依据前，需要独立的实验基准和假设检验。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Tale_of_Two_Geometries_Adaptive_Optimizers_and_Non_Euclidean_Descent.pdf

![[paperPDFs/ICLR_2026/A_Tale_of_Two_Geometries_Adaptive_Optimizers_and_Non_Euclidean_Descent.pdf]]
