---
title: "AlignFlow: Improving Flow-based Generative Models with Semi-Discrete Optimal Transport"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AlignFlow_Improving_Flow_based_Generative_Models_with_Semi_Discrete_Optimal_Transport.pdf
aliases:
- AlignFlow
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "AlignFlow precomputes a semi-discrete optimal transport map that deterministically pairs continuous noise samples with discrete training data points."
primary_logic: "It partitions noise space into Laguerre cells, uses the resulting noise-data alignment in flow-model training, and optionally rebalances imperfect assignments."
claims:
- "SDOT is well matched to finite empirical data and continuous noise distributions."
- "The deterministic full-dataset map avoids minibatch OT bias and batch-size dependence."
- "The note reports consistent FID improvements with less than one percent extra training time."
---

# AlignFlow: Improving Flow-based Generative Models with Semi-Discrete Optimal Transport

> [!tip] 核心洞察
> 由于训练数据有限（离散经验分布），而噪声分布是连续的，因此SDOT天然适用于此场景。SDOT映射具有确定性、批大小不变性、可证明收敛性，且计算开销极低（<1%），可作为即插即用模块无缝集成到现有FGM中，通过提供更直的流轨迹来提升性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AlignFlow：利用半离散最优传输改进基于流的生成模型 |
| 英文题名 | AlignFlow: Improving Flow-based Generative Models with Semi-Discrete Optimal Transport |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=nTCF3QNsIN); [GitHub](https://github.com/konglk1203/AlignFlow) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | AlignFlow |
| Dataset | CIFAR-10 (U-Net), ImageNet256 (DiT-B/2, Shortcut Model) |

> [!tip] 效果简介
> - CIFAR-10 (U-Net) 上，FID-50k (Euler 100步) 为 4.72，对比 4.80 (Minibatch OT)，变化 -0.08。
> - CIFAR-10 (U-Net) 上，FID-50k (Euler 1000步) 为 3.79，对比 3.92 (Minibatch OT)，变化 -0.13。
> - CIFAR-10 (U-Net) 上，FID-50k (DOPRI5) 为 3.71，对比 3.82 (Minibatch OT)，变化 -0.11。

## 概述

AlignFlow 是一种即插即用的噪声-数据对齐（Noise-Data Alignment, NDA）方法，旨在提升基于流的生成模型（Flow-based Generative Models, FGM）的性能。其核心思想是利用半离散最优传输（Semi-Discrete Optimal Transport, SDOT）在连续的噪声分布与离散的经验数据分布之间显式构造一个确定性的、最优的传输映射。该映射将噪声空间划分为 Laguerre 单元，每个单元对应一个数据点，从而为 FGM 训练提供固定的、最优的噪声-数据配对。AlignFlow 以极低的计算开销（<1%额外训练时间）实现了对现有 FGM 的即插即用改进，在 CIFAR-10 和 ImageNet256 等多个基准上取得了一致的性能提升。

## 背景与动机

基于流的生成模型通过学习从噪声分布到数据分布的连续可逆变换来生成数据。训练 FGM 时，噪声与数据的配对方式对生成质量有显著影响。现有方法主要分为三类：

- **独立采样（Vanilla Flow Matching）**：噪声与数据独立采样，导致随机配对，生成轨迹弯曲，需要更多函数评估（NFE）。
- **离散最优传输（Minibatch OT）**：在小批量内使用 Sinkhorn 算法计算噪声与数据的 OT 计划。该方法受限于小批量样本，导致有偏或错误的传输计划，且受维度灾难影响。
- **连续最优传输（ICNN-based OT）**：使用输入凸神经网络（ICNN）近似 Brenier 势能。该方法缺乏收敛保证，且计算开销较大。

现有 OT 方法在扩展到大规模模型和高维数据时面临严峻挑战。离散 OT 方法需要从两个分布中采样，其估计误差随维度指数增长；连续 OT 方法则难以保证收敛到全局最优解。

## 核心创新

AlignFlow 的核心创新在于利用半离散最优传输（SDOT）解决上述瓶颈。其关键洞察在于：训练数据是有限的离散经验分布，而噪声分布是连续的，因此 SDOT 天然适用于此场景。SDOT 映射具有以下关键特性：

1. **确定性**：每个噪声样本一致地匹配到固定数据点，与批大小无关，消除了随机性。
2. **批大小不变性**：SDOT 映射在整个数据集上计算，不依赖于小批量样本，确保稳定收敛。
3. **可证明收敛性**：SDOT 目标函数是凸的，优化过程具有收敛保证。
4. **极低计算开销**：SDOT 映射的计算开销不到总训练时间的 1%（CIFAR-10），在 ImageNet 上每类少于 10 秒。

## 整体框架

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_nTCF3QNsIN_AlignFlo/figures/002_Figure_1.jpg]]

AlignFlow 采用两阶段训练流程：

**阶段1：SDOT 映射计算**（Algorithm 2）
- 输入：噪声分布 p₀，经验数据分布 p₁ = Σᵢ bᵢ δ_{x₁ⁱ}（bᵢ = 1/|I|）
- 优化对偶权重 g，将噪声空间划分为 Laguerre 单元
- 输出：SDOT 映射 φ(x₀; g) = argminᵢ [c(x₀, x₁ⁱ) - gᵢ]

