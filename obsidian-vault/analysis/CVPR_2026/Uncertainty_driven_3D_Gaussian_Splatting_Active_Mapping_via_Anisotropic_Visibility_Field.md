---
title: Uncertainty-driven 3D Gaussian Splatting Active Mapping via Anisotropic Visibility Field
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Uncertainty_driven_3D_Gaussian_Splatting_Active_Mapping_via_Anisotropic_Visibility_Field.pdf
project_link: null
code_link: null
aliases:
- GGSAVF
- UD3GSAMAVF
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 各向异性可见性场——即每个高斯粒子相对于训练视角的方向依赖性可见性——直接决定预测的可靠性：可见性低的区域必然对应高不确定性。
primary_logic: 利用球谐函数解析地构建3DGS中各向异性可见性场，无需训练即可高效（1秒内构建）准确量化可见性，并将其集成到贝叶斯网络不确定性感知光栅化器中，从而在主动建图中可靠地为未观测区域分配高不确定性。
claims:
- GAVIS通过显式建模各向异性可见性，可靠地为训练视角未覆盖区域分配高不确定性，与真实网格可见性一致。
- GAVIS的可见性场构建无需训练，速度比NVF快约500倍（1秒内完成），不确定性量化帧率达200+ FPS。
- 在主动建图任务中，GAVIS在所有数据集（NeRF Synthetic, Space, Gibson, HM3D）上均显著优于现有方法（FisherRF, VIMC, NVF），同时计算开销更低。
- NeRF Synthetic 上 PSNR (dB) ↑ = 24.26 ±0.25
---

# Uncertainty-driven 3D Gaussian Splatting Active Mapping via Anisotropic Visibility Field

> [!tip] 核心洞察
> 利用球谐函数解析地构建3DGS中各向异性可见性场，无需训练即可高效（1秒内构建）准确量化可见性，并将其集成到贝叶斯网络不确定性感知光栅化器中，从而在主动建图中可靠地为未观测区域分配高不确定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于各向异性可见性场的不确定性驱动3D高斯喷溅主动建图 |
| 英文题名 | Uncertainty-driven 3D Gaussian Splatting Active Mapping via Anisotropic Visibility Field |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xue_Uncertainty-driven_3D_Gaussian_Splatting_Active_Mapping_via_Anisotropic_Visibility_Field_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | GAVIS (Gaussian Splatting Anisotropic Visibility Field) |
| Dataset | NeRF Synthetic, Space |

> [!tip] 效果简介
> - NeRF Synthetic 上，PSNR (dB) ↑ 24.26 ±0.25 vs VIMC 23.14 ±0.25 (最佳基线) (+1.12)；UQ FPS (fps) ↑ 251.5 vs FisherRF 146.3 (+105.2)；T_UP (s) ↓ 0.37 vs NVF 149.13 (-148.76)。
> - Space 上，PSNR (dB) ↑ 26.14 ±0.10 vs VIMC 24.56 ±0.55 (最佳基线) (+1.58)。

## 概要

### 核心问题：3DGS不确定性量化的OOD失效

主动建图（active mapping）要求机器人自主选择观测视角，以最高效地重建未知场景。其关键瓶颈在于**不确定性量化**——系统必须准确判断“哪里还没看清”，才能引导探索。现有基于3D高斯喷溅（3DGS）的不确定性方法，无论是基于费舍尔信息的**FisherRF**、基于变分推断的**VIMC**，还是基于神经网络的可见性场方法**NVF**，都面临一个共同缺陷：它们低估了训练视角未覆盖（out-of-distribution）区域的不确定性。这些方法依赖于训练数据的统计特性，却无法保证为从未被观测过的区域可靠地分配高不确定性，导致主动建图时探索效率低下。

### 核心洞察：可见性即不确定性

GAVIS（Gaussian Splatting Anisotropic Visibility Field）的出发点是一个简洁的因果逻辑：**一个区域的不确定性，本质上取决于它是否被训练视角“看到过”**。如果某个高斯粒子在所有训练视角中都不可见，那么它的颜色、位置等参数就缺乏数据约束，必然对应高不确定性。因此，显式建模每个高斯粒子相对于训练视角的可见性，就能获得可靠的不确定性估计——无需训练，无需猜测。

### 方法定位：解析可见性场 + 贝叶斯不确定性感知光栅化

GAVIS的核心贡献在于两点：

1. **各向异性可见性场的解析构建**：利用球谐函数（spherical harmonics）解析地表示每个高斯粒子在不同方向上的可见性，将方向依赖性（即“从某个角度看是否被遮挡”）显式编码。这一构建过程无需梯度优化，可在**1秒内**完成，比基于神经网络训练的NVF快约500倍。

