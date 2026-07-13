---
title: "EVA01: Unified Native 3D Understanding and Generation via Mixture-of-Transformers"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: "paperPDFs/arxiv_2026/EVA01:_Unified_Native_3D_Understanding_and_Generation_via_Mixture-of-Transformers.pdf"
project_link: https://www.seeles.ai/research/pages/EVA01
code_link: null
aliases:
- EVA01
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用Mixture-of-Transformers架构将模型解耦为理解专家(E_und)与生成专家(E_gen)，通过共享全局注意力及hard modality routing实现跨模态知识迁移，同时使用结构化的稀疏网格潜在表示替代无序的VecSet，并引入3D Interleaved MRoPE注入空间结构偏置。
primary_logic: 通过解耦专家设计、五阶段课程学习（包含对齐预热、图像温启动、模态丢弃和双向监督）以及有状态序列建模，能够将预训练MLLM的语义先验高效迁移到3D域，使文本、图像和3D网格在统一序列中协同，实现原生理解与身份保持的上下文感知编辑。
claims:
- 在Toys4K文本到3D任务上，EVA01获得用户偏好70.4%，是对最优基线TRELLIS(14.8%)的近5倍。
- 在多轮3D编辑评估中，EVA01以93.75%的用户偏好压倒性超过VoxHammer(3.75%)和TRELLIS(2.50%)，实现了无掩码的身份保持编辑。
- 采用结构化稀疏网格表征的生成损失远低于VecSet，后者在统一序列设置下无法产生可用的几何形状。
- 图像温启动相比纯文本训练显著提升生成收敛速度和最终得分，且增加mesh-understanding数据进一步带来增益。
---

# EVA01: Unified Native 3D Understanding and Generation via Mixture-of-Transformers

