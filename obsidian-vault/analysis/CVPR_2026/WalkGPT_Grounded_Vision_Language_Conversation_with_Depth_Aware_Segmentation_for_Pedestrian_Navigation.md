---
title: "WalkGPT: Grounded Vision-Language Conversation with Depth-Aware Segmentation for Pedestrian Navigation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/WalkGPT_Grounded_Vision_Language_Conversation_with_Depth_Aware_Segmentation_for_Pedestrian_Navigation.pdf
project_link: null
code_link: null
aliases:
- WalkGPT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过多尺度查询投影器（MSQP）聚合多层级视觉特征，以及校准文本投影器（CTP）和区域对齐损失实现精确的语言-视觉对齐，WalkGPT得以在统一框架内同时完成接地对话、分割掩码预测和物体级深度估计。
primary_logic: 行人导航需要深度感知的像素级接地；通过引入结构化令牌（<SEG>, <distance>等），将分割、深度和语言推理集成到单一自回归生成过程中，模型无需用户额外输入即可隐式学习空间关系并输出深度感知的接地导航指导。
claims:
- 零样本基线在所有指标上失败且完全无法预测深度，而WalkGPT在微调后大幅领先，13B模型将mIoU提升10%以上（20.16 vs 18.10），深度准确率提升25%以上（48.95 vs 39.00）。
- 将MSQP替换为简单MLP导致METEOR从43.01降至39.50，mIoU从20.16降至17.40，Depth Acc.从48.95降至43.39，表明多尺度视觉聚合至关重要。
- WalkGPT在RefCOCO/RefCOCO+/RefCOCOg的引用表达分割基准上均达到最优，验证了其精细的像素级接地能力（RefCOCO val 76.2%，RefCOCOg val(U) 72.6%）。
- PAVE (Segmentation) 上 mIoU = 20.16 (13B)
---

# WalkGPT: Grounded Vision-Language Conversation with Depth-Aware Segmentation for Pedestrian Navigation

> [!tip] 核心洞察
> 行人导航需要深度感知的像素级接地；通过引入结构化令牌（<SEG>, <distance>等），将分割、深度和语言推理集成到单一自回归生成过程中，模型无需用户额外输入即可隐式学习空间关系并输出深度感知的接地导航指导。

| 字段 | 内容 |
|------|------|
| 中文题名 | WalkGPT：面向行人导航的深度感知分割的接地视觉-语言对话 |
| 英文题名 | WalkGPT: Grounded Vision-Language Conversation with Depth-Aware Segmentation for Pedestrian Navigation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.10703) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | WalkGPT |
| Dataset | PAVE, RefCOCO val |

> [!tip] 效果简介
> - PAVE (Segmentation) 上，mIoU 20.16 (13B) vs PixelLM-FT: 18.10 (+2.06 (+11.4%))。
> - PAVE (Depth) 上，Depth Accuracy 48.95 (13B) vs OMG-LLaVA-FT: 39.02 (+9.93 (+25.5%))。
> - RefCOCO val 上，RES @0.5IoU 76.2 vs LISA: 74.1 (+2.1)。

## 概要

行人导航对话系统要求模型在理解场景语义的同时，具备**像素级接地**和**空间深度推理**能力——不仅要识别“前方有什么”，还要回答“它离我多远、是否构成障碍”。现有视觉-语言大模型（LVLMs）尽管在通用对话上表现优异，却普遍缺乏这两项能力：它们生成的描述无法精确锚定到图像区域，且难以提供可靠的距离信息，导致**对象幻觉**和**空间误判**，无法满足视障人士或复杂户外环境下的安全导航需求。

针对这一瓶颈，WalkGPT 提出将**分割、深度估计和语言推理统一到一个自回归生成框架**中。其核心机制是通过引入结构化令牌（`<SEG>`、`<distance>`、`<assessment>` 等），使模型在生成接地对话的同时，隐式学习空间关系并输出深度感知的导航指导，无需用户额外输入或外部深度头。

在架构层面，WalkGPT 的关键创新体现在两个模块：

- **多尺度查询投影器（MSQP）**：跨尺度聚合视觉编码器特征，将细粒度细节与全局场景上下文压缩为紧凑的图像令牌，供 LLM 进行语义推理。消融实验表明，将 MSQP 替换为简单 MLP 会导致对话质量（METEOR -3.51）、分割精度（mIoU -2.76）和深度准确率（-5.56）全面下降（Table 5）。
- **校准文本投影器（CTP）与区域对齐损失**：将 LLM 输出的 `<SEG>` 令牌映射到视觉空间，并通过 InfoNCE 对比损失强制其与对应图像区域对齐，从而驱动分割解码器生成精确掩码。

