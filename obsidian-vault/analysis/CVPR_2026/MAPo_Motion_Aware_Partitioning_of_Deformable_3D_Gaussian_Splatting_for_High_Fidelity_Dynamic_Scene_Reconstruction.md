---
title: "MAPo: Motion-Aware Partitioning of Deformable 3D Gaussian Splatting for High-Fidelity Dynamic Scene Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MAPo_Motion_Aware_Partitioning_of_Deformable_3D_Gaussian_Splatting_for_High_Fidelity_Dynamic_Scene_Reconstruction.pdf
project_link: null
code_link: null
aliases:
- MAPo
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 动态分数引导的高动态3D高斯递归时间分割，使得不同时间段使用专用变形网络，打破统一表示的限制。
primary_logic: 通过计算每个3D高斯的历史最大位移和位置方差并融合为动态分数，自适应识别高动态高斯并将其沿时间轴递归分区，为每个子段配备独立的变形网络以精确建模复杂运动；同时将低动态高斯视为静态以减少计算开销；引入跨帧一致性损失消除分割边界的不连续性。
claims:
- 动态分数整合最大位移和位置方差，通过百分位归一化和调和平均形成最终分数，用于指导分区。
- 基于动态分数对高动态3D高斯进行递归时间分区，每个子段复制专属的变形网络以捕捉精细运动。
- 跨帧一致性损失有效抑制时间分割造成的视觉不连续性，同时提升渲染质量。
- MAPo在N3DV和Meet Room数据集上取得SOTA渲染质量，尤其在高度动态区域细节丰富。
---

# MAPo: Motion-Aware Partitioning of Deformable 3D Gaussian Splatting for High-Fidelity Dynamic Scene Reconstruction

> [!tip] 核心洞察
> 通过计算每个3D高斯的历史最大位移和位置方差并融合为动态分数，自适应识别高动态高斯并将其沿时间轴递归分区，为每个子段配备独立的变形网络以精确建模复杂运动；同时将低动态高斯视为静态以减少计算开销；引入跨帧一致性损失消除分割边界的不连续性。

| 字段 | 内容 |
|------|------|
| 中文题名 | MAPo：面向高保真动态场景重建的运动感知可变形3D高斯泼溅分区 |
| 英文题名 | MAPo: Motion-Aware Partitioning of Deformable 3D Gaussian Splatting for High-Fidelity Dynamic Scene Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2508.19786) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MAPo |
| Dataset | N3DV, Meet Room |

> [!tip] 效果简介
> - N3DV (flame salmon frag1) 上，PSNR 31.33 vs best of compared methods (see Table 1) (SOTA)；SSIM 0.944 vs see Table 1 (SOTA)；LPIPS 0.044 vs see Table 1 (SOTA)。
> - Meet Room (discussion) 上，PSNR 26.72 vs best of compared methods (see Table 2) (SOTA)；LPIPS 0.066 vs see Table 2 (SOTA)。

## 概述

动态场景的新视角合成在虚拟现实、增强现实等领域具有重要应用价值。近年来，基于3D高斯泼溅（3DGS）的方法因其高效渲染和高质量重建受到广泛关注。然而，现有基于变形的动态3DGS方法通常采用**单一统一模型**来表示所有时空变化，这导致在高度动态区域产生**时间平均效应**——模型倾向于学习一个折中的平均表示，使得快速运动区域的细节模糊、渲染质量下降（Figure 2）。

针对这一瓶颈，本文提出 **MAPo**（Motion-Aware Partitioning），一种运动感知的可变形3D高斯泼溅分区方法。其核心洞察是：不同运动强度的3D高斯应当由不同容量的变形网络来建模。MAPo通过计算每个3D高斯的历史位置最大位移与方差，融合为**动态分数**来量化运动强度；基于该分数，高动态高斯沿时间轴被**递归分区**，每个子段配备专属变形网络以精确捕捉精细运动；低动态高斯则被识别为静态，跳过变形网络计算以降低开销。同时，引入**跨帧一致性损失**消除分区边界处的视觉不连续性。

