---
title: "Hunyuan3D 2.5: Towards High-Fidelity 3D Assets Generation with Ultimate Details"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Hunyuan3D_2_5_Towards_High_Fidelity_3D_Assets_Generation_with_Ultimate_Details.pdf
aliases:
- H25
- H25THF3AGUD
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在形状生成阶段，通过大规模扩展扩散模型LATTICE（10B参数，扩大高质量数据集与计算预算）捕捉精细几何先验；在纹理生成阶段，引入基于物理的PBR材质多视图生成框架，利用共享注意力掩码的双通道注意力机制确保材质空间对齐，并采用双阶段分辨率增强策略逐步提升纹理-几何对齐精度。
primary_logic: 形状的极限细节来源于对大规模高质量3D数据的充分训练，而无需牺牲表面平滑度；材质的真实感则依赖于将语义最丰富的albedo分支的参考注意力掩码共享给金属度-粗糙度通道，并通过zoom-in高分辨率训练逐步注入高频几何细节，从而在计算可行范围内实现多通道材料的一致高保真生成。
claims:
- 在形状生成定量比较中，Hunyuan3D 2.5在ULIP-T、Uni3D-T和Uni3D-I三项指标上均取得最优或持平结果（Table 1）。
- 在纹理生成定量比较中，Hunyuan3D 2.5在CLIP-FID、FID、CMMD、CLIP-I、LPIPS五个指标上全面优于所有公开对比方法（Table 2）。
- 用户研究中Hunyuan3D 2.5在图像到3D任务上的胜率达到72%，是对比商业模型的9倍，证明端到端生成质量显著领先（Figure 8）。
- LATTICE模型能够生成具有精细细节（如自行车辐条、手指数量正确）和锐利边缘的形状，同时保持表面光滑（Figure 4）。
---

# Hunyuan3D 2.5: Towards High-Fidelity 3D Assets Generation with Ultimate Details

