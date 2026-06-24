---
title: "GeoTikzBridge: Advancing Multimodal Code Generation for Geometric Perception and Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GeoTikzBridge_Advancing_Multimodal_Code_Generation_for_Geometric_Perception_and_Reasoning.pdf
project_link: null
code_link: null
aliases:
- GeoTikzBridge
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将几何图像转换为结构化的TikZ代码作为显式符号中间表示，从而用文本编码的几何元素与关系弥补视觉感知不足，并为下游推理提供精确的几何信息。
primary_logic: 通过迭代自优化数据扩展与局部代码变换策略，构建当前最大规模（2.5M对）的图像到TikZ数据集，并训练专门模型将几何视觉信息转化为高质量、可编译的TikZ代码；该代码可作为即插即用的推理模块，显著增强各类视觉/语言大模型的几何问题求解性能。
claims:
- GeoTikzBridge-Base在图像到TikZ任务上取得SOTA：在MathVista-GPS上CLIP-Score 0.915、FID 30.6，显著优于现有方法。
- 将GeoTikzBridge-Base生成的TikZ代码接入推理模型，在MathVista-GPS上使InternVL3.5-38B的准确率从0.688提升至0.718，GPT-5.0从0.891提升至0.937。
- 添加辅助线（无论以渲染图像或TikZ代码形式）均有助于几何问题求解，且TikZ代码比纯图像更有效，最高准确率达0.736（Table 4）。
- 局部代码变换策略使代码重复预测率下降15%，并在CLIP分数和编译成功率上带来显著增益（Figure 5）。
---

# GeoTikzBridge: Advancing Multimodal Code Generation for Geometric Perception and Reasoning

> [!tip] 核心洞察
> 通过迭代自优化数据扩展与局部代码变换策略，构建当前最大规模（2.5M对）的图像到TikZ数据集，并训练专门模型将几何视觉信息转化为高质量、可编译的TikZ代码；该代码可作为即插即用的推理模块，显著增强各类视觉/语言大模型的几何问题求解性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | GeoTikzBridge：推进面向几何感知与推理的多模态代码生成 |
| 英文题名 | GeoTikzBridge: Advancing Multimodal Code Generation for Geometric Perception and Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.22687) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | GeoTikzBridge |
| Dataset | DaTikZ, MathVista-GPS, GeoTikz-Instruct |

> [!tip] 效果简介
> - DaTikZ 上，CSR (编译成功率) 95.1% vs 86.7% (FigCodifier-8B) (+8.4%)。
> - MathVista-GPS 上，CLIP-Score 0.915 vs 0.884 (FigCodifier-8B) (+0.031)；FID 30.6 vs 42.5 (FigCodifier-8B) (-11.9)；几何推理准确率 (VLM InternVL3.5-38B) 0.718 (Base模型版本) vs 0.688 (未使用TikZ的InternVL3.5-38B) (+0.030)。
> - GeoTikz-Instruct (辅助线生成) 上，MSE 211.7 vs 1435.9 (FigCodifier) (-1224.2)。

## 概述

多模态大语言模型（MLLMs）在几何感知与推理中面临一个根本瓶颈：视觉编码器难以精准捕获线段关系、角度大小、形状约束等细粒度几何结构，而大规模几何图像-代码配对数据的匮乏进一步制约了模型对几何语义的深层理解。**GeoTikzBridge** 针对这一瓶颈，提出将几何图像转化为结构化的 **TikZ 代码** 作为显式符号中间表示——用文本编码的几何元素与关系弥补视觉感知的不足，并为下游推理提供精确、可编译的几何信息。

方法的核心机制在于**迭代自优化数据扩展**与**局部代码变换策略**：从一个约 145k 的高质量种子集（DaTikZ）出发，通过模型自生成、CLIP 分数过滤与代码行随机删除（最多 40%）等变换，逐步构建出当前最大规模的 2.5M 图像-TikZ 配对数据集 **GeoTikz-Base**，并同步训练图像到 TikZ 的专用模型 **GeoTikzBridge-Base**。在此基础上，进一步构建指令驱动的辅助线生成数据集 **GeoTikz-Instruct**，微调得到 **GeoTikzBridge-Instruct**，使模型能根据自然语言指令生成包含辅助线的 TikZ 代码。最终，这些模型作为即插即用的推理模块，将生成的 TikZ 代码（及可选的辅助线图像/代码）注入视觉/语言大模型，无需额外训练即可显著提升几何问题求解性能。