2. **不确定性感知的3DGS光栅化器**：将可见性场集成到贝叶斯网络中，为每个像素的颜色分布构建高斯混合模型（GMM）。其中，可见性高的粒子用低方差高斯表示（低不确定性），不可见的粒子用高方差先验表示（高不确定性）。候选视角的不确定性图由此合成，下一最佳视角（NBV）选择最大化该GMM熵的位姿。

Figure 2 给出了GAVIS的整体框架：给定已训练的3DGS，首先构建可见性场（VF CONST），然后对候选视角通过查询可见性场的不确定性感知光栅化器（UA 3DGS Rasterizer）合成不确定性图，最终选择最大不确定性视角。

### 主要结果概览

在NeRF Synthetic、Space、Gibson和HM3D四个数据集上的主动建图任务中，GAVIS在所有指标上均显著优于现有方法（见表1）：

- **重建质量**：在NeRF Synthetic上，GAVIS达到24.26 dB PSNR，比最佳基线VIMC（23.14 dB）提升**+1.12 dB**；在Space数据集上达到26.14 dB，比VIMC（24.56 dB）提升**+1.58 dB**。
- **计算效率**：不确定性准备时间（T_UP）仅需**0.37秒**，而NVF需要149.13秒；不确定性量化帧率达**251.5 FPS**，远超FisherRF的146.3 FPS。

定性结果（Figure 6）进一步验证了方法的可靠性：GAVIS准确地将高不确定性分配给训练视角未覆盖的区域，与真实网格可见性（GT Vis.）高度一致，而基线方法在不可见区域的不确定性估计明显偏低。

### 方法谱系与知识库定位

GAVIS处于**3DGS不确定性量化**与**主动视角规划**的交叉点。与基于学习的参数不确定性方法（FisherRF、VIMC）不同，GAVIS通过显式几何建模（可见性场）来驱动不确定性估计，避免了OOD泛化问题。与基于NeRF的可见性场方法（NVF）相比，GAVIS将各向同性可见性推广到各向异性，并利用球谐解析计算替代神经网络训练，实现了数量级的加速。此外，GAVIS可作为**后验增强模块**（post-hoc module）无缝集成到现有3DGS不确定性框架中，提升其性能（见表3）。

### 主动建图与3D高斯喷溅

主动建图（active mapping）要求自主智能体在未知环境中迭代地选择最优观测视角，以在有限步数内最大化场景重建质量。近年来，3D高斯喷溅（3D Gaussian Splatting, 3DGS）因其高质量实时渲染能力成为场景重建的主流表示。然而，将3DGS应用于主动建图面临一个核心挑战：如何可靠地量化3DGS表示中的不确定性，以指导下一最佳视角（next-best-view）的选择。

### 现有不确定性量化方法的瓶颈

当前基于3DGS的不确定性量化方法大致分为两类：基于参数不确定性的方法和基于学习的方法。**FisherRF** 利用费舍尔信息矩阵估计3DGS参数的不确定性，**VIMC** 则通过变分推断对粒子分布进行概率建模。这些方法虽然能在训练视角覆盖充分的区域提供合理的不确定性估计，但存在一个共同的致命缺陷：**它们系统性低估了训练视角未覆盖（out-of-distribution）区域的不确定性**。

这一缺陷的根源在于，基于学习的不确定性估计本质上依赖于训练数据的分布——模型在训练数据稀疏或缺失的区域倾向于“自信地犯错”，而非可靠地分配高不确定性。对于主动建图而言，这意味着探索策略会被误导，智能体无法有效识别并优先观测场景中真正未探索的区域，从而陷入低效的局部探索循环。

### 可见性：不确定性的直接决定因素

一个关键洞察是：**一个区域是否被训练视角观测到（即可见性），直接决定了该区域预测的可靠性**。如果某个3DGS粒子所在区域在所有训练视角中均不可见（例如被遮挡或处于相机视场之外），那么该粒子的颜色和几何属性必然是不可靠的，对应区域应当被赋予高不确定性。反之，被充分观测的区域自然具有低不确定性。

基于这一洞察，**NVF** 尝试为NeRF构建可见性场，但其存在两个根本局限：（1）采用各向同性（仅位置相关）的神经网络表示，无法捕捉可见性随视角变化的各向异性特性；（2）需要神经网络训练，每次规划耗时数分钟，无法满足主动建图的实时性需求。

### 本文动机

本文的核心动机是回答一个根本性问题：**能否在不依赖额外训练的前提下，高效且准确地量化3DGS中每个粒子相对于训练视角的可见性，并以此驱动可靠的不确定性感知主动建图？**

这一动机引出了三个关键技术目标：

1. **各向异性可见性建模**：显式建模每个高斯粒子相对于训练视角方向的方向依赖性可见性——粒子在正对相机的方向上可见性高，而在偏离视角的方向上可见性衰减。
2. **无训练高效构建**：利用球谐函数的解析性质，在1秒内完成可见性场构建，避免神经网络训练的时间开销。
3. **不确定性感知光栅化**：将可见性场集成到贝叶斯网络框架下的3DGS光栅化器中，使未观测区域可靠地获得高不确定性，从而引导主动建图策略高效探索。

