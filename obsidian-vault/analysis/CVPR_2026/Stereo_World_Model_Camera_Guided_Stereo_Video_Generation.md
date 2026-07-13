---
title: "Stereo World Model: Camera-Guided Stereo Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Stereo_World_Model_Camera_Guided_Stereo_Video_Generation.pdf
project_link: "https://sunyangtian.github.io/StereoWorld-web/"
code_link: null
aliases:
- SWMCGSVG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过扩展 Rotary Positional Encoding 的维度并注入相机位姿矩阵，在保留预训练先验的同时实现相对相机条件建模；同时将4D注意力分解为3D视图内注意力和水平行注意力，利用极线约束降低计算量，使得模型能够高效进行立体视频生成。
primary_logic: 立体视频的左右视图差严格沿水平极线分布，利用这一几何先验可将跨视图注意力简化为沿行的注意力，大幅降低计算量；同时通过在RoPE空间中新增相机投影维度而非改变原有编码，能够稳定注入相机条件，保持预训练视频扩散模型的时间一致性。
claims:
- 相比基于单目重建的SOTA方法，StereoWorld实现约3倍生成速度提升，同时视角一致性提高约5%。
- 统一相机帧RoPE使训练更稳定、收敛更快。
- 立体注意力在~50% FLOPs下保持与4D注意力相当的生成质量。
- 在相机准确度、视觉质量和视图同步性上全面优于现有世界模型。
---

# Stereo World Model: Camera-Guided Stereo Video Generation

