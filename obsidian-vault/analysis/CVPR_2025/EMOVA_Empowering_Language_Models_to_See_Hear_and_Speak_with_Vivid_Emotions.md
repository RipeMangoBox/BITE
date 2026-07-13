---
title: "EMOVA: Empowering Language Models to See, Hear and Speak with Vivid Emotions"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/EMOVA_Empowering_Language_Models_to_See_Hear_and_Speak_with_Vivid_Emotions.pdf
project_link: https://emova-ollm.github.io/
code_link: null
aliases:
- EMOVA
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "语义-声学解耦的语音分词器（semantic-acoustic disentangled speech tokenizer）与轻量级风格模块。该设计将语音分离为语义内容（用于与LLM对齐）和声学风格（用于情感/音高控制），使语音单元更接近文本嵌入空间，促进了全模态对齐；同时联合训练图像文本和语音文本数据，相互增强性能。"
primary_logic: "以文本模态为桥梁进行全模态对齐时，语义-声学解耦使得跨模态对齐更自然，避免了不同模态间的冲突，甚至产生了互相促进的效果。联合训练优于顺序训练，且仅需少量全模态指令数据即可让模型学会按指定格式（如JSON）生成多模态输出。"
claims:
- "语义-声学解耦的联合训练（Joint）在视觉语言和语音任务上均优于未解耦的联合训练（Joint-entangled）及顺序训练（VL→Speech, Speech→VL）。"
- "联合对齐图像-文本和语音-文本数据可以相互提升，Joint在视觉语言和ASR指标上均超越单独的VL和Speech基线。"
- "EMOVA在15个视觉语言基准中的11个上超越GPT-4o/4V和Gemini Pro 1.5，同时在LibriSpeech WER上以2.9击败Whisper Large（3.0）和Mini-Omni2（4.8）。"
- "U2S detokenizer的情感控制有效，四种常见情绪中三种被超过80%的概率正确识别，整体识别率高于75%（基于Emotion2Vec的混淆矩阵评估）。"
---

# EMOVA: Empowering Language Models to See, Hear and Speak with Vivid Emotions

