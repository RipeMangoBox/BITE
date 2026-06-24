---
title: "The Polar Express: Optimal Matrix Sign Methods and their Application to the Muon Algorithm"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/The_Polar_Express_Optimal_Matrix_Sign_Methods_and_their_Application_to_the_Muon_Algorithm.pdf
openreview_forum_id: yRtgZ1K8hO
aliases:
- PE
- PEOMSMTAMA
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "每一迭代步所使用的奇数多项式更新规则。通过根据当前奇异值所在区间动态地、贪婪地选择最优逼近多项式，可以控制每一步的收敛速度和数值稳定性，这是加速收敛和保证最终精度的核心操作。"
primary_logic: "通过贪婪地在每一步求解极小化极大（minimax）问题来选取最优奇数多项式，得到的多项式复合整体上在最大误差意义上是最优的；这种策略既能实现初期的快速推进，又能保证超指数收敛，且整个过程只使用矩阵乘法，非常适合 GPU 计算。"
claims:
- "Polar Express 在每一步构造的多项式复合是 sign(x) 在 supremum 范数下的最优逼近（定理 3.1）。"
- "Polar Express 在奇异值区间 [ℓ,1] 上比同次数的牛顿-舒尔茨迭代收敛更快，且具有超指数收敛速率（定理 3.3）。"
- "在合成矩阵和 GPT-2 梯度矩阵上，Polar Express 在所有迭代步均优于牛顿-舒尔茨、Jordan 方法和 You 方法（图 3）。"
- "在 GPT-2 语言模型训练中，使用 Polar Express 的 Muon 优化器始终获得更低的验证损失，且提升在不同学习率下稳定（图 1、4、6）。"
---

# The Polar Express: Optimal Matrix Sign Methods and their Application to the Muon Algorithm

