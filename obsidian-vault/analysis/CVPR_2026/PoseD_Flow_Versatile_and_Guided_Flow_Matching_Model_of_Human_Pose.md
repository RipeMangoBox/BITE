---
title: "PoseD-Flow: Versatile and Guided Flow Matching Model of Human Pose"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PoseD_Flow_Versatile_and_Guided_Flow_Matching_Model_of_Human_Pose.pdf
project_link: "https://circle-group.github.io/research/PoseD-Flow"
code_link: "https://github.com/circle-group/PoseDFlow"
aliases:
- PF
- PoseD-Flow
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在 SO(3) 乘积流形上构建 Riemannian Flow Matching 模型（PoseRFM）作为人体姿态先验，并通过微分黎曼 ODE 采样过程实现免训练的引导逆求解（Riemannian D-Flow）。
primary_logic: 通过流形上的源点优化对 ODE 进行反向传播，梯度更新天然受到数据局部协方差和流形曲率的共同塑形，从而产生朝向高密度、真实姿态的偏向，即使在严重遮挡和高噪声下也能稳定逆推。
claims:
- PoseRFM 在无条件生成上取得最优 FID (0.013) 和最低最近邻距离 (0.070)，显著优于扩散模型 DPoser 等。
- 在多种遮挡条件下的姿态补全中，PoseRFM 在 MPVPE 与多样性（APD）之间取得最佳平衡，优于所有对比方法。
- 几何消融实验表明，采用 Riemannian 流形和 geodesic loss + 轨迹正则化是性能提升的关键，仅在欧几里得空间的 Flow Matching 效果明显下降。
- AMASS unconditional generation 上 FID ↓ = 0.013 (PoseRFM N=1000)
---

# PoseD-Flow: Versatile and Guided Flow Matching Model of Human Pose

> [!tip] 核心洞察
> 通过流形上的源点优化对 ODE 进行反向传播，梯度更新天然受到数据局部协方差和流形曲率的共同塑形，从而产生朝向高密度、真实姿态的偏向，即使在严重遮挡和高噪声下也能稳定逆推。

