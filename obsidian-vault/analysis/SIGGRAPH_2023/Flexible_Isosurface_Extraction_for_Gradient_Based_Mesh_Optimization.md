---
title: "Flexible Isosurface Extraction for Gradient-Based Mesh Optimization"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/Flexible_Isosurface_Extraction_for_Gradient_Based_Mesh_Optimization.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/flexicubes/
aliases:
- FIEGBMO
tags:
- SIGGRAPH_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "在 Dual Marching Cubes 的框架下，为每个网格单元引入三组可优化的局部参数：插值权重 α（8维）和 β（12维）通过凸组合方式控制对偶顶点在单元内的自由定位；四边形分割权重 γ 控制非平面四边形的最优三角化；同时保留底层网格顶点的位移 δ 以进行空间对齐。这些参数通过自动微分与标量场一起优化，使得提取的网格在保持流形和几乎无自交的前提下，..."
primary_logic: "通过将顶点定位、四边形分割和网格变形都参数化为凸组合形式，FlexiCubes 在保证梯度稳定性的同时提供了足够的自由度。具体地，利用对偶顶点保持在网格单元的凸包内，避免了 DC 中 QEF 引起的顶点外爆问题；利用可微分的对角切线连续插值方式选择最优三角剖分；并通过合理的正则化（L_dev, L_sign）抑制自交和接缝，从而在多种下游任务中一致地生成高质量网格。"
claims:
- "在 128³ 分辨率的网格重建中，FlexiCubes 取得最低的 Chamfer Distance（4.31×10⁻⁵）和最大的 Edge F1（0.51），且法线角差>5° 的三角形比例（30.57%）远低于 DMTet（48.86%）和 Marching Cubes（42.56%）。"
- "消融实验显示，在基准 DMC centroid 的基础上，依次添加灵活顶点定位、网格变形和四边形分割权重后，IN>5° 从 53.02% 逐步降至 34.87%，EF1 从 0.19 提升至 0.43，证明每个参数组件的有效性。"
- "在 3D 生成模型 GET3D 中，将 DMTet 替换为 FlexiCubes 后，Motorbike 类的 FID 从 48.90 降至 44.87，Chair 类从 22.41 降至 17.51，Car 类从 10.60 降至 9.55，网格质量显著提升。"
- "在 nvdiffrec 逆向渲染重建中，FlexiCubes 产生的薄片三角形更少（最小角直方图分布更优），且 PSNR 和 Chamfer 距离与 DMTet 相当或更优（例如 Chair 场景 PSNR 31.8 dB 持平，CD 0.45 vs 4.51）。"
---

# Flexible Isosurface Extraction for Gradient-Based Mesh Optimization

> [!tip] 核心洞察
> 通过将顶点定位、四边形分割和网格变形都参数化为凸组合形式，FlexiCubes 在保证梯度稳定性的同时提供了足够的自由度。具体地，利用对偶顶点保持在网格单元的凸包内，避免了 DC 中 QEF 引起的顶点外爆问题；利用可微分的对角切线连续插值方式选择最优三角剖分；并通过合理的正则化（L_dev, L_sign）抑制自交和接缝，从而在多种下游任务中一致地生成高质量网格。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 用于基于梯度网格优化的灵活等值面提取 |
| 英文题名 | Flexible Isosurface Extraction for Gradient-Based Mesh Optimization |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://arxiv.org/abs/2308.05371) · [Project](https://research.nvidia.com/labs/toronto-ai/flexicubes/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FlexiCubes |
| Dataset | Mesh Reconstruction (128³ grid), 3D Generative Modeling (GET3D) on Motorbike |

> [!tip] 效果简介
> - Mesh Reconstruction (128³ grid) 上，Chamfer Distance (10⁻⁵) 为 4.31，对比 4.98 (DMTet)，变化 -0.67。
> - Mesh Reconstruction (128³ grid) 上，IN>5° (%) 为 30.57，对比 48.86 (DMTet)，变化 -18.29。
> - Mesh Reconstruction (128³ grid) 上，Edge F1 为 0.51，对比 0.39 (DMTet)，变化 +0.12。

## 概要

从有符号距离场（SDF）或占用场中提取等值面是三维视觉与图形学的基础操作。当等值面需要作为可微表示参与基于梯度的网格优化时，提取方法必须同时满足两个关键需求：**灵活性**——网格顶点能够局部、独立地调整以对齐几何特征并生成高质量三角形；**梯度有效性**——优化过程数值稳定、收敛良好。现有方法在这两个需求之间存在根本性的张力。

经典的 **Marching Cubes**（Lorensen and Cline, 1987）及其变种将顶点固定在规则网格边上，缺乏灵活性，导致阶梯伪影和大量薄片三角形。**Dual Contouring**（Ju et al., 2002）通过求解二次误差函数（QEF）提供顶点定位自由度，但梯度不稳定，顶点可能外爆出网格单元凸包，容易产生自交和发散。**DMTet**（Shen et al., 2021）等基于变形网格的方法提升了灵活性，但其顶点仍受限于四面体结构，无法独立移动，生成的三角形质量较差。

**FlexiCubes** 的核心洞察是：在 **Dual Marching Cubes**（Nielson, 2004）的框架下，通过引入三组可优化局部参数，在保持梯度稳定性的同时提供足够的自由度。具体而言，FlexiCubes 为每个网格单元引入可学习的插值权重 **α**（8维）和 **β**（12维），通过凸组合方式控制对偶顶点在单元凸包内的自由定位，避免了 DC 中 QEF 引起的顶点外爆问题；引入四边形分割权重 **γ** 控制非平面四边形的最优三角化方向；同时保留底层网格顶点的位移 **δ** 以进行空间对齐。配合合理的正则化项（L_dev 约束接缝、L_sign 抑制虚假几何），FlexiCubes 在保证流形性和几乎无自交的前提下，使提取的网格能够灵活调整形状并成功优化下游目标。

