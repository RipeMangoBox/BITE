---
title: "SeeU: Seeing the Unseen World via 4D Dynamics-aware Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SeeU_Seeing_the_Unseen_World_via_4D_Dynamics_aware_Generation.pdf
project_link: "https://yuyuanspace.com/SeeU/"
code_link: null
aliases:
- S242
- SeeU
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 显式地将动态场景重建为4D表示（3D+时间），并在连续时间上学习物理一致的动力学（解耦相机与前景、施加平滑/物理先验），以此作为控制生成内容的结构支架。
primary_logic: 在原生4D空间中建模连续动力学，可以显式解耦相机、前景和背景，并通过物理先验（如B-spline平滑性、加速度惩罚）实现任意时间/视角的插值和外推，为视频生成提供几何与运动骨架，再借助上下文修复能力填充外观细节。
claims:
- 直接在2D投影中建模动态会损失3D结构、时间关联和物理规律，而在4D世界中这些量可以简洁、自然地描述。
- 通过B-spline参数化连续动力学并施加物理损失（二阶导数惩罚），显著提升时间平滑性和外推稳定性。
- SeeU在未见时间生成（过去、插值、未来）的PSNR/SSIM/LPIPS上显著优于现有插值/预测/生成基线。
- SeeU在未见空间生成（相机移动、遮挡恢复）的EE/EIR/CLIP-V上超越相机可控视频生成模型。
---

# SeeU: Seeing the Unseen World via 4D Dynamics-aware Generation

> [!tip] 核心洞察
> 在原生4D空间中建模连续动力学，可以显式解耦相机、前景和背景，并通过物理先验（如B-spline平滑性、加速度惩罚）实现任意时间/视角的插值和外推，为视频生成提供几何与运动骨架，再借助上下文修复能力填充外观细节。

