---
title: Geometric Neural Distance Fields for Learning Human Motion Priors
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Geometric_Neural_Distance_Fields_for_Learning_Human_Motion_Priors.pdf
project_link: null
code_link: null
aliases:
- NRMFN
- GNDFLHMP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 在乘积流形上显式定义姿态、角速度和角加速度的联合分布，用三个条件神经距离场（NDF）的零水平集建模，并设计几何投影（RMF-Grad）和积分器（RMF-Integrator）确保物理可行性。
primary_logic: 将人体运动先验分解成姿态、过渡和加速度三层条件NDF，在SO(3)的乘积流形上通过黎曼梯度下降和投影欧拉积分，将任意噪声运动映射到合理流形，从而在一次优化中同时修正姿态、速度和加速度，捕获完整运动动力学。
claims:
- 在运动去噪任务中，NRMF的MPJPE（All）为16.4 mm，显著低于RoHM的20.9 mm和NRDF+T-NRDF的16.7 mm；加速度误差2.25，远低于RoHM的2.61。
- 在部分3D观测下，NRMF在All MPJPE（46.3 mm）和Acc Err（2.31）上均取得最低。
- 在3DPW数据集上拟合2D观测，NRMF（full）达到MPJPE 66.13 mm和Acc Err 6.52，优于其他先验组合。
- 在运动生成任务中，NRMF取得最低FIDm（5.317）和最低平均加速度范数（3.18）。
---

# Geometric Neural Distance Fields for Learning Human Motion Priors

> [!tip] 核心洞察
> 将人体运动先验分解成姿态、过渡和加速度三层条件NDF，在SO(3)的乘积流形上通过黎曼梯度下降和投影欧拉积分，将任意噪声运动映射到合理流形，从而在一次优化中同时修正姿态、速度和加速度，捕获完整运动动力学。

| 字段 | 内容 |
|------|------|
| 中文题名 | 学习人体运动先验的几何神经距离场 |
| 英文题名 | Geometric Neural Distance Fields for Learning Human Motion Priors |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.09667) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Neural Riemannian Motion Fields (NRMF) |
| Dataset | AMASS |

> [!tip] 效果简介
> - AMASS (noisy 3D) 上，MPJPE All (mm) 16.4 (NRMF) vs 20.9 (RoHM) (-4.5)；Acc Err 2.25 (NRMF) vs 2.61 (RoHM) (-0.36)；MPJPE All (mm) 16.4 (NRMF) vs 16.7 (NRDF+T-NRDF) (-0.3)。

## 概要

**研究问题**：现有的人体运动先验（如VAE、扩散模型等）主要建模姿态的静态分布或一阶过渡，普遍忽略二阶动力学（角加速度），导致运动估计中出现过平滑、时间不一致和漂移等问题；同时，它们缺乏在乘积流形上对关节间相互依赖性的联合建模。

**核心方法**：本文提出**Neural Riemannian Motion Fields (NRMF)**，一种通用且鲁棒的人体运动先验。其核心思想是将人体运动分解为姿态（0阶）、过渡（1阶）和加速度（2阶）三个层次，在SO(3)乘积流形上分别用三个条件神经距离场（NDF）的零水平集进行建模。具体而言，$f_{\Gamma} = [f_{\Phi}^R(\theta); f_{\Psi}^\omega(\dot{\theta} \mid \theta); f_{\Xi}^{\dot{\omega}}(\ddot{\theta} \mid \theta, \dot{\theta})]$ 联合预测任意运动状态到合理流形的测地距离。在此基础上，设计了**RMF-Grad**（三阶段自适应混合黎曼梯度下降投影）和**RMF-Integrator**（几何投影欧拉积分器），确保从加速度到姿态的物理可行演化，在一次优化中同时修正姿态、速度和加速度。

**核心发现**：NRMF通过捕获完整的运动动力学，在多项任务上一致超越现有方法：
- **运动去噪**（Table 1）：MPJPE（All）降至16.4 mm，低于RoHM的20.9 mm和NRDF+T-NRDF的16.7 mm；加速度误差2.25，远低于RoHM的2.61。
- **部分观测恢复**（Table 2）：All MPJPE 46.3 mm，Acc Err 2.31，均为最低。
- **2D观测拟合**（Table 3, 3DPW）：MPJPE 66.13 mm，Acc Err 6.52，优于其他先验组合。
- **运动生成**（Table 4）：FIDm最低（5.317），平均加速度范数最低（3.18），生成的运动更平滑自然。
- 在i3DB、PROX、EgoBody等多个真实世界数据集上均表现最优（Tables 5-7）。

**方法定位**：NRMF在神经距离场先验（如NRDF）的基础上，首次将二阶动力学显式纳入乘积流形表示，填补了现有先验（VPoser、HuMoR、RoHM、MDM等）在加速度建模上的空白。其投影和积分算法为在黎曼流形上处理时序运动数据提供了新范式。



### 人体运动先验的核心挑战

