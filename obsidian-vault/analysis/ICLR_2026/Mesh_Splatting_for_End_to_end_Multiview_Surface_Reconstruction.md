---
title: Mesh Splatting for End-to-end Multiview Surface Reconstruction
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Mesh_Splatting_for_End_to_end_Multiview_Surface_Reconstruction_023e28fff1e0.pdf
project_link: "https://www.blender.org/"
code_link: null
aliases:
- MS
- MSEEMSR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将基网格软化为多个可微分的半透明层（soft mesh），各层的透明度由到基网格的有符号距离计算，并保持对基网格顶点的可导通道，从而使体积渲染损失可以直接反向传播以更新基网格几何。
primary_logic: 通过将表面网格转化为伪体积表示（多层半透明网格），该方法保留了网格的可控拓扑特性（可通过重新网格化调整），同时获得体积渲染带来的丰富3D感受野和稳定梯度，从而在端到端优化中同时实现高精度和高质量的表面重建。
claims:
- 半透明层围绕基网格随机采样，显著扩大了用于学习复杂细节的3D感受野。
- 本方法可将表面表示可微地转化为体积表示，使体积渲染能够直接驱动基网格更新，避免网格提取带来的误差。
- DTU 上 Chamfer Distance (cm), Mean = 0.62
- BlendedMVS 上 Chamfer Distance (cm), Mean = 1.64
---

# Mesh Splatting for End-to-end Multiview Surface Reconstruction

