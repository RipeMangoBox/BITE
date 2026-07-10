---
title: "AnyLift: Lifting Unseen In-the-Wild Human Motions via Camera-Aware 2D Diffusion"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AnyLift_Scaling_Motion_Reconstruction_from_Internet_Videos_via_2D_Diffusion.pdf
aliases:
- AnyLift
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入相机轨迹与极线条件化的2D运动扩散模型，并结合混合数据源训练策略（真实视频关键点+现成估计器反投影的局部姿态），使模型能在有限视角覆盖的互联网视频上学到多视图一致的2D运动先验，进而实现世界坐标3D重建。
primary_logic: 通过从海量互联网视频中学习的2D运动先验，利用相机轨迹和极线几何约束，可以在无3D监督的情况下，端到端地恢复动态相机下的全局3D人体运动与人物交互。
claims:
- 在AIST++静态和动态相机设置下，AnyLift的根平移误差（T_root）与关节误差（MPJPE）均优于所有基线，尤其在动态相机下明显超过MVLift。
- 在新收集的体操和武术互联网视频上，AnyLift在2D关键点误差和FID上显著优于SMPLify、WHAM等基线，证明了在稀有动作上的泛化能力。
- 消融实验表明，移除混合数据源训练（即仅用视频2D关键点）会导致所有指标大幅下降，验证了该策略的关键作用。
- 在BEHAVE人物交互基准上，AnyLift在物体平移误差和平均关节误差上大幅超过SMPLify和VisTracker，展示了统一框架对HOI的有效性。
---

# AnyLift: Lifting Unseen In-the-Wild Human Motions via Camera-Aware 2D Diffusion

> [!tip] 核心洞察
> 通过从海量互联网视频中学习的2D运动先验，利用相机轨迹和极线几何约束，可以在无3D监督的情况下，端到端地恢复动态相机下的全局3D人体运动与人物交互。

| 字段 | 内容 |
|------|------|
| 中文题名 | AnyLift：通过相机感知的 2D 扩散提升未见过的野外人体运动 |
| 英文题名 | AnyLift: Lifting Unseen In-the-Wild Human Motions via Camera-Aware 2D Diffusion |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2604.17818) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | AnyLift |
| Dataset | AIST++, Gymnastics, BEHAVE (static) - Box |

> [!tip] 效果简介
> - AIST++ (static) 上，MPJPE (mm) 108.0 vs MVLift 110.7 (-2.7)；T_root (mm) 64.9 vs MVLift 67.6 (-2.7)。
> - AIST++ (dynamic) 上，MPJPE (mm) 109.3 vs MVLift 122.1 (-12.8)。
> - Gymnastics (Internet) 上，J_2D^C (px) 11.4 vs SMPLify 16.0 (-4.6)。

## 概述

从动态摄像机拍摄的单目视频中恢复世界坐标系下的全局一致三维人体运动，是计算机视觉领域的长期难题。现有方法在静态摄像机假设下表现尚可，但面对真实互联网视频中普遍存在的摄像机运动、稀有动作（如体操、武术）以及人物交互（HOI）场景时，泛化能力严重不足——根轨迹漂移、局部姿态失真、自穿透等伪影频发。

AnyLift 提出了一种统一的两阶段框架，核心思路是：**利用从海量互联网视频中学习的二维运动先验，结合摄像机轨迹与极线几何约束，在无三维监督的条件下端到端地恢复动态相机下的全局三维人体运动与人物交互。** 具体而言，第一阶段通过相机感知的单视图二维运动扩散模型合成多视图训练数据，第二阶段训练多视图二维运动扩散模型，从单目输入直接生成相机条件下多视图一致的二维关键点序列，进而通过多视图反投影优化恢复世界坐标系下的三维姿态和轨迹。

在方法定位上，AnyLift 区别于基于重投影优化的传统方法 **SMPLify**（Bogo et al., ECCV 2016）和依赖 AMASS 数据训练的 **WHAM**（Shin et al., CVPR 2024），也超越了仅适用于静态相机的多视图扩散方法 **MVLift**。其关键创新在于两个“因果旋钮”：（1）将摄像机轨迹和极线引入二维扩散模型的条件输入，使模型能够在动态相机下学习多视图一致性；（2）采用混合数据源训练策略——将真实视频二维关键点与现成估计器（GVHMR）反投影的局部二维姿态相结合，并丢弃根轨迹偏差，有效缓解了互联网视频视角覆盖有限的问题。

