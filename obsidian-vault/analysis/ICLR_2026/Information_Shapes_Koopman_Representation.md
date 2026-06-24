---
title: "Information Shapes Koopman Representation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Information_Shapes_Koopman_Representation.pdf
openreview_forum_id: Szh0ELyQxL
aliases:
- ISKR
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "信息论拉格朗日量中的权重系数（α控制时序一致性，β控制结构一致性，γ控制预测充分性）直接调节简单性与表达性的权衡。"
primary_logic: "借鉴信息瓶颈（IB）理论，揭示潜变量互信息限制预测误差上界，而冯·诺依曼熵防止谱权重集中在少数主导模态，从而在保持线性预测的同时维持表示的有效维度。"
claims:
- "潜变量互信息的下界决定了自回归预测的误差积累。"
- "最大潜变量互信息会导致水填充分配，使表示坍缩到少数模态，而冯·诺依曼熵正则化可防止此坍缩。"
- "所提方法在多种物理模拟、视觉控制和图结构动力学任务上均取得了最优或次优性能。"
- "Lorenz 63 上 5-NRMSE = 0.003 (0.002)"
---

# Information Shapes Koopman Representation

> [!tip] 核心洞察
> 借鉴信息瓶颈（IB）理论，揭示潜变量互信息限制预测误差上界，而冯·诺依曼熵防止谱权重集中在少数主导模态，从而在保持线性预测的同时维持表示的有效维度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 信息塑造Koopman表示 |
| 英文题名 | Information Shapes Koopman Representation |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=Szh0ELyQxL); [GitHub](https://github.com/Wenxuan52/InformationKoopman) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | InformationKoopman |
| Dataset | Lorenz 63, Kármán Vortex, Dam Flow, ERA5 Geopotential |

> [!tip] 效果简介
> - Lorenz 63 上，5-NRMSE 为 0.003 (0.002)，对比 0.004 (0.002) [KKR]，变化 -0.001。
> - Kármán Vortex 上，5-SSIM 为 0.936 (0.025)，对比 0.920 (0.030) [PFNN]，变化 +0.016。
> - Dam Flow 上，SDE 为 0.244，对比 0.269 [KKR]，变化 -0.025。

## 概述

Koopman算子理论为非线性动力学系统提供了一条通往线性化分析的路径——通过在合适的观测函数空间中定义线性演化算子，使得复杂的非线性轨迹预测转化为简单的线性前向映射。然而，这一优雅的理论框架在实际表示学习中面临一个根本性瓶颈：**表示简单性（线性预测）与表达性（模式多样性）之间的内在冲突**。过度追求线性结构会导致潜表示坍缩到少数主导模态，丧失对丰富动力学模式的刻画能力；而一味增加表达性又可能破坏线性演化假设，使预测不稳定。

本文从信息论视角重新审视这一权衡。核心洞察是：借鉴信息瓶颈（Information Bottleneck, IB）理论，潜变量互信息的下界直接决定了自回归预测的误差积累（Proposition 2），而冯·诺依曼熵正则化能够防止谱权重过度集中，维持表示的有效维度（Proposition 4, 5）。基于此，作者提出**InformationKoopman**——一个统一的信息论拉格朗日量框架，通过三个可调节的权重系数（α控制时序一致性，β控制结构一致性，γ控制预测充分性）显式平衡简单性与表达性。

在方法定位上，InformationKoopman区别于传统的Koopman自编码器（如**KAE**，Pan et al., 2023）和核回归方法（如**KKR**，Bevanda et al., 2023），首次将互信息最大化与熵正则化引入Koopman表示学习。实验覆盖物理模拟（Lorenz 63、Kármán涡街、Dam Flow）、视觉控制（Planar、Pendulum、Cartpole）和图结构动力学（绳索、软体）三类任务，在5步及长程预测指标上均取得了最优或次优性能。消融实验进一步验证了三个正则项各自的关键作用：移除互信息正则化（α=0）导致时序一致性丢失，潜空间退化为无几何结构的散点；移除结构一致性（β=0）导致潜流形崩塌；移除冯·诺依曼熵正则化（γ=0）则使某些维度被抑制，有效维度降低。

## 背景与动机

### 问题背景：Koopman表示的根本张力

非线性动力系统的长期预测与控制是科学计算与工程中的核心挑战。Koopman算子理论提供了一条优雅的路径：通过将非线性动力学提升到观测函数空间，系统演化在该空间中变为线性算子作用，从而可以用成熟的线性系统工具进行分析。具体而言，对于动力系统 $x_{n+1} = T(x_n)$，Koopman算子 $\mathcal{K}$ 作用在观测函数 $\phi$ 上，满足：

$$( \mathcal{K} \phi ) ( x ) = \phi ( T ( x ) )$$

学习的核心目标是找到一个有限维表示 $z_n = \phi(x_n)$，使得前向转移近似为线性：$z_n \approx K z_{n-1}$。

然而，这一目标内嵌了一个根本性的权衡：**简单性与表达性之间的矛盾**。简单性要求潜空间中的动力学是线性的（便于预测与控制），但线性约束天然限制了表示所能捕获的模式多样性。当模型过度追求线性简单性时，潜表示会坍缩到少数主导模态，丧失对系统丰富行为的表达能力——这就是**模式崩塌**；反之，若过度追求表达性，线性假设被破坏，预测误差将随时间步数累积而发散。这一瓶颈构成了Koopman表示学习领域的核心张力。

### 现有方法的缺口

当前主流的Koopman学习方法在应对上述权衡时存在明显盲区。**KAE**（Koopman Autoencoder, Pan et al., 2023）和**KKR**（Koopman Kernel Regression, Bevanda et al., 2023）等代表性方法主要依赖重构损失和简单的L2正则化来约束潜空间，缺乏对信息流动的显式建模。针对混沌系统的**PFNN**（Poincaré Flow Neural Network, Cheng et al., 2025）虽在特定场景表现优异，但其设计并未从信息论层面解释表示质量的退化机制。

这些方法的共同缺口在于：**缺少一个统一的理论框架来诊断和调节简单性与表达性之间的平衡**。具体表现为三个维度上的不足：

1. **时序一致性缺失**：潜变量 $z_n$ 与其时间邻域之间的互信息未被显式优化，导致跨时间步的表示连贯性无法保证。
2. **结构一致性缺失**：条件互信息 $I(z_n; x_n | z_{n-1})$ 未被约束，使得编码器可能将当前观测 $x_n$ 的信息过度注入 $z_n$，破坏线性前向结构。
3. **预测充分性缺失**：潜变量协方差矩阵的谱分布未被正则化，导致有效维度退化——少数特征值主导，多数维度被抑制，表示容量浪费。

### 本文动机：信息论视角的引入

本文的核心动机源于一个观察：**信息瓶颈（Information Bottleneck, IB）理论为导航表示学习中的权衡提供了元视角**。IB框架通过最大化表示与目标之间的互信息、同时最小化表示与输入之间的互信息，在压缩与保真之间取得平衡。将这一思想移植到Koopman表示学习中，可以提出一个中心问题：**能否在信息论原理的指导下，学习既结构简单又表达充分的Koopman表示？**

这一视角的引入带来了三个关键突破：

- **误差溯源**：信息沿Koopman表示的传播存在逐步退化——$I(x_{n-1}; x_n) \geq I(z_{n-1}; x_n) \geq I(z_{n-1}; z_n)$（Proposition 1），压缩编码和线性前向内在地限制了可保留的信息量。更重要的是，自回归预测的L2误差被逐步互信息差的上界所限定（Proposition 2），表明信息丢失直接导致误差累积。

- **谱视角的信息解耦**：潜变量与观测之间的互信息 $I(z_t; x_t)$ 可以被解耦为三个具有明确谱解释的分量（Proposition 3），分别对应Koopman算子的特征值模长、噪声协方差结构和观测映射的信息容量，使得信息流动与算子谱性质之间建立了直接联系。

- **水填效应与维度保护**：最大化潜变量互信息会导致“水填分配”（water-filling），使谱权重集中在少数强模态上（Proposition 4）；而冯·诺依曼熵 $S(\rho) = -\mathrm{tr}(\rho \log \rho)$ 的正则化可以防止这种坍缩，维持表示的有效维度（Proposition 5）。

基于以上分析，本文提出**InformationKoopman**——一个统一的信息论拉格朗日量框架，通过三个可调节的权重系数（$\alpha$ 控制时序一致性，$\beta$ 控制结构一致性，$\gamma$ 控制预测充分性）显式平衡简单性与表达性，从而在保持线性预测能力的同时，防止模式崩塌和不稳定。

## 核心创新

本文的核心贡献在于将**信息瓶颈（Information Bottleneck, IB）**理论引入Koopman表示学习，通过一个统一的信息论拉格朗日量，显式地平衡表示的**简单性**（线性可预测性）与**表达性**（模式多样性）。这一框架从根本上解决了Koopman学习中长期存在的模式崩塌与不稳定问题。

### 关键创新点

**1. 信息论损失函数的统一设计**

相较于现有Koopman方法仅依赖重构损失或简单KL散度，本文提出三项关键正则化槽位（changed slots），分别对应信息论框架中的不同目标：

- **时序一致性正则项（Temporal Coherence）**：引入 $\alpha I(z_n; \mathcal{P}_n)$，通过InfoNCE最大化潜变量与其时间邻域的互信息。这一设计确保潜空间保留时间上连贯的动力学结构，而非退化为无几何结构的散点。消融实验中，移除该项（$\alpha=0$）直接导致潜空间崩溃为散点。

- **结构一致性正则项（Structural Consistency）**：添加 $\beta (\mathbb{E}[\log q_\psi(z_n|z_{n-1})] + H_{p_\theta}(z_n|x_n))$，等价于最小化条件互信息 $I(z_n; x_n | z_{n-1})$。这强制潜变量在给定前一步潜状态时，尽可能少地依赖当前原始输入，从而保证Koopman算子的线性前向结构不被破坏。移除该项（$\beta=0$）导致潜流形崩塌。

- **预测充分性正则项（Predictive Sufficiency）**：引入 $\gamma S(\mathcal{C}/\text{tr}(\mathcal{C}))$，即潜变量协方差矩阵的冯·诺依曼熵。理论分析表明，单纯最大化潜变量互信息会导致“水填充”（water-filling）效应，使谱权重集中在少数主导模态上，造成有效维度坍缩。冯·诺依曼熵正则化强制谱权重在所有模态上均匀分布，防止模式崩塌。消融实验中，移除该项（$\gamma=0$）会抑制某些维度，仅保留循环分量。

**2. 理论保证：信息损失驱动误差积累**

本文首次建立了Koopman表示中信息损失与预测误差之间的定量联系。核心结论是：自回归预测的L2误差被逐步互信息差的上界所限定：

$$\| \mathbb{E}_{q^{KR}}[x_{1:t} \mid x_0] - \mathbb{E}_p[x_{1:t} \mid x_0] \|_2 \leq \bar{C} \sqrt{2 \sum_{n=1}^t (I(x_{n-1}; x_n) - I(z_{n-1}; z_n)) + \mathcal{E}}$$

这一不等式揭示了**信息在Koopman表示中沿时间传播时逐步退化**的根本原因：压缩编码和线性前向转移内在地限制了可保留的信息量，信息丢失直接转化为预测误差的累积。这为上述三项正则化提供了统一的理论动机——最大化潜变量互信息以保留信息，同时通过冯·诺依曼熵防止信息集中在少数模态。

**3. 与现有方法的本质区别**

| 方法 | 核心目标 | 关键缺失 |
|------|----------|----------|
| **KAE** (Pan et al., 2023) | 自编码器重构 + 线性潜空间 | 无信息论约束，潜空间缺乏几何结构 |
| **KKR** (Bevanda et al., 2023) | 核方法学习Koopman算子 | 无显式信息保留机制 |
| **PFNN** (Cheng et al., 2025) | 针对混沌动力学的专门设计 | 缺乏对谱多样性的理论保证 |
| **InformationKoopman (本文)** | 信息论驱动的简单性-表达性平衡 | — |

本文方法不依赖于特定动力学假设（如混沌），而是通过信息论原理提供了一种**通用的、可解释的**Koopman表示学习框架。实验表明，该方法在物理模拟（Lorenz 63、Kármán涡街、Dam Flow）、视觉控制（Pendulum、Cartpole）和图结构动力学（Rope、Soft）等多种任务上均取得了最优或次优性能，验证了信息论设计的跨域泛化能力。

## 整体框架

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_Szh0ELyQxL/figures/002_Figure_1.jpg]]
*Figure 1: Information-theoretic Koopman framework. (a) Structure overview, (b) Information disentanglement with spectral interpretations, and (c) Water-filling effect of Mutual Information (MI) and von Neumann entropy (VNE) on spectral information allocation*

