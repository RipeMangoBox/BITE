---
title: "UALM: Unified Audio Language Model for Understanding, Generation and Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/UALM_Unified_Audio_Language_Model_for_Understanding_Generation_and_Reasoning.pdf
project_link: https://research.nvidia.com/labs/adlr/UALM
code_link: https://github.com/NVIDIA/audio-intelligence/tree/main/UALM
openreview_forum_id: TsdlOjcQNu
aliases:
- UUALM
- UALM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "通过大规模数据、分类器自由引导(CFG)、直接偏好优化(DPO)和基于丰富字幕的多模态链式思维后训练，使单一自回归语言模型在音频生成上匹敌扩散模型，并在统一框架中实现生成式推理。"
primary_logic: "自回归语言模型在音频生成上的瓶颈可以通过数据规模扩展、CFG引导和DPO对齐来突破；将丰富字幕作为中间蓝图并进行多轮理解-生成-反思的链式思维，可以在同一模型中实现跨模态的生成推理能力。"
claims:
- "UALM-Gen 在音频生成上超越先前基于语言模型的方法，并达到与前沿扩散模型竞争的水平。"
- "统一模型 UALM 在音频理解任务上匹配当前最佳开源模型 (MMAUS Mean 74.1, MMAR Mean 55.2)。"
- "UALM 在文本推理能力上仅出现轻微下降 (MMLU 71.6, GSM8K 92.1, HumanEval 81.1)，优于先前视觉和语音统一模型。"
- "UALM-Reason 在生成式推理的主观评估中显著提升，如 Enrichment 从 3.77 升至 4.01，Self-reflection 从 3.82 升至 4.04。"
---

# UALM: Unified Audio Language Model for Understanding, Generation and Reasoning