> [!tip] 核心洞察
> 立体视频的左右视图差严格沿水平极线分布，利用这一几何先验可将跨视图注意力简化为沿行的注意力，大幅降低计算量；同时通过在RoPE空间中新增相机投影维度而非改变原有编码，能够稳定注入相机条件，保持预训练视频扩散模型的时间一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 立体世界模型：相机引导的立体视频生成 |
| 英文题名 | Stereo World Model: Camera-Guided Stereo Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.17375) · [Project](https://sunyangtian.github.io/StereoWorld-web/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | StereoWorld |
| Dataset | Custom Stereo Test Set, VBench |

> [!tip] 效果简介
> - Custom Stereo Test Set (435 samples) 上，FID↓ 111.36 vs 126.83 (Ours Monocular) (-15.47)。
> - Custom Stereo Test Set 上，FVD↓ 83.04 vs 96.87 (Ours Monocular) (-13.83)；Camera RotErr 1.01 vs 1.09 (SEVA) (-0.08)；Camera TransErr↓ 0.11 vs 0.13 (Aether) (-0.02)。
> - VBench 上，Aesthetic Quality↑ 44.27 vs 40.60 (SEVA) (+3.67)。

## 概要

现有世界模型主要围绕单目视频生成构建，缺乏显式的几何约束。当需要输出立体视频时，通常采用“单目生成 + 深度估计 + 图像修复”的后处理流水线，不仅效率低下，而且深度估计与修复误差会在左右视图间累积，导致视角不一致。同时，若直接在视频扩散模型中对所有左-右视图令牌执行4D时空注意力，计算量过大，难以高效实现立体视频生成。

针对上述瓶颈，本文提出 **StereoWorld**——一个端到端的立体世界模型。其核心思路是利用立体视觉的极线几何先验，将跨视图注意力简化为沿水平扫描线的行注意力，大幅降低计算开销；并通过在旋转位置编码（RoPE）空间中注入相机投影矩阵，在不破坏预训练先验的前提下实现统一的相机条件建模。

方法层面，StereoWorld 包含两个关键设计：
1. **统一相机帧 RoPE**：扩展令牌的特征维度，新增相机条件通道，以块对角旋转矩阵的形式将相机位姿参数化注入注意力计算，保持原有 RoPE 的时间-空间分解结构不变，使训练更稳定、收敛更快。
2. **立体感知注意力**：将完整的4D注意力分解为两部分——3D视图内注意力（保持时序与空间建模能力）和水平行注意力（仅在同行的左-右令牌间计算注意力），利用极线约束将计算量降低约50%，同时保持与4D注意力相当的生成质量。

实验结果表明，StereoWorld 在视觉质量、相机准确度和视图同步性上全面优于现有单目世界模型及其后处理立体转换方案。相比基于单目重建的 SOTA 方法，StereoWorld 实现了约3倍的生成速度提升，视角一致性提高约5%。消融实验进一步验证了统一相机帧 RoPE 的稳定性和立体注意力的效率优势。

世界模型旨在从感知输入中学习环境的动态演化规律，并预测未来的感官观测。近年来，基于扩散模型的世界模型在视频生成领域取得了显著进展，催生了一批能够根据相机轨迹生成逼真场景漫游视频的方法。然而，当前主流世界模型几乎全部聚焦于**单目（monocular）视频生成**，其输出模态存在一个根本性的结构缺陷：缺乏显式的、度量级的几何约束。

这一缺陷在实际应用中带来了两个关键问题。其一，单目世界模型生成的视频无法直接适配立体视觉（stereoscopic）显示设备——若要获得立体视频，必须依赖后处理流程：先通过深度估计从单目视频中恢复深度图，再基于深度图进行视图合成和图像修复（inpainting）以生成另一视角。这种多阶段流水线不仅效率低下，而且深度估计误差、修复伪影会在阶段间累积，最终破坏左右视图间的精细一致性（见图2的世界模型模态对比）。其二，缺乏显式几何锚点意味着模型对场景的三维结构理解是隐式且不稳定的，在长序列生成中容易出现漂移和空间不一致。

从技术实现角度看，将世界模型从单目扩展到双目立体面临两个核心瓶颈。**第一，相机条件注入的稳定性问题。** 现有视频扩散模型通常采用 Rotary Positional Encoding（RoPE）来编码时空位置关系，但相机位姿作为一种额外的条件信号，如何在不破坏预训练先验的前提下融入 RoPE 框架，是一个非平凡的设计问题。直接修改原有编码方案可能导致预训练权重失效，而将相机条件作为外部特征注入又难以建立精确的相对位姿关系。**第二，跨视图注意力的计算效率问题。** 立体视频的潜在空间同时包含左右视图的时空 token，若对所有 token 执行全 4D 注意力，计算量将随视图数平方增长，使得训练和推理成本急剧攀升，难以实用化。

本文提出的 **StereoWorld** 正是针对上述缺口，旨在构建一个端到端的、具备内在几何理解的立体世界模型。其核心动机可以概括为：**利用立体视觉的几何先验（极线约束），在保持预训练视频扩散模型时间一致性的同时，高效且稳定地注入相机条件，从而实现视角一致的立体视频直接生成。** 这一设计不仅绕过了后处理流水线的误差累积，还使模型无需显式深度监督即可推理出合理的视差结构，为 VR/AR 可视化、具身智能中的动作规划等下游任务提供了更原生、更高效的解决方案。

## 核心方法与创新机理

StereoWorld 的核心创新围绕一个根本瓶颈展开：**现有单目世界模型缺乏显式几何约束，转换为立体视频的后处理流程依赖深度估计与图像修复，效率低且易累积误差；同时直接在全令牌上执行4D注意力计算量过大，难以高效实现立体视频生成**。针对这一瓶颈，StereoWorld 在两个关键模块上做出了结构性改进——统一相机帧 RoPE 和立体感知注意力分解。

### 瓶颈与因果调控变量

单目世界模型（如 **SEVA** (Zhou et al., arXiv 2025)、**ViewCrafter** (Yu et al., arXiv 2024)）生成的是单视点 RGB 视频，要获得立体输出需经过“深度估计→左右视图重投影→图像修复”的多阶段后处理。这一流程不仅引入深度估计误差和修复伪影，还导致约 3 倍的额外耗时。另一方面，若直接在潜在空间中对左右视图所有 token 执行全 4D 注意力，计算量呈平方级增长，难以实用。

StereoWorld 的**因果调控变量**在于：不改变预训练视频扩散模型的骨干网络，而是通过扩展 Rotary Positional Encoding 的维度并注入相机位姿矩阵，实现相对相机条件建模；同时利用立体视觉的极线约束，将 4D 注意力分解为 3D 视图内注意力和水平行注意力，在保持生成质量的同时大幅降低计算开销。

### 核心洞察：极线先验与 RoPE 空间扩展

立体视频的左右视图差严格沿水平极线分布——这一几何先验是 StereoWorld 设计的核心洞察。跨视图的对应关系几乎完全集中在同一行上，因此跨视图注意力可以被简化为仅在同行的左-右 token 之间计算，无需处理所有 token 对。同时，通过在 RoPE 空间中新增相机投影维度而非改变原有编码，模型能够稳定注入相机条件，保持预训练视频扩散模型的时间一致性。

### 关键改进槽位

#### 改进槽位 1：位置编码方案

| 维度 | 基线方案 | StereoWorld 方案 |
|------|----------|------------------|
| 编码方式 | Vanilla RoPE / M-RoPE（时间-空间三维分解） | 统一相机帧 RoPE：扩展 token 维度插入相机投影矩阵，形成块对角旋转阵 |
| 相机条件 | 无显式相机编码，或通过外部嵌入注入 | 在新增的 $d_c$ 维上施加相机位姿的旋转编码，与原有 RoPE 正交共存 |
| 训练稳定性 | — | 训练更稳定、收敛更快（Fig. 7） |

具体而言，StereoWorld 将查询和键向量的维度从 $d$ 扩展为 $d+d_c$，并在扩展维度上应用相机投影矩阵的旋转：

$$\tilde{\mathbf{R}}_{t,x,y}^{\mathrm{cam}_t}(d+d_c) = \begin{bmatrix} \mathbf{R}_{\Delta t,\Delta x,\Delta y}(d) & \mathbf{0} \\ \mathbf{0} & \mathbf{I}_{d_c/4} \otimes \mathbf{P}_t \end{bmatrix}$$

该块对角矩阵的前 $d \times d$ 块与预训练模型的原始 RoPE 完全一致，保留了预训练先验；新增的 $d_c \times d_c$ 块通过 Kronecker 积 $\mathbf{I}_{d_c/4} \otimes \mathbf{P}_t$ 实现相机投影矩阵的旋转编码。两个 token 之间的相对相机关系由各自绝对位姿旋转矩阵相乘得到：

$$\tilde{\mathbf{R}}_{\Delta t,\Delta x,\Delta y}^{\Delta \mathrm{cam}}(d') = \tilde{\mathbf{R}}_{t_1,x_1,y_1}^{\mathrm{cam}_{t_1}}(d')\ (\tilde{\mathbf{R}}_{t_2,x_2,y_2}^{\mathrm{cam}_{t_2}}(d'))^{\top}$$

消融实验（Table 4）表明，**Copy Init 策略**（将原始 RoPE 的权重复制到新增相机维度进行初始化）在视觉质量和相机精度上均优于 Zero Init 和 Vanilla RoPE，且训练更稳定。

#### 改进槽位 2：跨视图注意力机制

| 维度 | 基线方案 | StereoWorld 方案 |
|------|----------|------------------|
| 注意力范围 | 全 4D 注意力（对所有 left-right-token 执行全局注意力） | 立体感知注意力：3D 视图内注意力 + 水平行注意力 |
| 计算量 | $\mathcal{O}((2 \times f \times h \times w)^2)$ | 约 50% FLOPs（Table 5：1.56 vs 3.11 ×10¹⁰） |
| 生成速度 | 0.34 FPS | 0.49 FPS（约 44% 提升） |

立体感知注意力的输出为两个分量的和：

$$f^{\mathrm{out}} = \mathrm{Attn}_{3\mathrm{D}}(f^{\mathrm{in}}) + \mathrm{Attn}_{\mathrm{row}}(f^{\mathrm{in}})$$

其中 $\mathrm{Attn}_{3\mathrm{D}}$ 在每个视图内独立执行三维（时空）注意力，保持单视图内的时序与空间一致性；$\mathrm{Attn}_{\mathrm{row}}$ 仅在相同时刻的水平对齐 token 之间计算跨视图注意力，利用极线约束实现高效的视差信息融合。消融实验（Table 5）证实，该分解方案在约 50% FLOPs 下保持了与 4D 注意力相当的生成质量。

### 创新价值总结

这两项创新共同构成了 StereoWorld 相对于现有世界模型的核心优势：**统一相机帧 RoPE** 使模型在保留预训练先验的前提下获得相机感知能力，训练稳定且收敛快；**立体感知注意力** 利用极线先验将计算量减半，同时保持视差一致性和生成质量。这使得 StereoWorld 能够以端到端方式直接生成立体视频，相比基于单目重建的 SOTA 方法实现约 3 倍生成速度提升，视角一致性提高约 5%（Table 2），且在相机准确度（RotErr 1.01, TransErr 0.11）和视觉质量（FID 111.36, FVD 83.04）上全面优于现有方法。

StereoWorld 的整体流程围绕“立体视频潜在扩散”构建，其核心设计目标是在保留预训练视频扩散模型时序先验的前提下，高效注入双目几何约束与相机运动条件。整个管线由五个主要模块串联构成，并在可选阶段引入长视频蒸馏以支持自回归生成。

**输入与条件表示。** 系统接收一对经过校正的立体图像 $(\mathbf{I}_{\mathrm{left}}, \mathbf{I}_{\mathrm{right}}) \in \mathbb{R}^{3 \times H \times W}$ 以及一条相机轨迹 $\{\mathsf{cam}_t\} := \{(\mathbf{K}_t \in \mathbb{R}^{3\times3}, \mathbf{T}_t \in \mathbb{R}^{4\times4}), t \in (1,2,\dots,\dot{N})\}$。其中 $\mathbf{K}_t$ 为内参矩阵，$\mathbf{T}_t$ 为外参矩阵，二者共同定义了每一帧的相机位姿。立体图像对提供了度量尺度的基线信息，而相机轨迹则作为“动作”条件驱动未来帧的生成。

**潜在空间压缩。** 立体视频首先通过一个 3D 变分自编码器（3D VAE）编码器 $\mathcal{E}$ 压缩为紧凑的时空潜在表示：
$$\mathbf{z} = \mathcal{E}(\mathbf{V}) \in \mathbb{R}^{f \times h \times w \times c}$$
其中 $f$、$h$、$w$、$c$ 分别对应帧数、高度、宽度和通道数。这一压缩步骤将像素域的双目视频映射到低维潜在空间，为后续 DiT 降噪器提供高效的计算基底。

**统一相机帧 RoPE 注入。** 在潜在变量进入 DiT 之前，StereoWorld 通过扩展 token 维度注入相机位姿条件。具体而言，模型在原有特征维度 $d$ 的基础上外扩 $d_c$ 维，形成扩展后的查询向量 $\widetilde{\mathbf{q}}_{(t,x,y)} \in \mathbb{R}^{d+d_c}$，并将相机投影矩阵 $\mathbf{P}_t$ 嵌入到新增维度的旋转矩阵中。这一设计的关键在于：原有 RoPE 的 $d \times d$ 旋转块保持与预训练权重完全一致，新增的 $d_c \times d_c$ 块则以块对角形式叠加相机条件，形成统一的旋转矩阵：
$$\tilde{\mathbf{R}}_{t,x,y}^{\mathrm{cam}_t}(d+d_c) = \begin{bmatrix} \mathbf{R}_{\Delta t,\Delta x,\Delta y}(d) & \mathbf{0} \\ \mathbf{0} & \mathbf{I}_{d_c/4} \otimes \mathbf{P}_t \end{bmatrix}$$
这种“外扩而非修改”的策略使得模型在稳定继承预训练视频先验的同时，获得了对相对相机运动的感知能力。

**DiT 降噪器与立体感知注意力。** 带噪潜在变量在 DiT 中逐步去噪，其核心是立体感知注意力机制。该机制将朴素的 4D 全注意力（在所有左、右视图 token 间计算全局注意力）分解为两个独立分支：
$$f^{\mathrm{out}} = \mathrm{Attn}_{3\mathrm{D}}(f^{\mathrm{in}}) + \mathrm{Attn}_{\mathrm{row}}(f^{\mathrm{in}})$$
其中 $\mathrm{Attn}_{3\mathrm{D}}$ 在单一视图内执行 3D 时空注意力，$\mathrm{Attn}_{\mathrm{row}}$ 则仅在水平对齐的左右视图 token 对之间计算跨视图注意力。这一分解利用了立体视觉的极线约束——左右视差严格沿水平扫描线分布——从而在约 50% FLOPs 的条件下保持了与 4D 注意力相当的生成质量。

**像素域重建。** 降噪后的潜在表示通过 3D VAE 解码器 $\mathcal{D}$ 重建为像素域立体视频，直接输出左右视图序列，无需后处理深度估计或图像修复。

**长视频蒸馏（可选）。** 为支持长时生成，StereoWorld 采用两阶段蒸馏范式：首先用双向注意力模型生成高质量短片段，再将其蒸馏为因果注意力模型，使推理速度从 0.49 FPS 提升至 5.6 FPS，可自回归生成约 10 秒的立体视频。

整体而言，该框架的关键瓶颈突破在于两点：其一，通过统一相机帧 RoPE 在位置编码空间中注入相机条件，避免了改变原有 RoPE 带来的预训练先验破坏；其二，通过立体感知注意力将 4D 计算量削减近半，使得端到端立体视频生成在计算上可行。

![[assets/figures/papers/paper_list_l2603_https_arxiv_org_abs_2603_17375/figures/003_Figure_2.jpg]]
*Figure 2: World Model Comparison. StereoWorld incorporates metric-scale geometry, producing output modalities that are more compatible with pretrained models. Moreover, it can be applied end-to-end for VR visualization, ensuring better consistency of fine-grained details between the left and right views*

StereoWorld 的核心架构建立在预训练视频扩散模型之上，由 3D VAE 与基于 Transformer 的 DiT 降噪器构成。其关键创新在于两个相互协同的模块：**统一相机帧 RoPE** 与 **立体感知注意力**。前者在不破坏预训练先验的前提下注入相机条件，后者利用极线几何先验大幅降低跨视图注意力计算量。

### 3D VAE 潜在编码

立体视频 $\mathbf{V}$ 首先通过 3D VAE 编码器 $\mathcal{E}$ 压缩为共享时空的潜在表示：

$$\mathbf{z} = {\mathcal{E}}(\mathbf{V}) \in \mathbb{R}^{f \times h \times w \times c}$$

其中 $f$ 为帧数，$h \times w$ 为空间尺寸，$c$ 为通道数。DiT 在此潜在空间中执行去噪，随后由解码器 $\mathcal{D}$ 重建像素域立体视频。

### 统一相机帧 RoPE

现有视频扩散模型采用的 M-RoPE 将位置编码分解为时间、高度、宽度三个独立维度：

$$\mathbf{A}_{(t_1,x_1,y_1),(t_2,x_2,y_2)} = \mathbf{q}_{(t_1,x_1,y_1)} \mathbf{R}_{\Delta t,\Delta x,\Delta y}(d) \mathbf{k}_{(t_2,x_2,y_2)}^{\top}$$

为注入相机条件，StereoWorld 提出**扩展 token 维度**而非修改原有 RoPE。在原有 $d$ 维特征上外扩 $d_c$ 维，形成扩展后的查询向量：

$$\widetilde{\mathbf{q}}_{(t,x,y)} = [\mathbf{q}_{\mathrm{cam}(t,x,y)}] \in \mathbb{R}^{d+d_c}$$

对应的旋转矩阵采用块对角结构，保留原有 RoPE 旋转块并新增相机投影矩阵的旋转：

$$\tilde{\mathbf{R}}_{t,x,y}^{\mathrm{cam}_t}(d+d_c) = \left[\begin{array}{cc} \mathbf{R}_{\Delta t,\Delta x,\Delta y}(d) & \mathbf{0} \\ \mathbf{0} & \mathbf{I}_{d_c/4} \otimes \mathbf{P}_t \end{array}\right]$$

其中 $\mathbf{P}_t$ 由相机外参矩阵 $\mathbf{T}_t$ 的旋转分量构造。两个 token 间的相对相机关系通过绝对位姿旋转矩阵相乘得到：

$$\tilde{\mathbf{R}}_{\Delta t,\Delta x,\Delta y}^{\Delta \mathrm{cam}}(d') = \tilde{\mathbf{R}}_{t_1,x_1,y_1}^{\mathrm{cam}_{t_1}}(d') (\tilde{\mathbf{R}}_{t_2,x_2,y_2}^{\mathrm{cam}_{t_2}}(d'))^{\top}$$

这一设计的核心优势在于：原有 $d \times d$ 块与预训练先验完全对齐，新增的 $d_c \times d_c$ 块作为正交的相机条件通道，实现稳定训练与更快收敛（见图 7 消融验证）。

### 立体感知注意力

立体视频的左右视图差严格沿水平极线分布。基于此几何先验，StereoWorld 将全 4D 注意力分解为两个独立组件：

$$f^{\mathrm{out}} = \mathrm{Attn}_{3\mathrm{D}}(f^{\mathrm{in}}) + \mathrm{Attn}_{\mathrm{row}}(f^{\mathrm{in}})$$

- **$\mathrm{Attn}_{3\mathrm{D}}$（视图内 3D 注意力）**：在每个视图内部执行标准的时空注意力，捕捉时序与空间依赖。
- **$\mathrm{Attn}_{\mathrm{row}}$（水平行注意力）**：仅在同一时刻、同一水平行的左右视图 token 间计算跨视图注意力，利用极线约束将计算范围从全量 token 缩减至行内 token。

消融实验表明，该分解方案在约 50% FLOPs 下取得与 4D 注意力相当的生成质量，FPS 提升约 44%（见表 5）。

![[assets/figures/papers/paper_list_l2603_https_arxiv_org_abs_2603_17375/figures/011_Figure_7.jpg]]
*Figure 7: Comparison of different camera-condition strategies*

## 实验与关键发现

### 主实验结果

StereoWorld 在自建的立体测试集（435个样本）上，与多个前沿世界模型及后处理立体转换方案进行了系统对比。表2汇总了视觉质量、相机准确度、视图同步性及推理速度四个维度的核心指标。

在视觉质量方面，StereoWorld 取得了 **FID 111.36** 和 **FVD 83.04** 的最佳成绩，显著优于单目版本（FID 126.83, FVD 96.87）以及所有对比基线。这表明端到端的立体生成不仅避免了后处理流程中的误差累积，还通过双目视图提供的物理“锚点”提升了生成质量。值得注意的是，单目版本与立体版本使用完全相同的参数量和计算预算，立体版本的优势直接归因于双目几何约束的引入。

在相机准确度上，StereoWorld 实现了最低的旋转误差（**RotErr 1.01**）和平移误差（**TransErr 0.11**），优于 **SEVA**（RotErr 1.09）和 **Aether**（TransErr 0.13）等具有显式相机条件建模的方法。这验证了统一相机帧 RoPE 在注入相机位姿信息方面的有效性——通过将相机投影矩阵嵌入块对角旋转阵，模型能够在保留预训练先验的同时实现精确的相对位姿编码。

视图同步性指标进一步揭示了端到端方法的优势。StereoWorld 的 **FVD-V 22.00** 和 **CLIP-V 97.50** 均大幅领先基于后处理转换的流水线（如 SEVA 的 FVD-V 31.10, CLIP-V 94.73），证明直接生成左右视图能更好地保持细节一致性和色调连贯性，避免深度估计和图像修复引入的伪影。

在推理速度上，StereoWorld 的基础版本达到 **0.49 FPS**，相比多阶段流水线（如 ViewCrafter 的 0.13 FPS）实现了约 **3.8 倍**的提升。这一加速源于模型以端到端方式完成立体视频生成，省去了深度估计、图像修复等中间环节。

在 VBench 基准测试上（表3），StereoWorld 同样展现出全面的质量优势。**Aesthetic Quality 44.27** 和 **Imaging Quality 66.51** 均超越所有对比方法，表明模型不仅具备几何准确性，还能生成符合人类审美的视觉内容。

### 消融实验

#### 相机条件注入策略

表4对比了三种相机条件注入策略：**Vanilla RoPE**（无相机条件）、**Zero Init**（零初始化扩展维度）和 **Copy Init**（复制原有权重初始化扩展维度）。Copy Init 在所有指标上均取得最优成绩——FID 最低，旋转和平移误差最小。图7进一步展示了训练过程中的收敛行为：Copy Init 策略训练更稳定，收敛速度更快。这是因为 Copy Init 保留了预训练权重的结构先验，使新增的相机条件通道能够平滑地融入原有表示空间，而 Zero Init 则需要从头学习相机维度的表示，导致训练初期的不稳定。

#### 注意力机制设计

表5对比了全 4D 注意力与立体感知注意力的性能与效率。立体感知注意力在 **约 50% FLOPs**（1.56×10¹⁰ vs 3.11×10¹⁰）的计算量下，取得了与 4D 注意力相当的生成质量，且 FPS 从 0.34 提升至 **0.49（约 44% 提升）**。这一结果验证了核心假设：立体视频的左右视差严格沿水平极线分布，将跨视图注意力限制在同行的左右 token 之间，几乎不损失信息交互能力，却大幅降低了计算复杂度。

### 失败模式分析

尽管 StereoWorld 在整体指标上表现优异，但仍存在若干值得关注的失败模式：

1. **场景级空间不一致**：部分样例会随时间出现物体位置漂移。图15展示了一个典型案例——序列起始时蓝色路牌并不存在，但随着视角推进，路牌逐渐出现并增大。这是因为模型缺乏显式的场景级一致性约束，仅依赖局部的注意力机制和相机条件，难以保证长序列中的全局空间一致性。

2. **长视频退化**：基础模型在生成长序列时会出现后期质量下降的问题。虽然通过蒸馏为因果注意力模型可将 FPS 提升至 5.6，但该过程存在一定的质量退化。

3. **动态场景局限**：模型主要针对静态场景训练，动态双目视频数据的匮乏限制了其在动态场景下的合成能力。在包含运动物体的场景中，左右视图的时序一致性可能受到影响。

4. **推理速度瓶颈**：尽管蒸馏版本将速度提升至 5.6 FPS，但距离实时交互（通常需 30 FPS 以上）仍有较大差距。如何在保持生成质量的前提下进一步加速推理，是后续研究的重要方向。

### 关键图表结论

- **表2**：StereoWorld 在视觉质量、相机准确度、视图同步性和推理速度上全面超越现有方法，端到端立体生成相比后处理流水线具有显著优势。
- **表3**：VBench 指标验证了模型在美学质量和成像质量上的领先地位。
- **表4**：Copy Init 相机注入策略在训练稳定性和最终性能上均优于 Zero Init 和 Vanilla RoPE。
- **表5**：立体感知注意力以约一半的计算量达到与 4D 注意力相当的生成质量，验证了极线先验的有效性。
- **图7**：统一相机帧 RoPE 使训练更稳定、收敛更快。
- **图15**：失败案例揭示了场景级空间不一致问题，指向未来需要引入空间记忆机制。

![[assets/figures/papers/paper_list_l2603_https_arxiv_org_abs_2603_17375/figures/007_Table_2.jpg]]
*Table 2: Comparison of stereo video with SOTA methods on visual quality, camera accuracy, view synchronization and FPS*

![[assets/figures/papers/paper_list_l2603_https_arxiv_org_abs_2603_17375/figures/009_Table_3.jpg]]
*Table 3: Comparison of stereo video on Vbench metrics*

![[assets/figures/papers/paper_list_l2603_https_arxiv_org_abs_2603_17375/figures/012_Table_4.jpg]]
*Table 4: Ablation on camera injection strategies*

![[assets/figures/papers/paper_list_l2603_https_arxiv_org_abs_2603_17375/figures/013_Table_5.jpg]]
*Table 5: Ablation on attention scheme*

## 定位与知识库关联

### 1. 问题谱系：从单目世界模型到立体世界模型

现有世界模型（world model）的探索主要沿两条路线展开：**单目 RGB 世界模型**和 **RGBD 世界模型**。前者以 **ViewCrafter**（Yu et al., arXiv 2024）和 **SEVA**（Zhou et al., arXiv 2025）为代表，直接从单目视频中学习场景先验，生成新视角下的 RGB 视频；后者如 **Voyager**、**DeepVerse** 和 **Aether**（Aether Team et al., arXiv 2025），通过显式引入深度通道来辅助几何推理。

这两条路线面临一个共同的瓶颈：**它们原生输出的是单目视频**。当需要立体视频（如 VR/AR 应用）时，必须经过后处理流程——先对单目序列进行深度估计，再通过图像修复（inpainting）合成另一视图。这一多阶段管线存在三个系统性缺陷：
1. **误差累积**：深度估计的误差会传递到视图合成，造成左右视图的几何不一致；
2. **效率低下**：多阶段串行处理导致生成速度慢，难以满足交互需求；
3. **细节丢失**：修复过程难以保持跨视图的细粒度纹理一致性和色调连贯性。

**StereoWorld** 的核心定位是：**将世界模型从单目范式直接推进到端到端的立体范式**，通过原生生成左右视图来绕过上述后处理管线。这一转变的关键在于：立体视频的左右视差严格沿水平极线分布，这一几何先验为模型设计提供了强约束。

### 2. 核心技术贡献的方法学定位

StereoWorld 的两个核心模块——**统一相机帧 RoPE** 和 **立体感知注意力**——分别解决了立体世界模型的两个关键挑战：相机条件注入的稳定性和跨视图注意力的计算效率。

#### 2.1 统一相机帧 RoPE：相机条件注入的新范式

在视频扩散模型中注入相机条件是近期世界模型研究的焦点。现有方案大致可分为两类：
- **外部条件注入**：将相机参数通过交叉注意力（cross-attention）或自适应归一化层注入网络，如 ViewCrafter 和 SEVA 的做法；
- **位置编码重参数化**：直接修改 RoPE 的旋转矩阵以编码相机信息。

StereoWorld 的**统一相机帧 RoPE** 采用了第三条路径：**扩展 token 维度而非改变原有编码**。具体而言，在原有 $d$ 维特征空间的基础上外扩 $d_c$ 维，形成块对角旋转矩阵：

$$\tilde{\mathbf{R}}_{t,x,y}^{\mathrm{cam}_t}(d+d_c) = \begin{bmatrix} \mathbf{R}_{\Delta t,\Delta x,\Delta y}(d) & \mathbf{0} \\ \mathbf{0} & \mathbf{I}_{d_c/4} \otimes \mathbf{P}_t \end{bmatrix}$$

其中上方的 $d \times d$ 块与预训练模型的 M-RoPE 完全一致，下方的 $d_c \times d_c$ 块通过相机投影矩阵 $\mathbf{P}_t$ 的 Kronecker 积构造旋转。这一设计的核心优势在于：
- **保留预训练先验**：原有 RoPE 子空间不受扰动，预训练的时间一致性知识得以完整保留；
- **正交注入**：新增的相机条件通道与原有位置通道正交，避免了信息干扰；
- **相对相机建模**：通过 $\tilde{\mathbf{R}}_{\Delta t,\Delta x,\Delta y}^{\Delta \mathrm{cam}}(d') = \tilde{\mathbf{R}}_{t_1,x_1,y_1}^{\mathrm{cam}_{t_1}}(d') (\tilde{\mathbf{R}}_{t_2,x_2,y_2}^{\mathrm{cam}_{t_2}}(d'))^{\top}$，模型学习的是**相对相机位姿关系**，而非绝对位姿，这使其对相机轨迹的泛化能力更强。

消融实验（Table 4）证实，Copy Init 策略（将原始 RoPE 权重复制到相机维度）在 FID 和相机旋转/平移误差上均优于 Zero Init 和 Vanilla RoPE。训练曲线（Figure 7）进一步显示，该策略带来更稳定的训练和更快的收敛。

#### 2.2 立体感知注意力：极线先验驱动的计算约简

跨视图注意力是立体生成的计算瓶颈。朴素方案是在所有左右视图 token 之间执行全 4D 注意力，计算复杂度为 $O((2 \times f \times h \times w)^2)$，在实际部署中难以承受。

StereoWorld 的**立体感知注意力**利用了一个基本的立体几何事实：**校正后的立体对中，对应点严格位于同一水平扫描线上**。基于这一极线先验，将全 4D 注意力分解为两个独立组件：

$$f^{\mathrm{out}} = \mathrm{Attn}_{3\mathrm{D}}(f^{\mathrm{in}}) + \mathrm{Attn}_{\mathrm{row}}(f^{\mathrm{in}})$$

- **3D 视图内注意力** $\mathrm{Attn}_{3\mathrm{D}}$：在每个视图内部执行标准的时空注意力，保持单视图的时序和空间一致性；
- **水平行注意力** $\mathrm{Attn}_{\mathrm{row}}$：仅在相同时刻、相同行的左右 token 之间计算注意力，实现跨视图的视差信息融合。

消融实验（Table 5）表明，该分解方案在约 **50% FLOPs**（$1.56 \times 10^{10}$ vs $3.11 \times 10^{10}$）下保持了与全 4D 注意力相当的生成质量，且 FPS 从 0.34 提升至 0.49（约 **44% 加速**）。这一结果验证了极线先验在立体生成中的有效性：水平行注意力足以捕获视差信息，额外的跨行跨时注意力是冗余的。

### 3. 适用边界与局限

#### 3.1 静态场景偏好

StereoWorld 的训练数据以静态场景为主（TartanAir 等合成数据集占主体，Table 1），动态双目视频数据匮乏。这导致模型对动态物体（行人、车辆等）的合成能力受限。在具身场景（Figure 11）中虽展示了初步效果，但动态场景下的视差一致性和时序稳定性仍需验证。

#### 3.2 长时生成退化

尽管通过 Self-Forcing 蒸馏将推理速度提升至 5.6 FPS（Figure 12），长视频生成仍存在后期质量退化问题。这主要源于：模型缺乏显式的场景级记忆机制，无法在长时间跨度内保持全局空间一致性。典型失败案例如 Figure 15 所示：蓝色路牌在序列起始时不存在，随视角推进逐渐出现并增大——这是场景级空间不一致的典型表现。

#### 3.3 推理速度与实时性

端到端版本的推理速度为 0.49 FPS，虽比多阶段管线快约 3 倍，但距离实时交互（>30 FPS）仍有数量级差距。蒸馏版本虽提升至 5.6 FPS，但存在质量退化，且论文未量化该退化程度。

#### 3.4 相机位姿评估的外部依赖

相机准确度评估依赖 VGGT 估计的位姿作为参考，这一第三方位姿估计器本身的精度会影响评估结果的可靠性。论文未报告 VGGT 在测试集上的位姿估计误差，因此相机准确度的绝对数值需谨慎解读。

### 4. 开放问题与未来方向

1. **动态立体视频数据获取**：如何高效收集或合成大规模动态双目视频数据，是扩展模型适用场景的关键瓶颈。可能的路径包括：利用游戏引擎渲染（类似 TartanAir 的扩展）、从单目动态视频通过立体匹配合成伪标签、或利用轻量级双目采集设备众包数据。

2. **长时一致性的空间记忆机制**：当前模型缺乏对已生成区域的显式记忆，导致长序列中出现物体"凭空出现"或位置漂移。引入空间记忆机制（如 VMem、SPMem 等）来维护场景级特征缓存，是提升长时一致性的直接方向。

3. **高质量实时蒸馏**：当前蒸馏方案在速度和质量之间存在权衡。探索更先进的蒸馏策略（如对抗蒸馏、一致性模型）以在保持生成质量的同时逼近实时推理，是推动 VR/AR 应用落地的关键。

4. **显式几何监督的引入**：StereoWorld 的一个有趣特性是：**无需深度监督即可隐式学习视差**（Figure 6）。引入轻量级的显式几何监督（如稀疏视差图或点云）是否能进一步提升几何精度和泛化能力，值得探索。

5. **与具身智能的深度整合**：立体世界模型为具身智能提供了天然的双目观测先验。如何将 StereoWorld 与策略学习（policy learning）或模型预测控制（MPC）结合，在导航和操作任务中发挥双目几何感知的优势，是一个具有潜力的交叉方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Stereo_World_Model_Camera_Guided_Stereo_Video_Generation.pdf]]
