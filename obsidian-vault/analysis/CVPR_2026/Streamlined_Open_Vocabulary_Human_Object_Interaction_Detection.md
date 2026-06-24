---
title: Streamlined Open-Vocabulary Human-Object Interaction Detection
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Streamlined_Open_Vocabulary_Human_Object_Interaction_Detection.pdf
project_link: null
code_link: "https://github.com/MPI-Lab/SL-HOI"
aliases:
- SH
- SOVHOID
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将交互查询与骨干输出的图像 tokens 一同送入冻结的文本对齐视觉头（vision head），利用其预训练的自注意力层进行语义引导（Semantic Bootstrapping），使查询与图像 tokens 在共享空间中相互适应，消除表示差异。随后通过轻量可学习的交叉注意力（Hierarchical Refinement）进一步挖掘上下文信息，实现高精...
primary_logic: DINOv3 的骨干网络与视觉头具有自然的协作分工：骨干的注意力聚焦于局部，提供细微空间线索，适合实例检测；视觉头的注意力是全局的，聚合关系上下文，适合交互分类。冻结整个 DINOv3，仅添加极少可学习参数，通过两阶段交互细化（语义引导 + 层次细化）无缝衔接两种能力，从而在保持结构精简的同时达到最优的开放词汇 HOI 检测性能。
claims:
- 在 SWiG-HOI 数据集上，SL-HOI 在所有指标上均取得最优，其中 Unseen 类别超过之前最佳方法 SGC-Net 6.58%，Full 类别提升 7.47%。
- 消融实验表明，在强基线基础上，仅仅添加 Semantic Bootstrapping 即可为 Unseen/Rare/Non-rare/Full 带来 +1.54%/+1.61%/+1.08%/+1.46% 的绝对提升；进一步添加 Hierarchical Refinement 再额外提升 +0.95%/+1.42%/+1.79%/+1.39%。
- 注意力图可视化证实了骨干与视觉头的关注模式存在天然差异：骨干注意点状、细粒度，视觉头注意全局、语义丰富，验证了互补利用的设计动机。
- 在 HICO-DET 开放词汇设定下，无目标检测预训练的方法中，SL-HOI 在 Unseen/Seen/Full 上分别超过次优方法 17.26%/14.65%/15.27% ，展现强大的泛化能力。
---

# Streamlined Open-Vocabulary Human-Object Interaction Detection