> [!tip] 核心洞察
> 通过贪婪地在每一步求解极小化极大（minimax）问题来选取最优奇数多项式，得到的多项式复合整体上在最大误差意义上是最优的；这种策略既能实现初期的快速推进，又能保证超指数收敛，且整个过程只使用矩阵乘法，非常适合 GPU 计算。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 极地特快：最优矩阵符号方法及其在 Muon 算法中的应用 |
| 英文题名 | The Polar Express: Optimal Matrix Sign Methods and their Application to the Muon Algorithm |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=yRtgZ1K8hO); [GitHub](https://github.com/NoahAmsel/PolarExpress) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | Polar Express |
| Dataset | GPT-2-Large (774M) on FineWeb 1B tokens, GPT-2-Small (124M) on FineWeb 1B tokens (no weight decay), GPT-2-Large on FineWeb 10B tokens (with weight decay 0.1), CIFAR-10 with ResNet-20 |

> [!tip] 效果简介
> - GPT-2-Large (774M) on FineWeb 1B tokens 上，final validation loss 为 3.340 (muon-PolarExp, lr=0.02)，对比 3.398 (muon-Jordan, lr=0.02) / 3.399 (muon-You, lr=0.02)，变化 -0.058 / -0.059。
> - GPT-2-Small (124M) on FineWeb 1B tokens (no weight decay) 上，final validation loss 为 3.588 (muon-PolarExp, lr=0.005)，对比 3.639 (muon-Jordan, lr=0.01) / 3.629 (muon-You, lr=0.01)，变化 -0.051 / -0.041。
> - GPT-2-Large on FineWeb 10B tokens (with weight decay 0.1) 上，best final validation loss 为 2.913 (muon-PolarExp, lr=0.002)，对比 2.921 (muon-Jordan, lr=0.002) / 2.919 (muon-You, lr=0.002)，变化 -0.008 / -0.006。

## 概述

### 问题与目标

在深度学习优化中，**Muon** 优化器使用动量梯度矩阵的极分解（polar decomposition）作为下降方向：

$$M_t = \beta M_{t-1} + (1-\beta) G_t, \quad W_{t+1} = W_t - \lambda \, \mathrm{polar}(M_t)$$

其中 $\mathrm{polar}(M) := U V^{\mathsf{T}}$ 是矩阵 $M$ 的最接近半正交矩阵。高效计算极分解因此成为 Muon 性能的关键瓶颈。

现有方法面临根本性矛盾：**牛顿-舒尔茨迭代**（Newton-Schulz）仅依赖 GPU 友好的矩阵乘法，但初期收敛缓慢；**Jordan 方法**和 **You 方法**等启发式多项式方法初期进展快，却无法最终收敛，精度停滞。同时，高精度方法普遍依赖矩阵求逆或 QR 分解，难以充分利用 GPU 并行能力。因此，亟需一种仅用矩阵乘法、初期收敛快且最终能超指数收敛的 GPU 友好算法。

### 核心方法

本文提出 **Polar Express**，其核心思路是：在每一步迭代中，根据当前奇异值所在区间 $[\ell_t, u_t]$，贪婪地求解极小化极大（minimax）问题来选取最优奇数多项式 $p_t$：

$$p_t = \underset{p \in \mathbb{P}_d^{\mathrm{odd}}}{\mathrm{arg\,min}} \underset{x \in [\ell_t, u_t]}{\mathrm{max}} |1 - p(x)|$$

由此得到的多项式复合 $p^{\star} = p_T \circ p_{T-1} \circ \cdots \circ p_1$ 是 $\mathrm{sign}(x)$ 在 supremum 范数下的最优逼近（定理 3.1），既能实现初期快速推进，又能保证超指数收敛：

$$\|\mathrm{polar}(M) - X_T\|_2 \leq |1 - \ell^2|^{(q+1)^T}$$

整个过程仅使用矩阵乘法和线性组合，非常适合 GPU 计算。

### 主要结果

在 **GPT-2-Large（774M）** 模型上训练 FineWeb 1B tokens，使用 Polar Express 的 Muon 优化器取得验证损失 **3.340**，显著优于 Muon-Jordan（3.398）和 Muon-You（3.399）（图 1）。在 GPT-2-Small 上同样一致领先（3.588 vs. 3.639/3.629，图 4）。消融实验表明，仅需 5–6 次迭代即可饱和优化性能，更多迭代或精确 SVD 不会进一步降低损失（图 5）。

### 方法定位

在方法谱系中，Polar Express 属于**自适应多项式迭代**方法：与固定多项式的牛顿-舒尔茨不同，它在每一步动态选择最优更新规则；与启发式的 Jordan/You 方法不同，其多项式选择有严格的最优性理论保证。在知识库中，该方法填补了“纯矩阵乘法、理论上最优收敛”这一空白，为 Muon 优化器提供了目前已知最强的极分解近似方案。

## 背景与动机

### 问题背景：Muon 优化器与极分解

Muon 优化器在深度学习中用于更新权重矩阵。对于动量矩阵 $M_t$，其更新规则为：

$$M_t = \beta M_{t-1} + (1-\beta) G_t, \quad W_{t+1} = W_t - \lambda \mathrm{polar}(M_t)$$

其中 $\mathrm{polar}(M) := U V^{\mathsf{T}}$ 是矩阵 $M$ 的极因子，即左奇异向量与右奇异向量的乘积。Muon 的核心计算瓶颈在于高效、准确地计算动量矩阵的极分解。由于该操作在每一步优化中都要执行，其计算效率和数值精度直接影响训练速度和模型质量。

### 现有方法的根本矛盾

计算极分解的方法主要分为两类，但在深度学习场景下存在根本性矛盾：

**经典多项式迭代法（牛顿-舒尔茨）** 使用固定的奇数多项式更新规则，仅依赖矩阵乘法，天然适合 GPU 并行计算。其 3 次迭代公式为：

$$X_{t+1} = \frac{3}{2} X_t - \frac{1}{2} X_t X_t^{\top} X_t$$

更高次版本（如 5 次）收敛更快，但整体上牛顿-舒尔茨在迭代初期进展缓慢——当奇异值较小时，多项式逼近 sign 函数的速度很慢，需要较多迭代步才能达到可用精度。

**近期启发式方法** 如 **Jordan 方法**（Jordan et al., 2024b）和 **You 方法**（Cesista et al., 2025）针对低精度区域进行了启发式搜索，迭代初期收敛极快，但最终不收敛：Jordan 方法的误差停滞在约 0.3，You 方法精度虽有改善但仍无法收敛到机器精度。

**高精度数值方法**（如牛顿法、QDWH）虽然收敛快且精度高，但依赖矩阵求逆或 QR 分解，无法充分利用 GPU 的大规模并行能力，在 bfloat16 等低精度算术下也难以稳定运行。

### 核心瓶颈与本文动机

上述方法的矛盾揭示了一个明确的技术缺口：**急需一种仅依赖矩阵乘法、初期收敛快且最终能超指数收敛的 GPU 友好算法**。具体而言：

1. **初期收敛**：必须快速推进，避免牛顿-舒尔茨式的缓慢起步；
2. **最终精度**：必须保证收敛，不能像 Jordan/You 方法那样停滞；
3. **计算原语**：只能使用矩阵乘法和线性组合，避免求逆或 QR 分解；
4. **低精度鲁棒性**：必须在 bfloat16 下稳定运行，处理极小奇异值带来的数值问题。

Polar Express 正是针对这些缺口提出的：通过每一步贪婪地求解极小化极大（minimax）问题来选取最优奇数多项式，得到的多项式复合在 sup 范数下是 sign 函数的最优逼近。这一策略既能实现初期的快速推进，又能保证超指数收敛，且整个过程只使用矩阵乘法，完美匹配 GPU 的计算特性。

## 核心创新

### 从固定多项式到贪婪最优多项式

现有矩阵符号函数的迭代方法遵循一个共同范式：选定一个固定的奇数多项式 $p(x)$，在每一步重复应用 $X_{t+1} = p(X_t)$。**牛顿-舒尔茨**（Newton-Schulz）方法使用 3 次或 5 次固定多项式（如 $p(x) = \frac{3}{2}x - \frac{1}{2}x^3$），其初期收敛极其缓慢——在奇异值接近 0 时，每次迭代的进展微乎其微。**Jordan 方法**和 **You 方法**分别通过启发式搜索和分段固定多项式来加速初期收敛，但付出了致命的代价：它们最终不收敛，误差停滞在约 0.3 的水平。

Polar Express 的核心创新在于**将“固定多项式”这一隐含假设彻底打破**。该方法在每一步迭代中，根据当前奇异值所处的区间 $[\ell_t, u_t]$，在线求解一个极小化极大（minimax）问题：

$$p_t = \underset{p \in \mathbb{P}_d^{\mathrm{odd}}}{\mathrm{arg\,min}} \underset{x \in [\ell_t, u_t]}{\mathrm{max}} |1 - p(x)|$$

这一步选择的是在当前区间上逼近符号函数 $\mathrm{sign}(x)$ 的**最优奇数多项式**。由于每一步的区间 $[\ell_t, u_t]$ 随迭代动态收缩，每一步的最优多项式也随之变化——初期多项式激进地推动奇异值远离 0，后期多项式精细地逼近 1。这种贪婪策略被证明具有全局最优性：最终得到的多项式复合 $p^* = p_T \circ p_{T-1} \circ \cdots \circ p_1$ 是在 supremum 范数下逼近 $\mathrm{sign}(x)$ 的最优解（定理 3.1），同时具有超指数收敛速率：

$$\|\mathrm{polar}(M) - X_T\|_2 \leq |1 - \ell^2|^{(q+1)^T}$$

对于 $d=5$（即 $q=2$），这意味着立方收敛——每一步迭代将误差的指数放大三倍。

### 三个关键工程改进

除核心算法外，Polar Express 在三个工程细节上做出了对实际部署至关重要的改进：

**1. 奇异值归一化策略**：传统方法使用 $\|M\|_F$ 归一化初始矩阵，但当矩阵存在极小奇异值时会导致数值不稳定。Polar Express 采用 $\|M\|_F + 10^{-2}$ 归一化，并在多项式评估时引入 $1.01$ 安全因子（将 $p_t(x)$ 替换为 $p_t(x/1.01)$），显著提升了 bfloat16 精度下的稳定性（附录 G，图 7）。

**2. 区间下界的鲁棒处理**：算法固定假设奇异值下界 $\ell = 10^{-3}$（针对 bfloat16），但实际矩阵的最小奇异值可能远小于此。当 $\ell_t < u_t/10$ 时，算法将 $\ell_t$ 视为 $u_t/10$ 来选择更新规则，避免了因下界过于保守而导致的收敛减速（第 3.3 节，附录 G）。

**3. 矩形矩阵的快速迭代**：对于高宽比 $\alpha \gg 1$ 的矩阵，传统迭代需要 $T$ 次矩阵乘法。Polar Express 提出了一种仅需两次矩形矩阵乘法即可完成全部 $T$ 次迭代的算法，配合重启策略保证数值稳定性（算法 3，附录 J）。在 $\alpha=4$ 时实现约 2 倍加速，$\alpha=32$ 时约 5 倍加速（图 18）。

### 与基线方法的本质差异

| 维度 | 牛顿-舒尔茨 | Jordan / You 方法 | Polar Express |
|------|-------------|-------------------|---------------|
| 多项式选择 | 固定（3 次或 5 次） | 启发式固定 | 每步贪婪最优 |
| 初期收敛 | 极慢 | 快 | 快 |
| 最终收敛 | 超指数收敛 | 不收敛（停滞在 ~0.3） | 超指数收敛 |
| 全局最优性 | 无保证 | 无保证 | 定理保证（定理 3.1） |
| 精度依赖 | 矩阵乘法 | 矩阵乘法 | 矩阵乘法 |

这种设计使得 Polar Express 成为首个**同时满足**初期快速推进、最终超指数收敛、且全程仅使用矩阵乘法的 GPU 友好方法。在合成矩阵和 GPT-2 真实梯度矩阵上，Polar Express 在所有迭代步均优于其他方法（图 3）；在 GPT-2-Large 训练中，验证损失从 muon-Jordan 的 3.398 降至 3.340（图 1）。

## 整体框架

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_yRtgZ1K8hO/figures/008_Figure_4.jpg]]
*Figure 4: Training a GPT-2-Small (124M) model on 1 Billion tokens of the FineWeb data set (Penedo et al., 2024). muon-\<method> denotes Muon with 5 iterations of \<method> to compute polar(M ). No weight decay is used. Left: final validation loss vs. learning rate. The best final validation losses for each method were adamw(lr =0.0005): 4.197, muon-Jordan(lr =0.01): 3.639, muon-You(lr =0.01): 3.629 and muon-PolarExp(lr =0.005): 3.588. Right: Validation loss vs. training iteration*

