---
title: "SAM2Text: Towards Prompt-Free and Multi-Resolution Video Scene Text Segmentation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SAM2Text_Towards_Prompt_Free_and_Multi_Resolution_Video_Scene_Text_Segmentation.pdf
project_link: null
code_link: "https://github.com/insuper-zhang/SAM2Text/"
aliases:
- SAM2Text
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过LoRA低秩适应将SAM2有效迁移到文本域；引入自提示模块使模型无需外部提示即可自动聚焦文本区域；构建多分辨率掩码解码器以恢复高保真细节；设计短时记忆与Top‑K检索的两级记忆机制，降低计算开销并抑制掩码闪烁。
primary_logic: 面向视频文本分割的SAM2改造应以保留流式处理能力为前提，通过LoRA微调实现域适应，利用自提示消除对外部提示的依赖，通过多分辨率输出恢复笔画结构，并借助限定的短时记忆和历史Top‑K上下文实现稳定的跨帧传播。
claims:
- LoRA微调在保留SAM2流式处理能力的同时将模型适配到文本域。
- 自提示模块使模型能够自主生成文本特异性提示，无需外部输入。
- 含512×512和1024×1024分支的多分辨率解码器提升了掩码保真度。
- 增强记忆机制将注意力复杂度从O(T)降至O(L+K)，同时保持时间稳定性。
---

# SAM2Text: Towards Prompt-Free and Multi-Resolution Video Scene Text Segmentation

> [!tip] 核心洞察
> 面向视频文本分割的SAM2改造应以保留流式处理能力为前提，通过LoRA微调实现域适应，利用自提示消除对外部提示的依赖，通过多分辨率输出恢复笔画结构，并借助限定的短时记忆和历史Top‑K上下文实现稳定的跨帧传播。