**InformationKoopman** 的核心框架建立在变分自编码器（VAE）结构之上，将信息论原理系统性地注入Koopman表示学习的每一个关键环节。整个pipeline由五个功能模块构成，通过统一的信息论拉格朗日量协调运作。

### 模块构成与数据流

1. **编码器（Encoder）**：将原始状态 $x_n$ 映射为潜变量 $z_n$，构成信息压缩的第一步。编码器输出潜变量的分布参数，从中采样得到 $z_n$。

2. **Koopman算子（Koopman Operator）**：执行线性前向转移 $z_n = \mathcal{K} z_{n-1} + \varepsilon$，其中 $\mathcal{K}$ 为待学习的线性算子，$\varepsilon$ 为高斯噪声。这一线性演化是Koopman表示理论的核心——在潜空间中用线性动力学近似原始非线性系统的演化。

3. **解码器（Decoder）**：从潜变量 $z_n$ 重构原始状态 $x_n$，确保潜表示保留了足够的状态信息。

4. **时序一致性模块（Temporal Coherence via InfoNCE）**：计算潜变量 $z_n$ 与其时间邻域 $\mathcal{P}_n = \{z_{n\pm i} \mid 1 \leq i \leq k\}$ 之间的互信息 $I(z_n; \mathcal{P}_n)$，通过InfoNCE损失最大化这一互信息。该模块确保潜表示在时间轴上保持连贯的几何结构，防止潜空间退化为无结构的散点。

