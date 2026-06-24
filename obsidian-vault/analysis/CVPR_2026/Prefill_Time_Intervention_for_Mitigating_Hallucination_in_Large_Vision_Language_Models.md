---
title: Prefill-Time Intervention for Mitigating Hallucination in Large Vision-Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Prefill_Time_Intervention_for_Mitigating_Hallucination_in_Large_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/huaiyi66/PTI"
aliases:
- PTIP
- PTIMHLVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在预填充阶段（prefill stage）对初始KV缓存进行一次性、模态感知的干预，通过解耦的键（Key）和值（Value）转向向量，分别增强物体为中心的注意力并过滤背景噪声。
primary_logic: Transformer中的KV缓存不仅存储上下文，还通过注意力机制主动塑造后续生成；利用键的“注意何处”与值的“聚合什么”解耦特性，以物体-背景对比信号提取方向，精准修正预填充表征，避免解码阶段的错误传播。
claims:
- DTI方法如VISTA在减少幻觉频率的同时加剧了残余幻觉的严重性，表现为PSH（雪球幻觉比例）升高（Figure 2）。
- PTI在LLaVA-1.5的Greedy解码下将CHAIR_S从47.4降至15.4（↓32.0），CHAIR_I从13.7降至5.4（↓8.3）（Table 1）。
- PTI在POPE基准上的平均F1分数为82.85，优于VISTA的81.98和VTI的81.64（Table 2）。
- 消融分析表明，视觉值缓存干预（object vs. background）对减少幻觉贡献最大，而视觉键缓存干预缓解了全局视觉注意力衰减（Figure 5）。
---

# Prefill-Time Intervention for Mitigating Hallucination in Large Vision-Language Models

> [!tip] 核心洞察
> Transformer中的KV缓存不仅存储上下文，还通过注意力机制主动塑造后续生成；利用键的“注意何处”与值的“聚合什么”解耦特性，以物体-背景对比信号提取方向，精准修正预填充表征，避免解码阶段的错误传播。

