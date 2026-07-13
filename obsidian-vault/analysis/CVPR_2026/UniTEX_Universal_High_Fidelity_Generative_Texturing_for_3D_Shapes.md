---
title: "UniTEX: Universal High Fidelity Generative Texturing for 3D Shapes"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UniTEX_Universal_High_Fidelity_Generative_Texturing_for_3D_Shapes.pdf
project_link: null
code_link: "https://github.com/YixunLiang/UniTEX"
aliases:
- UniTEX
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 提出 Texture Functions (TF) 将纹理表示为与网格拓扑无关的连续三维体积场，并设计 Large Texturing Model (LTM) 在体积空间中直接回归完整纹理，完全绕过 UV 参数化。
primary_logic: 将纹理从仅定义在表面的信号扩展为覆盖整个三维空间的连续函数（类似 Signed/Unsigned Distance Field），可利用密集的体积监督训练纹理回归模型，从而消除对特定 UV 布局的依赖，大幅提升模型泛化能力和输出纹理的完整与一致性。
claims:
- UV-based 方法在分布外的生成网格上失效，产生碎片化纹理（如 Paint3D 和 TexGEN 所示），直接验证了 UV 拓扑模糊性是核心瓶颈。
- UniTEX 在生成网格上取得 65.91% 的用户偏好率，显著高于 Paint3D 的 6.82% 和其他基线，其纹理更平滑且更贴合几何形状。
- 消融实验证实，相比仅表面监督，纹理函数监督 (TFS) 将 PSNR 从 25.81 提升至 27.01，UV PSNR 从 20.31 提升至 20.99，证明完整体积监督的增益。
- Artist-created Mesh (Table 1) 上 CMMD↓ = 0.826
---

# UniTEX: Universal High Fidelity Generative Texturing for 3D Shapes

