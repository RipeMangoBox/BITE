---
title: "Learning Straight Flows: Variational Flow Matching for Efficient Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Learning_Straight_Flows_Variational_Flow_Matching_for_Efficient_Generation.pdf
project_link: null
code_link: null
aliases:
- SVFMSV
- LSFVFMEG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入变分隐变量 z 来编码“生成概览”，使模型能区分交叉的插值线；同时通过直性损失惩罚速度场沿轨迹的时间变化率，强制轨迹为直线。
primary_logic: 在 Flow Matching 框架中加入带全局“生成概览”的变分隐变量 z，结合最小化速度场物质导数 D_t v 的直性目标，使模型即使在独立耦合导致插值交叉的情况下也能学习直线生成路径，从而用极少步数完成高质量生成。
claims:
- 独立耦合与直线轨迹学习存在根本矛盾：非交叉条件 V((X₀, X₁))=0 不可达，导致曲线路径。
- S‑VFM 通过变分隐变量 z 提供全局‘生成概览’，使速度场能够分辨交叉的插值，突破独立耦合的限制。
- 直性目标 L_S 通过最小化速度场的时间导数 D_t v，理论上等价于 V=0 且可支持一步生成。
- 在 CIFAR‑10 和 ImageNet 256×256 上，S‑VFM 在少步生成（NFE=1,2）中取得最优 FID，且 FID 随 NFE 增加单调下降，验证了直线轨迹的有效性。
---

# Learning Straight Flows: Variational Flow Matching for Efficient Generation

> [!tip] 核心洞察
> 在 Flow Matching 框架中加入带全局“生成概览”的变分隐变量 z，结合最小化速度场物质导数 D_t v 的直性目标，使模型即使在独立耦合导致插值交叉的情况下也能学习直线生成路径，从而用极少步数完成高质量生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 学习直线流：面向高效生成的变分流匹配 |
| 英文题名 | Learning Straight Flows: Variational Flow Matching for Efficient Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.17583) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Straight Variational Flow Matching (S‑VFM) |
| Dataset | CIFAR‑10 32×32, ImageNet 256×256 |

> [!tip] 效果简介
> - CIFAR‑10 32×32 上，FID 2.81 (S‑VFM adaptive norm, NFE=1) vs 2.83 (iCT, NFE=1) (-0.02)。
> - ImageNet 256×256 上，FID 3.31 (S‑VFM‑XL/2, NFE=1) vs 6.93 (iCT‑Deep, NFE=1) (-3.62)；FID 2.86 (S‑VFM‑XL/2, NFE=2) vs 5.94 (iCT‑Deep, NFE=2) (-3.08)。

## 概要

生成模型的核心追求之一，是在极少的推理步数内产出高质量样本。Flow Matching（FM）框架通过匹配条件速度场，为连续归一化流提供了简洁的训练范式，但其默认的**独立耦合**策略会在训练插值路径中引入大量交叉，迫使学习的边际速度场对不相容的方向取平均，最终产生弯曲的生成轨迹。这一根本矛盾使得标准 FM 必须依赖多步 ODE 模拟才能保证生成质量，难以实现高效的一步或极少步生成。

本文提出 **Straight Variational Flow Matching（S‑VFM）**，直击上述瓶颈。其核心思路包含两个相互协同的机制：

1. **变分隐变量提供“生成概览”**：在 FM 框架中引入变分隐变量 $z$，通过变分后验 $q_\phi(z \mid X_0, X_1, X_t, t)$ 编码每个源‑目标对的全局信息，使速度网络 $v_\theta(X_t, t, z)$ 能够区分原本交叉的插值线，从而突破独立耦合的限制。
2. **直性损失强制直线轨迹**：通过最小化速度场沿特征线的物质导数 $D_t v$，理论上等价于消除轨迹的曲率（即 $V((X_0, X_1)) = 0$），迫使生成路径趋近直线，使一步积分即可从源分布到达目标分布。

S‑VFM 的训练目标联合了变分流匹配损失 $\mathcal{L}_{\mathrm{VFM}}$ 与直性约束 $\mathcal{L}_{\mathrm{S}}$，在保持分布匹配精度的同时，显式地塑造速度场的几何性质。推理时，从先验 $p(z)$ 采样一个隐变量贯穿整个时间区间，配合少步 ODE 求解器即可完成生成。

