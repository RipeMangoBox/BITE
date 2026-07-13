---
title: "A Statistical Learning Perspective on Semi-dual Adversarial Neural Optimal Transport Solvers"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Statistical_Learning_Perspective_on_Semi_dual_Adversarial_Neural_Optimal_Transport_Solvers.pdf
project_link: null
code_link: https://github.com/milenagazdieva/StatOT
aliases:
- MQOS
- SLPSDANOTS
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "通过将泛化误差分解为估计误差（由经验分布代替真实分布引起）和近似误差（由受限函数类引起），并利用 Rademacher 复杂度分别界定这两项。"
primary_logic: "对于二次代价的 minimax OT 求解器，泛化误差可被估计误差与近似误差之和上界控制；估计误差仅依赖于神经网络函数类的 Rademacher 复杂度，近似误差可通过选择足够宽的网络任意减小；因此，通过足够多的样本和适当的网络类，泛化误差可任意小。"
claims:
- "泛化误差可被估计误差与近似误差之和上界控制"
- "估计误差上界由 Rademacher 复杂度给出：E^E ≤ 8 R_{p,N}(H) + 8 R_{q,M}(F)"
- "内层近似误差可通过选择适当的神经网络类 T 任意小"
- "外层近似误差在最优势函数 β-强凸时可任意小"
---

# A Statistical Learning Perspective on Semi-dual Adversarial Neural Optimal Transport Solvers