> [!tip] 核心洞察
> 通过将表面网格转化为伪体积表示（多层半透明网格），该方法保留了网格的可控拓扑特性（可通过重新网格化调整），同时获得体积渲染带来的丰富3D感受野和稳定梯度，从而在端到端优化中同时实现高精度和高质量的表面重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | 用于端到端多视角表面重建的网格溅射 |
| 英文题名 | Mesh Splatting for End-to-end Multiview Surface Reconstruction |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=PSgps4JXTb) · [Project](https://www.blender.org/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Mesh Splatting |
| Dataset | DTU, BlendedMVS, DTU / NeRF Synthetic |

> [!tip] 效果简介
> - DTU 上，Chamfer Distance (cm), Mean 0.62 vs 0.57 (IMLS-Splatting) (+0.05 (略高于当前最佳))。
> - BlendedMVS 上，Chamfer Distance (cm), Mean 1.64 vs 1.69 (GaussianSurfel) (-0.05 (本方法最佳))。
> - DTU (scan122, 1/4 scale) 上，GPU 内存 (GB) 2 vs 8 (Iterative Mesh Rasterization) (减少75%内存)。

## 概要

多视角表面重建的核心瓶颈在于表示范式的两难：体积方法（如 NeRF、3D Gaussian Splatting）虽能通过体积渲染获得丰富的 3D 感受野，但必须依赖后置网格提取步骤（Marching Cubes、Poisson Reconstruction），这一过程会积累误差并往往生成过于稠密的网格；纯表面方法直接优化网格，却只有单层感受野，难以捕捉复杂几何细节，过度依赖法线、深度或着色等先验信息。**Mesh Splatting** 通过将基网格软化为多个可微分的半透明层（soft mesh），将表面表示转化为伪体积表示，从而在保留网格可控拓扑特性的同时，获得体积渲染带来的稳定梯度与广阔感受野，实现端到端的高精度表面重建。

本方法的核心机制可概括为三个因果组件：**① 网格软化**——沿基网格顶点法线方向随机偏移生成多层半透明表面，各层透明度由到基网格的有符号距离可微计算，显著扩大 3D 感受野；**② 可微网格溅射**——基于瓦片光栅化投影三角面片，经深度排序后通过体积渲染合成像素颜色，使图像损失可直接反向传播更新基网格几何；**③ 混合拓扑控制**——早期采用 DMTet 维持拓扑稳定，后期冻结网格并启用连续重新网格化以优化面片质量。

实验表明，Mesh Splatting 在 DTU 数据集上取得与当前最佳方法相当的精度（Chamfer Distance 0.62 cm），在 BlendedMVS 上以 1.64 cm 达到最优，同时顶点数仅为体积方法的约 15%，训练时间约 20 分钟/场景，比 Neuralangelo 快 30 倍以上。消融实验证实，多层软化带来的体积监督和混合拓扑控制策略对最终精度均至关重要。

### 表面重建的两难困境

多视角表面重建旨在从一组标定图像中恢复场景的三维几何。当前主流方法可归为两类范式，二者在精度与效率之间长期处于“鱼与熊掌”的取舍之中。

**体积方法**（如 NeRF 及其变体）将场景建模为连续的密度场或符号距离场（SDF），通过体积渲染进行端到端优化。这类方法拥有广阔的 3D 感受野，能稳定捕捉复杂几何结构。然而，它们并不直接输出表面网格，必须依赖后置网格提取步骤——如 Marching Cubes 或 Poisson Reconstruction——才能获得可用的多边形表面。这一提取过程会积累误差，且往往生成顶点数过于稠密的网格（如 **GaussianSurfel** (Dai et al., 2024) 在 DTU 上产生约 200 万顶点，而本文方法仅需约 30 万顶点即可达到相当或更优精度）。更根本的是，即使输入完美的点云，Poisson 重建本身仍可能引入误差（如遗漏点），这构成了体积流水线实际精度的上限瓶颈。

**表面方法**直接优化网格或点云，天然保持表面表示的结构特性，且可输出顶点数可控的轻量网格。但其致命弱点是**单层感受野**：传统可微光栅化仅能感知恰好落在表面上的点，缺乏对表面邻域的感知能力，导致梯度稀疏、优化困难。因此，这类方法（如 **IMLS-Splatting** (Yang et al., TOG 2025)、**SuGaR** (Guedon & Lepetit, 2023)）严重依赖法线、深度或着色等先验信息作为辅助监督，在缺乏这些信号或几何细节复杂时精度受限。

### 核心瓶颈：表示与渲染的错配

上述困境的根源在于**表面表示与体积渲染之间的不可通约性**。体积渲染能提供丰富的 3D 梯度信号，但要求输入为体积表示；表面网格便于控制拓扑与面片质量，却天然适配可微光栅化而非体积渲染。现有工作要么停留在体积范式内（需后置网格提取），要么停留在表面范式内（受限于单层感受野），缺乏一种将二者优势融合的桥梁机制。

### 本文动机：将表面转化为伪体积

本文的核心动机是**打破这一壁垒**：能否在保留表面网格作为最终输出的前提下，使其获得体积渲染的梯度信号？换言之，能否将表面表示可微地转化为体积表示，从而让体积渲染损失直接驱动基网格的顶点更新？

这一思路的关键在于**软化网格（mesh softening）**：沿基网格顶点法线方向偏移生成多个半透明层，各层的透明度由该点到基网格的有符号距离可微计算。如此，原本不透明的单层表面被扩展为一个可控带宽的伪体积表示——它既保留了基网格的拓扑结构（可通过重新网格化调整面片质量），又获得了体积渲染带来的多层感受野，使梯度可以从偏离表面的区域反向传播以修正几何。

## 核心方法与创新机理

**Mesh Splatting** 的核心创新在于弥合了“体积重建精度高但需后置网格提取”与“表面重建可直接优化网格但感受野受限”之间的鸿沟。其关键洞察是：**将表面网格转化为伪体积表示，使体积渲染的丰富梯度能直接驱动基网格的端到端优化**，从而同时获得高精度几何与高质量可控拓扑。

这一创新通过三个紧密耦合的 **changed slots** 实现：

### 1. 表示类型：从单层不透明表面到可微多层半透明软网格

传统表面方法（如 **SuGaR** (Guedon & Lepetit, 2023)）仅优化单层不透明网格，其3D感受野局限于表面本身，难以捕捉复杂几何细节。体积方法（如 **Neuralangelo** (Li et al., CVPR 2023)、**GaussianSurfel** (Dai et al., 2024)）虽拥有丰富的体积感受野，但最终仍需通过 Marching Cubes 或 Poisson 重建提取网格，这一步骤会积累误差并往往生成过于稠密的网格（见 Figure 1 中红色圆圈所示的网格与点云错位）。

本方法提出 **软网格（soft mesh）**：沿基网格顶点法线方向偏移生成多层半透明表面，每层的透明度由该层到基网格的有符号距离可微计算：

$$
\mathbf{v}_{j}^{i} = \mathbf{v}_{j}^{0} + d_{j}^{i} \cdot \mathbf{n}_{j}
$$

$$
s_{j}^{i} = \mathrm{sign}(d_{j}^{i}) \| \mathrm{stop}(\mathbf{v}_{j}^{i}) - \mathbf{v}_{j}^{0} \|_{2}
$$

透明度通过类 VolSDF 的映射函数将符号距离转为 alpha 值（Equation 3），参数 $\beta$ 控制密度集中程度。这一设计使表面表示获得了**可控的3D感受野**——半透明层围绕基网格随机采样，显著扩大了用于学习复杂细节的梯度覆盖范围。同时，表面始终由基网格定义，保留了网格的结构化特性和拓扑可控性。

### 2. 渲染方式：从可微光栅化到基于瓦片的可微网格溅射

传统表面方法使用可微光栅化渲染单层网格，仅能利用着色或轮廓监督，几何信号薄弱。本方法提出 **可微网格溅射（Differentiable Mesh Splatting）**：将多层软网格的所有三角面片通过瓦片光栅化投影到图像平面，按深度排序后通过体积渲染合成像素颜色：

$$
\mathbf{C}_{p} = \sum_{i \in \mathcal{N}} \mathbf{c}_{i} \ \alpha_{i} \prod_{k=1}^{i-1} (1 - \alpha_{k})
$$

其中交点颜色由 MLP 根据插值后的顶点特征、法线、视线方向及哈希位置编码预测（Equation 5），重心坐标经过透视投影下的深度校正（Equation 4）。这一渲染方式使**体积渲染损失可以直接反向传播以更新基网格顶点**，避免了网格提取步骤带来的误差积累，同时保留了网格溅射的内存效率——在 DTU scan122 上仅需 2 GB 显存，而迭代式网格光栅化需 8 GB（Table 3）。

### 3. 拓扑控制：从固定拓扑到混合拓扑策略

纯表面方法通常在整个优化过程中保持固定拓扑，或仅在完成后重新网格化，无法在训练中动态调整面片分布。本方法提出 **混合拓扑控制策略**：

- **早期阶段**：使用 DMTet（Marching Tetrahedra）从四面体网格提取基网格并优化顶点符号距离值，确保全局拓扑的稳定收敛。消融实验表明，移除 DMTet 阶段会导致全局拓扑缺失（如出现破洞），Chamfer 距离从 1.57 升至 3.79（Table 4, Figure 7）。
- **后期阶段**：当 DMTet 阶段收敛后，冻结网格拓扑，切换至 **连续重新网格化（Continuous Remeshing）**，通过各向同性重新网格化优化面片质量，使顶点分布更加均匀合理。仅用 DMTet（分辨率128）得到的网格过于稀疏（CD 达 6.94），仅用连续重新网格化则无法稳定拓扑，混合策略取得最佳精度。

这一设计使方法既能捕获正确的全局拓扑结构，又能在细节区域获得高质量的面片分布，最终在 DTU 上以约 300k 顶点（比 GaussianSurfel 少 85%）达到 0.62 cm 的 Chamfer 距离，逼近当前最佳水平。

Mesh Splatting 的端到端多视角表面重建流水线由四个核心模块串联构成，形成“体积初始化 → 表面软化 → 可微溅射渲染 → 拓扑控制”的闭环优化路径，如 **Figure 3** 所示。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_PSgps4JXTb/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed method. An initial tetrahedral grid stores signed-distance values at its vertices, and a base mesh is extracted using Marching Tetrahedra. The base mesh is then softened into multiple layers by offsetting vertices along their normals, transforming it from a surface into a pseudo-volumetric representation. The multi-layer mesh is rendered via the proposed Differentiable Mesh Splatting based on tile-based rasterization, and supervised by the input images through a rendering loss*

### 流水线总览

1. **四面体网格初始化 (Tetrahedral Grid Initialization)**  
   在目标场景的包围盒内构建一个四面体网格，每个顶点存储一个可学习的符号距离值。通过 Marching Tetrahedra 从该网格中提取零水平集，得到初始基网格。这一步为后续优化提供了显式的三角面片拓扑结构。

2. **网格软化 (Mesh Softening)**  
   将基网格沿顶点法线方向偏移，生成多个半透明层，将单层表面表示转化为伪体积表示。每层的透明度由该层顶点到基网格的有符号距离通过类 VolSDF 的 alpha 映射函数计算，并保持对基网格顶点的可导性。这一软化操作是关键瓶颈突破点：它使原本只有单层感受野的表面表示获得了可控的 3D 感受野，从而能够通过体积渲染损失直接驱动基网格几何更新。

3. **可微网格溅射 (Differentiable Mesh Splatting)**  
   多层软化网格通过基于瓦片光栅化（tile-based rasterization）的溅射渲染器投影到图像平面。对于每个像素，所有覆盖该像素的三角面片按深度排序后，利用前向后 alpha 混合（体积合成）计算最终颜色。该渲染器在透视投影下使用深度校正的重心坐标进行属性插值，并通过 MLP 结合哈希位置编码预测每个交点的颜色。

4. **混合拓扑控制 (Hybrid Topology Control)**  
   训练早期采用 DMTet 阶段维持全局拓扑稳定，避免出现破洞等拓扑缺失问题；当 DMTet 阶段收敛后，冻结网格并切换至连续重新网格化（Continuous Remeshing），以优化面片质量并调整局部拓扑。这种混合策略兼顾了拓扑的全局完整性与局部细节的表达能力。

### 损失监督与输入输出

- **输入**：多视角图像及对应的相机位姿。
- **监督信号**：主要采用体积渲染损失（渲染图像与输入图像之间的光度误差），同时可辅以着色监督（shading supervision），后者通过栅格化基网格并计算漫反射加镜面色调分量来提供额外的几何约束。
- **输出**：经过端到端优化的高质量三角网格，具有可控的顶点数量和良好的拓扑结构。

### 关键设计动机

该流水线的核心洞察在于：通过将表面网格转化为伪体积表示，既保留了网格的可控拓扑特性（可通过重新网格化调整），又获得了体积渲染带来的丰富 3D 感受野和稳定梯度。这与纯体积方法（需后置网格提取步骤）和纯表面方法（仅单层感受野）形成根本区别——体积方法在 Marching Cubes 或 Poisson 重建阶段积累误差并常生成过于稠密的网格，而纯表面方法过度依赖法线、深度或着色等先验信息，难以捕捉复杂几何细节。

Mesh Splatting 将表面网格转化为可微伪体积表示，使体积渲染损失能够直接驱动基网格顶点更新。其核心由四个模块串联构成。

### 1. 四面体网格初始化

首先构建一个四面体网格，每个顶点存储一个可学习的符号距离值（SDF）。通过 Marching Tetrahedra（DMTet）从该 SDF 场中提取初始基网格。这一阶段为后续优化提供具有合理全局拓扑的初始表面。

### 2. 网格软化

基网格提取后，沿每个顶点法线方向偏移生成多层半透明表面，将单层表面转化为伪体积表示。

**顶点偏移**：对于基网格顶点 $\mathbf{v}_{j}^{0}$ 及其法线 $\mathbf{n}_{j}$，第 $i$ 层的顶点为：

$$\mathbf{v}_{j}^{i} = \mathbf{v}_{j}^{0} + d_{j}^{i} \cdot \mathbf{n}_{j}$$

其中 $d_{j}^{i}$ 是沿法线方向的偏移距离，通常从以基网格为中心的均匀分布中随机采样。

**有符号距离计算**：为保证对基网格的可导性，使用停止梯度操作计算软化顶点到基网格的有符号距离：

$$s_{j}^{i} = \mathrm{sign}(d_{j}^{i}) \, \| \mathrm{stop}(\mathbf{v}_{j}^{i}) - \mathbf{v}_{j}^{0} \|_{2}$$

停止梯度确保梯度仅通过符号和范数中的基网格顶点传播，而非通过偏移后的顶点位置。

**透明度映射**：将符号距离 $s$ 转换为透明度值 $\alpha$，采用类 VolSDF 的映射函数：

$$\alpha = \begin{cases} \frac{1}{\beta} \left(1 - \frac{1}{2} e^{s/\beta}\right), & s < 0, \\ \frac{1}{2\beta} e^{-s/\beta}, & s \ge 0 \end{cases}$$

其中 $\beta$ 控制密度在基网格表面附近的集中程度。当 $s<0$（位于基网格内部）时透明度趋近于 $1/\beta$；当 $s\ge0$（外部）时透明度指数衰减。这一软化机制显著扩大了 3D 感受野，使梯度能够从远离基网格的图像区域反向传播。

### 3. 可微网格溅射

多层软化网格通过基于瓦片光栅化的可微网格溅射进行渲染。

**深度校正的重心坐标**：在透视投影下，光线与三角形交点的重心坐标需根据各顶点深度进行校正：

$$\mathbf{w}_{i} = \operatorname{correct}\left( \mathbf{p}, \{ \mathbf{u}_{1}, \mathbf{u}_{2}, \mathbf{u}_{3} \}, \{ z_{1}, z_{2}, z_{3} \} \right)$$

其中 $\mathbf{p}$ 为像素坐标，$\mathbf{u}_{k}$ 为三角形顶点投影坐标，$z_{k}$ 为对应深度值。该校正确保在透视投影下插值属性的几何正确性。

**颜色预测**：交点颜色由一个小型 MLP 预测，输入包括插值后的顶点特征 $\mathbf{f}_{i}$、法线 $\mathbf{n}_{i}$、视线方向 $\mathbf{r}_{i}$ 以及交点位置的多分辨率哈希编码：

$$\mathbf{c}_{i} = \mathrm{MLP}\big( \mathbf{f}_{i}, \mathbf{n}_{i}, \mathbf{r}_{i}, \mathrm{Hash}(\mathbf{x}_{i}) \big)$$

**体积合成**：将瓦片内所有三角形按深度从近到远排序后，通过前向后 alpha 混合得到像素最终颜色：

$$\mathbf{C}_{p} = \sum_{i \in \mathcal{N}} \mathbf{c}_{i} \, \alpha_{i} \prod_{k=1}^{i-1} (1 - \alpha_{k})$$

其中 $\mathcal{N}$ 为像素 $p$ 处所有重叠三角形的集合。该体积合成公式使渲染损失能够通过多层半透明表面直接反向传播至基网格顶点。

**着色监督辅助**：除体积渲染外，可额外对基网格进行可微光栅化着色，提供辅助监督信号。栅格化像素颜色由漫反射分量与镜面色调分量组成：

$$\mathbf{c} = \mathbf{c}_{d} + \mathbf{s} \odot \Phi_{s}( \mathbf{f}_{s}, \omega, \omega_{r} )$$

其中 $\mathbf{c}_{d}$ 为漫反射颜色，$\mathbf{s}$ 为镜面色调，$\Phi_{s}$ 为基于特征 $\mathbf{f}_{s}$、光照方向 $\omega$ 和反射方向 $\omega_{r}$ 的镜面反射函数。

### 4. 混合拓扑控制

为在优化过程中同时保证拓扑稳定性和面片质量，采用两阶段混合策略：

- **早期 DMTet 阶段**：优化四面体网格顶点的 SDF 值，通过 Marching Tetrahedra 动态提取网格。该阶段维持全局拓扑的稳定性，防止出现破洞等拓扑缺陷。
- **后期连续重新网格化阶段**：DMTet 收敛后冻结网格拓扑，切换到 Continuous Remeshing 进行各向同性重新网格化，优化面片质量并调整顶点分布以适应几何细节。

消融实验（Table 4, Figure 7）证实：单独使用 DMTet（分辨率 128）得到的网格过于稀疏，Chamfer 距离高达 6.94；单独使用连续重新网格化则无法稳定拓扑；混合策略取得最佳精度。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_PSgps4JXTb/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative ablations. Hybrid topology control (DMTet + Continuous Remeshing) captures global topology and fine details more reliably than using either component alone*

### 补充图表

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_PSgps4JXTb/figures/002_Figure_2.jpg]]
*Figure 2: Comparison between regular meshes and soft mesh*