5. **熵正则化模块（Entropy Regularizer）**：基于批次内潜变量的协方差矩阵 $\mathcal{C}$，计算归一化后的冯·诺依曼熵 $S(\mathcal{C}/\mathrm{tr}(\mathcal{C}))$。该模块直接作用于潜空间的谱结构，防止谱权重集中在少数主导模态上，从而维持表示的有效维度。

### 统一优化目标

上述模块通过统一的信息论拉格朗日量整合为单一优化目标：

$$
\operatorname*{max}_{z} \; \alpha \log I(z_{t-n}; z_t) - \beta I(z_t; x_t \mid z_{t-n}) + \gamma S\!\left(\frac{\mathcal{C}}{\mathrm{tr}(\mathcal{C})}\right) + \log p(x_t \mid z_t)
$$

其中三个权重系数扮演着核心调控角色：
- **$\alpha$**（时序一致性）：最大化潜变量跨时间步的互信息，迫使表示保留时间上连贯的动力学信息；
- **$\beta$**（结构一致性）：最小化条件互信息 $I(z_t; x_t \mid z_{t-n})$，等价于要求潜变量在给定历史 $z_{t-n}$ 的条件下不额外依赖当前观测 $x_t$，从而强化Koopman线性转移的结构约束；
- **$\gamma$**（预测充分性）：最大化冯·诺依曼熵，鼓励谱多样性，防止模式崩塌。

