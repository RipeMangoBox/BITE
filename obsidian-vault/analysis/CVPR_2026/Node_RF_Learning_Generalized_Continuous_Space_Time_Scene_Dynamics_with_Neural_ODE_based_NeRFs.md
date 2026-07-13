---
title: "Node-RF: Learning Generalized Continuous Space-Time Scene Dynamics with Neural ODE-based NeRFs"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Node_RF_Learning_Generalized_Continuous_Space_Time_Scene_Dynamics_with_Neural_ODE_based_NeRFs.pdf
project_link: null
code_link: null
aliases:
- NR
- Node-RF
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 引入神经ODE（Neural ODE）将场景动力学建模为潜在状态在连续时间上的演化，从而将离散帧序列转化为平滑的微分方程驱动轨迹。
primary_logic: 将动态场景视为由ODE控制的潜在空间轨迹，结合NeRF体积渲染，使模型能够从任意时间点采样并进行长期外推，同时支持跨序列泛化。
claims:
- 在Bouncing Balls数据集的长期外推（4倍）中，Node-RF在LLaVA-Video相似度(Sim2)、运动平滑度(MS)和主体一致性(SC)上均优于所有基线方法
- 在Pendulum数据集上，Node-RF在插值和外推的PSNR、SSIM、LPIPS指标上均超越D-NeRF和4D-GS，并在外推PSNR上超过SimVP
- 在多序列泛化实验中，Node-RF在Oscillating Ball和Bifurcating Hill数据集上均取得最高IoU
- Lipschitz正则化对塑造结构化的潜在空间至关重要，未使用该正则化时模型难以收敛到代表系统动力学的潜在结构
---

# Node-RF: Learning Generalized Continuous Space-Time Scene Dynamics with Neural ODE-based NeRFs

> [!tip] 核心洞察
> 将动态场景视为由ODE控制的潜在空间轨迹，结合NeRF体积渲染，使模型能够从任意时间点采样并进行长期外推，同时支持跨序列泛化。

| 字段 | 内容 |
|------|------|
| 中文题名 | Node-RF：利用神经ODE的NeRF学习广义连续时空场景动力学 |
| 英文题名 | Node-RF: Learning Generalized Continuous Space-Time Scene Dynamics with Neural ODE-based NeRFs |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.12078) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Node-RF |
| Dataset | Bouncing Balls, Pendulum, Oscillating Ball, Bifurcating Hill |

> [!tip] 效果简介
> - Bouncing Balls (4× Extrapolation) 上，Sim2 ↑ (LLaVA-Video Similarity) 0.7937 vs 0.7883 (TiNeuVox*) (+0.0054)；MS ↑ (Motion Smoothness) 0.99648 vs 0.99617 (HexPlane*) (+0.00031)。
> - Pendulum (Interpolation) 上，PSNR ↑ 17.057 vs 13.906 (D-NeRF) (+3.151)。
> - Pendulum (Extrapolation) 上，PSNR ↑ 15.920 vs 15.804 (SimVP) (+0.116)。

## 概要

动态场景的3D重建与重渲染是计算机视觉的核心挑战之一，其关键瓶颈在于**时间维度的连续建模能力**。现有动态NeRF方法（如**D-NeRF**（Pumarola et al., CVPR 2021）、**HexPlane**、**TiNeuVox**等）以及基于3D高斯泼溅的方法（如**4D-GS**、**Motion-GS**）虽然在离散训练帧上表现出色，但它们仅学习离散时间索引对应的场景状态，缺乏对连续时间动态的内在理解。这导致两个根本性缺陷：一是**长期外推能力不足**——模型无法预测训练时间窗口之外的场景状态；二是**无法泛化到新的初始条件**——每个动态序列需要独立训练一个模型，无法将学到的物理规律迁移到同一系统下不同初始状态的轨迹上。

**Node-RF** 针对上述瓶颈提出了一个统一的解决方案。其核心思想是将神经常微分方程（Neural ODE）与动态NeRF深度融合：将动态场景视为由ODE控制的潜在空间轨迹，通过微分方程求解器在连续时间轴上传播场景的隐式状态，从而将离散帧序列转化为平滑的微分方程驱动演化。这一设计实现了三个关键突破：

- **连续时间动态建模**：神经ODE求解器 $f_\theta$ 根据初始潜在码 $z_{t_0}$ 生成任意时刻的潜在表示 $z_t = \mathrm{ODESolve}(f_\theta, z_{t_0}, t)$，使模型能够从任意时间点采样并进行渲染，天然支持插值和外推。
- **跨序列泛化能力**：通过学习一个共享的动力学ODE，模型仅需输入物体的初始条件（位置和速度）即可预测全新的运动轨迹，无需为新序列重新训练。
- **结构化潜在空间**：引入Lipschitz权重归一化正则化，约束NeRF线性层的Lipschitz常数，促使潜在空间平滑且具有物理可解释的结构——例如，系统稳态对应于潜在空间中的“汇”（sink），轨迹收敛方向与潜在散度 $\nabla z_t < 0$ 一致。

在实验验证上，Node-RF在多个基准上展示了显著优势：

