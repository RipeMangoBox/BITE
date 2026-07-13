---
title: "WAVE: Learning Unified & Versatile Audio-Visual Embeddings with Multimodal LLM"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/WAVE_Learning_Unified_Versatile_Audio_Visual_Embeddings_with_Multimodal_LLM.pdf
project_link: null
code_link: https://github.com/TCL606/WAVE
openreview_forum_id: MiV3WXDYJb
aliases:
- WAVE
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "层次化特征融合策略、联合多模态多任务训练及双音频编码器设计是实现高性能通用嵌入的关键机制。"
primary_logic: "通过在MLLM所有层上聚合last-token特征并经轻量级MLP融合，同时结合跨模态对比学习与指令感知的问答训练，WAVE能产生统一的、任务特定的嵌入，支持任意模态间的检索与推理。"
claims:
- "WAVE在MMEB-v2视频基准上全面超越开源模型，整体得分59.9相较于最强基线Seed-1.6-Embedding的55.3提升显著。"
- "联合训练在8项任务中的7项上优于独立训练，验证跨模态知识迁移的正向作用。"
- "使用分离问题提示的嵌入在视频QA任务上平均得分72.5，远超通用提示的51.8，证实指令感知嵌入的有效性。"
- "全层last-token融合（MLP fusion）在音视频检索上优于仅最后一层池化（last layer pooling），平均提升约1.4%。"
---

# WAVE: Learning Unified & Versatile Audio-Visual Embeddings with Multimodal LLM

