---
title: "ArtiFixer: Enhancing and Extending 3D Reconstruction with Auto-Regressive Diffusion Models"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2026
pdf_ref: paperPDFs/SIGGRAPH_2026/ArtiFixer_Enhancing_and_Extending_3D_Reconstruction_with_Auto_Regressive_Diffusion_Models.pdf
project_link: https://research.nvidia.com/labs/sil/projects/artifixer/
aliases:
- AAAA
- ArtiFixer
tags:
- SIGGRAPH_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "核心因果旋钮在于不透明度感知噪声混合策略：根据初始渲染的不透明度图，在低不透明度区域注入高斯噪声，将去噪起始点从纯噪声或退化渲染替换为混合分布，从而在保留已有观测一致性的同时释放生成先验的创造能力；进一步通过双向到因果自回归蒸馏，实现高效的长序列一致生成。"
primary_logic: "即使用高度退化的3D重建提供粗粒度条件，当其渲染作为源分布的一部分并根据不透明度混合噪声时，足以同时约束生成过程并避免模式崩塌，使生成模型既能修复伪影又能合理生成缺失内容，且该条件信号能有效支持蒸馏训练，简化流水线。"
claims:
- "在 Nerfbusters 和 DL3DV 上，ArtiFixer 所有变体均以大幅度超越先前方法，PSNR 提升 2 dB。"
- "在 DL3DV 新内容生成协议下，ArtiFixer3D+ 比第二好的 GenFusion 高出近 3 dB PSNR。"
- "消融实验表明，从初始渲染出发（denoising）相比通道拼接是确保与源图像一致性的关键；不透明度混合防止了完全未观察区域的模式崩塌。"
- "因果蒸馏使推理速度比双向 Wan 2.1 骨干网络快 70 倍，同时保持高质量。"
---

# ArtiFixer: Enhancing and Extending 3D Reconstruction with Auto-Regressive Diffusion Models