## 实验与关键发现

### 核心性能对比

Mesh Splatting 在标准对象级多视角表面重建基准上取得具有竞争力的精度，同时显著减少了网格顶点数量和训练时间。表 1 与表 2 分别报告了 DTU 与 BlendedMVS 数据集上的定量结果。

在 DTU 数据集上，本方法平均 Chamfer 距离为 **0.62 cm**，略高于当前最优的 **IMLS-Splatting**（Yang et al., TOG 2025）的 0.57 cm，但本方法生成的网格顶点数仅约 **300k**，远少于 **GaussianSurfel**（Dai et al., 2024）的约 2000k（减少约 85%），且训练时间仅约 **20 分钟/场景**，而 **Neuralangelo**（Li et al., CVPR 2023）需要超过 600 分钟，速度提升超过 30 倍。在 BlendedMVS 数据集上，本方法平均 Chamfer 距离为 **1.64 cm**，优于 GaussianSurfel 的 1.69 cm，取得最佳精度。

这种“精度–效率”双重优势的关键在于：本方法将表面网格软化为伪体积表示，使得体积渲染损失可以直接驱动基网格顶点更新，从而避免了体积流水线中 Marching Cubes 或 Poisson 重建引入的误差累积和过度稠密网格问题（见图 1(c–e)）。同时，混合拓扑控制策略（DMTet + 连续重新网格化）在保持全局拓扑完整性的前提下，允许面片质量持续优化。