## 核心方法与创新机理

GAVIS 的核心创新在于**将“可见性”显式建模为 3DGS 不确定性的主控旋钮**，并以解析方式构建各向异性可见性场，从而从根本上解决了现有方法对训练视角未覆盖区域不确定性估计不足的瓶颈。

### 从各向同性到各向异性：可见性场的表示变革

现有基于学习的不确定性量化方法（如 **FisherRF**、**VIMC**）隐式地从参数或预测分布中推断不确定性，缺乏对“该区域是否被训练视角观测过”这一先验的结构化建模。唯一显式建模可见性的工作 **NVF** 采用神经网络学习各向同性可见性场（仅与空间位置相关），但其训练耗时且无法捕捉可见性的方向依赖性。

GAVIS 的**关键设计转变**在于：

| 设计维度 | 基线方法 | GAVIS 创新 |
|---------|---------|-----------|
| **可见性场表示** | 各向同性神经网络 (NVF) | 各向异性球谐函数解析表示 |
| **构建方式** | 神经网络训练（每次规划耗时数分钟） | 无梯度解析计算（1 秒内完成） |
| **不确定性量化器** | 标准光栅化器或基于学习的不确定性估计 | 集成可见性校正贝叶斯网络的 UA 3DGS 光栅化器 |
| **未探索区域处理** | 无（粒子中心不确定性忽略空区域） | 基于可见性的虚拟粒子密度控制 |

### 核心机制：方向依赖性可见性

GAVIS 观察到：**一个高斯粒子是否被可靠重建，取决于它在训练视角下是否“可见”——而这不仅是位置函数，更是方向函数**。例如，墙壁背面虽然与训练相机位置接近，但因朝向背离而不可见，其重建必然不可靠。

为此，GAVIS 为每个高斯粒子定义了**单视角各向异性可见性**：

$$V_{\mathbf{p}}^{(i)}(\mathbf{d}) = \Phi_{i,\mathbf{p}} T_p(t_i^p) \nu(\mathbf{d}; \mathbf{d}_p)$$

其中 $\Phi_{i,\mathbf{p}}$ 表示粒子是否在相机视锥内，$T_p(t_i^p)$ 为沿射线的透射率（处理遮挡），$\nu(\mathbf{d}; \mathbf{d}_p) = \exp(\kappa \mathbf{d} \cdot \mathbf{d}_p) \cdot \exp(-\kappa)$ 是基于 von Mises-Fisher 分布的**方向可见性函数**——当查询方向 $\mathbf{d}$ 偏离训练视角 $\mathbf{d}_p$ 时，可见性呈指数衰减（见 Figure 3）。

多视角可见性则通过概率合并得到：粒子 $i$ 至少在一个训练视角中可见的概率为

$$V^{(i)}(d) = 1 - \prod_{p\in\mathcal{P}} (1 - V_{\mathbf{p}}^{(i)}(d))$$

### 解析效率：球谐展开与 AM-GM 下界

直接计算上述乘积对每个候选视角的每条射线都不可行。GAVIS 的第二个关键创新是将可见性场展开到**球谐函数（Spherical Harmonics）基**上：

$$\tilde{V}^{(i)}(\mathbf{d}) = \sum_{\ell=0}^{L} \sum_{m=-\ell}^{\ell} \gamma_{\ell m}^{\mathcal{P}} Y_{\ell}^{m}(\mathbf{d})$$

并通过**算术-几何平均（AM-GM）不等式**推导出可见性的高效下界估计：

$$V^{(i)}(d) \geq 1 - \left(1 - \frac{\tilde{V}^{(i)}(d)}{|\mathcal{P}|}\right)^{|\mathcal{P}|}$$

这一技巧避免了昂贵的球谐系数乘积运算，使得可见性场查询达到常数时间复杂度。最终，整个可见性场构建无需任何训练或梯度计算，**耗时不到 1 秒，比 NVF 快约 500 倍**，不确定性量化帧率达 200+ FPS。

### 不确定性感知光栅化器：可见性校正贝叶斯网络

GAVIS 将 3DGS 光栅化建模为贝叶斯网络，像素颜色的高斯混合模型（GMM）直接集成可见性校正项 $v_i$：

$$p(z_0) = \sum_i w_i^* v_i \mathcal{N}(\mu_{c_i}, Q_{c_i}) + \mathcal{N}(\mu_0, Q_0) \sum_i w_i^* (1-v_i)$$