- **长期外推**：在Bouncing Balls数据集的4倍外推任务中，Node-RF在LLaVA-Video相似度（Sim2: 0.7937）、运动平滑度（MS: 0.99648）和主体一致性（SC: 0.97775）上均优于所有基线方法（Table 1）。
- **插值与外推精度**：在Pendulum数据集上，Node-RF的插值PSNR达到17.057 dB，较D-NeRF提升3.151 dB；外推PSNR达到15.920 dB，超越SimVP等专用视频预测模型（Table 2）。
- **多序列泛化**：在Oscillating Ball和Bifurcating Hill数据集上，Node-RF分别取得0.3327和0.485的IoU，显著优于条件化基线D-NeRF(c)和Vid-ODE（Table 3）。

消融实验进一步验证了设计选择的合理性：位姿和速度辅助损失对泛化性能有显著增益；Lipschitz正则化是构建结构化潜在空间的关键，缺少该正则化时模型难以收敛到代表系统动力学的潜在结构（Figure 8）；神经ODE以3层MLP为最优配置，过深会导致性能下降（Table 6）。

**方法定位**：Node-RF处于动态NeRF、神经ODE和物理启发式表示学习的交叉点。与现有动态NeRF方法相比，它首次将ODE驱动的连续时间演化直接嵌入体积渲染框架，实现了从“离散帧拟合”到“连续动力学学习”的范式转变。与**SimVP**、**Vid-ODE**等2D视频预测方法相比，Node-RF在3D场景中保持多视图一致性，且不依赖固定时间间隔假设。该方法为确定性物理系统的3D动力学建模提供了新的基准思路，但在随机动力学、非刚性变形以及大规模真实场景中的适用性仍有待探索。



### 动态场景建模的核心挑战

三维动态场景的逼真重建与渲染是计算机视觉与图形学中的基础难题。以神经辐射场（NeRF）为代表的隐式神经表示，在静态场景的新视角合成上取得了突破性进展，但其向动态场景的扩展仍面临根本性瓶颈。现有动态NeRF方法——如**D-NeRF**（Pumarola et al., CVPR 2021）、**HexPlane**、**TiNeuVox**、**4D-GS**和**Motion-GS**等——虽然在插值任务上表现优异，却普遍存在一个关键缺陷：它们仅在离散的训练时间步上学习场景变化，缺乏对连续时间动态的建模能力。这意味着模型无法理解时间步之间的平滑过渡机制，更无法在训练时间范围之外进行可信的长期外推。

### 现有方法的根本瓶颈

这一缺陷的根源在于表示机制的设计。主流动态NeRF方法通常为每个离散帧分配独立的潜在编码，或使用时间条件变形场将采样点映射到规范空间。这种“逐帧索引”的范式将时间建模退化为一个查表操作，而非真正的动力学学习。其直接后果是：当测试时间超出训练分布时，模型缺乏任何物理或几何先验来约束预测，导致渲染质量急剧退化。此外，这些方法对每个动态序列独立训练一个模型，完全无法泛化到未见过的初始条件——即便新序列遵循完全相同的物理规律。

### 连续时间建模的契机

神经常微分方程（Neural ODE）的提出为上述困境提供了自然的解决思路。Neural ODE将隐藏状态的演化建模为由神经网络参数化的微分方程：

$$\frac{d h(t)}{d t} = f_{\theta}(h(t), t), \quad \text{with} \quad h(t_0) = h_0$$

这一框架的核心优势在于：它天然地将离散观测序列转化为连续时间轨迹，支持任意时刻的查询，并强制状态之间的平滑过渡。在视频生成领域，**Vid-ODE**和**SimVP**等方法已初步验证了ODE在2D像素空间中的时序建模潜力，但这些方法仅处理单视图2D视频，无法利用多视角几何约束，也难以扩展到3D体积渲染框架。

### 本文动机：从离散帧到连续动力学

本文的核心动机在于弥合上述两个方向之间的鸿沟——将Neural ODE的连续时间动力学能力与NeRF的3D体积渲染框架深度融合，构建一个真正能够学习、外推并泛化场景动力学的统一表示。具体而言，我们希望模型能够：

1. **连续时间建模**：从离散的多视角帧中学习一个隐式场景状态，该状态通过ODE求解器在连续时间轴上平滑演化，而非仅在训练帧上插值。
2. **长期外推**：在训练时间范围的数倍之外，仍能生成物理合理、视觉连贯的渲染结果。
3. **跨序列泛化**：从多个共享相同动力学规律的序列中学习一个通用的ODE，仅需输入新的初始条件（位置与速度）即可预测完整的新轨迹。

### 技术挑战与设计方向

实现上述目标面临多重挑战。首先，NeRF的体积渲染本身计算开销巨大，在其之上叠加ODE求解器的迭代积分将进一步增加训练负担。其次，如何将不同初始条件下的多序列信息压缩到一个共享的潜在动力学空间中，同时保持足够的表达能力来区分不同轨迹，是一个非平凡的表示学习问题。最后，若无适当的正则化，神经ODE学到的潜在空间可能缺乏结构，导致动力学行为不可解释且泛化能力受限。本文提出的Node-RF框架正是围绕这些挑战展开设计，其核心架构与实验验证将在后续章节中详述。



## 核心方法与创新机理

