---
title: Learning Physics-Grounded 4D Dynamics with Neural Gaussian Force Fields
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Learning_Physics_Grounded_4D_Dynamics_with_Neural_Gaussian_Force_Fields_00adafdb54c4.pdf
project_link: "https://neuralgaussianforcefield.github.io/"
code_link: null
aliases:
- NGFFN
- LPG4DNGFF
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过神经算子学习显式的对象间力场（包括全局变换力和局部应力场），并利用ODE求解器进行连续时间积分，使模型能够从视觉观察中直接推断物理动态。
primary_logic: 将前馈式3D高斯重建与基于DeepONet的力场预测相结合，通过二阶ODE求解器保障物理一致性，既实现高效推理，又具备空间、时间和组合泛化能力。
claims:
- 在空间泛化测试中，NGFF 的 RMSE 达到 0.082，比最强基线 Pointformer 的 0.096 降低 14.6%，推理速度比 MPM 模拟器快约 100 倍（0.363s vs 39.29s）。
- 在组合泛化（4-6 物体）场景下，NGFF 的 RMSE 为 0.104，远优于 Pointformer 的 0.162 和其他基线。
- 在视频生成任务中，NGFF 在未见背景和视角下的物理真实感（PhysR）显著高于 Cosmos 和 Veo3，例如在 novel-background 上获得 0.56 vs Cosmos 0.26。
- 通过消融实验移除局部变形建模后，各项指标均变差（如 MSE 从 0.00835 升至 0.01466），证实了显式力场建模的关键作用。
---

# Learning Physics-Grounded 4D Dynamics with Neural Gaussian Force Fields

