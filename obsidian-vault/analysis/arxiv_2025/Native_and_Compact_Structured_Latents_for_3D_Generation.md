---
title: Native and Compact Structured Latents for 3D Generation
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Native_and_Compact_Structured_Latents_for_3D_Generation.pdf
project_link: https://microsoft.github.io/TRELLIS.2
code_link: https://github.com/traveller59/
aliases:
- TRELLIS.2
- TRELLIS
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入无场稀疏体素结构 O-Voxel，通过灵活对偶网格直接表示任意几何并集成 PBR 材质；结合稀疏压缩 VAE（SC-VAE）实现 16 倍空间压缩，产生紧凑原生隐空间。
primary_logic: 将网格资产直接转换为可学习的结构化体素特征，省去昂贵的场评估和渲染步骤，通过高压缩 VAE 在紧凑隐空间中进行流匹配生成，实现了几何与材料统一的高质量、高效三维生成。
claims:
- O-Voxel 的灵活对偶网格能鲁棒处理任意拓扑并保留尖锐特征，支持无缝双向转换。
- SC-VAE 在 1024³ 分辨率下仅需约 9.6K 标记，重建质量大幅超越先前方法。
- 生成管线在 1536³ 分辨率下仅需约 60 秒，几何与材质质量显著优于现有模型（用户偏好 66.5%）。
- 原生 3D 材质生成，避免多视图纹理拼接的模糊和接缝，实现物理真实的 PBR 属性。
---

# Native and Compact Structured Latents for 3D Generation