> [!tip] 核心洞察
> 通过在MLLM所有层上聚合last-token特征并经轻量级MLP融合，同时结合跨模态对比学习与指令感知的问答训练，WAVE能产生统一的、任务特定的嵌入，支持任意模态间的检索与推理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | WAVE: 基于多模态大语言模型的统一通用音视频嵌入学习 |
| 英文题名 | WAVE: Learning Unified & Versatile Audio-Visual Embeddings with Multimodal LLM |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=MiV3WXDYJb) · [GitHub](https://github.com/TCL606/WAVE) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | WAVE |
| Dataset | MMEB-v2-Video (Overall), MMEB-v2-Video QA (w/ separate questions), AudioCaps (A-RET), Clotho (A-RET) |

> [!tip] 效果简介
> - MMEB-v2-Video (Overall) 上，Overall Accuracy 为 59.9，对比 55.3 (Seed-1.6-Embedding)，变化 +4.6。
> - MMEB-v2-Video QA (w/ separate questions) 上，Accuracy 为 72.5，对比 60.9 (Seed-1.6-Embedding)，变化 +11.6。
> - AudioCaps (A-RET) 上，R@1 为 44.2，对比 42.2 (Mei et al., 2024)，变化 +2.0。

## 概要

**问题瓶颈**：现有多模态大语言模型（MLLM）的嵌入方法主要聚焦于静态图像，忽视了音频与同步音视频流的统一表示，导致无法构建真正的通用音视频嵌入空间。

**核心方案**：WAVE 是首个基于 MLLM 的统一通用音视频嵌入模型。其核心机制包括三个关键设计：一是**层次化特征融合策略**——聚合 MLLM 所有层的 last-token 状态，经两层 MLP-GELU 压缩为最终嵌入；二是**双音频编码器架构**——在语音编码器之外引入 BEATs 通用音频编码器，覆盖环境声等非语音信息；三是**联合多模态多任务训练**——同时进行跨模态检索对比学习与指令感知的问答训练，实现跨模态知识迁移。

**主要结果**：WAVE 在 MMEB-v2 视频基准上以整体得分 59.9 全面超越最强基线 Seed-1.6-Embedding（55.3）；在视频 QA 任务上，使用分离问题提示的指令感知嵌入平均得分达 72.5，远超通用提示的 51.8；在 AudioCaps 和 Clotho 音频检索上分别达到 R@1 44.2 和 25.6；在 VGGSound 和 MusicCaps 音视频检索上分别达到 R@1 25.0 和 20.4，较仅编码器基线提升超过 10 个百分点。

**方法定位**：WAVE 属于基于 MLLM 的统一嵌入学习范式，区别于 LamRA、GME、CAFe 等仅处理视觉-文本的嵌入 LLM，首次将音频与同步音视频纳入统一表示空间。其技术路线融合了多模态对比学习与指令微调，在方法谱系中处于“通用多模态嵌入大模型”节点。



多模态嵌入旨在将不同模态的数据映射到统一的向量空间，使语义相似的样本彼此靠近，从而支撑跨模态检索、问答等下游任务。近年来，基于大语言模型的嵌入方法在文本与图像领域取得了显著进展，但其焦点长期局限于静态视觉模态，对音频及同步音视频流的统一建模关注不足。这一缺口导致现有方案难以构建真正通用的音视频嵌入空间——当任务需要同时理解画面中的动作、场景以及与之同步的语音、环境声时，缺乏统一表示的模型往往顾此失彼。

具体而言，当前方法面临三重瓶颈。其一，音频模态的嵌入建模严重滞后于视觉。主流多模态LLM嵌入工作（如**LamRA 7B** (Liu et al., 2025a)、**GME 7B** (Zhang et al., 2024)、**CAFe 7B** (Yu et al., 2025a)）主要围绕视频-文本检索展开，对音频-文本检索、音视频跨模态检索的支持极为有限。其二，即使部分模型能够处理视频输入，其嵌入提取策略也普遍采用标准last-token pooling——仅从LLM的最后一层隐藏状态中取出EOS对应的表示作为最终嵌入。这种单层池化丢弃了中间层的丰富语义信息，限制了嵌入的表达能力。其三，现有训练范式通常以单一模态对的对比学习为主，缺乏跨模态、多任务的联合训练机制，导致模型无法在检索与问答等异质任务间实现知识迁移。

WAVE的动机正是填补上述空白：构建一个同时覆盖文本、音频、视频的统一嵌入空间，使任意模态之间均可进行语义检索与推理。为实现这一目标，WAVE在架构上引入层次化特征融合策略，聚合LLM所有层的last-token状态；在输入侧采用双音频编码器设计，分别捕捉语音和通用音频事件；在训练侧实施多模态多任务联合训练，融合检索式对比学习与指令感知的问答训练。这种“全层融合+双路音频+联合训练”的组合机制，构成了WAVE突破单一模态嵌入范式的核心因果路径。



## 核心方法与创新机理

WAVE的核心创新在于将多模态大语言模型（MLLM）的嵌入能力从静态图像拓展至音频与同步音视频流，构建了首个统一文本、音频、视频三种模态的通用嵌入空间。其关键突破体现在三个互为支撑的机制上。

### 层次化特征融合策略

现有MLLM嵌入方法普遍采用标准的last-token pooling，即仅提取LLM最后一层输出的EOS隐藏状态作为最终嵌入。WAVE提出了一种**层次化特征融合策略**：聚合LLM所有层的last-token状态，将这些跨层表示拼接后，输入一个轻量级的两层MLP-GELU融合模块进行非线性变换与压缩，生成最终的统一嵌入（Figure 1, Section 3.1）。

这一设计的直接因果效应在于同时保留了浅层的感知线索与深层的语义推理信息。消融实验（Table 7）证实，全层MLP融合在音视频检索（A+V）上相比仅使用最后一层池化平均提升约1.4%（56.1 vs 54.7），验证了跨层信息聚合对多模态表示质量的增益。

### 双音频编码器设计

传统语音-文本嵌入模型通常仅依赖单一语音编码器（如基于Whisper的Qwen2.5-Omni speech encoder），难以充分捕捉环境声、音乐等非语音音频事件。WAVE在保留原有语音编码器的基础上，额外引入**BEATs通用音频编码器**，两者特征经两层MLP对齐后，按一对一方式交织输入LLM，使模型同时捕获语音语义与通用音频事件信息（Section 3.1, Appendix E）。

消融实验（Table 9）表明，双编码器设计相比单一语音编码器在音频检索和音视频检索上均有明显提升。这一机制直接支撑了WAVE在AudioCaps（R@1: 44.2 vs 42.2）和Clotho（R@1: 25.6 vs 21.5）上对Mei et al., 2024的显著超越（Table 4）。

### 联合多模态多任务训练与指令感知嵌入

现有嵌入模型通常仅在单一模态对（如图文或视频-文本）上进行检索式对比学习。WAVE采用了**联合多模态多任务训练**方案：同时训练视频-文本检索、视频问答、视频-音频检索和音频-文本检索四类任务，采用任务感知数据采样器确保每个mini-batch来自同一任务类型（Table 1, Section 3.2）。

联合训练的核心因果效应在于**跨模态知识迁移**。Table 6的消融实验显示，联合训练在8项任务中的7项上优于独立训练（如MMEB-v2-Video Overall: 59.0 vs 58.2），验证了多模态多任务协同对通用嵌入空间的正向塑造作用。

更进一步，WAVE利用MLLM的指令遵循能力生成**指令感知嵌入**。在视频QA任务中，使用分离问题提示（separate questions）产生的嵌入平均得分72.5，远超通用提示的51.8（Table 5），证实模型能够根据文本指令动态调整嵌入的语义焦点。Figure 2的热力图直观展示了同一视频在不同提示下生成的嵌入与不同概念文本嵌入的余弦相似度差异，揭示了指令感知嵌入的可控语义聚焦能力。



WAVE 的整体架构围绕一个核心设计原则展开：将多模态大语言模型（MLLM）转化为一个统一的嵌入提取器，使其能够为文本、图像、音频和视频四种模态生成可互检索的向量表示。图1展示了完整的端到端信息流。

### 输入模态与编码

系统接受四种输入组合：纯文本、纯视觉（图像或无声视频帧）、纯音频、以及同步音视频流。对于非文本模态，WAVE 采用专用编码器进行前置处理：

- **视觉编码器**：提取视频帧特征并将其转换为视觉 token 序列。
- **语音编码器**：基于 Whisper 架构（继承自 Qwen2.5-Omni），负责捕获语音相关特征，生成语音 token。
- **音频编码器 + 对齐器**：额外引入 BEATs 通用音频编码器，专门捕获环境声、音乐等非语音音频事件特征。其输出经过一个两层 MLP 对齐模块后生成音频事件 token。

这种双音频编码器设计是 WAVE 区别于仅依赖语音编码器的基线方案的关键改进（见 Table 9）。

### Token 交织与位置编码

不同模态的 token 按照特定策略交织后输入 LLM 骨干网络：

- **纯音频输入**：语音 token 与音频事件 token 以一对一方式交替排列。
- **同步音视频输入**：视觉 token 序列与听觉 token 序列按时间步分块后交织，确保同一时间帧的视觉和听觉 token 在序列中相邻。

为保证时空结构的一致性，WAVE 采用 Qwen2.5-Omni 引入的 **TMRoPE（时间对齐多模态旋转位置嵌入）**。同一帧对应的所有 token 共享相同的旋转位置嵌入，从而在位置编码层面实现精确的时间对齐。

### LLM 骨干与嵌入提取

经过交织的多模态 token 序列与文本指令提示（text prompt）拼接后，送入 **Qwen2.5-Omni 7B** 作为骨干 LLM。模型通过 LoRA（秩为 128，缩放因子 2.0，dropout 0.05）进行高效微调，冻结大部分预训练参数。

嵌入提取策略是 WAVE 的核心技术创新之一。与标准做法仅取 LLM 最后一层的 EOS 隐藏状态不同，WAVE 采用**层次化特征融合**：

1. 收集 LLM 所有层输出的 last-token 状态。
2. 将这些状态拼接为一个长向量。
3. 输入一个轻量级的两层 MLP（GELU 激活函数），将其压缩为最终的统一嵌入。

对于纯文本输入，则直接对 LLM 最后一层隐藏状态进行 last-token pooling 获得嵌入。

### 训练任务与损失函数

WAVE 在四个任务上联合训练（见表1），采用任务感知的数据采样器，确保每个 mini-batch 来自同一任务类型：

- **视频-文本检索**：双向对比学习，使用对称的交叉熵损失。以源嵌入为查询的损失为：

$$\mathcal{L}_{s_i} = -\log \frac{\exp(\sin(e_{s_i}, e_{t_i}) / \tau)}{\sum_{j=1}^{N} \exp(\sin(e_{s_i}, e_{t_j}) / \tau)}$$

其对称项以目标嵌入为查询，最终检索损失为二者的平均：

$$\mathcal{L}_{\mathrm{Retrieval}} = \frac{1}{2N} \sum_{i=1}^{N} (\mathcal{L}_{s_i} + \mathcal{L}_{t_i})$$

- **视频问答（QA）**：将 QA 建模为从候选答案池中选择正确选项的检索任务，损失函数在正样本与多个干扰答案之间计算对比：

$$\mathcal{L}_{\mathsf{QA}_i} = -\log \frac{\exp(\sin(e_{s_i}, e_{t_i}) / \tau)}{\exp(\sin(e_{s_i}, e_{t_i}) / \tau) + \sum_{k=1}^{n} \exp(\sin(e_{s_i}, e_{t_{i,k}}') / \tau)}$$

- **视频-音频检索**与**音频-文本检索**：同样采用双向对比学习框架，训练跨模态对齐。

温度参数 $\tau$ 统一设置为 0.01。整个训练在 192 块 H20 GPU 上进行一个 epoch，总耗时约 36 小时，学习率为 $2 \times 10^{-5}$。



### 3.1 统一嵌入提取流程

WAVE 的核心设计目标是从文本、视觉、音频及音视频同步流中提取统一的嵌入表示。其嵌入提取流程由以下关键模块构成：

**多模态编码器组。** 非文本输入由三个独立编码器处理：预训练视觉编码器提取视频帧特征并转换为视觉 token；基于 Whisper 的语音编码器（继承自 Qwen2.5-Omni）捕捉语音相关特征；额外引入的 BEATs 音频编码器负责捕获通用音频事件（环境声、音乐等），其输出经两层 MLP 对齐后生成音频事件 token。语音 token 与音频事件 token 按一对一交织方式送入 LLM，以覆盖非语音音频信息。

**时间对齐位置编码（TMRoPE）。** 对于同步音视频输入，视觉 token 与听觉 token 序列按时间步分区，同一时间步的 token 共享相同的 TMRoPE 位置嵌入，确保精确的时空对齐。

**层次化特征融合。** 对于多模态输入，WAVE 不采用传统的仅取 LLM 最后一层 EOS 隐藏状态的池化方式，而是收集 LLM 所有层的 last-token 状态，将其拼接后送入一个轻量级融合模块——两层 MLP（GELU 激活）——进行非线性变换与压缩，生成最终的统一嵌入。对于纯文本输入，则直接对 LLM 最后一层隐藏状态执行 last-token pooling。

这一设计的关键直觉是：低层特征保留感知线索，高层特征承载语义推理，全层聚合使嵌入同时受益于两者。

### 3.2 训练目标

WAVE 采用联合多任务训练框架，同时优化检索损失与问答损失。

**双向对比检索损失。** 给定一个 mini-batch 中的 $N$ 对源-目标样本，以源嵌入 $e_{s_i}$ 为查询、目标嵌入 $e_{t_j}$ 为候选的对比损失定义为：

$$\mathcal{L}_{s_i} = -\log \frac{\exp(\sin(e_{s_i}, e_{t_i}) / \tau)}{\sum_{j=1}^{N} \exp(\sin(e_{s_i}, e_{t_j}) / \tau)} \tag{1}$$

其中 $\sin(\cdot,\cdot)$ 表示余弦相似度，$\tau$ 为温度参数（设为 $0.01$）。对称地，以目标嵌入为查询的损失为：

$$\mathcal{L}_{t_i} = -\log \frac{\exp(\sin(e_{t_i}, e_{s_i}) / \tau)}{\sum_{j=1}^{N} \exp(\sin(e_{t_i}, e_{s_j}) / \tau)} \tag{2}$$

整个 batch 的平均双向检索损失为：

$$\mathcal{L}_{\mathrm{Retrieval}} = \frac{1}{2N} \sum_{i=1}^{N} (\mathcal{L}_{s_i} + \mathcal{L}_{t_i}) \tag{3}$$

**问答损失。** 对于 QA 任务，模型需从包含 $n$ 个干扰答案的候选池中选择正确选项。损失函数为：

$$\mathcal{L}_{\mathsf{QA}_i} = -\log \frac{\exp(\sin(e_{s_i}, e_{t_i}) / \tau)}{\exp(\sin(e_{s_i}, e_{t_i}) / \tau) + \sum_{k=1}^{n} \exp(\sin(e_{s_i}, e_{t_{i,k}}') / \tau)} \tag{4}$$

其中 $e_{t_{i,k}}'$ 为第 $k$ 个干扰答案的嵌入。整个 batch 的平均 QA 损失为：

$$\mathcal{L}_{\mathrm{QA}} = \frac{1}{N} \sum_{i=1}^{N} \mathcal{L}_{\mathrm{QA}_i} \tag{5}$$

**任务感知采样。** 训练时采用任务感知数据采样器，确保每个 mini-batch 内的样本来自同一任务类型，避免跨任务梯度冲突。四个训练任务（视频-文本检索、视频 QA、视频-音频检索、音频-文本检索）共涵盖约 4.9M 样本对。

### 3.3 指令感知嵌入机制

WAVE 的关键能力之一是生成指令感知嵌入：同一视频在不同文本提示下产生不同的嵌入表示。对于多模态输入，文本提示始终作为指令输入 LLM，引导模型关注与任务相关的语义维度。这一机制使 WAVE 在视频 QA 任务上展现出显著优势——使用分离问题提示的嵌入平均得分 72.5，远超通用提示的 51.8（Table 5），验证了指令条件对嵌入语义的调控作用。



## 实验与关键发现

### 主实验结果

WAVE在视频、音频及音视频多模态嵌入任务上均展现出显著优势，在多个基准上全面超越现有开源与工业级基线模型。

**视频嵌入基准。** 在MMEB-v2-Video整体得分上，WAVE以59.9分大幅领先最强基线**Seed-1.6-Embedding**的55.3分（+4.6），并远超其他视频嵌入LLM基线如**LamRA 7B**（Liu et al., 2025a）、**GME 7B**（Zhang et al., 2024）和**CAFe 7B**（Yu et al., 2025a）（Table 3）。在LoVR主题到片段检索任务上，WAVE的R@25达到66.0，优于LamRA 7B的60.2（+5.8），进一步验证其跨视频理解能力。


![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_MiV3WXDYJb/figures/004_Table_3.jpg]]
*Table 3: Results of video embedding benchmarks. Models are evaluated on the video track of MMEB-v2 and LoVR*

**音频与音视频嵌入基准。** 在音频-文本检索（A-RET）上，WAVE在AudioCaps数据集上R@1达到44.2，超过**Mei et al., 2024**的42.2（+2.0）；在Clotho数据集上R@1达25.6，较基线21.5提升4.1个点（Table 4）。在更具挑战性的音视频检索（AV-RET）任务上，WAVE在VGGSound上R@1为25.0，相较encoder-only检索基线的10.3提升14.7个点；在MusicCaps上R@1为20.4，相较基线8.6提升11.8个点。这些结果表明双音频编码器设计（Whisper-based语音编码器 + BEATs通用音频编码器）有效捕获了环境声与音乐等非语音信息。


![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_MiV3WXDYJb/figures/005_Table_4.jpg]]
*Table 4: Results of audio and audio-visual embedding benchmarks. Different tasks are evaluated, including audio retrieval (A-RET), audio-visual retrieval (AV-RET) and audio QA (A-QA)*

**视频问答（QA）基准。** WAVE在MMEB-v2视频QA任务上的表现尤其突出。当使用分离问题提示（separate questions）生成指令感知嵌入时，平均得分达到72.5，远超通用提示（common prompt）下的51.8，并显著优于Seed-1.6-Embedding的60.9（+11.6）（Table 5）。这一结果直接验证了WAVE的指令感知嵌入机制：MLLM骨干根据不同的文本提示动态调整语义焦点，从而为每个问题生成任务特定的嵌入表示。


![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_MiV3WXDYJb/figures/006_Table_5.jpg]]
*Table 5: Results of different models on MMEB-v2 video QA data, including Video-MME (Fu et al., 2025), MVBench (Li et al., 2024), NExT-QA (Xiao et al., 2021), EgoSchema (Mangalam et al., 2023), and ActivityNetQA (Yu et al., 2019). In the case of “w/ separate questions”, each question is used as a different prompt*

### 消融实验

通过系统的消融研究，本文揭示了WAVE性能提升的关键因果机制。

**联合训练 vs. 独立训练。** Table 6对比了联合多模态多任务训练与独立训练（separate training）的效果。联合训练在8项评估任务中的7项上优于独立训练，例如MMEB-v2-Video整体得分从58.2提升至59.0。这证实了跨模态知识迁移的正向作用：不同模态和任务之间的共享表征学习能够构建更鲁棒、更通用的嵌入空间。

**层次化特征融合策略。** Table 7对比了不同嵌入提取方法。全层last-token融合（MLP fusion）在音视频条件下的视频检索平均得分为56.1，相较仅使用最后一层池化（last layer pooling）的54.7提升约1.4%。这一结果表明，聚合LLM所有层的last-token状态能够同时保留低层感知线索与高层语义推理信息，而轻量级两层MLP-GELU融合模块有效压缩并整合了这些多层次特征。此外，音频信息的引入将纯视觉条件下的检索得分从54.7提升至56.1，验证了音视频联合建模的增益。


![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_MiV3WXDYJb/figures/008_Table_7.jpg]]
*Table 7: Results of embedding extraction methods on the MMEB-v2 video retrieval data, including MSR-VTT, VATEX, MSVD, DiDeMo, and YouCook2. Note that videos in MSR-VTT, VATEX, and YouCook2 are paired with audio. “V” and “A+V” refer to visual-only and audio-visual, respectively*

**双音频编码器设计。** Table 9的消融显示，采用双编码器（语音编码器 + BEATs音频编码器）相比仅使用单一语音编码器，在音频检索和音视频检索上均有明显提升。BEATs编码器专门捕获通用音频事件特征（如环境声、音乐），弥补了语音编码器对非语音音频理解的不足。


![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_MiV3WXDYJb/figures/011_Table_9.jpg]]
*Table 9: Results of using dual speech and audio encoders and using a speech encoder only. Video retrieval (V-RET), audio retrieval (A-RET), and audio-visual retrieval (AV-RET) are evaluated here*

**图像训练数据的影响。** Table 10表明，在训练中加入图像数据不仅大幅提升图像检索性能，对视频检索也有轻微增益。这说明静态图像与动态视频之间存在可迁移的视觉表征知识。


![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_MiV3WXDYJb/figures/012_Table_10.jpg]]
*Table 10: Comparison of results for training with and without image data. We evaluate text-toimage retrieval (Liu et al., 2021) on the VisualNews dataset and text-to-video retrieval on MMEBv2-Video*

**指令感知嵌入的有效性。** Table 5的核心发现——分离问题提示下QA性能从51.8跃升至72.5——揭示了指令感知嵌入的关键作用。Figure 2通过热力图直观展示了这一机制：同一视频在不同文本提示下生成的嵌入与各概念文本嵌入的余弦相似度呈现显著差异，证明WAVE能根据指令动态调整语义焦点，而非产生静态的通用表示。

### 关键图表结论

- **Figure 1**：架构图清晰展示了WAVE的多模态输入处理流程、层次化last-token融合机制以及文本提示始终作为指令输入的设计原则。
- **Table 3 & Table 4**：主结果表确立了WAVE在视频、音频、音视频三大模态嵌入任务上的全面领先地位。
- **Table 5**：指令感知嵌入的定量证据，分离问题提示带来超过20个点的QA性能提升。
- **Table 6**：联合训练的因果证据，8项任务中7项受益于跨模态知识迁移。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_MiV3WXDYJb/figures/007_Table_6.jpg]]
*Table 6: Comparison of model performance under separate vs. joint training schemes. The model jointly trained on all modalities and tasks consistently outperforms specialist models trained on separate modality-task pairs*

