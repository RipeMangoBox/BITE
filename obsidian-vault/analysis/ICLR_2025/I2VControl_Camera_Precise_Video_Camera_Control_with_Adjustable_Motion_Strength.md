---
title: "I2VControl-Camera: Precise Video Camera Control with Adjustable Motion Strength"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/I2VControl_Camera_Precise_Video_Camera_Control_with_Adjustable_Motion_Strength.pdf
aliases:
- IC
- I2VControl-Camera
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "将控制信号从稀疏的相机外参矩阵转换为相机坐标系下的稠密 2D 点轨迹 (T_λ)，并显式建模高阶非线性分量，通过可调节的整体运动强度 m_λ 来控制主体动态幅度。"
primary_logic: "将视频内容的 3D 点轨迹分解为线性项（对应刚性相机运动）和高阶非线性项（对应主体自身动态），分别作为相机控制与运动强度控制的信号，从而解耦并独立操控相机运动和对象运动。"
claims:
- "在 RealEstate10K 数据集上，提出的方法在 RotErr、TransErr、FID 和 MSC 四项指标上均显著优于 MotionCtrl 和 CameraCtrl。"
- "在包含可动对象的场景中，Ours-0 的 RotErr 为 0.76，TransErr 为 6.97，达到最佳控制精度；Ours-600 的 FID 为 91.86，MSC 为 47.70，同时保持最高图像质量和自然动态。"
- "通过调节运动强度 m_λ，可在相同相机轨迹下生成从完全静态到显著运动的视频，验证了运动强度可控性。"
- "RealEstate10K 上 RotErr, TransErr, FID, MSC = Ours-0: FID=155.01, MSC=12.93 （所有指标均为最佳）"
---

# I2VControl-Camera: Precise Video Camera Control with Adjustable Motion Strength

> [!tip] 核心洞察
> 将视频内容的 3D 点轨迹分解为线性项（对应刚性相机运动）和高阶非线性项（对应主体自身动态），分别作为相机控制与运动强度控制的信号，从而解耦并独立操控相机运动和对象运动。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | I2VControl-Camera：具有可调运动强度的精确视频相机控制 |
| 英文题名 | I2VControl-Camera: Precise Video Camera Control with Adjustable Motion Strength |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://arxiv.org/abs/2411.06525); [Project](https://wanquanf.github.io/I2VControlCamera) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | I2VControl-Camera |
| Dataset | RealEstate10K, Movable Object Dataset |

> [!tip] 效果简介
> - RealEstate10K 上，RotErr, TransErr, FID, MSC 为 Ours-0: FID=155.01, MSC=12.93 （所有指标均为最佳），对比 MotionCtrl, CameraCtrl 的相应指标均显著更差，变化 显著优于所有基线。
> - Movable Object Dataset 上，RotErr, TransErr 为 Ours-0: RotErr=0.76, TransErr=6.97，对比 MotionCtrl, CameraCtrl 的误差更高，变化 控制误差最小。
> - Movable Object Dataset 上，FID 为 Ours-600: FID=91.86，对比 MotionCtrl, CameraCtrl 的 FID 值更大，变化 最佳图像质量。

## 概述

视频生成中的相机控制面临一个根本性瓶颈：现有方法（如 **MotionCtrl** (Wang et al., 2023)、**CameraCtrl** (He et al., 2024)）仅依赖稀疏的相机外参矩阵或 Plücker 射线嵌入作为控制信号，导致控制精度不足、泛化能力受限，难以精确反映用户意图。更关键的是，这些方法完全忽视了场景中独立于相机运动的主体动态——当画面中存在可动对象时，生成结果往往僵硬、缺乏自然运动。

本文提出的 **I2VControl-Camera** 针对上述问题，将控制信号从稀疏的外参矩阵重构为相机坐标系下的**稠密 2D 点轨迹**，并首次显式建模了视频轨迹展开中的高阶非线性分量。核心思想是将 3D 点轨迹分解为线性项（对应刚性相机运动）与高阶非线性项（对应主体自身动态），从而将相机控制与对象运动解耦为两个独立可调的控制维度。

