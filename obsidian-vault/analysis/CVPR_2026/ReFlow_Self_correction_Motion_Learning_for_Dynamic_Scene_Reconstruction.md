---
title: "ReFlow: Self-correction Motion Learning for Dynamic Scene Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ReFlow_Self_correction_Motion_Learning_for_Dynamic_Scene_Reconstruction.pdf
project_link: null
code_link: "https://github.com/hustvl/4DGaussians"
aliases:
- ReFlow
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 自校正流匹配机制（Self-correction Flow Matching）——将3D运动投影为2D流，通过比较warped帧与实际帧的差异来直接调整3D运动，从而用原始视频作为运动监督信号，完全摒弃外部运动先验。
primary_logic: 准确的3D运动应能够解释视频帧间的像素变化；通过测量warped帧与真实帧的不一致，可自然地监督3D运动学习，形成一个自校正循环。
claims:
- 消融实验表明，在基线4DGS上直接加入自校正流匹配（Full Flow Matching）即可带来+0.64dB的PSNR提升；结合完整规范空间初始化、静动态分离和相机流匹配后，整体提升达+2.39dB（PSNR从25.81到28.20）。
- 与使用外部光流监督的变体（Ours (External Flow)）对比，自校正方法在Playground等场景中PSNR高出4.61dB（25.58 vs 20.97），说明外部光流在复杂运动场景下可能提供误导信号。
- 在Nvidia Monocular和Nerfies-HyperNeRF数据集上均取得最优PSNR/SSIM/LPIPS，超越MoDec-GS等最新方法，且在多个场景中PSNR提升超过2dB。
- Nvidia Monocular (平均) 上 PSNR / SSIM / LPIPS = 28.20 / 0.903 / 0.103
---

# ReFlow: Self-correction Motion Learning for Dynamic Scene Reconstruction

