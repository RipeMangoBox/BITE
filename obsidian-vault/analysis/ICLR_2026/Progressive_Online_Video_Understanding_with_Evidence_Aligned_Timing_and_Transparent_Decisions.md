---
title: "Progressive Online Video Understanding with Evidence-Aligned Timing and Transparent Decisions"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Progressive_Online_Video_Understanding_with_Evidence_Aligned_Timing_and_Transparent_Decisions.pdf
project_link: null
code_link: null
aliases:
- TQ
- POVUEATTD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "将推理控制（决策器）与记忆/集成分离，并引入可量化的进度信号ρ和置信度信号c，使模型能够根据证据的充分性自动确定响应时机，同时通过多层次聚合令牌在深度Transformer中渐进式更新紧凑的全局认知状态。"
primary_logic: "将用户查询分解为可观察的子目标，结合在Transformer不同深度层次上逐步聚合视觉信息的分层集成策略，可以在同一框架内同步实现证据对齐的响应时机、透明的决策推理和高效的因果状态追踪。"
claims:
- "Thinking-QwenVL在StreamingBench实时视觉理解任务上达到71.60%的准确率，超越之前最好的在线方法Dispider（67.63%），提升3.97个百分点。"
- "在OVOBench上，以93.75%的帧减少率，Thinking-QwenVL仍取得46.9%的整体准确率，显著优于所有其他在线方法（例如Dispider 41.8%）。"
- "HPSI的分层聚合至关重要：若将其替换为单步自适应池化（未分层），VideoMME总体准确率下降7.4%，OVOBench下降3.5%。"
- "ATDM具有框架无关性，将其嵌入Flash-VStream后，StreamingBench准确率从22.53%提升至26.58%（+4.05%）。"
---

# Progressive Online Video Understanding with Evidence-Aligned Timing and Transparent Decisions

> [!tip] 核心洞察
> 将用户查询分解为可观察的子目标，结合在Transformer不同深度层次上逐步聚合视觉信息的分层集成策略，可以在同一框架内同步实现证据对齐的响应时机、透明的决策推理和高效的因果状态追踪。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 渐进式在线视频理解：证据对齐时序与透明决策 |
| 英文题名 | Progressive Online Video Understanding with Evidence-Aligned Timing and Transparent Decisions |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=oKB0CacHaM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Thinking-QwenVL |
| Dataset | StreamingBench (Real-Time Visual Understanding), OVOBench (Overall), RTVBench (Overall), VideoMME (Overall, w/o subs) |

> [!tip] 效果简介
> - StreamingBench (Real-Time Visual Understanding) 上，准确率 (%) 为 71.60，对比 67.63 (Dispider)，变化 +3.97。
> - OVOBench (Overall) 上，准确率 (%) 为 46.9 (↓93.75% frames)，对比 41.8 (Dispider)，变化 +5.1。
> - RTVBench (Overall) 上，准确率 (%) 为 35.87，对比 32.75 (Qwen2.5-VL)，变化 +3.12。

## 概要

在线视频理解要求模型实时处理流式片段，并在累积充分视觉证据的恰当时刻对用户查询做出响应。现有在线视频大语言模型（VLLMs）面临两个根本性瓶颈：① 决策过程不透明，缺乏可观测的推理状态，无法将响应时刻 $t_r$ 精确对齐到最早充分证据时刻 $t^\star$，导致偏差 $\delta = |t_r - t^\star|$ 过大；② 在有限的计算和令牌预算下，难以高效维持和更新跨片段的全局因果一致认知状态 $h_t$。这种“何时回答”与“如何记忆”的双重挑战严重制约了流式视频理解的性能。

为此，本文提出 **Thinking-QwenVL**——一种渐进式、证据对齐的在线视频理解框架，将推理控制与视觉记忆/集成解耦，并引入两个核心模块：
- **主动思考决策器（Active Thinking Decision Maker, ATDM）**：作为透明的推理控制器，将决策过程分解为五个可观测阶段，输出连续的进度信号 $\rho \in [0,1]$ 和置信度信号 $c \in [0,1]$。这些信号既量化了当前证据的充分性，又压缩了历史中间判断，使模型能在内部状态满足条件时自动触发响应（$\rho = 1$），实现 $t_r \approx t^\star$。
- **层级渐进语义集成（Hierarchical Progressive Semantic Integration, HPSI）**：作为高效的记忆系统，在LLM内部不同深度层（$0$, $L/3$, $2L/3$）插入可学习的多层级聚合令牌，配合结构化稀疏注意力，逐层将密集视觉序列压缩为紧凑的全局认知状态，并以极小令牌预算支持跨片段的因果传播。

其核心思想在于：将用户查询分解为可观察的子目标，结合在Transformer不同深度层次逐步聚合视觉信息的分层集成策略，在同一框架内同步实现证据对齐的响应时机、透明的决策推理和高效的因果状态追踪。

