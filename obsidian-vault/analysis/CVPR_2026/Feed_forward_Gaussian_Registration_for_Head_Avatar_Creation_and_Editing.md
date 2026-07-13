---
title: Feed-forward Gaussian Registration for Head Avatar Creation and Editing
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Feed_forward_Gaussian_Registration_for_Head_Avatar_Creation_and_Editing.pdf
project_link: null
code_link: null
aliases:
- MMVAFTCH
- FFGRHACE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 设计了一种注册引导的注意力机制（registration-guided attention），限制每个UV令牌仅关注其对应头部区域的图像令牌，从而降低计算复杂度并大幅提升合成质量与跨身份泛化能力。
primary_logic: 通过前馈Transformer直接预测具有稠密语义对应关系的3D高斯splat纹理，彻底绕过逐帧跟踪和优化，在0.5秒内实现高质量重建，并可自然支持快速化身构建、语义编辑和表情迁移。
claims:
- MATCH直接预测具有稠密语义对应关系的高斯splats，将总化身创建时间缩短10倍（从45小时降至4.6小时）。
- 注册引导注意力模块带来了最大的性能提升，密集注意力（Dense Attention）导致最差的LPIPS（0.221）。
- MATCH在新视角合成、几何重建和化身质量上全面超越现行方法，同时在NeRSemble上仅用Ava-256训练即可泛化。
- Ava-256 上 LPIPS↓ = 0.163
---

# Feed-forward Gaussian Registration for Head Avatar Creation and Editing

> [!tip] 核心洞察
> 通过前馈Transformer直接预测具有稠密语义对应关系的3D高斯splat纹理，彻底绕过逐帧跟踪和优化，在0.5秒内实现高质量重建，并可自然支持快速化身构建、语义编辑和表情迁移。

| 字段 | 内容 |
|------|------|
| 中文题名 | 前馈高斯配准用于头部虚拟化身创建与编辑 |
| 英文题名 | Feed-forward Gaussian Registration for Head Avatar Creation and Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.15811) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MATCH (Multi-view Avatars from Topologically Corresponding Heads) |
| Dataset | Ava-256, NeRSemble |

> [!tip] 效果简介
> - Ava-256 上，LPIPS↓ 0.163 vs 0.208 (FaceLift) (-0.045)。
> - NeRSemble 上，LPIPS↓ 0.152 vs 0.200 (FaceLift) (-0.048)。
> - Ava-256 (Geometry) 上，P2P Full Head (mm)↓ 6.69 vs 7.34 (TEMPEH Glob.*) (-0.65)。

## 概要

**问题瓶颈**：传统头部化身创建流程依赖两阶段耗时优化——先以逐帧网格跟踪（如VHAP）建立跨帧对应，再优化可动画高斯化身（如GEM）。该流程单帧跟踪需12秒，完整化身重建耗时长达45小时，严重制约规模化应用。

**核心方法**：MATCH（Multi-view Avatars from Topologically Corresponding Heads）提出一种前馈Transformer架构，直接从标定多视图图像预测具有稠密语义对应关系的3D高斯splat纹理，单帧推理仅需0.5秒，彻底绕过逐帧跟踪与优化。其关键创新在于**注册引导注意力机制**（registration-guided attention），通过计算UV令牌与图像令牌之间的空间对应得分（公式见Equation 1），约束每个UV令牌仅关注其对应头部区域的图像令牌，在降低计算复杂度的同时显著提升合成质量与跨身份泛化能力。

**主要结果**：
- **新视角合成**：在Ava-256和NeRSemble数据集上，LPIPS分别达到0.163和0.152，全面超越FaceLift等现行方法（Table 1）。
- **化身构建效率**：将GEM化身创建总时间从45.3小时压缩至4.6小时，加速约10倍（Table 4）。
- **几何重建**：全头点对点距离（P2P）降至6.69mm，优于TEMPEH全局阶段（Table 3）。
- **消融验证**：注册引导注意力是最大性能增益来源——替换为密集注意力后LPIPS从0.187恶化至0.221（Table 2）。

**方法定位**：MATCH属于**前馈高斯配准**范式，区别于优化式化身（GEM、GaussianAvatars）和单视图/多视图预测方法（LAM、FaceLift、Avat3r）。其建立的跨身份、跨表情稠密对应关系，天然支持快速化身构建、语义编辑与表情迁移等下游应用（Figure 1）。



### 问题背景

创建逼真、可动画的头部虚拟化身是计算机视觉与图形学领域的核心挑战，在远程通信、虚拟现实和影视制作中具有广泛需求。传统头部化身构建流程通常包含三个关键步骤：首先对多视图视频序列进行逐帧网格跟踪以建立跨帧对应关系，随后基于跟踪结果训练可动画的神经化身模型，最后通过主成分分析（PCA）蒸馏为可实时驱动的参数化模型。然而，这一流程存在严重的效率瓶颈——以当前最优方法 **GEM**（Giebenhain et al., CVPR 2024）为例，仅网格跟踪就需约10.7小时，后续高斯优化又需27.7小时，总计约45小时才能完成一个特定主体的化身创建。如此高昂的时间成本使得大规模扩展极其昂贵，严重制约了头部化身技术的实际应用。

