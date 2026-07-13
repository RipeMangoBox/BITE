---
title: "A Recovery Guarantee for Sparse Neural Networks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Recovery_Guarantee_for_Sparse_Neural_Networks.pdf
project_link: null
code_link: null
aliases:
- IHTISMR
- RGSNN
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/learning_theory
core_operator: "将稀疏MLP优化重新表述为结构化线性感知问题，并利用凸松弛和迭代硬阈值（IHT）算法。"
primary_logic: "通过枚举或随机采样激活模式，将非凸的稀疏MLP训练转化为一个满足受限强凸性和受限光滑性的线性感知问题，从而保证IHT算法能以高概率精确恢复稀疏网络权重。"
claims:
- "IHT算法在满足Assumption 2的条件下，能以高概率精确恢复稀疏MLP权重。"
- "在随机高斯数据下，感知矩阵A以高概率满足受限强凸性和受限光滑性。"
- "Planted sparse scalar-output MLP (1-hidden-layer) 上 Average PSNR = IHT"
- "Planted sparse scalar-output MLP (2-hidden-layer) 上 Average PSNR = IHT"
---

# A Recovery Guarantee for Sparse Neural Networks

> [!tip] 核心洞察
> 通过枚举或随机采样激活模式，将非凸的稀疏MLP训练转化为一个满足受限强凸性和受限光滑性的线性感知问题，从而保证IHT算法能以高概率精确恢复稀疏网络权重。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 稀疏神经网络的可恢复性保证 |
| 英文题名 | A Recovery Guarantee for Sparse Neural Networks |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=6UpstNltZ4) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/learning_theory |
| Method | Iterative Hard Thresholding (IHT) for Sparse MLP Recovery |
| Dataset | Planted sparse scalar-output MLP (1-hidden-layer), Planted sparse scalar-output MLP (2-hidden-layer), Planted sparse vector-output MLP (1-hidden-layer), Planted sparse vector-output MLP (2-hidden-layer) |

> [!tip] 效果简介
> - Planted sparse scalar-output MLP (1-hidden-layer) 上，Average PSNR 为 IHT，对比 IMP，变化 IHT exhibits more robust performance。
> - Planted sparse scalar-output MLP (2-hidden-layer) 上，Average PSNR 为 IHT，对比 IMP，变化 IHT exhibits more robust performance。
> - Planted sparse vector-output MLP (1-hidden-layer) 上，Average PSNR 为 IHT，对比 IMP，变化 IHT is competitive。

## 概要

本文针对稀疏神经网络训练缺乏理论保证且内存效率与性能难以兼顾的瓶颈，提出了一种将稀疏MLP优化重构为结构化线性感知问题的方法。核心思路是通过固定生成器向量 $h_i$ 来枚举或随机采样激活模式，将非凸的两层ReLU网络转化为凸的线性感知问题：$\hat{y} = [\mathrm{diag}(\mathbb{I}\{X h_1 \geq 0\}) X \quad \ldots \quad \mathrm{diag}(\mathbb{I}\{X h_p \geq 0\}) X] [w_1; \ldots; w_p]$。这一转化使得优化目标从非凸的原始MLP损失变为凸的MSE损失，并允许使用迭代硬阈值（IHT）算法进行优化。

本文的核心理论贡献在于：在随机高斯数据条件下，证明了感知矩阵 $A$ 以高概率满足受限强凸性和受限光滑性，从而保证IHT算法能以高概率精确恢复稀疏网络权重。具体地，Theorem 1表明，在满足Assumption 2的条件下，经过 $K = O(\beta/\alpha \log(f(w^0)/\varepsilon))$ 步IHT迭代，可找到权重 $w^K$ 使得 $f(w^K) - f(w^\star) \leq \varepsilon$ 且 $\|w^K - w^\star\|_2^2 \leq 2\alpha^{-1}\varepsilon$。值得注意的是，该理论结果目前仅限于两层、标量输出的ReLU网络。

在实验方面，本文在planted稀疏MLP拟合、MNIST分类和隐式神经表示等任务上，将IHT与强基线方法迭代幅度剪枝（IMP）进行了比较。主要结果表明，IHT在多数场景下表现出更稳健的性能，且在整个优化过程中仅需与稀疏度 $s$ 成比例的固定参数预算，而IMP需要先训练参数数量随数据维度 $d$ 和隐藏维度 $m$ 增长的稠密网络。然而，实验规模较小，仅限于小规模MLP和图像过拟合任务，且顺序凸更新策略的收敛性缺乏理论保证。