> [!tip] 核心洞察
> DINOv3 的骨干网络与视觉头具有自然的协作分工：骨干的注意力聚焦于局部，提供细微空间线索，适合实例检测；视觉头的注意力是全局的，聚合关系上下文，适合交互分类。冻结整个 DINOv3，仅添加极少可学习参数，通过两阶段交互细化（语义引导 + 层次细化）无缝衔接两种能力，从而在保持结构精简的同时达到最优的开放词汇 HOI 检测性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 精简的开放词汇人-物交互检测 |
| 英文题名 | Streamlined Open-Vocabulary Human-Object Interaction Detection |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.27500) · [Code](https://github.com/MPI-Lab/SL-HOI) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SL-HOI |
| Dataset | SWiG-HOI, HICO-DET |

> [!tip] 效果简介
> - SWiG-HOI 上，mAP % (Full) 24.67 vs 17.20 (SGC-Net) (+7.47)；mAP % (Unseen) 19.04 vs 12.46 (SGC-Net) (+6.58)。
> - HICO-DET (Open-Vocabulary) 上，mAP % (Full) 42.49 vs 40.99 (BC-HOI, with detection pretraining) / 27.22 (SGC-Net, without detection... (+1.50 / +15.27)。
> - HICO-DET (Closed) 上，mAP % (Full) 45.05 vs 43.01 (BC-HOI) (+2.04)。

## 概述

开放词汇人-物交互（HOI）检测旨在识别图像中任意人与物体之间的交互关系，其核心挑战在于对未见过的交互类别进行泛化。现有方法大致分为两类：**VLM 协作式**方法依赖独立训练的检测器与视觉语言模型（VLM）协作，导致结构复杂且跨模型特征表示差异大、融合困难；**纯 VLM 式**方法使用单一 VLM 但缺乏细粒度空间特征，定位能力弱。根本瓶颈在于如何在一个统一框架内同时获得精确的实例定位与泛化交互分类所需的互补特征，并消除两者之间的表示鸿沟。

本文提出 **SL-HOI**（Streamlined Open-Vocabulary HOI Detection），一个仅基于 DINOv3 的精简框架。其核心洞察在于：DINOv3 的骨干网络与文本对齐视觉头具有天然的协作分工——骨干的注意力聚焦于局部，提供细微空间线索，适合实例检测；视觉头的注意力是全局的，聚合关系上下文，适合交互分类（见 Figure 2 注意力图可视化）。SL-HOI 冻结整个 DINOv3，仅添加极少可学习参数，通过**语义引导（Semantic Bootstrapping）**与**层次细化（Hierarchical Refinement）**两阶段交互细化，无缝衔接两种能力，从而在保持结构精简的同时达到最优的开放词汇 HOI 检测性能。

在 SWiG-HOI 数据集上，SL-HOI 在所有指标上均取得最优，其中 Unseen 类别超过之前最佳方法 **SGC-Net**（Lin et al., CVPR 2025）**6.58%**，Full 类别提升 **7.47%**。在 HICO-DET 开放词汇设定下，无目标检测预训练的方法中，SL-HOI 在 Unseen/Seen/Full 上分别超过次优方法 **17.26%/14.65%/15.27%**。消融实验证实，Semantic Bootstrapping 和 Hierarchical Refinement 各自带来显著且稳定的增益，且冻结全部 DINOv3 参数的训练策略优于部分微调或 LoRA。

## 背景与动机

### 开放词汇人-物交互检测的核心挑战

人-物交互（Human-Object Interaction, HOI）检测旨在从图像中同时定位“人-物”对并识别其交互关系（如“人骑马”）。传统 HOI 检测受限于封闭词汇设定，即训练和测试共享固定的交互类别集合，无法泛化到未见过的交互组合。开放词汇 HOI 检测的提出正是为了解决这一局限——模型需要在训练时从未见过的交互类别上也能做出正确预测。

这一任务的核心困难在于：**模型必须同时具备精确的实例定位能力和泛化的语义理解能力**，而这两种能力在现有视觉架构中往往来源于不同的组件，彼此之间存在天然的表示鸿沟。

### 现有范式的结构性缺陷

当前开放词汇 HOI 检测方法主要分为两类架构范式（如 Figure 1 所示），各有其结构性缺陷：

**VLM 协作式方法**（VLM-collaborated）采用“独立检测器 + 视觉语言模型（VLM）”的双模型架构：先用传统 HOI 检测器定位人-物对，再借助 CLIP 等 VLM 进行开放词汇交互分类。代表性工作包括 **GEN-VLKT**（Liao et al., CVPR 2022）、**HOICLIP**（Ning et al., CVPR 2023）、**SGC-Net**（Lin et al., CVPR 2025）等。这类方法的根本问题在于：
- **结构冗余**：需要维护两个独立训练的模型，推理流程复杂；
- **表示鸿沟**：检测器与 VLM 的特征空间差异巨大，跨模型特征融合困难，交互分类难以充分利用检测阶段的细粒度空间信息。

**单一 VLM 方法**（VLM-only）试图直接使用一个 VLM 完成检测与分类，如 **THID**（Wang et al., CVPR 2022）。这类方法虽然结构精简，但 VLM 天然缺乏细粒度空间特征，导致定位能力弱，难以精确回归人-物边界框。

### 本文动机：统一框架内的互补特征利用

上述分析揭示了一个根本瓶颈：**如何在单一统一框架内同时获得精确的实例定位与泛化交互分类所需的互补特征，并消除两者之间的表示差异**。

本文的核心观察来自对 DINOv3 模型内部组件特性的深入分析。如 Figure 2 的注意力图可视化所示，DINOv3 的骨干网络（backbone）与文本对齐视觉头（vision head）存在天然的协作分工：
- **骨干的注意力聚焦于局部**，呈现点状、细粒度的关注模式，提供细微空间线索，天然适合实例检测；
- **视觉头的注意力是全局的**，聚合丰富的语义上下文关系，天然适合交互分类。

这一观察揭示了一个被先前工作忽视的可能性：**无需引入额外的 VLM，仅凭 DINOv3 自身组件的互补特性，即可在一个冻结的统一框架内同时满足定位与分类的需求**。基于此，本文提出 SL-HOI——一个完全基于冻结 DINOv3 的精简开放词汇 HOI 检测框架，通过语义引导（Semantic Bootstrapping）与层次细化（Hierarchical Refinement）两个轻量级机制，无缝衔接骨干的定位能力与视觉头的语义理解能力，从根本上消除了多模型协作带来的表示鸿沟与结构冗余。

## 核心创新

SL-HOI 的核心创新在于**用单一冻结的 DINOv3 模型同时承担精确定位与开放词汇交互分类**，通过挖掘其内部组件的天然分工，以极简的架构消除现有方法中的表示鸿沟。以下从方法谱系定位和关键改变槽位两个维度展开。

### 方法谱系与知识库定位

开放词汇 HOI 检测的主流范式可归结为两条技术路线：

- **VLM 协作式（VLM-collaborated）**：将独立训练的 HOI 检测器与 CLIP 等视觉-语言模型组合，检测器负责定位，VLM 负责交互分类。代表工作包括 **GEN-VLKT**（Liao et al., CVPR 2022）、**HOICLIP**（Ning et al., CVPR 2023）、**MP-HOI-L**（Yang et al., CVPR 2024）等。这类方法的根本缺陷在于**跨模型特征表示差异大、融合困难**：检测器与 VLM 来自不同的训练目标和数据分布，特征空间不对齐，导致信息传递存在瓶颈。

- **单 VLM 式（VLM-only）**：仅使用一个 VLM 完成检测与分类，如 **THID**（Wang et al., CVPR 2022）。这类方法结构简洁，但**缺乏细粒度空间特征**，定位能力弱，无法与专门的检测器竞争。

SL-HOI 开创了**第三条路径**：利用 DINOv3 的“一模型双能力”特性——其骨干网络（backbone）提供细粒度空间线索，适合实例定位；其文本对齐视觉头（vision head）具有全局注意力，适合交互分类。这与 **SGC-Net**（Lin et al., CVPR 2025）的分层粒度比较策略形成鲜明对比：SGC-Net 仍依赖外部 CLIP 文本编码器进行语义匹配，而 SL-HOI 将分类能力内置于同一冻结模型内，从根本上避免了跨模型表示鸿沟。

### 关键改变槽位

SL-HOI 相对于强基线（Late Fusion 架构，类似 HOICLIP 的交互分类方式）做出了三个关键改变：

**1. 基础视觉模型：从 CLIP 到冻结的 DINOv3**

基线方法普遍采用 CLIP（ViT-B/16 或 ViT-L/14）作为视觉编码器。SL-HOI 替换为 **DINOv3 ViT-L/16 的 dino.txt 变体**，且所有参数冻结（Section 4.1, Section 5.2）。这一替换的深层动机在于：DINOv3 的骨干与视觉头之间存在天然的注意力分工——骨干的自注意力呈点状、细粒度，聚焦局部空间细节；视觉头的自注意力呈全局、语义丰富，聚合关系上下文（Figure 2 的可视化证实了这一互补模式）。冻结策略消融实验（Table 6, Supplementary）表明，冻结全部参数在 SWiG-HOI 上取得最佳 Full mAP 24.67，优于部分微调或 LoRA 微调，说明 DINOv3 预训练表示已足够强大，额外微调反而可能破坏其内部协调性。

**2. 交互分类特征融合：从 Late Fusion 到 Semantic Bootstrapping → Hierarchical Refinement 两阶段细化**

基线采用典型的 Late Fusion：交互查询直接与冻结视觉头输出做交叉注意力。SL-HOI 将其替换为两阶段级联：

- **Semantic Bootstrapping（语义引导）**：将交互查询 $\mathbf{Q}_r$ 与图像 tokens $\mathbf{X}_b$ 拼接后送入冻结视觉头的自注意力层（Eq.5），利用其预训练的全局注意力使查询与图像 tokens 在共享空间中相互适应。这一阶段的核心作用是**消除检测分支与分类分支之间的表示差异**，让交互查询“浸入”视觉头的语义空间。

- **Hierarchical Refinement（层次细化）**：以上一步输出的语义增强查询 $\mathbf{Q}_r'$ 为查询，以查询影响后的图像 tokens $\mathbf{X}_{\text{head}}$ 为键值，通过单层可学习交叉注意力产生最终交互嵌入 $\mathbf{E}_r$（Eq.6）。这一阶段进一步挖掘上下文信息，实现精细的交互分类。

消融实验（Table 4）严格验证了这一两阶段设计的增量价值：在强基线上仅添加 Semantic Bootstrapping，Unseen/Rare/Non-rare/Full 分别提升 +1.54%/+1.61%/+1.08%/+1.46%；在此基础上再添加 Hierarchical Refinement，四项指标进一步分别提升 +0.95%/+1.42%/+1.79%/+1.39%。合计贡献约占总提升的绝大部分，证明了两阶段细化是性能突破的核心因果杠杆。

**3. 交互查询初始化：从独立可学习查询到检测嵌入投影**

基线通常直接使用可学习查询或简单地从检测头获取交互查询。SL-HOI 通过对人体和物体解码器嵌入进行逐元素平均并线性投影得到初始交互查询 $\mathbf{Q}_r = \operatorname{Proj}((\mathbf{E}_h + \mathbf{E}_o) / 2)$（Eq.4）。这一设计将检测分支的空间信息显式注入交互分类分支，建立了从定位到分类的信息桥梁，使语义引导阶段能够基于已定位的实例特征进行上下文推理。

### 创新本质总结

SL-HOI 的创新不在于引入新的模块类型，而在于**对现有 DINOv3 组件能力的重新编排与衔接**。其核心洞察是：骨干与视觉头之间天然存在“局部-全局”的注意力分工，仅需通过 Semantic Bootstrapping 将交互查询插入视觉头的自注意力流，再以极轻量的可学习交叉注意力进行层次细化，即可无缝桥接两种能力。整个框架仅添加检测适配器、交互查询投影和单层交叉注意力解码器等少量可学习参数，在保持结构精简的同时达到最优的开放词汇 HOI 检测性能——这本质上是一种**表示鸿沟消除机制**，而非简单的特征增强。

## 整体框架

SL-HOI 的整体设计遵循一个核心原则：**在单一冻结的 DINOv3 模型内，利用其不同组件的天然互补性，以极简的架构实现开放词汇人-物交互检测**。整个框架仅包含极少量的可学习参数，无需额外的独立 VLM 或检测器，形成端到端的精简流程。

### 架构总览

如 Figure 3 所示，SL-HOI 由一条冻结的 DINOv3 ViT 编码器（骨干网络）驱动，其输出同时服务于两个分支：

![[assets/figures/papers/paper_list_l1080_https_arxiv_org_abs_2603_27500/figures/003_Figure_3.jpg]]
*Figure 3: Overall architecture of our SL-HOI framework. A frozen DINOv3 ViT encoder (backbone) provides features for two branches. The first branch performs standard instance detection, localizing interactive human-object pairs. The second branch, our core contribution, refines interaction queries in a two-step process. We feed the initial interaction queries*

1. **实例检测分支**：利用骨干网络提供的细粒度空间特征，定位交互中的人体和物体实例。
2. **交互分类分支**（核心贡献）：通过两阶段细化过程，将检测到的实例对转化为开放词汇的交互类别预测。

### 数据流与模块关系

整个 pipeline 的数据流可概括为以下步骤：

1. **特征提取**：输入图像经冻结的 DINOv3 骨干网络处理，输出图像 tokens $\mathbf{X}_b$。这些 tokens 保留了丰富的局部空间细节，天然适合实例定位任务。

2. **实例检测**：
   - $\mathbf{X}_b$ 首先经过检测适配器（Detection Adapter）处理：通过 1×1 卷积降维并加上位置编码，再经自注意力层编码，得到特征 $\mathbf{F}$（Eq.1）。
   - 可学习的人体查询 $\mathbf{Q}_h$ 和物体查询 $\mathbf{Q}_o$ 在 $\mathbf{F}$ 上进行交叉注意力解码，产生精细的人体嵌入 $\mathbf{E}_h$ 和物体嵌入 $\mathbf{E}_o$（Eq.2）。
   - 通过 MLP 从嵌入中预测人体和物体的边界框（Eq.3）。

3. **交互查询构建**：将人体嵌入 $\mathbf{E}_h$ 和物体嵌入 $\mathbf{E}_o$ 进行逐元素平均，再通过线性投影得到初始交互查询 $\mathbf{Q}_r$（Eq.4）。这一设计使交互查询天然携带了实例对的组合信息。

4. **语义引导（Semantic Bootstrapping）**：将 $\mathbf{Q}_r$ 与骨干输出的图像 tokens $\mathbf{X}_b$ 拼接，一同送入冻结的文本对齐视觉头（vision head）的自注意力层。视觉头的全局注意力机制使交互查询与图像 tokens 在共享语义空间中相互适应，输出语义增强的交互查询 $\mathbf{Q}_r'$ 和查询影响的图像 tokens $\mathbf{X}_{\mathrm{head}}$（Eq.5）。

5. **层次细化（Hierarchical Refinement）**：以 $\mathbf{Q}_r'$ 为查询，$\mathbf{X}_{\mathrm{head}}$ 为键值，通过一个轻量可学习的单层交叉注意力解码器，进一步挖掘上下文信息，产生最终的交互嵌入 $\mathbf{E}_r$（Eq.6）。

6. **开放词汇分类**：将 $\mathbf{E}_r$ 线性投影到文本嵌入空间后，与预计算的交互文本嵌入进行余弦相似度计算，通过可学习温度参数 $\tau$ 得到各类别的概率分布 $p_{ij}$（Eq.7）。

### 设计动机：骨干与视觉头的互补分工

该架构的合理性根植于对 DINOv3 内部注意力模式的观察。如 Figure 2 所示，骨干网络最后一层自注意力的关注模式呈现**点状、细粒度**的特征，聚焦于被查询 patch 周围的局部区域，这使其成为实例定位的理想特征源。而文本对齐视觉头的注意力则是**全局性、语义丰富**的，能够聚合来自整张图像的关系上下文信息，天然适合交互分类任务。

SL-HOI 通过冻结整个 DINOv3，完整保留这两种互补能力，并仅通过语义引导和层次细化两个轻量步骤将它们无缝衔接。这种“Local-Global-Local”的交互推理过程（Figure 5）使模型在保持架构精简的同时，实现了从细粒度定位到全局语义理解的平滑过渡。

### 补充图表

![[assets/figures/papers/paper_list_l1080_https_arxiv_org_abs_2603_27500/figures/001_Figure_1.jpg]]
*Figure 1: An illustration of the dominant architectural paradigms for open-vocabulary HOI detection. (a) VLM-collaborated methods that adopt both a VLM and a conventional HOI detector. (b) VLM-only methods that employ a single VLM for open-vocabulary HOI detection. (c) Our SL-HOI leverages the complementary strengths of DINOv3’s backbone and vision head*

## 核心模块与公式推导

SL-HOI 的核心创新在于将交互查询与冻结的文本对齐视觉头协同工作，通过两阶段细化机制消除检测与分类之间的表示鸿沟。整个框架围绕冻结的 DINOv3 ViT-L/16 构建，仅引入极少可学习参数，形成三个关键模块。

### 检测适配器与实例解码器

DINOv3 骨干输出图像 tokens $\mathbf{X}_b \in \mathbb{R}^{N \times D}$，其中 $N$ 为 patch 数量，$D$ 为特征维度。为适配下游检测任务，首先通过 1×1 卷积降维并添加位置编码，再经自注意力编码器处理：

$$\mathbf{F} = \operatorname{Adapter}(\operatorname{Conv}(\mathbf{X}_b) + \mathbf{E}_{pos}) \tag{1}$$

其中 $\mathbf{E}_{pos}$ 为可学习位置编码。随后，两组可学习查询 $\mathbf{Q}_h, \mathbf{Q}_o \in \mathbb{R}^{N_q \times d}$（$N_q=64$）在特征 $\mathbf{F}$ 上通过交叉注意力解码器产生精细的人体与物体嵌入：

$$\mathbf{E}_h, \mathbf{E}_o = \operatorname{Decoder}(\mathbf{Q}_h, \mathbf{Q}_o, \mathbf{F}) \tag{2}$$

边界框由 MLP 直接回归：

$$\hat{b}_h = \mathrm{MLP}_h(\mathbf{E}_h), \quad \hat{b}_o = \mathrm{MLP}_o(\mathbf{E}_o) \tag{3}$$

### 交互查询构造器

获得人体与物体嵌入后，通过对两者进行逐元素平均并线性投影，得到初始交互查询 $\mathbf{Q}_r$：

$$\mathbf{Q}_r = \operatorname{Proj}((\mathbf{E}_h + \mathbf{E}_o) / 2) \tag{4}$$

这一设计将成对实例的局部信息压缩为统一的查询表示，为后续语义引导提供起点。

### 语义引导（Semantic Bootstrapping）

这是 SL-HOI 消除表示鸿沟的核心机制。将交互查询 $\mathbf{Q}_r$ 与骨干图像 tokens $\mathbf{X}_b$ 拼接，送入冻结的文本对齐视觉头 $\mathscr{F}_{\mathrm{head}}$（即 DINOv3 的 dino.txt 变体头部）。视觉头的自注意力层使查询与图像 tokens 在共享语义空间中相互适应：

$$[\mathbf{Q}_r'; \mathbf{X}_{\mathrm{head}}] = \mathscr{F}_{\mathrm{head}}([\mathbf{Q}_r; \mathbf{X}_b]) \tag{5}$$

视觉头的输入序列结构为 $[ \mathrm{CLS}, \mathrm{Reg}_1, \dots, \mathrm{Reg}_4, Q_1, \dots, Q_{N_q}, P_1, \dots, P_N ]$，包含 CLS token、4 个 register tokens、$N_q$ 个交互查询和 $N$ 个 patch tokens。输出端得到语义增强的交互查询 $\mathbf{Q}_r'$ 和查询影响后的图像 tokens $\mathbf{X}_{\mathrm{head}}$。这一步骤利用了视觉头预训练中习得的全局注意力模式——与骨干的局部细粒度注意力形成互补——使交互查询获得丰富的上下文语义信息。

### 层次细化（Hierarchical Refinement）

语义引导后的查询 $\mathbf{Q}_r'$ 已携带全局语义，但缺乏对细粒度空间线索的显式利用。为此，引入一个轻量可学习的单层交叉注意力解码器 $\mathcal{G}_{\mathrm{decoder}}$，以 $\mathbf{Q}_r'$ 为查询，$\mathbf{X}_{\mathrm{head}}$ 为键值：

$$\mathbf{E}_r = \mathcal{G}_{\mathrm{decoder}}(\mathbf{Q}_r', \mathbf{X}_{\mathrm{head}}) \tag{6}$$

交叉注意力的键值序列为 $[ \mathsf{CLS}', \overline{P'}, P_1', \dots, P_N' ]$，其中 $\overline{P'} = \frac{1}{N} \sum_{i=1}^{N} P_i'$ 为平均 patch token，register tokens 被排除。这一结构使查询能够从 CLS 的全局语义、平均 patch 的整体上下文和各个 patch 的局部细节三个层次聚合信息，形成“局部-全局-局部”的推理过程。

### 开放词汇分类器

最终交互嵌入 $\mathbf{E}_r$ 经线性投影进入文本对齐空间后，与预计算的交互类别文本嵌入 $\mathbf{e}_t$ 进行余弦相似度计算，通过可学习温度 $\tau$ 得到分类概率：

$$p_{ij} = \frac{\exp(\tau \cdot \cos(\mathbf{e}_r'^{(i)}, \mathbf{e}_t^{(j)}))}{\sum_{k \in \mathcal{R}} \exp(\tau \cdot \cos(\mathbf{e}_r'^{(i)}, \mathbf{e}_t^{(k)}))} \tag{7}$$

其中 $\mathcal{R}$ 为所有交互类别的集合。与分别计算 CLS 和平均 patch 两个通道相似度再加权求和的方案相比，统一投影策略在实验中表现更优，但其深层原因仍有待进一步探究。

### 补充图表

![[assets/figures/papers/paper_list_l1080_https_arxiv_org_abs_2603_27500/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of attention maps from the last selfattention block of (a) DINOv3 backbone and (b) dino.txt vision head. The left column shows the original image of a person petting a horse, the middle column displays the attention map, and the right column overlays the attention on the original image. The red dot marks the queried patch located on the person. All other image patch tokens are as keys*

![[assets/figures/papers/paper_list_l1080_https_arxiv_org_abs_2603_27500/figures/009_Figure_5.jpg]]
*Figure 5: Visualization of attention maps across the interaction classification stage. The left two are in the self-attention blocks of the frozen head during Semantic Bootstrapping, and the right one is from the cross-attention block in Hierarchical Refinement, illustrating a Local-Global-Local interaction reasoning process*

## 实验与分析

### 主实验结果

SL-HOI 在两个标准 HOI 检测基准上系统验证了其有效性：SWiG-HOI（以场景为中心的开放词汇设定）和 HICO-DET（开放词汇与封闭设定双轨评估）。

**SWiG-HOI 数据集。** 如 Table 1 所示，SL-HOI 在所有指标上均取得最优结果。在 Unseen 类别上，SL-HOI 达到 19.04% mAP，超过此前最佳方法 **SGC-Net**（Lin et al., CVPR 2025）6.58 个百分点；在 Full 类别上达到 24.67%，提升 7.47 个百分点。值得注意的是，SL-HOI 在 Rare 和 Non-rare 类别上分别超过 **MP-HOI-L**（Yang et al., CVPR 2024）6.10% 和 4.86%，表明其不仅对未见交互具有强泛化能力，对常见类别同样保持优势。这一结果验证了核心设计动机：通过利用冻结 DINOv3 骨干与视觉头的互补注意力模式（骨干提供细粒度空间线索，视觉头提供全局语义上下文），SL-HOI 在单一框架内同时实现了精确的实例定位与泛化的交互分类。

**HICO-DET 开放词汇设定。** Table 2 将方法分为“有目标检测预训练”和“无目标检测预训练”两组进行公平比较——前者受益于 COCO 预训练带来的标签空间重叠，后者则完全依赖 HOI 数据。在无目标检测预训练的方法中，SL-HOI 在 Unseen/Seen/Full 上分别超过次优方法 17.26%/14.65%/15.27%，展现出极强的开放词汇泛化能力。即使在有目标检测预训练的强基线中（如 **BC-HOI**），SL-HOI 仍在 Seen 和 Full 类别上分别取得 2.16% 和 1.50% 的额外提升，证明了精简设计的竞争力。

**HICO-DET 封闭设定。** 在传统封闭词汇设定下（Table 3），SL-HOI 达到 45.05% Full mAP，超过 BC-HOI 2.04 个百分点，进一步验证了该框架在标准监督场景下的有效性。

### 消融实验

消融实验在 SWiG-HOI 数据集上系统拆解了 SL-HOI 各核心组件的贡献（Table 4、Table 5）。

![[assets/figures/papers/paper_list_l1080_https_arxiv_org_abs_2603_27500/figures/007_Table_4.jpg]]
*Table 4: Ablation study of our model’s architectural components on the SWiG-HOI dataset (mAP %)*

![[assets/figures/papers/paper_list_l1080_https_arxiv_org_abs_2603_27500/figures/010_Table_5.jpg]]
*Table 5: Ablation study of variants of our proposed method on the SWiG-HOI dataset (mAP %)*

**语义引导与层次细化的增量贡献。** 以 Late Fusion 策略（交互查询与冻结视觉头输出直接做交叉注意力）为强基线，仅添加 Semantic Bootstrapping 即可为 Unseen/Rare/Non-rare/Full 分别带来 +1.54%/+1.61%/+1.08%/+1.46% 的绝对提升。在此基础上进一步添加 Hierarchical Refinement 形成完整 SL-HOI，四个指标再分别提升 +0.95%/+1.42%/+1.79%/+1.39%。这一渐进式增益表明，语义引导通过将交互查询注入视觉头自注意力层，有效消除了查询与图像 tokens 之间的表示鸿沟；而层次细化则利用查询影响的图像 tokens 进行可学习交叉注意力，进一步挖掘了上下文信息。

**查询影响图像 tokens 的必要性。** Table 5 显示，若在 Hierarchical Refinement 中屏蔽查询对图像 tokens 的影响（Attention Mask），或完全移除交叉注意力而仅使用视觉头输出的查询，性能均出现下降。这证实了 Semantic Bootstrapping 阶段“查询影响图像 tokens”的机制是性能提升的关键——视觉头自注意力层中查询与图像 tokens 的交互使得图像 tokens 携带了交互语义，为后续细化提供了更丰富的上下文。

**检测适配器设计。** Figure 4 的消融表明，检测适配器使用 2 层自注意力编码器达到最佳性能，更多层数不会带来进一步收益。这说明轻量的特征编码已足以支撑下游的实例检测和交互分类。

**训练策略。** Table 6（附录）比较了不同训练策略：冻结全部 DINOv3 参数在 SWiG-HOI 上取得最高 Full mAP 24.67，优于部分微调或 LoRA 微调方案。这一结果与该方法的设计哲学一致——DINOv3 的骨干和视觉头已在预训练中习得了互补的注意力模式，微调反而可能破坏这种天然分工。

### 注意力图可视化分析

Figure 2 和 Figure 5 从注意力机制角度为方法设计提供了直观证据。Figure 2 显示，DINOv3 骨干的注意力呈现点状、细粒度模式，聚焦于局部空间细节；而 dino.txt 视觉头的注意力则呈全局分布，聚合了丰富的语义关系。这种天然差异正是 SL-HOI 分工利用的基础。Figure 5 进一步揭示了交互分类阶段的“Local-Global-Local”推理过程：Semantic Bootstrapping 中视觉头自注意力层先聚合全局上下文，Hierarchical Refinement 中交叉注意力再聚焦回关键局部区域，形成层次化的交互推理。

### 失败案例分析

Figure 8 展示了两个典型失败场景。在拥挤场景（如多人围坐餐桌）中，多重重叠的人-物实例增加了分配歧义，模型倾向于检测主导交互（如 sitting at, eating at），而遗漏次要交互。在小目标场景（如滑雪板、雪杖）中，模型可能出现定位偏差——ViT 下采样过程中空间信息的压缩使得细小物体的局部偏移难以区分，导致交互分类错误（如将 holding a snowboard 误判为 wearing a snowboard）。这些失败模式揭示了当前方法在密集场景和小目标条件下的固有局限，也为后续改进指明了方向：引入多尺度特征或可学习的位置编码可能在不显著增加复杂度的前提下增强鲁棒性。

![[assets/figures/papers/paper_list_l1080_https_arxiv_org_abs_2603_27500/figures/013_Figure_8.jpg]]
*Figure 8: Representative failure cases. Left: crowded scene where the detected interactions mainly include sitting at and eating at a dining table. Right: small-object detection where the detected interactions mainly include wearing, standing on, holding a snowboard, and wearing, carrying, standing on, holding, riding a skis*

### 补充图表

![[assets/figures/papers/paper_list_l1080_https_arxiv_org_abs_2603_27500/figures/005_Table_1.jpg]]
*Table 1: Comparison on the SWiG-HOI dataset (mAP %)*

![[assets/figures/papers/paper_list_l1080_https_arxiv_org_abs_2603_27500/figures/004_Table_2.jpg]]
*Table 2: Comparison on the HICO-DET dataset in the openvocabulary setting (mAP %)*

![[assets/figures/papers/paper_list_l1080_https_arxiv_org_abs_2603_27500/figures/006_Table_3.jpg]]
*Table 3: Comparison on the HICO-DET dataset in the closed setting (mAP %)*

![[assets/figures/papers/paper_list_l1080_https_arxiv_org_abs_2603_27500/figures/014_Table_6.jpg]]
*Table 6: Comparison of training recipes on the SWiG-HOI dataset (mAP %)*

![[assets/figures/papers/paper_list_l1080_https_arxiv_org_abs_2603_27500/figures/008_Figure_4.jpg]]
*Figure 4: Ablation studies on the number of encoder layers in the detection adapter on the SWiG-HOI dataset (mAP %)*

## 方法谱系与知识库定位

### 1. 问题脉络与前置工作

开放词汇人-物交互（HOI）检测的核心挑战在于同时满足精确的实例定位与泛化的交互语义理解。现有方法大致分为两条技术路线：

- **VLM 协作范式**：采用独立训练的 HOI 检测器与视觉语言模型（VLM）协作。检测器负责定位人-物对，VLM 提供开放词汇分类能力。代表工作包括 **GEN-VLKT**（Liao et al., CVPR 2022）和 **HOICLIP**（Ning et al., CVPR 2023），它们使用 CLIP 作为外部知识源，通过 late fusion 将检测特征与文本嵌入对齐。这类方法结构复杂，跨模型的表示空间差异大，融合困难。
- **单 VLM 范式**：仅使用一个 VLM 完成检测与分类，如 **THID**（Wang et al., CVPR 2022）。结构精简，但 VLM 的全局语义特征缺乏细粒度空间线索，实例定位能力弱。

近期工作试图弥合这一鸿沟。**SGC-Net**（Lin et al., CVPR 2025）通过分层粒度比较增强开放词汇分类；**MP-HOI-L**（Yang et al., CVPR 2024）引入多模态提示；**BC-HOI** 结合 BLIP-2 进行双向一致性约束。但这些方法仍未能从根本上消除定位特征与分类特征之间的表示差异。

### 2. SL-HOI 的定位：统一框架下的表示对齐

SL-HOI 的核心突破在于**在同一冻结模型内部完成表示对齐**，而非跨模型融合。其设计哲学源自对 DINOv3 内部结构的洞察：骨干网络的自注意力呈现点状、细粒度的局部关注模式，天然适合实例定位；而经过文本对齐训练的视觉头（dino.txt 变体）的自注意力呈现全局、语义丰富的关注模式，天然适合交互分类（见 Figure 2 注意力图可视化验证）。

基于这一发现，SL-HOI 将 DINOv3 的骨干与视觉头分别指派给检测与分类任务，并通过两阶段交互细化消除两者间的表示鸿沟：
1. **语义引导（Semantic Bootstrapping）**：将交互查询与图像 tokens 一同送入冻结的视觉头自注意力层，利用其预训练的全局注意力使查询与图像 tokens 在共享空间中相互适应。
2. **层次细化（Hierarchical Refinement）**：以语义增强后的查询为 query，以被查询影响后的图像 tokens 为 key/value，通过轻量可学习的单层交叉注意力进一步挖掘上下文。

这一设计使 SL-HOI 在结构上极度精简——仅添加极少可学习参数（检测适配器、交互查询投影、单层交叉注意力），所有 DINOv3 参数保持冻结。

### 3. 与关键基线的差异化对比

| 维度 | GEN-VLKT / HOICLIP | SGC-Net / MP-HOI-L | **SL-HOI（本方法）** |
|------|-------------------|-------------------|---------------------|
| 基础视觉模型 | CLIP (ViT) | CLIP / 多模态 | DINOv3 ViT-L/16（冻结） |
| 检测与分类模型 | 分离（检测器 + VLM） | 分离或部分共享 | 统一（同一 ViT 的骨干与视觉头） |
| 特征融合方式 | Late fusion（交叉注意力） | 分层比较 / 提示融合 | 语义引导 → 层次细化（自注意力 + 交叉注意力） |
| 表示对齐机制 | 无显式对齐 | 无显式对齐 | 视觉头自注意力隐式对齐查询与图像 tokens |
| 可学习参数量 | 中等 | 中等 | 极少（骨干与视觉头均冻结） |

### 4. 适用边界与局限

**适用场景**：
- 开放词汇 HOI 检测，尤其是需要泛化到未见交互类别的场景。
- 对模型精简度和推理效率有要求的部署环境（单一冻结骨干，无外部 VLM 调用）。

**已知局限**（需人工验证具体边界）：
1. **拥挤场景**：多重重叠的人-物实例增加分配歧义，可能导致漏检。论文在 Figure 8 中展示了餐厅场景下的典型失败案例。
2. **小目标检测**：ViT 下采样过程中空间信息压缩，细小物体（如叉子、滑雪板）的局部偏移难以区分，定位精度下降。
3. **冻结策略的泛化性**：当前结论基于 SWiG-HOI 数据集（Table 6），冻结全部参数优于部分微调或 LoRA。但在其他数据域（如大规模视频 HOI）是否依然成立，未经验证。
4. **统一投影的机理**：将交互嵌入统一投影到 2048 维文本空间优于分离通道加权求和，但原因未充分解释。

### 5. 开放问题

1. **表示对齐的深层机制**：语义引导为何能有效消除查询与图像 tokens 的表示差异？视觉头自注意力中的哪些参数或结构起到了关键作用？
2. **跨域泛化**：冻结策略在 SWiG-HOI 上的优势是否可迁移到 HICO-DET 封闭设定或其他视觉关系理解任务（如场景图生成）？
3. **小目标鲁棒性**：能否通过引入多尺度特征金字塔或可学习的位置编码增强小目标定位，而不显著增加复杂度？
4. **文本编码器的影响**：当前使用 dino.txt 的文本编码器，若替换为更强的文本编码器或优化提示模板，交互分类性能的提升空间有多大？
5. **扩展到其他任务**：该“骨干定位 + 视觉头语义引导”的架构范式能否推广到其他需要细粒度定位与开放词汇语义理解的视觉任务？

## 原文 PDF

![[paperPDFs/CVPR_2026/Streamlined_Open_Vocabulary_Human_Object_Interaction_Detection.pdf]]