> [!tip] 核心洞察
> 通过解耦专家设计、五阶段课程学习（包含对齐预热、图像温启动、模态丢弃和双向监督）以及有状态序列建模，能够将预训练MLLM的语义先验高效迁移到3D域，使文本、图像和3D网格在统一序列中协同，实现原生理解与身份保持的上下文感知编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | EVA01：基于混合专家Transformer的统一原生3D理解与生成 |
| 英文题名 | EVA01: Unified Native 3D Understanding and Generation via Mixture-of-Transformers |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2605.16745) · [Project](https://www.seeles.ai/research/pages/EVA01) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | EVA01 |
| Dataset | Toys4K, Multi-Turn Editing, PointLLM-200 captioning |

> [!tip] 效果简介
> - Toys4K (text-to-3D) 上，User Preference (%) 70.4 vs 14.8 (TRELLIS) (+55.6)；FDDINOv2 122.48 vs 310.55 (ShapeLLM-Omni) (-188.07)；KDDINOv2 1.18 vs 18.20 (ShapeLLM-Omni) (-17.02)。
> - Multi-Turn Editing (custom benchmark) 上，User Preference (%) 93.75 vs 3.75 (VoxHammer) / 2.50 (TRELLIS) (+90.0 / +91.25)。
> - PointLLM-200 captioning 上，GPT-img (render-grounded judge) 65.91 (EVA01-Final) vs 56.05 (GT caption) (+9.86)。

## 概要

现有3D生成方法将语义理解与几何重建解耦，无法将3D网格作为原生模态融入多模态大语言模型（MLLM）的序列流，缺乏语义先验与几何流形的系统对齐，且均为无状态重建，难以在多轮编辑中保持几何身份一致性。

EVA01针对这一瓶颈提出了一套统一框架。其核心洞察在于：通过**Mixture-of-Transformers（MoT）架构**将模型解耦为理解专家（E_und）与生成专家（E_gen），以共享全局注意力及硬模态路由实现跨模态知识迁移；同时采用**结构化的稀疏网格潜在表示**替代无序的VecSet，并引入**3D Interleaved MRoPE**注入空间结构偏置。配合五阶段课程学习策略，该设计能够将预训练MLLM的语义先验高效迁移到3D域，使文本、图像和3D网格在统一序列中协同，实现原生理解与身份保持的上下文感知编辑。

实验证据支撑了这一方案的有效性：

- **文本到3D生成**：在Toys4K基准上，EVA01的用户偏好率达70.4%，是对最优基线**TRELLIS**（14.8%）的近5倍；FDDINOv2指标（122.48）相比**ShapeLLM-Omni**（310.55）大幅降低。
- **多轮3D编辑**：EVA01以93.75%的用户偏好压倒性超过**VoxHammer**（3.75%）和**TRELLIS**（2.50%），实现了无需显式掩码的身份保持编辑。
- **网格理解**：在PointLLM-200字幕任务上，EVA01-Final的GPT-img评分（65.91）显著超越Ground Truth字幕（56.05）。
- **消融验证**：结构化稀疏网格表征的生成损失远低于VecSet（后者在统一序列设置下完全失败）；图像温启动相比纯文本训练显著提升收敛速度和最终得分。

EVA01当前仍存在对分布外组合泛化有限、单视图输入下薄结构细节丢失等局限，但其在统一原生3D理解与生成方面的突破，为构建真正的3D原生多模态基础模型提供了清晰的架构范式和训练路线。

### 3D内容生成的范式瓶颈

3D内容生成在游戏、影视、虚拟现实和具身智能等领域具有广泛需求，但现有方法面临一个根本性瓶颈：**语义理解与几何重建的系统性解耦**。当前主流方案将3D生成视为独立于多模态大语言模型（MLLM）的外部过程——文本或图像条件先被编码为语义特征，再交由专门的扩散模型或重建网络生成几何。这种架构设计导致三个关键缺陷：

1. **3D网格无法作为原生模态融入MLLM序列流**。文本和图像token可以在统一的Transformer序列中被自由处理，但3D几何表示（网格、点云、体素）始终是“二等公民”，需要额外的编码器桥接和独立解码，无法享受MLLM预训练带来的语义先验迁移。
2. **缺乏语义先验与几何流形的系统对齐机制**。预训练MLLM中蕴含的丰富语义知识（物体部件关系、材质属性、空间常识）无法直接指导几何生成过程，导致生成的3D资产在语义一致性、部件完整性和材质合理性上存在系统性缺陷。
3. **无状态重建，无法保持多轮编辑中的几何身份一致性**。现有编辑方法（如**VoxHammer**，Li et al., 2025a）每次编辑独立进行，缺乏对历史几何状态的记忆，导致多轮编辑后物体身份漂移、未编辑区域变形。

### 现有统一方法的尝试与不足

近期工作开始探索将3D理解与生成统一到单一框架中。**ShapeLLM-Omni**（Ye et al., 2025b）是代表性尝试，它采用统一backbone处理所有模态，试图在同一个Transformer中同时完成3D理解和生成。然而，这种“一刀切”的设计面临优化冲突：理解任务需要保留预训练MLLM的语义判别能力，而生成任务则需要学习从噪声到几何的连续映射，两者对参数空间的要求存在内在张力。在Toys4K文本到3D基准上，ShapeLLM-Omni的FDDINOv2距离达到310.55，远高于专用生成方法的水平，反映出统一backbone在生成质量上的妥协。

### 表征选择的深层困境

3D数据的表征形式是另一个关键战场。现有方法普遍采用**无序VecSet潜在token**（如3DShape2VecSet，Zhang et al., SIGGRAPH 2023）或VQ-VAE离散token。VecSet将3D形状编码为一组无序的特征向量，虽然灵活，但丢弃了三维空间的结构先验。消融实验表明，在统一序列设置下，VecSet表示的生成损失迅速平台化，无法产生可用的几何形状——这揭示了无序表征在需要精确空间推理的生成任务中的根本局限。

### EVA01的动机：原生3D多模态的统一路径

上述分析指向一个核心命题：**能否设计一种架构，使3D网格真正成为MLLM序列中的一等公民，在统一的注意力机制下实现理解、生成和上下文感知编辑的协同？**

EVA01的动机由此展开：通过**混合专家Transformer（Mixture-of-Transformers）**将模型解耦为理解专家（$E_{\text{und}}$）和生成专家（$E_{\text{gen}}$），前者作为稳定的语义锚点继承预训练MLLM的多模态先验，后者专注于几何合成，两者通过共享全局注意力和硬模态路由实现跨模态知识迁移。同时，采用**结构化的稀疏网格潜在表示**（O-Voxel）替代无序VecSet，每个token绑定到固定的三维坐标，联合编码几何与材质信息，并引入**3D交错MRoPE**注入欧氏空间结构偏置。配合五阶段课程学习策略，EVA01旨在将预训练MLLM的语义先验高效迁移到3D域，使文本、图像和3D网格在统一序列中协同，实现原生理解与身份保持的上下文感知编辑。

## 核心方法与创新机理

EVA01的核心创新在于将3D网格作为原生模态融入多模态大语言模型（MLLM）的序列流，通过**混合专家Transformer（Mixture-of-Transformers, MoT）架构**、**结构化稀疏网格潜在表示**和**五阶段课程学习**三大设计，系统性地解决了现有方法中语义理解与几何生成解耦、缺乏身份保持编辑能力的瓶颈。

### 1. 混合专家Transformer架构：解耦语义与几何

现有统一3D MLLM（如**ShapeLLM-Omni**, Ye et al., 2025b）采用单一backbone处理所有模态，导致语义理解与几何合成的优化目标相互冲突。EVA01将模型解耦为两个结构镜像的专家模块（Figure 2）：

- **理解专家（E_und）**：继承预训练MLLM（Qwen3-VL）的语义先验，作为稳定的语义锚点，处理文本（Qwen tokenizer）、图像（SigLIP2）和网格（Point-BERT）的编码。
- **生成专家（E_gen）**：专责几何合成，通过三阶段流匹配（稀疏结构→稀疏几何→稀疏材质）生成结构化网格潜在token。

两个专家通过**共享全局注意力（Shared Global Attention）**实现跨模态知识迁移。具体而言，E_gen通过统一的注意力机制查询E_und的语义token，结合**硬模态路由（hard modality routing）**按模态索引$m_i$选择不同的投影权重矩阵：

$$\mathbf{h}_i' = \mathbf{h}_i \mathbf{W}^{(m_i)}$$

$$\mathbf{q}_i, \mathbf{k}_i, \mathbf{v}_i = \mathbf{h}_i \mathbf{W}_Q^{(m_i)}, \mathbf{h}_i \mathbf{W}_K^{(m_i)}, \mathbf{h}_i \mathbf{W}_V^{(m_i)}$$

$$\mathbf{y}_i = \mathsf{Attn}(\mathbf{q}_i, \mathbf{K}, \mathbf{V}; \mathbf{M}) \mathbf{W}_O^{(m_i)}$$

其中统一掩码$\mathbf{M}$（Table 1）精确控制多轮编辑序列中的信息流——当前生成步仅可见干净的历史几何，噪声块对所有后续块不可见。这种设计使得语义条件能够高效注入几何生成，同时保持各专家的优化独立性。

### 2. 结构化稀疏网格潜在表示：替代无序VecSet

现有3D生成框架普遍采用**3DShape2VecSet**（Zhang et al., SIGGRAPH 2023）的无序潜在token集合，这种表示在统一序列设置下完全失败——消融实验显示，VecSet的生成损失迅速平台化，归一化得分远低于网格稀疏潜在表示（Figure 10 right）。

EVA01采用**结构化稀疏网格潜在token（O-Voxel）**，每个token绑定到固定的三维坐标，联合编码几何与材质：

$$\pmb { f } = \{ ( \pmb { f } _ { i } ^ { \mathrm { s h a p e } } , \pmb { f } _ { i } ^ { \mathrm { m a t } } , \pmb { p } _ { i } ) \} _ { i = 1 } ^ { L }$$

其中$\pmb{f}_i^{\mathrm{shape}}$编码局部几何特征，$\pmb{f}_i^{\mathrm{mat}}$编码PBR材质参数，$\pmb{p}_i$为活性体素坐标。预训练的稀疏体素VAE（O-Voxel）支持双向mesh↔latent转换，使网格成为序列流中的一等公民。

为进一步注入空间结构偏置，EVA01引入**3D交错MRoPE**，将Qwen3-VL原有的(T, W, H)旋转位置编码重新用于稀疏网格坐标(x, y, z)：

$$\mathsf{RoPE}(\mathbf{x}, \mathbf{p}) = \mathsf{Interleave}\left(\mathcal{R}_x(\mathbf{x}_{\mathcal{T}_x}), \mathcal{R}_y(\mathbf{x}_{\mathcal{T}_y}), \mathcal{R}_z(\mathbf{x}_{\mathcal{T}_z})\right)$$

该设计将欧氏几何偏置均匀分布于稀疏网格，有效防止长上下文编辑中的几何漂移。

### 3. 五阶段课程学习：渐进式语义-几何对齐

EVA01的训练策略从单阶段微调升级为五阶段课程学习（Table 2），核心机制包括：

- **对齐预热（Alignment Warm-up）**：消融实验表明，直接指令微调导致网格理解性能饱和，而10K步对齐预热后再微调可获得更优的字幕得分（Figure 10 left）。值得注意的是，使用生成侧的稀疏VAE潜在token进行语言对齐（Sparse Shape-to-Text）效果极差——交叉熵损失在高值处停滞，描述语义不可靠，说明理解与生成需要不同的3D表示空间。
- **图像温启动（Image Warm-up）**：纯文本训练收敛更慢且最终得分更低；图像温启动显著加速收敛，增加网格理解监督进一步带来增益（Figure 10 right）。
- **模态丢弃（Modality Dropout）**：在Stage 3中随机丢弃图像或文本模态，防止生成专家在弱文本条件下忽略文本语义，确保指令遵循能力。

### 4. 有状态序列建模：实现身份保持的多轮编辑

EVA01将多轮编辑建模为有状态的条件流匹配问题，第$k$步生成的条件包含当前指令token和历史网格状态：

$$\mathbf{c}_k = \{ \mathbf{t}_{\mathsf{inst}}, \mathbf{x}_{\mathsf{hist}} \}$$

结合Table 1的块注意力掩码，模型始终以干净的历史几何为条件，无需显式分割掩码即可实现身份保持的上下文感知编辑。这一设计使得EVA01在多轮编辑评估中以93.75%的用户偏好压倒性超过**VoxHammer**（Li et al., 2025a）的3.75%和**TRELLIS**（Xiang et al., 2024）的2.50%（Table 5）。

> **需要人工核实**：MoE架构中理解专家与生成专家的参数规模比例、共享注意力层的具体数量等实现细节需查阅原文确认。

EVA01 是一个统一的原生 3D 理解与生成多模态大语言模型（MLLM），其核心设计目标是将文本、图像和 3D 网格作为**一等公民**融入单一序列流，在连续上下文中同时支持网格理解、文本/图像条件生成以及上下文感知的多轮编辑。为此，EVA01 从三个层面重构了模型架构：**混合专家（Mixture-of-Transformers, MoT）骨干网络**、**结构化稀疏网格潜在表示**，以及**五阶段课程学习策略**。

### 架构总览

EVA01 以预训练的 **Qwen3-VL** 作为语义基座，将其扩展为双专家结构（Figure 2）：

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_16745/figures/002_Figure_2.jpg]]
*Figure 2: The Architecture of EVA01. EVA01 organizes tokenized text, image, and mesh inputs within a unified Mixture-of-Transformers backbone. The Understanding Expert*

