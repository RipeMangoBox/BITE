---
title: "A Derandomization Framework for Structure Discovery: Applications in Neural Networks and Beyond"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Derandomization_Framework_for_Structure_Discovery_Applications_in_Neural_Networks_and_Beyond.pdf
aliases:
- DF
- DFSDANNB
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/probabilistic_methods
core_operator: "使用ρ-二阶驻点（ρ-SOSP）作为解概念，并利用Stein引理将关于偏置b的二阶导数与关于权重W的一阶导数联系起来，从而在极弱正则化下导出W的Frobenius范数上界。"
primary_logic: "对于形如f(W,b;θ)=E_x[g_θ(Wx+b)]+λ‖W‖_F^2的目标函数，任何ρ-SOSP都满足‖W‖_F ≤ ρ/(2λ-√(Kρ))；当ρ→0时W→0。这一“去随机化引理”表明，二阶驻点条件本身就能迫使第一层权重趋于零（低秩），无需强正则化或特定优化器。"
claims:
- "任何ρ-SOSP满足‖W‖_F ≤ ρ/(2λ-√(Kρ))"
- "当偏置可训练时，极小正则化下w即可收敛到0；冻结偏置则需要大λ"
- "在教师-学生设定下，任何ρ-SOSP的第一层权重矩阵W满足‖W_⊥‖_F ≤ ρ/(2λ-√(Kρ))"
- "运行Algorithm 1（扰动梯度下降）可在多项式时间内以高概率得到‖W_⊥‖_F < ε的解"
---

# A Derandomization Framework for Structure Discovery: Applications in Neural Networks and Beyond

