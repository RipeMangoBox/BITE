---
title: "EVA: Efficient Reinforcement Learning for End-to-End Video Agent"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EVA_Efficient_Reinforcement_Learning_for_End_to_End_Video_Agent.pdf
project_link: null
code_link: null
aliases:
- EVA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 从‘先感知后推理’转变为‘先规划后感知’的范式，使智能体仅在文本查询阶段就决定观看什么、何时观看和如何观看。
primary_logic: 利用强化学习训练端到端视频智能体，通过迭代的总结-规划-行动-反思循环和灵活的帧选择工具，智能体能够自主分配视觉Token预算，在保持高精度的同时大幅减少计算量。
claims:
- 三阶段训练（SFT→KTO→GRPO）逐步提升性能，GRPO模型在多个基准上达到最优，同时减少帧消耗。
- 混合开放式和多选题数据的GRPO训练比单一类型数据更有效，防止奖励黑客行为。
- EVA在LSDbench上以6.2K视觉Token达到51.8%准确率，超越统一采样基线且Token使用显著更少。
- LSDBench 上 Acc (%) = 51.0
---

# EVA: Efficient Reinforcement Learning for End-to-End Video Agent

> [!tip] 核心洞察
> 利用强化学习训练端到端视频智能体，通过迭代的总结-规划-行动-反思循环和灵活的帧选择工具，智能体能够自主分配视觉Token预算，在保持高精度的同时大幅减少计算量。

| 字段 | 内容 |
|------|------|
| 中文题名 | EVA：面向端到端视频智能体的高效强化学习 |
| 英文题名 | EVA: Efficient Reinforcement Learning for End-to-End Video Agent |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.22918) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | EVA |
| Dataset | LSDBench, LongVideoBench, MLVU, VideoMME |

> [!tip] 效果简介
> - LSDBench 上，Acc (%) 51.0 vs 50.1 (Qwen2.5-VL, 256帧) (+0.9)。
> - LongVideoBench 上，Acc (%) 55.0 vs 52.9 (FrameThinker) (+2.1)。
> - MLVU 上，Acc (%) 68.3 vs 60.2 (Video-R1) (+8.1)。

## 概要

长视频理解面临一个根本瓶颈：主流多模态大模型（MLLM）将视频视为被动识别对象，采用统一帧采样策略，导致计算冗余严重且推理效率有限，无法自适应地聚焦于与查询相关的关键片段。**EVA** 针对这一瓶颈，提出从“先感知后推理”到**先规划后感知**的范式转变——智能体在仅接收文本查询的阶段就决定“看什么、何时看、如何看”，通过迭代的**总结–规划–行动–反思**循环和灵活的多参数帧选择工具，自主分配视觉Token预算，在保持高精度的同时大幅削减计算开销。

该方法以 **Qwen2.5-VL-7B-Instruct** 为基础模型，采用三阶段训练策略：监督微调（SFT）冷启动 → Kahneman–Tversky优化（KTO）偏好校正 → 组相对策略优化（GRPO）在线强化学习。GRPO阶段混合多项选择题与开放式问题数据进行训练，有效抑制奖励黑客行为。

核心实验结果：
- 在 **LSDbench**（采样困境基准）上，EVA 以约 6.2K 视觉Token达到 51.0% 准确率，超越统一采样基线 Qwen2.5-VL（50.1%，256帧），且Token消耗大幅降低（Table 1）。
- 在多个长视频理解基准上，EVA 相比通用 MLLM 基线提升 6–12%，相比先前自适应智能体方法（如 **FrameThinker**、**Video-R1**）提升 1–3%（Table 2）。具体而言，**LongVideoBench** 上达到 55.0%（+2.1% vs. FrameThinker），**MLVU** 上达到 68.3%（+8.1% vs. Video-R1），**VideoMME** 整体准确率 60.2%（+6.6% vs. Qwen2.5-VL）。
- 在幻觉基准 **ELV-Halluc** 上，EVA 将语义聚合幻觉比率（SAH Ratio）从 8.8% 降至 5.0%，同时取得最高的整体准确率（Table 4）。

