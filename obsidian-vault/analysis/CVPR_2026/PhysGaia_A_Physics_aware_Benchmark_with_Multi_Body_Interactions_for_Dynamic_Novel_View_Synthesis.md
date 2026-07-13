---
title: "PhysGaia: A Physics-aware Benchmark with Multi-Body Interactions for Dynamic Novel View Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PhysGaia_A_Physics_aware_Benchmark_with_Multi_Body_Interactions_for_Dynamic_Novel_View_Synthesis.pdf
project_link: "https://cv.snu.ac.kr/research/PhysGaia/"
code_link: "https://github.com/nvidia/warp"
aliases:
- PB
- PhysGaia
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 提供基于材料特定物理求解器（FLIP、Pyro、Vellum、MPM）生成的精确三维粒子轨迹和物理参数（如粘度、杨氏模量等），使得物理真实性的定量评估成为可能。
primary_logic: 通过构建真实物理模拟驱动的多体交互场景，将基准从单一的光度真实推进到物理一致性，暴露现有方法在复杂动态下的根本缺陷。
claims:
- PhysGaia 提供了完整的地面真实物理信息，包括三维粒子轨迹和物理参数，支持物理真实性的量化评估。
- 现有DyNVS方法在PhysGaia上表现显著下降，尤其在高动态场景中，表明其物理真实性的根本性不足。
- PhysGaia在运动复杂度和真实感方面均显著优于现有物理基准，动态得分最高，FID和KID最低。
- Cow (Rheological) 上 TD (Trajectory Distance) = 0.03 (Ground Truth)
---

# PhysGaia: A Physics-aware Benchmark with Multi-Body Interactions for Dynamic Novel View Synthesis

> [!tip] 核心洞察
> 通过构建真实物理模拟驱动的多体交互场景，将基准从单一的光度真实推进到物理一致性，暴露现有方法在复杂动态下的根本缺陷。