在多个基准上的实验验证了方法的有效性：
- **在线实时理解**：在 StreamingBench 的实时视觉理解任务上达到 71.60% 的准确率，较先前最优在线方法 Dispider（67.63%）提升 3.97 个百分点；在 OVOBench 上，即使将视频帧减少 93.75%，仍取得 46.9% 的整体准确率，显著优于其他在线方法。
- **离线长视频**：在 VideoMME、MLVU 等长视频基准上也表现出竞争力，证明 HPSI 在极端压缩下能有效保持记忆质量。
- **关键消融**：HPSI 的逐层渐进聚合对性能至关重要——替换为单步池化使 VideoMME 整体准确率下降 7.4%；ATDM 中的连续进度/置信度信号比二元门控带来 3.62 个百分点的增益，且该模块具有框架无关性，可直接嵌入其他在线 VLM 并提升其性能。
- **鲁棒性**：在面对 30% 丢帧压力时，准确率仅从 71.60% 降至 67.81%，展现出良好的流式鲁棒性。

综上，Thinking-QwenVL 通过可量化的决策控制和层级化记忆集成，为在线视频理解提供了一种高效、透明且鲁棒的新范式。



在线视频流理解（如实时监控、自动驾驶、视频助手）要求模型在视频片段持续到达的过程中，对用户查询（query）做出及时而准确的回应。理想情况下，回应的时刻 $t_r$ 应当与视频中首次出现足以支撑该问题答案的视觉证据的时刻 $t^\star$ 精确对齐，即最小化响应偏差 $\delta = |t_r - t^\star|$。然而，现有视频大语言模型（VLLM）主要面向离线场景，仅在全视频可获取后才做出回答（$t_r = T$），无从谈及“何时回答”的决策；而近期兴起的流式（在线）VLLM虽然在每一时刻 $t$ 仅能看到已到达的片段 $\mathbb{V}_t = \{v_1, \ldots, v_t\}$，却普遍缺乏显式的决策机制，导致响应时机（$t_r$）要么机械地固定在查询发出的时刻（$t_r = t_q$），要么依赖于粗糙的启发式规则（如场景切换），未能将回答时刻与最早充分证据时刻绑定。这一结构性缺陷造成两个直接后果：

1. **决策过程不透明**。以先前表现最好的在线方法 Dispider 为例，它采用一个二元的“可答性”头部决定是否在当前时刻输出答案，但该头部不提供任何可观测的中间推理状态，使用者无法知晓模型为何选择此刻回答、对当前证据的充分性究竟有多大把握。这种不透明性既降低了系统的可信度，也阻碍了对错误决策的溯源与修正。
2. **响应时机与证据不对齐**。无论是 Dispider 的二元门控，还是 VideoLLM‑online 的“以查询时刻为响应时刻”策略，均无法在证据积累过程中主动感知是否已达到“足够回答”的信心。由此，系统往往会过早给出猜测性答案，或在证据早已充分后仍无谓等待，造成 $\delta = |t_r - t^\star|$ 变大，直接影响正确率。

与此同时，在线视频理解还面临一个根本性的记忆挑战：流式输入的片段（clips）被依次处理，若不对历史信息进行高效压缩，则随着流长度增长，计算开销和显存占用将难以承受；若压缩过度，则丢失跨片段的因果依赖，导致全局认知不连贯。现有在线方法多采用单步池化或简单的片段间缓存，缺乏一种在深度 Transformer 内部进行分层渐进式集成的机制，无法在极低的令牌预算下维持可回溯的全局认知状态 $h_t$，其更新函数 $h_{t+1} = \mathscr{U}(h_t, v_{t+1})$ 的设计粗糙，难以捕捉长程因果链。

上述瓶颈的根本成因在于：现有系统将推理控制（何时回答、是否反思）与视觉记忆（如何积累认知状态）耦合在一个黑箱结构中，既无法对决策时机进行精细调控，也限制了记忆的建模能力。从宏观来看，离线模型过度等待（全视频结束），传统流式模型则过早回答（查询时刻），两者均未能实现证据对齐的响应，如图 1 所示的范式对比。

为此，本文的动机在于构建一个将推理控制与记忆集成解耦的框架，使得模型能够**根据证据的充分性自动确定响应时机**，同时能够在有限计算预算下**渐进式地保持因果一致的全局认知**。核心思路可概括为：将用户查询分解为可观察的子目标，结合在 Transformer 不同深度层次上逐步聚合视觉信息的分层集成策略，在同一框架内同步实现证据对齐的响应时机、透明的决策推理和高效的因果状态追踪。这一动机催生了两个核心组件——用于透明推理控制的主动思考决策器（ATDM）和用于渐进式语义集成的分层渐进语义集成模块（HPSI），二者协同工作，首次在在线视频 LLM 中明确量化和观测“能否回答”的进度信号 $\rho$ 与置信度信号 $c$，从而将响应时刻拉到 $t_r \approx t^\star$ 的理想点。



## 核心方法与创新机理

