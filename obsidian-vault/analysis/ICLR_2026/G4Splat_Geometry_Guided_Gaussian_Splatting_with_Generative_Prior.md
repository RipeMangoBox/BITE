---
title: "G4Splat: Geometry-Guided Gaussian Splatting with Generative Prior"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/G4Splat_Geometry_Guided_Gaussian_Splatting_with_Generative_Prior_fc38604907dd.pdf
project_link: "https://dali-jack.github.io/g4splat-web/"
code_link: null
aliases:
- G4Splat
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 利用场景中普遍存在的平面结构推导出尺度精确的深度图，作为强几何约束注入生成管线。
primary_logic: 平面表示能够从部分观测中可靠地推断完整平面的深度，结合全局平面融合可获得跨视图一致的尺度精确深度；将这种几何引导贯穿可见性估计、新视图选择与修复过程，可显著减轻多视图不一致，实现高质量的场景补全。
claims:
- 在Replica数据集5视图设置下，G4Splat的CD降至6.61，远优于MAtCha的10.12，重建指标全面领先。
- 消融实验表明，移除平面感知几何建模(PM)后几何重建质量大幅下降，验证了尺度精确深度监督的关键作用。
- 引入平面感知新视图选择和几何引导的修复策略后，渲染质量进一步提升，未观测区域的伪影显著减少。
- 在Mip‑NeRF360户外场景中，我们的方法仍能生成更少的漂浮高斯和更平滑的几何，证明其在非平面、非结构化环境中的鲁棒性。
---

# G4Splat: Geometry-Guided Gaussian Splatting with Generative Prior

> [!tip] 核心洞察
> 平面表示能够从部分观测中可靠地推断完整平面的深度，结合全局平面融合可获得跨视图一致的尺度精确深度；将这种几何引导贯穿可见性估计、新视图选择与修复过程，可显著减轻多视图不一致，实现高质量的场景补全。