深度神经网络的结构化稀疏性（即大部分权重为零）是降低模型存储与计算开销的关键手段。然而，现有稀疏网络训练方法存在两个根本性缺口：**缺乏理论保证**，以及**内存效率与最终性能难以兼得**。主流的迭代剪枝（Iterative Magnitude Pruning, IMP）方法虽然性能强劲，但其流程要求先完整训练一个稠密网络，再反复剪枝与微调——这导致训练过程中的内存占用与稠密网络规模成正比，违背了稀疏化的初衷。

本文的核心洞察是：**稀疏MLP的优化问题可以被重新表述为一个高度结构化的线性感知问题**，其中网络权重是待恢复的稀疏信号。具体而言，对于两层ReLU网络的标准非凸形式 $\hat{y} = \sum_{j=1}^{p} (X u_j)_+ v_j$，作者通过固定一组生成器向量 $h_i$ 来显式枚举或随机采样所有可能的激活模式，从而将问题凸化为：

$$\hat{y} = [\mathrm{diag}(\mathbb{I}\{X h_1 \geq 0\}) X \quad \ldots \quad \mathrm{diag}(\mathbb{I}\{X h_p \geq 0\}) X] [w_1; \ldots; w_p]$$

其中 $w_i = u_i v_i$ 是融合后的待恢复权重。这一凸松弛将非凸的激活模式学习转化为一个**感知矩阵 $A \in \mathbb{R}^{n \times dp}$** 上的线性回归问题。在随机高斯数据下，该感知矩阵以高概率满足**受限强凸性（Restricted Strong Convexity）和受限光滑性（Restricted Smoothness）**（Lemma 1），这为后续的稀疏恢复算法提供了理论基础。

基于这一凸松弛，作者证明**迭代硬阈值（IHT）算法**能以高概率精确恢复稀疏MLP的权重（Theorem 1）：在满足Assumption 2的条件下，经过 $K = O(\beta/\alpha \log(f(w^0)/\varepsilon))$ 步迭代，IHT能找到满足 $\|w^K - w^\star\|_2^2 \leq 2\alpha^{-1}\varepsilon$ 的稀疏解。这一保证同时涵盖了稀疏网络权重的**唯一可辨识性**和**高效恢复**，是首个适用于ReLU MLP的稀疏恢复理论结果。

值得注意的是，该理论结果目前仅限于**两层、标量输出的ReLU网络**和**随机高斯数据**，且IHT恢复所需的稀疏度水平 $\tilde{s} \geq 32(\beta/\alpha)^2 s$ 继承了Jain et al. (2014)中可能过于保守的膨胀因子。此外，实验中所用的**顺序凸更新策略**（sequential convex IHT）——即在IHT步骤之间周期性更新感知矩阵A以处理更深层网络——其收敛性目前缺乏理论保证。这些限制构成了后续研究的关键开放问题。

## 核心方法与创新机理

本文的核心创新在于**将稀疏MLP的训练问题重新表述为一个结构化线性感知问题，并首次为其提供了严格的可恢复性理论保证**。这一突破打破了现有稀疏训练方法（如IMP）依赖启发式、缺乏理论支撑的困境，同时实现了内存效率与性能的双赢。

**核心瓶颈**：现有稀疏神经网络训练方法（如迭代剪枝IMP）缺乏理论保证，且必须在优化过程中存储完整的稠密网络，导致内存开销随数据维度d和隐藏层维度m线性增长，难以兼顾资源效率与最终性能。

**因果杠杆**：作者将非凸的稀疏MLP优化问题，通过固定生成器向量和枚举/采样激活模式，转化为一个满足**受限强凸性（RSC）**和**受限光滑性（RSS）**的凸线性感知问题，从而能够利用经典的**迭代硬阈值（IHT）**算法以高概率精确恢复稀疏网络权重。

**核心洞察**：稀疏ReLU MLP的训练等价于一个高度结构化的线性感知问题，其中网络权重是待恢复的稀疏信号，而感知矩阵A由所有可能的激活模式与数据矩阵的乘积构成。通过固定生成器向量 $h_i$ 并枚举所有可能的激活模式 $D_i = \text{diag}(\mathbb{I}\{X h_i \ge 0\})$，非凸问题被凸化为：