实验验证了 WalkGPT 的有效性：在 PAVE 接地导航对话基准上，13B 模型的分割 mIoU 达到 20.16，较大幅领先微调后的 PixelLM（18.10，+11.4%）；深度准确率 48.95，显著超越 OMG-LLaVA（39.02，+25.5%）。在 RefCOCO/RefCOCO+/RefCOCOg 引用表达分割基准上，WalkGPT 同样取得最优结果（RefCOCO val 76.2%，RefCOCOg val(U) 72.6%），验证了其精细的像素级接地能力。值得注意的是，所有零样本基线均无法预测深度，而 WalkGPT 通过自回归结构化令牌学习，成功赋予了模型物体级深度推理能力。

**方法定位**：WalkGPT 属于像素接地视觉-语言对话模型，与 **GLAMM**、**LISA**、**PixelLM**、**GSVA**、**OMG-LLaVA** 等同期工作同处一个技术谱系，但其独特之处在于将深度感知纳入了统一的接地对话框架。

**主要局限**：深度估计目前仅为物体级文本描述，缺乏像素级深度图，绝对相对误差仍较高（AbsRel ~70%）；模型对透明物体（围栏）和强反射表面（建筑玻璃）容易产生误判；泛化性仅在 PAVE 数据集上验证，对光照、天气等变化的鲁棒性尚不明确。



视觉-语言模型（Vision-Language Models, VLMs）近年来在图像描述、视觉问答等任务上取得了显著进展。然而，当面向行人导航这一安全关键场景时，现有模型暴露出根本性缺陷：**缺乏像素级接地能力与深度空间推理**。具体而言，主流的大视觉-语言模型（Large Vision-Language Models, LVLMs）仅能在图像级生成描述性文本，无法将语言输出精确绑定到图像中的具体区域，更无法提供物体距离等三维空间信息。这导致两类严重问题——**对象幻觉**（模型提及不存在的物体或错误描述物体属性）和**不可靠的空间理解**（无法判断障碍物的实际距离与可通行性），使得此类模型在行人导航、无障碍辅助等场景中不具备实用安全性。

现有方法对此瓶颈的应对存在明显缺口。一方面，以 **LISA**、**PixelLM**、**GLAMM** 为代表的像素接地LVLM虽然能够根据文本指令生成分割掩码，但它们**不包含深度推理模块**，无法输出距离感知的导航指导。另一方面，**OMG-LLaVA**、**GSVA** 等视觉接地对话模型虽支持区域指代，但其视觉投影器通常采用简单MLP架构，缺乏跨尺度特征聚合能力，导致细粒度空间信息丢失。更关键的是，**零样本基线模型在深度估计任务上完全失败**（Table 1中所有零样本模型的深度指标均为N/A），说明现有LVLM架构本身不具备隐式距离感知能力，必须通过专门设计的结构化输出机制和训练范式才能赋予模型这一能力。

上述缺口直接催生了本文的核心动机：**构建一个能在统一自回归框架内同时完成接地对话、分割掩码预测和物体级深度估计的像素接地LVLM**。这一目标要求模型满足三个关键条件：（1）视觉编码器能够为语言生成和掩码预测提供共享的多尺度特征；（2）文本到视觉的映射必须保持语义一致性，确保 `<SEG>` 令牌能准确定位目标区域；（3）深度信息需以结构化令牌（如 `<distance>`）的形式嵌入语言生成过程，无需额外的密集深度监督。WalkGPT正是围绕这些条件设计，通过 **Multi-Scale Query Projector (MSQP)** 聚合多层级视觉特征、**Calibrated Text Projector (CTP)** 结合区域对齐损失实现精确的语言-视觉映射，以及结构化令牌体系连接分割、深度与语言推理，从而填补了现有LVLM在深度感知接地导航上的空白。



## 核心方法与创新机理

WalkGPT 的核心创新在于将**像素级接地、物体级深度估计与视觉-语言对话**统一到一个自回归生成框架中，解决了现有 LVLM 在行人导航场景中缺乏空间理解与深度推理的根本瓶颈。其关键创新点体现在以下三个 changed slots 上：

### 1. 多尺度查询投影器（MSQP）→ 替代简单 MLP 投影器

现有 LVLM（如 LLaVA）通常采用单层 MLP 将视觉编码器特征线性映射到语言空间，这导致细粒度空间信息的丢失。WalkGPT 提出的 **Multi-Scale Query Projector (MSQP)** 跨多个空间层级聚合视觉特征，将像素编码器的多尺度嵌入压缩为一组紧凑的图像令牌 $\mathbf{V}_{\mathrm{proj}}$，供 LLM 使用。

MSQP 的工作机制为：首先将 SAM ViT-H 像素编码器嵌入 $\mathbf{Z}$ 线性投影到工作维度 $d_{\mathrm{proj}}=1024$，得到 $\mathbf{F} = \mathbf{Z} \mathbf{W}_{\mathrm{proj}}$；然后在每个尺度 $s$ 上通过交叉注意力对门控令牌进行内容加权混合，输出 $\mathbf{o}_i^s = \sum_j \alpha_{ij} \mathbf{x}_j^s$。这种设计使模型能同时保留细粒度细节和全局场景上下文。