> [!tip] 核心洞察
> 将网格资产直接转换为可学习的结构化体素特征，省去昂贵的场评估和渲染步骤，通过高压缩 VAE 在紧凑隐空间中进行流匹配生成，实现了几何与材料统一的高质量、高效三维生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向三维生成的原生紧凑结构化隐表示 |
| 英文题名 | Native and Compact Structured Latents for 3D Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2512.14692) · [Project](https://microsoft.github.io/TRELLIS.2) · [Code](https://github.com/traveller59/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TRELLIS (O-Voxel + SC-VAE + Flow Matching) |
| Dataset | Toys4K Normal PSNR, Sketchfab Featured Normal PSNR, Material PBR Attributes, Image-to-3D Alignment |

> [!tip] 效果简介
> - Toys4K Normal PSNR 上，PSNR↑ 43.11 vs TRELLIS 30.29 (+12.82)。
> - Sketchfab Featured Normal PSNR 上，PSNR↑ 33.46 vs TRELLIS 27.68 (+5.78)。
> - Material PBR Attributes 上，PSNR↑ 38.89 vs N/A (无基线) (N/A)。

## 概要

三维内容生成的核心瓶颈在于现有表示方法无法同时满足**任意拓扑建模**与**完整物理材质外观（PBR）**的需求，且隐空间压缩率低导致高分辨率资产生成效率低下。本文提出 **TRELLIS** 框架，通过三项关键设计突破这一瓶颈：

1. **O-Voxel 表示**：一种无场稀疏体素结构，通过灵活对偶网格直接表示任意几何（包括开放表面、非流形结构和封闭内部），并原生集成 PBR 材质参数（基色、金属度、粗糙度、不透明度），省去昂贵的场评估与渲染步骤。
2. **SC-VAE 压缩**：全稀疏卷积残差自编码器，实现 **16 倍空间压缩**，在 1024³ 分辨率下仅需约 9.6K 标记即可高保真重建几何与材质（PSNR 大幅超越先前方法，见 Table 1）。
3. **流匹配生成**：在紧凑隐空间上训练稀疏 DiT 生成器，分阶段生成占用布局、几何隐码和 PBR 材质隐码，实现原生 3D 材质生成，避免多视图纹理拼接的模糊与接缝。

在图像到 3D 生成任务上，TRELLIS 在 1536³ 分辨率下推理仅需约 60 秒，用户偏好率达 **66.5%**，显著优于现有方法（如 Hunyuan3D 2.1 的 13.3%）。该方法将几何与材料统一在紧凑原生隐空间中，为高效、高质量的三维生成建立了新的技术范式。



### 三维生成的核心瓶颈：表示与效率的双重困境

高质量三维资产生成是计算机图形学与视觉领域的长期目标，其核心挑战可归结为两个相互纠缠的维度：**表示能力**与**生成效率**。

在表示层面，现有主流方法长期依赖基于场的隐式表示——如符号距离场（SDF）或基于等值面提取的Flexicubes。这类方法虽然能够产生光滑表面，却存在根本性的拓扑约束：它们天然假设封闭、流形的几何结构，难以同时建模任意拓扑（开放曲面、非流形结构、封闭内部空腔）与完整的物理材质外观（PBR）。这一限制使得许多真实世界资产——如带有薄壳结构的衣物、包含内部零件的机械体、或半透明材质——无法被统一且精确地表示。

在效率层面，现有隐空间（latent space）的压缩率普遍偏低。以先前方法TRELLIS（SLAT）为例，其空间压缩率仅为4×，导致高分辨率资产（如1024³或更高）需要极大量的latent token才能表示，直接推高了后续生成模型的推理成本与时间。这种低效的压缩使得端到端的高分辨率三维生成在计算上难以负担。

### 现有方法的缺口

综合来看，当前三维生成管线存在三个结构性缺口：

1. **表示缺口**：缺乏一种能够同时编码任意拓扑几何与完整PBR材质（基色、金属度、粗糙度、不透明度）的统一表示形式。现有方法要么仅建模几何（如纯SDF方法），要么将纹理作为后处理步骤通过多视图烘焙附加，这不可避免地引入模糊、接缝与不一致性。

2. **压缩缺口**：隐空间自编码器的压缩率不足，导致latent token数量随分辨率急剧膨胀。这限制了生成模型可处理的最大分辨率，也使得高质量资产生成的推理时间过长。

3. **生成缺口**：由于表示与压缩的限制，现有生成模型难以在合理的计算预算内同时产出高几何精度与物理真实材质的三维资产。多视图纹理拼接方案尤其容易在复杂拓扑处产生视觉伪影。

### 本文动机

针对上述困境，本文提出一种全新的技术路线：**以原生紧凑的结构化隐表示为核心，构建从表示、压缩到生成的一体化框架**。核心思路是摒弃传统的场式表示，转而设计一种“无场”（field-free）的稀疏体素结构——O-Voxel，使其能够通过灵活对偶网格直接表示任意拓扑并集成PBR材质参数。在此基础上，通过全稀疏卷积变分自编码器（SC-VAE）实现16×的高倍率空间压缩，产生紧凑的隐空间。最终，在该紧凑隐空间上应用条件流匹配（Conditional Flow Matching）进行高效生成，实现几何与材质统一的高质量三维资产生成。

这一设计使得在1536³分辨率下生成完整PBR材质的三维资产仅需约60秒，且重建质量与用户偏好均显著超越现有方法（用户偏好率达66.5%，相较于最强基线Hunyuan3D 2.1的13.3%）。



## 核心方法与创新机理

TRELLIS 的核心创新在于，它彻底跳出了“场函数拟合+后处理”的主流范式，转而构建了一套**原生紧凑的结构化隐表示**体系。这一体系的三个关键支点——O-Voxel 表示、SC-VAE 压缩架构和原生 PBR 材质生成——共同解决了现有方法在拓扑表达能力、压缩效率与材质真实性上的根本矛盾。

### 1. 无场几何表示：O-Voxel 灵活对偶网格

现有方法（如基于 SDF 或 Flexicubes 的等值面场）在表示任意拓扑时面临结构性缺陷：它们难以同时处理开放表面、非流形结构和封闭内部细节，且尖锐特征在提取过程中易被平滑丢失。TRELLIS 提出的 **O-Voxel 灵活对偶网格**（Flexible Dual Grid）绕过了场函数拟合这一瓶颈。

其核心机制是：在稀疏体素的主网格上构建对偶网格，每个主网格单元对应一个对偶顶点，每条主网格边对应一个对偶四边形面。对偶顶点的位置并非固定于单元中心，而是通过最小化**二次误差函数**（QEF）动态求解：

$$\min_{\boldsymbol{v} \in \mathrm{voxel}} e(\boldsymbol{v}) = \sum_i d_{\Pi,i}^2 + \lambda_{\mathrm{bound}} \sum_j d_{L,j}^2 + \lambda_{\mathrm{reg}} d_{\hat{\pmb{q}}}^2$$

该函数同时约束顶点到切平面的距离、边界对齐和正则项，使得对偶网格能够自适应地贴合任意几何形状。同时，对偶面的存在性由边上的符号变化标志 $\delta$ 决定，允许网格自然地产生边界和孔洞。这一设计实现了**网格资产与 O-Voxel 之间的无缝双向转换**（Fig 3），无需有损预处理，且能鲁棒保留尖锐边和法向不连续性（置信度 0.95）。

### 2. 极致压缩：稀疏残差自编码器（SC-VAE）

隐空间的紧凑性直接决定了生成模型的效率上限。先前方法（如 TRELLIS 的 SLAT）仅实现 4× 空间压缩，而 TRELLIS 通过 **SC-VAE** 将压缩率提升至 **16×**——在 $1024^3$ 分辨率下仅需约 9.6K 个标记，却实现了远超先前方法的重建质量（Table 1：Toys4K Normal PSNR 43.11 vs. TRELLIS 30.29，提升 +12.82 dB）。

这一突破来自两个关键设计：

- **稀疏下/上采样残差捷径**：下采样时将 8 个子体素特征堆叠到通道维并分组平均，得到粗级残差估计；上采样时通过通道到空间的解堆叠和组内复制，将粗特征分布回精细网格。这有效保留了跨尺度的结构信息，避免了稀疏卷积中常见的信息丢失。
- **优化的残差块**：将标准双卷积残差块替换为单卷积 + 宽点态 MLP 的 ConvNeXt 风格设计，在提升重建质量的同时保持稀疏卷积的计算效率。消融实验（Table 3）证实，去除稀疏残差自编码在 16× 压缩时导致 Mesh Distance 从 1.032 升至 1.747，32× 时更恶化至 7.394；而优化残差块相比标准双卷积进一步将 MD 从 1.198 降至 1.032。

### 3. 原生 PBR 材质生成

现有管线将材质生成视为几何生成的后处理步骤，依赖多视图纹理烘焙，这不可避免地引入视图间模糊、接缝和光照不一致。TRELLIS 首次将 **PBR 材质参数直接编码到 O-Voxel 的体素特征中**：

$$\pmb{f}_i^{\mathrm{mat}} = (\pmb{c}_i, m_i, r_i, \alpha_i)$$

每个激活体素携带 6 通道材质信息（基色、金属度、粗糙度、不透明度），与几何特征联合学习。生成时，材质生成器以几何隐码为条件，直接产出 PBR 属性，实现了**物理真实的材质生成**（Fig 7），避免了多视图拼接的固有缺陷（置信度 0.9）。

### 创新总结

这三个创新形成了完整的因果链：O-Voxel 提供了统一几何与材质的表达能力，SC-VAE 将这一表示压缩为极致紧凑的隐空间，流匹配生成器则在这一高效隐空间中进行高质量生成。最终在 $1536^3$ 分辨率下，整个生成过程仅需约 60 秒（~35s 几何 + ~25s 材质），且用户偏好率达到 66.5%，远超最强基线 Hunyuan3D 2.1 的 13.3%（Table 2）。



TRELLIS 的整体管线由三个核心模块串联构成：**O‑Voxel 原生表示**、**稀疏压缩变分自编码器（SC‑VAE）** 以及 **稀疏流匹配生成器**。该设计遵循“表示‑压缩‑生成”的递进范式，将三维资产生成转化为在紧凑结构化隐空间中的条件生成问题，其宏观流程如 Figure 2 所示。

### 1. 输入‑输出流与模块关系

管线的数据流可概括为以下三个阶段：

1. **原生表示阶段（O‑Voxel 转换）**  
   输入为带 PBR 材质的三维网格资产。通过 O‑Voxel 的灵活对偶网格（Flexible Dual Grid）结构，将网格无损转换为稀疏体素特征集合 $\pmb{f} = \{ (\pmb{f}_i^{\mathrm{shape}}, \pmb{f}_i^{\mathrm{mat}}, \pmb{p}_i) \}_{i=1}^{L}$（Eq. 1），其中每个激活体素同时编码几何特征、六通道材质特征（基色、金属度、粗糙度、不透明度，Eq. 3）及体素坐标。该转换支持任意拓扑（开放曲面、非流形、封闭内部结构）并保留尖锐特征（Sec 3.1.1, Fig 3）。

2. **压缩阶段（SC‑VAE 编解码）**  
   编码器将高分辨率 O‑Voxel 压缩为紧凑的结构化隐码，空间压缩率达 16×（相较于先前 SLAT 的 4× 压缩）。解码器从隐码重建完整 O‑Voxel，再通过双向转换算法（Algo 1‑4）恢复为网格资产。SC‑VAE 采用全稀疏卷积架构，并通过稀疏上下采样的残差捷径（Eq. 4‑5）增强信息流动（Sec 3.2.1, Fig 4）。

![[assets/figures/papers/Native_and_Compact_Structured_Latents_for_3D_Generation_06a8dd9e0b93/figures/004_Figure_4.jpg]]
*Figure 4: The network structure of SC-VAE*

3. **生成阶段（稀疏流匹配生成器）**  
   在 SC‑VAE 产生的紧凑隐空间上，级联三个稀疏 DiT 模型（每个约 1.3B 参数，宽度 1536，30 个块，12 个头，MLP 宽度 8192）分别负责：
   - **稀疏结构生成器**：生成占用布局（哪些体素被激活）；
   - **几何生成器**：在激活体素内生成几何隐码；
   - **材质生成器**：基于几何结构生成 PBR 材质隐码。
   生成过程以条件流匹配（Conditional Flow Matching, Eq. 11）为训练目标，从随机噪声逐步去噪得到目标隐码（Sec 3.3）。

### 2. 管线设计的因果逻辑

整个框架的核心因果链可归纳为：

> **“无场”表示 → 高压缩隐空间 → 高效生成**

- **因果瓶颈**：传统等值面场（SDF / Flexicubes）需昂贵场评估，且无法统一处理任意拓扑与完整 PBR 材质。  
- **因果操纵点**：O‑Voxel 用灵活对偶网格直接表示表面几何与材质，省去场评估和渲染步骤；SC‑VAE 通过稀疏残差自编码实现 16× 空间压缩，产生紧凑原生隐空间。  
- **因果效果**：在 1024³ 分辨率下仅需约 9.6K 标记即可实现高保真重建（Table 1），生成 1536³ 资产仅需约 60 秒（Figure 1 中部），且用户偏好率达 66.5%（Table 2）。

### 3. 训练与推理流程

- **SC‑VAE 训练**：分两阶段进行。第一阶段使用低分辨率数据，以直接 O‑Voxel 重建损失（Eq. 6）和 KL 散度训练；第二阶段加入高分辨率渲染感知损失（Eq. 7‑10），提升视觉质量（Sec 3.2.2）。训练使用 16 块 H100 GPU，批大小 128。
- **生成器训练**：在约 80 万资产的 TexVerse 数据集上训练，使用 32 块 H100 GPU，批大小 256（Sec 4）。
- **推理时缩放**：级联推理策略可将生成 O‑Voxel 降采样后重新应用几何生成，产生更精细细节（Fig 8）。

![[assets/figures/papers/Native_and_Compact_Structured_Latents_for_3D_Generation_06a8dd9e0b93/figures/010_Figure_8.jpg]]
*Figure 8: Scaling up resolution for finer detail and compute for higher quality during test time. (Best viewed with zoom)*

### 4. 需人工核实之处

- 各模块间的隐码维度、特征通道数等具体超参数在现有证据中未充分展开，需查阅 Table 4‑5 及附录获取完整架构细节。
- 双向转换算法（Algo 1‑4）的具体步骤仅在高层次描述，实现细节需参考源代码。



### 3.1 O-Voxel：原生结构化表示

O-Voxel 是 TRELLIS 的核心数据表示，将三维资产直接编码为一组稀疏体素上的特征元组。在分辨率为 $N \times N \times N$ 的规则三维网格上，每个激活体素 $i$ 携带一个特征元组（见 Figure 3）：

$$
\pmb{f} = \{ (\pmb{f}_i^{\mathrm{shape}}, \pmb{f}_i^{\mathrm{mat}}, \pmb{p}_i) \}_{i=1}^{L}
$$

其中 $\pmb{f}_i^{\mathrm{shape}}$ 为几何特征，$\pmb{f}_i^{\mathrm{mat}}$ 为材质特征，$\pmb{p}_i$ 为体素坐标，$L$ 为激活体素总数。该表示的关键优势在于**无场（field-free）**——直接存储结构化特征而非隐式场，避免了昂贵的场评估与渲染步骤。

#### 3.1.1 灵活对偶网格（Flexible Dual Grid）

O-Voxel 的几何表示基于灵活对偶网格。在每个原始体素单元内定义一个对偶顶点 $\boldsymbol{v}$，在每条原始边上定义一个四边形面。对偶顶点的位置通过最小化二次误差函数（QEF）求得：

$$
\min_{\boldsymbol{v} \in \mathrm{voxel}} e(\boldsymbol{v}) = \sum_i d_{\Pi,i}^2 + \lambda_{\mathrm{bound}} \sum_j d_{L,j}^2 + \lambda_{\mathrm{reg}} d_{\hat{\pmb{q}}}^2
$$

其中 $d_{\Pi,i}^2$ 为对偶顶点到表面切平面的距离，$d_{L,j}^2$ 为边界对齐项，$d_{\hat{\pmb{q}}}^2$ 为正则项。该公式允许对偶顶点在体素内灵活移动，从而**鲁棒处理任意拓扑（开放曲面、非流形、封闭内部）并保留尖锐特征**（见 Figure 3 首行）。对偶面的存在性由原始边是否穿过表面决定，实现无缝双向转换（Mesh ⇄ O-Voxel）。

#### 3.1.2 材质编码

O-Voxel 将物理真实感渲染（PBR）材质参数直接编码为每个激活体素的六通道特征向量：

$$
\pmb{f}_i^{\mathrm{mat}} = (\pmb{c}_i, m_i, r_i, \alpha_i)
$$

其中 $\pmb{c}_i$ 为基色（RGB），$m_i$ 为金属度，$r_i$ 为粗糙度，$\alpha_i$ 为不透明度。该原生 3D 材质表示避免了多视图纹理拼接中的模糊和接缝问题，实现了几何与材质的统一建模。

### 3.2 SC-VAE：稀疏压缩变分自编码器

SC-VAE 将高分辨率 O-Voxel 压缩为紧凑隐空间，实现 **16 倍空间压缩**（从 $1024^3$ 分辨率降至约 9.6K 标记）。

#### 3.2.1 稀疏残差自编码架构

SC-VAE 采用全稀疏卷积架构（见 Figure 4），其核心创新包括：

1. **优化的残差块**：将标准双卷积设计替换为单卷积层 + 宽点态 MLP（ConvNeXt 风格），在稀疏卷积场景下提升效率与质量。

2. **稀疏下采样残差捷径**：将 8 个子体素特征沿通道维堆叠后分组平均，得到粗级残差估计：

$$
F_{\mathrm{coarse}}^{\mathrm{raw}} = \mathrm{stack}(F_{\mathrm{child}_1}, \dots, F_{\mathrm{child}_s}) \in \mathbb{R}^{8C}, \quad F_{\mathrm{coarse}} = \mathrm{avg\_groups}(F_{\mathrm{coarse}}^{\mathrm{raw}}) \in \mathbb{R}^{C'}
$$

3. **稀疏上采样残差捷径**：通过通道到空间的解堆叠和组内复制，将粗特征分布回精细网格：

$$
F_{\mathrm{fine}}^{\mathrm{raw}} = \mathrm{unstack}(F_{\mathrm{coarse}}) \in \mathbb{R}^{8C'/8}, \quad F_{\mathrm{fine}} = \mathrm{dup\_groups}(F_{\mathrm{fine}}^{\mathrm{raw}}) \in \mathbb{R}^{C}
$$

#### 3.2.2 两阶段训练损失

**第一阶段损失**（低分辨率直接重建）：

$$
\mathcal{L}_{\mathrm{s1}} = \lambda_{\mathrm{v}} |\hat{v} - v|_2^2 + \lambda_{\delta} \mathrm{BCE}(\hat{\delta}, \delta) + \lambda_{\rho} \mathrm{BCE}(\hat{\rho}, \rho) + \lambda_{\mathrm{mat}} |\hat{\pmb{f}}^{\mathrm{mat}} - \pmb{f}^{\mathrm{mat}}|_1 + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}}
$$

其中各项分别对应：顶点位置 MSE、面标志 BCE、裁剪掩码 BCE、材质特征 L1 及 KL 散度。

**第二阶段损失**（高分辨率渲染感知监督）：

$$
\mathcal{L}_{\mathrm{s2}} = \mathcal{L}_{\mathrm{s1}} + \mathcal{L}_{\mathrm{render}}
$$

渲染感知损失 $\mathcal{L}_{\mathrm{render}}$ 分为几何和材质两部分。几何渲染损失为：

$$
\mathcal{L}_{\mathrm{render}}^{\mathrm{shape}} = \| \hat{m} - m \|_1 + 10 \cdot \| \hat{d} - d \|_1 + d_{\mathrm{p}}(\hat{\pmb{n}}, \pmb{n})
$$

材质渲染损失为：

$$
\mathcal{L}_{\mathrm{render}}^{\mathrm{mat}} = d_{\mathrm{p}}(\hat{\pmb{c}}, \pmb{c}) + d_{\mathrm{p}}(m\hat{\pmb{r}}\pmb{a}, m\pmb{r}\pmb{a})
$$

其中感知距离 $d_{\mathrm{p}}$ 结合 L1、SSIM 和 LPIPS：

$$
d_{\mathrm{p}}(\pmb{a}, \pmb{b}) = \| \pmb{a} - \pmb{b} \|_1 + 0.2 \cdot d_{\mathrm{SSIM}} + 0.2 \cdot d_{\mathrm{LPIPS}}
$$

### 3.3 生成管线：稀疏流匹配

生成阶段采用三个级联的稀疏 DiT（Diffusion Transformer），每个约 1.3B 参数（宽度 1536，30 层，12 头，MLP 宽度 8192）：

1. **稀疏结构生成器**：生成占用布局。
2. **几何生成器**：在激活体素内生成几何隐码。
3. **材质生成器**：基于几何结构生成 PBR 材质隐码（条件于几何隐码）。

所有生成器均采用条件流匹配（Conditional Flow Matching）训练：

$$
\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t, \mathbf{x}_0, \epsilon} \| \pmb{v}_{\theta}(\pmb{x}(t), t) - (\epsilon - \pmb{x}_0) \|_2^2
$$

