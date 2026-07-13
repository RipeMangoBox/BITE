---
title: "MMDIR: Multimodal Instruction-Driven Framework for Mixed-Degradation Document Image Restoration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MMDIR_Multimodal_Instruction_Driven_Framework_for_Mixed_Degradation_Document_Image_Restoration.pdf
project_link: null
code_link: "https://github.com/xiaomore/MMDIR"
aliases:
- MMIDFMDDIR
- MMDIR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入文本指令作为控制信号，利用LLM动态识别退化类型并生成语义提示，从而为视觉解码器提供退化感知的指导，实现多模态协同的恢复。
primary_logic: 将图像恢复任务与视觉语言理解结合，通过指令驱动的跨模态对齐，使模型能感知、推理并处理多种退化，突破了传统端到端映射的局限。
claims:
- MMDIR通过语义结构化指令动态识别存在的退化类型（模糊、阴影、文本水印、印章），增强退化感知学习。
- LLM动态解释指令以生成诊断响应，并引导视觉解码器进行有针对性的恢复。
- MMDIR在单一和混合退化基准上均取得最先进结果，特别是在提出的MixedDoc基准上大幅领先先前方法。
- 消融实验表明引入文本指令全面且显著地提升了所有恢复指标。
---

# MMDIR: Multimodal Instruction-Driven Framework for Mixed-Degradation Document Image Restoration

> [!tip] 核心洞察
> 将图像恢复任务与视觉语言理解结合，通过指令驱动的跨模态对齐，使模型能感知、推理并处理多种退化，突破了传统端到端映射的局限。