- **理解专家（E_und）**：冻结或部分微调的语义锚点，继承预训练 MLLM 的多模态先验。它通过 Qwen tokenizer 处理文本、通过 SigLIP2 编码图像、通过 Point-BERT 编码网格表面点云，并融合 DeepStack 视觉特征，为整个系统提供稳定的语义表征。
- **生成专家（E_gen）**：与 E_und 结构镜像对称的几何合成模块，仅处理网格 token。它接收历史条件的稀疏网格潜在表示，在条件流匹配（Conditional Flow Matching）框架下，通过**结构→形状→材质**三阶段逐步生成结构化 3D 潜在 token。

两个专家之间通过**共享全局注意力（Shared Global Attention）**实现跨模态知识迁移：E_gen 在每一层通过统一的注意力机制查询 E_und 的语义 token，而信息流由精心设计的统一注意力掩码（Table 1）严格控制——文本和图像 token 对生成侧可见，但生成侧的噪声潜在对理解侧不可见。

### 输入输出流

EVA01 的输入输出流围绕统一序列组织，支持多种模态组合：

| 任务模式 | 输入序列 | 输出序列 |
|---------|---------|---------|
| 网格理解 | `[text_prompt] [mesh_tokens]` | 自回归生成的文本描述 |
| 文本到 3D | `[text_prompt] [sparse_structure] [sparse_shape] [sparse_material]` | 条件流匹配生成的网格潜在 |
| 图像到 3D | `[text_prompt] [image_tokens] [sparse_structure] [sparse_shape] [sparse_material]` | 条件流匹配生成的网格潜在 |
| 多轮编辑 | `[turn1_inst] [mesh_hist1] [turn2_inst] [mesh_hist2] ... [current_inst] [noisy_latents]` | 保持身份一致性的编辑后网格 |