具体而言，方法引入了两个关键控制量：**点轨迹 $T_\lambda$** 由线性运动投影得到，提供像素级的相机控制精度；**运动强度 $m_\lambda$** 通过对非线性项速度的域积分获得，作为可调节的标量控制主体动态幅度。这一解耦设计使模型能在保持相机轨迹不变的前提下，生成从完全静止到显著运动的连续可调视频。

在 RealEstate10K 数据集上，I2VControl-Camera 在旋转误差（RotErr）、平移误差（TransErr）、FID 和运动评分（MSC）四项指标上均显著优于 MotionCtrl 与 CameraCtrl（Table 1）。在包含可动对象的场景中，方法在 $m_\lambda=0$ 时达到最佳控制精度（RotErr=0.76, TransErr=6.97），在 $m_\lambda=600$ 时取得最优图像质量（FID=91.86）和最丰富的自然动态（MSC=47.70），验证了控制精度与运动强度独立可调的有效性（Table 2, Figure 6）。

该方法采用与基础模型结构无关的适配器架构，可灵活集成至现有图像到视频扩散模型，为精确且灵活的视频相机控制提供了新的技术路径。

## 背景与动机

图像到视频（I2V）生成任务的核心挑战之一，在于对生成内容的精确运动控制。相机运动控制作为其中关键的子任务，要求模型在保持场景内容一致性的前提下，严格遵循用户指定的相机轨迹生成视频。这一能力对于电影级运镜、虚拟场景漫游等应用至关重要。

现有方法主要通过向扩散模型中注入相机外参矩阵来实现控制。**MotionCtrl**（Wang et al., 2023）将外参矩阵直接注入时序注意力层，而 **CameraCtrl**（He et al., 2024）则采用 Plücker 射线嵌入来增强控制的表达能力。此外，**AnimateDiff**（Guo et al., 2024b）通过 LoRA 适配器学习固定的相机运动模式。然而，这些方法面临两个根本性的瓶颈：

**瓶颈一：控制信号稀疏，泛化性不足。** 外参矩阵 $(\mathbf{R}, \mathbf{t})$ 仅描述了相机的全局刚体运动，是一种高度稀疏的表示。它缺乏与场景内容的显式对应关系，导致模型难以从有限数据中学习到精确的像素级控制映射。当相机轨迹偏离训练分布时，生成结果往往出现漂移或抖动，无法精确反映用户意图。

**瓶颈二：主体运动被忽视，动态僵硬。** 在真实场景中，视频内容同时包含相机运动（全局刚性变换）和主体自身动态（如人物行走、旗帜飘动）。现有方法完全将相机控制与主体运动混为一谈，缺乏对独立于相机运动的主体动态的显式建模。这导致一个严重的后果：在包含可动对象的场景中，对象要么随相机运动而僵硬漂移，要么完全静止，无法呈现自然的动态行为。

针对上述瓶颈，本文提出 **I2VControl-Camera**，核心动机在于实现相机运动与主体动态的解耦控制。关键洞察是：视频中任意 3D 点的运动轨迹 $\mathcal{F}(\mathbf{p}, \lambda)$ 可以被分解为线性项（对应刚性相机运动）和高阶非线性项（对应主体自身动态）：

$$\mathcal{F}(\mathbf{p}, \lambda) = \mathbf{R}_\lambda \cdot \mathcal{F}(\mathbf{p}, 0) + \mathbf{t}_\lambda + \mathcal{G}(\mathbf{p}, \lambda)$$

其中 $\mathbf{R}_\lambda \cdot \mathcal{F}(\mathbf{p}, 0) + \mathbf{t}_\lambda$ 为线性分量，$\mathcal{G}(\mathbf{p}, \lambda)$ 为非线性残差。基于此分解，本文分别从两个分量中构建控制信号：将线性项投影到相机平面得到稠密的 2D 点轨迹 $\mathbf{T}_\lambda$，作为高精度相机控制信号；对非线性项的时间导数进行空间积分，得到表征整体运动强度的标量 $m_\lambda$，作为可调节的主体动态控制输入。这一设计使得用户可以在保持相同相机轨迹的前提下，独立调节场景中对象的运动幅度——从完全静止到显著动态。

## 核心创新

I2VControl-Camera 的核心创新在于将视频生成中的相机控制与主体运动控制彻底解耦，并通过两个相互独立但协同工作的“控制旋钮”实现精确操控。这一设计直接回应了现有方法的两个根本性瓶颈：控制信号过于稀疏导致相机控制精度不足，以及完全忽视主体动态导致可动对象僵硬。

