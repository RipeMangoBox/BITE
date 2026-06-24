---
title: Spectral-Geometric Neural Fields for Pose-Free LiDAR View Synthesis
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Spectral_Geometric_Neural_Fields_for_Pose_Free_LiDAR_View_Synthesis.pdf
project_link: null
code_link: null
aliases:
- SN
- SGNFPFLVS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 融合等距不变谱嵌入与局部几何编码的混合表示可以恢复连续几何；基于混合特征兼容性的置信度感知图优化实现全局位姿对齐；跨帧对抗学习增强重建一致性。
primary_logic: 谱嵌入携带全局结构先验，能够弥补几何插值在无观测区域的不足；通过特征匹配构建非相邻帧约束比仅依赖时间相邻帧的成对对齐能获得更准确的全局轨迹。
claims:
- SG-NLF在nuScenes数据集上相比GeoNLF将Chamfer距离降低35.8%，绝对轨迹误差降低68.8%。
- "混合表示（几何编码+谱嵌入）相比纯几何编码显著提升重建质量（CD: 0.155 vs 0.241）。"
- 移除全局位姿优化（GP）会导致ATE从0.071 m升至0.798 m。
- KITTI-360 (low-freq) 上 CD (↓) = 0.1695
---

# Spectral-Geometric Neural Fields for Pose-Free LiDAR View Synthesis

> [!tip] 核心洞察
> 谱嵌入携带全局结构先验，能够弥补几何插值在无观测区域的不足；通过特征匹配构建非相邻帧约束比仅依赖时间相邻帧的成对对齐能获得更准确的全局轨迹。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向无位姿LiDAR视图合成的谱-几何神经场 |
| 英文题名 | Spectral-Geometric Neural Fields for Pose-Free LiDAR View Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.12903) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | SG-NLF |
| Dataset | KITTI-360, nuScenes |

> [!tip] 效果简介
> - KITTI-360 (low-freq) 上，CD (↓) 0.1695 vs 0.2363 (GeoNLF) (-28.3%)；Depth PSNR (↑) 28.7068 vs 25.2758 (GeoNLF) (+13.6%)；Intensity PSNR (↑) 19.2652 vs 16.5813 (GeoNLF) (+16.2%)。
> - nuScenes (low-freq) 上，CD (↓) 0.1545 vs 0.2408 (GeoNLF) (-35.8%)；ATE (m) (↓) 0.071 vs 0.228 (GeoNLF) (-68.8%)。
> - KITTI-360 (standard-freq) 上，Depth PSNR (↑) 32.7245 vs 30.9983 (GeoNLF) (+5.6%)。

## 概述

无位姿（pose-free）LiDAR新视角合成面临双重瓶颈：**LiDAR点云的稀疏性与无纹理特性**使得基于几何插值的神经场难以重建连续几何表面，而现有无位姿方法依赖的成对对齐策略难以保证全局位姿精度。针对这一难题，本文提出**SG-NLF**（Spectral-Geometric Neural Fields），一种融合谱-几何信息的神经场框架，同时实现高质量视图合成与精确位姿估计。

SG-NLF的核心洞察在于：**谱嵌入携带全局结构先验**，能够弥补几何插值在无观测区域的不足；通过特征匹配构建非相邻帧约束，比仅依赖时间相邻帧的成对对齐能获得更准确的全局轨迹。方法层面，SG-NLF设计了三个关键模块：**混合谱-几何表示**，将多分辨率哈希网格编码与连续谱嵌入融合，恢复平滑连续的几何结构；**置信度感知的全局位姿优化图**，基于混合特征兼容性建立跨帧约束；**跨帧对抗一致性模块**，利用多尺度PatchGAN判别器增强重建的几何一致性。

实验结果表明，SG-NLF在nuScenes数据集上相比先前最优的无位姿方法**GeoNLF**（Xue et al., NeurIPS 2024），Chamfer距离降低35.8%，绝对轨迹误差（ATE）降低68.8%；在KITTI-360低频场景下，深度PSNR提升13.6%，强度PSNR提升16.2%。消融实验进一步验证了混合表示和全局位姿优化的关键作用：移除全局位姿优化导致ATE从0.071 m飙升至0.798 m，而纯几何编码替换混合表示后CD从0.155升至0.241。

## 背景与动机

### 问题背景：无位姿LiDAR视图合成的双重挑战

自动驾驶与机器人系统依赖LiDAR传感器获取精确的三维环境感知，但真实采集过程常面临传感器位姿不准或完全缺失的问题。无位姿LiDAR视图合成（pose-free LiDAR novel view synthesis, NVS）旨在仅从多帧LiDAR点云序列出发，同时恢复场景的连续三维表示与每帧的全局位姿，从而支持任意新视角的深度图与强度图渲染。

这一任务面临两重根本性困难。**第一，LiDAR点云的稀疏性与无纹理特性**使得传统基于几何插值的神经场方法难以重建连续、完整的几何表面。如图Figure 2所示，现有方法在无观测区域会产生显著的“几何空洞”（geometric holes），这些空洞直接导致合成视图质量严重退化。**第二，位姿估计的全局一致性难以保证**——现有无位姿方法普遍依赖相邻帧之间的成对对齐约束，缺乏长程几何约束，使得累积漂移无法有效消除，全局轨迹精度受限。

