---
title: "SMEAR: Stylized Motion Exaggeration with ARt-direction"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/SMEAR_Stylized_Motion_Exaggeration_with_ARt_direction.pdf
aliases:
- SMEAR
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 基于对象运动结构的运动偏移量（分离平面/带）计算和可插拔的风格化函数，提供了艺术家对顶点领前/滞后程度的直接控制。
primary_logic: 通过将运动偏移量定义为顶点到分离面（简单对象）或分离带（关节对象）的归一化符号距离，可以在不改变输入姿态和网格拓扑的前提下，对网格进行沿轨迹的变形，从而生成保留对象细节和可识别性的涂抹帧效果。
claims:
- 方法分为两步：计算运动偏移量，然后进行风格化。
- 运动偏移量是分配给各顶点的标量值，表示其引领或滞后的程度。
- 使用运动偏移量能够生成拉长中间帧、多重中间帧和运动线三种涂抹帧效果。
- 方法比基于扫掠体积的方法快几个数量级（0.007秒/帧 vs 7秒/帧）。
---

# SMEAR: Stylized Motion Exaggeration with ARt-direction

> [!tip] 核心洞察
> 通过将运动偏移量定义为顶点到分离面（简单对象）或分离带（关节对象）的归一化符号距离，可以在不改变输入姿态和网格拓扑的前提下，对网格进行沿轨迹的变形，从而生成保留对象细节和可识别性的涂抹帧效果。

