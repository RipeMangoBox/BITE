---
title: Bridging Facial Understanding and Animation via Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Bridging_Facial_Understanding_and_Animation_via_Language_Models.pdf
project_link: "https://songluchuan.github.io/TDMM-LM/"
code_link: null
aliases:
- TLTD3MMLM
- BFUALM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将面部动作建模为离散几何令牌序列，绕过图像像素，利用大规模合成文本-3D面部参数配对训练LLM，实现双向面部理解与生成。
primary_logic: 面部表情的动态变化可以通过低维的3D几何参数（3DMM）有效表示，这些参数经向量量化后形成紧凑的序列令牌，能保留微表情的时序细节，且每个帧仅需一个令牌，从而在语言模型框架内高效地进行面部行为的理解与合成。
claims:
- 在Motion2Language任务中，几何令牌模型在情感（CorE）、运动（CorM）等指标上全面超越HumanOmni和Gemini-2.5 VLM。
- 本方法每帧仅使用1个几何令牌，而传统VLM每帧需300-500个图像令牌，显著降低令牌消耗并提升时序响应能力。
- 在Open3DFaceVid上训练显著优于MEAD和YouTube数据集，Motion2Language的CorE达到3.97，Language2Motion实现最佳几何保真度与文本对齐的权衡。
- Motion2Language (几何输入) 上 Cor_E ↑ (GPT-4) = 4.02
---

# Bridging Facial Understanding and Animation via Language Models