### 现有方法缺口

当前LiDAR NVS方法可大致分为两类。**位姿依赖方法**如**LiDARsim**（Manivasagam et al., CVPR 2020）和**PCGen**（Li et al., arXiv 2022）需要真实位姿作为输入，无法处理位姿未知的场景。**无位姿方法**则尝试联合优化重建与位姿，代表工作包括：

- **NeRF-based方法**：将BARF（Lin et al., ICCV 2021）、HASH（Heo et al., ICML 2023）、GeoTransformer（Qin et al., CVPR 2022）等位姿优化策略与LiDAR-NeRF（Tao et al., ACM MM 2024）结合，形成BARF-LN、HASH-LN、GeoTrans-LN。但这些方法的位姿优化仍局限于相邻帧约束，且NeRF表示本身对稀疏LiDAR观测的几何重建能力有限。
- **GeoNLF**（Xue et al., NeurIPS 2024）：专门针对无位姿LiDAR NVS设计，采用多分辨率哈希网格进行几何编码，并通过成对对齐进行位姿优化。然而，其纯几何表示在无观测区域无法提供有效的几何先验，成对对齐策略也难以保证全局位姿精度。

上述方法的共同缺口在于：**缺乏一种能够同时提供全局结构先验以填补几何空洞、并建立长程位姿约束以消除累积漂移的统一框架**。

### 核心动机与思路

本文的核心洞察是：**谱嵌入（spectral embedding）携带的等距不变全局结构信息，能够弥补纯几何编码在无观测区域的先天不足；而基于特征匹配构建的非相邻帧约束，比仅依赖时间相邻帧的成对对齐能获得更准确的全局轨迹。**

基于此，我们提出**SG-NLF**（Spectral-Geometric Neural Fields），通过以下三个关键设计突破现有瓶颈：

1. **混合谱-几何表示**：将离散几何编码与连续谱嵌入融合，使场景表示既保留局部几何细节，又具备全局结构先验，从而在无观测区域也能恢复连续几何。
2. **置信度感知图优化**：基于混合特征兼容性构建包含非相邻帧约束的位姿图，以空间一致性为边权重进行全局位姿优化，从根本上抑制累积漂移。
3. **跨帧对抗一致性**：引入多尺度PatchGAN判别器对合成深度图进行跨帧一致性监督，进一步增强重建质量。

实验表明，SG-NLF在nuScenes数据集上将Chamfer距离降低35.8%，绝对轨迹误差降低68.8%（相对于GeoNLF），在KITTI-360数据集上同样取得显著提升，验证了上述设计思路的有效性。

## 核心创新

SG-NLF 的核心创新在于针对无位姿 LiDAR 视图合成中“几何空洞”与“全局位姿漂移”两大瓶颈，提出了三个紧密耦合的 **changed slots**，形成“表示-位姿-一致性”的联合优化闭环。

### 1. 混合谱-几何表示：从离散插值到连续几何重建

**基线瓶颈**：现有方法（如 GeoNLF）依赖多分辨率哈希网格编码（**HASH**，Heo et al., ICML 2023）提取纯几何特征，但 LiDAR 点云的稀疏性与无纹理特性导致基于几何插值的神经场在无观测区域无法重建连续表面，产生严重的几何空洞（Figure 2 中白色区域）。这种空洞直接导致合成视图的质量退化。

**创新机制**：SG-NLF 将离散几何编码与连续谱嵌入融合为混合表示（Hybrid Spectral-Geometric Representation）。谱嵌入通过可微分方式优化 MLP 以逼近 Laplace-Beltrami 算子（LBO）的前 $K$ 个特征函数，这些特征函数天然携带几何表面的全局结构先验——等距不变性使其能够“感知”曲面的大尺度拓扑与连通性，从而弥补纯几何编码在无观测区域的插值盲区。

**因果链条**：谱嵌入提供全局几何骨架 → 混合特征在渲染时同时编码局部细节（几何编码）与全局结构（谱嵌入）→ NeRF 渲染网络从连续谱特征中恢复缺失表面 → 几何空洞被填补，合成深度图更连续。

**证据强度**：消融实验（Table 5）直接验证了这一因果逻辑——仅使用几何编码（w/o SE）时 CD 为 0.241，而混合表示将 CD 降至 0.155；仅使用谱嵌入（w/o GE）时 CD 升至 0.181，证明两者互补且几何编码的局部细节贡献不可替代。

### 2. 置信度感知图优化：从成对对齐到全局位姿约束

**基线瓶颈**：GeoNLF 等无位姿方法的位姿优化仅依赖相邻帧的成对对齐约束，这种局部策略无法消除累积漂移，导致全局轨迹误差随序列长度增长而发散。

