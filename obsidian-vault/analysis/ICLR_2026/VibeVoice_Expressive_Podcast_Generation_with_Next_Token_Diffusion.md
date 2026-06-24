---
title: "VibeVoice: Expressive Podcast Generation with Next-Token Diffusion"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/VibeVoice_Expressive_Podcast_Generation_with_Next_Token_Diffusion.pdf
openreview_forum_id: FihSkzyxdv
aliases:
- VibeVoice
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "核心因果旋钮是采用超低帧率（7.5 Hz）的连续声学分词器（σ-VAE）与语义分词器解耦设计，形成混合语音表示作为LLM输入，并利用轻量扩散头预测连续声学隐变量：这一设计大幅压缩序列长度，保留丰富声学细节和语言内容，使LLM可高效处理长达90分钟的播客，同时保持高自然度和说话人一致性。"
primary_logic: "将语音信号压缩至极低帧率（7.5 Hz）并分离声学、语义路径，使长序列生成可行；同时，LLM擅于捕获文本上下文和对话流，而扩散头确保高保真声学重建，二者通过混合表示协同，在下一令牌预测框架中统一，从而实现具有自然交互节奏、丰富表现力（如呼吸、唇齿音）的多说话人播客合成。"
claims:
- "超低帧率连续声学分词器在保持高保真前提下实现7.5 Hz的极致压缩，UTMOS达4.181（LibriTTS test-clean），优于众多高帧率方案"
- "混合分词器（声学+语义）在保持说话人相似度的同时，显著改善多说话人对话的清晰度（WER从纯声学的6.22降至1.84）"
- "7B参数模型在主观维度全面超越所有基线，平均MOS达3.76，优于Gemini 2.5 Pro TTS的3.66，并在多说话人长场景中保持WER=1.24、SIM‑O=0.75"
- "扩散步数10和CFG 1.25在WER与SIM‑O之间取得最佳平衡，过度去噪会损害说话人相似度"
---

# VibeVoice: Expressive Podcast Generation with Next-Token Diffusion

