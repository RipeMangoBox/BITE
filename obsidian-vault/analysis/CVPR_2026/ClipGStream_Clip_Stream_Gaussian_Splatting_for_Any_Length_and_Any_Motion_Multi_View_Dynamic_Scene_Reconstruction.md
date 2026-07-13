---
title: "ClipGStream: Clip-Stream Gaussian Splatting for Any Length and Any Motion Multi-View Dynamic Scene Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ClipGStream_Clip_Stream_Gaussian_Splatting_for_Any_Length_and_Any_Motion_Multi_View_Dynamic_Scene_Reconstruction.pdf
project_link: "https://liangjie1999.github.io/ClipGStreamWeb/"
code_link: null
aliases:
- ClipGStream
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过从参考剪辑继承并冻结静态特征、锚点和解码器，同时为每个源剪辑引入残差锚点补偿和独立时空场，既保证了跨剪辑的时间一致性，又能有效捕捉大规模位移和局部动态变化。
primary_logic: 将视频分割为参考剪辑和多个源剪辑，在剪辑内部采用独立时空场和残差锚点补偿以实现局部运动建模，在剪辑间通过继承冻结的静态组件来维持全局时间一致性，从而实现了可扩展、无闪烁的长序列动态重建框架。
claims:
- 在Long 360数据集上，ClipGStream在所有指标上均优于其他方法，PSNR达到24.54。
- 消融实验表明，移除残差锚点补偿模块(RAC)或锚点继承模块(AI)会导致跨剪辑闪烁加剧，而同时启用则显著抑制闪烁。
- ClipGStream在N3DV flame salmon场景（1200帧）上超越了先前最优方法，PSNR达29.40，SSIM 0.917。
- Long 360 (1400 frames) 上 PSNR = 24.54
---

# ClipGStream: Clip-Stream Gaussian Splatting for Any Length and Any Motion Multi-View Dynamic Scene Reconstruction

> [!tip] 核心洞察
> 将视频分割为参考剪辑和多个源剪辑，在剪辑内部采用独立时空场和残差锚点补偿以实现局部运动建模，在剪辑间通过继承冻结的静态组件来维持全局时间一致性，从而实现了可扩展、无闪烁的长序列动态重建框架。