其中 $\pmb{v}_{\theta}$ 为待学习的向量场网络，$\pmb{x}_0$ 为目标隐码，$\epsilon$ 为噪声样本。该损失驱动网络学习从噪声到目标隐码的最优传输路径，实现高效采样（$1536^3$ 分辨率约 60 秒完成几何与材质生成）。

### 关键设计总结

| 模块 | 核心机制 | 作用 |
|------|---------|------|
| O-Voxel 灵活对偶网格 | QEF 最小化 + 对偶面存在性判定 | 任意拓扑几何表示，保留尖锐特征 |
| O-Voxel 材质编码 | 六通道 PBR 参数 | 原生 3D 物理材质，避免多视图拼接 |
| SC-VAE 稀疏残差捷径 | 通道-空间堆叠/解堆叠 | 16× 空间压缩，保持重建精度 |
| SC-VAE 两阶段训练 | 直接重建 + 渲染感知损失 | 保真度与视觉质量平衡 |
| 级联稀疏 DiT | 结构→几何→材质三阶段生成 | 高质量、高效率的端到端生成 |

### 补充图表

![[assets/figures/papers/Native_and_Compact_Structured_Latents_for_3D_Generation_06a8dd9e0b93/figures/001_Figure_1.jpg]]
*Figure 1: Left: A 1536³ asset reconstruction by our method. Despite the high compactness of the latents (see token counts below), it faithfully recovers extremely fine geometric and material details, supports arbitrary topology, and preserves enclosed structures (shown in the second row). Middle: A 1536³ 3D asset generated in about one minute (∼35s for shape and ∼25s for texture; see more runtime in bottom row). Building on our latents, the generator efficiently produces high-quality PBR-textured assets, delivering intricate geometric detail and realistic materials across open-domain inputs. Right: Latent representation comparison on shape reconstruction. Our method achieves much higher fidelity with...*

