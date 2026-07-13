---
title: GPHLVM Bringing Motion Taxonomies to Continuous Domains via GPLVM on Hyperbolic Manifolds
type: paper
paper_level: A
venue: ICML
year: 2024
pdf_ref: paperPDFs/ICML_2024/GPHLVM_Bringing_Motion_Taxonomies_to_Continuous_Domains_via_GPLVM_on_Hyperbolic_Manifolds.pdf
project_link: null
code_link: https://github.com/geoopt/
aliases:
- GPHLVMG
- GBMTCDGHM
tags:
- ICML_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 潜在空间的双曲几何（具有指数增长距离特性，自然适合树状层次）结合显式图结构先验（应力损失）和距离保持反向约束，使嵌入能够准确反映原始分类图的拓扑距离。
primary_logic: 双曲流形上的距离呈指数增长，最短路径趋向通过原点，这一几何特性恰好对应连续的层次结构。因此，将高斯过程潜在变量模型（GPLVM）的潜在空间从欧氏空间推广到双曲流形，并注入分类学图结构的先验知识，可以在连续嵌入空间中忠实地编码离散的层次分类，并利用测地线插值生成平滑、真实感强的运动过渡。
claims:
- 双曲嵌入能够捕捉分类学的层次结构
- GPHLVM 将生成映射定义在双曲潜在空间上，并配合双曲核与包裹高斯先验
- 具有应力先验和反向约束的 GPHLVM 在多个运动分类学上均取得比欧氏 GPLVM 和 VAE 更低的应力值，即更好地保留了图距离结构
- 利用双曲潜在空间的测地线插值可以生成平滑且真实感强的运动过渡，其平滑度（急动度）显著优于欧氏空间中的线性插值
---

# GPHLVM Bringing Motion Taxonomies to Continuous Domains via GPLVM on Hyperbolic Manifolds

> [!tip] 核心洞察
> 双曲流形上的距离呈指数增长，最短路径趋向通过原点，这一几何特性恰好对应连续的层次结构。因此，将高斯过程潜在变量模型（GPLVM）的潜在空间从欧氏空间推广到双曲流形，并注入分类学图结构的先验知识，可以在连续嵌入空间中忠实地编码离散的层次分类，并利用测地线插值生成平滑、真实感强的运动过渡。

