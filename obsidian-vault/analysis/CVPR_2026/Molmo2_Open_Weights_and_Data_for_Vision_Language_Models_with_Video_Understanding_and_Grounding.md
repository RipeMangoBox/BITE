---
title: "Molmo2: Open Weights and Data for Vision-Language Models with Video Understanding and Grounding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Molmo2_Open_Weights_and_Data_for_Vision_Language_Models_with_Video_Understanding_and_Grounding.pdf
aliases:
- Molmo2
tags:
  - CVPR_2026
  - topic/vision_multimodal_applications/vision_models_multimodal
  - topic/vision_multimodal_applications
core_operator: 通过构建一系列完全开放的大规模视频数据集（密集字幕、QA、时空指向和追踪），并结合三阶段多任务联合训练（引入双向注意力、任务定制token权重、序列打包等技术），使模型在保持通用能力的同时获得强大的视频grounding能力。
primary_logic: 利用人类口述字幕、人机协作QA以及从现有分割/检测数据转换，可以高效收集覆盖广泛视觉概念的视频grounding数据；将这些数据与图像/NLP数据统一训练，并通过token weighting平衡长/短输出任务，能让开放模型在多个视频理解和grounding基准上达到甚至超越专有模型。
claims:
- Molmo2-8B在视频计数准确率上达到35.5，显著超过Qwen3-VL-8B的29.6，表明开放模型无需蒸馏也能获得强大grounding。
- Molmo2在视频指向F1上为38.4，远超专有模型Gemini 3 Pro的20.0，展示了开放数据驱动grounding的有效性。
- Molmo2-Cap数据集平均每视频924词，是现有最密集的字幕数据集，为详细理解提供了基础。
- 三阶段训练加上token weighting、双向注意力等技术可显著改善视频字幕和QA性能。
---

# Molmo2: Open Weights and Data for Vision-Language Models with Video Understanding and Grounding