> [!tip] 核心洞察
> 准确的3D运动应能够解释视频帧间的像素变化；通过测量warped帧与真实帧的不一致，可自然地监督3D运动学习，形成一个自校正循环。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReFlow：动态场景重建的自校正运动学习 |
| 英文题名 | ReFlow: Self-correction Motion Learning for Dynamic Scene Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.01561) · [Code](https://github.com/hustvl/4DGaussians) · [arXiv](https://arxiv.org/abs/2604.01561) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ReFlow |
| Dataset | Nvidia Monocular, Nerfies-HyperNeRF |

> [!tip] 效果简介
> - Nvidia Monocular (平均) 上，PSNR / SSIM / LPIPS 28.20 / 0.903 / 0.103 vs MoDec-GS: 26.63 / 0.879 / 0.160 (+1.57 / +0.024 / -0.057)。
> - Nerfies-HyperNeRF (Broom) 上，PSNR 23.97 vs 4DGS: 22.00 (+1.97)。

## 概述

从单目视频重建动态3D场景是计算机视觉中的核心挑战。现有方法普遍面临两个瓶颈：其一，依赖COLMAP等静态SfM管道进行场景初始化，导致动态区域覆盖不完整，且静态与动态高斯混合初始化，造成后续重建不稳定；其二，为补偿初始化缺陷，大量方法引入外部密集运动先验（如光流、点跟踪）作为硬约束，这不仅引入额外复杂度，更可能因外部估计误差而传播错误信号（见Figure 1）。

ReFlow的核心洞察是：准确的3D运动应当天然地解释视频帧间的像素变化。基于此，论文提出**自校正流匹配**（Self-correction Flow Matching）机制——将预测的3D运动投影为2D流场，通过比较warped帧与实际观测帧的差异来直接调整3D运动，从而用原始视频本身作为运动监督信号，完全摒弃外部运动先验。这一机制形成了一个自校正循环：错误运动会生成不对齐的warped结果，该差异反向驱动运动优化，使重建细节逐步恢复（见Figure 2）。

为支撑这一机制，ReFlow构建了两个配套模块：**完整规范空间构建**（Complete Canonical Space Construction）利用几何基础模型提供静动态分离的可靠初始化；**分离式动态场景建模**（Separation-Based Dynamic Scene Modeling）将静态和动态组件独立建模，为后续区域化运动约束提供基础。在此基础上，全流匹配（Full Flow Matching）监督场景整体运动，相机流匹配（Camera Flow Matching）对静态区域施加仅由相机运动导出的流约束，二者形成互补的自校正信号（见Figure 3、Figure 4）。

实验表明，ReFlow在Nvidia Monocular和Nerfies-HyperNeRF两个基准上均取得最优PSNR/SSIM/LPIPS，超越MoDec-GS等最新方法。消融研究证实，在基线4DGS上直接加入自校正流匹配即可带来+0.64dB的PSNR提升；结合完整初始化、静动态分离和相机流匹配后，整体提升达+2.39dB（PSNR从25.81提升至28.20）。与使用外部光流监督的变体相比，自校正方法在复杂运动场景中PSNR高出4.61dB，验证了外部运动先验在特定场景下可能提供误导信号。

## 背景与动机

### 动态场景重建的核心瓶颈

从单目视频重建4D动态场景是计算机视觉中的基础挑战。现有方法面临两个紧密耦合的瓶颈：

**瓶颈一：不完整的初始化。** 主流动态场景重建方法（如4DGS、Deformable-3DGS等）通常采用COLMAP等静态SfM管道获取初始点云。然而，静态SfM天然倾向于在动态区域失效——移动物体上的点难以建立可靠的多视图对应，导致动态区域点云稀疏甚至完全缺失。更关键的是，现有方法在初始化时不区分静态点与动态点，将两者混合为统一的高斯表示，使得后续优化从一开始就陷入纠缠状态，难以稳定收敛（见Figure 1顶部）。

**瓶颈二：对外部运动先验的过度依赖。** 为补偿初始化缺陷，许多方法引入外部密集运动先验作为约束——例如光流估计（RAFT等）、点跟踪或深度估计。这些外部信号虽然提供了额外的监督，但也引入了新的问题：（1）外部估计器自身的误差会传播到重建中；（2）在相机运动主导或小物体快速移动的场景下，外部光流可能提供不准确的运动信号；（3）系统复杂度显著增加，需要维护多个外部模型的推理管道（见Figure 1底部）。

### 核心洞察：从“外部监督”到“自校正”

ReFlow的动机源于一个简单的观察：**2D视频帧间的像素变化本质上由3D场景运动引起**。如果重建的3D运动是准确的，那么将其投影回2D平面产生的运动流，应当能够自然地解释帧间的视觉差异。反之，不准确的3D运动会表现为warped帧与真实帧之间的不一致，这种不一致本身就可以作为运动学习的监督信号（见Figure 2）。

这一洞察将问题从“如何获取外部运动真值”转变为“如何利用视频本身作为运动监督”，形成了一个**自校正循环**：预测3D运动 → 投影为2D流 → warp帧并比较差异 → 差异反向传播校正3D运动。该方法完全摒弃了对外部运动先验的依赖，仅使用原始视频帧作为唯一的运动监督源。

### 方法定位

ReFlow建立在4D Gaussian Splatting（4DGS）框架之上，但针对上述两个瓶颈进行了系统性改进：

1. **完整规范空间构建**：替代COLMAP的静态SfM，利用几何基础模型构建包含静态和动态区域的完整初始点云，并通过静动态分离提供干净的初始化。
2. **分离式动态场景建模**：将场景解耦为静态组件（仅依赖空间特征）和动态组件（结合时空特征），为后续的区域化运动约束提供结构化基础。
3. **自校正流匹配**：通过全流匹配（Full Flow Matching）监督全局运动，通过相机流匹配（Camera Flow Matching）约束静态区域仅由相机运动驱动，两者互补提供完整的运动自校正信号。

后续章节将详细展开各模块的设计原理、技术实现与实验验证。

## 核心创新

ReFlow 的核心创新在于构建了一个**自校正闭环**，使动态场景重建完全摆脱对外部运动先验（如光流、点跟踪）的依赖。这一闭环由三个紧密耦合的“changed slots”共同支撑：完整规范空间初始化、分离式静动态建模、以及自校正流匹配机制。

### 创新一：完整规范空间初始化（Complete Canonical Space Construction）

**基线瓶颈**：现有方法（如4DGS）采用 COLMAP 等静态 SfM 点云进行初始化，导致动态区域覆盖不完整，且静态与动态高斯混合初始化，造成后续优化不稳定（见 Figure 1 顶部）。

**创新机制**：ReFlow 引入几何基础模型（如 ）构建一个同时覆盖静态与动态区域的完整规范空间。具体流程为：
1. 利用几何基础模型获取每帧的深度图与动态掩膜 $M_i^{\mathrm{dyn}}$；
2. 通过全局对齐损失 $\mathcal{L}_{\mathrm{align}}$ 优化关键帧的相机位姿 $K_{\mathrm{pose}}$、内参 $K_{\mathrm{intr}}$ 和深度图 $K_{\mathrm{depth}}$，实现粗到细的对齐；
3. 根据动态掩膜将点云分离为静态与动态两部分，为后续分离式建模提供结构化的初始点云。

这一设计从源头上解决了动态区域“从零开始重建”的不稳定性，为后续运动学习提供了可靠的几何锚点。

### 创新二：分离式静动态建模（Separation-Based Dynamic Scene Modeling）

**基线瓶颈**：传统方法将所有高斯统一建模，不区分静动态区域，导致运动监督无法精准施加——静态区域可能产生虚假运动，动态区域则缺乏足够的运动自由度。

**创新机制**：ReFlow 对静态和动态组件采用不同的特征表示与解码策略：
- **静态组件**：仅使用三平面空间特征 $F_s$ 解码高斯参数 $G_s: \{\mu_s, s_s, q_s, \sigma_s, c_s\} = D_s(x, y, z; F_s)$，确保静态结构的时间一致性；
- **动态组件**：在三平面空间特征基础上额外引入时间平面特征，赋予动态高斯灵活的运动表达能力。

这一分离设计为后续**区域化运动约束**（全流匹配作用于全局，相机流匹配仅作用于静态区域）提供了结构基础，是实现精准运动监督的关键前提。

### 创新三：自校正流匹配机制（Self-correction Flow Matching）

这是 ReFlow 最核心的创新，其洞察可概括为：**准确的 3D 运动应当能够解释视频帧间的像素变化**（见 Figure 2）。基于此，ReFlow 用原始视频帧本身作为运动监督信号，形成一个无需外部先验的自校正循环。

**机制设计**：ReFlow 定义了两类 2D 流场（见 Figure 4(a)），分别捕获不同来源的运动：

- **全流（Full Flow）**：合成从 $t_1$ 到 $t_2$ 的总位移，包含物体运动与相机运动：
  $$\mathbf{F}_{full} = \mathrm{FlowRender}(G_{t_1}, G_{t_2}, \mathbf{P}_1, \mathbf{P}_2)$$

- **相机流（Camera Flow）**：仅由相机运动引起的位移，假设场景完全静态：
  $$\mathbf{F}_{cam} = \mathrm{CamFlowRender}(G_{t_1}, \mathbf{P}_1, \mathbf{P}_2)$$

两类流场分别驱动两个互补的监督损失：

1. **全流匹配（Full Flow Matching）**：将 $t_1$ 帧按 $\mathbf{F}_{full}$ warping 到 $t_2$，与真实帧 $I_2$ 比较，形成运动一致性损失 $\mathcal{L}_{mc}$ 和跨时间渲染损失 $\mathcal{L}_{cr}$：
   $$\mathcal{L}_{fullflow} = \lambda_{mc}\mathcal{L}_{mc} + \lambda_{cr}\mathcal{L}_{cr}$$

2. **相机流匹配（Camera Flow Matching）**：仅在静态区域施加相机流约束，确保静态结构稳定，消除虚假运动：
   $$\mathcal{L}_{camflow} = \lambda_{mc}^{cam}\mathcal{L}_{mc}^{cam} + \lambda_{cr}^{cam}\mathcal{L}_{cr}^{cam}$$

最终优化目标结合基线光度损失与两类流匹配损失：
$$\mathcal{L} = \mathcal{L}_{baseline} + \lambda_{ff}\mathcal{L}_{fullflow}(I_1, I_2) + \lambda_{cf}\mathcal{L}_{camflow}(I_1^{static}, I_2^{static})$$

**与外部光流监督的本质区别**：消融实验（Table 6）表明，使用 RAFT 等外部光流作为伪真值的变体（Ours (External Flow)）在 Playground 等复杂运动场景中 PSNR 仅为 20.97，而自校正方法达到 25.58（+4.61dB）。原因在于外部光流在相机运动主导或小物体快速移动时可能提供误导信号，而自校正机制直接从原始视频中提取运动监督，避免了外部估计误差的传播。

### 创新的协同效应

三个 changed slots 之间存在递进式依赖关系：完整规范空间初始化为分离式建模提供了结构化的起点，分离式建模又为区域化流匹配约束提供了施加对象。消融实验（Table 3）量化了这一协同效应：在基线 4DGS（PSNR 25.81）上逐步叠加各模块，PSNR 从 26.45（仅全流匹配，+0.64dB）→ 26.60（+规范空间初始化，+0.79dB）→ 27.00（+静动态分离，+1.19dB）→ 27.85（+全流匹配，+2.04dB）→ 最终 28.20（+相机流匹配，+2.39dB），验证了各组件独立贡献且正向叠加。

## 整体框架

ReFlow 的整体设计遵循“先构建完整静态/动态初始化，再解耦建模，最后通过自校正流匹配实现运动学习”的三阶段流水线，如图 3 所示。整个框架的输入为单目视频序列及其对应的相机位姿，输出是支持新视角渲染和动态场景重建的 4D 高斯表示。

### 流水线概览

**第一阶段：完整规范空间构建（Complete Canonical Space Construction）**。传统方法依赖 COLMAP 等静态 SfM 点云进行初始化，导致动态区域覆盖不完整且静动态高斯混合，造成后续重建不稳定。ReFlow 改用几何基础模型（geometry foundation model）从视频帧中提取深度和动态掩码，通过粗到细的全局对齐优化关键帧的相机位姿、内参和深度图，最终构建一个同时覆盖静态和动态区域的完整规范空间。该空间中的点云已按动态掩码分离为静态点云和动态点云，为后续建模提供了可靠的结构基础。

**第二阶段：分离式动态场景建模（Separation-Based Dynamic Scene Modeling）**。在完整规范空间的基础上，ReFlow 对静态和动态组件分别建模。静态高斯通过三平面空间特征（tri-plane spatial features）解码，动态高斯则在空间特征基础上增加时间平面特征（temporal plane features），使网络能够独立地聚合静态区域的时空信息，同时为动态元素保留灵活的运动表达能力。这一解耦设计为后续的区域化运动约束提供了结构前提。

**第三阶段：自校正流匹配（Self-correction Flow Matching）**。这是 ReFlow 的核心创新——完全摒弃外部光流或点跟踪等运动先验，转而利用原始视频帧间的像素变化作为运动监督信号。具体而言，框架定义了两种 2D 流场：**全流（Full Flow）** 和 **相机流（Camera Flow）**。全流通过流渲染器（Flow Renderer）合成从时刻 $t_1$ 到 $t_2$ 的总运动位移（包含物体运动和相机自运动），相机流则仅计算由相机运动引起的位移（假设场景静态）。这两种流分别用于不同的监督目标：全流对整个图像进行 warp 并与真实帧比较，提供全局运动一致性约束；相机流仅作用于静态区域，确保这些区域严格遵循相机运动，消除虚假运动。两者共同构成一个自校正循环——不准确的 3D 运动会导致 warp 结果与真值不对齐，由此产生的 photometric loss 反向驱动 3D 运动的优化。

### 损失函数整合

总训练损失将基线 4DGS 的光度渲染损失与两个流匹配项统一：

$$
\mathcal{L} = \mathcal{L}_{baseline} + \lambda_{ff}\mathcal{L}_{fullflow}(I_1, I_2) + \lambda_{cf}\mathcal{L}_{camflow}(I_1^{static}, I_2^{static})
$$

其中全流匹配损失 $\mathcal{L}_{fullflow}$ 由运动一致性损失 $\mathcal{L}_{mc}$ 和跨时间渲染损失 $\mathcal{L}_{cr}$ 加权组成，相机流匹配损失 $\mathcal{L}_{camflow}$ 同理作用于静态区域。这一设计使得运动学习不再依赖任何外部先验，而是直接从原始视频中自监督地校正。

### 关键设计决策与证据

消融实验（Table 3）揭示了各模块的贡献层级：在基线 4DGS（PSNR 25.81）上直接加入全流匹配（Full Flow Matching）即可带来 +0.64 dB 的 PSNR 提升，验证了自校正流匹配机制本身的有效性；加入完整规范空间初始化后达到 +0.79 dB；进一步引入静动态分离后达到 +1.19 dB；在此基础上叠加全流匹配和相机流匹配，最终整体提升达 +2.39 dB（PSNR 28.20）。这一递增趋势表明，三个模块之间存在协同效应——完整的初始化和结构化解耦为流匹配提供了更干净的监督信号，而流匹配又反过来纠正了初始化和建模中的残余误差。

### 局限与开销

该方法引入了适度的计算开销：训练时间增加约 30%，GPU 显存占用增加 1–2 GB（Table 4），主要来自流渲染和规范空间构建的额外计算。渲染速度（FPS）较基线下降约 10–20%，模型大小增加 20–50 MB，但推理阶段无额外计算负担。此外，整体性能受限于几何基础模型在物体出现/消失或拓扑变化场景下的可靠性（如图 9 所示的失败案例），这是当前流水线的一个结构性瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2604_01561/figures/003_Figure_3.jpg]]
*Figure 3: Overview of ReFlow. We start by constructing a complete canonical space(Sec. 3.2.1), which includes both static and dynamic components, ensuring a reliable 3D scene initialization. Next, we disentangle these elements using spatial and spatiotemporal feature planes(Sec. 3.2.2), providing a structured representation that separately handles static and dynamic regions. This preparation allows us to introduce targeted motion constraints(Sec. 3.3): Full Flow supervises motion across the entire scene, while Camera Flow enforces consistency in static regions, enabling the self-correction learning mechanism for accurate 3D motion reconstruction*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2604_01561/figures/001_Figure_1.jpg]]
*Figure 1: Typical Challenges in monocular dynamic scene reconstruction. Top: Incomplete initialization for dynamic regions: the initial 3D structure from SfM often misses dynamic components and initializes Gaussians without separating static points (green) from dynamic points (red), leading to an entangled and incomplete representation. Bottom: To compensate, existing methods frequently resort to external dense motion guidance to constrain and stabilize the reconstruction of dynamic regions*

