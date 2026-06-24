---
title: "Tavatar: Topology-Aware Gaussian Attribute Derivation for Animatable Human Avatars"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Tavatar_Topology_Aware_Gaussian_Attribute_Derivation_for_Animatable_Human_Avatars.pdf
project_link: "https://hailin545.github.io/tavatar/"
code_link: null
aliases:
- Tavatar
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将高斯参数的确定方式从优化驱动转向几何驱动，直接从可变形网格的局部拓扑解析计算尺度、旋转和位置，从而使高斯分布与网格变形严格一致。
primary_logic: 通过将高斯绑定到三角面的内心和顶点，并基于内切圆半径和最小边长解析推导其尺度，同时用正交坐标系对齐局部表面方向，实现了拓扑一致性，无需逐姿势优化即可稳健泛化。
claims:
- 在分布外姿势上，Tavatar将X-Avatar上的法线误差减少13.8%，PeopleSnapshot上减少17.9%，远超最佳基线。
- 消融实验中删除等边正则化后，法线精度从1.772上升到1.834，验证了网格质量对解析映射稳定性的关键作用。
- 仅用Face Gaussian或Vertex Gaussian时，渲染质量和几何一致性显著下降，证实两者互补的必要性。
- PeopleSnapshot 上 PSNR = 28.93
---

# Tavatar: Topology-Aware Gaussian Attribute Derivation for Animatable Human Avatars

> [!tip] 核心洞察
> 通过将高斯绑定到三角面的内心和顶点，并基于内切圆半径和最小边长解析推导其尺度，同时用正交坐标系对齐局部表面方向，实现了拓扑一致性，无需逐姿势优化即可稳健泛化。