### 消融实验

表 4 和图 7 报告了拓扑控制策略的消融结果，揭示了各组件对最终重建质量的影响机制：

- **移除 DMTet 阶段**：直接使用连续重新网格化从初始网格开始优化，导致全局拓扑严重缺失（如出现破洞），Chamfer 距离从完整模型的 1.57 急剧上升至 3.79。这表明 DMTet 阶段提供的初始拓扑结构对后续优化至关重要。
- **仅使用 DMTet**（分辨率 128）：得到的网格过于稀疏，Chamfer 距离高达 6.94，无法捕获精细几何细节。
- **仅使用连续重新网格化**：无法稳定拓扑结构，重建质量同样显著下降。

混合策略（DMTet + 连续重新网格化）取得了最佳精度，其因果机制在于：早期 DMTet 阶段在低分辨率四面体网格上建立可靠的全局拓扑骨架，后期冻结网格后切换至连续重新网格化，在保持拓扑的前提下优化面片形状和分布。

在 BlendedMVS 数据集上，去除多层软化（即仅保留着色监督）导致 Chamfer 距离从 1.64 恶化至 1.94（表 2），证实了体积监督提供的几何信号远强于纯着色监督。这一结果直接验证了核心设计动机：半透明层围绕基网格随机采样，显著扩大了 3D 感受野，使梯度能够从更远的图像区域传播到基网格顶点。

