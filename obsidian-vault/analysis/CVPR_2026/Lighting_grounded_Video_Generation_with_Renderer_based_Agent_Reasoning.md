---
title: Lighting-grounded Video Generation with Renderer-based Agent Reasoning
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Lighting_grounded_Video_Generation_with_Renderer_based_Agent_Reasoning.pdf
project_link: null
code_link: null
aliases:
- LGVGRBAR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过渲染器代理将场景光照分解为漫反射、粗糙GGX和光滑GGX三个2D渲染通道，并以此作为条件信号注入视频扩散模型，实现对光照行为的精确操控。
primary_logic: 将光照建模为场景的统一物理属性之一，利用2D渲染通道编码的光照线索与预训练视频生成先验相结合，通过轻量级编码器和适配器模块实现场景布局、相机轨迹与物理光照的解耦控制。
claims:
- LiVER conditions video synthesis on explicit 3D scene properties using a renderer-based agent and a lightweight conditional encoder/adapter.
- Physical cues are injected into a video diffusion model to synthesize photorealistic sequences with accurate lighting behavior, faithful scene layout, and precisely aligned camera...
- Our method achieves the lowest FVD (32.56), FID (129.56) and highest CLIP (30.97) on LiVERSet evaluation.
- In user study, our method is preferred in 83.4% (VQ), 83.3% (SC), 72.1% (CC), 59.3% (LC) of samples, outperforming all baselines.
---

# Lighting-grounded Video Generation with Renderer-based Agent Reasoning

> [!tip] 核心洞察
> 将光照建模为场景的统一物理属性之一，利用2D渲染通道编码的光照线索与预训练视频生成先验相结合，通过轻量级编码器和适配器模块实现场景布局、相机轨迹与物理光照的解耦控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | LiVER：基于渲染器代理推理的光照约束视频生成 |
| 英文题名 | Lighting-grounded Video Generation with Renderer-based Agent Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.07966) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | LiVER |
| Dataset | LiVERSet eval, User Study |

> [!tip] 效果简介
> - LiVERSet eval 上，FVD 32.56；FID 129.56；CLIP 30.97。
> - User Study 上，VQ↑ 83.4%；SC↑ 83.3%；CC↑ 72.1%。

## 概要

现有可控视频生成方法在引入3D场景信息时，通常仅关注几何布局与相机轨迹，而忽略了物理光照建模。这导致生成的视频中阴影、反射、环境光遮蔽等光照效果与真实材质表现脱节，缺乏物理真实感。LiVER 针对这一瓶颈，提出将光照作为场景的统一物理属性之一，通过**渲染器代理**将3D场景的光照行为显式分解为漫反射、粗糙GGX和光滑GGX三个2D渲染通道，并将这些物理线索作为条件信号注入预训练视频扩散模型，实现了场景布局、相机轨迹与物理光照的解耦控制。

该方法的核心洞察在于：2D渲染通道编码的光照线索可以与预训练视频生成先验有效结合，通过轻量级编码器和适配器模块，在不破坏原有生成能力的前提下，精确操控光照行为。在 LiVERSet 评测基准上，LiVER 取得了 FVD 32.56、FID 129.56、CLIP 30.97 的全面最优结果；用户偏好研究中，该方法在视觉质量（83.4%）、场景一致性（83.3%）、相机控制（72.1%）和光照控制（59.3%）四个维度上均显著优于现有基线方法。

方法谱系上，LiVER 延续了 **CameraCtrl**（He et al., ICLR 2025）等工作的可控视频生成路线，但将条件模态从文本描述和2D轨迹拓展为**光照约束的场景代理**，并采用三阶段训练策略（条件通路训练→联合LoRA微调→光照多样性扩展）来稳定收敛。与 **VideoFrom3D**（Kim et al., SIGGRAPH Asia 2025）等3D场景视频生成方法相比，LiVER 的差异化在于显式引入基于物理的渲染通道，而非仅依赖图像-视频扩散的互补先验。在知识库定位上，该方法处于3D感知视频生成与物理渲染的交叉地带，为可控视频合成提供了新的光照维度。

