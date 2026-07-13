---
title: "VQRAE: Representation Quantization Autoencoders for Multimodal Understanding, Generation and Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VQRAE_Representation_Quantization_Autoencoders_for_Multimodal_Understanding_Generation_and_Reconstruction.pdf
project_link: null
code_link: null
aliases:
- VQRAE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 基于预训练视觉基础模型（VFMs）的高维语义VQ codebook（1536维，100%利用率）与两阶段自蒸馏训练策略：第一阶段冻结编码器训练高维codebook和ViT解码器；第二阶段解冻编码器并引入自蒸馏损失以保持语义特征。
primary_logic: 利用预训练的VFMs作为统一编码器，直接对语义特征进行高维向量量化，并通过对称的ViT解码器重建图像；同时采用自蒸馏约束，使得单一tokenizer能够同时输出未量化的连续特征（用于多模态理解）和离散token（用于生成与重建），从而在统一架构下实现理解、生成与重建的有效权衡。
claims:
- VQRAE是首个在统一tokenizer中同时输出连续语义特征和离散生成token的工作，无需卷积编码器。
- 语义VQ codebook在1536维上达到100%利用率，与传统低维codebook的发现相反。
- VQRAE在重建质量和多模态理解上均超越双编码器方法（如TokenFlow, Janus）。
- 两阶段训练与自蒸馏损失在保持理解性能的同时增强了重建细节（Table 6, Figure 6）。
---

# VQRAE: Representation Quantization Autoencoders for Multimodal Understanding, Generation and Reconstruction

> [!tip] 核心洞察
> 利用预训练的VFMs作为统一编码器，直接对语义特征进行高维向量量化，并通过对称的ViT解码器重建图像；同时采用自蒸馏约束，使得单一tokenizer能够同时输出未量化的连续特征（用于多模态理解）和离散token（用于生成与重建），从而在统一架构下实现理解、生成与重建的有效权衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | VQRAE：面向多模态理解、生成与重建的表示量化自编码器 |
| 英文题名 | VQRAE: Representation Quantization Autoencoders for Multimodal Understanding, Generation and Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.23386) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | VQRAE |
| Dataset | ImageNet 256×256 50k validation, MME-Perception, SEEDBench-Img, TextVQA |

> [!tip] 效果简介
> - ImageNet 256×256 50k validation 上，rFID↓ VQRAE (SigLIP2) 1.31 vs TokenFlow 1.37 (-0.06 (更优))；PSNR↑ VQRAE (SigLIP2) 22.23 vs VQGAN 20.00 (+2.23)。
> - MME-Perception 上，score VQRAE+ (SigLIP2, Vicuna-13B 512) 1543.3 vs TokenFlow-L 1365.4 (+177.9)。
> - SEEDBench-Img 上，score VQRAE+ (SigLIP2, Vicuna-13B 512) 69.9 vs TokenFlow-L 62.6 (+7.3)。

## 概要

多模态大模型在统一视觉理解与生成时面临一个根本瓶颈：连续语义特征与离散视觉 token 之间存在固有矛盾。理解任务依赖高维连续语义表示，而生成任务需要将图像压缩为离散 token 以适配自回归范式。现有方案多采用双编码器设计——分别训练语义编码器和像素编码器，再通过 CLIP 损失等间接对齐（如 **Janus**（Wu et al., 2024）、**TokenFlow**（Xie et al., ICCV 2025）、**QLIP**（Zhao et al., 2025））——这不仅增加了模型复杂度，更阻碍了两种表示之间的深层交互，难以在不牺牲一方性能的前提下实现有效的理解-生成权衡。

VQRAE 针对这一瓶颈提出了一个简洁而高效的解法：**以预训练视觉基础模型（VFMs）作为统一编码器，直接对高维语义特征进行向量量化，并通过对称 ViT 解码器重建图像**。其核心因果调控机制包含两个关键设计：一是高维语义 VQ codebook（1536 维，与 VFMs 特征维度一致），在 16384 大小的码本上实现 100% 利用率，颠覆了传统低维 codebook（8-256 维）的必要性认知；二是两阶段自蒸馏训练策略——第一阶段冻结编码器训练 codebook 和解码器，第二阶段解冻编码器并引入自蒸馏损失，约束微调后的语义特征不偏离原始 VFMs 空间，从而在增强重建细节的同时保持多模态理解能力。

基于这一设计，VQRAE 成为首个在统一 tokenizer 中同时输出连续语义特征（用于理解）和离散视觉 token（用于生成与重建）的工作，无需卷积编码器。实验表明，该方法在重建质量上超越了双编码器方法：在 ImageNet 256×256 验证集上，VQRAE（SigLIP2）达到 rFID 1.31、PSNR 22.23，优于 TokenFlow 的 1.37 和 VQGAN 的 20.00；在多模态理解上，VQRAE+（SigLIP2, Vicuna-13B）在 MME-Perception 上得分 1543.3，较 TokenFlow-L 提升 177.9 分，在 SEEDBench-Img 上达到 69.9（+7.3）。在生成任务上，VQRAE 0.6B 模型在 GenEval 上达到 0.76，远超同规模 LlamaGen 的 0.32。

