---
title: "High-dimensional limit theorems for SGD: Momentum and Adaptive Step-sizes"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/High_dimensional_limit_theorems_for_SGD_Momentum_and_Adaptive_Step_sizes.pdf
project_link: null
code_link: null
openreview_forum_id: 5OJLOwwXV4
aliases:
- SMSMSSU
- HDLTSMASS
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/learning_theory
core_operator: "有效步长 δ/(1-β) 及校正项加权 δ/(1-β)²，即步长与动量参数的相对比例。"
primary_logic: "SGD-M 与在线 SGD 的临界步长标度相同，但动量强化了人口校正项，使动力学更远离最优解。通过适当调整步长可达到与在线 SGD 的动力学等价（仅差时间重标度），而采用单位梯度归一化的 SGD-U 能够提供更优的不动点并扩大容许步长范围，从而在理论层面解释早期预条件器如何稳定和改善高维优化。"
claims:
- "在临界步长范围内，SGD-M 放大高维效应，可能使动力学更偏离总体梯度。"
- "SGD-U 展现出更优的不动点并显著扩大收敛到这些解的容许步长范围。"
- "通过时间重标度和步长调整，SGD-M 与在线 SGD 的有效动力学等价。"
- "高维极限定理（Theorem 2.3）将 SGD-M 的摘要统计量收敛描述为一个随机微分方程。"
---

# High-dimensional limit theorems for SGD: Momentum and Adaptive Step-sizes

> [!tip] 核心洞察
> SGD-M 与在线 SGD 的临界步长标度相同，但动量强化了人口校正项，使动力学更远离最优解。通过适当调整步长可达到与在线 SGD 的动力学等价（仅差时间重标度），而采用单位梯度归一化的 SGD-U 能够提供更优的不动点并扩大容许步长范围，从而在理论层面解释早期预条件器如何稳定和改善高维优化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 随机梯度下降动量与自适应步长的高维极限定理 |
| 英文题名 | High-dimensional limit theorems for SGD: Momentum and Adaptive Step-sizes |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=5OJLOwwXV4) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/learning_theory |
| Method | SGD with momentum (SGD-M) 及带有梯度单位范数预条件的 SGD（SGD-U）的高维标度极限框架 |
| Dataset | Spiked Tensor / Matrix PCA, Single Index Model (f(x)=x^7+4x^4 with noise), Matrix PCA (diffusive limit around m=0) |

> [!tip] 效果简介
> - Spiked Tensor / Matrix PCA 上，|m(t)/R(t)| （与真实方向的对齐程度） 为 SGD-U 在 λ=0.8 时依然处于超临界状态（能收敛到非零 m 不动点），对比 online SGD 和 SGD-M 在 λ=0.8 时为亚临界（无法收敛到有信号的不动点），变化 SGD-U 在更弱的信号下即可实现方向恢复。
> - Single Index Model (f(x)=x^7+4x^4 with noise) 上，|m/R| 随训练步数的演变 为 SGD-U 在 c_δ=10^{-k} 下收敛到接近 1 的稳定值，对比 online SGD 需要 c_δ ≤ 10^{-10} 才能避免梯度爆炸，否则无法进展，变化 SGD-U 允许大几个数量级的步长且仍能收敛。
> - Matrix PCA (diffusive limit around m=0) 上，重标度统计量 √n m(t) 的波动性 为 SGD-M 的波动性随 β 增大而显著增强，对比 online SGD (β=0) 波动性最小，变化 动量使扩散项放大 1/(1-β) 倍。

## 概要

本文研究带 Polyak 动量的随机梯度下降（SGD-M）及自适应步长 SGD（SGD-U）在高维极限下的动力学行为。核心问题在于：在临界步长标度下，动量与自适应预条件器如何改变优化轨迹的有效漂移与扩散特性。

**问题瓶颈**：SGD-M 与在线 SGD 共享相同的临界步长标度，但动量通过因子 $1/(1-\beta)$ 和 $1/(1-\beta)^2$ 分别缩放信号项与人口校正项，使校正项权重相对增强，可能将动力学推离总体梯度方向。SGD-U 则通过单位梯度归一化改变 ODE 结构，展现出更优的不动点并显著扩大容许步长范围。

**方法定位**：本文扩展了 Ben Arous 等人（2024）的有效动力学框架，通过定义 $\delta_n$-可局部化与渐近可闭性条件，将 SGD-M 和 SGD-U 的高维参数演化压缩为低维摘要统计量的随机微分方程（SDE）。关键推导步骤包括：选择摘要统计量、验证局部化与可闭性、计算有效漂移 $\mathbf{h}$ 与波动率 $\mathbf{\Sigma}$，最终得到极限 SDE

$$\mathrm{d} \mathbf{u}_t = \mathbf{h}(\beta, \mathbf{u}_t) \mathrm{d} t + \frac{1}{1-\beta} \sqrt{\Sigma(\mathbf{u}_t)} \mathrm{d} \mathbf{B}_t.$$

