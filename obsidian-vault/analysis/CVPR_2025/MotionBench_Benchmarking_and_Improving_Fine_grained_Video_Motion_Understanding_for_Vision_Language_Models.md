---
title: "MotionBench: Benchmarking and Improving Fine-grained Video Motion Understanding for Vision Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/MotionBench_Benchmarking_and_Improving_Fine_grained_Video_Motion_Understanding_for_Vision_Language_Models.pdf
project_link: https://motion-bench.github.io
code_link: null
aliases:
- TFTEF
- MotionBench
tags:
- CVPR_2025
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "在视觉编码器内部引入深层帧间融合机制（TE Fusion中的分组自注意力），使得模型在压缩视频特征时能够更充分地提取帧间时间依赖关系，从而在固定解码器序列长度下显著提升运动感知能力。"
primary_logic: "深层融合（Through-Encoder Fusion）通过在视觉编码阶段对相邻帧进行分组自注意力，实现了帧间特征的深度交互，从而在不增加LLM输入长度的前提下增加了可处理的帧数，有效缓解了高帧率需求与计算成本之间的矛盾。"
claims:
- "主流视频语言模型在MotionBench上的准确率均低于60%，细粒度运动理解能力明显不足。"
- "TE Fusion以9B的LLM主干实现了与72B模型相当甚至更好的运动理解性能，验证了方法的高效性。"
- "在相同的LLM输入序列长度下，TE Fusion在MVBench上以k=4取得了72.1的准确率，远超无压缩baseline的64.5，并全面优于其他压缩方法。"
- "当压缩比达到16（极端压缩）时，TE Fusion在MotionBench上依然保持强大性能，远高于其他压缩方法，表明深层融合对高压缩比场景具有独特优势。"
---

# MotionBench: Benchmarking and Improving Fine-grained Video Motion Understanding for Vision Language Models

