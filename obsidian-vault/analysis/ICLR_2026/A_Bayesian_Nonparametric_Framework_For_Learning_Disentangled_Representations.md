---
title: "A Bayesian Nonparametric Framework For Learning Disentangled Representations"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Bayesian_Nonparametric_Framework_For_Learning_Disentangled_Representations.pdf
aliases:
- BQBQLA
- BNFLDR
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "采用贝叶斯非参数层次混合先验（Dirichlet Process prior）替代固定容量的离散先验，同时保持因子化的独立结构，并通过嵌套变分推断实现自适应容量扩展。"
primary_logic: "非参数先验的无限容量与因子化结构相结合，使得模型能够在保持可辨识性保证的前提下，根据数据复杂度自适应地扩展每个因子的表示容量，从而避免固定码本带来的容量上限问题，同时通过早期训练阶段的稀疏码本隐式正则化促进解耦。"
claims:
- "Bayes-QLAE在3DShapes数据集上InfoM达到0.91±0.03，InfoC达到0.61±0.02，D达到0.84±0.03，显著优于所有基线方法。"
- "Bayes-QLAE在MPI3D数据集上InfoM达到0.60±0.03，InfoC达到0.56±0.03，优于或持平于所有基线方法。"
- "嵌套变分推断（Bayes-QLAE）在所有解耦指标上一致优于截断变分推断（T-QLAE）和平均场变分推断（MF-QLAE）等消融变体。"
- "潜变量遍历可视化显示，每个因子被单个潜变量独立编码，且存在不活跃的潜变量维度，表明模型学习了紧凑且模块化的表示。"
---

# A Bayesian Nonparametric Framework For Learning Disentangled Representations

> [!tip] 核心洞察
> 非参数先验的无限容量与因子化结构相结合，使得模型能够在保持可辨识性保证的前提下，根据数据复杂度自适应地扩展每个因子的表示容量，从而避免固定码本带来的容量上限问题，同时通过早期训练阶段的稀疏码本隐式正则化促进解耦。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一种用于学习解耦表示的非参数贝叶斯框架 |
| 英文题名 | A Bayesian Nonparametric Framework For Learning Disentangled Representations |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=GVOLiaENgU) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Bayes-QLAE (Bayesian Quantized Latent Autoencoder) |
| Dataset | 3DShapes, MPI3D |

> [!tip] 效果简介
> - 3DShapes 上，InfoM 为 0.91 ± 0.03，对比 β-VAE: 0.62, FactorVAE: 0.68, β-TCVAE: 0.70, VQ-VAE: 0.55, QLAE: 0.82, Tripod: 0.85，变化 +0.06 over Tripod。
> - 3DShapes 上，InfoC 为 0.61 ± 0.02，对比 β-VAE: 0.35, FactorVAE: 0.40, β-TCVAE: 0.42, VQ-VAE: 0.30, QLAE: 0.52, Tripod: 0.55，变化 +0.06 over Tripod。
> - 3DShapes 上，D (Disentanglement) 为 0.84 ± 0.03，对比 β-VAE: 0.58, FactorVAE: 0.62, β-TCVAE: 0.65, VQ-VAE: 0.50, QLAE: 0.75, Tripod: 0.78，变化 +0.06 over Tripod。

## 概述

该论文提出了一种名为 Bayes-QLAE（贝叶斯量化潜变量自编码器）的非参数贝叶斯框架，旨在解决无监督解耦表示学习中的两个根本性挑战：一是各向同性高斯先验下潜变量缺乏可辨识性保证，二是固定容量离散先验（如 VQ-VAE、QLAE 中的码本）导致表示容量与正则化强度之间的固有权衡。核心思想是为每个生成因子独立引入 Dirichlet Process（DP）混合先验，利用其可数无限的支撑集替代固定大小的码本，从而在保持因子化独立结构的同时实现表示容量的数据驱动自适应扩展。

方法的核心创新在于四个关键设计：将潜变量先验从固定容量离散分布替换为每个因子独立的 DP 混合先验；采用结构化嵌套变分推断族，保留层次依赖关系并将超出截断的参数坍缩回先验，从而实现贪婪的组件扩展；使用深度摊销识别网络输出共轭似然势函数而非直接参数化变分分布；以及依赖分段仿射生成网络满足弱单射条件，为可辨识性提供理论保障。整个模型通过统一的 ELBO 目标函数优化，无需额外的正则化项。