### 渲染效率分析

表 3 对比了 Mesh Splatting（MS）、迭代式网格光栅化（IMR）和高斯溅射（GS）在 DTU scan122 不同图像尺度下的内存占用和训练时间。在 1/4 尺度下，MS 仅需 **2 GB** GPU 内存，而 IMR 需要 8 GB，内存减少 75%。这一效率优势源于基于瓦片的光栅化策略，避免了对每个像素迭代追踪光线–三角形交点的开销。

### 细结构重建能力

图 6 展示了在 NeRF Synthetic 数据集上的定性对比结果。本方法能够准确重建细薄结构（如船桅杆和 ficus 场景中的花瓶），并一致地优于 GaussianSurfel。这表明软网格的多层结构为细薄几何提供了足够的梯度覆盖，而纯表面方法或单层高斯表示在此类区域往往缺乏有效监督信号。

### 失败模式与局限性

尽管 Mesh Splatting 在多数场景下表现优异，实验揭示了以下边界条件：

1. **极细线缆结构**：各向同性的连续重新网格化对线缆、头发等狭长结构不够友好，可能丢失此类特征。这是当前重新网格化策略的固有局限。
2. **初始网格远离真实表面**：当基网格初始位置与目标表面距离超过软化层带宽时，体积梯度无法有效传播，导致优化失败。这限制了方法对初始化的鲁棒性。
3. **大规模场景扩展**：受四面体网格分辨率和 GPU 显存限制，直接扩展到超大规模场景存在瓶颈。