其核心设计在于：**可见性低的粒子贡献被抑制，其概率质量流向高方差先验 $\mathcal{N}(\mu_0, Q_0)$**，从而自然地使未观测区域呈现高熵（高不确定性）。这一机制确保了 GAVIS 在主动建图中能可靠地为训练视角未覆盖区域分配高不确定性，与真实网格可见性（GT Vis.）高度一致（见 Figure 6）。

### 虚拟粒子密度控制：区分自由空间与未探索区域

传统 3DGS 不确定性方法仅评估已有粒子中心的不确定性，无法区分“已被观测确认为空”的自由空间与“尚未探索”的未知区域。GAVIS 引入**虚拟粒子（virtual particles）**，在 3D 空间中采样候选位置，计算其对各训练视角的可见性 $1 - \prod_{p\in\mathcal{P}} (1 - \Phi_{i,p} T_p(t_i^p))$。若虚拟粒子对所有视角均不可见，则该区域被标记为未探索并赋予高不确定性；反之则为自由空间。消融实验证实，移除此模块导致 PSNR 从 24.70 降至 24.18（Table 2），验证了其对主动建图探索效率的关键作用。

GAVIS 的整体管线围绕“可见性场构建—不确定性感知光栅化—下一最佳视角选择”三个核心阶段展开，如 Figure 2 所示。给定一组已观测图像及其相机位姿，首先训练一个标准 3DGS 场景表示。在此基础上，**可见性场构建模块 (VF CONST)** 解析地计算每个高斯粒子相对于全部训练视角的各向异性可见性，并将其压缩为球谐系数，同时插入虚拟粒子以区分自由空间与未探索区域。随后，对于采样得到的候选视角集合，**不确定性感知光栅化器 (UA 3DGS Rasterizer)** 沿每条射线查询可见性场，将可见性校正项融入贝叶斯网络形式的像素颜色高斯混合模型，合成每个候选视角的不确定性图。最后，**下一最佳视角选择模块**以最大化合成视角 GMM 熵为目标，从候选集中选出下一观测位姿。该闭环在主动建图过程中迭代执行，每轮仅需约 1 秒完成可见性场构建，不确定性量化帧率达 200+ FPS，显著快于基于神经网络训练的 NVF（约 500 倍加速）。

![[assets/figures/papers/paper_list_l2281_https_openaccess_thecvf_com_content_CVPR2026_html_Xue_Uncertainty_driven/figures/002_Figure_2.jpg]]
*Figure 2: GAVIS framework. (Left) Given a trained 3DGS, GAVIS constructs a visibility field (VF CONST) to represent regions invisible to the training views. It then quantifies uncertainty over sampled candidate views using an uncertainty-aware 3DGS rasterizer (UA 3DGS Rasterizer) that queries the visibility field (VF QUERY). Finally, the maximum-uncertainty view is selected as the next observation. (Right) GAVIS achieves top performance across all evaluation metrics (see Sec. 5 for details)*

### 输入输出流

- **输入**：已观测图像集合与对应相机位姿。
- **阶段一**：训练 3DGS 重建，输出高斯粒子参数（位置、协方差、颜色、不透明度）。
- **阶段二 (VF CONST)**：基于训练视角，利用改进的 3DGS 光栅化器计算单视角粒子可见性 $\Phi_{i,\mathbf{p}} T_p(t_i^p)$，通过球谐展开构建各向异性可见性场 $V^{(i)}(\mathbf{d})$，并插入虚拟粒子。输出为可见性场参数（球谐系数 $\gamma_{\ell m}^{\mathcal{P}}$）及虚拟粒子集合。
- **阶段三 (UA 3DGS Rasterizer)**：对每个候选视角，沿射线方向 $\mathbf{d}$ 查询 $V^{(i)}(\mathbf{d})$ 获得可见性 $v_i$，代入像素颜色 GMM：
  
$$
p(z_0) = \sum_i w_i^* v_i \mathcal{N}(\mu_{c_i}, Q_{c_i}) + \mathcal{N}(\mu_0, Q_0) \sum_i w_i^* (1-v_i)
$$

  其中不可见区域由高方差先验 $\mathcal{N}(\mu_0, Q_0)$ 表征。输出为每像素的 GMM 熵，即不确定性图。
- **阶段四**：以最大化视角级熵为目标，选择下一最佳视角，将该视角图像加入训练集，进入下一轮迭代。

### 关键设计决策

