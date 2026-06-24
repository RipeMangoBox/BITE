---
title: "Probabilistic Kernel Function for Fast Angle Testing"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Probabilistic_Kernel_Function_for_Fast_Angle_Testing.pdf
openreview_forum_id: nCsF3Bsn2n
aliases:
- PKFFAT
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/probabilistic_methods
core_operator: "通过引入参考角度（reference angle）并设计确定性投影向量结构（如对称结构或交叉多胞形结构），可以直接控制角度估计的精度，而无需渐近条件。"
primary_logic: "利用参考角度信息，可以建立投影值与真实角度之间确定性的概率关系，不再依赖渐近假设。参考角度越小，核函数越准确，从而优于基于高斯分布的现有方法。"
claims:
- "引理4.2和4.3为K_S^1和K_S^2提供了无渐近假设的确定性概率保证。"
- "HNSW+KS2相比HNSW提升QPS 2.5–3倍，相比HNSW+PEOs提升10–30%。"
- "更小的参考角度带来更准确的核函数，如引理4.2所证明。"
- "所提出的确定性结构（S_sym, S_pol）优于随机高斯投影。"
---

# Probabilistic Kernel Function for Fast Angle Testing

> [!tip] 核心洞察
> 利用参考角度信息，可以建立投影值与真实角度之间确定性的概率关系，不再依赖渐近假设。参考角度越小，核函数越准确，从而优于基于高斯分布的现有方法。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 用于快速角度检测的概率核函数 |
| 英文题名 | Probabilistic Kernel Function for Fast Angle Testing |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=nCsF3Bsn2n); [GitHub](https://github.com/KejingLu-810/KS) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/probabilistic_methods |
| Method | Probabilistic Kernel Functions (K_S^1 and K_S^2) and their implementations KS1 / KS2 |
| Dataset |  |

## 概述

高维向量空间中，角度测试（angle testing）——即判断两个向量夹角是否小于给定阈值，或在两个候选向量中选出与查询向量夹角更小的那个——是最大内积搜索（MIPS）、近似最近邻搜索（ANNS）等任务的基础操作。现有方法普遍采用随机投影策略：**CEOs**（Pham, 2021）利用高斯随机向量与极端次序统计量的渐近分布进行角度比较，**PEOs**（Lu et al., 2024）则通过高斯空间划分实现图索引中的概率路由。这两类方法的共同瓶颈在于依赖渐近假设（投影数趋于无穷），导致有限投影下的概率估计精度不足，理论保证不可靠。

本文提出**概率核函数**（Probabilistic Kernel Functions）$K_S^1$ 和 $K_S^2$，分别对应角度比较（Problem 1.1）与角度阈值判定（Problem 1.2）。核心创新在于引入**参考角度**（reference angle）概念，并采用**确定性投影向量结构**（对称结构 $S_{\text{sym}}$ 或交叉多胞形结构 $S_{\text{pol}}$）替代高斯随机投影。这一设计使得投影值与真实角度之间建立起确定性的概率关系，无需渐近条件即可提供严格的概率保证（引理4.2、4.3）。参考角度越小，核函数越精确，从而在理论上优于基于高斯分布的现有方法。

在近似最近邻搜索实验中，HNSW+KS2 相比原始 HNSW 将每秒查询数（QPS）提升 2.5–3 倍，相比当前最优的 HNSW+PEOs 提升 10%–30%，同时索引体积减少约 5%。在 k-MIPS 召回率测试中，KS1（$S_{\text{pol}}$ 结构）在多数情况下达到最高探测精度。该方法在 NSSG 图结构上同样有效，表明其优势独立于底层图索引的选择。

## 背景与动机

高维向量空间中的角度测试是信息检索、推荐系统和相似性搜索的核心操作。给定查询向量 $\mathbf{q}$ 和数据向量 $\mathbf{v}$，角度测试需要回答两类问题：**角度比较**（$\mathbf{q}$ 与 $\mathbf{v}_1$ 的夹角是否小于 $\mathbf{q}$ 与 $\mathbf{v}_2$ 的夹角）和**角度阈值判定**（$\mathbf{q}$ 与 $\mathbf{v}$ 的夹角是否小于给定阈值）。这两类问题在最大内积搜索（MIPS）和近似最近邻搜索（ANNS）中扮演着关键角色。

### 现有方法的瓶颈：渐近假设与精度不足

当前基于随机投影的角度测试方法，以 **CEOs**（Pham, 2021）为代表，采用高斯分布生成投影向量集 $\{\mathbf{u}_i\}_{i=1}^m$，并利用极端次序统计量建立投影值与真实角度之间的概率关系。其核心依赖引理1.3所示的渐近分布：

$$\mathbf{v}^{\top} \mathbf{u}_{\mathrm{max}} \sim \mathcal{N}\left(\mathrm{sgn}(\mathbf{q}^{\top} \mathbf{u}_{\mathrm{max}}) \cdot \mathbf{q}^{\top} \mathbf{v} \sqrt{2 \ln m},\ 1 - (\mathbf{q}^{\top} \mathbf{v})^2\right)$$

然而，该关系的成立**要求投影向量数量 $m \to \infty$**。在实际应用中，$m$ 受限于计算和存储开销，渐近条件无法满足，导致概率估计精度下降，理论保证不可靠。换言之，现有方法的结构性缺陷在于：**高斯随机投影的精度本质上受制于渐近假设，而这一假设在有限资源下必然被违背**。

### 核心动机：用参考角度替代渐近条件

本文的出发点是打破上述困境：能否建立一种**无需渐近假设**的确定性概率关系？关键洞察在于引入**参考角度**（reference angle）这一概念——投影向量集本身具有一个可计算的结构性角度下界。通过设计确定性的投影向量结构，可以直接控制该参考角度的大小，从而建立投影值与真实角度之间**确定性的概率保证**，不再依赖 $m \to \infty$ 的极限条件。

这一思路将精度控制的因果杠杆从“增加投影数量”转移到“优化投影结构”上：参考角度越小，核函数越准确。这意味着，在相同投影数量下，精心设计的确定性结构可以优于纯随机高斯投影——这正是本文提出概率核函数 $\mathrm{K}_S^1$ 和 $\mathrm{K}_S^2$ 的根本动机。

## 核心创新

本文的核心创新在于**用确定性结构替代高斯随机投影**，从而消除了现有角度测试方法对渐近假设的依赖。具体而言，论文引入了两个关键的概念性改变（changed slots），构成方法层面的根本突破。

### 从高斯随机投影到确定性投影向量集

现有方法（如 **CEOs**, Pham, 2021）采用高斯分布随机生成投影向量，并依赖投影数量趋于无穷时的渐近分布（Lemma 1.3）来建立概率保证。这一策略的根本缺陷在于：有限投影数量下，渐近假设不成立，导致概率估计精度不足，理论保证不可靠。

本文的核心改变是用**确定性结构** $S$ 替代随机高斯矩阵。论文提出了两种具体的确定性配置：

- **$S_{\text{sym}}(m, L)$**（Algorithm 1）：基于对映点对的对称结构，在每层生成 $m/2$ 个独立同分布点及其对映点，利用对映性质将投影计算量减半。
- **$S_{\text{pol}}(m, L)$**（Algorithm 2）：基于多个交叉多胞形的结构，其顶点在 $m = 2d$ 时具有最小的覆盖半径，且可通过快速 Johnson–Lindenstrauss 变换加速投影计算。

这两种结构共享一个关键设计：通过类乘积量化技术将空间划分为 $L$ 个子空间（层级），每层独立配置 $m$ 个投影向量，从而虚拟生成 $m^L$ 个投影向量，在可控复杂度下获得丰富的投影覆盖。

### 从渐近概率关系到确定性概率关系

第二个关键改变是**核函数设计**本身。现有方法（如 CEOs 的 $v^\top u_{\max}$ 统计量）的概率保证依赖渐近条件。本文提出的两个核函数：

$$K_S^1(q, v) = \langle v, Z_{HS}(q) \rangle$$

$$K_S^2(q, v) = \langle Hq, Z_S(Hv) \rangle / A_S(Hv)$$

其核心区别在于引入了**参考角度**（reference angle）$A_S(\cdot)$ 和**参考向量**（reference vector）$Z_S(\cdot)$ 的概念。这使得投影值与真实角度之间建立的是**确定性的概率关系**（Lemma 4.2, 4.3），不再依赖投影数量趋于无穷的假设。因果机制可概括为：

> 参考角度越小 → 核函数的概率估计越精确 → 角度比较/阈值判断越可靠。

这一关系由 Lemma 4.2 和 4.3 严格保证，且无需渐近条件。实验证据支持这一因果链：$S_{\text{pol}}$ 通常比 $S_{\text{sym}}$ 产生更小的参考角度（Table 1），并相应获得更高的召回率；而高斯随机投影由于参考角度更大，表现更差，验证了“高斯分布是次优的”这一论断。

### 在相似图路由中的应用创新

基于 $K_S^2$，论文提出了 **KS2 测试**——一种新的 $(\delta, 0.5)$-路由测试，用于相似图上的近似最近邻搜索。相比 **PEOs**（Lu et al., 2024）的测试不等式，KS2 测试在形式上更简洁，所需存储的常量更少，且因确定性结构带来的更小参考角度而获得了更高的路由效率。这一改进直接转化为 HNSW+KS2 相比 HNSW+PEOs 10%–30% 的 QPS 提升，以及相比原始 HNSW 2.5–3 倍的加速。

## 整体框架

本文提出了一套基于**参考角度（reference angle）**的概率核函数框架，用于替代传统基于高斯随机投影和渐近假设的角度测试方法。整个框架围绕两个核心问题展开：角度比较（Problem 1.1）与角度阈值判定（Problem 1.2），并为此设计了两个概率核函数 $K_S^1$ 和 $K_S^2$。

### 核心模块与数据流

框架的运作流程可分解为以下三个关键模块：

1.  **投影向量集 $S$ 的确定性构造**
    输入为维度 $d$、层级数 $L$ 和每层向量数 $m$。模块输出一个精心设计的确定性投影向量集 $S$，而非传统方法中的高斯随机矩阵。本文提出了两种互补的构造算法：
    *   **$S_{\text{sym}}(m, L)$**（Algorithm 1）：基于对映点对（antipodal pairs）的对称结构，在每层独立采样 $m/2$ 个点及其对映点。
    *   **$S_{\text{pol}}(m, L)$**（Algorithm 2）：基于交叉多胞形（cross-polytopes）的结构，利用 $2d$ 个顶点作为投影向量，$S_{\text{pol}}$ 通常能产生略小的参考角度，且投影计算更高效。

    这两种结构是框架性能优于随机投影的**因果开关**：它们直接控制了参考角度的大小，而参考角度是决定核函数精度的关键因素。

2.  **参考向量与参考角度的提取**
    对于任意输入向量 $\boldsymbol{v}$，模块从投影集 $S$ 中提取两个关键信息：
    *   **参考向量 $Z_S(\boldsymbol{v})$**：$S$ 中与 $\boldsymbol{v}$ 内积最大的向量，即 $Z_S(\boldsymbol{v}) = \arg\max_{\boldsymbol{u} \in S} \langle \boldsymbol{u}, \boldsymbol{v} \rangle$。
    *   **参考角度 $A_S(\boldsymbol{v})$**：$\boldsymbol{v}$ 与 $Z_S(\boldsymbol{v})$ 之间夹角的余弦值，即 $A_S(\boldsymbol{v}) = \langle \boldsymbol{v}, Z_S(\boldsymbol{v}) \rangle$。

    此处的核心洞察是：参考角度 $A_S(\cdot)$ 包含了估计精度的全部信息。引理 4.2 和 4.3 严格证明了，参考角度越小（即 $A_S(\cdot)$ 越大），核函数的概率保证越强。

3.  **概率核函数的计算与应用**
    这是框架的输出层，利用前两个模块的结果计算核函数值，并将其集成到下游任务中。
    *   **$K_S^1(\boldsymbol{q}, \boldsymbol{v})$**：定义为 $\langle \boldsymbol{v}, Z_{HS}(\boldsymbol{q}) \rangle$，其中 $H$ 是一个随机旋转矩阵。它直接输出一个标量，用于比较 $\boldsymbol{q}$ 与不同 $\boldsymbol{v}$ 之间的角度大小，其概率保证由引理 4.2 给出。
    *   **$K_S^2(\boldsymbol{q}, \boldsymbol{v})$**：定义为 $\langle H\boldsymbol{q}, Z_S(H\boldsymbol{v}) \rangle / A_S(H\boldsymbol{v})$。它用于判断 $\angle(\boldsymbol{q}, \boldsymbol{v})$ 是否小于某个阈值，其概率保证由引理 4.3 给出。

    这两个核函数是框架的直接输出。它们不依赖于“投影数量趋于无穷”的渐近假设，而是建立了投影值与真实角度之间**确定性的概率关系**。

### 端到端集成示例：ANNS 与 k-MIPS

框架的实用性体现在它能即插即用地替换现有系统中的投影组件。

*   **在 k-MIPS（最大内积搜索）中**：KS1 方法直接将传统（如 CEOs，Pham, 2021）的高斯随机投影矩阵替换为 $S_{\text{sym}}$ 或 $S_{\text{pol}}$，其余流程保持不变。实验表明，这种替换带来了轻微但一致的召回率提升，验证了确定性结构优于高斯分布的论断。
*   **在 ANNS（近似最近邻搜索）中**：KS2 方法基于 $K_S^2$ 设计了一个新的概率路由测试（KS2 test），用于在图搜索（如 HNSW, Malkov & Yashunin, 2020）中提前剪枝。其测试不等式比当前最优的 PEOs 测试（Lu et al., 2024）更简洁，需要存储的常量更少。集成 KS2 后，HNSW 的查询吞吐量（QPS）提升了 2.5–3 倍，索引大小减少了约 5%。

整个框架的输入是向量化的查询和数据点，输出是角度关系的概率性估计或路由决策，其核心优势在于用可控的、确定性的参考角度机制，取代了传统方法中不可靠的渐近高斯假设。

## 核心模块与公式推导

### 概率核函数设计

本文针对角度比较（Problem 1.1）和角度阈值判断（Problem 1.2）两类任务，分别提出两个概率核函数 $K_S^1$ 和 $K_S^2$。这两个核函数的核心设计思想是：利用**参考角度**（reference angle）信息，建立投影值与真实角度之间确定性的概率关系，从而摆脱现有方法（如CEOs）对渐近假设的依赖。

#### $K_S^1$：面向角度比较

$K_S^1$ 的定义为查询向量 $\boldsymbol{q}$ 与候选向量 $\boldsymbol{v}$ 在旋转投影集 $HS$ 下的内积：

$$K_S^1(\boldsymbol{q}, \boldsymbol{v}) = \langle \boldsymbol{v}, Z_{HS}(\boldsymbol{q}) \rangle, \quad \boldsymbol{v}, \boldsymbol{q} \in \mathbb{S}^{d-1}$$

其中 $Z_{HS}(\boldsymbol{q})$ 表示在旋转后的投影向量集 $HS$ 中与 $\boldsymbol{q}$ 内积最大的向量（即参考向量）。该核函数直接以投影值作为角度比较的代理，其概率保证由引理4.2给出：在给定参考角度 $\psi$（满足 $A_S(\boldsymbol{q}) = \cos\psi$）的条件下，$K_S^1(\boldsymbol{q}, \boldsymbol{v})$ 的条件累积分布函数为

$$F_{K_S^1(\boldsymbol{q}, \boldsymbol{v})}(x \mid A_S(\boldsymbol{q}) = \cos\psi) = I_t\left(\frac{d-2}{2}, \frac{d-2}{2}\right)$$

其中 $I_t(\cdot,\cdot)$ 为正规化不完全Beta函数，参数 $t$ 由真实角度 $\phi$ 和参考角度 $\psi$ 共同决定：

$$t = \frac{1}{2} + \frac{x - \cos\phi \cos\psi}{2 \sin\phi \sin\psi}$$

这一分布不依赖任何渐近条件，而是由参考角度 $\psi$ 精确控制估计精度——参考角度越小，核函数越准确。

#### $K_S^2$：面向角度阈值判断

$K_S^2$ 的定义为：

$$K_S^2(\boldsymbol{q}, \boldsymbol{v}) = \frac{\langle H\boldsymbol{q}, Z_S(H\boldsymbol{v}) \rangle}{A_S(H\boldsymbol{v})}, \quad \boldsymbol{v}, \boldsymbol{q} \in \mathbb{S}^{d-1}$$

其中 $H$ 为随机旋转矩阵，$A_S(H\boldsymbol{v})$ 是 $H\boldsymbol{v}$ 在投影集 $S$ 上的参考角度余弦值。分子是 $H\boldsymbol{q}$ 与 $H\boldsymbol{v}$ 的参考向量的内积，除以 $A_S(H\boldsymbol{v})$ 进行归一化。引理4.3给出了 $K_S^2$ 的概率保证：其假阳性概率 $\epsilon_2$ 上界为

$$\epsilon_2 = I_{t'}\left(\frac{d-2}{2}, \frac{d-2}{2}\right) < 0.5$$

该上界同样由参考角度直接控制，无需渐近条件。

#### 核函数的通用化

为支持内积空间（如MIPS任务），$K_S^1$ 被推广为 $K_S^{1'}$：

$$K_S^{1'}(\boldsymbol{q}, \boldsymbol{v}) = \lVert \boldsymbol{v} \rVert \cdot \langle \boldsymbol{v}, Z_{HS}(\boldsymbol{q}) \rangle$$

即用 $\boldsymbol{v}$ 的范数对投影值进行缩放，使核函数适用于非单位球面向量。

### 投影向量集 $S$ 的确定性构造

核函数的精度取决于投影向量集 $S$ 的结构。本文提出两种确定性构造方案，替代CEOs中的高斯随机投影：

- **对称结构 $S_{\text{sym}}(m, L)$**（算法1）：在 $L$ 个低维子空间上分别独立采样 $m/2$ 个对映点对（antipodal pairs），拼接后得到 $m^L$ 个投影向量。对映结构使投影计算量减半，同时保证 $A_S(\boldsymbol{v}) > 0$。

- **交叉多胞形结构 $S_{\text{pol}}(m, L)$**（算法2）：在每个子空间使用 $m$ 个交叉多胞形（cross-polytope）的顶点作为投影向量。当 $m=2d$ 时，交叉多胞形顶点具有最小的覆盖半径（covering radius），因此能产生更小的参考角度，经验上优于对称结构。

两种结构均采用类似乘积量化（product quantization）的方式，将原始 $d$ 维空间划分为 $L$ 个低维子空间，通过拼接子向量实现投影向量的指数级扩展。参考角度（以余弦值 $J(S) = \mathbb{E}_{\boldsymbol{v}}[A_S(\boldsymbol{v})]$ 衡量）是衡量结构优劣的核心指标：$J(S)$ 越大（即参考角度越小），核函数精度越高。实验验证 $J(S_{\text{pol}})$ 通常略大于 $J(S_{\text{sym}})$。

### 计算复杂度

引理5.1给出了两个核函数在索引和查询阶段的复杂度：

- **索引阶段**：对大小为 $n$ 的数据集，$K_S^1$ 的复杂度为 $O(nmd)$，$K_S^2$ 为 $O(nd\log d + nmd)$（额外包含随机旋转的 $O(nd\log d)$ 开销）。
- **查询阶段**：$K_S^1$ 需要 $O(md)$ 时间完成投影计算，$K_S^2$ 同样为 $O(md)$。

当使用交叉多胞形结构且 $R=1$ 时，可借助快速Johnson-Lindenstrauss变换进一步加速投影计算。

## 实验与分析

### 核心实验结论

#### 角度测试精度：KS1 vs. CEOs

KS1在两个确定性投影结构（S_sym与S_pol）上的k-MIPS召回率均优于基于高斯随机投影的**CEOs**（Pham, 2021），验证了更小参考角度带来更准确估计的理论主张。在Word数据集上，KS1(S_sym)的Recall@10为34.167%，CEOs为34.106%；在GloVe1M上，KS1(S_sym)为1.792%，CEOs为1.773%（Table 1，2048个投影向量，top-5探测）。S_pol结构的召回率普遍高于S_sym，证实越接近最优覆盖的配置性能越好。这一结果直接支撑了论文的核心主张：高斯分布对于投影向量的生成是次优的。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_nCsF3Bsn2n/figures/001_Table_1.jpg]]
*Table 1: Comparison of recall rates (%) for k-MIPS, k = 10. The number of projection vectors is 2048. Top-5 projection vectors are probed. Probe@n means top-n points were probed on each probed projection vector. Results are averaged over 10 runs to reduce the bias introduced by random projection*

#### ANNS加速：HNSW+KS2 vs. HNSW/PEOs

在近似最近邻搜索（ANNS）任务中，HNSW+KS2在Recall-QPS曲线上显著优于基线。相比原始**HNSW**（Malkov & Yashunin, 2020），QPS提升2.5–3倍；相比当前最好的概率路由方法**HNSW+PEOs**（Lu et al., 2024），QPS提升10%–30%（Figure 1）。同时，HNSW+KS2的索引大小额外开销比HNSW+PEOs减少约5%。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_nCsF3Bsn2n/figures/002_Figure_1.jpg]]
*Figure 1: Recall-QPS evaluation of ANNS. k = 10*