> [!tip] 核心洞察
> 对于二次代价的 minimax OT 求解器，泛化误差可被估计误差与近似误差之和上界控制；估计误差仅依赖于神经网络函数类的 Rademacher 复杂度，近似误差可通过选择足够宽的网络任意减小；因此，通过足够多的样本和适当的网络类，泛化误差可任意小。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 半对偶对抗神经最优传输求解器的统计学习视角 |
| 英文题名 | A Statistical Learning Perspective on Semi-dual Adversarial Neural Optimal Transport Solvers |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=FJTdyG8jeJ) · [GitHub](https://github.com/milenagazdieva/StatOT) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Minimax Quadratic OT Solver (半对偶对抗神经最优传输求解器) |
| Dataset | 合成高斯分布 (D=2, 4, 8, 16, 32, 64, 128) |

> [!tip] 效果简介
> - 合成高斯分布 (D=2,4,8,16,32,64,128) 上，||T̂ - T*||_{L^2(P)}^2 为 Minimax OT solver，对比 Constant, Barycenter translation, Linear estimators，变化 OT solver 的估计误差显著低于所有基线。
> - 合成高斯分布 (D=2,4,8,16,32,64,128) 上，log10(||T̂ - T*||_{L^2(P)}^2) vs log10(N,M) 为 Minimax OT solver，对比 理论斜率 -0.5，变化 实际收敛斜率约 -0.5 或更陡。

## 概要

该研究为基于 minimax 半对偶形式的对抗神经最优传输求解器建立了首个统计学习理论框架。其核心瓶颈在于，现有方法虽在实践中有效，但缺乏对泛化误差——即真实最优传输映射 $T^*$ 与基于有限样本学习的映射 $\widehat{T}^R$ 之间 $L^2(p)$ 距离的期望上界——的定量刻画。针对二次代价（Wasserstein-2）的 minimax 求解器，本文的核心洞见在于，该误差可被分解为**估计误差**（由经验分布替代真实分布引起）与**近似误差**（由受限的神经网络函数类引起）之和，并分别受控于神经网络类的 Rademacher 复杂度与网络的逼近能力。

方法上，该求解器同时参数化一个对偶势函数 $\varphi_\theta$（采用输入凸神经网络 ICNN 并附加二次项以保证 $\beta$-强凸性）和一个原始传输映射 $T_\omega$（采用多层感知机 MLP），通过求解经验 minimax 优化问题 $\min_\theta \max_\omega \widehat{\mathcal{L}}(\varphi_\theta, T_\omega)$ 来学习映射。与仅优化势函数的非 minimax 方法相比，该框架直接学习传输映射，并允许进行统计学习分析。

主要理论结果（Theorem 4.9）表明，泛化误差的上界可写为：

$$
\mathbb{E}_{X,Y} \left\| T^* - \widehat{T}^R \right\|_{L^2(p)}^2 \leq \varepsilon + \frac{32}{\beta} \left( \mathcal{R}_{p,N}(\mathcal{H}) + \mathcal{R}_{q,M}(\mathcal{F}) \right),
$$

其中 $\mathcal{R}_{p,N}(\mathcal{H})$ 和 $\mathcal{R}_{q,M}(\mathcal{F})$ 分别为传输映射与势函数函数类的 Rademacher 复杂度。对于特定的神经网络类，该上界可达到 $O(1/\sqrt{N}) + O(1/\sqrt{M})$ 的收敛率。实验在合成高斯分布上验证了该理论：估计误差的收敛斜率接近理论预测的 -0.5，且近似误差随网络宽度增加而减小。然而，该分析严格限于二次代价与 $\beta$-强凸势函数假设，且实验仅在低维合成数据上进行，未在高维真实数据上验证。



最优传输（Optimal Transport, OT）问题的核心是寻找一个映射 $T$，在最小化传输代价 $c(x, T(x))$ 的同时，将源分布 $p$ 推送到目标分布 $q$。对于二次代价 $c(x, y) = \frac{1}{2}\|x - y\|_2^2$，该问题等价于求解 Wasserstein-2 距离，并可通过半对偶形式转化为一个关于 Kantorovich 势函数 $\varphi$ 的优化问题。近年来，基于神经网络的对抗式求解器通过引入一个额外的传输映射 $T$，将问题重写为 minimax 形式 $\min_{\varphi} \max_{T} \mathcal{L}(\varphi, T)$，从而同时学习势函数和传输映射。这类方法在实践中取得了成功，但其理论基础——特别是统计学习保证——却严重滞后。

现有工作的主要缺口在于：**缺乏对 minimax OT 求解器泛化误差的理论刻画**。传统的非 minimax 方法仅分析对偶间隙，而现有对抗式求解器的分析也仅停留在经验性能层面。具体而言，当使用有限样本 $\{x_n\}_{n=1}^N \sim p$ 和 $\{y_m\}_{m=1}^M \sim q$ 以及受限的神经网络函数类 $\mathcal{F}$（势函数）和 $\mathcal{T}$（传输映射）时，学习到的映射 $\widehat{T}$ 与真实最优传输映射 $T^*$ 之间的 $L^2(p)$ 误差——即泛化误差 $\mathbb{E}_{X,Y} \|\widehat{T} - T^*\|_{L^2(p)}^2$——的上界是未知的。这一理论空白使得我们无法回答一个基本问题：需要多少样本、多宽的网络，才能保证求解器以可接受的精度逼近真实 OT 映射？

本文的核心动机正是填补这一空白。作者从统计学习理论出发，将泛化误差系统地分解为两个来源：**估计误差**（因使用经验分布 $\hat{p}, \hat{q}$ 代替真实分布 $p, q$ 引起）和**近似误差**（因使用受限的神经网络函数类 $\mathcal{F}, \mathcal{T}$ 代替所有可能函数引起）。这一分解（Theorem 4.1）为后续分析提供了因果框架：要控制泛化误差，只需分别控制这两项。

进一步，作者利用 Rademacher 复杂度 $\mathcal{R}_{p,N}(\mathcal{H})$ 和 $\mathcal{R}_{q,M}(\mathcal{F})$ 给出了估计误差的上界（Theorem 4.2）：$\mathcal{E}^{E} \leq 8\mathcal{R}_{p,N}(\mathcal{H}) + 8\mathcal{R}_{q,M}(\mathcal{F})$，其中 $\mathcal{H}$ 是与传输映射相关的函数类。对于近似误差，作者证明通过选择足够宽的神经网络，内层近似误差（Theorem 4.3）和外层近似误差（Theorem 4.6，在最优势函数 $\varphi^*$ 为 $\beta$-强凸的假设下）均可任意小。最终，泛化误差被上界控制为 $\varepsilon + O(1/\sqrt{N}) + O(1/\sqrt{M})$（Theorem 4.9），其中 $\varepsilon$ 为可任意小的近似误差项，而 $O(1/\sqrt{N})$ 和 $O(1/\sqrt{M})$ 的收敛率来自神经网络类的 Rademacher 复杂度。

这一理论框架的核心洞见在于：**minimax OT 求解器的统计行为完全由神经网络函数类的容量（Rademacher 复杂度）和逼近能力（通用逼近定理）决定**，而 minimax 结构本身并不带来额外的统计困难。这为理解对抗式 OT 求解器的样本效率和网络设计提供了第一个严格的理论基础。



## 核心方法与创新机理

本文的核心创新在于为基于神经网络的 minimax 半对偶最优传输求解器提供了首个统计学习理论保证，填补了该领域缺乏泛化误差分析的空白。其关键突破在于将泛化误差（真实 OT 映射与近似映射之间的 L2 距离）系统地分解为可分别控制的估计误差与近似误差，并利用 Rademacher 复杂度和神经网络逼近理论给出了具体上界。

**优化目标的改变（Changed Slot）**：与仅优化势函数 φ 的标准半对偶损失不同，本文采用 minimax 半对偶损失（公式 6），同时优化势函数 φ 和传输映射 T。这一改变通过交换定理（Rockafellar, 2006, Theorem 3A）导出，使得求解器能同时学习对偶势和原始传输映射，为后续的误差分解提供了统一的优化框架。

**理论分析框架的建立（Changed Slot）**：现有 minimax OT 求解器仅分析对偶间隙，缺乏统计收敛率。本文首次建立了泛化误差的统计学习上界，核心洞察在于：对于二次代价的 minimax OT 求解器，泛化误差可被估计误差（由经验分布代替真实分布引起）与近似误差（由受限函数类引起）之和上界控制。具体而言：
- **误差分解**（Theorem 4.1）：泛化误差上界为 $(4/\beta)$ 乘以估计误差与近似误差的加权和。
- **估计误差上界**（Theorem 4.2）：总估计误差 $\mathcal{E}^{E} \leq 8\mathcal{R}_{p,N}(\mathcal{H}) + 8\mathcal{R}_{q,M}(\mathcal{F})$，仅依赖于传输映射类 $\mathcal{H}$ 和势函数类 $\mathcal{F}$ 的 Rademacher 复杂度，与数据维度无关。
- **近似误差可任意小**（Theorem 4.3 & 4.6）：通过选择足够宽的神经网络类，内层近似误差（映射类）和外层近似误差（势函数类，在最优势函数 β-强凸假设下）均可小于任意 $\varepsilon$。

**势函数参数化的改进（Changed Slot）**：为保证理论分析所需的 β-强凸性，势函数被参数化为 ICNN（输入凸神经网络）加上二次正则项 $\beta\|\cdot\|_2^2/2$，即 $\mathcal{F} = \{\varphi + \beta \|\cdot\|_2^2 / 2, \varphi \in \mathcal{F}_{icnn}\}$。

**核心定理的收敛率**：综合上述结果，泛化误差的最终上界（Theorem 4.9）为 $\varepsilon + (32/\beta)(\mathcal{R}_{p,N}(\mathcal{H}) + \mathcal{R}_{q,M}(\mathcal{F}))$。对于特定神经网络类，该上界可达到 $O(1/\sqrt{N}) + O(1/\sqrt{M})$ 的收敛率，与实验观察到的 log-log 尺度下斜率约 -0.5 的收敛行为一致（Figure 3）。

**实验验证**：在合成高斯分布上的实验表明：（1）估计误差的收敛率与理论预测的 $O(1/\sqrt{N})$ 吻合；（2）随着神经网络宽度增加，近似误差减小，当势函数架构与基准构造一致时（max H_φ=64），近似误差接近零（Figure 4）；（3）极浅网络（max H_φ=4,16）会导致近似误差崩溃，产生不良解（Figure 7）。这些结果验证了理论分析的合理性，但需注意实验仅在合成数据上进行。



该论文提出的 Minimax Quadratic OT Solver 是一个端到端的对抗式神经最优传输求解器，其整体 pipeline 围绕一个 **minimax 半对偶优化问题**构建。核心思想是同时学习两个神经网络：一个作为 **Kantorovich 势函数** $\varphi_\theta$，另一个作为 **传输映射** $T_\omega$，通过对抗训练逼近真实的 Monge 最优传输映射。

**模块关系与输入输出流：**

1.  **输入**：来自源分布 $p$ 的经验样本 $\{x_n\}_{n=1}^N$ 和目标分布 $q$ 的经验样本 $\{y_m\}_{m=1}^M$。
2.  **势函数模块** ($\varphi_\theta$)：采用 **ICNN（输入凸神经网络）** 架构，并附加一个 $\frac{\beta}{2}\|\cdot\|_2^2$ 的二次跳跃连接，以保证函数是 $\beta$-强凸的。该模块接收来自传输映射的输出 $T_\omega(x_n)$ 或目标样本 $y_m$，输出标量势函数值。
3.  **传输映射模块** ($T_\omega$)：采用 **MLP（多层感知机）** 架构，使用 ReLU 激活函数。该模块接收源样本 $x_n$，输出传输后的点 $T_\omega(x_n)$。
4.  **经验 Minimax 优化**：这是 pipeline 的核心循环。基于经验样本，求解以下对抗优化问题：
    
$$
\min_{\theta \in \Theta} \max_{\omega \in \Omega} \sum_{n=1}^N \frac{\langle x_n, T_\omega(x_n) \rangle - \varphi_\theta(T_\omega(x_n))}{N} + \sum_{m=1}^M \frac{\varphi_\theta(y_m)}{M}
$$

    该目标函数直接对应于二次代价函数下的半对偶 OT 问题的经验形式。优化过程交替更新 $\varphi_\theta$ 和 $T_\omega$，使得传输映射 $T_\omega$ 在对抗中学习到最优的映射。

**与现有方法的区别：**

- **优化目标**：与仅优化势函数 $\varphi$ 的传统半对偶方法不同，该论文的 **minimax 半对偶损失**同时优化 $\varphi$ 和 $T$，直接学习原始传输映射。
- **理论分析框架**：现有工作多分析对偶间隙，而该论文建立了**泛化误差的统计学习上界**。其核心因果机制是将泛化误差分解为：
    - **估计误差**：由经验分布 $\hat{p}, \hat{q}$ 代替真实分布 $p, q$ 引起。该误差的上界由神经网络函数类 $\mathcal{H}$ 和 $\mathcal{F}$ 的 **Rademacher 复杂度**决定。
    - **近似误差**：由受限的神经网络函数类（如 ICNN、MLP）无法精确表示最优解引起。该论文证明，通过选择足够宽的网络，近似误差可以任意小。
- **势函数参数化**：为保证理论分析中的强凸性条件，该论文使用 **ICNN + $\frac{\beta}{2}\|\cdot\|_2^2$** 的参数化方式，而非通用的 ICNN 或普通神经网络。

**整体流程**：源数据 $x$ 和目标数据 $y$ 输入系统，通过 minimax 对抗训练，最终输出一个训练好的传输映射 $T_\omega$，该映射的泛化误差被理论控制在 $O(1/\sqrt{N}) + O(1/\sqrt{M})$ 的收敛率内。实验在合成高斯分布上验证了该框架的有效性，但需注意其理论假设（如 $\beta$-强凸性）在实际应用中可能不成立，且实验未在真实高维数据集上验证。



### 问题设定与核心目标

本文研究二次代价函数 $c(x,y) = \frac{1}{2}\|x-y\|_2^2$ 下的 Monge 最优传输问题。真实 OT 映射 $T^*$ 由 Monge 问题定义：

$$
\operatorname{Cost}_c(p,q) \stackrel{\mathrm{def}}{=} \inf_{T_\# p = q} \int_{\mathcal X} c(x, T(x)) p(x) dx
$$

其半对偶形式为 Wasserstein-2 距离的表达：

$$
\operatorname{Cost}_{\frac{1}{2}\lVert 1 - \cdot \rVert_2^2}(p,q) = \int_{\chi} \frac{\lVert x \rVert_2^2}{2} p(x) dx + \int_{\mathcal{Y}} \frac{\lVert y \rVert_2^2}{2} q(y) dy - \min_{\varphi \in \mathcal{C}(\mathcal{Y})} \Big\{ \int_{\mathcal{X}} \overline{\varphi}(x) p(x) dx + \int_{\mathcal{Y}} \varphi(y) q(y) dy \Big\}
$$

其中 $\overline{\varphi}$ 是 $\varphi$ 的 $c$-变换。该文的核心创新在于将标准半对偶形式转化为 minimax 形式，同时优化势函数 $\varphi$ 和传输映射 $T$：

$$
\min_{\varphi} \max_{T} \left\{ \int_{\mathcal{L}} [\langle x, T(x) \rangle - \varphi(T(x))] p(x) dx + \int_{\mathcal{L}} \varphi(y) q(y) dy \right\} \stackrel{\mathrm{def}}{=} \min_{\varphi} \max_{T} \mathcal{L}(\varphi, T)
$$

在实际求解中，用经验分布 $\hat{p}, \hat{q}$ 替代真实分布，并用神经网络参数化 $\varphi_\theta$ 和 $T_\omega$，得到经验 minimax 目标：

$$
\min_{\theta \in \Theta} \max_{\omega \in \Omega} \sum_{n=1}^N \frac{\langle x_n, T_\omega(x_n) \rangle - \varphi_\theta(T_\omega(x_n))}{N} + \sum_{m=1}^M \frac{\varphi_\theta(y_m)}{M} \stackrel{\mathrm{def}}{=} \min_{\theta \in \Theta} \max_{\omega \in \Omega} \widehat{\mathcal{L}}(\varphi_\theta, T_\omega)
$$

### 误差分解定理

泛化误差定义为真实 OT 映射与经验 OT 映射之间的期望 $L^2$ 距离：$\mathbb{E}_{X,Y} \|T^* - \widehat{T}^R\|_{L^2(p)}^2$。该文的核心理论贡献是将其分解为估计误差和近似误差之和（Theorem 4.1）：

$$
\underset{X,Y}{\mathbb{E}} \left\| \widehat{T}^R - T^* \right\|_{L^2(p)}^2 \leq \frac{4}{\beta} \left( \mathcal{E}_{In}^E(\mathcal{F}, \mathcal{T}, N, M) + 3 \mathcal{E}_{In}^A(\mathcal{F}, \mathcal{T}) + \mathcal{E}_{Out}^E(\mathcal{F}, \mathcal{T}, N, M) + \mathcal{E}_{Out}^A(\mathcal{F}) \right)
$$

其中：
- $\mathcal{E}_{In}^E$ 和 $\mathcal{E}_{Out}^E$ 是估计误差，由经验分布代替真实分布引起；
- $\mathcal{E}_{In}^A$ 和 $\mathcal{E}_{Out}^A$ 是近似误差，由受限函数类 $\mathcal{F}, \mathcal{T}$ 无法表示真实最优解引起；
- $\beta$ 是势函数类的强凸性参数。

该分解的关键在于将传输映射误差转化为对偶间隙（duality gap）的控制，即 Theorem A.2：

$$
\|\widehat{T}^R - T^*\|_{L^2(p)}^2 \leq \frac{4}{\beta} \left( \mathcal{E}_1(\widehat{\varphi}^R, \widehat{T}^R) + \mathcal{E}_2(\widehat{\varphi}^R) \right)
$$

其中内层误差 $\mathcal{E}_1(\widehat{\varphi}^R, \widehat{T}^R) = \max_T \mathcal{L}(\widehat{\varphi}^R, T) - \mathcal{L}(\widehat{\varphi}^R, \widehat{T}^R)$ 衡量给定势函数下传输映射的次优性，外层误差 $\mathcal{E}_2(\widehat{\varphi}^R) = \max_T \mathcal{L}(\widehat{\varphi}^R, T) - \min_\varphi \max_T \mathcal{L}(\varphi, T)$ 衡量势函数的次优性。

### 估计误差的 Rademacher 复杂度上界

Theorem 4.2 给出了估计误差的 Rademacher 复杂度上界：

$$
\mathcal{E}^{E} \leq 8\mathcal{R}_{p,N}(\mathcal{H}) + 8\mathcal{R}_{q,M}(\mathcal{F})
$$

其中 $\mathcal{R}_{p,N}(\mathcal{H})$ 和 $\mathcal{R}_{q,M}(\mathcal{F})$ 分别是函数类 $\mathcal{H}$ 和 $\mathcal{F}$ 关于分布 $p, q$ 的经验 Rademacher 复杂度。该上界通过 Lemma A.3 的表示性（representativeness）引理建立：$\sup_{\varphi\in\mathcal{F}} \sup_{T\in\mathcal{T}} |\mathcal{L}(\varphi,T) - \widehat{\mathcal{L}}(\varphi,T)| \leq \mathrm{Rep}_{\mathcal{H},p}(X) + \mathrm{Rep}_{\mathcal{F},q}(Y)$，然后利用期望表示性与 Rademacher 复杂度的关系 $\mathbb{E} \mathrm{Rep}_{\mathcal{F},q}(Y) \leq 2\mathcal{R}_{q,M}(\mathcal{F})$ 得到最终上界。

### 近似误差的可任意小性

Theorem 4.3 和 Theorem 4.6 分别证明了内层和外层近似误差可以通过选择适当的神经网络类任意小：

- **内层近似误差**（Theorem 4.3）：对任意 $\varepsilon > 0$，存在神经网络类 $\mathcal{T}_{ub} = \mathcal{T}(\varepsilon, \mathcal{F})$，使得 $\mathcal{E}_{In}^A(\mathcal{F}, \mathcal{T}) < \varepsilon$。证明依赖于 Lemma A.4 和 Lemma A.6，后者建立了最优映射差分的 $L^1(p)$ 范数与势函数 Lipschitz 范数的关系：$\|T_{\varphi_1} - T_{\varphi_2}\|_{L^1(p)} \leq \frac{1}{\beta} \|\varphi_1 - \varphi_2\|_{Lip}$。

- **外层近似误差**（Theorem 4.6）：假设最优势函数 $\varphi^*$ 是 $\beta$-强凸的，则对任意 $\varepsilon > 0$，存在神经网络类 $\mathcal{F} = \mathcal{F}(\beta, \varepsilon)$，使得 $\mathcal{L}(\varphi_L^\beta) - \mathcal{L}(\varphi^*) < \varepsilon$。

### 泛化误差最终上界与收敛率

Theorem 4.9 综合上述结果，得到泛化误差的最终上界：

$$
\mathbb{E}_{x,Y} \left\| T^* - \widehat{T}^R \right\|_{L_2(p)}^2 \leq \varepsilon + \frac{32}{\beta} \left( \mathcal{R}_{p,N}(\mathcal{H}) + \mathcal{R}_{q,M}(\mathcal{F}) \right)
$$

对于特定神经网络类（如 ReLU 激活的 MLP），Rademacher 复杂度以 $O(1/\sqrt{N})$ 和 $O(1/\sqrt{M})$ 速率衰减，因此泛化误差收敛率为：

$$
\mathbb{E}_{x,Y} \left\| T^* - \widehat{T}^R \right\|_{L_2(p)}^2 \leq \varepsilon + O\left(\frac{1}{\sqrt{N}}\right) + O\left(\frac{1}{\sqrt{M}}\right)
$$

### 核心假设与局限性

上述理论框架依赖两个关键假设：二次代价函数和势函数类的 $\beta$-强凸性。势函数采用 ICNN + $\beta\|\cdot\|_2^2/2$ 的参数化形式以保证强凸性。该分析未考虑优化误差（非凸优化、鞍点问题）的影响，也未提供泛化误差的下界。



## 实验与关键发现

### 主结果：合成高斯分布上的估计误差与收敛率

本文在合成高斯分布上验证了所提 minimax OT 求解器的统计收敛性，实验设置与理论分析一致：源分布 $p$ 和目标分布 $q$ 均为零均值高斯分布，协方差矩阵分别为 $\Sigma_p = I_D$ 和 $\Sigma_q = \text{diag}([0.5, 1, 1.5, \dots])$，维度 $D \in \{2, 4, 8, 16, 32, 64, 128\}$。核心指标为估计的传输映射 $\widehat{T}$ 与真实 OT 映射 $T^*$ 之间的平方 $L^2(p)$ 距离 $\|\widehat{T} - T^*\|_{L^2(p)}^2$。

**收敛率（Figure 3）：** 在 log-log 尺度下，估计误差随样本量 $N, M$（实验中取 $N = M$）的增加而线性下降，实际斜率约为 $-0.5$ 或更陡。这与 Theorem 4.9 导出的理论上界 $O(1/\sqrt{N}) + O(1/\sqrt{M})$ 一致，表明所提求解器的经验收敛速率达到了统计学习理论预期的 $1/\sqrt{N}$ 量级。

**与基线对比（Figure 5）：** 将 minimax OT 求解器与三个解析基线进行比较：
- **Constant estimator**：常数映射 $T(x) = \mu_q$
- **Barycenter translation estimator**：平移映射 $T(x) = x + \mu_q - \mu_p$
- **Linear estimator**：线性映射 $T(x) = \Sigma_p^{-1/2} (\Sigma_p^{1/2} \Sigma_q \Sigma_p^{1/2})^{1/2} \Sigma_p^{-1/2} (x - \mu_p) + \mu_q$

在所有维度（$D=2,4,8,16,32,64,128$）和有限样本量下，minimax OT 求解器的估计误差均显著低于所有基线。这一结果验证了理论分析的核心结论：通过 minimax 联合优化势函数 $\varphi$ 和传输映射 $T$，可以同时控制估计误差和近似误差，从而获得更精确的 OT 映射估计。

### 消融实验：神经网络宽度对近似误差的影响

**Figure 4** 展示了浅层神经网络架构下近似误差随网络宽度的变化。实验中固定传输映射网络宽度 $H_T = 64$，变化势函数网络宽度 $H_\varphi \in \{4, 16, 64\}$。关键发现：
- 当势函数网络宽度 $H_\varphi = 64$（与基准构造一致）时，近似误差接近零。
- 随着网络宽度减小（$H_\varphi = 16, 4$），近似误差显著增大。
- 极浅网络（$H_\varphi = 4$）导致近似误差崩溃，产生不良解。

该结果直接支持 Theorem 4.3 和 Theorem 4.6 的理论结论：通过选择足够宽（即足够表达能力强）的神经网络类，近似误差可以任意小。反之，过窄的网络无法充分逼近最优势函数 $\varphi^*$，导致近似误差失控。

**Figure 7** 进一步可视化了浅层势函数导致解崩溃的现象。在 $D=2$、$H_T=8$ 的设置下，当 $H_\varphi$ 过小时，学习到的传输映射出现严重的结构性扭曲（如映射到非目标分布区域），而非平滑地逼近真实 OT 映射。这表明势函数的表达能力是 minimax OT 求解器成功的关键瓶颈。

### 失败模式与实验局限性

**失败模式：** 最突出的失败模式是势函数网络宽度不足导致的解崩溃。当 $H_\varphi$ 过小时，内层最大化问题无法被充分优化，导致估计的传输映射严重偏离真实 OT 映射。这一现象与理论分析一致：近似误差项 $\mathcal{E}^A_{In}(\mathcal{F}, \mathcal{T})$ 依赖于函数类 $\mathcal{F}$ 的表达能力，过窄的网络无法满足 $\beta$-强凸函数的逼近需求。

**实验局限性：**
1. **合成数据局限：** 所有实验仅在合成高斯分布上进行，未在真实高维数据集（如图像、生物数据）上验证。高斯分布的简单结构可能掩盖了实际应用中复杂的非凸优化问题。
2. **优化细节：** 所有实验使用 Adam 优化器，学习率固定为 $1\times10^{-3}$，未进行超参数调优。优化误差（如鞍点问题、非凸收敛）对泛化误差的影响未被量化。
3. **统计量有限：** 每个实验仅运行 3 次随机种子，统计量有限，无法精确刻画误差的方差。
4. **代价函数局限：** 实验仅针对二次代价（Wasserstein-2）进行，理论结果和实验验证均未推广到一般代价函数。



## 定位与知识库关联

### 与基线方法的关系

本文的核心贡献在于为**minimax 半对偶神经 OT 求解器**提供了首个统计学习理论保证。该求解器在优化目标上区别于传统的非 minimax 半对偶方法（仅优化势函数 φ），而是同时优化势函数 φ 和传输映射 T，形成 `min_φ max_T L(φ,T)` 的对抗式结构。这一改变使得模型能够直接学习可用的传输映射，而非仅通过对偶间隙间接推断。

在实验对比中，本文选取了三类经典解析基线作为下界参考：常数映射 `T = μ_q`、平移映射 `T(x) = x + μ_q - μ_p` 以及线性映射（基于协方差矩阵的显式解）。这些基线代表了在**无统计学习理论指导**下，仅利用样本矩信息所能达到的性能天花板。实验结果表明（Figure 5），所提 minimax OT 求解器在所有维度（D=2,4,8,16,32,64,128）上的估计误差均显著低于所有基线，这验证了神经网络参数化在捕捉分布间非线性传输结构上的优势。

### 理论框架的定位与适用边界

本文的理论框架建立在三个核心定理之上，形成了完整的误差分析链条：

1. **误差分解定理（Theorem 4.1）**：将泛化误差 `E_{X,Y} ||T̂^R - T*||_{L^2(p)}^2` 分解为估计误差（由经验分布代替真实分布引起）和近似误差（由受限函数类引起）之和。这一分解是统计学习理论的标准范式，但其在 minimax OT 语境下的具体形式——需要同时处理内层（max_T）和外层（min_φ）的误差——是本文的独特贡献。

2. **Rademacher 复杂度上界（Theorem 4.2）**：证明总估计误差 `E^E ≤ 8 R_{p,N}(H) + 8 R_{q,M}(F)`，其中 H 和 F 分别对应传输映射和势函数的函数类。这意味着估计误差仅依赖于神经网络类的复杂度，而不依赖于具体的数据分布或优化过程。

3. **逼近误差可控性（Theorem 4.3 & 4.6）**：证明通过选择足够宽的神经网络类，内层和外层近似误差均可任意小。这为神经网络架构选择提供了理论依据——宽度是关键瓶颈。

**适用边界**：该理论框架严格限定于二次代价（Wasserstein-2）的 minimax OT 求解器，且假设最优势函数 φ* 是 β-强凸的。这一假设在实际中可能不成立（如分布具有多模态或非凸支撑集时），是理论适用的核心约束。

### 局限性与开放问题

**已知局限**：
- 理论分析未考虑优化误差（非凸优化、鞍点问题）的影响，而实际训练中 minimax 优化可能陷入不良局部均衡。
- 未提供泛化误差的下界，因此无法判断所提上界的紧性。
- 实验仅在合成高斯分布上进行，未在真实高维数据集（如图像、生物数据）上验证，其结论在复杂分布上的泛化能力存疑。
- 实验中观察到极浅网络（max H_φ=4,16）导致近似误差崩溃（Figure 7），但理论分析未能解释这一相变现象的临界点。

**开放问题**：
1. **代价函数泛化**：如何将统计学习分析推广到一般代价函数（如余弦代价、一般凸代价）？这需要重新建立误差分解中 β-强凸性的对应条件。
2. **优化误差纳入**：非凸优化和鞍点问题对泛化误差的具体影响是什么？能否将其作为独立项纳入现有理论框架？
3. **下界与紧性**：能否建立泛化误差的下界，以刻画所提上界的紧性，从而指导实际中的样本量选择？
4. **架构选择指南**：如何为 minimax OT 求解器提供实用的神经网络架构选择指南（如宽度、深度的推荐范围）？当前理论仅给出存在性保证，缺乏可操作的指导。
5. **扩展到其他 OT 变体**：本文的统计学习分析能否扩展到熵正则化 OT、非平衡 OT、动态 OT 等变体？这些变体在生成建模和计算生物学中具有更广泛的应用。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Statistical_Learning_Perspective_on_Semi_dual_Adversarial_Neural_Optimal_Transport_Solvers.pdf

![[paperPDFs/ICLR_2026/A_Statistical_Learning_Perspective_on_Semi_dual_Adversarial_Neural_Optimal_Transport_Solvers.pdf]]