在 CIFAR‑10 和 ImageNet 256×256 上的实验表明，S‑VFM 在一步生成（NFE=1）中取得最优 FID（CIFAR‑10: 2.81；ImageNet: 3.31），且 FID 随 NFE 增加单调下降，验证了直线轨迹对少步生成的有效性。该方法在方法谱系上介于 **Flow Matching**（Lipman et al., ICLR 2023）与 **Variational Flow Matching**（Ma et al., ICML 2025）的延长线上，同时与 **Rectified Flow**（Liu et al., ICLR 2023）和 **Consistency Models**（Song et al., ICML 2023）等少步生成方法形成对比，为直线流学习提供了新的理论视角与实践方案。



深度生成模型的核心目标之一是学习从简单先验分布到复杂数据分布的映射。近年来，基于常微分方程（ODE）的连续归一化流及其变体——特别是 Flow Matching（FM）——因其模拟无关的训练方式而受到广泛关注。FM 通过在源分布 $p_0$ 和目标分布 $p_1$ 之间定义线性插值路径 $X_t = (1-t)X_0 + t X_1$，并以条件速度 $\Delta^X = X_1 - X_0$ 作为回归目标来训练速度场 $v_\theta$，从而避免了以往连续流模型需要反复求解 ODE 进行最大似然训练的昂贵开销。

### 独立耦合的根本矛盾

然而，FM 框架存在一个深层结构性瓶颈：其默认采用的**独立耦合**策略——即从源分布和目标分布中独立采样 $(X_0, X_1)$ 对——会导致训练插值路径在数据空间中大量交叉。当多条线性插值线在相同空间位置和时间点上交汇时，该点的真实条件速度存在多个相互矛盾的方向。速度网络 $v_\theta(X_t, t)$ 由于仅以当前状态和时间作为条件，无法分辨这些交叉来自哪一对 $(X_0, X_1)$，因此被迫对所有不兼容的方向取平均。

这一平均效应直接破坏了生成轨迹的直线性。理论分析表明，当且仅当条件 $V((X_0, X_1)) = 0$ 成立时，模型才能学习到直线生成路径；而在独立耦合下，该条件**不可达**——交叉点的存在使得速度场必然产生非零曲率，迫使生成轨迹弯曲。其后果是：推理时需要使用多步 ODE 求解器（如 Dopri5 或 Euler 方法）才能保证生成质量，严重削弱了 FM 框架在少步生成场景下的效率优势。

### 现有应对策略及其局限

针对上述问题，已有若干工作尝试从不同角度进行缓解：

- **Rectified Flow**（Liu et al., ICLR 2023）通过迭代式蒸馏来逐步消除插值路径的交叉，使轨迹逐轮“拉直”。但该方法需要多轮训练-采样循环，计算成本高昂，且本质上是对已训练模型的后续修正，而非从根源上解决交叉问题。
- **Consistency Models**（Song et al., ICML 2023）通过自一致性约束迫使轨迹上不同时间点的输出映射到同一起点-终点对，从而间接抑制弯曲。然而，其训练目标与直线性之间缺乏显式的理论等价关系，少步生成质量仍有提升空间。
- **Variational Flow Matching (VFM)**（Ma et al., ICML 2025）引入了变分隐变量 $z$ 来编码源-目标对的全局信息，使速度场能够感知不同插值对之间的差异。这为区分交叉插值线提供了机制基础，但 VFM 并未施加任何显式的直性约束，因此轨迹弯曲的问题仍未得到根本解决。

### 本文动机与核心思路

本文的核心洞察在于：**直性轨迹学习的两大条件——区分交叉插值的能力与显式的直性优化目标——必须同时满足，缺一不可。** 仅有隐变量区分能力而无直性约束（如 VFM），轨迹仍可能弯曲；仅有直性约束而无交叉分辨能力（如标准 FM 加直性损失），则网络在交叉点处无法选择正确方向，优化目标本身即存在内在冲突。

基于此，本文提出 **Straight Variational Flow Matching (S‑VFM)**，将变分隐变量编码的“生成概览”与显式直性损失有机结合。具体而言，S‑VFM 在 VFM 框架的基础上引入直性目标 $\mathcal{L}_S$，通过最小化速度场沿特征线的物质导数 $D_t v$ 来惩罚轨迹弯曲。理论分析证明，$D_t v = 0$ 与 $V((X_0, X_1)) = 0$ 等价，从而为直线生成提供了严格的优化准则。在推理时，模型从先验 $p(z)$ 中采样单个隐变量 $z$ 贯穿整个时间区间，配合少步 ODE 求解即可完成高质量生成，理论上在直性条件满足时可实现一步生成。



## 核心方法与创新机理

### 问题根因：独立耦合与直线轨迹的根本矛盾

