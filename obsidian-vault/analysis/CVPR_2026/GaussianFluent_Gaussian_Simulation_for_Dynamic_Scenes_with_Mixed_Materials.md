---
title: "GaussianFluent: Gaussian Simulation for Dynamic Scenes with Mixed Materials"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GaussianFluent_Gaussian_Simulation_for_Dynamic_Scenes_with_Mixed_Materials.pdf
project_link: "https://hb-pencil-zero.github.io/GaussianFluent/"
code_link: null
aliases:
- GaussianFluent
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 引入基于生成模型的内部高斯填充与多轴迭代纹理精化（无需额外训练数据），结合优化的连续损伤MPM（正则化回归映射+GPU并行）以及混合材料参数分配，使GS能够真实模拟脆性断裂、流体等复杂动态。
primary_logic: 通过将预训练图像生成模型与物理仿真深度融合，利用大模型先验合成多视图一致的内部纹理，并改进CD-MPM以消除回归映射的不连续性并实现GPU加速，从而在统一框架下实现从弹性变形到脆性断裂、从固体到流体的高保真动态场景仿真与渲染。
claims:
- 内部填充与纹理生成：定量对比（表1），CLIP分数大幅领先（35.4 vs 22.3/30.1），用户偏好达71.43%，定性（图6）内部结构清晰。
- 动态场景仿真：表2显示本文CLIP分数（22.7 vs 12.2/13.1）和用户偏好（88.46%）均显著优于基线；图5、图7验证混合材料断裂的真实性。
- GPU并行化将模拟从单帧4分钟降至1秒量级，支持交互式复杂场景（表A1）。
- 优化的CD-MPM回归映射消除了原算法在p=p0处的跳跃不连续性，保证了数值稳定性（图A1、式6及相关推导）。
---

# GaussianFluent: Gaussian Simulation for Dynamic Scenes with Mixed Materials

> [!tip] 核心洞察
> 通过将预训练图像生成模型与物理仿真深度融合，利用大模型先验合成多视图一致的内部纹理，并改进CD-MPM以消除回归映射的不连续性并实现GPU加速，从而在统一框架下实现从弹性变形到脆性断裂、从固体到流体的高保真动态场景仿真与渲染。