| 字段 | 内容 |
|------|------|
| 中文题名 | MMDIR: 面向混合退化文档图像恢复的多模态指令驱动框架 |
| 英文题名 | MMDIR: Multimodal Instruction-Driven Framework for Mixed-Degradation Document Image Restoration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_MMDIR_Multimodal_Instruction-Driven_Framework_for_Mixed-Degradation_Document_Image_Restoration_CVPR_2026_paper.html) · [Code](https://github.com/xiaomore/MMDIR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MMDIR (Multimodal Instruction-Driven Framework for Mixed-Degradation Document Image Restoration) |
| Dataset | BMVC, OSR, MixedDoc |

> [!tip] 效果简介
> - BMVC (Document Deblurring) 上，PSNR / SSIM / LPIPS / DISTS 29.03 / 0.977 / 0.0150 / 0.0233。
> - OSR (Document Deshadow) 上，PSNR / LPIPS / DISTS 19.60 / best (LPIPS, DISTS 最佳)。
> - MixedDoc (Mixed Degradation) 上，PSNR / SSIM 24.43 / 0.908。

## 概要

文档图像恢复（Document Image Restoration, DIR）长期面临一个核心瓶颈：现有方法大多针对单一退化类型（如模糊、阴影、水印、印章）设计端到端映射，无法有效应对现实场景中常见的混合退化与退化类型不确定性问题。这一局限导致在复杂场景下泛化性差，且缺乏对恢复过程的用户引导与可解释性。

MMDIR（Multimodal Instruction-Driven Framework for Mixed-Degradation Document Image Restoration）针对上述瓶颈，将文本指令引入恢复流程作为关键控制信号。其核心思想在于：利用大语言模型（LLM）动态识别输入图像中存在的退化类型，并生成语义诊断响应，进而为视觉解码器提供退化感知的引导，实现多模态协同恢复。这一范式突破了传统图像到图像映射的局限，将视觉语言理解与图像恢复深度融合。

在方法谱系上，MMDIR与此前工作的根本差异体现在三个维度：**输入模态**从单一退化图像扩展为“退化图像+文本指令”；**退化感知机制**从隐式映射或预处理提取的显式先验，转变为LLM动态生成退化识别诊断并以语义提示形式注入视觉解码器；**架构范式**从纯视觉编码器-解码器升级为“视觉编码器+文本嵌入+LLM+语义引导视觉解码器”的多模态架构（见 Figure 2）。

实验表明，MMDIR在单一退化基准（BMVC去模糊、OSR去阴影）和提出的混合退化基准MixedDoc上均取得最优结果。在MixedDoc上，MMDIR达到PSNR 24.43、SSIM 0.908，显著领先于DocDiff、DiffUIR等基线方法。消融实验进一步证实，引入文本指令在去模糊、去阴影及混合退化三个基准上全面且显著地提升了所有恢复指标。

文档图像恢复（Document Image Restoration, DIR）旨在从退化的文档图像中重建高质量的干净图像，是文档分析与识别流程中的关键预处理环节。现实场景中的文档图像常遭受多种退化类型的复合影响，包括模糊、阴影、文本水印以及印章覆盖等。这些退化往往以不确定的组合方式同时出现，严重损害文档的可读性与下游任务（如光学字符识别）的性能。

现有文档图像恢复方法在范式上存在明显局限。以 **DocDiff**（Yang et al., ACM Multimedia 2023）、**NAF-DPM**（Cicchetti et al., arXiv 2024）和 **LGA-Doc**（Tie et al., ICMR 2025）为代表的端到端图像到图像恢复模型，通常针对单一退化类型进行设计和训练，缺乏对退化类型的显式感知与提示引导。**DocRes**（Zhang et al., CVPR 2024）虽然引入了基于预处理退化图像提取的显式先验提示，试图区分不同退化类型，但其提示来源于对输入图像的预处理分析，本质上仍是一种前馈式的固定映射，缺乏对退化语义的深层理解与动态推理能力。这些方法的共同瓶颈在于：无法有效应对现实世界中常见的混合退化场景，且缺乏任务协同和用户引导能力，导致在复杂条件下的泛化性差。

上述瓶颈的根源在于传统范式将文档图像恢复视为一个纯粹的视觉映射问题，忽略了退化类型识别这一关键语义环节。现实中的退化往往是混合且不确定的——用户可能知道文档存在哪些类型的退化，也可能完全未知。现有方法既无法接收用户提供的退化描述作为指导，也无法自主推理图像中存在的退化类型并据此调整恢复策略，从而限制了恢复过程的透明性、可控性和针对性。

为突破这一局限，本文提出 **MMDIR**（Multimodal Instruction-Driven Framework for Mixed-Degradation Document Image Restoration），一种面向混合退化文档图像恢复的多模态指令驱动框架。其核心动机在于：将图像恢复任务与视觉语言理解相结合，通过引入文本指令作为控制信号，使模型能够动态识别退化类型并生成语义提示，从而为视觉解码器提供退化感知的指导。这一范式转变将文档图像恢复从“被动映射”升级为“主动感知与推理”，使模型不仅能恢复图像，还能回答“存在哪些退化”这一诊断性问题，提升了恢复过程的可解释性和人机交互能力。

## 核心方法与创新机理

### 1. 从单模态端到端映射到多模态指令驱动范式

传统文档图像恢复方法（如 **DocDiff** (Yang et al., ACM MM 2023)、**NAF-DPM** (Cicchetti et al., arXiv 2024)、**LGA-Doc** (Tie et al., ICMR 2025)）均采用端到端的图像到图像映射，缺乏对退化类型的显式感知与用户引导能力。**DocRes** (Zhang et al., CVPR 2024) 虽引入了基于预处理退化图像提取的显式先验提示，但其提示来源仍限于视觉域，未能利用语言模态的语义理解能力。

MMDIR 的根本性突破在于将文档图像恢复从**单模态视觉映射**升级为**多模态指令驱动范式**（Figure 1(c)）。模型同时接收退化图像 $I_d$ 和文本指令 $t$，通过跨模态对齐实现退化感知的恢复。这一范式转变的核心体现在三个 changed slots 上：

| 变更维度 | Baseline 做法 | MMDIR 做法 | 机制差异 |
|---------|-------------|-----------|---------|
| **输入模态** | 仅退化图像 | 退化图像 + 文本指令（问题 + 退化识别） | 引入语言模态作为控制信号 |
| **退化感知机制** | 隐式学习固定映射 或 基于预处理提取的显式先验 | LLM 动态生成退化识别诊断，并将回答特征作为语义提示注入视觉解码器 | 从静态映射升级为动态推理引导 |
| **架构范式** | 图像到图像编码器-解码器 | 多模态架构：视觉编码器 + 文本嵌入 + LLM + 语义引导的视觉解码器 | 新增跨模态对齐与语义引导模块 |

### 2. 退化识别与语义引导的闭环机制

MMDIR 的核心创新在于构建了一个**退化识别-语义引导**的闭环：LLM 首先动态解释指令，诊断输入图像中存在的退化类型（模糊、阴影、文本水印、印章），生成结构化回答；随后，回答特征 $F_t$ 作为语义提示，通过 GuidedLayer 注入视觉解码器，指导有针对性的恢复。

具体而言，LLM 处理拼接的视觉标记 $V$ 和文本标记 $(Q, A)$ 后输出回答特征 $F_t = \text{LLM}(\text{CAT}(V, Q, A))$（Section 3.1）。视觉解码器中的 GuidedLayer 对编码器特征 $F_e$ 和来自 LLM 的语义提示特征 $\nabla F_t$ 进行加权融合（Figure 3），最终重建恢复图像 $I_r = \text{VisDecoder}(F_e, F_t)$（Section 3.2）。

这一设计的因果逻辑在于：**退化识别为恢复提供了“诊断信息”，语义提示为解码器提供了“治疗方向”**。消融实验（Table 4）证实，引入文本指令在去模糊（BMVC）、去阴影（OSR）和混合退化（MixedDoc）三个基准上全面且显著地提升了所有恢复指标（PSNR/SSIM/LPIPS/DISTS），验证了该机制的有效性。

### 3. 损失函数中的退化区域感知设计

为增强模型对特定退化模式的感知能力，MMDIR 在标准像素级 L1 损失 $\mathcal{L}_{\text{pixel}} = \| I_{gt} - I_r \|_1$ 之外，引入了**局部区域损失**：

$$\mathcal{L}_{\text{local}} = \| I_{gt} \times I_{mask} - I_r \times I_{mask} \|_1$$

该损失仅作用于退化区域（由二值掩码 $I_{mask}$ 指示），强制模型关注退化像素的精确重建。总损失为四项的加权组合（Section 3.3）：

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{pixel}} + \alpha \mathcal{L}_{\text{local}} + \beta \mathcal{L}_{\text{ssim}} + \lambda \mathcal{L}_{\text{ce}}$$

