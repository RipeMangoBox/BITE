---
title: Selectively Extracting and Injecting Visual Attributes into Text-to-Image Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Selectively_Extracting_and_Injecting_Visual_Attributes_into_Text_to_Image_Models.pdf
project_link: null
code_link: "https://huggingface.co/black-forest-labs/FLUX.1-dev"
aliases:
- SAEIPCIM
- SEIVAITIM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过构建排除非目标属性的定制训练提示，并引入蒸馏嵌入（利用文本编码器中Transformer的注意力机制按类别提取目标特征）和残差嵌入（捕获剩余属性并加余弦相似度损失防止其学习目标概念），实现目标属性的选择性提取与注入。
primary_logic: "将占位符标记与类别词（如\"[*] color\"）一起送入文本编码器的Transformer，可让类别词对应的嵌入选择性地关注并蒸馏出该类别相关的视觉特征，而不会混入其他非目标属性。"
claims:
- 蒸馏嵌入在结构上阻止了非目标属性的学习，仅保留目标概念特征。
- 在概念相似性和概念排他性评估中，本文方法总体得分最高。
- 消融实验证实，移除残差嵌入会导致训练不稳定，无法成功学习目标概念。
- 用户研究结果表明，本文方法在概念相似性和排他性方面大幅优于现有基线。
---

# Selectively Extracting and Injecting Visual Attributes into Text-to-Image Models