| 字段 | 内容 |
|------|------|
| 中文题名 | PoseD-Flow：适用于人体姿态的多功能引导流匹配模型 |
| 英文题名 | PoseD-Flow: Versatile and Guided Flow Matching Model of Human Pose |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Nadar_PoseD-Flow_Versatile_and_Guided_Flow_Matching_Model_of_Human_Pose_CVPR_2026_paper.html) · [Project](https://circle-group.github.io/research/PoseD-Flow) · [Code](https://github.com/circle-group/PoseDFlow) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | PoseD-Flow |
| Dataset | AMASS unconditional generation, AMASS Pose Completion, AMASS motion denoising, EHF Human Mesh Recovery |

> [!tip] 效果简介
> - AMASS unconditional generation 上，FID ↓ 0.013 (PoseRFM N=1000) vs 0.019 (DPoser) (-0.006)；d_NN (rad) ↓ 0.070 (PoseRFM N=1000) vs 0.073 (DPoser) (-0.003)；APD (cm) ↑ 15.544 (PoseRFM N=1000) vs 14.992 (DPoser) (+0.552)。
> - AMASS Pose Completion (Occ. left leg) 上，MPVPE (mm) ↓ 83.81 vs 优于现有方法 (e.g., DPoser)。
> - AMASS motion denoising (noise 40mm) 上，MPJPE (mm) ↓ 18.88 vs 优于对比方法。

## 概述

人体姿态建模长期受限于两个根本性挑战：其一，铰接式姿态天然存在于非欧几里得的旋转流形上，而现有生成先验（如 VAE、扩散模型）或将其强行嵌入欧几里得空间，或依赖复杂的测地距离近似；其二，在遮挡、噪声等逆问题场景下，缺乏一种既能保持几何一致性、又无需针对特定任务重新训练的灵活推理机制。**PoseD-Flow** 针对这两大瓶颈，首次将流匹配引入人体姿态领域，提出了一个完整且多功能的框架。

该框架的核心由两个模块构成。**PoseRFM** 在 SO(3) 的乘积流形上直接构建黎曼流匹配模型，通过学习条件向量场来逼近真实姿态分布，从而获得一个高质量、几何内蕴的姿态先验。在此基础上，**Riemannian D-Flow** 提供了一种免训练的引导逆求解方法——通过对黎曼 ODE 的采样过程进行可微反向传播，在源点空间执行优化，使生成结果既符合观测约束，又自动偏向于数据流形上的高密度区域。这种“隐式偏差”使得模型即使在严重遮挡和高噪声条件下，也能稳定地恢复出物理合理、形态自然的姿态。

实验表明，PoseD-Flow 在无条件生成、姿态补全、运动去噪以及人体网格恢复等多个任务上均达到或超越了现有最优水平。在 AMASS 无条件生成中，PoseRFM 取得了 0.013 的 FID，优于基于扩散模型的 DPoser；在多种遮挡条件下的姿态补全中，Riemannian D-Flow 在精度（MPVPE）与多样性（APD）之间实现了最佳平衡。几何消融实验进一步证实，将建模空间从欧几里得空间迁移到黎曼流形，并引入测地损失与轨迹正则化，是性能提升的关键所在。

## 背景与动机

### 人体姿态建模的核心挑战

人体姿态建模是计算机视觉与图形学中的基础问题，其应用涵盖运动捕捉、人机交互、虚拟现实等广泛领域。该问题的核心难点在于：人体姿态本质上是高维、非线性的关节旋转集合，而非简单的欧几里得向量。具体而言，每个人体关节的旋转天然存在于三维旋转群 $\operatorname{SO}(3)$ 上：

$$\operatorname{SO}(3) = \{ R \in \mathbb{R}^{3\times 3} : R^{\top} R = I, \det(R) = 1 \}$$

这意味着 $K$ 个关节的人体姿态实际定义在 $\operatorname{SO}(3)^K$ 乘积流形上，而非 $\mathbb{R}^{3K}$ 的平坦空间。忽视这一几何结构会导致生成姿态违反人体关节的物理约束，产生不合理的扭转或扭曲。

### 现有方法的局限

近年来，深度生成模型在人体姿态先验建模方面取得了显著进展。**VPoser**（Pavlakos et al., CVPR 2019）采用变分自编码器学习姿态的潜在空间，但其高斯先验假设限制了分布建模的表达能力。**Pose-NDF**（Tiwari et al., ECCV 2022）和**NRDF**（He et al., CVPR 2024）分别利用神经距离场和黎曼距离场来隐式建模姿态流形，但在生成采样方面缺乏有效的机制。**GFPose**（Ci et al., CVPR 2023）通过梯度场建模姿态分布，但其逆问题求解能力有限。

扩散模型的出现带来了新的突破。**DPoser**（Lu et al., ICCV 2025）首次将扩散模型引入人体姿态先验，取得了当时最优的生成质量。然而，扩散模型存在采样效率低下的固有问题，通常需要数百甚至上千步的迭代去噪过程。

### 流匹配的机遇与两大障碍

流匹配（Flow Matching）作为扩散模型的强有力替代方案，通过直接建模从先验分布到数据分布的常微分方程（ODE）路径，实现了更高效、更稳定的生成采样。然而，将流匹配应用于人体姿态建模面临两个根本性障碍：

1. **缺少预训练的流先验**：在 PoseD-Flow 之前，尚无任何工作将流匹配框架用于人体姿态的生成建模，缺乏可用的流先验模型作为基础。

2. **非欧几里得几何本质**：人体姿态的铰接结构决定了其天然存在于 $\operatorname{SO}(3)^K$ 乘积流形上。标准流匹配方法假设数据位于欧几里得空间，无法直接处理流形上的几何约束——在平坦空间上定义的向量场和积分路径会破坏旋转矩阵的正交性和行列式约束，导致生成的姿态在几何上不合法。

### 本文的动机与核心思路

针对上述障碍，PoseD-Flow 提出了一套完整的解决方案，包含两个核心组件：

- **PoseRFM**：首个基于黎曼流匹配（Riemannian Flow Matching）的人体姿态先验模型，直接在 $\operatorname{SO}(3)^K$ 乘积流形上定义条件向量场和学习目标，天然保持姿态的几何合法性。

- **Riemannian D-Flow**：一种免训练的引导逆求解机制，通过微分黎曼 ODE 的采样动力学，在推理阶段对源点进行优化，使生成过程受观测数据约束，而无需任何针对特定任务的额外训练。该机制的核心洞察在于：流形上的源点优化天然受到数据局部协方差和流形曲率的共同塑形，产生朝向高密度、真实姿态的隐式偏差（implicit bias），即使在严重遮挡和高噪声条件下也能稳定逆推。

通过这一框架，PoseD-Flow 在无条件生成、姿态补全、运动去噪和人体网格恢复等多个任务上均展现出与扩散模型相当甚至更优的性能，同时保持了流匹配固有的采样效率优势。

## 核心创新

PoseD-Flow 的核心创新在于将**流匹配（Flow Matching）**首次引入人体姿态建模，并通过两个关键“changed slots”解决了此前流匹配无法直接应用于铰接姿态的根本障碍。

### 从欧几里得到黎曼流形：PoseRFM 的建模空间跃迁

此前的人体姿态先验模型——无论是基于 VAE 的 **VPoser**（Pavlakos et al., CVPR 2019）、基于扩散的 **DPoser**（Lu et al., ICCV 2025）、还是基于神经距离场的 **Pose-NDF**（Tiwari et al., ECCV 2022）——均在欧几里得空间或其隐空间中对关节旋转进行建模。流匹配的朴素应用 **PoseFM** 同样延续了这一范式。

**关键改变**：PoseRFM 将建模空间从 $\mathbb{R}^{K \times 3}$ 直接提升到 **$\mathrm{SO}(3)^K$ 乘积流形**上。这一改变由两个瓶颈驱动：

1. **缺少预训练的流先验**：流匹配需要从简单先验分布到目标数据分布的连续路径，而欧几里得空间中的高斯先验无法自然地适配旋转群的非欧几何。
2. **铰接姿态的非欧本质**：关节旋转天然属于 $\mathrm{SO}(3)$ 群，其测地距离、切空间、指数/对数映射均需在流形上定义。直接在欧几里得空间回归向量场会忽略旋转的周期性和正交约束，导致生成的姿态违反物理合理性。

PoseRFM 在乘积流形上定义条件向量场：

$$u_t(x \mid x_1) = \frac{1}{1-t} \mathrm{Log}_x(x_1)$$

该向量场以闭合形式沿测地线引导采样路径，天然保证了生成样本始终位于 $\mathrm{SO}(3)^K$ 流形上。消融实验（Table 6）提供了决定性证据：采用 Riemannian 流形和 geodesic loss + 轨迹正则化的 PoseRFM 在姿态补全中显著优于欧几里得流匹配基线 PoseFM，验证了流形建模的必要性。

### 从固定采样到微分引导：Riemannian D-Flow 的逆求解范式

扩散模型（如 DPoser）在解决逆问题（姿态补全、去噪、人体网格恢复）时，通常依赖固定步数的扩散采样或需要任务特定训练的引导策略。这限制了模型的灵活性和泛化能力。

**关键改变**：Riemannian D-Flow 提出了一种**免训练的引导逆求解范式**——通过对黎曼 ODE 采样过程进行微分反向传播，直接在流形上优化源点 $x_0$：

$$\min_{x_0 \in \mathcal{M}} \left( \mathcal{L}_{\mathrm{data}}(x(1)) + \mathcal{L}_{\mathrm{traj}}(x_0, u) \right)$$

其中 $x(1)$ 是 ODE 的终点。这一范式的核心机制体现在两个层面：

- **隐式偏差（Implicit Bias）**：源点梯度更新天然受到数据局部协方差和流形曲率的共同塑形（Figure 2 示意）。梯度被投影到“可达子空间”上，使得优化过程即使在严重遮挡和高噪声下也能朝向高密度、真实的姿态区域收敛，而非产生物理上不合理的解。
- **轨迹正则化**：引入 $\mathcal{L}_{\mathrm{traj}} = \sum_{i=1}^{K} \sum_{k=1}^{N} (3 - \mathrm{tr}(x_{ik}))$ 惩罚路径中的大旋转角度，防止优化过程中的突变和不自然姿态。

这一“微分 ODE 源点优化”机制使得 PoseD-Flow 无需任何任务特定的微调，即可统一应用于姿态补全、运动去噪和人体网格恢复等多个逆问题，且在精度与多样性之间取得了最佳平衡。

### 创新点的因果链条

两个 changed slots 之间存在因果依赖：**流形建模是微分引导的前提**。只有在 $\mathrm{SO}(3)^K$ 上正确定义了向量场和 ODE 采样过程，Riemannian D-Flow 才能利用流形的切空间投影和测地距离进行有意义的梯度反传。若在欧几里得空间中进行源点优化（如 PoseFM），不仅缺乏几何一致性，且梯度更新方向无法反映旋转群的内在结构，导致性能显著下降。

## 整体框架

PoseD-Flow 由两个核心模块构成：**PoseRFM**（Riemannian Flow Matching 姿态先验）与 **Riemannian D-Flow**（免训练的引导逆求解器），二者通过微分黎曼 ODE 采样过程紧密耦合，形成“先验生成 + 可控逆推”的统一框架（Figure 1）。

![[assets/figures/papers/paper_list_l1001_https_openaccess_thecvf_com_content_CVPR2026_html_Nadar_PoseD_Flow_Versa/figures/001_Figure_1.jpg]]
*Figure 1: PoseD-Flow framework: (top) PoseRFM, a robust human pose prior defined on the product manifold of joints using Riemannian Flow Matching; (bottom): Riemannian D-Flow, a flexible, geometry-aware inversion technique for flow models. Together, they provide a novel approach to solving inverse problems in human pose, achieving results competitive with SotA diffusion models*

### 模块关系与数据流

1. **PoseRFM 姿态先验（生成端）**  
   - **建模空间**：直接在 $K$ 个关节旋转构成的乘积流形 $\mathcal{M} = \operatorname{SO}(3)^K$ 上定义，而非欧几里得空间。这是与欧几里得流匹配基线 PoseFM 的根本差异（Table 6 消融证实，仅在欧几里得空间的 Flow Matching 性能显著下降）。  
   - **训练机制**：通过条件向量场 $u_t(x \mid x_1) = \frac{1}{1-t} \mathrm{Log}_x(x_1)$ 回归速度场网络 $v_w(x, t)$，学习从简单先验分布到数据分布的连续归一化流（Algorithm 1）。  
   - **输出**：给定初始噪声 $x_0 \sim p_0$，通过积分黎曼 ODE $\frac{d}{dt}\psi_t(x) = u_t(\psi_t(x))$ 得到生成样本 $x_1 = \psi_1(x_0)$，即一组关节旋转参数。

2. **Riemannian D-Flow 引导逆求解（控制端）**  
   - **问题形式化**：将逆任务（姿态补全、去噪、人体网格恢复等）统一为源点优化问题：
     $$\min_{x_0 \in \mathcal{M}} \left( \mathcal{L}_{\text{data}}(x(1)) + \mathcal{L}_{\text{traj}}(x_0, u) \right)$$
     其中 $x(1)$ 是以 $x_0$ 为初值求解 PoseRFM 黎曼 ODE 得到的终点，$\mathcal{L}_{\text{data}}$ 为任务相关数据损失，$\mathcal{L}_{\text{traj}}$ 为轨迹正则项（Eq. 10-11）。  
   - **免训练特性**：无需针对特定任务微调 PoseRFM 网络权重，仅通过微分 ODE 采样过程反向传播梯度至源点 $x_0$，即可将任意可微损失作为引导信号注入生成过程（Algorithm 2）。  
   - **几何感知梯度**：梯度经投影至切空间后由 Riemannian Adam 更新源点，更新方向天然受到数据局部协方差和流形曲率的共同塑形，产生朝向高密度真实姿态的隐式偏向（Figure 2）。

3. **SMPL 身体模型（桥接层）**  
   - 将 PoseRFM / D-Flow 输出的关节旋转参数与形状参数 $\beta$ 结合，通过 SMPL 模型生成人体网格和 3D 关键点，用于计算各类任务损失（如重投影损失 $\mathcal{L}_{\text{2D}}$、测地补全损失 $\mathcal{L}_{\text{data}}$ 等）。

### 输入输出流

- **无条件生成**：随机噪声 $x_0 \sim p_0$ → PoseRFM ODE 积分 → 关节旋转 $x_1$ → SMPL → 人体姿态。  
- **条件逆任务**：观测信号（部分关节点、噪声序列、2D 关键点等） + 随机初始 $x_0$ → Riemannian D-Flow 迭代优化 $x_0$ → 经 PoseRFM ODE 得 $x_1$ → SMPL → 与观测对齐的完整人体姿态。

### 框架关键优势

- **统一性**：同一套 PoseRFM 先验和 Riemannian D-Flow 求解器可处理姿态补全（Table 2）、运动去噪（Table 3）、人体网格恢复（Table 4-5）等多种逆问题，无需任务特定设计。  
- **几何一致性**：全程在 $\operatorname{SO}(3)^K$ 流形上操作，轨迹正则项 $\mathcal{L}_{\text{traj}} = \sum_{i=1}^{K} \sum_{k=1}^{N} (3 - \mathrm{tr}(x_{ik}))$ 惩罚大旋转突变，保证生成姿态的物理合理性（Table 6 消融证实其关键作用）。  
- **竞争性能**：PoseRFM 在无条件生成上取得最优 FID (0.013) 和最低最近邻距离 (0.070)，显著优于扩散模型 DPoser（Lu et al., ICCV 2025）等（Table 1）。

## 核心模块与公式推导

### 3.1 流形基础：SO(3) 乘积流形

人体姿态由 $K$ 个关节的旋转矩阵表示，每个关节旋转位于三维旋转群上：

$$
\operatorname{SO}(3) = \{ R \in \mathbb{R}^{3\times 3} : R^{\top} R = I, \det(R) = 1 \}
$$

完整姿态空间为 $K$ 个 $\operatorname{SO}(3)$ 的乘积流形 $\mathcal{M} = \operatorname{SO}(3)^K$。流形上两点 $x = (R_1, \dots, R_K)$ 与 $x' = (R_1', \dots, R_K')$ 的距离定义为各关节测地距离的欧几里得范数：

$$
d_{\mathcal{M}}(x, x') = \| d(R_1, R_1'), \dots, d(R_K, R_K') \|_2
$$

其中单个关节的测地距离为 $d(R, R') = \cos^{-1}\left(\frac{\operatorname{tr}(R^{\top} R') - 1}{2}\right)$。该乘积流形结构是 PoseRFM 建模的基础——直接在流形上定义概率路径与向量场，避免了欧几里得空间中的投影误差。