> [!tip] 核心洞察
> 深层融合（Through-Encoder Fusion）通过在视觉编码阶段对相邻帧进行分组自注意力，实现了帧间特征的深度交互，从而在不增加LLM输入长度的前提下增加了可处理的帧数，有效缓解了高帧率需求与计算成本之间的矛盾。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MotionBench：面向视觉语言模型的细粒度视频运动理解基准测试与改进 |
| 英文题名 | MotionBench: Benchmarking and Improving Fine-grained Video Motion Understanding for Vision Language Models |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2501.02955) · [Project](https://motion-bench.github.io) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | TE Fusion (Through-Encoder Fusion) |
| Dataset | MotionBench Dev, MVBench, VideoMME (short) |

> [!tip] 效果简介
> - MotionBench Dev 上，Accuracy (多选正确率) 为 0.58 (TE Fusion, 16 frames, 9B LLM)，对比 0.57 (Qwen2VL-72B, 1fps, 最佳现有模型)，变化 +0.01。
> - MVBench 上，Accuracy 为 72.1 (TE Fusion k=4, 4输入帧)，对比 64.5 (无压缩 baseline, 4帧)，变化 +7.6。
> - VideoMME (short) 上，Accuracy 为 61.0 (TE Fusion k=4, 4输入帧)，对比 51.4 (无压缩 baseline, 4帧)，变化 +9.6。

## 概要

现有视频视觉语言模型（Video VLMs）在细粒度运动理解方面存在严重瓶颈：主流模型在MotionBench基准上的准确率普遍低于60%（Table 3），其根本原因在于大语言模型（LLM）的序列长度限制阻碍了高帧率输入的实现，而当前主流的视频特征压缩方法仅依赖浅层融合（shallow fusion），难以有效消除帧间冗余并保留关键运动信息。

针对这一瓶颈，本文提出**Through-Encoder Fusion (TE Fusion)**，一种在视觉编码器内部进行深层帧间融合的视频特征压缩范式。其核心机制是在视觉编码阶段对相邻帧进行分组自注意力（group-level self-attention），使整个编码过程具备时间感知能力，从而在固定解码器序列长度下显著提升运动感知能力。该方法在不增加LLM输入长度的前提下增加了可处理的帧数，有效缓解了高帧率需求与计算成本之间的矛盾。

在方法谱系中，TE Fusion区别于三类主流压缩范式：**Pre-Encoder Fusion**（如Qwen2-VL，在编码器前沿通道维度拼接邻近帧）、**Post-Encoder Fusion**（如QFormer、PLLaVA、Kangaroo，在编码器后使用QFormer或池化进行时间压缩）以及无压缩的Baseline。TE Fusion将融合深度推进至编码器内部，实现了更彻底的帧间特征交互。

主要实验结果验证了方法的有效性：
- TE Fusion以9B的LLM主干在MotionBench Dev上达到0.58的准确率，与72B的Qwen2VL-72B（0.57）相当甚至更优（Table 3）。
- 在MVBench上，TE Fusion（k=4）取得72.1的准确率，远超无压缩Baseline的64.5，并全面优于其他压缩方法（Table 4）。
- 当压缩比达到16（极端压缩）时，TE Fusion在MotionBench上依然保持强大性能，远高于其他压缩方法，表明深层融合对高压缩比场景具有独特优势（Table 8）。

视频理解是当前多模态大模型研究的核心方向之一。然而，现有视频视觉语言模型（Video VLMs）在细粒度运动理解方面表现严重不足——在MotionBench基准测试中，主流模型的准确率普遍低于60%（Table 3）。这一瓶颈的根源在于，精细的运动感知（如动作顺序、重复计数、相机运动识别）要求模型能够捕获帧与帧之间的细微时序变化，而这通常需要高帧率输入作为支撑。

高帧率输入带来的直接挑战是计算成本与上下文长度的双重膨胀。大语言模型（LLM）解码器的序列长度有限，直接输入大量未经压缩的视频帧会迅速耗尽上下文窗口。因此，视频特征压缩成为必然选择。当前主流的压缩范式可分为三类：**编码前融合**（Pre-Encoder Fusion，如Qwen2-VL将邻近帧沿通道维度拼接）、**编码后融合**（Post-Encoder Fusion，如QFormer、PLLaVA、Kangaroo在视觉编码器输出后进行时序聚合），以及**无时间融合的逐帧处理**（Baseline）。这些方法的共同缺陷在于，它们仅依赖**浅层融合**（shallow fusion）——帧间交互要么发生在编码之前，要么发生在编码之后，而视觉编码器内部各帧保持独立处理。浅层融合难以有效消除帧间冗余，同时无法在编码过程中充分提取帧间时间依赖关系，导致压缩后的特征丢失关键运动信息。

这一结构性缺陷在高压缩比场景下尤为突出：当压缩比增大时，浅层融合方法的性能快速下降，无法在有限的解码器输入长度内保留足够的运动线索。因此，如何在固定LLM序列长度的约束下，实现高效且运动感知能力强的视频特征压缩，成为提升细粒度运动理解能力的关键突破口。本文正是在这一背景下，提出**Through-Encoder Fusion（TE Fusion）**——一种在视觉编码器内部引入深层帧间融合的新范式，旨在从根本上解决浅层融合的局限性。

## 核心方法与创新机理

本文的核心创新在于提出了一种**深层帧间融合范式——Through-Encoder Fusion (TE Fusion)**，以解决现有视频视觉语言模型（VLM）在细粒度运动理解中的根本瓶颈。

### 瓶颈分析：高帧率需求与序列长度约束的矛盾

现有视频VLM在细粒度运动理解上表现严重不足。在MotionBench基准测试中，主流模型准确率普遍低于60%（Table 3），其核心瓶颈在于：**有限的大语言模型（LLM）序列长度限制了高帧率输入的实现**。为了在固定上下文窗口内处理更多帧，现有方法普遍采用视频特征压缩，但这些压缩方法仅依赖**浅层融合（shallow fusion）**——要么在视觉编码器前（pre-encoder）拼接相邻帧，要么在编码器后（post-encoder）进行聚合——视觉编码器内部各帧仍独立处理，难以有效消除帧间冗余并保留关键运动信息。

### 关键创新：深层融合范式（TE Fusion）

TE Fusion 的核心设计在于**将时间融合深度嵌入视觉编码器内部**，具体体现为以下关键变化：

**1. 融合深度与位置的变革（Changed Slot）**

| 维度 | 基线方法（浅层融合） | TE Fusion（深层融合） |
|------|---------------------|----------------------|
| 融合位置 | 编码器前（如Qwen2-VL的通道拼接）或编码器后（如QFormer、PLLaVA、Kangaroo） | 视觉编码器内部，贯穿整个编码过程 |
| 融合机制 | 简单的帧间聚合或池化，各帧在编码器内独立前向 | 对分组后的相邻帧执行**分组自注意力（group-level self-attention）**，实现帧间特征深度交互 |
| 时间感知能力 | 编码阶段无时间感知，仅在输入/输出端进行浅层操作 | 整个编码过程具备时间感知能力，能更彻底地捕获帧间冗余 |

具体而言，TE Fusion 在视觉编码阶段将相邻帧划分为大小为 $k$ 的组，并在组内应用自注意力机制（Sec 4）。随后，对每组 $k$ 帧进行时空压缩，得到紧凑的视频表示。这一设计使得模型在不增加LLM输入序列长度的前提下，能够处理更多原始帧，从而缓解高帧率需求与计算成本之间的矛盾。

**2. 对压缩比的鲁棒性提升（Changed Slot）**

浅层融合方法在压缩比增大时性能快速下降——压缩比越高，丢失的运动信息越多。TE Fusion 展现出对高压缩比的强鲁棒性：

- 当 $k \leq 4$ 时，TE Fusion 几乎无性能下降（Fig 6）
- 当压缩比达到 $k=16$（极端压缩）时，TE Fusion 在 MotionBench 上依然保持强大性能，远高于其他压缩方法（Table 8）
- 在 MVBench 和 VideoMME-short 上，$k=4$ 的表现甚至优于 $k=2$，表明适度的深层压缩可能通过增强帧间建模带来额外收益

### 方法论谱系与知识库定位

TE Fusion 在视频VLM压缩方法谱系中占据独特位置：

- **Pre-Encoder Fusion**：如 **Qwen2-VL**，在编码前将邻近帧沿通道维度拼接，编码器内部仍逐帧独立处理
- **Post-Encoder Fusion**：如 **QFormer**（使用可学习查询进行时间融合）、**PLLaVA**（自适应池化压缩）、**Kangaroo**（统一时空切分），均在编码器输出后进行压缩
- **Through-Encoder Fusion（本文）**：在编码器内部进行深层帧间融合，是唯一在编码阶段即实现时间感知的范式

TE Fusion 以 GLM4-9B 作为LLM主干，在 MotionBench 上取得了0.58的准确率（Dev AVG），超越了使用72B LLM的 Qwen2VL-72B（0.57），验证了深层融合范式的高效性（Table 3）。在相同的LLM输入序列长度下，TE Fusion（$k=4$）在 MVBench 上取得72.1的准确率，远超无压缩baseline的64.5（Table 4），进一步证明了深层融合在固定解码器预算下的显著优势。

MotionBench 论文提出了一套“评测驱动改进”的双轨框架：一方面构建细粒度视频运动理解基准 **MotionBench**，另一方面针对评测暴露出的瓶颈设计 **Through-Encoder Fusion (TE Fusion)** 压缩架构。整体流程从视频输入到答案生成，可拆解为以下模块及其数据流关系。

### 评测基准：MotionBench 的数据管线

MotionBench 的构建遵循严格的质量控制流程（Table 2）：
1. **视频收集与分类**：根据来源、场景生动性和复杂度将视频划分为三类——带有复杂交互的真实视频、特定领域视频（如医疗操作）和虚拟合成视频。
2. **问题设计**：围绕六类核心运动理解能力设计多选题——运动识别（MR）、位置相关运动（LM）、相机运动（CM）、运动相关对象（MO）、动作顺序（AO）和重复计数（RC）。
3. **静态帧过滤**：使用多个图像 VLM 仅基于首帧进行预测，剔除所有可凭单帧或常识回答的问题，确保基准真正测量时序运动理解能力（Sec 3.1）。
4. **人工校验**：经过多轮人工审核，最终得到高标注密度的数据集（Annotation Density = 68.4，约为现有基准的两倍），其定义为问题总长度与视频时长之比：$$\mathrm{Annotation Density} = \frac{\mathrm{Total\ length\ of\ questions}}{\mathrm{Video\ duration}}$$

### 视频语言模型的通用管线与压缩瓶颈

现有视频 VLM 遵循如图 5 所示的通用架构：
1. **视觉编码器**：将输入视频帧独立编码为视觉特征。
2. **时间压缩模块**：对帧级特征进行下采样，以控制输入大语言模型（LLM）的序列长度。
3. **模态对齐投影层**：将压缩后的视觉特征映射到 LLM 的嵌入空间。
4. **LLM 解码器**：基于多模态上下文生成答案。

核心瓶颈在于：LLM 的序列长度限制迫使模型在固定解码器输入长度下压缩视频特征。主流压缩方法仅依赖**浅层融合**——要么在编码器前拼接帧（Pre-Encoder Fusion，如 Qwen2-VL），要么在编码器后使用 QFormer、自适应池化或统一时空切分（Post-Encoder Fusion，如 PLLaVA、Kangaroo），视觉编码器内部各帧仍独立处理。这种浅层交互难以有效消除帧间冗余并保留关键运动信息，导致现有模型在 MotionBench 上准确率普遍低于 60%（Table 3）。

### TE Fusion：深层融合的压缩架构

TE Fusion 的核心创新在于将时间融合**深度嵌入视觉编码器内部**，改变了压缩模块与编码器的交互方式。其管线如下（Sec 4）：

1. **帧分组模块**：将输入视频的 $N_{\mathrm{input}}$ 帧按相邻关系划分为大小为 $k$ 的组，$k$ 即为压缩比。
2. **视觉编码器（含分组自注意力）**：在编码过程中，对每组内的 $k$ 帧执行**分组自注意力**（group-level self-attention），使帧间特征在整个编码阶段持续交互。每一帧仍单独前向，但注意力计算跨越组内所有帧，实现深层时间融合。
3. **时空压缩模块**：编码器输出后，对每组 $k$ 帧进行时间维度下采样，将 $k$ 帧特征压缩为紧凑表示。最终 LLM 解码器的输入序列长度为：$$L_{\mathrm{decoder}} = \frac{N_{\mathrm{input}} \times l}{k}$$ 其中 $l$ 为单帧的 token 长度。
4. **模态对齐投影层**与**LLM 解码器**：与通用架构一致，将压缩特征映射后输入 GLM4-9B 等解码器生成答案。

这一设计的关键洞察是：通过编码阶段的深度帧间交互，TE Fusion 在不增加 LLM 输入长度的前提下，以更高的原始帧率捕获运动信息。当 $k \le 4$ 时，性能几乎无下降；即使在 $k=16$ 的极端压缩下，TE Fusion 在 MotionBench 上仍显著优于其他压缩方法（Table 8），验证了深层融合对高压缩比场景的独特优势。

### 方法总览

TE Fusion 的核心设计是在视觉编码阶段引入分组自注意力，使帧间融合从传统的浅层（编码器前或编码器后）推进到编码器内部，从而在固定 LLM 解码器输入长度的约束下，更有效地压缩视频特征并保留细粒度运动信息。

### 关键模块

**1. 帧分组模块**

将输入的 $N_{\text{input}}$ 帧按时间顺序划分为若干组，每组包含 $k$ 个相邻帧。分组后的帧组作为视觉编码器中自注意力计算的基本单元。分组大小 $k$ 即为压缩比，控制着最终输入 LLM 的 token 数量。

**2. 视觉编码器（含分组自注意力）**

这是 TE Fusion 的核心创新所在。在视觉编码器的每一层中，自注意力计算被限制在每组 $k$ 帧内部进行，而非在所有帧之间全局计算。具体而言，对于每组内的 $k$ 帧，它们的 patch 特征在编码器各层中通过自注意力机制进行深度交互，使得编码过程全程具备时间感知能力。每一帧仍然保持独立的前向传播路径，仅在注意力计算时与同组帧进行信息交换。

**3. 时空压缩模块**

在视觉编码器输出后，对每组 $k$ 帧在时间维度上进行下采样或池化操作，将 $k$ 帧的视觉特征压缩为一帧的表示。这一步骤将视觉 token 数量从 $N_{\text{input}} \times l$ 压缩至 $\frac{N_{\text{input}}}{k} \times l$，其中 $l$ 为每帧的 patch 数量。

**4. 模态对齐投影层**

将压缩后的视觉特征映射到 LLM 的嵌入空间，使其能够作为多模态上下文被 LLM 解码器理解。

**5. 大语言模型解码器**

接收压缩后的视觉 token 与文本 token 拼接后的序列，生成最终答案。论文中采用 GLM4-9B 作为 LLM 主干。

### 关键公式

**LLM 解码器输入长度公式**

给定压缩比 $k$，LLM 解码器的视觉 token 输入长度由下式确定：

$$L_{\text{decoder}} = \frac{N_{\text{input}} \times l}{k}$$

其中：
- $N_{\text{input}}$ 为输入视频的原始帧数
- $l$ 为视觉编码器输出的每帧 patch 数量
- $k$ 为压缩比（即每组包含的帧数）

该公式揭示了 TE Fusion 的核心权衡：在 $L_{\text{decoder}}$ 固定的约束下（由 LLM 上下文窗口决定），增大压缩比 $k$ 可以允许输入更多的原始帧 $N_{\text{input}}$，从而提升对高帧率视频的处理能力。实验表明，当 $k \leq 4$ 时，TE Fusion 几乎无性能下降；即使在 $k = 16$ 的极端压缩下，仍能保持较强的运动理解性能（Table 8），而其他浅层融合方法在此压缩比下性能急剧衰减。

**标注密度公式**

MotionBench 数据集的标注密度定义为：

$$\text{Annotation Density} = \frac{\text{Total length of questions}}{\text{Video duration}}$$

MotionBench 的标注密度达到 68.4，约为现有基准的两倍，反映了其问题标注的细粒度和高信息密度。

## 实验与关键发现

### 核心瓶颈验证：现有模型在MotionBench上的整体表现

论文首先通过大规模基准测试揭示了当前视频视觉语言模型在细粒度运动理解上的严重不足。在MotionBench的开发集（Dev）上，几乎所有主流模型的平均准确率均低于60%（Table 3）。即便是表现最佳的**Qwen2VL-72B**，以1fps的帧率输入，其Dev AVG也仅为0.57。这一结果直接印证了本文的核心论断：现有的视频理解模型在运动层面的感知能力存在明显瓶颈，无法可靠地处理需要精细时序推理的任务。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2501_02955/figures/009_Table_3.jpg]]
*Table 3: Evaluation results of the existing video VLMs. Abbreviations: MR (Motion Recognition), LM (Location-related Motion), CM (Camera Motion), MO (Motion-related Objects), AO (Action Order), RC (Repetition Count). We randomly split MotionBench into “dev” and “test”. We will release the ground truth answers in the “dev” set and set up an online platform for results submission in the “test” set*