在标准解耦基准上的实验验证了该方法的有效性。在 3DShapes 数据集上，Bayes-QLAE 在 InfoM（0.91±0.03）、InfoC（0.61±0.02）和 DCI 解耦度 D（0.84±0.03）指标上均显著优于所有基线方法，包括 β-VAE、FactorVAE、β-TCVAE、VQ-VAE、QLAE 和 Tripod。在更复杂的 MPI3D 数据集上，模型同样取得了领先或持平的结果（InfoM 0.60±0.03，InfoC 0.56±0.03）。消融实验进一步证实了嵌套变分推断和离散编码的隐式正则化对解耦性能的关键作用——嵌套变分推断一致优于截断和平均场变体，而去量化变体性能显著下降。潜变量遍历可视化显示模型成功将每个生成因子编码到单个潜变量维度，且存在不活跃维度，表明学习到了紧凑且模块化的表示。然而，模型在 MPI3D 上未能捕获所有真实因子，且其依赖的弱单射条件在更一般的非线性生成过程中可能不成立。

## 背景与动机

无监督解耦表示学习旨在从观测数据中恢复独立的生成因子，但其核心瓶颈在于**可辨识性缺失**与**容量-正则化权衡**。现有基于 VAE 的方法（如 β-VAE、FactorVAE、β-TCVAE）依赖各向同性高斯先验，但 Kivva et al. (2022) 等理论工作指出，仅凭高斯先验无法唯一恢复真实生成因子——可辨识性需要潜变量边际分布满足高斯混合模型且生成函数满足弱单射条件；更强的可辨识性（至多置换、缩放与平移）还需引入索引混合组件的离散潜变量，形成层次结构。另一方面，基于向量量化的方法（如 VQ-VAE、QLAE、Tripod）通过离散码本实现隐式正则化，但固定码本大小 K 引入了容量上限：过小的 K 导致容量错配（无法覆盖所有因子模式），过大的 K 则削弱结构约束，违反解耦所需的模块化原则。

本文的动机是**打破固定容量先验的局限性**，同时保持可辨识性所需的结构条件。核心思路是将每个生成因子的潜变量先验建模为独立的 Dirichlet Process 混合先验（stick-breaking 构造），其可数无限支撑允许模型根据数据复杂度自适应扩展每个因子的表示容量。这种设计同时满足三个关键条件：(i) 因子化的独立结构保持可辨识性所需的边际高斯混合形式；(ii) 非参数先验的无限容量避免了固定码本的容量上限；(iii) 早期训练阶段的稀疏码本（从 T=1 开始贪婪扩展）作为隐式正则化促进解耦。

该方法命名为 Bayes-QLAE（Bayesian Quantized Latent Autoencoder），其核心改变在于将潜变量先验从固定容量的离散分布替换为每个因子独立的 Dirichlet Process 混合先验，并通过结构化嵌套变分推断（保留层次依赖关系，超出截断 T 的参数绑定到先验）实现可处理的近似后验。与需要额外正则化项的基线方法不同，Bayes-QLAE 仅通过架构归纳偏置（非参数先验 + 因子化结构 + 弱单射生成函数）即可在统一 ELBO 目标下达到竞争性能，无需 β 权重或总相关正则项等额外项。

## 核心创新

Bayes-QLAE 的核心创新在于用**贝叶斯非参数层次混合先验**替代了现有解耦方法中固定容量的离散先验或各向同性高斯先验，并通过**结构化嵌套变分推断**实现数据驱动的自适应容量扩展，从而在理论上获得可辨识性保证，在实践上突破容量错配瓶颈。

**根本瓶颈与因果旋钮。** 现有无监督解耦方法面临两个根本挑战：一是缺乏可辨识性保证，简单的各向同性高斯先验无法唯一恢复真实生成因子；二是强正则化与表示容量之间存在固有权衡——固定码本大小（如 VQ-VAE 的 K 个嵌入向量）要么因容量不足而欠拟合，要么因容量过剩而过拟合，且结构约束常被违反。Bayes-QLAE 的因果旋钮是：为每个潜变量因子 $e_i$ 独立放置一个 Dirichlet Process (DP) 混合先验，该先验具有可数无限支撑，理论上可以逼近任意复杂的边际分布，同时通过因子化结构保持解耦所需的独立性。

**关键改变的插槽。** 与基线方法相比，四个核心插槽被改变：

