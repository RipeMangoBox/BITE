---
title: "ZeroHSI: Zero-Shot 4D Human-Scene Interaction by Video Generation"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/ZeroHSI_Zero_Shot_4D_Human_Scene_Interaction_by_Video_Generation.pdf
project_link: https://awfuact.github.io/zerohsi
code_link: null
aliases:
- ZeroHSI
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 从大规模预训练的视频生成模型中提取人景交互先验，并通过可微渲染将2D视频提升为4D交互运动。
primary_logic: 利用视频生成模型学到的丰富人体运动与环境交互知识，结合可微神经渲染优化，绕过对配对动作-场景数据的需求，实现零样本交互合成。
claims:
- ZeroHSI 通过集成视频生成和可微渲染，无需任何动捕数据即可合成4D人景交互。
- ZeroHSI 在静态场景交互上显著优于基线 TRUMANS 和 LINGO，尤其在场景穿透率上大幅降低。
- 消融实验表明完整的逐帧身体优化（OPT_body）对减少场景穿透至关重要。
- AnyInteraction (static) 上 CLIP Score = 23.52
---

# ZeroHSI: Zero-Shot 4D Human-Scene Interaction by Video Generation

> [!tip] 核心洞察
> 利用视频生成模型学到的丰富人体运动与环境交互知识，结合可微神经渲染优化，绕过对配对动作-场景数据的需求，实现零样本交互合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | ZeroHSI：通过视频生成的零样本四维人景交互 |
| 英文题名 | ZeroHSI: Zero-Shot 4D Human-Scene Interaction by Video Generation |
| 会议/期刊 | arXiv 2024 |
| Links | [Project](https://awfuact.github.io/zerohsi) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | ZeroHSI |
| Dataset | AnyInteraction |

> [!tip] 效果简介
> - AnyInteraction (static) 上，CLIP Score 23.52 vs TRUMANS 22.36 (+1.16)；CLIP Score 23.52 vs LINGO 22.61 (+0.91)；Pene%_scene 0.019 vs TRUMANS 0.046 (-0.027)。
> - AnyInteraction (dynamic) 上，CLIP Score 24.01 vs CHOIS 22.11 (+1.90)；CLIP Score 24.01 vs LINGO 22.99 (+1.02)；Cont. 0.835 vs CHOIS 0.687 (+0.148)。

## 概要

**核心问题**：现有人景交互（HSI）合成方法依赖成对的3D场景与动作捕捉数据，无法泛化到新场景，尤其是真实世界重建场景。这一数据依赖构成了方法向零样本泛化的根本瓶颈。

**核心洞察**：ZeroHSI 提出从大规模预训练视频生成模型中蒸馏人景交互先验，通过可微神经渲染将生成的2D视频提升为4D交互运动，从而完全绕过对配对动作-场景数据的需求。方法将视频生成模型的丰富交互知识与物理渲染约束相结合，在零样本条件下实现合理的人景交互合成。

**方法定位**：ZeroHSI 属于“视频生成先验 + 可微渲染优化”的混合范式。与使用导航轨迹的 **TRUMANS** 和基于文本指令的 **LINGO** 等基线不同，ZeroHSI 无需任何真实动作数据，而是通过四个串联模块——HSI视频生成、相机姿态估计、HSI优化（联合优化人体姿态与物体6D姿态）以及运动精炼——完成从文本描述到4D交互序列的端到端合成。

**主要结果**：在 AnyInteraction 基准上，ZeroHSI 在静态场景交互中取得 CLIP Score 23.52（TRUMANS 22.36，LINGO 22.61），场景穿透率 Pene%_scene 降至 0.019（TRUMANS 0.046，LINGO 0.058）；在动态对象交互中，CLIP Score 24.01（CHOIS 22.11，LINGO 22.99），接触率 Cont. 达 0.835（CHOIS 0.687，LINGO 0.699），物体穿透率 Pene_obj 降至 0.033（CHOIS 1.581）。人类研究进一步确认，参与者在运动真实感和语义对齐上均以大幅优势偏好 ZeroHSI 生成的结果。消融实验表明，完整的逐帧身体优化（OPT_body）对减少场景穿透至关重要，移除该模块后 Pene%_scene 从 0.019 升至 0.025。

**局限与开放问题**：方法性能受限于视频生成模型的质量，生成视频中的不正确内容或外观不一致可能导致次优结果；单视图监督带来的深度歧义影响复杂动作的精确重建；当前仅支持单个动态对象，且假设物体深度在短时间内恒定。未来方向包括处理多对象交互、引入更强物理先验以及解决长期交互中的漂移问题。

### 问题背景：四维人景交互合成

四维人景交互（4D Human-Scene Interaction, HSI）合成旨在生成人体在三维场景中随时间演化的自然运动序列，涵盖行走、坐卧、操作物体等复杂行为。这一任务在虚拟现实、具身智能、电影制作和机器人仿真等领域具有广泛的应用前景。其核心挑战在于同时满足三个层面的要求：**语义对齐**——生成的运动需符合文本描述或任务意图；**物理合理性**——人体需与场景几何保持一致，避免穿透地面、墙壁或物体；**运动多样性**——能够覆盖不同场景类型和交互类别。

### 现有方法的瓶颈：对配对动捕数据的强依赖

当前主流的 HSI 合成方法，如 **TRUMANS** 和 **LINGO**，虽然在特定场景下取得了可观效果，但其训练和推理均依赖于成对的三维场景与动作捕捉（MoCap）数据。这一范式存在两个根本性瓶颈：

1. **泛化能力受限**：动捕数据采集成本高昂，且通常局限于受控的实验室环境。当面对新的、尤其是真实世界重建的三维场景时，这些方法难以泛化，因为训练分布与新场景的几何布局、语义构成之间存在显著差异。

2. **数据获取不可扩展**：为每一个新场景采集对应的交互动作数据在工程上不可行，这从根本上限制了 HSI 合成技术向开放世界场景的推广。

### 本文动机：从视频生成模型中蒸馏交互先验

大规模预训练的视频生成模型在海量互联网视频数据上学习到了丰富的人体运动模式、物理常识以及人与环境的交互规律。这些隐式知识天然涵盖了多样化的场景类型和交互行为，且无需任何三维动作标注。ZeroHSI 的核心动机正是**绕过对配对动捕-场景数据的需求，转而从视频生成模型中提取人景交互先验**，并将其提升为四维运动表示。

具体而言，ZeroHSI 以三维场景和文本提示为输入，通过视频生成模型产生人景交互视频，再利用可微神经渲染框架，将生成的二维视频优化重建为包含人体姿态、相机轨迹和物体六自由度姿态的完整四维交互序列。这一范式实现了**零样本**（zero-shot）交互合成——无需在新场景上训练，即可生成语义合理、物理可信的人景交互运动。

## 核心方法与创新机理

ZeroHSI 的核心创新在于**将大规模预训练视频生成模型的人景交互先验，通过可微神经渲染提升为4D交互运动**，从而彻底绕过了传统方法对成对3D场景与动作捕捉数据的依赖。这一范式转变通过以下三个关键机制实现：

### 1. 零样本交互先验蒸馏

现有方法（如 TRUMANS、LINGO、CHOIS）的训练和推理均依赖成对的3D场景与动捕数据，导致泛化能力受限于训练场景分布。ZeroHSI 的核心洞察是：**当前最先进的视频生成模型已经隐式地学到了丰富的人体运动与环境交互知识**——包括人体如何在不同场景中行走、坐卧、操作物体等。通过将这些2D视频中的交互知识蒸馏出来，ZeroHSI 首次实现了对新场景的零样本交互合成，无需任何真实动作数据（Abstract: “eliminates the need for training on any MoCap data”）。

### 2. 可微渲染驱动的2D到4D提升

传统方法在2D视频到3D运动的提升中，通常直接使用现成的姿态估计模型（如 WHAM、WHAC）进行逐帧估计。然而，这些方法缺乏对场景几何的显式建模，导致严重的场景穿透和接触不自然。ZeroHSI 的创新在于：

- **联合优化框架**：在可微高斯渲染框架下，同时优化人体姿态参数（SMPL）、相机姿态和物体6D姿态，通过最小化渲染图像与生成视频帧之间的光度损失来实现（Eq. 9–14）。
- **逐帧绝对姿态优化**：直接优化每帧的绝对人体姿态参数 $M_t = (r_t, \phi_t, \Theta_t)$，而非使用相对变换，避免了累积误差（Section 3.4）。
- **动态物体联合处理**：通过深度正则化（$\mathcal{L}_{\mathrm{depth}}$）和中心点损失（$\mathcal{L}_{\mathrm{center}}$）联合优化物体6D姿态，在保持接触质量的同时惩罚不合理的深度变化（Eq. 11–14）。

### 3. 物理合理性增强

在可微渲染优化之后，ZeroHSI 在 VPoser 潜空间中进一步优化运动序列，结合拟合损失和物理损失（$\mathcal{L}_{\mathrm{physics}}$），在保持语义对齐的同时提升运动的物理合理性（Eq. 15–16）。消融实验表明，完整的逐帧身体优化（OPT_body）对减少场景穿透至关重要：移除该模块后，场景穿透率从 0.019 上升至 0.025（Table 4）。

### 关键证据

- **静态场景**：ZeroHSI 在场景穿透率（Pene%_scene）上达到 0.019，显著优于 TRUMANS（0.046）和 LINGO（0.058），同时 CLIP Score 更高（23.52 vs 22.36/22.61）（Table 1）。
- **动态对象**：ZeroHSI 在物体穿透率（Pene_obj）上仅为 0.033，远低于 CHOIS（1.581）和 LINGO（0.242），接触率（Cont.）达到 0.835（Table 2）。
- **消融验证**：用现成姿态估计方法 WHAM/WHAC 替代优化模块会导致全局平移估计不准，引起严重的穿透伪影（Fig. S6），进一步证实了可微渲染优化框架的必要性。

ZeroHSI 的整体设计遵循“生成-重建”范式，其核心洞察在于：**大规模预训练视频生成模型已内化丰富的人景交互先验，通过可微神经渲染可将2D视频中的交互知识蒸馏为4D运动序列**。这一范式彻底绕过了传统方法对成对3D场景与动作捕捉数据的依赖，实现了对新场景的零样本泛化。

### 输入与输出

给定一个3D场景 $s$、一个可交互的动态物体 $\mathcal{O}$、描述交互的文本提示 $c$，以及人体的初始状态（初始姿态 $\mathbf{M}_0$ 和物体初始6D姿态 $\mathbf{P}_0$），ZeroHSI 的目标是生成一段时序长度为 $T$ 的4D人景交互运动序列 $\tau = \{(\mathbf{M}_t, \mathbf{P}_t)\}_{t=1}^{T}$，其中 $\mathbf{M}_t$ 为第 $t$ 帧的人体姿态参数，$\mathbf{P}_t$ 为物体的6D姿态。

### Pipeline 四大模块

ZeroHSI 由四个串行模块构成，数据流从场景渲染到视频生成，再到逐帧优化与序列精炼，形成闭环：

**1. HSI视频生成（HSI Video Generation）**

首先以初始相机视角 $\mathbf{T}_0$ 渲染初始帧 $\mathbf{I}_0$：将可驱动的高斯人体 $\mathcal{G}_{\mathcal{H}}$、变换后的高斯物体 $\mathcal{G}_{\mathcal{O}}$ 与静态高斯场景 $\mathcal{G}_S$ 拼接后，通过高斯光栅化（alpha blending）合成初始交互图像。随后，将该渲染帧与文本提示 $c$ 一同送入现成的视频生成模型，生成一段包含人景交互的2D视频 $\{\mathbf{I}_t\}_{t=1}^{T}$。

**2. 相机姿态估计（Camera Pose Estimation）**

由于视频生成模型输出的帧序列缺乏显式相机参数，本模块利用静态背景区域的光度损失来估计逐帧相机相对变换。具体而言，在第 $t$ 帧，通过聚合从第0帧到第 $t$ 帧的动态前景掩码，构建静态背景掩码 $\mathbf{M}_t$，然后最小化渲染背景与生成帧背景之间的 $L_2$ 损失，求解相机相对变换 $\mathbf{T}_*$（见 Eq.7）。该设计有效消除了生成视频中新显露区域可能出现的错误内容对相机估计的干扰。

**3. HSI优化（HSI Optimization）**

这是整个框架的核心模块，通过可微渲染联合优化人体姿态和物体6D姿态。与现有方法直接使用现成姿态估计器（如 WHAM、WHAC）不同，ZeroHSI 在统一的渲染框架下逐帧优化人体参数 $\mathbf{M}_t = (\mathbf{r}_t, \phi_t, \Theta_t)$ 和物体姿态 $\mathbf{P}_t$。优化目标由组合损失驱动：渲染图像与生成帧之间的混合 $L_1$ 和 D-SSIM 损失（Eq.10）、物体掩码中心点的 $L_2$ 损失（Eq.11）辅助物体定位，以及物体深度正则化损失（Eq.13）惩罚不合理的深度突变。值得注意的是，人体姿态采用直接优化的方式而非相对变换累积，从根本上避免了累计误差导致的漂移问题。

**4. 精炼（Refinement）**

逐帧优化得到的运动序列可能存在时序不连贯和物理不合理之处。本模块将运动序列映射到 VPoser 的潜空间中，联合优化拟合损失（Eq.15）和物理损失（Eq.16），在保持与参考关节匹配精度的同时，提升运动的平滑性和物理合理性。

### 可微渲染的桥梁作用

贯穿整个 Pipeline 的关键技术是**可微高斯渲染**。人体通过 Animatable Gaussians 映射 $\mathcal{G}_{\mathcal{H}} \leftarrow \mathcal{A}(\mathbf{r}, \phi, \Theta; \mathbf{T})$（Eq.6）实现姿态驱动的形变，物体通过6D姿态变换其高斯表示，场景则保持静态。三者拼接后经光栅化渲染（Eq.2），使得从渲染像素到姿态参数的梯度可以端到端传播。这一设计将2D视频信号转化为3D/4D优化的监督源，是“从视频生成模型中蒸馏交互知识”这一核心思想的技术支点。

![[assets/figures/papers/paper_list_l1674_ZeroHSI_Zero_Shot_4D_Human_Scene_Interaction_by_Video_Generation/figures/002_Figure_2.jpg]]
*Figure 2: Overview of ZeroHSI. Our approach begins with HSI video generation conditioned on the rendered initial state and text prompt. Through differentiable neural rendering, we optimize per-frame camera pose, human pose parameters, and object 6D pose by minimizing the discrepancy between the rendered and generated reference videos*

ZeroHSI 将零样本人景交互合成分解为四个串联模块：**HSI 视频生成**、**相机姿态估计**、**HSI 优化**和**运动精炼**。整个流程建立在 3D Gaussian Splatting 的可微渲染基础之上。

### 3D Gaussian 表示与可微渲染

场景、人体和动态物体统一用 3D Gaussian 粒子表示。每个粒子由均值 $\pmb{\mu}$ 和协方差矩阵 $\pmb{\Sigma}$ 定义：

$$G(\mathbf{x}) = e^{-\frac{1}{2}(\mathbf{x} - \pmb{\mu})^{\top} \pmb{\Sigma}^{-1} (\mathbf{x} - \pmb{\mu})}$$

渲染时，对像素重叠的 $N$ 个有序粒子进行 alpha 混合得到颜色：

$$\mathbf{C} = \sum_{i=1}^{N} \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j) \mathbf{c}_i$$