## 核心模块与公式推导

ReFlow 的核心创新在于将动态场景重建从“依赖外部运动先验”转变为“从视频自身学习运动”，其技术路线围绕三个关键模块展开：完整规范空间构建、分离式静动态建模、以及自校正流匹配机制。以下逐一剖析各模块的设计逻辑与数学表达。

### 完整规范空间构建

传统方法（如 4DGS）直接使用 COLMAP 等静态 SfM 输出的点云作为初始化，导致动态区域覆盖不全、静动态高斯混合，为后续优化埋下不稳定因素。ReFlow 的解决方案是：借助几何基础模型（如 ）逐帧重建场景结构，再通过全局对齐将所有帧的点云统一到一个完整的规范空间中。

具体而言，该方法从视频中选取关键帧，利用几何基础模型估计每帧的深度图、相机内参和外参，然后通过最小化 3D 几何一致性损失进行全局优化：

$$
\operatorname* { m i n } _ { K _ { \mathrm { p o s e } } , K _ { \mathrm { i n t r } } , K _ { \mathrm { d e p t h } } } \sum _ { ( a , b ) \in E _ { K } } \mathcal { L } _ { \mathrm { a l i g n } } ( \mathbf { X } _ { a } , \mathbf { X } _ { b } )
$$

其中 $K_{\mathrm{pose}}$、$K_{\mathrm{intr}}$、$K_{\mathrm{depth}}$ 分别表示关键帧的相机位姿、内参和深度图，$E_K$ 为关键帧对集合，$\mathcal{L}_{\mathrm{align}}$ 衡量两个帧在 3D 空间中的几何对齐程度。优化完成后，利用几何基础模型提供的动态掩码 $M_i^{\mathrm{dyn}}$ 将点云分离为静态和动态两部分，为后续分离式建模提供结构化初始化。