1.  **潜变量先验分布**：从各向同性高斯（β-VAE 等）或固定容量离散先验（VQ-VAE, QLAE）变为**每个因子独立的 DP 混合先验**。其 Stick-breaking 构造为 $\beta_{i,k} \mid \alpha \sim \text{Beta}(1, \alpha), \theta_{i,k} \mid \lambda \sim G_0(\lambda)$，诱导出可数无限的高斯混合边际分布 $p(e_i)$。这一改变直接满足了 Kivva et al. (2022) 提出的可辨识性条件：当潜变量边际为高斯混合且引入索引混合组件的离散变量时，表示可达到置换、缩放和平移下的可辨识性；进一步施加最大性条件后，包括潜变量维度和基数在内的完整表示均可辨识。

2.  **离散潜变量容量**：从固定码本大小 K 变为**通过嵌套变分推断实现自适应、数据驱动的容量扩展**。具体地，推理从 T=1 开始，贪婪地逐步增加组件，仅当新组件带来 ELBO 的显著改进时才保留。分配给超出活跃截断 T 的组件的总概率 $q(z_i > T \mid \beta_i)$ 可被闭式计算，用作停止准则。这种"从简到繁"的扩展策略使得模型能够根据每个因子实际的数据复杂度自动决定所需容量，高方差因子（如颜色）先于低方差因子（如形状、方向）扩展。

3.  **变分推断族**：从平均场变分族或固定截断 T 的截断变分族变为**结构化嵌套变分族**。该族保留层次依赖关系——stick-breaking 比例 $\beta_i$、离散变量 $z_i$、组件参数 $\theta_i$ 和连续潜变量 $e_i$ 之间的条件依赖被完整保留。关键设计是：对于超出截断 T 的参数，将其变分分布绑定回先验分布（$q(\beta_{i,k}) = p(\beta_{i,k} \mid \alpha)$ for $k \ge T$）。这意味着未能编码有意义变化的组件会自然坍缩回先验，不会浪费模型容量或引入噪声。

4.  **目标函数**：从 ELBO + 额外正则化项（如 β-VAE 的 β 权重、FactorVAE 的 TC 项）变为**统一的 ELBO 目标函数**，无需任何额外正则化项。解耦能力完全来自于架构归纳偏置和贝叶斯非参数先验的结构约束，而非人工调参的正则化权重。

**核心洞察的因果链条。** 非参数先验的无限容量与因子化结构相结合，产生了一个自洽的因果机制：DP 先验的无限支撑提供了理论上的容量上限无界性 → 嵌套变分推断的贪婪扩展策略确保容量按需分配，避免浪费 → 早期训练阶段的稀疏码本（T 很小）隐式地起到正则化作用，迫使模型优先捕获最重要的变化 → 随着训练进行，高方差因子优先扩展其混合组件，低方差因子随后细化 → 最终每个因子被单个潜变量独立编码，且存在不活跃的潜变量维度，形成紧凑且模块化的表示。这一机制同时解决了容量错配和结构约束违反的问题。

**证据强度与局限。** 决定性证据来自三个方面：一是 Table 1 和 Table 2 显示 Bayes-QLAE 在 3DShapes 和 MPI3D 上全面超越所有基线方法（3DShapes 上 InfoM 0.91±0.03 对比 Tripod 0.85；MPI3D 上 InfoC 0.56±0.03 对比 Tripod 0.48），置信度 0.95；二是 Table 4 的消融实验表明嵌套变分推断（Bayes-QLAE）一致优于截断变分推断（T-QLAE）和平均场变分推断（MF-QLAE），且去量化变体（DQ-QLAE）性能显著下降，证实了离散编码的隐式正则化作用，置信度 1.0；三是 Figure 2 的可视化展示了因子特定混合组件数量的自适应增长过程，验证了非参数先验的数据驱动容量扩展能力，置信度 0.9。但需注意：在 MPI3D 上模型未能捕获所有真实生成因子，表明容量扩展可能仍受限于优化过程或数据复杂度；嵌套变分推断的贪婪扩展阈值选择可能影响最终性能，这一点需要手动验证其敏感性。

## 整体框架

Bayes-QLAE（Bayesian Quantized Latent Autoencoder）的整体pipeline以**贝叶斯非参数层次混合先验**替代传统解耦方法中固定容量的离散先验，形成一条数据驱动的自适应表示学习流。其核心设计围绕四个模块展开，构成一个端到端的可辨识生成框架。

**编码器（Amortized Recognition Network）** 是pipeline的入口。它不直接输出变分参数，而是为每个因子 $i$ 输出一个因子化的共轭似然势函数 $\hat{p}_\phi(e_i|x) = \exp\{\langle h_i(x;\phi), t_e(e_i) \rangle\}$。这一设计的关键动机在于：将数据依赖的信号以共轭形式注入后续的变分推断，使得后验更新可解析计算，从而避免标准VAE中直接参数化变分分布带来的近似误差。