| 字段 | 内容 |
|------|------|
| 中文题名 | SMEAR: 艺术导向的风格化运动夸张 |
| 英文题名 | SMEAR: Stylized Motion Exaggeration with ARt-direction |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [Code](https://github.com/MoStyle/SMEAR) · [paper](https://doi.org/10.1145/3641519.3657457) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SMEAR |
| Dataset | Motion offsets pre-processing performance, Memory usage per frame, Qualitative comparison: elongated in-betweens vs. swept volumes |

> [!tip] 效果简介
> - Motion offsets pre-processing performance (Table 1) 上，Time per frame (ms) 4 ms (482 verts), 5 ms (1344 verts), 70 ms (14267 verts, 65 bones) vs Swept volumes ~7000 ms per frame (Sellan et al. 2021) for a simple object (Up to ~1750× faster (4 ms vs. 7000 ms) for simple objects; ~100× faster (70 ms...)。
> - Memory usage per frame (Table 1) 上，Memory per frame (KB) 10 KB (482 verts), 27 KB (1344 verts), 280 KB (14267 verts, 65 bones) vs Not reported (Extremely low memory footprint, enabling interactive workflows)。
> - Qualitative comparison: elongated in-betweens vs. swept volumes 上，Visual preservation of object details and concavities Elongated in-betweens maintain surface details and concavities vs Swept volumes (Sellan et al. 2021) lose high-frequency details and hide concavi... (Our method produces more recognizable objects with preserved details)。

## 概述

传统二维动画中，艺术家通过“涂抹帧”（smear frames）在快速动作中故意扭曲对象形状，以传达运动速度和方向感。然而，在三维动画领域，自动生成具有艺术控制力的涂抹帧效果——尤其是拉长中间帧（elongated in-betweens）、多重中间帧（multiple in-betweens）和运动线（motion lines）——一直是一个未充分解决的问题。现有方法要么依赖计算成本高昂的扫掠体积（如 **Sellán et al., 2021**），难以保留对象表面细节和凹面结构；要么缺乏对艺术风格的精细控制，无法无缝集成到标准动画工作流中。

SMEAR 方法（SIGGRAPH 2024）针对这一瓶颈提出了一个两阶段框架：**先计算运动偏移量，再进行风格化变形**。其核心洞见在于，通过将运动偏移量定义为顶点到分离面（简单对象）或分离带（关节对象）的归一化符号距离，可以在不改变输入姿态和网格拓扑的前提下，对网格沿运动轨迹进行变形，从而生成保留对象细节和可识别性的涂抹帧效果。

运动偏移量是分配给每个顶点的标量值 $\bar{\delta}_i(f) \in [-1,1]$，表示该顶点相对于对象运动方向的“领前”或“滞后”程度。这一紧凑的中间表示构成了整个风格化流水线的因果旋钮：艺术家可以通过预设的风格化函数（如 $S_E$、$S_E^{\text{speed}}$、$S_M$ 等）或自定义节点图，直接控制变形强度、时间偏移和效果组合，而无需修改输入动画或网格拓扑。

在性能方面，SMEAR 的运动偏移量预处理比扫掠体积方法快数个数量级——对于简单对象仅需 4 ms/帧，而扫掠体积约需 7000 ms/帧（提速约 1750 倍）；对于具有 65 根骨骼的复杂角色也仅需 70 ms/帧，内存占用低至 280 KB/帧。该方法已实现为 Blender 几何节点插件，支持交互式预设和高级自定义，能够生成从简洁到复杂的多种运动夸张效果，并可组合使用三种涂抹帧效果以创建丰富的运动风格化。

**方法定位**：SMEAR 属于基于几何变形的非真实感渲染（NPR）方法，区别于基于物理模拟或后处理合成的方法。它通过一个轻量、可插拔的运动偏移量计算模块，将艺术控制权交给动画师，同时保持与现有动画工作流的兼容性。其主要局限性包括：对称旋转对象的自相交问题（需手动 UV 空间技巧解决）、细长肢体（如手指）的过度变形（需骨骼修剪），以及目前仅适用于关键帧动画输入。

## 背景与动机

### 涂抹帧：从2D动画到3D的挑战

在传统2D动画中，涂抹帧（smear frames）是一种经典的运动夸张手法——通过在快速动作中拉伸对象形态，在单帧内传达速度感和运动方向（Figure 2）。这种技术不仅增强了视觉冲击力，还利用了人眼的视觉暂留效应，使观众感知到流畅的连续运动。然而，将这一艺术手段迁移至3D动画领域面临着根本性困难：3D对象具有完整的几何拓扑，如何在保持对象可识别性和表面细节的前提下，生成可控的变形效果，同时无缝嵌入现有的动画制作流程，一直缺乏有效方案。

### 现有方法的瓶颈

当前3D动画中生成涂抹帧效果的尝试主要存在两条路径，各自面临显著局限。基于扫掠体积的方法（如 **Swept volumes**, Sellán et al., 2021）通过沿运动轨迹构建对象的体积包络来生成变形网格，但其计算开销极高（单帧约7秒），且结果会丢失表面高频细节和凹陷特征，导致对象可识别性下降（Figure 9）。另一方面，简单的局部几何方法（如点积法，Jones and Keyser, 2005）虽然计算快速，但缺乏全局运动结构的理解，在关节对象上容易产生剪切伪影和不连贯的变形（Figure 4）。更根本的是，这些方法都未能提供艺术家对变形程度、方向和范围的直接控制，难以融入以艺术导向为核心的动画工作流。

### 核心瓶颈与本文动机

上述困境的实质瓶颈在于：**现有方法难以在保持艺术交互性和动画工作流集成的同时，自动生成具有艺术控制性的涂抹帧效果，尤其是拉长中间帧（elongated in-betweens）。** 具体而言，挑战体现在三个层面：

1. **运动结构理解**：需要一种能感知对象整体运动结构（刚体或关节体）的机制，而非仅依赖局部几何信息。
2. **拓扑保持与细节保留**：变形后的网格必须与原网格保持同胚，避免扫掠体积方法中常见的细节丢失和凹陷隐藏。
3. **艺术控制性**：艺术家应能通过直观参数控制变形的强度、范围和时间特性，而非面对黑箱式的物理模拟。

本文提出的SMEAR方法正是针对这一瓶颈，通过引入**运动偏移量（motion offsets）** 这一核心概念，将运动结构分析与风格化变形解耦，从而在计算效率、几何质量和艺术控制性三个维度上同时取得突破。运动偏移量定义为各顶点到分离结构的归一化符号距离，既编码了对象沿运动方向的前导/滞后关系，又保持了与输入网格拓扑的一致性，为后续的多样化风格化提供了统一的数学基础。

## 核心创新

SMEAR 的核心创新在于将 3D 动画的涂抹帧（smear frame）生成从一个缺乏艺术控制的几何后处理问题，重新定义为**基于运动偏移量（motion offsets）的可微分风格化框架**。这一框架的根本突破体现在以下三个关键维度的改变上。

### 从局部法向投影到全局运动分离

传统方法（如 **Jones and Keyser, 2005** 的点积法）计算运动偏移量时，仅依赖顶点法向与速度的点积。这种局部操作对网格朝向极其敏感，在旋转或复杂运动中会产生不连贯的偏移量分布，导致拉伸变形撕裂对象结构（见 Figure 4 左半部的花生模型对比）。

SMEAR 将运动偏移量重新定义为**顶点到分离结构的归一化符号距离**：
- 对简单对象，使用过质心、法向为归一化速度的**分离平面**（separation plane），偏移量 $\bar{\delta}_i = \frac{(\mathbf{p}_i - \mathbf{c}) \cdot \hat{\mathbf{v}}}{\max_j |\delta_j|}$（Equation 1）；
- 对关节角色，使用沿骨骼延伸、局部正交于运动方向的**分离带**（separation ribbon），并通过球面线性插值（SLERP）平滑过渡根部和尖部的运动方向（Equation 4）。

这一改变将偏移量计算从“逐顶点局部估计”升级为“基于对象运动结构的全局划分”，使得领前（leading）和滞后（trailing）的语义在整个对象上保持空间连贯。**因果机制**在于：分离平面/带直接编码了“运动方向”这一全局信息，而非依赖顶点法向这一局部几何属性，从而对网格拓扑和朝向变化具有天然的鲁棒性。

### 从扫掠体积到保持拓扑的顶点位移

生成涂抹帧的另一种路径是基于扫掠体积（swept volumes），如 **Sellán et al., 2021** 的方法。扫掠体积沿轨迹扫过对象生成凸包，虽然能产生类似效果，但存在两个根本缺陷：
- **丢失表面细节**：扫掠过程会隐藏凹面和高频细节，导致对象可识别性下降（Figure 9 对比）；
- **计算代价极高**：单个简单对象的扫掠体积计算约需 7000 ms/帧，而 SMEAR 的运动偏移量预处理仅需 4 ms/帧（Table 1），速度提升约 1750 倍。

SMEAR 的关键改变在于**输出网格保持与输入相同的拓扑结构**。风格化过程不是生成新几何体，而是将运动偏移量作为标量场，通过风格化函数 $S_E$ 沿 Catmull-Rom 样条轨迹对原始顶点进行位移（Equation 10）。这意味着所有表面细节、UV 坐标和材质属性天然保留，且不会引入自相交之外的拓扑缺陷。**瓶颈突破**：将涂抹帧生成从“体积重建问题”转化为“顶点位移问题”，既保留了对象细节，又实现了数量级的性能飞跃。

### 从固定效果到可插拔的风格化引擎

此前的方法（无论是点积变形还是扫掠体积）产生的涂抹帧效果是固定的，艺术家无法在不修改输入动画的前提下调整风格。SMEAR 通过**解耦运动偏移量计算与风格化函数**，将艺术控制提升为第一类设计目标：

- 运动偏移量 $\bar{\delta}_i(f) \in [-1, 1]$ 作为一个中间表示，编码了“哪些部分领前、哪些部分滞后”的物理语义，与具体风格无关；
- 风格化函数（如 $S_E$、$S_E^{\text{speed}}$、$S_M$、$S_L$ 等）作为可插拔模块，接收运动偏移量和参数，输出顶点位移、不透明度或运动线长度；
- 艺术家可以通过 Blender 几何节点（Geometry Nodes）交互式调整参数，甚至构建自定义节点图组合多种效果（Figure 16）。

这一架构的**核心洞察**在于：运动偏移量作为一个归一化的、对象结构感知的标量场，天然适合作为风格化函数的输入域。不同的风格化函数（速度加权 $S_E^{\text{speed}}$、噪声调制 $S_E^{\text{noise}}$ 等）可以在不重新计算偏移量的前提下产生从简洁到复杂的多种效果（Figure 11），且通过变形运动偏移量（warped motion offsets）还能实现时间偏移效果（Figure 12），将风格化推向过去或未来帧。

### 总结

SMEAR 相对于 baselines 的创新可归纳为一次**表示层的范式转移**：用“运动偏移量 + 风格化函数”替代了“局部几何操作”或“体积重建”，在保持输入拓扑和细节的前提下，将涂抹帧生成从计算密集的几何处理转变为轻量、可控、可组合的艺术创作原语。这一转移的直接证据是：在性能上实现了三个数量级的加速（Table 1），在效果上保留了扫掠体积无法保留的凹面和细节（Figure 9），在控制上提供了从全局预设到逐顶点权重绘制的多层次艺术接口（Section 5.1, Figure 15）。

## 整体框架

SMEAR 的整体管线遵循“运动结构分析→风格化变形”的两阶段范式，其核心设计目标是**在不改变输入姿态和网格拓扑的前提下**，将艺术导向的涂抹帧效果自动注入到现有动画工作流中。

### 输入与输出

管线接收标准的关键帧动画作为输入，包括随时间变化的网格顶点位置序列和（对于关节对象）骨骼层次结构。输出为三种可组合的涂抹帧效果：**拉长中间帧**（elongated in-betweens）、**多重中间帧**（multiple in-betweens）和**运动线**（motion lines）。所有效果的生成均基于一个统一的中间表示——运动偏移量（motion offsets）。

### 两阶段管线

**第一阶段：运动偏移量计算（Motion Offset Computation）**

这是整个框架的基石模块。对于输入动画的每一帧，系统为每个网格顶点 $i$ 分配一个标量值 $\bar{\delta}_i(f) \in [-1,1]$，称为运动偏移量。该值的符号和大小编码了顶点在运动方向上是“领前”（正值）还是“滞后”（负值），以及领前/滞后的程度。偏移量的计算依据对象的结构类型分为两条路径：

- **简单对象**：以对象质心 $\mathbf{c}$ 和归一化速度 $\hat{\mathbf{v}}$ 定义分离平面，运动偏移量为顶点到该平面的归一化符号距离 $\bar{\delta}_i = \frac{(\mathbf{p}_i - \mathbf{c}) \cdot \hat{\mathbf{v}}}{\max_j |\delta_j|}$。
- **关节对象**：沿每根骨骼构建与骨骼轴正交且尽可能对齐局部运动方向的“分离带”（ribbon），计算顶点到带面的归一化符号距离，并引入共线权重 $w_{\text{coll.}}$ 抑制骨骼轴向运动导致的剪切伪影。多骨骼影响下的顶点通过蒙皮权重对各骨骼偏移量进行混合。

计算完成后，可施加时间窗口平滑以消除运动方向快速变化引起的偏移量突变。

**第二阶段：风格化引擎（Stylization Engine）**

基于第一阶段输出的运动偏移量，通过可插拔的风格化函数对网格进行变形或生成辅助几何体：

- **拉长中间帧**：将顶点沿其 Catmull-Rom 样条轨迹位移，位移量由风格化函数 $S_E(\bar{\delta}_i(f); \text{args})$ 控制。艺术家可通过调整函数参数（如最大位移量、速度加权等）直接控制变形强度。
- **多重中间帧**：扩展拉长中间帧框架，通过控制轨迹上多个采样点的不透明度实现视网膜持续性效果。
- **运动线**：在顶点轨迹上追踪生成薄管状网格，运动线长度由风格化函数 $S_L(\bar{\delta}_\ell(f); \text{args})$ 控制。

### 模块关系与数据流

两个阶段之间通过**运动偏移量**这一紧凑的中间表示解耦：第一阶段仅依赖输入动画的运动结构（质心/骨骼轨迹），与最终风格化效果无关；第二阶段仅消费运动偏移量，不接触原始动画数据。这种设计使得：

1. 运动偏移量可预计算并缓存（内存占用极低，14267 顶点/65 骨骼的模型仅需 280 KB/帧），艺术家可实时调整风格化参数而无需重新分析运动。
2. 风格化函数可自由替换和组合，形成从简洁到复杂的多种夸张效果。
3. 整个管线可作为 Blender 几何节点插件集成，支持交互式预设和高级自定义节点图。

### 与现有方法的根本差异

相比于基于扫掠体积的方法（如 **Sellán et al., 2021**），SMEAR 不生成新的体积几何，而是直接变形输入网格，因此保持了原始拓扑和表面细节（如凹陷和高频纹理），同时计算速度快几个数量级（简单对象约 4 ms/帧 vs. 扫掠体积约 7000 ms/帧）。相比于简单的局部点积方法（如 **Jones and Keyser, 2005**），SMEAR 的分离平面/带方法提供了空间上更一致的领前/滞后划分，避免了局部法线方向导致的噪声偏移量。

## 核心模块与公式推导

SMEAR 方法的核心流水线由两个关键模块构成：**运动偏移量计算**（Motion Offset Computation）与**风格化引擎**（Stylization Engine）。前者为每个顶点分配一个标量值 $\bar{\delta}_i(f) \in [-1, 1]$，表示该顶点在运动方向上“领前”（正值）或“滞后”（负值）的程度；后者以运动偏移量为输入，通过可插拔的风格化函数驱动网格变形，生成拉长中间帧、多重中间帧和运动线三种涂抹帧效果。

### 3.1 简单对象的运动偏移量

对于无骨骼的简单对象，运动偏移量定义为顶点到**分离平面**的归一化符号距离。分离平面以对象质心 $\mathbf{c}$ 为基点，以归一化速度 $\hat{\mathbf{v}}$ 为法向量：

$$
\bar{\delta}_i = \frac{\delta_i}{\max_j |\delta_j|} \quad \text{with} \quad \delta_i = (\mathbf{p}_i - \mathbf{c}) \cdot \hat{\mathbf{v}}
$$

该公式的因果机制在于：通过全局的质心-速度分离平面，将对象表面划分为“面向运动方向”和“背向运动方向”两个区域，从而获得空间连续的运动偏移量分布。与局部方法（如 **dot product method**，Jones and Keyser 2005）相比，全局分离平面避免了因顶点法向局部变化导致的偏移量不连续问题（Figure 4）。

![[assets/figures/papers/paper_list_l7_SMEAR_Stylized_Motion_Exaggeration_with_ARt_direction_motion20v2/figures/004_Figure_4.jpg]]
*Figure 4: Motion offsets and corresponding elongated in-between for a peanut model translating left to right, computed (left) as the dot product of the centroid velocity and vertex normals, and (right) with our approach*

为抑制运动方向快速变化引起的偏移量突变，对运动偏移量施加时间窗口为 $2N+1$ 的加权平均：

$$
\bar{\delta}_i(f) = \sum_{n=-N}^{N} w_n \bar{\delta}_i(f+n)
$$

### 3.2 关节对象的运动偏移量

对于带骨骼的关节对象，分离结构从平面推广为沿骨骼延伸的**分离带**（ribbon）。分离带法向量 $\hat{\mathbf{n}}(u)$ 要求同时正交于骨骼轴 $\hat{\mathbf{b}}$ 并尽可能对齐到局部运动方向 $\hat{\mathbf{v}}(u)$。

首先将顶点 $\mathbf{p}_i$ 映射为沿骨骼的一维参数位置 $u_i$，再通过球面线性插值（SLERP）获得该位置的局部运动方向：

$$
\hat{\mathbf{v}}(u) = \frac{\sin((1-u)\omega)}{\sin(\omega)} \hat{\mathbf{v}}_r + \frac{\sin(u\omega)}{\sin(\omega)} \hat{\mathbf{v}}_t, \quad \omega = \arccos(\hat{\mathbf{v}}_r \cdot \hat{\mathbf{v}}_t)
$$

其中 $\hat{\mathbf{v}}_r$ 和 $\hat{\mathbf{v}}_t$ 分别为骨骼根部和尖部的归一化速度。

单骨骼的运动偏移量在此基础上引入**共线权重** $w_{\text{coll.}}(u) = 1 - (\hat{\mathbf{v}}(u) \cdot \hat{\mathbf{b}})^2$，以抑制骨骼轴向运动导致的剪切伪影（消融实验 Figure 7 验证了该权重的必要性）：

![[assets/figures/papers/paper_list_l7_SMEAR_Stylized_Motion_Exaggeration_with_ARt_direction_motion20v2/figures/008_Figure_7.jpg]]
*Figure 7: Motion offsets computed for the animation in (a), weighted according to motion collinearity (c), and without this weighting scheme (b), yielding a noticeable shearing*

$$
\bar{\delta}_i = w_{\text{coll.}}(u_i) \frac{\delta_i}{\max_j |\delta_j|} \quad \text{with} \quad \delta_i = (\mathbf{p}_i - \mathbf{c}_r) \cdot \hat{\mathbf{n}}(u_i)
$$

对于受多骨骼影响的顶点，通过蒙皮权重 $w_{ik}$ 对各骨骼的运动偏移量进行混合（借鉴 **velocity skinning**，Rohmer et al. 2021 的权重混合策略）：

$$
\bar{\delta}_i = \sum_k w_{ik} \bar{\delta}_{ik}
$$

混合归一化因子 $M_{ik}$ 在骨骼根部顶点集 $\mathcal{V}_{k,r}$ 与尖部顶点集 $\mathcal{V}_{k,t}$ 的最大偏移量之间平滑过渡，避免关节处偏移量范围的突变（Figure 8 对比了不同归一化策略的效果）：

![[assets/figures/papers/paper_list_l7_SMEAR_Stylized_Motion_Exaggeration_with_ARt_direction_motion20v2/figures/009_Figure_8.jpg]]
*Figure 8: Motion offsets computed for the animation in (a) with different normalization factors (b-c). In (d), we compare the motion offsets computed considering all bones (left) with those obtained by considering the hand as a single body part affected by the forearm bone (right)*

$$
M_{ik} = u_{ik} \max_{j \in \mathcal{V}_{k,r}} |\delta_{jk}| + (1 - u_{ik}) \max_{j \in \mathcal{V}_{k,t}} |\delta_{jk}|
$$

### 4.1 拉长中间帧的顶点位移

获得运动偏移量后，拉长中间帧通过沿 Catmull-Rom 样条轨迹位移顶点来生成。顶点 $\mathbf{p}_i$ 在帧 $f$ 处的位移量由风格化函数 $S_E$ 作用于运动偏移量来控制：

$$
\beta_i(f) = S_E(\bar{\delta}_i(f); \text{args})
$$

风格化函数是可插拔的。例如，速度加权风格化函数 $S_E^{\text{speed}}$ 使位移量与顶点速度范数成正比，仅快速运动部分产生明显变形（Figure 12）：

$$
S_E^{\text{speed}}(\bar{\delta}_i; \mathbf{v}_i, \beta_{\max}) = \beta_{\max} \|\mathbf{v}_i\| \bar{\delta}_i
$$

运动线的长度同样由风格化函数控制：$\tau_{\ell}(f) = S_L(\bar{\delta}_{\ell}(f); \text{args})$，其中 $\bar{\delta}_{\ell}$ 为种子点 $\ell$ 的运动偏移量。

### 性能瓶颈与效率

运动偏移量计算是预处理步骤，其性能表现决定了整个流水线的交互性。Table 1 报告了在 Intel Core i9-7920X 2.90GHz CPU 上的测量结果：对于 482 顶点的简单对象仅需 4 ms/帧，对于 14267 顶点、65 根骨骼的复杂角色需 70 ms/帧。相比之下，基于扫掠体积的方法（**Swept volumes**，Sellán et al. 2021）对简单对象需约 7000 ms/帧，SMEAR 实现了约 1750 倍的加速（Figure 9）。内存占用同样极低，复杂角色仅需 280 KB/帧，使得交互式工作流成为可能。

### 补充图表

![[assets/figures/papers/paper_list_l7_SMEAR_Stylized_Motion_Exaggeration_with_ARt_direction_motion20v2/figures/007_Figure_6.jpg]]
*Figure 6: Motion offsets for a two-bones capsule, with onion skin visualization of the animation. Left: motion offsets computed using a secant plane as in Section 3.1. Right: motion offsets computed using a ribbon separation surface depending on the local motion direction*

![[assets/figures/papers/paper_list_l7_SMEAR_Stylized_Motion_Exaggeration_with_ARt_direction_motion20v2/figures/022_Figure_16.jpg]]
*Figure 16: The stylization effects achievable by our method may be combined to create complex motion stylizations*

## 实验与分析

### 主结果：性能与视觉质量

SMEAR 在预处理性能和视觉保真度两个维度上均展现出对基线方法的显著优势，其核心性能数据汇总于 **Table 1**。该方法在 Intel Core i9-7920X 2.90GHz CPU 上测量了不同复杂度对象的预处理开销，结果如下：

![[assets/figures/papers/paper_list_l7_SMEAR_Stylized_Motion_Exaggeration_with_ARt_direction_motion20v2/figures/010_Table_1.jpg]]
*Table 1: Pre-processing time and memory usage per frame on a computer with an Intel Core i9-7920X 2.90GHz CPU*

- **简单对象（482 顶点）**：每帧处理时间仅 4 ms，内存占用 10 KB。
- **中等对象（1344 顶点）**：每帧处理时间 5 ms，内存占用 27 KB。
- **复杂关节角色（14267 顶点，65 骨骼）**：每帧处理时间 70 ms，内存占用 280 KB。

与基于扫掠体积的方法（Sellán et al., 2021）相比，SMEAR 的速度优势极为突出。扫掠体积在简单对象上每帧耗时约 7000 ms，SMEAR 的 4 ms 处理时间意味着约 **1750 倍的加速**；即使在复杂的关节角色上，70 ms 的预处理时间也实现了约 **100 倍的加速**。这一性能差距的根源在于两种方法的核心机制差异：扫掠体积需要在每帧之间计算对象的完整扫掠几何体，计算复杂度随顶点数和轨迹曲率急剧增长；而 SMEAR 的运动偏移量计算仅依赖于分离面/带的解析距离和归一化操作，其复杂度与顶点数呈线性关系，且完全避开了体积重建的昂贵步骤。

在视觉质量方面，**Figure 9** 的定性对比揭示了两种方法的本质差异。对于同一简单对象的动画输入，SMEAR 生成的拉长中间帧完整保留了输入网格的拓扑结构和表面细节，包括凹面区域在内的几何特征均得到忠实呈现。相比之下，扫掠体积方法（Sellán et al., 2021）生成的中间体丢失了高频表面细节，且凹面区域被扫掠体的凸包所隐藏。这一差异的因果机制在于：SMEAR 通过沿轨迹位移顶点来变形原始网格，输出网格与输入网格保持同胚（homeomorphic），因此所有表面细节自然保留；而扫掠体积本质上是运动轨迹的并集，其边界由轨迹的外包络决定，无法表达凹面区域的内部结构。

![[assets/figures/papers/paper_list_l7_SMEAR_Stylized_Motion_Exaggeration_with_ARt_direction_motion20v2/figures/021_Figure_9.jpg]]
*Figure 9: Using (a) the animation of a simple object, we compare (b) elongated in-betweens generated by our method with the simple stylization function*

### 消融实验

#### 共线权重的作用

**Figure 7** 展示了共线权重（collinear weight）对运动偏移量质量的关键影响。当骨骼轴向运动分量较大时，若不加共线权重抑制，分离带法线会与骨骼轴产生较大的点积分量，导致运动偏移量在骨骼周围出现明显的剪切伪影（shearing artifacts）。共线权重项 $w_{\mathrm{coll.}}(u) = 1 - (\hat{\mathbf{v}}(u) \cdot \hat{\mathbf{b}})^2$ 通过检测局部运动方向与骨骼轴的共线程度，在运动方向趋近骨骼轴时自动衰减运动偏移量的幅值，从而消除了这种剪切失真。该消融实验直接验证了共线权重设计的必要性。

#### 归一化策略的影响

运动偏移量的归一化方式直接影响变形结果的空间分布。**Figure 8** 对比了不同归一化因子的效果。基于每骨骼最大值的归一化（per-bone max normalization）相比每部件归一化（per-part normalization）提供了更平滑的跨关节过渡。这是因为混合归一化项 $M_{ik} = u_{ik} \max_{j \in \mathcal{V}_{k,r}} |\delta_{jk}| + (1 - u_{ik}) \max_{j \in \mathcal{V}_{k,t}} |\delta_{jk}|$ 在骨骼根部和尖部的最大值之间根据参数位置 $u_{ik}$ 进行线性插值，避免了在关节处出现运动偏移量的不连续跳变。这一设计对于关节角色的自然变形至关重要。

#### 骨骼修剪对细长肢体的影响

**Figure 13** 揭示了将手指独立视为单独骨骼进行运动偏移量计算时的问题。细长肢体（如手指）在快速运动中会产生极端的运动偏移量值，导致拉长中间帧出现过度变形，使手指被拉伸至不自然的长度。通过骨骼修剪（bone pruning）将整个手部视为受前臂骨骼影响的单一身体部分，可以有效抑制这种过度变形。该消融实验表明，运动偏移量的骨骼粒度需要根据肢体比例进行手动调整，目前尚缺乏自动化的自适应机制。

#### 时间平滑的影响

时间平滑（Equation 2）对运动偏移量的时序稳定性有显著贡献。当运动方向在相邻帧之间发生快速变化时（例如物体突然转向），未平滑的运动偏移量会出现突变，导致风格化后的网格在时序上产生抖动。通过施加时间窗口为 $2N+1$ 的加权平均，时间平滑有效抑制了这种高频扰动。补充视频中展示了平滑前后的对比效果，但论文未提供定量的平滑参数消融数据。

#### 风格化函数的多样性

**Figure 11** 和 **Figure 16** 展示了不同风格化函数对同一输入动画产生的多样化效果。从简单的线性拉伸 $S_E$ 到速度加权拉伸 $S_E^{\mathrm{speed}}$、噪声扰动拉伸 $S_E^{\mathrm{noise}}$ 以及多重中间帧函数 $S_M$，艺术家可以通过选择不同的风格化函数和高层参数实现从简洁到复杂的运动夸张效果。这种可插拔的模块化设计是 SMEAR 艺术控制性的核心体现。**Figure 12** 进一步展示了变形运动偏移量（warped motion offsets）可以实现时间偏移效果，将风格化推向过去或未来帧，为艺术创作提供了额外的时间维度控制。

### 失败模式与局限性

尽管 SMEAR 在性能和视觉质量上表现优异，论文坦诚地揭示了若干失败模式：

1. **对称对象的旋转问题（Figure 19）**：当对称对象（如圆柱体）绕其对称轴旋转时，运动偏移量计算无法区分旋转运动与平移运动，导致拉长中间帧产生自相交伪影。这是因为分离面/带方法基于质心或骨骼的全局运动方向，无法感知绕对称轴的纯旋转分量。论文提出的变通方案是将旋转分量手动转换为 UV 空间的纹理平移，这本质上是用纹理动画替代几何变形，但需要额外的手动干预。

2. **细长肢体的过度变形（Figure 13）**：如前所述，骨骼级别的运动偏移量计算对细长肢体（如手指）会产生不自然的过度拉伸，需要手动进行骨骼修剪。这一问题的根源在于归一化步骤使用骨骼范围内的最大值作为分母，当骨骼覆盖的顶点集较小时，归一化后的偏移量对离群顶点更为敏感。

![[assets/figures/papers/paper_list_l7_SMEAR_Stylized_Motion_Exaggeration_with_ARt_direction_motion20v2/figures/016_Figure_13.jpg]]
*Figure 13: Left: Elongated in-betweens generated with motion offsets computed considering the hands as single body parts instead of each finger independently, and with the stylization function*

3. **分离结构的几何依赖性**：运动偏移量计算依赖于对象结构的全局总结（简单对象的质心或关节角色的骨骼），对于非标准几何体（如具有复杂拓扑或缺乏明确骨骼结构的对象），可能需要手动调整分离结构。论文未提供针对非标准几何体的自动化适配方案。

4. **输入数据格式限制**：当前方法仅适用于关键帧动画输入，无法直接处理视频流或物理模拟数据。这是因为运动偏移量的计算需要已知的顶点轨迹，而视频和模拟数据通常缺乏这种显式的对应关系。

5. **实时性边界**：虽然预处理步骤（运动偏移量计算）极快，但风格化步骤（尤其是多重中间帧和运动线的生成）需要在每帧重新评估风格化函数并生成新几何体。对于顶点数极大的场景或复杂的风格化组合，完全实时的交互可能无法保证。论文未提供风格化步骤的详细性能数据，这一点需要手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l7_SMEAR_Stylized_Motion_Exaggeration_with_ARt_direction_motion20v2/figures/014_Figure_12.jpg]]
*Figure 12: Left: elongated in-between created with*