实验证据表明：GeoTikzBridge-Base 在图像到 TikZ 任务上取得 SOTA，MathVista-GPS 上 CLIP-Score 达 0.915、FID 降至 30.6，显著优于 FigCodifier-8B 等基线（Table 1）。在下游推理中，将生成的 TikZ 代码接入 InternVL3.5-38B 使准确率从 0.688 提升至 0.718，接入 GPT-5.0 则从 0.891 提升至 0.937（Table 2, Table S8）。消融实验进一步证实，TikZ 代码作为几何表示优于自然语言描述，且代码变换策略使重复预测率下降 15%，带来 CLIP 分数与编译成功率的显著增益（Figure 4, Figure 5）。辅助线生成方面，GeoTikzBridge-Instruct 的 MSE 低至 211.7，远优于 FigCodifier 的 1435.9（Table 3）；将辅助线图像与 TikZ 代码协同输入时，解题准确率最高可达 0.736（Table 4）。

综上，GeoTikzBridge 通过“视觉→符号代码→推理”的路径，以数据驱动的方式系统性地缓解了 MLLMs 在局部几何感知上的短板，为几何视觉推理提供了一个可扩展、免训练的增强范式。

## 背景与动机

### 多模态大模型的几何感知瓶颈

多模态大语言模型（MLLMs）在自然图像理解与高层语义推理上取得了长足进步，但在**局部几何感知**层面仍存在显著瓶颈。具体表现为：模型难以精准解析线段之间的平行、垂直、相交关系，无法可靠判断角度大小与形状约束，对细粒度几何结构的空间理解能力不足。这一问题在几何问题求解场景中尤为突出——当模型面对包含复杂辅助线、嵌套三角形或多边形组合的几何图形时，纯视觉编码往往丢失关键的拓扑与度量信息，导致后续推理链条从起点就发生偏差。

### 现有方法的缺口

当前缓解上述瓶颈的路径主要有两条，但各自存在局限：

1. **端到端视觉推理增强**：通过扩大模型参数量或引入视觉指令微调来提升几何理解能力。然而，这类方法本质上仍依赖视觉编码器对像素级几何关系的隐式建模，缺乏对几何元素（点、线、角、形）的显式结构化表征，导致在需要精确度量比较或逻辑推导的任务上表现不稳定。

2. **图像到代码生成**：将几何图像转换为TikZ等图形描述语言，以文本形式编码几何结构。已有工作如**FigCodifier-8B**初步探索了这一方向，但受限于训练数据规模（约145k对）和缺乏对局部几何细节的专门建模，生成的代码在编译成功率和视觉还原度上仍有较大提升空间。

更为根本的缺口在于：**缺乏大规模、高质量的几何图像-代码配对数据**。TikZ代码的标注成本极高，人工标注难以规模化，这直接制约了图像到TikZ模型的性能上限。

### 本文动机

基于上述分析，本文的核心动机可概括为三个层面：

- **感知层面**：将几何图像转换为结构化的TikZ代码，作为显式的符号中间表示。TikZ代码以文本形式精确编码几何元素的坐标、关系和样式，能够弥补纯视觉感知在细粒度几何结构上的不足。

- **数据层面**：通过迭代自优化策略，从有限的种子数据集出发，逐步扩展构建大规模图像-TikZ配对数据，打破标注瓶颈。

- **推理层面**：将生成的TikZ代码作为即插即用的推理模块，为下游视觉/语言大模型提供精确的几何信息，从而在不修改推理模型本身的前提下，显著提升几何问题求解性能。

## 核心创新

GeoTikzBridge 的核心创新在于将几何图像的视觉感知问题转化为结构化代码生成问题，并通过**迭代自优化数据扩展**与**局部代码变换策略**构建了当前最大规模的图像到TikZ数据集（2.5M对），训练出专门的代码生成模型，使其作为即插即用的推理模块显著增强多模态大语言模型的几何问题求解能力。以下从四个关键维度展开：

### 1. 大规模迭代自优化数据集构建

现有图像到TikZ生成方法受限于训练数据规模（如DaTikZ种子集约145k对），难以覆盖多样化的几何图形和细粒度结构。GeoTikzBridge 提出迭代自优化框架，将数据规模从约145k扩展至2.5M对（Figure 3）：