这一可微渲染管线（Figure 3）将参数化高斯人体、经刚体变换的高斯物体和静态高斯场景拼接后，通过高斯光栅化合成图像，使得整个流程可端到端求导。

### 模块一：HSI 视频生成

给定 3D 场景和文本交互描述，首先在场景中初始化一个可驱动的人体化身。通过 Animatable Gaussians 将人体姿态（根节点平移 $\mathbf{r}$、全局朝向 $\phi$、姿态参数 $\Theta$）和相机视角 $\mathbf{T}$ 映射为高斯粒子：

$$\mathcal{G_H} \leftarrow \mathcal{A}(\mathbf{r}, \phi, \Theta; \mathbf{T})$$

将人体高斯、物体高斯与场景高斯拼接后渲染得到初始帧 $\mathbf{I}_0$。以该初始帧和文本提示为条件，利用预训练视频生成模型生成一段人景交互视频。这一步的核心作用是从视频模型中蒸馏交互先验，绕过了对成对动捕数据的需求。

### 模块二：相机姿态估计

生成的视频帧之间存在未知的相机运动。利用静态背景区域的光度一致性逐帧估计相机相对变换 $\mathbf{T}_*$：

$$\mathbf{T}_* = \arg\min_{\mathbf{T}} \mathcal{L}_2\Big(\mathcal{R}\big(\mathcal{G}_S(\mathbf{T}); \mathbf{T}_{t-1}\big) \odot \mathbf{M}_t,\; \mathbf{I}_t \odot \mathbf{M}_t\Big)$$