实验表明，AnyLift 在 AIST++ 基准上，动态相机设置下的根平移误差（T_root）和平均关节误差（MPJPE）均显著优于所有基线，其中 MPJPE 较 MVLift 降低 12.8 mm（Table 1）。在新收集的体操和武术互联网视频上，二维关键点误差和 FID 指标大幅领先 SMPLify、WHAM 等方法，验证了其对稀有动作的泛化能力（Table 2, Table 5）。在 BEHAVE 人物交互基准上，物体平移误差和关节误差同样大幅超越 VisTracker 和 SMPLify（Table 4），展示了统一框架对 HOI 的有效性。消融实验进一步证实，移除混合数据源训练会导致所有指标显著下降（Table 5），人类偏好研究也表明参与者更倾向完整模型的重建结果（Table 3）。

AnyLift 仍存在若干局限：需为每个动作类别单独训练单视图扩散模型，跨类别泛化受限；HOI 重建依赖手工设计的物体关键点，且每种物体类别需独立训练；严重遮挡或极端相机运动下，二维关键点提取和相机运动估计可能失效。这些开放问题指向未来方向——零样本跨类别重建、摆脱物体模板依赖，以及向多人多物交互场景的扩展。

## 背景与动机

从单目视频中恢复全局一致的3D人体运动是计算机视觉领域的长期挑战。当视频由动态摄像机拍摄时，问题进一步复杂化：人体在图像平面的表观运动同时包含自身动作和摄像机运动两个分量，解耦二者需要有效的几何约束与运动先验。

现有方法可大致分为两类。基于优化的方法，如 **SMPLify**（Bogo et al., ECCV 2016），通过2D重投影误差拟合参数化人体模型，但缺乏对世界坐标运动的约束，难以恢复合理的全局轨迹。基于学习的方法，如 **WHAM**（Shin et al., CVPR 2024）和 **GVHMR**（Shen et al., SIGGRAPH Asia 2024），利用AMASS等大规模运动捕捉数据训练回归网络，在常规动作上表现良好，但对稀有动作类别（如体操、武术）的泛化能力严重不足——这些动作在现有3D数据集中几乎不存在。

**MVLift** 率先将2D扩散模型引入3D人体运动重建，通过学习多视图2D关键点的一致性先验来提升静态摄像机下的重建质量。然而，该方法假定摄像机固定，无法处理动态摄像机场景，且训练数据仅来自视频提取的2D关键点，受限于互联网视频有限的视角覆盖。

**核心瓶颈**在于：在动态摄像机下，现有方法难以恢复世界坐标下全局一致的3D人体运动，尤其对于稀有动作以及人物交互（HOI）场景，泛化能力严重不足。从野外视频重建世界坐标系下的人体-物体交互，更是一个尚未解决的开放问题。

**AnyLift** 的动机正是突破上述局限：利用海量互联网视频中隐含的2D运动先验，结合摄像机轨迹与极线几何约束，实现在无3D监督条件下端到端地恢复动态摄像机下的全局3D人体运动与人物交互。

## 核心创新

AnyLift 的核心创新在于将**相机轨迹与极线几何约束**注入 2D 运动扩散模型，使系统能够从动态摄像机拍摄的单目视频中恢复世界坐标下的全局一致 3D 人体运动与人物交互。相较于现有方法，其关键改进体现在以下四个 changed slots 上。

### 1. 相机感知的 2D 扩散条件化

现有基于 2D 扩散的 3D 运动提升方法（如 **MVLift**）假设静态相机，无法处理动态摄像机下根轨迹与局部姿态的耦合歧义。AnyLift 将**相机轨迹 C 和极线 L** 作为单视图与多视图 2D 扩散模型的显式条件输入，使去噪网络学会在给定相机运动下生成几何一致的 2D 关键点序列。训练损失为 L1 重建损失：

$$\mathcal{L} = \mathbb{E}_{\mathbf{X}_0, n} \| \mathbf{X}_0 - \mathbf{X}_\theta(\mathbf{X}_n, n, \mathbf{C}, \mathbf{L}) \|_1$$

该设计使得模型能够区分“人物自身运动”与“相机运动引起的表观位移”，从而在动态相机设置下将根平移误差（T_root）从 MVLift 的 67.6 mm 降至 64.9 mm，MPJPE 从 122.1 mm 降至 109.3 mm（Table 1, dynamic）。

### 2. 混合数据源训练策略