| 字段 | 内容 |
|------|------|
| 中文题名 | GaussianFluent：面向混合材料动态场景的高斯物理仿真 |
| 英文题名 | GaussianFluent: Gaussian Simulation for Dynamic Scenes with Mixed Materials |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.09265) · [Project](https://hb-pencil-zero.github.io/GaussianFluent/) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | GaussianFluent |
| Dataset | Internal Texture Filling, Dynamic Scene Simulation |

> [!tip] 效果简介
> - Internal Texture Filling 上，CLIP Score 35.4 vs PhysGaussian 22.3 / 2D Inpainting 30.1 (+13.1 over PhysGaussian; +5.3 over 2D Inpainting)；User Study (Preference) 71.43% (60/84) vs PhysGaussian 3.57% / 2D Inpainting 25.00% (+67.86% over PhysGaussian; +46.43% over 2D Inpainting)。
> - Dynamic Scene Simulation 上，CLIP Score 22.7 vs PhysGaussian 12.2 / OmniPhysGS 13.1 (+10.5 over PhysGaussian; +9.6 over OmniPhysGS)；User Study (Preference) 88.46% (23/26) vs PhysGaussian 3.84% / OmniPhysGS 7.69% (+84.62% over PhysGaussian; +80.77% over OmniPhysGS)。

## 概要

**问题背景** 3D Gaussian Splatting（3DGS）在静态场景新视图合成中取得了显著进展，但其在动态场景物理仿真中面临两个根本性瓶颈：（1）3DGS仅建模物体表面，内部为空心，缺乏体积表示和多视图一致的内部纹理；（2）现有基于GS的物理仿真方法（如PhysGaussian及OmniPhysGS）受限于纯弹性材料模型，无法处理脆性断裂、材料混合及拓扑变化。此外，原生连续损伤物质点法（CD-MPM）的回归映射在体积拉伸量 $p=p_0$ 处存在跳跃不连续性，导致数值不稳定，且CPU实现严重制约性能。

**核心方法** GaussianFluent 提出了一套深度融合生成模型与物理仿真的统一框架，核心创新包括：（1）**内部高斯体积填充**——基于密度场初始化与透明度优化生成封闭的内部高斯体积，无需额外训练数据；（2）**多视图一致内部纹理生成**——利用预训练图像生成模型（MVInpainter + SD-XL）通过单视图修复初始化与迭代三轴精化，合成多视图一致的内部纹理；（3）**优化的CD-MPM物理仿真**——引入基于 $k$ 阶多项式的动态中心点正则化回归映射，消除原算法的不连续性并保证数值稳定，同时通过NVIDIA Warp实现GPU并行化，将单帧模拟从分钟级降至秒级；（4）**混合材料支持**——为不同部件（如果皮、果肉、种子）分配不同的损伤参数 $\beta$，实现符合物理的脆性断裂模式；（5）**动态光照渲染**——集成基于PCA法线估计的Blinn-Phong光照模型，支持动态光源与阴影。

**核心结论** 实验表明，GaussianFluent 在内部纹理填充上CLIP分数达到35.4，较PhysGaussian（22.3）提升13.1，用户偏好率达71.43%；在动态场景仿真上CLIP分数为22.7，较PhysGaussian（12.2）和OmniPhysGS（13.1）分别提升10.5和9.6，用户偏好率高达88.46%。定性结果展示了从弹性变形到脆性断裂、从固体到流体的高保真动态场景仿真与渲染能力。

**方法定位** GaussianFluent 在3DGS物理仿真方法谱系中首次实现了内部纹理合成与脆性断裂的统一建模：相较于PhysGaussian的纯弹性框架和OmniPhysGS的自动参数估计但无断裂支持，本方法通过改进CD-MPM的数值稳定性与GPU并行化，将GS物理仿真的适用范围从弹性变形拓展至断裂、切片等复杂动态，同时借助大模型先验解决了内部纹理的多视图一致性问题。



### 3D高斯泼溅与动态场景仿真的交汇

3D高斯泼溅（3D Gaussian Splatting, 3DGS）凭借其显式点基元表示和可微光栅化管线，在高保真静态场景重建与实时渲染领域取得了显著突破。然而，当研究者试图将3DGS从静态“快照”推向动态物理世界时，一个根本性瓶颈浮现：**3DGS的原始表示仅捕获物体表面信息，其内部是空心的**。这意味着，一旦物体发生断裂、切割或塑性变形，暴露出的内部区域将呈现空白或错误的纹理，严重破坏视觉真实感。

现有的3DGS物理仿真方法，如 **PhysGaussian** 和 **OmniPhysGS**，尝试将物质点法（Material Point Method, MPM）与高斯泼溅结合，实现了弹性体的变形仿真。但它们存在三个关键局限：

1. **物理模型单一**：仅支持纯弹性材料，无法处理脆性断裂、塑性流动等更丰富的物理现象。PhysGaussian框架本身不具备损伤模型，当应力超过材料强度时无法产生真实的裂纹和破碎效果。
2. **内部纹理缺失**：PhysGaussian采用“直接颜色拷贝”策略——将表面高斯的颜色复制给内部粒子，导致内部纹理模糊且缺乏真实结构（Table 1中CLIP分数仅22.3）。而2D修复方法虽能生成局部纹理，却缺乏多视图一致性，在倾斜视角下失效。
3. **数值稳定性与计算效率不足**：原生连续损伤MPM（CD-MPM）的回归映射（return mapping）在体积拉伸量 $p = p_0$ 处存在跳跃不连续性，导致仿真过程数值不稳定。同时，现有实现基于CPU，单帧模拟耗时数分钟，无法支撑交互式应用。

### 核心矛盾：从“表面壳”到“实体体”的跨越

上述问题指向同一个深层矛盾：**3DGS的显式表面表示与物理仿真所需的连续体表示之间存在语义鸿沟**。物理仿真需要物体具备完整的体积填充、一致的材料属性和可计算的内部应力-应变场，而原生3DGS仅提供一组离散的表面高斯。弥合这一鸿沟需要同时解决三个子问题：

- **体积填充**：如何在3DGS内部生成封闭、均匀的高斯体积，为仿真提供物质载体？
- **纹理合成**：如何为内部高斯赋予多视图一致的逼真纹理，使得断裂后暴露的内部结构与表面无缝衔接？
- **物理增强**：如何将脆性断裂、混合材料等复杂本构行为融入3DGS框架，并保证数值稳定与计算实时性？

### 本文动机与解决思路

**GaussianFluent** 正是针对上述矛盾提出的统一解决方案。其核心洞察在于：**将预训练图像生成模型与优化的连续损伤物理仿真深度融合，利用大模型先验合成多视图一致的内部纹理，同时改进CD-MPM以消除回归映射的不连续性并实现GPU并行加速**。

具体而言，GaussianFluent从三个层面突破现有瓶颈：

- **内部表示构建**：通过密度场阈值初始化内部高斯体积，结合透明度优化使表面平滑，再借助预训练生成模型（MVInpainter + Stable Diffusion XL）进行迭代多轴纹理精化，无需额外训练数据即可生成多视图一致的内部纹理。
- **物理模型升级**：引入优化的连续损伤MPM，支持NACC屈服面和损伤变量 $\alpha$ 驱动的脆性断裂。通过动态中心点正则化（Equation 6）消除回归映射在 $p = p_0$ 处的不连续性，并基于NVIDIA Warp实现GPU并行化，将单帧模拟从分钟级降至秒级（Table A1）。
- **混合材料支持**：允许为不同部件（如果皮、果肉、种子）分配不同的材料参数 $\beta$，实现更真实的差异化断裂行为（Figure 5）。

这一设计使得GaussianFluent能够在统一框架下，实现从弹性变形到脆性断裂、从固体到流体（通过 $p_0 \to 0$ 退化）的高保真动态场景仿真与渲染，并支持动态光照下的实时交互。



## 核心方法与创新机理

GaussianFluent 的核心突破在于将 **3D Gaussian Splatting（3DGS）从“表面壳”扩展为具有内部体积表示的物理实体**，并通过深度改进物理模型与计算后端，首次在统一框架下实现了从弹性变形到脆性断裂、从固体到流体的高保真动态场景仿真与渲染。其创新可归纳为三个紧密耦合的维度。

### 1. 内部体积表示与多视图一致纹理生成

现有 3DGS 物理仿真方法（如 **PhysGaussian** 和 **OmniPhysGS**）仅维护物体表面高斯，内部空心且无纹理，一旦发生断裂或切割即暴露空洞，严重破坏视觉真实感。GaussianFluent 从根本上改变了这一表示范式：

- **内部高斯填充**：首先通过密度场阈值初始化内部高斯体积——对空间任意点 $\mathbf{x}$，计算其密度 $d(\mathbf{x}) = \sum_{p \in P} \alpha_p \exp\big(-\frac{1}{2}(\mathbf{x} - \mathbf{x}_p)^T \mathbf{A}_p^{-1} (\mathbf{x} - \mathbf{x}_p)\big)$（式 2），将密度高于阈值的网格中心作为新高斯位置。随后执行仅优化透明度的精化步骤，并剪枝近零透明度的高斯，最终得到封闭、平滑的内部高斯体积（图 2）。

- **训练无关的多视图纹理生成**：这是连接大模型先验与物理仿真的关键创新。方法分为两阶段：（1）**单视图修复初始化**——利用 MVInpainter 和 Stable Diffusion XL 对六个正交视点进行内部纹理修复，生成粗纹理；（2）**迭代多轴精化**——沿三轴交替执行修复与 GS 优化，使纹理在多个视点间保持一致。定量结果显示，该方法在 CLIP 分数上达到 **35.4**，远超 PhysGaussian 的 22.3 和 2D Inpainting 的 30.1；用户偏好高达 **71.43%**（表 1）。定性对比（图 6）表明，PhysGaussian 的直接颜色拷贝导致内部模糊，2D Inpainting 在斜视点失效，而本文方法生成的内部结构清晰且多视图一致。

### 2. 优化的连续损伤 MPM 与混合材料仿真

PhysGaussian 仅支持纯弹性 MPM，无法处理脆性断裂和拓扑变化。GaussianFluent 引入连续损伤 MPM（CD-MPM）并做出两项关键改进：

- **连续回归映射**：原生 CD-MPM 的回归映射在 $p = p_0$ 处存在跳跃不连续性，导致数值不稳定。本文通过引入基于 $k$ 阶多项式的动态中心点 $p'_c = p_c + \phi_k(p^{\mathrm{tr}})(p^{\mathrm{tr}} - p_c)$（式 6），其中 $\phi_k(p^{\mathrm{tr}}) = |\frac{p^{\mathrm{tr}} - p_c}{p_0 - p_c}|^k$，取 $k=2$，将试应力平滑投影到 NACC 屈服面 $y(p,q;p_0,\beta,M) = q^2(1+2\beta) + M^2(p+\beta p_0)(p-p_0)$ 上，彻底消除了不连续性（图 A1），保证了塑性修正的数值稳定性。

- **混合材料参数分配**：不同于基线方法对整个物体使用统一的材料参数 $\beta$，GaussianFluent 允许为不同部件分配独立 $\beta$ 值。以西瓜为例（图 5），果皮、果肉、种子分别赋予 $\beta = 2, 0.6, 5$，产生符合物理直觉的差异断裂模式，而统一 $\beta$ 设置则导致不真实的均匀碎裂。

物理仿真通过 P2G→网格更新→G2P 迭代进行，计算变形梯度 $\mathbf{F}_p(t) = \frac{\partial \varphi(\mathbf{X}, t)}{\partial \mathbf{X}}$（式 5），并更新损伤变量 $\alpha$ 驱动断裂。仿真结果随后映射到 GS 属性（位置、协方差、SH 旋转）以更新渲染表示。

### 3. GPU 并行化与动态光照渲染

- **GPU 加速**：原生 CD-MPM 基于 CPU 实现，单帧模拟耗时数分钟。GaussianFluent 利用 NVIDIA Warp 将整个仿真管线 GPU 并行化，将单帧时间降至秒级（表 A1），使交互式复杂场景仿真成为可能。

- **Blinn-Phong 动态光照**：引入基于 PCA 法线估计的 Blinn-Phong 光照模型 $\mathbf{L}_i = \mathbf{c}_0 \odot \mathbf{I}_a + \sum_m T_{i,m} (\mathbf{c}_0 \odot \mathbf{I}_{L,m}) \frac{1}{r_m^2} (D_m + S_m)$（式 A20），支持动态光源与阴影，使同一场景在不同光照条件下呈现真实光影变化（图 1、图 A3）。尺度正则化项 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{MSE}} + \mathcal{L}_{\mathrm{SSIM}} + \lambda \sum_{i=1}^{N} \|\mathbf{s}_i\|_2^2$（式 1）在初始 GS 训练中促使高斯致密化，为后续 PCA 法线估计提供更准确的表面几何。

