---
title: "CaliTex: Geometry-Calibrated Attention for View-Coherent 3D Texture Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CaliTex_Geometry_Calibrated_Attention_for_View_Coherent_3D_Texture_Generation.pdf
project_link: "https://calitex-project.github.io"
code_link: null
aliases:
- CaliTex
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过将几何先验显式地校准到注意力计算中：Part-Aligned Attention将跨视角注意力限制在同一语义部件内部，消除跨视角歧义；Condition-Routed Attention通过双路径设计强制外观信息经由几何条件路由，抑制直接复制参考图像，解决跨模态歧义。
primary_logic: 几何一致性并非通过额外监督或后处理获得，而是应通过架构层面的注意力校准使其成为模型的固有行为：在注意力计算中直接嵌入三维结构感知，从而取代传统的全注意力机制。
claims:
- 全注意力不加区分地应用于所有token和模态，造成跨视角歧义和跨模态歧义。
- Part-Aligned Attention通过约束注意力在语义部件内，消除跨视角不一致。
- Condition-Routed Attention通过几何条件路由外观信息，避免直接参考复制，保证纹理与几何对齐。
- Test set (Objaverse + game assets) 上 FID = 157.8
---

# CaliTex: Geometry-Calibrated Attention for View-Coherent 3D Texture Generation

> [!tip] 核心洞察
> 几何一致性并非通过额外监督或后处理获得，而是应通过架构层面的注意力校准使其成为模型的固有行为：在注意力计算中直接嵌入三维结构感知，从而取代传统的全注意力机制。