> [!tip] 核心洞察
> 利用人类口述字幕、人机协作QA以及从现有分割/检测数据转换，可以高效收集覆盖广泛视觉概念的视频grounding数据；将这些数据与图像/NLP数据统一训练，并通过token weighting平衡长/短输出任务，能让开放模型在多个视频理解和grounding基准上达到甚至超越专有模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | Molmo2：面向视频理解与定位的开放权重与数据视觉语言模型 |
| 英文题名 | Molmo2: Open Weights and Data for Vision-Language Models with Video Understanding and Grounding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.10611) · [Code](https://github.com/allenai/molmo2) |
| Topic | #topic/vision_multimodal_applications/vision_models_multimodal #topic/vision_multimodal_applications |
| Method | Molmo2 |
| Dataset | Molmo2-VideoCount, Molmo2-VideoPoint, Molmo2-Track |

> [!tip] 效果简介
> - Molmo2-VideoCount 上，准确率 (Accuracy) 35.5 (Molmo2-8B) vs 29.6 (Qwen3-VL-8B) (+5.9)。
> - Molmo2-VideoPoint 上，F1 38.4 (Molmo2-8B) vs 20.0 (Gemini 3 Pro) (+18.4)。
> - Molmo2-Track 上，J&F 56.2 (Molmo2-8B) vs 41.1 (Gemini 3 Pro) (+15.1)。

## 概述

视觉语言模型（VLM）在图像理解上已取得长足进步，但将细粒度时空定位能力（指向、追踪）扩展到视频领域仍面临瓶颈：现有开源模型普遍缺乏高质量、多样化的视频grounding数据，且常用数据依赖从专有VLM蒸馏，限制了开放模型的时空定位上限。Molmo2针对这一缺口，构建了迄今为止规模最大的完全开放视频中心多模态语料库，包含九个全新数据集，覆盖密集字幕、长视频问答、开放词汇指向与追踪。通过三阶段多任务联合训练——图像字幕/指向预训练、联合多模态监督微调、长上下文后训练——并结合双向视觉注意力、任务定制token加权（视频字幕权重0.1，指向任务权重0.2，其余任务采用$4/\sqrt{n}$动态权重）以及序列打包等技术，Molmo2在保持通用图像理解能力的同时，获得了强大的视频grounding能力。

核心结论是：**完全开放数据驱动的视频grounding可以匹配甚至超越专有模型**。Molmo2-8B在视频计数准确率上达到35.5，显著超过开源权重模型Qwen3-VL-8B的29.6；在视频指向F1上达到38.4，远超专有模型Gemini 3 Pro的20.0；在目标追踪J&F上达到56.2，同样大幅领先Gemini 3 Pro的41.1。这些结果表明，通过人机协作数据采集和学术数据转换，无需依赖专有模型蒸馏，即可让开放VLM在细粒度视频理解任务上取得有竞争力的性能。

## 背景与动机

### 问题背景：视觉语言模型的视频理解与定位鸿沟

近年来，视觉语言模型（VLM）在图像理解任务上取得了显著进展，但在视频领域仍存在根本性挑战。视频不仅包含静态视觉信息，还涉及复杂的时空动态、对象运动、事件演变和多帧关联推理。现有的视频语言模型主要集中于高层语义理解（如视频问答、动作识别），但在细粒度时空定位能力上严重不足——即模型不仅要理解“发生了什么”，还需要精确指出“在哪里发生”、“何时发生”以及“如何随时间变化”。

这种能力缺口在开放模型中尤为突出。当前开源视频语言模型普遍缺乏高质量、多样化的视频grounding数据（包括指向、追踪等任务），而常用的数据获取方式依赖于从专有VLM进行知识蒸馏，这不仅限制了数据的可扩展性，也使得开放模型在细粒度时空定位上与闭源系统存在显著差距。

### 现有方法的局限

从数据层面看，现有视频数据集存在三个核心瓶颈：

1. **字幕密度不足**：主流的视频字幕数据集如Video Localized Narratives平均每视频仅75词，LLaVA-Video-178K为547词，远不足以捕捉视频中的细粒度视觉动态。稀疏的字幕导致模型无法学习到精确的时空描述能力。

2. **Grounding数据匮乏**：视频指向（pointing）和追踪（tracking）的标注成本极高，现有学术数据集规模有限且覆盖的视觉概念狭窄。开源模型通常只能从这些有限数据中学习，难以泛化到开放场景。

3. **依赖专有模型蒸馏**：许多开放模型通过蒸馏GPT-4V、Gemini等闭源系统的输出来获取训练数据，这不仅引入了许可和透明度问题，也使得开放模型的性能上限受制于蒸馏源。

从模型训练层面看，现有方法通常采用两阶段流程（预训练+微调），但未专门针对grounding能力设计预训练目标，导致模型在定位任务上缺乏基础能力。此外，多任务联合训练中缺乏有效的损失平衡机制，长输出任务（如密集字幕）与短输出任务（如计数）之间的训练冲突未被妥善处理。

### 本文动机与核心思路

Molmo2的提出正是为了填补上述缺口。其设计哲学基于一个核心洞察：**利用人类口述字幕、人机协作QA以及从现有分割/检测数据转换，可以高效收集覆盖广泛视觉概念的视频grounding数据；将这些数据与图像/NLP数据统一训练，并通过token weighting平衡长/短输出任务，能让开放模型在多个视频理解和grounding基准上达到甚至超越专有模型。**

具体而言，Molmo2的动机体现在三个层面：

- **数据开放性**：构建完全开放的大规模视频数据集，不依赖专有模型蒸馏，涵盖密集字幕、自由形式QA、时空指向和追踪等任务。其中Molmo2-Cap数据集平均每视频924词，是现有最密集的字幕数据集。

- **训练策略创新**：设计三阶段训练流程——图像captioning+pointing预训练→联合多模态SFT→长上下文SFT，使模型在保持通用能力的同时获得强大的视频grounding能力。引入双向注意力、任务定制token权重、序列打包等技术解决多任务训练中的冲突。

- **能力完整性**：支持单图像、多图像和视频输入，可同时生成自由形式文本和grounding输出（时空点、对象轨迹、定位思维链），实现理解与定位的统一。

这一设计使得Molmo2在视频计数准确率上达到35.5（显著超过Qwen3-VL-8B的29.6），在视频指向F1上达到38.4（远超Gemini 3 Pro的20.0），证明了开放数据驱动grounding的有效性，为开放视频语言模型的发展提供了新的范式。

## 核心创新

Molmo2的核心创新在于通过**完全开放的数据构建**与**系统性的训练设计**，首次在开放权重视觉语言模型中实现了覆盖图像、多图和视频的统一时空定位（grounding）能力。其关键突破体现在以下四个维度：

### 1. 全开放视频定位数据体系

现有开源视频模型普遍缺乏高质量的视频定位数据，或依赖从专有VLM蒸馏获取监督信号。Molmo2从根本上改变了这一范式：构建了**7个全新的人机协作数据集**（Table 1中粉色标注），覆盖密集视频字幕、自由形式QA、时空指向（pointing）和对象追踪（tracking），且全程未使用专有模型蒸馏。

- **Molmo2-Cap**：采用两阶段人工标注流水线——标注者先描述短视频片段，再汇总生成完整视频字幕。通过预设问题引导标注者关注动态视觉细节（如物体或事件随时间的变化），最终产生平均**924词/视频**的密集字幕，远超Video Localized Narratives（75词）和LLaVA-Video-178K（547词），成为当前最密集的视频字幕数据集。
- **Molmo2-VideoPoint**与**Molmo2-VideoTrack**：利用现有分割/检测数据转换和人工协作，为视频中的开放词汇对象提供时空坐标标注，使模型学习在帧序列中精确指向和持续追踪目标。
- **Molmo2-AskModelAnything**与**Molmo2-CapQA**：通过人机协作生成覆盖广泛视觉概念的自由形式QA对，补充学术数据集的覆盖盲区。

这一数据体系直接回应了**瓶颈问题**：开放模型缺乏多样化视频定位数据，且常用数据依赖专有模型蒸馏。

### 2. 三阶段多任务联合训练

Molmo2采用**三阶段训练流程**，将图像定位能力系统性地迁移并扩展至视频域：

| 阶段 | 数据组成 | 核心目标 |
|------|---------|---------|
| **预训练** | 60%图像字幕 + 30%图像指向 + 10%自然语言 | 建立基础的视觉-语言对齐和图像定位能力 |
| **联合SFT** | 图像/视频/多图/语言数据混合（含全部9个新数据集） | 多任务统一训练，将定位能力泛化至视频时空域 |
| **长上下文SFT** | 长视频数据 | 扩展模型处理长序列视频的能力 |

与传统两阶段流程（预训练+微调）相比，Molmo2在预训练阶段即引入**图像指向任务**，为后续视频定位奠定基础。消融实验（Table 18）证实，移除预训练中的图像指向会导致基准性能小幅下降。

### 3. 任务定制化训练技术

为平衡多任务联合训练中的长短输出冲突，Molmo2引入三项关键技术：

**Token加权策略**：对不同任务施加差异化损失权重，防止长输出任务（如视频字幕）主导梯度更新。
- 视频字幕：固定权重 **0.1**
- 指向任务：固定权重 **0.2**
- 其余任务：动态权重 $\frac{4}{\sqrt{n}}$，其中 $n$ 为答案token数

这一策略有效平衡了长文本生成与短坐标输出的训练信号。

**双向视觉注意力**：允许不同帧/图像间的视觉token进行双向注意力交互，而非传统的仅前向注意力。消融实验（Table 8b）表明，双向注意力、token加权和时间token三者联合可显著提升视频字幕和QA性能。

**序列打包与消息树掩码**：开发动态打包算法，将多个短示例合并为单条长序列，通过消息树注意力掩码阻止跨示例和跨QA对的交叉注意力（Figure 3），在提升训练吞吐量的同时保持语义独立性。

### 4. 统一的时空定位表示

Molmo2将点、轨迹和对象ID统一编码为紧凑的文本格式，使LLM能够直接输出归一化坐标、时间戳和对象标识。这种设计使得**计数、指向和追踪**三类定位任务共享同一输出空间：
- **指向**：输出目标在特定帧的归一化坐标
- **计数**：先指向后计数（pointing-before-counting）的策略，消融实验（Table 9a）证明这远优于直接预测数量
- **追踪**：输出带时间戳和对象ID的点序列，支持跨帧身份关联

消融实验（Table 10a）进一步揭示，训练中加入指向任务可显著提升追踪性能，表明不同定位子任务间存在正向迁移。

### 创新总结

Molmo2的核心创新可归纳为**因果操纵变量**的实现路径：通过构建全开放的大规模视频定位数据集（数据层面），结合三阶段联合训练和任务定制化技术（算法层面），使开放权重的视觉语言模型首次在视频计数、指向和追踪等细粒度时空定位任务上达到甚至超越专有模型水平，同时保持通用视觉理解能力不退化。

## 整体框架

Molmo2 采用“视觉编码器 → 连接器 → 大语言模型”的标准多模态架构，但在训练流水线、数据组织方式和任务表示上做了系统性设计，使其能够同时处理单张图像、多图像集合和视频，并输出自由文本与时空定位结果（点、轨迹、带定位的思维链）。

### 三阶段训练流水线

Molmo2 的训练分为三个序贯阶段，每个阶段承担不同的能力构建目标：

1. **图像字幕与指向预训练（Pre-training）**  
   仅使用图像数据，混合比例为 60% 字幕、30% 图像指向、10% 自然语言。该阶段运行约 32k 步（batch size 128），在 PixMo-Cap 上约 4 个 epoch，为模型注入基础的视觉理解和指向能力。消融实验表明，移除预训练中的图像指向会导致下游基准性能小幅下降（Table 18）。

2. **联合多模态监督微调（Joint SFT）**  
   将图像、视频、多图像和纯语言数据统一混合进行监督微调。此阶段引入全部 9 个新构建的视频数据集（密集字幕、QA、时空指向与追踪），并与学术数据集联合训练。关键技术创新包括：
   - **双向视觉注意力**：允许不同帧/图像间的视觉 token 进行双向注意力交互，而非仅限于前向注意力。
   - **任务定制 token 加权**：视频字幕固定权重 0.1，指向任务权重 0.2，其余任务采用动态权重 $4 / \sqrt{n}$（$n$ 为答案 token 数），以平衡长输出与短输出任务的训练信号。
   - **序列打包与消息树掩码**：通过动态打包将多个短示例合并为单一长序列，利用消息树注意力掩码阻断跨示例和跨 QA 对的注意力，提升训练吞吐量。

3. **长上下文后训练（Long-context SFT）**  
   在联合 SFT 基础上进行短期的长上下文微调，使用相同的超参数。该阶段显著提升了模型在长视频 QA 基准上的表现（Table 11）。

### 模型架构与输入输出流

**视觉编码**：使用 SigLIP 2 ViT 将图像和视频帧编码为 patch 特征。图像处理采用单张降采样全局裁剪加最多 K 个重叠局部裁剪的方式以处理高分辨率；视频以 2 fps 采样，最多支持 128 帧（长上下文版本可扩展至 384 帧）。

**视觉-语言连接器**：通过多头注意力池化（multi-head attention pooling）对 ViT 的多尺度特征进行聚合与投影，生成固定数量的视觉 token。

**大语言模型**：分别基于 Qwen3 和 OLMo 3 构建不同变体（Molmo2-4B/8B 和 Molmo2-O-7B）。LLM 接收交叉排列的视觉 token 和文本 token，自回归生成文本输出。

**定位输出表示**：模型以紧凑的文本格式输出归一化坐标、时间戳和对象 ID，统一支持计数、指向和追踪任务。例如，指向任务输出归一化的空间坐标序列，追踪任务额外输出帧时间戳和对象 ID 以维持身份关联。

### 关键设计决策与因果机制

整个流水线的核心瓶颈突破在于**视频 grounding 数据的规模化构建与多任务联合训练**。通过人类口述字幕、人机协作 QA、以及从现有分割/检测数据转换，Molmo2 创建了 7 个新数据集（Molmo2-Cap 平均每视频 924 词，为目前最密集的视频字幕数据集），填补了开源视频 grounding 数据的空白。这些数据与图像/NLP 数据统一训练，配合 token weighting 平衡长/短输出任务，使开放模型无需从专有 VLM 蒸馏即可获得强大的视频时空定位能力。

消融实验（Table 8）系统验证了各设计的作用：联合训练其他视频数据可改善视频字幕性能；双向注意力、token 加权和时间 token 均显著提升性能；Molmo2-Cap 和 Molmo2-QA 均优于仅使用学术数据集；视频+帧融合字幕（VF）至关重要。

### 补充图表

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2601_10611/figures/004_Figure_2.jpg]]
*Figure 2: Molmo2 follows the standard design of connecting a vision encoder and a language model to process video inputs*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2601_10611/figures/044_Figure_18.jpg]]
*Figure 18: Overview of the annotation pipeline for Molmo2-VideoTrack and the Molmo2-Track benchmark*

