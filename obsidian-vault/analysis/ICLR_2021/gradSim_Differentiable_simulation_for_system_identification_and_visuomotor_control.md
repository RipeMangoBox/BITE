---
title: "gradSim: Differentiable simulation for system identification and visuomotor control"
type: paper
paper_level: A
venue: ICLR
year: 2021
pdf_ref: paperPDFs/ICLR_2021/gradSim_Differentiable_simulation_for_system_identification_and_visuomotor_control.pdf
aliases:
- gradSim
tags:
- ICLR_2021
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "将可微物理引擎与可微渲染引擎耦合，使从图像像素到物理属性的端到端梯度反传成为可能，从而仅需图像空间监督即可进行优化。"
primary_logic: "通过构建一个覆盖从场景动力学到图像形成的统一可微计算图，可以将原本不适定的逆问题转化为可梯度下降的优化问题，实现从视频中精确推断质量、摩擦、弹性等物理属性，甚至完成视觉运动控制任务。"
claims:
- "∇Sim 通过耦合可微场景动力学与可微渲染，实现了从视频像素到物理属性的反向传播。"
- "在质量估计任务中，∇Sim 仅使用图像监督即可达到与需要三维监督的 DiffPhysics 相近的精度。"
- "∇Sim 的损失景观平滑且具有唯一最小值，而基于 REINFORCE 的非可微仿真器存在多个局部极小值。"
- "∇Sim 可以仅使用目标图像（无三维监督）完成可变形体和布料的视觉运动控制任务，而 DiffPhysics 依赖密集的三维状态奖励。"
---

# gradSim: Differentiable simulation for system identification and visuomotor control

