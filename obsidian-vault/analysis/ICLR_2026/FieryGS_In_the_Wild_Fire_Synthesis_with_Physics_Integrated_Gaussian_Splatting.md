---
title: "FieryGS: In-the-Wild Fire Synthesis with Physics-Integrated Gaussian Splatting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/FieryGS_In_the_Wild_Fire_Synthesis_with_Physics_Integrated_Gaussian_Splatting_d7901a6ed2cd.pdf
project_link: "https://pku-vcl-geometry.github.io/FieryGS/"
code_link: null
aliases:
- FieryGS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 将MLLM材料推理、体积燃烧模拟和3DGS渲染紧密耦合，使火焰能够自动适应真实场景的几何和材料属性，并提供精确的用户控制参数。
primary_logic: 通过零样本MLLM从3DGS重建中推断燃烧相关属性，驱动物理模拟，并将火焰、烟雾和3DGS统一渲染，首次实现了在真实世界场景中既物理合理又可控制的动态火焰合成。
claims:
- 在视觉质量和结构保持指标上均优于所有基线，Aesthetic Quality 0.624，DINO Structure Score 0.38。
- 用户研究中FieryGS在感知真实性和物理合理性上显著优于基线，偏好率高达88.9%。
- MLLM材料推理平均准确率达89.31%，为物理模拟提供了可靠的属性输入。
- 6 real-world scenes (Firewood, Kitchen, Chair, Stool, Garden, Playground) 上 Aesthetic Quality ↑ = 0.624
---

# FieryGS: In-the-Wild Fire Synthesis with Physics-Integrated Gaussian Splatting