> [!tip] 核心洞察
> 即使用高度退化的3D重建提供粗粒度条件，当其渲染作为源分布的一部分并根据不透明度混合噪声时，足以同时约束生成过程并避免模式崩塌，使生成模型既能修复伪影又能合理生成缺失内容，且该条件信号能有效支持蒸馏训练，简化流水线。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ArtiFixer：利用自回归扩散模型增强和扩展三维重建 |
| 英文题名 | ArtiFixer: Enhancing and Extending 3D Reconstruction with Auto-Regressive Diffusion Models |
| 会议/期刊 | SIGGRAPH 2026 |
| Links | [paper](https://arxiv.org/abs/2603.00492); [Project](https://research.nvidia.com/labs/sil/projects/artifixer); [Project](https://research.nvidia.com/labs/sil/projects/artifixer/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ArtiFixer（包含变体 ArtiFixer, ArtiFixer3D, ArtiFixer3D+） |
| Dataset | Nerfbusters, DL3DV, Mip-NeRF 360 (9 views), DL3DV (novel content generation) |

> [!tip] 效果简介
> - Nerfbusters 上，PSNR 为 20.24 (ArtiFixer3D)，对比 18.51 (DIFIX3D+ 3DGS)，变化 +1.73 dB。
> - DL3DV 上，PSNR 为 20.14 (ArtiFixer3D)，对比 17.99 (DIFIX3D+ 3DGS)，变化 +2.15 dB。
> - Mip-NeRF 360 (9 views) 上，PSNR 为 20.24 (ArtiFixer3D)，对比 16.79 (3DGS)，变化 +3.45 dB。

## 概述

### 背景与瓶颈

从稀疏或非结构化的图像集合重建三维场景是计算机视觉的核心挑战。尽管神经辐射场（NeRF）和三维高斯溅射（3DGS）等方法在密集观测条件下取得了显著进展，但在稀疏或缺失观测区域，这些方法普遍产生伪影、空洞或完全失败——它们缺乏对未观测区域的合理生成能力。另一方面，利用生成先验（如扩散模型）来增强重建的方法面临两个根本性困境：**可扩展性差**（帧数受限，需要昂贵的迭代蒸馏）和**生成不一致**（生成内容与已有观测不一致，在完全未观察区域出现模式崩塌）。

### 核心方法：ArtiFixer

ArtiFixer 提出了一套统一的框架，同时解决伪影修复和缺失内容生成问题。其核心创新包括：

1. **不透明度感知噪声混合**：根据初始重建的不透明度图，在低不透明度区域注入高斯噪声，将去噪起始点从纯噪声替换为退化渲染与噪声的混合分布。这一设计在保留已有观测一致性的同时，释放了生成先验在未观测区域的创造能力，防止模式崩塌。

2. **双向到因果自回归蒸馏**：先训练一个双向流匹配教师模型（基于 Wan 2.1 T2V-14B），再通过 Self Forcing 风格的 DMD 蒸馏将其转化为因果自回归学生模型，支持任意长度的视图序列生成，推理速度比双向骨干网络快 70 倍。

3. **显式相机控制与多条件注入**：通过 PixelUnshuffle 和线性层将 Plücker 射线图和不透明度图逐块注入 Transformer，同时利用 PRoPE 实现相对相机条件，确保即使输入完全为空区域仍能提供准确的相机控制。

方法包含三个递进变体：**ArtiFixer** 直接生成增强视图序列；**ArtiFixer3D** 将生成结果蒸馏回 3DGS 表示以获得显式三维一致性；**ArtiFixer3D+** 在此基础上重新应用生成器进一步提升细节。

### 主要结果

在多个基准数据集上，ArtiFixer 各变体均以大幅度超越先前方法：

- **伪影去除**（Nerfbusters 和 DL3DV）：PSNR 提升约 2 dB，全面领先 DIFIX3D+、GenFusion 等方法。
- **稀疏视图重建**（Mip-NeRF 360 9视图）：PSNR 达 20.24 dB，比 3DGS 基线高 3.45 dB。
- **新内容生成**（DL3DV 大未观测区域协议）：ArtiFixer3D+ 比第二好的 GenFusion 高出近 3 dB PSNR。

消融实验确证：从初始渲染出发的去噪（而非通道拼接）是确保与源图像一致性的关键；不透明度混合防止了完全未观测区域的模式崩塌。

### 局限与开放问题

ArtiFixer 虽达到交互式帧率，但仍慢于直接渲染神经场景表示；输出分辨率受骨干视频模型限制为 720p；在极长序列下的漂移和幻觉累积尚未量化评估。

## 背景与动机

三维场景重建旨在从一组稀疏的二维观测图像中恢复完整的几何与外观信息。以 3D Gaussian Splatting（3DGS）为代表的显式神经表示方法，通过将场景建模为一组可微的高斯原色，实现了高质量、实时的新视角渲染。其渲染过程可描述为沿视线方向的前向后投射合成：

$$C(\mathfrak{p}) = \sum_i c_i \prod_{k<i} (1 - \alpha_k)$$

然而，当输入视角稀疏或场景中存在大面积未观测区域时，重建结果往往出现严重伪影、几何塌缩和空洞。这一瓶颈的本质在于：神经表示本身缺乏对未见区域的合理推断能力，仅能忠实复现观测到的内容，对缺失区域则表现为噪声或退化渲染。

为填补这一能力缺口，研究者尝试将生成先验引入重建流水线。一类方法（如 **DiffusioNeRF**、**ZeroNVS**、**DIFIX3D+**）利用图像扩散模型对渲染结果进行增强或引导优化；另一类方法（如 **GenFusion**、**GS-Fixer**）则借助双向视频扩散模型，以通道拼接方式将退化渲染作为条件，生成修复后的视图序列。但这些方案面临两个根本性困境：

1. **可扩展性差**：双向视频扩散模型受限于固定帧数的生成窗口，无法直接处理任意长度的相机轨迹。为覆盖完整场景，通常需要迭代蒸馏或滑动窗口拼接，导致计算开销高昂且流程复杂。

2. **生成不一致**：在完全未观测区域，通道拼接的条件信号强度不足，生成模型容易偏离已有场景结构，产生与源图像不一致的内容；而在已有观测区域，生成过程又可能过度“创造”，破坏原有的保真度。这种“既要保持一致性，又要生成新内容”的矛盾，构成了现有方法的因果性瓶颈。

上述困境的核心在于**源分布初始化策略**：现有方法将退化渲染作为额外条件注入生成过程，但生成起点始终是纯高斯噪声。这一定义使得模型在未观测区域缺乏足够的结构约束，容易陷入模式崩塌；而在观测区域，噪声起点又过度依赖生成先验，难以精确保持与源图像的一致性。

ArtiFixer 的动机正是打破这一僵局。其核心洞察在于：**即使高度退化的初始重建，当其渲染作为源分布的一部分并根据不透明度混合噪声时，足以同时约束生成过程并避免模式崩塌**。这一设计将退化渲染从“条件”提升为“起点”，使生成模型既能修复伪影，又能合理推断缺失内容，且该条件信号能有效支持蒸馏训练，从而简化整个流水线。

## 核心创新

ArtiFixer 的核心创新在于重新定义了生成先验与三维重建的结合方式，通过三个关键设计突破现有方法的瓶颈：**不透明度感知的噪声混合策略**解决了生成一致性与创造力的根本矛盾；**因果自回归蒸馏**实现了长序列的高效一致生成；**精细的相机与不透明度条件注入**确保了即使输入完全退化时空洞区域仍能获得有效的几何引导。

### 不透明度感知的噪声混合：生成一致性与创造力的统一

现有利用生成先验增强三维重建的方法面临一个根本困境：若将退化渲染通过通道拼接作为额外条件注入生成过程，模型倾向于忽略该条件，导致生成结果与已有观测不一致（如桌子的语义漂移）；若直接以退化渲染作为去噪起点，虽能保持一致性，但在完全未观测区域会出现严重的模式崩塌，无法生成合理内容。

ArtiFixer 的解决方案是将退化渲染与高斯噪声在潜在空间中进行不透明度加权混合，直接作为流匹配的源分布：

$$ \mathbf{z}_0 := \mathbf{O}_z \mathbf{z}_{deg} + (1 - \mathbf{O}_z) \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I}) $$