## 核心模块与公式推导

Molmo2 的模型架构遵循“视觉编码器 → 视觉-语言连接器 → 大语言模型”的标准设计，并在训练流程中引入多项关键技术创新。本节聚焦于对性能有决定性影响的模块与公式。

### 视觉-语言连接器与多尺度特征处理

Molmo2 采用 SigLIP 2 作为视觉编码器（ViT）将图像和视频帧编码为 patch 特征。连接器模块通过**多头注意力池化**（multi-head attention pooling）压缩 ViT 的多尺度特征，生成固定数量的视觉 token（Figure 2）。

对于高分辨率图像，Molmo2 使用单张降采样裁剪图加上最多 K 个重叠裁剪图（overlapping crops）进行拼接处理。视频则以 2 fps 采样，最多支持 128 帧（短视频）或 384 帧（长上下文训练），所有帧的视觉 token 与文本 token 交叉排列后送入 LLM。

### 双向视觉注意力机制

传统 VLM 中，视觉 token 通常仅具有前向（causal）注意力。Molmo2 的一项关键改进是**允许不同帧/图像之间的视觉 token 进行双向注意力**（bidirectional attention）。消融实验（Table 8b）证实，这一设计能显著提升视频字幕和 QA 性能。其直觉在于：视频帧之间存在天然的时序关联，双向注意力使模型能够跨帧聚合上下文信息，而非仅依赖单向的时序累积。