> [!tip] 核心洞察
> 以文本模态为桥梁进行全模态对齐时，语义-声学解耦使得跨模态对齐更自然，避免了不同模态间的冲突，甚至产生了互相促进的效果。联合训练优于顺序训练，且仅需少量全模态指令数据即可让模型学会按指定格式（如JSON）生成多模态输出。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | EMOVA：赋能语言模型以生动情感看、听与说 |
| 英文题名 | EMOVA: Empowering Language Models to See, Hear and Speak with Vivid Emotions |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2409.18042) · [Project](https://emova-ollm.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | EMOVA |
| Dataset | MME, MMBench, OCRBench, MathVista |

> [!tip] 效果简介
> - MME 上，score 为 2402 (EMOVA 72B)，对比 2310 (GPT-4o)，变化 +92。
> - MMBench 上，score 为 86.4 (EMOVA 72B)，对比 83.4 (GPT-4o)，变化 +3.0。
> - OCRBench 上，score 为 843 (EMOVA 72B)，对比 736 (GPT-4o)，变化 +107。

## 概要

EMOVA 旨在解决全模态大语言模型（Omni-modal LLM）领域一个核心瓶颈：现有模型要么依赖外部 TTS 工具进行语音生成，无法实现端到端的实时交互；要么使用离散视觉分词器导致视觉细节丢失，且普遍缺乏对语音情感的精细控制能力。如何在保持 SOTA 视觉语言性能的前提下，无缝整合语音模态并赋予其生动的情绪表达能力，是尚未被充分解决的难题。

EMOVA 的核心设计理念是**以文本模态为桥梁，实现语义与声学解耦的全模态对齐**。其关键因果机制在于：通过语义-声学解耦的语音分词器，将输入语音分离为语义内容（用于与 LLM 对齐）和声学风格（用于情感/音高控制），使得语音单元更接近文本嵌入空间，从而促进跨模态对齐；同时，联合训练图像-文本和语音-文本数据，不仅避免了模态间的冲突，还产生了相互增强的效果。

**主要结论与结果**：

- **视觉语言能力**：EMOVA 在 15 个视觉语言基准中的 11 个上超越 GPT-4o/4V 和 Gemini Pro 1.5，例如在 MME 上达到 2402（GPT-4o 为 2310），OCRBench 上达到 843（GPT-4o 为 736）。
- **语音能力**：在 LibriSpeech 语音识别任务上，WER 低至 2.9，优于专用模型 Whisper Large（3.0）和同类语音 LLM Mini-Omni2（4.8）。
- **情感语音生成**：U2S 解分词器支持四种基本情绪的控制，超过 80% 的合成语音被正确识别为目标情绪，整体识别率高于 75%（基于 Emotion2Vec 的混淆矩阵评估）。
- **全模态对齐效果**：联合训练在视觉语言和语音任务上均优于顺序训练及未解耦的联合训练，证实了语义-声学解耦与文本中心对齐策略的有效性。

**方法定位**：EMOVA 采用连续视觉编码器（QwenViT）保留细粒度视觉信息，结合语义-声学解耦的离散语音分词器（SPIRAL + FSQ）实现端到端语音理解与生成，并通过轻量级风格模块控制语音的情感、音高等声学属性。模型以 Qwen-2.5 为底座 LLM，提供 3B/7B/72B 三种规模的全系列开源版本。



大型语言模型（LLM）在文本理解和生成方面取得了显著进展，但要让模型真正像人类一样“看、听、说”并与世界进行多模态交互，仍然是一个核心挑战。当前的多模态LLM大多局限于视觉与文本的双模态理解，少数支持语音的模型则面临以下瓶颈：

**现有全模态模型的缺口。** 一方面，许多模型依赖外部TTS工具进行语音生成（如VITA），导致无法实现端到端的实时交互，也难以对语音风格进行精细控制。另一方面，采用离散视觉分词器的全模态模型（如AnyGPT）虽然统一了模态表示，却牺牲了视觉细节。更为关键的是，如何在保持SOTA视觉语言性能的前提下整合语音模态，并赋予模型情感表达能力，是一个未被充分解决的难题——商用模型如GPT-4o虽然展现了强大的全模态能力，但其技术细节并不公开，开源社区缺乏一个真正对标的全模态方案。

**核心瓶颈：模态对齐与风格控制。** 语音模态与文本、视觉模态之间存在天然的语义鸿沟。如果直接将未解耦的语音表示输入LLM，会迫使模型在语义理解和声学风格之间进行不必要的权衡，从而损害跨模态对齐的质量。同时，情感语音生成要求模型能够显式地感知和控制说话风格（如情绪、音高），而现有开源模型普遍缺乏这一能力。

**本文动机。** EMOVA旨在填补上述空白：通过设计语义-声学解耦的语音分词器，将语音内容与风格分离，使语音单元更接近文本嵌入空间，从而促进全模态对齐；同时以文本模态为桥梁，联合训练图像-文本和语音-文本数据，实现视觉语言与语音能力的相互增强。最终，EMOVA致力于成为首个在视觉语言和语音基准上同时达到SOTA、且支持情感口语对话的开源全模态LLM。



## 核心方法与创新机理

EMOVA 的核心创新在于以**语义-声学解耦的语音分词器**和**文本为中心的全模态联合对齐**为两个关键支点，系统性地解决了现有全模态大语言模型在语音生成、视觉保真与情感表达三者之间的根本性冲突。

### 语义-声学解耦：从“能听会说”到“情感表达”

现有全模态模型在语音生成上主要依赖两种路径：一是调用外部 TTS 工具（如 **VITA**），无法实现端到端实时交互；二是使用连续语音编码器，仅支持语音理解而不具备生成能力。EMOVA 通过一个语义-声学解耦的离散语音分词器（基于 SPIRAL 架构 + FSQ 量化，码本大小 4,096）从根本上改变了这一格局。

该分词器的核心机制是：语音编码器 $s(\cdot)$ 从输入语音 $\mathbf{X}_S$ 中同时提取语义嵌入 $\mathbf{E}_{semantic}$ 和风格嵌入 $\mathbf{E}_{style}$（见 Eq. (2)）。语义部分经量化后作为离散语音单元输入 LLM，与文本 token 共享自回归生成空间；声学风格（性别、情绪、音高）则被分离出来，通过一个轻量级风格模块（Style Encoder + 可学习原型嵌入 Codebook）独立控制。在输出端，U2S 解分词器 $d(\cdot)$ 根据 LLM 生成的语义嵌入 $\mathbf{E}_{semantic}^o$ 和风格嵌入 $\mathbf{E}_{style}^o$ 重建语音波形 $\mathbf{Y}_S^o$。

这一解耦设计的效果由 Figure 6 的混淆矩阵直接验证：在四种常见情绪中，三种被超过 80% 的概率正确识别，整体识别率高于 75%（基于 Emotion2Vec 评估）。这意味着模型不仅能“说话”，还能以可感知的情感语调说话——这是 **GPT-4o**、**Mini-Omni2** 等主流基线尚未内置的能力。

### 文本为中心的全模态联合对齐：互相促进而非此消彼长

另一个关键创新在于训练范式的转变。传统思路是顺序训练（先视觉语言再语音，或反之），但 EMOVA 的消融实验（Figure 3）揭示了两个重要发现：

1. **联合训练优于顺序训练**：Joint 在视觉语言和语音基准上均一致超越 VL→Speech 和 Speech→VL，顺序训练存在灾难性遗忘问题。
2. **解耦优于纠缠**：语义-声学解耦的 Joint 在视觉语言基准和 ASR 任务上均优于未解耦的 Joint-entangled，说明解耦使语音单元更接近文本嵌入空间，降低了跨模态冲突。

更值得注意的是 **Observation 1**：联合对齐图像-文本和语音-文本数据可以相互增强——Joint 在视觉语言和 ASR 指标上均超越单独的 VL 和 Speech 基线。这表明以文本模态为桥梁时，视觉和语音模态不仅不冲突，反而产生了正向迁移效应。

### 从架构到能力的因果链路

这些创新并非孤立存在，而是形成了一条清晰的因果链：语义-声学解耦 → 语音单元与文本嵌入空间自然对齐 → 全模态联合训练可行且互相促进 → 仅需少量全模态指令数据（EMOVA-SFT，4.4M 样本）即可让模型学会按 JSON 格式生成多模态输出（Figure 4）→ 最终在 15 个视觉语言基准中的 11 个上超越 GPT-4o/4V 和 Gemini Pro 1.5，同时在 LibriSpeech WER 上以 2.9 击败 Whisper Large（3.0）和 Mini-Omni2（4.8）（Table 2）。

需要指出的是，EMOVA 目前仍以文本模态作为语音生成的中介（先文本后语音单元），尚未实现直接的单元到单元生成，这制约了语音响应的实时性。同时，双工交流（同时听和说）与对话中动态情感感知仍是未解决的开放问题。



![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2409_18042/figures/003_Figure_2.jpg]]
*Figure 2: Model architecture of EMOVA. The vision encoder extracts continuous visual features, which are projected into the textual embedding space as visual tokens, while the input speech is encoded and quantized into discrete speech units. Given the omni-modal inputs, EMOVA can generate both textual and speech responses with vivid emotional controls. Check Sec. 3 for more architectural details*

