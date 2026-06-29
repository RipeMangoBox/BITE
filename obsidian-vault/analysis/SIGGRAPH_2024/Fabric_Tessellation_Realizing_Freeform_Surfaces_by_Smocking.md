---
title: "Fabric Tessellation: Realizing Freeform Surfaces by Smocking"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Fabric_Tessellation_Realizing_Freeform_Surfaces_by_Smocking.pdf
project_link: null
code_link: null
aliases:
- TBSID
- FTRFSBS
tags:
- SIGGRAPH_2024
- topic/graphics_geometry_processing
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入Tangram图作为中间表示，显式连接开/闭状态下的2D图案几何与3D形状，从而将逆设计问题转化为对Tangram开形态的能量优化（形状、褶皱、接缝）。
primary_logic: 将抽褶图案分解为衬层面（underlay faces）和褶皱面（pleat faces），通过Tangram闭态逼近目标曲面、开态兼顾褶皱规律，并利用无缝参数化引入必要奇点，实现自由曲面的织物镶嵌。
claims:
- "提出的Tangram优化可将边缘再现误差降至10^{-4}以下，表明2D图案能够精确恢复目标几何的度量。"
- 物理制造实例（如扭曲甜甜圈、云朵、心形）与数字预览高度一致，验证了逆设计方法的可行性。
- 添加褶皱能量项后，抽褶花纹扭曲明显减少，证明了显式褶皱控制对视觉效果的关键作用。
- Diverse 3D shapes (Cloud, Heart, Sphere, Bunny, Torus, etc.) 上 Tangram edge reproduction error = < 1e-4
---

# Fabric Tessellation: Realizing Freeform Surfaces by Smocking

> [!tip] 核心洞察
> 将抽褶图案分解为衬层面（underlay faces）和褶皱面（pleat faces），通过Tangram闭态逼近目标曲面、开态兼顾褶皱规律，并利用无缝参数化引入必要奇点，实现自由曲面的织物镶嵌。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过抽褶实现自由曲面的织物镶嵌 |
| 英文题名 | Fabric Tessellation: Realizing Freeform Surfaces by Smocking |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://igl.ethz.ch/projects/3dsmocking/) |
| Topic | #topic/graphics_geometry_processing #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Tangram-based Smocking Inverse Design |
| Dataset | Diverse 3D shapes, Optimization runtime, Preview generation, Visual quality on hyperbolic surface |

> [!tip] 效果简介
> - Diverse 3D shapes (Cloud, Heart, Sphere, Bunny, Torus, etc.) 上，Tangram edge reproduction error < 1e-4 vs N/A (N/A)。
> - Optimization runtime (MacBook M1 Max) 上，optimization time 5 ~ 17 seconds vs N/A (N/A)。
> - Preview generation (MacBook M1 Max) 上，preview time 5 ~ 16 seconds vs N/A (N/A)。

## 概要

本文提出一种通过抽褶（smocking）将平面织物转化为自由曲面3D形状的逆向设计方法。核心挑战在于2D缝合线布局与目标3D形状之间缺乏直接映射，且常规抽褶无法处理曲率奇点。作者引入**Tangram图**作为中间表示——它将抽褶图案分解为衬层面（underlay faces）与褶皱面（pleat faces），显式连接图案的开态2D几何与闭态3D形状。在此基础上，通过优化开态Tangram的形状逼近、褶皱规律性与接缝一致性三项能量，自动求解出可物理制造的2D缝合图案。为支持任意曲面，方法采用无缝N-方向场生成带必要奇点的半规则网格。实验表明，优化后的Tangram边缘再现误差低于10⁻⁴，物理制造实例（扭曲甜甜圈、云朵、心形等）与数字预览高度吻合。该方法在计算制造领域建立了从折纸镶嵌到织物镶嵌的桥梁，适用于建筑表皮、声学设计及可编程拉胀材料等场景。

## 核心方法与创新机理

### 问题本质与核心瓶颈