其中，网格 token 采用**稀疏体素 VAE（O-Voxel）**进行编解码：预训练的 VAE 将 O-Voxel 特征元组 $\\pmb { f } = \\{ ( \\pmb { f } _ { i } ^ { \\mathrm { s h a p e } } , \\pmb { f } _ { i } ^ { \\mathrm { m a t } } , \\pmb { p } _ { i } ) \\} _ { i = 1 } ^ { L }$ 压缩为稀疏潜在 token，每个 token 绑定到固定的三维坐标 $\\pmb{p}_i$，联合编码局部几何（$\\pmb{f}_i^{\\mathrm{shape}}$）和 PBR 材质参数（$\\pmb{f}_i^{\\mathrm{mat}}$）。这种**结构化稀疏网格表示**是 EVA01 区别于 VecSet 范式的关键——消融实验表明，VecSet 在统一序列设置下完全失败，损失迅速平台化，无法产生可用几何（Figure 10 right）。

### 空间偏置注入

为防止长上下文编辑中的几何漂移，EVA01 引入**3D 交错 MRoPE**：将 Qwen3-VL 原生的 (T, W, H) 旋转位置编码重新用于稀疏体素坐标 (x, y, z)，对网格 token 应用交错旋转嵌入 $\\mathsf{RoPE}(\\mathbf{x}, \\mathbf{p}) = \\mathsf{Interleave}\\left(\\mathcal{R}_x(\\mathbf{x}_{\\mathcal{T}_x}), \\mathcal{R}_y(\\mathbf{x}_{\\mathcal{T}_y}), \\mathcal{R}_z(\\mathbf{x}_{\\mathcal{T}_z})\\right)$，将欧氏几何偏置均匀注入稀疏网格。

### 数据管线

支撑上述架构的是一个层次化数据管线（Figure 3）：首先通过几何规范化、美学过滤和多视图密集标注构建高质量**文本-图像-网格三元组**静态语料；然后通过**程序化编辑**（利用刚体变换和动画关键帧）与**语义编辑**（利用 2D 生成先验）两条互补路径合成多轮编辑序列，为上下文感知编辑提供训练信号。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_16745/figures/005_Figure_3.jpg]]
*Figure 3: Data Curation Pipeline of EVA01. (Left) Static 3D Asset Curation: We standardize raw 3D assets through geometric canonicalization, aesthetic filtering, and multi-view dense captioning to construct high-quality text-image-mesh triplets. (Right) Interleaved Editing Sequences: To enable context-aware editing, we synthesize multi-turn sequences via two complementary pathways: Procedural Editing (top right) utilizing rigid transformations and animation keyframes for structural precision, and Semantic Editing (bottom right) leveraging 2D generative priors for open-ended stylistic modification*

### 关键设计决策的证据支撑

架构中的每个关键选择均有消融实验支撑：

1. **结构化稀疏网格 vs. VecSet**：VecSet 在统一序列设置下生成损失远高于网格稀疏潜在，归一化得分极低（Figure 10 right），证明无序表示无法在 MLLM 序列流中有效工作。
2. **图像温启动 vs. 纯文本训练**：纯文本训练收敛更慢且最终得分更低，图像温启动显著加速收敛并提升最终生成质量（Figure 10 right）。
3. **对齐预热 vs. 直接指令微调**：直接指令微调导致网格理解性能饱和且归一化字幕得分更低，10K 步对齐预热后再微调获得更优表现（Figure 10 left）。
4. **模态丢弃**：在 Stage 3 中必不可少，防止生成专家在弱文本条件下忽略文本语义（Sec. 5）。