其中 $\mathbf{M}_t$ 是静态背景掩码，通过聚合历史帧的动态前景掩码得到，用于排除生成视频中人体和物体区域的错误内容对相机估计的干扰。

### 模块三：HSI 优化

这是方法的核心瓶颈突破点——通过可微渲染联合优化每帧的人体姿态和物体 6D 姿态，将 2D 视频提升为 4D 交互序列。

**人体姿态优化**：直接优化每帧的 SMPL 参数 $(\mathbf{r}_t, \phi_t, \Theta_t)$，而非使用帧间相对变换，以避免累积误差。

**渲染光度损失**：最小化渲染帧与生成视频帧之间的差异：

$$\mathcal{L}_{\mathrm{rgb}} = (1 - \lambda) \mathcal{L}_1(\hat{\mathbf{I}}_t, \mathbf{I}_t) + \lambda \mathcal{L}_{\mathrm{D-SSIM}}(\hat{\mathbf{I}}_t, \mathbf{I}_t)$$

**物体中心点损失**：辅助物体 6D 姿态 $\mathbf{P}_t$ 优化，约束渲染物体掩码中心点与生成帧物体掩码中心点一致：

$$\mathcal{L}_{\mathrm{center}} = \mathcal{L}_2(\hat{C}_{\mathcal{O}}^t, C_{\mathcal{O}}^t)$$