**因果证据**：消融实验（Table 5）显示，将 MSQP 替换为简单 MLP 导致 METEOR 从 43.01 降至 39.50（−3.51），mIoU 从 20.16 降至 17.40（−2.76），Depth Acc. 从 48.95 降至 43.39（−5.56）。即使仅移除多尺度聚合而保留单尺度，METEOR 仍下降 1.41，Depth Acc. 下降 4.25。这表明多尺度聚合对语言生成和深度推理均至关重要。

### 2. 校准文本投影器（CTP）+ 区域对齐损失 → 替代单层线性投影

传统方法将 LLM 输出的 `<SEG>` 令牌通过单层线性投影映射到视觉空间以驱动分割解码器，但这种方式难以保持语义与空间位置的精确对应。WalkGPT 的 **Calibrated Text Projector (CTP)** 将每个降维后的向量扩展为结构化的校准子嵌入集合，保留细粒度语义，从而提升分割掩码预测的空间一致性。

CTP 由 **Region Alignment Loss**（InfoNCE 对比损失）监督。具体而言，对每个 `<SEG>` 令牌 $\mathbf{t}_{b,m}$，通过交叉注意力计算其与视觉特征 $\mathbf{Z}_b$ 之间的注意力权重 $\boldsymbol{\pi}$，聚合 top-K 关注的视觉特征形成正样本区域嵌入 $\mathbf{z}_{b,m}^+$。InfoNCE 损失将 CTP 投影嵌入拉向正样本区域嵌入，同时推远负样本：

$$\mathcal{L}_{\mathrm{NCE}} = -\frac{1}{BM} \sum_{b,m} \log \frac{\exp(a_{b,m})}{\exp(a_{b,m}) + \sum_{k \in K^-} \exp(r_{b,mk})}$$

这一设计使语言接地与视觉定位形成闭环，确保生成的 `<SEG>` 令牌精确指向图像中的对应区域。

### 3. 结构化深度令牌 → 替代外部深度头或零深度能力

现有 LVLM 要么完全不具备深度感知能力，要么依赖独立的外部深度估计模块。WalkGPT 通过引入结构化 `<distance>` 令牌，使模型在自回归生成对话的过程中**隐式学习并输出物体级深度估计**，无需密集深度图监督。

模型在生成导航指导时，自然地将 `<distance>` 令牌与对应的 `<SEG>` 令牌关联，输出如“前方约 3 米处有障碍物”的描述。深度准确率采用乘性容忍度判别：预测深度 $d_i^{\mathrm{pred}}$ 落在真值 $d_i^{\mathrm{gt}}$ 的 0.5 至 2 倍范围内视为正确。

**因果证据**：消融实验（Table 5）表明，移除 `<distance>` 令牌使 Depth Acc. 骤降 10.18（从 48.95 降至 38.77），但对分割 mIoU 影响极小（仅降 0.15）。这证明深度推理能力是通过结构化令牌设计内化到自回归生成过程中的，而非依赖分割质量的副产品。零样本基线（Table 1）完全无法预测深度（Depth metrics 为 N/A），而 WalkGPT 微调后 Depth Acc. 达 48.95，领先最强基线 OMG-LLaVA-FT 达 25.5%（48.95 vs. 39.02）。

### 创新协同：统一训练目标

上述三个创新模块通过加权联合损失协同优化：

$$\mathcal{L}_{\mathrm{total}} = \alpha_1 \mathcal{L}_{\mathrm{CE}} + \alpha_2 \mathcal{L}_{\mathrm{seg}} + \alpha_3 \mathcal{L}_{\mathrm{NCE}}$$

其中 $\mathcal{L}_{\mathrm{CE}}$ 为自回归语言生成交叉熵损失，$\mathcal{L}_{\mathrm{seg}}$ 为分割损失（Dice + BCE），$\mathcal{L}_{\mathrm{NCE}}$ 为区域对齐对比损失。这种设计使对话生成、像素接地和深度推理在单一自回归过程中相互增强，无需用户提供额外输入即可输出深度感知的接地导航指导。



WalkGPT 的整体架构围绕“统一像素编码器 + 多尺度视觉聚合 + 校准文本投影 + 结构化令牌生成”这一核心设计展开，将语言对话、分割掩码预测和物体级深度估计整合进单一的自回归生成框架。

### 架构总览

如图 2a 所示，WalkGPT 的推理流程可概括为四个阶段：

