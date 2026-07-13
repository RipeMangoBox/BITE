---
title: Real-Time Dynamic Scene Rendering with Controlled Compressibility and Contact Awareness
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Real_Time_Dynamic_Scene_Rendering_with_Controlled_Compressibility_and_Contact_Awareness.pdf
project_link: null
code_link: null
aliases:
- SADRCCCUSAF
- RTDSRCCCA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 在连续性方程中显式引入源项（source-sink field）以及在隐式约束曲面上实施非穿透和库仑摩擦约束，从而联合控制可压缩流动和接触行为。
primary_logic: 通过源增强的连续性方程、压缩感知的速度场先验（Helmholtz分解、各向异性子空间、仿射族）以及基于隐式曲面的接触约束，可将密度变化、外观变化和物理接触分离，并在可微渲染流水线中通过投影式求解器高效实现。
claims:
- 提出了一种统一框架，通过高效并行内求解将预测速度投影到物理先验上，包括Helmholtz参数化、可压缩方向先验和仿射族。
- 引入源项明确分离了运动驱动的密度变化与真正的产生或湮灭，保持了连续性。
- 通过隐式曲面表示障碍物并构造法向和切向物理先验，从而施加几何约束，处理曲面障碍物。
- Plenoptic Video Dataset 上 PSNR = 33.84
---

# Real-Time Dynamic Scene Rendering with Controlled Compressibility and Contact Awareness

> [!tip] 核心洞察
> 通过源增强的连续性方程、压缩感知的速度场先验（Helmholtz分解、各向异性子空间、仿射族）以及基于隐式曲面的接触约束，可将密度变化、外观变化和物理接触分离，并在可微渲染流水线中通过投影式求解器高效实现。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于可控压缩与接触感知的实时动态场景渲染 |
| 英文题名 | Real-Time Dynamic Scene Rendering with Controlled Compressibility and Contact Awareness |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Shi_Real-Time_Dynamic_Scene_Rendering_with_Controlled_Compressibility_and_Contact_Awareness_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Source-Aware Dynamic Rendering with Compressibility and Contact Constraints (Unified Source-Aware Framework) |
| Dataset | Plenoptic Video Dataset, D-NeRF Dataset |

> [!tip] 效果简介
> - Plenoptic Video Dataset 上，PSNR 33.84 vs ≈30.84 (strongest prior) (+3.0 dB)。
> - D-NeRF Dataset 上，PSNR / SSIM / LPIPS 35.24 / 0.99 / 0.02 vs 优于所有NeRF和Gaussian基线 (显著提升)。

## 概要

动态场景渲染的核心挑战在于，真实世界中的运动往往伴随**压缩、膨胀、生长、衰减以及物体间的接触与摩擦**，而现有方法普遍依赖不可压缩、无源的运动假设，导致遮挡边界和接触区域的伪影难以消除。本文提出了一种**源感知的统一动态渲染框架**，在连续性方程中显式引入源-汇场（source-sink field）来分离运动驱动的密度变化与真正的物质产生/湮灭，同时通过基于隐式曲面的非穿透和库仑摩擦约束来处理接触行为。

方法的核心思路是将网络预测的速度场投影到物理先验上，包括：**(i)** 将速度分解为无散度分量与势流分量的 **Helmholtz 参数化**；**(ii)** 限制体积变化方向于指定子空间的**各向异性可压缩方向先验**；以及 **(iii)** 解耦旋转与各向同性缩放的**仿射运动族**。接触约束则通过逐样本的闭式投影和二阶锥规划实现，无需额外的软惩罚项。

在 **Plenoptic Video Dataset** 上，本方法达到 **33.84 dB PSNR**，较最强先前方法提升 **+3.0 dB**；在 **D-NeRF Dataset** 上取得 **35.24 dB PSNR / 0.99 SSIM / 0.02 LPIPS**，全面优于 NeRF 基线和 3D Gaussian 基线（如 **K-Planes** (Fridovich-Keil et al., CVPR 2023)、**Deformable 3D Gaussians** (Yang et al., arXiv 2023)）。消融实验表明，源感知可压缩流和接触约束各自独立带来显著精度增益，且几乎不增加计算开销；局部线性场投影在质量与效率间取得最优权衡。

方法仍存在对光照变化、遮挡和传感器噪声敏感的局限，隐式曲面重建依赖准确的深度或掩膜信息，接触检测的超参数（阈值 $\varepsilon$、摩擦系数 $\mu$）需场景适配，且当前框架假设速度场分段光滑，对剧烈断裂或拓扑变化场景的泛化能力有待验证。



### 动态场景渲染的核心挑战

