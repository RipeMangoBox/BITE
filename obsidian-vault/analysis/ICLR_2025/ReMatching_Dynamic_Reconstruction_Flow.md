---
title: "ReMatching Dynamic Reconstruction Flow"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/ReMatching_Dynamic_Reconstruction_Flow.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/ReMatchingDynamicReconstructionFlow/
aliases:
- RF
- RDRF
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过 ReMatching 损失控制优化过程，使重建流尽可能接近所需速度场先验类，而不是严格强制隶属。"
primary_logic: "利用速度场先验类的简化特性，将时间依赖重建函数到先验类的投影转化为流匹配问题，并通过模拟交替投影法设计 ReMatching 损失，在不降低保真度的前提下整合先验知识。"
claims:
- "ReMatching 框架的优化目标对齐重建解与先验正则化，而不牺牲保真度。"
- "将投影到速度场先验类上的问题转化为流匹配问题。"
- "ReMatching 损失作为流匹配损失，将匹配后的速度场重新投影回重建流集合。"
- "最终损失函数为重建损失与 ReMatching 损失的加权和，λ=0.001 控制先验强度。"
---

# ReMatching Dynamic Reconstruction Flow

> [!tip] 核心洞察
> 利用速度场先验类的简化特性，将时间依赖重建函数到先验类的投影转化为流匹配问题，并通过模拟交替投影法设计 ReMatching 损失，在不降低保真度的前提下整合先验知识。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ReMatching动态重建流 |
| 英文题名 | ReMatching Dynamic Reconstruction Flow |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://arxiv.org/abs/2411.00705) · [Project](https://research.nvidia.com/labs/toronto-ai/ReMatchingDynamicReconstructionFlow/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ReMatching Framework |
| Dataset | D-NeRF (GA3D setting), Dynamic Scenes |

> [!tip] 效果简介
> - D-NeRF (GA3D setting) 上，PSNR↑ 为 32.21，对比 32.02，变化 +0.19。
> - D-NeRF (GA3D setting) 上，PSNR↑ 为 38.18，对比 37.83，变化 +0.35。
> - Dynamic Scenes 上，LPIPS↓ 为 0.2533，对比 0.2922，变化 -0.0389。

## 概要

动态场景重建的核心瓶颈在于：多视角输入在时间和空间维度上高度稀疏，使得模型难以有效学习时变表示；而引入形变先验时，又往往以牺牲重建保真度为代价。ReMatching 框架针对这一矛盾，提出了一种新的优化控制机制——通过 ReMatching 损失引导重建流尽可能接近所需的速度场先验类，而非强制严格隶属，从而在不降低保真度的前提下整合先验知识。

该方法的核心洞察在于：将时间依赖重建函数到速度场先验类的投影转化为流匹配问题，并借鉴模拟交替投影法设计 ReMatching 损失。具体而言，框架在标准重建损失 $L_{\mathrm{REC}}$ 基础上，附加一个流匹配损失 $L_{\mathrm{RM}}$，总损失为 $L(\boldsymbol{\theta}) = L_{\mathrm{REC}}(\boldsymbol{\theta}) + \lambda L_{\mathrm{RM}}(\boldsymbol{\theta})$，其中 $\lambda=0.001$ 控制先验强度。该损失仅在训练阶段使用，不影响推断速度。

实验表明，ReMatching 框架可无缝嵌入现有动态重建流程。在 D-NeRF 基准上，应用于 GA3D 基线时，Hell Warrior 场景 PSNR 从 32.02 提升至 32.21，JumpingJacks 场景从 37.83 提升至 38.18；在 Dynamic Scenes 基准上，Truck 场景 LPIPS 从 0.2922 降至 0.2533。定性结果进一步显示，该方法在运动部件周围的重建更为精确。

**方法定位**：ReMatching 属于动态重建中基于速度场先验的正则化框架，区别于依赖数值模拟 ODE 的流程，专为仿真自由的动态模型设计。其先验类可灵活定义，涵盖分片刚体、体积保持等约束，并支持自适应组合。

动态场景重建旨在从多视角视频输入中恢复随时间变化的三维几何与外观，是计算机视觉与图形学中长期存在的核心问题。其应用涵盖虚拟现实、电影制作和数字孪生等领域。近年来，基于神经辐射场（NeRF）和三维高斯溅射（3D Gaussian Splatting）的静态重建方法取得了显著进展，但这些方法向动态场景的扩展面临根本性挑战。