Node-RF 的核心创新在于将**神经常微分方程（Neural ODE）**与**动态神经辐射场（NeRF）**深度融合，从而将离散的帧序列转化为连续时间上的平滑动力学轨迹。现有动态 NeRF 方法（如 **D-NeRF**（Pumarola et al., CVPR 2021））在每个训练时间步上学习独立的潜在码或变形场，缺乏对时间连续性的显式建模，导致长期外推能力不足，且无法泛化到未见过的初始条件。Node-RF 通过以下三个关键设计突破这一瓶颈。

### 1. 神经 ODE 驱动的连续时间潜在演化

Node-RF 将场景动力学建模为潜在空间中的微分方程初值问题：

$$z_{t_0}, \ldots, z_{t_N} = \mathrm{ODESolve}(f_{\theta}, z_{t_0}, (t_0, \ldots, t_N))$$

其中神经 ODE 模块 $f_{\theta}$ 捕获潜在表示在时间维度上的连续演化，生成与视角无关的潜在表示 $z_t$。这一设计将时间建模从“离散帧索引的查找”转变为“微分方程驱动的平滑轨迹”，使得模型可以从任意时间点采样并进行长期外推。在 Pendulum 数据集上，这一连续时间建模能力使 Node-RF 的外推 PSNR 达到 15.920，超越了基于离散帧预测的 **SimVP**（15.804），并在插值 PSNR 上以 17.057 大幅领先 **D-NeRF** 的 13.906（Table 2）。

### 2. 多序列泛化的初始条件编码

传统动态 NeRF 为每个序列独立训练一个模型，无法泛化到新的初始条件。Node-RF 引入编码器 $E$，将物体的初始位姿 $p^c$ 映射为条件向量，使得共享的神经 ODE 能够根据不同初始条件生成对应的潜在轨迹。在 Oscillating Ball 和 Bifurcating Hill 数据集的多序列泛化实验中，Node-RF 分别取得 0.3327 和 0.485 的 IoU，均优于条件化改进的 **D-NeRF(c)**（0.2807）和 **Vid-ODE**（0.409）（Table 3）。这一能力源于模型学习的是“动力学规律”而非“特定序列的记忆”。

### 3. 辅助监督与 Lipschitz 正则化的协同作用

Node-RF 在 NeRF 重建损失 $\mathcal{L}_{NeRF}$ 之外，引入位姿损失 $\mathcal{L}_{p}$ 和速度损失 $\mathcal{L}_{v}$ 作为辅助监督：

$$\mathcal{L} = \lambda_1 \mathcal{L}_{NeRF} + \lambda_2 \mathcal{L}_{p} + \lambda_3 \mathcal{L}_{v} + \lambda_4 \mathcal{L}_{lipschitz}$$

消融实验（Table 4）表明，仅靠 NeRF 重建损失即可使框架具备基本泛化能力，但添加位姿和速度辅助损失能显著提升指标。更关键的是，Lipschitz 正则化通过对 NeRF 线性层施加权重归一化：

$$W_i \gets \mathrm{normalization}(W_i, \mathrm{softplus}(c_i))$$

并惩罚网络的 Lipschitz 上界 $\mathcal{L}_{lipschitz} = \prod_i \mathrm{softplus}(c_i)$，强制潜在空间变得平滑结构化。Figure 8 的对比显示，未使用 Lipschitz 正则化时模型难以收敛到代表系统动力学的潜在结构，而引入正则化后潜在轨迹呈现清晰的收敛模式（绿色起点到红色终点的平滑流动），这是 Node-RF 能够进行长期稳定外推的关键机制。

**总结**：Node-RF 的创新并非单一技术点的替换，而是通过“神经 ODE 连续演化 + 初始条件编码 + Lipschitz 结构化正则化”的组合，将动态 NeRF 从“离散帧拟合”提升为“连续动力学学习”，从而同时获得长期外推和跨序列泛化能力。



Node-RF 的核心设计思路是将动态场景的时空演化建模为神经ODE驱动的连续潜在轨迹，再通过NeRF体积渲染实现新视角合成。整个框架围绕一个关键因果机制展开：**用微分方程替代离散帧索引，使场景状态在时间维度上具有连续性和可外推性**。

### 双模式架构设计

框架支持两种训练模式，共享同一个NeRF渲染核心，但在潜在状态初始化上有所区别（Figure 2）：

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2603_12078/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Node-RF*

**单序列连续动力学模式**：针对单个动态序列，模型需要从观测中推断出隐含的初始状态。具体做法是先用两帧预热（warmup）学习 $z_{t_0}$ 和 $z_{t_1}$，然后通过 **ODE-RNN 变分自编码器** 根据这两个潜在码学习潜在初始状态的分布，从中采样获得ODE求解的起点 $z_{t_0}$。随后神经ODE求解器沿时间轴积分，生成连续时间点的潜在表示序列 $z_{t_0}, \ldots, z_{t_N}$。

**多序列泛化模式**：当多个序列遵循相同的确定性动力学但具有不同初始条件时，框架学习一个共享的动力学ODE。输入变为物体的初始位姿 $p^c$，经过编码器 $E$ 映射为条件向量，再与可学习的规范潜在码 $z_{can}$ 结合形成初始潜在状态。这种设计使得模型能够泛化到训练中未见过的初始条件。

### 模块关系与数据流

