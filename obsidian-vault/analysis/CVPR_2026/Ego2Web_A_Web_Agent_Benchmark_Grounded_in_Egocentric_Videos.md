---
title: "Ego2Web: A Web Agent Benchmark Grounded in Egocentric Videos"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Ego2Web_A_Web_Agent_Benchmark_Grounded_in_Egocentric_Videos.pdf
project_link: null
code_link: "https://github.com/tatsu-lab/alpaca\\_"
aliases:
- EBEE
- Ego2Web
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 对第一人称视频的密集视觉理解（包括精细时空线索和物体细节）是完成任务的核心驱动因素；移除视频输入或仅依赖文本描述会导致性能急剧下降。
primary_logic: 首次将第一人称视频感知与在线Web任务执行相结合，构建连接物理世界与数字世界的基准，同时提出Ego2WebJudge自动评估框架，通过整合视频证据可靠衡量智能体的跨模态能力。
claims:
- Ego2WebJudge achieves approximately 84% agreement with human judgment, significantly outperforming previous automatic evaluation methods.
- All state-of-the-art agents leave a clear room (about 40% gap) from the oracle performance.
- Raw video input provides a substantial boost over text-only captions (48.2% vs 23.6% SR).
- Ego2Web human evaluation 上 Success Rate (SR) = 58.6% (BU-Gemini-3-Flash)
---

# Ego2Web: A Web Agent Benchmark Grounded in Egocentric Videos