**核心瓶颈**在于多视角输入的稀疏性——不仅在空间上（有限相机数量），更在时间上（离散帧采样）。这种双重稀疏性使得从观测中直接学习时变表示变得极度欠定：模型需要在仅看到少量时间戳的条件下，推断出任意时刻的连续形变。现有的动态重建方法通常通过引入某种形变先验来缓解这一困难，例如依赖网络结构的隐式平滑性，或显式建模刚体运动。然而，这些先验往往以牺牲重建保真度为代价——更强的正则化虽然稳定了优化，却可能导致对细节的过度平滑或对复杂运动的错误解释。

这一困境暴露了当前动态重建流程的一个关键缺口：**如何在整合形变先验知识的同时，不损害对观测数据的高保真度拟合**。现有方法缺乏一种灵活的机制，能够在优化过程中动态平衡先验约束与数据拟合，而不是简单地将先验作为硬约束或固定惩罚项。

本文的动机正是源于这一观察。我们提出 **ReMatching 框架**，其核心思想是：利用速度场先验类（velocity-field prior class）的简化特性，将时间依赖重建函数到先验类的投影转化为一个流匹配（flow-matching）问题。通过设计一种名为 **ReMatching 损失**的新型训练目标，框架引导优化过程使重建流尽可能接近所需的速度场先验类，而非严格强制隶属关系。这种“软对齐”策略使得模型能够在保持重建保真度的前提下，有效吸收先验知识，从而突破了传统方法中保真度与正则化之间的折中困境。

## 核心方法与创新机理

ReMatching 框架的核心创新在于**解耦了动态重建中的保真度优化与形变先验整合**，通过一个精心设计的流匹配损失（ReMatching Loss）来引导优化过程，而非强制约束重建解必须严格属于某个先验类。

### 1. 瓶颈洞察：保真度与先验的固有张力

动态场景重建面临一个根本性困境：多视角输入在时间和空间维度上高度稀疏，使得模型难以仅从数据中学习到物理上合理的动态表示；然而，直接引入形变先验（如刚体运动、体积保持等）往往会过度约束优化空间，导致重建保真度下降。现有方法通常将先验知识硬编码到网络结构或损失函数中，缺乏对约束强度的灵活控制。

### 2. 核心机制：流匹配作为软约束

ReMatching 框架的关键突破是将“先验整合”重新定义为一个**流匹配问题**。给定一个仿真自由（simulation-free）的动态重建模型 $\Psi_t$ 和一个速度场先验类 $\mathcal{P}$，框架并不要求 $\Psi_t$ 生成的形变流严格属于 $\mathcal{P}$，而是：

1. **匹配投影**：对于每个时间步 $t$，在 $\mathcal{P}$ 中寻找与当前重建流最接近的速度场 $u_t$：
   $$u(\cdot, t) = \underset{u_t \in \mathcal{P}}{\arg\min} \; \rho(u_t, \psi_t)$$
   其中 $\rho$ 是衡量速度场与重建函数之间差异的泛函，基于连续性方程定义：
   $$\rho(u_t, \psi_t) = \int \left| \frac{\partial}{\partial t} \psi_t(\pmb{x}) + \mathrm{div}(\psi_t(\pmb{x}) u_t(\pmb{x})) \right|^2 d\pmb{x}$$

2. **反向投影损失**：将匹配得到的最优先验速度场 $u_t$ 作为目标，计算重建流与之的偏差，形成 ReMatching 损失：
   $$L_{\mathrm{RM}}(\theta) = \mathbb{E}_{t \sim U[0,1]} \; \rho(u_t, \psi_t)$$

3. **加权联合优化**：最终训练目标为重建损失与 ReMatching 损失的加权和：
   $$L(\pmb{\theta}) = L_{\mathrm{REC}}(\pmb{\theta}) + \lambda L_{\mathrm{RM}}(\pmb{\theta})$$
   其中 $\lambda = 0.001$ 在所有实验中固定，提供稳定且微弱的先验引导。

这一设计的精妙之处在于：**$\lambda$ 控制的是优化方向的偏好强度，而非解空间的硬性边界**。当 $\lambda \to 0$ 时，框架退化为纯重建基线；当 $\lambda$ 适度增大时，优化过程被温和地推向与先验一致的解，但不会强制牺牲数据拟合。