可控视频生成旨在根据用户提供的条件信号（如文本描述、相机轨迹、边界框等）合成视觉上真实且结构上一致的视频序列。近年来，以扩散模型（Diffusion Models）为核心的视频生成方法取得了显著进展，能够生成具有丰富语义和时序连贯性的视频内容。然而，当用户需求从“生成一段视频”升级为“精确控制场景的物理属性”时，现有方法暴露出一个根本性瓶颈：**光照建模的缺失**。

现有可控视频生成方法主要关注两个维度的控制——**场景布局**与**相机运动**。例如，**CameraCtrl**（He et al., ICLR 2025）和**MotionCtrl**（Wang et al., SIGGRAPH 2024）通过注入2D轨迹或相机参数来实现对视频中对象位置和视角变化的控制；**VideoFrom3D**（Kim et al., SIGGRAPH Asia 2025）则利用3D场景表示来提供几何基础的引导。这些方法虽然在一定程度上实现了对“物体在哪里”和“相机怎么动”的控制，但都隐含地忽略了一个关键问题：**光照如何影响场景的外观**。

在真实世界中，物体的视觉呈现不仅取决于其几何形状，更取决于材质与光照的物理交互——漫反射决定了物体的基础色调，粗糙表面的GGX反射塑造了柔和的阴影过渡，光滑表面的GGX反射则产生锐利的高光和镜面反射。当视频生成模型缺乏对这些光照行为的显式建模时，生成的阴影可能方向错误、反射与材质粗糙度不匹配、环境光遮蔽缺失，从而导致整体画面缺乏真实感。这正是当前方法的症结所在：**仅提供几何基础，而忽视基于物理的精确光照（如BRDF），导致生成结果中阴影、反射、环境光遮蔽等光照效果与真实材质表现不匹配**。

本文的核心动机源于一个关键洞察：**光照应当被建模为场景的统一物理属性之一，而非视频生成的事后修饰**。如果将光照分解为可渲染的2D通道（漫反射、粗糙GGX、光滑GGX），并将其作为显式条件信号注入视频扩散模型，就有可能在保持预训练生成先验的同时，实现对光照行为的精确操控。这一思路将光照控制从“隐式学习”转变为“显式引导”，使得模型能够理解材质响应、阴影方向和反射强度等物理线索，从而生成光照真实、布局忠实、相机轨迹精确对齐的视频序列。

基于上述动机，本文提出**LiVER（Lighting-grounded Video Generation with Renderer-based Agent Reasoning）**，一个基于渲染器代理推理的光照约束视频生成框架。LiVER通过三个核心设计填补了现有方法的缺口：（1）引入渲染器代理（Renderer-based Agent），从文本提示中推理出3D场景、HDR光照环境和相机轨迹；（2）利用基于物理的渲染器生成光照约束的场景代理（Scene Proxy），包含漫反射、粗糙GGX和光滑GGX三个2D通道；（3）通过轻量级编码器和适配器模块，将这些物理线索注入预训练视频扩散模型，实现场景布局、相机轨迹与物理光照的解耦控制。

## 核心方法与创新机理

### 从“几何感知”到“光照感知”的条件范式迁移

当前可控视频生成方法（如 **CameraCtrl** (He et al., ICLR 2025)、**MotionCtrl** (Wang et al., SIGGRAPH 2024)）主要依赖文本描述或2D轨迹/边界框作为条件信号，即便部分方法引入了3D场景信息（如 **VideoFrom3D** (Kim et al., SIGGRAPH Asia 2025)），也仅停留在几何层面的粗粒度布局控制，完全忽视了光照这一决定视觉真实感的核心物理属性。这导致生成结果中阴影方向错误、反射缺失、环境光遮蔽不一致等典型失效——模型“知道物体在哪，但不知道光从哪来”。

LiVER将条件信号从“几何占位”推进到“物理光照约束”，其核心创新在于将光照建模为场景的统一物理属性之一，而非生成过程的附属产物。具体而言，该方法将场景光照分解为**纯漫反射**（$x^{\mathrm{DIFF}}$）、**粗糙GGX**（$x^{\mathrm{GGX1}}$）和**光滑GGX**（$x^{\mathrm{GGX2}}$）三个2D渲染通道，构成“光照场景代理”（lighting-grounded scene proxy），作为视频扩散模型的核心条件输入。这一设计的因果机制在于：三个通道分别编码了材质对入射光的漫反射响应、粗糙表面的模糊反射和光滑表面的镜面反射，使得模型能够显式地学习光照-材质-几何之间的物理耦合关系，而非从像素中隐式猜测。