### 待验证的开放性方向

- 自适应重新网格化策略（在平坦区域保持各向同性面片，在线缆状区域生成狭长三角形）是否能解决细结构丢失问题？
- 自适应层带宽或层次化软化是否能支持大规模场景的高效重建？
- 结合更先进的材质/光照模型后，能否进一步减少对显式着色监督的依赖，实现纯图像驱动的端到端优化？

### 补充图表

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_PSgps4JXTb/figures/010_Table_4.jpg]]
*Table 4: Ablation metrics*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_PSgps4JXTb/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of reconstruction paradigms. Yellow points denote ground-truth point clouds. “Verts” and “CD” denote the number of vertices and the Chamfer distance, respectively. (a) Our method optimizes meshes end-to-end and uses remeshing for topology control, achieving accurate surfaces with the fewest vertices. (b) SuGaR Guedon & Lepetit (2023) also optimizes ´ meshes but relies on a single-layer Gaussian-splatting proxy and cannot perform remeshing, which limits accuracy. (c–d) As volumetric methods, GaussianSurfel Dai et al. (2024) and Neuralangelo Li et al. (2023) require a meshing step to extract surfaces, which accumulates errors and often yields unnecessarily dense meshes; note the mi...*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_PSgps4JXTb/figures/011_Figure_9.jpg]]
*Figure 9: Qualitative comparison on Neuralangelo*