| 字段 | 内容 |
|------|------|
| 中文题名 | PhysGaia: 面向动态新视角合成的物理感知多体交互基准 |
| 英文题名 | PhysGaia: A Physics-aware Benchmark with Multi-Body Interactions for Dynamic Novel View Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2506.02794) · [Project](https://cv.snu.ac.kr/research/PhysGaia/) · [Code](https://github.com/nvidia/warp) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | PhysGaia Benchmark |
| Dataset | Cow, Box-smoke, All scenes |

> [!tip] 效果简介
> - Cow (Rheological) 上，TD (Trajectory Distance) 0.03 (Ground Truth) vs 0.07 (D-3DGS ) (-0.04)。
> - Box-smoke (Gas) 上，TD 0.84 (Ground Truth) vs 4.01 (D-3DGS ) (-3.17)；AUOP (Area Under Outlier Percentage) 0.3 (Ground Truth) vs 37.9 (D-3DGS ) (-37.6)。
> - All scenes (Monocular) 上，PSNR (db) N/A (Benchmark) vs 21.7 (D-3DGS), 22.7 (4DGS) (—)。

## 概要

动态新视角合成（DyNVS）领域近年来在光度重建质量上取得了显著进展，但现有基准几乎完全忽略了场景的**物理一致性**——即重建结果是否遵循真实的物理运动规律。这一缺失的根源在于，当前数据集仅提供多视角RGB图像，缺乏用于评估物理真实性的地面真实物理信息（如三维轨迹和物理参数），导致对方法的评价停留在视觉层面，无法诊断其在复杂动态场景下的根本性缺陷。

**PhysGaia** 是一个面向DyNVS的物理感知基准，其核心贡献在于：通过材料特定的物理求解器（FLIP、Pyro、Vellum、MPM）生成涵盖液体、气体、纺织品和流变物质四类材料的复杂多体交互场景，并首次提供完整的**三维粒子轨迹**和**物理参数**（如粘度、杨氏模量、泊松比）作为地面真值。这使得对重建方法的物理真实性进行定量评估成为可能，将基准从单一的光度真实推进到物理一致性维度。

实验揭示了一个关键发现：现有DyNVS方法在PhysGaia上表现显著下降，尤其在高动态场景（如气体扩散、流变物质碰撞）中，其物理真实性存在根本性不足。以**D-3DGS**为代表的3D高斯泼溅方法在box-smoke（气体）场景上的轨迹距离（TD）高达4.01，而地面真值仅为0.84；离群百分比（AUOP）达到37.9%，表明重建轨迹严重偏离真实物理流。在逆物理参数估计任务中，现有方法（PAC-NeRF、GIC）显著低估杨氏模量，因其设计仅针对单一物体场景，无法处理多体交互。

PhysGaia在运动复杂度和视觉真实感方面均显著优于现有物理基准：动态得分0.444（最高），FID 207.8（最低），KID 0.118（最低），为动态场景重建领域提供了更具挑战性和诊断力的评估平台。

### 动态新视角合成的现状与瓶颈

动态新视角合成（Dynamic Novel View Synthesis, DyNVS）旨在从一组稀疏的输入视图重建任意时刻、任意视角下的动态场景。近年来，以NeRF和3D高斯泼溅（3DGS）为代表的神经渲染方法在该领域取得了显著进展，在多个基准数据集上展现出令人印象深刻的光度真实感。然而，现有评估体系存在一个根本性瓶颈：**它们仅关注渲染图像的光度质量（如PSNR、SSIM、LPIPS），却完全忽略了动态场景的物理一致性**。这意味着，一个在视觉上看似逼真的重建结果，其底层运动可能严重违背物理定律——例如物体穿透、流体不守恒、形变不符合材料本构关系等。

这一瓶颈的根源在于现有DyNVS基准的数据构造方式。当前主流基准（如D-NeRF、HyperNeRF、NeRF-DS）的场景主要依赖人工设计动作或真实世界拍摄，缺乏对物理过程的精确建模。这些数据集不提供地面真实的物理信息（如三维粒子轨迹、材料物理参数），使得物理真实性的定量评估成为不可能。

### 现有物理相关基准的局限

少数工作尝试将物理模拟引入动态场景数据集，如ScalarFlow（烟雾）、PAC-NeRF（单一弹性体）和Spring-Gaus（弹簧-质量系统）。然而，这些数据集存在三个关键局限：

1. **材料覆盖狭窄**：每个数据集仅涉及单一材料类型（气体、弹性固体或简单质点系统），无法覆盖自然界中多样化的物质形态。
2. **动力学过度简化**：场景通常只包含单个物体或极简的交互，缺乏真实世界中普遍存在的多体、多材料耦合交互。
3. **物理真值缺失**：现有数据集不提供物理参数（如粘度、杨氏模量）和完整的三维运动轨迹，使得物理一致性的量化评估难以开展。

**Figure 4** 直观展示了这些局限性：ScalarFlow仅处理烟雾上升的简单场景，PAC-NeRF局限于单个弹性体变形，Spring-Gaus则停留在弹簧-质点系统的层面。这些数据集远不足以支撑对动态场景重建方法物理真实性的系统评估。

### PhysGaia的动机与核心洞察

上述分析揭示了一个明确的缺口：**DyNVS领域亟需一个同时具备丰富多体交互和完整物理真值的基准，以实现从“光度真实”到“物理一致”的评估范式跃迁**。

PhysGaia的核心洞察在于：通过构建由真实物理模拟驱动的多体交互场景，可以将基准从单一的光度真实推进到物理一致性层面。具体而言，PhysGaia利用材料特定的物理求解器（FLIP用于液体、Pyro用于气体、Vellum用于纺织品、MPM用于流变物质）生成严格遵循物理定律的动态场景，并同时输出完整的地面真实信息——包括三维粒子轨迹和物理参数（如粘度、杨氏模量、泊松比、气体温度等）。这使得研究者首次能够定量评估重建方法在物理运动层面的保真度，而非仅停留在视觉质量层面。

### 方法谱系与知识库定位

PhysGaia作为基准工作，其定位在于为现有DyNVS方法提供统一的物理真实性评估平台。在方法谱系中，被评估的基线方法包括：

- **基于3DGS的动态重建**：**D-3DGS**（Luiten et al.）、**4DGS**（Wu et al., CVPR 2024）采用HexPlane变形场建模4D高斯泼溅；**STG**（Li et al.）使用多项式运动模型驱动高斯原语。
- **基于NeRF的动态重建**：**MoSca**（Lei et al., NeurIPS 2023）通过运动模态分解实现单目动态重建；**SoM**（Wang et al., CVPR 2024）结合ARAP约束和深度估计。
- **逆物理参数估计**：**PAC-NeRF**（Li et al., NeurIPS 2022）和**GIC**（Zhang et al., ECCV 2024）尝试从视觉观测中反推物理参数。

PhysGaia的独特贡献在于填补了评估体系中的“物理真值”空缺。与上述方法侧重于重建算法本身不同，PhysGaia提供了物理模拟器生成的精确三维轨迹和材料参数，使得对物理一致性的定量诊断成为可能。这一基准不仅暴露了现有方法在复杂多体交互场景下的根本性缺陷，也为未来物理感知的动态重建方法指明了方向。

## 核心方法与创新机理

PhysGaia 的核心创新在于将动态新视角合成（DyNVS）的评估范式从**单一的光度真实推进到物理一致性**。这一转变通过以下三个相互关联的关键改进实现。

### 1. 完整的物理真值信息

现有 DyNVS 基准（如 D-NeRF、HyperNeRF、iPhone 等）仅提供 RGB 图像作为监督信号，完全缺乏用于评估物理真实性的地面真实物理信息。PhysGaia 首次为每个场景提供了**精确的三维粒子轨迹和物理参数**，包括液体的粘度、流变物质的杨氏模量与泊松比、气体场景的温度等（Section 3.1）。这使得定量评估重建结果的物理一致性成为可能——不仅是“看起来像不像”，更是“动得对不对”。

### 2. 多体、多材料交互场景

现有物理模拟数据集（如 ScalarFlow、PAC-NeRF、Spring-Gaus）存在三个根本局限：材料覆盖范围窄、动力学过度简化、缺乏丰富的多体交互（Figure 4）。PhysGaia 通过**材料特定的物理求解器**突破了这些限制——FLIP 用于液体、Pyro 用于气体、Vellum 用于纺织品、MPM 用于流变物质——构建了包含复杂多体碰撞、飞溅、非局部刚体运动等丰富物理现象的 12 个场景（Figure 2, Table 1-2）。与仅关注单一物体或单一材料的现有基准相比，PhysGaia 的场景涉及多个不同材料物体之间的真实物理交互，这暴露了现有方法在复杂动态下的根本性缺陷。

### 3. 物理真实性度量体系

为量化物理一致性，PhysGaia 引入了两个专用度量指标：**轨迹距离（TD）** 和**离群百分比下面积（AUOP）**。TD 衡量重建高斯原语与最近地面真实轨迹之间的平均欧氏距离，直接度量运动重建的物理保真度；AUOP 则通过累积时序上的离群点比例，捕捉整个序列中的异常行为（Section 4）。这一度量体系填补了现有 PSNR/SSIM/LPIPS 仅评估光度质量而无法反映物理运动一致性的空白。

**核心因果链条**：物理求解器提供精确真值 → 多体多材料场景暴露方法缺陷 → 专用物理度量实现定量评估。这一链条使 PhysGaia 成为一个“压力测试”基准：现有方法在 PhysGaia 上的表现显著下降（Table 4, Table E），尤其在高动态的气体和流变物质场景中，揭示了其物理真实性的根本不足。

PhysGaia 构建了一套以物理模拟器为核心、路径追踪渲染器为桥梁、多模态真值生成为输出的完整数据流水线，其设计目标是为动态新视角合成（DyNVS）任务提供兼具光度真实与物理真实的多体交互基准。

### 流水线总览

整个流水线由三个核心阶段串联而成：

1. **物理模拟阶段**：根据目标材料类型，调用专用物理求解器生成包含精确三维粒子轨迹和物理参数的地面真值。
2. **渲染阶段**：将模拟输出的粒子/网格状态通过路径追踪渲染器转化为多视角 RGB 图像及辅助模态。
3. **评估与下游适配阶段**：利用提供的物理真值（轨迹、参数）和光度真值（多视角图像），对 DyNVS 方法进行光度真实性和物理真实性双维度评估；同时，用户可通过仿真节点图定制输出模态以适应特定下游任务。

### 物理模拟阶段：材料特定求解器

PhysGaia 的核心创新在于针对不同材料类型选用最适合的物理求解器，而非使用单一通用引擎。这一设计保证了模拟的物理准确性，并使得多体、多材料交互场景成为可能。具体求解器分工如下：

- **FLIP 求解器**（Fluid-Implicit Particle）用于液体材料，基于不可压缩 Navier-Stokes 方程模拟溅射、融合等复杂流体行为。其动量方程形式为：
  
  $$\rho \left( \frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla) \mathbf{u} \right) = -\nabla p + \mu \nabla^2 \mathbf{u} + \rho \mathbf{g}$$

  其中 $\rho$ 为密度，$\mathbf{u}$ 为速度场，$p$ 为压力，$\mu$ 为动力粘度，$\mathbf{g}$ 为重力加速度。