**创新机制**：SG-NLF 构建置信度感知图（Confidence-Aware Pose Graph Optimizer），其边集不仅包含时序相邻帧，还通过混合特征兼容性动态引入非相邻帧约束。具体而言，对于任意帧对 $(i, j)$，首先计算粗粒度互最近邻匹配集 $\mathcal{M}_c^{ij}$，再通过精细匹配 $\mathcal{M}_f^{ij}$ 计算特征余弦相似度的均值作为边兼容性得分 $E^{ij}$（Eq. 10）。仅当 $E^{ij}$ 超过阈值时，该非相邻边才被纳入位姿图。每条边的权重 $\alpha^{ij}$ 由空间一致性 $P_{mn}$ 决定，使得高质量匹配对图优化的贡献更大。

**因果链条**：混合特征提供更鲁棒的跨帧匹配信号 → 非相邻帧约束形成闭环 → 图优化同时考虑局部平滑与全局一致性 → 累积漂移被有效抑制。

**证据强度**：移除全局位姿优化（w/o GP）导致 ATE 从 0.071 m 飙升至 0.798 m（Table 6），增幅超过 10 倍，直接证明图优化是位姿精度的决定性组件。在 nuScenes 上，SG-NLF 相比 GeoNLF 将 ATE 降低 68.8%（Table 4）。

### 3. 跨帧对抗一致性：从单帧监督到序列级几何约束

**基线瓶颈**：GeoNLF 仅使用单帧像素级损失（如深度 L1/L2），缺乏对相邻帧间几何一致性的显式建模，导致合成序列出现帧间抖动与伪影。

**创新机制**：SG-NLF 引入跨帧对抗模块（Cross-Frame Adversarial Module），采用多尺度 PatchGAN 判别器 $\Phi$ 对合成深度图进行真伪判别。判别器输入为相邻帧的合成深度图拼接，通过 hinge 损失（Eq. 14）迫使生成器产生跨帧几何一致的深度序列。与传统的单帧判别不同，PatchGAN 的多尺度结构能够捕获从局部纹理到全局结构的序列级不一致性。

**因果链条**：判别器评估跨帧深度图的对齐质量 → 对抗梯度反向传播至渲染网络 → 生成器被迫学习帧间一致的几何表示 → 合成序列的时间平滑性提升。

**证据强度**：移除跨帧一致性损失（w/o CFC）使 CD 从 0.155 升至 0.182，深度 PSNR 从 28.409 降至 26.597（Table 6），验证了对抗监督对重建质量的独立贡献。

### 三个 Changed Slots 的协同关系

上述三个创新并非孤立组件，而是形成正向反馈循环：混合表示提供的谱特征增强了跨帧匹配的鲁棒性（服务于图优化），图优化获得的精确全局位姿又为跨帧对抗提供了正确的帧间对应关系，而对抗一致性进一步约束渲染网络学习更稳定的混合表示。这一协同机制解释了为何 SG-NLF 在重建质量（CD 降低 35.8%）与位姿精度（ATE 降低 68.8%）上同时取得大幅提升。

## 整体框架

SG-NLF 是一个面向无位姿 LiDAR 新视图合成的统一框架，其核心设计目标是同时解决**高质量视图合成**与**精确全局位姿估计**两个相互耦合的问题。如图 3 所示，框架由四个关键模块构成，形成一条从多帧 LiDAR 输入到合成视图与优化位姿的完整流水线。

### 输入与预处理

给定一个多帧 LiDAR 序列 $\{\mathcal{P}_i\}_{i=1}^{M}$，每帧点云包含三维坐标、强度值和射线丢失（ray-drop）信息。初始阶段，系统为每帧分配一个可学习的位姿参数 $\xi_i \in \mathfrak{se}(3)$，通过指数映射 $\mathbf{T}_i = \exp(\xi_i^{\wedge})$ 将李代数向量恢复为 $\mathrm{SE}(3)$ 变换矩阵，该位姿在训练过程中与网络参数联合优化。

### 混合谱-几何表示（Hybrid Spectral-Geometric Representation）

框架的第一个核心模块是**混合表示**，它将两种互补的特征类型融合：

- **离散几何编码**：基于多分辨率哈希网格编码（Müller et al., 2022）从点云坐标中提取局部几何特征，捕获精细的表面细节。
- **连续谱嵌入**：通过可微分方式优化一组 MLP 来近似 Laplace-Beltrami 算子的前 $K$ 个本征函数，获得携带全局结构先验的等距不变谱嵌入。这些谱嵌入能够在无观测区域提供连续的几何先验，弥补纯几何插值的不足。

融合后的混合特征 $\mathbf{f}$ 同时服务于后续的渲染网络和图构建模块。

### NeRF 渲染网络

渲染网络以混合特征为输入，沿射线采样点预测体积密度 $\sigma$，并通过标准体积渲染公式计算深度、强度和射线丢失概率：

$$\hat{\mathcal{D}}(\mathbf{r}) = \sum_{i=1}^{N} T_i \left(1 - e^{-\sigma_i \delta_i}\right) z_i, \quad T_i = \exp(-\sum_{j=1}^{i-1} \sigma_j \delta_j)$$

渲染输出直接用于单帧监督损失的计算。

### 置信度感知位姿图优化器（Confidence-Aware Pose Graph Optimizer）

该模块利用混合特征构建一个**置信度感知图**，实现全局位姿优化。与传统方法仅依赖相邻帧成对对齐不同，SG-NLF 的边集 $\mathcal{E}$ 同时包含：