$$
\hat{y} = [\mathrm{diag}(\mathbb{I}\{X h_1 \ge 0\}) X \quad \ldots \quad \mathrm{diag}(\mathbb{I}\{X h_p \ge 0\}) X] [w_1; \ldots; w_p]
$$

其中 $w_i = u_i v_i$ 是待恢复的融合权重。在随机高斯数据下，该感知矩阵A以高概率满足RSC/RSS条件（Lemma 1），从而保证IHT算法能以指数级收敛速度精确恢复稀疏权重（Theorem 1）。

**与基线（IMP）的关键差异**：

| 变更维度 | 基线（IMP） | 本文方法（IHT） |
| :--- | :--- | :--- |
| **优化目标** | 非凸的原始MLP损失函数 | 凸松弛后的线性感知问题（MSE损失） |
| **优化算法** | 随机梯度下降（SGD）或Adam | 迭代硬阈值（IHT），一种投影梯度下降方法 |
| **内存使用** | 需存储整个稠密网络，参数随d和m增长 | 仅需存储与稀疏度s成比例的固定参数预算 |
| **激活模式处理** | 隐式通过反向传播学习 | 通过固定生成器向量 $h_i$ 显式枚举或随机采样 |

**证据强度与失效模式**：
- **强证据**：Theorem 1 提供了严格的收敛保证，证明IHT在 $K = O(\beta/\alpha \log(f(w^0)/\varepsilon))$ 步内可达到 $\varepsilon$ 精度，且权重误差 $\|w^K - w^\star\|_2^2 \le 2\alpha^{-1}\varepsilon$。该证明基于Jain et al. (2014)的经典IHT框架，置信度高达0.95。
- **条件依赖**：理论结果依赖于三个关键假设：(1) 数据矩阵X服从i.i.d.标准正态分布；(2) 感知矩阵A的列经过$\ell_2$归一化；(3) 激活模式集合满足Assumption 2（即存在足够多的唯一模式）。若数据非高斯或激活模式不充分，RSC/RSS条件可能不成立，导致理论保证失效。
- **保守性**：理论所需的稀疏度水平 $\tilde{s} \ge 32(\beta/\alpha)^2 s$ 远大于实际需要的s，这一膨胀继承自Jain et al. (2014)的框架，在实际中可能过于保守。

**实验验证**：在planted稀疏MLP恢复、MNIST分类和隐式神经表示等任务上，IHT在保持固定参数预算（内存高效）的同时，在PSNR和分类准确率上均表现出比IMP更稳健的性能（Figure 1-5）。消融实验（Table 1-2）进一步揭示，顺序凸更新A的频率k是控制收敛的关键：当k < 5时，IHT能在100步内以数值精度匹配planted模型；随着k增大，收敛速度显著减慢，PSNR下降。

该论文提出的方法核心是将稀疏MLP的训练问题转化为一个结构化线性感知问题，并利用迭代硬阈值（IHT）算法进行求解。整个pipeline由四个关键模块组成，形成一个从非凸优化到凸松弛、再到稀疏恢复的端到端流程。

**瓶颈与因果机制**：现有稀疏神经网络训练方法（如迭代幅度剪枝IMP）缺乏理论保证，且需要在训练过程中维护一个完整的稠密网络，导致内存效率低下。论文的核心洞察在于：通过固定生成器向量并枚举或随机采样激活模式，可以将非凸的稀疏MLP优化转化为一个满足受限强凸性（Restricted Strong Convexity, RSC）和受限光滑性（Restricted Strong Smoothness, RSS）的线性感知问题。这一转化使得IHT算法能以高概率精确恢复稀疏网络权重。

**pipeline模块与数据流**：

1. **凸松弛模块**：这是整个框架的理论基础。该模块将标准非凸两层ReLU网络 $\hat{y} = \sum_{j=1}^{p} (X u_j)_+ v_j$ 转化为凸形式。具体做法是：用 $p$ 个固定的生成器向量 $h_i \in \mathbb{R}^d$ 替换可学习的隐藏层权重 $u_i$，并将权重融合为 $w_i = u_i v_i$。转化后的模型为：
   $$\hat{y} = [\mathrm{diag}(\mathbb{I}\{X h_1 \geq 0\}) X \quad \ldots \quad \mathrm{diag}(\mathbb{I}\{X h_p \geq 0\}) X] [w_1; \ldots; w_p]$$
   这相当于将非凸的隐藏层-输出层乘积分解为线性感知问题。