### 创新总结

上述三个维度的创新形成闭环：内部体积表示为断裂提供物质基础，多视图纹理生成保证断裂面视觉真实，优化的 CD-MPM 提供数值稳定的物理驱动，GPU 并行化使实时交互成为可能，动态光照则增强场景表现力。定量证据表明，在动态场景仿真中，GaussianFluent 的 CLIP 分数（**22.7**）和用户偏好（**88.46%**）均大幅领先 PhysGaussian（12.2 / 3.84%）和 OmniPhysGS（13.1 / 7.69%）（表 2），验证了各创新模块的协同增益。



GaussianFluent 构建了一条从静态表面高斯到可物理仿真的体积表示的完整流水线，其核心设计围绕一个关键瓶颈展开：原生 3DGS 缺乏内部体积表示与多视图一致的内部纹理，且现有 GS 物理仿真方法（如 **PhysGaussian**）仅支持弹性变形，无法处理脆性断裂、材料混合及拓扑变化。该框架通过将预训练图像生成模型与优化的连续损伤物质点法（CD-MPM）深度融合，在统一框架下实现了从弹性变形到脆性断裂、从固体到流体的高保真动态场景仿真与渲染。

### 流水线总览

整体流水线如图 3 所示，由三大阶段构成，各阶段之间存在明确的输入输出依赖关系：