实验验证了 FlexiCubes 的有效性和通用性。在 128³ 分辨率的网格重建中，FlexiCubes 取得了最低的 Chamfer Distance（4.31×10⁻⁵）和最高的 Edge F1（0.51），且法线角差超过 5° 的三角形比例（30.57%）远低于 DMTet（48.86%）和 Marching Cubes（42.56%）。消融实验证实了每个参数组件（灵活顶点定位、网格变形、四边形分割权重）的独立贡献。在 3D 生成模型 GET3D 中，将 DMTet 替换为 FlexiCubes 后，Motorbike 类的 FID 从 48.90 降至 44.87，Chair 类从 22.41 降至 17.51。在 nvdiffrec 逆向渲染重建中，FlexiCubes 产生的薄片三角形更少，PSNR 与 DMTet 持平或更优，Chamfer 距离显著降低（Chair 场景：0.45 vs 4.51）。

FlexiCubes 的主要局限在于：不保证完全无自交（尽管比例极低），缺乏全局连续性因而不适合需要光滑形变路径的应用，额外参数增加了存储和计算开销。未来方向包括将体积渲染与基于网格的表示更紧密地结合、将自适应层级网格提取扩展到生成式建模和实时应用等。

### 等值面提取在梯度优化中的双重困境

三维几何的隐式表示（如符号距离函数 SDF）在深度学习驱动的几何处理任务中占据核心地位。然而，将隐式场转换为显式网格的等值面提取（isosurface extraction）步骤，在基于梯度的优化场景中面临一个根本性的两难困境：**灵活性**与**梯度有效性**难以兼得。

具体而言，理想的等值面提取方法需同时满足两个关键需求：
1. **灵活性**：网格顶点能够局部、独立地调整位置，以对齐尖锐几何特征并生成高质量、均匀的三角剖分；
2. **梯度有效性**：提取过程可微，且优化过程数值稳定、收敛良好，不产生梯度消失或爆炸。

现有的主流方法均未能同时满足这两个条件。

### 现有方法的缺口

**Marching Cubes (MC)**（Lorensen and Cline, 1987）及其变种是应用最广泛的等值面提取方法。其基本操作是在标量场符号变化的网格边上，通过线性插值确定顶点位置：

$$u_e = \frac{x_a \cdot s(x_b) - x_b \cdot s(x_a)}{s(x_b) - s(x_a)}$$

该公式在 $s(x_a) = s(x_b)$ 时存在奇异性，但更关键的问题在于：MC 的顶点被严格固定在规则网格的边上。这种刚性约束导致两个严重后果：一是无法捕捉尖锐特征，产生阶梯状伪影（staircase artifacts）；二是在梯度优化中，顶点只能沿网格边滑动，缺乏独立移动的自由度，生成的三角形质量较差，容易出现薄片三角形（sliver triangles）。

**Dual Contouring (DC)**（Ju et al., 2002）通过在每个包含零交叉的网格单元内求解二次误差函数（QEF）来定位对偶顶点，从而获得了捕捉尖锐特征的能力：

$$v_d = \underset{v_d}{\mathrm{argmin}} \sum_{u_e \in \mathcal{Z}_e} \nabla s(u_e) \cdot (v_d - u_e)$$

然而，QEF 求解存在严重的梯度问题（见 Fig. 2）：求解得到的顶点不保证位于网格单元的凸包内，导致几何与拓扑情形之间的不一致；当法向量共面时 QEF 存在奇异性；更致命的是，在梯度优化中，顶点可能“爆出”单元边界，引发自交和发散。此外，DC 在某些配置下会产生非流形顶点（见 Fig. 3）。

**Dual Marching Cubes (DMC)**（Nielson, 2004）通过使用重心位置（centroid）作为对偶顶点，避免了 DC 的非流形问题，但其顶点自由度远小于 DC，表达尖锐特征的能力受限。

**DMTet**（Shen et al., 2021）等基于变形网格的方法通过允许底层网格顶点移动来提升灵活性，在生成式建模和逆向渲染中取得了显著进展。但其顶点仍受限于四面体网格的整体变形约束，无法独立移动，导致生成的三角形质量较差——在 128³ 分辨率下，法线角差大于 5° 的三角形比例高达 48.86%（见 Table 2）。

### 核心洞察与动机

上述分析揭示了一个清晰的因果链条：**顶点定位的自由度与梯度稳定性之间存在根本性的张力**。MC 系列因顶点固定在规则网格边上而梯度稳定但缺乏灵活性；DC 系列通过 QEF 提供了灵活性但牺牲了梯度稳定性；DMTet 等变形方法在两者之间取得了折中，但仍未从根本上解决顶点独立移动的问题。

FlexiCubes 的核心洞察是：在 Dual Marching Cubes 的框架下，将对偶顶点的定位、四边形分割和网格变形都参数化为**凸组合（convex combination）**形式。这一设计的关键在于——对偶顶点始终保持在网格单元的凸包内（见 Fig. 6 的绿色区域），从根本上避免了 DC 中 QEF 引起的顶点外爆问题，同时通过可学习参数（α、β、γ、δ）提供了足够的自由度来灵活调整网格几何和连接关系。这种“在安全区域内提供最大自由度”的设计哲学，使得 FlexiCubes 能够在保持梯度稳定性的同时，一致地生成高质量网格。

## 核心方法与创新机理

### 问题诊断：现有等值面方法的“灵活性-梯度有效性”悖论

基于梯度的网格优化要求等值面表示同时满足两个关键条件：**灵活性**（顶点可局部独立调整以对齐几何特征）和**梯度有效性**（优化过程数值稳定、收敛良好）。现有方法难以兼得：