2. **激活模式枚举/采样模块**：该模块负责构建感知矩阵 $A$。对于每个生成器向量 $h_i$，计算其对应的激活模式对角矩阵 $D_i = \mathrm{diag}(\mathbb{I}\{X h_i \geq 0\})$，然后与数据矩阵 $X$ 相乘并拼接，形成完整的感知矩阵：
   $$A := [\mathrm{diag}(\mathbb{I}\{X h_1 \geq 0\}) X \quad \ldots \quad \mathrm{diag}(\mathbb{I}\{X h_p \geq 0\}) X] \in \mathbb{R}^{n \times dp}$$
   对于每个隐藏神经元最多 $s'$ 个非零权重的稀疏网络，可能的不同激活模式数量上界为 $p \leq 2 s' \binom{d}{s'} (n/s')^{s'}$。该模块可以通过枚举所有可能的模式，或随机采样足够多的模式来保证覆盖。

3. **迭代硬阈值（IHT）优化模块**：这是核心优化引擎。给定感知矩阵 $A$ 和目标输出 $y$，IHT通过投影梯度下降求解MSE目标 $f(w) = \frac{1}{2} \|A w - y\|_2^2$。其更新规则为：
   $$w^{k+1} = H_{\tilde{s}}( w^k - \eta A^T (A w^k - y) )$$
   其中 $H_{\tilde{s}}$ 是硬阈值算子，将权重投影到 $\tilde{s}$-稀疏集上（$\tilde{s} \geq 32(\beta/\alpha)^2 s$，$\alpha$ 和 $\beta$ 分别是RSC和RSS常数）。该模块的输入是感知矩阵 $A$ 和目标 $y$，输出是稀疏权重向量 $w^K$。

4. **顺序凸更新模块（实验中使用）**：为了处理深层网络（3层及以上），论文在IHT步骤之间周期性地根据当前权重更新感知矩阵 $A$。该模块在凸公式化（公式3）和非凸公式化（公式2）之间切换，每 $k$ 步IHT后重新计算激活模式。实验表明，当 $k < 5$ 时IHT能收敛并以数值精度匹配planted模型；随着 $k$ 增大，收敛速度减慢，PSNR下降。

**数据流**：输入数据 $X \in \mathbb{R}^{n \times d}$ 首先进入凸松弛模块，与固定的生成器向量 $h_i$ 结合生成感知矩阵 $A$。$A$ 和目标输出 $y$ 进入IHT优化模块，经过 $K = O(\beta/\alpha \log(f(w^0)/\varepsilon))$ 步迭代后，输出满足 $f(w^K) - f(w^\star) \leq \varepsilon$ 且 $\|w^K - w^\star\|_2^2 \leq 2\alpha^{-1}\varepsilon$ 的稀疏权重。对于深层网络，顺序凸更新模块在IHT迭代过程中周期性地基于当前权重 $w^k$ 重新计算 $A$，形成反馈循环。

**证据强度**：理论保证依赖于Lemma 1中感知矩阵 $A$ 在随机高斯数据下以高概率满足RSC和RSS条件（概率下界包含多个指数衰减项），以及Theorem 1中IHT的收敛保证（置信度0.95）。实验验证覆盖了planted稀疏MLP拟合、MNIST分类和隐式神经表示等任务，均显示IHT优于或匹敌IMP基线。需要手动验证的是：非高斯数据分布下RSC/RSS条件的成立性，以及顺序凸更新策略的收敛性缺乏理论保证。

本文的核心贡献在于将稀疏MLP的训练问题转化为一个结构化线性感知问题，并利用凸松弛和迭代硬阈值（IHT）算法提供了理论恢复保证。以下梳理关键模块与公式。

### 1. 问题形式化：从非凸MLP到凸线性感知

标准的单隐藏层ReLU网络（非凸形式）为：
$$\hat{y} = \sum_{j=1}^{p} (X u_j)_+ v_j$$
其中 $X \in \mathbb{R}^{n \times d}$ 是数据矩阵，$u_j$ 是隐藏层权重，$v_j$ 是输出层权重。

核心洞察是引入一组**固定的生成器向量** $h_i$ 来替代可学习的 $u_j$，从而将问题凸化。通过“融合”权重 $w_i = u_i v_i$（将隐藏层和输出层权重合并为一个标量），网络输出可以重写为：
$$\hat{y} = [\mathrm{diag}(\mathbb{I}\{X h_1 \geq 0\}) X \quad \ldots \quad \mathrm{diag}(\mathbb{I}\{X h_p \geq 0\}) X] [w_1; \ldots; w_p]$$

这构成了一个标准的线性感知问题 $y \approx A w$，其中感知矩阵 $A \in \mathbb{R}^{n \times dp}$ 定义为：
$$A := [ \mathrm{diag}(\mathbb{I}\{X h_1 \geq 0\}) X \quad \ldots \quad \mathrm{diag}(\mathbb{I}\{X h_p \geq 0\}) X ]$$

**瓶颈与机制**：该凸化的成功依赖于两个关键假设。第一，生成器向量 $h_i$ 的集合必须足够丰富，以覆盖所有可能由稀疏隐藏层权重 $u_j$ 产生的激活模式。对于每个隐藏神经元最多有 $s'$ 个非零权重的情况，不同激活模式数量的上界为：
$$p \leq 2 s' \binom{d}{s'} \left(\frac{n}{s'}\right)^{s'}$$
第二，对于随机高斯数据，该感知矩阵 $A$ 以高概率满足**受限强凸性**和**受限光滑性**条件（Lemma 1），这是IHT算法收敛的理论基石。

### 2. 核心算法：迭代硬阈值（IHT）

为了从线性感知问题 $y = A w^\star + \epsilon$ 中恢复稀疏权重 $w^\star$（满足 $\|w^\star\|_0 \leq s$），论文使用IHT算法。其更新规则为：
$$w^{k+1} = H_{\tilde{s}}( w^k - \eta A^T (A w^k - y) )$$
其中：
- $H_{\tilde{s}}(\cdot)$ 是硬阈值算子，将向量中除最大 $\tilde{s}$ 个元素外的所有元素置零。
- $\tilde{s}$ 是膨胀的稀疏度水平，满足 $\tilde{s} \geq 32(\beta/\alpha)^2 s$，其中 $\alpha, \beta$ 分别是受限强凸性和受限光滑性常数。
- 步长 $\eta = 2/(3\beta)$。

**恢复保证**：Theorem 1 证明，在Assumption 2（激活模式的性质）和随机高斯数据下，经过 $K = O(\beta/\alpha \log(f(w^0)/\varepsilon))$ 次迭代后，IHT算法能以高概率找到稀疏权重 $w^K$，使得：
$$f(w^K) - f(w^\star) \leq \varepsilon \quad \text{且} \quad \|w^K - w^\star\|_2^2 \leq 2\alpha^{-1}\varepsilon$$

**因果机制**：IHT的收敛性直接依赖于矩阵 $A$ 的受限强凸性（$\alpha$）和受限光滑性（$\beta$）。Lemma 1 给出了在随机高斯数据下，$A$ 的任意 $s$ 列子矩阵 $A_S$ 满足 $\alpha I_s \preceq A_S^T A_S \preceq \beta I_s$ 的高概率界。该界确保了梯度下降方向在稀疏子空间上的有效性，而硬阈值投影则维持了权重的稀疏性。

### 3. 实验中的关键模块与变体

为处理更深层网络和实际任务，实验采用了**顺序凸IHT**（Sequential Convex IHT）策略。该策略在IHT步骤之间周期性地根据当前权重 $w^k$ 更新感知矩阵 $A$（即更新生成器向量 $h_i$），从而在凸公式化（公式3）和非凸公式化（公式2）之间切换。

**关键消融实验**（Table 1, Table 2）揭示了更新频率 $k$ 的控制作用：
- 当 $k < 5$（更新频繁），IHT收敛并能以数值精度匹配 planted 模型。
- 随着 $k$ 增大（更新频率降低），模型在100步内不再收敛，PSNR下降，且 $A$ 的收敛速度减慢。
- 当 $k=5$ 时，$A$ 在100步内未收敛，但在135步时收敛，PSNR达到161.44。

**证据强度**：该消融实验直接验证了顺序凸更新频率是控制IHT收敛率的关键旋钮。频繁更新 $A$ 使其更接近当前权重的真实激活模式，从而维持了凸近似的有效性。但该策略的理论收敛性保证尚不完善，是论文指出的开放问题之一。

## 实验与关键发现

**主要结果**：本文通过一系列实验，将所提出的IHT方法与强基线方法——迭代幅度剪枝（IMP）进行了系统比较。实验覆盖了从合成数据到真实图像的多类任务，包括拟合planted稀疏MLP、MNIST手写数字分类以及隐式神经表示（INR）任务。在所有实验中，IHT均展现出与IMP相当或更稳健的性能。

**合成数据实验**：在拟合planted标量输出稀疏MLP的任务中，Figure 1展示了IHT和IMP在不同隐藏维度m和稀疏度s下的平均PSNR。结果显示，IHT在大多数参数配置下都表现出更稳健的性能，尤其是在稀疏度较高（s较小）或隐藏维度较大（m较大）的区域。对于两层网络（一个隐藏层）和三层网络（两个隐藏层），IHT均能稳定地恢复planted模型，而IMP在某些配置下PSNR显著下降。在拟合planted向量输出（10维输出）MLP时，Figure 2显示IHT与IMP性能相当，IHT在部分区域略优。

**MNIST分类实验**：Figure 3比较了两者在MNIST手写数字分类任务上的平均准确率。在二分类（如数字4和9）和10分类任务中，IHT均展现出更稳健的性能。在隐藏维度m较小或稀疏度s较高的困难设置下，IHT的准确率下降幅度小于IMP，表明IHT在参数预算受限时能更有效地利用稀疏结构。

**隐式神经表示（INR）实验**：Figure 4和Figure 5分别展示了在MNIST和CIFAR-10图像上过拟合INR的PSNR。在MNIST上，IHT的PSNR几乎不随隐藏维度m变化，表现出稳定的恢复能力，而IMP的PSNR随m增大而显著下降。在CIFAR-10上，IHT在所有配置下均优于IMP，尤其是在两层网络设置中优势更为明显。

**消融实验**：Table 1和Table 2系统研究了顺序凸更新中A的更新频率k对IHT性能的影响。实验使用一个输入维度100、隐藏维度m=10、稀疏度s=500的标量输出两层MLP，优化100步。关键发现如下：
- 当A更新频率较高（k < 5）时，IHT收敛并能以数值精度匹配planted模型，PSNR达到160以上。
- 随着k增大（如k=5），模型在100步内不再收敛，PSNR急剧下降至36.63。
- 当k=5时，若继续优化至135步，A的支撑集收敛，PSNR回升至161.44，表明A的收敛速度随k增大而减慢。
- 当k=100（即A在整个优化过程中固定），PSNR仅为19.88，说明频繁更新A对恢复性能至关重要。

![[assets/figures/papers/iclr26_0003_6UpstNltZ4_A_Recovery_Guarantee_for_Sparse_Neural_Networks/figures/021_Table_1.jpg]]
*Table 1: Fitting a scalar-output 2-layer MLP with input dimension 100, hidden dimension m = 1 0 . and sparsity level s = 5 0 0 , optimized over 100 steps of IHT with random initialization and sequential convex updates to A every k steps. In our main experiments k = 1 $\cdot$ ; here we observe that fitting quality degrades with increasing k*

![[assets/figures/papers/iclr26_0003_6UpstNltZ4_A_Recovery_Guarantee_for_Sparse_Neural_Networks/figures/022_Table_2.jpg]]
*Table 2: Fitting a scalar-output 2-layer MLP with input dimension 100, hidden dimension m = 1 0 . and sparsity level s = 5 0 0 $\AA$ , optimized over 100 steps of IHT with random initialization and sequential convex updates to A every k steps. In our main experiments k = 1 ; ; here we observe that A converges more slowly with increasing k. We report “convergence step” as the first step of optimization at which the set of active columns of A does not change, signaling support recovery*

**公平性说明**：所有实验在3次随机试验上取平均值，附录Figure 6-10报告了标准差。IHT和IMP使用相同的稀疏度预算s，但IHT在优化过程中保持固定参数预算，而IMP需要先训练稠密网络，其参数数量随数据维度d和隐藏维度m增长。

![[assets/figures/papers/iclr26_0003_6UpstNltZ4_A_Recovery_Guarantee_for_Sparse_Neural_Networks/figures/030_Figure_6.jpg]]
*Figure 6: Standard deviation over the three random trials (top row) for each experiment reported in Figure 1 (bottom row)*

**失败模式分析**：IHT的主要失败模式出现在顺序凸更新频率过低时（k ≥ 5）。此时，固定的激活模式矩阵A无法捕捉网络权重变化带来的新激活模式，导致优化陷入次优解。此外，理论结果仅限于两层标量输出ReLU网络和随机高斯数据，对于更深层网络、向量输出或非高斯数据分布，受限强凸性和受限光滑性条件可能不成立。实验规模也仅限于小规模MLP和图像过拟合任务，在大型数据集或深度网络上的性能尚待验证。

![[assets/figures/papers/iclr26_0003_6UpstNltZ4_A_Recovery_Guarantee_for_Sparse_Neural_Networks/figures/038_Figure_7.jpg]]
*Figure 7: Standard deviation over the three random trials (top row) for each experiment reported in Figure 2 (bottom row)*

![[assets/figures/papers/iclr26_0003_6UpstNltZ4_A_Recovery_Guarantee_for_Sparse_Neural_Networks/figures/047_Figure_8.jpg]]
*Figure 8: Standard deviation over the three random trials (top row) for each experiment reported in Figure 3 (bottom row)*

![[assets/figures/papers/iclr26_0003_6UpstNltZ4_A_Recovery_Guarantee_for_Sparse_Neural_Networks/figures/054_Figure_9.jpg]]
*Figure 9: Standard deviation over the three random trials (top row) for each experiment reported in Figure 4 (bottom row)*

## 定位与知识库关联

### 与基线方法的关系

本文提出的迭代硬阈值（IHT）方法，在理论框架和实际性能上均与迭代幅度剪枝（IMP）形成鲜明对比。IMP作为强基线，其核心瓶颈在于**内存效率与最终性能之间的根本矛盾**：它需要先完整训练一个参数数量随数据维度d和隐藏层维度m增长的稠密网络，再通过剪枝获得稀疏子网络。这导致IMP在优化过程中消耗大量内存，尽管其最终性能可能较好。

IHT则从根本上重构了这一流程。它通过将稀疏MLP优化重新表述为结构化线性感知问题，使得优化过程**直接作用于稀疏权重空间**，参数预算在整个训练过程中固定且仅与稀疏度s成比例。这种设计使得IHT在内存效率上具有天然优势——它无需存储稠密网络的中间状态，从而打破了IMP的“先稠密后稀疏”范式。

实验证据表明，在拟合planted稀疏MLP（标量输出，Figure 1）、MNIST分类（Figure 3）以及隐式神经表示任务（CIFAR-10，Figure 5）中，IHT展现出比IMP**更鲁棒的恢复性能**。具体而言，IHT在不同隐藏维度m和稀疏度s的组合下，其平均PSNR或分类准确率的波动更小，而IMP在某些参数组合下性能急剧下降。对于向量输出MLP（Figure 2），IHT与IMP性能相当（“competitive”），但IHT仍保持了内存效率优势。

### 核心机制与因果链

IHT方法的核心因果链可分解为三个关键环节：

1. **凸松弛**：通过固定生成器向量 $h_i$ 替代可学习的隐藏层权重 $u_i$，将非凸的两层ReLU网络：
   
$$
\hat{y} = \sum_{j=1}^{p} (X u_j)_+ v_j
$$

   转化为凸的线性感知问题：
   
$$
\hat{y} = [\mathrm{diag}(\mathbb{I}\{X h_1 \geq 0\}) X \quad \ldots \quad \mathrm{diag}(\mathbb{I}\{X h_p \geq 0\}) X] [w_1; \ldots; w_p]
$$

   其中 $w_i = u_i v_i$ 为融合权重。这一松弛的代价是：需要枚举或采样所有可能的激活模式 $D_i = \mathrm{diag}(\mathbb{I}\{X h_i \geq 0\})$，其数量上界为 $p \leq 2 s' \binom{d}{s'} (n/s')^{s'}$。