1. **视觉编码**：输入图像首先通过一个共享的 SAM ViT-H 像素编码器提取多层级视觉特征。该编码器同时服务于语言生成和掩码预测两条路径，避免了多编码器带来的特征不一致问题。
2. **多尺度特征聚合**：多尺度查询投影器（MSQP）将像素编码器的多层级特征压缩为一组紧凑的图像令牌 $\mathbf{V}_{\mathrm{proj}}$，送入大语言模型（LLM）进行多模态推理。
3. **接地对话生成**：LLM 以自回归方式生成包含结构化令牌（`<SEG>`、`<distance>`、`<assessment>`、`<p>`）的文本响应。其中 `<SEG>` 令牌作为文本提示，驱动后续的掩码预测。
4. **掩码与深度预测**：校准文本投影器（CTP）将 LLM 输出的 `<SEG>` 令牌映射到视觉空间，生成校准后的提示嵌入；SAM 像素解码器依据这些嵌入预测分割掩码，同时模型自回归输出物体级的 `<distance>` 深度估计。

### 关键模块关系

三个核心模块之间形成紧密的协同关系：

- **MSQP → LLM**：MSQP 通过跨尺度的交叉注意力机制，将像素编码器在不同空间层级上的特征聚合为语义对齐的图像令牌。消融实验表明，将 MSQP 替换为简单 MLP 会导致 METEOR 下降 3.51、mIoU 下降 2.76、Depth Acc. 下降 5.56（Table 5），证实了多尺度聚合对下游任务的关键支撑作用。
- **LLM → CTP → 像素解码器**：LLM 生成的 `<SEG>` 令牌经 CTP 扩展为结构化的子嵌入，再由区域对齐损失（InfoNCE）约束其与视觉空间中对应区域的一致性。这一“文本提示→视觉嵌入→掩码预测”的通路是 WalkGPT 实现像素级接地的核心机制。
- **结构化令牌串联**：`<SEG>` 令牌连接语言与分割，`<distance>` 令牌引入深度推理，`<assessment>` 和 `<p>` 令牌承载可访问性分析。这些结构化令牌使模型无需外部深度头或独立分割模块即可在统一的生成过程中完成多任务输出。

### 训练目标

WalkGPT 的联合训练目标为三个损失函数的加权和：

$$\mathcal{L}_{\mathrm{total}} = \alpha_1 \mathcal{L}_{\mathrm{CE}} + \alpha_2 \mathcal{L}_{\mathrm{seg}} + \alpha_3 \mathcal{L}_{\mathrm{NCE}}$$

其中 $\mathcal{L}_{\mathrm{CE}}$ 为标准自回归交叉熵损失，用于接地对话生成；$\mathcal{L}_{\mathrm{seg}}$ 为 Dice + BCE 的组合分割损失，监督掩码预测；$\mathcal{L}_{\mathrm{NCE}}$ 为对比对齐损失，将 CTP 投影嵌入拉向正样本区域嵌入、推远负样本，强化文本-视觉的空间对应关系。三者联合优化使模型在对话质量、分割精度和深度估计三个维度上同步提升。

### 补充图表

![[assets/figures/papers/paper_list_l2184_https_arxiv_org_abs_2603_10703/figures/002_Figure_2.jpg]]
*Figure 2: Overview of WalkGPT for grounded navigation guidance. (a) Overall framework. (b) The Multi-Scale Query Projector (MSQP), which aggregates multi-level visual features into spatially aligned image tokens for language reasoning. (c) The Calibrated Text Projector (CTP), guided by the proposed Region Alignment Loss, maps \<SEG> tokens into the visual space. Structured tokens (\<SEG>, \<distance>, \<assessment>, \<p>) link language generation with segmentation and depth reasoning*



WalkGPT 的核心架构围绕三个关键设计展开：**多尺度查询投影器（MSQP）** 实现跨尺度视觉特征聚合、**校准文本投影器（CTP）** 配合区域对齐损失实现精确的语言-视觉接地、以及**结构化令牌**将分割与深度推理统一到自回归生成过程中。

### 多尺度查询投影器（MSQP）

现有 LVLM 通常采用简单 MLP 将视觉编码器输出映射到语言空间，但这种方式丢失了细粒度空间信息，难以支撑像素级接地。MSQP 的设计目标是将 SAM ViT-H 像素编码器的多层级特征压缩为一组紧凑的图像令牌 $\mathbf{V}_{\mathrm{proj}}$，同时保留从局部细节到全局场景的多尺度上下文。

MSQP 的工作流程分为两步。首先，像素编码器嵌入 $\mathbf{Z}$ 通过线性投影映射到工作维度 $d_{\mathrm{proj}} = 1024$：

$$\mathbf{F} = \mathbf{Z} \mathbf{W}_{\mathrm{proj}} \in \mathbb{R}^{B \times L \times d_{\mathrm{proj}}}$$

随后，在多个空间尺度 $s$ 上执行交叉注意力，通过可学习的门控令牌对内容进行加权混合：

$$\mathbf{o}_i^s = \sum_j \alpha_{ij} \mathbf{x}_j^s$$

其中 $\alpha_{ij}$ 为注意力权重，$\mathbf{x}_j^s$ 为尺度 $s$ 下的视觉特征。通过跨多个空间层级进行注意力聚合，MSQP 将细粒度细节与全局场景上下文压缩为紧凑令牌集，供 LLM 进行语言推理。

