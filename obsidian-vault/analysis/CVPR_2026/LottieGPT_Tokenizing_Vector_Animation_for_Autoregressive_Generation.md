---
title: "LottieGPT: Tokenizing Vector Animation for Autoregressive Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LottieGPT_Tokenizing_Vector_Animation_for_Autoregressive_Generation.pdf
project_link: null
code_link: null
aliases:
- LottieGPT
tags:
- CVPR_2026
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/vision_multimodal_applications
core_operator: 设计一种能够将Lottie JSON的层次化几何图元与关键帧时间动态压缩为紧凑令牌序列的Lottie Tokenizer，并采用“静态优先、后动态”的训练策略，使自回归视觉语言模型能够学习生成矢量动画。
primary_logic: 将矢量动画视为结构化代码而非像素序列，利用Lottie格式的层次化图层和关键帧插值表示，可大幅度压缩表示长度（约34–63%），同时保留结构信息和运动质量，让通用视觉语言模型高效生成可编辑、分辨率无关的矢量动画。
claims:
- Lottie Tokenizer大幅压缩令牌数量：在MMSVG-icon上从2.6k降至1.3k（50%压缩），在LottieAnimation上从27.5k降至17.4k（63.3%压缩），且保持生成质量。
- 完整模型（Stage2）在Text+Image动画生成上取得97.83%有效率和0.9886 SSIM，远超Sora2（0.8661）等视频生成模型及few-shot大语言模型（有效率通常低于52%）。
- 去掉Lottie Tokenizer（仅用原始Lottie JSON微调）使JSON结构相似度降至0.0089，有效率仅22.61%；引入专用分词器后相似度回升至0.8062，有效率达96.96%。
- LottieBench Static Graphics (Text-Only) 上 CLIP↑ = 0.9331 (LottieGPT-Stage1)
---

# LottieGPT: Tokenizing Vector Animation for Autoregressive Generation

> [!tip] 核心洞察
> 将矢量动画视为结构化代码而非像素序列，利用Lottie格式的层次化图层和关键帧插值表示，可大幅度压缩表示长度（约34–63%），同时保留结构信息和运动质量，让通用视觉语言模型高效生成可编辑、分辨率无关的矢量动画。

| 字段 | 内容 |
|------|------|
| 中文题名 | LottieGPT: 向量动画的标记化与自回归生成 |
| 英文题名 | LottieGPT: Tokenizing Vector Animation for Autoregressive Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.11792) |
| Topic | #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/vision_multimodal_applications |
| Method | LottieGPT |
| Dataset | LottieBench Static Graphics, LottieBench Animation |

> [!tip] 效果简介
> - LottieBench Static Graphics (Text-Only) 上，CLIP↑ 0.9331 (LottieGPT-Stage1) vs 0.8321 (OmniSVG) (+0.1010)。
> - LottieBench Static Graphics (Text+Image) 上，SSIM↑ 0.8151 (LottieGPT-Stage1) vs 0.3851 (StarVector) (+0.4300)。
> - LottieBench Animation (Text-Only) 上，LPIPS↓ 0.0366 (LottieGPT-Stage2) vs 0.2528 (GPT-5 few-shot) (-0.2162)。

## 概述

**问题瓶颈**：现有生成模型仅能输出固定分辨率的栅格视频，无法生成矢量动画，导致分辨率无关性、可编辑性和结构化运动信息完全丢失。

**核心因果机制**：LottieGPT 将矢量动画重新定义为结构化代码而非像素序列。其关键设计是 **Lottie Tokenizer**——一种将 Lottie JSON 的层次化几何图元与关键帧时间动态压缩为紧凑令牌序列的专用分词器，并采用“静态优先、后动态”的两阶段课程学习策略，使自回归视觉语言模型能够高效学习生成矢量动画。

**核心洞察与压缩收益**：利用 Lottie 格式天然的层次化图层和关键帧插值表示，Lottie Tokenizer 仅存储关键帧与缓动函数，而非逐帧数据，从而大幅压缩表示长度。在 MMSVG-icon 上令牌数从 2.6k 降至 1.3k（50% 压缩），在 LottieAnimation 上从 27.5k 降至 17.4k（63.3% 压缩），且保持生成质量（Table 3）。

**主要结果**：
- **静态矢量图形**（Text+Image）：LottieGPT-Stage1 取得 SSIM 0.8151，远超 StarVector 的 0.3851（Table 2）。
- **矢量动画生成**（Text+Image）：完整模型（Stage2）有效率达 97.83%，SSIM 0.9886，远超 Sora2 的 0.8661；相比之下，few-shot 大语言模型的有效率通常低于 52%（Table 2）。
- **分词器消融**：去掉 Lottie Tokenizer 直接微调原始 JSON 使 JSON 结构相似度降至 0.0089，有效率仅 22.61%；引入专用分词器后相似度回升至 0.8062，有效率达 96.96%（Table 2）。

**方法定位**：LottieGPT 构建于 Qwen2.5-VL 视觉语言骨干之上，扩展词表引入专用 Lottie 令牌，通过 MLP 适配器将视觉特征映射到语言模型空间，以自回归方式生成 Lottie 令牌序列（Figure 3）。训练分为 Stage1（静态 Lottie 图像预训练，学习矢量构图基础）和 Stage2（动态微调，学习关键帧驱动的动画生成）。基线对比涵盖静态 SVG 生成方法（OmniSVG、StarVector）、栅格视频生成模型（Sora2、Kling、Veo 3.1）以及少样本大语言模型（GPT-5、Claude Sonnet 4.5、Gemini 2.5 Pro 等）。