> [!tip] 核心洞察
> 通过构建一个覆盖从场景动力学到图像形成的统一可微计算图，可以将原本不适定的逆问题转化为可梯度下降的优化问题，实现从视频中精确推断质量、摩擦、弹性等物理属性，甚至完成视觉运动控制任务。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | gradSim：用于系统识别与视觉运动控制的可微仿真 |
| 英文题名 | gradSim: Differentiable simulation for system identification and visuomotor control |
| 会议/期刊 | ICLR 2021 |
| Links | [paper](https://arxiv.org/abs/2104.02646); [Project](https://gradsim.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | ∇Sim |
| Dataset | Rigid-body mass estimation (custom dataset of 14 objects), Rigid-body contact parameter estimation, Deformable solid FEM parameter estimation, Visuomotor control (control-cloth) |

> [!tip] 效果简介
> - Rigid-body mass estimation (custom dataset of 14 objects) 上，Absolute relative error 为 9.01e-5 (∇Sim)，对比 0.0094 (ConvLSTM)，变化 ∇Sim 远优于 ConvLSTM（~104 倍），且仅需图像监督，无需三维标签。。
> - Rigid-body contact parameter estimation 上，Absolute relative error (friction μ) 为 0.0073 (∇Sim)，对比 0.0107 (DiffPhysics, 3D sup.)，变化 ∇Sim 略优于需要三维监督的 DiffPhysics，且完全从视频推断。。
> - Deformable solid FEM parameter estimation 上，Relative MAE (per-particle mass) 为 0.048 (∇Sim)，对比 0.032 (DiffPhysics, 3D sup.)，变化 ∇Sim 接近需要三维监督的 DiffPhysics，差距合理，优势在于无需状态标签。。

## 概述

从视频观测中推断物理世界的内在属性——如物体的质量、摩擦系数、弹性参数——是计算机视觉与机器人学中的一个基本难题。传统方法通常依赖于精确的三维状态监督（如每个时间步的位置与速度真值），然而对于可变形体、布料等系统，获取此类密集的三维标签成本极高甚至不可行。∇Sim 的核心突破在于：**将可微物理引擎与可微渲染引擎耦合为一个统一的端到端计算图**，使得从图像像素到物理属性的梯度反向传播成为可能，从而彻底消除了对三维监督的依赖。

这一设计将原本不适定的逆问题转化为一个可通过梯度下降直接优化的过程：从视频观测出发，通过可微多物理仿真（刚体、有限元可变形体、布料）生成三维状态序列，再经由可微光栅化渲染为二维图像帧，最终以像素级均方误差作为损失信号反向传播，同步更新物理参数甚至控制策略。∇Sim 在刚体质量估计、接触参数推断、可变形体弹性参数辨识以及视觉运动控制等任务上均表现出色：在质量估计中，其仅使用图像监督即可达到与需要三维监督的 **DiffPhysics** 相近的精度（绝对相对误差 9.01e-5）；在布料控制任务中，它仅凭单张目标图像即可成功收敛，而依赖质心三维状态奖励的基线方法则因歧义而陷入次优解。损失景观分析进一步表明，∇Sim 的优化曲面平滑且具有唯一最小值，而基于 REINFORCE 梯度估计的非可微仿真器则存在多个局部极小值，对超参数高度敏感。

∇Sim 的方法论定位清晰：它属于**白箱动力学辨识**路线，但与以往工作不同，它将监督信号从状态空间迁移到了图像空间。这一转变的关键在于可微渲染模块的引入，使得梯度能够穿越从物理仿真到图像形成的完整链路。消融实验揭示了一个重要洞见：动力学建模误差（如未建模摩擦或弹性）对参数估计精度的影响远大于渲染建模误差（如使用光真实渲染替代简单着色），这为后续工作的模型选择提供了明确的优先级指引。

## 背景与动机

### 物理推理的核心瓶颈：三维监督的诅咒

从视频中理解物理世界——推断物体的质量、摩擦系数、弹性模量等内在属性——是计算机视觉与机器人学的长期目标。这类任务本质上是一个逆问题：给定观测到的像素序列，反推生成这些观测的物理参数。传统上，白箱动力学方法（white-box dynamics）通过显式物理引擎建模场景演化，并利用梯度信息优化参数。然而，这些方法面临一个根本性瓶颈：**它们要求在每个时间步提供精确的三维状态标签（位置、速度等）作为监督信号**。

这一依赖在理论上是自然的——物理引擎运算于三维状态空间，损失函数自然定义在状态空间上。但在实践中，它构成了严峻的障碍。对于可变形体、布料、颗粒介质等系统，获取密集的三维真实状态极为困难且成本高昂。即便对于刚体，精确的三维轨迹标注也需要动作捕捉系统或精心校准的多视角设置。这种对三维监督的刚性需求，将白箱物理推理的适用范围严重限制在了受控实验室环境内。

### 现有方法的缺口

围绕这一瓶颈，研究界形成了两条主要的技术路线，各有其根本性局限：

**白箱方法（仅可微物理引擎）**：以 **DiffPhysics** 为代表的工作将物理引擎实现为可微操作，允许通过仿真步骤反向传播梯度。这使得从三维状态标签到物理参数的端到端优化成为可能。然而，如前所述，这类方法完全依赖三维监督，无法直接从图像像素中学习。当目标系统是布料等质心在体外且缺乏刚性参考点的对象时，即使提供了三维监督，状态空间中的歧义也会导致优化陷入次优解（见 Table 3 中 DiffPhysics 在布料任务上的性能下降）。

**黑箱方法（学习型预测器）**：以 **ConvLSTM**（Xu et al., 2019b）为代表的基于学习的方法直接从视频中预测物理参数，绕过了显式物理建模。这类方法虽然无需三维标签，但缺乏对物理规律的归纳偏置，导致泛化能力差、数据效率低。在刚体质量估计任务中，ConvLSTM 的绝对相对误差为 0.0094，远逊于白箱方法。

**梯度估计方法**：另一条路径是通过 **REINFORCE** 等黑箱梯度估计器使非可微仿真器（如 **PyBullet**）变得“可优化”（Ehsani et al., 2020）。然而，这类方法的损失景观充满局部极小值，对超参数极为敏感，优化过程不稳定，实用性大打折扣。

### 核心洞察：统一可微计算图

本文的核心洞察在于：**将视觉观测到物理属性的逆问题，转化为一个统一可微计算图上的梯度下降问题**。具体而言，如果将场景动力学的演化（物理引擎）与图像的形成过程（渲染引擎）耦合为一个端到端的可微管道，那么就可以定义图像空间中的损失函数（如像素级均方误差），并将梯度从像素反向传播到物理参数。

这一思路的关键在于认识到：物理引擎和渲染引擎本质上都是确定性函数——前者将参数和初始状态映射到三维状态序列，后者将三维状态映射到二维图像。如果两者都是可微的，那么整个映射就是可微的。此时，原本不适定的逆问题（从二维像素推断三维物理属性）就变成了一个可以通过梯度下降求解的优化问题。

### 技术挑战与本文贡献

实现这一愿景面临多重挑战：物理引擎需要支持刚体、可变形体（有限元法）、布料等多种动力学模型，且每种模型的数值积分方案必须保持可微性；渲染引擎需要在光栅化过程中实现平滑梯度流，避免传统光栅化中离散边界导致的零梯度问题；整个计算图的内存和计算开销必须可控，以保证实用价值。

**∇Sim** 通过以下方式应对这些挑战：

1. **可微多物理引擎**：基于隐式时间积分和伴随方法（adjoint method），将任意离散积分格式抽象为隐式关系 $\mathbf{g}(\mathbf{s}^-, \mathbf{s}^+, \boldsymbol{\theta}) = \mathbf{0}$，并通过隐函数定理高效计算梯度。支持刚体、Neo-Hookean 超弹性体（FEM）、布料等多种物理模型。

2. **可微渲染引擎**：采用 **SoftRas** 和 **DIB-R** 等可微光栅化方法，通过平滑概率映射替代硬边界，使渲染过程对顶点位置、光照参数等完全可微。

3. **端到端图像空间优化**：将物理引擎与渲染引擎级联，构建从物理参数到图像像素的完整可微计算图。仅需目标图像（或视频帧）作为监督，即可通过 Adam 等梯度优化器推断物理属性或优化控制策略。

这一框架从根本上解除了白箱方法对三维状态监督的依赖，使得从普通视频中精确推断物理属性成为可能，并进一步拓展到视觉运动控制任务——仅凭一张目标图像即可引导可变形体或布料达到期望配置。

## 核心创新

∇Sim 的核心创新不在于提出新的可微物理引擎或可微渲染器，而在于**首次将两者耦合为统一的端到端计算图**，从而从根本上改变了物理参数估计与视觉运动控制的监督范式。这一耦合带来了三个紧密关联的 changed slots，构成了该方法区别于所有先前工作的本质差异。

### 从三维状态监督到二维图像监督

传统的白箱动力学方法（如 **DiffPhysics**）依赖可微物理引擎进行参数推断，但其损失函数必须构建在三维状态空间上——即每个时间步需要真实的广义坐标 $\mathbf{q}(t)$ 和广义速度 $\mathbf{u}(t)$ 作为监督信号。这对于可变形体、布料等系统而言极为苛刻：获取密集的逐粒子三维轨迹在现实中成本高昂甚至不可行。

∇Sim 通过将可微渲染嵌入计算图，使损失函数可以直接定义在图像空间（像素级 MSE），从而**仅需视频帧作为监督**。具体而言，给定仿真函数 $\mathbf{Sim}_{\eta} : \mathbb{R}^P \times [0,1] \mapsto \mathbb{R}^H \times \mathbb{R}^W$，优化目标变为最小化渲染图像与观测图像之间的像素差异，梯度通过渲染器反向传播至物理状态，再经由伴随方法传递至物理参数 $\theta$。这一改变使得原本需要昂贵三维标注的逆问题转化为仅需廉价二维观测即可求解的优化问题。

### 非可微渲染到可微光栅化

在 ∇Sim 之前，物理仿真与渲染是分离的：仿真器输出三维状态后，渲染仅用于可视化，不参与梯度计算。这导致基于非可微仿真器的方法（如 **PyBullet + REINFORCE**，Ehsani et al., 2020）只能依赖黑箱梯度估计器（如 REINFORCE）来推断物理参数，优化过程对超参数敏感且易陷入局部极小值。

∇Sim 引入了两种可微光栅化方案——**SoftRas**（Liu et al., 2019）和 **DIB-R**（Chen et al., 2019）——将渲染过程纳入可微计算图。光栅化的不可微性（边缘处的阶跃函数）通过平滑 sigmoid 近似得以解决，使得从像素损失到三维顶点位置、再到物理参数的完整梯度链得以建立。这一 changed slot 是端到端可微性的技术前提。

### 从黑箱梯度估计到精确解析梯度

前述两个 changed slots 共同促成了第三个根本性变化：梯度计算方式从黑箱估计转向精确的解析反向传播。∇Sim 通过隐式时间积分抽象 $\mathbf{g}(\mathbf{s}^-, \mathbf{s}^+, \boldsymbol{\theta}) = \mathbf{0}$ 和伴随方法，利用隐函数定理计算损失对初始状态和参数的梯度：

$$\frac{\partial l}{\partial \mathbf{s}^-} = \mathbf{c}^T \frac{\partial \mathbf{g}}{\partial \mathbf{s}^-}, \quad \left(\frac{\partial \mathbf{g}}{\partial \mathbf{s}^+}\right)^T \mathbf{c} = -\left(\frac{\partial l}{\partial \mathbf{s}^+}\right)^T$$

其中 $\mathbf{c}$ 为伴随变量。这种解析梯度的直接后果是损失景观极为平滑且具有唯一最小值（Figure 4），而基于 REINFORCE 的非可微仿真器则呈现多个局部极小值，优化过程对当前估计值的中心位置高度敏感（Figure 11）。

### 创新带来的质变效应

这三个 changed slots 的协同效应在实验中体现为两个关键突破：

1. **监督效率的跃迁**：在刚体质量估计任务中，∇Sim 仅使用图像监督即达到绝对相对误差 $9.01 \times 10^{-5}$，远超基于学习的黑箱方法 ConvLSTM（Xu et al., 2019b）的 0.0094（Table 1），甚至在某些指标上优于需要三维监督的 DiffPhysics。

2. **歧义问题的解决**：在布料视觉运动控制任务中，DiffPhysics 因依赖质心位置作为三维状态监督而陷入次优解（质心位于布料外部导致歧义），而 ∇Sim 仅需单张目标图像即可成功收敛（Figure 6b）。这表明图像空间的隐式目标比显式三维状态具有更强的表达能力和更少的歧义性。

需要指出的是，∇Sim 的性能高度依赖动力学和渲染模型的选择。消融实验（Table 4）表明，未建模的物理现象（如摩擦、弹性）导致的误差远大于渲染模型的简化（如使用非光真实渲染），这揭示了该方法作为白箱方法的本质局限：**建模偏差是性能上界的关键约束**。

## 整体框架

∇Sim 构建了一个从视频像素到物理属性的端到端可微计算图，其核心在于将**可微物理引擎**与**可微渲染引擎**耦合，使梯度能够穿越场景动力学演化与图像形成的全过程。这一设计消除了白箱动力学方法对三维状态真值标签的依赖——传统方法（如 DiffPhysics）需要每时间步的精确位置与速度监督，而 ∇Sim 仅需二维图像空间的像素级均方误差（MSE）即可完成优化。

### 计算图结构

整个 pipeline 由四个关键模块串联而成，形成一条完整的梯度传播链路：

1. **可微物理引擎**：接收场景物体的初始物理属性（质量、摩擦系数、弹性参数等）与控制输入，通过隐式时间积分方案演化系统状态。其核心抽象为 $\mathbf{g}(\mathbf{s}^-, \mathbf{s}^+, \boldsymbol{\theta}) = \mathbf{0}$，将任意离散时间积分格式统一为关于初始状态 $\mathbf{s}^-$、最终状态 $\mathbf{s}^+$ 和物理参数 $\boldsymbol{\theta}$ 的隐式关系。物理引擎支持刚体、基于四面体有限元（FEM）的超弹性可变形体、以及布料薄壳等多种动力学模型。

2. **可微渲染引擎**：将物理引擎输出的三维场景状态渲染为二维图像。∇Sim 采用 SoftRas 或 DIB-R 两种可微光栅化方案，通过平滑 sigmoid 函数实现边缘的可微处理，替代传统光栅化的硬边界离散操作。

3. **图像空间损失函数**：计算渲染图像与目标视频帧之间的像素级 MSE，形成标量损失信号。该损失是唯一的外部监督来源，无需任何三维状态标签。

4. **基于梯度的优化器**：利用自动微分框架（如 PyTorch）对整个计算图进行反向传播，获取损失对物理参数或控制策略的精确解析梯度，并通过 Adam 等优化器执行梯度下降更新。

### 关键设计特性

**物理与渲染的解耦速率**：∇Sim 允许物理仿真与渲染以独立且可调节的速率运行。物理引擎可以以高于渲染帧率的频率更新状态，从而在保证动力学精度的同时降低渲染计算开销——这是通过仅对部分物理步对应的状态进行渲染来实现的。

**源到源自动微分**：为实现高性能梯度计算，∇Sim 将仿真内核的 Python 子集转换为 C++/CUDA 代码，并将其包装为自定义 autograd 操作。这种设计在保持 Python 接口便利性的同时，获得了接近原生 CUDA 的伴随计算效率。

**多物理场统一框架**：Table 6 列出了 ∇Sim 支持的可微仿真类型及其可优化参数，涵盖初始粒子位置、速度、每粒子质量、初始朝向、弹簧刚度/阻尼/静止长度、驱动参数、重力、摩擦系数、弹性参数及外力参数等。这使得同一框架可处理刚体碰撞、可变形体弹性形变、布料动力学等多种物理场景。

### 输入输出规范

- **输入**：目标视频序列（或单张目标图像，用于视觉运动控制任务）以及场景物体的初始物理属性猜测（通常从均匀分布中随机采样）。
- **输出**：优化后的物理属性估计值，或训练得到的控制策略网络权重。
- **优化过程**：从随机初始化的参数出发，展开可微仿真生成预测视频，与目标视频逐像素比较计算 MSE 损失，反向传播梯度并更新参数，迭代至收敛。

Figure 2 完整展示了这一计算图：从视频观测出发，经随机初始化的场景属性（a）、可微物理引擎的时间演化（b）、可微渲染器的图像生成（c），最终到达图像空间损失（d）并反向传播梯度。传统方法（f）仅依赖可微物理引擎且需要状态空间的三维监督，而 ∇Sim（g）仅需图像空间监督即可完成同等精度的参数推断。

### 补充图表

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_02646/figures/001_Figure_1.jpg]]
*Figure 1: ∇Sim is a unified differentiable rendering and multiphysics framework that allows solving a range of control and parameter estimation tasks (rigid bodies, deformable solids, and cloth) directly from images/video*