从多视角视频中重建和渲染动态三维场景是计算机视觉与图形学中的基本问题，在虚拟现实、增强现实、电影制作和自由视点视频等应用中具有广泛需求。近年来，以神经辐射场（**NeRF**，Mildenhall et al., ECCV 2020）和三维高斯泼溅（**3DGS**，Kerbl et al., ACM TOG 2023）为代表的神经渲染方法在静态场景重建上取得了突破性进展。然而，将这些方法扩展到动态场景时，一个根本性的瓶颈逐渐浮现：**现有方法普遍假设场景运动是不可压缩、无源的**，即物体的运动仅表现为几何形变，而不会发生体积膨胀、收缩或物质的产生与湮灭。

这一假设在理想化的合成场景中或许成立，但在真实世界中却频繁失效。火焰的燃烧与蔓延、烟雾的扩散与消散、软体组织的形变与接触、流体的飞溅与融合——这些现象都涉及**压缩、膨胀、接触等物理效应**。当现有方法强行用不可压缩运动模型去拟合这些现象时，往往在遮挡边界和接触区域产生显著的伪影，表现为模糊、几何失真或时间不连贯。

### 现有方法的两个关键缺口

**缺口一：连续性方程中缺失源项。** 经典的动态场景渲染流水线，无论是基于形变场的方法（如 **Deformable 3D Gaussians**，Yang et al., arXiv 2023）还是基于时空分解的方法（如 **K-Planes**，Fridovich-Keil et al., CVPR 2023），其底层运动模型都隐含地依赖无源传输假设。这意味着密度或外观的变化被完全归因于速度场的散度效应，而无法区分“运动驱动的密度变化”与“真正的产生或湮灭”。当场景中存在火焰生长、烟雾消散等源-汇行为时，模型被迫用不恰当的形变来解释外观变化，导致重建质量下降。

**缺口二：缺乏显式的接触约束。** 在动态场景中，物体与障碍物之间的交互——如手与桌面的接触、流体与容器壁的碰撞——会产生复杂的边界行为。现有方法要么完全忽略接触约束，要么仅通过数据驱动的软惩罚间接处理，缺乏对**非穿透条件**和**摩擦行为**的显式建模。这使得重建结果在接触区域容易出现穿透、滑移不自然等物理不一致现象。

### 本文动机与核心思路

针对上述瓶颈，本文提出了一种**源感知的动态渲染统一框架**，其核心思路是在可微渲染流水线中显式引入物理先验，通过投影式求解器将网络预测的速度场约束到物理合理的子空间上。具体而言，本文从三个层面突破现有方法的局限：

1. **源增强的连续性方程**：在连续性方程中显式引入源-汇场 $q$，将运动驱动的密度变化与真正的物质产生/湮灭解耦，使模型能够自然地处理生长、衰减等现象。
2. **可压缩速度场先验**：通过 Helmholtz 分解将速度场分离为无散度分量和势流分量，并进一步将可压缩分量限制在各向异性的预设子空间内，从而在保持辨识度的前提下允许可控的体积变化。
3. **基于隐式曲面的接触约束**：利用隐式曲面表示障碍物，构造法向和切向的物理先验，在投影求解中施加非穿透条件和库仑摩擦约束，确保接触区域的几何一致性和物理合理性。

这些物理先验以高效并行的内层求解方式集成到可微渲染流水线中，在几乎不增加计算开销的前提下，显著提升了动态场景的重建质量和时间稳定性。



## 核心方法与创新机理

本工作围绕动态场景渲染中两个被现有方法系统性忽视的物理瓶颈，提出了**统一源感知框架（Unified Source-Aware Framework）**。核心创新并非提出全新的表示结构，而是在现有可微渲染流水线中嵌入三个物理驱动的“变化槽”（changed slots），通过高效的投影式内层求解将网络预测速度约束到物理合理流形上。

### 创新一：源增强的连续性方程——分离运动驱动与内在变化

现有动态渲染方法（如 **Deformable 3D Gaussians**（Yang et al., arXiv 2023））普遍假设无源传输，即场景外观的变化完全由速度场驱动的平流解释。这一假设在现实场景中频繁失效：火焰的生长与熄灭、烟雾的生成与消散、物体的出现与消失，均涉及“产生”或“湮灭”而非单纯的物质重分布。

本文的核心操作是**在连续性方程中显式引入源-汇场（source-sink field）$q$**：

$$
\partial _ { t } \psi + u \cdot \nabla \psi + \psi \nabla \cdot u = q
$$

该方程将光测变化分解为三个可区分的物理机制：
- **平流项** $u \cdot \nabla \psi$：速度场驱动的空间输运；
- **压缩项** $\psi \nabla \cdot u$：速度散度引起的密度变化；
- **源项** $q$：真正的物质产生或湮灭，与运动无关。