**主要结果**：
- 在 Spiked Tensor/Matrix PCA 上，SGD-U 在更弱信噪比下仍保持超临界（Figure 1 中 $\lambda=0.8$ 仅 SGD-U 收敛到非零不动点）；SGD-M 的临界 $\lambda$ 高于 SGD-U，且动量增大波动性（Figure 2）。
- 在单指标模型中，SGD-U 允许比在线 SGD 大数个数量级的步长，且仍能收敛到接近最优的不动点（Figure 3）。
- 理论层面，通过将 SGD-M 的步长重标定为 $\delta/(1-\beta)$，可恢复与在线 SGD 等价的动力学（仅差时间重标度），建立了算法间的等价关系。

**局限与开放问题**：当前分析限于标量预条件器（梯度归一化），未涵盖矩阵形式自适应方法（如 Adam）；推导依赖在线流式数据和高维极限标度，中等维度下的实用性待验证；缺乏真实数据集评估。



高维非凸优化中，随机梯度下降（SGD）的动力学行为已通过“有效动力学”框架得到系统刻画。该框架将高维参数向量的演化压缩为一组低维摘要统计量，并在临界步长标度 $\delta_n \sim 1/n$ 下导出随机微分方程（SDE）极限。然而，现有理论主要局限于标准在线 SGD，未覆盖实际训练中广泛使用的动量方法与自适应步长机制。

本文的核心动机在于填补这一理论缺口：**将有效动力学框架推广至 Polyak 动量 SGD（SGD-M）和带有梯度单位范数预条件的 SGD（SGD-U）**。这一推广并非平凡的参数替换——动量与自适应步长在高维极限下引入了质变的动力学效应，需要重新分析漂移项与扩散项的结构。

具体而言，现有框架面临三个关键缺口：

1. **动量如何改变临界标度与高维校正**：在线 SGD 的临界步长标度为 $\delta_n = c_\delta / n$。SGD-M 是否保持相同标度？动量参数 $\beta$ 如何介入漂移与扩散项，是否会放大或抑制高维效应？

2. **自适应步长能否缓解高维校正**：高维优化中存在“人口校正项”（population corrector），使动力学偏离真实总体梯度方向。简单的标量预条件器（如梯度归一化）能否在理论层面解释其稳定化效果，并扩大容许步长范围？

3. **不同算法间的动力学等价性**：SGD-M、SGD-U 与在线 SGD 之间是否存在通过步长重标度或时间重参数化建立的精确等价关系？

本文通过统一的渐近分析框架回答了上述问题。核心发现是：SGD-M 与在线 SGD 共享相同的临界步长标度，但动量通过因子 $1/(1-\beta)$ 放大扩散项，并通过 $1/(1-\beta)^2$ 重加权人口校正项，使得动力学更远离最优解；而 SGD-U 则展现出更优的不动点，并显著扩大收敛到这些解的容许步长范围。这些结果从高维极限理论的角度，为动量与自适应步长的实际效果提供了机理性解释。



## 核心方法与创新机理

本文的核心创新在于将高维极限有效动力学框架从标准在线 SGD 推广到两类重要的优化变体——带动量的 SGD（SGD-M）和带梯度单位范数预条件的 SGD（SGD-U），从而在统一的标度极限下揭示了动量与自适应步长对高维优化动力学的根本性影响。

### 关键发现：动量放大高维校正效应

理论分析表明，SGD-M 与在线 SGD 共享相同的临界步长标度（$\delta_n = c_\delta / n$），但动量参数 $\beta$ 显著改变了有效动力学的结构。具体而言，极限随机微分方程（SDE）中漂移项的分解揭示了动量对信号项与校正项的不对称重标度：

$$
\mathrm{d} \mathbf{u}_t = \left[ -\frac{1}{1-\beta} \mathbf{f}(\mathbf{u}_t) + \frac{1}{(1-\beta)^2} \mathbf{g}(\mathbf{u}_t) \right] \mathrm{d} t + \frac{1}{1-\beta} \sqrt{\mathbf{\Sigma}(\mathbf{u}_t)} \mathrm{d} \mathbf{B}_t
$$

其中 $\mathbf{f}$ 代表总体梯度方向（信号项），$\mathbf{g}$ 代表由随机梯度方差驱动的人口校正项。动量使信号项仅被 $1/(1-\beta)$ 缩放，而校正项则被 $1/(1-\beta)^2$ 放大。**当 $\beta \to 1$ 时，校正项相对于信号项的影响急剧增强，可能导致动力学被校正项主导，从而偏离真正的总体梯度方向**（confidence 0.9）。这一现象在 Matrix PCA 的扩散极限模拟中得到验证：随着 $\beta$ 增大，SGD-M 在 $m=0$ 附近的波动性显著增强（Figure 2），直接反映了扩散项被 $1/(1-\beta)$ 放大的理论预测。

### 步长重标度等价性

尽管动量引入了额外的复杂性，论文证明了一个重要的等价关系：**对于 SGD-M 的任意步长 $\delta_n$，存在一个对应的在线 SGD 步长 $\delta_n/(1-\beta)$，使得两者的有效动力学在时间重标度 $t \to t/(1-\beta)$ 下完全一致**（confidence 0.95）。这意味着动量本质上可以通过适当调整在线 SGD 的步长来模拟，但前提是必须在临界标度内操作。

### SGD-U：单位梯度归一化的突破性优势

更具根本性的创新来自 SGD-U 的分析。该方法采用标量预条件器 $\eta(x, Y) = \sqrt{n} / \|\nabla L(x, Y)\|$，将每次更新的梯度归一化为单位范数。高维极限分析揭示了 SGD-U 的两个关键优势：