### 序列打包与消息树掩码

为提升训练吞吐量并避免无效填充，Molmo2 开发了**动态序列打包算法**（on-the-fly packing）。该算法将多个短示例合并为单一长序列，并通过**消息树掩码**（message tree masking）阻止跨分支的注意力泄露（Figure 3）。具体而言：
- 不同训练示例之间完全屏蔽交叉注意力；
- 同一示例内不同 QA 对之间也屏蔽交叉注意力；
- 帧 token 保留前向注意力以维持时序因果性。

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2601_10611/figures/003_Figure_3.jpg]]
*Figure 3: Attention mask for a packed sequence with two examples. The first contains two QA pairs for one image. Frame tokens (dark pink) have forward attention, while masking blocks cross-attention between different examples (lower-left empty block) and between distinct QA pairs within the same example (upper empty block)*

### 点与轨迹的紧凑文本表示

Molmo2 将空间定位信息编码为紧凑的文本格式，使 LLM 能够直接生成 grounding 输出：
- **点坐标**：归一化到 [0, 100] 范围的 `(x, y)` 值；
- **时间戳**：以秒为单位的帧时间标记；
- **对象 ID**：用于追踪任务的身份标识。

这种表示使得计数、指向和追踪任务可以统一为文本生成问题，无需额外的检测头或分割模块。

