---
title: "FaithFusion: Harmonizing Reconstruction and Generation via Pixel-wise Information Gain"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FaithFusion_Harmonizing_Reconstruction_and_Generation_via_Pixel_wise_Information_Gain.pdf
project_link: "https://shalfun.github.io/faithfusion"
code_link: "https://github.com/wangyuanbiubiubiu/FaithFusion"
aliases:
- FaithFusion
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 像素级期望信息增益（Expected Information Gain, EIG）作为统一的编辑策略，用于指导扩散生成和 3DGS 微调。
primary_logic: 将“是否编辑及编辑到何种程度”的决策重新表述为信息论指标——编辑减少后验不确定性的程度，从而为重构-生成融合提供可解释、可泛化的像素级指导。
claims:
- EIG 作为空间加权函数在生成分支中引导扩散，仅在低置信区域生成内容，从而抑制过度恢复和几何漂移。
- 在 Waymo 数据集上，FaithFusion 在 6 米车道偏移时实现了 FID 107.47，优于其他融合方法。
- 消融实验表明，逐步加入 EIG 指导、EIGent 和渐进式集成，最终 FID 较基线 DIFIX3D+ 降低了 12.77。
- 像素级 EIG 与新视角合成质量呈强相关，通过掩码高 EIG 区域可以验证。
---

# FaithFusion: Harmonizing Reconstruction and Generation via Pixel-wise Information Gain

> [!tip] 核心洞察
> 将“是否编辑及编辑到何种程度”的决策重新表述为信息论指标——编辑减少后验不确定性的程度，从而为重构-生成融合提供可解释、可泛化的像素级指导。