消融实验（Table 5）证实了 MSQP 的关键作用：将 MSQP 替换为简单 MLP 投影器导致 METEOR 从 43.01 降至 39.50（−3.51）、mIoU 从 20.16 降至 17.40（−2.76）、Depth Acc. 从 48.95 降至 43.39（−5.56）；仅移除多尺度聚合（使用单一尺度）也使 METEOR 下降 1.41、Depth Acc. 下降 4.25。

### 校准文本投影器（CTP）与区域对齐损失

当 LLM 生成 `<SEG>` 令牌时，需要将其映射回视觉空间以驱动 SAM 像素解码器进行掩码预测。简单的单层线性投影容易导致令牌多样性丧失和语义漂移。CTP 通过将每个缩减向量扩展为一组 $K_{\mathrm{bank}}$ 个校准嵌入，在保持细粒度语义的同时建立更精确的空间对应关系。

区域对齐损失通过对比学习强化 CTP 投影嵌入与视觉区域之间的对应。给定第 $b$ 个样本的第 $m$ 个 `<SEG>` 令牌 $\mathbf{t}_{b,m}$，计算其与视觉特征之间的注意力权重以定位相关空间区域：

$$\mathbf{q} = \mathbf{t}_{b,m} \mathbf{W}_q, \quad \mathbf{K}_b = \mathbf{Z}_b \mathbf{W}_k, \quad \mathbf{V}_b = \mathbf{Z}_b \mathbf{W}_v,$$
$$\boldsymbol{\pi} = \mathrm{softmax}\left(\frac{\mathbf{K}_b \mathbf{q}^\top}{\sqrt{d_k}}\right) \in \mathbb{R}^{L}$$

取 top-$K$ 注意力权重聚合为正样本区域嵌入：

$$\mathbf{z}_{b,m}^+ = \mathbf{W}_o \left( \sum_{i \in \mathcal{T}_K} \alpha_i \mathbf{v}_{b,i} \right) \in \mathbb{R}^{d_{\mathrm{vis}}}$$

基于 InfoNCE 的对比损失将 CTP 投影嵌入 $\hat{\mathbf{e}}_{b,m}$ 拉向正样本区域嵌入 $\mathbf{z}_{b,m}^+$，同时推远负样本：

$$\mathcal{L}_{\mathrm{NCE}} = -\frac{1}{BM} \sum_{b,m} \log \frac{\exp(a_{b,m})}{\exp(a_{b,m}) + \sum_{k \in K^-} \exp(r_{b,mk})}$$

其中 $a_{b,m} = \langle\hat{\mathbf{e}}_{b,m}, \mathbf{z}_{b,m}^+\rangle / \tau$，$r_{b,mk} = \langle\hat{\mathbf{e}}_{b,m}, \hat{\mathbf{z}}_k^-\rangle / \tau$，$\tau$ 为温度参数。该损失确保 `<SEG>` 令牌的文本表示与对应视觉区域在嵌入空间中紧密对齐。

### 结构化令牌与深度推理

WalkGPT 引入四类结构化令牌将语言生成与分割、深度推理统一到自回归框架中：`<SEG>` 触发分割掩码预测、`<distance>` 输出物体级深度估计、`<assessment>` 给出可访问性判断、`<p>` 标记段落结构。模型以自回归方式逐令牌生成响应，当遇到 `<SEG>` 令牌时，CTP 将其映射为提示嵌入驱动像素解码器预测掩码；当遇到 `<distance>` 令牌时，直接输出物体级距离数值，无需密集深度监督。

### 总训练目标

WalkGPT 的最终训练目标为三个互补损失的加权和：

$$\mathcal{L}_{\mathrm{total}} = \alpha_1 \mathcal{L}_{\mathrm{CE}} + \alpha_2 \mathcal{L}_{\mathrm{seg}} + \alpha_3 \mathcal{L}_{\mathrm{NCE}}$$

其中 $\mathcal{L}_{\mathrm{CE}}$ 为标准自回归交叉熵损失，条件于文本和投影图像令牌：

$$\mathcal{L}_{\mathrm{CE}} = -\frac{1}{S} \sum_{s=1}^{S} \log P(y_s \mid y_{<s}, x, \mathbf{V}_{\mathrm{proj}})$$

$\mathcal{L}_{\mathrm{seg}}$ 为分割损失，组合 Dice 损失与二元交叉熵损失；$\mathcal{L}_{\mathrm{NCE}}$ 为上述区域对齐对比损失。三者联合优化对话生成质量、掩码预测精度和视觉-文本对齐一致性。

消融实验（Table 5）表明：移除 `<distance>` 令牌主要损害深度预测（Depth Acc. −10.18），但对分割影响极小（mIoU 仅降 0.15）；冻结 LLM（移除 LoRA）导致所有指标骤降（METEOR −7.81，mIoU −2.36，Depth Acc. −8.74），验证了多模态微调对于接地导航任务的必要性。