**阶段一：内部体积填充与纹理生成（Sec. 3.1）**
- **输入**：多视图 RGB 图像或视频序列重建的初始 3DGS 模型（仅表面高斯）。
- **内部体积初始化**：通过密度场阈值检测物体边界，在内部区域填充高斯粒子；随后进行仅透明度优化与近零透明度粒子剪枝，形成封闭的内部高斯体积。
- **内部纹理生成**：采用免训练的两阶段方法——首先利用单视图修复（MVInpainter + SD-XL）生成粗纹理，再通过迭代三轴修复与 GS 优化实现多视图一致的内部纹理。
- **输出**：具有完整内部体积与多视图一致纹理的 3DGS 模型。

**阶段二：CD-MPM 物理仿真（Sec. 3.2）**
- **输入**：阶段一输出的完整 3DGS 模型，每个高斯粒子被赋予质量、速度、体积、应力等物理属性。
- **仿真核心**：采用优化的 CD-MPM，引入连续损伤变量 $\\alpha$ 驱动脆性断裂，并通过正则化回归映射消除原算法在 $p=p_0$ 处的跳跃不连续性。支持为不同部件（如西瓜的果皮、果肉、种子）分配不同材料参数 $\\beta$ 实现混合材料仿真。
- **计算后端**：基于 NVIDIA Warp 实现 GPU 并行化，将单帧模拟时间从 CPU 的数分钟降至秒级。
- **输出**：更新后的粒子位置与变形梯度 $\\mathbf{F}_p(t)$。

**阶段三：GS 属性演化与渲染**
- **输入**：MPM 仿真输出的位置与变形梯度。
- **属性映射**：将变形梯度映射为高斯的均值、协方差与球谐系数旋转，更新渲染属性。
- **光照渲染**：采用基于 PCA 法线估计的 Blinn-Phong 光照模型，支持动态光源与阴影下的实时渲染。
- **输出**：任意视角下的动态场景渲染图像。

### 模块间关系

流水线中的关键因果链路可概括为：**尺度正则化 → 表面致密化 → 内部填充精度提升 → 纹理修复与法线估计质量提升 → 仿真与渲染保真度提升**。具体而言，初始 GS 训练中引入的尺度正则化损失（式 1）促使高斯核致密化，使得基于密度场的内部填充更精确、表面更平滑，进而为后续的纹理修复和 PCA 法线估计提供更可靠的几何基础。这一设计使整个框架无需额外训练数据即可实现从静态表面到可仿真体积表示的转换。

### 补充图表




GaussianFluent 的核心技术路线围绕两个瓶颈展开：**3DGS 缺乏内部体积表示与多视图一致内部纹理**，以及**现有 GS 物理仿真局限于弹性变形、数值不稳定且受限于 CPU 性能**。为此，方法在三个层面引入因果性改进——内部高斯体积与纹理生成、优化的连续损伤 MPM 仿真、以及 GPU 并行化与动态光照渲染。以下按模块拆解关键公式与变量含义。

### 3.1 内部高斯体积构建与纹理生成

**问题**：标准 3DGS 仅在物体表面重建高斯原语，内部空心无纹理，无法支撑断裂后的内部暴露渲染。

**核心思路**：先通过密度场阈值初始化内部高斯体积，再借助预训练图像生成模型以无需额外训练数据的方式合成多视图一致的内部纹理。

#### 3.1.1 内部高斯填充与透明度优化

首先，在训练初始 3DGS 时引入尺度正则化，促使高斯核致密化并贴近表面，便于后续内部填充和法线估计：

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{MSE}} + \mathcal{L}_{\mathrm{SSIM}} + \lambda \sum_{i=1}^{N} \|\mathbf{s}_i\|_2^2 \tag{1}
$$

其中 $\mathbf{s}_i$ 为第 $i$ 个高斯的尺度向量，$\lambda$ 为权重系数。该正则项约束高斯尺度，避免大尺度高斯跨越物体边界。

