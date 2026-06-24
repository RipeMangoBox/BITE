---
title: "Simplicits: Mesh-Free, Geometry-Agnostic, Elastic Simulation"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Simplicits_Mesh_Free_Geometry_Agnostic_Elastic_Simulation.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/simplicits/
aliases:
- Simplicits
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将所有几何表示统一为占有率函数（occupancy function）查询接口，并采用数据无关的物理启发式训练策略（弹性损失+正交损失）直接在占有率函数上优化神经蒙皮权重，从而建立表示无关的减基模拟框架。"
primary_logic: "任意标准的3D几何表示均可转化为空间任意点的占有率查询；基于此，利用线性混合蒙皮（LBS）作为形变基，并通过随机变换采样的蒙特卡洛弹性能量最小化来学习形状感知的神经蒙皮权函数，可以在没有网格或任何显式离散化的条件下进行物理模拟，实现表示无关性。"
claims:
- "任意标准几何表示可归约为占有率函数查询，形成表示无关的模拟接口。"
- "使用数据无关的弹性损失与正交性损失训练神经蒙皮权重，可捕获物理合理的大形变。"
- "与线性四面体FEM参考解相比，9个手柄的Simplicits结果非常接近，优于SPH和MPM。"
- "使用ELU激活比SIREN更严格地满足边界条件。"
---

# Simplicits: Mesh-Free, Geometry-Agnostic, Elastic Simulation

> [!tip] 核心洞察
> 任意标准的3D几何表示均可转化为空间任意点的占有率查询；基于此，利用线性混合蒙皮（LBS）作为形变基，并通过随机变换采样的蒙特卡洛弹性能量最小化来学习形状感知的神经蒙皮权函数，可以在没有网格或任何显式离散化的条件下进行物理模拟，实现表示无关性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Simplicits：无网格、几何无关的弹性模拟 |
| 英文题名 | Simplicits: Mesh-Free, Geometry-Agnostic, Elastic Simulation |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://arxiv.org/abs/2407.09497); [Project](https://research.nvidia.com/labs/toronto-ai/simplicits/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Simplicits |
| Dataset | Mesh monkey (triangle mesh), SDF key (signed distance function), Gaussian Splat lego, Cantilever bar (corotational FEM reference) |

> [!tip] 效果简介
> - Mesh monkey (triangle mesh) 上，Training time / Sim Step time 为 180 sec / 51 ms，对比 N/A，变化 N/A。
> - SDF key (signed distance function) 上，Training time / Sim Step time 为 886 sec / 107 ms，对比 N/A，变化 N/A。
> - Gaussian Splat lego 上，Training time / Sim Step time 为 5550 sec / 74 ms，对比 N/A，变化 N/A。

## 概述

**问题瓶颈**：现有弹性物理模拟器高度依赖特定的输入几何表示——四面体网格、显式网格或粒子系统——难以无缝处理神经辐射场（NeRF）、高斯泼溅、符号距离函数（SDF）等新兴隐式或稀疏表示。这迫使研究者为每种几何形式设计复杂的转换流程和算法适配，严重限制了模拟技术的通用性与易用性。

**核心思路**：Simplicits 提出了一种表示无关的减基模拟框架。其关键洞察在于：任意标准的3D几何表示均可归约为空间任意点的占有率函数（occupancy function）查询接口。在此统一抽象之上，方法利用线性混合蒙皮（LBS）作为形变基，通过随机变换采样的蒙特卡洛弹性能量最小化来学习形状感知的神经蒙皮权函数，从而在无网格、无显式离散化的条件下进行物理模拟。

**方法定位**：Simplicits 属于数据无关的神经减基模拟方法。与依赖预模拟数据的 CROM/LiCROM 不同，它仅需几何的占有率查询即可训练；与基于网格的 Fast Skinning Eigenmodes 相比，它不依赖任何显式拓扑结构；与 SPH、MPM 等无网格方法相比，它在极低自由度下仍能保持与线性四面体 FEM 参考解接近的精度。

**主要结果**：
- **精度**：在悬臂梁对比实验中，9个手柄的 Simplicits 结果与线性四面体 FEM 参考解非常接近，显著优于 SPH（5582粒子）和 MPM（5000粒子），并与基于网格的减基方法 Fast Skinning Eigenmodes 表现相当（Fig. 8）。
- **表示通用性**：成功在三角网格、SDF、高斯泼溅、NeRF、CT扫描体、点云等多种几何表示上完成弹性模拟，验证了占有率接口的统一能力（Fig. 1, 13–17）。
- **性能**：训练时间从网格猴子的约3分钟到高斯泼溅乐高的约1.5小时不等；运行时每模拟步在51–107 ms范围内（Table 1），且模拟步时随自由度增加呈超线性增长（Fig. 10）。
- **关键消融**：非线性 Neo-Hookean 能量训练与全仿射变换采样是保证大扭曲精度的核心设计（Fig. 9）；弹性损失对产生物理真实响应至关重要，去除后模拟响应退化（Fig. 11）；ELU 激活函数比 SIREN 更严格地满足边界条件（Fig. 7）。