**非参数先验模块（DP Prior per Factor）** 是框架的理论核心。对每个潜变量维度 $i$，模型独立放置一个Dirichlet Process混合先验。通过Sethuraman的stick-breaking构造，每个因子的边缘分布 $p(e_i)$ 被建模为可数无限的高斯混合：

$$
\beta_{i,k} \mid \alpha \sim \text{Beta}(1, \alpha), \quad \theta_{i,k} \mid \lambda \sim G_0(\lambda)
$$

这一设计的因果机制在于：无限容量使得模型无需预先指定每个因子的离散模式数量，而因子化结构则保证了每个潜变量独立控制一个生成因子，从而满足可辨识性所需的条件（GMM边缘分布 + 层次离散变量索引）。

**结构化嵌套变分推断模块** 是连接先验与数据的推断引擎。它保留每个因子内部stick-breaking比例 $\beta_i$、离散变量 $z_i$、组件参数 $\theta_i$ 和连续潜变量 $e_i$ 之间的层次依赖关系：

$$
q_\nu(e_i, z_i, \beta_i, \pmb{\theta}_i) = q(e_i \mid z_i, \pmb{\theta}_i) q(z_i \mid \beta_i) \prod_{k=1}^{T-1} q_{\nu_{\beta_{i,k}}}(\beta_{i,k}) \prod_{k=1}^{T} q_{\nu_{\theta_{i,k}}}(\theta_{i,k})
$$

嵌套变分族的关键创新在于：对于超出活跃截断 $T$ 的组件，将其变分参数绑定回先验分布 $p(\beta_{i,k} \mid \alpha)$ 和 $p(\theta_{i,k} \mid \lambda)$。这一设计使得模型可以从 $T=1$ 开始，通过贪婪扩展逐步增加组件数量——仅当新组件带来显著的ELBO改进时才被激活。训练过程中，那些未能编码有意义变化的组件会自动坍缩回先验，从而实现数据驱动的容量自适应。

**解码器（Piecewise Affine Generator）** 使用ReLU激活的分段仿射深度神经网络，满足弱单射条件。这一设计确保了生成函数 $g_{\theta_g}: \mathbb{R}^d \to \mathcal{X}$ 的可辨识性理论成立——在GMM先验和层次离散结构的共同作用下，潜空间可达置换、缩放和平移意义下的可辨识性。

四个模块之间的数据流如下：输入 $x$ 经编码器产生共轭势函数 $\hat{p}_\phi(e|x)$；该势函数与非参数先验在嵌套变分推断模块中融合，通过局部ELBO分解逐因子计算后验；推断得到的连续潜变量 $e$ 传递给解码器生成重建 $\hat{x}$。整个pipeline的优化目标为统一的ELBO，无需任何额外的正则化项——这是与 $\beta$-VAE、FactorVAE等基线方法的根本区别。

## 核心模块与公式推导

### 1. 生成模型与联合分布分解

Bayes-QLAE 的核心在于为每个潜变量维度 $i$ 独立地放置一个 **Dirichlet Process (DP) 混合先验**，从而构造一个具有可数无限支撑的层次化生成结构。该结构直接回应了可辨识性的理论要求：仅当潜变量边缘分布为高斯混合模型（GMM）且引入索引混合组件的离散潜变量时，才能实现排列、缩放和平移意义上的可辨识性；进一步施加最大性条件（Kivva et al. 2022 的 P3）后，可达到完整潜表示（包括维度、基数与排列）的可辨识性。

生成模型的联合分布分解如下（锚点 2.1）：

$$
p \left( x , e , z , \beta , \boldsymbol { \theta } \mid \alpha , \lambda \right) = p _ { \boldsymbol { \theta } _ { g } } \left( x \mid e \right) \prod _ { i = 1 } ^ { d } p \left( e _ { i } \mid z _ { i } , \boldsymbol { \theta } _ { i } \right) p \left( z _ { i } \mid \beta _ { i } \right) \prod _ { k = 1 } ^ { \infty } p \left( \beta _ { i , k } \mid \alpha \right) p \left( \theta _ { i , k } \mid \lambda \right)
$$

