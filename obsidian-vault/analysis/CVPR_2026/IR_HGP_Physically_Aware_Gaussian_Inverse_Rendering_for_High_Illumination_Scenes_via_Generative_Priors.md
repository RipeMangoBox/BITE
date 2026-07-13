---
title: "IR-HGP: Physically-Aware Gaussian Inverse Rendering for High-Illumination Scenes via Generative Priors"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/IR_HGP_Physically_Aware_Gaussian_Inverse_Rendering_for_High_Illumination_Scenes_via_Generative_Priors.pdf
project_link: null
code_link: null
aliases:
- IH
- IR-HGP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过引入显式网格代理的物理可见性（HVD）、条件扩散生成先验（GIFP）及自适应辐射校正（PARC），实现材质与光照的物理正确分离。
primary_logic: 利用物理可见性（HVD）与生成先验（GIFP）约束逆渲染优化空间，并通过自适应ACES色调映射（PARC）稳定高动态范围梯度，解决高光照下的材质-光照混淆问题。
claims:
- 在RelightObj数据集上，平均PSNR达33.61，SSIM 0.9761，LPIPS 0.0369，全面超越TensoIR、GS-IR、R3DG、DiscretizedSDF等基线方法。
- 在Mip-NeRF 360数据集上同样取得最优指标，验证了对真实世界复杂光照的鲁棒性。
- RelightObj 上 PSNR (Mean) = 33.61
- RelightObj 上 SSIM (Mean) = 0.9761
---

# IR-HGP: Physically-Aware Gaussian Inverse Rendering for High-Illumination Scenes via Generative Priors

> [!tip] 核心洞察
> 利用物理可见性（HVD）与生成先验（GIFP）约束逆渲染优化空间，并通过自适应ACES色调映射（PARC）稳定高动态范围梯度，解决高光照下的材质-光照混淆问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | IR-HGP：面向高光照场景的物理感知高斯逆渲染与生成先验 |
| 英文题名 | IR-HGP: Physically-Aware Gaussian Inverse Rendering for High-Illumination Scenes via Generative Priors |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_IR-HGP_Physically-Aware_Gaussian_Inverse_Rendering_for_High-Illumination_Scenes_via_Generative_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | IR-HGP |
| Dataset | RelightObj, Mip-NeRF 360 |

> [!tip] 效果简介
> - RelightObj 上，PSNR (Mean) 33.61 vs DiscretizedSDF 32.12 (+1.49)；SSIM (Mean) 0.9761 vs DiscretizedSDF 0.9700 (+0.0061)；LPIPS (Mean) 0.0369 vs DiscretizedSDF 0.0453 (-0.0084)。
> - Mip-NeRF 360 上，PSNR/SSIM/LPIPS 26.92/0.807/0.196 vs Outperforming NVS and inverse rendering baselines (N/A)。

## 概要

高光照场景下的3D高斯泼溅（3DGS）逆渲染面临一个根本瓶颈：**材质与光照的耦合难以分离**。现有3DGS方法缺乏物理可解释性，在高动态范围（HDR）光照条件下，镜面高光和阴影容易被错误地“烘焙”进反射率图中，导致重光照结果失真。

IR-HGP通过三个关键机制打破这一瓶颈：**混合可见性分解（HVD）** 引入显式网格代理进行光线追踪，提供物理正确的可见性与阴影计算；**生成式光照场先验（GIFP）** 利用条件扩散模型为HDR环境光照图提供生成约束，缩小逆渲染的优化空间；**物理感知辐射校正（PARC）** 通过可学习的自适应ACES色调映射稳定HDR损失梯度，消除高光区域的梯度不稳定问题。

在RelightObj数据集上，IR-HGP取得了平均PSNR 33.61、SSIM 0.9761、LPIPS 0.0369的最优结果（Table 1），全面超越**TensoIR**（Jin et al., CVPR 2023）、**GS-IR**（Liang et al., CVPR 2024）、**R3DG**（Gao et al., ECCV 2024）和**DiscretizedSDF**（Zhu et al., ICCV 2025）等基线方法。在Mip-NeRF 360真实场景数据集上同样取得最优指标（Table 3），验证了方法对真实世界复杂光照的鲁棒性。

从方法谱系来看，IR-HGP属于**物理感知的3DGS逆渲染**路线，区别于纯NeRF逆渲染（如TensoIR）和纯3DGS逆渲染（如GS-IR），其核心创新在于将显式几何代理、扩散生成先验与自适应辐射校正三者协同引入高斯表示框架，在保持实时渲染能力（92 FPS）的同时，实现了高光照场景下材质-光照的物理正确分离。

### 高光照场景下的逆渲染困境