## 核心模块与公式推导

### 整体计算图

∇Sim 的核心架构由两个可微组件串联构成：**可微物理引擎**与**可微渲染引擎**。整个系统定义为一个从物理参数到图像的映射：

$$Sim_{\eta} : \mathbb{R}^P \times [0,1] \mapsto \mathbb{R}^H \times \mathbb{R}^W; \quad \mathbf{Sim}(\mathbf{p}, t) = \mathcal{Z}$$

其中 $\mathbf{p}$ 为待优化的物理属性与控制参数，$t$ 为时间，$\mathcal{Z}$ 为渲染图像。通过在该计算图上定义图像空间损失（如像素级 MSE）并执行端到端反向传播，梯度可经由渲染器、物理状态序列，最终抵达物理参数，实现“从像素到物理属性”的优化闭环（Figure 2）。

### 可微物理引擎

物理引擎负责演化系统状态。系统状态定义为广义坐标与广义速度的联合向量：

$$\mathbf{s}(t) = [\mathbf{q}(t), \mathbf{u}(t)]$$

其动力学演化由二阶常微分方程描述：

$$\mathbf{M}(\mathbf{s}, \theta) \dot{\mathbf{s}} = \mathbf{f}(\mathbf{s}, \theta)$$

其中 $\mathbf{M}$ 为质量矩阵，$\mathbf{f}$ 为广义力函数，$\theta$ 为物理模型参数（如质量、弹性模量、摩擦系数等）。