![[assets/figures/papers/Native_and_Compact_Structured_Latents_for_3D_Generation_06a8dd9e0b93/figures/005_Figure_5.jpg]]
*Figure 5: High-quality 3D assets generated by our method, featuring intricate geometric details and physically accurate materials with high visual fidelity, including thin structures, open surfaces, and translucent regions that highlight the model’s expressive capability*

![[assets/figures/papers/Native_and_Compact_Structured_Latents_for_3D_Generation_06a8dd9e0b93/figures/003_Figure_2.jpg]]
*Figure 2: Overview of our approach. We introduce O-Voxel for shape and material representation (Sec. 3.1), based on which we employ Sparse Compression VAEs for compact latent space learning (Sec. 3.2) and large flow models for 3D generation (Sec. 3.3)*



## 实验与关键发现

### 重建质量与效率

SC‑VAE 在紧凑隐空间下的重建质量显著超越先前方法。在 Toys4K 测试集上，本方法以仅约 **9.6K** 个 token（1024³ 分辨率）实现了 **43.11 dB** 的法线 PSNR，相比 TRELLIS 的 30.29 dB 提升 **+12.82 dB**（Table 1）。在 Sketchfab Featured 数据集上，法线 PSNR 达到 33.46 dB（TRELLIS 为 27.68 dB，提升 +5.78 dB）。即使与采用更密集表示的 **Dora (Shape2Vecset)** 和 **Direct3D‑s2** 等基线相比，本方法在 Mesh Distance（MD）和 Chamfer Distance（CD）上仍保持大幅领先，同时 token 数量远少于对手（Figure 1 右面板）。

