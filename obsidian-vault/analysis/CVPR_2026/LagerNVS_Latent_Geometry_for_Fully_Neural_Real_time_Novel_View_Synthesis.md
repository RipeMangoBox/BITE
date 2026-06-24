---
title: "LagerNVS: Latent Geometry for Fully Neural Real-time Novel View Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LagerNVS_Latent_Geometry_for_Fully_Neural_Real_time_Novel_View_Synthesis.pdf
project_link: null
code_link: null
aliases:
- LagerNVS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将编码器初始化为使用显式3D监督预训练的 VGGT 模型，使潜在特征隐含 3D 感知能力；并采用高速公路编码器-解码器架构，最大化源图像到潜在表示的信息流。
primary_logic: 即使不进行显式 3D 重建，通过引入由显式 3D 监督预训练所获得的 3D 感知特征，并配合无瓶颈的高速公路编码器-解码器设计，可以在保持实时解码速度的同时大幅提升 NVS 质量。
claims:
- 使用 VGGT 预训练的 3D 感知特征比从头训练高出 +2.9 dB PSNR。
- 高速公路编码器-解码器优于解码器唯一和瓶颈编码器-解码器。
- 端到端微调整个模型（解冻 VGGT）比冻结主干网络提升约 2.01 dB。
- LagerNVS 以 +1.7 dB 显著超越先前最优 LVSM。
---

# LagerNVS: Latent Geometry for Fully Neural Real-time Novel View Synthesis

> [!tip] 核心洞察
> 即使不进行显式 3D 重建，通过引入由显式 3D 监督预训练所获得的 3D 感知特征，并配合无瓶颈的高速公路编码器-解码器设计，可以在保持实时解码速度的同时大幅提升 NVS 质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | LagerNVS：用于全神经实时新视角合成的潜在几何 |
| 英文题名 | LagerNVS: Latent Geometry for Fully Neural Real-time Novel View Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.20176) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | LagerNVS |
| Dataset | RealEstate10k, DL3DV 4-view, RealEstate10k 2-view, DL3DV 6-view |

> [!tip] 效果简介
> - RealEstate10k 上，PSNR 31.39 (LagerNVS highway-full, batch 512) vs 29.67 (LVSM decoder-only, batch 512) (+1.72)。
> - DL3DV 4-view 上，PSNR 27.56 vs 22.30 (DepthSplat) (+5.26)。
> - RealEstate10k 2-view (unposed) 上，PSNR 25.54 (Ours v2) vs 24.06 (NoPoSplat) (+1.48)。

## 概述

新视角合成（Novel View Synthesis, NVS）旨在从一组稀疏的源图像生成任意新视角下的场景画面。现有方法大致分为三类：基于显式 3D 重建的方法（如 3D Gaussian Splatting）几何保真度高但难以实时泛化；纯 2D 生成式方法灵活但缺乏几何一致性；而重建-free 的编码器-解码器方法虽能实时渲染，却因缺乏足够的 3D 归纳偏置，在新视角合成的几何一致性与细节保真度上始终存在瓶颈。

LagerNVS 针对这一瓶颈提出了一个关键洞察：**即使不进行显式 3D 重建，通过引入由显式 3D 监督预训练所获得的 3D 感知特征，并配合无信息瓶颈的高速公路编码器-解码器设计，可以在保持实时解码速度的同时大幅提升 NVS 质量**。具体而言，LagerNVS 将编码器初始化为使用显式 3D 监督预训练的 VGGT 模型，使潜在特征隐含 3D 感知能力；同时采用高速公路（highway）编码器-解码器架构，为每张源图像保留独立的特征 token，最大化源图像到潜在表示的信息流，避免了瓶颈式架构的信息损失。

在标准基准 RealEstate10k 上，LagerNVS 以 **31.39 dB PSNR** 显著超越先前最优的重建-free 方法 LVSM（29.67 dB），提升幅度达 **+1.72 dB**。在 DL3DV 数据集上，LagerNVS 相较于前馈 3DGS 方法 DepthSplat 的优势更为突出：4 视图设定下领先 **+5.26 dB**，6 视图设定下领先 **+5.98 dB**。即使在不提供源相机位姿的设定下，LagerNVS 同样优于 NoPoSplat 等无位姿前馈 3DGS 方法（+1.48 dB）。消融实验进一步揭示了性能增益的因果链条：VGGT 的 3D 预训练贡献 **+2.9 dB**，高速公路架构相较于解码器唯一设计贡献 **+2.63 dB**，端到端微调（解冻 VGGT 主干）相较于冻结编码器贡献 **+2.01 dB**。这些结果共同验证了“3D 感知预训练 + 高速公路架构 + 端到端微调”这一组合策略的有效性。