### 信息瓶颈视角

框架的设计逻辑可通过对标准表示与Koopman表示的信息论对比（Table 1）来理解：标准表示的目标是“压缩过去以预测未来”，而Koopman表示的目标是“以线性、可解释的方式压缩过去以预测未来”。这一额外约束——线性演化——使得简单性与表达性之间的张力更为尖锐：线性算子天然倾向于将信息集中在少数主导模态上，导致有效维度坍缩。InformationKoopman通过引入冯·诺依曼熵正则化直接对抗这一倾向，同时用时序互信息保证压缩过程不丢失对预测至关重要的动力学信息。

### 关键理论支撑

框架的设计并非经验性的试凑，而是由两条核心理论洞察所驱动：

- **误差上界**（Proposition 2）：自回归预测的L2误差被逐步互信息差的上界所限定，即 $\| \mathbb{E}_{q^{KR}}[x_{1:t} \mid x_0] - \mathbb{E}_p[x_{1:t} \mid x_0] \|_2 \leq \bar{C} \sqrt{2 \sum (I(x_{n-1}; x_n) - I(z_{n-1}; z_n)) + \mathcal{E}}$。这表明信息在潜传播中的丢失直接导致预测误差的累积——因此最大化 $I(z_{n-1}; z_n)$ 是控制长期预测精度的根本手段。

- **谱分配机制**（Proposition 4 & 5）：最大化潜变量互信息在有限方差约束下会产生“水填充分配”（water-filling）效应，将谱权重集中于少数时间相干模态；而冯·诺依曼熵正则化则对抗这一集中趋势，迫使谱权重在所有模态上保持正分布，从而维持潜空间的有效维度。Figure 1(c) 直观展示了这一对抗平衡：互信息倾向于将信息分配给少数主导方向，而冯·诺依曼熵则推动信息向更多方向扩散。

## 核心模块与公式推导

### 信息瓶颈视角下的Koopman表示学习

传统Koopman表示学习面临的核心瓶颈在于**表示简单性（线性预测）与表达性（模式多样性）之间的根本权衡**：过度追求线性结构会导致模式崩塌，而过度追求表达性则破坏线性可预测性。本文借鉴信息瓶颈（Information Bottleneck, IB）理论，将这一权衡形式化为统一的信息论拉格朗日量，通过三个权重系数直接调节简单性与表达性的平衡。

Koopman表示下的概率轨迹模型由三个模块串联构成：

$$p^{KR}(x_{1:t} | x_0) = \int p(z_0|x_0) \prod_{n=1}^t p(z_n|z_{n-1}) p(x_n|z_n) dz_0 dz_1 \cdots dz_t$$

其中编码器 $p(z_0|x_0)$ 将初始状态映射到潜空间，线性高斯潜转移 $p(z_n|z_{n-1})$ 实现Koopman前向演化，解码器 $p(x_n|z_n)$ 重构原始状态。这一概率建模为后续的信息论分析奠定了基础。

### 信息退化与误差累积

Koopman表示中存在严格的信息退化链：

$$I(x_{n-1}; x_n) \geq I(z_{n-1}; x_n) \geq I(z_{n-1}; z_n)$$

这一不等式揭示了信息沿编码-转移路径逐步丢失的必然性：编码压缩和线性前向传播内在地限制了可保留的信息量。更重要的是，这种信息丢失直接导致自回归预测误差的累积上界：