![[assets/figures/papers/Native_and_Compact_Structured_Latents_for_3D_Generation_06a8dd9e0b93/figures/006_Table_1.jpg]]
*Table 1: Comparison of shape reconstruction efficiency and fidelity. MD and CD is reported $\times$ 1 $0 ^ { 6 }$ ; runtime meaured on an A100 GPU*

材质重建方面，PBR 属性（基色、金属度、粗糙度、不透明度）的 PSNR 达到 **38.89 dB**，LPIPS 为 0.033；渲染阴影图像的 PSNR 为 38.69 dB，LPIPS 为 0.026（Sec 4.1）。这些结果表明 O‑Voxel 的灵活对偶网格不仅能鲁棒处理任意拓扑，还能高保真地保留材质细节。

推理效率上，本方法在 H100 GPU 上约 **3 秒**完成 512³ 资产重建，**17 秒**完成 1024³，**60 秒**完成 1536³（Figure 1），兼顾了高分辨率下的实时性需求。

### 生成质量与用户偏好

在图像到三维生成任务上，本方法在所有自动化指标上均取得最优。CLIP Score 达到 **0.894**，超过表中所有竞争者（Table 2）。用户研究进一步验证了感知质量优势：在整体偏好投票中，本方法获得 **66.5%** 的偏好率，而最强基线 **Hunyuan3D 2.1** 仅获 13.3%（Table 2），优势达 +53.2 个百分点。