消融实验证实，SFT → KTO → GRPO 三阶段训练逐步提升性能并降低帧/轮次消耗，GRPO 模型学会了更精打细算的多轮推理（Figure 4）；混合数据类型训练比单一类型数据更有效（Figure 5）。

**方法定位**：EVA 属于端到端视频智能体方法，与 **VideoAgent**（依赖手工设计流程）和 **FrameThinker**（固定工作流、有限帧选择灵活性）等早期智能体方法相比，其核心差异在于将主动视频理解形式化为马尔可夫决策过程（MDP），并通过强化学习端到端优化策略，而非依赖硬编码规则。与统一采样框架（如 Qwen2.5-VL、LongVA）相比，EVA 从“被动识别”转向“主动规划感知”，实现了视觉Token的动态分配。



视频理解正从静态图像分析向长视频推理快速演进。当视频时长从数十秒扩展到数千秒时，传统多模态大语言模型（MLLM）面临一个根本性瓶颈：**统一帧采样导致的冗余计算与有限推理效率**。现有方法将模型视为被动识别器——先对视频进行均匀采样，再将所有帧编码为视觉Token后输入模型进行推理。这种“先感知后推理”的范式在长视频场景下暴露了两个致命缺陷：

1. **信息密度与采样预算的错配**：长视频中关键信息往往稀疏地分布在少数片段中，但统一采样将计算资源平均分配到所有时间点，大量视觉Token被浪费在无关内容上。
2. **上下文窗口的硬约束**：MLLM的上下文长度有限，均匀采样意味着要么牺牲时间覆盖范围，要么被迫降低帧分辨率，二者均损害理解精度。

这种困境在极端长视频场景中尤为突出——例如一段超过6600秒的视频中，回答“角色完成了哪些动作序列”这样的问题，传统方法几乎不可能在有限Token预算内捕获所有相关片段（Figure 1）。

### 现有方法的缺口

近期工作尝试通过自适应智能体方法缓解上述问题。**VideoAgent**等早期智能体方法引入了外部工具调用，但仍依赖手工设计的固定工作流，缺乏灵活的帧选择能力。**FrameThinker**等自适应方法虽然实现了基本的帧选择，但其工具接口仅支持时间范围等有限参数，无法进行空间分辨率的动态调整，且工作流模式固化，难以根据查询复杂度自主决定“看什么、何时看、怎么看”。

另一条技术路线是基于强化学习的视频推理模型（如**Video-R1**），它们通过RL优化推理链，但本质上仍沿用统一采样的感知前端，未从根本上改变感知与推理的顺序关系。

### 本文动机：从被动识别到主动感知

上述方法的共同局限在于**感知先于推理**——模型在看到视频之前并不知道应该关注什么。EVA的核心动机是逆转这一范式：**让智能体在文本查询阶段就决定观看策略，再选择性获取视觉证据**。这一“先规划后感知”的范式转变，使智能体能够像人类一样，先形成关于“需要什么信息”的假设，再有针对性地观察视频，从而在保持高精度的同时大幅减少视觉Token消耗。

为实现这一目标，EVA引入了三个关键设计：
- **迭代的总结-规划-行动-反思循环**：智能体在多轮交互中逐步获取证据、评估信息充分性、决定是否继续探索。
- **灵活的多参数帧选择工具**：支持`start_time`、`end_time`、`nframes`、`resize`四个参数，实现时域和空域的联合动态调整。
- **三阶段强化学习训练策略**：从监督微调冷启动，到偏好优化纠正典型错误，再到在线强化学习自主探索最优感知策略。

这一框架将视频理解重新定义为**主动信息获取问题**，而非被动的内容识别任务，为长视频推理开辟了新的效率-精度平衡空间。



## 核心方法与创新机理

EVA 的核心创新在于将视频理解从**被动识别范式**扭转为**主动感知范式**，并通过强化学习赋予智能体自主分配视觉 Token 预算的能力。其关键变化槽位（changed slots）体现在三个层面：

### 1. 感知范式：从“先感知后推理”到“先规划后感知”