为支持可微性，∇Sim 将任意离散时间积分格式抽象为隐式关系：

$$\mathbf{g}(\mathbf{s}^-, \mathbf{s}^+, \boldsymbol{\theta}) = \mathbf{0}$$

其中 $\mathbf{s}^-$ 和 $\mathbf{s}^+$ 分别表示时间步前后的系统状态。该隐式形式统一了显式欧拉、隐式欧拉、BDF 等多种积分器，使得梯度可通过隐函数定理和伴随方法高效计算（见下文梯度计算模块）。

对于**可变形体**，∇Sim 采用四面体有限元（FEM）与 Neo-Hookean 超弹性本构模型，其能量密度为：

$$\Psi(\mathbf{q}, \theta) = \frac{\mu}{2}(I_C - 3) + \frac{\lambda}{2}(J - \alpha)^2 - \frac{\mu}{2}\log(I_C + 1)$$

其中 $\lambda$、$\mu$ 为 Lamé 参数，$\alpha$ 为单元激活参数（控制局部膨胀/收缩），$I_C$ 和 $J$ 分别为 Cauchy-Green 不变量与变形梯度行列式。该公式直接嵌入物理引擎的力计算中，其参数即为可优化的材料属性。

### 可微渲染引擎

渲染器将三维场景状态转换为二维图像。传统光栅化因离散的三角形边界而产生不可微的阶梯函数。∇Sim 采用两种可微替代方案：**SoftRas** (Liu et al., 2019) 与 **DIB-R** (Chen et al., 2019)，其核心思路是将离散占用边界替换为平滑 sigmoid 函数，使像素颜色对顶点位置连续可微，从而允许渲染梯度反向传播至物理状态与场景几何。