- **Pyro 求解器**用于气体（烟雾）材料，模拟浮力驱动和非线性对流扩散过程，输出温度场和密度场作为物理参数。
- **Vellum 求解器**用于纺织品，处理布料碰撞、拉伸和弯曲约束，输出面片级变形轨迹。
- **MPM 求解器**（Material Point Method）用于流变物质（如黏弹性果冻），采用 Kelvin–Voigt 模型分解应力：
  
  $$\pmb{\sigma} = \pmb{\sigma}_{\mathrm{elastic}} + \pmb{\sigma}_{\mathrm{viscous}}$$
  
  弹性应力分量由超弹性本构给出，粘性分量基于应变率张量，二者叠加描述材料的蠕变和应力松弛行为。

每个场景的地面真值物理信息包含：**三维粒子轨迹**（时间序列上的空间位置）和**物理参数**（如液体的粘度、流变物质的杨氏模量与泊松比、气体的温度场）。这些信息是现有 DyNVS 基准（如 D-NeRF、HyperNeRF、NeRF-DS 等）完全缺失的，构成了 PhysGaia 在物理真实性评估上的独特优势。

### 渲染阶段：路径追踪与多模态输出

模拟输出的粒子/网格状态被送入**路径追踪渲染器**（256 样本/像素）生成光度真实的多视角 RGB 图像。由于路径追踪忠实模拟了光的物理传播（包括镜面反射、折射和全局光照），渲染结果在视觉真实感上显著优于现有基于光栅化或简化光照模型的数据集。