> [!tip] 核心洞察
> 将语音信号压缩至极低帧率（7.5 Hz）并分离声学、语义路径，使长序列生成可行；同时，LLM擅于捕获文本上下文和对话流，而扩散头确保高保真声学重建，二者通过混合表示协同，在下一令牌预测框架中统一，从而实现具有自然交互节奏、丰富表现力（如呼吸、唇齿音）的多说话人播客合成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VibeVoice：基于下一令牌扩散的富有表现力的播客生成 |
| 英文题名 | VibeVoice: Expressive Podcast Generation with Next-Token Diffusion |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=FihSkzyxdv); [GitHub](https://github.com/microsoft/VibeVoice) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | VIBEVOICE |
| Dataset | 主观评估 (8个多话题对话，24名标注员), VIBEVOICE-Eval Short（0~12分钟，所有说话人数）, LibriTTS test-clean 音频重建 |

> [!tip] 效果简介
> - 主观评估 (8个多话题对话，24名标注员) 上，平均MOS (Realism/Richness/Preference) 为 VIBEVOICE-7B: 3.76，对比 Gemini 2.5 Pro preview TTS: 3.66，变化 +0.10。
> - VIBEVOICE-Eval Short（0~12分钟，所有说话人数） 上，WER-W 为 VIBEVOICE-1.5B (64K): 1.22，对比 Cosyvoice2-Concat: 4.27，变化 -3.05。
> - VIBEVOICE-Eval Short（0~12分钟，所有说话人数） 上，SIM-O 为 VIBEVOICE-7B (32K): 0.75，对比 MoonCast (成功案例): 0.55†，变化 +0.20。

## 概述

### 问题瓶颈

传统语音合成系统在生成多说话人长篇对话音频时面临根本性困难：单说话人短句合成范式难以自然扩展至具有高保真度和自然交互节奏的长篇播客。核心挑战在于三个方面——首先，现有系统缺乏对自然话轮转换、非词汇线索（如呼吸、唇齿音）和长时间说话人一致性的有效建模；其次，离散码本的高帧率表示（如Encodec 600 Hz、DAC 400 Hz）导致序列长度急剧膨胀，使长序列建模效率低下；第三，端到端方案在长上下文场景下的稳定性与可扩展性不足，例如MoonCast在处理超过10分钟或3人以上对话时频繁崩溃。

### 核心方法

VibeVoice采用**下一令牌扩散框架**，其核心设计包括三个关键创新：一是使用超低帧率（7.5 Hz）的连续声学分词器（σ-VAE），将24kHz音频压缩3200倍，在保留精细声学细节的同时大幅缩短序列长度；二是将声学分词器与语义分词器解耦，通过可学习投影层融合为混合语音表示，使LLM能够同时捕获文本内容和声学特征；三是以轻量扩散头（约123M参数）替代传统自回归解码器，在LLM隐藏状态条件下预测连续声学隐变量，实现下一令牌扩散生成。配合课程学习策略（上下文窗口从4k逐步扩展至65k tokens），VibeVoice可稳定合成最长达90分钟、包含4名说话人的播客。

### 主要结果

在主观评估中，VibeVoice-7B的平均MOS达3.76，超越Gemini 2.5 Pro TTS的3.66，并在真实感（3.71）、丰富度（3.81）和偏好度（3.75）三个维度均取得最优。在客观指标上，VibeVoice-1.5B在VIBEVOICE-Eval短时长子集上取得WER-W 1.22，显著优于Cosyvoice2-Concat的4.27；VibeVoice-7B的SIM-O达0.75，远超MoonCast成功案例的0.55。声学分词器在LibriTTS test-clean上取得UTMOS 4.181，优于WavTokenizer（75 Hz）的4.049。推理效率方面，1.5B模型在单张NVIDIA A6000上RTF为0.83，低于MoonCast的1.43，实现实时生成。

## 背景与动机

### 播客生成的规模化困境

播客作为一种长篇、多说话人、富含表现力的对话媒介，近年来成为语音合成领域的新兴挑战。传统文本到语音（TTS）系统在设计之初便以单说话人、短句合成为目标——它们擅长在数秒内生成高保真语音，却难以将这种能力自然扩展至数十分钟的多方对话。当这些系统被强行拼接以生成长播客时，一系列根本性问题随之暴露：话轮转换缺乏自然的节奏与重叠，非词汇线索（如呼吸、唇齿音、犹豫填充）被抹平或丢失，长时间跨度的说话人音色一致性难以维持。这些缺陷并非工程实现层面的疏忽，而是源于传统TTS架构对“对话流”这一时间维度上的结构性盲区。

### 现有端到端方案的瓶颈

近年来，基于语言模型的端到端语音生成方法试图突破上述限制。它们将语音离散化为令牌序列，交由自回归模型统一建模。然而，这一范式面临两个相互纠缠的瓶颈。

**第一，离散码本的高帧率困境。** 主流声学分词器——如Encodec（600 Hz）和DAC（400 Hz）——将每秒音频切分为数百个离散令牌。对于一段30分钟的播客，这意味着数十万乃至上百万个令牌的序列长度，远超当前大语言模型（LLM）高效处理的范围。即使采用RVQ等压缩技术，序列长度的膨胀仍然使长上下文建模在计算和内存层面难以负担。

**第二，声学细节与语义内容的表征冲突。** 离散码本通过矢量量化将连续声学信号压缩至有限码字集合，这一过程不可避免地丢失了精细的声学纹理——包括说话人音色、环境混响、以及前述的非词汇表达。与此同时，纯声学令牌对语义信息的编码能力有限，导致生成语音的文本清晰度在多说话人场景中急剧下降。现有公开模型如**MoonCast**（Ju et al., 2025）虽已尝试端到端播客生成，但仅支持最多2名说话人、时长不超过10分钟，且在3人以上场景中频繁崩溃，暴露出当前架构在稳定性与可扩展性上的深层不足。

### 核心动机：低帧率连续表示与混合表征的协同

VibeVoice的动机源于对上述瓶颈的因果性诊断：**序列长度膨胀的根源在于帧率过高，而声学保真度与语义清晰度的冲突源于单一表征路径的过度负载。** 由此衍生出两个核心设计目标：

1. **极致压缩帧率而不牺牲保真度**：能否将帧率从数百赫兹压缩至个位数赫兹，同时避免离散量化带来的信息损失？这要求声学分词器在连续隐空间中工作，以保留波形中的精细结构。

2. **解耦声学与语义路径**：能否让声学特征专注于高保真重建（包括非词汇线索和环境纹理），而让语义特征专注于文本内容的准确传递，二者通过可学习的融合机制协同工作，而非相互干扰？

这两个目标的实现，将使LLM能够在可管理的序列长度内（数万而非数十万令牌）建模长达90分钟的多人对话，同时保持说话人一致性和自然交互节奏。这正是VibeVoice通过**7.5 Hz连续σ-VAE声学分词器**与**声学-语义混合表示**所瞄准的核心突破点。

## 核心创新

VIBEVOICE 针对多说话人长篇播客生成的核心瓶颈——长序列建模效率低、自然话轮转换与声学细节（呼吸、唇齿音）难以保持——提出了三个相互协同的创新设计，构成其与现有方案的本质差异。

### 极致帧率压缩：连续声学分词器（σ‑VAE）

传统语音分词器依赖离散码本（如 Encodec 600 Hz、DAC 400 Hz），高帧率导致长序列建模的计算开销不可接受。VIBEVOICE 采用连续 σ‑VAE 作为声学分词器，将 24 kHz 输入波形压缩至 **7.5 Hz**（3200× 降采样），避免了离散量化带来的信息损失，同时保留了精细的声学细节。在 LibriTTS test-clean 上，该分词器的 UTMOS 达 4.181，PESQ 达 3.068，优于 WavTokenizer（75 Hz）等更高帧率方案。这一设计是支撑 90 分钟超长播客生成的前提——序列长度被压缩了约两个数量级，使 LLM 能够高效处理全局对话上下文。

### 声学‑语义解耦的混合表示

不同于单一编码器输出的共享表示或纯声学特征，VIBEVOICE 将声学分词器与语义分词器**完全解耦**：声学分词器通过 σ‑VAE 重建波形，语义分词器则通过 ASR 代理任务提取与文本对齐的内容特征，二者帧率同为 7.5 Hz。两条路径的输出经可学习投影矩阵 $W_a$、$W_s$ 融合为混合表示 $z_{p,i} = W_a z_{a,i} + W_s \ \mathrm{Semantic_{Enc}}(y_i)$，作为 LLM 的输入。消融实验表明，这一设计将多说话人场景的 WER 从纯声学模型的 6.22 大幅降至 1.84，同时保持说话人相似度 SIM‑O 为 0.64；而耦合分词器（共享编码器）的 SIM‑O 仅 0.45，验证了解耦的必要性。

### 下一令牌扩散生成：LLM + 轻量扩散头

VIBEVOICE 将长序列生成统一为**下一令牌扩散**框架：LLM（基于 Qwen2.5 1.5B/7B）接收混合表示序列，建模多说话人对话流与文本内容，其隐藏状态 $h_i$ 作为条件输入一个轻量扩散头（4 层，约 123M 参数）。扩散头通过迭代去噪预测连续的声学 VAE 隐变量 $z_{a,i}$，再由声学解码器恢复为波形片段。推理时采用 Classifier‑Free Guidance（CFG），在条件与无条件噪声预测之间线性插值以增强控制。消融显示，DDPM 步数 10、CFG 1.25 时 WER 最低（1.55），而过高步数会导致过度去噪，损害说话人环境纹理（如房间混响），使 SIM‑O 显著下降。这一架构使 LLM 擅长捕获文本上下文和对话流，扩散头确保高保真声学重建，二者通过混合表示协同，在下一令牌预测框架中统一。

### 课程学习驱动的长上下文扩展

为使模型适应超长播客，VIBEVOICE 采用课程学习策略，将 LLM 训练序列长度从 4,096 tokens 逐步提升至 65,536 tokens（分四个阶段，共 110k 训练步）。这使得 7B 模型在 12–30 分钟的长播客上仍保持 WER‑W 1.24、SIM‑O 0.75，且推理实时因子（RTF）在单 NVIDIA A6000 上为 0.97，接近实时生成。相比之下，端到端基线 MoonCast 在 3 人以上或长音频场景下频繁崩溃，其有效指标仅基于成功子集。

## 整体框架

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FihSkzyxdv/figures/009_Figure_4.jpg]]
*Figure 4: An illustration of the Coupled Tokenizer architecture. A single encoder produces a shared latent representation $\mu$ , which is utilized for both speech reconstruction (Acoustic Decoder) and ASR (Semantic Decoder). This design contrasts with our final Hybrid architecture (Figure 2), which employs separate encoders to decouple semantic and acoustic representations*