> [!tip] 核心洞察
> 首次将第一人称视频感知与在线Web任务执行相结合，构建连接物理世界与数字世界的基准，同时提出Ego2WebJudge自动评估框架，通过整合视频证据可靠衡量智能体的跨模态能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | Ego2Web：基于第一人称视角视频的Web智能体基准测试 |
| 英文题名 | Ego2Web: A Web Agent Benchmark Grounded in Egocentric Videos |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.22529) · [Code](https://github.com/tatsu-lab/alpaca\_) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Ego2Web (benchmark) and Ego2WebJudge (evaluator) |
| Dataset | Ego2Web human evaluation, Evaluation agreement, Ablation on visual modality |

> [!tip] 效果简介
> - Ego2Web human evaluation 上，Success Rate (SR) 58.6% (BU-Gemini-3-Flash) vs 26.4% (Claude 3.7), 44.4% (BU-GPT-4.1) (~32.2% over weakest agent)。
> - Evaluation agreement (Judge vs Human) 上，Agreement Rate (AR) 84.0% (Ego2WebJudge w/ GPT-4o) vs 74.7% (WebVoyager), 78.4% (WebJudge) (+5.6% over WebJudge)。
> - Ablation on visual modality 上，Success Rate (SR) 48.2% (raw video, BU-Gemini-3-Flash) vs 23.6% (detailed caption only), 4.4% (no visual) (+24.6% over caption)。

## 概要

当前Web智能体（Web Agent）基准测试普遍依赖网页截图或文本指令，缺乏对真实物理世界的视觉感知能力。这一缺口导致智能体无法利用用户在现实场景中获取的第一人称视觉信息来指导在线操作，例如根据视频中看到的商品在电商网站上进行搜索与购买。**Ego2Web** 首次将第一人称（egocentric）视频感知与在线Web任务执行相结合，构建了一个连接物理世界与数字世界的基准测试平台。

该基准的核心洞察在于：对第一人称视频的密集视觉理解——包括精细的时空线索和物体细节——是完成任务的关键驱动因素。实验表明，移除视频输入或仅依赖文本描述会导致性能急剧下降（成功率从原始视频输入的48.2%降至纯文本描述的23.6%，无视觉输入时仅为4.4%）。这一发现揭示了视觉理解与数字行动之间的因果瓶颈。

为支持该基准的自动化评估，研究者同时提出了 **Ego2WebJudge**，一个融合视频证据与网页截图的多模态LLM-as-a-Judge框架。该框架与人类判断的一致性达到约84%，显著优于现有自动评估方法（如WebVoyager的74.7%和WebJudge的78.4%），为跨模态智能体的可靠自动评估提供了可行方案。

在方法谱系上，Ego2Web区别于纯视频推理数据集（如EgoThink、EgoSchema）和仅关注网页截图感知的Web智能体基准（如WebVoyager、VisualWebArena），首次将真实世界第一人称视觉感知与可执行的在线Web任务统一在一个无约束的在线评估设定下。数据构建采用半自动流水线：由MLLM（Qwen3-VL）生成结构化视频描述，LLM（GPT-5）自动合成任务指令，再由人工进行视觉依据、Web可行性和指令质量的三方核验。

主要实验结果显示，当前最先进的Web智能体在Ego2Web上表现最佳的为**Browser Use with Gemini-3-Flash**（成功率58.6%），与理论最优性能（oracle）之间仍存在约40%的显著差距。这一结果表明，第一人称视觉感知驱动的Web操作仍是一个极具挑战性的开放问题，现有智能体在物体误识别和时间顺序理解方面存在突出短板。



### 第一人称视觉理解与Web操作的脱节

随着多模态大语言模型（MLLM）和Web智能体的快速发展，AI系统在数字环境中的自主操作能力取得了显著进步。以**WebVoyager**（He et al., 2024）和**VisualWebArena**（Koh et al., 2024）为代表的基准测试，已经能够评估智能体基于网页截图执行在线任务的能力。与此同时，以**EgoSchema**（Mangalam et al., 2023）和**EgoThink**（Cheng et al., 2024）为代表的视频推理数据集，则专注于评估模型对第一人称视频的纯视觉理解能力。

然而，这两条研究脉络之间存在一个关键缺口：**现有基准无法将第一人称视觉感知与在线Web操作相连接**。在真实场景中，用户常常需要根据亲眼所见的物理世界信息——例如某款产品的品牌名称、某个地标的外观特征、或视频中第三个出现的物品——在Web上完成搜索、比价、预订等后续操作。当前的Web智能体基准仅依赖网页截图作为视觉输入，完全缺失了真实世界视觉感知这一前置环节；而视频推理数据集则止步于问答，不涉及任何可执行的在线交互。**Table 1** 系统性地展示了这一空白：Ego2Web是首个同时要求第一人称视频感知和真实在线Web操作执行的基准。

### 视觉输入模态的关键瓶颈

这一缺口的实际影响远超基准设计的范畴，它直接制约了当前最先进Web智能体的能力边界。当任务需要从物理世界中提取精细的时空视觉线索时——例如识别视频中“第四个被拿起的零食”或“中间位置出现的黑色背包”——仅依赖文本指令或网页截图的智能体将完全无法获取这些前置信息。**Figure 1** 直观地展示了这一挑战：智能体必须首先在视频中进行时空定位以识别相关视觉线索，然后基于这些线索执行对应的Web操作。

该论文的消融实验（**Table 5**）为这一瓶颈提供了决定性的量化证据：当使用原始视频作为输入时，智能体的成功率达到48.2%；若仅提供由MLLM生成的详细文本描述，成功率骤降至23.6%；而完全移除视觉信号后，成功率仅为4.4%。这表明**精细的时空视觉细节（如物体的精确外观、动作的时间顺序）无法通过文本描述有效传递**，构成了当前视觉-文本融合流水线的重大瓶颈。

### 评估方法的不足

与任务设计缺口相伴的是评估方法的局限。现有Web智能体基准的自动评估方法，如**WebVoyager**使用的文本轨迹比对和**WebJudge**（Xue et al., 2025）的多模态LLM-as-a-Judge，在判断任务完成时仅依赖网页截图和动作历史，缺乏对真实世界视觉证据的核验能力。当任务要求验证“网页上找到的产品是否与视频中看到的物品一致”时，这些方法无法获取视频中的视觉证据，因而难以做出准确判断。

### 本文动机

基于上述分析，本文的核心动机可归纳为三个层面：

1. **填补基准空白**：构建首个将第一人称视频感知与在线Web任务执行相结合的基准，连接物理世界视觉理解与数字世界行动能力。
2. **量化能力鸿沟**：通过系统评估揭示当前最先进Web智能体在真实世界视觉接地任务上的真实表现，为后续研究提供明确的改进方向。
3. **建立可靠评估**：设计能够整合视频证据的自动评估框架，在保证与人类判断高度一致（约84%一致率）的前提下，降低人工评估成本并提升可重复性。



## 核心方法与创新机理

Ego2Web 的核心创新在于将**第一人称视频感知**与**在线 Web 任务执行**首次系统性地结合，构建了一个连接物理世界与数字世界的基准测试。与现有工作相比，这一创新体现在三个关键维度的根本性改变上。

### 视觉感知依据：从网页截图到第一人称视频

现有 Web 智能体基准（如 **WebVoyager**、**VisualWebArena**）仅依赖网页截图或文本指令作为感知输入，智能体无需理解真实物理世界。Ego2Web 将感知依据彻底改变为**第一人称视频**（$V = \{ f_1, f_2, ..., f_t \}$），要求智能体从用户的真实视觉环境中提取关键信息——如识别视频中“第四个拿起的零食”或“中间位置的黑色背包”——再据此执行 Web 操作。这一改变使得任务从纯数字交互跨越到物理世界感知与数字行动的结合，形成了全新的跨模态智能体测试场景（见 Table 1 的系统性对比）。

### 评估方式：从轨迹文本匹配到多模态视频证据融合

现有自动评估方法（如 WebVoyager 的评估器、WebJudge）主要基于文本轨迹或最终响应的语义匹配来判断任务完成情况，无法验证智能体是否真正理解了视频中的视觉证据。Ego2Web 提出的 **Ego2WebJudge** 评估框架改变了这一范式：它通过三阶段流水线——关键要点识别（Key-Point Identification）、关键截图筛选（Key Screenshot Selection）和最终结果判定（Final Outcome Judgment）——将**视频证据片段**（$\nu$）、任务指令（$I$）、动作序列（$A$）和网页截图（$S$）进行联合推理，输出二元评估结果 $O = \text{Ego2WebJudge}(I, \nu, A, S)$。该框架通过显式建模视觉证据与动作一致性，将评估与人类判断的一致性率提升至约 **84%**，比 WebJudge 高出 5.6 个百分点（Table 4）。

### 数据生成：从纯人工标注到模型-人类协作流水线

传统基准的数据构建依赖大量人工标注，成本高昂且难以扩展。Ego2Web 设计了**半自动模型-人类协作流水线**：首先由 MLLM（Qwen3-VL）对视频片段生成密集的结构化描述，涵盖全局场景上下文和带时间戳的局部物体细节；随后由 LLM（GPT-5）根据视频概况和指定网站自动合成 Web 任务指令；最后由人工标注者从视觉依据、Web 可行性和指令质量三方面进行核验和修正。这一流水线在保证任务质量的同时大幅降低了构建成本，使得大规模、高质量的第一人称视频-Web 任务对成为可能。

### 创新效果的因果验证

消融实验（Table 5）揭示了上述创新的因果效应：当移除视频输入、仅提供文本描述时，智能体成功率从 **48.2%** 骤降至 **23.6%**；完全移除视觉信号后，成功率仅为 **4.4%**。这表明精细的时空视觉线索对于任务完成具有不可替代的驱动作用，也验证了 Ego2Web 所引入的第一人称视频感知维度构成了当前智能体的核心能力瓶颈。



Ego2Web构建了一个连接物理世界视觉感知与数字Web操作的完整流水线，其核心由**数据生成**、**智能体执行**与**自动评估**三个相互衔接的阶段组成。

### 任务定义与输入输出

基准的形式化定义建立在一组明确的数据结构之上。给定一段由 $t$ 个帧组成的第一人称视频 $V = \{ f_1, f_2, ..., f_t \}$ 和一条任务指令 $I$，智能体需要首先对视频进行时空定位，识别出与任务相关的视觉线索（例如视频中第四个被拿起的零食），随后在真实在线浏览器环境中执行一系列Web动作 $A = \{ a_1, a_2, ..., a_n \}$，最终生成任务响应。这一任务定义将Ego2Web与纯视频推理基准（如EgoThink、EgoSchema）和仅依赖网页截图的Web智能体基准（如WebVoyager、VisualWebArena）明确区分开来——前者只关注视觉理解，后者只关注在线交互，而Ego2Web首次将二者融合于非受控在线评估环境中（Table 1）。

### 数据生成流水线

Ego2Web采用**模型-人工协作的半自动流水线**来合成视觉锚定的Web任务，该流水线由三个模块串联构成（Figure 3左）：

1. **视频描述生成（Qwen3-VL）**：使用冻结的多模态大语言模型（MLLM）将视频片段转换为结构化密集描述。MLLM以片段为单位生成带时间戳的描述，同时涵盖全局场景语境和局部物体细节，形成视频元数据 $V_{\text{meta}} = \{ \nu_{\text{meta}}^1, \nu_{\text{meta}}^2, ..., \nu_{\text{meta}}^k \}$。

2. **任务指令合成（GPT-5）**：基于视频概况和指定的目标网站，利用大语言模型自动生成Web任务指令。这一步骤将视觉理解从MLLM转移到LLM的任务合成能力中，实现跨模态的任务构造。

3. **人工核验与修正**：人工标注者从三个维度对生成的任务进行质量把关——视觉依据的准确性（任务是否确实需要视频中的视觉信息）、Web可行性（任务能否在指定网站上执行），以及指令清晰度。这一环节确保了基准中每条任务都具备可靠的视觉锚定和可执行性。

最终构建的Ego2Web基准覆盖了电子商务、媒体检索、知识查询、本地/地图服务等多个任务领域，任务类型和网站域分布详见Figure 4。

### 智能体执行流程

在评估阶段，智能体同时接收第一人称视频和文本指令作为输入（Figure 2）。对于能够原生处理视频的智能体（如Browser Use搭配Gemini-3-Flash），视频以关键帧或原始视频流的形式直接输入底层MLLM；对于无法直接访问视频输入的智能体（如Claude系列和GPT-5.4），则统一使用Gemini-3.1-Pro生成的详细结构化文本描述作为视觉信息的代理。智能体在浏览器中执行一系列动作，同时记录动作历史、网页截图序列和最终响应，这些共同构成后续评估的完整轨迹。

![[assets/figures/papers/paper_list_l818_https_arxiv_org_abs_2603_22529/figures/002_Figure_2.jpg]]
*Figure 2: | The workflow overview for agent action and evaluation in real-world, egocentric video perception. The agent operates using both egocentric video and textual instructions, and outputs a series of web actions, screenshots and a final response to the task. To enable automatic evaluation in a live, unconstrained web environment, we further introduce a new LLM-as-a-Judge framework tailored for this real-world visually grounded web task. Our LLM-as-a-Judge framework takes the instruction, action history, screenshots, and a final response, and compares them with the annotated visual evidence (video clip) to assess whether the task is successfully completed*

### Ego2WebJudge自动评估框架

为解决在线、非受控Web环境中缺乏可靠自动评估方法的问题，本文提出了**Ego2WebJudge**——一个专为第一人称视频锚定的Web任务设计的多模态LLM-as-a-Judge框架（Figure 3右）。该框架在WebJudge（Xue et al., 2025）的基础上扩展，整合了来自第一人称视频的视觉证据信号。评估流程分为三个阶段：

1. **关键要点识别（Key-Point Identifier）**：从任务指令中提取任务完成所需的关键要点，作为后续判断的细粒度依据。

2. **关键截图筛选（Key Screenshot Selector）**：从智能体的完整网页截图序列中，筛选出与任务高度相关的截图子集，减少冗余信息对判断的干扰。

3. **最终结果判定（Final Judge）**：综合任务指令 $I$、标注的第一人称视觉证据片段 $\nu$、动作序列 $A$ 和关键截图 $S$，进行成功/失败的二元分类判定，即 $O = \text{Ego2WebJudge}(I, \nu, A, S)$。

该框架的核心优势在于**显式建模视觉证据与动作之间的一致性**，而非仅依赖文本轨迹或最终响应。实验表明，Ego2WebJudge与人类判断的一致性达到约84%（GPT-4o版本），显著优于WebVoyager（74.7%）和WebJudge（78.4%）等先前方法。这一改进主要源于其对第一人称视频中视觉信号的有效利用，减少了先前评估器常见的误判模式。

### 补充图表

![[assets/figures/papers/paper_list_l818_https_arxiv_org_abs_2603_22529/figures/001_Figure_1.jpg]]
*Figure 1: | In this paper, we propose Ego2Web, a new benchmark introducing a novel web-agent task grounded in users’ real-world visual surroundings. The tasks span diverse domains, like e-commerce, media retrieval, knowledge lookup, and local/maps services. Given an egocentric video and an instruction, the agent must first perform spatio-temporal grounding to identify the relevant visual cue (e.g., the fourth snack picked up in the video), and then execute corresponding web actions based on both the grounded visual evidence and the instruction*



### 任务形式化定义

Ego2Web将第一人称视频感知与在线Web任务执行形式化为一个跨模态智能体任务。给定一段由 $t$ 个帧组成的第一人称视频：

$$V = \{ f_1, f_2, ..., f_t \}$$

智能体需要在浏览器环境中执行一系列Web动作：

$$A = \{ a_1, a_2, ..., a_n \}$$

其中，$V$ 捕捉用户的第一人称视角物理环境，$A$ 表示智能体在真实在线网站上执行的 $n$ 个连续操作。智能体必须首先对视频进行时空定位（spatio-temporal grounding），识别与任务相关的视觉线索（如视频中第几个被拿起的物品），然后基于定位到的视觉证据和文本指令执行相应的Web操作。该任务的核心挑战在于：视觉理解发生在连续动态的第一人称视频中，而行动输出发生在离散的网页交互空间内，两者之间存在模态鸿沟。

### 半自动数据生成流水线

Ego2Web基准的构建依赖一条模型-人工协同的数据生成流水线，包含三个核心模块：

**模块1：视频结构化描述生成（Video Captioning）**
使用冻结的MLLM（如Qwen3-VL）将第一人称视频逐片段转换为密集的结构化描述。该模块生成 $k$ 个带时间戳的视频元数据条目：

$$V_{meta} = \{ \nu_{meta}^1, \nu_{meta}^2, ..., \nu_{meta}^k \}$$

每个 $\nu_{meta}^i$ 包含全局场景上下文和局部物体细节（如品牌名称、物体外观、空间位置），为后续任务合成提供精确的视觉锚点。

**模块2：任务指令自动合成（Task Instruction Generation）**
基于 $V_{meta}$ 和指定的目标网站，使用LLM（GPT-5）自动生成Web任务指令。合成过程要求任务必须具有明确的视觉依据——即任务的正确答案必须能从视频中唯一确定，而非依赖常识猜测。

**模块3：人工核验（Human Verification）**
标注者从三个维度对生成的任务进行核验与修正：(1) 视觉依据的准确性——视频中是否确实包含完成任务所需的视觉信息；(2) Web可行性——任务在真实网站上是否可执行；(3) 指令质量——任务描述是否清晰无歧义。这一人工环节确保了基准的高质量和视觉可追溯性。

### Ego2WebJudge自动评估框架

针对第一人称视频驱动的Web任务难以自动评估的问题，Ego2WebJudge设计为三阶段多模态LLM-as-a-Judge框架，其整体评估函数为：

$$O = Ego2WebJudge(I, \nu, A, S)$$

其中 $I$ 为任务指令，$\nu$ 为标注的第一人称视觉证据片段，$A$ 为智能体的动作序列，$S$ 为网页截图序列。输出 $O$ 为二元判定（成功/失败）。三阶段具体如下：

**阶段1：关键要点识别（Key-Point Identifier）**
从任务指令 $I$ 中提取完成该任务所需满足的关键要点列表。这些要点构成后续判断的检查清单，确保评估覆盖任务的所有必要子目标。

**阶段2：关键截图筛选（Key Screenshot Selector）**
从智能体轨迹的网页截图序列 $S$ 中筛选出与任务高度相关的子集。该阶段过滤掉大量无关的中间截图，降低后续判断阶段的上下文噪声。

**阶段3：最终判定（Final Judge）**
综合四类证据——任务指令 $I$、视觉证据片段 $\nu$、动作历史 $A$ 和关键截图——进行成功/失败的二元判定。该阶段的核心创新在于显式建模视觉证据与网页操作之间的一致性：判断器不仅检查最终结果是否正确，还验证智能体的操作路径是否基于对视频的正确理解。这有效减少了先前评估器（如WebVoyager评估、WebJudge）中常见的误判模式——例如智能体偶然猜对答案但视觉理解完全错误的情况。

Ego2WebJudge与人类判断的一致性达到约84%（GPT-4o版本），显著优于WebVoyager评估（74.7%）和WebJudge（78.4%），验证了融合视频证据对评估可靠性的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l818_https_arxiv_org_abs_2603_22529/figures/004_Figure_3.jpg]]
*Figure 3: | Left: Overview of the semi-automatic data generation pipeline proposed in our Ego2Web. We first build video profiles via a frozen MLLM that converts video clips into structured captions, then prompt an LLM to automatically generate web task instructions. Human annotators are required to verify and refine generated tasks to ensure quality. Right: A detailed view of our proposed automatic evaluation method, Ego2WebJudge, for the egocentric video grounded web agent tasks*