在N3DV和Meet Room数据集上的实验表明，MAPo在PSNR、SSIM和LPIPS指标上均取得SOTA渲染质量，尤其在复杂或快速运动区域细节保留显著优于现有方法（Figure 1）。渐进式消融验证了动态分数分区、静态识别和跨帧一致性损失各组件的有效性，其中静态分区在几乎不损失质量的前提下将存储从67MB降至48MB、训练时间从1h42m缩短至1h12m。

## 背景与动机

### 动态场景新视角合成：从静态到时空建模

新视角合成（Novel View Synthesis）的目标是从一组稀疏的输入视图重建场景并渲染出任意视角的逼真图像。近年来，以3D Gaussian Splatting（3DGS）为代表的显式辐射场方法凭借其高保真渲染质量和实时推理速度，在静态场景重建中取得了显著成功。然而，将3DGS扩展到动态场景面临根本性挑战：场景中的物体和区域随时间发生复杂运动，要求模型不仅捕捉空间结构，还需精确建模时空演变。

### 基于变形的动态3DGS范式及其瓶颈

当前主流的动态3DGS方法采用**基于变形的范式**：维护一组规范空间（canonical space）中的3D高斯，通过一个变形网络（deformation network）预测每个时间步的位移和旋转，将规范高斯变换到当前帧。代表性工作包括 **4DGaussians**（Wu et al., 2023）和 **E-D3DGS**（Bae et al., ECCV 2024）。

然而，这些方法存在一个根本性瓶颈：**所有时间段的所有3D高斯共享同一个变形网络**，形成统一的时空表示。这种设计在高度动态区域会产生**时间平均效应**——变形网络倾向于学习一个折中的平均表示，导致快速运动或复杂变形区域的细节被模糊化。如图2所示，直接渲染规范高斯得到的图像呈现出明显的平均化特征，某些区域（红色高亮）与平均表示存在显著视觉差异，这正是统一模型无法精细捕捉的时空细节。

### 核心动机：从统一表示到专业化时空分区

MAPo的核心动机源于一个关键观察：动态场景中不同区域的运动强度存在天然差异，且同一区域在不同时间段的运动模式也可能截然不同。用一个统一的变形网络去拟合所有时空变化，本质上是一种欠拟合——网络容量被低动态区域的简单运动所稀释，而高动态区域的精细运动则被平均化。

因此，MAPo提出**运动感知分区**策略：通过量化每颗3D高斯的历史运动强度，自适应识别高动态高斯，并沿时间轴将其递归分割为子段，为每个子段分配专属的变形子网络。这种设计使不同时间段能够学习专门化的运动表示，从根本上打破统一模型的表示瓶颈。同时，低动态高斯被识别为静态，跳过变形网络计算以提升效率。此外，引入跨帧一致性损失消除时间分区边界处的视觉跳跃，确保渲染序列的平滑过渡。

## 核心创新

MAPo的核心创新在于**用动态分数驱动的递归时间分区替代传统单一统一变形模型**，从根本上解决现有基于变形的动态3DGS方法在高度动态区域产生时间平均效应和模糊渲染的瓶颈问题。具体而言，MAPo通过三个关键的changed slots实现了突破：

### 1. 时空建模策略：从统一建模到专业化分区

现有变形方法（如**E-D3DGS**（Bae et al., ECCV 2024）、**4DGaussians**（Wu et al., 2023））采用单一变形网络统一处理所有时间段的所有3D高斯，这导致在复杂或快速运动区域，模型被迫学习一种“时间平均化”的表示（参见Figure 2），从而丢失精细的运动细节。