EMOVA 的整体架构围绕一个以文本为中心的全模态对齐范式构建，其核心思想是**以文本模态作为桥梁**，将连续视觉表示与离散语音表示统一到同一个自回归语言模型的嵌入空间中。整个 pipeline 由六个关键模块串联而成，形成“编码—对齐—生成—合成”的端到端信息流。

### 输入处理流

对于视觉输入，模型采用 **QwenViT** 作为视觉编码器 $v(\cdot)$，提取连续视觉特征，再通过一个 MLP 投影器 $p(\cdot)$ 以 4 倍下采样率将特征投影到 LLM 的文本嵌入空间，形成视觉 token。这一设计保留了细粒度视觉细节，避免了离散视觉分词器（如 AnyGPT 所用方案）造成的信息损失。

对于语音输入，模型使用基于 **SPIRAL** 架构的语音编码器 $s(\cdot)$，其关键创新在于**语义-声学解耦**：编码器从输入语音 $\mathbf{X}_S$ 中同时提取语义嵌入 $\mathbf{E}_{\text{semantic}}$ 和风格嵌入 $\mathbf{E}_{\text{style}}$：

$$\{\mathbf{E}_{\text{semantic}}, \mathbf{E}_{\text{style}}\} = \mathbf{E}_S = s(\mathbf{X}_S)$$