**局限与开放问题**：矢量图形固有的颜色表示难以表达复杂渐变与纹理；当前分词器对粒子系统、复杂路径、高级混合模式和 3D 变换的编码效率较低；受限于上下文长度，长时序动画的时序一致性仍具挑战。未来方向包括扩展分词器以支持更丰富的动画效果、设计层次化生成策略突破长度限制，以及探索矢量与光栅混合表示。

## 背景与动机

### 矢量动画的表示困境

矢量图形与动画因其分辨率无关性、紧凑的文件体积和天然的可编辑性，在UI动效、数据可视化和数字内容创作中占据核心地位。Lottie格式作为Airbnb开源的矢量动画标准，以JSON描述层次化的几何图元、变换属性和关键帧驱动的缓动插值，已被广泛应用于移动端和Web端的高性能渲染。然而，矢量动画的自动生成仍是一个几乎未被探索的领域——现有生成模型几乎全部面向栅格输出。

### 现有方法的根本性缺口

当前主流的视觉生成范式存在两个结构性缺陷：

**栅格优先的生成路径。** 文本到视频模型（如**Sora2**、**Kling**、**Veo 3.1**）输出固定分辨率的像素帧序列，虽在视觉质量上取得了显著进展，但生成的视频丢失了结构化信息：无法缩放、无法编辑单个形状或运动曲线、无法提取图层。这些能力在专业设计工作流中是不可或缺的。

**矢量生成的静态局限。** 近期的矢量图形生成工作（如**OmniSVG**、**StarVector**）聚焦于从文本或图像合成单帧SVG代码，将矢量生成视为代码补全任务。然而，这些方法无法处理时间维度——关键帧插值、缓动曲线、图层级的动态变换均超出了其建模范围。少数尝试动画生成的方法（如LINR-bridge、AniClipart）则受限于简单的几何结构，无法处理Lottie格式中普遍存在的Group嵌套和Transform层级。

**通用大语言模型的直接失效。** 一个直观的思路是利用强大的自回归语言模型（如**GPT-5**、**Claude Sonnet 4.5**、**Gemini 2.5 Pro**、**Qwen3-235B**、**DeepSeek-V3.1**）通过少样本提示直接生成Lottie JSON代码。但实验表明，即使提供3个示例，这些模型的输出有效率普遍低于52%，且JSON结构相似度极低。根本原因在于：通用分词器将Lottie JSON视为无结构的文本流，无法捕捉层次化的几何语义和时间动态，导致生成结果频繁出现语法错误、结构缺失或不可渲染。

### 核心瓶颈与本文动机

上述缺口指向一个根本瓶颈：**现有生成模型缺乏一种能够将矢量动画的结构化时空信息紧凑编码为令牌序列的表示机制。** 栅格方法将动画展平为像素网格，丢失了结构；代码生成方法将动画视为非结构化文本，丢失了几何语义和时间约束。

本文的核心动机在于：将矢量动画重新定义为**结构化代码**而非像素序列，利用Lottie格式天然具备的层次化图层和关键帧插值表示，设计专用分词器将动画压缩为紧凑的令牌序列，使自回归视觉语言模型能够高效学习生成可编辑、分辨率无关的矢量动画。这一思路的关键洞察是：Lottie的关键帧+缓动表示天然支持时间压缩——仅存储关键帧和插值方法，而非逐帧数据，可大幅缩减序列长度（约34–63%），同时完整保留结构信息和运动质量。

## 核心创新

### 瓶颈与动机

现有生成模型在动画领域存在根本性限制：无论是视频扩散模型（如**Sora2**、**Kling**、**Veo 3.1**）还是SVG生成模型（如**OmniSVG**、**StarVector**），其输出均为固定分辨率的栅格像素，无法生成可编辑、分辨率无关的矢量动画。这种范式丢失了动画的结构化运动信息、层次化图层关系和关键帧插值语义，使得生成结果难以在专业工作流中直接使用。

LottieGPT 的核心动机在于将矢量动画重新定义为**结构化代码**而非像素序列。Lottie JSON 格式天然携带层次化图层、几何图元、变换矩阵和关键帧缓动曲线，若能将其高效压缩为紧凑的令牌序列，便可使通用视觉语言模型以自回归方式生成可编辑的矢量动画。

### 关键创新：Lottie Tokenizer

LottieGPT 的首要创新是设计了首个**Lottie Tokenizer**，能够将 Lottie JSON 的层次化几何图元与关键帧时间动态压缩为紧凑的令牌序列。其设计包含以下 changed slots：

**1. 动画表示与分词（vs. 通用文本分词器）**

基线方法（如直接微调 Lottie JSON 的**Finetuned w. Lottie JSON** 或 few-shot 大语言模型）使用通用文本分词器处理原始 JSON 字符串，导致序列冗长且丢失结构语义。Lottie Tokenizer 采用专用特殊令牌编码层次结构、形状类型（Ellipse、Fill、Gradient、Group、PolyStar、Rectangle、Rounded Corners、Stroke 等）与关键帧属性，将动画从无结构文本转化为语义对齐的令牌序列。