MAPo的解决方案是**基于动态分数对高动态3D高斯进行递归时间分区**。具体流程为：
- 在训练过程中，持续记录每个3D高斯的历史位置，计算其**最大位移** $r_i$ 和**位置方差** $v_i$（见公式(3)），并通过**百分位归一化**将其映射到[0,1]区间（见公式(4)）。
- 采用**调和平均**融合归一化后的位移和方差，得到最终的**动态分数** $S_i$（见公式(5)），该分数综合量化了每个3D高斯的运动强度和离散程度。
- 当某个3D高斯在第 $l$ 层的动态分数超过当前层阈值 $\tau_l$ 时，在时间中点 $t_{\text{mid}} = (t_{\text{start}} + t_{\text{end}})/2$ 处对其进行分割。同时，**父段的变形网络被复制**，为每个新的时间子段创建专属的变形子网络，实现专业化的时空建模。

这一策略的本质是**将高度动态的高斯从统一表示中“解放”出来**，为不同时间段分配专用的变形能力，从而精确捕捉复杂运动轨迹。Figure 4中的玩具示例直观验证了这一机制：用两个点加两个MLP拟合分段曲线（图4c）相比单点单MLP拟合整条曲线（图4b），显著降低了拟合误差。

### 2. 静态区域处理：动态分数引导的计算优化

传统方法中，所有3D高斯均需通过变形网络计算，即使场景中存在大量静态或低动态区域。MAPo利用动态分数机制，将**动态分数低于预定义阈值 $\tau_{\text{static}}$ 的3D高斯识别为静态**。这些静态高斯在训练早期完成变形后，其属性被直接更新，**后续渲染过程中跳过所有变形网络计算**。

这一设计的双重收益在消融实验中得到充分验证（Table 3）：
- **计算效率大幅提升**：存储从67MB降至48MB，训练时间从1h42m缩短至1h12m，FPS从54.56提升至92.59。
- **渲染质量几乎无损**：PSNR仅从26.63微降至26.60，说明动态分数的判别能力足够精准，不会误伤需要建模的动态区域。

### 3. 时序平滑约束：跨帧一致性损失

递归时间分区虽然带来了专业化建模的优势，但不可避免地引入了**分区边界处的视觉不连续性**——相邻时间段由不同的变形网络处理，可能导致渲染结果的突然跳变。现有方法缺乏针对这一问题的专门约束。