### 现有方法缺口

近年来，研究者尝试通过前馈方法绕过部分优化步骤来加速这一流程。**FastAvatar**（Xu et al., CVPR 2024）和 **LAM**（Li et al., ECCV 2024）从单张图像直接预测附着于3D形变模型（3DMM）的高斯splat，但依赖隐式对应关系，合成质量有限。**Avat3r**（Giebenhain et al., ArXiv 2024）和 **FaceLift**（Ma et al., CVPR 2024）通过像素对齐方式从多视图预测高斯，但仍未建立显式的稠密语义对应，导致跨身份泛化和编辑能力受限。**TEMPEH**（Bolkart et al., 2024）虽能一步式完成网格注册，但其全局阶段仅输出粗配准，精细几何仍需后续优化。总体而言，现有前馈方法在效率、合成质量与语义对应之间难以兼顾：要么继承缓慢的逐帧跟踪，要么牺牲稠密对应带来的编辑灵活性和跨身份泛化能力。

### 核心动机

本文的核心动机在于：**能否彻底绕过逐帧跟踪和优化，通过一次前馈推理直接预测具有稠密语义对应关系的3D高斯splat纹理？** 若能实现，不仅可将单帧重建时间从数小时压缩至亚秒级，还能天然支持快速化身构建、语义编辑和表情迁移等下游应用。这一思路的关键挑战在于如何设计高效的注意力机制，使Transformer能够在多视图图像令牌与UV纹理令牌之间建立精确的空间对应，同时避免全局自注意力带来的计算爆炸和泛化退化。



## 核心方法与创新机理

### 瓶颈突破：从逐帧优化到前馈推理

传统头部化身创建流程存在严重的时间瓶颈：基于网格跟踪的方法（如VHAP）单帧需约12秒，完整序列跟踪耗时10.7小时；随后的可动画高斯优化（如GEM）还需额外27.7小时，总计约45小时才能构建一个特定主体的化身。这种逐帧优化范式使得大规模扩展极其昂贵。

MATCH的核心突破在于**彻底绕过逐帧跟踪和优化**，通过前馈Transformer直接预测具有稠密语义对应关系的3D高斯splat纹理，单帧推理仅需0.5秒。这一设计将总化身创建时间从45小时压缩至4.6小时，实现了**10倍加速**，同时保持了与优化式方法相当甚至更优的合成质量。

### 关键创新点：注册引导注意力机制

MATCH最关键的架构创新是**注册引导注意力（Registration-guided Attention）**模块。传统Transformer在处理多视图图像和UV令牌时，若采用密集自注意力，每个UV令牌需关注所有图像令牌，计算复杂度高且容易引入无关区域的噪声。

注册引导注意力的核心思想是：利用粗网格注册提供的几何先验，**限制每个UV令牌仅关注其对应头部区域的图像令牌**。具体而言，对于每对UV令牌和图像令牌，计算对应得分 $S(\mathcal{T}_{\mathrm{uv}}, \mathcal{T}_{\mathrm{img}})$：

$$S(\mathcal{T}_{\mathrm{uv}}, \mathcal{T}_{\mathrm{img}}) = \frac{\mathrm{RoI}_{\mathcal{T},\mathrm{uv}} \cap \mathcal{B}_{\mathcal{T},\mathrm{img}}}{\mathcal{B}_{\mathcal{T},\mathrm{img}}} + \lambda \cdot \frac{\mathrm{RoI}_{\mathcal{T},\mathrm{uv}}}{\mathcal{B}_{\mathrm{encomp}}}$$

该得分由两部分加权组成（λ=0.1）：第一项衡量UV令牌对应区域在图像令牌视野内的占比，第二项衡量UV令牌区域在整体包围盒中的占比。基于此得分，每个UV令牌仅关注得分最高的 $k_{T,\mathrm{img}}$ 个图像令牌。

消融实验充分验证了这一设计的决定性作用：将注册引导注意力替换为密集注意力后，LPIPS从0.187急剧恶化至0.221（Table 2），成为所有消融项中性能降幅最大的组件。同时，该机制还带来了显著的计算效率提升——推理速度明显快于密集注意力版本。

### 方法谱系与知识库定位

MATCH在头部化身重建领域的定位可从以下维度理解：

**与优化式方法的对比**：GEM（Giebenhain, CVPR 2024）和GaussianAvatars（Xu et al., TOG 2023）等优化式方法需要长时间的逐帧跟踪和高斯优化，MATCH以前馈推理替代了该流程。