在方法谱系上，LagerNVS 属于重建-free 的编码器-解码器 NVS 范式，与 **LVSM**（Jin et al., ECCV 2024）构成直接对标，同时与基于前馈 3DGS 的方法如 **AnySplat**（Chen et al., CVPR 2025）、**DepthSplat**（Xu et al., CVPR 2024）、**NoPoSplat**（Ye et al., ECCV 2024）以及编码器-解码器缩放研究 **SVSM**（Chen et al., arXiv 2025）形成横向比较。LagerNVS 的核心区分点在于：以显式 3D 监督预训练的 VGGT 作为编码器初始化源，而非依赖随机初始化或 2D 自监督预训练（如 DinoV2），从而在潜在空间中注入了更强的 3D 结构先验。

## 背景与动机

### 问题背景

新视角合成（Novel View Synthesis, NVS）旨在从一组稀疏的源图像中渲染任意目标视角的逼真图像。该任务在增强现实、虚拟现实、具身智能和内容创作等领域具有广泛的应用前景。近年来，前馈式 NVS 方法因其无需逐场景优化的推理效率而受到广泛关注。这类方法的核心范式是将 NVS 建模为编码器-解码器架构：

$$z = e(I_1, g_1, \ldots, I_V, g_V), \quad I = h(z; g).$$

其中编码器 $e$ 将 $V$ 张源图像及其（可选的）相机参数 $g_i$ 映射为中间表示 $z$，解码器 $h$ 则在给定目标相机 $g$ 的条件下从 $z$ 渲染目标视图 $I$。

### 现有方法缺口

当前的前馈式 NVS 方法主要存在两类瓶颈：

**1. 缺乏足够的 3D 归纳偏置。** 现有重建-free NVS 模型的编码器通常采用随机初始化或仅依赖 2D 自监督预训练（如 DinoV2），缺乏对场景三维结构的显式感知能力。这导致模型在新视角合成中难以保持几何一致性，尤其在遮挡边界、薄结构和高频纹理区域表现不佳。相比之下，显式 3D 重建方法虽能提供更强的几何约束，但其重建过程计算代价高昂，难以满足实时渲染需求。

**2. 架构设计未能充分利用多视图 3D 线索。** 先前的最优方法 **LVSM** 采用解码器唯一（decoder-only）架构，将源图像信息仅通过交叉注意力注入解码器，编码器与解码器之间存在严重的信息瓶颈。而瓶颈编码器-解码器（bottleneck encoder-decoder）虽然引入了编码器，但其潜在 token 数量与源视图数 $V$ 无关，限制了多视图信息的表达能力。这两种设计均未能最大化从源图像到潜在表示的信息流，同时保持实时解码速度。

### 核心动机与洞察

本文的核心洞察是：**即使不进行显式 3D 重建，通过引入由显式 3D 监督预训练所获得的 3D 感知特征，并配合无瓶颈的高速公路编码器-解码器（highway encoder-decoder）设计，可以在保持实时解码速度的同时大幅提升 NVS 质量。**

具体而言，该洞察包含三个关键要素：

- **3D 感知预训练**：将编码器初始化为使用显式 3D 监督预训练的 VGGT 模型权重，使潜在特征隐含 3D 感知能力，为解码器提供更强的几何先验。
- **高速公路架构**：采用高速公路编码器-解码器，为每张源图像保留独立的特征 token（$z = (z_1, \ldots, z_V)$），消除信息瓶颈，最大化源图像到潜在表示的信息流。
- **端到端微调**：在 NVS 任务上端到端微调整个模型（包括 VGGT 主干），使 3D 预训练特征适应外观渲染需求。

基于上述动机，本文提出 **LagerNVS**，一种全神经、前馈、实时的 NVS 方法，旨在以确定性推理实现最先进的合成质量，同时保持超过 30 FPS 的实时渲染速度。

## 核心创新

LagerNVS 的核心创新在于将**显式 3D 监督预训练**获得的 3D 感知能力注入到完全神经的 NVS pipeline 中，并配合**高速公路编码器-解码器架构**，在保持实时解码速度的同时大幅提升新视角合成质量。其关键设计围绕以下四个 changed slots 展开。

### 1. 编码器预训练：从 3D 重建中继承几何先验

现有重建-free NVS 方法（如 **LVSM**）的编码器通常采用随机初始化或 2D 自监督预训练（如 DinoV2），缺乏对三维结构的显式理解。LagerNVS 直接使用 **VGGT** 的预训练权重初始化编码器主干网络——VGGT 是一个以显式 3D 监督训练的 3D 重建模型。