框架由以下核心模块串联构成，数据流从视觉观测到渲染输出形成闭环：

1. **静态背景 NeRF 模块**：独立学习与时间无关的静态场景部分，在预热阶段训练，为后续动态建模提供稳定的背景先验。

2. **神经 ODE 模块 $f_\theta$**：这是框架的动力学核心。给定初始潜在状态 $h(t_0)$，ODE求解器按 $\frac{d h(t)}{d t} = f_{\theta}(h(t), t)$ 沿连续时间轴积分，生成各时刻的视角无关潜在表示 $z_t$。这一步骤将离散的帧序列转化为平滑的微分方程驱动轨迹，是实现连续时间建模和长期外推的关键。

3. **解码器组 $D_n, D_p, D_v$**：在多序列泛化模式下，动态潜在码分别输入三个解码器——$D_n$ 输出场景动态特征供NeRF使用；$D_p$ 预测物体位姿；$D_v$ 预测物体速度。后两者提供辅助监督信号。

4. **NeRF 渲染器 $F_\Theta$**：接收空间位置 $\mathbf{x}$、视角方向 $\mathbf{d}$ 和时间潜在码 $z_t$，映射为颜色 $\mathbf{c}$ 和密度 $\sigma$，再通过体积渲染积分沿相机射线计算像素颜色：
   $$C_t(\mathbf{r}) = \int_{s_n}^{s_f} T(s) \sigma(\mathbf{r}(s), z_t) \mathbf{c}(\mathbf{r}(s), \mathbf{d}, z_t) ds$$

5. **Lipschitz 正则化层**：应用于NeRF的线性层，通过可训练的Lipschitz界 $c_i$ 对权重矩阵进行归一化：
   $$W_i \gets \mathrm{normalization}(W_i, \mathrm{softplus}(c_i))$$
   对应的正则化损失 $\mathcal{L}_{lipschitz} = \prod_i \mathrm{softplus}(c_i)$ 惩罚网络各层的Lipschitz上界，强制潜在空间平滑结构化。消融实验（Figure 8）表明，缺乏该正则化时模型难以收敛到代表系统动力学的潜在结构。

### 训练损失构成

总损失为四项的加权组合：
$$\mathcal{L} = \lambda_1 \mathcal{L}_{NeRF} + \lambda_2 \mathcal{L}_{p} + \lambda_3 \mathcal{L}_{v} + \lambda_4 \mathcal{L}_{lipschitz}$$

其中 $\mathcal{L}_{NeRF}$ 是所有帧、粗细层次和所有射线的L2颜色重建损失；$\mathcal{L}_{p}$ 和 $\mathcal{L}_{v}$ 分别是位姿和速度的L1辅助损失（仅多序列模式）；$\mathcal{L}_{lipschitz}$ 是潜在空间平滑正则项。消融实验（Table 4）证实，仅靠NeRF重建损失已能使框架泛化到新初始条件，但添加位姿和速度辅助损失能显著提升指标，Lipschitz正则化进一步改善潜在空间结构和性能。

### 关键设计选择

框架对几个超参数较为敏感。潜在向量维度从256增至512带来性能提升，但继续增至1024会导致过拟合（Table 5）。神经ODE的MLP深度以3层最优，5层或7层均造成性能下降或学习失败（Table 6）。预热阶段使用的潜在向量数量对性能影响不大，2个即可捕获初始动态（Table 7）。训练时间随序列长度线性增长，多序列泛化实验约需3天（Table 8）。

### 补充图表

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2603_12078/figures/001_Figure_1.jpg]]
*Figure 1: Node-RF Overview. Multiple observations of the red ball being dropped onto the dual ramp end in damped oscillations towards the two valleys. Node-RF learns to encodes generalized dynamics of deterministic motions from sequences such as A (pink), C (yellow) into an implicit space-time latent representation using NeRF and nODE. Embedded sequence states depicted as scene latent points zt on the embedding space are propagated through time t using an implicit neural ODE. Intermediate and future states (centre to right encodings) can be extrapolated and rendered (top, bottom) given initial frame conditions (on the left). Latent divergence ∇zt (colour coded) characterizes behaviour of the learnt s...*



### 整体架构

Node-RF 将神经辐射场（NeRF）与神经常微分方程（Neural ODE）深度融合，构建了一个连续时间隐式体积表示框架。其核心思想是：将动态场景视为由 ODE 控制的潜在空间轨迹，潜在状态 $z_t$ 在连续时间上平滑演化，NeRF 渲染器则根据 $z_t$ 将三维场景映射为图像。这一设计使模型能够从任意时间点采样并进行长期外推。

框架包含六个关键模块（见 Figure 2）：

1. **静态背景 NeRF 模块**：学习并渲染与时间无关的静态背景，与动态前景解耦。
2. **神经 ODE 模块 $f_\theta$**：根据初始条件通过微分方程求解器传播潜在状态，生成各时刻的潜在表示，是连续时间建模的核心引擎。
3. **编码器 $E$**：将物体初始位姿 $p^c$ 编码为条件向量，注入 ODE 的初始状态。
4. **解码器组 $D_n, D_p, D_v$**：分别将动态潜在解码为场景动态特征、预测位姿和预测速度，提供多任务监督信号。
5. **NeRF 渲染器 $F_\Theta$**：将空间位置 $\mathbf{x}$、视角方向 $\mathbf{d}$ 和潜在码 $z_t$ 映射为颜色 $\mathbf{c}$ 和密度 $\sigma$，进行体积渲染。
6. **Lipschitz 正则化层**：应用于 NeRF 的线性层，约束权重矩阵的 Lipschitz 常数，增强潜在空间的平滑性和结构化程度。