### 3. 与基线方法的关键差异

| 设计维度 | 基线方法（D3G / GA3D） | ReMatching 框架 |
|---------|----------------------|----------------|
| **训练损失** | 仅图像重建损失 $L_{\mathrm{REC}}$ | $L_{\mathrm{REC}} + \lambda L_{\mathrm{RM}}$，$\lambda=0.001$ |
| **动态先验** | 无显式形变先验，仅通过时间条件 MLP 隐式正则化 | 显式速度场先验类（分片刚体、体积保持、自适应组合），通过流匹配损失引导 |
| **约束性质** | 隐式、不可控 | 显式、软约束，强度可调 |
| **推断开销** | 无额外开销 | 无额外开销（ReMatching 损失仅训练时计算） |

### 4. 先验类的灵活设计

框架支持多种速度场先验类，可根据场景特性灵活选择：

- **$\mathcal{P}_{\mathrm{II}}$（分片刚体先验）**：速度场由反对称矩阵（旋转）与平移生成，适用于刚体运动主导的场景：
  $$\mathcal{P}_{\mathrm{II}} = \{ u_t \mid u(\mathbf{x}, t) = A_t \mathbf{x} + b_t, \; A_t = -A_t^T \}$$

- **$\mathcal{P}_{\mathrm{III}}$（体积保持先验）**：通过旋度基函数构造无散度速度场，适用于不可压缩形变：
  $$\mathcal{P}_{\mathrm{III}} = \{ u_t \mid u_t(\pmb{x}) = \sum_{j=1}^{k} \beta_j b_j(\pmb{x}), \; \mathrm{div}(b_j) = 0 \}$$

- **$\mathcal{P}_{\mathrm{IV}}$（自适应组合先验）**：通过学习权重 $w_j(\pmb{x}, t)$ 组合多个刚体运动，自动发现场景中的运动部件：
  $$\mathcal{P}_{\mathrm{IV}} = \{ u_t \mid u(\pmb{x}, t) = \sum_{j=1}^{k} w_j(\pmb{x}, t) u_j(\pmb{x}, t), \; u_j \in \mathcal{P}_{\mathrm{II}} \}$$

自适应组合先验是框架最具特色的设计：它无需人工指定运动部件，而是通过可学习的权重网络自动分配高斯点到不同的刚体运动模式，配合熵正则化防止权重退化到平凡解。

### 5. 梯度计算的关键技巧

ReMatching 损失涉及内层 $\arg\min$ 优化问题，直接计算梯度需要昂贵的二阶导数。框架利用 **Danskin 定理**规避了这一困难：在匹配优化问题为严格凸且唯一解的条件下，$L_{\mathrm{RM}}$ 对模型参数 $\theta$ 的梯度可以通过对最优 $u_t$ 处的外层函数直接求导获得，无需对 $\arg\min$ 算子求导。这一技巧使得训练开销保持在可接受范围内（参见 Figure 15 的运行时分析）。

### 6. 适用范围与边界

该创新机制的一个关键前提是重建模型必须是**仿真自由**的——即 $\psi_t$ 的每次评估仅需单步前向计算，不涉及 ODE 数值求解。这使其天然适用于基于 MLP 的时间条件变形网络（如 D3G、GA3D），但**不适用于需要数值模拟的神经 ODE 类方法**。此外，先验类的设计仍依赖领域知识，对于液体、气体等复杂物理现象，需要设计更丰富的先验类（论文将此列为开放问题）。

ReMatching 框架的核心设计理念是：**在不牺牲重建保真度的前提下，将形变先验注入动态重建模型的优化过程**。框架假定重建模型由一组仿真自由（simulation-free）的时间依赖函数 $\psi_t$ 构成，即每次评估 $\psi_t$ 仅需单步计算，无需数值求解常微分方程。

### 框架总览

整个 pipeline 由四个核心模块构成，形成“重建—匹配—投影—反馈”的闭环：