这一设计的因果机制在于：VGGT 的中间特征已经隐含了丰富的 3D 几何信息（如深度、对应关系、表面朝向），编码器无需从零学习这些底层表征，而是直接将其转化为对 NVS 有用的潜在表示。消融实验给出了决定性证据：从 VGGT 初始化的模型比从头训练高出 **+2.9 dB PSNR**（Table 2, row (a) vs row (e)），且该增益远大于架构选择本身带来的差异。

### 2. 高速公路编码器-解码器：消除信息瓶颈

传统编码器-解码器 NVS 方法存在两种设计范式：**瓶颈式**（bottleneck）将多视图信息压缩为固定数量的 token，与源视图数 V 解耦；**解码器唯一式**（decoder-only，如 LVSM）则完全放弃编码器，直接在解码器中处理源图像。前者存在信息瓶颈，后者限制了编码器扩展能力。

LagerNVS 提出**高速公路编码器-解码器**（highway encoder-decoder），为每个源图像保留独立的特征向量 $z = (z_1, \ldots, z_V)$，最大化从源图像到潜在表示的信息流。消融实验表明，高速公路架构比解码器唯一式提升 **+2.63 dB PSNR**（Table 2, row (a) vs row (c)），且优于瓶颈式变体。

### 3. 解码器注意力机制：从 $O(V^2)$ 到 $O(V)$ 的实时化

完全自注意力将所有场景 token 和目标相机 token 拼接后计算注意力，复杂度为 $O(V^2)$，在多视图场景下难以实时。LagerNVS 采用**双向交叉注意力**：

$$
q_1 = s; \quad k_1 = v_1 = (z_1, \ldots, z_V), \quad \text{and} \quad q_2 = (z_1, \ldots, z_V); \quad k_2 = v_2 = s
$$

第一层让目标相机 token $s$ 关注所有场景 token，第二层让场景 token 关注相机 token，复杂度降至 $O(V)$。该设计在 2 视图下仅比完全注意力低 0.28 dB PSNR（Table A3），但实现了 1–9 视图下 56–30 FPS 的实时渲染。

### 4. 端到端微调策略：释放预训练特征的潜力

仅冻结 VGGT 编码器进行训练会导致性能次优，因为 VGGT 的预训练目标（3D 重建）与 NVS 目标（外观渲染）存在差异。LagerNVS 采用**端到端微调**（E2E），解冻 VGGT 主干网络，使 3D 感知特征在 NVS 任务上自适应优化。消融实验表明，端到端微调比冻结 VGGT 提升 **+2.01 dB PSNR**（Table 2, row (a) vs row (g)），证明预训练特征需要针对渲染任务进行适配才能发挥最大效用。

### 创新点的协同效应

上述四个 changed slots 并非孤立改进，而是形成协同效应：3D 预训练提供了高质量的初始特征空间，高速公路架构保证了这些特征无损传递，交叉注意力在保持实时性的同时实现充分交互，端到端微调则弥合了重建与渲染之间的任务鸿沟。这一组合使 LagerNVS 在 RealEstate10k 上以 **+1.72 dB** 显著超越先前最优 LVSM（31.39 vs 29.67 PSNR，Table 1），并在 DL3DV 等多场景基准上以超过 5 dB 的优势领先前馈 3DGS 方法（Table 3）。

## 整体框架

LagerNVS 采用**编码器-解码器**架构，将新视角合成 (NVS) 分解为两个阶段：编码器 $e$ 从任意数量的源图像（及可选相机参数）中提取中间潜在表示 $z$，解码器 $h$ 则根据目标相机位姿 $g$ 将该表示渲染为目标视图 $I$：

$$z = e(I_1, g_1, \ldots, I_V, g_V), \quad I = h(z; g).$$

### 输入与输出

模型输入为 $V$ 张源图像 $\{I_1, \ldots, I_V\}$，以及可选的对应相机参数 $\{g_1, \ldots, g_V\}$。当相机位姿未知时，模型采用规范水平视场角 $k_0 = 53.13^\circ = \arctan(0.5)$ 作为默认内参，使水平焦距等于图像宽度。输出为与目标相机 $g$ 对应的 512×512 RGB 图像，在单张 H100 GPU 上以超过 30 FPS 的速率实时渲染（1–9 张源图像时）。

### 编码器：3D 感知潜在特征提取

编码器基于 **VGGT** 预训练模型构建。VGGT 是一个使用显式 3D 监督训练的重建网络，其主干为高容量 Transformer。具体流程为：