| 字段 | 内容 |
|------|------|
| 中文题名 | SeeU：基于4D动力学感知生成看见不可见世界 |
| 英文题名 | SeeU: Seeing the Unseen World via 4D Dynamics-aware Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.03350) · [Project](https://yuyuanspace.com/SeeU/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | SeeU (2D→4D→2D 框架) |
| Dataset | SeeU45 - Temporal: Past, SeeU45 - Temporal: Interpolation, SeeU45 - Temporal: Future, SeeU45 - Spatial: Dolly Out |

> [!tip] 效果简介
> - SeeU45 - Temporal: Past (6.67%) 上，PSNR 20.47 vs 15.55 (SoM) (+4.92)。
> - SeeU45 - Temporal: Interpolation 上，PSNR 21.07 vs 20.54 (InterpAny) (+0.53)。
> - SeeU45 - Temporal: Future (6.67%) 上，PSNR 20.54 vs 20.07 (Cosmos) (+0.47)。

## 概要

从稀疏的2D单目视频帧中理解并生成动态场景的未见世界，是计算机视觉与生成模型的一个核心挑战。其根本瓶颈在于：**2D投影天然丢失了3D几何信息，且相机运动与场景运动在像素空间中高度纠缠**，使得直接从2D数据学习视频生成难以保证物理一致性和跨视角泛化能力（Figure 2）。

**SeeU** 针对这一瓶颈提出了一个 **2D→4D→2D** 的三阶段生成框架。其核心洞察是：在原生4D空间（3D空间+时间）中显式建模连续动力学，可以自然解耦相机、前景和背景运动，并通过物理先验实现任意时间/视角的插值与外推，从而为视频生成提供几何与运动骨架。具体而言，SeeU 首先从稀疏单目帧重建包含前景高斯和相机轨迹的4D动态场景表示；随后通过低秩运动基与B-spline参数化学习连续时间的4D动力学，并施加加速度惩罚等物理约束以确保平滑性和外推稳定性；最后将演化的4D场景重投影为2D骨架，借助时空上下文视频修复能力填充外观细节（Figure 3）。

在方法谱系上，SeeU 区别于端到端2D视频生成模型（如 **Wan 2.2**、**Cosmos Predict2.5**）和纯2D帧插值/预测方法（如 **InterpAny**（Zhong et al., ECCV 2024）），其关键不同在于将**动态建模域从2D像素空间提升至4D表示空间**，并引入**显式物理约束**与**连续时间参数化**。与已有的4D-aware方法（如 **Shape-of-Motion (SoM)**、**DaS**、**HunyuanWorld-Voyager**）相比，SeeU 的连续动力学模型和物理损失使其在时间外推的平滑性和空间生成的几何一致性上具有显著优势。

主要实验结果验证了这一设计的有效性：
- **时间维度**：在 SeeU45 基准上，SeeU 在未见过去帧生成（PSNR 20.47 vs SoM 15.55）、中间帧插值（PSNR 21.07 vs InterpAny 20.54）和未来帧预测（PSNR 20.54 vs Cosmos 20.07）上均取得最优或次优结果（Table 1）。
- **空间维度**：在相机移动场景下，SeeU 在极线误差（EE 0.200 vs ReCamMaster 0.238）、极线内点率（EIR 0.785 vs ReCamMaster 0.674）和场景语义一致性（CLIP-V 0.969 vs ReCamMaster 0.937）上全面超越相机可控生成基线（Table 2）。
- **消融实验**证实：B-spline 参数化相比 MLP 显著提升时间平滑性（PSNR 21.08→17.54），物理损失移除导致帧一致性下降（PSNR 21.08→19.36），验证了连续动力学和物理先验的关键作用（Table 3）。

SeeU 的主要局限在于依赖上游几何模块（相机位姿估计、跟踪、深度预测）的质量，对纹理稀疏或薄结构的场景性能下降（Figure 9），且在极端快速运动或多物体交互场景下仍可能产生伪影（Figure 10）。这些限制指出了未来在提升上游模块鲁棒性和处理更复杂动态方面的研究方向。

### 问题背景：从2D投影理解动态世界的根本困难

人类视觉系统天然具备从稀疏的2D视网膜投影中推断三维结构和运动的能力。然而，对于当前的计算机视觉模型而言，从单目2D视频帧中恢复精确的3D几何与物理轨迹仍然极具挑战性。这一困难的核心根源在于**投影过程的本质信息损失**——当三维世界被投影到二维图像平面时，深度信息、遮挡关系以及场景的完整空间结构都被不可逆地压缩了。

更关键的是，在动态场景中，**相机运动与场景运动彼此纠缠**。一个像素在连续帧之间的位移可能同时来源于相机自身的移动和场景中物体的独立运动，而2D投影本身无法自动区分这两种运动来源。这种纠缠使得直接从2D像素变化中学习准确的3D几何和物理轨迹变得异常困难，尤其在遮挡、非刚体变形和新视角等情况下，模型的泛化能力会受到严重制约。

### 现有方法的缺口：缺乏显式4D世界建模

当前主流的视频生成和动态场景建模方法大多在**2D像素或特征空间**中操作。无论是基于Transformer、MLP还是Mamba架构的模型，它们通常采用端到端的方式直接从2D输入学习像素变化，缺乏对底层3D结构和物理规律的显式建模。这种“黑箱”式的学习范式存在三个关键缺陷：

1. **3D感知缺失**：在2D空间中建模动态无法自然地表达场景的三维几何结构，导致模型在需要3D推理的任务（如新视角合成、遮挡区域恢复）中表现不佳。
2. **物理一致性缺失**：纯数据驱动的方法没有内置的物理约束，生成的运动轨迹可能违反基本的运动学规律，表现为时间上的不连续或物理上的不合理。
3. **运动纠缠未解耦**：相机运动、前景运动、背景运动在2D投影中高度耦合，模型难以独立控制或编辑其中任一成分。

### 核心动机：在原生4D空间中建模连续动力学

SeeU的核心洞察在于：**在4D世界（3D空间+时间）中，上述被2D投影所掩盖的量可以被显式、简洁且优雅地描述**。具体而言：

- **3D几何**在4D坐标系中可以自然地表示为规范空间中的高斯原语及其随时间的刚体变换，无需通过2D线索间接推断。
- **物理轨迹**可以通过对运动参数的平滑性约束（如加速度惩罚）来显式施加，而非依赖数据隐式学习。
- **运动解耦**可以在统一的4D坐标系中将相机、前景和背景的运动分量显式分离，实现独立建模与控制。

基于这一动机，SeeU提出了一种**2D→4D→2D**的全新学习框架：首先从稀疏的单目2D帧重建4D动态场景表示，随后在连续时间上学习物理一致的4D动力学（通过低秩运动基和B-spline参数化），最后将习得的4D世界演化并重投影为2D骨架，借助时空上下文修复能力填充外观细节。这一设计使得模型能够生成任意时间点和任意视角下的未见世界，同时保持物理上合理的运动和一致的3D几何结构。

### 方法定位：统一框架下的多任务覆盖

值得注意的是，现有方法通常仅针对特定子任务设计：例如**InterpAny**（Zhong et al., ECCV 2024）仅支持视频帧插值，**Cosmos Predict2.5**仅支持未来帧预测，而**ReCamMaster**（Bai et al., ICCV 2025）和**GCD**则专注于相机可控的视频生成。SeeU的目标是在一个统一的4D动力学框架下，同时覆盖过去重建、中间插值、未来预测以及新视角生成等全时间范围和全空间范围的任务，从而实现对动态场景的更完整理解与生成能力。

## 核心方法与创新机理

SeeU的核心创新在于提出了一套**2D→4D→2D的动力学感知生成框架**，从稀疏单目2D帧中显式地学习连续4D动态世界，并以此为结构支架生成未见时间与视角的2D内容。该框架的根本动机在于：直接从2D投影学习视频生成会丢失3D几何与物理一致性，相机和场景运动彼此纠缠，导致模型在遮挡、非刚体变形、新视角等情况下泛化能力差（Figure 2）。SeeU通过将动态建模从2D像素空间提升至4D原生空间，从根本上解耦了相机、前景与背景，并施加物理先验以确保运动的平滑性与可外推性。

### 关键改变槽位

SeeU相对于现有基线的方法差异可归纳为以下四个关键改变槽位：

| 改变槽位 | 基线做法 | SeeU做法 | 证据 |
|---------|---------|---------|------|
| **动态建模域** | 2D像素/特征空间，直接从视频学习像素变化 | 4D（3D空间+时间）表示，显式重建动态场景并学习连续动力学 | Section 2, Section 4.1–4.2 |
| **运动表示与学习** | 隐式端到端学习（Transformer/MLP/Mamba），无显式运动参数化 | 低秩运动基 $\mathbf{P}_t^i = \mathbf{P}_0^i + \mathbf{B}(t)\mathbf{w}_i$ + B-spline连续时间函数（C4DD），共享基+控制点优化 | Section 4.3, Eq. (3)–(4) |
| **物理约束** | 无显式物理约束，仅依赖数据驱动 | 物理损失 $\mathcal{L}_{\mathrm{phys}}$：对运动基和相机轨迹的二阶导数施加惩罚，外推区间权重更大 | Section 4.3, Eq. (7) |
| **生成流程** | 直接从2D输入到2D输出（端到端生成或预测） | 2D→4D重建 → 连续4D动力学 → 4D→2D重投影 + 时空上下文视频修复 | Section 1, Section 4.4, Figure 3 |

### 创新机制分析

**1. 4D原生建模与运动解耦。** 现有方法（如**InterpAny**（Zhong et al., ECCV 2024）、**Cosmos Predict2.5**、**Wan 2.2**）在2D像素空间直接学习运动模式，相机运动与场景运动无法分离，导致新视角或遮挡情形下几何一致性差。SeeU在统一的4D坐标系中显式表示相机、前景和背景，从源头上消除了运动纠缠。这是性能提升的根本因果机制——当相机和前景运动被解耦后，模型可以独立地外推相机轨迹或前景动态，而不受另一方的干扰。

**2. 低秩B-spline连续动力学。** SeeU的连续4D动力学模型（C4DD）采用低秩运动基 $\mathbf{B}(t)$ 与B-spline参数化，将离散帧的4D重建扩展为连续时间函数。与隐式MLP相比，B-spline的平滑性归纳偏置天然适合物理运动建模。消融实验（Table 3）表明：将B-spline替换为MLP后，PSNR从21.08骤降至17.54，证实了样条先验对时间平滑性的关键作用（Figure 7, Figure 8）。低秩分解则大幅降低了参数规模，使连续动力学学习在计算上可行。

**3. 物理损失驱动可外推性。** C4DD的训练目标 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{data}} + \lambda_{\mathrm{phys}} \mathcal{L}_{\mathrm{phys}}$ 中，物理损失对运动基和相机轨迹的平移/旋转加速度施加L2惩罚，且在外推时间区间赋予更高权重。这一设计使得模型不仅在观测帧区间内拟合数据，更在未见时间区间上保持平滑、物理合理的运动。移除物理损失（$\lambda_{\mathrm{phys}}=0$）导致PSNR从21.08降至19.36（Table 3），帧一致性显著下降，验证了物理先验对外推稳定性的决定性贡献。