VIBEVOICE 是一个端到端的、基于大型语言模型（LLM）的播客生成系统，其核心设计目标是实现长达数十分钟、包含多名说话人的高表现力对话音频合成。系统整体遵循“下一令牌扩散”（next-token diffusion）范式，将语音生成建模为在给定对话历史和文本脚本条件下，逐步预测未来语音片段声学隐变量的过程。

### 核心架构与数据流

系统的输入由两部分组成：**语音提示（voice prompts）** 为每位说话人提供音色参考，**文本脚本（text scripts）** 定义对话内容与说话人切换。输入首先经过两条独立的分词路径处理：

1.  **声学分词器**（Acoustic Tokenizer）基于 σ‑VAE，将原始 24 kHz 波形压缩至极低帧率（7.5 Hz）的连续隐变量 $z_a$，保留精细的声学细节（如呼吸、唇齿音、环境纹理）。
2.  **语义分词器**（Semantic Tokenizer）以 ASR 为代理任务，提取与文本语义对齐的特征，帧率同样为 7.5 Hz。

两条路径的特征通过可学习的投影层 $W_a$ 和 $W_s$ 映射至 LLM 隐藏维度，并逐帧相加形成**混合表示** $z_{p,i}$（见公式 3）。这一混合表示序列作为 LLM 的输入条件，使 LLM 能够同时建模对话流、文本内容与声学特征。

LLM（基于 Qwen2.5，提供 1.5B 和 7B 两个版本）作为核心序列模型，接收混合表示序列后，在每个时间步输出隐藏状态 $h_i$。该隐藏状态作为条件，送入一个轻量级的**扩散头**（Diffusion Head，约 123M 参数，仅 4 层）。扩散头通过迭代去噪过程，从随机噪声中重建出下一段语音的声学隐变量 $z_{a,i+1}$。最后，预训练的声学解码器将 $z_{a,i+1}$ 还原为波形片段 $y_{i+1}$。

### 关键设计决策