> [!tip] 核心洞察
> 形状的极限细节来源于对大规模高质量3D数据的充分训练，而无需牺牲表面平滑度；材质的真实感则依赖于将语义最丰富的albedo分支的参考注意力掩码共享给金属度-粗糙度通道，并通过zoom-in高分辨率训练逐步注入高频几何细节，从而在计算可行范围内实现多通道材料的一致高保真生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | Hunyuan3D 2.5：面向极致细节的高保真3D资产生成 |
| 英文题名 | Hunyuan3D 2.5: Towards High-Fidelity 3D Assets Generation with Ultimate Details |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2506.16504) · [Code](https://github.com/Tencent/Hunyuan3D-2) · [arXiv](https://arxiv.org/abs/2503.19011) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Hunyuan3D 2.5 |
| Dataset | Shape generation, Texture generation |

> [!tip] 效果简介
> - Shape generation 上，ULIP-T(↑) 0.07853 vs 0.0771 (Hunyuan3D 2.0) (+0.00143)；Uni3D-T(↑) 0.2542 vs 0.2519 (Hunyuan3D 2.0) (+0.0023)。
> - Texture generation 上，CLIP-FID↓ 23.97 vs 26.86 (Paint3D) (-2.89)；FID↓ 165.8 vs 176.9 (Paint3D) (-11.1)；CMMD↓ 2.064 vs 2.400 (Paint3D) (-0.336)。

## 概述

Hunyuan3D 2.5 是一个端到端的图像到3D资产生成模型，旨在解决现有方法无法同时实现精细几何细节、锐利边缘与光滑表面，以及缺乏物理真实感PBR材质生成的瓶颈问题。该模型延续了Hunyuan3D 2.0的两阶段管线架构：首先生成无纹理的3D网格形状，再基于该形状生成纹理贴图。

在形状生成阶段，Hunyuan3D 2.5 引入了一个全新的形状基础模型——**LATTICE**，这是一个大规模扩散模型，通过扩展高质量训练数据集、模型参数量（10B参数）和计算预算，实现了对精细几何先验的充分捕捉，能够生成具有锐利边缘和平滑表面的高保真形状，而无需牺牲细节精度。

在纹理生成阶段，Hunyuan3D 2.5 提出了一个基于物理的PBR材质多视图生成框架，能够同时生成albedo、粗糙度和金属度贴图。其核心创新在于**双通道注意力机制**：将语义最丰富的albedo分支的参考注意力掩码共享给金属度-粗糙度通道，确保多通道材质在空间上严格对齐；同时采用**双阶段分辨率增强策略**，通过随机zoom-in的高分辨率训练逐步注入高频几何细节，在计算可行范围内实现多通道材料的一致高保真生成。

实验结果表明，Hunyuan3D 2.5 在形状生成和纹理生成任务上均取得了领先性能。在形状生成定量比较中，模型在ULIP-T、Uni3D-T和Uni3D-I三项指标上均达到最优或持平水平（Table 1）。在纹理生成比较中，模型在CLIP-FID、FID、CMMD、CLIP-I和LPIPS五个指标上全面优于所有公开对比方法（Table 2）。用户研究进一步验证了端到端生成质量的显著优势：在图像到3D任务上，Hunyuan3D 2.5的胜率达到72%，是对比商业模型的9倍（Figure 8）。

## 背景与动机

### 3D资产生成的核心瓶颈

高保真3D资产的自动生成是计算机图形学与视觉领域的长期目标，其应用覆盖游戏、影视、AR/VR等场景。然而，现有方法在两大关键维度上始终未能突破：**精细几何细节的生成**与**真实感材质的还原**。

在几何层面，主流3D生成模型往往面临“细节-平滑”的权衡困境——能够生成锐利边缘和复杂结构（如自行车辐条、手指等精细部件）的模型，通常会在表面引入噪声或伪影；而能保证表面光滑的模型，又倾向于丢失高频几何特征。Figure 2 直观展示了这一矛盾：现有方法要么在细节生成上失败，要么输出的形状缺乏锐度。

在纹理层面，问题更为严峻。当前开源社区的主流方案仍以RGB纹理生成为主，而RGB纹理将光照信息“烘焙”到颜色通道中，导致资产在不同光照条件下缺乏真实感。基于物理的渲染（PBR）材质——包含反照率（albedo）、金属度（metallic）和粗糙度（roughness）三通道——是工业级真实感渲染的标准，但其自动生成在开源领域仍不成熟。更关键的是，多通道PBR材质要求albedo与金属-粗糙度（MR）通道之间保持严格的空间对齐，否则会出现“金属区域错位”“粗糙度边界漂移”等伪影，而现有方法缺乏有效的跨通道对齐机制。

### 多视图一致性与纹理-几何对齐的挑战

3D纹理生成本质上是一个多视图合成问题：模型需要从多个视角为3D网格生成一致的纹理贴图。这带来了两个深层挑战：

1. **多视图一致性**：不同视角生成的纹理必须在颜色、材质属性上保持一致，否则在视角切换或烘焙到UV贴图时会产生明显接缝和视觉跳变。
2. **纹理-几何对齐**：纹理细节需要精确附着于几何表面，尤其在复杂高多边形几何体上，细微的错位即会导致纹理漂移或融合伪影。

现有方法在处理这两个挑战时往往顾此失彼。例如，基于文本条件的纹理生成方法（如**Text2Tex**，Chen et al., ICCV 2023）在多视图一致性上表现薄弱；而基于图像条件的方法（如**Paint3D**，Zeng et al., CVPR 2024）虽能利用参考图像提升保真度，但在高分辨率下的纹理-几何对齐精度仍有明显不足。

### Hunyuan3D 2.5的动机与定位

正是在上述瓶颈下，Hunyuan3D 2.5 被提出。其前身 Hunyuan3D 2.0（Zhao et al., 2025）已建立了两阶段生成管线（先形状后纹理），但在细节生成和材质真实感方面仍存在可感知的差距。Hunyuan3D 2.5 的核心动机可以归纳为三个递进目标：

- **形状端**：通过大规模扩展扩散模型，在不牺牲表面平滑度的前提下，充分捕捉精细几何先验，实现“锐利边缘+光滑表面+丰富细节”的统一。
- **纹理端**：从RGB纹理生成升级为PBR材质生成，并设计跨通道对齐机制以确保多通道材料在空间上的一致性。
- **系统端**：在计算可行的范围内，通过双阶段分辨率增强策略逐步注入高频几何细节，提升纹理-几何对齐精度，同时控制多视图融合阶段的伪影风险。

这一动机链条直接对应了Figure 3所示的两阶段管线设计：输入图像经预处理后，首先由形状生成模型LATTICE输出高保真无纹理网格，经后处理提取几何条件（法线、UV坐标等），再由PBR材质生成模型输出多视图一致的三通道材质贴图。

## 核心创新

Hunyuan3D 2.5 在继承 Hunyuan3D 2.0 两阶段管线（先形状、后纹理）的基础上，针对“精细几何细节”与“真实感材质”两大瓶颈进行了系统性的方法替换与机制创新。其核心创新可归结为四个关键的 changed slots。

### 1. 形状生成：从通用扩散模型到大规模基础模型 LATTICE

Hunyuan3D 2.5 将形状生成模型替换为全新的基础模型 **LATTICE**，这是一款参数量达 **10B** 的大规模扩散模型。与 Hunyuan3D 2.0 的 vecset-based 扩散模型相比，LATTICE 的核心变化在于 **大规模高质量数据、模型容量与计算预算的同步扩展**（Section 2.1）。这一 scaling 策略使得模型能够捕捉到更为精细的几何先验，从而在单个图像或多视图条件下，直接生成具有锐利边缘和光滑表面的高保真形状。

定性结果显示，LATTICE 能够生成如自行车辐条、正确手指数量等精细结构，而这些细节在以往方法中极易丢失或变形（Figure 4）。这表明，通过充分的训练规模扩展，模型可以在不牺牲表面平滑度的前提下，习得极致的几何细节。

### 2. 纹理生成：从 RGB 贴图到 PBR 材质的多视图生成

Hunyuan3D 2.5 将纹理生成范式从传统的 RGB 颜色贴图生成，升级为基于物理的渲染（PBR）材质生成，输出 **albedo（反照率）、roughness（粗糙度）、metallic（金属度）** 三个通道的材质贴图（Section 2.2）。这一转变使得生成的 3D 资产能够在多样化光照环境下展现出更真实的材质响应，而不再局限于单一的 baked-in 光照效果。

为实现多通道 PBR 材质的多视图一致性生成，论文提出了一个专用的多视图生成框架。该框架以预先生成的法线图、几何渲染条件及参考图像作为输入，并行生成多视图下的完整材质贴图。

### 3. 多通道对齐：基于共享注意力掩码的双通道注意力机制

多通道 PBR 生成的核心难点在于，不同材质通道（尤其是 albedo 与 roughness/metallic）之间容易出现空间不对齐，导致材质语义错位。Hunyuan3D 2.5 的解决方案是引入 **共享注意力掩码的双通道注意力机制**。

具体而言，模型首先利用 albedo 通道的查询向量 $Q_{albedo}$ 与参考图像的键向量 $K_{ref}$ 计算注意力掩码：

$$\mathbf { M } _ { a t t n } = \mathrm { S o f t m a x } \left( \frac { Q _ { a l b e d o } K _ { r e f } ^ { T } } { \sqrt { d } } \right)$$

随后，该注意力掩码 $\mathbf{M}_{attn}$ 被共享至金属-粗糙度（MR）通道，用于指导两个分支的特征更新：

$$\begin{array} { r } { z _ { a l b e d o } ^ { n e w } = z _ { a l b e d o } + \mathbf { M L P } _ { a l b e d o } \left[ \mathbf { M } _ { a t t n } \cdot V _ { a l b e d o } \right] , } \\ { z _ { M R } ^ { n e w } = z _ { M R } + \mathbf { M L P } _ { M R } \left[ \mathbf { M } _ { a t t n } \cdot V _ { M R } \right] } \end{array}$$

这一设计的因果逻辑在于：albedo 通道承载了最丰富的语义信息（颜色、纹理结构），其注意力分布能够为材质属性通道提供可靠的空间参考。通过共享注意力掩码而非独立计算，模型强制 MR 通道在 albedo 所确定的语义区域上进行特征聚合，从而从机制层面消除了多通道间的空间不对齐风险。各通道再经由独立的 MLP 映射，保留通道特定的材质属性表达。

### 4. 分辨率增强：双阶段 Zoom-in 训练策略

为在计算可行范围内提升纹理-几何对齐精度，Hunyuan3D 2.5 采用了 **双阶段分辨率增强策略**。第一阶段使用 6 视图 512×512 分辨率的图像进行基础训练；第二阶段引入随机 zoom-in 机制，对参考图像和多视图生成图像进行随机区域放大，使模型在高分辨率局部细节上进行微调。推理时，模型可利用 UniPC 采样器加速生成最高 768×768 分辨率的多视图图像。

这一策略的效用在于：zoom-in 训练迫使模型关注局部高频几何细节与纹理的对应关系，从而在复杂高多边形几何体上改善纹理-几何对齐，同时降低融合与烘焙阶段出现伪影和接缝的风险。然而，论文也指出，多视图一致性仍然是挑战，高多边形几何体上的精确对齐依然困难（Section 2.2），这一点需要读者在评估方法时予以关注。

## 整体框架

Hunyuan3D 2.5 延续了 Hunyuan3D 2.0（Zhao et al., 2025）的两阶段级联范式，将图像到 3D 资产生成解耦为**形状生成**与**纹理生成**两个顺序执行的阶段，如 Figure 3 所示。整体管线由四个核心模块串联构成：图像预处理、形状生成（LATTICE）、网格后处理、以及 PBR 材质纹理生成。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_16504/figures/003_Figure_3.jpg]]
*Figure 3: Overview of Hunyuan3D 2.5 pipeline. It separates the 3D asset generation into two stages: first, it generates the shape, and then it creates the texture based on that shape*