随后，对物体包围盒内的均匀网格点 $\mathbf{x}$ 计算密度场：

$$
d(\mathbf{x}) = \sum_{p \in P} \alpha_p \exp\left(-\frac{1}{2}(\mathbf{x} - \mathbf{x}_p)^T \mathbf{A}_p^{-1} (\mathbf{x} - \mathbf{x}_p)\right) \tag{2}
$$

其中 $P$ 为表面高斯的邻域集合，$\alpha_p$ 为第 $p$ 个高斯的透明度，$\mathbf{A}_p$ 为其协方差矩阵。将密度高于阈值的网格点初始化为新的内部高斯。由于密度初始化不够精确，随后执行**仅透明度优化**（固定位置与协方差），并剪枝透明度接近零的高斯，得到光滑的内部高斯体积（见 Figure 2）。

![[assets/figures/papers/paper_list_l2082_https_arxiv_org_abs_2601_09265/figures/002_Figure_2.jpg]]
*Figure 2: Internal Gaussian filling and refinement. The opacity optimization improves the smoothness of the GS surface after internal filling, beneficial for texture inpainting and simulation*

#### 3.1.2 内部纹理生成

内部纹理生成采用**无需训练的两阶段策略**：

1. **单视图修复初始化**：选取一帧渲染视图，使用 MVInpainter 与 Stable Diffusion XL 对内部区域进行修复，生成粗略内部纹理。
2. **迭代多轴精化**：沿三个正交轴分别进行修复与 GS 优化迭代，利用生成模型的先验知识合成多视图一致的内部纹理。

对于内部高斯，其零阶球谐系数由修复颜色初始化：

$$
\mathbf{sh}_i^0 = \frac{\mathbf{c}_i - 0.5}{C_0}
$$

其中 $\mathbf{c}_i$ 为修复颜色，$C_0 = 1/(2\sqrt{\pi})$ 为归一化常数。该初始化确保内部纹理与外部视图在渲染时保持连贯。

### 3.2 优化的连续损伤 MPM 仿真

**问题**：PhysGaussian 仅支持弹性变形，无法处理脆性断裂与拓扑变化；原生 CD-MPM 的回归映射在 $p = p_0$ 处存在跳跃不连续性，导致数值不稳定。

**核心思路**：将连续损伤 MPM（CD-MPM）集成到 GS 框架中，引入动态中心点正则化消除回归映射的不连续性，并支持混合材料参数分配。

#### 3.2.1 变形梯度与损伤模型

每个高斯原语被赋予质量、速度、体积和应力等物理属性，通过背景欧拉网格进行 P2G（粒子到网格）→ 网格更新 → G2P（网格到粒子）迭代。核心量是**变形梯度**：

$$
\mathbf{F}_p(t) = \frac{\partial \mathbf{x}}{\partial \mathbf{X}} = \frac{\partial \varphi(\mathbf{X}, t)}{\partial \mathbf{X}} \tag{5}
$$

其中 $\varphi(\mathbf{X}, t)$ 为从参考构型 $\mathbf{X}$ 到当前构型 $\mathbf{x}$ 的变形映射。$\mathbf{F}_p$ 编码了刚体旋转与非刚体拉伸/剪切，是连接物理仿真与 GS 渲染的桥梁——其旋转分量用于更新高斯的协方差矩阵，拉伸分量驱动损伤演化。

CD-MPM 采用 NACC 屈服面定义弹性区域边界：

$$
y(p, q; p_0, \beta, M) = q^2 (1 + 2\beta) + M^2 (p + \beta p_0)(p - p_0)
$$

其中 $p$ 为体积拉伸量，$q$ 为剪切量，$p_0$ 控制弹性区域大小并由损伤变量 $\alpha$ 动态收缩，$\beta$ 为材料内摩擦参数，$M$ 为屈服面斜率。当应力状态超出屈服面时，损伤 $\alpha$ 累积；当 $\alpha$ 达到阈值时，高斯原语被标记为断裂并从仿真中移除，实现脆性断裂效果。

#### 3.2.2 连续回归映射

原生 CD-MPM 的回归映射以固定点 $(p_c, 0)$ 为中心将试应力投影到屈服面，但在 $p = p_0$ 处映射方向发生跳跃，导致数值不稳定。GaussianFluent 引入**动态中心点**：

$$
p'_c = p_c + \phi_k(p^{\mathrm{tr}})(p^{\mathrm{tr}} - p_c) \tag{6}
$$

其中 $p^{\mathrm{tr}}$ 为试应力的体积分量，平滑函数定义为：

$$
\phi_k(p^{\mathrm{tr}}) = \left| \frac{p^{\mathrm{tr}} - p_c}{p_0 - p_c} \right|^k
$$

取 $k = 2$ 时，动态中心点 $p'_c$ 随 $p^{\mathrm{tr}}$ 平滑移动，消除了原算法在 $p = p_0$ 处的不连续性（见 Figure A1），保证了塑性修正的数值稳定性。

![[assets/figures/papers/paper_list_l2082_https_arxiv_org_abs_2601_09265/figures/010_Figure.jpg]]
*Figure: A1. Comparison of two return mapping kinds*