| 字段 | 内容 |
|------|------|
| 中文题名 | Tavatar：面向可动画人类化身的拓扑感知高斯属性推导 |
| 英文题名 | Tavatar: Topology-Aware Gaussian Attribute Derivation for Animatable Human Avatars |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Luo_Tavatar_Topology-Aware_Gaussian_Attribute_Derivation_for_Animatable_Human_Avatars_CVPR_2026_paper.html) · [Project](https://hailin545.github.io/tavatar/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Tavatar |
| Dataset | PeopleSnapshot, X-Avatar |

> [!tip] 效果简介
> - PeopleSnapshot 上，PSNR 28.93 vs (best baseline: 28.76 by GoMAvatar) (+0.17)；Normal 1.687 vs (best baseline: 2.055?) (-17.9%)。
> - X-Avatar 上，PSNR 29.03 vs (best baseline: 28.86 by GaussianAvatar) (+0.17)；Normal 1.772 vs (best baseline: 2.055) (-13.8%)。

## 概述

### 问题背景

基于3D高斯泼溅（3DGS）的可动画人类化身重建面临一个关键瓶颈：现有方法通常将高斯的旋转约束在人体网格表面，但将其**尺度（scale）**交由自由优化决定。这种优化驱动的策略导致高斯分布与网格形变在根本上分离——当人体姿势超出训练分布（out-of-distribution, OOD）时，高斯会出现漂浮、脱落或表面孔洞，严重破坏渲染质量和几何一致性。**GaussianAvatar**（Hu et al., CVPR 2024）和**GART**（Lei et al., CVPR 2024）完全依赖非约束优化，**IHuman**（Paudel et al., ECCV 2024）虽约束了旋转却仍放任尺度自由，而**GoMAvatar**（Wen et al., CVPR 2024）虽将高斯绑定到网格表面，但缺乏对网格规则性的保障。这些方法的共同缺陷在于：高斯的几何属性与网格拓扑之间缺乏确定性的因果联系。

### 核心思想

Tavatar 从根本上改变了这一范式，将高斯属性的确定方式从**优化驱动转向几何驱动**。其核心洞察是：如果高斯的尺度、旋转和位置能够直接从可变形网格的局部拓扑中解析计算，那么高斯分布将与网格变形保持严格一致，无需逐姿势优化即可稳健泛化。

具体而言，Tavatar 设计了两种互补的高斯类型：**Face Gaussian** 和 **Vertex Gaussian**。Face Gaussian 绑定于三角面的内心，其面内尺度由内切圆半径解析推导，形成扁平碟状覆盖三角面区域；Vertex Gaussian 锚定于网格顶点，其尺度取决于一环邻域的最小边长，实现局部自适应密度并融合接缝。所有高斯的旋转矩阵通过正交坐标系与局部表面方向对齐，从面法线和顶点面积加权法线解析构建。这一拓扑感知的绑定机制确保了高斯在任何姿势下都与网格结构保持紧密耦合。

### 方法定位

Tavatar 在方法谱系中占据独特位置：它既不同于完全依赖自由优化的方法（如 GaussianAvatar、GART），也超越了仅部分约束旋转的方法（如 IHuman）。与 GoMAvatar 的表面绑定不同，Tavatar 引入了显式的**等边正则化**来维护网格质量，防止极端变形下三角形退化导致解析映射失效。通过将可变形网格作为拓扑支架、解析高斯推导作为绑定机制、等边正则化作为稳定性保障，Tavatar 构建了一个完整的几何驱动化身重建框架。

### 主要结果

在分布外姿势的泛化能力上，Tavatar 展现出显著优势。与最强基线相比，Tavatar 在 X-Avatar 数据集上将法线误差降低了 **13.8%**，在 PeopleSnapshot 上降低了 **17.9%**，验证了拓扑感知绑定对几何一致性的关键作用。渲染质量方面，Tavatar 在 PeopleSnapshot 上达到 PSNR **28.93**，在 X-Avatar 上达到 **29.03**，均优于现有方法。消融实验进一步证实：移除 Face Gaussian 导致 PSNR 下降 1.35 dB，移除 Vertex Gaussian 导致 PSNR 下降 2.57 dB，证明两类高斯的互补必要性；移除等边正则化后法线精度从 1.772 恶化至 1.834，验证了网格质量对解析映射稳定性的支撑作用。

### 局限与展望

Tavatar 的性能依赖于底层 SMPL 模型的拟合精度，初始拟合不准确会限制最终化身质量。当前方法假设服装与身体保持静态拓扑关系，无法处理宽松或动态服装（如裙子飘动）。未来方向包括将解析绑定机制扩展到多对象交互场景、针对关节高频变形区域设计自适应正则化权重，以及探索该范式在非人体对象的动画控制中的应用潜力。

## 背景与动机

### 可动画人类化身重建的挑战

从多视角视频中重建可动画的高保真人类化身，是计算机视觉与图形学领域的核心问题之一，广泛应用于虚拟现实、电影特效和远程交互等场景。近年来，基于 **3D 高斯泼溅**（3D Gaussian Splatting, 3DGS）的方法凭借其高效的渲染速度和优异的视觉质量，逐渐成为该方向的主流范式。这类方法通常将一组三维高斯核绑定到参数化人体模型（如 SMPL）上，通过线性混合蒙皮（Linear Blend Skinning, LBS）驱动高斯随姿态变化，从而实现对任意姿态的动画控制。

### 现有方法的根本瓶颈：优化驱动的属性确定方式

尽管取得了显著进展，现有 3DGS 方法在动画鲁棒性上仍存在一个根本性瓶颈：**高斯的几何属性（位置、旋转、尺度）与驱动网格的形变在优化过程中是分离的**。具体而言：

- **GaussianAvatar**（Hu et al., CVPR 2024）和 **GART**（Lei et al., CVPR 2024）等早期工作将高斯的旋转和尺度完全交由自由优化决定，仅在位置层面与网格保持松耦合。这导致在训练分布外的姿态（out-of-distribution, OOD）下，高斯容易脱离网格表面，出现漂浮或表面孔洞，严重破坏渲染质量。
- **IHuman**（Paudel et al., ECCV 2024）对旋转施加了法线约束，但尺度仍然自由优化，未能从根本上解决高斯与网格形变的分离问题。
- **GoMAvatar**（Wen et al., CVPR 2024）将高斯绑定到网格表面，但缺乏对网格本身规则性的约束，在极端姿态下网格退化同样会导致高斯分布失稳。

这一瓶颈的根源在于：**优化驱动的范式无法保证高斯分布与网格变形之间的一致性**。当训练姿态无法覆盖所有可能的变形模式时，自由优化的几何属性在测试姿态下就会偏离合理的局部几何结构，导致渲染伪影。

### 本文动机：从优化驱动到几何驱动

针对上述问题，**Tavatar** 提出了一种范式转变：将高斯几何属性的确定方式从**优化驱动**转向**几何驱动**。核心思想是：直接从可变形网格的局部拓扑结构解析计算高斯的尺度、旋转和位置，使得高斯分布与网格变形严格一致，无需逐姿态优化即可稳健泛化到 OOD 姿态。

具体而言，Tavatar 设计了两种拓扑绑定高斯——**面高斯**（Face Gaussian）和**顶点高斯**（Vertex Gaussian）——分别绑定到三角面的内心和网格顶点。面高斯的尺度基于三角形的内切圆半径解析推导，顶点高斯的尺度基于一环邻域的最小边长自适应确定；两者的旋转均通过局部正交坐标系与表面方向对齐。这种解析绑定机制确保了高斯在任意姿态下都能保持结构化的网格一致性布局，从根本上消除了高斯漂浮和表面孔洞问题。

此外，Tavatar 引入了**等边正则化**（Equilateral Regularization），显式约束三角网格的边长方差和角度偏离，防止极端姿态下的三角形退化，从而保证解析映射的数值稳定性。这一设计使方法在保持高质量渲染的同时，在几何精度上实现了对现有方法的显著超越——在 X-Avatar 和 PeopleSnapshot 数据集上分别将法线误差降低了 13.8% 和 17.9%。

## 核心创新

Tavatar 的核心创新在于将高斯属性的确定方式从**优化驱动**转向**几何驱动**，彻底改变了现有 3DGS 人体化身方法中高斯与网格形变分离的根本问题。这一范式转换体现在三个相互关联的 changed slots 上。

### 从自由优化到解析推导：高斯尺度的拓扑绑定

现有方法普遍将高斯尺度交由自由优化决定：**GaussianAvatar**（Hu et al., CVPR 2024）和 **GART**（Lei et al., CVPR 2024）完全依赖梯度下降来调整每个高斯的尺度参数；**IHuman**（Paudel et al., ECCV 2024）虽然约束了旋转方向，但仍将尺度作为自由变量优化。这种优化驱动的策略导致高斯与人体网格的形变分离——当训练姿势与测试姿势差异较大时，优化出的尺度参数无法适应新的网格几何，产生高斯漂浮或表面孔洞（见 Figure 2 中 GART 和 IHuman 的失效案例）。

Tavatar 的解决方案是**直接从网格局部拓扑解析计算尺度**，彻底消除尺度优化自由度：

- **Face Gaussian** 的平面内尺度与三角面的内切圆半径 $r_i$ 成正比：$s_{f,x}^i = s_{f,y}^i = \beta \cdot r_i$，其中 $\beta = 0.5$，法向尺度 $s_{f,z}^i = \epsilon = 10^{-3}$，形成扁平碟状高斯（Eq.8）。这意味着无论网格如何变形，Face Gaussian 始终紧密贴合三角形表面，覆盖面积与局部几何严格一致。
- **Vertex Gaussian** 的尺度取决于顶点到其一环邻域的最小边长：$s_{v,x}^j = s_{v,y}^j = \gamma \cdot \min_{\mathbf{v}_k \in \mathcal{N}_1(j)} \|\mathbf{v}_k^p - \mathbf{v}_j^p\|$，$\gamma = 0.5$（Eq.11）。这种设计使得顶点高斯在网格密集区域自动缩小、在稀疏区域自动扩大，实现局部自适应密度，同时保持与网格形变的严格一致。

这一 changed slot 的因果机制在于：尺度不再是一个需要从数据中学习的自由参数，而是网格拓扑的确定性函数。当网格通过 LBS 驱动到 OOD 姿势时，高斯尺度自动跟随局部几何变化，无需逐姿势优化即可保持表面覆盖的完整性。

### 从随机方向到正交坐标系：高斯旋转的拓扑对齐

高斯的旋转矩阵决定了其在 3D 空间中的朝向，对渲染质量和几何一致性至关重要。现有方法中，**GaussianAvatar** 将旋转作为自由参数优化，**IHuman** 虽然将高斯法向约束为网格表面法线，但切线方向仍然随机，导致高斯的各向异性方向与表面特征不对齐。

Tavatar 为每类高斯构建了**基于局部拓扑的正交坐标系**：

- **Face Gaussian** 的旋转矩阵 $R_f^i = [\mathbf{t}_1^i, \mathbf{t}_2^i, \mathbf{n}_f^i]$，其中 $\mathbf{n}_f^i$ 为三角面法线，$\mathbf{t}_1^i$ 对齐于三角形的最长边方向（Eq.6-7）。这确保了高斯的长轴方向与三角面的主要延展方向一致。
- **Vertex Gaussian** 的旋转矩阵 $R_v^j = [\mathbf{t}_1^j, \mathbf{t}_2^j, \mathbf{n}_v^j]$，其中 $\mathbf{n}_v^j$ 为面积加权的邻面法线平均（Eq.9），$\mathbf{t}_1^j$ 选择与 $\mathbf{n}_v^j$ 最垂直的参考轴（Eq.10）。这种设计使顶点高斯在曲面接缝处能够平滑过渡。

这一 changed slot 的关键在于：旋转矩阵不再是优化的产物，而是网格局部微分几何的直接反映。当网格变形时，法线和切线方向自动更新，高斯朝向始终与表面保持几何一致，避免了 OOD 姿势下因旋转不匹配导致的渲染伪影。

### 从隐式光滑到显式正则化：网格质量的主动保障

解析映射的稳定性高度依赖网格质量——如果三角形退化（如过于狭长或角度极端），基于内切圆半径和边长的尺度计算将失去数值意义。现有方法如 **GoMAvatar**（Wen et al., CVPR 2024）仅依赖隐式的表面光滑约束，缺乏对三角形形状的直接控制。

Tavatar 引入**显式等边正则化项** $\mathcal{L}_{\mathrm{tri}}$（Eq.15），同时惩罚边长方差和角度偏离 $60^\circ$ 的程度：

$$\mathcal{L}_{\mathrm{tri}} = \sum_{f \in \mathbf{F}_s} \left[ \mathrm{Var}(\{\|\mathbf{e}_1\|, \|\mathbf{e}_2\|, \|\mathbf{e}_3\|\}) + \sum_{\phi \in \Theta_f} (1 - \cos \phi)^2 \right]$$

这一 changed slot 的因果作用在消融实验中得到直接验证：移除等边正则化后，法线精度从 1.772 恶化至 1.834（Table 4, X-Avatar 00019），证实了网格质量对解析映射稳定性的关键支撑作用。权重 $\lambda_t = 0.01$ 的设置使得正则化既能防止退化，又不至于过度约束网格的表达能力。

### 三类创新的协同机制

上述三个 changed slots 并非孤立设计，而是构成了一个**因果闭环**：等边正则化保证网格质量 → 高质量网格支撑解析尺度/旋转的数值稳定性 → 解析属性确保高斯分布与网格形变的严格一致 → 一致的高斯分布降低对优化自由度的依赖。这一闭环使得 Tavatar 仅需优化颜色系数（球谐函数），而所有几何属性均由网格拓扑确定性推导，从根本上消除了 OOD 姿势下的高斯漂移问题。

定量证据表明，这一范式转换带来的几何一致性提升远超现有方法：在 X-Avatar 上法线误差降低 13.8%，PeopleSnapshot 上降低 17.9%（Table 3）。消融实验进一步揭示了两类高斯设计的互补必要性——移除 Face Gaussian 导致 PSNR 下降 1.35 dB，移除 Vertex Gaussian 导致 PSNR 下降 2.57 dB（Table 4），证实了面覆盖与顶点细节的双重拓扑绑定缺一不可。

## 整体框架

Tavatar 提出了一种**几何驱动**的可动画人类化身重建范式，其核心思路是将高斯属性的确定方式从传统的优化驱动转向从可变形网格的局部拓扑中解析推导。如图1所示，整个pipeline由三个紧密耦合的模块构成：可变形网格表示、拓扑感知高斯推导和等边正则化，三者协同工作，使高斯分布与网格变形严格一致，从而在分布外（OOD）姿势下仍保持稳健的渲染质量和几何一致性。

### Pipeline 总览

**输入**是多视角视频帧及其对应的SMPL参数（姿态 $\pmb{\theta}$ 和形状 $\beta$）。系统首先从SMPL规范模板出发，通过一个神经形状编码器 $E_s$ 预测逐顶点偏移量 $\Delta \mathbf{v}$，生成个性化的穿衣网格 $\mathbf{V}_s$；随后利用SMPL的线性混合蒙皮（LBS）将该网格驱动到任意目标姿势，得到变形后的网格顶点 $\mathbf{v}^p$。这一可变形网格为后续所有高斯属性提供了稳定的拓扑支架。

**核心模块**是拓扑感知高斯推导。Tavatar 设计了两类互补的高斯原语：**Face Gaussian**（面高斯）绑定于每个三角面的内心，负责大面积表面覆盖；**Vertex Gaussian**（顶点高斯）锚定于网格顶点，用于处理细节区域和面间接缝融合。两类高斯的所有几何属性——位置 $\mu$、旋转矩阵 $\mathbf{R}$、尺度 $\mathbf{S}$——均从网格的局部几何信息（边长、法线、内切圆半径等）中解析计算得出，**无需逐姿势优化**。唯一可学习的参数是用于颜色建模的二阶球谐系数。

**优化目标**由四项损失联合驱动：RGB重建损失（L1 + SSIM）、法线伪监督损失、网格拉普拉斯平滑损失以及等边正则化损失 $\mathcal{L}_{\mathrm{tri}}$。其中等边正则化通过惩罚三角网格的边长方差和内角偏离，防止极端姿势下的三角形退化，从而保证解析映射的数值稳定性。

### 模块间数据流

整个pipeline的数据流可以概括为以下步骤：

1. **规范网格生成**：$E_s(\mathbf{V}_c) \rightarrow \Delta \mathbf{v}$，得到个性化顶点 $\mathbf{v}^s = \mathbf{v}^c + \Delta \mathbf{v}$。
2. **姿势驱动变形**：通过LBS将 $\mathbf{v}^s$ 变换到目标姿势下的 $\mathbf{v}^p$（Eq.1）。
3. **高斯属性解析**：
   - **Face Gaussian**：位置 $\mu_f^i$ 取三角形内心（Eq.5）；旋转矩阵 $\mathbf{R}_f^i$ 由面法线和最对齐参考轴构建的正交坐标系确定（Eq.6-7）；面内尺度与内切圆半径 $r_i$ 成正比（$s_{f,x}^i = s_{f,y}^i = \beta \cdot r_i$，$\beta=0.5$），法向尺度极小（$s_{f,z}^i = \epsilon = 10^{-3}$），形成扁平碟状（Eq.8）。
   - **Vertex Gaussian**：位置 $\mu_v^j$ 直接取顶点坐标 $\mathbf{v}_j^p$；旋转矩阵 $\mathbf{R}_v^j$ 基于面积加权法线 $\mathbf{n}_v^j$ 构建（Eq.9-10）；尺度取决于到一环邻点的最小边长（$s_{v,x}^j = s_{v,y}^j = \gamma \cdot \min\|\mathbf{v}_k^p - \mathbf{v}_j^p\|$，$\gamma=0.5$）（Eq.11）。
4. **渲染与监督**：所有高斯通过3DGS的可微光栅化渲染RGB和法线图，与真实图像计算损失。
5. **网格正则化**：$\mathcal{L}_{\mathrm{tri}}$ 反向传播至形状编码器，约束网格保持等边性（Eq.15）。

### 与基线方法的范式差异

传统方法（如 **GaussianAvatar** (Hu et al., CVPR 2024)、**GART** (Lei et al., CVPR 2024)）将高斯的旋转和尺度均交由自由优化，导致高斯与人体网格的形变分离，在OOD姿势下出现高斯漂浮或表面孔洞。**IHuman** (Paudel et al., ECCV 2024) 仅约束旋转而尺度仍自由，未能根本解决该问题。**GoMAvatar** (Wen et al., CVPR 2024) 虽将高斯绑定到网格表面，但缺乏对网格规则性的显式约束。Tavatar 的关键突破在于将尺度、旋转、位置三者全部从网格拓扑中解析确定，使高斯分布与网格变形形成严格的因果绑定，从根本上消除了优化-形变不一致带来的几何伪影。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Tavatar_Topology_A/figures/001_Figure_1.jpg]]
*Figure 1: Method overview. We propose Tavatar, a geometry-driven paradigm that reconstructs high-quality animatable human avatars by analytically deriving Gaussian attributes from a deformable mesh. Our approach includes: Analytical Gaussian Attribute Derivation: All Gaussian positions, scales, and orientations are computed directly from mesh topology yielding structurally correct Gaussian placement, improved surface coverage, and pose-consistent animation across challenging motions. Equilateral Geometry Regularization: An equilateral constraint enforces stable Gaussian binding on the mesh, preventing degeneration and ensuring robust reconstruction quality, especially under large deformations and in...*