**2. 关键帧时间压缩（vs. 逐帧存储）**

区别于栅格视频或逐帧 SVG 的存储方式，Lottie Tokenizer 仅编码关键帧和缓动插值函数，而非每一帧数据。如 Figure 4 所示，对于 300 帧仅含 5 个关键帧的动画，压缩比可达 98%。这一设计利用了 Lottie 格式的核心特性——通过三次贝塞尔曲线（Equation 9）定义缓动，使模型只需学习关键帧参数即可重建完整运动。

**3. JSON 简化与数值压缩（vs. 完整 JSON 文本）**

在分词前，通过简化 JSON 字段、压缩数值精度、利用预设缓动编码等手段，序列长度额外减少 34%（Section 8.3），且不影响渲染质量。这一预处理步骤进一步降低了自回归模型的上下文负担。

### 训练策略创新：两阶段课程学习

LottieGPT 采用“静态优先、后动态”的两阶段训练策略（Section 4.3）：

- **Stage 1（静态预训练）**：在静态 Lottie 图像数据上学习矢量构图基础，使模型掌握形状、颜色、层次关系等基本语法。
- **Stage 2（动态微调）**：引入时间动态，学习关键帧驱动的动画生成。

消融实验（Table 2）验证了这一策略的必要性：仅完成 Stage 1 训练的模型在动画生成上有效率仅 78.35%，而完成 Stage 2 后跃升至 96.96%。这证明模型需要先建立对矢量结构的稳固理解，才能有效学习时序动态。

### 压缩效率的实证支撑

Table 3 提供了 Lottie Tokenizer 压缩效率的定量证据：

- 在 MMSVG-icon 数据集上，令牌数从 2.6k 降至 1.3k（50% 压缩）
- 在 LottieAnimation 数据集上，令牌数从 27.5k 降至 17.4k（63.3% 压缩）
- 量化后可进一步压缩至原始长度的 24%

### 方法谱系与知识库定位

LottieGPT 在矢量图形生成领域填补了从**静态 SVG 生成**到**矢量动画生成**的关键空白：

- 静态矢量生成方面，**OmniSVG** 和 **StarVector** 分别实现了文本到 SVG 和图像到 SVG 的生成，但无法处理时间维度。
- 视频生成方面，**Sora2**、**Kling**、**Veo 3.1** 等扩散模型可生成高质量栅格视频，但输出不可编辑且分辨率固定。
- 少样本大语言模型方案（**GPT-5**、**Claude Sonnet 4.5**、**Gemini 2.5 Pro**、**Qwen3-235B**、**DeepSeek-V3.1**）虽能输出 Lottie JSON 文本，但有效率通常低于 52%，且缺乏对矢量结构的深层理解。

LottieGPT 通过专用分词器与两阶段训练，首次将自回归视觉语言模型（基于 **Qwen2.5-VL** 架构）应用于矢量动画生成，在保持可编辑性和分辨率无关性的同时，取得了远超所有基线的生成质量与有效率。

### 局限与开放问题

当前 Lottie Tokenizer 对复杂效果（粒子系统、高级混合模式、3D 变换等）的编码效率较低，且受限于视觉语言模型的上下文长度，长时序复杂动画的生成仍具挑战。如何扩展分词器以覆盖更丰富的动画效果、设计层次化生成策略突破上下文限制，是值得探索的方向。

## 整体框架

LottieGPT 的整体框架建立在预训练视觉语言模型 **Qwen2.5-VL** 之上，通过引入专用的 **Lottie Tokenizer** 和两阶段课程学习策略，将矢量动画生成转化为自回归令牌预测任务。图3展示了系统的完整架构。

**多模态输入编码**。模型接受文本描述与可选的图像/关键帧作为条件输入。文本通过语言模型的标准分词器编码，图像则经过 Qwen2.5-VL 的视觉编码器提取特征，再通过一个 **MLP 适配器** 将视觉特征映射到语言模型的表示空间。所有输入最终被统一为前缀令牌序列，为后续的自回归生成提供多模态条件 $\mathbf{c}$。

**Lottie Tokenizer：结构化动画令牌化**。这是框架的核心创新模块。与直接使用原始 Lottie JSON 文本进行分词不同，Lottie Tokenizer 将 Lottie 文件的层次化结构——包括图层（Layer）、几何图元（Ellipse、Rectangle、PolyStar、Fill、Stroke、Gradient 等）、变换矩阵以及关键帧驱动的动画属性——分解为一组紧凑的、语义对齐的特殊令牌。具体而言，Tokenizer 对动画元信息（版本、帧率、尺寸）、每个图层的类型与变换参数、形状的几何属性以及时间维度的关键帧与缓动函数进行结构化编码，而非存储逐帧数据。这一设计使得表示长度大幅压缩：在 MMSVG-icon 上令牌数从 2.6k 降至 1.3k（50% 压缩），在 LottieAnimation 上从 27.5k 降至 17.4k（63.3% 压缩），且量化后可进一步压缩至 24%（Table 3）。