其中 $\alpha=4, \beta=0.5, \lambda=0.5$。这一设计使模型在混合退化场景下既能保持全局结构一致性，又能精细恢复局部退化区域。

### 4. 与现有工作的本质差异总结

相较于 **DiffUIR** (Zheng et al., CVPR 2024) 等统一图像恢复方法使用扩散先验进行隐式退化处理，MMDIR 的创新在于**显式化退化识别过程**，使模型具备可解释的退化诊断能力。模型不仅能恢复图像，还能输出退化类型判断（Figure 9），这为文档图像恢复任务引入了透明度和可解释性，突破了传统端到端黑盒映射的局限。

MMDIR 是一个端到端的多模态指令驱动框架，其核心设计在于将文档图像恢复任务重新定义为视觉-语言协同推理问题。与传统的图像到图像映射或基于显式先验提示的方法不同，MMDIR 同时接收退化图像和文本指令作为输入，并通过大语言模型（LLM）的推理能力动态感知退化类型，进而为视觉解码器提供语义引导。

### 框架总体结构

如 Figure 2 所示，MMDIR 由四个核心模块串联构成：视觉编码器（VisEncoder）、投影器（Projector）、大语言模型（LLM）和视觉解码器（VisDecoder）。训练阶段与推理阶段的数据流略有不同，但底层架构保持一致。

![[assets/figures/papers/paper_list_l2327_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MMDIR_Multimodal_In/figures/002_Figure_2.jpg]]
*Figure 2: The architecture of our proposed MMDIR. Our model handles multimodal inputs and outputs for document image restoration. In training stage as shown in the (a) on the left, it takes a Degraded Image*

**训练阶段流程：**