进一步分析各任务维度的得分可以发现，模型在不同运动理解子任务上的表现极不均衡。在“动作顺序”（Action Order, AO）和“重复计数”（Repetition Count, RC）这两个高度依赖细粒度时序建模的任务上，几乎所有模型的表现都接近随机猜测水平。唯一的例外是**GLM-4V-9B + TE Fusion**和**GLM-4V-plus**，它们在RC任务上分别取得了0.39和0.37的准确率，显著高于其他模型，这表明深层时序融合机制对于捕捉周期性运动模式具有独特优势。

### 主实验结果：TE Fusion的性能优势

TE Fusion在多个基准上展现了显著且一致的性能提升，其核心优势体现在以较小的模型规模实现了超越大模型的表现。

在MotionBench Dev上，基于GLM4-9B主干的TE Fusion（16帧输入）取得了0.58的平均准确率，超越了72B参数量的Qwen2VL-72B（0.57），实现了以9B模型对抗72B模型的高效性能（Table 3）。这一结果强有力地证明了，通过深层编码器融合来优化视频特征表示，可以比单纯扩大语言模型规模更有效地提升运动理解能力。

在通用视频理解基准上的对比进一步验证了TE Fusion的泛化能力。在MVBench上，当解码器输入帧数固定为4时，TE Fusion（k=4）取得了72.1的准确率，相比无压缩baseline的64.5提升了7.6个百分点（Table 4）。在VideoMME短视频子集上，同样的配置下TE Fusion取得了61.0的准确率，较baseline的51.4提升了9.6个百分点。这些结果表明，深层融合带来的帧间特征交互不仅有利于细粒度运动理解，也能提升通用视频理解任务的性能。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2501_02955/figures/011_Table_4.jpg]]
*Table 4: Benchmark results for different compression methods at various compression rates, all using the same sequence length in the VLM decoder. We set $\begin{array} { r } { \frac { N _ { \mathrm { i n p u t } } } { k } = \bar { 4 } . } \end{array}$ , with the baseline representing video models that process 4 frames without compression. Note that each compression method is re-implemented on the GLM-4V-9B backbone to ensure a fair comparison