**两阶段课程学习**。训练采用“静态优先、后动态”的策略：
- **Stage 1（静态预训练）**：模型首先在静态 Lottie 图形数据上学习矢量构图的基础知识，包括几何形状的布局、颜色填充与层次关系。
- **Stage 2（动态微调）**：在 Stage 1 的基础上引入时间动态，使模型学习关键帧驱动的动画生成，包括属性值随时间的变化与缓动插值。

两个阶段均采用标准因果语言建模损失进行自回归训练：

$$\mathcal{L} = - \sum_{i=1}^{N} \log P(t_i \mid t_{<i}, \mathbf{c})$$

其中 $t_i$ 为当前令牌，$t_{<i}$ 为前缀令牌序列，$\mathbf{c}$ 为多模态条件。

**数据流转**。图2展示了完整的数据采集与处理流程：从互联网收集约 10M SVG 资源和 660K After Effects 动画资源，转换为 Lottie JSON 格式后，经过不影响渲染结果的简化算法进行过滤，并使用 QwenVL 为矢量图形和动画生成文本标注。此外，在训练前还对 Lottie JSON 进行字段简化与数值精度压缩，使序列长度额外减少约 34%（Section 8.3），进一步降低了自回归模型的上下文负担。

**消融验证**。框架中各组件的必要性得到了严格的消融实验支持。去掉 Lottie Tokenizer、仅用原始 Lottie JSON 微调时，JSON 结构相似度骤降至 0.0089，有效率仅 22.61%；而引入专用分词器后相似度回升至 0.8062，有效率达 96.96%（Table 2）。同样，仅完成 Stage 1 训练的模型在动画生成上的有效率仅 78.35%，远低于完整两阶段训练的 96.96%，验证了课程学习策略的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l994_https_arxiv_org_abs_2604_11792/figures/003_Figure_3.jpg]]
*Figure 3: Overview of LottieGPT. LottieGPT is built upon the pre-trained vision-language model Qwen2.5-VL and incorporates a Lottie tokenizer. The model encodes both text and image inputs as prefix tokens, while the Lottie tokenizer encodes vector animation commands into a unified representation space. We first train the model on static Lottie images, followed by training on Lottie animations*

![[assets/figures/papers/paper_list_l994_https_arxiv_org_abs_2604_11792/figures/002_Figure_2.jpg]]
*Figure 2: Data curation pipeline. We collected 10M SVG resources and 660K After Effects (AE) animation resources from the internet, then converted them to Lottie Json format, filtered them using simplification algorithms that do not affect rendering results, and used QwenVL to generate text labels for vector graphics and vector animations*

## 核心模块与公式推导

LottieGPT 的核心架构由三个关键模块构成：**Lottie Tokenizer**（动画标记化）、**Qwen2.5-VL 视觉语言骨干**（多模态编码）与**自回归语言模型**（序列生成）。三者协同实现从文本或图像条件到结构化 Lottie JSON 的端到端生成。

### Lottie Tokenizer：结构化动画的紧凑编码

Lottie Tokenizer 是整个系统的核心创新，其设计目标是将层次化的 Lottie JSON 动画文件转换为紧凑的、语义对齐的令牌序列。与处理像素帧的传统方法不同，该分词器直接编码几何图元、层次分组、关键帧属性曲线及插值方法，实现了**关键帧级时间压缩**而非逐帧存储（Figure 4）。

![[assets/figures/papers/paper_list_l994_https_arxiv_org_abs_2604_11792/figures/005_Figure_4.jpg]]
*Figure 4: Unlike raster pixel-based videos or frame-by-frame saved SVGs, the Lottie Tokenizer only stores keyframes and interpolation methods, which significantly reduces the number of tokens required to represent an animation. In the figure, KF denotes keyframes, while F represents frames obtained through easing-based animation interpolation*

分词过程分为三个层次：

1. **动画元信息编码**：将 Lottie 文件的全局属性（版本号、帧率、起止帧、画布尺寸、3D 标志）映射为专用令牌序列。格式为 `<|M|> <|v|> • 5.9.5 • <|fr|> 30 <|ip|> 0 <|op|> 90 <|w|> 512 <|h|> 512 <|3d|> 0`，其中 `fr` 表示帧率，`ip/op` 分别标记入点和出点帧号。

2. **图层与形状编码**：每个图层以 `<|LAYER|>` 令牌起始，后接图层类型（`ty`）、透明度（`op`）、起始时间（`st`）、混合模式（`bm`）等属性。形状图元（椭圆、填充、渐变、群组、多角星形、矩形、圆角、描边等）直接以专用令牌编码，无需分解为独立线段，从而保留了 Lottie 格式的结构语义。

3. **关键帧时间压缩**：这是分词器区别于先前工作的核心机制。Lottie 动画通过关键帧和缓动函数定义属性随时间的变化，分词器仅编码关键帧值及其插值方法，而非每一帧的完整状态。压缩比随动画时长增长而提升——在 300 帧仅含 5 个关键帧的极端情况下，压缩比可达 98%（Figure 4）。

### 缓动函数的数学表达

Lottie 动画的运动节奏由三次贝塞尔缓动曲线控制。给定归一化时间进度 $t_{\mathrm{norm}} \in [0, 1]$，缓动后的动画进度为：

$$t_{\mathrm{eased}} = f(t_{\mathrm{norm}})$$

其中 $f$ 由三次贝塞尔曲线定义：