- **自优化集筛选**：在第k轮迭代中，模型M_k对输入图像I生成TikZ代码Ĉ，经渲染得到Î后，计算CLIP分数s(I, Î)；仅当分数超过阈值τ时，该样本才被纳入自优化集D_k^R（Eq. 2）。这一机制确保了扩展数据的语义保真度。
- **变换增强集生成**：对自优化集中的代码应用局部变换策略（见下文），将编译通过的变体及其渲染图像作为增强样本D_k^T（Eq. 3）。
- **数据集合并与模型迭代**：D_k = D_{k-1} ∪ D_{k-1}^R ∪ D_{k-1}^T，在此基础上优化模型M_k（Eq. 1），最大迭代轮数K=4。

这一框架使数据规模实现了约17倍的增长，为模型提供了丰富的几何结构覆盖，是后续性能提升的基础。

### 2. 局部几何变换策略

论文观察到一个关键瓶颈：复杂图像常导致模型忽略细粒度几何细节（如线段关系、角度大小），且模型倾向于机械重复已有代码模式。为此提出**局部代码变换策略**：

- **代码层面**：对TikZ代码随机删除不超过40%的行，强制模型学习从部分代码推断完整几何结构。
- **图像层面**：配套应用透视变换、模糊、扭曲等图像增强，提升模型对几何细节的鲁棒性。

消融实验（Figure 5）表明，该策略将代码重复预测率降低15%，并在CLIP分数和编译成功率上带来显著增益。这一设计直接针对MLLM在局部几何感知上的根本瓶颈，是本工作的关键因果调节变量。

### 3. 指令驱动的辅助线生成

传统图像到TikZ方法仅能重现已有图形，无法根据解题需求主动添加辅助线。GeoTikzBridge 进一步构建了GeoTikz-Instruct数据集，并微调得到GeoTikzBridge-Instruct模型：

- **数据构建**：对GeoTikz-Base样本施加代码变换后，由Qwen2.5-VL-72B标注辅助线添加指令，再经Doubao过滤不可靠标注，最终得到指令-图像-代码三元组D_ins（Eq. 5）。
- **模型训练**：以指令和图像为条件，最大化目标TikZ代码的生成概率（Eq. 6）。

实验显示，GeoTikzBridge-Instruct在辅助线生成任务上的MSE仅为211.7，远低于FigCodifier的1435.9（Table 3），填补了现有方法在主动几何构造能力上的空白。

### 4. 免训练的即插即用推理增强

GeoTikzBridge 的核心设计理念是将代码生成模型作为独立模块，无需对下游VLM/LLM进行任何额外训练：

- **输入形式扩展**：将原始图像+问题文本的输入，扩展为原始图像+问题文本+生成的TikZ代码（及可选辅助线图像/代码）。
- **推理流程**：由VLM分析问题后，GeoTikzBridge-Instruct生成包含辅助线的TikZ代码，渲染为辅助线图像后与原始图像、TikZ代码一同送入推理模型求解（Algorithm 1）。

这一设计使GPT-5.0在MathVista-GPS上的准确率从0.891提升至0.937（Table S8），InternVL3.5-38B从0.688提升至0.718（Table 2），验证了TikZ代码作为符号中间表示在几何推理中的通用增强作用。

## 整体框架

GeoTikzBridge 的整体设计围绕一个核心因果机制展开：**将几何图像的视觉感知转化为结构化的 TikZ 代码，以此作为显式符号中间表示，弥补多模态大语言模型（MLLMs）在局部几何感知上的不足，并为下游推理提供精确的几何信息**。该框架由四个功能模块构成一条免训练的几何视觉推理流水线。

### 1. 迭代自优化数据集构建与模型训练

框架的起点是构建大规模、高质量的图像到 TikZ 数据集 **GeoTikz-Base**。该模块以 DaTikZ 种子集（约 145k 样本）为基础，通过迭代自优化循环逐步扩展数据并同步训练 **GeoTikzBridge-Base** 模型。每轮迭代包含三个步骤：

1. **样本生成与筛选**：当前模型对输入图像生成 TikZ 代码，渲染后计算与原图的 CLIP 分数，超过阈值 τ 的样本被视为可靠，加入自优化集 $\mathcal{D}_k^R$。
2. **局部几何变换增强**：对自优化集中的 TikZ 代码施加代码级变换（随机删除最多 40% 的代码行），将编译通过的变体及其渲染图像作为变换增强集 $\mathcal{D}_k^T$。
3. **模型优化**：将前一轮数据集与自优化集、变换增强集合并，以因果自回归损失 $\mathcal{L}_{\mathrm{gen}}$ 优化模型。

经过 $K=4$ 轮迭代，最终构建出 **2.5M 图像-TikZ 对**的 GeoTikz-Base 数据集，并训练得到 GeoTikzBridge-Base 模型（8B 和 38B 两个版本，分别从 FigCodifier-8B 和 InternVL3.5-38B-Instruct 初始化）。