### 控制信号表示：从稀疏外参到稠密点轨迹

现有相机控制方法（如 **MotionCtrl**（Wang et al., 2023）和 **CameraCtrl**（He et al., 2024））均以相机外参矩阵 $(R, t)$ 或其衍生表示（如 Plücker 射线嵌入）作为控制信号。这类信号本质上是稀疏的——一个 $4 \times 4$ 的刚体变换矩阵仅编码了全局相机位姿，缺乏与场景几何的像素级对应关系，导致生成视频的相机运动难以精确反映用户意图。

I2VControl-Camera 将控制信号替换为**相机坐标系下的稠密 2D 点轨迹** $T_\lambda$。具体而言，该方法将输入图像提升为 RGBD 点云 $\Omega$，然后根据相机运动 $(R_\lambda, t_\lambda)$ 对点云施加线性平移并投影回 2D 平面：

$$T_\lambda = \Pi(R_\lambda \cdot \Omega + t_\lambda), \quad \lambda \in [0, \Lambda]$$

这一信号提供了像素级的运动先验，使生成模型能够逐像素对齐相机运动（见 Figure 5 的定性验证）。与稀疏外参相比，稠密点轨迹将控制粒度从“整帧位移”提升到“逐点轨迹”，从根本上提高了控制精度。

### 主体运动建模：从完全忽视到显式可调

现有方法对场景中独立于相机运动的主体动态（如行走的人、飘动的衣物）完全不加区分，将其与相机运动混为一谈。这导致两个问题：在静态场景中，模型可能错误地引入不必要的主体运动；在动态场景中，主体运动又无法被独立控制。

I2VControl-Camera 通过将视频内容的 3D 点轨迹函数 $\mathcal{F}(p, \lambda)$ 进行线性-非线性分解来解决这一缺陷：

$$\mathcal{F}(p, \lambda) = R_\lambda \cdot \mathcal{F}(p, 0) + t_\lambda + \underbrace{\mathcal{G}(p, \lambda)}_{\text{非线性残差}}$$

其中线性项 $(R_\lambda, t_\lambda)$ 对应刚性相机运动，高阶非线性残差 $\mathcal{G}(p, \lambda)$ 对应主体自身动态。基于此分解，方法定义了一个标量**整体运动强度** $m_\lambda$，通过对非线性项速度的 $L_2$ 范数在空间域上积分得到：

$$m_\lambda = \frac{1}{|\Omega|} \int_\Omega \left\| \frac{\partial \mathcal{G}(p, \lambda)}{\partial \lambda} \right\|_2 dp$$

在离散实现中，$m_\lambda$ 近似为相邻帧间非线性轨迹图的平均 $L_2$ 距离。这一标量作为可调节的控制输入，使用户能够在相同相机轨迹下独立控制主体运动幅度：$m_\lambda = 0$ 时场景近乎静止，$m_\lambda$ 增大时主体运动逐渐显著（见 Figure 6 和 Table 2 的消融验证）。

### 网络集成方式：与基础模型解耦的适配器架构

与 **AnimateDiff**（Guo et al., 2024b）通过微调基础模型注入固定相机模式，或 MotionCtrl/CameraCtrl 通过嵌入特定模块（如 LoRA、适配器）与特定基础模型绑定不同，I2VControl-Camera 采用**与基础模型结构无关的独立适配器网络**。该适配器仅接收拼接后的控制信号 $(T_\lambda, m_\lambda)$，生成控制特征后注入扩散过程的时序注意力层。这一设计使得控制模块可灵活适配不同的 I2V 基础模型，无需修改预训练权重。

### 关键证据支撑

上述创新的有效性在实验中得到了系统验证。在 RealEstate10K 数据集上，所提方法在 RotErr、TransErr、FID 和 MSC 四项指标上均显著优于 MotionCtrl 和 CameraCtrl（Table 1）。在包含可动对象的场景中，$m_\lambda = 0$ 的变体（Ours-0）取得了最低的 RotErr（0.76）和 TransErr（6.97），验证了相机控制精度；而 $m_\lambda = 600$ 的变体（Ours-600）取得了最佳的 FID（91.86）和最高的 MSC（47.70），同时保持了自然的主体动态（Table 2）。这种在同一框架下通过单一标量参数实现控制精度与动态幅度独立调节的能力，是现有方法所不具备的。