其中 $\mathbf{z}_{deg}$ 是退化渲染经过冻结 VAE 编码后的潜在表示，$\mathbf{O}_z$ 是下采样后的不透明度图。这一设计的因果机制在于：

- **高不透明度区域**（已有观测区域）：$\mathbf{O}_z \to 1$，源分布趋近于退化渲染，模型仅需微调即可恢复干净内容，天然保持与源图像的一致性。
- **低不透明度区域**（未观测或稀疏区域）：$\mathbf{O}_z \to 0$，源分布趋近于高斯噪声，释放预训练视频扩散模型的生成能力，允许模型创造合理的新内容。

这种混合策略的本质是将“一致性约束”和“生成自由度”编码在同一个源分布中，而非将其作为分离的条件信号。消融实验（Table 4）证实了这一设计的决定性作用：将不透明度混合替换为通道拼接后，Mip-NeRF 360 上的 PSNR 从 17.99 dB 骤降至 15.43 dB；完全移除不透明度混合则导致未观测区域的模式崩塌（Figure 4）。

### 因果自回归蒸馏：从双向生成到高效长序列推理

现有基于视频扩散模型的方法（如 GenFusion）依赖双向注意力机制，一次只能生成固定帧数（如 16 帧），需要迭代蒸馏才能覆盖长序列，导致推理效率低下且累积误差。ArtiFixer 提出将双向流匹配教师模型蒸馏为因果自回归学生模型，核心改动包括：

- **块因果注意力掩码**：将双向注意力替换为块因果注意力，使每一帧仅依赖当前帧及历史帧，支持自回归生成任意长度的视图序列。
- **Diffusion Forcing 风格的噪声扰动**：对每一帧施加不同噪声水平，使模型学会在不同去噪阶段进行条件生成。
- **DMD 蒸馏**：通过分布匹配蒸馏将多步去噪压缩为 4 步，大幅提升推理速度。

蒸馏后的因果模型在保持生成质量的同时，推理速度达到 8.36 FPS（14B 参数），相比双向 Wan 2.1 骨干网络（0.12 FPS）实现了约 70 倍加速（Table 5）。这一效率提升使得 ArtiFixer 能够单次推理生成数百帧视图，为后续的 3D 蒸馏提供高质量的伪监督信号。

### 精细的相机与不透明度条件注入

为充分利用退化重建提供的几何线索，ArtiFixer 设计了专门的条件注入模块，将 Plücker 射线图 $\mathbf{R}$ 和不透明度图 $\mathbf{O}$ 逐块注入 Transformer 的视觉 token 中：

$$ T_{r} := T_{s} + f_{r}(\mathrm{PixelUnshuffle}(\mathbf{R})) $$
$$ T_{o} := T_{r} + f_{o}(\mathrm{PixelUnshuffle}(\mathbf{O})) $$

其中 $\mathrm{PixelUnshuffle}$ 将射线图和不透明度图的空间分辨率下采样至与 VAE 潜在空间匹配，$f_r$ 和 $f_o$ 是每个 Transformer 块独立的线性层。这些条件信号绕过了 VAE，直接作用于潜在空间，确保了即使在输入渲染完全退化的空区域，相机位姿信息仍能有效引导生成过程。

此外，ArtiFixer 支持将 0 到 12 张干净参考视图编码为视觉 token，在每一层交叉注意力中与目标 token 交互，并通过 PRoPE 施加相对位姿条件。所有新增参数（$f_r$、$f_o$ 和交叉注意力的 $V_n$ 投影）均采用零初始化，确保与预训练权重的兼容性。

### 方法变体与流水线设计

ArtiFixer 提供三个递进式变体，形成完整的三维重建增强流水线：

1. **ArtiFixer**：因果自回归模型直接生成增强后的视图序列，无需显式三维表示。
2. **ArtiFixer3D**：将 ArtiFixer 生成的干净视图蒸馏回 3DGS 表示，获得显式的多视角一致性三维重建，代价是轻微模糊。
3. **ArtiFixer3D+**：在 ArtiFixer3D 的基础上重新应用生成器，恢复锐度的同时保持三维一致性，在 PSNR 和视觉质量之间取得最佳平衡。

这一流水线设计的关键洞察在于：高度退化的三维重建虽然自身质量不佳，但其渲染结果作为不透明度混合的源分布时，足以同时约束生成过程并避免模式崩塌；而生成器产生的干净视图又可反哺三维表示，形成“重建→生成→重建”的闭环增强。

## 整体框架

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2603_00492/figures/002_Figure_2.jpg]]
*Figure 2: Method overview. We first train a bidirectional flow matching model that transports degraded RGB renderings into clean outputs. We encode the input RGB into latent space and mix with Gaussian noise using the rendered opacity maps to avoid mode collapse in unseen regions. We inject fine-grained opacity information and camera control along with optional clean reference views and a text prompt. In the second phase of our pipeline, we distill the teacher into an auto-regressive causal model via Self Forcing-style DMD distillation [Huang et al. 2025], which can be directly used to render novel views or used as pseudo-supervision to distill back into the underlying 3D representation*