MAPo设计了**跨帧一致性损失** $L_{\text{cross}}$，包含两个互补的约束：
- **当前一致性损失** $L_{\text{current}} = \| I_t(G_t, V) - I_t(G_{t'}, V) \|_1$：强制同一帧在不同时间段模型下的渲染结果尽可能一致，直接抑制边界区域的不连续性。
- **真值一致性损失** $L_{\text{gt}} = \| I_t(G_{t'}, V) - I^{\text{GT}} \|_1$：使相邻时间段的渲染结果逼近当前帧的真值，防止一致性约束导致整体偏离真实外观。
- 最终损失为 $L_{\text{cross}} = 0.5 \cdot L_{\text{current}} + L_{\text{gt}}$，且**仅对分区边界附近5帧以内的训练视角施加**，避免不必要的计算开销。

消融实验（Table 3, Figure 8, Figure 9）系统验证了 $L_{\text{cross}}$ 各组件的作用：逐步添加 $L_{\text{current}}$ 和 $L_{\text{gt}}$ 后，分区边界的时序光流误差（tOF Bnd）持续下降，最终低于无分区的基线水平，且连续帧过渡最为平滑。Figure 4d的玩具示例也佐证了这一点：在分区边界处施加一致性约束后，两个MLP的拟合结果在边界处实现了无缝衔接。

### 创新总结

MAPo的三个changed slots形成了完整的创新链条：**动态分数**提供了量化运动强度的可计算指标，**递归时间分区**基于该指标实现了时空建模的专业化，**跨帧一致性损失**则消除了专业化带来的边界副作用。三者协同，使得MAPo在N3DV和Meet Room数据集上均取得SOTA渲染质量，尤其在高度动态区域展现出显著优于现有方法的细节保留能力。

## 整体框架

MAPo 的整体 pipeline 围绕一个核心矛盾展开：**单一统一变形模型在高度动态区域会产生时间平均效应，导致模糊渲染**。为解决这一问题，MAPo 引入了一套基于“动态分数”的自适应时空分区机制，将不同运动强度的 3D 高斯分配到不同粒度的时空表示中，实现专业化建模。

### 核心流程

MAPo 的输入为多视角视频帧序列，输出为对应视角的渲染图像。其 pipeline 由以下关键模块串联而成：

1.  **动态分数计算**：在训练过程中，持续记录每个 3D 高斯的历史位置。基于这些历史位置，计算两项统计量——**最大位移** $r_i$ 和**位置方差** $v_i$，分别量化该高斯的运动幅度和运动离散程度。随后，通过百分位归一化将两者映射到 $[0,1]$ 区间，再以调和平均融合为最终的**动态分数** $S_i$：
    $$S_i = \frac{2}{\frac{1}{\tilde{r}_i + \varepsilon} + \frac{1}{\tilde{v}_i + \varepsilon}}$$
    该分数是后续所有分区决策的核心依据。

2.  **基于动态分数的时间分区**：根据动态分数的高低，3D 高斯被分为两类处理：
    -   **高动态 3D 高斯**（分数超过当前层级阈值 $\tau_l$）：沿时间维度进行**递归中点切分**。具体而言，当某个高斯在层级 $l$ 的动态分数超过阈值时，其所在的时间段在 $t_{\text{mid}} = (t_{\text{start}} + t_{\text{end}}) / 2$ 处被一分为二，该高斯本身被复制，同时其变形网络也被复制，为每个子段创建专属的子变形网络。这一递归过程持续进行，直至达到预设的最大分区级别，使得高动态区域获得更细粒度的时空建模能力。
    -   **低动态 3D 高斯**（分数低于静态阈值 $\tau_{\text{static}}$）：被识别为**静态高斯**。它们在完成一次变形后，其属性被直接更新，并在后续渲染中**跳过变形网络的计算**，从而显著降低计算开销和存储占用。

3.  **跨帧一致性损失**：时间分区不可避免地会在分区边界引入视觉不连续性。为此，MAPo 设计了**跨帧一致性损失** $L_{\text{cross}}$，它由两项构成：
    -   **当前一致性损失** $L_{\text{current}}$：最小化同一时刻 $t$ 的渲染结果在相邻两个时间分区模型下的差异。
    -   **真值一致性损失** $L_{\text{gt}}$：强制相邻时间段的模型对当前时刻的渲染结果逼近真实图像。
    $$L_{\text{cross}} = 0.5 \cdot L_{\text{current}} + L_{\text{gt}}$$
    该损失仅在分区边界附近的训练视图上计算，有效消除了视觉跳跃并提升了边界处的渲染质量。

4.  **可微渲染**：最终，所有处理后的动态和静态 3D 高斯被投影到像平面，通过标准的 alpha 混合合成最终的渲染图像。

### 数据流与模块关系

整个框架的数据流可以概括为：**历史位置 → 动态分数 → 分区决策 → 专业化变形 → 一致性约束 → 渲染输出**。

各模块间的因果关系清晰：动态分数是分区决策的**唯一量化依据**；时间分区通过复制变形网络，为不同时间段提供了**独立的建模容量**；静态分区则通过冻结低动态高斯，在**不损害渲染质量的前提下**大幅压缩了计算和存储开销；跨帧一致性损失作为分区策略的**必要补充**，消除了分区带来的副作用，使得自适应分区策略在提升细节的同时保证了时序平滑性。

### 补充图表

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2508_19786/figures/003_Figure_3.jpg]]
*Figure 3: An overview of MAPo. (a) 3DGs’ deformation process. (b) Compute the dynamic score of 3DGs from history positions during training. (c) High-dynamic 3DGs are recursively temporally partitioned, and low-dynamic ones are deformed and treated as static. (d) Dynamic and static 3DGs are combined for rendering. Losses are computed on the left*

## 核心模块与公式推导

### 动态分数计算

MAPo 的核心创新在于通过**动态分数**（Dynamic Score）量化每个 3D 高斯的运动强度，从而指导后续的自适应时间分区。该分数基于训练过程中记录的每个 3D 高斯的历史位置计算，融合了两个互补的运动指标：

**最大位移** $r_i$ 衡量高斯中心在时间窗口内的最大空间跨度：

$$r_i = \left\| \max_j \mu_{ij} - \min_j \mu_{ij} \right\|$$

**位置方差** $v_i$ 衡量高斯中心在时间窗口内的离散程度：

$$v_i = \sum_{j=1}^{m} \frac{\| \mu_{ij} - \bar{\mu}_i \|^2}{m}$$

其中 $\mu_{ij}$ 表示第 $i$ 个 3D 高斯在第 $j$ 个时间步的位置，$\bar{\mu}_i$ 为其时间平均位置，$m$ 为记录的历史帧数。

由于最大位移和位置方差的数值尺度不同，MAPo 采用**百分位归一化**将其映射到 $[0,1]$ 区间：

$$\tilde{r}_i = \sum_{k=1}^{100} \frac{\mathbf{1}(r_i \geq q_r(k))}{100}, \quad \tilde{v}_i = \sum_{k=1}^{100} \frac{\mathbf{1}(v_i \geq q_v(k))}{100}$$

其中 $q_r(k)$ 和 $q_v(k)$ 分别表示所有高斯在最大位移和方差上的第 $k$ 个百分位数。最后通过**调和平均**融合两个归一化指标，得到动态分数 $S_i$：

$$S_i = \frac{2}{\frac{1}{\tilde{r}_i + \varepsilon} + \frac{1}{\tilde{v}_i + \varepsilon}}, \quad \varepsilon = 10^{-6}$$

调和平均的选择使得只有当高斯的位移和方差同时较高时，动态分数才会显著偏高，从而更准确地识别真正的高动态高斯。

### 递归时间分区

基于动态分数，MAPo 对高动态 3D 高斯执行**递归时间分区**。其核心机制是：当第 $l$ 层的某个 3D 高斯的动态分数超过当前层阈值 $\tau_l$ 时，将其在时间中点 $t_{\text{mid}} = (t_{\text{start}} + t_{\text{end}}) / 2$ 处切分为两个子段。同时，父段的变形网络被复制，为每个新的时间子段创建专属的变形子网络，实现专业化的时空建模。

递归过程持续进行，直到达到预设的最大分区级别或所有高斯的动态分数均低于对应层阈值。这一策略打破了现有方法中单一变形网络统一处理所有时间段的限制，使得不同时间段的高动态区域能够拥有独立的变形参数，从而精确捕捉复杂运动细节。

### 静态高斯识别与处理

与高动态高斯的分区策略互补，MAPo 将动态分数低于预定义阈值 $\tau_{\text{static}}$ 的 3D 高斯识别为**静态**。这些静态高斯在初始变形后直接冻结其属性，后续渲染过程中跳过变形网络计算。这一设计在不损害渲染质量的前提下，显著降低了存储开销和训练时间。

### 跨帧一致性损失

递归时间分区虽然提升了高度动态区域的建模精度，但在分区边界处可能引入视觉不连续性。为此，MAPo 设计了**跨帧一致性损失** $L_{\text{cross}}$，包含两个约束项：

**当前一致性损失** $L_{\text{current}}$ 强制同一帧在不同时间分区模型下的渲染结果保持一致：

$$L_{\text{current}} = \left\| I_t(G_t, V) - I_t(G_{t'}, V) \right\|_1$$

其中 $I_t(G_t, V)$ 表示当前时刻 $t$ 所属分区模型的渲染结果，$I_t(G_{t'}, V)$ 表示相邻分区模型对同一时刻的渲染结果。

**真值一致性损失** $L_{\text{gt}}$ 使相邻时间段的渲染结果逼近当前帧的真值 $I^{\text{GT}}$：

$$L_{\text{gt}} = \left\| I_t(G_{t'}, V) - I^{\text{GT}} \right\|_1$$

最终跨帧一致性损失为两者的加权组合：

$$L_{\text{cross}} = 0.5 \cdot L_{\text{current}} + L_{\text{gt}}$$

该损失仅在训练视图中帧索引距离任意分区边界 5 帧以内的视图上施加，以集中消除边界处的不连续性。消融实验（Table 3）表明，逐步添加 $L_{\text{current}}$ 和 $L_{\text{gt}}$ 后，分区边界处的时序光流误差 tOF 明显下降，最终低于基线，且连续帧过渡最平滑（Figure 9）。

### 补充图表

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2508_19786/figures/004_Figure_4.jpg]]
*Figure 4: Effectiveness of temporal partitioning strategy and consistency loss on a toy example. (a) A 3D curve p(t) simulates a dynamic trajectory. (b) A single point and a single MLP to fit*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2508_19786/figures/002_Figure_2.jpg]]
*Figure 2: Rendering results of a single unified model. (a) shows the temporally averaged representation, which is visualized by directly rendering the canonical 3DGs. The regions highlighted in blue in (b) and (c) are visually close to this average. The region highlighted in red in (c) is visually distant from this average*

## 实验与分析

### 核心瓶颈的实证验证

MAPo的动机源于一个关键观察：基于单一统一变形网络的动态3DGS方法在高度动态区域会产生**时间平均效应**，导致渲染模糊。Figure 2通过可视化典型帧的渲染结果验证了这一瓶颈——直接渲染规范空间3D高斯得到的图像（Figure 2a）代表了模型学到的“时间平均表示”，而两帧实际渲染中，蓝色高亮区域在视觉上接近该平均值，红色高亮区域则远离平均值。这意味着统一模型无法同时精确表达偏离平均值的运动状态，本质上是将精细运动细节“平均掉”了。

### 主实验结果

#### N3DV数据集

Table 1报告了N3DV数据集上的定量对比。以*flame salmon frag1*场景为例，MAPo在全部三个指标上取得最优：

- **PSNR**：31.33，超越所有对比方法
- **SSIM**：0.944
- **LPIPS**：0.044

对比方法包括基于变形的**E-D3DGS**（Bae et al., ECCV 2024）、**4DGaussians**（Wu et al., 2023）以及高效动态场景方法**Swift4D**（Wu et al., 2025）。值得注意的是，E-D3DGS是MAPo的变形场基础架构，MAPo在其之上通过动态分数引导的分区策略实现了显著的渲染质量提升。

#### Meet Room数据集

Table 2展示了Meet Room数据集上的结果。以*discussion*场景为例：

- **PSNR**：26.72，领先所有对比方法
- **LPIPS**：0.066

Figure 5提供了两个数据集上的定性对比，MAPo在细节保留上明显优于SOTA方法，尤其在运动复杂的区域。

### 消融实验

#### 渐进式组件消融

Table 3在Meet Room数据集上通过渐进添加各组件，系统验证了每个设计的贡献：

**动态分区策略（+Var vs +Max Dis）**：仅使用最大位移（+Max Dis）进行分区相比基线已有提升，但融合位置方差后的综合动态分数（+Var）获得了更高的渲染质量，验证了调和平均融合位移和方差的必要性。Figure 6在Vrheadset场景上可视化了这一差异，+Var能更准确地识别和分区高动态高斯。

**静态分区（+Static）**：在+Var基础上引入静态分区后，**存储从67MB降至48MB**，**训练时间从1h42m缩短至1h12m**，而PSNR仅从26.63微降至26.60，几乎无损。Figure 7在Salmon场景上展示了静态分区的渲染结果与真值的对比，确认静态高斯的分区不损害渲染质量。

**跨帧一致性损失（+L_current → +L_gt）**：逐步添加$L_{\mathrm{current}}$和$L_{\mathrm{gt}}$后，分割边界处的时序光流误差tOF持续下降，最终低于基线。Figure 8通过时间拼接图像直观展示了$L_{\mathrm{cross}}$消除视觉不连续性的效果。Figure 9在分割边界（第74-75帧）附近展示了连续帧序列，完整的$L_{\mathrm{cross}}$提供了最平滑的过渡和最优的细节保留。

#### 分区级别消融

Table 4在*flame salmon frag3*上研究了最大分区级别的影响。当级别从0增至5时，PSNR逐渐提升，但**在级别3之后质量增益递减**，而存储和训练时间几乎线性增加。因此主实验选用级别3作为质量与开销的最佳平衡点。

### 补充图表

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2508_19786/figures/006_Table.jpg]]

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2508_19786/figures/008_Table_2.jpg]]
*Table 2: Quantitative comparison on the Meet Room dataset. Storage, training time, and FPS are calculated on discussion*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2508_19786/figures/007_Table_3.jpg]]
*Table 3: Progressive component ablation on Meet Room. Storage, training time, and FPS are calculated on discussion*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2508_19786/figures/012_Table_4.jpg]]
*Table 4: Ablation study on the partition level parameter. All experiments are conducted on the flame salmon frag3*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2508_19786/figures/009_Figure_6.jpg]]
*Figure 6: Observation of dynamic partition on Vrheadset*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2508_19786/figures/010_Figure_7.jpg]]
*Figure 7: Observation of static partition on Salmon*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2508_19786/figures/013_Figure_8.jpg]]
*Figure 8: Observation of*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2508_19786/figures/014_Figure_9.jpg]]
*Figure 9: Ablation study on the*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2508_19786/figures/001_Figure.jpg]]
*Figure: (d) Ground Truth ure 1: Overview. (a-b) Existing deformation-based methods often result in blurriness in areas with intense motion, and evFigure 1. Overview. (a-b) Deformation-based methods often blur details in regions with complex or rapid motion. (c) Our MAPo hancing the capabilities of the deformation fields does not leadsignificantly improves rendering quality in these areas. (d) Ground Truth*