| 字段 | 内容 |
|------|------|
| 中文题名 | ClipGStream：适用于任意长度和任意运动的多视角动态场景重建的Clip-Stream高斯泼溅 |
| 英文题名 | ClipGStream: Clip-Stream Gaussian Splatting for Any Length and Any Motion Multi-View Dynamic Scene Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.13746) · [Project](https://liangjie1999.github.io/ClipGStreamWeb/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | ClipGStream |
| Dataset | Long 360, VRU, Neural 3D Video Dataset, N3DV flame salmon |

> [!tip] 效果简介
> - Long 360 (1400 frames) 上，PSNR 24.54 vs 21.94 (3DGStream) (+2.60)。
> - Long 360 上，DSSIM1 0.079 vs 0.085 (2DGS static, best static) (-0.006)。
> - VRU (GZ) 上，PSNR / SSIM / LPIPS 30.67 / 0.946 / 0.137 vs Best competitor (see Table 2) (显著提升)。

## 概要

多视角动态场景重建面临两大核心挑战：**长序列建模**与**大规模运动捕捉**。现有方法可分为两类——帧流式（Frame-Stream）方法（如 **3DGStream**，Sun et al., CVPR 2024）可逐帧扩展但存在帧间抖动与累积误差；剪辑式（Clip）方法（如 **4DGaussian**, Wu et al., CVPR 2024；**SpaceTimeGS**, Li et al., CVPR 2024）具有局部时间一致性，但内存开销随序列长度线性增长，难以处理超长序列。两类方法均未同时解决可扩展性与大规模运动建模的冲突。

ClipGStream 提出首个 **Clip-Stream 动态重建框架**，核心思路是将完整视频分割为一个参考剪辑（Reference Clip）和多个源剪辑（Source Clips），在剪辑内部通过独立时空场和残差锚点补偿建模局部运动，在剪辑间通过继承并冻结参考剪辑的静态特征、锚点和解码器来维持全局时间一致性。这一设计的关键因果机制在于：**静态特征承载所有背景信息，跨剪辑共享可保证时间一致性；动态特征仅学习控制动态内容可见性的残差信息，因此各剪辑可独立建模**。

在包含 1400 帧的 Long 360 数据集上，ClipGStream 的 PSNR 达到 **24.54**，较帧流式最优方法 3DGStream（21.94）提升 **+2.60 dB**，且在所有指标上均优于对比方法。在 N3DV flame salmon 场景（1200 帧）上，PSNR 达 **29.40**，超越先前最优方法 Grid4D 和 LocalDyGS。消融实验进一步验证：移除残差锚点补偿模块（RAC）或锚点继承模块（AI）会导致跨剪辑静态区域出现强烈残差响应（闪烁），同时启用两者则显著抑制闪烁，证明了两组件在维持跨剪辑稳定性中的关键作用。



多视角动态场景重建的目标是从同步拍摄的多个视频流中恢复出随时间变化的三维几何与外观，这一任务在自由视点视频、VR/AR、体育转播等应用中具有核心地位。近年来，基于三维高斯泼溅（3D Gaussian Splatting, 3DGS）的方法在静态场景重建中取得了显著成功，其显式点云表示与高效可微光栅化管线使得实时渲染成为可能。然而，将3DGS扩展到动态场景——尤其是**任意长度、任意运动幅度**的长序列——仍面临根本性挑战。

### 现有范式的结构性缺陷

当前主流的动态3DGS方法可归为两类范式，各自存在难以调和的局限性。

**帧流式方法（Frame-Stream）** 以 **3DGStream**（Sun et al., CVPR 2024）为代表，逐帧增量更新高斯场，理论上可处理任意长序列。但其因果式更新机制缺乏全局时间约束，导致两个致命问题：一是**帧间抖动**——相邻帧的几何与外观缺乏一致性约束，渲染结果出现肉眼可见的高频闪烁；二是**累积误差**——每帧的微小估计偏差沿时间轴传播放大，序列末端重建质量严重退化。在Long 360数据集（1400帧）上，3DGStream的PSNR仅为21.94，远低于静态方法的上限参考。

**剪辑式方法（Clip）** 将长视频分割为若干短剪辑，在每个剪辑内独立优化时空表示，代表工作包括 **4DGaussian**（Wu et al., CVPR 2024）、**SpaceTimeGS**（Li et al., CVPR 2024）、**LocalDyGS**（Wu et al., ArXiv 2025）和 **Grid4D**（Jiawei et al., NeurIPS 2024）。剪辑内联合优化天然保证了局部时间一致性，但引入两个新瓶颈：其一，**序列长度受限**——随序列增长，剪辑内需建模的时空复杂度急剧上升，内存开销与训练时间不可扩展；其二，**剪辑间闪烁**——各剪辑独立优化导致剪辑边界处静态背景出现跳变，表现为跨剪辑的伪影。图9的时序PSNR分析直接揭示了LocalDyGS在短剪辑配置下的时间不稳定性及其在长序列配置下的训练失败。

### 瓶颈交汇：大规模运动与长序列的冲突

更深层的问题在于，**大规模运动**与**长序列建模**之间存在根本冲突。帧流式方法通过逐帧微调可适应大幅位移，但牺牲了时间一致性；剪辑式方法通过剪辑内联合优化保证了局部平滑，但面对大幅运动时，剪辑内的高斯场需要覆盖更大的空间范围，导致表示效率骤降、内存爆炸。现有方法无一能同时解决这两个需求。

### ClipGStream的核心动机

本文提出**ClipGStream**，旨在打破上述僵局。核心洞察是：将视频分割为**一个参考剪辑（Reference Clip）和多个源剪辑（Source Clip）**，在剪辑内部采用独立时空场和残差锚点补偿以灵活建模局部运动，在剪辑间通过继承并冻结参考剪辑的静态组件（锚点、静态特征、解码器）来维持全局时间一致性。这一“Clip-Stream”框架首次实现了可扩展、无闪烁的长序列动态重建，同时具备处理任意运动幅度的能力。



## 核心方法与创新机理

ClipGStream 提出首个 **Clip-Stream 动态重建框架**，通过将长视频分割为参考剪辑（Reference Clip）与多个源剪辑（Source Clip），在剪辑内部采用独立时空场与残差锚点补偿以建模局部运动，在剪辑间通过继承并冻结静态组件来维持全局时间一致性，从而同时解决大规模运动与长序列建模两大瓶颈。其核心创新体现在以下四个 changed slots 上。

### 跨剪辑一致性策略：继承并冻结而非独立优化

现有剪辑式方法（如 **4DGaussian** (Wu et al., CVPR 2024)、**SpaceTimeGS** (Li et al., CVPR 2024)、**LocalDyGS** (Wu et al., ArXiv 2025)）对各剪辑独立优化，导致剪辑边界出现闪烁伪影；帧流式方法（如 **3DGStream** (Sun et al., CVPR 2024)）虽可扩展但累积帧间误差。ClipGStream 的核心策略是：参考剪辑训练完成后，将其**锚点、静态特征和解码器继承至所有源剪辑并冻结**（Sec. 3.2.2）。这一设计的因果逻辑在于：静态特征编码了场景的背景与外观基元，跨剪辑共享可确保同一静态区域在不同剪辑中生成一致的外观；解码器继承则保证了几何-外观映射的连续性。消融实验（Table 5）验证了该策略的因果效应：移除解码器继承模块（DI）后，PSNR 从 24.54 降至 24.34；完全独立训练各剪辑（无任何继承）时 PSNR 仅为 21.85（Table 6），降幅达 2.69 dB。图 8 进一步显示，无解码器继承时渲染图像出现明显模糊，而继承解码器可恢复清晰细节。

### 锚点集构建：从单一 COLMAP 初始化到继承加残差补偿

传统方法直接从 COLMAP 重建点云初始化锚点，无法利用已学到的场景结构先验。ClipGStream 的锚点集构建公式为：

$$A_n = A_0 \cup A_n^r = A_0 \cup \mathrm{Dedup}(A_n^c, A_0)$$

即源剪辑的锚点集由继承自参考剪辑的基础锚点 $A_0$ 与经几何感知去重后的残差锚点 $A_n^r$ 的并集组成（Eq. (6)）。去重过程（Figure 4）将参考剪辑点云转化为球形覆盖场——每点 $p$ 的球半径 $r$ 定义为到其三个最近邻的平均欧氏距离（Eq. (7)）——然后对候选锚点 $q$ 计算有符号距离 $SDF(q)$：若 $SDF(q) > 0$（位于覆盖场外部），则保留为残差锚点；否则过滤。这一机制使新增或大幅位移的结构能获得专用锚点，而静态区域复用已有锚点，避免了冗余初始化带来的优化负担。消融实验（Table 5）显示，移除残差锚点补偿模块（RAC）导致 PSNR 从 24.54 降至 23.62。图 5 的跨剪辑残差热力图更直观地揭示了因果机制：移除 RAC 或锚点继承模块（AI）后，静态区域出现强烈残差响应（即闪烁），而同时启用两者可显著抑制闪烁。

### 时空场设计：从共享到剪辑专属

现有方法通常共享单个时空场（STF）建模所有时间动态，这在长序列中难以捕捉不同时段内差异显著的运动模式。ClipGStream 为每个剪辑分配独立的时空场 $STF_n$（Sec. 3.2.1），其动态特征计算为：

$$f_{d,n} = \phi_n(h_n(\mu_n, t))$$

其中 $h_n$ 为 4D 哈希网格，$\phi_n$ 为 MLP（Eq. (10)）。剪辑专属 STF 的因果逻辑在于：不同剪辑覆盖不同的时间窗口，其运动幅度、速度和模式可能截然不同；独立 STF 使每个剪辑能够专注于局部时间段的动态建模，而无需在全局共享参数中妥协。Table 6 的消融实验验证了这一设计的必要性：将独立 STF 替换为共享 STF 后，PSNR 从 24.54 降至 23.11，降幅达 1.43 dB。

### 静态特征处理：从重新学习到继承冻结

传统方法对每个剪辑重新学习静态特征，导致同一静态区域在不同剪辑中可能产生外观不一致。ClipGStream 将参考剪辑的静态特征 $f_{s,0}$ 继承并冻结，仅学习新增的残差静态特征 $f_{s,n}^r$，最终源剪辑的静态特征为拼接形式：

$$f_{s,n} = [f_{s,0}; f_{s,n}^r]$$

（Eq. (9)，Figure 3）。这一设计的因果机制在于：静态特征负责编码所有背景信息（Figure 3a），冻结继承部分确保了跨剪辑的背景外观一致性；可学习的残差部分则允许源剪辑补充参考剪辑中未出现的新静态结构。动态特征则负责控制动态内容的可见性，因此保持剪辑独立（Figure 3b）。这一静态-动态解耦策略是 ClipGStream 实现无闪烁长序列重建的关键使能因素。

### 创新总结

上述四个 changed slots 构成一个因果闭环：锚点继承与残差补偿确保了几何结构的跨剪辑连续性；静态特征冻结与残差学习保证了外观的时间一致性；剪辑专属时空场赋予各剪辑独立的运动建模能力；解码器继承则锁定了几何-外观的映射关系。这一设计使 ClipGStream 在 Long 360（1400 帧）上以 PSNR 24.54 显著超越帧流式最优方法 3DGStream（21.94，+2.60 dB）和剪辑式方法 4DGaussian（22.05），并在 N3DV flame salmon（1200 帧）上以 PSNR 29.40 超越先前 SOTA（Grid4D、LocalDyGS），验证了 Clip-Stream 范式的有效性。



ClipGStream 提出了一种 Clip-Stream 范式，将任意长度的多视角动态视频序列分割为若干时间上连贯的短剪辑，并通过两阶段训练策略实现可扩展、无闪烁的长序列重建。其核心设计在于：**剪辑内部**采用独立时空场与残差锚点补偿以捕捉局部复杂运动；**剪辑之间**通过继承并冻结参考剪辑的静态组件来维持全局时间一致性。

### 两阶段训练流水线

整个训练流程分为参考剪辑训练阶段与源剪辑训练阶段（Figure 2）。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_13746/figures/002_Figure_2.jpg]]
*Figure 2: Our training process is divided into two stages: the Reference Clip (Clip0) Training Stage and Source Clip*