**物体深度正则化**：单视图视频的深度歧义是主要挑战。引入深度先验，鼓励物体每帧的平均深度与首帧保持一致：

$$\mathcal{L}_{\mathrm{depth}} = \mathcal{L}_2(\hat{D}_{\mathcal{O}}^t, D_{\mathcal{O}}^0)$$

这一正则项是处理动态物体的关键设计——它惩罚不合理的深度突变，在保持接触质量的同时抑制穿透。

### 模块四：运动精炼

逐帧优化得到的姿态序列可能存在帧间抖动和物理不合理。精炼阶段在 VPoser 潜空间中优化运动序列，平衡拟合精度和物理合理性：

$$\mathcal{L}_{\mathrm{fit}}^{t} = \mathcal{L}_2\Big(\hat{J}_t, J_t\big(\mathbf{r}_t, \phi_t, \mathcal{D}(\mathbf{z}_t)\big)\Big)$$

$$\mathcal{L} = \frac{1}{T} \sum_{t=0}^{T} \mathcal{L}_{\mathrm{fit}}^{t} + \lambda_{\mathrm{physics}} \mathcal{L}_{\mathrm{physics}}$$

其中 $\mathcal{D}(\mathbf{z}_t)$ 是 VPoser 解码器，将潜变量 $\mathbf{z}_t$ 映射为姿态参数；$\mathcal{L}_{\mathrm{physics}}$ 包含速度、加速度和接触力等物理约束项。消融实验（Table 4）表明，完整的逐帧身体优化（OPT_body）对降低场景穿透率至关重要，而精炼模块进一步提升了运动的时序平滑性。