## 方法谱系与知识库定位

### 1. 方法谱系：在动态3DGS中的定位

MAPo 的核心创新在于对**基于变形的动态3DGS**（Deformation-based Dynamic 3DGS）框架的时空建模策略进行了根本性重构。其直接对话的基线工作构成了清晰的方法谱系：

- **E-D3DGS** (Bae et al., ECCV 2024)：作为 MAPo 的变形场基础架构和核心对比方法，E-D3DGS 采用单一统一的变形网络处理所有时间段的所有3D高斯。这是 MAPo 直接改进的对象——MAPo 保留了其变形场的基本范式，但将“统一处理”替换为“动态分数引导的递归分区与专业化建模”。

- **4DGaussians** (Wu et al., 2023)：同样是基于变形的动态3DGS方法，面临与 E-D3DGS 相同的时间平均效应问题。在图1的定性对比中，4DGaussians 在高度动态区域产生明显模糊，这构成了 MAPo 要解决的核心瓶颈。

- **Swift4D** (Wu et al., 2025)：作为高效动态场景重建的代表方法，MAPo 与之在渲染质量和计算开销两个维度上进行了对比。

MAPo 的方法论突破可概括为：**从“统一时空建模”到“运动感知的分治时空建模”**。这一转变通过三个关键槽位的变化实现：