![[assets/figures/papers/Native_and_Compact_Structured_Latents_for_3D_Generation_06a8dd9e0b93/figures/008_Table_2.jpg]]
*Table 2: Comparison of image-to-3D generation results. -N: measured with normal map*

定性对比（Figure 6）显示，本方法生成的资产在法线细节和 PBR 材质分解上均优于基线——基色、金属度和粗糙度通道清晰且物理一致，而基线常出现模糊或伪影。Figure 5 展示了本方法在薄结构、开放曲面和半透明区域上的表达能力，验证了 O‑Voxel 对任意拓扑的建模能力。

### 材质生成：原生 3D vs. 多视图烘焙

与依赖多视图纹理拼接的 **Hunyuan3D‑Paint** 和 **TEXGen** 相比，本方法的原生 3D PBR 材质生成避免了视图间模糊和接缝问题（Figure 7）。生成管线中的材质生成器以几何隐码为条件，直接在 3D 空间预测 PBR 参数，产出的材质在不同光照条件下保持一致且物理真实。

![[assets/figures/papers/Native_and_Compact_Structured_Latents_for_3D_Generation_06a8dd9e0b93/figures/009_Figure_7.jpg]]
*Figure 7: Visual comparison of PBR texture generation*

### 消融实验

Table 3 报告了 SC‑VAE 架构设计的消融结果：