$$\mathbf{B}(u) = (1-u)^3 P_0 + 3(1-u)^2 u P_1 + 3(1-u)u^2 P_2 + u^3 P_3$$

端点固定为 $P_0 = (0, 0)$、$P_3 = (1, 1)$，控制点 $P_1(o_x, o_y)$ 和 $P_2(i_x, i_y)$ 决定曲线形状。通过对 $u$ 求解 $\mathbf{B}_x(u) = t_{\mathrm{norm}}$ 获得参数 $u$，再代入 $\mathbf{B}_y(u)$ 得到缓动后的进度值（Figure 24 展示了典型缓动曲线的效果）。

![[assets/figures/papers/paper_list_l994_https_arxiv_org_abs_2604_11792/figures/022_Figure_24.jpg]]
*Figure 24: Bezier easing curve transforms time progress (x-axis) ´ into animation progress (y-axis). At 25% time, animation has only progressed 16% (slow start); at 75% time, animation has reached 84% (slow end)*

统计表明，Lottie 动画中最常见的 8 种缓动曲线覆盖了 75.4% 的使用场景（Figure 25），其中第三种最常用模式（15.78%）的控制点 $(0.167, 0.167)$ 和 $(0.833, 0.833)$ 位于线性对角线上，功能上与线性插值等价。分词器利用这一冗余，将高频缓动模式编码为预设令牌，进一步压缩序列长度。

![[assets/figures/papers/paper_list_l994_https_arxiv_org_abs_2604_11792/figures/024_Figure_25.jpg]]
*Figure 25: Top 8 most common Bezier easing curves in Lottie animations, covering 75.4% of all usage. Each curve is defined by control ´ points*

### JSON 扁平化与结构评估

为评估生成动画的结构保真度，LottieGPT 引入 JSON 扁平化操作，将嵌套结构展开为键值对集合：

$$\Phi(\mathcal{I}) = \{ (k, v) \mid k \in K(\mathcal{I}) \}$$

其中 $k$ 为层次路径（如 `layers[0].shapes[1].ty`），$v$ 为对应值。基于此，定义键 F1 分数衡量拓扑准确性：

$$\mathrm{Key}\text{-}F_1 = \frac{2 |\mathcal{K}^c|}{|\mathcal{K}^{\mathrm{gt}}| + |\mathcal{K}^{\mathrm{pred}}|}$$

其中 $\mathcal{K}^c = \mathcal{K}^{\mathrm{gt}} \cap \mathcal{K}^{\mathrm{pred}}$ 为公共键集。最终的结构相似度综合得分以 7:3 权重结合键匹配和数值匹配：

$$\mathrm{JsonStructSim} = 0.7 \cdot \mathrm{Key}\text{-}F_1 + 0.3 \cdot \mathrm{ValueMatch}$$

其中 $\mathrm{ValueMatch} = \frac{1}{|\mathcal{N}|} \sum_{k \in \mathcal{N}} |v_k^{\mathrm{gt}} - v_k^{\mathrm{pred}}|$ 为数值键上的平均绝对误差。

### 自回归训练目标

整个模型以标准因果语言建模目标进行端到端训练：

$$\mathcal{L} = - \sum_{i=1}^{N} \log P(t_i \mid t_{<i}, \mathbf{c})$$

其中 $t_i$ 为第 $i$ 个令牌，$\mathbf{c}$ 为多模态条件（文本或文本+图像前缀）。训练采用两阶段课程学习策略：Stage 1 在静态 Lottie 图像数据上学习矢量构图基础，Stage 2 引入时间动态学习关键帧驱动的动画生成。消融实验证实，仅完成 Stage 1 的模型在动画生成上的有效率仅为 78.35%，而完整两阶段训练后提升至 96.96%（Table 2），验证了该策略的必要性。

## 实验与分析

### 核心实验设计

LottieGPT 的评估体系覆盖五个维度：视觉质量（SSIM、LPIPS、DINOv2）、语义一致性（CLIP）、结构保真度（JsonStructSim）、内容准确性（ValueMatch）以及渲染成功率（Valid Rate）。测试集按令牌数量分层为 Simple（150 样本）、Medium（40 样本）与 Complex（40 样本）三个难度级别，以考察模型在不同复杂度下的泛化能力。

关键对比基线包括：静态矢量图形生成方法 **OmniSVG** 与 **StarVector**；栅格视频生成模型 **Sora2**、**Kling** 与 **Veo 3.1**；以及少样本提示下的大语言模型 **GPT-5**、**Claude Sonnet 4.5**、**Gemini 2.5 Pro**、**Qwen3-235B** 与 **DeepSeek-V3.1**。值得注意的是，矢量动画基线方法（LINR-bridge、AniClipart）因无法处理含有 Group 和 Transform 的 Lottie 结构而未能参与定量对比；视频生成基线仅能在渲染帧上计算视觉指标，无法评估结构层和有效率。

### 主要结果

#### 静态矢量图形生成