- **极低帧率压缩**：声学分词器实现 3200 倍降采样（24 kHz → 7.5 Hz），将长序列建模的计算负担降低约两个数量级，使 LLM 能够处理长达 90 分钟的播客上下文。
- **声学-语义解耦**：声学与语义分词器独立训练、各司其职，避免单一编码器在保真度与语义对齐之间的权衡。消融实验表明，耦合分词器（共享编码器）会导致说话人相似度（SIM‑O）大幅下降至 0.45。
- **扩散头生成**：不同于自回归预测离散码本，扩散头在连续空间中预测声学隐变量，避免了矢量量化的信息损失，同时通过 Classifier‑Free Guidance（CFG）机制在推理时调节保真度与说话人相似度的平衡。
- **课程学习训练**：LLM 训练时，上下文窗口从 4,096 tokens 逐步扩展至 65,536 tokens（110k 步），使模型稳定适应超长播客的生成。

### 推理流程示意

推理时，系统逐段生成语音：每生成一个语音片段，其声学隐变量与对应文本的语义特征融合为新的混合表示 $z_{p,i+1}$，追加至 LLM 的上下文窗口，驱动下一段的生成。这一自回归式的扩展机制使 VIBEVOICE 能够合成具有自然话轮转换、丰富非词汇线索（如呼吸、唇齿音）和长时间说话人一致性的多说话人播客。

## 核心模块与公式推导

### 2.1 连续语音分词器：声学与语义解耦

VIBEVOICE 的核心设计之一是采用一对解耦的连续语音分词器，二者均工作在 **7.5 Hz** 的超低帧率（从 24kHz 输入实现 3200× 降采样），为后续 LLM 长序列建模奠定基础。

**声学分词器**采用 σ‑VAE 架构，在连续隐空间中编码语音信号，避免离散码本带来的信息压缩损失：

$$
\mu = \mathrm{Encoder}_\phi(\pmb{x}) \\
z = \mu + \sigma \odot \epsilon, \quad \epsilon \sim \mathcal{N}(0,1), \quad \sigma \sim \mathcal{N}(0, C_\sigma) \\
\hat{\pmb{x}} = \mathrm{Decoder}_\psi(z)
$$

其中固定方差 $C_\sigma$ 控制随机程度，$\epsilon$ 为标准高斯噪声，$z$ 为最终声学隐变量。该设计使分词器在保持高保真重建（LibriTTS test-clean: PESQ 3.068, UTMOS 4.181）的同时，将帧率压缩至极低水平。

**语义分词器**镜像声学编码器的层次结构，但移除了 VAE 组件，以 ASR 作为代理任务进行确定性内容特征提取。其目标是输出与文本语义对齐的语义特征，帧率同为 7.5 Hz。这一解耦设计使得声学细节（如音色、呼吸、环境纹理）与语言内容分别由专用编码器独立建模。

### 2.2 混合语音表示与下一令牌扩散生成

#### 2.2.1 混合表示构造

给定语音片段 $y_i$，VIBEVOICE 通过可学习投影矩阵将声学特征 $z_{a,i}$ 和语义特征融合为 LLM 输入的混合表示：

$$
z_{p,i} = W_a z_{a,i} + W_s \mathrm{Semantic}_{\mathrm{Enc}}(y_i)
$$

其中 $W_a \in \mathbb{R}^{d_{llm} \times d_a}$、$W_s \in \mathbb{R}^{d_{llm} \times d_s}$ 为可学习投影矩阵。混合表示 $z_{p,i}$ 同时携带声学身份信息和语义内容信息，使 LLM 能够在统一序列中建模多说话人对话流。

#### 2.2.2 序列生成范式

VIBEVOICE 采用下一令牌预测框架，基于当前上下文和历史混合表示预测下一段声学隐变量：

$$
z_{a,i+1} = \mathrm{VIBEVOICE}(X, z_{p,0}, \dots, z_{p,i})
$$

随后通过声学解码器将预测的隐变量转换为波形：

$$
\pmb{y}_{i+1} = \mathrm{Acoustic}_{\mathrm{Dec}}(z_{a,i+1})
$$

其中 $X$ 为文本脚本与语音提示等全局上下文。

#### 2.2.3 扩散头条件生成

LLM 输出的隐藏状态 $h_i$ 作为条件输入轻量扩散头（4 层，约 123M 参数），通过去噪过程生成声学隐变量。训练时，向干净的 $z_{a,i}$ 逐步注入高斯噪声：

$$
z_{a,i}(t) = \sqrt{\bar{\alpha}_t} z_{a,i} + \sqrt{1 - \bar{\alpha}_t} \epsilon
$$

扩散头 $\epsilon_\theta$ 以 $h_i$ 为条件预测注入的噪声，训练损失为：

$$
\mathcal{L}_{\mathrm{Diff}} = \mathbb{E}_{t, z_{a,i}, \epsilon, h_i} \| \epsilon - \epsilon_\theta(z_{a,i}(t), t, h_i) \|^2
$$

推理时采用 Classifier‑Free Guidance 增强条件控制：

$$
\hat{\epsilon} = \epsilon_\theta(z_{a,i}(t), t, h_{<\mathrm{S}>}) + w \cdot (\epsilon_\theta(z_{a,i}(t), t, h_i) - \epsilon_\theta(z_{a,i}(t), t, h_{<\mathrm{S}>}))
$$