- **Table 7**：层次化融合策略的因果证据，全层MLP融合优于传统最后一层池化。

### 补充图表

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_MiV3WXDYJb/figures/002_Table_1.jpg]]
*Table 1: An overview of training tasks and data. Four tasks are trained for our models: video-text retrieval, video-QA, video-autio retrieval and audio-text retrieval*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_MiV3WXDYJb/figures/003_Table_2.jpg]]
*Table 2: Details of the evaluation benchmarks. We formulate all tasks as “query-to-target” retrieval*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_MiV3WXDYJb/figures/009_Table_8.jpg]]
*Table 8: Results of video-to-text, audio-to-text and audio-to-video retrieval. Corresponding reference models and their scores are also provided*



## 定位与知识库关联

### 1. 问题定位与基线对比

WAVE 的核心定位是构建首个基于大语言模型的、覆盖文本、音频和视频的统一嵌入空间。此前，多模态 LLM 嵌入方法（如 **LamRA 7B**（Liu et al., 2025a）、**GME 7B**（Zhang et al., 2024）、**CAFe 7B**（Yu et al., 2025a））主要聚焦于静态图像或视频-文本对齐，忽视了音频模态以及同步音视频流的统一表示。工业级方案如 **Seed-1.6-Embedding** 虽在视频基准上表现强劲（MMEB-v2 Overall 55.3），但同样缺乏对音频模态的原生支持。