$$\| \mathbb{E}_{q^{KR}}[x_{1:t} \mid x_0] - \mathbb{E}_p[x_{1:t} \mid x_0] \|_2 \leq \bar{C} \sqrt{2 \sum_{n=1}^t (I(x_{n-1}; x_n) - I(z_{n-1}; z_n)) + \mathcal{E}}$$

该上界表明：**潜变量互信息的下界决定了预测误差的累积速率**。每步信息丢失 $I(x_{n-1}; x_n) - I(z_{n-1}; z_n)$ 越大，长期预测的L2误差增长越快。这为最大化潜变量互信息提供了理论依据。

### 潜变量互信息的谱结构与水填充分配

在Koopman表示下，潜变量互信息具有闭式表达：

$$I(z_{t-n}; z_t) = \frac{1}{2} \log \det(\mathrm{I} + \mathcal{M}_n^{-\frac{1}{2}} (\mathcal{K}^n) \mathcal{C} (\mathcal{K}^n)^\top \mathcal{M}_n^{-\frac{1}{2}})$$

其中 $\mathcal{K}$ 为Koopman算子，$\mathcal{C}$ 为潜变量协方差矩阵，$\mathcal{M}_n$ 为多步噪声协方差。该闭式解揭示了互信息由Koopman谱和潜空间协方差结构共同决定。

然而，单纯最大化潜变量互信息会导致**水填充分配效应**：谱权重集中在少数主导模态上，表示坍缩到低维子空间，丧失模式多样性。为对抗这一坍缩，引入冯·诺依曼熵正则化：

$$S(\rho) = -\mathrm{tr}(\rho \log \rho)$$

其中 $\rho = \mathcal{C} / \mathrm{tr}(\mathcal{C})$ 为归一化协方差矩阵。冯·诺依曼熵反映潜空间的有效维度：当熵接近0时，谱权重集中于单一方向；当熵接近 $\log d$ 时，谱权重均匀分布。通过最大化该熵项，强制表示在保持线性预测的同时维持足够的有效维度。

### 统一信息论拉格朗日量与可计算损失

综合上述分析，Koopman表示学习的目标可形式化为统一的信息论拉格朗日量：

$$\operatorname*{max}_{z} \ \alpha \log I(z_{t-n}; z_t) - \beta I(z_t; x_t | z_{t-n}) + \gamma S\Big( \frac{\mathcal{C}}{\mathrm{tr}(\mathcal{C})} \Big) + \log p(x_t | z_t)$$

三项正则化分别对应：
- **时序一致性**（$\alpha$ 控制）：最大化 $\log I(z_{t-n}; z_t)$，保留跨时间步的共享信息；
- **结构一致性**（$\beta$ 控制）：最小化条件互信息 $I(z_t; x_t | z_{t-n})$，确保潜转移捕获足够的动态结构；
- **预测充分性**（$\gamma$ 控制）：最大化冯·诺依曼熵，防止谱退化和模式崩塌。

为实际训练，将上述拉格朗日量转化为可计算损失函数：

$$\operatorname*{max} \sum_n \Big[ \alpha I(z_n; \mathcal{P}_n) + \beta \mathbb{E}_{p_\theta(z_n | x_n)} [\log q_\psi(z_n | z_{n-1})] + \beta H_{p_\theta}(z_n | x_n) \Big] + \log p_\omega(x_n | z_n) + \gamma S\Big( \frac{\mathcal{C}}{\mathrm{tr}(\mathcal{C})} \Big) + \mathcal{L}_{\mathrm{ELBO}}$$

其中：
- $I(z_n; \mathcal{P}_n)$ 通过InfoNCE估计，$\mathcal{P}_n = \{z_{n\pm i} | 1 \leq i \leq k\}$ 为时序邻域，最大化潜变量与其时间邻域的互信息以保持时序连贯性；
- $\mathbb{E}_{p_\theta}[\log q_\psi(z_n | z_{n-1})]$ 为潜转移的对数似然，等价于最小化条件互信息 $I(z_n; x_n | z_{n-1})$；
- $H_{p_\theta}(z_n | x_n)$ 为编码器熵，防止潜表示过度确定性；
- $S(\mathcal{C} / \mathrm{tr}(\mathcal{C}))$ 基于批次潜变量协方差计算冯·诺依曼熵；
- $\mathcal{L}_{\mathrm{ELBO}}$ 为标准变分下界，保证训练稳定性和重构质量。

三个权重系数 $(\alpha, \beta, \gamma)$ 构成了调节表示简单性与表达性权衡的直接因果旋钮，其消融效果在摆锤任务中得到验证：$\alpha=0$ 导致时序结构丢失、潜空间退化为无几何结构的散点；$\beta=0$ 导致潜流形崩塌；$\gamma=0$ 则抑制某些维度，仅保留循环分量，有效维度显著降低。

