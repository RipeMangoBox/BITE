---
title: "Independence Test for Linear Non-Gaussian Data and Applications in Causal Discovery"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Independence_Test_for_Linear_Non_Gaussian_Data_and_Applications_in_Causal_Discovery.pdf
project_link: null
code_link: null
openreview_forum_id: Uc1EAICxTD
aliases:
- LLNGIC
- ITLNGDACD
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/causality
core_operator: "独立性检验的灵敏度可通过约束检验条件——仅检查条件期望和条件方差的恒定性来提升，而无需捕捉全部高阶依赖。"
primary_logic: "在线性非高斯混合模型中，X 与 Y 独立当且仅当条件期望 E(Y|X) 为常数且条件方差 Var(Y|X) 为常数；这一等价性使检验问题降维为一阶和二阶矩的恒定检验。"
claims:
- "独立性等价于条件期望与条件方差的恒定性"
- "通过检验 Cov(f(X),Y)=0 和 Cov(f(X),Y²)=0 可同时验证这两个条件"
- "所提 LiNGIC 统计量在零假设下收敛到加权 χ² 分布，能有效控制 I 型错误"
- "线性非高斯合成数据 (d=3, Laplace, n=500) 上 Test Power = 0.80 (LiNGIC)"
---

# Independence Test for Linear Non-Gaussian Data and Applications in Causal Discovery