## 实验与关键发现

### 智能体主结果：第一人称视频感知构成显著瓶颈

Ego2Web在6个代表性Web智能体上进行评估，涵盖多模态原生模型与仅文本模型两类。所有智能体均在相同的真实在线网站条件下运行，人类评估由三位标注者独立完成并采用多数投票确定最终结果。

**Table 2** 展示了人类评估与Ego2WebJudge（三种MLLM后端）下的成功率（Success Rate, SR）。核心发现如下：

- **BU-Gemini-3-Flash** 以 **58.6%** 的人类评估SR位居首位，显著领先于其他智能体。相比之下，**Claude Sonnet 3.7 Computer Use** 仅取得 **26.4%**，**BU-GPT-4.1** 取得 **44.4%**，最优与最弱智能体之间的差距超过32个百分点。
- 在Ego2WebJudge自动评估下，BU-Gemini-3-Flash同样保持领先：使用Qwen3-VL-Flash作为评判后端时SR为 **57.2%**，使用Gemini-2.5 Pro时为 **48.2%**。
- 所有智能体距离Oracle性能仍存在 **约40%** 的显著差距（根据人类评估），表明当前最先进的Web智能体在处理第一人称视频感知与在线操作联合任务时存在明确的性能天花板。

**Table 3** 按任务领域细分SR。不同智能体在不同领域表现差异明显，但整体趋势一致：需要精细时空定位的任务（如电商商品搜索、媒体检索）对所有智能体构成最大挑战。