## 实验与关键发现

### 4.1 实验设置

**数据集与划分。** WalkGPT在PAVE数据集上进行训练和评估。PAVE包含91个行人视角视频会话，其中85个会话（约8.5k帧）用于训练，6个会话（约600帧）用于验证。数据集中存在严重的类别不平衡——stairs、obstacle等安全关键类别的出现频次远低于road、sidewalk等常见类别，可能影响少数类的分割和深度估计性能。

**评估指标。** 接地导航对话生成从三个维度评估：文本质量采用CIDEr和METEOR；分割质量采用AP50、mIoU和Recall；深度估计采用Depth Accuracy（预测值落在真值的0.5至2倍范围内视为正确）和AbsRel（绝对相对误差）。引用表达分割（RES）基准采用cIoU和gIoU指标。

**公平性保障。** 所有对比方法均使用相同的训练/验证划分，并统一扩展了相同的结构化令牌接口（<SEG>, <distance>等）。零样本模型（†标记）的深度指标列为N/A，因为它们在未微调时完全无法产生深度估计。

### 4.2 接地导航对话生成主结果

Table 1展示了PAVE验证集上的综合对比。核心发现如下：

**零样本基线完全失败。** 所有零样本LVLM（GLAMM†、LISA†、PixelLM†、GSVA†、OMG-LLaVA†）在深度估计上完全无法输出有效预测，验证了现有模型缺乏深度推理能力这一关键瓶颈。

**WalkGPT全面领先微调基线。** 在文本生成质量上，WalkGPT-13B的METEOR达到43.01，CIDEr达到125.41，均优于PixelLM-FT（METEOR 41.62, CIDEr 118.30）和OMG-LLaVA-FT（METEOR 39.50, CIDEr 110.20）。在分割质量上，13B模型将mIoU从PixelLM-FT的18.10提升至20.16（+11.4%），AP50从26.30提升至28.10。在深度估计上，Depth Accuracy从OMG-LLaVA-FT的39.02跃升至48.95（+25.5%），AbsRel从0.72降至0.68。

**性能增益来源。** 这些提升源于WalkGPT的统一像素编码器配合MSQP和CTP：MSQP提供细粒度的多尺度视觉令牌，CTP在区域对齐损失的引导下维持语言生成与分割掩码之间的接地一致性。7B模型同样展现出显著优势，验证了方法的可扩展性。

### 4.3 引用表达分割基准

Table 2展示了在RefCOCO/RefCOCO+/RefCOCOg三个标准RES基准上的对比。WalkGPT在所有数据集上均达到最优：RefCOCO val cIoU 76.2%（超过LISA的74.1%），RefCOCO+ val 69.8%，RefCOCOg val(U) 72.6%。这一结果验证了WalkGPT精细的像素级接地能力不仅限于导航场景，在通用引用表达分割任务上同样具有竞争力。

### 4.4 幻觉与对象覆盖分析

Table 4报告了CHAIRi（幻觉率）和Cover（对象覆盖率）指标。WalkGPT的CHAIRi显著低于GLAMM和LISA等基线，表明结构化令牌和区域对齐损失有效抑制了对象幻觉。同时Cover指标更高，说明模型能更全面地描述场景中的可访问性相关对象。

### 4.5 消融实验

Table 5的系统性消融揭示了各设计组件的关键作用：

**MSQP的核心地位。** 将MSQP替换为简单MLP投影器（类似LLaVA方案）导致全面性能崩溃：METEOR从43.01降至39.50（-3.51），mIoU从20.16降至17.40（-2.76），Depth Acc.从48.95降至43.39（-5.56）。进一步移除MSQP的多尺度聚合（仅使用单一尺度）同样造成显著下降：METEOR -1.41，mIoU -0.86，Depth Acc. -4.25。这证实了跨尺度视觉特征聚合对语言生成和空间理解的双重重要性。

**结构化令牌的分工。** 移除<distance>令牌主要损害深度预测（Depth Acc. -10.18至38.77），但对分割影响极小（mIoU仅降0.15至20.01），验证了深度估计与分割在令牌层面的解耦设计。移除<assessment>令牌则主要影响文本生成质量。

**LLM微调的必要性。** 冻结LLM（移除LoRA）导致所有指标骤降：METEOR -7.81至35.20，mIoU -2.36至17.80，Depth Acc. -8.74至40.21。这表明即使有强大的视觉编码器和投影器，LLM的适应性微调仍是多模态接地推理不可或缺的环节。

**CTP与区域对齐损失。** 移除CTP（退化为简单线性投影）或移除InfoNCE区域对齐损失均导致分割和深度指标的明显下降，证实了校准文本投影和对比对齐对维持精确视觉-语言空间对应的重要性。

### 4.6 失败模式分析