### 3.2 PoseRFM：黎曼流匹配姿态先验

**核心思想**：PoseRFM 是首个直接在 $\operatorname{SO}(3)^K$ 乘积流形上定义的流匹配模型。与扩散模型不同，流匹配通过直接回归速度场来学习连续归一化流，无需多步去噪过程。

**黎曼 ODE 与流映射**：给定时间依赖的向量场 $u_t(x) \in T_x\mathcal{M}$，流映射 $\psi_t(x)$ 满足：

$$
\frac{d}{dt} \psi_t(x) = u_t(\psi_t(x)), \quad \psi_0(x) = x
$$

从初始噪声分布 $p_0$ 采样 $x_0$，沿 ODE 积分至 $t=1$ 得到生成样本 $x_1 = \psi_1(x_0) \sim p_1$，其中 $p_1$ 近似真实姿态分布。

**条件向量场设计**：PoseRFM 采用基于测地距离的条件概率路径。给定目标姿态 $x_1$，条件向量场为沿测地线以线性调度 $\kappa(t) = t$ 引导的极小范数向量场：

$$
u_t(x \mid x_1) = \frac{1}{1-t} \operatorname{Log}_x(x_1)
$$

其中 $\operatorname{Log}_x(x_1)$ 是黎曼对数映射，将 $x_1$ 映射到 $x$ 处的切空间。该闭合形式避免了每步求解测地线边值问题，使训练高效可行。