传统 MLLM 视频理解方法（如 Qwen2.5-VL 的统一采样框架）采用“先感知后推理”范式：先对视频进行均匀帧采样并编码为视觉 Token，再基于这些固定 Token 进行推理。这导致两个根本性问题：（1）冗余计算——大量帧与查询无关却被编码；（2）信息瓶颈——关键帧可能因采样稀疏而丢失。

EVA 提出了**先规划后感知**范式（Figure 1, Section 1）。智能体在仅获得文本查询的阶段就制定观察计划，决定“观看什么、何时观看、如何观看”，然后才调用帧选择工具进行定向感知。这一范式的因果机制在于：将视觉 Token 的分配决策从编码器端转移到策略端，使 Token 预算能够按需动态聚焦于与查询相关的时空区域。

### 2. 帧选择工具：从固定参数到灵活多参数控制

基线方法（如 FrameThinker、VideoAgent）的帧选择工具通常仅支持时间范围参数，缺乏空间分辨率的灵活控制。EVA 设计了一个**多参数帧选择工具**（Section 3.1），支持四个维度的动态调整：

| 参数 | 功能 |
|------|------|
| `start_time` | 起始时间戳 |
| `end_time` | 结束时间戳 |
| `nframes` | 采样帧数 |
| `resize` | 空间分辨率调整 |

这一工具设计使智能体能够在时间维度（何时看、看多长）、密度维度（看多少帧）和空间维度（以何种分辨率看）上联合优化视觉信息获取。例如，对于需要细节定位的任务，智能体可以选择高分辨率、少帧数；对于需要全局时序理解的任务，则选择低分辨率、多帧数。

### 3. 训练策略：从单一监督到三阶段强化学习

基线方法通常仅依赖监督微调（SFT）或手工规则。EVA 引入了**三阶段训练策略**（Figure 2）：

- **SFT 冷启动**：在合成数据上训练智能体掌握总结-规划-行动-反思的基本推理模式，使其学会工具调用的正确格式。
- **KTO 偏好优化**：利用单样本偏好标签，让模型从典型失败模式中学习，纠正错误行为倾向。
- **GRPO 在线强化学习**：采用 KL 正则化的策略优化目标，最大化复合奖励函数（精度奖励 + 格式奖励），使智能体在保持与参考策略接近的同时探索更优的帧选择策略。

消融实验（Table 2, Figure 4）证实了这一三阶段序列的有效性：SFT→KTO→GRPO 逐步提升性能，GRPO 模型学会了更精打细算的多轮推理，在保持甚至提升准确率的同时显著降低帧消耗。此外，GRPO 训练中混合多项选择题和开放式问题的数据比单一类型数据更有效，有效防止了奖励黑客行为（Figure 5）。



EVA 将主动视频理解问题形式化为一个**马尔可夫决策过程（MDP）**，并在此基础上构建了一个**先规划后感知**的端到端智能体框架。其核心工作流由四个模块构成的迭代循环驱动：**总结 → 规划 → 行动 → 反思**。

### 信念状态与策略参数化

在每个时间步 $t$，智能体维护一个信念状态：

$$
s _ { t } = \{ q , h _ { t } , F _ { t } \}
$$

其中 $q$ 为原始查询，$h_t$ 为交错文本与帧的历史记录，$F_t$ 为已获取的视觉证据集。智能体的策略 $\pi_{\boldsymbol{\theta}}(a_t \mid s_t)$ 由参数 $\boldsymbol{\theta}$ 决定，在给定当前状态 $s_t$ 时输出动作 $a_t$。

### 四模块迭代循环

1. **总结模块（Summary Module）**：基于已获取的帧生成视觉证据的接地描述，为后续决策提供事实基础。
2. **规划模块（Planning Module）**：根据当前信息提出潜在的动作方案，并估计每种动作的成本与预期结果。
3. **行动模块（Action Module / Tool Calling）**：调用灵活的帧选择工具，根据规划模块的输出从视频中提取关键帧。该工具支持多参数控制——`start_time`、`end_time`、`nframes`、`resize`——实现时间维度和空间分辨率的动态调整。
4. **反思模块（Reflection Module）**：评估当前已获取的视觉信息是否足以回答问题；若不足，则触发下一轮探索，否则输出最终答案。