### 任务定制 Token 加权

多任务联合训练的核心挑战在于平衡长短输出任务的学习。Molmo2 采用差异化的损失权重策略：

- **视频字幕**：固定权重 **0.1**
- **指向任务**（pointing）：固定权重 **0.2**
- **其余任务**：采用动态启发式权重

$$w = \frac{4}{\sqrt{n}}$$

其中 $n$ 为答案 token 数量。该公式的设计动机是：短答案任务（如 VQA）的每个 token 携带更高信息密度，需要更高权重以防止被长文本任务（如密集字幕）淹没；而长答案任务的权重随长度衰减，避免单个长序列主导梯度更新。平方根形式在两者之间取得平衡，经验上优于均匀权重或线性衰减。

### 计数近似准确度

在视频计数评估中，Molmo2 采用容差机制判断预测正确性：

$$|pred - gt| \leq \Delta, \quad \Delta = 1 + \lfloor 0.05 \times gt \rfloor$$

其中 $pred$ 为预测计数，$gt$ 为真实计数。该公式允许误差随真实计数线性增长（5% 相对容差 + 1 绝对容差），避免对高计数场景过于严苛。例如，真实值为 20 时允许误差 ≤ 2，真实值为 100 时允许误差 ≤ 6。

### 高阶追踪准确率 HOTA

对于需要输出追踪 ID 的模型，Molmo2 采用 HOTA（Higher Order Tracking Accuracy）指标：

$$HOTA = \sqrt{DetA \times AssA}$$

其中 $DetA$ 为检测准确率（衡量定位精度），$AssA$ 为关联准确率（衡量身份一致性）。该公式的几何平均形式确保两者缺一不可——模型必须同时准确定位目标并正确关联跨帧身份，才能获得高 HOTA 分数。对于不输出稳定追踪 ID 的 VLM，则仅报告逐帧点 F1 分数。

### 关键模块的消融证据

| 模块/技术 | 消融发现 | 证据锚点 |
|-----------|----------|----------|
| 双向视觉注意力 | 显著提升视频字幕和 QA 性能 | Table 8b |
| Token 加权 | 显著提升整体性能 | Table 8b |
| 时间 token | 显著提升性能 | Table 8b |
| 序列打包 | 提升训练吞吐量，无性能损失 | Section 3.2 |
| 预训练中移除图像指向 | 导致基准小幅下降 | Table 18 |

这些模块共同构成了 Molmo2 从数据到训练的系统性创新，使其在保持通用视觉语言能力的同时获得强大的视频 grounding 能力。

## 实验与分析

### 核心结果总览

Molmo2在视频理解、grounding和追踪三个维度上均展现出强大的竞争力，尤其在开放权重模型中表现突出。其核心优势源于完全开放的大规模视频grounding数据构建与三阶段多任务联合训练策略。

在**视频计数**任务上，Molmo2-8B在Molmo2-VideoCount基准上达到35.5%的准确率，显著超越开放权重基线Qwen3-VL-8B的29.6%（+5.9个百分点）。在**视频指向**任务上，Molmo2-8B的F1分数达到38.4，远超专有模型Gemini 3 Pro的20.0（+18.4个百分点），证明了开放数据驱动的grounding能力可以超越依赖蒸馏的专有系统。在**视频追踪**方面，Molmo2-8B在Molmo2-Track基准上取得56.2的J&F分数，相比Gemini 3 Pro的41.1提升15.1个百分点。

这些结果表明，Molmo2通过构建大规模、多样化的视频grounding数据（密集字幕、时空指向、对象追踪），结合精心设计的训练策略，成功打破了开放模型在细粒度时空定位能力上的瓶颈。

### 视频理解与字幕