在 LottieBench 静态图形任务上，LottieGPT-Stage1 展现出全面优势（Table 2）。Text-Only 设置下，CLIP 得分达到 0.9331，较 OmniSVG（0.8321）提升 **+0.1010**；Text+Image 设置下，SSIM 达到 0.8151，较 StarVector（0.3851）提升 **+0.4300**。这一优势的因果链条清晰：Lottie Tokenizer 对层次化几何图元的原生编码能力，使模型能够直接学习矢量构图的拓扑关系，而非从 SVG 代码文本中隐式推断结构。值得强调的是，LottieGPT-Stage1 仅使用 750K MMSVG-Icon 样本训练，而 OmniSVG 使用了 2M 样本（含 MMSVG-Illustrations），数据量劣势下的全面领先进一步验证了分词器设计的有效性。

![[assets/figures/papers/paper_list_l994_https_arxiv_org_abs_2604_11792/figures/006_Table_2.jpg]]
*Table 2: Lottie image and animation generation with Text-Only, Text+Image input*

#### 矢量动画生成

在动画生成任务上，LottieGPT-Stage2 的优势更为显著（Table 2）。Text-Only 设置下，LPIPS 低至 0.0366，而最强少样本 LLM 基线 GPT-5 仅为 0.2528，差距达 **-0.2162**；Text+Image 设置下，SSIM 达到 0.9886，远超 Sora2（0.8661）等视频生成模型，提升 **+0.1225**。

更关键的是渲染成功率指标：LottieGPT-Stage2 在 Text+Image 动画生成上达到 **97.83%** 的有效率，而少样本 LLM 基线中表现最好的 Claude Sonnet 4.5 仅为 51.74%，GPT-5 和 DeepSeek-V3.1 的有效率甚至低于 27%。这一鸿沟揭示了通用 LLM 在结构化代码生成中的根本性局限——缺乏专用分词器时，模型需要同时学习 JSON 语法、Lottie 模式与动画语义，令牌预算被大量消耗在语法细节上，导致结构性错误频发。

用户调研（Table 5，20 名参与者，5 分制）进一步验证了主观质量优势：LottieGPT 在视觉质量、运动自然度与整体偏好三个维度上均获得最高评分。

![[assets/figures/papers/paper_list_l994_https_arxiv_org_abs_2604_11792/figures/023_Table_5.jpg]]
*Table 5: User study results (5-point scale, 20 participants). LottieGPT achieves the highest ratings across all metrics*

### 消融实验

#### Lottie Tokenizer 的必要性

最关键的消融是将 Lottie Tokenizer 替换为原始 Lottie JSON 文本微调（Table 2，“Finetuned w. Lottie Json”）。结果表明，JsonStructSim 从 0.8062 骤降至 **0.0089**，有效率从 96.96% 暴跌至 **22.61%**。这一消融揭示了瓶颈的本质：通用文本分词器将 JSON 键名、数值和结构符号切分为碎片化的子词令牌，破坏了层次化几何图元与关键帧动态之间的语义关联，使模型难以学习有效的动画生成策略。

#### 两阶段训练的必要性

仅完成 Stage1 训练的模型在动画生成上有效率为 78.35%，远低于 Stage2 的 96.96%（Table 2）。这验证了“静态优先、后动态”课程学习策略的有效性：Stage1 建立了矢量构图的基础表征，Stage2 在此基础上引入时间动态，避免了同时学习空间结构与运动模式的困难。

#### 压缩效率

Lottie Tokenizer 在不同数据集上展现出显著的压缩效果（Table 3）：在 MMSVG-icon 上从 2.6k 令牌降至 1.3k（**50%** 压缩），在 LottieAnimation 上从 27.5k 降至 17.4k（**63.3%** 压缩）。进一步量化后，压缩率可提升至 **24%**。压缩的因果机制来自三个层面：简化 JSON 字段使序列长度减少 34%；关键帧插值替代逐帧存储（300 帧仅需 5 个关键帧时可实现 98% 压缩）；利用预设缓动编码消除冗余贝塞尔参数。

![[assets/figures/papers/paper_list_l994_https_arxiv_org_abs_2604_11792/figures/008_Table_3.jpg]]
*Table 3: Tokenizer comparison on MMSVG-icon and LottieAnimation datasets. Our Lottie tokenizer achieves significantly better compression ratios while maintaining generation quality*

### 失败模式与局限性

LottieGPT 的典型失败案例（Figure 13）表现为可渲染但视觉不一致：生成结果中出现多余或缺失的形状，偏离预期设计。这类错误的根源在于自回归解码的累积误差——早期令牌的微小偏差通过层次化依赖关系传播至后续几何图元，导致整体构图的偏移。

![[assets/figures/papers/paper_list_l994_https_arxiv_org_abs_2604_11792/figures/017_Figure_13.jpg]]
*Figure 13: LottieGPT may still generate cases that are renderable but visually inconsistent with expectations, typically manifesting as extraneous or missing shapes relative to the intended design*

更根本的局限来自矢量图形本身的表达能力边界：难以表示真实照片中的复杂渐变、纹理和细节。当前 Lottie 格式与分词器对粒子系统、复杂路径、高级混合模式和 3D 变换的编码效率较低。此外，受限于视觉语言模型的上下文长度，生成长时间复杂动画时的时序一致性仍具挑战。

### 关键图表结论