Flow Matching（FM）框架（Lipman et al., ICLR 2023）通过独立耦合从联合分布中采样源点 $X_0$ 和目标点 $X_1$，并以线性插值 $X_t = (1-t)X_0 + t X_1$ 构建训练路径。然而，这一看似自然的做法隐含了一个被长期忽视的结构性缺陷：**多条线性插值在空间中频繁交叉**。

当两条插值路径在某个时刻 $t$ 交汇于同一点 $X_t$ 时，它们对应的条件速度方向 $\Delta^X = X_1 - X_0$ 通常不同。但标准 FM 的速度网络 $v_\theta(X_t, t)$ 仅以当前点和时间为条件，缺乏分辨交叉路径来源的能力，因此被迫对不兼容的速度方向取平均。这一平均效应直接导致学习到的边际速度场产生弯曲的生成轨迹，需要多步 ODE 模拟才能保证生成质量。

论文对此给出了严格的理论刻画：**学习直线生成轨迹的目标等价于要求 $V((X_0, X_1)) = 0$，其中 $V$ 度量速度场沿插值路径的变化**。然而在独立耦合下，该条件不可达——交叉使得网络无法为每对 $(X_0, X_1)$ 输出精确的 $\Delta^X$ 而不产生冲突。这构成了 FM 框架在少步生成场景中的核心瓶颈。

### 关键机制：变分隐变量提供“生成概览”

S-VFM 的核心创新在于引入一个**变分隐变量 $z$** 来打破独立耦合的信息瓶颈。该隐变量通过变分后验编码器 $q_\phi(z \mid X_0, X_1, X_t, t)$ 获取每对源-目标点的全局信息，论文将其称为“生成概览”（generation overview）。速度网络随即以三元组 $(X_t, t, z)$ 为条件：

$$v_\theta(X_t, t, z)$$

这一设计赋予了模型**分辨交叉插值的能力**：即使两个不同的 $(X_0, X_1)$ 对在时刻 $t$ 交汇于同一点，只要它们对应的隐变量 $z$ 不同，网络就可以输出不同的速度方向，从而避免了对不兼容方向的强制平均。

推理时，从先验 $p(z)$ 采样一个隐变量，并在整个时间区间 $t \in [0,1]$ 内保持固定，引导 ODE 求解器沿直线轨迹生成。

### 直性约束：从理论等价到可优化目标

仅有隐变量并不足以保证轨迹的直线性。S-VFM 进一步引入**直性损失 $\mathcal{L}_S$**，直接惩罚速度场沿特征线的时间变化率。其理论依据由 Theorem 5 给出：

> **Theorem 5**：$V((X_0, X_1)) = 0$ 当且仅当速度场的物质导数 $D_t v^X(X_t, t) = 0$ 对所有 $t \in [0,1]$ 成立。

其中物质导数定义为：

$$D_t v(x,t) = \frac{\partial v}{\partial t} + (\nabla_x v) \cdot v$$

直性损失 $\mathcal{L}_S$ 通过 Jacobian-Vector Product（JVP）高效计算该导数的范数并最小化，迫使速度场沿每条生成轨迹保持恒定。当此条件满足时，积分可一步完成（Corollary 11）：

$$X_1 = X_0 + \int_0^1 v^X(X_t, t) dt = X_0 + \Delta^X$$

### 与相关工作的关键差异

| 维度 | FM (Lipman et al., 2023) | VFM (Ma et al., 2025) | Rectified Flow (Liu et al., 2023) | S‑VFM (本文) |
|------|--------------------------|-----------------------|-----------------------------------|-------------|
| 隐变量 | 无 | 有，仅用于速度匹配 | 无 | 有，同时用于速度匹配与直性约束 |
| 直性机制 | 无 | 无 | 迭代蒸馏消除交叉 | 单阶段训练，通过 $\mathcal{L}_S$ 强制 |
| 交叉处理 | 平均化导致弯曲 | 可分辨但无直性保证 | 多次训练逐步拉直 | 隐变量分辨 + 直性损失联合优化 |

与 **VFM**（Ma et al., ICML 2025）相比，S-VFM 的关键增量在于直性损失 $\mathcal{L}_S$——VFM 仅用隐变量增强速度匹配，但未显式约束轨迹的几何形状。与 **Rectified Flow** 相比，S-VFM 无需迭代蒸馏，在单阶段训练中同时解决交叉分辨和轨迹拉直两个问题。与 **Consistency Models**（Song et al., ICML 2023）相比，S-VFM 不依赖自一致性约束，而是从速度场几何性质出发直接优化直线性。

### 实现层面的 changed slots