> [!tip] 核心洞察
> 将前馈式3D高斯重建与基于DeepONet的力场预测相结合，通过二阶ODE求解器保障物理一致性，既实现高效推理，又具备空间、时间和组合泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于神经高斯力场的物理驱动4D动力学学习 |
| 英文题名 | Learning Physics-Grounded 4D Dynamics with Neural Gaussian Force Fields |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KxvboPqav6) · [Project](https://neuralgaussianforcefield.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Neural Gaussian Force Field (NGFF) |
| Dataset | GSCollision 动态预测 |

> [!tip] 效果简介
> - GSCollision 动态预测 上，RMSE (空间泛化) 0.082 vs 0.096 (Pointformer) (-0.014)；RMSE (时间泛化) 0.107 vs 0.129 (Pointformer) (-0.022)；RMSE (组合泛化-4物体) 0.104 vs 0.162 (Pointformer) (-0.058)。
> - GSCollision 视频生成 上，PhysR (VLM 评估, 新背景) 0.56 (NGFF-V) vs 0.26 (Cosmos) (+0.30)；PhysR (VLM 评估, 综合) 0.30 (NGFF-V) vs 0.29 (Veo3) (+0.01)。

## 概要

当前视频生成模型在模拟复杂物理交互时，常因缺乏对基本物理定律（如重力、物体永久性）的显式建模而产生违反直觉的动态，而传统物理引擎仿真计算开销极大，难以满足实时交互需求。针对这一瓶颈，本文提出 **Neural Gaussian Force Field (NGFF)**，一种物理驱动的 4D 动力学学习框架。

NGFF 的核心思想是：将前馈式 3D 高斯重建与基于神经算子的显式力场预测相结合，并通过二阶常微分方程（ODE）求解器进行连续时间积分，从而在保障物理一致性的前提下，实现高效的推理与强泛化能力。具体而言，该方法首先将多视角 RGB 输入重建为对象感知的 3D 高斯表示，随后利用基于 DeepONet 的关系图神经算子预测对象间的全局力场与局部应力场，最后通过 ODE 求解器将力场积分为连续的位置与速度轨迹。

在 GSCollision 数据集上的实验表明，NGFF 在动态预测任务中显著优于现有基线：空间泛化场景下 RMSE 达 0.082，相较最强基线 Pointformer 降低 14.6%；推理速度比传统 MPM 模拟器快约 108 倍（0.363s vs 39.29s）。在视频生成任务中，NGFF 在新背景与组合泛化场景下的物理真实感（PhysR）大幅领先 Cosmos 与 Veo3 等大规模生成模型。消融实验进一步证实，显式的局部变形建模是性能提升的关键因素。

当前方法仍存在若干局限：依赖约 10 个视角的多视角输入进行可靠重建，力场预测器在真实世界复杂材料属性上的迁移能力有待验证，且视频生成的视觉保真度与纯生成模型相比尚有一定差距。



### 问题背景：视频生成中的物理一致性危机

当前视频生成模型（如 **Cosmos** (NVIDIA et al., 2025)、**Veo3** (DeepMind, 2025)）在视觉质量上取得了显著进展，但普遍缺乏对物理定律的显式建模。这导致生成的视频中频繁出现违反基本物理法则的现象，包括但不限于：重力方向错误、物体无端穿透、碰撞响应缺失、以及物体永久性（object permanence）被破坏——物体凭空出现或消失。这些物理不一致性严重限制了视频生成模型在需要可靠动态推理的场景（如机器人仿真、物理教育、交互式内容创作）中的实际应用。

### 现有方法的根本缺口

解决物理一致性问题的现有路线主要分为两类，各自存在难以逾越的瓶颈：

**1. 纯数据驱动的动态预测模型。** 以 **Pointformer** (Wu et al., 2024b) 为代表的方法直接在观测数据上学习状态转移函数，缺乏对力场、接触力学等物理机制的归纳偏置。这类模型在训练分布内可以表现良好，但一旦面临空间泛化（新初始位置）、时间泛化（更长预测时域）或组合泛化（更多物体交互）等分布外场景，性能急剧退化——这暴露了其并未真正学到物理规律，而只是拟合了训练数据的统计相关性。

**2. 基于物理引擎的仿真方法。** 以 **VLM-MPM** (Chen et al., 2025) 和 **PhysGen3D** (Chen et al., 2025) 为代表的方法利用物质点法（Material Point Method, MPM）等传统物理求解器进行仿真。尽管物理准确性有保障，但其计算开销极大：单场景仿真动辄数十秒甚至数百秒（如 VLM-MPM 完成 100 步仿真需 39.29 秒），远无法满足实时交互需求。此外，物理引擎依赖显式的材料参数（密度、杨氏模量等）和边界条件，这些参数在真实场景中难以从视觉观测中自动获取。

### 核心动机：从视觉观测中学习物理力场

上述两类方法的根本矛盾在于：纯学习模型缺乏物理结构，而物理引擎缺乏感知接口和计算效率。本文的核心动机正是弥合这一鸿沟——**能否构建一个既能从视觉观测中自动推断物理属性、又能以接近实时速度进行物理一致仿真的统一框架？**

实现这一目标的关键洞察在于：物理交互的本质是力场的时空演化。如果能够从多视角 RGB 图像中重建出带有对象语义的 3D 场景表示，并利用神经算子直接预测对象间的显式力场（包括全局相互作用力和局部接触应力），再通过常微分方程（ODE）求解器进行连续时间积分，就可以在保持物理一致性的同时实现高效推理。这一思路将感知（3D 重建）与动力学（力场预测）统一在一个端到端的可学习框架中，既避免了纯数据驱动方法的物理不可解释性，又绕过了传统物理引擎的计算瓶颈。



## 核心方法与创新机理

NGFF 的核心创新在于将视频预测重新表述为**显式力场学习与常微分方程（ODE）积分**，从而在物理一致性、泛化能力和推理效率三个维度上突破了现有方法的瓶颈。与现有基线相比，NGFF 在两个关键环节上做出了根本性的改变。

### 从状态转移学习到力场算子学习

传统动态预测方法（如 **GCN**（Kipf & Welling, 2017）和 **Pointformer**（Wu et al., 2024b））直接学习从当前状态到下一状态的映射函数 $f_\theta: \mathscr{G}_t \mapsto \mathscr{G}_{t+1}$。这种黑箱式状态转移存在两个根本缺陷：一是缺乏对物理定律的显式约束，导致长时序预测中误差累积和物理违反；二是泛化能力弱，难以适应训练分布之外的物体组合或场景布局。

NGFF 的核心突破在于将预测目标从“状态”改为“力场”。具体而言，系统通过一个基于 **DeepONet** 架构的关系图神经算子，显式预测作用于每个对象的力场。该力场由两个互补分量组成：

- **全局力场** $\mathbf{F}^{\mathrm{global}}$：建模对象间的整体交互力，通过聚合邻居对象的编码状态计算：
  $$\mathbf{F}^{\mathrm{global}}(\mathbf{z}^{q}(t)), \mathbf{F}^{\mathrm{latent}}(\mathbf{z}^{q}(t)) = \sum_{i \in \mathcal{N}(q)} \mathbf{W} \left( f_{\eta}(\mathbf{z}^{i}(t)) \odot f_{\phi}(\mathbf{z}^{q}(t)) \right) + \mathbf{b}$$
  其中查询对象 $q$ 与每个邻居对象 $i$ 的编码状态进行逐元素乘积后线性投影，同时输出全局力向量和潜在力向量。

- **局部应力场** $\mathbf{F}^{\mathrm{local}}$：专门建模接触区域的点级别变形力，是 NGFF 处理刚体-软体交互的关键：
  $${\bf F}^{\mathrm{local}}({\bf z}^{q}(t)) = \Phi \left( {\bf F}^{\mathrm{latent}}({\bf z}^{q}(t)), \mathrm{CAM}, {\bf x}^{q}(t), \dot{\bf x}^{q}(t) \right)$$
  该模块以潜在力向量、接触区域掩模（CAM）以及点云的位置和速度为输入，通过神经网络 $\Phi$ 预测逐点应力。

统一力场 $\mathbf{F}(\mathbf{z}^{q}(t)) = \left( \mathbf{F}^{\mathrm{local}}, \mathbf{F}^{\mathrm{global}} \right)$ 随后被送入二阶 ODE 求解器，通过连续时间积分恢复完整的运动轨迹：
$$\mathbf{z}^{q}(t) = {\mathrm{ODEsolve}} \left( \mathbf{z}^{q}(0), \mathbf{F}, 0, t \right)$$

这一设计带来了三重优势：ODE 积分天然保证轨迹的连续性和平滑性；力场作为中间表示具有明确的物理意义，便于施加约束和进行交互式编辑；算子学习范式使得模型对物体数量和组合具有内在的组合泛化能力。

### 从粒子云到对象中心 3D 高斯表示

在场景表示层面，NGFF 摒弃了传统方法常用的粒子云或隐式神经场，转而采用**对象感知的 3D 高斯表示**，并通过一套前馈式重建流水线实现高效构建。

具体流程包括三个步骤：首先，利用前馈式几何 Transformer 将未标定相机姿态的多视角 RGB 图像直接映射为 3D 高斯场景表示 $\mathcal{G}$，同时估计相机姿态、高斯中心及属性；其次，通过 **SAM2**（Ravi et al., 2025）生成像素级实例掩码，经多数投票反向投影到高斯上，将场景分割为 $K$ 个对象组；最后，利用 **DiffSplat**（Lin et al., 2025a）结合 **Simp3q** 姿态估计对每个对象的 3D 高斯进行补全细化，以缓解遮挡和噪声导致的拓扑不完整性。

这种对象中心表示与力场建模形成了深度耦合：每个对象的 3D 高斯不仅提供了用于力场预测的点云几何信息，还通过可微高斯溅射渲染器直接生成多视角视频帧，实现了从物理仿真到视觉生成的端到端统一。相比之下，**VLM-MPM**（Chen et al., 2025）虽然也采用物理仿真，但依赖传统的物质点法（MPM）求解器，既无法从前馈重建中受益，推理速度也比 NGFF 慢约 108 倍（0.363s vs 39.29s，Table 1）。

消融实验进一步验证了这两个创新点的关键作用：当移除局部应力场预测模块（NGFF w/o deform.）后，空间泛化 RMSE 从 0.082 恶化至 0.110，时间泛化 RMSE 从 0.107 升至 0.127（Table 1 & Table A4），证实了显式力场建模——尤其是局部变形分量——对物理一致性是不可或缺的。



NGFF 将 4D 视频预测形式化为学习**神经力场**，该力场控制 3D 高斯场景表征的时间演化。整个框架由两个互补组件构成：**前馈式重建**将多视角 RGB 观测转换为对象感知的 3D 高斯，以及**神经动力学预测**通过 ODE 求解器模拟物理上合理的动态。

### 前馈式对象中心重建

给定未标定相机姿态的多视角 RGB 图像，NGFF 首先通过前馈式几何 Transformer 将场景重建为 3D 高斯表示。随后，利用 SAM2 生成像素级实例掩码，通过多数投票机制将掩码反投影到高斯上，将场景划分为 K 个对象组。为处理遮挡和噪声，系统使用 DiffSplat 结合 Simp3q 姿态估计对每个对象的高斯表示进行细化，增强其拓扑完备性。

### 基于 DeepONet 的力场预测

细化后的对象高斯被编码为高维特征，送入基于 DeepONet 的关系图神经算子。该算子预测两类力场：
- **全局力场**：通过将查询对象与邻居对象的编码状态进行逐元素乘积和线性投影，计算作用于对象质心的合力；
- **局部应力场**：基于全局力场计算中产生的潜在力向量、接触区域掩码以及点云位置和速度，由神经网络 Φ 预测点级别的应力场，实现对软体变形的显式建模。

统一力场由局部和全局力组合而成，直接决定对象的加速度。

### ODE 求解与渲染

预测的力场通过二阶 ODE 求解器（显式欧拉或自适应步长）进行连续时间积分，从初始状态恢复位置和速度轨迹。进化后的 3D 高斯通过可微高斯溅射渲染器生成多视角且物理一致的视频帧。整个流程支持迭代预测与渲染，在保持物理一致性的同时实现新视角合成、新背景合成以及力提示的交互式生成。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_KxvboPqav6/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of NGFF. Given unposed RGB inputs, our approach first reconstructs the scene into object-aware 3D Gaussians through feed-forward prediction, followed by segmentation and refinement to handle occlusions and noise. The refined Gaussians are encoded into high-dimensional features and processed by a DeepONet-based neural operator to predict object-centric force fields. These force fields are integrated through ODE solvers to simulate realistic dynamics, enabling iterative prediction and rendering of future scene states with maintained physical consistency*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_KxvboPqav6/figures/001_Figure_1.jpg]]
*Figure 1: Capabilities of NGFF. NGFF is a physics-grounded video prediction framework that unifies perception and dynamics to model complex interactions and synthesize 4D videos. Built on Gaussian representations and force fields, it enables novel-view and novel-background synthesis as well as force-prompted interactive generation (Section 4.3). Moreover, NGFF achieves strong spatial and temporal generalization in dynamic prediction (Section 4.2) and can be effectively adapted to real-world scenarios (Section 4.4)*