互联网视频的视点分布往往存在严重偏置（如体操视频中人物多面向相机，见 Figure S.1），仅用视频提取的 2D 关键点训练会导致视角覆盖不足。AnyLift 提出**混合数据源训练**：将真实视频的全局 2D 关键点序列与现成估计器（**GVHMR**, Shen et al., SIGGRAPH Asia 2024）反投影的**局部 2D 姿态**结合，并采用分解表示——对反投影姿态仅保留髋关节以外的局部关键点（掩码 M），丢弃不可靠的根轨迹偏差：

$$\mathcal{L}^{\mathrm{proj}} = \mathbb{E}_{\mathbf{X}_0, n} \| \mathbf{M} \odot \mathbf{X}_0 - \mathbf{M} \odot \mathbf{X}_\theta(\mathbf{X}_n^{\mathrm{proj}}, n, \mathbf{C}, \mathbf{L}) \|_1$$

消融实验（Table 5）表明，移除该策略后所有互联网视频指标（J_2D、J_2D^C、FID）均大幅下降，人类偏好研究也显示参与者以 65.6% vs. 34.4% 的比例倾向完整模型（Table 3），验证了视角多样性对泛化能力的关键作用。

### 3. 高效的多视图一致性损失

在通过分数蒸馏采样（SDS）合成多视图训练数据时，MVLift 对所有视图对施加极线匹配损失，计算开销随视图数平方增长。AnyLift **仅对相邻视图和输入视图对施加线匹配损失**：

$$\mathcal{L}_{\mathrm{line}}^{u v} = \sum_{t=1}^{T} \big\langle \mathbf{L}_t^{u v}, (\mathbf{X}_{v,t}^{\mathrm{g}}, \mathbf{1}) \big\rangle$$

这一简化在保持多视图几何一致性的同时显著降低计算负担，使 SDS 优化过程可扩展至更多视图。

### 4. 统一的人物交互重建框架

现有方法（如 **SMPLify**, Bogo et al., ECCV 2016; **VisTracker**, Xie et al., CVPR 2023）将人体重建与物体重建分离处理，难以保证交互的物理一致性。AnyLift 将 HOI 重建纳入统一框架：多视图扩散模型同时输出人体与物体关键点，3D 优化阶段联合优化 SMPL 人体参数与物体位姿（6D 旋转 r_t、平移 t_t、全局尺度 s），并通过物体拟合损失与平滑正则项保证时序连贯：

$$\mathcal{L}_{\mathrm{fit}}^{\mathrm{obj}} = \frac{1}{TM} \sum_{t=1}^{T} \sum_{i=1}^{M} m_i \| s \operatorname{Rot}(\mathbf{r}_t) \mathbf{p}_i + \mathbf{t}_t - \mathbf{q}_{i,t} \|_2$$

在 BEHAVE 基准上，AnyLift 的 Box 类别 MPJPE 仅为 42.68 mm，而 SMPLify 为 114.56 mm；物体平移误差也大幅低于 VisTracker（95.38 vs. 143.59，Table 4），证明统一框架在 HOI 场景下的显著优势。

**创新总结**：AnyLift 的四项 changed slots 形成了一条完整因果链——相机条件化解耦相机运动与人体运动，混合训练弥补视点偏置，高效一致性损失使多视图合成可行，统一 HOI 框架将人体与物体的几何约束内化于同一扩散先验中。这些设计共同实现了从互联网动态视频到世界坐标 3D 重建的端到端泛化。

## 整体框架

AnyLift 采用**两阶段统一流水线**，从动态摄像机单目视频中重建世界坐标系下的 3D 人体运动及人-物交互（HOI）。其核心设计立足一个关键瓶颈：现有方法在动态摄像机下难以恢复全局一致的 3D 运动，尤其对稀有动作和交互场景泛化不足。AnyLift 的因果调控旋钮在于引入**相机轨迹与极线条件化的 2D 运动扩散模型**，并配合**混合数据源训练策略**，从海量互联网视频中学习多视图一致的 2D 运动先验，进而在无 3D 监督的情况下端到端地恢复全局 3D 运动。

流水线的两个阶段如图 2 所示，模块间关系与数据流如下：