## 实验与关键发现

### 主实验结果

ZeroHSI 在 AnyInteraction 基准（涵盖 12 个室内外 3D 场景，100 个评估实例）上，分别在静态场景交互和动态对象交互两类任务中与现有方法进行了定量比较。为保证公平，所有方法的输出均未应用 Refinement 后处理，视频帧率统一降采样至 10 fps，基线方法使用相同的水密网格计算占用栅格和穿透指标。

**静态场景交互**（Table 1）：与 TRUMANS 和 LINGO 相比，ZeroHSI 在语义对齐、运动多样性和物理合理性上均取得最优。CLIP Score 达到 23.52，分别超出 TRUMANS（22.36）和 LINGO（22.61）1.16 和 0.91 分。物理合理性方面，场景穿透率 Pene%_scene 降至 0.019，远低于 TRUMANS 的 0.046 和 LINGO 的 0.058，降幅分别达 58.7% 和 67.2%。这表明通过可微渲染逐帧优化人体姿态，能有效抑制穿透伪影。

**动态对象交互**（Table 2）：ZeroHSI 同样显著优于 CHOIS 和 LINGO。CLIP Score 达 24.01（CHOIS 22.11，LINGO 22.99），接触率 Cont. 提升至 0.835（CHOIS 0.687，LINGO 0.699），物体穿透率 Pene_obj 仅 0.033，而 CHOIS 高达 1.581。接触率的提升和穿透率的大幅下降，验证了物体中心点损失和深度正则化在联合优化物体 6D 姿态中的关键作用。