**第一阶段：参考剪辑训练（Reference Clip Training）**
- 将视频的首个剪辑 $Clip_0$ 作为参考剪辑，融合该剪辑内所有帧的 COLMAP 点云初始化锚点集 $A_0$。
- 每个锚点被赋予可学习的静态特征 $f_{s,0}$，同时通过剪辑专属的时空场 $STF_0$（由 4D 哈希网格 $h_0$ 和全融合 MLP $\phi_0$ 组成）提取动态特征 $f_{d,0} = \phi_0(h_0(\mu_0, t))$。
- 静态与动态特征拼接后输入共享解码器 $d$，生成时域高斯（Temporal Gaussians）$G_{t,0} = d([f_{s,0}; f_{d,0}])$，再通过光栅化渲染进行端到端优化。
- 此阶段建立起包含静态背景和动态内容的稳定时空基表示。

**第二阶段：源剪辑训练（Source Clip Training）**
- 对于后续每个源剪辑 $Clip_n$（$n \in [1, N-1]$），继承参考剪辑的三类冻结组件：**锚点 $A_0$、静态特征 $f_{s,0}$ 和解码器 $d$**。
- **残差锚点补偿**：利用当前剪辑的 COLMAP 点云 $A_n^c$，通过几何感知去重模块筛选出与参考剪辑不重叠的新锚点作为残差锚点 $A_n^r$，构建完整的源剪辑锚点集 $A_n = A_0 \cup A_n^r$。
- **独立时空场**：为每个源剪辑分配全新的独立时空场 $STF_n$，以灵活建模该剪辑内的局部运动模式。
- **残差静态特征**：继承的静态特征被冻结，同时为新增残差锚点学习可训练的残差静态特征 $f_{s,n}^r$，拼接后形成完整的静态表示 $f_{s,n} = [f_{s,0}; f_{s,n}^r]$。
- 最终采用与参考剪辑相同的解码-渲染管线完成训练。