1.  **Stage 1：多视图 2D 合成数据生成**
    此阶段的目标是为后续多视图模型准备训练数据。它包含三个核心模块：
    -   **单视图 2D 运动扩散模型**：该模型以相机轨迹和极线为条件，学习特定动作领域（如体操、武术）的 2D 运动先验。其输入为从互联网视频提取的 2D 关键点序列，输出为去噪后的 2D 运动。
    -   **混合数据源训练**：为克服互联网视频视角覆盖有限的固有问题，训练时混合两类数据：(1) 视频中提取的全局 2D 关键点序列；(2) 利用现成 3D 估计器（GVHMR）重建并反投影得到的**局部 2D 姿态**。后者通过分解表示丢弃了不可靠的根轨迹偏差，显著提升了视角多样性。
    -   **多视图 2D 运动数据合成**：利用已学到的单视图 2D 运动先验，通过**分数蒸馏采样（SDS）** 联合**多视图一致性损失**（极线匹配损失），从单视图输入生成多视图 2D 关键点序列。为降低计算开销，极线匹配损失仅施加于相邻视图及每视图与输入视图之间，而非所有视图对。

2.  **Stage 2：多视图 2D 运动扩散与 3D 重建**
    此阶段直接从单目视频输入恢复世界坐标下的 3D 运动。
    -   **多视图 2D 运动扩散模型**：该模型以单视图 2D 输入和相机轨迹为条件，生成相机条件下多视图一致的 2D 运动。它是连接 2D 观测与 3D 重建的核心桥梁。
    -   **3D 运动重建（含 HOI）**：通过最小化多视图反投影误差，将多视图 2D 关键点拟合到 SMPL 人体模型，恢复世界坐标下的 3D 姿态和轨迹。对于人-物交互，该模块同时优化人体和物体位姿，利用预定义的物体关键点与重建的 3D 关键点进行对齐，实现统一框架下的人与物体运动重建。

整个框架的输入端为动态摄像机拍摄的单目视频，输出端为世界坐标系下的 3D 人体运动序列 $\\tau = ( \\mathcal{H}, \\mathcal{O} )$，其中人体运动 $\mathcal{H}_t = ( \mathbf{r}_t, \phi_t, \Theta_t )$ 包含根平移、全局朝向和身体姿态参数，物体运动 $\mathcal{O}_t = \{ \mathbf{r}_t, \mathbf{t}_t, s \}$ 包含旋转、平移和全局缩放。

### 补充图表

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2604_17818/figures/002_Figure_2.jpg]]
*Figure 2: Overview of AnyLift. (a) We first train a single-view 2D motion diffusion model conditioned on camera trajectories and epipolar lines to synthesize multi-view 2D training data. (b) During training, we employ a hybrid data source strategy that enhances viewpoint coverage by combining global 2D pose sequences from videos with locally reprojected poses. (c) Finally, we train a multi-view 2D motion diffusion model to reconstruct consistent world-coordinated 3D human and HOI motions from real-world videos*

## 核心模块与公式推导

AnyLift 遵循两阶段管线：**多视图 2D 合成数据生成** 与 **多视图 2D 运动扩散**。前者利用单视图 2D 运动扩散模型合成多视图训练数据；后者以相机轨迹为条件，从单目视频 2D 关键点生成多视图一致的 2D 运动，再通过反投影误差优化恢复世界坐标下的 3D 姿态和轨迹。

### 3.1 单视图 2D 运动扩散模型

模型将长度为 $T$ 的 2D 运动序列表示为 $\mathbf{X}_0 \in \mathbb{R}^{T \times J \times 2}$，其中 $J$ 为关键点数量。前向扩散过程逐步加噪：

$$q(\mathbf{X}_n | \mathbf{X}_{n-1}) = \mathcal{N}(\mathbf{X}_n; \sqrt{1-\beta_n} \mathbf{X}_{n-1}, \beta_n \mathbf{I}) \quad \text{(Eq. 1)}$$

去噪网络 $\mathbf{X}_\theta$ 以噪声样本 $\mathbf{X}_n$、噪声步长 $n$、相机轨迹 $\mathbf{C}$ 和极线 $\mathbf{L}$ 为条件，通过 L1 损失预测干净样本：

$$\mathcal{L} = \mathbb{E}_{\mathbf{X}_0, n} \| \mathbf{X}_0 - \mathbf{X}_\theta(\mathbf{X}_n, n, \mathbf{C}, \mathbf{L}) \|_1 \quad \text{(Eq. 2)}$$

其中相机轨迹 $\mathbf{C}$ 编码了每帧的相机内外参，极线 $\mathbf{L}$ 编码了视图间的对极几何约束。这一条件化设计是 AnyLift 区别于 MVLift（仅适用于静态相机）的核心改动。

### 3.2 混合数据源训练