### 压缩比鲁棒性：深层融合的核心优势

TE Fusion最突出的特性在于其对高压缩比的卓越鲁棒性，这是其区别于所有浅层融合方法的关键优势。

在固定解码器输入帧数为16的条件下，系统性地改变压缩比k（从2到16）的实验揭示了不同方法的本质差异（Figure 6, Table 8）。TE Fusion在k ≤ 4时几乎无性能下降，在MotionBench上的表现保持稳定。更令人关注的是，在MVBench和VideoMME-short上，k=4的TE Fusion表现甚至优于k=2，这表明适度的深层压缩可能通过强制模型学习更具判别力的帧间关系而带来额外收益。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2501_02955/figures/010_Figure_6.jpg]]
*Figure 6: Model performance variation with respect to different compression ratios k = 2 , 4 , 8 , 1 6 , given a fixed VLM input frame count of $N _ { \mathrm { i n p u t } }$ = 1 6 The pink dotted line represents the performance of the baseline model, which processes 16 frames without temporal compression. Note that each compression method is re-implemented on the GLM-4V-9B backbone to ensure a fair comparison*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2501_02955/figures/015_Table_8.jpg]]
*Table 8: Model performance variation with respect to different compression ratios k = 2, 4, 8, 16, given a fixed VLM input frame count of $N _ { \mathrm { i n p u t } }$ = 1 6 . Note that each compression method is re-implemented on the GLM-4V-9B backbone to ensure a fair comparison*