**4. 4D骨架引导的2D生成。** 与端到端2D生成不同，SeeU将习得的连续4D场景演化并重投影为2D骨架帧，再利用时空上下文视频生成器（微调的**VACE**）修复缺失或不确定区域。这种“结构先行、外观后补”的策略将几何一致性交给显式的4D渲染管线保证，而将外观细节交给生成模型的上下文修复能力填充，实现了几何精度与视觉质量的解耦优化。

### 证据强度评估

上述创新点的证据强度总体较高：核心改变槽位均有明确的公式、消融实验和可视化支撑（Table 3, Figure 7, Figure 8）。与基线的定量对比（Table 1, Table 2）覆盖了时间维度（过去/插值/未来）和空间维度（Dolly/Tilt/Pan）的多个指标，且SeeU在几乎所有设置下均取得最优或次优结果。值得注意的是，某些基线仅针对特定子任务（如InterpAny仅支持插值，Cosmos仅支持未来预测），而SeeU在统一框架下覆盖全时间范围，这一泛化能力本身也体现了4D建模范式的优势。

SeeU 遵循一个 **2D→4D→2D** 的三阶段学习框架，其核心创新在于将动态场景的建模从2D像素空间显式提升到4D（3D空间+时间）表示空间，从而解耦相机运动、前景运动和背景结构，并在连续时间上学习物理一致的动力学。

### 三阶段流水线