语义嵌入随后通过有限标量量化器（FSQ）离散化为语音单元，码本大小为 4096，输入 LLM 进行处理。风格嵌入则被保留用于后续的语音合成控制。

### 核心处理：LLM 自回归生成

LLM 基座采用 **Qwen-2.5** 系列（3B / 7B / 72B 三种配置），其词表由原始文本词表与新增的语音单元词表合并而成：$V = V_T \cup V_S$。给定全模态输入 $\mathbf{U}_{\text{omni}}$（包含文本、视觉 token 和语音单元），LLM 自回归地生成输出文本 $\mathbf{U}_T^o$ 和输出语音单元 $\mathbf{U}_S^o$：

$$\mathbb{P}(\mathbf{U}_T^o, \mathbf{U}_S^o \mid \mathbf{U}_{\text{omni}}) = \prod_{i=1}^{L} \mathbb{P}(\mathbf{x}_i \mid \mathbf{U}_{T,<i}^o, \mathbf{U}_{S,<i}^o, \mathbf{U}_{\text{omni}})$$

### 输出合成与风格控制

生成的语音单元并非直接转换为波形，而是进入 **U2S 解分词器**（U2S detokenizer）$d(\cdot)$，结合 LLM 预测的风格标签对应的风格原型嵌入，合成最终语音波形：

$$\mathbf{Y}_S^o = d(\mathbf{E}_{\text{semantic}}^o, \mathbf{E}_{\text{style}}^o)$$

**轻量级风格模块**（Style Encoder + Codebook）负责将 LLM 输出的情绪标签和音高标签映射为风格嵌入，从而控制合成语音的性别、情绪和音高。这使得 EMOVA 成为首个支持**情感口语对话**的全模态 LLM（见 Table 1 的能力对比）。

### 训练策略：以文本为中心的全模态对齐

EMOVA 摒弃了“先视觉语言再语音”或“先语音再视觉语言”的顺序训练范式，转而采用**联合全模态对齐**。在预训练阶段，图像-文本数据和语音-文本数据被混合训练，使两种模态以文本为中介相互增强。消融实验（Figure 3）表明：联合训练（Joint）在视觉语言基准和 ASR 指标上均显著优于顺序训练（VL→Speech / Speech→VL），也优于使用未解耦语音表示的联合训练（Joint-entangled），证实了语义-声学解耦对全模态对齐的关键作用。

在全模态指令微调阶段，每条数据被组织为 JSON 格式，包含可选图像 $x_V$、输入语音单元 $u_S$、文本回复 $x_T^o$、预测风格标签 $c_{\text{style}}^o$ 和输出语音单元 $u_S^o$：

$$D_{\text{omi}} = \{ ( x_V, u_S, x_T^o, c_{\text{style}}^o, u_S^o )_i \}_{i=1}^{N}$$

语音响应被分解为五个步骤的链式条件概率：识别用户指令、生成文本回复、预测情绪标签、预测音高标签、生成语音单元。该数据合成自现有文本和视觉指令数据集，经过滤、清洗、风格标注和 TTS 转换后得到，总计 4.4M 条多任务全模态样本（Figure 8）。



### 整体架构与全模态生成概率

EMOVA 的架构围绕一个核心思想展开：以文本模态为桥梁，将连续视觉表示与语义-声学解耦的离散语音表示统一到 LLM 的文本嵌入空间中。模型接收的输入 $\mathbf{U}_{omni}$ 可包含文本、视觉和语音模态，LLM 自回归地生成输出文本单元 $\mathbf{U}_T^o$ 和输出语音单元 $\mathbf{U}_S^o$，其联合条件概率分解为：