## 核心模块与公式推导

Tavatar 的核心设计理念是将高斯属性的确定方式从**优化驱动**转向**几何驱动**：所有高斯的尺度、旋转和位置均从可变形网格的局部拓扑中解析计算，仅保留颜色系数（二阶球谐函数）作为可学习参数。该方法包含三个关键模块。

### 可变形网格表示

方法以规范姿态（T-pose）的 SMPL 模型为起点，通过一个神经形状编码器预测每个顶点的偏移量，生成个性化的穿衣网格：

$$\mathbf{V}_s = \mathbf{V}_c + E_s(\mathbf{V}_c) = \{\mathbf{v}_i^s = \mathbf{v}_i^c + \Delta \mathbf{v}_i\}_{i=1}^N$$

随后，该个性化网格通过 SMPL 的线性混合蒙皮（LBS）驱动到任意目标姿势：

$$\mathbf{v}_p = \sum_{k=1}^{K} w_k \left( \mathbf{R}_k(\pmb{\theta}) \mathbf{v} + \mathbf{t}_k(\pmb{\theta}) \right)$$

这一设计为后续的高斯绑定提供了稳定的拓扑支架，确保网格在不同姿势下保持一致的三角面结构。

### 拓扑感知高斯推导

Tavatar 设计了两类互补的高斯原语，所有几何属性均从网格拓扑解析推导。