如 Figure 3 所示，整个系统由三个顺序衔接的阶段构成：

![[assets/figures/papers/paper_list_l2593_https_arxiv_org_abs_2512_03350/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline of SeeU. (a) A dynamic scene is lifted into a 4D representation. (b) Continuous 4D dynamics are learned efficiently with physical and smoothness priors. (c) The learned dynamics evolve the 4D world, which is re-projected to 2D at unseen times and viewpoints; a spatial–temporal in-context video generator completes the unobserved or uncertain areas*

1. **2D→4D 动态场景重建（Stage 1）**：从稀疏的单目2D帧出发，利用 MegaSaM 估计相机内参、外参和逐帧深度，结合 Track-Anything 分割前景运动物体、TAPIR 提取2D点轨迹，最终将场景提升为一个包含前景3D高斯（3D Gaussians）和相机轨迹的4D表示。每个规范高斯 $g_0^i$ 由位置 $\mu_0^i$、朝向 $\mathbf{R}_0^i$、尺度 $\mathbf{s}^i$、不透明度 $o^i$ 和颜色 $\mathbf{c}^i$ 参数化，并通过逐帧 SE(3) 刚性变换演化到各时间步。

2. **离散4D→连续4D 动力学学习（Stage 2）**：在重建得到的离散时间4D表示之上，引入 **Continuous 4D Dynamics Model (C4DD)**。该模块采用低秩运动基参数化——前景高斯属性表示为初始状态加上共享运动基 $\mathbf{B}(t)$ 与每高斯系数 $\mathbf{w}_i$ 的乘积：$\mathbf{P}_t^i = \mathbf{P}_0^i + \mathbf{B}(t) \mathbf{w}_i$。运动基通过可学习的 B-spline 控制点 $\mathbf{q}_j$ 和基函数 $N_{j,d}(t)$ 在连续时间上计算：$\hat{\mathbf{B}}_t = \sum_{j=1}^M N_{j,d}(t) \mathbf{q}_j$。训练时同时优化数据保真项和物理正则化项 $\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{data}} + \lambda_{\text{phys}} \mathcal{L}_{\text{phys}}$，其中物理损失对运动基和相机轨迹的平移/旋转加速度施加二阶导数惩罚，外推区间权重更高。

3. **4D→2D 时空上下文生成（Stage 3）**：习得的连续4D动力学驱动场景演化，并在未见时间和视点处重投影为2D骨架帧。随后，一个时空上下文视频生成器（基于微调的 VACE）接收三类上下文先验——VLM 生成的场景语义提示、重投影帧、以及修复遮罩——通过 Context Encoder 注入预训练视频生成器，填充未观测或不确定区域，输出最终的2D视频内容。

### 输入输出流

- **输入**：一段稀疏的单目2D视频帧序列。
- **中间表示**：包含前景3D高斯和相机轨迹的4D重建，以及由 C4DD 习得的连续时间动力学函数。
- **输出**：在未见时间（过去、中间插值、未来）和未见空间（相机平移、倾斜等）下生成的2D视频帧，保持3D几何一致性和物理合理运动。

### 模块间的依赖关系

Stage 1 为 Stage 2 提供初始的离散4D表示（相机位姿、前景高斯属性），Stage 2 在此基础上学习连续动力学，Stage 3 则依赖 Stage 2 输出的演化后4D场景进行重投影和视频修复。三个阶段的训练顺序进行，上游模块的质量直接影响下游性能——例如，Stage 1 的相机估计和前景分割精度决定了 C4DD 可学习的运动空间上限，而 C4DD 的平滑性和外推能力又约束了 Stage 3 生成内容的几何一致性。

### 2D→4D 动态场景重建

SeeU 的第一阶段将稀疏单目 2D 帧提升为显式 4D 表示。该模块依赖三个上游组件协作完成场景重建：**MegaSaM** 估计相机内参、外参与逐帧深度，**Track-Anything** 分割运动前景目标，**TAPIR** 提取 2D 点跟踪轨迹。在此基础上，场景被建模为一组规范 3D 高斯（canonical Gaussians），每个高斯的参数化为：

$$g _ { 0 } ^ { i } = ( \mu _ { 0 } ^ { i } , { \bf R } _ { 0 } ^ { i } , { \bf s } ^ { i } , o ^ { i } , { \bf c } ^ { i } )$$

其中 $\mu_0^i$ 为位置，$\mathbf{R}_0^i$ 为朝向，$\mathbf{s}^i$ 为尺度，$o^i$ 为不透明度，$\mathbf{c}^i$ 为颜色。高斯从规范帧到时刻 $t$ 的演化通过 SE(3) 刚性变换实现：

$$\pmb { \mu } _ { t } ^ { i } = \mathbf { R } _ { 0 t } \pmb { \mu } _ { 0 } ^ { i } + \mathbf { t } _ { 0 t } , \quad \mathbf { R } _ { t } ^ { i } = \mathbf { R } _ { 0 t } \mathbf { R } _ { 0 } ^ { i }$$

这一阶段的核心产出包括：前景高斯的逐帧属性序列和相机轨迹的离散估计，为后续连续动力学学习提供初始骨架。

### 连续 4D 动力学模型（C4DD）

第二阶段将离散重建转化为连续时间动力学，这是 SeeU 实现任意时刻插值与外推的关键模块。其设计围绕三个相互配合的机制展开。

**低秩运动参数化。** 为高效建模前景运动，C4DD 采用低秩运动基表示。对任意前景高斯 $i$ 在时刻 $t$ 的属性 $\mathbf{P}_t^i$，有：

$$\mathbf{P}_t^i = \mathbf{P}_0^i + \mathbf{B}(t) \mathbf{w}_i$$

其中 $\mathbf{P}_0^i$ 为初始属性，$\mathbf{B}(t)$ 是所有高斯共享的运动基函数，$\mathbf{w}_i$ 为每高斯的系数向量。该设计将高维运动空间压缩至低秩流形，显著降低参数量。

**B-spline 连续时间函数。** 运动基 $\mathbf{B}(t)$ 通过 B-spline 参数化实现连续时间上的平滑预测：

$$\hat{\mathbf{B}}_t = \sum_{j=1}^M N_{j,d}(t) \mathbf{q}_j$$

其中 $\mathbf{q}_j$ 为可学习控制点，$N_{j,d}(t)$ 为 $d$ 阶 B 样条基函数。论文采用三次 B 样条（$d=3$），设置 8 个控制点。B-spline 的局部支撑性和固有平滑性为连续动力学提供了强归纳偏置——消融实验中将其替换为 MLP 后，PSNR 从 21.08 骤降至 17.54（Table 3），且运动基的时间平滑性显著恶化（Figure 7、Figure 8）。

![[assets/figures/papers/paper_list_l2593_https_arxiv_org_abs_2512_03350/figures/012_Figure_8.jpg]]
*Figure 8: Visual comparison on C4DD Architectures. The C4DD with spline constrains (a) has better smoothness and physical consistency (both camera pose and foreground dynamics)*

**物理损失。** C4DD 的训练目标由数据保真项与物理正则化项组成：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{data}} + \lambda_{\mathrm{phys}} \mathcal{L}_{\mathrm{phys}}$$