$$\mathbb{P}(\mathbf{U}_T^o, \mathbf{U}_S^o | \mathbf{U}_{omni}) = \prod_{i=1}^{L} \mathbb{P}(\mathbf{x}_i | \mathbf{U}_{T,<i}^o, \mathbf{U}_{S,<i}^o, \mathbf{U}_{omni})$$

其中 $\mathbf{x}_i$ 表示第 $i$ 步生成的 token（可以是文本 token 或语音单元 token），$\mathbf{U}_{T,<i}^o$ 和 $\mathbf{U}_{S,<i}^o$ 分别表示已生成的文本和语音前缀。LLM 的词汇表由原始文本词表和新增的语音单元词表合并而成：$V = V_T \cup V_S$。

### 视觉处理管线

视觉模态采用连续编码器以避免离散化导致的信息损失。具体而言，使用 **QwenViT** 作为视觉编码器 $v(\cdot)$，提取连续视觉特征后，通过一个 MLP 视觉投影器 $p(\cdot)$ 以 4 倍下采样率将特征投影到 LLM 的文本嵌入空间，形成视觉 token。这一设计保留了细粒度视觉细节，与使用离散视觉分词器（如 AnyGPT）的方法形成对比。

### 语义-声学解耦的语音分词器

语音模态的处理是整个方法的因果关键。EMOVA 采用 **SPIRAL** 架构的语音编码器 $s(\cdot)$，从输入语音 $\mathbf{X}_S$ 中同时提取语义嵌入和风格嵌入：

$$\{\mathbf{E}_{semantic}, \mathbf{E}_{style}\} = \mathbf{E}_S = s(\mathbf{X}_S)$$

语义嵌入 $\mathbf{E}_{semantic}$ 通过有限标量量化器 FSQ 离散化为语音单元，码本大小为 4,096。这些离散单元作为 LLM 的输入和输出 token，与文本 token 共享同一自回归生成空间。风格嵌入 $\mathbf{E}_{style}$ 则捕获声学特征（如音色、情绪、音高），不参与 LLM 的 token 生成，而是传递给下游的 U2S 解分词器。

该解耦设计的因果逻辑在于：语义内容与文本嵌入空间天然接近，有利于全模态对齐；声学风格被分离后，既避免了不同模态间的表示冲突，又为情感控制提供了显式接口。

### 风格控制的语音解分词器

输出语音的合成由 U2S 解分词器 $d(\cdot)$ 完成，它接收 LLM 生成的语义嵌入 $\mathbf{E}_{semantic}^o$ 和风格嵌入 $\mathbf{E}_{style}^o$，重建语音波形：

$$\mathbf{Y}_S^o = d(\mathbf{E}_{semantic}^o, \mathbf{E}_{style}^o)$$

风格控制通过轻量级风格模块实现，包含风格编码器和风格原型码本。LLM 在生成语音单元的同时输出风格标签（情绪类别和音高等级），这些标签被映射到风格原型嵌入，驱动 U2S 解分词器合成具有目标情感和音高的语音。该模块使 EMOVA 成为首个支持情感口语对话的全模态 LLM（见 Table 1）。

### 全模态指令数据的结构化表示

在指令微调阶段，每条全模态数据以 JSON 格式组织，形式化表示为：

$$D_{omi} = \{ ( x_V, u_S, x_T^o, c_{style}^o, u_S^o )_i \}_{i=1}^{N}$$

其中 $x_V$ 为可选图像，$u_S$ 为输入语音单元，$x_T^o$ 为文本回复，$c_{style}^o$ 为预测的风格标签（情绪与音高），$u_S^o$ 为输出语音单元。语音响应过程被链式分解为五个步骤：识别用户指令、生成文本回复、预测情绪标签、预测音高标签、生成语音单元（详见附录 B.2）。这种显式的分步设计使模型能够按指定格式生成多模态输出，且仅需少量全模态指令数据即可学会。



## 实验与关键发现

### 核心结果：视觉语言与语音双SOTA