1. **动态高斯溅射渲染模块**：以可微 3D 高斯表示场景，通过 alpha 混合渲染图像。该模块接收时变高斯参数（位置、协方差、颜色、不透明度），输出渲染图像。
2. **时间依赖形变 MLP ($\psi_t$)**：为每个参考高斯预测时变偏移量 $\mu^i(t)$、$\Sigma^i(t)$，以及自适应组合权重 $w_{ij}(t)$。该模块采用位置编码与多层感知机，将时间 $t$ 映射到高斯参数空间。
3. **ReMatching 损失计算模块**：这是框架的核心创新。给定当前重建流 $\psi_t$ 和预设的速度场先验类 $\mathcal{P}$，该模块求解一个匹配优化问题，找到先验类中最接近 $\psi_t$ 的速度场 $u_t$，然后计算流匹配损失 $L_{\mathrm{RM}}$。
4. **重建损失模块**：计算渲染图像与真实图像之间的 $L_1$/$L_2$ 重建损失 $L_{\mathrm{REC}}$。

### 数据流与优化闭环

训练时，输入为多视角动态视频帧。数据流如下：

- **前向传播**：时间 $t$ 输入形变 MLP $\psi_t$，生成时变高斯参数 $\Psi_t = \{ \mu^i + \mu^i(t), \Sigma + \Sigma^i(t), c^i, \alpha^i, w_{ij}(t) \}_{i=1}^n$；高斯溅射渲染模块据此生成渲染图像。
- **重建损失**：渲染图像与真实图像比较，计算 $L_{\mathrm{REC}}$。
- **ReMatching 损失**：从 $\psi_t$ 中提取粒子的位置与速度信息（或图像空间的对应量），在速度场先验类 $\mathcal{P}$ 中求解匹配优化问题得到 $u_t$，再计算 $L_{\mathrm{RM}} = \mathbb{E}_{t \sim U[0,1]} \rho(u_t, \psi_t)$。
- **总损失**：$L(\theta) = L_{\mathrm{REC}}(\theta) + \lambda L_{\mathrm{RM}}(\theta)$，其中 $\lambda = 0.001$ 控制先验强度。
- **反向传播**：通过 Danskin 定理，$L_{\mathrm{RM}}$ 的梯度可直接计算，无需对匹配优化中的 $\arg\min$ 进行微分。

### 关键设计决策

**仿真自由假设**是框架适用性的边界条件。ReMatching 仅适用于每个时间步可独立评估的模型（如 NeRF、3D 高斯溅射），无法直接用于需要数值模拟 ODE 的流程。

**先验类与匹配解耦**是框架灵活性的来源。先验类 $\mathcal{P}$ 定义了允许的形变模式（分片刚体、体积保持、自适应组合等），而匹配优化将当前重建流投影到该先验类上。这种解耦使得先验设计独立于重建模型架构，同一套先验类可应用于不同的动态重建基线。

**ReMatching 损失仅在训练阶段使用**，推断时不增加任何计算开销。训练采用统一协议：100K 高斯，40K 迭代，前 3K 迭代仅优化静态参数 $\{\mu^i, \Sigma^i, c^i, \alpha^i\}$，之后引入形变 MLP 和 ReMatching 损失进行联合优化。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2411_00705/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative comparison of our method to D3G (Yang et al., 2023) on the HyperNeRF dataset (Park et al., 2021b). Our framework yields more accurate reconstructions, in particular around moving parts*


### 动态图像模型

ReMatching 框架将动态重建模型统一抽象为时间依赖的图像模型 $\Psi_t$：

$$t \mapsto \Psi_t = \{ \psi(t) \mid \psi : \mathbb{R}_+ \to V \}$$

其中每个 $\psi$ 将时间映射到向量空间 $V$，$\Psi_t$ 表示所有模型组件在时刻 $t$ 的评估结果。框架假设重建模型是**仿真自由**的（simulation-free），即每次对 $\psi_t$ 的评估仅需单步计算，无需数值求解常微分方程。这一假设排除了需要数值模拟 ODE 的流程，但覆盖了当前主流的动态重建范式。

### 速度场与连续性方程

对于时间依赖的重建函数 $\psi_t$，其形变可由速度场 $v: \mathbb{R}^d \times \mathbb{R}_+ \to \mathbb{R}^d$ 描述。$\psi_t$ 与生成速度场 $v_t$ 之间满足**连续性方程**：

$$\frac{\partial}{\partial t} \psi_t(\pmb{x}) + \mathrm{div}\left( \psi_t(\pmb{x}) v_t(\pmb{x}) \right) = 0, \quad \forall \pmb{x} \in \mathbb{R}^d$$