## 整体框架

![[assets/figures/papers/paper_list_l37_I2VControl_Camera_Precise_Video_Camera_Control_with_Adjustable_Motion_St/figures/001_Figure_1.jpg]]
*Figure 1: We propose I2VControl-Camera, a novel camera control method for image-to-video generation, offering high control precision and adjustable motion strength*

I2VControl-Camera 的核心目标是将图像到视频生成中的相机控制与主体动态解耦，实现精确的相机轨迹跟随和可调节的主体运动幅度。为此，该方法构建了一套“控制信号构建—数据预处理—适配器注入”的三阶段流水线。

**控制信号构建模块**是整个框架的理论基础。给定一段动态视频，3D 空间中的任意点 $\mathbf{p}$ 随时间 $\lambda$ 的运动轨迹可表示为光滑映射 $\mathcal{F}(\mathbf{p}, \lambda): \mathbb{R}^3 \times [0, \Lambda] \to \mathbb{R}^3$。该方法的关键洞察在于将这一轨迹分解为线性项与高阶非线性项：

$$\mathcal{F}(\mathbf{p}, \lambda) = \mathbf{R}_\lambda \cdot \mathcal{F}(\mathbf{p}, 0) + \mathbf{t}_\lambda + \mathcal{G}(\mathbf{p}, \lambda)$$

其中，线性项 $(\mathbf{R}_\lambda, \mathbf{t}_\lambda)$ 对应场景中静态部分的刚性相机运动，而非线性残差 $\mathcal{G}(\mathbf{p}, \lambda) = o(\mathbf{p})$ 则捕获了独立于相机的主体动态。基于此分解，框架输出两类控制信号：

- **稠密 2D 点轨迹** $\mathbf{T}_\lambda$：将线性运动作用于 3D 区域 $\Omega$ 后投影到相机平面，得到 $\mathbf{T}_\lambda = \Pi(\mathbf{R}_\lambda \cdot \mathbf{\Omega} + \mathbf{t}_\lambda)$。相比传统方法使用的稀疏外参矩阵或 Plücker 嵌入，这一稠密轨迹提供了像素级的控制信号，显著提升了相机控制的精度与泛化性。
- **整体运动强度** $m_\lambda$：通过对非线性残差的时间导数求 $L_2$ 范数并在空间域积分，获得一个标量值 $m_\lambda = \frac{1}{|\Omega|} \int_\Omega \left\| \frac{\partial \mathcal{G}(\mathbf{p}, \lambda)}{\partial \lambda} \right\|_2 d\mathbf{p}$，用以表征场景中主体运动的剧烈程度。该标量作为可调节的控制输入，使用户能够在相同相机轨迹下独立操控对象的动态幅度。

**数据预处理流水线**负责从原始 RGB 视频中提取上述控制信号。其核心挑战在于视频中并不天然具备动静区域的标注。该方法通过迭代算法解决这一问题：首先利用深度估计和点追踪获取各帧的 3D 点轨迹；随后，在每轮迭代中，基于当前动静划分 $\Omega = \Omega_S \sqcup \Omega_D$，在静态区域上通过非线性最小二乘估计相机位姿：

$$(\mathbf{R}_\lambda, \mathbf{t}_\lambda) = \underset{\mathbf{R}, \mathbf{t}}{\arg\min} \| \Pi(\mathcal{F}(\Omega_S, \lambda)) - \Pi(\mathbf{R} \cdot \Omega_S + \mathbf{t}) \|^2$$

继而根据轨迹与线性运动模型的偏差更新动静划分，直至收敛。最终，从静态区域求解的 $(\mathbf{R}_\lambda, \mathbf{t}_\lambda)$ 用于计算 $\mathbf{T}_\lambda$，而运动强度 $m_\lambda$ 则在离散域中通过相邻帧间非线性轨迹的 $L_2$ 距离近似：

$$m_\lambda = \begin{cases} 0 & \text{if } \lambda = 0 \\ \frac{1}{HW} \sum_{i,j=1}^{H,W} \| \mathcal{G}(\mathbf{p}, \lambda) - \mathcal{G}(\mathbf{p}, \lambda-1) \|_2 & \text{if } \lambda > 0 \end{cases}$$