1. **图像与相机 token 化**：源图像被上采样至 VGGT 期望的输入尺寸；相机参数 $g$ 通过一个 2 层 MLP 投影为 1024 维的条件 token。
2. **VGGT 主干前向传播**：图像 token 与相机 token 一同输入 VGGT 的 Transformer 主干（使用 VGGT 预训练权重初始化）。
3. **特征提取**：从 VGGT 最后若干层的局部注意力层和全局注意力层中提取 token（丢弃相机 token 后拼接），再通过线性投影映射到解码器的通道维度 $C$，形成最终的潜在 3D 表示 $z = (z_1, \ldots, z_V)$，其中 $z_i \in \mathbb{R}^{P \times C}$ 对应第 $i$ 张源图像。

该设计的关键在于：VGGT 的预训练权重赋予了编码器内在的 **3D 感知能力**，使得潜在特征 $z$ 隐含几何与外观信息，而无需显式 3D 重建。

### 解码器：目标视图渲染

解码器采用 **ViT-B** Transformer，配合 FlashAttention 注意力内核以加速推理。其输入为：

- **场景 token**：编码器输出的潜在 3D 表示 $(z_1, \ldots, z_V)$。
- **目标相机 token $s$**：目标相机位姿以 **Plücker 射线图** 形式密集表示并 token 化。

解码器通过注意力机制融合场景 token 与目标相机 token，随后丢弃寄存器 token 和场景 token，仅保留目标相机 token 经线性层投影为 8×8 的 RGB patch，最终重塑为完整的目标视图。

### 架构变体：高速公路编码器-解码器

LagerNVS 的核心架构创新在于**高速公路编码器-解码器**设计（Figure 4）。与瓶颈式编码器-解码器（token 数量与源视图数 $V$ 无关）不同，高速公路架构为每张源图像保留独立的 token 向量，最大化从源图像到潜在表示的信息流，避免了信息瓶颈。同时，与解码器唯一模型（如 **LVSM**）相比，该架构允许在不拖慢解码速度的前提下扩展编码器容量。

解码器注意力机制提供两种变体：

- **完全注意力**：$q = k = v = (s, z_1, \dotsc, z_V)$，复杂度 $O(V^2)$。
- **双向交叉注意力**：先由相机 token 关注场景 token，再由场景 token 关注相机 token：
  $$q_1 = s; \quad k_1 = v_1 = (z_1, \ldots, z_V),$$
  $$q_2 = (z_1, \ldots, z_V); \quad k_2 = v_2 = s.$$
  该变体复杂度为 $O(V)$，在 2 视图下仅比完全注意力低 0.28 dB PSNR，但允许在 1–9 视图下保持 56–30 FPS 的实时渲染。

### 训练策略

模型采用端到端训练，损失函数为 L2 损失与感知损失 (LPIPS) 的加权组合：

$$\mathcal{L} = \lambda_2 \mathcal{L}_2 + \lambda_p \mathcal{L}_p.$$

消融实验表明，**解冻 VGGT 主干进行端到端微调**比冻结编码器提升约 +2.01 dB PSNR，说明让 3D 预训练特征适应 NVS 任务至关重要。

### 补充图表

![[assets/figures/papers/paper_list_l2260_https_arxiv_org_abs_2603_20176/figures/002_Figure_2.jpg]]
*Figure 2: Method. The model takes any number of images and, optionally, their camera parameters as input. A large network initialized from a reconstruction model [70] outputs an intermediate feature representation with implicit 3D information. A lightweight network is queried on a target camera pose and renders a 512×512 image at more than 30 FPS on a single H100 GPU when provided with up to 9 input images*

## 核心模块与公式推导

LagerNVS 将新视角合成形式化为一个编码器-解码器框架，其核心公式为：

$$z = e(I_1, g_1, \ldots, I_V, g_V), \quad I = h(z; g).$$

其中，编码器 $e$ 将 $V$ 张源图像 $I_i$ 及其对应的相机参数 $g_i$ 映射为中间潜在表示 $z$；解码器 $h$ 以 $z$ 和目标相机参数 $g$ 为条件，渲染出目标视角图像 $I$。这一分离设计使得编码过程与目标相机无关，解码器可在给定 $z$ 后独立查询任意目标视角。

### 编码器：3D 感知潜在特征提取

编码器的核心设计在于利用 **VGGT** 作为预训练主干网络。VGGT 是一个经过显式 3D 监督预训练的重建模型，其权重为编码器提供了强 3D 归纳偏置。具体流程如下：

1. **输入处理**：源图像被上采样至 VGGT 期望的输入尺寸；相机参数 $g$ 通过一个 2 层 MLP 投影为 1024 维的条件 token。
2. **Token 提取**：图像 token 与相机 token 一同送入 VGGT 的 Transformer 主干。编码器从 VGGT 的最后局部注意力层和全局注意力层中提取 token 数组 $z_i \in \mathbb{R}^{P \times C}$（丢弃相机 token 后拼接），再投影至解码器所需的通道维度 $C$，形成最终的潜在 3D 表示 $(z_1, \ldots, z_V)$。