### 问题定位与设计动机

Polar Express 旨在解决一个根本性矛盾：现有矩阵极分解（polar decomposition）方法在深度学习场景中无法同时满足**初期快速收敛**、**最终高精度**和**GPU友好**三个要求。经典方法如牛顿-舒尔茨（Newton-Schulz）迭代仅依赖矩阵乘法，但初期进展缓慢；近期启发式方法（Jordan、You）初期快却最终不收敛，误差停滞。同时，大多数高精度方法依赖矩阵求逆或QR分解，无法充分利用GPU并行能力。

Polar Express 的核心设计理念是：**将极分解的逼近问题转化为每一步动态选择最优奇数多项式的极小化极大（minimax）问题**，使得整个多项式复合在 supremum 范数下是最优的。这一策略既能实现初期的快速推进，又能保证超指数收敛，且整个过程只使用矩阵乘法和线性组合，非常适合GPU计算。

### 整体Pipeline

Polar Express 的整体流程分为**离线预计算**和**在线迭代评估**两个阶段，如 Algorithm 1 所述：

```
Algorithm 1: Polar Express

离线阶段（float64精度，仅执行一次）:
  给定: 初始下界 ℓ₁, 多项式次数 d, 迭代次数 T
  for t = 1 to T:
    使用 Remez 算法求解:
      p_t = argmin_{p ∈ P_d^odd} max_{x ∈ [max(ℓ_t, u_t/10), u_t]} |1 - p(x)|
    更新区间:
      ℓ_{t+1} = p_t(ℓ_t)
      u_{t+1} = 2 - ℓ_{t+1}
  保存多项式系数 {a_t, b_t, c_t}（d=5时）

在线阶段（bfloat16精度，每次优化步执行）:
  输入: 动量矩阵 M
  初始化: X₀ = M / (||M||_F + 10⁻²)
  for t = 1 to T:
    Y = X_{t-1}^T X_{t-1}
    X_t = X_{t-1} (a_t I + Y (b_t I + c_t Y))   [Horner规则]
  输出: X_T ≈ polar(M)
```