- **Marching Cubes (MC)** 及其变种将顶点固定在规则网格边上，缺乏灵活性，导致阶梯伪影和大量薄片三角形。
- **Dual Contouring (DC)** 通过 QEF 求解提供特征保留能力，但 QEF 解可能落在单元凸包之外，造成几何-拓扑不一致和梯度不稳定，容易产生自交和发散。
- **DMTet** 通过变形四面体网格提升了灵活性，但顶点仍无法独立移动，三角形质量较差。

FlexiCubes 的核心洞察是：在 **Dual Marching Cubes (DMC)** 的流形保证框架下，通过引入精心设计的可学习参数，将顶点定位、四边形剖分和网格变形全部参数化为**凸组合形式**，从而在保证梯度稳定性的同时提供足够的自由度。

### Changed Slots：三个关键参数化创新

FlexiCubes 相对于 DMC centroid 基线，引入了三组可优化的局部参数，构成其核心创新：

#### Slot 1：对偶顶点定位 — 从固定重心到可学习凸组合

- **基线值**：DMC centroid 使用面心（等权平均）作为对偶顶点；DC 使用 QEF 最小解。
- **FlexiCubes 方案**：引入两类可学习权重：
  - **顶点权重 α**（每立方体角 8 维）：调整边交叉点的位置，公式为 $u_e = \frac{s(x_i) \alpha_i x_j - s(x_j) \alpha_j x_i}{s(x_i) \alpha_i - s(x_j) \alpha_j}$。
  - **边权重 β**（每立方体边 12 维）：将对偶顶点定义为相关边交叉点的凸组合 $v_d = \frac{1}{\sum_{u_e \in V_E} \beta_e} \sum_{u_e \in V_E} \beta_e u_e$。
- **关键机制**：凸组合保证对偶顶点始终位于网格单元的凸包内（Fig. 6 绿色区域），彻底避免了 DC 中 QEF 导致的顶点外爆问题，同时提供了灵活的局部调整能力。

#### Slot 2：四边形三角化策略 — 从固定对角线到可微分割

- **基线值**：固定对角线划分非平面四边形。
- **FlexiCubes 方案**：引入可学习的分割权重 γ，通过插值两种对角线划分的中点来平滑控制三角化方向：
  $$\overline{v_d} = \frac{\gamma_{c_1}\gamma_{c_3}(v_d^{c_1}+v_d^{c_3})/2 + \gamma_{c_2}\gamma_{c_4}(v_d^{c_2}+v_d^{c_4})/2}{\gamma_{c_1}\gamma_{c_3}+\gamma_{c_2}\gamma_{c_4}}$$
- **关键机制**：优化时通过插值中点生成四个三角形，推理时沿主对角线切分，使四边形剖分能够适应局部几何特征，避免固定剖分导致的不理想几何。

#### Slot 3：网格变形能力 — 从固定均匀网格到局部对齐

- **基线值**：MC 系列使用固定均匀网格；DC 系列无独立变形能力。
- **FlexiCubes 方案**：允许底层网格顶点移动，位移 δ 限制在半网格间距内。
- **关键机制**：使网格能够局部对齐薄特征和尖锐边缘，进一步增加自由度，同时通过约束范围保持拓扑稳定性。

### 配套正则化：保障优化质量

上述参数化创新需要合理的正则化来抑制退化：

- **L_dev（顶点偏离正则）**：$\mathcal{L}_{\mathrm{dev}} := \sum_{v \in V} \mathrm{MAD}\big[ \{ |v - u_e|_2 : u_e \in N_v \} \big]$，约束对偶顶点与邻接边交叉点之间距离的 MAD，减少接缝（Fig. 26）。
- **L_sign（符号一致性正则）**：$\mathcal{L}_{\mathrm{sign}} := \sum_{(s_a, s_b) \in \vec{\mathcal{E}}_g} H\big( \sigma(s_a), \mathrm{sign}(s_b) ) \big)$，鼓励网格边上标量场的符号与真值一致，抑制虚假几何碎片。

### 消融验证：每个 Slot 的独立贡献

消融实验（Table 3; Fig. 9）证实了各组件的独立有效性：在基准 DMC centroid 上依次添加灵活顶点定位、网格变形和四边形分割权重后，IN>5° 从 53.02% 逐步降至 34.87%，EF1 从 0.19 提升至 0.43。每个参数组件均带来可测量的网格质量增益。

### 扩展能力

FlexiCubes 的核心参数化框架还支持两个重要扩展：
- **四面体网格提取**（Section 4.5）：从表面网格生成内部一致的可微四面体网格，用于物理仿真。
- **自适应网格分辨率**（Section 4.6）：基于八叉树的层级细化，通过约束细层级顶点的 SDF 保持拓扑一致，实现局部高分辨率网格。

FlexiCubes 构建于 Dual Marching Cubes（DMC）框架之上，其核心设计思路是：在保持 DMC 固有流形性保证的前提下，向等值面提取过程中注入额外的可优化自由度，使提取出的网格既能灵活对齐几何特征，又能在梯度优化中保持数值稳定。

### 输入与输出

**输入**：一个定义在规则网格（或八叉树层级网格）上的标量场 $s(x)$，通常由神经网络隐式表示。网格分辨率为 $N^3$，每个网格单元携带 8 个角点的标量值及符号信息。

**输出**：一个由三角形面片组成的二维流形表面网格，以及可选的内部四面体网格。输出网格的顶点数量、拓扑连接关系由标量场的符号配置决定，但顶点的精确空间位置和四边形三角化方式由 FlexiCubes 引入的可学习参数控制。

### Pipeline 模块

FlexiCubes 的提取流程由以下核心模块串联而成，每个模块在 DMC 基线之上引入了一组可微分的自由度：