1. **视觉编码**：退化图像 $I_d$ 经过基于 ViTDet 架构的视觉编码器，提取多尺度视觉特征 $F_e$。
2. **特征投影**：投影器通过两层 $3 \times 3$ 卷积，对 $F_e$ 进行降维和通道扩展，生成视觉标记 $V$。
3. **多模态融合与退化识别**：将视觉标记 $V$ 与文本指令标记 $Q$（问题）和答案标记 $A$（退化识别真值）拼接后送入 LLM。LLM 在训练阶段同时接收答案标记，学习跨模态特征对齐，并输出回答特征 $F_t$。
4. **语义引导恢复**：视觉解码器以视觉特征 $F_e$ 和来自 LLM 的语义提示特征 $F_t$ 为输入，通过 GuidedLayer 进行特征加权融合，最终重建恢复图像 $I_r$。

**推理阶段流程：**

推理时，模型仅接收退化图像 $I_d$ 和文本指令问题 $Q$，不再需要答案标记 $A$。LLM 通过逐步解码生成退化识别响应，该响应中实际存在的退化类型以绿色高亮标注，不存在的以红色标注，待识别的以橙色标注。生成的回答特征 $F_t$ 随后注入视觉解码器，指导图像恢复。

### 关键公式

整个前向传播过程可形式化为：

$$
F_e = \text{VisEncoder}(I_d)
$$
$$
V = \text{Projector}(F_e)
$$
$$
F_t = \text{LLM}(\text{CAT}(V, Q, A))
$$
$$
I_r = \text{VisDecoder}(F_e, F_t)
$$

其中 $\text{CAT}(\cdot)$ 表示拼接操作。视觉解码器的核心是 GuidedLayer（见 Figure 3），它对视觉特征图 $F_e$ 和 LLM 输出的语义提示特征 $\nabla F_t$ 进行加权融合，使恢复过程能够感知并响应指令中指定的退化类型。

### 与现有范式的本质区别

Figure 1 清晰对比了三代文档图像恢复范式：

- **传统端到端方法**（如 **DocDiff** (Yang et al., ACM Multimedia 2023)、**NAF-DPM** (Cicchetti et al., arXiv 2024)、**LGA-Doc** (Tie et al., ICMR 2025)）：仅接收退化图像，无任何提示引导，且通常针对单一退化类型训练。
- **显式先验提示方法**（如 **DocRes** (Zhang et al., CVPR 2024)）：使用从预处理退化图像中提取的显式先验作为提示，区分退化类型。
- **MMDIR 的多模态指令驱动范式**：同时处理多模态输入和输出。文本指令与退化图像一同输入，模型首先回答指令问题（识别退化类型的存在与否），再将语义理解结果作为引导信号反馈给视觉解码器。这一设计使退化感知从隐式映射或预处理提取提升为动态语义推理。

### 训练损失设计

为增强模型对退化区域的感知能力，MMDIR 采用多分量联合损失函数：

$$
\mathcal{L}_{total} = \mathcal{L}_{pixel} + \alpha \mathcal{L}_{local} + \beta \mathcal{L}_{ssim} + \lambda \mathcal{L}_{ce}
$$

其中：
- $\mathcal{L}_{pixel} = \| I_{gt} - I_r \|_1$ 为像素级 L1 损失；
- $\mathcal{L}_{local} = \| I_{gt} \times I_{mask} - I_r \times I_{mask} \|_1$ 为退化区域的局部 L1 损失，通过二值掩码 $I_{mask}$ 引导模型关注退化位置；
- $\mathcal{L}_{ssim}$ 为结构相似性感知损失；
- $\mathcal{L}_{ce}$ 为退化识别的交叉熵损失。

加权系数设置为 $\alpha = 4$、$\beta = 0.5$、$\lambda = 0.5$。局部损失的设计直接呼应了框架的退化感知目标——模型不仅需要恢复图像，还需要准确识别退化类型，并在对应区域施加更强的重建约束。

### 3.1 多模态编码：从退化图像到语义诊断

MMDIR 的核心感知链路始于对退化图像与文本指令的联合编码，其目标是将“图像恢复”重新定义为一种跨模态的条件生成任务。整个前向编码过程可形式化为三个连续步骤：

$$
F_e = \text{VisEncoder}(I_d) \\
V = \text{Projector}(F_e) \\
F_t = \text{LLM}(\text{CAT}(V, Q, A))
$$