**输入与预处理。** 系统接收单张参考图像作为输入，首先进行背景移除与尺寸调整，为下游阶段提供统一的图像条件。

**第一阶段：形状生成。** 预处理后的图像被送入新引入的形状基础模型 **LATTICE**——一个参数量扩展至 10B 的大规模扩散模型。LATTICE 在大幅扩展的高质量数据集与计算预算下训练，能够从单张或多视图图像条件中生成具有锐利边缘、光滑表面和精细几何细节的无纹理 3D 网格（Figure 4）。该模块的核心瓶颈突破在于：通过充分的大规模训练捕捉精细几何先验，而无需牺牲表面平滑度。

**网格后处理。** 生成的网格随后经过后处理，提取法线图、UV 坐标等几何信息，为纹理生成阶段提供几何条件。

**第二阶段：PBR 材质纹理生成。** 纹理生成模块接收法线图、几何渲染条件以及原始参考图像，通过多视图 PBR 材质生成框架输出多视图一致的材质贴图（albedo、roughness、metallic）。该框架的关键设计包括：
- **双通道注意力机制**：将语义最丰富的 albedo 分支的注意力掩码共享给金属度-粗糙度（MR）通道，确保多通道材质之间的空间对齐（公式见 Section 2.2）。
- **双阶段分辨率增强策略**：第一阶段在 512×512 分辨率下进行 6 视图基础训练；第二阶段引入随机 zoom-in 训练，推理时使用 UniPC 采样器加速至最高 768×768 分辨率，逐步注入高频几何细节，改善复杂高多边形几何体上的纹理-几何对齐，同时降低融合阶段的伪影与接缝风险。