**训练目标**：神经网络 $v_w(x, t)$ 参数化向量场，通过最小化条件流匹配损失进行训练：

$$
\mathcal{L}_{\text{CFM}}(w) = \mathbb{E}_{t \sim \mathcal{U}[0,1], x_1 \sim p_{\text{data}}, x \sim p_t(\cdot \mid x_1)} \left[ \| v_w(x, t) - u_t(x \mid x_1) \|_g^2 \right]
$$

训练流程如 Algorithm 1 所示：从数据分布采样目标姿态 $x_1$，从先验分布采样 $x_0$，沿测地线插值得到中间点 $x_t$，计算条件向量场作为回归目标。

### 3.3 Riemannian D-Flow：免训练引导逆求解

**问题形式化**：给定观测 $y$（如部分可见关节、含噪声的运动序列），目标是找到先验分布中的源点 $x_0$，使其经 PoseRFM 的 ODE 演化后与观测一致：

$$
\min_{x_0 \in \mathcal{M}} \left( \mathcal{L}_{\text{data}}(x(1)) + \mathcal{L}_{\text{traj}}(x_0, u) \right)
$$

其中 $x(1) = \psi_1(x_0)$ 是 ODE 终点，$\mathcal{L}_{\text{data}}$ 是任务相关的数据拟合损失，$\mathcal{L}_{\text{traj}}$ 是轨迹正则项。