**与前馈方法的差异**：
- **Avat3r**（Giebenhain et al., ArXiv 2024）和**FaceLift**（Ma et al., CVPR 2024）同样采用多视图像素对齐高斯预测，但未显式建立稠密语义对应关系，MATCH通过UV纹理映射实现了跨身份、跨表情的对应。
- **FastAvatar**（Xu et al., CVPR 2024）和**LAM**（Li et al., ECCV 2024）从单图预测3DMM附着的高斯，依赖隐式对应，MATCH的多视图输入和显式UV映射提供了更强的几何约束。
- **GPAvatar**（Cao et al., CVPR 2024）基于三平面生成可动画头部，MATCH则直接预测高斯splat纹理，支持更高效的下游应用。

**技术继承与创新**：MATCH的Transformer架构受Large Reconstruction Models（LRM）系列启发，图像标记化遵循GS-LRM方案，并融合了Sapiens预训练特征以增强泛化能力。其核心区分点在于注册引导注意力模块和UV纹理映射策略，将粗网格注册的几何先验转化为注意力约束，实现了效率与质量的双重提升。

### 稠密语义对应的下游价值

MATCH预测的高斯splats具有**跨身份、跨表情的稠密语义对应关系**，这一特性直接解锁了多项下游应用：
- **快速化身构建**：对预测序列进行PCA蒸馏即可获得可动画化身，跳过网格跟踪和CNN训练。
- **语义编辑**：可替换特定语义区域（如鼻子、胡须、嘴唇、眼睛、发型）的高斯纹理。
- **表情迁移**：将源身份的口腔表达和下颌关节迁移至目标身份。
- **身份插值**：通过因子γ在身份和表情之间平滑插值。

这些应用无需额外训练或优化，直接受益于前馈推理建立的对应关系，体现了MATCH从“重建工具”向“编辑平台”的范式拓展。



MATCH 的整体流水线以前馈 Transformer 为核心，直接从多视图图像预测具有稠密语义对应关系的 3D 高斯 splat 纹理，彻底绕开传统方法中耗时数小时的逐帧网格跟踪和高斯优化。整个流程由五个关键模块串联构成：**图像标记化**、**粗网格注册**、**UV 令牌化**、**注册引导注意力与分组注意力**，以及 **UV 去令牌化**。

### 输入与输出

给定一组校准的多视图图像（默认 12 张），MATCH 在 **0.5 秒/帧** 内预测一张 UV 纹理图，该纹理编码了 3D 高斯 splat 的全部属性——颜色、不透明度、旋转四元数、尺度和 3D 位置。纹理分辨率为 1024×1024，对应约 100 万个高斯 splat，每个 UV 令牌负责 16×16 的纹理块。

### 模块功能与数据流

1. **图像标记化**：将每张输入图像划分为 8×8 的块，融合预训练的 Sapiens 视觉特征后，通过线性投影编码为 d 维图像令牌。这一步为 Transformer 提供了富含语义信息的视觉表征。

2. **粗网格注册**：利用预训练的 TEMPEH 全局阶段估计一个粗配准网格。该网格提供了关键的几何先验——一方面用于生成 UV 令牌所需的 RGB 和 3D 位置纹理，另一方面为后续的注册引导注意力提供空间对应基础。

3. **UV 令牌化**：基于粗网格渲染 RGB 纹理和 XYZ 位置纹理，结合可学习的位置嵌入，将 UV 空间划分为 64×64 个令牌。每个 UV 令牌因此携带着网格表面特定区域的几何与外观信息。

4. **注册引导注意力与分组注意力**：这是整个流水线的核心创新。Transformer 交替执行两种注意力机制：
   - **注册引导注意力**：根据 UV 令牌与图像令牌之间的空间对应得分，限制每个 UV 令牌仅关注其对应头部区域的图像令牌，而非执行全局密集注意力。这大幅降低了计算复杂度，同时提升了合成质量与跨身份泛化能力。
   - **分组注意力**：分别在 UV 令牌和每张图像的令牌上执行自注意力，在保持线性复杂度的同时传播信息。

5. **UV 去令牌化**：将 Transformer 输出的 UV 令牌投影回高斯参数纹理，直接得到可渲染的 3D 高斯 splat。

### 训练损失

MATCH 的训练由三项损失加权组成：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{photometric}} + w_{\mathrm{geometry}} \cdot \mathcal{L}_{\mathrm{geometry}} + w_{\mathrm{reg}} \cdot \mathcal{L}_{\mathrm{reg}}$$

其中光度损失进一步分解为 LPIPS、L1 和 SSIM 的加权和：

$$\mathcal{L}_{\mathrm{photometric}} = w_{\mathrm{LPIPS}} \cdot \mathcal{L}_{\mathrm{LPIPS}} + w_{\mathrm{L1}} \cdot \mathcal{L}_{\mathrm{L1}} + w_{\mathrm{SSIM}} \cdot \mathcal{L}_{\mathrm{SSIM}}$$