**定性对比**（Figure 4、5）：在“滑下滑梯”“靠梯子”“坐在沙发背上”等静态交互中，ZeroHSI 生成的动作与文本提示更一致，且避免了基线方法中常见的穿透和漂浮现象。在“坐在沙发上弹吉他”“举杠铃”“坐在办公椅上滑动”等动态对象交互中，ZeroHSI 在保持物体接触的同时最小化穿透，成功处理了基线方法难以应对的复杂交互。

**人类评估**（Table 3）：在静态和动态两种场景下，参与者均以较大优势偏好 ZeroHSI 生成的运动真实感和语义对齐度，进一步佐证了定量指标的可靠性。

### 消融实验

Table 4 报告了组件消融结果，揭示了各模块对性能的贡献：

![[assets/figures/papers/paper_list_l1674_ZeroHSI_Zero_Shot_4D_Human_Scene_Interaction_by_Video_Generation/figures/010_Table_4.jpg]]
*Table 4: Quantitative results of ablation study*

- **移除逐帧身体优化（w/o OPT_body）**：场景穿透率 Pene%_scene 从完整方法的 0.019 上升至 0.025，增幅约 31.6%。这直接证明了直接优化每帧人体姿态参数（而非依赖相对变换累积）对减少穿透至关重要。
- **移除物体优化（w/o OPT_obj）**：动态交互中的接触率和物体穿透指标显著恶化，验证了物体 6D 姿态联合优化的必要性。
- **用现成姿态估计替代优化**（Fig. S6）：用 WHAM 或 WHAC 直接估计姿态会导致全局平移不准，产生严重的穿透伪影，说明在可微渲染框架内联合优化是 2D 视频到 4D 交互提升的核心瓶颈突破点。

![[assets/figures/papers/paper_list_l1674_ZeroHSI_Zero_Shot_4D_Human_Scene_Interaction_by_Video_Generation/figures/018_Figure_S.6.jpg]]
*Figure S.6: Qualitative results of ablation study on our optimization-based HSI motion reconstruction. Our full method reconstructs root translation more accurately than WHAM and WHAC while achieving smoother results than ZeroHSI w/o*

### 失败模式与局限性

尽管 ZeroHSI 在零样本设定下取得了显著进展，但仍存在以下失败模式和局限：