**阶段2：FGM 训练**（Algorithm 3）
- 使用预计算的 SDOT 映射配对噪声与数据
- 训练任意 FGM（如 Flow Matching, Shortcut Model, MeanFlow）
- 可选：当 SDOT 映射未完全收敛时，执行 Rebalance 操作消除偏差

## 核心模块与公式推导

### 5.1 标准 FGM 损失函数

独立采样时，FGM 训练损失为：

$$\mathcal{L}(\theta) = \mathbb{E}_{t\sim\mathrm{Unif}[0,1], x_0\sim p_0, x_1\sim p_1} \|u(x_t, t; \theta) - \mathrm{TargetVectorField}(x_0, x_1)\|_p^p \quad \text{(Eq. 1)}$$

使用耦合 γ 时，损失函数变为：

$$\mathcal{L}_\gamma(\theta) = \mathbb{E}_{t\sim\mathrm{Unif}[0,1], (x_0,x_1)\sim\gamma} \|u(x_t, t; \theta) - \mathrm{TargetVectorField}(x_0, x_1)\|_p^p \quad \text{(Eq. 2)}$$

### 5.2 最优传输问题

标准 OT 问题定义为：

$$\gamma_* := \arg\min_{\gamma\in\Gamma(q_1,q_2)} \left( \int_{\mathcal{X}\times\mathcal{X}} c(y_1, y_2) \, \mathbf{d}\gamma(y_1, y_2) \right) \quad \text{(Eq. 4)}$$

### 5.3 SDOT 映射与 Laguerre 单元

SDOT 映射将噪声点 x₀ 映射到具有最小调整成本的数据点索引：

$$\varphi(x_0; \mathbf{g}) := \arg\min_{i\in I} \, c(x_0, x_1^i) - g_i \quad \text{(Eq. 5)}$$

对应的 Laguerre 单元定义为：

$$\mathsf{L}_i(\mathbf{g}) := \{x \in \mathcal{X} : c(x, y_i) - g_i \leq c(x, y_j) - g_j, \forall j\} \quad \text{(Eq. 6)}$$

### 5.4 SDOT 对偶目标函数

SDOT 的对偶目标函数为：

$$E(\mathbf{g}) := \sum_{i\in I} \int_{\mathsf{L}_i(\mathbf{g})} (c(x, y_i) - g_i) \, dp_0(x) + \langle \mathbf{g}, \mathbf{b} \rangle \quad \text{(Eq. 7)}$$

其梯度为：

$$\nabla E(\mathbf{g})_i = -\int_{\mathsf{L}_i(\mathbf{g})} dp_0 + b_i \quad \text{(Section 3.3)}$$

### 5.5 质量评估指标

最大相对误差（MRE）用于评估 SDOT 映射质量：

$$\mathrm{MRE} = \max_{i\in I} \frac{|p_i - b_i|}{b_i} \quad \text{(Eq. 10)}$$

L1 距离为：

$$\mathrm{L}_1(\mathbf{g}) = \sum_{i\in I} |p_i - b_i| \quad \text{(Section B.1)}$$

### 5.6 Rebalance 操作

当 SDOT 映射未完全收敛时，通过最小扰动使数据点被均匀采样：

$$\mathrm{rebalance}\left(\{m_j\}_{j=1}^M\right) := \arg\max_{\{\tilde{m}_j\}} \left\{ \sum_j \mathbb{1}(\tilde{m}_j = m_j) : \left| \max_{i\in\mathcal{X}} \sum_{j=1}^M \mathbb{1}_i(\tilde{m}_j) - \min_{i\in\mathcal{X}} \sum_{j=1}^M \mathbb{1}_i(\tilde{m}_j) \right| \leq 1 \right\} \quad \text{(Eq. 12)}$$

## 实验与分析

### 6.1 主要结果

**CIFAR-10（U-Net）**：AlignFlow 在所有 ODE 积分器下均优于 Minibatch OT。

| 积分器 | Minibatch OT | AlignFlow | 改进 |
|--------|-------------|-----------|------|
| Euler 100步 | 4.80 | **4.72** | -0.08 |
| Euler 1000步 | 3.92 | **3.79** | -0.13 |
| DOPRI5 | 3.82 | **3.71** | -0.11 |

*Table 2: Comparison of FID-50k scores between Minibatch OT and AlignFlow for U-Net trained on CIFAR-10, evaluated across different ODE integrators. Results are averaged over 5 independent runs.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_nTCF3QNsIN_AlignFlo/figures/007_Table_2.jpg]]
*Table 2: Comparison of FID-50k scores between Minibatch OT and AlignFlow for U-Net trained on CIFAR-10, evaluated across different ODE integrators. Results are averaged over 5 independent runs. AlignFlow consistently achieves better performance than Minibatch OT under all tested ODE integrators.*

**ImageNet256（DiT-B/2, Shortcut Model）**：AlignFlow 在所有 NFE 配置下提升性能。