| 字段 | 内容 |
|------|------|
| 中文题名 | CaliTex: 几何校准注意力实现视角一致的3D纹理生成 |
| 英文题名 | CaliTex: Geometry-Calibrated Attention for View-Coherent 3D Texture Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.21309) · [Project](https://calitex-project.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | CaliTex |
| Dataset | Test set |

> [!tip] 效果简介
> - Test set (Objaverse + game assets) 上，FID 157.8 vs not reported (best among compared methods) (lowest)；User Study Qual (overall quality) 4.53 vs not reported (highest) (highest)。

## 概要

从单张参考图像生成高质量三维纹理，核心挑战在于**跨视角一致性与几何对齐**。现有方法普遍采用不加区分的全注意力机制，导致两类内在歧义：(1) **跨视角歧义**——几何相似但语义不同的区域（如左右肢体）错误关注，产生纹理接缝与空间不一致；(2) **跨模态歧义**——噪声token在参考图像与几何条件之间交替关注，造成外观过拟合或几何过度依赖，最终纹理与几何错位。

CaliTex 的核心洞察是：**几何一致性不应通过额外监督或后处理获得，而应通过架构层面的注意力校准使其成为模型的固有行为**。基于此，CaliTex 提出两种几何校准的注意力机制，将三维结构感知直接嵌入注意力计算中：

- **Part-Aligned Attention (PAA)**：利用 PartField 将三维网格分解为语义部件（K=20），约束跨视角注意力仅在相同部件内的 token 间计算，从源头消除跨视角歧义。
- **Condition-Routed Attention (CRA)**：通过双路径设计（condition-reference 组融合几何与视觉先验，noise-condition 组注入几何感知特征）强制外观信息经由几何条件路由，抑制直接复制参考图像，解决跨模态歧义。

整体框架采用**两阶段扩散Transformer**：Single-View DiT 捕获单视角内部语义，Multi-View DiT 通过 PAA 和 CRA 增强跨视角与跨模态一致性，生成的多视角图像经反投影与修复得到最终纹理贴图。

在 Objaverse 与游戏资产测试集上，CaliTex 取得最低 FID（157.8）和最高用户研究评分（4.53），消融实验证实 PAA 和 CRA 分别显著改善像素级多视角一致性（MV-MSE）和纹理-几何对齐。该方法以几何先验校准注意力，为视角一致的纹理生成提供了新的架构范式。

### 3D纹理生成的核心挑战：从图像先验到几何一致的表面外观

为三维资产生成高质量纹理是计算机图形学与视觉内容创作中的关键环节。近年来，基于扩散模型（Diffusion Models）的图像生成技术取得了显著进展，使得从单张参考图像出发为三维网格生成纹理成为一条极具潜力的技术路线。然而，将二维图像先验迁移到三维表面时，如何保持**跨视角一致性**与**几何对齐**仍然是尚未解决的核心难题。

当前主流的3D纹理生成方法普遍采用基于多视角注意力（Multi-View Attention）的扩散Transformer架构。这些方法在生成多视角图像时，通常在所有视角的token之间施加**不加区分的全注意力（Full Attention）**机制。这种朴素的设计虽然简单直接，却引入了两种深层次的注意力歧义，严重损害纹理的质量与一致性。

### 瓶颈：全注意力机制引发的双重歧义

**（1）跨视角歧义（Cross-view Ambiguity）**

全注意力允许模型在任意视角的任意空间位置之间自由建立关联。当三维物体存在几何对称性或重复结构时（例如人物的左右肢体、椅子的四条腿），模型极易将不同视角中几何相似但语义不同的区域混淆。这种错误关联导致生成的纹理在不同视角之间出现接缝（seams）和空间错位，破坏了视觉连续性。如图2(a)所示，模型将第二个视角中的左肢与右肢混淆，在纹理上产生了明显的接缝。

**（2）跨模态歧义（Cross-modality Ambiguity）**

在多视角纹理生成中，噪声token（noise tokens）需要同时关注两类信息源：参考图像的**外观先验**和三维几何的**结构条件**。在全注意力机制下，噪声token可以在两者之间自由切换注意力，缺乏明确的信息路由规则。这导致两种典型的失败模式：一是模型过度依赖参考图像中的视觉相似区域进行直接复制，忽略底层几何结构，造成纹理与几何的错位（如图2(c)中衣物纹理的扭曲）；二是在某些区域过度依赖几何条件，丧失了参考图像中的细节纹理信息。

这两种歧义的根本原因在于：**现有的注意力机制缺乏对三维结构的显式建模**。模型在计算token间的关联时，完全没有意识到这些token在三维空间中对应的几何位置和语义归属，因此无法做出符合物理一致性的注意力决策。

### 现有方法的局限与本文动机

尽管已有工作尝试通过多视角扩散模型（如**MV-Adapter** (Huang et al., ICCV 2025)、**UniTEX** (Liang et al., arXiv 2025)、**Step1X-3D** (Li et al., arXiv 2025) 和 **Hunyuan3D 2.1** (Tencent Hunyuan3D Team, arXiv 2025)）来改进纹理生成质量，但它们大多沿用全注意力范式，仅通过数据驱动的方式隐式学习跨视角对应关系。这种隐式学习在面对复杂几何结构或高度对称的物体时，往往无法可靠地消除上述两种歧义，导致生成的纹理在接缝处出现不连续，或在细节区域与几何结构错位。

本文的核心动机在于：**几何一致性不应通过额外的后处理或监督信号来补救，而应通过架构层面的注意力校准，使其成为模型的内在行为**。具体而言，本文提出将三维几何先验**显式地嵌入到注意力计算过程中**，使模型在决定“关注哪里”时具备三维结构感知能力，从而从根本上消除跨视角歧义和跨模态歧义。这一思路催生了CaliTex框架及其两个核心机制：**Part-Aligned Attention**（部件对齐注意力）和**Condition-Routed Attention**（条件路由注意力），分别针对上述两种歧义进行架构层面的校准。

## 核心方法与创新机理

CaliTex 的核心创新在于**将几何先验显式地校准到注意力计算中**，从根本上解决当前多视角纹理生成中普遍存在的注意力歧义问题。现有方法（如 **MV-Adapter** (Huang et al., ICCV 2025)、**UniTEX** (Liang et al., arXiv 2025)、**Step1X-3D** (Li et al., arXiv 2025)、**Hunyuan3D 2.1** (Tencent Hunyuan3D Team, arXiv 2025)）在扩散 Transformer 中采用不加区分的全注意力机制，导致两类内在歧义：

- **跨视角歧义**：不同视角间几何相似但语义不同的区域（如左右肢体）错误地相互关注，产生纹理接缝与空间不一致。
- **跨模态歧义**：噪声 token 在参考图像 token 和几何条件 token 之间交替关注，造成外观过拟合或几何过度依赖，最终纹理与几何错位。

针对上述瓶颈，CaliTex 从架构层面重新设计了注意力机制，提出两个关键模块：

### Part-Aligned Attention (PAA)

**变更点**：将基线方法中所有视角间的完全注意力，替换为基于语义部件的分组注意力。

PAA 利用 PartField 将三维网格 $M$ 分解为 $K=20$ 个语义部件 $\mathcal{P}_1, \mathcal{P}_2, \ldots, \mathcal{P}_K$。对于每个图像 token $t_i$，若其对应图像块中任一像素属于部件 $k$，则将该 token 分配至组 $\mathcal{G}_k$：

$$\mathcal{G}_k = \{ t_i \mid \exists p \in \operatorname{Patch}(t_i), c(p) = k \}$$

跨视角注意力仅在组内计算，保留了视角内的全局注意力以维持语义完整性，而在跨视角维度上强制几何感知的局部性：

$$\operatorname{Attn}_{\mathrm{PAA}}(Q, K, V) = \bigcup_{k=1}^{K} \operatorname{Attn}_k(Q, K, V)$$

这一设计消除了跨视角歧义——几何相似但语义不同的区域不再相互干扰，从机制上保证了纹理的跨视角一致性。

### Condition-Routed Attention (CRA)

**变更点**：将基线方法中噪声 token 与参考图像 token 的直接交互，替换为经由几何条件路由的双路径注意力。

CRA 将 Multi-View DiT 中的 token 分为三个集合：噪声 token、条件 token 和参考 token。注意力计算被重构为两条并行路径：

1. **condition–reference 组**：条件 token 与参考 token 在组内进行自注意力，融合几何与外观先验：
   $$\operatorname{Attn}_{\mathrm{cr}} = \operatorname{Softmax}\left(\frac{Q_{\mathrm{cr}} K_{\mathrm{cr}}^\top}{\sqrt{d}}\right) V_{\mathrm{cr}}$$

2. **noise–condition 组**：噪声 token 仅与条件 token 交互，注入几何感知特征，而非直接访问参考图像。

最终输出为两条路径的并集，且每对 token 仅计算一次注意力：
$$\operatorname{Attn}_{\mathrm{CRA}} = \operatorname{Attn}_{\mathrm{n-c}} \cup \operatorname{Attn}_{\mathrm{c-r}}$$

CRA 通过强制外观信息经由几何条件路由，抑制了噪声 token 直接复制参考图像中视觉相似区域的行为，确保纹理与几何严格对齐。

### 架构层面的系统性变更

上述两个模块嵌入在一个**两阶段扩散 Transformer 框架**中：Single-View DiT 捕获单视角内部的语义对应关系，Multi-View DiT 通过 PAA 和 CRA 增强跨视角与跨模态一致性。这一设计将几何一致性从外部约束内化为模型的固有行为，而非依赖额外监督或后处理。

CaliTex 采用**两阶段扩散Transformer架构**，将3D纹理生成分解为视角内语义建模与跨视角几何校准两个互补阶段，并在核心注意力层嵌入几何先验，从根本上消除全注意力机制引发的跨视角歧义与跨模态歧义。

### 输入输出流

整个pipeline的输入包括：
- 一张**参考图像**（提供外观先验）
- 目标三维网格的**多视角几何条件**（法线图或深度图等渲染视图）
- 初始**噪声潜在变量**（每个目标视角对应一个噪声token序列）

输出为**多视角RGB图像**，随后通过**反投影与修复**（Back-projection and Inpainting）模块映射到三维表面，得到最终的UV纹理贴图。

### 两阶段生成架构

如图3所示，生成过程由两个级联的DiT模块完成：

**第一阶段：Single-View DiT**
该模块独立处理每个目标视角，在单视角内部执行完全自注意力，捕获视角内的外观与语义对应关系。其作用是为后续跨视角推理提供高质量的逐视角特征表示。

**第二阶段：Multi-View DiT**
将所有视角的噪声token、几何条件token以及视角平均后的参考图像token展平拼接，形成统一的序列输入。该阶段的核心任务是通过两个校准注意力机制——**Condition-Routed Attention (CRA)** 和 **Part-Aligned Attention (PAA)**——显式建模跨视角空间对应关系与跨模态信息路由，消除全注意力带来的固有歧义。

### 核心校准机制的设计逻辑

全注意力不加区分地应用于所有token和模态，导致两种内在歧义：
1. **跨视角歧义**：几何相似但语义不同的区域之间错误关注，产生纹理接缝与空间不一致。
2. **跨模态歧义**：噪声token交替关注参考图像或几何条件，造成外观过拟合或几何过度依赖，最终纹理与几何错位。

CaliTex 的解决方案是将几何先验**嵌入注意力计算本身**，而非依赖额外监督或后处理：

- **Condition-Routed Attention** 将Multi-View DiT中的注意力重构为双路径设计：condition–reference组内自注意力融合几何与视觉先验，noise–condition组注意力将几何感知特征注入噪声token。这一结构强制外观信息经由几何条件路由，抑制噪声token直接复制参考图像，从而解决跨模态歧义。
- **Part-Aligned Attention** 利用PartField将三维网格分解为K=20个语义部件，并将跨视角token按部件分组——仅在同一部件组内计算跨视角注意力。这种几何感知的局部性约束消除了跨视角歧义，确保纹理在不同视角间保持语义一致性。

### 训练目标

整个多视角生成网络采用流匹配目标进行训练：

$$\mathcal{L}(\theta) = \mathbb{E}_{t, z_0, \epsilon} \Big[ || z_{\mathbf{img}}' - (\epsilon - z_0) ||^2 \Big]$$

该损失驱动模型学习从噪声到目标多视角图像的连续变换轨迹。

### 从多视角图像到纹理贴图

Multi-View DiT生成的多视角RGB图像通过反投影操作映射到三维网格表面，并对遮挡区域进行修复，最终输出完整的UV纹理贴图。这一后处理步骤将2D生成结果转化为可直接用于渲染的3D资产。

> **注意**：本文未提供代码链接和发表会议/年份信息，上述架构描述完全基于论文文本分析。训练数据规模为Objaverse-XL与Texverse中的约80k个物体，在8块GPU上训练约600 GPU小时。

![[assets/figures/papers/paper_list_l2446_https_arxiv_org_abs_2511_21309/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our method. (a) We employ a two-stage generation framework: the Single-View DiT captures intra-view correlations, while the Multi-View DiT enhances geometric alignment and cross-view consistency using (b) Condition-Routed Attention and (c) Part-Aligned Attention. The generated multi-view images are then projected back and inpainted to produce the final 3D texture*

CaliTex 的核心设计是将三维几何先验显式地嵌入扩散 Transformer 的注意力计算中，以取代传统不加区分的全注意力。方法采用两阶段生成架构：**Single-View DiT** 负责捕获单视角内部的语义与外观对应关系，**Multi-View DiT** 则通过两个校准的注意力机制——**Condition-Routed Attention (CRA)** 和 **Part-Aligned Attention (PAA)**——分别解决跨模态歧义与跨视角歧义。

### Condition-Routed Attention (CRA)

CRA 解决的核心问题是：噪声 token 在注意力计算中交替关注参考图像或几何条件，导致外观过拟合或几何过度依赖，最终纹理与几何错位。CRA 通过双路径设计强制外观信息经由几何条件路由，切断噪声 token 与参考图像 token 的直接交互。

具体而言，Multi-View DiT 的输入由三部分组成：各视角的噪声隐变量、条件隐变量（几何条件编码）以及视角平均的参考图像隐变量。这些 token 被划分为两组独立计算注意力：

- **Condition–Reference 组**：在条件 token 与参考图像 token 之间计算自注意力，融合几何先验与视觉先验：

$$
\mathrm{Attn}_{\mathrm{cr}} = \mathrm{Softmax}\left( \frac{Q_{\mathrm{cr}} K_{\mathrm{cr}}^{\top}}{\sqrt{d}} \right) V_{\mathrm{cr}}
$$

- **Noise–Condition 组**：噪声 token 仅与条件 token 交互，获取经过几何感知的外观特征，而非直接复制参考图像。

两组注意力输出通过合并操作得到最终的 CRA 注意力，且每对 token 仅计算一次：

$$
\mathrm{Attn}_{\mathrm{CRA}} = \mathrm{Attn}_{\mathrm{n-c}} \cup \mathrm{Attn}_{\mathrm{c-r}}
$$

这一设计从架构层面确保了“外观信息总是经由几何条件中介”，从而抑制跨模态歧义。

### Part-Aligned Attention (PAA)

PAA 解决的核心问题是：几何相似但语义不同的区域（如左右肢体）在全注意力下错误互相关注，产生纹理接缝与空间不一致。PAA 利用 PartField 将三维网格分解为 $K=20$ 个语义部件：

$$
M = \{ \mathcal{P}_{1}, \mathcal{P}_{2}, \ldots, \mathcal{P}_{K} \}
$$

基于此，每个 token $t_i$ 根据其对应图像块中像素的部件归属被分配到对应组 $\mathcal{G}_k$：

$$
\mathcal{G}_k = \{ t_i \mid \exists p \in \operatorname{Patch}(t_i), \, c(p) = k \}
$$

PAA 在部件组内部计算跨视角自注意力，而视角内部仍保留完全自注意力以维持全局上下文。部件级注意力定义为：

$$
\mathrm{Attn}_k(Q, K, V) = \mathrm{Softmax}\left( \frac{Q_k K_k^{\top}}{\sqrt{d}} \right) V_k
$$

整体 PAA 输出为所有部件组注意力的聚合：

$$
\mathrm{Attn}_{\mathrm{PAA}}(Q, K, V) = \bigcup_{k=1}^{K} \mathrm{Attn}_k(Q, K, V)
$$

视角内全注意力则独立计算：

$$
\mathrm{Attn}_{\mathrm{intra}}^{(v)}(Q, K, V) = \mathrm{Softmax}\left( \frac{Q^{(v)} {K^{(v)}}^{\top}}{\sqrt{d}} \right) V^{(v)}
$$

通过将跨视角注意力约束在同一语义部件内部，PAA 消除了因几何歧义导致的错误跨视角对应。

### 训练目标

多视角生成网络的训练采用流匹配目标（flow-matching objective）：

$$
\mathcal{L}(\theta) = \mathbb{E}_{t, z_0, \epsilon} \Big[ \| z_{\mathbf{img}}' - (\epsilon - z_0) \|^2 \Big]
$$

其中 $z_0$ 为初始噪声，$\epsilon$ 为目标噪声，$z_{\mathbf{img}}'$ 为网络预测的图像分量速度场。该目标驱动模型学习从噪声到多视角纹理图像的映射。

### 评估指标：MV-MSE

为量化多视角一致性，论文定义了像素级多视角均方误差 MV-MSE，计算对应像素在渲染视图间的平均 MSE：

$$
\mathbf{MV-MSE} = \frac{2}{N(N-1)} \sum_{(i,j)} \frac{1}{|\Omega_i(j)|} \sum_{p \in \Omega_i(j)} \| I_i(p) - I_j(\pi_j(X_p)) \|_2^2
$$

其中 $\Omega_i(j)$ 表示视角 $i$ 中在视角 $j$ 可见的像素集合，$\pi_j$ 为视角 $j$ 的投影变换。该指标直接度量了生成纹理在几何对应点上的跨视角一致性，是消融实验中验证 PAA 和 CRA 有效性的关键依据。

![[assets/figures/papers/paper_list_l2446_https_arxiv_org_abs_2511_21309/figures/002_Figure_2.jpg]]
*Figure 2: Illustration issues caused by attention ambiguity and our proposed solutions. Zoom in for more details. (a) The model confuses the left limb in the second view with the right limb, producing seams in the texture. (b) Our Part-Aligned Attention constrains attention computation within semantic parts, effectively eliminating cross-view inconsistency. (c) The model directly copies visually similar regions from the reference image, leading to misalignment with the geometry condition. (d) Our Condition-Routed Attention ensures geometry-aligned texture generation, correcting the distortion on the clothing, as highlighted in the bottom-right*

## 实验与关键发现

### 实验设置

CaliTex采用两阶段扩散Transformer架构：**Single-View DiT**捕获视角内语义对应，**Multi-View DiT**通过校准的注意力机制增强跨视角与跨模态一致性。DiT主干网络从FLUX.1-Kontext初始化，并集成秩为16的LoRA适配器。训练数据来自Objaverse-XL和Texverse，共约80k个三维对象。模型在8块GPU上训练，总计约600 GPU小时。多视角生成网络采用流匹配目标进行训练：

$$ \mathcal { L } ( \theta ) = \mathbb { E } _ { t , z _ { 0 } , \epsilon } \Big [ | | z _ { \mathbf { i m g } } ^ { \prime } - ( \epsilon - z _ { 0 } ) | | ^ { 2 } \Big ] $$

对比基线包括开源方法**MV-Adapter**（Huang et al., ICCV 2025）、**UniTEX**（Liang et al., arXiv 2025）、**Step1X-3D**（Li et al., arXiv 2025）和**Hunyuan3D 2.1**（Tencent Hunyuan3D Team, arXiv 2025）。

### 主实验结果

定量评估在Objaverse与游戏资产混合测试集上进行，指标涵盖FID、CLIP-FID、CMMD、CLIP-I、LPIPS以及用户研究。CaliTex在所有指标上均取得最优结果（Table 1）：FID降至157.8，为对比方法中最低；用户研究整体质量评分（Qual）达到4.53，同样为最高。用户研究还评估了几何对齐度（GeoAlign）和多视角一致性（MV-Cons），CaliTex均优于所有基线。

定性对比（Figure 4）进一步揭示了现有方法的典型失败模式：开源和商业模型普遍存在跨视角接缝（黄色高亮区域）和纹理与几何错位（蓝色高亮区域），而CaliTex生成的纹理在这些区域表现出显著改善，验证了几何校准注意力机制的有效性。

### 消融实验

#### 像素级多视角对齐

为量化跨视角一致性，论文引入**MV-MSE**指标，计算对应像素在渲染视图间的平均MSE：

$$ \mathbf { M V - M S E } = \displaystyle \frac { 2 } { N ( N - 1 ) } \sum _ { ( i , j ) } \frac { 1 } { | \Omega _ { i } ( j ) | } \sum _ { p \in \Omega _ { i } ( j ) } \| I _ { i } ( p ) - I _ { j } ( \pi _ { j } ( X _ { p } ) ) \| _ { 2 } ^ { 2 } $$

Table 2的消融结果显示，移除Part-Aligned Attention后MV-MSE从0.0384上升至0.0415，表明跨视角一致性显著下降。该结果直接证实了全注意力机制引入的跨视角歧义会损害多视角纹理的对齐质量。

#### Part-Aligned Attention消融

Figure 5展示了PAA的消融效果：移除PAA后，模型在不同视角间产生错误的跨视角对应，导致明显的纹理错位；而加入PAA后，注意力被约束在同一语义部件内部，有效消除了这些错误对应，生成一致的纹理。

#### Condition-Routed Attention消融

Figure 6展示了CRA的消融效果：移除CRA后，噪声token可直接复制参考图像中视觉相似的区域，导致纹理与几何条件错位（如衣物纹理扭曲）；CRA通过双路径设计强制外观信息经由几何条件路由，改善了纹理-几何对齐，减少了最终纹理中的瑕疵。

### 失败模式与局限

论文未明确报告系统性的失败模式或局限性分析。从方法设计角度推断，Part-Aligned Attention依赖于PartField将网格分解为K=20个语义部件，当网格拓扑复杂或部件边界模糊时，token分组可能引入歧义。此外，Condition-Routed Attention的几何条件路由能力受限于条件编码的质量，在极端的几何-外观不匹配场景下可能仍存在对齐误差。上述推断需通过进一步实验验证。

![[assets/figures/papers/paper_list_l2446_https_arxiv_org_abs_2511_21309/figures/007_Table_2.jpg]]
*Table 2: Ablation on pixel-level multi-view alignment*

![[assets/figures/papers/paper_list_l2446_https_arxiv_org_abs_2511_21309/figures/009_Figure_5.jpg]]
*Figure 5: Ablation study of Part-Aligned Attention. Without Part-Aligned Attention, ambiguous cross-view attention causes incorrect alignment across views, while our method yields correct results*

![[assets/figures/papers/paper_list_l2446_https_arxiv_org_abs_2511_21309/figures/008_Figure_6.jpg]]
*Figure 6: Ablation study on the Condition-Routed Attention. We compare textures generated with and without the proposed Condition-Routed Attention. The bottom-right inset shows the corresponding multi-view generation results, while the top-right inset illustrates the final textured mesh*

![[assets/figures/papers/paper_list_l2446_https_arxiv_org_abs_2511_21309/figures/001_Figure_1.jpg]]
*Figure 1: A collection of 3D objects textured by our method, demonstrating high-fidelity, seamless and geometry-aligned textures facilitated by our framework with geometry-calibrated attention. Visit our project website at https://calitex-project.github.io*

## 定位与知识库关联

### 问题背景与基线方法

当前3D纹理生成的主流范式基于多视角扩散模型，其核心瓶颈在于注意力机制的设计。现有方法普遍采用**不加区分的全注意力（full attention）**，导致两类内在歧义：(1) **跨视角歧义**——几何相似但语义不同的区域（如左右肢体）之间错误关注，产生纹理接缝与空间不一致；(2) **跨模态歧义**——噪声token在参考图像token与几何条件token之间交替关注，造成外观过拟合或几何过度依赖，最终纹理与几何错位。这一诊断构成CaliTex的出发点。

论文对比的基线方法包括四类开放源方案：**MV-Adapter**（Huang et al., ICCV 2025）、**UniTEX**（Liang et al., arXiv 2025）、**Step1X-3D**（Li et al., arXiv 2025）和**Hunyuan3D 2.1**（Tencent Hunyuan3D Team, arXiv 2025）。这些方法在注意力机制上均未显式嵌入三维结构感知，因此共享上述歧义问题。

### 核心差异：注意力机制的架构级校准

CaliTex的独特贡献在于**将几何一致性从后处理或额外监督提升为架构层面的固有行为**。具体而言，它在两个关键slot上改变了基线设计：

| 设计维度 | 基线方法 | CaliTex |
|---------|---------|---------|
| 跨视角注意力 | 所有视角间的完全注意力 | **Part-Aligned Attention (PAA)**：基于PartField将token按语义部件分组，仅在同一部件内计算跨视角注意力 |
| 跨模态注意力 | 噪声token与参考图像token直接交互 | **Condition-Routed Attention (CRA)**：双路径设计——condition-reference组融合几何与外观先验，noise-condition组注入几何感知特征 |
| 整体架构 | 单一阶段多视角注意力 | 两阶段扩散Transformer：Single-View DiT捕获视角内语义，Multi-View DiT通过PAA和CRA增强跨视角与跨模态一致性 |

**PAA的核心机制**：利用PartField将三维网格分解为K=20个语义部件，将每个token根据其对应图像块中像素的部件归属分配至对应组，然后在组内计算自注意力。这一约束消除了跨部件（如左右肢体）的错误对应。**CRA的核心机制**：通过双路径设计强制外观信息经由几何条件路由——condition-reference组首先融合几何与视觉先验，noise-condition组再从几何感知特征中提取信息，从而抑制直接复制参考图像的倾向。

### 方法谱系定位

CaliTex处于**几何感知注意力**这一新兴技术路线上。与依赖后处理优化（如纹理缝合、泊松融合）或增加额外监督信号（如多视角一致性损失）的方法不同，CaliTex通过在注意力计算中直接嵌入三维结构感知来解决问题。其技术渊源可追溯至：(1) 扩散Transformer（DiT）架构，特别是从**FLUX.1-Kontext**初始化的骨干网络；(2) PartField的语义部件分解技术；(3) 流匹配（flow matching）训练目标。

在知识库定位上，CaliTex属于**架构创新驱动的方法**——其增益并非来自更多数据或更大模型，而是来自对注意力机制的重新设计。这一设计哲学使得该方法具有较好的可迁移性：PAA和CRA作为即插即用的注意力模块，理论上可集成至其他基于多视角扩散的纹理生成框架中。

### 适用边界与局限

论文未明确报告方法的局限性，但基于方法设计可推断以下适用边界：

1. **对几何条件的依赖**：PAA和CRA均依赖PartField分解和几何条件输入，因此在几何条件质量较差或PartField分解不准确时，注意力校准的精度可能下降。这一推断需要在实际部署中验证。

2. **部件数量的敏感性**：PAA将网格固定分解为K=20个语义部件。对于部件数量远多于此的复杂物体，或部件边界模糊的有机体，分组策略可能需要调整。论文未提供K值的敏感性分析，这一点需要手动验证。

3. **计算开销**：两阶段DiT架构和双路径注意力设计引入了额外的计算成本。论文报告训练使用了8块GPU约600 GPU小时，但未与基线方法进行推理效率的定量对比。实际部署中的延迟和显存占用需要进一步评估。

4. **开放世界泛化**：训练数据来自Objaverse-XL和Texverse的80k物体，测试集包含Objaverse和游戏资产。对于训练分布之外的物体类别（如高度风格化的卡通角色、透明或半透明材质），方法的泛化能力尚未验证。

### 未解决的问题

论文未提出明确的开放问题，但基于方法设计可识别以下待探索方向：

- **动态部件分解**：当前PAA依赖预计算的静态PartField分解。能否学习自适应的、输入感知的部件分组，以适应更多样化的几何结构？
- **注意力校准与生成质量的权衡**：PAA通过限制注意力范围提升一致性，但可能牺牲长程外观建模能力。如何在局部一致性与全局外观保真度之间取得更优平衡？
- **扩展到视频或4D纹理**：当前方法针对静态3D物体。几何校准注意力的思想能否推广到时序一致的4D纹理生成？

## 原文 PDF

![[paperPDFs/CVPR_2026/CaliTex_Geometry_Calibrated_Attention_for_View_Coherent_3D_Texture_Generation.pdf]]