逆渲染旨在从多视角图像中恢复场景的固有属性——几何、材质与光照，从而支持自由视点重光照等下游应用。近年来，3D Gaussian Splatting（3DGS）凭借其高保真新视角合成能力与实时渲染速度，成为逆渲染的有力表示。然而，**3DGS在高光照（High-Illumination）场景下面临根本性的物理可解释性缺陷**：其显式点云表示缺乏对光照遮挡的物理建模，导致材质属性（反射率、粗糙度）与光照效果（镜面高光、阴影）在优化过程中相互耦合、难以分离。这一材质-光照混淆问题集中表现为“阴影烘焙”与“高光烘焙”——阴影和镜面高光被错误地编码进反射率图中，而非作为独立的光照分量被正确分解。

### 现有方法的三个缺口

当前逆渲染方法在上述问题上存在三个关键缺口：

1.  **可见性建模缺失**：基于NeRF的方法（如**TensoIR**（Jin et al., CVPR 2023））虽能隐式表示几何，但体渲染的可见性计算精度有限；基于3DGS的方法（如**GS-IR**（Liang et al., CVPR 2024））则普遍采用简化的球谐光照或环境光遮挡近似，无法进行物理正确的光线追踪可见性判定。**R3DG**（Gao et al., ECCV 2024）虽引入了光线追踪，但其可见性仍受限于高斯椭球体的不精确几何代理。

2.  **环境光照先验匮乏**：高光照场景的环境光照图（Environment Map）通常包含复杂的高频细节与极端动态范围。现有方法多采用无约束的球谐系数或启发式初始化来估计环境光照，缺乏有效的正则化先验，导致估计结果模糊、高频丢失，进而加剧材质-光照的解耦误差。**DiscretizedSDF**（Zhu et al., ICCV 2025）虽改进了几何表示，但光照估计仍依赖传统优化，未能引入数据驱动的生成先验。

3.  **HDR优化不稳定**：高动态范围（HDR）渲染值在反向传播时梯度幅度差异极大，直接使用sRGB空间或固定ACES色调映射进行损失计算，容易在极亮区域产生梯度爆炸、在暗部产生梯度消失，导致优化过程不稳定，并最终将光照残差“烘焙”进材质图中。

### 本文动机与核心思路

针对上述缺口，本文提出**IR-HGP**（Physically-Aware Gaussian Inverse Rendering for High-Illumination Scenes via Generative Priors），其核心动机是：**通过引入物理正确的可见性、数据驱动的生成光照先验、以及自适应的辐射校正，构建一个端到端可微的3DGS逆渲染框架，从根本上解决高光照场景下的材质-光照混淆问题。**

具体而言，IR-HGP设计了三个协同模块：

*   **混合可见性分解（HVD）**：利用2D高斯面片与定期抽取的显式TSDF融合网格，进行光线追踪可见性计算，为PBR着色提供物理正确的遮挡判定。
*   **生成式光照场先验（GIFP）**：基于条件扩散模型，通过得分蒸馏采样（SDS）梯度将生成先验注入可学习的环境光照图，约束其位于自然光照流形上。
*   **物理感知辐射校正（PARC）**：采用带可学习单变量曝光参数β的自适应ACES色调映射，在HDR空间中稳定损失梯度，消除烘焙伪影。

通过三者协同，IR-HGP在RelightObj与Mip-NeRF 360等基准上实现了材质-光照分解质量的显著提升，为高光照场景的可重光照3D资产构建提供了新的技术路径。

## 核心方法与创新机理

IR-HGP 的核心创新在于通过三个**物理感知的 changed slots**，系统性地解决了 3DGS 在高光照场景下材质与光照难以解耦的根本瓶颈——即**缺乏物理可解释性导致的镜面高光与阴影烘焙**问题。这三个模块分别从可见性建模、光照先验约束和辐射校正三个维度，构建了物理正确的逆渲染优化空间。

### 混合可见性分解（HVD）：从近似遮挡到物理光线追踪

现有 3DGS 逆渲染方法（如 **GS-IR**（Liang et al., CVPR 2024）、**R3DG**（Gao et al., ECCV 2024））普遍缺乏显式的光照遮挡计算，或仅依赖简化的环境光遮挡/球谐光照近似，导致阴影信息被错误地“烘焙”进材质贴图。IR-HGP 提出的 **HVD 模块**将这一 slot 从“无/近似遮挡”升级为“物理正确的光线追踪可见性”。

其核心机制是**双几何代理的协同**：一方面利用 2D 高斯面片（2DGS）提供高质量的 G-buffer 属性积累（Eq. 1），另一方面在训练过程中每 5000 次迭代定期从高斯场中提取显式 TSDF 融合网格，用于光线追踪计算物理可见性项 $V$。该可见性直接调制 PBR 着色的辐射分解方程（Eq. 2），使得直接光照 $L_{\mathrm{dir}}$ 与间接光照 $L_{\mathrm{ind}}$ 的分离建立在真实的几何遮挡关系之上。消融实验（Fig. 7, Table 2）证实，引入光线追踪可见性后，阴影判断的准确性显著提升，烘焙现象被有效消除。这一设计的代价是网格提取与可见性计算约占训练总时间的 18%，但换取了物理正确性这一核心增益。