## 实验与分析

### 核心瓶颈与因果机制

Koopman表示学习面临的根本矛盾在于**表示简单性**（线性前向预测）与**表达性**（捕获系统多样模态）之间的权衡。若过度追求线性结构，潜空间会坍缩至少数主导模态，丧失对复杂动力学的刻画能力；反之，若忽视结构约束，则表示退化为无几何意义的散点，预测误差随步长累积。本文通过信息论拉格朗日量中的三个权重系数直接调节这一权衡：**α** 控制时序一致性（最大化潜变量与其时间邻域的互信息），**β** 控制结构一致性（最小化给定过去潜变量下当前潜变量与观测的条件互信息），**γ** 控制预测充分性（通过冯·诺依曼熵正则化鼓励谱多样性）。

理论分析揭示了因果链条：Proposition 2 表明，自回归预测的 L2 误差上界由逐步互信息损失决定——即 $\| \mathbb{E}_{q^{KR}}[x_{1:t} \mid x_0] - \mathbb{E}_p[x_{1:t} \mid x_0] \|_2 \leq \bar{C} \sqrt{2 \sum_{n=1}^t (I(x_{n-1}; x_n) - I(z_{n-1}; z_n)) + \mathcal{E}}$。这意味着信息沿潜变量传播时的每一步丢失，都会直接转化为预测误差的累积。而 Proposition 4 与 Proposition 5 进一步揭示：最大化潜变量互信息会导致“水填充”效应，使谱权重集中于少数时间相干模态，造成模式崩塌；冯·诺依曼熵正则化 $S(\mathcal{C}/\mathrm{tr}(\mathcal{C}))$ 则通过惩罚谱集中度，强制保留有效维度，从而在维持线性预测的同时防止表示退化。

### 主实验结果

**物理模拟任务**（Table 2）：在 Lorenz 63、Kármán 涡街和 Dam Flow 三个基准上，InformationKoopman 均取得最优或次优性能。具体而言，Lorenz 63 的 5-NRMSE 为 0.003（vs. KKR 的 0.004），Kármán 涡街的 5-SSIM 为 0.936（vs. PFNN 的 0.920），Dam Flow 的 SDE 为 0.244（vs. KKR 的 0.269）。值得注意的是，PFNN 是专为混沌动力学设计的 SOTA 方法，但在 Kármán 涡街上仍被本方法超越，说明信息论正则化在非混沌任务上具有更普适的优势。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_Szh0ELyQxL/figures/004_Table_2.jpg]]
*Table 2: Performance comparison of five algorithms on physical simulation tasks. PFNN is designed for chaotic dynamics and is thus not evaluated on Dam Flow. Here, N-NRMSE and N-SSIM denote errors at N prediction steps, values in parentheses indicate variance, and SDE is the spectral distribution error. Best results are highlighted in bold with green, second best are shaded in blue*

**天气预测任务**（Table 6）：在 ERA5 高维随机天气数据上，本方法在全部通道的短时和长时预测中均优于所有基线。以位势高度和温度为例，5-NRMSE 分别为 0.023 和 0.956（5-SSIM），相比 PFNN 的 0.046 和 0.888 分别降低 50% 和提升 7.6%。这表明信息论框架能有效应对高维随机系统的谱多样性需求。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_Szh0ELyQxL/figures/022_Table_6.jpg]]
*Table 6: Per-channel performance comparison on ERA5 weather forecasting. N-NRMSE and N-SSIM denote errors at N prediction steps; values in parentheses indicate the standard deviation across test samples. Even under the highly stochastic and high-dimensional ERA5 weather dynamics, our approach outperforms all baselines across both short-term and long-term prediction horizons*

**图结构动力学任务**（Figure 5）：在 Rope 和 Soft 环境的 100 步 rollout 预测中，本方法的 NRMSE 约为 0.05，仅为 CKO（Li et al., 2020）的一半（~0.10）。这一差距在含噪声条件下依然保持，说明时序一致性与结构一致性正则化对图结构系统的长程预测稳定性至关重要。

**视觉控制任务**（Table 8/9）：在含噪声和无噪声 rollout 条件下，本方法的 Percentage to Goal 指标均优于 E2C 和 PCC（Banijamali et al., 2019），验证了信息论表示在控制场景中的迁移能力。

### 消融实验

消融实验（Figure 6，摆锤任务）系统验证了三个正则项的独立作用：

- **移除时序一致性（α=0）**：潜空间退化为无几何结构的散点，丧失了相位空间的 $S^1 \times \mathbb{R}$ 拓扑。这是因为缺少互信息引导，潜变量无法保持时间邻域的一致性。
- **移除结构一致性（β=0）**：潜流形发生崩塌，说明仅靠重构损失无法维持潜空间的几何结构，需要显式最小化条件互信息 $I(z_t; x_t \mid z_{t-1})$ 来约束编码器。
- **移除冯·诺依曼熵（γ=0）**：潜空间仅保留循环分量（$S^1$），径向维度（$\mathbb{R}$）被抑制。Figure 20 进一步显示，γ=0 时潜变量协方差矩阵的谱权重随训练集中在少数特征值上，而 γ=0.5 时谱分布保持均匀，有效维度得以维持。