| 字段 | 内容 |
|------|------|
| 中文题名 | G4Splat：几何引导生成先验的高斯泼溅 |
| 英文题名 | G4Splat: Geometry-Guided Gaussian Splatting with Generative Prior |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=kdPmsMVhZf) · [Project](https://dali-jack.github.io/g4splat-web/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | G4Splat |
| Dataset | Replica, ScanNet++, DeepBlending, Mip-NeRF 360 |

> [!tip] 效果简介
> - Replica (5 input views) 上，PSNR↑ 23.90 vs 17.81 (MAtCha) (+6.09)；CD↓ 6.61 vs 10.12 (MAtCha) (-3.51)。
> - ScanNet++ (5 input views) 上，PSNR↑ 18.69 vs 13.58 (MAtCha) (+5.11)。
> - DeepBlending (5 input views) 上，PSNR↑ 16.76 vs 14.74 (MAtCha) (+2.02)。

## 概要

**核心问题**：稀疏视图下的3D场景重建面临严重的形状-外观歧义。现有方法将3D高斯泼溅与生成先验结合时，普遍缺乏可靠的几何监督与有效的多视图一致性机制，导致观测区域与未观测区域的重建质量均不理想——漂浮高斯密集、几何结构破碎、渲染伪影显著。这一瓶颈在5视图等极度稀疏的设置下尤为突出。

**G4Splat的核心思路**：利用人造环境中广泛存在的平面结构（符合曼哈顿世界假设），从部分观测中可靠地推断完整平面的尺度精确深度，并将这种几何引导贯穿可见性估计、新视图选择与扩散修复的全流程。具体而言，方法先提取全局3D平面，通过射线-平面交会计算平面区域的绝对深度，再以线性对齐将单目深度估计转换到统一尺度，形成“平面感知深度图”。以此为基础构建3D可见性体素网格获得可靠掩码，并以全局平面为代理目标搜索最优新相机位姿，最终用几何引导的单一视点颜色监督减少多视图修复冲突。

**主要结果**：在Replica数据集5视图设置下，G4Splat的Chamfer Distance降至6.61（MAtCha为10.12），PSNR达到23.90（MAtCha为17.81），几何与渲染指标全面领先。在ScanNet++、DeepBlending及Mip-NeRF 360户外场景中同样取得一致优势，证明方法对非平面、非结构化环境也具有鲁棒性。消融实验证实，平面感知几何建模是几何质量提升的关键驱动，而几何引导的生成管线进一步消除了未观测区域的伪影。

**方法定位**：G4Splat以**MAtCha**（Guédon et al., 2025）为骨架，继承其图表对齐初始化与稀疏视图训练目标，但在深度监督来源、可见性掩码估计、新视点选择策略、多视图修复一致性及结构损失计算五个关键环节进行了根本性改造，将平面几何约束系统性地注入生成重建管线，属于“几何引导的生成式3DGS”方法。

### 稀疏视图三维重建的核心挑战

从少量输入图像恢复完整的三维场景是计算机视觉中的核心难题。当输入视图数量极度稀疏（如5～9张）时，场景的大部分区域在训练视图中不可见，系统必须同时完成两项任务：对已观测区域进行精确的几何与外观重建，以及对未观测区域进行合理的场景补全。这两个目标相互耦合——几何精度不足会导致补全区域出现漂浮伪影，而补全策略的不一致又会反向污染已观测区域的重建质量。

近年来，三维高斯泼溅（3D Gaussian Splatting, **3DGS** (Kerbl et al., 2023)）及其变体（如 **2DGS** (Huang et al., 2024a)）凭借实时渲染与显式几何表示的优势成为场景重建的主流范式。然而，这些方法对输入视图数量高度敏感：在稀疏视图条件下，优化过程缺乏足够的多视图约束，导致几何解空间高度欠定，形状与外观之间存在严重的歧义性。

### 现有方法的瓶颈：几何监督缺失与多视图不一致

为缓解稀疏性带来的歧义，近期工作开始引入生成先验进行场景补全。**MAtCha** (Guédon et al., 2025) 通过图表对齐（chart-based alignment）从 MASt3R-SfM 获取深度图作为几何监督，并结合视频扩散模型生成新视图以扩展观测覆盖。类似地，**GenFusion** (Wu et al., 2025c)、**Difix3D+** (Wu et al., 2025a) 和 **GuidedVD** (Zhong et al., 2025) 等方法也尝试将扩散模型的生成能力注入高斯泼溅管线。

然而，这些方法存在两个根本性缺陷：

1. **几何监督不可靠**：MAtCha 通过图表对齐获得的深度图在训练视图之间的非重叠区域存在显著误差（见 Figure 3a），导致几何重建质量不佳。在稀疏视图设定下，非重叠区域恰恰是场景补全的关键区域，错误的深度监督会直接导致补全区域出现漂浮高斯和几何塌缩。

2. **生成管线缺乏多视图一致性**：现有方法在利用视频扩散模型修复新视图时，缺乏有效的机制来保证不同视角之间的颜色与几何一致性。朴素的新视图选择策略（如椭圆轨迹）仅提供局部覆盖，导致最终重建中出现可见的接缝和黑色阴影（见 Figure 3c 和 Figure A3）。此外，基于 alpha 图的可见性掩码估计在可见区域常出现误判，将本已观测的区域错误标记为缺失，进一步加剧了训练信号中的冲突。

### 核心洞察：平面结构作为几何锚点

本文的核心观察是：在人造环境中，平面结构（墙壁、地板、桌面等）普遍存在，符合曼哈顿世界假设（Coughlan & Yuille, 1999）。这些平面结构具有一个关键性质——即使只能从部分视角观测到平面的一部分，也可以通过多视图几何推断出完整平面的三维参数。一旦获得全局一致的平面方程，就可以通过射线-平面交会精确计算平面区域内任意像素的深度值，从而获得**尺度精确**的深度监督。

这一洞察直接回应了上述两个瓶颈：尺度精确的深度图为几何重建提供了强约束，缓解了形状-外观歧义；而全局平面作为场景的轻量级代理，可以引导新视图选择、可见性估计和修复一致性的优化，从而系统性地提升生成管线的多视图一致性。

### 本文动机与目标

基于上述分析，本文提出 **G4Splat**（Geometry-Guided Gaussian Splatting with Generative Prior），旨在将可靠的几何引导系统性地注入生成式高斯泼溅管线。具体而言，G4Splat 追求以下目标：

- 利用场景中普遍存在的平面结构，从部分观测中推导出尺度精确的深度图，为稀疏视图重建提供强几何约束；
- 将几何引导贯穿于可见性估计、新视图选择与扩散修复的全流程，显著减轻多视图不一致问题；
- 在保持生成先验补全能力的同时，使重建结果在已观测和未观测区域均达到高质量几何与外观。

## 核心方法与创新机理

G4Splat 的核心创新在于将**尺度精确的平面几何约束**系统性地注入生成式高斯基元重建管线，从而解决稀疏视图下观测区域与未观测区域均面临的形状-外观歧义问题。与现有方法（如 MAtCha）仅依赖 SfM 导出的噪声深度监督不同，G4Splat 从场景中普遍存在的平面结构出发，构建了一套完整的几何引导机制，贯穿深度估计、可见性判定、新视点选择与多视图修复等关键环节。

### 关键改进维度

**1. 平面感知的尺度精确深度图**

MAtCha 通过图表对齐从 MASt3R-SfM 获取深度图，但在无重叠区域存在明显误差（见 Figure 3a）。G4Splat 的核心突破在于利用曼哈顿世界假设下的平面先验来推导绝对尺度的深度约束：
- 先通过 SAM 实例分割与法向图 K-means 聚类提取 2D 平面掩码，再结合 3D 点云合并为全局一致的 3D 平面 $\Phi_k : \mathbf{n}_k^{\top}\mathbf{x} + d_k = 0$。
- 对平面掩码内的像素，通过射线-平面交会直接计算精确深度 $D_i^v(\mathbf{u}) = \frac{-\mathbf{n}_{k_i}^{\top}\mathbf{o}^v - d_{k_i}}{\mathbf{n}_{k_i}^{\top}\mathbf{r}^v(\mathbf{u})}$。
- 对非平面区域，利用平面区域已知的绝对深度，通过最小二乘拟合 $D^v(\mathbf{u}) = a_v \hat{D}^v(\mathbf{u}) + b_v$ 将单目相对深度线性对齐至绝对尺度。

这一设计使 G4Splat 获得了比 MAtCha 更可靠、更完整的深度监督信号，为后续所有几何引导操作奠定了基础。

**2. 几何引导的可见性掩码估计**

MAtCha 基于 alpha 图的掩码在可见区域常被误判为缺失（见 Figure 3b）。G4Splat 改用平面感知深度图构建 3D 可见性体素网格：将每个体素中心投影至训练视图，检查是否落在有效深度范围内，若在所有训练视图中均可见则标记为可见。对于新视点中的像素，沿射线采样 $Q$ 个点并查询体素网格，仅当所有采样点均可见时该像素才被判定为可见：$V^v(\mathbf{u}) = \prod_{q=1}^{Q} v_q$。这种基于显式几何的判定方式显著减少了误判，使修复区域更准确地聚焦于真正需要生成的内容。

**3. 平面感知的新视点选择**

MAtCha 的朴素椭圆轨迹仅提供局部覆盖，导致可见接缝（见 Figure 3c）。G4Splat 以全局 3D 平面为对象代理，搜索最大化平面覆盖率、最小化距离且对齐平面法向的新相机位姿。这一策略使新视点能更完整地覆盖场景结构，为后续生成修复提供更优的观测条件。

**4. 几何引导的多视图修复一致性**

视频扩散模型（如 See3D）的输出仍存在多视图不一致，直接训练会引入黑色阴影（见 Figure A3）。G4Splat 根据平面区域选取最完整视角、非平面区域采用首次可见视角，以单一视点颜色监督各区域，减少多视图冲突。这一策略有效抑制了修复伪影，使渲染结果更清晰锐利。

**5. 结构损失中的几何约束增强**

G4Splat 采用与 MAtCha 相同的总训练损失形式 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{rgb}} + \mathcal{L}_{\mathrm{reg}} + \mathcal{L}_{\mathrm{struct}}$，但关键区别在于：结构损失中的深度项 $D_i$、法向项 $N_i$ 和平均曲率项 $M_i$ 均改用平面感知深度图计算，而非 MAtCha 的图表对齐深度。这为训练过程引入了更强的几何约束，使重建几何更加平滑完整。