EMOVA在15个视觉语言基准中的11个上超越了GPT-4o/4V和Gemini Pro 1.5，同时在语音识别上达到可比专用模型的水平。Table 2汇总了主要对比结果：

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2409_18042/figures/006_Table_2.jpg]]
*Table 2: Comparison on vision-language and speech benchmarks. 1) EMOVA outperforms GPT-4o/4V and Gemini Pro 1.5 on 11 of the 15 vision-language benchmarks, providing a powerful open-sourced alternative. 2) Meanwhile, our EMOVA achieves state-of-the-art performance on Librispeech, surpassing its speech and omni-modal counterparts significantly. ∗: reported by [43]*

- **视觉语言能力**：EMOVA 72B在MME上取得2402分（GPT-4o为2310），在MMBench上达到86.4（GPT-4o为83.4），在OCRBench上获得843分（GPT-4o为736），在MathVista上达到69.9（GPT-4o为63.8）。EMOVA 7B在MathVerse上超越GPT-4V达+7.3分，在MME上比同期全模态模型VITA高出220分。
- **语音识别能力**：EMOVA 72B在LibriSpeech测试集上取得WER 2.9，优于专用模型Whisper Large（3.0）和语音LLM Mini-Omni2（4.8），达到端到端全模态模型中的最优水平。
- **语音合成质量**：在TTS-WER指标上，EMOVA 72B达到3.5，显著优于自身3B版本的5.8（Table 6），表明更大规模的LLM能生成更准确的语音内容。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2409_18042/figures/016_Table_6.jpg]]
*Table 6: Comparison on the ASR and TTS benchmarks*

这些结果表明，以文本为中心的全模态对齐策略不仅避免了模态间的冲突，还产生了相互促进的效果——联合训练使视觉理解和语音能力同时超越了各自的双模态基线。

### 消融分析：全模态对齐范式的关键设计

**联合训练 vs. 顺序训练**。Figure 3系统比较了四种对齐范式：仅视觉语言（VL）、仅语音（Speech）、顺序训练（VL→Speech和Speech→VL）、以及联合训练（Joint）。联合训练在视觉语言基准和ASR任务上均一致优于顺序训练方案。顺序训练存在明显的灾难性遗忘——先训练视觉再训练语音会导致视觉能力下降，反之亦然。而联合训练同时暴露图像-文本和语音-文本数据，使LLM在统一优化过程中建立了跨模态的共享表示。

**语义-声学解耦的关键作用**。Figure 3中Joint与Joint-entangled的对比揭示了解耦设计的决定性贡献。Joint-entangled使用未解耦的语音单元进行联合训练，其在视觉语言基准上明显弱于Joint，在ASR任务上的差距更为显著。这验证了核心洞察：语义-声学解耦使语音单元更接近文本嵌入空间，降低了全模态对齐的难度；未解耦的语音单元携带声学风格信息，与文本和视觉特征形成干扰，阻碍了跨模态融合。

**视觉编码器配置与模板选择**。Table 7的消融显示，使用一半深层ViT参数且学习率2e-6的QA模板在视觉语言预训练中效果最佳（MME达1838）。这一配置在视觉特征提取效率和对齐质量之间取得了平衡。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2409_18042/figures/017_Table_7.jpg]]
*Table 7: Ablation on the ViT configurations and templates for vision-language alignment*

### 情感控制的有效性验证

U2S解分词器的情感控制能力通过Emotion2Vec模型进行客观评估。Figure 6展示了生成情绪与识别情绪之间的混淆矩阵：四种常见情绪（开心、悲伤、愤怒、中性）中，三种被超过80%的概率正确识别，整体识别率高于75%。这一结果独立于LLM的文本生成质量，直接验证了风格模块对声学特征的有效调控——LLM输出的风格标签通过风格原型嵌入成功驱动了目标情绪的语音合成。

### 语音对话综合评估

Table 3报告了EMOVA-7B在四个语音对话测试集上的端到端表现。在英文场景下，端到端评分达到7.45（语音-图像）和6.85（语音-文本），风格分类的情绪准确率超过81%，音高准确率超过84%。中文场景的识别合成指标同样表现稳定，但TTS-CER相对较高（12.0），反映出中文语音合成在韵律和声调控制上的额外挑战。值得注意的是，文本输入（Text In）与语音单元输入（Unit In）之间的性能差距较小，说明语义-声学解耦后的语音单元有效保留了语义内容，使LLM能够像处理文本一样处理语音指令。