### 失败模式与局限性

当前框架存在以下已知局限：

1. **高斯噪声假设**：理论推导和损失函数设计均基于线性高斯潜转移 $z_n = \mathcal{K} z_{n-1} + \varepsilon$，对于高度非高斯或状态不连续的观测系统（如碰撞动力学），可能无法准确建模。
2. **样本复杂度未分析**：附录 D 明确指出，理论框架未涉及非渐近收敛性分析，实际应用中可能需要大量样本才能稳定估计互信息和协方差矩阵。
3. **连续时间与偏观测扩展**：当前方法面向离散时间全观测系统，向连续时间流和部分观测场景的推广仍是开放问题。

### 重要图表结论

- **Table 1**：对比标准表示与 Koopman 表示的信息论目标，揭示 Koopman 表示需要在“压缩过去信息”与“保留未来预测能力”之间寻求 β 加权的平衡。
- **Figure 1**：全景展示信息论 Koopman 框架——(a) VAE 结构，(b) 互信息可分解为三个谱解释分量，(c) 水填充效应与冯·诺依曼熵对谱分配的对立作用。
- **Figure 2**：Kármán 涡街的特征值分布与 t-SNE 流形可视化表明，本方法的 Koopman 算子特征值更接近单位圆，潜流形更清晰地呈现极限环结构，而基线方法（尤其是 VAE 和 KAE）的流形则出现扭曲或断裂。
- **Figure 20**：直接对比 γ=0 与 γ=0.5 时潜变量协方差矩阵随训练 epoch 的演化，直观展示冯·诺依曼熵正则化如何防止谱权重向少数特征值集中。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_Szh0ELyQxL/figures/001_Table_1.jpg]]
*Table 1: Information-theoretic comparison between standard and Koopman representations. Here, $\beta$ controls the trade-off between simplicity and future-state expressiveness*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_Szh0ELyQxL/figures/003_Figure_1.jpg]]
*Figure 1: Proposition 3 (Information Disentanglement and Spectral Property) The mutual information I ( $\boldsymbol { z } _ { t } ; \boldsymbol { x } _ { t }$ ) can be disentangled into a summation of three distinct components, each with a spectral interpretation (see proof in Appendix F.4, see Figure 1(b))

### 补充图表

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_Szh0ELyQxL/figures/008_Figure.jpg]]

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_Szh0ELyQxL/figures/013_Figure_9.jpg]]
*Figure 9: Spectral behavior of the Koopman operator under different regimes. Left: Eigenvalues of K (orange dots) lie on the complex unit circle ( | $\lambda$ | = 1 ) , and those of $\textstyle { \mathcal { K } } ^ { n }$ with n = 7 (blue crosses) remain on the unit circle, indicating temporal coherence and preservation of information. Right: Eigenvalues of K lie strictly inside the complex unit circle ( | $\lambda$ | < 1 ) , and the spectrum of ${ \boldsymbol { \kappa } } ^ { \tilde { n } }$ contracts toward the origin as n increases, reflecting fast mixing and information dissipation

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_Szh0ELyQxL/figures/029_Figure_21.jpg]]
*Figure 21: Visualization of the von Neumann entropy regularization loss and the total training loss over epochs for the physical simulation tasks. The stable behavior of both the total loss and the von Neumann entropy loss indicates that our training procedure is numerically stable and robust across different systems*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_Szh0ELyQxL/figures/010_Table_3.jpg]]
*Table 3: Notations in the Main Text*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_Szh0ELyQxL/figures/014_Table_4.jpg]]
*Table 4: Spectral interpretation of information components in Koopman representation*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_Szh0ELyQxL/figures/018_Table_5.jpg]]
*Table 5: Model structures across experimental environments. Here, $\boldsymbol { \mathcal { K } } \boldsymbol { z } _ { t } + \boldsymbol { B } \boldsymbol { a } _ { t }$ denotes a controlled latent transition with linear control input $a _ { t }$ (Visual Inputs case). $\kappa$ ( A ) denotes an adjacencyconditioned Koopman operator, corresponding to a shared Koopman composition modulated by the adjacency matrix A (i.e., K(A) := A ⊗ K in graph environments; see Li et al. (2020, Page 4) for details)

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_Szh0ELyQxL/figures/023_Table_7.jpg]]
*Table 7: Training time statistics for different models and tasks. Epoch times are reported as mean ± std (in seconds). For Ours, InfoNCE and entropy (von Neumann entropy) rows correspond to the total per-epoch computation. Notably, the overhead introduced by InfoNCE and von Neumann entropy is marginal, accounting for only a small percentage of the total training time*