- **顺序边**：时间相邻帧之间的约束。
- **非相邻边**：基于特征兼容性筛选的高置信度远距离帧对。

边的兼容性通过精细匹配特征对的平均余弦相似度计算：

$$E^{ij} = \frac{1}{|\mathcal{M}_f^{ij}|} \sum_{(m,n) \in \mathcal{M}_f^{ij}} \frac{\mathbf{f}_m^{i} \cdot \mathbf{f}_n^{j}}{\lVert\mathbf{f}_m^{i}\rVert_2 \lVert\mathbf{f}_n^{j}\rVert_2}$$

仅当兼容性分数超过阈值时，边才被纳入图结构。位姿图损失以空间一致性为权重，对图中所有边施加加权 Chamfer 距离约束：

$$\mathcal{L}_{\mathrm{graph}} = \sum_{(i,j) \in \mathcal{E}} \alpha^{ij} \cdot \mathcal{L}_{\mathrm{cd}}^{ij}$$

其中 $\alpha^{ij}$ 为边 $(i,j)$ 的平均空间一致性权重。这一设计通过非相邻帧约束有效抑制了长序列中的累积漂移。

### 跨帧对抗模块（Cross-Frame Adversarial Module）

为进一步增强跨帧几何一致性，框架引入了一个多尺度 PatchGAN 判别器。该判别器以成对深度图（真实深度图 $\mathbf{I}_{\mathrm{real}}$ 与合成深度图 $\mathbf{I}_{\mathrm{fake}}$）为输入，通过 hinge 对抗损失评估跨帧对齐质量：

$$\mathcal{L}_{\mathrm{con}} = \max(0, 1 - \Phi(\mathbf{I}_{\mathrm{real}})) + \max(0, 1 + \Phi(\mathbf{I}_{\mathrm{fake}}))$$

这一对抗监督信号驱动渲染网络生成在相邻帧之间几何一致的深度图，弥补单帧像素级损失在跨帧约束上的不足。

### 总损失与端到端训练

框架的总损失由以下分量加权组合：单帧深度与强度的重建损失、谱嵌入优化损失 $\mathcal{L}_{\mathrm{spe}}$（包含 Rayleigh 商残差、归一化损失和正交损失）、位姿图损失 $\mathcal{L}_{\mathrm{graph}}$，以及跨帧一致性对抗损失 $\mathcal{L}_{\mathrm{con}}$。所有模块（混合表示、渲染网络、位姿参数、判别器）在训练中端到端联合优化，使视图合成质量与位姿估计精度相互促进。

### 补充图表