织物抽褶逆设计的根本困难在于：2D缝合线布局与最终3D形状之间的映射是高度非线性和间接的。当给定一个自由曲面作为目标，直接修改2D图案上的缝合线位置来逼近该曲面，缺乏可计算的梯度路径。更棘手的是，在修改图案以适配目标形状的过程中，抽褶花纹原有的几何规律性极易被破坏——褶皱会变得大小不一、扭曲变形，丧失手工抽褶特有的美学品质。此外，常规抽褶图案基于平面规则镶嵌设计，天然缺乏对曲率集中区域（奇点）的支持，使得处理负高斯曲率曲面时出现图案重叠等结构性问题。

### 核心洞察：Tangram图作为中间表示

本文的核心创新在于引入**Tangram图**（Tangram graph）这一中间表示，将逆设计问题转化为一个可优化的计算流程。Tangram图显式地连接了三个关键状态：

1. **2D抽褶图案**（smocking pattern）：包含缝合线段和面料区域的平面布局。
2. **开态Tangram**（open Tangram）：将2D图案中的衬层面（underlay faces）提取出来，在缝合线未收紧时的平面配置。
3. **闭态Tangram**（closed Tangram）：当所有缝合线长度收缩至零时，衬层面相互靠拢形成的3D三角网格结构，其组合结构与抽褶完成后的衬层面网络等价。

这一表示的核心洞察在于：**抽褶图案被分解为衬层面和褶皱面（pleat faces）两部分**。衬层面是那些边界由“衬层边”（underlay edges）界定、内部不含任何缝合线的区域；褶皱面则是包含缝合线的互补区域。当缝合线收紧时，衬层面被拖拽旋转，迫使褶皱面在2D中收缩、在3D中隆起形成立体褶皱（参见Fig. 6）。因此，闭态Tangram的3D几何完全由衬层面的空间位置决定，而褶皱则自然填充了衬层面之间的空隙。

### Changed Slot 1：从规则网格到无缝等距参数化

**基线方法**（如Scherer 2019）使用规则六边形网格对曲面进行参数化，这种方案不支持奇点，导致在曲率变化剧烈的区域产生严重的面积畸变。当抽褶图案被映射到这样的参数化上时，褶皱大小极不均匀，形状逼近误差显著。

**本文方案**则引入**无缝N-方向场**（seamless N-direction field）计算，生成允许奇点的半规则四边形网格。具体流程为：
- 在输入曲面上计算一个无缝N-方向场，其中N由所选抽褶图案的旋转对称性决定（如Resch-4图案对应N=4）。
- 通过追踪方向场生成四边形网格，奇点自然出现在方向场指数不为零的位置。
- 该网格作为闭态Tangram的组合模板，其面片对应衬层面。

这一改变的关键因果效应是：**等距参数化使得闭态Tangram上每个衬层面的边长尽可能保持均匀**，从而在后续优化中，开态Tangram的边长调整量更小，最终产生的褶皱大小更为一致，形状逼近精度也更高。消融实验（Fig. 30, Appendix C）证实，相比于共形参数化，等距方案能产生更均匀的褶皱并降低形状误差。

### Changed Slot 2：从启发式布局到能量驱动的Tangram优化

**基线方法**依赖手工设计的规则图案或基于刚性变换的局部启发式布局，无法针对任意目标曲面进行系统优化。

**本文方案**将逆设计问题形式化为对**开态Tangram顶点位置Y**的能量最小化问题。核心流程分为三步：

**步骤一：构建闭态Tangram与目标曲面的映射。**
将无缝重网格化后的曲面作为闭态Tangram，记录每条边$e_{ij}$的3D长度作为目标边长。这些目标边长编码了目标曲面的度量信息。

**步骤二：切割与旋转生成初始开态Tangram。**
将闭态Tangram沿特定路径切割，并将每个面片旋转展开到平面，得到开态Tangram的初始布局。切割路径的选择决定了哪些边将成为物理缝合的接缝（seams），这些对应边被记录在集合$C$中。

**步骤三：优化开态Tangram。**
求解以下加权能量最小化问题：

$$\mathbf{Y}^o = \arg\min_{\mathbf{Y}} \, w_s\mathbb{E}_{\mathrm{shape}} + w_p\mathbb{E}_{\mathrm{pleat}} + w_c\mathbb{E}_{\mathrm{seam}}$$

其中三个能量项各自承担不同的几何约束：