**局限性**：当前方法假设形变基在仿真过程中保持不变，无法处理拓扑变化（如断裂、切割）；对刚度分布极不均匀的物体训练可能收敛困难；从形变映射反向渲染隐式场尚未完全解决；复杂几何的训练时间仍较长。

## 背景与动机

弹性体物理模拟是计算机图形学、机器人学和工程设计中的核心技术，其目标是预测物体在力、碰撞和约束作用下的形变与运动。传统上，这一任务由有限元法（FEM）主导，但FEM高度依赖特定的空间离散化——通常需要将输入几何转化为高质量的四面体网格或六面体网格。这一前置步骤不仅计算代价高昂、难以自动化，更关键的是，它与近年来涌现的多样化三维表示范式产生了根本性矛盾。

### 表示碎片化：模拟技术面临的核心瓶颈

当前三维视觉与重建领域已发展出丰富多样的几何表示形式：显式三角网格、点云、符号距离函数（SDF）、神经辐射场（NeRF）、三维高斯泼溅（3D Gaussian Splatting）、占用网络（Occupancy Networks），乃至直接从CT扫描获取的体素数据。每一种表示都服务于不同的应用场景，在存储效率、渲染质量和重建精度上各具优势。然而，现有的弹性模拟器几乎无一例外地要求特定的输入格式：

- **基于网格的方法**（如共旋线性四面体FEM、**Fast Skinning Eigenmodes**（Benchekroun et al., 2023））需要显式的体网格连接关系，对非网格表示需要复杂的四面体化或重新网格化流程；
- **无网格方法**（如**SPH**（Kugelstadt et al., 2021）和**MPM**（Hu et al., 2019））虽然摆脱了网格约束，但仍依赖于粒子采样和邻域查询，对于SDF、NeRF等隐式表示需要额外的表面采样或体积填充步骤；
- **数据驱动的降阶模型**（如**CROM/LiCROM**（Chen et al., 2023b; Chang et al., 2023））虽然能加速模拟，但需要预先在特定表示上运行完整FEM仿真以生成训练数据，无法直接泛化到新的几何表示。

这种“表示碎片化”导致了实际工作流中的严重摩擦：从重建到模拟的管线需要繁琐的格式转换、几何修复和算法适配，不仅增加了工程复杂度，还可能引入几何精度损失和模拟误差。更根本的是，这限制了物理模拟技术向新兴三维表示生态的渗透——当用户拥有一个NeRF重建的青蛙或高斯泼溅重建的乐高模型时，直接对其进行物理模拟几乎是不可能的任务。

### 统一抽象的缺失与本文动机

上述困境的根源在于：现有模拟方法将物理计算与特定的几何离散化方式深度耦合，缺乏一个统一的、表示无关的几何抽象层。Simplicits的核心动机正是建立这样一个抽象——观察到**任意标准的三维几何表示都可以归约为空间任意点的占有率函数（occupancy function）查询**，即给定空间中的一个点 $\mathbf{X}$，返回该点是否位于物体内部的指示 $\Phi(\mathbf{X}) \in [0,1]$。这一观察构成了表示无关模拟的理论基础。

基于此，Simplicits提出了一种全新的范式：将物理模拟从显式空间离散化中彻底解耦，转而在一个连续神经场中隐式编码形变基。具体而言，方法用一个小型隐式神经网络 $\mathbf{W}_\theta: \mathbb{R}^3 \to \mathbb{R}^n$ 来存储空间变化的蒙皮权重，这些权重充当降阶形变基；训练过程不需要任何预仿真数据，而是通过随机手柄变换采样的蒙特卡洛弹性能量最小化来学习物理上有意义的运动模式。这一设计使得Simplicits能够直接消费网格、SDF、高斯泼溅、NeRF、CT扫描体素等几乎任意几何表示，无需格式转换、网格生成或邻域查询，真正实现了“即插即用”的弹性模拟。

### 技术挑战与设计抉择

实现这一愿景面临三个关键技术挑战：

1. **如何在没有网格的条件下计算物理量？** 传统FEM依赖网格单元内的数值积分来计算质量矩阵和弹性能量。Simplicits通过将体积积分转化为占有率加权的蒙特卡洛积分 $\int_{\mathbb{R}^3} \Phi(\mathbf{X}) g(\mathbf{X}) d\mathbf{X}$，在固定的预采样点上一次性完成积分评估，完全绕过显式离散化。

2. **如何在不依赖仿真数据的前提下学习物理合理的形变基？** 数据驱动的降阶模型需要大量FEM仿真数据，这本身就要求预先拥有可仿真的网格表示。Simplicits采用数据无关的物理启发式训练策略：通过随机采样手柄变换并最小化对应的弹性能量（弹性损失 $\mathcal{L}_{\mathrm{elastic}}$），同时强制蒙皮权重相互正交（正交损失 $\mathcal{L}_{\mathrm{ortho}}$），使网络自主发现低能形变模式。