> [!tip] 核心洞察
> 自回归语言模型在音频生成上的瓶颈可以通过数据规模扩展、CFG引导和DPO对齐来突破；将丰富字幕作为中间蓝图并进行多轮理解-生成-反思的链式思维，可以在同一模型中实现跨模态的生成推理能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | UALM：面向理解、生成和推理的统一音频语言模型 |
| 英文题名 | UALM: Unified Audio Language Model for Understanding, Generation and Reasoning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=TsdlOjcQNu) · [GitHub](https://github.com/NVIDIA/audio-intelligence/tree/main/UALM) · [Project](https://research.nvidia.com/labs/adlr/UALM) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | UALM (Unified Audio Language Model) |
| Dataset | AudioCaps, SongDescriber, MMAU-v0.5.15.25 |

> [!tip] 效果简介
> - AudioCaps 上，FD↓ 为 65.87 (UALM)，对比 80.13 (ETTA)，变化 -14.26 (绝对值改善)。
> - SongDescriber 上，OVL↑ 为 4.07 (UALM-Gen)，对比 3.91 (MusicGen-stereo-L)，变化 +0.16。
> - AudioCaps 上，CL↑ 为 0.65 (UALM-Gen)，对比 0.54 (ETTA)，变化 +0.11。

## 概要

现有音频语言模型面临一个根本性瓶颈：理解与生成任务通常由独立模型分别处理，且自回归语言模型在音频生成质量上长期落后于扩散模型。更重要的是，这些模型普遍缺乏在生成任务上的多模态推理能力，无法像人类一样实现理解、生成与推理的统一。

UALM（Unified Audio Language Model）通过三条关键路径突破上述瓶颈：**数据规模扩展**——将音频生成训练数据量提升至30M样本（约80k小时），远超扩散模型通常使用的规模；**生成范式革新**——在单一解码器LLM中引入分类器自由引导（CFG）和直接偏好优化（DPO），使自回归模型在音频生成上匹敌甚至超越扩散基线；**多模态链式思维后训练**——以丰富字幕作为中间蓝图，构建“丰富-对话-自我反省”的推理流程，首次在同一模型中实现生成式推理能力。

在方法定位上，UALM以Qwen2.5-7B为文本主干，通过声学编码器-适配器架构处理连续音频输入，利用X-codec离散码本和延迟模式生成音频输出。训练流程分为模态对齐、统一预训练和推理后训练三个阶段，其中模态对齐阶段冻结变换器主体，仅更新适配器和嵌入层，是实现理解与生成统一的关键。

主要结果方面：UALM-Gen在AudioCaps上的FD达到65.87，显著优于基于语言模型的MusicGen-stereo-L和扩散模型ETTA；统一模型UALM在音频理解基准MMAU上取得74.1的平均分，匹配当前最佳开源模型；文本推理能力仅出现轻微下降（MMLU 71.6，GSM8K 92.1，HumanEval 81.1），优于先前视觉和语音统一模型；UALM-Reason在生成式推理的主观评估中，Enrichment得分从3.77提升至4.01，Self-reflection从3.82提升至4.04。消融研究进一步证实CFG对提示遵循度的关键作用、DPO对感知质量的改善，以及增强VAE对FAD的大幅降低（SongDescriber上从224.72降至74.43）。

值得注意的局限性包括：评估主要覆盖英文音频场景，推理能力缺乏大规模客观基准，7B模型规模和30M训练数据带来的部署成本较高。

### 音频智能的碎片化现状

音频内容理解、声音生成和多模态推理是人类处理复杂听觉任务的三个核心能力。例如，创作一首符合特定情感主题的音乐，不仅需要理解音乐元素，还需要生成高质量的音频，并在过程中进行反思和调整。然而，当前的人工智能系统在这三个维度上呈现明显的碎片化。

在音频**理解**方面，现有模型已能较好地完成音频字幕生成、音频问答等任务，代表性工作包括 **Audio Flamingo 3**（Goel et al., 2025）等专家模型，以及 **Qwen2.5-Omni**（Xu et al., 2025）等统一多模态模型。在音频**生成**方面，扩散模型长期占据主导地位，如 **TangoFlux**（Hung et al., 2024）和 **Stable Audio Open**（Evans et al., 2024），基于语言模型（LM）的生成方法如 **MusicGen**（Copet et al., 2024）和 **AudioGen**（Kreuk et al., 2022）虽然具备序列建模的优势，但在生成质量上始终落后于扩散模型。

### 核心瓶颈：自回归生成的质量与推理缺失

这一碎片化格局背后存在两个深层瓶颈。

**瓶颈一：自回归语言模型在音频生成上的质量差距。** 扩散模型通过迭代去噪实现高保真生成，而基于解码器仅架构的语言模型在直接预测离散音频码时，面临提示遵循度弱、感知质量不足的问题。尽管语言模型在多模态统一方面具有天然优势——它们可以无缝处理文本和音频的交错序列——但生成质量的落后使其难以成为统一的解决方案。

**瓶颈二：生成任务上的多模态推理能力缺失。** 现有音频模型要么专注于理解，要么专注于生成，缺乏在生成过程中进行“理解-生成-反思”循环的能力。人类在创作音频时会不断评估自己的输出并修正，但现有系统无法在单一模型中实现这种生成式推理。

### 本文动机：走向理解-生成-推理的统一

UALM 的核心动机是打破上述壁垒，证明一个单一的自回归语言模型可以同时胜任音频理解、音频生成和多模态推理三大任务。这需要回答三个关键问题：

1. **生成质量能否追平扩散模型？** 通过大规模数据扩展、分类器自由引导（CFG）和直接偏好优化（DPO），能否让自回归语言模型在音频生成上达到与前沿扩散模型竞争的水平？
2. **统一是否损害单项能力？** 当理解、生成和文本能力被整合进同一模型时，是否会牺牲各任务的性能？
3. **如何实现生成式推理？** 能否利用丰富字幕作为中间蓝图，构建多轮“理解-生成-反思”的链式思维，使模型具备跨模态的生成推理能力？

UALM 的设计正是围绕这三个问题展开，其架构以 Qwen2.5-7B 作为主干，通过声学编码器、MLP 适配器和音频码本实现音频与文本的统一序列建模，并在后训练阶段引入推理能力。

## 核心方法与创新机理

UALM 的核心创新在于通过三个关键机制，首次在单一自回归语言模型中实现了音频理解、生成与推理的统一，并打破了此前“语言模型在音频生成上落后于扩散模型”的瓶颈。

**1. 纯解码器语言模型的音频生成范式革新**

UALM 摒弃了传统音频语言模型对外部文本编码器（如 T5）的依赖，直接利用预训练文本 LLM 的内置 BPE 分词器处理文本提示，使文本和音频令牌在统一的解码器主干中完成端到端建模（§2.2）。这一范式转变的关键推力来自三个技术杠杆：

- **数据规模扩展**：将训练数据量提升至 30M 样本（约 80k 小时），远超扩散模型的常规数据规模（通常 <2M 样本）。消融实验（Fig.5.b）证实，当数据量降至原有的 1/32 时，模型严重过拟合且性能大幅下降，表明数据规模是语言模型在音频生成上成功的必要条件。
- **分类器自由引导（CFG）**：将扩散模型中广泛使用的 CFG 技术引入自回归音频生成，在推理时通过条件与无条件分布的插值增强指令遵循：

$$\pi_{\theta}^{\mathrm{CFG}}(y_t|y_{1:t-1},x) = \lambda \cdot \pi_{\theta}(y_t|y_{1:t-1},x) + (1-\lambda) \cdot \pi_{\theta}(y_t|y_{1:t-1},\emptyset)$$

消融实验（Table 8）表明，移除 CFG 导致提示遵循度（CL）严重下降（SongDescriber CL: 0.45 → 0.39），且整体质量退化，验证了 CFG 对生成质量的关键作用。实验确定最优引导权重为 λ = 3.0（Fig.5.a）。

- **直接偏好优化（DPO）**：将偏好对齐引入语言模型驱动的音频生成框架，利用偏好样本对优化模型：

$$\mathcal{L}_{\mathrm{DPO}}(\pi_{\theta}) = -\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\left[\log\sigma\left(\beta\log\frac{\pi_{\theta}(y_w|x)}{\pi_{\mathrm{ref}}(y_w|x)} - \beta\log\frac{\pi_{\theta}(y_l|x)}{\pi_{\mathrm{ref}}(y_l|x)}\right)\right]$$

DPO 训练使 SongDescriber 上的 CL 从 0.45 提升至 0.51，AES 从 6.70 提升至 7.36（Table 8）。值得注意的是，DPO 训练前需先在合成音频上对基模型进行约 1k 步的适应性微调，否则损失函数会在训练初期出现尖峰（Fig.5.c）。

**2. 模态对齐阶段的渐进式训练策略**

UALM 在统一预训练前引入了专用的模态对齐阶段（§2.3），这是实现多任务统一的关键设计。该阶段冻结 Transformer 主体和声学编码器，仅更新 MLP 适配器和音频嵌入表，使模型在保持文本能力的同时建立跨模态连接。这一策略避免了直接全参数微调可能导致的灾难性遗忘，为后续的理解与生成能力协同发展奠定了基础。

**3. 基于丰富字幕的多模态链式思维推理**

UALM-Reason（§2.4）引入了一种新颖的多模态链式思维（CoT）范式，将丰富字幕作为中间“蓝图”，使模型能够执行“理解-生成-反思”的迭代推理循环。具体而言，模型首先对输入进行语义丰富（Enrichment），生成包含细节描述的中间字幕；然后基于该蓝图生成音频；最后对生成结果进行自我反思（Self-reflection）和迭代优化。这一机制使 UALM 在推理导向生成的主观评估中显著提升：Enrichment 从 3.77 升至 4.01，Self-reflection 从 3.82 升至 4.04（Table 4）。

**4. 增强 VAE 的感知质量提升**

UALM 引入增强 VAE 模块（§2.1, Appendix B.2），将 16kHz 单声道波形提升至 48kHz 立体声，其训练目标融合了立体声多分辨率 STFT 损失、对数梅尔损失、对抗损失、特征匹配损失和 KL 散度：

$$\mathcal{L}_{\mathrm{VAE}} = \mathcal{L}_{\mathrm{stereoMRSTFT}} + \mathcal{L}_{\mathrm{logmel}} + \mathcal{L}_{\mathrm{adv}} + \mathcal{L}_{\mathrm{feat}} + \zeta \cdot \mathcal{L}_{\mathrm{KL}}$$

消融实验（Table 8）表明，增强 VAE 使 SongDescriber 上的 FD 从 224.72 大幅降至 74.43，是感知质量提升的关键模块。

**创新总结**：UALM 的核心突破在于证明了自回归语言模型在音频生成上的瓶颈并非架构固有缺陷，而是数据规模、推理时引导策略和偏好对齐不足所致。通过 CFG + DPO + 数据缩放的三位一体策略，以及模态对齐和 CoT 推理的训练范式创新，UALM 首次在单一模型中实现了与扩散模型竞争甚至超越的音频生成质量，同时保持了强理解能力和文本推理能力。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_TsdlOjcQNu/figures/002_Figure_2.jpg]]
*Figure 2: UALM architecture overview and the multimodal pre-training data blending ratios*