> [!tip] 核心洞察
> 面部表情的动态变化可以通过低维的3D几何参数（3DMM）有效表示，这些参数经向量量化后形成紧凑的序列令牌，能保留微表情的时序细节，且每个帧仅需一个令牌，从而在语言模型框架内高效地进行面部行为的理解与合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | TDMM-LM：通过语言模型桥接面部理解与动画 |
| 英文题名 | Bridging Facial Understanding and Animation via Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.16936) · [Project](https://songluchuan.github.io/TDMM-LM/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TDMM-LM (Text-Driven 3D Morphable Model Language Model) |
| Dataset | Motion2Language, Language2Motion |

> [!tip] 效果简介
> - Motion2Language (几何输入) 上，Cor_E ↑ (GPT-4) 4.02 vs 2.45 (Gemini-2.5 VLM) (+1.57)。
> - Motion2Language (自然图像输入) 上，Cor_E ↑ (GPT-4) 4.02 vs 4.21 (Gemini-2.5 VLM) (-0.19)。
> - Language2Motion 上，L2 ↓ 0.219 vs 0.226 (T2M-GPT) (-0.007)。

## 概要

### 问题瓶颈

现有大规模视觉语言模型（VLM）在面部理解与动画生成任务中面临根本性瓶颈：它们依赖逐帧图像分词，每帧需要300–500个图像令牌，导致面部微表情和动态时序信息在密集的视觉令牌流中丢失。同时，训练语料中情感类别严重不平衡，缺乏细粒度的文本-面部运动配对数据，制约了模型对面部行为的语义理解与生成能力。

### 核心洞察与因果机制

本工作提出**TDMM-LM**（Text-Driven 3D Morphable Model Language Model），其核心洞察是：面部表情的动态变化可以通过低维的3D几何参数（3DMM）有效表示。这些参数经向量量化后形成紧凑的离散几何令牌序列——每帧仅需**1个令牌**——能保留微表情的时序细节，从而在语言模型框架内高效地进行面部行为的双向理解与合成。这一设计绕过了图像像素层级，使LLM能够直接对3D面部运动进行推理。

### 方法定位

TDMM-LM在方法谱系中占据独特位置：

- **区别于视觉语言模型**：**HumanOmni**（Zhao et al., arXiv 2025）和**Gemini-2.5 VLM**（Gemini Team et al., arXiv 2023）等基线直接消费图像令牌，而TDMM-LM以几何令牌替代，显著降低令牌消耗并提升时序响应能力。
- **区别于文本-动作生成模型**：**T2M-GPT**（Zhang et al., CVPR 2023）和**T2M-X**（Liu et al., arXiv 2024）等基线面向人体动作生成，TDMM-LM则专注于面部动画，并通过词级语言前缀注入预训练LLM嵌入，实现文本对局部面部运动的精细控制。
- **知识库贡献**：引入**Open3DFaceVid**——约80小时的合成面部运动语料库，覆盖187个情感类别，是目前最大规模的文本-3D面部参数配对数据集。

### 主要结果

在Motion2Language任务中，几何令牌模型在情感正确性（CorE）指标上达到**4.02**，大幅超越HumanOmni（2.45）和Gemini-2.5 VLM（2.45），提升达+1.57（Table 1）。在Language2Motion任务中，模型在几何保真度（L2=0.219）与文本-运动对齐（CorE=4.13）之间实现了最优权衡（Table 3）。消融实验证实，在Open3DFaceVid上训练显著优于MEAD和YouTube数据集，Motion2Language的CorE达到3.97（Table 4）。

**需要手动验证**：自然图像输入场景下，本方法在CorE上略低于Gemini-2.5 VLM（4.02 vs 4.21，Table 2），但考虑到每帧仅使用1个几何令牌而Gemini需要300–500个图像令牌，该结果反而凸显了几何表示的令牌效率优势。合成数据域偏差对真实场景泛化能力的影响尚需进一步评估。

面部行为是人类交流的核心载体，承载着情感、意图和社交信号。近年来，大规模视觉语言模型（VLLM）在通用视觉理解任务上取得了显著进展，但在面部行为理解与生成这一特定领域仍面临根本性瓶颈。

**核心瓶颈：逐帧图像分词导致微表情与动态时序信息丢失。** 现有VLLM（如**HumanOmni**（Zhao et al., arXiv 2025）、**Gemini-2.5 VLM**（Gemini Team et al., arXiv 2023））将视频处理为独立图像帧序列，每帧需消耗300–500个图像令牌。这种逐帧离散化策略存在双重缺陷：其一，大量令牌被用于编码静态纹理、光照和背景等与面部动态无关的信息，造成严重的计算冗余；其二，帧间微表情的连续变化——如嘴角的细微抽动、眉梢的短暂上扬——在像素级分词过程中被平滑或丢失，导致模型难以捕获时序依赖关系。

**数据层面的结构性缺陷加剧了上述问题。** 现有面部视频数据集（如MEAD仅含8个情感类别，YouTube数据集含37个情感类别）存在严重的情感类别不平衡：大部分样本为中性表情，极端或复合情感（如“苦涩的微笑”“压抑的愤怒”）的样本极度稀缺。此外，这些数据集缺乏细粒度的文本-面部运动配对标注，难以支撑语言与面部行为之间的精确对齐学习。

**本文的核心动机在于绕开像素瓶颈。** 面部表情的动态变化本质上可由低维3D几何参数（3D Morphable Model, 3DMM）有效表示——表情的起承转合、强度变化和时序演化均编码在紧凑的参数轨迹中。基于此洞察，本文提出**TDMM-LM**（Text-Driven 3D Morphable Model Language Model），将面部运动建模为离散几何令牌序列：每帧仅需1个令牌即可保留微表情的时序细节，在语言模型框架内实现高效的双向面部理解与生成。同时，构建了约80小时的合成语料库**Open3DFaceVid**，覆盖187个情感类别，提供迄今最大规模的文本-3DMM轨迹配对数据，从数据层面缓解情感不平衡与标注稀疏问题。

## 核心方法与创新机理

本工作提出 **TDMM-LM (Text-Driven 3D Morphable Model Language Model)**，其核心创新在于用**低维离散几何令牌**替代传统视觉语言模型中的高维图像令牌，在语言模型框架内实现面部运动理解与生成的双向统一。以下从三个关键“changed slots”展开。

### 1. 面部运动表示：从图像令牌到几何令牌

现有大规模视觉语言模型（如 **HumanOmni** (Zhao et al., arXiv 2025) 和 **Gemini-2.5 VLM** (Gemini Team et al., arXiv 2023)）依赖逐帧原始视频作为输入，每帧需消耗 300–500 个图像令牌。这种密集的像素级表示不仅计算开销大，更关键的是**丢失了面部微表情的动态时序信息**——图像分词器并非为捕捉精细的肌肉运动而设计，导致对微妙表情变化的感知能力不足。

TDMM-LM 从根本上改变了这一范式：通过 **Geometry VQ-VAE** 将 3D 面部几何参数（FLAME 3DMM）量化到离散码本中，**每帧仅需 1 个几何令牌**。这一设计背后的因果机制在于：面部表情的动态变化本质上可由低维的 3D 几何参数有效表示，向量量化后的紧凑序列令牌能保留微表情的时序细节，同时大幅压缩了令牌长度。实验证据表明，在 Motion2Language 任务中，几何令牌模型在情感正确性（Cor_E）等指标上全面超越 HumanOmni 和 Gemini-2.5 VLM（Table 1），而令牌消耗仅为后者的 1/300–1/500。

### 2. 训练数据：从情感不平衡到大规模合成配对语料

传统面部视频数据集（如 MEAD 仅含 8 个情感类别，YouTube 含 37 个）存在**情感类别严重不平衡、标注稀疏**的问题，大部分视频内容为中性表情，缺乏细粒度的文本-面部运动配对数据。这直接制约了模型对面部行为语义的理解与生成能力。

本工作构建了 **Open3DFaceVid**，一个约 80 小时的合成面部运动语料库，包含 **187 个情感类别**（Figure 9），通过程序化提示多款 Text-to-Video 基础模型生成多样化面部视频，并提取每帧 3DMM 参数形成文本-3D 轨迹配对。消融实验提供了决定性证据：在 Motion2Language 任务中，Open3DFaceVid 上训练的模型 Cor_E 达到 3.97，远超 MEAD（3.03）和 YouTube（2.74）（Table 4）；在 Language2Motion 任务中，Open3DFaceVid 实现了几何保真度与文本-运动对齐之间的最佳权衡（Table 5）。这一结果表明，**大规模、情感平衡的合成配对数据**是解锁面部语言模型表达能力的关键因果杠杆。

### 3. 处理流程：从单向消费到双向统一框架

传统流程中，LLM 仅作为图像令牌的被动消费者，无法主动生成面部运动。TDMM-LM 通过 **Geometry VQ-VAE 令牌化 + LLM 微调** 的统一架构，同时支持两个方向的任务：

- **Motion2Language**：输入几何令牌序列，LLM 直接生成自然语言描述，实现面部运动理解。模型仅依赖几何令牌即可“推理”出正确的情绪和运动语义（Figure 5）。
- **Language2Motion**：以词级语言前缀为条件，自回归变换器预测未来几何令牌，驱动面部动画生成。这种前缀融合方式保留了提示词的结构，使单个词能够引导局部面部运动（Figure 6）。

双向能力的统一源于一个核心洞察：**面部运动与语言之间的映射可以在离散令牌空间中建立**。几何令牌作为面部行为的“符号化观测”，使得 LLM 能够像处理文本一样处理面部运动，从而在单一框架内实现理解与生成。

### 令牌效率的深层意义

值得特别强调的是，TDMM-LM 在自然图像输入下（Table 2）的 Cor_E 为 4.02，略低于 Gemini-2.5 VLM 的 4.21（差距仅 0.19），但这是在**每帧仅使用 1 个令牌**的条件下取得的——Gemini 每帧消耗 300–500 个令牌。这一对比揭示了几何令牌表示的极端效率：单个几何令牌所承载的面部语义信息量，已接近数百个图像令牌的信息密度。这种紧凑性不仅降低了计算开销，更重要的是**使模型能够处理更长的时序上下文**，这对于理解缓慢展开的微表情序列至关重要。

### 局限与待验证边界

尽管几何令牌范式展现出显著优势，仍需注意其当前边界：（1）数据集完全由合成生成，对真实世界中光照、遮挡、非正面姿态等复杂因素的泛化能力尚未充分评估；（2）模型未利用音频信息，缺乏多模态面部表达理解能力；（3）几何令牌丢弃了纹理等视觉细节，可能削弱对细粒度外观差异的捕捉。这些限制指明了未来工作的方向——结合真实视频域适应、融合音频模态、以及探索几何令牌与视觉特征的协同表示。

TDMM-LM 围绕一个核心洞察构建：面部表情的动态变化可以通过低维的3D几何参数（3DMM）有效表示，经向量量化后形成紧凑的序列令牌，每帧仅需一个令牌即可保留微表情的时序细节。基于此，整个框架将面部理解与动画统一在语言模型的范式之下，形成双向的信息流动。

**数据集构建 → 几何令牌化 → 双向任务**，三者构成完整闭环：

1. **Open3DFaceVid 数据集**：通过多款基础文本到视频（T2V）模型合成约80小时的面部视频语料，覆盖187个情感类别。随后从视频中恢复FLAME 3DMM参数，形成大规模文本-3D面部轨迹配对数据，解决现有语料情感不平衡、缺乏细粒度文本-运动配对的瓶颈（Figure 1 左面板、Figure 3）。

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2603_16936/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed Open3DFaceVid dataset and 3D facial understanding/animation pipeline. The left panel visualizes the Open3DFaceVid corpus, which covers a wide range of identities, emotions, and speaking styles generated via text-to-video (T2V) models. The right panel illustrates our interactive 3D facial interface: given a 3DMM sequence, the user prompts the agent to describe expressions and head motion in natural language, and the agent returns fine-grained, parameter-based interpretations. In the reverse direction, the agent is able to condition on user prompts to generate new 3DMM trajectories with controllable emotion and pose. Please refer to https://songluchuan.github.io/TDMM-...*

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2603_16936/figures/004_Figure_3.jpg]]
*Figure 3: Dataset overview. Top two rows: starting from a fixed text prompt, we vary the random seed and emphasize different prompt keywords to modulate facial identity and video attributes, showcasing subjects across different genders. Bottom three rows: we recover FLAME facial parameters and pair the resulting trajectories with the corresponding prompt, forming Text–3DMM dataset*