当压缩比增大到极端值16时，方法间的差异变得极为显著。TE Fusion在MotionBench上依然保持了较高的性能水平，而其他压缩方法（如Qwen2-VL的预编码融合、PLLaVA的后编码池化）的性能则出现了断崖式下滑。这一对比揭示了浅层融合方法的根本局限：仅在编码器外部进行简单的帧间聚合，无法有效消除高压缩比下的信息损失。TE Fusion通过在视觉编码器内部进行分组自注意力，使得每一层Transformer都能感知帧间时序关系，从而在压缩过程中保留了关键的运动信息。

### 方法对比：深层融合vs.浅层融合范式

Table 4和Table 8系统比较了TE Fusion与多种主流视频压缩方法在相同解码器序列长度约束下的表现。对比方法涵盖了视频压缩的三种主要范式：

- **后编码融合（Post-Encoder Fusion）**：包括QFormer、PLLaVA的自适应池化、Kangaroo的统一时空切分。这些方法在视觉编码器完成逐帧独立编码后才进行时序聚合，帧间交互发生在最浅层。
- **预编码融合（Pre-Encoder Fusion）**：以Qwen2-VL为代表，在编码器前将相邻帧沿通道维度拼接。这种方法虽然让编码器看到了多帧信息，但融合深度有限，且在高压缩比下通道维度的信息混合效率下降。
- **深层编码融合（Through-Encoder Fusion）**：本文提出的TE Fusion，在视觉编码器的每一层对分组帧执行自注意力，实现了贯穿整个编码过程的深层时序交互。