### 模块关系与数据流

整个系统由三个核心模块构成，数据流单向传递：

1. **离线多项式预计算模块**：在 float64 精度下，使用 Remez 算法（或 d=3,5 时的闭式解）预先为一系列区间 [ℓ_t, u_t] 计算最优奇数多项式系数。该模块仅执行一次，输出一组系数 {a_t, b_t, c_t} 供在线阶段使用。

2. **在线迭代评估模块**：在 bfloat16 精度下，接收动量矩阵 M，先进行归一化处理（除以 ||M||_F + 10⁻²），然后应用预计算的多项式通过 Horner 规则迭代更新矩阵。每次迭代仅需一次矩阵乘法（计算 Y = X^T X）和若干线性组合操作。

3. **矩形矩阵快速迭代模块（可选）**：针对高宽比矩阵（α = m/n ≫ 1），通过仅两次矩形矩阵乘法计算所有 T 次迭代，结合重启策略保证数值稳定性。该模块可显著降低运行时间：α=4 时约 2 倍加速，α=32 时约 5 倍加速。

### 关键设计决策

| 设计要素 | 传统做法 | Polar Express 方案 | 依据 |
|---------|---------|-------------------|------|
| 迭代多项式 | 固定多项式（如牛顿-舒尔茨的 3 次或 5 次） | 每步贪婪选择当前区间上的 minimax 最优多项式 | Theorem 3.1：整体复合最优 |
| 奇异值归一化 | 仅用 ||M||_F | 除以 ||M||_F + 10⁻²，并引入 1.01 安全因子 | Section 3.4 & Appendix G：bfloat16 稳定性 |
| 区间下界 ℓ | 需精确估计或保守小值 | 固定 ℓ = 10⁻³，当 ℓ_t < u_t/10 时视为 u_t/10 | Section 3.3：针对 bfloat16 的补救措施 |