其中 $\lambda_{\mathrm{phys}} = 1 \times 10^{-4}$。物理损失对运动基和相机轨迹的加速度施加 L2 惩罚：

$$\mathcal{L}_{\mathrm{phys}} = \mathbb{E}_{\tau_{\mathrm{ex}}(t)} \Big[ \| \operatorname{\ddot{M}B}_{\mathrm{trans}}(t) \|_2^2 + \| \mathrm{C}\tilde{\mathrm{am}}_{\mathrm{trans}}(t) \|_2^2 + \mathbb{I}_{\mathrm{rot}} \| \mathrm{C}\tilde{\mathrm{am}}_{\mathrm{rot}}(t) \|_2^2 \Big]$$

该损失在三个层面施加约束：(1) 运动基平移分量的二阶导数 $\operatorname{\ddot{M}B}_{\mathrm{trans}}(t)$；(2) 相机轨迹平移加速度 $\mathrm{C}\tilde{\mathrm{am}}_{\mathrm{trans}}(t)$；(3) 由指示函数 $\mathbb{I}_{\mathrm{rot}}$ 控制的相机旋转加速度 $\mathrm{C}\tilde{\mathrm{am}}_{\mathrm{rot}}(t)$。关键设计在于期望 $\mathbb{E}_{\tau_{\mathrm{ex}}(t)}$ 在**外推时间区间**施加更高权重，使模型在未见时间段仍保持物理一致性。消融实验证实：移除物理损失（$\lambda_{\mathrm{phys}}=0$）后 PSNR 从 21.08 降至 19.36（Table 3），帧间一致性明显退化。

### 4D→2D 时空上下文修复生成

第三阶段将习得的连续 4D 场景在目标时刻和视角下重投影为 2D 骨架帧，并生成对应的修复遮罩（inpainting mask）以标记未观测或不确定区域。随后，一个微调的 **VACE** 视频生成器接收三类上下文先验完成修复：(1) 由 VLM 提取的场景语义描述作为结构化提示；(2) 重投影帧作为视觉锚点；(3) 修复遮罩界定生成区域。Context Encoder 将这些先验编码为上下文嵌入并注入预训练视频生成器，最终输出时空一致的完整视频帧。这一设计使得 4D 骨架负责几何与运动一致性，而视频生成器仅需填充外观细节，实现了结构控制与外观生成的解耦。

## 实验与关键发现

### 评估设置与基准