从视觉观测中估计或生成逼真的人体运动，是计算机视觉与图形学中的基础难题。其核心困难在于：人体运动天然存在于一个高度非线性、高维且受物理约束的流形上，而观测数据往往是稀疏、含噪或部分遮挡的。因此，一个强健的运动先验成为连接“观测”与“合理运动”之间不可或缺的桥梁。

现有的运动先验方法通常将运动视为姿态序列，并采用生成模型（如VAE、扩散模型或归一化流）来学习其分布。然而，这些方法存在一个共同的**瓶颈**：它们未能充分建模运动的**二阶动力学**——即加速度信息。这直接导致了三个相互关联的典型失败模式：

1. **过平滑与时间不一致**：缺乏对加速度的显式约束，使得生成或恢复的运动在时序上趋于平均化，丢失了运动中的细微动态变化。
2. **物理漂移**：在长序列优化或生成中，姿态误差会随时间累积，导致肢体长度变化、脚部滑动等物理上不可行的结果。
3. **关节间依赖建模不足**：大多数方法将各关节的动力学独立处理，忽略了人体运动中关节间协同与制约的强相互依赖性。

### 现有方法的缺口

当前主流运动先验可以按其建模的动力学阶数进行划分：

- **零阶先验（仅姿态）**：如**VPoser**（VAE）、**Pose-NDF**（神经距离场）和**NRDF**（黎曼NDF）等方法，仅建模单帧姿态的合理性。它们虽然能约束静态姿态，但完全无法捕捉运动的时间结构，在时序任务中容易产生抖动和不连续。
- **一阶先验（姿态+过渡）**：如**HuMoR**（VAE）和**RoHM**（扩散模型+物理）等方法，同时建模姿态和帧间变化（角速度）。这在一定程度上改善了时间平滑性，但仍缺乏对加速度的直接约束——而加速度恰恰是决定运动“力度”与“锐度”的二阶量。
- **二阶先验的缺失**：扩散模型（如**MDM**）或流模型（如**NeMF**）虽然在生成质量上表现优异，但其隐式建模方式并未在几何流形上显式定义加速度的合理分布，导致在优化恢复任务中难以有效利用二阶信息。

这种“阶数缺失”的根本原因在于：在非欧几里得流形（即SO(3)的乘积空间）上，同时定义姿态、速度和加速度的联合分布，并设计相应的投影与积分算法，是一项极具挑战性的几何与计算问题。

### 本文的动机与核心思路

针对上述缺口，本文的核心动机是：**能否在乘积流形上显式建模人体运动的完整动力学链（姿态→速度→加速度），并通过几何方法将任意噪声运动“投影”回合理流形？**

为此，本文提出**Neural Riemannian Motion Fields（NRMF）**，其核心洞察在于：

> 将人体运动先验分解为三个条件神经距离场（NDF）的零水平集——分别对应姿态（0阶）、过渡（1阶）和加速度（2阶）——并在SO(3)的乘积流形上，通过黎曼梯度下降和几何投影欧拉积分，在一次优化中同时修正姿态、速度和加速度，从而捕获完整的运动动力学。

这一设计使得NRMF能够从根本上解决过平滑和物理漂移问题：加速度先验直接约束运动的二阶行为，而几何投影算法确保优化轨迹始终保持在合理流形上。后续章节将详细展开这一方法的技术实现与实验验证。



## 核心方法与创新机理

NRMF 的核心创新在于将人体运动先验从静态姿态或一阶过渡建模，**系统性地提升至包含加速度的二阶动力学联合建模**，并在乘积黎曼流形上设计了配套的几何投影与积分算法，确保物理可行性。以下从三个 changed slots 展开其相对于现有方法的本质差异。

### 1. 运动表示维度：从 0/1 阶到 0–1–2 阶联合建模

现有运动先验在表示维度上存在结构性缺失：
- **姿态先验**（VPoser、Pose-NDF、NRDF 等）仅建模单帧姿态的合理性，完全忽略帧间动力学；
- **一阶运动先验**（HuMoR、RoHM、MDM 等）虽引入过渡（速度）信息，但未显式建模加速度，导致运动估计中普遍存在过平滑、时间不一致和漂移问题。

NRMF 将状态空间扩展为 **姿态、角速度、角加速度的乘积流形**：

$$\mathbf{X} = [\mathbf{t}_{\mathrm{r}} \ \pmb{\theta} \ \pmb{\dot{\theta}} \ \ddot{\pmb{\theta}}] \in (\mathbb{R}^3 \times \mathcal{M})$$

其中 $\mathcal{M} = \mathrm{SO}(3)^{N_J} \times \mathfrak{so}(3)^{N_J} \times \mathbb{R}^{3 \times N_J}$。这一表示使得先验能够同时约束**关节在哪里、向哪里运动、以及运动如何变化**，从而在一次优化中捕获完整的运动动力学。消融实验（Table 1）直接验证了维度扩展的收益：在 NRDF（仅姿态）基础上添加过渡 NDF 将 MPJPE 从 22.8 mm 降至 16.7 mm，进一步添加加速度 NDF 降至 16.4 mm；加速度误差从 3.12 经 2.97 最终降至 2.25。