![[assets/figures/papers/paper_list_l2598_https_arxiv_org_abs_2603_12903/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the SG-NLF. Given multi-view LiDAR sequences*

## 核心模块与公式推导

### 3.1 神经渲染基础

SG-NLF建立在神经辐射场（NeRF）的体积渲染框架之上。给定一条射线 $\mathbf{r}(t) = \mathbf{o} + t\mathbf{d}$，沿射线采样 $N$ 个点，通过神经网络预测各点的体积密度 $\sigma_i$，累积透射率 $T_i$ 和深度值 $z_i$ 渲染深度图。深度渲染公式为：

$$\hat{\mathcal{D}}(\mathbf{r}) = \sum_{i=1}^{N} T_i \left(1 - e^{-\sigma_i \delta_i}\right) z_i, \quad T_i = \exp(-\sum_{j=1}^{i-1} \sigma_j \delta_j)$$

其中 $\delta_i$ 为相邻采样点间距。类似地，强度值 $\hat{\mathcal{I}}(\mathbf{r})$ 和射线丢失概率 $\hat{\mathcal{O}}(\mathbf{r})$ 也通过体积渲染获得。位姿参数化采用李代数表示，通过指数映射将6维李代数向量 $\xi \in \mathfrak{se}(3)$ 映射到SE(3)变换矩阵：

$$\mathbf{T} = \exp(\xi^{\wedge}) = \sum_{n=0}^{\infty} \frac{1}{n!} (\xi^{\wedge})^n = \begin{bmatrix} \mathbf{R} & \mathbf{J}\rho \\ \mathbf{0}^{\top} & 1 \end{bmatrix}$$

### 3.2 混合谱-几何表示

SG-NLF的核心创新在于将离散几何编码与连续谱嵌入融合为混合表示。

**几何编码**：基于多分辨率哈希网格编码提取离散几何特征。对于3D空间点 $\mathbf{x}$，通过哈希查找获得多分辨率特征向量，经小型MLP处理得到几何编码 $\mathbf{f}_g(\mathbf{x})$。该编码能够捕捉局部几何细节，但在无观测区域缺乏全局结构先验。

**谱嵌入**：为弥补几何编码的不足，SG-NLF引入连续谱嵌入。从LiDAR点云拟合的隐式神经表面出发，通过可微分方式优化MLP网络 $\Psi_k(\mathbf{x})$ 来近似前 $K$ 个Laplace-Beltrami算子（LBO）特征函数。谱嵌入携带等距不变全局结构信息，能够在无观测区域提供平滑几何先验。

谱嵌入的优化目标由三部分组成。首先，Rayleigh商残差项 $\mathcal{R}_{\Sigma}(\Psi_i)$ 衡量 $\Psi_i$ 对LBO特征函数的近似程度：

$$\mathcal{R}_{\Sigma}(\Psi_i) = \frac{\int_{\Sigma} \|\nabla_{\Sigma} \Psi_i\|^2 dA}{\int_{\Sigma} \Psi_i^2 dA}$$

其中曲面梯度通过将3D空间梯度投影到切平面计算：

$$\nabla_{\Sigma} \Psi(\hat{\mathbf{x}}_i) = \nabla \Psi(\hat{\mathbf{x}}_i) - \langle \nabla \Psi(\hat{\mathbf{x}}_i), \mathbf{n}(\hat{\mathbf{x}}_i) \rangle \mathbf{n}(\hat{\mathbf{x}}_i)$$

局部面积元由第一基本形式系数计算：$dA_i = \sqrt{E_i \cdot G_i - F_i^2}$。

其次，归一化损失 $\mathcal{L}_{\mathrm{norm}}$ 约束特征函数具有单位范数；正交损失 $\mathcal{L}_{\mathrm{ortho}}$ 确保不同特征函数之间相互正交。总谱损失为：

$$\mathcal{L}_{\mathrm{spe}} = \sum_{i=1}^{K} \mathcal{R}_{\Sigma}(\Psi_{i}) + \lambda_{n} \mathcal{L}_{\mathrm{norm}} + \lambda_{o} \mathcal{L}_{\mathrm{ortho}}$$

最终，混合特征通过拼接几何编码与谱嵌入获得：$\mathbf{f}(\mathbf{x}) = [\mathbf{f}_g(\mathbf{x}), \Psi_1(\mathbf{x}), ..., \Psi_K(\mathbf{x})]$。该混合表示同时具备局部几何精度与全局结构连续性。

### 3.3 置信度感知位姿图优化

SG-NLF将位姿估计转化为图优化问题。图节点对应各帧的位姿参数 $\xi_i$，边的构建基于混合特征兼容性。

**特征匹配与图构建**：对于帧对 $(i, j)$，首先通过特征空间中的相互最近邻搜索建立粗对应集合：

$$\mathcal{M}_c^{ij} = \left\{ (m, n) \mid \|\mathbf{f}_m^{i} - \mathbf{f}_n^{j}\|_2 = \min_{n'} \|\mathbf{f}_m^{i} - \mathbf{f}_{n'}^{j}\|_2 = \min_{m'} \|\mathbf{f}_{m'}^{i} - \mathbf{f}_n^{j}\|_2 \right\}$$

经几何一致性过滤后获得精细匹配集 $\mathcal{M}_f^{ij}$。边的兼容性得分定义为精细匹配特征对之间的平均余弦相似度：

$$E^{ij} = \frac{1}{|\mathcal{M}_f^{ij}|} \sum_{(m,n) \in \mathcal{M}_f^{ij}} \frac{\mathbf{f}_m^{i} \cdot \mathbf{f}_n^{j}}{\lVert\mathbf{f}_m^{i}\rVert_2 \lVert\mathbf{f}_n^{j}\rVert_2}$$

边集 $\mathcal{E}$ 不仅包含时序相邻帧，还纳入兼容性得分高于阈值的非相邻帧对，从而建立长程约束。

**图优化损失**：每条边 $(i, j)$ 关联一个权重 $\alpha^{ij}$，由精细匹配点的平均空间一致性 $P_{mn}$ 计算：

$$\alpha^{ij} = \frac{1}{|\mathcal{M}_f^{ij}|} \sum_{(m,n) \in \mathcal{M}_f^{ij}} P_{mn}$$

位姿图损失为加权Chamfer距离：

$$\mathcal{L}_{\mathrm{graph}} = \sum_{(i,j) \in \mathcal{E}} \alpha^{ij} \cdot \mathcal{L}_{\mathrm{cd}}^{ij}$$

其中 $\mathcal{L}_{\mathrm{cd}}^{ij}$ 衡量帧 $i$ 点云经位姿变换后与帧 $j$ 点云的双向Chamfer距离。通过联合优化所有节点的位姿参数，SG-NLF实现全局一致的轨迹估计。

### 3.4 跨帧对抗一致性

为进一步增强合成视图的跨帧几何一致性，SG-NLF引入对抗学习策略。采用多尺度PatchGAN判别器 $\Phi$，以成对深度图作为输入，区分真实深度图对 $\mathbf{I}_{\mathrm{real}}$ 与合成深度图对 $\mathbf{I}_{\mathrm{fake}}$。对抗一致性损失采用hinge形式：

$$\mathcal{L}_{\mathrm{con}} = \max(0, 1 - \Phi(\mathbf{I}_{\mathrm{real}})) + \max(0, 1 + \Phi(\mathbf{I}_{\mathrm{fake}}))$$

该损失促使生成网络产生在局部块级别上具有跨帧几何一致性的深度图，有效抑制因位姿误差或表示不连续导致的伪影。

### 补充图表

![[assets/figures/papers/paper_list_l2598_https_arxiv_org_abs_2603_12903/figures/002_Figure_2.jpg]]
*Figure 2: Geometric Inconsistency [11, 39, 50]. The geometric hole mask is generated by comparing rendered opacity with ground truth LiDAR measurements. White regions in rectangular boxes (first row) highlight areas where these methods fail to reconstruct geometry. Comparisons between second and third rows further show these holes lead to poor-quality synthesized views*

## 实验与分析

### 核心定量结果

SG-NLF 在两个主流自动驾驶数据集 KITTI-360 和 nuScenes 上进行了全面评估，实验设置覆盖低频（10 帧稀疏采样）与标准频率两种场景，对比对象包括位姿依赖的 LiDAR 视图合成方法（**LiDARsim** (Manivasagam et al., CVPR 2020)、**PCGen** (Li et al., arXiv 2022)、**LiDAR4D** (Zheng et al., CVPR 2024)）以及无位姿方法（**BARF-LN**、**HASH-LN**、**GeoTrans-LN**、**GeoNLF** (Xue et al., NeurIPS 2024)）。其中非 LiDAR NVS 方法统一采用 LiDAR-NeRF 作为重建后端以保证公平性。

在 KITTI-360 低频场景下（Table 1），SG-NLF 在所有点云重建与视图合成指标上均取得最优。相比最强基线 GeoNLF，Chamfer Distance (CD) 从 0.2363 降至 **0.1695（↓28.3%）**，深度 PSNR 从 25.2758 提升至 **28.7068（↑13.6%）**，强度 PSNR 从 16.5813 提升至 **19.2652（↑16.2%）**。在 nuScenes 低频场景下（Table 2），CD 从 0.2408 降至 **0.1545（↓35.8%）**，F-score 从 0.8837 升至 0.9244，深度 PSNR 从 25.0581 升至 28.4094。

![[assets/figures/papers/paper_list_l2598_https_arxiv_org_abs_2603_12903/figures/004_Table_1.jpg]]
*Table 1: Comparisons with state-of-the-art methods on KITTI-360 [26] dataset with a low-frequency setting [50]. We compare our method with pose-dependent [20, 31, 55] and pose-free methods [10, 27, 35, 50]. For approaches not originally designed for LiDAR NVS [10, 27, 35], we follow GeoNLF [50] and adopt LiDAR-NeRF [39] for reconstruction. For pose-dependent methods, we employ ground-truth poses for synthesis. We color the best results as red and the second-best as orange*

![[assets/figures/papers/paper_list_l2598_https_arxiv_org_abs_2603_12903/figures/005_Table_2.jpg]]
*Table 2: Comparisons with state-of-the-art methods on nuScenes [4] dataset with a low-frequency setting [50]. We color the best results as red and the second-best as orange. The notations are consistent with the KITTI-360 [26] dataset in Table 1 above*

在 KITTI-360 标准频率场景下（Table 3），SG-NLF 同样保持竞争力，深度 PSNR 达到 **32.7245**，相比 GeoNLF 的 30.9983 提升 5.6%，且接近部分使用真实位姿的位姿依赖方法。

![[assets/figures/papers/paper_list_l2598_https_arxiv_org_abs_2603_12903/figures/007_Table_3.jpg]]
*Table 3: Comparisons on the KITTI-360 [26] dataset with standard-frequency setting [39]. We compare SG-NLF with state-of-the-art pose-dependent methods [11, 20, 31, 39, 55] and pose-free model [50]. We color the best results as red and the second-best as orange*

**位姿估计精度**是 SG-NLF 的另一核心优势。在 nuScenes 上（Table 4），SG-NLF 的绝对轨迹误差 (ATE) 仅为 **0.071 m**，而 GeoNLF 为 0.228 m（**↓68.8%**），相对旋转误差从 0.381°/m 降至 0.117°/m，相对平移误差从 1.226% 降至 0.384%。在 KITTI-360 上，ATE 从 0.063 m 降至 0.048 m。值得注意的是，SG-NLF 的位姿精度显著优于传统配准基线（如 ICP、FGR、GeoTransformer）和其他无位姿 NeRF 方法。Figure 5 通过将多帧点云按估计位姿拼合并按高度着色，直观展示了 SG-NLF 的全局对齐质量明显优于 GeoNLF 等方法，拼接场景中的鬼影和错位现象大幅减少。

### 消融实验与因果机制验证

为验证各模块的独立贡献，论文在 nuScenes 数据集上进行了系统消融（Table 5、Table 6）。

![[assets/figures/papers/paper_list_l2598_https_arxiv_org_abs_2603_12903/figures/011_Figure_6.jpg]]
*Figure 6: Qualitative comparison for hybrid representation*

![[assets/figures/papers/paper_list_l2598_https_arxiv_org_abs_2603_12903/figures/012_Table_5.jpg]]
*Table 5: Hybrid Representation Analysis. Ablation study of geometric encodings (GE) and spectral embeddings (SE) on nuScenes [4], with comparisons to GeoNLF [50]*

**混合表示的有效性**（Table 5）：完整模型（GE + SE）的 CD 为 0.155。当仅使用几何编码（w/o SE，即退化为 GeoNLF 的表示）时，CD 升至 0.241；当仅使用谱嵌入（w/o GE）时，CD 为 0.181。这表明几何编码提供了精确的局部结构信息，而谱嵌入携带的全局等距不变先验能有效填补无观测区域的几何空洞，二者互补。Figure 6 的定性对比进一步显示，移除谱嵌入后，重建点云在遮挡区域出现明显的几何断裂和缺失。

**全局位姿优化的关键性**（Table 6）：移除全局位姿优化模块（w/o GP）导致 ATE 从 0.071 m 急剧升至 **0.798 m**，增幅超过 10 倍。这验证了仅依赖相邻帧成对对齐（如 GeoNLF 的策略）会累积漂移误差，而基于混合特征兼容性构建的非相邻帧约束是获得准确全局轨迹的核心因果机制。

**跨帧一致性模块的贡献**（Table 6）：移除跨帧对抗损失（w/o CFC）使 CD 从 0.155 升至 0.182，深度 PSNR 从 28.409 降至 26.597。这表明多尺度 PatchGAN 判别器提供的跨帧几何一致性监督能有效抑制不同视角合成深度图之间的不连续和伪影。

### 定性分析与失败模式

Figure 4 展示了距离深度和强度重建的定性对比。在物体边缘和远距离区域，SG-NLF 恢复的深度图边界更清晰、强度纹理更锐利，而 GeoNLF 等方法在这些区域存在模糊和断裂。Figure 2 揭示了先前方法（如 LiDAR4D、LiDAR-NeRF、GeoNLF）中普遍存在的几何不一致问题——通过比较渲染不透明度与真实 LiDAR 测量可生成几何空洞掩码，这些空洞直接导致合成视图质量下降。SG-NLF 的谱嵌入通过提供连续全局几何先验，显著减少了此类空洞。

![[assets/figures/papers/paper_list_l2598_https_arxiv_org_abs_2603_12903/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparisons for LiDAR range depth and intensity reconstruction. Both pose-dependent [20, 55] and pose-free methods [50] are compared. Regions with obvious differences are highlighted in the rectangular boxes and arrows*

论文指出的主要局限在于：当前实现仅为 SG-NLF 的一种有效实例化，动态场景扩展和不同 LiDAR 传感器配置的适应性仍待探索。对于极端稀疏采样（如低于 5 帧）或大范围回环缺失的场景，谱嵌入的质量可能受限于点云密度，该边界条件下的性能需要手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l2598_https_arxiv_org_abs_2603_12903/figures/001_Figure_1.jpg]]
*Figure 1: (a) Reconstruction and synthesis quality. The X-axis shows Chamfer Distance (CD) for point cloud reconstruction on the low-frequency KITTI-360 dataset [26, 50]. The Y-axis shows RMSE for range depth and intensity synthesis. Circle area represents inference time. Lower CD and RMSE mean better reconstruction and synthesis. Our framework outperforms prior work by large margins. (b) Pose accuracy. The axis represents Absolute Trajectory Error (ATE) for pose estimation. Our SG-NLF demonstrates higher accuracy compared to existing NeRF-based models*

![[assets/figures/papers/paper_list_l2598_https_arxiv_org_abs_2603_12903/figures/008_Figure_5.jpg]]
*Figure 5: Visual comparisons for pose estimation. We transform input sequences into a unified scene using estimated global poses and color-code the composite scene by height. We compare with pose-free methods [27, 39, 50]. Best view zoomed in on-screen for details*

![[assets/figures/papers/paper_list_l2598_https_arxiv_org_abs_2603_12903/figures/010_Table_4.jpg]]
*Table 4: Pose estimation comparisons on KITTI- 360 [26, 50] and nuScenes [4, 50]. We compare with registration baselines [3, 5, 30, 35, 40] and pose-free NeRF methods [10, 27, 39, 50]*

## 方法谱系与知识库定位

### 基线脉络与差异化定位

SG-NLF 处于无位姿 LiDAR 神经视图合成（pose-free LiDAR NVS）这一新兴方向的交汇点，其基线体系可沿两条轴线梳理：**位姿依赖性**与**表示形式**。

**位姿依赖的 LiDAR 模拟与生成。** 早期工作 **LiDARsim**（Manivasagam et al., CVPR 2020）和 **PCGen**（Li et al., arXiv 2022）开创了基于学习的光线投射与点云生成范式，但它们强依赖真实位姿作为输入。**LiDAR4D**（Zheng et al., CVPR 2024）进一步将这一范式拓展到动态场景，但同样受限于位姿依赖假设。这些方法在面对无可靠位姿的野外采集数据时存在根本性适用障碍。

**位姿自由的 NeRF 适配。** 为解决位姿缺失问题，研究者尝试将无位姿 NeRF 框架与 LiDAR 重建后端耦合：**BARF-LN**（Lin et al., ICCV 2021 + Tao et al., ACM MM 2024）、**HASH-LN**（Heo et al., ICML 2023 + Tao et al., ACM MM 2024）和 **GeoTrans-LN**（Qin et al., CVPR 2022 + Tao et al., ACM MM 2024）均采用 LiDAR-NeRF 作为统一重建后端，但在位姿估计前端分别依赖 BARF 的全连接隐式表示、Instant-NGP 的哈希编码和 GeoTransformer 的几何匹配。这些方法的共同瓶颈在于：位姿优化仅依赖相邻帧的成对对齐，缺乏全局结构约束，在长序列上容易累积漂移。

**GeoNLF 的突破与局限。** **GeoNLF**（Xue et al., NeurIPS 2024）是首个专门为无位姿 LiDAR NVS 设计的神经场框架，其核心贡献在于将几何编码与位姿优化统一到端到端训练中。然而 GeoNLF 的表示层仅依赖多分辨率哈希网格编码来提取局部几何特征，在面对 LiDAR 点云的稀疏性和无纹理特性时，缺乏对连续几何表面的先验约束，导致在无观测区域产生几何空洞（如 Figure 2 所示）。此外，GeoNLF 的位姿图仅包含时序相邻帧的成对约束，无法利用非相邻帧之间的结构冗余来纠正长程漂移。

**SG-NLF 的三重差异化。** 本文在 GeoNLF 的基础上进行了三个关键维度的重构：

1. **表示层**：从纯几何编码升级为**几何编码 + 连续谱嵌入的混合表示**。谱嵌入通过可微优化近似 Laplace-Beltrami 算子的前 K 个特征函数，携带等距不变的结构先验，能够在几何插值失效的无观测区域提供平滑的曲面延拓。这一设计在方法论上借鉴了神经谱方法（如 DeltaConv 等）的谱分解思路，但将其首次引入 LiDAR 神经场重建任务。

2. **位姿优化层**：从仅相邻帧的成对对齐升级为**基于混合特征兼容性的置信度感知全局图优化**。通过构建粗到细的特征匹配流程（式 (9)-(10)），SG-NLF 能够识别并引入非相邻帧之间高置信度的几何约束，形成更稠密的位姿图拓扑。这一设计有效抑制了长序列上的误差累积，使得 ATE 从 GeoNLF 的 0.228 m 降至 0.071 m（nuScenes，Table 4）。

3. **监督层**：引入**多尺度 PatchGAN 跨帧对抗监督**（式 (14)），通过判别器评估合成深度图的跨帧几何一致性，迫使渲染结果在相邻视角间保持结构连贯。这一设计弥补了单帧像素级损失无法捕捉帧间结构失配的缺陷。

### 适用边界与局限

**场景假设。** SG-NLF 当前针对的是**静态场景**下的多帧 LiDAR 序列。动态物体（如行驶车辆、行人）的存在会破坏谱嵌入所依赖的等距假设，导致几何重建和位姿估计同时退化。论文明确将动态场景拓展列为未来工作方向。

**传感器假设。** 方法在 KITTI-360 和 nuScenes 两个数据集上验证，两者均使用旋转式机械 LiDAR（Velodyne HDL-64E 和 HDL-32E）。对于固态 LiDAR、MEMS 扫描或不同线束密度的传感器配置，谱嵌入的离散化策略（式 (4) 中的局部面元计算）和哈希网格的分辨率设置可能需要重新调整，泛化能力尚未验证。

**计算开销。** 谱嵌入的优化需要在前向传播中计算表面梯度（式 (5)）和 Rayleigh 商（式 (7)），增加了训练时的计算负担。虽然 Figure 1 显示 SG-NLF 的推理时间与 GeoNLF 同处于可比较的量级，但训练阶段的额外开销在论文中未做定量分析。

**谱嵌入的理论前提。** 谱嵌入的有效性依赖于 Laplace-Beltrami 算子的离散化质量，而后者又取决于 LiDAR 点云能否形成足够稠密的局部邻域。在极端稀疏区域（如远距离扫描线之间），局部面元估计（式 (4)）的数值稳定性可能下降，此时谱嵌入提供的全局先验可能不足以完全补偿几何编码的缺失——Table 5 显示仅使用谱嵌入（w/o GE）时 CD 升至 0.181，虽优于纯几何编码的 0.241，但仍不及混合表示。

### 开放问题

1. **动态场景拓展**：如何将谱嵌入的等距不变性推广到非刚性形变场景，或通过运动分割将动态区域与静态背景解耦，是 SG-NLF 走向实际部署的关键挑战。

2. **传感器泛化**：不同 LiDAR 传感器的扫描模式、点密度和噪声特性差异显著，混合表示中的哈希网格分辨率和谱嵌入的邻域半径等超参数如何自适应调整，需要系统性的跨传感器迁移研究。

3. **训练效率优化**：谱嵌入的优化与 NeRF 渲染网络和位姿图优化三者耦合训练，是否存在更高效的解耦训练策略（如预训练谱嵌入后冻结），值得探索。

4. **理论分析**：谱嵌入对几何重建的改进是否有更严格的理论保证（如收敛界或误差界），目前论文仅提供了经验性消融证据，缺乏形式化分析。

5. **更大规模场景**：当前实验的序列长度有限（KITTI-360 和 nuScenes 的标准序列），在城市场景级的大规模建图中，全局位姿图的规模增长可能导致优化收敛变慢，置信度感知的边剪枝策略是否需要更激进的稀疏化，有待验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/Spectral_Geometric_Neural_Fields_for_Pose_Free_LiDAR_View_Synthesis.pdf]]