![[assets/figures/papers/paper_list_l7_SMEAR_Stylized_Motion_Exaggeration_with_ARt_direction_motion20v2/figures/023_Figure_11.jpg]]
*Figure 11: Elongated in-betweens created with different stylization functions for the middle frame of a character animation*

![[assets/figures/papers/paper_list_l7_SMEAR_Stylized_Motion_Exaggeration_with_ARt_direction_motion20v2/figures/002_Figure_2.jpg]]
*Figure 2: Example of smear frames in traditional 2D animation, “The Dover Boys at Pimento Academy”, directed by Charles M. Jones (public domain)*

![[assets/figures/papers/paper_list_l7_SMEAR_Stylized_Motion_Exaggeration_with_ARt_direction_motion20v2/figures/012_Figure_15.jpg]]
*Figure 15: Various stylization effects (c-e) of a sword slash motion using (a) motion offsets computed with a single bone to control the axis of separation, and (b) manually painted weights to control stylization intensity*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

现有3D动画管线中，涂抹帧（smear frames）的生成长期依赖手工绘制或基于物理模拟的后处理，难以在保持艺术交互性和动画工作流集成的同时，自动生成具有艺术控制性的效果——尤其是拉长中间帧（elongated in-betweens）。SMEAR的核心洞察在于：通过将运动偏移量定义为顶点到分离面（简单对象）或分离带（关节对象）的归一化符号距离，可以在不改变输入姿态和网格拓扑的前提下，对网格进行沿轨迹的变形，从而生成保留对象细节和可识别性的涂抹帧效果。