#### 3.2.3 混合材料建模

不同于 PhysGaussian 对整个物体使用统一的 $\beta$ 值，GaussianFluent 支持为不同部件（如果皮、果肉、种子）分配不同 $\beta$ 值，实现混合材料仿真。Figure 5 的消融实验表明，混合材料建模比统一 $\beta$ 产生更真实、符合物理的断裂模式。

### 3.3 GS 属性演化与渲染

MPM 仿真输出的位置和变形梯度被映射到 GS 的渲染属性：高斯均值直接由仿真位置更新，协方差矩阵通过 $\mathbf{F}_p$ 的旋转分量进行变换，球谐系数也相应旋转以保持视角相关外观。此外，引入基于 PCA 法线估计的 Blinn-Phong 光照模型：

$$
\mathbf{L}_i = \mathbf{c}_0 \odot \mathbf{I}_a + \sum_m T_{i,m} (\mathbf{c}_0 \odot \mathbf{I}_{L,m}) \frac{1}{r_m^2} (D_m + S_m)
$$

其中 $\mathbf{c}_0$ 为基色，$\mathbf{I}_a$ 为环境光，$T_{i,m}$ 为光源可见性，$D_m$ 和 $S_m$ 分别为漫反射和镜面反射项。该模型支持动态光源与阴影，增强了动态场景的视觉真实感（见 Figure 1、Figure A3）。

![[assets/figures/papers/paper_list_l2082_https_arxiv_org_abs_2601_09265/figures/012_Figure.jpg]]
*Figure: A3. More examples of object simulation and illumination*

### 3.4 GPU 并行化

原生 MPM 的 CPU 实现严重制约性能（单帧数分钟）。GaussianFluent 基于 NVIDIA Warp 框架将整个 P2G→网格更新→G2P 循环 GPU 并行化，将单帧模拟时间从约 4 分钟降至秒级（见 Table A1），使得交互式复杂动态场景的仿真与渲染成为可能。



## 实验与关键发现

### 内部纹理填充评估

GaussianFluent 的内部纹理生成能力通过定量指标与用户调研进行验证，对比基线包括 **PhysGaussian** 的直接颜色拷贝策略和基于 2D 修复的单视图方法。

**Table 1** 展示了定量对比结果。在 CLIP 分数上，本文方法达到 **35.4**，显著高于 PhysGaussian 的 22.3（+13.1）和 2D Inpainting 的 30.1（+5.3）。用户调研共收集 168 份评分，本文方法获得了 **71.43%**（60/84）的偏好率，远超 PhysGaussian 的 3.57% 和 2D Inpainting 的 25.00%。PhysGaussian 的直接颜色拷贝导致内部纹理模糊，而 2D 修复在倾斜视角下失效且缺乏多视图一致性。

**Figure 6** 的定性对比进一步印证了上述结论。本文方法生成的内部纹理在不同视角下保持清晰、一致的结构，而 PhysGaussian 仅将外部颜色复制到内部高斯，造成严重模糊；2D Inpainting 则在倾斜视角下产生明显的纹理断裂和伪影。

消融实验表明，迭代多轴纹理精化是性能提升的关键。该方法结合 MVInpainter 与低强度 SD-XL 修复，相较于单视图修复或直接颜色拷贝，显著提升了 3D 内部纹理的一致性与清晰度（Table 1, Figure 6）。这一设计有效利用了预训练生成模型的先验知识，无需额外训练数据即可合成多视图一致的内部结构。

![[assets/figures/papers/paper_list_l2082_https_arxiv_org_abs_2601_09265/figures/006_Table_1.jpg]]
*Table 1: Quantitative internal filling comparison. PhysGaussian’s direct color copying results in blurred textures, whereas 2D inpainting fails on oblique viewpoints*

### 动态场景仿真评估

动态场景仿真对比中，基线方法包括 **PhysGaussian**（仅支持弹性材料）和 **OmniPhysGS**（自动估计材料参数但仍限于弹性框架）。**Table 2** 显示，本文方法在 CLIP 分数上达到 **22.7**，大幅领先 PhysGaussian 的 12.2（+10.5）和 OmniPhysGS 的 13.1（+9.6）。用户调研（208 份评分）中，本文方法获得 **88.46%**（23/26）的偏好率，对比 PhysGaussian 的 3.84% 和 OmniPhysGS 的 7.69%，优势极为显著。

![[assets/figures/papers/paper_list_l2082_https_arxiv_org_abs_2601_09265/figures/007_Table_2.jpg]]
*Table 2: Dynamic scene simulation comparison. Our method significantly outperforms baselines. PhysGaussian fails to produce brittle fracture, and OmniPhysGS is constrained by the PhysGaussian framework*

**Figure 4** 展示了果冻材料被子弹击穿的场景对比。PhysGaussian 无法产生脆性断裂，仅表现为弹性变形；而本文方法通过连续损伤 MPM 正确模拟了断裂过程，并可视化损伤变量 α 的演化。**Figure 7** 的棒棒糖断裂对比进一步验证了混合材料仿真的优势——本文方法准确再现了不同材料组分的断裂模式，而两个基线均无法处理此类复杂动态。

