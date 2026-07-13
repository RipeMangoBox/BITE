---
title: "Hunyuan3D 2.0: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Hunyuan3D_2_0_Scaling_Diffusion_Models_for_High_Resolution_Textured_3D_Assets_Generation.pdf
project_link: null
code_link: https://github.com/Tencent/Hunyuan3D-2
aliases:
- H20
- H20SDMHRT3AG
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 采用基于重要性采样的点云编码变分自编码器与流匹配驱动的双流/单流扩散变压器，结合双流参考网络与并行多任务注意力机制，在形状与纹理生成两个阶段分别引入针对性的表示增强和一致性约束。
primary_logic: 通过重要性采样保留高频几何细节，利用双流/单流 Transformer 实现形状生成的条件对齐；借助零噪声固定权重参考网络保持图像细节，并通过并行多任务注意力同时达成多视图一致与条件遵循，从而生成高保真纹理。
claims:
- Hunyuan3D-ShapeVAE 的重要性采样策略显著提升重建精度，V-IoU 达 93.6%，比最强基线 Direct3D 高 5.17 个百分点。
- Hunyuan3D-DiT 在条件跟随能力上全面超越所有对比方法，Uni3D-I 得分 0.3151。
- Hunyuan3D-Paint 生成最符合条件的纹理图，CMMD 低至 2.318，显著优于所有基线。
- 用户研究表明 Hunyuan3D 2.0 在视觉质量、条件依从性和整体满意度上均优于对比方法。
---

# Hunyuan3D 2.0: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation

> [!tip] 核心洞察
> 通过重要性采样保留高频几何细节，利用双流/单流 Transformer 实现形状生成的条件对齐；借助零噪声固定权重参考网络保持图像细节，并通过并行多任务注意力同时达成多视图一致与条件遵循，从而生成高保真纹理。