### 收敛性质

Polar Express 的收敛行为由两个定理保证：
- **Theorem 3.1**：贪婪构造的多项式复合 p* = p_T ∘ ... ∘ p_1 是 sign(x) 在 supremum 范数下的最优逼近。
- **Theorem 3.3**：对于 d = 2q+1 次多项式，误差随迭代次数超指数衰减：||polar(M) - X_T||₂ ≤ |1 - ℓ²|^{(q+1)^T}。d=5 时达到立方收敛。

实验表明，5~6 次 Polar Express 迭代足以使大于 10⁻³ 的奇异值近似收敛，满足 Muon 优化器对矩阵符号函数的精度需求；更多迭代或使用精确 SVD 不会进一步降低验证损失，但 SVD 会显著增加运行时间。

## 核心模块与公式推导

### 问题形式化与GPU约束

Polar Express 的目标是在仅使用 GPU 友好操作（矩阵乘法和线性组合）的约束下，求解矩阵极分解的最优多项式逼近。给定矩阵 $M \in \mathbb{R}^{m \times n}$，其极因子定义为：

$$\mathrm{polar}(M) := U V^{\mathsf{T}}$$

其中 $U \Sigma V^{\mathsf{T}}$ 是 $M$ 的奇异值分解。该方法寻找一系列奇数多项式 $p_1, p_2, \dots, p_T$，使得复合多项式 $p = p_T \circ p_{T-1} \circ \cdots \circ p_1$ 在谱范数下极小化最坏情况误差：

$$p^{\star} = \arg\min_{p = p_T \circ p_{T-1} \circ \cdots \circ p_1} \max_{M \in \mathbb{R}^{m \times n}} \| \mathrm{polar}(M) - p(M) \|_2$$

迭代评估通过 Horner 规则进行，仅需矩阵乘法：

$$X_0 = M, \quad X_t = p_t(X_{t-1}) \quad \text{for } t = 1, 2, \dots, T$$

奇数单项式的计算利用恒等式 $M^{2q+1} = M (M^{\top} M)^q$，将高次幂转化为矩阵乘法的组合。

### 贪婪最优多项式选择（核心机制）

Polar Express 的核心操作变量是每一步迭代所使用的奇数多项式。定理 3.1 证明：给定前序多项式的选择，当前步的多项式可以**贪婪地**选取，且最终得到的复合多项式在 supremum 范数下是 $\mathrm{sign}(x)$ 的最优逼近。

每一步的贪婪选择求解如下极小化极大（minimax）问题：

$$p_t = \underset{p \in \mathbb{P}_d^{\mathrm{odd}}}{\mathrm{arg\,min}} \underset{x \in [\ell_t, u_t]}{\mathrm{max}} |1 - p(x)|$$

其中 $[\ell_t, u_t]$ 是当前步奇异值所在的区间。该问题通过 Remez 算法离线求解（或对 $d=3,5$ 使用闭式解），得到最优奇数多项式的系数。

### 区间演化与误差传播

一旦 $p_t$ 确定，新区间仅需评估多项式在下界处的值即可获得：

$$\ell_{t+1} = p_t(\ell_t), \quad u_{t+1} = 2 - \ell_{t+1}$$

当前迭代的最大误差恰好为：

$$\max_{x \in [\ell_t, u_t]} |1 - p_t(x)| = 1 - \ell_{t+1}$$

最终 $T$ 步迭代后的谱范数误差有界：

$$\|\mathrm{polar}(M) - X_T\|_2 \leq 1 - \ell_{T+1}$$

### 超指数收敛速率

对于 $d = 2q+1$ 次多项式，Polar Express 的收敛速率由定理 3.3 给出：

$$\|\mathrm{polar}(M) - X_T\|_2 \leq |1 - \ell^2|^{(q+1)^T}$$

这意味着：$d=3$（即 $q=1$）时达到**二次收敛**，$d=5$（即 $q=2$）时达到**三次收敛**。误差随迭代次数 $T$ 呈超指数衰减，这是该方法同时实现初期快速推进和后期高精度的理论保证。

### bfloat16 稳定性修正

为适应半精度训练，Polar Express 引入了两项关键修正：