3. **如何保证降阶基的表达能力和边界条件满足？** 降阶模拟的本质是用少量自由度近似全阶动力学，因此基的质量至关重要。Simplicits采用全仿射变换（3×4矩阵）而非仅平移变换作为手柄动作空间，并使用非线性Neohookean能量而非线性能量进行训练，以捕获大形变下的几何非线性效应。此外，ELU激活函数的使用被实验证明比SIREN更严格地满足固定边界条件。

通过这些设计，Simplicits在保持降阶模拟计算效率的同时，实现了对输入几何表示的完全无关性，为物理模拟技术与现代三维视觉生态的融合开辟了新路径。

## 核心创新

Simplicits的核心创新在于将弹性物理模拟从对特定几何表示的依赖中解放出来，构建了一个**无网格、几何无关的减基模拟框架**。其关键突破可归纳为以下几个相互关联的changed slots：

### 1. 形变基存储：从显式离散化到连续神经场

传统减基模拟方法（如**Fast Skinning Eigenmodes**, Benchekroun et al. 2023）的形变基严格依附于显式四面体网格或粒子系统及其连接关系。Simplicits将形变基存储为一个连续的向量值神经场 $\mathbf{W}_\theta: \mathbb{R}^3 \to \mathbb{R}^n$，即神经蒙皮权函数，无需任何显式支架。这一转变的因果机制在于：连续神经场可以在空间任意点被查询，从而天然适配任何能够提供空间点占有率查询的几何表示。

### 2. 几何接口：统一为占有率函数查询

该框架的表示无关性根植于一个核心洞察：**任意标准的3D几何表示均可归约为空间任意点的占有率函数查询** $\Phi(\mathbf{X}) \in [0,1]$。无论是显式三角网格、符号距离函数（SDF）、高斯泼溅、神经辐射场（NeRF）还是CT扫描体素，Simplicits仅需一个统一的查询接口即可工作。这消除了传统流程中复杂的几何转换和算法适配步骤，是方法通用性的根本保障。

### 3. 训练策略：数据无关的物理启发式优化

与需要预模拟数据作为监督的神经降阶模型（如**CROM/LiCROM**, Chen et al. 2023b; Chang et al. 2023）不同，Simplicits采用完全数据无关的训练策略。其损失函数由两项物理启发式损失组成：

$$\theta^* = \arg\min_\theta \lambda_{\mathrm{elastic}} \mathcal{L}_{\mathrm{elastic}} + \lambda_{\mathrm{ortho}} \mathcal{L}_{\mathrm{ortho}}$$

- **弹性损失** $\mathcal{L}_{\mathrm{elastic}}$：对随机采样的手柄仿射变换 $\mathbf{Z}$，最小化物体内部的弹性势能，鼓励权重学习物理上低能量的形变模式。
- **正交性损失** $\mathcal{L}_{\mathrm{ortho}}$：强制不同手柄的蒙皮权重相互正交，避免模式坍缩，确保形变基的多样性。

训练完成后，神经网络**无需在物理时间步进循环中被调用**，仅需在预处理阶段于固定采样点处计算一次权重及其导数，这保证了运行时的高效性。

### 4. 手柄变换类型：从纯平移到全仿射

先前的蒙皮本征模工作通常仅考虑手柄的平移变换。Simplicits将手柄变换扩展为**全仿射变换（3×4矩阵）**，并在训练中采样这些全变换。消融实验（Fig. 9）表明，在强扭曲近屈曲状态下，采样全仿射变换并使用非线性Neohookean能量训练，比仅用线性能量或仅平移变换能带来适度的精度提升。

### 5. 空间积分：从网格求积到蒙特卡洛采样

传统方法依赖基于网格的求积或显式体素采样来计算质量矩阵和弹性势能的空间积分。Simplicits将一般积分形式化为占有率加权的蒙特卡洛积分：

$$G = \int_{\mathbb{R}^3} \Phi(\mathbf{X}) g(\mathbf{X}) d\mathbf{X}$$

积分在**预处理阶段于一组固定采样点**上通过蒙特卡洛方法计算，完全避免了运行时的空间离散化依赖。

### 6. 边界条件满足：ELU激活优于SIREN

在神经场的实现细节上，Simplicits发现使用ELU激活函数比SIREN（Sitzmann et al. 2020）能更严格地满足固定边界条件（Fig. 7）。这一实验发现对于确保模拟精度具有实际意义，尤其是在大形变场景下。

### 关键证据强度评估

上述创新的核心主张均具有较高置信度（≥0.9），主要证据来自论文中的定量消融实验和定性对比：
- 表示无关性由占有率接口的理论归约和多种几何表示（网格、SDF、高斯泼溅、NeRF、CT）的成功模拟案例支撑。
- 物理启发式训练的必要性由Fig. 11（有无弹性损失对比）和Fig. 9（非线性能量与全变换采样消融）直接验证。
- 与FEM参考解的精度对比（Fig. 8）显示，9个手柄的Simplicits结果与基于网格的Fast Skinning Eigenmodes非常接近，且显著优于SPH和MPM等纯无网格方法。