### 模块关系与数据流

各核心模块之间的依赖与数据流关系如下：

1. **锚点继承与去重模块**：参考剪辑锚点 $A_0$ 作为静态结构的骨架被完整保留；源剪辑新增的 COLMAP 候选锚点经过基于球形覆盖场的 SDF 过滤（$SDF(q) > 0$ 时保留），仅添加非重复的残差锚点（Figure 4）。这保证了静态区域的锚点一致性，同时允许动态/新出现区域获得新的几何载体。

2. **静态特征继承与冻结**：参考剪辑的静态特征 $f_{s,0}$ 编码了所有背景信息，跨剪辑共享并冻结可从根本上消除静态区域的帧间闪烁（Figure 3a）。新增的残差静态特征 $f_{s,n}^r$ 仅需学习与参考剪辑的差异部分。

3. **独立时空场分配**：每个剪辑拥有专属的 $STF_n$，使得不同剪辑内的动态内容（如人物大幅度位移）能被独立且充分地建模。消融实验证实，共享单个时空场会导致 PSNR 从 24.54 降至 23.11（Table 6），验证了剪辑专属 STF 的必要性。

4. **解码器继承**：所有剪辑复用同一个冻结的解码器 $d$，确保几何与外观的解码逻辑在剪辑间完全一致。移除解码器继承会导致渲染模糊（Figure 8），PSNR 从 24.54 降至 24.34（Table 5）。

5. **损失函数驱动**：整体训练目标为 $L = (1 - \lambda_{\mathrm{SSIM}}) L_1 + \lambda_{\mathrm{SSIM}} L_{\mathrm{SSIM}} + \lambda_v L_v$，其中 $L_v = \sum_{i=1}^{M} \mathrm{Prod}(s_t^i)$ 为体积正则化项，通过对活跃时域高斯的尺度求积并求和来促进紧凑性，减少浮动物。

### 输入输出规范

- **输入**：多视角视频序列，按时间轴分割为 $N$ 个剪辑；每个剪辑提供 COLMAP 估计的相机参数与稀疏点云。
- **输出**：每个剪辑的时域高斯表示，可在任意新视角和时间戳下通过 alpha 合成渲染出高保真图像。
- **推理**：渲染时根据目标时间戳选择对应剪辑的时域高斯，冻结的静态特征与解码器保证跨剪辑边界的无缝过渡。