NGFF 将 4D 视频预测形式化为学习控制 3D 高斯场景表示时间演化的 **神经力场 (Neural Force Fields, NFFs)**。其核心架构由两个互补组件构成：将多视角 RGB 观测转换为对象感知 3D 高斯的前馈重建模块，以及通过 ODE 求解器进行物理一致动态模拟的神经动力学预测模块。

### 3.1 对象中心的前馈重建

该模块将未标定相机姿态的多视角图像转换为对象级 3D 高斯表示。首先通过前馈几何 Transformer（Wang et al., 2025a;b）预测场景的 3D 高斯属性与相机姿态。随后利用 **SAM2**（Ravi et al., 2025）生成像素级实例掩码，通过多数投票机制将掩码反投影到高斯上，将场景分割为 $K$ 个对象组。为处理遮挡和噪声，采用 **DiffSplat**（Lin et al., 2025a）结合 **Simp3q** 姿态估计对对象表示进行细化，增强拓扑完整性。

### 3.2 基于 DeepONet 的力场预测网络

动力学预测的核心是学习显式的对象间力场。对于查询对象 $q$，其状态 $\mathbf{z}^{q}(t)$ 包含所有组成粒子的位置 $\mathbf{x}^{q}(t)$ 和速度 $\dot{\mathbf{x}}^{q}(t)$。力场预测分为全局交互力与局部应力两个分支。