2. **Geometry VQ-VAE**：将3DMM序列量化到离散码本中，直接在重建的面部几何上操作，生成紧凑的几何令牌。该模块在网格空间上受 $\mathcal{L}_1$ 损失监督，确保令牌保留面部运动的感知一致性（Figure 4）。这是整个框架的表示枢纽——它绕过了传统VLM每帧300-500个图像令牌的冗余，将面部动态压缩为每帧1个令牌。

3. **Motion2Language（面部理解）**：几何令牌序列作为符号化观测输入LLM，LLM在文本-运动配对样本上微调后，直接生成自然语言描述，实现从面部运动到语义理解的映射（Figure 5）。

4. **Language2Motion（面部动画）**：以词级语言前缀为条件，将预训练LLM嵌入注入自回归面部运动Transformer，逐令牌预测未来几何令牌，驱动3D面部动画生成。前缀融合保留了提示词的结构，使个别词语能够引导局部面部运动（Figure 6）。

**输入输出流**：在理解方向，输入为3DMM序列经VQ-VAE编码的离散令牌流，输出为自然语言描述；在生成方向，输入为自然语言提示词经LLM嵌入后的前缀，输出为自回归预测的几何令牌序列，最终解码为3D面部动画。两个方向共享同一几何令牌码本，形成统一的面部行为理解与合成框架。