EVA01 的核心设计围绕一个核心矛盾展开：如何将预训练 MLLM 的语义先验高效迁移到 3D 几何域，同时保持多轮编辑中的身份一致性。其解决方案可归纳为三个关键模块：**混合专家 Transformer 主干**、**结构化稀疏网格潜在表示**，以及**五阶段课程学习策略**。

### 混合专家 Transformer 主干

EVA01 将模型解耦为**理解专家**（$E_{\text{und}}$）和**生成专家**（$E_{\text{gen}}$），二者在结构上镜像对称，通过共享全局注意力实现跨模态知识迁移。

**理解专家**作为稳定的语义锚点，继承预训练 MLLM（Qwen3-VL）的多模态先验，负责处理文本（Qwen tokenizer）、图像（SigLIP2 视觉编码器）和网格（Point-BERT 编码器）的编码。**生成专家**则专门负责几何合成，仅处理网格 token，实现三阶段流匹配：稀疏结构 → 稀疏几何 → 稀疏材质。

双专家的硬路由通过模态特定的线性变换实现：

$$\mathbf{h}_i' = \mathbf{h}_i \mathbf{W}^{(m_i)}$$

其中 $m_i$ 为第 $i$ 个 token 的模态索引，$\mathbf{W}^{(m_i)}$ 为对应模态的权重矩阵。这确保理解专家和生成专家各自优化的参数空间相互独立。

共享全局注意力是跨专家推理的核心窗口。每个 token 的 Query、Key、Value 通过模态特定的投影矩阵计算：

$$\mathbf{q}_i, \mathbf{k}_i, \mathbf{v}_i = \mathbf{h}_i \mathbf{W}_Q^{(m_i)}, \mathbf{h}_i \mathbf{W}_K^{(m_i)}, \mathbf{h}_i \mathbf{W}_V^{(m_i)}$$

随后，所有 token 的 Key 和 Value 被汇聚到统一的注意力计算中，由注意力掩码 $\mathbf{M}$ 控制信息流：

$$\mathbf{y}_i = \mathsf{Attn}(\mathbf{q}_i, \mathbf{K}, \mathbf{V}; \mathbf{M}) \mathbf{W}_O^{(m_i)}$$

注意力掩码 $\mathbf{M}$ 的设计是保证多轮编辑一致性的关键机制（参见 Table 1）：当前生成轮次的稀疏结构、稀疏几何和稀疏材质块对历史轮次的干净几何采用双向注意力，但对自身及后续轮次的噪声块则施加因果或掩码约束，从而防止信息泄漏。

### 结构化稀疏网格潜在表示

EVA01 摒弃了无序的 VecSet 表示，采用结构化的稀疏网格潜在 token（O-Voxel）。每个 3D 资产被表示为一组特征元组：

$$\pmb{f} = \{ (\pmb{f}_i^{\mathrm{shape}}, \pmb{f}_i^{\mathrm{mat}}, \pmb{p}_i) \}_{i=1}^{L}$$

其中 $\pmb{f}_i^{\mathrm{shape}}$ 编码局部几何特征，$\pmb{f}_i^{\mathrm{mat}}$ 编码 PBR 材质参数，$\pmb{p}_i$ 为活性体素的三维坐标。预训练的稀疏体素 VAE（O-Voxel VAE）负责 mesh ↔ latent 的双向转换，将体素特征压缩为稀疏潜在 token。

为注入欧氏几何偏置，EVA01 将 Qwen3-VL 原生的 $(T, W, H)$ 旋转位置编码重新用于稀疏网格坐标 $(x, y, z)$，提出 **3D Interleaved MRoPE**：

$$\mathsf{RoPE}(\mathbf{x}, \mathbf{p}) = \mathsf{Interleave}\left(\mathcal{R}_x(\mathbf{x}_{\mathcal{T}_x}), \mathcal{R}_y(\mathbf{x}_{\mathcal{T}_y}), \mathcal{R}_z(\mathbf{x}_{\mathcal{T}_z})\right)$$

该操作将旋转嵌入沿 $x$、$y$、$z$ 三个轴交错应用于特征切片，使空间信息均匀分布在稀疏网格中。这一设计在长上下文编辑中防止了几何漂移，是多轮身份保持的结构性保障。

### 五阶段课程学习

EVA01 的训练分为五个阶段（参见 Table 2）：

- **Stage 1（网格理解热身）**：在网格字幕数据上进行对齐预热，建立语义-几何的初始映射。
- **Stage 2（视觉-几何初始化）**：图像温启动，利用图像生成数据初始化生成专家的几何先验。
- **Stage 3（语义模态对齐）**：通过 Triple-Batch Sampling 和 Modality Dropout 实现文本、图像与网格的跨模态对齐。
- **Stage 4（上下文感知指令调优）**：在多轮编辑序列上进行指令微调，条件为历史网格状态 $\mathbf{c}_k = \{ \mathbf{t}_{\mathsf{inst}}, \mathbf{x}_{\mathsf{hist}} \}$。
- **Stage 5（高质量微调）**：在精选数据上进行最终优化。

