---
title: "NeuROK: Generative 4D Neural Object Kinematics"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/NeuROK_Generative_4D_Neural_Object_Kinematics.pdf
project_link: "https://chen-geng.com/neurok"
code_link: null
aliases:
- NNOK
- NeuROK
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 数据驱动的神经对象运动学参数化（NEUROK）——通过条件VAE从4D几何轨迹学习到的低维潜在空间，作为物理系统的广义坐标。
primary_logic: 将对象变形空间建模为条件VAE学习到的低维流形，并将其作为拉格朗日力学中的广义坐标，从而在无需物理注释或类别先验的情况下，生成物理合理的4D动态。
claims:
- 学习一个潜在空间和变形解码器，可将任意采样的潜在向量解码为合理的对象变形。
- 方法仅需4D几何轨迹作为监督，无需物理参数或动作标注。
- 将学习到的NEUROK用作广义坐标，通过定义拉格朗日量并求解欧拉-拉格朗日方程来模拟动态。
- "在PartNet-Mobility逆运动学重建和4D生成用户研究中，NEUROK显著超越现有基线（Chamfer L1: 0.028 vs 0.067; 用户偏好 Alignment: 81.43% vs <6.67%）。"
---

# NeuROK: Generative 4D Neural Object Kinematics

> [!tip] 核心洞察
> 将对象变形空间建模为条件VAE学习到的低维流形，并将其作为拉格朗日力学中的广义坐标，从而在无需物理注释或类别先验的情况下，生成物理合理的4D动态。