**全局力场与潜在力场预测**采用基于 DeepONet 的关系图神经算子，聚合邻居对象 $i \in \mathcal{N}(q)$ 的交互信息：

$$\mathbf{F}^{\mathrm{global}}(\mathbf{z}^{q}(t)), \mathbf{F}^{\mathrm{latent}}(\mathbf{z}^{q}(t)) = \sum_{i \in \mathcal{N}(q)} \mathbf{W} \left( f_{\eta}(\mathbf{z}^{i}(t)) \odot f_{\phi}(\mathbf{z}^{q}(t)) \right) + \mathbf{b}$$

其中 $f_{\eta}$ 和 $f_{\phi}$ 分别对邻居对象与查询对象的状态进行编码，$\odot$ 表示逐元素乘积，$\mathbf{W}$ 和 $\mathbf{b}$ 为可学习的投影参数。该操作同时输出作用于对象质心的全局力 $\mathbf{F}^{\mathrm{global}}$ 和用于后续局部建模的潜在力向量 $\mathbf{F}^{\mathrm{latent}}$。

**局部应力场预测**针对可变形物体的接触区域进行点级建模：

$${\bf F}^{\mathrm{local}}({\bf z}^{q}(t)) = \Phi \left( {\bf F}^{\mathrm{latent}}({\bf z}^{q}(t)), \mathrm{CAM}, {\bf x}^{q}(t), \dot{\bf x}^{q}(t) \right)$$

其中 $\Phi$ 为神经网络，$\mathrm{CAM}$ 为接触区域掩码（Contact Area Mask），指示物体间发生碰撞的粒子区域。该模块以潜在力、接触掩码及当前点云状态为输入，预测每个粒子的局部应力场。

**统一力场**将全局与局部力组合为最终力场：