- **Table 2** 构成实验部分的核心证据矩阵，覆盖静态图形与动画生成在 Text-Only 和 Text+Image 两种输入模式下的全部指标对比。LottieGPT 在所有设置下均取得最优结果，且在有效率指标上形成对少样本 LLM 的压倒性优势。
- **Table 3** 量化了 Lottie Tokenizer 的压缩效率，支撑“关键帧插值压缩”这一核心设计动机。
- **Figure 8 与 Figure 9** 分别展示 Text-to-Animation 和 Text+Image-to-Animation 的定性比较，揭示了少样本 LLM 基线频繁出现不可渲染输出的问题（多次尝试后仍标记为 ✗）。
- **Figure 13** 呈现失败案例，为理解模型的能力边界提供了直观参考。

![[assets/figures/papers/paper_list_l994_https_arxiv_org_abs_2604_11792/figures/012_Figure_8.jpg]]
*Figure 8: For the Text-to-Animation task, all LLM baselines were provided with identical 3-shot examples. ✗ indicates that no renderable Lottie JSON was obtained even after the fifth attempt. More results on vector animation can be found in the supplementary video and on the project website*

![[assets/figures/papers/paper_list_l994_https_arxiv_org_abs_2604_11792/figures/013_Figure_9.jpg]]
*Figure 9: Using Text+Image as input to generate animations. Few-shot refers to providing three description-Lottie JSON data pairs. Except for Deepseek which does not support image input, all other methods use a single image and text description as input. pass@x indicates that x attempts were required to generate a renderable Lottie JSON. ✗ indicates that no renderable Lottie JSON was obtained even after the fifth attempt*

### 补充图表

![[assets/figures/papers/paper_list_l994_https_arxiv_org_abs_2604_11792/figures/016_Figure_12.jpg]]
*Figure 12: A manually edited Lottie animation where we modified the wing color using LottieLab*

## 方法谱系与知识库定位

### 1. 问题定位与基线对比

LottieGPT 处于**矢量图形生成**与**视频生成**两个领域的交叉地带，其核心贡献在于首次将自回归视觉语言模型应用于结构化矢量动画的生成。现有的基线方法可归为以下四类，每一类在关键维度上均存在 LottieGPT 所填补的空白：

**（1）静态矢量图形生成方法**

- **OmniSVG** 与 **StarVector** 代表了当前基于 SVG 代码合成的静态矢量图形生成前沿。OmniSVG 通过文本到 SVG 的序列生成实现静态矢量图形合成，StarVector 则聚焦于图像到 SVG 的转换。两者的共同局限在于：仅能生成单帧静态图形，完全不涉及时间动态建模，且依赖通用文本分词器处理 SVG 代码，未能利用矢量格式的结构化特性进行压缩。LottieGPT 在静态图形子任务（Stage1）上已全面超越上述方法——在仅使用 750K 训练样本（OmniSVG 使用 2M）的条件下，Text-Only 场景下 CLIP 得分领先 0.1010，Text+Image 场景下 SSIM 领先 0.4300（Table 2），验证了 Lottie Tokenizer 在静态矢量表示上的压缩与语义对齐优势。

**（2）文本/图像到栅格视频生成方法**

- **Sora2**、**Kling**、**Veo 3.1** 等商业视频生成模型输出固定分辨率的栅格视频，无法生成可编辑的矢量动画。尽管这些模型在渲染帧的视觉质量上具有竞争力（Sora2 在 Text+Image 动画生成上 SSIM 为 0.8661），但 LottieGPT-Stage2 在同一指标上达到 0.9886（Table 2），且在 LPIPS 上以 0.0278 显著优于 Sora2 的 0.1447。更关键的是，栅格视频模型完全无法评估结构层指标（Key-F1、JsonStructSim）和有效率（Valid Rate），因为其输出根本不包含可解析的矢量结构。这一对比揭示了 LottieGPT 在**表示维度**上的根本性差异：将动画视为结构化代码而非像素序列。

**（3）大语言模型的少样本 Lottie JSON 生成**

- **GPT-5**、**Claude Sonnet 4.5**、**Gemini 2.5 Pro**、**Qwen3-235B**、**DeepSeek-V3.1** 等前沿 LLM 在 few-shot 提示下可尝试生成 Lottie JSON，但有效率普遍低于 52%（Table 2），且即使成功渲染，视觉质量也远逊于专用模型（GPT-5 在 Text-Only 动画上 LPIPS 为 0.2528，LottieGPT 为 0.0366）。这一对比揭示了通用 LLM 的文本分词器在处理高度结构化的 Lottie JSON 时的根本性低效——缺乏对层次化几何图元、关键帧动态和缓动函数的语义感知，导致生成结果频繁出现语法错误或逻辑不一致。

**（4）矢量动画专用方法**

- **LINR-bridge** 与 **AniClipart** 等矢量动画方法受限于其设计假设，无法处理包含 Group 和 Transform 的 Lottie 层次结构，因此未能直接参与定量对比。这一空白恰恰凸显了 LottieGPT 在**格式兼容性**上的独特优势：Lottie Tokenizer 原生支持 Lottie 格式的完整层次化图层、变换矩阵和关键帧插值，覆盖了实际动画制作中的主流需求。

### 2. 关键设计选择与消融证据

LottieGPT 的性能优势可归因于三个因果可控的设计槽位，每个槽位的贡献均有消融实验支撑：