1. **边交叉点计算（α 参数）**：对于每条存在符号翻转的网格边，标准 MC 通过线性插值确定零点位置。FlexiCubes 引入每个网格角点的可学习权重 $\alpha_i \in \mathbb{R}_{>0}$（每单元 8 维），将边交叉点公式推广为加权形式：
   $$u_e = \frac{s(x_i) \alpha_i x_j - s(x_j) \alpha_j x_i}{s(x_i) \alpha_i - s(x_j) \alpha_j}$$
   该参数化允许交叉点在边上偏移，为后续对偶顶点定位提供更多自由度。

2. **对偶顶点定位（β 参数）**：在 DMC 中，每个“主面”（primal face）对应一个对偶顶点，传统做法是取相关边交叉点的重心。FlexiCubes 引入每条网格边的可学习权重 $\beta_e \in \mathbb{R}_{>0}$（每单元 12 维），将对偶顶点定义为边交叉点的凸组合：
   $$v_d = \frac{1}{\sum_{u_e \in V_E} \beta_e} \sum_{u_e \in V_E} \beta_e u_e$$
   凸组合的构造确保 $v_d$ 始终位于网格单元的凸包内（Fig. 6 中的绿色区域），从根本上避免了 Dual Contouring 中 QEF 求解导致的顶点外爆和梯度奇异问题。

3. **四边形自适应分割（γ 参数）**：DMC 将四个相邻对偶顶点连接为四边形面片，传统做法沿固定对角线将其切分为两个三角形。FlexiCubes 引入每个网格单元的可学习分割权重 $\gamma$，通过插值两种可能对角线的中点来生成平滑过渡的三角剖分：
   $$\overline{v}_d = \frac{\gamma_{c_1}\gamma_{c_3}(v_d^{c_1}+v_d^{c_3})/2 + \gamma_{c_2}\gamma_{c_4}(v_d^{c_2}+v_d^{c_4})/2}{\gamma_{c_1}\gamma_{c_3}+\gamma_{c_2}\gamma_{c_4}}$$
   优化时，四边形被分割为四个三角形（以 $\overline{v}_d$ 为中心点），推理时则沿优化收敛后的主对角线切分。这使得网格三角化能自适应地匹配底层几何的局部曲率。

4. **网格变形（δ 参数）**：为进一步增加自由度，FlexiCubes 允许底层网格顶点在局部移动，位移 $\delta$ 被限制在半网格间距内。这使网格能局部拉伸以对齐薄片特征，同时避免大范围变形导致的网格退化。

5. **正则化约束**：两个关键正则器保障优化稳定性：
   - **$\mathcal{L}_{\mathrm{dev}}$**：约束每个对偶顶点与其邻接边交叉点之间距离的中位绝对偏差（MAD），鼓励顶点保持理想的对偶关系，减少网格接缝。
   - **$\mathcal{L}_{\mathrm{sign}}$**：鼓励网格边上标量场的符号与真值一致，抑制虚假几何碎片的产生，提高拓扑稳定性。

### 可选扩展

- **四面体网格提取**：在表面网格的基础上，通过对内部体积进行空间划分，FlexiCubes 可生成内部一致的四面体网格（Fig. 10），用于物理仿真等需要体积离散化的应用。
- **自适应网格分辨率**：基于八叉树的层级细化策略，允许在几何复杂区域使用高分辨率网格，同时约束细层级顶点的 SDF 以保持拓扑一致性，实现局部高精度提取（Fig. 14）。

### 优化流程

整个 pipeline 通过自动微分进行端到端优化。在每次迭代中，标量场 $s(x)$ 和所有可学习参数（$\alpha, \beta, \gamma, \delta$）联合接收来自下游目标函数（如 Chamfer 距离、渲染损失、物理仿真损失等）的梯度信号。网格拓扑由标量场符号配置决定，而几何形状由参数连续调节，二者解耦使得拓扑变化和几何细化可以协同进行。

### 性能特征

在 $128^3$ 网格分辨率下，FlexiCubes 的每次迭代时间（315 ms）与 DMTet（307 ms）相当，显存占用因存储额外的每单元参数而略高（15.3 GiB vs 13.1 GiB）。但在生成式建模等应用中，由于 FlexiCubes 生成的三角形数量更少，整体显存反而更低（11.1 GiB vs 11.6 GiB）。提取的网格自交比例极低（$128^3$ 下仅 0.017%），远优于 Dual Contouring（1.28%），保证了梯度优化的可靠性。

FlexiCubes 的核心设计围绕一个关键洞察展开：在 Dual Marching Cubes (DMC) 的框架内，通过引入三组可优化的局部参数，使等值面提取在保持流形性和梯度稳定性的同时，获得足够的自由度来对齐几何特征。以下逐一解析各模块的数学构造与功能。

### 对偶顶点灵活定位 (α, β 参数)

传统 Marching Cubes 沿网格边线性插值确定顶点位置，公式为：

$$u_e = \frac{x_a \cdot s(x_b) - x_b \cdot s(x_a)}{s(x_b) - s(x_a)}$$

该公式在 $s(x_a) = s(x_b)$ 时存在奇异性，且顶点被严格锁定在网格边上，无法局部调整。Dual Contouring (DC) 通过求解二次误差函数 (QEF) 来定位对偶顶点：

$$v_d = \underset{v_d}{\mathrm{argmin}} \sum_{u_e \in \mathcal{Z}_e} \nabla s(u_e) \cdot (v_d - u_e)$$

但 QEF 解不保证顶点位于单元凸包内，导致梯度不稳定和自交问题（见 Fig. 2）。普通 DMC 则简单取面心作为对偶顶点：

$$v_d = \frac{1}{|V_E|} \sum_{u_e \in V_E} u_e$$

这保证了凸包约束，但牺牲了灵活性。

