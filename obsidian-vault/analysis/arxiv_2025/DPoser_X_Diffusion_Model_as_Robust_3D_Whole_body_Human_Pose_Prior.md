---
title: DPoser X Diffusion Model as Robust 3D Whole body Human Pose Prior
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/DPoser_X_Diffusion_Model_as_Robust_3D_Whole_body_Human_Pose_Prior.pdf
project_link: https://dposer.github.io/
code_link: null
aliases:
- DX
- DXDMAR3WBHPP
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将无条件扩散模型作为姿态先验，结合变分扩散采样进行测试时优化；针对姿态数据特点设计截断时间步调度策略；采用混合训练策略融合部分数据集与全身数据集。
primary_logic: 扩散模型能有效学习三维人体姿态分布，其噪声预测过程可作为通用正则化项嵌入各类姿态逆问题求解；姿态关键信息集中在后期时间步，截断调度能提升优化效率并保持合理性。
claims:
- DPoser-X 在 8 个基准上最多带来 61% 的提升，全面超越现有先验如 VPoser 和 NRDF。
- 在 EHF 人体网格恢复任务中，DPoser 从零初始化获得 PA-MPJPE 56.05，优于所有对比方法。
- DPoser 在 AMASS 运动去噪上取得 MPJPE 19.87，超越专用运动先验 HuMoR。
- 截断时间步调度在全身体网格恢复消融中取得最佳 PA-MPVPE_all 60.98，优于均匀调度。
---

# DPoser X Diffusion Model as Robust 3D Whole body Human Pose Prior

> [!tip] 核心洞察
> 扩散模型能有效学习三维人体姿态分布，其噪声预测过程可作为通用正则化项嵌入各类姿态逆问题求解；姿态关键信息集中在后期时间步，截断调度能提升优化效率并保持合理性。