> [!tip] 核心洞察
> 将占位符标记与类别词（如"[*] color"）一起送入文本编码器的Transformer，可让类别词对应的嵌入选择性地关注并蒸馏出该类别相关的视觉特征，而不会混入其他非目标属性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向文本到图像模型的选择性视觉属性提取与注入方法 |
| 英文题名 | Selectively Extracting and Injecting Visual Attributes into Text-to-Image Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Choi_Selectively_Extracting_and_Injecting_Visual_Attributes_into_Text-to-Image_Models_CVPR_2026_paper.html) · [HuggingFace](https://huggingface.co/black-forest-labs/FLUX.1-dev) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Selective Attribute Extraction and Injection (proposed concept injection method) |
| Dataset | Concept Learning Dataset |

> [!tip] 效果简介
> - Concept Learning Dataset (自定义) 上，Prompt Fidelity (用户研究) 0.815 vs TokenVerse 0.573 / ProSpect 0.820 (+0.242 vs TokenVerse, -0.005 vs ProSpect)；Concept Similarity (CS) & Concept Exclusivity (CE) 最高综合得分 vs 低于本文方法 (定性及定量上均显著优于大部分基线)。

## 概述

文本到图像生成模型在将自然语言描述转换为视觉内容方面已取得显著进展，但用户若希望从一张参考图像中提取特定的视觉属性（如形状、材质、姿态或镜头角度），并将其灵活注入到新的生成场景中，仍面临根本性困难。这一瓶颈的根源在于，参考图像中的多个视觉属性高度纠缠——一张照片同时包含了物体的颜色、形状、材质、光照和构图等信息，现有方法在学习可迁移的概念表示时，往往无法将目标属性与非目标属性精确分离，导致生成的嵌入不必要地复制了参考图像的布局、视角等无关特征。

针对这一核心问题，本文提出了一种**选择性视觉属性提取与注入方法**。其关键洞察在于：将占位符标记与类别词（如“`[*] color`”）一起送入文本编码器的Transformer时，类别词对应的嵌入能够通过自注意力机制选择性地关注并蒸馏出该类别相关的视觉特征，而不会混入其他非目标属性。基于这一发现，方法构建了三个协同工作的核心组件：（1）利用视觉语言模型（VLM）生成明确排除目标属性的定制训练提示，从输入端粗略过滤非目标信息；（2）引入**蒸馏嵌入**（distilled embedding），在结构层面阻止非目标属性的学习，仅保留目标概念特征；（3）引入**残差嵌入**（residual embedding）捕获剩余属性，并通过余弦相似度损失强制其与蒸馏嵌入正交，从而稳定训练过程并防止目标概念泄露。

实验结果表明，该方法在概念相似性和概念排他性两个维度上总体优于现有基线方法。用户研究进一步证实，本文方法在提示保真度方面取得最高分（0.815），显著超越**TokenVerse**（Garibi et al., TOG 2025）等属性级概念学习方法。消融实验验证了蒸馏嵌入与残差嵌入的必要性：移除残差嵌入会导致训练不稳定，而仅使用定制提示而不采用蒸馏嵌入，则非目标属性仍会混入标记嵌入。该方法在方法谱系上属于**基于文本反转的属性解耦学习**范式，与**Textual Inversion**（Gal et al., arXiv 2022）等整体对象学习方法形成互补，为解决细粒度视觉属性迁移问题提供了新的技术路径。

## 背景与动机

文本到图像生成模型近年取得了长足进步，用户只需提供自然语言描述即可生成高质量的视觉内容。然而，当用户希望从单张参考图像中精确提取某个特定视觉属性（如形状、材质、姿态或镜头角度），并将其注入到全新的场景中时，现有方法面临根本性困难。

**核心瓶颈在于属性的高度纠缠。** 参考图像天然包含多个相互耦合的视觉特征——同一张图像同时承载着物体的形状、颜色、纹理、光照、构图和背景信息。传统方法在从图像中学习概念时，往往将整张图像的信息压缩到一个可学习的标记嵌入中，导致非目标属性不可避免地混入所学表示。例如，当用户只想提取“蓝色”这一颜色属性时，标准方法学到的嵌入可能同时携带了参考图像中的物体形状、相机焦距甚至背景布局（见 Figure 4a 的定性证据）。这种属性泄漏严重限制了概念迁移的精确性和背景生成的灵活性。

**现有方法的缺口。** 以 **Textual Inversion**（Gal et al., arXiv 2022）为代表的早期工作通过优化单个标记嵌入来重建参考图像中的完整物体，但其设计目标本身就是物体级（subject-driven）生成，天然不具备属性级解耦能力。后续工作如 **ProSpect**（Zhang et al., TOG 2023）和 **TokenVerse**（Garibi et al., TOG 2025）尝试通过提示谱分解或调制参数优化来实现更细粒度的概念学习，但它们在面对高度纠缠的视觉属性时，仍难以将目标属性从其他特征中干净地剥离出来。**U-VAP**（Wu et al., CVPR 2024）聚焦于用户指定的外观个性化，同样未系统解决属性选择性提取的问题。此外，像 **OmniGen2**（Wu et al., arXiv 2025）和 **GPT Image 1** 等统一多模态生成模型虽具备零样本概念学习能力，但在属性级精确控制方面表现有限（见 Figure 9 的对比证据）。

**手动提示工程的局限。** 一个直观的替代方案是用户通过精细的文本提示来描述目标属性，试图在生成过程中“还原”该属性。然而，如图 Figure 2a 所示，即便用户提供了详尽的描述，生成结果中的目标属性仍可能偏离预期。这是因为自然语言对视觉属性的编码能力有限——许多微妙的视觉特征（如特定的材质光泽、笔触风格或透视角度）难以用文字精确刻画。直接从参考图像中“提取”属性，而非用语言“描述”属性，成为解决这一问题的关键路径。

**本文的动机。** 上述困境催生了一个核心研究问题：能否设计一种方法，从单张充满纠缠特征的参考图像中，**选择性地**提取用户指定的目标视觉属性，并将其**独立地**注入到任意新场景中，同时保持非目标属性的完全灵活？本文的答案是通过构建一种新的概念注入范式——在训练阶段利用视觉语言模型（VLM）显式排除非目标属性，并引入蒸馏嵌入和残差嵌入的联合优化机制，从根本上阻断非目标特征进入所学表示。这一设计使得方法能够在形状、材质、姿态、镜头角度等多个属性维度上实现干净、可控的概念迁移（见 Figure 1 的示例结果）。

## 核心创新

本文的核心创新在于提出了一套**选择性属性提取与注入**机制，通过三个紧密协作的“changed slots”系统性地解决了现有方法中视觉属性高度纠缠的瓶颈。

### 创新1：VLM驱动的定制训练提示（排除非目标属性）

传统方法（如**Textual Inversion** (Gal et al., arXiv 2022)）通常使用简单的提示（如“A [*]”）来学习整个对象的概念，导致标记嵌入不可避免地吸收参考图像中的所有视觉属性。

本文的创新在于引入**视觉语言模型（VLM）**自动生成**排除目标概念**的定制训练提示 $\tilde{y}_{\text{custom}}$。具体而言，给定参考图像 $\mathbf{x}_0$ 和目标概念 $c$（如“颜色”），VLM被指示用一句话描述 $\mathbf{x}_0$ 中除 $c$ 以外的所有属性（如形状、材质、姿态、构图等），然后将占位符短语（如“[*] color”）插入该描述中，形成定制提示。这一策略在训练初始阶段就**粗略排除了非目标属性的干扰**，为后续的精细解耦奠定了基础。

### 创新2：蒸馏嵌入（选择性提取目标特征）

这是本文最核心的技术创新。传统方法直接优化可学习的标记嵌入 $\mathbf{e}_*$ 来重建整个图像，导致 $\mathbf{e}_*$ 中混合了所有视觉属性。

本文提出了**蒸馏嵌入** $\mathbf{h}_{[\text{category}]*}$，其关键机制在于利用文本编码器中Transformer的自注意力结构：将“[*] [category]”短语送入文本编码器，其中 [category] 是目标概念的粗粒度类别描述词（如“color”、“material”、“pose”）。由于自注意力机制的作用，[category] 对应的嵌入会**选择性地从 [*] 中提取与该类别相关的视觉特征**，从而在结构上隔离了目标概念。

Figure 5 的可视化实验直接证实了这一机制：当用实际颜色词（如“red”、“green”、“blue”）替换 [*] 时，颜色嵌入发生显著变化；而替换为非颜色词（如“circular”、“stretching”）时，嵌入几乎不变。这表明蒸馏嵌入天然具备**类别选择性**，不会混入非目标属性。

### 创新3：残差嵌入与余弦相似度损失（稳定训练与属性隔离）

仅使用蒸馏嵌入进行重建会引发训练冲突：定制提示 $\tilde{y}_{\text{custom}}$ 中未描述的非目标属性仍需被某个嵌入表示，否则模型会强行将其压缩进蒸馏嵌入中。

为解决这一问题，本文引入**可学习的残差嵌入** $\mathbf{h}_{\text{residual}}$，将其前置（prepend）到提示序列中，专门用于捕获所有未被 $\tilde{y}_{\text{custom}}$ 描述的剩余属性。同时，引入**余弦相似度损失**：

$$\mathcal{L}_{\text{cosine}} = \max\left(0, \frac{\mathbf{h}_{\text{residual}} \cdot \mathbf{h}_{[\text{category}]*}}{\|\mathbf{h}_{\text{residual}}\| \|\mathbf{h}_{[\text{category}]*}\|}\right)$$

该损失强制 $\mathbf{h}_{\text{residual}}$ 与 $\mathbf{h}_{[\text{category}]*}$ 正交，**从损失函数层面阻止残差嵌入学习目标概念**。消融实验（Figure 6）直接证实：移除残差嵌入（Ours w/o $\mathbf{h}_{\text{residual}}$）会导致训练不稳定，无法成功提取目标概念。

### 创新总结

三个创新形成了完整的**因果链条**：定制提示提供粗粒度的属性排除 → 蒸馏嵌入利用Transformer的自注意力实现结构性的类别特征选择 → 残差嵌入与余弦损失提供训练稳定性和精细的属性隔离。这一组合使模型能够在保持背景灵活性的同时，仅从单张参考图像中精确迁移目标属性，而不会复制布局、相机焦点等非目标特征（Figure 4 直接对比证实）。

## 整体框架

本文提出的选择性属性提取与注入方法，旨在从单张参考图像中解耦并学习特定的视觉属性概念（如形状、材质、姿态、镜头角度），随后将该概念灵活注入到任意新场景中。整个框架围绕一个核心矛盾展开：参考图像中多个视觉属性高度纠缠，传统的可学习标记嵌入会不可避免地吸收非目标属性，导致概念迁移时背景灵活性丧失。为解决这一问题，方法构建了一个四阶段协同优化的pipeline，其输入输出流与模块关系如Figure 3所示。

**输入与输出流**：系统的输入包括一张参考图像 $\mathbf{x}_0$ 和一个用户指定的目标概念 $c$（如“颜色”、“形状”）。输出为一个经过优化的、仅编码目标概念特征的文本嵌入，该嵌入可像普通文本标记一样被插入到任意扩散模型的提示中，用于生成保留目标属性但背景完全不同的图像。

**模块协作关系**：整个pipeline由四个核心模块串联而成，形成“排除非目标属性→选择性提取目标属性→残差捕获→联合优化”的级联结构：

1.  **VLM驱动的提示构建模块**：首先，利用视觉语言模型（VLM）生成一条描述参考图像的句子，但明确要求VLM**排除**目标概念 $c$。随后，将概念特定的占位符短语（如 `[*]`）插入到该句子中，形成定制训练提示 $\tilde{y}_{\text{custom}}$。这一步骤在进入优化循环之前，从文本层面粗略地排除了非目标属性，为后续的精确分离奠定基础。

2.  **蒸馏嵌入提取模块**：这是实现选择性提取的关键。将占位符与目标概念的类别词组成的短语（如 `[*] color`）送入文本编码器的Transformer中。由于自注意力机制的作用，类别词（如 `color`）对应的输出嵌入会**选择性地关注并从 `[*]` 的表示中蒸馏出与该类别相关的视觉特征**。由此产生的嵌入被称为蒸馏嵌入 $\mathbf{h}_{\text{[category]*}}$，它在结构上被强制仅包含目标概念的特征，而排除了布局、视角等非目标信息。

3.  **残差嵌入提取与优化模块**：由于定制提示无法完美描述所有非目标属性，仅使用蒸馏嵌入进行重建会导致训练不稳定。为此，引入一个可学习的残差嵌入 $\mathbf{h}_{\text{residual}}$，其设计目的是**吸收所有未被定制提示描述的剩余视觉属性**。该残差嵌入被预先添加到定制提示的文本编码序列前端，与蒸馏嵌入共同参与图像重建。

4.  **联合优化环路**：在冻结扩散模型全部参数的前提下，整个系统仅对两个组件进行迭代优化——蒸馏嵌入所依赖的可学习占位符标记，以及残差嵌入。优化目标是一个组合损失函数：
    $$ \mathcal{L}_{\text{total}} = \mathcal{L}_{\text{recon}} + \lambda \mathcal{L}_{\text{cosine}} $$
    其中，$\mathcal{L}_{\text{recon}}$ 是标准的重建损失，要求模型利用蒸馏嵌入和残差嵌入共同重建参考图像；而 $\mathcal{L}_{\text{cosine}}$ 是一个余弦相似度损失，它强制残差嵌入与蒸馏嵌入保持正交，从而**在数学上阻止残差嵌入学习目标概念**，确保目标属性仅由蒸馏嵌入捕获。通过这一联合优化，模型最终学会将目标概念从纠缠的视觉特征中精确解耦出来。

### 补充图表

![[assets/figures/papers/paper_list_l2343_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Selectively_Extra/figures/004_Figure_3.jpg]]
*Figure 3: An overview of our method. (a) Given a reference image x0 and a target concept c, we utilize a VLM to construct a custom training prompt that explicitly describes the untargeted attributes. (b) To isolate the target concept, we extract a distilled embedding (h[category]←∗) through the text transformer. Concurrently, a residual embedding (hresidual) captures the remaining attributes to stabilize the joint optimization*

![[assets/figures/papers/paper_list_l2343_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Selectively_Extra/figures/002_Figure_1.jpg]]
*Figure 1: Results generated by the proposed concept injection method. The method extracts attribute-level concepts from an image of entangled visual features and applies them to diverse environments*

![[assets/figures/papers/paper_list_l2343_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Selectively_Extra/figures/003_Figure_2.jpg]]
*Figure 2: Two image generation scenarios. (a) A user attempts to reconstruct the target attribute with a detailed prompt, but the generated attribute deviates. (b) Our method successfully reconstructs the attribute by extracting it directly from the reference image*

## 核心模块与公式推导

本方法的核心由四个功能模块构成，围绕“选择性属性提取与注入”这一目标协同工作。以下逐一阐述各模块的设计逻辑与关键公式。

### 模块一：VLM驱动的定制训练提示构建

该模块的目标是在训练开始前，从文本层面粗略排除非目标属性，为后续嵌入优化提供干净的语义条件。

给定参考图像 $x_0$ 和目标概念 $c$（如“颜色”），方法指示一个视觉语言模型（VLM）用一句话描述 $x_0$，但**明确排除**目标概念 $c$。随后，在该描述中插入一个概念专用短语（如 `[*]`），得到定制训练提示 $y_{\text{custom}}$。例如，若 $c$ 为“形状”，VLM 生成的描述可能为“一个具有[材质]纹理和[颜色]色调的物体”，从而在文本条件中预先剥离了形状信息。

这一设计改变了传统 Textual Inversion 使用简单提示（如 `A [*]`）的做法。其因果作用在于：当后续优化可学习标记嵌入时，由于 $y_{\text{custom}}$ 已明确描述了非目标属性，模型不再需要让标记嵌入去编码这些已知信息，从而降低了属性纠缠的程度。

### 模块二：蒸馏嵌入提取模块

这是本方法实现选择性属性分离的核心机制。传统 Textual Inversion 直接优化一个标记嵌入 $e_*$ 来重建整个参考图像，导致 $e_*$ 不可避免地吸收所有视觉属性（形状、材质、姿态等）。本方法提出**蒸馏嵌入** $h_{\text{[category]*}}$，其提取过程如下：

将占位符与类别词组成的短语 `[*] [category]` 送入文本编码器的 Transformer，其中 `[category]` 是目标概念 $c$ 的粗粒度类别描述词（如 `color`、`shape`、`material`）。Transformer 的自注意力机制使 `[category]` 对应的嵌入能够**选择性关注并从 `[*]` 中提取与该类别相关的视觉特征**，而忽略其他非目标属性。将此时 `[category]` 位置的前向嵌入记为 $h_{\text{[category]*}}$，即为蒸馏嵌入。

蒸馏嵌入的重建损失定义为：

$$\mathcal{L}_{\text{distill}} = \mathbb{E}_{\epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I}), t} \| x_{\theta}(\mathbf{x}_t, t, \text{Insert}(\tau(\tilde{y}_{\text{custom}}), h_{\text{[category]*}})) - \mathbf{x}_0 \|_2^2$$