Figure 5和Figure 7展示了WalkGPT的两类典型失败案例：

**强反射表面误判。** 当建筑玻璃幕墙产生强烈的路面反射时，WalkGPT将反射中的路面纹理误判为物理障碍物，尽管实际路径完全可通行。这暴露了模型对镜面反射和间接光照的脆弱性。

**透明障碍物漏判。** 面对透明围栏，WalkGPT错误地推断围栏后方区域为开放可通行路径，被围栏的透明性和后方清晰视野所误导。这在行人导航场景中构成严重安全隐患。

**深度估计精度局限。** 尽管Depth Accuracy指标相对基线有显著提升，但绝对相对误差（AbsRel）仍约70%，表明自回归物体级深度预测的绝对精度尚不足以支持精细的避障决策。模型仅输出物体级文本描述（如“约3米”），缺乏像素级深度图。

### 4.7 定性结果

Figure 4展示了PAVE验证集上的定性输出。WalkGPT能够从单张行人视角图像生成包含<assessment>、<distance>、<SEG>和<p>结构化令牌的接地对话，同时输出分割掩码和深度感知的距离估计。Figure 6进一步展示了非道路场景（不平坦地形、密集植被）下的泛化能力，模型能识别有限的可行走表面并提供相应的可访问性评估。

### 补充图表

![[assets/figures/papers/paper_list_l2184_https_arxiv_org_abs_2603_10703/figures/005_Table_1.jpg]]
*Table 1: Performance comparison on grounded navigation conversation generation. Models marked with † are zero-shot; “-FT” indicates fine-tuned on PAVE. Depth metrics for zero-shot models are listed as N/A because they fail to produce any depth estimations. Best results are bold-faced*

![[assets/figures/papers/paper_list_l2184_https_arxiv_org_abs_2603_10703/figures/006_Table_2.jpg]]
*Table 2: Performance comparison on the referring expression segmentation (RES) benchmark. Best results are bold-faced*

![[assets/figures/papers/paper_list_l2184_https_arxiv_org_abs_2603_10703/figures/008_Table_5.jpg]]
*Table 5: Ablation study examining the impact of different design choices in WalkGPT*