> **注意**：当前框架完全基于合成数据训练，未利用音频信息，对真实场景中光照、遮挡、非正面姿态等因素的适应能力尚未充分验证，这些限制需在实际应用中加以考虑。

### 3D面部几何表示

TDMM-LM的核心思想是将面部运动从高维像素空间转移到低维几何空间。具体而言，系统从视频帧中恢复FLAME 3D可变形模型（3DMM）参数，包括表情系数、姿态系数和形状系数。这些参数通过FLAME解码器映射为三维网格顶点位置，从而将每帧的面部状态表示为一个紧凑的几何向量，而非数百个图像令牌。

### Geometry VQ-VAE：离散几何令牌化

Geometry VQ-VAE是连接面部几何与语言模型的关键桥梁（见Figure 4）。该模块将连续的3D面部几何序列量化为离散码本中的索引，形成紧凑的几何令牌序列。

**设计动机**：直接在3DMM参数空间上进行向量量化存在困难，因为参数的不同维度对重建质量的影响权重不均。因此，TDMM-LM选择在重建后的网格顶点空间上操作——先将表情编码映射到FLAME网格，再对网格顶点位置进行编码和量化。

**工作流程**：
1. **编码**：输入面部表情编码（expression codes）经编码器映射到连续潜在表示。
2. **量化**：将潜在向量映射到离散码本中最近的码向量索引。
3. **解码**：码向量经解码器重建FLAME网格顶点位置。
4. **监督**：在网格空间上施加顶点位置的 $\mathcal{L}_1$ 损失进行重建监督。