1. **更优的不动点**：在张量 PCA 问题中，SGD-U 的有效 ODE 结构（Proposition 3.1）使得不动点比 SGD-M 更接近真实方向。临界信噪比的对比直接量化了这一优势——对于 $k=2$：
   $$
   \lambda_{\text{crit}}^M(2,\beta,c_\delta) = \frac{c_\delta}{1-\beta}, \qquad \lambda_{\text{crit}}^U(2,c_\delta) = \left(\frac{c_\delta}{2\sqrt{2}}\right)^{2/3}
   $$
   SGD-U 的临界 $\lambda$ 显著更小，意味着**在更弱的信号下即可收敛到非平凡解**（confidence 0.9）。

2. **显著扩大的容许步长范围**：在单指标模型的实验中（Figure 3），SGD-U 在 $c_\delta = 10^{-k}$ 时即可收敛到接近 1 的稳定值，而标准 SGD 对于 $f(x)=x^7+4x^4$ 需要 $c_\delta \leq 10^{-10}$ 才能避免梯度爆炸。**SGD-U 允许大几个数量级的步长且仍能收敛**（confidence 0.9）。

### 理论框架的推广

论文还将有效动力学框架推广到一般的标量马尔可夫预条件器（Appendix A，Theorem A.3），定义了 $(\delta_n, \eta_n)$-局部化与渐近可闭性的充分条件。这为未来分析更复杂的自适应方法（如基于历史梯度统计的预条件器）奠定了理论基础。

**需要手动验证的点**：论文仅研究了标量预条件器，未涉及矩阵形式的自适应方法（如 AdaGrad、Adam），且实验均为模拟验证，缺乏真实数据集评估。对于中等维度或非渐近条件下的实用性，理论预测的步长优势是否仍然成立有待进一步验证。



本文构建了一个统一的“有效动力学”极限框架，用于分析带 Polyak 动量（SGD‑M）和带标量自适应步长（SGD‑U）的在线随机梯度下降在高维极限下的行为。该框架将 Ben Arous 等人（2024）的方法从无动量情形推广到动量与预条件器并存的情形，核心思路是将高维参数向量的演化压缩为一组低维摘要统计量的随机微分方程（SDE）。

### 框架的模块化流程

整个分析管线由四个核心模块串联而成，从算法定义到极限 SDE 的严格推导形成一个闭环：

1. **摘要统计量选择**  
   首先定义一组低维函数 $u_n(x) = (u_1^n(x), \dots, u_k^n(x))$，用以刻画高维参数向量 $x \in \mathbb{R}^n$ 的关键特征（如与真实信号方向的重叠 $m$、残差范数 $r^2$ 等）。这些统计量是后续降维分析的对象。

2. **$\delta_n$-局部化与渐近可闭性验证**  
   这是框架的“准入条件”模块。需验证所选统计量满足两项技术条件：
   - **$\delta_n$-局部化**（Definition 2.1）：统计量及其导数在局部紧集上具有一致有界性，保证梯度噪声不会使过程逃逸出有效域。
   - **渐近可闭性**（Definition 2.2）：一阶微分算子（漂移）和二阶微分算子（波动率）作用于统计量后，其极限形式可表示为仅依赖于统计量自身的函数。即存在漂移函数 $\mathbf{h}$ 和波动率矩阵 $\Sigma$，使得在统计量的紧子集上一致地有：
     $$ \sup_{x \in u_n^{-1}(E_K)} \left\| \left( -\frac{1}{1-\beta} \mathcal{A}_n + \frac{1}{(1-\beta)^2} \delta_n \mathcal{L}_n \right) u_n(x) - \mathbf{h}(\beta, u_n(x)) \right\| \to 0, $$
     以及波动率的相应收敛条件。此处的 $\mathcal{A}_n$ 和 $\mathcal{L}_n$ 分别对应总体梯度漂移和梯度协方差扩散算子。

3. **有效漂移与波动率计算**  
   在可闭性成立的前提下，通过取极限得到低维动力学的系数函数：
   - 漂移项 $\mathbf{h}(\beta, \mathbf{u})$ 由总体梯度的一阶效应和梯度方差的二阶效应共同构成，其具体形式依赖于动量参数 $\beta$ 和步长标度 $\delta_n$。
   - 波动率矩阵 $\Sigma(\mathbf{u})$ 刻画了随机梯度噪声在统计量空间中的扩散强度。动量使扩散项放大 $1/(1-\beta)$ 倍（见 Theorem 2.3）。

4. **随机微分方程极限推导**  
   利用辅助过程构造（Doob 分解）、鞅方法及 Kolmogorov 连续性定理，证明摘要统计量的分段常数插值过程在 $C([0,T])$ 上弱收敛于以下 SDE 的解：
   $$ \mathrm{d} \mathbf{u}_t = \mathbf{h}(\beta, \mathbf{u}_t) \mathrm{d} t + \frac{1}{1-\beta} \sqrt{\Sigma(\mathbf{u}_t)} \mathrm{d} \mathbf{B}_t. $$
   这是 Theorem 2.3 的核心结论。当漂移项可进一步分解为信号项 $\mathbf{f}$ 和人口校正项 $\mathbf{g}$ 时（Remark 2.4），动力学呈现以下结构：
   $$ \mathrm{d} \mathbf{u}_t = \left[ -\frac{1}{1-\beta} \mathbf{f}(\mathbf{u}_t) + \frac{1}{(1-\beta)^2} \mathbf{g}(\mathbf{u}_t) \right] \mathrm{d} t + \frac{1}{1-\beta} \sqrt{\mathbf{\Sigma}(\mathbf{u}_t)} \mathrm{d} \mathbf{B}_t. $$
   该分解揭示了动量的双重效应：信号项被 $1/(1-\beta)$ 缩放，而校正项被 $1/(1-\beta)^2$ 缩放，后者在 $\beta \to 1$ 时显著增强。