其中 $w$ 为引导系数，$h_{<\mathrm{S}>}$ 为无条件（空提示）隐藏状态。消融实验表明，DDPM 步数为 10、CFG 为 1.25 时在 WER（1.55）与 SIM‑O 之间取得最优平衡；更高步数会导致过度去噪，损害说话人相似度（Figure 6 频谱分析证实：步数=50 时模型激进剥离非语音成分，造成频谱发散和环境纹理丢失）。

### 2.3 关键设计选择

- **连续隐空间 vs 离散码本**：离散码本（如 Encodec 600 Hz、DAC 400 Hz）的高帧率使长序列建模效率低下，且量化压缩会丢失精细声学细节（如呼吸、唇齿音）。VIBEVOICE 的连续 σ‑VAE 在 7.5 Hz 下保留这些非词汇线索，避免自然度损失。
- **解耦 vs 耦合分词器**：消融实验（Table 5）显示，耦合分词器（共享编码器）的 SIM‑O 仅 0.45，而解耦的混合分词器在保持 SIM‑O 0.64 的同时将多说话人 WER 从纯声学模型的 6.22 降至 1.84，验证了解耦设计的必要性。
- **课程学习策略**：LLM 训练序列长度从 4,096 tokens 逐步扩展至 65,536 tokens（前 40k 步 4K，40k–80k 步 16K，80k–100k 步 32K，100k–110k 步 65K），使模型能够稳定合成最长达 90 分钟、4 说话人的播客。

## 实验与分析

### 核心瓶颈与因果机制

多说话人播客生成的核心瓶颈在于：传统TTS系统面向单说话人、短句合成设计，无法自然扩展至高保真、自然交互的长篇对话。具体表现为：(1) 缺乏对自然话轮转换和非词汇线索（呼吸、唇齿音）的有效建模；(2) 离散码本的高帧率表示使长序列建模效率低下，现有端到端方案在长上下文场景下稳定性不足。VibeVoice通过一个关键的因果旋钮突破这一瓶颈：**超低帧率（7.5 Hz）的连续声学分词器与语义分词器解耦设计**。该设计将语音信号压缩至极低帧率，同时分离声学与语义路径，使LLM可高效处理长达90分钟的播客，而轻量扩散头确保高保真声学重建——二者通过混合表示协同，在下一令牌预测框架中统一。

### 主观评估：整体质量与表现力

Table 1展示了主要主观评估结果。VIBEVOICE-7B在所有主观维度上全面超越基线模型，平均MOS达**3.76 ± 0.93**，优于Gemini 2.5 Pro preview TTS的3.66。分项来看，VIBEVOICE-7B在Realism（3.71）、Richness（3.81）和Preference（3.75）三个维度均取得最高分，表明其生成的播客在自然度、表现力丰富性和听感偏好上具有显著优势。值得注意的是，VIBEVOICE-1.5B的平均MOS为3.54，虽低于7B版本，但仍与商业闭源模型Elevenlabs v3 alpha（3.54）持平，且优于开源基线SesameAILabs-CSM（3.11）和Higgs Audio V2（3.20）。这一结果表明，即使在较小参数规模下，低帧率混合表示与扩散头架构的组合已能提供有竞争力的合成质量。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FihSkzyxdv/figures/003_Table_1.jpg]]
*Table 1: Human subjective and objective evaluation results. WER-W means using Whisper while WER-N means using Nemo. For all subjective metrics and SIM-O, higher scores are better. For WER, lower scores are better. Best results are in bold. The first phase subjective evaluation of Cosyvoice2, Mooncast and VIBEVOICE-1.5B can be found in Appendix I*

客观指标方面，VIBEVOICE-7B取得WER-W 1.29、WER-N 1.95和SIM-O 0.692，在清晰度和说话人相似度之间取得了良好平衡。需要指出的是，主观评估中每位标注员需听取约6小时音频（相当于2160个10秒短句），可能引入疲劳偏倚；但所有模型使用相同样本和标注标准，相对排序的可信度较高。

### 长播客客观评估：可扩展性验证

Table 2在VIBEVOICE-Eval数据集上按说话人数和时长分层评估，揭示了各模型在真实播客场景下的可扩展性差异。在短时长子集（0–12分钟）上，VIBEVOICE-7B (32K)取得总体WER-W **0.66**、SIM-O **0.75**的优异表现；相比之下，Cosyvoice2-Concat（拼接短片段方式）的WER-W高达4.27，SIM-O仅0.40，说明简单拼接无法维持长对话的一致性和清晰度。MoonCast在2说话人场景下SIM-O可达0.55（仅成功案例），但在3人以上或长音频场景下频繁崩溃，其指标仅基于成功子集（Table 2中以‡标注），因此对比可能对MoonCast不利。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FihSkzyxdv/figures/004_Table_2.jpg]]
*Table 2: Results of VIBEVOICE and baseline models on the VIBEVOICE-Eval dataset for multispeaker podcast generation. Results are presented for short (0∼12 min) and long (12∼30 min) duration subsets, across varying speaker counts. Seq. Leng. denotes the LLM training sequence length. “∗” denotes using a subset (12–13 min), and “‡” denotes using the successful cases only (with 3 retries) due to MoonCast crashes on long and multi-speaker(≥ 3) generation*