这一设计的直接收益是令牌效率的质变——每帧仅需**1个几何令牌**，而传统视觉语言模型（如HumanOmni、Gemini-2.5 VLM）每帧需要300–500个图像令牌。这从根本上解决了逐帧图像分词导致的时序信息丢失和计算冗余问题。

### Motion2Language：面部运动理解

Motion2Language模块（见Figure 5）实现了从3D面部运动到自然语言描述的单向映射。其核心机制如下：

1. **输入处理**：一段面部视频被解析为3DMM参数序列，经Geometry VQ-VAE编码为离散几何令牌序列。
2. **LLM微调**：将几何令牌作为符号化观测输入到预训练的大语言模型中，在成对的运动-文本样本上进行微调。LLM仅以几何令牌为条件，自回归生成自然语言描述。
3. **关键特性**：由于几何令牌保留了微表情的时序细节（每帧一个令牌，序列长度等于帧数），模型能够捕捉到传统VLM因图像令牌化而丢失的动态信息。

### Language2Motion：文本驱动面部动画

Language2Motion模块（见Figure 6）实现了反向映射——从自然语言描述生成3D面部运动序列。其架构设计包含以下要点：

1. **词级语言前缀**：将用户文本提示经预训练LLM的文本分词器转换为词级令牌嵌入，形成语言前缀（language prefix）。这种词级注入方式保留了提示的结构信息，使单个词语能够引导局部面部运动。
2. **自回归运动Transformer**：以语言前缀为条件，自回归预测未来的几何令牌序列。训练时使用成对的文本-3DMM轨迹数据，通过教师强制（teacher forcing）进行监督。
3. **前缀融合的优势**：相较于将文本压缩为单一全局嵌入，词级前缀允许模型在生成不同时间步的运动时关注文本的不同部分，从而实现对“先微笑再皱眉”等时序复合指令的精确响应。

### 关键公式

系统在Geometry VQ-VAE的重建阶段使用顶点位置的 $\mathcal{L}_1$ 损失作为主要监督信号：

$$\mathcal{L}_1 = \|\mathbf{V} - \hat{\mathbf{V}}\|_1$$

