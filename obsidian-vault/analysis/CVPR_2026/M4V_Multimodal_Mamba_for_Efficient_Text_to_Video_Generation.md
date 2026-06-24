---
title: "M4V: Multimodal Mamba for Efficient Text-to-Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/M4V_Multimodal_Mamba_for_Efficient_Text_to_Video_Generation.pdf
project_link: "https://huangjch526.github.io/M4V_project/"
code_link: null
aliases:
- MMMVM
- M4V
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将模型中的统一Transformer块替换为具有线性复杂度的多模态扩散Mamba（MM-DiM）块，通过对输入序列进行多模态令牌重组来弥补Mamba缺乏显式跨模态交互的缺点。
primary_logic: 通过在序列起始和末尾两次放置文本令牌实现双向信息流，结合zigzag空间扫描和逐帧可学习寄存器，使得Mamba的状态空间模型能够有效感知文本、空间和时间关系，从而在几乎不损失生成质量的前提下大幅降低计算量。
claims:
- MM-DiM块在生成768×1280视频时比全注意力基线减少45%的FLOPs
- 在VBench基准上，M4V (PyramidFlow) 得到81.55总分，M4V (Wan2.1) 得到86.14总分，均为使用公开数据训练的模型中的最佳结果
- 消融实验中，文本令牌重组显著提升文本-视频对齐指标，逐帧寄存器和时序分支分别提升了视频质量指标和总体得分，且组合后达到最佳效率-性能平衡
- VBench 上 Total Score = 81.55 (M4V-PyramidFlow) / 86.14 (M4V-Wan2.1)
---

# M4V: Multimodal Mamba for Efficient Text-to-Video Generation

> [!tip] 核心洞察
> 通过在序列起始和末尾两次放置文本令牌实现双向信息流，结合zigzag空间扫描和逐帧可学习寄存器，使得Mamba的状态空间模型能够有效感知文本、空间和时间关系，从而在几乎不损失生成质量的前提下大幅降低计算量。