1. **条件化方式**：从仅依赖 $(X_t, t)$ 扩展为 $(X_t, t, z)$，$z$ 通过自适应归一化（adaptive normalization）或瓶颈求和（bottleneck sum）注入网络。
2. **训练损失**：从单一的 $\mathcal{L}_{FM}$ 扩展为 $\mathcal{L} = \mathcal{L}_{VFM} + \alpha \mathcal{L}_S$，其中 $\mathcal{L}_{VFM}$ 包含速度匹配和 KL 散度正则，$\mathcal{L}_S$ 通过 JVP 计算物质导数范数。
3. **推理流程**：从多步 ODE 积分简化为“采样 $z \sim p(z)$ → 少步 Euler/Dopri5 积分”，在 NFE=1 时即可获得竞争性生成质量。



S‑VFM 的核心思想是在 Flow Matching 框架中引入一个变分隐变量 $z$ 来编码“生成概览”（generation overview），同时通过直性损失显式惩罚速度场沿轨迹的时间变化率，从而迫使模型学习直线生成路径。整体 pipeline 由训练和推理两个阶段组成，二者共享相同的模块结构，但在隐变量的来源和积分步数上有所不同。

**训练阶段**：对于每一对源样本 $X_0$ 和目标样本 $X_1$，首先按 $X_t = (1-t)X_0 + t X_1$ 构造线性插值点，并计算条件速度 $\Delta^X = X_1 - X_0$。变分后验编码器 $q_\phi$ 以 $(X_0, X_1, X_t, t)$ 为输入，输出隐变量 $z$ 的均值与方差，通过重参数化采样得到 $z$。速度预测网络 $v_\theta$ 以 $(X_t, t, z)$ 为条件预测当前速度向量。训练目标由两部分构成：**VFM 损失** $\mathcal{L}_{\mathrm{VFM}}$ 同时优化速度匹配误差和隐变量的 KL 散度正则项，确保 $z$ 携带有效的全局信息；**直性损失** $\mathcal{L}_{\mathrm{S}}$ 通过 Jacobian‑向量积（JVP）计算速度场沿特征线的物质导数 $D_t v$ 并最小化其范数，从理论上等价于消除轨迹弯曲（即 $V((X_0, X_1)) = 0$）。总损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{VFM}} + \alpha \mathcal{L}_{\mathrm{S}}$，其中 $\alpha$ 控制直性约束的强度。

**推理阶段**：从先验分布 $p(z)$ 采样一个固定的隐变量 $z$，该 $z$ 贯穿整个生成过程（$t \in [0,1]$）。从源分布采样初始噪声 $X_0$，利用速度预测网络 $v_\theta(X_t, t, z)$ 沿时间进行 ODE 积分（如 Euler 或 Dopri5 求解器），逐步演化到 $X_1$。由于直性损失强制速度场在时间上几乎不变，轨迹接近直线，因此仅需极少步数（NFE=1 或 2）即可获得高质量生成结果。

**模块关系与数据流**：pipeline 包含四个核心模块——变分后验编码器 $q_\phi$、速度预测网络 $v_\theta$、直性损失计算模块和 ODE 采样器。训练时，$q_\phi$ 和 $v_\theta$ 构成类似 VAE 的结构：$q_\phi$ 将全局信息压缩为隐变量 $z$，$v_\theta$ 则利用 $z$ 来消除独立耦合下插值线交叉带来的歧义。直性损失计算模块接收 $v_\theta$ 的输出及其梯度，通过 JVP 高效计算 $D_t v$ 并回传梯度。推理时，ODE 采样器替代 $q_\phi$，直接从先验采样 $z$ 并调用 $v_\theta$ 完成少步积分。这一设计使 S‑VFM 在保持 Flow Matching 简洁训练范式的同时，突破了独立耦合带来的曲线路径瓶颈，实现了直线生成与高效采样的统一。



### 问题形式化：Flow Matching 的直线性困境

Flow Matching 框架（Lipman et al., ICLR 2023）通过线性插值路径 $X_t = (1-t)X_0 + tX_1$ 定义条件速度 $\Delta^X = X_1 - X_0$，并训练网络 $v_\theta$ 匹配该速度：

$$\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}\left[\|v_\theta(X_t, t) - \Delta^X\|^2\right]$$

然而，标准 FM 采用**独立耦合**（independent coupling），即 $X_0$ 与 $X_1$ 从各自的边缘分布独立采样。这导致不同源-目标对的线性插值路径在空间中大量交叉。当多条插值线在 $(X_t, t)$ 处相交时，速度场被迫对不兼容的方向取平均，从而产生**曲线生成轨迹**，需要多步 ODE 模拟才能保证生成质量。