1. **各向异性可见性的解析构建**：与依赖神经网络训练的 NVF 不同，GAVIS 利用 von Mises-Fisher 分布建模方向可见性函数 $\nu(\mathbf{d}; \mathbf{d}_p) = \zeta \exp(\kappa \mathbf{d} \cdot \mathbf{d}_p)$，并通过球谐展开实现常数时间查询，无需梯度计算。
2. **可见性校正的贝叶斯光栅化**：标准 3DGS 光栅化器仅输出颜色均值，GAVIS 将其扩展为贝叶斯网络，显式建模每个高斯粒子的颜色不确定性，并用可见性 $v_i$ 加权——可见粒子贡献低不确定性，不可见粒子贡献高不确定性先验。
3. **虚拟粒子密度控制**：由于 3DGS 粒子仅存在于场景表面附近，未探索的空旷区域缺乏粒子，导致不确定性估计出现盲区。GAVIS 在可见性场构建时插入虚拟粒子，其可见性按多视角联合概率计算，从而可靠地区分自由空间与未探索区域。消融实验表明，移除该模块会使 PSNR 从 24.70 降至 24.18（Table 2）。

### 整体框架

GAVIS 的核心思想是：**可见性决定不确定性**——一个高斯粒子若在训练视角中不可见，其预测必然不可靠。基于这一洞察，GAVIS 将不确定性量化分解为三个关键模块：

1. **各向异性可见性场构建 (VF CONST)**：解析计算每个高斯粒子相对于所有训练视角的方向依赖性可见性，无需训练。
2. **不确定性感知光栅化器 (UA 3DGS Rasterizer)**：将可见性校正项集成到贝叶斯网络中，为候选视角合成不确定性图。
3. **下一最佳视角选择**：以最大化合成视角的 GMM 熵为目标，选取下一观测位姿。

整体流程如 Figure 2 所示。

### 各向异性可见性场 (Anisotropic Visibility Field)

#### 单视角可见性

对于高斯粒子 $i$ 和训练相机位姿 $\mathbf{p}$，沿方向 $\mathbf{d}$ 的单视角可见性定义为：

$$V_{\mathbf{p}}^{(i)}(\mathbf{d}) = \Phi_{i,\mathbf{p}} \, T_p(t_i^p) \, \nu(\mathbf{d}; \mathbf{d}_p)$$

其中：
- $\Phi_{i,\mathbf{p}}$：粒子 $i$ 是否在相机 $\mathbf{p}$ 的视锥体内（FOV 指示函数）；
- $T_p(t_i^p)$：沿射线到粒子中心 $t_i^p$ 的累积透射率，编码遮挡关系；
- $\nu(\mathbf{d}; \mathbf{d}_p)$：**方向可见性函数**，刻画可见性随视角偏差的衰减。

方向可见性函数基于 von Mises-Fisher 分布构建：

$$\nu(\mathbf{d}; \mathbf{d}_p) := \zeta \exp(\kappa \, \mathbf{d} \cdot \mathbf{d}_p), \quad \zeta = \exp(-\kappa)$$

其中 $\kappa$ 控制方向敏感度，$\mathbf{d}_p$ 为训练视角的主轴方向。当查询方向与训练方向一致时，$\nu$ 取最大值；偏差增大时，$\nu$ 指数衰减。Figure 3 展示了单视角、带遮挡单视角和多视角下的各向异性可见性极坐标图。

#### 多视角可见性

粒子 $i$ 在方向 $\mathbf{d}$ 上至少被一个训练视角观测到的概率为：

$$V^{(i)}(\mathbf{d}) = 1 - \prod_{p \in \mathcal{P}} \left(1 - V_{\mathbf{p}}^{(i)}(\mathbf{d})\right)$$

该式假设各视角观测独立，乘积项表示所有视角均未观测到该粒子的概率。

#### 球谐展开与高效计算

直接计算多视角可见性需对每个查询方向遍历所有训练视角，开销过大。GAVIS 引入辅助可见性场 $\tilde{V}^{(i)}(\mathbf{d})$ 并利用球谐函数 (Spherical Harmonics, SH) 展开：

$$\tilde{V}^{(i)}(\mathbf{d}) = \sum_{\ell=0}^{L} \sum_{m=-\ell}^{\ell} \gamma_{\ell m}^{\mathcal{P}} \, Y_{\ell}^{m}(\mathbf{d})$$

其中 $Y_{\ell}^{m}(\mathbf{d})$ 为标准正交球谐基函数，系数 $\gamma_{\ell m}^{\mathcal{P}}$ 由训练视角集合 $\mathcal{P}$ 解析确定（通过公式 (11) 计算，见原文）。球谐展开实现了常数时间的方向查询。

为避免昂贵的球谐乘法运算，GAVIS 进一步利用算术-几何平均 (AM-GM) 不等式推导可见性下界：

$$V^{(i)}(\mathbf{d}) \geq 1 - \left(1 - \frac{\tilde{V}^{(i)}(\mathbf{d})}{|\mathcal{P}|}\right)^{|\mathcal{P}|}$$

该下界仅需查询辅助场 $\tilde{V}^{(i)}(\mathbf{d})$ 即可高效计算，是实际实现中的核心查询公式 (Eq. 9)。