FlexiCubes 将顶点定位参数化为凸组合形式。首先，引入每个网格单元角点的可学习权重 $\alpha_i \in \mathbb{R}_{>0}^8$，调整边交叉点位置：

$$u_e = \frac{s(x_i) \alpha_i x_j - s(x_j) \alpha_j x_i}{s(x_i) \alpha_i - s(x_j) \alpha_j}$$

然后，引入每条边的可学习权重 $\beta_e \in \mathbb{R}_{>0}^{12}$，将对偶顶点定义为相关边交叉点的凸组合：

$$v_d = \frac{1}{\sum_{u_e \in V_E} \beta_e} \sum_{u_e \in V_E} \beta_e u_e$$

由于 $\alpha$ 和 $\beta$ 均为正值，$v_d$ 必然位于网格单元的凸包内（Fig. 6 中绿色区域），从而在根本上避免了 DC 中 QEF 导致的顶点外爆问题，同时赋予每个对偶顶点在单元内自由移动的能力。

### 四边形自适应分割 (γ 参数)

DMC 提取的网格由四边形面片构成，需要三角化才能用于渲染和下游任务。固定对角线划分可能导致不理想的几何形态。FlexiCubes 在每个网格单元引入可学习的分割权重 $\gamma$，通过插值两种可能对角线划分的中点来平滑控制三角化方向：

$$\overline{v_d} = \frac{\gamma_{c_1}\gamma_{c_3}(v_d^{c_1}+v_d^{c_3})/2 + \gamma_{c_2}\gamma_{c_4}(v_d^{c_2}+v_d^{c_4})/2}{\gamma_{c_1}\gamma_{c_3}+\gamma_{c_2}\gamma_{c_4}}$$

其中 $v_d^{c_1}, v_d^{c_2}, v_d^{c_3}, v_d^{c_4}$ 是构成四边形的四个对偶顶点。优化过程中，通过该中点 $\overline{v_d}$ 生成四个三角形；推理时则沿主导对角线切分。这一可微操作使网格能自适应选择最优三角剖分，避免固定分割造成的几何失真（消融实验证实该模块独立贡献显著，见 Table 3 与 Fig. 9）。

### 网格变形 (δ 参数)

为进一步增加自由度，FlexiCubes 允许底层网格顶点在有限范围内移动，位移 $\delta$ 被限制在半网格间距内。这使得网格能局部拉伸以对齐薄特征，同时不破坏 DMC 的拓扑结构。与 DMTet 等变形网格方法不同，FlexiCubes 的顶点可以独立于网格边移动，从而在尖锐特征处生成更高质量的三角形。

### 正则化约束

两个关键正则器保障优化稳定性：

- **顶点偏离正则** $L_{\mathrm{dev}}$：惩罚每个对偶顶点与其邻接边交叉点之间距离的中位数绝对偏差 (MAD)，鼓励理想的对偶关系，减少接缝：

$$\mathcal{L}_{\mathrm{dev}} := \sum_{v \in V} \mathrm{MAD}\big[ \{ |v - u_e|_2 : u_e \in N_v \} \big]$$

- **符号一致性正则** $L_{\mathrm{sign}}$：鼓励网格边上标量场的符号与真值一致，抑制虚假几何碎片的产生：

$$\mathcal{L}_{\mathrm{sign}} := \sum_{(s_a, s_b) \in \vec{\mathcal{E}}_g} H\big( \sigma(s_a), \mathrm{sign}(s_b) \big)$$

其中 $H$ 为交叉熵损失。这两个正则器使 FlexiCubes 在添加等边三角形正则化时仅轻微牺牲几何精度，而 MC 和 DMTet 的精度则显著下降（Table 4），验证了参数化设计带来的鲁棒性。

### 扩展模块

- **四面体网格提取**：FlexiCubes 可选的扩展通过分割内部体积生成一致的可微四面体网格，用于物理仿真等应用（Section 4.5, Fig. 10）。
- **自适应网格分辨率**：基于八叉树的层级细化，通过约束细层级顶点的 SDF 保持拓扑一致，实现局部高分辨率网格（Section 4.6, Fig. 12, Fig. 14）。

## 实验与关键发现

### 核心性能瓶颈与实验设计逻辑

FlexiCubes 的实验设计围绕一个核心命题展开：**能否在保持梯度优化稳定性的前提下，赋予等值面提取足够的局部灵活性，以生成更高质量的网格？** 为此，作者设计了三个层次的实验验证：1）网格重建任务检验几何精度与网格质量；2）消融实验分离各参数组件的独立贡献；3）下游应用（逆向渲染、3D 生成、物理仿真）验证方法的泛化能力。所有实验均以 **DMTet**（Shen et al., 2021）作为主要竞争基线，同时纳入 **Marching Cubes (MC)** 系列和 **Dual Contouring (DC)** 系列作为参考。

实验的公平性保障措施包括：所有方法使用相同的标量场分辨率（DMTet 使用匹配三角面数的稍高分辨率以公平对比）、统一的数据预处理（中心归一化），并报告了计算开销对比（Table 7, Table 8）以消除效率优势的质疑。

### 主要实验结果

#### 网格重建：几何精度与网格质量的双重优势

在 128³ 分辨率的网格重建任务中（Table 2），FlexiCubes 在多项指标上一致优于 DMTet：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2308_05371/figures/013_Table_2.jpg]]
*Table 2: antitative results on Mesh Reconstruction. We report the following metrics: { 1 } ${ \mathsf { N } }$ { > } $5 ^ { \circ }$ { : } normal angle difference > 5◦, CD: Chamfer Distance, F1: F1 score, ECD: Edge Chamfer Distance, EF1: Edge F1 Score. #V: number of vertices, #F: number of faces