这种“高速公路”编码器设计保留了每个源图像的独立 token，避免了瓶颈编码器因固定 token 数量而导致的信息压缩，使潜在表示 $z$ 的容量随源视图数 $V$ 线性增长。

### 解码器：双向交叉注意力与实时渲染

解码器采用 ViT-B 架构，其关键创新在于注意力机制的选择。给定目标相机 token $s$（由 Plücker 射线图密集表示）和场景 token $(z_1, \ldots, z_V)$，论文对比了两种注意力变体：

**完全注意力变体**将所有 token 拼接后执行自注意力：

$$q = k = v = (s, z_1, \dotsc, z_V).$$

该变体质量最高，但计算复杂度为 $O((V+1)^2)$，限制了可支持的源视图数量。

**双向交叉注意力变体**将交互分解为两层：

$$q_1 = s; \quad k_1 = v_1 = (z_1, \ldots, z_V),$$
$$q_2 = (z_1, \ldots, z_V); \quad k_2 = v_2 = s.$$

第一层让目标相机 token 关注所有场景 token，第二层让场景 token 关注目标相机 token。复杂度降为 $O(V)$，在 2 视图下仅比完全注意力低 0.28 dB PSNR（Table A3），但支持最多 9 视图的实时渲染（56–30 FPS）。

解码器输出经线性层投影为 $8 \times 8$ 的 patch，再重塑为目标分辨率图像。

### 训练损失

模型以组合损失端到端训练：

$$\mathcal{L} = \lambda_2 \mathcal{L}_2 + \lambda_p \mathcal{L}_p,$$

其中 $\mathcal{L}_2$ 为像素级 L2 损失，$\mathcal{L}_p$ 为感知损失（LPIPS），$\lambda_2$ 和 $\lambda_p$ 为加权系数。消融实验表明，端到端微调整个模型（解冻 VGGT 主干）比冻结编码器提升约 2.01 dB PSNR，证明 3D 预训练特征需要针对 NVS 任务进行适应性调整才能充分发挥作用。

### 补充图表

![[assets/figures/papers/paper_list_l2260_https_arxiv_org_abs_2603_20176/figures/004_Figure_4.jpg]]
*Figure 4: Architectures. Our highway encoder-decoder (left) maximizes information flow from source images to the latent representation (R), making it more expressive than the bottleneck encoder-decoder (middle). Unlike decoder-only models (right), our design allows scaling the encoder without slowing decoding*

## 实验与分析

### 核心定量结果

LagerNVS 在标准确定性新视角合成基准上全面超越先前最优方法。在 RealEstate10k 数据集上，LagerNVS 以 **31.39 PSNR** 显著领先前最优重建-free 方法 **LVSM** 的 29.67 PSNR，提升 **+1.72 dB**（Table 1，batch size 512）。这一优势在较小训练规模（batch size 64）下同样保持。

在与前馈 3D Gaussian Splatting（3DGS）方法的对比中，LagerNVS 的优势更为突出：
- **DL3DV 4-view**：27.56 PSNR vs DepthSplat 的 22.30 PSNR（**+5.26 dB**）
- **DL3DV 6-view**：29.45 PSNR vs DepthSplat 的 23.47 PSNR（**+5.98 dB**）
- **RealEstate10k 2-view（无位姿）**：25.54 PSNR vs NoPoSplat 的 24.06 PSNR（**+1.48 dB**）

这些结果表明，潜在 3D 表示在无显式重建的情况下即可提供更强的几何一致性。需注意，NoPoSplat 仅在 RealEstate10k 上训练，与其他在更大数据混合上训练的模型可能存在不对等比较，但论文已明确标注。

### 消融实验：三大关键设计

消融实验（Table 2）系统解耦了 LagerNVS 性能提升的三个因果旋钮：

![[assets/figures/papers/paper_list_l2260_https_arxiv_org_abs_2603_20176/figures/009_Table_2.jpg]]
*Table 2: Ablations. Even when handicapped by using faster crossattention, our highway encoder-decoder model outperforms the decoder-only and bottleneck encoder-decoder variants, which are analogous to the models introduced by LVSM [34]. Using 3Daware pre-training (Pre-tr.) is crucial, but only effective if the features are fine-tuned end-to-end (“E2E”)*

**1. 3D 感知预训练（+2.9 dB）**
将编码器初始化为 VGGT 预训练权重（row a）相比从头训练（row e）提升 +2.9 dB PSNR。这验证了核心洞察：显式 3D 监督预训练所获得的 3D 感知特征，即使不进行显式重建，也能为 NVS 提供关键的几何归纳偏置。