### 关键公式推导

**动态 NeRF 映射。** 基础映射函数将空间位置、视角方向和时间潜在码映射为颜色和密度：

$$F_{\Theta}(\mathbf{x}, \mathbf{d}, z_t) = (\mathbf{c}, \sigma) \tag{1}$$

**体积渲染。** 从相机射线在时间 $t$ 的积分计算像素颜色：

$$C_t(\mathbf{r}) = \int_{s_n}^{s_f} T(s) \sigma(\mathbf{r}(s), z_t) \mathbf{c}(\mathbf{r}(s), \mathbf{d}, z_t) ds \tag{2}$$

其中 $T(s) = \exp(-\int_{s_n}^{s} \sigma(\mathbf{r}(u), z_t) du)$ 为累积透射率，$s_n$ 和 $s_f$ 分别为射线的近远边界。

**NeRF 重建损失。** 累计所有帧、粗/细层次和所有射线的 L2 颜色差异：

$$\mathcal{L}_{NeRF} = \sum_{t \in T, j \in J, \mathbf{r} \in R} \left\| \hat{C}_t^j(\mathbf{r}) - C_t(\mathbf{r}) \right\|_2^2 \tag{4}$$

**神经 ODE 定义。** 连续时间动态系统的隐藏状态演化由神经网络参数化的微分方程控制：

$$\frac{d h(t)}{d t} = f_{\theta}(h(t), t), \quad \text{with} \quad h(t_0) = h_0 \tag{5}$$

**ODE 求解生成潜在序列。** 使用数值 ODE 求解器从初始潜在码生成连续时间潜在轨迹，这是实现连续时间建模的关键操作：

$$z_{t_0}, \ldots, z_{t_N} = \mathrm{ODESolve}(f_{\theta}, z_{t_0}, (t_0, \ldots, t_N)) \tag{7}$$

**位姿和速度辅助损失。** 在多序列泛化任务中，解码器 $D_p$ 和 $D_v$ 分别预测物体位姿和速度，通过 L1 损失提供额外监督：

$$\mathcal{L}_{p} = \frac{1}{T} \sum_{i=0}^{T} \left| \hat{p}_{t_i}^c - p_{t_i}^c \right|, \quad \mathcal{L}_{v} = \frac{1}{T-1} \sum_{i=0}^{T-1} \left| \hat{v}_{t_i}^c - v_{t_i}^c \right| \tag{9}$$

**总训练损失。** 加权组合图像重建、姿态、速度和 Lipschitz 正则化损失：

$$\mathcal{L} = \lambda_1 \mathcal{L}_{NeRF} + \lambda_2 \mathcal{L}_{p} + \lambda_3 \mathcal{L}_{v} + \lambda_4 \mathcal{L}_{lipschitz} \tag{10}$$

**Lipschitz 权重归一化。** 利用可训练的 Lipschitz 界 $c_i$ 对权重矩阵进行归一化，约束每层的 Lipschitz 常数：

$$W_i \gets \mathrm{normalization}(W_i, \mathrm{softplus}(c_i)) \tag{11}$$

**Lipschitz 正则化损失。** 惩罚网络各层的 Lipschitz 上界，促使更平滑的潜在表示：

$$\mathcal{L}_{lipschitz} = \prod_i \mathrm{softplus}(c_i) \tag{12}$$

### 单序列与多序列模式

Node-RF 支持两种训练模式（见 Figure 2）：

- **单序列模式**：使用 ODE-RNN 变分自编码器，根据前两帧的潜在码学习潜在初始状态的分布，再采样获得起点用于 ODE 求解（Algorithm 1）。该模式适用于单一动态序列的连续时间建模。
- **多序列泛化模式**：学习一个共享的动力学 ODE，只需输入初始条件（位置和速度）即可预测新轨迹。编码器 $E$ 将物体初始位姿 $p^c$ 编码为条件向量，注入 ODE 的初始状态，解码器组提供位姿和速度的辅助监督（Algorithm 2）。

### 模块间的因果机制

整个框架的因果链条为：**初始条件 → 编码器 → ODE 求解器 → 潜在轨迹 → 解码器/渲染器 → 图像/位姿预测**。其中，神经 ODE 模块 $f_\theta$ 是瓶颈组件——它决定了潜在状态在时间维度上的演化质量。Lipschitz 正则化在此处起到关键的约束作用：消融实验（Figure 8）表明，未使用该正则化时模型难以收敛到代表系统动力学的潜在结构，潜在空间呈现杂乱无章的分布；而施加正则化后，潜在轨迹呈现出清晰的汇聚结构（绿色起点向红色终点流动），与物理系统的吸引子行为一致。

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2603_12078/figures/011_Figure_8.jpg]]
*Figure 8: Latent Space Comparison of models w/o and w/ Lipschitz regularization. The green and red dots represent the starting and ending points of the trajectories respectively*



