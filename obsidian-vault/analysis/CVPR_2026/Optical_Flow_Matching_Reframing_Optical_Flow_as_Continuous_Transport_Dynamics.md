---
title: "Optical Flow Matching: Reframing Optical Flow as Continuous Transport Dynamics"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Optical_Flow_Matching_Reframing_Optical_Flow_as_Continuous_Transport_Dynamics.pdf
project_link: null
code_link: "https://github.com/LA30/OFM"
aliases:
- OFMO
- OFMROFACTD
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 采用时间依赖的速度场并利用ODE求解器将光流估计转化为连续的像素坐标传输过程，使位移由底层运动动态产生。
primary_logic: 借鉴Flow Matching的连续传输理论，将光流建模为条件最优传输路径上的坐标演化；通过三角形速度协同（TVS）策略，将理论上的目标速度分解为可学习的代理速度与校正项，解决了直接拟合Flow Matching目标导致的训练不稳定性，从而将离散估计提升为物理一致的运动推理。
claims:
- OFM通过速度场传输坐标，实现了光流的连续动态建模。
- TVS通过几何分解调和了Flow Matching理论目标与光流网络的训练目标。
- OFM在Sintel, KITTI和Spring上实现了最先进的精度和更强的跨数据集泛化。
- Sintel (train) Clean 上 EPE = 0.81
---

# Optical Flow Matching: Reframing Optical Flow as Continuous Transport Dynamics

> [!tip] 核心洞察
> 借鉴Flow Matching的连续传输理论，将光流建模为条件最优传输路径上的坐标演化；通过三角形速度协同（TVS）策略，将理论上的目标速度分解为可学习的代理速度与校正项，解决了直接拟合Flow Matching目标导致的训练不稳定性，从而将离散估计提升为物理一致的运动推理。