## 整体框架

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2407_09497/figures/009_Figure_8.jpg]]
*Figure 8: A cantilever bar comparison between a reference linear-tetrahedral, Corotational FEM beam,our method with 6and 9 handles,Fast Skinning Eigenmodes [Benchekroun et al.2023] with 10 handles,SPH[Kugelstadt et al.2021] with 5582 particles,and MPM [Hu etal.2019] with 5000 particles and initial grid density of 10.Notice ours matches Fast Skinning Eigenmodes very closely andf exhibits similar numerical coarsening due to reduction when compared to FEM.Simulations are run for 300 steps with timestep 0.01s,with young's modulus 5e6Pa,poisson ratio 0.45,density 1 0 0 0 $\mathrm { k g / m ^ { 3 } }$ using corotational linear elastic material*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2407_09497/figures/002_Figure_2.jpg]]
*Figure 2: Simulations of point clouds undergoing large deformations. Our method produces shape-aware skinning weights on complex geometries*

Simplicits 提出了一套**表示无关的弹性物理模拟流程**，其核心思想是将任意标准 3D 几何表示统一归约为占有率函数（occupancy function）查询接口，并在此之上训练一个神经蒙皮权场作为减基形变基，从而在无网格、无显式离散化的条件下实现物理模拟。

### 流程总览

整体 pipeline 如图 3 所示，分为三个主要阶段：

1. **几何抽象层**：将输入几何（三角网格、点云、SDF、高斯泼溅、NeRF 等）统一转化为占有率函数 $\Phi(\mathbf{X}) \in [0,1]$，该函数可在空间任意点 $\mathbf{X} \in \mathbb{R}^3$ 查询该点属于物体内部的概率。这一层屏蔽了底层几何表示的差异，为后续所有物理计算提供统一接口。

2. **神经蒙皮权训练（离线预处理）**：利用一个小型隐式神经网络 $\mathbf{W}_\theta: \mathbb{R}^3 \to \mathbb{R}^n$ 编码 $n$ 个手柄（handle）对应的空间变化蒙皮权重。训练采用**数据无关的物理启发式损失**——通过随机采样手柄仿射变换 $\mathbf{Z}_j$（$3\times4$ 矩阵），最小化物体在这些随机扰动下的弹性势能（弹性损失 $\mathcal{L}_{\mathrm{elastic}}$），同时施加正交性损失 $\mathcal{L}_{\mathrm{ortho}}$ 确保各形变模式互不冗余。训练仅需在固定采样点上进行一次蒙特卡洛积分预处理，不依赖任何预模拟数据。

3. **运行时模拟**：将训练好的蒙皮权场在采样点上的权重及其导数作为预计算量，构建减基系统的质量矩阵 $\mathbf{M}$ 和弹性势能 $E_{\mathrm{pot}}$。模拟时采用隐式欧拉时间积分，通过牛顿法求解每一步的自由度 $\mathbf{z}$，形变映射由线性混合蒙皮（LBS）给出：
   $$\phi(\mathbf{X}, \mathbf{z}) = \mathbf{X} + \sum_{j=1}^{n} \mathbf{W}_j(\mathbf{X}) \mathbf{Z}_j \left[ \mathbf{X} \right]$$
   运行时**无需再次查询神经网络**，所有物理量均在降维空间内高效计算。

### 模块关系与数据流

| 模块 | 输入 | 输出 | 角色 |
|------|------|------|------|
| 占有率函数接口 | 任意 3D 几何表示 | $\Phi(\mathbf{X})$ 查询 | 统一几何抽象层，使后续模块与具体表示解耦 |
| 神经蒙皮权 MLP | 空间坐标 $\mathbf{X}$ | $\mathbf{W}_\theta(\mathbf{X}) \in \mathbb{R}^n$ | 学习形状感知的减基形变基 |
| 随机手柄变换采样 | 正态分布 $\mathcal{N}(\mu, \mathbf{0})$，$\mu=0.1$ | 随机仿射变换 $\mathbf{Z}_j$ | 提供训练扰动，激发物理显著的形变模式 |
| 蒙特卡洛积分 | $\Phi$、$\mathbf{W}_\theta$、采样点 | $\mathbf{M}$、$E_{\mathrm{pot}}$ 等物理量 | 无网格空间积分，一次性预处理 |
| 隐式欧拉牛顿求解器 | $\mathbf{M}$、$E_{\mathrm{pot}}$、外力 | 自由度轨迹 $\mathbf{z}_t$ | 运行时动力学模拟 |

### 关键设计决策