### 混合材料消融

**Figure 5** 以西​​瓜坠落为例，对比了混合材料建模与统一 β 参数设置的效果。本文方法为果皮、果肉和种子分别分配不同的 β 值（2、0.6 和 5），产生了更符合物理直觉的断裂模式。相比之下，采用单一统一 β 值的设置无法区分不同部件的力学响应，导致断裂行为失真。该消融直接验证了混合材料参数分配对仿真真实感的决定性贡献。

### 计算性能

GPU 并行化是 GaussianFluent 实现交互式仿真的关键工程贡献。**Table A1** 报告了各场景的每帧平均耗时。通过 NVIDIA Warp 将 CD-MPM 从 CPU 迁移至 GPU，模拟时间从单帧约 4 分钟降至秒级，支持复杂场景的实时交互。所有性能指标均在提供 103 Tensor TFLOPS（FP16）的 GPU 上测得。

![[assets/figures/papers/paper_list_l2082_https_arxiv_org_abs_2601_09265/figures/009_Table.jpg]]
*Table: A1. Parameters and Timings. Seconds per frame (s/frame) is an average. All performance metrics were obtained from experiments conducted on a GPU delivering 103 Tensor TFLOPS at FP16 precision*

### 回归映射稳定性验证

优化的 CD-MPM 回归映射消除了原算法在 $p = p_0$ 处的跳跃不连续性。**Figure A1** 对比了两种回归映射方式：原始分段映射在临界点处产生数值跳变，而本文引入的动态中心点 $p_c'$（式 6）通过 $k$ 阶多项式平滑过渡（取 $k=2$），保证了塑性修正的数值稳定性。该改进是脆性断裂仿真得以稳定运行的理论基础。

### 失败模式与局限性

尽管 GaussianFluent 在定量和定性评估中均表现优异，仍存在以下局限：

1. **材料参数依赖人工定义**：当前方法需要手动指定各部件参数（如 β、E、ν），尚未实现自动参数估计或基于逆渲染的学习，限制了大规模场景的部署效率。
2. **内部纹理受生成模型制约**：纹理质量依赖预训练生成模型的输出，在语义复杂或罕见对象上可能产生不一致或伪影，且受提示词质量影响。
3. **实时性仍有边界**：虽然 GPU 并行显著加速，但面对极大粒子数或复杂多物理场耦合时，实时性仍可能受限。
4. **流体仿真未充分验证**：流体效果通过 $p_0 \to 0$ 的退化实现，未专门针对自由表面流或多相流进行系统验证。
5. **本构模型单一**：目前仅采用 NACC 这一种损伤模型，未探索粘塑性、超弹性-损伤耦合等更丰富的本构关系，物理逼真度仍有提升空间。

### 公平性说明

所有对比方法使用公开可用的实现或据原文复现，在相同 GPU 硬件上运行。定量评估采用统一的 CLIP 提示词和相同对象的用户研究，内部填充与模拟分别收集 168 和 208 份评分。虽然 PhysGaussian 本身不支持断裂，但仍在可比较的帧上评估 CLIP 相似度以衡量渲染真实感。

### 补充图表

![[assets/figures/papers/paper_list_l2082_https_arxiv_org_abs_2601_09265/figures/004_Figure_4.jpg]]
*Figure 4: A jelly-like material is shot with a bullet. We compare our method with PhysGaussian to demonstrate the effectiveness of our simulation and visualize the damage variable α*

![[assets/figures/papers/paper_list_l2082_https_arxiv_org_abs_2601_09265/figures/005_Figure_5.jpg]]
*Figure 5: Comparison between our mixed material modeling and fixed β setting. Our approach assigns distinct β values, i.e., 2, 0.6, and*



## 定位与知识库关联

### 1. 与基线工作的关系

GaussianFluent 的核心技术路线是在 3D Gaussian Splatting（3DGS）物理仿真框架上，通过“内部表示重建 + 材料本构升级 + 数值方法改进”三条路径实现对现有基线的系统性超越。

**相对于 PhysGaussian 的突破。** PhysGaussian 是首个将 Material Point Method（MPM）与 3DGS 结合的框架，但其物理模型局限于纯弹性材料，且仅使用表面高斯，物体内部呈空心状态，断裂后暴露的截面缺乏纹理。GaussianFluent 在三个维度上突破了这一基线：
- **内部表示**：通过密度场初始化与透明度优化生成封闭的内部高斯体积，并结合预训练图像生成模型（MVInpainter + SD-XL）实现多视图一致的内部纹理合成。定量对比（Table 1）显示，CLIP 分数从 PhysGaussian 的 22.3 提升至 35.4，用户偏好从 3.57% 跃升至 71.43%。
- **物理模型**：将纯弹性 MPM 替换为连续损伤 MPM（CD-MPM），引入损伤变量 $\alpha$ 驱动脆性断裂，使框架能够模拟果冻穿透、西瓜摔裂等拓扑变化场景。
- **数值稳定性**：原生 CD-MPM 的回归映射在 $p = p_0$ 处存在跳跃不连续性，GaussianFluent 通过引入 $k$ 阶多项式动态中心点 $p'_c = p_c + \phi_k(p^{\mathrm{tr}})(p^{\mathrm{tr}} - p_c)$ 实现了连续映射，取 $k=2$ 时在数值稳定性与精度间取得平衡（Figure A1）。