### 评估方法一致性：Ego2WebJudge显著优于先前方法

**Table 4** 报告了不同自动评估方法与人类判断的一致性率（Agreement Rate, AR）。Ego2WebJudge在使用GPT-4o作为评判后端时达到 **84.0%** 的最高一致性，使用Gemini-2.5-Pro时达到 **80.8%**。相比之下，**WebVoyager** 评估方法仅取得 **74.7%**，**WebJudge** 取得 **78.4%**，Ego2WebJudge较WebJudge提升 **+5.6%**。

这一改进主要源于Ego2WebJudge显式建模了第一人称视频中的视觉证据与智能体动作序列之间的一致性，而非仅依赖文本轨迹或最终响应进行判断。通过引入视频证据片段作为评判依据，Ego2WebJudge有效减少了先前评估器在视觉依赖型任务中的常见误判模式。

### 消融研究：原始视频输入不可替代

**Table 5** 报告了视觉输入模态对BU-Gemini-3-Flash性能影响的消融实验。在三种条件下对比：

- **原始视频输入**：SR = **48.2%**
- **详细文本描述**（由Gemini-3.1-Pro生成的结构化密集描述）：SR = **23.6%**
- **无视觉输入**（仅任务指令）：SR = **4.4%**

原始视频相对文本描述的提升达 **+24.6个百分点**，相对无视觉输入的提升超过43个百分点。这一结果强有力地证明：**精细的时空视觉线索（物体细节、时序关系、场景上下文）对于成功完成任务至关重要，且无法通过现有文本描述技术有效替代。**