### 分离式静动态建模

在获得完整的规范空间点云后，ReFlow 采用分离式架构对静态和动态组件分别建模。这一设计的深层动机在于：静态区域仅受相机运动影响，而动态区域同时包含物体运动和相机运动——只有将二者解耦，才能施加区域化的运动约束。

**静态组件**通过三平面空间特征解码：

$$
G _ { s } : \{ \mu _ { s } , s _ { s } , q _ { s } , \sigma _ { s } , c _ { s } \} = D _ { s } ( x , y , z ; F _ { s } )
$$

其中 $F_s$ 为空间三平面特征，$D_s$ 为静态解码器，输出静态高斯的中心位置 $\mu_s$、尺度 $s_s$、旋转四元数 $q_s$、不透明度 $\sigma_s$ 和颜色 $c_s$。静态组件仅依赖空间坐标，不随时间变化。

**动态组件**则在空间三平面的基础上增加时间平面特征，使其能够灵活捕捉物体的非刚性形变和运动。这种分离设计使得后续的自校正流匹配能够对静态区域施加仅由相机运动导出的约束，而对动态区域施加包含物体运动的完整约束。

### 自校正流匹配机制

这是 ReFlow 最核心的贡献——完全摒弃外部光流或点跟踪等运动先验，转而从原始视频帧的像素变化中直接生成运动监督信号。其核心洞察是：如果重建的 3D 运动是准确的，那么将 $t_1$ 时刻的图像按该运动 warp 到 $t_2$ 时刻后，应与 $t_2$ 时刻的真实观测一致；反之，warp 结果与真实图像的差异就构成了运动学习的自然监督信号。