| 字段 | 内容 |
|------|------|
| 中文题名 | GPHLVM：基于双曲流形高斯过程潜在变量模型的运动分类学嵌入 |
| 英文题名 | GPHLVM Bringing Motion Taxonomies to Continuous Domains via GPLVM on Hyperbolic Manifolds |
| 会议/期刊 | ICML 2024 |
| Links | [Code](https://github.com/geoopt/) · [paper](https://arxiv.org/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Gaussian Process Hyperbolic Latent Variable Model (GPHLVM) |
| Dataset | Hand Grasps Taxonomy, Whole-body Support Poses Taxonomy |

> [!tip] 效果简介
> - Hand Grasps Taxonomy (Stival et al., 2019) 上，Stress (lower better) GPHLVM L^2 BC+stress: 0.14±0.16 vs GPLVM R^2 BC+stress: 0.39±0.41 (降低 0.25)。
> - Whole-body Support Poses Taxonomy (Borras et al., 2017) 上，应力 (lower better) GPHLVM L^2 BC+stress: 0.53±0.83 vs GPLVM R^2 BC+stress: 0.63±0.94 (降低 0.10)。
> - Hand Grasps Taxonomy (motion generation quality) 上，急动度 (Jerkiness, lower smoother) GPHLVM L^2: 108.65±140.54 vs GPLVM R^2: 1377.05±1721.44 (降低约 92%)。

## 概要

人类运动分类学（如抓握类型、全身支撑姿态）以层次化图结构组织离散的运动类别，蕴含丰富的先验知识。然而，现有运动生成模型通常忽略这种离散层次信息，导致分类学难以直接用于连续运动表示与生成。本文提出**高斯过程双曲潜在变量模型（GPHLVM）**，核心思路是将潜在空间从欧氏空间推广到双曲流形——双曲几何的距离呈指数增长、最短路径趋向通过原点，这一特性恰好对应树状层次结构——从而在连续嵌入空间中忠实地编码离散的分类学层次。

具体而言，GPHLVM 在三个关键层面进行了改造：将潜在变量先验替换为双曲包裹高斯分布，将高斯过程核函数替换为基于热方程解的双曲核（2D 时采用保证正定的蒙特卡洛近似），并将优化过程替换为黎曼优化。在此基础上，引入**图距离保持的应力先验**和**反向约束映射**，显式地将分类学图的拓扑结构注入潜在嵌入。

实验覆盖三种机器人运动分类学（双手操控、抓握、全身支撑姿态），结果表明：
- 双曲嵌入在应力（stress）指标上显著优于欧氏 GPLVM，即更好地保留了分类图的节点间最短路径距离；
- 利用双曲潜在空间的测地线插值生成的连续运动，其平滑度（急动度）比欧氏线性插值降低约 92%；
- 与 VAE 及其双曲变体相比，GPHLVM 在应力与重建误差上均表现更优，且仅需约 100 个静态姿态即可达到可比较的运动质量，体现出在低数据量下的优势。

本方法在**方法谱系**上属于高斯过程潜在变量模型的几何推广，将双曲表征学习与图结构保持正则化相结合，为层次化分类学知识的连续嵌入与运动生成提供了新路径。

### 人类运动分类学的表示困境

人类运动理解与生成长期面临一个核心矛盾：一方面，认知科学和机器人学积累了丰富的**离散层次化运动分类学**（taxonomy），例如手部抓握分类（Stival et al., 2019）、全身支撑姿态分类（Borras et al., 2017）和双手操控动作分类（Krebs & Asfour, 2022）。这些分类学以树状或图状结构组织，蕴含了动作之间的语义距离和层次关系。另一方面，真实运动数据存在于**高维连续空间**——例如全身关节角度或手部关节构型——其几何结构与离散分类图之间存在根本性差异。

这一鸿沟导致了一个关键瓶颈：**分类学的层次知识难以被直接注入到连续运动表示学习中**。现有方法要么忽略分类学结构，仅在欧氏空间中学习无结构的嵌入；要么将分类学仅作为标签使用，无法利用层次间的距离信息。其结果是，生成的运动插值往往在语义上不连贯，或无法反映分类学所定义的动作过渡路径。

### 现有方法的局限

**欧氏高斯过程潜在变量模型（GPLVM）**（Lawrence, NIPS 2003; Titsias & Lawrence, AISTATS 2010）是连续运动数据降维和生成的代表性框架。它将潜在变量定义在欧氏空间 $\mathbb{R}^Q$ 上，配合标准高斯先验 $\mathcal{N}(\mathbf{0}, \pmb{I})$ 和平方指数核，通过高斯过程将低维潜在表示映射到高维观测空间。然而，欧氏空间的几何特性——距离呈多项式增长——与树状层次结构的**指数增长距离特性**根本不相容。这导致 GPLVM 即使在引入图先验的情况下，也无法在潜在空间中忠实地保持分类图的拓扑距离（Table 1 中 GPLVM R² BC+stress 的应力值显著高于对应的双曲模型）。

类似地，**变分自编码器（VAE）**及其双曲变体虽然能够学习非线性嵌入，但其 KL 正则化项的目标是使潜在分布趋近先验，而非保持图结构距离。实验表明，VAE 的嵌入在应力指标上表现不佳，其正则化目标与保持分类学图距离之间存在内在冲突（Table 13, App. H.1）。

### 核心洞察：双曲几何作为层次结构的自然载体

本文的核心洞察来源于双曲几何的一个基本性质：**在双曲流形上，距离随径向坐标呈指数增长，且最短路径（测地线）倾向于通过原点**。这一几何特性恰好对应树状层次结构——从根节点到叶节点的路径在双曲空间中可以被自然嵌入，使得父子节点间的距离与它们在分类学中的语义距离成正比。

基于此，本文提出将 GPLVM 的潜在空间从欧氏空间推广到**双曲洛伦茨模型 $\mathcal{L}^Q$**，形成**高斯过程双曲潜在变量模型（GPHLVM）**。这一推广并非简单的几何替换，而是需要对 GPLVM 的三个核心组件进行系统性重构：

1. **潜在变量先验**：从标准正态分布替换为双曲包裹高斯分布 $\mathcal{N}_{\mathcal{L}^Q}(\pmb{\mu}_0, \alpha \mathcal{I})$
2. **核函数**：从欧氏平方指数核替换为基于热方程解的双曲核 $k^{\mathcal{L}^Q}$
3. **优化过程**：从标准梯度下降替换为基于 Riemannian Adam 的黎曼优化

### 从几何先验到结构注入

双曲几何本身提供了与层次结构相容的**归纳偏置**（inductive bias），但仅靠几何先验无法保证嵌入精确反映特定分类图的拓扑距离。为此，本文进一步引入两个互补机制：

- **图距离应力先验**（stress prior）：通过惩罚嵌入间测地距离与分类图最短路径距离的差异，强制全局图结构保持
- **图距离保持反向约束**（back-constraints）：将潜在变量定义为观测数据与图节点相似性的函数，使新数据嵌入后仍能保持局部与全局结构

这一双重机制使得 GPHLVM 能够在连续双曲嵌入空间中**忠实地编码离散层次分类**，并利用测地线插值生成平滑、语义连贯的运动过渡。

## 核心方法与创新机理

GPHLVM 的核心创新在于将高斯过程潜在变量模型（GPLVM）的潜在空间从欧氏空间推广到双曲流形，并引入显式的图结构先验，从而在连续嵌入空间中忠实地编码离散层次分类学。这一创新沿着三条轴线展开：

### 1. 潜在空间几何的变革：从欧氏到双曲

标准 GPLVM（Lawrence, NIPS 2003; Titsias & Lawrence, AISTATS 2010）将潜在变量定义在欧氏空间 $\mathbb{R}^Q$ 上，赋予标准正态先验 $\mathcal{N}(\mathbf{0}, \pmb{I})$。然而，欧氏空间的线性距离增长特性与分类学的树状层次结构存在根本性的几何失配——在树结构中，节点数量随深度指数增长，而欧氏空间的体积仅多项式增长。

GPHLVM 将潜在空间替换为双曲洛伦茨模型 $\mathcal{L}^Q$，其核心优势在于：
- **指数增长的距离特性**：双曲流形上的测地距离随半径指数增长，天然对应树状层次结构中节点数量的指数扩张。
- **最短路径趋向原点**：双曲空间中的测地线倾向于经过原点，这一几何特性恰好对应连续的层次结构——从根节点到叶节点的路径自然映射为穿过原点的测地线。

具体而言，潜在变量先验从标准正态分布替换为双曲包裹高斯分布 $\mathcal{N}_{\mathcal{L}^Q}(\pmb{\mu}_0, \alpha\mathcal{I})$，其对数密度函数为：

$$\log \mathcal{N}_{\mathcal{L}^d}(\pmb{x}; \pmb{\mu}, \pmb{\Sigma}) = \log \mathcal{N}(\pmb{v}; \mathbf{0}, \pmb{\Sigma}) - (d-1) \log\left( \sinh(\|\pmb{u}\|_c) / \|\pmb{u}\|_c \right)$$

该分布通过将切空间中的高斯样本平行传输后经指数映射投影到流形上得到，保证了先验本身与双曲几何的一致性。

### 2. 核函数与优化方法的双曲适配

仅改变潜在空间的几何是不够的，GPLVM 的两个核心组件——核函数与优化过程——也必须适配双曲流形：

**双曲热核**：标准 GPLVM 使用欧氏平方指数（SE）核或 Matérn 核度量潜在变量间的相似性。GPHLVM 将其替换为基于热方程解的双曲核。对于 $\mathcal{L}^2$（二维双曲空间），核函数为积分形式：

$$k^{\mathcal{L}^2}(\pmb{x}, \pmb{x}') = \frac{\sigma^2}{C_\infty} \int_{\rho}^{\infty} \frac{s e^{-s^2/(2\kappa^2)}}{(\cosh(s) - \cosh(\rho))^{1/2}} \mathrm{d}s$$

该积分无闭式解，论文采用保证正定的蒙特卡洛近似。对于 $\mathcal{L}^3$，存在闭式解：

$$k^{\mathcal{L}^3}(\pmb{x}, \pmb{x}') = \frac{\sigma^2}{C_\infty} \frac{\rho}{\sinh \rho} e^{-\rho^2/(2\kappa^2)}$$

**黎曼优化**：标准 GPLVM 使用欧氏梯度下降或 Adam 优化器。GPHLVM 采用 Riemannian Adam，其更新步骤包含指数映射与平行传输：

$$\eta_t \leftarrow h(\text{grad } \ell(\pmb{x}_t), \tau_{t-1}), \quad \pmb{x}_{t+1} \leftarrow \text{Exp}_{\pmb{x}_t}(-\alpha_t \eta_t), \quad \tau_t \leftarrow P_{\pmb{x}_t \to \pmb{x}_{t+1}}(\eta_t)$$

这确保了参数更新始终位于双曲流形上，保持几何一致性。

### 3. 分类学图结构的显式注入

仅仅使用双曲几何作为归纳偏置不足以保证嵌入忠实地反映分类学图结构。GPHLVM 引入两个互补机制将离散的图先验注入连续潜在空间：

**应力损失（Stress Loss）**：直接惩罚嵌入间测地距离与分类图最短路径距离的差异：

$$\ell_{\text{stress}}(\pmb{X}) = \sum_{i < j} \big( \text{dist}_{\mathbb{G}}(c_i, c_j) - \text{dist}_{\mathcal{L}^Q}(\pmb{x}_i, \pmb{x}_j) \big)^2$$

该正则化项强制全局图拓扑在嵌入空间中得以保持。消融实验表明，无正则化的纯 GPHLVM 无法编码有意义的分类图距离结构，而仅添加应力先验即可使嵌入的测地距离与图的最短路径距离高度一致。

**图距离保持的反向约束（Back-constraints）**：将潜在变量定义为观测数据与图节点相似性的函数：

$$\pmb{x}_n = \text{Exp}_{\pmb{\mu}_0}(\tilde{\pmb{x}}_n), \quad \tilde{x}_{n,q} = \sum_{m=1}^{N} w_{q,m} k^{\mathbb{R}^D}(\pmb{y}_n, \pmb{y}_m) k^{\mathbb{G}}(c_n, c_m)$$

通过观测的欧氏核与图核的乘积，反向约束使新数据嵌入后仍能保持局部与全局结构，并在类别内部基于观测相似性组织嵌入。实验表明，应力先验与反向约束的组合在多个运动分类学上均取得比欧氏 GPLVM 和 VAE 更低的应力值（Table 1），验证了图结构先验对层次保持的关键作用。

### 创新总结

GPHLVM 的创新可概括为三个 **changed slots** 的协同作用：双曲几何提供层次结构的归纳偏置，图先验（应力损失+反向约束）提供显式的拓扑监督，而双曲核与黎曼优化则保证整个概率框架在非欧流形上的数学一致性。三者缺一不可——纯双曲嵌入缺乏结构约束，纯图正则化缺乏几何适配，而两者的结合使得离散分类学与连续运动生成之间的鸿沟得以弥合。

GPHLVM 的整体框架围绕一个核心思想展开：**将离散的运动分类学图嵌入到连续的双曲潜在空间中，并利用高斯过程建立从潜在空间到观测空间的生成映射**。这一框架通过四个关键组件的协同工作，实现了分类学层次结构的忠实保留与高质量运动生成。

### 输入与输出

**输入**由两部分组成：
1. **运动观测数据** $\mathbf{Y} \in \mathbb{R}^{N \times D}$：$N$ 个运动姿态，每个姿态为 $D$ 维向量（如关节角度或位置）。
2. **分类学图** $\mathbb{G}$：一个有向无环图，节点 $c_i$ 代表运动类别，边编码类别间的层次关系。图中节点间的最短路径距离 $\text{dist}_{\mathbb{G}}(c_i, c_j)$ 作为监督信号。

**输出**为：
1. **潜在嵌入** $\mathbf{X} = \{\mathbf{x}_n \in \mathcal{L}^Q\}_{n=1}^N$：每个训练姿态在 $Q$ 维双曲洛伦茨流形上的坐标。
2. **生成映射**：从任意潜在点 $\mathbf{x}^* \in \mathcal{L}^Q$ 到观测空间 $\mathbf{y}^*$ 的高斯过程回归函数，支持新姿态生成与运动插值。

### 核心模块与数据流

整个 pipeline 由以下模块串联构成，数据流从分类学图和观测数据出发，经过双曲嵌入学习、图结构正则化、再到生成映射训练，最终输出可插值的连续潜在空间：

```
分类学图 G + 观测数据 Y
        │
        ▼
┌─────────────────────────────┐
│  1. 双曲潜在空间 (L^Q)      │  ← 指数增长距离，自然适配树状层次
│     洛伦茨模型              │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  2. 双曲热核 (GP 核)        │  ← 在流形上定义点间相似性
│     Q=2: MC 近似 (Eq.4-6)   │
│     Q=3: 闭式解             │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  3. 图结构正则化            │  ← 强制嵌入距离匹配图距离
│     应力损失 (Eq.11)        │
│     反向约束映射 (Eq.12)    │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  4. 黎曼优化                │  ← 约束参数更新在流形上
│     Riemannian Adam         │
└─────────────────────────────┘
        │
        ▼
   潜在嵌入 X + 生成映射 f
        │
        ▼
   测地线插值 → 连续运动序列
```

### 模块间关系与因果机制

**模块 1 → 模块 2**：潜在空间选择双曲洛伦茨模型 $\mathcal{L}^Q$ 而非欧氏空间，是整个方法有效性的根基。双曲流形上距离呈指数增长、最短路径（测地线）趋向通过原点，这一几何特性恰好对应树状分类学中"根节点附近分叉、叶节点间距离远"的结构。若替换为欧氏空间（即标准 GPLVM），这种层次距离关系无法被有效编码——Table 1 显示欧氏模型的应力值显著更高。

**模块 2 → 模块 3**：双曲热核 $k^{\mathcal{L}^Q}$ 定义了潜在点之间的 GP 协方差，是生成映射的基石。但仅靠核函数本身无法保证嵌入自动反映分类图结构——消融实验表明，无正则化的纯 GPHLVM（vanilla）嵌入无法编码有意义的图距离（Fig. 2a, 3a, 11a）。因此模块 3 通过两个互补机制注入图结构先验：
- **应力损失** $\ell_{\text{stress}}$ 直接惩罚嵌入测地距离与图最短路径距离之间的差异，强制全局拓扑保持。
- **反向约束映射**将潜在变量定义为观测数据核与图核乘积的函数，使新数据嵌入后局部与全局结构同时得以保持。

两者叠加（BC+stress）在三个分类学上均取得最低应力值（Table 1），验证了图先验的必要性。

**模块 4 贯穿全程**：由于潜在变量和核参数定义在非欧流形上，标准梯度下降不再适用。Riemannian Adam 通过指数映射 $\text{Exp}_{\mathbf{x}_t}$ 将更新投影回流形，通过平行传输 $\mathcal{P}_{\mathbf{x}_t \to \mathbf{x}_{t+1}}$ 保持动量张量的几何一致性，确保整个优化过程始终在双曲流形上进行。

### 训练与推理流程

**训练阶段**：对于小数据集（本文实验约 100 个姿态），采用最大后验估计，优化目标为：
$$\ell_{\text{MAP}} = \log p(\mathbf{Y}|\mathbf{X}) + \log p(\mathbf{X}) - \gamma \cdot \ell_{\text{stress}}(\mathbf{X})$$
其中 $p(\mathbf{X})$ 为双曲包裹高斯先验，$\gamma$ 控制图正则化强度。对于大数据集，可切换为变分推断，通过最大化 ELBO 进行训练。

**推理与生成**：训练完成后，给定两个分类节点对应的潜在嵌入 $\mathbf{x}_A$ 和 $\mathbf{x}_B$，沿双曲测地线均匀采样中间点，再通过 GP 后验均值映射回观测空间，即可生成平滑的连续运动过渡。Table 11 显示，这种测地线插值生成的运动急动度（jerkiness）仅为欧氏线性插值的约 8%，平滑度提升约 92%。

### 计算代价与权衡

框架的主要计算瓶颈在于 **2 维双曲热核**：$\mathcal{L}^2$ 上的核没有闭式解，需通过蒙特卡洛采样近似（Eq. 4-6），导致训练时间从欧氏模型的约 3 秒激增至约 415 秒（Table 2）。相比之下，$\mathcal{L}^3$ 上的核具有闭式解，计算代价显著更低。这一权衡意味着：追求最佳可视化效果（2D 嵌入）需付出高昂的计算代价；若优先计算效率，3 维双曲空间是更务实的选择。

![[assets/figures/papers/paper_list_l1910_GPHLVM_Bringing_Motion_Taxonomies_to_Continuous_Domains_via_GPLVM_on_Hyp/figures/019_Table_2.jpg]]
*Table 2: In order to show the computational cost of our approach, we ran a set of experiments to measure the average runtime for the training and decoding phases, using 2 and 3-dimensional latent spaces. As a reference, we added the runtime measurements of Euclidean counterpart, that is, the vanilla GPLVM. Table 2 shows the runtime measurements. Note that the main computational burden arises in our GPLHVM with a 2-dimensional latent space, which is in sharp contrast with the experiments using a 3-dimensional latent space. This increase in computational cost is mainly attributed to the 2-dimensional hyperbolic kernel. Nevertheless, we also measured the computational cost of evaluating the kernel and...*

### 1. 双曲潜在空间与包裹高斯先验

GPHLVM 将标准 GPLVM 的潜在空间从欧氏空间 $\mathbb{R}^Q$ 推广到双曲洛伦茨模型 $\mathcal{L}^Q$。这一几何选择的因果逻辑在于：双曲流形上的距离呈指数增长，最短路径（测地线）趋向通过原点，恰好对应连续的层次结构。因此，将潜在变量定义在双曲流形上，为嵌入分类学的树状拓扑提供了天然的归纳偏置。

潜在变量 $\pmb{x}$ 的先验分布采用双曲包裹高斯分布 $\mathcal{N}_{\mathcal{L}^Q}(\pmb{\mu}_0, \alpha \mathcal{I})$，其对数概率密度函数为：

$$
\log \mathcal{N}_{\mathcal{L}^d}(\pmb{x}; \pmb{\mu}, \pmb{\Sigma}) = \log \mathcal{N}(\pmb{v}; \mathbf{0}, \pmb{\Sigma}) - (d-1) \log\left( \sinh(\|\pmb{u}\|_c) / \|\pmb{u}\|_c \right)
$$

该分布的构造逻辑为：（1）在均值点 $\pmb{\mu}$ 的切空间中采样一个欧氏高斯变量；（2）通过平行传输将其映射到原点切空间；（3）利用指数映射 $\mathrm{Exp}_{\pmb{\mu}_0}$ 将切向量投影回流形表面。式中 $\pmb{v}$ 为切空间中的高斯样本，$\pmb{u}$ 为平行传输后的切向量，$\|\pmb{u}\|_c$ 为洛伦茨范数，第二项为体积膨胀的 Jacobian 修正项。

### 2. 双曲热核与高斯过程映射

GPHLVM 的生成映射从双曲潜在空间 $\mathcal{L}^Q$ 到观测空间 $\mathbb{R}^D$ 基于独立的高斯过程：

$$
y_{n,d} \sim \mathcal{N}(y_{n,d}; f_{n,d}, \sigma_d^2), \quad f_{n,d} \sim \mathrm{GP}(m_d(\pmb{x}_n), k_d^{\mathcal{L}^Q}(\pmb{x}_n, \pmb{x}_n)), \quad \pmb{x}_n \sim \mathcal{N}_{\mathcal{L}^Q}(\pmb{\mu}_0, \alpha \mathcal{I})
$$

其中 $k_d^{\mathcal{L}^Q}$ 为定义在双曲流形上的核函数。该核基于热方程解（heat kernel）构建，可视为欧氏平方指数核在双曲几何下的推广。对于 $Q=3$ 维双曲空间，存在闭式解：

$$
k^{\mathcal{L}^3}(\pmb{x}, \pmb{x}') = \frac{\sigma^2}{C_\infty} \frac{\rho}{\sinh \rho} e^{-\rho^2/(2\kappa^2)}
$$

其中 $\rho = \mathrm{dist}_{\mathcal{L}^3}(\pmb{x}, \pmb{x}')$ 为两点间测地距离，$\kappa$ 为长度尺度参数，$C_\infty$ 为归一化常数。

对于 $Q=2$ 维双曲空间（洛伦茨平面），热核仅有积分形式，无已知闭式解：

$$
k^{\mathcal{L}^2}(\pmb{x}, \pmb{x}') = \frac{\sigma^2}{C_\infty} \int_{\rho}^{\infty} \frac{s e^{-s^2/(2\kappa^2)}}{(\cosh(s) - \cosh(\rho))^{1/2}} \mathrm{d}s
$$

为解决该积分的计算问题，论文采用了一种保证正定的蒙特卡洛近似方法：将积分重写为内积形式后，从特定分布中采样 $s$ 和辅助变量 $b$，得到可微且正定的核估计：

$$
k^{\mathcal{L}^2}(\pmb{x}, \pmb{x}') \approx \frac{\sigma^2}{C_\infty'} \frac{1}{L} \sum_{l=1}^{L} s_l \tanh(\pi s_l) \overline{w} \overline{w}
$$

该近似是二维 GPHLVM 计算开销的主要瓶颈——每次核评估需对 $L$ 个蒙特卡洛样本求和，导致训练时间远超对应的欧氏模型（约 414s vs 3s，见 Table 2）。

### 3. 黎曼优化

由于潜在变量和部分超参数定义在双曲流形上，标准欧氏梯度下降不再适用。GPHLVM 采用黎曼优化方法（Riemannian Adam），其通用更新步骤为：

$$
\eta_t \leftarrow h(\mathrm{grad}\ \ell(\pmb{x}_t), \tau_{t-1}), \quad \pmb{x}_{t+1} \leftarrow \mathrm{Exp}_{\pmb{x}_t}(-\alpha_t \eta_t), \quad \tau_t \leftarrow P_{\pmb{x}_t \to \pmb{x}_{t+1}}(\eta_t)
$$

其中 $\mathrm{grad}\ \ell(\pmb{x}_t)$ 为目标函数在流形上的黎曼梯度，$\mathrm{Exp}_{\pmb{x}_t}$ 为指数映射（将切向量沿测地线投影回流形），$P_{\pmb{x}_t \to \pmb{x}_{t+1}}$ 为平行传输（将动量向量沿流形搬运至新点）。这一机制确保参数更新始终位于双曲流形上，保持几何一致性。

对于小数据集，GPHLVM 可通过最大化对数后验（MAP）训练：

$$
\ell_{\mathrm{MAP}} = \log\big(p(\mathcal{Y} | \mathcal{X}) p(\mathcal{X})\big)
$$

对于大数据集，则采用变分推断，引入双曲包裹正态变分后验 $q_\phi(\pmb{X}) = \prod_{n=1}^{N} \mathcal{N}_{\mathcal{L}^Q}(\pmb{x}_n; \pmb{\mu}_n, \pmb{\Sigma}_n)$，最大化证据下界（ELBO）：

$$
\log p(\pmb{Y}) \ge \mathbb{E}_{q_\phi(\pmb{X})} \left[ \log p(\pmb{Y} | \pmb{X}) \right] - \mathrm{KL}\big(q_\phi(\pmb{X}) || p(\pmb{X})\big)
$$

### 4. 图结构保持正则化

仅靠双曲几何的归纳偏置不足以在潜在空间中忠实地编码分类学图结构（消融实验中无正则化的 vanilla GPHLVM 无法捕获有意义的图距离，见 Fig. 2a, 3a, 11a）。论文引入两个互补机制：

**应力损失（Stress Loss）** 作为图距离保持先验，直接惩罚嵌入间测地距离与分类图最短路径距离的差异：

$$
\ell_{\mathrm{stress}}(\pmb{X}) = \sum_{i < j} \big( \mathrm{dist}_{\mathbb{G}}(c_i, c_j) - \mathrm{dist}_{\mathcal{L}^Q}(\pmb{x}_i, \pmb{x}_j) \big)^2
$$

其中 $\mathrm{dist}_{\mathbb{G}}(c_i, c_j)$ 为分类图中节点 $c_i$ 与 $c_j$ 的最短路径距离，$\mathrm{dist}_{\mathcal{L}^Q}(\pmb{x}_i, \pmb{x}_j)$ 为对应嵌入点间的双曲测地距离。该损失作为正则项加入训练目标，强制全局图拓扑在嵌入空间中得以保留。定量结果表明，仅添加应力先验即可使嵌入的测地距离与图距离高度一致（Table 1, Stress 列）。

**图距离保持反向约束（Back-constraints）** 将潜在变量定义为观测数据与图节点相似性的函数：

$$
\pmb{x}_n = \mathrm{Exp}_{\pmb{\mu}_0}(\tilde{\pmb{x}}_n), \quad \tilde{x}_{n,q} = \sum_{m=1}^{N} w_{q,m} k^{\mathbb{R}^D}(\pmb{y}_n, \pmb{y}_m) k^{\mathbb{G}}(c_n, c_m)
$$

其中 $k^{\mathbb{R}^D}$ 为观测空间的欧氏核（捕获姿态相似性），$k^{\mathbb{G}}$ 为图核（捕获节点在分类学中的关系），$w_{q,m}$ 为可学习权重，$\mathrm{Exp}_{\pmb{\mu}_0}$ 将切空间映射回双曲流形。该约束使新数据嵌入后既能保持局部结构（通过观测核），又能保持全局图结构（通过图核），实现了在类别内部基于姿态相似性组织嵌入的同时不破坏全局拓扑。

消融实验表明，应力先验与反向约束具有互补作用：应力先验保证全局图距离结构，反向约束进一步在类别内部建立有意义的局部组织（Fig. 2c, 3c, 11c；Table 1 BC+Stress 列）。值得注意的是，采用曲损（distortion）损失替代应力损失进行正则化的尝试未能成功编码图距离（App. F, Fig. 8），说明应力损失的平方形式对图结构保持至关重要。

## 实验与关键发现

### 核心性能：双曲嵌入对分类学结构的忠实保持

GPHLVM 的核心优势在于其双曲潜在空间能够自然地编码运动分类学的层次结构。这一优势通过**应力（Stress）**指标进行量化，该指标直接度量嵌入点之间的测地距离与分类图节点间最短路径距离的偏差，数值越低表示嵌入对图拓扑结构的保持越好。

Table 1 展示了在三种运动分类学上的应力对比。在双手抓握分类学（Hand Grasps Taxonomy, Stival et al., 2019）上，配备反向约束和应力先验的 GPHLVM（L² BC+stress）取得了 **0.14±0.16** 的应力值，而同等配置的欧氏 GPLVM（R² BC+stress）为 0.39±0.41，双曲模型将应力降低了约 64%。在全身支撑姿态分类学（Whole-body Support Poses Taxonomy, Borras et al., 2017）上，GPHLVM 同样优于欧氏模型（0.53 vs 0.63），但由于该分类学显式区分了左右侧接触，导致部分差异较大的姿态被归入同一节点，增加了嵌入难度，因此改进幅度相对较小。

值得注意的是，**无正则化的纯 GPHLVM 无法在潜在空间中编码有意义的分类图距离结构**（Fig. 2a, 3a, 11a），其嵌入点呈散乱分布，应力值极高。这表明仅靠双曲几何的归纳偏置不足以自动捕捉图结构，必须辅以显式的图先验。

### 消融分析：图先验的增量贡献

通过逐步添加正则化组件，可以清晰看到各模块的增量贡献：

1. **仅应力先验（Stress only）**：在双曲潜在空间中添加图距离保持的应力损失（Eq. 11）后，嵌入的测地距离与图的节点间最短路径距离呈现高度一致性。Table 1 中，GPHLVM L² stress 的应力值已显著低于无正则化版本，证明应力损失能够有效强制全局图结构的保持。

2. **加入反向约束（BC+stress）**：进一步引入基于图核与观测核乘积的反向约束映射（Eq. 12）后，模型能够在保持全局图结构的同时，根据观测数据的相似性在类别内部组织嵌入。从 Fig. 2c, 3c, 11c 的嵌入可视化可以看出，BC+stress 配置下的嵌入不仅保持了正确的类别间拓扑关系，还在类别内部形成了更紧凑、语义一致的聚类。

3. **曲损损失（Distortion loss）失效**：实验还尝试了用曲损损失替代应力损失进行正则化，但该方案在所有实验中均未能成功编码图距离（App. F, Fig. 8）。这表明应力损失所采用的逐对距离匹配策略对于层次结构的编码更为有效。

![[assets/figures/papers/paper_list_l1910_GPHLVM_Bringing_Motion_Taxonomies_to_Continuous_Domains_via_GPLVM_on_Hyp/figures/011_Figure_8.jpg]]
*Figure 8: Embeddings learned with distortion regularization. (a) and (b) display the latent embeddings alongside distance matrices after training our GPHLVM model with an added distortion loss*

### 与生成模型的对比：VAE 的局限性

Table 13 全面比较了 GPHLVM、GPLVM 以及欧氏/双曲 VAE 在三个分类学上的应力与重建误差。结果显示，**无论是欧氏 VAE 还是双曲 VAE，其应力值均显著高于 GPHLVM**。根本原因在于 VAE 的 KL 正则化项的目标是将潜在编码拉向先验分布，这与保持图距离的目标存在根本性冲突——VAE 倾向于将不同类别的嵌入在潜在空间中分离，而非按照层次距离进行组织。Fig. 20-22 的 VAE 嵌入可视化也直观证实了这一点：VAE 的嵌入虽然能形成聚类，但类别间的距离关系与分类图的结构严重不符。

![[assets/figures/papers/paper_list_l1910_GPHLVM_Bringing_Motion_Taxonomies_to_Continuous_Domains_via_GPLVM_on_Hyp/figures/040_Table_13.jpg]]
*Table 13: Average stress and reconstruction error per model, geometry, and regularization*

### 运动生成质量：测地线插值的平滑性优势

GPHLVM 的另一项关键能力是利用双曲潜在空间的测地线插值生成平滑的运动过渡。Table 11 展示了不同模型生成运动的**急动度（Jerkiness）**对比——急动度越低，运动越平滑。在双手抓握分类学上，GPHLVM L² 的急动度为 **108.65±140.54**，而欧氏 GPLVM R² 的急动度高达 1377.05±1721.44，双曲模型将急动度降低了约 92%。

这一巨大差异的几何根源在于：欧氏空间中的线性插值路径会穿越潜在空间的低密度区域，导致生成的运动出现剧烈抖动；而双曲流形上的测地线自然趋向通过原点（对应连续层次结构的根节点），使得插值路径始终经过高概率密度区域，从而产生平滑、真实感强的过渡（Fig. 4, Fig. 15-19）。

![[assets/figures/papers/paper_list_l1910_GPHLVM_Bringing_Motion_Taxonomies_to_Continuous_Domains_via_GPLVM_on_Hyp/figures/006_Figure_4.jpg]]
*Figure 4: Motions obtained via geodesic interpolation in the backconstrained GPHLVM latent space. Top: Grasp taxonomy from ring (Ri) to index finger extension (IE). Bottom: Support pose taxonomy from LFRH to K2RH. Gray circles denote contacts*

### 计算成本与可扩展性

Table 2 和 Table 9 揭示了 GPHLVM 的计算瓶颈。在 2 维双曲潜在空间中，由于热核缺乏闭式解，必须依赖蒙特卡洛采样近似（Eq. 4-6），导致训练时间显著增加：GPHLVM L² 的平均训练时间约 **414.67 秒**，而对应的欧氏 GPLVM R² 仅需约 **2.98 秒**，差距约 140 倍。相比之下，3 维双曲核具有闭式解，计算开销大幅降低，但仍高于欧氏模型。这一计算瓶颈限制了 GPHLVM 在更大规模数据上的实时应用，是当前方法最突出的局限性。

![[assets/figures/papers/paper_list_l1910_GPHLVM_Bringing_Motion_Taxonomies_to_Continuous_Domains_via_GPLVM_on_Hyp/figures/005_Table_2.jpg]]
*Table 2: Average runtime for training and decoding phases over 10 experiments of the hand grasps taxonomy. Training time was measured over 500 iterations for both models. The implementations are fully developed on Python, and the runtime measurements were taken using a standard laptop with 32 GB RAM, Intel Xeon CPU E3-1505M v6 processor, and Ubuntu 20.04 LTS*

### 低数据量下的优势：与 VPoser 的对比

在与 **VPoser**（Pavlakos et al., 2019）的比较中，GPHLVM 展现出在低数据量条件下的独特优势。VPoser 是在约 100 万条全身运动捕捉数据上训练的大规模 VAE 人体姿态先验模型，而 GPHLVM 仅在约 100 个静态姿态上训练。尽管数据量差距悬殊，GPHLVM 通过显式注入分类学图先验和利用测地线插值，仍能生成与 VPoser 可比较的运动质量。这一结果说明，**当领域知识以结构化分类学的形式可用时，将其作为先验注入模型可以有效弥补数据量的不足**。

### 失败模式与注意事项

1. **分类学歧义导致嵌入失败**：在全身支撑姿态分类学中，若不显式区分左右侧接触，差异极大的姿态可能被归入同一分类节点，导致嵌入空间中出现不合理的插值结果。这一发现强调了分类学设计质量对模型性能的决定性影响。

2. **物理可行性未建模**：模型未引入任何物理约束或接触力建模，生成的插值轨迹可能违反物理可行性（如穿越物体、关节超限等）。这是当前方法的一个重要局限，也是未来工作的方向。

3. **黎曼度量 GPLVM 的失败**：实验还评估了学习黎曼度量的 GPLVM（Tosi et al., 2014），其潜在空间和距离误差矩阵（Fig. 23）显示，没有显式分类学先验的模型完全无法捕捉层次图结构，进一步印证了显式图先验的必要性。

![[assets/figures/papers/paper_list_l1910_GPHLVM_Bringing_Motion_Taxonomies_to_Continuous_Domains_via_GPLVM_on_Hyp/figures/047_Figure_23.jpg]]
*Figure 23: Embeddings of taxonomy data on learned manifolds: The first row shows the latent spaces of the GPLVM. The background color is proportional to volume of the learned Riemannian metric. The second row displays the error matrix between the geodesic and taxonomy graph distances*

## 定位与知识库关联

### 1. 方法沿革与基线关系

GPHLVM 的核心谱系可追溯至两条独立的技术路线：**高斯过程潜在变量模型（GPLVM）**和**双曲表示学习**。

**上游继承：从 GPLVM 到双曲推广。** 标准 GPLVM（Lawrence, NIPS 2003; Titsias & Lawrence, AISTATS 2010）将高维观测数据映射到低维欧氏潜在空间，通过高斯过程建模从潜在变量到观测空间的生成映射。GPHLVM 在此基础上进行了三个关键改造：（1）将潜在空间从欧氏空间 $\mathbb{R}^Q$ 替换为洛伦茨双曲模型 $\mathcal{L}^Q$；（2）将潜在变量先验从标准高斯 $\mathcal{N}(\mathbf{0}, \pmb{I})$ 替换为双曲包裹高斯 $\mathcal{N}_{\mathcal{L}^Q}(\pmb{\mu}_0, \alpha \mathcal{I})$；（3）将核函数从欧氏平方指数核替换为基于热方程解的双曲核（2D 时采用保证正定的蒙特卡洛近似，3D 具有闭式解）。这些改造的理论动机在于：双曲流形上的距离呈指数增长，最短路径趋向通过原点，这一几何特性恰好对应连续的层次结构，使得双曲空间成为编码分类学树状拓扑的自然载体。

**并行对比：双曲 VAE。** 与 GPHLVM 并行的方法是将变分自编码器（VAE）的潜在空间推广到双曲流形，即双曲 VAE。该方法的生成映射由神经网络参数化，而非高斯过程。实验表明（Table 13），双曲 VAE 在应力指标上显著劣于 GPHLVM：VAE 的 KL 正则化项倾向于将嵌入点拉向先验中心，这与保持分类图节点间距离的目标产生冲突。相比之下，GPHLVM 的图距离应力先验直接优化嵌入间测地距离与分类图最短路径距离的一致性，在目标函数层面与结构保持目标一致。

**下游参照：VPoser。** VPoser（Pavlakos et al., 2019）是在约 1M 全运动轨迹数据上训练的 VAE 人体姿态先验模型。GPHLVM 仅在约 100 个静态姿态上训练，通过注入分类学图结构先验和利用双曲测地线插值，在运动生成平滑度（急动度）上达到了可比较的质量。这一对比揭示了 GPHLVM 的核心优势：**在低数据量条件下，显式的层次结构先验可以弥补数据规模的不足**。

**已探索的替代方案。** 论文还测试了以下变体，均未成功：（1）使用曲损（distortion）损失替代应力损失进行正则化，未能编码图距离（App. F, Fig. 8）；（2）学习黎曼度量的 GPLVM（Tosi et al., 2014）在没有显式分类学先验的情况下，无法捕捉层次图结构（Fig. 23）。

### 2. 适用边界

**适用场景。** GPHLVM 最适合以下条件同时满足的情形：
- 数据具有已知的离散层次分类结构（如运动分类学、本体论树）；
- 训练数据量较小（数十到数百个样本），无法支撑大规模生成模型的训练；
- 需要在连续嵌入空间中保留分类图的拓扑距离，并利用测地线插值生成平滑过渡。

**不适用或需谨慎使用的场景：**
- **大规模分类学数据。** 2D 双曲核依赖蒙特卡洛采样，GPHLVM（$\mathcal{L}^2$）的训练时间约 414.67s，而对应的欧氏 GPLVM（$\mathbb{R}^2$）仅需约 2.98s（Table 2），计算开销差距约 140 倍。3D 双曲核虽有闭式解，但维度增加会引入其他挑战。
- **缺乏明确层次结构的数据。** 若数据不具备树状拓扑，双曲几何的指数增长距离特性可能成为误导性归纳偏置。
- **需要物理可行性保证的运动生成。** GPHLVM 未引入任何物理约束或接触力建模，生成的插值轨迹可能违反物理可行性（如穿越物体、关节超限等）。

### 3. 核心局限

**计算瓶颈。** 2D 双曲热核缺乏闭式解，需通过蒙特卡洛采样近似，且为保证正定性需从特定分布采样并重写为内积形式。这导致 $\mathcal{L}^2$ 模型的计算成本远超对应的欧氏模型和 $\mathcal{L}^3$ 模型，限制了在高维或大规模分类学上的应用。

**数据规模验证不足。** 当前实验使用的三个分类学数据集规模均较小（约 100 个姿态），模型在大规模分类学（如包含数千节点的完整运动本体论）上的扩展性和嵌入质量尚待验证。

**分类学图假设过强。** 模型将分类学图视为确定且正确的先验，而实际中分类层次可能存在主观性、遗漏或错误。模型未对图结构的不确定性进行建模，对噪声或部分错误的图结构缺乏鲁棒性。

**超参数选择的经验性。** 应力损失权重 $\gamma$ 等关键超参数的选择仍是经验性的。由于双曲核计算代价高昂，训练超参数搜索的范围可能受限，最优配置可能未被充分探索。

**物理可行性缺失。** 生成的插值运动未经过物理约束（如接触稳定性、关节限位、碰撞检测）的验证，在机器人执行或动画生成中可能需要后处理或额外的物理过滤。

### 4. 开放问题

1. **高效双曲核设计。** 如何设计更高效的采样策略或近似方法，以显著降低双曲热核的计算成本，使 GPHLVM 适应高维或大规模分类学数据？可能的路径包括稀疏 GP 近似、随机傅里叶特征的双曲推广、或预计算核矩阵的缓存策略。

2. **物理约束融合。** 在生成运动时，如何将物理约束、接触稳定性或动态可行性自然地融入潜在空间与插值过程中？可能的方案包括在测地线插值上施加约束优化、或在解码器输出端添加物理损失项。

3. **鲁棒图先验。** 对于不完全、含噪声或动态演变的分类学图，如何调整图先验（例如通过自适应权重、概率图模型、或图结构学习）来保持嵌入的鲁棒性？这涉及到将图结构本身从固定输入转变为可优化的变量。

4. **下游任务拓展。** 是否可以利用双曲嵌入的非欧几何特性进行其他下游任务，例如运动规划（利用测地线作为自然路径）、模仿学习（在双曲潜在空间中进行策略表示）、或跨域迁移（利用层次结构的共享表示）？

5. **主动学习与不确定性估计。** 能否结合 GP 的不确定性估计，在嵌入空间中识别当前分类学覆盖不足的区域，并指导新姿态/新类别的采集？这可以将 GPHLVM 从被动嵌入工具升级为主动数据采集策略的核心组件。

6. **与大规模预训练模型的协同。** GPHLVM 在低数据量下表现优异，而 VPoser 等模型受益于大规模预训练。如何将两者结合——例如用 GPHLVM 的结构先验指导大规模模型的微调，或用大规模模型的表示初始化 GPHLVM 的观测空间——是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/ICML_2024/GPHLVM_Bringing_Motion_Taxonomies_to_Continuous_Domains_via_GPLVM_on_Hyperbolic_Manifolds.pdf]]