### 2. 动力学先验形式：三层条件神经距离场

与 VAE、扩散模型等生成式先验不同，NRMF 采用**三个条件神经距离场（NDF）**建模不同阶动力学的合理性，每个 NDF 预测当前状态到最近合理样本的测地距离：

$$f_{\Gamma} = [f_{\Phi}^R(\theta);\ f_{\Psi}^\omega(\dot{\theta} \mid \theta);\ f_{\Xi}^{\dot{\omega}}(\ddot{\theta} \mid \theta, \dot{\theta})]$$

这一设计的核心洞察在于**显式建模关节间的相互依赖性与阶次间的条件关系**：
- **$f_{\Phi}^R$**：姿态 NDF，建模关节旋转在 $\mathrm{SO}(3)^{N_J}$ 上的联合分布；
- **$f_{\Psi}^\omega$**：过渡 NDF，以当前姿态为条件，建模角速度的合理性——同一姿态下不同运动方向的合理性不同；
- **$f_{\Xi}^{\dot{\omega}}$**：加速度 NDF，以姿态和速度共同为条件，建模加速度的合理性——捕获运动趋势的物理约束。

这种条件分层设计使得先验能够区分“静态合理但动态不可能”的状态组合，而传统单帧先验或无条件生成模型无法做到这一点。

### 3. 投影/集成算法：RMF-Grad 与 RMF-Integrator

现有方法通常采用标准梯度下降或无几何约束的欧拉积分，忽略了 $\mathrm{SO}(3)$ 流形的黎曼几何结构。NRMF 提出了两个在乘积流形上操作的几何算法：

- **RMF-Grad**（三阶段自适应混合梯度下降）：沿 NDF 的黎曼梯度方向投影，将任意噪声状态拉回零水平集。姿态更新遵循 $\mathrm{SO}(3)$ 上的指数映射：

$$\theta_{t+1} = \Pi^{R}(\theta_t) = \mathrm{Exp}_{\theta_t}\left(-\alpha_\theta f_{\Phi}^R(\theta_t) \frac{\mathrm{grad} f_{\Phi}^R(\theta_t)}{\|\mathrm{grad} f_{\Phi}^R(\theta_t)\|}\right)$$

速度与加速度的投影类似，但分别在切空间和欧氏空间中操作，确保每一步更新都保持在物理可行的流形上。

- **RMF-Integrator**（几何投影欧拉积分）：将连续动力学离散化为投影欧拉步，从加速度序列生成或修正运动轨迹。速度更新为 $\dot{\pmb{\theta}}_{t+1} = \Pi^{\omega}(\dot{\pmb{\theta}}_t + \lambda_t \ddot{\pmb{\theta}}_t)$，姿态更新为 $\pmb{\theta}_{t+1} = \Pi^{R}(\mathrm{Exp}_{\pmb{\theta}_t}(\alpha_t [\dot{\pmb{\theta}}_t]_{\times}))$。通过在每一步积分后施加 NDF 投影，RMF-Integrator 有效抑制了误差累积和漂移。

这两个算法的组合使得 NRMF 既能作为优化中的正则化项（通过 RMF-Grad），也能作为运动生成器（通过 RMF-Integrator 从噪声加速度序列生成合理运动），在去噪、补间、生成等多种任务中统一发挥作用。

### 创新总结

NRMF 的 changed slots 构成了一条完整的因果链：**更高维的表示**（0–2 阶联合）提供了约束运动动力学的可能性，**条件 NDF 先验**将这种可能性转化为可微的距离度量，**几何投影/积分算法**则确保优化和生成过程始终尊重 $\mathrm{SO}(3)$ 的流形结构。三者缺一不可，共同解释了 NRMF 在运动去噪（MPJPE 16.4 mm vs. RoHM 20.9 mm）、部分观测恢复（All MPJPE 46.3 mm）和运动生成（FIDm 5.317）等任务上的系统性提升。



NRMF 将人体运动先验构建为三个条件神经距离场（NDF）的零水平集，分别对应运动的第零阶（姿态）、第一阶（角速度过渡）和第二阶（角加速度）动力学，并在 SO(3) 的乘积流形上显式建模这些量的联合分布。

**核心思想**：传统运动先验（VAE、扩散模型等）通常仅建模姿态或姿态与过渡的一阶关系，导致运动估计过平滑、时间不一致和漂移。NRMF 的关键洞察是将姿态、过渡和加速度作为相互依赖的隐式曲面来建模——三个 NDF 分别预测输入到合理样本集的测地距离，从而在一次优化中同时修正姿态、速度和加速度，捕获完整运动动力学。

**整体流程**：

1. **运动状态表示**：人体运动状态定义为 $\mathbf{X} = [\mathbf{t}_{\mathrm{r}} \ \pmb{\theta} \ \pmb{\dot{\theta}} \ \ddot{\pmb{\theta}}] \in (\mathbb{R}^3 \times \mathcal{M})$，其中 $\mathbf{t}_{\mathrm{r}}$ 为根位移，$\pmb{\theta}$ 为关节角（旋转矩阵），$\pmb{\dot{\theta}}$ 为角速度，$\ddot{\pmb{\theta}}$ 为角加速度。所有旋转量均在 SO(3) 乘积流形上操作，严格尊重关节运动的底层几何。