为缓解互联网视频视角覆盖有限的问题，训练数据混合了两个互补来源：
1. 从真实视频提取的全局 2D 关键点序列 $\mathbf{X}^{\text{video}}$；
2. 利用现成 3D 估计器（GVHMR）重建并反投影得到的局部 2D 姿态 $\mathbf{X}^{\text{proj}}$。

对于反投影的局部姿态，采用分解表示丢弃根轨迹偏差：通过掩码 $\mathbf{M}$ 排除髋关节等携带全局平移信息的关节，仅对局部姿态计算扩散损失：

$$\mathcal{L}^{\mathrm{proj}} = \mathbb{E}_{\mathbf{X}_0, n} \| \mathbf{M} \odot \mathbf{X}_0 - \mathbf{M} \odot \mathbf{X}_\theta(\mathbf{X}_n^{\mathrm{proj}}, n, \mathbf{C}, \mathbf{L}) \|_1 \quad \text{(Eq. 4)}$$

这一策略使模型能从有限视角覆盖的视频中学到多视图一致的 2D 运动先验，消融实验（Table 5）表明移除混合训练会导致所有指标大幅下降。

### 3.3 多视图 2D 运动数据合成

利用已学到的 2D 运动先验，通过分数蒸馏采样（SDS）合成多视图训练数据。对于每个目标视图 $v$，SDS 梯度为：

$$\nabla_{\mathbf{X}_v} \mathcal{L}_{\mathrm{SDS}} = \mathbb{E}_{n,\epsilon} \Bigl[ w(n) \bigl( \epsilon_{\theta}(\mathbf{X}_{v,n}, n, \mathbf{C}, \mathbf{L}) - \epsilon \bigr) \Bigr] \quad \text{(Eq. 5)}$$

其中 $\epsilon_\theta$ 为预训练的去噪网络，$w(n)$ 为噪声相关的权重。为强制多视图几何一致性，引入视图 $u$ 和 $v$ 之间的极线匹配损失：

$$\mathcal{L}_{\mathrm{line}}^{u v} = \sum_{t=1}^{T} \big\langle \mathbf{L}_t^{u v}, (\mathbf{X}_{v,t}^{\mathrm{g}}, \mathbf{1}) \big\rangle \quad \text{(Eq. 6)}$$

该损失鼓励视图 $v$ 中关键点的齐次坐标落在视图 $u$ 定义的极线上。与 MVLift 对所有视图对施加线匹配损失不同，AnyLift 仅对相邻视图和输入视图对应用此损失，以降低计算开销。

### 3.4 3D 运动重建与 HOI 扩展

多视图 2D 运动扩散模型生成相机条件下的多视图一致 2D 关键点后，通过最小化多视图反投影误差优化 SMPL 模型参数，恢复世界坐标下的 3D 人体姿态 $\mathcal{H}_t = (\mathbf{r}_t, \phi_t, \Theta_t)$，其中 $\mathbf{r}_t$ 为根平移、$\phi_t$ 为全局朝向、$\Theta_t$ 为身体姿态参数。

对于人物交互（HOI），框架统一处理人体和物体运动。物体运动表示为 $\mathcal{O}_t = \{ \mathbf{r}_t, \mathbf{t}_t, s \}$，其中 $\mathbf{r}_t$ 为 6D 旋转、$\mathbf{t}_t$ 为平移、$s$ 为全局尺度。从重建的物体 3D 关键点 $\mathbf{Q}$ 和预定义的规范关键点 $\mathbf{P}$，通过带可见性掩码的 L2 拟合损失估计物体姿态：

$$\mathcal{L}_{\mathrm{fit}}^{\mathrm{obj}} = \frac{1}{TM} \sum_{t=1}^{T} \sum_{i=1}^{M} m_i \| s \operatorname{Rot}(\mathbf{r}_t) \mathbf{p}_i + \mathbf{t}_t - \mathbf{q}_{i,t} \|_2 \quad \text{(Eq. S3)}$$

并辅以旋转连续性正则项：

$$\mathcal{L}_{\mathrm{smooth}}^{\mathrm{obj}} = \frac{1}{T-1} \sum_{t=1}^{T-1} \| \mathbf{r}_t - \mathbf{r}_{t+1} \|_2 \quad \text{(Eq. S4)}$$

需注意，HOI 重建依赖手工设计的物体关键点，且每种物体类别需单独训练多视图扩散模型，这是当前方法的一个限制。

## 实验与分析

AnyLift 在三个核心场景下接受验证：标准基准 AIST++（含静态与动态相机）、自收集的互联网稀有运动视频（体操、武术），以及人物交互基准 BEHAVE。评估覆盖 2D 重投影精度、3D 关节误差、根轨迹误差、运动质量（FID）和物理合理性（足部滑动、人类偏好）等多个维度。