- **ELU 激活函数**：实验表明（图 7），相比 SIREN，ELU 激活能更严格地满足固定边界条件，这对模拟精度至关重要。
- **非线性 Neohookean 能量训练**：消融实验（图 9）证明，在训练阶段使用非线性 Neohookean 能量并采样全仿射变换（而非仅平移），能在强扭曲近屈曲状态下显著提升精度。
- **运行时与训练解耦**：训练阶段使用的超弹性材料模型可与模拟阶段不同，赋予用户灵活选择材料本构的自由。

### 输入输出规范

- **输入**：任意可转化为占有率查询的 3D 几何表示（显式网格、点云、SDF、高斯泼溅、NeRF 等），以及物理参数（杨氏模量、泊松比、密度等）。
- **输出**：物体在用户指定手柄变换或外力作用下的动态形变动画，表现为采样点或渲染后的形变几何序列。

## 核心模块与公式推导

### 3.1 隐式时间积分框架

Simplicits 的动力学仿真建立在隐式欧拉时间积分之上，将其转化为关于广义自由度 $\mathbf{z}$ 的无约束优化问题：

$$
\mathbf{z}_{t+1} = \underset{\mathbf{z}}{\arg\min} \frac{1}{2} \|\mathbf{z} - \tilde{\mathbf{z}_t}\|_{\mathbf{M}}^2 + h^2 E_{\mathrm{pot}}(\mathbf{z}) \tag{1}
$$

其中 $\tilde{\mathbf{z}}_t = \mathbf{z}_t + h \dot{\mathbf{z}}_t$ 为惯性预测项，$h$ 为时间步长，$\mathbf{M}$ 为质量矩阵，$E_{\mathrm{pot}}$ 为弹性势能。该优化问题在运行时通过牛顿法求解，而 $\mathbf{M}$ 和 $E_{\mathrm{pot}}$ 的具体形式则依赖于后续的形变基选择。

### 3.2 神经蒙皮形变基

形变映射采用线性混合蒙皮（Linear Blend Skinning, LBS），将 $n$ 个手柄的仿射变换通过空间变化的蒙皮权重场进行混合：

$$
\phi(\mathbf{X}, \mathbf{z}) = \mathbf{X} + \sum_{j=1}^{n} \mathbf{W}_j(\mathbf{X}) \mathbf{Z}_j \left[ \mathbf{X} \right] \tag{2}
$$

式中 $\mathbf{X} \in \mathbb{R}^3$ 为参考构型中的物质点坐标，$\mathbf{Z}_j \in \mathbb{R}^{3\times4}$ 为第 $j$ 个手柄的仿射变换矩阵，$\mathbf{W}_j(\mathbf{X})$ 为对应的标量蒙皮权重函数。$\mathbf{z} \in \mathbb{R}^{12n}$ 将所有手柄变换的自由度展平为向量。

与传统的网格蒙皮不同，Simplicits 将蒙皮权重函数存储为**向量值连续神经场** $\mathbf{W}_\theta: \mathbb{R}^3 \to \mathbb{R}^n$，使用约 9 层隐藏层、ELU 激活的 MLP 实现。该神经场无需显式网格或粒子连接关系，是实现几何无关性的核心设计。

### 3.3 物理量的无网格积分

质量矩阵和弹性势能在参考构型上定义为空间积分：

$$
\mathbf{M} = \int_{\Omega} \rho \mathbf{J}(\mathbf{X})^T \mathbf{J}(\mathbf{X}) d\Omega \qquad E_{\mathrm{pot}} = \int_{\Omega} \Psi(\phi(\mathbf{X})) d\Omega \tag{3}
$$

其中 $\mathbf{J}(\mathbf{X}) = \partial\phi/\partial\mathbf{z}$ 为形变映射关于自由度的雅可比，$\Psi$ 为超弹性能量密度函数。

**占有率函数接口（核心抽象）**：为统一处理任意几何表示，Simplicits 将所有积分重写为占有率加权形式：

$$
G = \int_{\mathbb{R}^3} \Phi(\mathbf{X}) g(\mathbf{X}) d\mathbf{X} \tag{4}
$$

$\Phi(\mathbf{X}) \in [0,1]$ 为空间任意点的占有率函数，对显式网格、SDF、高斯泼溅、NeRF 等均可通过查询获得。积分通过蒙特卡洛方法在**预处理阶段一次性采样的固定点集**上求值，运行时无需再访问神经场或原始几何表示。

### 3.4 数据无关的蒙皮权重训练

Simplicits 的核心创新在于完全无需预模拟数据的权重优化策略。训练目标为：

$$
\theta^* = \arg\min_\theta \lambda_{\mathrm{elastic}} \mathcal{L}_{\mathrm{elastic}} + \lambda_{\mathrm{ortho}} \mathcal{L}_{\mathrm{ortho}} \tag{5}
$$

**弹性损失**：对随机采样的手柄变换 $\mathbf{Z}$，最小化对应的弹性能量，鼓励权重学习低能（即物理合理）的形变模式：

