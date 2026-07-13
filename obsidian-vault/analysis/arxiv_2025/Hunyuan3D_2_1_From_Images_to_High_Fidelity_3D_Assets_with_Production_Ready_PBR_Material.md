---
title: Hunyuan3D 2.1 From Images to High-Fidelity 3D Assets with Production-Ready PBR Material
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Hunyuan3D_2_1_From_Images_to_High_Fidelity_3D_Assets_with_Production_Ready_PBR_Material.pdf
project_link: null
code_link: https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1
aliases:
- H21
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将形状生成与纹理合成分离为独立阶段，并在纹理合成中引入多通道PBR材质扩散框架，结合空间对齐多注意力、3D RoPE和光照不变训练，从而显著提升3D资产的质量与实用性。
primary_logic: 通过分阶段生成策略，先利用流匹配扩散模型和变分自编码器生成高保真几何形状，再通过多视角PBR扩散模型及光照不变训练产生物理正确的材质，实现了可独立使用又可集成的生产级3D资产创建。
claims:
- Hunyuan3D-DiT在形状生成的ULIP-T、ULIP-I、Uni3D-T、Uni3D-I四个指标上均超越了所有对比的基线方法。
- Hunyuan3D-Paint在纹理生成的CLIP-FID、CMMD、CLIP-I、LPIPS指标上均取得了最佳性能。
- 分离式架构允许用户仅生成无纹理网格，或独立将纹理应用于自定义资产，极大提高了工业灵活性。
- 形状生成测试集 (750个对象) 上 ULIP-T / ULIP-I / Uni3D-T / Uni3D-I = 0.0774 / 0.1395 / 0.2556 / 0.3213
---

# Hunyuan3D 2.1 From Images to High-Fidelity 3D Assets with Production-Ready PBR Material

> [!tip] 核心洞察
> 通过分阶段生成策略，先利用流匹配扩散模型和变分自编码器生成高保真几何形状，再通过多视角PBR扩散模型及光照不变训练产生物理正确的材质，实现了可独立使用又可集成的生产级3D资产创建。