其中 $\mathbf{V}$ 为FLAME解码器输出的真实网格顶点坐标，$\hat{\mathbf{V}}$ 为Geometry VQ-VAE解码器重建的顶点坐标。该损失直接在三维几何空间约束重建质量，确保离散令牌保留了足够的表情细节。

> **注意**：论文未提供完整的VQ-VAE码本损失、承诺损失（commitment loss）或Language2Motion中自回归Transformer的交叉熵损失的具体公式形式。上述 $\mathcal{L}_1$ 损失是论文明确给出的唯一公式，其余损失项需参考通用VQ-VAE和自回归语言模型的标准实践进行推断。

## 实验与关键发现

### 核心瓶颈与设计动机

现有大规模视觉语言模型（VLM）在处理面部行为时存在根本性缺陷：它们依赖逐帧图像分词，每帧产生300–500个图像令牌，不仅造成巨大的计算开销，更关键的是在令牌化过程中丢失了面部微表情的动态时序信息。此外，训练语料中情感类别严重不平衡——MEAD仅含8类情感，YouTube抽取数据约37类——且缺乏细粒度的文本-面部运动配对标注，导致模型对面部行为的理解与生成能力受限。

本文的核心洞察在于：面部表情的动态变化可以通过低维3D几何参数（3DMM）有效表示。这些参数经向量量化后形成紧凑的序列令牌，每帧仅需**1个几何令牌**，却能保留微表情的时序细节。这一表示选择构成了整个方法体系的因果旋钮——绕过图像像素，直接在几何空间进行面部行为的理解与合成。

### 数据集：Open3DFaceVid 的关键作用

Open3DFaceVid是本文构建的约80小时合成面部运动语料库，通过多款T2V模型程序化生成多样化面部视频并提取每帧3DMM参数，形成大规模文本-3D面部参数配对数据。该数据集拥有**187个情感类别**（Figure 9），远超MEAD（8类）和YouTube（37类），为模型提供了丰富的表达空间。

消融实验（Table 4, Table 5）证实了数据集质量的决定性影响：在Motion2Language任务中，Open3DFaceVid上训练的模型CorE达到**3.97**，而MEAD和YouTube分别仅为3.03和2.74；在Language2Motion任务中，Open3DFaceVid训练出的模型在几何保真度与文本-运动对齐之间实现了最佳平衡。这验证了情感平衡的大规模配对数据是面部行为语言建模的关键瓶颈。

### Motion2Language：几何令牌下的面部理解

Table 1展示了以几何图像为输入时的定量对比。本文方法在各项指标上全面超越HumanOmni和Gemini-2.5 VLM：CorE达到**4.02**（Gemini为2.45，提升+1.57），CorM达到3.35（Gemini为2.48，提升+0.87），人工评估USER_E达到4.29。这证实了几何令牌在保留微表情时序信息方面的优势——传统VLM因逐帧图像分词丢失的动态细节，在离散几何令牌序列中得以保留。

当输入切换为自然图像时（Table 2），本文方法的CorE为4.02，略低于Gemini的4.21（差距-0.19）。但需注意：本文方法每帧仅用1个几何令牌，而Gemini需要300–500个图像令牌。在令牌效率相差两个数量级的前提下，性能接近竞品，这恰恰突显了几何表示的信息密度优势。该结果同时提示，从自然图像到3DMM参数的提取环节可能引入信息损失，是当前流程的薄弱点。

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2603_16936/figures/008_Table_2.jpg]]
*Table 2: Quantitative evaluation of Motion2Language with natural images input. We employ the same correctness metric as in Table 1, while replacing geometry-image inputs with natural facial images to better adapt the evaluation setting to VLMs*

### Language2Motion：文本驱动的面部动画生成

Table 3报告了Language2Motion任务的定量结果。与T2M-GPT和T2M-X相比，本文方法在几何保真度（L2↓ 0.219 vs. T2M-GPT 0.226）和文本-运动对齐（CorE↑ 4.13 vs. T2M-GPT 3.57，提升+0.56）上均取得最优。人工评估USER分数为3.95，略高于T2M-GPT的3.91（+0.04），优势幅度较小，提示在人类感知层面，生成质量的提升空间仍然存在。