> **需注意**：该方法依赖 COLMAP 为每个剪辑生成初始点云，对于极低纹理或运动模糊严重的场景可能存在鲁棒性瓶颈，但论文未对此进行定量消融。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_13746/figures/001_Figure_1.jpg]]
*Figure 1: ClipGStream enables scalable and temporally stable dynamic scene reconstruction for sequences of any length and any motion. (a) Unlike Frame-Stream methods that accumulate errors and Clip methods that produce clip-level flicker, ours Clip-Stream framework divides the video into a Reference Clip and subsequent Source Clips, where each Source Clip is trained on top of the trained representation of the Reference Clip to ensure robust large-motion handling and temporal consistency. (b) ClipGStream achieves higher reconstruction quality on the 1,400-frame Long 360 dataset. Cross-clip residual heatmaps show effective flicker suppression. (c) ClipGStream further surpasses prior SOTA methods on the...*



### 3D 高斯泼溅基础

ClipGStream 基于 3D Gaussian Splatting 框架构建。每个高斯基元由均值 $\mu$ 和协方差矩阵 $\Sigma$ 定义，其空间分布为：

$$G(x) = e^{-\frac{1}{2}(x-\mu)^T \Sigma^{-1} (x-\mu)}$$

渲染时，像素颜色 $C(p)$ 通过有序 2D 高斯的 alpha 合成得到：

$$C(p) = \sum_{i\in K} c_i \alpha_i(p) \prod_{j=1}^{i-1} (1-\alpha_j(p)), \quad \alpha_i(p) = \sigma_i G_i'(p)$$

为提升表达能力，方法从锚点生成神经高斯。给定锚点均值 $\mu_a$、可学习偏移量 $\{O_0, ..., O_{k-1}\}$ 和缩放因子 $l_a$，$k$ 个神经高斯的位置为：

$$\{\mu_0, ..., \mu_{k-1}\} = \mu_a + \{O_0, ..., O_{k-1}\} \cdot l_a$$

---

### 参考剪辑训练（Reference Clip Training）

参考剪辑 $Clip_0$ 首先进行完整优化，建立稳定的时空表示基础。其核心在于将每个锚点的静态特征与动态特征解耦，并通过共享解码器生成时域高斯。

**动态特征**通过时空场 $STF_0$ 提取，该场由 4D 哈希网格 $h_0$ 和全融合 MLP $\phi_0$ 组成：

$$f_{d,0} = \phi_0(h_0(\mu_0, t))$$

其中 $\mu_0$ 为锚点位置，$t$ 为时间编码。

**时域高斯生成**将静态特征 $f_{s,0}$ 与动态特征 $f_{d,0}$ 拼接后送入解码器 $d$：

$$G_{t,0} = d([f_{s,0}; f_{d,0}])$$

解码器输出时域高斯的全部属性（位置、协方差、颜色、不透明度等），经光栅化渲染为图像。

---

### 源剪辑训练与残差锚点补偿（Source Clip Training & Residual Anchors Compensation）

对于后续源剪辑 $Clip_n$（$n \in [1, N-1]$），方法继承参考剪辑的锚点集 $A_0$，并通过几何感知去重机制引入残差锚点 $A_n^r$，构成完整的锚点集：

$$A_n = A_0 \cup A_n^r = A_0 \cup \mathrm{Dedup}(A_n^c, A_0)$$

其中 $A_n^c$ 为当前剪辑 COLMAP 重建的候选锚点。

**几何感知去重**（Geometry-Aware Deduplication，Figure 4）的核心在于构建参考剪辑的球形覆盖场。对参考剪辑点云中的每个点 $p$，以其为中心、半径为 $r$ 构造球体，半径定义为到三个最近邻的平均欧氏距离：

$$r = \frac{1}{3}\sum_{i=1}^{3}\|p_i - p\|_2$$

对候选锚点 $q$，计算其到覆盖场表面的有符号距离 $SDF(q)$。若 $SDF(q) > 0$（位于覆盖场外部），则保留为残差锚点；否则视为冗余锚点予以剔除。这一机制确保仅新增或位移显著的结构才会被引入锚点集。

---

### 剪辑间继承机制（Inter-clip Inheritance）

剪辑间继承是 ClipGStream 保证跨剪辑时间一致性的核心设计，包含三个冻结共享的组件：

**静态特征继承与冻结**（Figure 3a）：参考剪辑的静态特征 $f_{s,0}$ 学习全部背景信息，将其冻结并传递给所有源剪辑。源剪辑 $Clip_1$ 的静态特征由冻结的继承特征与可学习的残差静态特征拼接而成：

$$f_{s,1} = [f_{s,0}; f_{s,1}^r]$$