## 实验与关键发现

### 核心实验设置与评估协议

Node-RF 在三个不同维度的任务上接受检验：**单序列连续动力学建模**、**长期外推**以及**跨序列泛化**。评估涵盖 2D 单视图与 3D 多视图场景，数据集包括 Bouncing Balls、Pendulum、Oscillating Ball 和 Bifurcating Hill。

评估指标因任务而异：
- 对 Bouncing Balls 长期外推，采用 VBench 的 **Motion Smoothness (MS)** 和 **Subject Consistency (SC)**，以及基于 X-CLIP 和 LLaVA-Video 的提示相似度（**Sim1** 和 **Sim2**）。
- 对 Pendulum 数据集，使用传统的图像重建指标 **PSNR**、**SSIM** 和 **LPIPS**，仅评估前景动态部分。
- 对跨序列泛化任务，采用动态流掩膜的 **IoU** 作为核心度量。

公平性方面需注意：SimVP 假设固定时间间隔 Δt，无法进行插值评估；Vid-ODE 不处理相机姿态，仅在 2D Bifurcating Hill 上比较；D-NeRF(c) 是为多序列泛化定制的条件化版本，3D 基线无法直接处理 2D 单视图泛化数据集。

### 长期外推：Bouncing Balls 数据集

Table 1 展示了 Bouncing Balls 数据集上 4 倍外推的定量对比。Node-RF 在 LLaVA-Video 相似度（Sim2: **0.7937**）、运动平滑度（MS: **0.99648**）和主体一致性（SC: **0.97775**）三项指标上均取得最优。值得关注的是，Node-RF 在运动平滑度上的优势（相对次优的 HexPlane 提升 0.00031）虽然数值微小，但考虑到该指标已接近饱和（所有方法均在 0.99 以上），这一提升仍具统计意义。在 Sim1（X-CLIP 相似度）上，Node-RF 的 **0.9163** 略低于 TiNeuVox 的 0.9196，差距约 0.0033。

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2603_12078/figures/003_Table_1.jpg]]
*Table 1: Long-term (4×) Extrapolation comparison on Bouncing Balls [24]. * indicates retraining. SIM1: X-CLIP Similarity, SIM2: LLaVA-Video Similarity. MS: Motion Smoothness, SC: Subject Consistency*

定性结果（Figure 4）进一步验证：基线方法如 D-NeRF 在外推后期出现明显的球体模糊和轨迹漂移，而 Node-RF 能保持清晰的球体边界和准确的碰撞反弹轨迹。这归因于神经 ODE 提供的连续时间动力学约束——它迫使潜在状态沿平滑的微分方程轨迹演化，而非像离散帧索引方法那样在训练帧之间进行无约束的插值。

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2603_12078/figures/007_Figure_4.jpg]]
*Figure 4: Long-term extrapolations, Bouncing Balls[24] scene*

### 插值与外推：Pendulum 数据集

Table 2 报告了 Pendulum 数据集的结果。在插值任务上，Node-RF 以 **PSNR 17.057**、**SSIM 0.531** 和 **LPIPS 0.0234** 全面超越 D-NeRF（PSNR 13.906）和 4D-GS。这一优势在外推任务上延续：Node-RF 的 PSNR 达到 **15.920**，LPIPS 为 **0.0257**，均优于所有 3D 基线。

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2603_12078/figures/004_Table_2.jpg]]
*Table 2: Comparison on Pendulum [9]. Evaluated only on the foreground dynamic part. Interpolation and extrapolation are reported*

与 2D 视频预测模型 SimVP 相比，Node-RF 在外推 PSNR 上小幅领先（15.920 vs. 15.804），但需注意 SimVP 仅能处理单视图 2D 视频，且无法进行插值评估。Node-RF 的独特优势在于其 `Temporal Continuity` 能力——神经 ODE 求解器可以从任意连续时间点采样，这是所有对比的 3D 基线（D-NeRF、4D-GS、HexPlane、TiNeuVox、Motion-GS）所不具备的。

Figure 3 的定性对比显示，D-NeRF 在外推帧中摆锤边缘出现伪影，而 Node-RF 保持了清晰的几何边界和正确的摆动相位。

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2603_12078/figures/005_Figure_3.jpg]]
*Figure 3: Extrapolation results on the Pendulum dataset [9]*

### 跨序列泛化：Oscillating Ball 与 Bifurcating Hill

Table 3 展示了最具挑战性的泛化实验——模型在训练序列之外的全新初始条件下预测动力学。Node-RF 的核心设计优势在此充分体现：通过学习一个共享的动力学 ODE 并条件化初始状态（位置和速度），模型无需为每个新序列重新训练。

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2603_12078/figures/006_Table_3.jpg]]
*Table 3: Comparison on Oscillating Ball (3D) and Bifurcating Hill (2D) on IoU between GT and prediction flows. A ✓ under 3D indicates that the method can handle 3D scenes*

在 3D Oscillating Ball 数据集上，Node-RF 的 **IoU 0.3327** 显著优于条件化 D-NeRF(c) 的 0.2807（提升约 18.5%）。在 2D Bifurcating Hill 数据集上，Node-RF 的 **IoU 0.485** 同样领先于 Vid-ODE 的 0.409（提升约 18.6%）。Figure 6 和 Figure 7 的动态流掩膜可视化表明，Node-RF 能准确预测新轨迹中球的运动区域，而基线方法在分叉点附近出现明显的流预测错误。