| 字段 | 内容 |
|------|------|
| 中文题名 | 光流匹配：将光流重新定义为连续传输动力学 |
| 英文题名 | Optical Flow Matching: Reframing Optical Flow as Continuous Transport Dynamics |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Luo_Optical_Flow_Matching_Reframing_Optical_Flow_as_Continuous_Transport_Dynamics_CVPR_2026_paper.html) · [Code](https://github.com/LA30/OFM) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Optical Flow Matching (OFM) |
| Dataset | Sintel (train) Clean, Sintel (train) Final, KITTI-15, Spring |

> [!tip] 效果简介
> - Sintel (train) Clean 上，EPE 0.81 vs - (-)。
> - Sintel (train) Final 上，EPE 2.16 vs - (-)。
> - KITTI-15 (train) 上，Fl-epe 3.32 vs - (-)。

## 概述

**问题瓶颈**：传统光流估计方法将运动建模为图像对之间的离散像素位移预测，忽略了真实世界中运动由底层速度场驱动的连续物理过程。这种离散对应范式导致光流估计在时序一致性、运动边界清晰度和跨数据集泛化能力方面存在固有局限。

**核心思想**：本文提出**光流匹配（Optical Flow Matching, OFM）**，将光流重新定义为连续的坐标传输过程。OFM学习一个时间依赖的速度场，并通过常微分方程（ODE）求解器将像素坐标从起始位置逐步演化至目标位置，从而将光流估计从离散位移预测提升为物理一致的运动推理。借鉴Flow Matching的连续传输理论，OFM将光流建模为条件最优传输路径上的坐标演化。

**关键技术**：针对直接拟合Flow Matching理论目标导致的训练不稳定性，论文设计了**三角形速度协同（Triangle Velocities Synergy, TVS）**策略。TVS通过几何分解将理论目标速度拆解为可学习的代理速度与校正项，在保留Flow Matching理论保证的同时，实现了与现有光流网络训练目标的协调统一。

**主要结果**：OFM在Sintel、KITTI和Spring等标准基准上取得了最先进的精度，展现出更强的时序稳定性和跨数据集泛化能力。消融实验验证了TVS对稳定训练的必要性，以及OFM框架对不同光流架构（如RAFT、GMFlow）的兼容性。

**方法定位**：OFM属于基于连续传输建模的光流估计方法，其核心贡献在于将Flow Matching理论引入光流领域，并通过TVS策略解决了理论与实践的衔接问题。与RAFT（Teed and Deng, ECCV 2020）、GMFlow（Xu et al., CVPR 2022）、FlowFormer++（Shi et al., CVPR 2023）等基线方法相比，OFM在输出表示（速度场替代离散位移）、训练目标（条件流匹配损失替代L1/L2损失）和推断过程（迭代ODE求解替代单步前向传播）三个维度上实现了范式转变。

## 背景与动机

光流估计是计算机视觉中的基础任务，旨在计算两帧图像之间像素级的稠密运动场。这一任务在视频理解、运动结构恢复、自动驾驶等应用中扮演着关键角色。然而，传统光流方法的核心范式存在一个根本性局限：它们将光流建模为**离散的像素对应关系**，即直接从图像对回归出一个位移场，而忽视了运动在物理世界中是由连续速度场驱动的动态演化过程。

这种离散对应范式带来了两个层面的问题。首先，从物理本质上看，像素的运动并非瞬间完成，而是遵循某种连续轨迹——这一轨迹由底层速度场在时间维度上积分得到。传统方法直接预测位移，相当于跳过了中间的动力学过程，导致预测结果缺乏时序上的一致性。其次，从学习范式上看，现有主流方法——无论是基于迭代相关性的 **RAFT**（Teed and Deng, ECCV 2020）、基于全局匹配的 **GMFlow**（Xu et al., CVPR 2022），还是基于 Transformer 的 **FlowFormer++**（Shi et al., CVPR 2023）和高效变体 **SEA-RAFT**（Wang et al., ECCV 2024）——均采用 L1/L2 损失直接监督光流位移场，训练目标与运动的连续本质之间存在结构性错配。

近年来，生成建模领域中的 **Flow Matching** 框架为连续传输问题提供了新的理论工具。Flow Matching 通过学习时间依赖的速度场，利用常微分方程（ODE）将样本从源分布连续传输到目标分布，在图像生成等任务中展现出强大的建模能力。这一框架的核心思想——用速度场驱动坐标的连续演化——与光流的物理本质高度契合，但如何将其从生成建模迁移到光流估计这一条件预测任务中，并解决由此带来的训练稳定性问题，是一个尚未被充分探索的方向。

本文的核心动机正是弥合这一鸿沟：**将光流重新定义为连续传输动力学问题**，借助 Flow Matching 的理论框架，使光流估计从离散位移预测升维为物理一致的运动推理。

## 核心创新

OFM 的核心创新在于将光流估计从传统的**离散位移回归**重新定义为**连续坐标传输动力学**，并围绕这一范式转移构建了三个紧密耦合的 changed slots，解决了离散对应范式的根本性瓶颈。

### 范式转移：从位移预测到速度场驱动的坐标传输

传统光流方法（如 **RAFT**，Teed and Deng, ECCV 2020；**GMFlow**，Xu et al., CVPR 2022）将问题建模为像素对之间的离散对应，直接输出位移场。OFM 的核心洞察在于：物理世界中，像素运动由底层速度场在时间上的积分产生，而非孤立的位移跳跃。因此，OFM 学习一个**时间依赖的速度场** $\mathcal{V}_{\theta}^{\mathrm{OF}}(\boldsymbol{x}_t, t \mid \mathrm{I}_1, \mathrm{I}_2)$，并通过 ODE 求解器将像素坐标从初始位置 $\boldsymbol{x}_0$ 连续传输至目标位置 $\boldsymbol{x}_1$，最终光流由 $\boldsymbol{x}_1 - \boldsymbol{x}_i$ 自然导出（图 1）。这一范式转移直接针对真实瓶颈：传统方法无法捕捉运动在物理上由速度场驱动的连续演化过程，导致时序一致性不足。

### 关键 Changed Slots

**1. 输出表示：从位移场到时间依赖速度场。** 基线方法输出一个静态的二维位移向量场；OFM 输出一个以坐标 $\boldsymbol{x}_t$ 和时间 $t$ 为输入、以图像对为条件的速度向量。位移不再是直接预测的目标，而是通过积分常微分方程 $\frac{d\boldsymbol{x}_t}{dt} = \boldsymbol{v}(\boldsymbol{x}_t, t)$ 产生的涌现结果。这使得模型能够建模运动过程中的中间状态，为时序一致性提供了内在的物理约束。

**2. 训练目标：从 L1/L2 直接监督到条件流匹配损失。** 基线方法使用端点误差的直接回归损失；OFM 采用条件流匹配（Conditional Flow Matching, CFM）损失，监督速度场在概率路径上的预测：

$$\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t, \boldsymbol{x}_1, \boldsymbol{x}_0} \| \mathcal{V}_{\theta}^{\mathrm{OF}}(\boldsymbol{x}_t, t \mid \mathrm{I}_1, \mathrm{I}_2) - \boldsymbol{v}_t(\boldsymbol{x}_t \mid \boldsymbol{x}_1) \|^2$$