实验结果表明，在相同的LLM输入序列长度下，TE Fusion在所有压缩比设置下均全面优于其他方法。特别是在k=4的典型设置下，TE Fusion在MVBench上的72.1准确率远超第二名方法。这一系统性优势验证了深层融合范式的有效性：将时序建模从编码器外部移入编码器内部，是实现高效视频特征压缩的关键设计选择。

### 深层融合机制的因果效应分析

TE Fusion的性能优势可以从信息瓶颈的角度进行因果解释。在传统的浅层融合方法中，视觉编码器对每一帧独立编码，帧间冗余只能在编码器输出后的压缩阶段被消除。这种“先编码、后压缩”的流程导致了一个根本性问题：编码器在逐帧处理时无法感知哪些信息是帧间冗余的，因此会在每一帧的表示中保留大量重复信息，而这些冗余在后续的浅层压缩中难以被有效识别和消除。

TE Fusion通过在编码器内部引入分组自注意力，改变了这一信息流动模式。在每一层Transformer中，同一组内的k帧可以相互访问彼此的特征，使得模型能够在编码的早期阶段就识别并抑制帧间冗余，同时增强运动相关的时序特征。这种“边编码、边融合”的机制使得最终输出的视频表示更加紧凑且信息密集，从而在相同的LLM输入长度约束下传递了更丰富的运动信息。