在长时长子集（12–30分钟）上，VIBEVOICE-7B (32K)维持WER-W **1.24**、SIM-O **0.75**，性能衰减远小于其他模型。这一稳定性直接归因于课程学习策略：训练时将LLM上下文窗口从4,096逐步扩展至65,536 tokens（超过110k训练步），使模型能适应超长序列。相比之下，MoonCast在超过10分钟的样本上几乎无法完成生成，Cosyvoice2-Concat的WER-W随长度增加急剧恶化至5.71。这验证了端到端长上下文建模对于多说话人长播客的必要性。

### 分词器重建质量：极致压缩与保真度平衡

Table 3展示了声学分词器在LibriTTS数据集上的重建质量。VIBEVOICE的连续σ-VAE分词器以**7.5 Hz**的极低帧率运行，在test-clean子集上取得PESQ **3.068**、UTMOS **4.181**的领先成绩，优于WavTokenizer（75 Hz, UTMOS 4.049）和DAC（400 Hz, UTMOS 3.867）等高帧率方案。在test-other子集上同样保持优势（PESQ 2.848, UTMOS 3.724）。这表明连续隐空间避免了离散码本的信息损失，使极低帧率下仍能保留丰富声学细节。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FihSkzyxdv/figures/007_Figure_3.jpg]]
*Figure 3: Ablation of CFG and DDPM steps on WER and SIM-O. Heatmaps show the effect of DDPM steps (x-axis) and classifier-free guidance (CFG) scale (y-axis) on SIM-O and WER scores. Table 3: Objective evaluation of reconstruction quality on the LibriTTS test-clean and test-other datasets. N _ { q } denotes the number of quantizers; VIBEVOICE uses a single continuous σ-VAE. Token Rate indicates the number of tokens/frames generated per second of audio. Higher PESQ, STOI, and UTMOS scores indicate better performance. Best results are in bold*

然而，该分词器的STOI指标相对较低（test-clean 0.828, test-other 0.823），主要因为训练播客数据未经过深度噪声抑制。这意味着在极端嘈杂环境下，语音可懂度可能受到一定影响——这是该设计的一个已知折衷。

### 消融实验：混合表示与架构选择

**分词器架构消融**（Table 5）揭示了解耦设计的关键作用。纯声学分词器模型的WER高达6.22，说明缺乏语义引导时LLM难以在多说话人场景中维持内容准确性。耦合分词器（共享编码器，Figure 4）的SIM-O仅0.45，验证了单一编码器无法同时服务声学重建和语义理解两个目标。混合分词器（声学+语义解耦）将WER大幅降至**1.84**，同时保持SIM-O **0.64**，实现了清晰度与说话人相似度的最佳平衡。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FihSkzyxdv/figures/010_Table_5.jpg]]
*Table 5: Ablation study on tokenizer architectures for podcast generation (no more than 12 minutes). The final Hybrid approach is evaluated against Acoustic-only and Coupled baselines. The results show that our Hybrid approach achieves the best overall balance of WER and higher SIM-O, especially in multi-speaker scenarios*

**模型规模扩展**（Table 2 Overall指标）：从1.5B扩展至7B，WER-W由2.11降至0.66，SIM-O由0.59升至0.75，主观MOS由3.54升至3.76。这显示更大LLM能更好地捕获对话流和说话人特征，且扩散头的条件生成质量随LLM隐藏状态质量提升而改善。

**扩散步数与CFG消融**（Figure 3热力图）：DDPM步数10、CFG=1.25时WER最低（1.55）；更高步数（如50步）导致SIM-O显著下降。Figure 6的频谱分析揭示了原因：高步数下模型过度"清洁化"音频，剥离了环境纹理（房间混响、背景噪声），这些非语音成分恰恰是说话人相似度感知的重要线索。步数10在保真度与自然度之间取得最佳平衡。

**数据管道设计选择**：移除语音增强组件保留了呼吸、唇齿音等非词汇表达，避免自然度损失——这一设计决策虽可能影响STOI等可懂度指标，但对播客场景的表现力至关重要。

### 推理效率

Table 8展示了推理实时因子（RTF）对比。VIBEVOICE-1.5B使用10步扩散时RTF为**0.83**（单NVIDIA A6000），低于实时阈值1.0，优于MoonCast的1.43。7B模型10步扩散RTF为0.97，仍在实时范围内。推理耗时主要由LLM自回归生成（1.5B: 37.1ms/段; 7B: 43.4ms/段）和扩散头迭代去噪（10步: 2.9ms/段）构成，其中扩散头仅约123M参数，计算开销远低于LLM部分。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FihSkzyxdv/figures/013_Table_8.jpg]]
*Table 8: presents a breakdown of the inference cost in milliseconds (ms) per generated segment for different VIBEVOICE model sizes (1.5B and 7B LLM parameters) and varying numbers of DDPM diffusion steps (1 and 10) for the diffusion head. The measurements include the time taken by the Large Language Model (LLM), the Diffusion Head, the Acoustic Decoder, and the Semantic Encoder, along with Real-Time Factor (RTF). Table 8: Inference cost (ms) and Real-Time Factor (RTF) comparison between VIBEVOICE and baseline models. Measurements were conducted on a single NVIDIA A6000 GPU with a batch size of 1*