这一分离的因果意义在于：当场景中出现外观变化时，框架可以判断其源于运动压缩（由速度散度解释）还是源于独立的源过程（由 $q$ 解释），从而避免将源效应错误地归因于速度场，导致遮挡边界的运动伪影。在图像平面上，该约束通过最小二乘残差实现：

$$
\rho ( u , q ; \psi _ { t } ) = \sum _ { i } \Bigl [ s _ { i } + g _ { i } ^ { \top } u ( x _ { i } , t ) + \psi _ { i } ( \nabla \cdot u ) ( x _ { i } , t ) - q ( x _ { i } , t ) \Bigr ] ^ { 2 }
$$

速度场 $u$ 与源场 $q$ **联合估计**，而非分步后处理，确保两者在优化过程中相互一致。

### 创新二：压缩感知的速度场先验族——从不可压缩到可控压缩

现有方法的速度场先验通常局限于不可压缩（无散）假设或简单的方向性约束，无法表达现实世界中普遍存在的压缩与膨胀效应（如呼吸、挤压、热胀冷缩）。本文构建了一个**可压缩速度场先验的层次化族**，通过三个递进的参数化形式控制压缩自由度：

1. **Helmholtz 分解**：将速度场显式分离为无散分量与势流分量——
   $$
   u ( x , t ) = \sum _ { k } \beta _ { k } ( t ) b _ { k } ( x ) + \sum _ { \ell } \alpha _ { \ell } ( t ) \nabla \phi _ { \ell } ( x )
   $$
   其中散度完全由势流分量承载：$\nabla \cdot u = \sum _ { \ell } \alpha _ { \ell } ( t ) \Delta \phi _ { \ell } ( x )$。这使框架可以在保持无散运动的同时，选择性激活压缩模式。

2. **各向异性子空间压缩**：将体积变化限制在低维子空间内——
   $$
   \nabla \cdot u = \mathrm { t r } \big ( P \nabla ^ { 2 } \Phi \big ) = \sum _ { k = 1 } ^ { r } \frac { \partial ^ { 2 } \Phi } { \partial \xi _ { k } ^ { 2 } } , \qquad \xi = V ^ { \top } x
   $$
   通过在降维坐标 $\xi$ 中建模散度，大幅减少压缩自由度的数量，在表达能力与计算效率之间取得平衡。

3. **仿射运动族**：将局部运动解耦为旋转与各向同性缩放，进一步约束可压缩模式的结构。

这三种先验通过**投影式求解器**实施：网络预测的原始速度场被投影到满足选定先验的最近可行解上，投影过程通过凸最小二乘或小规模二阶锥规划高效求解。消融实验表明，仅启用源感知可压缩流（无接触约束）即可在基准上获得显著准确率提升，且几乎无额外计算成本（Table 3, config b vs a）。

### 创新三：基于隐式曲面的接触约束——从软惩罚到硬几何约束

动态场景中物体与障碍物的交互（如手与桌面接触、工具与物体碰撞）是现有方法的主要失败模式之一。基线方法通常不施加任何接触约束，或仅使用软惩罚项，导致穿透伪影和滑动不自然。