### 失败模式与局限性

尽管EMOVA在全模态对齐上取得了显著进展，仍存在以下局限：

1. **双工交互缺失**：当前模型仅支持半双工模式，无法同时进行听和说。在真实对话场景中，这意味着模型无法在用户说话时实时生成反馈或进行打断，限制了交互的自然性。
2. **文本中介瓶颈**：语音生成依赖文本作为中间表示（先识别为文本、生成文本回复、再合成语音），而非直接从语音单元生成语音单元。这增加了推理延迟，且文本到语音的转换可能丢失副语言信息。
3. **中文TTS复杂度**：中文语音合成在韵律和声调控制上的表现弱于英文（Table 3中TTS-CER偏高），说明当前风格模块对声调语言的建模能力有待加强。
4. **动态情感适应未解决**：模型在对话中预设固定的情感标签，无法根据用户情绪的实时变化调整语音风格，距离真正的情感交互仍有差距。

### 补充图表

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2409_18042/figures/002_Table_1.jpg]]
*Table 1: Comparison of Multi-modal Large Language Models. EMOVA is the very first Omni-modal LLM capable of emotional spoken dialogue with state-of-the-art vision-language and speech capabilities simultaneously. “Gen.” stands for Generation*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2409_18042/figures/007_Table.jpg]]

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2409_18042/figures/014_Table_4.jpg]]
*Table 4: Statistics of the EMOVA speech instruction tuning datasets*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2409_18042/figures/015_Table_5.jpg]]
*Table 5: Detailed configuration for different training stages of EMOVA. The table illustrates the vision configurations, dataset characteristics, and training hyperparameters*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2409_18042/figures/001_Figure_1.jpg]]
*Figure 1: EMOVA is the very first omni-modal LLM with stateof-the-art performance on both vision-language and speech benchmarks simultaneously. See detailed results in Table 2*



## 定位与知识库关联

### 1. 与基线方法的关系

EMOVA 处于全模态大语言模型（Omni-modal LLM）这一新兴技术路线上，但其设计选择与现有工作形成显著差异，主要体现在三个维度：

**模态处理范式的分野。** 现有全模态模型大致分为两条路径：一是依赖外部工具的松耦合方案，如 **VITA** 仅用连续语音编码器支持语音理解，语音生成仍需外部 TTS 工具，无法实现端到端实时交互；二是统一离散化方案，如 **AnyGPT** 将视觉也离散化为 token，但这导致视觉细节信息的不可逆损失。EMOVA 选择了一条折中路径：视觉侧保留连续编码器（QwenViT + MLP 投影）以保持细粒度视觉理解，语音侧采用离散 tokenizer/detokenizer 实现端到端语音生成，同时通过语义-声学解耦设计使离散语音单元更接近文本嵌入空间，促进了全模态对齐的自然性。

**语音表示的根本差异。** 在语音 token 的表示层面，EMOVA 的语义-声学解耦设计是其区别于 **Mini-Omni2** 等使用单纯离散单元方案的关键。传统方案将语音的内容和声学特征混为一体进行量化，导致语音 token 与文本 token 的语义距离较大，增加了 LLM 对齐的难度。EMOVA 利用 SPIRAL 架构将输入语音分解为语义嵌入和风格嵌入，仅对语义部分进行 FSQ 量化后送入 LLM，声学风格则作为旁路控制信号用于后续语音合成。这一设计使得语音 token 在嵌入空间中更接近文本 token，为以文本为中心的全模态对齐奠定了基础（消融实验中 Joint 显著优于 Joint-entangled 即验证了这一点）。

**训练策略的范式突破。** 在训练策略上，多数多模态模型采用顺序训练（如先做视觉-语言对齐，再追加语音模态），EMOVA 的消融实验（Figure 3）明确表明这种顺序方案会因灾难性遗忘导致性能下降——无论是 VL→Speech 还是 Speech→VL，在视觉语言和语音基准上均劣于联合训练（Joint）。EMOVA 的联合训练同时使用图像-文本和语音单元-文本数据进行对齐，不仅避免了遗忘，还观察到了跨模态的相互促进效应：Joint 在视觉语言指标和 ASR 指标上均超越单独的 VL 和 Speech 基线。这一发现为全模态对齐提供了新的训练范式依据。