该方程是 $v_t$ 生成流 $\phi_t$ 下 $\psi_t = \psi_0 \circ \phi_t^{-1}$ 的充分必要条件，为后续匹配优化提供了约束基础。

### 匹配优化问题

给定先验速度场类 $\mathcal{P}$，ReMatching 的核心操作是将当前重建流投影到先验类上，求解匹配优化问题：

$$\boldsymbol{u}(\cdot, t) = \underset{\boldsymbol{u}_t \in \mathcal{P}}{\arg\min} \; \rho(\boldsymbol{u}_t, \boldsymbol{\psi}_t)$$

其中匹配代价泛函 $\rho$ 测量速度场 $u_t$ 与重建函数 $\psi_t$ 之间的差异，基于连续性方程构造：

$$\rho(u_t, \psi_t) = \int \left| \frac{\partial}{\partial t} \psi_t(\pmb{x}) + \mathrm{div}\left( \psi_t(\pmb{x}) u_t(\pmb{x}) \right) \right|^2 d\pmb{x}$$

### ReMatching 损失

匹配优化得到的先验速度场 $u_t$ 随后被用于引导重建流的优化方向。ReMatching 损失定义为时间上的期望：

$$L_{\mathrm{RM}}(\theta) = \mathbb{E}_{t \sim U[0,1]} \; \rho(u_t, \psi_t)$$

该损失作为流匹配损失，旨在使重建流尽可能接近先验速度场 $u_t$，但不强制严格隶属。梯度计算通过 **Danskin 定理**实现，无需对 $\arg\min$ 算子求导，从而保证训练的高效性。

### 总损失函数

训练总损失为重建损失与 ReMatching 损失的加权组合：

$$L(\pmb{\theta}) = L_{\mathrm{REC}}(\pmb{\theta}) + \lambda L_{\mathrm{RM}}(\pmb{\theta})$$

其中 $L_{\mathrm{REC}}$ 为图像重建损失（如 L1 损失），$\lambda$ 控制先验正则化强度。在所有实验中 $\lambda = 0.001$ 固定不变，消融实验表明 $\lambda \in [5\times10^{-4}, 5\times10^{-3}]$ 范围内 PSNR 稳定提升，$\lambda \leq 5\times10^{-5}$ 时与基线一致，$\lambda \geq 0.01$ 时优化不稳定。

### 粒子形式与隐式表示形式

匹配损失 $\rho$ 的具体形式取决于向量空间 $V$ 的选择：

**粒子形式**（$V = \mathbb{R}^{n \times d}$）：当 $\psi_t$ 由 $n$ 个粒子的轨迹 $\gamma_t^i$ 定义时，匹配损失退化为：

$$\rho(u_t, \psi_t) = \sum_{i=1}^{n} \left\| u_t(\gamma_t^i) - \frac{d}{dt} \gamma_t^i \right\|^2$$

**隐式表示形式**（$V = C^1(\mathbb{R}^d)$）：当 $\psi_t$ 为连续可微函数时，匹配损失在采样点 $\pmb{x}_i$ 上近似为：

$$\rho(u_t, \psi_t) = \sum_{i=1}^{n} \left| \frac{\partial}{\partial t} \psi_t(\pmb{x}_i) + \langle \nabla \psi_t(\pmb{x}_i), u_t(\pmb{x}_i) \rangle \right|^2$$

### 先验速度场类

ReMatching 框架通过设计不同的先验类 $\mathcal{P}$ 引入形变约束：

**刚体形变先验** $\mathcal{P}_{II}$：速度场由反对称矩阵（旋转）与平移生成，适用于局部刚体运动：

$$\mathcal{P}_{II} = \{ u_t \mid u(\mathbf{x}, t) = A_t \mathbf{x} + b_t, \; A_t = -A_t^T, \; b_t \in \mathbb{R}^d \}$$

**无散度先验** $\mathcal{P}_{III}$：速度场满足 $\mathrm{div}(u) = 0$，保证体积保持。通过旋度基函数 $b_j$ 构造：

$$\mathcal{P}_{III} = \{ u_t \mid u_t(\pmb{x}) = \sum_{j=1}^{k} \beta_j b_j(\pmb{x}), \; \beta \in \mathbb{R}^k \}$$