#### 两种流的定义

为区分不同来源的运动，ReFlow 定义了两类 2D 流场：

**全流（Full Flow）** 包含物体运动和相机运动的综合效果。给定 $t_1$ 和 $t_2$ 时刻的高斯集合 $G_{t_1}$、$G_{t_2}$ 及对应的相机参数 $\mathbf{P}_1$、$\mathbf{P}_2$，通过流渲染函数合成：

$$
\mathbf{F}_{full} = \mathrm{FlowRender}(G_{t_1}, G_{t_2}, \mathbf{P}_1, \mathbf{P}_2) \tag{1}
$$

**相机流（Camera Flow）** 仅由相机运动引起，假设场景完全静态。它仅使用 $t_1$ 时刻的高斯集合和两个时刻的相机参数：

$$
\mathbf{F}_{cam} = \mathrm{CamFlowRender}(G_{t_1}, \mathbf{P}_1, \mathbf{P}_2) \tag{2}
$$

#### 全流匹配损失

全流匹配对整幅图像施加运动约束，由两项组成：

**运动一致性损失** 将 $t_1$ 时刻的真实图像 $I_1$ 按 $\mathbf{F}_{full}$ 进行 warp，与 $t_2$ 时刻的真实图像 $I_2$ 比较：

$$
\mathcal{L}_{mc} = \mathcal{L}_{photo}(I_1^{warped}, I_2) \tag{3}
$$

**跨时间渲染损失** 为进一步强化时间一致性，将 $t_1$ 时刻的渲染图像 $\hat{I}_1$ 也按同一流场 warp，与 $I_2$ 比较：

$$
\mathcal{L}_{cr} = \mathcal{L}_{photo}(\hat{I}_1^{warped}, I_2) \tag{4}
$$

两项加权求和构成全流匹配目标：

$$
\mathcal{L}_{fullflow} = \lambda_{mc}\mathcal{L}_{mc} + \lambda_{cr}\mathcal{L}_{cr} \tag{5}
$$

#### 相机流匹配损失

相机流匹配专门约束静态区域，确保其仅跟随相机运动，避免产生虚假的物体运动。同样包含两项：

**静态运动一致性损失** 将 $t_1$ 时刻的静态区域图像 $I_1^{static}$ 按 $\mathbf{F}_{cam}$ warp，与 $t_2$ 时刻的静态区域 $I_2^{static}$ 比较：

$$
\mathcal{L}_{mc}^{cam} = \mathcal{L}_{photo}(I_1^{static,warped}, I_2^{static}) \tag{6}
$$

**静态跨时间渲染损失** 将 $t_1$ 时刻静态区域的渲染图像 $\hat{I}_1^{static}$ 按 $\mathbf{F}_{cam}$ warp 后与 $I_2^{static}$ 比较：

$$
\mathcal{L}_{cr}^{cam} = \mathcal{L}_{photo}(\hat{I}_1^{static,warped}, I_2^{static}) \tag{7}
$$

相机流匹配总损失为：

$$
\mathcal{L}_{camflow} = \lambda_{mc}^{cam}\mathcal{L}_{mc}^{cam} + \lambda_{cr}^{cam}\mathcal{L}_{cr}^{cam} \tag{8}
$$