Figure 5 进一步分析了 Bifurcating Hill 中新轨迹的位姿误差随时间的变化：Node-RF 的位姿误差在整个预测窗口内保持相对稳定，未出现典型的误差累积发散现象，这验证了 ODE 驱动的潜在动力学具有长期数值稳定性。

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2603_12078/figures/008_Figure_5.jpg]]
*Figure 5: Pose error for a novel trajectory in Bifurcating Hill*

### 消融实验

**损失项消融**（Table 4，Oscillating Ball 数据集）：仅使用 NeRF 重建损失（$\mathcal{L}_{NeRF}$）即可使框架具备基本的泛化能力，但添加位姿损失（$\mathcal{L}_p$）和速度损失（$\mathcal{L}_v$）后 IoU 显著提升。进一步引入 Lipschitz 正则化（$\mathcal{L}_{lipschitz}$）后性能达到最优，验证了这三种辅助监督各自独立贡献于动力学学习。

**潜在维度消融**（Table 5，Bouncing Balls 重建集）：潜在向量维度从 256 增至 512 带来性能提升，但继续增至 1024 会导致过拟合，指标反而下降。这表明 512 维在表达能力和泛化性之间达到了平衡。

**nODE 深度消融**（Table 6，Oscillating Ball）：神经 ODE 的 MLP 深度以 3 层最优。5 层造成性能下降，7 层则导致学习失败——过深的 ODE 网络可能使微分方程过于复杂，难以通过数值求解器稳定传播梯度。

**预热潜在数量消融**（Table 7，Bouncing Balls 重建集）：预热阶段使用的潜在向量数量对性能影响不大，2 个即可有效捕获初始动态，增加数量仅略微提升外推稳定性。这暗示 ODE-RNN 变分自编码器从两帧中已能充分推断初始状态分布。

**训练时间**（Table 8）：训练时间随序列长度线性增长，多序列泛化实验约需 3 天（72 小时），这是该方法目前的主要计算瓶颈。

### Lipschitz 正则化的关键作用

Figure 8 揭示了 Lipschitz 正则化对潜在空间结构的塑造作用。未使用该正则化时，潜在轨迹呈现杂乱无章的分布，模型难以收敛到代表系统动力学的结构化表示。引入正则化后，潜在空间形成清晰的流形结构：绿色起点和红色终点有序排列，轨迹线平滑汇聚，且潜在散度（$\nabla z_t$）在稳态点附近呈现负值（Figure 1 右侧），表明学习到的动力学系统具有正确的吸引子结构。

### 失败模式与局限性

1. **训练成本**：多序列泛化训练约需 72 小时，且时间随序列长度线性增长，限制了在长序列或大规模数据集上的应用。
2. **超参数敏感**：nODE 层数和潜在维度对性能影响显著，需要仔细调参（3 层 ODE、512 维潜在向量为推荐配置）。
3. **动力学假设**：仅在遵循相同确定性动力学的序列上验证，未涉及随机性动力学或复杂非刚性变形场景（如流体、烟雾）。
4. **监督质量依赖**：Bifurcating Hill 等 2D 数据集依赖 CNOS 估计的伪真值位姿，监督质量受上游模型影响。
5. **真实场景未知**：尚未在真实世界大规模数据上评估，鲁棒性和可扩展性有待验证。

### 补充图表

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2603_12078/figures/013_Table_4.jpg]]
*Table 4: Ablation study on loss term in Oscillating Ball*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2603_12078/figures/015_Table_6.jpg]]
*Table 6: Ablation study of nODE layers on different evaluation metrics in Oscillating Ball dataset*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2603_12078/figures/017_Table_8.jpg]]
*Table 8: Training time per dataset*



## 定位与知识库关联

### 1. 方法谱系：从离散帧到连续动力学

Node-RF 的核心贡献在于将动态场景建模从“离散帧索引驱动”推进到“连续时间微分方程驱动”。传统动态 NeRF 方法——如 **D-NeRF** (Pumarola et al., CVPR 2021)、**HexPlane**、**TiNeuVox**——以及基于 3D 高斯泼溅的方法如 **4D-GS** 和 **Motion-GS**，均通过为每个训练时间步分配独立的潜在码或时间条件变形场来建模运动。这种设计的根本瓶颈是：模型仅在离散观测点上学习，缺乏对时间维度连续性的显式约束，导致长期外推能力不足，且无法泛化到训练中未见过的初始条件。

Node-RF 通过引入神经 ODE（Neural ODE）改变了这一范式。其关键设计是将场景动力学建模为潜在空间中的连续演化轨迹：

$$\frac{d h(t)}{d t} = f_{\theta}(h(t), t), \quad \text{with} \quad h(t_0) = h_0$$

ODE 求解器从初始潜在码 $z_{t_0}$ 出发，生成任意时刻的潜在表示 $z_t$：

$$z_{t_0}, \ldots, z_{t_N} = \mathrm{ODESolve}(f_{\theta}, z_{t_0}, (t_0, \ldots, t_N))$$