**适配器网络**将构建好的控制信号 $(\mathbf{T}_\lambda, m_\lambda)$ 注入基础图像到视频扩散模型。该适配器与基础模型结构无关，仅接收控制信号并生成控制特征，注入到扩散过程的时序注意力层中。在实现上，基础模型采用 MagicVideo-V2，生成 24 帧、704×448 分辨率的视频；适配器在约 30K 个包含相机运动和自然动态的视频片段上训练，使用 16 块 NVIDIA A100 GPU，训练约 20K 步、耗时约 36 小时。

整体而言，I2VControl-Camera 通过将运动分解为线性相机项与非线性主体项，分别作为控制精度与运动强度的信号源，实现了相机控制与对象运动的解耦操控。这一设计使得用户既能获得像素级对齐的相机轨迹跟随，又能通过调节 $m_\lambda$ 在“完全静止”到“显著运动”之间连续控制主体动态。

## 核心模块与公式推导

I2VControl-Camera 的核心架构由三个功能模块构成：**控制信号构建模块**、**数据预处理流水线**和**适配器网络**。其理论根基在于将视频内容的 3D 运动轨迹显式分解为线性项与高阶非线性项，从而解耦相机运动与主体动态。

### 动态序列的数学表示

考虑一段视频，将其中任意 3D 点 $\mathbf{p} \in \mathbb{R}^3$ 在时间 $\lambda \in [0, \Lambda]$ 上的运动轨迹定义为一个光滑映射函数 $\mathcal{F}$：

$$\mathcal{F}(\mathbf{p}, \lambda): \mathbb{R}^3 \times [0, \Lambda] \to \mathbb{R}^3, \quad \text{s.t.} \quad \mathcal{F}(\mathbf{p}, 0) = \mathbf{p}$$

该函数以第一帧为参考原点，描述了整个 3D 世界随时间的演变。直观上，整个 3D 世界可划分为**静态部分**与**动态部分**：静态部分在相机坐标系下遵循刚性线性运动，而动态部分则包含主体自身的非线性运动。

### 运动轨迹的线性-非线性分解

为解耦相机控制与主体运动，对 $\mathcal{F}$ 在 $\mathbf{p} = \mathbf{0}$ 处进行一阶麦克劳林展开：

$$\mathcal{F}(\mathbf{p}, \lambda) = \mathcal{F}(\mathbf{0}, \lambda) + \mathbf{J}_{\mathcal{F}}(\mathbf{0}, \lambda) \cdot \mathbf{p} + o(\mathbf{p})$$

其中 $\mathbf{J}_{\mathcal{F}}(\mathbf{0}, \lambda)$ 为雅可比矩阵，$o(\mathbf{p})$ 为高阶无穷小。将 $\mathcal{F}(\mathbf{0}, \lambda)$ 记作平移向量 $\mathbf{t}_\lambda$，$\mathbf{J}_{\mathcal{F}}(\mathbf{0}, \lambda)$ 记作旋转矩阵 $\mathbf{R}_\lambda$，则上式可重写为：

$$\mathcal{F}(\mathbf{p}, \lambda) = \mathbf{R}_\lambda \cdot \mathcal{F}(\mathbf{p}, 0) + \mathbf{t}_\lambda + o(\mathbf{p})$$

由此，定义**非线性残差** $\mathcal{G}(\mathbf{p}, \lambda)$ 为轨迹中偏离刚性相机运动的部分：

$$\mathcal{G}(\mathbf{p}, \lambda) \triangleq \mathcal{F}(\mathbf{p}, \lambda) - (\mathbf{R}_\lambda \cdot \mathcal{F}(\mathbf{p}, 0) + \mathbf{t}_\lambda) = o(\mathbf{p})$$

$\mathcal{G}$ 刻画了主体自身的动态程度——对于完全静态的场景，$\mathcal{G} \equiv \mathbf{0}$。

### 控制信号构建模块

基于上述分解，控制信号构建模块生成两类输入：

**1. 稠密 2D 点轨迹 $\mathbf{T}_\lambda$（相机控制信号）**