这一机制也解释了为什么TE Fusion在高压缩比下具有独特优势：当k增大时，浅层方法在编码器输出端面临的信息损失是“一次性且不可恢复的”，而TE Fusion的深层融合使得信息筛选贯穿整个编码过程，每一层都有机会保留关键的时序线索，从而在极端压缩下仍能维持可接受的性能。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2501_02955/figures/003_Table_1.jpg]]
*Table 1: The comparison of existing video VLM benchmarks with MotionBench. MotionBench collects various video sources including web videos and synthetic videos, and provides a new evaluation perspective in motion level perception*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2501_02955/figures/012_Table_6.jpg]]
*Table 6: The model configurations of all ablated architectures*


## 定位与知识库关联

### 视频运动理解中的压缩范式谱系

当前视频视觉语言模型（Video VLM）在细粒度运动理解上的瓶颈，根源于一个核心矛盾：**高帧率输入对捕获精细运动至关重要，但LLM解码器的序列长度限制使得直接输入大量帧变得不可行**。围绕这一矛盾，现有方法在“何时进行时间融合与压缩”这一关键设计选择上形成了三条技术路线，TE Fusion 则代表了第四条——深层融合路线。

**Pre-Encoder Fusion（编码前融合）**：以 **Qwen2-VL** 为代表。该方法在视觉编码器之前，将邻近帧沿通道维度拼接，试图在编码入口处注入时间信息。其局限在于融合深度不足——通道拼接仅提供静态的、线性的帧间组合，编码器内部各帧仍以独立方式处理，无法形成深层的帧间交互。实验证据表明，当压缩比增大时，Qwen2-VL 的性能快速下降（Fig. 6），说明浅层的预编码融合不足以在压缩过程中保留关键运动特征。

**Post-Encoder Fusion（编码后融合）**：这是目前最主流的范式，包括 **QFormer**、**PLLaVA**（自适应池化压缩）和 **Kangaroo**（统一时空切分压缩）等。这些方法在视觉编码器完成逐帧独立编码后，再对帧序列进行时间维度的聚合或压缩。其共同缺陷在于：视觉编码阶段完全缺乏时间感知，编码器输出的每一帧特征都仅包含单帧的空间信息，后续的压缩模块只能在“已成定局”的特征上进行事后补救。当压缩比增大时，这种先独立编码再强行压缩的策略不可避免地丢失帧间运动线索。

**TE Fusion（Through-Encoder Fusion，编码中融合）**：本文提出的方法将融合深度推进到视觉编码器内部。核心操作是**帧分组自注意力**——将输入视频帧划分为大小为 $k$ 的组，在视觉编码器的自注意力层中，每组内的 $k$ 帧执行分组级别的自注意力计算。这意味着编码器的每一层都能感知到组内帧间的时间依赖关系，整个编码过程从始至终都是时间感知的。编码完成后，再对每组 $k$ 帧进行时空压缩，将 $k$ 帧压缩为紧凑的视频表示。

### 关键设计差异与因果机制