### 创新机制的协同效应

上述改进并非孤立生效，而是形成正向反馈循环：平面感知深度图提供可靠的几何初始化 → 可见性网格准确识别缺失区域 → 平面感知新视点选择优化观测覆盖 → 几何引导修复生成一致内容 → 增强的结构损失约束训练过程。消融实验（Table 3）定量验证了这一协同效应：仅加入生成先验（GP）时 CD 为 10.60；补充平面感知几何建模（PM）后 CD 降至 6.61；再引入几何引导的生成管线（PP）后 PSNR 进一步提升至 23.90，证明各模块的叠加贡献。

G4Splat 的整体流程围绕一个核心洞察展开：场景中普遍存在的平面结构可以从部分观测中可靠地推断完整平面的深度，结合全局平面融合可获得跨视图一致的尺度精确深度；将这种几何引导贯穿可见性估计、新视图选择与修复过程，可显著减轻多视图不一致，实现高质量的场景补全。

### 方法总览

G4Splat 建立在 **MAtCha**（Guédon et al., 2025）的基础框架之上，后者通过图表对齐从 MASt3R-SfM 获取几何初始化，并以 2DGS（Huang et al., 2024a）作为底层高斯泼溅表示。G4Splat 的完整训练流程采用**迭代生成式训练循环**，如 Figure 2 所示，每个循环包含以下关键模块：

![[assets/figures/papers/paper_list_l83_https_openreview_net_forum_id_kdPmsMVhZf/figures/002_Figure_2.jpg]]
*Figure 2: Overview of G4SPLAT. For each training loop (Section 3.4), we first extract global 3D planes from all training views and compute plane-aware depth maps (Section 3.2). Subsequently, we construct a visibility grid from these depth maps, select plane-aware novel views, inpaint their invisible regions, and incorporate the completed views back into the training set (Section 3.3)*

1. **全局 3D 平面提取与平面感知深度图生成**（Section 3.2）：从所有训练视图中提取全局一致的 3D 平面，并利用射线-平面交会计算平面区域的尺度精确深度；非平面区域则通过单目深度估计与线性对齐获得绝对尺度深度。
2. **几何引导的生成管线**（Section 3.3）：基于平面感知深度图构建 3D 可见性体素网格，获得可靠的可见性掩码；以全局 3D 平面为代理目标进行平面感知的新视点选择；对选定的新视点使用视频扩散模型修复不可见区域，并通过几何引导的单一视点颜色监督减少多视图冲突。
3. **训练与迭代扩展**（Section 3.4）：将修复后的新视点加入训练集，采用与 MAtCha 相同的总损失形式进行 2DGS 训练，但将结构损失中的深度项替换为平面感知深度图，以引入更强的几何约束。在实验中采用三个生成训练循环，逐步扩展观测覆盖并优化一致性。