## 定位与知识库关联

### 1. 问题瓶颈与范式断裂

多视角表面重建领域长期存在两条技术路线的断裂：

- **体积路线**（NeRF 类、3D Gaussian Splatting 类）：以连续场或显式基元表示场景，依赖体积渲染获得丰富的3D感受野和稳定梯度，但最终必须通过后置网格提取步骤（Marching Cubes、Poisson Reconstruction）才能获得表面网格。这一后处理步骤会积累误差，并往往生成顶点数远超必要的稠密网格。如 **GaussianSurfel** (Dai et al., 2024) 和 **Neuralangelo** (Li et al., CVPR 2023) 均受此制约——即使底层表示质量尚可，提取的网格仍可能与真实点云存在明显错位（见图1红色圆圈标注），且顶点数可达约2000k。

- **表面路线**（可微光栅化类）：直接优化显式网格，避免了网格提取误差，但单层不透明表面只有极薄的感受野，难以捕捉复杂几何细节，过度依赖法线、深度或着色等先验信息。**SuGaR** (Guedon & Lepetit, 2023) 虽通过高斯溅射代理优化网格，但无法进行重新网格化，限制了精度上限；**IMLS-Splatting** (Yang et al., TOG 2025) 作为最近的强基线，同样依赖着色监督。

**Mesh Splatting 的核心突破**在于将这两条路线可微地桥接：将表面网格转化为伪体积表示，使体积渲染损失能直接反向传播以更新基网格几何，从而同时获得体积渲染的丰富感受野和表面路线的可控拓扑特性。

### 2. 关键机制：从表面到体积的可微转化

本方法通过三个紧密耦合的机制实现上述桥接：

**（1）网格软化（Mesh Softening）**：沿基网格顶点法线方向偏移生成多个半透明层，各层的透明度由到基网格的有符号距离计算（见公式 2–3），并保持对基网格顶点的可导通道。这一设计将单层表面的零厚度感受野扩展为可控带宽的3D感受野，使体积梯度能有效传递到基网格。

