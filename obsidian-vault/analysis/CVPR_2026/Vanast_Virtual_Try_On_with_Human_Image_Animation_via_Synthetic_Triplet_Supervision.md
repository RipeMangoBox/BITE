---
title: "Vanast: Virtual Try-On with Human Image Animation via Synthetic Triplet Supervision"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Vanast_Virtual_Try_On_with_Human_Image_Animation_via_Synthetic_Triplet_Supervision.pdf
project_link: "https://hyunsoocha.github.io/vanast/"
code_link: "https://github.com/blackforest-labs/flux"
aliases:
- Vanast
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: "通过合成三元组监督（生成穿着不同服装的人类图像 I^{G'}，并从野外视频提取服装图像 G）构建大规模训练数据；同时采用双模块架构，将人体动画条件（HAM）与服装转移条件（GTM）解耦并注入冻结的文本到视频扩散主干，以实现稳定训练并独立控制两个关键因素。"
primary_logic: 生成身份保留但穿着替代服装的人类图像，使得模型被迫学习服装转移而非简单模仿动画；双模块注入策略在不破坏预训练生成质量的前提下，显著提高了服装精度、姿势遵循和身份保持，并天然支持零样本服装插值。
claims:
- "合成三元组训练是必要的：消融实验去除 I^{G'} 导致服装转移失败，完整模型在所有指标上显著优于 w/o SynthHuman 变体。"
- 双模块架构优于单模块或主干 LoRA 方案：定量结果（Table 3）显示 Vanast 在 L1、PSNR、SSIM、LPIPS、FID、VFID 上均取得最佳性能；定性上，单模块无法控制姿势，主干 LoRA 和 w/o SynthHuman 无法准确转移服装（Fig. 7）。
- Vanast 在统一的端到端框架中优于所有两阶段组合基线：在 Internet 数据集上，我们的方法在所有评估指标上均优于 Subject-to-Image + Animation 和 VTON + Animation 的组合，定性比较（Fig. 4, Fig. 5）也显示结果最接近真值。
- 双模块架构支持零样本服装插值：通过 GTM 输出的加权求和，可在无额外训练的情况下实现平滑的服装样式过渡（Fig. 10）。
---

# Vanast: Virtual Try-On with Human Image Animation via Synthetic Triplet Supervision

> [!tip] 核心洞察
> 生成身份保留但穿着替代服装的人类图像，使得模型被迫学习服装转移而非简单模仿动画；双模块注入策略在不破坏预训练生成质量的前提下，显著提高了服装精度、姿势遵循和身份保持，并天然支持零样本服装插值。