其中 $f_{s,0}$ 冻结不更新，仅 $f_{s,1}^r$ 参与训练，用于捕捉剪辑间细微的背景变化。

**解码器继承**：参考剪辑的解码器 $d$ 被所有源剪辑复用并冻结，确保跨剪辑的几何与外观解码一致性。消融实验（Table 5, Figure 8）表明，移除解码器继承（DI）会导致渲染图像明显模糊，PSNR 从 24.54 降至 24.34。

**独立时空场**（Figure 3b）：与静态特征不同，动态特征学习控制动态内容可见性的残差信息，具有剪辑依赖性。因此每个源剪辑分配独立的时空场 $STF_n$：

$$f_{d,n} = \phi_n(h_n(\mu_n, t))$$

消融实验（Table 6）验证了这一设计的必要性：若所有剪辑共享单个 $STF$，PSNR 从 24.54 骤降至 23.11，表明剪辑专属时空场对建模局部运动差异至关重要。

---

### 训练损失函数

总训练目标由三部分加权组合：

$$L = (1 - \lambda_{\mathrm{SSIM}}) L_1 + \lambda_{\mathrm{SSIM}} L_{\mathrm{SSIM}} + \lambda_v L_v$$

其中 $L_1$ 为像素级 L1 损失，$L_{\mathrm{SSIM}}$ 为结构相似性损失。轻量级体积正则化项 $L_v$ 用于促进时域高斯的紧凑性，对每个活跃时域高斯的尺度求积并求和：

$$L_v = \sum_{i=1}^{M} \mathrm{Prod}(s_t^i)$$

该正则化项抑制高斯过度膨胀，有助于提升渲染质量和训练稳定性。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_13746/figures/003_Figure_3.jpg]]
*Figure 3: (a)Static features*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_13746/figures/004_Figure_4.jpg]]
*Figure 4: Geometry-aware deduplication. (a) The points from the Reference Clip is converted into a spherical coverage field: for each point p, a sphere s is centered at p with radius set to the mean distance to its three nearest neighbors (computed via KNN). (b) Given the field and the Source Clip candidate anchors, residual anchors are selected based on their signed distance to the field surface. q1 (red box)*



## 实验与关键发现

### 主要结果

ClipGStream在多个公开基准和长序列场景上均取得了最优或极具竞争力的重建质量。

**Long 360数据集（1400帧）**。如Table 1所示，ClipGStream在所有指标上均显著优于现有方法。PSNR达到24.54，相较帧流式基线**3DGStream**（Sun et al., CVPR 2024）的21.94提升了2.60 dB；DSSIM1降至0.079，优于静态上限方法**2DGS**（0.085）。这验证了Clip-Stream框架在同时处理长序列和大运动幅度方面的优势——帧流式方法受累积误差困扰，剪辑式方法则受限于内存和序列长度。

**VRU (GZ)数据集**。如Table 2所示，ClipGStream在复杂动态交互场景下取得PSNR 30.67、SSIM 0.946、LPIPS 0.137，全面超越**4DGaussian**（Wu et al., CVPR 2024）和**LocalDyGS**（Wu et al., ArXiv 2025）等剪辑式方法。静态区域（如球场地面）和动态区域（如运动员）均呈现更清晰的渲染结果（Figure 6）。

**Neural 3D Video数据集**。如Table 3所示，ClipGStream在五个300帧场景上取得PSNR 32.53、DSSIM1 0.024、DSSIM2 0.012，同时推理速度达106 FPS，训练仅需0.5小时，模型大小98 MB，在精度-效率权衡上表现突出。

**N3DV flame salmon场景（1200帧）**。如Table 4所示，ClipGStream以PSNR 29.40、SSIM 0.917、LPIPS 0.144超越先前最优方法**Grid4D**（Jiawei et al., NeurIPS 2024）和**LocalDyGS**，尤其在狗的面部和火焰等精细动态区域保留了更多细节（Figure 7）。

### 消融实验

消融实验系统性地验证了ClipGStream各核心组件的贡献。

**解码器继承（DI）与残差锚点补偿（RAC）**。如Table 5所示，移除DI模块导致PSNR从24.54降至24.34；移除RAC模块则使PSNR进一步降至23.62。Figure 8的定性结果表明，不继承解码器会导致渲染图像出现明显模糊。更关键的是，Figure 5的跨剪辑残差热力图显示：移除RAC或锚点继承模块（AI）后，静态区域出现强烈的残差响应（即跨剪辑闪烁），而同时启用两者则显著抑制闪烁，保证了平滑的剪辑过渡。

**训练策略**。如Table 6所示，独立训练各剪辑（无继承）PSNR仅为21.85，远低于完整方法；共享时空场（STF）使PSNR降至23.11，验证了为每个剪辑分配独立STF以捕捉局部运动差异的必要性。这从因果机制上印证了核心设计：继承冻结的静态组件保证了全局一致性，而独立STF和残差锚点补偿则赋予各剪辑足够的灵活性来建模大规模位移。