#### 与量化方法的对比

在Word数据集的高召回区域，**ScaNN**的性能优于HNSW+KS2。论文将此归因于HNSW的图连通性问题，而非KS2测试本身的瓶颈——这意味着KS2的增益受限于底层图索引的质量。

### 关键消融与参数分析

#### 投影结构选择（S_sym vs. S_pol）

S_pol（多交叉多胞形结构）在参考角度指标J(S)上通常略大于S_sym（对称对映结构），这解释了S_pol在k-MIPS召回率上的优势。具体而言，S_pol利用交叉多胞形顶点在m=2d时具有最小覆盖半径的性质，在投影计算效率上也更优（可通过快速Johnson-Lindenstrauss变换加速）。

#### 层级数L的影响

L控制着通过类乘积量化技术虚拟生成的投影向量总数（m^L）。Figure 8展示了L对索引大小和搜索性能的影响：增加L可以提升搜索精度，但会增大索引开销。在HNSW+PEOs与HNSW+KS2的对比中，KS2在同等索引开销下始终获得更高QPS，且索引额外开销更小。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_nCsF3Bsn2n/figures/013_Figure_8.jpg]]
*Figure 8: Impact of L on index sizes and search performance. k = 10*

#### 探测投影向量数的影响

Tables 4和5分别展示了top-2和top-10投影向量探测设置下的k-MIPS召回率。KS1在不同探测数量下均保持对CEOs的微弱但一致的精度优势（最高约0.8%），表明确定性投影结构的优势不依赖于特定的探测参数选择。