| 字段 | 内容 |
|------|------|
| 中文题名 | 浑元3D 2.0：面向高分辨率纹理3D资产生成的扩散模型扩展 |
| 英文题名 | Hunyuan3D 2.0: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2501.12202) · [Code](https://github.com/Tencent/Hunyuan3D-2) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Hunyuan3D 2.0 |
| Dataset | Shape Reconstruction, Shape Generation, Texture Map Synthesis, User Study |

> [!tip] 效果简介
> - Shape Reconstruction 上，V-IoU 93.6% vs 88.43% (Direct3D) (+5.17%)；S-IoU 89.16% vs 81.55% (Direct3D) (+7.61%)。
> - Shape Generation (Image Conditional) 上，Uni3D-I 0.3151 vs 0.3116 (Trellis) (+0.0035)；Uni3D-T 0.2519 vs 0.2516 (Shape Model 3) (+0.0003)。
> - Texture Map Synthesis 上，CMMD 2.318 vs 2.651 (Paint3D) (-0.333)。

## 概要
从单张图像生成高分辨率、带纹理的3D资产是计算机图形学与视觉领域的一项核心挑战。现有方法在形状生成阶段难以精准捕捉表面边缘与角落的复杂几何细节，而在纹理合成阶段，由于缺乏有效的几何先验与光照解耦，常出现多视图不一致和条件对齐差的问题，导致生成质量受限。

针对上述瓶颈，**Hunyuan3D 2.0** 提出了一套两阶段生成管线：首先通过 **Hunyuan3D-ShapeVAE + Hunyuan3D-DiT** 从输入图像生成无纹理的裸网格（bare mesh），再通过 **Hunyuan3D-Paint** 为该网格合成高保真纹理贴图。其核心洞察在于：在形状端，利用基于边缘/角落重要性采样的点云编码变分自编码器保留高频几何细节，并借助双流/单流混合 Transformer 与流匹配训练实现条件对齐的形状扩散生成；在纹理端，引入冻结权重的零噪声双流参考网络保持图像细节，并通过并行多任务注意力模块同时达成多视图一致性与条件遵循。

实验结果表明，该方法在多个维度上取得了显著提升：
- **形状重建**：Hunyuan3D-ShapeVAE 的体积 IoU 达到 93.6%，比最强基线 Direct3D 高出 5.17 个百分点（Table 1）。
- **形状生成**：Hunyuan3D-DiT 在条件跟随指标 Uni3D-I 上以 0.3151 超越所有对比方法（Table 2）。
- **纹理合成**：Hunyuan3D-Paint 的 CMMD 低至 2.318，显著优于 Paint3D 等基线（Table 3）。
- **用户研究**：在视觉质量、条件依从性和整体满意度上均获得最高偏好（Figure 10）。

### 3D 资产生成的核心挑战

高质量 3D 资产（包含精细几何与高保真纹理）在游戏、影视、AR/VR 等领域需求巨大，但其手工制作成本极高。自动化生成面临两大核心瓶颈：

1. **几何细节捕捉困难**：现有 3D 形状生成方法难以精准重建表面边缘与角落的复杂细节。基于均匀表面采样的编码策略会丢失高频几何信息，导致重建网格在边缘处模糊、细节缺失。
2. **纹理合成中的多视图不一致与条件对齐差**：纹理生成需要在多个视角下保持一致性，同时精确遵循输入图像的纹理细节。现有方法在缺乏有效几何先验与光照解耦的情况下，常出现视图间纹理错位、色彩偏移或与参考图像语义偏离的问题。

### 现有方法的局限

**形状生成侧**，主流方法可归为两类：基于隐式表示（如 SDF、NeRF）和基于显式表示（如 mesh、点云）。隐式方法虽能表达任意拓扑，但提取高质量 mesh 仍需后处理且计算量大；显式方法直接生成 mesh，但受限于表示能力，难以同时保证全局结构合理与局部细节丰富。例如：
- **3DShape2VecSet**（Zhang et al., TOG 2023）与 **Michelangelo**（Zhao et al., NeurIPS 2023）采用向量集表示隐式函数，但采样策略为均匀表面采样，对边缘和角落的细节保留不足。
- **Direct3D**（Wu et al., arXiv 2024）在重建精度上有所提升，但 V-IoU 仅达 88.43%，与理想水平仍有差距。

**纹理合成侧**，基于扩散模型的多视图生成方法（如 **Zero-1-to-3**（Liu et al., ICCV 2023）、**Wonder3D**（Long et al., CVPR 2024）、**Era3D**（Li et al., arXiv 2024））虽能生成多视图图像，但在视图一致性和条件精确对齐方面存在明显不足。**Paint3D**（Zeng et al., CVPR 2024）引入纹理烘焙流程，但其 CMMD 仍高达 2.651，表明纹理与参考图像的条件偏离较大。

### 本文动机

针对上述缺口，Hunyuan3D 2.0 提出了一套两阶段生成管线，核心动机在于：

- **通过重要性采样保留高频几何细节**：在形状变分自编码器（ShapeVAE）中，对网格边缘和角落进行有偏采样，使编码器能捕获传统均匀采样所遗漏的关键几何特征。
- **利用双流/单流 Transformer 实现形状生成的条件对齐**：在形状扩散模型中，采用混合双流与单流块的 Transformer 架构，增强图像条件与形状表示的跨模态交互。
- **借助零噪声固定权重参考网络与并行多任务注意力达成纹理高保真**：纹理生成阶段，冻结预训练 Stable Diffusion 的 ReferenceNet 权重以精确保留输入图像细节，同时通过并行参考注意力与多视图注意力模块，同时满足条件遵循与视图一致性要求。

这一设计思路旨在端到端地解决“几何细节丢失”与“纹理不一致/不对齐”两大核心问题，实现高分辨率、高保真的 3D 纹理资产生成。

## 核心方法与创新机理
Hunyuan3D 2.0 的核心创新围绕“形状生成”与“纹理合成”两个阶段展开，通过一系列针对性的表示增强、网络结构改进与一致性约束，系统性地解决了现有方法在几何细节捕捉、条件对齐和多视图一致性方面的瓶颈。

**1. 面向高频几何细节的重要性采样 ShapeVAE**

现有 3D 形状 VAE（如 **3DShape2VecSet** (Zhang et al., TOG 2023)、**Michelangelo** (Zhao et al., NeurIPS 2023)、**Direct3D** (Wu et al., arXiv 2024)）普遍采用均匀表面采样策略，难以有效捕捉边缘、角落等高频区域的复杂细节。Hunyuan3D-ShapeVAE 引入了重要性采样策略：在均匀采样的基础上，额外在网格边缘与角落密集采样点云，并将两组点云分别通过最远点采样（FPS）构建查询点序列，共同输入编码器。这一改变使模型能够显式地保留高频几何信息，在重建评估中 V-IoU 达到 93.6%，比最强基线 Direct3D 的 88.43% 提升 5.17 个百分点（Table 1）。

**2. 流匹配驱动的双流/单流混合扩散变压器**

形状生成阶段，Hunyuan3D-DiT 采用带条件最优传输路径的流匹配（Flow Matching）训练目标替代传统的 DDPM/DDIM 范式，加速采样并提升生成质量。在网络结构上，摒弃了标准 DiT 或 U-ViT 架构，设计了双流与单流块混合的 Transformer：双流块中形状与图像条件分别经过独立的注意力路径，促进跨模态交互；单流块则将两者串联处理，增强条件跟随能力。此外，模型有意省略了隐序列的位置编码，使形状潜在表示保持空间无关性，有利于学习更本质的几何结构。

**3. 零噪声固定权重参考网络与并行多任务注意力**

纹理合成阶段，Hunyuan3D-Paint 对参考图像的注入方式进行了关键改进。不同于常见的共享权重 ReferenceNet 或含噪参考分支，该方法直接使用冻结权重的 Stable Diffusion 2.1 作为参考网络，输入无噪声的 VAE 特征，并将参考分支的时间步固定为 0。这一设计最大程度保留了参考图像的细节信息，避免了噪声引入导致的纹理退化。

在多视图一致性与条件对齐方面，Hunyuan3D-Paint 设计了并行参考注意力与多视图注意力模块，叠加在冻结的自注意力输出之上：

$$Z_{MVA} = Z_{SA} + \lambda_{ref} \cdot \mathrm{Softmax}\left( \frac{Q_{ref} K_{ref}^T}{\sqrt{d}} \right) V_{ref} + \lambda_{mv} \cdot \mathrm{Softmax}\left( \frac{Q_{mv} K_{mv}^T}{\sqrt{d}} \right) V_{mv}$$

其中参考注意力负责将无光照参考图的细节注入生成过程，多视图注意力则确保不同视角图像之间的一致性。两者并行执行，避免顺序注意力可能带来的信息衰减或计算冗余。

**4. 光照解耦与贪婪覆盖视角选择**

纹理合成前，引入图像去光照模块（Image Delighting Module），通过 image-to-image 方法移除输入图像的光照与阴影，获得光线不变的参考图。这一预处理步骤使后续多视图生成不受原始光照条件干扰，显著提升了纹理在不同光照环境下的泛化性。

在视角选择上，Hunyuan3D-Paint 采用基于贪婪覆盖的视角选择算法，以最大化 UV 纹理覆盖面积为目标，从 44 个预设视角中逐步选取最优视角组合。训练阶段引入视图丢弃策略（View Dropout），随机选择 6 个视角进行训练，增强模型对稀疏视角输入的鲁棒性。推理时则生成密集多视图图像，通过纹理烘焙与基于顶点权重的漏洞补全获得完整纹理贴图。

**创新点总结**

| 改进维度 | 基线方案 | Hunyuan3D 2.0 方案 | 效果 |
|---------|---------|-------------------|------|
| 点云采样 | 均匀表面采样 | 均匀采样 + 边缘/角落重要性采样 | V-IoU +5.17% (Table 1) |
| 扩散训练目标 | DDPM/DDIM | 条件最优传输流匹配 | 加速采样，提升生成质量 |
| 形状扩散网络 | 标准 DiT/U-ViT | 双流/单流混合 Transformer，省略位置编码 | Uni3D-I 0.3151 最优 (Table 2) |
| 纹理参考注入 | 共享权重/含噪参考分支 | 冻结 SD2.1，零噪声 VAE 特征，时间步固定为 0 | CMMD 2.318 最优 (Table 3) |
| 多视图一致性 | 顺序/共享注意力 | 并行参考注意力 + 多视图注意力 | 多视图一致性与条件对齐同步优化 |
| 视角选择 | 固定视角/均匀采样 | 贪婪覆盖视角选择 + 视图丢弃策略 | 训练鲁棒，推理覆盖完整 |

这些创新并非孤立存在，而是形成了完整的因果链条：重要性采样保留几何高频信息 → 流匹配与双流 Transformer 实现精准条件跟随 → 去光照与零噪声参考网络保持纹理细节 → 并行多任务注意力同时达成条件对齐与多视图一致性。最终，Hunyuan3D 2.0 在形状重建、条件生成和纹理合成三个核心维度上均取得了显著超越现有方法的性能。

Hunyuan3D 2.0 采用**两阶段生成管线**：第一阶段从单张输入图像生成无纹理的裸网格（bare mesh），第二阶段为该网格合成高保真纹理贴图。两个阶段分别由 **Hunyuan3D-DiT** 和 **Hunyuan3D-Paint** 两大组件承担，整体架构如图 2 所示。

### 形状生成阶段：Hunyuan3D-DiT

该阶段的核心是“先压缩、后生成”的潜在扩散范式，由形状变分自编码器 **Hunyuan3D-ShapeVAE** 与流匹配驱动的扩散变压器 **Hunyuan3D-DiT** 串联组成。

- **Hunyuan3D-ShapeVAE（压缩与重建）**：将 3D 形状编码为紧凑的潜在 token 序列，并从中解码重建有符号距离场（SDF）。其关键创新在于**重要性采样策略**——在均匀表面采样的基础上，额外对网格边缘和角落进行密集采样，使编码器能捕获高频几何细节。训练时采用多分辨率策略（随机采样不同长度的潜在 token 序列）以加速收敛，损失函数为 SDF 重建 MSE 与加权 KL 散度之和：

  $$\mathcal{L}_r = \mathbb{E}_{x \in \mathbb{R}^3} [ \mathrm{MSE}( \mathcal{D}_s(x | Z_s), \mathrm{SDF}(x) ) ] + \gamma \mathcal{L}_{KL}$$

- **Hunyuan3D-DiT（图到形状生成）**：在 ShapeVAE 的潜在空间中执行条件生成。采用**双流/单流混合 Transformer 架构**（图 4），双流模块促进形状与图像两种模态的交互，单流模块则专注于形状潜在序列的建模；同时**省略了潜在序列的位置编码**，使模型更关注几何语义本身。训练目标为带条件最优传输路径的流匹配损失：

  $$\mathcal{L} = \mathbb{E}_{t, x_0, x_1} [\| u_{\theta}(x_t, c, t) - u_t \|_2^2]$$

  其中 $u_t = x_1 - x_0$，$x_t = (1-t)x_0 + t x_1$。

### 纹理合成阶段：Hunyuan3D-Paint

纹理合成采用**三阶段框架**：预处理、多视图图像合成、纹理烘焙。

- **预处理（光照解耦）**：通过图像去光照模块（Image Delighting Module）去除输入图像中的光照和阴影，获得光线不变的参考图，避免光照信息被错误“烘焙”到纹理中。

- **多视图图像合成（Hunyuan3D-Paint）**：以去光照参考图和裸网格的几何条件（规范法线图、坐标图）为输入，生成多视图一致且与参考图对齐的彩色图像。核心设计包括：
  - **双流参考网络（Double-stream Reference-Net）**：冻结 Stable Diffusion 2.1 权重，将参考图的**零噪声 VAE 特征**直接注入参考分支，时间步固定为 0，从而最大程度保留图像细节。
  - **并行多任务注意力（Multi-task Attention）**：在冻结的自注意力输出上并行叠加参考注意力与多视图注意力，同时实现条件对齐与视图一致性：

    $$Z_{MVA} = Z_{SA} + \lambda_{ref} \cdot \mathrm{Softmax}\left( \frac{Q_{ref} K_{ref}^T}{\sqrt{d}} \right) V_{ref} + \lambda_{mv} \cdot \mathrm{Softmax}\left( \frac{Q_{mv} K_{mv}^T}{\sqrt{d}} \right) V_{mv}$$

  - **视角选择与丢弃策略**：训练时从 44 个预设视角中随机选取 6 个并随机丢弃部分视角（view dropout），推理时基于贪婪覆盖函数选取密集视角集，最大化 UV 纹理覆盖面积：

    $${\mathcal{F}}(v_i, \mathbb{V}_s, \mathbf{M}) = {\mathcal{A}}_{area}\left\{ {\mathcal{UV}}_{\mathrm{cover}}(v_i, \mathbf{M}) \setminus \left[ {\mathcal{UV}}_{\mathrm{cover}}(v_i, \mathbf{M}) \cap \left( \bigcup_{s \in \mathbb{V}_s} {\mathcal{UV}}_{\mathrm{cover}}(v_s, \mathbf{M}) \right) \right] \right\}$$

- **纹理烘焙与补全**：将多视图图像烘焙为 UV 纹理贴图，并通过单图超分和基于顶点权重的漏洞补全（inpainting）消除接缝与空洞。

### 数据流与端到端衔接

输入图像首先进入 Hunyuan3D-DiT 生成裸网格；该网格一方面提供几何条件（法线图、坐标图）输入 Hunyuan3D-Paint，另一方面其 UV 参数化用于后续纹理烘焙。输入图像经去光照后作为参考图，与几何条件一同驱动多视图扩散模型生成一致的多视图图像，最终烘焙为可直接用于渲染的纹理贴图。整个管线实现了从单张 RGB 图像到带纹理 3D 资产的端到端生成。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2501_12202/figures/003_Figure_2.jpg]]
*Figure 2: An overall of Hunyuan3D 2.0 architecture for 3D generation. It consists of two main components: Hunyuan3D-DiT for generating bare mesh from a given input image and Hunyuan3D-Paint for generating a textured map for the generated bare mesh. Hunyuan3D-Paint takes geometry conditions – normal maps and position maps of generated mesh as inputs and generates multi-view images for texture baking*