![[assets/figures/papers/paper_list_l2184_https_arxiv_org_abs_2603_10703/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative results of WalkGPT on the PAVE validation set. Given a scene image, WalkGPT generates grounded conversations together with segmentation masks and depth-aware distance estimates, reflecting its understanding of accessibility and spatial context. Additional examples are provided in the Appendix*

![[assets/figures/papers/paper_list_l2184_https_arxiv_org_abs_2603_10703/figures/010_Table_4.jpg]]
*Table 4: Comparison of hallucination (CHAIRi) and object coverage (Cover) scores across LVLMs on the PAVE dataset*

![[assets/figures/papers/paper_list_l2184_https_arxiv_org_abs_2603_10703/figures/007_Table_3.jpg]]
*Table 3: Segmentation performance on PAVE compared with representative vision-only segmentation benchmarks*

![[assets/figures/papers/paper_list_l2184_https_arxiv_org_abs_2603_10703/figures/011_Figure_6.jpg]]
*Figure 6: Additional qualitative results of WalkGPT on the PAVE validation set for off-road scenes. Examples illustrate the model’s ability to handle unstructured outdoor environments with uneven terrain, dense vegetation, and limited walkable surfaces*

![[assets/figures/papers/paper_list_l2184_https_arxiv_org_abs_2603_10703/figures/009_Figure_5.jpg]]
*Figure 5: Failure case study on PAVE. WalkGPT misinterprets strong road reflections on the building fac¸ade as physical obstacles, producing incorrect guidance even though the path itself is fully accessible. Part of the image is blurred for privacy*

![[assets/figures/papers/paper_list_l2184_https_arxiv_org_abs_2603_10703/figures/012_Figure_7.jpg]]
*Figure 7: Another failure case on PAVE. WalkGPT incorrectly infers that the fenced area provides an open and accessible path, misled by the transparency of the fence and the clear view of the space behind it*

![[assets/figures/papers/paper_list_l2184_https_arxiv_org_abs_2603_10703/figures/014_Figure_9.jpg]]
*Figure 9: Per-class sample occurrence counts across all semantic categories (including background class 0). The x-axis denotes class IDs and the y-axis indicates the number of samples containing each class*



## 定位与知识库关联

### 任务定位与基线关系

WalkGPT 定位于**像素级接地视觉-语言对话**与**行人可访问性导航指导**的交叉点。其直接对比的基线可分为三类：

**像素接地对话基线**：**GLAMM**、**PixelLM**、**GSVA**、**OMG-LLaVA** 和 **Sa2VA** 均支持视觉接地对话，但缺乏深度感知能力。从 Table 1 可见，这些模型在零样本设定下完全无法预测深度（Depth metrics 为 N/A），即使经 PAVE 微调后（如 PixelLM-FT 的 mIoU 18.10，OMG-LLaVA-FT 的 Depth Acc. 39.02），其空间理解仍局限于二维平面，无法为行人提供距离感知的安全指导。

**推理分割基线**：**LISA** 在引用表达分割（RES）任务上表现强劲（RefCOCO val 74.1%），但 WalkGPT 在同一基准上达到 76.2%（Table 2），且在 RefCOCO+ 和 RefCOCOg 上均取得最优，验证了 MSQP 多尺度聚合和 CTP 区域对齐带来的精细接地能力。

**视觉-only 分割基线**：Table 3 将 WalkGPT 与 SAM、OneFormer 等纯视觉分割模型在 PAVE 上对比，尽管 WalkGPT 作为 LVLM 并非专为分割设计，其 mIoU（20.16）仍展现出竞争力，说明统一框架并未牺牲分割质量。

### 核心差异机制

WalkGPT 与上述基线的本质差异在于三个技术槽位：

1. **视觉投影器**：基线普遍采用简单 MLP（如 LLaVA 架构），WalkGPT 以 **Multi-Scale Query Projector (MSQP)** 替代，跨尺度聚合 SAM ViT-H 的多层级特征。消融实验（Table 5）证实，将 MSQP 替换为 MLP 导致 METEOR 从 43.01 降至 39.50（-3.51），mIoU 从 20.16 降至 17.40（-2.76），Depth Acc. 从 48.95 降至 43.39（-5.56），说明多尺度视觉聚合对三项任务均有决定性影响。

2. **文本到视觉映射**：基线使用单层线性投影，WalkGPT 引入 **Calibrated Text Projector (CTP)** 将 `<SEG>` 令牌扩展为结构化子嵌入，并辅以 **Region Alignment Loss**（InfoNCE 对比损失），将文本嵌入显式拉向正样本区域嵌入。这一设计确保了语言接地与分割掩码之间的空间一致性，是 RES 基准领先的关键。

3. **深度估计**：基线或完全无深度能力，或依赖外部深度头。WalkGPT 通过结构化 `<distance>` 令牌实现**自回归物体级深度预测**，无需密集深度监督。Table 5 显示，移除 `<distance>` 令牌使 Depth Acc. 骤降 10.18（48.95 → 38.77），但对分割影响极小（mIoU 仅降 0.15），表明深度推理与分割接地在架构上可解耦。

### 适用边界

**有效场景**：WalkGPT 在 PAVE 数据集覆盖的行人视角城市场景中表现良好，包括道路、人行道、楼梯、障碍物等典型可访问性要素的接地与深度估计。Figure 4 的定性结果显示，模型能生成连贯的接地导航对话，同时输出分割掩码和距离描述。

**已知失效模式**：
- **透明/反射表面误判**：Figure 5 展示了建筑玻璃幕墙反射路面导致的误判——模型将反射误解为物理障碍物。Figure 7 则显示透明围栏使模型错误推断围栏后方为可通过路径。这表明模型缺乏对镜面反射和透明材质的物理理解。
- **绝对深度误差较大**：尽管 Depth Acc.（乘性容忍度 0.5×–2×）达到 48.95，但 AbsRel 约 70%，意味着物体级深度描述的绝对精度不足以支撑精细避障。
- **类别不平衡**：PAVE 数据集中 stairs、obstacle 等安全关键类出现频次远低于 road、sidewalk（Figure 9），可能导致少数类的分割和深度估计性能不可靠。

**泛化局限**：所有实验仅在 PAVE 数据集上进行（85 个会话训练，6 个会话验证），对光照变化、天气条件（雨雪、夜间）、季节更替以及不同地理环境的泛化能力未经实证。模型在 CityNav、GOAT 等其他导航基准上的跨域性能仍是开放问题。

### 开放问题

1. **深度估计精度提升**：当前物体级文本深度描述无法替代像素级深度图。能否引入轻量深度解码器或与单目深度估计模型（如 Depth Anything）协同，在不破坏统一架构的前提下提供密集深度？

2. **时序一致性**：PAVE 源自视频会话（SANPO 数据集），但 WalkGPT 逐帧独立推理。引入时序信息（跨帧特征融合或视频 LLM）有望缓解运动模糊（Figure 8a）带来的分割噪声，并提升跨帧的空间一致性。

3. **鲁棒性扩展**：如何通过数据增强（合成反射、透明物体、极端光照）或物理感知预训练，提升模型对透明围栏、镜面反射、低光照等 adversarial 条件的鲁棒性？

4. **安全关键类精度**：针对 stairs、obstacle 等低频但高风险类别，是否需要重采样、焦点损失或类特定评估协议来确保导航指导的安全性？



## 原文 PDF

![[paperPDFs/CVPR_2026/WalkGPT_Grounded_Vision_Language_Conversation_with_Depth_Aware_Segmentation_for_Pedestrian_Navigation.pdf]]