Thinking-QwenVL相对于现有在线视频LLM的核心创新在于将**推理控制与视觉记忆解耦**，并通过两个可量化信号——进度ρ与置信度c——将决策过程透明化，从而在单一框架内同时解决证据对齐响应时机、高效因果状态追踪和可解释决策三大瓶颈。

### 关键模块与changed slots

**1. 视觉记忆：从单步池化到分层渐进式语义集成（HPSI）**

现有在线方法多采用单步池化或无层次聚合，跨片段缺乏因果传播，难以在极端令牌压缩下维持长程依赖。HPSI将此替换为在Transformer的不同深度层（第0层、L/3层、2L/3层）插入可学习的多层级聚合令牌p^(j)，配合结构化稀疏注意力掩码，实现三层渐进式集成：

- **浅层（第0层）**：保留细粒度局部证据，令牌数最多（3:2:1比例）；
- **中层（L/3层）**：整合中程时序与结构模式；
- **深层（2L/3层）**：形成紧凑的全局认知状态h_t，支持因果传播。

聚合令牌通过自适应池化从前一级初始化，并在训练中显式约束其忠实地重建对应片段的池化特征及层级间平滑过渡（Eq.5）。消融实验证实，若将HPSI退化为单步自适应池化（移除层级2和3），VideoMME总体准确率下降7.4%，OVOBench下降3.5%（Table 4），证明逐层渐进式聚合不可替代。

**2. 决策机制：从不透明门控到透明五阶段决策器（ATDM）**

基线方法采用二元“可答/不可答”门控（如Dispider）或固定t_r = t_q，缺乏可观测的中间状态，无法说明响应时机的依据。ATDM将决策过程分解为五个透明阶段：

1. **问题引导的字幕指南生成**：将用户查询转换为具体的视觉元素关注指令；
2. **问题分解**：将复杂查询拆解为可逐片段验证的子问题——移除该模块使StreamingBench准确率下降2.37个百分点（Figure 7）；
3. **逐片段字幕与证据提取**（在线执行）；
4. **子答案提取与进度/置信度跟踪**（在线执行）——输出连续信号(ρ, c)，替代二元标志。实验表明，将连续进度跟踪替换为二元“可答/不可答”标志导致准确率下降3.62个百分点，是五个组件中影响最大的（Figure 7）；
5. **主动反思触发**：当置信度c过低或出现语义剧变时，自动回溯并修正前期判断。

ATDM具有框架无关性：将其嵌入Flash-VStream后，StreamingBench准确率从22.53%提升至26.58%（+4.05%），验证了决策透明化本身即可释放通用VLM的推理能力，而非依赖特定架构。

### 创新协同效应

HPSI与ATDM的协同体现为：HPSI在极小令牌预算下维持紧凑全局认知状态，使ATDM在每个片段都能基于完整历史做出知情的进度判断；ATDM通过ρ和c信号指导HPSI的记忆更新优先级，并在证据充分时（ρ=1）触发回答，使t_r ≈ t★。这一解耦设计在StreamingBench上达到71.60%（超越Dispider的67.63%），在OVOBench上以93.75%帧减少率取得46.9%（超越Dispider的41.8%），同时面对30%帧丢失时准确率仍维持67.81%（Table 5），证实了证据对齐时机与高效记忆在统一框架中的可行性。