最终输出为带 PBR 材质的高保真 3D 资产，可直接用于支持物理渲染的下游应用。

## 核心模块与公式推导

Hunyuan3D 2.5 延续了 Hunyuan3D 2.0（Zhao et al., 2025）的两阶段管线架构（Figure 3）：先进行形状生成，再基于生成的形状进行纹理生成。两阶段的核心模块分别进行了根本性的升级。

### 2.1 形状生成模块：LATTICE

形状生成阶段的核心模块是 **LATTICE**——一个参数量扩展至 10B 的大规模扩散模型。其设计思路并非引入新的网络结构，而是将现有扩散模型在**高质量数据集、模型规模与计算预算**三个维度上进行大规模扩展（Section 2.1）。这一扩展策略使得模型能够从单张图像或多视图条件中捕捉到丰富的几何先验，从而生成具有以下关键特性的形状（Figure 4）：

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_16504/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of major features of the new shape generation model in Hunyuan3D 2.5*

- **精细几何细节**：能够生成如自行车辐条、正确手指数量等复杂结构。
- **锐利边缘与光滑表面**：在保持边缘锐利度的同时，不牺牲曲面的平滑性，解决了传统方法中细节与平滑度难以兼得的矛盾。

管线中，输入图像首先经过预处理（背景移除与尺寸调整），随后送入 LATTICE 生成无纹理的高保真网格，最后通过后处理提取法线、UV 坐标等几何信息，为纹理生成阶段提供条件。