**轨迹正则项**：为防止 ODE 轨迹中出现不合理的剧烈旋转，引入对旋转角度的惩罚：

$$
\mathcal{L}_{\text{traj}} = \sum_{i=1}^{K} \sum_{k=1}^{N} (3 - \operatorname{tr}(x_{ik}))
$$

其中 $x_{ik}$ 是第 $i$ 个关节在第 $k$ 个积分步的旋转矩阵。$\operatorname{tr}(R) = 3$ 当且仅当 $R = I$（零旋转），因此该项惩罚偏离恒等旋转的累积角度。

**可微 ODE 反向传播**：每次迭代中，从当前 $x_0$ 出发用欧拉积分求解 ODE 得到 $x_1$，计算损失 $\mathcal{L}(x_1)$，通过自动微分反向传播梯度至 $x_0$。梯度被投影到 $x_0$ 的切空间以获得黎曼梯度，然后使用黎曼 Adam 更新源点。该过程无需对 PoseRFM 进行任何微调，实现了完全的免训练引导。

**隐式偏差机制**：如 Figure 2 所示，源点优化的梯度更新天然受到数据局部协方差和流形曲率的共同塑形。终点梯度被投影到由数据分布决定的“可达子空间”上，从而产生朝向高密度、真实姿态的偏向——即使在严重遮挡和高噪声条件下也能稳定逆推至合理姿态。

### 3.4 任务相关数据损失

不同逆问题通过替换 $\mathcal{L}_{\text{data}}$ 实现统一框架下的适配：

- **姿态补全**：对观测关节集 $\Omega$ 计算测地距离之和：
  $$
  \mathcal{L}_{\text{data}}(x) = \sum_{k \in \Omega} \cos^{-1}\left( \frac{\operatorname{tr}(x_k^{\top} x_k^{\text{obs}}) - 1}{2} \right)
  $$

- **人体网格恢复（HMR）**：通过 SMPL 模型 $M(\beta, x)$ 从姿态 $x$ 和体型 $\beta$ 生成网格与 3D 关键点，计算加权鲁棒重投影误差：
  $$
  \mathcal{L}_{\text{2D}}(x, \beta) = \operatorname{diag}(\sigma) \, \rho(p_k^{\text{obs}} - \Pi(\mathcal{I}(M(\beta, x))))
  $$
  其中 $\Pi$ 为相机投影，$\rho$ 为 Geman-McClure 鲁棒函数。