UALM 以预训练纯文本解码器大语言模型 Qwen2.5-7B 为骨干，通过增加音频输入与输出模块，实现单一语言模型对理解、生成与推理三类任务的统一处理。整体架构遵循“编码器-适配器-LLM”范式，采用连续特征表示处理音频输入，同时以离散码本令牌实现音频输出，从而避免因离散化导致的信息损失，并保证生成效率。

**输入流**：原始音频波形首先送入声学编码器，提取为帧级连续特征表示。这些特征经 MLP 适配器投影至 LLM 的嵌入空间，形成与文本 BPE 令牌兼容的嵌入序列。文本提示则直接通过 LLM 内置的 BPE 分词器转换为令牌嵌入。两者在嵌入层被拼接为交错序列，送入 Transformer 解码器进行统一建模。

**输出流**：当模型需要生成音频时，LLM 在对应位置预测离散音频码本令牌。系统采用 X-codec 作为声学码本，以 50 Hz 帧率运行，并引入延迟模式进行帧内自回归预测——同一时间步并行预测多个残差矢量量化层的令牌，从而平衡生成质量与推理效率。生成的离散令牌序列最终通过声学码本解码器重建为波形。为提升感知质量，系统在解码器后级联一个增强 VAE 模块，将 16 kHz 单声道波形上采样至 48 kHz 立体声。