2. **三层条件 NDF 建模**：
   - **姿态 NDF** $f_{\Phi}^R(\theta)$：预测给定姿态到合理姿态集的测地距离，用于投影姿态。
   - **过渡 NDF** $f_{\Psi}^{\omega}(\dot{\theta} \mid \theta)$：在给定姿态条件下预测角速度的合理性距离，用于投影过渡。
   - **加速度 NDF** $f_{\Xi}^{\dot{\omega}}(\ddot{\theta} \mid \theta, \dot{\theta})$：在给定姿态和速度条件下预测角加速度的合理性距离，用于投影加速度。
   
   三者组合为联合隐式函数 $f_{\Gamma} = [f_{\Phi}^R(\theta); f_{\Psi}^{\omega}(\dot{\theta} \mid \theta); f_{\Xi}^{\dot{\omega}}(\ddot{\theta} \mid \theta, \dot{\theta})]$，其零水平集定义了合理运动的流形。

3. **几何投影与积分器**：
   - **RMF-Grad**：三阶段自适应混合梯度下降，在乘积流形上沿黎曼梯度方向将任意噪声运动投影到零水平集附近。
   - **RMF-Integrator**：几何投影欧拉积分器，从加速度序列生成或修正运动轨迹——速度更新通过 $\dot{\pmb{\theta}}_{t+1} = \Pi^{\omega}(\dot{\pmb{\theta}}_t + \lambda_t \ddot{\pmb{\theta}}_t)$ 投影，姿态更新通过 $\pmb{\theta}_{t+1} = \Pi^{R}(\mathrm{Exp}_{\pmb{\theta}_t}(\alpha_t [\dot{\pmb{\theta}}_t]_{\times}))$ 投影，确保每一步都保持在合理流形上。

4. **测试时优化**：采用两阶段优化策略——
   - **阶段 I**：仅使用姿态先验 $f_{\Phi}^R$ 和形状先验进行初始化，目标函数为 $E_I(\mathbf{t}_{\mathrm{r}}, \theta, \beta) = \mathcal{L}_{\mathrm{data}} + \lambda_{\beta} \mathcal{L}_{\beta} + \lambda_{\theta} \mathcal{L}_{\theta} + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}}$。
   - **阶段 II**：引入过渡先验损失 $\mathcal{L}_{\dot{\theta}} := f_{\Psi}^{\omega}(\dot{\theta}_i)$ 和加速度先验损失 $\mathcal{L}_{\ddot{\theta}} := f_{\Xi}^{\dot{\omega}}(\ddot{\theta}_i)$，形成完整优化目标 $E_{II}'(\mathbf{t}_{\mathrm{r}}, \theta, \beta) = \mathcal{L}_{\mathrm{data}} + \lambda_{\beta} \mathcal{L}_{\beta} + \lambda_{\theta} \mathcal{L}_{\theta} + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}} + \lambda_{\dot{\theta}} \mathcal{L}_{\dot{\theta}} + \lambda_{\ddot{\theta}} \mathcal{L}_{\ddot{\theta}}$，结合数据项和三个 NDF 先验联合恢复运动。

**输入输出流**：NRMF 作为通用无条件运动先验，接受任意噪声或部分观测的运动序列作为输入，通过测试时优化输出物理合理、时间一致的运动估计。该框架可灵活部署于运动去噪、部分观测补全、2D 观测拟合、运动生成和稀疏关键帧插值等多种下游任务。

### 补充图表

![[assets/figures/papers/paper_list_l1026_https_arxiv_org_abs_2509_09667/figures/002_Figure_2.jpg]]
*Figure 2: Neural Riemannian Motion Fields (NRMF) models the motion in the zero-level-set of three disjoint distance fields*



NRMF 将人体运动先验建模为乘积流形上的三个条件神经距离场，并设计几何投影与积分算法确保物理可行性。本节聚焦其核心组件与关键公式。

### 1. 乘积流形上的运动表示

人体运动状态定义在旋转群与欧氏空间的乘积流形上。首先，单个关节的旋转矩阵属于特殊正交群：

$$
\mathrm{SO}(3) = \{ \mathbf{R} \in \mathbb{R}^{3 \times 3} : \mathbf{R}^{\top} \mathbf{R} = \mathbf{I}, \det(\mathbf{R}) = 1 \}
$$

其切空间由左不变向量场定义：

$$
\mathcal{T}_{\mathbf{R}} \mathrm{SO}(3) = \{ \mathbf{R} \boldsymbol{\Omega} : \boldsymbol{\Omega} \in \mathfrak{so}(3) \}
$$

对于具有 $N_J$ 个关节的人体骨架，完整运动状态 $\mathbf{X}$ 由根位移、关节角、角速度和角加速度组成：