几何损失约束预测的 3D 位置与真值网格顶点一致，正则化损失则施加在 UV 令牌上以促进平滑的纹理预测。

### 关键设计决策

- **对应得分机制**：注册引导注意力中的对应得分 S 定义为 UV 令牌对应区域与图像令牌覆盖区域的空间交并比，加上邻近区域占比的加权项（λ=0.1），确保每个 UV 令牌能精准定位到相关图像信息。
- **Sapiens 特征融合**：消融实验表明，移除 Sapiens 预训练特征提取器会使 LPIPS 从 0.187 恶化至 0.202，证明强大的视觉先验对泛化至关重要。
- **UV 纹理分辨率**：从 256 提升至 1024 可逐步改善重建质量（LPIPS 从 0.194 降至 0.187），但需权衡计算开销。

### 从 MATCH 到化身构建

MATCH 预测的高斯纹理可直接用于快速化身构建：跳过传统的网格跟踪和 CNN 化身训练步骤，直接对多帧预测的高斯纹理进行联合 PCA 蒸馏，构建 GEM 线性模型。这使总化身创建时间从 GEM 的 45 小时降至 4.6 小时，加速约 10 倍。

### 补充图表

![[assets/figures/papers/paper_list_l1019_https_arxiv_org_abs_2603_15811/figures/002_Figure_2.jpg]]
*Figure 2: Overview. Given calibrated multi-view input images, MATCH first predicts a coarse mesh registration using a pretrained network. We obtain RGB and XYZ textures combined with learnable positional embeddings to encode UV tokens and follow GS-LRM [67] to tokenize the input images. The image and UV tokens serve as input to a transformer with two alternating attention blocks. In the novel registration-guided attention block, we render UV coordinate images from the input views, and for each UV token restrict the attention to image tokens displaying the relevant mesh region. The subsequent grouped attention block performs attention across the UV tokens and the tokens of each input image separately....*



### 方法总览

MATCH 的核心流程如 Figure 2 所示：给定标定的多视图输入图像，系统首先预测粗网格注册，随后将 UV 纹理和图像分别编码为令牌，送入一个包含两种交替注意力模块的 Transformer 中。Transformer 输出的 UV 令牌通过去令牌化投影为高斯 splat 纹理，最终渲染出具有稠密语义对应关系的 3D 高斯表示。

### 关键模块

#### 图像标记化 (Image Tokenization)

输入图像被分割为 8×8 的块（patch），并遵循 **Avat3r**（Giebenhain et al., ArXiv 2024）的做法，将图像令牌与预训练的 **Sapiens** 特征提取器（Khirodkar et al., 2024）的输出通过拼接和线性投影融合，增强视觉表征的泛化能力。消融实验表明，移除 Sapiens 特征提取器会导致 LPIPS 从 0.187 恶化至 0.202（Table 2），证实了预训练视觉特征对跨身份泛化的重要性。

#### 粗网格注册 (Coarse Mesh Registration)

使用预训练的 **TEMPEH**（Bolkart et al., 2024）全局阶段估计粗配准网格，为后续 UV 令牌化提供几何先验。该网格注册作为引导信号，使系统能够建立 UV 空间与图像空间之间的对应关系，是注册引导注意力机制的基础。

#### UV 令牌化 (UV Tokenization)

基于粗网格生成 RGB 纹理和 3D 位置纹理，结合可学习的位置嵌入编码为 UV 令牌。MATCH 预测 64×64 个 UV 令牌，每个令牌对应 16×16 的纹理块，最终构成 1024×1024 的高斯纹理，包含约 100 万个高斯 splat。

#### 注册引导注意力 (Registration-guided Attention)

这是 MATCH 最核心的创新模块。其设计动机是：传统密集注意力在所有 UV 令牌与图像令牌之间计算全局交互，不仅计算复杂度高，还容易引入无关区域的噪声。注册引导注意力通过以下机制解决该问题：

首先，为每对 UV 令牌 $\mathcal{T}_{\mathrm{uv}}$ 和图像令牌 $\mathcal{T}_{\mathrm{img}}$ 计算对应得分 $S$：

$$S(\mathcal{T}_{\mathrm{uv}}, \mathcal{T}_{\mathrm{img}}) = \frac{\mathrm{RoI}_{\mathcal{T},\mathrm{uv}} \cap \mathcal{B}_{\mathcal{T},\mathrm{img}}}{\mathcal{B}_{\mathcal{T},\mathrm{img}}} + \lambda \cdot \frac{\mathrm{RoI}_{\mathcal{T},\mathrm{uv}}}{\mathcal{B}_{\mathrm{encomp}}}$$