### 范式转变

与传统MLLM采用的“先感知后推理”（统一采样帧后再进行推理）不同，EVA 在仅见到文本查询的阶段即开始制定观看计划，决定**看什么、何时看、如何看**。这一“先规划后感知”的范式使智能体能够自主分配视觉 Token 预算，在长视频场景中大幅减少冗余计算，同时保持甚至提升推理精度（见 Figure 1）。

### 三阶段训练流水线

EVA 的训练并非一步到位，而是通过三个递进阶段逐步塑造智能体的规划与工具调用能力（见 Figure 2）：

![[assets/figures/papers/paper_list_l2310_https_arxiv_org_abs_2603_22918/figures/003_Figure_2.jpg]]
*Figure 2: Data Pipeline and Training Stage of EVA. The base model is first fine-tuned on synthetic dataset with certain reasoning and tool-calling pattern. Then we use KTO to help the model learn from typical failures. Finally, we introduce a Data-Enhanced Multi-Stage GRPO training pipeline, where we collect the failure cases of current policy and employ an teacher MLLM to generate new open-ended video QA dataset*

- **阶段一：SFT 冷启动**——使用合成的监督微调数据，使基座模型初步掌握总结-规划-行动-反思的标准推理格式与工具调用模式。
- **阶段二：KTO 偏好优化**——利用单样本偏好标签，让模型从典型失败案例中学习，纠正不良行为。
- **阶段三：GRPO 在线强化学习**——通过 KL 正则化的策略优化目标，结合复合奖励函数（精度奖励 + 格式奖励），在真实采样中进一步优化策略。

这一流水线的设计使 EVA 从“学会格式”到“学会纠错”再到“学会精打细算”，逐步获得高效的多轮推理能力。

### 补充图表

![[assets/figures/papers/paper_list_l2310_https_arxiv_org_abs_2603_22918/figures/012_Figure_8.jpg]]
*Figure 8: Cold Start Data Pipeline*



### 2.1 先规划后感知的MDP形式化

EVA将主动视频理解问题形式化为一个马尔可夫决策过程（MDP）。智能体在时刻 $t$ 的信念状态定义为：

$$s _ { t } = \{ q , h _ { t } , F _ { t } \}$$

其中 $q$ 为用户查询，$h_t$ 为交错文本-帧的交互历史，$F_t$ 为已获取的视觉证据帧集合。策略 $\pi_{\boldsymbol{\theta}}$ 以信念状态为条件输出动作 $a_t$：

$$\pi _ { \boldsymbol { \theta } } { \left( a _ { t } \ \middle | \ s _ { t } \right) }$$

这一形式化的核心突破在于：智能体并非在感知全部视频后再推理，而是从查询 $q$ 出发，在每一轮迭代中根据当前信念状态自主决定“看什么、何时看、怎么看”，从而将视觉Token预算动态分配到关键时空片段。

### 2.2 迭代式推理循环的四个模块

EVA的推理过程由四个功能模块构成迭代循环，每个模块对应SFT数据实例中的一个字段：

- **总结模块（Summary Module）**：对已获取的帧集合 $F_t$ 进行描述，将视觉证据接地为文本摘要，为后续规划提供信息基础。
- **规划模块（Planning Module）**：基于当前信念状态 $s_t$，提出潜在动作选项，并估计各动作的成本与预期结果。该模块体现了“先规划后感知”的决策逻辑——在调用视觉工具前先进行推理规划。
- **动作模块（Action Module / Tool Calling）**：调用帧选择工具执行具体感知动作。工具接口提供四个参数：`start_time`（起始时间）、`end_time`（结束时间）、`nframes`（帧数）、`resize`（分辨率调整），支持时域和空域的动态控制。这一灵活的工具设计使智能体能够根据规划结果精确调整视觉采样的粒度和范围。
- **反思模块（Reflection Module）**：评估当前视觉信息是否足以回答问题，决定是终止推理并输出答案，还是继续下一轮探索。