![[assets/figures/papers/Native_and_Compact_Structured_Latents_for_3D_Generation_06a8dd9e0b93/figures/007_Table_3.jpg]]
*Table 3: Ablation study of SC-VAE architecture designs*

- **稀疏残差自编码器**：移除残差连接后，在 16× 压缩下几何质量严重退化——MD 从 1.032 升至 1.747；在 32× 压缩下退化更为剧烈（7.394 vs. 1.405），证实了残差捷径对深层稀疏网络的关键作用。
- **优化残差块设计**：采用单卷积 + 点态 MLP 的 ConvNeXt 风格残差块，相比标准双卷积设计进一步提升了重建质量（MD 1.032 vs. 1.198，PSNR 27.26 vs. 26.67），同时降低了计算开销。
- **压缩率**：16× 压缩（约 9.6K token）在质量与紧凑性之间取得最佳平衡；32× 压缩虽进一步减少 token 数，但质量下降明显。

### 测试时扩展

本方法支持测试时分辨率扩展以换取更精细细节（Figure 8）。将生成的低分辨率 O‑Voxel 降采样后重新应用几何生成器（级联推理），可在不重新训练的情况下提升几何细节和结构稳定性。这一机制为不同算力预算下的质量调节提供了灵活入口。

### 失败模式与局限性

尽管整体性能优异，方法仍存在以下已知局限：

1. **亚体素混叠**：当几何特征小于单个体素时（如两个极近的平行面），灵活对偶网格可能产生模糊或表面平均，导致细节丢失（Sec 5）。
2. **小孔问题**：解码器在高分辨率稀疏结构中偶尔无法保证完全封闭的流形表面，需依赖后处理（如孔洞填充）来修复。
3. **语义信息缺失**：O‑Voxel 当前仅编码几何与材质，未显式包含部件级分割或图拓扑结构，限制了在需要语义理解的下游任务中的直接应用。

以上失败模式提示，未来工作可探索在 O‑Voxel 中融入部件级语义、改进解码器稳定性以从根本上消除小孔，以及在不牺牲紧凑性的前提下提升对极薄结构的表示精度。

### 补充图表

![[assets/figures/papers/Native_and_Compact_Structured_Latents_for_3D_Generation_06a8dd9e0b93/figures/013_Figure_9.jpg]]
*Figure 9: Speed test for FlexGEMM backend and baselines including Spconv [11], Torchsparse [58], fvdb [62], and WarpConvNet [8]*

![[assets/figures/papers/Native_and_Compact_Structured_Latents_for_3D_Generation_06a8dd9e0b93/figures/012_Table_4.jpg]]
*Table 4: Architectural details of the SC-VAE encoder. The decoder follows a symmetrical design*

![[assets/figures/papers/Native_and_Compact_Structured_Latents_for_3D_Generation_06a8dd9e0b93/figures/002_Figure_3.jpg]]
*Figure 3: Illustration of O-Voxel and the instant bidirectional convertion between 3D asset and O-Voxel*



## 定位与知识库关联

### 表示层谱系：从等值面场到无场原生体素

三维生成的核心瓶颈长期受制于几何表示的取舍。主流方法依赖基于场的等值面表示（如 SDF、Flexicubes），其优势在于连续性和可微性，但代价是：无法原生表示开放曲面、非流形结构和封闭内部，且每次查询都需要昂贵的场评估。TRELLIS 的前代版本 **SLAT** 已尝试引入稀疏结构化隐空间，但其压缩率仅 4×，且仍受限于等值面场的拓扑约束。