表2展示了Molmo2在多个视频理解、字幕和计数基准上的综合表现。在MVBench和MotionBench等通用视频理解基准上，Molmo2超越了此前的开放权重模型。在视频字幕方面，Molmo2-Cap数据集平均每视频924词，是现有最密集的字幕数据集（对比Video Localized Narratives的75词和LLaVA-Video-178K的547词），为模型提供了丰富的视觉-语言对齐信号。

值得注意的是，Molmo2-4B在视觉计数和字幕任务上仅被最强的闭源系统（如Gemini 3.0）超越，显示出小规模模型在高质量数据驱动下也能获得强大的视频理解能力。

### 视频Grounding：计数与指向

表3详细呈现了视频计数与指向的结果。在BURST-VC和Molmo2-VP基准上，Molmo2均取得最高分；在Molmo2-VC的近似准确率上略低于Gemini 2.5 Pro，但整体表现仍然强劲。计数评估采用近似准确度标准：当$|pred - gt| \leq \Delta$，其中$\Delta = 1 + \lfloor 0.05 \times gt \rfloor$时，预测视为正确。

指向任务的成功得益于Molmo2-VideoPoint数据集的构建，该数据集通过人机协作和从现有分割/检测数据转换，覆盖了广泛的视觉概念和时空场景。

### 视频追踪

表4展示了学术基准上的追踪结果。对于专用分割模型报告J&F指标，对于能逐帧生成点的VLM报告F1点准确率，对于提供追踪ID的模型报告HOTA追踪准确率（$HOTA = \sqrt{DetA \times AssA}$）。Molmo2在多个追踪基准上表现出色，表5进一步按视频域细分了Molmo2-Track的结果，显示模型在不同场景类型下均保持稳定的追踪能力。

### 图像能力保持

表6和表7分别展示了图像理解/计数基准和Point-Bench图像指向结果。Molmo2在保持强大视频能力的同时，并未牺牲图像理解性能：在MMBench、MMMU、MathVista等主流图像基准上与专有模型保持竞争力，在图像指向任务上也取得了领先成绩。这表明三阶段训练策略（图像预训练→联合多模态SFT→长上下文SFT）有效地实现了能力的正向迁移。

### 关键消融分析

#### 视频字幕专业化（Table 8a）
联合训练其他视频数据可显著改善视频字幕性能。仅使用视频字幕数据训练的模型性能明显低于加入多样化视频任务（QA、指向、追踪）的联合训练模型，验证了多任务学习对视频理解的促进作用。

#### 建模技术贡献（Table 8b）
双向注意力、token加权和时间token三项技术均显著提升性能。具体而言：
- **双向注意力**：允许不同帧/图像间的视觉token双向交互，增强了时序建模能力
- **Token加权**：视频字幕权重0.1，指向任务权重0.2，其余任务采用$\frac{4}{\sqrt{n}}$动态权重（n为答案token数），有效平衡了长/短输出任务的学习
- **时间token**：显式的时间戳表示帮助模型建立时序关联

#### SFT数据构成（Table 8c）
Molmo2-Cap和Molmo2-QA两个自建数据集均优于仅使用学术数据集，证明了人机协作数据收集策略的有效性。

#### 字幕数据形式（Table 8d）
使用视频+帧融合字幕（VF）至关重要，相比单独使用视频级或帧级字幕均有显著提升。

#### 计数与指向策略（Table 9a-c）
- **先指向后计数**远优于直接预测计数：让模型先定位目标对象再统计数量，大幅提高了计数准确率
- **同时使用Molmo2-VideoPoint和AcademicVideoPoint**达到最佳整体性能
- **对中高计数示例上采样**有利于计数和指向任务

#### 追踪任务混合（Table 10a）
训练中加入指向任务有助于追踪性能，表明空间定位能力可正向迁移至时序追踪。

#### 长上下文SFT（Table 11）
长上下文后训练显著提升了长视频QA基准上的表现，验证了序列打包和消息树编码在扩展上下文窗口方面的有效性。

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2601_10611/figures/019_Table_11.jpg]]
*Table 11: Long-context SFT ablation. Columns show the average of our 12 video benchmarks divided by short/long video benchmarks, using validation sets for EgoSchema, PerceptionText, and MLVU, video captioning F1, the average of the 11 image benchmarks using validation sets for InfoQA, DocQA, ChartQA, VQA v2, and AI2D*

### 预训练阶段影响

移除预训练中的图像指向任务会导致基准性能小幅下降（Table 18），说明早期阶段的空间定位能力对后续视频grounding学习具有奠基作用。

### 失败模式与局限性

尽管整体表现优异，Molmo2仍存在以下已知失败模式：

1. **视频Grounding退化**：在指向和追踪任务中，模型有时会在单帧上生成大量重复点，尤其对高频对象或长视频场景。这可能是多任务联合训练中的任务干扰所致。

2. **指标上限受限**：视频grounding整体不如图像grounding稳健，计数和指向指标均未超过40%，可能受限于视觉编码器（SigLIP 2）的分辨率不足及缺乏视频预训练。