本文的创新在于**将接触建模从速度先验的范畴提升为流形约束**：
- 使用隐式曲面表示障碍物，在每个高斯原语位置构造局部法向 $n_k$ 和切向基；
- 对法向速度分量施加**非穿透投影** $\hat { v } _ { n } = \operatorname*{m a x } ( \bar { v } _ { n } , 0 )$，确保原语不会进入障碍物内部；
- 对切向分量施加**库仑摩擦锥投影**，区分粘滞与滑动状态：
  $$
  \tilde { v } _ { t } = \left\{ \begin{array} { l l } { 0 , } & { \left\| \bar { v } _ { t } \right\| \leq \mu _ { k } \hat { v } _ { n } \quad \mathrm { ( s t i c k ) } , } \\ { \mu _ { k } \hat { v } _ { n } \frac { \bar { v } _ { t } } { \left\| \bar { v } _ { t } \right\| } , } & { \mathrm { ( s l i d e ) } . } \end{array} \right.
  $$

投影后的速度重构为 $u _ { i } ^ { * } = u _ { \mathrm { s u r f } , k } + \hat { v } _ { n } n _ { k } + \tilde { v } _ { t }$。这些投影以逐样本闭式解或极小规模优化实现，可并行处理所有原语，不增加显著的墙钟时间开销。消融实验证实，仅启用流形和接触约束即可改进重建质量，且保持计算耗时不变（Table 3, config c vs a）。

### 创新四：统一的投影-训练协同设计

上述三个创新并非孤立模块，而是通过**投影损失**耦合到端到端训练中：

$$
\mathcal { L } _ { \mathrm { p r o j } } = \sum _ { i = 1 } ^ { n } { w _ { i } \left. { v _ { \theta } ( x _ { i } , t ) - \tilde { v } ( x _ { i } , t ) } \right. _ { 2 } ^ { 2 } }
$$

该损失强制网络预测速度 $v_\theta$ 与投影后速度 $\tilde{v}$ 一致，使物理约束通过梯度信号反向传播至网络参数。同时，逐像素的连续性一致性损失 $\mathcal{L}_{\mathrm{CE}}$ 惩罚投影后速度对源增强传输律的违反。这种“预测-投影-惩罚”的闭环设计，使得物理先验不是后处理修正，而是训练过程的有机组成部分。

### 与基线方法的系统性差异

| 变化槽 | 基线方法 | 本方法 |
|--------|----------|--------|
| **速度场先验** | 不可压缩/无源假设，简单方向性先验 | 可压缩、含源项先验族：Helmholtz分解 → 各向异性子空间 → 仿射族 |
| **接触建模** | 无约束或软惩罚 | 隐式曲面上的非穿透投影 + 库仑摩擦锥投影 |
| **源项处理** | 无显式源项，假设无源传输 | 显式源-汇场 $q$，与速度场联合估计 |

消融实验的最终结论是：**局部线性场（LL）投影变体**在质量与效率之间达到最优权衡（Table 3, config f），验证了将压缩自由度控制在低维子空间中的设计合理性。



本文提出一个**源感知的统一动态渲染框架**，其核心思想是将物理先验——可压缩流动与接触约束——以投影式内求解的形式嵌入可微渲染流水线中，从而在不牺牲实时性的前提下提升动态场景的重建质量与物理合理性。

### 流水线总览

框架的整体数据流如 Figure 1 所示，由四个关键模块串联构成：

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_Real_Time_Dynamic/figures/001_Figure_1.jpg]]
*Figure 1: Framework Overview. We begin with sparse 3D point clouds and encode them into a space–time set of Gaussian primitives, which evolve under a learned deformable field. Compressibility and contact priors jointly constrain the motion of Gaussian primitives, yielding dynamics that are physically consistent and temporally stable. Images are generated with a differentiable rasterization pipeline*

1. **点云编码**：以稀疏三维点云为输入，将其编码为一组时空高斯原语（space–time Gaussian primitives），作为场景的显式表示。
2. **可学习变形场**：高斯原语在可学习的变形场驱动下随时间演化，变形场由神经网络参数化并输出逐点的速度预测。
3. **速度投影求解器**：这是框架的核心创新所在。网络预测的原始速度场并非直接用于驱动原语运动，而是经过一个**投影式内求解器**，将速度投影到物理先验约束的可行域上。该求解器包含两个并行分支：
   - **可压缩流先验投影**：将速度场投影到 Helmholtz 分解、各向异性压缩子空间或仿射运动族上，实现对散度（压缩/膨胀）的显式控制，并引入源项 $q$ 以分离运动驱动的密度变化与真正的产生/湮灭。
   - **接触约束投影**：基于隐式曲面表示障碍物，对接触点处的速度施加非穿透约束（法向分量截断）和库仑摩擦约束（切向分量在摩擦锥上的闭式投影），从而在遮挡边界和接触区域消除伪影。
4. **可微光栅化**：投影后的物理一致速度场驱动高斯原语运动，最终通过可微光栅化流水线生成渲染图像，并与光度损失联合端到端优化。

### 速度投影求解器的内部机制

投影求解器采用迭代策略，每次迭代完成两类闭式运算：

- **压缩感知投影**：将网络预测速度 $v_\theta$ 投影到由 Helmholtz 基函数、各向异性压缩方向或局部仿射场所张成的子空间上，得到满足可压缩性先验的速度场 $\tilde{v}$。同时，源项 $q$ 与速度场联合估计，通过源增强的连续性方程约束两者的耦合关系。
- **接触投影**：对于接近隐式曲面（距离小于阈值 $\varepsilon$）的高斯原语，先计算曲面法向 $n_k$ 和曲面速度 $u_{\text{surf},k}$，然后将相对速度的法向分量截断为非负（$\hat{v}_n = \max(\bar{v}_n, 0)$），再根据库仑摩擦锥将切向分量投影到粘滞或滑动状态。

投影损失 $\mathcal{L}_{\text{proj}}$ 强制网络预测速度与投影后速度保持一致，从而将物理先验作为软约束注入学习过程。

### 关键设计选择