其中，$\tau(\tilde{y}_{\text{custom}})$ 是将定制提示中 `[*]` 替换为占位符后的文本编码结果，$\text{Insert}(\cdot)$ 操作将蒸馏嵌入 $h_{\text{[category]*}}$ 插入到原 `[*]` 位置。模型仅通过蒸馏嵌入所携带的目标类别特征来重建图像，从而在结构上阻止了非目标属性的学习。

### 模块三：残差嵌入提取与正交约束

仅使用蒸馏嵌入进行训练会导致不稳定的优化，因为定制提示 $y_{\text{custom}}$ 无法穷尽描述所有非目标属性，未被描述的残余属性仍需要一个“出口”。为此，方法引入一个可学习的**残差嵌入** $h_{\text{residual}}$，将其预置在提示序列前端，用于吸收所有未被 $y_{\text{custom}}$ 覆盖的剩余视觉信息。

为防止 $h_{\text{residual}}$ 反过来学习目标概念，引入**余弦相似度损失**进行正交约束：

$$\mathcal{L}_{\text{cosine}} = \max\left(0, \frac{h_{\text{residual}} \cdot h_{\text{[category]*}}}{\|h_{\text{residual}}\| \|h_{\text{[category]*}}\|}\right)$$

该损失强制残差嵌入的方向与蒸馏嵌入保持非负余弦相似度的下界为零，即二者在特征空间中趋于正交，从而确保目标概念特征仅由蒸馏嵌入负责。