| 字段 | 内容 |
|------|------|
| 中文题名 | SAM2Text：走向免提示和多分辨率视频场景文本分割 |
| 英文题名 | SAM2Text: Towards Prompt-Free and Multi-Resolution Video Scene Text Segmentation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_SAM2Text_Towards_Prompt-Free_and_Multi-Resolution_Video_Scene_Text_Segmentation_CVPR_2026_paper.html) · [Code](https://github.com/insuper-zhang/SAM2Text/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SAM2Text |
| Dataset | Total-Text, TextSeg, STS-SynthV, STS-RealV |

> [!tip] 效果简介
> - Total-Text 上，fgIOU 85.50 vs 84.59 (Hi-SAM) (+0.91)。
> - TextSeg 上，fgIOU / F-score 89.52 / 94.33。
> - STS-SynthV 上，fgIOU 93.25 vs 91.67 (Hi-SAM) (+1.58)。

## 概述

### 问题与瓶颈

视频场景文本分割（Video Scene Text Segmentation）旨在对视频帧中的文本区域进行像素级提取。尽管图像文本检测与分割数据集已相当丰富，视频文本分割的专用基准长期缺失（Figure 1）。更关键的瓶颈在于，通用视频分割模型**SAM2**直接迁移到文本域时面临三重挑战：其一，模型缺乏**文本特异性特征提取能力**，无法有效区分文字笔划与背景纹理；其二，原生输出分辨率仅256×256，不足以保留精细笔划和字符细节；其三，SAM2的记忆机制需存储全部历史帧，在长序列中注意力复杂度随帧数线性增长，且难以维持稳定的时间一致性。

### 核心方法

**SAM2Text**以保留SAM2的流式处理能力为前提，通过四个相互协同的模块实现从通用视频分割到视频文本分割的跨越：

| 模块 | 解决的问题 | 技术手段 |
|------|-----------|---------|
| **LoRA适应编码器** | 文本域适应 | 在图像编码器注入低秩增量（rank 16, alpha 32），冻结原有权重，仅训练轻量适配参数 |
| **自提示模块** | 消除外部提示依赖 | 四级深度可分离卷积生成空间注意力，经加权平均与交叉注意力自动产生文本定位提示令牌 |
| **多分辨率掩码解码器** | 恢复笔划细节 | 在原生256×256分支之上增加512×512和1024×1024两个独立上采样分支，各尺度通过动态卷积权重独立预测掩码 |
| **增强记忆模块** | 时间稳定性与计算效率 | 两层记忆机制：固定容量短时FIFO缓存维持近期上下文，Top‑K检索从长期记忆池筛选历史相关帧，将注意力复杂度从O(T)降至O(L+K) |

### 主要结果

在图像文本分割基准上，SAM2Text在**Total-Text**取得85.50% fgIOU，超越Hi-SAM（Ye et al., TPAMI 2025）0.91个百分点；在**TextSeg**上达到89.52% fgIOU和94.33% F-score。在视频基准上，合成数据集**STS-SynthV**上fgIOU达93.25%（+1.58%），真实场景数据集**STS-RealV**上fgIOU达80.71%（+2.37%），均显著优于Hi-SAM。

消融实验（Table 3）逐组件验证了贡献：LoRA适应带来+1.47% fgIOU提升，自提示模块追加+0.72%，多分辨率解码器再贡献+0.51%，增强记忆模块最终贡献+0.56%，四组件累计将fgIOU从SAM2.1基线的77.45%提升至80.71%。

### 方法定位

SAM2Text处于**视频分割基础模型域适应**与**场景文本分割**的交叉点。其技术路线区别于两类工作：一是**Hi-SAM**等基于SAM的层次文本分割方法，后者仍依赖外部提示且面向图像；二是**EAFormer**（Yu et al., ECCV 2024）、**TFT**（Yu et al., ACM MM 2023）等专用文本分割Transformer，这些模型不具备视频流式处理能力。SAM2Text通过“LoRA微调+自提示+多分辨率输出+高效记忆”的组合，首次实现了免提示、高保真、时间稳定的视频文本分割。

> **注意**：SAM2Text的消融基线（如+SAM2.1、+LoRA）在评估时使用了oracle提示（GT边界框），而完整模型在无提示设定下运行，因此报告的增益可能部分来自基线评估条件更严苛这一因素。合成数据训练的模型在真实复杂场景下的泛化边界、以及极长视频或严重运动模糊条件下的稳定性，仍需进一步验证。

## 背景与动机

### 视频场景文本分割的独特挑战

场景文本分割（Scene Text Segmentation, STS）要求在像素级别精确分离文本前景与背景，是文本检测、识别、编辑和擦除等下游任务的基础。然而，现有研究几乎全部集中在静态图像领域，视频场景文本分割长期处于空白状态。与图像分割相比，视频文本分割面临三重核心挑战：

1. **时序一致性**：视频中文本实例的掩码必须在帧间保持稳定，避免闪烁和抖动。
2. **流式处理能力**：实际应用（如增强现实、实时视频编辑）要求模型能够逐帧在线处理，而非依赖离线全局信息。
3. **精细结构保留**：文本笔划纤细、边缘锐利，低分辨率掩码会严重损失可读性和编辑质量。

### 现有方法的缺口

**数据集层面**：如 Figure 1 所示，现有文本检测与分割数据集在图像检测、视频检测和图像分割三个方向均已相对丰富，但视频场景文本分割数据集完全缺失。这一数据基础设施的空白直接制约了该方向的方法研发。

**方法层面**：通用视频分割模型 SAM2（Segment Anything Model 2）虽具备强大的流式视频分割能力，但直接应用于视频文本分割时暴露出三个根本性缺陷：

- **域不匹配**：SAM2 的图像编码器基于自然图像预训练，缺乏文本特异性特征提取能力，无法有效区分细粒度文本结构与复杂背景。
- **分辨率瓶颈**：SAM2 的掩码解码器仅输出 256×256 分辨率的掩码，对于需要保留笔划细节的文本分割任务而言，该分辨率严重不足。
- **记忆机制低效**：SAM2 的记忆模块存储全部历史帧信息，注意力复杂度随序列长度线性增长（$O(T)$），在长视频场景中计算开销高昂，且难以维持稳定的时间一致性。

已有的文本分割方法（如 **Hi-SAM**（Ye et al., TPAMI 2025）、**EAFormer**（Yu et al., ECCV 2024）、**TFT**（Yu et al., ACM MM 2023）等）均面向静态图像设计，缺乏时序建模和流式推理能力，无法直接迁移到视频场景。

### 本文动机与核心思路

针对上述瓶颈，本文提出 **SAM2Text** 框架，以 SAM2 的流式架构为基础，通过四个关键改造系统性地解决视频文本分割的核心挑战：

1. **LoRA 域适应**：以低秩适应（LoRA）替代全参数微调，在保留 SAM2 流式处理能力的前提下，高效地将模型适配到文本域。
2. **自提示机制**：引入自提示模块，使模型无需外部点、框等提示即可自动聚焦文本区域，实现免提示（prompt-free）的文本分割。
3. **多分辨率解码**：扩展掩码解码器，增加 512×512 和 1024×1024 两个独立输出分支，恢复高保真的文本笔划细节。
4. **增强记忆机制**：设计短时 FIFO 缓存与 Top-K 历史检索相结合的两级记忆模块，将注意力复杂度从 $O(T)$ 降至 $O(L+K)$，在降低计算开销的同时抑制掩码闪烁，保障跨帧时间一致性。

此外，为填补数据空白，本文构建了首个大规模视频场景文本分割数据集，包含合成数据集 **STS-SynthV**（1,410 段视频，147,852 帧）和真实场景数据集 **STS-RealV**（660 段视频，69,000 帧），为该方向的系统评估提供了基准。

## 核心创新

SAM2Text 的核心创新在于将通用视频分割模型 SAM2 改造为专用的视频场景文本分割器，同时完整保留其流式处理能力。这一改造围绕四个关键维度展开，分别对应 SAM2 在文本域暴露的结构性缺陷。

### 瓶颈诊断：SAM2 为何不适配视频文本分割

SAM2 在视频文本分割任务上存在三重根本性瓶颈。其一，**特征域不匹配**：SAM2 的图像编码器在自然图像上预训练，缺乏对文本笔划、字体结构等纹理特异性特征的提取能力。其二，**输出分辨率不足**：SAM2 的掩码解码器仅输出 256×256 分辨率的掩码，远不足以保留文本笔划的精细边缘和细节结构。其三，**时间一致性脆弱**：SAM2 的原始记忆机制存储全部历史帧，在长序列中注意力复杂度随帧数线性增长（$O(T)$），且难以抑制掩码闪烁。这三重瓶颈构成了 SAM2Text 设计的因果起点。

### 关键改造点：四个 Changed Slots

SAM2Text 在 SAM2 架构上进行了四处定向改造，每一项均对应上述瓶颈的因果干预。

**Slot 1：图像编码器微调策略——从冻结权重到 LoRA 低秩适应**

SAM2 的原始图像编码器采用冻结预训练权重的策略，无法适配文本域。SAM2Text 引入 **LoRA（Low-Rank Adaptation）** 对图像编码器进行参数高效微调，在注意力机制中的 QKV 投影和交叉注意力层注入低秩增量（rank=16, alpha=32.0）。其前向传播形式为：

$$\mathbf{y} = \mathbf{W} \mathbf{x} + \Delta \mathbf{W} \mathbf{x}$$

这一设计使模型在仅引入极少可训练参数的前提下，将特征空间从通用视觉域迁移至文本域，同时完全保留 SAM2 的流式推理能力。消融实验表明，LoRA 适配在 STS-RealV 上带来 fgIOU 提升 1.47%、F-score 提升 1.25%（相对 SAM2.1 基线）。

**Slot 2：提示生成方式——从外部提示依赖到自提示模块**

SAM2 依赖外部输入的点、框等提示来定位分割目标，这在视频文本分割场景中不切实际。SAM2Text 设计了**自提示模块（Self-Prompting Module）**，通过四级深度可分离卷积生成空间注意力图：

$$S = \mathrm{Sigmoid}(D_4(D_3(D_2(D_1(F)))))$$

随后通过空间注意力加权平均提取稀疏提示令牌：

$$\mathbf{P}_{b,l,:} = \frac{1}{H \cdot W} \sum_{h=1}^{H} \sum_{w=1}^{W} S_{b,l,h,w} F_{b,:,h,w}$$

提示令牌经自注意力和与增强图像特征的交叉注意力进一步精炼，最终作为掩码解码器的自动提示输入。该模块使模型在推理阶段完全免于外部提示，消融实验贡献 fgIOU 提升 0.72%、F-score 提升 0.64%。

**Slot 3：掩码输出分辨率——从单一 256×256 到三级多分辨率解码**

SAM2 原始掩码解码器仅输出 256×256 分辨率的掩码，难以保留文本笔划细节。SAM2Text 将解码器扩展为**多分辨率掩码解码器**，在原有 256×256 分支之上增加 512×512 和 1024×1024 两个独立上采样分支。各尺度分支通过动态卷积权重生成掩码预测：

$$M_s(x,y) = \langle w_s, F_s^{\mathrm{dec}}(x,y) \rangle$$

其中 $w_s = g_s(t)$ 为尺度特定的 MLP 从掩码令牌生成的动态卷积权重。三级输出级联后经上采样融合，显著提升了掩码保真度，消融实验贡献 fgIOU 提升 0.51%、F-score 提升 0.34%。

**Slot 4：记忆机制——从全量历史存储到短时缓存 + Top‑K 检索**

SAM2 的原始记忆机制存储全部历史帧，注意力复杂度为 $O(T)$，在长序列中计算开销高昂且易引入噪声。SAM2Text 提出**两级增强记忆机制**：第一级为固定容量 $L$ 的短时 FIFO 缓存，按先进先出策略更新：

$$\mathcal{M}_s^t = \mathrm{FIFO\text{-}Update}(\mathcal{M}_s^{t-1}, k_t, v_t, L)$$

第二级为基于相关性的 Top‑K 历史检索，从长期记忆池中按余弦相似度与质量分数的加权得分选取最相关的 $K$ 个条目：

$$r_j = \cos(q_t, k_j) + \lambda \cdot \mathrm{qual}_j$$

最终的有效记忆集由短时缓存和 Top‑K 检索结果共同构成，注意力复杂度降至 $O(L+K)$。这一设计在维持跨帧时间一致性的同时显著降低了计算开销，消融实验贡献 fgIOU 提升 0.56%、F-score 提升 0.24%。

### 创新逻辑链总结

四个 changed slots 构成一条因果链路：LoRA 适配解决特征域不匹配 → 自提示模块消除外部提示依赖 → 多分辨率解码器恢复笔划细节 → 增强记忆机制保障时间一致性。各组件增益在消融实验中呈累加效应，从 SAM2.1 基线（fgIOU 77.45%）逐级提升至完整 SAM2Text（fgIOU 80.71%），验证了每项改造的独立贡献与协同作用。

## 整体框架

SAM2Text 在 SAM2 的流式视频分割架构之上，围绕四个核心瓶颈进行改造：**文本域适应性不足**、**对外部提示的依赖**、**掩码分辨率受限**以及**长序列时间一致性退化**。框架整体保持 SAM2 的逐帧流式处理范式，通过 LoRA‑adapted 图像编码器、自提示模块、多分辨率掩码解码器和增强记忆模块四个组件串联，实现从原始视频帧到高保真文本掩码的端到端映射。

### 数据流与模块关系

对于每一个输入帧，处理流程如下：

1. **LoRA‑adapted 图像编码器** 接收当前帧，提取文本特异性特征。编码器主体沿用 SAM2 的预训练权重，仅通过 LoRA 低秩适应（rank 16, alpha 32）对注意力机制中的 QKV 投影和交叉注意力层进行参数高效微调，使得特征表示从通用视觉域迁移到文本域，同时完整保留原生流式推理能力。前向传播形式为：

   $$\mathbf{y} = \mathbf{W} \mathbf{x} + \Delta \mathbf{W} \mathbf{x}$$

   其中 $\Delta \mathbf{W}$ 为低秩增量矩阵。

2. **自提示模块** 从编码器输出的多尺度特征图 $F$ 中自动生成文本位置的稀疏提示令牌，无需任何外部点、框或掩码输入。模块首先通过四级深度可分离卷积生成空间注意力图：

   $$S = \mathrm{Sigmoid}(D_4(D_3(D_2(D_1(F)))))$$

   随后利用该注意力图对特征进行加权池化，提取稀疏提示令牌 $\mathbf{P}$：

   $$\mathbf{P}_{b,l,:} = \frac{1}{H \cdot W} \sum_{h=1}^{H} \sum_{w=1}^{W} S_{b,l,h,w} F_{b,:,h,w}$$

   提示令牌依次经过自注意力与交叉注意力（与经 $3\times3$ 卷积 + GELU 增强的局部特征 $F'$ 交互），生成最终的文本感知提示表示 $\mathbf{P}''$，作为后续掩码解码的条件信号。

3. **多分辨率掩码解码器** 接收自提示模块输出的提示令牌与编码器的多尺度特征，在三个独立分支上分别预测 $256\times256$、$512\times512$ 和 $1024\times1024$ 分辨率的掩码 logits。每个分支通过尺度特定的 MLP 从掩码令牌生成动态卷积权重 $w_s$，再与解码器特征 $F_s^{\mathrm{dec}}$ 做内积得到掩码预测：

   $$M_s(x, y) = \langle w_s, F_s^{\mathrm{dec}}(x, y) \rangle$$

   相比 SAM2 原生的单一 $256\times256$ 输出，多分辨率设计能有效恢复文本笔划的精细结构。

4. **增强记忆模块** 负责跨帧传播文本掩码信息以维持时间一致性。模块采用两层记忆设计（详见 Figure 3）：
   - **短时记忆**：固定容量 $L$ 的 FIFO 缓存 $\mathcal{M}_s^t$，存储最近若干帧的键值对，更新方式为：

     $$\mathcal{M}_s^t = \mathrm{FIFO\text{-}Update}(\mathcal{M}_s^{t-1}, k_t, v_t, L)$$

   - **Top‑K 历史检索**：从有界长期记忆池 $\mathcal{M}_g$ 中，按余弦相似度与质量分数的加权得分检索最相关的 $K$ 个历史条目：

     $$r_j = \cos(q_t, k_j) + \lambda \cdot \mathrm{qual}_j$$

   短时缓存与 Top‑K 检索结果合并为有效记忆集 $\mathcal{U}_t$，交叉注意力仅在该集合上运算，将注意力复杂度从 SAM2 原始的 $O(T)$ 降至 $O(L+K)$，同时有效抑制长序列中的掩码闪烁。

### 训练与推理特性

整个框架以端到端方式训练，采用 AdamW 优化器（学习率 $3\times10^{-5}$）、batch size 1 和 bfloat16 混合精度，在合成数据集 STS-SynthV 上训练 80 个 epoch。推理时，SAM2Text 保持逐帧流式处理能力：每帧依次经过编码器 → 自提示 → 多分辨率解码 → 记忆更新，无需访问未来帧，适合在线视频场景。

> **注意**：消融实验中的早期变体（如仅加 LoRA 的 SAM2.1、无自提示版本）在评估时使用了 oracle 提示（GT 边界框），而完整 SAM2Text 在完全免提示的自动设定下运行，因此 Table 3 中各组件的实际增益可能被低估——基线条件比完整模型更宽松。

### 补充图表

![[assets/figures/papers/paper_list_l2414_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SAM2Text_Towards/figures/002_Figure_2.jpg]]
*Figure 2: The overview of our proposed SAM2Text*

## 核心模块与公式推导

SAM2Text 在 SAM2 基座上引入四个关键改造模块，协同解决视频场景文本分割中的域适应、免提示、精细掩码和时间一致性难题。

### 3.1 LoRA 低秩适应

为将 SAM2 图像编码器高效迁移至文本域，同时完整保留其流式处理能力，采用 LoRA 对注意力层进行参数高效微调。对原始权重矩阵 $\mathbf{W} \in \mathbb{R}^{d \times d}$，前向传播引入低秩增量：

$$\mathbf{y} = \mathbf{W}\mathbf{x} + \Delta\mathbf{W}\mathbf{x}$$

其中 $\Delta\mathbf{W} = \mathbf{B}\mathbf{A}$，$\mathbf{B} \in \mathbb{R}^{d \times r}$，$\mathbf{A} \in \mathbb{R}^{r \times d}$，秩 $r=16$，缩放系数 $\alpha=32$。LoRA 仅作用于 QKV 投影和交叉注意力层，冻结其余参数，使模型在仅引入极少可训参数的前提下获得文本特异性特征提取能力。

### 3.2 自提示模块

自提示模块使模型摆脱对外部点、框等提示的依赖，自主生成文本区域的稀疏提示令牌。该模块包含三个子步骤。

**空间注意力生成。** 对图像编码器输出的多尺度特征图 $F \in \mathbb{R}^{B \times C \times H \times W}$，通过四级深度可分离卷积生成空间注意力权重：

$$S = \mathrm{Sigmoid}(D_4(D_3(D_2(D_1(F)))))$$

其中 $D_i$ 为第 $i$ 级深度可分离卷积层，$S \in \mathbb{R}^{B \times L \times H \times W}$，$L$ 为提示令牌数量。

**稀疏提示令牌提取。** 以空间注意力为权重，对特征图进行全局加权池化，获得 $L$ 个稀疏提示令牌：

$$\mathbf{P}_{b,l,:} = \frac{1}{H \cdot W} \sum_{h=1}^{H} \sum_{w=1}^{W} S_{b,l,h,w} \, F_{b,:,h,w}$$

**提示令牌精炼。** 先通过 $3 \times 3$ 卷积与 GELU 激活增强图像局部纹理：

$$F' = \mathrm{GELU}(\mathrm{Conv2D}(F))$$

随后对提示令牌依次施加自注意力和与增强特征的交叉注意力，并辅以残差连接与层归一化：

$$\mathbf{P}' = \mathrm{LayerNorm}(\mathbf{P} + \mathrm{Dropout}(\mathrm{SelfAttn}(\mathbf{P})))$$

$$\mathbf{P}'' = \mathrm{LayerNorm}\big(\mathbf{P}' + \mathrm{Dropout}(\mathrm{CrossAttn}(\mathbf{P}', F'))\big)$$

最终 $\mathbf{P}''$ 作为文本特异性提示送入掩码解码器。

### 3.3 多分辨率掩码解码器

SAM2 原生解码器仅输出 $256 \times 256$ 分辨率的掩码，不足以保留文本笔划的精细结构。SAM2Text 在原有架构上扩展两个独立上采样分支，分别输出 $512 \times 512$ 和 $1024 \times 1024$ 分辨率的掩码 logits。

对每个尺度 $s \in \{256, 512, 1024\}$，从掩码令牌 $t$ 通过尺度特定的 MLP $g_s$ 生成动态卷积权重：

$$w_s = g_s(t) \in \mathbb{R}^{C_s}$$

将 $w_s$ 与对应尺度的解码器特征图 $F_s^{\mathrm{dec}}$ 逐位置做内积，得到该尺度的掩码预测：

$$M_s(x, y) = \langle w_s, F_s^{\mathrm{dec}}(x, y) \rangle$$

三个分支独立预测，训练时以多尺度真值掩码分别监督，推理时取 $1024 \times 1024$ 输出作为最终高保真掩码。

### 3.4 增强记忆机制

为在长视频序列中维持时间一致性并控制计算开销，设计两层记忆机制，将交叉注意力的复杂度从 $O(T)$ 降至 $O(L + K)$。

**短时记忆。** 维护一个固定容量 $L$ 的 FIFO 缓存 $\mathcal{M}_s^t$，存储最近 $L$ 帧的键值对：

$$\mathcal{M}_s^t = \mathrm{FIFO\text{-}Update}(\mathcal{M}_s^{t-1}, k_t, v_t, L)$$

**Top-K 历史检索。** 维护一个长期记忆池 $\mathcal{M}_g$，对当前帧查询 $q_t$，基于余弦相似度与质量分数计算各历史条目的相关性得分：

$$r_j = \cos(q_t, k_j) + \lambda \cdot \mathrm{qual}_j$$

其中 $\mathrm{qual}_j$ 为第 $j$ 个记忆条目的预测质量分数，$\lambda$ 为平衡系数。选取得分最高的 $K$ 个条目与短时缓存合并，构成有效记忆集 $\mathcal{U}_t$，解码器的交叉注意力仅在该集合上运算。此设计既保留了近期帧的时序连贯性，又通过检索机制回溯关键历史上下文，有效抑制掩码闪烁。

### 补充图表

![[assets/figures/papers/paper_list_l2414_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SAM2Text_Towards/figures/003_Figure_3.jpg]]
*Figure 3: Two-tier memory: Top-K retrieval from the bounded long-term memory pool*

## 实验与分析

### 实验设置

SAM2Text 基于 SAM2.1 进行构建，图像编码器采用 **LoRA** 低秩适应微调，秩设为 16，alpha 为 32.0，应用于 QKV 投影和交叉注意力层。模型使用 AdamW 优化器训练 80 个 epoch，学习率 3e-5，batch size 为 1，采用 bfloat16 混合精度训练。

### 图像场景文本分割基准

在 Total-Text 和 TextSeg 两个图像场景文本分割数据集上，SAM2Text 与 **Hi-SAM**（Ye et al., TPAMI 2025）、**SegFormer**（Xie et al., NeurIPS 2021）、**EAFormer**（Yu et al., ECCV 2024）、**TFT**（Yu et al., ACM MM 2023）、**DeepLabV3**（Chen et al., ECCV 2018）和 **HRNet**（Wang et al., TPAMI 2020）等方法进行了对比。如 Table 1 所示，SAM2Text 在 Total-Text 上达到 85.50% fgIOU，比 Hi-SAM 高出 0.91%；在 TextSeg 上达到 89.52% fgIOU 和 94.33% F-score，在所有对比方法中取得最优。

![[assets/figures/papers/paper_list_l2414_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SAM2Text_Towards/figures/005_Table_1.jpg]]
*Table 1: Comparison on Total-Text and TextSeg. Best in bold*

### 视频场景文本分割基准

在作者构建的两个视频数据集上，如 Table 2 所示，SAM2Text 在合成数据集 STS-SynthV 上取得 93.25% fgIOU 和 94.83% F-score，分别超出 Hi-SAM 1.58% 和 0.68%；在真实场景数据集 STS-RealV 上取得 80.71% fgIOU 和 87.45% F-score，分别超出 Hi-SAM 2.37% 和 1.53%。真实场景下的提升幅度更大，表明多分辨率解码和增强记忆机制对复杂背景下的文本分割尤为关键。

![[assets/figures/papers/paper_list_l2414_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SAM2Text_Towards/figures/006_Table_2.jpg]]
*Table 2: Performance comparison on video scene text segmentation datasets. Best results are highlighted in bold*

### 消融实验

Table 3 展示了在 STS-RealV 上的逐组件消融结果，以 SAM2.1 基线（使用 oracle 提示，即 GT 边界框）为起点：

![[assets/figures/papers/paper_list_l2414_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SAM2Text_Towards/figures/007_Table_3.jpg]]
*Table 3: Ablation study of the proposed components on the STS-RealV dataset*

- **+LoRA 微调**：fgIOU 从 77.45% 提升至 78.92%（+1.47%），F-score 从 84.98% 提升至 86.23%（+1.25%），验证了参数高效域适应的有效性。
- **+自提示模块**：fgIOU 进一步提升至 79.64%（+0.72%），F-score 至 86.87%（+0.64%），证明模型在免除外部提示后仍能有效定位文本区域。
- **+多分辨率解码器**：fgIOU 增至 80.15%（+0.51%），F-score 至 87.21%（+0.34%），表明高分辨率分支（512×512 和 1024×1024）恢复了更多笔划细节。
- **+增强记忆模块**：最终 fgIOU 达到 80.71%（+0.56%），F-score 达到 87.45%（+0.24%），验证了两级记忆机制对跨帧时间一致性的贡献。

> ⚠️ **公平性说明**：以上消融中，SAM2.1 基线及早期变体（+LoRA、不含自提示的版本）均使用 oracle 提示进行评估，而完整 SAM2Text 工作在免提示的自动设定下。因此报告的性能增益部分可能源于基线评估条件更宽松这一因素，实际增益可能略低于报告值。

### 失败模式与局限性

尽管 SAM2Text 在整体指标上表现优异，论文指出了以下局限：

1. **域间隙问题**：合成数据（STS-SynthV）与真实场景（STS-RealV）之间仍存在显著的域间隙。仅依赖合成数据训练可能影响模型对真实复杂背景（如光照剧烈变化、非刚性形变文本）的泛化能力。
2. **极端条件未验证**：论文未在极长视频（数分钟以上）或严重运动模糊、大面积遮挡等极端条件下系统验证记忆模块的稳定性，增强记忆机制在长程传播中的退化行为尚不明确。
3. **密集文本与低对比度场景**：自提示模块在密集文本排列或低对比度场景下的失败案例未详尽分析，可能存在漏检或错误合并相邻文本实例的风险。此部分需要人工进一步验证。

### 关键图表结论

- **Table 1**：SAM2Text 在图像文本分割基准上全面超越 Hi-SAM 等现有方法，验证了 LoRA 域适应和多分辨率解码在静态图像上的有效性。
- **Table 2**：在视频数据集上，SAM2Text 对 Hi-SAM 的优势在真实场景下更为显著，表明增强记忆机制有效抑制了掩码闪烁问题。
- **Table 3**：四个组件均带来正向增益，其中 LoRA 微调贡献最大（+1.47% fgIOU），增强记忆模块在已有较高基线（80.15% fgIOU）上仍提供 0.56% 的增量，证明了各模块的互补性。

### 补充图表

![[assets/figures/papers/paper_list_l2414_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SAM2Text_Towards/figures/001_Figure_1.jpg]]
*Figure 1: Overview of existing datasets [1–11] for text detection and segmentation: rich for image/video detection and image segmentation, but missing for video segmentation*

## 方法谱系与知识库定位

### 与现有方法的关系

**SAM2Text** 建立在 **SAM2**（Segment Anything Model 2）的流式视频分割框架之上，其核心改造策略是保留原生流式处理能力的同时，通过四个关键模块将通用分割模型迁移到视频场景文本域。这一设计思路与近年将基础模型适配到文本分割的路线一脉相承，但在适配深度和自动化程度上形成了明显差异。

在图像场景文本分割领域，**Hi-SAM**（Ye et al., TPAMI 2025）是 SAM2Text 最直接的参照对象。Hi-SAM 同样基于 SAM 架构，通过层次化提示实现文本分割，但仍需外部提示（如点、框）来定位文本区域。SAM2Text 的自提示模块从根本上消除了这一依赖，使模型能够在免提示条件下自动聚焦文本。此外，Hi-SAM 仅输出单一分辨率掩码，而 SAM2Text 的多分辨率解码器（256×256、512×512、1024×1024）在笔画保真度上具有结构性优势。

更广泛地，场景文本分割领域的主流方法可分为两类：基于语义分割的通用架构和专门设计的文本感知模型。**SegFormer**（Xie et al., NeurIPS 2021）、**DeepLabV3**（Chen et al., ECCV 2018）和 **HRNet**（Wang et al., TPAMI 2020）属于前者，它们依赖像素级分类范式，缺乏对文本实例级别结构的显式建模。**EAFormer**（Yu et al., ECCV 2024）和 **TFT**（Yu et al., ACM MM 2023）属于后者，分别通过边缘感知和文本聚焦机制增强分割精度，但均为图像级方法，不具备时序建模能力。SAM2Text 的差异化定位在于：它是首个将视频流式处理、免提示自动分割和多分辨率输出统一在一个框架内的方法。

从技术谱系看，SAM2Text 的 LoRA 微调策略遵循了参数高效迁移学习的主流范式，其自提示模块借鉴了稀疏注意力机制在视觉任务中的应用思路，而两层记忆机制（短时 FIFO 缓存 + Top‑K 历史检索）则是对 SAM2 原始记忆模块的定向优化——将注意力复杂度从 $O(T)$ 降至 $O(L + K)$，在保持时间一致性的同时显著降低了长序列推理的计算开销。

### 适用边界

SAM2Text 的设计前提是视频中存在可辨识的场景文本实例，其适用边界可从以下几个维度界定：

1. **文本形态**：模型针对的是场景文本（scene text），即自然场景中出现的印刷或手写文字，而非文档扫描文本。自提示模块通过空间注意力生成文本位置提示，其有效性依赖于文本区域与背景之间存在一定的视觉对比度。

2. **视频长度**：增强记忆模块采用固定容量的短时缓存（容量 $L$）和 Top‑K 检索机制，理论上支持任意长度视频的流式处理。但论文仅在常规长度的视频片段上验证，未在数分钟以上的极长视频或需要跨场景记忆的场景下测试。

3. **分辨率需求**：多分辨率解码器最高支持 1024×1024 的掩码输出，对于需要更高保真度的应用（如超大尺寸招牌文字）可能存在上限。

4. **训练数据依赖**：模型在合成数据集 STS-SynthV 上训练，尽管在真实数据集 STS-RealV 上展现了可观的泛化能力（fgIOU 80.71%，F-score 87.45%），但合成数据与真实场景之间的域间隙仍构成适用边界——在复杂光照、严重运动模糊或极端遮挡条件下，性能可能下降。

### 局限与开放问题

**已识别的局限**：

- **域间隙问题**：仅依赖合成数据训练可能影响对真实复杂背景的泛化能力。论文未探索域自适应或半监督学习策略来弥合这一差距。
- **极端条件验证不足**：论文未在极长视频（数分钟以上）或严重运动模糊、遮挡等条件下系统验证记忆模块的稳定性。两层记忆机制在长程依赖和灾难性遗忘方面的表现尚不明确。
- **自提示模块的失败模式**：在密集文本或低对比度场景下，自提示模块可能存在漏检或错误合并的问题，但论文未提供详尽的失败案例分析。
- **公平性评估的偏差**：消融实验中的基线 SAM2.1 和早期变体（如 +LoRA、无自提示）使用 oracle 提示（GT 边界框），而完整 SAM2Text 在免提示条件下运行。这意味着报告的部分性能增益可能源于基线评估条件更宽松，而非模型能力的纯粹提升。这一公平性问题需要手动验证。

**开放问题**：

- 自提示模块能否泛化到非文本的细粒度分割任务（如 logo、符号），从而扩展 SAM2Text 的应用范围？
- 两层记忆机制中的 Top‑K 检索质量分数 $\mathrm{qual}_j$ 的具体计算方式及其对检索鲁棒性的影响，论文未充分展开。
- 多分辨率分支之间是否存在互补或冗余，能否通过尺度自适应融合进一步压缩计算开销？
- 在实时视频流场景下，1024×1024 分支的推理延迟是否满足部署要求，论文未提供推理速度的基准测试。

## 原文 PDF

![[paperPDFs/CVPR_2026/SAM2Text_Towards_Prompt_Free_and_Multi_Resolution_Video_Scene_Text_Segmentation.pdf]]