ArtiFixer 的整体流水线围绕一个核心矛盾展开：如何让生成模型在修复三维重建伪影的同时，在完全未观察区域产生合理的新内容，而不破坏与已有观测的一致性。为此，流水线被设计为两阶段：**双向流匹配教师训练**与**因果自回归蒸馏**，并在两个阶段之间通过**不透明度感知噪声混合**这一关键机制桥接一致性与生成能力。

### 流水线总览

第一阶段训练一个双向流匹配模型作为“教师”。该模型接收来自初始三维重建的退化渲染（degraded rendering）及其对应的不透明度图，在潜在空间中将退化渲染与高斯噪声按不透明度混合后作为源分布，通过流匹配预测干净的目标渲染。这一过程同时注入 Plücker 射线图提供的相机控制、可选的干净参考视图以及文本提示，使模型学会在保留已有结构的同时填充缺失区域。

第二阶段将双向教师蒸馏为因果自回归“学生”模型。学生模型通过块因果注意力掩码和 Diffusion Forcing 风格的噪声扰动进行训练，无需生成完整的 ODE 轨迹。蒸馏后的模型支持 4 步去噪，可自回归地生成任意长度的视图序列，推理速度比双向骨干提升约 70 倍。

可选地，生成的多视图序列可作为伪监督信号蒸馏回显式的三维高斯溅射（3DGS）表示，得到 ArtiFixer3D；再次应用生成器则得到 ArtiFixer3D+，在显式三维一致性与渲染锐度之间取得平衡。

### 模块关系与数据流

流水线由以下核心模块串联构成：

1. **初始三维重建模块**：利用 3DGUT + MCMC 从稀疏输入构建初始 3DGS 重建，输出退化渲染及其不透明度图。该重建质量可能很差，但提供了粗粒度的场景几何与外观先验。

2. **不透明度感知噪声混合**：将退化渲染经冻结 VAE 编码后的潜在表示 $\mathbf{z}_{deg}$ 与高斯噪声 $\boldsymbol{\epsilon}$ 按不透明度图 $\mathbf{O}_z$ 混合：
   $$\mathbf{z}_0 := \mathbf{O}_z \mathbf{z}_{deg} + (1 - \mathbf{O}_z) \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$
   在高不透明度区域（已有观测），源样本接近退化渲染，从而约束生成结果与源图像一致；在低不透明度区域（未观测），源样本接近纯噪声，释放生成先验的创造能力。这一混合策略是防止模式崩塌的关键因果旋钮。

3. **双向流匹配教师模型**：基于 Wan 2.1 T2V-14B 构建。退化渲染经 VAE 编码和 3D 块化（patch size $(1, 2, 2)$）后与混合噪声结合作为源样本。相机控制通过 PixelUnshuffle 下采样 Plücker 射线图和不透明度图，经逐块线性层 $f_r$、$f_o$ 注入 Transformer 的视觉 token：
   $$T_{r} := T_{s} + f_{r}(\mathrm{PixelUnshuffle}(\mathbf{R}))$$
   $$T_{o} := T_{r} + f_{o}(\mathrm{PixelUnshuffle}(\mathbf{O}))$$
   参考视图经冻结 VAE 编码为视觉 token，在交叉注意力中通过 PRoPE 施加相对位姿条件。文本提示经冻结文本编码器注入。所有新增参数（$f_r$、$f_o$、交叉注意力的 $K_n$、$V_n$ 投影）均零初始化以保证与预训练权重的兼容性。

4. **因果自回归学生模型**：从双向教师权重初始化，施加块因果注意力掩码，通过 DMD（Distribution Matching Distillation）实现 4 步快速去噪。学生模型可自回归生成任意长度的视图序列，避免了双向模型固定帧数生成和迭代蒸馏的瓶颈。

5. **三维蒸馏模块（可选）**：将自回归模型生成的干净视图作为伪真值，蒸馏回 3DGS 表示，得到显式三维一致的 ArtiFixer3D。进一步重新应用生成器得到 ArtiFixer3D+，恢复因三维蒸馏而损失的部分锐度。

### 输入输出规范

- **输入**：初始退化渲染序列（含对应相机位姿）、不透明度图、Plücker 射线图、0~12 张干净参考视图、可选文本提示。
- **输出**：干净渲染序列（ArtiFixer）或增强后的 3DGS 重建（ArtiFixer3D/3D+）。
- **关键约束**：退化渲染和干净渲染共享相同的相机轨迹；参考视图与目标视图的相机位姿通过 PRoPE 关联；文本提示在训练时以 10% 概率丢弃以支持无文本推理。

## 核心模块与公式推导

### 3DGS 渲染与退化渲染生成