生成训练采用条件流匹配损失：

$$\mathcal{L}_{\mathsf{FM}}(\theta) = \mathbb{E}_{t, \mathbf{x}_0, \mathbf{x}_1, \mathbf{c}} [ || \mathbf{v}_\theta (\mathbf{x}_t, t, \mathbf{c}) - (\mathbf{x}_1 - \mathbf{x}_0) ||^2 ]$$

其中 $\mathbf{x}_1$ 为干净潜在，$\mathbf{x}_0$ 为噪声，$\mathbf{c}$ 为历史上下文条件。理解训练则采用标准的自回归交叉熵损失：

$$\mathcal{L}_{\mathsf{CE}}(\theta) = - \sum_{i=1}^{T} \log p_\theta (t_i \mid t_{<i}, \mathbf{x}_{\mathrm{mesh}})$$

**关键消融证据**：VecSet 表示在统一序列设置下完全失败——损失迅速平台化，归一化得分远低于网格稀疏潜在表示。图像温启动相比纯文本训练显著提升生成收敛速度和最终得分，增加网格理解监督进一步带来增益。对齐预热对于网格理解至关重要：直接指令微调导致饱和，而 10K 步预热后再微调获得更优表现。Modality Dropout 在 Stage 3 中必不可少，防止生成专家在弱文本条件下忽略文本语义。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_16745/figures/015_Figure_9.jpg]]
*Figure 9: Representation visualization across visual and image-generation encoders. We visualize the same feature paths probed in Table 6 using input views, PCA projections, normalized activation maps, self-similarity, and cross-view correspondence overlays. Lavender rows denote semantic or understanding-token paths, while mint rows denote dense visual or generation-side latent paths. The visualization reveals that global semantic alignment, dense spatial correspondence, and generation-side appearance latents form distinct representation regimes rather than a single universally optimal feature space*

## 实验与关键发现

### 主结果分析

#### 文本/图像到3D生成

EVA01在Toys4K基准上展现出对现有方法的显著优势。在文本到3D生成任务中，EVA01的用户偏好率达到**70.4%**，而最强基线TRELLIS仅为14.8%（Table 3），偏好差距接近**5倍**。在分布相似性指标上，EVA01的FDDINOv2为122.48，远低于ShapeLLM-Omni的310.55（降低188.07），KDDINOv2为1.18，同样大幅优于ShapeLLM-Omni的18.20（降低17.02）。这表明EVA01生成的3D资产在语义一致性和几何质量上均显著优于基线方法。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_16745/figures/006_Table_3.jpg]]
*Table 3: Quantitative comparisons on Toys4K. We report CLIP, FDDINOv2, KDDINOv2, and user-study preference (Pref). KD is reported ×100. N/A denotes unsupported modalities*

定性比较（Figure 4）进一步验证了这一结论：在图像条件和文本条件两种设置下，EVA01生成的网格在物体级语义保持、部件结构和材质一致性上均优于**3DTopia-XL**（Chen et al., CVPR 2025）、**Hunyuan3D-2.1**（Tencent Hunyuan3D Team, 2025a）、**Michelangelo**（Zhao et al., NeurIPS 2023）、**ShapeLLM-Omni**（Ye et al., 2025b）、**Step1X-3D**（Li et al., 2025b）、**TRELLIS**（Xiang et al., 2024/2025）、**3DGen-R1**（Tang et al., 2025a）和**GVGEN**（He et al., ECCV 2024）等代表性基线。基线方法常出现部件缺失、拓扑扭曲、过度平滑或表面碎片化等问题，而EVA01能产生完整且几何连贯的网格。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_16745/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative Comparison with Baselines. We compare EVA01 with representative text-to-3D and image-to-3D baselines on Toys4K, including 3DTopia-XL, Hunyuan3D-2.1, Michelangelo, ShapeLLM-Omni, Step1X-3D, TRELLIS, 3DGen-R1, and GVGEN. Across both image-conditioned cases (left) and text-conditioned cases (right), EVA01 better preserves object-level semantics, part structure, and material consistency, producing complete meshes with coherent geometry where prior methods often suffer from missing components, distorted topology, over-smoothed shapes, or fragmented surfaces*

#### 3D网格理解

在PointLLM-200网格描述任务上，EVA01-Final的GPT-img得分达到**65.91**，甚至超过了人工标注的GT描述得分56.05（Table 4），表明模型生成的描述在渲染图语义评估下比人工标注更优。在BLEU-1指标上，EVA01-Align取得23.592，超越GreenPLM等基线方法。定性结果（Figure 5、Figure 6）显示，EVA01-Final相比对齐阶段模型能提供更丰富的部件级、材质级、颜色级和结构级描述。

#### 多轮3D编辑

在多轮3D编辑评估中，EVA01以**93.75%**的用户偏好率压倒性超过**VoxHammer**（Li et al., 2025a）的3.75%和TRELLIS的2.50%（Table 5），实现了**无掩码的身份保持编辑**。CD和PSNR指标评估未编辑区域的一致性，CLIP和FDDINOv2评估整体编辑质量，EVA01在所有维度上均保持领先。Figure 7展示了从EVA01文本到3D生成出发的三轮连续编辑轨迹，模型能够累积指令——添加或移除部件、改变物体状态、替换组件、修改姿态——同时保持物体身份和几何历史的一致性。