值得注意的是，对于无法原生处理视频的智能体（Claude系列和GPT-5.4），实验中统一使用Gemini-3.1-Pro生成的详细文本描述作为视觉信息的代理。这些智能体的性能显著弱于能直接利用密集视频输入的智能体（如BU-Gemini-3-Flash），进一步说明当前视觉-文本转换流水线存在不可忽视的信息损失瓶颈。

### 失败模式分析：时间理解与物体误识别为核心短板

**Figure 6** 展示了一个典型的失败案例：BU-Gemini-3-Flash被要求识别视频中**第二个被拿起的酱料**并检索其产品页面。智能体因时间顺序理解错误而定位到错误的物品，且未能在网页上验证所需信息。这一案例揭示了当前智能体的两大核心失败模式：

1. **时间顺序误解**：智能体难以准确识别视频中事件发生的先后顺序，导致定位到错误的视觉目标。
2. **物体误识别**：在密集视觉场景中，智能体难以区分外观相似的物体，或在跨模态验证（视频中的物体 vs 网页上的商品信息）时出现偏差。

这些失败模式与消融实验中“无视觉输入SR仅4.4%”的发现相互印证：视觉感知能力是任务成功的必要条件，但当前智能体的视觉理解精度远未达到可靠水平。

### 补充图表