其中：
- $\mathrm{RoI}_{\mathcal{T},\mathrm{uv}}$ 表示 UV 令牌对应网格区域在图像平面上的投影区域（Region of Interest）
- $\mathcal{B}_{\mathcal{T},\mathrm{img}}$ 表示图像令牌对应的图像块边界框
- $\mathcal{B}_{\mathrm{encomp}}$ 是包含所有 $\mathrm{RoI}$ 的包围框
- $\lambda = 0.1$ 为权重系数，用于平衡精确匹配与邻近区域的贡献

该得分的物理含义是：第一项衡量 UV 令牌投影区域与图像块的重叠程度（精确对应），第二项衡量该 UV 区域在整体头部中的占比（邻近容错）。得分越高，表示该图像令牌越可能包含对应 UV 令牌所需的视觉信息。

基于此得分，注册引导注意力模块限制每个 UV 令牌仅关注得分最高的 $k_{T,\mathrm{img}}$ 个图像令牌，而非所有图像令牌。消融实验（Table 8）表明，$k_{T,\mathrm{img}} \leq 100$ 时性能最佳（$k=25$ 时 LPIPS 为 0.184，$k=100$ 时为 0.187），且可微幅提升推理效率。

![[assets/figures/papers/paper_list_l1019_https_arxiv_org_abs_2603_15811/figures/024_Table_8.jpg]]
*Table 8: Quantitative ablation study for*

消融实验（Table 2）强有力地证明了该模块的关键地位：将其替换为密集注意力（Dense Attention）后，LPIPS 从 0.187 恶化至 0.221，是所有消融项中性能下降最严重的。

#### 分组注意力 (Grouped Attention)

在注册引导注意力之后，分组注意力模块分别在 UV 令牌内部和每张图像的令牌内部执行自注意力，实现信息的传播与融合。这种设计保持了线性计算复杂度，避免了跨所有令牌的二次复杂度增长。

#### UV 去令牌化 (UV De-tokenization)

Transformer 输出的 UV 令牌通过线性投影恢复为高斯 splat 属性纹理，包括颜色 $\mathbf{c}$、不透明度 $\alpha$、旋转四元数 $\phi$、尺度 $\sigma$ 和 3D 位置 $\pmb{\theta}$。

### 训练损失

总训练损失由三部分加权组成：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{photometric}} + w_{\mathrm{geometry}} \cdot \mathcal{L}_{\mathrm{geometry}} + w_{\mathrm{reg}} \cdot \mathcal{L}_{\mathrm{reg}}$$

**光度损失**约束渲染外观与真值图像一致：

$$\mathcal{L}_{\mathrm{photometric}} = w_{\mathrm{LPIPS}} \cdot \mathcal{L}_{\mathrm{LPIPS}} + w_{\mathrm{L1}} \cdot \mathcal{L}_{\mathrm{L1}} + w_{\mathrm{SSIM}} \cdot \mathcal{L}_{\mathrm{SSIM}}$$

其中 LPIPS 感知损失捕捉高层语义差异，L1 损失约束像素级精度，SSIM 损失保持结构相似性。不同训练阶段的损失权重配置详见 Table 5。

![[assets/figures/papers/paper_list_l1019_https_arxiv_org_abs_2603_15811/figures/017_Table_5.jpg]]
*Table 5: MATCH loss weights in different training stages*

**几何损失** $\mathcal{L}_{\mathrm{geometry}}$ 约束预测的 3D 位置纹理与网格注册真值之间的一致性。**正则化损失** $\mathcal{L}_{\mathrm{reg}}$ 约束高斯 splat 属性的合理性（如尺度范围、不透明度分布等）。

### GEM 线性模型

MATCH 预测的静态高斯纹理可直接用于构建可动画化身。对于特定主体，MATCH 对多帧预测的高斯纹理进行 PCA 分解，建立线性模型：

$$\mathcal{G} = \{ \mu_i + \mathbf{B}_i \mathbf{k}_i \ | \ i \in \{\alpha, \phi, \sigma, \pmb{\theta}\} \}$$

其中 $\mu_i$ 为属性 $i$ 的均值纹理，$\mathbf{B}_i$ 为 PCA 基向量矩阵，$\mathbf{k}_i$ 为低维系数。颜色 $\mathbf{c}$ 视为常量不参与 PCA。这种设计使得化身创建时间从传统 GEM 的 45.3 小时缩短至 4.6 小时（Table 4），实现了 10 倍加速。

### 补充图表

![[assets/figures/papers/paper_list_l1019_https_arxiv_org_abs_2603_15811/figures/003_Figure_3.jpg]]
*Figure 3: Correspondence score estimation between image tokens and UV tokens. To ease visualization, the full mesh is rasterized in overlay with the UV renders and patch sizes are increased*