这使得模型能够从训练帧之间进行平滑插值，也能向未来进行长期外推——这两点都是离散索引方法无法原生支持的。在 Pendulum 数据集的外推评估中，Node-RF 的 PSNR（15.920）超越 **SimVP**（15.804），且是唯一同时支持插值和外推的 3D 方法（Table 2, TC 列）。

与同样采用神经 ODE 的 2D 视频方法 **Vid-ODE** 相比，Node-RF 的区别在于将 ODE 嵌入到 NeRF 体积渲染框架中，从而直接处理 3D 场景和多视角输入，而非仅限于 2D 像素空间预测。

### 2. 多序列泛化：从单场景拟合到动力学学习

现有动态 NeRF 方法的一个共同局限是：每个动态序列需要独立训练一个模型，模型学到的只是特定初始条件下的运动轨迹，而非底层的动力学规律。当面对新的初始条件（如小球从不同位置释放）时，这些方法需要重新训练。

Node-RF 的多序列泛化模式（Section 4.2）突破了这一边界。其核心设计包括：

1. **条件化初始状态**：编码器 $E$ 将物体的初始位姿 $p^c$ 映射为条件向量，注入到 ODE 的初始潜在状态中。
2. **共享动力学 ODE**：所有序列共享同一个神经 ODE $f_\theta$，学习的是跨序列通用的运动方程，而非单条轨迹。
3. **辅助监督信号**：在 NeRF 重建损失 $\mathcal{L}_{NeRF}$ 之外，增加位姿 L1 损失 $\mathcal{L}_{p}$ 和速度 L1 损失 $\mathcal{L}_{v}$，为潜在空间中的动力学学习提供直接约束。

$$\mathcal{L} = \lambda_1 \mathcal{L}_{NeRF} + \lambda_2 \mathcal{L}_{p} + \lambda_3 \mathcal{L}_{v} + \lambda_4 \mathcal{L}_{lipschitz}$$

在 Oscillating Ball 和 Bifurcating Hill 两个泛化数据集上，Node-RF 的 IoU 分别达到 0.3327 和 0.485，显著优于条件化版本的 **D-NeRF(c)**（0.2807）和 **Vid-ODE**（0.409）（Table 3）。消融实验（Table 4）进一步表明：仅使用 NeRF 重建损失已能使框架泛化到新初始条件，但添加位姿和速度辅助损失能显著提升指标。

### 3. 潜在空间正则化：Lipschitz 约束的关键作用

Node-RF 引入 Lipschitz 权重归一化来塑造潜在空间的结构：

$$W_i \gets \mathrm{normalization}(W_i, \mathrm{softplus}(c_i))$$

$$\mathcal{L}_{lipschitz} = \prod_i \mathrm{softplus}(c_i)$$

该正则化作用于 NeRF 渲染器的线性层，通过惩罚网络的 Lipschitz 上界，促使潜在表示在时间维度上平滑演化。Figure 8 的对比分析表明，未使用该正则化时，模型难以收敛到代表系统动力学的结构化潜在空间；加入后，潜在轨迹呈现出清晰的吸引子结构，与物理系统的稳态行为一致。

### 4. 适用边界与局限

**适用场景边界：**
- Node-RF 假设场景动力学是**确定性的**，即相同的初始条件产生相同的轨迹。随机性动力学（如布朗运动、湍流）不在当前框架的建模范围内。
- 验证数据集（Bouncing Balls、Pendulum、Oscillating Ball、Bifurcating Hill）均为**刚体运动或简单变形**场景，尚未在复杂非刚性变形（如人体动作、流体）上评估。
- 多序列泛化要求所有序列遵循**相同的底层运动方程**，仅初始条件不同。

**计算与调参成本：**
- 多序列泛化训练时间约 3 天（72 小时），且随输入序列长度线性增长（Table 8）。
- 模型对神经 ODE 的层数敏感：3 层 MLP 最优，5 层或 7 层均造成性能下降或学习失败（Table 6）。
- 潜在向量维度从 256 增至 512 带来性能提升，但继续增至 1024 会过拟合导致指标下降（Table 5）。

**监督信号依赖：**
- 在 Bifurcating Hill 等 2D 数据集上，位姿监督依赖 CNOS 估计的伪真值，监督质量受上游模型影响。
- 尚未在真实世界大规模数据上验证，鲁棒性和可扩展性未知。

### 5. 开放问题

1. **随机动力学扩展**：如何将框架从确定性 ODE 扩展到随机微分方程（SDE），以建模具有内在随机性的动态场景？
2. **复杂变形场景**：当前验证限于刚体和简单周期运动，框架在非刚性变形（如衣物、肌肉）上的有效性需进一步验证。
3. **真实世界部署**：在真实世界光照变化、遮挡、传感器噪声条件下的鲁棒性尚未评估。
4. **训练效率优化**：72 小时的训练时间限制了快速迭代，能否通过更高效的 ODE 求解器或混合表示（如结合 3D 高斯泼溅）加速？
5. **动力学解耦**：当前框架将静态背景和动态前景分离处理，但未显式建模多物体之间的相互作用动力学。



## 原文 PDF

![[paperPDFs/CVPR_2026/Node_RF_Learning_Generalized_Continuous_Space_Time_Scene_Dynamics_with_Neural_ODE_based_NeRFs.pdf]]