### 方法差异点与基线对比

SMEAR的方法分为两步：首先计算时空连贯的运动偏移量（motion offsets），然后通过风格化函数对这些偏移量进行艺术化处理。与已有方法的关键差异体现在以下维度：

**运动偏移量计算范式。** 早期方法如**Jones和Keyser**（2005）采用顶点法向与速度的点积作为局部运动指示器，但该方法对复杂几何体产生不一致的偏移量分布（Figure 4）。基于扫掠体积的方法如**Sellán等人**（2021）虽能生成全局一致的涂抹效果，但计算成本高昂（约7秒/帧），且扫掠体积会隐藏凹面和高频细节，输出网格与输入拓扑不同胚（Figure 9）。SMEAR的运动偏移量计算在计算效率上比扫掠体积快数个数量级（0.007秒/帧 vs 7秒/帧），同时保持输入网格的拓扑结构和表面细节。

**关节对象的分离结构。** 对于关节角色，SMEAR引入了基于骨骼的分离带（ribbon）概念，通过球面线性插值（SLERP）获得沿骨骼的局部运动方向，并引入共线权重 $w_{\mathrm{coll.}}(u) = 1 - (\hat{\mathbf{v}}(u) \cdot \hat{\mathbf{b}})^2$ 来抑制骨骼轴向运动导致的剪切伪影（Figure 7）。这一设计避免了简单对象分离平面方法在关节处的运动偏移量不连续问题（Figure 6）。