| 字段 | 内容 |
|------|------|
| 中文题名 | Vanast：基于合成三元组监督的虚拟试穿人物动画 |
| 英文题名 | Vanast: Virtual Try-On with Human Image Animation via Synthetic Triplet Supervision |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.04934) · [Project](https://hyunsoocha.github.io/vanast/) · [Code](https://github.com/blackforest-labs/flux) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Vanast |
| Dataset | Ablation on Lower Garment Transfer, Internet Dataset (80 samples) vs. two-stage pipelines, Qualitative comparison on posed video generation |

> [!tip] 效果简介
> - Ablation on Lower Garment Transfer (Internet Dataset) 上，L1 ↓ / PSNR ↑ / SSIM ↑ / LPIPS ↓ / FID ↓ / VFIDI3D ↓ / VFIDResNeXt ↓ 0.1069 / 14.74 / 0.6657 / 0.3673 / 104.59 / 35.60 / 1.21 vs Single Module: 0.1162 / 14.28 / 0.6609 / 0.3974 / 108.84 / 39.64 / 1.76; Backbo... (improvements across all metrics (best scores in bold))。
> - Internet Dataset (80 samples) vs. two-stage pipelines 上，All metrics (L1, PSNR, SSIM, LPIPS, FID, VFID) Best scores across all metrics vs Combinations of Subject-to-Image (Mosaic, VisualCloze, Less-to-More) or VTON (O... (N/A (optimal in all metrics))。
> - Qualitative comparison on posed video generation 上，visual fidelity, pose following, garment transfer, identity preservation Most accurate pose following and garment transfer, best identity preservation vs Two-stage pipelines (subject-to-image + animation; VTON + animation) (significantly better visual results)。

## 概要

现有虚拟试穿人物动画方法普遍采用**两阶段流水线**：先进行虚拟试穿生成穿着目标服装的单帧图像，再以该图像为输入驱动人物动画。这一范式存在根本性瓶颈——**身份漂移、服装变形以及前后视图不一致**，原因在于两阶段之间缺乏联合优化，服装转移与运动生成被割裂处理。更深层的问题是：学术界缺乏包含**不同服装的人类图像与对应视频的三元组训练数据**，使得端到端学习服装转移与动画的联合生成长期不可行。

**Vanast** 的核心洞察是：通过**合成三元组监督**打破数据瓶颈，并采用**双模块架构**将人体动画条件与服装转移条件解耦注入冻结的文本到视频扩散主干，从而在一个统一的端到端框架内同时解决身份保持、服装精度和姿势遵循三个相互冲突的目标。

具体而言，Vanast 做出了以下关键贡献：

1. **合成三元组数据集生成流水线**：生成身份保留但穿着替代服装的人类图像 $I^{G'}$，并从野外视频提取服装图像 $G$，构造大规模三元组训练数据。这迫使模型学习真正的服装转移，而非简单复现视频中已有的服装-运动耦合。消融实验证实，去除 $I^{G'}$ 后服装转移完全失败。

2. **双模块架构**：将条件注入拆分为**人体动画模块（HAM）**和**服装转移模块（GTM）**，两者输出以加性方式每两个 DiT 块注入一次冻结的 T2V 主干。相比单模块串联或主干 LoRA 方案，该设计在不破坏预训练生成质量的前提下，显著提升了服装精度、姿势遵循和身份保持，并天然支持零样本服装插值。

3. **全面的实验验证**：在 Internet 数据集上，Vanast 在所有评估指标（L1、PSNR、SSIM、LPIPS、FID、VFID）上均优于由主体到图像模型（如 **Mosaic** (She et al., arXiv 2025)、**VisualCloze** (Li et al., arXiv 2025)）或虚拟试穿模型（如 **OOTDiffusion** (Xu et al., AAAI 2025)、**CatVTON** (Chong et al., arXiv 2024)）与动画模型（如 **Champ** (Zhu et al., ECCV 2024)、**StableAnimator** (Tu et al., CVPR 2025)）构成的所有两阶段组合基线，定性比较也显示出最优的视觉保真度。

虚拟试穿人物动画（Virtual Try-On with Human Image Animation）旨在将目标服装图像转移到给定人物图像上，并同时驱动该人物按照指定的姿势序列生成连贯的动画视频。这一任务在电子商务、虚拟时尚和数字人内容创作中具有广泛的应用前景。然而，现有方法普遍采用**两阶段流水线**：先执行图像级虚拟试穿（VTON）或主体到图像（Subject-to-Image）生成，再将结果输入独立的动画模型。这种解耦范式带来了三个核心瓶颈：

1. **身份漂移**：两阶段模型各自优化独立目标，动画阶段可能改变第一阶段生成的人物身份特征，导致最终视频中的人物与原始输入不一致。
2. **服装变形与细节丢失**：动画模型在处理带有复杂纹理、Logo 或特定款式的服装时，容易产生几何扭曲和纹理模糊，因为其训练目标并未显式约束服装保真度。
3. **前后视图不一致**：由于缺乏端到端的联合优化，服装在不同帧之间的外观可能发生抖动或突变，破坏了视频的时间连贯性。

上述问题的根源在于**训练数据的结构性缺失**：现有数据集通常只包含穿着特定服装的人物视频，缺乏“同一人物穿着不同服装、且对应相同姿势序列”的三元组数据。这使得模型无法直接学习“服装转移”与“动画生成”之间的联合映射，只能退而求其次地采用分阶段近似。

针对这一缺口，本文提出 **Vanast**——一个端到端的统一框架，直接从人物图像、服装图像和姿势视频合成服装转移后的人物动画。Vanast 的核心动机在于：通过构建**合成三元组监督**来填补数据空白，并设计**双模块条件注入架构**以在冻结的预训练文本到视频扩散主干上独立控制人体动画与服装转移两个关键因素，从而在保持预训练生成质量的前提下，实现高保真的服装精度、姿势遵循和身份保持。

## 核心方法与创新机理

Vanast 的核心创新在于**将虚拟试穿与人物动画从两阶段级联范式重构为统一的端到端生成框架**，并通过两个相互协同的设计突破实现了这一目标：合成三元组监督数据构建与双模块条件注入架构。

### 1. 瓶颈洞察：两阶段级联的身份漂移与服装变形

现有方法普遍采用“先虚拟试穿、再动画生成”的两阶段流水线，或“先生成主体图像、再驱动动画”的组合方案。这一范式存在根本性缺陷：第一阶段的人体/服装生成误差会在第二阶段被放大，导致**身份漂移**（人物面部与身体特征不一致）、**服装变形**（纹理扭曲或细节丢失）以及**前后视图不一致**（服装在不同帧间出现跳变）。其深层原因在于，两个阶段独立优化，缺乏对服装转移与动画生成的联合建模，模型无法理解“同一人物穿着特定服装执行特定动作”的全局一致性约束。

更关键的是，**训练数据的结构性缺失**进一步固化了这一瓶颈：现有数据集要么只包含穿着固定服装的人类视频，要么只提供静态的虚拟试穿图像对，缺乏“同一人物穿着不同服装的多视角动作视频”这样的三元组监督信号，使得端到端学习服装转移与动画的联合生成在数据层面不可行。

### 2. 合成三元组监督：迫使模型学习服装转移而非运动复现

Vanast 的核心洞察是：**通过生成身份保留但穿着替代服装的人类图像** $I^{G'}$，可以构造出 $(G, I^{G'}, K)$ 三元组训练数据，其中 $G$ 是从野外视频中提取的目标服装图像，$K$ 是姿势序列，而 $I^{G'}$ 中的服装 $G'$ 与目标服装 $G$ 不同。这一设计的关键在于，模型无法通过简单地“模仿输入人类图像的外观”来完成生成任务——因为输入人物穿着的服装与目标服装不一致，模型必须真正学会**解耦身份与服装**，将目标服装 $G$ 准确地转移到输入人物的身体上，同时遵循姿势序列 $K$ 的引导。

消融实验有力地验证了这一机制的必要性：去除合成人类图像（w/o SynthHuman）的变体在所有指标上显著劣于完整模型（Table 3），定性结果显示其无法完成准确的服装转移（Fig. 7）。这表明，合成三元组监督并非简单的数据增强，而是**改变了模型的学习目标**——从“复现输入图像的外观”转变为“执行服装转移操作”。

### 3. 双模块条件注入：解耦动画控制与服装转移

在架构层面，Vanast 提出了**双模块（Dual Module）架构**，将人体动画条件与服装转移条件注入到冻结的文本到视频（T2V）扩散主干中，通过独立的人体动画模块（Human Animation Module, HAM）和服装转移模块（Garment Transfer Module, GTM）分别处理两类异质性条件。

具体而言，HAM 接收人类图像 $I^{G'}$ 和姿势序列 $K$，生成人体动画的条件表示；GTM 接收服装图像 $G$，生成服装转移的条件表示。两个模块的输出以加性方式注入主干 DiT 的特定层（每两个块注入一次）：

$$h_{l+1} = \begin{cases} \mathrm{B}_l^{\mathrm{T2V}}(h_l), & \text{if } l \neq 2k, \\ \mathrm{B}_l^{\mathrm{T2V}}(h_l) + \alpha \cdot \mathrm{B}_l^{\mathrm{HAM}}(h_l) + \beta \cdot \mathrm{B}_l^{\mathrm{GTM}}(h_l), & \text{otherwise} \end{cases}$$

这一设计与现有方案形成鲜明对比：

| 条件注入方式 | 基线方案 | Vanast |
|---|---|---|
| 条件融合策略 | 所有条件串联或通过单个上下文模块融合 | HAM 与 GTM 独立处理，输出加性注入主干 |
| 服装与姿势的耦合 | 通过共享模块同时建模姿势和服装 | 通过独立模块解耦，分别控制 |
| 主干训练方案 | 全参数微调或 LoRA 调整整个 DiT | 冻结预训练 T2V DiT，仅优化 HAM 和 GTM |

消融实验证实了双模块架构的优越性（Table 3, Fig. 7）：单模块变体（Single Module）无法有效控制姿势条件（红色框标注区域出现姿势跟随失败），而主干 LoRA 变体（Backbone-LoRA）无法准确转移服装（蓝色框标注区域服装纹理错误）。完整模型在所有指标（L1、PSNR、SSIM、LPIPS、FID、VFID）上均取得最优结果。

### 4. 冻结主干与零样本服装插值

Vanast 的另一个关键设计选择是**冻结预训练的 T2V DiT 主干**，仅优化 HAM 和 GTM 模块。这带来了双重收益：一方面，保留了预训练模型的生成质量与多样性，避免了全参数微调可能导致的模式坍塌或质量退化；另一方面，由于可训练参数集中在条件注入路径上，模型收敛更快、训练更稳定。

双模块架构天然支持**零样本服装插值**：通过对 GTM 输出的服装表示进行加权求和，可在无需额外训练的情况下实现平滑的服装样式过渡：

$$h_{l+1} = \mathrm{B}_l^{\mathrm{T2V}}(h_l) + \alpha \cdot \mathrm{B}_l^{\mathrm{HAM}}(h_l) + \gamma \cdot \mathrm{B}_l^{\mathrm{GTM}}(h_l; \mathbf{G}_A) + (1-\gamma) \cdot \mathrm{B}_l^{\mathrm{GTM}}(h_l; \mathbf{G}_B)$$

其中 $\gamma \in [0,1]$ 为插值权重，控制两个服装 $G_A$ 与 $G_B$ 的混合比例。这一能力源于 GTM 学习到的服装表示具有良好的连续性与可组合性，是双模块解耦设计的自然涌现特性（Fig. 10）。

### 5. 创新总结

Vanast 的创新链条清晰且自洽：**合成三元组监督**解决了训练数据的结构性缺失，迫使模型学习服装转移而非运动复现；**双模块架构**将异质性条件（人体动画与服装转移）解耦为独立路径，在冻结主干的前提下实现精准的条件控制；**加性注入与冻结主干**的组合策略保留了预训练生成质量，同时支持零样本服装插值。这一设计使得 Vanast 在统一的端到端框架中，全面超越了所有两阶段组合基线（Table 1, Table 2），在姿势遵循、服装精度和身份保持三个维度上均取得最优结果。

Vanast 是一个端到端的统一框架，直接从人物图像、服装图像和姿势引导视频合成服装转移后的人物动画视频，无需传统的两阶段流水线（先虚拟试穿再动画生成）。其核心设计围绕两个关键创新展开：**合成三元组数据集生成流水线**和**双模块架构**。

### 输入输出定义

Vanast 的生成过程可形式化表示为：

$$\mathbf{V} = \mathrm{Vanast}(\mathbf{G}, \mathbf{I}^{\mathbf{G}'}, \mathbf{K}, \mathbf{T})$$

其中：
- $\mathbf{G}$：目标服装图像（可为单件或多件）
- $\mathbf{I}^{\mathbf{G}'}$：穿着任意替代服装 $\mathbf{G}'$ 的目标人物图像（由合成流水线生成）
- $\mathbf{K}$：从野外视频中通过 DWPose 提取的 2D 姿势关键点序列，作为运动引导
- $\mathbf{T}$：文本提示
- $\mathbf{V}$：输出的 $F$ 帧动画视频

### 合成三元组数据集生成流水线

现有方法面临的核心瓶颈是缺乏包含不同服装的人物图像与对应视频的三元组训练数据。Vanast 通过**合成三元组监督**解决这一问题：流水线首先为每个人物生成穿着替代服装的身份保留图像 $\mathbf{I}^{\mathbf{G}'}$，同时从野外视频中提取对应的服装图像 $\mathbf{G}$，从而构建大规模三元组训练数据。这一设计迫使模型学习真正的服装转移，而非简单模仿动画中的服装外观。消融实验证实，去除合成人类图像（w/o SynthHuman）会导致服装转移失败，完整模型在所有指标上显著优于该变体（Table 3, Fig. 7）。

### 双模块架构

Vanast 采用**双模块架构**，将人体动画条件与服装转移条件解耦，分别通过两个专用模块注入冻结的文本到视频（T2V）扩散主干：

- **人体动画模块（Human Animation Module, HAM）**：接收人物图像 $\mathbf{I}^{\mathbf{G}'}$ 和姿势序列 $\mathbf{K}$，生成人体动画的条件表示，控制身份保留和姿势遵循。
- **服装转移模块（Garment Transfer Module, GTM）**：接收服装图像 $\mathbf{G}$，生成服装转移的条件表示，控制服装外观的准确迁移。

两个模块的输出以加性方式注入冻结的 T2V DiT 主干网络，每两个块注入一次：

$$h_{l+1} = \begin{cases} \mathrm{B}_l^{\mathrm{T2V}}(h_l), & \text{if } l \neq 2k, \\ \mathrm{B}_l^{\mathrm{T2V}}(h_l) + \alpha \cdot \mathrm{B}_l^{\mathrm{HAM}}(h_l) + \beta \cdot \mathrm{B}_l^{\mathrm{GTM}}(h_l), & \text{otherwise} \end{cases}$$

其中 $\alpha$ 和 $\beta$ 为可学习的权重参数。这种设计的关键优势在于：
1. **训练稳定性**：冻结预训练主干，仅优化 HAM 和 GTM 模块，保留了预训练生成质量并加速收敛。
2. **独立控制**：HAM 和 GTM 分别处理姿势和服装，避免了单模块方案中条件耦合导致的姿势失控或服装转移失败问题（Table 3, Fig. 7）。
3. **零样本服装插值**：GTM 模块天然支持通过加权求和实现平滑的服装样式过渡：

$$h_{l+1} = \mathrm{B}_l^{\mathrm{T2V}}(h_l) + \alpha \cdot \mathrm{B}_l^{\mathrm{HAM}}(h_l) + \gamma \cdot \mathrm{B}_l^{\mathrm{GTM}}(h_l; \mathbf{G}_A) + (1-\gamma) \cdot \mathrm{B}_l^{\mathrm{GTM}}(h_l; \mathbf{G}_B)$$

其中 $\gamma$ 为插值权重，无需额外训练即可在两个服装表示之间平滑过渡（Fig. 10）。

### 整体流水线

如图 2 所示，Vanast 的整体流水线分为两个阶段：**数据生成阶段**通过合成流水线构建三元组训练数据；**推理阶段**将目标服装 $\mathbf{G}$、合成人物图像 $\mathbf{I}^{\mathbf{G}'}$、姿势序列 $\mathbf{K}$ 和文本提示 $\mathbf{T}$ 输入双模块架构，由冻结的 T2V 主干生成最终的服装转移动画视频。这一端到端设计消除了两阶段流水线中常见的身份漂移、服装变形和前后视图不一致问题。

![[assets/figures/papers/paper_list_l1085_https_arxiv_org_abs_2604_04934/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Vanast Pipeline. Our Vanast framework generates virtual try-on human animation videos from a human image, garment images, and a pose video. By incorporating scalable human-image and garment-image generation pipelines, our method avoids dataset-specific constraints and trains effectively at scale. The Dual Modules architecture ensures that the three conditioning signals, human image IG′ , garment images G, and pose video K, are faithfully reflected in the resulting video*

Vanast 的核心设计围绕两个关键机制展开：**合成三元组监督**构建训练数据，以及**双模块注入架构**实现服装转移与人体动画的解耦控制。以下从数据生成、模型架构和公式化定义三个层面进行解析。

### 合成三元组数据生成模块

传统虚拟试穿动画方法依赖两阶段流水线（先试穿后动画），其根本瓶颈在于缺乏包含“同一人物穿着不同服装”的视频三元组数据，导致模型无法端到端学习服装转移与动画的联合生成。Vanast 通过一个可扩展的数据生成流水线解决这一问题：给定一段野外视频 $\bar{\mathbf{V}}^{\mathbf{G}}$（人物穿着服装 $\mathbf{G}$），首先提取其 2D 姿势关键点序列 $\mathbf{K} = \{\bar{\mathbf{k}}_t\}_{t=1}^F$（使用 DWPose），然后利用图像生成模型合成一张身份保留但穿着替代服装 $\mathbf{G}'$ 的人类图像 $\mathbf{I}^{\mathbf{G}'}$。由此构建三元组 $(\mathbf{G}, \mathbf{I}^{\mathbf{G}'}, \mathbf{K})$，其中 $\mathbf{G}$ 从视频中直接提取，$\mathbf{I}^{\mathbf{G}'}$ 为合成图像，$\mathbf{K}$ 为真实运动序列。这一设计的核心洞见在于：**模型被迫学习服装转移而非简单模仿动画**，因为输入的人类图像穿着与目标视频不同的服装。

### 双模块注入架构

Vanast 采用冻结的预训练文本到视频（T2V）扩散主干作为基础生成器，仅在其上附加两个可训练的条件模块——**人体动画模块（Human Animation Module, HAM）**和**服装转移模块（Garment Transfer Module, GTM）**，两者与主干 DiT 块共享部分架构。HAM 接收人类图像 $\mathbf{I}^{\mathbf{G}'}$ 和姿势序列 $\mathbf{K}$，生成人体动画的条件表示；GTM 接收服装图像 $\mathbf{G}$，生成服装转移的条件表示。两个模块的输出以加性方式注入主干网络，每两个 DiT 块注入一次。

这种设计的优势在于：**(1)** 冻结主干保留了预训练 T2V 模型的生成质量，仅优化 HAM 和 GTM 实现快速稳定收敛；**(2)** 将姿势遵循和服装转移解耦到独立模块，避免了单模块方案中姿势条件不可控、或主干 LoRA 方案中服装转移失败的问题（消融实验证实，单模块无法控制姿势，Backbone-LoRA 和 w/o SynthHuman 变体均无法准确转移服装，见 Table 3 和 Fig. 7）。

### 核心公式化定义

**整体生成定义**：给定目标服装图像 $\mathbf{G}$、穿着替代服装的人类图像 $\mathbf{I}^{\mathbf{G}'}$、姿势视频 $\mathbf{K}$ 和文本提示 $\mathbf{T}$，Vanast 输出 $F$ 帧动画视频 $\mathbf{V}$：

$$\mathbf{V} = \mathrm{Vanast}(\mathbf{G}, \mathbf{I}^{\mathbf{G}'}, \mathbf{K}, \mathbf{T}) \tag{1}$$

**双模块注入规则**：设 $h_l$ 为第 $l$ 个 DiT 块的隐藏状态，$\mathrm{B}_l^{\mathrm{T2V}}$ 为主干块，$\mathrm{B}_l^{\mathrm{HAM}}$ 和 $\mathrm{B}_l^{\mathrm{GTM}}$ 分别为 HAM 和 GTM 块。注入规则为每两个块（$l = 2k$）执行一次加性条件注入：

$$h_{l+1} = \begin{cases} \mathrm{B}_l^{\mathrm{T2V}}(h_l), & \text{if } l \neq 2k, \\ \mathrm{B}_l^{\mathrm{T2V}}(h_l) + \alpha \cdot \mathrm{B}_l^{\mathrm{HAM}}(h_l) + \beta \cdot \mathrm{B}_l^{\mathrm{GTM}}(h_l), & \text{otherwise} \end{cases} \tag{2}$$

其中 $\alpha, \beta$ 为可学习的标量权重，控制两个条件信号的注入强度。

**零样本服装插值**：GTM 模块天然支持服装样式插值，无需额外训练。给定两件服装 $\mathbf{G}_A$ 和 $\mathbf{G}_B$，通过对 GTM 输出进行 $\gamma$ 加权求和实现平滑过渡：

$$h_{l+1} = \mathrm{B}_l^{\mathrm{T2V}}(h_l) + \alpha \cdot \mathrm{B}_l^{\mathrm{HAM}}(h_l) + \gamma \cdot \mathrm{B}_l^{\mathrm{GTM}}(h_l; \mathbf{G}_A) + (1-\gamma) \cdot \mathrm{B}_l^{\mathrm{GTM}}(h_l; \mathbf{G}_B) \tag{3}$$

其中 $\gamma \in [0,1]$ 控制插值比例。这一性质源于 GTM 输出的服装表示在特征空间中具有语义连续性，使得加权求和能产生有意义的中间服装样式（Fig. 10 展示了平滑的服装过渡效果）。

## 实验与关键发现

### 主实验结果

Vanast 在两个评估基准上均全面超越现有的两阶段组合基线。我们在 Internet 数据集（80 个样本）和 ViViD 数据集（50 个样本）上，将 Vanast 与两类两阶段流水线进行对比：**主体到图像生成 + 动画模型**，以及**图像虚拟试穿 + 动画模型**。

**表 1** 报告了与主体到图像生成模型（**Mosaic**，She et al., arXiv 2025；**VisualCloze**，Li et al., arXiv 2025；**Less-to-More**，Wu et al., arXiv 2025）与动画模型（**Champ**，Zhu et al., ECCV 2024；**DisPose**，Li et al., arXiv 2024；**StableAnimator**，Tu et al., CVPR 2025）组合的定量对比。Vanast 在全部指标上取得最优：L1 0.0719、PSNR 17.95、SSIM 0.7550、LPIPS 0.2370、FID 91.05、VFID_I3D 22.52、VFID_ResNeXt 0.39。两阶段流水线因身份漂移和服装变形累积误差，在 FID 和 VFID 等感知质量指标上显著落后。

**表 2** 报告了与图像虚拟试穿模型（**OOTDiffusion**，Xu et al., AAAI 2025；**CatVTON**，Chong et al., arXiv 2024；**OmniTry**，Feng et al., arXiv 2025；**Any2AnyTryOn**，Guo et al., arXiv 2025）与动画模型组合的对比。Vanast 同样在所有指标上保持最优，仅在 SSIM 上接近但未显著超越最强基线。两阶段 VTON + 动画方案面临的核心瓶颈在于：试穿阶段生成的服装纹理在前向视角下可能准确，但动画阶段进行多视角渲染时，缺乏对服装与人体运动联合约束的建模，导致前后视图不一致和服装细节丢失。

**定性对比**（图 4 和图 5）进一步验证了定量结论。Vanast 在姿势遵循、服装转移精度和身份保持三个维度上均生成最接近真值的结果，而两阶段基线普遍存在服装纹理漂移、肢体错位和面部身份退化等问题。

### 消融实验

我们通过消融实验（表 3、图 7）验证了双模块架构和合成三元组数据的必要性。

**双模块架构 vs. 单模块与主干 LoRA。** 单模块变体（Single Module）将人体动画和服装转移条件通过同一模块注入，结果在姿势条件上表现出脆弱性——图 7 红色框标注区域显示肢体与目标姿势偏离。主干 LoRA 变体（Backbone-LoRA）在冻结的 T2V DiT 上仅添加 LoRA 适配器，无法准确转移服装，图 7 蓝色框区域出现明显的服装纹理错误。定量上，完整 Vanast 在所有指标上均优于这两个变体（表 3）：L1 0.1069 vs. Single Module 0.1162 vs. Backbone-LoRA 0.1359；FID 104.59 vs. 108.84 vs. 120.97。这表明独立的 HAM 和 GTM 模块对于解耦并精确控制两个条件信号是必要的。

**合成人类图像（SynthHuman, I^{G'}）的关键作用。** 去除 I^{G'} 的变体（w/o SynthHuman）仅使用从视频中抽取的原始帧作为人类图像输入，此时服装转移几乎完全失败（图 7 蓝色框区域）。定量指标同样显著恶化：LPIPS 从 0.3673 升至 0.3943，VFID_ResNeXt 从 1.21 升至 1.93（表 3）。这验证了核心洞察：当人类图像穿着与目标服装相同的衣服时，模型倾向于复现输入帧的运动模式而非学习服装转移；合成三元组强制模型面对“身份相同但服装不同”的人类图像，从而真正学习服装与运动的联合生成。

**冻结主干的训练策略。** 我们仅优化 HAM 和 GTM 模块，保持预训练 T2V DiT 主干冻结。这一策略保留了预训练模型的生成质量，并显著加速收敛。相比之下，全参数微调或主干 LoRA 方案容易破坏预训练先验，导致生成质量下降（表 3、图 7 中 Backbone-LoRA 的 FID 和 VFID 均显著劣化）。

### 服装转移能力展示

Vanast 支持多种服装转移模式。**单服装转移**（图 6）展示了仅使用单张服装图像生成动画视频的结果，服装纹理和细节得到准确保留。**多服装零样本转移**（图 8）同时转移上下装，服装的 logo 和精细纹理在动画中保持稳定。**野外服装转移**（图 9）使用 TikTokDress 数据集中的野外服装图像，验证了方法对非受控场景的泛化能力。

### 零样本服装插值

双模块架构的一个天然优势是支持零样本服装插值。通过对 GTM 输出的两个服装表示进行 γ 加权求和：

$$h_{l+1} = \mathrm{B}_l^{\mathrm{T2V}}(h_l) + \alpha \cdot \mathrm{B}_l^{\mathrm{HAM}}(h_l) + \gamma \cdot \mathrm{B}_l^{\mathrm{GTM}}(h_l; \mathbf{G}_A) + (1-\gamma) \cdot \mathrm{B}_l^{\mathrm{GTM}}(h_l; \mathbf{G}_B)$$

无需任何额外微调即可实现服装样式的平滑过渡。图 10 展示了 γ 从 0 到 1 变化时，服装从 G_A 向 G_B 的连续插值效果，验证了 GTM 学到的服装表示具有良好的语义连续性和可插值性。这一能力源于 GTM 与 HAM 的条件解耦设计：服装表示独立于人体动画表示，因此可以在不干扰姿势和身份的条件下进行代数操作。

### 失败模式与局限

当前验证的分析未提供显式的失败案例（limitations 字段为空）。根据方法设计推断，潜在局限可能包括：极端姿势或遮挡下的服装转移精度下降、合成三元组数据中人类图像生成质量对整体性能的制约、以及多服装转移时服装间交互（如衣领重叠）的建模不足。这些推断需要人工对照原文进一步确认。

![[assets/figures/papers/paper_list_l1085_https_arxiv_org_abs_2604_04934/figures/006_Table_1.jpg]]
*Table 1: Quantitative Comparison with the Combination of Subject-to-Image and Animation Models. We compare our model with a baseline that combines a subject-to-image model and an animation model. Our model achieves the best performance across all metrics. Bold text indicates the best score in each column*

![[assets/figures/papers/paper_list_l1085_https_arxiv_org_abs_2604_04934/figures/007_Table_2.jpg]]
*Table 2: Quantitative Comparison with the Combination of Image Virtual Try-On and Animation Models. We compare our model with a baseline that combines a image virtual try-on model and an animation model. Our model achieves the best performance across all metrics. Bold text indicates the best score in each column*

![[assets/figures/papers/paper_list_l1085_https_arxiv_org_abs_2604_04934/figures/010_Table_3.jpg]]
*Table 3: Ablation Study. We conduct ablation study for each component of our model and dataset configuration. Bold text indicates the best score in each column*

![[assets/figures/papers/paper_list_l1085_https_arxiv_org_abs_2604_04934/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative Comparisons (Subject-to-Image-based). We compare our results with baselines constructed by combining subject-to-image generation and animation models. Our method produces the most accurate pose following and garment transfer while preserving identity with high fidelity*

![[assets/figures/papers/paper_list_l1085_https_arxiv_org_abs_2604_04934/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative Comparisons (Virtual Try-On-based). We compare our results with baselines formed by combining image virtual try-on models with animation models. Our method achieves the most accurate pose following and garment transfer while preserving identity with the highest fidelity*

## 定位与知识库关联

### 任务定位与问题边界

Vanast 解决的是 **虚拟试穿人物动画生成** 这一复合任务：给定一张人类图像、一张或多张服装图像，以及一段姿势引导视频，直接合成一段穿着目标服装、遵循输入姿势的人物动画视频。与现有工作将任务拆分为“先虚拟试穿再动画生成”或“先主体到图像再动画生成”的两阶段流水线不同，Vanast 首次将服装转移与人体动画整合到一个端到端的统一框架中。

这一任务定位决定了其适用边界：
- **输入依赖**：需要一张身份明确的人类图像、至少一张服装图像和一段姿势视频（通过 DWPose 提取 2D 关键点序列 K 获得）。模型不处理纯文本驱动的服装生成，也不支持无姿势引导的自由动画。
- **服装类型**：支持单件服装转移（如上装或下装，Fig. 6）、多件服装同时转移（Fig. 8），以及野外场景下的服装转移（Fig. 9，使用 TikTokDress 数据集）。零样本服装插值（Fig. 10）进一步扩展了服装样式的平滑过渡能力，无需额外训练。
- **生成范围**：输出为固定帧数的动画视频，身份保留和姿势遵循是核心约束。模型不涉及 3D 人体重建或物理模拟，而是完全依赖 2D 扩散生成先验。

### 与两阶段组合基线的对比

现有方法的主流范式是将任务分解为两个独立阶段：首先生成穿着目标服装的静态图像（通过主体到图像生成或虚拟试穿模型），再将该图像输入动画模型生成视频。Vanast 在 Internet 数据集（80 样本）上系统性地对比了这两类组合基线：

**主体到图像 + 动画组合**（Table 1）：
- 主体到图像模型：**Mosaic** (She et al., arXiv 2025)、**VisualCloze** (Li et al., arXiv 2025)、**Less-to-More** (Wu et al., arXiv 2025)
- 动画模型：**Champ** (Zhu et al., ECCV 2024)、**DisPose** (Li et al., arXiv 2024)、**StableAnimator** (Tu et al., CVPR 2025)
- 结果：Vanast 在所有指标（L1、PSNR、SSIM、LPIPS、FID、VFID）上均取得最优，定性比较（Fig. 4）显示两阶段方法在身份漂移和服装变形方面存在明显退化。

**虚拟试穿 + 动画组合**（Table 2）：
- 虚拟试穿模型：**OOTDiffusion** (Xu et al., AAAI 2025)、**CatVTON** (Chong et al., arXiv 2024)、**OmniTry** (Feng et al., arXiv 2025)、**Any2AnyTryOn** (Guo et al., arXiv 2025)
- 动画模型：同上
- 结果：Vanast 在所有指标上（除 SSIM 外）均显著优于所有组合。定性比较（Fig. 5）表明，两阶段流水线在前后视图一致性、服装细节保留和姿势精确跟随方面均不及端到端方法。

这些对比揭示了 Vanast 的核心优势来源：两阶段方法中，第一阶段的误差（如服装纹理丢失、身份特征模糊）会不可逆地传播到动画阶段，而端到端框架通过联合优化服装转移和动画生成，从根本上避免了级联误差。

### 与统一视频生成模型的对比

除了两阶段组合基线，Vanast 还与 **VACE** (Jiang et al., arXiv 2025) 形成对比。VACE 是一个统一的视频创建模型，通过单一条件模块融合多种控制信号。Vanast 在架构层面做出了关键区分：将人体动画条件（HAM）和服装转移条件（GTM）解耦为两个独立模块，并交替注入冻结的文本到视频扩散主干（每两个块注入一次）。消融实验（Table 3, Fig. 7）表明：
- **单模块变体**（Single Module）无法控制姿势条件（Fig. 7 红色框），说明条件解耦对姿势遵循至关重要。
- **主干 LoRA 变体**（Backbone-LoRA）无法准确转移服装（Fig. 7 蓝色框），说明独立的条件注入模块比全模型微调或 LoRA 调整更能保留预训练生成质量的同时实现精确控制。

### 训练范式与数据构建的差异

Vanast 在训练数据构建上做出了根本性创新：通过合成三元组监督（生成穿着不同服装的人类图像 I^{G'}，并从野外视频提取服装图像 G）构建大规模训练数据。这与现有方法从视频中直接抽取一帧作为训练目标的做法形成鲜明对比。消融实验（Table 3, Fig. 7）中去除合成人类图像（w/o SynthHuman）导致服装转移完全失败，证明 I^{G'} 对迫使模型学习“服装转移”而非简单“运动复现”是不可或缺的。

在训练策略上，Vanast 冻结预训练的文本到视频 DiT 主干，仅优化 HAM 和 GTM 模块。这种选择性微调策略在保留预训练生成质量、加速收敛方面具有优势，与全模型微调或 LoRA 方案形成对比。

### 适用边界与局限

基于论文提供的证据，Vanast 的适用边界和潜在局限包括：

1. **数据依赖性**：合成三元组数据的质量直接影响模型性能。论文未讨论当合成人类图像 I^{G'} 存在身份保留失败或服装生成错误时，对下游训练的影响程度。这一点的鲁棒性需要手动验证。

2. **姿势引导的局限性**：模型依赖 DWPose 提取的 2D 关键点作为运动引导。对于极端姿势、严重遮挡或多人场景，2D 关键点的表达能力可能不足。论文未报告在这些困难场景下的性能。

3. **服装泛化边界**：虽然展示了野外服装转移（Fig. 9）和零样本服装插值（Fig. 10），但未系统评估对极端服装类型（如宽松长袍、复杂褶皱、透明材质）的泛化能力。

4. **计算开销**：双模块架构虽然冻结了主干，但 HAM 和 GTM 模块共享部分 DiT 块架构，推理时的计算开销和显存占用未与两阶段方法进行系统对比。

5. **评估覆盖**：定量评估集中在 Internet 数据集（80 样本）和 ViViD 数据集（50 样本），样本量较小。更大规模、更多样化的评估将增强结论的可靠性。

### 开放问题

1. **身份保留与服装转移的冲突**：当目标服装与源人类图像的服装在纹理、颜色或形状上产生强烈冲突时，模型如何在身份保留和服装准确转移之间取得平衡？这一权衡机制未被深入分析。

2. **时序一致性的理论保证**：双模块注入策略如何显式地保证生成视频的时序一致性（而非仅依赖扩散模型的隐式先验），论文未提供机制层面的解释。

3. **扩展到更多条件**：HAM 和 GTM 的解耦架构是否可自然扩展到其他条件（如背景、光照、相机运动），形成更通用的可控视频生成框架，是一个值得探索的方向。

4. **与 3D 方法的结合**：当前方法完全基于 2D 表示，与基于 3D 人体模型（如 SMPL）的方法在服装几何保真度上的差距未量化。

## 原文 PDF

![[paperPDFs/CVPR_2026/Vanast_Virtual_Try_On_with_Human_Image_Animation_via_Synthetic_Triplet_Supervision.pdf]]