- **形状逼近能量** $\mathbb{E}_{\mathrm{shape}}$ 测量开态Tangram边长相较于闭态目标边长的偏差：
$$\mathbb{E}_{\mathrm{shape}}(\mathbf{Y}) = \sum_{(i,j)\in\mathcal{E}_u} \left(\frac{e_{ij}}{\|\mathbf{y}_i^c - \mathbf{y}_j^c\|_2} - 1\right)^2$$
这里$e_{ij}$是闭态Tangram中的目标边长，$\mathbf{y}_i^c$是开态顶点在优化过程中的当前位置。该能量驱动开态Tangram的边长分布逼近目标曲面的度量，是实现形状逼近的核心机制。

- **褶皱规律能量** $\mathbb{E}_{\mathrm{pleat}}$ 保持褶皱面边界边之间的夹角：
$$\mathbb{E}_{\mathrm{pleat}}(\mathbf{Y}) = \sum_{f\in\mathcal{F}_{\pmb{\mathscr{p}}}} \sum_{(i,j),(j,k)\in f} \frac{1}{2\pi}(\mathcal{L}(\mathbf{e}_{ij},\mathbf{e}_{kj}) - \theta_{ijk})^2$$
其中$\mathcal{F}_{\pmb{\mathscr{p}}}$是所有褶皱面的集合，$\theta_{ijk}$是原始规则图案中边$(i,j)$与$(j,k)$之间的目标夹角。该能量是保护抽褶花纹视觉规律性的关键——没有它，图案在适应目标形状时褶皱会产生严重畸变（见消融实验Fig. 15）。

- **接缝长度一致能量** $\mathbb{E}_{\mathrm{seam}}$ 确保切割产生的对应边保持等长：
$$\mathbb{E}_{\mathrm{seam}}(\mathbf{Y}) = \sum_{(i,j)\in C} \left(\frac{e_{ij}}{e_{ij}'} - \frac{e_{ij}'}{e_{ij}}\right)^2$$
其中$e_{ij}$和$e_{ij}'$是一对对应接缝边的长度。该能量保证物理缝合时两段布料能够精确对齐。

### Changed Slot 3：从无控制到显式褶皱规律保护

**基线方法**在修改图案适应形状时，褶皱的几何形态完全由形状逼近需求被动决定，缺乏主动的美学控制，导致褶皱扭曲、大小不一。

**本文方案**通过$\mathbb{E}_{\mathrm{pleat}}$能量项实现了对褶皱形状的**显式角度约束**。其作用机制是：在开态Tangram中，褶皱面的边界边是衬层面的边界。当形状逼近能量驱动衬层面移动时，这些边界边的相对角度会发生变化。$\mathbb{E}_{\mathrm{pleat}}$施加惩罚，强制相邻边界边之间的夹角维持在原始规则图案中的值$\theta_{ijk}$。这使得优化过程在逼近目标形状的同时，尽可能保持每个褶皱的“展开形态”与原始图案一致，从而在3D中形成规律的褶皱排列。

### 完整流水线与模块间因果链

**模块1：无缝网格化（Seamless Remeshing）**
输入目标曲面，计算无缝N-方向场，生成带奇点的半规则四边形网格。该网格定义了闭态Tangram的组合结构，其面片将对应衬层面。奇点的位置和指数由曲面的高斯曲率分布决定——负曲率区域需要负指数奇点来避免图案重叠。

**模块2：切割与旋转（Cutting & Rotation）**
将闭态Tangram沿选定的边路径切割，将每个面片旋转展开到2D平面。切割路径定义了物理制造中需要缝合的接缝。初始开态Tangram的顶点位置作为后续优化的起点。不同的切割路径和初始旋转角度会影响优化结果，尤其是褶皱的最终体积——从“半闭”状态（褶皱面积较小）开始优化，可得到体积更小的褶皱（Fig. 16）。

**模块3：开Tangram优化（Tangram Optimization）**
这是整个方法的核心计算模块。优化变量是开态Tangram的所有顶点2D坐标$\mathbf{Y}$。三个能量项通过加权和耦合：
- $w_s\mathbb{E}_{\mathrm{shape}}$将目标曲面的度量信息“注入”开态布局，是形状逼近的驱动力。
- $w_p\mathbb{E}_{\mathrm{pleat}}$在形状逼近的过程中“拉住”褶皱边界角，防止图案美学被破坏。
- $w_c\mathbb{E}_{\mathrm{seam}}$保证切割边对的等长性，是物理可制造性的必要条件。