| 字段 | 内容 |
|------|------|
| 中文题名 | DPoser-X：基于扩散模型的鲁棒三维全身人体姿态先验 |
| 英文题名 | DPoser X Diffusion Model as Robust 3D Whole body Human Pose Prior |
| 会议/期刊 | arXiv 2025 |
| Links | [Project](https://dposer.github.io/) · [paper](https://arxiv.org/abs/2508.00599) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DPoser-X |
| Dataset | EHF, AMASS, ReInterHand, ARCTIC |

> [!tip] 效果简介
> - EHF 上，PA-MPJPE (from scratch) 56.05 vs 57.38 (NRDF) (-1.33)。
> - AMASS (motion denoising, 40mm noise) 上，MPJPE 19.87 vs 22.69 (HuMoR) (-2.82)。
> - ReInterHand (hand IK, sparse) 上，MPJPE 3.21 vs 8.25 (VPoser) (-5.04)。

## 概要

三维人体姿态先验是连接二维观测与三维重建的关键桥梁，广泛服务于人体网格恢复、运动去噪、姿态补全与生成等任务。然而，现有先验面临双重瓶颈：**表达能力受限**——高斯混合模型（GMM）或变分自编码器（VAE）难以覆盖真实姿态分布的长尾与多模态特性；**数据匮乏**——高质量全身姿态数据的稀缺进一步制约了复杂交互场景下的建模能力。这导致传统先验（如 VPoser、Pose-NDF、NRDF）在多样性与泛化性之间长期失衡。

针对上述问题，本文提出 **DPoser-X**，一种基于无条件扩散模型的三维全身人体姿态先验。其核心洞察在于：扩散模型的噪声预测过程天然刻画了数据分布的概率流，可作为通用正则化项嵌入各类姿态逆问题求解。DPoser-X 将姿态估计形式化为逆问题 $\mathbf{y} = \mathcal{A}(\mathbf{x}_0) + \mathbf{n}$，并利用变分扩散采样在测试时进行优化——通过单步去噪估计构造正则化损失 $L_{\mathrm{DPoser}}$，引导优化轨迹趋向合理姿态流形。同时，针对姿态数据“关键信息集中于后期时间步”的特点，设计了**截断时间步调度策略**（从 $t_{\mathrm{max}}$ 线性递减至 $t_{\mathrm{min}}$），在提升优化效率的同时保持姿态合理性。为克服全身数据稀缺，进一步提出**混合训练策略**：冻结分部模型，融合全身模块，利用分部数据集与随机掩码机制联合训练。

实验层面，DPoser-X 在 **8 个基准**上展现出全面领先性能，最高带来 **61%** 的相对提升。在 EHF 人体网格恢复任务中，从零初始化取得 PA-MPJPE **56.05**，优于所有对比方法（包括 NRDF 的 57.38）；在 AMASS 运动去噪上，MPJPE 达 **19.87**，超越专用时序运动先验 HuMoR（22.69）；在 ReInterHand 手部逆运动学任务中，稀疏观测设定下 MPJPE 仅 **3.21**，相比 VPoser（8.25）降低逾 60%。消融实验验证了截断调度与混合训练策略的关键贡献：截断调度使全身网格恢复的 PA-MPVPE_all 从均匀调度的 61.62 降至 **60.98**；混合训练将手部误差 PA-MPVPE_hands 进一步压缩至 **15.83**。

DPoser-X 的局限性同样值得关注：训练数据偏向常见站立动作，对瑜伽等极端姿态泛化不足；变分扩散采样的模式寻求特性导致生成多样性受限（Recall 仅 0.163），难以覆盖真实分布的长尾区域；对低质量二维关键点估计较为敏感。这些开放问题指向未来方向：通过重要性采样或粒子变分推断增强分布覆盖，以及在盲逆问题中联合建模测量算子与数据分布。

三维人体姿态建模是计算机视觉与图形学中的核心问题，其关键在于构建能够刻画真实人体运动分布的先验模型。此类先验不仅需要生成自然、多样化的姿态，还必须能够作为通用正则化组件嵌入各类下游任务，如人体网格恢复、运动去噪和姿态补全。

然而，现有姿态先验在表达能力与泛化性之间长期面临两难困境。早期方法采用高斯混合模型（GMM）作为姿态先验，虽计算高效但表达能力极为有限，难以捕捉人体姿态的高维非线性流形结构。变分自编码器（VAE）类方法如 **VPoser** 通过隐空间建模提升了表达力，但其高斯隐变量假设本质上限制了分布拟合的精度，难以覆盖复杂姿态的长尾分布。基于神经距离场（NDF）的先验如 **Pose-NDF** 和 **NRDF** 虽在单姿态优化任务中表现优异，但训练不稳定且泛化能力不足。

更为关键的是，上述方法均未有效解决**高质量全身姿态数据匮乏**这一根本瓶颈。现有数据集多为局部标注（仅身体、手部或面部），而同时包含身体、手部和面部的全身标注数据稀少且动作多样性有限。这导致现有先验要么仅能建模局部姿态，要么在全身场景下泛化能力急剧下降，无法有效支撑日益增长的全身人体建模需求。

扩散模型在图像、视频等领域的突破性进展，展示了其在高维复杂分布建模上的巨大潜力。直觉上，扩散模型通过逐步去噪的学习范式，天然适合捕捉人体姿态流形中的多模态结构与细粒度约束。然而，如何将扩散模型从生成任务适配为通用的姿态先验，并将其无缝嵌入各类逆问题求解框架，仍是一个开放挑战。

本文提出 **DPoser-X**，旨在以扩散模型为核心构建一种鲁棒、通用且可扩展的三维全身人体姿态先验。核心动机在于：将姿态估计、补全、去噪等异构任务统一建模为逆问题，利用扩散模型的噪声预测过程作为通用的正则化项，通过测试时优化实现任务无关的即插即用。针对全身数据匮乏问题，进一步提出混合训练策略，融合局部数据集与全身数据集，在保持泛化能力的同时显著提升全身姿态建模精度。

## 核心方法与创新机理

DPoser-X 的核心创新在于将**无条件扩散模型**引入三维人体姿态先验领域，并通过一系列针对姿态数据特性的设计，系统性地突破了现有先验方法的表达能力瓶颈。其创新点可归纳为四个关键维度的“changed slots”。

### 1. 先验类型：从 VAE/NDF 到扩散模型

传统姿态先验主要依赖 VAE（如 **VPoser**）或神经距离场（如 **Pose-NDF**、**NRDF**），这些方法受限于隐空间表征能力或对复杂分布建模的不足。DPoser-X 直接采用无条件扩散模型学习姿态分布 $p(\theta)$，利用 sub-VP SDE 参数化（Song et al., ICLR 2021）对高维、多模态的姿态流形进行建模。这一转变的本质在于：扩散模型通过逐步去噪过程捕获了姿态空间的精细几何结构，其噪声预测网络 $\epsilon_\phi(\mathbf{x}_t; t)$ 隐式编码了数据分布的梯度场，从而为下游任务提供了更强的正则化信号。

### 2. 测试时集成：从隐空间优化到变分扩散采样

现有方法通常将先验作为固定的正则化项直接嵌入优化目标。DPoser-X 将各类姿态任务统一建模为逆问题 $\mathbf{y} = \mathcal{A}(\mathbf{x}_0) + \mathbf{n}$，并采用**变分扩散采样**进行求解。其核心在于 DPoser 正则化损失：

$$L_{\mathrm{DPoser}} = w_t \| \mathbf{x}_0 - \mathbf{sg}[\hat{\mathbf{x}}_0(t)] \|_2^2$$

其中 $\hat{\mathbf{x}}_0(t) = \frac{\mathbf{x}_t - \sigma_t \epsilon_\phi(\mathbf{x}_t; t)}{\alpha_t}$ 为单步去噪估计。该设计的关键机制是：优化过程中对当前姿态注入噪声后执行单步去噪，将去噪结果作为“合理姿态”的伪标签，引导优化方向。与传统隐空间优化相比，这种方法无需编码器，直接在原始姿态空间操作，避免了隐空间映射带来的信息损失。

### 3. 扩散时间步调度：从均匀采样到截断线性调度

标准扩散模型在生成时均匀遍历所有时间步。DPoser-X 发现姿态的关键结构信息集中在扩散过程的**后期时间步**（即低噪声阶段），前期高噪声阶段主要影响全局姿态而非局部关节配置。基于此观察，提出了截断线性调度策略：

$$t = t_{\mathrm{max}} - \frac{(t_{\mathrm{max}} - t_{\mathrm{min}}) \times \mathrm{iter}}{N - 1}$$

该调度从 $t_{\mathrm{max}}$ 线性递减至 $t_{\mathrm{min}}$，跳过早期高噪声时间步。消融实验证实，截断调度在全身网格恢复中取得 PA-MPVPE_all 60.98，优于均匀调度的 61.62（Table 9），验证了姿态细化集中在后期时间步的假设。

### 4. 全身训练策略：从分部独立到混合训练

高质量全身姿态数据的匮乏是全身先验建模的主要障碍。DPoser-X 提出**混合训练策略**：冻结预训练的身体、手部、脸部分部模型，仅训练一个融合模块；同时利用分部数据集（仅有部分关节标注）和全身数据集进行训练，对分部数据仅计算可用部分的损失，对全身数据则随机掩码部分关节以防止网络对缺失部分产生任意预测。该策略使 DPoser-X-mixed 的手部误差 PA-MPVPE_hands 降至 15.83，显著优于基础版本（17.54）和仅融合版本（17.79）（Table 11），有效缓解了数据匮乏问题。

DPoser-X 的核心思路是将**无条件扩散模型**作为三维人体姿态的通用先验，通过**变分扩散采样**将其嵌入各类姿态逆问题的测试时优化中。整个框架围绕三个关键设计展开：扩散先验的学习、先验与任务损失的融合机制、以及面向全身姿态的混合训练策略。

### 姿态逆问题建模

各类姿态相关任务被统一建模为逆问题：

$$\mathbf{y} = \mathcal{A}(\mathbf{x}_0) + \mathbf{n}$$

其中 $\mathbf{x}_0$ 为干净姿态参数，$\mathcal{A}(\cdot)$ 为任务特定的退化算子（如相机投影、部分关节观测），$\mathbf{y}$ 为退化后的测量，$\mathbf{n}$ 为噪声。求解该逆问题的核心挑战在于先验 $p(\mathbf{x}_0)$ 的表达能力——这正是 DPoser 所填补的空白。

### 扩散先验学习

DPoser 采用无条件扩散模型学习姿态分布 $p(\theta)$，训练目标为标准噪声预测损失：

$$\mathbb{E}_{\mathbf{x}_0 \sim p_{\mathrm{data}}, \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I}), t \sim \mathcal{U}[0,1]} \left[ w(t) \| \epsilon - \epsilon_\phi(\mathbf{x}_t; t) \|_2^2 \right]$$