### 失败模式与局限性

1. **高召回区域的图连通性瓶颈**：在Word数据集上，当召回率要求极高时，HNSW本身的图连通性问题限制了KS2的性能上限，使得ScaNN等量化方法反超。这说明KS2作为路由测试，无法弥补底层图索引的结构缺陷。

2. **最优投影配置的开放性**：论文指出，最优投影向量集S_m^*仅在m ≤ d+3时有已知解，一般情况下的最优配置仍是开放问题。当前S_sym和S_pol虽优于高斯随机投影，但并非理论最优。

3. **理论保证的适用范围**：引理4.2和4.3的概率保证要求A_S(v) > 0，即参考角度余弦为正。S_sym和S_pol结构通过设计确保了这一条件成立，但对于其他可能的投影结构，该前提需要额外验证。

4. **维度与投影数量的权衡**：当维度d较大时，为获得足够小的参考角度，需要增加投影向量数m或层级数L，这会线性增加存储和计算开销。论文未给出在固定预算下m与L的最优分配策略。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_nCsF3Bsn2n/figures/005_Figure_3.jpg]]
*Figure 3: An illustration of the KS2 test*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_nCsF3Bsn2n/figures/006_Figure_4.jpg]]
*Figure 4: An illustration of Falconn, CEOs, and the proposed structure KS1*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_nCsF3Bsn2n/figures/010_Figure_5.jpg]]
*Figure 5: Numerical computation under different m’s and d’s. The y-axis denotes the cosine of reference angle*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_nCsF3Bsn2n/figures/011_Figure_6.jpg]]
*Figure 6: Recall-QPS evaluation of ANNS. k = 100*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_nCsF3Bsn2n/figures/012_Figure_7.jpg]]
*Figure 7: Recall-QPS evaluation of ANNS. k = 1*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_nCsF3Bsn2n/figures/014_Figure_9.jpg]]
*Figure 9: Recall-QPS evaluation of ANNS, with NSSG+KS2. k = 10*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_nCsF3Bsn2n/figures/003_Figure_2.jpg]]
*Figure 2: Impact of L (See Appendix D.4 for other datasets). k = 10. The y-axis of the upper figures denotes the additional index cost (%) of HNSW+PEOs compared to the original HNSW. ACKNOWLEDGEMENTS*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_nCsF3Bsn2n/figures/004_Table_2.jpg]]
*Table 2: Frequently used notations*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_nCsF3Bsn2n/figures/007_Table_3.jpg]]
*Table 3: Dataset statistics*