$$\mathbf{F}(\mathbf{z}^{q}(t)) = \left( \mathbf{F}^{\mathrm{local}}, \mathbf{F}^{\mathrm{global}} \right)$$

### 3.3 ODE 轨迹解码

预测的力场通过二阶 ODE 求解器进行连续时间积分，恢复物体在任意时刻的状态：

$$\mathbf{z}^{q}(t) = {\mathrm{ODEsolve}} \left( \mathbf{z}^{q}(0), \mathbf{F}, 0, t \right)$$

具体而言，位置和速度通过积分力场得到：

$$\mathbf{s}(t) = \mathbf{s}(0) + \int_{0}^{t} {\dot{\mathbf{s}}}(t) dt, \quad {\dot{\mathbf{s}}}(t) = {\dot{\mathbf{s}}}(0) + \int_{0}^{t} \mathbf{F}(\mathbf{z}^{q}(t)) dt$$

其中 $\mathbf{s}(t)$ 和 $\dot{\mathbf{s}}(t)$ 分别表示位置和速度状态。ODE 求解器支持显式欧拉法或自适应步长方法，确保长时间推演下的数值稳定性。

### 3.4 训练策略

NGFF 采用两阶段训练。前馈重建模块在 **WildRGBD** 数据集上微调预训练的 $\pi^3$ 参数；神经动力学模拟器在合成 **MPM（Material Point Method）** 仿真数据上独立训练，优化均方误差（MSE）损失。这种解耦设计使得动力学模块能够专注于学习物理规律，而不受重建误差的干扰。



## 实验与关键发现

### 核心实验设置

NGFF 的评估围绕一个核心命题展开：**显式力场建模能否在动态预测与视频生成任务中同时实现物理准确性、泛化能力和推理效率**？为此，作者构建了大规模合成数据集 **GSCollision**（3200 场景，64 万视频，4.25 TB），覆盖从软体（布料、绳索）到刚体（碗、手机）的 10 类日常物体，并通过材料密度与杨氏模量的参数空间系统采样以保证物理多样性（Figure 3）。评测维度被精细划分为四种泛化场景：**空间泛化**（新初始位置）、**时间泛化**（更长 rollout）、**组合泛化**（4-6 物体场景）和**新视角/新背景**合成。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_KxvboPqav6/figures/003_Figure_3.jpg]]
*Figure 3: GSCollision dataset. (a) Distribution of 10 representative objects characterized by density and material hardness (Young’s modulus, log scale). The parameter space spans from soft, lightweight materials (e.g., cloth, rope, pillow) in the lower-left region to rigid, dense objects (e.g., bowl, phone) in the upper-right, providing comprehensive coverage of everyday material properties. (b) Dataset composition totaling 4.25 TB across 3,200 scenes and 640k videos. The pie chart shows storage distribution among training and test splits, multi-view initial scene captures, and auxiliary data files. (c) Representative frame gallery across evaluation scenarios: training sequences, longer temporal rol...*

所有动态预测基线（**GCN**、**Pointformer**、**VLM-MPM**）均在同一数据集上按原文配置训练；视频生成基线（**Cosmos**、**Veo3**、**PhysGen3D**）因闭源且不可微调，采用 VLM 评估与人工评估相结合的方案。推理时间统一在单块 NVIDIA H100 80G GPU 上测量，确保对比公平。

### 动态预测：精度、泛化与效率的三重优势

Table 1 汇总了动态预测的核心结果，NGFF 在所有泛化维度上一致超越最强基线 **Pointformer**（Wu et al., 2024b）：

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_KxvboPqav6/figures/004_Table_1.jpg]]
*Table 1: Dynamic prediction performance across generalization scenarios. We evaluate models using four key metrics: Root Mean Squared Error (RMSE) between predicted and ground-truth trajectories for positional accuracy, Final Position Error (FPE) for long-term stability, correlation coefficient R for temporal consistency, and average inference time over 100 simulation steps for computational efficiency. Arrows indicate whether higher (Ò) or lower (Ó) values represent better performance. The ablation study NGFF w/o deform. demonstrates our framework’s performance when soft body deformation modeling is disabled, isolating the contribution of local stress field prediction*

- **空间泛化**：NGFF 的 RMSE 降至 **0.082**，较 Pointformer 的 0.096 降低 **14.6%**；FPE（最终位置误差）从 0.149 降至 **0.124**，表明长期稳定性显著提升。
- **时间泛化**：在更长 rollout 下，NGFF 的 RMSE 为 **0.107**（Pointformer 0.129），FPE 为 **0.164**（Pointformer 0.205），证明力场建模有效抑制了误差累积。
- **组合泛化**：当场景物体数从训练时的 3 个增至 4-6 个时，NGFF 的 RMSE 仅为 **0.104**，而 Pointformer 高达 0.162——差距扩大至 **0.058**，凸显了基于物理交互算子的组合泛化能力。