**训练流程**：训练分为四个阶段。首先进行 UALM-Gen 的音频生成预训练，在大规模文本-音频对上训练模型从文本生成音频码本令牌。随后进入模态对齐阶段——冻结 Transformer 主体与声学编码器，仅更新 MLP 适配器与音频嵌入表，以最小代价实现音频理解能力的注入。接着进行统一预训练，混合音频理解、音频生成与纯文本数据，使模型同时保持三类能力。最后通过多模态链式思维后训练获得 UALM-Reason，赋予模型“丰富-对话-自我反省”的生成式推理能力。

**关键设计决策**：音频生成阶段移除了传统 LM 方法中依赖的外部文本编码器，直接利用 LLM 内置 BPE 分词器处理文本提示；推理时采用分类器自由引导以增强指令遵循；并通过直接偏好优化对齐人类偏好。数据方面，音频生成预训练使用了 30M 样本（约 80k 小时），远超典型扩散模型的训练规模，是 LM 方法达到竞争性能的关键因素。

UALM 的核心由三个功能模块构成：音频生成模块（UALM-Gen）、模态对齐阶段，以及多模态推理后训练模块（UALM-Reason）。以下分别阐述其关键机制与支撑公式。

### 音频生成模块（UALM-Gen）

UALM-Gen 将文本到音频的生成任务统一为单一解码器语言模型的离散令牌预测问题。与依赖外部文本编码器（如 T5）的传统方法不同，UALM-Gen 直接利用预训练文本 LLM 的内置 BPE 分词器处理文本提示，消除了对外部嵌入的依赖。音频输出则通过预测离散音频码本令牌实现，采用 X-codec（50Hz 帧率）配合延迟模式（delay pattern）进行帧内自回归解码，以提升效率。

该模块引入两项关键训练与推理技术：

**分类器自由引导（CFG）** 是扩散模型中广泛使用的推理时技术，UALM 将其迁移到自回归语言模型的音频生成中。其核心是在条件分布与无条件分布之间进行插值，以增强模型对文本提示的遵循度：

$$\pi_{\theta}^{\mathrm{CFG}}(y_t|y_{1:t-1},x) = \lambda \cdot \pi_{\theta}(y_t|y_{1:t-1},x) + (1-\lambda) \cdot \pi_{\theta}(y_t|y_{1:t-1},\emptyset)$$

其中 $x$ 为条件（文本提示），$\emptyset$ 表示无条件生成，$\lambda$ 为引导权重。实验表明 $\lambda = 3.0$ 达到最优（Fig.5.a），移除 CFG 将导致提示遵循度严重下降（SongDescriber CL 从 0.45 降至 0.39，Table 8）。

**直接偏好优化（DPO）** 通过偏好对数据进一步对齐生成质量。给定获胜样本 $y_w$ 和失败样本 $y_l$，DPO 损失函数为：

$$\mathcal{L}_{\mathrm{DPO}}(\pi_{\theta}) = -\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\left[\log\sigma\left(\beta\log\frac{\pi_{\theta}(y_w|x)}{\pi_{\mathrm{ref}}(y_w|x)} - \beta\log\frac{\pi_{\theta}(y_l|x)}{\pi_{\mathrm{ref}}(y_l|x)}\right)\right]$$

其中 $\pi_{\theta}$ 为当前策略，$\pi_{\mathrm{ref}}$ 为参考模型，$\beta$ 控制偏离参考模型的程度。DPO 训练前需先将基模型在合成音频的获胜样本上微调约 1k 步，否则损失会在早期训练阶段急剧上升（Fig.5.c）。加入 DPO 后，SongDescriber 上 CL 从 0.45 升至 0.51，AES 从 6.70 升至 7.36（Table 8）。