### 生成式光照场先验（GIFP）：从无约束优化到扩散模型正则化

传统逆渲染方法对环境光照图的优化通常缺乏有效先验，仅依赖球谐函数等低维表示或启发式初始化，在高光照场景下极易陷入材质-光照的耦合歧义。IR-HGP 的 **GIFP 模块**将这一 slot 从“无约束/弱约束”升级为“基于条件扩散模型的生成先验正则化”。

GIFP 首先通过一个粗糙光照编码器（Eq. 3）从多视角图像中提取低维场景光照特征 $L_{\mathrm{Coarse}}$，作为预训练 HDR 扩散模型 $D_{\mathrm{HDR}}$ 的条件输入。在优化过程中，扩散模型根据当前估计的环境光照图 $\hat{L}_{\mathrm{env}}$ 预测所加噪声（Eq. 4），并通过得分蒸馏采样（SDS）梯度（Eq. 5）将生成先验蒸馏到环境光照图的优化中。这一机制使得估计的环境光照图在保持与输入图像一致性的同时，被约束在真实 HDR 光照分布的流形上。消融实验（Fig. 8, Table 2）表明，GIFP 使估计的环境光照图更接近真实值，并有效减少了高频伪影，提升了漫反射与镜面反射的分离质量。需要注意的是，该模块依赖预训练扩散模型的分布覆盖能力，若场景光照超出训练集分布，可能产生不准确的光照预测（见局限性分析）。

### 物理感知辐射校正（PARC）：从固定色调映射到自适应 HDR 梯度稳定

高光照场景下的逆渲染面临一个被普遍忽视的挑战：直接 sRGB 或固定 ACES 色调映射会导致 HDR 损失梯度不稳定，迫使优化过程将高光信息“烘焙”进材质通道以降低光度损失。**PARC 模块**将色调映射这一 slot 从“固定映射”升级为“带可学习曝光参数的自适应 ACES 映射”。

PARC 的核心是一个单变量可学习曝光参数 $\beta$，它扩展了标准 ACES 色调映射曲线（Eq. 6, Fig. 2a）：当 $\beta=1$ 时退化为标准 ACES，而可学习的 $\beta$ 提供了更精细的高光/阴影控制能力。光度损失在 PARC 校正后的空间中计算（Eq. 7），使得优化过程能够自适应地调整动态范围，避免因固定映射导致的梯度裁剪或饱和。消融实验（Fig. 9, Table 2）表明，PARC 是消除烘焙阴影最有效的单一模块，其产生的反射率图在视觉上最为干净。一个开放问题是，单变量 $\beta$ 是否足以应对极端局部高光区域，未来可能需要与空间变化的色调映射相结合。

### 创新协同：从独立模块到物理正确的优化闭环

三个 changed slots 并非孤立运作，而是形成了**物理正确的逆渲染优化闭环**：HVD 提供物理正确的可见性 $V$，使得 PBR 着色方程（Eq. 8）中的直接/间接光照分解建立在真实的几何遮挡之上；GIFP 为环境光照图提供生成先验约束，防止优化陷入材质-光照耦合的局部最优；PARC 稳定 HDR 损失梯度，确保高光区域的优化信号不被扭曲。三者共同作用于总损失函数（Eq. 9）的优化过程，使得 IR-HGP 在高光照场景下实现了对 **TensoIR**（Jin et al., CVPR 2023）、**DiscretizedSDF**（Zhu et al., ICCV 2025）等基线方法的全面超越（RelightObj 平均 PSNR 33.61 vs. 次优 32.12，Table 1）。

IR-HGP 的整体 pipeline 围绕一个核心矛盾展开：**高光照场景下，3D Gaussian Splatting 的材质与光照耦合难以分离，导致镜面高光和阴影被错误地“烘焙”进材质图**。为解决这一问题，框架将物理正确性显式注入逆渲染的每个关键环节，形成三条协同主线——可见性、光照先验与辐射校正。

### 框架总览

整个优化流程从多视角 HDR 图像输入开始，输出可重光照的 3D 资产（包含反射率、粗糙度、金属度等材质属性，以及 HDR 环境光照图）。如图 3 所示，框架由四个核心模块串联：

1. **混合可见性分解 (HVD)**：将场景表示为 2D Gaussian 面片集合，并定期从中抽取显式表面网格，用于光线追踪计算物理正确的可见性。
2. **PBR 着色**：基于 Cook-Torrance 微表面 BRDF，利用 HVD 提供的可见性项 $V$ 将最终辐射分解为直接光照 $L_{\mathrm{dir}}$ 与间接光照 $L_{\mathrm{ind}}$。
3. **生成式光照场先验 (GIFP)**：引入条件扩散模型，以多视角图像的粗糙光照特征为条件，对可学习 HDR 环境光照图施加生成先验约束。
4. **物理感知辐射校正 (PARC)**：在损失计算前，通过带可学习曝光参数 $\beta$ 的自适应 ACES 色调映射，将 HDR 渲染结果与目标图像映射到稳定梯度空间。