**风格化框架的可插拔性。** 与**Rohmer等人**（2021）的速度蒙皮（velocity skinning）方法相比，SMEAR借鉴了蒙皮权重混合机制（Equation 7: $\bar{\delta}_i = \sum_k w_{ik} \bar{\delta}_{ik}$），但将其用于运动偏移量的骨架级融合，而非直接的顶点变形。SMEAR的风格化函数（如 $S_E$, $S_E^{\mathrm{speed}}$, $S_M$, $S_L$）作为可插拔模块，艺术家可通过调整高层参数控制顶点领前/滞后程度，生成从简洁到复杂的多种运动夸张效果（Figure 11, 16）。

### 适用边界与局限

**对称旋转对象的自相交问题。** 当对象绕其旋转对称轴运动时，拉长中间帧会产生自相交伪影（Figure 19）。论文提出的变通方案是将旋转分量手动转换为UV空间的纹理平移，这需要艺术家介入，并非自动化解决方案。

**细长肢体的过度变形。** 将运动偏移量应用于所有骨骼层级时，手指等细长结构会产生不符合艺术预期的过度拉长。论文通过骨骼修剪将手视为单一身体部分来缓解此问题（Figure 13），但该操作同样依赖手动调整。

**运动分解的缺失。** 当前方法将对象的整体运动（平移、旋转等）统一编码为速度方向，无法自动分解运动变换分量。艺术家无法选择性地对特定运动成分（如仅对平移分量）进行风格化，这限制了精细艺术控制的可能性。