| 指标 | FlexiCubes | DMTet | 提升幅度 |
|------|-----------|-------|---------|
| Chamfer Distance (×10⁻⁵) | **4.31** | 4.98 | -13.5% |
| Edge F1 | **0.51** | 0.39 | +30.8% |
| IN>5° (%) | **30.57** | 48.86 | -37.4% |

**关键解读**：IN>5°（法线角差超过 5° 的三角形比例）的大幅降低表明 FlexiCubes 生成的网格表面更加光滑，这与 DMTet 因顶点无法独立移动而导致的“阶梯伪影”形成鲜明对比。Edge F1 的提升则直接验证了灵活顶点定位对尖锐几何特征的对齐能力——DMTet 的变形网格虽然整体可调，但顶点受限于四面体结构，无法精确贴合特征边。

在网格内在质量方面（Fig. 15），FlexiCubes 的最小角分布明显优于 DMTet，薄片三角形（sliver triangles）比例显著减少。这一优势在逆向渲染任务中得到了进一步验证（Fig. 18）：FlexiCubes 生成的 Chair 场景网格最小角直方图更集中于健康角度区间，而 DMTet 产生了大量接近 0° 的退化三角形。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2308_05371/figures/020_Figure_18.jpg]]
*Figure 18: Visualization of nvdiffrec reconstructions for two scenes in the NeRF synthetic dataset. We compare DMTet and FlexiCubes for the topology extraction step. We note fewer sliver triangles for FlexiCubes. We illustate this by including min angle histogram for nvdiffrec reconstructions for all eight scenes in the NeRF synthetic dataset. Fewer triangles with small angles means less sliver triangles for FlexiCubes*

#### 3D 生成模型：FID 指标的显著提升

在 GET3D 生成框架中，将 DMTet 替换为 FlexiCubes 后（Table 6），三个类别的 FID 均获得显著改善：

| 类别 | DMTet FID | FlexiCubes FID | 改善 |
|------|----------|---------------|------|
| Motorbike | 48.90 | **44.87** | -8.2% |
| Chair | 22.41 | **17.51** | -21.9% |
| Car | 10.60 | **9.55** | -9.9% |

**因果机制**：GET3D 使用 MLP 预测每个网格单元的参数（α, β, γ），而非直接存储，因此 FlexiCubes 的额外参数并未增加显存负担——反而因为生成所需三角形数量减少，整体显存从 11.6 GiB 降至 11.1 GiB（Table 8）。这验证了“灵活参数化→更优网格质量→更少三角形→更低资源消耗”的良性循环。

#### 逆向渲染：视觉质量持平，几何质量跃升

在 nvdiffrec 逆向渲染重建中（Table 5），FlexiCubes 与 DMTet 在 PSNR 上基本持平（Chair 场景均为 31.8 dB），但在 Chamfer Distance 上展现出数量级优势：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2308_05371/figures/024_Table_5.jpg]]
*Table 5: View interpolation results (PSNR) for nvdiffrec reconstructions of the NeRF synthetic dataset, using either DMTet or FlexiCubes for the topology step. The image metric scores are arithmetic means over all test images. We also include Chamfer distances (CD) computed on visible triangles (the set of triangles visible in at least one test view) using 2.5 M point. Lower scores indicate be er geometric fidelity*

| 场景 | DMTet CD (×10⁻²) | FlexiCubes CD (×10⁻²) |
|------|-----------------|---------------------|
| Chair | 4.51 | **0.45** |
| Hotdog | 1.14 | **0.17** |
| Lego | 0.75 | **0.41** |

**深层含义**：PSNR 持平说明两种方法在视图合成质量上相当，但 Chamfer Distance 的巨大差距揭示了 DMTet 的一个隐蔽失败模式——它在视觉上“看起来对”但几何上存在系统性偏差，可能产生不可见的内部空洞或表面偏移。FlexiCubes 通过允许顶点在凸包内自由定位，更精确地恢复了真实几何。

### 消融实验：逐层拆解参数贡献

消融实验（Table 3, Fig. 9）以 **DMC centroid**（Nielson, 2004 的 Dual Marching Cubes 面心基线）为起点，逐步叠加 FlexiCubes 的三个核心参数组件：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2308_05371/figures/017_Table_3.jpg]]
*Table 3: antitative results on shape reconstruction ablating different formulations of the dual vertex*

| 配置 | IN>5° (%) | Edge F1 |
|------|----------|---------|
| DMC centroid（基线） | 53.02 | 0.19 |
| + 灵活顶点定位（α, β） | 42.31 | 0.32 |
| + 网格变形（δ） | 37.14 | 0.38 |
| + 四边形分割（γ） | **34.87** | **0.43** |

**逐组件分析**：

1. **灵活顶点定位（α, β）**：贡献最大的单一组件。从 centroid 的固定面心改为凸组合定位后，IN>5° 降低 10.71 个百分点，Edge F1 提升 68%。这直接验证了核心洞察——将顶点从“固定于面心”解放为“凸包内可调”是解决阶梯伪影的关键。

2. **网格变形（δ）**：在顶点已可自由定位的基础上，进一步允许底层网格位移，IN>5° 再降 5.17 个百分点。这表明某些薄特征需要网格本身局部拉伸才能对齐，仅靠顶点在单元内移动不够。

3. **四边形分割（γ）**：IN>5° 再降 2.27 个百分点，Edge F1 提升至 0.43。可微分的对角线选择使得非平面四边形的三角剖分与几何特征对齐，避免了固定对角线导致的“错误折痕”。

**正则化器的独特价值**（Table 4）：当施加等边三角形正则器时，FlexiCubes 的 IN>5° 仅从 30.57% 升至 41.05%（牺牲 10.48 个百分点），而 MC 从 42.56% 升至 50.16%（牺牲 7.60 个百分点但基线更差），DMTet 从 48.86% 飙升至 67.65%（牺牲 18.79 个百分点）。这揭示了 FlexiCubes 的一个深层优势：**灵活性使其在满足正则化约束时仍有足够自由度维持几何精度**，而 DMTet 的变形自由度被正则化严重挤占，导致质量崩溃。