更重要的是，仿真节点图（node graphs）允许用户生成远超 RGB 的辅助模态（Figure 3），包括深度图、法向图、重光照图像等。这种多模态输出机制使得 PhysGaia 不仅是一个评估基准，更是一个可定制的数据生成平台，能够灵活适配逆渲染、物理参数估计等下游任务。

### 评估流水线：双维度度量

PhysGaia 的评估体系分为两个维度：

1. **光度真实性**：沿用 PSNR、SSIM、LPIPS 等标准图像质量指标，评估重建视角与渲染真值的像素级一致性。
2. **物理真实性**：引入两个原创度量——**轨迹距离（Trajectory Distance, TD）** 和**离群百分比曲线下面积（Area Under Outlier Percentage, AUOP）**。TD 计算重建高斯原语与最近地面真值轨迹之间的平均欧氏距离，AUOP 通过跟踪轨迹偏离阈值的时间演化来捕捉累积离群行为。这两个度量共同量化了重建方法对底层物理运动的保真度，是现有基准无法提供的评估维度。

### 输入输出流总结

- **输入**：仿真节点图定义的场景配置（材料类型、初始条件、边界约束等）。
- **中间产物**：物理求解器输出的粒子/网格状态序列（含轨迹和参数）。
- **最终输出**：多视角 RGB 图像 + 辅助模态（深度、法向等）+ 完整物理真值（三维轨迹、粘度、杨氏模量等）。