### 模态对齐阶段

在统一预训练之前，UALM 引入一个专用的模态对齐阶段。此阶段冻结 Transformer 主体和声学编码器，仅更新 MLP 适配器和音频嵌入表。这一设计使音频连续表征能够平稳映射到 LLM 的嵌入空间，同时避免破坏预训练文本能力。消融实验表明，该阶段对统一预训练的成功至关重要（§2.3）。

### 增强 VAE 模块

为提升感知质量，UALM 在音频码本解码后级联一个增强 VAE，将 16kHz 单声道波形提升至 48kHz 立体声。其训练目标为：

$$\mathcal{L}_{\mathrm{VAE}} = \mathcal{L}_{\mathrm{stereoMRSTFT}} + \mathcal{L}_{\mathrm{logmel}} + \mathcal{L}_{\mathrm{adv}} + \mathcal{L}_{\mathrm{feat}} + \zeta \cdot \mathcal{L}_{\mathrm{KL}}$$

包含立体声多分辨率 STFT 损失、对数梅尔谱损失、对抗损失、特征匹配损失和 KL 散度正则项。该模块使 FD 指标大幅下降：SongDescriber 上从 224.72 降至 74.43（Table 8）。

### 多模态链式思维推理（UALM-Reason）

UALM-Reason 在基模型之上引入多模态链式思维（CoT）范式，使模型能够生成中间多模态推理步骤。其核心机制是将丰富字幕（rich caption）作为中间蓝图，支持三种推理模式：

- **丰富化（Enrichment）**：模型先生成详细的音频描述，再据此生成音频。
- **对话式推理（Dialogue）**：模型在理解与生成之间交替进行多轮交互。
- **自我反思（Self-reflection）**：模型分析并批判自身生成的音频，利用批判进行迭代优化。

该阶段通过监督微调实现，不引入额外公式，但其有效性在主观评估中得到验证：Enrichment 从 3.77 升至 4.01，Self-reflection 从 3.82 升至 4.04（Table 4）。

## 实验与关键发现

### 音频生成：自回归语言模型匹敌扩散模型

UALM 在音频生成上的核心主张是：通过数据规模扩展、分类器自由引导（CFG）和直接偏好优化（DPO），单一自回归语言模型可以匹敌前沿扩散模型的生成质量。**Table 1** 在 AudioCaps 和 SongDescriber 两个数据集上系统验证了这一主张。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_TsdlOjcQNu/figures/009_Table_1.jpg]]
*Table 1: Audio Generation results of UALM-Gen (§2.2) and UALM (§2.3) compared to LM-based and diffusion-based baselines. 5-scale subjective scores (OVL, REL) 95% CI ≈ 0.10. Bold indicates best, underline second-best*

在客观指标上，UALM 在 AudioCaps 上取得了最优的 Fréchet 距离（FD）65.87，显著优于扩散模型基线 ETTA 的 80.13（绝对值改善 14.26）。在提示遵循度（CL）上，UALM-Gen 达到 0.65，同样超越 ETTA 的 0.54。在 SongDescriber 数据集上，UALM-Gen 的主观总体质量评分（OVL）达到 4.07，优于基于语言模型的 MusicGen-stereo-L（3.91）和扩散模型 Stable Audio Open（3.93）。

值得注意的是，UALM-Gen 在 AudioCaps 上的音频美学评分（AES）达到 5.08，在所有对比方法中排名第一。这表明自回归语言模型在感知质量上不仅不逊于扩散模型，甚至可能在某些维度上取得优势。

### 音频理解：匹配专用开源模型

统一模型 UALM 在音频理解任务上匹配了当前最佳开源模型的水平（**Table 2**）。在 MMAU 基准上，UALM 的总体平均分（Sound+Music+Speech）达到 74.1，略高于音频理解专家模型 Audio Flamingo 3 的 72.3。在 MMAR 基准上，UALM 取得 55.2 的平均分。这一结果表明，将音频生成能力集成到同一模型中并未显著损害其理解性能。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_TsdlOjcQNu/figures/010_Table_2.jpg]]
*Table 2: Audio understanding results of UALM (§2.3) versus open-sourced understanding models*

### 文本能力保持：优于先前统一模型