| 字段 | 内容 |
|------|------|
| 中文题名 | NEUROK：生成式4D神经对象运动学 |
| 英文题名 | NeuROK: Generative 4D Neural Object Kinematics |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Geng_NeuROK_Generative_4D_Neural_Object_Kinematics_CVPR_2026_paper.html) · [Project](https://chen-geng.com/neurok) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | NEUROK (Neural Object Kinematics) |
| Dataset | PartNet-Mobility, 4D Generation, VBench |

> [!tip] 效果简介
> - PartNet-Mobility 上，Chamfer L1 ↓ 0.028 vs 0.067 (KeyPointDeformer) (-0.039)；IoU ↑ 0.764 vs 0.570 (KeyPointDeformer) (+0.194)。
> - 4D Generation (User Study) 上，Alignment ↑ (%) 81.43 vs 5.95 (PhysDreamer) (+75.48)；Realism ↑ (%) 83.33 vs 6.67 (AnimateAnyMesh) (+76.66)。
> - VBench 上，Aesthetic Quality (AQ) ↑ 0.483 vs 0.450 (AnimateAnyMesh) (+0.033)。

## 概要

**问题瓶颈**：现有4D动态生成方法普遍依赖特定类别的物理模型与系统辨识，缺乏一种通用的、可学习的运动学状态参数化，严重制约了跨类别泛化与可扩展性。

**核心方法**：本文提出**NEUROK（Neural Object Kinematics）**——一种数据驱动的神经对象运动学参数化。其核心思想是将对象的变形空间建模为一个条件变分自编码器（cVAE）学习到的低维潜在流形，并将该流形作为拉格朗日力学中的广义坐标。该框架仅需4D几何轨迹作为监督，无需任何物理参数或动作标注，依赖的唯一归纳偏置是“对象的变形空间是低维的”，使其能够广泛适用于弹性体、布料、连续体及多体对象等多种动态对象类型。

**关键结论**：在PartNet-Mobility数据集上，NEUROK在逆运动学重建任务中以Chamfer L1 0.028（对比最优基线KeyPointDeformer的0.067）和IoU 0.764（对比0.570）显著超越现有方法。在4D生成用户研究中，NEUROK在Alignment（81.43%）和Realism（83.33%）指标上均以压倒性优势领先所有基线（最高基线分别仅5.95%和6.67%）。此外，该方法在能量守恒分析和未见类别泛化实验中均展现出优异的物理一致性与通用性。

### 问题背景：静态3D资产的4D动态生成

随着3D内容创作的蓬勃发展，大规模静态3D资产库日益丰富，但赋予这些静态对象物理合理的动态行为——即生成“4D内容”——仍然是一项极具挑战的任务。4D生成的核心在于，给定一个静态的3D形状以及物理条件（如外力、动作指令、初始速度），生成该对象在时间维度上演化的连续动态轨迹。这一能力对于具身智能仿真、数字孪生、影视特效和交互式内容创作等领域具有重要价值。

从形式化角度看，4D动态生成可以被理解为两个子问题的耦合：**运动学参数化**（kinematic state parameterization）与**物理动力学模拟**。运动学参数化定义了对象的配置空间——即一组能够完备描述对象几何形态的状态向量；动力学模拟则在这些状态向量上演化出符合物理规律的轨迹。

### 现有方法的瓶颈

当前主流的4D生成方法存在一个根本性瓶颈：**缺乏通用的、可学习的运动学状态参数化**。具体而言，现有方法可大致分为两类，各自面临难以逾越的局限：

**基于物理模型的方法**（如PhysDreamer、OmniPhysGS）依赖特定类别的物理先验与系统辨识。例如，对于铰接体对象，需要预先定义关节类型、关节轴和运动链；对于弹性体，需要估计材料参数（杨氏模量、泊松比等）并选择合适的本构模型。这类方法的问题在于：
- **类别局限性**：每种物理模型仅适用于特定类型的动态对象（刚体、弹性体、布料、流体等），无法跨类别泛化；
- **标注依赖性**：系统辨识需要物理参数或动作标注，而这些标注在大规模数据上获取成本极高；
- **可扩展性差**：每遇到新类别，需要重新设计物理模型和辨识流程。

**基于几何插值的方法**（如AnimateAnyMesh、Pixie）通过在观察到的变形轨迹之间进行插值或外推来生成动态。这类方法虽然避免了显式物理建模，但：
- **缺乏物理合理性**：生成的轨迹可能违反能量守恒、动量守恒等基本物理定律；
- **状态空间冗余**：直接在高维几何空间（如顶点位移场）中操作，未能利用变形空间的低维结构。

### 核心洞察与动机

本文的核心洞察源于对经典力学与现代深度学习的交叉思考。在拉格朗日力学框架中，一个物理系统的动力学完全由其**广义坐标**（generalized coordinates）上的拉格朗日量（动能减势能）决定，而广义坐标的选择具有高度灵活性——任何一组能够完备描述系统构型的独立参数均可作为广义坐标。

这一观察引出了一个关键问题：**能否从数据中学习到一组广义坐标，使其既具备紧凑的表达能力，又能支撑物理合理的动力学模拟？**

具体而言，本文的动机建立在以下推理链之上：

1. **变形空间的低维性**：尽管3D对象的几何变形在顶点空间中表现为高维（数万维），但物理上合理的变形通常位于一个低维流形上。这一观察构成了方法的最小归纳偏置。

2. **从轨迹中学习参数化**：如果拥有大规模4D几何轨迹数据（即对象在不同时刻的3D形状序列），就可以通过生成式模型学习到该低维流形的参数化——一个潜在空间及其到几何空间的解码映射。

3. **潜在空间作为广义坐标**：学习到的低维潜在空间自然地充当了物理系统的广义坐标。在此空间中定义动能和势能函数，即可通过求解欧拉-拉格朗日方程推导出物理合理的动态轨迹。

4. **类别无关的普适框架**：由于整个流程不依赖任何特定类别的物理先验或参数标注，该框架在理论上可适用于任意类型的动态对象——从弹性体、布料、连续体到多体系统。

### 本文方案定位

基于上述动机，本文提出**NEUROK（Neural Object Kinematics）**——一种数据驱动的神经对象运动学参数化框架。其核心设计原则是：

- **仅需4D几何轨迹作为监督**，无需物理参数或动作标注；
- **最小归纳偏置**：仅假设对象的变形空间是低维的；
- **物理合理性内置**：通过潜在空间上的拉格朗日力学求解，天然保证能量守恒等物理约束；
- **跨类别泛化**：统一的框架可处理铰接体、弹性体、布料等多种动态对象类型。

如图2所示，NEUROK在符号化参数化（简洁但不可从逆问题中获取）和几何参数化（可获取但冗余）之间建立了一座桥梁——通过学习得到的神经参数化，同时实现了紧凑性和可获取性。

## 核心方法与创新机理

NEUROK 的核心创新在于将对象运动学状态参数化从传统的**几何派生**或**符号定义**范式，转变为一种**数据驱动的、可学习的神经潜在空间**，并以此作为拉格朗日力学中的广义坐标，从而构建了一个无需物理注释、类别先验极少的通用4D动态生成框架。这一转变体现在以下四个关键环节。

### 1. 运动学状态参数化：从几何派生到神经潜在空间

现有方法通常依赖密集粒子集或预定义的符号参数（如关节角度）来描述对象的运动学状态。这些参数化方式要么维度冗余、缺乏语义紧凑性，要么需要针对特定类别进行人工设计，难以跨类别泛化。NEUROK 提出了一个根本性的替代方案：**将对象的变形空间建模为由条件变分自编码器（cVAE）学习到的低维潜在流形**。

具体而言，给定一个静态3D网格 $\mathcal{M}_0$，NEUROK 学习一个实例特定的潜在空间 $\mathcal{Z}(\mathcal{M}_0)$ 和一个解码器 $\mathcal{F}$，使得该空间中的任意采样潜在向量 $\mathbf{z}$ 都能被解码为该对象的一个合理变形状态。这种参数化被形式化地定义为一个二元组 $(\mathcal{Z}, \mathcal{F})$，其中解码器 $\mathcal{F}$ 的像集恰好构成对象的位形流形。与传统的符号参数化相比，NEUROK 的潜在空间是**从大规模4D几何轨迹数据中自动涌现**的，无需人工指定关节类型或运动链结构。

### 2. 物理模拟：从特定类别物理模型到潜在空间上的拉格朗日力学

传统4D生成方法通常需要为每一类对象构建专门的物理模型并进行系统辨识（如估计质量、刚度、阻尼等参数），这严重限制了可扩展性。NEUROK 的核心洞察在于：一旦获得了紧凑的神经潜在空间，就可以将其中的潜在向量 $\mathbf{z}$ 视为物理系统的**广义坐标**，进而在该潜在空间上直接运用拉格朗日力学框架。

论文在潜在空间上定义了系统的拉格朗日量 $L = T - V$（动能减势能），并通过求解欧拉-拉格朗日方程来推导运动轨迹：

$${ \frac { \mathrm { d } } { \mathrm { d } t } } { \frac { \partial L } { \partial { \dot { \mathbf { z } } } } } = { \frac { \partial L } { \partial \mathbf { z } } }$$

在实际实现中，这被展开为包含质量矩阵 $\mathbf{G}(\mathbf{z})$、科里奥利项 $\mathbf{C}(\mathbf{z}, \dot{\mathbf{z}})$ 和势能梯度 $\nabla_{\mathbf{z}} V$ 的运动方程：

$$m \mathbf{G}(\mathbf{z}) \ddot{\mathbf{z}} + \mathbf{C}(\mathbf{z}, \dot{\mathbf{z}}) + \nabla_{\mathbf{z}} V = 0$$

这一设计的精妙之处在于：**物理模拟的动力学方程是类别无关的**——无论对象是弹性体、布料、连续体还是多体铰接结构，只要其变形空间被 NEUROK 成功建模，就可以用同一套拉格朗日求解器生成物理合理的动态轨迹。能量守恒分析（Figure 8）证实，通过欧拉-拉格朗日动力学生成的轨迹总能量保持近似恒定，而简单插值则无法维持物理一致性。

### 3. 训练监督：从物理标注依赖到纯几何轨迹自监督

传统物理模拟方法需要显式的物理参数（质量、弹性模量等）或动作标注（力、力矩序列）作为监督信号。NEUROK 的训练**仅需4D几何轨迹**——即对象在不同时刻的3D形状序列。cVAE 的训练目标仅包含重建误差和 KL 散度：

$$\mathcal{L} = ||\delta_{\mathrm{sample}} - \delta_{\mathrm{pred}}||_2^2 + \lambda D_{KL}(q_{\mathcal{M}_0}(\mathbf{z} \mid \phi) || p_{\mathcal{M}_0}(\mathbf{z}))$$

其中 $\lambda$ 设为 0.01。这种自监督特性意味着 NEUROK 可以直接利用大规模4D形状数据集进行训练，而无需任何物理测量或人工标注，极大降低了数据获取成本并提升了可扩展性。

### 4. 归纳偏置：从强类别先验到最小假设

与依赖特定类别运动学先验（如铰接模型的关节树结构）的基线方法不同，NEUROK 仅依赖一个**极简的归纳偏置**：对象的变形空间是低维的。这一假设广泛适用于从弹性体到多体系统的各类动态对象，使得框架具备天然的跨类别泛化能力——实验表明，NEUROK 能够泛化到训练数据中完全未见过的对象类别（Figure 9）。

### 创新总结

| 设计维度 | 基线方法 | NEUROK |
|---------|---------|--------|
| 运动学状态参数化 | 几何派生（密集粒子集） | 学习到的神经潜在空间（cVAE） |
| 物理模拟 | 特定类别的物理模型与系统辨识 | 潜在空间上的拉格朗日力学，求解欧拉-拉格朗日方程 |
| 训练监督 | 需要物理参数或动作标注 | 仅需4D几何轨迹（自监督） |
| 归纳偏置 | 强类别先验 | 变形空间低维（最小假设） |

这四项创新相互耦合、层层递进：神经潜在空间提供了紧凑且可学习的广义坐标；拉格朗日力学在此坐标上实现了类别无关的物理模拟；自监督训练使得大规模学习成为可能；最小归纳偏置则保障了跨类别泛化。三者共同构成了一个**从数据中自动发现运动学结构、在潜在空间中模拟物理动态**的通用框架。

NEUROK 的整体框架围绕一个核心抽象展开：**将对象运动学状态参数化建模为从数据中学习到的低维潜在流形**。这一抽象将传统的几何派生或符号化状态表示替换为可学习的神经参数化，使得框架能够以最小的归纳偏置（仅假设对象变形空间是低维的）统一处理弹性体、布料、连续体和多体对象等多种动态类型。

### 框架总览

给定一个静态三维网格 $\mathcal{M}_0$，整个 pipeline 分为两大阶段（图3）：

**阶段一：运动学状态空间的生成式学习。** 一个基于 Transformer 的条件编码器 $E_{\text{cond}}$ 将输入网格编码为实例特定的潜在先验分布 $p_{\mathcal{M}_0}(\mathbf{z})$，该分布定义在 $k$ 维潜在空间 $\mathcal{Z}$ 上。该潜在空间中的每一个采样点 $\mathbf{z}$ 都对应对象的一个可能变形状态。变形解码器 $\mathcal{F}$（即 $\mathcal{D}$）将任意采样潜在向量映射回三维空间，生成对应的变形后网格。这一阶段的核心成果是获得了一个紧凑的运动学状态参数化 $(\mathcal{Z}, \mathcal{F})$——即 **NEUROK**。

**阶段二：潜在空间上的物理驱动动态生成。** 在获得 NEUROK 参数化后，框架在潜在空间中定义拉格朗日量 $L = T - V$（动能减势能），并通过求解欧拉-拉格朗日方程来生成动态轨迹。不同物理条件（力、动作、初速度等）通过边界条件优化的方式注入系统：优化初始潜在状态 $\mathbf{z}_0$ 和初始潜在速度 $\dot{\mathbf{z}}_0$，使其解码后的位置和速度与给定的物理条件匹配。

### 关键模块与数据流

框架由六个核心模块组成，数据流贯穿训练与推理两个阶段：

| 模块 | 角色 | 数据流位置 |
|------|------|-----------|
| **形状编码器** $E_{\text{cond}}$ | 将静态网格编码为潜在先验分布参数 | 训练与推理均使用 |
| **变分变形编码器** $E_{\text{VAE}}$ | 将变形场编码为后验分布 | 仅训练阶段 |
| **变形解码器** $\mathcal{D}$ | 从潜在向量解码为变形网格 | 训练与推理均使用 |
| **主动子空间降维** | 压缩高维潜在空间，移除冗余自由度 | 训练后处理 |
| **拉格朗日动力学求解器** | 在潜在空间中求解运动方程 | 推理阶段 |
| **边界条件优化** | 将物理条件映射为初始潜在状态 | 推理阶段 |

**训练阶段**（图4）：从大规模4D数据集中随机采样实例网格及其一个变形场 $\phi$。形状编码器 $E_{\text{cond}}$ 输出先验分布 $p_{\mathcal{M}_0}(\mathbf{z})$，变分变形编码器 $E_{\text{VAE}}$ 输出后验分布 $q_{\mathcal{M}_0}(\mathbf{z}|\phi)$。从后验中采样 $\mathbf{z}$，经解码器 $\mathcal{D}$ 重建变形场。训练目标为条件 VAE 的标准损失：

$$\mathcal{L} = \|\delta_{\text{sample}} - \delta_{\text{pred}}\|_2^2 + \lambda D_{KL}\big(q_{\mathcal{M}_0}(\mathbf{z}|\phi) \| p_{\mathcal{M}_0}(\mathbf{z})\big)$$

其中 $\lambda = 0.01$，$\delta$ 表示顶点位移。该损失同时约束重建精度和潜在空间的规整性。

**推理阶段**：仅使用 $E_{\text{cond}}$ 获取先验分布，从中采样或通过边界条件优化确定初始潜在状态，随后在潜在空间中求解运动方程：

$$m G(\mathbf{z}) \ddot{\mathbf{z}} + C(\mathbf{z}, \dot{\mathbf{z}}) + \nabla_{\mathbf{z}} V = 0$$

其中 $G$ 为质量矩阵，$C$ 为科里奥利项，$V$ 为势能。求解得到的潜在轨迹 $\mathbf{z}(t)$ 通过解码器 $\mathcal{F}$ 逐帧映射回三维网格序列，生成最终的4D动态。

### 核心设计决策

框架的关键设计在于**将物理模拟从显式的三维几何空间迁移到学习到的潜在空间**。这一迁移带来三个优势：(1) 潜在空间的低维性天然抑制了非物理的高频抖动；(2) 拉格朗日力学在广义坐标上的通用性使得框架无需针对不同对象类别设计不同的物理模型；(3) 整个 pipeline 的训练仅需4D几何轨迹作为监督信号，完全消除了对物理参数标注或动作标注的依赖。

### 补充图表

![[assets/figures/papers/paper_list_l969_https_openaccess_thecvf_com_content_CVPR2026_html_Geng_NeuROK_Generative/figures/002_Figure_2.jpg]]
*Figure 2: Kinematic state parameterization. (a) Several kinematic state parameterizations can be used to describe a physical system. The symbolic parameterizations used in classical mechanics are concise yet not accessible in inverse problems. Traditional inverse simulation approaches use geometry-derived parameterizations, yet require dense physical constraints to solve the over-parameterized system. We instead learn low-dimensional parameterizations that are both compact and learnable from data. (b) As formally defined in Def. 1, a kinematic state parameterization studied in this paper is a pair (Z, F) which contains a latent manifold Z and a decoder*

### 3.1 运动学状态参数化的形式化定义

NEUROK 的核心是将对象变形空间建模为一个可学习的低维流形。形式化地，一个运动学状态参数化定义为一个二元组 $(\mathcal{Z}, \mathcal{F})$，其中 $\mathcal{Z} \subseteq \mathbb{R}^k$ 是 $k$ 维潜在状态空间，$\mathcal{F}: \mathcal{Z} \rightarrow \mathbb{R}^{3N}$ 将任意潜在向量映射到对象的顶点配置。与经典力学中依赖符号化广义坐标（如关节角度）不同，NEUROK 的 $\mathcal{F}$ 是一个神经网络，其值域恰好覆盖对象的配置流形，从而无需类别特定的物理先验。

### 3.2 生成式学习架构

NEUROK 通过条件变分自编码器（CVAE）从4D几何轨迹中学习实例特定的潜在空间。整个架构包含三个核心模块，如 Figure 4 所示：

![[assets/figures/papers/paper_list_l969_https_openaccess_thecvf_com_content_CVPR2026_html_Geng_NeuROK_Generative/figures/004_Figure_4.jpg]]
*Figure 4: Generative learning of NEUROK. During training, we randomly sample an instance mesh and one of its possible deformation fields from the training set, and supervise all three models with KL and reconstruction targets. During inference, we only use*

**运动学先验编码器 $E_{\text{cond}}(\mathcal{M}_0)$**：以静态网格 $\mathcal{M}_0$ 为条件输入，输出该实例潜在空间上的先验分布参数 $p_{\mathcal{M}_0}(\mathbf{z})$。该模块采用 Transformer 架构，将输入网格编码为实例特定的潜在空间表征。

**变分变形编码器 $E_{\text{VAE}}(\phi, \mathcal{M}_0)$**：以变形场 $\phi$ 和条件网格 $\mathcal{M}_0$ 为输入，输出后验分布 $q_{\mathcal{M}_0}(\mathbf{z} \mid \phi)$ 的参数。该模块在训练时使用，用于将观测到的变形场映射到潜在空间。

**变形解码器 $\mathcal{D}(\mathbf{z}, \mathcal{M}_0)$**：从先验分布中采样潜在向量 $\mathbf{z}$，并将其解码为变形后的网格 $\mathcal{M}_{\mathbf{z}}$。解码器使用双四元数（dual-quaternion）参数化变形场，以保证变形后的网格保持局部刚性。

训练时，模型从数据集中随机采样实例网格及其一个可能的变形场，通过以下条件 VAE 目标进行监督：

$$\mathcal{L} = \|\delta_{\text{sample}} - \delta_{\text{pred}}\|_2^2 + \lambda D_{KL}\big(q_{\mathcal{M}_0}(\mathbf{z} \mid \phi) \,\|\, p_{\mathcal{M}_0}(\mathbf{z})\big)$$

其中 $\delta_{\text{sample}}$ 和 $\delta_{\text{pred}}$ 分别为真实和预测的顶点位移，$\lambda = 0.01$ 平衡重建精度与潜在空间正则化。推理时仅使用 $E_{\text{cond}}$ 获得先验分布，采样后经 $\mathcal{D}$ 解码。

### 3.3 主动子空间降维

为移除潜在空间中的冗余维度，NEUROK 引入主动子空间方法（Active Subspace Method）进行降维。该模块通过考虑一个代理函数 $f: \mathcal{Z} \rightarrow \mathbb{R}$（此处取为解码器输出的顶点位置方差），计算其梯度外积矩阵的特征分解，保留主导特征值对应的方向，从而将高维潜在空间 $\mathcal{Z}$ 压缩到更紧凑的子空间。消融实验（Table 1）表明，移除该降维模块会导致 Chamfer L1 和 IoU 指标显著下降。

### 3.4 拉格朗日动力学求解

NEUROK 将学习到的潜在空间作为物理系统的广义坐标，通过拉格朗日力学框架生成物理合理的动态轨迹。系统的拉格朗日量定义为动能与势能之差 $L = T - V$，其中：

- 动能 $T = \frac{1}{2} m \dot{\mathbf{z}}^\top G(\mathbf{z}) \dot{\mathbf{z}}$，$G(\mathbf{z}) = J_{\mathbf{z}}^\top J_{\mathbf{z}}$ 为质量矩阵，$J_{\mathbf{z}}$ 是解码器 $\mathcal{F}$ 在 $\mathbf{z}$ 处的雅可比矩阵；
- 势能 $V(\mathbf{z})$ 由重力势能和弹性势能组成，弹性势能通过网格边长变化量计算。

将 $L$ 代入欧拉-拉格朗日方程：

$$\frac{\mathrm{d}}{\mathrm{d}t}\frac{\partial L}{\partial \dot{\mathbf{z}}} = \frac{\partial L}{\partial \mathbf{z}}$$

推导得到 NEUROK 潜在空间中的运动方程：

$$m\, G(\mathbf{z}) \ddot{\mathbf{z}} + C(\mathbf{z}, \dot{\mathbf{z}}) + \nabla_{\mathbf{z}} V = 0$$

其中 $C(\mathbf{z}, \dot{\mathbf{z}})$ 为科里奥利项（包含质量矩阵对时间的导数），$\nabla_{\mathbf{z}} V$ 为势能梯度。该常微分方程（ODE）可通过标准数值积分器求解，生成潜在轨迹 $\mathbf{z}(t)$，再经解码器 $\mathcal{F}$ 映射为网格动画序列。Figure 8 的能量守恒分析验证了该动力学建模能保持系统总能量近似恒定，而纯插值方法则无法维持物理一致性。

### 3.5 边界条件优化

为匹配用户指定的初始条件（如位置 $\mathbf{x}_0$ 和速度 $\dot{\mathbf{x}}_0$），NEUROK 通过优化初始潜在状态 $\mathbf{z}_0$ 和潜在速度 $\dot{\mathbf{z}}_0$ 来满足边界条件：

$$\min_{\mathbf{z}_0, \dot{\mathbf{z}}_0} \|\mathbf{x}_0 - \mathcal{F}(\mathbf{z}_0)\|_2^2 + \|\dot{\mathbf{x}}_0 - J_{\mathbf{z}} \dot{\mathbf{z}}_0\|_2^2$$

第一项确保解码位置与目标位置一致，第二项通过雅可比矩阵 $J_{\mathbf{z}}$ 将潜在速度映射到顶点速度空间，保证运动方向匹配。优化完成后，以 $(\mathbf{z}_0, \dot{\mathbf{z}}_0)$ 为初值求解前述运动方程，即可生成满足边界条件的物理合理动态轨迹。

## 实验与关键发现

本节从逆运动学重建与物理启发的4D生成两个维度验证NEUROK的有效性，并结合消融实验与能量守恒分析揭示各设计选择的贡献与方法的物理合理性。

### 逆运动学重建

逆运动学任务要求模型在给定目标姿态形状的条件下，找到最佳匹配的运动学状态向量，并评估解码重建形状与目标的匹配程度。该任务直接衡量运动学状态参数化的紧凑性与平滑性。

**定量结果**（Table 1）：在PartNet-Mobility基准上，NEUROK在Chamfer L1和IoU两项指标上均显著超越所有基线方法。与最强的几何派生参数化方法**KeyPointDeformer**（KPD）相比，NEUROK将Chamfer L1从0.067降至**0.028**（降低58.2%），IoU从0.570提升至**0.764**（提升34.0%）。其他基线如**NeuralDeformationGraphs**（NDG）、**SINGAPO**、**FreeArt3D**和**CANOR**的表现均远低于NEUROK。这一结果验证了核心洞见：从4D数据中学习到的低维潜在空间能够比手工设计的几何参数化更紧凑地捕捉对象的变形流形。

**定性结果**（Figure 5）：NEUROK重建的形状与目标姿态高度吻合，尤其在铰接关节处保持了精确的几何对齐，而基线方法常出现部件穿透或姿态偏差。

### 物理启发的4D生成

4D生成任务给定单一静态形状与条件动作（如力、速度），要求生成物理合理的动态序列。该任务综合考察运动学参数化与动力学求解的协同效果。

**用户研究**（Table 2）：在成对比较中，NEUROK在“动作对齐度”（Alignment）上获得**81.43%**的偏好率，而最佳基线**PhysDreamer**仅为5.95%；在“真实感”（Realism）上获得**83.33%**的偏好率，最佳基线**AnimateAnyMesh**仅为6.67%。NEUROK在两项主观指标上均以压倒性优势胜出。

**自动指标**（Table 2）：在VBench的客观评估中，NEUROK在美学质量（AQ: 0.483）和动态程度（DD: 0.567）上优于所有基线；在WorldScore的CLIP分数上也取得最高值。值得注意的是，**OmniPhysGS**和**Pixie**等基于物理先验的方法在自动指标上表现较弱，反映出其类别特定假设在跨类别评估中的局限性。

**定性结果**（Figure 6）：NEUROK生成的动态序列展现出自然的惯性与弹性行为，而基线方法常出现不自然的抖动或物理不一致的变形。

### 消融实验

Table 1中的消融行揭示了三个关键设计的作用：

- **移除模型降维**（w/o Model Reduction）：Chamfer L1从0.028升至0.034，IoU从0.764降至0.721。这表明Active Subspace方法成功移除了潜在空间中的冗余维度，使参数化更加紧凑。
- **移除数据增强**（w/o Data Augmentation）：Chamfer L1升至0.032，IoU降至0.738。训练时的变形增强策略对模型的泛化能力有显著贡献。
- **移除双四元数参数化**（w/o Dual-Quaternion）：Chamfer L1升至0.031，IoU降至0.745。采用双四元数混合蒙皮作为变形表示比直接预测顶点位移更有利于学习平滑的变形流形。

三项消融一致表明，每个设计选择均对最终性能有不可忽略的正向贡献。

### 能量守恒分析

Figure 8对比了基于欧拉-拉格朗日方程的动力学模拟与简单潜在空间插值的能量行为。在NEUROK的拉格朗日动力学框架下，模拟运动的总能量保持近似恒定，符合无耗散物理系统的能量守恒特性。相比之下，插值方法的总能量出现明显波动，缺乏物理一致性。这一分析从物理第一性原理层面验证了将NEUROK作为广义坐标并求解Euler-Lagrange方程（公式(3)）的合理性。

### 泛化能力

Figure 9展示了NEUROK对训练集中完全未出现的新对象类别的泛化效果。模型能够为这些未见类别推断合理的潜在空间，并生成物理一致的动态序列。这验证了方法所依赖的最小归纳偏置——仅假设变形空间是低维的——使其具备跨类别的可扩展性。

### 真实物体模拟

Figure 7展示了NEUROK在真实扫描物体上的模拟效果。模型能够处理来自真实世界的几何输入，生成符合物理直觉的动态行为，表明该方法从合成4D数据中学到的运动学先验可迁移至真实场景。

### 补充图表

![[assets/figures/papers/paper_list_l969_https_openaccess_thecvf_com_content_CVPR2026_html_Geng_NeuROK_Generative/figures/008_Table_1.jpg]]
*Table 1: Quantitative comparison on inverse-kinematics optimization*

![[assets/figures/papers/paper_list_l969_https_openaccess_thecvf_com_content_CVPR2026_html_Geng_NeuROK_Generative/figures/011_Table_2.jpg]]
*Table 2: Quantitative comparison on physically-inspired generation. We report user study preferences along with metrics from VBench [36] and WorldScore [27]. AQ: Aesthetic Quality, DD: Dynamic Degrees, IQ: Imaging Quality, CLIP: CLIP score [89], MM: Motion Magnitude*

![[assets/figures/papers/paper_list_l969_https_openaccess_thecvf_com_content_CVPR2026_html_Geng_NeuROK_Generative/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison on learning object kinematics. We evaluate different methods on learning compact and smooth kinematic spaces. Given an input object and the shape of a target pose, we perform inverse kinematics and find the best-matching kinematic state. We compare how well the reconstructed shape decoded from the obtained state vectors matches the target*

![[assets/figures/papers/paper_list_l969_https_openaccess_thecvf_com_content_CVPR2026_html_Geng_NeuROK_Generative/figures/006_Figure_6.jpg]]
*Figure 6: Qualitative comparison on physically-inspired 4D generation. We compare against baselines on the task of generating physically-plausible 4D motion given a single shape and conditioning actions*

![[assets/figures/papers/paper_list_l969_https_openaccess_thecvf_com_content_CVPR2026_html_Geng_NeuROK_Generative/figures/010_Figure_8.jpg]]
*Figure 8: Analysis of energy conservation. Our approach maintains physical consistency in the generated trajectories through Euler–Lagrangian modeling. Under this formulation, the total energy of the simulated motion remains approximately constant*

![[assets/figures/papers/paper_list_l969_https_openaccess_thecvf_com_content_CVPR2026_html_Geng_NeuROK_Generative/figures/009_Figure_9.jpg]]
*Figure 9: Generalization on unseen categories. Our model can generalize to novel object categories that are completely not present in the training data*

![[assets/figures/papers/paper_list_l969_https_openaccess_thecvf_com_content_CVPR2026_html_Geng_NeuROK_Generative/figures/001_Figure_1.jpg]]
*Figure 1: We present a versatile and scalable framework for generating simulative 4D dynamics of static 3D objects under physical conditions (e.g., forces, actions, velocities). Trained on a large-scale 4D shape dataset without any explicit physical annotations, our method does not rely on any inductive bias of the object’s dynamic structure and therefore can be applied to various types of dynamic objects, ranging from elastic bodies, cloth, and continuum bodies, to multi-body objects. Project page: https://chen-geng.com/neurok*

## 定位与知识库关联

### 核心瓶颈与因果杠杆

现有4D动态生成方法面临一个根本性瓶颈：它们依赖特定类别的物理模型与系统辨识，缺乏通用的、可学习的运动学状态参数化。无论是基于符号关节参数（如铰接角度）的经典方法，还是基于密集粒子集的几何派生表示（如**NDG**、**SINGAPO**、**FreeArt3D**、**CANOR**、**KeyPointDeformer**等逆运动学基线），都预设了对象动态结构的强归纳偏置，限制了跨类别泛化与可扩展性。

NEUROK的因果杠杆在于：**将对象变形空间建模为条件VAE学习到的低维潜在流形，并将其作为拉格朗日力学中的广义坐标**。这一设计实现了两个关键突破：（1）运动学状态参数化从手工设计转向数据驱动，仅需4D几何轨迹作为监督，无需物理参数或动作标注；（2）物理模拟从特定类别的系统辨识转向潜在空间上的通用拉格朗日力学框架——定义类别无关的能量函数，直接通过Euler-Lagrange方程导出动力学。

### 方法谱系中的位置

#### 相对于逆运动学基线

传统逆运动学方法在紧凑性和平滑性上存在明显局限。**KeyPointDeformer (KPD)** 等几何派生方法将状态参数化锚定在密集粒子集或关键点上，导致状态空间高维且不平滑。NEUROK通过学习到的低维潜在空间替代几何派生表示，在PartNet-Mobility基准上取得显著提升：Chamfer L1降至0.028（KPD为0.067），IoU升至0.764（KPD为0.570）。消融实验进一步证实，模型降维（Active Subspace Method）、训练数据增强和双四元数变形参数化各自对性能有显著贡献——移除任何一项均导致指标下降。

#### 相对于4D生成基线

现有4D生成方法（如**PhysDreamer**、**OmniPhysGS**、**Pixie**、**AnimateAnyMesh**）通常将物理先验硬编码为特定类别的模拟器或能量函数。NEUROK的差异化在于：物理合理性不来自显式物理注释，而来自潜在空间上的拉格朗日动力学求解。用户研究中，NEUROK在“对齐度”（Alignment）上达到81.43%，远超PhysDreamer的5.95%；在“真实感”（Realism）上达到83.33%，远超AnimateAnyMesh的6.67%。在VBench自动指标上，美学质量（AQ）为0.483，略高于AnimateAnyMesh的0.450。能量守恒分析（Figure 8）进一步验证：Euler-Lagrangian动力学生成的轨迹总能量近似恒定，而纯插值轨迹能量波动显著，从机制层面解释了物理合理性的来源。

#### 知识库定位

NEUROK位于三个研究方向的交叉点：

1. **神经运动学表示**：继承条件VAE的生成建模范式，但将其用于学习实例特定的变形流形，而非全局形状先验。
2. **可微物理模拟**：将拉格朗日力学从显式坐标空间迁移到学习到的潜在空间，形成“神经广义坐标+解析动力学”的混合框架。
3. **4D生成**：将动态生成重新定义为潜在空间上的ODE求解问题，避免了逐帧生成的不一致性。

### 适用边界与局限

NEUROK的核心归纳偏置极简——仅假设对象变形空间是低维的——这使其理论上适用于弹性体、布料、连续体和多体对象等多种动态类型（Figure 1）。Figure 9展示了其对训练数据中完全未出现的新类别的泛化能力，证实了类别无关设计的有效性。

然而，需要注意以下边界条件：

- **训练数据依赖性**：方法需要大规模4D几何轨迹数据集进行训练。虽然无需物理注释降低了数据获取门槛，但4D数据的采集和整理本身仍具挑战性。
- **潜在空间质量**：动力学求解的物理合理性依赖于学习到的潜在流形的平滑性和覆盖度。若训练数据未充分覆盖某些变形模式，对应的动力学轨迹可能失真。
- **能量函数设计**：当前框架中的拉格朗日量（质量矩阵 $G(\mathbf{z})$、势能 $V$）需要针对潜在空间进行定义。论文未详细讨论这些函数的参数化方式及其对不同对象类型的泛化能力，这一点需要进一步验证。

### 开放问题

1. **潜在空间的可解释性**：学习到的潜在维度是否对应物理上有意义的运动模式（如弯曲、扭转）？能否通过解耦学习增强可控性？
2. **与物理参数的显式连接**：当前方法将物理参数隐式编码在能量函数中。是否存在路径从潜在动力学中恢复材料属性（如刚度、阻尼），以支持更精确的物理推理？
3. **长时程稳定性**：Euler-Lagrangian ODE的数值求解在长时程模拟中是否保持稳定？Figure 8的能量守恒分析仅展示了短时程行为，长时程漂移特性尚不明确。
4. **多对象交互**：当前框架面向单对象动态。扩展到多对象接触与碰撞场景时，潜在空间上的拉格朗日力学如何融入接触约束？

## 原文 PDF

![[paperPDFs/CVPR_2026/NeuROK_Generative_4D_Neural_Object_Kinematics.pdf]]