![[assets/figures/papers/paper_list_l818_https_arxiv_org_abs_2603_22529/figures/005_Figure.jpg]]
*Figure: (a) Task type distribution of Ego2Web. (b) Distribution of website domains in Ego2Web*

![[assets/figures/papers/paper_list_l818_https_arxiv_org_abs_2603_22529/figures/009_Table_2.jpg]]
*Table 2: | Success Rate (SR) measured by human evaluation and Ego2WebJudge using different Multimodal LLMs*

![[assets/figures/papers/paper_list_l818_https_arxiv_org_abs_2603_22529/figures/010_Table_3.jpg]]
*Table 3: | Fine-grained Success Rate (SR) per task domain across different models, evaluated by Ego2WebJudge with Gemini-2.5 Pro*

![[assets/figures/papers/paper_list_l818_https_arxiv_org_abs_2603_22529/figures/011_Table_4.jpg]]
*Table 4: | Agreement Rate (AR) between human evaluation and automatic evaluation methods across agents*

![[assets/figures/papers/paper_list_l818_https_arxiv_org_abs_2603_22529/figures/012_Table_5.jpg]]
*Table 5: | Ablation studies on the impact of video perception in our Ego2Web task. We report the Successful Rate (SR). We use Gemini-3.1-Pro to generate structured and detailed captions to represent an egocentric video. The experiment is conducted with Browser-Use (Gemini-3-Flash) and evaluated with Ego2WebJudge (Gemini-2.5-Pro)*