该损失理论上等价于边际流匹配损失，但避免了边际速度的难以计算的问题。路径采用线性条件最优传输形式 $\boldsymbol{x}_t = t\boldsymbol{x}_1 + (1-t)\boldsymbol{x}_0$，为训练提供了简洁的条件速度目标。

**3. 推断过程：从单步前向传播到迭代 ODE 求解。** 基线方法通过单次网络前向传播直接输出光流；OFM 在推断时采用欧拉方法对速度场进行多步积分，逐步演化坐标。函数评估次数（NFE）成为控制精度与效率的关键参数——消融实验表明，适度增加 NFE 可逐步降低误差（Table 3），验证了 ODE 求解精度对最终光流的积极影响。

### 核心因果机制：三角形速度协同（TVS）

直接使用 Flow Matching 的理论目标训练速度场（OFM-Naive）会导致训练崩溃或性能极差（Table 3）。这一失败源于理论目标速度 $\boldsymbol{v}_t(\boldsymbol{x}_t \mid \boldsymbol{x}_1)$ 与光流网络实际预测能力之间的不匹配。**三角形速度协同（Triangle Velocities Synergy, TVS）** 是 OFM 的决定性因果调节器，通过几何分解调和了这一矛盾。

TVS 引入两条辅助概率路径 $\boldsymbol{y}_t$ 和 $\boldsymbol{z}_t$，将目标速度分解为代理速度与校正项：

$$\boldsymbol{v}_t(\boldsymbol{x}_t \mid \boldsymbol{x}_1) = \boldsymbol{v}_t(\boldsymbol{y}_t \mid \boldsymbol{x}_1) - \boldsymbol{v}_t(\boldsymbol{z}_t \mid \boldsymbol{x}_0)$$

其中 $\boldsymbol{y}_t = t\boldsymbol{x}_1 + (1-t)\boldsymbol{x}_i$，$\boldsymbol{z}_t = t\boldsymbol{x}_0 + (1-t)\boldsymbol{x}_i$，$\boldsymbol{x}_i$ 为初始坐标，$\boldsymbol{x}_l$ 由全局流预测分支提供作为可学习的参考点。这一分解使网络只需预测两个更易学习的速度项，同时保持了 Flow Matching 的理论保证。消融实验强有力地验证了 TVS 的必要性：OFM-Naive 训练崩溃，而加入 TVS 后性能大幅提升（Table 3）。

## 整体框架

Optical Flow Matching (OFM) 将传统的光流估计从离散位移回归重新定义为**连续传输动力学问题**。其核心 pipeline 由三个关键模块串联构成：特征提取与条件化、时间依赖速度场预测、以及基于 ODE 的坐标演化。

### 输入与特征准备

给定一对输入图像 $\mathrm{I}_1$ 和 $\mathrm{I}_2$，系统首先通过 **Twins-SVT 特征编码器** 提取两组互补的视觉表征（Figure 2）：
- **上下文特征** $\mathbf{f}_c$：提供场景的语义与结构先验；
- **相关体积** $\mathbf{f}_{cv}$：通过计算两帧特征图之间的视觉相似性，编码像素级的匹配信息。