四个模块形成“总结→规划→动作→反思”的闭环，使智能体能够在多轮交互中逐步积累视觉证据，而非一次性处理大量冗余帧。

### 2.3 三阶段训练策略与优化目标

EVA采用三阶段训练流水线，逐步提升智能体的推理能力和Token效率：

1. **SFT冷启动**：在合成数据集上进行监督微调，使基座模型（Qwen2.5-VL-7B-Instruct）初步掌握工具调用格式和推理模式。每个SFT实例遵循“总结+规划+动作+反思”的结构化格式。
2. **KTO偏好优化**：利用Kahneman–Tversky优化框架，从典型失败案例中学习。KTO仅需单样本偏好标签，无需成对比较数据，用于在GRPO之前修正明显的策略偏差。
3. **GRPO在线强化学习**：采用Group Relative Policy Optimization进行最终的策略优化。GRPO的优化目标为KL正则化的期望回报最大化：

$$\operatorname* { m a x } _ { \theta } \ \mathbb { E } _ { \tau \sim \pi _ { \theta } } \big [ R ( \tau ) \big ] - \lambda \mathbb { E } _ { ( s , a ) \sim \pi _ { \theta } } [ \mathrm { K L } ( \pi _ { \theta } ( \cdot \vert s ) \| \pi _ { \mathrm { r e f } } ( \cdot \vert s ) ) ]$$

其中第一项鼓励高回报行为，第二项通过KL散度约束策略不偏离参考模型 $\pi_{\mathrm{ref}}$ 过远，$\lambda$ 控制正则化强度。

### 2.4 复合奖励函数设计

针对视频问答中多选题和开放式问题并存的特性，EVA设计了复合奖励函数：

$$R ( \tau ) = w _ { \mathrm { a c c } } r _ { \mathrm { a c c } } + w _ { \mathrm { f m t } } r _ { \mathrm { f m t } }$$

其中 $w_{\mathrm{acc}}$ 和 $w_{\mathrm{fmt}}$ 分别为精度奖励和格式奖励的权重。精度奖励根据问题类型自适应切换：