物理仿真与渲染以**独立且可调节的速率**运行，允许以低于物理更新频率的帧率渲染，在计算成本与精度之间灵活权衡。

### 梯度计算：伴随法与源码转换自动微分

梯度通过整个计算图的反向传播获得。对于物理仿真部分，直接通过计算图自动微分可能因长序列展开导致内存爆炸。∇Sim 采用**伴随法**求解梯度：对于损失 $l$ 关于初始状态 $\mathbf{s}^-$ 的梯度，引入伴随变量 $\mathbf{c}$，满足：

$$\left(\frac{\partial \mathbf{g}}{\partial \mathbf{s}^+}\right)^T \mathbf{c} = -\left(\frac{\partial l}{\partial \mathbf{s}^+}\right)^T$$

$$\frac{\partial l}{\partial \mathbf{s}^-} = \mathbf{c}^T \frac{\partial \mathbf{g}}{\partial \mathbf{s}^-}$$

该方式避免了存储完整中间激活，显著降低内存开销。

在工程实现层面，∇Sim 使用**源码转换自动微分**：将仿真内核的 Python 子集编译为高性能 C++/CUDA 代码，并包装为 PyTorch 自定义 autograd 算子，兼顾了表达灵活性与运行时效率。

### 关键模块总结

| 模块 | 功能 | 核心技术 |
|------|------|----------|
| 可微物理引擎 | 演化系统状态并保持可微性 | 隐式时间积分、伴随法梯度、FEM 超弹性模型 |
| 可微渲染引擎 | 将三维场景渲染为二维图像 | SoftRas / DIB-R 可微光栅化 |
| 图像空间损失 | 提供优化信号 | 像素级 MSE |
| 梯度优化器 | 更新物理参数与控制策略 | Adam 等基于梯度的优化器 |
| 源码转换 Autodiff | 高性能梯度计算 | Python→C++/CUDA 编译 + 自定义 autograd 算子 |

## 实验与分析

### 核心实验设计

∇Sim 的实验体系围绕一个核心主张展开：**仅凭二维图像监督即可实现与依赖三维状态标签的方法相当甚至更优的物理参数推断与视觉运动控制性能**。实验覆盖三类物理系统——刚体、可变形固体（FEM）、布料——并分别评估参数估计与视觉运动控制两大任务。

参数估计任务的基本流程为：随机初始化待估计的物理属性（如质量、摩擦系数、弹性参数），通过可微物理引擎演化系统状态，经可微渲染生成预测视频帧，计算像素级均方误差（MSE），再沿整个计算图反向传播梯度以更新参数。视觉运动控制任务则在此基础上引入控制策略网络或直接优化初始速度，以单张目标图像作为隐式监督。

基线体系包含四个层次：**DiffPhysics**（仅可微物理引擎 + 每时间步 30 FPS 的真实三维状态监督）作为上限参考；**PyBullet + REINFORCE**（Ehsani et al., 2020）代表基于梯度估计的非可微仿真器方案；**ConvLSTM**（Xu et al., 2019b）作为黑箱学习方法；以及 **Average baseline** 和 **Random baseline** 两个平凡基线。

---

### 主实验结果

#### 刚体质量估计

Table 1 展示了刚体质量估计的定量对比。∇Sim 以 **绝对相对误差 9.01e-5** 的性能远超 ConvLSTM（0.0094），差距约两个数量级。值得注意的是，∇Sim 仅使用图像监督，而 DiffPhysics 依赖精确的三维状态标签，但 ∇Sim 仍取得了极具竞争力的结果（平均绝对误差 2.36e-5 kg）。PyBullet + REINFORCE 方案虽无需可微渲染，但其梯度估计的方差导致精度显著不如 ∇Sim，这从损失景观分析（Figure 4）中可找到根源——REINFORCE 的奖励景观存在多个局部极小值，而 ∇Sim 的损失景观平滑且具有唯一最小值。

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_02646/figures/005_Table_1.jpg]]
*Table 1: Mass estimation: ∇Sim obtains precise mass estimates, comparing favourably even with approaches that require 3D supervision (diffphysics). We report the mean abolute error and absolute relative errors for all approaches evaluated. Table 2: Rigid-body parameter estimation: ∇Sim estimates contact parameters (elasticity, friction) to a high degree of accuracy, despite estimating them from video. Diffphys. requires accurate 3D ground-truth at 30 FPS. We report absolute relative errors for each approach evaluated*