**效率关键**：单视角粒子可见性 $\Phi_{i,\mathbf{p}} T_p(t_i^p)$ 通过修改后的 3DGS 光栅化器高效计算（详见原文附录 Alg. 2），整个可见性场构建在 1 秒内完成，比基于神经网络训练的 **NVF** 快约 500 倍。

### 不确定性感知光栅化器

GAVIS 将 3DGS 光栅化建模为贝叶斯网络，像素颜色的后验分布为高斯混合模型 (GMM)，并引入可见性校正项：

$$p(z_0) = \sum_i w_i^* v_i \, \mathcal{N}(\boldsymbol{\mu}_{c_i}, \boldsymbol{Q}_{c_i}) + \mathcal{N}(\boldsymbol{\mu}_0, \boldsymbol{Q}_0) \sum_i w_i^* (1 - v_i)$$

其中：
- $w_i^*$：粒子 $i$ 的混合权重（经 alpha 混合后的有效权重）；
- $v_i$：粒子 $i$ 在查询方向上的可见性，由可见性场 $V^{(i)}(\mathbf{d})$ 沿射线方向 $\mathbf{d}$ 查询得到（使用 Eq. 9）；
- $\mathcal{N}(\boldsymbol{\mu}_{c_i}, \boldsymbol{Q}_{c_i})$：可见粒子贡献的颜色高斯分量；
- $\mathcal{N}(\boldsymbol{\mu}_0, \boldsymbol{Q}_0)$：不可见区域的高方差先验分布，$\boldsymbol{Q}_0$ 预设为较大值以编码高不确定性。

该 GMM 的熵直接作为不确定性的客观度量：可见性高的区域由低方差分量主导（低熵），不可见区域由高方差先验主导（高熵），从而可靠地为未观测区域分配高不确定性。

### 虚拟粒子密度控制

粒子中心的不确定性无法反映粒子间空白区域的状态。GAVIS 提出虚拟粒子策略：在场景中采样虚拟粒子，若其在所有训练视角下的可见性（按 $1 - \prod_{p \in \mathcal{P}} (1 - \Phi_{i,p} T_p(t_i^p))$ 计算）低于阈值，则判定该区域为未探索区域并赋予高不确定性；否则视为自由空间。消融实验 (Table 2) 表明，移除该模块后 PSNR 从 24.70 降至 24.18，验证了其对区分未探索区域与自由空间的关键作用。

![[assets/figures/papers/paper_list_l2281_https_openaccess_thecvf_com_content_CVPR2026_html_Xue_Uncertainty_driven/figures/001_Figure_1.jpg]]
*Figure 1: GAVIS overview. Gaussian Splatting Anisotropic Visibility Field (GAVIS) quantifies uncertainty in 3DGS by modeling visibility, i.e., whether a region is observed by the training views. Observed regions have low uncertainty (left room), whereas unobserved regions have high uncertainty (right room)*

## 实验与关键发现

### 主结果：主动建图性能

GAVIS在四个数据集（NeRF Synthetic、Space、Gibson、HM3D）上对所有基线方法实现了全面且显著的领先。Table 1汇总了定量对比结果。

在重建质量上，GAVIS在NeRF Synthetic上达到**24.26 dB PSNR**，较最佳基线VIMC（23.14 dB）提升**+1.12 dB**；在Space数据集上达到**26.14 dB PSNR**，较VIMC（24.56 dB）提升**+1.58 dB**。这一优势源于各向异性可见性场对未观测区域的精确高不确定性分配，使主动建图策略能高效探索被遗漏的场景结构。

在计算效率上，GAVIS的不确定性准备时间（T_UP）仅为**0.37秒**，而基于神经网络训练的NVF需要**149.13秒**，加速约**400倍**。不确定性量化帧率（UQ FPS）达到**251.5 fps**，较FisherRF（146.3 fps）提升**+105.2 fps**。这一效率优势来源于可见性场的无梯度解析构建——球谐系数通过一次前向计算即可获得，无需任何训练迭代。

Figure 4和Figure 5展示了Gibson、HM3D、HST和Lego场景的定性重建结果与相机视角分布。GAVIS的探索轨迹（绿色视锥）更均匀地覆盖了场景的未观测区域，重建结果在边缘和细节区域明显更完整。相比之下，FisherRF和VIMC倾向于在已观测区域重复采样，导致未探索区域长期被忽略。

### 不确定性估计的定性验证

Figure 6提供了不确定性估计的核心定性证据。所有方法在仅部分覆盖场景的相同训练视角集上训练后，GAVIS准确地将高不确定性分配给训练视角未覆盖的不可见区域（GT Vis.中亮色区域），与真实网格可见性高度一致。而FisherRF和VIMC的不确定性图在不可见区域表现出明显的低估——它们倾向于将低不确定性扩散到未观测区域，这正是现有基于学习的3DGS不确定性量化方法的根本瓶颈。

### 消融实验