扩散过程采用 sub-VP SDE 参数化，前向加噪定义为 $\mathbf{x}_t = \alpha_t \mathbf{x}_0 + \sigma_t \epsilon$。训练完成后，网络 $\epsilon_\phi$ 可在任意时间步 $t$ 预测噪声，进而通过一步去噪估计恢复干净姿态：

$$\hat{\mathbf{x}}_0(t) = \frac{\mathbf{x}_t - \sigma_t \epsilon_\phi(\mathbf{x}_t; t)}{\alpha_t}$$

### DPoser 正则化与变分扩散采样

在测试时优化中，DPoser 作为正则化项嵌入任务损失。核心正则化损失基于一步去噪估计：

$$L_{\mathrm{DPoser}} = w_t \| \mathbf{x}_0 - \mathrm{sg}[\hat{\mathbf{x}}_0(t)] \|_2^2$$

其中 $\mathrm{sg}[\cdot]$ 为停止梯度操作，防止优化目标直接坍缩到去噪估计。该损失鼓励当前姿态 $\mathbf{x}_0$ 趋近于扩散模型认为的“合理姿态”。

以人体网格恢复（HMR）为例，完整优化目标为：

$$L(\theta, \beta) = L_{\mathrm{HMR}} + w_{\beta} L_{\beta} + w_{\theta} L_{\mathrm{DPoser}}$$

