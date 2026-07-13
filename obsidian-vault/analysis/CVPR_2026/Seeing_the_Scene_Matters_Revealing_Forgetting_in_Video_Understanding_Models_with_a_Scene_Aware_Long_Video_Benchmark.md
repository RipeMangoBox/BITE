---
title: "Seeing the Scene Matters: Revealing Forgetting in Video Understanding Models with a Scene-Aware Long-Video Benchmark"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Seeing_the_Scene_Matters_Revealing_Forgetting_in_Video_Understanding_Models_with_a_Scene_Aware_Long_Video_Benchmark.pdf
project_link: null
code_link: null
huggingface_link: "https://huggingface.co/datasets/SinerChen/SceneBench"
aliases:
- SR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 模型是否具备以场景为单位的动态记忆构建与检索能力，从而整合跨时间段的视觉与音频证据。
primary_logic: 将视频组织为语义连贯的场景片段，并通过检索增强生成（RAG）机制按需提供相关场景记忆，可显著缓解长程遗忘，提升场景级推理性能。
claims:
- 随着问题与答案之间的时间距离增加，模型准确率显著下降，但Scene-RAG能在中长距离上保持较高准确率，缓解遗忘。
- 场景级任务（SceneQA）较片段级任务（ClipQA）准确率大幅度下降（开源的MLLMs平均-25.62点，-49.5%），而Scene-RAG在SceneBench上带来平均+1.40%的绝对提升。
- 在Video-MME基准上，Scene-RAG相比非RAG基线平均提升10.47点，验证了场景级检索增强在通用长视频理解上的有效性。
- SceneBench 上 平均任务准确率增益（6任务） = 无RAG基线 +1.40%（Scene-RAG平均增益）
---

# Seeing the Scene Matters: Revealing Forgetting in Video Understanding Models with a Scene-Aware Long-Video Benchmark