![[assets/figures/papers/paper_list_l1019_https_arxiv_org_abs_2603_15811/figures/025_Figure_17.jpg]]
*Figure 17: Top: Quantitative ablation study for the number of input views to MATCH on Ava-256. We evaluate two scenarios: i) Changing the number of input views to MATCH while keeping the number of inputs to the coarse mesh registration model (TEM-PEH) at the default (V = 12). ii) Changing the number of input views for both TEMPEH and MATCH. Bottom: Inference speed comparison between our model with the novel registration-guided attention versus a version with dense attention across all UV and image tokens*



## 实验与关键发现

### 核心瓶颈与因果机制

传统头部化身创建流程存在严重的效率瓶颈：逐帧优化式网格跟踪（如VHAP需10.7小时）和高斯优化（如GEM需27.7小时）使得整个化身构建耗时约45小时，难以规模化扩展。MATCH通过前馈Transformer直接预测具有稠密语义对应关系的3D高斯splat纹理，将单帧推理压缩至0.5秒，彻底绕过逐帧跟踪和优化环节。

性能提升的核心因果开关是**注册引导注意力机制**（registration-guided attention）。该模块根据UV令牌与图像令牌之间的空间对应得分，限制每个UV令牌仅关注其对应头部区域的图像令牌，而非执行全局密集注意力。消融实验（Table 2）表明，密集注意力（Dense Attention）导致LPIPS恶化至0.221，而注册引导注意力将LPIPS降至0.187，是所有组件中贡献最大的设计选择。

![[assets/figures/papers/paper_list_l1019_https_arxiv_org_abs_2603_15811/figures/006_Table_2.jpg]]
*Table 2: Ablation experiments on Ava-256*

### 新视角合成主结果

Table 1汇总了在Ava-256和NeRSemble两个数据集上的新视角合成定量对比。MATCH在所有指标上一致超越现有方法：

- **Ava-256**: LPIPS 0.163（FaceLift为0.208，领先0.045），PSNR 21.661，SSIM 0.795
- **NeRSemble**: LPIPS 0.152（FaceLift为0.200，领先0.048），PSNR 25.509，SSIM 0.880

值得注意的是，MATCH仅在Ava-256上训练即可在NeRSemble上取得有竞争力的泛化结果（Figure 5），表明注册引导注意力有效抑制了跨数据集的身份过拟合。与单视图方法LAM相比，MATCH利用多视图信息将LPIPS降低约0.03-0.05，验证了多视图融合对重建保真度的增益。

![[assets/figures/papers/paper_list_l1019_https_arxiv_org_abs_2603_15811/figures/008_Figure_5.jpg]]
*Figure 5: Novel view synthesis on NeRSemble. Ours (Ava) / Ours (NeRSemble) are trained on Ava-256 and NeRSemble only, respectively*

### 消融实验关键发现

Table 2和Figure 6系统消融了核心设计选择：

1. **注意力机制**：注册引导注意力是最关键组件。密集注意力（Dense Attention）LPIPS 0.221 vs 完整方法0.187，性能差距达0.034。注册引导注意力不仅提升质量，还降低计算复杂度（Figure 17底部显示推理速度对比），使模型可线性扩展至更多输入视图。

2. **预训练视觉特征**：移除Sapiens特征提取器（w/o Sapiens）导致LPIPS升至0.202，表明大规模预训练视觉先验对跨身份泛化至关重要，尤其在训练数据有限时。

3. **UV纹理分辨率**：将纹理分辨率从256×256逐步提升至1024×1024，LPIPS从0.194降至0.187，验证了更高空间分辨率对细节重建的持续增益。

4. **注意力令牌数量**：减少注册引导注意力中每个UV令牌关注的图像令牌数 $k_{T,\text{img}}$ 至25-100范围可微幅提升性能（Table 8），表明稀疏但精准的注意力比冗余的全覆盖更有效。

### 化身构建效率与质量

Table 4对比了特定主体化身的自重建和交叉-再现性能。MATCH-based GEM在自重建任务上LPIPS为0.174，显著优于GEM的0.214和RGBAvatar的0.219；在交叉-再现任务上CSIM为0.813，略高于GEM的0.800。更重要的是，MATCH将总化身构建时间从45.3小时压缩至4.6小时，实现10倍加速，同时比最快的基线RGBAvatar（约11.5小时）还快2.5倍。

化身构建的消融（Table 11, Figure 22）揭示了两项关键改进：采用联合PCA（而非按模态独立PCA）以及固定口腔内部颜色/尺度/不透明度，可在极端表情下提升保真度，自重建LPIPS从0.180降至0.174。

![[assets/figures/papers/paper_list_l1019_https_arxiv_org_abs_2603_15811/figures/032_Figure_22.jpg]]
*Figure 22: Qualitative ablation study of the changes applied to GEM [70] to create subject-specific head avatars from MATCH’s predictions. Ours uses 150 PCA components*