其中 $L_{\mathrm{HMR}}$ 为重投影损失，$L_{\beta}$ 为形状先验，$L_{\mathrm{DPoser}}$ 替代了传统 SMPLify 中复杂的穿透惩罚项。优化过程采用变分扩散采样框架，通过最小化后验与先验间的 KL 散度来求解。

### 截断时间步调度

扩散模型的去噪过程存在明显的阶段性特征：姿态的语义结构在早期时间步确定，而细节细化集中在后期（Figure 3 的可视化验证了这一点）。基于此观察，DPoser 采用截断线性调度：

$$t = t_{\mathrm{max}} - \frac{(t_{\mathrm{max}} - t_{\mathrm{min}}) \times \mathrm{iter}}{N - 1}$$

优化从 $t_{\mathrm{max}}$ 开始，逐步递减至 $t_{\mathrm{min}}$，跳过无关的早期时间步。消融实验（Table 9）表明，该调度在全身体网格恢复上取得 PA-MPVPE_all 60.98，优于均匀调度（61.62），验证了“姿态关键信息集中在后期时间步”这一核心洞察。

### 全身混合训练策略

DPoser-X 将全身姿态拆分为身体、手部、面部三个部分，分别由独立的部件扩散模型处理。为融合这些部件模型并利用异构数据集（部分数据集仅含身体或手部标注），提出混合训练策略（Figure 4）：

1. **冻结部件网络**：身体、手部、面部的部件模型在各自数据集上预训练后冻结。
2. **全身融合模块**：在冻结的部件网络之上训练一个融合模块，使用全身数据集。
3. **随机掩码**：对全身数据随机掩码部分肢体，仅对可用部分计算损失，防止模型在缺失部分上产生任意预测。

这一策略使 DPoser-X-mixed 的手部误差 PA-MPVPE_hands 降至 15.83，显著优于仅融合版本（17.79）和基础版本（17.54），证明混合训练有效利用了部分数据集中的高质量标注。

### 整体数据流

1. **输入**：任务测量 $\mathbf{y}$（如 2D 关键点、部分关节位置）和初始姿态估计。
2. **前向扩散**：对当前姿态 $\mathbf{x}_0$ 加噪得到 $\mathbf{x}_t$。
3. **噪声预测**：扩散模型 $\epsilon_\phi(\mathbf{x}_t; t)$ 预测噪声。
4. **一步去噪**：通过 $\hat{\mathbf{x}}_0(t)$ 恢复干净姿态估计。
5. **损失计算**：结合任务测量损失与 DPoser 正则化损失。
6. **梯度更新**：反向传播更新姿态参数 $\mathbf{x}_0$。
7. **时间步递减**：按截断调度降低 $t$，重复步骤 2-6 直至收敛。

该框架的模块化设计使其可无缝适配多种任务：HMR 中 $\mathcal{A}$ 为相机投影，手部逆运动学中 $\mathcal{A}$ 为关节选择掩码，运动去噪中 $\mathcal{A}$ 为恒等映射加噪声。Figure 2 直观展示了这一优化框架的闭环结构。

**证据强度说明**：上述框架描述基于论文 Section 2 的方法论陈述及 Figure 2、Figure 4 的结构可视化，核心公式（Eq. 1-6, 8, 11）均来自原文，置信度较高。截断调度的因果机制（姿态细化集中在后期时间步）有 Figure 3 的定性可视化支撑，但该结论基于 DDIM 有限步采样的观察，其在不同采样器下的普适性需进一步验证。

![[assets/figures/papers/paper_list_l8_DPoser_X_Diffusion_Model_as_Robust_3D_Whole_body_Human_Pose_Prior_motion20v2/figures/001_Figure_1.jpg]]
*Figure 1: An overview of DPoser-X’s versatility and performance across multiple pose-related tasks. Built on diffusion models, DPoser-X serves as a robust and adaptable prior for 3D whole-body human pose modeling. Shown are scenarios in (a) pose generation, (b) human mesh recovery, and (c) pose completion. With up to 61% improvement across 8 benchmarks, DPoser-X consistently outstrips existing priors like VPoser [51] and NRDF [24], proving its superiority in tasks involving the human body, hand, and face*

DPoser-X 的核心是将无条件扩散模型作为三维人体姿态的通用先验，并通过变分扩散采样将其嵌入各类姿态逆问题的测试时优化中。其方法体系由三个关键模块构成：**扩散姿态先验学习**、**DPoser 正则化与逆问题求解**、以及**截断时间步调度**。以下逐一展开其公式推导与设计逻辑。

### 扩散姿态先验学习

DPoser 采用无条件扩散模型学习姿态表示 $\theta$（对于全身模型则为 $\mathbf{x}_0$）的分布 $p(\mathbf{x}_0)$。扩散前向过程遵循 sub-VP SDE 参数化，逐步向干净姿态注入高斯噪声：