### 2. 局部几何变换增强

该模块内嵌于数据扩展循环中，是提升模型对细粒度几何结构敏感度的关键设计。研究发现，复杂图像容易使模型忽略局部几何细节，因此引入两类变换：

- **代码变换**：随机删除 TikZ 代码中的若干行（删除比例 < 40%），迫使模型学习更鲁棒的代码-图像映射关系。
- **图像变换**：对渲染图像施加透视变换、模糊、扭曲等增强，进一步提升模型对几何细节的鲁棒性。

消融实验表明，该策略使代码重复预测率下降 15%，并在 CLIP 分数和编译成功率上带来显著增益（Figure 5）。

### 3. 指令驱动辅助线生成

为解决几何问题中常见的辅助线绘制需求，框架在 GeoTikzBridge-Base 基础上构建了指令驱动的辅助线生成能力。具体流程：

1. 对 GeoTikz-Base 样本施加代码变换并重新渲染，得到变体图像。
2. 使用 **Qwen2.5-VL-72B** 为变体图像标注辅助线添加指令，再通过 **Doubao** 过滤不可靠标注，得到指令-图像-代码三元组 $\mathcal{D}_{\mathrm{ins}}$。
3. 以指令和图像为条件，微调 GeoTikzBridge-Base 得到 **GeoTikzBridge-Instruct** 模型，使其能够根据自然语言指令生成包含辅助线的 TikZ 代码。

### 4. 免训练几何视觉推理流水线

这是框架的最终输出层，将 GeoTikzBridge-Base/Instruct 作为**即插即用模块**接入下游 VLM/LLM。如 Algorithm 1 所示，推理流程为：

1. VLM 分析问题图像 $I_p$ 和问题文本 $T_p$，判断是否需要辅助线。
2. 若需要，VLM 生成辅助线指令 $P_{\mathrm{aux}}$，由 GeoTikzBridge-Instruct 生成含辅助线的 TikZ 代码 $C_{\mathrm{aux}}$。
3. 将原始图像、问题文本、生成的 TikZ 代码（及可选的辅助线渲染图像）拼接为统一提示词，送入推理模型求解。

该流水线无需对下游 VLM/LLM 进行任何额外训练。实验表明，将 GeoTikzBridge-Base 生成的 TikZ 代码接入推理模型后，**InternVL3.5-38B** 在 MathVista-GPS 上的准确率从 0.688 提升至 0.718，**GPT-5.0** 从 0.891 提升至 0.937（Table 2, Table S8），验证了 TikZ 作为几何符号表示的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l2510_https_arxiv_org_abs_2603_22687/figures/001_Figure_1.jpg]]
*Figure 1: GeoTikzBridge demonstrates advantages in geometric perception and mathematical reasoning. (1) GeoTikzBridge-Base achieves the most accurate reconstruction of local geometric structures compared to existing approaches. (2) The generated tikz representations enhance MLLMs’ mathematical and visual geometric reasoning*

## 核心模块与公式推导

GeoTikzBridge 的核心由三个递进模块构成：**迭代自优化数据集构建与模型训练**、**指令驱动的辅助线生成**，以及**免训练几何视觉推理流水线**。以下逐一展开其关键公式与机制。

### 迭代自优化数据集构建与模型训练

该模块是 GeoTikzBridge-Base 模型的能力来源，其核心思想是：利用模型自身生成能力筛选高质量样本，并结合局部代码变换策略，逐步扩大训练集规模与多样性。

**迭代更新范式** 在第 $k$ 轮迭代中，数据集 $\mathcal{D}_k$ 由上一轮数据集 $\mathcal{D}_{k-1}$、自优化集 $\mathcal{D}_{k-1}^R$ 和变换增强集 $\mathcal{D}_{k-1}^T$ 合并而成，模型 $M_k$ 在此基础上优化生成损失：

$$
\mathcal{D}_k = \mathcal{D}_{k-1} \cup \mathcal{D}_{k-1}^R \cup \mathcal{D}_{k-1}^T, \quad M_k = \arg\min_{M \mid M_{k-1}} \mathbb{E}_{(I,C)\sim\mathcal{D}_k}[\mathcal{L}_{\mathrm{gen}}(M(I), C)]
$$

**自优化集筛选** 对每个输入图像 $I$，模型 $M_k$ 生成 TikZ 代码 $\hat{C}$，经渲染器 $\mathcal{R}$ 得到渲染图像 $\hat{I}$。仅当 $\hat{I}$ 与原图 $I$ 的 CLIP 相似度 $s(I,\hat{I})$ 超过阈值 $\tau$ 时，该样本才被纳入自优化集：

