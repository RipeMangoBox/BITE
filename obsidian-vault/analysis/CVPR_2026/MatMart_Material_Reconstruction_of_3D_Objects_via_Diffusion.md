---
title: "MatMart: Material Reconstruction of 3D Objects via Diffusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MatMart_Material_Reconstruction_of_3D_Objects_via_Diffusion.pdf
project_link: null
code_link: "https://github.com/mseitzer/pytorch-fid"
aliases:
- MatMart
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用两阶段渐进式推理框架，结合视图-材质交叉注意力（VMCA）保持多视图一致性，并将材质预测与生成统一于端到端优化的单一扩散模型中。
primary_logic: 将材质重建解耦为基于输入的准确预测和基于先验的未观察区域生成两个阶段，利用渐进推理和VMCA实现O(1)空间复杂度的多视图一致，并在视图空间而非UV空间进行生成以利用更丰富的语义信息，避免引入额外预训练模型。
claims:
- 在单视图和多视图设置下，MatMart在Albedo SSIM、PSNR、Metallic/Roughness MSE以及渲染FID/LPIPS上均显著优于MaterialMVP等现有方法，定量结果支持提出的两阶段快速材质重建有效性。
- 使用视图-材质交叉注意力（VMCA）将跨视图一致性维护的空间复杂度从O(N^2)降为O(1)，使得模型可以处理任意数量高分辨率输入，消融实验证实移除VMCA会导致预测不一致和质量下降。
- 在生成阶段使用材质先验（来自第一阶段预测）显著提升生成结果一致性，消融实验表明无先验条件下生成混乱，渲染质量下降。
- Objaverse subset (single-view) 上 Albedo SSIM↑ = 0.931
---

# MatMart: Material Reconstruction of 3D Objects via Diffusion