| 字段 | 内容 |
|------|------|
| 中文题名 | M4V：面向高效文本生成视频的多模态Mamba框架 |
| 英文题名 | M4V: Multimodal Mamba for Efficient Text-to-Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Huang_M4V_Multimodal_Mamba_for_Efficient_Text-to-Video_Generation_CVPR_2026_paper.html) · [Project](https://huangjch526.github.io/M4V_project/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | M4V (Multi-Modal Video Mamba) |
| Dataset | VBench, Computational efficiency |

> [!tip] 效果简介
> - VBench 上，Total Score 81.55 (M4V-PyramidFlow) / 86.14 (M4V-Wan2.1) vs N/A (公开数据训练模型的最佳结果) (N/A)。
> - Computational efficiency (241-frame, 768p) 上，TFLOPs (mixer layers) 29.52 (Full+Temp-Branch) vs 55.44 (Full Attention) (-46.7%)。

## 概述

**核心瓶颈**：基于Transformer的视频扩散模型在处理长序列高分辨率视频时，其自注意力机制的二次复杂度（$\mathcal{O}((T M)^2)$，$T$为帧数，$M$为每帧序列长度）导致计算成本极高，严重制约了实际部署的可扩展性。

**方法定位**：M4V是一个以状态空间模型（SSM）为核心的高效文本生成视频框架。其核心创新在于设计**多模态扩散Mamba（MM-DiM）块**，替代传统DiT架构中的统一Transformer块，将计算复杂度从二次降至线性（$\mathcal{O}(T M + T^2)$）。为克服Mamba缺乏显式跨模态交互的固有局限，MM-DiM块引入了三项关键技术：**双向令牌重组**（文本令牌置于序列首尾实现双向信息流）、**Zigzag空间扫描与逐帧寄存器**（增强空间感知与帧边界识别）、以及**轻量时序因果注意力分支**（补充长程时序依赖）。该方法在保持生成质量的前提下大幅降低计算开销。

**主要结果**：在VBench基准上，M4V（PyramidFlow）获得81.55总分，M4V（Wan2.1）获得86.14总分，均为使用公开数据训练的模型中的最佳结果。在768×1280分辨率下生成241帧视频时，MM-DiM块相比全注意力基线减少约45%的FLOPs（29.52 vs 55.44 TFLOPs）。消融实验证实，文本令牌重组显著提升文本-视频对齐，逐帧寄存器与轻量时序分支分别提升视频质量指标和总体得分，三者组合达到最优效率-性能平衡。

## 背景与动机

文本生成视频（Text-to-Video, T2V）旨在根据自然语言描述合成逼真且时序连贯的视频序列。近年来，基于扩散模型（Diffusion Models）的方法在该领域取得了显著进展，涌现出如**Sora**、**Kling**、**Gen-3 Alpha**等商业级系统，以及**CogVideoX**、**Open-Sora Plan**、**PyramidFlow**、**Wan2.1**等开源方案。这些模型通常采用基于Transformer的扩散主干网络（Diffusion Transformer, DiT），利用自注意力机制对文本和视觉令牌进行统一建模。

然而，Transformer架构的核心瓶颈在于自注意力机制的计算复杂度与序列长度呈二次关系。在视频生成场景中，输入序列需同时包含空间维度上平展的视觉令牌和文本令牌，当处理高分辨率、长时长视频时，序列长度急剧膨胀——例如，一段241帧、768p分辨率的视频，其全序列注意力复杂度可达$\mathcal{O}((T M)^2)$，其中$T$为帧数，$M$为每帧序列长度。这导致训练和推理的计算成本极高，严重限制了实际部署的规模和效率。

为应对这一挑战，状态空间模型（State Space Models, SSMs）——特别是**Mamba**——因其线性复杂度$\mathcal{O}(T M)$而受到关注。Mamba通过输入依赖的参数化机制（$\mathbf{A}$、$\mathbf{B}$、$\mathbf{C}$、$\Delta$随输入变化）增强了传统SSM的表达能力，在长序列建模上展现出与Transformer相当的性能，同时保持线性计算开销。然而，将Mamba直接应用于多模态视频生成面临两个根本性困难：

1. **缺乏显式跨模态交互机制**：Mamba本质上是序列到序列的映射，不具备Transformer中QKV注意力天然赋予的跨令牌信息交换能力。在文本-视频生成中，文本语义需要有效地注入视觉生成过程，而视觉信息也应反向影响文本理解，这种双向交互在原生Mamba中难以实现。

2. **时空依赖建模不足**：视频数据包含复杂的空间结构和时序动态。标准的1D扫描策略无法充分捕获二维空间中的局部邻域关系，而简单的逐帧串行处理则忽略了帧间长程时序依赖。Mamba的递归状态更新虽能传递时序信息，但在长序列中可能面临信息衰减问题。

针对上述问题，本文提出**M4V（Multi-Modal Video Mamba）**——一个基于多模态Mamba的高效文本生成视频框架。M4V的核心动机并非完全抛弃Transformer，而是在保留前端多模态DiT块（来自**FLUX**）的前提下，将后续计算密集的统一Transformer块替换为所提出的**多模态扩散Mamba（MM-DiM）块**。通过精心设计的令牌重组策略、空间扫描机制和轻量时序分支，MM-DiM块在几乎不损失生成质量的前提下，将计算量大幅降低——在生成768×1280分辨率视频时，相比全注意力基线减少**45%的FLOPs**（见**Figure 1**）。这一设计使得M4V能够在公开数据训练的条件下，在VBench基准上取得领先的生成质量（M4V-PyramidFlow总分81.55，M4V-Wan2.1总分86.14），同时保持显著的计算效率优势。

## 核心创新

M4V的核心创新在于用**多模态扩散Mamba（MM-DiM）块**替代视频扩散模型中的统一Transformer块，从根本上解决了自注意力机制的二次复杂度瓶颈。这一替换并非简单的算子更换，而是围绕Mamba状态空间模型（SSM）的固有局限——缺乏显式跨模态交互能力——进行了三项关键设计，形成了一套完整的**changed slots**体系。

### 从全注意力到线性复杂度的统一块替换

在基线架构**PyramidFlow**（Jin et al., arXiv 2024）中，视频生成模型由8个MM-DiT块和16个统一Transformer块堆叠而成。M4V保留前8个MM-DiT块不变，将后续16个统一块全部替换为MM-DiM块（Section 3.2）。这一替换带来了计算复杂度的质变：全序列注意力复杂度为 $\mathcal{O}((T M)^2)$，而MM-DiM块的总复杂度降至 $\mathcal{O}(T M + T^2)$，其中 $\mathcal{O}(T M)$ 来自SSM的线性扫描，$\mathcal{O}(T^2)$ 来自轻量时序分支的因果注意力（Section 4.2）。在768p分辨率下，MM-DiM块的混合器层计算量仅为29.52 TFLOPs，相比全注意力基线的55.44 TFLOPs**降低约46.7%**（Table 4）。

### 双向令牌重组：弥补Mamba的跨模态盲区

Transformer通过QKV注意力自然地实现文本与视觉令牌的交互，而Mamba的SSM本质上是一个单向序列模型，缺乏这种跨模态感知能力。M4V的**MM-Token Re-Composition**策略通过巧妙的序列编排解决了这一问题：将文本令牌同时放置在序列的起始和末尾，且前置文本令牌采用左侧零填充（$Z_l = [\emptyset, Z]$），使得视觉令牌在SSM扫描过程中逐步“看到”文本上下文，同时末尾的文本令牌也能吸收视觉信息，形成双向信息流（Section 3.3, Figure 2(c)）。消融实验证实，这一设计显著提升了Overall Consistency指标，直接改善了文本-视频对齐质量（Table 3）。

### Zigzag空间扫描与逐帧寄存器：3D视频潜变量的结构化感知

视频潜变量是3D张量，而Mamba处理的是1D序列。M4V采用**zigzag多路径空间扫描**策略（8种不同扫描路径交替使用），并结合**逐帧寄存器（Per-Frame Registers）**来指示帧边界和分辨率变化，使SSM能够有效捕获空间结构信息（Section 3.3）。消融实验表明，加入逐帧寄存器后，所有视频质量指标均获提升，验证了其在帮助Mamba感知时空依赖方面的关键作用（Table 3）。

### 轻量时序分支：SSM与注意力的互补融合

尽管SSM具备一定的序列建模能力，但在长程时序依赖上仍弱于注意力机制。M4V在每个MM-DiM块中并行嵌入一个**轻量时序分支**：先对条件帧进行空间下采样，再沿时间维度执行因果注意力（Section 3.3, Figure 2(b)）。这一设计以极小的计算代价（$\mathcal{O}(T^2)$，仅与帧数相关）弥补了SSM的时序建模短板。消融实验中，加入时序分支后所有指标进一步提升，且“Full + Temp-Branch”变体以更低计算成本取得了最佳平均得分58.75，充分体现了SSM与注意力的互补性（Table 3, Table 4）。

### 训练后奖励学习：轻量级质量增强

作为补充创新，M4V引入训练后**奖励学习**策略：对每一帧执行一步去噪得到预测干净帧 $\hat{x}_1^i$，解码后使用HPSv2和CLIP两个奖励模型计算损失 $\mathcal{L}_{\mathrm{reward}} = - r_1(D(\hat{x}_1^i)) - r_2(D(\hat{x}_1^i))$ 并反向传播（Section 3.4, Eq. 5-6）。该策略在VBench上带来0.16%的Total Score提升，结合合成数据增强后进一步提升至81.91（Table 5）。

### 创新边界与待验证空间

当前设计的替换范围限于后16个统一块，前8个MM-DiT块仍保留Transformer结构。是否可将MM-DiM推广至全架构、在更大规模公开数据集上的效率优势能否持续、以及能否引入视频级奖励模型，均为论文明确指出的开放问题。此外，训练依赖大规模预训练权重初始化，且使用了包含专有数据的混合数据集，可能影响完全公开条件下的复现性。

## 整体框架

M4V 的整体生成架构遵循“先多模态融合，后高效扩散建模”的宏观设计。如图 2(a) 所示，模型前端保留 8 个 **MM-DiT 块**（来自 FLUX），它们拥有独立的文本与视觉参数，负责初始的文本-视觉深度交互。在此之后，所有后续的 16 个统一块被替换为本文提出的 **多模态扩散 Mamba（MM-DiM）块**，这是整个框架效率瓶颈突破的核心所在。

### 输入输出流

1. **文本编码**：输入文本通过预训练语言模型编码为文本令牌序列 $Z$。
2. **视觉潜变量生成**：视觉部分以噪声潜变量 $x_t^i$ 作为起点，在流匹配（Flow Matching）框架下逐步去噪。对于 PyramidFlow 基线，当前帧的生成条件由前序帧的多级压缩潜变量构建（式 4），形成自回归条件序列。
3. **多模态序列组装**：在进入 MM-DiM 块之前，文本令牌 $Z$ 与视觉令牌 $X_v$ 被拼接为统一序列 $X \equiv [Z, X_v]$，随后送入 Mamba 的 SSM 扫描管线。

### MM-DiM 块内部流程

每个 MM-DiM 块解决两个关键挑战：**多模态交互** 和 **3D 视频潜变量的空间-时间排列**。其内部流程如下：

- **MM-Token 重组（MM-Token Re-Composition）**：将文本令牌分别放置于序列的起始和末尾。前置文本令牌经过左侧零填充（$Z_l = [\emptyset, Z]$），使视觉令牌在 SSM 扫描中逐令牌地累积文本上下文；后置文本令牌则使文本令牌也能吸收视觉信息，实现双向信息流。
- **多路径 Zigzag 空间扫描**：对 2D 空间潜变量采用 8 种不同路径交替的 zigzag 扫描策略，将空间结构展开为 1D 序列，同时插入**逐帧寄存器（Per-Frame Registers）**以指示帧边界和分辨率变化，帮助 Mamba 感知空间-时间依赖。
- **SSM 扫描与逆重组**：经过重组的序列通过 Mamba 的线性复杂度 SSM 核心进行状态空间建模，随后执行逆重组恢复原始令牌顺序。
- **轻量时序分支（Temporal Branch）**：与主 SSM 分支并行，对条件帧进行空间下采样后，沿时间维度施加因果注意力，以捕获长程帧间依赖，弥补 SSM 在显式时序建模上的不足。

### 训练后优化

在训练完成后，M4V 引入了一个可选的**奖励学习（Reward Learning）**阶段：对每一帧执行一步去噪预测干净潜变量 $\hat{x}_1^i$，将其解码后由 HPSv2 和 CLIP 奖励模型评估，计算奖励损失 $\mathcal{L}_{\mathrm{reward}}$ 并反向传播，进一步提升生成质量。

### 模块关系总结

整个 pipeline 可概括为：**文本编码 → MM-DiT 初始融合 → MM-DiM 高效扩散建模（含令牌重组、SSM 扫描、时序分支）→ 流匹配解码 → 奖励学习后优化**。这种设计将 Transformer 的二次复杂度 $O((TM)^2)$ 降至 MM-DiM 的 $O(TM + T^2)$，在保持多模态交互能力的同时实现了显著的效率提升。

### 补充图表

![[assets/figures/papers/paper_list_l2222_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_M4V_Multimodal_M/figures/002_Figure_2.jpg]]
*Figure 2: (a) Overview of the generation architecture. (b) Detailed strcture of our MM-DiM Block*

## 核心模块与公式推导

### 3.1 状态空间模型基础

M4V 的核心计算单元建立在状态空间模型（State Space Model, SSM）之上。连续时间线性系统可表示为：

$$h'(\tau) = \mathbf{A} h(\tau) + \mathbf{B} x(\tau), \quad y(\tau) = \mathbf{C} h(\tau) + \mathbf{D} x(\tau)$$

其中 $h(\tau)$ 为隐状态，$x(\tau)$ 为输入信号，$y(\tau)$ 为输出。为适配离散序列处理，引入时间采样参数 $\Delta$ 对连续参数进行离散化：

$$\overline{\mathbf{A}} = \exp(\Delta \mathbf{A}), \quad \overline{\mathbf{B}} = (\Delta \mathbf{A})^{-1} [\exp(\Delta \mathbf{A}) - \mathbf{I}] \Delta \mathbf{B}$$

离散化后的递归更新与输出计算为：

$$h^{\tau} = \overline{\mathbf{A}} h^{\tau-1} + \overline{\mathbf{B}} x^{\tau}, \quad y^{\tau} = \mathbf{C} h^{\tau} + \mathbf{D} x^{\tau}$$

Mamba 的核心改进在于使参数 $\mathbf{A}$、$\mathbf{B}$、$\mathbf{C}$、$\Delta$ 依赖于输入，从而突破线性时不变系统的容量限制，在保持线性复杂度的同时获得更强的序列建模能力。

### 3.2 多模态扩散 Mamba（MM-DiM）块

**设计动机。** 视频扩散模型中的统一 Transformer 块依赖全序列自注意力，其计算复杂度为 $\mathcal{O}((T M)^2)$，其中 $T$ 为帧数，$M$ 为每帧序列长度。当生成高分辨率长视频时，该二次复杂度成为严重瓶颈。

**架构替换策略。** M4V 保留前 8 个 MM-DiT 块（源自 FLUX，拥有独立文本与视觉参数）不变，将后续 16 个统一 Transformer 块全部替换为 MM-DiM 块。MM-DiM 块需解决两个关键挑战：（1）实现视觉令牌与文本令牌之间的有效跨模态交互；（2）将 3D 视频潜变量合理排列以适配 Mamba 的 1D 扫描特性。

**总体复杂度。** MM-DiM 块的总体计算复杂度为：

$$\mathcal{O}(T M + T^2)$$

其中 $\mathcal{O}(T M)$ 来自 SSM 扫描的线性复杂度，$\mathcal{O}(T^2)$ 来自轻量时序分支的因果注意力。相比全注意力方案的 $\mathcal{O}((T M)^2)$，该设计在理论上实现了数量级缩减。

### 3.3 多模态令牌重组（MM-Token Re-Composition）

**输入序列构造。** 输入序列由文本令牌 $Z$ 和视觉令牌 $X_v$ 拼接而成：

$$X \equiv [Z, X_v]$$

为实现双向信息流，文本令牌被复制并分别放置在序列两端。前置文本令牌采用左侧零填充：

$$Z_l = [\emptyset, Z]$$

使得视觉令牌在 SSM 扫描过程中逐步感知文本上下文；后置文本令牌则使文本令牌能够吸收视觉信息，弥补 Mamba 单向扫描缺乏显式跨模态交互的缺陷。

**Zigzag 空间扫描与逐帧寄存器。** 视觉令牌采用多路径 Zigzag 扫描策略（8 种不同路径交替使用），将 2D 空间特征重新排列为适合 SSM 处理的 1D 序列。同时，在每个视觉令牌序列中插入逐帧可学习寄存器（Per-Frame Registers），用于指示帧边界与分辨率变化，帮助 Mamba 捕获时空依赖性。

### 3.4 轻量时序分支

在每个 MM-DiM 块中，与主 SSM 分支并行设置一个轻量时序分支。该分支首先对条件帧进行空间下采样，随后沿时间维度执行因果注意力，专门捕获帧间长程时序依赖。时序分支的注意力复杂度仅为 $\mathcal{O}(T^2)$，与每帧令牌数 $M$ 无关，因此计算开销极小。

### 3.5 奖励学习

**一步去噪预测。** 在流匹配框架下，从含噪潜变量 $x_t^i$ 和预测速度 $\hat{v}^i$ 中一步估计干净潜变量：

$$\hat{x}_1^i = \frac{1}{\sigma_e} \Bigl( x_t^i + \frac{\sigma_e - \sigma_t}{\sigma_e - \sigma_s} \hat{v}^i - (1 - \sigma_e) x_0^i \Bigr)$$

**奖励损失。** 对解码后的预测干净帧 $D(\hat{x}_1^i)$，使用 HPSv2 和 CLIP 两个奖励模型进行评估并计算损失：

$$\mathcal{L}_{\mathrm{reward}} = - r_1(D(\hat{x}_1^i)) - r_2(D(\hat{x}_1^i))$$

该损失在训练后对每一帧进行一步去噪并反向传播，以提升生成质量。

### 3.6 PyramidFlow 自回归条件

M4V 沿用了 PyramidFlow 的自回归生成范式，利用前序帧的多级压缩潜变量构建当前帧的生成条件：

$$\boldsymbol{c}^i = [K_{\downarrow_2}(x^0), \ldots, K_{\downarrow_2}(x^{i-3}), K_{\downarrow_1}(x^{i-2}), x^{i-1}]$$

其中 $K_{\downarrow_1}$ 和 $K_{\downarrow_2}$ 分别表示不同级别的空间压缩操作。

### 补充图表

![[assets/figures/papers/paper_list_l2222_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_M4V_Multimodal_M/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of FLOPS between full attention baseline and ours*

## 实验与分析

### 核心定量结果：VBench 基准

M4V 在两个不同基座架构上均取得了公开数据训练模型中的最佳成绩。如 **Table 1** 所示，M4V (PyramidFlow) 在 VBench 上获得 **81.55** 的总分，而 M4V (Wan2.1) 进一步提升至 **86.14**。这一结果验证了 MM-DiM 块设计的跨架构泛化能力——无论是基于流匹配的 PyramidFlow 还是 Wan2.1，替换统一 Transformer 块后均能维持甚至超越原有生成质量。

![[assets/figures/papers/paper_list_l2222_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_M4V_Multimodal_M/figures/003_Table_1.jpg]]
*Table 1: Benchmark results on VBench [23]. The best results among models trained on public data are marked in bold. †: Reproduced results using official code and the same training data as in our experiments. *: Models that are initialized (or partially initialized) from public models*

**Table 1** 同时列出了多个对比模型，包括 CogVideoX、HunyuanVideo、T2V-Turbo 等。其中标注 † 的结果为使用官方代码与本文相同训练数据复现的版本，标注 * 的模型为从公开模型初始化（或部分初始化）的版本。M4V 的两个变体在所有仅使用公开数据训练的模型中均以粗体标记为最优，表明其在文本-视频对齐、运动平滑度、美学质量等多个维度上具有综合优势。

### 计算效率分析

效率是 M4V 的核心设计目标。**Table 4** 给出了在 768p 分辨率、241 帧条件下，不同架构设计的混合器层（注意力或 Mamba）计算量对比：

![[assets/figures/papers/paper_list_l2222_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_M4V_Multimodal_M/figures/007_Table_4.jpg]]
*Table 4: Computational analysis of architectural designs. TFLOPs are calculated for mixer layers, i.e., attention or Mamba. Both TFLOPs and inference time are estimated at 768p resolution, on a single NVIDIA A100 GPU*

- **全注意力基线**：55.44 TFLOPs
- **Full + Temp-Branch（最终方案）**：29.52 TFLOPs，**降低 46.7%**

这一结果与摘要中宣称的“768×1280 分辨率下减少 45% FLOPs”高度吻合。**Figure 1** 进一步以可视化方式对比了全注意力基线与 M4V 在不同分辨率下的 FLOPs 增长曲线，直观展示了 Mamba 线性复杂度带来的可扩展性优势。

从复杂度公式角度，全序列注意力的计算量为 $\mathcal{O}((T M)^2)$，其中 $T$ 为帧数，$M$ 为每帧序列长度；而 MM-DiM 的总复杂度为 $\mathcal{O}(T M + T^2)$——SSM 部分贡献 $\mathcal{O}(T M)$ 的线性项，轻量时序分支贡献 $\mathcal{O}(T^2)$ 的帧间注意力项。当 $M$ 随分辨率增大时，线性项的优势愈发显著。

**Table 2** 提供了端到端生成速度对比，展示了不同模型在具体视频尺寸下的推理耗时。M4V 在保持生成质量的同时实现了更快的推理速度，这对于实际部署场景至关重要。

### 消融实验：架构设计的逐项验证

**Table 3** 通过快速评估协议对模型架构进行了系统性消融，揭示了三个关键设计各自的贡献：

#### 文本令牌重组（Text Token Re-Composition）
启用文本令牌重组后，**Overall Consistency 指标显著提升**，这是衡量文本-视频对齐的核心指标。该设计通过在序列首尾两次放置文本令牌（前置令牌含左侧零填充），使视觉令牌在 SSM 扫描过程中逐步感知文本上下文，同时后置文本令牌也能吸收视觉信息，弥补了 Mamba 缺乏显式跨模态注意力交互的固有缺陷。

#### 逐帧寄存器（Per-Frame Registers）
将逐帧寄存器引入视觉序列后，**所有视频质量指标均获得提升**。这些可学习的帧边界标记帮助 Mamba 感知帧间边界与分辨率变化，配合 zigzag 多路径空间扫描策略（8 种不同路径交替使用），有效捕获了时空依赖性。

#### 轻量时序分支（Temporal Branch）
在 MM-DiM 块中加入并行的轻量因果注意力模块后，**所有指标进一步提升**。该分支先对条件帧进行空间下采样，再沿时间维度执行因果注意力，专门捕获长程帧间依赖。这一结果表明 SSM 与注意力机制在时序建模上具有互补性。

**Table 4** 的消融进一步揭示了效率与性能的权衡：
- **Full + Temp-Branch** 在降低计算成本的同时获得最佳平均得分（Avg. Score **58.75**），是效率-性能的最优平衡点
- **Parallel** 变体虽获得最高平均得分（59.97），但计算成本也最高
- 这验证了论文的设计选择：以可控的计算开销换取时序建模能力的显著增强

### 训练后优化：奖励学习

**Table 5** 展示了训练改进策略的消融结果。奖励学习（Reward Learning）模块在训练后对每一帧进行一步去噪预测，利用 HPSv2 和 CLIP 两个奖励模型对解码后的预测干净帧计算损失并反向传播：

$$\mathcal{L}_{\mathrm{reward}} = - r_1(D(\hat{x}_1^i)) - r_2(D(\hat{x}_1^i))$$

单独使用奖励学习在 VBench 上带来 **0.16%** 的 Total Score 提升。当结合合成数据增强（使用 HunyuanVideo 生成额外训练数据）时，Total Score 进一步提升至 **81.91**。**Figure 5** 提供了奖励学习的可视化效果对比，直观展示了该策略对生成质量的改善。

![[assets/figures/papers/paper_list_l2222_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_M4V_Multimodal_M/figures/010_Figure_5.jpg]]
*Figure 5: Visual analysis of reward learning*

### 用户偏好研究

**Figure 3** 展示了用户研究结果，将 M4V 与 T2V-Turbo、CogVideoX、HunyuanVideo 和 PyramidFlow 进行对比。M4V 在用户偏好中取得了具有竞争力的结果，进一步验证了其生成质量在实际人眼评估中的表现。

### 已知局限与待验证方向

尽管实验证据充分，以下局限需要在解读结果时注意：

1. **架构替换范围有限**：当前设计仅替换了后 16 个统一块，前 8 个 MM-DiT 块仍沿用 Transformer 结构。全 Mamba 架构的潜力尚未被探索。

2. **训练数据依赖性**：训练依赖大规模预训练权重初始化，且使用了包含专有数据的混合数据集（约 1000 万单镜头视频片段及图像数据集），这可能影响完全公开设置下的复现性。

3. **奖励学习的局限**：奖励学习仅在有限步骤下进行，且仅使用了两种图像级奖励模型（HPSv2 和 CLIP），对视频整体质量的影响可能有限。能否引入视频级别的奖励模型（如 VBench 评估器本身）是值得探索的方向。

4. **超长视频场景未验证**：Mamba 的线性复杂度理论上在超长视频（>1000 帧）生成中应带来显著的吞吐量优势，但当前实验主要在 241 帧条件下进行，该假设需要进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l2222_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_M4V_Multimodal_M/figures/004_Table_2.jpg]]
*Table 2: Generation speed comparison across models*

![[assets/figures/papers/paper_list_l2222_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_M4V_Multimodal_M/figures/005_Figure_3.jpg]]
*Figure 3: User study between Ours, T2V-Turbo, CogvideoX, HunyanVideo and Pyramidflow*

![[assets/figures/papers/paper_list_l2222_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_M4V_Multimodal_M/figures/006_Table_3.jpg]]
*Table 3: Ablation study of the model architecture using the proposed fast evaluation protocol. Text: Enables bi-directional information aggregation through text token re-composition. Vis: Adds per-frame registers within the visual sequence. Temp: Incorporates a temporal branch within each block. Overall-Con measures the consistency between the generated video and the input text, while the other metrics assess different aspects of video quality. Significant metric changes with Text and Vis are highlighted for clarity*

![[assets/figures/papers/paper_list_l2222_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_M4V_Multimodal_M/figures/009_Table_5.jpg]]
*Table 5: Ablation study of training improvements on official VBench [23]*

![[assets/figures/papers/paper_list_l2222_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_M4V_Multimodal_M/figures/008_Figure.jpg]]
*Figure: (a) A stylish woman walks down the streets of Tokyo, surrounded by warm neon lights and vibrant city signs. She wears a black leather jacket, ... (b) A futuristic cityscape at dusk, with flying cars zipping between towering skyscrapers adorned with neon lights. (c) A determined individual in a sleek, black athletic outfit jogs along a winding forest trail, surrounded by towering trees and*

## 方法谱系与知识库定位

### 1. 对Transformer视频扩散路线的继承与替换

M4V的方法论根植于**基于流匹配的Transformer视频扩散模型**，直接继承了两个代表性基线架构的宏观设计：

- **PyramidFlow**（Jin et al., arXiv 2024）：采用FLUX的MM-DiT块作为初始多模态处理层，随后堆叠统一的自注意力Transformer块，并通过金字塔式流匹配实现自回归视频生成。M4V保留了其前8个MM-DiT块不变，仅将后续16个统一Transformer块替换为MM-DiM块，同时沿用了其自回归条件构建公式（Eq. 4）和流匹配框架。
- **Wan2.1**（Wang et al., arXiv 2025）：作为另一个验证泛化性的基线，M4V同样将其后半部分Transformer块替换为MM-DiM块，证明了该替换策略的跨架构适用性。

这种“保留前端多模态Transformer + 替换后端统一块”的策略，本质上是在**利用预训练权重初始化**与**引入线性复杂度序列建模**之间寻求平衡。论文明确指出现有Mamba视频模型（如VideoMamba）仅能处理简单生成任务，而M4V通过MM-DiM块的设计首次使Mamba能够胜任复杂文本生成视频任务。

### 2. 与Mamba视频理解/生成工作的关系

M4V处于**Mamba架构向视频扩散模型迁移**的技术路线上，其核心贡献在于解决了两个此前阻碍Mamba应用于复杂T2V生成的关键瓶颈：

| 瓶颈 | 现有Mamba方案的局限 | M4V的解决方案 |
|------|---------------------|---------------|
| 多模态交互 | Mamba缺乏显式跨模态注意力机制，文本与视觉令牌间信息流受限 | 双向令牌重组：文本令牌前置（含左侧零填充）使视觉令牌逐步感知文本上下文，后置使文本令牌吸收视觉信息 |
| 3D视频潜变量排列 | 简单平展的1D序列丢失空间与时间结构 | Zigzag多路径空间扫描 + 逐帧可学习寄存器指示帧边界与分辨率变化 |

在空间扫描策略上，M4V采用了Hu et al. 提出的zigzag扫描方案，但将其扩展为8种不同路径交替使用，并结合逐帧寄存器增强了Mamba对时空依赖的感知能力。这一设计使Mamba的线性复杂度优势得以在视频扩散模型中兑现：SSM部分的复杂度为$O(T M)$，远低于全序列注意力的$\mathcal{O}((T M)^2)$。

### 3. 时序建模的混合架构定位

M4V的时序分支设计体现了**SSM与注意力机制的互补性**认知。论文通过消融实验表明：

- 纯Mamba方案（Full Mamba）虽计算成本最低（29.52 TFLOPs），但视频质量指标和总体得分低于加入时序注意力的变体；
- 加入轻量时序因果注意力分支（Full + Temp-Branch）在几乎不增加计算开销的前提下，将Avg. Score从纯Mamba的57.63提升至58.75；
- 并行注意力方案（Parallel）虽然性能最高（Avg. Score 59.97），但计算成本也最高（55.44 TFLOPs）。

这表明**时序维度的长程依赖仍然受益于注意力机制的显式建模**，而空间维度则可以通过Mamba的线性扫描高效处理。这种“空间SSM + 时序注意力”的混合架构，与VideoMamba等在理解任务中将SSM应用于时空两个维度的做法形成对比，值得进一步探索统一方案的可能性。

### 4. 训练后优化策略的定位

M4V引入了基于奖励学习的训练后优化策略，使用HPSv2和CLIP两个图像级奖励模型对每一帧进行一步去噪预测并计算奖励损失（Eq. 6）。这一策略在VBench上带来0.16%的Total Score提升（Table 5），结合合成数据增强后进一步提升至81.91。

与基于RLHF的视频生成优化方法（如InstructVideo）相比，M4V的奖励学习更为轻量（仅使用图像级奖励模型、有限步骤优化），避免了复杂的视频级偏好标注。但其局限性也在于此：**仅使用图像奖励模型可能无法充分捕获视频级别的时序一致性和运动质量**。论文在开放问题中也指出，将视频级别的奖励模型（如VBench评估器）纳入框架是未来的改进方向。

### 5. 适用边界与局限

**适用边界**：
- 当前设计仅适用于**基于流匹配的自回归视频扩散框架**，对DDPM等其他扩散范式的迁移需要额外适配；
- 训练依赖大规模预训练权重初始化，且使用了包含专有数据的混合数据集（约10M单镜头视频片段），**完全公开数据下的复现性可能受限**；
- 前8个MM-DiT块仍沿用Transformer结构，尚未探索全Mamba架构的潜力。

**已知局限**（论文明确承认）：
1. 仅替换了后半部分统一块，全Mamba架构的潜力未被充分探索；
2. 奖励学习仅在有限步骤下进行，且仅使用两种图像奖励模型，对视频整体质量的影响可能有限；
3. 训练数据包含专有数据，可能影响完全公开下的复现性。

### 6. 开放问题与未来方向

基于论文的讨论和当前技术脉络，以下开放问题值得关注：

1. **全Mamba架构探索**：是否可以将MM-DiM块推广到所有层，包括初始的MM-DiT块？这需要解决Mamba在早期多模态融合中的有效性验证问题。
2. **规模化训练验证**：在更大规模公开视频数据集上训练时，M4V的效率优势能否保持并继续提升质量？当前81.55/86.14的VBench总分仍有提升空间。
3. **视频级奖励模型集成**：能否将VBench评估器或其他视频级质量模型纳入奖励学习框架，以直接优化时序一致性和运动质量？
4. **超长视频生成**：Mamba的线性复杂度$\mathcal{O}(T M + T^2)$是否在超长视频（>1000帧）生成中带来显著的吞吐量优势？此时时序注意力的$\mathcal{O}(T^2)$项可能成为新瓶颈。
5. **与其他高效架构的对比**：M4V与基于线性注意力、稀疏注意力或状态空间对偶（如Mamba-2）的视频扩散模型之间的效率-质量权衡尚未被系统比较。

## 原文 PDF

![[paperPDFs/CVPR_2026/M4V_Multimodal_Mamba_for_Efficient_Text_to_Video_Generation.pdf]]