**视觉编码器（VisEncoder）** 采用 ViTDet-based 架构，接收退化图像 $I_d$，输出多尺度视觉特征 $F_e$。该编码器的关键作用在于保留细粒度的纹理与结构信息，为后续解码器提供丰富的空间上下文。

**投影器（Projector）** 由两层 $3 \times 3$ 卷积构成，对 $F_e$ 进行降采样与通道扩张，生成视觉标记 $V$。这一操作将视觉特征映射到与语言模型兼容的嵌入空间，是实现跨模态对齐的结构性桥梁。

**大语言模型（LLM）** 采用 Qwen2.5 0.5B 版本，训练期间除嵌入层外全部冻结。LLM 接收拼接后的视觉标记 $V$、文本指令标记 $Q$（问题）和答案标记 $A$，通过自回归解码生成回答特征 $F_t$。该特征实质上是 LLM 对“图像中存在哪些退化类型”这一诊断性问题的语义响应，明确指示了模糊、阴影、文本水印和印章四类退化的存在与否。这一设计构成了本文的核心因果调节变量——将退化感知从隐式映射显式化为可解释的语义信号。

### 3.2 语义引导的视觉解码器

视觉解码器以编码器特征 $F_e$ 和 LLM 回答特征 $F_t$ 为双路输入，最终重建恢复图像 $I_r$：

$$
I_r = \text{VisDecoder}(F_e, F_t)
$$

解码器的关键创新在于 **GuidedLayer** 模块。该层对 $F_e$ 的特征图与来自 LLM 的语义提示特征 $\nabla F_t$ 进行加权融合，使恢复过程显式受控于退化诊断结果。具体而言，GuidedLayer 将语义提示作为通道维度的调制信号，引导解码器在不同空间位置施加差异化的恢复策略——例如，在检测到阴影的区域增强亮度校正，在印章覆盖区域强化纹理重建。

解码器内部采用 NAF Block 中的简化通道注意力（SCA）机制，并结合 PixelShuffle 进行多尺度特征融合与上采样，最终输出与输入分辨率一致的恢复图像。

### 3.3 训练损失函数

总损失函数由四项加权组合构成：

$$
\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{pixel}} + \alpha \mathcal{L}_{\text{local}} + \beta \mathcal{L}_{\text{ssim}} + \lambda \mathcal{L}_{\text{ce}}
$$

各项定义与作用如下：

**像素级 L1 损失** 约束恢复图像与干净真值 $I_{gt}$ 的全局一致性：

$$
\mathcal{L}_{\text{pixel}} = \| I_{gt} - I_r \|_1
$$

**局部区域 L1 损失** 针对退化区域施加额外监督，利用二值掩码 $I_{\text{mask}}$ 指示退化位置：

$$
\mathcal{L}_{\text{local}} = \| I_{gt} \times I_{\text{mask}} - I_r \times I_{\text{mask}} \|_1
$$

这一项迫使模型将恢复能力聚焦于实际受损区域，避免对干净背景的过度修正。

**SSIM 感知损失** 补充像素级损失的感知盲区，提升结构保真度。**交叉熵损失** $\mathcal{L}_{\text{ce}}$ 则直接监督 LLM 的退化识别输出，确保语义诊断的准确性。加权系数设定为 $\alpha = 4$，$\beta = 0.5$，$\lambda = 0.5$，体现了对局部退化区域恢复质量的侧重。

### 3.4 关键设计决策的因果逻辑

整个框架的设计遵循一条清晰的因果链：**文本指令 → LLM 退化诊断 → 语义提示注入 → 条件化图像恢复**。与传统端到端映射（如 **DocDiff** (Yang et al., ACM Multimedia 2023)、**NAF-DPM** (Cicchetti et al., arXiv 2024)）或基于预处理先验的 **DocRes** (Zhang et al., CVPR 2024) 不同，MMDIR 将退化类型的识别从隐式特征学习解耦为显式的跨模态推理任务。消融实验（Table 4）证实，移除文本指令（即去除 LLM 分支）会导致三个基准上的 PSNR、SSIM、LPIPS 和 DISTS 全面劣化，验证了语义引导作为核心因果调节变量的有效性。