> [!tip] 核心洞察
> 将材质重建解耦为基于输入的准确预测和基于先验的未观察区域生成两个阶段，利用渐进推理和VMCA实现O(1)空间复杂度的多视图一致，并在视图空间而非UV空间进行生成以利用更丰富的语义信息，避免引入额外预训练模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | MatMart：基于扩散模型的3D物体材质重建 |
| 英文题名 | MatMart: Material Reconstruction of 3D Objects via Diffusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18900) · [Code](https://github.com/mseitzer/pytorch-fid) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MatMart |
| Dataset | Objaverse subset |

> [!tip] 效果简介
> - Objaverse subset (single-view) 上，Albedo SSIM↑ 0.931 vs 0.901 (MaterialMVP) (+0.030)；Albedo PSNR↑ 29.89 vs 27.57 (MaterialMVP) (+2.32)；Metallic MSE↓ 0.017 vs 0.026 (MaterialMVP) (-0.009)。
> - Objaverse subset (multi-view) 上，Albedo SSIM↑ 0.945 vs 0.902 (MaterialMVP) (+0.043)；Albedo PSNR↑ 32.10 vs 27.61 (MaterialMVP) (+4.49)；Metallic MSE↓ 0.015 vs 0.026 (MaterialMVP) (-0.011)。

## 概要

**问题瓶颈**：现有3D材质重建方法普遍面临一个核心矛盾——难以在保持输入图像细节的同时灵活处理任意数量的高分辨率视图。主流方案往往依赖多个预训练模型级联（如**Material Anything**, Huang et al., CVPR 2025），导致训练部署复杂、稳定性不足；而基于全局交叉注意力的多视图一致性机制（如**MaterialMVP**, He et al., ICCV 2025）则面临空间复杂度$O(N^2)$的扩展性瓶颈。

**核心结论**：MatMart提出了一种**两阶段渐进式推理框架**，将材质重建解耦为“基于输入的准确预测”与“基于先验的未观察区域生成”两个阶段，并统一于端到端优化的单一扩散模型中。其关键创新在于**视图-材质交叉注意力（VMCA）**机制，通过固定目标视图与参考视图的注意力计算，将多视图一致性的空间复杂度从$O(N^2)$降至$O(1)$，使模型可处理任意数量的高分辨率输入。

**方法定位**：与在UV空间直接生成的方案（如**TexGEN**, Yu et al., TOG 2024）不同，MatMart选择在**视图空间**进行材质生成，利用更丰富的语义信息，并通过自适应视图选择和材质先验引导确保生成质量。这一设计使其在方法谱系中处于“预测-生成联合优化”的交叉地带，既区别于纯预测方法（如**NvDiffRec**, Munkberg et al., CVPR 2022），也区别于依赖额外预训练模型的生成方案。

**主要结果**：在多视图设置下，MatMart（1024×1024）的Albedo SSIM达到0.945、PSNR达到32.10，较MaterialMVP分别提升0.043和4.49；渲染FID从38.00降至26.20，LPIPS从0.088降至0.052。消融实验证实，移除VMCA会导致视图间预测不一致，而去除材质先验则使生成结果跨视图差异显著增大，验证了各组件的关键作用。

高质量材质（反照率、金属度、粗糙度）是逼真3D物体渲染与重光照的核心要素。从单张或多张RGB图像中重建物理渲染（PBR）材质，始终面临着**输入信息不足与材质分解歧义**的双重挑战。近年来，基于深度学习的材质估计方法取得了显著进展，但现有工作仍存在若干关键瓶颈。

**现有方法的局限。** 当前主流方案大致分为两类。一类方法依赖多个预训练模型的级联，如 **Material Anything**（Huang et al., CVPR 2025）将预训练RGB生成模型与材质预测模型串联，导致训练部署复杂、稳定性不足。另一类方法如 **MaterialMVP**（He et al., ICCV 2025）虽然实现了端到端训练，但其多视图一致性机制采用全局交叉注意力，需联合处理所有视图，空间复杂度达到 $O(N^2)$，严重限制了可处理的输入视图数量与分辨率。此外，**TexGEN**（Yu et al., TOG 2024）等生成式方法直接在UV空间进行材质生成，由于UV空间缺乏视图空间中的丰富语义信息，生成质量与纹理-几何对齐度均受到制约。

**核心瓶颈。** 综合来看，现有材质重建方法面临一个根本性困境：难以在保持输入图像细节保真度的同时，灵活处理任意数量的高分辨率视图，并且普遍依赖多模型级联带来的复杂工程与不稳定风险。

**本文动机。** 针对上述问题，MatMart 提出了一种**两阶段渐进式推理框架**，将材质重建解耦为“基于输入的准确预测”与“基于先验的未观察区域生成”两个阶段，并将预测与生成统一于**单一扩散模型**中端到端优化。其核心创新在于：通过**视图-材质交叉注意力（VMCA）**将多视图一致性的空间复杂度从 $O(N^2)$ 降至 $O(1)$，使模型能够处理任意数量的高分辨率输入；同时将材质生成从UV空间迁移至语义信息更丰富的**视图空间**，并利用第一阶段预测的材质先验引导生成过程，从而在无需额外预训练模型的前提下实现高质量、高一致性的材质重建。

## 核心方法与创新机理

MatMart 的核心创新在于将材质重建任务解耦为**两阶段渐进式推理框架**，并通过**视图-材质交叉注意力（VMCA）** 与**视图空间生成**两个关键机制，系统性地解决了现有方法在多视图一致性、输入灵活性与模型复杂度上的瓶颈。

### 1. 从 O(N²) 到 O(1)：视图-材质交叉注意力（VMCA）

现有材质重建方法在处理多视图输入时，通常采用全局交叉注意力联合处理所有视图，其空间复杂度随视图数量 N 呈平方增长（O(N²)），严重限制了可处理的分辨率与视图数量。MatMart 提出的 VMCA 机制从根本上改变了这一范式：

- **渐进式推理策略**：模型逐帧处理输入视图，每次仅使用当前目标视图与一个参考视图进行交互，而非一次性联合处理所有视图。
- **单向信息传递设计**：VMCA 的核心公式为：

$$
\mathbf{Z} = \left( \mathrm{Softmax} \left( \frac{\mathbf{Q}_{\mathrm{Tgt}} \cdot \mathbf{K}_{\mathrm{Tgt+Ref}}^{T}}{\sqrt{d}} \right) \cdot \mathbf{V}_{\mathrm{Tgt+Ref}} \right) \oplus \mathbf{V}_{\mathrm{Ref}}
$$

其中目标视图作为 Query，拼接的目标与参考视图作为 Key/Value，注意力输出再与参考视图的 Value 级联。参考视图不作为 Query 参与注意力计算，确保了信息仅从参考视图单向流向目标视图，而非双向交互。

- **O(1) 空间复杂度**：由于推理过程中目标视图与参考视图的数量固定，VMCA 的空间复杂度恒为 O(1)，使得 MatMart 能够处理**任意数量高分辨率输入视图**。消融实验证实，移除 VMCA 后视图间材质预测出现明显不一致，定量指标显著下降（Fig. 3, Fig. 8）。

### 2. 视图空间生成 vs. UV 空间生成

传统材质生成方法（如 **TexGEN** (Yu et al., TOG 2024)）直接在 UV 空间进行纹理补全，但 UV 空间缺乏丰富的语义信息，导致生成质量受限。MatMart 选择在**视图空间**进行材质生成，利用视角下的语义上下文信息提升生成质量（Fig. 5 对比验证了 UV 空间生成的质量瓶颈）。

为将视图空间生成结果有效融合到 UV 纹理，MatMart 设计了**交替烘焙与分组生成**策略：

$$
\mathbf{T} = \frac{\mathbf{T}' \cdot \mathbf{W}' + \mathbf{T} \cdot \mathbf{W}}{\mathbf{W}' + \mathbf{W}}, \quad \mathbf{W}' = \mathbf{S}'^{\lambda}
$$

新生成的纹理 $\mathbf{T}'$ 与现有纹理 $\mathbf{T}$ 按权重加权混合，权重 $\mathbf{W}'$ 基于法线与相机轴余弦相似度的幂次计算，确保高置信度区域贡献更大。同时采用**自适应视图选择**，基于 UV 纹理覆盖度贪婪地选择生成用视图，提高效率。

### 3. 单一扩散模型统一预测与生成

现有方法（如 **Material Anything** (Huang et al., CVPR 2025)）通常依赖多个预训练模型级联（RGB 生成模型 + 材质预测模型），训练部署复杂且稳定性不足。MatMart 采用**单一扩散模型**同时完成材质预测与生成，通过端到端优化使模型同时具备两种能力。该统一架构集成了跨分量注意力、VMCA 和文本提示控制，避免了引入额外预训练模型带来的工程复杂度。

### 4. 材质先验引导的渐进式生成

在第二阶段生成中，MatMart 将第一阶段预测的材质结果作为**材质先验**输入生成模型，为未观察区域提供强约束。消融实验表明，移除材质先验后仅靠几何先验生成的结果跨视图差异显著，导致材质混乱、渲染质量下降（Fig. 9, Tab. 2）。这一设计将生成任务从“无中生有”转化为“基于可靠先验的补全”，显著提升了多视图生成的一致性。

**总结**：MatMart 通过 VMCA 实现 O(1) 复杂度的多视图一致预测，通过视图空间生成利用丰富语义信息，通过单一扩散模型简化架构，通过材质先验约束生成一致性，四个 changed slots 协同构成了其相对于 MaterialMVP、TexGEN 等基线方法的核心优势。

MatMart 将材质重建任务解耦为两个渐进式阶段，并在单一扩散模型中统一完成预测与生成，避免了多模型级联带来的训练复杂性。

### 两阶段渐进式推理

核心洞察在于：输入视图覆盖的区域需要**精确的材质预测**，而未观察或被遮挡的区域则需借助**材质先验进行生成**。基于此，MatMart 将流程划分为：

1. **阶段一：渐进式材质估计 (Progressive Material Estimation)**  
   对输入图像逐帧进行材质预测。为保证多视图间的一致性，引入**视图-材质交叉注意力 (VMCA)**，使目标视图在预测时可单向参考已处理视图的信息。预测结果随即被烘焙至 UV 纹理空间，作为阶段二的先验。

2. **阶段二：先验引导的材质生成 (Prior-guided Material Generation)**  
   利用阶段一的材质先验与几何先验（法线等），在**视图空间**中交替进行材质生成与纹理烘焙，逐步补全 UV 纹理中缺失的区域。视图空间相比 UV 空间具有更丰富的语义信息，有利于生成高质量结果。

### 统一扩散模型架构

两阶段的任务——材质预测与材质生成——被集成于**同一个扩散模型**中，通过端到端优化同时具备两种能力。模型基于 Stable Diffusion 架构，集成了以下关键组件：

- **跨分量注意力 (Cross-Component Attention)**：处理 Albedo、Roughness、Metallic 等多通道材质分量间的关联。
- **视图-材质交叉注意力 (VMCA)**：在渐进推理中维持多视图一致性，空间复杂度为 O(1)。
- **文本提示控制**：通过文本嵌入引导材质风格。

### 关键数据流

1. **输入**：任意数量的 RGB 视图及其对应的几何信息（法线、深度等）。
2. **阶段一数据流**：  
   `RGB视图 → 渐进式材质预测 (VMCA) → UV烘焙 → 材质先验纹理`
3. **阶段二数据流**：  
   `材质先验 + 几何先验 → 自适应视图选择 → 视图空间生成 (扩散模型) → 交替烘焙 → 完整UV材质纹理`
4. **输出**：完整的 PBR 材质贴图（Albedo、Roughness、Metallic），可直接用于渲染。

### 与现有方法的架构差异

| 设计维度 | 现有方法 | MatMart |
|---------|---------|---------|
| 多视图一致性 | 全局交叉注意力，复杂度 O(N²) | 渐进式推理 + VMCA，复杂度 O(1) |
| 生成空间 | UV 空间直接生成（如 **TexGEN** (Yu et al., TOG 2024)） | 视图空间生成，语义信息更丰富 |
| 模型架构 | 多模型级联（如 **Material Anything** (Huang et al., CVPR 2025) 使用预训练 RGB 生成模型 + 材质预测模型） | 单一扩散模型端到端优化 |

这种统一架构使得 MatMart 能够灵活处理任意数量的高分辨率输入视图，同时保持训练与部署的简洁性。

![[assets/figures/papers/paper_list_l2543_https_arxiv_org_abs_2511_18900/figures/002_Figure_2.jpg]]
*Figure 2: Method overview. Our framework, MatMart, divides the material reconstruction task into two stages. In the first stage, progressive material prediction is performed on the input images, and the predicted results are baked into the UV space. In the second stage, prior-guided material generation and texture baking are alternately conducted for unobserved and occluded regions. Both prediction and generation tasks are unified within a single diffusion model and can be accomplished through end-to-end optimization*

MatMart 将材质重建任务分解为两个阶段，并通过一个统一的扩散模型完成端到端优化。其核心设计围绕三个关键模块展开：**渐进式材质估计**、**视图-材质交叉注意力（VMCA）** 以及**先验引导的材质生成**。

### 渐进式材质估计与视图-材质交叉注意力（VMCA）

在第一阶段，MatMart 对输入图像逐帧进行材质预测。与以往方法将所有视图联合处理、导致空间复杂度为 $O(N^2)$ 的全局交叉注意力不同，MatMart 引入了**视图-材质交叉注意力（VMCA）**，将多视图一致性的维护成本降至 $O(1)$。这一设计使得模型可以处理任意数量的高分辨率输入视图，而不会遭遇显存爆炸问题。

VMCA 的核心机制在于其单向信息传递结构。在渐进推理过程中，每一轮仅处理一个**目标视图**和一个固定的**参考视图**。参考视图的信息被单向注入目标视图的潜在特征中，而参考视图本身不受目标视图的影响。其注意力操作定义为：

$$\mathbf{Z} = \left( \mathrm{Softmax} \left( \frac{\mathbf{Q}_{\mathrm{Tgt}} \cdot \mathbf{K}_{\mathrm{Tgt+Ref}}^{T}}{\sqrt{d}} \right) \cdot \mathbf{V}_{\mathrm{Tgt+Ref}} \right) \oplus \mathbf{V}_{\mathrm{Ref}}$$

其中，$\mathbf{Q}_{\mathrm{Tgt}}$ 为目标视图的 Query，$\mathbf{K}_{\mathrm{Tgt+Ref}}$ 和 $\mathbf{V}_{\mathrm{Tgt+Ref}}$ 分别为目标视图与参考视图拼接后的 Key 和 Value。注意力输出与参考视图的 Value $\mathbf{V}_{\mathrm{Ref}}$ 进行级联（$\oplus$），形成最终的特征 $\mathbf{Z}$。由于目标视图和参考视图的数量在推理过程中固定，整体空间复杂度保持为 $O(1)$。消融实验证实，移除 VMCA 会导致不同视图间的材质预测出现显著不一致，验证了该模块对多视图一致性的关键作用。

### 先验引导的材质生成与交替烘焙

第二阶段的目标是对第一阶段未观察或被遮挡的区域进行材质补全。MatMart 选择在**视图空间**而非 UV 空间进行生成，其依据是 UV 空间语义信息较弱，现有方法在此空间直接生成时质量不佳。为了在视图空间生成的同时保持全局一致性，该阶段引入了两个关键设计：**材质先验引导**和**交替烘焙与分组生成**。

在每一轮生成中，模型以第一阶段预测并烘焙至 UV 空间的材质作为**材质先验**，同时结合几何先验（法线图），从选定的视点渲染出部分填充的材质图作为条件输入。生成的新材质通过加权混合的方式更新至 UV 纹理：

$$\mathbf{T} = \frac{\mathbf{T}' \cdot \mathbf{W}' + \mathbf{T} \cdot \mathbf{W}}{\mathbf{W}' + \mathbf{W}}, \quad \mathbf{W}' = \mathbf{S}'^{\lambda}$$

其中 $\mathbf{T}'$ 为新生成的纹理，$\mathbf{T}$ 为现有纹理，权重 $\mathbf{W}'$ 基于该像素处法线与相机轴夹角的余弦相似度 $\mathbf{S}'$ 的 $\lambda$ 次幂计算，使得更正面朝向相机的区域获得更高权重。权重随后累积更新：$\mathbf{W} \gets \mathbf{W}' + \mathbf{W}$。这种“边生成边烘焙”的策略确保最新生成结果能即时融入全局纹理，指导后续视图的生成。消融实验表明，移除材质先验会导致跨视图生成结果混乱、渲染质量显著下降；而跳过第一阶段的烘焙直接生成，则会损失纹理细节，降低重建质量。

## 实验与关键发现

### 主实验：单视图与多视图材质重建

MatMart 在 Objaverse 子集上进行了单视图与多视图两种设定下的定量评估，对比方法包括 **MaterialMVP**（He et al., ICCV 2025）、**Material Anything**（Huang et al., CVPR 2025）、**Paint3D**（Zeng et al., CVPR 2024）、**TexGEN**（Yu et al., TOG 2024）和 **NvDiffRec**（Munkberg et al., CVPR 2022）。评估指标覆盖材质图质量（Albedo SSIM/PSNR、Metallic/Roughness MSE）以及渲染质量（FID/LPIPS）。

**Table 1** 给出了完整量化结果。在多视图设定下，MatMart（1024×1024 分辨率）在所有指标上均取得最优：Albedo SSIM 达到 0.945（对比 MaterialMVP 的 0.902，提升 0.043），PSNR 达到 32.10（对比 27.61，提升 4.49 dB）；Metallic MSE 降至 0.015，Roughness MSE 降至 0.008；渲染 FID 大幅降至 26.20（对比 MaterialMVP 的 38.00，降低 11.80），LPIPS 降至 0.052。单视图设定下优势保持：Albedo SSIM 0.931 vs. 0.901，PSNR 29.89 vs. 27.57，渲染 FID 31.49 vs. 38.27。

定性对比（Figure 5、Figure 6）显示，MatMart 恢复的反照率更忠实于真值，粗糙度和金属度估计更准确，渲染结果与真值的一致性明显优于对比方法。在真实世界数据 Stanford-ORB 上的定性对比（Figure 7）进一步验证了方法的泛化能力。

![[assets/figures/papers/paper_list_l2543_https_arxiv_org_abs_2511_18900/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison of single-view input. Our method recovers more accurate materials across various types of objects, thereby achieving rendering results that are more consistent with the ground truth. From left to right are albedo, roughness, and metallic*

![[assets/figures/papers/paper_list_l2543_https_arxiv_org_abs_2511_18900/figures/008_Figure_7.jpg]]
*Figure 7: Qualitative comparison on real-world data Stanford-ORB [19]. From top to bottom: albedo, roughness, and metallic*

### 消融实验

消融实验在**多视图输入**设定下进行，检验三个关键设计的作用（Table 2）：

**1. 视图-材质交叉注意力（VMCA）的移除。**
移除 VMCA 后，模型在渐进式材质估计中失去跨视图一致性约束。如 Figure 3 所示，无 VMCA 时同一物体的不同视图预测出现明显不一致（如桶的反照率和粗糙度在不同视角下差异显著）。定量上，Albedo SSIM 和 PSNR 均下降，渲染 FID/LPIPS 恶化，证实 VMCA 是维持多视图一致性的关键机制。其核心优势在于将空间复杂度从 O(N²) 降至 O(1)，使模型可处理任意数量高分辨率输入。

**2. 材质先验的移除。**
在第二阶段生成中，若不使用第一阶段预测的材质先验，仅依赖几何先验（法线等），生成结果跨视图差异增大，材质出现混乱。Figure 9 展示了无材质先验条件下生成的反照率和粗糙度在不同视角间缺乏一致性，导致最终渲染质量下降。定量指标同样出现退化，验证了材质先验对渐进式生成一致性的保障作用。

![[assets/figures/papers/paper_list_l2543_https_arxiv_org_abs_2511_18900/figures/010_Figure_9.jpg]]
*Figure 9: Material priors ablations. Material priors ensure the consistency for progressive generation*

**3. 阶段一烘焙的跳过。**
跳过第一阶段材质预测后的 UV 烘焙，直接进行第二阶段生成，会导致纹理细节损失。Figure 10 显示，无阶段一烘焙时重建结果在纹理锐度和细节保真度上均有下降，定量指标也相应降低。这说明将预测结果及时烘焙至 UV 空间，对后续生成阶段的信息传递和质量保持至关重要。

![[assets/figures/papers/paper_list_l2543_https_arxiv_org_abs_2511_18900/figures/012_Figure_10.jpg]]
*Figure 10: Stage1 baking improves the quality*

### 失败模式与局限性

尽管 MatMart 在整体上表现优异，论文指出了两个主要局限性：

- **材质分解的固有歧义**：反照率-光照分解本身存在多解性，可能导致预测的反照率出现缩放颜色偏差（scaled color）。这是基于图像的材质估计领域的共性问题，并非 MatMart 特有。
- **强自遮挡物体的信息不足**：对于具有严重自遮挡的物体，部分区域在输入视图中不可见，第二阶段生成可能因信息不足而质量下降。此类物体需要更多输入视图来保证生成质量。

### 推理效率与开放问题

MatMart 完成单个物体的完整重建需要 9–23 分钟，这一推理时间限制了其在实时或大规模场景中的应用。此外，模型在真实世界复杂光照和遮挡条件下的泛化能力、以及向透明/半透明/体积材质扩展的可行性，仍是待探索的开放问题。

![[assets/figures/papers/paper_list_l2543_https_arxiv_org_abs_2511_18900/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons for single-view and multi-view settings. Best results are marked as 1st and 2nd*

## 定位与知识库关联

### 1. 核心瓶颈与设计动机

现有材质重建方法面临三重困境：**（1）** 难以在保持输入图像细节的同时灵活处理任意数量高分辨率视图；**（2）** 多视图一致性维护通常依赖全局交叉注意力，空间复杂度高达 $O(N^2)$，限制了可处理的视图数量与分辨率；**（3）** 多数方法依赖多个预训练模型级联（如先进行 RGB 生成再进行材质预测），导致训练部署复杂、稳定性不足。MatMart 的因果调控点在于：将材质重建解耦为**基于输入的准确预测**（阶段一）和**基于先验的未观察区域生成**（阶段二），并通过**视图-材质交叉注意力（VMCA）** 将多视图一致性维护的空间复杂度降至 $O(1)$，同时将预测与生成统一于端到端优化的单一扩散模型中。

### 2. 与已有工作的关系

#### 2.1 逆渲染方法

**NvDiffRec**（Munkberg et al., CVPR 2022）代表基于物理的逆渲染路线，需对每个物体进行单独优化，计算开销大且泛化能力有限。MatMart 通过前馈式扩散模型直接预测材质，无需逐物体优化，在效率与泛化性上具有本质优势。

#### 2.2 单视图材质估计

**Material Anything**（Huang et al., CVPR 2025）采用预训练 RGB 生成模型与材质预测模型的级联架构，流程复杂且模型间协同优化困难。MatMart 使用单一扩散模型端到端完成预测与生成，简化了训练管线并提升了稳定性。

#### 2.3 多视图材质重建

**MaterialMVP**（He et al., ICCV 2025）是当前多视图材质重建的代表方法，但其全局联合处理所有视图的方式导致空间复杂度随视图数量平方增长。MatMart 通过渐进式推理与 VMCA 将复杂度降至 $O(1)$，可处理任意数量高分辨率视图，在多视图设置下 Albedo PSNR 提升 4.49 dB（32.10 vs 27.61）、渲染 FID 降低 11.80（26.20 vs 38.00）。

#### 2.4 UV 空间纹理生成

**Paint3D**（Zeng et al., CVPR 2024）和 **TexGEN**（Yu et al., TOG 2024）在 UV 空间直接生成纹理，但 UV 空间语义信息弱，难以产生高质量结果。MatMart 选择在视图空间进行生成，利用更丰富的语义信息，并通过交替烘焙将结果融合至 UV 纹理。

### 3. 关键技术差异点

| 维度 | 已有方法 | MatMart |
|------|----------|---------|
| 多视图一致性机制 | 全局交叉注意力（$O(N^2)$） | 渐进式推理 + VMCA（$O(1)$） |
| 材质生成空间 | UV 空间直接生成 | 视图空间生成 + 交替烘焙 |
| 模型架构 | 多模型/预训练模型级联 | 单一扩散模型端到端优化 |
| 视图数量灵活性 | 固定或受限 | 任意数量输入 |

### 4. 适用边界与局限

**适用场景**：MatMart 在 Objaverse 子集和 Stanford-ORB 真实世界数据上均展现出优异性能，适用于各类刚性物体的材质重建，尤其在多视图高分辨率输入下优势显著。

**已知局限**：
- **材质分解歧义**：反照率预测可能出现缩放颜色（scaled color），这是材质分解的固有歧义，需手动验证具体场景下的表现。
- **强自遮挡物体**：对于存在严重自遮挡的物体，可能需要更多视图进行生成，否则部分区域信息不足，导致重建质量下降。
- **推理时间**：单物体推理需 9–23 分钟，尚不能满足实时或大规模应用需求。

### 5. 开放问题

1. **推理效率优化**：如何进一步缩短推理时间，使方法适用于实时交互或大规模资产生产场景？
2. **真实世界泛化**：模型在复杂光照（如强镜面反射、环境光遮挡）和严重遮挡条件下的泛化能力尚需更系统的评估。
3. **材质类型扩展**：当前方法聚焦于标准 PBR 材质（反照率、粗糙度、金属度），是否能够扩展到透明、半透明或体积材质的重建？
4. **几何联合优化**：MatMart 假设输入几何已知，未来是否可将几何优化与材质重建统一于同一框架？

## 原文 PDF

![[paperPDFs/CVPR_2026/MatMart_Material_Reconstruction_of_3D_Objects_via_Diffusion.pdf]]