**（2）可微网格溅射（Differentiable Mesh Splatting）**：基于瓦片光栅化投影三角面片，通过深度校正的重心坐标（公式 4）计算交点属性，经 MLP+哈希编码预测颜色（公式 5），最终按深度排序进行体积合成（公式 6）。该渲染器在保持可微性的同时，比迭代式网格光栅化效率高得多——相同精度下内存占用仅 1/4（2 GB vs 8 GB，Table 3）。

**（3）混合拓扑控制（Hybrid Topology Control）**：早期采用 DMTet 维持全局拓扑稳定（避免破洞），后期冻结网格并启用连续重新网格化（Continuous Remeshing）优化面片质量。消融实验（Table 4, Figure 7）表明，单独使用 DMTet 导致网格过于稀疏（CD=6.94），单独使用连续重新网格化则无法稳定拓扑（CD=3.79），而混合策略取得最优精度。

### 3. 与基线方法的谱系定位

| 方法 | 表示类型 | 渲染方式 | 拓扑控制 | 关键局限 |
|------|----------|----------|----------|----------|
| **NeuS** (Wang et al., NeurIPS 2021) | 隐式 SDF | 体积渲染 | 无（需 MC 提取） | 网格提取误差，训练慢 |
| **Neuralangelo** (Li et al., CVPR 2023) | 混合体积（哈希编码） | 体积渲染 | 无（需 MC 提取） | 网格稠密，训练 >600 min |
| **GaussianSurfel** (Dai et al., 2024) | 显式高斯基元 | 体积渲染 | 无（需 Poisson 重建） | 网格稠密（~2000k verts） |
| **SuGaR** (Guedon & Lepetit, 2023) | 单层高斯代理+网格 | 高斯溅射 | 固定（无重新网格化） | 精度受限 |
| **IMLS-Splatting** (Yang et al., TOG 2025) | 点云+网格 | 着色监督 | 有 | 仅着色监督，感受野有限 |
| **Mesh Splatting (本方法)** | 多层半透明软网格 | 体积合成网格溅射 | 混合（DMTet+CR） | 各向同性 CR 对细结构不友好 |

本方法在 DTU 上以约 300k 顶点达到 CD=0.62（仅次于 IMLS-Splatting 的 0.57，但顶点数远少于 GaussianSurfel 的约 2000k），在 BlendedMVS 上以 CD=1.64 取得最佳。训练时间约 20 分钟/场景（Neuralangelo 的 1/30）。

### 4. 适用边界与局限

**（1）细结构退化风险**：连续重新网格化采用各向同性策略，对线缆、头发等极细结构不友好，可能丢失此类特征。这是当前方法的明确局限，而非推测。

**（2）初始位置敏感性**：当基网格初始位置离真实表面很远时，软化层的带宽可能无法覆盖目标区域，导致体积梯度失效。这限制了方法在缺乏粗略初始化的场景中的直接适用性。

**（3）规模扩展瓶颈**：受四面体网格分辨率和 GPU 显存限制，方法难以直接扩展到超大规模场景。需要进一步改进，如自适应带宽或分层软化策略。

**（4）着色监督的依赖**：虽然体积监督提供了更强的几何信号（消融实验证实去除多层软化后 CD 从 1.64 升至 1.94），但方法仍部分依赖着色监督作为辅助。在纹理稀疏或光照复杂的场景中，这一依赖可能构成瓶颈。

### 5. 开放问题与后续方向

**（1）自适应重新网格化**：能否探索在平坦区域保持各向同性面片的同时，为细长结构（如线缆）生成狭长三角形？这将直接缓解当前各向同性 CR 的局限。

**（2）层次化软化与大规模场景**：采用自适应层带宽或层次化软化（hierarchical softening）有望突破当前规模瓶颈，使方法适用于城市场景或完整建筑重建。

**（3）纯图像驱动的端到端优化**：本方法能否与更先进的材质/光照模型（如基于物理的渲染）结合，进一步减少对显式着色监督的依赖？这将使方法更接近“从图像直接到表面”的理想范式。

**（4）动态场景与时序一致性**：当前方法针对静态场景设计。将软网格溅射扩展到动态场景，并保持时序上的拓扑一致性，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/Mesh_Splatting_for_End_to_end_Multiview_Surface_Reconstruction_023e28fff1e0.pdf]]