消融实验进一步验证了方法设计的有效性：高维 codebook 是实现 100% 利用率的关键，低维 codebook 则导致训练不收敛和码本崩塌；两阶段训练搭配自蒸馏在重建与理解的权衡上达到最优（rFID 2.71, MME-P 1439.1），而纯端到端训练虽重建略好但理解性能崩溃。当前方法的主要局限在于文本重建和高密度场景仍存在瑕疵，生成中的人脸和手指存在伪影，且尚未探索重建与生成对理解的潜在促进作用。

多模态大模型正朝着统一理解与生成的方向快速演进，但**连续语义特征**与**离散视觉token**之间的根本矛盾始终是核心瓶颈。理解任务依赖高维连续语义表示来捕捉细粒度语义，而生成任务则要求将图像压缩为离散token序列以适配自回归范式。现有的统一方案主要分为两条技术路线，均存在结构性缺陷。

**双编码器范式**（如 **Janus** (Wu et al., 2024)、**TokenFlow** (Xie et al., ICCV 2025)）分别为理解和生成设计独立的编码器。理解编码器提取连续语义特征，生成编码器（通常基于CNN）输出离散视觉token。这种设计的代价是双重的：模型参数量和计算开销显著增加，且两套表示之间缺乏显式交互机制，难以实现真正的表示共享。实际上，如 Figure 4 的K-means聚类可视化所示，连续语义特征与离散token在语义聚类上呈现高度一致性，暗示双编码器存在冗余。

**CLIP监督范式**（如 **QLIP** (Zhao et al., 2025)、**Uni-Tok**）试图用单一编码器统一输出，但通过CLIP损失间接约束离散token的语义质量。这种方式绕开了直接量化的难题，却引入了额外的训练目标和复杂度，且离散token的语义保真度受限于CLIP空间的表达能力。

更深层的问题在于**向量量化（VQ）的维度困境**。传统VQ tokenizer（如 **VQGAN** (Esser et al., CVPR 2021)）基于CNN像素编码器，在低维空间（8-256维）进行量化以维持codebook的稳定性和利用率。然而，预训练视觉基础模型（VFMs，如SigLIP2、InternViT）输出的语义特征维度高达1024-1536维——直接将低维量化范式迁移到高维语义特征上会导致训练不收敛和codebook崩塌（Table 5）。这一发现从根本上挑战了“低维codebook是重建与生成的关键”的既有认知。

此外，即使成功构建了统一tokenizer，**理解与重建的权衡**依然棘手。端到端联合训练虽能提升重建细节，却会破坏编码器的语义表示能力（Table 6, Figure 6）；冻结编码器虽能保持语义，却限制了重建质量的进一步提升。如何在单一架构内实现两者的有效平衡，是统一tokenizer走向实用的关键。

正是基于上述缺口，VQRAE提出了一个核心洞察：**利用预训练VFMs作为统一编码器，直接对高维语义特征进行向量量化，并通过自蒸馏约束在微调编码器的同时保持语义特征**，从而在单一tokenizer内同时输出连续语义特征（用于理解）和离散视觉token（用于生成与重建），实现理解、生成与重建在统一架构下的有效权衡。

## 核心方法与创新机理

VQRAE 的核心创新在于通过**统一编码器架构**与**高维语义向量量化**，从根本上打破了多模态理解与生成任务中长期存在的双编码器范式。其关键突破可归结为三个维度的设计变更：

### 从双编码器到统一编码器

传统统一多模态模型普遍采用双编码器范式——一个语义编码器负责理解，一个像素编码器负责生成（如 **Janus** (Wu et al., 2024) 系列和 **TokenFlow** (Xie et al., ICCV 2025)）。这种设计增加了模型复杂度，且两类编码器提取的特征难以有效交互，导致理解与生成之间存在结构性妥协。

VQRAE 直接采用预训练的视觉基础模型（VFMs，如 SigLIP2 或 InternViT）作为**唯一的编码器**，同时输出两类表示：未量化的连续语义特征（用于多模态理解）和经向量量化后的离散 token（用于生成与重建）。这一设计消除了双编码器的冗余，使得同一语义空间能够同时服务于理解和生成任务（Figure 1c）。

### 高维语义 VQ Codebook

这是 VQRAE 最具颠覆性的技术选择。传统离散 tokenizer（如 **VQGAN** (Esser et al., CVPR 2021)）依赖低维 codebook（通常 8-256 维），因为低维被认为对重建和生成至关重要。然而，当对 VFMs 提取的 ViT 特征进行量化时，低维 codebook 会导致训练不收敛和码本崩塌。

VQRAE 反其道而行，将 codebook 维度提升至与 VFMs 特征一致的 **1536 维**，并实现了 **100% 的码本利用率**。消融实验（Table 5）表明，当维度从 8 逐步提升至 1152 时，重建质量持续改善（rFID 从崩溃降至 2.65），利用率从接近 0 升至 100%。这一发现颠覆了离散 tokenizer 领域“低维优先”的固有认知。

### 两阶段训练与自蒸馏约束

单纯端到端训练统一编码器会导致理解性能崩溃——模型在优化重建目标时丢失了预训练 VFMs 的语义能力。VQRAE 采用**两阶段训练策略**解决这一权衡：