#### 总体优化目标

最终训练损失在基线 4DGS 的光度渲染损失 $\mathcal{L}_{baseline}$ 之上，叠加全流匹配和相机流匹配两项：

$$
\mathcal{L} = \mathcal{L}_{baseline} + \lambda_{ff}\mathcal{L}_{fullflow}(I_1, I_2) + \lambda_{cf}\mathcal{L}_{camflow}(I_1^{static}, I_2^{static}) \tag{9}
$$

其中 $\lambda_{ff}$ 和 $\lambda_{cf}$ 为平衡系数。全流匹配为整个场景提供全局运动监督，相机流匹配则锁定静态区域的结构稳定性——两者形成互补的自校正信号，驱动 3D 运动学习，全程无需任何外部运动先验。

### 补充图表

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2604_01561/figures/004_Figure_4.jpg]]
*Figure 4: Self-correction flow matching mechanism. (a) Different Motion and Flow in the 4D Scene. Static areas move only due to camera motion (camera flow), while dynamic areas involve both camera and object motion (full flow). Accurate motion learning requires region-specific flow supervision. (b) Self-correction flow matching. We apply full flow to warp the entire image from state t1 to state*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2604_01561/figures/002_Figure_2.jpg]]
*Figure 2: Motivation of Self-correction Flow Matching. (a) We start with a simple observation: 2D observations, such as the shifting balloon, are caused by 3D motion. Accurate reconstructed 3D Motion should naturally align with these visible changes. (b) Unlike previous methods that use external motion priors to supervise 3D motion, we instead uses raw video as motion supervision through a self-correction flow matching mechanism to directly align predicted 3D motion projections with 2D frame differences*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2604_01561/figures/011_Figure_8.jpg]]
*Figure 8: Illustration of the computation of Full Flow (top-left) and Camera Flow (bottom-right)*

## 实验与分析

### 核心发现：自校正流匹配的有效性

ReFlow 在两个主流单目动态场景基准上均取得最优性能，验证了“用原始视频作为运动监督信号”这一核心设计理念。

**Nvidia Monocular 数据集**：如 Table 1 所示，ReFlow 在平均指标上全面超越此前最优方法 **MoDec-GS**，PSNR 提升 **+1.57 dB**（28.20 vs 26.63），SSIM 提升 **+0.024**（0.903 vs 0.879），LPIPS 降低 **0.057**（0.103 vs 0.160）。逐场景分析显示，ReFlow 在 Balloon1、Balloon2、Jumping、Playground、Skating、Truck、Umbrella 七个场景中均取得最优 PSNR/SSIM/LPIPS，尤其在 Playground 场景中优势显著——该场景包含复杂的多人交互与快速运动，恰好是外部光流方法容易失效的情形。

**Nerfies-HyperNeRF 数据集**：如 Table 2 所示，ReFlow 同样超越所有对比方法。在 Broom 场景中，ReFlow 的 PSNR 达到 23.97，相较基线 **4DGS** 的 22.00 提升 **+1.97 dB**，相较 **HyperNeRF** 等动态 NeRF 方法优势更为明显。该数据集采用跨相机视角评估（训练与测试使用不同同步相机），对运动建模的泛化性要求更高，ReFlow 的领先表现说明自校正机制学习到的运动具有较好的跨视角一致性。

定性对比（Figure 5、Figure 6）进一步揭示：在 MoDec-GS 出现模糊或伪影的细节区域（如快速移动的肢体边缘、小物体纹理），ReFlow 能恢复更清晰的几何结构与纹理。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2604_01561/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison on Nvidia Monocular dataset [18]. Yellow boxes highlight zoomed-in regions for detail examination. Per-scene average PSNR values are provided*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2604_01561/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative comparison on Nerfies-HyperNeRF dataset [45, 46]. Yellow boxes highlight zoomed-in regions for detail examination. Per-scene average PSNR values are provided*

### 消融实验：各模块贡献的逐层拆解

Table 3 的消融实验以 **4DGS** 为基线（PSNR 25.81），按模块逐步叠加，清晰揭示了各组件的因果贡献：

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2604_01561/figures/010_Table_3.jpg]]
*Table 3: Ablation study of key components in our method. CompInit.: Complete Canonical Space Initialization; Sep.: Separation-based Dynamic Scene Modeling; FullFM: Full Flow Matching; CamFM: Camera Flow Matching. We highlight best performance in bold*

| 配置 | PSNR | Δ PSNR | 累积增益 |
|------|------|--------|----------|
| 基线 4DGS | 25.81 | — | — |
| + Full Flow Matching | 26.45 | +0.64 | +0.64 |
| + Complete Canonical Space Init | 26.60 | +0.15 | +0.79 |
| + Separation-Based Modeling | 27.00 | +0.40 | +1.19 |
| + Full Flow Matching (完整) | 27.85 | +0.85 | +2.04 |
| + Camera Flow Matching (最终) | **28.20** | +0.35 | **+2.39** |

**关键洞察**：