推理效率方面，NGFF 完成 100 步仿真仅需 **0.363 秒**，而基于传统 MPM 物理引擎的 **VLM-MPM**（Chen et al., 2025）需 39.29 秒，加速约 **108 倍**。这一速度优势源于 NGFF 将昂贵的 PDE 求解替换为神经算子前馈预测 + ODE 积分，使实时交互成为可能。

定性对比（Figure 4）进一步揭示了基线方法的典型失效模式：GCN 在长序列中出现轨迹漂移，Pointformer 在刚-软体交互中产生非物理形变，传统 MPM 则在复杂接触下计算失稳。NGFF 则始终保持物理一致的轨迹与逼真的变形模式。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_KxvboPqav6/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison of dynamic prediction methods. Temporal progression of multi-object scenes demonstrating NGFF’s superior trajectory prediction compared to baseline approaches. Each row shows predictions from a different method (NGFF, GCN, Pointformer, Traditional MPM) across identical initial conditions, with time advancing from left to right. The scenarios feature complex, rigid-soft body interactions, including deformable objects (pillows, ropes) interacting with rigid bodies (balls, containers) under gravitational and contact forces. NGFF maintains physically consistent trajectories and realistic deformation patterns throughout extended rollouts, while baseline methods exhibit dri...*

### 视频生成：物理真实感的质变

Table 2 展示了视频生成任务上的 VLM 评估结果。核心指标 **PhysR**（物理真实感）衡量生成视频是否符合物理定律：

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_KxvboPqav6/figures/007_Table_2.jpg]]
*Table 2: Video generation performance across generalization scenarios. Performance metrics (higher is better) evaluated on compositional (Comp.), novel-background (NB), novel-view (NV), and comprehensive (All) splits testing different aspects of generalization capability. The comprehensive split combines all three generalization challenges. Note that Cosmos performs standard novel-view generalization using existing viewpoints, while NGFF tackles the more challenging novel-view synthesis task requiring generation from entirely unseen camera perspectives*

- 在**新背景**（NB）场景下，NGFF-V 的 PhysR 达到 **0.56**，远超 Cosmos 的 0.26 和 Veo3 的 0.27，提升超过一倍。
- 在**综合**（All）场景下，NGFF-V 的 PhysR 为 **0.30**，略优于 Veo3 的 0.29，但显著高于 Cosmos（0.22）和 PhysGen3D（0.18）。

值得注意的是，NGFF-V 在视觉真实感（PhotoR）上为 0.35，低于纯生成模型 Veo3（0.42）和 Cosmos（0.43），反映出当前前馈式 3D 重建精度对渲染质量的制约——这是精度与视觉珍实度之间的固有权衡。

交互式生成实验（Figure 5）提供了更直观的证据：当施加外力扰动（如向上拉枕头、向左拉布料），NGFF 产生物理一致的连锁反应，而 Cosmos 和 Veo3 则生成违反物理约束的非真实动态（如物体悬浮、碰撞缺失）。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_KxvboPqav6/figures/006_Figure_5.jpg]]
*Figure 5: Interactive generation under external perturbations. Red arrows indicate applied forces. Left: upward force on fallen pillow; Right: leftward force on cloth affecting ball motion. NGFF produces physically consistent responses to interventions, while baseline methods (Cosmos, Veo3) generate unrealistic dynamics that violate physical constraints. Baseline prompts: Cosmos—“modify the pillow...to show a significant, sudden external force stretching it upward into the air, with interactions with panda and miku”; Veo3—“modify the clothing...to show a significant, sudden external force stretching it leftward.”*

### 消融实验：局部应力场的决定性作用

移除局部变形建模（NGFF w/o deform.）的消融实验（Table A4）证实了显式力场建模的关键贡献：

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_KxvboPqav6/figures/018_Table.jpg]]
*Table: A4: Ablation results of NGFF and NGFF without deformation across different generalization settings. Arrows indicate whether higher (Ò) or lower (Ó) values are better. Table A5: Inference time for different video generation methods Times are measured on a single NVIDIA H100 80G GPU*

- 空间泛化 RMSE 从 0.082 升至 **0.110**（退化 34%），FPE 从 0.124 升至 **0.174**（退化 40%）。
- 组合泛化场景下退化更为严重：RMSE 从 0.104 升至 **0.157**，FPE 从 0.157 升至 **0.247**。