这一流水线使得 PhysGaia 在运动复杂度（动态得分 0.444，为现有物理基准最高）和视觉真实感（FID 207.8、KID 0.118，均为最低）两个关键维度上均显著超越现有数据集，为 DyNVS 研究从“看起来对”迈向“物理上对”提供了基础设施。

### 物理模拟管线

PhysGaia 基准的物理真实性源于其材料特异的物理求解器管线。针对不同物质类型，分别采用四种成熟的数值求解器生成粒子轨迹和物理参数真值：

- **FLIP 求解器**（Fluid-Implicit Particle）：用于液体材料模拟，基于不可压缩流体的动量守恒方程驱动。其核心控制方程为：

$$
\rho \left( \frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla) \mathbf{u} \right) = -\nabla p + \mu \nabla^2 \mathbf{u} + \rho \mathbf{g}
$$

其中 $\rho$ 为密度，$\mathbf{u}$ 为速度场，$p$ 为压力，$\mu$ 为动力粘度，$\mathbf{g}$ 为重力加速度。该方程描述粘性不可压缩流体在重力作用下的运动，重力为唯一外力项。

- **Pyro 求解器**：用于气体（烟雾）场景模拟，可生成温度场等物理参数真值。

- **Vellum 求解器**：用于纺织品模拟，处理布料等柔性材料的变形与交互。

- **MPM 求解器**（Material Point Method）：用于流变物质模拟，采用 Kelvin–Voigt 粘弹性本构模型，将总应力分解为弹性和粘性分量：

$$
\pmb{\sigma} = \pmb{\sigma}_{\mathrm{elastic}} + \pmb{\sigma}_{\mathrm{viscous}}
$$

其中 $\pmb{\sigma}_{\mathrm{elastic}}$ 为弹性应力分量，$\pmb{\sigma}_{\mathrm{viscous}}$ 为粘性应力分量。该模型可同时捕捉材料的弹性恢复和粘性耗散行为。

以上求解器均在 Houdini 节点图框架内实现，PhysGaia 提供完整的仿真节点图，用户可据此生成多模态输出（RGB、深度、法向、重光照）。

### 物理真实性评估指标

为定量评估重建结果与物理真值的一致性，PhysGaia 引入两个核心指标。

#### 轨迹距离（Trajectory Distance, TD）

TD 度量重建高斯原语轨迹与最近邻地面真实轨迹之间的平均欧氏距离：

$$
\mathrm{TD} = \frac{1}{MT} \sum_{i=0}^{M-1} \sum_{t=0}^{T-1} \| X_i^{t,\mathrm{recon}} - X_{j(i)}^{t,\mathrm{gt}} \|_2
$$

其中 $M$ 为重建原语数量，$T$ 为时间帧数，$X_i^{t,\mathrm{recon}}$ 为第 $i$ 个重建原语在时刻 $t$ 的空间位置，$X_{j(i)}^{t,\mathrm{gt}}$ 为与之匹配的最近邻地面真实轨迹位置。TD 值越低，表明重建运动与物理真值越一致。

#### 离群百分比曲线下面积（AUOP）

为补充 TD 对整体轨迹偏差的度量，AUOP 聚焦于偏离阈值 $\delta$ 的离群原语随时间的累积行为。首先定义离群指示器：

$$
O_i^t = \begin{cases} 1 & \text{if } O_i^{t-1}=1 \text{ or } \| X_i^{t,\mathrm{recon}} - X_{j(i)}^{t,\mathrm{gt}} \|_2 > \delta \\ 0 & \text{otherwise} \end{cases}
$$

该指示器具有“一旦离群、始终离群”的传播特性：若原语在 $t-1$ 时刻已标记为离群，或在 $t$ 时刻轨迹偏差超过阈值 $\delta$，则 $O_i^t=1$。AUOP 通过计算整个序列中离群百分比曲线下的面积，全面捕捉重建方法在物理流跟踪上的失败程度。