![[assets/figures/papers/paper_list_l818_https_arxiv_org_abs_2603_22529/figures/003_Table_1.jpg]]
*Table 1: | Benchmark comparison between Ego2Web and representative video reasoning and multimodal web-agent benchmarks. Unlike pure video reasoning datasets (e.g., EgoThink, EgoSchema) that focus on visual understanding alone, and prior web-agent benchmarks (e.g., WebVoyager, VisualWebArena) that emphasize online interaction with only web screenshot perception , Ego2Web uniquely connects real-world egocentric video with executable web tasks under an unconstrained online evaluation setting, forming a new testbed for multimodal agents grounded in the real-world visual perception*

![[assets/figures/papers/paper_list_l818_https_arxiv_org_abs_2603_22529/figures/013_Figure_6.jpg]]
*Figure 6: | Visualization of a web agent (BU-Gemini-3-Flash) failure case. The agent is required to identify the second picked-up sauce from the egocentric video and retrieve its product page. The agent incorrectly identifies the target item due to temporal misunderstanding and fails to verify the required information on the webpage*

![[assets/figures/papers/paper_list_l818_https_arxiv_org_abs_2603_22529/figures/014_Table_6.jpg]]
*Table 6: | Mapping from task categories to representative websites in Ego2Web, along with the number of tasks per category*

![[assets/figures/papers/paper_list_l818_https_arxiv_org_abs_2603_22529/figures/015_Figure_7.jpg]]
*Figure 7: | Example of egocentric video in Ego2Web, the detailed captions generated by Gemini-3.1-pro are listed above*



## 定位与知识库关联

### 1. 与现有基准的定位关系

Ego2Web 处于**第一人称视频理解**与**多模态 Web 智能体**两个研究方向的交叉地带，其核心贡献在于首次将物理世界的视觉感知与数字世界的在线操作耦合为统一的评估任务。Table 1 的系统对比清晰地刻画了这一独特定位：

- **相对于纯视频推理基准**（如 EgoThink、EgoSchema）：这些基准仅评估视觉理解能力，不涉及后续的 Web 操作。Ego2Web 则要求智能体将视频中的感知结果转化为可执行的在线 Web 动作，形成“感知→行动”的闭环评估。
- **相对于现有 Web 智能体基准**（如 WebVoyager、VisualWebArena）：这些基准的视觉输入仅限于网页截图，缺乏真实世界感知维度。Ego2Web 引入了第一人称视频作为必要的任务前置条件，要求智能体同时具备时空定位能力和 Web 操作能力。
- **相对于 WebJudge**（Xue et al., 2025）：Ego2WebJudge 在 WebJudge 的评估框架基础上进行扩展，引入了来自第一人称视频的视觉证据信号，使自动评估能够核实智能体是否真正基于视频中的视觉线索完成任务，而非仅依赖文本轨迹或最终响应。

### 2. 与基线智能体的能力边界

Ego2Web 评估了 6 个代表性 Web 智能体，覆盖了不同的视觉处理能力和架构设计：