### 数据流与模块协作

**前向渲染流**：输入图像经过 HVD 模块，2D Gaussian 面片通过 alpha 混合合成 G-buffer（包含法线、材质属性等）：

$$\mathbf{X}_{\mathrm{pixel}} = \sum_{i=1}^{N} \mathbf{x}_i T_i \boldsymbol{\alpha}_i$$

同时，HVD 定期抽取的显式网格提供光线追踪可见性 $V$，指导辐射分解：

$$L(\mathbf{p}, \omega_o) = V \cdot L_{\mathrm{dir}}(\mathbf{p}, \omega_o) + L_{\mathrm{ind}}(\mathbf{p}, \omega_o)$$

直接光照部分由可学习 HDR 环境图驱动，通过标准渲染方程积分：

$$L_{\mathrm{dir}}(\mathbf{p},\omega_o) = \int_{\Omega} f_r(\mathbf{p},\omega_i,\omega_o) L_i(\mathbf{p},\omega_i) (\mathbf{n}\cdot\omega_i) d\omega_i$$

其中 BRDF $f_r$ 遵循金属-粗糙度工作流，采用 Cook-Torrance 微表面模型。

**反向优化流**：渲染结果与目标图像在 PARC 校正后的空间中计算光度损失：

$$\mathcal{L}_{\mathrm{c}} = \| \mathcal{C}_{\mathrm{PARC}}(L_{\mathrm{rendered}}, \beta) - \mathcal{C}_{\mathrm{PARC}}(L_{\mathrm{target}}, \beta) \|_1$$

其中 $\mathcal{C}_{\mathrm{PARC}}$ 为自适应 ACES 色调映射：

$$L_{\mathrm{corr}} = \mathcal{C}_{\mathrm{PARC}}(L_{\mathrm{in}}, \beta) = \frac{x(2.51x+0.03)}{x(2.43x+0.59)+0.14}, \quad x = L_{\mathrm{in}} \cdot \beta$$

可学习参数 $\beta$ 使色调映射曲线能够自适应场景动态范围——如图 2 所示，相比固定 ACES 映射（$\beta=1$），PARC 在高光与阴影区域提供更精细的控制，避免将高光/阴影烘焙进材质图。

同时，GIFP 模块对可学习环境图施加生成正则化：先通过粗糙光照编码器从多视角图像提取条件特征 $L_{\mathrm{Coarse}}$，再利用预训练条件扩散模型 $D_{\mathrm{HDR}}$ 预测噪声，并以 SDS 梯度形式蒸馏生成先验：

$$\nabla_{\hat{L}_{\mathrm{env}}} \mathcal{L}_{\mathrm{g}} \propto (\mathbf{z}_{\mathrm{pred}} - \mathbf{z})$$

**总损失函数**为四项加权组合：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{c}} + \lambda_{\mathrm{g}} \mathcal{L}_{\mathrm{g}} + \lambda_n \mathcal{L}_n + \lambda_{\mathrm{smooth}} \mathcal{L}_{\mathrm{smooth}}$$

其中 $\mathcal{L}_n$ 为法线正则化损失，$\mathcal{L}_{\mathrm{smooth}}$ 为材质平滑损失。

### 模块间因果机制

三个核心模块各自解决高光照逆渲染中的一个瓶颈，且互为补充：

- **HVD** 解决“可见性缺失”问题：传统 3DGS 方法缺乏显式遮挡判断，导致阴影被错误解释为材质暗色。HVD 通过光线追踪可见性 $V$ 将遮挡信息显式注入渲染方程，从物理层面切断材质-光照混淆。
- **GIFP** 解决“光照歧义”问题：高光照场景中，镜面高光与漫反射的边界模糊，仅靠光度损失难以正确分离。扩散模型的生成先验约束了环境光照图的空间，使其趋向真实分布，从而提升漫反射/镜面反射分离质量。
- **PARC** 解决“梯度不稳定”问题：HDR 图像的高动态范围使直接 sRGB 映射产生梯度截断或爆炸。PARC 通过可学习 $\beta$ 自适应压缩动态范围，稳定端到端优化，从数值层面消除残余的烘焙伪影。

消融实验（Table 2, Fig 7-9）验证了这一因果链条：HVD 提供了准确的可见性判断，GIFP 使估计环境图更接近真实值，PARC 则产出了视觉上最干净的反射率图。三者叠加实现了从“物理可见性→光照先验→数值稳定”的完整闭环。