Table 2报告了消融实验结果，验证了两个关键设计选择的必要性。

**各向异性可见性（Anisotropic Visibility）**：将方向可见性函数ν(d; d_p)设为常数1（即退化为各向同性可见性），PSNR从**24.70 dB降至23.97 dB**（-0.73 dB）。这表明仅依赖粒子位置而忽略视角方向的可见性建模无法捕捉3DGS的视角依赖特性——同一空间位置在不同视角下的可见性可能截然不同（例如，从背面观察一个面向正面的高斯粒子时，其对颜色的贡献几乎为零）。

**虚拟粒子密度控制（Visibility-Field Density Control）**：移除该模块后，PSNR降至**24.18 dB**（-0.52 dB）。虚拟粒子被插入到可见性场中可见性极低的区域，用于区分“自由空间”（已被观测确认为空）与“未探索区域”（尚未被任何训练视角覆盖）。缺少这一机制时，不确定性感知光栅化器无法在空区域与未探索区域之间做出区分，导致主动建图策略将宝贵的观测预算浪费在已知为空的空间上。

### GAVIS作为后验增强模块的通用性

Table 3验证了GAVIS作为即插即用的后验增强模块的通用性。将GAVIS应用于基线3DGS不确定性量化方法（FisherRF、VIMC）后，这些方法的主动建图性能均获得提升。这证明各向异性可见性场捕捉的是一种与具体不确定性估计器正交的互补信号——可见性低必然意味着预测不可靠，这一因果机制独立于参数不确定性或贝叶斯推断的具体实现方式。

### 公平性说明

所有方法使用相同的主动建图管线与无启发式采样的候选视角采样器，确保性能差异仅来源于不确定性量化方法本身的质量，而非管线设计或采样策略的差异。

![[assets/figures/papers/paper_list_l2281_https_openaccess_thecvf_com_content_CVPR2026_html_Xue_Uncertainty_driven/figures/004_Table_1.jpg]]
*Table 1: Quantitative results. Active mapping performance on all datasets across all baselines and our method. Best results are in bold; second-best are underlined. Here*

![[assets/figures/papers/paper_list_l2281_https_openaccess_thecvf_com_content_CVPR2026_html_Xue_Uncertainty_driven/figures/005_Table_2.jpg]]
*Table 2: Ablation study. We evaluate GAVIS for active mapping by isolating the effects of (i) anisotropic visibility*