#### 刚体接触参数估计

Table 2 报告了刚体接触参数（弹性、摩擦系数）的估计精度。∇Sim 对摩擦系数 μ 的绝对相对误差为 **0.0073**，略优于需要三维监督的 DiffPhysics（0.0107）。这一结果尤为关键：它表明**耦合可微渲染不仅弥补了监督信号的降级，甚至可能通过图像空间提供的丰富视觉线索（如接触点的形变模式、运动轨迹的几何约束）实现更优的参数辨识**。弹性参数的估计同样表现出高精度，验证了框架对多参数联合优化的能力。

#### 可变形体参数估计

Table 3 呈现了可变形固体（FEM 超弹性模型）与布料的参数估计结果。对于可变形固体的每粒子质量估计，∇Sim 的相对 MAE 为 **0.048**，而 DiffPhysics（三维监督）为 0.032，差距在合理范围内。在布料场景中，DiffPhysics 出现了可感知的性能下降——这是因为布料的质心常位于物体外部，导致三维状态空间中的监督信号存在歧义。∇Sim 通过图像空间的全局像素匹配，自然规避了这一质心歧义问题。

#### 视觉运动控制

Figure 5 和 Figure 6 展示了视觉运动控制的定性与定量结果。在 control-fem 任务中（Figure 6a），∇Sim 使用单张目标图像即可成功驱动柔性体到达目标配置，而 DiffPhysics 依赖密集的三维状态奖励。在 control-cloth 任务中（Figure 6b），DiffPhysics 收敛到次优解，∇Sim 则凭借图像空间损失提供的全局形状约束，成功解决了因质心歧义导致的优化困难。这进一步印证了图像监督在特定场景下的独特优势：**像素级 MSE 隐含编码了物体的整体几何配置，避免了三维状态空间中因坐标系选择或参考点定义引入的歧义**。

---

### 消融实验

#### 动力学模型误差 vs. 渲染模型误差

Table 4（左）系统分析了模型失配对参数估计精度的影响。以完美模型（Perfect model）的相对绝对误差 0.1071 为参考上界，引入光真实渲染（Photorealistic render）后误差升至 0.1793，而未建模摩擦（Unmodeled friction）和未建模弹性（Unmodeled elasticity）分别导致误差升至 0.1866 和 0.2281。更极端的模型错配——将刚体建模为可变形体（Rigid-as-deformable）或将可变形体建模为刚体（Deformable-as-rigid）——分别产生 0.3462 和 0.4974 的误差。

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_02646/figures/011_Table_4.jpg]]
*Table 4: and perform physical parameter estimation from video. We notice that the performance obtained under this setting is superior compared to ones with dynamics model imperfections. Table 4: (Left) Impact of imperfect models: The accuracy of physical parameters estimated by ∇Sim is impacted by the choice of dynamics and graphics (rendering) models. We find that the system is more sensitive to the choice of dynamics models than to the rendering engine used. (Right) Timing analysis: We report runtime in simulation steps / second (Hz). ∇Sim is significantly faster than real-time, even for complex geometries*

核心结论是：**动力学建模误差对参数辨识精度的影响显著大于渲染建模误差**。这一发现具有重要的工程指导意义：在计算资源有限时，优先确保物理模型的准确性比追求光真实渲染更具性价比。

#### 视觉线索对收敛速度的影响

Figure 7 揭示了着色（shading）与纹理（texture）线索对优化收敛速度的显著影响。添加着色信息后，收敛速度大幅提升；进一步引入纹理线索，收敛速度在着色基础上仍有略微改善（插图采用对数 Y 轴）。这一现象可从梯度信息的角度理解：**着色和纹理在图像空间中引入了更丰富的空间梯度分布，使得像素级 MSE 损失对物理参数的偏导数具有更强的方向性，从而加速梯度下降**。纯轮廓匹配的损失景观相对平坦，优化需要更多迭代才能到达最小值。

#### 视频序列长度的影响

Figure 12 分析了视频序列长度对损失景观陡峭度的影响。较短的视频序列（如仅使用首尾帧）产生更陡峭的损失景观，但所有长度下损失景观均保持平滑且具有相同的唯一最小值。这意味着 ∇Sim 即使在极稀疏的时间监督下也能保持优化稳定性，但更长的序列通过提供更密集的约束，可能提高对噪声的鲁棒性。

#### 可微性对优化质量的影响

Figure 11 和 Appendix H.1 对比了 ∇Sim（精确解析梯度）与 PyBullet + REINFORCE（梯度估计）在质量估计任务上的损失景观。REINFORCE 的负对数似然景观在真实值附近仅呈现局部极小值，且该极小值的位置对当前质量估计的中心高度敏感，导致优化过程易陷入次优解。相比之下，∇Sim 的 MSE 损失景观在真实参数处具有唯一、主导的全局最小值。这从根本上解释了**端到端可微性带来的优化质量优势：精确梯度提供了可靠的下降方向，而梯度估计的方差不仅减慢收敛，更可能将优化引向错误的局部极小值**。