### 训练损失

G4Splat 的总损失沿用 MAtCha 的框架：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{rgb}} + \mathcal{L}_{\mathrm{reg}} + \mathcal{L}_{\mathrm{struct}}$$

其中 $\mathcal{L}_{\mathrm{rgb}}$ 为 RGB 重建损失，$\mathcal{L}_{\mathrm{reg}}$ 为 2DGS 的正则化损失，$\mathcal{L}_{\mathrm{struct}}$ 为结构损失。G4Splat 的关键改动在于：**结构损失中的 $D_i$、$N_i$、$M_i$ 均改用平面感知深度图计算**，从而将尺度精确的几何约束注入优化过程。

### 核心模块间的因果链路

整个管线的因果链条可概括为：**平面提取 → 尺度精确深度 → 可靠可见性掩码 → 合理新视点选择 → 一致性修复 → 强几何约束训练**。每个模块的改进都直接针对前序模块的不足：

- **平面感知深度图**解决了 MAtCha 在无重叠区域的深度误差问题（Figure 3a），为后续模块提供了准确的 3D 几何参考。
- **可见性体素网格**基于精确深度构建，避免了基于 alpha 图的噪声掩码中将可见区域误判为缺失的问题（Figure 3b）。
- **平面感知新视点选择**以全局 3D 平面为代理目标，搜索最大化平面覆盖率、最小化距离且对齐平面法向的相机位姿，克服了朴素椭圆轨迹仅提供局部覆盖导致可见接缝的缺陷（Figure 3c）。
- **几何引导修复**根据平面区域选取最完整视角、非平面区域采用首次可见视角，以单一视点颜色监督各区域，有效消除了多视图不一致修复引入的黑色阴影伪影（Figure A3）。

### 输入输出流

- **输入**：稀疏的多视图 RGB 图像（如 5 或 9 张），可选的相机位姿（也支持无位姿视频和单视图场景）。
- **中间产物**：全局 3D 平面参数 $\Phi_k : \mathbf{n}_k^{\top}\mathbf{x} + d_k = 0$、平面感知深度图 $D^v$、可见性掩码 $V^v$、修复后的新视点图像。
- **输出**：可渲染任意新视点的 3D 高斯泼溅表示，同时可导出带纹理的网格用于几何评估。

该框架对底层扩散模型的依赖是可插拔的——实验表明，即使搭配较弱的生成先验（如 ViewCrafter），几何引导管线仍能保持高质量重建（Table A2, Figure A4），验证了方法的普适性。

![[assets/figures/papers/paper_list_l83_https_openreview_net_forum_id_kdPmsMVhZf/figures/014_Table.jpg]]
*Table: A2: Quantitative results of our method integrated with different diffusion models*

G4Splat 的核心架构建立在 **MAtCha** (Guédon et al., 2025) 的图表对齐初始化与稀疏视图训练目标之上，通过三个关键模块注入几何引导：**平面感知几何建模**、**几何引导的生成管线**、以及**迭代训练循环**。整体训练损失沿用 MAtCha 的形式：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{rgb}} + \mathcal{L}_{\mathrm{reg}} + \mathcal{L}_{\mathrm{struct}}$$

其中 $\mathcal{L}_{\mathrm{rgb}}$ 为 RGB 重建损失，$\mathcal{L}_{\mathrm{reg}}$ 为 2DGS 原始正则化损失，而 $\mathcal{L}_{\mathrm{struct}}$ 为结构损失。G4Splat 的核心改动在于：结构损失中的深度项 $D_i$、法向项 $N_i$ 与平均曲率项 $M_i$ 不再使用 MAtCha 的图表对齐深度计算，而是改用**平面感知深度图**计算（见 Section B.3），从而引入更强的几何约束。

---

### 平面提取与全局 3D 平面估计

该模块的目标是从稀疏训练视图中提取全局一致的 3D 平面表示，作为后续所有几何引导的锚点。

**2D 平面掩码提取**：对每张训练图像，首先利用 **SAM** (Kirillov et al., 2023) 生成实例掩码，同时从深度图梯度或单目法向预测器 (Ye et al., 2024) 获取法向图；然后在每个实例掩码内对法向进行 K‑means 聚类，得到 2D 平面掩码。

**全局 3D 平面合并**：将各视图的 2D 平面掩码提升至 3D 点云后，通过几何相似性（法向夹角与偏移距离）将跨视图的平面片段合并为全局 3D 平面。每个全局平面 $\Phi_k$ 由单位法向量 $\mathbf{n}_k$ 和偏移量 $d_k$ 参数化：

$$\Phi_k : \mathbf{n}_k^{\top}\mathbf{x} + d_k = 0$$

对每个全局平面的高置信度点云子集 $\mathcal{P}_k^{\mathrm{conf}}$，通过 RANSAC 稳健估计平面参数：