其中：
- $x$ 为观测数据，由解码器 $p_{\theta_g}(x|e)$ 生成，该解码器采用满足弱单射条件的 ReLU 分段仿射网络。
- $e_i$ 为第 $i$ 个因子的连续潜变量，其条件分布 $p(e_i|z_i, \theta_i)$ 为高斯分布，由离散潜变量 $z_i$ 索引的混合组件参数 $\theta_i$ 决定。
- $z_i$ 为离散潜变量，其分布由 stick-breaking 比例 $\beta_i$ 通过 $p(z_i|\beta_i)$ 决定，$\beta_i$ 本身服从 Beta(1, $\alpha$) 先验：
  $$
  \beta _ { i , k } \mid \alpha \sim p ( \beta \mid \alpha ) = \mathrm { B e t a } \left( 1 , \alpha \right) , \quad \theta _ { i , k } \mid \lambda \sim p ( \theta \mid \lambda ) = G _ { 0 } ( \lambda )
  $$
- $\alpha$ 为 DP 的浓度参数，控制组件分配的倾向性；$\lambda$ 为基分布 $G_0$ 的超参数（在实验中为 Normal-Inverse-Wishart 分布）。

**瓶颈机制**：该分解的因果杠杆在于，每个因子的表示容量不再受固定码本大小 $K$ 的限制，而是由 DP 先验的可数无限支撑自适应决定。因子化的先验结构（$\prod_i$）确保了不同因子的表示在生成过程中是独立的，这是解耦的结构性前提。

### 2. 结构化嵌套变分推断

由于后验 $p(e, z, \beta, \theta|x)$ 是难以处理的，论文提出了一个保留层次依赖关系的**结构化变分族**（锚点 2.2）：

$$
q _ { \nu } ( e _ { i } , z _ { i } , \beta _ { i } , \pmb { \theta } _ { i } ) = q ( e _ { i } \mid z _ { i } , \pmb { \theta } _ { i } ) q ( z _ { i } \mid \beta _ { i } ) \prod _ { k = 1 } ^ { T - 1 } q _ { \nu _ { \beta _ { i } , k } } ( \beta _ { i , k } ) \prod _ { k = 1 } ^ { T } q _ { \nu _ { \theta _ { i , k } } } ( \theta _ { i , k } )
$$

其中 $T$ 为当前活跃的截断水平。该变分族的关键创新在于**嵌套结构**：对于超出截断 $T$ 的组件，其变分分布被绑定到先验分布，从而避免了固定截断带来的容量上限问题：

$$
q _ { \nu _ { \beta } } ( \beta _ { i } ) = \prod _ { k = 1 } ^ { T } q _ { \nu _ { \beta _ { i , k } } } ( \beta _ { i , k } ) \prod _ { k = T } ^ { \infty } p ( \beta _ { i , k } \mid \alpha ) , \qquad q _ { \nu _ { \theta } } ( \theta _ { i } ) = \prod _ { k = 1 } ^ { T } q _ { \nu _ { \theta _ { i , k } } } ( \theta _ { i , k } ) \prod _ { k = T } ^ { \infty } p ( \theta _ { i , k } \mid \lambda )
$$

**失败模式**：与传统的截断变分推断（T-QLAE）相比，固定截断 $k=10$ 或 $k=50$ 会导致容量错配——要么过早截断限制了表达能力，要么过大的固定容量引入了冗余组件并增加了优化难度。嵌套变分族通过将未使用组件的变分参数坍缩回先验，实现了数据驱动的容量自适应。

### 3. 证据下界（ELBO）与局部分解

在嵌套变分族下，单个数据点的 ELBO 为（锚点 2.3）：

$$
\mathcal { L } = \mathbb { E } _ { q _ { \nu _ { \beta } } } \left[ \log \frac { p ( \beta \mid \alpha ) } { q _ { \nu _ { \beta } } ( \beta ) } \right] + \mathbb { E } _ { q _ { \nu _ { \theta } } } \left[ \log \frac { p ( \theta \mid \lambda ) } { q _ { \nu _ { \theta } } ( \theta ) } \right] + \mathbb { E } _ { q _ { \nu } } \left[ \log \frac { p _ { \theta _ { g } } ( x \mid e ) p ( e \mid z , \theta ) p ( z \mid \beta ) } { q ( e \mid z , \theta ) q ( z \mid \beta ) } \right]
$$

前两项为全局参数（$\beta$ 和 $\theta$）的 KL 散度，第三项为数据依赖项。为处理数据依赖项中的难解积分，论文采用了**摊销共轭似然势函数**（锚点 2.3），由识别网络 $h(x; \phi)$ 输出：

$$
\hat { p } _ { \phi } ( e \mid x ) = \prod _ { i = 1 } ^ { d } \hat { p } _ { \phi } ( e _ { i } \mid x ) = \prod _ { i = 1 } ^ { d } \exp \{ \langle h _ { i } ( x ; \phi ) , t _ { e } ( e _ { i } ) \rangle \}
$$