**输入格式限制。** 方法目前仅适用于关键帧动画输入，依赖预定义的骨骼结构和顶点轨迹，无法直接处理视频或物理模拟数据。

**实时性边界。** 虽然运动偏移量预处理效率极高（Table 1: 482顶点4ms/帧，14267顶点70ms/帧），但重新计算运动偏移量后需要重新评估风格化节点图，对于极复杂场景可能无法保证完全实时交互。

### 开放问题

1. **实时应用扩展。** 能否将该方法扩展用于视频游戏等实时场景中的动态涂抹帧生成？这需要在不预知未来帧的情况下在线计算运动偏移量。

2. **运动成分的自动分解。** 如何自动将运动分解为平移、旋转、缩放等分量，使艺术家能选择性对特定成分进行风格化？这涉及运动表示的重新设计。

3. **感知影响的定量评估。** 涂抹帧效果对运动感知（如速度感、方向感）和材质感知（如柔软度、重量感）的定量影响尚不明确。论文明确指出未来需要进行感知研究来量化这些效果。

4. **统一风格化流水线。** 能否将涂抹帧与其他运动夸张效果（如压缩-拉伸、预备-跟随）结合，形成统一的动画风格化流水线？这需要处理不同效果之间的协调与冲突。

5. **对称旋转的自动化处理。** 是否存在不依赖UV空间技巧的自动化方法，能够在不产生自相交的前提下处理对称旋转对象的运动风格化？这可能需要在运动偏移量计算中显式建模旋转分量。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/SMEAR_Stylized_Motion_Exaggeration_with_ARt_direction.pdf]]