**相对于 OmniPhysGS 的差异。** OmniPhysGS 在 PhysGaussian 基础上加入了自动材料参数估计，但物理框架仍限于弹性变形，无法处理断裂与拓扑变化。GaussianFluent 则直接升级了底层物理模型至 CD-MPM，并在混合材料建模上支持为不同部件（如果皮、果肉、种子）分配独立的 $\beta$ 值，产生更符合物理直觉的断裂模式（Figure 5）。动态场景定量评估（Table 2）中，GaussianFluent 的 CLIP 分数（22.7）大幅领先 OmniPhysGS（13.1），用户偏好达 88.46%。

**相对于 2D Inpainting 的改进。** 2D Inpainting 方法仅对单视图进行内部纹理修复，缺乏 3D 一致性，在倾斜视角下失效。GaussianFluent 采用两阶段训练无关方案：先通过单视图修复初始化粗纹理，再沿多个正交轴迭代修复并联合 GS 优化，使内部纹理在不同视角下保持一致（Figure 6）。CLIP 分数从 2D Inpainting 的 30.1 提升至 35.4，用户偏好从 25.00% 提升至 71.43%。

### 2. 知识库定位

GaussianFluent 处于 **3D 高斯泼溅物理仿真** 与 **生成模型辅助的 3D 内容创建** 的交叉地带，其技术贡献可映射到以下知识脉络：

**物理仿真层面。** 该方法继承了 MPM 在图形学中的长期积累（从冰雪仿真到弹塑性体），但将计算后端从传统 CPU 实现迁移至 NVIDIA Warp GPU 并行框架，使单帧仿真时间从数分钟降至秒级（Table A1），为交互式动态场景渲染铺平了道路。同时，NACC 屈服面的引入使框架具备脆性断裂能力，而 $p_0 \to 0$ 的退化设置可近似流体行为，在统一框架下覆盖了从固体到流体的材料谱系。

**3D 表示层面。** 相比于 NeRF 类隐式表示，3DGS 的显式点云结构天然适配拉格朗日粒子仿真——变形梯度 $\mathbf{F}_p(t)$ 可直接映射为高斯的协方差矩阵旋转，避免了隐式场到显式几何的转换开销。GaussianFluent 进一步通过 PCA 法线估计与 Blinn-Phong 光照模型，使动态场景支持实时重光照，弥补了原生 3DGS 缺乏法线信息的短板。

**生成模型融合层面。** 该方法开创性地将预训练图像生成模型（SD-XL）的视觉先验注入物理仿真管线，在无需额外训练数据的条件下合成多视图一致的内部纹理。这一“大模型先验 + 物理仿真”的范式，为 3D 内容创建中“所见即所得”到“所剖亦真实”的跨越提供了新思路。

### 3. 适用边界与局限

尽管 GaussianFluent 在混合材料动态场景仿真上取得了显著进展，其适用边界仍受以下因素制约：

1. **材料参数依赖人工定义。** $\beta$、杨氏模量 $E$、泊松比 $\nu$ 等物理参数需手动设定，尚未实现基于逆渲染或学习的自动估计。这限制了方法在未知物体上的开箱即用能力。

2. **内部纹理质量受生成模型制约。** 纹理合成依赖 SD-XL 的修复质量与提示词设计，在语义复杂或训练分布外的罕见对象上可能产生不一致或伪影。当前验证集中于食物、水果等常见类别，对工业零件或生物组织的泛化性尚待检验。

3. **本构模型单一。** 仅采用 NACC 这一种损伤模型，未探索粘塑性、超弹性-损伤耦合等更丰富的本构关系。流体仿真通过 $p_0 \to 0$ 的退化实现，未针对自由表面流或多相流进行专门验证，物理逼真度存在提升空间。

4. **极端规模的实时性挑战。** 虽然 GPU 并行化带来数量级加速，但在粒子数超万级或涉及多物理场耦合（如热-力-化学）的复杂场景中，实时性仍可能受限。

### 4. 开放问题

从 GaussianFluent 的技术路线出发，以下开放问题值得后续工作关注：

- **物理参数自动推断**：如何通过逆渲染或基于学习的预测仿真方法，从多视图观测中自动估计 $\beta$、$E$、$\nu$ 等参数，减少人工调节负担？
- **本构模型扩展**：能否将更广泛的本构模型（如粘塑性、超弹性-损伤耦合）融入统一框架，提升对真实材料行为的覆盖度？
- **生成模型与仿真的深度耦合**：是否可以利用仿真结果反馈指导纹理生成，实现“仿真-渲染-生成”的闭环优化？
- **超大规模场景**：如何在保持交互帧率的前提下，将方法扩展到包含上万颗粒子、多相流和复杂碰撞检测的场景？



## 原文 PDF

![[paperPDFs/CVPR_2026/GaussianFluent_Gaussian_Simulation_for_Dynamic_Scenes_with_Mixed_Materials.pdf]]