**Face Gaussian（面高斯）** 绑定于每个三角面的内心，其位置按对边边长加权计算：

$$\mu_f^i = \frac{l_1 \mathbf{v}_{i,1}^p + l_2 \mathbf{v}_{i,2}^p + l_3 \mathbf{v}_{i,3}^p}{l_1 + l_2 + l_3}$$

旋转矩阵由面法线 $\mathbf{n}_f^i$ 和对齐的边方向 $\mathbf{t}_1^i$ 构建正交坐标系 $\mathbf{R}_f^i = [\mathbf{t}_1^i, \mathbf{t}_2^i, \mathbf{n}_f^i]$。尺度则基于三角形内切圆半径 $r_i$ 解析确定：

$$s_{f,x}^i = s_{f,y}^i = \beta \cdot r_i, \quad s_{f,z}^i = \epsilon$$

其中 $\beta=0.5$，$\epsilon=10^{-3}$，形成紧贴表面的扁平碟状高斯，不透明度固定为 $\alpha_f^i = 1.0$。

**Vertex Gaussian（顶点高斯）** 直接锚定于网格顶点 $\mu_v^j = \mathbf{v}_j^p$，用于覆盖面高斯之间的接缝区域。其法线通过相邻面的面积加权平均计算：

$$\mathbf{n}_v^j = \frac{\sum_{f \in N(j)} A_f \mathbf{n}_f}{\Vert \sum_{f \in N(j)} A_f \mathbf{n}_f \Vert}$$