定性对比（Figure 8）进一步印证：本文模型生成的表情和头部姿态更忠实地遵循文本描述的情感语义，而基线方法在复杂情感表达上容易出现语义漂移或表情模糊。

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2603_16936/figures/012_Figure_8.jpg]]
*Figure 8: Qualitative comparison for Language2Motion. Given prompts, we visualize generated 3D facial motion from different method. Our model produces expressions and head poses that more faithfully follow the described affect*

### 规模化行为与局限性

Figure 12揭示了有趣的非对称规模化特性：Motion2Language的性能在4B–8B参数区间趋于饱和，而Language2Motion则随模型规模持续提升。这表明面部理解任务对模型容量的需求相对有限，但面部生成任务受益于更大规模的参数空间，可能涉及更复杂的时序建模和条件依赖。

当前方法存在若干明确局限：（1）训练数据完全来自合成生成，对真实场景中细微表情、光照变化、遮挡等因素的泛化能力未经验证；（2）模型未利用音频信息，无法处理视听协同的表情生成；（3）几何令牌丢失了纹理等视觉细节，可能削弱对细粒度外观差异的捕捉。这些问题指向后续研究的关键方向——域适应、多模态融合、以及几何令牌与视觉特征的互补编码。

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2603_16936/figures/009_Table_3.jpg]]
*Table 3: Quantitative evaluation of Language2Motion. Comparison with T2M-X and T2M-GPT on parameter-space measures*

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2603_16936/figures/016_Figure_13.jpg]]
*Figure 13: Language-controlled expressive ablation. We modify one keyword in prompt and let the Language2Motion model generate the corresponding facial motion. The two happy prompts produce different intensity level, while the angry prompt yields clearly distinct mouth shapes, demonstrating fine-grained text control over emotional style*

## 定位与知识库关联

### 1. 与现有基线的结构性差异

本工作提出的 **TDMM-LM** 与当前主流的面部理解与生成方法存在根本性的表示层差异，而非仅仅是模型架构的改进。

**对比基于视觉的VLM方法**：现有的面部理解系统，如 **HumanOmni** (Zhao et al., arXiv 2025) 和 **Gemini-2.5 VLM** (Gemini Team et al., arXiv 2023)，均采用逐帧图像分词策略，每帧需要300–500个图像令牌。这种密集表示导致两个瓶颈：(1) 面部微表情的时序动态信息在大量冗余像素令牌中被稀释；(2) 令牌预算的膨胀限制了长序列建模能力。TDMM-LM通过Geometry VQ-VAE将每帧压缩为**单个几何令牌**，在令牌效率上实现数量级提升，同时保留3DMM参数中的表情、姿态等关键动态信息。实验证据表明，在几何输入条件下，TDMM-LM在情感正确性指标CorE上达到4.02，显著超越Gemini-2.5 VLM的2.45（Table 1）。值得注意的是，即便在自然图像输入场景下，TDMM-LM仅凭单令牌表示便取得4.02的CorE，与Gemini-2.5 VLM的4.21差距极小（Table 2），这从侧面验证了几何令牌的表示紧凑性。

**对比基于文本的动作生成方法**：在Language2Motion任务中，基线方法 **T2M-GPT** (Zhang et al., CVPR 2023) 和 **T2M-X** (Liu et al., arXiv 2024) 均为面向人体动作的通用生成框架，其设计并未针对面部运动的特殊性进行优化。TDMM-LM引入了词级语言前缀机制，将预训练LLM的文本嵌入注入自回归面部运动变换器，使得每个词可以独立引导局部面部运动。在参数空间指标L2上，TDMM-LM达到0.219，优于T2M-GPT的0.226；在文本-运动对齐指标CorE上，TDMM-LM以4.13显著领先T2M-GPT的3.57（Table 3）。人工评估USER指标上两者接近（3.95 vs. 3.91），表明几何令牌在保持运动自然度方面具备竞争力。