Hunyuan3D 2.0 的核心生成能力建立在三个紧密协作的模块之上，它们分别解决了形状重建/生成与纹理合成中的关键瓶颈。

### 形状压缩与重建：Hunyuan3D-ShapeVAE

该模块的目标是将三维形状压缩为紧凑的隐空间表征，同时保留高频几何细节。其核心创新在于**重要性采样策略**：除了传统的均匀表面采样外，额外在网格的边缘和角落进行密集采样，以捕捉精细的表面结构。编码器以点云的三维坐标和法向量作为输入，通过变分编码器-解码器 Transformer 架构，预测符号距离函数（SDF）以实现形状重建。

训练损失函数由 SDF 重建的均方误差与加权 KL 散度组成：

$$ \mathcal{L}_r = \mathbb{E}_{x \in \mathbb{R}^3} [ \mathrm{MSE}( \mathcal{D}_s(x | Z_s), \mathrm{SDF}(x) ) ] + \gamma \mathcal{L}_{KL} $$

其中，$Z_s$ 为编码后的隐变量，$\mathcal{D}_s$ 为 SDF 解码器，$\gamma$ 控制 KL 正则化强度。该设计使 Hunyuan3D-ShapeVAE 在重建精度上显著超越 **Direct3D** (Wu et al., arXiv 2024) 等基线模型（详见 Table 1）。