### 几何重建评估

Table 3展示了全头几何重建的定量对比。MATCH在完整头部区域的点对点距离（P2P）为6.69mm，优于TEMPEH全局阶段的7.34mm。在面部区域（不含嘴、眼、耳），MATCH的P2P为2.83mm，与TEMPEH全局阶段的2.82mm相当。Figure 9的热力图可视化显示，MATCH在脸颊和额头等大面积平滑区域的重建误差更小，但在耳朵等几何复杂区域仍有改进空间。

### 失败模式与局限性

Figure 11系统展示了三类典型失败模式：

1. **身份泄漏**：在直接算术表情迁移中，当源身份和目标身份差异极大时，迁移结果可能混入目标身份特征，导致身份边界模糊。
2. **自相交表面**：从预测高斯3D位置纹理提取的网格可能包含自相交表面，尤其在口腔和耳朵等拓扑复杂区域。
3. **表情插值限制**：特定主体化身仅能对训练表情进行插值，无法跟踪眼球运动或生成训练集外的极端表情。

此外，当前训练依赖Ava-256的网格配准作为监督，未能完全摆脱人工标注数据；模型主要在统一照明的多视图工作室数据上训练，对户外自然场景的泛化有限（尽管初步实验表明可适配，Figure 19）。

### 开放问题

- 能否完全摆脱网格监督，仅通过合成数据或自监督方式训练几何部分？
- 更先进的学习型表情迁移方法（如条件VAE）是否会比当前算术式迁移更鲁棒？
- 如何利用MATCH建立的跨身份/跨表情对应关系，学习覆盖广泛身份和表情的先验模型？
- 如何在保持高效推理的同时加入对未观测区域（如口腔内部）更精细的动态建模？

### 补充图表

![[assets/figures/papers/paper_list_l1019_https_arxiv_org_abs_2603_15811/figures/004_Table_1.jpg]]
*Table 1: Novel view synthesis results on Ava-256 and NeRSemble*

![[assets/figures/papers/paper_list_l1019_https_arxiv_org_abs_2603_15811/figures/011_Table_4.jpg]]
*Table 4: Quantitative comparison of subject-specific head avatars*

![[assets/figures/papers/paper_list_l1019_https_arxiv_org_abs_2603_15811/figures/001_Figure_1.jpg]]
*Figure 1: Given calibrated multi-view images as input, MATCH infers static Gaussian splat textures in 0.5 seconds. The resulting Gaussians are in dense semantic correspondence across subjects and expressions. This enables diverse downstream applications such as fast head avatar creation, interpolation, semantic editing, and expression transfer. For visualization, we show 6 of the 12 input images, display predicted Gaussians for three separate frames, and apply a checkerboard semantic texture to highlight the dense correspondence*

![[assets/figures/papers/paper_list_l1019_https_arxiv_org_abs_2603_15811/figures/026_Figure_18.jpg]]
*Figure 18: Robustness to errors in the coarse TEMPEH mesh*



## 定位与知识库关联

### 1. 方法演进脉络

MATCH 处于头部化身创建从“逐帧优化”向“前馈预测”范式迁移的关键节点。传统方法遵循一条耗时极长的流水线：先通过可微网格跟踪（如 VHAP，约 12 秒/帧，总计 10.7 小时）获得逐帧配准，再训练 CNN 化身模型，最后通过 PCA 蒸馏得到可驱动的高斯化身（如 **GEM** (Giebenhain et al., CVPR 2024)，总计约 45 小时）。MATCH 的核心突破在于用前馈 Transformer 一次性预测具有稠密语义对应关系的高斯 splat 纹理，将单帧重建时间压缩至 0.5 秒，化身总创建时间降至 4.6 小时（10× 加速），同时跳过网格跟踪和 CNN 训练环节。

在方法谱系上，MATCH 融合了三条技术路线：

**（1）多视图前馈高斯重建。** 受 Large Reconstruction Models (LRM) 系列启发，MATCH 采用 Transformer 架构处理多视图输入。与 **Avat3r** (Giebenhain et al., ArXiv 2024) 和 **FaceLift** (Ma et al., CVPR 2024) 等像素对齐高斯预测方法相比，MATCH 的关键区别在于预测的是 UV 纹理空间中的高斯属性，而非直接在像素空间定位高斯。这一设计使其天然具备跨身份、跨表情的稠密语义对应关系——同一 UV 坐标总对应相同的语义区域（如鼻尖），而像素对齐方法缺乏这种结构化对应。

**（2）基于 UV 纹理的头部表示。** 将头部几何与外观编码为 UV 纹理图是计算机图形学的经典范式。**FastAvatar** (Xu et al., CVPR 2024) 和 **LAM** (Li et al., ECCV 2024) 从单张图像预测附着于 3DMM 的高斯 splat，隐式依赖 3DMM 的 UV 参数化建立对应。MATCH 则直接预测完整的 UV 高斯纹理（1024×1024 分辨率，约 1M 个高斯），无需 3DMM 作为中间表示，从而获得更丰富的几何表达能力（如可重建完整头部而非仅面部区域）。