$$\min_{\mathbf{n}_k, d_k} \sum_{\mathbf{p} \in \mathcal{P}_k^{\mathrm{conf}}} (\mathbf{n}_k^{\top}\mathbf{p} + d_k)^2, \; \mathrm{s.t.} \; \|\mathbf{n}_k\|=1$$

> **因果机制**：全局平面合并将局部 2D 观测聚合为跨视图一致的 3D 代理，使得平面区域深度可从射线‑平面交会直接计算，从根本上规避了 MAtCha 在无重叠区域因 MASt3R‑SfM 稀疏点云不足导致的深度误差（见 Figure 3a）。

---

### 平面感知深度图生成

该模块为每张训练视图生成尺度精确的完整深度图，是 G4Splat 最核心的几何约束来源。

**平面区域深度**：对于像素 $\mathbf{u}$ 所属的平面 $k_i$，通过相机射线 $\mathbf{r}^v(\mathbf{u})$ 与全局平面 $\Phi_{k_i}$ 的交会直接计算深度：

$$D_i^v(\mathbf{u}) = \frac{-\mathbf{n}_{k_i}^{\top}\mathbf{o}^v - d_{k_i}}{\mathbf{n}_{k_i}^{\top}\mathbf{r}^v(\mathbf{u})}$$

其中 $\mathbf{o}^v$ 为相机光心。该深度具有绝对尺度且跨视图几何一致。

**非平面区域深度对齐**：对于非平面像素，先使用单目深度估计器获取相对深度 $\hat{D}^v(\mathbf{u})$，再利用平面区域已知的绝对深度通过最小二乘拟合线性变换参数 $a_v, b_v$，将相对深度拉伸至绝对尺度：

$$D^v(\mathbf{u}) = a_v \hat{D}^v(\mathbf{u}) + b_v$$

最终得到的 $D^v$ 融合了几何一致的平面深度与尺度对齐的单目深度，形成完整且尺度精确的平面感知深度表示。

> **因果机制**：这一设计将场景中普遍存在的平面结构转化为强几何先验——平面区域深度由解析几何直接给出（零估计误差），非平面区域深度通过平面锚点获得可靠的绝对尺度校准。消融实验证实，移除该模块后 CD 从 6.61 升至 10.60，几何重建质量大幅下降（Table 3）。

---

### 几何引导的生成管线

该管线包含三个子模块，将平面感知深度图提供的几何信息贯穿于可见性估计、新视点选择与扩散修复全过程。

**可见性网格构建**：根据所有训练视图的平面感知深度图构建 3D 体素网格。对每个体素，将其中心投影至各训练视图，若投影深度落在有效深度范围内则标记为可见（visibility = 1）。对于新视点中的像素 $\mathbf{u}$，沿其射线采样 $Q$ 个点并查询体素网格，所有采样点均可见时该像素才被视为可见：

$$V^v(\mathbf{u}) = \prod_{q=1}^{Q} v_q$$

与 MAtCha 基于 alpha 图的噪声掩码相比，该方法能准确区分真正未观测区域与可见区域（见 Figure 3b）。

**平面感知新视点选择**：以全局 3D 平面为场景代理，搜索最大化平面覆盖率、最小化距离且对齐平面法向的新相机位姿 $\mathbf{c}^*$：

$$\mathbf{c}^* = \arg\max_{\mathbf{c}\in\mathcal{C}} \Big( R(\mathbf{c}) + \big|\cos\theta(\mathbf{c},\mathbf{p},\mathbf{n})\big| - D(\mathbf{c},\mathbf{p},\mathbf{n}) \Big)$$

其中 $R(\mathbf{c})$ 为平面点覆盖率，$\theta$ 为视角与平面法向的夹角，$D$ 为相机到平面的距离。该策略相比朴素椭圆轨迹能提供更全局的覆盖，减少可见接缝（见 Figure 3c）。

**几何引导的扩散修复**：使用视频扩散模型（默认 **See3D**，Ma et al., 2025）修复新视点中的不可见区域。关键在于修复后的多视图监督策略：对平面区域，选取该平面最完整的单一视角颜色作为监督；对非平面区域，采用首次可见视角的颜色监督。这种“单视点颜色监督”避免了多视图不一致修复导致的黑色阴影伪影（见 Figure A3）。消融实验表明，加入该管线（PP）后 PSNR 从已有 GP+PM 的基础上进一步提升至 23.90（Table 3）。

---

### 迭代训练循环

G4Splat 采用两阶段迭代训练（见 Figure 2）：

1. **初始化阶段**：使用平面感知深度图进行 2DGS 初始训练，建立可靠的几何基座。
2. **生成循环阶段**：执行多次生成循环（默认 3 次），每轮包括：构建可见性网格 → 选择平面感知新视点 → 几何引导修复 → 将修复后的新视点加入训练集重新训练 2DGS。每轮训练沿用 Eq. (1) 的总损失，但结构损失中的深度项始终使用平面感知深度图计算。