$$
\mathcal{D}_k^R = \{(\hat{I},\hat{C}) \mid \hat{C}=M_k(I),\,\hat{I}=\mathcal{R}(\hat{C}),\, s(I,\hat{I}) > \tau\}
$$

**变换增强集构造** 对自优化集中的代码 $\hat{C}$ 施加随机删除行（最多 40%）的代码变换 $\mathcal{T}$，仅保留编译通过的变体 $\widetilde{C}$ 及其渲染图像 $\widetilde{I}$：

$$
\mathcal{D}_k^T = \{(\widetilde{I},\widetilde{C}) \mid \widetilde{I}=\mathcal{R}(\widetilde{C}),\,\widetilde{C}=\mathcal{T}(\hat{C}),\,\hat{C}\in\mathcal{D}_k^R\}
$$

该策略迫使模型在训练中学习从残缺代码推断完整几何结构，从而增强对局部几何细节的感知能力。消融实验表明，代码变换使重复预测率下降 15%，并在 CLIP 分数和编译成功率上带来显著增益（Figure 5）。

![[assets/figures/papers/paper_list_l2510_https_arxiv_org_abs_2603_22687/figures/009_Figure_5.jpg]]
*Figure 5: Ablation study of localized geometric transformation strategies for GeoTikzBridge-Base-8B, evaluated on the MathVista-GPS benchmark*

**生成损失** 模型训练采用因果自回归范式，以图像 $I$ 为条件最大化 TikZ 代码序列 $C = \{c_i\}$ 的生成概率：

$$
\mathcal{L}_{\mathrm{gen}}(M(I), C) = -\sum_i \log \mathrm{P}_M(c_i \mid I, c_{<i})
$$

### 指令驱动的辅助线生成

在 GeoTikzBridge-Base 基础上，进一步构建指令数据集 $\mathcal{D}_{\mathrm{ins}}$ 并微调得到 GeoTikzBridge-Instruct 模型，使其能根据自然语言指令生成包含辅助线的 TikZ 代码。

**指令数据集构造** 对 GeoTikz-Base 中的代码 $C_K$ 施加变换 $\mathcal{T}$ 并渲染得到 $\tilde{I}_K$，由 Qwen2.5-VL-72B 标注指令 $Q$，再经 Doubao 过滤不可靠标注，最终得到指令-图像-代码三元组：