### 已知局限与开放问题

1. **可懂度-自然度权衡**：声学分词器STOI偏低，在嘈杂环境下可懂度可能不足。改进方向包括引入感知损失或优化训练数据降噪策略。
2. **说话人相似度度量**：SIM-O在高保真区间对人类感知的敏感性不足，需要更精细的评估指标捕捉音色、韵律和风格一致性。
3. **场景泛化**：模型主要在播客数据上训练，对多人会议、多角色有声书等场景的泛化能力尚未验证。
4. **说话人数量限制**：当前最多支持4名说话人且需独立语音提示，零样本扩展至更多说话人仍需研究。
5. **超长播客连贯性**：超过30分钟的极长播客中，LLM如何维持主题连贯性、避免事实冲突和保持一致情感脉络是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FihSkzyxdv/figures/008_Table_4.jpg]]
*Table 4: List of models and tools used in our data processing pipeline*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FihSkzyxdv/figures/011_Table_6.jpg]]
*Table 6: presents the results on the SEED test sets. Although our model is primarily trained on long-form speech, it demonstrates strong generalization on short-utterance benchmarks. In addition, by employing a lower frame rate, our model substantially reduces the number of decoding steps required to synthesize one second of speech. Table 6: Results on the SEED test sets*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FihSkzyxdv/figures/012_Table_7.jpg]]
*Table 7: Reconstruction results on LibriSpeech test-clean set. N _ { q } denotes the number of quantizers; VIBEVOICE uses a single continuous σ-VAE. Higher PESQ, STOI, and UTMOS scores indicate better performance*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FihSkzyxdv/figures/014_Table_9.jpg]]
*Table 9: Summary of training hyperparameters for Tokenizer and VIBEVOICE model stages*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FihSkzyxdv/figures/015_Table_10.jpg]]
*Table 10: Distribution of the VIBEVOICE-Eval dataset, stratified by the number of speakers per sample. Durations are provided in seconds (average) and hours (total)*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FihSkzyxdv/figures/019_Table_11.jpg]]
*Table 11: Subjective and objective evaluation on podcast generation. For all subjective metrics and SIM-O, higher scores indicate better performance. For WER, lower scores are better*

## 方法谱系与知识库定位

### 1. 核心设计选择与基线对比

VibeVoice 的方法论定位源于对传统 TTS 系统在长时多说话人场景下根本性瓶颈的突破。其核心因果旋钮——**超低帧率（7.5 Hz）连续声学分词器与语义分词器的解耦设计**——直接回应了离散码本高帧率表示（如 Encodec 600 Hz、DAC 400 Hz）导致的长序列建模效率低下问题。这一设计将 24kHz 输入音频压缩至 3200× 降采样率，使得 LLM 可处理的序列长度大幅缩短，为长达 90 分钟的多说话人播客生成提供了计算可行性。

在生成架构层面，VibeVoice 采用 **LLM + 轻量扩散头** 的端到端设计，区别于纯自回归预测离散令牌的范式。扩散头（约 123M 参数，4 层）以 LLM 隐藏状态 $h_i$ 为条件，预测连续声学 VAE 隐变量 $z_{a,i}$，在下一令牌预测框架中统一了文本上下文建模与高保真声学重建。这一设计借鉴了 **LatentLM**（Sun et al., 2024）的连续隐变量生成思路，但将其扩展至语音域，并通过混合表示机制实现声学与语义的协同。

与现有播客生成基线的关键差异体现在以下维度：

| 设计维度 | 基线方法 | VibeVoice 创新 |
|---------|---------|---------------|
| 分词器帧率 | 数百 Hz（Encodec 600 Hz, DAC 400 Hz） | **7.5 Hz**（连续 σ-VAE，3200× 降采样） |
| 声学表示类型 | 离散码本（RVQ） | **连续 σ-VAE 隐变量**（避免码本压缩，保留精细声学细节） |
| 声学/语义耦合 | 单一编码器共享表示或纯声学特征 | **分离的声学与语义分词器**，通过投影层融合为混合表示 $z_{p,i} = W_a z_{a,i} + W_s \text{Semantic\_Enc}(y_i)$ |
| 生成架构 | 自回归预测离散令牌或独立并行生成 | **LLM + 轻量扩散头**，下一令牌扩散生成 |
| 训练序列长度 | 短序列（如 **MoonCast**（Ju et al., 2025）约 40K tokens） | **课程学习逐步提升至 65,536 tokens**，适应超长播客 |

### 2. 与具体基线工作的关系

**Cosyvoice2**（Du et al., 2024）：作为单说话人 TTS 基线，Cosyvoice2 通过拼接短片段生成长播客，但缺乏对自然话轮转换和长时间说话人一致性的建模。VibeVoice 的端到端生成在 VIBEVOICE-Eval Short 子集上将 WER-W 从 4.27 降至 1.22（1.5B 模型），验证了统一建模对话流的优势。