> [!tip] 核心洞察
> 将纹理从仅定义在表面的信号扩展为覆盖整个三维空间的连续函数（类似 Signed/Unsigned Distance Field），可利用密集的体积监督训练纹理回归模型，从而消除对特定 UV 布局的依赖，大幅提升模型泛化能力和输出纹理的完整与一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniTEX：面向三维形状的通用高保真生成纹理 |
| 英文题名 | UniTEX: Universal High Fidelity Generative Texturing for 3D Shapes |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2505.23253) · [Code](https://github.com/YixunLiang/UniTEX) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | UniTEX |
| Dataset | Artist-created Mesh, Generative Mesh |

> [!tip] 效果简介
> - Artist-created Mesh (Table 1) 上，CMMD↓ 0.826 vs 1.196 (Paint3D) (↓0.370)；FIDCLIP↓ 16.03 vs 20.52 (Paint3D) (↓4.49)。
> - Generative Mesh (Table 1) 上，User-perf.↑ 65.91% vs 6.82% (Paint3D) (↑59.09%)。

## 概要

### 问题背景

为三维网格生成高质量纹理是计算机图形学与生成式 AI 的核心任务。现有主流方法几乎都依赖 UV 参数化——将三维表面展开为二维纹理图谱，再通过扩散模型进行涂漆或修复。然而，UV 映射存在固有的拓扑模糊性：同一网格的不同 UV 布局会导致截然不同的纹理生成结果。当面对分布外（out-of-distribution）的生成式网格时，这种模糊性被急剧放大——自动 UV 展开会产生大量碎片化、噪声化的 UV 区域，导致基于 UV inpainting 的纹理细化模型输出不完整、碎片化且多视图不一致的纹理（见图 2 中 Paint3D 与 TexGEN 的失效案例）。

### 核心思路

UniTEX 提出了一种根本性的解决路径：**完全绕过 UV 参数化，将纹理建模为与网格拓扑无关的连续三维体积场**。具体而言，该方法引入 **Texture Functions (TFs)**——受无符号距离函数（UDF）启发，将纹理从仅定义在表面的信号扩展为覆盖整个三维空间的连续函数。基于这一表示，UniTEX 设计了一个 **Large Texturing Model (LTM)**，在体积空间中直接从多视图图像和部分纹理化几何体回归完整纹理，从而消除对特定 UV 布局的依赖，大幅提升模型在不同拓扑网格上的泛化能力。

### 方法定位

UniTEX 是一个两阶段三维纹理生成框架。第一阶段利用经 LoRA 微调的扩散 Transformer（基于 Flux）生成六个正交视图的无光照图像；第二阶段通过 LTM 在三维函数空间中回归完整纹理函数，并与投影的部分纹理进行混合，产生最终纹理。与 **Paint3D**（Zeng et al., CVPR 2024）、**TexGEN**（Yu et al., TOG 2024）、**TexPainter**（Zhang et al., SIGGRAPH 2024）等 UV-based 方法以及 **Hunyuan2.0-Paint**（Zhao et al., arXiv 2025）等商业系统相比，UniTEX 在表示层面做出了根本性改变，使其在生成式网格上展现出显著优势。

### 主要结果

在艺术家创建网格上，UniTEX 的 CMMD 指标降至 0.826（Paint3D 为 1.196），FIDCLIP 降至 16.03（Paint3D 为 20.52）。在更具挑战性的生成式网格上，UniTEX 的用户偏好率达到 **65.91%**，远超 Paint3D 的 6.82% 及其他基线方法。消融实验证实，纹理函数监督（TFS）相比仅表面监督，将 PSNR 从 25.81 提升至 27.01，UV PSNR 从 20.31 提升至 20.99，验证了完整体积监督的增益。

### 三维纹理生成的现状与瓶颈

为三维形状生成高质量纹理是计算机图形学与三维内容创作中的核心任务，其应用涵盖游戏、影视、虚拟现实等众多领域。近年来，基于扩散模型的二维图像生成技术取得了突破性进展，推动了三维纹理生成方法的大量涌现。这些方法通常遵循一个两阶段范式：首先生成多视图图像，然后将这些图像“映射”到三维网格表面以形成完整纹理。

然而，现有方法在纹理映射阶段几乎无一例外地依赖于 **UV 参数化**——即将三维表面展开为二维平面图谱。这一依赖构成了当前纹理生成的根本瓶颈：UV 映射存在固有的**拓扑模糊性**。同一个三维形状可以对应无数种不同的 UV 展开方式，而自动 UV 展开算法（如自动展开工具产生的碎片化布局）往往会产生大量不连续的小块区域，这些区域在拓扑上与训练数据中常见的整洁、大块连续 UV 布局截然不同。

### UV 依赖的泛化困境

这种拓扑模糊性直接导致了基于 UV 的纹理细化方法在面对**分布外网格**时泛化能力严重不足。如图 2 所示，以 **Paint3D**（Zeng et al., CVPR 2024）和 **TexGEN**（Yu et al., TOG 2024）为代表的 UV-based 方法，在艺术家手工创建的、具有规整 UV 布局的网格上表现良好；但当面对生成式网格（如扩散模型生成的具有复杂几何的高多边形网格）时，其纹理输出出现严重的碎片化、不完整和多视图不一致问题。根本原因在于这些模型在训练过程中形成了对“干净、大区域 UV 布局”的偏差，难以处理自动展开产生的小而碎片化的 UV 区域。

这一泛化困境在生成式三维内容日益普及的背景下尤为突出——越来越多的网格来自生成模型而非手工建模，其 UV 布局往往是自动计算且不可控的。因此，**摆脱对特定 UV 参数化的依赖**，成为提升纹理生成方法通用性的关键突破口。

### 本文动机与核心思路

针对上述瓶颈，UniTEX 提出了一条根本性的替代路径：**完全绕过 UV 空间，直接在统一的三维函数空间中进行纹理操作**。核心洞察在于：将纹理从仅定义在表面的信号，扩展为覆盖整个三维空间的连续函数——类似于有符号/无符号距离场（SDF/UDF）对几何的表示方式。这种被称为 **Texture Functions (TFs)** 的表示天然与网格拓扑无关，从而从根本上消除了 UV 布局差异带来的泛化障碍。

基于这一表示，UniTEX 设计了一个基于 Transformer 架构的 **Large Texturing Model (LTM)**，在体积空间中直接回归完整纹理，并通过密集的体积监督信号进行训练。这一设计使得模型能够学习到与几何结构内在关联的纹理先验，而非记忆特定的 UV 展开模式，从而在艺术家创建网格和生成式网格上均能输出完整、平滑且贴合几何形状的纹理。

## 核心方法与创新机理

UniTEX 的核心创新在于从**纹理表示空间**和**细化阶段模型**两个维度彻底绕过传统 UV 映射的拓扑模糊性瓶颈，构建了一个对任意拓扑网格具有强泛化能力的通用纹理生成框架。

### 瓶颈根源：UV 映射的拓扑模糊性

现有主流纹理生成方法（如 **Paint3D** (Zeng et al., CVPR 2024)、**TexGEN** (Yu et al., TOG 2024)）依赖 UV 参数化将三维表面展开为二维图谱，再通过 UV inpainting 扩散模型完成纹理细化。这一范式在艺术家手工创建的、具有规整 UV 布局的网格上表现良好，但在面对自动展开的生成式网格时，UV 图谱呈现碎片化、噪声化的拓扑结构，导致扩散模型无法有效推理，产生不完整、多视图不一致的纹理（见 Figure 2）。这一观察直接揭示了 UV 拓扑模糊性是限制纹理生成泛化能力的根本瓶颈。

### 关键机制：纹理函数 (Texture Functions)

为从根本上消除对 UV 布局的依赖，UniTEX 提出了**纹理函数 (Texture Functions, TFs)**——一种将纹理从表面约束信号扩展为覆盖整个三维空间的连续体积场表示。其设计灵感源于无符号距离函数 (UDF)：对于空间中任意查询点，通过查找其最近表面点并赋予对应颜色，将纹理建模为定义在全空间的连续函数。这一表示的核心优势在于：

- **拓扑无关性**：纹理不再绑定于特定 UV 参数化，模型在统一的体积空间中进行推理，天然适配任意拓扑的网格。
- **完整体积监督**：训练时可将表面颜色信息扩展为薄壳区域，提供密集的三维监督信号，引导模型学习更完整的纹理分布。

### 架构实现：大型纹理模型 (Large Texturing Model)

基于纹理函数表示，UniTEX 设计了**大型纹理模型 (Large Texturing Model, LTM)**——一个基于 Transformer 的三维回归模型，替代传统的 UV inpainting 扩散模型作为细化阶段核心。LTM 的工作流程如下：

1. **统一令牌化**：将部分纹理化的几何体与多视图图像统一编码为共享的 triplane-cube 令牌表示。
2. **Transformer 处理**：通过 Transformer 架构提取几何感知特征。
3. **颜色解码**：对于任意查询点 `x`，从 triplane-cube 特征中采样并通过轻量 MLP 解码预测 RGB 颜色：

$$
\hat{\mathbf{c}}(\pmb{x}, \mathcal{TC}) = \mathbf{MLP}_{\theta}\big(gridsample(\pmb{x}, \mathcal{TC})\big)
$$

训练目标为在表面点集 `Ω` 上最小化预测颜色与真实值的 MSE，并辅以总变差正则项：

$$
\mathcal{L}_{\mathrm{texture}} = \mathbb{E}_{{\mathbf{x}}\sim\Omega}\left[\|\hat{\mathbf{c}}({\pmb x}, \mathcal{TC}) - {\mathbf c}({\pmb x})^{*}\|^2\right] + \lambda\mathcal{L}_{tv}(\mathcal{T})
$$

### 训练效率创新：Drop Training 策略

在多视图生成阶段，UniTEX 提出了**Drop Training**策略：每次训练步仅保留部分令牌（如 50%），扩散 Transformer 仅基于所选令牌进行条件生成。这一策略在保持生成质量与全令牌微调相当的前提下，节省 22.5% 显存，训练速度提升 44.5%，显著降低了大规模纹理生成模型的训练成本。

### 消融验证：纹理函数监督的有效性

消融实验直接证实了体积监督的核心增益（Table 4）：相比仅表面点监督，纹理函数监督 (TFS) 将 PSNR 从 25.81 提升至 27.01（+1.20），UV PSNR 从 20.31 提升至 20.99（+0.68），并产生更完整、更高质量的纹理（Figure 9）。这一定量证据表明，将监督信号从表面扩展至体积空间是提升纹理完整性的关键机制。

### 创新总结

UniTEX 通过三个相互耦合的 changed slots 实现了对 UV 范式的系统性替代：

| 创新维度 | 传统方案 | UniTEX 方案 | 核心收益 |
|---------|---------|------------|---------|
| 纹理表示空间 | UV 参数化（二维图谱） | 纹理函数（连续三维体积场） | 拓扑无关，天然泛化 |
| 细化阶段模型 | UV inpainting 扩散模型 | Large Texturing Model (Transformer 回归) | 体积空间直接推理 |
| 训练监督信号 | 仅表面点颜色监督 | 完整体积纹理函数监督 | 更完整的纹理学习 |

UniTEX 采用两阶段纹理生成框架，核心设计动机在于**绕过 UV 参数化固有的拓扑模糊性**——基于 UV inpainting 的方法（如 **Paint3D** (Zeng et al., CVPR 2024)、**TexGEN** (Yu et al., TOG 2024)）在分布外的生成式网格上会产生碎片化、不完整的纹理（见 Figure 2）。UniTEX 通过将纹理建模为连续三维体积场来消除对特定 UV 布局的依赖。

### 流水线概览

整体流水线如 Figure 3 所示，由四个串行模块构成：

![[assets/figures/papers/paper_list_l2619_https_arxiv_org_abs_2505_23253/figures/003_Figure_3.jpg]]
*Figure 3: Overall pipeline of UniTEX. Given a textureless geometry and reference image, UniTEX first generates a high-fidelity multi-view image through 3 steps (RGB generation, delighting, and super-resolution (SR)) using finetuned DiTs (detailed in Sec. 3.2). The texture will be reprojected to a partial textured mesh and sent to the Large Texturing Model (Detailed in Sec. 3.3) with generated images to predict the corresponding complete texture functions (Detailed in Sec. 3.3.2). The final texture is then synthesized by blending the predicted texture functions with the partial textured geometry*

**第一阶段：多视图生成。** 给定无纹理几何体与参考图像，UniTEX 使用经 LoRA 微调的 DiTs（基于 Flux）依次执行三步操作——RGB 生成、去光照（delighting）与可选超分辨率（SR）——生成 6 个正交视图的高保真图像。为降低 DiTs 微调的显存与时间开销，作者提出了 **Drop Training 策略**：每个训练步仅保留部分令牌（如 50%），扩散 Transformer 仅在这些选定令牌上进行条件生成，使显存节省 22.5%、训练速度提升 44.5%，且生成质量与全令牌微调相当（Table 3）。

**第二阶段：投影与混合。** 生成的多视图图像通过反投影与混合操作映射到网格表面，形成**部分纹理化几何体**（partial textured geometry）。这一中间表示同时保留了已填充的纹理区域与待补全的空白区域。

**第三阶段：Large Texturing Model (LTM)。** LTM 是 UniTEX 的核心创新模块（Figure 4），接收两部分输入：六视图生成图像与部分纹理化几何体。其工作流程为：
1. **统一表示**：将图像特征与几何信息融合为共享的 triplane-cube 令牌表示；
2. **Transformer 处理**：基于 Transformer 架构提取几何感知特征；
3. **颜色解码**：通过轻量级 MLP 从 triplane-cube 特征中解码 RGB 颜色，即 $\hat{\mathbf{c}}(\pmb{x}, \mathcal{TC}) = \mathbf{MLP}_{\theta}\big(\mathrm{gridsample}(\pmb{x}, \mathcal{TC})\big)$（Eq. 1）。

LTM 的核心机制是在三维函数空间中直接回归**完整的纹理函数（Texture Functions, TFs）**，而非在 UV 空间进行局部修补。TF 将纹理从仅定义在表面的信号扩展为覆盖整个三维空间的连续体积函数（类似无符号距离函数 UDF 的建模方式，见 Figure 5），使模型能够利用密集的体积监督进行训练。

**第四阶段：纹理合成。** 将 LTM 预测的纹理函数与第二阶段的部分纹理化几何体进行混合，生成最终的完整纹理。

### 关键设计决策的因果链

| 瓶颈 | 因果调节 | 实现机制 |
|------|---------|---------|
| UV 拓扑模糊性导致跨网格泛化失败 | 纹理表示空间从 UV 图谱迁移至连续三维体积场 | Texture Functions (TF) |
| UV inpainting 扩散模型对碎片化 UV 区域失效 | 细化阶段模型从扩散模型替换为体积回归模型 | Large Texturing Model (LTM) |
| DiTs 全参数微调成本高 | 引入 LoRA 高效训练与 Drop Training 策略 | 仅保留部分令牌进行条件生成 |
| 仅表面点监督导致纹理不完整 | 扩展监督信号至表面薄壳区域 | 纹理函数监督 (TFS) |

消融实验证实了上述设计的有效性：纹理函数监督将 PSNR 从 25.81 提升至 27.01，UV PSNR 从 20.31 提升至 20.99（Table 4），并产生更完整、高质量的纹理（Figure 9）。在生成网格上，UniTEX 的用户偏好率达 65.91%，显著高于 Paint3D 的 6.82%（Table 1），验证了绕过 UV 空间的体积回归策略在泛化能力上的决定性优势。

### 纹理函数 (Texture Functions, TF)

UniTEX 的核心创新在于将纹理从仅定义在网格表面的二维信号扩展为覆盖整个三维空间的连续体积函数。这一设计直接绕过了 UV 参数化引入的拓扑模糊性问题——如图 2 所示，基于 UV 的方法（如 **Paint3D** (Zeng et al., CVPR 2024) 和 **TexGEN** (Yu et al., TOG 2024)）在艺术家创建网格上表现良好，但在分布外的生成式网格上因 UV 布局碎片化而产生严重失效。

纹理函数的构建受无符号距离函数 (UDF) 启发：对于空间中任意查询点 $\pmb{x}$，首先找到其在网格表面上的最近点，然后将该最近点的纹理颜色赋予 $\pmb{x}$。由此，纹理被定义为一个从 $\mathbb{R}^3$ 到 RGB 颜色空间的连续映射，使得模型可以在整个三维体积中学习纹理分布，而非局限于表面信号。图 5 展示了纹理函数与 UDF 的可视化对比。

### 大型纹理模型 (Large Texturing Model, LTM)

LTM 是 UniTEX 第二阶段的核心模块，负责在体积空间中直接回归完整纹理。其输入包括第一阶段生成的 6 个正交视图图像以及经投影混合得到的部分纹理化几何体，输出为完整的纹理函数。

#### Triplane-Cube 特征表示

LTM 首先将部分纹理几何体与多视图图像统一到一个共享的 triplane-cube 令牌表示中。triplane-cube 是一种混合三维特征结构，结合了 triplane 的高效性与立方体网格的表达能力，能够在保持计算可行性的同时捕获细粒度几何特征。给定查询点 $\pmb{x}$，通过 `gridsample` 操作从 triplane-cube 特征 $\mathcal{TC}$ 中采样得到特征向量，再经轻量级 MLP 解码为 RGB 颜色：

$$
\hat{\mathbf{c}}(\pmb{x}, \mathcal{TC}) = \mathbf{MLP}_{\theta}\big(\text{gridsample}(\pmb{x}, \mathcal{TC})\big) \tag{1}
$$

其中 $\hat{\mathbf{c}}$ 为预测颜色，$\mathbf{MLP}_{\theta}$ 为可学习解码器。Transformer 架构随后对这些令牌进行全局上下文建模，提取几何感知特征。

#### 纹理函数监督 (Texture Function Supervision, TFS)

训练时，UniTEX 不仅监督表面点颜色，更将监督信号扩展至表面附近的薄壳区域，使模型学习完整的三维纹理函数。训练目标为：

$$
\mathcal{L}_{\mathrm{texture}} = \mathbb{E}_{\mathbf{x} \sim \Omega}\left[\|\hat{\mathbf{c}}(\pmb{x}, \mathcal{TC}) - \mathbf{c}(\pmb{x})^{*}\|^{2}\right] + \lambda \mathcal{L}_{tv}(\mathcal{T}) \tag{2}
$$

其中 $\Omega$ 为采样点集（包含表面点及其薄壳扩展区域），$\mathbf{c}(\pmb{x})^{*}$ 为真实颜色，$\mathcal{L}_{tv}$ 为总变差正则项，用于平滑 triplane-cube 表示 $\mathcal{T}$，$\lambda$ 为平衡系数。

消融实验（表 4）验证了 TFS 的关键作用：相比仅表面监督，TFS 将 PSNR 从 25.81 提升至 27.01，UV PSNR 从 20.31 提升至 20.99，且产生显著更完整、更高质量的纹理（图 9）。

### 多视图生成的 Drop Training 策略

在第一阶段的多视图纹理生成中，UniTEX 对 DiTs (Flux) 进行 LoRA 微调。为降低训练成本，提出 Drop Training 策略：在每个训练步中仅保留部分令牌（如 50%），扩散 Transformer 仅基于这些选中令牌进行条件生成。表 3 显示，该策略在 MV 纹理生成任务中节省 22.5% 显存（69.2GB → 53.6GB），训练速度提升 44.5%（38.76s/it → 21.50s/it），且生成质量与全令牌微调相当。

## 实验与关键发现

### 主结果：纹理质量与泛化性

UniTEX 在两类网格上均展现出显著优势：艺术家创建的规整网格（域内），以及生成模型产出的高面数、碎片化网格（域外）。表 1 汇总了定量对比结果。

**艺术家创建网格。** 在以 Objaverse 子集构建的测试集上，UniTEX 的 CMMD 降至 0.826，较 Paint3D（1.196）下降 30.9%；FIDCLIP 为 16.03，较 Paint3D（20.52）下降 21.9%。CLIPscore 与 LPIPS 同样领先，表明生成纹理与参考图像语义一致性更高，且与真实纹理的感知差异更小。

**生成网格。** 这是 UV-based 方法的系统性失败场景。如图 2 所示，Paint3D 与 TexGEN 在面对碎片化 UV 布局时产生不完整、割裂的纹理。UniTEX 则因完全脱离 UV 空间，在该场景下取得压倒性优势：用户偏好率高达 65.91%，而 Paint3D 仅 6.82%，Hunyuan2.0-Paint 为 9.09%。FIDCLIP（0.826）与 CLIPscore（0.844）亦为最优。定性对比（图 6）进一步显示，UniTEX 的纹理更平滑、完整，且与几何形状贴合更紧密，而商业工具 Meshy 和 Rodin 在复杂网格上同样出现纹理模糊或错位。

### 细化阶段分析

纹理细化是 UV-based 方法的另一薄弱环节。表 2 报告了细化阶段的定量指标。UniTEX 在全部指标上领先：PSNRuv 达 23.01（TexPainter 为 21.25），PSNRuv*（仅不可见区域）达 19.89（TexPainter 为 17.62），PSNR 达 30.45，LPIPS 低至 0.023。图 7 提供了定性证据：当人脸网格的自动 UV 展开产生碎片化布局时，Paint3D 和 TexGEN 在碎片区域（蓝色框）出现纹理断裂；UniTEX 则生成平滑连贯的纹理，且更尊重几何语义（如眼镜、肋骨和徽章区域）。这直接验证了 Texture Functions 绕过 UV 参数化的核心优势。

### 消融实验

**Drop Training 策略。** 表 3 报告了在多视图纹理生成任务上的效率消融。丢弃 50% 令牌后，显存占用从 69.2GB 降至 53.6GB（节省 22.5%），每轮训练时间从 38.76s 降至 21.50s（加速 44.5%），且生成质量与全令牌微调相当。该策略在法线估计任务上同样有效，证明其作为通用高效微调策略的潜力。

**纹理函数监督 (TFS)。** 表 4 对比了仅表面监督与完整体积监督的效果。TFS 将 PSNR 从 25.81 提升至 27.01（+1.20），UV PSNR 从 20.31 提升至 20.99（+0.68），LPIPS 从 0.052 降至 0.045。图 9 的可视化表明，在相同训练迭代下，TFS 训练的模型能生成更完整、更高质量的纹理，而仅表面监督的模型在不可见区域仍存在纹理缺失。这证实了将纹理扩展为连续体积函数并施加密集空间监督的有效性。

### 失败模式与局限性

论文未明确报告失败案例。从方法设计推断，潜在风险包括：纹理函数在远离表面的空间区域可能产生无意义的颜色外推；Large Texturing Model 依赖多视图生成质量，当第一阶段生成图像出现严重多视图不一致时，回归的纹理函数可能继承这些伪影。上述推断需通过进一步实验验证。

![[assets/figures/papers/paper_list_l2619_https_arxiv_org_abs_2505_23253/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison between artist-created and generative mesh on different texturing methods*

![[assets/figures/papers/paper_list_l2619_https_arxiv_org_abs_2505_23253/figures/008_Figure_7.jpg]]
*Figure 7: Qualitative comparison of refinement stage across different methods. In the first case, automatically unwrapping makes fragmented and noisy UV layout on the face. UV-based methods such as Paint3D and TexGen struggle with these (blue boxs). In contrast, our method generates smooth and coherent textures that more respect to geometry (glasses in the first row and the ribcage and emblem in the second row)*

![[assets/figures/papers/paper_list_l2619_https_arxiv_org_abs_2505_23253/figures/014_Figure_9.jpg]]
*Figure 9: Visualization of the effectiveness of Texture Function Supervision (TFS). Under identical training iterations, models trained with TFS yield significantly higher-quality and completed textures compared to those supervised solely on surface signals. (Best viewed when zoomed in)*

![[assets/figures/papers/paper_list_l2619_https_arxiv_org_abs_2505_23253/figures/015_Table_3.jpg]]
*Table 3: Ablation studies of MV texture generation and normal estimation using drop training strategy*

![[assets/figures/papers/paper_list_l2619_https_arxiv_org_abs_2505_23253/figures/016_Table_4.jpg]]
*Table 4: Ablation studies on Texture function*

## 定位与知识库关联

### 纹理生成范式的演进与分化

三维纹理生成方法可按其核心表示空间划分为两大范式：**基于 UV 参数化的二维纹理合成**与**基于三维空间的直接纹理回归**。UniTEX 属于后者，其核心创新在于将纹理从表面受限信号扩展为覆盖整个三维空间的连续函数，从而绕开 UV 映射固有的拓扑模糊性问题。

基于 UV 的方法长期主导该领域，其基本流程为：先将三维网格展开为二维 UV 图谱，再在图像空间完成纹理修复或生成。代表性工作包括 **Paint3D**（Zeng et al., CVPR 2024）和 **TexGEN**（Yu et al., TOG 2024），前者采用双阶段 UV inpainting 策略，后者将扩散模型引入网格纹理生成。这类方法在艺术家创建、具有规整 UV 布局的网格上表现良好，但在面对自动展开产生的碎片化 UV 区域时，训练偏差导致纹理不完整、多视图不一致，尤其在生成式网格等分布外数据上失效明显（Figure 2）。**TexPainter**（Zhang et al., SIGGRAPH 2024）尝试从多视图一致的角度缓解该问题，但本质上仍受限于 UV 参数化框架。商业工具如 **Meshy**、**Rodin** 以及 **Hunyuan2.0-Paint**（Zhao et al., arXiv 2025）也面临类似的泛化瓶颈。

UniTEX 的方法论转折在于提出 **Texture Functions (TFs)**——受无符号距离函数（UDF）启发，将纹理建模为与网格拓扑无关的连续三维体积场。这一表示选择从根本上消除了对特定 UV 布局的依赖，使模型能够在统一的函数空间中进行纹理回归。与之配套的 **Large Texturing Model (LTM)** 采用 Transformer 架构，在 triplane-cube 令牌表示上直接预测完整纹理函数，并通过体积监督（Texture Function Supervision, TFS）实现训练。

### 关键设计选择与基线差异

下表梳理 UniTEX 相对于 UV-based 基线在四个关键设计维度上的差异：

| 设计维度 | UV-based 基线（Paint3D / TexGEN） | UniTEX |
|---------|--------------------------------|--------|
| 纹理表示空间 | UV 参数化（二维图谱） | Texture Functions（连续三维体积场） |
| 细化阶段模型 | 基于 UV inpainting 的扩散模型 | Large Texturing Model（Transformer 三维回归） |
| 多视图适应策略 | 全参数微调 | LoRA + Drop Training（令牌子集训练） |
| 训练监督信号 | 仅表面点颜色监督 | 完整体积纹理函数监督（含表面薄壳区域） |

其中，**Drop Training** 策略是一项具有工程启发的训练优化：在每次训练步中仅保留部分令牌（50% 丢弃率），使多视图纹理生成任务节省 22.5% 显存、训练速度提升 44.5%，同时保持与全令牌微调相当的生成质量（Table 3）。该方法虽非核心理论贡献，但显著降低了大规模纹理模型的训练门槛。

**纹理函数监督（TFS）** 则是方法有效性的关键支撑。相比仅表面监督，TFS 将 PSNR 从 25.81 提升至 27.01，UV PSNR 从 20.31 提升至 20.99，并产生更完整、更高质量的纹理（Table 4, Figure 9）。该消融实验直接验证了体积监督相对于表面监督的增益。

### 适用边界与局限

尽管 UniTEX 在跨网格类型的泛化能力上显著优于 UV-based 方法，论文中未明确报告其计算开销与推理时间。LTM 的 Transformer 架构和体积场采样可能带来较高的推理延迟，这在实时或交互式纹理生成场景中可能构成限制。此外，纹理函数监督依赖于从已有纹理网格中提取体积真值，该方法在缺乏高质量纹理训练数据时的可扩展性尚待验证。

论文未系统讨论 UniTEX 在极端拓扑（如非流形网格、高亏格曲面）或稀疏视图条件下的表现，这些场景下体积场的定义和采样策略可能需要额外适配。多视图生成阶段依赖 DiTs（Flux）的微调，该模块的性能上限可能制约整体纹理质量的天花板。

### 开放问题

1. **体积表示的计算效率**：Texture Functions 的连续体积采样在推理时引入额外计算，如何在保持纹理完整性的同时降低采样密度或压缩表示，是走向实用的关键问题。
2. **纹理编辑与局部控制**：UV 参数化的一个优势是支持直观的二维编辑，UniTEX 的体积表示是否支持类似的局部纹理编辑操作，论文未予讨论。
3. **与生成式几何的联合优化**：当前 UniTEX 假定输入网格固定，未来是否可将纹理函数与几何表示（如 SDF、NeRF）统一建模，实现几何-纹理的端到端生成，值得探索。
4. **训练数据依赖性**：TFS 需要从纹理网格中提取体积监督信号，该方法对训练数据质量和多样性的敏感度尚未量化评估。

## 原文 PDF

![[paperPDFs/CVPR_2026/UniTEX_Universal_High_Fidelity_Generative_Texturing_for_3D_Shapes.pdf]]