### 2.2 纹理生成模块：PBR 材质多视图生成框架

纹理生成阶段的核心创新是引入了基于物理的渲染（PBR）材质生成框架，替代了前代版本的 RGB 纹理生成。该框架需要同时生成三通道材质贴图：**albedo（反照率）、roughness（粗糙度）和 metallic（金属度）**，其中 albedo 承载了最丰富的语义信息，而粗糙度与金属度（统称为 MR 通道）决定了材质的光学响应特性。

#### 双通道注意力机制（共享注意力掩码）

多通道材质生成的核心挑战在于确保 albedo 与 MR 通道之间的**空间对齐**。若各通道独立计算注意力，容易出现同一表面区域在不同材质通道中语义不一致的问题。为解决这一问题，框架采用了**共享注意力掩码**的双通道注意力机制（Section 2.2）：

首先，由 albedo 分支的查询 $Q_{albedo}$ 与参考图像的键 $K_{ref}$ 计算注意力掩码：

$$\mathbf { M } _ { a t t n } = \mathrm { S o f t m a x } \left( \frac { Q _ { a l b e d o } K _ { r e f } ^ { T } } { \sqrt { d } } \right)$$

其中 $d$ 为特征维度。该掩码 $\mathbf{M}_{attn}$ 随后被**共享**至 MR 分支，用于更新两个通道的特征：

$$\begin{array} { r } { z _ { a l b e d o } ^ { n e w } = z _ { a l b e d o } + \mathbf { M L P } _ { a l b e d o } \left[ \mathbf { M } _ { a t t n } \cdot V _ { a l b e d o } \right] , } \\ { z _ { M R } ^ { n e w } = z _ { M R } + \mathbf { M L P } _ { M R } \left[ \mathbf { M } _ { a t t n } \cdot V _ { M R } \right] } \end{array}$$

此处，$V_{albedo}$ 与 $V_{MR}$ 分别为两个通道的值向量，$\mathbf{MLP}_{albedo}$ 与 $\mathbf{MLP}_{MR}$ 是各自独立的映射网络。这一设计的核心洞察在于：**以语义最丰富的 albedo 分支作为注意力引导，通过共享其空间注意力分布来约束 MR 通道的特征聚合**，从而在保持各通道独立表达能力的条件下实现空间对齐。

#### 双阶段分辨率增强策略

为进一步提升纹理细节与几何对齐精度，框架采用了**双阶段 zoom-in 训练策略**（Section 2.2）：

- **第一阶段**：使用 6 视图 512×512 分辨率图像进行基础训练。
- **第二阶段**：在训练过程中对参考图像和多视图生成图像进行**随机 zoom-in**，使模型逐步注入高频几何细节，同时维持多视图一致性。
- **推理阶段**：使用 UniPC 采样器，支持高达 768×768 分辨率的多视图图像生成。

该策略有效改善了复杂高多边形几何体上的纹理-几何对齐质量，并降低了融合与烘焙阶段的伪影与接缝风险。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_16504/figures/005_Figure_5.jpg]]
*Figure 5: Overview of material generation framework*

## 实验与分析

### 形状生成定量评估

Hunyuan3D 2.5 的形状生成模型 LATTICE 在标准 3D 语义对齐指标上取得了最优或持平结果。**Table 1** 报告了与多个公开基线方法及商业模型的数值对比。在文本对齐指标 ULIP-T 上，LATTICE 达到 **0.07853**，略优于前代 Hunyuan3D 2.0 的 0.0771（+0.00143）；在 Uni3D-T 上达到 **0.2542**，同样领先 Hunyuan3D 2.0 的 0.2519（+0.0023）。在图像对齐指标 Uni3D-I 上，LATTICE 取得 **0.3151**，与最强基线持平或略优。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_16504/figures/008_Table_1.jpg]]
*Table 1: Numerical comparisons of different shape generation models on ULIP-T/I, Uni3D-T/I*