![[assets/figures/papers/paper_list_l2327_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MMDIR_Multimodal_In/figures/003_Figure_3.jpg]]
*Figure 3: The architecture of vision decoder. SCA represents the Simplified Channel Attention in the NAF Block [2]. The GuidedLayer weights the feature maps of*

## 实验与关键发现

### 实验设置与公平性保障

MMDIR 基于 PyTorch 框架实现，视觉编码器采用 ViTDet 架构，大语言模型选用 **Qwen2.5 (0.5B)** 并在训练过程中冻结除嵌入层外的所有参数。训练使用余弦衰减学习率调度，最大学习率为 $3 \times 10^{-4}$，输入分辨率统一设置为 $1024 \times 1024$。

为保障比较的公平性，所有对比方法均使用相同的合成数据集和统一训练配置重新训练或复现。其中 **DiffUIR**（Zheng et al., CVPR 2024）按照作者公开代码并使用相同训练数据重新实现（在结果中以“*”标注）。评估指标覆盖像素级保真度（PSNR、SSIM）、感知质量（LPIPS、DISTS）、下游 OCR 性能（CER、ED）以及生成质量（FID），从多维度验证恢复效果。

### 单一退化基准上的性能

在去模糊基准 **BMVC** 和去阴影基准 **OSR** 上的定量对比结果如表 1 所示。MMDIR 在 BMVC 上取得了 29.03 PSNR 和 0.977 SSIM，在 OSR 上取得了 19.60 PSNR，并在 LPIPS 和 DISTS 指标上达到最优。与先前方法相比，MMDIR 在感知指标上的提升尤为显著：LPIPS 改善约 11.2%，DISTS 改善约 43.0%，表明恢复结果在结构和纹理层面更接近真实图像。

图 6 和图 7 分别展示了去模糊和去阴影任务上的可视化对比。红色和绿色放大框突出了细节差异——MMDIR 恢复的文字边缘更清晰，阴影区域的字符可读性显著优于基线方法，验证了退化感知引导对局部细节恢复的有效性。

### 混合退化基准 MixedDoc 上的性能

为评估模型在真实复杂场景下的表现，作者构建了混合退化基准 **MixedDoc**，包含模糊、阴影、文本水印和印章四种退化类型的随机组合（样本可视化见 Figure 5）。在该基准上（表 3），MMDIR 以 **24.43 PSNR** 和 **0.908 SSIM** 大幅领先先前方法，相比次优方法提升显著。

![[assets/figures/papers/paper_list_l2327_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MMDIR_Multimodal_In/figures/005_Figure_5.jpg]]
*Figure 5: Several samples visualization of our test benchmark MixedDoc. Top row: the degraded images. Middle row: the degradation types Seal, Blur, Shadow, or Watermark. Bottom row: the ground-truth images. Zoom in for the best view*

下游 OCR 评估（表 5）进一步验证了恢复质量的实际效用：MMDIR 取得 **0.17 CER** 和 **240.8 ED**，FID 降至 **9.07**，表明恢复后的文档图像在字符识别准确率和视觉真实感上均达到最优。图 8 的定性对比显示，**DocDiff**（Yang et al., ACM Multimedia 2023）和 DiffUIR 在混合退化场景下容易残留阴影或水印伪影，而 MMDIR 能更彻底地去除多种退化。

### 文本指令的消融分析

消融实验（表 4）直接验证了文本指令这一核心设计的作用。在去模糊（BMVC）、去阴影（OSR）和混合退化（MixedDoc）三个基准上，引入文本指令（LLM 语义引导）全面且显著地提升了所有恢复指标（PSNR、SSIM、LPIPS、DISTS）。这证明 LLM 生成的退化识别诊断确实为视觉解码器提供了有效的退化感知语义提示，而非冗余组件。

### 退化类型数量对性能的影响

Figure 10 揭示了模型性能随退化类型数量增加的变化趋势：当单张图像包含的退化类型从 1 种增加到 4 种时，PSNR 和 SSIM 均呈现持续下降趋势。这表明密集型混合退化仍然是当前方法的瓶颈——多退化叠加可能造成特征冲突或语义提示信息过载，导致视觉解码器难以同时兼顾所有退化模式的精确恢复。这一发现为后续研究指明了优化方向。