这种迭代设计使观测覆盖逐步扩展，同时几何约束贯穿始终，确保新增的修复区域与已有几何保持一致。

> **证据强度说明**：上述模块的有效性由 Table 3 的消融实验系统验证——逐步加入生成先验 (GP)、平面感知几何建模 (PM) 与几何引导管线 (PP) 后，各项指标持续提升。Table A2 进一步表明，即使替换为较弱的扩散模型（如 ViewCrafter），几何引导管线仍能保持高质量重建，验证了方法的普适性。

## 实验与关键发现

### 实验设置

所有实验遵循统一的公平性协议：所有基线方法均使用 **MASt3R‑SfM** 进行几何初始化，以保证稀疏视图下的对比公平性；所有方法在相同硬件环境下运行，训练迭代次数固定为 7000 次，且生成循环中每轮新增视图数量一致（10 张）。G4Splat 采用三个生成训练循环，训练损失沿用 **MAtCha** (Guédon et al., 2025) 的总损失形式（式 (1)），但将图表深度图替换为平面感知深度图，从而引入更强的几何约束。

### 主要定量结果

**室内场景（5 输入视图）。** 在 Replica、ScanNet++ 和 DeepBlending 三个数据集上，G4Splat 在全部重建与渲染指标上显著超越所有基线方法（Table 1）。以 Replica 数据集为例，G4Splat 的 Chamfer Distance (CD) 降至 **6.61**，较 MAtCha 的 10.12 降低 3.51，降幅达 34.7%；PSNR 达到 **23.90** dB，较 MAtCha 的 17.81 dB 提升 6.09 dB。在 ScanNet++ 上，PSNR 从 13.58 dB 提升至 **18.69** dB（+5.11 dB），CD 从 9.86 降至 **6.34**。在 DeepBlending 上，PSNR 从 14.74 dB 提升至 **16.76** dB（+2.02 dB）。值得注意的是，G4Splat 在几何指标（CD、F-Score、Normal Consistency）上的优势尤为突出，验证了平面感知几何建模对重建质量的根本性贡献。

**室外场景（9 输入视图）。** 在 Mip‑NeRF 360 数据集上，G4Splat 同样取得最优结果（Table 2），PSNR 达到 **18.66** dB，较基于视频扩散模型的 **See3D** (Ma et al., 2025) 的 16.92 dB 提升 1.74 dB。逐场景分析（Table A3）表明，G4Splat 不仅在室内曼哈顿式场景（bonsai、counter、kitchen、room）表现优异，在室外非结构化场景（bicycle、flowers、garden、stump、treehill）同样保持领先，证明其几何引导策略对非平面环境具有鲁棒性。

**不同稀疏度下的稳定性。** 在 Replica 数据集上测试不同输入视图数量（Table A1），G4Splat 在所有稀疏度设置下均一致优于基线方法，表明其几何引导机制不依赖特定视图密度。

### 消融实验

消融实验（Table 3）系统拆解了三个核心组件的贡献：

![[assets/figures/papers/paper_list_l83_https_openreview_net_forum_id_kdPmsMVhZf/figures/008_Table_3.jpg]]
*Table 3: Ablation study*

1. **生成先验 (GP) 的基础作用。** 仅使用生成先验而不引入几何建模时，方法退化为类似 MAtCha 的基线，CD 约为 10.60，PSNR 约为 17.81。
2. **平面感知几何建模 (PM) 的关键贡献。** 在 GP 基础上加入 PM 后，CD 从 10.60 骤降至 **6.61**，降幅达 37.6%，证明尺度精确的平面感知深度监督是几何重建质量提升的核心驱动力。这一结果与 Figure 3(a) 中的中间可视化一致：MAtCha 在非重叠区域存在显著的深度误差，而平面感知深度图有效修正了这些区域。
3. **几何引导管线 (PP) 的增益。** 在 GP+PM 基础上进一步引入平面感知新视点选择与几何引导修复策略，PSNR 进一步提升至 **23.90** dB，渲染伪影显著减少。Figure A3 的对比直观展示了不一致修复导致的黑色阴影，以及几何引导一致性修复对伪影的消除效果。

**扩散模型通用性。** 将 G4Splat 的几何引导管线与不同扩散模型（如 ViewCrafter）集成时（Table A2、Figure A4），仍能保持高质量重建，即使使用较弱的生成先验，也能有效抑制漂浮高斯并减少模糊，验证了框架的通用性。

### 定性分析

Figure 4 展示了主要定性对比：G4Splat 在观测区域与未观测区域均生成更少漂浮高斯、更平滑的几何以及更清晰的外观。Figure A6 进一步叠加可见性掩码，金色区域标记了 5 个输入视图中完全不可见的区域，G4Splat 在这些区域仍能恢复合理几何与纹理，而基线方法则出现明显空洞或噪声。Figure 5 展示了跨场景泛化能力，涵盖室内、室外、单视图、无位姿视频等多种输入条件。