#### 时间性能

Table 4（右）报告了 ∇Sim 各模块的仿真速率。可微物理引擎与可微渲染引擎均以远超实时的速度运行，即使对于复杂几何体也是如此。物理仿真与渲染以独立且可调的速率执行，允许通过降低渲染帧率来换取计算效率，这一设计在实际部署中提供了灵活的精度-速度权衡。

---

### 失败模式与局限性

尽管 ∇Sim 展现了令人瞩目的性能，但其局限性同样值得正视：

1. **极小质量物体的数值不稳定**：当物体质量 ≤ 100g 时，物理引擎的数值稳定性下降，梯度计算可能发散。这是隐式时间积分与伴随法在极端参数下的已知问题，需要进一步研究正则化策略或自适应时间步长。

2. **接触密集运动的处理能力有限**：当前框架对含有大量不连续接触的运动（如颗粒流、多体碰撞）处理能力不足。这是因为接触检测与响应的梯度传播依赖于平滑近似，而密集接触场景下的非光滑性会破坏梯度信息的可靠性。需要引入可微 LCP（线性互补问题）求解器等更先进的接触处理方案。

3. **铰接体支持缺失**：当前不支持含棱柱关节的铰接体系统，限制了在机器人学等领域的直接应用。

4. **仿真-现实差距**：真实世界视频中存在大量未建模的物理现象（如复杂摩擦、空气动力学效应、非均匀材质），直接部署到现实场景时性能会显著下降。Table 4 的消融实验已从仿真侧量化了模型失配的影响，但现实世界的未建模因素更加多样且难以枚举。

5. **前期工程成本高**：作为白箱方法，∇Sim 的性能高度依赖动力学和渲染模型的选择，需要针对具体场景定制物理模型、网格划分和渲染参数。这一前期投入在快速原型验证场景中可能成为瓶颈。

---

### 关键图表结论汇总

| 图表 | 核心结论 | 证据强度 |
|------|----------|----------|
| Table 1 | ∇Sim 仅用图像监督即可达到与三维监督方法相当的刚体质量估计精度 | 强（多基线、定量指标） |
| Table 2 | 接触参数估计中 ∇Sim 略优于 DiffPhysics，图像监督未造成精度损失 | 强（直接对比三维监督基线） |
| Table 3 | 可变形体估计接近三维监督方法；布料场景中 ∇Sim 规避了质心歧义 | 较强（DiffPhysics 在布料上出现退化） |
| Figure 4 | ∇Sim 损失景观平滑且具有唯一最小值，REINFORCE 存在多个局部极小值 | 强（可视化 + 定量分析） |
| Figure 6 | 视觉运动控制中 ∇Sim 仅需单张目标图像即可成功，DiffPhysics 收敛到次优解 | 较强（两个任务的一致性结果） |
| Table 4（左） | 动力学建模误差的影响 > 渲染建模误差 | 强（系统消融，多模型变体） |
| Figure 7 | 着色和纹理线索显著加速收敛 | 较强（对数坐标显示明显差异） |
| Figure 12 | 视频长度影响损失景观陡峭度但不改变最小值位置 | 中等（仅可视化，无定量指标） |

### 补充图表

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_02646/figures/004_Table.jpg]]

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_02646/figures/022_Table_5.jpg]]
*Table 5: PyBullet-REINFORCE hyperparameters*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_02646/figures/023_Table_6.jpg]]
*Table 6: presents an overview of the differentiable simulations implemented in ∇Sim, and the optimizable parameters therein. Table 6: An overview of optimizable parameters in ∇Sim. Table columns are (in order, from left to right): Initial particle positions (pos), Initial particle velocities (vel), Per-particle mass (mass), Initial object orientation (rot), Spring rest lengths (rest), Spring stiffnesses (stiff), Spring damping coefficients (damp), Actuation parameters (actuation), Gravity (g), Friction parameters µ, Elasticity parameters (e), External force parameters (ext forces)*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2104_02646/figures/003_Figure_3.jpg]]
*Figure 3: Parameter Estimation: For deformable experiments, we optimize the material properties of a beam to match a video of a beam hanging under gravity. In the rigid experiments, we estimate contact parameters (elasticity/friction) and object density to match a video (GT). We visualize entire time sequences (t) with color-coded blends*

## 方法谱系与知识库定位

### 方法谱系

∇Sim 处于**可微物理仿真**与**可微渲染**的交汇点，其核心贡献在于首次将两者耦合为统一的端到端可微计算图，从而将逆问题求解从三维状态空间迁移到二维图像空间。

**上游基线对比。** ∇Sim 所回应的核心瓶颈是：以往基于白箱动力学的方法（如 **DiffPhysics**）虽能通过可微物理引擎精确推断物理属性，但**依赖每时间步的三维真实状态标签**（位置、速度等，30 FPS），这对可变形体或布料等系统获取成本极高甚至不可行。∇Sim 的关键突破在于将监督信号从三维状态替换为二维图像（像素级 MSE 损失），同时保持与三维监督方法相近的精度。例如，在刚体质量估计任务中，∇Sim 的绝对相对误差为 $9.01 \times 10^{-5}$，显著优于基于学习的黑箱方法 **ConvLSTM**（Xu et al., 2019b）的 0.0094，且与需要三维监督的 DiffPhysics 性能可比（Table 1）。