3. **长视频Grounding支持有限**：训练数据以2fps采样，最长支持128/384帧，对3分钟以上视频的grounding标注对齐无法保证。

4. **追踪点飘移**：目标追踪中，输出点的位置可能飘移，原因是点生成管道未保证每帧的一致性。

5. **长文本重复**：生成长视频字幕时，使用贪婪解码可能出现重复文本问题，尤其当输出几千token后。

6. **编程能力下降**：Molmo2在编程基准（如MBPP+）上相比基座语言模型有明显下降，可能源于多模态训练对纯文本能力的干扰。

这些失败模式为后续研究指明了方向：开发完全开放数据的图像编码器、改进视频grounding的一致性约束、扩展长视频支持，以及优化多任务训练中的能力平衡。

### 补充图表

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2601_10611/figures/015_Table_8.jpg]]
*Table 8: Video ablations. For ablations (a)(b)(c) we train models on only video data; ablation (d) has models with only video captions*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2601_10611/figures/005_Table_2.jpg]]
*Table 2: Video benchmark results for a range of proprietary APIs, open-weight baselines, video-specialized models, and our Molmo2 family across video understanding, captioning, and counting benchmarks. The result of the best-performing open-weight model is in bold, and the second best is underlined*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2601_10611/figures/007_Table_4.jpg]]
*Table 4: Tracking Results on Academic Benchmark. J &F is reported for specialized segmentation or points-tosegmentation models. F1 is the point accuracy measured for VLMs that can generate points per frame. HOTA [97] is the tracking accuracy that accounts for association accuracy for models that provide tracking IDs*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2601_10611/figures/008_Table_5.jpg]]
*Table 5: Tracking results on Molmo2-Track by video domain. Overall is the accuracy across all samples*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2601_10611/figures/009_Table_6.jpg]]
*Table 6: Image benchmark results for a range of proprietary APIs, open-weight baselines, and our Molmo2 family across image understanding and counting benchmarks. The result of the best-performing open-weight model is in bold. The Molmo1 models do not support multi-image input, so those evaluations are left blank*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2601_10611/figures/010_Table_7.jpg]]
*Table 7: Point-Bench results1 baseline scores taken from the Point-Bench leaderboard. Qwen3-VL-235B-A22B-Instruct and VisionReasoner-7B scores were taken from their evaluation in Poivre [171], which did not include sub-category scores*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2601_10611/figures/017_Table_9.jpg]]
*Table 9: Counting and pointing ablations. BVC represents Burst-VideoCount accuracy; and MVC and MVP are Molmo2-VideoCount accuracy and Molmo2-VideoPoint F1 on the validation sets*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2601_10611/figures/018_Table_10.jpg]]
*Table 10: Tracking ablations. We report average metrics across the five tracking benchmarks (the valid-u split for MeViS). HOTA [97] measures association accuracy*

## 方法谱系与知识库定位

### 1. 在开放视频-语言模型谱系中的位置

Molmo2 的核心定位是**完全开放权重与数据的视频-语言模型**，其区别于现有工作的关键特征在于：不依赖专有VLM进行数据蒸馏，而是通过人机协作和学术数据转换构建大规模视频grounding训练语料。

在开源视频-语言模型生态中，Molmo2的直接对比对象包括：
- **Qwen3-VL**：开源权重模型，但在视频grounding能力上显著落后于Molmo2（视频计数准确率29.6 vs 35.5）。
- **InternVL3.5**、**GLM-4.1V**、**MiniCPM-V**：同为开源权重视频-语言模型，但论文未报告它们在视频grounding（指向、追踪）上的系统对比，这些模型通常缺乏专门的时空定位训练数据。
- **Molmo1**：Molmo系列的前代模型，不支持多图像输入和视频理解，Molmo2在此基础上扩展了视频grounding能力。

与专有模型的对比揭示了Molmo2的突破点与边界：
- **Gemini 2.5 Pro / Gemini 3 Pro / GPT-5 / Claude Sonnet 4.5**：在视频指向F1上，Molmo2-8B（38.4）大幅超越Gemini 3 Pro（20.0）；在追踪J&F上，Molmo2-8B（56.2）也显著优于Gemini 3 Pro（41.1）。这表明开放数据驱动的grounding训练可以超越依赖大规模内部数据的专有系统。然而，在视频计数准确率上，Molmo2-8B（35.5）仍略低于Gemini 2.5 Pro，说明在细粒度计数任务上仍有差距。

### 2. 方法创新的因果机制

Molmo2的方法创新围绕一个核心因果链展开：**开放数据构建 → 多任务联合训练 → 统一输出空间 → 视频grounding能力涌现**。