旋转矩阵 $\mathbf{R}_v^j = [\mathbf{t}_1^j, \mathbf{t}_2^j, \mathbf{n}_v^j]$ 通过选择最垂直于法线的参考轴构建。尺度取决于顶点到其一环邻域的最小边长，实现局部自适应密度：

$$s_{v,x}^j = s_{v,y}^j = \gamma \cdot \min_{\mathbf{v}_k \in \mathcal{N}_1(j)} \|\mathbf{v}_k^p - \mathbf{v}_j^p\|, \quad s_{v,z}^j = \epsilon$$

其中 $\gamma=0.5$。

**两类高斯的互补性**在消融实验中得到了充分验证：移除 Face Gaussian 后 PSNR 下降 1.35 dB，法线误差上升 0.371；移除 Vertex Gaussian 后 PSNR 下降 2.57 dB，法线误差上升 0.915。前者负责大面积表面覆盖，后者对细节和接缝融合不可或缺。

### 等边正则化

当网格在极端姿势下发生退化（如细长三角面）时，基于拓扑的解析映射会变得数值不稳定。为此，Tavatar 引入显式的等边正则化项：

$$\mathcal{L}_{\mathrm{tri}} = \sum_{f \in \mathbf{F}_s} \left[ \mathrm{Var}(\{\|\mathbf{e}_1\|, \|\mathbf{e}_2\|, \|\mathbf{e}_3\|\}) + \sum_{\phi \in \Theta_f} (1 - \cos \phi)^2 \right]$$