![[assets/figures/papers/paper_list_l2327_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MMDIR_Multimodal_In/figures/013_Figure_10.jpg]]
*Figure 10: Trend of PSNR and SSIM with increasing degradation types on the MixedDoc benchmark*

### 退化识别的准确性

MMDIR 不仅输出恢复图像，还能同步诊断图像中存在的退化类型。表 6 报告了各退化类型的精确率、召回率和 F1 分数；表 7 进一步细分了不同退化数量组合下的识别性能。这些结果表明 LLM 在多标签退化分类任务上具有可靠的判别能力，为框架的可解释性和用户交互提供了基础。

### 失败模式与局限性

尽管 MMDIR 在各项基准上取得领先，分析揭示了以下局限：

1. **密集型混合退化性能衰减**：如前所述，退化类型增多时恢复质量下降，表明模型在处理高度复杂的退化组合时仍有不足。
2. **合成数据的域间隙**：训练数据均为合成生成，尽管模拟了真实退化模式，但与开放环境中非均匀、不规则的噪声分布仍存在差异，域外泛化能力需要进一步验证。
3. **LLM 能力的未充分挖掘**：当前使用 Qwen2.5 0.5B 并冻结参数，更强大 LLM 或对 LLM 进行微调是否能提升退化识别的鲁棒性和指令泛化性，仍属开放问题。

![[assets/figures/papers/paper_list_l2327_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MMDIR_Multimodal_In/figures/006_Table_1.jpg]]
*Table 1: Comparisons on single degradation benchmark. “↑” indicates the higher the better and “↓” denotes the opposite. The best performing result is shown in Bold font, and the second best result is shown with an underline. The “*” indicates results reproduced based on the authors’ public code and the same training dataset as used in our method. “256” and*

![[assets/figures/papers/paper_list_l2327_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MMDIR_Multimodal_In/figures/014_Figure_9.jpg]]
*Figure 9: Visualization of our model’s predictions*

## 定位与知识库关联

### 1. 与基线方法的关系与定位

MMDIR 处于**文档图像恢复（DIR）**与**多模态视觉语言理解**的交叉点，其核心创新在于将文本指令作为控制信号引入恢复流程，从而突破了传统端到端映射范式的局限。

**传统端到端恢复方法**（如 **DocDiff** (Yang et al., ACM Multimedia 2023)、**NAF-DPM** (Cicchetti et al., arXiv 2024)、**LGA-Doc** (Tie et al., ICMR 2025)）采用图像到图像的编码器-解码器架构，专注于单一退化类型（如去模糊或去阴影）。这类方法将退化感知隐式编码在网络权重中，缺乏对退化类型的显式建模能力，因此在面对混合退化时泛化性急剧下降——模型无法判断当前输入中存在哪些退化，更无法针对性地调度恢复策略。

**显式先验提示方法**以 **DocRes** (Zhang et al., CVPR 2024) 为代表，通过预处理从退化图像中提取先验提示来区分退化类型。这在一定程度上引入了退化感知，但其先验提取依赖手工设计的预处理流程，提示质量受限于预处理精度，且无法利用语义层面的退化推理。**DiffUIR** (Zheng et al., CVPR 2024) 则采用扩散先验进行统一图像恢复，但同样缺乏对退化类型的动态识别机制。

MMDIR 与上述方法的**三个关键差异槽位**如下：

| 差异维度 | 基线方法 | MMDIR |
|---------|---------|-------|
| **输入模态** | 仅退化图像 | 退化图像 + 文本指令（问题 + 退化识别） |
| **退化感知机制** | 隐式固定映射 或 预处理提取的显式先验 | LLM 动态生成退化诊断，并将回答特征作为语义提示注入视觉解码器 |
| **架构范式** | 图像到图像编码器-解码器（无跨模态组件） | 多模态架构：视觉编码器 + 文本嵌入 + LLM + 语义引导的视觉解码器 |

从**因果机制**角度看，MMDIR 的突破在于识别并操纵了关键因果节点：**退化感知信号**。传统方法将该信号隐式编码在网络参数中（不可控、不可解释），DocRes 通过预处理引入显式但粗糙的信号，而 MMDIR 利用 LLM 的语义理解能力动态生成精细的退化诊断，并通过 GuidedLayer 将该语义提示注入视觉解码器的多尺度特征融合过程。这一设计使得恢复过程从“盲目映射”转变为“感知-推理-恢复”的认知流程。