### 渲染管线

物理模拟生成的三维粒子轨迹经路径追踪渲染器生成多视角 RGB 图像，每个像素采样 256 条光线。稀疏视角的相机位姿通过 COLMAP 从渲染图像中重建，为高斯泼溅等下游方法提供初始化点云。

## 实验与关键发现

### 基准特性验证：运动复杂度与真实感

在评估现有方法之前，我们首先验证 PhysGaia 作为基准的内在质量。与现有物理基准的对比（Table 3）表明，PhysGaia 在运动复杂度和真实感两个维度上均取得最优：动态得分 0.444（最高），FID 207.8（最低），KID 0.118（最低）。这意味着 PhysGaia 提供了比 ScalarFlow、PAC-NeRF、Spring-Gaus 等现有数据集更丰富的动态行为和更高的视觉真实感。Figure 4 揭示了这些现有数据集的根本局限：它们要么覆盖的材料类型极为狭窄（如单一烟雾或单类弹性体），要么动态过于简化，且均缺乏多体交互场景和完整的物理真值信息。

![[assets/figures/papers/paper_list_l2239_https_arxiv_org_abs_2506_02794/figures/006_Table_3.jpg]]
*Table 3: Comparison with existing physics-based benchmarks on motion complexity and photorealism. PhysGaia achieves the highest dynamic score [44] and lowest FID [23] and KID [3], demonstrating richer dynamics and greater visual realism than existing DyNVS datasets. Note that PAC-NeRF sequences are too short to compute a dynamic score*

### 光度重建性能：现有方法的系统性退化

Table 4 按材料类别汇总了各算法的平均定量结果。一个清晰的趋势是：所有方法在纺织品类场景上表现相对较好，但在流变物质场景上性能急剧恶化——后者正是多体交互最复杂的材料类别。以单目设置为例（Table 5），**D-3DGS** 在全部 17 个场景上的平均 PSNR 仅为 21.7 dB，**4DGS** 为 22.7 dB，即使多目设置下的最优结果也未能突破 30 dB。这与现有 DyNVS 基准（如 D-NeRF 数据集、NeRF-DS 数据集）上这些方法通常能取得 30+ dB 的表现形成鲜明对比。

![[assets/figures/papers/paper_list_l2239_https_arxiv_org_abs_2506_02794/figures/008_Table_4.jpg]]
*Table 4: Average quantitative results for each material category across all algorithms. While performance is generally high for textile, it deteriorates significantly for rheological substances, which typically exhibit complex dynamics involving multiple interacting components*

![[assets/figures/papers/paper_list_l2239_https_arxiv_org_abs_2506_02794/figures/011_Table_5.jpg]]
*Table 5: Average quantitative results for both monocular and multiview settings, averaged across all 17 scenes. While multiview setups generally offer better reconstruction performance than monocular ones, even multiview results achieve PSNR scores below 30. This highlights the substantial difficulty in reconstructing the complex multi-body interactions in our benchmark*

定性结果（Figure 5）进一步暴露了失败模式：在 jelly party 等多体交互场景中，所有方法均频繁产生针状伪影，且无法准确重建相互碰撞物体的接触边界。作者将这一退化归因于 PhysGaia 中多体交互带来的运动复杂性——Figure 6 的运动多样性对比证实，PhysGaia 的动态得分在所有 DyNVS 数据集中最高，其包含的非局部、非刚性运动远超现有基准。