该损失同时惩罚三角面的边长方差和内角偏离 60° 的程度，权重设为 $\lambda_t = 0.01$。消融实验中，移除该正则化后法线精度从 1.772 退化至 1.834，验证了网格质量对解析映射稳定性的关键作用。

### 联合优化框架

完整的优化目标为：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{rgb}} + \lambda_n \mathcal{L}_{\mathrm{normal}} + \lambda_m \mathcal{L}_{\mathrm{mesh}} + \lambda_t \mathcal{L}_{\mathrm{tri}}$$

其中 $\mathcal{L}_{\mathrm{rgb}}$ 为 RGB 的 L1 损失与 SSIM 损失的组合（$\lambda_{\mathrm{SSIM}}=0.2$），$\mathcal{L}_{\mathrm{normal}}$ 为法线伪监督的 L1+SSIM 损失（$\lambda_n=0.05$），$\mathcal{L}_{\mathrm{mesh}}$ 为网格拉普拉斯平滑损失（$\lambda_m=0.01$）。整个框架端到端训练形状编码器和球谐系数，高斯的所有几何属性在每次迭代中从当前网格状态解析重算，无需逐姿势优化。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Tavatar_Topology_A/figures/002_Figure_2.jpg]]
*Figure 2: Gaussian distribution under OOD poses on PeopleSnapshot. Our topology-aware binding maintains structured, mesh-coherent Gaussian layouts across pose variations, while GART and IHuman exhibit floating Gaussians and geometric artifacts, demonstrating the necessity of analytical attribute derivation for robust animation*

## 实验与分析

### 主实验结果

Tavatar 在两个主流可动画人类化身基准上进行了系统评估，与四类代表性基线方法对比：**GaussianAvatar** (Hu et al., CVPR 2024)、**GART** (Lei et al., CVPR 2024)、**IHuman** (Paudel et al., ECCV 2024) 和 **GoMAvatar** (Wen et al., CVPR 2024)。所有方法均基于相同的 SMPL 模型和训练数据分割，评估时使用官方提供的协议和分布外（OOD）姿势子集，确保对比公平。

在渲染质量方面，Tavatar 在 PeopleSnapshot 和 X-Avatar 数据集上均取得最优或次优的 PSNR/SSIM/LPIPS 指标。具体而言，在 PeopleSnapshot 的 male-3-casual 序列上，Tavatar 达到 PSNR 28.93，略优于最佳基线 GoMAvatar 的 28.76（+0.17 dB）；在 X-Avatar 的 subject 00016 上，PSNR 达到 29.03，较最佳基线 GaussianAvatar 的 28.86 提升 0.17 dB。需要指出的是，渲染质量的提升幅度相对有限，这与 Tavatar 将高斯几何属性完全解析化、仅优化颜色系数的设计一致——其核心优势在于几何一致性而非像素级重建精度的极限提升。