1. **自校正流匹配是最大单一增益来源**：在基线 4DGS 上直接加入 Full Flow Matching 即可带来 +0.64 dB 的提升，证明仅通过 warped 帧与真实帧的差异监督 3D 运动，无需任何外部先验，即可显著改善重建质量。

2. **完整规范空间初始化与静动态分离形成协同效应**：CompInit 单独贡献 +0.15 dB，Sep 在此基础上贡献 +0.40 dB。两者结合为后续的区域化流匹配提供了干净的“画布”——静态区域稳定、动态区域完整，使得流匹配的监督信号更加精准。

3. **相机流匹配是精细化提升的关键**：在已有 Full Flow Matching 的基础上，Camera Flow Matching 额外贡献 +0.35 dB。这一增益源于对静态区域施加仅由相机运动导出的流约束，有效消除了动态建模对静态结构的“污染”，防止虚假运动漂移。

### 自校正 vs 外部光流：一个关键对比实验

Table 6 对比了 ReFlow 的自校正流匹配与使用外部光流（RAFT）作为伪真值的变体 **Ours (External Flow)**。结果极具启发性：

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2604_01561/figures/016_Table_6.jpg]]
*Table 6: Quantitative comparison using PSNR(↑), SSIM(↑), and LPIPS(↓) metrics. Best results are in bold*

- 在 Playground 场景中，自校正方法 PSNR 为 25.58，而 External Flow 变体仅为 20.97，差距高达 **+4.61 dB**。
- 在其他多数场景中，自校正方法同样优于或持平 External Flow 变体。

**失败机制分析**：外部光流在相机运动为主导或小物体快速移动的场景中，容易产生估计误差。当这些错误的光流信号被用作硬约束监督 3D 运动时，会直接导致运动建模偏差，进而污染渲染质量。ReFlow 的自校正机制通过直接比较 warped 帧与真实帧的像素级差异，天然规避了外部估计器的误差传播问题——这是一个“端到端一致性”优于“中间表示监督”的典型案例。

### 效率与开销

Table 4 和 Table 5 报告了训练与推理效率。ReFlow 的训练时间相较基线 4DGS 增加约 30%，峰值 GPU 显存增加 1–2 GB，主要开销来自流渲染和规范空间构建的额外计算。渲染速度（FPS）下降约 10–20%，模型存储大小增加 20–50 MB。值得注意的是，这些开销仅存在于训练阶段，推理时无额外计算负担，保持了与基线相同的渲染管线。

### 失败模式与局限性

Figure 9 展示了 ReFlow 的一个典型失败案例：当场景中出现物体突然出现/消失或发生剧烈拓扑变化时，所依赖的几何基础模型难以建立可靠的帧间对应，导致聚合点云出现噪声和畸变。这种初始化的质量退化会级联影响后续的运动学习，最终导致重建失败。该问题本质上源于 ReFlow 的逐场景优化范式对初始化的敏感性——这是与可泛化的前馈方法（如 Table 7 所述）相比的结构性局限。

### 训练过程中的自校正演进

Figure 10 可视化了训练过程中自校正流匹配的逐步收敛过程。以 DynamicFace 序列为例，在训练初期（迭代 300），warped 图像 $I_1^{warped}$ 与目标帧 $I_2$ 存在显著偏差；随着训练推进（迭代 1000 → 5000 → 7000），$I_1^{warped}$ 逐渐逼近 $I_2$，面部细节和边缘对齐持续改善。这一可视化直接证明了自校正机制的有效性：无需任何外部运动标签，3D 运动在“预测-比较-校正”的闭环中逐步收敛到与 2D 观测一致的状态。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2604_01561/figures/015_Figure_10.jpg]]
*Figure 10: Visualization of our self-correction flow matching progress across training iterations, using the DynamicFace sequence from the Nvidia Monocular dataset [18]. Each row shows results at different training iterations: 300 (top row), 1000 (second row), 5000 (third row), and 7000 (bottom row). The columns present: Left column*

### 补充图表

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2604_01561/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on Nvidia Monocular dataset. We report PSNR/SSIM/LPIPS per scene; the last block shows the mean across all available scenes (including dynamicFace when available)*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2604_01561/figures/009_Table_2.jpg]]
*Table 2: Quantitative comparison on Nerfies-HyperNeRF dataset [45, 46]. We highlight the best and second best results*

## 方法谱系与知识库定位

### 1. 方法继承与基线对照

ReFlow 的方法谱系可追溯至两条主线：**3D Gaussian Splatting（3DGS）静态重建** 与 **基于变形的动态场景重建**。其直接技术基座为 **4DGS**，该框架在 3DGS 基础上引入时间条件变形场，将规范空间的高斯球体映射到各时间步。然而，4DGS 继承了 3DGS 的固有局限：初始化依赖 COLMAP 等静态 SfM 点云，导致动态区域覆盖不完整，且所有高斯球体在统一变形场中混合建模，缺乏静动态分离机制。

ReFlow 在 4DGS 基线上进行了三个关键槽位的替换：