**关键设计决策**：所有损失均在流形终点 $x_1$ 上计算，梯度通过 ODE 轨迹反向传播至源点 $x_0$。这种“通过采样过程优化”的范式使得 PoseRFM 的先验知识能够有效约束解空间，避免传统优化方法中的非真实姿态。

### 补充图表

![[assets/figures/papers/paper_list_l1001_https_openaccess_thecvf_com_content_CVPR2026_html_Nadar_PoseD_Flow_Versa/figures/002_Figure_2.jpg]]
*Figure 2: Implicit bias: The source point update steers the endpoint gradient towards the reachable subspace induced by the data*

## 实验与分析

PoseD-Flow 的实验评估围绕三个核心维度展开：**无条件生成的逼真度与多样性**、**逆问题求解的精度与鲁棒性**，以及**几何建模组件的因果贡献**。实验在 AMASS 数据集上进行训练与评估，覆盖姿态补全、运动去噪、人体网格恢复（HMR）等任务，并与扩散模型、VAE、神经距离场等代表性先验方法进行系统对比。

### 无条件姿态生成

PoseRFM 在无条件生成任务上取得了最优的逼真度-多样性平衡。如 Table 1 所示，PoseRFM（N=1000）的 FID 达到 **0.013**，显著优于扩散模型 DPoser（0.019，Lu et al., ICCV 2025）和 VAE 方法 VPoser（Pavlakos et al., CVPR 2019）。在最近邻距离 d_NN 上，PoseRFM（N=100）取得 **0.069** 的最低值，表明生成样本与真实数据分布的高度吻合。同时，平均成对距离 APD 达到 15.544 cm，说明模型在保持高逼真度的同时并未牺牲多样性。Figure 3 展示了 PoseRFM 的无条件生成样本，姿态自然且符合人体运动学约束。

![[assets/figures/papers/paper_list_l1001_https_openaccess_thecvf_com_content_CVPR2026_html_Nadar_PoseD_Flow_Versa/figures/004_Table_1.jpg]]
*Table 1: Results for unconditional pose generation. Last three rows indicate our models*

![[assets/figures/papers/paper_list_l1001_https_openaccess_thecvf_com_content_CVPR2026_html_Nadar_PoseD_Flow_Versa/figures/003_Figure_3.jpg]]
*Figure 3: PoseRFM samples from unconditional generation*

### 姿态补全

在多种遮挡条件下的姿态补全任务中，Riemannian D-Flow 引导的 PoseRFM 在精度（MPVPE）与多样性（APD）之间取得了最佳平衡（Table 2）。当遮挡左腿时，PoseRFM 的 MPVPE 降至 **83.81 mm**，优于 DPoser 等对比方法。Figure 4 的定性结果显示，即使在腿部或手臂完全不可见的情况下，模型仍能生成符合人体运动学且与可见关节一致的补全姿态。这一优势源于 Riemannian D-Flow 在 SO(3) 乘积流形上进行源点优化时，梯度更新天然受到数据局部协方差和流形曲率的共同塑形（Figure 2），使优化过程偏向高密度、真实姿态区域。

![[assets/figures/papers/paper_list_l1001_https_openaccess_thecvf_com_content_CVPR2026_html_Nadar_PoseD_Flow_Versa/figures/005_Table_2.jpg]]
*Table 2: Pose Completion results under varying occlusion scenarios. We report MPVPE (mm) and APD (cm) metrics*

![[assets/figures/papers/paper_list_l1001_https_openaccess_thecvf_com_content_CVPR2026_html_Nadar_PoseD_Flow_Versa/figures/007_Figure_4.jpg]]
*Figure 4: Completed poses with legs (top row) and arms (bottom row) occluded. Visible and occluded joints*

### 运动去噪

Table 3 报告了不同高斯噪声水平下的运动去噪结果。在 40 mm 噪声水平下，PoseRFM 取得 **18.88 mm** 的 MPJPE，优于所有对比方法。值得注意的是，即使在极端噪声（100 mm）下，模型仍能稳定恢复合理的姿态序列，验证了 Riemannian 流形先验对噪声扰动的鲁棒性。

### 人体网格恢复

在 EHF 数据集上的 HMR 任务中（Table 4, Table 5），PoseD-Flow 从零初始化（from scratch）即可取得 **54.85 mm** 的 PA-MPJPE，优于 DPoser 等方法。Figure 5 展示了在 3DPW 野外图像上的定性结果：无论是从零拟合还是以 CLIFF 初始化，模型均能恢复出与图像观测一致的合理三维人体姿态。这得益于 Riemannian D-Flow 在逆求解过程中通过微分 ODE 反向传播，自动将二维重投影损失（Eq. HMR）转化为流形上的源点更新，无需针对特定任务进行额外训练。

![[assets/figures/papers/paper_list_l1001_https_openaccess_thecvf_com_content_CVPR2026_html_Nadar_PoseD_Flow_Versa/figures/008_Table_4.jpg]]
*Table 4: Human Mesh Recovery on EHF [53] dataset. We report PA-MPJPE (mm)*