$$
\mathcal{D}_{\mathrm{ins}} = \{(Q',\tilde{I}',C') \mid \tilde{I}'=\mathcal{F}(\tilde{I}_K),\,\tilde{I}_K=\mathcal{R}(\mathcal{T}(C_K)),\, Q'=\mathcal{F}(Q),\, C'=\mathcal{F}(C_K)\}
$$

**指令模型优化** 以指令 $Q'$ 和图像 $\tilde{I}'$ 为条件，最大化目标 TikZ 代码 $C'$ 的生成概率：

$$
M_{\mathrm{ins}} = \arg\min_M \mathbb{E}_{(Q',\tilde{I}',C')\sim\mathcal{D}_{\mathrm{ins}}}[\mathcal{L}_{\mathrm{gen}}(M(\tilde{I}',Q'), C')]
$$

该模型在辅助线生成任务上取得 MSE 211.7，远优于 FigCodifier 的 1435.9（Table 3）。

### 免训练几何视觉推理流水线

GeoTikzBridge-Base/Instruct 作为即插即用模块嵌入下游推理：将原始几何图像转换为 TikZ 代码（及可选辅助线代码/图像），与问题文本一同输入 VLM/LLM 进行解题。该流水线无需对推理模型进行任何额外训练，仅通过提示词引入结构化几何信息，即可显著提升推理准确率（Table 2, Table 4）。

## 实验与分析

### 图像到TikZ生成主结果

GeoTikzBridge-Base在图像到TikZ转换任务上全面超越现有方法。**Table 1**汇总了四个基准上的对比结果：在DaTikZ上，GeoTikzBridge-Base-38B的编译成功率（CSR）达到**95.1%**，比FigCodifier-8B的86.7%高出8.4个百分点；在MathVista-GPS上，CLIP-Score达到**0.915**，FID降至**30.6**，分别较FigCodifier-8B提升0.031和降低11.9。8B版本同样表现强劲，在DaTikZ上CSR为92.7%，在MathVista-GPS上CLIP-Score为0.907、FID为34.6，均显著优于所有开源基线（Qwen2.5-VL-32B/72B、InternVL3.5-38B、FigCodifier-8B）。

![[assets/figures/papers/paper_list_l2510_https_arxiv_org_abs_2603_22687/figures/004_Table_1.jpg]]
*Table 1: Performance comparison of image-to-tikz methods across four datasets. The best and second-best results are marked with bold and underlines, respectively*

这些增益的因果链条清晰：**2.5M规模的GeoTikz-Base数据集**（Figure 3）通过迭代自优化框架构建，每轮将自优化集$\mathcal{D}_k^R$（CLIP分数超过阈值$\tau$的可靠生成样本）和变换增强集$\mathcal{D}_k^T$并入训练集，使模型逐步从145k种子数据扩展到大规模高质量配对数据。**局部几何变换策略**（随机删除最多40%的代码行并配套图像增强）迫使模型关注细粒度几何结构，将代码重复预测率降低15%（Figure 5），直接贡献于CLIP分数和编译成功率的提升。

![[assets/figures/papers/paper_list_l2510_https_arxiv_org_abs_2603_22687/figures/003_Figure_3.jpg]]
*Figure 3: Distribution of the 2.5M GeoTikz-Base dataset*

### 下游几何推理增益

将GeoTikzBridge-Base生成的TikZ代码作为即插即用的推理模块接入VLM/LLM，在多个基准上带来一致的准确率提升。**Table 2**显示，在MathVista-GPS上，InternVL3.5-38B的准确率从0.688提升至**0.718**（+0.030）；**Table S8**进一步表明，GPT-5.0的准确率从0.891提升至**0.937**（+0.046）。这一增益源于TikZ代码以结构化符号形式显式编码了几何元素及其空间关系，弥补了MLLM在局部几何感知上的瓶颈——模型无需仅凭视觉猜测线段关系或角度大小，而是可以直接从代码中读取精确的几何约束。

![[assets/figures/papers/paper_list_l2510_https_arxiv_org_abs_2603_22687/figures/005_Table_2.jpg]]
*Table 2: Performance comparison of downstream mathematical reasoning across five benchmarks. The best and second-best results are marked with bold and underlines, respectively*

![[assets/figures/papers/paper_list_l2510_https_arxiv_org_abs_2603_22687/figures/019_Table_S.8.jpg]]
*Table S.8: Mathematical reasoning performance of latest closedsource models on the MathVista-GPS benchmark. Scores are reported as original model / model + GeoTikzBridge-Base-8B*

**Figure 4**的消融实验直接验证了这一机制：以Qwen3-VL-30B-A3B为基线，使用TikZ代码作为几何表示的推理准确率显著高于使用自然语言描述，且GeoTikzBridge-Base生成的TikZ代码优于更大参数量VLM（如Qwen2.5-VL-72B）直接生成的TikZ代码。这说明**专门的图像到TikZ模型比通用VLM更擅长捕捉几何细节**，验证了“专用生成器+通用推理器”的架构合理性。

### 辅助线生成与多模态推理格式

**Table 3**展示了指令驱动辅助线生成的结果：GeoTikzBridge-Instruct在MSE指标上达到**211.7**，而FigCodifier高达1435.9，差距超过1200。**Table 4**进一步揭示了不同推理格式对解题准确率的影响——以InternVL3.5-38B为基线（0.688），仅添加辅助线图像提升至0.720，仅添加TikZ代码提升至0.718，而**同时提供辅助线图像和TikZ代码**达到最高的**0.736**（+0.048）。这表明辅助线的视觉提示与TikZ的符号编码存在互补效应：辅助线图像提供直观的几何构造基础，TikZ代码则精确编码构造后的空间结构，二者协同使推理模型能够准确应用几何定理（如Figure S14中的直角三角形构造案例）。

### 消融与关键设计选择

**迭代轮次与过滤阈值**：Figure S.2和Figure S.3的消融表明，自优化迭代轮次$K=4$和CLIP分数阈值$\tau=0.95$是最优配置。过少的迭代无法充分扩展数据规模，过低的阈值则引入噪声样本，两者均导致性能下降。

**局部变换策略的有效性**：Figure 5直接量化了代码变换策略的贡献——应用随机行删除（≤40%）后，CLIP分数和编译成功率均显著提升，代码重复预测率下降15%。这表明迫使模型从部分代码中恢复完整几何结构，有效增强了对局部细节的感知能力。图像变换增强（透视变换、模糊、扭曲等）进一步提升了模型对视觉扰动的鲁棒性（Section I, Figure S2）。

### 失败模式与局限性

尽管整体表现优异，GeoTikzBridge仍存在明确的失效场景：

1. **长代码截断**：8B模型在处理复杂几何图形时，生成的TikZ代码token长度可能超出限制导致截断，直接引起编译失败或几何信息丢失。这是小参数量模型在复杂场景下的结构性瓶颈。

2. **精细指令执行不足**：Instruct模型在绘制严格平行线等特定指令的生成精度仍有不足，说明指令跟随的细粒度控制尚未完全解决。

3. **领域泛化边界**：当前方法深度依赖LaTeX/TikZ生态，对无法用TikZ清晰表达的图示（如某些工程图表）适应性有限。在立体几何和解析几何等复杂数学领域，单纯依靠TikZ代码增强的推理仍存在失败案例，需要更深入的端到端几何推理范式。

4. **评估指标局限**：CLIP-Score和FID主要衡量渲染图像的视觉相似度，可能无法完全捕获几何结构的语义正确性。CSR仅验证编译通过，不保证语义准确。

### 补充图表

![[assets/figures/papers/paper_list_l2510_https_arxiv_org_abs_2603_22687/figures/006_Table_3.jpg]]
*Table 3: Performance comparison of instructed code generation in the downstream auxiliary line generation task. The best results are marked with bold*

![[assets/figures/papers/paper_list_l2510_https_arxiv_org_abs_2603_22687/figures/007_Figure_4.jpg]]
*Figure 4: Ablation study of geometric representation on the MathVista-GPS benchmark. The baseline model is Qwen3-VL-30B-A3B*

![[assets/figures/papers/paper_list_l2510_https_arxiv_org_abs_2603_22687/figures/008_Table_4.jpg]]
*Table 4: Performance comparison of four different visual reasoning formats on the MathVista-GPS benchmark. The baseline model is InternVL3.5-38B*

![[assets/figures/papers/paper_list_l2510_https_arxiv_org_abs_2603_22687/figures/010_Figure_6.jpg]]
*Figure 6: Visualization results of tikz codes generated by GeoTikzBridge-Base compared with GPT-5.0[30], each figure shows the input image (either geometric or non-geometric) and the corresponding image rendered from our predicted tikz code*

![[assets/figures/papers/paper_list_l2510_https_arxiv_org_abs_2603_22687/figures/011_Figure_7.jpg]]
*Figure 7: Visualization results of instruction-driven auxiliary line generation compared with GPT-5.0[30], each figure shows the input geometric image, the natural language instruction for auxiliary line addition, and the rendered image from the generated tikz code*

![[assets/figures/papers/paper_list_l2510_https_arxiv_org_abs_2603_22687/figures/013_Figure_S.2.jpg]]
*Figure S.2: Ablation study of different values of self-refinement K for GeoTikzBridge-Base-8B, evaluated on the MathVista-GPS benchmark*

## 方法谱系与知识库定位

### 1. 问题定位与核心瓶颈

当前多模态大语言模型（MLLMs）在几何问题求解中面临一个关键瓶颈：**局部几何感知能力不足**。具体表现为难以精准解析线段之间的空间关系、角度大小、形状约束等细粒度几何结构。此外，该领域长期缺乏大规模、高质量的图像-几何代码配对数据，导致模型既无法从视觉信号中可靠提取几何信息，也难以将几何理解转化为可操作的符号推理。GeoTikzBridge 的提出正是针对这一双重困境——视觉感知的模糊性与符号表示的缺失。

### 2. 与现有方法的对比与定位

#### 2.1 图像到代码生成基线

在图像到 TikZ 代码生成这一核心任务上，GeoTikzBridge 直接对标 **FigCodifier-8B**（已有图像到 TikZ 生成模型）。两者的关键差异体现在三个维度：

- **训练数据规模**：FigCodifier 基于约 145k 的 DaTikZ 种子集进行训练，而 GeoTikzBridge 通过迭代自优化策略将数据集扩展至 2.5M 对（GeoTikz-Base），实现了数量级的提升。
- **局部几何变换策略**：FigCodifier 未采用针对性的几何增强，而 GeoTikzBridge 引入了代码随机删除行（最多 40%）以及配套的图像变换增强策略，该策略使代码重复预测率下降 15%，并在 CLIP 分数和编译成功率上带来显著增益（Figure 5）。
- **辅助线生成能力**：FigCodifier 不支持指令驱动的辅助线生成，GeoTikzBridge 则通过 GeoTikz-Instruct 数据集微调得到 GeoTikzBridge-Instruct，能够根据自然语言指令生成包含辅助线的 TikZ 代码。

在性能表现上，GeoTikzBridge-Base 在 MathVista-GPS 上取得 CLIP-Score 0.915、FID 30.6，显著优于 FigCodifier-8B 的 0.884 和 42.5；在 DaTikZ 上的编译成功率（CSR）从 86.7% 提升至 95.1%（Table 1）。

#### 2.2 多模态大模型基线

在下游几何推理任务中，GeoTikzBridge 以“即插即用”的方式增强现有 VLM/LLM，而非替代它们。对比的基线模型包括：

- **Qwen2.5-VL-32B** 和 **Qwen2.5-VL-72B**：开源多模态大模型基线。
- **InternVL3.5-38B**：开源多模态大模型基线，在 MathVista-GPS 上的原始准确率为 0.688。接入 GeoTikzBridge-Base 生成的 TikZ 代码后，准确率提升至 0.718（+0.030）。
- **GPT-5.0**：在 MathVista-GPS 上的原始准确率为 0.891，接入 GeoTikzBridge-Base 后提升至 0.937（+0.046，Table S8）。

值得注意的是，GeoTikzBridge 对 VLM/LLM 的增强**不涉及任何额外训练**，仅通过提示词将生成的 TikZ 代码作为几何信息补充引入推理流程。这一设计使其与需要端到端微调的几何推理方法形成本质区别。

#### 2.3 几何表示形式的消融定位

GeoTikzBridge 的核心设计选择之一是将几何图像转换为结构化的 TikZ 代码作为显式符号中间表示，而非自然语言描述。消融实验（Figure 4）表明，使用 TikZ 代码作为几何表示比自然语言描述更有效，且 GeoTikzBridge-Base 生成的 TikZ 代码质量优于更大参数量 VLM 直接生成的 TikZ 代码。这一定位说明：**专门的图像到代码模型在几何感知精度上优于通用 VLM 的端到端生成**。

### 3. 适用边界与局限

#### 3.1 模型规模与复杂度约束

8B 参数版本的 GeoTikzBridge-Base 在处理复杂几何图形时，因生成的 TikZ 代码 token 长度超出限制导致截断，引起性能下降。这意味着该方法的实际适用性受限于目标图形的复杂度与模型上下文窗口的匹配程度。

#### 3.2 精细指令执行的不足

GeoTikzBridge-Instruct 在绘制严格平行线等特定指令的生成精度仍有不足。这表明指令驱动的辅助线生成在精确几何约束的满足上尚未达到完全可控的水平。

#### 3.3 生态依赖性

当前方法深度依赖于 LaTeX/TikZ 生态系统。对于无法用 TikZ 清晰表达的图示（如某些工程图表、电路图等），该方法的适应性有限。这构成了其从几何图形向更广泛技术图表泛化的主要障碍。

#### 3.4 复杂数学领域的推理局限

在立体几何和解析几何等复杂数学领域，单纯依靠 TikZ 代码增强的推理仍存在失败案例。这说明符号化的几何表示虽然能弥补视觉感知的不足，但对于需要深度空间推理或代数推导的问题，仍需要更深入的端到端几何推理范式。

### 4. 开放问题

基于上述定位与局限，GeoTikzBridge 开启的研究方向包括：

1. **跨领域泛化**：能否将图像到代码的生成能力扩展至电路图、工程图等非几何技术图表？这需要解决 TikZ 生态之外的代码表示问题。

2. **Agent 化集成**：如何将 GeoTikzBridge 作为代码生成工具集成到多模态 Agent 中，以 Agentic RL 方式进一步提升交互式推理能力？这涉及工具调用、反馈循环与推理策略的联合优化。

3. **长代码截断问题**：如何解决长代码 token 截断问题，使 Base-8B 模型在复杂大图上也能保持高精度？可能的路径包括分块生成、层次化代码结构或模型上下文窗口的扩展。

4. **端到端几何推理**：能否开发端到端的几何推理范式，直接联合优化 TikZ 生成与解题过程，以克服对复杂角度、立体几何、解析几何的弱点？这需要重新设计训练目标与模型架构。

5. **精细几何操作的精度提升**：平行线绘制等精细操作的生成精度应如何通过数据增强策略或模型架构改进来提升？这可能需要针对特定几何约束设计专门的损失函数或后处理机制。

## 原文 PDF

![[paperPDFs/CVPR_2026/GeoTikzBridge_Advancing_Multimodal_Code_Generation_for_Geometric_Perception_and_Reasoning.pdf]]