| NFE | Baseline | AlignFlow | 改进 |
|-----|----------|-----------|------|
| 4 | 33.11 | **30.31** | -2.80 |
| 1 | 46.65 | **43.92** | -2.73 |

*Table 3: Evaluation of AlignFlow on DiT-B/2 for ImageNet256 using FID-50k demonstrates consistent performance improvements across all tested NFE configurations.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_nTCF3QNsIN_AlignFlo/figures/008_Table_3.jpg]]
*Table 3: Evaluation of AlignFlow on DiT-B/2 for ImageNet256 using FID-50k demonstrates consistent performance improvements across all tested NFE configurations.*

**ImageNet256（MeanFlow, NFE=1）**：AlignFlow 在所有 SiT 模型大小下提升性能。

| 模型 | Baseline | AlignFlow | 改进 |
|------|----------|-----------|------|
| SiT-B/4 | 15.53 | **13.75** | -1.78 |
| SiT-B/2 | 6.17 | **5.60** | -0.57 |
| SiT-L/2 | 3.84 | **3.51** | -0.33 |
| SiT-XL/2 | 3.43 | **3.23** | -0.20 |

*Table 4: We evaluate AlignFlow on ImageNet256 using MeanFlow (NFE=1), showing consistent performance improvements across all model sizes.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_nTCF3QNsIN_AlignFlo/figures/009_Table_4.jpg]]
*Table 4: We evaluate AlignFlow on ImageNet256 using MeanFlow (NFE=1), showing consistent performance improvements across all model sizes.*

### 6.2 消融与分析

- **训练收敛加速**：Figure 2 显示 AlignFlow 在所有测试任务中均加速了训练收敛速度（FID 随训练步数下降更快）。
- **SDOT 映射收敛性**：在 CIFAR-10 上，Rebalance 操作后超过 85% 的数据分配保持不变，表明 SDOT 映射已充分收敛。
- **轨迹直线性**：Figure 3 显示在合成 Checkerboard 数据上，AlignFlow 生成比 Minibatch OT 和 Vanilla Flow Matching 更直的轨迹。
- **计算开销**：CIFAR-10 上 SDOT 映射计算耗时 8 分 30 秒（L40S GPU），不到 1% 额外训练时间；ImageNet 上每类少于 10 秒。

### 6.3 公平性说明

- 所有对比实验使用相同的超参数以确保公平比较。
- CIFAR-10 结果基于 5 次独立运行的平均值。
- ImageNet 实验使用官方或广泛认可的基线实现（Frans et al. 2025; Geng et al. 2025）。
- SDOT 映射计算在 FGM 训练之前完成，不干扰训练过程。

### 补充图表

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_nTCF3QNsIN_AlignFlo/figures/001_Table_1.jpg]]
*Table 1: A comparison between coupling methods and AlignFlow, a Noise-Data Alignment method.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_nTCF3QNsIN_AlignFlo/figures/010_Table_5.jpg]]

## 方法谱系与知识库定位

AlignFlow 属于基于最优传输的流生成模型改进方法，其方法谱系定位如下：

- **上游方法**：Flow Matching (Lipman et al., 2022)、Minibatch OT (Tong et al., 2023; Pooladian et al., 2023)、ICNN-based OT (Kornilov et al., 2024)
- **核心差异**：与依赖小批量样本的离散 OT 方法不同，AlignFlow 利用 SDOT 在整个数据集上计算确定性映射，避免了维度灾难和批大小依赖问题。
- **下游应用**：可无缝集成到 Shortcut Model (Frans et al., 2025) 和 MeanFlow (Geng et al., 2025) 等 SOTA FGM 中。

**局限性**：
1. SDOT 映射本身无法泛化到新数据点，必须依赖 FGM 训练阶段通过神经网络的归纳偏置实现泛化。
2. 当 SDOT 映射未完全收敛时（MRE > 0），需要 Rebalance 操作进行修正，引入了少量受控随机性。
3. SDOT 映射的计算需要访问整个数据集，对于超大规模数据集（如数十亿样本），其 O(|I|) 的每步迭代成本可能成为瓶颈。
4. 当前方法主要针对图像生成任务验证，其在文本、音频等其他模态上的有效性尚未探索。

**开放问题**：
1. 如何将 AlignFlow 扩展到文本或音频等非连续、非欧几里得数据模态？
2. SDOT 映射的 Rebalance 操作对最终生成质量的定量影响如何？是否存在更优的偏差修正策略？
3. 对于超大规模数据集（如 LAION-5B），SDOT 映射的计算能否通过近似方法（如聚类或分层 SDOT）实现可扩展？
4. AlignFlow 与蒸馏方法的结合是否能进一步降低 NFE 至 1 以下，同时保持高质量？
5. SDOT 映射的几何结构（Laguerre 单元）能否用于解释或控制生成模型的潜在表示？

## 原文 PDF

![[paperPDFs/ICLR_2026/AlignFlow_Improving_Flow_based_Generative_Models_with_Semi_Discrete_Optimal_Transport.pdf]]