### 形状生成：Hunyuan3D-DiT

Hunyuan3D-DiT 是一个基于流匹配（Flow Matching）的大规模扩散 Transformer，负责从输入图像生成裸网格。其核心设计包括：

- **流匹配训练目标**：采用带条件最优传输路径的仿射路径，损失函数为：

$$ \mathcal{L} = \mathbb{E}_{t, x_0, x_1} [\| u_{\theta}(x_t, c, t) - u_t \|_2^2] $$

其中 $u_t = x_1 - x_0$ 为目标速度场，$x_t = (1-t)x_0 + t x_1$ 为插值状态，$c$ 为图像条件。

- **双流/单流混合 Transformer**：网络交替使用双流块（促进形状与图像模态交互）和单流块，并省略隐序列的位置编码，以增强条件对齐能力。

### 纹理合成：Hunyuan3D-Paint

纹理合成阶段面临两大挑战：多视图一致性与条件图像对齐。Hunyuan3D-Paint 通过以下模块解决这些问题：

- **双流图像条件参考网络**：以冻结权重的 Stable Diffusion 2.1 作为参考分支，输入零噪声的 VAE 特征，时间步固定为 0，从而无失真地保留参考图像细节。
- **并行多任务注意力**：在冻结的自注意力输出上叠加参考注意力和多视图注意力：