### 输入输出流

- **输入**：在线数据流 $\{y_\ell\}$、损失函数 $L_n(x, y)$、步长序列 $\delta_n$、动量参数 $\beta \in [0,1)$（SGD‑M）或标量预条件器 $\eta(x, Y)$（SGD‑U）。
- **处理**：通过局部化和可闭性验证，将高维随机迭代映射为低维确定性的 ODE/SDE 系统。
- **输出**：摘要统计量 $\mathbf{u}_t$ 的极限动力学（ODE 或 SDE），直接给出算法在总体水平上的收敛性、不动点位置、稳定条件和相变边界。

### 两种算法的框架实例化

- **SGD‑M**：更新规则为 $p_\ell = \beta p_{\ell-1} - \delta_n \nabla L_n(x_{\ell-1}, y_\ell)$, $x_\ell = x_{\ell-1} + p_\ell$。临界步长标度为 $\delta_n = c_\delta / n$，与在线 SGD 相同，但动量通过 $\beta$ 重新加权了漂移项中的信号与校正项比例。
- **SGD‑U**：在标准 SGD 基础上引入梯度范数归一化的标量预条件器 $\eta(x, Y) = \sqrt{n} / \|\nabla L(x, Y)\|$。该预条件器改变了有效漂移和波动率的结构，使得不动点更接近总体最优解，并显著拓宽了允许收敛的步长范围（在张量 PCA 中 $\lambda_{\text{crit}}^U < \lambda_{\text{crit}}^M$，见 Section 3.1）。

### 证据强度说明

上述框架的数学严格性由 Theorem 2.3 及其在附录 B 中的完整证明保证（置信度 0.95）。动量对扩散项的放大效应、校正项的相对权重变化，以及 SGD‑U 的优越不动点性质，均在正文的解析推导和 Figure 1–3 的模拟验证中得到一致支持（置信度 0.9–0.95）。但需注意，框架目前仅覆盖标量预条件器，向矩阵预条件器（如 Adam）的推广仍是开放问题。



### 摘要统计量与可闭性框架

论文将高维参数向量 $x \in \mathbb{R}^n$ 的动力学压缩为一组低维摘要统计量 $u_n(x) = (u_1^n(x), \dots, u_k^n(x))$。推导极限 SDE 的核心在于验证两个充分条件：

**Definition 2.1（$\delta_n$-局部化）**：存在递增紧集序列 $(E_K)_K$，使得摘要统计量在该序列上具有一致的正则性（梯度有界、Hessian 有界等），且 SGD 迭代以高概率停留在这些紧集内。

**Definition 2.2（渐近可闭性）**：在 $\delta_n$-局部化条件下，要求一阶和二阶微分算子的极限系数仅通过 $u_n(x)$ 依赖于 $x$，即存在函数 $h$ 和 $\Sigma$ 使得

$$
\sup_{x \in u_n^{-1}(E_K)} \left\| \left(-\frac{1}{1-\beta} A_n + \frac{1}{(1-\beta)^2} \delta_n L_n\right) u_n(x) - h(\beta, u_n(x)) \right\| \to 0,
$$

二阶算子 $L_n$ 类似地收敛到 $\Sigma$。这里 $A_n$ 为总体漂移算子，$L_n$ 为梯度协方差算子（人口校正项）。

### 极限 SDE 与动量效应

**Theorem 2.3**：若上述条件满足，则 SGD-M 的摘要统计量弱收敛到如下 SDE 的解：

$$
\mathrm{d} \mathbf{u}_t = \mathbf{h}(\beta, \mathbf{u}_t) \mathrm{d} t + \frac{1}{1-\beta} \sqrt{\Sigma(\mathbf{u}_t)} \mathrm{d} \mathbf{B}_t.
$$

**Remark 2.4** 进一步将漂移分解为信号项 $f$ 与人口校正项 $g$：

$$
\mathrm{d} \mathbf{u}_t = \left[ -\frac{1}{1-\beta} \mathbf{f}(\mathbf{u}_t) + \frac{1}{(1-\beta)^2} \mathbf{g}(\mathbf{u}_t) \right] \mathrm{d} t + \frac{1}{1-\beta} \sqrt{\mathbf{\Sigma}(\mathbf{u}_t)} \mathrm{d} \mathbf{B}_t.
$$

关键瓶颈在此显现：动量参数 $\beta$ 对信号项和校正项施加了**不同的重标度**——信号项被 $1/(1-\beta)$ 缩放，而校正项被 $1/(1-\beta)^2$ 缩放。当 $\beta \to 1$ 时，校正项相对于信号项的影响被显著放大，可能压倒真实梯度信号，使动力学偏离总体最优方向。同时，扩散项也被 $1/(1-\beta)$ 放大，增加了波动性。