### 消融实验

消融实验揭示了EVA01训练策略和表征选择中的关键因果机制：

**网格理解侧**（Figure 10左）：
- **对齐预热（alignment warm-up）不可或缺**：直接进行指令微调会导致性能饱和，归一化描述得分更低；而先进行10K步对齐预热再进行微调，能获得显著更优的表现。这验证了渐进式语义-几何对齐在跨模态知识迁移中的必要性。
- **稀疏Shape-to-Text路径不可行**：使用生成侧的稀疏VAE潜在token进行语言对齐时，交叉熵损失在高值处停滞，描述语义不可靠。这说明理解任务需要专门的编码路径，生成侧的压缩表示丢失了语义对齐所需的信息。

**网格生成侧**（Figure 10右）：
- **图像温启动（image warm-up）是生成训练的必需条件**：纯文本训练收敛更慢且最终得分更低；增加网格理解监督进一步提升了收敛速度和最终得分。这证明了从预训练MLLM的视觉先验中温启动对于几何生成至关重要。
- **VecSet表示在统一序列设置下完全失败**：损失迅速平台化，归一化得分远低于网格稀疏潜在表示。这一结果直接支持了核心设计选择——结构化的稀疏网格潜在token（O-Voxel）是3D网格作为原生模态融入MLLM序列流的必要条件。
- **模态丢弃（Modality Dropout）在Stage 3中必不可少**：能防止生成专家在弱文本条件下忽略文本语义，确保跨模态对齐的鲁棒性。

### 特征空间探测

Table 6和Figure 9揭示了不同编码器路径的表征特性：全局语义对齐（如理解token路径）、密集空间对应（如视觉token路径）和生成侧外观潜在（如VAE latent路径）形成了**三个截然不同的表征体系**，而非单一的最优特征空间。这一发现解释了为何EVA01需要分别设计理解专家和生成专家的编码路径，而非共享统一的3D编码器。

### 失败模式分析

Figure 11系统展示了EVA01的典型失败案例：

1. **分布外组合泛化有限**：文本到3D生成中对新颖的物体组合泛化能力不足。
2. **空间推理和精确计数不完善**：模型在需要精确空间关系理解和数量判断的任务上仍存在错误。
3. **3D表面文字/符号布局质量差**：生成可读的文字或符号纹理是当前的薄弱环节。
4. **图像到3D的像素证据不足问题**：当单视图输入缺少足够的密集像素证据时（薄结构、遮挡部件或远距离微小组件欠采样），模型可能恢复主导物体但丢失局部细节或产生不完整几何。

这些失败模式与论文中识别的局限性一致，指向了SigLIP2视觉路径在语义对齐和密集空间对应上的固有局限，以及当前模型规模（相对于潜在的大规模基础模型）带来的容量瓶颈。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2605_16745/figures/016_Figure_10.jpg]]
*Figure 10: Training Dynamics and Loss Curves. Left: mesh-understanding ablations comparing direct instruction tuning, a 10K alignment warm-up followed by instruction tuning, and Sparse Shape-to-Text, which uses generation-side sparse VAE latents for captioning. Solid curves report CE loss, and dashed marker curves report normalized captioning score. Right: Sparse Shape generation ablations comparing text-only training, image warm-up, image warm-up with mesh understanding, VecSet representation, and multi-layer hidden-feature concatenation for cross-attention. Solid curves report MSE loss, and dashed marker curves report normalized generation score relative to the best text-to-3D checkpoint*

## 定位与知识库关联

### 1. 与现有基线的结构性差异

EVA01 在统一3D理解与生成的框架中引入了三个核心架构变更，使其从根本上区别于现有方法。

**架构解耦 vs 统一骨干。** 现有统一3D多模态模型（如 **ShapeLLM-Omni** (Ye et al., 2025b)）采用单一骨干处理所有模态，将理解与生成任务耦合在同一参数空间中。EVA01 则基于 Mixture-of-Transformers（MoT）架构，将模型解耦为理解专家（E_und）和生成专家（E_gen），通过 hard modality routing 实现任务分离优化。E_und 继承预训练 MLLM（Qwen3-VL）的语义先验，处理文本、图像和网格编码；E_gen 则专门负责几何合成，执行三阶段流匹配（稀疏结构→稀疏几何→稀疏材质）。两专家通过共享全局注意力实现跨模态知识迁移，其中 E_gen 查询 E_und 的语义 token，结合统一的注意力掩码（Table 1）控制信息流。

**结构化稀疏网格 vs 无序潜在表示。** 现有3D生成框架广泛采用 VecSet 范式（**3DShape2VecSet**, Zhang et al., SIGGRAPH 2023），将3D形状编码为无序的潜在 token 集合。EVA01 用结构化的稀疏网格潜在 token（O-Voxel）替代这一范式：每个 token 绑定到固定的三维坐标 $(x,y,z)$，联合编码局部几何 $f_i^{\text{shape}}$ 与 PBR 材质参数 $f_i^{\text{mat}}$（Eq. 1）。消融实验（Figure 10 right）表明，VecSet 在统一序列设置下完全失效——损失迅速平台化，归一化得分远低于网格稀疏潜在表示。这一证据强度较高（confidence 0.95），直接验证了结构化表示对统一序列建模的必要性。