将输入图像通过深度估计提升为 RGBD 点云，取一个覆盖全图的 3D 区域 $\boldsymbol{\Omega}$。对该区域施加线性变换 $(\mathbf{R}_\lambda, \mathbf{t}_\lambda)$ 后，经相机投影 $\Pi$ 映射到 2D 平面，得到稠密的点轨迹：

$$\mathbf{T}_\lambda = \Pi(\mathbf{R}_\lambda \cdot \boldsymbol{\Omega} + \mathbf{t}_\lambda), \quad \lambda \in [0, \Lambda]$$

相比传统方法仅使用稀疏的 $4 \times 4$ 外参矩阵或 Plücker 射线嵌入，$\mathbf{T}_\lambda$ 提供了像素级稠密的控制信号，显著增强了可控精度。

**2. 运动强度 $m_\lambda$（主体动态控制信号）**

对非线性残差 $\mathcal{G}$ 求时间导数，并在空间域 $\Omega$ 上积分其 $L_2$ 范数，得到表征整体运动动态的标量：

$$m_\lambda = \frac{1}{|\Omega|} \int_\Omega \left\| \frac{\partial \mathcal{G}(\mathbf{p}, \lambda)}{\partial \lambda} \right\|_2 d\mathbf{p}$$

在离散视频中，以相邻帧间轨迹图的 $L_2$ 距离近似导数：

$$m_\lambda = \begin{cases} 0 & \text{if } \lambda = 0 \\ \frac{1}{HW} \sum_{i,j=1}^{H,W} \| \mathcal{G}(\mathbf{p}, \lambda) - \mathcal{G}(\mathbf{p}, \lambda-1) \|_2 & \text{if } \lambda > 0 \end{cases}$$

$m_\lambda$ 作为可调节的标量输入，控制生成视频中主体运动的幅度：当 $m_\lambda = 0$ 时场景近乎静止，增大 $m_\lambda$ 则主体运动愈发显著。

### 数据预处理流水线

为从原始 RGB 视频中提取训练所需的 $(\mathbf{T}_\lambda, m_\lambda)$ 控制信号，论文设计了一套迭代式动静分离算法：

1. **深度估计与点追踪**：对视频逐帧估计深度，并通过点追踪获得各像素的 3D 轨迹 $\mathcal{F}(\mathbf{p}, \lambda)$。
2. **动静区域划分**：将像素集合 $\Omega$ 划分为静态区域 $\Omega_S$ 与动态区域 $\Omega_D$（$\Omega = \Omega_S \sqcup \Omega_D$）。静态区域满足：
   $$\mathcal{F}(\mathbf{p}, \lambda) \equiv \mathbf{R}_\lambda \cdot \mathcal{F}(\mathbf{p}, 0) + \mathbf{t}_\lambda, \quad \forall \mathbf{p} \in \Omega_S$$
3. **相机位姿估计**：在静态区域上通过非线性最小二乘求解旋转和平移：
   $$(\mathbf{R}_\lambda, \mathbf{t}_\lambda) = \underset{\mathbf{R}, \mathbf{t}}{\arg\min} \left\| \Pi(\mathcal{F}(\Omega_S, \lambda)) - \Pi(\mathbf{R} \cdot \Omega_S + \mathbf{t}) \right\|^2$$
4. **迭代优化**：交替更新动静划分与相机位姿，直至收敛，最终输出 $(\mathbf{T}_\lambda, m_\lambda)$。

### 适配器网络

适配器网络与基础模型结构无关，接收拼接后的控制信号 $(\mathbf{T}_\lambda, m_\lambda)$，编码为控制特征后注入到基础 I2V 扩散模型（MagicVideo-V2）的时序注意力层中。这种即插即用的设计使得方法可迁移至不同的基础架构，而无需修改扩散模型本身的权重。

## 实验与分析

### 实验设置

本文采用 **MagicVideo-V2** 作为基础图像到视频（I2V）扩散模型，所有生成视频均为 24 帧、704×448 分辨率。训练使用 16 张 NVIDIA A100 GPU，每卡批次大小为 1，共训练 20K 步，耗时约 36 小时。训练数据集包含约 30K 个视频片段，涵盖相机运动和自然主体动态，而非直接使用 RealEstate10K 进行训练。评估指标采用领域标准的旋转误差（RotErr）、平移误差（TransErr）、FID 和运动平滑度一致性（MSC）。基线方法包括 **MotionCtrl**（Wang et al., 2023）、**CameraCtrl**（He et al., 2024）和 **AnimateDiff**（Guo et al., 2024b），均使用相同的基础模型和分辨率设置，确保对比公平性。