| 设计槽位 | 基线取值 | LottieGPT 取值 | 消融证据 |
|---------|---------|---------------|---------|
| 动画表示与分词 | 通用文本分词器处理原始 JSON | Lottie Tokenizer 用特殊令牌编码层次、形状与关键帧 | 去掉 Lottie Tokenizer 后 JsonStructSim 从 0.8062 降至 0.0089，Valid Rate 从 96.96% 降至 22.61%（Table 2） |
| 训练策略 | 混合静态/动态数据联合训练 | 两阶段课程学习（Stage1 静态 → Stage2 动态） | 仅 Stage1 训练的模型在动画生成上 Valid Rate 仅 78.35%，远低于 Stage2 的 96.96%（Table 2） |
| 数据表示压缩 | 无压缩的完整 JSON 文本 | 简化字段、压缩精度、利用预设缓动编码，序列长度减少 34% | Lottie Tokenizer 在 MMSVG-icon 上压缩 50% 令牌，在 LottieAnimation 上压缩 63.3%（Table 3） |

**Lottie Tokenizer 的因果机制**：通用文本分词器将 Lottie JSON 视为无结构的字符流，导致两个致命问题——（a）序列长度膨胀，超出 LLM 的有效上下文建模范围；（b）语义单元被碎片化，模型难以学习层次化图层与关键帧之间的长程依赖。Lottie Tokenizer 通过将每个几何图元（Ellipse、Fill、Gradient、Group 等）、每个变换属性（位置、旋转、缩放）和每个关键帧动态编码为独立令牌，使令牌序列与动画的语义结构对齐，从而大幅降低了自回归建模的难度。

**两阶段课程学习的必要性**：Stage1（静态预训练）使模型先掌握矢量图形的基本构图规律（形状组合、颜色填充、层次关系），Stage2（动态微调）再引入时间维度的关键帧插值。消融实验表明，跳过 Stage1 直接训练动画生成会导致模型在结构一致性上的严重退化，验证了“先静态后动态”的课程设计对复杂时序生成的必要性。

### 3. 适用边界与局限

LottieGPT 的能力边界受以下因素制约：

**（1）颜色与纹理的表达能力限制**：矢量图形的本质决定了其难以表达真实照片中的复杂渐变、纹理和细节。LottieGPT 生成的动画在颜色保真度上天然受限，这是矢量表示本身的信息瓶颈，而非模型设计缺陷。对于需要照片级真实感的应用场景，栅格视频生成方法（如 Sora2）仍是更合适的选择。

**（2）复杂动画效果的编码效率**：当前 Lottie Tokenizer 对粒子系统、复杂贝塞尔路径、高级混合模式和 3D 变换等专业动画效果的编码效率较低。这些效果在 Lottie 格式中本身就有复杂的参数化表示，将其纳入紧凑的令牌序列需要进一步的分词器设计。图 26 中的弹性缓动动画示例揭示了极端下冲场景下数值精度的挑战——在 165.8% 的超调量下，关键帧之间的插值行为对数值误差高度敏感。

**（3）上下文长度与时序一致性**：受限于底层视觉语言模型（Qwen2.5-VL）的上下文窗口，LottieGPT 在生成长时间复杂动画时面临时序一致性的挑战。虽然 Lottie Tokenizer 的关键帧压缩机制已大幅减少了令牌数量（在 300 帧/5 关键帧场景下可达 98% 压缩率），但对于包含大量图层和形状的复杂动画，令牌序列仍可能超出模型的可靠建模范围。

**（4）数据覆盖的偏向性**：训练数据来源于 10M SVG 资源和 660K After Effects 动画资源的自动转换与筛选，其风格分布可能偏向特定类型的矢量图形（如图标、插画），对某些小众动画风格（如手绘逐帧动画、抽象动态图形）的泛化能力需要进一步验证。

### 4. 开放问题与未来方向

基于上述局限，以下开放问题值得后续工作关注：

1. **分词器的表达能力扩展**：如何设计 Lottie Tokenizer 的扩展方案，以更高效地编码粒子系统、复杂路径操作、高级混合模式与 3D 变换？这可能需要引入层次化的令牌结构或可学习的令牌压缩机制。

2. **长时序生成的层次化策略**：能否通过先规划动画的宏观结构（场景分割、镜头切换），再逐段生成细节的层次化生成策略，来突破上下文长度的限制？这与视频生成中的“先粗后精”范式有相似之处，但需要在矢量动画的结构化表示空间中重新设计。

3. **矢量-栅格混合表示**：能否通过混合矢量与光栅表示来兼顾紧凑性与色彩保真度？例如，用矢量表示动画的主体结构和运动，用光栅纹理贴图补充复杂渐变和纹理细节。这一方向需要在表示的统一性和生成的端到端性之间寻找平衡。

4. **可编辑性的量化评估**：当前评估体系主要关注渲染质量和结构相似度，但矢量动画的核心价值——可编辑性——尚未有系统的量化指标。如何设计衡量生成动画的图层可分离性、运动可调整性和形状可修改性的评估基准，是推动该领域发展的关键问题。

5. **交互式动画编辑的闭环**：LottieGPT 生成的动画已展示出在 LottieLab 中进行手动编辑的能力（Figure 12），但如何实现“生成-编辑-再生成”的交互闭环，使用户能够通过自然语言指令迭代修改动画的特定属性，是一个具有实际应用价值的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/LottieGPT_Tokenizing_Vector_Animation_for_Autoregressive_Generation.pdf]]