$$
\mathbf{x}_t = \alpha_t \mathbf{x}_0 + \sigma_t \epsilon, \quad \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I}) \tag{1}
$$

其中 $\alpha_t$ 为信号保留系数，$\sigma_t$ 为噪声方差系数，二者由方差保持 SDE 的噪声调度函数 $\xi(s)$ 定义：

$$
\alpha_t = \exp\left(-\frac{1}{2}\int_0^t \xi(s)\mathrm{d}s\right), \quad \sigma_t = 1 - \exp\left(-\int_0^t \xi(s)\mathrm{d}s\right)
$$

训练目标为噪声预测网络 $\epsilon_\phi(\mathbf{x}_t; t)$ 的加权 L2 损失：

$$
\mathbb{E}_{\mathbf{x}_0 \sim p_{\mathrm{data}}, \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I}), t \sim \mathcal{U}[0,1]} \left[ w(t) \| \epsilon - \epsilon_\phi(\mathbf{x}_t; t) \|_2^2 \right] \tag{2}
$$

训练完成后，$\epsilon_\phi$ 隐式编码了姿态流形，为下游逆问题提供正则化基础。

### DPoser 正则化与逆问题求解

姿态相关任务被统一建模为逆问题：

$$
\mathbf{y} = \mathcal{A}(\mathbf{x}_0) + \mathbf{n} \tag{3}
$$

其中 $\mathbf{y}$ 为退化观测（如 2D 关键点），$\mathcal{A}(\cdot)$ 为已知的测量算子（如相机投影），$\mathbf{n}$ 为观测噪声。求解该逆问题的核心挑战在于从欠定观测中恢复合理的三维姿态，这正是扩散先验发挥作用的环节。

基于变分扩散采样框架，优化目标为最小化后验与变分近似之间的 KL 散度，其损失函数可分解为测量误差项与扩散正则项：

$$
\mathcal{L} = \| \mathbf{y} - \mathcal{A}(\mathbf{x}_0) \|^2 + w_t (\mathbf{sg}[\epsilon_\phi(\mathbf{x}_t; t) - \epsilon])^\top \mathbf{x}_0 \tag{4}
$$

其中 $\mathbf{sg}[\cdot]$ 表示停止梯度操作。为简化实现，该正则项等价于以下 **DPoser 正则化损失**——鼓励当前姿态 $\mathbf{x}_0$ 趋近于单步去噪估计 $\hat{\mathbf{x}}_0(t)$：

$$
L_{\mathrm{DPoser}} = w_t \| \mathbf{x}_0 - \mathbf{sg}[\hat{\mathbf{x}}_0(t)] \|_2^2 \tag{5}
$$

其中单步去噪估计由噪声预测网络直接给出：

$$
\hat{\mathbf{x}}_0(t) = \frac{\mathbf{x}_t - \sigma_t \epsilon_\phi(\mathbf{x}_t; t)}{\alpha_t} \tag{6}
$$

这一设计的直觉在于：$\hat{\mathbf{x}}_0(t)$ 是扩散模型对“当前含噪姿态 $\mathbf{x}_t$ 对应的干净姿态”的最优估计，因此迫使 $\mathbf{x}_0$ 靠近 $\hat{\mathbf{x}}_0(t)$ 等价于将姿态拉回扩散模型所学习的合理流形。

以人体网格恢复（HMR）为例，完整优化目标融合重投影损失、形状先验与 DPoser 正则化：

$$
L(\theta, \beta) = L_{\mathrm{HMR}} + w_{\beta} L_{\beta} + w_{\theta} L_{\mathrm{DPoser}} \tag{8}
$$

其中 $L_{\mathrm{HMR}}$ 为 2D 关键点重投影误差：

$$
L_{\mathrm{HMR}} = \sum_{i \in \mathrm{Joints}} \lambda_i \rho\left(\Pi_C\left(M_J(\theta, \beta)_i\right) - J_i^{\mathrm{est}}\right)
$$

$\Pi_C$ 为相机投影，$M_J$ 为 SMPL 模型的关节点回归器，$\rho$ 为鲁棒损失函数（如 Geman-McClure）。

### 截断时间步调度

扩散模型的去噪过程存在一个关键特性：**姿态的精细结构主要在后期时间步（较小 $t$）中形成**。这意味着在优化过程中，始终使用高噪声水平（大 $t$）的正则化不仅冗余，还可能引入不必要的模糊性。基于此观察，DPoser 提出截断线性时间步调度：

$$
t = t_{\mathrm{max}} - \frac{(t_{\mathrm{max}} - t_{\mathrm{min}}) \times \mathrm{iter}}{N - 1} \tag{11}
$$