值得注意的是，作者明确指出 ULIP-T/I 和 Uni3D-T/I 等传统定量指标**不能完全反映模型的实际生成能力**，定性效果远超定量差距所体现的水平。这一声明提示读者在解读数值时应保持审慎——指标上的微小领先可能掩盖视觉质量上的显著差异。

**Figure 6** 提供了不同方法的形状生成视觉对比。LATTICE 生成的形状在精细细节（如自行车辐条的完整结构、手指数量的正确性）、锐利边缘保持以及表面光滑度方面展现出明显优势，这与此前 **Figure 4** 中展示的模型关键特性——在不牺牲表面平滑度的前提下捕捉极限几何细节——形成呼应。对比基线包括 **Michelangelo**（Zhao et al., NeurIPS 2023）、**Craftsman 1.5**（Li et al., 2024b）、**Trellis**（Xiang et al., 2024）以及两个闭源商业模型。

### 纹理生成定量评估

**Table 2** 展示了 PBR 材质生成模型在五个指标上与 SOTA 方法的全面对比，涵盖仅基于文本条件的方法和基于图像条件的方法两类基线。Hunyuan3D 2.5 在所有指标上均取得最优：

| 指标 | Hunyuan3D 2.5 | 最强基线 (Paint3D) | 提升幅度 |
|------|---------------|---------------------|----------|
| CLIP-FID ↓ | **23.97** | 26.86 | -2.89 |
| FID ↓ | **165.8** | 176.9 | -11.1 |
| CMMD ↓ | **2.064** | 2.400 | -0.336 |
| CLIP-I ↑ | **0.9281** | 0.8871 | +0.0410 |
| LPIPS ↓ | **0.1231** | 0.1261 | -0.0030 |

CLIP-I 的提升幅度最大（+0.0410），表明生成的纹理与参考图像在语义层面保持了更高的一致性。FID 下降 11.1 点，说明纹理分布更接近真实材质。对比基线包括 **Text2Tex**（Chen et al., ICCV 2023）、**SyncMVD**（Liu et al., SIGGRAPH Asia 2024）、**Paint-it**（Youwang et al., CVPR 2024）、**Paint3D**（Zeng et al., CVPR 2024）和 **TexGen**（Yu et al., TOG 2024）。

**Figure 7** 的视觉对比进一步揭示了定量优势的物理意义：Hunyuan3D 2.5 生成的完整材质贴图和 albedo 贴图在前视图与后视图上均表现出更好的多视图一致性，且材质分解（albedo 与金属-粗糙度通道）的空间对齐更为精确，减少了伪影和色彩偏移。

### 用户研究

端到端图像到 3D 任务的用户偏好测试（**Figure 8**）显示，Hunyuan3D 2.5 的胜率达到 **72%**，是对比商业模型的 **9 倍**。这一结果直接验证了端到端生成质量在人类感知层面的显著领先，弥补了自动指标可能无法捕捉的视觉质量维度。但需注意，测试集的具体类别分布和规模未公开，结果的普适性有待进一步验证。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_16504/figures/010_Figure_8.jpg]]
*Figure 8: User study against three latest commerical models in terms of end-to-end textured results*

### 消融分析与关键设计验证

论文通过定性消融验证了两个核心设计选择的有效性：

1. **共享注意力掩码机制**（Section 2.2）：将语义最丰富的 albedo 分支的参考注意力掩码 $\mathbf{M}_{attn}$ 共享给金属-粗糙度通道，是消除多通道材料空间不对齐的关键。公式 $\mathbf{M}_{attn} = \mathrm{Softmax}\left(\frac{Q_{albedo} K_{ref}^T}{\sqrt{d}}\right)$ 定义的掩码被同时用于更新 albedo 特征 $z_{albedo}^{new}$ 和 MR 特征 $z_{MR}^{new}$，各自通过独立的 MLP 映射实现通道特定输出。该设计的消融证据来自 Section 2.2 的定性描述（置信度 0.7），**建议手动核实原文中的具体对比结果**。