TE Fusion 与三条基线路线的本质差异在于**时间融合的深度与位置**（changed_slot 1），这一差异直接决定了方法对压缩比的鲁棒性（changed_slot 2）。

| 范式 | 融合位置 | 融合机制 | 编码器时间感知 | 高压缩比鲁棒性 |
|------|---------|---------|-------------|-------------|
| Pre-Encoder (Qwen2-VL) | 编码前 | 通道拼接 | 无 | 弱 |
| Post-Encoder (QFormer/PLLaVA/Kangaroo) | 编码后 | QFormer/池化/切分 | 无 | 弱 |
| **TE Fusion** | **编码中** | **分组自注意力** | **全程感知** | **强** |

因果链条如下：**深层融合 → 编码器内部帧间特征交互 → 压缩时可利用已融合的时间信息 → 高压缩比下运动特征得以保留**。消融实验提供了强有力的因果证据：在固定 LLM 输入序列长度为 4 的条件下，TE Fusion 在 MVBench 上取得 72.1 的准确率，远超无压缩 baseline 的 64.5（Table 4, k=4），说明深层融合不仅在压缩时保留了信息，甚至通过增强帧间建模带来了额外收益。更关键的是，当压缩比达到 16（极端压缩）时，TE Fusion 在 MotionBench 上依然保持强大性能，远高于其他压缩方法（Table 8），验证了深层融合对高压缩比场景的独特优势。

### 适用边界与局限

**适用场景**：
1. **高压缩比需求**：当 LLM 上下文窗口紧张，需要将大量输入帧压缩为少量 token 时，TE Fusion 是最优选择。实验显示 $k \leq 4$ 时几乎无性能下降（Fig. 6）。
2. **细粒度运动理解**：MotionBench 上的 SOTA 表现（0.58 vs Qwen2VL-72B 的 0.57，Table 3）表明 TE Fusion 对需要精确感知运动方向、速度、时序的任务特别有效。
3. **中小规模 LLM 骨干**：以 9B 的 GLM4-9B 骨干实现与 72B 模型相当的性能，说明 TE Fusion 在计算资源受限场景下具有高效性。

**已知局限**：
1. **极端压缩比下的性能衰减**：虽然 TE Fusion 在 $k=16$ 时仍优于其他方法，但相对于 $k=4$ 仍有性能下降，说明深层融合无法完全消除极端压缩带来的信息损失。
2. **Repetition Count 任务的普遍困难**：即使 TE Fusion 在 Repetition Count 上取得 0.39 的准确率（Table 3），显著高于其他模型，但绝对值仍然较低，表明重复动作计数对当前所有方法都是严峻挑战。
3. **分组内帧数固定**：当前设计假设每组 $k$ 帧执行独立的自注意力，组间不进行交互。对于跨越组边界的长期运动模式，这种设计可能无法充分捕获。

### 开放问题

1. **组间交互机制**：当前 TE Fusion 仅在组内进行自注意力，组间完全独立。引入跨组的稀疏注意力或层次化时间建模是否能进一步提升长期运动理解能力？

2. **分组策略的自适应**：$k$ 值目前作为超参数固定。是否可以根据视频内容的运动复杂度自适应调整分组大小——运动剧烈的片段用较小的 $k$ 保留细节，静态片段用较大的 $k$ 节省计算？

3. **与预训练策略的协同**：TE Fusion 改变了视觉编码器的内部计算图，这是否需要对应的预训练策略调整？当前实验基于已有预训练权重微调，从头预训练 TE Fusion 架构是否会有更大收益？

4. **Repetition Count 的突破路径**：所有模型在该任务上接近随机水平，说明现有架构可能缺乏对周期性模式的归纳偏置。引入显式的时序计数模块或频域特征是否必要？

5. **计算开销的精确量化**：深层融合在编码器中引入了分组自注意力，虽然不增加 LLM 输入长度，但会增加编码阶段的计算量。这一开销与性能收益的 Pareto 前沿尚未被系统刻画。

## 原文 PDF

![[paperPDFs/CVPR_2025/MotionBench_Benchmarking_and_Improving_Fine_grained_Video_Motion_Understanding_for_Vision_Language_Models.pdf]]