$$r _ { \mathrm { a c c } } = { \left\{ \begin{array} { l l } { r _ { \mathrm { c s v } } , } & { { \mathrm { i f ~ m u l t i p l e - c h o i c e } } , } \\ { r _ { \mathrm { r o u g e } } , } & { { \mathrm { i f ~ o p e n - e n d e d } } . } \end{array} \right. }$$

- 多选题使用CSV判定（$r_{\mathrm{csv}}$），即二元正确/错误信号。
- 开放式问题使用ROUGE分数，具体为ROUGE-1、ROUGE-2、ROUGE-L F1分数的平均值：

$$r _ { \mathrm { r o u g e } } = \frac { 1 } { 3 } \big ( R _ { 1 } + R _ { 2 } + R _ { L } \big )$$

格式奖励 $r_{\mathrm{fmt}}$ 用于约束模型输出符合工具调用和推理循环的结构化格式。消融实验表明，混合多选题和开放式数据的GRPO训练比单一类型数据更有效，能防止模型通过猜测答案来获取奖励（奖励黑客行为）。

### 补充图表

![[assets/figures/papers/paper_list_l2310_https_arxiv_org_abs_2603_22918/figures/011_Figure_7.jpg]]
*Figure 7: The advantage of plan before perception matters*

![[assets/figures/papers/paper_list_l2310_https_arxiv_org_abs_2603_22918/figures/002_Table.jpg]]



## 实验与关键发现

### 核心实验设置

EVA以**Qwen2.5-VL-7B-Instruct**为基础模型，采用三阶段训练策略：监督微调（SFT）冷启动、KTO偏好校正、GRPO在线强化学习。SFT阶段训练2个epoch，批次大小为8，学习率2e-6；GRPO阶段训练1个epoch，批次大小为64，每样本采样8条轨迹，学习率1e-6，部署于32块H100 GPU。视觉Token估算采用每帧650 tokens的近似假设，以便与统一采样基线进行公平比较。

### 主结果分析

**采样困境基准（LSDbench）** 是检验EVA核心能力的关键战场。该基准专门考察模型在极长视频中面对“采样困境”时的表现——即如何在有限的视觉Token预算下定位关键信息。如Table 1所示，EVA以仅**6.2K视觉Token**达到**51.8%**准确率，超越了使用256帧统一采样的Qwen2.5-VL基线（50.1%），且Token消耗显著更低。这一结果直接验证了“先规划后感知”范式的有效性：智能体通过文本查询阶段即决定观看什么、何时观看，从而将Token精准分配到关键片段，而非在冗余帧上浪费计算。

在多个通用视频理解基准上，EVA展现出跨基准的稳健提升（Table 2）：
- **LongVideoBench**：55.0%（vs. FrameThinker 52.9%，+2.1%）
- **MLVU**：68.3%（vs. Video-R1 60.2%，+8.1%）
- **VideoMME**：60.2%（vs. Qwen2.5-VL 53.6%，+6.6%）
- **LVBench**：43.3%（vs. Video-R1 35.3%，+8.0%）

![[assets/figures/papers/paper_list_l2310_https_arxiv_org_abs_2603_22918/figures/006_Table_2.jpg]]
*Table 2: Main performance on multiple video understanding benchmark. Baseline results are directly cited from [17].The number of frames for EVA, which is indicated by *, is estimated by assuming 650 visual tokens per frame for fair comparison; the actual number of frames may vary depending on the resolution determined by the model adaptively*

值得注意的是，EVA在MLVU和LVBench上相对Video-R1的8%以上提升尤为突出，表明基于GRPO的端到端强化学习比依赖手工规则的推理方法更能适应长视频的复杂时空推理需求。

在**视频推理基准Video-Holmes**（Table 3）上，EVA在零样本设定下展现了较强的时序因果推理（TCI）和社会推理（SR）能力，进一步验证了迭代总结-规划-行动-反思循环对深层语义理解的促进作用。

![[assets/figures/papers/paper_list_l2310_https_arxiv_org_abs_2603_22918/figures/007_Table_3.jpg]]
*Table 3: Zero-shot performance on video reasoning benchmark: Video-Holmes [8], where SR stands for Social Reasoning; IMC stands for Intention & Motive Chaining; TCI stands for Temporal Causal Inference; TA Timeline Analysis; MHR stands for Multimodal Hint Reasoning; PAR stands for Physical Anomaly Reasoning; CTI stands for Core Theme Inference*

**幻觉控制**方面，EVA在ELV-Halluc基准上取得了**5.0%的SAH比率**（Table 4），显著低于Qwen2.5-VL-7B的8.8%。SAH比率越低，表明模型跨视频与视频内的语义聚合幻觉越少。这一优势源于EVA的信念状态机制：智能体在每轮交互中接地视觉证据，通过反思模块评估信息充分性后再决定是否继续探索，从而抑制了无根据的语义推测。

### 消融研究：训练阶段的因果贡献

三阶段训练的消融实验揭示了各阶段的因果作用（Table 2, Figure 4）：

![[assets/figures/papers/paper_list_l2310_https_arxiv_org_abs_2603_22918/figures/009_Figure_4.jpg]]
*Figure 4: Distribution of Rounds and Visual Token cross Models and Benchmarks*

1. **SFT冷启动**奠定了基本的工具调用和推理格式能力，但模型仍倾向于单轮快速回答，视觉Token分配不够精细。
2. **KTO偏好校正**通过从典型失败案例中学习，初步抑制了急躁回答行为，使模型开始尝试多轮探索。
3. **GRPO在线强化学习**是性能跃升的关键驱动力。GRPO模型学会了更审慎的多轮推理策略——在每轮中更精确地分配视觉Token预算，而非一次性采样大量帧。Figure 4的轮次与Token分布统计表明，GRPO训练的智能体在不同基准上均展现出灵活的Token分配模式，根据问题复杂度动态调整探索深度。

**数据混合策略的消融**（Figure 5）进一步揭示：GRPO训练中混合多项选择题（MC）和开放式问题（OE）数据比单一类型数据更有效。仅使用MC数据时，模型倾向于猜测答案（奖励黑客行为）；仅使用OE数据时，模型缺乏结构化判定的训练信号。混合数据提供了更丰富的学习环境，迫使智能体在两种监督形式下均发展出稳健的推理能力。

### 失败模式与局限性

尽管EVA在多个基准上取得显著提升，分析揭示了以下局限：

1. **工具接口的刚性约束**：当前推理循环依赖预定义的帧选择工具（start_time, end_time, nframes, resize），虽然比统一采样灵活，但在面对极端噪声或分布外查询时，固定的参数空间可能不足以表达最优观察策略。
2. **计算资源与奖励敏感性**：GRPO训练需要32块H100 GPU，且对奖励设计较为敏感。复合奖励中精度奖励和格式奖励的权重（$w_{acc}$和$w_{fmt}$）需要仔细调参，否则可能导致策略偏离预期行为。
3. **教师模型偏差**：SFT和KTO数据依赖教师模型生成，可能引入分布偏差，影响模型在真实场景中的泛化能力。Figure 3的训练数据分布显示数据集中于特定视频类型和查询模式，暗示覆盖度可能不足。
4. **Token估算近似**：视觉Token计算采用每帧650 tokens的假设，实际消耗因帧分辨率和内容复杂度而异，可能影响效率比较的精度。

### 关键图表结论

- **Table 1**：EVA在LSDbench上以6.2K Token达到51.8%，证明“先规划后感知”范式在极长视频中比统一采样更高效。
- **Table 2**：三阶段训练递进提升性能，GRPO模型在多个基准上达到最优，同时帧消耗低于SFT/KTO阶段。
- **Figure 4**：GRPO训练的智能体学会了多轮精细推理，Token分配随问题复杂度动态调整。
- **Figure 5**：混合MC+OE数据的GRPO训练防止奖励黑客行为，是性能提升的必要条件。
- **Table 4**：EVA在ELV-Halluc上的低SAH比率（5.0%）表明信念状态机制有效抑制了语义聚合幻觉。

![[assets/figures/papers/paper_list_l2310_https_arxiv_org_abs_2603_22918/figures/005_Table_1.jpg]]
*Table 1: Performance on sampling dilemma bench. We report different stages of EVA model’s performance on LSDbench. SOTA model performance are directly from [17]. The visual token are roughly measured by 258, 144 ,256 and 650 token per frame for gemini, LongVA, LongVila and Qwen-VL family models*

![[assets/figures/papers/paper_list_l2310_https_arxiv_org_abs_2603_22918/figures/010_Figure_5.jpg]]
*Figure 5: Ablation study on the GRPO training dataset. The comparison between multi-choice (MC) only, open-ended (OE) only, and mixed (MC+OE) data shows that mixed data provides a more effective learning environment for the agent, which leads to better performance on VideoMME*

### 补充图表

![[assets/figures/papers/paper_list_l2310_https_arxiv_org_abs_2603_22918/figures/008_Figure_6.jpg]]
*Figure 6: Diverse Workflows generated by EVA*

![[assets/figures/papers/paper_list_l2310_https_arxiv_org_abs_2603_22918/figures/014_Figure_9.jpg]]
*Figure 9: EVA statistics across rounds*




## 定位与知识库关联

### 1. 范式转变：从“先感知后推理”到“先规划后感知”

EVA 的核心贡献在于对视频理解任务中感知与推理顺序的根本性重构。传统多模态大语言模型（MLLM），如 **Qwen2.5-VL**，采用“先感知后推理”范式：先将视频统一采样为固定数量的帧，再基于这些帧进行推理。这一范式在长视频场景下面临两个结构性瓶颈：（1）统一采样导致关键信息可能被遗漏，而大量冗余帧消耗了宝贵的视觉 Token 预算；（2）模型缺乏对“观看什么”的自主决策能力，始终是被动的信息接收者。

EVA 将这一范式颠倒为“先规划后感知”。智能体在仅接收文本查询的阶段，就通过规划模块决定需要观看哪些时间片段、以何种分辨率观看、以及需要多少帧。这一转变的本质是将视频理解从“识别问题”重新定义为“序列决策问题”——智能体通过迭代的总结–规划–行动–反思循环，逐步收集证据，直至信息充分后才给出最终答案。该范式与 **FrameThinker** 等早期自适应方法的关键区别在于：FrameThinker 仍采用固定的工作流模板，帧选择灵活性有限；而 EVA 将整个交互过程建模为马尔可夫决策过程（MDP），使智能体能够根据信念状态动态调整策略。

### 2. 与现有智能体方法的谱系关系

EVA 处于视频理解智能体方法演进的关键节点。早期工作如 **VideoAgent** 率先将工具调用引入视频理解，通过调用外部检测器或检索器获取信息，但其工作流依赖手工设计的规则，缺乏端到端的学习能力。**FrameThinker** 进一步实现了自适应帧选择，但其工具接口仅支持时间范围参数，无法进行空间分辨率的动态调整。

EVA 在此基础上实现了三个关键升级：

- **工具接口的完备化**：帧选择工具支持 `start_time`、`end_time`、`nframes`、`resize` 四个参数，同时控制时间范围、帧密度和空间分辨率，使智能体能够在“粗略扫描”与“精细观察”之间灵活切换。
- **端到端的强化学习训练**：不同于依赖手工规则的先前方法，EVA 通过三阶段训练（SFT 冷启动 → KTO 偏好优化 → GRPO 在线强化学习）使智能体自主学会最优的视觉信息收集策略。
- **与通用 MLLM 的深度集成**：EVA 以 **Qwen2.5-VL-7B-Instruct** 为基础模型，将规划、工具调用、反思等能力直接融入模型权重，而非作为外部模块挂载。

与同期基于强化学习的视频推理模型 **Video-R1** 相比，EVA 的差异化优势在于显式的工具调用机制。Video-R1 主要依赖模型内部的链式推理，而 EVA 通过实际的帧提取动作与环境交互，使推理过程具有可验证的视觉接地。

### 3. 适用边界与局限性

EVA 的适用场景具有明确的边界条件：

- **长视频理解优势显著**：在超过 6600 秒的超长视频上，EVA 能够以极少的视觉 Token 达到与统一采样方法相当或更优的精度。在 LSDbench 上，EVA 仅使用 6.2K 视觉 Token 即达到 51.8% 准确率，而统一采样基线需要数倍于此的 Token 量。
- **工具接口的封闭性**：当前推理循环依赖预定义的帧选择工具，智能体无法自主发明新的感知动作类型。在面对需要音频分析、文本 OCR 定位等跨模态需求时，框架的扩展性受限。
- **训练资源与奖励敏感性**：GRPO 训练阶段需要 32 块 H100 GPU，且对奖励函数设计较为敏感。复合奖励中精度奖励与格式奖励的权重配比直接影响智能体的行为模式。
- **教师模型依赖**：SFT 和 KTO 阶段的训练数据由教师模型生成，可能引入系统性偏差，影响模型在分布外查询上的泛化能力。

### 4. 开放问题与未来方向

EVA 开辟了若干值得深入探索的方向：

- **工具生态的扩展**：如何将框架从单一的帧选择工具扩展到更丰富的感知动作空间（如目标检测、OCR、音频分析），使智能体能够根据查询需求自主组合多种工具？
- **去教师化的自我探索**：能否在不依赖教师模型生成训练数据的情况下，通过环境反馈和内在奖励驱动智能体自主发现有效的感知策略？
- **视觉 Token 的进一步压缩**：在多轮交互中，已获取的视觉信息如何被高效压缩为记忆表征，避免重复编码相同的帧内容？
- **跨模态记忆与迁移**：如何将一次视频理解任务中积累的视觉知识迁移到相关任务，实现跨查询的记忆共享？

这些问题的解决将推动视频理解智能体从“单次查询–单次响应”走向“持续学习–累积理解”的新阶段。



## 原文 PDF

![[paperPDFs/CVPR_2026/EVA_Efficient_Reinforcement_Learning_for_End_to_End_Video_Agent.pdf]]