ArtiFixer 的输入来源于一个初始的 3D 重建。论文采用 3DGUT 结合 MCMC 策略从稀疏视图构建初始 3DGS 表示。3DGS 的渲染过程可表述为沿光线从前向后合成高斯原色：

$$C(\mathfrak{p}) = \sum_i c_i \prod_{k<i} (1 - \alpha_k)$$

其中 $c_i$ 为高斯原色的颜色，$\alpha_k$ 为前序高斯的不透明度。该渲染同时产生 RGB 图像和对应的不透明度图 $O$，二者共同构成后续生成模型的“退化渲染”输入。不透明度图在此承担关键角色：它标识了初始重建中哪些区域已被充分观测（高不透明度），哪些区域是空洞或伪影（低不透明度），为后续的不透明度混合策略提供了像素级的置信度信号。

### 流匹配基础

ArtiFixer 的生成模型基于条件流匹配框架。给定源分布样本 $\mathbf{z}_0$ 和目标分布样本 $\mathbf{z}_1$，流匹配通过线性插值定义中间状态：

$$\mathbf{z}_t = (1-t)\mathbf{z}_0 + t\mathbf{z}_1$$

对应的目标速度场为常向量：

$$\mathbf{v}_t = \mathbf{z}_1 - \mathbf{z}_0$$

训练目标是最小化神经网络预测的速度场与目标速度场之间的 $L_2$ 误差：

$$\min_\theta \mathbb{E}_{t,\mathbf{z}_0,\mathbf{z}_1} \left\| \mathbf{v}_\theta(\mathbf{z}_t, t) - \mathbf{v}_t \right\|_2^2$$

在 ArtiFixer 的语境中，$\mathbf{z}_0$ 并非传统的高斯噪声，而是经过不透明度混合后的退化渲染潜在编码，$\mathbf{z}_1$ 为对应的干净渲染潜在编码。这一源分布的重定义是整个方法的核心因果旋钮。

### 不透明度感知噪声混合

不透明度混合策略是 ArtiFixer 区别于以往方法的最关键模块。其公式为：

$$\mathbf{z}_0 := \mathbf{O}_z \mathbf{z}_{deg} + (1 - \mathbf{O}_z) \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$

其中 $\mathbf{z}_{deg}$ 是退化渲染经冻结 VAE 编码后的潜在表示，$\mathbf{O}_z$ 是经过相应下采样的不透明度图，$\boldsymbol{\epsilon}$ 为标准高斯噪声。该操作的因果逻辑是：

- **高不透明度区域**（$\mathbf{O}_z \to 1$）：$\mathbf{z}_0 \approx \mathbf{z}_{deg}$，源分布几乎完全保留退化渲染的信息，去噪过程仅需微调即可恢复与已有观测一致的细节，从而确保一致性。
- **低不透明度区域**（$\mathbf{O}_z \to 0$）：$\mathbf{z}_0 \approx \boldsymbol{\epsilon}$，源分布退化为纯噪声，释放生成先验的全部创造能力，使模型能够在完全未观察区域生成合理的新内容。
- **中间区域**：混合分布提供了平滑过渡，避免了硬边界带来的伪影。

消融实验（Table 4）证实：若改用通道拼接（将退化渲染作为额外条件通道，而非混合到源分布中），Mip-NeRF 360 上的 PSNR 从 17.99 骤降至 15.43，表明从初始渲染出发的去噪范式是确保与源图像一致性的关键；若完全移除不透明度混合（即始终从退化渲染出发），则会在完全未观察区域出现模式崩塌（Figure 4）。

### 相机控制与条件注入

ArtiFixer 基于预训练的文本到视频模型 Wan 2.1 T2V-14B 构建，冻结其 VAE 和文本编码器，在每层 Transformer 块中注入相机和不透明度信息。具体地，Plücker 射线图 $\mathbf{R}$ 和不透明度图 $\mathbf{O}$ 通过 PixelUnshuffle 操作下采样至与 VAE 空间压缩因子匹配的尺寸，再经每块独立的线性层编码后添加到自注意力 token 中：

$$T_{r} := T_{s} + f_{r}(\mathrm{PixelUnshuffle}(\mathbf{R}))$$

$$T_{o} := T_{r} + f_{o}(\mathrm{PixelUnshuffle}(\mathbf{O}))$$

其中 $T_s$ 为自注意力输出的 token，$f_r$ 和 $f_o$ 为零初始化的线性层，确保与预训练权重的兼容性。这种设计使相机控制信号直接参与 token 空间的构建，即使输入渲染完全为空区域，模型仍能获得精确的相机位姿信息。

对于参考视图，ArtiFixer 将其经冻结 VAE 编码为视觉 token，在交叉注意力层中与目标 token 交互，并利用 PRoPE 施加相对位姿条件。$K_n$ 和 $V_n$ 投影同样采用零初始化。

### 因果自回归蒸馏

