---
title: "3D-LATTE: Latent Space 3D Editing from Textual Instructions"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/3D_LATTE_Latent_Space_3D_Editing_from_Textual_Instructions.pdf
project_link: "https://mparelli.github.io/3d-latte"
code_link: null
aliases:
- 3L
- 3LLS3EFTI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 在原生3D扩散模型的潜在空间中直接操作，并通过注入源对象的3D自注意力和交叉注意力图来引导编辑生成过程，从而避免2D视图间的不一致。
primary_logic: 3D注意力图编码了文本令牌与3D高斯之间的对应关系以及空间结构；将源对象的注意力图注入编辑去噪过程，可以在保持3D结构的同时实现语义对齐的编辑。
claims:
- 在CLIP Dir、CLIP Diff No-Edit和CLIP-Dir-Con三个指标上均取得最优结果
- 在GPTEval3D评估中，Prompt Alignment、3D Plausibility、Texture三项胜率均大幅领先基线方法
- 用户研究显示，在指令忠实度和视觉质量上，我们的方法获得了显著更高的投票比例
- 3D editing benchmark (edit scenarios) 上 CLIP Dir↑ = 0.178
---

# 3D-LATTE: Latent Space 3D Editing from Textual Instructions

> [!tip] 核心洞察
> 3D注意力图编码了文本令牌与3D高斯之间的对应关系以及空间结构；将源对象的注意力图注入编辑去噪过程，可以在保持3D结构的同时实现语义对齐的编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | 3D-LATTE：基于文本指令的潜在空间3D编辑 |
| 英文题名 | 3D-LATTE: Latent Space 3D Editing from Textual Instructions |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.00269) · [Project](https://mparelli.github.io/3d-latte) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | 3D-LATTE |
| Dataset | 3D editing benchmark, GPTEval3D |

> [!tip] 效果简介
> - 3D editing benchmark (edit scenarios) 上，CLIP Dir↑ 0.178。
> - 3D editing benchmark 上，CLIP Diff No-Edit↓ 0.039；CLIP-Dir-Con ↑ 0.77。
> - GPTEval3D 上，Prompt Alignment (win rate vs MVEdit) 87% vs 50% (+37%)。

## 概述

### 1. 问题背景与瓶颈

对3D资产进行语义编辑是内容创作的关键环节。现有方法大多依赖2D扩散先验，通过对多视图图像迭代编辑或蒸馏来实现3D编辑，如 **Instruct-NeRF2NeRF** (Haque et al., CVPR 2023)、**GaussianEditor** (Chen et al., CVPR 2023)、**Vox-E** (Sella et al., ICCV 2023) 等。然而，这种基于2D先验的范式存在根本性瓶颈：**多视图不一致**——各视角独立编辑后再融合，难以保证全局几何和外观的连贯性，常导致结果模糊、失真，甚至出现“多头”等严重伪影。

### 2. 核心方法定位

3D-LATTE 针对上述瓶颈，提出了一条**无需训练**的3D编辑路径：直接在**原生3D扩散模型的潜在空间**中进行操作，而非依赖2D先验的蒸馏或多视图拼接。其核心调控手段是**3D注意力注入**——在编辑去噪过程中，将源对象的3D自注意力和交叉注意力图注入生成过程，从而在保持3D结构的同时实现语义对齐的编辑。

具体而言，3D-LATTE 基于预训练的文本引导3D扩散模型 DiffSplat，将源3D对象表示为**多视图高斯溅射格**并反演至噪声潜在空间；随后以编辑提示引导去噪，同时注入源对象的3D注意力图。为提升编辑质量，方法还集成了几何正则化、频域退火和3D增强细化等辅助模块。

### 3. 关键结论

实验表明，3D-LATTE 在多项指标上显著优于现有基线：

- **CLIP评分**：在 CLIP Dir、CLIP Diff No-Edit 和 CLIP-Dir-Con 三项指标上均取得最优结果（Table 1）。
- **GPTEval3D评估**：在 Prompt Alignment 上对 MVEdit 胜率达 87%（+37%），对 Edit360 胜率达 67%；在 3D Plausibility 和 Texture 上同样大幅领先（Table 2）。
- **用户研究**：在指令忠实度和视觉质量上，3D-LATTE 获得了显著更高的投票比例（Figure 7）。

定性比较（Figure 5）和多样化编辑结果（Figure 6）进一步验证了方法在保持未编辑区域完整性的同时，实现高质量、多视图一致的3D编辑的能力。

## 背景与动机

3D内容的创建与编辑是计算机图形学和视觉计算中的核心任务，在游戏、影视、虚拟现实等领域有着广泛需求。近年来，随着文本到3D生成模型的快速发展，用户可以通过自然语言指令快速创建3D资产。然而，对已有3D对象进行精确、可控的语义编辑仍然是一个开放挑战——用户希望仅通过一句文本指令，就能改变对象的局部外观、替换部件或调整风格，同时保持未编辑区域的完整性和多视图几何一致性。

当前主流的3D编辑方法大多依赖2D扩散先验。典型范式包括：**Instruct-NeRF2NeRF**（Haque et al., CVPR 2023）和**Instruct-GS2GS**（Vachha et al., 2024）通过迭代数据集更新，利用InstructPix2Pix对多视图图像逐帧编辑后重建3D表示；**Vox-E**（Sella et al., ICCV 2023）在体素空间中进行文本引导编辑；**GaussCTRL**（Wu et al., ECCV 2024）引入深度条件来增强多视图一致性；**MVEdit**（Chen et al., arXiv 2024）则采用混合2D-3D策略，借助多视图扩散适配器进行编辑。这些方法的共同瓶颈在于：**编辑操作发生在2D图像空间，再将编辑结果蒸馏或融合到3D表示中，不可避免地引入多视图不一致**。当编辑涉及显著的几何变形或外观变换时，这种不一致会导致3D结果出现模糊、失真，甚至产生“多头”等严重伪影，难以实现全局一致的编辑效果。

这一瓶颈的根源在于：2D扩散先验本身缺乏对3D空间结构和多视图对应关系的显式建模。在2D视图中看似合理的编辑，在不同视角下可能产生冲突的几何解释，使得后续的3D融合过程难以调和。因此，一个自然的思路是：**直接在原生3D扩散模型的潜在空间中进行编辑操作**。原生3D扩散模型（如DiffSplat）将3D对象表示为多视图高斯溅射格（multi-view Gaussian splat grid），并在该潜在空间中进行扩散和去噪。这种表示天然编码了3D空间结构，为在编辑过程中保持几何一致性提供了基础。

3D-LATTE正是在这一思路下提出的。其核心洞察是：**3D扩散模型中的注意力图编码了文本令牌与3D高斯之间的语义对应关系以及空间结构信息**——交叉注意力图揭示了哪些高斯响应特定的文本令牌，自注意力图则捕获了高斯之间的空间亲和性（如Figure 3和Figure 4所示）。通过将源对象的3D注意力图注入编辑去噪过程，可以在保持源对象3D结构的同时，引导生成过程对齐编辑指令的语义，从而突破2D方法的多视图不一致瓶颈。基于这一洞察，3D-LATTE构建了一套完整的训练无关编辑框架，在潜在空间中实现全局一致的3D编辑。

## 核心创新

3D-LATTE 的核心创新在于将 3D 编辑从“2D 先验蒸馏 + 多视图重建”的间接范式，迁移到**原生 3D 扩散模型的潜在空间**中直接操作，从而从根本上解决 2D 方法固有的多视图不一致问题。这一范式转换通过四个关键的 changed slots 实现，每个 slot 都针对现有方法的瓶颈提供了因果性改进。

### 编辑空间：从 2D 投影到 3D 原生潜在空间

现有方法（如 **Instruct-NeRF2NeRF** (Haque et al., CVPR 2023)、**GaussianEditor** (Chen et al., CVPR 2023)、**Vox-E** (Sella et al., ICCV 2023)）普遍依赖 2D 扩散先验（如 InstructPix2Pix）对多视图图像进行独立编辑，再通过蒸馏或重建恢复 3D 一致性。这种“编辑-重建”分离的流程不可避免地引入视图间的纹理错位、几何失真甚至“多头”伪影。

3D-LATTE 直接在预训练 3D 扩散模型 **DiffSplat** 的潜在空间——即多视图高斯溅射格（multi-view Gaussian splat grid）——上进行编辑。源 3D 对象被表示为一组结构化的 3D 高斯原语，通过 DDPM 反演获得对应的噪声潜在编码，编辑去噪过程全程在 3D 域内完成，无需任何 2D 到 3D 的转换。这一设计使得编辑操作天然具有 3D 全局一致性，从根源上杜绝了视图间的不一致问题。

### 结构保持机制：3D 注意力注入

此前方法的结构保持主要依赖 2D 编辑后的多视图一致性约束或轨迹对齐（如 **Edit360** (Huang et al., ICCV 2025)），但这些约束是间接的、脆弱的。3D-LATTE 提出了**3D 注意力注入机制**，直接利用源对象在扩散去噪过程中产生的 3D 自注意力和交叉注意力图来引导编辑生成。

具体而言，交叉注意力图编码了文本令牌与 3D 高斯之间的语义对应关系。在编辑去噪时，对于源提示和编辑提示中共享的令牌（如描述对象类别或材质的词），3D-LATTE 将源对象的交叉注意力图注入编辑过程，确保这些语义区域的 3D 高斯分布保持一致。注入策略通过令牌对齐函数 $CT(j)$ 和时序阈值 $\tau_{\mathrm{cross}}$ 控制：

$$
\hat{W}_{\mathcal{G}_t}^{\mathrm{cross}} = F_{\mathrm{cross}}^{3D}(W_{\mathcal{G}}^{\mathrm{cross}}, (W_{\mathcal{G}}^*)^{\\mathrm{cross}}, t)_{i,j} = \begin{cases} ((W_{\mathcal{G}_t}^*)^{\\mathrm{cross}})_{i,j}, & \text{if } CT(j) = \mathcal{O} \text{ or } t < \tau_{\mathrm{cross}}, \\\\ (W_{\mathcal{G}_t}^{\\mathrm{cross}})_{i, CT(j)}, & \text{otherwise.} \end{cases}
$$

自注意力图则编码了 3D 高斯之间的空间结构关系（如不同部件间的相对位置和邻接关系）。在去噪早期时间步（$t < \tau_{\mathrm{self}}$），3D-LATTE 将源对象的自注意力图完全注入编辑过程：

$$
\hat{W_{\mathcal{G}_t}}^{\mathrm{self}} = F_{\mathrm{self}}^{3D}\left(W_{\mathcal{G}}^{\mathrm{self}}, (W_{\mathcal{G}}^*)^{\\mathrm{self}}, t\right) = \begin{cases} (W_{\mathcal{G}_t^*})^{\\mathrm{self}}, & \text{if } t < \tau_{\mathrm{self}}, \\\\ W_{\mathcal{G}_t^*}, & \text{otherwise.} \end{cases}
$$

这种双重注意力注入机制使得编辑能够在保留 3D 空间布局和部件结构的前提下，实现语义对齐的外观变换——这是 2D 方法无法达成的因果性优势。

### 几何正则化：主动维持编辑区域的空间完整性

现有方法通常缺乏对编辑区域几何质量的显式约束，导致编辑后的区域可能出现部分透明、收缩甚至消失的问题。3D-LATTE 引入**几何感知的正则化项**作为分类器引导信号，在去噪过程中主动惩罚编辑区域高斯的退化行为：

$$
\mathcal{L}_{\mathrm{geo}} = \lambda_o \sum_i R_t^i \cdot \exp(-\gamma_o \cdot o_i) + \lambda_{\Sigma} \sum_i R_t^i \cdot \exp(-\gamma_{\Sigma} \cdot \mathrm{Tr}(\Sigma_i))
$$

其中 $R_t^i$ 标识编辑区域的高斯，第一项惩罚低不透明度（$o_i$），第二项惩罚协方差矩阵迹过小（即高斯过度收缩）。该损失通过梯度引导去噪方向：

$$
z_{t-1} = \hat{z}_{t-1} - s \cdot \nabla_{z_t} \mathcal{L}_{\mathrm{geo}}(z_t)
$$

消融实验（Figure 9a）证实，移除该正则化后编辑区域会变得部分透明或完全消失，几何质量显著退化。

### 频率退火：抑制源纹理残留与噪声放大

在注意力注入过程中，源对象的高频纹理（如 Logo、复杂印花）可能被过度保留，导致编辑结果出现噪声纹理。3D-LATTE 提出**频域退火策略**，在 U-Net 跳跃连接特征图的傅里叶域进行调制：

$$
F^{\prime}(h_{l,t}) = F(h_{l,t}) \odot \beta_{l,t}
$$

其中 $\beta_{l,t}$ 控制各频段的保留比例，在去噪早期抑制高频分量，随时间步推进逐步引入精细细节。这一设计平衡了结构保持与纹理更新的矛盾——消融实验（Figure 9b）表明，移除频率退火后，源对象的复杂纹样会被模型过度强调，产生明显的噪声纹理。

### 创新总结

上述四个 changed slots 构成了一个完整的创新链条：**3D 原生潜在空间**提供了编辑的一致性基础，**3D 注意力注入**解决了结构保持与语义对齐的核心矛盾，**几何正则化**和**频率退火**分别从空间完整性和纹理质量两个维度弥补了注意力机制的不足。这一组合使得 3D-LATTE 在无需训练的条件下，首次实现了全局一致、语义精准的 3D 编辑。

## 整体框架

3D-LATTE 的整体流程围绕“在原生3D扩散模型的潜在空间中完成编辑”这一核心思想展开，其输入是一个已重建的3D资产（以多视图高斯溅射格 $\mathcal{G} = \{ G_i \}_{i=1}^{V}$ 表示）和一条用户指定的文本编辑指令，输出是编辑后的3D资产。整个 pipeline 由六个串行且相互协作的模块构成，如 **Figure 2** 所示。

![[assets/figures/papers/paper_list_l2034_https_arxiv_org_abs_2509_00269/figures/002_Figure_2.jpg]]
*Figure 2: Overview of 3D-LATTE. We operate in the latent space of a pre-trained 3D generative model. The source 3D object is represented as a multi-view Gaussian splat grid and inverted into its corresponding noise latent. Starting from this latent, we perform denoising guided by the edit prompt, while injecting 3D cross- and self-attention maps derived from the source object. A geometry regularization guidance term, a frequency modulation strategy and a 3D enhancement module further refine the result. Region-specific edits are supported via masks generated using GroundingDINO [29] and SAM2 [33]*

**流程概览。** 首先，源3D对象通过 **3D反演（3D Inversion）** 被编码到预训练3D扩散模型 **DiffSplat** 的噪声潜在空间中，得到对应的噪声潜在变量及编辑友好的噪声图 $\eta_t$。随后，在由编辑提示引导的去噪过程中，**3D注意力注入（3D Attention Injection）** 模块将源对象在去噪过程中产生的3D自注意力和交叉注意力图注入到编辑生成分支，以此在实现语义对齐编辑的同时保持源对象的3D结构与布局。对于局部编辑需求，**掩码生成与区域编辑（Mask Generation and Region Editing）** 利用 GPT-4o、GroundingDINO 和 SAM2 自动生成多视图一致的2D掩码，并将其升维为3D编辑掩码 $M$，再通过潜在变量混合公式 $\hat{z}_{t-1} = (1 - M) \odot z_{t-1} + M \odot z_{t-1}^*$ 将原始潜在与编辑潜在融合，实现仅编辑指定区域。

**质量保障与后处理。** 为抑制编辑过程中常见的几何退化问题，**几何正则化（Geometry Regularization）** 以分类器引导的形式施加几何感知损失 $\mathcal{L}_{\mathrm{geo}}$，对编辑区域内高斯的不透明度下降和空间收缩进行惩罚。同时，**频率退火（Frequency Annealing）** 在 U-Net 跳跃连接的特征图傅里叶域进行频谱调制，早期抑制高频分量以避免源对象复杂纹样被过度强调，后期逐步引入精细细节。最后，**3D增强细化（3D Enhancement Refinement）** 通过基于 ControlNet-Tile 的迭代数据集更新，仅在编辑区域恢复细节并锐化纹理，进一步提升视觉质量。

整个框架是免训练的（training-free），所有模块均作用于预训练好的 DiffSplat 模型之上，无需针对特定编辑任务进行微调。

## 核心模块与公式推导

3D-LATTE 的核心工作流建立在原生3D扩散模型 **DiffSplat** 的潜在空间之上。源3D对象首先被表示为一组多视角高斯溅射网格 $\mathcal{G} = \{ G_i \}_{i=1}^{V}$，其中每个高斯基元 $g_i \in \mathbb{R}^{12}$ 由RGB颜色、3D位置、尺度、旋转四元数和透明度参数化。编辑过程围绕六个关键模块展开，其技术链路如 Figure 2 所示。

### 3D反演

该模块将源3D对象编码至扩散模型的噪声潜在空间，为后续编辑提供起点。方法适配了DDPM反演机制，使其作用于多视角高斯溅射网格。反演过程沿前向扩散轨迹构建噪声图 $\eta_t$：

$$z_t = \sqrt{\alpha_t} z_0 + \sqrt{1 - \alpha_t} \epsilon_t, \quad \eta_t = \frac{(z_{t-1} - \mu_\theta(z_t, t))}{\sigma_t}$$

其中 $z_0$ 为源对象的潜在表示，$\epsilon_t$ 为标准高斯噪声，$\mu_\theta$ 和 $\sigma_t$ 分别为扩散模型的预测均值和方差调度参数。反演得到的噪声潜在 $z_T$ 成为编辑去噪过程的起始点。

### 3D注意力注入

这是实现编辑语义对齐与结构保持的核心机制。其关键洞察在于：3D交叉注意力图编码了文本令牌与3D高斯之间的对应关系，而自注意力图则捕获了高斯之间的空间结构依赖。在编辑提示的去噪过程中注入源对象的注意力图，可在保持3D布局的同时引导语义变换。

**交叉注意力注入**通过令牌对齐函数 $CT$ 实现，该函数将编辑提示 $p^*$ 中的令牌索引映射至源提示 $p$ 中的对应令牌索引：

$$\hat{W}_{\mathcal{G}_t}^{\mathrm{cross}} = F_{\mathrm{cross}}^{3D}(W_{\mathcal{G}}^{\mathrm{cross}}, (W_{\mathcal{G}}^*)^{\\mathrm{cross}}, t)_{i,j} = \begin{cases} ((W_{\mathcal{G}_t}^*)^{\\mathrm{cross}})_{i,j}, & \text{if } CT(j) = \mathcal{O} \text{ or } t < \tau_{\mathrm{cross}}, \\\\ (W_{\mathcal{G}_t}^{\\mathrm{cross}})_{i, CT(j)}, & \text{otherwise.} \end{cases}$$

其中 $\mathcal{O}$ 表示编辑提示中新增的令牌（无对应源令牌），$\tau_{\mathrm{cross}}$ 为时间阈值。对于共享令牌，注入源对象的注意力值以保持语义一致性；对于新增令牌，保留编辑提示的注意力以引入新语义。Figure 3 展示了不同令牌在3D溅射上的注意力分布，验证了令牌-高斯对应关系的有效性。

![[assets/figures/papers/paper_list_l2034_https_arxiv_org_abs_2509_00269/figures/003_Figure_3.jpg]]
*Figure 3: Per-token attention over 3D splats, rendered from multiple viewpoints*

**自注意力注入**仅在早期时间步（$t < \tau_{\mathrm{self}}$）应用，以在去噪初期建立稳固的3D结构骨架：

$$\hat{W_{\mathcal{G}_t}}^{\mathrm{self}} = F_{\mathrm{self}}^{3D}\left(W_{\mathcal{G}}^{\mathrm{self}}, (W_{\mathcal{G}}^*)^{\\mathrm{self}}, t\right) = \begin{cases} (W_{\mathcal{G}_t^*})^{\\mathrm{self}}, & \text{if } t < \tau_{\mathrm{self}}, \\\\ W_{\mathcal{G}_t^*}, & \text{otherwise.} \end{cases}$$

Figure 4 通过自注意力图的归一化拉普拉斯特征分解，将前三特征向量映射为高斯颜色，直观揭示了自注意力图编码的3D语义分割结构。

![[assets/figures/papers/paper_list_l2034_https_arxiv_org_abs_2509_00269/figures/004_Figure_4.jpg]]
*Figure 4: We form the normalized Laplacian of the 3D selfattention graph and map the first three eigenvectors to a color value per Gaussian*

### 掩码生成与区域编辑

为实现局部编辑，方法利用 **GPT-4o** 解析编辑指令中的目标区域，结合 **GroundingDINO** 和 **SAM2** 生成多视角一致的2D掩码，并将其升维为3D编辑掩码 $M$。编辑潜在 $z_{t-1}^*$ 与源潜在 $z_{t-1}$ 通过掩码混合：

$$\hat{z}_{t-1} = (1 - M) \odot z_{t-1} + M \odot z_{t-1}^*$$

### 几何正则化

编辑过程中，编辑区域的高斯可能出现透明度降低或空间收缩，导致几何退化。几何感知正则化损失作为分类器引导信号，在去噪步骤中施加约束：

$$\mathcal{L}_{\mathrm{geo}} = \lambda_o \sum_i R_t^i \cdot \exp(-\gamma_o \cdot o_i) + \lambda_{\Sigma} \sum_i R_t^i \cdot \exp(-\gamma_{\Sigma} \cdot \mathrm{Tr}(\Sigma_i))$$

其中 $R_t^i$ 标识高斯是否属于编辑区域，$o_i$ 为透明度，$\mathrm{Tr}(\Sigma_i)$ 为协方差矩阵的迹（度量空间扩展程度）。该损失惩罚编辑区域内低透明度和收缩的高斯，鼓励其保持充分的空间支持。去噪步骤更新为 $z_{t-1} = \hat{z}_{t-1} - s \cdot \nabla_{z_t} \mathcal{L}_{\mathrm{geo}}(z_t)$。

### 频率退火

U-Net跳跃连接传递的特征图包含不同频率的信息。频率退火策略在傅里叶域对这些特征图进行调制：

$$F^{\prime}(h_{l,t}) = F(h_{l,t}) \odot \beta_{l,t}$$

其中 $F$ 为傅里叶变换，$\beta_{l,t}$ 控制第 $l$ 层在时间步 $t$ 的各频段保留比例。早期去噪阶段抑制高频分量，防止源对象复杂纹样（如Logo）被过度强调而产生噪声纹理；后期逐步引入高频细节，恢复精细结构。

### 3D增强细化

作为后处理步骤，该模块通过迭代数据集更新和 **ControlNet-Tile** 超分，仅在编辑区域应用增强，恢复细节并锐化纹理，同时保持3D几何不变。

## 实验与分析

### 核心定量结果

3D-LATTE在标准化3D编辑基准上进行了全面评估，与8个基线方法进行了对比。**Table 1** 报告了三个CLIP指标的结果，我们的方法在所有指标上均取得最优：

![[assets/figures/papers/paper_list_l2034_https_arxiv_org_abs_2509_00269/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison using CLIP score metrics. Best , second-best and third-best results are indicated*

- **CLIP Dir↑**：0.178，衡量编辑结果与目标文本的语义对齐程度，表明3D-LATTE在指令忠实度上显著领先。
- **CLIP Diff No-Edit↓**：0.039，衡量编辑对非目标区域的干扰程度，说明我们的注意力注入机制有效保护了源对象的未编辑部分。
- **CLIP-Dir-Con↑**：0.77，作为方向性与内容保持的综合指标，反映了编辑质量与结构保真度之间的良好平衡。

在**GPTEval3D**评估（**Table 2**）中，我们进一步验证了3D编辑的多维度质量。与最强基线MVEdit相比，3D-LATTE在Prompt Alignment上取得87%的胜率（+37%），在3D Plausibility上取得71%的胜率，在Texture质量上取得70%的胜率。与Edit360相比，Prompt Alignment胜率为67%。这些结果表明，基于原生3D扩散模型潜在空间的操作在几何一致性和纹理质量上具有系统性优势。

### 用户研究

**Figure 7** 展示了用户研究结果。参与者在指令忠实度和视觉质量两个维度上进行二选一判断，3D-LATTE在两个维度上均获得了显著更高的投票比例。这验证了自动指标无法完全捕捉的主观质量维度——用户更偏好我们方法生成的编辑结果。

### 消融实验

我们系统性地消融了三个核心设计组件：

**几何正则化（Geometry Regularization）**：如**Figure 9(a)**所示，移除几何正则化损失后，编辑区域出现部分透明或完全消失的现象。该损失通过惩罚编辑区域内高斯的低不透明度和空间收缩，维持了编辑区域的几何稳定性。定量上，缺少该模块会导致3D Plausibility显著下降。

**频率退火（Frequency Annealing）**：**Figure 9(b)**展示了移除频率退火的影响。源对象中复杂的高频纹样（如Logo、印花）会被模型过度强调，产生噪声纹理并干扰编辑语义。频率退火通过在U-Net跳跃连接的特征图傅里叶域进行调制，早期抑制高频分量、后期逐步引入细节，有效避免了源纹理对编辑结果的污染。

**3D增强模块（3D Enhancement Refinement）**：**Figure 8**展示了增强模块的效果。该模块基于ControlNet-Tile进行迭代的3D超分细化，仅在编辑区域应用，能够恢复精细细节并锐化纹理，同时保持3D几何结构不变。消融结果显示，缺少该模块时编辑结果的纹理清晰度和细节丰富度明显下降。

### 定性分析

**Figure 5** 提供了与多个基线方法的定性比较。在处理"将汽车变为敞篷车""给雕像戴上墨镜"等多样化编辑指令时，3D-LATTE能够生成几何一致、纹理清晰的结果，而非编辑区域保持完整。相比之下，基于2D先验的方法（如Instruct-NeRF2NeRF、GaussianEditor）在多视图渲染时容易出现纹理模糊、几何失真或"多头"伪影。

**Figure 6** 展示了更多定性结果，涵盖材质替换、部件增减、风格迁移等多种编辑类型，验证了方法的通用性。

### 失败模式与局限性

尽管3D-LATTE在整体性能上表现优异，但在以下场景中仍存在挑战：当编辑指令涉及大幅度的拓扑变化（如将闭合物体变为开放结构）时，几何正则化可能不足以约束生成过程，导致几何退化。此外，编辑质量依赖于底层3D扩散模型DiffSplat的表达能力，对于训练分布之外的极端编辑，结果可能出现语义偏差。这些失败模式在消融实验中已部分体现，进一步改进需要更强大的3D生成先验或自适应正则化策略。

### 补充图表

![[assets/figures/papers/paper_list_l2034_https_arxiv_org_abs_2509_00269/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison with baselines. Our approach achieves the most plausible edits wrt. the input instruction text, while preserving the unedited parts of the 3D objects*

![[assets/figures/papers/paper_list_l2034_https_arxiv_org_abs_2509_00269/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative Results. Our method yields high-quality 3D objects for a diverse set of edits*

![[assets/figures/papers/paper_list_l2034_https_arxiv_org_abs_2509_00269/figures/009_Figure_7.jpg]]
*Figure 7: User study. Our approach shows a significantly higher percentage of votes in instruction faithfulness and visual quality*

![[assets/figures/papers/paper_list_l2034_https_arxiv_org_abs_2509_00269/figures/008_Figure_8.jpg]]
*Figure 8: Effect of 3D enhancement*

![[assets/figures/papers/paper_list_l2034_https_arxiv_org_abs_2509_00269/figures/010_Figure_9.jpg]]
*Figure 9: Effect of our proposed additional components*

## 方法谱系与知识库定位

### 核心瓶颈与因果杠杆

3D编辑领域的根本瓶颈在于**多视图一致性**：基于2D扩散先验蒸馏或多视图图像编辑的方法（如**Instruct-NeRF2NeRF** (Haque et al., CVPR 2023)、**GaussianEditor** (Chen et al., CVPR 2023)、**Instruct-GS2GS** (Vachha et al., 2024)）在几何和外观变换时，因各视图独立处理而产生模糊、失真甚至“多头”等伪影，难以实现全局一致的3D编辑。

3D-LATTE的因果杠杆是**将编辑操作从2D像素/图像空间迁移到原生3D扩散模型的潜在空间**。该方法在预训练3D生成模型DiffSplat的噪声潜在空间中直接操作，绕开了2D视图间的一致性难题。其核心洞察在于：3D交叉注意力图编码了文本令牌与3D高斯之间的语义对应关系，而3D自注意力图则编码了高斯之间的空间结构关系——将源对象的这些注意力图注入编辑去噪过程，可以在保持3D几何结构的同时实现语义对齐的编辑。

### 方法谱系中的定位

3D-LATTE位于**原生3D潜在空间编辑**这一新兴范式，与现有方法形成清晰的方法论断层：

| 编辑范式 | 代表方法 | 编辑空间 | 一致性保障机制 |
|---------|---------|---------|--------------|
| 迭代数据集更新 | **Instruct-NeRF2NeRF** (Haque et al., CVPR 2023) | 2D图像空间 | 逐视图独立编辑，隐式依赖NeRF重建 |
| 2D先验引导3D编辑 | **Vox-E** (Sella et al., ICCV 2023)、**GaussCTRL** (Wu et al., ECCV 2024) | 2D扩散先验+体素/高斯表示 | 深度条件或轨迹对齐 |
| 多视图扩散适配 | **MVEdit** (Chen et al., arXiv 2024) | 2D多视图扩散+3D表示 | 多视图扩散适配器 |
| 密集视图合成 | **Edit360** (Huang et al., ICCV 2025) | 密集视图合成+轨迹对齐 | 视图间轨迹一致性 |
| 前馈3D编辑 | **Preditor3D** (Erkoc et al., CVPR 2024) | 3D形状潜空间 | 端到端前馈网络 |
| **原生3D潜在空间编辑** | **3D-LATTE** | **3D扩散模型潜在空间** | **3D注意力图注入+几何正则化+频域退火** |

### 关键差异维度

1. **编辑空间**：与所有基线方法不同，3D-LATTE在原生3D扩散模型的潜在空间（多视图高斯溅射格）中操作，避免了2D-3D转换中的信息损失和一致性误差。

2. **结构保持机制**：基线方法依赖多视图一致性约束或轨迹对齐，而3D-LATTE通过注入源对象的3D自注意力和交叉注意力图来保持布局和结构（Eq. 2-3），这是一种训练无关的、在去噪过程中直接传递结构信息的方式。

3. **几何正则化**：3D-LATTE引入几何感知的惩罚项（Eq. 5），对编辑区域中低不透明度和收缩的高斯进行惩罚，鼓励编辑区域保持空间支持。消融实验表明，移除该正则化会导致编辑区域部分透明或完全消失（Figure 9a），而基线方法通常缺乏此类显式的3D几何约束。

4. **频率处理**：通过傅里叶域的频段调制，早期抑制高频分量以避免源对象复杂纹样的过度强调，后期逐步引入精细细节。消融实验证实，移除频域退火会使Logo等高频图案被过度强调，产生噪声纹理（Figure 9b）。

5. **后处理细化**：基于ControlNet-Tile的迭代3D增强模块仅在编辑区域应用，恢复细节并锐化纹理，同时保持3D几何（Figure 8）。这是基线方法普遍缺失的环节。

### 适用边界

- **适用场景**：3D-LATTE适用于需要对3D资产进行文本驱动的语义编辑的场景，包括外观变换（如材质、颜色、纹理）和几何变换（如添加/移除部件、形状变形），支持全局编辑和基于掩码的区域编辑。
- **技术前提**：方法依赖预训练的3D扩散模型DiffSplat，编辑能力受限于该生成模型的表达空间。掩码生成依赖GPT-4o、GroundingDINO和SAM2等多模型流水线。
- **评估指标局限**：自动指标（CLIP Dir、CLIP Diff No-Edit）可能无法完全替代人类对3D编辑质量的主观评判，尽管用户研究（Figure 7）和GPTEval3D评估（Table 2）提供了补充验证。

### 局限与开放问题

论文未明确列出方法局限，但基于方法论分析可推断以下潜在边界：

1. **编辑幅度约束**：注意力图注入机制在早期时间步强制保持源对象结构，可能限制大幅度几何变换的能力。当编辑指令要求根本性结构改变时，结构保持与编辑忠实度之间存在内在张力。

2. **生成模型依赖性**：方法效果高度依赖底层3D扩散模型的生成质量和潜在空间表达能力。DiffSplat的训练数据分布决定了可编辑的对象类别和编辑类型范围。

3. **多模型流水线复杂性**：掩码生成涉及GPT-4o、GroundingDINO、SAM2等多个模型，增加了系统复杂性和潜在故障点。多视图掩码一致性是区域编辑成功的关键前提，但论文未深入讨论掩码不一致时的鲁棒性处理。

4. **开放问题**：需要进一步研究的内容包括——如何将注意力注入机制推广到其他3D生成架构，如何在保持结构的同时支持更激进的几何变换，以及如何减少对外部掩码模型的依赖。

## 原文 PDF

![[paperPDFs/CVPR_2026/3D_LATTE_Latent_Space_3D_Editing_from_Textual_Instructions.pdf]]