**2. 高速公路编码器-解码器架构（+2.63 dB）**
高速公路架构（row a，21.02 PSNR）相比解码器唯一变体（row c，18.39 PSNR）提升 +2.63 dB。这证明保留每个源图像的独立 token、避免信息瓶颈，对最大化源图像到潜在表示的信息流至关重要。瓶颈编码器-解码器（row b）表现介于两者之间，其唯一优势是解码速度与源视图数无关，但在质量上不及高速公路设计。

**3. 端到端微调（+2.01 dB）**
解冻 VGGT 主干进行端到端微调（row a，21.02 PSNR）相比冻结编码器（row g，19.01 PSNR）提升 +2.01 dB。这表明，尽管 VGGT 预训练提供了强大的初始化，但让 3D 特征适应 NVS 任务的像素级外观需求同样不可或缺。

定性对比（Figure 7）进一步佐证：同时具备高速公路架构、3D 预训练和端到端微调的模型，在几何一致性和细节保真度上均明显优于缺失任一组件的变体。

![[assets/figures/papers/paper_list_l2260_https_arxiv_org_abs_2603_20176/figures/008_Figure_7.jpg]]
*Figure 7: Ablations. Our architecture (1), pre-training (2) and end-to-end training (3) result in the best NVS quality*

### 解码器注意力机制的效率-质量权衡

解码器注意力变体的对比（Table A3）揭示了实时性与质量之间的可控权衡：
- **完全自注意力**：2 视图下 21.30 PSNR，但复杂度为 O(V²)，无法支持多视图实时渲染。
- **双向交叉注意力**：2 视图下 21.02 PSNR（仅低 0.28 dB），复杂度降为 O(V)，支持 1–9 视图下 **56–30 FPS** 的实时渲染。
- **单向交叉注意力**：质量进一步下降，但速度更快。

![[assets/figures/papers/paper_list_l2260_https_arxiv_org_abs_2603_20176/figures/019_Table.jpg]]
*Table: A3. Decoder attention variants. The bidirectional cross-attention mechanism used for the main model offers a good trade-off between real-time rendering speed and NVS quality*

LagerNVS 最终采用双向交叉注意力，在保持实时解码的前提下最大化渲染质量。

### 与前馈 3DGS 的定性对比

定性结果（Figure 8, Figure A2）显示，LagerNVS 在多个具有挑战性的场景中优于前馈 3DGS 方法：
- **薄结构**：金属杆、椅子扶手等细薄结构重建更完整。
- **反射区域**：镜面和桌面的反射表现更准确。
- **遮挡处理**：地板遮挡区域和行李箱把手等结构的表面连续性更好。
- **位姿灵活性**：支持有/无源相机位姿两种推理模式，而多数 3DGS 方法依赖已知位姿。

![[assets/figures/papers/paper_list_l2260_https_arxiv_org_abs_2603_20176/figures/011_Figure_8.jpg]]
*Figure 8: Comparison to feed-forward 3DGS. Our model better handles thin parts, reflections, and occlusions, and supports inference with and without source camera poses*

![[assets/figures/papers/paper_list_l2260_https_arxiv_org_abs_2603_20176/figures/015_Figure.jpg]]
*Figure: A2. Qualitative comparison vs Feed-forward 3DGS. Our model more accurately represents reflective areas (mirror, top row and table, second row) and thin structures (metal rod, top row and chair arm, second row). The global, latent representation leads to better surface alignment (suitcase handle, third row and teddy bear, bottom row) and is more robust to occlusions (floor, third row)*

### 与 LVSM 的深入对比

相比 LVSM，LagerNVS 的改进体现在两个维度（Figure 5, Figure A1）：
- **几何估计**：在 2D 匹配困难的区域（如重复纹理、遮挡边界），LagerNVS 保持更一致的形状估计。
- **单目线索利用**：更好地利用单目深度线索进行深度推理，表明 VGGT 预训练赋予了更强的单目 3D 理解能力。

![[assets/figures/papers/paper_list_l2260_https_arxiv_org_abs_2603_20176/figures/006_Figure_5.jpg]]
*Figure 5: Comparison to LVSM. Our model estimates geometry better than LVSM in regions where 2D matching is challenging (top). It also uses monocular cues better for depth (bottom)*

![[assets/figures/papers/paper_list_l2260_https_arxiv_org_abs_2603_20176/figures/014_Table.jpg]]
*Table: Figure A1. Additional comparison vs LVSM. Our model better maintains consistent shape in regions where 2D matching across inputs is challenging (top 2 rows) and shows better monocular depth estimation (bottom row). Table A2. LagerNVS outperforms SVSM due to greater model capacity and 3D pre-training*

### 失败模式与局限性