第二阶段，ArtiFixer 将双向流匹配教师模型蒸馏为因果自回归学生模型。蒸馏过程采用 Self Forcing 风格的 DMD 方法：直接对教师权重施加块因果注意力掩码，对每帧输入扰动不同程度的噪声（类似 Diffusion Forcing），其余训练协议与教师模型保持一致。因果模型支持 4 步去噪，可自回归地生成任意长度的视图序列，推理速度较双向教师提升约 70 倍（Table 5：8.36 FPS vs 0.12 FPS）。

### 3D 蒸馏（可选）

ArtiFixer3D 将自回归模型生成的干净视图一次性蒸馏回 3DGS 表示，获得显式的多视角一致 3D 重建。ArtiFixer3D+ 在此基础上重新应用生成器，以恢复 3D 蒸馏过程中损失的锐度。

## 实验与分析

### 核心瓶颈与因果机制

现有3D场景重建方法在稀疏或缺失观测区域面临根本性困境：传统重建方法（如3DGS、Zip-NeRF）产生伪影或空洞，而利用生成先验的方法则陷入“一致性-生成能力”的权衡——要么与已有观测不一致，要么在完全未观察区域完全失败。ArtiFixer通过两个关键因果旋钮打破这一僵局：

1. **不透明度感知噪声混合**：根据初始渲染的不透明度图，在低不透明度区域注入高斯噪声，将去噪起始点从纯噪声替换为混合分布 $\mathbf{z}_0 := \mathbf{O}_z \mathbf{z}_{deg} + (1 - \mathbf{O}_z) \boldsymbol{\epsilon}$。这在高不透明度区域保留已有观测的一致性，同时在未观察区域释放生成先验的创造能力，防止模式崩塌（Fig. 4）。
2. **因果自回归蒸馏**：将双向流匹配教师模型蒸馏为因果学生模型，通过自回归生成支持任意长度视图序列，推理速度提升70倍（Table 5）。


![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2603_00492/figures/012_Table_5.jpg]]
*Table 5: Inference speed. Causal distillation yields a 70× speedup over the bidirectional Wan 2.1 backbones. ArtiFixer3D renders directly from 3DGUT. Additional configurations are reported in Table 7*

### 主实验结果

**伪影去除**（Table 1）：在Nerfbusters和DL3DV基准上，ArtiFixer所有变体均以大幅度超越先前方法。ArtiFixer3D在Nerfbusters上达到PSNR 20.24，相比DIFIX3D+ 3DGS（18.51）提升1.73 dB；在DL3DV上达到20.14，相比DIFIX3D+ 3DGS（17.99）提升2.15 dB。ArtiFixer直接生成更锐利的渲染，ArtiFixer3D通过显式3D表示获得更好的源图像一致性但略模糊，ArtiFixer3D+重新应用生成器恢复锐度（Fig. 5）。


![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2603_00492/figures/005_Table_1.jpg]]
*Table 1: Artifact removal on Nerfbusters and DL3DV. All ArtiFixer variants outperform prior methods by a considerable margin, improving PSNR by 2 dB*

**稀疏视图重建**（Table 2）：在Mip-NeRF 360的9视图设置下，ArtiFixer3D达到PSNR 20.24，相比3DGS（16.79）提升3.45 dB，在所有指标上全面超越现有稀疏视图方法。在极端的3视图场景中，ArtiFixer能从参考视图恢复正确几何，即使输入渲染完全不准确（Fig. 9）。


![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2603_00492/figures/006_Table_2.jpg]]
*Table 2: Sparse view reconstruction methods on the Mip-NeRF 360 dataset. We exceed existing work by a wide margin across every metric*

**新内容生成**（Table 3）：在DL3DV的大面积未观察区域协议下，ArtiFixer3D+达到PSNR 20.15，比第二好的GenFusion（17.03）高出近3 dB。GenFusion的双向视频模型每次仅生成16帧，需要迭代蒸馏导致模糊结果；Gen3C的渲染虽锐利但常不尊重源内容且存在几何错误。ArtiFixer在高度退化区域仍能生成合理且一致的几何（Fig. 8）。


![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2603_00492/figures/008_Table_3.jpg]]
*Table 3: Novel content generation. We reconstruct DL3DV scenes following a protocol that creates large areas unobserved by training views. We outperform the next-best method (GenFusion) by almost 3 dB in PSNR*

**多视角一致性**（Table 11）：通过MEt3R评估，所有ArtiFixer变种均超越基线，ArtiFixer3D因显式3D表示获得最佳一致性。

### 消融分析

Table 4在Mip-NeRF 360上系统验证了关键设计选择：


![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2603_00492/figures/010_Table_4.jpg]]
*Table 4: Diagnostics. We evaluate reconstruction quality on Mip-NeRF 360. Denoising input renderings instead of conditioning via channel concatenation is crucial to producing outputs consistent with source images*

- **从初始渲染出发 vs 通道拼接**：使用通道拼接代替从初始渲染出发的去噪，导致PSNR从17.99骤降至15.43，证实了从初始渲染出发是确保与源图像一致性的关键。
- **不透明度混合的作用**：移除不透明度混合导致完全未观察区域的模式崩塌和生成质量下降（Fig. 4定性展示）。
- **因果初始化**：因果模型权重初始化提供了小幅性能提升，非必需但有益。