$$ Z_{MVA} = Z_{SA} + \lambda_{ref} \cdot \mathrm{Softmax}\left( \frac{Q_{ref} K_{ref}^T}{\sqrt{d}} \right) V_{ref} + \lambda_{mv} \cdot \mathrm{Softmax}\left( \frac{Q_{mv} K_{mv}^T}{\sqrt{d}} \right) V_{mv} $$

其中 $\lambda_{ref}$ 和 $\lambda_{mv}$ 分别为参考注意力和多视图注意力的权重系数。该设计使模型能同时满足条件依从性和视图间一致性。

- **图像去光照模块**：在生成前去除输入图像的光照和阴影，获得光线不变的参考图，避免光照信息干扰纹理合成。
- **贪婪覆盖视角选择**：推理时基于覆盖函数 $\mathcal{F}(v_i, \mathbb{V}_s, \mathbf{M})$ 选择能最大化 UV 纹理覆盖面积的视角，训练阶段则引入视角丢弃策略以增强鲁棒性。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2501_12202/figures/005_Figure_4.jpg]]
*Figure 4: Overview of Hunyuan3D-DiT. It adopts a transformer architecture with both double- and single-stream blocks. This design benefits the interaction between modalities of shape and image, helping our model to generate bare meshes with exceptional quality. (Note that the orange blocks have no learnable parameters, the blue blocks contain trainable parameters, and the gray blocks indicate a module composed of more details.)*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2501_12202/figures/006_Figure_5.jpg]]
*Figure 5: Overview of Hunyuan3D-Paint. We leverage an image delighting module to convert the input image to an unlit state to produce light-invariant texture maps. The system features a doublestream image conditioning reference-net, which provides faithfully conditional image features to the model. Furthermore, it facilitates the production of texture maps that conform closely to the input image. The multi-task attention module ensures that the model synthesizes multi-view consistent images. This module maintains the coherence of all generated images while adhering to the input*

## 实验与关键发现
### 形状重建与生成评估

**形状VAE重建精度。** Hunyuan3D-ShapeVAE 在体积交并比（V-IoU）和表面交并比（S-IoU）两项指标上全面超越所有基线方法。如 Table 1 所示，其 V-IoU 达到 93.6%，比最强基线 **Direct3D**（Wu et al., arXiv 2024）的 88.43% 高出 5.17 个百分点；S-IoU 达到 89.16%，比 Direct3D 的 81.55% 高出 7.61 个百分点。这一显著提升的核心驱动力在于重要性采样策略——通过在高频细节密集的边缘与角落区域增加采样密度，ShapeVAE 的编码器得以保留传统均匀采样所丢失的精细几何信息。视觉对比（Figure 6）进一步印证了数值结论：只有 Hunyuan3D-ShapeVAE 重建的网格呈现出清晰的表面凹凸与规整的空间拓扑，而基线方法在尖锐边缘和复杂曲面处普遍出现模糊或塌陷。