1. **安全因子**：将每个多项式替换为 $p_t(x/1.01)$，通过略微收缩自变量范围避免 bfloat16 下的数值溢出。
2. **区间下界缓冲**：当 $\ell_t < u_t/10$ 时，将 $\ell_t$ 视为 $u_t/10$ 进行多项式选择，避免极小奇异值导致的数值不稳定。实际实现中固定使用 $\ell = 10^{-3}$ 作为下界猜测。

初始归一化使用 $\|M\|_F + 10^{-2}$ 而非纯粹的 $\|M\|_F$，进一步提升了 bfloat16 下的鲁棒性。

### 算法流程

**离线阶段**（Algorithm 1）：在 float64 下使用 Remez 算法（或 $d=3,5$ 的闭式解）为一系列区间 $[\ell_t, u_t]$ 预计算最优奇数多项式系数，仅需执行一次。

**在线阶段**（Algorithm 1）：在 bfloat16 下应用预计算多项式，通过 Horner 规则迭代更新。以 5 次多项式 $p(x) = ax + bx^3 + cx^5$ 为例：

$$X_t = X_{t-1} (a I + Y_{t-1} (b I + c Y_{t-1})), \quad \text{where } Y_{t-1} = X_{t-1}^{\top} X_{t-1}$$

每次迭代仅需一次矩阵乘法（计算 $Y_{t-1}$）和若干线性组合，完全适配 GPU 并行特性。

## 实验与分析

### 主实验：GPT-2 语言模型训练

Polar Express 的核心验证场景是将其作为 Muon 优化器中极分解的计算后端，在 GPT-2 语言模型训练中评估对最终验证损失的影响。所有对比方法均使用 5 次迭代、bfloat16 精度，Muon 超参数保持一致（动量 0.9，无权重衰减），仅将 Muon 应用于二维及以上参数并排除 embedding 层。

**GPT-2-Large（774M）在 FineWeb 1B tokens 上的训练**（Figure 1）：
- muon-PolarExp（lr=0.02）达到最低验证损失 **3.340**，相比 muon-Jordan（3.398）降低 0.058，相比 muon-You（3.399）降低 0.059。
- 该优势在不同学习率下保持稳定，右图显示 Polar Express 在整个训练过程中的损失曲线始终低于其他变体。

**GPT-2-Small（124M）在 FineWeb 1B tokens 上的训练**（Figure 4，无权重衰减）：
- muon-PolarExp（lr=0.005）达到 **3.588**，优于 muon-Jordan（lr=0.01, 3.639）和 muon-You（lr=0.01, 3.629），分别降低 0.051 和 0.041。
- 作为参照，AdamW 的验证损失为 4.197，差距显著。

**GPT-2-Large（774M）在 FineWeb 10B tokens 上的训练**（Figure 6，有权重衰减 0.1）：
- muon-PolarExp（lr=0.002）达到 **2.913**，优于 muon-Jordan（2.921）和 muon-You（2.919）。
- 差距缩小至 0.006–0.008，表明在更大数据量和正则化条件下，Polar Express 仍保持一致但更温和的增益。

### 图像分类实验

在 CIFAR-10 上使用 ResNet-20 时（Figure 14），muon-PolarExp（lr=0.001）达到最佳验证准确率 **0.893**，略高于 muon-Jordan（0.891）和 muon-Newton（0.890），显著优于 AdamW（0.878）和 SGD-M（0.855）。所有结果在三个随机种子上取平均。

然而，在 CIFAR-10 ViT 任务上（Figure 16），muon-PolarExp（lr=10⁻⁵）准确率为 **0.860**，低于 muon-Newton（lr=10⁻⁴, 0.874）和 muon-You（lr=10⁻⁵, 0.865），仅略高于 AdamW（lr=10⁻³, 0.861）。这表明 Polar Express 在特定视觉架构上并非始终最优，可能需要针对此类任务进一步调优。

### 收敛性分析

**合成矩阵与真实梯度矩阵上的收敛**（Figure 3）：
- 在合成矩阵（σ_max=1, σ_min=10⁻⁶）上，Polar Express 经过 11 次迭代达到极高精度，收敛速度约为牛顿-舒尔茨的两倍。
- 在随机初始化 GPT-2 的梯度矩阵上，适当调优后的 Polar Express 在**每个迭代步**都优于牛顿-舒尔茨、Jordan 方法和 You 方法。
- 以 Frobenius 范数和余弦相似度度量时（Figure 8），Polar Express 同样保持优势。