$$
\mathcal{L}_{\mathrm{elastic}} = \int_{\mathbb{R}^3} \Phi(\mathbf{X}) \Psi(\phi_{\mathbf{W}_\theta}(\mathbf{X}, \mathbf{Z})) d\mathbf{X} \tag{6}
$$

手柄变换从分布 $\mathcal{N}(\mu, 0)$ 采样（$\mu=0.1$），且采用**全仿射变换**（含旋转、缩放、剪切）而非仅平移变换——消融实验表明这对强扭曲场景的精度至关重要。

**正交性损失**：强制不同手柄的蒙皮权重在物体内部相互正交，避免模式坍缩和冗余：

$$
\mathcal{L}_{\mathrm{ortho}} = \sum_{i=1}^n \sum_{j=1}^n \int_{\mathbb{R}^3} \Phi(\mathbf{X}) \left( \mathbf{W}_\theta^i(\mathbf{X}) \mathbf{W}_\theta^j(\mathbf{X}) - \delta_{ij} \right)^2 d\mathbf{X} \tag{7}
$$

其中 $\delta_{ij}$ 为克罗内克符号。

### 3.5 关键设计决策

**激活函数选择**：实验表明 ELU 激活比 SIREN 更严格地满足固定边界条件（Fig. 7），这是因为 ELU 在零附近的线性行为有利于权重在边界区域自然衰减至零。

**训练与仿真的能量解耦**：训练阶段使用非线性 Neohookean 能量以引入更强的非线性正则化，而仿真阶段可自由选择任意超弹性材料模型——两者无需一致。消融实验（Fig. 9）证实，移除训练中的 Neohookean 能量或仅采样平移变换均会降低强扭曲下的精度。

**运行时效率**：神经场仅在预处理阶段计算一次，用于获取采样点上的权重及其导数；物理时间步进循环中完全不需要神经网络推理，这是 Simplicits 在保持表示无关性的同时实现交互式仿真速度（每步 51–107 ms）的关键。

## 实验与分析

### 实验设置与基准

Simplicits 在多种几何表示上进行了系统评估，包括显式三角形网格、符号距离函数（SDF）、高斯泼溅（Gaussian Splat）重建体、CT扫描体数据、NeRF生成模型以及点云。所有实验采用统一的物理参数：杨氏模量 $5 \times 10^6\,\text{Pa}$、泊松比 $0.45$、密度 $1000\,\text{kg/m}^3$、时间步长 $0.01\,\text{s}$，共模拟 $300$ 步。训练与推理在相同硬件环境下完成。

对比基准覆盖四类代表性方法：
- **线性四面体FEM**（Corotational）：作为参考真值，用于精度对比；
- **Fast Skinning Eigenmodes**（Benchekroun et al., 2023）：基于网格的减基模拟方法；
- **SPH**（Kugelstadt et al., 2021）：无网格粒子法，5582个粒子；
- **MPM**（Hu et al., 2019）：无网格网格法，5000个粒子，初始网格密度为10。

### 主要性能结果

**训练与推理效率。** 表1汇总了三种典型几何表示的训练与模拟步进时间。三角形网格猴头训练仅需 $180$ 秒，单步模拟 $51$ 毫秒；SDF钥匙训练 $886$ 秒，单步 $107$ 毫秒；高斯泼溅乐高因几何复杂度最高，训练耗时 $5550$ 秒（约 $1.5$ 小时），但单步模拟仍控制在 $74$ 毫秒。值得注意的是，神经网络仅在预处理阶段计算采样点上的蒙皮权重及其导数，物理时间步进循环内无需调用网络，这是运行时效率的关键保证。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2407_09497/figures/008_Table_1.jpg]]
*Table 1: Selected timing results.See supplements for details*

| 对象 | 几何表示 | 训练时间 (s) | 模拟步时间 (ms) |
|------|----------|-------------|----------------|
| 猴头 | 三角形网格 | 180 | 51 |
| 钥匙 | SDF | 886 | 107 |
| 乐高 | 高斯泼溅 | 5550 | 74 |

**悬臂梁对比（Fig. 8）。** 以线性四面体FEM为参考，Simplicits 使用 $9$ 个手柄的结果与 Fast Skinning Eigenmodes（$10$ 个手柄）高度吻合，两者均因减基近似而表现出与全阶FEM相似的数值粗化效应。相比之下，SPH 和 MPM 在相同粒子/网格规模下未能准确复现梁的弯曲与扭转形变。这一结果验证了 Simplicits 在无网格条件下可以达到与网格基减基方法相当的精度，同时显著优于纯无网格粒子/网格法。

**自由度扩展性（Fig. 10）。** 单步模拟时间随自由度数量呈超线性增长，瓶颈在于牛顿法中的稠密线性求解。这是减基方法共有的特性，实际应用中需在手柄数量（精度）与计算成本之间权衡。

### 消融实验