论文在 Section 4.1 中严格论证了这一根本矛盾：学习直线生成轨迹的目标等价于条件 $V((X_0, X_1)) = 0$（即插值线互不交叉），而独立耦合下该条件**不可达**。

### 核心模块一：变分隐变量编码器 $q_\phi$

为解决交叉歧义问题，S‑VFM 引入**变分隐变量 $z$** 来编码每个源-目标对的全局“生成概览”。具体而言，变分后验 $q_\phi$ 将 $(X_0, X_1, X_t, t)$ 映射为隐变量 $z$ 的高斯分布：

$$q_\phi(z \mid X_0, X_1, X_t, t) = \mathcal{N}\big(z; \mu_\phi(X_0, X_1, X_t, t), \sigma_\phi(X_0, X_1, X_t, t)\big)$$

其中：
- $\mu_\phi$：编码器预测的均值
- $\sigma_\phi$：编码器预测的方差
- $z$ 的维度远小于数据维度，作为紧凑的全局条件信号

该模块使速度网络能够根据 $z$ 区分在 $(X_t, t)$ 处相交的不同插值线，从而突破独立耦合的限制。

### 核心模块二：速度预测网络 $v_\theta$

速度网络以 $(X_t, t, z)$ 为条件，预测当前点的速度向量。$z$ 通过两种可选机制注入网络：
- **自适应归一化**（adaptive normalization）：将 $z$ 映射为特征图的缩放与偏置参数
- **瓶颈求和**（bottleneck sum）：将 $z$ 投影后与网络中间特征相加

推理时，从先验 $p(z) = \mathcal{N}(0, I)$ 采样单个 $z$，并在整个时间区间 $[0,1]$ 内固定使用，通过 Euler 或 Dopri5 求解器进行少步积分：

$$X_{t_{i+1}} = X_{t_i} + (t_{i+1} - t_i)\, v_\theta(X_{t_i}, t_i, z)$$

### 核心模块三：直性损失 $\mathcal{L}_{\mathrm{S}}$

为使轨迹强制为直线，S‑VFM 最小化速度场沿特征线的**物质导数** $D_t v$。定理 5 证明：$V((X_0, X_1)) = 0$ 当且仅当 $D_t v^X(X_t, t) = 0$ 对所有 $t \in [0,1]$ 成立。

物质导数定义为：

$$D_t v(x,t) = \frac{\partial v}{\partial t} + (\nabla_x v) \cdot v$$

在 S‑VFM 中，$v_\theta$ 还依赖隐变量 $z$，而 $z$ 本身也沿轨迹变化（由编码器 $q_\phi$ 给出），因此直性损失需考虑 $z$ 的全微分：

$$\mathcal{L}_{\mathrm{S}}(\theta, \phi) = \mathbb{E}\left[\big\|\partial_{X_t} v \cdot \Delta^X + \partial_t v + \partial_z v \cdot (\partial_{X_t} z \cdot \Delta^X + \partial_t z)\big\|^2\right]$$

其中：
- $\partial_{X_t} v \cdot \Delta^X$：速度场对空间位置变化的响应
- $\partial_t v$：速度场对时间变化的直接响应
- $\partial_z v \cdot (\partial_{X_t} z \cdot \Delta^X + \partial_t z)$：隐变量 $z$ 沿轨迹变化对速度的间接影响

该损失通过 Jacobian-Vector Product (JVP) 高效计算。

### 联合训练目标

最终训练损失为 VFM 损失与直性损失的加权和：

$$\mathcal{L}(\theta, \phi) = \mathcal{L}_{\mathrm{VFM}}(\theta, \phi) + \alpha\,\mathcal{L}_{\mathrm{S}}(\theta, \phi)$$

其中 VFM 损失包含速度匹配项与 KL 正则化项：

$$\mathcal{L}_{\mathrm{VFM}}(\theta, \phi) = \mathbb{E}\Big[\|v_\theta(X_t, t, z) - \Delta^X\|^2\Big] + \beta\,D_{KL}\big(q_\phi(z \mid \cdots) \,\|\, p(z)\big)$$

- $\alpha$：直性权重（实验固定为 10）
- $\beta$：KL 散度权重（实验固定为 $10^{-2}$）

当直性条件完全满足时，推论 11 保证生成可一步完成：$X_1 = X_0 + \int_0^1 v^X(X_t, t)\,dt = X_0 + \Delta^X$，积分结果与路径无关。



## 实验与关键发现

### 核心瓶颈与实验动机