![[assets/figures/papers/paper_list_l1001_https_openaccess_thecvf_com_content_CVPR2026_html_Nadar_PoseD_Flow_Versa/figures/009_Figure_5.jpg]]
*Figure 5: Results of HMR on in-the-wild images from 3DPW [64]. Fitting from scratch (top) and init. using CLIFF [36] (bottom)*

![[assets/figures/papers/paper_list_l1001_https_openaccess_thecvf_com_content_CVPR2026_html_Nadar_PoseD_Flow_Versa/figures/010_Table_5.jpg]]
*Table 5: Detailed HMR evaluation with additional metrics*

### 几何组件的因果消融

Table 6 的消融实验揭示了三个几何设计的关键因果作用：

![[assets/figures/papers/paper_list_l1001_https_openaccess_thecvf_com_content_CVPR2026_html_Nadar_PoseD_Flow_Versa/figures/011_Table_6.jpg]]
*Table 6: Ablation study on the effect of geometric components*

1. **Riemannian 流形 vs. 欧几里得空间**：将建模空间从 SO(3)^K 乘积流形退化为欧几里得空间的 PoseFM 基线，在姿态补全任务上 MPVPE 显著上升、APD 下降，证明直接在流形上建模是性能提升的根本前提。

2. **测地损失（geodesic loss）**：移除测地距离损失并替换为欧几里得损失，导致补全精度和多样性同时恶化，表明测地度量能更准确地刻画关节旋转空间的结构。

3. **轨迹正则项（L_traj）**：移除轨迹正则项后，模型在遮挡场景下倾向于产生不合理的突变旋转，MPVPE 明显升高。L_traj 通过惩罚轨迹中的大角度旋转（Eq. 11），有效抑制了逆求解过程中的几何不稳定。

### 失败模式与局限性

尽管 PoseD-Flow 在多个任务上表现优异，仍需注意以下局限：

- **内存与实时性**：Riemannian D-Flow 的逆求解依赖微分 ODE 的反向传播，每次迭代需完整求解前向 ODE 并存储计算图，内存消耗较大，当前不适合实时应用。
- **模型泛化**：训练与评估均基于 SMPL 身体模型，扩展到 MANO（手部）或 FLAME（面部）等其他参数化模型需要重新训练 PoseRFM 先验。
- **多样性注入**：当前 D-Flow 引导过程是确定性的，在需要多样化解的下游任务中，可通过在源点优化中引入受控随机扰动来提升生成多样性。
- **时序建模缺失**：当前框架仅处理单帧静态姿态，未建模运动序列的时序依赖关系。

## 方法谱系与知识库定位

### 1. 核心瓶颈与突破路径

PoseD-Flow 的提出直指流匹配（Flow Matching）在人体姿态建模中尚未被应用的两大根本障碍：

- **缺少预训练的流先验**：此前流匹配在图像、分子等欧几里得域取得进展，但从未被构建为可复用的铰接人体姿态先验。
- **姿态空间的非欧几里得本质**：人体姿态由关节旋转构成，自然定义在 SO(3) 乘积流形上，直接将标准流匹配应用于欧几里得关节空间会忽视旋转的几何约束，导致生成质量下降。

论文的因果旋钮在于：**在 SO(3)^K 乘积流形上构建 Riemannian Flow Matching 模型（PoseRFM）作为姿态先验，并通过微分黎曼 ODE 采样过程实现免训练的引导逆求解（Riemannian D-Flow）**。这一组合同时解决了先验缺失和几何适配两个瓶颈。

### 2. 相对于现有基线的定位

#### 2.1 姿态先验谱系

PoseRFM 在姿态先验的演进中占据“**流形原生 + 连续归一化流**”这一新位置，与已有方法形成清晰对比：

| 方法 | 先验类型 | 建模空间 | 生成机制 |
|------|----------|----------|----------|
| **VPoser** (Pavlakos et al., CVPR 2019) | VAE | 欧几里得隐空间 | 采样隐变量再解码 |
| **Pose-NDF** (Tiwari et al., ECCV 2022) | 神经距离场 | 欧几里得关节空间 | 隐式表面建模 |
| **GFPose** (Ci et al., CVPR 2023) | 梯度场 | 欧几里得关节空间 | 得分函数引导 |
| **NRDF** (He et al., CVPR 2024) | 神经黎曼距离场 | SO(3) 乘积流形 | 隐式距离场 |
| **DPoser** (Lu et al., ICCV 2025) | 扩散模型 | 欧几里得关节空间 | 迭代去噪采样 |
| **PoseFM**（本文基线） | 流匹配 | 欧几里得关节空间 | ODE 积分采样 |
| **PoseRFM**（本文） | 流匹配 | **SO(3)^K 乘积流形** | 黎曼 ODE 积分采样 |