**非线性训练能量与全仿射变换采样（Fig. 9）。** 在顶部固定、底部扭转的方形杆上，以FEM参考解（红色）为基准，完整方法在训练阶段使用非线性Neohookean能量并采样全仿射手柄变换。消融结果表明：移除其中任一组分均会导致精度下降，尤其在接近屈曲的高扭曲状态下退化更为显著。这验证了非线性训练能量和全变换采样对于捕获复杂大形变模态的必要性。

**弹性损失的必要性（Fig. 11）。** 若不使用弹性损失 $\mathcal{L}_{\text{elastic}}$ 训练蒙皮权重，模拟响应严重退化，物体无法产生物理真实的形变。仅依赖正交损失 $\mathcal{L}_{\text{ortho}}$ 不足以使权重编码有意义的力学模态，物理启发的训练能量是 Simplicits 方法的核心支柱。

**手柄数量与MLP容量（Fig. 6）。** 在扭曲杆实验中，增加手柄数量和MLP隐藏层容量可系统性提升精度，逼近全阶FEM参考解。仅使用 $4$ 个手柄时，MLP无法表达复杂形变所需的自由度，表明减基空间的维度与网络表达能力共同决定了模拟上限。

**激活函数选择（Fig. 7）。** 在大变形场景下，ELU激活函数比SIREN更严格地满足固定边界条件。SIREN的周期性激活特性可能导致边界处权重泄漏，而ELU的饱和行为天然抑制了远离物体区域的非零响应，从而提升边界约束的准确性。

### 接触响应与泛化能力

**接触响应（Fig. 12）。** 尽管训练过程从未见过接触场景，Simplicits 在碰撞测试中表现出令人惊讶的响应能力。在相同模态数（$10$）下，基于网格的蒙皮本征模无法捕获接触的尖锐特征，而 Simplicits 的形变模式更加局部化，位移误差（相对于网格包围盒对角线）显著更小。这表明数据无关的物理训练策略学习到的蒙皮权重具有良好的泛化性。

**异质材料与复杂几何（Fig. 14–17）。** Simplicits 成功处理了CT扫描膀胱的非线性接触（Fig. 14）、CT颅脑数据的异质刚度模拟（软脑组织与硬颅骨，Fig. 15）、薄SDF片和线的重力碰撞（Fig. 16），以及由Magic3D生成的NeRF青蛙模拟（Fig. 17）。这些结果展示了方法对多样化几何表示和材料分布的广泛适用性。

**2D图像编辑初步探索（Fig. 18）。** 论文展示了将Simplicits应用于2D图像弹性模拟的初步结果，利用MIDAS单目深度估计进行分割，并通过Adobe Firefly修复遮挡区域，暗示了该方法向图像编辑等视觉计算任务扩展的潜力。

### 失败模式与局限

尽管 Simplicits 在无网格弹性模拟上取得了突破，仍存在以下明确局限：

1. **拓扑不变假设。** 形变基在模拟过程中保持固定，无法处理断裂、切割等拓扑变化。
2. **极端刚度差异。** 对于刚度分布极不均匀的物体，训练可能收敛困难，需要手动验证具体场景。
3. **隐式场渲染。** 从正向形变映射渲染NeRF等隐式体积表示需要额外的逆映射，尚未完全解决。
4. **复杂几何训练成本。** 高斯泼溅乐高训练约需 $1.5$ 小时，对于实时交互式工作流仍有优化空间。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2407_09497/figures/001_Figure.jpg]]

## 方法谱系与知识库定位

### 1. 方法定位：无网格减基模拟的新范式

Simplicits 提出了一种**几何表示无关**的弹性体模拟框架，其核心创新在于将任意标准 3D 几何表示（三角网格、点云、SDF、NeRF、高斯泼溅等）统一归约为**占有率函数（occupancy function）** 查询接口，并在此之上直接训练神经蒙皮权重作为减基形变基。这与现有弹性模拟方法形成了清晰的谱系分化：

- **基于网格的 FEM 方法**（如 Corotational 线性四面体 FEM）：需要显式的四面体网格和连接关系，是物理精度最高的参考基准，但几何预处理流程复杂且无法直接处理新兴的隐式或稀疏表示。
- **基于网格的减基模拟方法**（如 **Fast Skinning Eigenmodes**，Benchekroun et al.，2023）：在显式网格上计算蒙皮本征模，实现了高效降维，但仍依赖网格拓扑，且手柄变换仅限于平移。
- **无网格粒子/网格方法**（如 **SPH**，Kugelstadt et al.，2021；**MPM**，Hu et al.，2019）：摆脱了网格约束，但需要大量粒子或背景网格来维持连续性，且精度受粒子分辨率限制。
- **数据驱动的神经降阶模型**（如 **CROM / LiCROM**，Chen et al. 2023b；Chang et al. 2023）：需要预先模拟的全阶数据来训练降阶基，无法脱离数据生成流程。

Simplicits 在谱系中占据的位置是：**数据无关的、物理启发式的、表示无关的减基模拟**。它既不需要网格，也不需要预模拟数据，仅通过随机手柄变换采样的蒙特卡洛弹性能量最小化即可学习形状感知的形变基。