### 2. 适用边界与局限

尽管 EMOVA 在 15 个视觉语言基准中的 11 个上超越 GPT-4o/4V 和 Gemini Pro 1.5，同时在 LibriSpeech WER 上达到 2.9（超越 Whisper Large 的 3.0），但其设计选择也划定了明确的适用边界：

**双工交互的缺失。** EMOVA 目前只能同时处理输入或输出，无法实现同时听和说的双工交流。这意味着模型在真实对话场景中无法实时感知用户的情感变化并动态调整回应策略，限制了其在情感陪伴、实时翻译等需要双向同步交互场景中的应用。

**文本中介的生成瓶颈。** 当前模型的语音生成流程依赖于文本作为中间表示：LLM 先自回归生成文本回复和风格标签，再基于文本生成语音单元，最后由 U2S detokenizer 合成语音。这种“文本→语音单元→波形”的链式生成路径虽然保证了语义质量，但制约了生成速度。论文明确指出尚未充分探索直接从语音单元生成语音单元（unit-to-unit generation）的能力，这是提升语音响应实时性的关键方向。

**视觉模态的单一编码器限制。** EMOVA 仅使用单一预训练视觉编码器 QwenViT，未探索多编码器融合或专家混合架构。在面对需要多尺度视觉理解（如同时分析宏观场景和微观文字）或低质量输入（模糊图像、遮挡场景）时，单一编码器的鲁棒性可能存在瓶颈。此外，模型目前仅支持视觉理解，未涉及可控视觉生成能力。

**情感控制的范围与泛化。** U2S detokenizer 的情感控制已证明在四种常见情绪（如 Figure 6 混淆矩阵所示，三种情绪识别率超过 80%）上有效，但该评估基于 Emotion2Vec 的分类器，尚未在真实用户感知实验中验证情感表达的自然度和多样性。对于更微妙的情感状态（如讽刺、犹豫、惊喜混合）或跨语言的情感表达差异，风格模块的泛化能力尚需进一步验证。

### 3. 开放问题

论文和当前技术格局揭示了以下待解决的关键问题：

**动态情感双工建模。** 如何将可调节的情感控制融入双工会话模型，使对话中情感状态能够实时演变？这需要模型同时具备：1）从用户语音中实时感知情感变化的能力；2）根据对话上下文动态调整自身情感表达的策略学习机制。当前 EMOVA 的风格标签是显式预测的离散标签，未来可能需要探索连续的情感表示空间和基于强化学习的情感策略优化。

**直接单元到单元生成。** 如何强化从语音单元直接生成语音单元的能力，以大幅提高语音生成效率？这涉及两个子问题：一是训练数据层面，需要构建大规模语音单元到语音单元的配对数据；二是模型架构层面，需要设计能够捕捉语音单元间时序依赖和声学连续性的专用解码器，同时保持语义一致性。

**视觉感知的深度增强。** 如何结合自监督视觉编码器或专家混合架构进一步提升视觉感知？当前视觉编码器主要依赖监督预训练，自监督方法（如 DINOv2、MAE）可能提供更丰富的视觉表征。此外，针对文档理解、医学影像、遥感等专业领域，可能需要引入领域特定的视觉专家模块。

**全模态鲁棒性。** 在嘈杂或低质量视觉/语音输入下，如何保证全模态模型的鲁棒性？现实场景中常出现背景噪声、多人重叠语音、低光照图像等情况，当前模型在这些条件下的性能退化程度尚缺乏系统评估。可能的解决方向包括：引入对抗训练增强模态编码器的鲁棒性、设计模态置信度估计机制以动态调整模态融合权重、以及构建覆盖退化条件的全模态测试基准。



## 原文 PDF

![[paperPDFs/CVPR_2025/EMOVA_Empowering_Language_Models_to_See_Hear_and_Speak_with_Vivid_Emotions.pdf]]