| 字段 | 内容 |
|------|------|
| 中文题名 | FaithFusion：通过像素级信息增益协调重建与生成 |
| 英文题名 | FaithFusion: Harmonizing Reconstruction and Generation via Pixel-wise Information Gain |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.21113) · [Project](https://shalfun.github.io/faithfusion) · [Code](https://github.com/wangyuanbiubiubiu/FaithFusion) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | FaithFusion |
| Dataset | Waymo |

> [!tip] 效果简介
> - Waymo (Lane Shift @3m) 上，FID 71.51 vs 84.12 (DIFIX3D+) (-12.61)。
> - Waymo (Lane Shift @6m) 上，FID 107.47 vs 120.24 (DIFIX3D+) (-12.77)；NTA-IoU 0.517 vs 0.504 (DIFIX3D+) (+0.013)；NTL-IoU 55.78 vs 53.77 (DIFIX3D+) (+2.01)。

## 概述

**问题瓶颈**：在自动驾驶场景的可控新视角合成中，现有方法面临一个根本性矛盾——基于几何的 3D Gaussian Splatting（3DGS）重建在偏离训练轨迹时产生严重伪影，而外观驱动的扩散模型虽能生成逼真内容，却缺乏像素级、3D 一致的编辑准则。直接融合二者往往导致**过度恢复**（扩散模型对已重建良好的区域也进行修改）和**几何漂移**（生成内容与底层 3D 结构不一致），使融合策略的收益被系统性误差累积所抵消。

**核心思想**：FaithFusion 将“是否编辑、在何处编辑、编辑到何种程度”的决策重新表述为一个**信息论问题**——编辑的价值在于它能在多大程度上减少渲染结果的后验不确定性。基于此，方法引入**像素级期望信息增益**（Expected Information Gain, EIG）作为统一的编辑策略：EIG 量化每个像素在当前 3DGS 模型下的认知不确定性，高 EIG 区域对应模型“不知道”的部分（如未观测区域、几何模糊处），低 EIG 区域对应模型已充分学习的部分。

**方法定位**：FaithFusion 是一个 **3DGS-扩散融合框架**，通过 EIG 协调两个分支的协同工作：
- **生成分支**：EIG 作为空间先验引导扩散模型，仅在低置信区域生成内容，有效抑制过度恢复和几何漂移；
- **重建分支**：EIG 作为像素级损失权重，将扩散模型的编辑知识选择性蒸馏回 3DGS 结构，实现渐进式知识整合。

**主要结果**：在 Waymo 数据集的车道偏移新视角合成任务上，FaithFusion 取得了最优性能。在最具挑战性的 6 米横向偏移设置下，FID 达到 **107.47**，较主要融合基线 DIFIX3D+ 改善 **12.77**；NTA-IoU 和 NTL-IoU 也分别提升至 0.517 和 55.78。消融实验证实，EIG 引导、EIGent 生成模块和渐进式集成的逐步加入带来了持续的增益累积，验证了 EIG 作为统一编辑策略的有效性。

## 背景与动机

### 可控驾驶场景重建的瓶颈

自动驾驶场景的真实感重建与重渲染，要求模型在保持 3D 几何一致性的同时，能够泛化到偏离训练轨迹的新视角。当前主流方案可大致分为两类：**几何基重建方法**（如基于 3D Gaussian Splatting 的 **OmniRe**）擅长保持多视图几何一致性，但在大视角偏移下渲染质量急剧下降，产生模糊、伪影和几何塌缩；**外观驱动生成方法**（如 **FreeVS**）依赖 LiDAR 等额外条件，能生成高保真外观，却缺乏显式 3D 约束，导致时空不一致与几何漂移。

融合这两种范式——用扩散模型的生成能力填补 3DGS 在新视角下的渲染缺陷——成为自然思路。代表性融合方法 **ReconDreamer**、**ReconDreamer++** 和 **DIFIX3D+** 已初步验证了这一方向的有效性。然而，这些方法面临一个核心瓶颈：**缺乏像素级、3D 一致的编辑准则**。当前融合策略要么依赖视图级启发式规则，要么对整帧施加均匀的生成或微调强度，无法区分“哪些像素需要编辑”以及“编辑到何种程度”。这导致两个典型失败模式：

- **过度恢复（over-restoration）**：扩散模型在原本已渲染良好的区域也施加修改，破坏 3DGS 已正确重建的几何结构。
- **几何漂移（geometric drift）**：生成内容在多次迭代中逐渐偏离真实几何，误差在 3DGS-扩散循环中累积放大。

### 信息论视角的动机

FaithFusion 的核心洞察在于：**“是否编辑及编辑到何种程度”的决策，可以被重新表述为信息论指标——编辑减少后验不确定性的程度**。具体而言，3DGS 在新视角下渲染的某个像素，若其对应的后验不确定性高，则说明模型对该区域的几何/外观缺乏信心，需要扩散模型介入；反之，低不确定性区域应保留原始渲染，避免过度修改。

这一视角将融合问题从启发式规则提升为**可解释、可泛化的像素级指导信号**。FaithFusion 提出的**像素级期望信息增益（Expected Information Gain, EIG）**正是这一信号的量化形式：EIG 通过 Laplace 近似与 Fisher 信息累积，为每个渲染像素计算“观测该像素能将 3DGS 参数后验不确定性降低多少”，从而天然成为统一的编辑策略——**EIG 高的区域需要生成修复，EIG 低的区域应保持原样**。

### 现有方法缺口

表 1 的系统对比揭示了当前方法的几个关键缺口：

1. **额外条件依赖**：FreeVS 等纯生成方法需要 LiDAR、3D 框或 HDMap 作为条件输入，限制了其在无额外传感器场景下的适用性。FaithFusion 仅依赖原始 3DGS 渲染，无需外部条件。
2. **架构修改代价**：ReconDreamer++ 等融合方法需要显著的架构或几何修改（如分解建模、新轨迹场），而 FaithFusion 在现有 3DGS 基础上通过 EIG 加权损失即可实现选择性知识蒸馏。
3. **编辑粒度粗糙**：DIFIX3D+ 等基线缺乏像素级编辑控制，FaithFusion 的 EIG 作为空间先验，同时指导扩散生成（作为空间加权函数）和 3DGS 微调（作为像素级损失权重），实现了统一的细粒度编辑策略。

### 方法概览

FaithFusion 的 EIG 引导渐进式训练循环包含三个步骤（图 2）：首先从原始 3DGS 渲染横向偏移的新视角及其像素级 EIG 图；然后通过双分支 **EIGent** 模型修复高 EIG 区域——早期使用 Video DiT 保证时空一致性，后期使用 DIFIX3D+ 进行逐帧感知精炼；最后用 EIG 加权损失将修复后的视图选择性蒸馏回 3DGS。这一闭环使得 EIG 成为贯穿生成与重建的统一编辑策略，在 Waymo 数据集上实现了 FID 107.47（6 米车道偏移），较 DIFIX3D+ 基线改善 12.77。

## 核心创新

FaithFusion 的核心创新在于将 **3DGS–扩散模型融合中的编辑决策重新表述为信息论问题**，并通过像素级期望信息增益（Expected Information Gain, EIG）为生成与重建分支提供统一的、可解释的空间策略。其关键设计围绕以下三个 changed slots 展开。

### 1. 像素级编辑触发与强度控制

现有融合方法（如 **DIFIX3D+**、**ReconDreamer++**）缺乏精细的编辑准则，通常依赖视图级启发式或全局条件来决定“何处编辑、编辑多少”，这容易导致过度恢复（over-restoration）和几何漂移（geometric drift）。FaithFusion 将这一决策转化为像素级 EIG 的计算——EIG 量化了在新视角下观测到某像素能带来的后验不确定性减少量。高 EIG 区域对应 3DGS 渲染质量低、不确定性大的像素（如未观测区域），从而自然地标记出需要扩散模型修复的位置和强度。

这一设计的因果机制在于：EIG 作为空间先验，在生成分支中充当**空间加权函数**，引导扩散模型仅在高不确定性区域生成内容，有效抑制了对已重建良好区域的过度修改；在重建分支中，EIG 归一化后作为**像素级损失权重**，使 3DGS 微调聚焦于低置信区域的知识蒸馏。Figure 3 的验证实验表明，逐步保留高 EIG 区域会导致 PSNR 持续下降，确认了 EIG 与渲染质量之间的强负相关关系。

### 2. 生成分支中的 EIG 引导条件注入

与基线方法采用的无条件或全局条件注入不同，FaithFusion 提出了 **EIGent**——一个双分支、由粗到精的 EIG 引导修复模型。EIGent 的架构包含两个关键组件：

- **EIG 语义上下文编码分支**：将降采样的 EIG 图 $E$、噪声潜变量 $L_N$ 和 VAE 潜变量 $L$ 输入轻量级上下文编码器 $\mathcal{G}$，生成多尺度的 EIG 引导信号。
- **DIFIX 修复注入分支**：通过交叉注意力机制将上下文编码注入预训练的 DiT 去噪骨干网络，同时利用掩码 $M$ 抑制高 EIG 区域，实现可控修复。

其核心公式为：

$$\epsilon_\theta(z_t, t, C)_k = \epsilon_\theta(z_t, t, C)_k + M \odot \mathcal{G}(L_N, L, E)_k$$

该设计在早期使用 Video DiT 保证时空一致性，后期使用 DIFIX3D+ 进行逐帧感知精炼，形成了从粗到精的渐进式修复策略。消融实验证实，引入 EIGent 使整体 FID 下降 5.07，其中 FID-UCR（不可靠区域 FID）下降 6.22，表明视频生成有效补偿了新视角合成中的结构缺失。

### 3. 重构损失的像素级加权

传统 3DGS 优化采用均匀的 L1/SSIM 损失或仅依赖深度监督，无法区分不同像素的置信度。FaithFusion 将归一化 EIG 矩阵 $\lambda_{\text{EIG}}$ 作为像素级权重调制新视角图像重建损失：

$$\mathcal{L}_{\text{img}}^{\text{novel}} = \lambda_{\text{EIG}} \odot \left( \lambda_r \mathcal{L}_1^{\text{novel}} + (1 - \lambda_r) \mathcal{L}_{\text{SSIM}}^{\text{novel}} \right)$$

这一设计的因果链条为：EIG 高的像素对应渲染不可靠区域，赋予更高损失权重，迫使 3DGS 从扩散模型生成的内容中蒸馏知识；EIG 低的像素对应已重建良好区域，权重降低以避免破坏已有几何结构。结合稀疏深度监督 $\mathcal{L}_{\text{depth}}^{\text{novel}}$（来自相邻帧的点云投影），总损失为：

$$\mathcal{L}_{\text{novel}}(\omega) = \mathcal{L}_{\text{img}}^{\text{novel}} + \lambda_d \mathcal{L}_{\text{depth}}^{\text{novel}}$$

这种跨模态的 EIG 引导机制——生成侧用 EIG 抑制内容、重建侧用 EIG 选择性蒸馏——构成了 FaithFusion 协调重建与生成的核心闭环。消融实验（Table 2）表明，端到端的渐进式集成最终使 FID 较 DIFIX3D+ 基线降低 12.77，且 FID-UCR 和 FID-HPR 分别下降 10.95 和 4.91。

## 整体框架

FaithFusion 是一个以**像素级期望信息增益（Expected Information Gain, EIG）**为统一驱动信号的 3DGS-扩散模型融合框架。其核心设计理念在于：将“何处编辑、何时编辑、编辑到何种程度”的启发式决策，重新表述为可计算的信息论指标——EIG 量化了通过观测新视角数据所能减少的渲染后验不确定性，从而为生成与重建两条分支提供可解释、可泛化的像素级指导。

### 管线总览

如图 2 所示，FaithFusion 采用**渐进式 EIG 引导训练循环**，包含三个紧密耦合的步骤：

1. **新视角合成（Novel-view Synthesis）**：从原始 3DGS 渲染横向偏移的新视角图像，同时计算对应的像素级 EIG 图。该 EIG 图作为渲染质量的代理指标，高 EIG 区域标记了 3DGS 在新视角下重建不可靠的像素位置。

2. **EIGent 修复（EIGent Fixed）**：将渲染结果与 EIG 图输入双分支生成模型 EIGent，对高 EIG 区域进行可控修复。早期利用 Video DiT 保证时空一致性，后期使用 DIFIX3D+ 进行逐帧感知精炼，形成从粗到细的生成策略。

3. **EIG 引导的 3DGS 更新（EIG-guided 3DGS Update）**：使用 EIGent 修复后的视图微调 3DGS 模型。在此阶段，归一化的 EIG 矩阵作为像素级损失权重，使模型选择性蒸馏生成分支的知识——高 EIG 区域获得更高的优化关注，而低 EIG（高置信度）区域则被约束以保持原有几何结构。

### 统一编辑策略：EIG 的跨模态角色

EIG 在整个管线中扮演双重角色，构成了框架的统一编辑策略：

- **在生成侧**：EIG 作为空间先验，引导扩散模型仅在低置信度区域生成内容，有效抑制过度恢复（over-restoration）和几何漂移（geometric drift）。具体而言，EIGent 通过掩码机制 $M$ 和多尺度上下文编码 $\mathcal{G}(L_N, L, E)$ 将 EIG 信息注入 DiT 去噪过程（公式 6），实现像素级可控修复。

- **在重建侧**：归一化 EIG 图作为像素级损失权重 $\lambda_{\mathrm{EIG}}$，调制新视角图像重建损失（公式 8）：
  $$\mathcal{L}_{\mathrm{img}}^{\mathrm{novel}} = \lambda_{\mathrm{EIG}} \odot \left( \lambda_r \mathcal{L}_1^{\mathrm{novel}} + (1 - \lambda_r) \mathcal{L}_{\mathrm{SSIM}}^{\mathrm{novel}} \right)$$
  这使 3DGS 微调聚焦于高不确定性区域，同时保留已可靠重建的部分。

### EIG 作为渲染质量的代理指标

框架的有效性建立在 EIG 与新视角合成质量之间的强相关性之上。通过 Laplace 近似与 Fisher 信息累积（公式 3-5），FaithFusion 计算像素级 EIG 上界：
$$\mathrm{EIG} \leq \frac{1}{2} \sum_i \mathrm{tr}\left( H''[Y_i^{\mathrm{NVS}} | X_i^{\mathrm{NVS}}, \omega^*] \, H''[\omega^*]^{-1} \right)$$

实验验证（图 3）表明，随着高 EIG 区域被逐步保留，渲染 PSNR 持续下降，确认了高 EIG 确实标记低质量渲染区域。这一特性使 EIG 成为无需额外监督即可指导生成-重建融合的可靠信号。

### 与现有融合方法的区别

相较于 DIFIX3D+ 等现有融合方法采用的视图级启发式或无明确控制策略，FaithFusion 的关键创新在于将编辑触发与强度控制从视图级提升到像素级，并通过信息论框架赋予了可解释性。这使框架能够在保持 3D 一致性的同时，有针对性地修复未观测区域的渲染伪影，而非对整帧进行无差别生成。

### 补充图表

![[assets/figures/papers/paper_list_l2484_https_arxiv_org_abs_2511_21113/figures/002_Figure_2.jpg]]
*Figure 2: FaithFusion pipeline. The EIG-guided progressive training loop with three steps: Step 1: Novel-view synthesis. Render laterally offset novel views and their pixel-level EIG maps from the original 3DGS. Step 2: EIGent Fixed. Feed the renders and EIG maps into EIGent to repair high-EIG regions—using Video DiT early for spatio-temporal consistency and DIFIX3D+ later for per-frame perceptual refinement. Step 3: EIG-guided 3DGS Update. Fine-tune the 3DGS model with the EIGent-restored views and EIG maps*

## 核心模块与公式推导

FaithFusion 的核心设计围绕一个统一的信息论指标——像素级期望信息增益（Expected Information Gain, EIG）展开。EIG 同时承担三重角色：生成分支中的空间先验、重构分支中的损失权重，以及连接两者的知识蒸馏桥梁。以下按管线顺序拆解关键模块及其数学基础。

### 3DGS 渲染与优化基础

FaithFusion 建立在 3D Gaussian Splatting（3DGS）之上。给定相机位姿 $X_i$，3DGS 通过沿射线对有序高斯体集合 $\mathcal{M}$ 进行 Alpha 混合，计算像素颜色：

$$\mathbf { C } = \sum _ { i \in \mathcal { M } } \mathbf { c } _ { i } \alpha _ { i } ^ { \prime } \prod _ { j = 1 } ^ { i - 1 } \left( 1 - \alpha _ { j } ^ { \prime } \right)$$

其中 $\mathbf{c}_i$ 为高斯体颜色，$\alpha_i'$ 为经 2D 投影和不透明度调制后的有效 Alpha 值。记渲染函数为 $\mathcal{F}(X_i, \omega)$，$\omega$ 为 3DGS 全体参数。在训练轨迹 $\mathcal{D}_{train}$ 上，3DGS 通过最小化重建误差获得最优参数 $\omega^*$：

$$\omega ^ { * } = \arg \min _ { \omega } \sum _ { ( X _ { i } , Y _ { i } ) \in \mathcal { D } _ { t r a i n } } \| Y _ { i } ^ { t r a i n } - \mathcal { F } ( X _ { i } ^ { t r a i n } , \omega ) \| _ { 2 } ^ { 2 }$$

这一优化仅在训练视角上收敛，当相机横向偏移至新轨迹时，$\omega^*$ 泛化能力有限，产生大量渲染伪影——这正是 EIG 需要捕获和修复的核心问题。

### 像素级期望信息增益计算

EIG 的推导从贝叶斯视角出发：将 $\omega^*$ 视为后验分布的众数，利用 Laplace 近似将参数后验建模为高斯分布：

$$\Omega \approx \mathcal{N} ( \omega ^ { * }, H ^ { \prime \prime } [ \omega ^ { * } ] ^ { - 1 } )$$

其中 $H''[\omega^*]$ 为在 $\omega^*$ 处的 Hessian 矩阵。对于新视角 $(X_i^{NVS}, Y_i^{NVS})$，其期望信息增益定义为先验熵与期望后验熵之差：

$$\mathrm { E I G } = \mathbb { H } [ \Omega ] - \mathbb { E } _ { p ( Y _ { i } | X _ { i } ) } [ \mathbb { H } [ \Omega | Y _ { i } ^ { N V S } , X _ { i } ^ { N V S } ] ]$$

直观上，EIG 量化了观测某个像素后参数不确定性的预期减少量：高 EIG 意味着该像素包含大量 3DGS 尚未捕获的结构信息，即渲染质量差的区域；低 EIG 则表明现有模型已能可靠重建。

直接计算 EIG 涉及高维积分，不可行。FaithFusion 利用对数行列式不等式推导出可计算的上界：

$$\mathrm { E I G } \leq \frac { 1 } { 2 } \sum _ { i } \mathrm { t r } \left( H ^ { \prime \prime } [ Y _ { i } ^ { N V S } | X _ { i } ^ { N V S } , \omega ^ { * } ] \cdot H ^ { \prime \prime } [ \omega ^ { * } ] ^ { - 1 } \right)$$

该上界将 EIG 分解为逐像素 Fisher 信息与全局 Fisher 信息逆矩阵的迹，可在 3DGS 渲染过程中高效累积计算（详见 Algorithm 1）。Figure 3 的验证实验表明，逐步保留高 EIG 区域时 PSNR 持续下降，确认了 EIG 作为新视角合成质量代理的有效性。

![[assets/figures/papers/paper_list_l2484_https_arxiv_org_abs_2511_21113/figures/003_Figure_3.jpg]]
*Figure 3: Image quality vs. EIG mask threshold. We validate pixel-level EIG as a proxy for novel-view synthesis quality by progressively retaining high-EIG regions and evaluating PSNR. The consistent decrease in PSNR as high-EIG regions are retained confirms that higher EIG marks lower-quality rendering*

### EIGent：EIG 引导的双分支修复模型

生成修复模块 EIGent 是 FaithFusion 的核心创新之一。它是一个双分支模型，以粗到细的方式将 EIG 空间先验注入预训练扩散模型。其数据构建采用跨视角配对策略：用前向相机训练的 3DGS 渲染右前视角，生成含伪影的新视角渲染图和逐像素 EIG 图，与真实右前视频帧时序对齐。

在去噪过程中，EIGent 通过上下文编码器 $\mathcal{G}$ 将下采样 EIG 图 $E$、噪声隐变量 $L_N$ 和 VAE 隐变量 $L$ 融合为引导信号，并通过掩码 $M$ 抑制高 EIG 区域的内容生成，将修复聚焦于低置信区域。引导信号经交叉注意力注入预训练 DiT 主干：

$$\epsilon _ { \theta } ( z _ { t } , t , C ) _ { k } = \epsilon _ { \theta } ( z _ { t } , t , C ) _ { k } + M \odot \mathcal { G } ( L _ { N } , L , E ) _ { k }$$

EIGent 采用两阶段策略：早期使用 Video DiT 保证时空一致性，后期切换为 DIFIX3D+ 进行逐帧感知精炼。这种设计在保持前景几何一致性的同时，有效补偿了新视角中的缺失结构。

### EIG 加权渐进式 3DGS 微调

修复后的新视角需将生成知识蒸馏回 3DGS 表示。FaithFusion 设计了双轨损失函数。原始轨迹损失保持标准形式：

$$\mathcal { L } _ { o r i } ( \omega ) = \lambda _ { r } \mathcal { L } _ { 1 } ^ { o r i } + ( 1 - \lambda _ { r } ) \mathcal { L } _ { S S I M } ^ { o r i } + \lambda _ { d } \mathcal { L } _ { d e p t h } ^ { o r i }$$

新视角损失则引入归一化 EIG 矩阵 $\lambda_{EIG}$ 作为像素级权重：

$$\mathcal { L } _ { \mathrm { i m g } } ^ { \mathrm { n o v e l } } = \lambda _ { \mathrm { E I G } } \odot \left( \lambda _ { r } \mathcal { L } _ { 1 } ^ { \mathrm { n o v e l } } + ( 1 - \lambda _ { r } ) \mathcal { L } _ { \mathrm { S S I M } } ^ { \mathrm { n o v e l } } \right)$$

$$\mathcal { L } _ { \mathrm { n o v e l } } ( \omega ) = \mathcal { L } _ { \mathrm { i m g } } ^ { \mathrm { n o v e l } } + \lambda _ { d } \mathcal { L } _ { \mathrm { d e p t h } } ^ { \mathrm { n o v e l } }$$

$\lambda_{EIG}$ 的核心作用在于选择性知识蒸馏：高 EIG 区域获得更大损失权重，驱动 3DGS 从 EIGent 输出中学习新结构；低 EIG 区域权重趋近于零，保护已可靠重建的部分免受生成噪声干扰。这种机制从根源上抑制了融合方法中常见的过度恢复和几何漂移问题——消融实验（Table 2）证实，仅引入 EIG 加权损失即可使 FID 下降约 1.23，而完整的渐进式集成最终将 FID 从 DIFIX3D+ 基线的 120.24 降至 107.47，改善幅度达 12.77。

### 补充图表

![[assets/figures/papers/paper_list_l2484_https_arxiv_org_abs_2511_21113/figures/004_Figure_4.jpg]]
*Figure 4: Overview of EIGent. Data: Cross-view pairing: a forward-camera–trained 3DGS renders right-front views to produce artifactprone novel-view renders and per-pixel EIG (Alg. 1), temporally aligned with real right-front videos. Architecture: EIGent is a dual-branch model with coarse-to-fine EIG guidance: downsampled E, noise latent*

## 实验与分析

### 实验设置

FaithFusion 在 Waymo 开放数据集上进行评估，核心任务为**可控驾驶场景下的横向车道偏移新视角合成**。实验设置 3 m 和 6 m 两种偏移幅度，模拟自动驾驶中车辆变道时的观测视角变化。评估指标涵盖三个维度：**FID** 衡量生成图像的感知质量与分布对齐；**NTA-IoU** 和 **NTL-IoU** 分别评估新视角下外观和布局与真实观测的结构一致性。对比方法包括纯生成方法 **FreeVS**、3DGS 重建基线 **OmniRe**、以及融合方法 **ReconDreamer**、**ReconDreamer++** 和 **DIFIX3D+**（主要融合基线，不依赖额外条件输入）。为公平对比，FreeVS 的输出在计算指标时裁切至仅保留 LiDAR 覆盖区域。

### 主实验结果

Table 1 给出了不同车道偏移下的定量对比。FaithFusion 在所有偏移设置下均取得最优结果：

![[assets/figures/papers/paper_list_l2484_https_arxiv_org_abs_2511_21113/figures/006_Table_1.jpg]]
*Table 1: Comparison of different lane shifts on the Waymo dataset [41], highlighting key methodology requirements. Extra Condition indicates the reliance on additional data injected as a condition to guide the synthesis process (e.g., LiDAR, 3D boxes, HDMap). ∗ denotes that the method requires significant architectural or geometrical modifications, including decomposed modeling and new trajectory field*

**3 m 车道偏移：**
- FID 达到 **71.51**，较 DIFIX3D+ 的 84.12 降低 12.61，降幅约 15.0%。
- 相比依赖额外条件（LiDAR、3D boxes、HDMap）的方法，FaithFusion 在不引入额外模态输入的前提下实现了更优的感知质量。

**6 m 车道偏移（最具挑战性设置）：**
- FID 降至 **107.47**，较 DIFIX3D+ 的 120.24 降低 **12.77**，改善幅度约 10.6%。
- NTA-IoU 达到 **0.517**（DIFIX3D+: 0.504），NTL-IoU 达到 **55.78**（DIFIX3D+: 53.77），表明 EIG 驱动的融合策略在极端偏移下仍能维持几何与外观一致性。

Figure 5 的定性对比进一步验证：在相同轨迹的新视角渲染中，FaithFusion 在遮挡边界、远距离纹理等挑战性区域（橙色框标注）展现出明显更优的细节保真度和结构完整性。

![[assets/figures/papers/paper_list_l2484_https_arxiv_org_abs_2511_21113/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison on Waymo [41]. Novel-view renderings for the same trajectory across representative methods [35, 46, 47, 64]. Orange boxes highlight regions where our approach yields noticeably better results*

![[assets/figures/papers/paper_list_l2484_https_arxiv_org_abs_2511_21113/figures/011_Figure_S.2.jpg]]
*Figure S.2: Extended Qualitative Comparison on Waymo. This figure provides additional novel view renderings for the same trajectory across representative methods, complementing the results shown in Fig. 5 of the main paper. Our method (last column) consistently maintains superior detail and fidelity across challenging regions, highlighted by the orange boxes, compared to methods [35, 46, 47]*

### 消融实验

为解耦 FaithFusion 各组件的贡献，Table 2 以 DIFIX3D+ 为基线，在 6 m 偏移任务上逐步引入三个 EIG 引导模块：

![[assets/figures/papers/paper_list_l2484_https_arxiv_org_abs_2511_21113/figures/007_Table_2.jpg]]
*Table 2: Ablation Study: Incremental Contributions of Faith-Fusion’s Core Components. Results on the most challenging 6-meter lateral-shift novel-view synthesis task, showing the gain from sequentially adding the three proposed EIG-guided modules to the DIFIX3D+ baseline*

**EIG 引导的扩散生成：**
引入像素级 EIG 作为空间先验指导扩散模型仅在低置信区域生成内容，使 FID 下降约 **1.23**。这一改进虽幅度有限，但验证了信息论指标替代启发式编辑决策的有效性——EIG 能精准定位需要修复的像素，避免对已可靠区域的过度修改。

**EIGent 修复模块：**
在 EIG 引导基础上加入 EIGent（双分支 EIG 感知修复模型），FID 进一步降低 **5.07**，FID-UCR（不可靠区域 FID）降低 **6.22**。这表明 EIGent 的视频级时空一致性生成能力有效补偿了新视角合成中的几何漂移，尤其在 EIG 标记的高不确定性区域。

**渐进式集成（完整 FaithFusion）：**
将 EIGent 修复后的视图通过 EIG 加权损失蒸馏回 3DGS，实现端到端渐进式训练。最终 FID 达到 **107.47**，较基线改善 **12.77**；FID-UCR 和 FID-HPR（高置信区域 FID）分别下降 **10.95** 和 **4.91**。值得注意的是，高置信区域的 FID 也有改善，说明 EIG 加权损失在选择性蒸馏生成知识时，并未破坏已有的可靠渲染。

Figure 6 的可视化消融直观展示了 EIG 引导组件逐步抑制过度恢复和几何漂移的过程：基线方法在遮挡区域产生明显的纹理扭曲和几何错位，而完整 FaithFusion 保持了与真实观测高度一致的几何结构和外观细节。

![[assets/figures/papers/paper_list_l2484_https_arxiv_org_abs_2511_21113/figures/008_Figure_6.jpg]]
*Figure 6: Ablation overview. We incrementally integrate EIG-guided components into the OmniRe baseline. The results highlight the incremental contributions of EIG guidance in resolving over-restoration and geometric drift by acting as a unified pixel-wise editing policy*

### EIG 作为渲染质量代理的验证

Figure 3 通过渐进式保留高 EIG 区域并评估 PSNR，验证了像素级 EIG 与新视角合成质量之间的强相关性。随着高 EIG 区域被逐步保留，PSNR 持续下降，证实**更高的 EIG 值确实标记了更低质量的渲染区域**。这一发现为 EIG 作为统一编辑准则提供了实证基础——EIG 不仅是理论上的信息增益度量，更是实践中可靠的渲染质量代理。

### 失败模式与局限性

尽管 FaithFusion 在各项指标上取得显著提升，分析仍揭示了两类值得关注的局限：

1. **误差积累未完全消除：** EIG 有效减缓了 3DGS-扩散融合中的误差传播，但在极端未观测区域（如大角度旋转、长距离遮挡），修复后的视图仍可能引入细微的纹理不一致，并在后续 3DGS 微调中被部分固化。这可能源于当前 3DGS 表示本身对分布外视角的泛化能力有限。

2. **底层表示的限制：** 当前方法建立在标准 3DGS 架构之上，未对高斯原语的分布、密度或各向异性进行专门设计。在 6 m 偏移下，某些场景的几何漂移仍可察觉，提示可能需要定制化的 3DGS 架构来从根本上提升融合鲁棒性。

### 关键图表结论

- **Table 1：** FaithFusion 在 3 m 和 6 m 偏移下均以显著优势超越所有对比方法，且无需依赖 LiDAR 等额外条件输入。
- **Table 2：** EIG 引导的渐进式集成使 FID 累计改善 12.77，其中 EIGent 贡献最大（5.07），端到端蒸馏进一步释放了融合潜力。
- **Figure 3：** 像素级 EIG 与渲染质量呈单调负相关，验证了其作为编辑准则的可靠性。
- **Figure 5：** 定性结果中，FaithFusion 在遮挡恢复和远距离细节保持上明显优于 DIFIX3D+ 和 ReconDreamer++。

### 补充图表

![[assets/figures/papers/paper_list_l2484_https_arxiv_org_abs_2511_21113/figures/009_Figure_7.jpg]]
*Figure 7: Region partition for EIG-based evaluation. We use EIG as a proxy for rendering quality. With a threshold τ = 0.4, renderings are partitioned into UCR and HPR, and we report regionspecific metrics: FID-UCR and FID-HPR*

![[assets/figures/papers/paper_list_l2484_https_arxiv_org_abs_2511_21113/figures/001_Figure_1.jpg]]
*Figure 1: Comparative overview. Comparison of FreeVS [46], OmniRe [7], the fusion-based methods DIFIX3D+ [47] and ReconDreamer++ [64], and our EIG-integrated FaithFusion, which simultaneously achieves consistency, quality, and faithfulness*

## 方法谱系与知识库定位

### 1. 基线对比与差异化定位

FaithFusion 位于**3DGS-扩散模型融合**的交叉点上，其核心差异化在于将“编辑决策”从启发式规则提升为**信息论驱动的像素级策略**。表 1 将主要对比方法按方法论需求进行了分类，清晰揭示了 FaithFusion 在条件依赖和架构侵入性上的优势。

**纯生成方法**：**FreeVS** 依赖 LiDAR 等额外条件直接生成新视角，无需 3D 重建，但其输出在无 LiDAR 覆盖区域存在伪影，且缺乏显式几何约束。FaithFusion 不依赖此类额外条件，而是通过 EIG 在 3DGS 渲染基础上进行选择性修复，保持了几何一致性。

**纯重建方法**：**OmniRe** 作为 3DGS 重建基线，在新视角合成时面临过度恢复和几何漂移问题，尤其在大偏移场景下质量急剧下降。FaithFusion 在 OmniRe 等 3DGS 重建基线上叠加扩散修复能力，但通过 EIG 加权损失仅在高不确定性区域蒸馏生成知识，避免了全局修改对已重建区域的破坏。

**融合方法**：这是 FaithFusion 最直接的竞争谱系。
- **DIFIX3D+** 作为主要融合基线，采用扩散模型修复新视角渲染，但缺乏像素级编辑策略，导致生成内容可能覆盖原本重建良好的区域，产生过度恢复。FaithFusion 在 DIFIX3D+ 基线上逐步加入 EIG 指导、EIGent 和渐进式集成，最终在 6 米车道偏移下将 FID 从 120.24 降至 107.47（改善 12.77），NTA-IoU 从 0.504 提升至 0.517。
- **ReconDreamer** 和 **ReconDreamer++** 需要显著的架构或几何修改（如分解建模和新轨迹场），而 FaithFusion 的 EIG 策略可直接嵌入现有 3DGS 管线，无需改变底层表示。

### 2. 方法适用边界

**优势场景**：
- **大偏移新视角合成**：在 Waymo 数据集的 6 米车道偏移任务上，FaithFusion 的 FID 优势随偏移增大而更加显著（3 米时改善 12.61，6 米时改善 12.77），表明 EIG 策略在极端未观测区域具有更强的补偿能力。
- **无需额外条件的场景**：FaithFusion 不依赖 LiDAR、3D 框或 HDMap 等外部条件，使其在仅有图像输入的自动驾驶场景重建中具有更广泛的适用性。

**局限与约束**：
- **误差累积未完全消除**：EIG 虽然有效减缓了 3DGS-扩散融合中误差的积累，但问题并未根本解决。当前方法仍建立在现有 3DGS 基础上，未对底层表示进行专门设计，可能限制了对极端未观测区域的泛化能力。消融实验显示，即使完整 FaithFusion 的 FID-UCR 仍为 43.23，表明高不确定性区域仍存在可改进空间。
- **3DGS 架构依赖**：EIG 计算基于 Laplace 近似和 Fisher 信息累积，其有效性依赖于 3DGS 参数后验的高斯近似质量。在 3DGS 表示本身存在系统性偏差的场景（如天空区域，论文中单独处理），EIG 的可靠性可能下降。
- **超参数敏感性**：EIG 阈值 τ（用于 UCR/HPR 区域划分，论文中使用 τ=0.4）在不同场景下的自适应调整策略尚未明确。

### 3. 开放问题与未来方向

FaithFusion 将信息论指标引入 3DGS-扩散融合范式，为以下研究方向提供了新的切入点：

1. **定制化 3DGS 架构设计**：当前 EIG 策略是对现有 3DGS 的“外挂式”增强。能否针对 3DGS-扩散融合范式设计专门的 3DGS 架构，从根本上抑制几何漂移？例如，在 3DGS 参数化中显式建模不确定性，使 EIG 计算更加精准。

2. **主动探索与建图**：EIG 本质上量化了观测的信息增益，这与主动建图中的“下一步最佳视角”选择天然契合。如何将 EIG 纳入主动探索策略，以提升整体重建效率，是一个有前景的方向。

3. **跨场景自适应**：EIG 阈值等关键超参数在不同场景（城市、高速、乡村）和不同偏移幅度下的自适应调整策略，需要系统的实验验证和理论分析。

4. **与其他重建表示的兼容性**：EIG 框架的核心是“像素级不确定性量化 + 选择性修复”，这一思想是否可迁移至 NeRF、3D Gaussian Splatting 的其他变体，或更广泛的神经渲染管线中，值得进一步探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/FaithFusion_Harmonizing_Reconstruction_and_Generation_via_Pixel_wise_Information_Gain.pdf]]