| 建模维度 | 基线方法（E-D3DGS等） | MAPo 方法 |
|---------|---------------------|-----------|
| 时空建模策略 | 单一变形网络统一处理所有时间段 | 基于动态分数递归分区，为高动态高斯分配专属变形网络 |
| 静态区域处理 | 所有高斯均通过变形网络计算 | 低动态高斯识别为静态，跳过变形网络运算 |
| 时序平滑约束 | 无额外时序一致性损失 | 跨帧一致性损失 $L_{\mathrm{cross}}$ 消除分区边界不连续性 |

### 2. 核心因果机制

MAPo 的性能提升源于一条清晰的因果链：

**瓶颈识别** → 统一变形模型在高度动态区域产生时间平均效应，导致渲染模糊（Figure 2 提供了直接证据：规范空间渲染呈现时间平均表示，偏离该平均的区域恰好是运动剧烈区域）。

**因果调节变量** → 动态分数 $S_i$ 作为量化运动强度的可计算指标，通过调和平均融合最大位移 $r_i$ 和位置方差 $v_i$：
$$S_i = \frac{2}{\frac{1}{\tilde{r}_i + \varepsilon} + \frac{1}{\tilde{v}_i + \varepsilon}}$$

**干预机制** → 基于 $S_i$ 的自适应递归分区：当某高斯在层级 $l$ 的动态分数超过阈值 $\tau_l$ 时，在时间中点 $t_{\mathrm{mid}}$ 进行分割，并为子段复制专属变形网络。这使得不同时间段的复杂运动由专用网络分别建模，打破了统一表示的限制。