**形状生成条件跟随能力。** Hunyuan3D-DiT 在图像条件形状生成任务上取得了最优的条件对齐性能。Table 2 显示，其 Uni3D-I 得分为 0.3151，略优于 **Trellis**（Xiang et al., arXiv 2024）的 0.3116；Uni3D-T 得分为 0.2519，与最强基线 **Shape Model 3** 的 0.2516 基本持平。尽管数值差距较小，但结合双流/单流混合 Transformer 架构的设计——双流模块促进形状与图像模态间的交叉注意力交互，单流模块专注形状潜变量自身的去噪——使得生成结果在语义保真度上表现出更精准的条件跟随。Figure 7 的视觉对比展示，Hunyuan3D-DiT 生成的裸网格能忠实再现输入图像中的表面起伏与复杂细节，而基线方法常出现结构偏离或细节丢失。

### 纹理合成评估

**纹理图质量与条件符合度。** Hunyuan3D-Paint 在所有纹理合成指标上均取得最优结果。Table 3 显示，其 CMMD（条件最大均值差异）低至 2.318，显著优于 **Paint3D**（Zeng et al., CVPR 2024）的 2.651，降幅达 0.333；CLIP-score 为 0.8893，高于 Paint3D 的 0.8661；LPIPS 为 0.0059，低于 Paint3D 的 0.0085。CMMD 的大幅领先直接归因于双流参考网络与并行多任务注意力的协同设计：冻结权重的 SD2.1 ReferenceNet 以零噪声 VAE 特征注入无光照参考图像，完整保留了输入纹理细节；并行参考注意力与多视图注意力模块在保持条件对齐的同时强制跨视图一致性，避免了顺序注意力或共享注意力方案中常见的视图间色偏与接缝伪影。Figure 8 的视觉对比直观展示了这一优势——Hunyuan3D-Paint 生成的纹理图在色彩、材质与图案上与输入条件高度一致，且多视图拼接处无缝平滑，而基线方法普遍存在纹理漂移或视图不一致。

**纹理重贴图能力。** Figure 9 展示了 Hunyuan3D-Paint 在纹理重贴图（texture reskinning）任务上的泛化性能。给定同一网格的不同参考图像，模型能生成风格迥异但均贴合几何表面的纹理图，验证了图像去光照模块与条件注入机制对光照不变纹理特征的有效解耦。

### 用户研究

Figure 10 所示的用户研究结果从主观感知维度验证了数值评估结论。50 名参与者在视觉质量、条件依从性和整体满意度三个维度上对 Hunyuan3D 2.0 与多个基线方法进行偏好比较，Hunyuan3D 2.0 在所有维度上均获得显著更高的偏好率。这一结果与客观指标的领先趋势一致，表明重要性采样、流匹配扩散以及并行多任务注意力等设计在实际感知质量上同样有效。

### 消融与失败模式

论文未提供系统性的消融实验数据，因此各设计模块（如重要性采样比例、双流与单流模块的消融、并行注意力权重系数 λ_ref 与 λ_mv 的敏感性）的定量贡献尚无法确认。此外，在极端视角遮挡、复杂拓扑（如薄壳结构）或高光反射材质等场景下的失败模式也未在论文中明确讨论。上述两点需在实际部署中通过额外实验进行验证。

### 公平性说明

所有对比实验均在统一条件下进行：形状重建与生成评估使用 300 个测试用例；ShapeVAE 比较中除 Direct3D（固定 3072 token）外均采用 1024 token 序列长度；纹理合成评估基于自采大尺度 3D 数据集中的测试对象；用户研究涉及 50 名参与者，确保统计稳定性。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2501_12202/figures/007_Table_1.jpg]]
*Table 1: Numerical comparisons. We evaluate the reconstruction performance of Hunyuan3D-ShapeVAE and baselines based on volume IoU (V-IoU) and Surface (S-IoU). The results indicate Hunyuan3D-ShapeVAE overwhelms all baselines in the reconstruction performance*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2501_12202/figures/008_Figure_6.jpg]]
*Figure 6: Visual comparisons. We illustrate the reconstructed mesh (blue paint aims to show more details) in the figure, which showcases that only Hunyuan3D-ShapeVAE reconstructs mesh with fine-grained surface details and neat space. (Better viewed by zooming in.)*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2501_12202/figures/009_Table_2.jpg]]
*Table 2: Numerical comparisons. By evaluating the shape generation performance on ULIP-T/I, Uni3D-T/I, demostrating Hunyuan3D-DiT could produce the most condition followed results*

## 定位与知识库关联
Hunyuan3D 2.0 的贡献可置于以下技术谱系中理解：