文本提示的影响（Table 6）：在稀疏设置（Mip-NeRF 360 3-view）下，VLM生成的提示带来微小增益（+0.14 dB）；在密集设置下影响可忽略。这表明ArtiFixer主要依赖视觉条件信号，文本起辅助作用。


![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2603_00492/figures/016_Table_6.jpg]]
*Table 6: Text conditioning. We measure the impact of VLM-generated prompts vs. no prompt for ArtiFixer3D+. Text prompts provide a small benefit in sparse settings that diminishes with denser captures*

模型规模影响（Table 8, Table 9）：1.3B变体在Mip-NeRF 360 3-view上与CAT3D仅差0.02 dB，在DL3DV新内容生成上远超其他视频模型基线，展示了方法的参数效率。


![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2603_00492/figures/021_Table_9.jpg]]
*Table 9: Impact of model scale on novel content generation (DL3DV). Even with a 1.3B backbone, ArtiFixer3D+ outperforms the other video model baselines by a wide margin*

### 推理效率

因果蒸馏实现了显著的推理加速（Table 5）：14B模型达到8.36 FPS，相比双向Wan 2.1骨干（0.12 FPS）提升约70倍。通过减少去噪步数和跨GPU上下文并行，1.3B变体可达101.77 FPS（Table 7）。ArtiFixer在仅1步去噪时即可生成合理内容，但在空白区域的锐度和时序一致性有所下降（Fig. 11）。


![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2603_00492/figures/017_Table_7.jpg]]
*Table 7: Inference configurations. Fewer denoising steps and context parallelism across multiple GPUs further improve throughput, with the 1.3B variant reaching up to 101.77 FPS*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2603_00492/figures/020_Figure_11.jpg]]
*Figure 11: Denoising steps. We vary the number of denoising steps when beginning from the initial degraded rendering. ArtiFixer can render plausible content in as few as 1 step, although sharpness and temporal consistency suffer somewhat in empty areas. Table 8. Impact of model scale on Mip-NeRF 360. Our 1.3B variant matches CAT3D within 0.02 dB on the 3-view split and exceeds other video model baselines despite using fewer parameters*

### 失败模式与局限

1. **分辨率限制**：ArtiFixer和ArtiFixer3D+受骨干视频模型限制，输出分辨率上限为720p；ArtiFixer3D可渲染原生分辨率。
2. **推理延迟**：以时间块解码引入延迟，不适合某些实时应用（如具身AI）；虽达交互帧率，仍显著慢于直接渲染3DGS。
3. **细节保真度**：与其他视频扩散模型类似，可能模糊精细细节和文字，在渲染条件缺失或高度退化时引入微妙颜色偏移。
4. **极长序列漂移**：论文声称条件信号足够防止自回归漂移，但未提供极长序列的量化评估，此点需进一步验证。

### 开放问题

- 能否进一步减少去噪步数并保持时间一致性？
- 能否实现单帧解码同时维持时间连贯性？
- 视频超分辨率技术能否弥补720p分辨率限制？
- 不透明度混合策略在完全未观察区域中的生成质量和多视角一致性如何进一步量化？

### 补充图表

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2603_00492/figures/001_Figure.jpg]]
*Figure: Rendered Trajectory*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2603_00492/figures/019_Figure.jpg]]
*Figure: 1 Step 3 Steps 4 Steps*

## 方法谱系与知识库定位

### 1. 方法谱系与核心差异

ArtiFixer 位于**生成先验增强的3D重建**这一交叉领域，其技术路线同时触及显式神经重建、扩散先验增强和多视图生成三条谱系。

**与显式神经重建基线的差异。** 传统方法如 **3DGS**、**Nerfacto**、**Zip-NeRF**、**2DGS** 在稀疏或缺失观测区域直接产生伪影或空洞，缺乏内容生成能力。稀疏视图重建方法（**FSGS**、**FreeNeRF**、**SimpleNeRF**）通过前馈网络或几何正则化缓解该问题，但本质上仍是对现有观测的插值，无法在完全未观察区域生成合理内容。ArtiFixer 的出发点正是将这些方法的退化渲染作为生成模型的源分布，而非最终输出。

**与扩散先验增强方法的差异。** 以 **DiffusioNeRF**、**ZeroNVS**、**NeRFLiX**、**GANeRF**、**DIFIX3D+** 为代表的方法利用图像扩散模型增强重建质量，但面临两个核心瓶颈：（1）帧数受限，难以扩展到长序列；（2）生成内容与已有观测不一致。这些方法通常将退化渲染通过**通道拼接**作为额外条件注入扩散模型，从纯高斯噪声开始去噪。ArtiFixer 的关键设计变更在于**不透明度感知噪声混合策略**——根据初始渲染的不透明度图，在低不透明度区域注入高斯噪声，将流匹配的源分布从纯噪声替换为混合分布 $\mathbf{z}_0 := \mathbf{O}_z \mathbf{z}_{deg} + (1 - \mathbf{O}_z) \boldsymbol{\epsilon}$。这一设计同时实现了两个目标：高不透明度区域保留与源图像的一致性，低不透明度区域释放生成先验的创造能力。消融实验证实，使用通道拼接代替该策略会导致 Mip-NeRF 360 上 PSNR 从 17.99 降至 15.43（Table 4），而移除不透明度混合则会在完全未观察区域引发模式崩塌（Figure 4）。