| 字段 | 内容 |
|------|------|
| 中文题名 | 预填充阶段干预以缓解大型视觉语言模型中的幻觉 |
| 英文题名 | Prefill-Time Intervention for Mitigating Hallucination in Large Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.25642) · [Code](https://github.com/huaiyi66/PTI) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Prefill-Time Intervention (PTI) |
| Dataset | CHAIR, POPE, MME, AMBER |

> [!tip] 效果简介
> - CHAIR 上，CHAIR_S / CHAIR_I 15.4 / 5.4 vs 47.4 / 13.7 (↓32.0 / ↓8.3)；CHAIR_S / CHAIR_I 20.6 / 7.0 vs 39.6 / 12.0 (↓19.0 / ↓5.0)。
> - POPE 上，Average F1-score 82.85 vs 81.23 (+1.62)；Average Accuracy 85.69 vs 83.69 (+2.00)。
> - MME 上，Total Score 671.6 vs 651.6 (+20.0)。

## 概述

大型视觉-语言模型（LVLM）在图像描述与视觉问答中常产生与视觉输入不一致的“幻觉”内容。现有解码时间干预（DTI）方法在每一步解码中持续施加统一的转向向量，虽能降低幻觉频率，却无法从源头修正错误的视觉-语言表征，反而导致残余幻觉的严重性上升——即“雪球幻觉”（snowball hallucination）加剧（Figure 2）。这一瓶颈揭示了在解码之前对初始表征进行一次性、精准干预的必要性。

本文提出**预填充时间干预（Prefill-Time Intervention, PTI）**，将干预时机从解码阶段前移至预填充阶段，仅对初始KV缓存执行一次模态感知的转向。核心洞察在于：Transformer中的KV缓存不仅存储上下文，还通过注意力机制主动塑造后续生成；利用键（Key）决定“注意何处”与值（Value）决定“聚合什么”的解耦特性，可以从物体-背景对比信号中提取独立的方向，分别增强物体为中心的注意力并过滤背景噪声。

PTI包含两个阶段（Figure 3）：
- **阶段一**：在MSCOCO对比样本上，分别从视觉和文本模态的正负KV缓存差异中提取解耦的键转向向量和值转向向量。
- **阶段二**：将这些方向按模态注入下游输入的预填充KV缓存，随后以标准自回归解码生成响应。

在幻觉基准上，PTI展现出显著且一致的增益。在LLaVA-1.5的Greedy解码下，CHAIR_S从47.4降至15.4（↓32.0），CHAIR_I从13.7降至5.4（↓8.3）（Table 1）；POPE平均F1分数达到82.85，优于VISTA（81.98）与VTI（81.64）（Table 2）。消融分析表明，视觉值缓存中物体vs.背景的对比对减少幻觉贡献最大，而视觉键缓存干预缓解了生成过程中的全局视觉注意力衰减（Figure 5）。PTI引入的延迟开销极低（所有模型均低于×1.02），且可与解码阶段方法（PAI、VISTA）组合进一步提升性能（Table 6），具备良好的跨模型迁移能力。

**方法定位**：PTI属于训练无关的推理时干预方法，与基于对比解码（如VCD）、Beam Search优化（如OPERA）以及解码时间隐藏状态干预（如VISTA、PAI、VTI）等路线正交。其核心创新在于将干预对象从粗粒度的隐藏状态升级为细粒度、解耦的KV缓存，并将干预时机从多步解码压缩为预填充阶段的一次性操作，从而在源头阻断错误的累积传播。

## 背景与动机

大型视觉语言模型（LVLMs）在图像描述和视觉问答等任务中取得了显著进展，但“物体幻觉”——即模型生成与图像内容不符的物体描述——仍是阻碍其可靠部署的核心障碍。现有的无训练缓解方法主要分为两类：对比解码策略和基于转向向量的解码时间干预。对比解码方法（如 **VCD**、**OPERA**）通过放大视觉信息与语言先验之间的差异来减少幻觉，但通常仅支持特定的解码策略，提升幅度有限。解码时间干预方法（如 **PAI**、**VTI**、**VISTA**）则在解码的每一步持续向隐藏状态施加统一的转向向量，试图引导模型远离幻觉。

然而，这类解码时间干预存在一个被忽视的根本性缺陷：**雪球幻觉**。如图 Figure 2 的定量分析所示，以 VISTA 为代表的解码时间干预方法虽然在 CHAIR 指标上降低了幻觉的总体频率，却同时加剧了残余幻觉的严重性——表现为 PSH（雪球幻觉比例）的升高。这一现象揭示了解码时间干预的因果瓶颈：在解码阶段持续施加统一的转向向量，无法从源头修正初始的视觉-语言表征错误，反而导致初始错误在自回归生成过程中不断累积和放大，形成“雪球”效应。

这一瓶颈的根源在于 Transformer 架构中 KV 缓存的独特角色。KV 缓存不仅被动存储上下文信息，更通过注意力机制主动塑造后续生成的每一步。解码时间干预在错误已经嵌入缓存之后才进行修正，犹如在雪球已开始滚动后试图阻止其增大，难以从根本上阻断错误传播。

基于上述分析，本文的核心动机是：**将干预时机从解码阶段前移至预填充阶段（prefill stage），在错误累积发生之前，对初始 KV 缓存进行一次性的、模态感知的精准修正**。具体而言，我们提出利用 Transformer 中键（Key）负责“注意何处”与值（Value）负责“聚合什么”的解耦特性，通过物体与背景的对比信号提取针对性方向，分别增强物体为中心的注意力并过滤背景噪声，从而从源头阻断幻觉的生成链条。

## 核心创新

PTI 的核心创新在于将干预时机从“解码阶段每步持续干预”迁移至“预填充阶段仅干预一次”，并将干预对象从粗粒度的隐藏状态重构为细粒度、模态感知且键值解耦的初始 KV 缓存。这一范式转变直接回应了现有解码时间干预（DTI）方法中观察到的“雪球幻觉”困境——即持续施加统一转向向量虽能降低幻觉频率，却加剧了残余幻觉的严重性（Figure 2）。

具体而言，PTI 引入了四个互锁的 **changed slots**，共同构成其相对于 DTI 方法（如 **VISTA**、**VTI**、**PAI**）的差异化优势：

1.  **干预时机：从解码阶段到预填充阶段。** DTI 方法在自回归解码的每一步对隐藏状态施加干预，这导致初始错误一旦产生便沿生成序列累积放大。PTI 在预填充阶段一次性增强初始 KV 缓存，在错误传播的源头完成修正，从根本上阻断了雪球效应的形成路径。

2.  **干预目标表示：从隐藏状态到 KV 缓存。** 隐藏状态是高度混合的表示，难以进行精准调控。PTI 直接操作 Transformer 中功能解耦的 Key 和 Value 缓存——Key 控制“注意何处”，Value 决定“聚合什么”。这种细粒度控制使得干预能够分别引导注意力分布和过滤信息内容，而非笼统地扰动整个表示空间。

3.  **模态感知：从统一向量到视觉/文本独立方向。** 视觉输入和文本输入在 LVLM 中承载不同语义角色，但 DTI 方法通常采用模态不可知的统一转向向量。PTI 为视觉 tokens 和文本 tokens 分别提取专属的转向方向，使视觉干预聚焦于物体-背景对比信号，文本干预则强化物体锚定的语言表征，避免了跨模态信号的相互干扰。

4.  **键值解耦：从无区分干预到 Key/Value 分工。** 这是 PTI 实现精细控制的核心机制。视觉 Key 缓存转向向量引导注意力头聚焦于物体区域，缓解生成过程中的全局视觉注意力衰减（Figure 5b 左）；视觉 Value 缓存转向向量则过滤背景噪声，强化物体相关信息的聚合（Figure 5a）。消融实验证实，Value 缓存的物体 vs. 背景对比对幻觉减少贡献最大，而 Key 缓存干预则增强了局部物体中心注意力（Figure 5b 右）。

上述 changed slots 通过两阶段流水线实现：**Stage I** 在 MSCOCO 对比样本上提取解耦的转向向量（Eq. 3, Eq. 5），**Stage II** 将这些向量按模态注入下游输入的预填充 KV 缓存（Eq. 7, Eq. 8），随后进行标准自回归解码。这一设计使得 PTI 能够在不修改模型架构、不增加训练开销的前提下，以极小的延迟代价（所有模型均低于 ×1.02，Table 9）实现跨模型、跨解码策略的幻觉缓解，并与解码阶段方法（如 PAI、VISTA）兼容叠加，进一步提升性能（Table 6）。

## 整体框架

PTI 遵循“方向提取—多模态注入—标准解码”的两阶段流水线，其核心设计在于将干预时机从解码阶段前移至预填充阶段，并在 KV 缓存层面进行模态感知的键值解耦操作。

### 干预范式的根本转变

现有解码时间干预（DTI）方法（如 **VISTA**、**VTI**、**PAI**）在每步解码时持续对隐藏状态施加统一的转向向量，这种持续的、模态不可知的干预方式不仅无法修正预填充阶段已经形成的错误表征，反而会因错误累积加剧“雪球”幻觉。Figure 1 清晰地对比了两种范式：DTI 在预填充和已生成 token 的隐藏状态上反复介入；而 PTI 仅在预填充阶段对初始 KV 缓存进行一次性的模态特定干预，随后将增强后的缓存交还给标准自回归解码器。

![[assets/figures/papers/paper_list_l774_https_arxiv_org_abs_2604_25642/figures/001_Figure_1.jpg]]
*Figure 1: Comparative analysis. (a): Decoding-Time Intervention methods continuously intervene in the hidden states of the prefill and generated token. (b): Our method applies modal-specific interventions to the KV cache only once in the prefill phase*

### 两阶段流水线

Figure 3 展示了 PTI 的完整流水线，由两个解耦的阶段构成：

![[assets/figures/papers/paper_list_l774_https_arxiv_org_abs_2604_25642/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline overview of our PTI. PTI consists of two stages. Stage I: we separately extracted the object signals from the visual and textual contrastive KV caches to extract the directions. Stage II: these directions are applied as multi-modal interventions to the initial KV cache of downstream input. The modified cache is then passed back to the decoder to generate responses*

**Stage I：方向提取（Object Directions Extraction）**

该阶段的目标是从对比样本中提取视觉和文本两个模态的转向向量，这些向量将作为后续干预的“方向信号”。具体而言：

- **视觉方向**：利用 MSCOCO 数据集中的物体分割标注，构造正样本（仅保留物体区域，背景置零）和负样本（仅保留背景，物体区域置零）。将正负样本分别送入目标 LVLM 的视觉编码器和 LLM 解码器的预填充阶段，提取所有层的 KV 缓存。视觉转向向量定义为正负样本 KV 缓存在视觉 token 位置上的差异，经平均池化后得到：
  $$ \Delta C_{\mathrm{img}}^{i,l} = \mathrm{AP}(C_{\mathrm{pos}}^{i,l} - C_{\mathrm{neg}}^{i,l})[\mathcal{T}_{\mathrm{img}}], \quad C\in\{K,V\} $$
  最终对 N 个样本取平均，得到层级的视觉键转向向量 $S_{\mathrm{k,img}}^l$ 和值转向向量 $S_{\mathrm{v,img}}^l$。

- **文本方向**：构造正样本（包含物体名称的文本描述）和负样本（原始文本），提取最后一个文本 token 位置的 KV 缓存差异：
  $$ \Delta \hat{C}_{\mathrm{txt}}^{i,l} = (\hat{C}_{\mathrm{pos}}^{i,l} - \hat{C}_{\mathrm{neg}}^{i,l})[N_x-1], \quad \hat{C}\in\{\hat{K},\hat{V}\} $$
  同样对 N 个样本取平均，得到文本键转向向量 $S_{\mathrm{k,txt}}^l$ 和值转向向量 $S_{\mathrm{v,txt}}^l$。

方向提取仅需在 MSCOCO 的 100 对 VQA 样本上进行一次，无需针对每个下游输入重复计算。

**Stage II：多模态干预（Multi-modal Intervention）**

对于下游输入，模型正常执行预填充阶段得到初始 KV 缓存。随后，PTI 将 Stage I 提取的方向按模态和 token 位置注入：

- **视觉干预**：在所有视觉 token 位置 $\mathcal{T}_{\mathrm{img}}$ 上施加：
  $$ \tilde{K}^l[\mathcal{T}_{\mathrm{img}}] \mathrel{+}= \lambda_{\mathrm{k,img}} S_{\mathrm{k,img}}^l, \quad \tilde{V}^l[\mathcal{T}_{\mathrm{img}}] \mathrel{+}= \lambda_{\mathrm{v,img}} S_{\mathrm{v,img}}^l $$
  其中 $\lambda_{\mathrm{k,img}}$ 和 $\lambda_{\mathrm{v,img}}$ 是控制干预强度的超参数。

- **文本干预**：仅在最后一个文本 token 位置 $\mathcal{T}_{\mathrm{txt}}$ 上施加：
  $$ \tilde{K}^l[\mathcal{T}_{\mathrm{txt}}] += \lambda_{\mathrm{k,txt}} S_{\mathrm{k,txt}}^l, \quad \tilde{V}^l[\mathcal{T}_{\mathrm{txt}}] += \lambda_{\mathrm{v,txt}} S_{\mathrm{v,txt}}^l $$

干预完成后，增强的 KV 缓存 $\tilde{K}^l$ 和 $\tilde{V}^l$ 被传递回解码器，后续的解码过程完全遵循标准的自回归生成流程，无需任何额外修改。

### 键值解耦的设计逻辑

PTI 对键和值的干预具有明确的功能分工：

- **键缓存干预**：通过物体-背景对比提取的键方向，引导注意力机制在生成过程中持续关注视觉上存在的物体区域，缓解全局视觉注意力随解码步数增加而衰减的问题。
- **值缓存干预**：通过物体-背景对比提取的值方向，过滤背景噪声，增强物体相关信息的聚合质量。

消融实验（Figure 5）验证了这一设计的有效性：视觉值缓存干预（物体 vs. 背景对比）对幻觉减少的贡献最大；视觉键缓存干预则在缓解注意力衰减和增强局部物体注意力方面发挥作用。Table 5 进一步表明，在所有视觉 token 上施加视觉干预是减少幻觉的最关键组件，而在最后一个文本 token 上施加文本干预则有助于恢复 F1 分数。

## 核心模块与公式推导

### 干预范式：从解码时间到预填充时间

现有的解码时间干预（DTI）方法在自回归生成的每一步持续施加统一的转向向量，这种“事后修正”策略面临两个根本性问题：第一，初始的视觉-语言表征错误在解码开始前已经形成，后续干预无法从源头消除；第二，持续的干预反而可能扰乱正常的生成过程，导致残余幻觉的严重性加剧——即“雪球幻觉”现象（见 Figure 2 的 PSH 指标分析）。PTI 将干预时机前移至预填充阶段（prefill stage），在解码开始前对初始 KV 缓存进行一次性的模态感知修正，从源头阻断错误传播。

干预范式的对比如 Figure 1 所示：DTI 方法（Figure 1a）在预填充和每个生成 token 的隐藏状态上持续干预；PTI（Figure 1b）仅在预填充阶段对 KV 缓存施加一次模态特定的干预，随后由标准自回归解码接管。

### 方法总览：两阶段流水线

PTI 的完整流水线如 Figure 3 所示，包含两个阶段：

**阶段一：物体方向提取（Object Directions Extraction）**。利用 MSCOCO 数据集中的物体分割标注，构造正负对比样本对，从预训练的 LVLM 中提取视觉和文本两个模态的转向向量。视觉方向通过物体区域与背景区域的 KV 缓存差异获得，文本方向通过物体锚定的描述与原始描述的 KV 缓存差异获得。

**阶段二：多模态干预（Multi-modal Intervention）**。将阶段一提取的视觉和文本转向向量，按模态分别注入下游输入在预填充阶段产生的初始 KV 缓存中。视觉方向施加于所有视觉 token 位置，文本方向施加于最后一个文本 token 位置。干预后的增强缓存直接送入解码器进行标准自回归生成。

### 关键公式与变量含义

#### 基础：KV 缓存投影

在 Transformer 的第 $l$ 层，输入嵌入 $X^l$ 通过线性投影生成键（Key）和值（Value）张量：

$$\mathbf{K}^l = X^l \mathbf{W}_K^l, \quad \mathbf{V}^l = X^l \mathbf{W}_V^l$$

其中 $\mathbf{W}_K^l, \mathbf{W}_V^l$ 分别为第 $l$ 层的键和值投影矩阵。预填充阶段结束后，所有 token 的 $(\mathbf{K}^l, \mathbf{V}^l)$ 被缓存，作为后续解码的上下文基础。PTI 正是在这个初始缓存上进行干预。

#### 视觉转向向量提取

对于第 $i$ 个 MSCOCO 样本，构造正样本（仅保留物体区域的图像）和负样本（仅保留背景区域的图像），分别通过 LVLM 的视觉编码器和 Transformer 层获取其 KV 缓存。视觉转向向量定义为正负样本缓存差异在视觉 token 位置上的平均池化：

$$\Delta C_{\mathrm{img}}^{i,l} = \mathrm{AP}(C_{\mathrm{pos}}^{i,l} - C_{\mathrm{neg}}^{i,l})[\mathcal{T}_{\mathrm{img}}], \quad C\in\{K,V\}$$

其中 $\mathcal{T}_{\mathrm{img}}$ 表示视觉 token 的索引集合，$\mathrm{AP}(\cdot)$ 为平均池化操作。对所有 $N$ 个样本的方向取平均，得到最终的视觉键和值转向向量：

$$S_{\mathrm{k,img}}^l = \frac{1}{N}\sum_{i=1}^{N} \Delta K_{\mathrm{img}}^{i,l}, \quad S_{\mathrm{v,img}}^l = \frac{1}{N}\sum_{i=1}^{N} \Delta V_{\mathrm{img}}^{i,l}$$

**物理含义**：$S_{\mathrm{k,img}}^l$ 编码了“物体区域应被关注”的方向信号，引导注意力头在生成时将更多权重分配给物体 token；$S_{\mathrm{v,img}}^l$ 编码了“物体特征应被聚合”的方向信号，抑制背景噪声对值聚合的干扰。这种键值解耦的设计是 PTI 区别于以往统一干预方法的核心创新。

#### 文本转向向量提取

文本方向同样通过对比学习获得。对于第 $i$ 个样本，正样本为包含物体名称的锚定描述（如“a photo of a cat”），负样本为原始描述。提取最后一个文本 token 位置的 KV 缓存差异：

$$\Delta \hat{C}_{\mathrm{txt}}^{i,l} = (\hat{C}_{\mathrm{pos}}^{i,l} - \hat{C}_{\mathrm{neg}}^{i,l})[N_x-1], \quad \hat{C}\in\{\hat{K},\hat{V}\}$$

其中 $N_x$ 为文本 token 数量，$[N_x-1]$ 索引最后一个 token 位置。对所有样本取平均得到文本转向向量 $S_{\mathrm{k,txt}}^l$ 和 $S_{\mathrm{v,txt}}^l$。

#### 下游干预：注入转向向量

在推理时，对于新的下游输入，首先完成预填充阶段获得初始 KV 缓存 $\tilde{K}^l, \tilde{V}^l$，然后按模态和位置施加干预：

**视觉干预**（施加于所有视觉 token 位置 $\mathcal{T}_{\mathrm{img}}$）：

$$\tilde{K}^l[\mathcal{T}_{\mathrm{img}}] \mathrel{+}= \lambda_{\mathrm{k,img}} S_{\mathrm{k,img}}^l, \quad \tilde{V}^l[\mathcal{T}_{\mathrm{img}}] \mathrel{+}= \lambda_{\mathrm{v,img}} S_{\mathrm{v,img}}^l$$

**文本干预**（施加于最后一个文本 token 位置 $\mathcal{T}_{\mathrm{txt}}$）：

$$\tilde{K}^l[\mathcal{T}_{\mathrm{txt}}] += \lambda_{\mathrm{k,txt}} S_{\mathrm{k,txt}}^l, \quad \tilde{V}^l[\mathcal{T}_{\mathrm{txt}}] += \lambda_{\mathrm{v,txt}} S_{\mathrm{v,txt}}^l$$

其中 $\lambda_{\mathrm{k,img}}, \lambda_{\mathrm{v,img}}, \lambda_{\mathrm{k,txt}}, \lambda_{\mathrm{v,txt}}$ 为四个独立的干预强度超参数。消融实验（Figure 6-8）表明，值缓存干预强度对幻觉缓解起主导作用，但过大的强度会降低生成质量（F1 下降、输出长度缩短），需要精细调节。

### 模块功能定位

| 模块 | 功能 | 关键设计 |
|------|------|----------|
| 物体方向提取 | 从 MSCOCO 对比样本中学习转向向量 | 物体-背景对比信号；键值解耦提取 |
| 视觉缓存干预 | 增强物体注意力，过滤背景噪声 | 键引导“注意何处”，值控制“聚合什么” |
| 文本缓存干预 | 强化物体锚定的语言先验 | 仅在最后一个文本 token 位置施加 |
| 标准自回归解码 | 基于增强缓存生成响应 | 无需修改解码策略，即插即用 |

消融分析（Table 5）确认了各模块的贡献：视觉值缓存干预（物体 vs. 背景对比）是实现最大幻觉减少的核心组件；视觉键缓存干预缓解了生成过程中的全局视觉注意力衰减（Figure 5b）；文本干预在最后一个 token 位置施加可恢复因视觉干预导致的 F1 下降。

### 补充图表

![[assets/figures/papers/paper_list_l774_https_arxiv_org_abs_2604_25642/figures/010_Figure_5.jpg]]
*Figure 5: Internal interpretability analysis of visual cache intervention on LLAVA-1.5 across 300 randomly selected images from MSCOCO. (a): Ablation study on value intervention strategies, validating that the maximal contrast (object vs. background) yields the largest hallucination reduction. (b): Analysis of the key cache intervention, demonstrating its dual effect: mitigating global visual attention decay during generation (left) and enhancing local, object-centric attention (right). The change rate formula is detailed in Appendix A*

## 实验与分析

### 核心发现：从频率抑制到严重性控制

现有解码时间干预（DTI）方法（如 **VISTA**）虽然在降低幻觉频率上取得了一定成效，但存在一个被忽视的副作用——残余幻觉的严重性加剧。Figure 2 的定量分析揭示了这一“雪球幻觉”（Snowball Hallucination）现象：VISTA 在降低 CHAIR 指标的同时，其 PSH（雪球幻觉比例）反而升高，表明模型一旦开始幻觉，后续生成会以更严重的错误级联。这一瓶颈的根源在于 DTI 方法在解码阶段每步持续施加统一的转向向量，无法从源头修正错误的视觉-语言表征，导致初始错误在自回归过程中不断累积。

![[assets/figures/papers/paper_list_l774_https_arxiv_org_abs_2604_25642/figures/002_Figure_2.jpg]]
*Figure 2: Quantitative analysis of LLAVA-1.5 on CHAIR Benchmark [33]. We report*

PTI 通过将干预时机前移至预填充阶段，对初始 KV 缓存进行一次性修正，从根本上切断了错误传播链条。

### 物体幻觉基准：CHAIR 上的显著增益

Table 1 报告了 CHAIR 基准上的幻觉评估结果。在 LLaVA-1.5 的 Greedy 解码策略下，PTI 将 CHAIR_S 从 47.4 降至 15.4（↓32.0），CHAIR_I 从 13.7 降至 5.4（↓8.3），降幅远超所有对比方法。VISTA 同期仅将 CHAIR_S 降至 34.3，VTI 降至 32.3。在 Qwen-VL-Chat 上，PTI 同样取得 CHAIR_S 20.6（Vanilla 为 39.6，↓19.0）的最优结果。值得注意的是，PTI 在不同解码策略（Greedy、Nucleus Sampling、Beam Search）下均表现稳定，而 **VCD** 和 **OPERA** 等方法仅对特定解码策略有效且提升有限。

![[assets/figures/papers/paper_list_l774_https_arxiv_org_abs_2604_25642/figures/004_Table_1.jpg]]
*Table 1: CHAIR hallucination evaluation results across different decoding strategies and LVLMs. PTI is compared against SOTA trainingfree methods that operate during decoding, where “Vanilla” stands for the original model. The maximum new token is set to 512. The best result is highlighted in bold, while the second-best is marked with an underline. We provide the latency comparison in Appendix B*

![[assets/figures/papers/paper_list_l774_https_arxiv_org_abs_2604_25642/figures/015_Figure_6.jpg]]
*Figure 6: Ablation matrices for multi-modal KV cache intervention strength on LLAVA-1.5 with greedy decoding strategy. Brighter colors indicate better performance, while red boxes highlight the parameter combinations used in Table 1*

Table 3 的 AMBER 基准结果进一步验证了 PTI 的泛化能力。在 DeepSeek-VL-Chat 的 Greedy 解码下，PTI 将 CHAIR_I 从 6.0 降至 4.0，优于 VISTA（5.0）和 PAI（5.0）。

![[assets/figures/papers/paper_list_l774_https_arxiv_org_abs_2604_25642/figures/006_Table_3.jpg]]
*Table 3: Experiment results on AMBER Benchmark. The generative task’s parameters and metrics follow CHAIR, while the discriminative task’s align with POPE*

### 判别式基准：POPE 上的全面提升

Table 2 展示了 POPE 基准上的实验结果。PTI 在 LLaVA-1.5 上取得平均 F1 分数 82.85，优于 VISTA（81.98）和 VTI（81.64）。在最具挑战性的对抗子集（Adversarial）上，PTI 的 F1 达到 79.18，相比 Vanilla（76.23）提升 2.95 个百分点。Qwen-VL-Chat 上 PTI 的平均准确率达到 85.69，相比 Vanilla 提升 2.00 个百分点。Table 7 的随机和流行子集补充结果显示，PTI 在所有子集上均保持领先。

![[assets/figures/papers/paper_list_l774_https_arxiv_org_abs_2604_25642/figures/005_Table_2.jpg]]
*Table 2: Experiment results on POPE Benchmark. We report the average accuracy and F1-score computed across three object splits, as well as the specific results on the most challenging adversarial split. We set the maximum new token to 32 and use the nucleus sampling strategy. The complete table can be found in Appendix B*

### 综合基准：MMHal-Bench 与 MME

Figure 4 按 MMHal-Bench 的八个问题类别细分了性能对比。PTI 在物体属性（ATTR）、对抗性物体（ADV）、空间关系（SPAT）等类别上均优于 Vanilla 和 VISTA，尤其在需要细粒度视觉定位的类别上优势明显。

![[assets/figures/papers/paper_list_l774_https_arxiv_org_abs_2604_25642/figures/007_Figure_4.jpg]]
*Figure 4: Performance comparison on MMHal-Bench, with results disaggregated by its eight question categories: attributes (ATTR), adversarial objects (ADV), comparisons (COMP), counting (COUNT), spatial relations (SPAT), environmental inference (ENV), holistic descriptions (HOL), and others (OTHER). All the model responses are evaluated using GPT-5 for alignment with ground-truth answers*

Table 4 和 Table 8 的 MME 评估显示，PTI 在 DeepSeek-VL-Chat 上取得总分 671.6（Vanilla 为 651.6，+20.0），在存在性判断、计数、位置识别等子任务上均有提升，且未引入显著的认知能力退化。

### 消融分析：模态与位置的关键作用

Table 5 的消融研究揭示了干预模态和位置对性能的差异化影响。在所有视觉 tokens 上施加视觉干预是减少幻觉的最关键组件，但单独使用会降低 F1 分数；在最后一个文本 token 上施加文本干预可以有效恢复 F1，形成互补。仅使用文本干预而不进行视觉干预时，CHAIR 指标几乎无改善，验证了视觉缓存修正是幻觉缓解的核心驱动力。

![[assets/figures/papers/paper_list_l774_https_arxiv_org_abs_2604_25642/figures/009_Table_5.jpg]]
*Table 5: Ablation study for intervention modality and position on LLAVA-1.5. “CS”: CHAIRS, “CI”: CHAIRI, “F1”: F1-score*

Figure 5 从内部可解释性角度进一步剖析了视觉缓存干预的机制。Figure 5(a) 的值缓存消融表明，物体 vs. 背景的最大对比策略（即正样本为仅含物体的 KV 缓存，负样本为仅含背景的 KV 缓存）实现了最大程度的幻觉减少，而物体 vs. 噪声或物体 vs. 空白的对比效果次之。Figure 5(b) 左图显示，视觉键缓存干预缓解了生成过程中的全局视觉注意力衰减——Vanilla 模型在生成后期对视觉 tokens 的注意力逐渐下降，而 PTI 维持了更稳定的视觉注意力分配。右图则表明，键干预增强了局部、以物体为中心的注意力质量。

### 泛化性与组合能力

Table 6 的跨模型和组合方法研究表明，PTI 提取的转向方向具有良好的跨模型迁移能力。将 LLaVA-1.5 上提取的方向直接应用于 Qwen-VL-Chat，仍能取得显著的幻觉减少效果。此外，PTI 与解码阶段方法（**PAI**、**VISTA**）结合可进一步提升性能，表明预填充干预和解码干预具有互补性。

![[assets/figures/papers/paper_list_l774_https_arxiv_org_abs_2604_25642/figures/011_Table_6.jpg]]
*Table 6: Cross-models and Comb-methods generalization study. Performance on POPE Adversarial subset*

### 效率分析

Table 9 的推理效率对比显示，PTI 引入的延迟开销极小——所有模型上的延迟增加均低于 ×1.02，吞吐量损失低于 ×0.98。相比之下，**VCD** 的延迟开销高达 ×2.0 以上，**OPERA** 的吞吐量损失显著。PTI 的高效性源于其仅需在预填充阶段干预一次，无需在解码过程中进行额外的前向传播或缓存操作。

![[assets/figures/papers/paper_list_l774_https_arxiv_org_abs_2604_25642/figures/014_Table_9.jpg]]
*Table 9: Measure of Latency (ms/token) and Throughput (token/s) on CHAIR benchmark. All results use the Nucleus Sampling decoding strategy on a NVIDIA 4090 GPU*

### 失败模式与局限性

尽管 PTI 在物体幻觉缓解上表现优异，但分析揭示了以下边界：

1. **干预强度敏感**：Figure 6-8 的超参数消融矩阵显示，值缓存干预强度对幻觉缓解起主导作用，但过大的强度会导致生成质量下降（F1 降低、输出长度缩短）。不同模型的最优强度组合差异显著，需要针对每个模型进行精细调节。
2. **方向提取的数据依赖**：转向方向从 MSCOCO 的 100 个 VQA 样本中提取，依赖该数据集的物体分割和标注质量，可能引入数据偏差，在分布外场景下的有效性需进一步验证。
3. **任务范围限制**：当前验证集中于物体幻觉基准（CHAIR、POPE、AMBER）和通用综合基准（MME、MMHal），未在复杂推理任务（如数学、代码生成）上测试，PTI 对非物体类错误（如逻辑错误、关系推理错误）的影响尚不明确。

## 方法谱系与知识库定位

### 核心干预范式的转变：从解码时间到预填充时间

PTI 的提出直接回应了现有解码时间干预（Decoding-Time Intervention, DTI）方法的结构性缺陷。DTI 方法——包括 **VISTA**、**VTI**、**PAI**——在自回归解码的每一步持续施加统一的转向向量。这种持续干预虽然能降低幻觉的整体频率，却无法从源头修正初始的视觉-语言表征错误。Figure 2 的定量分析揭示了这一悖论：VISTA 在降低 CHAIR_S 和 CHAIR_I 的同时，其 PSH（雪球幻觉比例）反而升高，表明残余幻觉的严重性在加剧。PTI 将干预窗口前移至预填充阶段（prefill stage），在解码开始之前对初始 KV 缓存进行一次性的模态感知修正，从根本上切断了错误累积的链条。

### 与现有训练无关方法的对比定位

PTI 属于训练无关（training-free）的幻觉缓解方法，与以下基线形成清晰对比：

- **对比解码方法**（如 **VCD**）：通过对比原始模型和扰动模型的输出分布来抑制幻觉，但仅支持特定的解码策略（如 Nucleus Sampling），且性能提升有限。PTI 在 Greedy、Beam Search、Nucleus Sampling 等多种解码策略下均表现出一致的性能增益（Table 1），泛化性显著更强。

- **Beam Search 优化方法**（如 **OPERA**）：通过修改 Beam Search 的评分机制来惩罚过度依赖语言先验的候选序列。该方法同样受限于特定解码策略，而 PTI 的 KV 缓存干预与解码策略解耦，适用面更广。

- **解码时间干预方法**（**VTI**、**PAI**、**VISTA**）：这些方法在解码阶段对隐藏状态施加统一的转向向量。PTI 与之相比有三项关键改进：（1）干预时机从解码阶段每步干预变为预填充阶段仅干预一次；（2）干预目标从粗粒度的隐藏状态变为细粒度的初始 KV 缓存；（3）干预方式从模态不可知的统一向量变为解耦的键（引导物体注意力）和值（过滤背景噪声）的模态感知干预。

### 知识库定位与理论基础

PTI 的核心理念植根于 Transformer 中 KV 缓存的角色认知。KV 缓存不仅存储上下文信息，更通过注意力机制主动塑造后续生成过程。PTI 利用键（Key）的“注意何处”与值（Value）的“聚合什么”的解耦特性，以物体-背景对比信号提取方向，精准修正预填充阶段的表征。

方向提取策略采用 MSCOCO 数据集的物体分割标注构建正负对比样本：正样本为仅包含物体的视觉上下文，负样本为仅包含背景的视觉上下文。这种物体-背景的最大对比被消融实验证实是实现幻觉减少的关键（Figure 5a）。文本方向的提取则通过对比包含物体锚定信息的文本与原始文本的 KV 缓存差异来实现。

### 适用边界与局限

PTI 的有效性存在以下边界条件：

1. **干预强度敏感**：视觉和文本的键值干预强度需要精细调节。过大的干预强度虽然能进一步降低幻觉指标，但会导致 F1 分数下降和输出长度缩短（Figure 6-8），表明过度转向会损害生成质量。

2. **方向提取依赖外部数据**：转向向量的提取依赖 MSCOCO 的物体分割和标注，可能引入该数据集的分布偏差。对于 MSCOCO 中未覆盖的物体类别或场景类型，转向向量的有效性尚待验证。

3. **任务覆盖范围有限**：当前验证集中在物体幻觉相关的基准（CHAIR、POPE、AMBER）和综合理解基准（MMHal-Bench、MME），未在复杂推理任务（如数学、代码生成）上验证 PTI 的影响。

4. **架构依赖性**：PTI 的干预机制基于 Transformer 的 KV 缓存结构，对于采用其他架构（如状态空间模型）的 LVLM，该方法无法直接迁移。

### 组合性与迁移性

PTI 展现出良好的组合性和跨模型迁移能力。Table 6 表明，PTI 与解码阶段方法（PAI、VISTA）结合可进一步提升性能，说明预填充阶段干预与解码阶段干预具有互补性。此外，从一个模型提取的转向方向可直接应用于另一个模型，跨模型迁移有效，这暗示 PTI 捕获的物体-背景对比信号具有一定的模型无关性。

### 开放问题

1. PTI 能否在更大规模（如数十亿参数级别）或不同架构的 LVLM 上保持有效性？当前验证集中在 LLaVA-1.5、Qwen-VL-Chat 和 DeepSeek-VL-Chat 等中等规模模型。

2. 转向方向的提取可否实现动态或针对特定输入的自适应调整？当前采用固定的平均方向，可能无法充分利用输入图像的特定物体分布信息。

3. PTI 对物体幻觉之外的错误类型（如关系推理错误、空间位置错误、属性绑定错误）的泛化能力如何？Figure 4 的 MMHal-Bench 细分结果显示 PTI 在不同问题类别上的增益并不均匀，暗示某些错误类型可能无法通过物体-背景对比信号有效缓解。

4. 预填充阶段干预的时机选择是否最优？是否存在更精细的层级别干预策略（如仅干预特定层）可以进一步提升效率或效果？

## 原文 PDF

![[paperPDFs/CVPR_2026/Prefill_Time_Intervention_for_Mitigating_Hallucination_in_Large_Vision_Language_Models.pdf]]