2. **受限强凸性与光滑性**：在随机高斯数据下，感知矩阵A（由激活模式对角矩阵与数据矩阵拼接而成）以高概率满足受限强凸性（RSC）和受限光滑性（RSS）条件（Lemma 1）。这是IHT收敛的理论基石——它保证了在稀疏子空间上，MSE目标函数 $f(w) = \frac{1}{2} \|A w - y\|_2^2$ 具有良好的几何性质。

3. **IHT优化**：利用硬阈值算子 $H_{\tilde{s}}$ 执行投影梯度下降：
   
$$
w^{k+1} = H_{\tilde{s}}( w^k - \eta A^T (A w^k - y) )
$$

   Theorem 1保证，在满足Assumption 2的条件下，经过 $K = O(\beta/\alpha \log(f(w^0)/\varepsilon))$ 步迭代，IHT能以高概率找到稀疏权重 $w^K$，使得 $f(w^K) - f(w^\star) \leq \varepsilon$ 且 $\|w^K - w^\star\|_2^2 \leq 2\alpha^{-1}\varepsilon$。

### 适用边界与证据强度

**适用边界**：
- **网络架构**：理论结果严格限定于两层、标量输出的ReLU MLP。实验虽扩展到三层网络和向量输出，但缺乏相应的理论保证。
- **数据分布**：理论分析假设数据矩阵X的条目服从i.i.d.标准正态分布。对于非高斯数据，RSC/RSS条件可能不成立。
- **稀疏度要求**：IHT恢复需要膨胀的稀疏度水平 $\tilde{s} \geq 32(\beta/\alpha)^2 s$，继承自Jain et al. (2014)。这意味着实际可恢复的稀疏度s远小于IHT投影的稀疏度$\tilde{s}$，在实践中可能过于保守。
- **激活模式覆盖**：需要枚举或采样足够多的生成器向量$h_i$以覆盖所有可能的激活模式。Theorem 1要求“the activation patterns ... are enumerated to include all unique patterns”，这在实践中可能不可行——当输入维度d或稀疏度s较大时，激活模式数量呈指数增长。