- **第一阶段**：冻结 VFMs 编码器，仅训练高维 VQ codebook 和对称 ViT 解码器，以像素重建为目标建立离散表示能力。
- **第二阶段**：解冻编码器，联合优化编码器、codebook 和解码器，同时引入**自蒸馏损失**（以冻结的初始编码器作为教师），约束微调后的编码器输出不偏离原始语义特征空间。

自蒸馏损失的形式为 $\mathcal{L}_{\mathrm{distill}} = \| Z_{I} - T(X) \|_{2}^{2}$，其中 $T(X)$ 为冻结教师模型的输出。消融实验（Table 6, Figure 6）证实，两阶段训练配合自蒸馏在重建与理解之间达到了最优权衡（rFID 2.71, MME-P 1439.1），而纯端到端训练虽重建略优但理解性能崩溃。

### 对称 ViT 解码器

与 VQGAN 等方法的 CNN 像素解码器不同，VQRAE 采用与编码器结构对称的 **ViT 解码器**。这一设计使得编码器-解码器之间形成结构一致性，有利于高维语义特征到像素空间的映射，同时避免了 CNN 解码器引入的归纳偏置与 ViT 编码器特征之间的不匹配。

VQRAE 的总体设计围绕一个核心矛盾展开：**连续语义特征与离散视觉 token 之间的根本张力**。在统一多模态理解、生成与重建的单一架构中，理解任务需要高保真的连续语义表示，而生成与重建任务则依赖于可被自回归模型消费的离散 token。现有双编码器范式（如 **Janus** (Wu et al., 2024)、**TokenFlow** (Xie et al., ICCV 2025)）通过独立的语义编码器和像素编码器分别处理这两类需求，但这增加了模型复杂度、阻碍了表示间的交互，且难以在不牺牲性能的前提下平衡像素级重建与语义理解。

VQRAE 的核心洞察在于：**利用预训练的视觉基础模型（VFMs）本身作为统一编码器，直接对其输出的高维语义特征进行向量量化**，从而在单一 tokenizer 内同时输出未量化的连续特征（用于多模态理解）和离散 token（用于生成与重建）。这一设计彻底摒弃了卷积编码器，使整个 pipeline 在 ViT-only 的范式下运行。

### Pipeline 总览

VQRAE 的端到端流程可分为三个关键阶段：

1. **统一语义编码**：输入图像 $X$ 经过预训练的 VFMs 编码器 $E$（如 SigLIP2 或 InternViT），提取连续语义特征 $Z_I = E(X)$。该特征直接服务于下游多模态理解任务，无需额外对齐或微调。

2. **高维向量量化**：连续特征 $Z_I$ 进入高维 VQ codebook $\mathcal{C}$（采用 SimVQ 方法，大小 16384，维度 1536），通过 L2 距离查找完成离散化：
   $$Z_{q} = \operatorname{lookup}\left(\arg\min_i \| \hat{Z}_{c} - c^{i} w^{i} \|\right), \quad i = 1, \ldots, k$$
   量化后的离散 token $Z_q$ 作为视觉生成任务的输入。与传统低维 codebook（8-256 维）的关键区别在于，VQRAE 在 1536 维的高维空间实现了 **100% 的码本利用率**，彻底避免了码本崩塌问题。

3. **对称 ViT 解码**：离散 token $Z_q$ 经由与编码器结构镜像对称的 ViT 解码器 $D$，重建图像 $X' = D(Z_q)$。解码器摒弃了传统 CNN 像素解码器（如 VQGAN 所用），采用与 VFMs 编码器一致的 Transformer 架构，确保特征空间的对称性和信息流的保真度。

### 双输出机制：理解与生成的统一

VQRAE 的关键创新在于其 **双输出机制**：
- **连续特征 $Z_I$**：直接来自编码器，未经量化损失，保留完整语义信息，用于多模态理解（如 VQA、基准评测）。
- **离散 token $Z_q$**：经 codebook 量化，适配自回归生成范式，用于图像重建和条件生成。

这种设计使得 VQRAE 在单一编码器内同时服务于两类任务，而无需维护两个独立的编码分支。Figure 4 的 K-means 聚类可视化验证了这一点：连续特征按语义类别（如“狗”“猫”）形成清晰聚类，而离散 token 则按视觉细节（如纹理、颜色）分组，表明同一编码器确实能同时捕获语义判别性和视觉细粒度信息。

### 两阶段训练策略

为在理解与重建之间取得最优权衡，VQRAE 采用两阶段训练策略（Figure 3b）：