### 渲染器代理：将物理知识外化为可计算条件

传统方法依赖神经网络隐式学习光照，缺乏物理约束，导致光照行为不可控且难以泛化。LiVER通过引入**渲染器代理**（renderer-based agent）将物理光照知识外化为可计算、可干预的条件信号。该代理接收文本提示后，解析对象类别、空间关系与场景语义，从预定义资产库中选择3D网格，设置HDR环境图作为全局光照源，并规划相机轨迹，最终通过物理渲染器（Blender）输出三个像素对齐的光照通道。

这一设计的关键创新在于“物理先验的注入方式”：不是让模型自己去理解光照，而是将光照的物理计算结果直接作为条件送入扩散模型。渲染器代理充当了物理世界与生成模型之间的桥梁，其输出的场景代理 $y = [x^{\mathrm{DIFF}}, x^{\mathrm{GGX1}}, x^{\mathrm{GGX2}}] = R(s^i, l^i, c^i)$ 将复杂的BRDF积分计算从学习问题转化为条件编码问题，大幅降低了模型对光照行为的建模难度。

### 轻量适配：将光照线索注入预训练视频先验

直接微调大型视频扩散模型以接受新的条件模态会导致灾难性遗忘和巨大计算开销。LiVER的第三个关键创新在于其**轻量级条件注入机制**：通过一个2D CNN代理编码器将场景代理下采样为紧凑特征 $z^y$，再通过可学习标量 $\alpha$ 将其叠加到原始视频潜变量上：

$$z' = z + \alpha \cdot z^y$$

其中 $\alpha$ 初始化为零，确保训练初期模型行为与预训练权重一致，随后逐步引入光照控制信号。这一“零初始化残差连接”设计使得模型能够平稳地从无条件生成过渡到光照约束生成，避免了训练不稳定问题。配合LoRA微调策略，整个条件适配仅需在预训练主干上添加少量可训练参数，在8张NVIDIA H100 GPU上训练约100K步即可收敛。

### 三阶段训练：解耦控制能力的渐进习得

与基线方法的端到端训练不同，LiVER采用三阶段训练策略，这是实现解耦控制的关键设计：

1. **条件通路训练**（Conditional Pathway Training）：仅训练新增的条件编码模块，冻结预训练主干，确保条件特征提取器学会编码光照信息而不破坏生成先验。
2. **联合LoRA微调**（Joint LoRA Fine-tuning）：引入LoRA层，联合优化条件编码器和主干网络，使模型学会利用光照线索生成逼真细节。
3. **光照多样性扩展**（Lighting Diversity Expansion）：在合成数据（LiVER-Syn）上进一步训练，增强模型对不同光照条件的泛化能力。

消融实验证实，跳过第一阶段直接从联合训练开始会导致输出几乎静止、质量严重退化；仅用真实数据而不用合成数据则会产生错误且均匀的照明效果。这表明分阶段训练策略不仅是工程优化，更是实现光照解耦控制的必要条件——模型需要先“学会看光照”，再“学会用光照”，最后“学会适应不同光照”。

LiVER 的整体设计围绕一个核心洞察展开：**将光照建模为场景的统一物理属性**，并通过渲染器代理将3D场景的几何、材质与光照信息压缩为2D渲染通道，作为条件信号注入预训练视频扩散模型，从而实现对场景布局、相机轨迹与物理光照的解耦控制。

### 三阶段处理流水线

如图1所示，LiVER 的生成流水线分为三个递进阶段：

**阶段一：渲染器代理推理。** 给定文本提示 $T$，Scene Agent 解析其中的物体类别、空间关系与粗略几何信息，从预定义资产库中选择合适的3D资产，构建初始3D场景 $s^i$；同时，Camera Agent 推断与描述视点和场景语义一致的相机轨迹 $c^i$。此外，代理还根据场景光照需求选取HDR环境图作为全局光照表示 $l^i$。最终，代理将推理得到的资产组合 $[s^{\inf}, l^{\inf}, c^{\inf}]$ 作为完整的场景表示输出。