为全面评估SeeU在未见世界生成上的能力，作者构建了**SeeU45数据集**（Table 4），包含45个覆盖室内外、物体、人体、动物等多样场景的视频序列，每个场景提供首尾各6.67%时长作为外推测试区间，中间帧用于插值评估。空间维度评估则通过施加推拉（Dolly）、平移（Pan）、俯仰（Tilt）等相机运动来测试新视角生成质量。

![[assets/figures/papers/paper_list_l2593_https_arxiv_org_abs_2512_03350/figures/010_Table_4.jpg]]
*Table 4: Statistics of the SeeU45 dataset*

评估指标涵盖三个层面：
- **像素保真度**：PSNR、SSIM、LPIPS，以及专门设计的C-LPIPS（需接近参考值而非越低越好）；
- **3D几何一致性**：对极误差（EE，式10的Sampson近似）和对极内点率（EIR，式11），无需相机内参即可衡量生成视图与参考视图的几何对齐程度；
- **语义一致性**：CLIP-V，度量场景级视觉语义保持度。

对比基线按任务类型分组：时间维度包括帧插值方法**InterpAny**（Zhong et al., ECCV 2024）、图像到视频生成模型**Wan 2.2**、未来预测模型**Cosmos Predict2.5**、4D重建与外推方法**Shape-of-Motion (SoM)**；空间维度包括相机可控生成模型**ReCamMaster**（Bai et al., ICCV 2025）和**GCD**；4D感知生成方法**DaS**和**HunyuanWorld-Voyager**。所有方法均在单张NVIDIA A100 (80GB) GPU上训练，使用Adam优化器。

### 时间维度生成：全时间跨度统一建模

Table 1汇总了未见时间生成的核心结果。SeeU在**过去外推**（PSNR 20.47 vs SoM 15.55，+4.92）、**中间插值**（PSNR 21.07 vs InterpAny 20.54，+0.53）和**未来外推**（PSNR 20.54 vs Cosmos 20.07，+0.47）三个子任务上均取得最优。关键发现：

1. **外推优势显著**：过去外推的增益（+4.92 PSNR）远大于插值（+0.53），说明显式4D动力学建模在外推场景中具有决定性优势——2D方法因缺乏3D结构先验，在远离观测区间时迅速崩溃，而SeeU通过B-spline参数化的连续运动基和物理损失约束，能够稳定外推。

2. **统一框架 vs 专用模型**：InterpAny仅支持插值，Cosmos仅支持未来预测，而SeeU以单一框架覆盖全时间范围，且在各子任务上均超越专用模型。这验证了核心洞察：在4D空间中建模连续动力学天然支持任意时间的查询。

3. **C-LPIPS的参考对齐**：SeeU的C-LPIPS值最接近参考值，表明生成内容的感知特征分布与真实序列一致，而非简单的像素级拟合。

Figure 4的定性对比进一步揭示：SoM的线性外推在复杂运动下产生明显漂移，InterpAny在遮挡区域产生模糊，而SeeU保持了物体的刚体结构和运动轨迹的物理合理性。

Figure 5的误差分析展示了预测误差随时间距离的变化趋势：SeeU的误差增长曲线明显平缓于基线，且在外推边界处未出现突变，验证了B-spline连续参数化和物理损失对外推稳定性的贡献。

### 空间维度生成：3D几何一致性的突破

Table 2报告了未见空间生成的定量结果。在推拉（Dolly Out）任务上，SeeU相比最强基线ReCamMaster在三个指标上全面领先：EE降低至0.200（-0.038，越低越好），EIR提升至0.785（+0.111），CLIP-V达到0.969（+0.032）。在Dolly Right、Dolly Up、Tilt Up、Pan Right等其他相机运动类型上，SeeU同样保持一致的领先。

EE和EIR的改善尤为关键：这两个指标直接度量生成视图与参考视图之间的对极几何约束满足程度，低EE和高EIR意味着SeeU生成的像素级内容在3D空间中是几何一致的，而非仅靠2D纹理拼凑。这归因于框架的因果链路——4D重建提供了显式的3D几何支架，连续动力学保证了相机和前景的解耦演化，重投影后的2D骨架为视频生成器提供了精确的空间引导。

Figure 6的定性结果展示了SeeU在相机大幅移动时仍能保持场景结构的稳定性，而ReCamMaster在遮挡边界处出现几何断裂和纹理撕裂。

### 4D感知模型对比

Table 5将SeeU与同为4D-aware的DaS和HunyuanWorld-Voyager进行对比。SeeU在EIR（0.802 vs DaS 0.762）和CLIP-V（0.959 vs DaS 0.925）上均占优，表明其4D动力学学习策略优于直接生成4D表示的方法。差异的核心在于：SeeU将4D重建与连续动力学学习解耦，使得动力学模型可以专注于运动规律本身，而非同时承担重建和生成的双重负担。

### 消融实验：架构选择与物理先验

Table 3的系统消融揭示了三个关键设计的作用：