这表明**局部应力场预测**（StressNet）是处理接触区域复杂形变的核心组件，尤其在刚-软体交互和多物体组合场景中不可或缺。全局力场（Interaction Network）单独不足以捕捉细粒度的接触力学行为。

### 推理效率与精度权衡

Table A5 对比了不同视频生成方法的推理时间：NGFF-V 生成 3 物体场景约需 **37 秒**，远快于 PhysGen3D（400 秒），但慢于纯生成模型 Cosmos（20 秒）。这一差距主要来自前馈重建和 ODE 积分的计算开销，但换来了物理一致性的质变——在需要可信物理交互的应用场景中，这是可接受的权衡。

### 真实世界验证

真实世界实验（Figure 7）使用 10 台 Pocket 3 相机拍摄物体下落场景，NGFF 展现了与真实动力学高度一致的预测，而视频生成模型则出现物体幻化、重力异常和碰撞错误等典型失效。这验证了物理先验在弥合合成-真实域差距中的关键作用，但也暴露了当前方法对多视角输入的依赖——单视角或稀疏视角下的重建质量仍是瓶颈。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_KxvboPqav6/figures/009_Figure_7.jpg]]
*Figure 7: Real-world validation. (a) Multi-view capture setup using 10 Pocket 3 cameras recording object dropping experiments. (b) Initial multi-view frames from real-world scenes. (c) Model comparison against ground truth. While video generation models produce visually appealing results, they exhibit physical inconsistencies including object hallucination, unrealistic gravity, and incorrect collision dynamics. NGFF demonstrates superior physical accuracy and consistency with real-world dynamics*

### 失败模式与局限

综合实验证据，NGFF 的主要失效模式可归纳为三类：
1. **重建误差传播**：前馈式 3D 重建在遮挡严重或纹理稀疏区域的误差会直接污染力场预测输入，导致轨迹偏差。
2. **材料属性外推不足**：力场预测器在训练时依赖合成 MPM 数据，对真实世界中不均匀密度、复杂摩擦等材料属性的泛化有限。
3. **视觉珍实度瓶颈**：与大规模生成模型相比，基于高斯溅射的渲染在纹理细节和光照一致性上仍有差距，尤其在复杂背景替换场景中明显。

这些局限指向了未来工作的关键方向：稀疏视角重建、神经力场与生成先验的融合，以及向断裂、流体等更复杂物理现象的扩展。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_KxvboPqav6/figures/008_Figure_6.jpg]]
*Figure 6: Video generation quality comparison. Temporal sequences comparing NGFF against video generation baselines across diverse scenarios. NGFF maintains coherent object shapes, physically plausible interactions, and consistent backgrounds throughout generated sequences, while baseline methods exhibit shape distortions, unrealistic dynamics, and scene inconsistencies that violate physical constraints*



## 定位与知识库关联

### 1. 方法沿革与脉络

NGFF 的核心贡献在于将**前馈式 3D 场景重建**与**基于神经算子的力场学习**进行系统整合，形成了一条区别于传统物理仿真和纯生成模型的 4D 动态建模路径。其方法谱系可从三个维度追溯：

**场景表示维度**。NGFF 继承并发展了 3D 高斯溅射（3D Gaussian Splatting）的显式场景表示范式，但区别于需要逐场景优化的原始方案，它采用前馈式几何 Transformer（Wang et al., 2025a;b）实现从多视角 RGB 到 3D 高斯的单次推理重建。在此基础上，通过 SAM2（Ravi et al., 2025）实例分割和 DiffSplat（Lin et al., 2025a）补全，将场景进一步分解为对象中心的高斯群组，这一“重建-分割-补全”流水线使其在表示层面即具备了对象级语义结构化能力。

**动力学建模维度**。传统方法可归为两类：一类以 GCN（Kipf & Welling, 2017）和 Pointformer（Wu et al., 2024b）为代表，直接学习状态转移函数 $f_\theta: \mathscr{G}_t \to \mathscr{G}_{t+1}$，缺乏对物理机制的显式建模；另一类以 VLM-MPM（Chen et al., 2025）和 PhysGen3D（Chen et al., 2025）为代表，依赖物质点法（MPM）等传统物理引擎进行仿真，虽物理精度高，但计算开销巨大（100 步推理需 39.29s）。NGFF 的关键创新在于引入 DeepONet 架构的关系图神经算子，显式预测对象间的**全局力场**和接触区域的**局部应力场**，再通过二阶 ODE 求解器进行连续时间积分——这实质上将动力学预测重新表述为“力场算子学习 + ODE 轨迹解码”的物理先验注入范式。