![[assets/figures/papers/paper_list_l2524_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_IR_HGP_Physicall/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our framework. Our Hybrid Visibility Decomposition (HVD) yields 2D Gaussian surfels and an explicit mesh. The mesh provides physically-accurate ray-traced visibility. This visibility modulates the PBR shading, which is lit by an HDR map. Our Generative Illumination Field Prior (GIFP) regularizes this map. Finally, the Physics-Aware Radiance Correction (PARC) module uses a single learnable exposure*

IR-HGP 围绕三个核心模块构建，分别解决高光照场景逆渲染中的可见性、光照先验和辐射校正问题。以下逐一展开其设计动机、数学形式与作用机制。

### 3.1 混合可见性分解（HVD）

**动机**：传统3DGS逆渲染方法缺乏物理正确的可见性判断，导致阴影和高光被错误地“烘焙”进材质图中。HVD 的目标是在保持3DGS实时渲染优势的前提下，引入显式的光线追踪可见性。

**核心设计**：HVD 将场景分解为两个互补的表示：
- **2D高斯面片集合** $\mathcal{G}$：负责高效的微分渲染和属性（法线、材质参数）优化；
- **显式网格代理** $\mathcal{M}$：从2DGS面片中周期性提取，专门用于光线追踪可见性计算。

**G-buffer积累**：2D高斯面片的属性通过alpha混合合成像素级G-buffer：

$$\mathbf{X}_{\mathrm{pixel}} = \sum_{i=1}^{N} \mathbf{x}_i T_i \boldsymbol{\alpha}_i$$

其中 $\mathbf{x}_i$ 为第 $i$ 个面片的属性向量（包含法线、漫反射率、粗糙度等），$T_i$ 为累积透射率，$\boldsymbol{\alpha}_i$ 为alpha值。这一过程将显式几何与可微渲染桥接起来。

**辐射分解**：利用HVD计算的物理可见性 $V$，将最终辐射分解为直接光照与间接光照：

$$L(\mathbf{p}, \omega_o) = V \cdot L_{\mathrm{dir}}(\mathbf{p}, \omega_o) + L_{\mathrm{ind}}(\mathbf{p}, \omega_o)$$

这里 $V \in \{0, 1\}$ 由网格代理的光线追踪结果决定，使得阴影和镜面高光的位置完全由物理几何决定，而非由优化过程“猜测”。消融实验（Figure 7, Table 2）证实，HVD模块显著提升了光照判断的准确性，消除了阴影/高光的烘焙现象。

**工程细节**：网格代理每5k次训练迭代提取一次，网格提取和可见性计算约占总训练时间的18%（Sec 4.1-4.2），这是为换取物理正确可见性所做的必要权衡。

### 3.2 生成式光照场先验（GIFP）

**动机**：高光照场景下，从稀疏视角估计HDR环境光照图是一个高度欠定问题。无约束的球谐光照或启发式初始化容易陷入局部最优，导致材质-光照混淆。GIFP 利用预训练的扩散模型为环境光照图提供强生成先验。

**粗糙光照编码**：首先从多视角图像 $\{\mathbf{I}_i\}_{i=1}^{N}$ 中提取低维场景光照特征，作为扩散模型的条件信号：

$$L_{\mathrm{Coarse}} = \operatorname{Encoder}(\{\mathbf{I}_i\}_{i=1}^{N})$$

**扩散噪声预测**：条件扩散模型 $D_{\mathrm{HDR}}$ 根据粗糙光照特征预测当前噪声步 $t$ 下的噪声：

$$\mathbf{z}_{\mathrm{pred}} = D_{\mathrm{HDR}}\big( \hat{L}_{\mathrm{env}}^{(t)}, t \mid L_{\mathrm{Coarse}}\big)$$

其中 $\hat{L}_{\mathrm{env}}^{(t)}$ 为当前优化的环境光照图在扩散时间步 $t$ 的加噪版本。

**SDS梯度估计**：借鉴Score Distillation Sampling（SDS），通过预测噪声与真实噪声的差值来近似生成损失相对于环境光照图的梯度：

$$\nabla_{\hat{L}_{\mathrm{env}}} \mathcal{L}_{\mathrm{g}} \propto (\mathbf{z}_{\mathrm{pred}} - \mathbf{z})$$

这一梯度在优化过程中持续将环境光照图拉向扩散先验所定义的自然光照分布，从而抑制高频伪影并提升漫反射/镜面反射分离质量（Figure 8, Table 2）。

### 3.3 物理感知辐射校正（PARC）

**动机**：HDR场景的线性辐射值范围极大，直接使用sRGB或固定ACES色调映射会导致高光区域梯度消失或裁剪，进而使优化过程将高光信息错误地嵌入材质图中。

**自适应ACES映射**：PARC 引入带可学习曝光参数 $\beta$ 的自适应ACES色调映射函数：

$$L_{\mathrm{corr}} = \mathcal{C}_{\mathrm{PARC}}(L_{\mathrm{in}}, \beta) = \frac{x(2.51x+0.03)}{x(2.43x+0.59)+0.14}$$

其中 $x = L_{\mathrm{in}} \cdot \beta$。当 $\beta = 1$ 时退化为标准ACES曲线；$\beta$ 的可学习性使得映射曲线能够动态适应不同场景的HDR范围（Figure 2）。

![[assets/figures/papers/paper_list_l2524_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_IR_HGP_Physicall/figures/002_Figure_2.jpg]]
*Figure 2: (a) Comparison of Tone Mapping Curves. Our modified ACES curve (controlled by β) is an extension of the standard curve (β = 1). It provides finer HDR tone mapping, offering enhanced highlight/shadow control while also avoiding clipping artifacts from naive sRGB conversion. (b) Rendering Effect of Tone Mapping Curves. As visualized, our work avoids baking shadows or highlights into the material map, unlike the direct sRGB transform*

**PARC光度损失**：在PARC校正后的空间中计算L1损失，确保HDR梯度稳定传播：

$$\mathcal{L}_{\mathrm{c}} = \| \mathcal{C}_{\mathrm{PARC}}(L_{\mathrm{rendered}}, \beta) - \mathcal{C}_{\mathrm{PARC}}(L_{\mathrm{target}}, \beta) \|_1$$

消融实验（Figure 9, Table 2）表明，PARC模块通过可学习动态范围参数，最有效地消除了烘焙阴影，获得了视觉上最干净的反射率图。

### 3.4 PBR着色与优化

**直接光照渲染**：采用标准Cook-Torrance微表面BRDF $f_r$ 和金属-粗糙度工作流，直接光照由渲染方程计算：

$$L_{\mathrm{dir}}(\mathbf{p},\omega_o) = \int_{\Omega} f_r(\mathbf{p},\omega_i,\omega_o) L_i(\mathbf{p},\omega_i) (\mathbf{n}\cdot\omega_i) d\omega_i$$

其中 $L_i$ 由GIFP模块优化的HDR环境光照图提供，可见性 $V$ 由HVD模块提供。

**总损失函数**：端到端优化的目标函数为四个损失项的加权组合：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{c}} + \lambda_{\mathrm{g}} \mathcal{L}_{\mathrm{g}} + \lambda_n \mathcal{L}_n + \lambda_{\mathrm{smooth}} \mathcal{L}_{\mathrm{smooth}}$$

其中 $\mathcal{L}_{\mathrm{c}}$ 为PARC颜色损失，$\mathcal{L}_{\mathrm{g}}$ 为SDS生成损失，$\mathcal{L}_n$ 为法线一致性损失，$\mathcal{L}_{\mathrm{smooth}}$ 为材质平滑正则项。各权重系数通过实验调优确定。

## 实验与关键发现

### 实验设置

实验在**RelightObj**基准上评估，包含10个多样化3D物体（6个来自NeRF Synthetic，4个来自Shiny Blender），每个物体在6种HDR环境光照下渲染，共60组配置。每组配置使用100张多视角图像训练，200张新视角图像测试。所有方法均在单块NVIDIA RTX 4090 GPU上以相同配置评估。IR-HGP训练耗时约1.5小时，渲染速度达92 FPS——慢于GS-IR（208 FPS）但快于R3DG（51 FPS），在速度与真实感之间取得了平衡。HVD模块的网格提取与光线追踪可见性计算约占总训练时间的18%，这是为换取物理正确可见性所做的必要权衡。

### 主结果：RelightObj数据集

Table 1展示了RelightObj上的重光照定量对比。IR-HGP在所有指标上达到最优：平均PSNR **33.61**（较次优的DiscretizedSDF提升+1.49）、SSIM **0.9761**（+0.0061）、LPIPS **0.0369**（−0.0084），全面超越**TensoIR**（Jin et al., CVPR 2023）、**GS-IR**（Liang et al., CVPR 2024）、**R3DG**（Gao et al., ECCV 2024）和**DiscretizedSDF**（Zhu et al., ICCV 2025）等基线方法。这一优势源于三个核心模块的协同作用：HVD提供物理正确的可见性判断，消除了阴影/高光烘焙到材质图中的错误；GIFP利用扩散生成先验使估计的环境光照图更接近真实值；PARC通过自适应色调映射稳定HDR优化梯度。

定性结果（Figure 5, Figure 6）进一步验证：IR-HGP估计的环境光照图在细节和色彩保真度上明显优于基线；重光照结果中，基于NeRF的方法（如TensoIR）细节模糊，而基于3DGS的方法（如GS-IR）存在材质-光照耦合伪影，IR-HGP则实现了更干净的材质与光照分离。

![[assets/figures/papers/paper_list_l2524_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_IR_HGP_Physicall/figures/007_Figure_6.jpg]]
*Figure 6: Relighting results. Our method can provide more detailed relighting results than NeRF-based methods. We also alleviate the artifacts of Gaussian-based methods by achieving a better decoupling of material and illumination*

![[assets/figures/papers/paper_list_l2524_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_IR_HGP_Physicall/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparisons of the estimated environment maps for different objects*

### 主结果：Mip-NeRF 360数据集

在真实世界复杂光照场景的Mip-NeRF 360数据集上（Table 3），IR-HGP同样取得最优指标（PSNR 26.92 / SSIM 0.807 / LPIPS 0.196），在存在传感器噪声的条件下仍同时超越新视角合成和逆渲染基线。这验证了方法对真实世界高光照场景的鲁棒性。

![[assets/figures/papers/paper_list_l2524_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_IR_HGP_Physicall/figures/012_Table_3.jpg]]
*Table 3: Quantitative results on Mip-NeRF 360. IR-HGP achieves superior metrics, outperforming both NVS and inverse rendering baselines despite real-world sensor noise. ( 1st , 2nd , 3rd )*

### 消融实验

Table 2和Figure 7-9展示了逐模块消融结果，每个模块的增益稳定且显著：

- **HVD模块**（Figure 7）：移除光线追踪可见性后，模型退化为简化的环境光遮挡近似，导致阴影/高光被错误烘焙到反射率图中。HVD通过2D高斯面片的法线优势和显式网格的光线追踪可见性，实现了准确的照明判断。
- **GIFP模块**（Figure 8）：移除扩散生成先验后，环境光照图估计质量下降，出现高频伪影，漫反射/镜面反射分离质量降低。GIFP的条件扩散模型为HDR环境光照图提供了强先验约束，使其更接近真实值。
- **PARC模块**（Figure 9）：移除可学习曝光参数β或退化为固定ACES映射时，高光区域出现明显的阴影烘焙。完整的PARC模块通过自适应动态范围参数，产生了视觉上最干净的反射率图，这是消除烘焙阴影最有效的单一组件。

![[assets/figures/papers/paper_list_l2524_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_IR_HGP_Physicall/figures/009_Figure_8.jpg]]
*Figure 8: Ablation study on GIFP. The diffusion-based generative constraint brings our learnable environment map closer to the ground truth*

### 局限性

尽管IR-HGP在重光照质量上取得显著提升，仍存在以下局限：

1. **生成先验的分布依赖**：GIFP模块依赖预训练的扩散模型，若场景光照分布超出训练集覆盖范围，可能产生不准确的光照预测，影响逆渲染的物理正确性。
2. **渲染速度权衡**：92 FPS的实时渲染速度虽优于R3DG（51 FPS），但与纯3DGS逆渲染方法GS-IR（208 FPS）相比有所下降，这是引入网格提取和光线追踪可见性的性能代价。
3. **大规模场景瓶颈**：HVD模块定期抽取网格并计算光线追踪可见性（约占训练时间18%），在超大规模城市场景中，网格抽取和存储可能成为新的瓶颈。

## 定位与知识库关联

### 3DGS逆渲染的方法谱系

IR-HGP处于基于3D Gaussian Splatting（3DGS）的逆渲染研究脉络中，该脉络的核心挑战始终是**材质与光照的解耦**。早期的NeRF类方法如**TensoIR**（Jin et al., CVPR 2023）通过张量分解实现了场景属性的隐式建模，但其体积渲染框架在高光照场景下难以产生清晰的镜面反射分离。3DGS的引入带来了实时渲染的优势，但也暴露了新的瓶颈：高斯椭球体缺乏明确的表面定义，导致可见性判断模糊，材质与光照的耦合难以物理正确地分离。

在3DGS逆渲染的演进中，**GS-IR**（Liang et al., CVPR 2024）率先将法线损失引入优化过程，试图通过几何约束改善材质估计，但其可见性建模仍停留在简化的环境光遮挡层面。**R3DG**（Gao et al., ECCV 2024）进一步引入光线追踪进行直接光照计算，迈出了物理正确渲染的关键一步，但其环境光照仍依赖无约束的球谐函数表示，在高光照场景下容易产生错误的镜面高光烘焙。**DiscretizedSDF**（Zhu et al., ICCV 2025）通过离散符号距离场改善了表面重建精度，但同样缺乏对光照先验的有效约束。

IR-HGP在这一谱系中的定位是**物理感知的生成式逆渲染**。其核心突破在于同时解决了三个此前方法未能有效处理的关键问题：（1）通过混合可见性分解（HVD）实现了物理正确的光线追踪可见性计算；（2）通过生成式光照场先验（GIFP）为HDR环境光照提供了数据驱动的正则化约束；（3）通过物理感知辐射校正（PARC）稳定了高动态范围场景下的优化梯度。

### 知识库定位：物理渲染与生成模型的交叉

从知识库的角度，IR-HGP的工作位于**物理渲染**、**3D高斯表示**和**生成模型**三个领域的交叉点。

在物理渲染维度，IR-HGP继承了基于物理的渲染（PBR）管线的成熟理论，包括Cook-Torrance微表面BRDF模型、金属-粗糙度工作流以及直接/间接光照分解。与纯图形学方法不同的是，IR-HGP将这些物理约束嵌入到可微分渲染管线中，使其能够从多视角图像中端到端地优化场景属性。HVD模块中定时抽取显式网格进行光线追踪的做法，本质上是在神经表示与经典几何处理之间建立了桥梁——这一设计借鉴了计算机图形学中代理几何体的思想，但将其与可学习的2D高斯面片动态耦合。

在生成模型维度，GIFP模块将条件扩散模型的生成先验引入逆渲染优化，这一思路与Score Distillation Sampling（SDS）在文本到3D生成中的成功应用一脉相承。IR-HGP的创新在于将SDS梯度从3D资产生成迁移到环境光照图的优化中，并通过粗糙光照编码器从多视角图像中提取条件特征，使扩散模型能够感知场景的光照分布。这一设计使得逆渲染不再仅依赖像素级重建损失，而是获得了来自大规模HDR图像数据集的语义级光照先验。

在3D高斯表示维度，IR-HGP采用2D高斯面片（2DGS）而非传统的3D高斯椭球体，这一选择直接服务于物理渲染的需求：2DGS的平面结构天然提供了明确的法线方向，与PBR着色管线中的法线计算无缝衔接。同时，2DGS的alpha混合机制使得G-buffer（包括反照率、粗糙度、法线等）的合成具有物理可解释性。

### 适用边界与局限

**适用场景**：IR-HGP在以下条件下表现最优——（1）场景具有明确的高动态范围光照，如室外强光或室内多光源环境；（2）物体材质以金属-粗糙度模型可描述的表面为主；（3）训练视角覆盖充分，能够为网格提取提供足够的几何信息。在RelightObj数据集（10个物体×6种HDR环境）和Mip-NeRF 360真实场景上的实验表明，该方法对合成数据和真实传感器噪声均具有鲁棒性。

**已知局限**：

1. **生成先验的分布依赖性**：GIFP模块依赖于预训练的HDR扩散模型，若场景光照分布（如极端非自然光谱或特殊艺术化光照）超出训练集分布，扩散模型可能产生不准确的光照预测，进而误导逆渲染的物理正确性。这一局限本质上是数据驱动先验的固有边界。

2. **渲染速度的权衡**：尽管IR-HGP实现了92 FPS的实时渲染，但与纯3DGS方法如GS-IR（208 FPS）相比存在明显下降。这一性能开销主要来自HVD模块的网格提取和光线追踪可见性计算，占总训练时间的约18%。对于需要极致渲染速度的应用（如移动端实时重光照），这一开销可能构成瓶颈。

3. **大规模场景的可扩展性**：HVD模块定期（每5k迭代）从高斯面片中抽取显式网格，这一操作的内存和计算开销随场景规模线性增长。在面对超大规模城市场景或动态场景时，网格的频繁更新和存储可能成为新的瓶颈。论文未在超过Mip-NeRF 360规模的数据集上进行验证。

4. **动态光照与可变形物体的泛化**：当前框架假设场景光照和几何在训练期间保持静态。对于动态照明场景（如移动光源）或非刚性物体（如可变形衣物），HVD的网格更新策略和GIFP的光照先验能否有效泛化仍是开放问题。

### 开放问题

1. **生成光照先验的时空扩展**：GIFP当前仅处理静态HDR环境光照，能否将其扩展到动态照明场景（如包含时间维度的光照变化）或空间变化的光照条件（如室内多光源场景），以支持更通用的可重光照3D资产构建？

2. **可见性计算的效率提升**：HVD模块中定期提取网格的耗时占比较高（约18%），是否可以通过神经隐式可见性场替代显式网格，或采用增量式网格更新策略来降低计算开销？这对大规模场景的实用性至关重要。

3. **自适应色调映射的空间泛化**：PARC模块使用单变量曝光参数β进行全局色调映射校正，但极端局部高光区域（如金属表面的镜面反射峰值）可能需要空间变化的色调映射策略。将PARC与局部自适应机制结合是否能够进一步改善高光区域的材质-光照解耦质量？

4. **多模态先验的融合**：当前仅使用扩散模型提供光照先验，是否可以将语言引导或物理约束（如光源类型、色温范围）作为额外的先验条件，使逆渲染在稀疏输入或歧义场景下更加鲁棒？

## 原文 PDF

![[paperPDFs/CVPR_2026/IR_HGP_Physically_Aware_Gaussian_Inverse_Rendering_for_High_Illumination_Scenes_via_Generative_Priors.pdf]]