$$
\mathbf{X} = [\mathbf{t}_{\mathrm{r}} \ \pmb{\theta} \ \pmb{\dot{\theta}} \ \ddot{\pmb{\theta}}] \in (\mathbb{R}^3 \times \mathcal{M})
$$

其中 $\mathcal{M} = \mathrm{SO}(3)^{N_J} \times \mathbb{R}^{3N_J} \times \mathbb{R}^{3N_J}$ 为乘积流形。角加速度通过旋转矩阵的时间导数定义：

$$
\frac{\mathrm{d} [\omega_t]_{\times}}{\mathrm{d} t} := [\dot{\omega}_t]_{\times} := \ddot{\mathbf{R}}_t = \mathbf{R}_t \left(\Omega_t^2 + \dot{\Omega}_t\right)
$$

### 2. 三层条件神经距离场（Riemannian Motion Fields）

NRMF 的核心是将合理运动流形建模为三个条件 NDF 的零水平集（见 Figure 2）。每个 NDF 预测输入到最近合理样本的测地距离：

$$
f_{\Gamma} = [f_{\Phi}^R(\theta); f_{\Psi}^\omega(\dot{\theta} \mid \theta); f_{\Xi}^{\dot{\omega}}(\ddot{\theta} \mid \theta, \dot{\theta})]
$$

三个组件分别对应：

- **姿态 NDF** $f_{\Phi}^R: \mathrm{SO}(3)^{N_J} \to \mathbb{R}_+$：预测关节旋转的合理性距离，捕捉静态姿态分布 $p(\theta)$。
- **过渡 NDF** $f_{\Psi}^\omega: \mathfrak{so}(3)^{N_J} \to \mathbb{R}_+$：以当前姿态为条件，预测角速度的合理性距离，捕捉 $p(\dot{\theta} \mid \theta)$。
- **加速度 NDF** $f_{\Xi}^{\dot{\omega}}: \mathbb{R}^{3 \times N_J} \to \mathbb{R}_+$：以当前姿态和速度为条件，预测角加速度的合理性距离，捕捉 $p(\ddot{\theta} \mid \theta, \dot{\theta})$。

这种条件分解显式建模了姿态、速度和加速度之间的相互依赖性，这是现有方法（如 **NRDF** 仅建模姿态、**HuMoR** 仅建模姿态与过渡的 VAE 先验）所缺失的。

### 3. 几何投影：RMF-Grad

为将任意噪声运动映射回流形，NRMF 设计了基于黎曼梯度的投影算子。姿态投影步为：

$$
\theta_{t+1} = \Pi^{R}(\theta_t) = \mathrm{Exp}_{\theta_t}\left(-\alpha_\theta f_{\Phi}^R(\theta_t) \frac{\mathrm{grad} f_{\Phi}^R(\theta_t)}{\|\mathrm{grad} f_{\Phi}^R(\theta_t)\|}\right)
$$

该公式沿距离场梯度方向在 $\mathrm{SO}(3)$ 流形上进行测地线步进。步长由当前距离值 $f_{\Phi}^R(\theta_t)$ 自适应调节——距离越大步长越大，接近流形时步长自动减小。$\Pi^{\omega}$ 和 $\Pi^{\dot{\omega}}$ 分别在速度空间和加速度空间执行类似投影。

RMF-Grad 采用三阶段自适应混合梯度下降：先投影姿态，再投影速度，最后投影加速度，逐步将完整运动状态拉回合理流形。

### 4. 几何积分器：RMF-Integrator

RMF-Integrator 将投影操作嵌入欧拉积分，从加速度序列生成物理上可行的运动轨迹。速度更新为投影欧拉步：

$$
\dot{\pmb{\theta}}_{t+1} = \Pi^{\omega}(\dot{\pmb{\theta}}_t + \lambda_t \ddot{\pmb{\theta}}_t)
$$

姿态更新结合指数映射与投影：

$$
\pmb{\theta}_{t+1} = \Pi^{R}\left(\mathrm{Exp}_{\pmb{\theta}_t}\left(\alpha_t [\dot{\pmb{\theta}}_t]_{\times}\right)\right)
$$

两步交替执行：先用投影后的加速度更新速度，再用投影后的速度通过指数映射更新姿态，随后再次投影姿态。这确保了整个积分轨迹始终保持在合理运动流形附近，从根本上抑制了标准欧拉积分的漂移和发散问题。

### 5. 测试时优化目标

在下游任务中，NRMF 采用两阶段优化。第一阶段仅使用姿态先验进行初始化：

$$
E_I(\mathbf{t}_{\mathrm{r}}, \theta, \beta) = \mathcal{L}_{\mathrm{data}} + \lambda_\beta \mathcal{L}_\beta + \lambda_\theta \mathcal{L}_\theta + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}}
$$

第二阶段引入过渡和加速度先验损失，它们直接定义为对应 NDF 的输出值：