**与在线 SGD 的等价性**：Remark 2.4 指出，若将 SGD-M 的步长重标定为 $\delta/(1-\beta)$，则其有效动力学与在线 SGD 仅差一个时间重标度 $t \to t/(1-\beta)$，建立了两种算法的动力学等价关系。

### Tensor PCA 下的有效 ODE

**Proposition 3.1** 给出了 Spiked Tensor PCA 模型下 SGD-M 和 SGD-U 的高维 ODE 极限。

SGD-M 的动力学（$m$ 为与真实方向的对齐度，$R^2 = m^2 + r^2$ 为参数范数）：

$$
\mathrm{d} m = \frac{1}{1-\beta} 2m (\lambda k m^{k-2} - k R^{2(k-1)}) \mathrm{d} t,
$$

$$
\mathrm{d} r^2 = -\frac{4k R^{2(k-1)}}{(1-\beta)^2} (r^2(1-\beta) - c_\delta) \mathrm{d} t.
$$

SGD-U 的动力学（$\eta(x,Y) = \sqrt{n}/\|\nabla L(x,Y)\|$）：

$$
\mathrm{d} m = \sqrt{k} \left( \lambda \left( \frac{m}{R} \right)^{k-1} - R^{k-1} m \right) \mathrm{d} t,
$$

$$
\mathrm{d} r^2 = -2\sqrt{k} \left( R^{k-1} r^2 - \frac{c_\delta}{2\sqrt{k}} \right) \mathrm{d} t.
$$

SGD-U 的 ODE 结构中，信号项与校正项的权重关系不同于 SGD-M，使得不动点更接近真实解。在 $k=2$（矩阵 PCA）时，两者的临界信噪比分别为：

$$
\lambda_{\mathrm{crit}}^M(2,\beta,c_\delta) = \frac{c_\delta}{1-\beta}, \qquad \lambda_{\mathrm{crit}}^U(2,c_\delta) = \left(\frac{c_\delta}{2\sqrt{2}}\right)^{2/3}.
$$

SGD-U 的临界 $\lambda$ 小于 SGD-M，意味着在更弱的信号下即可收敛到非零不动点。

### Single Index Model 下的动力学

**Proposition 3.5**：在单指标模型 $y = f(\langle a, x \rangle) + \varepsilon$ 下，SGD-M 的 $m$ 漂移为：