![[assets/figures/papers/paper_list_l2281_https_openaccess_thecvf_com_content_CVPR2026_html_Xue_Uncertainty_driven/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative uncertainty estimation. All methods are trained on the same set of views that only partially cover the scene, leaving some regions underexplored. GT Vis. indicates rasterized ground-truth mesh visibility (binary face labels), where brighter denotes higher uncertainty (invisible faces) and darker denotes lower uncertainty (visible faces). Our method accurately assigns high uncertainty to invisible regions, aligning with GT Vis*

![[assets/figures/papers/paper_list_l2281_https_openaccess_thecvf_com_content_CVPR2026_html_Xue_Uncertainty_driven/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative active mapping. Reconstruction results and camera-view distributions (green frustums) from different methods’ active-mapping trajectories on Gibson scene (top) and HM3D scene (bottom). Full results are provided in Sec. 12*

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

现有基于3D高斯喷溅（3DGS）的主动建图方法在不确定性量化上存在根本性缺陷：**基于学习的不确定性估计方法（如FisherRF、VIMC）系统性低估了训练视角未覆盖（out-of-distribution）区域的不确定性**。这些方法依赖参数梯度或变分推断来估计不确定性，但无法保证为未观测区域可靠分配高不确定性——而这恰恰是主动建图探索效率的关键。其深层原因在于，3DGS粒子仅存在于已重建的表面区域，粒子中心的不确定性天然会忽略空旷区域与未探索区域，导致下一最佳视角选择策略缺乏有效的探索信号。

另一条技术路线——基于神经辐射场（NeRF）的可见性场方法（如**NVF**）——虽然通过显式建模可见性来量化不确定性，但存在两个关键瓶颈：（1）可见性场建模为各向同性（仅与位置相关），忽略了3DGS中粒子可见性对视角方向的强依赖性；（2）依赖神经网络训练来构建可见性场，每次规划耗时数分钟，无法满足实时主动建图需求。

### 2. 核心洞察与因果调控

GAVIS的核心洞察在于识别出**各向异性可见性场**是连接3DGS表示与不确定性量化的因果调控变量：每个高斯粒子相对于训练视角的方向依赖性可见性直接决定预测的可靠性——可见性低的区域必然对应高不确定性。这一因果链条可形式化为：

- **因果调控变量**：粒子 $i$ 在方向 $\mathbf{d}$ 上的多视角可见性 $V^{(i)}(\mathbf{d})$，定义为粒子至少在一个训练视角中可见的概率（Eq. 5）；
- **调控机制**：通过显式建模方向依赖性可见性函数 $\nu(\mathbf{d}; \mathbf{d}_p)$（基于von Mises-Fisher分布的球面函数，捕捉可见性随视角偏差的指数衰减），将3DGS的视角依赖性从颜色域迁移至可见性域；
- **下游效应**：将可见性校正项 $v_i$ 集成到贝叶斯网络不确定性感知光栅化器的像素颜色高斯混合模型中（Eq. 3），使未可见区域自动获得高方差先验，从而在主动建图中可靠地为未观测区域分配高不确定性。

### 3. 方法谱系中的位置

GAVIS在3DGS不确定性量化方法谱系中占据**显式可见性建模**与**解析高效计算**的交汇点，与现有方法形成清晰对比：

| 维度 | FisherRF | VIMC | NVF | **GAVIS** |
|------|----------|------|-----|-----------|
| **不确定性来源** | 费舍尔信息（参数梯度） | 变分推断（后验方差） | 各向同性可见性（神经网络） | **各向异性可见性（球谐解析）** |
| **可见性建模** | 无显式建模 | 无显式建模 | 各向同性，仅位置相关 | **各向异性，方向相关** |
| **构建方式** | 需梯度计算 | 需变分训练 | 神经网络训练（数分钟） | **无梯度解析计算（<1秒）** |
| **对未探索区域处理** | 弱（粒子中心不确定性忽略空区域） | 弱（同上） | 中等（各向同性限制） | **强（虚拟粒子密度控制+方向感知）** |
| **速度** | 中等（~146 FPS） | 慢 | 极慢（T_UP ~149s） | **快（~251 FPS, T_UP ~0.37s）** |

**关键差异化优势**：

1. **解析可见性场构建**：利用球谐函数（SH）的正交基展开辅助可见性场 $\tilde{V}^{(i)}(\mathbf{d}) = \sum_{\ell=0}^{L} \sum_{m=-\ell}^{\ell} \gamma_{\ell m}^{\mathcal{P}} Y_{\ell}^{m}(\mathbf{d})$（Eq. 6），并通过算术-几何平均不等式得到可见性下界估计（Eq. 9），避免昂贵的球谐乘法，实现常数时间查询。整个构建过程无需训练，速度比NVF快约500倍（1秒内完成）。

2. **方向感知的不确定性量化**：通过显式建模 $\nu(\mathbf{d}; \mathbf{d}_p) = \zeta \exp(\kappa \mathbf{d} \cdot \mathbf{d}_p)$（其中 $\zeta = \exp(-\kappa)$），捕捉可见性随视角偏差的指数衰减，使不确定性估计对不同观测方向具有区分力。

3. **后验增强能力**：GAVIS可作为即插即用的后验模块，无缝集成到现有3DGS不确定性量化框架中。消融实验（Table 3）表明，将GAVIS应用于FisherRF和VIMC后，两者在主动建图任务上的PSNR均获得显著提升，验证了可见性场作为通用不确定性增强模块的有效性。

### 4. 适用边界与局限

**适用场景**：
- 需要高效探索的主动建图/主动视觉任务，特别是对实时性要求较高的场景（UQ FPS > 200）；
- 训练视角部分覆盖场景的稀疏观测条件，GAVIS在此类场景下优势最为显著；
- 可作为现有3DGS不确定性量化方法的通用增强模块。

**已知局限**（需人工验证）：
- 论文未明确讨论方法在动态场景或非刚性形变下的适用性；
- 球谐展开的阶数 $L$ 对可见性场精度的敏感性未在消融实验中量化；
- 虚拟粒子密度控制策略的插入密度与位置选择对最终性能的影响机制未深入分析；
- 方法在极端稀疏观测（如仅2-3个训练视角）下的退化行为未报告。

### 5. 开放问题

1. **可见性场与几何重建的联合优化**：当前GAVIS将可见性场构建与3DGS训练解耦，能否将可见性场作为3DGS训练的正则化项，实现端到端的联合优化？

2. **多智能体协同探索**：各向异性可见性场天然编码了视角覆盖信息，能否将其扩展到多智能体协同主动建图场景，用于视角覆盖的分布式推理？

3. **不确定性校准**：GAVIS的不确定性估计是否经过良好校准（calibrated）？即高不确定性区域是否确实对应高重建误差？论文未提供不确定性校准曲线（如reliability diagram）。

4. **与神经隐式表示的融合**：可见性场的球谐表示能否反向指导3DGS粒子的增删策略，实现更高效的场景覆盖？

## 原文 PDF

![[paperPDFs/CVPR_2026/Uncertainty_driven_3D_Gaussian_Splatting_Active_Mapping_via_Anisotropic_Visibility_Field.pdf]]