多模态扩展通常会导致文本能力的灾难性遗忘，但 UALM 在这一问题上表现突出（**Table 3**）。在 MMLU（71.6）、GSM8K（92.1）和 HumanEval（81.1）三个核心文本基准上，UALM 仅出现轻微退化，显著优于先前的视觉和语音统一模型（如 Qwen2.5-Omni 的 MMLU 70.3、GSM8K 89.4、HumanEval 73.8）。这一优势归因于模态对齐阶段冻结 Transformer 主体的策略，有效保护了预训练文本能力。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_TsdlOjcQNu/figures/011_Table_3.jpg]]
*Table 3: Text capability of prior unified multimodal language models (in the vision domain) and our UALM. Our model is initialized from Qwen2.5-7B*

### 生成式推理：多模态链式思维的有效性

UALM-Reason 在推理导向生成上的主观评估结果（**Table 4**）验证了多模态链式思维（CoT）范式的有效性。在丰富（Enrichment）维度上，UALM-Reason 从基线的 3.77 提升至 4.01；在对话推理（Dialogue）上从 3.92 提升至 4.02；在自我反省（Self-reflection）上从 3.82 提升至 4.04。所有提升均在 95% 置信区间内具有统计显著性（CI ≈ 0.10）。这一结果证实了“丰富字幕作为中间蓝图→生成→自我批评→迭代优化”的推理链能够在统一模型中实现跨模态的生成推理能力。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_TsdlOjcQNu/figures/014_Table_4.jpg]]
*Table 4: 5-scale subjective score of UALM-Reason on reasoning-oriented generation with 95% CI*

### 消融研究：CFG、DPO 与增强 VAE 的因果作用

**Table 8** 的消融实验揭示了三个关键组件的因果贡献：

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_TsdlOjcQNu/figures/019_Table_8.jpg]]
*Table 8: Ablation study of UALM-Gen and UALM showing the effect of CFG, DPO, and Enhancement VAE. Objective metrics include: (1) Frechet distance (FD) using OpenL3 (Cramer et al., 2019) at 44.1kHz; (2) Kullback–Leibler divergence (KL) using PaSST (Koutini et al., 2022) at 32kHz; (3) Inception Score (IS) using PANNs (Kong et al., 2020) at 16kHz; (4) CLAP scores (CL) using LAION-CLAP (Wu et al., 2023) at 48kHz; (5) AudioBox-Aesthetic score (AES) (Tjandra et al., 2025) using an average of (CE, CU, PC, PQ) at 16kHz. Table 8 shows an ablation study of UALM-Gen and UALM. We note the ablation model without DPO and the enhancement VAE module using a ‘-Base’ suffix. First, activating CFG significantly improv...*

1. **CFG 的不可替代性**：移除 CFG 导致提示遵循度严重下降——SongDescriber 上的 CL 从 0.45 降至 0.39，OVL 从 3.68 降至 3.42。**Figure 5(a)** 进一步显示，CFG 权重 $\lambda = 3.0$ 为最优设置，无 CFG（$\lambda = 1.0$）时生成质量遭遇严重退化。CFG 的作用机制是在条件分布 $\pi_{\theta}(y_t|y_{1:t-1},x)$ 和无条件分布 $\pi_{\theta}(y_t|y_{1:t-1},\emptyset)$ 之间插值，增强指令遵循能力。

2. **DPO 的增量收益**：在 CFG 基础上引入 DPO 训练，SongDescriber 的 CL 从 0.45 进一步提升至 0.51，AES 从 6.70 升至 7.36。DPO 损失函数为：
   $$\mathcal{L}_{\mathrm{DPO}}(\pi_{\theta}) = -\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\left[\log\sigma\left(\beta\log\frac{\pi_{\theta}(y_w|x)}{\pi_{\mathrm{ref}}(y_w|x)} - \beta\log\frac{\pi_{\theta}(y_l|x)}{\pi_{\mathrm{ref}}(y_l|x)}\right)\right]$$
   其实施需注意一个关键细节：基础模型在真实音频上训练，而偏好数据来自合成音频，因此必须先对获胜样本进行约 1k 步的适配微调，否则 DPO 损失在训练早期会出现尖峰（**Figure 5(c)**）。