> [!tip] 核心洞察
> 将视频组织为语义连贯的场景片段，并通过检索增强生成（RAG）机制按需提供相关场景记忆，可显著缓解长程遗忘，提升场景级推理性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 场景感知的长视频理解基准揭示视频理解模型中的遗忘 |
| 英文题名 | Seeing the Scene Matters: Revealing Forgetting in Video Understanding Models with a Scene-Aware Long-Video Benchmark |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.27259) · [HuggingFace](https://huggingface.co/datasets/SinerChen/SceneBench) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Scene-RAG |
| Dataset | SceneBench, Video-MME |

> [!tip] 效果简介
> - SceneBench 上，平均任务准确率增益（6任务） 无RAG基线 +1.40%（Scene-RAG平均增益） vs 无RAG基线（LongVA, Long-LLaVA, LLaVA-OneVision-7B各自基线） (+1.40%)。
> - Video-MME 上，平均准确率增益（Overall） 无RAG基线 +10.47（Scene-RAG平均增益） vs 无RAG基线 (+10.47)。

## 概要

现有视觉语言模型（MLLMs）在长视频理解中面临一个根本性瓶颈：**长程上下文遗忘**。随着视频时长增加，模型难以有效聚合跨场景的语义信息来完成复杂推理任务。现有基准主要关注片段级（clip-level）理解，忽视了场景级（scene-level）推理对长程记忆与多模态证据整合的核心需求。

本文的核心洞察在于：**将视频组织为语义连贯的场景片段，并通过检索增强生成（RAG）机制按需提供相关场景记忆，可显著缓解长程遗忘**。基于此，作者提出**SceneBench**——首个系统评估长视频场景级理解的基准，包含2,485个视频（平均约1,978秒）和8,903个问答对，涵盖6种挑战性任务；同时提出**Scene-RAG**方法，以场景为单位构建动态多模态记忆库，并通过查询分解与检索实现场景级推理增强。

关键实证发现包括：

- **遗忘现象的量化验证**：随着问题与答案之间的时间距离增加，模型准确率显著下降（Figure 1），场景级任务（SceneQA）较片段级任务（ClipQA）在开源MLLMs上平均准确率下降**25.62个百分点**（相对降幅49.5%）（Table 2）。
- **Scene-RAG的有效性**：在SceneBench上，Scene-RAG为三个基线模型带来平均**+1.40%**的绝对提升（Table 3）；在通用长视频基准Video-MME上，相比无RAG基线平均提升**10.47点**，显著优于基于帧级检索的Video-RAG方法（Table 4）。
- **消融验证**：视觉编码、音频描述与场景分块三个组件对性能均有正向贡献，移除任一组分均导致准确率下降（Table 5）。

Scene-RAG的局限性在于引入额外离线预处理开销（46分钟视频约需277秒），且长程遗忘问题尚未完全解决——在开源模型上的提升绝对值仍较小。该方法在更长视频（数小时级）上的扩展性以及与长上下文模型集成的潜力，仍有待进一步探索。

### 长视频理解的层次性困境

视频理解任务天然存在信息粒度的层次结构。如图2所示，视频信息可划分为帧、片段、场景和视频四个层级：帧级信息聚焦单帧内的主体细节，片段级信息引入时序但仅能描述对象的客观行为，场景级信息整合大量片段内容形成完整的叙事事件，而视频级信息则由因果逻辑串联多个相关场景构成完整的故事线。现有长视频理解基准和模型主要围绕帧级或片段级推理展开，忽视了场景级理解这一关键中间层。

### 长程上下文遗忘：核心瓶颈

当前视觉语言模型（Vision-Language Models, VLMs）在长视频理解中面临一个根本性瓶颈：**长程上下文遗忘**。模型难以在跨越数分钟的视频内容中有效聚合分散的语义线索，导致复杂推理能力随信息跨度增大而急剧退化。Figure 1 直观地揭示了这一现象——随着问题与答案之间的时间距离增加，模型准确率持续下降。这暴露了现有模型在长程依赖建模上的结构性缺陷：它们缺乏以场景为单位的动态记忆构建与检索能力，无法将跨时间段的视觉与音频证据整合为连贯的推理链条。

### 现有基准的缺口

主流长视频理解基准（如Video-MME、MLVU等）在任务设计上存在明显局限：其问答对多聚焦于短时片段内的局部信息提取，未能系统性地评估模型对场景级语义的整合能力。SceneBench的统计对比（Table 1）显示，该基准包含2,485个视频（平均时长1,978秒）和8,903个问答对，覆盖6种挑战类型，其SceneQA任务中问答间的平均时间跨度达262秒（标准差310秒），远超现有基准的时空粒度。这使得SceneBench成为首个系统评估长视频场景级理解的基准。

### 动机：从帧级检索到场景级记忆

现有检索增强生成（RAG）方法在视频理解中的应用——如Video-RAG——基于帧级相似度检索，虽能改善短程和长程推理，但在中程距离上表现挣扎（Figure 1）。其根本原因在于：帧级检索割裂了视频的语义连贯性，无法捕获场景内的事件完整性。这一观察驱动了本文的核心动机：**将视频组织为语义连贯的场景片段，构建以场景为粒度的多模态记忆库，并通过查询驱动的动态检索机制按需提供相关上下文**，从而系统性缓解长程遗忘问题。

## 核心方法与创新机理

### 问题洞察：从帧级理解到场景级遗忘

现有视觉语言模型（VLLMs）在长视频理解中普遍采用均匀帧采样或固定时长片段分割策略，将视频视为时间维度上等间距的帧序列。这种帧级范式存在根本性缺陷：**均匀采样无法捕捉视频内在的语义结构，导致模型在需要跨长时间跨度聚合证据时发生严重的上下文遗忘**。

SceneBench的评估结果定量揭示了这一瓶颈：当问题与答案所需证据之间的时间距离增加时，模型准确率呈显著下降趋势（Figure 1）。更关键的是，场景级任务（SceneQA）相较于片段级任务（ClipQA），开源MLLMs的平均准确率骤降25.62个百分点，降幅达49.5%（Table 2）。这表明，**模型在需要整合跨场景语义信息以完成复杂推理时，其长程记忆能力面临严峻考验**。

### 方法创新：以场景为单位的检索增强记忆

针对上述瓶颈，Scene-RAG提出了三个关键的设计转变（changed slots），构成其核心创新：

#### 1. 视频分割方式：从均匀采样到场景分块（Scene Tiling）

传统方法将视频切分为等长的均匀片段，忽略了视频天然的叙事结构。Scene-RAG采用基于Total Variation L1正则化的场景分块方法，通过最小化以下目标函数对帧间相似度序列进行去噪：

$$\operatorname*{min}_{x \in \mathbb{R}^{n}} \frac{1}{2}\sum_{t=1}^{n}(x_t - s_t)^2 + \lambda\sum_{t=2}^{n}|x_t - x_{t-1}|$$

其中 $s_t$ 为相邻帧的原始相似度序列，$\lambda$ 控制分段常数近似的光滑程度。去噪后得到的平台（plateaus）对应语义连贯的场景段，再通过统计阈值 $k = \mu_x + \alpha\sigma_x$ 提取显著场景段（$\alpha=1.5$，最小段长 $L_{\min}=3s$）。这一设计使视频被组织为具有叙事意义的场景单元，而非机械的时间片段。

#### 2. 记忆构建：从无显式记忆到多模态场景记忆库

传统基线方法（如LongVA、Long-LLaVA）对视频进行端到端处理，缺乏显式的可检索记忆结构。Scene-RAG为每个检测到的场景构建多模态记忆表征：使用InternVideo2编码视觉特征，同时利用Qwen-Audio2对音频轨道进行转录和描述生成，形成对齐的视觉-音频场景记忆库。这种设计使模型能够按需检索特定场景的语义内容，而非依赖单一前向传播中有限的长程注意力。

#### 3. 检索机制：从无检索到查询分解驱动的场景级检索

与现有帧级检索方法（如Video-RAG）不同，Scene-RAG利用Qwen3 14B将用户查询分解为细粒度文本线索，在场景记忆库中进行语义相似度检索，返回Top-K（K=10）相关场景。检索结果与原始查询融合后输入MLLM生成回答。Figure 4对比了Scene-RAG与传统视频RAG的架构差异，核心在于**检索粒度从帧级提升到场景级**，使模型能够获取语义完整的上下文片段。

### 创新效果验证

Scene-RAG的创新设计在两类任务上得到验证：

- **SceneBench场景级任务**：Scene-RAG在三个基线模型（LongVA、Long-LLaVA、LLaVA-OneVision-7B）上平均带来+1.40%的绝对提升（Table 3），尤其在SceneQA-Audio任务上增益达+2.73。
- **通用长视频理解（Video-MME）**：Scene-RAG相比无RAG基线平均提升10.47个百分点（Table 4），显著优于帧级检索的Video-RAG方法。

消融实验（Table 5）进一步证实，视觉编码、音频描述与场景分块三个组件对性能均有正向贡献，移除任一组分均导致准确率下降（完整模型54.4 vs 无组件53.3）。

### 局限性

尽管Scene-RAG在场景级推理上取得进展，其创新仍存在边界：在开源模型上的提升绝对值较小（SceneBench约1.4%），长程遗忘问题并未完全解决。此外，场景分块引入的离线预处理开销（46分钟视频约需277秒）限制了实时应用场景的适用性。

Scene-RAG 的核心设计理念是将长视频组织为语义连贯的**场景**（scene）单元，而非均匀的帧或片段序列，并围绕这些场景构建可检索的外部记忆，以缓解现有视觉语言模型（MLLM）在长程上下文推理中的遗忘问题。整个框架由三个串行阶段构成，形成一条从视频预处理到答案生成的完整流水线。

**阶段一：场景分块（Scene Tiling）。** 输入一段长视频，Scene-RAG 首先不依赖固定时长切割，而是通过 Total Variation L1 正则化对相邻帧的视觉相似度序列进行去噪，产生分段常数近似，其平台区域对应语义连贯的场景段。具体而言，给定帧间相似度序列 $s_t$，求解如下优化问题：

$$\operatorname*{min}_{x \in \mathbb{R}^n} \frac{1}{2} \sum_{t=1}^{n} (x_t - s_t)^2 + \lambda \sum_{t=2}^{n} |x_t - x_{t-1}|$$

其中 $\lambda$ 控制去噪强度（实验中取 $\lambda = 1.5$）。去噪后的序列 $x_t$ 通过统计阈值 $k = \mu_x + \alpha \sigma_x$ 提取显著平台，并过滤掉短于最小段长 $L_{\min} = 3s$ 的片段，最终输出一组语义完整的场景段。这一过程将原始视频从“帧/片段”的物理粒度提升到“场景”的叙事粒度，为后续记忆构建提供了有意义的组织单元。

**阶段二：多模态记忆构建（Multimodal Memory Construction）。** 对每个场景段，Scene-RAG 并行编码视觉与音频信息。视觉方面，使用 **InternVideo2** 对场景段提取视觉嵌入；音频方面，通过 **Qwen-Audio2** 对音轨进行转录与描述生成，获得结构化的音频文本表示。二者对齐后构成该场景的多模态记忆条目，存入可检索的外部记忆库。

**阶段三：查询检索（Query Retrieval）。** 当用户提出问题时，Scene-RAG 首先利用 **Qwen3 14B** 将查询分解为一组细粒度的文本线索，然后在记忆库中执行场景级相似度检索，返回 Top-K（实验中 $K = 10$）最相关的场景上下文。这些检索到的场景记忆被融合后，与原始查询一起送入下游 MLLM 进行推理与答案生成。

三个阶段的输入输出关系可以概括为：**原始视频 → Scene Tiling → 场景段集合 → Memory Construction → 多模态记忆库 → Query Retrieval → Top-K 相关场景 → MLLM 推理 → 最终答案**。这一流水线的关键优势在于，它将长视频的全局信息压缩为按需检索的场景记忆，使模型无需在单次前向传播中处理整个视频的上下文，从而显著缓解长程遗忘（见 Figure 4 的架构对比示意）。

![[assets/figures/papers/paper_list_l826_https_arxiv_org_abs_2603_27259/figures/005_Figure_4.jpg]]
*Figure 4: Comparison of Scene-RAG with traditional RAGs working on video understanding tasks. Scene-RAG first aggregates long-range visual scenes via scene tiling, stores aligned visual–audio evidence, and retrieves task-relevant segments conditioned on user queries*

值得注意的是，Scene-RAG 是一个**模型无关**的检索增强框架，可与不同的骨干 MLLM（如 LongVA、Long-LLaVA、LLaVA-OneVision-7B）配合使用，仅通过替换记忆构建与检索模块即可适配。

Scene-RAG 的核心设计动机源于一个关键观察：现有视觉语言模型在长视频理解中面临严重的长程上下文遗忘，难以有效聚合跨场景的语义信息以完成复杂推理。其因果调节变量在于模型是否具备以场景为单位的动态记忆构建与检索能力。基于此，Scene-RAG 将视频组织为语义连贯的场景片段，并通过检索增强生成机制按需提供相关场景记忆，从而缓解长程遗忘。

Scene-RAG 由三个串联的阶段构成：**Scene Tiling**（场景分块）、**Multimodal Memory Construction**（多模态记忆构建）和**Query Retrieval**（查询检索）。其与传统视频 RAG 方法的核心区别在于，记忆的组织单元从均匀帧采样或固定时长片段转变为语义连贯的场景段（Figure 4）。

### Scene Tiling：基于 TV-L1 的场景边界检测

Scene Tiling 模块负责将长视频自动分割为语义连贯的场景段，替代传统的均匀帧采样策略。其核心是一个基于总变分 L1 正则化（TV-L1）的去噪优化过程。

给定视频相邻帧的视觉相似度序列 $s_t$（$t=1,\dots,n$），Scene Tiling 通过求解以下 TV-L1 最小化问题获得分段常数近似 $x_t$：

$$\operatorname*{min}_{x \in \mathbb{R}^{n}} \; \frac{1}{2} \sum_{t=1}^{n} (x_t - s_t)^2 + \lambda \sum_{t=2}^{n} |x_t - x_{t-1}|$$

其中：
- $s_t$ 为原始帧间相似度序列，反映相邻帧的视觉连续性；
- $x_t$ 为去噪后的分段常数序列，其平坦区域（plateau）对应语义连贯的场景段；
- $\lambda$ 为正则化系数，控制去噪平滑程度与分段数之间的权衡（实验设定 $\lambda = 1.5$）；
- 第一项 $\frac{1}{2}\sum (x_t - s_t)^2$ 为保真项，约束 $x_t$ 不偏离原始信号过远；第二项 $\lambda\sum |x_t - x_{t-1}|$ 为 L1 总变分惩罚项，鼓励 $x_t$ 呈现分段常数结构。

在获得去噪序列 $x_t$ 后，Scene Tiling 使用统计阈值从平坦区域中提取显著场景段：

$$k = \mu_x + \alpha \sigma_x$$

其中 $\mu_x$ 和 $\sigma_x$ 分别为 $x_t$ 的均值和标准差，$\alpha$ 为灵敏度参数（实验设定 $\alpha=1.5$）。高于阈值 $k$ 的连续高激活区域被识别为场景段，同时过滤掉长度小于 $L_{\min}=3\text{s}$ 的短片段以抑制噪声碎片。

### Multimodal Memory Construction：多模态场景记忆编码

记忆构建阶段为每个检测到的场景段生成可检索的多模态表示：
- **视觉编码**：使用 InternVideo2 对场景段进行视觉特征编码，生成场景级视觉嵌入；
- **音频编码**：使用 Qwen-Audio2 对音频轨道进行转录和描述生成，形成文本形式的音频语义表示；
- **记忆存储**：将视觉嵌入与音频描述对齐后存入场景记忆库，作为后续检索的索引单元。

这种以场景为粒度的记忆组织方式，使得每个记忆单元天然封装了完整的叙事片段，而非孤立的帧级信息。

### Query Retrieval：查询分解与场景检索

在推理阶段，Query Retrieval 模块负责将用户查询与记忆库中的场景进行匹配：
1. **查询分解**：使用 Qwen3 14B 将原始查询分解为细粒度的文本线索（fine-grained textual clues）；
2. **场景检索**：基于分解后的线索，在场景记忆库中进行相似度检索，返回 Top-K 个最相关的场景段（实验设定 $K=10$）；
3. **上下文融合**：将检索到的场景上下文与原始查询拼接，送入下游 MLLM 进行答案生成。

### 模块消融验证

消融实验（Table 5）证实了三个组件的独立贡献：在 SceneBench 上，完整 Scene-RAG 得分 54.4，移除任一组件后性能均有下降（无组件基线 53.3）。超参数分析（Table 8）进一步表明，降低场景检测灵敏度 $\alpha$ 至 0.5 会导致 VideoMME 性能下降 1.2，过短的 $L_{\min}=2\text{s}$ 也会轻微降低性能（下降 0.5），验证了场景分块粒度对整体效果的关键影响。

## 实验与关键发现

### 核心实验设置

SceneBench 包含 2,485 个视频（平均时长 1,978 秒）和 8,903 个问答对，覆盖 6 种任务类型。所有评估模型均采用其官方推荐的最佳帧数和分辨率配置。Scene-RAG 的超参数基于验证集选择：TV-L1 正则化系数 $\lambda = 1.5$，最小场景段长 $L_{\min} = 3\text{s}$，检索返回 Top-K 场景数 $K = 10$，统计阈值系数 $\alpha = 1.5$。视频检索器基于 InternVideo2，查询分解使用 Qwen3 14B。

### 主实验结果

**场景级理解的长程遗忘现象。** 在 SceneBench 上对 19 个 MLLM（16 个开源、3 个商业）的全面评估揭示了显著的长程遗忘：场景级任务 SceneQA 相比片段级任务 ClipQA，开源模型平均准确率下降 25.62 点（相对降幅 49.5%）。这一结果直接量化了现有模型在跨场景语义聚合上的瓶颈。同时，SceneQA-Audio 相比 SceneQA 平均高出 2.97 点，表明音频信息对场景理解具有补充价值，但远未弥补场景级推理的性能缺口。

**Scene-RAG 的场景级增益。** Scene-RAG 在三个基线模型（LongVA、Long-LLaVA、LLaVA-OneVision-7B）上均带来一致的性能提升，SceneBench 六任务平均绝对增益约 +1.40%（Table 3）。分任务来看，Scene-RAG 在 Comment Prediction（+1.97）、SceneQA-Audio（+2.73）和 SceneQA（+1.30）上提升最为显著，这些任务恰好对跨场景时序推理要求最高。相比帧级检索方法 Video-RAG，Scene-RAG 在 SceneQA 和 SceneQA-Audio 上分别额外提升 +1.20 和 +2.60，验证了以场景为单位的记忆组织优于均匀帧检索。

**跨基准泛化能力。** 在通用长视频理解基准 Video-MME 上，Scene-RAG 相比无 RAG 基线平均提升 10.47 点（Table 4），其中 LongVA 提升 11.0 点，Long-LLaVA 提升 11.8 点，LLaVA-OneVision-7B 提升 8.6 点。该结果表明场景级检索增强并非仅在 SceneBench 上有效，而是具有跨基准的泛化价值。

**时间距离与遗忘曲线。** Figure 1 揭示了准确率随 SceneQA 问题与答案时间距离增加的单调下降趋势。Video-RAG 在短距离和长距离设置下改善基线，但在中等距离上表现挣扎；Scene-RAG 在中长距离上保持较高准确率，缓解了遗忘曲线的陡降斜率。这一发现直接支撑了核心洞见：场景级记忆检索能有效桥接中等时间跨度的语义断裂。

### 消融实验

**组件贡献分析。** Table 5 的消融实验表明，视觉编码、音频描述与场景分块三个组件对 SceneBench 性能均有正向贡献。完整模型得分 54.4，移除任一组分后降至 53.3，验证了多模态场景记忆的必要性。在 MLVU 基准上，完整模型同样优于各消融变体，进一步确认各组件的互补性。

**超参数敏感性。** Table 8 在 Video-MME 上对 SceneTiling 和检索大小进行消融：降低场景检测灵敏度 $\alpha$ 至 0.5 导致性能下降 1.2 点，过短的最小段长 $L_{\min}=2\text{s}$ 轻微降低 0.5 点，最优 $K=10$。这表明场景分块的粒度对下游推理有实质影响——过于宽松的检测会引入噪声场景，过于严格的检测则遗漏关键上下文。

**帧数对模态任务的影响。** Figure 5 分析了输入帧数（16/32/64/128）对 SceneQA 和 SceneQA-Audio 的影响。SceneQA 随帧数增加略有改善，但 SceneQA-Audio 在 32 帧时性能达到峰值，更长序列反而轻微下降。这一现象暗示音频相关推理对视觉帧的冗余信息更敏感，可能源于音频描述与视觉线索在长序列中的对齐退化。

### 失败模式与局限性

**开源模型上的绝对增益有限。** Scene-RAG 在 SceneBench 上的平均绝对提升仅约 1.4%，长程遗忘问题远未完全解决。这表明检索增强虽能缓解但无法根治 MLLM 的上下文遗忘，更深层的架构改进仍是必需的。

**离线预处理开销。** Table 7 展示了 Scene-RAG 对一段 2,767 秒视频的运行时分解：离线预处理（场景分块、记忆构建）耗时约 277 秒，不适合实时或低延迟应用场景。该开销主要来自 InternVideo2 编码和 Qwen-Audio2 音频描述生成。

**数据覆盖的局限。** SceneBench 目前仅包含英语视频，类型限于电影、vlog、纪录片等，且因视觉和语义歧义，部分场景在人工标注中被放弃（每个 QA 对耗时约 36 分钟）。这些因素可能限制基准在非英语或更广泛视频类型上的代表性。

### 重要图表结论

- **Table 1**：SceneBench 在视频数量、类型多样性和场景级标注密度上区别于现有长视频基准，SceneQA 的平均时间跨度为 262 秒（标准差 310 秒），体现了广泛的时间多样性。
- **Table 2**：19 个 MLLM 在六任务上的完整结果，场景级任务（SceneQA、SceneQA-Audio、Title Prediction）普遍低于片段级任务（ClipQA、Comment Prediction），商业模型在场景级任务上同样出现显著退化。
- **Table 6**：SceneQA 和 SceneQA-Audio 样本在不同时间跨度区间的分布，大部分样本集中在 100–500 秒区间，验证了基准对中等时间跨度推理的侧重。

![[assets/figures/papers/paper_list_l826_https_arxiv_org_abs_2603_27259/figures/003_Table_1.jpg]]
*Table 1: Comparison of SceneBench with existing long-video understanding benchmarks. SceneBench offers a balanced number of videos, diverse genres, and high–time-range, scene-based QA annotations. The average temporal distance between each question and its corresponding answer in SceneQA is 262s, with a standard deviation of 310s, illustrating the wide temporal diversity of the dataset. “†” denotes automatically or partially automatically generated QA pairs*

![[assets/figures/papers/paper_list_l826_https_arxiv_org_abs_2603_27259/figures/006_Table_2.jpg]]
*Table 2: Benchmark results on the SceneBench. “Frame Count” indicates the number of frames used as input. Comm.: Comment*

![[assets/figures/papers/paper_list_l826_https_arxiv_org_abs_2603_27259/figures/007_Table_3.jpg]]
*Table 3: Performance of different MLLMs on the SceneBench benchmark. The average improvement of Scene-RAG is ∼1.40% in average*

![[assets/figures/papers/paper_list_l826_https_arxiv_org_abs_2603_27259/figures/014_Table_8.jpg]]
*Table 8: Ablation over SceneTiling*

![[assets/figures/papers/paper_list_l826_https_arxiv_org_abs_2603_27259/figures/004_Figure_3.jpg]]
*Figure 3: Statistical overview of our SceneBench benchmark. (A) Distribution of scene lengths. (B) Distribution of task counts. (C) Distribution of SceneQA and SceneQA-Audio length duration proportion over the full video*

## 定位与知识库关联

### 方法谱系：从帧级检索到场景级记忆增强

Scene-RAG 的核心贡献在于将视频理解中的检索增强生成（RAG）从**帧级/片段级**提升到**场景级**，其方法谱系可沿两条主线追溯：视频 RAG 范式的演进，以及视频结构化表示的分层思想。

**视频 RAG 的基线锚点。** 传统的视频 RAG 方法（如 **Video-RAG**）将视频均匀分割为固定时长片段，对每个片段独立编码后构建记忆库，查询时通过帧级或片段级相似度检索相关上下文。这一范式的根本局限在于：均匀分割破坏了视频的语义连贯性，导致检索到的片段可能缺乏完整的叙事上下文。Scene-RAG 直接针对这一瓶颈，将记忆组织的基本单元从“均匀片段”替换为“语义场景”——通过 TV-L1 正则化自动检测的、视觉与音频叙事连贯的连续时间段（Figure 4）。这一设计使检索结果天然携带完整的因果与情节信息，而非孤立的视觉快照。

**视频分层理解的认知基础。** Scene-RAG 的场景级设计建立在对视频信息层次的明确认知之上：帧级信息描述主体细节，片段级信息包含时序但仅能刻画客观行为，场景级信息整合大量片段级内容并形成完整的事件单元，而视频级信息则由因果关联的场景构成逻辑故事线（Figure 2）。这一分层框架为 SceneBench 的任务设计提供了理论依据——SceneQA 任务的线索被刻意设计为跨越至少两分钟，迫使模型进行跨场景推理。

**与现有 MLLM 的关系。** Scene-RAG 并非替代现有 MLLM，而是作为**即插即用的外部记忆增强模块**叠加于骨干模型之上。论文在三个开源骨干模型上验证了这一设计：**LongVA**、**Long-LLaVA** 和 **LLaVA-OneVision-7B**。这些模型本身已具备长视频处理能力（通过高帧数输入或长上下文窗口），但 Scene-RAG 仍能在其上带来一致的增益（SceneBench 平均 +1.40%，Video-MME 平均 +10.47 点），表明**外部场景记忆与模型内部长上下文能力是互补而非冗余的**。

### 知识库定位：场景感知长视频理解基准的空白填补

SceneBench 在长视频理解基准谱系中占据独特位置。Table 1 的系统对比揭示了其差异化定位：现有基准（如 Video-MME、MLVU、LongVideoBench）虽然覆盖长视频，但 QA 标注并非以场景为粒度组织——它们要么依赖自动生成（如 EgoSchema、CinePile），要么缺乏对问题-答案时间跨度的系统控制。SceneBench 的独特贡献在于：

- **全手工标注**：每个 QA 对耗时约 36 分钟，经过多轮验证，确保问题确实需要跨场景推理；
- **时间跨度可控**：SceneQA 的平均时间距离为 262 秒（标准差 310 秒），覆盖从短程到长程的广泛分布（Table 6）；
- **多任务覆盖**：6 类任务（Title Prediction、Comment Prediction、ClipQA、SceneQA、SceneQA-Audio、I-VQA）从不同角度探测场景级理解能力。

这一设计使得 SceneBench 成为**首个系统性评估场景级长视频理解的基准**，填补了帧级/片段级评估与视频级整体理解之间的粒度空白。

### 适用边界与局限

**计算开销与实时性约束。** Scene-RAG 的离线预处理阶段引入了不可忽视的计算成本：对一个 2,767 秒（约 46 分钟）的视频，场景分块、视觉编码和音频描述的总预处理时间约 277 秒（Table 7）。这使得 Scene-RAG 不适合需要即时响应的实时应用场景（如直播理解），其适用边界更偏向**离线分析、视频归档检索和异步问答**场景。

**性能增益的量级与上限。** 尽管 Scene-RAG 在统计上显著且一致地提升性能，但在 SceneBench 上的绝对增益（约 +1.40%）仍然较小。这表明**场景级检索增强缓解了但远未解决长程遗忘问题**——模型在处理跨场景推理时仍存在根本性的信息整合困难。在 Video-MME 上的更大增益（+10.47 点）暗示 Scene-RAG 在通用长视频理解任务上可能更具优势，但这一差异也可能部分源于 Video-MME 与 SceneBench 在任务设计上的不同侧重。

**数据多样性的局限。** SceneBench 目前仅包含英语视频，类型限于电影、vlog、纪录片等，且由于视觉和语义歧义，部分场景在标注过程中被放弃。这限制了基准对多语言、多文化长视频场景的代表性。此外，Scene-RAG 的超参数（λ=1.5, L_min=3s, topK=10 等）基于验证集选择，但未对所有可能配置进行穷举搜索，其最优性在不同视频类型上的泛化能力有待进一步验证。

### 开放问题

1. **更长视频的扩展性**：Scene-RAG 在数十分钟视频上验证有效，但在数小时乃至更长的视频（如完整电影、监控录像）上，场景记忆库的规模增长可能导致检索精度下降和推理延迟增加。场景分块的层次化索引或记忆压缩策略是可能的扩展方向。

2. **多模态嵌入对齐的细节缺失**：论文未详细说明视觉嵌入（InternVideo2）与音频描述嵌入（Qwen-Audio2）在记忆库中的对齐方式——是简单拼接、加权融合还是跨模态注意力？这一设计选择可能显著影响检索质量，但完整实现细节和伪代码尚未公开。

3. **场景分块的精确过滤参数**：Scene Tiling 中用于过滤短段的精确 ε 参数未明确给出，这影响方法的可复现性和在不同视频风格上的调优策略。

4. **与长上下文模型的深度集成**：当前 Scene-RAG 以外部记忆形式叠加于骨干模型，未来是否可以将场景级记忆直接融入模型的长上下文窗口或训练目标中，实现更紧耦合的场景感知推理，仍是一个开放的研究问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/Seeing_the_Scene_Matters_Revealing_Forgetting_in_Video_Understanding_Models_with_a_Scene_Aware_Long_Video_Benchmark.pdf]]