$$
\mathcal{L}_{\dot{\theta}} := f_{\Psi}^\omega(\dot{\theta}_i), \quad \mathcal{L}_{\ddot{\theta}} := f_{\Xi}^{\dot{\omega}}(\ddot{\theta}_i)
$$

完整优化目标为：

$$
E_{II}'(\mathbf{t}_{\mathrm{r}}, \theta, \beta) = \mathcal{L}_{\mathrm{data}} + \lambda_\beta \mathcal{L}_\beta + \lambda_\theta \mathcal{L}_\theta + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}} + \lambda_{\dot{\theta}} \mathcal{L}_{\dot{\theta}} + \lambda_{\ddot{\theta}} \mathcal{L}_{\ddot{\theta}}
$$

该目标在一次联合优化中同时修正姿态、速度和加速度，捕获完整的二阶运动动力学。消融实验（Table 1）证实：在 NRDF 基础上添加过渡 NDF（T-NRDF）将 MPJPE 从 22.8 mm 降至 16.7 mm，进一步添加加速度 NDF（A-NRDF，即完整 NRMF）降至 16.4 mm，同时加速度误差从 2.97 降至 2.25，验证了二阶动力学建模的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l1026_https_arxiv_org_abs_2509_09667/figures/014_Figure_7.jpg]]
*Figure 7: Illustration of angular velocity and accelaration for two points on a manifold. Given two points on the manifold (pi), the velocities are vectors in the tangent planes at those points. In practice, to compute an angular acceleration, they are parallel transported to the tangent space of the identity and then compared. If the points are close enough, the variation of the tangent spaces are ignored, and the computation is carried out by directly comparing vectors. Sphere is chosen for illustration purposes whereas the manifold or articulated bodies is higher dimensional*



## 实验与关键发现

### 核心实验设置

NRMF 的训练与评估均基于 AMASS 数据集的标准划分，所有对比方法在相同数据划分下进行。对于扩散模型基线 **MDM**，作者将其重新训练以适配四元数表示并具备去噪能力，确保对比公平性。在 PROX 等真实场景数据集上，采用与 **RoHM** 一致的现成回归器获取逐帧初始化。

### 运动去噪：二阶动力学的决定性作用

Table 1 报告了从含噪 3D 观测中进行运动与形状估计的结果。NRMF 在所有指标上均取得最优：**MPJPE (All) 16.4 mm**，显著低于 RoHM 的 20.9 mm 和 NRDF+T-NRDF 的 16.7 mm；**加速度误差 2.25**，远低于 RoHM 的 2.61。

![[assets/figures/papers/paper_list_l1026_https_arxiv_org_abs_2509_09667/figures/004_Table_1.jpg]]
*Table 1: Motion and shape estimation from noisy 3D observations (motion denoising)*

消融实验直接揭示了二阶动力学建模的因果贡献：
- 在 NRDF（纯姿态先验）基础上添加过渡 NDF（T-NRDF），将 MPJPE 从 22.8 mm 降至 16.7 mm，加速度误差从 4.60 降至 2.97；
- 进一步添加加速度 NDF（A-NRDF，即完整 NRMF），MPJPE 降至 16.4 mm，加速度误差降至 2.25。

这表明**过渡先验是提升位置精度的主要驱动力，而加速度先验进一步抑制了高频抖动，使加速度误差逼近真实运动水平**。Figure 4 显示 NRMF 在不同噪声水平下均保持较低误差，表现出比现有方法更强的鲁棒性——当噪声增大时，其他方法迅速过平滑或漂移，而 NRMF 的误差增长更为平缓。

![[assets/figures/papers/paper_list_l1026_https_arxiv_org_abs_2509_09667/figures/008_Figure_4.jpg]]
*Figure 4: Behavior of differentlower errors for visible body methods for increasing levels ofparts, the model suffers noise.from over-smoothing and*

### 部分观测与真实场景：一致领先

在部分 3D 观测条件下（Table 2），NRMF 在 All MPJPE（46.3 mm）和 Acc Err（2.31）上均取得最低。在 3DPW 数据集上拟合 2D 观测（Table 3），NRMF（full）达到 MPJPE 66.13 mm 和 Acc Err 6.52，优于其他先验组合。Figure 5 的定性对比显示，NRMF 恢复的紫色身体部位在部分观测和运动补间任务中均比 [22, 63] 更符合解剖学合理性。

![[assets/figures/papers/paper_list_l1026_https_arxiv_org_abs_2509_09667/figures/006_Table_2.jpg]]
*Table 2: Motion and shape estimation from partial 3D observations*

![[assets/figures/papers/paper_list_l1026_https_arxiv_org_abs_2509_09667/figures/007_Table_3.jpg]]
*Table 3: Ftting to 2D obsertations on 3DPW. We compare the refinement results after optimizing SMPLer-X [8] with different prior terms. MPJPE and MPVPE are in millimeters*