## 方法谱系与知识库定位

### 1. 方法谱系

**InformationKoopman** 位于 Koopman 表示学习与信息瓶颈（Information Bottleneck, IB）理论的交叉地带。其直接前驱是两类工作：

**Koopman 自编码器家族**。早期工作如 **KAE**（Koopman Autoencoder, Pan et al., 2023）和 **KKR**（Koopman Kernel Regression, Bevanda et al., 2023）分别通过自编码器和核方法学习线性前向映射，但缺乏对潜空间信息结构的显式约束。**PFNN**（Poincaré Flow Neural Network, Cheng et al., 2025）针对混沌动力学设计了专门的流形约束，在 Lorenz 63 和 Kármán 涡街等混沌任务上达到 SOTA，但其设计目标窄，不适用于 Dam Flow 等非混沌系统。**CKO**（Compositional Koopman Operator, Li et al., 2020）将 Koopman 扩展到图结构动力学，但同样未从信息论角度处理简单性-表达性权衡。

**潜空间嵌入控制方法**。**E2C**（Embed to Control）和 **PCC**（Prediction, Consistency, Curvature, Banijamali et al., 2019）在视觉控制场景中学习前向潜空间，但它们的正则化设计（如曲率惩罚）是启发式的，缺乏对信息流和谱结构的理论分析。

InformationKoopman 的核心推进在于**将上述方法的正则化策略统一到信息论框架下**：时序一致性对应潜变量互信息最大化（α 项），结构一致性对应条件互信息最小化（β 项），预测充分性对应冯·诺依曼熵正则化（γ 项）。这三个权重系数直接调节简单性与表达性的权衡，使方法在不同动力学类型（混沌、周期、图结构）上均可通过调参适配，无需为每个任务设计专用约束。

### 2. 适用边界与局限

**适用场景**。该方法在以下条件下表现最优：
- 观测噪声近似高斯分布，潜状态转移为线性高斯过程；
- 动力学具有可发现的低维潜结构（如 Lorenz 63 的混沌吸引子、Kármán 涡街的极限环、摆锤的 $S^1 \times \mathbb{R}$ 相空间）；
- 观测维度高但潜维度低，信息压缩有益于去噪和结构发现。

**已知局限**（来自论文自述及分析推断）：
1. **非高斯/不连续系统**。当前理论框架基于高斯噪声假设，对于高度非高斯观测或状态不连续的系统（如碰撞、切换动力学），线性高斯转移假设可能失效。消融实验（图6）显示，移除结构一致性（β=0）时潜流形崩塌，暗示该方法对条件互信息项的依赖较强，在噪声模型不匹配时可能不稳定。
2. **样本复杂度未分析**。论文附录 D 明确指出，理论框架未涉及样本复杂度或非渐近收敛性分析。这意味着在极小样本场景下，互信息估计（通过 InfoNCE）和协方差估计的可靠性缺乏理论保证。
3. **连续时间与偏观测**。当前方法针对离散时间、全观测状态设计。如何扩展到连续时间流和部分可观测系统（如仅观测部分状态分量）是开放问题。
4. **线性 Koopman 算子的表达力上限**。尽管冯·诺依曼熵正则化能防止谱退化，但线性算子本身的表达力受限于潜空间维度。对于需要极高维潜空间的系统，线性前向映射可能不充分，需要核技巧或非线性推广。

### 3. 开放问题

1. **更紧的信息论下界**。当前自回归误差界（Proposition 2, Equation 6）由逐步互信息差的上界给出，但该界是否紧致？能否通过更精细的分析（如考虑条件互信息的链式法则）得到更紧的界，从而指导更优的正则化设计？

2. **连续时间与偏观测扩展**。Koopman 理论天然适用于连续时间流（通过生成元/无穷小生成元），但信息论框架如何迁移到随机微分方程驱动的连续时间观测？偏观测场景下，互信息的估计需要处理隐状态推断，这是否会引入额外的信息损失项？

3. **非线性观测函数与核方法**。当前分析假设编码器学习线性化观测函数 φ。能否将信息论分析推广到更一般的非线性观测函数族？核技巧（如 KKR 使用的核方法）是否能与信息论正则化结合，在保持线性前向的同时提升观测函数的表达力？

4. **权重系数 α、β、γ 的自适应调节**。当前三个系数是固定超参数。是否存在基于数据特性的自适应调节策略？例如，根据动力学的时间尺度自动调整 α（时序一致性强度），或根据潜空间有效维度自动调整 γ（熵正则化强度）？

## 原文 PDF

![[paperPDFs/ICLR_2026/Information_Shapes_Koopman_Representation.pdf]]