| 技术维度 | 代表性基线工作 | Hunyuan3D 2.0 的关键改进 |
|---------|---------------|------------------------|
| 3D形状压缩与重建 | **3DShape2VecSet** (Zhang et al., TOG 2023)、**Michelangelo** (Zhao et al., NeurIPS 2023)、**Direct3D** (Wu et al., arXiv 2024) | 引入边缘/角落重要性采样策略，在相同 token 序列长度下显著提升 V-IoU 与 S-IoU |
| 图像到3D形状生成 | **Craftsman 1.5** (Li et al., 2024)、**Trellis** (Xiang et al., arXiv 2024) | 采用流匹配替代 DDPM/DDIM，设计双流/单流混合 Transformer 并省略位置编码，增强条件对齐 |
| 多视图纹理合成 | **Zero-1-to-3** (Liu et al., ICCV 2023)、**Wonder3D** (Long et al., CVPR 2024)、**Era3D** (Li et al., arXiv 2024)、**Dense-Texture** (Liu et al., SIGGRAPH Asia 2024)、**Paint3D** (Zeng et al., CVPR 2024) | 冻结权重的 SD2.1 双流 ReferenceNet + 并行多任务注意力，配合图像去光照预处理与基于贪婪覆盖的视角选择 |

该方法并非孤立改进某一模块，而是系统性地重塑了从形状表示、扩散训练目标、网络结构到纹理条件注入与多视图一致性约束的全链路设计。其技术路线代表了“大规模扩散模型 + 专用表示增强 + 多阶段解耦生成”方向在3D资产生成领域的一次重要推进。

### 1. 形状生成谱系：从 VAE 压缩到流匹配扩散

Hunyuan3D 2.0 的形状生成管道建立在潜扩散模型的经典范式之上，但其核心组件的设计选择与现有工作形成了明确的改进关系。

**形状 VAE 谱系。** 基于点云的 3D 形状压缩与重建是该领域的基础模块。早期工作 **3DShape2VecSet** (Zhang et al., TOG 2023) 采用均匀表面采样与 Transformer 编码器-解码器结构，将形状表示为隐向量集合。**Michelangelo** (Zhao et al., NeurIPS 2023) 进一步扩展了这一思路，将形状 VAE 与生成模型联合训练。**Direct3D** (Wu et al., arXiv 2024) 则在编码器设计上做了改进。

Hunyuan3D-ShapeVAE 的关键突破在于**重要性采样策略**：在均匀采样的基础上，额外对网格边缘与角落区域进行密集采样，使编码器能捕获高频几何细节。这一设计直接回应了现有方法“难以精准捕捉表面边缘与角落的复杂细节”的瓶颈。定量证据显示，在 1024 token 序列长度下，ShapeVAE 的 V-IoU 达到 93.6%，比最强基线 Direct3D 的 88.43% 高出 5.17 个百分点；S-IoU 达到 89.16%，比 Direct3D 的 81.55% 高出 7.61 个百分点（Table 1）。此外，ShapeVAE 采用了多分辨率训练策略（随机采样隐 token 序列长度）以加速收敛，并通过 SDF 解码器直接预测符号距离函数值，训练损失为 SDF 重建 MSE 与加权 KL 散度之和：

$$\mathcal{L}_r = \mathbb{E}_{x \in \mathbb{R}^3} [ \mathrm{MSE}( \mathcal{D}_s(x | Z_s), \mathrm{SDF}(x) ) ] + \gamma \mathcal{L}_{KL}$$

**形状扩散模型谱系。** 在生成模型层面，**Craftsman 1.5** (Li et al., 2024) 和 **Trellis** (Xiang et al., arXiv 2024) 代表了基于图像条件生成 3D 形状的最新进展。Hunyuan3D-DiT 在此基础上做了两项关键改动：

1. **训练目标替换**：从传统的 DDPM/DDIM 范式转向**带条件最优传输路径的流匹配**（Flow Matching with conditional optimal transport schedule），训练损失为：

   $$\mathcal{L} = \mathbb{E}_{t, x_0, x_1} [\| u_{\theta}(x_t, c, t) - u_t \|_2^2]$$

   其中 $u_t = x_1 - x_0$，$x_t = (1-t)x_0 + t x_1$。这一选择使得生成过程在更少的采样步数下保持高质量。

2. **双流/单流混合 Transformer 架构**：采用双流块处理图像与形状潜在表示的跨模态交互，单流块处理形状潜在表示的自注意力，同时**省略了潜在序列的位置编码**。这一设计与标准 DiT 或 U-ViT 形成对比，旨在让模型更灵活地学习形状的全局结构。

在条件跟随能力上，Hunyuan3D-DiT 的 Uni3D-I 得分 0.3151，略高于 Trellis 的 0.3116（Table 2），表明其在图像到形状的对齐上具有微弱但一致的优势。

### 2. 纹理合成谱系：从多视图扩散到解耦注意力

纹理合成是多视图生成与纹理烘焙的交叉领域，Hunyuan3D-Paint 的设计在多个维度上与现有基线形成对比。