**阶段二：物理渲染生成场景代理。** 上述3D场景表示被送入基于物理的渲染器 $R$（Blender），渲染出三个像素对齐的2D光照通道：
- **纯漫反射** $x^{\mathrm{DIFF}}$：仅包含 Lambertian 漫反射分量，无镜面高光；
- **粗糙GGX** $x^{\mathrm{GGX1}}$：高粗糙度的微表面BRDF响应，呈现模糊反射；
- **光滑GGX** $x^{\mathrm{GGX2}}$：低粗糙度的微表面BRDF响应，呈现清晰反射与高光。

三者沿通道维度拼接，形成光照约束的场景代理 $y = [x^{\mathrm{DIFF}}, x^{\mathrm{GGX1}}, x^{\mathrm{GGX2}}] = R(s^i, l^i, c^i)$。这种分解方式将复杂的物理光照行为编码为模型可直接感知的2D信号，同时保留了材质响应、阴影和反射等关键光照线索。

**阶段三：视频扩散生成。** 场景代理 $y$ 通过轻量级 Proxy Encoder（2D CNN）下采样编码为紧凑特征 $z^y$；Conditioning Encoder 则生成与VAE潜在空间对齐的空间残差。最终，DiT架构的视频扩散骨干网络（基于 Wan2.2-5B-TI2V 预训练权重）整合场景条件 $X_{\mathrm{cond}}$、相机条件 $C$ 和光照条件 $L$，通过 Flow Matching 目标进行去噪生成：

$$\mathcal{L} = \mathbb{E}_{z, \epsilon, t}\left[\left| u_{\theta}(z_t, y, c^{\mathrm{txt}}, t) - v_t \right|^2 \right]$$

其中 $u_\theta$ 预测速度向量 $v_t$，引导噪声潜变量 $z_t$ 逐步恢复为真实视频潜变量。

### 关键设计：残差调制与渐进控制

为避免光照条件对预训练生成先验的剧烈干扰，LiVER 采用**可学习残差调制**机制将代理特征注入视频潜变量：

$$z' = z + \alpha \cdot z^{y}$$

其中 $\alpha$ 为可学习标量，初始化为零。这一设计确保了训练初期模型行为完全由预训练先验主导，随着训练推进，$\alpha$ 逐步增大，光照控制信号平滑介入，从而在不破坏生成质量的前提下实现精确的光照约束。配合 LoRA 低秩适配，整个条件注入模块仅引入极少的可训练参数，有效避免了灾难性遗忘。

### 数据支撑：LiVER-Syn 与 LiVER-Real

为训练上述流水线，LiVER 构建了双来源数据集（共约11K视频片段，每段81帧，分辨率720×1280，其中10K用于训练、1K用于评估）：
- **LiVER-Syn**：由渲染器代理自动生成的合成数据，提供完美的3D几何、光照与相机真值标注；
- **LiVER-Real**：从真实视频中通过3D重建与HDR环境图估计逆向渲染获得的光照表示，用于桥接合成-真实域差异。

### 方法谱系与知识库定位

LiVER 处于**3D感知可控视频生成**与**物理光照建模**的交叉点。相较于仅依赖2D轨迹或边界框的方法（如 **CameraCtrl** (He et al., ICLR 2025)、**MotionCtrl** (Wang et al., SIGGRAPH 2024)），LiVER 通过显式3D场景代理引入了几何精确的布局与相机控制；相较于 **VideoFrom3D** (Kim et al., SIGGRAPH Asia 2025) 等3D场景视频生成方法，LiVER 进一步将光照从隐式生成结果提升为显式可控的物理条件，实现了对阴影、反射和环境光遮蔽等光照效果的独立操控。

![[assets/figures/papers/paper_list_l2537_https_arxiv_org_abs_2604_07966/figures/001_Figure_1.jpg]]
*Figure 1: Overall framework. (1) A renderer-based agent produces a coarse geometric layout, camera trajectory, and a High Dynamic Range (HDR) environment map. (2) Physically-based rendering generates a lighting-grounded scene proxy containing diffuse, rough, and glossy materials with shading signals. (3) These physical cues are injected into a video diffusion model to synthesize photorealistic sequences with accurate lighting behavior, faithful scene layout, and precisely aligned camera trajectory*