其中 $b_j(\pmb{x}) \in \{ \mathrm{curl}(\phi_j(\pmb{x}) \pmb{e}_1^T), \cdots, \mathrm{curl}(\phi_j(\pmb{x}) \pmb{e}_d^T) \}$。

**自适应组合先验** $\mathcal{P}_{IV}$：通过学习权重 $w_j$ 组合多个刚体运动，实现分片刚体形变：

$$\mathcal{P}_{IV} = \{ u_t \mid u(\pmb{x}, t) = \sum_{j=1}^{k} w_j(\pmb{x}, t) u_j(\pmb{x}, t), \; u_j \in \mathcal{P}_{II} \}$$

权重 $w_j$ 由形变 MLP 预测并通过 softmax 归一化，需额外引入熵正则化以避免权重退化为单一件分配。消融实验表明零件数 $k \in [5, 15]$ 范围内性能稳定，$k=1$ 时退化为 $\mathcal{P}_I$ 导致性能下降。

### 关键模块总结

| 模块 | 角色 | 核心机制 |
|------|------|----------|
| 动态高斯溅射渲染 | 场景表示与图像渲染 | 可微 3D 高斯通过 alpha 混合渲染像素颜色 |
| 时间依赖形变 MLP | 预测时变偏移 | 位置编码 + MLP 预测 $\mu^i(t)$、$\Sigma^i(t)$ 及权重 $w_{ij}(t)$ |
| ReMatching 损失计算 | 先验引导优化 | 求解匹配优化得 $u_t$，计算流匹配损失 $L_{\mathrm{RM}}$ |
| 重建损失 | 数据保真度 | 渲染图像与真实图像间的 L1/L2 损失 |

ReMatching 损失的两种应用模式——基于几何（粒子位置）和基于图像（渲染像素）——使其可灵活适配不同的动态重建管线。该损失仅在训练阶段使用，推断时间不受影响。

## 实验与关键发现

### 核心实验设置

所有实验遵循统一的训练协议，以确保公平比较。模型使用 **100K 个 3D 高斯**，训练 **40K 次迭代**，前 **3K 次迭代**仅优化静态参数（均值 μ^i、协方差 Σ^i、颜色 c^i、不透明度 α^i）。ReMatching 损失权重 λ 在所有实验中固定为 **0.001**。评估在多个基准上进行，涵盖合成与真实场景：**D-NeRF** (Pumarola et al., 2021)、**HyperNeRF** (Park et al., 2021b) 和 **Dynamic Scenes** (Yoon et al., 2020; Yang et al., 2023)。推断时间不受 ReMatching 影响，因为该损失仅在训练时使用。

### 主要结果

在 D-NeRF 数据集上，将 ReMatching 框架应用于 **D3G** (Yang et al., 2023) 基线时，未见帧的 PSNR 指标取得一致提升。Table 1 报告了完整评估结果，其中多个场景的 PSNR 和 SSIM 指标均优于基线。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2411_00705/figures/003_Table_1.jpg]]
*Table 1: Image quality evaluation on unseen frames for the D-NeRF dataset (Pumarola et al., 2021)*

进一步地，在 **GA3D** (Lu et al., 2024) 基线上应用 ReMatching 框架，结果如 Table 3 所示。在 Hell Warrior 场景上，PSNR 从 32.02 提升至 **32.21** (+0.19)；在 JumpingJacks 场景上，PSNR 从 37.83 提升至 **38.18** (+0.35)。该实验使用 400×400 分辨率、白色背景，保持 GA3D 原论文的评估设定。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2411_00705/figures/012_Table_3.jpg]]
*Table 3: Image quality evaluation on unseen frames for the D-NeRF dataset with our framework applied on top of the 3D Geometry-aware Deformable Gaussians (Lu et al., 2024). Image resolution is scaled down to 400x400 pixels and the background is white, maintaining the settings of the GA3D paper evaluation*

在 Dynamic Scenes 真实场景数据集上，Table 4 展示了未见帧的评估结果。Truck 场景的 LPIPS 从 0.2922 降至 **0.2533** (-0.0389)，表明感知重建质量显著提升。Figure 8 的定性比较显示，ReMatching 方法在动态区域（尤其是移动部件周围）的重建更为精确。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2411_00705/figures/015_Figure.jpg]]

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2411_00705/figures/017_Figure.jpg]]