2. **双阶段分辨率增强策略**（Section 2.2）：第一阶段使用 6 视图 512×512 图像训练，第二阶段通过随机 zoom-in 注入高频几何细节，推理时使用 UniPC 采样器加速至 768×768 分辨率。该策略在维持多视图一致性的前提下显著提升了复杂高多边形几何体上的纹理-几何对齐质量，消除了融合与烘焙阶段可能出现的伪影和接缝。消融证据同样来自 Section 2.2 的定性描述（置信度 0.7），**建议手动核实原文中的具体对比结果**。

### 已知局限与失败模式

尽管整体表现优异，Hunyuan3D 2.5 仍存在以下局限：

- **多视图一致性问题**：融合与烘焙阶段仍可能出现伪影和接缝，这是多视图纹理生成方法的共性挑战。
- **高多边形对齐困难**：对于复杂几何体，精确的纹理-几何对齐依然困难，双阶段分辨率增强策略虽有所改善但未完全解决。
- **可复现性受限**：论文未提供模型扩展的训练成本、数据集统计以及双阶段训练的具体资源配置，限制了成本评估与完全复现。
- **泛化能力未知**：缺乏对非自然图像、复杂环境或未见类别上的系统评估，模型在这些场景下的表现需要进一步验证。
- **指标局限性**：现有自动指标与人类感知存在差距，形状拓扑正确性和几何平滑度的自动化评估仍是开放问题。

### 对比公平性说明

部分基线方法（如两个商业模型）为闭源系统，无法保证完全公平的比较环境。此外，测试集的具体来源、大小及类别分布未公开，可能影响结果的普适性与可复现性。在解读定量结果时应将这些因素纳入考量。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_16504/figures/009_Table_2.jpg]]
*Table 2: Quantitative comparison with state-of-the-art methods. We compare with two classes of methods, one conditioned on text only, and the other one based on image. Our method achieves the best performance compared with both classes*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_16504/figures/006_Figure_6.jpg]]
*Figure 6: Visual comparison of different methods in terms of shape generation*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_16504/figures/007_Figure_7.jpg]]
*Figure 7: Visual comparison of different methods in terms of texture generation. We compared the front and back of models generated by different methods, as well as the effects of the corresponding complete material maps and albedo maps*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_16504/figures/002_Figure_2.jpg]]
*Figure 2: Drawbacks of existing methods: failure at detail generation and incorrect PBR*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2506_16504/figures/001_Figure_1.jpg]]
*Figure 1: High quality 3D assets generated by Hunyuan3D 2.5*

## 方法谱系与知识库定位

### 1. 技术脉络与基线关系

Hunyuan3D 2.5 继承了 **Hunyuan3D 2.0**（Zhao et al., 2025）的两阶段生成范式——先形状后纹理，但在两个核心模块上进行了根本性重构。其技术定位可从形状生成与纹理生成两条脉络分别审视。

**形状生成脉络。** 该领域长期受困于“细节-平滑”的权衡：基于Transformer的 **Michelangelo**（Zhao et al., NeurIPS 2023）和 **Craftsman 1.5**（Li et al., 2024b）等隐式表示方法能在一定程度上保持表面平滑，但高频几何细节（如自行车辐条、手指数量）往往丢失；而基于稀疏结构的 **Trellis**（Xiang et al., 2024）等体素/网格方法虽能保留部分细节，却易产生粗糙表面。Hunyuan3D 2.5 的 **LATTICE** 模型通过将扩散模型参数规模扩展至 10B 并匹配大规模高质量训练数据与计算预算，在保持平滑表面的同时首次系统性地解决了精细细节生成问题（Figure 4），本质上是以规模化训练替代了架构层面的显式权衡设计。Table 1 的定量结果（ULIP-T 0.07853、Uni3D-T 0.2542、Uni3D-I 0.3151）虽领先幅度有限，但作者明确指出这些语义对齐指标无法充分反映几何质量的实质提升，定性视觉对比（Figure 6）中的差异更为显著。