几何精度是 Tavatar 的显著优势所在。在法线误差指标上，Tavatar 在 X-Avatar 上达到 1.772，较最佳基线降低 13.8%；在 PeopleSnapshot 上达到 1.687，降低 17.9%。这一大幅领先验证了解析绑定机制的核心假设：通过从网格拓扑直接推导高斯属性，可以从根本上消除优化驱动方法中高斯与网格形变分离导致的几何伪影。

### 消融实验

消融实验在 X-Avatar subject 00019 上进行，系统验证了三个关键设计的作用。

**Face Gaussian 的贡献。** 移除 Face Gaussian（仅保留 Vertex Gaussian）后，PSNR 从 28.24 降至 26.89（-1.35 dB），法线误差从 1.772 升至 2.143（+0.371）。这一退化表明，仅靠顶点高斯无法有效覆盖大面积平坦区域（如躯干、大腿），Face Gaussian 通过内切圆半径解析确定的扁平碟状尺度对表面覆盖至关重要。

**Vertex Gaussian 的贡献。** 移除 Vertex Gaussian（仅保留 Face Gaussian）导致更严重的退化：PSNR 降至 25.67（-2.57 dB），法线误差升至 2.687（+0.915）。这验证了顶点高斯在缝合相邻三角面、处理曲率变化区域（如关节、面部细节）中的不可替代性。两类高斯形成互补：Face Gaussian 提供大面积覆盖，Vertex Gaussian 融合接缝并增强局部细节。

**等边正则化的贡献。** 移除等边正则化项后，法线误差从 1.772 升至 1.834，PSNR 从 28.24 降至 27.83。这一结果表明，网格质量直接影响解析映射的数值稳定性——退化三角形（如细长三角面）会导致内切圆半径和顶点法线计算失准，进而破坏高斯分布的几何一致性。等边正则化通过惩罚边长方差和角度偏离 60°，在极端姿势下维持网格质量，是解析绑定范式的关键保障。

### 分布外姿势下的高斯分布可视化

定性可视化揭示了不同方法在 OOD 姿势下高斯分布的结构差异。Tavatar 的拓扑感知绑定使高斯始终紧密贴合网格表面，保持结构化布局；而 GART 和 IHuman 等优化驱动方法出现明显的高斯漂浮和表面孔洞现象。这一对比直观展示了从“优化驱动”转向“几何驱动”的范式优势：解析推导的高斯属性与网格变形严格一致，无需逐姿势优化即可实现稳健泛化。

### 局限性

尽管 Tavatar 在几何一致性上取得显著突破，其性能仍受两个因素制约。首先，方法性能与底层 SMPL 模型的拟合精度强相关——如果初始模型拟合不准确（例如对极端体型或复杂服装），会限制最终化身质量。其次，当前方法假设服装与身体保持静态拓扑关系，无法处理宽松或动态服装（如裙子飘动），这限制了其在开放场景服装建模中的适用性。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Tavatar_Topology_A/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison on X-Avatar dataset. Our method achieves superior RGB rendering and accurate normal maps across challenging OOD poses. Topology-aware Gaussian binding preserves high-fidelity surface details with anatomically plausible deformations, while baselines exhibit geometric artifacts and surface inconsistencies, validating the effectiveness of our method*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Tavatar_Topology_A/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison on X-Avatar. The best scores are bold, and the second best scores of ours are underlined*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Tavatar_Topology_A/figures/006_Table_3.jpg]]
*Table 3: Geometric accuracy comparison on PeopleSnapshot and X-Avatar datasets. Our method significantly outperforms existing approaches in geometry quality. The best scores are bold*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Tavatar_Topology_A/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative ablation result on X-Avatar subject 00019*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Tavatar_Topology_A/figures/008_Table_4.jpg]]
*Table 4: Quantitative ablation result on X-Avatar subject 00019*

## 方法谱系与知识库定位

### 核心范式转换：从优化驱动到几何驱动

Tavatar 的根本创新在于对高斯属性确定方式的范式转换。现有方法将高斯的几何属性（位置、旋转、尺度）作为可优化参数，仅通过渲染损失间接约束其与人体网格的关系。这种“优化驱动”范式在分布内姿势下尚可工作，但在分布外（OOD）姿势下暴露出结构性缺陷：高斯与网格形变分离，导致漂浮高斯或表面孔洞（见 Figure 2）。

Tavatar 将这一范式转换为“几何驱动”：所有高斯的几何属性直接从可变形网格的局部拓扑解析计算，仅保留颜色系数（球谐函数）作为可学习参数。这一转换的核心因果杠杆在于：**高斯的空间分布不再依赖优化器的隐式发现，而是与网格变形保持严格一致的确定性映射**。

### 与现有方法的差异分析