**第一阶段（冻结编码器）**：编码器 $E$ 权重冻结，仅训练高维 VQ codebook 和 ViT 解码器。优化目标为重建损失与量化损失之和：
$$\mathcal{L}_{\mathrm{stage1}} = \mathcal{L}_{\mathrm{rec}} + \mathcal{L}_{\mathrm{quant}}$$
其中重建损失 $\mathcal{L}_{\mathrm{rec}}$ 由像素级 L2 损失、感知损失 $\mathcal{L}_{\mathrm{P}}$ 和对抗损失 $\mathcal{L}_{\mathrm{G}}$ 组成：
$$\mathcal{L}_{\mathrm{rec}} = \ell_{2}(X, X') + \mathcal{L}_{\mathrm{P}}(X, X') + \lambda_{\mathrm{G}} \mathcal{L}_{\mathrm{G}}(X')$$
量化损失为 SimVQ 的承诺损失：
$$\mathcal{L}_{\mathrm{quant}} = \| \mathrm{sg}(C) - Z_{q} \|_{2}^{2} + \beta \cdot \| Z_{q} - \mathrm{sg}(C) \|_{2}^{2}$$

**第二阶段（解冻编码器 + 自蒸馏）**：解冻编码器，联合优化编码器、codebook 和解码器。关键引入 **自蒸馏损失**，以冻结的第一阶段编码器作为教师模型 $T$，约束微调后的编码器输出不偏离原始语义特征空间：
$$\mathcal{L}_{\mathrm{distill}} = \| Z_{I} - T(X) \|_{2}^{2}$$
第二阶段总损失为：
$$\mathcal{L}_{\mathrm{stage2}} = \mathcal{L}_{\mathrm{rec}} + \mathcal{L}_{\mathrm{quant}} + \lambda_{d} \mathcal{L}_{\mathrm{distill}}$$

消融实验（Table 6, Figure 6）证实，纯端到端训练虽能略微提升重建细节，但会导致理解性能崩溃（MME-P 骤降）；而两阶段训练配合自蒸馏在重建质量（rFID 2.71）和理解性能（MME-P 1439.1）之间实现了最优权衡。这一训练策略是 VQRAE 能够超越双编码器方法的核心工程支撑。

### 与基线方法的架构对比

Figure 1 清晰展示了 VQRAE 与现有统一 tokenizer 的架构差异：
- **Janus 系列**：采用双编码器范式，语义编码器和像素编码器独立运行，输出分别服务于理解和生成。
- **QLIP / Uni-Tok**：使用 CLIP 损失监督离散 token，试图在离散空间中保留语义，但受限于低维 codebook 的表达能力。
- **VQRAE**：单一 VFMs 编码器直接产出连续和离散两种表示，架构最简洁，且在高维 codebook 的支撑下实现了更优的理解-重建权衡。

![[assets/figures/papers/paper_list_l2274_https_arxiv_org_abs_2511_23386/figures/001_Figure_1.jpg]]
*Figure 1: Comparions of different unified tokenizers. (a) Janus [7, 76] series adopt dual-encoder paradigm. (b) QLIP [95] and Uni-Tok [41] supervise dicrete tokens with CLIP loss. (c) Our VQRAE can produce continuous and discrete tokens for different tasks*

VQRAE 的核心设计在于用一个统一的 ViT 编码器替代传统的双编码器范式，并引入高维语义向量量化与对称 ViT 解码器，配合两阶段自蒸馏训练策略，实现连续语义特征与离散视觉 token 的单一模型输出。

### 统一编码器：预训练 VFMs 的复用

VQRAE 直接采用预训练的视觉基础模型（VFMs，如 SigLIP2 或 InternViT）作为统一编码器 $E$。这一选择的关键在于：VFMs 提取的语义特征本身已具备强大的判别能力，无需额外引入 CNN 像素编码器来捕捉底层纹理。编码器输出的连续特征 $Z_I = E(X)$ 同时承担两个角色——作为多模态理解任务中 LLM 的视觉输入，以及作为向量量化的源特征。这从根本上消除了双编码器范式（如 **Janus**，Wu et al., 2024；**TokenFlow**，Xie et al., ICCV 2025）中语义编码器与像素编码器之间的表示冗余，如 Figure 4 的 K-means 聚类所示，连续特征与离散 token 均能形成有意义的语义分组。

![[assets/figures/papers/paper_list_l2274_https_arxiv_org_abs_2511_23386/figures/005_Figure_4.jpg]]
*Figure 4: We perform K-means clustering on the ImageNet-1K validation set using continuous features and discrete tokens. The visualization illustrates images grouped by (a) continuous features and (b) discrete tokens, both derived from our VQRAE. VQRAE is capable of producing discriminative features for multimodal understanding and discrete visual tokens for fine-grained reconstruction and generation simultaneously within a unified tokenizer. It indicates the redundancy in the dual-encoder paradigm*

### 高维语义 VQ Codebook

与传统 VQGAN（Esser et al., CVPR 2021）使用低维 codebook（8–256 维）不同，VQRAE 在 VFMs 的原始特征维度（如 1536 维）上直接进行向量量化。量化过程采用 SimVQ 方法，给定 codebook $C = \{c^1, c^2, \ldots, c^k\}$（$k=16384$），对编码器输出的归一化特征 $\hat{Z}_c$ 进行最近邻查找：

$$Z_{q} = \operatorname{lookup}\left(\arg\min_i \| \hat{Z}_{c} - c^{i} w^{i} \| \right), \quad i = 1, \ldots, k$$

其中 $w^i$ 为可学习的权重因子。量化后的离散 token $Z_q$ 作为视觉生成与重建任务的输入。

这一设计的核心发现是：**高维 codebook 在 VFMs 特征空间中可实现接近 100% 的利用率**，这与传统认知中“低维 codebook 对重建与生成至关重要”的结论截然相反。消融实验（Table 5）证实，当 codebook 维度降至 8 或 256 时，训练不收敛且出现严重的码本崩塌；维度提升至 1152–1536 时，利用率稳定在 100%，重建质量（rFID）持续改善。codebook 大小从 4096 增至 16384 时重建质量提升，但超过 16K 后性能轻微下降。

### 对称 ViT 解码器

VQRAE 摒弃了传统 CNN 像素解码器，改用与编码器结构镜像对称的 ViT 解码器。解码器以量化后的离散 token $Z_q$ 为输入，重建图像 $X'$。对称结构保证了编码器语义特征与解码器重建之间的表示一致性，避免了跨架构的信息损失。

### 损失函数体系

**第一阶段**训练冻结编码器，仅优化 codebook 和解码器。总损失由重建损失与量化损失构成：

$$\mathcal{L}_{\mathrm{stage1}} = \mathcal{L}_{\mathrm{rec}} + \mathcal{L}_{\mathrm{quant}}$$

其中重建损失 $\mathcal{L}_{\mathrm{rec}}$ 包含三项：

$$\mathcal{L}_{\mathrm{rec}} = \ell_{2}(X, X') + \mathcal{L}_{\mathrm{P}}(X, X') + \lambda_{\mathrm{G}} \mathcal{L}_{\mathrm{G}}(X')$$

- $\ell_2$：像素级 L2 损失，保证重建图像的保真度
- $\mathcal{L}_{\mathrm{P}}$：感知损失，在特征空间约束重建质量
- $\mathcal{L}_{\mathrm{G}}$：对抗损失，由判别器提供，权重 $\lambda_{\mathrm{G}}$ 控制

量化损失 $\mathcal{L}_{\mathrm{quant}}$ 采用标准承诺损失形式：

$$\mathcal{L}_{\mathrm{quant}} = \| \mathrm{sg}(C) - Z_{q} \|_{2}^{2} + \beta \cdot \| Z_{q} - \mathrm{sg}(C) \|_{2}^{2}$$

其中 $\mathrm{sg}(\cdot)$ 为梯度截断算子，$\beta$ 为承诺权重。

**第二阶段**解冻编码器，引入自蒸馏损失以保护语义理解能力。教师模型 $T$ 为第一阶段冻结的初始编码器，蒸馏损失约束微调后编码器输出 $Z_I$ 与教师输出 $T(X)$ 的一致性：

$$\mathcal{L}_{\mathrm{distill}} = \| Z_{I} - T(X) \|_{2}^{2}$$

第二阶段总损失为：

$$\mathcal{L}_{\mathrm{stage2}} = \mathcal{L}_{\mathrm{rec}} + \mathcal{L}_{\mathrm{quant}} + \lambda_{d} \mathcal{L}_{\mathrm{distill}}$$

其中 $\lambda_d$ 为蒸馏权重。消融实验（Table 6, Figure 6）表明，两阶段训练搭配自蒸馏在重建与理解的权衡上达到最优（rFID 2.71, MME-P 1439.1），纯端到端训练虽重建略好，但理解性能崩溃——这验证了自蒸馏约束是平衡语义保持与细节重建的关键因果机制。

## 实验与关键发现

### 核心实验设计思路

VQRAE 的实验验证围绕一个中心命题展开：**统一编码器能否在不牺牲理解能力的前提下，同时提供高质量的离散 token 用于重建与生成**。实验设计从三个维度递进——先通过引导实验（Table 1）建立统一 tokenizer 的可行性基线，再分别在重建（Table 2）、多模态理解（Table 3）和视觉生成（Table 4）三个下游任务上进行系统对比，最后通过消融实验（Table 5-6）揭示高维 codebook 和两阶段自蒸馏训练策略的因果作用。

![[assets/figures/papers/paper_list_l2274_https_arxiv_org_abs_2511_23386/figures/003_Table_1.jpg]]
*Table 1: Comparisons of various methods in multimodal understanding and reconstruction. “Und.” and “Gen.” refer to Understanding and Generation. “C” and “D” indicate Continuous and Discrete representations used for specific tasks. † denotes training on LLaVA-v1.5 [37] setting. Reconstruction quality is evaluated on the 256 × 256 ImageNet 50k validation set. MME-P: MME-Perception [18]; SEED: SEEDBench-Img [29]; TQA: TextVQA [54]; TokenFlow: TokenFlow-L-13B [49]*

![[assets/figures/papers/paper_list_l2274_https_arxiv_org_abs_2511_23386/figures/006_Table_2.jpg]]
*Table 2: Comparisons of reconstruction quality on the 256 × 256 ImageNet 50k validation set. Ratio: downsample ratio*

![[assets/figures/papers/paper_list_l2274_https_arxiv_org_abs_2511_23386/figures/007_Table_3.jpg]]
*Table 3: Evaluation on multimodal understanding benchmarks. We collect evaluations including: POPE [32]; GQA [25]; TQA: TextVQA [54]; MMB: MMBench-En [38]; MME-P: MME-Perception [18]; SEED: SEEDBench-Img [29]; MMMU [91]; AI2D [27]. † denotes training on LLaVA-v1.5 [37] setting. “Res.” is an abbreviation of resolution. Our pretrained VQRAE can be directly comparable with SOTA open-sourced MLLMs without specific fine-tuning as detailed in Sec. 3.4*

![[assets/figures/papers/paper_list_l2274_https_arxiv_org_abs_2511_23386/figures/010_Table_5.jpg]]
*Table 5: Ablation on the hyperparameters of the VQ codebook*

---

### 引导实验：统一 tokenizer 的可行性验证

Table 1 构成了全文实验逻辑的锚点。该表将 VQRAE 与三类代表性方法进行横向对比：

| 方法类型 | 代表方法 | 编码器策略 | 理解表示 | 生成/重建表示 |
|---------|---------|-----------|---------|-------------|
| 双编码器 | Janus (Wu et al., 2024) | 独立的语义编码器 + 像素编码器 | 连续 | 离散 |
| CLIP 蒸馏 | QLIP (Zhao et al., 2025) | 统一编码器 + CLIP 损失监督 | 连续 | 离散（CLIP 约束） |
| 连续自编码器 | RAE (Zheng et al., 2025) | 统一编码器 | 连续 | 连续 |
| **本文方法** | **VQRAE** | 统一编码器 + 高维 VQ | 连续 | 离散（VQ） |

引导实验的核心发现是：**VQRAE 在重建质量（rFID 1.31）上超越双编码器方法 TokenFlow（rFID 1.37），同时在多模态理解上达到 MME-Perception 1543.3、SEEDBench-Img 69.9**，证明了统一编码器范式在理解-重建权衡上的优越性。这一结果直接挑战了“理解与生成需要独立编码器”的既有假设。

---

### 重建质量：高维语义量化的突破

Table 2 报告了 ImageNet 256×256 50k 验证集上的重建质量对比。VQRAE 的两个变体均取得领先：

- **VQRAE (SigLIP2)**：rFID 1.31, PSNR 22.23, SSIM 0.762，下采样比 16×
- **VQRAE (InternViT)**：rFID 1.39, PSNR 22.18, SSIM 0.759，下采样比 16×

相比经典像素级 tokenizer **VQGAN**（Esser et al., CVPR 2021）的 PSNR 20.00，VQRAE 提升了 2.23 dB。这一提升的因果机制在于：**高维语义 codebook（1536 维，与 VFMs 特征维度对齐）保留了比低维像素 codebook 更丰富的结构信息**。Figure 5 和 Figure 7 的可视化结果进一步证实，VQRAE 重建图像在纹理细节和语义保真度上均优于基线。

值得注意的是，VQRAE 在 16× 下采样比下仍能维持高质量重建，而传统 VQGAN 通常需要更小的下采样比。这归因于 ViT 解码器的全局感受野——对称的 ViT 解码器能够更有效地利用离散 token 中的全局语义信息进行像素重建。

---

### 多模态理解：几乎无损的统一

Table 3 在八个多模态理解基准上进行了全面评估。关键结果包括：

- **VQRAE+ (SigLIP2, Vicuna-13B, 512 分辨率)**：MME-P 1543.3, SEEDBench-Img 69.9, MMBench 68.9，全面超越 TokenFlow-L（MME-P 1365.4, SEED 62.6）
- **VQRAE (InternViT, Qwen2.5-7B)**：TextVQA 80.6，与纯理解模型 InternVL3（80.2）几乎持平（+0.4），证明量化引入的语义损失极小

**核心因果机制**：两阶段训练中的自蒸馏损失（Equation 5, $\mathcal{L}_{\mathrm{distill}} = \| Z_{I} - T(X) \|_{2}^{2}$）是维持理解性能的关键。冻结的初始编码器作为教师模型，约束微调后的编码器输出不偏离原始语义特征空间。Table 6 的消融实验（下文详述）直接验证了这一点——移除自蒸馏后，理解性能显著下降。

---

### 视觉生成：离散 token 的生成能力

Table 4 评估了 VQRAE 作为生成 tokenizer 的表现。在 GenEval 基准上，VQRAE 0.6B 模型取得 Overall 0.76，远超同规模的 **LlamaGen 0.8B**（0.32）和 **PixArt-α 0.6B**（DPG-Bench 71.11 vs VQRAE 86.67）。

这一优势源于两个因素：
1. **高维语义 token 携带了更丰富的视觉概念信息**，使得自回归生成模型更容易学习 token 间的语义依赖
2. **100% 的 codebook 利用率**确保了离散 token 空间的有效表达能力，避免了低利用率 codebook 中常见的“死码”问题

---

### 消融实验：揭示因果机制

#### 高维 codebook 的必要性（Table 5）

Table 5 系统探索了 VQ codebook 的维度和大小对重建质量的影响：

- **维度消融**：当 codebook 维度从 1536 降至 8 时，训练无法收敛且出现严重的 codebook 崩塌（利用率骤降）。这与传统 VQGAN 中“低维 codebook 有利于重建”的发现**截然相反**——当量化对象从像素特征变为 VFMs 的高维语义特征时，codebook 维度必须与特征维度匹配，否则 L2 距离度量在高维空间中的信息损失将导致优化失败。
- **大小消融**：codebook 大小从 4096 增至 16384 时，rFID 持续改善；继续增至 32768 时出现轻微退化（rFID 从 2.65 升至 2.71）。最优配置为 16384 大小、1152 维，此时 rFID 2.65, PSNR 20.14, SSIM 0.668，利用率 100%。

#### 两阶段训练与自蒸馏（Table 6, Figure 6）

Table 6 和 Figure 6 构成了全文最具因果解释力的消融。三种训练策略的对比：

| 训练策略 | rFID↓ | MME-P↑ | MMB↑ |
|---------|-------|--------|------|
| 仅第一阶段（冻结编码器） | 3.45 | 1493.5 | 67.4 |
| 端到端训练（无蒸馏） | **2.52** | 1338.7 | 62.0 |
| 两阶段 + 自蒸馏 | 2.71 | **1439.1** | **65.8** |

**因果解读**：
- 端到端训练虽然重建最优（rFID 2.52），但理解能力大幅退化（MME-P 从 1493.5 降至 1338.7）——编码器在优化重建损失时偏离了预训练的语义特征空间
- 两阶段 + 自蒸馏在重建（rFID 2.71）和理解（MME-P 1439.1）之间达到了最佳权衡：第一阶段冻结编码器保护语义空间，第二阶段的自蒸馏损失（$\lambda_d \mathcal{L}_{\mathrm{distill}}$）作为正则项约束编码器微调幅度

Figure 6 的可视化直接展示了这一权衡：第二阶段训练增加了细粒度纹理细节，而端到端训练虽然纹理更丰富，但语义一致性受损。

---

### 失败模式与局限性

Figure 9 和 Figure 10 分别展示了重建和生成的失败案例：

- **文本重建缺陷**（Figure 9）：在包含密集文字的图像中，VQRAE 重建的文字出现模糊、变形或缺失。这源于离散 token 的有限表达能力——文字需要极高的空间精度，而 16× 下采样不可避免地丢失了部分字符级信息。
- **生成伪影**（Figure 10）：生成图像中的人脸和手指区域存在明显的结构扭曲和纹理伪影。论文指出这可以通过更大规模的训练数据和强化学习（如 [11, 19, 67] 中的探索）来缓解，但当前版本尚未解决。

**量化损失的根本性限制**：离散 tokenizer 的量化操作（Equation 3）引入了不可消除的信息瓶颈。论文承认 VQRAE 在纯重建质量上难以与最先进的连续 VAE 竞争——这是离散表示的固有代价，换取的是与自回归生成范式的天然兼容性。

---

### 训练配置概要

Table 7-9 提供了完整的训练配置细节，关键参数包括：
- **Tokenizer 训练**（Table 7）：两阶段训练，第一阶段冻结编码器训练 150 epochs，第二阶段联合优化 50 epochs，自蒸馏权重 $\lambda_d$ 设为 1.0
- **多模态理解训练**（Table 8）：在 LLaVA-v1.5 框架下进行，VQRAE tokenizer 无需额外的对齐或指令微调即可直接使用
- **视觉生成训练**（Table 9）：自回归 Transformer 在 VQRAE 离散 token 上进行训练，模型规模 0.6B

---

### 实验总结与待验证问题

VQRAE 的实验体系完整验证了三个核心主张：
1. **统一编码器 + 高维语义 VQ 在理解-重建-生成三角权衡上超越双编码器范式**
2. **高维 codebook 的 100% 利用率是语义量化的关键使能因素**
3. **两阶段自蒸馏训练是实现理解-重建权衡的必要条件**

但仍存在若干需要人工核实或进一步探索的问题：
- 论文声称 VQRAE“无需多模态对齐或指令微调”即可用于理解任务，但 Table 3 中 VQRAE+ 仍标注了 LLaVA-v1.5 训练设置（† 标记），具体训练细节需对照原文确认
- 重建对理解的促进作用（如利用重建信号增强视觉 grounding）尚未验证，属于开放问题
- 高维 codebook 的特性是否可推广至视频、音频等时序模态，论文未给出实验证据

## 定位与知识库关联

### 从双编码器到统一tokenizer的演进

VQRAE 的提出直接回应了多模态理解与生成统一框架中的一个根本性瓶颈：**连续语义特征与离散视觉token之间的矛盾**。在 VQRAE 之前，统一tokenizer 的设计主要沿着三条技术路线展开：

1. **双编码器范式**：以 **Janus**（Wu et al., 2024）和 **TokenFlow**（Xie et al., ICCV 2025）为代表，分别为理解任务和生成任务配备独立的编码器。理解编码器输出连续语义特征，生成编码器输出离散视觉token。这种设计虽然能在各自任务上保持较好性能，但引入了显著的模型冗余——VQRAE 通过聚类可视化（Figure 4）表明，连续语义特征和离散token实际上编码了高度重叠的信息，双编码器存在结构性的表示冗余。此外，双编码器架构增加了模型复杂度，阻碍了表示层面的交互与共享。

2. **CLIP 损失监督范式**：以 **QLIP**（Zhao et al., 2025）和 **Uni-Tok** 为代表，尝试用 CLIP 损失直接监督离散token，使其同时具备语义判别能力。然而，这种间接的语义注入方式在理解性能上存在天花板，难以达到专用语义编码器的水平。

3. **连续自编码器路线**：**RAE**（Zheng et al., 2025）采用纯连续表示，在理解任务上表现优异，但缺乏离散化能力，无法直接接入自回归生成框架。**Tar** 则尝试对离散token进行语义蒸馏，但在理解性能上仍落后于 VQRAE（MME-P: 1571.0 vs 1746.8，Table 3）。

VQRAE 的关键突破在于：**利用预训练视觉基础模型（VFMs，如 SigLIP2、InternViT）作为统一编码器，直接对高维语义特征进行向量量化**，从而在单一tokenizer中同时输出连续特征（用于理解）和离散token（用于生成与重建）。这是首个无需卷积编码器即可实现此目标的统一tokenizer。

### 与 VQGAN 的核心差异：高维语义量化 vs 低维像素量化

VQRAE 与经典离散tokenizer **VQGAN**（Esser et al., CVPR 2021）的差异体现在多个维度，构成了从“像素级tokenizer”到“语义级tokenizer”的范式转变：

| 设计维度 | VQGAN | VQRAE |
|---------|-------|-------|
| 编码器架构 | CNN像素编码器 | 预训练ViT编码器（VFMs） |
| codebook维度 | 低维（8-256） | 高维（1536，与VFMs特征维度一致） |
| codebook利用率 | 易崩塌，需辅助技巧 | 100%利用率（4k-16k条目） |
| 解码器结构 | CNN解码器 | 对称ViT解码器 |
| 表示语义性 | 像素级，语义弱 | 语义级，可直接用于多模态理解 |

这一转变的关键洞察在于：**当量化对象从像素特征变为来自VFMs的语义特征时，codebook必须采用高维设计**。传统观点认为低维codebook对重建和生成至关重要，但 VQRAE 的消融实验（Table 5）表明，低维codebook（如8维）在量化ViT语义特征时会导致训练不收敛和码本崩塌，而1536维codebook实现了100%利用率。这一发现颠覆了离散tokenizer的设计常识。

### 训练策略的因果机制：两阶段训练与自蒸馏

VQRAE 的两阶段训练策略是其在理解-重建权衡上取得优势的核心因果机制：

- **第一阶段**（冻结编码器）：冻结预训练VFMs编码器，仅训练高维VQ codebook和ViT解码器。这一阶段确保了语义特征的稳定性，避免了量化训练对预训练表示的破坏。
- **第二阶段**（解冻编码器 + 自蒸馏）：解冻编码器进行联合优化，同时引入自蒸馏损失（$\mathcal{L}_{\text{distill}} = \| Z_I - T(X) \|_2^2$），以冻结的初始编码器作为教师模型，约束微调后的编码器输出不偏离原始语义空间。

消融实验（Table 6, Figure 6）揭示了这一策略的因果效应：纯端到端训练（无蒸馏约束）虽然能获得略好的重建质量，但理解性能崩溃；而两阶段训练搭配自蒸馏在重建（rFID 2.71）和理解（MME-P 1439.1, MMB 65.8）之间达到了最优权衡。Figure 6 的可视化进一步表明，第二阶段训练在保留语义的同时增加了细粒度重建细节。

### 适用边界与局限

VQRAE 的适用边界受以下因素制约：

1. **重建质量的天花板**：离散tokenizer固有的量化损失使其难以与最先进的连续VAE竞争。在文本重建和高密度场景下，重建质量仍有明显缺陷（Figure 9），表现为文字模糊、细节丢失。

2. **生成伪影**：图像生成中手指和人脸仍存在伪影（Figure 10），论文指出这可以通过扩展训练数据和强化学习来缓解，但尚未在本文中解决。

3. **理解性能的妥协**：尽管自蒸馏策略有效，但统一tokenizer在理解性能上仍可能存在轻微退化。论文承认“尚未探索更有效的方法来最小化理解能力的妥协”，这表明当前方案在理解-生成权衡上仍有优化空间。

4. **未验证的协同效应**：论文尚未验证重建与生成任务是否能够反过来增强多模态理解，这一潜在的协同效应仍是开放问题。

5. **模态泛化性未知**：高维codebook的特性是否可推广至其他模态（如音频、视频）尚未得到验证。

### 开放问题与未来方向

VQRAE 为统一多模态模型开辟了若干值得深入探索的方向：

- **任务间协同机制**：能否利用重建与生成任务反过来增强多模态理解？这需要设计更精细的表示交互机制。
- **权衡边界的进一步推进**：如何在保证语义理解的同时进一步优化重建与生成质量？可能需要探索新的训练策略或架构设计。
- **规模扩展**：如何高效扩展统一模型至更大规模？VQRAE 目前验证了 0.6B 参数规模的生成能力，更大规模下的行为尚待探索。
- **跨模态推广**：高维语义VQ codebook的设计原则是否适用于音频、视频等其他模态？这需要验证其在不同特征空间下的有效性。
- **与推理能力的结合**：论文指出离散tokenizer的量化损失是重建质量的天花板，未来工作可探索如何将 VQRAE 的语义token与更强大的解码器结合，或引入强化学习来弥补生成伪影。

## 原文 PDF

![[paperPDFs/CVPR_2026/VQRAE_Representation_Quantization_Autoencoders_for_Multimodal_Understanding_Generation_and_Reconstruction.pdf]]