![[assets/figures/papers/paper_list_l1026_https_arxiv_org_abs_2509_09667/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison with state-of-the-art methods [22, 63] on motion estimation from noisy partial observation (top two) and motion in-between (bottom two) where the purple body parts represent the recovered motion*

在真实世界数据集上（i3DB、PROX、EgoBody，Tables 5-7），NRMF 一致超越现有方法。Figure 6 和 Figure 12 的定性结果表明，即使在遮挡、背景杂乱等挑战条件下，NRMF 仍能恢复出更合理、时间一致且解剖学准确的运动。

![[assets/figures/papers/paper_list_l1026_https_arxiv_org_abs_2509_09667/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparison with state-of-the-art methods for in-the-wild motion estimation*

### 运动生成：FID 与物理合理性双优

Table 4 报告了姿态与运动生成任务的定量分析。NRMF 取得最低 **FIDm（5.317）** 和最低平均加速度范数（3.18），表明生成的运动既接近真实分布，又具有物理合理性。这验证了将加速度显式建模为零水平集可以自然约束生成运动的二阶平滑性。

![[assets/figures/papers/paper_list_l1026_https_arxiv_org_abs_2509_09667/figures/010_Table_4.jpg]]
*Table 4: Quantitative analysis of pose and motion generation*

### 失败模式与局限性

尽管 NRMF 在各项任务中表现优异，但存在以下局限：
- **推理效率**：迭代优化导致较长运行时间，处理 10 秒视频约需 6 分钟，不适合实时应用；
- **分布外泛化**：方法依赖于 AMASS 的训练分布，对极端或训练集中未出现的姿态可能泛化有限；
- **理论完备性**：投影积分器 RMF-Integrator 缺乏严格的理论理解，无法证明其最优性。

### 补充图表

![[assets/figures/papers/paper_list_l1026_https_arxiv_org_abs_2509_09667/figures/011_Table_5.jpg]]
*Table 5: Motion and shape from RGB sequences on i3DB*

![[assets/figures/papers/paper_list_l1026_https_arxiv_org_abs_2509_09667/figures/012_Table_6.jpg]]
*Table 6: Motion estimation from RGB(-D) input on PROX*

![[assets/figures/papers/paper_list_l1026_https_arxiv_org_abs_2509_09667/figures/013_Table_7.jpg]]
*Table 7: Motion estimation results on EgoBody dataset*



## 定位与知识库关联

### 1. 方法谱系与基线对比

NRMF 的核心贡献在于将人体运动先验从低阶动力学显式扩展到二阶（加速度），并在乘积流形上进行联合建模。为理解其定位，需将其与三类基线方法进行对比：**姿态先验**、**运动先验**和**物理约束方法**。

#### 1.1 姿态先验

姿态先验仅建模单帧姿态的合理性，忽略时序动力学。

- **VPoser**：基于VAE的姿态先验，在隐空间中建模姿态分布。NRMF 与 VPoser 的根本差异在于：VPoser 仅建模 0 阶动力学（姿态），而 NRMF 在乘积流形上联合建模 0、1、2 阶动力学。在 Table 3 的 3DPW 2D 观测拟合实验中，VPoser 作为先验项时的 MPJPE 为 72.59 mm，Acc Err 为 8.07；NRMF（full）的 MPJPE 为 66.13 mm，Acc Err 为 6.52，表明二阶动力学先验对运动一致性的显著提升。

- **Pose-NDF**：将神经距离场引入姿态先验，通过零水平集隐式建模合理姿态流形。NRMF 继承了 NDF 的隐式流形建模思想，但将其从单帧姿态空间扩展到包含角速度和角加速度的乘积流形 $\mathcal{M}$。

- **NRDF**：在 SO(3) 乘积流形上建模姿态 NDF，引入黎曼梯度投影。NRMF 直接以 NRDF 为基础构建姿态分支 $f_\Phi^R(\theta)$。消融实验（Table 1）显示，单独使用 NRDF 的 MPJPE 为 22.8 mm，添加过渡 NDF（T-NRDF）后降至 16.7 mm，再添加加速度 NDF（A-NRDF，即完整 NRMF）后进一步降至 16.4 mm，证明了逐阶扩展动力学的有效性。

#### 1.2 运动先验

运动先验建模时序运动分布，但通常未显式建模加速度或缺乏几何约束。

- **HuMoR**：基于 CVAE 的运动先验，在隐空间中建模姿态-过渡联合分布。HuMoR 的局限性在于：其 VAE 框架倾向于过平滑生成，且未在乘积流形上显式建模加速度。在 Table 1 的运动去噪任务中，HuMoR 的 Acc Err 为 2.53，显著高于 NRMF 的 2.25。

- **RoHM**：结合扩散模型与物理约束的运动先验，是 NRMF 最直接的对比基线之一。RoHM 通过物理模拟器施加约束，但未在乘积流形上显式建模二阶动力学。Table 1 显示，NRMF 的 MPJPE（All）为 16.4 mm，显著低于 RoHM 的 20.9 mm；Acc Err 为 2.25，低于 RoHM 的 2.61。在 Table 2 的部分 3D 观测实验中，NRMF 同样全面优于 RoHM。

- **MDM**：基于扩散模型的运动生成方法。为保证公平对比，本文重新训练 MDM 以适配四元数表示并具备去噪能力（见 fairness_notes）。在 Table 4 的运动生成任务中，NRMF 的 FIDm 为 5.317，显著优于 MDM 的 12.306，且 NRMF 生成运动的平均加速度范数（3.18）更接近真实数据（3.05），表明二阶动力学建模对运动自然度的重要性。

- **NeMF**：基于归一化流的运动先验。NeMF 通过流模型建模运动分布，但同样未在乘积流形上显式建模加速度。NRMF 的几何投影积分器（RMF-Integrator）提供了不同于流模型采样的运动生成路径，在 Table 4 中取得了更优的生成质量。

#### 1.3 物理约束方法

部分方法通过物理模拟器或动力学方程施加约束，但通常依赖外部物理引擎，缺乏与数据驱动先验的紧密耦合。

- **RoHM** 的物理分支：RoHM 使用物理模拟器进行后处理优化，但物理约束与数据先验是分离的。NRMF 将动力学合理性直接编码在三个条件 NDF 中，通过 RMF-Integrator 在积分过程中同时满足数据约束和物理可行性，无需外部物理引擎。

### 2. 适用边界

NRMF 在以下场景表现出显著优势：

- **运动去噪与修复**：当输入包含噪声或部分缺失时，NRMF 通过三阶段投影（RMF-Grad）同时修正姿态、速度和加速度，避免过平滑和时间不一致。Table 1-2 和 Figure 4 验证了其在不同噪声水平下的鲁棒性。
- **从稀疏/2D 观测恢复运动**：在 3DPW（Table 3）、i3DB（Table 5）、PROX（Table 6）和 EgoBody（Table 7）等真实世界数据集上，NRMF 均一致超越现有方法，尤其在遮挡场景下表现出色（Figure 10, Figure 12）。
- **运动生成**：NRMF 通过 RMF-Integrator 从加速度序列生成运动，在 FIDm 和加速度自然度上优于扩散和 VAE 方法（Table 4）。

适用边界受限的场景：

- **实时应用**：迭代优化导致较长运行时间（处理 10 秒视频约需 6 分钟），不适合需要实时响应的应用。
- **极端分布外姿态**：NRMF 的三个 NDF 均基于 AMASS 数据集训练，对训练分布中未出现的极端姿态可能泛化有限。这一点在 limitations 中明确提及，但缺乏定量实验验证，需人工确认。
- **多人物交互**：当前方法仅建模单人运动，扩展到多人交互场景仍是一个开放问题。

### 3. 局限与开放问题

#### 3.1 计算效率

NRMF 的测试时优化需要迭代投影，处理 10 秒视频约需 6 分钟（见 Runtime Table）。这与 HuMoR 等 VAE 方法的前向推理速度形成鲜明对比。如何通过元学习或学习优化加速推理过程，是第一个开放问题。

#### 3.2 投影积分器的理论理解

RMF-Integrator 采用几何投影欧拉积分，在实验中被证明有效，但缺乏严格的理论理解——无法证明其最优性或收敛性保证（见 limitations）。能否将黎曼 Langevin MCMC 等原理性采样算法作为积分器，是第二个开放问题。

#### 3.3 分布外泛化

三个条件 NDF 的训练依赖于 AMASS 数据分布。对于训练集中未出现的极端姿态或高速运动，NDF 的零水平集可能无法准确刻画合理流形边界。这一局限性在论文中被承认，但缺乏系统性评估，需人工验证。

#### 3.4 多人物交互扩展

当前 NRMF 仅建模单人运动状态 $\mathbf{X} = [\mathbf{t}_{\mathrm{r}} \ \pmb{\theta} \ \pmb{\dot{\theta}} \ \ddot{\pmb{\theta}}]$，未考虑人物间交互约束。如何将乘积流形框架扩展到多人物场景，是第三个开放问题。

### 4. 知识库定位

NRMF 处于**数据驱动人体运动先验**与**黎曼几何深度学习**的交叉点。其核心贡献可总结为：

1. **动力学维度扩展**：将运动先验从 0 阶（姿态）或 1 阶（姿态+过渡）显式扩展到 2 阶（加速度），在乘积流形 $\mathbb{R}^3 \times \mathcal{M}$ 上联合建模。
2. **几何投影算法**：RMF-Grad 和 RMF-Integrator 提供了在乘积流形上进行梯度投影和欧拉积分的几何一致方法，确保生成运动满足 SO(3) 约束。
3. **条件 NDF 架构**：三个条件神经距离场 $f_\Phi^R$, $f_\Psi^\omega$, $f_\Xi^{\dot{\omega}}$ 实现了对姿态、速度和加速度相互依赖性的解耦建模。

NRMF 的下游应用覆盖运动去噪、部分观测修复、2D 观测拟合、运动生成和稀疏关键帧插值，形成了一个以乘积流形 NDF 为核心的通用运动先验框架。



## 原文 PDF

![[paperPDFs/CVPR_2026/Geometric_Neural_Distance_Fields_for_Learning_Human_Motion_Priors.pdf]]