其中 $t_{\mathrm{max}}$ 和 $t_{\mathrm{min}}$ 分别为截断区间的上下界，$\mathrm{iter}$ 为当前迭代轮次，$N$ 为总迭代数。该调度在优化初期使用较大 $t$ 以快速约束姿态的全局结构，随后线性递减至 $t_{\mathrm{min}}$，使正则化聚焦于姿态的局部细节优化。消融实验证实，截断调度在全身体网格恢复中取得 PA-MPVPE_all 60.98，优于均匀调度的 61.62（Table 9），验证了“姿态细化集中在后期时间步”的核心假设。

### 全身混合训练策略

为应对高质量全身姿态数据匮乏的瓶颈，DPoser-X 采用分治与融合策略：首先在分部数据集上训练身体、手部、脸部的独立扩散模型并冻结，随后在全身数据集上训练一个融合模块，将各分部特征整合为统一的全身姿态表示。训练时采用**混合训练策略**——对于仅含部分关节的分部数据，仅对可用部分计算损失；对于全身数据，则随机掩码部分身体区域以模拟分部数据分布，防止模型在缺失区域产生任意预测。这一设计使 DPoser-X-mixed 在全身体网格恢复中将手部误差 PA-MPVPE_hands 降至 15.83，显著优于仅融合版本（17.79）和基础版本（17.54）（Table 11）。