### 失败模式与边界条件

尽管 FlexiCubes 在多数场景中表现优异，实验和分析揭示了几个明确的失败模式：

1. **拓扑跳变问题**：当等值面滑过网格顶点时，网格会发生不连续跳变（原文明确指出“不适合需要光滑形变路径的应用”）。这在动画和变形任务中可能产生视觉伪影，但在静态优化任务中影响有限。

2. **自交的残余风险**：虽然自交比例极低（128³ 下为 0.017%，远低于 DC 的 1.28%），但严格约束以避免所有自交会“导致表达能力和优化易度下降”。这是一种有意的设计取舍——用极低概率的自交换取更高的灵活性和优化稳定性。

3. **内存开销的上下文依赖性**：在直接存储每个网格单元参数的场景（如 nvdiffrecmc）中，FlexiCubes 的显存占用（15.3 GiB）高于 DMTet（13.1 GiB），主要因为每个立方体需要存储 20 个额外标量参数（α: 8 维, β: 12 维, γ: 1 维）。但在使用 MLP 预测参数的场景（如 GET3D）中，这一开销消失。

4. **自适应网格的四面体填充缺陷**：在八叉树扩展中，特定拓扑配置（Case C18）下内部体积可能无法完全被四面体填充，这对物理仿真应用构成潜在限制。

### 性能基准：开销与收益的权衡

Table 7 和 Table 8 提供了完整的性能画像。FlexiCubes 的等值面提取操作本身比 DMTet 慢约 3 倍（前向+反向），但在完整应用管道中，这一开销被下游任务的计算主导地位稀释——nvdiffrecmc 中每次迭代时间仅从 307 ms 增至 315 ms（+2.6%）。在 GET3D 中，FlexiCubes 甚至因三角形数量减少而整体更快。

**关键结论**：FlexiCubes 的计算开销是“固定成本”而非“比例成本”——它不随下游任务复杂度增长而放大，因此在实际应用中几乎可以忽略。

### 补充图表


![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2308_05371/figures/002_Table_1.jpg]]
*Table 1: Taxonomy of isosurfacing methods. Grad means gradient-based based optimization is effective in practice, and Uniform means the resulting tessellations are generally uniform without sliver triangles*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2308_05371/figures/016_Table_4.jpg]]
*Table 4: antitative results on mesh reconstruction with equilateral triangle regularizer. Adding regularizer for DMTet and MC significantly impacts geometric metrics (IN>5◦(%), CD), while FlexiCubes only sacrifices a bit*

## 定位与知识库关联

### 1. 问题定位：可微等值面提取的两难困境

在基于梯度的网格优化中，可微等值面提取方法长期面临一对核心矛盾：**灵活性与梯度有效性难以兼得**。具体而言：

- **灵活性**要求网格顶点能够局部、独立地调整位置，以对齐尖锐几何特征并生成高质量三角形；
- **梯度有效性**要求优化过程数值稳定、收敛良好，避免因参数化不当导致的梯度消失或发散。

现有方法在这两个维度上呈现明显的权衡取舍（Table 1）：

| 方法 | 灵活性 | 梯度优化 | 均匀性 | 无自交 | 2-流形 |
|------|--------|----------|--------|--------|--------|
| **Marching Cubes** (Lorensen & Cline, 1987) | ✗ | ✓ | ✓ | ✓ | ✓ |
| **Dual Contouring** (Ju et al., 2002) | ✓ | ✗ | ✗ | ✗ | ✗ |
| **DMTet** (Shen et al., 2021) | 部分 | ✓ | ✗ | ✓ | ✓ |
| **NDC** (Chen et al., 2022b) | ✓ | 部分 | ✗ | ✗ | ✗ |
| **FlexiCubes** (本文) | ✓ | ✓ | ✓ | 近似✓ | ✓ |

**Marching Cubes (MC)** 及其变种（如 MC_SDF）将顶点固定在规则网格边上，通过线性插值确定零交叉位置。这种刚性约束导致两个问题：一是无法捕捉尖锐特征，产生阶梯伪影；二是生成的三角形中薄片三角形比例高。从梯度优化角度看，MC 的顶点位置完全由标量场值决定，缺乏独立调整的自由度。

**Dual Contouring (DC)** 通过在每个网格单元内求解二次误差函数（QEF）来定位对偶顶点，理论上提供了更大的灵活性。然而，QEF 求解存在两个致命缺陷：一是顶点可能落在单元凸包之外（Fig. 2），导致几何与拓扑配置不一致；二是当法向量共线时 QEF 出现奇异性，梯度不稳定，优化中容易产生自交和发散。**Neural Dual Contouring (NDC)** 尝试用神经网络替代 QEF 求解，但未能根本解决梯度稳定性问题。

**DMTet** 将网格变形引入可微提取流程，通过优化底层四面体网格的顶点位移来对齐几何。这在一定程度上提升了灵活性，但其顶点仍受四面体拓扑约束，无法独立移动，生成的三角形质量较差——在 128³ 分辨率重建中，法线角差 >5° 的三角形比例高达 48.86%。

### 2. FlexiCubes 的方法学突破

FlexiCubes 的核心洞察在于：**在 Dual Marching Cubes (DMC) 的框架下，通过引入凸组合形式的可学习参数，可以在保证梯度稳定性的同时获得足够的自由度**。具体而言，FlexiCubes 在三个关键环节进行了参数化改造：

**（1）对偶顶点定位（α, β 参数）**