#### 非约束优化方法

**GaussianAvatar** (Hu et al., CVPR 2024) 和 **GART** (Lei et al., CVPR 2024) 代表了最宽松的优化策略：高斯的旋转和尺度均为自由参数，仅通过渲染损失间接约束。这类方法在训练姿势下可通过过参数化补偿形变不一致，但在 OOD 姿势下缺乏结构先验，高斯容易脱离网格表面，产生几何伪影。Tavatar 的消融实验间接验证了这一点：当移除解析尺度推导、转而自由优化时，法线误差显著上升。

#### 部分约束方法

**IHuman** (Paudel et al., ECCV 2024) 迈出了约束的第一步：将高斯旋转与网格法线对齐，但尺度仍交由自由优化。这种“半约束”策略缓解了旋转方向的自由度爆炸，但未解决尺度与网格形变的耦合问题——当网格在大变形下拉长或压缩时，自由优化的尺度无法自适应调整，导致覆盖不足或过度重叠。

**GoMAvatar** (Wen et al., CVPR 2024) 将高斯绑定到网格表面，增强了位置一致性，但缺乏对网格质量的显式控制。当底层网格在极端姿势下出现退化三角形（如过于细长）时，绑定在退化面上的高斯也会产生畸变。Tavatar 的等边正则化正是针对这一被忽视的脆弱环节。

#### Tavatar 的差异化定位

Tavatar 的独特之处在于**完备的解析推导链**：

| 高斯属性 | 非约束方法 | 部分约束方法 | Tavatar |
|---------|-----------|-------------|---------|
| 位置 | 自由优化 | 网格绑定 | 内心/顶点解析定位 |
| 旋转 | 自由优化 | 法线对齐 | 正交坐标系解析构建 |
| 尺度 | 自由优化 | 自由优化 | 内切圆半径/最小边长解析推导 |
| 网格质量 | 无控制 | 无显式控制 | 等边正则化显式约束 |

这种完备性意味着：一旦网格确定，所有高斯的空间配置即唯一确定，无需任何逐姿势优化。这从根本上消除了 OOD 姿势下的形变不一致问题。

### 适用边界与局限

#### 对底层参数化模型的依赖

Tavatar 的性能与 SMPL 模型的拟合精度强相关。SMPL 提供了规范拓扑和蒙皮权重，这是解析推导的几何基础。如果初始 SMPL 拟合不准确（例如对宽松服装或非标准体型），个性化网格的顶点偏移可能无法完全补偿，导致高斯绑定的几何参考本身存在偏差。这一局限是当前所有基于参数化人体模型的方法共同面临的瓶颈。

#### 拓扑静态假设

当前方法假设服装与身体保持静态拓扑关系——网格的顶点连接关系在变形过程中不变。这意味着 Tavatar 无法处理：
- **宽松服装的动态形变**：如裙子飘动、外套摆动等拓扑外观变化
- **服装与身体的分离**：如背包、手持物品等独立于身体的附件
- **多层服装**：内外层服装的相对运动

这些场景需要动态拓扑或额外的物理仿真层，论文也明确将其列为未来工作方向。

#### 等边正则化的全局性

等边正则化对所有三角形施加统一的边长均匀性和角度一致性约束。在关节等高频变形区域，适度的网格拉伸可能是有益的（允许更稀疏的高斯覆盖大面积区域），而当前的全局权重可能限制了这种自适应性。消融实验显示移除等边正则化后几何精度下降（Normal 从 1.772 升至 1.834），但并未探索区域自适应权重是否能在保持几何精度的同时进一步提升关节区域的渲染质量。

### 开放问题

1. **多对象交互与全身服装**：解析绑定机制能否扩展到包含头发、随身物品、多人物交互等更复杂的场景？这可能需要超越单一 SMPL 拓扑的多网格融合策略。

2. **区域自适应正则化**：等边正则化是否在所有网格区域都最优？针对关节、面部、手部等高频变形区域，是否需要自适应权重或局部正则化策略来平衡几何稳定性与表达灵活性？

3. **跨领域泛化**：该几何驱动范式是否适用于更一般的非人体对象动画控制？例如四足动物、软体机器人等具有不同拓扑和变形模式的对象，需要重新设计高斯类型和解析推导规则。

4. **与物理仿真的融合**：对于宽松服装等动态拓扑场景，能否将解析绑定作为“静态层”，叠加物理仿真驱动的“动态层”高斯，实现更真实的服装动画？

5. **实时性能优化**：虽然解析推导避免了逐姿势优化，但个性化网格的神经形状编码器仍需要前向推理。能否通过预计算或轻量化设计实现移动端实时动画？

## 原文 PDF

![[paperPDFs/CVPR_2026/Tavatar_Topology_Aware_Gaussian_Attribute_Derivation_for_Animatable_Human_Avatars.pdf]]