**关键收敛特性**：
- 仅关注大于 σ_max/10³ 的奇异值时（Figure 10），Polar Express 在 5–6 次迭代内即近似收敛。这与 Muon 的实际需求一致——小奇异值方向对优化质量影响有限。
- 定理 3.3 保证的超指数收敛速率在实践中得到验证：d=5 时达到立方收敛，误差上界为 $|1 - \ell^2|^{(q+1)^T}$。

### 消融实验

**迭代次数与精确 SVD 的影响**（Figure 5）：
- 使用 5 或 6 次 Polar Express 迭代足以达到 Muon 所需精度；更多迭代（>6 次）或直接使用 SVD 不会进一步降低验证损失。
- 运行时对迭代次数不敏感，但 SVD 显著增加运行时间。这说明 5 次迭代在精度-效率上达到最佳平衡。

**小奇异值方向处理方式**（Figure 9）：
- 比较了精确映射（所有奇异值→1）、截断（小于 γ 的奇异值→0）和反转（小于 γ 的奇异值→−1）三种策略。
- 当截断阈值 γ ≈ 10⁻³ 时，三种策略表现接近。这是因为 5 次 Polar Express 迭代恰好使大于 10⁻³ 的奇异值近似收敛，小奇异值方向无论如何处理对优化影响都很小。

**谱感知初始化**（Figure 17）：
- 针对具有大奇异值间隙的矩阵（如幂律衰减谱 σ_j(M) = j⁻⁵），谱感知初始化可显著加速牛顿-舒尔茨和 Polar Express 的收敛。
- 代价是额外一次迭代的矩阵乘法开销。

**矩形矩阵快速迭代**（Figure 18）：
- Algorithm 3 在高宽比矩阵上显著降低运行时间：宽高比 α=4 时约 2 倍加速，α=32 时约 5 倍加速。
- 但在当前 GPT-2 规模实验中，这一加速尚未转化为实际运行时间收益，其效果可能依赖于模型规模和具体实现。

**数值稳定性措施**（Figure 7）：
- 使用安全因子（将多项式参数缩放 1/1.01）和缓冲修正（当 ℓ_t < u_t/10 时将其视为 u_t/10）可有效抑制 bfloat16 下的数值振荡。
- 蓝色曲线（原始最优多项式）在奇异值约 0.8 处出现大幅下冲，经过稳定化处理后（红色曲线）振荡显著减小。

### 失败模式与局限

1. **CIFAR-10 ViT 上的性能反转**：Polar Express 在该任务上不如牛顿-舒尔茨和 You 方法，说明其在视觉 Transformer 场景下的超参数（如学习率、迭代次数）可能需要针对性调整。

2. **矩形加速的规模依赖性**：Algorithm 3 的理论加速在 GPT-2 级别模型中尚未兑现，可能需要在更大规模模型（如 GPT-3 级别）或更高宽高比矩阵上才能体现实际 FLOP 节省。

3. **固定下界 ℓ 的假设**：Polar Express 依赖固定猜测 ℓ = 10⁻³（针对 bfloat16）。如果实际矩阵的最小奇异值远小于此值，早期收敛可能会减慢。自适应估计 ℓ（如幂方法动态跟踪最小奇异值）是一个待探索的方向。

4. **精度方案的限制**：所有实验均在 bfloat16 下完成，对于其他半精度（如 float16）或混合精度方案的鲁棒性尚未全面验证。

5. **未完全收敛即饱和的现象**：尽管 5 次迭代后 Polar Express 在 Frobenius 范数下尚未完全收敛，但优化性能已饱和——这一现象的原因尚不明确，是开放问题之一。

## 方法谱系与知识库定位

### 极分解的矩阵符号方法谱系

Polar Express 所解决的核心问题是**仅使用矩阵乘法计算矩阵极分解（polar decomposition）**，这一约束源于深度学习场景对 GPU 并行性的极致追求。该谱系可追溯至经典的 **Newton-Schulz** 迭代（Higham, 2008, Chapter 8），其核心是一个固定的三次或五次奇数多项式更新：

$$X_{t+1} = \frac{3}{2} X_t - \frac{1}{2} X_t X_t^\top X_t$$

该方法完全由矩阵乘法和线性组合构成，GPU 友好性极佳，但存在**初期收敛缓慢**的固有缺陷——在奇异值远离 1 的区间上，固定多项式无法快速推进。

近期工作试图通过启发式搜索更优的多项式来弥补这一缺陷。**Jordan's method**（Jordan et al., 2024b）针对低精度区域设计多项式，初期收敛快，但最终不收敛，误差停滞在约 0.3 的水平。**You's method**（Cesista et al., 2025）采用六个连续不同多项式的启发式更新，精度优于 Jordan 方法，但仍无法实现最终收敛。这两类方法的共同瓶颈在于：**多项式选择缺乏理论保证**，无法同时兼顾初期快速推进和终期超指数收敛。