WAVE 与上述基线的方法论差异体现在三个关键维度：

- **模态覆盖**：WAVE 首次将音频（含语音与环境声）纳入 LLM 嵌入的统一框架，而 LamRA、GME、CAFe 等仅处理视觉与文本。
- **嵌入提取策略**：基线方法通常采用标准的 last-token pooling（仅使用 LLM 最后一层的 EOS 隐藏状态），WAVE 则聚合所有 LLM 层的 last-token 状态，经两层 MLP-GELU 融合模块压缩为最终嵌入（Section 3.1, Table 7）。
- **音频编码架构**：基线方法若涉及音频，通常仅依赖单一语音编码器（如 Qwen2.5-Omni 自带的 Whisper-based speech encoder）。WAVE 采用双编码器设计，额外引入 **BEATs** 音频编码器捕获通用音频事件特征，两者经对齐后交织输入 LLM（Appendix E, Table 9）。

### 2. 方法继承与创新

WAVE 构建于 **Qwen2.5-Omni 7B**（Xu et al., 2025）之上，继承了其 TMRoPE（Time-aligned Multimodal Rotary Position Embedding）位置编码机制，确保同一时间步的音视频 token 共享相同的旋转位置嵌入。在此基础上，WAVE 的方法论创新可归纳为三个因果性操作：