Flow Matching（FM）的独立耦合策略导致训练插值路径在数据空间中大量交叉。当多条线性插值 $X_t = (1-t)X_0 + t X_1$ 在相同位置相交时，网络被迫对不兼容的条件速度 $\Delta^X = X_1 - X_0$ 取平均，学习到的边际速度场产生弯曲的生成轨迹。这意味着标准 FM 在少步 ODE 模拟（NFE=1 或 2）时生成质量急剧下降——这是本文实验设计的核心出发点。

S‑VFM 通过两个因果机制解决这一问题：**变分隐变量 $z$** 编码“生成概览”，使速度场能区分交叉的插值线；**直性损失 $\mathcal{L}_S$** 最小化速度场沿特征线的物质导数 $D_t v$，强制轨迹为直线。实验设计围绕验证这两点展开：在 2D 合成数据上可视化轨迹直性，在 CIFAR‑10 和 ImageNet 256×256 上量化少步生成质量。

### 主要定量结果

**CIFAR‑10 32×32（Table 1）。** S‑VFM（自适应归一化变体）在单步生成（NFE=1）上取得 FID 2.81，略优于 iCT 的 2.83，并显著优于其他 Flow Matching 变体及蒸馏方法。关键趋势是：S‑VFM 的 FID 随 NFE 增加**单调下降**——NFE=2 时 FID 降至 2.67，NFE=5 时进一步降至 2.59。这一单调性直接验证了直性损失的有效性：速度场沿轨迹的曲率被抑制，增加积分步数不会引入离散化误差累积，反而稳定提升精度。相比之下，标准 FM 和 VFM 在少步时 FID 显著恶化。

**ImageNet 256×256（Table 2）。** S‑VFM‑XL/2 在 NFE=1 时取得 FID 3.31，大幅领先 iCT‑Deep 的 6.93（差距 -3.62）；NFE=2 时 FID 2.86，对比 iCT‑Deep 的 5.94（差距 -3.08）。S‑VFM‑XL 在 NFE=1 和 NFE=2 下均**一致优于** Consistency Models 和 Mean Velocity Models 等同期少步生成方法。这一结果在高分辨率、高多样性的 ImageNet 上验证了方法的可扩展性。

**训练效率（Figure 5）。** ImageNet 上的 FID‑50K 训练曲线显示，S‑VFM‑XL 在相同训练迭代数下始终优于基线方法，且收敛后 FID 更低。这表明直性约束不仅改善推理质量，还加速了训练收敛。

### 定性分析与轨迹可视化

**2D 合成数据（Figure 1, Figure 2）。** 在六边形和八高斯到月形数据集上，S‑VFM 的生成轨迹呈现近乎完美的直线，而标准 FM 和 VFM 的轨迹明显弯曲。这直观验证了理论分析：独立耦合导致 $V((X_0, X_1)) \neq 0$，速度场无法学习直线路径；引入 $z$ 和 $\mathcal{L}_S$ 后，$D_t v \approx 0$，轨迹变直。

**隐变量的“生成概览”作用（Figure 3, Figure 4）。** Figure 3 展示不同 NFE 下的生成样本，每行对应不同的初始噪声集 $X_0$ 和隐变量集 $z$。即使在 NFE=1 时，生成质量已具有竞争力，且增加 NFE 后细节逐步改善，无模式崩塌。Figure 4 进一步揭示隐变量的核心作用：**相同初始噪声 $X_0$ 但不同 $z$ 产生语义不同的生成结果**（如不同类别或姿态），证明 $z$ 确实编码了全局生成方向，使速度场能沿不同“通道”推进，而非在交叉点取平均。

### 消融实验

**超参数敏感性（Figure 6）。** 对直性损失权重 $\alpha$ 和 KL 散度权重 $\beta$ 的网格搜索显示，在 $\alpha=10, \beta=10^{-2}$ 附近存在**稳定的性能平台**：单步生成 FID 对该区域内的超参数变化不敏感。这降低了调参负担，增强了方法的实用性。

**条件化机制对比。** 两种隐变量注入方式——自适应归一化和瓶颈求和——均取得有竞争力的结果，表明框架对具体实现细节具有鲁棒性。

### 局限与待验证点

*   **超大规模验证缺失。** 论文未在 text‑to‑image 或更高分辨率（如 1024×1024）场景下验证，ImageNet 256×256 的结果虽强，但扩展到更大模型时的直性约束稳定性需手动验证。
*   **隐变量可解释性未量化。** Figure 4 定性展示了 $z$ 的语义控制能力，但缺乏定量指标（如 FID 对 $z$ 变化的敏感性、解耦度量），$z$ 空间的结构化程度需进一步分析。
*   **与蒸馏方法的公平比较。** Table 1/2 中与 iCT 等蒸馏方法的比较，训练预算和模型容量的对齐细节需从原文确认，避免不公平对比。
*   **长尾生成与模式覆盖。** 直性约束是否会导致模式覆盖下降（如牺牲多样性换取轨迹直性）未在实验中专门讨论，需手动检查生成样本的召回率指标。