![[assets/figures/papers/paper_list_l2071_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Optical_Flow_Match/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Optical Flow Matching (OFM). Given an image pair, the network extracts context features and a correlation volume to parameterize a time-dependent velocity field. Starting from perturbed pixel coordinates*

这两组特征共同构成速度场网络的条件信号，使后续的传输过程能够感知图像内容与帧间对应关系。

### 条件速度场网络

OFM 的核心是一个**时间依赖的速度场网络** $\mathbf{V}_\theta^{\text{OF}}$。该网络接收三个输入：
1. 当前像素坐标 $\mathbf{x}_t$；
2. 时间参数 $t \in [0, 1]$；
3. 图像条件 $(\mathbf{f}_{cv}, \mathbf{f}_c)$。

网络输出一个速度向量 $\hat{\mathbf{v}}_t$，表示坐标 $\mathbf{x}_t$ 在时刻 $t$ 的瞬时运动方向与速率。这一设计使速度场成为时间与空间的连续函数，而非仅预测终点位移。

### 坐标传输与光流生成

在推理阶段，OFM 采用**欧拉 ODE 求解器**对速度场进行迭代积分。从初始坐标 $\mathbf{x}_0$（在像素初始位置 $\mathbf{x}_i$ 附近施加扰动得到）出发，沿时间轴逐步演化：

$$\frac{d\mathbf{x}_t}{dt} = \mathbf{v}(\mathbf{x}_t, t)$$

经过 $N$ 次函数评估（NFE），坐标被传输至终点 $\mathbf{x}_1$。最终光流通过简单的坐标差计算得到：

$$\mathbf{f}_{\text{pred}} = \mathbf{x}_1 - \mathbf{x}_i$$

### 训练中的关键策略：TVS

直接以 Flow Matching 理论目标训练速度场网络会导致训练不稳定（OFM-Naive 方案）。为解决这一问题，OFM 引入 **Triangle Velocities Synergy (TVS)** 策略（Figure 3）：将理论上的目标速度 $\mathbf{v}_t(\mathbf{x}_t \mid \mathbf{x}_1)$ 几何分解为可学习的代理速度与校正项之和：

$$\mathbf{v}_t(\mathbf{x}_t \mid \mathbf{x}_1) = \mathbf{v}_t(\mathbf{y}_t \mid \mathbf{x}_1) - \mathbf{v}_t(\mathbf{z}_t \mid \mathbf{x}_0)$$

其中 $\mathbf{y}_t$ 和 $\mathbf{z}_t$ 是 TVS 引入的两条辅助概率路径（Eq. 8）。网络实际预测的是代理速度，训练时通过条件流匹配损失（Eq. 6）进行监督，推理时再通过上述三角关系还原为物理一致的目标速度进行 ODE 积分。

此外，系统还包含一个**全局流预测分支**，提供粗粒度的全局位移作为可学习的参考点 $\mathbf{x}_l$，辅助坐标初始化和传输过程。

### 端到端数据流

整体数据流可总结为：**图像对 → 特征提取 → 速度场参数化 → ODE 坐标传输 → 位移输出**。这一设计将光流估计从单步前向传播转变为多步物理推理过程，使位移由底层运动动态自然产生，而非直接回归。

### 补充图表

![[assets/figures/papers/paper_list_l2071_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Optical_Flow_Match/figures/001_Figure_1.jpg]]
*Figure 1: Idea Illustration. Optical Flow Matching (OFM) reframes optical flow as a continuous transport process, where a learned velocity field*

## 核心模块与公式推导

### 问题重定义：从离散位移到连续传输

传统光流估计将任务建模为预测像素坐标的离散位移场 $\mathbf{f} = \mathbf{x}_1 - \mathbf{x}_0$，其中 $\mathbf{x}_0$ 和 $\mathbf{x}_1$ 分别表示源图像与目标图像中对应点的坐标。这种范式忽略了运动在物理上由速度场驱动的连续演化过程，导致时序一致性不足。

OFM 将光流量构为一个**连续传输过程**：学习一个时间依赖的速度场 $\mathbf{v}_\theta(\mathbf{x}_t, t \mid \mathbf{I}_1, \mathbf{I}_2)$，通过 ODE 求解器将像素坐标从起始位置 $\mathbf{x}_0$ 沿概率路径逐步传输至终点 $\mathbf{x}_1$，最终光流由 $\mathbf{f}_{\text{pred}} = \mathbf{x}_{\text{pred}} - \mathbf{x}_i$ 计算得到（$\mathbf{x}_i$ 为初始像素坐标）。

### 核心模块

OFM 框架由以下关键模块构成（参见 Figure 2）：

1. **Twins-SVT 特征编码器**：从输入图像对 $(\mathbf{I}_1, \mathbf{I}_2)$ 中提取上下文特征 $\mathbf{f}_c$ 并构建 4D 相关体积 $\mathbf{f}_{cv}$，为速度场网络提供图像条件信息。

2. **条件速度场网络 $\mathbf{V}_\theta^{\text{OF}}$**：以相关体积 $\mathbf{f}_{cv}$、上下文特征 $\mathbf{f}_c$、当前坐标 $\mathbf{x}_t$ 和时间步 $t$ 为输入，预测速度向量 $\hat{\mathbf{v}}_t = \mathbf{v}_\theta(\mathbf{x}_t, t \mid \mathbf{f}_{cv}, \mathbf{f}_c)$。

3. **全局流预测分支**：提供粗全局流作为可学习的参考点 $\mathbf{x}_l$，用于构造 TVS 策略中的辅助路径。

4. **Euler ODE 求解器**：在推理阶段，从扰动后的起始坐标 $\mathbf{x}_0$ 出发，通过迭代积分速度场得到最终像素坐标 $\mathbf{x}_{\text{pred}}$。函数评估次数（NFE）控制积分精度。

### 关键公式推导

#### 3.1 Flow Matching 理论基础

Flow Matching 的目标是学习一个边际速度场 $\mathbf{v}_\theta(\mathbf{x}_t, t)$，使其逼近真实的速度场 $\mathbf{v}(\mathbf{x}_t, t)$。原始 Flow Matching 损失定义为：

$$\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{t, p_t(\boldsymbol{x}_t)} \| \boldsymbol{v}_{\boldsymbol{\theta}}(\boldsymbol{x}_t, t) - \boldsymbol{v}(\boldsymbol{x}_t, t) \|^2 \tag{3}$$

其中边际速度场 $\mathbf{v}(\mathbf{x}_t, t)$ 定义为条件速度场的期望：

$$\mathbf{v}(\mathbf{x}_t, t) \triangleq \mathbb{E}_{p_t(\mathbf{v}_t \mid \mathbf{x}_t)} [\mathbf{v}_t]$$

由于直接计算该期望不可行，Conditional Flow Matching (CFM) 提供了一个等价但可计算的替代目标。

#### 3.2 条件流匹配损失

OFM 将光流估计的条件概率路径定义为 $\mathbf{x}_t = a_t \mathbf{x}_1 + b_t \mathbf{x}_0$，采用线性条件最优传输路径：

$$\boldsymbol{x}_t = t \boldsymbol{x}_1 + (1 - t) \boldsymbol{x}_0 \tag{7}$$

对应的条件流匹配损失为：

$$\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t, \boldsymbol{x}_1, \boldsymbol{x}_0} \| \boldsymbol{\mathcal{V}}_{\theta}^{\mathrm{OF}}(\boldsymbol{x}_t, t \mid \mathrm{I}_1, \mathrm{I}_2) - \boldsymbol{v}_t(\boldsymbol{x}_t \mid \boldsymbol{x}_1) \|^2 \tag{6}$$

其中 $\mathbf{v}_t(\mathbf{x}_t \mid \mathbf{x}_1) = \mathbf{x}_1 - \mathbf{x}_0$ 是线性路径上的条件目标速度。理论上，$\mathcal{L}_{\mathrm{CFM}}$ 与 $\mathcal{L}_{\mathrm{FM}}$ 的梯度等价，因此最小化 CFM 损失等价于学习边际速度场。

#### 3.3 ODE 生成方程

学习到的速度场通过以下常微分方程驱动坐标演化：

$$\frac{d \boldsymbol{x}_t}{d t} = \boldsymbol{v}(\boldsymbol{x}_t, t) \tag{4}$$

从 $t=0$ 到 $t=1$ 积分该 ODE 即可将起始坐标 $\mathbf{x}_0$ 传输至终点 $\mathbf{x}_1$。

#### 3.4 三角形速度协同（TVS）

直接拟合 CFM 目标中的 $\mathbf{v}_t(\mathbf{x}_t \mid \mathbf{x}_1) = \mathbf{x}_1 - \mathbf{x}_0$ 会导致训练不稳定（OFM-Naive 在实验中表现崩溃或性能极差，见 Table 3）。TVS 通过几何分解解决此问题。

TVS 引入两条辅助概率路径：

$$\boldsymbol{y}_t = t \boldsymbol{x}_1 + (1 - t) \boldsymbol{x}_i, \quad \boldsymbol{z}_t = t \boldsymbol{x}_0 + (1 - t) \boldsymbol{x}_i \tag{8}$$

其中 $\mathbf{x}_i$ 为初始像素坐标，$\mathbf{x}_l$ 为全局流预测分支提供的可学习参考点。基于向量三角形关系，目标速度可分解为：

$$v_{t}(\boldsymbol{x}_{t} \mid \boldsymbol{x}_{1}) = v_{t}(\boldsymbol{y}_{t} \mid \boldsymbol{x}_{1}) - v_{t}(\boldsymbol{z}_{t} \mid \boldsymbol{x}_{0})$$

该分解将理论目标速度转化为**可学习的代理速度**与**校正项**的组合（Figure 3）。训练时直接监督预测速度 $\hat{\mathbf{v}}_t$，推理时通过 TVS 关系转换为积分所需的速度 $\mathbf{v}_t$。这一策略调和了 Flow Matching 的理论保证与光流网络的训练目标，使模型能够直接使用标准光流真值 $\mathbf{f}_{gt}$ 进行监督。

![[assets/figures/papers/paper_list_l2071_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Optical_Flow_Match/figures/003_Figure_3.jpg]]
*Figure 3: Difference between OFM-Naive (a) and OFM-TVS (b). OFM-TVS replaces the single perturbed velocity in OFM-Naive with a geometrically consistent triangular decomposition*

### 训练与推理流程

**训练阶段**（Algorithm 1 核心步骤）：
1. 从图像对中采样像素坐标 $\mathbf{x}_i$，根据真值光流计算 $\mathbf{x}_1 = \mathbf{x}_i + \mathbf{f}_{gt}$
2. 随机采样时间 $t \sim \mathcal{U}(0,1)$，生成扰动起始点 $\mathbf{x}_0$ 和路径点 $\mathbf{x}_t$
3. 通过 TVS 关系计算目标速度，监督速度场网络输出

**推理阶段**：
1. 以扰动坐标 $\mathbf{x}_0$ 为起点
2. 使用 Euler 方法迭代求解 ODE，将坐标沿速度场传输至 $t=1$
3. 最终光流 $\mathbf{f}_{\text{pred}} = \mathbf{x}_{\text{pred}} - \mathbf{x}_i$

> 注：公式编号沿用原文标记，具体推导细节建议核对原文 Section 3.2 及 Algorithm 1。

## 实验与分析

### 核心实验设置

OFM 采用 **Twins-SVT** 作为特征编码器，在标准光流数据集上进行训练与评估。模型以图像对 $(I_1, I_2)$ 为输入，通过条件速度场网络 $\mathcal{V}_{\theta}^{\mathrm{OF}}$ 预测时间依赖的速度向量，并利用 **Euler ODE 求解器** 沿时间轴积分得到最终像素坐标，光流由 $f_{\mathrm{pred}} = x_{\mathrm{pred}} - \mathrm{coord}_0$ 计算得出。训练使用条件流匹配损失 $\mathcal{L}_{\mathrm{CFM}}$（Eq. 6），该损失在理论上等价于边际流匹配损失 $\mathcal{L}_{\mathrm{FM}}$（Eq. 3），但仅需光流真值即可监督，无需直接估计难以获取的边际速度场。

### 标准基准主结果

**Table 1** 展示了 OFM 在 Sintel 和 KITTI-15 基准上的定量表现。在 Sintel Clean 训练集上，OFM 取得 **0.81 EPE**，Final 训练集为 **2.16 EPE**；在线评测中，Clean 和 Final 的 EPE 分别为 **0.94** 和 **1.85**。在 KITTI-15 训练集上，OFM 的 Fl-epe 为 **3.32**，Fl-all 为 **10.9%**。论文报告 OFM 在标准基准上的平均排名达到 **1.1**，表明其整体性能处于领先水平。

**Table 2** 报告了 Spring 测试集的零样本评估结果。OFM 取得 **3.660** 的 1px 指标和 **0.468 EPE**，在仅使用双帧输入的条件下超越了多数现有方法（包括部分多帧方法，表中以灰色标记）。这一结果直接支撑了论文的核心主张：OFM 具备 **更强的跨数据集泛化能力**。

定性结果方面，**Figure 4** 展示了 Sintel 数据集上的可视化对比。OFM 在运动边界处产生更清晰的分割，在挑战性区域（虚线框标注）表现出更连贯的运动估计，相较于 DPFlow 和 SEA-RAFT (L) 在结构保真度和细节精度上均有提升。**Figure 5** 的 Spring 测试集误差可视化进一步印证了这一优势——OFM 的误差图中红色高误差区域显著更少。

![[assets/figures/papers/paper_list_l2071_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Optical_Flow_Match/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative Comparison on Sintel. OFM produces sharper boundaries and more coherent motion in challenging regions (dashed boxes), outperforming DPFlow [36] and SEA-RAFT (L) [54] in both structural fidelity and fine-grained detail*

![[assets/figures/papers/paper_list_l2071_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Optical_Flow_Match/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative Comparisons on the Spring Test Set. Top: predicted flow fields. Bottom: error visualizations. On the right, the colorbar for error visualization is shown, where red represents larger errors and blue indicates smaller errors (see the official website for more details). OFM delivers sharper motion boundaries and lower errors compared to DPFlow [36] and MemFlow [1]*

### 消融研究

**Table 3** 系统验证了 OFM 各组件的贡献：

1. **TVS 策略的必要性**：直接使用 Flow Matching 理论目标训练（OFM-Naive，无 TVS）会导致训练崩溃或性能极差；引入 TVS 后性能大幅提升。这直接验证了 **因果调节变量**——TVS 通过几何分解调和了 Flow Matching 理论目标与光流网络训练目标之间的冲突，是稳定训练的关键。

2. **额外训练数据的影响**：加入 TartanAir 数据集后，Fl-epe 降低约 **0.21**，Fl-all 降低约 **0.8%**，表明 OFM 能够有效利用额外数据提升性能。

3. **ODE 求解步数（NFE）**：适度增加函数评估次数可逐步降低误差，表明 **ODE 求解精度对最终光流质量有正向影响**。论文将默认 NFE 设为合理值以平衡精度与效率。

4. **架构兼容性**：OFM 可无缝集成到不同光流架构（如 RAFT、GMFlow）中，且均能获得一致提升，表明其作为通用框架的潜力。

### 效率分析

**Table 4** 对比了 OFM 与基线方法的参数量和推理时间（处理 KITTI 图像，尺寸 376×1248）。OFM 在实现领先精度的同时，保持了可竞争的推理效率。论文指出当前实现基于经典的 Euler ODE 求解器，未来可通过融合更高效的 Flow Matching 变体（如 MeanFlow、Shortcut Models）进一步减少推理步骤。

### 失败模式与局限

论文明确指出的局限包括：

- **ODE 求解器的选择**：当前采用的条件最优传输路径和 Euler 求解器仅代表经典方案，并非最优。更先进的 Flow Matching 变体有望进一步提升效率。
- **高分辨率场景**：在实时或高分辨率应用中，ODE 迭代求解的计算开销仍是待优化的问题。

需要注意的是，论文未提供 OFM 在极端运动遮挡、大位移或光照剧变等特定失败场景下的系统分析，这些场景下的鲁棒性需要手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l2071_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Optical_Flow_Match/figures/005_Table_1.jpg]]
*Table 1: Quantitative Results on Standard Benchmarks. We compare OFM against leading two-frame methods using official metrics, and average ranks are reported for overall comparison. Best and second-best results are shown in bold and underline, respectively*

![[assets/figures/papers/paper_list_l2071_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Optical_Flow_Match/figures/007_Table_2.jpg]]
*Table 2: Quantitative Results on Spring Benchmarks. We compare OFM with state-of-the-art methods under zero-shot evaluation. Best and second-best results are shown in bold and underline, respectively. Multi-frame methods are marked in gray for reference*

![[assets/figures/papers/paper_list_l2071_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Optical_Flow_Match/figures/008_Table_3.jpg]]
*Table 3: Ablation Study. The default settings are marked in bold. 1-NFE means a single function evaluation, i.e., one-step sampling*

![[assets/figures/papers/paper_list_l2071_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Optical_Flow_Match/figures/009_Table_4.jpg]]
*Table 4: Parameter and Runtime Comparison. The reported time is for processing KITTI images with size of 376 × 1248*

## 方法谱系与知识库定位

### 1. 范式迁移：从离散位移回归到连续传输动力学

传统光流估计方法，无论是基于迭代相关性的 **RAFT** (Teed and Deng, ECCV 2020)、基于全局匹配的 **GMFlow** (Xu et al., CVPR 2022)，还是基于Transformer的 **FlowFormer++** (Shi et al., CVPR 2023) 和高效变体 **SEA-RAFT** (Wang et al., ECCV 2024)，其核心范式均为**离散对应范式**：网络直接预测像素从帧1到帧2的位移向量场。这种范式在物理本质上存在一个被长期忽视的缺陷——它跳过了运动发生的中间过程，无法捕捉运动由速度场驱动的连续演化特性，导致时序一致性和跨域泛化能力受限。

OFM的根本性创新在于将光流估计重新定义为**连续传输动力学问题**。具体而言，OFM学习一个时间依赖的速度场 $\mathcal{V}_{\theta}^{\mathrm{OF}}$，通过ODE求解器将像素坐标从初始位置 $\mathbf{x}_0$ 沿时间轴连续传输到目标位置 $\mathbf{x}_1$，光流则由 $\mathbf{x}_1 - \mathbf{x}_i$ 自然导出。这一范式迁移的因果机制是：**将光流的生成从“直接预测结果”转变为“模拟物理过程”**，使得位移成为底层运动动态的涌现属性，而非网络的直接输出。

### 2. 与Flow Matching生成范式的继承与适配

OFM的理论基础直接继承自Flow Matching生成模型框架。其核心损失函数——条件流匹配损失（CFM）——在理论上等价于边际流匹配损失（FM）：

$$\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t, \mathbf{x}_1, \mathbf{x}_0} \| \mathcal{V}_{\theta}^{\mathrm{OF}}(\mathbf{x}_t, t \mid \mathrm{I}_1, \mathrm{I}_2) - \mathbf{v}_t(\mathbf{x}_t \mid \mathbf{x}_1) \|^2$$

然而，直接将Flow Matching应用于光流估计面临一个关键障碍：**理论目标速度 $\mathbf{v}_t(\mathbf{x}_t \mid \mathbf{x}_1)$ 与光流网络可学习的监督信号之间存在根本性张力**。Flow Matching要求学习从扰动坐标 $\mathbf{x}_0$ 到目标坐标 $\mathbf{x}_1$ 的条件速度，但光流任务中我们仅有图像对和真实光流 $\mathbf{f}_{gt}$，缺乏对中间传输过程的直接监督。

### 3. TVS策略：调和理论目标与训练可行性的关键机制

Triangle Velocities Synergy (TVS) 是OFM从理论走向实践的决定性创新。其核心思想是通过**几何分解**绕开直接估计Flow Matching目标速度的困难：

$$\mathbf{v}_{t}(\mathbf{x}_{t} \mid \mathbf{x}_{1}) = \mathbf{v}_{t}(\mathbf{y}_{t} \mid \mathbf{x}_{1}) - \mathbf{v}_{t}(\mathbf{z}_{t} \mid \mathbf{x}_{0})$$

其中 $\mathbf{y}_t = t\mathbf{x}_1 + (1-t)\mathbf{x}_i$ 和 $\mathbf{z}_t = t\mathbf{x}_0 + (1-t)\mathbf{x}_i$ 是两条辅助概率路径，$\mathbf{x}_i$ 为可学习的参考点（由全局流预测分支提供）。这一分解将目标速度拆解为**代理速度**与**校正项**之差，使得网络可以仅使用标准光流真值 $\mathbf{f}_{gt}$ 进行监督，同时保持Flow Matching的理论保证。

消融实验（Table 3）提供了强有力的因果证据：OFM-Naive（无TVS的直接Flow Matching）导致训练崩溃或性能极差，而加入TVS后性能大幅提升，验证了TVS对稳定训练的**必要性**。

### 4. 在光流方法谱系中的定位

从方法谱系角度看，OFM占据了一个独特的位置：

- **相对于RAFT系列**：RAFT依赖迭代相关查找和GRU更新，本质仍是离散优化；OFM用连续ODE求解替代了这一迭代过程，使运动推理具有物理一致性。
- **相对于GMFlow/FlowFormer**：这些方法通过Transformer进行全局特征匹配，但输出仍是单步位移；OFM保留了相关体积作为条件输入，但将输出空间从位移场转换为速度场。
- **相对于多帧方法**：OFM作为两帧方法，在Spring基准上（Table 2）的零样本评估中展现出与多帧方法可比的性能，表明连续传输建模本身就能捕获时序结构，无需显式多帧输入。

值得注意的是，OFM展现出**架构无关性**：Table 3的兼容性实验表明，TVS策略可以无缝集成到RAFT、GMFlow等不同架构中，且均能获得一致提升。这表明TVS作为一种训练策略具有独立于骨干网络的价值。

### 5. 适用边界与局限性

OFM-TVS框架存在以下适用边界：

1. **求解器依赖**：当前实现基于经典的欧拉ODE求解器和线性条件最优传输路径，这仅代表Flow Matching家族中最基础的配置。论文明确指出，更高效的变体（如MeanFlow、Shortcut Models）尚未被探索，这些方法有望减少推理所需的函数评估次数（NFE），从而提升效率。

2. **计算开销**：Table 4的参数与运行时间对比显示，OFM的ODE求解步骤引入了额外的计算成本。虽然适度增加NFE可逐步降低误差（Table 3消融实验证实），但在高分辨率或实时应用中，NFE与精度的权衡仍需进一步优化。

3. **理论完备性**：TVS策略虽然通过几何分解实现了训练稳定性，但其对Flow Matching理论最优性的保持程度尚未得到严格证明。论文将其定位为“经典解决方案而非最优方案”，暗示存在进一步提升的空间。

### 6. 开放问题

基于上述分析，以下开放问题值得关注：

- **更先进Flow Matching变体的融合**：MeanFlow和Shortcut Models等方法的核心理念（如均值路径规划、跳跃式采样）如何适配到OFM框架中，以同时提升训练效率和推理速度？
- **求解器-网络协同设计**：当前欧拉求解器与速度场网络是分离设计的，是否存在端到端优化的求解器结构，能够根据图像内容自适应调整积分步长？
- **多帧扩展的自然路径**：OFM的连续传输框架天然支持多帧输入（将时间轴从两帧扩展到多帧），这一方向尚未被探索，可能进一步弥合两帧方法与多帧方法之间的性能差距。
- **物理先验的进一步注入**：TVS的三角分解本质上是一种几何先验，是否存在其他形式的物理先验（如流体力学约束）可以进一步增强速度场学习的合理性？

## 原文 PDF

![[paperPDFs/CVPR_2026/Optical_Flow_Matching_Reframing_Optical_Flow_as_Continuous_Transport_Dynamics.pdf]]