### AIST++ 基准：动态相机下的鲁棒性验证

Table 1 报告了 AIST++ 数据集上的定量结果。在静态相机设置下，AnyLift 的 MPJPE 达到 108.0 mm，略优于 MVLift 的 110.7 mm；根平移误差 T_root 为 64.9 mm，同样低于 MVLift 的 67.6 mm。这表明即使在不涉及相机运动的简单场景中，相机轨迹条件化与混合数据源训练仍带来一致的精度增益。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2604_17818/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation on the AIST++ dataset [19] under (1) static-camera setup (upper) and (2) dynamic-camera setup (lower). AnyLift achieves competitive 3D joint accuracy and improved root translation estimation while maintaining robustness under dynamic camera*

动态相机设置下的差距更为显著。AnyLift 的 MPJPE 为 109.3 mm，而 MVLift 升至 122.1 mm，误差降低 12.8 mm。这一对比直接验证了核心瓶颈——MVLift 基于静态相机假设，在动态相机下 2D 运动先验失效，而 AnyLift 通过将相机轨迹 C 和极线 L 作为扩散模型的条件输入（Eq. 2），使模型学会在相机运动下保持多视图一致的 2D 运动预测。值得注意的是，AnyLift 在动态相机下的 MPJPE（109.3 mm）与静态相机下（108.0 mm）几乎持平，证明该方法对相机运动具有高度鲁棒性。

### 互联网稀有运动视频：泛化能力检验

Table 2 和 Table 5 展示了在自收集的体操和武术互联网视频上的结果。AnyLift 在 2D 关键点误差 J_2D^C 上达到 11.4 px，显著低于基于优化的 **SMPLify**（Bogo et al., ECCV 2016）的 16.0 px，以及基于 AMASS 训练的 **WHAM**（Shin et al., CVPR 2024）等基线方法。FID 指标同样大幅领先，表明 AnyLift 生成的 2D 运动在分布上更接近真实观测。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2604_17818/figures/003_Table_2.jpg]]
*Table 2: Quantitative evaluation on our collected Internet videos. AnyLift outperforms all baselines across most metrics, demonstrating the plausibility of our method on Internet videos*

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2604_17818/figures/009_Table_5.jpg]]
*Table 5: Ablation study on our collected Internet videos. Performance drops across all metrics without incorporating local 2D poses from diverse viewpoints*

这一优势源于两个机制。第一，单视图 2D 扩散模型在特定动作类别的互联网视频上训练，学到了该类运动的强先验，使模型在遭遇训练分布外的稀有动作（如空翻、武术套路）时仍能生成合理结果。第二，混合数据源训练策略引入了 GVHMR 反投影的局部 2D 姿态，这些姿态虽带有全局轨迹偏差，但通过分解表示丢弃根轨迹后，为模型提供了丰富的多视角局部姿态信息，弥补了互联网视频视角覆盖不足的缺陷。

Table 3 的人类偏好研究进一步佐证了上述结论。参与者在 65.6% 的情况下更偏好完整 AnyLift 的重建结果，而非去除混合训练的变体（34.4%），主要理由为更好的地面接触和运动质量。这从感知层面验证了混合数据源策略对物理合理性的贡献。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2604_17818/figures/005_Table_3.jpg]]
*Table 3: Human study on reconstructed human motions from our collected Internet videos. Participants prefer our reconstruction results for their better ground contact and motion quality*

### 消融实验：混合数据源的关键作用

Table 5 的消融实验直接检验了混合数据源训练的必要性。移除该策略（即仅使用视频提取的 2D 关键点训练单视图扩散模型）后，所有互联网视频指标均出现大幅下降：J_2D、J_2D^C 和 FID 全面恶化。这一结果揭示了单一数据源的致命缺陷——互联网视频的相机视角分布高度偏斜（Figure S1 展示了体操和武术视频中人体朝向在相机坐标系下的分布），仅靠这些视角有限的 2D 关键点无法学到足够多样化的 2D 运动先验。GVHMR 反投影的局部姿态虽然自身带有估计误差，但其提供的多视角信息有效弥补了这一缺陷，形成了互补的数据源组合。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2604_17818/figures/010_Figure_S.1.jpg]]
*Figure S.1: Facing direction distributions of estimated humans in the gymnastics (upper) and martial arts (lower) videos under the camera coordinate system. The angular axis indicates the facing direction and the radial axis represents number of frames*