### 模块四：联合优化环路

最终的完整重建损失将残差嵌入和蒸馏嵌入同时纳入：

$$\mathcal{L}_{\text{recon}} = \mathbb{E}_{\epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I}), t} \| x_{\theta}(\mathbf{x}_t, t, \text{Insert}(\text{Prepend}(\tau(\tilde{y}_{\text{custom}}), h_{\text{residual}}), h_{\text{[category]*}})) - \mathbf{x}_0 \|_2^2$$

其中 $\text{Prepend}(\cdot)$ 将残差嵌入预置在文本编码序列前端。总损失为二者的加权组合：

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{recon}} + \lambda \mathcal{L}_{\text{cosine}}$$

在整个优化过程中，扩散模型参数 $\theta$ 保持冻结，仅优化蒸馏嵌入 $h_{\text{[category]*}}$ 和残差嵌入 $h_{\text{residual}}$。这一联合优化环路使得目标概念的特征被精准蒸馏到 $h_{\text{[category]*}}$ 中，非目标残余信息被 $h_{\text{residual}}$ 吸收，并通过正交约束实现二者的解耦。

### 补充图表

![[assets/figures/papers/paper_list_l2343_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Selectively_Extra/figures/005_Figure_4.jpg]]
*Figure 4: Comparison of the token and distilled embeddings. (a) When a standard token embedding e∗ is optimized using x0 from Fig. 3a, it naturally absorbs untargeted attributes from the reference image, such as the layout or camera focus. (b) By using our distilled embedding h[category]←∗ (e.g., hcolor←∗), the model structurally isolates the target features, successfully representing only the targeted concept while excluding undesired visual elements*