**MoonCast**（Ju et al., 2025）：作为公开的多说话人播客生成模型，MoonCast 最多支持 2 说话人、10 分钟，且在 3 人以上场景频繁崩溃。VibeVoice 通过超低帧率分词器和课程学习策略，将支持范围扩展至 4 说话人、最长 90 分钟，并在成功案例对比中保持 SIM-O 优势（0.75 vs 0.55）。

**SesameAILabs-CSM**（2025）、**Higgs Audio V2**（Boson AI, 2025）、**Elevenlabs v3 alpha**、**Gemini 2.5 Pro preview TTS**：这些开源或商业闭源多说话人模型在主观评估中作为对比基线。VibeVoice-7B 以平均 MOS 3.76 超越 Gemini 的 3.66，在真实感（3.71）、丰富度（3.81）和偏好度（3.75）三个维度均取得最优。

### 3. 适用边界与泛化能力

VibeVoice 的设计在以下场景展现出明确优势：
- **长时多说话人播客**（0–90 分钟，2–4 说话人）：通过课程学习策略（4,096 → 65,536 tokens，110k 步）使 LLM 逐步适应超长上下文，长场景（12–30 分钟）下仍维持 WER-W 1.24、SIM-O 0.75。
- **零样本 TTS**：在 SEED 标准测试集上表现出强泛化能力，尽管模型主要在长形式播客数据上训练，低帧率设计大幅减少了序列长度，使其在短句基准上仍具竞争力。
- **非词汇表达保留**：数据管道中刻意移除语音增强组件，保留了呼吸、唇齿音等情感表达线索，避免了传统降噪导致自然度损失的问题。

然而，以下边界条件需要关注：
- **说话人数量限制**：当前仅支持最多 4 名说话人，且需为每位说话人提供独立语音提示，零样本地扩展至更多说话人或未知提示仍需验证。
- **场景泛化未验证**：模型主要在播客类型数据上训练，对多人会议、多角色有声书等其他多说话人场景的泛化性能尚未评估。
- **语言迁移能力未知**：从播客数据中学习到的自然对话模式能否迁移至其他语言（尤其是低资源语言）仍是开放问题。

### 4. 关键局限与失败模式

**声学分词器的 STOI 瓶颈**：尽管在 PESQ（test-clean: 3.068）和 UTMOS（4.181）上取得领先，但 STOI 相对较低（test-clean: 0.828），主要因为训练播客数据未经过深度噪声抑制。这可能影响极端嘈杂环境下的语音清晰度，需通过改进数据降噪策略或引入感知损失来解决。

**扩散步数对说话人相似度的敏感性**：消融实验揭示了一个关键权衡——DDPM 步数 10、CFG 1.25 时 WER 最优（1.55），但更高步数（如 50）会导致模型过度"清洁化"，剥离环境纹理（房间混响、背景噪声），显著损害说话人相似度（SIM-O 下降）。频谱分析（Figure 6）证实了这一现象：高步数下生成的信号虽更干净，但频谱发散，丧失了维持高 SIM-O 所需的声学"氛围"。

**说话人相似度度量的不敏感性**：SIM-O 在超过一定阈值后对人类感知的一致性不再敏感，因此在评估高保真说话人保留时存在偏差。需要更精细的指标捕捉音色、韵律和风格一致性。

**推理实时因子的优化空间**：7B 模型 10 步扩散的 RTF 为 0.97，虽在实时范围内，但若需支持更高质量或更高并发，仍需进一步优化。1.5B 模型 RTF 为 0.83，已实现实时推理。

**自动标注流水线的错误传播**：VIBEVOICE-Eval 数据集的构建依赖 Whisper 和 WeSpeaker 等工具进行 WER 和 SIM-O 评估，这些工具的固有错误会传播至训练数据和评估指标，可能影响结论的可靠性。

### 5. 开放问题与未来方向

1. **分词器保真度与帧率的进一步平衡**：如何提升 STOI 同时维持 7.5 Hz 极低帧率？可能的路径包括改进训练数据降噪策略、引入多尺度判别器或感知损失函数。

2. **超长播客的主题连贯性**：在超过 30 分钟的极长播客中，LLM 如何维持主题连贯性、避免事实冲突（如前后矛盾），以及保持一致的情感脉络？这可能需要引入显式记忆机制或层次化规划模块。

3. **动态说话人管理**：能否在对话中间动态插入新说话人，或允许改变语音风格，而无需重新提供全量提示？这对交互式应用至关重要。

4. **声学与语义融合的自适应调节**：混合表示中 $W_a$ 与 $W_s$ 的融合比例是否可以自适应调节（例如根据文本情感或说话速度），从而在保真度与鲁棒性之间动态平衡？

5. **更精细的说话人相似度评估**：需要开发能够捕捉人类感知到的音色、韵律和风格一致性的评估指标，而非仅依赖嵌入余弦相似度。

6. **跨语言与跨领域迁移**：VibeVoice 从播客数据中学习到的自然对话模式能否迁移至其他语言（尤其是低资源语言）和其他多说话人场景（如会议、有声书）？这需要在多样化数据上进行系统验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/VibeVoice_Expressive_Podcast_Generation_with_Next_Token_Diffusion.pdf]]