这三个能量项之间存在天然的张力：形状逼近可能要求衬层面大幅移动，从而拉伸或压缩褶皱边界角；褶皱规律约束则抵抗这种变形。权重$w_s$、$w_p$、$w_c$的平衡决定了最终结果在形状精度与褶皱美观之间的取舍。

**模块4：缝合线提取（Pattern Extraction）**
优化完成后，从开态Tangram还原出具体的2D抽褶图案。衬层面的边界直接给出缝合线段的位置和长度。褶皱面则由衬层面之间的空隙区域自然定义。该模块的输出是可直接用于物理制造的完整图案。

**模块5：数字预览（Digital Preview）**
为验证图案质量，使用无缝ARAP（As-Rigid-As-Possible）变形将闭态Tangram的衬层面提升到3D目标位置，再通过均值坐标（MVC）插值估算褶皱顶点的3D位置（Fig. 20）。该预览工具可在数秒内生成逼真的3D抽褶效果，无需实际缝制即可评估设计质量。

### 关键公式的变量含义与作用总结

| 能量项 | 核心变量 | 作用 |
|--------|----------|------|
| $\mathbb{E}_{\mathrm{shape}}$ | $e_{ij}$：闭态目标边长；$\mathbf{y}_i^c$：开态顶点 | 将目标曲面度量编码为边长约束 |
| $\mathbb{E}_{\mathrm{pleat}}$ | $\theta_{ijk}$：原始图案夹角；$\mathbf{e}_{ij}$：褶皱边界边 | 保护褶皱几何规律性 |
| $\mathbb{E}_{\mathrm{seam}}$ | $e_{ij}, e_{ij}'$：对应接缝边长 | 保证物理可缝合性 |

这三个能量项共同构成了从“目标3D形状”到“可制造2D图案”的完整计算桥梁，其因果链为：目标曲面度量 → 闭态Tangram边长 → 形状能量驱动开态优化 → 褶皱能量保护美学 → 接缝能量保证可制造性 → 优化后的开态Tangram → 提取2D图案。

![[assets/figures/papers/paper_list_l19_https_igl_ethz_ch_projects_3dsmocking/figures/024_Figure_23.jpg]]
*Figure 23: Conceptual illustration of applying fabric tessellation in acoustic design for a musical hall*

![[assets/figures/papers/paper_list_l19_https_igl_ethz_ch_projects_3dsmocking/figures/006_Figure_6.jpg]]
*Figure 6: The Tangram-graph paradigm provides an intuitive representation of how pleats are formed during smocking (bottom row). As the stitching lines (colored gray in the top row) become shorter, they drag the adjacent blue underlay faces and make them rotate, forcing the red pleat faces to shrink in 2D (top row) and pop up to form 3D voluminous pleats (middle row)*

## 实验与关键发现

### 主结果：形状逼近精度与运行性能

本文在多种自由曲面上验证了所提出 Tangram 逆设计方法的有效性，涵盖正高斯曲率（半球、心形）、负高斯曲率（Pringle 煎饼形、双曲面）和混合曲率（云朵、环面）等典型情形。核心定量指标为 **Tangram 边再现误差**（edge reproduction error），即优化后开态 Tangram 的边长与闭态目标边长之间的偏差。Table 1 报告了各模型的复杂度与运行性能：在 MacBook M1 Max 平台上，优化时间（$t_{\mathrm{opt}}$）为 5–17 秒，数字预览生成时间（$t_{\mathrm{preview}}$）为 5–16 秒，所有模型的边再现误差均降至 **$10^{-4}$ 以下**，表明 2D 图案能够以极高精度恢复目标曲面的度量结构（Sec. 7.1, Table 1）。