| 字段 | 内容 |
|------|------|
| 中文题名 | Hunyuan3D 2.1：从图像到高保真3D资产与生产就绪PBR材质 |
| 英文题名 | Hunyuan3D 2.1 From Images to High-Fidelity 3D Assets with Production-Ready PBR Material |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2506.15442) · [Code](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Hunyuan3D 2.1 |
| Dataset |  |

> [!tip] 效果简介
> - 形状生成测试集 (750个对象) 上，ULIP-T / ULIP-I / Uni3D-T / Uni3D-I 0.0774 / 0.1395 / 0.2556 / 0.3213 vs TripoSG 0.0767 / 0.1225 / 0.2506 / 0.3129 (+0.0007 / +0.0170 / +0.0050 / +0.0084)。
> - 纹理生成测试集 上，CLIP-FID / CMMD / CLIP-I / LPIPS 24.78 / 2.191 / 0.9207 / 0.1211 vs 最佳基线（未提供具体数值） (优于所有对比方法)。

## 概要

**核心瓶颈**：现有3D生成模型普遍缺乏生产级的PBR材质生成能力，且形状与纹理生成过程高度耦合，难以灵活适配工业应用场景。

**核心洞察与因果调节变量**：Hunyuan3D 2.1将形状生成与纹理合成分离为独立阶段，通过分阶段生成策略——先利用流匹配扩散模型和变分自编码器生成高保真几何形状，再通过多视角PBR扩散模型及光照不变训练产生物理正确的材质——实现了可独立使用又可集成的生产级3D资产创建。

**方法定位**：Hunyuan3D 2.1属于图像到3D生成的分阶段方法，形状生成采用基于流匹配的Hunyuan3D-DiT配合变分形状自编码器Hunyuan3D-ShapeVAE，纹理生成采用多视角PBR扩散框架Hunyuan3D-Paint，输出albedo、metallic、roughness三通道材质图。其关键创新包括：空间对齐多注意力模块实现材质通道对齐、3D-Aware RoPE保障多视角一致性、以及光照不变训练策略增强材质对环境光的鲁棒性。

**主要结果**：
- 在形状生成的定量评估中，Hunyuan3D-DiT在ULIP-T（0.0774）、ULIP-I（0.1395）、Uni3D-T（0.2556）、Uni3D-I（0.3213）四个指标上均超越了包括**TripoSG**（Li et al., arXiv 2025）、**Michelangelo**（Zhao et al., NeurIPS 2023）、**Craftsman 1.5**（Li et al., arXiv 2024）等在内的所有对比基线方法（Table 1）。
- 在纹理生成评估中，Hunyuan3D-Paint在CLIP-FID（24.78）、CMMD（2.191）、CLIP-I（0.9207）、LPIPS（0.1211）指标上均取得了最佳性能（Table 2）。
- 分离式架构允许用户仅生成无纹理网格，或独立将纹理应用于自定义资产，极大提高了工业灵活性。

3D资产生成在游戏、影视、虚拟现实和工业设计等领域具有广泛的应用需求。近年来，随着扩散模型和大规模多模态学习的快速发展，从单张图像或文本提示生成3D内容取得了显著进展。然而，现有方法在生成质量与工业实用性之间仍存在明显鸿沟，主要体现在以下两个方面。

**形状与纹理的耦合困境。** 当前主流的3D生成管线通常将形状生成与纹理合成紧密耦合在一个统一的框架中，这种一体化设计虽然简化了训练流程，却牺牲了工业场景所需的灵活性。在实际生产中，设计师往往需要独立获取无纹理的高保真网格，或为已有自定义资产赋予新的材质外观。耦合式架构难以同时满足这两种需求，限制了3D生成技术在实际工作流中的落地。

**材质生成的物理真实性缺失。** 绝大多数现有方法仅输出单一的RGB颜色纹理，缺乏对物理渲染（Physically-Based Rendering, PBR）材质的支持。PBR材质通过反照率（albedo）、金属度（metallic）和粗糙度（roughness）等多通道信息描述表面光学属性，是实现生产级渲染的标准范式。缺少PBR材质意味着生成的3D资产无法直接导入游戏引擎或渲染管线，需要大量人工后期处理。此外，现有纹理生成方法对环境光照变化敏感，同一物体在不同光照条件下可能产生不一致的纹理结果，进一步降低了材质生成的鲁棒性。

针对上述瓶颈，Hunyuan3D 2.1提出了一个分阶段的生成框架：将形状生成与纹理合成分离为两个独立模块，分别由基于流匹配的Hunyuan3D-DiT和变分形状自编码器Hunyuan3D-ShapeVAE负责几何建模，由多视角PBR扩散模型Hunyuan3D-Paint负责材质生成。这一解耦设计使得用户既可以端到端地生成带PBR材质的完整3D资产，也可以单独使用形状模块或纹理模块，极大提升了工业灵活性。在纹理阶段，通过空间对齐多注意力机制、3D感知旋转位置编码（3D-Aware RoPE）以及光照不变训练策略，Hunyuan3D-Paint能够生成多视角一致、物理正确的PBR材质，填补了从图像到生产就绪3D资产的关键技术缺口。

## 核心方法与创新机理

Hunyuan3D 2.1 的核心创新在于将3D资产生成解耦为**形状生成**与**PBR材质合成**两个独立阶段，并通过一系列针对性设计解决了传统方法中形状-纹理耦合、材质物理正确性不足、多视角一致性薄弱等瓶颈。

### 1. 分阶段解耦架构

现有3D生成模型通常将形状与纹理生成耦合在单一流程中，导致工业应用灵活性不足——用户无法单独获取无纹理网格，也难以将纹理独立迁移至自定义资产。Hunyuan3D 2.1 将流程明确分离：形状生成阶段输出高保真几何，纹理合成阶段为给定网格生成多通道PBR材质。这种解耦使两个模块既可独立使用，也可串联为完整管线，极大提升了工业适配性（证据来源：Section 1 Introduction）。

### 2. 形状生成：流匹配扩散变换器 + 变分形状自编码器

形状生成模块由 **Hunyuan3D-ShapeVAE** 和 **Hunyuan3D-DiT** 组成，替代了传统扩散模型或重建模型的单一范式。

- **Hunyuan3D-ShapeVAE**：基于3DShape2VecSet的向量集表示，采用变分编码器-解码器Transformer将3D形状压缩为紧凑连续的隐空间令牌。编码过程通过最远点采样在均匀点云和重要性采样点云上生成查询点，解码器则从隐变量重建SDF场。训练损失为SDF重建的均方误差与KL散度正则项的加权和：
  $$\mathcal{L}_r = \mathbb{E}_{x \in \mathbb{R}^3} [\mathrm{MSE}(\mathcal{D}_s(x | Z_s), \mathrm{SDF}(x))] + \gamma \mathcal{L}_{KL}$$
  该设计使隐空间具备良好的连续性和重建精度（证据来源：Section 3.1.1）。

- **Hunyuan3D-DiT**：在ShapeVAE的隐空间上执行流匹配扩散生成，以输入图像为条件生成形状令牌。采用仿射路径与条件最优传输调度：$x_t = (1 - t) \times x_0 + t \times x_1$，目标速度场 $u_t = x_1 - x_0$，训练损失为预测速度场与真实速度场的L2距离：
  $$\mathcal{L} = \mathbb{E}_{t, x_0, x_1} [\| u_{\theta}(x_t, c, t) - u_t \|_2^2]$$
  DiT块架构沿用了Hunyuan-DiT的设计（证据来源：Section 3.1.2, Figure 3）。

### 3. 纹理生成：多视角PBR扩散模型

纹理合成模块 **Hunyuan3D-Paint** 将纹理生成从单一RGB颜色提升为物理正确的PBR材质输出，包含三个关键设计：

- **多通道PBR输出**：基于Disney Principled BRDF模型，同时生成albedo（反照率）、metallic（金属度）、roughness（粗糙度）三通道材质图，使生成的3D资产可直接用于生产级渲染管线（证据来源：Section 3.2）。

- **空间对齐多注意力模块**：为解决多通道材质间的对齐问题，将albedo分支的注意力输出传播至metallic-roughness分支，确保不同材质通道在空间上的一致性（证据来源：Section 3.2）。

- **3D-Aware RoPE**：引入基于3D坐标的多分辨率旋转位置编码，显式注入多视角几何关系，增强跨视角纹理的一致性，弥补了传统方法缺乏显式一致性约束的不足（证据来源：Section 3.2）。

- **光照不变训练策略**：强制同一物体在不同光照条件下生成一致的材质参数，消除环境光变化对纹理预测的干扰，使模型学习到材质的内禀属性而非光照效果（证据来源：Section 3.2）。

### 4. 创新效果验证

定量实验表明上述创新带来了显著的性能提升：

- **形状生成**：在750个对象的测试集上，Hunyuan3D-DiT在ULIP-T（0.0774）、ULIP-I（0.1395）、Uni3D-T（0.2556）、Uni3D-I（0.3213）四个指标上均超越了**Michelangelo**（Zhao et al., NeurIPS 2023）、**Craftsman 1.5**（Li et al., arXiv 2024）、**TripoSG**（Li et al., arXiv 2025）、**Trellis**（Xiang et al., arXiv 2024）等基线方法（证据来源：Table 1）。

- **纹理生成**：Hunyuan3D-Paint在CLIP-FID（24.78）、CMMD（2.191）、CLIP-I（0.9207）、LPIPS（0.1211）上均取得了最优性能（证据来源：Table 2）。

Hunyuan3D 2.1 采用**形状生成与纹理合成分离**的两阶段流水线架构，将单张输入图像转化为具备生产级PBR材质的高保真3D资产。这一设计决策直击现有方法的核心瓶颈：形状与纹理的耦合生成不仅限制了各自的优化空间，更难以适配工业场景中“仅需无纹理网格”或“为自定义资产独立贴图”的灵活需求。

### 流水线总览

整体流程由两个可独立运行又可无缝集成的阶段构成，如Figure 2和Figure 4所示：

1. **形状生成阶段**：输入单张RGB图像，通过**Hunyuan3D-DiT**（流匹配扩散变换器）在**Hunyuan3D-ShapeVAE**（变分形状自编码器）的紧凑连续隐空间中生成形状令牌，再由ShapeVAE解码器重建为高保真3D网格。该阶段输出的是纯净的几何形状，不包含任何纹理信息。

2. **纹理生成阶段**：以第一阶段生成的网格（或任意用户提供的3D资产）为输入，**Hunyuan3D-Paint**多视角PBR扩散模型从多个视点渲染条件图像，生成包含**albedo（反照率）、metallic（金属度）、roughness（粗糙度）**三通道的物理正确PBR材质贴图。

### 数据预处理管线

两个生成阶段共享一套标准化的数据预处理流程（Algorithm 1），确保训练数据的一致性和高质量：

- **归一化与坐标对齐**：将原始3D资产缩放至 $[-1, 1]^3$ 的规范空间，并通过PCA对齐主方向。
- **水密化处理**：对非水密网格，采用广义卷绕数（generalized winding number）判定内外，结合Marching Cubes在零等值面提取水密网格。SDF值通过 $\mathbf{SDF}(\mathbf{q}) = \mathrm{distance\_to\_mesh}(\mathbf{q}) \cdot \mathrm{sign}(\omega(\mathbf{q}))$ 计算。
- **SDF采样**：采用双重采样策略——在表面附近密集采样以捕获细节，在 $[-1, 1]^3$ 空间均匀采样以保持全局结构。
- **表面采样与条件渲染**：从网格表面采样点云，并在多视角、多光照条件下渲染RGB图像和PBR材质通道，为后续的纹理扩散模型提供训练对。

### 模块间数据流与接口

形状生成与纹理生成之间的接口是**标准三角网格**，这一松耦合设计带来了两个关键优势：

- **独立使用**：用户可仅运行形状生成阶段获取无纹理网格，直接用于下游应用（如物理仿真、几何编辑）。
- **灵活组合**：Hunyuan3D-Paint可接受任意来源的3D网格作为输入，为其生成PBR材质，而不仅限于Hunyuan3D-DiT的输出。

### 核心创新在框架层面的体现

分离式架构使得每个阶段可以针对其特定任务进行深度优化，而无需在形状精度与材质真实感之间做出折衷：

- **形状生成阶段**引入流匹配扩散模型，相比传统DDPM具有更高效的采样路径；ShapeVAE的变分隐空间为扩散模型提供了紧凑且连续的生成目标。
- **纹理生成阶段**独立设计多视角PBR扩散框架，并引入**空间对齐多注意力模块**（将albedo分支的注意力输出传播至metallic-roughness分支，确保材质通道间的空间一致性）、**3D-Aware RoPE**（基于3D坐标的多分辨率旋转位置编码，强化多视角一致性）以及**光照不变训练策略**（强制同一物体在不同光照下生成一致的材质参数），这些创新在耦合式框架中难以有效实现。

Figure 1展示了该框架生成的完整3D资产效果，验证了分离式设计在视觉质量和工业实用性上的显著提升。

![[assets/figures/papers/Hunyuan3D_2.1_From_Images_to_High-Fidelity_3D_Assets_with_Production-Ready_PBR_M_f6142fe646f9/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline for shape generation. Given a single image input, combining Hunyuan3D-DiT and Hunyuan3D-VAE can generate a high-quality and high-fidelity 3D shape*

![[assets/figures/papers/Hunyuan3D_2.1_From_Images_to_High-Fidelity_3D_Assets_with_Production-Ready_PBR_M_f6142fe646f9/figures/003_Figure_3.jpg]]
*Figure 3: Overview of DiT block. We adopt the DiT implemented by Hunyuan-DiT [4] in our pipeline*

![[assets/figures/papers/Hunyuan3D_2.1_From_Images_to_High-Fidelity_3D_Assets_with_Production-Ready_PBR_M_f6142fe646f9/figures/004_Figure_4.jpg]]
*Figure 4: Overview of material generation framework*

Hunyuan3D 2.1 的核心架构由四个关键模块串联构成，分别负责几何压缩、形状生成、材质合成与多通道对齐，形成从单张图像到生产级 PBR 资产的完整管线。

### 数据预处理管线

在进入生成模型之前，所有 3D 训练数据需经过标准化处理，流程如 Algorithm 1 所示，包含归一化、水密化、SDF 采样、表面采样与条件渲染五个步骤。其中水密化是关键环节：对于非水密网格，首先计算广义卷绕数 $\omega(\mathbf{q})$ 作为内部/外部判定依据（$\omega \approx 1$ 表示内部，$\omega \approx 0$ 表示外部），然后通过以下公式计算符号距离函数：

$$
\mathbf{SDF}(\mathbf{q}) = \underbrace{\mathrm{distance\_to\_mesh}(\mathbf{q}, V, F)}_{\mathrm{nearest\ surface\ distance}} \cdot \underbrace{\mathrm{sign}(\omega(\mathbf{q}))}_{\mathrm{inside/outside\ sign}}
$$

最终使用 Marching Cubes 在零水平等值面提取水密网格。SDF 采样采用双重策略：一部分查询点靠近表面以捕获细节，另一部分在 $[-1,1]^3$ 空间内均匀分布以保持整体结构。

### Hunyuan3D-ShapeVAE（变分形状自编码器）

该模块将 3D 形状压缩为紧凑的连续隐空间表示，采用基于 3DShape2VecSet 的变分编码器-解码器 Transformer 架构。编码过程首先对均匀采样点云 $P_u$ 和重要性采样点云 $P_i$ 分别应用最远点采样（Farthest Point Sampling），生成查询点集 $Q_u$ 和 $Q_i$，随后通过交叉注意力将几何信息聚合为隐变量 $Z_s$。训练损失由 SDF 重建误差与 KL 散度正则项构成：

$$
\mathcal{L}_r = \mathbb{E}_{x \in \mathbb{R}^3} [\mathrm{MSE}(\mathcal{D}_s(x | Z_s), \mathrm{SDF}(x))] + \gamma \mathcal{L}_{KL}
$$

其中 $\mathcal{D}_s(x | Z_s)$ 为解码器在查询点 $x$ 处预测的 SDF 值，$\gamma$ 控制正则化强度。

### Hunyuan3D-DiT（流匹配扩散变换器）

在 ShapeVAE 的隐空间上，Hunyuan3D-DiT 执行条件流匹配以从输入图像生成形状令牌。该模块采用 Hunyuan-DiT 的 DiT Block 架构（Figure 3），使用仿射路径构建概率流：

$$
x_t = (1 - t) \times x_0 + t \times x_1, \quad u_t = x_1 - x_0
$$

其中 $x_0$ 为噪声，$x_1$ 为目标隐变量，$u_t$ 为真实速度场。模型通过最小化预测速度场 $u_{\theta}(x_t, c, t)$ 与真实速度场的 L2 距离进行训练：

$$
\mathcal{L} = \mathbb{E}_{t, x_0, x_1} [ \| u_{\theta}(x_t, c, t) - u_t \|_2^2 ]
$$

其中 $c$ 为图像条件，$t$ 为时间步。该模块与 ShapeVAE 解耦，允许用户仅生成无纹理网格。

### Hunyuan3D-Paint（多视角 PBR 扩散模型）

该模块为给定网格生成多通道、多视角一致的 PBR 材质纹理，基于 Disney Principled BRDF 模型，同时输出 albedo、metallic 和 roughness 三个通道。其架构（Figure 4）包含两个关键设计：

- **空间对齐多注意力模块**：将 albedo 分支的注意力输出传播至 metallic-roughness 分支，确保材质通道间的空间一致性。
- **3D-Aware RoPE**：基于 3D 坐标的多分辨率旋转位置编码，为多视角渲染提供显式的几何一致性约束。

此外，采用**光照不变训练策略**，强制同一物体在不同光照条件下生成一致的材质参数，消除环境光对纹理预测的干扰。

## 实验与关键发现

### 形状生成主结果

Hunyuan3D-DiT 在包含 750 个对象的形状生成测试集上，于 ULIP-T、ULIP-I、Uni3D-T、Uni3D-I 四项指标上均取得了最优性能（Table 1）。具体而言，其 ULIP-T 达到 0.0774，ULIP-I 达到 0.1395，Uni3D-T 达到 0.2556，Uni3D-I 达到 0.3213。相较于最强基线 **TripoSG**（Li et al., arXiv 2025）的 0.0767 / 0.1225 / 0.2506 / 0.3129，Hunyuan3D-DiT 在 ULIP-I 上取得了 +0.0170 的显著提升，在 Uni3D-I 上取得了 +0.0084 的提升，表明其生成的几何形状在语义一致性和实例级对齐方面具有明显优势。与 **Michelangelo**（Zhao et al., NeurIPS 2023）、**Craftsman 1.5**（Li et al., arXiv 2024）、**Step1X-3D**（Li et al., arXiv 2025）、**Trellis**（Xiang et al., arXiv 2024）和 **Direct3D-S2**（Wu et al., arXiv 2025）等基线方法相比，Hunyuan3D-DiT 在所有四项指标上均实现了全面超越。

![[assets/figures/papers/Hunyuan3D_2.1_From_Images_to_High-Fidelity_3D_Assets_with_Production-Ready_PBR_M_f6142fe646f9/figures/005_Table_1.jpg]]
*Table 1: The quantitative comparison for shape generation. The Hunyuan3D-DiT presents the best performance*

定性对比（Figure 5）进一步印证了这一结论：Hunyuan3D-DiT 生成的形状在细节保真度和与输入图像的结构一致性上明显优于其他方法，基线方法在复杂几何区域（如纤细结构、曲面过渡）常出现拓扑错误或细节丢失，而 Hunyuan3D-DiT 保持了更完整的水密网格和更准确的轮廓还原。

### 纹理生成主结果

Hunyuan3D-Paint 在纹理生成任务上同样取得了最佳性能（Table 2）。其 CLIP-FID 为 24.78，CMMD 为 2.191，CLIP-I 为 0.9207，LPIPS 为 0.1211，在所有指标上均优于对比方法。CLIP-I 超过 0.92 表明生成的纹理与输入参考图像在语义层面高度对齐，而 LPIPS 仅为 0.1211 则说明感知层面的纹理差异极小。

![[assets/figures/papers/Hunyuan3D_2.1_From_Images_to_High-Fidelity_3D_Assets_with_Production-Ready_PBR_M_f6142fe646f9/figures/008_Figure_6.jpg]]
*Figure 6: The qualitative comparisons for texture synthesis. Table 2: The quantitative comparison for texture generation. Hunyuan3D-Paint achieves the best performance*

定性对比（Figure 6）显示，Hunyuan3D-Paint 生成的多通道 PBR 材质（albedo、metallic、roughness）在不同光照条件下表现出一致且物理正确的材质属性，而基线方法常出现颜色偏移、金属度与粗糙度通道不匹配、或光照变化导致纹理失真等问题。Figure 7 的综合图像到 3D 生成定性对比进一步表明，Hunyuan3D 2.1 的分离式架构在最终资产质量上具有整体性优势。

### 消融实验

本部分需要手动验证。当前分析的实验证据中未提取到消融实验的具体结果。根据方法设计，关键的消融维度应包含：形状生成中流匹配扩散模型与变分自编码器的贡献分离、纹理生成中 3D-Aware RoPE 对多视角一致性的影响、空间对齐多注意力模块对材质通道对齐的作用、以及光照不变训练策略对材质鲁棒性的提升效果。建议查阅原文 Section 4 的消融研究部分以获取定量数据。

### 失败模式与局限

当前分析的实验证据中未提取到明确的失败模式讨论。根据方法架构可推断的潜在局限包括：分离式架构虽然提高了灵活性，但形状与纹理的独立生成可能导致全局风格不一致的风险；PBR 材质生成依赖于训练数据的材质标注质量，对于复杂材质（如半透明、次表面散射）可能无法准确建模；多视角一致性虽通过 3D-Aware RoPE 得到增强，但在遮挡严重或极端视角下仍可能出现纹理撕裂。以上推断需结合原文的实验分析或附录进行验证。

## 定位与知识库关联

### 两阶段解耦范式的定位

Hunyuan3D 2.1 的核心架构决策是将形状生成与纹理合成分离为两个独立阶段。这一设计与当前主流的端到端单阶段生成范式（如 Trellis、Direct3D-S2 等直接输出带纹理3D资产的方法）形成鲜明对比。分离式架构的直接收益在于：用户可独立使用形状生成模块获取无纹理的高保真网格，也可将纹理生成模块应用于任意自定义资产，从而适配工业管线中“几何建模→材质赋予→光照渲染”的标准流程。

该范式在知识谱系上可追溯至两股技术脉络：
- **形状生成侧**：继承自 Michelangelo (Zhao et al., NeurIPS 2023) 和 Craftsman 1.5 (Li et al., arXiv 2024) 等图像到形状重建模型的技术路径，但将骨干网络替换为基于流匹配的扩散变换器（Hunyuan3D-DiT），并结合变分形状自编码器（Hunyuan3D-ShapeVAE）实现连续隐空间中的几何生成。
- **纹理生成侧**：从传统单通道RGB纹理生成跃迁至多通道PBR材质生成，输出 albedo、metallic、roughness 三通道，直接对接 Disney Principled BRDF 渲染管线。这一能力在现有开源3D生成模型中尚属稀缺。

### 关键技术创新与基线对比

以下从五个关键技术槽位分析 Hunyuan3D 2.1 相对于基线方法的改进：

| 技术槽位 | 基线方法特征 | Hunyuan3D 2.1 方案 | 改进性质 |
|---------|-------------|-------------------|---------|
| 形状生成模型 | 传统扩散或重建模型（如 Michelangelo 的 Transformer 解码器） | 流匹配扩散变换器 + 变分形状VAE | 架构替换：流匹配提供更稳定的训练动力学和更快的推理收敛 |
| 纹理生成 | 单一RGB颜色纹理 | 多视角PBR材质生成（albedo/metallic/roughness三通道） | 能力跃迁：从“外观生成”到“物理材质生成” |
| 多视角一致性 | 缺乏显式约束，依赖隐式学习 | 3D-Aware RoPE（基于3D坐标的多分辨率旋转位置编码） | 机制创新：将3D空间先验注入注意力位置编码 |
| 材质通道对齐 | 无 | 空间对齐多注意力模块：albedo注意力输出传播至metallic-roughness分支 | 机制创新：显式建模材质通道间的空间一致性 |
| 训练光照鲁棒性 | 纹理对环境光变化敏感 | 光照不变训练策略：同一物体在不同光照下强制生成一致材质 | 训练策略创新：解耦光照与材质的学习 |

**形状生成对比**：在 Table 1 的定量评估中，Hunyuan3D-DiT 在 ULIP-T (0.0774)、ULIP-I (0.1395)、Uni3D-T (0.2556)、Uni3D-I (0.3213) 四项指标上均超越了包括 TripoSG (Li et al., arXiv 2025)、Step1X-3D (Li et al., arXiv 2025)、Trellis (Xiang et al., arXiv 2024)、Direct3D-S2 (Wu et al., arXiv 2025) 在内的所有对比基线。其中 ULIP-I 指标领先 TripoSG 达 0.0170，表明语义一致性优势明显。

**纹理生成对比**：Table 2 显示 Hunyuan3D-Paint 在 CLIP-FID (24.78)、CMMD (2.191)、CLIP-I (0.9207)、LPIPS (0.1211) 上均取得最优。需要指出的是，原文未提供各基线的具体数值，仅声明“优于所有对比方法”，因此各项优势的统计显著性需结合原始数据进一步验证。

### 适用边界与局限

分离式架构在带来工业灵活性的同时，也引入了若干适用边界：

1. **两阶段信息损失**：形状生成阶段不感知纹理需求，纹理生成阶段仅以固定网格为条件。这意味着几何细节（如微小凹凸）无法与材质（如法线贴图）协同优化，可能导致“完美几何+贴图材质”的视觉割裂感。原文未对此进行消融分析。

2. **PBR材质的数据依赖**：光照不变训练策略要求同一物体在多光照条件下的渲染数据，这对训练数据的采集和合成提出了更高要求。原文未详细披露PBR训练数据的规模与来源，该策略的泛化边界尚不明确。

3. **形状VAE的表示能力**：Hunyuan3D-ShapeVAE 将3D形状压缩为连续隐空间令牌，其重建精度直接构成形状生成的上限。虽然原文给出了VAE的训练损失公式（MSE重建损失 + KL正则项），但未报告VAE的重建精度指标（如Chamfer Distance或IoU），该模块的实际保真度需查阅补充材料。

### 开放问题

- **端到端联合优化的可能性**：当前分离式设计牺牲了形状与纹理的协同优化空间。是否存在轻量级的跨阶段反馈机制（如纹理生成阶段反向传播梯度至形状隐变量），在不破坏模块独立性的前提下提升整体一致性？这是一个值得探索的方向。
- **动态场景与重光照**：PBR材质的核心价值在于支持任意光照条件下的真实感渲染。原文未展示生成资产在新光照环境下的渲染效果，也未评估材质参数在重光照任务中的物理准确性。
- **与3D原生基础模型的整合**：Hunyuan3D-DiT 采用了 Hunyuan-DiT 的 DiT 块设计（Figure 3），这暗示其与2D基础模型存在架构同源性。未来是否可将3D形状生成纳入多模态基础模型的统一框架，实现文本/图像/3D的联合理解与生成，是更宏观的开放问题。

## 原文 PDF

![[paperPDFs/arxiv_2025/Hunyuan3D_2_1_From_Images_to_High_Fidelity_3D_Assets_with_Production_Ready_PBR_Material.pdf]]