**效果验证** → 消融实验（Table 3）证实：仅添加动态分区（+Var）相比基线已在 Meet Room 上带来显著质量提升；进一步添加静态分区（+Static）将存储从 67MB 降至 48MB、训练时间从 1h42m 降至 1h12m，而 PSNR 几乎不变（26.60 vs 26.63）；完整的跨帧一致性损失（+$L_{\mathrm{cross}}$）在分区边界处将时序光流误差 tOF 降至最低。

### 3. 适用边界与局限

基于已分析证据，MAPo 的适用边界可从以下维度界定：

**运动类型适配性**：动态分数基于历史位置的最大位移和方差，这意味着该方法天然适用于具有明确空间位移的动态场景（如人体动作、物体运动）。对于以非刚性形变为主、位移幅度小但拓扑变化复杂的场景（如流体、烟雾），位移-方差指标可能无法充分捕捉其动态特性，需要进一步验证。

**分区粒度的收益递减**：Table 4 的消融显示，最大分区级别从 0 增至 5 时 PSNR 逐渐提升，但在级别 3 后质量增益递减，而存储和训练时间几乎线性增加。这表明递归分区的边际收益存在上限，过深的分区树可能引入冗余的变形网络副本。

**跨帧一致性损失的适用范围**：该损失仅在分区边界附近 5 帧范围内的训练视图上施加（见实验部分），这意味着其有效性依赖于分区边界附近的密集观测。对于帧间运动极大或视角稀疏的场景，该约束的强度可能需要调整。