**多视图纹理生成基线。** **Zero-1-to-3** (Liu et al., ICCV 2023) 开创了基于扩散模型的视角条件生成，**Wonder3D** (Long et al., CVPR 2024) 和 **Era3D** (Li et al., arXiv 2024) 进一步扩展了多视图一致性的处理。**Dense-Texture** (Liu et al., SIGGRAPH Asia 2024) 和 **Paint3D** (Zeng et al., CVPR 2024) 则专注于纹理图的直接合成。这些方法的共同瓶颈在于：纹理合成在缺乏有效几何先验与光照解耦时，面临多视图不一致和条件对齐差的问题。

Hunyuan3D-Paint 通过三个关键设计突破这一瓶颈：

1. **光照解耦预处理**：引入 Image Delighting Module，在生成前去除输入图像的光照和阴影，获得光线不变的参考图。这避免了纹理图中嵌入场景光照信息导致的泛化问题。

2. **冻结权重的双流参考网络**：不同于共享权重的 ReferenceNet 或 noisy 参考分支，Hunyuan3D-Paint 直接使用冻结权重的 SD2.1 作为参考分支，输入零噪声的 VAE 特征，时间步固定为 0。这一设计保留了预训练模型的图像理解能力，同时避免了参考图像信息在扩散过程中被噪声污染。

3. **并行多任务注意力**：这是 Hunyuan3D-Paint 最核心的创新。现有方法通常采用顺序注意力或共享注意力来处理条件注入与多视图一致性，而 Hunyuan3D-Paint 将参考注意力与多视图注意力设计为**并行结构**，叠加在冻结的自注意力输出上：

   $$Z_{MVA} = Z_{SA} + \lambda_{ref} \cdot \mathrm{Softmax}\left( \frac{Q_{ref} K_{ref}^T}{\sqrt{d}} \right) V_{ref} + \lambda_{mv} \cdot \mathrm{Softmax}\left( \frac{Q_{mv} K_{mv}^T}{\sqrt{d}} \right) V_{mv}$$

   其中 $\lambda_{ref}$ 和 $\lambda_{mv}$ 分别控制参考条件与多视图一致性的强度。这种并行设计使得模型能同时达成条件遵循与视图间一致性，而非在两者之间折衷。

在定量评估中，Hunyuan3D-Paint 的 CMMD 低至 2.318，显著优于 Paint3D 的 2.651；CLIP-score 达到 0.8893，高于 Paint3D 的 0.8661；LPIPS 为 0.0059，低于 Paint3D 的 0.0085（Table 3）。这些结果表明其在纹理质量与条件对齐上均具有明显优势。

### 3. 适用边界与局限

尽管 Hunyuan3D 2.0 在多个基准上取得了领先结果，其设计选择也划定了适用边界：

- **数据依赖**：纹理合成模型在自采的大规模 3D 数据集上训练，渲染时使用均匀白光照明以适配 delighting 模型。对于极端光照或非自然光照条件下的输入图像，delighting 模块的鲁棒性需要进一步验证。
- **视角选择策略**：训练阶段采用视角丢弃策略（从 44 个预设视角中随机选择 6 个），推理阶段使用基于贪婪覆盖的视角选择。这一策略在覆盖效率与计算开销之间取得了平衡，但对于拓扑结构复杂的网格，可能存在覆盖盲区。
- **纹理补全**：纹理烘焙后的漏洞补全基于顶点权重插值，对于大面积缺失区域，该方法可能产生模糊或失真的纹理。
- **评估局限性**：用户研究涉及 50 名参与者，虽然显示了显著偏好（Figure 10），但主观评估的统计效力有限。此外，形状生成在 Uni3D-T 指标上仅比 Shape Model 3 高 0.0003，优势微弱，需要更多定性分析确认实际差异。

### 4. 开放问题

1. **端到端联合优化**：当前两阶段管道（形状生成 → 纹理合成）是解耦的，形状生成的误差会传播到纹理阶段。是否可以通过端到端训练或中间表示的共享来缓解这一问题？

2. **重要性采样的泛化性**：边缘/角落重要性采样策略在 ShapeVAE 中带来了显著增益，但这一策略是否适用于其他基于点云的 3D 表示学习任务（如点云补全、分类）尚未被验证。

3. **多任务注意力的可解释性**：$\lambda_{ref}$ 和 $\lambda_{mv}$ 的权重设置对生成结果的影响机制尚不明确。是否存在更优的自适应权重调整策略？

4. **纹理重绘能力的上限**：Figure 9 展示了纹理重绘（reskinning）的结果，但在保持几何细节与纹理风格迁移之间的权衡关系缺乏系统分析。

## 原文 PDF
![[paperPDFs/arxiv_2025/Hunyuan3D_2_0_Scaling_Diffusion_Models_for_High_Resolution_Textured_3D_Assets_Generation.pdf]]