3. **增强 VAE 的感知质量飞跃**：增强 VAE 将 16kHz 单声道波形提升至 48kHz 立体声，使 Fréchet 距离大幅降低——SongDescriber 上从 224.72 降至 74.43，AudioCaps 上从 95.51 降至 65.87。这是所有消融中幅度最大的单一改进，表明音频表示的分辨率和通道数对感知质量有决定性影响。增强 VAE 的训练目标为：
   $$\mathcal{L}_{\mathrm{VAE}} = \mathcal{L}_{\mathrm{stereoMRSTFT}} + \mathcal{L}_{\mathrm{logmel}} + \mathcal{L}_{\mathrm{adv}} + \mathcal{L}_{\mathrm{feat}} + \zeta \cdot \mathcal{L}_{\mathrm{KL}}$$

### 数据规模的临界作用

**Figure 5(b)** 揭示了数据规模对自回归语言模型音频生成的临界性：当训练数据量从 30M 样本缩减至 1/32（约 94 万样本）时，模型过拟合且性能大幅下降。这一发现解释了先前基于语言模型的音频生成方法落后于扩散模型的关键瓶颈——扩散模型通常在不到 200 万样本上训练即可收敛，而自回归语言模型需要更大规模的数据才能有效泛化。UALM 使用的 30M 样本（约 80k 小时、17B 令牌）是突破这一瓶颈的关键。

### 理解与生成的收敛速度差异

**Figure 6** 展示了一个值得关注的训练动态：音频理解能力的收敛速度远快于音频生成能力。这一非对称性暗示两类任务对模型容量和训练数据的需求存在本质差异，理解任务可能主要依赖适配器与嵌入层的对齐，而生成任务需要更深层的分布建模。

### 评估的局限性

需注意以下方法学局限：主观评测仅使用 20 个测试提示，样本量较小可能影响统计稳健性；音频生成评估仅覆盖 AudioCaps 和 SongDescriber 两个数据集，对不同音频类型的泛化能力尚待验证；推理能力的评估主要依赖主观评分，缺乏大规模客观基准。此外，该工作仅验证了英文音频场景，未涵盖多语言和更复杂的音频事件组合。

## 定位与知识库关联

### 1. 与基线方法的关系

UALM 的核心贡献在于将音频理解、生成与推理统一到单一的自回归语言模型框架中，其方法定位需从音频生成、音频理解和统一多模态模型三个维度进行谱系梳理。

**音频生成维度：LM 范式对扩散范式的追赶。** 传统音频生成由扩散模型主导，代表工作包括 **ETTA** (Lee et al., 2024)、**TangoFlux** (Hung et al., 2024) 和 **Stable Audio Open** (Evans et al., 2024)。这些方法通常依赖外部文本编码器（如 T5 或 CLAP）将文本提示映射为条件嵌入，再通过扩散过程生成音频。基于语言模型的方法如 **MusicGen-stereo-L** (Copet et al., 2024) 和 **AudioGen-M** (Kreuk et al., 2022) 虽尝试用自回归方式建模离散音频码，但生成质量长期落后于扩散模型。UALM 的关键突破在于：通过将训练数据量扩展至 30M 样本（约 80k 小时），引入分类器自由引导（CFG）作为推理时技巧，并首次在 LM 文本到音频框架中集成直接偏好优化（DPO），使自回归 LM 的生成质量达到与前沿扩散模型竞争的水平。Table 1 显示，UALM-Gen 在 AudioCaps 上的 FD 降至 65.87，优于扩散基线 ETTA 的 80.13；在 SongDescriber 上的主观评分 OVL 达到 4.07，超越 MusicGen-stereo-L 的 3.91。这一结果打破了“自回归 LM 在音频生成上天然劣于扩散模型”的固有认知。

**音频理解维度：与专家模型和统一模型的对比。** 在理解侧，**Audio Flamingo 3** (Goel et al., 2025) 代表了音频理解专家模型的当前最佳水平，**Qwen2.5-Omni** (Xu et al., 2025) 则是在语音和音频理解上做统一的代表性工作。UALM 在 MMAU 基准上取得 74.1 的均值分数，略超 Audio Flamingo 3 的 72.3（Table 2），表明统一模型在理解能力上并未因加入生成任务而出现显著退化。这一结果验证了“理解与生成可以在同一模型中协同训练”的可行性。

**文本能力保持：优于先前视觉统一模型。** 与视觉领域的统一多模态模型相比，UALM 在文本推理能力上的退化幅度更小。Table 3 显示，UALM 在 MMLU 上保持 71.6、GSM8K 上保持 92.1、HumanEval 上保持 81.1，优于先前视觉统一模型在类似基准上的表现。这得益于 UALM 采用的模态对齐阶段策略——冻结 Transformer 主干和声学编码器，仅更新 MLP 适配器和音频嵌入表，从而最大限度地保留了预训练文本 LLM 的能力。