**纹理生成脉络。** 现有开源方法主要面向RGB纹理生成：**Text2Tex**（Chen et al., ICCV 2023）依赖逐视图投影与修复，**SyncMVD**（Liu et al., SIGGRAPH Asia 2024）侧重多视图同步去噪，**Paint-it**（Youwang et al., CVPR 2024）和 **Paint3D**（Zeng et al., CVPR 2024）引入了不同程度的条件控制，**TexGen**（Yu et al., TOG 2024）则探索了文本引导的纹理合成。但这些方法均未涉及基于物理的渲染（PBR）材质生成，无法产出可重光照的金属度-粗糙度通道。Hunyuan3D 2.5 首次在开源框架中实现了端到端的多通道PBR材质生成，其核心创新——共享注意力掩码的双通道注意力机制——直接回应了albedo与金属-粗糙度（MR）通道之间的空间对齐难题，这是此前方法因独立处理各通道而遗留的关键缺口。Table 2 显示该方法在 CLIP-FID（23.97）、FID（165.8）、CMMD（2.064）、CLIP-I（0.9281）、LPIPS（0.1231）五项指标上全面超越所有公开对比方法，且用户研究中 72% 的胜率（Figure 8，约为商业模型的 9 倍）进一步验证了端到端生成质量的实质优势。

### 2. 适用边界与局限

**多视图一致性的残留风险。** 尽管双阶段分辨率增强策略（zoom-in训练 + UniPC采样至 768×768）有效提升了纹理-几何对齐精度，作者仍明确指出融合与烘焙阶段可能出现伪影和接缝（Section 2.2）。这意味着在需要360°无死角观察的应用场景（如AR/VR实时交互）中，生成的资产可能仍需人工后处理。

**高多边形几何体的对齐瓶颈。** 当输入形状具有极高多边形密度时，纹理-几何对齐的精确度仍是未完全解决的问题。双阶段增强策略缓解了这一问题，但未从根本上消除，这限制了模型在影视级高精度资产生产中的直接可用性。

**评估体系的固有缺陷。** 作者坦承 ULIP-T/I、Uni3D-T/I 等语义对齐指标无法充分反映模型的实际生成能力，这暗示 Table 1 中的数值差距可能低估了方法间的真实质量差异。同时，测试集的具体来源、规模与类别分布未公开，影响了结果的普适性判断。部分对比基线为闭源商业模型，无法保证完全公平的比较环境。

**规模化细节的不透明。** 论文未披露 LATTICE 模型扩展至 10B 参数的具体训练成本、数据集统计信息及缩放法则，这使得成本-收益分析和可复现性评估缺乏关键依据。双阶段分辨率增强的随机zoom策略、阶段切换准则及训练资源配置同样未公开。

### 3. 开放问题

1. **缩放法则与表示学习。** LATTICE 如何在扩展过程中保持稳定的性能提升？其内部表示是否涌现出结构化的几何先验？参数规模、数据规模与生成质量之间的量化关系尚未阐明，这限制了对更大规模扩展潜力的预测。

2. **PBR材质的解耦鲁棒性。** 生成的金属度-粗糙度通道在多样化光照条件下的解耦表现是否鲁棒？当前评估主要依赖多视图渲染一致性，缺乏在不同HDR环境贴图下对材质本征属性稳定性的系统验证。

3. **输入模态的泛化能力。** 模型是否支持文本提示驱动的生成？当输入图像存在多视角不一致（如不同视角照片拼接）时，形状生成与纹理生成模块的鲁棒性如何？这些边界条件尚未被测试。

4. **自动化几何质量评估。** 如何自动化评估生成形状的拓扑正确性（如流形性、亏格）和几何平滑度？现有语义对齐指标存在缺陷，而依赖定性或人工评判无法支撑大规模系统性改进。

5. **与后续工作的接口。** 该框架生成的PBR材质贴图能否直接输入到基于物理的实时渲染管线（如glTF标准）？与动态光照、阴影投射等下游模块的兼容性如何？这决定了其在游戏引擎、数字孪生等实际部署场景中的即插即用程度。

## 原文 PDF

![[paperPDFs/arxiv_2025/Hunyuan3D_2_5_Towards_High_Fidelity_3D_Assets_Generation_with_Ultimate_Details.pdf]]