> [!tip] 核心洞察
> 对于形如f(W,b;θ)=E_x[g_θ(Wx+b)]+λ‖W‖_F^2的目标函数，任何ρ-SOSP都满足‖W‖_F ≤ ρ/(2λ-√(Kρ))；当ρ→0时W→0。这一“去随机化引理”表明，二阶驻点条件本身就能迫使第一层权重趋于零（低秩），无需强正则化或特定优化器。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 结构发现的去随机化框架：在神经网络及其他领域的应用 |
| 英文题名 | A Derandomization Framework for Structure Discovery: Applications in Neural Networks and Beyond |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=dtIf5HsOIn); [GitHub](https://github.com/yorgospantis/StructureDiscovery) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/probabilistic_methods |
| Method | 去随机化框架（Derandomization Framework） |
| Dataset | 单层NN玩具示例（ReLU³激活，一维输入）, 两层NN教师-学生设定（tanh单索引教师，d=2, h=1000）, MAXCUT（随机图）, Johnson-Lindenstrauss嵌入（k=30, d=500, n=100） |

> [!tip] 效果简介
> - 单层NN玩具示例（ReLU³激活，一维输入） 上，最优权重w* vs 正则化参数λ 为 训练偏置时，w*在极小λ下即收敛到0，对比 冻结偏置时，w*仅在λ很大时才接近0，变化 训练偏置使所需λ降低数个数量级。
> - 两层NN教师-学生设定（tanh单索引教师，d=2, h=1000） 上，第一层权重是否收敛到主成分子空间 为 权重收敛到教师方向张成的子空间，对比 N/A（本文首次在如此宽松条件下展示），变化 N/A。
> - MAXCUT（随机图） 上，割值 为 达到最优割值41，对比 Goemans-Williamson随机化算法约36，变化 +5（约14%提升）。

## 概述

本文提出了一种**去随机化框架**，用于解释神经网络训练中第一层权重自然收敛到低秩结构的现象。核心问题在于：现有理论（如Mousavi-Hosseini等人2023年的工作）在证明这一收敛性时，需要强正则化、浅层网络、冻结偏置等严格假设，限制了理论的普适性。本文的关键洞察是：对于形如 $f(W,b;\theta) = \mathbb{E}_x[g_\theta(Wx+b)] + \lambda\|W\|_F^2$ 的目标函数，任何 $\rho$-二阶驻点（$\rho$-SOSP）都满足 $\|W\|_F \le \rho/(2\lambda - \sqrt{K\rho})$（Lemma 3.1, Key Derandomization Lemma）。当 $\rho \to 0$ 时 $W \to 0$，这意味着**二阶驻点条件本身就能迫使第一层权重趋于零（低秩）**，无需强正则化或特定优化器。

该方法的核心机制是利用**Stein引理**将关于偏置 $b$ 的二阶导数与关于权重 $W$ 的一阶导数联系起来，从而在极弱正则化下导出 $W$ 的Frobenius范数上界。与基线方法相比，本文放松了多项关键假设：正则化强度 $\lambda$ 可从任意小值（$\lambda > \sqrt{K\rho}/2$）生效；偏置 $b$ 可训练而非冻结；网络可为任意大小和深度；优化器可为任何能收敛到 $\rho$-SOSP 的方法（如扰动梯度下降PGD）。

主要实验结果包括：（1）在单层NN玩具示例中，训练偏置使所需正则化 $\lambda$ 降低数个数量级（Figure 1 vs Figure 2）；（2）在两层NN教师-学生设定下，第一层权重收敛到教师方向张成的子空间（Figure 3）；（3）在MAXCUT问题上，优化方法达到最优割值41，优于Goemans-Williamson随机化算法的约36（Figure 4）；（4）在Johnson-Lindenstrauss嵌入中，最大失真降至接近零（Figure 6）。然而，所有实验均基于合成数据（高斯输入），未在真实大规模数据集上验证，且MAXCUT实验仅在一个随机图上进行。

## 背景与动机

神经网络中第一层权重的结构发现（如收敛到低秩子空间）是理解特征学习机制的核心问题。现有理论工作（如 Mousavi-Hosseini 等人 2023 年的工作）在证明此类收敛时，依赖于一系列严格假设：需要强正则化、仅适用于浅层网络、冻结偏置（b=0），且优化器限定为 SGD。这些限制使得理论结果与实践中观察到的现象之间存在显著差距——实践中，深度网络在极小正则化下即可学习到有意义的低秩特征。

本文的核心动机是消除这些限制，建立一个更普适的结构发现理论。作者识别出的关键瓶颈在于：现有方法将权重收敛归因于优化器（SGD）或强正则化的特定作用，而忽略了偏置项（bias）在二阶驻点条件中的核心角色。

**因果机制的重新审视**：本文的核心洞察在于，对于形如 $f(W,b;\theta) = \mathbb{E}_x[ g_\theta(W x + b) ] + \lambda \|W\|_F^2$ 的正则化风险函数（其中输入 $x \sim \mathcal{N}(0, I_d)$），任何 $\rho$-二阶驻点（$\rho$-SOSP，即梯度范数 $\le \rho$ 且 Hessian 最小特征值 $\ge -\sqrt{K\rho}$）都自动满足一个关于权重范数的上界。通过 Stein 引理，关于权重 $W$ 的梯度可以重写为 $\frac{\partial f}{\partial W} = \mathbb{E}_x[\nabla^2 g_\theta(Wx+b) + 2\lambda I] W$。结合 $\rho$-SOSP 条件对偏置 $b$ 的 Hessian 约束（$\mathbb{E}_x[\nabla^2 g_\theta(Wx+b)] \succcurlyeq -\sqrt{K\rho} I$），可以直接导出关键的去随机化引理（Lemma 3.1）：任何 $\rho$-SOSP 满足 $\|W\|_F \le \frac{\rho}{2\lambda - \sqrt{K\rho}}$。当 $\rho \to 0$ 时，$W \to 0$。

这一机制揭示了偏置训练的必要性：训练偏置使得二阶导数信息（通过 Stein 引理）能够传导至一阶条件，从而在极小正则化下迫使权重趋于零。相比之下，冻结偏置（b=0）切断了这一传导路径，导致需要大 $\lambda$ 才能实现类似效果（Figure 1 vs Figure 2 的对比直观地展示了这一差异）。

**证据强度**：去随机化引理（Lemma 3.1）的数学推导完整，置信度为 1.0。Figure 1 和 Figure 2 的对比实验（在单层 ReLU³ 激活的玩具示例上）直接验证了偏置训练与冻结偏置在所需正则化强度上的数量级差异，置信度为 0.95。然而，该实验仅在一维输入上验证，其在高维和真实数据上的普适性尚待确认。

## 核心创新

本文的核心创新在于提出了一个“去随机化框架”，该框架从根本上改变了结构发现问题的理论假设与求解路径。相比基线方法（如Mousavi-Hosseini等人2023年的工作），该框架在多个关键维度上实现了突破，其核心是一个简洁而强大的“去随机化引理”（Key Derandomization Lemma, Lemma 3.1）。

**核心洞察：二阶驻点本身即是去随机化机制**

该框架的核心洞察在于，对于形如 $f(W,b;\theta) = \mathbb{E}_x[g_\theta(Wx+b)] + \lambda\|W\|_F^2$ 的目标函数（其中输入 $x \sim N(0, I_d)$），任何 $\rho$-二阶驻点（$\rho$-SOSP）都自动迫使第一层权重矩阵 $W$ 的Frobenius范数满足一个严格的上界：$\|W\|_F \le \rho / (2\lambda - \sqrt{K\rho})$。这意味着，当优化算法收敛到一个近似二阶驻点（$\rho$很小）时，$W$ 的范数必然很小，即模型第一层权重被迫“低秩”或趋于零。这一结论的关键在于，它不依赖于强正则化（$\lambda$可以任意小，只要大于 $\sqrt{K\rho}/2$）、特定的网络深度或宽度，也无需冻结偏置。其证明机制巧妙地运用了Stein引理，将关于权重 $W$ 的一阶导数与关于偏置 $b$ 的二阶导数联系起来，从而从 $\rho$-SOSP 的Hessian负曲率下界（$\lambda_{\min}(\nabla^2 f) \ge -\sqrt{K\rho}$）中导出了 $W$ 的范数上界。当达到完美SOSP（$\rho=0$）时，直接有 $W=0$。

**关键变化（Changed Slots）**

与基线方法相比，该框架在以下五个关键设计槽位上做出了根本性改变：

1.  **正则化强度 $\lambda$**：
    *   **基线**：需要较大的 $\lambda$ 值来迫使权重收缩。
    *   **本文**：允许任意小的 $\lambda$（只需满足 $\lambda > \sqrt{K\rho}/2$），正则化强度可由收敛精度 $\rho$ 控制。这极大地放宽了理论假设。

2.  **偏置 $b$ 是否可训练**：
    *   **基线**：通常冻结偏置（如设 $b=0$）。
    *   **本文**：**训练偏置 $b$ 是去随机化生效的必要条件**。实验（Figure 1 vs. Figure 2）清晰地展示了这一点：冻结偏置时，最优权重 $w^*$ 仅在 $\lambda$ 很大时才接近0；而训练偏置时，$w^*$ 在极小 $\lambda$ 下即收敛到0。这是因为可训练的偏置能够吸收输入分布的均值偏移，使Stein引理的推导得以成立。

3.  **解概念**：
    *   **基线**：主要关注一阶驻点（FOSP）。
    *   **本文**：采用 $\rho$-二阶驻点（$\rho$-SOSP）作为解概念。正是二阶信息（Hessian的负曲率下界）提供了驱动去随机化的关键约束。

4.  **网络深度与宽度**：
    *   **基线**：理论结果仅限于两层网络。
    *   **本文**：该框架适用于**任意大小和深度**的神经网络。其推导过程不依赖于网络的层数或宽度，仅依赖于目标函数的整体L-光滑和K-Hessian Lipschitz性质。

5.  **优化器要求**：
    *   **基线**：理论分析通常针对特定优化器（如SGD）。
    *   **本文**：该框架适用于**任何能够收敛到 $\rho$-SOSP 的方法**，例如扰动梯度下降（PGD, Algorithm 1）、Hessian descent（Algorithm 2）或SGD。这大大增强了框架的普适性。

**框架的模块化流程**

该去随机化框架由以下四个模块构成一个完整的流程：

1.  **目标函数构造**：将具体问题（如神经网络风险、MAXCUT、Johnson-Lindenstrauss嵌入）的目标函数统一写成 $f(W,b;\theta)=\mathbb{E}_x[g_\theta(Wx+b)]+\lambda\|W\|_F^2$ 的形式。
2.  **Stein引理应用**：利用Stein引理，将关于 $W$ 的梯度重写为 $\partial f/\partial W = \mathbb{E}_x[\nabla^2 g_\theta(Wx+b) + 2\lambda I] W$。这一步骤建立了 $W$ 的梯度与 $g_\theta$ 关于其输入的Hessian矩阵之间的桥梁。
3.  **$\rho$-SOSP条件验证**：结合 $\rho$-SOSP 的梯度范数上界（$\|\nabla f\| \le \rho$）和Hessian最小特征值下界（$\lambda_{\min}(\nabla^2 f) \ge -\sqrt{K\rho}$），特别是关于偏置 $b$ 的Hessian条件，代入第2步的梯度表达式，即可导出核心的去随机化引理。
4.  **优化算法**：运行如Algorithm 1（PGD）等算法，以 $O(1/\rho^2)$ 的迭代次数高概率地收敛到一个 $\rho$-SOSP，从而保证得到的 $W$ 满足低秩性质。

**实验证据与局限**

实验证据有力地支撑了上述理论创新：
*   **单层NN玩具示例**：对比Figure 1和Figure 2，直观展示了训练偏置相对于冻结偏置的巨大优势，使所需正则化强度降低数个数量级。
*   **两层NN教师-学生设定**：实验（Figure 3）首次在如此宽松的条件（任意宽度、训练偏置）下展示了两层网络第一层权重收敛到教师方向的子空间。
*   **MAXCUT和JL嵌入**：通过将问题构造为本文框架的形式，实验（Figure 4-7）展示了优化过程不仅收敛到高质量的解（MAXCUT达到最优值41，JL失真接近零），而且其内在的随机性（以方差 $\sigma^2$ 衡量）也随着优化过程被系统地消除，实现了“去随机化”。

然而，需要指出的是，该框架的实验验证存在**明显局限**：所有实验均基于**合成数据**（高斯输入），且规模较小（如NN输入维度 $d=2$，JL样本数 $n=100$）。在真实大规模数据集（如ImageNet）或高维输入下的表现尚待验证。此外，MAXCUT实验仅在一个随机图上进行，缺乏多次运行的统计结果，其稳健性需要手动验证。

## 整体框架

本文提出一个统一的去随机化框架，其核心 pipeline 由四个模块组成，共同将随机算法中的随机性消除，使解趋于确定性低秩结构。

**模块一：目标函数构造。** 将各类应用（神经网络风险最小化、MAXCUT 图割、Johnson-Lindenstrauss 嵌入）统一写成如下形式（Equation 1）：

$$
f(W,b;\theta) = \mathbb{E}_x[ g_\theta(W x + b) ] + \lambda \|W\|_F^2
$$

其中 $x \sim \mathcal{N}(0, I_d)$ 为标准高斯输入，$g_\theta$ 是参数化的非线性函数，$\lambda$ 是正则化系数。该形式的关键在于：第一层权重 $W$ 仅通过线性变换 $Wx+b$ 进入 $g_\theta$，且受 Frobenius 范数正则化约束。

**模块二：Stein 引理应用。** 利用 Stein 引理将关于 $W$ 的梯度重写为（Appendix B.1, Equation 10）：

$$
\frac{\partial f}{\partial W} = \mathbb{E}_x[\nabla^2 g_\theta(Wx+b) + 2\lambda I] W
$$

这一改写建立了关于 $W$ 的一阶导数与关于偏置 $b$ 的二阶导数（即 Hessian）之间的联系。具体地，Hessian 矩阵 $\mathbb{E}_x[\nabla^2 g_\theta(Wx+b)]$ 同时出现在两个表达式中，构成因果链中的关键桥梁。

**模块三：$\rho$-二阶驻点（$\rho$-SOSP）条件验证。** 框架采用 $\rho$-SOSP 作为解概念（Definition 2.2），要求：

$$
\|\nabla f(\mathbf{x}^*)\|_2 \le \rho \quad \text{and} \quad \lambda_{\min}(\nabla^2 f(\mathbf{x}^*)) \ge -\sqrt{K\rho}
$$

即梯度范数足够小，且 Hessian 的最小特征值不低于负值。利用模块二得到的梯度形式，结合 $\rho$-SOSP 的 Hessian 下界，可导出核心去随机化引理（Lemma 3.1）：

$$
\|W\|_F \le \frac{\rho}{2\lambda - \sqrt{K\rho}}
$$

当 $\rho \to 0$ 时，$\|W\|_F \to 0$。这意味着二阶驻点条件本身就能迫使第一层权重趋于零（低秩），无需强正则化或特定优化器。该引理是框架的理论核心，其证明仅依赖于 $g_\theta$ 的 K-Hessian Lipschitz 假设（Assumption 2.3）和 $\lambda > \sqrt{K\rho}/2$ 的温和条件。

**模块四：优化算法（Algorithm 1: 扰动梯度下降 PGD）。** 框架不依赖特定优化器，任何能收敛到 $\rho$-SOSP 的方法（如 PGD、Hessian descent、SGD）均可使用。具体地，PGD 在 $O(1/\rho^2)$ 迭代次数内以高概率收敛到 $\rho$-SOSP（Jin et al., 2017）。在教师-学生设定下，Theorem 4.2 进一步保证：运行 Algorithm 1 可在多项式时间内以高概率得到 $\|W_\perp\|_F < \varepsilon$ 的解，其中 $W_\perp$ 是权重矩阵中与教师方向正交的分量。

**输入输出流：** 输入为标准高斯数据 $x \sim \mathcal{N}(0, I_d)$ 和任务定义（损失函数、正则化参数 $\lambda$）。输出为满足 $\|W\|_F \le \rho/(2\lambda - \sqrt{K\rho})$ 的权重矩阵 $W$，以及训练后的偏置 $b$ 和网络参数 $\theta$。在神经网络应用中，这一输出意味着第一层权重自动收敛到低秩结构（教师子空间）；在 MAXCUT 中，输出为确定性割向量；在 JL 嵌入中，输出为低方差投影矩阵。

**框架的因果机制：** 正则化 $\lambda$ 和 $\rho$-SOSP 的精度 $\rho$ 是主要控制旋钮。训练偏置 $b$ 是必要条件——冻结偏置时，需要大 $\lambda$ 才能迫使 $W$ 接近零；训练偏置时，极小 $\lambda$ 即可生效（Figure 1 vs Figure 2）。这一差异源于 Stein 引理建立的梯度- Hessian 联系：当偏置可训练时，关于 $b$ 的 Hessian 约束直接作用于关于 $W$ 的梯度，形成自洽的收缩机制。

## 核心模块与公式推导

本文的核心理论贡献是一个通用“去随机化引理”，它揭示了正则化风险函数的二阶驻点条件与第一层权重矩阵低秩结构之间的内在联系。该引理的核心机制在于：通过利用**ρ-二阶驻点（ρ-SOSP）** 的定义，并借助 **Stein 引理** 将关于偏置 `b` 的二阶导数信息与关于权重 `W` 的一阶导数联系起来，从而在极弱的正则化假设下，为 `W` 的 Frobenius 范数导出一个严格的上界。

**核心公式与变量含义**

1.  **通用目标函数族**：
    $$f(W,b;\theta) = \mathbb{E}_x[ g_\theta(W x + b) ] + \lambda \|W\|_F^2$$
    *   `x ~ N(0, I_d)`: 标准高斯分布输入。
    *   `g_θ`: 参数化的非线性函数，代表神经网络或其他模型。
    *   `W`, `b`: 第一层权重矩阵和偏置向量。
    *   `λ`: 权重衰减正则化系数。
    *   `‖W‖_F`: W的Frobenius范数。

2.  **ρ-二阶驻点 (ρ-SOSP) 条件**：
    $$\|\nabla f(x^*)\|_2 \le \rho \quad \text{and} \quad \lambda_{\min}(\nabla^2 f(x^*)) \ge -\sqrt{K\rho}$$
    *   `f`: 目标函数，满足L-光滑和K-Hessian Lipschitz假设。
    *   `ρ`: 驻点的近似程度参数。
    *   `K`: Hessian Lipschitz常数。
    *   该定义意味着点 `x*` 的梯度范数很小，且Hessian矩阵的负曲率有界。

3.  **核心去随机化引理 (Lemma 3.1) 的边界**：
    $$\| W \|_F \le \frac{\rho}{2\lambda - \sqrt{K\rho}}$$
    *   **推导瓶颈**：该不等式的推导依赖于一个关键桥梁——**Stein 引理**。它允许将关于 `W` 的梯度重写为：
        $$\frac{\partial f(W, b, \theta)}{\partial W} = \mathbb{E}_{x}[\nabla^2 g_{\theta}(W x + b) + 2\lambda I] W$$
    *   **因果机制**：在 `ρ`-SOSP 处，关于 `b` 的 Hessian 矩阵 `E_x[∇²g_θ(Wx+b)]` 满足 `≽ -√(Kρ) I`。将这个下界代入上述梯度表达式中，并结合 `ρ`-SOSP 的梯度范数上界 `‖∂f/∂W‖_F ≤ ρ`，即可推导出 `W` 的范数上界。
    *   **证据强度**：该引理是本文理论的核心，置信度为 1.0。当 `ρ → 0` 时，`‖W‖_F → 0`，表明一个完美的二阶驻点（SOSP）会强制权重矩阵为零。这解释了为什么收敛到 `ρ`-SOSP 是“去随机化”的充分条件。

4.  **教师-学生模型下的结构发现 (Theorem 4.1)**：
    $$\| W_\perp \|_F \le \frac{\rho}{2\lambda - \sqrt{K\rho}}$$
    *   `W_⊥`: 权重矩阵中与教师信号方向正交的分量。
    *   该定理将引理 3.1 推广到教师-学生设定。它表明，在 `ρ`-SOSP 处，`W` 中与任务无关的正交分量会被强制缩小，从而使 `W` 收敛到教师方向张成的子空间（低秩结构）。

**模块化流程**

1.  **目标函数构造**：将问题（如神经网络风险、MAXCUT、JL嵌入）转化为形如 `f(W,b;θ)=E_x[g_θ(Wx+b)] + λ‖W‖_F^2` 的正则化风险函数。
2.  **Stein 引理应用**：建立 `∂f/∂W` 与 `E_x[∇²g_θ(Wx+b)]` 的联系，将关于 `W` 的一阶条件与关于 `b` 的二阶条件耦合。
3.  **ρ-SOSP 条件验证**：利用 ρ-SOSP 的梯度范数上界和 Hessian 负曲率下界，结合第 2 步的结果，导出 `‖W‖_F` 的上界。
4.  **优化算法 (Algorithm 1: PGD)**：运行扰动梯度下降（Perturbed Gradient Descent, PGD）等算法，以高概率在多项式时间内收敛到一个 `ρ`-SOSP。Theorem 4.2 保证，运行 Algorithm 1 可以在 `T = O(L/ρ^2 log^4(d))` 次迭代后，以高概率得到满足 `‖W_⊥‖_F < ε` 的解。

**关键发现与机制总结**

*   **训练偏置是关键**：该理论框架的有效性依赖于偏置 `b` 的可训练性。实验（Figure 1 vs Figure 2）清晰地展示了，当 `b` 被冻结时，需要非常大的正则化 `λ` 才能迫使权重归零；而训练 `b` 时，极小的 `λ` 即可实现。这是因为可训练的 `b` 使得关于 `b` 的 Hessian 条件（ρ-SOSP 的第二部分）能够被有效利用，从而通过 Stein 引理限制 `W` 的范数。
*   **弱正则化即可生效**：该框架仅要求 `λ > √(Kρ)/2`，这是一个非常弱的条件，远优于之前需要强正则化的方法（如 Mousavi-Hosseini et al., 2023）。这显著提升了理论的普适性。
*   **优化器无关**：该理论适用于任何能够收敛到 `ρ`-SOSP 的优化方法（如 PGD, Hessian descent, SGD），不局限于特定优化器，这进一步增强了其实用性。

## 实验与分析

### 核心结果：偏置可训练性是去随机化的关键开关

本文的实验设计直指理论核心：**训练偏置（bias）是去随机化生效的必要条件，而冻结偏置则会使理论退化为需要强正则化的旧结果。**

**单层NN玩具示例（ReLU³激活，一维输入）** 清晰地展示了这一因果机制。Figure 1 显示，当偏置被冻结（b=0）时，全局最小化器 w* 仅在正则化参数 λ 很大时才趋近于零；而 Figure 2 显示，当偏置可训练时，w* 在极小的 λ 下即可收敛到 0。这一对比验证了 Lemma 3.1 的核心洞察：训练偏置使得 Hessian 关于 b 的二阶导数能够通过 Stein 引理与关于 W 的一阶导数耦合，从而在 ρ-SOSP 条件下导出 W 的 Frobenius 范数上界 ‖W‖_F ≤ ρ/(2λ - √(Kρ))。当 ρ→0 时，W→0 无需大正则化。

**两层NN教师-学生设定（tanh单索引教师，d=2, h=1000）** 进一步验证了理论在更深网络中的适用性。Figure 3 显示，学生网络的第一层权重 W 收敛到教师方向张成的子空间（主成分子空间），即正交分量 W_⊥ 趋近于零。这与 Theorem 4.1 和 Theorem 4.2 一致：任何 ρ-SOSP 满足 ‖W_⊥‖_F ≤ ρ/(2λ - √(Kρ))，且 Algorithm 1（扰动梯度下降）可在多项式时间内以高概率得到 ‖W_⊥‖_F < ε 的解。该实验在极弱正则化下首次展示了任意深度网络的结构发现能力，突破了 Mousavi-Hosseini et al. (2023) 需要强正则化、两层网络、冻结偏置的限制。

### 跨领域应用：去随机化框架的通用性

**MAXCUT（随机图）**：Figure 4 显示，优化过程中割值随迭代次数单调上升，最终达到最优值 41，而 Goemans-Williamson 随机化算法仅约 36（提升约 14%）。Figure 5 显示，最大方差 σ² 随迭代稳步下降，表明随机性被优化过程消除。这一结果验证了去随机化引理在组合优化中的适用性：通过将随机化目标重写为形如 f(Vz+μ) = E_z[∑_{i<j} w̃_{i,j} Ĩ(v_i·z+μ_i, v_j·z+μ_j)] + λ‖V‖_F² 的正则化风险，任何 ρ-SOSP 都能迫使随机化参数（方差）趋于零。

**Johnson-Lindenstrauss嵌入（k=30, d=500, n=100）**：Figure 6 显示，优化后的最大失真从标准高斯随机投影的平均约 1 下降至接近零。Figure 7 显示，最大方差 σ² 收敛到零，意味着投影矩阵趋于确定性。这验证了 Theorem 4.2 在 JL 嵌入中的对应版本：通过优化失真函数 h(A; x_i) = |‖Ax_i‖₂² - 1| 的正则化期望，任何 ρ-SOSP 都能产生低方差的确定性投影。

### 消融实验与机制验证

**偏置可训练 vs. 冻结**：Figure 1 vs. Figure 2 的对比是本文最关键的消融。冻结偏置时，Hessian 关于 b 的二阶导数条件消失，Stein 引理无法将关于 W 的梯度与 b 的 Hessian 耦合，导致需要 λ 很大才能迫使 W 趋近于零。这直接解释了为何 Mousavi-Hosseini et al. (2023) 需要强正则化——他们的分析假设 b=0。

**优化器无关性**：本文未对不同优化器进行消融实验，但理论表明任何能收敛到 ρ-SOSP 的方法（如 PGD、Hessian descent、SGD）都适用。实验中使用 PGD（Algorithm 1），其迭代复杂度为 O(L/ρ² log⁴(d/δ))，与 Jin et al. (2017) 的标准结果一致。

### 实验局限性

所有实验均使用合成数据（高斯输入），未在真实图像/文本数据集上验证。MAXCUT 实验仅在一个随机图上进行，未报告多次运行的平均值和方差。JL 实验使用 n=100 个样本，k=30，d=500，规模较小。神经网络实验仅使用 d=2 的二维输入，未在高维设定下验证。这些局限性意味着本文的理论在真实大规模问题上的有效性仍需进一步验证。

## 方法谱系与知识库定位

本文提出的去随机化框架（Derandomization Framework）在方法谱系上直接回应了 Mousavi-Hosseini 等人（2023）工作的核心瓶颈。该基线方法在证明神经网络第一层权重收敛到低秩结构时，需要同时满足强正则化、网络深度限制为两层、偏置冻结为零以及优化器限定为 SGD 等严格假设。本文的核心方法论贡献在于，通过将解概念从一阶驻点（FOSP）提升为 ρ-二阶驻点（ρ-SOSP），并利用 Stein 引理建立偏置二阶导数与权重一阶梯度的代数联系，在极弱正则化条件（仅需 λ > √(Kρ)/2）下即导出第一层权重 Frobenius 范数的上界 ‖W‖_F ≤ ρ/(2λ - √(Kρ))（Lemma 3.1）。这一“去随机化引理”表明，二阶驻点条件本身就能迫使权重趋于零，无需强正则化或特定优化器——即因果机制从“通过大 λ 强制压缩”转变为“通过二阶驻点条件自动诱导低秩”。

该方法在五个关键设计维度上改变了基线假设：（1）正则化强度 λ 从“需要较大值”放松为“任意小值，可由 ρ 控制”；（2）偏置 b 从“冻结为零”变为“可训练”，而这是去随机化生效的必要条件（Figure 1 vs Figure 2 对比清晰展示了这一因果开关）；（3）解概念从 FOSP 升级为 ρ-SOSP，这允许利用 Hessian 信息而非仅梯度信息；（4）网络架构从“仅两层”扩展为“任意大小和深度”；（5）优化器从“仅 SGD”泛化为“任何能收敛到 ρ-SOSP 的方法（如 PGD、Hessian descent、SGD）”。

在适用边界方面，该框架的核心假设是所有理论结果依赖于输入分布为标准高斯分布（x ∼ N(0, I_d)），且目标函数需满足 L-光滑和 K-Hessian Lipschitz 条件。实验验证覆盖了三个应用领域：神经网络结构发现（教师-学生设定，d=2, h=1000）、MAXCUT 组合优化（随机图，最优割值 41 vs 基线约 36）、Johnson-Lindenstrauss 确定性嵌入（k=30, d=500, n=100），但所有实验均使用合成数据，未在真实图像/文本数据集上验证。MAXCUT 实验仅在一个随机图上进行，未报告多次运行的统计结果；JL 实验和神经网络实验的规模均较小（n=100, d=2）。这些限制意味着该框架在真实大规模高维问题上的有效性仍需进一步验证。

当前存在的开放问题包括：（1）如何将去随机化框架扩展到非高斯输入分布（如次高斯分布或混合分布）？（2）能否将结构发现与泛化保证结合，建立端到端的学习理论？（3）对于更复杂的网络结构（如卷积、Transformer），去随机化引理是否仍然成立？（4）在有限样本（经验风险）而非总体风险下，ρ-SOSP 条件是否仍能保证低秩结构？（5）去随机化框架能否应用于其他随机算法（如随机特征方法、随机优化）的去随机化？（6）MAXCUT 实验中，优化方法是否总能收敛到全局最优割，还是可能陷入局部最优？需要指出的是，这些开放问题中部分（如非高斯分布扩展、泛化保证）已在论文结论部分被明确提及为未来工作方向，而其他问题（如复杂网络结构适用性、有限样本分析）则来自对方法逻辑的推演。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Derandomization_Framework_for_Structure_Discovery_Applications_in_Neural_Networks_and_Beyond.pdf

![[paperPDFs/ICLR_2026/A_Derandomization_Framework_for_Structure_Discovery_Applications_in_Neural_Networks_and_Beyond.pdf]]