> [!tip] 核心洞察
> 在线性非高斯混合模型中，X 与 Y 独立当且仅当条件期望 E(Y|X) 为常数且条件方差 Var(Y|X) 为常数；这一等价性使检验问题降维为一阶和二阶矩的恒定检验。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 线性非高斯数据的独立性检验及其在因果发现中的应用 |
| 英文题名 | Independence Test for Linear Non-Gaussian Data and Applications in Causal Discovery |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Uc1EAICxTD) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/causality |
| Method | LiNGIC (Linear Non-Gaussian Independence Criterion) |
| Dataset | 线性非高斯合成数据 (d=3, Laplace, n=500), Student-t, Downstream Direct-LiNGAM on synthetic Sachs data (10 nodes, Uniform noise), Varying dependence strength c (d=3 |

> [!tip] 效果简介
> - 线性非高斯合成数据 (d=3, Laplace, n=500) 上，Test Power 为 0.80 (LiNGIC)，对比 0.77 (HSIC), 0.61 (SCIT)，变化 +0.03 (vs HSIC); +0.19 (vs SCIT)。
> - 线性非高斯合成数据 (d=3, Student-t, n=500) 上，Test Power 为 0.97 (LiNGIC)，对比 0.85 (HSIC), 0.69 (SCIT)，变化 +0.12 (vs HSIC)。
> - Downstream Direct-LiNGAM on synthetic Sachs data (10 nodes, Uniform noise) 上，F1 score (higher) & SHD (lower) 为 F1=0.98, SHD=0.8，对比 F1=0.97 (dCor), SHD=1.0 (dCor); F1=0.93 (HSIC-RFF), SHD=1.2，变化 F1:+0.01 vs dCor; SHD:-0.2 vs dCor。

## 概要

独立性检验是统计推断与因果发现中的核心模块。通用非参数检验（如 HSIC、dCor）虽能捕捉任意形式的依赖，但在**线性非高斯混合模型**这一常见场景下，其有限样本功效常显不足——它们未利用数据生成结构，导致对微弱依赖的区分能力受限。

本文的核心洞察是：在线性非高斯数据中，独立性等价于一阶和二阶条件矩的恒定性。具体而言，若 $X$ 和 $Y$ 均为独立非高斯噪声的线性混合，则 $Y \perp\!\!\!\perp X$ 当且仅当 $\mathbb{E}(Y|X)$ 为常数且 $\mathrm{Var}(Y|X)$ 为常数（Theorem 4.2）。这一等价性将原本需要捕捉全部高阶依赖的检验问题，**降维**为检验条件期望和条件方差的恒定性。

基于此，作者提出 **LiNGIC（Linear Non-Gaussian Independence Criterion）**——一种针对线性非高斯数据的核独立性检验方法。其关键设计在于：对 $X$ 侧使用通用核以保持灵活性，对 $Y$ 侧使用二阶多项式核以仅捕获均值和方差信息，并通过对称化构造保证数值稳定性。LiNGIC 的统计量在零假设下收敛于加权 $\chi^2$ 分布，可有效控制 I 型错误；对立假设下则渐近正态，具备统计功效的理论保证。

实验表明，LiNGIC 在合成线性非高斯数据上的检验功效系统性地优于 HSIC、dCor 等通用方法——尤其在重尾分布（如 Student-t）和弱依赖条件下优势显著。在下游因果发现任务（Direct-LiNGAM）中，LiNGIC 在多个噪声类型上取得了最低的 SHD。但需注意，该优势**严格依赖**线性非高斯假设；在真实 Sachs 数据上，其 F1 分数未超越 dCor，提示模型假设与实际数据的契合度仍需审慎评估。



独立性检验是统计推断与因果发现中的核心工具。给定两个随机变量 $X$ 和 $Y$，检验 $X \perp\!\!\!\perp Y$ 是否成立。通用的非参数独立性检验方法——如 Hilbert-Schmidt 独立性准则（HSIC）、距离相关（dCor）——通过核函数或距离度量捕捉 $X$ 与 $Y$ 之间的任意形式依赖。HSIC 的定义为交叉协方差算子的 Hilbert-Schmidt 范数：

$$\| \Sigma_{XY} \|_{\mathcal{HS}}^2 = \| \mathbb{E}_{\mathbb{P}_{XY}} [ (\psi_X - \mu_X) \otimes (\phi_Y - \mu_Y) ] \|_{\mathcal{HS}}^2$$

这类方法在理论上具有一致性，能够检测任意形式的统计依赖。然而，在有限样本下，这种“通用性”反而成为瓶颈：检验需要捕捉所有可能的高阶依赖模式，导致统计功效不足，尤其在依赖强度较弱时难以可靠区分 $H_0$（独立）与 $H_1$（依赖）。

**瓶颈的本质**：现有通用检验未利用数据生成过程的结构信息。当数据来自线性非高斯模型（即 $X$ 和 $Y$ 均为独立非高斯成分的线性混合）时，独立性具有更简洁的等价刻画——仅需检查条件期望和条件方差的恒定性，而无需捕捉全部高阶依赖。通用检验对此结构“视而不见”，将统计功效浪费在对无关高阶矩的估计上。

**动机**：Figure 1 直观展示了这一洞察。在一般分布中，即使 $\mathbb{E}(Y|X)$ 和 $\text{Var}(Y|X)$ 被控制为常数，$X$ 与 $Y$ 之间仍可能存在复杂的非线性依赖。但在线性非高斯混合模型中，这种情形不可能发生：若条件均值和条件方差均为常数，则 $X$ 与 $Y$ 必然独立。这意味着，对于线性非高斯数据，独立性检验可以降维为对一阶矩和二阶矩恒定性的检验，从而在有限样本下获得更高的统计功效。

本文正是基于这一观察，提出了一种专门针对线性非高斯数据的独立性检验框架，将检验条件从“捕捉任意依赖”收缩为“验证条件期望和条件方差恒定”，在保持 I 型错误控制的同时显著提升检验功效。



## 核心方法与创新机理

### 瓶颈：通用检验在线性非高斯结构下的功效不足

现有通用非参数独立性检验（如 HSIC、dCor）通过特征核捕捉任意形式的统计依赖，在有限样本下未能利用线性非高斯混合模型的结构特性。其根本困境在于：为覆盖所有可能的依赖形式，这类检验必须在高维特征空间中进行，导致统计功效被稀释——当依赖强度较弱或样本量有限时，难以可靠区分微弱依赖与独立。论文的核心突破在于识别并利用了一个关键等价性：**在线性非高斯混合模型中，独立性检验可降维为仅检查条件期望和条件方差的恒定性**，而无需捕捉全部高阶依赖。

### 理论创新：独立性等价于一阶和二阶矩的恒定

论文建立了线性非高斯设定下的核心理论桥梁。**Theorem 4.2** 证明：设 $\varepsilon_1, \ldots, \varepsilon_m$ 为独立的非高斯随机变量，$X$ 与 $Y$ 为这些变量的线性混合，则 $Y \perp\!\!\!\perp X$ 当且仅当存在常数 $c$ 和 $\sigma_0^2$ 使得：

$$\mathbb{E}(Y \mid X) = c \quad \text{且} \quad \operatorname{Var}(Y \mid X) = \sigma_0^2$$

这一等价性将独立性检验问题从“检测任意形式的依赖”压缩为“验证两个条件矩的恒定性”，为构造更高效的检验统计量提供了理论依据。**Theorem 4.3** 进一步将此条件转化为可操作的协方差形式：$X \perp\!\!\!\perp Y$ 当且仅当对任意有界连续函数 $f$，同时满足 $\operatorname{Cov}(f(X), Y) = 0$ 和 $\operatorname{Cov}(f(X), Y^2) = 0$。

关键的是，**仅检验其中一个条件是不充分的**。Figure 2 给出了反例：当 $\mathbb{E}(Y \mid X)$ 为常数但 $\operatorname{Var}(Y \mid X)$ 随 $X$ 变化时，$X$ 与 $Y$ 并不独立。这说明必须同时约束两个条件矩。

### 方法创新：LiNGIC 的检验准则与核函数设计

基于上述理论，论文提出 **LiNGIC**（Linear Non-Gaussian Independence Criterion），其核心设计体现在以下三个 changed slots：

**1. 检验准则：从捕捉任意依赖到仅检测协方差结构**

- **Baseline（HSIC）**：利用通用核捕捉 $X$ 与 $Y$ 之间任意形式的依赖，检验准则为 $\| \Sigma_{XY} \|_{\mathcal{HS}}^2 = \| \mathbb{E}[(\psi_X - \mu_X) \otimes (\phi_Y - \mu_Y)] \|_{\mathcal{HS}}^2$。
- **LiNGIC**：仅检测 $X$ 与 $Y$（及 $Y^2$）之间的协方差是否为零，等效于验证 $\mathbb{E}(Y \mid X)$ 和 $\operatorname{Var}(Y \mid X)$ 的恒定性。统计量定义为 $\operatorname{LiNGIC}(X,Y) = \| \operatorname{Cov}(\varphi^1(X), \varphi^2(Y)) \|_{\mathcal{HS}}^2$，其中 $\varphi^1$ 和 $\varphi^2$ 为块对角特征映射。

**2. 核函数选择：Y 侧采用 2 阶多项式核**

- **Baseline（HSIC）**：$X$ 和 $Y$ 两侧均使用通用核（如高斯核），试图捕捉所有阶的依赖。
- **LiNGIC**：$X$ 侧保留通用核 $\phi(\cdot)$ 以提供丰富的函数空间，$Y$ 侧则使用 2 阶多项式核 $\psi(y) = (y, y^2)^\top$。这一设计直接对应 Theorem 4.3 中的条件——2 阶多项式核恰好捕获了 $Y$ 的均值和方差信息，避免了对高阶矩的无谓建模，从而在不损失必要信息的前提下降低估计方差。

**3. 对称化处理：通过块对角特征映射合并两个方向**

- **Baseline（HSIC）**：原始 HSIC 是不对称的，仅测量一个方向的依赖。
- **LiNGIC**：通过构造块对角特征映射 $\varphi^1(x) = \begin{bmatrix} \phi(x) & \mathbf{0} \\ \mathbf{0} & \psi(x) \end{bmatrix}$，将 $X \to Y$ 和 $Y \to X$ 两个方向的检验信息合并为一个对称统计量。样本估计量为：

$$\operatorname{LiNGIC}_b(\mathcal{D}) = \frac{1}{n^2} \operatorname{Tr}(K_X H L_Y H) + \frac{1}{n^2} \operatorname{Tr}(K_Y H L_X H)$$

其中 $K_X, K_Y$ 为通用核矩阵，$L_X, L_Y$ 为多项式核矩阵，$H = I - \frac{1}{n} \mathbf{1}\mathbf{1}^\top$ 为中心化矩阵。对称化不仅提高了数值稳定性（附录 E 指出原始不对称版本在重尾分布下可能出现极端值），还使统计量在两个方向上具有一致的检验能力。

### 分布近似创新：针对 LiNGIC 的 Gamma 近似

虽然 HSIC 和 LiNGIC 的零假设渐近分布均为加权 $\chi^2$ 和（**Theorem 4.5**：$n \operatorname{LiNGIC}_b(\mathcal{D}) \xrightarrow{d} \sum_{l=1}^{\infty} \lambda_l \chi_{1l}^2$），但 LiNGIC 的核结构不同，导致权重 $\lambda_l$ 的估计公式需要重新推导。论文在 **Theorem 4.7** 中给出了针对 LiNGIC 的矩匹配 Gamma 近似参数估计，其中均值的核心估计量为：

$$\widehat{A} = \widehat{\mu_{xx}^k \mu_{yy}^l} + \widehat{\|\mu_x^k\|^2} \widehat{\|\mu_y^l\|^2} - \widehat{\mu_{xx}^k} \widehat{\|\mu_y^l\|^2} - \widehat{\mu_{yy}^l} \widehat{\|\mu_x^k\|^2} + \cdots$$

这一近似使 LiNGIC 在实际应用中无需昂贵的排列检验（permutation test），即可快速获得 $p$-值，同时有效控制 I 型错误在名义水平 $\alpha = 0.05$ 附近。

### 创新边界与适用条件

上述创新的有效性严格依赖于**线性混合且噪声独立非高斯**的假设。当数据包含非线性混合或高斯成分时，Theorem 4.2 的等价性不再成立，LiNGIC 的优势可能消失。在 Sachs 真实数据上的下游因果发现实验中，LiNGIC 的 F1 分数（0.22）未超越 dCor（0.29），提示模型假设对实际数据的契合度仍需进一步验证。此外，当前版本仅支持两变量独立性检验，尚未扩展至多变量联合独立性（类比 dHSIC），计算复杂度仍为 $O(n^2)$ 且未提供基于随机特征的加速版本。



### 问题设定与输入输出

LiNGIC 框架面向一个受限但广泛存在的检验问题：给定两个随机变量 $X$ 和 $Y$，它们均为有限个独立非高斯成分的线性混合，判断 $X$ 与 $Y$ 是否独立。输入为观测样本 $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^n$，输出为二值检验决策（拒绝或接受独立性原假设）及对应的 $p$ 值。

### 核心检验逻辑

整个 pipeline 围绕一个关键理论等价性构建：在线性非高斯混合模型中，$X \perp\!\!\!\perp Y$ 当且仅当条件期望 $\mathbb{E}(Y|X)$ 为常数且条件方差 $\mathrm{Var}(Y|X)$ 为常数（Theorem 4.2）。这一等价性将原本需要捕捉任意形式依赖的检验问题，降维为仅需验证一阶矩和二阶矩的恒定性。

进一步，Theorem 4.3 将这两个条件转化为可操作的协方差约束：$X \perp\!\!\!\perp Y$ 当且仅当对任意有界连续函数 $f$，同时满足 $\mathrm{Cov}(f(X), Y) = 0$ 和 $\mathrm{Cov}(f(X), Y^2) = 0$。这意味着检验只需检查 $X$ 与 $Y$ 之间、以及 $X$ 与 $Y^2$ 之间的所有非线性相关性是否为零。

### Pipeline 模块

框架包含两个串联模块：

**模块 1：LiNGIC 统计量计算。** 将上述协方差约束嵌入再生核 Hilbert 空间框架。具体做法是：$X$ 侧使用通用核 $\phi(\cdot)$（如高斯核）以捕获任意非线性依赖，$Y$ 侧使用 2 阶多项式核 $\psi(\cdot)$ 以捕获均值和方差信息。不对称版本 $\mathrm{LiNGIC}_1$ 定义为 $\| \mathrm{Cov}(\phi(X), \psi(Y)) \|_{\mathcal{HS}}^2$。为避免多项式核在重尾分布下带来的数值不稳定，通过块对角特征映射将两个方向合并，得到对称统计量：

$$\mathrm{LiNGIC}(X,Y) = \| \mathrm{Cov}(\varphi^1(X), \varphi^2(Y)) \|_{\mathcal{HS}}^2$$

其样本估计为基于 V-统计量的偏差形式：

$$\mathrm{LiNGIC}_b(\mathcal{D}) = \frac{1}{n^2} \mathrm{Tr}(K_X H L_Y H) + \frac{1}{n^2} \mathrm{Tr}(K_Y H L_X H)$$

其中 $K_X, K_Y$ 为通用核矩阵，$L_X, L_Y$ 为多项式核矩阵，$H = I - \frac{1}{n}\mathbf{1}\mathbf{1}^\top$ 为中心化矩阵。

**模块 2：Gamma 近似零分布估计。** 零假设下 $n \cdot \mathrm{LiNGIC}_b(\mathcal{D})$ 渐近收敛于加权 $\chi^2$ 和 $\sum_{l=1}^{\infty} \lambda_l \chi_{1l}^2$（Theorem 4.5），但该分布依赖未知的数据生成过程。为快速计算 $p$ 值，采用矩匹配方法：估计零假设下统计量的均值 $\widehat{A}$ 和方差，进而拟合 Gamma 分布的形状与尺度参数（Theorem 4.7），实现常数时间的阈值判断。

### 与 HSIC 的关键差异

| 设计维度 | HSIC | LiNGIC |
|---------|------|--------|
| 检验准则 | 捕获任意形式依赖 | 仅检验 $\mathrm{Cov}(f(X),Y)$ 和 $\mathrm{Cov}(f(X),Y^2)$ 是否为零 |
| $Y$ 侧核函数 | 通用核（如高斯核） | 2 阶多项式核 |
| 对称性 | 不对称 | 通过块对角特征映射对称化 |
| 渐近近似 | 加权 $\chi^2$ 或 Gamma 近似 | Gamma 近似（矩公式针对 LiNGIC 重新推导） |

这一简化使得 LiNGIC 在满足线性非高斯假设的场景下，能以更低的方差实现更高的检验功效，而计算复杂度仍为 $O(n^2)$，与 HSIC 同阶（Table 5）。



### 模块一：LiNGIC 统计量构造

LiNGIC 的构造围绕一个核心洞察展开：在线性非高斯混合模型中，检验 $X$ 与 $Y$ 的独立性等价于检验 $\mathbb{E}(Y|X)$ 和 $\mathrm{Var}(Y|X)$ 是否为常数（Theorem 4.2）。这意味着无需捕捉全部高阶依赖，只需验证一阶矩和二阶矩的恒定性。

基于此，Theorem 4.3 将条件矩检验转化为协方差检验：$X \perp\!\!\!\perp Y$ 当且仅当对任意有界连续函数 $f$，同时满足 $\mathrm{Cov}(f(X), Y) = 0$ 和 $\mathrm{Cov}(f(X), Y^2) = 0$。这为核化实现提供了直接入口。

**LiNGIC₁ 定义**（Section 4.2）：在 $X$ 侧使用通用核 $\phi$（如高斯核），在 $Y$ 侧使用 2 阶多项式核 $\psi$，统计量定义为交叉协方差算子的 Hilbert-Schmidt 范数平方：

$$\mathrm{LiNGIC}_1 (X,Y) = \| \mathrm{Cov}( \phi(X), \psi(Y) ) \|_{\mathcal{HS}}^2$$

其中 $\psi(Y) = (Y, Y^2)$ 的多项式特征映射恰好捕获了 $Y$ 的均值和方差信息，而通用核 $\phi$ 负责在 $X$ 侧探测任意形式的条件均值变化。

**对称化处理**：原始 $\mathrm{LiNGIC}_1$ 不对称，且在重尾分布下可能出现数值不稳定。为此，通过块对角特征映射合并两个方向的信息，得到对称统计量：

$$\mathrm{LiNGIC}(X,Y) = \| \mathrm{Cov}( \varphi^1(X), \varphi^2(Y) ) \|_{\mathcal{HS}}^2$$

其中 $\varphi^1(x) = \begin{bmatrix} \phi(x) & \mathbf{0} \\ \mathbf{0} & \psi(x) \end{bmatrix}$，$\varphi^2(y)$ 类似构造。该对称版本提高了数值稳定性（附录 E）。

**样本估计量**：基于 V-统计量，偏差估计量为：

$$\mathrm{LiNGIC}_b (\mathcal{D}) = \frac{1}{n^2} \mathrm{Tr} ( K_X H L_Y H ) + \frac{1}{n^2} \mathrm{Tr} ( K_Y H L_X H )$$

其中 $K_X, K_Y$ 分别为 $X$ 侧和 $Y$ 侧的通用核矩阵，$L_X, L_Y$ 为对应的 2 阶多项式核矩阵，$H = I - \frac{1}{n}\mathbf{1}\mathbf{1}^\top$ 为中心化矩阵。

### 模块二：渐近分布与 Gamma 近似

**零假设下的渐近分布**（Theorem 4.5）：在独立性假设 $\mathcal{H}_0$ 下，缩放后的统计量收敛于加权 $\chi^2$ 和：

$$n \,\mathrm{LiNGIC}_b (\mathcal{D}) \stackrel{d}{\to} \sum_{l=1}^{\infty} \lambda_l \chi_{1l}^2$$

其中 $\lambda_l$ 由对称核函数 $h_{ijqr}$ 的特征值方程决定，$\chi_{1l}^2$ 为独立的标准 $\chi^2_1$ 变量。

**对立假设下的渐近分布**（Theorem 4.6）：当依赖存在时，统计量经 $\sqrt{n}$ 缩放后渐近正态：

$$\sqrt{n} ( \mathrm{LiNGIC}_b(\mathcal{D}) - \mathrm{LiNGIC}(X,Y) ) \xrightarrow{d} \mathcal{N}(0,\sigma^2)$$

其中渐近方差 $\sigma^2 = 16( \mathbb{E}_i ( \mathbb{E}_{j,q,r} h_{ijqr} )^2 - \mathrm{LiNGIC}(X,Y)^2 )$。

**Gamma 近似**（Theorem 4.7）：实际检验中，无限加权 $\chi^2$ 和难以直接计算，采用矩匹配的 Gamma 近似。通过估计零假设下 $n \cdot \mathrm{LiNGIC}_b$ 的均值和方差，得到 Gamma 分布的形状和尺度参数，用于快速计算 $p$ 值和阈值判断。均值估计公式涉及核矩阵的迹运算：

$$\widehat{A} = \widehat{\mu_{xx}^k \mu_{yy}^l} + \widehat{\|\mu_x^k\|^2} \widehat{\|\mu_y^l\|^2} - \widehat{\mu_{xx}^k} \widehat{\|\mu_y^l\|^2} - \widehat{\mu_{yy}^l} \widehat{\|\mu_x^k\|^2} + \dots$$

该近似避免了耗时的排列检验，使 LiNGIC 的计算复杂度与 HSIC 同为 $O(n^2)$（Table 5 验证了运行时间无显著额外开销）。

### 关键设计决策的消融依据

1. **仅检验一阶和二阶矩的充分性**：Figure 2 的反例表明，单独检验 $\mathbb{E}(Y|X)$ 恒定或 $\mathrm{Var}(Y|X)$ 恒定均不足以判定独立性——当条件方差随 $X$ 变化时，即使条件期望为常数，$X$ 与 $Y$ 仍可存在依赖。因此必须同时检验两个条件。

2. **多项式核的方差降低效应**：$Y$ 侧使用 2 阶多项式核（而非通用核）直接对应 Theorem 4.3 的协方差条件，在捕获必要信息的同时降低了估计方差，使 LiNGIC 在弱依赖下（如 Table 4 中 $c=0.8$ 时）功效优势更为显著（LiNGIC 0.86 vs HSIC 0.53）。

3. **对称化的必要性**：不对称的 $\mathrm{LiNGIC}_1$ 在重尾分布（如 Student-t）下可能出现极端值，对称版本通过合并两个方向的交叉协方差信息缓解了此问题（附录 E），使统计量在不同分布下表现更稳健。

### 公式符号速查

| 符号 | 含义 |
|------|------|
| $\phi(\cdot)$ | 通用核（如高斯核）的特征映射 |
| $\psi(\cdot)$ | 2 阶多项式核的特征映射，$\psi(Y) = (Y, Y^2)$ |
| $\varphi^1, \varphi^2$ | 块对角特征映射，用于对称化 |
| $K_X, K_Y$ | 通用核的 Gram 矩阵 |
| $L_X, L_Y$ | 多项式核的 Gram 矩阵 |
| $H$ | 中心化矩阵 $I - \frac{1}{n}\mathbf{1}\mathbf{1}^\top$ |
| $h_{ijqr}$ | 对称核函数，用于 V-统计量表达和渐近分析 |
| $\lambda_l$ | 零假设渐近分布中的加权系数 |



## 实验与关键发现

### 核心实验设计

实验围绕两个层次展开：(1) 独立性检验本身的统计功效与 I 型错误控制；(2) 将 LiNGIC 嵌入 Direct-LiNGAM 因果发现框架后的下游性能。合成数据严格遵循线性非高斯混合模型：独立成分 $\varepsilon_i$ 从 Laplace、Student-t、Uniform、Truncated Normal 等非高斯分布采样，通过线性混合 $X = \sum b_i \varepsilon_i$, $Y = \sum a_i \varepsilon_i$ 生成。依赖与独立的区分在于：依赖情形下 $X$ 和 $Y$ 共享部分 $\varepsilon_i$（对应系数乘积非零），独立情形下两者使用不相交的独立成分集。

### 主结果：检验功效与 I 型错误控制

**Figure 3** 展示了固定样本量 $n=500$ 时，检验功效随独立成分数 $d \in \{2,3,4,5,6\}$ 变化的趋势。在 Laplace 分布下，LiNGIC 在 $d=3$ 时达到功效 0.80，而 HSIC 为 0.77，SCIT 仅为 0.61（Table 3）。在 Student-t 分布下差距更为显著：LiNGIC 功效 0.97，HSIC 为 0.85，提升达 +0.12。所有方法在零假设下的 I 型错误均被控制在名义水平 $\alpha=0.05$ 附近，表明 LiNGIC 在不牺牲假阳性控制的前提下获得了更高的灵敏度。

![[assets/figures/papers/iclr26_0009_Uc1EAICxTD_Independence_Test_for_Linear_Non-Gaussian_Data_a/figures/011_Table_3.jpg]]
*Table 3: Comparison of Type I error and Power across different distributions and dimensions (d)*

![[assets/figures/papers/iclr26_0009_Uc1EAICxTD_Independence_Test_for_Linear_Non-Gaussian_Data_a/figures/003_Figure_3.jpg]]
*Figure 3: The experiment results when we change the number of the independent components of the linear mixtures with 500 samples. The number of components d $\in \{$ 2 , $\bar { 3 }$ , 4 , 5 , 6 $\}$ . Each column shows the results with $\varepsilon _ { i } \sim { \bf a }$ different distribution. The first row demonstrates Test Power and the second row shows the Type I error. The significance level 0.05 is annotated as the black line

**Figure 4** 进一步检验样本量 $n \in \{300,500,700,900,1100\}$ 的影响。LiNGIC 的功效随 $n$ 单调增长，且在所有样本量下均优于 HSIC、HSIC-RFF、dCor 和 SCIT。这一优势在 Student-t 和 Laplace 等重尾分布下尤为突出，验证了 Theorem 4.2 的理论预期：当数据满足线性非高斯假设时，仅需检验条件期望和条件方差的恒定性即可判定独立，无需捕捉所有高阶依赖。

![[assets/figures/papers/iclr26_0009_Uc1EAICxTD_Independence_Test_for_Linear_Non-Gaussian_Data_a/figures/004_Figure_4.jpg]]
*Figure 4: The experiment results when we change the sample sizes of the linear mixtures of 3 independent components from different distributions. The sample sizes n $\in \{$ 3 0 0 , 5 0 0 , 7 0 0 , 9 0 0 , 1 1 0 0 $\}$*

### 依赖性强度敏感性

**Table 4** 报告了在 Student-t 分布、$d=3$、$n=500$ 设置下，改变依赖强度 $c$（共享成分的系数乘积）时的功效对比。当 $c=0.8$（弱依赖）时，LiNGIC 功效为 0.86，HSIC 仅为 0.53，差距达 +0.33。这表明 LiNGIC 对微弱依赖的检测能力显著优于通用核方法——通用核在弱信号下需要更多样本才能区分依赖与噪声，而 LiNGIC 通过将检验降维至一阶和二阶矩，有效降低了估计方差。

![[assets/figures/papers/iclr26_0009_Uc1EAICxTD_Independence_Test_for_Linear_Non-Gaussian_Data_a/figures/014_Table_4.jpg]]
*Table 4: Power comparison (higher is better) under varying dependence strength c. The last column reports the Type I error at c = 0 (lower is better, target α = 0.05)*

### 下游因果发现任务

**Table 1** 展示了将不同独立性检验嵌入 Direct-LiNGAM 后在合成 Sachs 数据（10 节点，Uniform 噪声）上的表现。LiNGIC 取得了 SHD=0.8 和 F1=0.98，优于 dCor 的 SHD=1.0 和 F1=0.97，以及 HSIC-RFF 的 SHD=1.2 和 F1=0.93。在四种噪声类型（Uniform、Laplace、Student-t、TruncNorm）上，LiNGIC 的 SHD 均为最低，说明更准确的独立性判断直接转化为更精确的因果图结构恢复。

![[assets/figures/papers/iclr26_0009_Uc1EAICxTD_Independence_Test_for_Linear_Non-Gaussian_Data_a/figures/005_Table_1.jpg]]
*Table 1: SHD and F1 Score of Direct-LiNGAM algorithm using different testing methods*

然而，在真实 Sachs 数据集（Table 7）上，LiNGIC 的 F1 为 0.22，低于 dCor 的 0.29。这一退化提示模型假设与真实数据之间存在差距：Sachs 数据中的蛋白质信号网络可能包含非线性调控关系或近似高斯噪声成分，此时 Theorem 4.2 的等价性不再严格成立，LiNGIC 的结构化优势反而成为限制。

### 消融分析

**单独检验条件均值或条件方差不充分。** Figure 2 给出了一个反例：当 $\mathbb{E}(Y|X)$ 为常数但 $\mathbb{V}\text{ar}(Y|X)$ 随 $X$ 变化时，$X$ 与 $Y$ 存在依赖。Theorem 4.2 的等价性要求两个条件同时成立，缺少任一方面都会导致假阴性。LiNGIC 通过同时检验 $\text{Cov}(f(X),Y)=0$ 和 $\text{Cov}(f(X),Y^2)=0$（Theorem 4.3）来覆盖这两个条件。

![[assets/figures/papers/iclr26_0009_Uc1EAICxTD_Independence_Test_for_Linear_Non-Gaussian_Data_a/figures/002_Figure_2.jpg]]

**对称化处理缓解数值不稳定。** 原始不对称版本 LiNGIC₁ 在重尾分布（如 Student-t）下可能出现极端统计量值。对称化版本通过块对角特征映射 $\varphi^1(x) = \begin{bmatrix} \phi(x) & 0 \\ 0 & \psi(x) \end{bmatrix}$ 合并两个方向的协方差信息，在附录 E 中报告了更稳定的零分布近似和更一致的 I 型错误控制。

**二阶多项式核的选择。** LiNGIC 在 $Y$ 侧使用二阶多项式核 $\psi(y) = (y, y^2)$ 而非通用核，这直接对应 Theorem 4.3 中检验 $Y$ 和 $Y^2$ 与 $f(X)$ 协方差为零的需求。实验表明，这一针对性设计在不损失功效的前提下降低了统计量的估计方差，而通用核在有限样本下会因捕捉无关高阶矩而引入额外噪声。

### 计算开销

**Table 5** 显示 LiNGIC 的运行时间与 HSIC 同阶 $O(n^2)$，无显著额外开销。在 Direct-LiNGAM 的完整流程中（Table 6），使用 LiNGIC 替代 HSIC 的总运行时间基本持平。当前版本未提供基于随机傅里叶特征或 Nyström 近似的加速方案，这在大规模数据场景下构成实际瓶颈。

### 失败模式与假设边界

LiNGIC 的功效优势严格依赖于两个前提：(1) 数据由独立非高斯成分线性混合生成；(2) 噪声成分的方差有限。当这些假设不满足时——例如包含非线性混合、存在高斯成分、或真实数据偏离线性非高斯模型——Theorem 4.2 的“独立 $\iff$ 条件均值与方差恒定”等价性失效。Sachs 真实数据上的 F1 退化（Table 7）正是这一边界的体现：此时 LiNGIC 可能漏检仅在高阶矩中体现的依赖关系，而 HSIC 或 dCor 等通用检验反而更鲁棒。在实际应用中，若对数据生成过程的线性非高斯性质存疑，建议将 LiNGIC 作为互补工具而非完全替代通用检验。



## 定位与知识库关联

### 与基线方法的关系

LiNGIC 的核心定位是在**线性非高斯模型**这一特定结构假设下，对通用非参数独立性检验进行**降维强化**。其与各基线方法的本质差异可归结为检验准则的收缩：

- **vs HSIC / dCor / RDC**：HSIC 等通用检验通过特征核（如高斯核）在再生核希尔伯特空间中捕捉任意形式的依赖，等价于检验 $ \mathbb{E}[f(X)g(Y)] = \mathbb{E}[f(X)]\mathbb{E}[g(Y)] $ 对所有有界连续函数 $f,g$ 成立。这一全空间检验在有限样本下统计功效分散，对微弱依赖的灵敏度不足。LiNGIC 将检验空间收缩至仅需验证 $ \mathrm{Cov}(f(X), Y) = 0 $ 和 $ \mathrm{Cov}(f(X), Y^2) = 0 $（Theorem 4.3），等效于检验条件期望和条件方差的恒定性（Theorem 4.2）。这种降维在合成数据上转化为显著的功效增益：Student-t 分布下 LiNGIC 功效达 0.97，HSIC 为 0.85（Table 3, d=3, n=500）；弱依赖强度 c=0.8 时，LiNGIC 功效 0.86 远超 HSIC 的 0.53（Table 4）。

- **vs SCIT**：SCIT 面向条件独立性检验，而 LiNGIC 聚焦二元边缘独立性，二者问题设定不同。在合成数据直接对比中，LiNGIC 功效显著优于 SCIT（Laplace: 0.80 vs 0.61; Student-t: 0.97 vs 0.69）。

- **核函数选择的本质差异**：HSIC 对 X 和 Y 两侧均使用通用核。LiNGIC 在 Y 侧采用 2 阶多项式核 $ \psi(y) = (y, y^2)^\top $，仅捕获一阶和二阶矩信息，从而将检验聚焦于线性非高斯结构下的充分统计量。X 侧仍保留通用核以保证对任意非线性变换的覆盖。这种非对称设计是 LiNGIC 功效优势的关键来源。

- **对称化处理**：原始 HSIC 本身不对称，LiNGIC 通过块对角特征映射将两个方向合并为对称统计量，避免多项式核在重尾分布下可能引起的数值不稳定（Appendix E）。

### 适用边界与假设依赖

LiNGIC 的理论保证建立在以下严格假设之上，任一假设的偏离都可能导致检验失效：

1. **线性混合**：X 和 Y 必须是独立成分的线性组合 $ X = \sum b_i \varepsilon_i $, $ Y = \sum a_i \varepsilon_i $。若数据包含非线性混合（如后非线性模型），Theorem 4.2 的等价性不再成立。
2. **独立非高斯成分**：成分 $ \varepsilon_i $ 必须相互独立且为非高斯分布。若任一共享成分为高斯，Darmois-Skitovich 定理的条件被破坏，条件矩恒定不再蕴含独立性。
3. **有限方差**：Theorem 4.2 要求成分具有有限方差，这排除了柯西分布等重尾无限方差情形。

当数据严格满足上述假设时，LiNGIC 在多种非高斯分布（Laplace, Student-t, Uniform, Truncated Normal）下均能有效控制 I 型错误于名义水平 α=0.05 附近（Figure 3/4），且功效一致优于 HSIC 等通用检验。但当模型假设不成立时，功效优势可能消失甚至反转——Sachs 真实数据上，下游 Direct-LiNGAM 的 F1 分数为 0.22，低于 dCor 的 0.29（Table 7），提示实际数据对线性非高斯假设的契合度有限。

### 局限与已知失效模式

- **非线性混合失效**：若数据生成过程涉及非线性变换，条件矩恒定与独立性之间的等价关系断裂。此时 LiNGIC 退化为仅检验一阶和二阶依赖，可能漏检高阶非线性依赖。
- **高斯成分污染**：当共享成分中包含高斯变量时，即使条件均值和方差恒定，X 与 Y 仍可能存在高阶依赖。LiNGIC 对此类依赖完全盲视。
- **仅支持二元检验**：当前版本仅适用于两个随机变量的独立性检验，尚未扩展到多元联合独立性（类比 dHSIC）。
- **计算复杂度**：统计量计算复杂度为 $O(n^2)$，与 HSIC 同阶（Table 5 证实运行时间无显著额外开销），但未提供基于随机傅里叶特征或 Nyström 近似的加速版本。
- **真实数据表现受限**：Sachs 数据集上 LiNGIC 的下游因果发现 F1 未超越 dCor，说明模型假设与实际数据分布之间的差距是实际应用的主要瓶颈。

### 开放问题

1. **非线性扩展**：能否将检验准则推广到后非线性模型 $ Y = g( \sum a_i \varepsilon_i ) $ 或一般加性噪声模型？这需要重新刻画条件矩恒定与独立性的等价条件。
2. **多变量版本**：如何构造直接测试多个线性非高斯变量联合独立性的统计量，类似 dHSIC 的多变量扩展？
3. **加速近似**：是否存在基于随机特征的近似算法，可在不显著损失统计功效的前提下将计算复杂度降至 $O(n)$ 或 $O(n \log n)$？
4. **混合高斯-非高斯场景**：当部分成分为高斯时，检验等价性是否可松弛？能否设计自适应机制，在检测到高斯成分时自动混合 LiNGIC 与 HSIC 的检验准则？
5. **高维稀疏场景**：在成分数量远大于样本量的高维设定下，LiNGIC 的渐近分布近似质量如何？是否需要针对稀疏结构进行修正？



## 原文 PDF

![[paperPDFs/ICLR_2026/Independence_Test_for_Linear_Non_Gaussian_Data_and_Applications_in_Causal_Discovery.pdf]]