### BEHAVE 人物交互基准：统一框架的有效性

Table 4 展示了 BEHAVE 数据集上的人物交互重建结果。在静态相机下，AnyLift 在 Box 类别上的 MPJPE 仅为 42.68 mm，而 SMPLify 高达 114.56 mm，误差降低 71.88 mm。物体平移误差 T_root^O 同样大幅领先 **VisTracker**（Xie et al., CVPR 2023）。在 Chair 和 Table 类别上趋势一致，动态相机下优势依然保持。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2604_17818/figures/008_Table_4.jpg]]
*Table 4: Quantitative evaluation on the BEHAVE dataset [1] under (1) static-camera setup (upper) and (2) dynamic-camera setup (lower). AnyLift outperforms all baselines across object categories and achieves robust performance under dynamic-camera conditions*

这一性能提升得益于 AnyLift 的统一框架设计：多视图 2D 扩散模型在训练时接受物体关键点的掩码训练（Eq. 4），使模型能同时推理人体和物体的 2D 关键点序列；3D 重建阶段通过 Eq. S3 的物体拟合损失将模板对齐到多视图一致的 3D 关键点，Eq. S4 的平滑正则项则保证物体运动的时序连续性。相比分别处理人体和物体的基线方法，统一框架能更好地捕捉人与物体之间的空间约束关系。

### 失败模式与局限性

尽管 AnyLift 在多数场景下表现优异，分析中仍识别出以下失败模式：

1. **严重遮挡与极端相机运动**：当 2D 关键点提取器（ViTPose）因遮挡或运动模糊失效时，后续的扩散模型和 3D 优化均会受到影响。类似地，相机运动估计器（MegaSaM）在极端旋转或快速变焦场景下的误差会通过极线条件 L 传播至整个管线。

2. **跨类别泛化受限**：单视图 2D 扩散模型需为每个动作类别（如体操、武术）单独训练，无法 zero-shot 迁移至新类别。这源于模型学到的 2D 运动先验与训练数据的动作分布紧密耦合。

3. **物体表示依赖手工设计**：HOI 重建需要预定义物体模板和规范关键点，且多视图扩散模型需针对每种物体类别单独训练。这限制了方法向未见物体类别的扩展能力。

4. **视点偏见残留**：混合训练策略虽部分缓解了互联网视频的视点偏见，但 Figure S1 显示体操和武术视频的相机视角分布仍高度集中，可能影响模型在极端视角下的重建质量。

### 补充图表

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2604_17818/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative comparison of human motion reconstruction on our collected Internet videos. AnyLift produces more plausible motions, mitigating the root trajectory errors, inaccurate local body pose, and self-penetration artifacts observed in baselines*

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2604_17818/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of HOI reconstruction on the BEHAVE [1] dataset. We show results on two object categories, chair and table. AnyLift produces coherent and physically plausible human-object interactions with accurate contact and minimal penetration*

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2604_17818/figures/001_Figure_1.jpg]]
*Figure 1: Human and human-object interaction (HOI) motions lifted by our approach. Trained on 2D keypoints and corresponding camera trajectories, our framework AnyLift reconstructs world-coordinated 3D human motion and HOI from monocular videos captured by dynamic cameras. We demonstrate its effectiveness on human motion reconstruction from Internet gymnastics videos (left) and on HOI reconstruction from captured real-world videos (right). Please refer to our project page for video results*

## 方法谱系与知识库定位

### 与基线工作的关系

AnyLift 处于从单目视频恢复世界坐标下 3D 人体运动这一研究脉络中，其直接前身是 **MVLift**——一种基于多视图 2D 扩散的 3D 运动重建方法，但 MVLift 假设静态相机，无法处理互联网视频中普遍存在的动态相机场景。AnyLift 的核心推进在于将相机轨迹与极线约束注入扩散模型的条件输入，使框架从“静态相机下的多视图一致”拓展为“动态相机下的相机感知多视图一致”。这一改动在根本上改变了问题设定：MVLift 的极线约束是固定的，而 AnyLift 的极线随相机运动逐帧变化，要求模型同时学习运动先验与相机几何的耦合关系。

与基于优化的经典方法 **SMPLify**（Bogo et al., ECCV 2016）相比，AnyLift 不再依赖单帧 2D 重投影误差的逐帧优化，而是通过扩散模型学习时序 2D 运动先验，从根本上缓解了深度歧义和轨迹漂移。在互联网体操视频上的 2D 关键点误差（J_2D^C）从 SMPLify 的 16.0 px 降至 11.4 px（Table 2 与 Table 5），这一差距在动态相机下尤为显著。