### Polar Express 的核心突破

Polar Express 将上述谱系推进至**理论最优**的层面。其核心操作是将每一步的多项式选择形式化为一个极小化极大（minimax）问题：

$$p_t = \underset{p \in \mathbb{P}_d^{\mathrm{odd}}}{\mathrm{arg\,min}} \underset{x \in [\ell_t, u_t]}{\mathrm{max}} |1 - p(x)|$$

这一设计的因果逻辑链清晰：**每一步贪婪地选择当前奇异值区间上的最优逼近多项式 → 整体多项式复合在 supremum 范数下达到最优（定理 3.1）→ 误差以超指数速率衰减（定理 3.3）**。对于五次多项式（d=5），收敛速率达到立方级别：

$$\|\mathrm{polar}(M) - X_T\|_2 \leq |1 - \ell^2|^{3^T}$$

这一理论保证是 Newton-Schulz、Jordan、You 等方法所不具备的。Newton-Schulz 虽然也具有超指数收敛性质，但其固定多项式无法在初期自适应调整；Jordan 和 You 方法则完全缺乏收敛性证明。

### 与 Muon 优化器的关系

Polar Express 的直接应用场景是 **Muon 优化器**，后者使用动量梯度矩阵的极分解作为下降方向：

$$W_{t+1} = W_t - \lambda \cdot \mathrm{polar}(M_t)$$

在 Muon 的语境下，Polar Express 替代了此前 Jordan 方法或 Newton-Schulz 的极分解实现。关键发现是：**5~6 次 Polar Express 迭代即可使大于 10⁻³ 的奇异值近似收敛**（图 10），进一步增加迭代次数或使用精确 SVD 不会改善最终验证损失（图 5）。这一现象暗示 Muon 的优化性能对极分解精度的需求存在一个“饱和点”——该饱和点的存在机制目前仍是开放问题。

### 适用边界与局限

**数值精度依赖**：Polar Express 的所有实验均在 bfloat16 下进行，且依赖多项安全措施来保证稳定性——包括使用 $\|M\|_F + 10^{-2}$ 归一化、引入 1.01 安全因子缩放多项式输入、以及对早期迭代使用略微次优但振荡更小的多项式（附录 G）。对于其他半精度或混合精度方案的鲁棒性尚未全面验证。

**奇异值下界的固定假设**：算法固定使用 $\ell = 10^{-3}$ 作为奇异值下界的估计，并辅以补救措施（当 $\ell_t < u_t/10$ 时将其视为 $u_t/10$）。如果实际矩阵的最小奇异值远小于此值，早期收敛可能减慢。自适应估计 $\ell$（如通过幂方法动态跟踪最小奇异值）是潜在的改进方向。

**视觉任务的非普适优势**：在 CIFAR-10 ViT 上，Polar Express 验证准确率（0.860）低于 Newton-Schulz（0.874）和 You 方法（0.865），说明其在卷积/注意力混合架构上的优势并非绝对，可能需要针对不同任务族进行超参数调优。

**矩形加速的规模门槛**：针对高宽比矩阵的快速迭代算法（Algorithm 3）在 $\alpha=4$ 时约 2 倍加速，$\alpha=32$ 时约 5 倍加速（图 18），但在实际 GPT-2 规模训练中尚未带来显著的运行时间收益。该方法的实际 FLOP 节省可能需要更大规模模型（如 GPT-3 级别）才能显现。

### 开放问题

1. **优化饱和机制**：为何 Muon 中 5~6 次迭代后 Polar Express 在 Frobenius 范数下还未完全收敛，但优化性能已饱和？小奇异方向的处理方式（精确、截断、反转）对优化质量影响很小（图 9），这一现象的理论解释尚缺。

2. **自适应 $\ell$ 估计**：能否通过在线估计最小奇异值来动态调整区间下界，从而在保持鲁棒性的同时进一步加速初期收敛？

3. **更大规模的验证**：Polar Express 在 GPT-3 级别模型上的表现，以及矩形加速算法是否能在此规模实现实际 FLOP 节省，仍需实验确认。

4. **跨精度泛化**：当前的安全措施专为 bfloat16 设计，向 FP8 等更低精度格式的迁移可能需要重新设计稳定化策略。

## 原文 PDF

![[paperPDFs/ICLR_2026/The_Polar_Express_Optimal_Matrix_Sign_Methods_and_their_Application_to_the_Muon_Algorithm.pdf]]