LiVER 的核心设计思路是将物理光照建模为显式条件信号，通过渲染器代理（Renderer-based Agent）将 3D 场景属性转换为 2D 光照通道，再注入预训练视频扩散模型，实现对场景布局、相机轨迹和光照行为的解耦控制。整个流水线由四个关键模块构成。

### 场景代理构建与物理渲染

**Scene Agent** 接收文本提示 $T$，解析对象类别、空间关系和粗略几何信息，从预定义资产库中选择 3D 网格 $s^i$，设置 HDR 环境图 $l^i$，并由 Camera Agent 推断与描述视角一致的相机轨迹 $c^i$。这些资产被送入基于物理的渲染器（Blender），生成光照约束的场景代理（scene proxy）$y$：

$$
y = [ x ^ { \mathrm { { D I F F } } } , x ^ { \mathrm { { G G X 1 } } } , x ^ { \mathrm { { G G X 2 } } } ] = R ( s ^ { i } , l ^ { i } , c ^ { i } )
$$

其中 $x^{\mathrm{DIFF}}$ 为纯漫反射分量，$x^{\mathrm{GGX1}}$ 为粗糙 GGX 分量（高粗糙度），$x^{\mathrm{GGX2}}$ 为光滑 GGX 分量（低粗糙度）。这三个 2D 渲染通道分别编码材质的漫反射响应、粗糙表面着色和镜面反射等高光行为，形成像素对齐的物理光照线索。这种分解方式使模型能够区分不同材质对同一光照条件的差异化响应，是实现光照可控性的关键。

### 代理编码与条件注入

**Proxy Encoder** 是一个轻量级 2D CNN，将场景代理 $y$ 下采样并编码为紧凑特征 $z^y$。**Conditioning Encoder** 则生成空间残差，对齐至 VAE 潜在空间。编码后的代理特征通过可学习的标量 $\alpha$ 叠加到原始视频潜变量 $z$ 上：

$$
z ^ { \prime } = z + \alpha \cdot z ^ { \mathrm { y } }
$$

$\alpha$ 初始化为零，确保训练初期模型行为与预训练先验一致，随后逐步引入光照控制信号。这种残差调制策略避免了直接条件注入对预训练权重的破坏性干扰，同时实现了对光照强度的平滑调控。

### 视频扩散骨干与训练目标

LiVER 基于 **Wan 2.2-5B-TI2V** 预训练视频扩散模型构建，采用 DiT（Diffusion Transformer）架构，并通过 LoRA 进行高效适配以降低计算开销并防止灾难性遗忘。模型在给定场景代理 $y$ 和文本嵌入 $c^{\mathrm{txt}}$ 的条件下，使用 Flow Matching 目标进行训练：

$$
\mathcal { L } = \mathbb { E } _ { z , \epsilon , t } \left[ \left| u _ { \theta } ( z _ { t } , y , c ^ { \mathrm { t x t } } , t ) - v _ { t } \right| ^ { 2 } \right]
$$

其中 $u_\theta$ 为预测的速度向量，$v_t$ 为从噪声到真实潜变量的目标速度场。这一目标使模型学习在光照条件、相机轨迹和文本语义的联合约束下生成物理一致的光照效果。

### 三阶段训练策略

为确保稳定收敛，LiVER 采用分阶段训练方案：(1) **Conditional Pathway Training**：仅训练代理编码器和条件编码器，冻结扩散骨干；(2) **Joint LoRA Fine-tuning**：联合微调 LoRA 层与条件模块；(3) **Lighting Diversity Expansion**：在合成数据（LiVER-Syn）上扩展光照多样性。消融实验表明，直接从联合训练开始会导致输出几乎静止、质量严重退化，验证了分阶段策略的必要性。