**梯度计算方式的根本差异。** 与使用梯度估计器（如 REINFORCE）通过非可微仿真器（**PyBullet + REINFORCE**，Ehsani et al., 2020）进行优化的方法相比，∇Sim 通过整个计算图（物理引擎 + 渲染引擎）的**精确解析梯度反向传播**，获得了平滑且具有唯一最小值的损失景观（Figure 4）。相比之下，REINFORCE 的损失景观存在多个局部极小值，对超参数敏感，优化过程易陷入次优解（Figure 11b），这从根本上限制了其在实际应用中的可靠性。

**渲染可微性的引入。** 在 ∇Sim 之前，可微物理引擎通常独立工作，不包含渲染模块或其渲染不可微。∇Sim 通过集成 **SoftRas**（Liu et al., 2019）和 **DIB-R**（Chen et al., 2019）两种可微光栅化方案，使梯度能够从像素空间经渲染器回传至物理状态，再经物理引擎回传至物理参数。这一架构设计使得原本不适定的“从视频推断物理属性”问题转化为可梯度下降的优化问题。

### 适用边界与关键假设

∇Sim 的性能高度依赖**动力学模型与渲染模型的选择**，这是白箱方法的固有特性。消融实验（Table 4 左）揭示了建模偏差的影响层级：

| 模型变体 | 平均相对绝对误差 |
|---------|----------------|
| 完美模型（参考上界） | 0.1071 |
| 光真实渲染（无动力学误差） | 0.1793 |
| 未建模摩擦 | 0.1866 |
| 未建模弹性 | 0.2281 |
| 刚体当作可变形体建模 | 0.3462 |
| 可变形体当作刚体建模 | 0.4974 |

核心发现是：**动力学建模误差的影响远大于渲染建模误差**。即使使用光真实渲染器，若动力学模型存在未建模的摩擦或弹性，误差也会显著增加；而将刚体错误地建模为可变形体（或反之）会导致误差急剧上升（3-5 倍）。这意味着 ∇Sim 的部署需要针对具体场景定制合理的物理模型。

**视觉线索的作用。** 着色和纹理线索能显著加速收敛（Figure 7），其中纹理相比于单向着色提供额外的微弱提升（对数坐标轴内插图）。这表明渲染管线的信息丰富度直接影响优化效率，但并非收敛的必要条件。

**视频长度的影响。** 较短的视频序列产生更陡峭的损失景观，但所有视频长度下损失景观均保持平滑且具有相同的唯一最小值（Figure 12）。这为实际应用中在计算成本与优化稳定性之间权衡提供了依据。

### 局限性与开放问题

**已知局限性：**

1. **数值稳定性边界**：无法处理极小质量（$\leq 100\text{g}$）的物体，物理引擎在极端参数区域的数值稳定性需要进一步研究。
2. **机构类型限制**：当前不支持含棱柱关节的铰接体，限制了在机器人学中的应用范围。
3. **接触密集场景**：对含有大量不连续性的接触密集运动处理能力有限，需采用更先进的接触检测和线性互补问题（LCP）求解器。
4. **现实差距**：真实世界视频中存在大量未建模的物理现象（如复杂摩擦、空气动力学效应），直接部署到现实场景存在显著差距。
5. **工程成本**：构建仿真基础设施的前期工程成本较高，需要针对具体场景定制物理与渲染模型。

**开放研究问题：**

1. **机构扩展**：如何将可微框架扩展到铰接体与复杂多关节系统？
2. **接触求解**：如何通过可微 LCP 或互补求解器处理高密度接触运动，同时保持梯度流的数值稳定性？
3. **现实迁移**：如何弥合仿真与真实世界的差距，以适应未建模的物理现象？域随机化或系统辨识的在线自适应可能是可行方向。
4. **数值鲁棒性**：如何改善极小质量物体的数值稳定性并保持可微性？
5. **渲染升级**：能否将光真实渲染（如路径追踪）融入可微管道，同时维持高效的梯度计算？当前光真实渲染实验（Table 4）已显示其可行性，但计算效率仍是瓶颈。
6. **机器人部署**：如何将该框架应用于真实机器人系统的在线参数辨识与视觉运动控制？这需要解决实时性约束和传感器噪声建模等问题。

### 知识库定位

∇Sim 在知识谱系中扮演**桥梁角色**：它连接了可微物理仿真社区（以 DiffPhysics 为代表的三维监督范式）与可微渲染社区（以 SoftRas、DIB-R 为代表的图像空间梯度计算），开创了“仅需图像监督即可进行物理属性推断与视觉运动控制”的新范式。其方法论为后续工作在以下方向提供了基础：从视频中学习物理直觉、基于图像的机器人系统辨识、以及将视觉感知与物理推理统一在可微框架下的更广泛尝试。

## 原文 PDF

![[paperPDFs/ICLR_2021/gradSim_Differentiable_simulation_for_system_identification_and_visuomotor_control.pdf]]