![[assets/figures/papers/paper_list_l2343_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Selectively_Extra/figures/006_Figure_5.jpg]]
*Figure 5: Visualization of token embeddings and distilled embeddings. When the phrase “[*] color” is passed through the text transformer, the*

## 实验与分析

### 定量评估与用户研究

本文构建了一个自定义的概念学习数据集，并在其上进行了系统的定量与定性评估。评估主要围绕两个核心维度展开：**概念相似性（Concept Similarity, CS）** 和 **概念排他性（Concept Exclusiveness, CE）** 。前者衡量生成图像中目标概念的还原程度，后者衡量非目标属性是否被成功排除。

在定量比较中（Figure 8），本文方法在 CS 与 CE 的综合得分上达到了最高。用户研究（Table 1）进一步验证了这一结论：在概念相似性与排他性方面，本文方法大幅优于大部分基线方法。在提示保真度（Prompt Fidelity）指标上，本文方法得分为 0.815，显著高于 TokenVerse 的 0.573，与 ProSpect 的 0.820 基本持平。

![[assets/figures/papers/paper_list_l2343_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Selectively_Extra/figures/010_Figure_8.jpg]]
*Figure 8: Quantitative comparison with baselines and ablation setups*

![[assets/figures/papers/paper_list_l2343_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Selectively_Extra/figures/009_Table_1.jpg]]
*Table 1: User study results. In prompt fidelity, we highlight the highest score in bold and the second-highest score with an underline*