## 方法谱系与知识库定位

### 问题背景与现有方法的瓶颈

在高维向量检索中，快速判断两个向量之间的角度关系（角度比较与角度阈值测试）是许多近似最近邻搜索（ANNS）和最大内积搜索（MIPS）算法的核心子问题。本文聚焦于基于随机投影的角度测试方法，其核心瓶颈在于：现有方法普遍采用高斯分布生成投影向量，并依赖渐近假设（投影数量趋于无穷）来建立概率估计。这一范式存在两个根本缺陷：

1. **概率估计精度不足**：以 **CEOs**（Pham, 2021）为代表的方法利用极端次序统计量（extreme order statistics）的渐近分布进行角度比较，但实际应用中投影数量有限，渐近条件不成立，导致理论保证在实际场景中不可靠。
2. **投影向量结构未优化**：高斯随机向量并非为角度估计精度而设计，其覆盖球面的效率低于确定性结构。

类似地，**PEOs**（Lu et al., 2024）将高斯空间划分用于相似图概率路由测试，但其测试统计量同样缺乏归一化，且未显式利用参考角度信息来控制估计精度。更早的 **Falconn**（Andoni et al., 2015）基于局部敏感哈希（LSH）进行角度估计，但其精度受限于哈希函数的随机性。

### 本文的方法定位与核心创新