![[assets/figures/papers/paper_list_l8_DPoser_X_Diffusion_Model_as_Robust_3D_Whole_body_Human_Pose_Prior_motion20v2/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the DPoser-regularized optimization framework. Task inputs (e.g., 2D keypoints in human mesh recovery) and current poses are used to compute the measurement loss based on the degradation pattern*

![[assets/figures/papers/paper_list_l8_DPoser_X_Diffusion_Model_as_Robust_3D_Whole_body_Human_Pose_Prior_motion20v2/figures/004_Figure_4.jpg]]
*Figure 4: Overview of the DPoser-X methodology. (a) The whole-body network consists of frozen part-only networks, and a fused module trained on whole-body datasets. (b) The mixed training strategy utilizes part-only datasets by applying loss only to available parts. To prevent arbitrary predictions on unavailable parts, the whole-body data is sometimes randomly masked, and loss is applied to all parts*

## 实验与关键发现

### 姿态生成

DPoser 在无条件身体姿态生成任务中展现出强大的分布拟合能力。如表 1 所示，DPoser 取得 APD 14.28、FID 0.07、Precision 0.72、Recall 0.80、dNN 2.63 的综合指标，在保真度（FID）和覆盖率（Recall）上显著优于 VPoser 和 Pose-NDF 等现有先验。值得注意的是，当使用仅 10 步的 DDIM 采样器（DPoser*）时，Recall 飙升至 0.95，但 Precision 骤降至 0.10，APD 升至 19.03。这一现象揭示了扩散采样步数与生成质量之间的核心权衡：少步采样虽能覆盖更广的分布范围，但牺牲了单样本的真实性。图 5 的定性对比直观印证了这一结论——DPoser 生成的姿态自然且符合人体结构，而 DPoser* 的部分结果虽然 APD 较高，却缺乏自然外观。

### 人体网格恢复

在 EHF 数据集的人体网格恢复任务中，DPoser 从零初始化（from scratch）取得 PA-MPJPE 56.05，优于 NRDF 的 57.38 和 VPoser 的 57.68，验证了扩散先验在缺乏回归初始化时的鲁棒性。当结合 CLIFF 回归初始化后，DPoser 进一步将误差降至 49.05，在所有对比方法中保持最优。图 6 展示了从零初始化条件下的恢复可视化结果，DPoser 的重建网格在肢体姿态和整体形态上均与真值高度吻合。

### 运动去噪

在 AMASS 和 HPS 数据集上的运动去噪实验（表 3）进一步验证了 DPoser 的通用性。在 40mm 噪声强度下，DPoser 取得 MPJPE 19.87（AMASS）和 20.54（HPS），不仅大幅优于静态先验 VPoser（分别为 38.15 和 37.06），甚至超越了专门的时序运动先验 HuMoR（22.69 和 24.02）。这一结果表明，扩散模型学习的姿态分布本身蕴含了足够的运动合理性约束，无需显式建模时序依赖即可实现高质量去噪。

### 手部逆运动学

在 ReInterHand 数据集的手部逆运动学任务中（表 4），DPoser 在稀疏关键点设定下取得 MPJPE 3.21，相比 VPoser 的 8.25 实现超过 60% 的误差降低。这一优势在不同掩码设定下均保持一致，表明扩散先验对手部高自由度关节空间的约束能力显著强于基于 VAE 的潜在空间正则化。

### 全身网格恢复与消融

在 ARCTIC 数据集的全身网格恢复任务中，DPoser-X 取得 PA-MPVPE All 60.98，优于 VPoser-X 的 66.74（表 8）。消融实验揭示了两个关键设计的作用：

**截断时间步调度。** 表 9 的消融表明，截断调度（从 $t_{\text{max}}$ 线性递减至 $t_{\text{min}}$）在全身网格恢复中取得 PA-MPVPE_all 60.98，优于均匀调度的 61.62。这一改进源于姿态细化集中在扩散过程的后期时间步（图 3），截断调度将优化算力聚焦于关键阶段，同时避免早期高噪声时间步引入的无效扰动。

**混合训练策略。** 表 11 的消融显示，DPoser-X-mixed 的手部误差 PA-MPVPE_hands 降至 15.83，显著优于仅融合版本（17.79）和基础版本（17.54）。混合训练通过利用部分数据集（仅含身体或手部标注）并结合随机掩码策略，有效缓解了高质量全身姿态数据匮乏的瓶颈，使模型在保持身体姿态合理性的同时，显著提升了对末端执行器（手部）的建模精度。

### 失败模式与局限性

尽管 DPoser-X 在多个基准上取得显著提升，分析揭示了以下局限性：

1. **极端姿态泛化不足。** 训练数据偏向常见站立动作，对瑜伽等分布外极端姿态的建模能力有限，可能导致正则化项将合理但罕见的姿态拉向常见分布区域。
2. **生成多样性受限。** 变分扩散采样的模式寻求（mode-seeking）特性导致 Recall 仅 0.163，难以覆盖真实姿态分布的长尾区域。这一问题在需要多样化输出的场景（如姿态生成）中尤为突出。
3. **关键点质量敏感性。** 优化过程依赖 2D 关键点估计的准确性，低质量的关键点输入会通过测量损失项误导优化方向，导致重建姿态偏离真实值。

![[assets/figures/papers/paper_list_l8_DPoser_X_Diffusion_Model_as_Robust_3D_Whole_body_Human_Pose_Prior_motion20v2/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison of generated human poses: (e) illustrates naturalistic poses aligned with real-world data, whereas (f) shows poses that, despite superior APD, lack natural appearance. *We use a DDIM sampler [60] with only 10 steps*

![[assets/figures/papers/paper_list_l8_DPoser_X_Diffusion_Model_as_Robust_3D_Whole_body_Human_Pose_Prior_motion20v2/figures/008_Figure_6.jpg]]
*Figure 6: Visualization of human mesh recovery results (body only) on EHF [51] when fitting from scratch*

![[assets/figures/papers/paper_list_l8_DPoser_X_Diffusion_Model_as_Robust_3D_Whole_body_Human_Pose_Prior_motion20v2/figures/018_Table_9.jpg]]
*Table 9: Ablation of timestep scheduling on key pose-related tasks*

## 定位与知识库关联

### 核心设计定位

DPoser-X 的核心贡献在于将**无条件扩散模型**引入三维人体姿态先验的建模，并将姿态逆问题求解统一到**变分扩散采样**框架下。与现有方法相比，其设计在四个关键维度上实现了系统性转变：

| 设计维度 | 现有范式 | DPoser-X 方案 |
|---------|---------|-------------|
| 先验类型 | VAE 高斯潜变量（VPoser）/ 神经距离场（Pose-NDF, NRDF） | 无条件扩散模型，直接建模 $p(\theta)$ |
| 测试时集成 | 潜空间优化或直接正则化 | 变分扩散采样 + 单步去噪正则化 |
| 时间步策略 | 均匀采样 $t$ | 截断线性调度 $t_{\text{max}} \to t_{\text{min}}$ |
| 全身训练 | 分部位独立训练或仅用全身数据 | 混合训练 + 随机掩码，冻结分部模型后融合全身模块 |

### 与现有先验的关系

**GMM**（SMPLify 原始先验）仅能捕捉单峰或有限混合分布，对复杂姿态的表达能力严重不足。**VPoser** 将 VAE 引入姿态先验，通过高斯潜变量实现了连续、可微的正则化，但其高斯先验假设限制了分布建模的灵活性。**Pose-NDF** 和 **NRDF** 采用神经距离场建模姿态流形的隐式表面，虽提升了表达力，但在泛化性和优化稳定性上存在瓶颈。

DPoser-X 通过扩散模型的逐步去噪过程，避免了 VAE 的潜空间瓶颈和 NDF 的隐式表面约束。其噪声预测网络 $\epsilon_\phi(\mathbf{x}_t; t)$ 学习的是姿态分布的全域 score function，理论上能够建模任意复杂的分布形态。实验表明，在 EHF 人体网格恢复任务中，DPoser 从零初始化取得 PA-MPJPE 56.05，优于 NRDF 的 57.38（Table 2）；在 AMASS 运动去噪上，DPoser 的 MPJPE 19.87 甚至超越了专用时序运动先验 **HuMoR** 的 22.69（Table 3）。

### 与扩散模型逆问题求解的关系

DPoser-X 的方法论建立在扩散模型逆问题求解的通用框架之上。其核心公式：

$$\mathcal{L} = \Vert \mathbf{y} - \mathcal{A}(\mathbf{x}_0) \Vert^2 + w_t (\mathbf{sg}[\epsilon_\phi(\mathbf{x}_t; t) - \epsilon])^\top \mathbf{x}_0$$

将测量误差与扩散正则项统一在变分扩散采样目标中。这一设计与 **DPS**（Diffusion Posterior Sampling）等方法共享相同的理论基础，但 DPoser-X 的关键创新在于针对**姿态数据的特性**进行了领域适配：

1. **截断时间步调度**：观察到姿态生成中关键结构信息集中在后期时间步（Figure 3），因此将优化过程的时间步从 $t_{\text{max}}$ 线性递减至 $t_{\text{min}}$，而非均匀采样。消融实验证实，截断调度在全身网格恢复中取得 PA-MPVPE_all 60.98，优于均匀调度的 61.62（Table 9）。

2. **单步去噪正则化**：将 DPoser 损失简化为 $L_{\text{DPoser}} = w_t \Vert \mathbf{x}_0 - \mathbf{sg}[\hat{\mathbf{x}}_0(t)] \Vert_2^2$，其中 $\hat{\mathbf{x}}_0(t)$ 是单步去噪估计。这种设计避免了完整逆向扩散采样的计算开销，使先验能够高效嵌入各类优化循环。

### 全身姿态建模的混合训练策略

DPoser-X 的全身扩展面临一个关键瓶颈：高质量全身姿态数据稀缺，而身体、手部、面部分部位数据相对丰富。其解决方案是**混合训练策略**（Figure 4）：先冻结在分部位数据上预训练的部件模型，然后引入融合模块，在全身数据集上训练，同时利用分部位数据通过仅对有效部位计算损失的方式进行补充。为防止模型在缺失部位上产生任意预测，还对全身数据进行随机掩码。

消融实验证实了这一策略的有效性：DPoser-X-mixed 在全身网格恢复中的手部误差 PA-MPVPE_hands 降至 15.83，显著优于仅融合版本（17.79）和基础版本（17.54）（Table 11）。

### 适用边界与局限

尽管 DPoser-X 在多个基准上取得了显著提升，其适用性仍存在明确边界：

**数据分布局限**：训练数据偏向常见站立和行走动作，对瑜伽、杂技等极端姿态的泛化能力不足。这是扩散模型数据驱动本质的固有限制——模型只能学习训练分布内的模式。

**生成多样性不足**：变分扩散采样的模式寻求（mode-seeking）特性导致生成多样性有限。在姿态生成任务中，DPoser 的 Recall 仅为 0.163（Table 1），表明其难以覆盖真实分布的长尾。这一特性在逆问题求解中是把双刃剑：模式寻求有助于产生合理结果，但可能丢失真实但罕见的姿态解。

**观测质量敏感**：方法对低质量 2D 关键点估计敏感。当输入关键点存在较大误差时，测量损失项会误导优化过程。这是基于优化的方法的共性弱点，与基于回归的 HMR 方法（如 CLIFF）形成互补——后者对观测噪声更鲁棒但缺乏先验约束的灵活性。

**计算效率**：作为测试时优化方法，DPoser-X 的推理速度无法与单步前馈回归方法相比。这限制了其在实时应用场景中的部署。

### 开放问题

1. **分布外泛化**：如何通过重要性采样、数据增强或类别平衡训练，提升扩散先验对训练分布外姿态的鲁棒性？这是将方法扩展到更广泛人体活动场景的关键。

2. **多样性增强**：能否结合粒子变分推断或温度调节技术，在保持结果合理性的前提下增强扩散后验采样的多样性？这对于需要探索多个可能解的任务（如姿态补全）尤为重要。

3. **盲逆问题扩展**：当前方法假设测量算子 $\mathcal{A}$（如相机投影）已知。如何在未知相机参数等盲逆问题场景中联合建模测量算子与数据分布，将 DPoser 扩展至更一般的 HMR 场景？

4. **实时集成**：能否通过知识蒸馏或扩散模型加速技术，将扩散先验的约束能力集成到基于回归的实时 HMR 方法中，兼顾效率与合理性？

## 原文 PDF

![[paperPDFs/arxiv_2025/DPoser_X_Diffusion_Model_as_Robust_3D_Whole_body_Human_Pose_Prior.pdf]]