- **源项解耦**：传统方法假设无源传输，将外观变化全部归因于运动，导致压缩、膨胀、生长等效应下的估计偏差。本文显式引入源–汇场 $q$，在连续性方程 $\partial_t \psi + u \cdot \nabla \psi + \psi \nabla \cdot u = q$ 中分离传输与产生/湮灭，使速度场估计更鲁棒。
- **投影而非惩罚**：与常见的软惩罚或正则化项不同，本文采用闭式投影将速度严格约束在物理可行域内，避免了超参数调谐的困难，且计算开销极低。
- **并行化设计**：所有投影操作均可在高斯原语级别并行执行，不引入串行瓶颈，保证了实时渲染能力。



### 源增强连续性方程

现有动态场景重建方法普遍隐含不可压缩与无源假设，即标量场（如密度、颜色）在运动过程中仅被平流传输，既不被压缩也不被产生或湮灭。然而，现实场景中充斥着压缩、膨胀、生长、衰减等现象，这些效应在遮挡边界和接触区域尤为显著，若强行忽略，将导致运动估计偏差与渲染伪影。

本文的核心突破在于**将连续性方程显式地扩展为含源形式**。设标量场为 $\psi(x,t)$（可表示密度、颜色或高斯原语的不透明度），速度场为 $u(x,t)$，则统一的传输规律为：

$$
\partial _ { t } \psi + u \cdot \nabla \psi + \psi \nabla \cdot u = q
$$

其中 $q(x,t)$ 为**源–汇场**（source–sink field），显式建模标量场中与运动无关的产生或湮灭。当 $q>0$ 时表示标量“产生”（如物体生长、新表面显现），$q<0$ 时表示“湮灭”（如衰减、消融）。当 $q=0$ 且 $\nabla \cdot u = 0$ 时，该方程退化为经典的无源不可压缩平流方程，即现有方法的隐含假设。

该方程的关键意义在于**将密度变化解耦为两个独立来源**：运动驱动的压缩/膨胀（$\psi \nabla \cdot u$ 项）与真正的物质产生/湮灭（$q$ 项）。这一解耦使得框架能够同时处理可压缩流动和非运动性外观变化，而不会将二者混淆。

### 图像平面上的连续性残差

为从观测数据中估计速度场和源场，本文将上述连续性方程投影到二维图像平面上，构造逐帧的最小二乘残差。对于时刻 $t$ 的图像，定义：

$$
\rho ( u , q ; \psi _ { t } ) = \sum _ { i } \Bigl [ s _ { i } + g _ { i } ^ { \top } u ( x _ { i } , t ) + \psi _ { i } ( \nabla \cdot u ) ( x _ { i } , t ) - q ( x _ { i } , t ) \Bigr ] ^ { 2 }
$$

其中 $x_i$ 为像素位置，$s_i$ 和 $g_i$ 分别表示该像素处的标量时间导数和空间梯度（通过图像序列的有限差分或可微网络获得），$\psi_i$ 为当前标量值。该残差惩罚了每个像素上连续性方程的违反程度，是后续速度场投影求解的核心目标函数。

### 速度场的物理先验参数化

直接从高维数据中估计无约束的速度场极易过拟合到噪声和遮挡区域。本文提出三类物理先验，将预测速度投影到结构化的低维子空间上。

**（1）亥姆霍兹分解（Helmholtz Parameterization）**

根据亥姆霍兹定理，任意足够光滑的速度场可唯一分解为无散度分量与无旋（势流）分量之和：

$$
u ( x , t ) = \sum _ { k } \beta _ { k } ( t ) b _ { k } ( x ) + \sum _ { \ell } \alpha _ { \ell } ( t ) \nabla \phi _ { \ell } ( x )
$$

其中 $b_k(x)$ 为无散度基函数（$\nabla \cdot b_k = 0$），$\phi_\ell(x)$ 为标量势函数，$\beta_k(t)$ 和 $\alpha_\ell(t)$ 为时变系数。该分解的优势在于：散度完全由势流分量承担，即

$$
\nabla \cdot u = \sum _ { \ell } \alpha _ { \ell } ( t ) \Delta \phi _ { \ell } ( x )
$$

这使得对压缩性的控制可以**仅通过调节势流系数 $\alpha_\ell$ 来实现**，而无散度分量负责描述不可压缩的旋转运动，二者各司其职。

**（2）各向异性可压缩方向先验（Anisotropic Compressible Directional Prior）**

进一步地，本文将体积变化限制在预设的低维子空间内。设 $V$ 为 $d \times r$ 的正交矩阵（$r \ll d$），定义子空间坐标 $\xi = V^\top x$，则散度可表示为：

$$
\nabla \cdot u = \mathrm { t r } \big ( P \nabla ^ { 2 } \Phi \big ) = \sum _ { k = 1 } ^ { r } \frac { \partial ^ { 2 } \Phi } { \partial \xi _ { k } ^ { 2 } } , \qquad \xi = V ^ { \top } x
$$