### 补充图表

![[assets/figures/papers/paper_list_l893_https_arxiv_org_abs_2511_17583/figures/005_Table_1.jpg]]
*Table 1: Quantitative Comparison with Different Generation Methods on CIFAR-10 Dataset. Our method (adaptive normalization variant) achieves the best performance in one-step generation (NFE = 1). Moreover, the FID score consistently decreases as NFE increases*

![[assets/figures/papers/paper_list_l893_https_arxiv_org_abs_2511_17583/figures/006_Table_2.jpg]]
*Table 2: Quantitative Comparison with Different Generation Methods on ImageNet 256 × 256 Dataset. Our method achieves the best performance in few-step generation*

![[assets/figures/papers/paper_list_l893_https_arxiv_org_abs_2511_17583/figures/007_Figure_6.jpg]]
*Figure 6: Ablation Study Results by Adjusting α and β on CIFAR-10 Dataset. The value in the grid represents the FID score of one-step generation (NFE = 1), lower is better*

![[assets/figures/papers/paper_list_l893_https_arxiv_org_abs_2511_17583/figures/003_Figure_3.jpg]]
*Figure 3: Randomly Selected Generation Results under Different NFE. Each row corresponds to a distinct initial noise set (X10 or X20 ) and its associated latent code set*

![[assets/figures/papers/paper_list_l893_https_arxiv_org_abs_2511_17583/figures/004_Figure_4.jpg]]
*Figure 4: Generation results under the same initial noise but different latent codes. Panels (a) and (b) are generated from the same initial noise set*

![[assets/figures/papers/paper_list_l893_https_arxiv_org_abs_2511_17583/figures/001_Figure_1.jpg]]
*Figure 1: Generation Trajectory Visualization in the 2D Synthesized Hexagonal Dataset*

![[assets/figures/papers/paper_list_l893_https_arxiv_org_abs_2511_17583/figures/002_Figure_2.jpg]]
*Figure 2: Generation Trajectory Visualization in the 2D Synthesized Eight-Gaussians-to-Moon Dataset*

![[assets/figures/papers/paper_list_l893_https_arxiv_org_abs_2511_17583/figures/008_Figure_5.jpg]]
*Figure 5: Comparison of FID-50K Score over Training Iterations on ImageNet 256 × 256 Dataset*



## 定位与知识库关联

### 问题根源：Flow Matching 的直性悖论

S‑VFM 的核心动机源于对 **Flow Matching** (Lipman et al., ICLR 2023) 框架下生成轨迹弯曲问题的理论诊断。在标准 Flow Matching 中，训练使用**独立耦合**（independent coupling）——从源分布和目标分布独立采样 $X_0$ 和 $X_1$，构造线性插值路径 $X_t = (1-t)X_0 + t X_1$，并以条件速度 $\Delta^X = X_1 - X_0$ 作为回归目标。然而，不同样本对的插值线在空间中频繁交叉，导致网络学习的边际速度场 $v_\theta(X_t, t)$ 在交叉点处被迫对多个不兼容的方向取平均，产生弯曲的生成轨迹。

论文在 Section 4.1 中给出了严格的理论表述：Flow Matching 学习直线生成轨迹的目标等价于要求速度场的条件方差满足 $V((X_0, X_1)) = 0$，但在独立耦合下该条件**不可达**，因为交叉插值线必然引入非零的条件方差。这构成了 Flow Matching 框架的根本性矛盾——训练所用的插值路径是直线，但模型无法学到直线轨迹，必须依赖多步 ODE 模拟来补偿弯曲带来的积分误差。

### 与变分流匹配 (VFM) 的继承与突破

S‑VFM 的直接前身是 **Variational Flow Matching (VFM)** (Ma et al., ICML 2025)。VFM 首次在 Flow Matching 中引入变分隐变量 $z$，通过 VAE 结构的后验编码器 $q_\phi(z \mid X_0, X_1, X_t, t)$ 提取全局“生成概览”（generation overview），使速度网络 $v_\theta(X_t, t, z)$ 能够感知每个样本对的整体信息。这一设计突破了独立耦合下模型只能看到局部插值点 $X_t$ 的限制，为区分交叉路径提供了信息基础。