![[assets/figures/papers/paper_list_l83_https_openreview_net_forum_id_kdPmsMVhZf/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison. Our approach achieves better appearance and geometry reconstruction with fewer Gaussian floaters in both observed and unobserved regions*

![[assets/figures/papers/paper_list_l83_https_openreview_net_forum_id_kdPmsMVhZf/figures/006_Figure_5.jpg]]
*Figure 5: Any-view scene reconstruction. Our method demonstrates strong generalization across diverse scenarios, including indoor and outdoor scenes, unposed scenes and even single-view scenes*

![[assets/figures/papers/paper_list_l83_https_openreview_net_forum_id_kdPmsMVhZf/figures/017_Figure.jpg]]
*Figure: A6: Qualitative comparison from 5 input views with visibility mask. In the GT images, golden regions indicate areas unobserved across the 5 input views. G4Splat outperforms baselines in both visible and unobserved regions, producing superior geometry with improved smoothness and minimal Gaussian artifacts*

### 失败模式与局限性

尽管 G4Splat 在多数场景表现优异，仍存在以下局限：

1. **修复区域色差。** 受限于当前视频扩散模型的颜色一致性，修复区域的颜色可能与原始场景不完全匹配，导致训练后渲染输出出现局部色差（Figure A5）。
2. **严重遮挡场景。** 对于被前景物体严重遮挡的区域（如被桌子部分遮挡的椅子），难以生成合理的观测相机位姿，导致重建质量下降（Figure A5）。
3. **非平面区域深度精度。** 方法依赖平面假设提取尺度精确深度；虽然单目深度估计器在非平面区域表现尚可，但更通用的曲面表示有望进一步提升非平面区域的深度精度。

### 运行时间分析

Table 4 报告了各方法的运行时间对比。G4Splat 的完整管线在计算开销上有所增加，但通过下采样加速版本（Ours DS）可在保持显著性能优势的同时大幅降低时间成本，体现了方法在实际部署中的灵活性。

## 定位与知识库关联

### 1. 技术脉络与继承关系

G4Splat 的核心架构建立在 **MAtCha**（Guédon et al., 2025）的基础之上。MAtCha 引入图表对齐（chart-based alignment）机制，将 MASt3R-SfM 导出的稀疏点云与可变形表面图表进行拟合，为稀疏视图下的 3DGS 训练提供结构约束。G4Splat 完整继承了这一训练框架——包括总损失函数 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{rgb}} + \mathcal{L}_{\mathrm{reg}} + \mathcal{L}_{\mathrm{struct}}$、图表变形初始化策略以及生成循环的迭代范式——但在五个关键环节进行了系统性改造，将“几何猜测”升级为“几何测量”。

在底层表示层面，G4Splat 沿用 **2DGS**（Huang et al., 2024a）的二维高斯泼溅基元，这使其天然继承了 2DGS 在表面重建上的优势。与之对比，**3DGS**（Kerbl et al., 2023）作为经典三维高斯泼溅基线，在稀疏视图下缺乏有效的几何约束机制，而 **FSGS**（Zhu et al., 2024）和 **InstantSplat**（Fan et al., 2024）虽针对稀疏视图进行了优化，但未引入生成先验来补全未观测区域。

在生成先验的利用方式上，G4Splat 与同期工作形成鲜明对比。**GenFusion**（Wu et al., 2025c）和 **Difix3D+**（Wu et al., 2025a）将扩散模型直接用于新视图合成或修复，但缺乏对多视图一致性的显式几何约束。**GuidedVD**（Zhong et al., 2025）引入视频扩散模型，但在新视图选择上采用朴素的椭圆轨迹，导致可见性接缝。G4Splat 的核心差异在于：将平面几何作为“先验注入的锚点”，贯穿深度监督、可见性估计、新视图选择和修复一致性四个环节，而非仅在生成结果上进行后处理。

### 2. 关键改造点与因果机制

G4Splat 对 MAtCha 的五项改造构成了一个因果闭环，其逻辑链条如下：

**改造一：深度监督来源的根本性替换。** MAtCha 通过图表对齐从 MASt3R-SfM 获取深度图，但在视图间无重叠区域存在显著误差（Figure 3a 中圈出的区域）。G4Splat 转而利用场景中普遍存在的平面结构，先提取全局 3D 平面 $\Phi_k : \mathbf{n}_k^{\top}\mathbf{x} + d_k = 0$，再通过射线-平面交会直接计算平面区域的尺度精确深度 $D_i^v(\mathbf{u}) = \frac{-\mathbf{n}_{k_i}^{\top}\mathbf{o}^v - d_{k_i}}{\mathbf{n}_{k_i}^{\top}\mathbf{r}^v(\mathbf{u})}$。非平面区域则用单目深度估计并通过线性对齐 $D^v(\mathbf{u}) = a_v \hat{D}^v(\mathbf{u}) + b_v$ 转换至绝对尺度。这一改造是后续所有几何引导模块的基石。

**改造二：可见性掩码从“噪声猜测”到“几何判定”。** MAtCha 基于 alpha 图的掩码常将可见区域误判为缺失（Figure 3b）。G4Splat 根据平面感知深度构建三维可见性体素网格，沿射线采样 Q 个点，累积判定像素可见性 $V^v(\mathbf{u}) = \prod_{q=1}^{Q} v_q$。这一改造直接影响了后续修复区域的选择精度。

**改造三：新视图选择从“局部覆盖”到“平面代理驱动”。** 朴素椭圆轨迹仅提供局部覆盖，导致最终重建出现可见接缝（Figure 3c）。G4Splat 以全局 3D 平面为对象代理，搜索最大化平面覆盖率、最小化距离且对齐平面法向的新相机位姿 $\mathbf{c}^* = \arg\max_{\mathbf{c}\in\mathcal{C}} \big( R(\mathbf{c}) + |\cos\theta(\mathbf{c},\mathbf{p},\mathbf{n})| - D(\mathbf{c},\mathbf{p},\mathbf{n}) \big)$。这一策略确保新视图能有效覆盖未观测的平面区域。

**改造四：多视图修复从“冲突融合”到“单源监督”。** 视频扩散模型（**See3D**，Ma et al., 2025）的输出仍存在多视图不一致，直接训练会引入黑色阴影（Figure A3 中的 Incon. 结果）。G4Splat 根据平面区域选取最完整视角、非平面区域采用首次可见视角，以单一视点颜色监督各区域，从源头减少多视图冲突。

**改造五：结构损失中的深度项替换。** MAtCha 结构损失中的 $D_i$、$N_i$、$M_i$ 原基于图表对齐深度计算，G4Splat 改用平面感知深度，引入更强的几何约束。

消融实验验证了这一因果链条的强度：仅加入平面感知几何建模（PM）即可将 CD 从 10.60 降至 6.61；在此基础上补充几何引导的生成管线（PP）使 PSNR 进一步提升至 23.90（Table 3）。

### 3. 适用边界与局限

**平面假设的依赖与鲁棒性。** G4Splat 的核心机制依赖曼哈顿世界假设——场景中存在可提取的平面结构。在室内结构化场景（Replica、ScanNet++）中，这一假设充分成立，方法表现优异。在 Mip-NeRF 360 的户外场景中，尽管存在大量非平面结构（树木、花卉、山丘），G4Splat 仍能生成更少的漂浮高斯和更平滑的几何（Table A3，Figure A7），PSNR 达到 18.66，优于 See3D 的 16.92（Table 2）。这表明平面感知深度在非平面区域通过单目深度对齐仍能提供有效的尺度约束，但更通用的曲面表示有望进一步提升非平面区域的深度精度。

**生成先验的固有限制。** 受限于当前视频扩散模型的颜色一致性，修补区域的颜色可能与原始场景不完全匹配，导致局部色差。这一限制在消融实验中表现为：即使使用较弱的生成先验（如 ViewCrafter），G4Splat 的几何重建仍保持高质量，但渲染质量有所下降（Table A2，Figure A4）。

**严重遮挡场景的退化。** 对于被物体严重遮挡的区域（如被桌子部分遮挡的椅子），难以生成合理的观测相机位姿，导致重建质量不佳。这是方法明确记录的失败模式（Figure A5）。

**计算开销。** 平面提取、全局平面融合、可见性网格构建和平面感知新视图搜索引入了额外计算。Table 4 显示完整流程的运行时间高于 MAtCha，但下采样加速版本（Ours DS）在保持性能优势的同时显著降低了时间开销。

### 4. 开放问题

1. **物体级先验的引入。** 当前方法仅依赖平面级几何先验，对于严重遮挡的场景区域，能否引入 CAD 模型或类别级形状先验来推断被遮挡物体的完整几何？这需要解决通用物体先验与场景特定几何之间的配准与融合问题。

2. **通用曲面表示。** 平面假设在非结构化自然场景中受限。能否设计一种比平面更灵活但保持计算高效性的曲面表示（如局部二次曲面或可变形面片），以同时提升平面和非平面区域的深度估计精度？这需要在表示能力与优化稳定性之间取得平衡。

3. **无约束场景的推广。** 当前方法在曼哈顿世界假设下表现最佳。能否将几何引导的生成修复策略推广到完全无约束的自然景观，而无需依赖平面结构提取？可能的路径包括从运动恢复结构（SfM）中提取更通用的几何基元，或利用语义分割引导的区域深度估计。

4. **实时部署的加速。** 如何进一步减小几何引导管线带来的计算开销，使方法能更快速地部署于实时应用？可能的优化方向包括：平面提取的轻量化、可见性网格的稀疏化、以及新视图选择的近似搜索策略。

5. **生成先验与几何约束的更深层融合。** 当前框架中，生成先验（扩散模型）和几何约束（平面深度）是串行协作的。能否在扩散模型的去噪过程中直接注入几何条件，使生成结果天然满足多视图几何一致性，而非在生成后再进行几何引导的选择与过滤？

## 原文 PDF

![[paperPDFs/ICLR_2026/G4Splat_Geometry_Guided_Gaussian_Splatting_with_Generative_Prior_fc38604907dd.pdf]]