1. **视频生成质量依赖**：方法性能受限于底层视频生成模型的能力。当生成视频出现身体部位消失、外观不一致或不正确的内容时，后续优化会受到影响。虽然方法通过静态背景掩码聚合（Eq. 背景掩码公式）对部分错误具有一定鲁棒性，但极端情况下仍会产生次优结果。
2. **单视图深度歧义**：仅依赖单视图视频提供的 RGB 监督，在复杂动作（如大幅度转身、四肢交错）中可能出现深度歧义，影响姿态重建精度。
3. **场景几何建模缺失**：零样本设定下缺乏对场景几何的显式理解，偶尔会出现轻微穿透或接触不自然的情况，尤其在场景几何复杂或接触区域狭窄时。
4. **动态对象限制**：当前仅支持单个动态对象，且深度正则化假设物体深度在短时间内恒定（Eq. 13），不适用于物体深度快速变化的运动（如抛接物体）。

### 长期交互与真实场景泛化

Figure 6 展示了 ZeroHSI 在 Mip-NeRF 360 重建的真实场景（Garden、Bicycle）上生成多段文本提示驱动的长期交互序列的能力。通过分段生成与拼接，方法可在重建的真实世界场景中生成连贯的交互运动，验证了其在非合成场景上的泛化性。但长期交互中的漂移问题仍需更有效的解决方案。

![[assets/figures/papers/paper_list_l1674_ZeroHSI_Zero_Shot_4D_Human_Scene_Interaction_by_Video_Generation/figures/006_Figure_6.jpg]]
*Figure 6: Qualitative results of long-term interactions with reconstructed real scenes on AnyInteraction. ZeroHSI generates long-term interaction sequences with multiple text prompts in reconstructed scenes from the Mip-NeRF 360 (Garden and Bicycle) dataset [4]*