### 2. 适用边界

MMDIR 的适用边界由以下因素界定：

**退化类型覆盖范围**：当前框架明确支持的退化类型包括模糊（Blur）、阴影（Shadow）、文本水印（Text Watermark）和印章（Seal）四类。训练数据通过合成流水线生成这些退化的组合样本（见 Figure 4），因此模型在这四类退化及其组合上表现最佳。对于训练中未见的退化类型（如污渍、折痕、低光照、墨迹渗透），模型的泛化能力尚未验证，属于开放问题。

**退化复杂度上限**：消融实验（Figure 10）揭示了明确的性能退化趋势——当单张图像包含的退化类型从 1 种增加到 4 种时，PSNR 和 SSIM 均呈下降趋势。这表明尽管 MMDIR 能处理混合退化，但在密集型多退化叠加场景下，恢复质量仍有明显衰减。这一趋势的潜在瓶颈可能在于：LLM 生成的语义提示在多退化并存时信息密度增加，而视觉解码器的 GuidedLayer 在多目标引导下的特征融合能力存在上限。

**数据域限制**：训练数据主要为合成数据，退化模式虽经设计以模拟真实场景，但与开放环境中的非均匀噪声分布、光照变化、纸张纹理等复杂因素仍有差距。这构成了域外泛化的潜在风险，需要在实际部署前进行域适配验证。

**LLM 能力依赖**：框架依赖 LLM 的推理能力进行退化识别，当前使用 **Qwen2.5 0.5B** 且冻结除嵌入层外的所有参数。LLM 的规模、预训练质量以及是否微调，直接影响退化识别的准确率（见表 6、表 7 的退化识别 F1 指标）和指令泛化能力。

### 3. 局限与开放问题

**已识别的局限**：

1. **密集型混合退化性能衰减**：如 Figure 10 所示，退化类型增多时 PSNR 和 SSIM 持续下降，表明模型在处理高复杂度混合退化时存在瓶颈。这可能源于语义提示在多目标场景下的信息稀释效应，或视觉解码器多尺度融合能力的饱和。

2. **合成数据与真实场景的差距**：尽管合成流水线尽力模拟真实退化，但真实文档图像中的退化往往具有非均匀空间分布、复杂光照交互和物理介质相关特性，合成数据难以完全覆盖。

3. **LLM 参数的冻结策略**：当前仅训练嵌入层，LLM 主体参数冻结。这一设计虽然降低了训练成本，但也限制了模型对退化描述语言的深度适配能力，可能影响指令变体的鲁棒性。

**待探索的开放问题**：

1. **退化类型的可扩展性**：如何将框架扩展到更广泛或未见过的退化类型（如污渍、折痕、低光照、墨迹渗透）？这需要研究指令模板的泛化设计和增量学习策略。

2. **LLM 能力的深度利用**：在当前冻结参数的基础上，微调 LLM 或引入更强大的模型（如更大规模的 Qwen 变体或指令微调模型）是否能提升退化识别的鲁棒性和恢复质量？这涉及计算成本与性能增益的权衡。

3. **真实数据驱动的训练范式**：能否利用真实采集的混合退化数据替代或增强合成流水线，从而缩小域间隙？这需要构建大规模的真实混合退化文档数据集，并设计相应的标注协议。

4. **与下游任务的联合优化**：该指令驱动范式如何与文档理解下游任务（如 OCR、布局分析、信息提取）进行更深层次的联合优化？当前恢复质量通过 CER/ED 间接评估对 OCR 的影响（Table 5），但恢复模型与 OCR 模型的端到端联合训练尚未探索。

5. **指令泛化性**：Table 2 展示了指令变体对退化识别的影响，但更广泛的指令措辞变化、多语言指令、以及零样本退化描述下的鲁棒性仍需系统评估。

## 原文 PDF

![[paperPDFs/CVPR_2026/MMDIR_Multimodal_Instruction_Driven_Framework_for_Mixed_Degradation_Document_Image_Restoration.pdf]]