**与基于视频扩散的方法的差异。** **GenFusion** 和 **GS-Fixer** 采用双向视频扩散模型进行生成增强，但受限于固定帧数的双向生成，需要迭代蒸馏过程，导致结果模糊且效率低下。ArtiFixer 通过**双向到因果自回归蒸馏**解决该问题：先训练双向流匹配教师模型（基于 Wan 2.1 T2V-14B），再通过 Self Forcing 风格的 DMD 蒸馏训练因果自回归学生模型，支持任意长度的自回归生成，推理速度提升 70 倍（Table 5：8.36 FPS vs 0.12 FPS）。

**与多视图生成方法的差异。** **CAT3D**、**Gen3C**、**ReconX** 等方法利用扩散生成先验进行多视图生成，但 Gen3C 的渲染虽然清晰，却常常不尊重源内容、几何错误且存在颜色偏移（Figure 8）。ArtiFixer 通过将退化渲染作为源分布的一部分（而非额外条件），从根本上约束了生成过程，确保即使输入渲染完全退化时，仍能恢复正确的几何结构（Figure 9）。

**关键技术槽位变更总结。** 相较于先前工作，ArtiFixer 在五个关键槽位进行了系统性变更：（1）源分布初始化从通道拼接改为不透明度混合；（2）生成模型架构从双向视频扩散改为蒸馏后的因果自回归模型；（3）相机控制通过 PixelUnshuffle 和线性层将 Plücker 射线图与不透明度图逐块注入 Transformer；（4）参考视图整合支持可变数量（0~12）的干净视图，通过交叉注意力和 PRoPE 相对位姿条件交互；（5）学习策略从标准扩散训练改为双向教师训练加因果蒸馏。

### 2. 适用边界与局限

**分辨率限制。** ArtiFixer 和 ArtiFixer3D+ 受骨干视频模型限制，输出分辨率上限为 720p。ArtiFixer3D 通过直接渲染 3DGS 表示可输出原生分辨率，但生成质量略有下降（Figure 5）。应用视频超分辨率技术是潜在的弥补方向。

**推理速度与实时性。** 虽然因果蒸馏实现了 70 倍加速，达到 8.36 FPS（14B 模型），但仍显著慢于直接渲染神经场景表示（如 3DGS）。以时间块解码的方式会引入额外延迟，可能不适合对延迟敏感的实时应用（如具身 AI）。1.3B 变体在上下文并行加速下可达 101.77 FPS（Table 7），但性能有所下降（Table 8）。

**精细细节与颜色保真度。** 与其他视频扩散模型类似，ArtiFixer 可能模糊精细细节和文字，并在渲染条件缺失或高度退化时引入微妙的颜色偏移。这是扩散模型固有的平滑倾向，也是未来改进方向。

**极长序列下的漂移。** 论文声称条件信号（退化渲染和不透明度图）足以防止自回归生成中的漂移和幻觉累积，但未提供极长序列（如数百帧以上）的量化评估，该声明需要进一步验证。

### 3. 开放问题与未来方向

**去噪步数与时间一致性。** 能否进一步减少去噪步数（目前为 4 步）并保持时间一致性？Figure 11 显示 ArtiFixer 在仅 1 步去噪时仍能生成合理内容，但清晰度和时间一致性在空白区域有所下降。探索更高效的采样策略或一致性模型蒸馏是可行方向。

**单帧解码与实时应用。** 当前自回归模型以时间块解码，能否实现单帧解码同时维持时间连贯性？这将直接影响实时应用（如 VR/AR）的可行性。

**分辨率扩展。** 能否应用视频超分辨率技术弥补 720p 限制？考虑到骨干模型已冻结 VAE，在潜在空间进行超分辨率或在像素空间进行后处理是两种可能的路径。

**不透明度混合的量化分析。** 不透明度混合策略在完全未观察区域中的生成质量和多视角一致性如何进一步量化？当前消融主要依赖定性展示（Figure 4）和整体 PSNR 指标，缺乏针对不同不透明度区间的细粒度分析。

**自回归漂移的量化评估。** 自回归模型在极长序列下的漂移和幻觉累积需要系统性的量化研究，包括长序列下的多视角一致性退化曲线和内容漂移度量。

**文本提示的利用效率。** 文本提示在稀疏设置下仅带来微小增益（+0.14 dB，Table 6），密集设置下影响可忽略。如何更有效地利用文本条件来指导未观察区域的内容生成，是提升生成合理性的潜在方向。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2026/ArtiFixer_Enhancing_and_Extending_3D_Reconstruction_with_Auto_Regressive_Diffusion_Models.pdf]]