在 HyperNeRF 数据集上，Figure 3 的定性比较显示，相比 D3G 基线，ReMatching 框架在移动部件附近产生了更准确的重建结果。

### 自适应先验类的有效性

Figure 4 可视化了自适应组合先验类（P_IV）学习到的零件分配。可以看出，模型自动将场景中的不同运动部件分配到不同的刚体运动组，无需人工标注。这种自适应机制使得先验能够灵活适应场景的局部运动结构。

### 消融实验

**ReMatching 损失权重 λ**：Figure 18 展示了 λ 对 PSNR 的影响。在 Hell Warrior 和 Lego 场景上，λ 在 **[5e-4, 5e-3]** 范围内 PSNR 稳定提升；λ ≤ 5e-5 时性能与基线一致（先验未生效）；λ ≥ 0.01 时优化不稳定。该消融确认了 λ=0.001 作为默认值的合理性。

**自适应先验类的零件数 k**：Figure 19 展示了 k 值对 PSNR 的影响。在 Mutant 和 Lego 场景上，k 在 **[5, 15]** 范围内性能稳定；当 k=1 时，先验退化为 P_I（单一全局先验），导致性能下降。这表明多零件自适应组合对复杂场景是必要的。

**熵损失权重**：Figure 20 展示了熵正则化权重对 PSNR 的影响。在 Hell Warrior 场景上，权重在 **[1e-4, 1e-3]** 范围内性能稳定。熵正则化用于防止自适应权重 w_{ij} 退化为均匀分布，消融表明该范围内的正则化强度足够且不过度。

### 训练动态与收敛分析

Figure 16 报告了 ReMatching 模型与 D3G 基线在 40K 训练迭代中的损失曲线。Figure 17 展示了 ReMatching 损失的运行平均值（窗口大小 20），显示损失稳定下降并收敛。Figure 14 的可视化比较了收敛后的速度场 u_t（白色箭头）与真实速度（绿色箭头）：使用 ReMatching 损失时，匹配后的 u_t 与真实速度对齐更紧密，绿色箭头几乎不可区分，验证了流匹配机制的有效性。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2411_00705/figures/023_Figure_16.jpg]]
*Figure 16: Loss curves report of our model and D3G (Yang et al., 2023) over 40k training iterations. Figure 17: Loss curve report for the ReMatching loss, showing a running average with a window size of 20*

### 运行时开销

Figure 15 报告了不同高斯数量 n 下的前向+反向传播平均时间。ReMatching 损失增加了训练计算开销，但推断阶段完全不受影响，因为该损失仅在训练时使用。

### 失败模式与局限性

1. **先验类设计依赖领域知识**：P_I、P_II、P_III 和 P_IV 的设计需要用户根据场景特性选择或组合，自适应组合权重的学习需要额外的熵正则化来避免退化。
2. **场景扩展性待验证**：实验主要在室内和受控场景上进行，扩展到大规模、复杂户外动态场景的效果有待进一步验证。
3. **框架适用范围限制**：ReMatching 框架仅适用于仿真自由的动态重建模型（simulation-free），无法直接用于需要数值模拟 ODE 的流程。
4. **物理现象覆盖不足**：当前的先验类（刚体、分片刚体、体积保持）对液体、气体等更复杂的物理现象支持有限。


## 定位与知识库关联

**核心定位**。ReMatching 框架并非提出一个全新的动态重建模型，而是在现有仿真自由（simulation-free）的动态重建流程之上，通过引入速度场先验类与流匹配损失来引导优化方向。其核心贡献在于将“形变先验整合”问题转化为一个流匹配问题，从而在不牺牲重建保真度的前提下，使重建解尽可能接近预定义的形变先验类。

**与基线方法的关系**。在实验验证中，ReMatching 框架被应用于两类动态高斯溅射基线之上：
- **D3G**（Yang et al., 2023）：基于时间条件变形网络的动态高斯溅射重建方法，使用 MLP 预测高斯粒子的时变偏移。ReMatching 在其基础上添加了 ReMatching 损失 $L_{\mathrm{RM}}$，总损失为 $L = L_{\mathrm{REC}} + \lambda L_{\mathrm{RM}}$（$\lambda=0.001$）。
- **GA3D**（Lu et al., 2024）：3D 几何感知可变形高斯重建方法，结合 k-planes 变形模型。ReMatching 同样以即插即用的方式部署于其上，在 D-NeRF 基准上取得了 PSNR 提升（如 Hell Warrior 场景 +0.19 dB，JumpingJacks 场景 +0.35 dB）。