### 失败模式与局限性

尽管ClipGStream在多个基准上表现优异，但其设计存在以下边界条件：

1. **COLMAP依赖**：方法需要COLMAP为每个剪辑生成初始点云以构建锚点集。在极低纹理或运动模糊严重的场景中，COLMAP的重建质量可能不足以支撑残差锚点的有效去重和补偿，从而导致几何初始化失败。此点需要手动验证具体退化程度。

2. **静态背景假设**：跨剪辑继承策略假设背景基本不变（继承并冻结静态特征）。当摄像机视角发生大幅变动或背景出现显著变化时，继承的静态特征可能不再适用，需要额外的自适应机制。论文未展示此类场景的实验结果。

3. **超长序列的存储与训练开销**：虽然Clip-Stream框架在原理上可扩展至任意长度，但论文未讨论数万帧级别超长序列下的存储开销（每个剪辑需保存独立STF参数）和训练时间优化。实时流式处理的可行性仍是一个开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_13746/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative results on Long 360 (1,400 frames; extreme motion amplitudes and long-sequence challenges) and VRU GZ [31] (complex dynamic interactions). Compared to 4DGaussian [29] and LocalDyGS [31], our method produces sharper renderings in both dynamic regions (e.g., athletes) and static areas (e.g., court floor), with more stable and temporally coherent reconstructions. Additional results are provided in the supplementary video and materials*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_13746/figures/011_Figure_7.jpg]]
*Figure 7: Qualitative results of flame salmon from the N3DV dataset [14], a fine-scale motion sequence. Our method outperforms SOTA approaches (Grid4D [42], LocalDyGS [31]) by better preserving details in dynamic regions such as the dog’s face and flames*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_13746/figures/013_Table_5.jpg]]
*Table 5: Ablation on Decoder Inheritance Module (DI) and Residual Anchors Compensation Module (RAC) in Long 360*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_13746/figures/014_Table_6.jpg]]
*Table 6: Experiments on two clip training strategies. Our method achieves superior objective quality. Experiments are carried out on the Long 360 dataset*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_13746/figures/015_Figure_8.jpg]]
*Figure 8: The Ablation study on decoder inheritance. (a) Without inheriting the decoder, the rendered image exhibits noticeable blurriness. In contrast, employing decoder inheritance yields clear details, as visualized in (b)*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_13746/figures/005_Figure_5.jpg]]
*Figure 5: The ablation study on the Residual Anchors Compensation Module (RAC) and the Anchors Inheritance Module (AI). As seen from the residual heatmaps between adjacent clips, removing either module leads to strong responses in static regions as shown in (a)(b)(c), while enabling them, as illustrated in (d), significantly suppresses flicker and preserves smooth clip transitions, which demonstrates that both components play essential roles in maintaining inter clip stability*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_13746/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison on Long 360 , which contains 1400 frames. Static methods are tested on frame 0*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_13746/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison on VRU (GZ) dataset [39]. Static methods are evaluated on frame 0 only, serving as an upperbound reference for dynamic reconstruction*



## 定位与知识库关联

### 1. 问题定位：帧流式与剪辑式方法的双重困境

ClipGStream 瞄准的是多视角动态场景重建中的一个根本性矛盾：**可扩展性与时间一致性之间的权衡**。现有方法可归为两类范式，各自存在难以调和的瓶颈：

- **帧流式方法（Frame-Stream）**：以 **3DGStream**（Sun et al., CVPR 2024）为代表，逐帧增量式更新场景表示。其优势在于序列长度理论上不受限，但帧间误差会逐步累积，导致长序列末端的渲染质量退化，且难以处理大幅度的帧间运动。
- **剪辑式方法（Clip）**：包括 **4DGaussian**（Wu et al., CVPR 2024）、**SpaceTimeGS**（Li et al., CVPR 2024）、**LocalDyGS**（Wu et al., ArXiv 2025）和 **Grid4D**（Jiawei et al., NeurIPS 2024）等，将视频分割为固定长度的剪辑独立优化。剪辑内部具有较好的局部时间一致性，但剪辑之间缺乏显式约束，切换时产生视觉闪烁；同时，每个剪辑需存储完整的模型参数，内存开销随序列长度线性增长，限制了可处理的序列规模。

此外，两类方法在**大规模运动**场景下均表现不佳——帧流式方法因增量更新的局限性难以补偿剧烈位移，剪辑式方法则因各剪辑独立初始化而缺乏跨剪辑的运动连续性。

### 2. 方法锚点：Clip-Stream 范式的核心创新