其中 $P = VV^\top$ 为子空间投影矩阵，$\Phi$ 为势函数。该参数化将可压缩自由度从 $O(d^2)$ 降至 $O(r)$，在保留主要形变模式的同时大幅提升了计算效率和数值稳定性。

**（3）仿射运动族（Affine Family）**

对于局部区域的运动，仿射变换可同时描述旋转、缩放和剪切。本文引入仿射族先验，将旋转与各向同性缩放解耦，使得网络只需预测少量仿射参数即可表达复杂的局部运动模式。

### 投影式求解与训练目标

上述物理先验通过一个**凸投影求解器**施加于网络预测的速度场 $v_\theta$ 上，得到投影后的速度场 $\tilde{v}$。投影过程为逐样本的闭式求解或小规模二阶锥规划，可高效并行化。

训练时，**投影损失**强制网络预测与物理投影结果一致：

$$
\mathcal { L } _ { \mathrm { p r o j } } = \sum _ { i = 1 } ^ { n } { w _ { i } \left. { v _ { \theta } ( x _ { i } , t ) - \tilde { v } ( x _ { i } , t ) } \right. _ { 2 } ^ { 2 } }
$$

其中 $w_i$ 为像素权重。同时，**连续性一致性损失**惩罚投影后速度场对源增强传输律的违反：

$$
\mathcal { L } _ { \mathrm { C E } } = \sum _ { i } \Big | \partial _ { t } \psi _ { t } ( x _ { i } ) + \nabla \psi _ { t } ( x _ { i } ) ^ { \top } \tilde { v } ( x _ { i } , t ) + \psi _ { t } ( x _ { i } ) \left( \nabla \cdot \tilde { v } \right) ( x _ { i } , t ) - q ( x _ { i } , t ) \Big | ^ { 2 }
$$

两项损失共同作用：投影损失确保网络输出服从物理结构，连续性损失确保投影后的场在观测数据上自洽。

### 接触约束的闭式投影

对于涉及障碍物或自接触的场景，本文在隐式曲面上施加**非穿透约束**和**库仑摩擦约束**。设障碍物表面由隐函数 $f(x)=0$ 定义，表面法向量为 $n = \nabla f / \|\nabla f\|$，表面点速度为 $u_{\mathrm{surf},k}$。

首先将相对速度投影到法向，强制非穿透：

$$
\hat { v } _ { n } = \operatorname* { m a x } ( \bar { v } _ { n } , 0 )
$$

其中 $\bar{v}_n$ 为原始法向分量。该操作确保速度不会指向障碍物内部。

随后对切向分量施加库仑摩擦锥投影，区分粘滞与滑动状态：

$$
\tilde { v } _ { t } = \left\{ \begin{array} { l l } { 0 , } & { \left\| \bar { v } _ { t } \right\| \leq \mu _ { k } \hat { v } _ { n } \quad \mathrm { ( s t i c k ) } , } \\ { \mu _ { k } \hat { v } _ { n } \frac { \bar { v } _ { t } } { \left\| \bar { v } _ { t } \right\| } , } & { \mathrm { ( s l i d e ) } . } \end{array} \right.
$$

其中 $\mu_k$ 为库仑摩擦系数。当切向相对速度的模小于摩擦锥半径 $\mu_k \hat{v}_n$ 时，物体粘滞于表面；否则沿摩擦锥表面滑动。

最终投影后的速度为：

$$
u _ { i } ^ { * } = u _ { \mathrm { s u r f } , k } + \hat { v } _ { n } n _ { k } + \tilde { v } _ { t }
$$

该投影为逐样本的闭式操作，可在保持实时性的同时实现物理上合理的接触行为。



## 实验与关键发现

### 主实验结果

本文在两个标准动态场景基准上系统评估了所提框架。

**Plenoptic Video Dataset** 上的定量比较（Table 1）表明，该方法取得了 **33.84 dB** 的 PSNR，相比最强先验方法提升约 **+3.0 dB**。对比对象涵盖 NeRF 类方法（如 **K-Planes**，Fridovich-Keil et al., CVPR 2023）和高斯类方法（如 **Deformable 3D Gaussians**，Yang et al., arXiv 2023）。定性结果（Figure 2）进一步显示，该方法在运动表面渲染上能够产生物理上更合理的遮挡边界和接触区域，伪影明显减少。

**D-NeRF Dataset** 上的结果（Table 2）同样具有竞争力：PSNR 达 **35.24 dB**，SSIM 达 **0.99**，LPIPS 低至 **0.02**，全面超越包括 **NeRF**（Mildenhall et al., ECCV 2020）和 **3DGS**（Kerbl et al., ACM TOG 2023）在内的所有 NeRF 类与高斯类基线。这一优势源于可压缩流动先验与接触约束的联合作用，使得密度变化和外观变化被有效分离，从而在复杂变形场景中保持了时序一致性。

### 消融实验

Table 3 在 D-NeRF 数据集上系统拆解了各组件的贡献。基线配置（a）为无物理先验的纯可变形场。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_Real_Time_Dynamic/figures/004_Table_3.jpg]]
*Table 3: Ablation Study on the D-NeRF Dataset. GP represents the Gaussian-primitive level projection, LL represents the locallinear field projection*