### 主实验结果

**RealEstate10K 数据集。** 如表 1 所示，I2VControl-Camera 在所有四项指标上均显著优于 MotionCtrl 和 CameraCtrl。具体而言，Ours-0（运动强度设为 0 的变体）在控制精度上达到最优：FID 为 155.01，MSC 为 12.93，表明生成的视频在相机轨迹精度、图像质量和时序一致性上全面领先。MotionCtrl 和 CameraCtrl 由于仅依赖稀疏的外参矩阵或 Plücker 嵌入，控制信号泛化性不足，导致 RotErr 和 TransErr 明显偏高。


![[assets/figures/papers/paper_list_l37_I2VControl_Camera_Precise_Video_Camera_Control_with_Adjustable_Motion_St/figures/008_Table_1.jpg]]
*Table 1: Comparison on the RealEstate10k dataset*

**可动对象数据集。** 表 2 的结果进一步验证了该方法在包含独立运动主体的场景中的优势。Ours-0 取得了最低的控制误差（RotErr=0.76, TransErr=6.97），证明在完全抑制主体动态时，相机控制精度不受影响。Ours-600（运动强度设为 600 的变体）则取得了最佳 FID（91.86）和最高 MSC（47.70），表明在允许主体自然运动时，图像质量和动态丰富度均达到最优。对比方法的 MSC 值介于 Ours-0 的 18.96 与 Ours-600 的 47.70 之间，无法实现从静态到动态的灵活调节。


![[assets/figures/papers/paper_list_l37_I2VControl_Camera_Precise_Video_Camera_Control_with_Adjustable_Motion_St/figures/009_Table_2.jpg]]
*Table 2: Comparison on the movable object dataset*

### 运动强度可调性分析

运动强度 $m_\lambda$ 是本文的核心可控变量。定性结果（Figure 6）表明：当 $m_\lambda=0$ 时，即使场景中存在北极熊、宇航员、狼等可动对象，整个画面也近乎静止；当 $m_\lambda$ 增大至 600 时，主体对象开始显著运动，而相机轨迹保持一致。定量上，Ours-0 和 Ours-600 在 MSC 上的巨大跨度（18.96 vs 47.70）直接量化了这种可调性，且相机控制精度（RotErr, TransErr）在此过程中保持稳定。这验证了将视频 3D 点轨迹分解为线性项（相机运动）和高阶非线性项（主体动态）的解耦策略的有效性。

### 像素级控制精度

Figure 5 展示了该方法的像素级可控性。通过估计输入图像的度量深度，将 RGBD 点云按控制信号操纵后渲染预览图，生成结果与预览图在像素级别高度对齐（如绿色框所示），即使在存在可动对象（如猫，红色框所示）的区域，相机运动仍被精确执行，主体动态保持独立。

### 与基线的定性比较

Figure 7 的定性对比显示，在相同相机轨迹下，I2VControl-Camera 的生成结果最接近预览图，控制精度明显优于 MotionCtrl 和 CameraCtrl。后两者由于控制信号稀疏，在复杂场景中容易出现漂移或内容失配。

### 消融与局限性

消融实验的核心结论是：运动强度 $m_\lambda$ 的引入是实现主体动态可控的关键。当 $m_\lambda$ 设为 0 时，场景趋于静态；当 $m_\lambda$ 增大时，主体运动幅度随之增加，且相机控制精度不受影响（Table 2, Figure 6）。

当前框架的局限性主要体现在两方面：其一，仅支持相机运动与主体运动的解耦控制，尚未包含拖拽、运动刷等更细粒度的局部控制模态；其二，控制信号的构建依赖于深度估计和点追踪的精度，对训练数据的质量有较高要求。在更复杂的动态场景（如多物体交互、快速运动）中，控制精度和运动自然度仍有待进一步验证。
## 方法谱系与知识库定位

### 与现有相机控制方法的对比