**证据强度**：
- **理论证明**：Theorem 1和Lemma 1的证明基于Hanson-Wright不等式和Jain et al. (2014)的IHT收敛定理，数学推导严谨，置信度0.95。但Assumption 2（激活模式性质）的验证在非高斯数据下缺乏保障。
- **实验验证**：所有实验在3次随机试验上取平均值并报告标准差（附录Figure 6-10），使用相同随机种子和超参数以确保公平。但实验规模较小，仅限于小规模MLP（隐藏维度m和稀疏度s均较小）和图像过拟合任务，尚未在大型数据集（如ImageNet）或深度网络上验证。
- **消融研究**：Table 1和Table 2揭示了顺序凸更新频率k对IHT收敛的关键影响。当k < 5时，IHT能在100步内收敛并匹配planted模型；当k增大到5时，100步内不再收敛，但继续优化到135步时仍能收敛（PSNR 161.44）。这表明**A的更新频率是控制IHT收敛率的因果旋钮**，但缺乏理论解释为何k=5时收敛速度骤降。

### 局限与开放问题

**核心局限**：
1. **理论-实践差距**：理论结果仅限于两层标量输出网络和高斯数据，而实验已扩展到更深、向量输出的网络和真实数据。顺序凸更新策略（sequential convex IHT）——在IHT步骤之间周期性地根据当前权重更新感知矩阵A——在实验中表现良好，但缺乏收敛性理论保证。
2. **膨胀稀疏度**：$\tilde{s} > s$的要求使得IHT在实际中需要存储比目标稀疏度更多的参数，削弱了其内存效率优势。如何收紧这一条件是“compelling direction for further study”。
3. **激活模式爆炸**：枚举所有激活模式在理论上可行，但实际中p可能巨大。论文采用随机采样策略，但采样数量与覆盖概率之间的权衡缺乏系统分析。

**开放问题**：
- **扩展性**：如何将恢复保证扩展到更深层、向量输出的网络？如何适应更广泛的架构（如卷积网络）和数据分布（如图像、文本）？
- **收敛率控制**：顺序凸更新频率k如何精确控制IHT的收敛率？是否存在最优的k值或自适应策略？
- **向量输出网络**：对于多输出任务，最优的自适应步长策略是什么？Count Sketch近似误差如何影响不同架构下的IHT性能？
- **非高斯数据**：对于非高斯数据，RSC/RSS条件是否仍然成立？是否需要修改感知矩阵A的构造方式？

这些开放问题共同指向一个核心方向：**如何将稀疏神经网络的可恢复性保证从受限的理论设定推广到更广泛、更实际的深度学习场景**。本文作为“first recovery results for sparse MLPs”，为这一方向奠定了理论基础，但距离实用化的稀疏训练方法仍有显著差距。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Recovery_Guarantee_for_Sparse_Neural_Networks.pdf

![[paperPDFs/ICLR_2026/A_Recovery_Guarantee_for_Sparse_Neural_Networks.pdf]]