**B-spline vs MLP（C4DD架构）**：将B-spline运动基替换为MLP后，PSNR从21.08骤降至17.54，SSIM从0.552降至0.459。Figure 7和Figure 8直观展示了原因：MLP学习的运动基在时间轴上出现高频抖动，缺乏平滑性，导致相机轨迹和前景运动均产生物理不合理的震荡。B-spline通过可学习控制点和基函数的显式平滑性归纳偏置，天然约束了运动的连续性和可微性。

**物理损失的作用**：移除物理损失（λ_phys=0）导致PSNR下降至19.36，EE从0.197升至0.224，CLIP-V从0.960降至0.920。这表明仅靠数据保真项无法保证外推区间的运动合理性——物理损失通过对运动基和相机轨迹的二阶导数施加惩罚（式7），强制模型学习符合物理规律的平滑运动，尤其在外推区间（τ_ex(t)权重更高）效果显著。

**输入帧数的影响**：从5帧增加到10帧带来明显增益（PSNR +1.32），10帧到20帧收益趋缓（+0.46），表明SeeU能够有效利用稀疏观测，且10帧左右已能捕获场景的核心动力学模式。

### 失败模式与局限性

Figure 9展示了SeeU的典型失败案例：当输入视频包含**薄结构**（如细杆、绳索）或**缺乏纹理**的区域时，生成质量明显下降。这反映了上游模块的固有局限——MegaSaM的深度估计和TAPIR的点跟踪在无纹理区域失效，导致4D重建不完整，进而影响动力学学习和最终生成。

Figure 10的鲁棒性评估显示，在极端快速运动、多物体交互和人群等复杂场景下，SeeU仍可能产生局部伪影。当前方法假设前景运动平滑且可被低秩基表示，对于突然的速度变化或非刚体变形，该假设可能不成立。

更根本的局限性在于：SeeU的2D→4D重建阶段依赖单目视频，仅能处理有限的视角变化，对于大范围遮挡恢复缺乏多视角信息的补充。此外，框架尚未扩展到长时间视频或多场景交互的动态建模。