![[assets/figures/papers/paper_list_l1674_ZeroHSI_Zero_Shot_4D_Human_Scene_Interaction_by_Video_Generation/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison of interactions with static scenes on AnyInteraction. ZeroHSI generates 4D HSIs that are more realistic and better aligned with text prompts, demonstrating generalizability across diverse scenes and interaction types compared to baselines*

![[assets/figures/papers/paper_list_l1674_ZeroHSI_Zero_Shot_4D_Human_Scene_Interaction_by_Video_Generation/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison of interactions with dynamic objects in scenes on AnyInteraction. Our method maintains proper object contact while minimizing penetration, successfully handling challenging interactions like sliding while seated on an office chair*

## 定位与知识库关联

### 核心瓶颈与因果机制

现有人景交互（HSI）合成方法的根本瓶颈在于**对成对3D场景与动作捕捉数据的强依赖**，这导致模型无法泛化到训练时未见的新场景，尤其难以处理真实世界重建场景。ZeroHSI 的因果调控旋钮是**从大规模预训练视频生成模型中蒸馏人景交互先验**，并通过**可微神经渲染**将2D视频提升为4D交互运动，从而彻底绕开对配对动捕数据的需求。这一设计实现了零样本泛化——给定任意3D场景和文本描述，即可合成合理的人体交互序列。

### 与基线方法的关系与对比

**静态场景交互基线**

- **TRUMANS**：使用导航轨迹生成交互，依赖场景几何与预定义路径点。ZeroHSI 在 AnyInteraction 静态场景评测中，CLIP Score 达 23.52（vs 22.36），场景穿透率 Pene%_scene 仅 0.019（vs 0.046），语义对齐与物理合理性均显著领先。
- **LINGO**：基于文本指令和场景理解生成动作，CLIP Score 为 22.61，Pene%_scene 为 0.058。ZeroHSI 在穿透率上降低约 3 倍，表明可微渲染优化对接触质量的关键作用。

**动态对象交互基线**

- **CHOIS**：基于语言和稀疏物体路径点生成交互，CLIP Score 22.11，接触率 Cont. 0.687，物体穿透 Pene_obj 高达 1.581。ZeroHSI 将接触率提升至 0.835（+0.148），物体穿透降至 0.033（降低约 48 倍），证明联合优化物体6D姿态与深度正则化的有效性。
- **LINGO** 在动态场景下接触率 0.699，物体穿透 0.242，ZeroHSI 同样大幅领先。

**关键设计差异**：所有基线均依赖某种形式的显式动作数据或场景-动作配对，而 ZeroHSI 的零样本特性使其可直接应用于任意3D场景，无需针对新环境重新训练或微调。

### 方法谱系中的位置

ZeroHSI 处于**视频生成、可微神经渲染与人体运动合成**的交叉点。其技术路线可追溯至两条主线：

1. **视频生成驱动运动合成**：继承自大规模视频扩散模型（如文中引用的视频生成模型 ）的运动先验提取思路，但不同于直接使用现成姿态估计器（如 WHAM 、WHAC ），ZeroHSI 将生成视频视为“软监督”，通过可微渲染进行端到端优化，避免了估计误差累积导致的穿透伪影（消融实验中 Fig. S6 证实了这一点）。

2. **可微人体渲染与逆渲染**：基于 Animatable Gaussians 的可驱动人体表征，ZeroHSI 将 SMPL 姿态参数、相机外参、物体6D姿态统一纳入可微渲染管线，通过光度损失（Eq.10）、中心点损失（Eq.11）和深度正则化（Eq.13）联合优化。这与传统的“先估计后优化”两阶段方法形成根本区别。

### 适用边界

- **场景类型**：支持静态场景和含单个动态对象的场景，涵盖室内外多种环境（AnyInteraction 基准包含 7 个室内和 5 个室外场景）。
- **交互类型**：覆盖行走、坐下、倚靠、清洁等静态场景交互，以及浇水、举重、弹吉他、滑动座椅等动态对象交互。
- **输入条件**：需要3D场景、可选的动态物体、文本描述和初始状态（人体初始姿态与物体初始位姿）。
- **长期交互**：通过多段文本提示的拼接，可生成长期交互序列（Fig. 6 展示了在 Mip-NeRF 360 重建的真实场景上的多段交互）。

### 局限性与开放问题

**已确认的局限性**

1. **视频生成质量依赖**：方法性能受限于底层视频生成模型。当生成视频出现身体部位消失、外观不一致或内容错误时，优化结果会退化。虽然方法通过背景掩码聚合（Eq. 背景掩码公式）等手段展示了一定鲁棒性，但仍可能产生次优结果。
2. **单视图深度歧义**：仅依赖单一渲染视图的光度监督，复杂动作（如大幅度转身、肢体交叉）可能因深度信息不足而导致重建不精确。
3. **缺乏显式场景几何建模**：零样本设置下未对场景几何进行显式推理，偶尔会出现轻微穿透或接触不自然。
4. **动态对象限制**：当前仅支持单个动态对象，且假设物体深度在短时间内恒定（深度正则化 Eq.13 鼓励与首帧平均深度一致），不适用于深度快速变化的运动。

**开放问题**

1. **动态对象几何泛化**：如何处理未见动态对象的大幅几何变化（如变形物体、非刚体），使得零样本交互更加通用？
2. **无文本引导的交互生成**：当文本描述与场景不匹配或完全缺失时，视频生成模型能否仍产生有意义的交互？
3. **多对象与多主体扩展**：如何将框架扩展到多个交互对象和复杂的多主体场景？
4. **物理合理性增强**：能否引入更强的物理仿真或接触力学先验（如摩擦力、支持力约束），进一步提升运动的物理合理性？
5. **长期交互漂移**：当前依赖分段生成与拼接处理长期交互，如何更有效地解决累积漂移问题？

> **注意**：上述局限性均来自论文自身的讨论与消融实验证据。关于动态对象深度恒定假设的严格性、以及视频生成模型在不同场景类型下的失效模式，建议结合补充材料中的 Fig. S6 和用户研究（Table 3）进行交叉验证。

## 原文 PDF

![[paperPDFs/arxiv_2024/ZeroHSI_Zero_Shot_4D_Human_Scene_Interaction_by_Video_Generation.pdf]]