其中 $t_e(e_i)$ 为 $e_i$ 的充分统计量。该势函数替代了标准 VAE 中直接参数化变分分布的做法，使得数据依赖信号能够以共轭方式与结构化先验结合。

在共轭条件下，数据依赖 ELBO 项可分解为每个因子 $i$ 的局部贡献之和：

$$
\mathcal { L } _ { i } = \mathbb { E } _ { q _ { \nu _ { \beta } } ( \beta _ { i } ) q ( z _ { i } | \beta _ { i } ) } \left[ \log \frac { p ( z _ { i } \mid \beta _ { i } ) } { q ( z _ { i } \mid \beta _ { i } ) } + \mathbb { E } _ { q _ { \nu _ { \theta } } ( \theta _ { i } ) q ( e _ { i } | z _ { i } , \theta _ { i } ) } \left[ \log \frac { p ( e _ { i } \mid z _ { i } , \theta _ { i } ) } { q ( e _ { i } \mid z _ { i } , \theta _ { i } ) } + \log \hat { p } _ { \phi } ( e _ { i } \mid x ) \right] \right]
$$

**因果机制**：该局部分解使得每个因子的变分更新可以独立进行，是因子化先验结构在推断层面的自然延伸。$e_i$ 的最优变分分布具有闭式解：

$$
q ( e _ { i } \mid z _ { i } , \pmb \theta _ { i } ) = \exp \left\{ \langle \eta _ { e } ( z _ { i } , \eta _ { \theta } ( \pmb \theta _ { i } ) , \phi ) , t _ { e } ( e ) \rangle - A _ { e } ( \eta _ { e } ( z _ { i } , \eta _ { \theta } ( \pmb \theta _ { i } ) , \phi ) ) \right\}
$$

其中 $\eta_e$ 为结合了结构化先验自然参数和识别网络输出 $\hat{p}_\phi$ 的联合自然参数。

### 4. 贪心组件扩展与停止准则

嵌套变分族支持一个**贪心推断过程**（锚点 2.3）：从 $T=1$ 开始，逐步增加组件数量，仅当新组件能显著提升 ELBO 时才保留。扩展的停止准则基于分配给所有超出活跃截断 $T$ 的组件的总概率的可处理闭式估计：

$$
q ( z _ { i } > T \mid \beta _ { i } ) = \Bigl ( 1 - \displaystyle \sum _ { k = 1 } ^ { T } \pi _ { i , k } \Bigr ) \cdot \exp \Bigl \{ \mathbb { E } _ { p ( \theta \mid \lambda ) } \log \hat { p } _ { \phi } ( x _ { i } \mid \theta ) \Bigr \}
$$

其中 $\pi_{i,k}$ 为第 $k$ 个组件的混合权重。该准则衡量了当前模型对未探索变化空间的捕获潜力。

**证据强度**：消融实验（Table 4）验证了嵌套变分推断（Bayes-QLAE）在 MPI3D 上 InfoM 达到 0.58±.04，显著优于截断变分推断 T-QLAE（k=10: 0.54±.04; k=50: 0.51±.06）和平均场变分推断 MF-QLAE（0.49±.04）。去量化变体 DQ-QLAE（InfoM: 0.52±.02）的性能下降进一步表明，离散编码的隐式正则化对解耦至关重要。Figure 2 的可视化也证实了高方差因子（如颜色）的组件数量先于低方差因子（如形状、方向）扩展，表明模型优先捕获对重建目标贡献更大的变化。

## 实验与分析

**主结果：Bayes-QLAE 在标准解耦基准上达到最优**

在 3DShapes 数据集上（Table 1），Bayes-QLAE 在所有指标上均显著超越基线方法。InfoM 达到 0.91±0.03（Tripod 基线为 0.85），InfoC 达到 0.61±0.02（Tripod 为 0.55），DCI 解耦度 D 达到 0.84±0.03（Tripod 为 0.78）。这一优势在更复杂的 MPI3D 数据集上（Table 2）同样保持：InfoM 为 0.60±0.03（Tripod 为 0.55），InfoC 为 0.56±0.03（Tripod 为 0.48）。相比于基于 VAE 的强正则化方法（β-VAE、FactorVAE、β-TCVAE）和基于固定码本量化的方法（VQ-VAE、QLAE），Bayes-QLAE 的 InfoC 提升尤为显著，表明其模块化表示在紧凑性上具有本质优势。值得注意的是，这一性能提升完全来自结构归纳偏置（即非参数先验与嵌套变分推断），无需引入任何额外的正则化项。