![[assets/figures/papers/paper_list_l19_https_igl_ethz_ch_projects_3dsmocking/figures/022_Table_1.jpg]]
*Table 1: We report the shape complexity (including the number of faces*

这一精度水平源于本文在参数化、能量建模和优化策略上的联合改进。与朴素重网格化方案相比，本文采用的 **无缝等距参数化**（seamless isometric parameterization）能生成尺寸更均匀的衬层面单元，从而降低形状逼近能量的残余误差（Fig. 29, Appendix C）。在双曲面案例上，与 Scherer 2019 所用规则六边形网格相比，本文方法在褶皱规律性和形状保真度上均有显著视觉改善——后者因缺乏奇点支持，在负曲率区域出现明显的褶皱扭曲（Fig. 4, Sec. 7.1）。

![[assets/figures/papers/paper_list_l19_https_igl_ethz_ch_projects_3dsmocking/figures/004_Figure_4.jpg]]
*Figure 4: A hyperbolic surface smocked by different patterns. We show the optimized smocking patterns and a digital preview of the smocked results. The fabrication process comprises the stitching together of line segments, followed by securing them with a knot*

### 消融实验：褶皱能量项的决定性作用

**褶皱规律能量 $\mathbb{E}_{\mathrm{pleat}}$** 的消融实验是最具说服力的因果证据。当从总优化目标中移除该项后，优化器仅追求形状逼近和接缝一致性，导致抽褶花纹的原始几何美感被严重破坏：褶皱面边界边之间的夹角发生任意畸变，图案失去其可辨识的规律性（Fig. 15d）。相比之下，加入 $\mathbb{E}_{\mathrm{pleat}}$ 后，优化结果在逼近目标形状的同时有效保持了原图案的褶皱样式（Fig. 15e）。这证实了显式角度约束对视觉质量的因果作用——形状逼近与褶皱保护之间存在内在张力，需要在优化中显式平衡。

**参数化方案的选择**同样影响褶皱质量。与共形参数化相比，等距参数化产生的褶皱尺寸更均匀，形状逼近误差也更低（Fig. 30, Appendix C）。其因果机制在于：等距参数化使闭态 Tangram 的面片面积更一致，从而在开态优化时，各褶皱面承担的形变更为均衡，避免了局部过度拉伸或压缩。

**初始开态配置**提供了对最终褶皱体积的控制手段。以 WaterBomb 图案为例，从全开 Tangram 开始优化得到体积较大的褶皱，而从半闭 Tangram（褶皱面面积较小）开始则得到体积较小的褶皱（Fig. 16）。这一特性允许用户在形状逼近精度与褶皱视觉密度之间进行权衡。

### 物理制造验证与数字预览一致性

物理制造实例是验证逆设计方法可行性的关键。本文制作了多个物理抽褶模型，包括扭曲甜甜圈（torus）、云朵、心形和半球等（Fig. 19），其外观与数字预览高度一致。环面的内部结构（Fig. 7）清晰展示了闭 Tangram 的三角形网格骨架，验证了 Tangram 图范式对 3D 物理结构的准确预测。此外，本文成功制造了带有不同指数奇点（$1/3, -1/3, 1/4, -1/4, 1/6, -1/6$）的织物样本（Fig. 12），证明无缝参数化引入的奇点可以在物理上实现。

### 失败模式与适用边界

**图案类型限制**：本文方法仅适用于具有旋转对称性的抽褶图案（如 Resch 系列的 $N=3,4,6$）。对于仅具平移对称性的图案，目前无法实现无缝拼接——这是 Tangram 闭态组合逻辑的内在约束，而非优化算法的局限。

**负曲率区域的重叠问题**：当目标曲面包含负高斯曲率区域时，优化后的 2D 图案可能出现面片重叠（Fig. 14）。当前方案需要手动将重叠区域分割并标注在多片织物上，再通过额外缝合完成制造，无法完全自动化。

**物理偏差**：数字预览基于无缝 ARAP 变形与均值坐标（MVC）插值，未考虑真实布料的弯曲刚度、厚度和重力效应。因此，物理实物的褶皱形态可能与预览存在细微偏差，尤其在悬垂或大曲率区域。

**可展开性缺失**：优化得到的闭 Tangram 缺乏可展开性（developability）的理论保证——即使开态 Tangram 是平面的，闭合后的 3D 结构是否一定能从平面状态物理实现，仍是一个开放问题。当前所有成功案例均为经验验证，未给出曲面类别的充要条件。

**切割路径敏感性**：Tangram 的切割与旋转步骤（Sec. 5.2.4）依赖手动或启发式选择切割路径，不同的切割方案可能影响接缝数量、褶皱分布和最终形状逼近精度，该选择尚未自动化。

![[assets/figures/papers/paper_list_l19_https_igl_ethz_ch_projects_3dsmocking/figures/005_Figure_5.jpg]]
*Figure 5: Paper folding vs. fabric stitching. (a) shows the crease pattern of a hexagon Fujimoto twist for paper folding, with black (red) lines representing the mountain (valley) folds, respectively. (b) and (c) show the front and back views of the folded result. The visible region in the front view (b) is highlighted with the same color scheme as in (a). Multiple points in the folded result coincide, such as the set of orange (blue) points highlighted in (d), which correspond to the orange (blue) point in (c). This allows for the design of a smocking pattern (black stitching lines in (d)) that mimics the origami result when smocked, see [Rutzky and Palmer 2011, page 17]*

![[assets/figures/papers/paper_list_l19_https_igl_ethz_ch_projects_3dsmocking/figures/015_Figure_15.jpg]]
*Figure 15: Explicit control over pleat shapes is essential in solving the inverse design problem. Modifying the 2D smocking pattern to approximate a 3D shape can potentially damage the pleat shape if no regularizer is added, as shown in (d). For comparison, our formulation allows to effectively preserve the pleat shapes, shown in (e)*

## 定位与知识库关联

本文的核心贡献在于为“通过抽褶实现自由曲面”这一逆设计问题建立了首个可计算的形式化框架。其相对于已有工作的本质差异，可以从“改变的是哪一个 slot”这一角度得到清晰定位。

### 改变的 Slot：从“局部启发式”到“全局可微优化”

在本文之前，抽褶图案的设计主要依赖两种范式：一是手工设计的规则图案（如传统刺绣和手工艺中的经典花纹），二是基于启发式刚性变换的局部布局方法。这两种范式共享一个根本局限——**缺乏从 2D 缝合线布局到 3D 形状误差之间的可微映射**，因此无法对任意给定的自由曲面进行系统性的逆设计。本文通过引入 **Tangram 图**这一中间表示，将这一映射显式化，从而将问题转化为一个可直接优化的能量最小化问题。具体而言：

- **Scherer 2019** 等方法使用规则六边形网格对曲面进行参数化，但未引入奇点，且图案生成依赖局部启发式规则，无法处理任意曲率的自由曲面。本文将其替换为**无缝 N-方向场驱动的半规则网格化**，允许在必要位置引入奇点（索引为 ±1/3, ±1/4, ±1/6 等），从而使参数化更等距、更适应曲率变化（见 Fig. 29, Fig. 30）。
- 传统方法对**褶皱的视觉规律性无显式控制**——当图案被强行适应目标形状时，褶皱常发生严重畸变。本文引入褶皱能量项 $\mathbb{E}_{\mathrm{pleat}}$，通过强制保持相邻褶皱边界边的夹角，将图案原有的几何美学作为软约束嵌入优化目标，实现了形状逼近与褶皱规则性的解耦控制（消融实验见 Fig. 15）。

这一 slot 改变的深层逻辑是：将抽褶逆设计从“设计图案→模拟结果→手工调整”的试错循环，升级为“定义 Tangram→优化开态顶点→提取缝合线”的端到端计算流程。

### 知识库挂载点

本文的方法论贡献可挂载到以下知识库节点：

1. **计算折纸（Computational Origami）的“折叠-展开”对偶性**：  
   本文从 Resch 系列折纸图案（Resch 1968; Tachi 2013）出发，利用“折纸折叠中多个点重合”这一现象，推导出等价的抽褶缝合线布局（Fig. 5, Fig. 10）。这一从折纸到织物镶嵌的转换机制，为折纸图案库向可缝纫图案的自动翻译提供了理论基础。反向问题——“能否从抽褶图案自动推导出等价折纸图案”——则作为开放问题被明确列出。

2. **无缝参数化与方向场设计（Seamless Parameterization & N-RoSy Fields）**：  
   本文的网格化模块直接建立在 N-方向场和无缝参数化的成熟理论之上（如 Bommes et al. 2009 等的 QuadCover 相关工作），但将其应用场景从四边形网格生成拓展到了“为 Tangram 闭态提供组合模板”。奇点索引与抽褶图案的旋转对称性（N=3,4,6）之间的对应关系，是这一挂载点的关键连接。

3. **物理模拟与逆向设计（Inverse Design in Physics-Based Graphics）**：  
   本文的优化框架（形状能量 + 褶皱能量 + 接缝能量）与计算机图形学中“通过优化实现逆向设计”的传统一脉相承（如 Origamizer [Tachi 2008] 的折纸逆设计），但其目标域从刚性折纸转移到了柔性织物。值得注意的是，本文**未模拟真实布料的弯曲、厚度和重力**，数字预览仅依赖无缝 ARAP 变形和均值坐标（MVC）插值（Fig. 20），因此实物与预览之间存在系统偏差——这一简化既是方法的实用性保障，也是其当前边界。

### 适用边界与局限

本文方法的适用边界由以下条件共同界定：

- **图案对称性约束**：仅支持具有旋转对称性的抽褶图案（Resch 系列的 N=3,4,6），对于仅具平移对称性的图案（如部分 Brick、Diamond 变体），目前无法实现无缝拼接。这是由 Tangram 闭态的组合结构决定的——旋转对称性保证了闭态面片可以构成一个无重叠的平面镶嵌。
- **负高斯曲率的处理**：当目标曲面包含负高斯曲率区域时，优化后的开态 Tangram 会产生面片重叠（Fig. 14）。当前解决方案是手动分割重叠区域并标注在两块布料上分别缝制，尚未实现自动化。
- **可展开性缺乏理论保证**：优化得到的闭 Tangram 是否一定能从平面开态通过物理缝合实现，本文未给出理论证明。这导致某些极端曲率的目标形状可能在物理制造中失败——这是一个需要后续工作填补的理论空白。
- **材料物理属性的忽略**：如 7.2 节所述，真实布料的弹性、弯曲刚度和重力效应未被纳入优化模型，因此数字预览（见 Fig. 19 的 column (d)）与物理实物（column (e)）之间可能存在细微偏差，尤其在褶皱体积和悬垂形态方面。

### 后续启发与可扩展方向

本文为多个方向提供了方法论起点：

1. **可编程拉胀材料（Programmable Auxetics）**：  
   如 Fig. 25 所示，本文的 Tangram 优化框架可直接应用于设计“从近闭合状态膨胀到目标形状”的拉胀结构。这一扩展将织物镶嵌从静态造型拓展到了动态变形设计，为软体机器人和可展开结构提供了新的设计工具。

2. **建筑与声学设计**：  
   Fig. 22 和 Fig. 23 分别展示了自由形式建筑表皮和音乐厅声学设计的应用场景。Tangram 框架提供的“精确几何控制 + 可预测褶皱纹理”的组合，使织物镶嵌成为一种兼具结构性能与美学表达的建筑表皮方案。

3. **与折纸的双向翻译**：  
   本文已验证了从 Resch 折纸图案到抽褶图案的单向推导。若能建立双向翻译的通用理论，将使两个领域的设计工具和图案库实现互通，极大扩展可用图案的空间。

4. **物理感知优化**：  
   将布料的弯曲刚度、厚度和重力纳入优化目标或约束，有望缩小数字预览与实物之间的差距，使框架从“几何逆设计”升级为“物理逆设计”。这需要引入可微布料模拟器或数据驱动的代理模型。

5. **切割路径自动化**：  
   当前接缝的切割路径依赖人工选择，不同路径会影响最终结果的形状逼近精度和褶皱分布。将切割路径也纳入优化变量，有望进一步提升方法的自动化程度和结果质量。

综上，本文的核心定位是：**在计算折纸和织物手工艺的交叉点上，首次建立了基于 Tangram 中间表示的、可优化的抽褶逆设计框架**。其改变的 slot 是从局部启发式到全局可微优化的范式转换，知识库挂载点涵盖计算折纸、无缝参数化和逆向设计三个领域，适用边界受限于图案对称性、负曲率处理和物理建模的简化，但已为拉胀材料、建筑设计和物理感知优化等方向提供了清晰的方法论延伸路径。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Fabric_Tessellation_Realizing_Freeform_Surfaces_by_Smocking.pdf]]