| 智能体 | 视觉输入方式 | 核心能力特征 |
|--------|-------------|-------------|
| **SeeAct** (Zheng et al., 2024b) | 网页截图 | 基于视觉-语言模型的 Web 操作 |
| **Browser Use + GPT-4.1** (Müller & Žunič, 2024; OpenAI, 2026a) | 视频关键帧 | 通用 MLLM 驱动的浏览器操作框架 |
| **Browser Use + Gemini-3-Flash** (Deepmind, 2026) | 原生视频 | 原生视频理解 + 浏览器操作 |
| **Claude Sonnet 3.7/4.5 Computer Use** (Anthropic, 2024/2025) | 文本描述（代理） | 计算机操作能力，但无法直接处理视频 |
| **GPT-5.4** (OpenAI, 2026b) | 文本描述（代理） | 通用推理能力，视频通过文本描述间接输入 |

**关键区分维度**：智能体能否原生处理视频输入是性能分化的核心因素。BU-Gemini-3-Flash 以原生视频输入达到 58.6% 的人类评估成功率，而依赖文本描述的 Claude 3.7 仅达到 26.4%。这一差距直接揭示了当前视觉融合流水线的瓶颈：将视频转为文本描述会不可避免地丢失精细的时空视觉细节。

### 3. 适用边界

Ego2Web 的设计决定了其适用范围存在以下边界：

- **语言与场景覆盖**：当前基准仅覆盖英文网站和主要来自 Ego4D 数据集的西方场景第一人称视频，对非英语语言和其他文化场景的泛化能力未经验证。
- **任务复杂度**：任务主要集中在视觉理解驱动的搜索式操作（电子商务检索、媒体查找、知识查询、本地/地图服务），尚未涉及复杂的多页面交易流程或需要长期规划的 Web 任务。
- **视觉依据的粒度**：任务要求智能体从视频中识别特定物体或事件，但视频中的视觉线索通常是稀疏且非结构化的，对需要精确空间定位或细粒度属性判别的场景可能不够充分。
- **评估环境**：所有评估均在真实在线网站上进行，网站内容、布局或可访问性的动态变化可能引入不可控方差，影响结果的可重复性。

### 4. 局限与开放问题

#### 4.1 已识别的局限

1. **视觉-文本转换的信息损失**：对于无法原生处理视频的智能体（Claude 系列、GPT-5.4），必须依赖 Gemini-3.1-Pro 生成的详细文本描述作为代理。消融实验（Table 5）表明，仅使用文本描述的成功率（23.6%）远低于原始视频输入（48.2%），说明当前文本代理方案无法有效传递精细的时空视觉线索。

2. **Ego2WebJudge 的评估可靠性**：虽然 Ego2WebJudge 达到了约 84% 的人类判断一致率，但在模糊场景或跨模态冲突情况下仍可能出错，不能完全替代人类评估。特别是在智能体的动作序列与视频证据之间存在微妙不一致时，自动评估可能产生误判。

3. **在线评估的生态效度与可重复性矛盾**：真实在线网站提供了高生态效度，但网站的动态变化使得同一任务在不同时间的评估结果可能不一致，对基准的长期可重复性构成挑战。

4. **时空推理的薄弱环节**：错误分析（Figure 6）显示，智能体在时间顺序理解（如“视频中拿起的第二件物品”）和物体误识别方面失败率较高，这些能力是当前 MLLM 的普遍短板。

#### 4.2 开放问题

1. **如何设计更有效的视觉-文本融合机制**，使仅能接收文本的智能体也能利用丰富的视觉线索？这是弥合原生视频智能体与文本代理智能体之间性能差距的关键。

2. **能否通过引入更细粒度的时空标注或视频-网页联合推理**来进一步提升 Ego2WebJudge 的评估准确性？当前的评估框架依赖关键帧和截图的对齐，更精细的跨模态对齐机制值得探索。

3. **在真实世界应用中，如何平衡在线评估的生态效度和可重复性**？可能的方案包括定期快照网站状态、构建静态镜像，或设计对动态内容鲁棒的评估指标。

4. **如何针对性地加强智能体在物体误识别和时间顺序误解方面的能力**？这可能需要专门的训练数据或推理时干预策略，例如引入显式的时序推理模块或多帧对比验证机制。



## 原文 PDF

![[paperPDFs/CVPR_2026/Ego2Web_A_Web_Agent_Benchmark_Grounded_in_Egocentric_Videos.pdf]]