![[assets/figures/papers/iclr26_0001_GVOLiaENgU_A_Bayesian_Nonparametric_Framework_For_Learning/figures/001_Table_1.jpg]]
*Table 1: Disentanglement metrics measured in InfoMEC and DCI for 3DShapes dataset. For each metric a higher score is better. The scores for all the models were averaged across 5 runs with different random seeds with intervals denoting 95% confidence intervals of the mean estimated assuming a t-distribution. The results for the VQE-based and QLAE-based models are obtained using the hyperparameter settings and experimental conditions as described in Locatello et al. (2019b) and Hsu et al. (2024a;b) respectively*

![[assets/figures/papers/iclr26_0001_GVOLiaENgU_A_Bayesian_Nonparametric_Framework_For_Learning/figures/002_Table_2.jpg]]
*Table 2: Disentanglement metrics measured in InfoMEC and DCI for MPI3D dataset. For each metric a higher score is better. The scores for all the models were averaged across 5 runs with different random seeds with intervals denoting 95% confidence intervals of the mean estimated assuming a t-distribution*

**消融研究：嵌套变分推断与离散编码是关键机制**

Table 4 的消融实验揭示了两个核心机制的作用。第一，变分推断族的选择至关重要：嵌套变分推断（Bayes-QLAE）在 MPI3D 上 InfoM 为 0.58±0.04，InfoC 为 0.51±0.03，一致优于截断变分推断（T-QLAE，k=10 时 InfoM 0.54±0.04、InfoC 0.40±0.03；k=50 时 InfoM 0.51±0.06、InfoC 0.48±0.05）和平均场变分推断（MF-QLAE，InfoM 0.49±0.04、InfoC 0.49±0.04）。T-QLAE 即使增加截断容量（k=10→50）也无法匹配嵌套族的性能，说明截断近似破坏了后验中的层次依赖关系，导致容量分配失配。第二，离散编码的隐式正则化不可或缺：去量化变体 DQ-QLAE（InfoM 0.52±0.02、InfoC 0.43±0.02）性能显著下降，证实了离散潜变量在促进解耦中的关键作用。

![[assets/figures/papers/iclr26_0001_GVOLiaENgU_A_Bayesian_Nonparametric_Framework_For_Learning/figures/004_Table_4.jpg]]
*Table 4: Model performance comparison across different information metrics*

**自适应容量扩展与学习动态**

Figure 2 展示了 3DShapes 训练过程中每个因子对应的混合组件数量的演化。高方差因子（如地板色、物体色、墙壁色）的组件数率先增长，而低方差几何因子（如物体方向、形状）则在后训练阶段才逐步细化。这一数据驱动的容量扩展模式验证了非参数先验的核心优势：模型根据各因子对重建目标的贡献度自适应分配表示容量，而非依赖人工预设的固定码本。Figure 1 的潜变量遍历可视化进一步表明，模型成功将 3DShapes 的 6 个真实生成因子和 MPI3D 的 7 个因子分别编码到独立的潜变量维度上，且存在不活跃的潜变量维度，说明学习到的表示是紧凑且模块化的。

**失败模式与局限性**

尽管取得了最优性能，Bayes-QLAE 在 MPI3D 上仍未能捕获所有真实生成因子（Figure 3 注释指出某些因子未被分配到活跃潜变量维度）。这表明非参数先验的容量扩展可能受限于优化过程——贪婪组件扩展依赖于 ELBO 改进阈值，该阈值的选择可能影响最终性能。此外，模型依赖分段仿射生成函数（ReLU 网络）和弱单射条件，这些假设在更一般的非线性生成过程中可能不成立。当前框架仅在图像数据上验证，其在文本、音频等模态的适用性尚待探索。

### 补充图表

![[assets/figures/papers/iclr26_0001_GVOLiaENgU_A_Bayesian_Nonparametric_Framework_For_Learning/figures/003_Table_3.jpg]]
*Table 3: Fixed Hyperparameters and initializations*

## 方法谱系与知识库定位

Bayes-QLAE 在解耦表示学习的方法谱系中占据一个独特的位置：它直接回应了无监督解耦领域两个根本性的瓶颈——**缺乏可辨识性保证**与**固定容量先验导致的容量错配**。从方法谱系看，它位于两条技术路线的交汇点：一是以 β-VAE、FactorVAE、β-TCVAE 为代表的基于强正则化的连续潜变量路线，二是以 VQ-VAE、QLAE、Tripod 为代表的基于向量量化的离散潜变量路线。Bayes-QLAE 的核心洞察在于，将后者的离散编码结构（提供隐式正则化）与前者的连续潜变量灵活性相结合，但用**非参数贝叶斯层次混合先验**替代了固定码本大小这一关键瓶颈。