- **源感知可压缩流（config b vs a）**：仅启用含源项的压缩性先验即可带来显著的精度增益，且几乎不增加计算开销。这验证了显式源-汇场 $q$ 对生长、衰减等非传输性外观变化的建模能力。
- **流形与接触约束（config c vs a）**：仅启用基于隐式曲面的非穿透和库仑摩擦约束，在保持推理耗时不变的前提下改善了重建质量，尤其体现在物体边界和接触区域的几何一致性上。
- **联合启用（config d–f）**：同时启用两类先验可叠加收益。其中，**局部线性场投影（LL）** 变体（config f）在质量与效率之间取得了最优权衡，成为最终推荐配置。定性消融（Figure 3）直观展示了各组件对遮挡边界伪影和接触面滑移的抑制效果。

### 失败模式与局限性

尽管整体性能优异，分析中仍识别出若干失效场景：

1. **光照变化与遮挡敏感性**：速度场和源项估计在光照突变、严重遮挡或传感器噪声下仍较脆弱（引言部分明确指出 *Estimation remains fragile under illumination changes, occlusions, and sensor noise*），可能导致运动估计漂移。
2. **隐式曲面退化**：接触约束依赖于从深度或掩膜信息重建的隐式曲面及其法向。在纹理稀疏或弱纹理区域，曲面估计可能退化，进而影响非穿透投影的准确性。
3. **超参数敏感性**：接触检测依赖于距离阈值 $\varepsilon$，库仑摩擦依赖于摩擦系数 $\mu_k$。这些参数可能需要针对不同场景手动调整，限制了开箱即用的泛化性。
4. **拓扑变化限制**：当前框架假设运动速度场分段光滑，对于剧烈断裂、融合等拓扑变化场景，Helmholtz 分解和投影式求解器的适应性有待验证。

### 关键图表结论

- **Figure 1（框架总览）**：展示了从稀疏 3D 点云编码、可变形场驱动、压缩性与接触先验约束投影，到可微光栅化渲染的完整流水线，明确了各模块间的数据依赖关系。
- **Table 1 & Table 2**：定量证实了源感知可压缩流与接触约束联合建模在 PSNR/SSIM/LPIPS 三个维度上的全面领先。
- **Table 3 & Figure 3**：消融实验揭示了压缩性先验和接触约束的独立贡献及叠加效应，LL 投影变体在精度-效率曲线上构成帕累托最优。
- **Figure 2**：定性对比直观展示了该方法在动态表面渲染中对物理一致性的保持能力，尤其在遮挡边界和接触区域显著优于基线。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_Real_Time_Dynamic/figures/003_Table_1.jpg]]
*Table 1: Quantitative Comparison on Plenoptic Video Dataset. We compare our approach with both NeRF-based and Gaussianbased methods. Our approach outperforms the baselines in PSNR. *: trained on 8 GPUs and tested only on the Flame Salmon scene*

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_Real_Time_Dynamic/figures/005_Table_2.jpg]]
*Table 2: Quantitative Comparison on D-NeRF Dataset. Our approach surpasses both NeRF-based and Gaussian-based baselines in PSNR*

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_Real_Time_Dynamic/figures/002_Figure_2.jpg]]
*Figure 2: Qualitative Comparison on Plenoptic Video Dataset. Our approach outperforms strong baselines by rendering physically plausible moving surfaces*



## 定位与知识库关联

### 方法谱系：从无源不可压缩流到源感知可压缩接触模型

本文提出的统一源感知框架（Unified Source-Aware Framework）位于动态场景渲染方法谱系中“物理先验增强的可微渲染”分支。其核心演进路径可概括为：从静态表示到动态扩展，再从无物理约束的运动场到引入可压缩性与接触约束的物理一致运动场。

**相对于静态基线的演进。** 框架的底层表示建立在 **3DGS**（Kerbl et al., ACM TOG 2023）的可微光栅化流水线之上，将静态高斯原语扩展为时空高斯原语集合，并由可学习的可变形场驱动其运动。这一扩展思路与 **Deformable 3D Gaussians**（Yang et al., arXiv 2023）共享“静态高斯+变形场”的范式，但本文的关键分歧在于对变形场施加的物理约束层次。