### 2. 关键设计选择的因果机制

UALM 的几项关键设计选择直接对应了其性能突破的因果链条：

| 设计选择 | 基线做法 | 因果机制 | 证据锚点 |
|:---|:---|:---|:---|
| 移除外部文本编码器 | 扩散模型依赖 T5/CLAP 编码器 | LLM 内置 BPE 分词器直接处理文本提示，消除外部编码器带来的信息瓶颈和架构冗余 | §2.2 |
| 数据规模扩展至 30M | 扩散模型通常 <2M 样本 | LM 范式对数据量更敏感，大规模数据使模型学习到更鲁棒的文本-音频映射 | Fig.5.b, §3.2 |
| 推理时 CFG (λ=3.0) | 扩散模型常用，LM 范式罕见 | 条件与无条件分布插值显著增强指令遵循度；移除 CFG 导致 SongDescriber CL 从 0.45 降至 0.39 | Table 8, Fig.5.a |
| DPO 对齐训练 | 未在 LM 音频生成中使用 | 利用偏好对优化模型，使获胜响应获得更高隐式奖励；SongDescriber CL 从 0.45 提升至 0.51，AES 从 6.70 提升至 7.36 | Table 8 |
| 增强 VAE | 无后处理或简单上采样 | 将 16kHz 单声道提升至 48kHz 立体声，大幅改善感知质量；SongDescriber FD 从 224.72 降至 74.43 | Table 8, Appendix B.2 |
| 模态对齐阶段 | 直接微调或联合训练 | 冻结主干仅更新适配器，防止音频模态的引入破坏文本能力 | §2.3 |

### 3. 适用边界与局限

尽管 UALM 在统一音频语言模型上取得了显著进展，其适用边界和局限同样明确：

**模态与语言覆盖。** 当前工作仅验证了英文音频场景的统一，未涵盖多语言提示和更复杂的音频事件组合（如多声源重叠、长时域场景切换）。模型对非英语指令的遵循度和跨文化音频概念的理解能力尚待验证。

**推理评估的客观性不足。** UALM-Reason 的推理能力评估主要依赖 20 个测试提示的主观评分（Table 4），缺乏大规模、可复现的客观推理质量基准。Enrichment 从 3.77 提升至 4.01、Self-reflection 从 3.82 提升至 4.04 的结果虽在统计上显著（95% CI ≈ 0.10），但样本量限制了结论的泛化性。

**计算与数据成本。** 模型以 Qwen2.5-7B 为骨干，音频生成需 30M 训练样本，预训练在 16 节点 × 8 张 A100 80GB GPU 上进行 660,000 步。增强 VAE 虽有效提升 48kHz 立体声保留能力，但引入了额外的模型复杂性和推理开销。这些因素共同限制了 UALM 在资源受限环境中的部署可行性。

**生成评估的覆盖范围。** 音频生成评估仅覆盖 AudioCaps 和 SongDescriber 两个数据集，分别代表通用音频和音乐场景。对于语音合成、环境声事件生成等细分任务的泛化能力尚未得到系统性验证。

### 4. 开放问题

论文明确提出的开放问题包括：

1. **统一音频表示的设计。** 如何构建一个统一的音频表示，以同时促进理解、生成和推理的可扩展训练？当前 UALM 在输入端使用连续声学特征，输出端使用离散 RVQ 令牌，两端表示的不对称可能限制联合建模的上限。

2. **合成音频字幕的质量评估。** UALM 依赖合成丰富字幕进行多模态链式思维训练，但如何设计可量化的方法来评估这些合成字幕的质量，目前仍是一个未解决的问题。

3. **复杂生成场景的评估指标。** 现有音频质量评估指标（FD、KL、IS、CLAP 分数）在复杂音频生成和多模态推理链场景下的适用性存疑，需要开发更细粒度的评估体系。

4. **推理链中自反思的忠实性。** 在多模态推理中，模型对自身生成音频的批评和反思是否真正基于音频内容，还是仅依赖文本先验进行表面推理？是否可以将外部验证信号（如客观音频质量指标）引入循环以增强忠实性？

5. **跨模态扩展的可能性。** 该统一框架是否可以扩展到其他音频相关模态（如音乐简谱、环境声事件标签、语音情感标注）的生成与推理？这需要重新审视模态对齐策略和训练数据混合比例的通用性。

## 原文 PDF

![[paperPDFs/ICLR_2026/UALM_Unified_Audio_Language_Model_for_Understanding_Generation_and_Reasoning.pdf]]