**数据瓶颈的突破**：现有开源视频模型缺乏高质量grounding数据的根本原因在于标注成本高、覆盖范围窄。Molmo2通过三条路径破解这一瓶颈：
1. **人类口述字幕**（Molmo2-Cap）：利用两阶段流水线（先描述短片段，再总结全视频），辅以预定义问题引导标注者关注动态视觉细节，产出了平均每视频924词的最密集字幕数据集。
2. **人机协作QA**（Molmo2-AskModelAnything、Molmo2-CapQA等）：结合人类标注与模型辅助生成，扩展自由形式问答的覆盖范围。
3. **学术数据转换**（Molmo2-VideoPoint、Molmo2-VideoTrack）：从现有分割/检测数据集转换生成时空指向和追踪标注，将已有视觉概念迁移到grounding任务。

**训练机制的因果贡献**：消融实验（Table 8-11）揭示了几个关键因果节点：
- **三阶段训练**（预训练→联合SFT→长上下文SFT）是性能的基础架构：跳过预训练中的图像指向会导致基准小幅下降（Table 18），而长上下文后训练显著提升长视频QA性能（Table 11）。
- **双向注意力**允许不同帧/图像间的视觉token交互，是视频理解的关键使能技术（Table 8b）。
- **Token加权策略**（视频字幕权重0.1，指向任务权重0.2，其余任务采用 $\frac{4}{\sqrt{n}}$ 动态权重）解决了长短输出任务训练不平衡的问题，对视频字幕和QA性能有显著改善（Table 8b）。
- **序列打包与消息树编码**（Figure 3）通过动态打包多个示例到单一序列并利用消息树掩码阻止跨分支注意力，提升了训练吞吐量，是工程层面的关键优化。

### 3. 适用边界与局限

Molmo2的能力边界受限于以下几个因素：

**视觉编码器的开放性问题**：Molmo2使用SigLIP 2作为图像编码器，该模型并非完全开放数据训练，这导致整个pipeline在“完全开放”声明上存在缺口。论文明确将此列为局限，并提出未来需要开发完全开放数据的图像编码器。

**数据生成的透明度**：在数据构建过程中使用了闭源LLM辅助生成，降低了数据收集流程的完全透明性。这一问题在Molmo2-AskModelAnything等数据集中尤为突出。

**视频grounding的稳健性不足**：
- 视频指向和追踪有时输出退化，例如在单帧上生成大量重复点，尤其对高频对象或长视频。
- 整体grounding指标偏低：计数准确率35.5、指向F1 38.4，均未超过40%。论文推测这可能受限于视觉编码器的分辨率及缺乏视频预训练。
- 长视频（>3分钟）grounding支持有限，因为训练数据仅限于2fps采样且无法保证帧-标注对齐。
- 目标追踪中输出点的位置可能发生飘移，可能源于点生成管道未保证每帧的一致性。

**长文本生成的退化**：在生成长视频字幕时，使用贪婪解码可能出现重复文本问题，尤其当输出超过几千token后。

**编程能力的退化**：Molmo2在编程基准（如MBPP+）上相比基座语言模型有明显下降，表明多模态训练可能对代码生成能力产生负面影响。

### 4. 开放问题与未来方向

Molmo2的工作揭示了以下待解决的关键问题：

1. **全开放数据管道的构建**：能否开发完全开放数据的图像编码器替代SigLIP 2？未来开放LLM能否完全取代闭源LLM用于数据生成？这是实现“完全开放”承诺的核心挑战。

2. **视频grounding退化输出的根因分析**：追踪和指向中的退化输出是否因多任务联合训练中的任务间干扰导致？如何通过训练策略或架构设计缓解这一问题？

3. **视频grounding指标的根本性提升**：当前<40%的指标是否主要受限于低帧率处理（2fps）和视觉编码器缺乏视频预训练？增大帧数或结合SlowFast编码与长上下文训练能否带来显著提升？

4. **长视频grounding的扩展**：如何有效扩展grounding支持到更长的视频（>3分钟）并保持帧-标注对齐？这可能需要新的数据采集策略和训练范式。

5. **身份感知追踪的改进**：对于不输出稳定追踪ID的VLM，如何改进身份感知的追踪指标（HOTA）？这涉及输出格式和评估方法的协同设计。

6. **长上下文SFT的泛化性**：长上下文SFT对其他未列出的视频任务（如动作检测、事件定位）影响如何？这需要更广泛的基准评估。

7. **多模态训练对语言能力的侵蚀**：Molmo2在编程基准上的下降是否普遍存在于多模态训练中？如何通过训练数据混合或训练策略减轻这种负面影响？

## 原文 PDF

![[paperPDFs/CVPR_2026/Molmo2_Open_Weights_and_Data_for_Vision_Language_Models_with_Video_Understanding_and_Grounding.pdf]]