### 消融实验

消融实验（Figure 6）系统验证了三个核心组件的必要性：

![[assets/figures/papers/paper_list_l2343_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Selectively_Extra/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative comparison of our method with ablation setups. When only*

1.  **定制训练提示（$y_{\text{custom}}$）的必要性**：当仅使用定制提示进行标准 Textual Inversion（TI w/ $y_{\text{custom}}$）而不采用蒸馏嵌入时，任何未在提示中显式描述的非目标属性（如布局、镜头焦点）仍会被标记嵌入自然吸收，导致属性分离失败。

2.  **蒸馏嵌入的核心作用**：对比标准标记嵌入与蒸馏嵌入（Figure 4），标准标记嵌入在优化过程中会不可避免地混入参考图像中的非目标视觉元素。而蒸馏嵌入在结构上阻止了非目标属性的学习，仅保留目标概念特征。

3.  **残差嵌入的稳定训练作用**：移除残差嵌入（Ours w/o $h_{\text{residual}}$）会导致训练不稳定，模型无法正确提取目标概念。残差嵌入通过捕获未被定制提示覆盖的剩余属性，并借助余弦相似度损失（Eq. (4)）强制其与蒸馏嵌入正交，防止其学习目标概念，从而稳定联合优化过程。

### 与零样本概念学习方法的对比

本文还将方法与大语言模型驱动的零样本概念学习方法进行了对比（Figure 9）。结果显示，**GPT Image 1** 和 **Gemini 2.5 Flash Image (Nano Banana)** 在提取隐性概念（如镜头角度、拍摄视角）时表现挣扎，并且倾向于将参考图像中的非目标属性一并复制到生成结果中。相比之下，本文方法能够更精确地隔离并迁移这类抽象视觉属性。

![[assets/figures/papers/paper_list_l2343_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Selectively_Extra/figures/011_Figure_9.jpg]]
*Figure 9: We provide additional concept learning results and comparison with GPT Image 1 and Gemini 2.5 Flash Image (Nano Banana)*

### 失败模式与局限性

尽管方法在属性解耦上表现出色，但仍存在若干局限：

- **单属性学习限制**：当前方法一次仅能优化学习一个属性级概念。虽然训练后可将多个独立学习的属性组合到同一个提示中，但无法在单次优化中同时提取多个纠缠属性。
- **对 VLM 生成质量的依赖**：属性分离效果高度依赖 VLM 生成的定制训练提示质量。若 VLM 未能完美描述所有非目标属性，可能导致部分残留属性混入蒸馏嵌入。
- **评估基准的规模**：评估数据集为自行构建，其规模和多样性有限，缺乏大规模标准化基准来验证方法的广泛泛化性。
- **特定领域的稳定性**：在生成人类图像等特定领域（尤其在使用 FLUX.1 dev 模型时）可能存在不稳定表现，需进一步验证与调整。

### 补充图表

![[assets/figures/papers/paper_list_l2343_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Selectively_Extra/figures/008_Figure_7.jpg]]
*Figure 7: Qualitative comparison with TokenVerse [15], U-VAP [45], ProSpect [48], OmniGen2 [44], and Textual Inversion (TI) [13]. We highlight the regions copied from the reference images with red rectangles*

## 方法谱系与知识库定位

### 1. 与基线方法的关系定位

本文所提出的选择性属性提取与注入方法，处于文本到图像生成中**概念学习（concept learning）**与**属性级解耦（attribute-level disentanglement）**的交叉地带。与现有工作的核心差异在于，它不试图学习整个对象，而是从单张高度纠缠的参考图像中精确分离并迁移**单个视觉属性**（如形状、材质、姿态、镜头角度）。

**相对于对象级概念学习方法：**
- **Textual Inversion (TI)**（Gal et al., arXiv 2022）通过优化单个标记嵌入来重建整个对象，但该嵌入天然会吸收参考图像中的所有视觉属性（包括布局、焦点等非目标属性）。Figure 4a 的对比直接证实，标准标记嵌入无法避免非目标属性的混入。本文的蒸馏嵌入机制正是针对这一瓶颈的结构性改进——通过将占位符与类别词（如 `[*] color`）共同送入文本编码器的 Transformer，使类别嵌入选择性地关注并蒸馏出目标特征，从嵌入空间层面阻断了非目标属性的学习路径。
- **ProSpect**（Zhang et al., TOG 2023）虽然具备属性感知能力，但其通过提示谱（prompt spectrum）进行个性化，本质上仍是对多个属性的联合建模。在用户研究的提示保真度（Prompt Fidelity）指标上，ProSpect 得分 0.820，本文方法得分 0.815，二者接近（Table 1），但在概念排他性（Concept Exclusivity）方面本文方法总体更优（Figure 8），表明本文在属性分离的纯粹性上具有优势。

**相对于属性级概念学习方法：**
- **TokenVerse**（Garibi et al., TOG 2025）通过优化调制参数实现属性级概念学习，是本文最直接的可比基线。用户研究中，TokenVerse 的提示保真度仅为 0.573，远低于本文的 0.815（Table 1）；在概念相似性与排他性的综合评估中，本文方法亦显著领先（Figure 8）。这一差距的因果机制在于：TokenVerse 缺乏结构性的非目标属性排除机制，而本文的定制训练提示（VLM 显式描述非目标属性）与蒸馏嵌入形成了双重过滤。

**相对于零样本概念学习方法：**
- **OmniGen2**（Wu et al., arXiv 2025）、**GPT Image 1**（OpenAI, 2025）和 **Gemini 2.5 Flash Image** 代表了无需训练的零样本概念学习范式。Figure 9 的定性对比显示，这些模型在提取隐含概念（如镜头角度、拍摄方式）时表现挣扎，且倾向于将非目标属性一并复制。本文方法的优势在于通过优化过程实现了对特定属性的精细解耦，但其代价是需要针对每个属性进行约 5000 次迭代训练。

### 2. 方法适用边界

**适用场景：**
- 从单张参考图像中提取**单一、可被类别词粗略描述**的视觉属性（如颜色、纹理、形状、姿态、镜头角度）。
- 需要将提取的属性注入到**灵活多变的背景环境**中，且不希望背景或布局受参考图像约束。
- 目标属性与参考图像中的其他属性高度纠缠，手动提示工程（Figure 2a）难以精确分离。

**不适用或需谨慎使用的场景：**
- **多属性同时学习**：当前方法一次仅能优化一个属性级概念。虽然训练后可将多个已学概念组合到一条提示中，但不能在单次优化中同时学习多个属性。这是方法架构层面的固有限制。
- **VLM 描述质量敏感**：属性分离效果依赖于视觉语言模型（VLM）生成的定制训练提示质量。若 VLM 未能准确或完整地描述所有非目标属性，未被描述的非目标属性仍可能通过残差嵌入或蒸馏嵌入的残留通道混入目标概念。这一依赖引入了外部模型偏差的风险。
- **特定领域的稳定性**：论文明确指出在生成人类图像等特定领域可能存在不稳定表现（尤其是使用 FLUX.1 dev 时），表明方法对内容域有一定敏感性。
- **复杂多对象场景**：当参考图像包含多个复杂对象或场景时，蒸馏嵌入能否精确定位到正确对象的属性，尚缺乏验证。

### 3. 局限与开放问题

**已确认的局限：**
1. **单属性学习瓶颈**：一次仅能学习一个属性级概念，无法同时优化多个属性。
2. **VLM 依赖链**：属性分离质量受 VLM 描述能力的上限约束，VLM 的偏见或错误会向下传播。
3. **评估基准局限**：实验基于自行构建的数据集，规模和多样性有限，缺乏大规模标准化基准来验证广泛泛化性。
4. **人类图像生成不稳定**：在特定领域（如使用 FLUX.1 dev 生成人脸）存在表现波动。

**开放问题与未来方向：**
1. **多属性联合学习**：能否扩展架构，在单次优化中同时学习多个属性而不需要后组合？这可能需要重新设计嵌入结构和损失函数，使得多个蒸馏嵌入在训练中保持正交。
2. **跨模态与时序扩展**：如何将选择性属性提取与注入推广到视频或其他模态，实现时序一致的属性迁移？这涉及时间维度的属性一致性约束设计。
3. **复杂场景下的属性定位**：当参考图像包含多个对象时，蒸馏嵌入能否自动定位到正确的对象属性？可能需要引入额外的空间注意力引导或对象检测先验。
4. **去 VLM 依赖**：是否能够设计完全无需 VLM 辅助的、基于模型内部表征的自动非目标属性过滤机制？例如，利用文本编码器自身的语义理解能力自动识别并排除非目标属性。
5. **与其他生成架构的集成**：该方法目前基于扩散模型（Stable Diffusion 3）实现，能否与基于流的模型或其他生成架构集成以进一步提升解耦能力，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Selectively_Extracting_and_Injecting_Visual_Attributes_into_Text_to_Image_Models.pdf]]