**（3）可驱动高斯化身。** 在化身下游任务中，MATCH 沿用 **GEM** 的 PCA 线性模型框架，但将输入从优化式高斯替换为 MATCH 预测的高斯纹理序列。与 **GaussianAvatars** (Xu et al., TOG 2023) 和 **RGBAvatar** (Liu et al., 2024) 等优化式方法相比，MATCH-based GEM 将重建时间从 45 小时降至 4.6 小时，同时保持可比的渲染质量（自重建 LPIPS 0.174 vs GEM 0.214）。

### 2. 关键设计决策与消融证据

**注册引导注意力（Registration-guided Attention）** 是 MATCH 最核心的技术创新，也是性能增益最大的单一组件。该模块利用粗网格配准（由预训练的 **TEMPEH** (Bolkart et al., 2024) 全局阶段提供）计算每个 UV 令牌与各图像令牌的空间对应得分，限制每个 UV 令牌仅关注其对应头部区域的图像令牌。消融实验表明，将其替换为密集注意力（Dense Attention）会导致 LPIPS 从 0.187 恶化至 0.221（Table 2），证实了结构化注意力约束对合成质量和泛化能力的关键作用。该设计同时降低了计算复杂度，使推理速度显著优于密集注意力方案（Figure 17）。

**Sapiens 预训练特征** 是第二重要的设计选择。移除该特征提取器后 LPIPS 升至 0.202，表明大规模预训练的视觉特征对跨身份泛化至关重要。UV 纹理分辨率从 256 提升至 1024 可逐步改善重建质量（LPIPS 从 0.194 降至 0.187），但边际收益递减。

在化身构建阶段，采用**联合 PCA**（而非按模态独立 PCA）以及**固定口腔内部颜色/尺度/不透明度**可提升极端表情下的保真度（Table 11，LPIPS 0.174 vs 模态特定 PCA 0.180）。

### 3. 适用边界与局限

**训练监督依赖。** MATCH 当前依赖 Ava-256 数据集的网格配准作为训练监督信号，尚未完全摆脱人工标注的网格数据。这限制了其在无网格标注场景下的直接应用，但初步实验表明模型对粗网格误差具有一定鲁棒性（Figure 18），且可在自然场景图像上运行（Figure 19）。

**表情迁移的身份泄漏。** 直接的算术式表情迁移（将源身份高斯与目标表情高斯的差值相加）在极端表情或身份差异极大时可能出现身份泄漏（Figure 11a），即目标身份特征被意外带入源身份渲染结果。论文指出更先进的学习型迁移方法（如条件 VAE）可能是更鲁棒的选择。

**几何重建伪影。** 从预测的高斯 3D 位置纹理提取的网格可能包含自相交表面（Figure 11b），这在口腔、眼窝等复杂拓扑区域尤为明显。当前几何重建精度（全头 P2P 6.69mm）虽优于 TEMPEH 全局阶段，但仍落后于需要逐帧优化的方法。

**表情空间受限。** 特定主体化身仅能对训练表情进行插值，无法跟踪眼球运动（Figure 11c），且对训练集外的新颖表情泛化能力有限。这是 PCA 线性模型的固有限制。

**光照泛化。** 模型主要在统一照明的多视图工作室数据上训练，对户外自然场景的泛化需要进一步验证，但初步实验显示了适配潜力（Figure 19）。

### 4. 开放问题

1. **完全摆脱网格监督。** 能否通过合成数据渲染或自监督几何约束（如多视图光度一致性）训练几何预测部分，使方法适用于无网格标注的任意对象？
2. **更鲁棒的表情迁移。** 基于学习的表情解耦与迁移方法（如条件 VAE 或扩散模型引导）是否能消除当前算术式迁移的身份泄漏问题，同时保持稠密对应的优势？
3. **通用头部先验模型。** 如何利用 MATCH 建立的跨身份/跨表情稠密对应关系，学习覆盖广泛身份和表情空间的生成式先验模型，实现单视图或稀疏视图的高质量重建？
4. **动态口腔建模。** 在保持高效推理的前提下，如何对未观测区域（如口腔内部）引入更精细的动态建模，提升极端张嘴表情下的真实感？
5. **实时驱动与编辑。** 当前化身推理虽快（0.5 秒/帧），但尚未达到实时交互速率。进一步压缩模型或采用更高效的推理方案是否能实现实时语义编辑和表情驱动？



## 原文 PDF

![[paperPDFs/CVPR_2026/Feed_forward_Gaussian_Registration_for_Head_Avatar_Creation_and_Editing.pdf]]