然而，VFM 的训练目标仅包含速度匹配损失和 KL 正则化项，**缺乏对轨迹几何性质的显式约束**。S‑VFM 的关键突破在于引入直性损失 $\mathcal{L}_S$，通过最小化速度场沿特征线的物质导数 $D_t v$，从几何层面强制轨迹趋近直线。Theorem 5 证明了直性条件 $D_t v = 0$ 与 $V((X_0, X_1)) = 0$ 的等价性，将几何直觉转化为可优化的目标函数。这一理论桥梁使得 S‑VFM 在继承 VFM 隐变量机制的同时，从根本上解决了轨迹弯曲问题。

### 与其他直性/少步生成方法的对比

**Rectified Flow** (Liu et al., ICLR 2023) 采用迭代蒸馏策略来消除插值交叉：通过多轮“重采样-重训练”逐步拉直轨迹，每轮使用上一轮模型生成的源-目标对作为新的耦合。该方法在理论上保证收敛到直线轨迹，但需要多次完整训练流程，计算开销巨大。S‑VFM 通过隐变量和直性损失的联合优化，**在单轮训练中**即实现轨迹拉直，避免了迭代蒸馏的重复成本。

**Consistency Models (CT)** (Song et al., ICML 2023) 通过自一致性约束迫使模型将同一起点在不同时间步的输出映射到同一终点，从而实现少步生成。CT 的改进版 iCT 在 CIFAR‑10 和 ImageNet 上取得了有竞争力的少步生成效果。从 Table 1 和 Table 2 的对比来看，S‑VFM 在一步生成（NFE=1）上全面超越 iCT：CIFAR‑10 上 FID 为 2.81 vs. 2.83，ImageNet 256×256 上为 3.31 vs. 6.93。更重要的是，S‑VFM 的 FID 随 NFE 增加单调下降（Table 1），验证了其轨迹确实接近直线——增加积分步数不会引入显著的离散化误差，而是持续逼近真实分布。

**MeanFlow** 基于平均速度场建模，试图直接学习从源到目标的平均速度向量，但缺乏对轨迹中间行为的约束。S‑VFM 的直性损失作用于整个时间区间 $t \in [0,1]$，对轨迹的全局几何性质施加控制，理论上更完备。

### 方法边界与适用条件

S‑VFM 的有效性依赖于两个关键前提：

1. **隐变量信息充分性**：变分后验 $q_\phi$ 需要能从 $(X_0, X_1, X_t, t)$ 中提取足够区分不同插值路径的全局信息。当数据分布具有高度多模态或样本对之间的交叉模式过于复杂时，隐变量的表示能力可能成为瓶颈。Figure 4 展示了相同初始噪声在不同隐变量下生成不同样本的能力，验证了 $z$ 确实编码了有意义的生成概览，但其信息容量的理论上限有待进一步分析。

2. **直性损失的可优化性**：$\mathcal{L}_S$ 的计算涉及速度场对空间、时间和隐变量的偏导数（通过 JVP 实现），引入了额外的计算开销和优化难度。Figure 6 的消融实验显示，在 $\alpha=10, \beta=10^{-2}$ 附近存在稳定的性能平台，表明方法对超参数不敏感，但该结论仅在 CIFAR‑10 上验证，更大规模数据上的超参数鲁棒性需要进一步确认。

### 局限与开放问题

当前分析中未提供论文明确声明的局限性。基于方法设计可识别以下潜在边界：

- **计算开销**：直性损失 $\mathcal{L}_S$ 需要计算速度场的物质导数，涉及空间梯度和时间导数，相比标准 Flow Matching 增加了反向传播的复杂度。论文未报告训练时间或显存占用的对比数据，实际部署效率需要手动验证。
- **隐变量先验假设**：推理时从固定先验 $p(z) = \mathcal{N}(0, I)$ 采样单个 $z$ 贯穿整个时间区间。当目标分布与先验不匹配时，单隐变量可能不足以覆盖所有生成模式，导致样本多样性受限。论文未提供多样性指标（如 Recall 或 Coverage）的对比。
- **理论完备性**：Theorem 5 证明了 $D_t v = 0$ 与直性条件的等价性，但该结论建立在速度场精确匹配条件速度的假设上。实际训练中速度匹配损失和直性损失存在权衡，两者联合优化的收敛性质尚未得到理论刻画。
- **扩展到其他模态**：当前实验限于 CIFAR‑10 和 ImageNet 的图像生成任务，方法在文本、音频或分子生成等领域的适用性未经验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/Learning_Straight_Flows_Variational_Flow_Matching_for_Efficient_Generation.pdf]]