### 2. 关键设计选择与因果机制

TDMM-LM的核心因果旋钮在于**将面部运动从像素空间迁移至3D几何令牌空间**，这一选择带来了连锁的机制性优势：

- **表示紧凑性**：3DMM参数经向量量化后，每帧仅需1个离散令牌，使LLM能够直接对时序几何序列进行因果推理，而非间接从像素中推断运动语义。
- **训练数据质量**：Open3DFaceVid数据集（约80小时合成语料）提供了187个情感类别的平衡覆盖（Figure 9），远超MEAD的8类和YouTube的37类。消融实验证实，在Open3DFaceVid上训练使Motion2Language的CorE达到3.97，显著优于MEAD（3.03）和YouTube（2.74）（Table 4）。
- **双向统一架构**：同一套几何令牌和LLM骨干同时支持Motion2Language（面部运动→文本描述）和Language2Motion（文本描述→面部运动），避免了传统方法中理解与生成系统相互割裂的问题。

### 3. 适用边界与失效模式

尽管TDMM-LM在受控实验中表现出色，其适用边界受以下因素制约：

**合成域偏差**：Open3DFaceVid完全由T2V模型合成生成，虽然情感类别丰富，但合成视频中的面部运动可能与真实人类行为存在系统性差异。模型对真实场景中的细微表情、非正面姿态、光照变化和遮挡等条件的泛化能力尚未经过充分验证。这一局限性使得当前模型更适用于虚拟角色驱动、游戏动画等合成场景，而非需要处理真实视频的面部分析任务。

**模态单一性**：当前框架仅使用视觉几何信息，未纳入音频模态。这意味着模型无法处理视听协同的面部表达（如语音驱动的唇形同步、语调与表情的联合建模），限制了其在数字人、虚拟主播等需要多模态对齐的场景中的应用。

**长序列上下文建模**：几何令牌虽然紧凑，但丢弃了纹理、皱纹等视觉细节。对于需要细粒度外观差异辨别的任务（如微表情识别中的皮肤纹理变化），纯几何表示可能不足以捕捉全部判别性信息。

**规模化行为差异**：消融实验揭示了一个有趣的不对称现象——Motion2Language的性能在4B–8B参数时趋于饱和，而Language2Motion则随模型规模持续提升（Figure 12）。这表明面部理解与生成任务对模型容量的需求存在本质差异，在实际部署时需要针对具体任务选择合适的模型规模。

### 4. 开放问题与未来方向

基于上述分析，以下研究方向值得关注：

1. **域适应与真实数据融合**：如何将真实视频数据（如MEAD）与合成数据结合，通过域适应或联合训练减轻合成域偏差，是提升模型在真实场景下表现的关键。

2. **多模态扩展**：将音频信息（语音、环境音）纳入统一的几何令牌框架，实现视听联合的面部表达理解与生成，将显著扩展模型的应用范围。

3. **几何令牌与视觉知识的融合**：探索将几何令牌与大规模预训练视觉模型中的知识蒸馏相结合，在保持令牌效率的同时增强语义理解深度。

4. **动态码本设计**：当前Geometry VQ-VAE使用固定大小的离散码本。动态调整码本大小或引入层级化结构，可能在表示效率与运动表现力之间取得更好的平衡，尤其对于罕见表情或极端姿态的建模。

5. **长序列与实时性权衡**：在需要处理长视频或实时交互的场景中，进一步压缩几何令牌序列（如引入时序池化或自适应帧率）同时保持运动语义完整性，是一个具有实际价值的研究问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/Bridging_Facial_Understanding_and_Animation_via_Language_Models.pdf]]