**与基线的关系：三个关键差异**

1. **先验容量的可扩展性**：所有基线方法（VQ-VAE 的固定 K 个码本、QLAE 的固定码本、Tripod 的固定离散化）都要求预先设定潜变量的容量上限。Bayes-QLAE 通过为每个因子独立放置 Dirichlet Process 混合先验，实现了数据驱动的自适应容量扩展——从 T=1 开始，仅当新组件能显著提升 ELBO 时才逐步添加。这种设计直接避免了固定码本带来的容量上限问题，同时通过早期阶段的稀疏码本隐式正则化促进解耦。消融实验（Table 4）证实，嵌套变分推断（Bayes-QLAE）在所有解耦指标上一致优于截断变分推断（T-QLAE）和平均场变分推断（MF-QLAE），表明保留层次依赖关系的结构化推断是性能提升的关键。

2. **可辨识性保证**：β-VAE 等连续方法依赖各向同性高斯先验，理论上无法唯一恢复真实生成因子。Bayes-QLAE 通过引入因子化的 GMM 先验（每个因子独立的高斯混合）以及额外的离散潜变量索引混合组件，满足了 Kivva et al. (2022) 提出的可辨识性条件——在层次结构上施加最大性条件后，潜变量表示（包括维度、基数和语义）可辨识到置换、缩放和平移。这是 VQ-VAE/QLAE 等离散方法所不具备的理论保证。

3. **统一的目标函数**：与 β-VAE 等需要额外正则化项（β 权重、TC 项）不同，Bayes-QLAE 仅通过架构归纳偏置——非参数先验的无限容量与因子化结构——在统一的 ELBO 目标下实现解耦。这避免了正则化强度超参数调优的负担，也规避了强正则化与表示容量之间的固有权衡。

**适用边界与条件**

Bayes-QLAE 的有效性依赖于几个关键假设：(i) 生成函数为分段仿射（ReLU 网络）且满足弱单射条件，这在更一般的非线性生成过程中可能不成立；(ii) 每个生成因子的变化可被有限个高斯组件覆盖（离散模式），对于具有连续生成因子的数据集（如连续旋转角度），非参数先验的有效性需要进一步验证；(iii) 当前仅在标准解耦基准（3DShapes、MPI3D）上验证，这些数据集具有已知的、独立的真实生成因子，且图像尺寸较小（64×64）。

**局限与开放问题**

1. **容量扩展的局限性**：在 MPI3D 数据集上，模型未能捕获所有真实生成因子（某些因子未被分配到活跃潜变量维度），表明非参数先验的容量扩展仍受限于优化过程或数据复杂度。Figure 2 显示，高方差因子（如颜色）先于低方差因子（如形状、方向）扩展，这种层次学习策略虽然合理，但也暗示了优化可能陷入局部最优。

2. **先验选择**：当前使用 Dirichlet Process 先验，其 stick-breaking 构造假设组件的权重按指数衰减。对于具有幂律因子分布的数据集，Pitman–Yor 过程可能更合适，但这需要进一步验证。

3. **模态泛化**：当前仅针对图像数据验证，其在文本、音频等其他模态上的适用性尚未探索。非参数先验的因子化结构是否适用于序列数据或结构化数据仍是开放问题。

4. **阈值敏感性**：贪婪组件扩展策略依赖于 ELBO 改进阈值，该阈值的选择可能影响最终性能。当前实验未系统分析阈值对解耦质量的影响。

5. **公平性**：模型通过因子化先验结构显式分离不同因子，这为将敏感属性隔离到独立潜变量维度提供了框架基础，但本文未进行公平性评估。在涉及敏感属性（如种族、性别）的应用中，需要额外的公平性约束。

总体而言，Bayes-QLAE 在无监督解耦领域提供了一个理论上有保证、实践上有效的框架，但其在更复杂数据、更一般生成假设下的适用性仍需进一步验证。将非参数先验扩展到连续生成因子、探索更灵活的随机过程（如 Pitman–Yor 过程），以及将框架推广到其他模态，是当前最直接的开放方向。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Bayesian_Nonparametric_Framework_For_Learning_Disentangled_Representations.pdf

![[paperPDFs/ICLR_2026/A_Bayesian_Nonparametric_Framework_For_Learning_Disentangled_Representations.pdf]]