![[assets/figures/papers/paper_list_l2239_https_arxiv_org_abs_2506_02794/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative results of recent DyNVS methods on the jelly party scene with monocular setup. All methods struggle to accurately capture multi-body interactions by frequently exhibiting needle-like artifacts and failing to reconstruct dynamic elements accurately. Please refer to our supplementary documents for more qualitative results*

### 物理真实性评估：轨迹偏差揭示的根本缺陷

光度指标仅反映视觉质量，而 PhysGaia 独有的物理真值信息允许直接度量重建的物理一致性。Table 6 报告了 Trajectory Distance (TD) 和 AUOP 两个物理真实性指标。

在 Box-smoke（气体）场景中，**D-3DGS** 的 TD 高达 4.01，而真值为 0.84——这意味着重建的高斯原语轨迹与真实粒子运动之间存在数量级的偏差。AUOP 的差距更为惊人：D-3DGS 为 37.9，真值为 0.3。Figure 7 通过重建粒子流与地面真实物理流的可视化对比，直观展示了这一失败：现有方法生成的“流”在空间分布和运动方向上与真实物理流几乎无关。Figure 8 进一步显示，离群百分比随时间持续攀升，表明方法无法在长时间跨度上跟踪物理运动——这恰恰是物理一致性评估所揭示的、光度指标无法捕捉的根本性缺陷。

![[assets/figures/papers/paper_list_l2239_https_arxiv_org_abs_2506_02794/figures/013_Figure_7.jpg]]
*Figure 7: Comparison of reconstructed flows and ground truth on the Box-smoke and Pisa scenes. Reconstructed flows deviate significantly from ground truth, where photorealism is achieved through local surface fluctuations rather than following actual physical motion*

在流变物质场景（Cow）中，TD 的差距相对较小（D-3DGS: 0.07 vs. GT: 0.03），这与该类材料运动速度较慢、形变更可预测的特性一致。但即便如此，多体碰撞引起的局部快速形变仍导致明显的轨迹偏离。

### 逆物理参数估计的失败

Table 7 展示了逆物理参数估计任务的结果。**PAC-NeRF** 和 **GIC** 两种方法均显著低估了杨氏模量 E——在包含多体交互的场景中，估计值往往比真值低一个数量级。这是因为这些方法的设计假设场景中仅存在单一物体，其损失函数无法解耦多体交互中来自不同物体的力学信号。这进一步证实了 PhysGaia 所引入的多体交互场景对现有方法构成了超出光度重建范畴的深层挑战。

![[assets/figures/papers/paper_list_l2239_https_arxiv_org_abs_2506_02794/figures/015_Table_7.jpg]]
*Table 7: Comparison of estimated physics parameters (Young’s modulus E and Poisson’s ratio ν) against ground truth. Both PAC-NeRF [41] and GIC [6] methods substantially underestimate material stiffness in multi-object scenarios*

### 失败模式总结

综合上述分析，现有 DyNVS 方法在 PhysGaia 上暴露出的失败模式可归纳为三个层次：

1. **细粒度动态捕捉失败**：基于 MLP 或网格的表示（如 D-NeRF、4DGS）无法建模流体飞溅等细粒度动态，产生模糊或缺失的重建。
2. **多体交互建模失败**：所有方法在多个物体碰撞、接触的场景中产生针状伪影和边界模糊，高斯原语的运动轨迹与真实物理流严重偏离。
3. **物理参数估计失败**：逆物理方法因无法解耦多体力学信号而系统性低估材料刚度。

这些失败模式共同指向一个核心结论：现有方法在 PhysGaia 上的表现瓶颈并非来自光度重建能力不足，而是源于对复杂物理动态的根本性建模缺陷。PhysGaia 通过提供完整物理真值，使这一缺陷首次可被定量诊断。

## 定位与知识库关联

### 基准构建的方法学定位

PhysGaia 并非提出一种新的动态新视角合成（DyNVS）算法，而是构建了一个物理感知的评估基准，其核心方法论贡献在于将**物理一致性**确立为与光度质量并列的评估维度。这一设计直接回应了现有 DyNVS 基准的根本性瓶颈：仅关注光度真实，缺乏用于评估物理一致性的真实物理信息（如三维轨迹和物理参数）。

从方法谱系来看，PhysGaia 的构建范式与三类现有工作形成对比：

**相对于 DyNVS 数据集**（Table 1）：现有基准如 D-NeRF、HyperNeRF、DyCheck 等仅提供多视角 RGB 图像，缺乏任何形式的物理真值。PhysGaia 通过材料特定物理求解器——FLIP（液体）、Pyro（气体）、Vellum（纺织品）、MPM（流变物质）——生成精确的三维粒子轨迹和物理参数（粘度、杨氏模量、泊松比等），使物理真实性的定量评估首次成为可能。

**相对于物理模拟数据集**（Table 2）：ScalarFlow、PAC-NeRF、Spring-Gaus 等虽涉及物理现象，但存在三重局限：（1）材料覆盖狭窄，通常仅限于单一流体或弹性体；（2）动态过于简化，缺乏多体交互；（3）未提供完整的物理参数真值。PhysGaia 覆盖四种材料类型、引入复杂多体交互场景，并提供完整的轨迹与参数真值，填补了这一空白。定量证据表明，PhysGaia 在运动复杂度（动态得分 0.444，最高）和真实感（FID 207.8，最低；KID 0.118，最低）方面均显著优于现有物理基准（Table 3）。

**相对于逆物理估计方法**：PAC-NeRF 和 GIC 等方法尝试从视觉观测中估计物理参数，但它们针对单一物体场景设计。在 PhysGaia 的多体交互场景中，这些方法显著低估杨氏模量 E（Table 7），暴露了其处理复杂交互的根本性不足。

### 适用边界与能力范围

PhysGaia 的适用边界由其设计选择决定：

**支持的评估维度**：基准同时支持光度质量评估（PSNR、SSIM、LPIPS）和物理真实性评估（Trajectory Distance TD、Area Under Outlier Percentage AUOP）。TD 度量重建轨迹与最近真值轨迹的平均欧氏距离，AUOP 则通过累积离群百分比捕捉整个序列中的跟踪失败行为。这种双重评估体系使研究者能够区分“看起来好”和“物理上正确”的重建结果。

**多模态扩展能力**：由于场景由仿真节点图驱动，用户可生成 RGB 之外的多种模态（深度、法向、重光照等，Figure 3），便于适配特定下游任务。基准提供完整源代码和仿真节点图，研究人员可定制数据，避免评估偏差。

**已知局限**：
1. **仿真-真实差距**：物理模拟器使用简化的本构假设和数值离散化，可能无法完全捕捉真实世界的复杂材料响应和细尺度交互（Section F）。数据集为仿真生成，与真实世界的视觉差距可能影响泛化性能。
2. **求解器-表示不匹配**：体积求解器（如烟雾的 Pyro）基于欧拉描述，而主流 DyNVS 方法（如 3D/4D Gaussian Splatting）基于拉格朗日粒子表示，二者之间的整合仍是开放问题。
3. **知识产权风险**：场景编辑能力可能引发原始视频内容的知识产权问题（Section F）。

### 开放问题与未来方向

PhysGaia 揭示的开放问题指向三个关键方向：

1. **体积-粒子表示桥接**：如何将体积求解器（如烟雾的 Pyro）的输出有效整合到基于粒子的高斯泼溅框架中？当前方法在气体场景上的 TD 高达 4.01（Box-smoke，D-3DGS），AUOP 达 37.9，表明根本性的表示不匹配。

2. **细尺度物理建模**：基于仿真的方法如何更好地捕捉复杂材料响应（如流变物质的粘弹性应力分解 $\pmb{\sigma} = \pmb{\sigma}_{\mathrm{elastic}} + \pmb{\sigma}_{\mathrm{viscous}}$）或细尺度交互（如飞溅）？现有 MLP 和网格表示在流体飞溅等细粒度动态上表现失败（Section 5.2.1）。

3. **物理感知的重建架构**：现有方法（D-3DGS、4DGS、STG、MoSca、SoM）在 PhysGaia 上表现显著下降，尤其在高动态场景中（Tables 4-5），表明需要将物理先验（如动量守恒 $\rho \left( \frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla) \mathbf{u} \right) = -\nabla p + \mu \nabla^2 \mathbf{u} + \rho \mathbf{g}$）显式嵌入重建架构，而非仅依赖数据驱动的变形场。

## 原文 PDF

![[paperPDFs/CVPR_2026/PhysGaia_A_Physics_aware_Benchmark_with_Multi_Body_Interactions_for_Dynamic_Novel_View_Synthesis.pdf]]