尽管整体性能优异，LagerNVS 存在以下已知失败模式：
- **未观测区域**：渲染结果模糊，存在块状伪影，视频生成时可能出现 flicker 现象。
- **高频纹理**：草地、树木等高频纹理区域重建质量较差。
- **相机内参假设**：模型假设所有源图像具有相同内参且与目标相机一致，不同内参或不一致内参会导致性能下降。
- **场景限制**：仅适用于静态场景，训练数据未包含人类或鱼眼等畸变图像。

对于复杂遮挡场景，模型倾向于产生“均值回归”式的模糊补全（Figure A3），这在确定性框架下是预期行为——扩散解码器的初步实验（Figure 9）展示了通过生成式方法改善未观测区域补全质量的潜力。

![[assets/figures/papers/paper_list_l2260_https_arxiv_org_abs_2603_20176/figures/010_Figure_9.jpg]]
*Figure 9: Diffusion. Our decoder can be fine-tuned with a diffusion objective, enabling hallucination of unobserved regions*

![[assets/figures/papers/paper_list_l2260_https_arxiv_org_abs_2603_20176/figures/016_Figure.jpg]]
*Figure: Input 1 Input 2 Novel View Figure A3. Occlusions. Our model can handle simple occlusions, such as the corner of the bathtub (top) or the bottom part of the black box (middle). In more difficult settings (bottom), completions are blurry (as expected), but still reasonable*

### 补充图表

![[assets/figures/papers/paper_list_l2260_https_arxiv_org_abs_2603_20176/figures/007_Table_3.jpg]]
*Table 3: Feed-forward 3DGS comparison. Our model outperforms state-of-the-art feed-forward 3DGS models across the board, both with and without input camera poses available, illustrating the strength of latent 3D representations. NoPoSplat only trained on RealEstate10k (a potentially unfair comparison), but we include it here for completeness. See Sec. C.3 for details of ‘Ours (v2)’*

## 方法谱系与知识库定位

### 重建-free 新视角合成的演进脉络

LagerNVS 处于**重建-free 新视角合成（NVS）**这一研究脉络中。该脉络的核心思路是绕过显式三维重建（如点云、网格或 3D Gaussian），直接由神经网络从源图像预测目标视角。这一范式在近年来经历了从“光场编码器-解码器”到“前馈 3DGS”再到“全神经潜在表示”的演进。

早期代表性工作如 **SRT**（Sajjadi et al., ICCV 2023）采用前馈光场编码器-解码器架构，将场景压缩为潜在表示后解码渲染，但其编码器缺乏显式的 3D 监督信号。**LVSM**（Jin et al., ECCV 2024）将这一思路推向当时最优，通过潜在编码器-解码器设计在 RealEstate10k 上取得 29.67 PSNR，但其架构选择——解码器唯一或瓶颈编码器-解码器——在信息流和渲染速度之间存在取舍，未能充分利用多视图 3D 线索。

另一条并行脉络是**前馈 3D Gaussian Splatting**，代表性工作包括 **AnySplat**（Zhang et al., arXiv 2025）、**Flare**（Jin et al., CVPR 2025）、**DepthSplat**（Xu et al., ECCV 2024）和 **NoPoSplat**（Ye et al., CVPR 2025）。这些方法通过前馈网络预测 3DGS 参数，再通过光栅化渲染，在几何一致性上具有天然优势。然而，它们对薄结构、反射区域和遮挡的处理仍存在困难，且多数要求已知相机位姿。

### LagerNVS 的方法定位与核心区分

LagerNVS 在方法谱系中的定位是**全神经、潜在几何驱动的重建-free NVS**。其与前述工作的本质区分在于三个关键设计：

**1. 3D 感知预训练编码器。** 与 LVSM 的随机初始化或 2D 自监督预训练（如 DinoV2）不同，LagerNVS 将编码器初始化为 **VGGT**（Wang et al., CVPR 2025）的预训练权重。VGGT 是一个使用显式 3D 监督（深度、相机位姿）训练的高容量重建网络。这一设计使潜在特征从训练伊始即具备 3D 感知能力——消融实验表明，仅此一项便带来 **+2.9 dB PSNR** 的提升（Table 2, row (a) vs (e)）。

**2. 高速公路编码器-解码器架构。** 论文明确区分了三类架构（Figure 4）：解码器唯一（decoder-only，如 LVSM 的部分变体）、瓶颈编码器-解码器（bottleneck，将多视图信息压缩为固定数量 token）和高速公路编码器-解码器（highway，每个源图像保留独立 token，无信息瓶颈）。LagerNVS 采用高速公路架构，最大化源图像到潜在表示的信息流，同时允许编码器独立缩放而不影响解码速度。消融实验证实，高速公路架构比解码器唯一高出 **+2.63 dB PSNR**（Table 2, row (a) vs (c)）。