**计算开销的权衡**：虽然静态分区显著降低了开销，但动态分区本身引入了额外的变形网络副本。在极端情况下（所有高斯均为高动态且分区深度大），存储和计算开销可能超过统一模型。Table 3 中 +Var 的存储（67MB）和训练时间（1h42m）均高于基线（40MB, 1h22m），表明纯动态分区是以计算换质量。

### 4. 开放问题

以下问题在当前证据中未被充分探讨，值得后续工作关注：

1. **动态分数阈值的自适应设定**：当前 $\tau_l$ 和 $\tau_{\mathrm{static}}$ 的设定机制在已有材料中未详细说明。这些阈值如何在不同场景间泛化，是否依赖手动调参，是实际部署中的关键问题。

2. **分区策略的在线性**：动态分数的计算依赖历史位置记录，这意味着分区决策需要一定的预热期。该方法是否支持在线/流式场景，即在新帧到达时动态调整分区结构，尚不明确。

3. **与其他动态场景表示的结合**：MAPo 的分治思想是否可推广到其他动态表示（如 4D 高斯、HexPlane 等），以及动态分数机制是否可与其他运动分解方法（如刚体-非刚体分离）协同工作，是值得探索的方向。

4. **长序列的可扩展性**：递归分区树的深度随序列长度增长，当前实验在 N3DV（约 50-90 帧）和 Meet Room 上进行。对于分钟级或更长序列，分区树的管理、存储和训练效率需要进一步研究。

5. **多对象场景的语义分区**：当前动态分数是逐高斯的底层运动指标，未涉及语义信息。在包含多个独立运动对象的场景中，是否可结合语义或实例分割进行更结构化的分区，可能进一步提升专业化建模的效果。

## 原文 PDF

![[paperPDFs/CVPR_2026/MAPo_Motion_Aware_Partitioning_of_Deformable_3D_Gaussian_Splatting_for_High_Fidelity_Dynamic_Scene_Reconstruction.pdf]]