> [!tip] 核心洞察
> 通过零样本MLLM从3DGS重建中推断燃烧相关属性，驱动物理模拟，并将火焰、烟雾和3DGS统一渲染，首次实现了在真实世界场景中既物理合理又可控制的动态火焰合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | FieryGS：基于物理集成高斯溅射的真实场景火焰合成 |
| 英文题名 | FieryGS: In-the-Wild Fire Synthesis with Physics-Integrated Gaussian Splatting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ziKFH7whvy) · [Project](https://pku-vcl-geometry.github.io/FieryGS/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | FieryGS |
| Dataset | 6 real-world scenes, User study |

> [!tip] 效果简介
> - 6 real-world scenes (Firewood, Kitchen, Chair, Stool, Garden, Playground) 上，Aesthetic Quality ↑ 0.624 vs 0.605 (Runway-V2V) (+0.019)。
> - 6 real-world scenes 上，Imaging Quality ↑ 0.702 vs 0.701 (Runway-V2V) (+0.001)；DINO Structure Score ↓ 0.38 vs 0.68 (Runway-V2V) (-0.30)。
> - User study (86/88 participants) 上，Perceptual Realism preference rate (Image/Video) FieryGS preferred at 88.9% / 77.8% (vs AutoVFX) vs AutoVFX。

## 概要

**问题与瓶颈**：在真实世界场景中合成火焰效果是一项极具挑战的任务。传统基于物理的计算流体力学（CFD）和视觉特效（VFX）管线依赖繁琐的手工建模与参数调试，商业软件（如SimsUshare）多局限于预录制效果的简单叠加，而新兴的大型视频生成模型（如Runway Gen-3 Alpha）虽能产生视觉上逼真的火焰，却缺乏对场景几何与物理一致性的保证。现有方法无法在单一框架内同时实现视觉真实性与物理可控的火焰合成。

**核心方法定位**：FieryGS 提出了一种物理集成的火焰合成范式，将三个关键模块紧密耦合：多模态大语言模型（MLLM）驱动的零样本材料物理属性推理、高效体积燃烧模拟，以及统一的火焰与三维高斯泼溅（3DGS）渲染器。该方法从多视角图像出发，首先利用 PGSR（Chen et al., 2024）重建具有高精度法向与深度信息的3DGS场景；随后通过 GPT-4o 对分割后的高斯区域进行材料类型、可燃性、热扩散率等燃烧相关属性的零样本推断；基于这些属性自动构建仿真域并驱动火焰传播、烟雾扩散与物体表面炭化的体积模拟；最终在统一渲染管线中联合积分火焰自发射、烟雾吸收、3DGS炭化效果以及基于 Phong 模型的火焰光照，生成物理合理且视觉逼真的动态火焰。

**主要结果**：在6个真实场景上的定量评估表明，FieryGS 在美学质量（Aesthetic Quality 0.624）和结构保持（DINO Structure Score 0.38）上均优于 AutoVFX、Runway-V2V 和 Instruct-GS2GS 等基线方法。用户研究中，FieryGS 在感知真实性与物理合理性上的偏好率分别高达 88.9% 和 86.6%，显著领先于基线。MLLM 材料推理模块的平均准确率达 89.31%，为物理模拟提供了可靠输入。整体框架模拟与渲染阶段平均每帧耗时 2.37 秒，GPU 显存低于 10.0 GB，展现了实用化的计算效率。

火焰合成是计算机图形学、视觉特效（VFX）与安全仿真等领域的长期核心需求。真实世界中的燃烧过程——如消防演练中的实火训练（Figure 2左）或全尺寸燃烧实验中的火焰蔓延测试（Figure 2右）——受材料属性、几何结构、气流和热传递等多重物理因素的共同支配，表现出高度复杂的时空动态。然而，在任意真实场景中生成既视觉逼真又物理可控的火焰，至今仍是一个悬而未决的难题。

现有方法在三个关键维度上存在显著缺口。**传统物理仿真管线**（如基于计算流体动力学CFD的VFX工具和商业软件AutoVFX）虽然能产生物理合理的火焰，但需要用户手动构建三维几何体、标注材料可燃性并配置仿真域，流程繁琐且高度依赖专业经验，难以在真实世界场景中快速部署。**商业应急仿真软件**（如SimsUshare）则依赖预录制的二维火焰效果进行简单叠加，缺乏场景感知能力，无法根据真实物体的几何与材料产生自适应的燃烧行为。**大型视频生成模型**（如Runway Gen-3 Alpha）虽然能生成视觉上引人注目的火焰视频，但其生成过程是一个黑箱，缺乏对底层物理过程的显式建模，因而无法保证火焰传播的物理一致性，且经常意外篡改场景结构（如物体几何变形、纹理漂移）。**基于3DGS的场景编辑方法**（如Instruct-GS2GS）仅能产生静态的、低保真度的火焰外观修改，完全不具备时间演化能力。

上述方法的核心瓶颈在于：**视觉真实性与物理可控性无法在同一框架内兼得**。物理仿真方法缺乏对真实场景的自动感知能力，而数据驱动或生成式方法则牺牲了物理合理性。这揭示了一个根本性的因果机制：要将火焰合成从受控的虚拟环境推向任意真实场景，必须将**场景理解**（材料属性与几何结构的自动获取）、**物理模拟**（燃烧动力学的显式建模）和**真实感渲染**（火焰、烟雾与场景的联合绘制）三者紧密耦合，形成一个闭环系统。

FieryGS正是在这一动机下提出的。其核心洞察是：利用多模态大语言模型（MLLM）的零样本推理能力，从3DGS重建中自动提取燃烧相关的物理属性，以此驱动物理仿真，并最终通过统一的体积渲染管线将火焰、烟雾和3DGS场景无缝融合。这一设计使得火焰能够自动适应真实场景的几何与材料，同时提供对点火位置、火焰强度和气流方向等关键参数的直观控制，首次实现了在真实世界场景中既物理合理又可交互控制的动态火焰合成。

## 核心方法与创新机理

FieryGS 的核心创新在于将多模态大语言模型（MLLM）的材料推理、体积燃烧模拟与 3D 高斯泼溅（3DGS）渲染紧密耦合，首次实现了在真实世界场景中既物理合理又可精确控制的动态火焰合成。其关键突破体现在以下五个维度。

### 从 3DGS 重建到物理模拟的零样本属性推断

现有 VFX 管道（如 **AutoVFX**, Hsu et al., 2024）依赖手动标注材料类型和可燃性，或使用预定义的属性库，无法自动适应任意真实场景。FieryGS 采用 **PGSR**（Chen et al., 2024）从多视角图像重建具有高质量法线和深度的 3DGS 场景，随后将高斯体分割为材料一致的 3D 区域，并利用 **GPT-4o** 零样本推断每个区域的材料类型、可燃性、热扩散率等燃烧相关物理属性（Figure 4）。实验表明，该 MLLM 材料推理模块的平均准确率达 **89.31%**（Table 5），为后续物理模拟提供了可靠且自动化的属性输入，彻底消除了手工建模的瓶颈。

### 场景自适应的体积燃烧模拟

传统方法需要手工构建仿真域并指定可燃区域。FieryGS 从 3DGS 占据网格自动构建仿真域，并根据 MLLM 推理结果自动标记可燃与非可燃体素。在此基础上，系统运行基于不可压缩流动模型的火焰模拟（考虑浮力和涡度约束力）和简化的固体传热方程驱动的炭化模拟。用户可通过设置点火位置、调节浮力系数 $\alpha$ 控制火焰强度、添加外部风力控制气流方向，实现直觉化的物理参数控制（Figure 7）。

### 统一体积渲染管线

现有方案通常将火焰仿真渲染与场景渲染分离，或简单叠加预录制效果。FieryGS 提出了首个统一体积渲染框架，其像素辐射量合成公式为：

$$L = L_{\mathrm{fire}} + L_{\mathrm{smoke}} + \hat{T} ( L_{\mathrm{GS}} + L_{\mathrm{phong}} )$$

该管线联合积分火焰自发射（基于普朗克黑体辐射定律）、烟雾吸收、3DGS 炭化颜色调整，以及基于 Phong 模型的场景照明——从高温火焰体素累加光谱辐射量计算漫反射和镜面反射：

$$L_{\lambda} = \sum_{i} L_{e,\lambda}^{(i)} \cdot \left[ k_d ( \mathbf{n} \cdot \mathbf{l}_i ) + k_s ( \mathbf{r}_i \cdot \mathbf{v} )^s \right]$$

Figure 5 的渲染组件分解验证了炭化、烟雾、火焰和 Phong 光照各自的有效贡献。

### 物理一致性与视觉质量的统一

定量实验（Table 2）显示，FieryGS 在 6 个真实场景上的 Aesthetic Quality 达 **0.624**，DINO Structure Score 低至 **0.38**，显著优于 **Runway-V2V**（0.605 / 0.68），表明其在保持场景结构的同时实现了更高的视觉质量。用户研究（Table 3）中，FieryGS 在感知真实性和物理合理性上的偏好率高达 **88.9%**（vs AutoVFX），证明了物理模拟驱动的合成比纯生成式方法更受用户认可。

### 计算效率与可选的生成式精炼

整体框架模拟与渲染阶段平均每帧耗时 **2.37 秒**，GPU 显存低于 10.0 GB（Table 6），证明了计算效率。此外，FieryGS 还引入了基于扩散视频模型 **Wan2.1** 的可选生成式精炼模块，可进一步提升视觉保真度，但该模块在长时间序列中存在时间一致性限制（Figure 11）。

FieryGS 的核心设计理念是将**物理燃烧模拟**与**3D高斯泼溅（3DGS）场景重建**紧密耦合，通过多模态大语言模型（MLLM）作为桥梁，自动从真实场景的多视角图像中推断燃烧所需的物理属性。整个 pipeline 如图3所示，由五个关键模块串联构成一个端到端的合成系统。

### 输入与场景重建

给定一组真实场景的多视角图像作为输入，FieryGS 首先采用 **PGSR**（Chen et al., 2024）进行场景重建。选择 PGSR 而非通用 3DGS 方法的关键原因在于，PGSR 能联合重建出高保真的外观和精确的几何信息——包括高质量的法线和深度图。这些几何信息对后续的物理模拟至关重要：法线用于渲染管线中的火焰光照计算，深度和占据网格则为体积仿真提供了精确的表面边界条件。

### 高斯分割与材料推理

重建完成后，系统将 3D 高斯体分割为材料一致的 3D 区域，每个区域共享同一种材质属性。随后，这些分割区域的 2D 渲染结果被送入 **GPT-4o**（Hurst et al., 2024）进行零样本材料推理。MLLM 不仅识别材料类型（如木材、塑料、金属），还推断与燃烧直接相关的物理属性：可燃性、热扩散率、反应速率等。推理结果通过投影机制回写到对应的 3D 高斯体上，使每个高斯体都携带燃烧感知的物理属性标签。

### 仿真域构建与燃烧模拟

基于携带物理属性的 3DGS，系统自动构建体积仿真所需的占据网格。网格中的体素根据 MLLM 推理结果被标记为可燃或非可燃区域，无需任何手工标注。燃烧模拟分为两个并行的子过程：

- **火焰模拟**：采用不可压缩流动模型（Nguyen et al., 2002），在空气区域计算速度场、压力和反应进程变量 $Y$。温度被近似为 $Y$ 的二次函数，避免了求解复杂的 PDE 热模型，在保持物理合理性的同时显著提升计算效率。模拟支持用户通过调节浮力系数 $\alpha$、反应速率 $k$ 和外加风力来控制火焰强度、传播速度和气流方向。
- **炭化模拟**：在可燃固体区域运行简化的传热方程，计算材料温度 $T_m$ 的时空演变。当温度超过炭化阈值时，材料表面颜色逐渐变暗，模拟真实的烧焦效果。

### 统一体积渲染

FieryGS 引入了一个统一的体积渲染管线，将模拟的火焰、烟雾与 3DGS 场景联合渲染为最终图像。每个像素的辐射量由以下公式合成：

$$L = L_{\mathrm{fire}} + L_{\mathrm{smoke}} + \hat{T} ( L_{\mathrm{GS}} + L_{\mathrm{phong}} )$$

其中 $L_{\mathrm{fire}}$ 为基于普朗克黑体辐射定律计算的火焰自发射贡献，$L_{\mathrm{smoke}}$ 为烟雾的吸收和散射效应，$\hat{T}$ 为累积透过率，$L_{\mathrm{GS}}$ 为原始 3DGS 场景辐射（已根据炭化程度调整颜色），$L_{\mathrm{phong}}$ 为火焰对场景表面的 Phong 光照贡献。该渲染管线首次将火焰自发射、烟雾吸收、炭化颜色调整和动态场景照明统一到一个可微的体积渲染框架中。

### 可选生成式精炼

作为后处理步骤，FieryGS 提供了一个基于扩散视频模型 **Wan2.1**（Wang et al., 2025）的可选生成式精炼模块。该模块将仿真视频编码到潜在空间，注入噪声后以首帧为图像条件进行去噪，通过无分类器引导在保持场景结构的同时增强火焰的视觉保真度（如增强地面反射等细节）。需要注意的是，该模块可能引入时间不一致性（见 Figure 11），因此标记为可选。

### 模块间数据流

整个 pipeline 的数据流是单向且紧密耦合的：PGSR 重建提供几何基础 → 高斯分割与 MLLM 推理赋予物理语义 → 物理属性驱动燃烧模拟 → 模拟结果与 3DGS 场景在统一渲染器中合成最终输出。这种设计使得 FieryGS 能够在零人工干预的情况下，将任意真实场景的多视角图像转化为物理合理、用户可控的动态火焰合成结果。

![[assets/figures/papers/paper_list_l81_https_openreview_net_forum_id_ziKFH7whvy/figures/005_Figure_3.jpg]]
*Figure 3: Overall Pipeline of FieryGS. Given multi-view images as input, we first apply PGSR (Chen et al., 2024) to reconstruct scenes with high-quality normal and depth. Next, we leverage MLLM to infer combustionrelated properties, such as material type and burnability. Based on these, we conduct combustion simulations, enabling fire and charring effects with user control. A unified volumetric renderer seamlessly integrates 3DGS and fire, accounting for smoke scattering, fire illumination, and charring, producing realistic fire results*

FieryGS 的核心架构由三个紧耦合模块构成，形成从场景理解到物理模拟再到统一渲染的完整闭环。

### 3DGS 场景重建与材料推理

给定多视角图像，系统首先采用 **PGSR**（Chen et al., 2024）进行场景重建，同时获取高保真外观与精确的法线、深度信息。随后，将重建的 3D 高斯体分割为材料一致的 3D 区域，每个区域共享同一材质属性。这些区域通过零样本 **MLLM（GPT-4o）** 进行材料推理，自动推断材料类型、可燃性、热扩散率等燃烧相关物理属性，并将推断结果投影回对应的 3D 高斯体上。这一流程将传统需要手工标注的材料属性获取过程完全自动化，为后续物理模拟提供了可靠的输入——实验表明材料推理平均准确率达 89.31%（Table 5）。

### 体积燃烧模拟

燃烧模拟分为火焰模拟与炭化模拟两部分，均基于 MLLM 推断的物理属性驱动。

**火焰模拟**采用不可压缩流动模型（Nguyen et al., 2002），以平衡物理合理性与计算效率。其核心控制方程为：

$$
\frac{\partial \mathbf{u}}{\partial t} + \mathbf{u} \cdot \nabla \mathbf{u} = -\frac{1}{\rho} \nabla p + \mathbf{f}, \quad \text{s.t.} \ \nabla \cdot \mathbf{u} = 0
$$

$$
\frac{\partial Y}{\partial t} + \mathbf{u} \cdot \nabla Y = -k
$$

其中 $\mathbf{u}$ 为速度场，$p$ 为压力，$\rho$ 为密度，$\mathbf{f}$ 为外力项（包含浮力 $\mathbf{f}_{\text{buo}} = \alpha(T - T_{\text{air}})\mathbf{z}$ 和涡旋约束力），$Y$ 为反应进程变量，$k$ 为反应速率。温度 $T$ 被近似为 $Y$ 的二次函数，避免求解完整的 PDE 热模型，从而在保持物理合理性的同时显著降低计算开销。

**炭化模拟**通过简化的传热方程计算固体材料的温度演变：

$$
\frac{\partial T_m}{\partial t} = \beta \nabla^2 T_m + \gamma_m (T_{\text{amb}}^4 - T_m^4) + S_{T_m}
$$

其中 $T_m$ 为材料温度，$\beta$ 为热扩散率（由 MLLM 推断），$\gamma_m$ 控制辐射换热，$S_{T_m}$ 为火焰热源项。当材料温度超过炭化阈值时，表面颜色向炭化色过渡，模拟燃烧导致的视觉退化效果。

用户可通过设置点火位置、调节浮力系数 $\alpha$（控制火焰强度）和反应速率 $k$、添加外部风力等参数，实现对燃烧过程的直观控制。

### 统一体积渲染管线

渲染管线将模拟的火焰、烟雾与 3DGS 场景进行联合渲染。每个像素的最终辐射量由以下公式合成：

$$
L = L_{\text{fire}} + L_{\text{smoke}} + \hat{T} (L_{\text{GS}} + L_{\text{phong}})
$$

其中 $L_{\text{fire}}$ 为火焰自发射辐射，基于普朗克黑体辐射定律计算：

$$
L_{e,\lambda}(T) = \frac{2hc^2}{\lambda^5} \frac{1}{e^{\frac{hc}{\lambda kT}} - 1}
$$

$L_{\text{smoke}}$ 为烟雾的散射与吸收贡献，$\hat{T}$ 为累积透射率，$L_{\text{GS}}$ 为原始 3DGS 渲染结果（经炭化颜色调制），$L_{\text{phong}}$ 为火焰对场景表面的光照贡献。Phong 光照模型从高温火焰体素累加光谱辐射量，计算场景表面的漫反射和镜面反射：

$$
L_{\lambda} = \sum_{i} L_{e,\lambda}^{(i)} \cdot \left[ k_d (\mathbf{n} \cdot \mathbf{l}_i) + k_s (\mathbf{r}_i \cdot \mathbf{v})^s \right]
$$

其中 $\mathbf{n}$ 为表面法线（由 PGSR 提供），$\mathbf{l}_i$ 为火焰体素 $i$ 到表面点的方向，$\mathbf{r}_i$ 为反射方向，$\mathbf{v}$ 为视线方向，$k_d$、$k_s$ 和 $s$ 为材质参数。这一统一渲染框架首次将火焰自发射、烟雾吸收散射、3DGS 场景反射和火焰光照整合到单一体积渲染通道中，实现了物理一致的火焰-场景交互视觉合成。

## 实验与关键发现

### 定量评估

FieryGS 在 6 个真实场景（Firewood、Kitchen、Chair、Stool、Garden、Playground）上与三类基线方法进行了定量比较：基于 LLM 指令的自动 VFX 管道 **AutoVFX**（Hsu et al., 2024）、商业视频到视频生成模型 **Runway-V2V**（Runway, 2024a;b），以及文本驱动的 3DGS 编辑方法 **Instruct-GS2GS**（Vachha & Haque, 2024）。所有基线均使用相同的目标对象和标准文本提示进行公平比较，Runway-V2V 使用其官方视频编辑提示，AutoVFX 和 Instruct-GS2GS 使用统一的指令提示。

如 Table 2 所示，FieryGS 在视觉质量指标上取得了最高分——Aesthetic Quality 达到 **0.624**（Runway-V2V 为 0.605），Imaging Quality 为 **0.702**（与 Runway-V2V 的 0.701 基本持平）。更关键的是，在衡量场景结构保持能力的 DINO Structure Score 上，FieryGS 取得了 **0.38** 的最低分（越低越好），远优于 Runway-V2V 的 0.68。这表明 Runway-V2V 虽然能生成视觉上逼真的火焰，但会严重改变原始场景的外观和几何结构，而 FieryGS 在合成火焰的同时保持了底层场景的完整性。

![[assets/figures/papers/paper_list_l81_https_openreview_net_forum_id_ziKFH7whvy/figures/009_Table_2.jpg]]
*Table 2: Quantitative comparisons*

Table 1 从适用性维度对比了各类燃烧方法。传统 CFD/VFX 需要手动建模，商业软件（如 **SimsUshare**, 2025）依赖预录制效果，大型视频模型缺乏物理一致性。FieryGS 通过将场景对齐的物理模拟、视觉保真度、计算效率和用户控制相结合，首次为真实场景提供了可访问的火焰仿真方案。

![[assets/figures/papers/paper_list_l81_https_openreview_net_forum_id_ziKFH7whvy/figures/004_Table_1.jpg]]
*Table 1: Applicability comparison of combustion approaches. FieryGS offers accessible fire simulation for real-world scenes by combining scene-aligned physics, visual fidelity, efficiency, and user control*

### 用户研究

为评估感知质量，作者进行了用户研究（Table 3），招募了 86 至 88 名参与者，在感知真实性和物理合理性两个维度上进行偏好判断。

![[assets/figures/papers/paper_list_l81_https_openreview_net_forum_id_ziKFH7whvy/figures/008_Table_3.jpg]]
*Table 3: User Studies results*

在图像评估中，FieryGS 相比 AutoVFX 获得了 **88.9%** 的感知真实性偏好率和 **86.6%** 的物理合理性偏好率；相比 Runway-V2V 分别为 **79.4%** 和 **79.4%**；相比 Instruct-GS2GS 分别为 **85.5%** 和 **85.5%**。在视频评估中，FieryGS 同样显著优于所有基线：相比 AutoVFX 的偏好率为 **77.8%**（感知真实性）和 **85.5%**（物理合理性），相比 Runway-V2V 为 **66.5%** 和 **66.5%**，相比 Instruct-GS2GS 为 **63.0%** 和 **63.0%**。这些结果一致表明，用户认为 FieryGS 生成的火焰在视觉真实感和物理行为上都更可信。

### 定性比较

Figure 6 展示了 Kitchen 场景上各方法随时间演化的火焰合成结果。AutoVFX 在复杂室内环境中火焰真实感有限；Runway-V2V 生成视觉上合理的火焰，但显著改变了场景外观，且跳过了点火动态过程；Instruct-GS2GS 产生静态、低保真度的编辑，缺乏时间演化。相比之下，FieryGS 合成了物理上合理的、随时间演化的火焰，包含真实的点火、蔓延和场景照明效果。

![[assets/figures/papers/paper_list_l81_https_openreview_net_forum_id_ziKFH7whvy/figures/010_Figure_6.jpg]]
*Figure 6: Fire synthesis results over time on Kitchen scene. AutoVFX shows limited fire realism in complex indoor environments. Runway-V2V generates visually plausible flames but significantly alters the scene and omits ignition dynamics. Instruct-GS2GS produces static, low-fidelity edits without temporal evolution. In contrast, FieryGS synthesizes physically grounded, time-evolving fire with realistic ignition, spread, and scene illumination*

补充材料中的更多场景（Firewood、Stool、Chair、Garden、Playground，Figure 12-16）进一步验证了这一结论：FieryGS 在所有场景中一致地保持了场景结构，同时生成从点火到蔓延再到衰减的自然火焰动态，而基线方法要么破坏场景几何，要么缺乏时间连贯性。

### 消融实验

**MLLM 材料推理准确性。** Table 5 报告了 MLLM 材料推理模块在测试场景上的准确率，平均达到 **89.31%**。这一结果验证了零样本属性推断的有效性——GPT-4o 能够从 2D 渲染中可靠地识别材料类型（如木材、塑料、金属）并推断可燃性和热扩散率等燃烧相关物理属性。Figure 4 展示了定性案例：在包含金属勺子的复杂区域中，方法能正确区分勺子并推断其不可燃的金属属性。

**渲染组件分解。** Figure 5 逐层展示了统一渲染管线的贡献：从原始视图开始，依次添加炭化效果（b）、模拟烟雾（c）、模拟火焰（d），最后 Phong 光照增强了火焰对地面的照明效果（e）。可选的生成式精炼模块进一步增强了地面反射（f）。各组件独立渲染结果证明了炭化、烟雾、火焰和 Phong 光照各自的有效贡献。

**计算效率。** Table 6 报告了各场景关键组件的运行时分解，整体框架模拟与渲染阶段平均每帧耗时 **2.37 秒**，GPU 显存低于 **10.0 GB**。GPT-4o API 调用成本约为每场景 **$0.55**（Table 4），证明了方法的计算效率和经济可行性。

### 可控性验证

Figure 7 展示了 FieryGS 的用户控制能力。通过改变点火位置（桌下、桌后、桌前）和调整模拟参数（原始设置、通过增大浮力系数 α 和降低反应速率 k 增强火焰强度、添加右侧风力），方法能够直观地控制火焰的点火位置、强度和气流方向。这种细粒度的物理参数控制是现有方法无法提供的。

![[assets/figures/papers/paper_list_l81_https_openreview_net_forum_id_ziKFH7whvy/figures/011_Figure_7.jpg]]
*Figure 7: Controllability of FieryGS. Rows vary ignition location: under (Bottom), behind (Behind), and in front of the table (Front). Columns show simulation settings: baseline (Original), increased intensity via stronger buoyancy (↑ α) and lower reaction rate (↓ k) (Intensified), and added rightward wind (Airflow). FieryGS enables intuitive control over ignition, intensity, and airflow*

### 失败模式与局限性

尽管取得了显著成果，FieryGS 存在以下已知局限：

1. **物理简化。** 方法不模拟质量损失和热降解（如收缩、碎裂、坍塌），限制了极端燃烧场景下的物理真实感。也不模拟火焰如何点燃周围其他材料，无法表现火焰传播的复杂物理过程。

2. **场景规模限制。** 当前方法局限于物体级场景，无法直接应用于大规模场景（如森林或建筑火灾）。

3. **3DGS 重建伪影。** 重建的 3DGS 点分布不均匀，主要集中于物体表面，可能在体积仿真和渲染中引入伪影。

4. **MLLM 推理鲁棒性。** MLLM 材料推理在细小/远处背景物体、严重遮挡区域或 3DGS 重建伪影下存在误分类。

5. **生成式精炼的时间一致性。** Figure 11 展示了可选的生成式精炼模块的局限性：虽然火焰视觉上更逼真，但在火焰消散后底层桌子纹理发生了变化，揭示了扩散模型在长时间跨度上保持场景一致性的不足。

## 定位与知识库关联

FieryGS 处于真实场景火焰合成这一交叉领域，其核心贡献在于将**物理模拟的因果可控性**与**3DGS 的场景保真度**首次紧密耦合，填补了现有方案在“真实世界场景中物理合理且可控的火焰合成”这一关键空白。

### 与现有方法的边界与关系

**传统 CFD/VFX 管道**（如 **AutoVFX** (Hsu et al., 2024) 代表的基于 Blender 物理引擎的自动 VFX 管道）虽然具备物理模拟能力，但依赖手工构建的几何体和管理员指定的可燃区域，无法自动适应真实世界场景的复杂几何与材质分布。FieryGS 通过 PGSR (Chen et al., 2024) 重建和 MLLM 零样本推理，将这一手动建模过程完全自动化，同时保留了物理模拟的因果可控性。

**大型视频生成模型**（如 **Runway-V2V** (Runway, 2024a;b)）能够生成视觉上逼真的火焰，但其生成过程是黑箱的，缺乏对点火位置、火焰强度、气流方向等物理参数的精确控制，且会显著改变原始场景的结构——定量实验中其 DINO Structure Score 高达 0.68，而 FieryGS 仅为 0.38，表明 Runway-V2V 对场景结构的破坏远大于 FieryGS。此外，视频模型跳过了火焰从点燃到蔓延的时间演化过程，只展示完全发展的火焰。

**3DGS 编辑方法**（如 **Instruct-GS2GS** (Vachha & Haque, 2024)）通过文本驱动编辑 3DGS 场景，但其输出是静态的、低保真度的效果，缺乏时间动态和物理基础，无法表达火焰的传播、炭化和烟雾扩散等过程。

**商业消防仿真软件**（如 **SimsUshare**, 2025）依赖预录制的火焰效果库，无法根据任意真实场景的几何和材质自适应生成火焰。

### 核心因果机制与适用边界

FieryGS 的核心因果链条是：**PGSR 高精度几何 → MLLM 材料推理 → 物理模拟域自动构建 → 体积燃烧模拟 → 统一体积渲染**。这一链条使得火焰效果能够因果性地响应场景属性（材料可燃性、热扩散率）和用户控制参数（点火位置、浮力系数 α、反应速率 k、外部风力）。

**适用边界**明确：方法目前局限于**物体级场景**（如木柴、椅子、厨房台面），无法直接应用于大规模场景（如森林火灾、建筑火灾）。模拟不包含质量损失和热降解（收缩、碎裂、坍塌），也不模拟火焰点燃周围其他材料的二次传播过程。此外，3DGS 点云主要集中于物体表面，内部点分布不均匀，可能在体积仿真和渲染中引入伪影。

### 局限与开放问题

**物理建模的局限**：
- 不模拟质量损失和热降解（收缩、碎裂、坍塌），限制了物理真实感的上限。
- 不模拟火焰如何点燃周围其他可燃材料，无法表现火焰传播的完整物理过程。
- 方法局限于物体级场景，扩展至大规模场景需要解决计算效率和模拟域构建的根本挑战。

**感知与推理的局限**：
- MLLM 材料推理在细小/远处背景物体、严重遮挡区域或 3DGS 重建伪影下存在误分类，平均准确率为 89.31%，仍有约 10% 的错误率。
- 重建的 3DGS 点云分布不均匀，主要集中于物体表面，可能在体积仿真和渲染中引入伪影。

**生成式精炼的局限**：
- 可选的 Wan2.1 扩散视频模型精炼虽然提升了视觉保真度，但在长视频中可能出现时间不一致性——火焰遮挡的背景纹理在火焰消散后发生变化。
- 如何在生成式精炼中选择性地增强火焰效果而不影响背景，以及如何保持长视频中的 3D 一致性，仍是开放问题。

### 在知识库中的定位

FieryGS 在以下维度上建立了新的能力边界：
- **物理与视觉的联合保真**：首次在真实世界场景中同时实现物理模拟的因果可控性和 3DGS 的场景保真度。
- **零样本属性推理**：将 MLLM 引入燃烧模拟管道，以零样本方式从视觉信息推断物理属性，平均准确率 89.31%，GPT-4o API 调用成本约每场景 $0.55。
- **统一体积渲染**：将火焰自发射、烟雾吸收、3DGS 场景反射和基于 Phong 模型的火焰光照统一在一个体积渲染方程中，实现了火焰与场景的物理一致光照。
- **计算效率**：模拟与渲染阶段平均每帧耗时 2.37 秒，GPU 显存低于 10.0 GB，证明了在消费级硬件上的可行性。

该方法为后续研究开辟了若干方向：如何在模拟中加入质量损失和热降解以增强物理真实感，如何模拟火焰的二次传播过程，如何扩展至大规模场景，以及如何提高 MLLM 推理在低可见度和遮挡条件下的鲁棒性。

## 原文 PDF

![[paperPDFs/ICLR_2026/FieryGS_In_the_Wild_Fire_Synthesis_with_Physics_Integrated_Gaussian_Splatting_d7901a6ed2cd.pdf]]