**3. 双向交叉注意力解码。** 为在保持实时性的同时支持多视图输入，LagerNVS 采用双向交叉注意力替代完全自注意力（复杂度从 $O(V^2)$ 降至 $O(V)$）。该设计使模型在 1–9 个源视图下仍保持 56–30 FPS 的实时渲染速度，且 2 视图下仅比完全注意力低 0.28 dB PSNR（Table A3）。

### 与前馈 3DGS 的关系与边界

LagerNVS 与前馈 3DGS 方法的关系值得深入辨析。两者均追求前馈、可泛化的 NVS，但实现路径截然不同：

- **3DGS 方法**（AnySplat、DepthSplat、NoPoSplat 等）通过显式预测 3D 高斯参数，依赖光栅化渲染，在几何结构上具有强归纳偏置，但对薄结构、反射和遮挡敏感。
- **LagerNVS** 将 3D 信息隐式编码在潜在 token 中，直接由解码器渲染像素，避免了显式几何重建的脆弱性，在薄结构、反射区域和遮挡处理上表现更优（Figure 8, Figure A2）。

定量对比（Table 3）显示，LagerNVS 在所有基准上全面超越前馈 3DGS 方法：在 DL3DV 4-view 上比 **DepthSplat** 高出 **+5.26 dB PSNR**（27.56 vs 22.30），在 6-view 上高出 **+5.98 dB**（29.45 vs 23.47）；在无位姿的 RealEstate10k 2-view 设置下，比 **NoPoSplat** 高出 **+1.48 dB**（25.54 vs 24.06）。需要指出的是，NoPoSplat 仅训练于 RealEstate10k，与其他在更大数据混合上训练的模型可能存在不公对等，论文已明确标注此点。

### 适用边界与关键局限

LagerNVS 的能力边界由以下假设和约束划定：

**1. 相机内参一致性假设。** 模型假设所有源图像具有相同的相机内参，且与目标相机一致。当源图像来自不同焦距的相机时，性能会下降。这是当前架构的一个根本性限制，论文将其列为开放问题。

**2. 未观测区域的生成质量。** 在遮挡严重或视角外推较大的区域，模型渲染趋于模糊，并出现块状伪影（blocky artifacts）。当用于视频生成时，这些伪影表现为帧间 flicker。扩散解码器微调（Figure 9）可在一定程度上生成未观测区域的合理补全，但引入了随机性，牺牲了确定性渲染的一致性。

**3. 高频纹理重建不足。** 对于草地、树木等高频纹理，模型的重建质量较差，这是全神经渲染方法的共性挑战。

**4. 静态场景与数据分布限制。** 训练数据仅包含静态场景，未涉及动态物体、人类或鱼眼等畸变图像，模型在这些场景下的泛化能力未经验证。

### 未解决的开放问题

论文明确提出了若干值得后续探索的方向：

- **变焦距支持**：如何扩展模型以处理不同焦距的源图像，以及渲染任意目标焦距的视图？
- **生成质量提升**：如何减少未观测区域的块状伪影和视频 flicker？扩散解码器提供了生成能力的初步验证，但连续视频的 flicker-free 生成仍待解决。
- **高频纹理重建**：当前模型对高频细节的保真度不足，可能的改进方向包括引入更精细的解码器或混合渲染策略。
- **动态与复杂场景拓展**：模型目前仅限于静态场景，向动态场景、含人物或畸变图像的拓展是重要的应用方向。
- **VGGT 的 NVS 适配**：论文建议未来版本的 VGGT 等重建模型应在预训练阶段添加渲染头和渲染损失，以保留外观信息，从而更直接地服务于 NVS 任务。
- **确定性补全**：能否在保持确定性渲染的前提下改善复杂遮挡区域的均值回归问题？这需要在不引入随机性的情况下学习更丰富的多模态分布。

### 知识库定位总结

LagerNVS 的核心贡献在于证明了**显式 3D 监督预训练 + 无瓶颈高速公路架构**这一组合在重建-free NVS 中的决定性作用。它并非提出全新的网络模块，而是通过系统性的架构选择（编码器预训练策略、信息流设计、注意力机制）将现有组件组合为一种高效的全神经渲染方案。该方法在方法论上连接了 3D 重建预训练与 NVS 两个领域，为后续研究提供了明确的改进方向：更强的 3D 预训练信号、更灵活的内参处理、以及确定性渲染与生成能力的更好融合。

## 原文 PDF

![[paperPDFs/CVPR_2026/LagerNVS_Latent_Geometry_for_Fully_Neural_Real_time_Novel_View_Synthesis.pdf]]