### 2. 与基线方法的关键差异

下表总结了 Simplicits 与代表性基线方法在核心设计维度上的差异：

| 维度 | 线性四面体 FEM | Fast Skinning Eigenmodes | SPH / MPM | CROM / LiCROM | **Simplicits** |
|------|---------------|-------------------------|-----------|---------------|----------------|
| 几何表示 | 四面体网格 | 三角网格 | 粒子/背景网格 | 四面体网格 | 占有率函数（任意表示） |
| 形变基存储 | 网格节点自由度 | 网格蒙皮权重 | 粒子位移 | 预计算降阶基 | 连续神经场 $W_\theta: \mathbb{R}^3 \to \mathbb{R}^n$ |
| 训练数据需求 | 无 | 无 | 无 | 需要全阶模拟数据 | 无（随机扰动驱动） |
| 手柄变换类型 | N/A | 仅平移 | N/A | N/A | 全仿射变换（3×4 矩阵） |
| 训练能量 | N/A | 线性（Corotational） | N/A | N/A | 非线性 Neohookean |
| 空间积分 | 网格高斯积分 | 网格积分 | 粒子/网格求和 | 网格积分 | 蒙特卡洛采样（固定点） |
| 权重正交性 | N/A | 未强制 | N/A | N/A | 正交损失 $\mathcal{L}_{\text{ortho}}$ 显式约束 |

**关键差异的因果机制：**

1. **占有率接口的设计**使得 Simplicits 能够无缝适配从 CT 扫描体数据（Fig. 14、15）到 NeRF 生成模型（Fig. 17）再到高斯泼溅重建体（Fig. 13）的各类几何表示，这是所有基线方法无法实现的通用性。

2. **全仿射变换采样 + 非线性 Neohookean 训练**是精度提升的关键。消融实验（Fig. 9）表明，移除任一组分都会在强扭曲近屈曲状态下显著恶化精度。这与 Fast Skinning Eigenmodes 的仅平移假设形成对比——后者在纯弯曲场景下足够，但在扭转场景中表达能力不足。

3. **正交损失 $\mathcal{L}_{\text{ortho}}$** 的引入避免了蒙皮权重的模式坍缩，确保每个手柄学到独立的形变模式。这是 Simplicits 在无监督训练条件下仍能产生物理合理响应的关键正则化手段。

### 3. 适用边界与局限

**适用场景：**
- 需要从多种 3D 表示（特别是隐式或稀疏表示）直接进行弹性模拟的应用。
- 对预处理自动化要求高、希望避免网格生成的流程。
- 大形变弹性体模拟，形变基在仿真过程中保持不变。
- 异质材料模拟（如 CT 扫描的脑与颅骨，Fig. 15）。

**已知局限：**

1. **拓扑不变性假设**：当前方法假设形变基在仿真过程中保持不变，无法处理拓扑变化（如断裂、切割）。这是减基方法的内在限制。

2. **刚度分布极不均匀时的训练困难**：对于刚度分布极为复杂且变化剧烈的物体，神经蒙皮权重的训练可能收敛困难。原文将此列为开放挑战。

3. **隐式场的渲染逆映射**：从正向形变映射 $\phi(\mathbf{X}, \mathbf{z})$ 渲染 NeRF 等隐式场需要额外的逆映射，尚未完全解决。这限制了 Simplicits 与 NeRF 等表示的原生端到端集成。

4. **训练时间与几何复杂度相关**：虽然 MLP 规模较小，但对复杂几何（如高斯泼溅乐高）的训练时间可达约 1.5 小时（5550 秒，Table 1），且时间随采样点数量线性增长。

5. **仿真步时的超线性扩展**：由于牛顿法中的稠密线性求解，每步模拟时间随自由度增加呈超线性增长（Fig. 10），这限制了手柄数量的大幅扩展。

### 4. 开放问题与后续方向

1. **高频次级效应与断裂扩展**：如何将 Simplicits 范式扩展到高频次级效应、断裂或铰接连接等更复杂的物理现象，是原文明确提出的开放方向。

2. **可逆形变表征与形变感知渲染**：为原生支持隐式几何的动态渲染，需要设计可逆的形变表征或适配形变的渲染方案。这是 Simplicits 与 NeRF/3DGS 等表示深度集成的关键瓶颈。

3. **跨连续介质现象推广**：将该范式推广至其他连续介质现象（如流体、塑性）的可能性，是方法泛化性的重要探索方向。

4. **2D 图像弹性模拟**：原文展示了 2D 图像弹性模拟的初步结果（Fig. 18），利用单目深度估计和图像修复进行对象分割和遮挡区域填充。这一方向将 Simplicits 的应用边界拓展到了图像编辑领域，但当前仍处于初步阶段，需要手动验证其鲁棒性和泛化能力。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Simplicits_Mesh_Free_Geometry_Agnostic_Elastic_Simulation.pdf]]