![[assets/figures/papers/iclr26_0015_oKB0CacHaM_Progressive_Online_Video_Understanding_with_Evid/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline of Thinking-QwenVL. Given streamed clips and a query Q, ATDM generates question-guided caption instructions, decomposes Q into sub-questions, and iteratively extracts evidence from each clip (with progressive visual integration using HPSI), updating sub-answers with progress $\rho \in$ [ 0 , 1 ] and confidence $\mathbf { c } \in$ [ 0 , 1 ] . This process runs in parallel across clips and permits to trigger active reflection according to c. The model emits an answer at $t _ { r } = t _ { i }$ once $\pmb { \rho } ( t _ { i }$ ) = $\mathbf { 1 }$

Thinking-QwenVL 的整体 pipeline 围绕**透明的推理控制**与**高效的视觉记忆**两个解耦功能模块构建，将在线视频理解转化为一个渐进的、证据对齐的决策过程。系统的核心输入是用户查询 $Q$ 与流式视频片段序列 $\mathbb{V}_t = \{v_1, \dots, v_t\}$，输出则是一个在最早充分证据时刻 $t^\star$ 附近触发的最终响应，并伴随可观测的进度信号 $\rho \in [0,1]$ 与置信度信号 $c \in [0,1]$ 作为中间决策状态。

如图 3 所概览，该框架的工作流可以归纳为以下几个关键步骤：

1. **查询分解与字幕指导**  
   当查询 $Q$ 被提交，**主动思维决策器（Active Thinking Decision Maker, ATDM）** 首先生成问题引导的视觉描述指令，并将 $Q$ 分解为一组可观察的子问题（sub‑questions）。这部分在流式开始时就完成，为后续逐片段的证据提取提供明确的子目标。

2. **逐片段证据提取与视觉集成**  
   对于每一个到达的片段 $v_i$，模型并行执行两项操作：
   - **视觉集成**：**分层渐进语义集成模块（Hierarchical Progressive Semantic Integration, HPSI）** 将片段内的密集视觉令牌在 LLM 的不同深度层（层 0、$L/3$、$2L/3$）上逐步压缩为三层可学习的聚合令牌 $p_{\text{clip}_i}^{(1)}, p_{\text{clip}_i}^{(2)}, p_{\text{clip}_i}^{(3)}$，并通过结构化稀疏注意力将压缩后的信息因果地传播至后续片段，形成不断更新的紧凑全局认知状态 $h_t$（见公式 1–5 及图 2）。
   - **证据抽取**：ATDM 利用当前认知状态与子问题，提取与各子目标相关的视觉证据，更新子答案，并输出本片段对应的局部进度贡献与置信度评估。

3. **主动反思与停止决策**  
   ATDM 将上述过程封装为一个五阶段的可观察思维链（Figure 4），其中进度 $\rho$ 和置信度 $c$ 构成连续型的决策遥测信号。当某个片段的处理导致置信度 $c$ 过低或语义内容发生剧烈变化时，ATDM 会自动触发跨片段的**主动反思（active reflection）**，重新审视过去的判断。一旦累积的进度 $\rho = 1$，模型即判定已经收集到回答 $Q$ 所需的充分证据，随即在当前时刻 $t_r$ 输出最终答案，使得 $t_r \approx t^\star$（见 Section 3.2）。

值得强调的是，HPSI 负责**状态记忆与视觉压缩**，ATDM 负责**推理控制与时机决策**，二者在 LLM 内部通过统一的令牌流协同工作，既保证了在线场景下对长程因果关系的捕获，又赋予了系统透明、可量化的决策能力。这一分离设计使得 ATDM 可以作为通用控制器，在无需修改 HPSI 的前提下被迁移至其他在线视觉语言模型（例如 Flash‑VStream），大幅提升其响应决策质量（Table 1 中 Flash‑VStream 嵌入 ATDM 后准确率从 22.53% 提升至 26.58%）。



Thinking-QwenVL 的核心由两大模块构成：**分层渐进语义集成 (HPSI)** 负责在极低令牌预算下构建紧凑的全局认知状态，**主动思维决策器 (ATDM)** 则通过可观测的进度与置信度信号实现证据对齐的响应时机控制。二者的目标均围绕最小化响应偏差 $\delta = |t_r - t^\star|$ 展开，其中 $t_r$ 为模型实际输出回答的时刻，$t^\star$ 为流中首次出现充分视觉证据的时刻。视觉信息的渐进更新由递归式认知状态更新 $h_{t+1} = \mathscr{U}(h_t, v_{t+1})$ 表征，具体由 HPSI 在前向传播中逐片段完成。

### 1. 分层渐进语义集成 (HPSI)

HPSI 在 LLM 的不同 Transformer 深度（第 0、$L/3$、$2L/3$ 层）插入三组可学习的聚合令牌，配合结构化稀疏注意力，以层次化方式将密集视觉序列压缩为保留因果关系的高层语义表示。关键公式如下：

**完整输入序列构造**  

$$
\widetilde{\mathcal{T}} = \mathrm{concat} \big( 
\boldsymbol{w}, 
\boldsymbol{v}_{\mathrm{clip}_1}, \boldsymbol{p}_{\mathrm{clip}_1}^{(1)}, \boldsymbol{p}_{\mathrm{clip}_1}^{(2)}, \boldsymbol{p}_{\mathrm{clip}_1}^{(3)}, 
\dots, 
\boldsymbol{v}_{\mathrm{clip}_n}, \boldsymbol{p}_{\mathrm{clip}_n}^{(1)}, \boldsymbol{p}_{\mathrm{clip}_n}^{(2)}, \boldsymbol{p}_{\mathrm{clip}_n}^{(3)}, 
\boldsymbol{w} \big)
$$

其中：
- $\boldsymbol{w}$：文本指令的嵌入表示；
- $\boldsymbol{v}_{\mathrm{clip}_i}$：第 $i$ 个视频片段的视觉令牌；
- $\boldsymbol{p}_{\mathrm{clip}_i}^{(j)}$：第 $i$ 个片段在第 $j$ 层（$j=1,2,3$）的聚合令牌，其数量比例为 $3:2:1$。

**聚合令牌初始化**  

$$
\boldsymbol{p}_{\mathrm{clip}_i}^{(j)} = \mathtt{AdapterPool} \Big( \boldsymbol{p}_{\mathrm{clip}_i}^{(j-1)}, \ (4-j) \, N_{vc} \Big)
$$

- $\mathtt{AdapterPool}$：自适应平均池化操作；
- $N_{vc}$：单个片段的视觉令牌数目；
- 该式表明第 $j$ 层聚合令牌由上一级令牌通过池化降维得到，越深的层级保留越少的令牌。

**渐进集成训练目标**  

$$
\min\, \mathcal{T}_{\mathrm{integration}} = \sum_{l=0}^{L-1} \sum_{j=1}^{3} 
\Big( \| \boldsymbol{p}_{\mathrm{clip}_i}^{(j)(l)} - \mathtt{POOL}( \boldsymbol{v}_{\mathrm{clip}_i} ) \|_2 
+ \| \boldsymbol{p}_{\mathrm{clip}_i}^{(j)(l)} - \boldsymbol{p}_{\mathrm{clip}_i}^{(j-1)(l)} \|_2 \Big)
$$

- $\boldsymbol{p}_{\mathrm{clip}_i}^{(j)(l)}$：第 $l$ 层 Transformer 输出后第 $j$ 级聚合令牌的表示；
- $\mathtt{POOL}(\boldsymbol{v}_{\mathrm{clip}_i})$：片段的全局池化特征；
- 第一项鼓励聚合令牌忠实地恢复原始视觉信息，第二项强制相邻层级间语义平滑过渡，从而保证层次化压缩的因果一致性。

通过这些机制，HPSI 在仅保留约 6.25% 视频帧（即压缩率 93.75%）的情况下，仍能维持紧凑且可传播的全局认知状态 $h_t$。

### 2. 主动思维决策器 (ATDM)

ATDM 将决策过程外部化为五个可观测的阶段：①问题引导的视觉描述指令生成；②问题分解为子目标；③片段级描述；④子答案提取与连续状态更新（输出进度 $\rho \in [0,1]$ 和置信度 $c \in [0,1]$）；⑤低置信度触发的跨片段主动反思。最终当 $\rho = 1$ 时，模型在 $t_r$ 时刻输出最终答案。

该模块并无显式的标量公式，但其行为由以下整体框架约束：
- **决策目标**：使响应时间尽可能逼近最早充分证据时间，即最小化 $\delta = |t_r - t^\star|$。
- **状态追踪**：利用 HPSI 输出的认知状态 $h_t$ 进行迭代推理，并依据历史进展 $(\rho, c)$ 决定是否继续等待或触发反思。

消融实验表明，将连续进度/置信度跟踪（阶段④）替换为二值“可答/不可答”标志会导致 StreamingBench 准确率下降 3.62 个百分点，是 ATDM 五个组件中影响最大的部分（Figure 7）；同时 ATDM 具有框架无关性，将其嵌入 Flash-VStream 后使该基线在 StreamingBench 上提升 +4.05%（Table 1）。



## 实验与关键发现

### 主结果：在线实时理解与离线长视频基准

Thinking-QwenVL 在多个在线和离线基准上均取得领先结果，其核心增益来源于两个因果机制：(1) HPSI 在极端令牌压缩下保留因果一致的认知状态；(2) ATDM 根据可观测的进度 $\rho$ 和置信度 $c$ 将响应时刻 $t_r$ 对齐到充分证据出现时刻 $t^\star$，避免传统流式模型在查询时刻机械应答或全片完成后才输出的局限。

**在线流式基准。** 在 StreamingBench 的 Real-Time Visual Understanding 任务上，Thinking-QwenVL 取得 **71.60%** 的整体准确率，较此前最强的在线方法 Dispider (67.63%) 提升 +3.97 个百分点（Table 1）。Table 1 同时显示，以开源基座 Qwen2.5-VL 的注意力重分配实现 HPSI 时，我们的方法显著优于只做流式注入而无显式决策的 Flash-VStream（22.53% → 26.58% 仅通过嵌入 ATDM，说明决策控制器的框架无关性）。在 OVOBench 上，模型在帧减少 93.75% 的苛刻条件下，整体准确率达到 **46.9%**，远超 Dispider (41.8%) 和其他在线方法（Table 2），其中 Real‑Time Visual Perception、Backward Tracing 和 Forward Active Responding 均有明显优势。该结果表明 HPSI 的紧凑全局认知状态 $h_t$ 在长依赖回溯和前向主动响应中提供了有效的证据维持。

![[assets/figures/papers/iclr26_0015_oKB0CacHaM_Progressive_Online_Video_Understanding_with_Evid/figures/005_Table_1.jpg]]
*Table 1: Accuracy (100%) comparison on StreamingBench focusing on Real-Time Visual Understanding tasks. † indicates the reproduced results. The meaning of each subtask is in Appendix A.5*

![[assets/figures/papers/iclr26_0015_oKB0CacHaM_Progressive_Online_Video_Understanding_with_Evid/figures/006_Table_2.jpg]]
*Table 2: Accuracy on OVOBench. Real.: Real-Time Visual Perception, Back.: Backward Tracing, Forw.: Forward Active Responding. –: The specific requirements of Forw. task resulted in VideoLLM-online not being able to response in demanded format*

**离线长视频基准。** 即使将帧数量压缩至原始视频的 1/16（↓93.75%），Thinking-QwenVL 在 VideoMME (w/o subs) 的整体准确率达到 **56.3%**，高于全帧访问的 TimeChat-Online (52.8%)（Table 3）。在 MLVU 上，当以注意力重分配替代插入 100% 帧时（即不实际增加视觉令牌数），模型取得 **68.3%**，说明 HPSI 的分层聚合可在不牺牲语义的前提下实现高效推理。RTVBench 上，模型整体准确率从基线的 32.75% 提升至 **35.87%**（+3.12%，Table 7），进一步验证了 ATDM 在多类实时感知、意图分析等子任务上的决策质量。

### 消融实验：验证因果组件

消融实验定量揭示了 HPSI 的分层集成与 ATDM 的透明遥测是性能的核心支点。

**HPSI 三层聚合的必要性。** 若将 HPSI 替换为单步自适应池化（Table 4 ♠），即仅保留第一层聚合且最终令牌预算相同，VideoMME 整体准确率下降 **7.4%**，OVOBench 下降 **3.5%**。进一步移除深层聚合令牌（Level‑2 或 Level‑3）均造成可观的性能损失，而移除“首帧保留”设计（First Frame）则严重损害长视频子集的表现。这些结果证实：浅层保留细粒度局部证据、中层整合时序模式、深层构建全局因果图的逐层分工，是低令牌预算下维持连贯认知的关键，不可用单一池化替代。

![[assets/figures/papers/iclr26_0015_oKB0CacHaM_Progressive_Online_Video_Understanding_with_Evid/figures/009_Table_4.jpg]]
*Table 4: Impact of 3 level aggregation on VideoMME w/o subs and OVOBench. We ablate by directly removing the corresponding level tokens. ♠ denotes that the first-stage compressed-token count is set as the final token budget (1×)—equivalent to applying adaptive pooling to visual tokens before the LLM, as in prior long-video models. FF: First Frame. LV: Level. ■ : burden of tokens*

**ATDM 组件贡献。** Figure 7 对 ATDM 五个部分逐一消融，显示将连续进度 $(\rho, c)$ 替换为二元“可答/不可答”标志（Part‑4）带来的损失最大（**‑3.62%**），其次是视频片段字幕提取（Part‑3，‑3.35%）和问题分解（Part‑2，‑2.37%）。这直接证明：连续遥测不仅提供停止信号，还浓缩了此前所有中间判断的历史信息，远比二元门控丰富；同时，将查询分解为子问题并逐片段收集证据，是实现证据对齐响应的前提。若移除整个 ATDM 而采用简单的视觉问答头部，StreamingBench 准确率显著下降，进一步说明透明决策流水线对在线设定不可或缺。

![[assets/figures/papers/iclr26_0015_oKB0CacHaM_Progressive_Online_Video_Understanding_with_Evid/figures/012_Figure_7.jpg]]
*Figure 7: Impact of ATDM components. All represents the complete model performance when use ATDM. Each column beyond this represents the ablation of the corresponding part of ATDM*

**框架无关性与鲁棒性。** 将 ATDM 嵌入原本无决策机制的 Flash-VStream 后，StreamingBench 准确率从 22.53% 提升至 26.58%（+4.05%，Table 1），表明决策器可独立于特定视觉记忆系统发挥作用。系统丢帧压力测试（Table 5）显示，即使随机丢失 30% 帧（保留 70%），模型在 StreamingBench 上的准确率仍能维持 **67.81%**（完整帧为 71.60%），展现出对流式帧缺失的良好鲁棒性。

![[assets/figures/papers/iclr26_0015_oKB0CacHaM_Progressive_Online_Video_Understanding_with_Evid/figures/014_Table_5.jpg]]
*Table 5: Robustness and Applicability. Top: Stress-testing streaming robustness under abnormal conditions by uniformly dropping frames after 1 FPS extraction (retaining 100%, 80%, 70%). Bottom: The ATDM controller is applied to multiple backbones (Flash-VStream-LLaVA-7B, Our Thinking-Qwen2.5-VL-3B/7B), showing its framework-agnostic utility. Figure 8: Efficiency on NVIDIA A100 GPUs. Impact of the aggregation rate in HPSI on FPS and token throughput. At 93.75% aggregation rate, our method matches Flash-VStream’s FPS (8.49 vs. 8.45) with 78× higher avg. token throughput (1261 vs. 16), and a slight latency increase (13.2ms vs. 9.5ms)*

### 效率与延迟分析

Figure 8 展示了在 NVIDIA A100 GPU 上的效率分析：在 93.75% 聚合率下，我们的方法保持了与 Flash-VStream 相当的 FPS（8.49 vs. 8.45），但平均令牌吞吐量提高了约 78 倍（1261 vs. 16），仅引入微小额外延迟（13.2 ms vs. 9.5 ms）。这一结果说明，HPSI 通过结构化稀疏注意力和可学习聚合令牌，以几乎可忽略的额外计算代价，实现了信息密度的巨大提升，使其兼具实时性能和高语义保真度。

### 失败模式与当前局限

尽管 Thinking-QwenVL 在多个维度取得领先，仍存在以下已知限制，需在部署时谨慎对待或通过后续工作改进：

1. **模态局限**：当前方法仅处理视觉流，未集成音频或其他传感器模态。在多模态证据对齐场景（如视频带语音或环境音）中，无法利用跨模态互补信息，可能导致决策偏差。
2. **极长流稳定性未验证**：基准测试的视频时长大多不超过 120 分钟，对于数小时乃至数天的持续流，HPSI 的全局状态膨胀和 ATDM 历史依赖的长期漂移效应尚未经过充分验证，长期稳定性存疑。
3. **决策阈值的经验设定**：ATDM 中置信度边界（如 $c \approx 0.5$ 视为相关，$c > 0.85$ 视为充分）目前基于人工经验选择，缺乏跨任务自动校准机制。在分布外数据或新任务上，固化阈值可能导致过早或过晚响应。
4. **可解释性受限于底层 LLM**：ATDM 的透明推理依赖文本化中间输出，其质量取决于 Qwen2.5-VL 的指令遵循能力与视觉幻觉倾向。当 LLM 生成不忠实或无关的字幕时，进度与置信度信号可能被误导。
5. **边缘设备部署门槛**：尽管分层压缩极大降低了令牌数，但在资源极度受限的边缘设备上，Transformer 深层推理和实时决策的延迟与内存占用仍需进一步优化。

> 以上全部结论均基于已报告的实验数据和分析，部分失败模式（如极长流稳定性）未在论文中给出量化评估，建议在实际应用时针对目标场景进行专项验证。



## 定位与知识库关联

Thinking‑QwenVL 回应了在线视频理解中两个长期被忽视的系统性瓶颈：**决策不透明**与**时序-证据错位**。当前在线方法（如 Dispider、Flash‑VStream、VideoLLM‑online、TimeChat‑Online）普遍将“何时回答”简化为不可观测的二值门控（可答/延迟）或固定在查询时刻 $t_q$ 瞬间应答，导致响应时间 $t_r$ 与最先充分证据时刻 $t^\star$ 之间存在无法量化的偏差 $\delta = |t_r - t^\star|$，且在连续流式输入下无法追溯推理过程。与此同时，这些方法依赖单步池化或无层次聚合的视觉记忆，跨片段缺乏因果传播，难以在有限令牌预算下维持全局因果一致的理解。Thinking‑QwenVL 通过**将推理控制与记忆/集成分离**，并引入可量化的进度信号 $\rho$ 和置信度信号 $c$，从根本上改变了这一格局。

### 相对于基准方法的改进本质

相比于现有在线视频 LLM，Thinking‑QwenVL 在两条正交的因果控制轴上进行了结构性改造：

**视觉记忆与集成**：Dispider、Flash‑VStream 等基线普遍采用**单步池化或浅层融合**，记忆状态 $h_t$ 缺乏层次化抽象，难以在长时序中传播因果信息。Thinking‑QwenVL 的 **HPSI（Hierarchical Progressive Semantic Integration）** 则在 Transformer 的不同深度层（$0,\ L/3,\ 2L/3$）注入可学习的多层级聚合令牌 $\boldsymbol{p}_{\text{clip}}^{(j)}$，配合结构化稀疏注意力，将密集视觉序列压缩为紧凑的、保留因果关系的全局认知状态。这一设计使模型在下游任务中获得了显著的性能优势：移除 HPSI 的层级 2 和层级 3（即退化为单步自适应池化）直接导致 VideoMME 总体准确率下降 7.4%，OVOBench 下降 3.5%（Table 4 ♠ 变体）。由此可见，**逐层渐进式聚合**并非简单的工程优化，而是维持长程因果推理的必要条件。

**决策与响应时机**：基线方法普遍采用**不透明的二元门控**（Dispider）或**固定 $t_r = t_q$**（VideoLLM‑online），缺乏可观测的中间决策状态，无法解释为何某时刻选择回答。Thinking‑QwenVL 的 **ATDM（Active Thinking Decision Maker）** 将决策过程外部化为五个透明阶段（问题引导指南生成、问题分解、逐片段字幕、子答案提取与更新、低置信度触发的主动反思），并输出连续进度 $\rho\in[0,1]$ 和置信度 $c\in[0,1]$。当 $c$ 过低或出现语义剧变时，自动触发跨片段反思；仅在 $\rho=1$ 时确定 $t_r \approx t^\star$，首次实现了证据对齐的应答时机。消融实验表明，将 $\rho, c$ 连续跟踪替换为二元“可答/不可答”标志会使 StreamingBench 准确率下降 3.62 个百分点（Figure 7, P_4 消融），这是五个 ATDM 组件中影响最显著的一项，证实了**连续状态信号的可观测性**对于决策质量的决定性作用。

ATDM 的另一关键特性是**框架无关性**：将其嵌入 Flash‑VStream（原版无显式决策机制）后，StreamingBench 准确率从 22.53% 跃升至 26.58%（+4.05%，Table 1），表明 ATDM 的透明决策器可独立于底层视觉编码器或记忆机制发挥作用，具有向其他在线视频系统嫁接的潜力。

### 适用边界

Thinking‑QwenVL 的设计天然适配**在线、单轮、流式视频问答**场景，涵盖实时视觉感知、回溯追踪与前向主动响应三类任务（OVOBench 的三大子类）。HPSI 的高压缩率特性使其在**极端帧削减**（↓93.75% 帧保留）下仍保持竞争力——在 OVOBench 上以仅 6.25% 的原始帧实现 46.9% 的整体准确率，显著优于在线基准 Dispider 的 41.8%（Table 2）。同时，该方法能稳定处理最长约 120 分钟的视频流（VideoMME、LVBench 等离线长视频基准），且在 30% 帧丢失的压力测试下，StreamingBench 准确率仅从 71.60% 降至 67.81%（Table 5），显示出对帧缺失的强鲁棒性。

然而，当前方法存在明确的**模态局限**：仅处理视觉流，尚未集成音频或其他传感器信息，因此在需要多模态证据对齐的任务中可能无法发挥全部潜力。此外，尽管 HPSI 在 NVIDIA A100 GPU 上以极低延迟增量（13.2 ms vs. 基准 9.5 ms）实现了 78 倍的令牌吞吐量提升（Figure 8），但整个系统对**极端边缘设备**（如移动端 NPU）的适配尚未验证，实时推理时的内存占用和功耗仍是潜在障碍。

### 局限性

1. **模态单一**：ATDM 和 HPSI 均围绕视觉令牌设计，未考虑音频、文本流等多模态信息的统一聚合与证据对齐，限制了其在具身智能、多模态对话代理等场景中的直接应用。
2. **长期稳定性未充分验证**：虽然测试基准覆盖了最长 120 分钟的视频，但数小时乃至数天的持续流式输入下，HPSI 的记忆压缩是否会出现灾难性遗忘，以及 ATDM 的逐片段决策是否会积累误差漂移，均缺乏系统性评估。
3. **可解释性的质量受制于底层 LLM**：ATDM 的透明推理以文本化的中间字幕和子答案展开，其忠实度完全依赖基座 LLM 的指令遵循能力，在面临模糊查询或分布外数据时可能出现幻觉，导致 $\rho$ 和 $c$ 的估计失真，进而误导停止决策。
4. **推理延迟尚未达到真正的“实时”**：尽管令牌吞吐量显著提升，但整体推理仍然以片段为单位进行，对于需要毫秒级响应的在线应用（如自动驾驶、高频人机交互），端到端延迟仍需进一步降低。
5. **决策阈值缺乏自动校准**：ATDM 中判断“可回答”的进度与置信度阈值（如 $c\approx 0.5$ 为相关边界，$c>0.85$ 为充分边界）完全依赖经验设定，缺乏跨任务、跨领域的自适应调节机制，可能在新环境中引入不必要的等待或过早应答。

### 开放问题

1. **多模态记忆的深度分层**：能否将 HPSI 的“深度作为记忆”思想推广至多流输入，为音频、深度图等多种模态各自建立层次化聚合令牌，并通过轻量级门控在 Transformer 层间动态融合，从而构建统一的、可解释的跨模态认知状态？
2. **显式且经校准的内部信号**：$\rho$ 和 $c$ 目前仅为推理过程中的非标量产出，尚未经过严格的不确定性校准。能否发展出带置信区间的进度估计，使其成为通用推理代理中可信的“何时回答、等待或反思”的控制信号？
3. **基准测试的维度缺失**：当前主流评测（StreamingBench、OVOBench 等）仅评估最终答案的准确性，忽略了对响应时机和证据对齐质量的独立评分。构建能够综合评价准确率、响应偏差 $\delta$ 以及推理透明度多维度的新基准，将是推动该领域发展的关键。
4. **超长流与动态环境下的鲁棒性**：在数小时乃至数天的视频流中，HPSI 的因果压缩是否仍能维持实体关联？ATDM 的反思机制在话题漂移或场景剧变时能否及时自我校正？这些都需在更接近真实应用的持续学习设定下进行深度检验。
5. **与外部工具的协同**：ATDM 的透明推理流水线天然提供了可被外部系统解析的中间状态（子问题、子答案、进度与置信度）。能否将其与工具调用、记忆检索或知识图谱查询相结合，使在线视频助手不仅能理解“看到了什么”，还能主动执行“该做什么”，是拓展其应用边界的重要方向。



## 原文 PDF

![[paperPDFs/ICLR_2026/Progressive_Online_Video_Understanding_with_Evidence_Aligned_Timing_and_Transparent_Decisions.pdf]]