当前图像到视频（I2V）生成中的相机控制方法主要集中在如何将相机运动信号注入扩散模型。**MotionCtrl** (Wang et al., 2023) 直接将外参矩阵（旋转矩阵和平移向量）作为控制信号，通过微调基础模型的时序注意力层来实现相机轨迹控制。**CameraCtrl** (He et al., 2024) 在此基础上将外参矩阵转换为 Plücker 射线嵌入，以增强控制信号的空间表达能力。**AnimateDiff** (Guo et al., 2024b) 则通过 LoRA 适配器学习固定的相机运动模式。

这些方法的共同瓶颈在于：控制信号本质上是稀疏的——外参矩阵仅包含 6 个自由度（3 个旋转 + 3 个平移），Plücker 嵌入虽有所改善，但仍难以精确反映用户对画面中每个像素运动轨迹的意图。更关键的是，它们完全忽视了场景中独立于相机运动的主体动态（如行走的人、飘动的旗帜），导致可动对象在生成视频中僵硬或无法自然运动。

I2VControl-Camera 从三个维度突破了上述局限：

1.  **控制信号表示**：将稀疏的外参矩阵替换为相机坐标系下的稠密 2D 点轨迹 $\mathbf{T}_\lambda$。具体而言，将输入图像提升为 RGBD 点云，根据相机运动参数在三维空间中移动该点云，再投影回二维平面，得到逐像素的运动轨迹。这种稠密表示使控制精度从“全局一致”提升到“像素级对齐”。

2.  **主体运动建模**：首次显式建模场景中独立于相机运动的主体动态。将视频内容的 3D 点轨迹 $\mathcal{F}(\mathbf{p}, \lambda)$ 分解为线性项（对应刚性相机运动 $\mathbf{R}_\lambda, \mathbf{t}_\lambda$）和高阶非线性残差 $\mathcal{G}(\mathbf{p}, \lambda)$，并通过非线性项时间导数的域积分计算整体运动强度 $m_\lambda$，作为可调节的控制输入。

3.  **网络集成方式**：采用与基础模型结构无关的独立适配器网络，仅接收控制信号 $(\mathbf{T}_\lambda, m_\lambda)$ 并生成控制特征注入扩散过程，无需修改基础模型的预训练权重。这使得方法可以灵活适配不同的基础 I2V 模型。

### 适用边界与局限

**适用场景**：

- 需要精确相机轨迹控制的图像到视频生成任务，如建筑漫游、产品展示等静态场景。
- 同时包含相机运动和主体动态的混合场景，如街道跟拍、自然风光中的人物/动物活动。
- 需要调节主体运动幅度的创意生成场景，从完全静态到显著运动连续可调。

**已知局限**：

1.  **控制模态单一**：当前框架仅支持相机运动和主体运动强度的解耦控制，未包含拖拽（drag）、运动刷（motion brush）等更细粒度的局部控制模态。对于需要精确操控特定对象运动轨迹的场景，方法尚无法覆盖。

2.  **数据质量依赖**：控制信号的构建依赖于深度估计和点追踪的精度。深度估计误差会导致 RGBD 点云几何失真，点追踪误差会污染动静分离和运动强度计算。这意味着方法性能与训练/推理数据的质量强相关，在深度估计困难（如透明物体、弱纹理区域）或点追踪失败（如快速运动、严重遮挡）的场景下，控制精度可能下降。

### 开放问题

1.  **多模态控制扩展**：如何将当前框架扩展以支持拖拽控制、运动刷控制等更多控制模态？一个可能的方向是将非线性残差 $\mathcal{G}(\mathbf{p}, \lambda)$ 进一步分解为不同对象/区域的独立运动分量，实现更精细的视频内容操控。

2.  **复杂动态场景鲁棒性**：当前实验主要在 RealEstate10K（以静态场景为主）和自建的可动对象数据集上验证。在多物体交互、快速运动、严重遮挡等更复杂的动态场景中，动静分离算法和非线性建模能否保持控制精度和运动自然度，尚需进一步验证。

3.  **与基础模型的解耦程度**：虽然适配器网络在结构上与基础模型无关，但训练过程仍依赖于特定基础模型的中间特征分布。能否实现完全零样本（zero-shot）迁移到新的基础 I2V 模型，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/ICLR_2025/I2VControl_Camera_Precise_Video_Camera_Control_with_Adjustable_Motion_Strength.pdf]]