与基于大规模 3D 运动捕捉数据训练的 **WHAM**（Shin et al., CVPR 2024）和 **GVHMR**（Shen et al., SIGGRAPH Asia 2024）相比，AnyLift 的定位差异更为根本：WHAM 和 GVHMR 依赖 AMASS 等 3D 监督数据，其泛化能力受限于训练集中的动作分布。AnyLift 则完全绕过了对 3D 标注的需求，仅从互联网视频的 2D 关键点和相机轨迹中学习，这使得它能够处理体操、武术等稀有动作类别——这些动作在现有 3D 数据集中几乎不存在。Table 2 和 Table 5 的定量结果以及 Figure 3 的定性对比（根轨迹误差、局部姿态精度、自穿透伪影的改善）共同支撑了这一优势。

在人物交互（HOI）重建方面，AnyLift 与 **VisTracker**（Xie et al., CVPR 2023）形成对比。VisTracker 是专门的单目 RGB HOI 重建方法，而 AnyLift 在统一框架内同时处理人体和物体运动。在 BEHAVE 基准的静态相机设置下，AnyLift 在 Box 类别的物体平移误差（T_root^O）上达到 95.38，而 VisTracker 为 143.59（Table 4），差距达 -48.21。这得益于多视图 2D 扩散模型对物体关键点的联合优化，而非后处理式的物体位姿估计。

### 适用边界

AnyLift 的有效性受以下边界条件约束：

1. **动作类别特异性**：单视图 2D 扩散模型需要为每个动作类别（如体操、武术）单独训练。这是因为不同类别的 2D 运动分布差异巨大（见 Figure S1 中体操与武术的面向方向分布差异），单一模型难以同时覆盖。这意味着将 AnyLift 应用于全新动作类别时，需要重新收集该类别互联网视频并训练单视图扩散模型。

2. **物体类别特异性**：HOI 重建依赖手工设计的物体关键点，且多视图扩散模型针对每种物体类别（如椅子、桌子、箱子）单独训练。这限制了模型对未见物体类别的 zero-shot 泛化能力。

3. **2D 关键点质量依赖**：整个 pipeline 以 ViTPose 提取的 2D 关键点作为输入。在严重遮挡或极端相机运动场景下，2D 关键点提取和 MegaSaM 相机运动估计可能同时失效，导致 SDS 合成多视图数据时误差累积，最终影响 3D 重建质量。

4. **视点分布偏见**：学习过程依赖于互联网视频固有的视点分布。混合数据源训练策略通过引入 GVHMR 反投影的局部 2D 姿态来增加视点多样性，但这一缓解是部分的——反投影姿态本身受 GVHMR 估计误差影响，且无法覆盖完全未见的视点角度。

### 局限与开放问题

**已确认的局限**：

- **跨类别泛化不足**：每个动作类别需要独立训练单视图扩散模型，无法实现 zero-shot 跨类别迁移。这一局限根源于 2D 运动先验的类别特异性，而非训练策略的选择。
- **物体表示依赖模板**：HOI 重建依赖预定义的物体模板和手工关键点，无法从视频中自主学习可推广的物体表示。这使得框架难以扩展到无模板的通用物体交互场景。
- **2D 噪声鲁棒性有限**：消融实验（Table 5）表明，移除混合数据源训练后性能大幅下降，间接说明仅靠互联网视频的 2D 关键点（含噪声和追踪错误）不足以学习鲁棒的 2D 运动先验。

**开放问题**：

- 能否通过元学习或条件扩散模型实现跨动作类别的统一 2D 运动先验，避免为每个新类别重训模型？
- 能否摆脱对物体模板和手工关键点的依赖，直接从视频中学习隐式物体表示或利用可微分渲染进行端到端优化？
- 如何将框架扩展至多人和多对象交互的复杂场景？当前的多视图一致性损失假设场景中仅有一个主体，多人场景下的极线匹配和 SDS 优化策略需要根本性重新设计。
- 如何鲁棒地处理互联网视频中固有的 2D 关键点噪声和追踪错误？可能的路径包括在扩散模型中显式建模关键点不确定性，或引入自监督的 2D 关键点精炼模块。

## 原文 PDF

![[paperPDFs/CVPR_2026/AnyLift_Scaling_Motion_Reconstruction_from_Internet_Videos_via_2D_Diffusion.pdf]]