本文提出的概率核函数 **KS1** 和 **KS2** 在方法谱系中占据了一个独特位置：它保留了随机投影的计算高效性，但通过引入**参考角度**（reference angle）并采用**确定性投影向量结构**，从根本上摆脱了对渐近假设的依赖。

核心创新可概括为三个层次：

**层次一：参考角度驱动的概率关系重建。** 现有方法（如 CEOs）的核函数形式为 $\boldsymbol{v}^\top \boldsymbol{u}_{\max}$，其分布仅在 $m \to \infty$ 时退化为已知形式。本文重新定义了核函数 $K_S^1$ 和 $K_S^2$，使其显式依赖于参考向量 $Z_S(\cdot)$ 和参考角度 $A_S(\cdot)$。这一设计使得投影值与真实角度之间的关系成为**确定性概率关系**——引理 4.2 和 4.3 分别给出了 $K_S^1$ 和 $K_S^2$ 的条件累积分布函数，无需任何渐近条件。具体而言，$K_S^1$ 的条件 CDF 由正则化不完全 Beta 函数 $I_t(\frac{d-2}{2}, \frac{d-2}{2})$ 给出，其中参数 $t = \frac{1}{2} + \frac{x - \cos\phi \cos\psi}{2 \sin\phi \sin\psi}$，$\psi$ 为参考角度。这一公式直接揭示了参考角度 $\psi$ 对估计精度的控制机制：$\psi$ 越小，分布越集中，核函数越准确。