**有状态序列建模 vs 无状态重建。** 现有3D编辑方法（如 **VoxHammer** (Li et al., 2025a) 和 **TRELLIS** (Xiang et al., 2024/2025)）每次编辑均为独立的重建过程，不保持跨轮次的几何身份一致性。EVA01 通过有状态序列建模实现上下文感知编辑：第 $k$ 步生成的条件 $\mathbf{c}_k = \{ \mathbf{t}_{\text{inst}}, \mathbf{x}_{\text{hist}} \}$ 包含当前指令 token 和累积的历史网格状态。此外，3D Interleaved MRoPE（Eq. 5）将 Qwen3-VL 的 $(T,W,H)$ 旋转位置编码重新用于稀疏网格坐标 $(x,y,z)$，注入欧氏几何偏置以防止长上下文编辑中的几何漂移。

### 2. 训练策略的关键创新

EVA01 的五阶段课程学习（Table 2）是其方法有效性的核心支撑，其中三个机制尤为关键：

- **对齐预热（Alignment Warm-up）：** Stage 1 中 10K 步的网格理解预热对后续性能至关重要。消融实验（Figure 10 left）显示，跳过预热直接进行指令微调会导致交叉熵损失饱和且归一化字幕得分更低。值得注意的是，使用生成侧的稀疏 VAE 潜在 token 进行语言对齐（Sparse Shape-to-Text）效果很差——交叉熵损失在高值处停滞，描述语义不可靠。这暗示理解与生成任务对3D表示的需求存在本质差异，验证了解耦专家设计的合理性。

- **图像温启动（Image Warm-up）：** Stage 2 的图像温启动对生成训练是必需的。纯文本训练收敛更慢且最终得分更低；增加网格理解监督进一步提升了收敛速度和最终得分（Figure 10 right）。这一发现表明，预训练 MLLM 的视觉语义先验是桥接文本到3D几何的关键中介。

- **模态丢弃（Modality Dropout）：** Stage 3 中的 Triple-Batch Sampling 和 Modality Dropout 防止生成专家在弱文本条件下忽略文本语义。论文明确将其列为不可或缺的机制（Sec. 5, confidence 0.9），但未提供独立的消融曲线，该结论的证据强度略低于前述两项。

### 3. 适用边界与已知局限

**分布外泛化有限。** 在文本到3D生成中，EVA01 对分布外组合的泛化能力不足，空间推理、精确计数和3D表面文字/符号布局仍不完美（Figure 11）。这些失败模式与当前视觉编码路径的语义对齐局限相关——SigLIP2 在密集空间对应性上存在不足（Table 6, Figure 9），限制了生成质量的上限。

**单视图信息瓶颈。** 在图像到3D场景中，当单视图输入缺少足够的密集像素证据（薄结构、遮挡部件或远距离微小组件欠采样）时，模型可能丢失局部细节或产生不完整几何（Figure 11）。这本质上是一个输入信息瓶颈问题，而非架构缺陷。

**模型规模约束。** 当前 EVA01 的模型规模相对较小。论文明确指出将各专家扩展至 4B–8B 参数、并将稀疏体素分辨率提升至 $1024^3$ 是未来方向。此外，开发稀疏体素原生的编码器家族以统一理解与生成专家的3D表示，以及用能够同时保留文本对齐和密集块结构的替代编码器（如 DINOv3 启发的视觉路径）替换 SigLIP2，是系统性地提升生成质量的关键开放问题。

### 4. 知识库定位

EVA01 处于3D原生多模态大语言模型（3D-native MLLM）这一新兴方向的交叉点。与 **PointLLM**（Xu et al., 2024b）和 **ShapeLLM**（Qi et al., 2024）等仅关注3D理解的模型不同，EVA01 首次将网格理解、生成和上下文感知编辑统一在单一 MoT 架构中。与 **TRELLIS** 和 **Hunyuan3D-2.1**（Tencent Hunyuan3D Team, 2025a）等纯生成模型不同，EVA01 将3D网格作为原生模态融入 MLLM 序列流，而非将生成作为独立的后处理步骤。

在多轮编辑维度，EVA01 以 93.75% 的用户偏好压倒性超过 VoxHammer（3.75%）和 TRELLIS（2.50%）（Table 5, confidence 0.98），实现了无掩码的身份保持编辑。这一差距（+90.0%）远超单轮生成任务中对 TRELLIS 的优势（70.4% vs 14.8%，+55.6%，Table 3），表明有状态序列建模在多轮交互场景中的价值远大于单轮生成场景。

**需要手动验证的点：** GreenPLM 的引用信息在分析中缺失，若需在正文中精确引用，建议查阅原始论文确认作者和发表信息。此外，3DGen-R1（Tang et al., 2025a）和 Step1X-3D（Li et al., 2025b）的发表 venue 未在分析中提供，需要进一步核实。

## 原文 PDF

![[paperPDFs/arxiv_2026/EVA01:_Unified_Native_3D_Understanding_and_Generation_via_Mixture-of-Transformers.pdf]]