1. **层次化特征融合**（Hierarchical Feature Fusion）：摒弃标准的单层 last-token pooling，改为收集 LLM 所有层的 last-token 隐藏状态，拼接后送入两层 MLP-GELU 融合模块。这一设计同时保留了低层感知线索和高层语义推理信号，在音视频检索上相较 last layer pooling 平均提升约 1.4%（Table 7）。

2. **双音频编码器**（Dual Audio Encoder）：在原有语音编码器之外引入 BEATs 音频编码器，专门捕获环境声、音乐等非语音音频事件。两者特征经对齐模块后交织输入 LLM，使模型能够区分并联合建模语音内容与背景声学场景（Section 3.1, Table 9）。

3. **联合多模态多任务训练**（Joint Multi-modal Multi-task Training）：采用任务感知数据采样器，确保每个 mini-batch 来自同一任务类型，联合训练视频-文本检索、视频 QA、视频-音频检索和音频-文本检索四类任务。消融实验表明，联合训练在 8 项任务中的 7 项上优于独立训练（Table 6），验证了跨模态知识迁移的正向作用。

### 3. 适用边界与局限

尽管 WAVE 在多个基准上取得了领先结果，其适用边界仍需审慎界定：

- **模态范围**：当前统一嵌入空间覆盖文本、图像、音频和视频，但论文未涉及 3D 点云、触觉、深度图等其他模态。WAVE 的层次化融合策略是否能泛化到这些模态，仍需进一步验证。
- **模型规模**：WAVE 基于 7B 参数的 Qwen2.5-Omni 构建。虽然 LoRA 高效微调（rank=128, scaling factor=2.0）控制了训练成本（192 H20 GPU，约 36 小时），但更大规模 MLLM 上的可扩展性尚未探索。
- **QA 任务的静态表示限制**：在视频 QA 任务上，使用分离问题提示（separate questions）的指令感知嵌入显著优于通用提示（72.5 vs 51.8, Table 5），表明单一静态表示无法充分捕捉复杂多模态问答的细粒度语义需求。这一局限性在需要指代表达理解或时序推理的场景中可能更为突出。
- **训练数据依赖性**：WAVE 的训练数据总量为 4.9M 样本（Table 1），覆盖视频-文本检索、视频 QA、视频-音频检索和音频-文本检索四类任务。引入图像训练数据虽能提升图像检索并轻微增益视频检索（Table 10），但论文未系统分析数据配比与性能上限的关系。

### 4. 开放问题

1. **跨模态迁移的未解机制**：WAVE 的统一嵌入空间如何在未经显式训练的情况下实现跨模态转移至音频推理任务？这一现象的深层机制尚不明确。

2. **静态嵌入的根本限制**：对于需要动态语义聚焦的复杂多模态问答任务，单一静态表示存在哪些根本性限制？指令感知嵌入（Figure 2 的热力图已初步展示其动态调节能力）是否足以弥补这一差距？

3. **层次化融合的可泛化性**：WAVE 的全层 last-token 融合策略是否能泛化到更大规模的 MLLM 或更多模态（如 3D 点云、触觉）？融合模块的结构（当前为两层 MLP-GELU）是否需要随模型规模调整？

4. **细粒度对齐的精度缺口**：指令感知嵌入与通用嵌入在细粒度多模态对齐任务（如指代表达理解、时序定位）上的性能差异尚未被系统评估，这可能是 WAVE 框架的下一个重要验证方向。



## 原文 PDF

![[paperPDFs/ICLR_2026/WAVE_Learning_Unified_Versatile_Audio_Visual_Embeddings_with_Multimodal_LLM.pdf]]
