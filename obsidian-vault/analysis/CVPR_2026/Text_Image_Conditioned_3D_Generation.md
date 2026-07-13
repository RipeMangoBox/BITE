---
title: Text-Image Conditioned 3D Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Text_Image_Conditioned_3D_Generation.pdf
project_link: "https://jumpat.github.io/tigon-page"
code_link: null
aliases:
- TIC3G
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入文本-图像联合条件并设计轻量级跨模态融合机制（双分支DiT + 零初始化跨模态桥接 + 预测平均），使两模态互补信号共同指导生成过程。
primary_logic: 图像提供精确的视角对齐外观与几何线索，文本提供高层语义以消歧未观察区域；通过显式早期特征融合与后期预测平均，可在不破坏单模态能力的前提下整合互补信息，实现更鲁棒、可控的3D生成。
claims:
- 简单的晚期融合（SimFusion）在低信息视角下大幅优于单一模态模型，证明图像与文本高度互补。
- 零初始化跨模态桥接对性能提升至关重要，缺少桥接则性能增益极小。
- Toys4K 上 CLIP↑ = 92.97 (mesh)
- Toys4K 上 FDDINOv2↓ = 61.59 (GS)
---

# Text-Image Conditioned 3D Generation

> [!tip] 核心洞察
> 图像提供精确的视角对齐外观与几何线索，文本提供高层语义以消歧未观察区域；通过显式早期特征融合与后期预测平均，可在不破坏单模态能力的前提下整合互补信息，实现更鲁棒、可控的3D生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 文本-图像条件3D生成 |
| 英文题名 | Text-Image Conditioned 3D Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.21295) · [Project](https://jumpat.github.io/tigon-page) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | TIGON |
| Dataset | Toys4K, UniLat1K |

> [!tip] 效果简介
> - Toys4K 上，CLIP↑ 92.97 (mesh) vs 91.85 (UniLat3D, image-conditioned, mesh) (+1.12)；FDDINOv2↓ 61.59 (GS) vs 85.30 (UniLat3D, image-conditioned, GS) (-23.71)；ULIP↑ 41.36 (mesh) vs 40.32 (UniLat3D, image-conditioned, mesh) (+1.04)。
> - UniLat1K 上，FDDINOv2↓ 130.08 (GS) vs 155.99 (UniLat3D, image-conditioned, GS) (-25.91)。

## 概要

当前3D生成方法普遍依赖单一模态条件——要么是图像，要么是文本——二者各有难以调和的局限。图像条件模型（如**TRELLIS**，Xiang et al., CVPR 2025）能够保持参考视角的局部外观与几何细节，但对视角信息量高度敏感：当参考视角仅提供有限的可观测线索时，模型必须在未观察区域进行“幻觉式”补全，极易产生语义偏离的伪影。文本条件模型则提供高层语义指导，却缺乏像素级视觉约束，生成结果往往视觉保真度不足。两类模态无法同时满足保真度与语义一致性的双重需求。

本文提出 **TIGON**，一个极简的文本-图像联合条件3D生成基线。其核心洞察在于：图像提供精确的视角对齐外观与几何线索，文本提供高层语义以消歧未观察区域；通过显式的早期特征融合与后期预测平均，可在不破坏单模态能力的前提下整合互补信号，实现更鲁棒、可控的3D生成。TIGON采用双分支DiT架构——图像条件分支与文本条件分支各自预测速度场，并在每层DiT块之间通过零初始化线性桥接进行双向跨模态特征注入（早期融合），最终以预测平均的方式合成统一速度场（晚期融合）。训练时引入条件丢弃策略，使模型能够处理任意模态组合的推理需求。

诊断实验揭示了一个关键信号：简单的晚期融合基线（SimFusion）在低信息视角下大幅优于单一模态模型——在Toys4K基准上，SimFusion（View-1+Text）的FD_DINOv2降至82.40，而纯图像条件的TRELLIS为143.58，纯文本条件为145.06——有力证明了图像与文本信号的高度互补性。在此基础上，TIGON通过零初始化跨模态桥接将FD_DINOv2进一步从66.78压缩至61.59，而缺少桥接时性能增益微乎其微（仅从66.78降至66.04），表明早期特征融合是实现有效跨模态协同的关键机制。

在Toys4K与UniLat1K两个基准上，TIGON在CLIP、FD_DINOv2和ULIP指标上均一致优于单模态变体及其他现有方法。消融实验进一步表明，在已有早期融合和联合微调的前提下，简单的预测平均即可达到最优，更复杂的可学习晚期融合策略未能带来额外增益。TIGON还与TRELLIS架构兼容，验证了该融合范式的通用性。



### 3D生成中的单模态困境

当前3D内容生成方法主要依赖单一模态条件——要么是图像，要么是文本——但两种范式各自存在难以克服的短板。图像条件模型（如 **TRELLIS** (Xiang et al., CVPR 2025)、**UniLat3D**、**TripoSR** 等）能够从参考视角精确捕获局部外观与几何线索，然而其对视角信息量高度敏感：当参考视角仅覆盖物体的部分表面时，模型必须在未观察区域进行“幻觉式”补全。诊断实验（Table 1）清晰地揭示了这一问题——在信息丰富的 View-0 条件下，TRELLIS 的 FD\_DINOv2 为 56.08；当切换至信息量更低的 View-1 时，该指标急剧恶化至 143.58。这种退化表明，图像条件模型的保真度优势在低信息视角下迅速瓦解，未观察区域的语义偏离成为系统性缺陷。

文本条件模型则提供了另一极端的特性：文本承载了物体的高层语义与类别先验，能够在全局层面约束生成内容的语义一致性。然而，文本天然缺乏细粒度的视觉对齐信号，导致生成结果在几何精度和外观保真度上远逊于图像条件方法。在 Toys4K 基准上，文本条件的 UniLat3D 仅取得 FD\_DINOv2 154.88 的成绩，甚至低于低信息视角下的图像条件模型。两类模态的互补性由此凸显——图像提供精确的视角对齐线索，文本提供消歧未观察区域的语义约束——但现有方法始终无法将二者整合于统一的生成框架中。

### 核心瓶颈：模态互补信号未被有效利用

上述现象指向一个明确的研究瓶颈：**图像与文本两种模态在3D生成任务中高度互补，但缺乏一种机制使它们的互补信号在生成过程中协同发挥作用**。图像条件模型在可见区域表现优异，却因缺乏语义引导而在不可见区域产生偏差；文本条件模型具备全局语义理解，却因缺乏像素级约束而难以保证视觉质量。简单的晚期融合（如直接平均两模态预测的速度场）虽能带来初步改善——SimFusion 在 View-1+Text 条件下将 FD\_DINOv2 降至 82.40，远优于单一模态的 143.58 和 145.06——但这一朴素策略并未充分挖掘模态间的深层交互潜力。

### 本文动机：以轻量融合实现鲁棒的文本-图像联合3D生成

基于上述分析，本文提出 **TIGON**（Text-Image Conditioned 3D Generation），一个极简而有效的文本-图像联合条件3D生成基线。TIGON 的设计遵循一个核心洞见：**图像提供精确的视角对齐外观与几何线索，文本提供高层语义以消歧未观察区域；通过显式的早期特征融合与后期预测平均，可以在不破坏单模态能力的前提下整合互补信息**。具体而言，TIGON 采用双分支 DiT 架构（图像分支与文本分支），并通过两项轻量级融合机制实现跨模态协同：（1）零初始化跨模态线性桥接，在每层 DiT 块之间双向注入特征，实现早期融合；（2）逐去噪步的预测平均，作为晚期融合策略。该方法通过条件丢弃训练支持任意模态组合推理（仅图像、仅文本或联合条件），在保持单模态能力的同时，使两模态互补信号共同指导生成过程，从而实现更鲁棒、更可控的3D生成。



## 核心方法与创新机理

TIGON 的核心创新在于**首次将文本-图像联合条件引入原生3D生成框架**，并通过一套轻量级融合机制，在不破坏单模态预训练能力的前提下，实现两模态互补信号的协同利用。其创新可凝练为三个层面的 changed slots：

### 1. 条件模态：从单模态到自由形式多模态

现有原生3D生成器（如 **TRELLIS** (Xiang et al., CVPR 2025)、**UniLat3D**）仅支持单一模态条件——要么以图像驱动、要么以文本驱动。图像条件模型虽能保持参考视角的局部外观，但对视角信息量高度敏感：当参考图像仅覆盖部分表面时，未观察区域会产生语义偏离的幻觉；文本条件模型提供全局语义约束，却缺乏像素级视觉线索，生成结果保真度差。**两模态各自存在结构性盲区，且无法在同一框架内被同时利用。**

TIGON 将条件空间从单模态扩展为**文本-图像联合条件**，并支持任意模态组合的推理（仅图像、仅文本、或联合条件）。这一能力通过训练时的条件丢弃（condition dropout）实现：独立随机丢弃图像或文本条件，使模型学会在缺失某模态时仍能正常生成。推理时，用户可自由选择提供单张参考图像、文本描述、或二者同时提供，无需切换模型。

### 2. 架构设计：从单分支到双分支DiT + 零初始化跨模态桥接

TIGON 的架构创新在于**双分支DiT主干 + 逐层跨模态桥接**的组合设计，而非简单地将两种条件拼接输入单一网络。

- **双分支DiT**：图像分支和文本分支各自由独立的DiT（Diffusion Transformer）主干构成，分别接收图像条件 $\mathbf{I}$ 和文本条件 $\mathbf{T}$，在共享的潜在空间中预测速度场 $\mathbf{v}_{\mathrm{img}}$ 和 $\mathbf{v}_{\mathrm{txt}}$。两分支均基于 UniLat3D 的预训练权重初始化，图像分支直接复用其 DINO 编码器，文本分支则将条件编码器替换为 CLIP 文本编码器后从头训练。这种设计保留了各模态专属的特征提取能力，避免了模态间的表示冲突。

- **零初始化跨模态桥接（Zero Linears）**：在每层DiT块之间，通过线性投影 $\mathcal{P}_{\mathrm{txt}\to\mathrm{img}}^{(i)}$ 和 $\mathcal{P}_{\mathrm{img}\to\mathrm{txt}}^{(i)}$ 将文本分支特征注入图像分支、反之亦然：

$$\mathbf{f}_{\mathrm{img}}^{(i),\prime} = \mathbf{f}_{\mathrm{img}}^{(i)} + \mathcal{P}_{\mathrm{txt}\to\mathrm{img}}^{(i)}(\mathbf{f}_{\mathrm{txt}}^{(i)}), \quad \mathbf{f}_{\mathrm{txt}}^{(i),\prime} = \mathbf{f}_{\mathrm{txt}}^{(i)} + \mathcal{P}_{\mathrm{img}\to\mathrm{txt}}^{(i)}(\mathbf{f}_{\mathrm{img}}^{(i)})$$

**所有跨模态桥接在初始化时权重为零**，这一设计具有关键的战略意义：训练初期，桥接不产生任何贡献，模型行为等价于两个独立分支的简单平均（SimFusion），从而保护了预训练权重不被破坏；随着训练推进，桥接逐步学习有意义的跨模态特征注入，使两分支在去噪过程中保持对齐。

### 3. 融合策略：早期特征注入 + 晚期预测平均

TIGON 采用**早期融合与晚期融合相结合**的双层融合策略，这是其性能超越简单基线（SimFusion）的关键。

- **早期融合**：通过上述跨模态桥接，在每一层DiT块中实现细粒度的特征级信息交换。消融实验（Table 3）表明，去除桥接后，仅靠晚期预测平均，FDDINOv2 从 61.59 升至 66.04，性能增益极为有限；加入桥接则使 FDDINOv2 从 66.78 降至 61.59，证明**早期融合是不可或缺的性能驱动因素**。定性分析（Figure 7）进一步揭示其机制：无桥接时，两分支在去噪过程中逐渐发散，生成异常结构；有桥接时，分支保持对齐，最终生成一致的高质量3D资产。

- **晚期融合**：在每个去噪步，对两分支预测的速度场取简单平均：

$$\mathbf{v} = \frac{1}{2}(\mathbf{v}_{\mathrm{txt}} + \mathbf{v}_{\mathrm{img}})$$

消融实验对比了三种晚期融合策略——简单平均（Sim）、自适应加权（AW）和自适应变换（AT）。在已有早期融合和联合微调的条件下，三者性能差异微小（FDDINOv2 分别为 61.59、60.90、62.00），表明**简单平均已接近该框架下的融合上限**，更复杂的可学习融合策略未能带来额外增益。

### 创新本质：轻量级互补信号整合

TIGON 的创新本质可归结为一个核心洞察：**图像提供精确的视角对齐外观与几何线索，文本提供高层语义以消歧未观察区域；通过显式早期特征融合与后期预测平均，可在不破坏单模态能力的前提下整合互补信息**。这一设计哲学体现在三个技术选择上：双分支而非单分支（保护模态特异性）、零初始化桥接而非随机初始化（保护预训练权重）、简单预测平均而非可学习融合（避免过拟合）。最终，TIGON 以极简的架构增量（仅增加线性投影层和条件丢弃机制）实现了对单模态基线的显著超越。



TIGON 的整体框架围绕一个核心洞见构建：**图像条件提供精确的视角对齐外观与几何线索，文本条件提供高层语义以消歧未观察区域**，两者天然互补。为实现这一互补，TIGON 采用双分支 DiT 架构，在不破坏各分支单模态能力的前提下，通过轻量级的早期特征融合与晚期预测平均将两路信号整合为统一的生成过程。

### Pipeline 总览

整个生成流程分为三个关键阶段：

1. **潜在编码**：输入图像 $\mathbf{I}$ 和文本 $\mathbf{T}$ 分别被编码后，与噪声化的 3D 潜在表示 $\tilde{\mathbf{z}}$ 一同送入双分支主干网络。潜在空间沿用 UniLat3D 的统一编码 $\mathbf{z}_{\mathrm{uni}} \in \mathbb{R}^{16 \times 16 \times 16 \times c}$（Eq. 5），保证两分支在相同的表示空间内操作，为后续的简单加性融合奠定基础。

2. **双分支去噪预测**：图像分支 $\mathcal{F}_{\mathrm{img}}$ 和文本分支 $\mathcal{F}_{\mathrm{txt}}$ 各自独立预测速度场：
   $$\mathbf{v}_{\mathrm{img}} = \mathcal{F}_{\mathrm{img}}(\tilde{\mathbf{z}}, t, \mathbf{I}), \quad \mathbf{v}_{\mathrm{txt}} = \mathcal{F}_{\mathrm{txt}}(\tilde{\mathbf{z}}, t, \mathbf{T})$$
   两分支均基于 UniLat3D 的 DiT 骨干，其中文本分支将原 DINO 条件编码器替换为 CLIP 文本编码器。在去噪过程的每一步，两分支通过**跨模态桥接**实现逐层特征交换（早期融合）。

3. **预测融合与解码**：最终速度场由两分支预测取平均得到：
   $$\mathbf{v} = \frac{1}{2}(\mathbf{v}_{\mathrm{txt}} + \mathbf{v}_{\mathrm{img}})$$
   该速度场驱动去噪过程，解码后输出 3D 资产（支持网格和 3DGS 两种表示）。训练时通过**条件丢弃**独立屏蔽图像或文本条件，使模型能够在推理时灵活处理仅图像、仅文本或联合条件三种模态组合，避免评估时的模态偏差。

### 跨模态桥接：早期融合的关键机制

Figure 3 展示了双分支架构中跨模态桥接的具体位置：在每层 DiT 块之间，图像分支的特征 $\mathbf{f}_{\mathrm{img}}^{(i)}$ 和文本分支的特征 $\mathbf{f}_{\mathrm{txt}}^{(i)}$ 通过零初始化的线性投影相互注入：
$$\mathbf{f}_{\mathrm{img}}^{(i),\prime} = \mathbf{f}_{\mathrm{img}}^{(i)} + \mathcal{P}_{\mathrm{txt}\to\mathrm{img}}^{(i)}(\mathbf{f}_{\mathrm{txt}}^{(i)}), \quad \mathbf{f}_{\mathrm{txt}}^{(i),\prime} = \mathbf{f}_{\mathrm{txt}}^{(i)} + \mathcal{P}_{\mathrm{img}\to\mathrm{txt}}^{(i)}(\mathbf{f}_{\mathrm{img}}^{(i)})$$

![[assets/figures/papers/paper_list_l2608_https_arxiv_org_abs_2603_21295/figures/003_Figure_3.jpg]]
*Figure 3: TIGON employs a dual-branch architecture, with a text-conditioned DiT (left) and an image-conditioned DiT (right). Paired blocks exchange features via cross-modal bridges (“Zero Linears”). At each denoising step, two predictions are averaged to produce the velocity field v. T denotes the denoising timestep*

**零初始化**是这一设计的核心约束：训练初期桥接权重为零，保证两分支在融合前保持各自的预训练能力不被破坏；随着训练推进，桥接逐步学习注入互补信息。消融实验证实，缺少桥接时两分支预测在去噪过程中发散，产生异常结构（Figure 7），而加入桥接后分支保持对齐，FDDINOv2 从 66.78 降至 61.59（Table 3），性能增益显著。

### 融合策略的选择

在已有早期桥接和联合微调的前提下，TIGON 采用最简单的**预测平均**作为晚期融合策略。消融实验表明，更复杂的可学习融合策略（注意力加权、自适应融合）仅带来微小波动（Table 3：Sim 61.59，AW 60.90，AT 62.00），暗示简单平均在当前架构下已接近性能上限。这一发现说明，早期逐层特征交换已经为两分支提供了充分的跨模态对齐，晚期融合只需做轻量级整合即可。

### 诊断性验证：互补性的直接证据

为验证图像与文本的互补性，论文设计了 SimFusion 基线——直接将预训练的图像条件模型和文本条件模型的速度场预测取平均，不做任何联合训练。在低信息视角（View-1）下，SimFusion 的 FDDINOv2 达到 82.40，远优于纯图像模型 TRELLIS 的 143.58 和纯文本模型的 145.06（Table 1）。这一结果直接证明：**即使是最简单的晚期融合，也能使两模态互补信号产生显著增益**，为 TIGON 的整体设计提供了坚实的动机基础。

### 补充图表

![[assets/figures/papers/paper_list_l2608_https_arxiv_org_abs_2603_21295/figures/001_Figure_1.jpg]]
*Figure 1: Single-modality conditioning has limitations in satisfying user intent. Image-only conditioning captures local appearance but omits unobserved regions; text-only conveys semantics but lacks visual fidelity. In contrast, joint text–image conditioning produces 3D assets that are both semantically aligned with the description and faithful to the reference appearance*



TIGON 的核心架构由四个关键模块构成：双分支 DiT 主干、零初始化跨模态桥接（早期融合）、预测速度场平均（晚期融合）以及条件丢弃训练策略。以下逐一展开其设计逻辑与关键公式。

### 双分支 DiT 主干

TIGON 继承 UniLat3D 的统一潜在空间，将视图聚合特征 $\mathbf{F}$ 编码为结构化的 3D 潜在表示：

$$\mathbf{z}_{\mathrm{uni}} = \mathcal{E}_{\mathrm{uni}}(\mathbf{F}), \quad \mathbf{z}_{\mathrm{uni}} \in \mathbb{R}^{16 \times 16 \times 16 \times c}$$

在此共享潜在空间之上，TIGON 构建两条并行的 DiT 分支：图像分支接收参考图像 $\mathbf{I}$ 作为条件，文本分支接收文本提示 $\mathbf{T}$ 作为条件。在去噪过程的每一步 $t$，两分支分别预测各自的速度场：

$$\mathbf{v}_{\mathrm{img}} = \mathcal{F}_{\mathrm{img}}(\tilde{\mathbf{z}}, t, \mathbf{I}), \quad \mathbf{v}_{\mathrm{txt}} = \mathcal{F}_{\mathrm{txt}}(\tilde{\mathbf{z}}, t, \mathbf{T})$$

其中 $\tilde{\mathbf{z}}$ 为当前时刻的噪声潜在表示。两分支均基于相同的 UniLat3D 骨干网络，文本分支仅将其 DINO 条件编码器替换为 CLIP 文本编码器，从而确保两分支在共享潜在空间中操作，为后续的简单加性融合奠定基础。

### 零初始化跨模态桥接（早期融合）

若两分支完全独立运行，去噪轨迹将逐渐发散，导致最终生成的 3D 结构出现语义不一致。TIGON 在每一层 DiT 块之间插入双向线性投影，实现细粒度的跨模态特征注入：

$$\mathbf{f}_{\mathrm{img}}^{(i),\prime} = \mathbf{f}_{\mathrm{img}}^{(i)} + \mathcal{P}_{\mathrm{txt}\to\mathrm{img}}^{(i)}(\mathbf{f}_{\mathrm{txt}}^{(i)}), \quad \mathbf{f}_{\mathrm{txt}}^{(i),\prime} = \mathbf{f}_{\mathrm{txt}}^{(i)} + \mathcal{P}_{\mathrm{img}\to\mathrm{txt}}^{(i)}(\mathbf{f}_{\mathrm{img}}^{(i)})$$

其中 $\mathbf{f}_{\mathrm{img}}^{(i)}$ 和 $\mathbf{f}_{\mathrm{txt}}^{(i)}$ 分别表示第 $i$ 层图像分支和文本分支的中间特征，$\mathcal{P}_{\mathrm{txt}\to\mathrm{img}}^{(i)}$ 和 $\mathcal{P}_{\mathrm{img}\to\mathrm{txt}}^{(i)}$ 为对应的线性投影。**所有跨模态桥接在训练初期均以零初始化**，这一设计确保融合能力从零开始逐步习得，避免在训练早期破坏各分支已预训练好的单模态表征能力。消融实验（Table 3）证实：缺少桥接时，联合微调仅带来微弱增益（FD_DINOv2 从 66.78 降至 66.04）；启用桥接后，FD_DINOv2 进一步降至 61.59，性能提升显著。

### 预测速度场平均（晚期融合）

在每步去噪的末端，TIGON 对两分支预测的速度场取简单算术平均，得到最终速度场：

$$\mathbf{v} = \frac{1}{2}(\mathbf{v}_{\mathrm{txt}} + \mathbf{v}_{\mathrm{img}})$$

这一设计基于两分支共享同一潜在空间的事实，无需引入可学习参数。消融实验表明，在已有早期融合和联合微调的前提下，简单平均（Sim）已接近最优（FD_DINOv2 61.59），更复杂的注意力加权（AW, 60.90）或自适应融合（AT, 62.00）仅带来微小波动，未能带来统计显著的进一步提升。这暗示简单平均在当前框架下可能已逼近融合策略的性能上限。

### 条件丢弃训练

为使单一模型能灵活处理仅图像、仅文本或联合条件等多种推理场景，TIGON 在训练阶段独立地随机丢弃图像条件或文本条件（条件丢弃）。这一策略使模型学会在缺失某一模态时仍能产生合理预测，避免了评估阶段的模态偏差问题。

### 补充图表

![[assets/figures/papers/paper_list_l2608_https_arxiv_org_abs_2603_21295/figures/009_Figure_7.jpg]]
*Figure 7: Effect of early fusion. Without cross-modal bridges, the two branches diverge during denoising. Full text prompt is available in the supplement*



## 实验与关键发现

### 瓶颈诊断：单模态条件的信息脆弱性

TIGON的核心动机源于一个简洁的诊断实验。作者在Toys4K基准上，分别使用高信息量的参考视角（View-0）和低信息量的参考视角（View-1，可观测线索显著减少）对现有图像条件模型进行测试（图2）。结果表明，当视角信息量下降时，图像条件模型的性能急剧退化：TRELLIS的FDDINOv2从56.08飙升至143.58，UniLat3D从57.59升至114.75（表1）。文本条件模型虽然不受视角限制，但缺乏像素级视觉约束，生成质量始终处于低位（UniLat3D文本条件FDDINOv2为154.88）。

这一诊断揭示了当前3D生成的核心瓶颈：图像条件模型对视角信息量高度敏感，未观察区域会产生语义偏离的幻觉；文本条件模型提供全局语义但无法保证视觉保真度。两种模态的互补性由此凸显——图像提供精确的视角对齐外观与几何线索，文本提供高层语义以消歧未观察区域。

### SimFusion：一个简单的晚期融合基线

为验证模态互补假设，作者首先构造了一个极简基线SimFusion：在去噪过程的每一步，直接对图像条件和文本条件两个独立整流流模型预测的速度场取平均。在低信息视角（View-1）下，SimFusion的FDDINOv2降至82.40，大幅优于图像单模态的TRELLIS（143.58）和文本单模态模型（145.06）。这一结果直接证明：图像与文本信号高度互补，即使是最简单的晚期融合也能显著提升低信息条件下的生成鲁棒性。

### TIGON主结果：跨模态融合的定量增益

在Toys4K和UniLat1K两个基准上，TIGON（联合文本-图像条件）一致优于所有单模态对比方法（表2）。以3DGS表示为例，TIGON在Toys4K上取得FDDINOv2 61.59，相比图像条件的UniLat3D（85.30）降低23.71，相比文本条件的UniLat3D（145.06）降低83.47。在语义一致性指标上，TIGON的CLIP得分（92.33）同样优于文本条件模型（86.14），提升6.19。在UniLat1K上，TIGON的FDDINOv2为130.08，较图像条件UniLat3D（155.99）降低25.91。网格表示下的结果趋势一致，TIGON在CLIP（92.97）、ULIP（41.36）等指标上均取得最优。

定性对比（图4）进一步印证：图像单模态模型虽能保持参考视角的外观，但在未观察区域产生明显伪影（虚线框标注）；文本单模态模型缺乏像素对齐的线索，几何与外观保真度低。TIGON则同时保持了参考视角的视觉忠实度和全局语义一致性。

### 消融实验：跨模态桥接是关键

消融实验（表3）系统拆解了TIGON各组件的贡献，核心发现如下：

**零初始化跨模态桥接至关重要。** 在已有联合微调（FT）和简单预测平均（Sim）的条件下，加入跨模态桥接使FDDINOv2从66.78降至61.59；而无桥接时，联合微调仅带来微弱增益（66.78→66.04）。定性分析（图7）揭示了其作用机制：无桥接时，图像分支与文本分支在去噪过程中逐渐发散，最终生成异常结构；加入桥接后，两分支在去噪全程保持对齐，生成结果正常。

**简单预测平均已接近最优。** 在已有早期融合（桥接）和联合微调的前提下，三种晚期融合策略——简单平均（Sim，61.59）、可学习注意力加权（AW，60.90）、可学习注意力变换（AT，62.00）——性能差异极小。这表明早期跨模态桥接已使两分支预测高度对齐，复杂的可学习晚期融合无法带来额外增益，反而可能引入微小波动。

**与TRELLIS的集成兼容性。** 表A1展示了将TIGON的跨模态桥接集成到TRELLIS框架中的实验结果。受限于计算资源，仅对稀疏结构流（sparse-structure flow）添加跨模态桥接（ssbridge），未对SLAT流进行融合。即便如此，该集成仍使FDDINOv2从TRELLIS图像条件的143.58降至联合条件的109.24，验证了TIGON融合策略的框架通用性。作者指出，完整集成可能需要更多计算资源。

### 可控生成与模态冲突行为

TIGON支持通过固定图像、变化文本实现可控生成（图5），以及处理图像与文本显式冲突的场景（图6）。当文本描述与参考图像不一致时（如文本要求“蓝色”而图像为“红色”），TIGON倾向于偏向图像条件，这在消歧未观察区域时是合理的设计选择。但论文未对这种冲突场景下的动态权衡策略进行定量分析，是否存在更优的模态权重调节机制仍是一个开放问题。

### 局限性与待验证问题

论文未设置专门的局限性章节，但综合实验分析可识别以下边界：

1. **晚期融合上限**：更复杂的可学习融合策略未能超越简单平均，暗示当前框架的融合增益可能已接近饱和。
2. **计算资源约束**：与TRELLIS的完整集成受限于资源，仅对部分流添加桥接，完整集成的性能上限未知。
3. **数据规模泛化**：训练数据量为TRELLIS-500K，在更大规模、更开放域的3D数据集上，文本-图像联合条件的互补增益能否保持尚待验证。
4. **表示形式拓展**：当前验证限于3DGS和网格，该方法能否推广至NeRF、SDF等其他3D表示形式仍需探索。

### 补充图表

![[assets/figures/papers/paper_list_l2608_https_arxiv_org_abs_2603_21295/figures/002_Figure_2.jpg]]
*Figure 2: Reference views used in our diagnostic study. Moving from View-0 to View-1 reduces observable cues and creates a lower-information setting. Under this shift, single-modality baselines exhibit a marked performance drop*

![[assets/figures/papers/paper_list_l2608_https_arxiv_org_abs_2603_21295/figures/004_Table_1.jpg]]
*Table 1: Performance of existing methods on the Toys4K dataset under different conditioning signals. ‘GS’ denotes that the 3D representation is 3DGS*

![[assets/figures/papers/paper_list_l2608_https_arxiv_org_abs_2603_21295/figures/005_Table_2.jpg]]
*Table 2: Quantitative results on Toys4K (left) and UniLat1K (right). “Cond.” denotes conditioning modality (“I”: image, “T”: text), and “Rep.” denotes output representation (“M.”: mesh, “GS”: 3DGS)*

![[assets/figures/papers/paper_list_l2608_https_arxiv_org_abs_2603_21295/figures/010_Table_3.jpg]]
*Table 3: Ablations on Toys4K. “Bridges” denotes zero-initialized cross-modal bridges; “Sim”, “AW”, and “AT” denote three fusion strategies; “FT” denotes joint fine-tuning. The TIGON setting is highlighted in light gray*

![[assets/figures/papers/paper_list_l2608_https_arxiv_org_abs_2603_21295/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison on Toys4K and UniLat1K against image-only and text-only variants of TRELLIS and UniLat3D. Dashed boxes mark artifacts from prior methods. Image-only models respect the reference view but must hallucinate unseen regions, while textonly models lack pixel-aligned cues and often produce low-fidelity geometry and appearance. Full prompts are provided in the supplement*

![[assets/figures/papers/paper_list_l2608_https_arxiv_org_abs_2603_21295/figures/007_Figure_5.jpg]]
*Figure 5: Controllable generation under text and image conditions*

![[assets/figures/papers/paper_list_l2608_https_arxiv_org_abs_2603_21295/figures/008_Figure_6.jpg]]
*Figure 6: Generation with conflicting text-image conditions*

![[assets/figures/papers/paper_list_l2608_https_arxiv_org_abs_2603_21295/figures/011_Figure.jpg]]
*Figure: A1. The adaptive fusion module used in the ablation study. D denotes the intermediate feature dimension, and C denotes the latent output dimension*

![[assets/figures/papers/paper_list_l2608_https_arxiv_org_abs_2603_21295/figures/012_Table.jpg]]
*Table: A1. Integrating TIGON with TRELLIS. Experiment is conducted on Toys4K. We use 3D-GS as the representation. ‘ssbridge’ denotes the cross-modal bridge for the sparse-structure flow model*



## 定位与知识库关联

### 1. 基线谱系与定位

TIGON 处于**多模态条件3D生成**的交叉点上，其直接基线可沿两条轴分解：条件模态与生成架构。

**条件模态轴**。现有方法几乎全部依赖单一模态条件。图像条件模型以 **TRELLIS**（Xiang et al., CVPR 2025）和 **UniLat3D** 为代表，能够从参考视角重建局部外观与几何，但对未观察区域产生语义偏离的幻觉；诊断实验表明，当参考视角从信息丰富的 View-0 切换至低信息的 View-1 时，TRELLIS 的 FD_DINOv2 从 56.08 急剧退化至 143.58（Table 1）。文本条件模型如 TRELLIS 和 UniLat3D 的文本变体，提供全局语义但缺乏像素级视觉约束，FD_DINOv2 达 145.06–154.88，视觉质量显著低于图像条件对应物。TIGON 首次将两类模态联合注入原生3D生成流程，通过互补信号弥合了保真度与语义一致性的鸿沟。

**融合策略轴**。论文提出的 **SimFusion** 基线——在去噪每一步直接平均图像分支与文本分支预测的速度场——是理解 TIGON 贡献的关键参照点。SimFusion 本身已展现出跨模态互补的巨大潜力：在 View-1+Text 条件下，其 FD_DINOv2 为 82.40，远优于图像单模态的 143.58 和文本单模态的 145.06（Table 1）。这验证了核心假设：图像提供视角对齐的外观与几何线索，文本消歧未观察区域的语义。TIGON 在此基础上引入**零初始化跨模态桥接**（早期融合），使两分支在每层 DiT 块间双向注入特征，将 FD_DINOv2 从 66.78 进一步降至 61.59（Table 3）。

**架构轴**。与需要从头设计联合编码器的方案不同，TIGON 采用**双分支 DiT 架构**：图像分支复用 UniLat3D 预训练权重，文本分支替换 DINO 编码器为 CLIP 文本编码器后从头训练 1M 迭代，两者共享同一潜在空间，使简单加性融合成为可能。这种“预训练单模态分支 + 轻量跨模态桥接”的范式，在保持各分支独立能力的同时实现了有效融合。

### 2. 与相关工作的关系

**与 TRELLIS 的关系**。TIGON 在实现上基于 TRELLIS 和 UniLat3D 框架，但并非简单扩展。论文进一步验证了 TIGON 与 TRELLIS 的集成兼容性：对 TRELLIS 的稀疏结构流（sparse-structure flow）添加跨模态桥接后，在 Toys4K 上同样获得增益（Table A1）。这表明 TIGON 的融合机制具有跨架构迁移潜力，尽管受限于计算资源，未对 SLAT 流进行完整集成。

**与通用多模态融合方法的区别**。TIGON 的融合设计刻意保持极简。消融实验表明，在已有早期桥接和联合微调的前提下，简单的预测平均（SimFusion）即可达到最优，更复杂的可学习自适应融合模块（注意力加权 AW、注意力变换 AT）仅带来微小波动（AW: 60.90, AT: 62.00 vs. Sim: 61.59，Table 3），说明当前简单融合策略可能已接近性能上限。这与多模态学习中常见的“复杂融合优于简单融合”的直觉形成对比，暗示在共享潜在空间且分支充分预训练的条件下，晚期线性融合已足够捕获互补信息。

**与3D重建/生成模型的关系**。TIGON 在 Toys4K 和 UniLat1K 上与 **TripoSR**、**Step1X-3D+**、**Hunyuan3D-2.1**、**Stable3DGen**、**Direct3D-S2** 等图像条件模型进行了系统对比（Table 2）。值得注意的是，Hunyuan3D-2.1 使用了非公开训练数据，论文在评估中对此进行了标注以确保公平性。

### 3. 适用边界与局限

**数据规模边界**。TIGON 的文本分支在 TRELLIS-500K 数据集上训练，该数据集规模相对有限。在更大规模、更多样化的开放域3D数据上，文本-图像联合条件的互补增益能否保持，尚缺乏实验验证。

**冲突条件处理**。当图像与文本显式冲突时，TIGON 目前倾向于硬性偏向图像条件（Figure 6）。这种设计在参考图像可信度高的场景下合理，但在图像质量差或用户意图主要由文本表达时可能次优。是否存在更灵活的动态权衡策略（如基于图像信息量的自适应加权）仍是一个开放问题。

**计算开销**。双分支架构在推理时需同时运行两个 DiT 主干，计算量约为单模态模型的两倍。跨模态桥接虽为轻量线性投影，但在深层网络中累积的通信开销不可忽略。论文未探讨自适应稀疏连接或分支共享等降低开销的方案。

**表示形式与框架泛化**。当前实现基于 UniLat3D 的统一潜在表示（$z_{uni} \in \mathbb{R}^{16 \times 16 \times 16 \times c}$），输出为 Mesh 或 3DGS。该方法能否推广至其他3D表示（如 NeRF、SDF）或其他生成框架（如扩散模型、自回归模型），仍需进一步研究。

### 4. 开放问题

1. **大规模开放域泛化**：在更大规模、更多样化的3D数据集上，文本-图像联合条件能否保持互补增益？文本分支的语义理解能力是否受限于训练数据的语义丰富度？

2. **冲突条件的动态权衡**：当图像与文本显式冲突时，除硬性偏向图像外，能否设计基于不确定性估计或图像信息量的自适应融合权重？

3. **计算效率优化**：跨模态桥接是否可以设计为自适应稀疏连接，或通过分支共享部分层来降低推理开销？在资源受限场景下，能否实现单分支退化的无缝切换？

4. **表示与框架迁移**：该方法能否推广至其他3D表示形式（如 NeRF、SDF）或其他生成框架（如扩散模型、流匹配模型）？零初始化桥接策略在其他潜在空间中的有效性如何？

5. **融合上限的本质**：消融实验显示复杂晚期融合未能超越简单平均，这是否意味着当前双分支架构已达到跨模态互补的信息上限，还是更精细的早期融合设计（如跨注意力、动态路由）可能突破这一瓶颈？



## 原文 PDF

![[paperPDFs/CVPR_2026/Text_Image_Conditioned_3D_Generation.pdf]]