**层次二：确定性投影结构的优化。** 本文提出两种投影向量集配置算法：$S_{\text{sym}}(m, L)$（算法 1，基于对映点对）和 $S_{\text{pol}}(m, L)$（算法 2，基于交叉多胞形）。这两种结构均优于纯随机高斯投影，原因有三：(1) 对映点对使投影计算量减半；(2) 两者均保证 $A_S(\boldsymbol{v}) > 0$，满足核函数的理论前提；(3) 当 $m = 2d$ 时，交叉多胞形的 $2d$ 个顶点具有最小覆盖半径。实验表明 $S_{\text{pol}}$ 通常获得比 $S_{\text{sym}}$ 稍大的参考角度余弦值 $J(S)$，验证了更接近最优覆盖的配置能带来更好的性能。

**层次三：乘积量化式空间划分。** 为在实际维度下生成足够多的投影向量，本文采用类似乘积量化（Jégou et al., 2011）的技术，将原始空间划分为 $L$ 个子空间，每层独立配置投影向量，从而虚拟生成 $m^L$ 个投影向量。这一技巧在保持计算可行性的同时，显著提升了投影的覆盖能力。

### 与基线方法的关系

**KS1 与 CEOs 的关系**：KS1 是 CEOs 的直接改进。在 CEOs 中，随机高斯矩阵可被 $S_{\text{sym}}$ 或 $S_{\text{pol}}$ 直接替换，其余部分保持不变。实验表明，KS1 在 k-MIPS 任务上相比 CEOs 提供最高 0.8% 的召回率提升（如 Word 数据集上 Recall@10 从 34.106% 提升至 34.167%），这一微小但一致的提升验证了“更小参考角度带来更准确估计”的理论主张。