**相对于动态基线的方法论跃迁。** 现有动态场景渲染方法——无论是基于NeRF的 **K-Planes**（Fridovich-Keil et al., CVPR 2023）还是基于高斯的变形方法——在运动建模上普遍采用不可压缩或无源的隐式假设。本文的方法论跃迁体现在三个相互耦合的维度：

1. **从无源到源感知**：传统方法将光测变化完全归因于平流传输，假设无源传输。本文在连续性方程中显式引入源-汇场 $q$，将运动驱动的密度变化与真正的产生/湮灭过程解耦，从而能建模生长、衰减等非传输性变化。

2. **从不可压缩到可压缩**：通过Helmholtz分解将速度场拆分为无散度分量和势流分量，并将体变约束在预设的低维子空间内，实现了各向异性、可压缩且源感知的速度场先验。这突破了传统方向性先验的不可压缩限制。

3. **从无接触到接触感知**：将障碍物表示为隐式曲面，并在曲面上构造法向非穿透投影和切向库仑摩擦锥投影，以闭式投影或小型二阶锥规划的形式施加几何约束。这替代了传统方法中缺失接触约束或仅使用软惩罚的做法。

**方法论谱系定位表**（基于verified_analysis中的changed_slots）：

| 方法槽位 | 基线值 | 本文方案 | 核心机制 |
|---------|--------|---------|---------|
| 速度场先验 | 不可压缩/无源假设 | 可压缩、含源项先验 | Helmholtz分解 + 各向异性子空间 + 仿射运动族 |
| 接触建模 | 无约束或软惩罚 | 非穿透 + 库仑摩擦 | 隐式曲面投影 + 二阶锥规划 |
| 源项建模 | 无显式源项 | 源-汇场 $q$ | 与速度场联合估计的凸最小二乘投影 |

### 适用边界与局限

本文框架的适用边界由以下假设和约束共同界定：

**运动光滑性假设。** 框架假设运动速度场是分段光滑的，通过投影式求解器将网络预测速度投影到物理先验上。对于包含剧烈断裂、拓扑变化或冲击波的场景，该光滑性假设可能失效，导致投影引入过大的运动误差。

**隐式曲面的感知依赖。** 接触约束的实施依赖于隐式曲面的准确重建和法向估计。当前框架需要深度或掩膜信息来构造障碍物的隐式表示，在纹理稀疏区域、透明物体或缺乏可靠深度监督的场景中，曲面重建质量可能退化，进而影响接触约束的有效性。

**超参数敏感性。** 接触检测依赖阈值 $\varepsilon$ 来判定高斯原语是否进入接触集，库仑摩擦模型需要预设摩擦系数 $\mu_k$。这些超参数可能需要针对不同场景手动调整，缺乏自适应的设定机制。

**光度脆弱性。** 源感知连续性方程的估计本质上依赖光测一致性假设。在光照变化显著、存在严重遮挡或传感器噪声较大的场景中，速度场和源项的联合估计仍然脆弱（论文引言部分明确指出该局限）。

**多物体交互的扩展性。** 当前框架主要处理单一动态物体与静态障碍物的交互。向多物体非刚性变形和相互接触场景的扩展，需要在接触检测、碰撞求解和计算效率方面进行非平凡的推广。

### 开放问题

基于上述局限，以下开放问题值得进一步探索：

1. **无监督隐式曲面学习**：能否在无掩膜或深度监督的条件下，仅从多视图外观信号中可靠地估计隐式曲面和接触集？这涉及将曲面重建与接触约束形成端到端的联合优化。

2. **拓扑变化与断裂建模**：如何将框架扩展到允许拓扑变化的运动场？可能的路径包括引入间断Galerkin形式的传输方程，或在投影求解器中加入拓扑自适应机制。

3. **源项解耦的可靠性边界**：在纹理极度缺失或运动模糊的极端条件下，速度场与源项的联合估计是否存在不可辨识性？需要从可观测性角度分析解耦的可靠性条件。

4. **端到端可学习的物理先验**：当前框架的物理先验（压缩性子空间维度、摩擦系数、接触阈值等）以手工设定的形式引入。能否将这些先验参数化为可学习的量，使框架在不同场景中自适应地调整物理约束的强度？

5. **计算效率与物理精度的权衡**：消融实验表明局部线性场（LL）投影在质量与效率之间达到最优权衡，但这是否在所有场景类别中普遍成立？是否存在场景自适应的投影粒度选择策略？



## 原文 PDF

![[paperPDFs/CVPR_2026/Real_Time_Dynamic_Scene_Rendering_with_Controlled_Compressibility_and_Contact_Awareness.pdf]]