这些基线方法的核心共性是：它们仅依赖图像重建损失（如 L1 损失）进行优化，形变正则化完全由网络结构的隐式偏置提供。ReMatching 的改进在于将显式的形变先验知识（如分片刚体运动、体积保持）通过速度场先验类编码，并以流匹配损失的形式注入训练过程，而不改变推断时的网络架构或计算开销。

**方法谱系中的位置**。从动态重建的方法谱系看，ReMatching 处于“先验正则化”与“仿真自由重建”的交汇点。传统上，引入形变先验往往需要数值模拟 ODE（如在 NeRF 中嵌入物理约束），这增加了计算复杂度并可能导致保真度下降。ReMatching 通过以下机制绕过了这一困境：
1. 将时间依赖重建函数 $\psi_t$ 到速度场先验类 $\mathcal{P}$ 的投影转化为匹配优化问题：$\boldsymbol{u}_t = \arg\min_{\boldsymbol{u}_t \in \mathcal{P}} \rho(\boldsymbol{u}_t, \boldsymbol{\psi}_t)$。
2. 利用连续性方程 $\frac{\partial}{\partial t} \psi_t + \mathrm{div}(\psi_t v_t) = 0$ 建立速度场与重建函数之间的约束关系。
3. 通过 Danskin 定理计算 ReMatching 损失的梯度，避免了对 $\arg\min$ 的直接微分。

这种设计使 ReMatching 能够统一处理多种模型函数类型（几何表示、图像渲染），并支持基于粒子位置和基于渲染像素两种匹配损失形式。

**适用边界**。ReMatching 框架的适用性受以下条件约束：
- **仿真自由假设**：框架要求重建模型 $\psi_t$ 的每次评估仅需单步计算，无法直接用于需要数值模拟 ODE 的流程。这排除了那些显式求解物理方程的方法。
- **先验类设计依赖领域知识**：速度场先验类的有效性取决于对场景形变特性的先验理解。论文中设计了四类先验（$\mathcal{P}_{\mathrm{I}}$ 到 $\mathcal{P}_{\mathrm{IV}}$），其中自适应分片刚体先验 $\mathcal{P}_{\mathrm{IV}}$ 通过学习权重 $w_j(\mathbf{x}, t)$ 组合多个刚体运动，但需要额外的熵正则化来避免权重退化到单一零件。
- **场景规模限制**：实验主要在室内和受控场景（D-NeRF、HyperNeRF、Dynamic Scenes）上进行，扩展到大规模、复杂户外动态场景的效果有待验证。

**局限性与开放问题**。论文明确指出的局限包括：
1. ReMatching 损失仅在训练阶段使用，增加了训练计算开销（尽管推断速度不受影响）。
2. 先验类的设计空间尚未穷尽，当前先验主要覆盖刚体、分片刚体和体积保持形变，对于液体、气体等更复杂的物理现象需要设计更丰富的先验类。
3. 框架目前处理的是非刚性形变，扩展到拓扑变化场景仍需进一步研究。

论文提出的开放问题指向了三个有前景的方向：
- **数据驱动先验**：如何从视频生成模型中导出速度场先验类，以利用大规模数据驱动先验替代手工设计的先验。
- **更丰富的物理先验**：设计能够处理流体、气体等复杂物理现象的速度场先验类。
- **通用非刚性形变**：将 ReMatching 框架扩展到更通用的非刚性形变和拓扑变化场景。

**知识库定位**。ReMatching 的核心洞察——利用速度场先验类的简化特性，将投影问题转化为流匹配问题——为动态重建中的先验整合提供了一个新的理论视角。其“模拟交替投影法”的设计思路（先投影到先验类，再重新投影回重建流集合）在方法论上具有一般性，可被后续工作借鉴用于其他需要平衡先验约束与数据保真度的重建任务。

## 原文 PDF

![[paperPDFs/ICLR_2025/ReMatching_Dynamic_Reconstruction_Flow.pdf]]