**KS2 与 PEOs 的关系**：KS2 测试是 PEOs 测试的简化与改进。KS2 的测试不等式 $\sum_{i=1}^{L} \boldsymbol{q}_i^\top \boldsymbol{u}_{e[i]}^i \geq A_S(\boldsymbol{e}) \cdot \frac{\|\boldsymbol{w}\|^2/2 - \tau - \boldsymbol{v}^\top \boldsymbol{q}}{\|\boldsymbol{e}\|}$ 比 PEOs 的测试不等式更简洁，且需要存储的常数更少。在 ANNS 任务中，HNSW+KS2 相比 HNSW+PEOs 提升 QPS 10%–30%，同时减少约 5% 的索引大小。

**与图基 ANNS 基线的集成**：KS2 作为概率路由测试，可集成到 HNSW（Malkov & Yashunin, 2020）等图基 ANNS 方法中。HNSW+KS2 相比原始 HNSW 提升 QPS 2.5–3 倍，在高召回区域可与量化型方法 ScaNN 竞争，尽管在部分数据集上因 HNSW 的连通性问题而略逊。

### 适用边界与局限

1. **参考角度与精度的权衡**：理论保证依赖于参考角度 $\psi$ 的大小，$\psi$ 越小核函数越准确，但过小的 $\psi$ 要求更多的投影向量或更复杂的结构，增加索引构建和查询的计算开销。实际应用中需在精度与效率之间权衡。
2. **最优配置的开放性**：最优投影向量集 $S_m^*$（最大化最坏情况覆盖）仅在 $m \leq d+3$ 时已知，一般情况下的最优配置仍是开放问题。当前使用的 $S_{\text{sym}}$ 和 $S_{\text{pol}}$ 是启发式近似，并非理论最优。
3. **高维退化效应**：尽管乘积量化式空间划分缓解了维度灾难，但在极高维度下，参考角度的余弦值 $J(S)$ 可能趋近于零，核函数的区分能力随之下降。这一效应的定量分析在文中未充分展开。
4. **与量化方法的竞争**：在部分数据集的高召回区域，ScaNN 等量化型方法仍优于 HNSW+KS2，表明概率路由测试在图连通性较差的场景下存在固有局限。

### 开放问题

- 对于一般 $m$ 和 $d$，如何构造或近似最优投影向量集 $S_m^*$？
- 参考角度与核函数精度之间的定量关系能否进一步紧致化，以指导实际参数选择？
- 概率核函数框架能否推广到非欧几里得空间（如双曲空间）或非内积相似度（如编辑距离）？

## 原文 PDF

![[paperPDFs/ICLR_2026/Probabilistic_Kernel_Function_for_Fast_Angle_Testing.pdf]]