本文提出的 **O-Voxel** 彻底跳出了“场”的范式，转而采用**灵活对偶网格（Flexible Dual Grid）** 直接编码几何。其核心机制是：在稀疏主网格的每个激活体素内，通过求解二次误差函数（QEF，Eq. 2）自适应调整对偶顶点位置，并动态决定对偶面的存在性。这使得 O-Voxel 能够鲁棒处理任意拓扑——包括开放边界、薄壳结构、透明区域和内部封闭空间——同时保留尖锐特征和法线不连续性，无需像传统方法那样进行有损的预处理（如四面体化或水密化）。

这一设计将 O-Voxel 置于表示谱系中一个独特位置：它兼具体素表示的离散可控性和网格表示的拓扑灵活性，且支持与标准网格资产的**瞬时双向转换**（Algo 1-4），无需昂贵的优化或渲染步骤。

### 外观建模谱系：从纹理烘焙到原生 PBR 材质

现有三维资产生成管线（如 **Hunyuan3D-Paint**、**TEXGen**）普遍采用“几何生成 + 多视图纹理烘焙”的后处理范式。这种分离式方案存在根本性缺陷：多视图纹理拼接引入模糊和接缝伪影，且仅能生成漫反射颜色，无法还原物理真实的材质属性（金属度、粗糙度等）。

TRELLIS 将外观建模从 2D 纹理空间拉回 3D 原生空间。每个激活体素直接编码六通道 PBR 材质特征（基色、金属度、粗糙度、不透明度，Eq. 3），与几何特征统一在同一 O-Voxel 结构中。材质生成器以几何隐码为条件，在稀疏体素上直接预测 PBR 参数，实现了几何与材质的**原生耦合生成**。这从根本上消除了多视图拼接的歧义性，使生成的资产支持物理渲染和重新打光。

### 压缩与生成谱系：从 Transformer 到全稀疏架构

在隐空间学习层面，前代方法 **SLAT** 采用 Transformer 架构处理稀疏标记，计算复杂度随体素数平方增长，限制了可处理的体素规模和压缩率。本文的 **SC-VAE** 转向**全稀疏卷积 + 残差自编码**架构，并通过两个关键设计实现高效压缩：

1. **稀疏残差捷径**（Eq. 4-5）：在下采样时，将 8 个子体素特征堆叠到通道维并分组平均，形成粗级残差估计；上采样时通过通道到空间的解堆叠和组内复制恢复细粒度信息。这使得网络在 16× 空间压缩下仍能保留高频细节。

2. **ConvNeXt 风格残差块**：用单卷积层 + 宽点态 MLP 替代标准双卷积设计，在稀疏卷积中显著降低计算开销。

消融实验（Table 3）验证了这些设计的必要性：去除稀疏残差自编码导致 16× 压缩时几何质量严重退化（MD 从 1.032 升至 1.747），32× 时尤其严重（7.394 vs 1.405）；优化残差块进一步将 MD 从 1.198 降至 1.032。

在生成端，TRELLIS 采用**三阶段级联稀疏 DiT**（结构 → 几何 → 材质），每个 DiT 约 1.3B 参数，在流匹配框架下逐步生成。级联推理策略（将生成 O-Voxel 降采样后重新应用几何生成）可在测试时扩展分辨率，产生更精细的细节。

### 适用边界与局限

**适用场景**：TRELLIS 在开放域图像到三维资产生成任务中表现最优，尤其适合需要 PBR 材质和任意拓扑的高质量资产创建。1024³ 分辨率下仅需约 9.6K 标记，1536³ 分辨率下生成约 60 秒（H100），在效率与质量之间取得了当前最优平衡。

**已知局限**：

- **亚体素混叠**：当几何特征小于单个体素时（如两个极近的平行面），灵活对偶网格可能产生表面平均或模糊伪影，无法精确表示亚体素细节。
- **小孔问题**：解码器在高分辨率稀疏结构中有时无法保证完全封闭的流形表面，当前依赖后处理（如孔洞填充）缓解，但非根本解决方案。
- **语义信息缺失**：O-Voxel 目前仅编码几何和材质属性，未显式包含部件级分割、图拓扑结构或语义标签，限制了其在需要结构化编辑和部件感知应用中的适用性。

### 开放问题

1. **语义扩展**：如何将部件级分割和基于图的拓扑结构纳入 O-Voxel 框架，使其支持更广泛的语义编辑和结构化生成任务？
2. **解码稳定性**：能否通过改进解码过程的拓扑约束，从根本上消除小孔伪影，而非依赖后处理？
3. **极薄结构精度**：在不牺牲紧凑性的前提下，如何提升对毛发、细线等亚体素结构的表示精度？可能的路径包括自适应体素细分或混合表示策略。



## 原文 PDF

![[paperPDFs/arxiv_2025/Native_and_Compact_Structured_Latents_for_3D_Generation.pdf]]