ClipGStream 提出了**首个 Clip-Stream 动态重建框架**，通过“剪辑内独立建模 + 剪辑间冻结继承”的双阶段策略，同时解决了大规模运动建模和长序列时间一致性问题。其关键设计可拆解为以下四个“变更槽”（changed slots）：

| 设计维度 | 基线方法 | ClipGStream 方案 | 证据锚点 |
|---------|---------|-----------------|---------|
| **跨剪辑一致性策略** | 各剪辑独立优化，无显式约束 | 继承并冻结参考剪辑的锚点、静态特征和解码器 | Sec. 3.2.2 |
| **锚点集构建** | 直接从 COLMAP 重建点云初始化锚点 | 继承参考剪辑锚点，通过几何感知去重添加残差锚点 | Eq. (6), Figure 4 |
| **时空场设计** | 共享单个时空场 | 每个剪辑分配独立的时空场 STF_n | Sec. 3.2.1, Tab. 6 |
| **静态特征处理** | 静态特征重新学习或无分解 | 继承参考剪辑的静态特征并冻结，仅学习新增残差静态特征 | Eq. (9), Figure 3 |

**核心洞察**：将视频分割为参考剪辑和多个源剪辑，在剪辑内部采用独立时空场和残差锚点补偿以实现局部运动建模，在剪辑间通过继承冻结的静态组件来维持全局时间一致性。这一解耦设计使得模型既能灵活捕捉各剪辑内的复杂动态，又能在剪辑边界保持静态区域的像素级稳定。

### 3. 流水线模块与功能分工

ClipGStream 的训练流程由四个功能模块构成：

1. **Reference Clip Training**（参考剪辑训练）：使用融合点云初始化锚点，通过共享解码器同时学习静态和动态特征，建立基础时空表示（Sec. 3.2.1, Figure 2）。
2. **Source Clip Training (Intra-clip)**（源剪辑内部训练）：继承参考剪辑的锚点与静态特征，通过残差锚点补偿新增/位移结构，利用独立时空场建模局部运动（Sec. 3.2.1, Eq. (6)-(10)）。
3. **Inter-clip Inheritance**（跨剪辑继承）：跨剪辑复用并冻结解码器、锚点及静态特征，确保静态区域与几何外观解码的一致性（Sec. 3.2.2, Figure 3）。
4. **Geometry-Aware Deduplication**（几何感知去重）：基于球形覆盖场和 SDF 过滤重复锚点，仅保留残差锚点（Sec. 3.2.1, Figure 4）。

### 4. 适用边界与局限

尽管 ClipGStream 在多个基准上取得了最优性能，其设计仍存在若干适用性边界：

- **依赖 COLMAP 初始化的鲁棒性**：方法依赖 COLMAP 为每个剪辑生成初始点云（用于锚点构建和残差锚点补偿），在极低纹理或运动模糊严重的场景下，COLMAP 的重建质量可能退化，进而影响锚点初始化的准确性和几何感知去重的有效性。
- **静态背景假设**：跨剪辑继承策略的核心前提是静态特征（背景信息）在序列中基本不变。当背景发生剧烈变化时（如自由摄像机路径下的大幅视角变动），继承的静态特征可能无法覆盖新出现的背景区域，需要额外策略或自适应调整。
- **超长序列的存储与效率**：论文尚未讨论实时推演下的内存与训练时间优化，以及极端长序列（如数万帧）下参考剪辑静态特征的持续有效性和存储开销问题。

### 5. 开放问题

基于当前方法的局限，以下开放问题值得后续探索：

1. **超长序列的可扩展性**：扩展到数万帧时，参考剪辑的静态特征能否持续有效？是否需要引入多级参考剪辑或层次化继承策略？
2. **自由摄像机路径**：当前方法假设多视角输入来自固定或可控的摄像机阵列，能否处理自由摄像机路径下的动态场景重建？
3. **实时流式处理**：如何进一步减少每个剪辑的训练时间，以实现接近实时的流式处理？是否可以通过预训练参考剪辑或轻量化时空场设计来加速？
4. **自适应继承策略**：对于背景发生显著变化的场景（如舞台灯光变化、户外天气变化），静态继承策略是否需要引入变化检测机制或自适应权重调整？
5. **与基础模型的结合**：是否可以利用预训练视觉基础模型（如深度估计、光流、语义分割）来增强 COLMAP 初始化或指导残差锚点的选择？

> **注意**：以上开放问题基于论文自身局限性的逻辑延伸，部分方向（如自由摄像机路径、自适应继承）尚未在论文中讨论，需结合后续研究进行验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/ClipGStream_Clip_Stream_Gaussian_Splatting_for_Any_Length_and_Any_Motion_Multi_View_Dynamic_Scene_Reconstruction.pdf]]