传统 DMC 使用面心（centroid）作为对偶顶点，位置固定。FlexiCubes 引入两组可学习权重：
- **顶点权重 α ∈ ℝ⁸₊**：调整每条网格边上的零交叉位置，使边交叉点 $u_e$ 可沿边移动；
- **边权重 β ∈ ℝ¹²₊**：将对偶顶点 $v_d$ 定义为相关边交叉点的凸组合。

由于 α 和 β 均约束为正，$v_d$ 始终位于网格单元的凸包内（Fig. 6），从根本上避免了 DC 中 QEF 导致的顶点外爆问题。这种凸组合参数化天然保证了梯度稳定性——顶点位置随参数平滑变化，不会出现跳变或奇异性。

**（2）四边形自适应分割（γ 参数）**

DMC 生成的网格面为四边形，需要三角化。固定对角线划分可能导致不理想的几何。FlexiCubes 引入分割权重 γ，通过插值两种对角线划分的中点来生成四个三角形，优化时平滑过渡，推理时沿主对角线切分。这使得网格连接性可以适应局部几何特征。

**（3）网格变形（δ 参数）**

在灵活顶点定位的基础上，FlexiCubes 进一步允许底层网格顶点移动，位移 δ 限制在半网格间距内。这使网格能够局部对齐薄特征，同时保持拓扑稳定性。

**消融实验（Table 3; Fig. 9）** 验证了各组件的独立贡献：在基准 DMC centroid 上依次添加灵活顶点定位、网格变形和四边形分割权重后，IN>5° 从 53.02% 逐步降至 34.87%，EF1 从 0.19 提升至 0.43。

### 3. 与关键基线的方法论对比

**vs. DMTet (Shen et al., 2021)**

DMTet 是梯度网格优化中最广泛使用的等值面提取方法。两者的核心差异在于：
- DMTet 的顶点自由度来自四面体网格变形，顶点移动受四面体拓扑约束，无法独立调整；
- FlexiCubes 的顶点自由度来自凸组合参数化，每个对偶顶点可在其单元凸包内独立定位。

这导致 FlexiCubes 在网格质量上显著优于 DMTet：在 128³ 重建中，FlexiCubes 的 IN>5° 为 30.57%（DMTet 为 48.86%），Chamfer Distance 为 4.31×10⁻⁵（DMTet 为 4.98×10⁻⁵）。在 nvdiffrec 逆向渲染中，FlexiCubes 产生的薄片三角形更少，Chair 场景的 Chamfer Distance 从 4.51×10⁻² 降至 0.45×10⁻²。

**vs. Dual Contouring (Ju et al., 2002)**

DC 通过 QEF 求解提供顶点灵活性，但梯度不稳定。FlexiCubes 用凸组合替代 QEF 求解，在保持灵活性的同时消除了奇异性。在 128³ 下，FlexiCubes 的自交比例仅为 0.017%，远低于 DC 的 1.28%。

**vs. Marching Cubes 系列**

MC 系列（包括 MC_SDF）顶点固定于网格边，缺乏灵活性。FlexiCubes 继承了 DMC 的流形性保证，同时通过 α、β、γ 参数获得了 MC 所不具备的顶点自由度。

### 4. 适用边界与局限性

**适用场景：**
- 基于梯度的网格重建与优化（几何目标、视觉目标、物理目标）
- 3D 生成模型中的网格提取（如 GET3D 替换 DMTet）
- 逆向渲染与摄影测量（如 nvdiffrec）
- 需要高质量三角形网格的下游应用

**关键局限：**

1. **不完全保证无自交**：虽然自交比例极低（0.017%），但在极端参数配置下仍可能出现少量自交三角形。严格的全局无自交约束会显著降低表达能力和优化易度。

2. **缺乏全局连续性**：当等值面滑过网格顶点时，网格拓扑会发生不连续跳变。这使得 FlexiCubes 不适合需要光滑形变路径的应用，如连续动画中的网格演化。

3. **额外参数开销**：每个网格单元引入 20 个额外标量参数（α: 8, β: 12, γ: 1），在直接存储每个单元参数的场景中（如 nvdiffrecmc），显存占用从 DMTet 的 13.1 GiB 增至 15.3 GiB。但在生成式应用中（如 GET3D），因生成所需三角形数量减少，总体显存反而降低（11.1 GiB vs 11.6 GiB）。

4. **自适应网格化的拓扑限制**：基于八叉树的层级细化扩展在特定拓扑配置（如 Case C18）中，内部体积可能无法完全被四面体填充。

5. **正则化依赖**：为抑制自交和接缝，FlexiCubes 依赖 L_dev 和 L_sign 正则器。正则权重的选择需要在几何精度和网格质量之间权衡——添加等边三角形正则器后，IN>5° 从 30.57% 升至 41.05%，但相比 MC（42.56%→50.16%）和 DMTet（48.86%→67.65%），精度损失最小（Table 4）。

### 5. 开放问题与后续方向

1. **体积渲染与网格表示的融合**：如何将体积渲染的梯度信号更有效地传递到基于网格的表示中，减少对密集采样点的依赖，是视觉任务中的关键挑战。

2. **自适应层级网格的生成式扩展**：当前八叉树扩展主要用于重建任务，如何将其引入生成式建模和实时应用仍需探索。

3. **拓扑变化下的蒙皮权重优化**：在动画和蒙皮任务中，当网格拓扑发生变化时，如何一致地优化蒙皮权重是一个未解决的问题。

4. **四面体网格的裂隙修复**：FlexiCubes 的四面体扩展在过滤操作后可能引入微小裂隙，需要设计新的正则化项来进一步提高物理仿真的稳定性。

5. **连续形变路径的支持**：当前方法的拓扑跳变特性限制了其在需要光滑形变的应用中的使用，如何设计连续可微的拓扑变换机制是一个开放方向。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/Flexible_Isosurface_Extraction_for_Gradient_Based_Mesh_Optimization.pdf]]