![[assets/figures/papers/paper_list_l2537_https_arxiv_org_abs_2604_07966/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline of LiVER. Given a text prompt T , our Scene Agent parses object categories, spatial relations, and coarse geometry to construct an initial 3D scene. The Camera Agent infers a camera trajectory consistent with the described viewpoint and scene semantics, producing the camera condition*

![[assets/figures/papers/paper_list_l2537_https_arxiv_org_abs_2604_07966/figures/002_Figure_2.jpg]]
*Figure 2: Our data annotation pipeline for LiVER-Real. We process each video to reconstruct its 3D geometry and estimate its HDR environment map. These are then used to render three pixel-aligned lighting representations (Diffuse, Glossy GGX, Rough GGX), which are concatenated to form the final conditioning input*

## 实验与关键发现

### 评估设置

LiVER 在自建数据集 **LiVERSet** 上进行评估，该数据集包含超过 11K 个视频片段，每个视频 81 帧，分辨率为 720 × 1280，其中 10K 用于训练，1K 用于测试。模型基于 **Wan 2.2-5B-TI2V** 预训练视频扩散模型构建，使用 8 块 NVIDIA H100 GPU 训练约 100K 步，每 GPU 批量大小为 2，采用 AdamW 优化器，恒定学习率 $1 \times 10^{-5}$，并引入 LoRA 以降低计算开销并防止灾难性遗忘。生成视频分辨率为 704 × 1280。

定量评估覆盖多个维度：视频质量（FVD、FID）、文本-视频语义对齐（CLIP）、相机轨迹精度（ATE、RPEt、RPEr）、光照误差（LE）以及布局保持度（mIoU）。此外，还通过用户研究从四个维度进行主观评价：视频质量（VQ）、场景一致性（SC）、相机控制（CC）和光照控制（LC）。

### 主实验结果

**定量结果。** 如表 1 所示，LiVER 在所有自动化指标上均达到最优。具体而言，FVD 降至 **32.56**，FID 降至 **129.56**，CLIP 分数达到 **30.97**，表明生成视频在视觉质量和文本对齐方面显著优于基线方法。在相机控制方面，ATE 为 **2.48**、RPEt 为 **0.71**、RPEr 为 **0.50**，均低于对比方法，验证了 3D 场景代理对相机轨迹的精确约束能力。光照误差 LE 低至 **0.04**，布局 mIoU 达到 **0.87**，说明显式物理渲染通道有效编码了光照和几何信息。

**用户研究。** 如表 2 所示，人类评估者在多数样本中偏好 LiVER 的生成结果：视频质量偏好率 **83.4%**，场景一致性 **83.3%**，相机控制 **72.1%**，光照控制 **59.3%**。光照控制维度的优势相对较小（59.3%），这与该任务本身的高感知难度一致——人类观察者对细微光照差异的敏感度有限，但 LiVER 仍显著优于所有基线。

**定性对比。** 图 4 展示了与 **CameraCtrl**（He et al., ICLR 2025）、**MotionCtrl**（Wang et al., SIGGRAPH 2024）和 **VideoFrom3D**（Kim et al., SIGGRAPH Asia 2025）等方法的视觉对比。LiVER 在物体布局保持、相机轨迹跟随和光照一致性方面均表现出明显优势：基线方法常出现物体漂移、阴影缺失或光照与场景几何不匹配的问题，而 LiVER 生成的视频中，阴影方向、反射强度和材质表现与给定的 HDR 环境图保持物理一致。

### 消融实验

**合成数据的必要性。** 消融实验（图 6）表明，仅使用真实数据（LiVER-Real）训练会导致模型产生错误且均匀的照明效果，缺乏对光照方向和强度的精确响应。引入合成数据（LiVER-Syn）后，模型能够学习到光照与材质之间的物理关联，生成具有方向性阴影和镜面反射的真实感结果。这验证了合成数据在提供多样化、精确标注的光照条件方面的关键作用。

**分阶段训练策略。** 直接进行联合训练（跳过 Conditional Pathway Training 阶段）会导致生成视频几乎静止、质量严重退化（图 6）。三阶段训练——(1) Conditional Pathway Training、(2) Joint LoRA Fine-tuning、(3) Lighting Diversity Expansion——对稳定收敛至关重要。第一阶段使条件编码器学会从场景代理中提取有效特征；第二阶段通过 LoRA 将控制信号注入预训练先验；第三阶段通过光照增广提升模型对多样化光照的泛化能力。

**3D 场景代理 vs. 2D 轨迹。** 与仅使用 2D 轨迹或边界框的方法相比，显式 3D 场景代理提供了几何精确的物体布局和相机运动控制。定量结果（表 1 中 ATE 和 mIoU 的显著优势）和定性观察均支持这一结论：3D 代理通过渲染器生成的像素对齐光照通道，使模型能够推理遮挡关系和透视变化，而 2D 条件信号在这些场景中容易产生歧义。

### 光照可控性分析

图 5 展示了 LiVER 的光照操控能力。通过替换 HDR 环境图，模型能够产生连续且物理一致的光照变化：阴影方向随光源位置旋转而平滑移动，镜面高光在光滑表面上的强度和位置相应调整，而物体的几何结构和材质属性保持稳定。场景代理的三个分量（漫反射、粗糙 GGX、光滑 GGX）为模型提供了从粗糙到光滑材质的完整光照响应线索，使生成结果中的光照行为符合物理直觉。

### 失败模式与局限性

尽管 LiVER 在整体性能上表现优异，但分析揭示了以下局限：

1. **资产库覆盖范围有限。** 代理推理依赖预定义的 3D 资产库和 HDR 环境图库，对于长尾场景（如罕见物体或极端光照条件），资产匹配可能不准确，导致场景代理与文本描述之间存在语义偏差。
2. **动态遮挡与间接光照。** 在涉及动态物体间复杂遮挡关系的场景中，渲染器生成的 2D 代理无法完全编码间接光照和相互反射，可能导致生成结果中局部光照不够真实。
3. **合成数据的域差异。** 尽管合成数据对光照控制至关重要，但其与真实数据的域差异可能在生成结果中引入细微伪影，尤其在材质细节和纹理自然度方面。这一问题在光照多样性扩展阶段需要进一步的正则化策略来缓解。

### 开放性讨论

- **代理鲁棒性。** 当前场景代理的构建质量对文本提示的表述方式较为敏感，如何通过更精细的提示工程或基于反馈的迭代优化提升代理的场景解析鲁棒性，是实际部署中的关键挑战。
- **动态光照扩展。** 方法目前处理静态 HDR 环境图，将其扩展到动态光照效果（如移动光源、时变天空模型）将显著提升应用范围，但需解决时序光照一致性和计算开销的平衡问题。
- **多物体交互。** 在保持高质量光照控制的同时支持更复杂的多物体物理交互（如碰撞、堆叠），需要更精细的场景图建模和渲染策略，这是从“场景漫游”向“场景交互”演进的核心瓶颈。

![[assets/figures/papers/paper_list_l2537_https_arxiv_org_abs_2604_07966/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art methods. Our method consistently outperforms the baselines. †Only compare first 16 frames*

![[assets/figures/papers/paper_list_l2537_https_arxiv_org_abs_2604_07966/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison with state-of-the-art controllable video generation models. In each block, each row corresponds to one video, and frames are arranged from left to right in temporal order. The top row shows the results of each comparison method, followed by ours, with the ground truth (GT) shown in the final row*

![[assets/figures/papers/paper_list_l2537_https_arxiv_org_abs_2604_07966/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative results of our ablation study*

## 定位与知识库关联

### 1. 与现有可控视频生成方法的关系

LiVER 的核心贡献在于将**物理精确的光照建模**引入可控视频生成的 conditioning 体系，这一思路与现有工作形成了清晰的继承与突破关系。

**继承自相机/运动可控生成**。现有可控视频生成方法主要聚焦于相机轨迹和物体运动的精确控制。**CameraCtrl**（He et al., ICLR 2025）通过相机位姿序列实现视频生成中的视角控制，**MotionCtrl**（Wang et al., SIGGRAPH 2024）进一步统一了相机运动与物体运动的联合控制。这些工作证明了将结构化控制信号注入预训练视频扩散模型的技术可行性，LiVER 沿用了这一"conditioning 注入预训练先验"的基本范式，但在控制信号的维度上做了根本性扩展——从纯几何运动扩展到包含材质响应（BRDF）的物理光照。

**突破于 3D 场景视频生成**。**VideoFrom3D**（Kim et al., SIGGRAPH Asia 2025）通过互补的图像与视频扩散模型从 3D 场景生成视频，证明了 3D 几何信息对视频生成质量的提升作用。然而该类方法仅提供几何基础，忽视了物理光照——阴影、反射、环境光遮蔽等效果与真实材质表现不匹配。LiVER 的突破在于：将光照建模为场景的统一物理属性，通过渲染器代理将漫反射、粗糙 GGX 和光滑 GGX 三个 2D 渲染通道作为条件信号，使视频扩散模型能够"理解"并复现物理一致的光照行为。

**条件模态的根本性变化**。从技术 slot 角度看，LiVER 将 conditioning modality 从文本描述（`c^txt`）和可选的 2D 轨迹/边界框，替换为**光照约束的场景代理**（漫反射 + 粗糙 GGX + 光滑 GGX）配合 HDR 环境图与相机轨迹。这一变化使得模型能够解耦控制场景布局、相机轨迹与物理光照三个独立维度，而非将光照效果隐式地"烘焙"在生成结果中。

### 2. 适用边界与局限

尽管 LiVER 在定量指标和用户偏好上均显著优于基线方法，其方法设计本身存在明确的适用边界：

**资产库依赖**。场景代理的推理依赖于预定义的 3D 资产库和 HDR 环境图库（基于 Poly Haven ）。当用户文本提示涉及长尾场景或罕见物体时，代理可能无法找到匹配的 3D 资产，导致场景构建失败或质量下降。这一局限在开放域文本到视频生成场景中尤为突出。

**动态遮挡与间接光照**。即使在光照条件可控的情况下，动态物体间复杂的遮挡关系与间接光照（如运动物体投射的移动阴影、物体间相互反射）仍可能不完全真实。渲染器代理提供的是静态场景的光照分解，而视频生成过程中的动态交互需要模型自行"想象"，这构成了物理真实感的上限。

**合成数据的域差异**。LiVER 的训练数据混合了合成数据（LiVER-Syn）和真实视频标注数据（LiVER-Real）。消融实验（Fig. 6）表明合成数据对光照控制至关重要——仅用真实数据训练会产生错误且均匀的照明效果。然而合成数据的渲染质量与真实视频之间存在固有的域差异，可能在真实场景中引入细微伪影，这一问题的量化评估尚不充分。

**对文本描述的敏感性**。场景代理的构建依赖于 LLM 代理对用户文本提示的解析，提示工程的质量直接影响场景图构建的准确性。当文本描述存在歧义或过于简洁时，代理的场景解析鲁棒性可能不足。

### 3. 开放问题

LiVER 开辟了物理光照约束视频生成这一新方向，同时留下了若干值得探索的开放问题：

**动态光照扩展**。当前方法处理的是静态 HDR 环境图下的光照条件。能否将方法扩展到动态光照效果——如移动光源、物体表面材质随时间变化、昼夜切换——而不显著增加计算开销？这需要渲染器代理支持时变的光照表示，同时视频扩散模型需要学习光照变化的时序一致性。

**多物体交互与物理模拟**。当前场景代理主要处理静态物体布局，如何在保持高质量光照控制的同时支持更复杂的多物体交互（如碰撞、堆叠、遮挡关系动态变化）？这可能需要在渲染器代理中引入轻量级物理模拟模块。

**代理鲁棒性提升**。如何通过更精细的提示工程或反馈机制提升代理对用户指令的场景解析鲁棒性？一个可能的方向是引入迭代式场景优化——生成视频后通过视觉质量评估反馈修正场景代理参数。

**泛化至非刚性物体与室外场景**。当前实验主要集中于刚性物体的室内/产品级场景。方法能否泛化至包含非刚性变形（如布料、流体）和复杂室外光照（如天空模型、体积光散射）的场景，仍需验证。

**计算效率优化**。三阶段训练策略（Conditional Pathway Training → Joint LoRA Fine-tuning → Lighting Diversity Expansion）虽然对稳定收敛至关重要（消融实验表明直接从联合训练开始会导致输出几乎静止），但增加了训练复杂度。能否通过更高效的训练策略或架构设计减少阶段数，同时保持生成质量？

## 原文 PDF

![[paperPDFs/CVPR_2026/Lighting_grounded_Video_Generation_with_Renderer_based_Agent_Reasoning.pdf]]