![[assets/figures/papers/paper_list_l2593_https_arxiv_org_abs_2512_03350/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison on unseen spatial generation. Lower Epipolar Error (EE) and higher Epipolar Inlier Ratio (EIR) indicate better 3D geometric consistency, and higher CLIP-V refers to higher scene consistency*

![[assets/figures/papers/paper_list_l2593_https_arxiv_org_abs_2512_03350/figures/004_Figure_4.jpg]]
*Figure 4: Visual comparisons on unseen temporal generation. SeeU supports continuous-time generation across the entire time span ( past – between – future ), yielding more physically plausible motion and stronger geometric consistency*

![[assets/figures/papers/paper_list_l2593_https_arxiv_org_abs_2512_03350/figures/009_Figure_6.jpg]]
*Figure 6: Visual comparisons on unseen spatial generation. SeeU exhibits strong 3D awareness and scene consistency*

## 定位与知识库关联

### 1. 问题定位：从2D生成到4D动力学感知

现有视频生成与预测方法主要在2D像素或特征空间建模动态变化，其核心瓶颈在于：**2D投影过程不可逆地丢失了3D几何信息，且相机运动与场景运动在像素空间中彼此纠缠**（见 Figure 2）。这一根本性限制导致模型在以下场景中泛化能力不足：（1）遮挡区域的恢复；（2）非刚体变形的物理一致性；（3）新视角下的几何稳定性。SeeU 的核心洞察在于：**在原生4D空间（3D+时间）中，相机、前景和背景的运动可以被显式解耦，物理规律（如平滑性、加速度约束）可以被自然地施加**，从而为视频生成提供几何与运动骨架。

### 2. 方法谱系中的位置

SeeU 的 2D→4D→2D 框架处于以下研究脉络的交汇点：

**（1）相对于4D动态场景重建方法**

SeeU 的第一阶段（2D→4D）继承了基于3D Gaussian Splatting的动态重建管线。与 **Shape-of-Motion (SoM)** 类似，SeeU 采用低秩运动基参数化前景高斯运动（$\mathbf{P}_t^i = \mathbf{P}_0^i + \mathbf{B}(t) \mathbf{w}_i$），但关键区别在于：
- SoM 仅对观测时间窗口内的运动进行线性外推，缺乏对连续时间动力学的显式建模；
- SeeU 引入 **Continuous 4D Dynamics Model (C4DD)**，通过 B-spline 参数化运动基（$\hat{\mathbf{B}}_t = \sum_{j=1}^M N_{j,d}(t) \mathbf{q}_j$）实现连续时间上的平滑动力学学习，并施加物理损失 $\mathcal{L}_{\mathrm{phys}}$ 对运动基和相机轨迹的二阶导数进行惩罚，从而在插值和外推任务上获得显著提升（PSNR 从 SoM 的 15.55 提升至 20.47，Table 1）。

**（2）相对于视频帧插值与预测方法**

传统视频帧插值方法（如 **InterpAny** (Zhong et al., ECCV 2024)）和未来帧预测方法（如 **Cosmos Predict2.5**、**Wan 2.2**）直接在2D域操作，缺乏对3D几何和物理约束的显式建模。SeeU 在未见时间生成任务上全面超越这些基线：
- 过去外推：PSNR 20.47 vs SoM 15.55（+4.92）
- 中间插值：PSNR 21.07 vs InterpAny 20.54（+0.53）
- 未来预测：PSNR 20.54 vs Cosmos 20.07（+0.47）

值得注意的是，上述基线各自仅能处理特定子任务（插值或预测），而 SeeU 在统一框架下覆盖全时间范围。

**（3）相对于相机可控视频生成方法**

**ReCamMaster** (Bai et al., ICCV 2025) 和 **GCD** 等相机可控生成方法通过条件控制实现新视角合成，但仍缺乏对场景3D几何的显式重建。SeeU 在未见空间生成任务上的优势体现在几何一致性指标上：
- Dolly Out 场景：EE 0.200 vs ReCamMaster 0.238（↓16%），EIR 0.785 vs 0.674（↑16.5%），CLIP-V 0.969 vs 0.937

这表明4D动力学骨架为生成内容提供了更强的3D几何约束。

**（4）相对于4D-aware生成方法**

与 **DaS** 和 **HunyuanWorld-Voyager** 等4D-aware方法相比，SeeU 在 EIR（0.802 vs 0.762）和 CLIP-V（0.959 vs 0.925）上均取得领先（Table 5）。SeeU 的差异化优势在于显式的物理先验（B-spline平滑性 + 加速度惩罚）和连续时间动力学建模，而非仅依赖数据驱动的隐式学习。

### 3. 关键技术决策的消融证据

SeeU 的设计选择得到了充分的消融实验验证（Table 3）：

| 消融变量 | PSNR | SSIM | LPIPS | EE | CLIP-V |
|---------|------|------|-------|-----|--------|
| Ours (20 frames) | 21.08 | 0.552 | 0.239 | 0.197 | 0.960 |
| C4DD w/ MLP | 17.54 | 0.474 | 0.317 | 0.282 | 0.897 |
| w/o physics loss | 19.36 | 0.527 | 0.274 | 0.224 | 0.920 |

**关键发现**：
- **B-spline vs MLP**：将 B-spline 替换为 MLP 导致 PSNR 下降 3.54，时间平滑性和物理一致性显著恶化（见 Figure 7、Figure 8）。这验证了 B-spline 的归纳偏置对连续动力学建模的重要性。
- **物理损失的作用**：移除 $\mathcal{L}_{\mathrm{phys}}$ 使 PSNR 下降 1.72，EE 上升 13.7%，证明加速度惩罚对维持外推稳定性的关键作用。
- **输入帧数敏感性**：5→10 帧提升显著，10 帧以上收益趋缓，表明方法在稀疏输入下已能有效工作。

### 4. 适用边界与局限

**上游依赖与输入要求**：
SeeU 的性能受限于上游几何模块（MegaSaM 相机估计、TAPIR 跟踪、Track-Anything 分割）的质量。这要求输入视频具有**显著的前景目标**和**充足的空间纹理细节**。对于前景极小、缺乏纹理或包含薄结构的场景，输出质量会下降（Figure 9）。

**运动假设的限制**：
当前方法侧重于平滑、时间稳定的前景运动。在以下场景中可能产生伪影（Figure 10）：
- 极端快速的运动
- 多物体复杂交互
- 密集人群场景
- 频繁遮挡与非刚体变形

**视角变化范围**：
2D→4D 重建阶段仅适用于有限的视角变化。对于大基线多视角输入，当前框架的4D重建完整性和准确性需要进一步增强。

### 5. 开放问题

1. **长时序与多场景扩展**：如何将框架扩展到长时间视频或多场景交互的更复杂动态，而不导致误差累积？

2. **非平滑运动建模**：当前物理先验假设平滑运动，如何处理更普遍的非刚体变形和频繁遮挡情形（如碰撞、断裂等不连续事件）？

3. **多视角融合**：如何有效融合多视角输入以增强4D重建的完整性和准确性，特别是在遮挡区域的几何恢复？

4. **计算效率**：三阶段流水线的推理效率是否满足实时或近实时应用需求？是否存在端到端联合优化的可能性？

5. **与基础模型的深度整合**：当前4D→2D阶段依赖微调的视频生成器（VACE）进行上下文修复。是否存在更紧密的整合方式，使4D动力学直接指导扩散模型的去噪过程？

## 原文 PDF

![[paperPDFs/CVPR_2026/SeeU_Seeing_the_Unseen_World_via_4D_Dynamics_aware_Generation.pdf]]