**关键区分**：NRDF 虽也在 SO(3) 流形上建模，但它是隐式距离场而非生成式归一化流，无法通过 ODE 直接采样。DPoser 虽为生成式先验，但基于扩散模型，采样步骤多且缺乏流形约束。PoseRFM 首次将流匹配的快速采样优势与流形几何约束统一。

#### 2.2 逆问题求解谱系

Riemannian D-Flow 在逆问题求解中占据“**免训练 + 可微 ODE 引导**”的位置：

- **传统方法**（如 VPoser 的优化式拟合）：需针对每项任务设计损失函数，迭代优化隐变量，但梯度未受数据流形几何的塑形。
- **扩散引导方法**（如 DPoser 的 Reconstruction Guidance）：在推理时通过额外梯度步骤引导扩散采样，但采样步数多，且未考虑流形结构。
- **Riemannian D-Flow**：通过微分黎曼 ODE 对源点进行优化，梯度更新天然受到**数据局部协方差和流形曲率的共同塑形**（Figure 2 的理论分析），产生朝向高密度、真实姿态的隐式偏差。这一机制无需任务特定训练，且得益于流匹配的少步采样特性。

### 3. 改变的关键技术槽位

PoseD-Flow 相对于基线方法改变了三个核心槽位：

1. **流匹配建模空间**：从欧几里得空间（PoseFM）迁移到 SO(3)^K 乘积流形（PoseRFM）。消融实验（Table 6）表明，仅在欧几里得空间做 Flow Matching 效果明显下降，验证了流形约束的必要性。

2. **逆问题求解方式**：从固定步数的扩散采样或无引导优化，升级为可微分的黎曼 ODE 源点优化（Riemannian D-Flow）。这使得推理过程可端到端优化初始条件，而非仅依赖前向采样。

3. **引导中的正则化**：在数据损失之外增加了轨迹正则项 $\mathcal{L}_{\mathrm{traj}} = \sum_{i=1}^{K} \sum_{k=1}^{N} (3 - \mathrm{tr}(x_{ik}))$，惩罚轨迹中过大的旋转角度，防止不合理的姿态突变。消融实验（Table 6）证实该正则项对精度和多样性的平衡至关重要。

### 4. 适用边界

- **身体模型依赖**：当前训练与评估均基于 SMPL 模型，扩展到其他参数化身体模型（如 MANO 手部模型、FLAME 面部模型）需额外适配关节映射和流形结构。
- **单帧静态姿态**：PoseRFM 建模的是独立姿态分布，未编码运动时序依赖，不适用于需要时序一致性的运动生成或预测任务。
- **流形假设**：方法假设姿态可有效嵌入 SO(3)^K 乘积流形，对于包含平移、缩放等非旋转自由度的任务需额外处理。
- **观测类型**：Riemannian D-Flow 依赖可微的观测损失，目前验证了 3D 关键点、2D 重投影等损失，对其他观测模态（如深度图、点云）的适配需定义相应的可微损失函数。

### 5. 局限与开放问题

#### 5.1 已知局限

- **内存与实时性**：逆求解依赖微分 ODE 的反向传播，需存储中间激活，内存消耗较大，当前不支持实时应用。
- **多样性控制**：生成多样性（APD 指标）虽优于多数方法，但与扩散模型相比仍有提升空间，可在引导过程中引入随机扰动。
- **单帧局限**：未建模运动时序，无法直接处理运动序列的时空一致性约束。

#### 5.2 开放问题

1. **内存效率优化**：是否可以通过结合 FlowGrad 或基于最优控制的 OC-Flow 来降低微分 ODE 的内存占用，实现实时性能？
2. **可控随机性注入**：如何在逆求解中注入受控随机性，以在保持精度的同时进一步提升生成样本的多样性？
3. **时序扩展**：能否将 PoseD-Flow 框架扩展到运动序列建模，同时保持 SO(3) 流形上的几何一致性？这需要解决时序条件向量场的设计和流形上的序列积分问题。
4. **鲁棒性边界**：除遮挡和噪声外，该框架对其他类型的损坏（如传感器漂移、关节点完全缺失、异常旋转值）的鲁棒性如何？理论分析中的隐式偏差是否在这些场景下仍然有效？
5. **多身体模型泛化**：如何以最少的适配成本将 PoseRFM 先验迁移到 MANO、FLAME 等不同拓扑的身体模型？

### 6. 知识库定位总结

PoseD-Flow 在人体姿态建模知识库中确立了“**流形原生流匹配先验 + 免训练可微引导**”这一新范式。其核心贡献不是流匹配算法本身，而是**将流匹配从欧几里得空间系统性地迁移到非欧姿态流形，并证明流形几何与 ODE 微分的协同效应可产生超越扩散模型的生成质量和逆求解鲁棒性**。这一范式为后续工作在流形生成建模与结构化逆问题求解之间架设了桥梁。

## 原文 PDF

![[paperPDFs/CVPR_2026/PoseD_Flow_Versatile_and_Guided_Flow_Matching_Model_of_Human_Pose.pdf]]