- **场景初始化方式**：从 COLMAP 静态 SfM 点云 → 几何基础模型（如 ）构建的完整规范空间（Complete Canonical Space Construction）。该模块通过粗到细的全局对齐，从全视频帧中聚合静态与动态区域的完整点云，并利用几何基础模型提供的动态掩码实现静动态点云的显式分离。这一改进直接解决了基线中动态区域初始化缺失的根本问题。

- **静动态建模架构**：从统一变形场 → 分离式动态场景建模（Separation-Based Dynamic Scene Modeling）。静态组件使用三平面空间特征解码，动态组件额外引入时间平面特征，使两类区域在特征层面解耦，为后续区域化运动约束提供了结构化基础。

- **运动监督机制**：从纯光度渲染损失 → 自校正流匹配（Self-correction Flow Matching）。这是 ReFlow 最核心的方法论创新——将 3D 运动投影为 2D 流场，通过比较 warped 帧与实际帧的差异来直接调整 3D 运动参数，形成"运动预测 → 流投影 → 帧差异反馈 → 运动修正"的自校正循环。该机制完全摒弃了 **STGS**、**Ex4DGS**、**Efficient-D3DGS** 等方法中常用的外部密集运动先验（如 RAFT 光流、点跟踪），将原始视频本身作为唯一的运动监督信号。

与当前最优方法 **MoDec-GS** 相比，ReFlow 在 Nvidia Monocular 数据集上取得了 +1.57dB 的 PSNR 提升（28.20 vs 26.63），在 Nerfies-HyperNeRF 数据集上也全面超越。这一优势在动态区域复杂的场景（如 Playground）中尤为显著——ReFlow 的自校正方法比使用外部光流监督的变体高出 4.61dB PSNR（25.58 vs 20.97），表明外部光流在复杂运动场景下可能提供误导信号，而自校正机制通过直接对齐视频帧差异避免了这一错误传播。

### 2. 适用边界与局限

**适用场景**：ReFlow 主要面向单目动态场景重建，适用于相机运动与物体运动并存的通用 4D 场景。其自校正机制在以下条件下表现最佳：
- 场景具有相对完整的几何覆盖，且不存在剧烈的物体出现/消失或拓扑变化；
- 视频帧间存在可被流场捕获的像素级对应关系；
- 相机位姿可通过 SfM 或几何基础模型可靠估计。

**已知局限**：

1. **几何质量依赖**：整体性能受限于场景几何的质量。当物体出现/消失或发生拓扑变化时（如 Figure 9 所示），几何基础模型难以建立可靠对应，导致重建失败。这是当前方法的根本性瓶颈。

2. **计算开销增加**：相比基线 4DGS，ReFlow 引入了约 30% 的额外训练时间和 1-2GB 的显存开销（Table 4），主要来自流渲染和规范空间构建的额外计算。渲染速度（FPS）降低约 10-20%，模型存储增大 20-50MB（Table 5），但推理时无额外计算负担。

3. **逐场景优化范式的固有限制**：ReFlow 属于逐场景优化方法，对初始化敏感，且无法像前馈方法（如预训练 GS 模型）那样在多个场景间泛化。尽管其输出初始化可与其他模型的输出结合（Table 7 讨论），但本质上仍需要针对每个新场景进行完整训练。

4. **极端运动的处理能力**：在物体快速移动或相机运动剧烈时，流场估计的准确性可能下降，进而影响自校正信号的质量。当前方法未显式处理遮挡区域的流场不连续性。

### 3. 开放问题与后续方向

**核心开放问题**：ReFlow 正面回答了"能否从纯 2D 观测中解锁 4D 动态场景重建"这一根本问题，并给出了肯定答案。然而，以下方向仍有待探索：

1. **复杂拓扑变化下的鲁棒性**：当场景中出现物体出现/消失、非刚性变形或拓扑结构改变时，当前的自校正流匹配机制缺乏有效的处理策略。如何将流匹配与更灵活的几何表示（如基于 NeRF 的密度场或隐式表面）结合，是一个值得深入的方向。

2. **与先进几何基础模型的融合**：ReFlow 的规范空间构建依赖几何基础模型，其性能上限受限于该模型的输出质量。随着 Align3r、MegaSAM 等更强大的几何基础模型的出现，将自校正流匹配机制与这些模型结合，有望在极端场景下取得突破。

3. **前馈与优化的混合范式**：Table 7 的讨论暗示了一个潜在方向——利用大规模预训练的前馈 GS 模型提供初始化和运动先验，再通过自校正流匹配进行逐场景精炼。这种混合范式可能兼顾泛化能力和重建精度。

4. **多模态运动监督的融合**：虽然 ReFlow 证明了纯视频监督的可行性，但在某些场景下，稀疏的外部运动先验（如语义关键点匹配）可能提供互补信息。如何在不引入错误传播的前提下选择性融合多模态信号，是一个开放的设计问题。

5. **实时或近实时的自校正重建**：当前方法的训练时间开销限制了其在实时应用中的部署。通过流渲染的近似计算、规范空间构建的增量更新等工程优化，有望将自校正机制推向在线场景。

## 原文 PDF

![[paperPDFs/CVPR_2026/ReFlow_Self_correction_Motion_Learning_for_Dynamic_Scene_Reconstruction.pdf]]