**视频生成维度**。与 Cosmos（NVIDIA et al., 2025）和 Veo3（DeepMind, 2025）等大规模扩散/自回归生成模型不同，NGFF 不直接生成像素，而是通过物理驱动的 3D 高斯演化，再经可微高斯溅射渲染生成多视角视频。这一设计使其天然具备新视角合成和物理一致性保障，但也导致其视觉珍实度受限于前馈重建的精度。

### 2. 与基线方法的关系定位

从 Table 1 和 Table 2 的全面对比可以明确 NGFF 在方法谱系中的坐标：

- **相对于纯学习式动态预测器（GCN, Pointformer）**：NGFF 在所有泛化维度上均显著占优。以空间泛化 RMSE 为例，NGFF 的 0.082 较 Pointformer 的 0.096 降低 14.6%；在更具挑战性的组合泛化场景（4-6 物体）中，NGFF 的 RMSE 为 0.104，远优于 Pointformer 的 0.162。这证明显式力场建模和 ODE 积分带来的物理归纳偏置，在分布外泛化中具有决定性优势。

- **相对于物理引擎仿真器（VLM-MPM）**：NGFF 在保持相近物理精度的同时，实现了约 108 倍的推理加速（0.363s vs 39.29s/100 步）。这一定量对比直接验证了“神经力场 + ODE 求解器”替代传统 MPM 迭代求解的可行性。

- **相对于大规模视频生成模型（Cosmos, Veo3）**：在物理真实感（PhysR）评估中，NGFF 在未见背景场景下达到 0.56，而 Cosmos 仅为 0.26；在综合评估中 NGFF 以 0.30 略优于 Veo3 的 0.29。但 NGFF 的视觉真实感（PhotoR）为 0.35，低于纯生成模型（Cosmos 0.61, Veo3 0.67），这揭示了物理约束与视觉珍实度之间的固有张力。

### 3. 适用边界与关键约束

NGFF 的能力边界受以下因素制约：

**输入依赖性**。当前方法需要约 10 个视角的多视图输入才能可靠完成 3D 高斯重建和对象分割。在单视角或稀疏视角条件下，前馈重建的质量下降会通过“重建误差→力场预测误差→轨迹漂移”的级联效应影响最终动态预测精度。这一约束限制了其在非受控场景中的直接部署。

**材料属性覆盖**。力场预测器在合成 MPM 数据上训练，虽覆盖了从软质轻量（布料、绳索）到刚性高密度（碗、手机）的 10 类代表性物体（Figure 3a），但对不均匀密度分布、复杂摩擦系数、各向异性材料等真实世界物理属性的泛化能力尚未验证。

**变形建模的精度-速度权衡**。消融实验（Table A4）表明，移除局部应力场预测后，空间 RMSE 从 0.082 升至 0.110，证实变形建模对精度的关键贡献。但完整的 NGFF-V 在 3 物体场景下仍需 37s（Table A5），虽远快于 PhysGen3D 的 400s，却慢于 Cosmos 的 20s，在实时交互场景中仍有优化空间。

### 4. 局限与开放问题

基于上述分析，NGFF 当前面临以下局限和开放挑战：

**稀疏观测下的鲁棒重建**。如何从单张图像或极稀疏视角实现可靠的 3D 重建和物理推理，是该方法走向实用化的核心瓶颈。可能的路径包括引入单目几何先验或与预训练 3D 生成模型协同。

**物理先验与生成先验的融合**。NGFF 在物理一致性上显著优于纯生成模型，但在视觉珍实度上存在差距。如何将学到的力场模型作为物理约束注入扩散生成过程，或利用生成先验补全 3D 重建的细节缺失，是提升综合质量的关键方向。

**复杂物理现象的扩展**。当前力场模型聚焦于刚体-软体碰撞和接触变形，尚未涉及断裂、塑性变形、流体交互等更具挑战性的物理现象。扩展到这些场景需要重新设计力场表示（如引入拓扑变化建模）和训练数据生成策略。

**真实世界迁移**。Figure 7 展示了在受控真实场景中的初步验证，但训练数据完全来自合成 MPM 仿真，sim-to-real gap 在复杂材质和不规则几何体上的表现尚需系统评估。领域自适应或少量真实数据微调可能是可行的缓解方案。



## 原文 PDF

![[paperPDFs/ICLR_2026/Learning_Physics_Grounded_4D_Dynamics_with_Neural_Gaussian_Force_Fields_00adafdb54c4.pdf]]