$$
\mathrm{d} m = \frac{-2}{(1-\beta)} \mathbb{E}[a_1 f'(m a_1 + r a_2)(f(m a_1 + r a_2) - f(a_1))] \mathrm{d} t.
$$

此时动力学仅包含一阶信号项，受 $1/(1-\beta)$ 缩放，但 $r^2$ 的演化中仍包含校正项。

**Proposition 3.8**：对于单项式连接函数 $f(x) = x^k$，SGD-M 在 $(1,0)$ 不动点局部稳定的充要条件为：

$$
0 < c_\delta < \frac{1-\beta}{k^2} \cdot \frac{(2k-3)!!}{(4k-5)!!}.
$$

该条件明确量化了动量 $\beta$ 和多项式次数 $k$ 对允许步长范围的约束。

**Proposition 3.9**：当噪声 $\sigma \to 0$ 时，SGD-U 对任何严格单调的连接函数都收敛到相同的极限 ODE：

$$
\mathrm{d} m = -\sqrt{\frac{2}{\pi}} \frac{m-1}{\sqrt{(m-1)^2+r^2}} \mathrm{d} t, \quad \mathrm{d} r^2 = \left[-\frac{2\sqrt{2/\pi} r^2}{\sqrt{(m-1)^2+r^2}} + c_\delta\right] \mathrm{d} t.
$$

该动力学具有唯一不动点 $(1, c_\delta^2 \pi/8)$，且不依赖于具体的 $f$ 形式，体现了 SGD-U 在小噪声极限下的通用性。

### Tensor PCA 的扩散极限

**Proposition 3.4** 给出了 SGD-U 下重标度统计量 $\tilde{m} = \sqrt{n} m$ 在 $m \approx 0$ 附近的扩散极限：

$$
\mathrm{d} \tilde{m} = \left( \lambda \left( \frac{\tilde{m}}{r} \right)^{k-1} \mathbb{1}_{k=2} - r^{k-1} \tilde{m} \right) \mathrm{d} t + \sqrt{c_\delta} \left( (k-1) \frac{\tilde{m}^2}{r^2} + 1 \right)^{1/2} \mathrm{d} B_t.
$$

与 SGD-M 不同，SGD-U 的扩散系数依赖于 $\tilde{m}$ 本身，不再是标准 OU 过程，这解释了其在弱信号下的均值排斥行为（Figure 2 中观察到）。



## 实验与关键发现

### 实验设置与基准任务

论文在两类高维统计模型上验证理论预测：**Spiked Tensor/Matrix PCA**（信号恢复任务）和**Single Index Model**（非线性回归任务）。所有实验均在在线流式数据设定下进行，维度 $n=10^4$，步长采用临界标度 $\delta_n = c_\delta / n$。对比方法包括 online SGD（$\beta=0$）、SGD-M（不同 $\beta$ 值）以及 SGD-U（梯度单位范数预条件）。

### 主结果

**SGD-U 在弱信号下保持超临界状态。** 在 Matrix PCA 任务中，Figure 1 展示了三种信噪比（$\lambda=0.8, 1.2, 2.2$）下统计量 $|m(t)/R(t)|$ 的演化。当 $\lambda=0.8$ 时，仅 SGD-U 处于超临界状态，能收敛到非零的 $m$ 不动点；online SGD 和 SGD-M 均为亚临界，无法实现方向恢复。当 $\lambda=1.2$ 时，SGD-U 和 online SGD 均超临界，但 SGD-U 获得与真实方向更好的对齐。当 $\lambda=2.2$ 时，仅 $\beta=0.9$ 的 SGD-M 表现为亚临界。这一结果直接验证了理论预测：SGD-U 的临界信噪比 $\lambda_{\text{crit}}^U(2,c_\delta) = (c_\delta/(2\sqrt{2}))^{2/3}$ 小于 SGD-M 的 $\lambda_{\text{crit}}^M(2,\beta,c_\delta) = c_\delta/(1-\beta)$，使其在更弱信号下即可分离出非平凡不动点。

![[assets/figures/papers/iclr26_0010_5OJLOwwXV4_High-dimensional_limit_theorems_for_SGD_Momentum/figures/003_Figure_1.jpg]]
*Figure 1: Matrix PCA in dimension n = 1 0 0 0 0 for $\lambda$ = 0 . 8 (left figure), $\lambda$ = 1 . 2 (middle figure), and $\lambda$ = 2 . 2 (right figure) with $c _ { \delta }$ = 1 . Depicted is the evolution of the statistic | m ( t ) / R ( t ) | for 20n steps with random initialization. We note that in the left figure, only SGD-U is supercritical. In the middle figure, both SGD-U and online SGD are supercritical, however the former attains better alignment with the direction vector v . The rightmost figure shows only SGD-M with $\beta$ = 0 . 9 as subcritical, however the alignment order is consistent

**SGD-U 允许大几个数量级的步长且仍能收敛。** 在 Single Index Model 实验中（Figure 3），对于连接函数 $f(x)=x^7+4x^4$，online SGD 需要 $c_\delta \leq 10^{-10}$ 才能避免梯度爆炸，否则训练无法进展；而 SGD-U 在 $c_\delta = 10^{-k}$（$k$ 为满足动力学的较小整数）下即可收敛到 $|m/R| \approx 1$ 的稳定值。对于 $f(x)=x^2$ 和 $f(x)=x^3$，SGD-U 同样以更大的有效步长实现收敛。这验证了 SGD-U 通过梯度归一化显著扩大了容许步长范围的理论优势。

![[assets/figures/papers/iclr26_0010_5OJLOwwXV4_High-dimensional_limit_theorems_for_SGD_Momentum/figures/007_Figure_3.jpg]]
*Figure 3: We plot the value of | m / R | over the course of training for independent runs of SGD (full lines) and SGD-U (dashed lines) for various functions f with different amounts of additive noise. We set n = 1 0 , 0 0 0 , $\delta = c _ { \delta }$ / n and the total number of steps is taken as one million. We consider f ( x ) = $x ^ { 2 }$ , f ( ${ \overset { . } { x } }$ ) = $x ^ { 3 }$ and $\dot { f }$ ( x ) = $x ^ { 7 }$ + 4 $x ^ { 4 }$ . In each case we choose $c _ { \delta }$ = 1 $0 ^ { - k }$ for the smallest integer k such that the dynamics are not effected by exploding gradients

**动量放大高维波动性。** Figure 2 展示了 Matrix PCA 在 $m=0$ 附近的重标度统计量 $\tilde{u}_1 = \sqrt{n} m(t)$ 的扩散极限行为。随着 $\beta$ 增大，SGD-M 的波动性显著增强——这与理论 SDE 中扩散项被放大 $1/(1-\beta)$ 倍的预测一致。相比之下，SGD-U 在较小 $\lambda$ 下呈现均值排斥行为，与 Figure 1 的超临界/亚临界特性一致。

![[assets/figures/papers/iclr26_0010_5OJLOwwXV4_High-dimensional_limit_theorems_for_SGD_Momentum/figures/006_Figure_2.jpg]]
*Figure 2: Matrix PCA in dimension n = 1 0 0 0 0 for $\lambda$ = 0 . 8 (left figure), $\lambda$ = 1 . 2 (middle figure), and $\lambda$ = 2 . 2 (right figure) with $c _ { \delta }$ = 1 . Depicted is the evolution of the rescaled statistic $\tilde { u } _ { 1 } = \sqrt { n }$ m ( t ) for 6n steps around a fixed window about m = 0 . . We note the increased volatility of the diffusive limits for SGD-M as $\beta$ increases. We see that SGD-U becomes mean repellent for smaller values of λ, similar to Figure 1

### 消融分析

**动量参数 $\beta$ 强化人口校正项。** 从有效动力学分解来看，SGD-M 的极限 SDE 为：
$$
\mathrm{d} \mathbf{u}_t = \left[ -\frac{1}{1-\beta} \mathbf{f}(\mathbf{u}_t) + \frac{1}{(1-\beta)^2} \mathbf{g}(\mathbf{u}_t) \right] \mathrm{d} t + \frac{1}{1-\beta} \sqrt{\mathbf{\Sigma}(\mathbf{u}_t)} \mathrm{d} \mathbf{B}_t
$$
其中 $\mathbf{f}$ 为总体漂移（信号项），$\mathbf{g}$ 为人口校正项（方差项）。当 $\beta \to 1$ 时，校正项 $\mathbf{g}$ 的权重 $1/(1-\beta)^2$ 相对于信号项 $\mathbf{f}$ 的权重 $1/(1-\beta)$ 增长更快，使得高维效应可能压倒底层信号，将动力学引离总体梯度方向。这一理论预测在 Figure 2 的波动性放大和 Figure 1 中高 $\beta$ SGD-M 的亚临界行为中得到验证。

**步长重标度可实现 SGD-M 与 online SGD 的动力学等价。** 若将 SGD-M 的步长调整为 $\delta_n/(1-\beta)$，其有效动力学在时间重标度 $t \to t/(1-\beta)$ 后与 online SGD 一致。这意味着动量本身并不改变动力学的定性结构，而是通过有效步长 $\delta/(1-\beta)$ 和校正项加权 $\delta/(1-\beta)^2$ 重新标度了各项的相对重要性。

**单项式连接函数的稳定条件。** 对于 $f(x)=x^k$，SGD-M 在不动点 $(1,0)$ 局部稳定的充要条件为：
$$
0 < c_\delta < \frac{1-\beta}{k^2} \cdot \frac{(2k-3)!!}{(4k-5)!!}
$$
该条件显式地刻画了步长参数、动量参数和连接函数非线性程度之间的约束关系。$k$ 越大，容许的 $c_\delta$ 范围越窄，解释了 Figure 3 中高次连接函数对步长的苛刻要求。

**SGD-U 的小噪声极限具有普适性。** 当噪声 $\sigma \to 0$ 时，对于任意严格单调的连接函数，SGD-U 的动力学收敛到相同的 ODE：
$$
\mathrm{d} m = -\sqrt{\frac{2}{\pi}} \frac{m-1}{\sqrt{(m-1)^2+r^2}} \mathrm{d} t, \quad \mathrm{d} r^2 = \left[-\frac{2\sqrt{2/\pi} r^2}{\sqrt{(m-1)^2+r^2}} + c_\delta\right] \mathrm{d} t
$$
该 ODE 具有唯一不动点 $(1, c_\delta^2\pi/8)$，且 $m$ 的固定点恰好为真实方向。这一普适性解释了 SGD-U 在不同连接函数下的一致优势。

### 失败模式与边界条件

**SGD-M 在临界步长下的性能退化。** 当步长处于临界标度时，动量放大人校正项可能导致动力学偏离总体梯度方向。在 Matrix PCA 实验中（Figure 1 右图），$\beta=0.9$ 的 SGD-M 在 $\lambda=2.2$ 时仍为亚临界，而 online SGD 和 SGD-U 均已收敛。这表明动量在临界区域并非无条件有益。

**SGD-U 的均值排斥行为。** 在较小 $\lambda$ 下（Figure 2 左图），SGD-U 在 $m=0$ 附近呈现均值排斥——即扩散过程倾向于远离零点。这与 SGD-U 在弱信号下仍能收敛到非零不动点的特性相关，但在极低信噪比下可能导致不稳定。

**高次连接函数的梯度爆炸。** 对于 $f(x)=x^7+4x^4$ 等高次连接函数，online SGD 需要极小的 $c_\delta$（$\leq 10^{-10}$）才能避免梯度爆炸。SGD-U 虽能缓解此问题，但仍需通过实验确定合适的 $c_\delta$ 值。

> **注意：** 以上失败模式均来自模拟实验，缺乏真实数据集验证。对于中等维度或非渐近步长的实用性，需进一步实验确认。



## 定位与知识库关联

### 与基准方法的关系

本文的核心理论框架直接继承自 Ben Arous 等人在在线 SGD 高维极限动力学方面的工作。基准方法为**无动量的在线 SGD**，其有效动力学在临界步长标度 $\delta_n \sim 1/n$ 下已由前人建立。本文在此基础上将框架**扩展至两个新方向**：

1. **Polyak 动量 SGD（SGD‑M）**：在基准在线 SGD 的更新规则中引入动量项 $p_\ell = \beta p_{\ell-1} - \delta_n \nabla L_n(x_{\ell-1}, y_\ell)$，其中 $\beta \in [0,1)$。当 $\beta=0$ 时退化回基准方法。

2. **单位梯度归一化的自适应 SGD（SGD‑U）**：在基准更新中引入标量预条件器 $\eta(x, Y) = \sqrt{n} / \|\nabla L(x, Y)\|$，使得每次更新的步长被梯度的范数自适应地调节。

从动力学等价性来看，SGD‑M 与在线 SGD 之间存在**精确的映射关系**：若将 SGD‑M 的步长重标定为 $\delta/(1-\beta)$，其有效动力学与在线 SGD 仅差一个时间重标度 $t \to t/(1-\beta)$（Remark 2.4）。这意味着动量本身并不改变临界步长的标度律，但会通过 $1/(1-\beta)$ 和 $1/(1-\beta)^2$ 的因子**重新加权漂移项中的信号分量 $f$ 与人口校正项 $g$**，使得校正项的影响随 $\beta \to 1$ 而被显著放大。

SGD‑U 则与上述两者有本质不同：其预条件器改变了梯度的有效方向（而不仅是幅度），导致极限 ODE 的结构发生根本变化，不动点的位置和稳定性条件均不可通过简单的步长重标度从 SGD‑M 或在线 SGD 导出。

### 适用边界

本框架的适用性受到以下关键假设的约束：

| 假设维度 | 具体约束 | 依据 |
|---------|---------|------|
| **数据分布** | 在线流式设置，每个样本 $(x_i, y_i)$ 独立同分布 | 全文基础假设 |
| **步长标度** | $\delta_n = c_\delta / n$，即步长与维度 $n$ 成反比 | Section 3.1 |
| **维度** | $n \to \infty$ 的高维极限，动力学由低维摘要统计量刻画 | Theorem 2.3 |
| **损失函数** | 需满足 $\delta_n$-局部化条件（Definition 2.1）和渐近可闭性（Definition 2.2） | Section 2 |
| **预条件器类型** | 仅研究了标量预条件器（梯度范数归一化），未涵盖矩阵形式 | Section 3, Appendix A |
| **连接函数** | 在单指标模型中假设 $f$ 已知且严格单调（小噪声极限下） | Section 3.2.1 |

特别值得注意的是，**临界步长标度 $\delta_n \sim 1/n$ 是框架成立的前提**。在此标度之外，高维效应与信号项的平衡将被打破，有效动力学的推导不再成立。

### 已知局限

1. **预条件器的覆盖范围有限**：本文仅分析了 SGD‑U 这一种特定的标量预条件器。更一般的标量预条件器在附录 A 中给出了理论框架（Theorem A.3），但未进行系统的实例分析和对比。**矩阵形式的自适应方法（如 AdaGrad、RMSProp、Adam）完全不在当前框架的覆盖范围内**，而这些方法在实践中的重要性远高于标量预条件器。

2. **数据设置的理想化**：分析基于在线流式 i.i.d. 数据，未涉及有限样本的多次遍历（multi-pass）、批量训练或非稳态分布偏移。在实际深度学习场景中，这些因素可能显著改变高维校正效应的表现。

3. **连接函数需已知**：在单指标模型的分析中，连接函数 $f$ 被假设为已知。实际应用中，模型结构（如神经网络架构）本身也在被学习，这引入了额外的耦合效应，当前理论无法直接处理。

4. **中等维度的实用性未验证**：所有理论预测均建立在 $n \to \infty$ 的渐近极限上。对于中等维度（如 $n=1000$）或非渐近步长，理论给出的步长优势和收敛性质是否仍然成立，需要进一步的经验研究来确认。论文中的模拟实验（$n=10000$）虽然与理论吻合良好，但这不能替代对更小维度的系统性验证。

5. **实验验证局限于模拟**：所有实验结果均来自合成数据上的模拟（Spiked Tensor/Matrix PCA 和 Single Index Model），**缺乏在真实数据集上的评估**。这使得理论预测在实际优化问题中的迁移性存在不确定性。

### 开放问题

1. **标量预条件器的系统理论**：能否建立一个统一的理论框架来分析和对比各类标量预条件器（如梯度范数归一化、梯度裁剪、符号梯度等）在高维极限下的动力学？不同预条件器对人口校正项的抑制机制是否存在共性？

2. **矩阵预条件器的高维极限**：AdaGrad、RMSProp 和 Adam 等矩阵形式的自适应方法在实践中占据主导地位。它们在高维极限下的有效动力学是什么？是否同样能够缓解人口校正效应？初步推测是，这些方法通过累积梯度二阶矩来构建预条件器，可能在极限下产生与 SGD‑U 不同的校正机制。

3. **非渐近与中等维度下的行为**：在 $n$ 固定且中等大小的情况下，理论预测的步长优势（如 SGD‑U 允许比 SGD 大几个数量级的步长）是否仍然成立？是否存在一个临界维度 $n_0$，使得当 $n > n_0$ 时渐近理论开始提供可靠的指导？

4. **动量与自适应步长的交互**：本文分别研究了动量（SGD‑M）和自适应步长（SGD‑U），但未分析二者**同时使用**时的动力学。在实践中，Adam 等方法同时包含动量和自适应预条件器，二者的交互效应可能产生非平凡的高维行为。

5. **非凸与非 i.i.d. 扩展**：当前框架依赖于损失函数在摘要统计量上的特定结构（如球对称性）。对于一般的非凸优化问题或非 i.i.d. 数据流（如强化学习中的策略梯度），能否建立类似的高维极限理论？分布偏移场景下的标度分析是一个重要但尚未触及的方向。

6. **理论指导下的算法设计**：基于本文揭示的机制——动量放大人口校正项而梯度归一化可抑制之——能否设计出新的自适应优化器，在理论上保证更优的不动点位置和更大的容许步长范围？这需要将当前的分析从标量预条件器推广到更实用的参数化预条件器族。



## 原文 PDF

![[paperPDFs/ICLR_2026/High_dimensional_limit_theorems_for_SGD_Momentum_and_Adaptive_Step_sizes.pdf]]
