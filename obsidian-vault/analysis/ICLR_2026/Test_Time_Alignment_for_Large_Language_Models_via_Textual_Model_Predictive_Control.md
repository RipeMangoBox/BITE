---
title: "Test-Time Alignment for Large Language Models via Textual Model Predictive Control"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Test_Time_Alignment_for_Large_Language_Models_via_Textual_Model_Predictive_Control.pdf
aliases:
- TMPCT
- TTALLMTMPC
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning
core_operator: "用文本模型预测控制在测试时滚动搜索高奖励子目标。"
primary_logic: "TMPC从冻结LLM rollout中事后识别高奖励文本片段写入缓冲，再以子目标条件化重生成来稳定改进输出。"
claims:
- "TMPC把测试时对齐建模为轨迹优化，平衡token级引导的horizon诅咒和整段重写的维度诅咒。"
- "事后子目标识别和子目标条件重生成两个原则的消融都会明显降低奖励。"
- "TMPC无需微调参数，在翻译、长回复和MBPP程序合成任务上优于多种测试时基线。"
- "方法对缓冲大小、段长、奖励噪声和阈值变化表现出较强鲁棒性。"
---

# Test-Time Alignment for Large Language Models via Textual Model Predictive Control

> [!tip] 核心洞察
> 将测试时对齐重新建模为轨迹优化问题，并借鉴控制理论中的模型预测控制（MPC），通过滚动时域控制和子目标缓冲来平衡horizon诅咒与维度诅咒，无需微调模型参数。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过文本模型预测控制实现大语言模型测试时对齐 |
| 英文题名 | Test-Time Alignment for Large Language Models via Textual Model Predictive Control |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=DsS3xRPSs5); [Project](https://rl-bandits-lab.github.io/TMPC/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning |
| Method | Textual Model Predictive Control (TMPC) |
| Dataset | WMT'24 Discourse-Level Literary Translation (zh→en), WMT'24 Discourse-Level Literary Translation (zh→de), WMT'24 Discourse-Level Literary Translation (zh→ru), MBPP Program Synthesis |

> [!tip] 效果简介
> - WMT'24 Discourse-Level Literary Translation (zh→en) 上，SEGALE_comet 为 94.62，对比 94.58 (GPT-4o)，变化 +0.04。
> - WMT'24 Discourse-Level Literary Translation (zh→de) 上，SEGALE_comet 为 91.73，对比 91.70 (GPT-4o)，变化 +0.03。
> - WMT'24 Discourse-Level Literary Translation (zh→ru) 上，SEGALE_comet 为 91.53，对比 93.74 (GPT-4o)，变化 -2.21。

## 概述

本文提出**Textual Model Predictive Control (TMPC)**，一种新颖的测试时对齐框架，旨在解决大型语言模型在测试阶段的对齐问题。TMPC将文本生成重新建模为轨迹优化问题，并借鉴控制理论中的模型预测控制（MPC），通过滚动时域控制和子目标缓冲来平衡两种现有测试时对齐方法的核心缺陷：引导解码（guided decoding）面临的“horizon诅咒”和迭代优化（iterative refinement）面临的“维度诅咒”。TMPC无需微调模型参数，仅通过冻结的LLM作为提议分布，在三个具有不同边界特征的任务上进行了评估：WMT'24语篇级机器翻译、HH-RLHF长回复子集和MBPP程序合成。实验结果表明，TMPC在zh→en翻译上达到94.62 SEGALE_comet，优于包括GPT-4o（94.58）在内的所有基线；在MBPP程序合成上达到61% pass rate，优于Best-of-35和TPO；在长回复生成上平均奖励和GPT-4胜率均优于DPO和Best-of-20。

## 背景与动机

### 2.1 测试时对齐的根本挑战

大型语言模型（LLMs）在训练后仍可通过测试时计算进一步提升输出质量。然而，现有测试时对齐方法面临两个根本性挑战：

- **Horizon诅咒**：当动作定义为token级别（如引导解码）时，长轨迹上的信用分配不可靠，方法难以在长序列中有效分配奖励。
- **维度诅咒**：当动作为响应级别（如迭代优化）时，每次重写整个序列导致搜索空间巨大且不稳定。


### 2.2 现有方法的局限性

现有测试时对齐方法可分为三类：

- **训练时对齐方法**（如DPO、SimPO、RLHF）：需要微调模型参数，计算成本高且可能遗忘预训练知识。
- **引导解码方法**（如ARGS、RE-Control）：在token级别操作，受horizon诅咒影响。
- **迭代优化方法**（如TPO）：在响应级别操作，受维度诅咒影响。

### 2.3 核心洞察

TMPC的核心洞察在于：将测试时对齐重新建模为轨迹优化问题，并借鉴控制理论中的模型预测控制（MPC），通过滚动时域控制和子目标缓冲来平衡horizon诅咒与维度诅咒，无需微调模型参数。

## 核心创新

TMPC引入两个核心原则来解决上述权衡：

1. **事后子目标识别（Hindsight Subgoal Identification）**：从模型rollout中回顾性地识别高奖励中间输出作为子目标，存入缓冲B。这一原则允许TMPC发现有意义的规划步骤。

2. **子目标条件重生成（Subgoal-Conditioned Re-Generation）**：利用缓冲B中的子目标条件化新rollout的生成，确保稳定累积改进。这一原则确保稳定的、累积的进展。

## 整体框架

![[assets/figures/papers/iclr26_0002_DsS3xRPSs5_Test-Time_Alignment_for_Large_Language_Models_vi/figures/001_Figure_1.jpg]]
*Figure 1: Textual Model Predictive Control (TMPC) balances the curse of horizon in guided decoding against the curse of dimensionality in naive iterative refinement. It employs Hindsight Subgoal Identification to dynamically discover promising states from rollouts and Subgoal-Conditioned Re-Generation to guide the search from these discovered subgoals, ensuring a stable alignment.*

TMPC的整体框架如图1所示，它通过两个核心原则平衡引导解码的horizon诅咒与迭代优化的维度诅咒。

![[assets/figures/papers/iclr26_0002_DsS3xRPSs5_Test-Time_Alignment_for_Large_Language_Models_vi/figures/001_Figure_1.jpg]]

图2展示了TMPC框架的详细流程，包括事后子目标识别和子目标条件重生成两个核心原则。

![[assets/figures/papers/iclr26_0002_DsS3xRPSs5_Test-Time_Alignment_for_Large_Language_Models_vi/figures/002_Figure_2.jpg]]

## 核心模块与公式推导

### 5.1 问题形式化

文本生成被形式化为一个有限horizon马尔可夫决策过程（MDP）：

$$\bar { \mathcal { M } } \overset { = } ( \mathcal { S } , \mathcal { A } , \mathcal { P } , R , \bar { \mu , T } )$$

其中状态空间S、动作空间A、转移函数P、奖励函数R、初始状态分布μ和episode长度T。转移函数是确定性的：$P(s_{t+1} | s_t, a_t) = 1$。

轨迹τ的累积奖励定义为：

$$\mathcal { I } ( \tau ) : = \sum _ { t = 0 } ^ { T - 1 } R ( s _ { t } , a _ { t } )$$

测试时对齐的目标是搜索最优动作序列以最大化总奖励：

$$\pmb { a } ^ { * } ( s _ { 0 } ) : = \arg \operatorname* { m a x } _ { \pmb { a } _ { 0 : T - 1 } } \sum _ { t = 0 } ^ { T - 1 } R ( s _ { t } , a _ { t } )$$

### 5.2 MPC动作选择

标准MPC在步骤t通过优化horizon H内的局部问题来确定动作：

$$a ^ { \mathrm { M P C } } ( s _ { t } ) : = \arg \operatorname* { m a x } _ { \substack { a _ { t : t + H - 1 } } } \quad \sum _ { i = t } ^ { t + H - 1 } R ( s _ { t } , a _ { t } )$$

### 5.3 TMPC聚合函数

TMPC定义聚合函数G，根据多个文本rollout及其累积奖励确定动作序列：

$$\pmb { a } ^ { \mathrm { T M P C } } ( s )  \mathcal { G } \Big ( \{ \tau ^ { ( i ) } \} _ { i = 1 } ^ { K } , \{ \mathcal { I } ( \tau ^ { ( i ) } ) \} _ { i = 1 } ^ { K } ; s \Big )$$

### 5.4 事后子目标识别（缓冲更新规则）

事后子目标识别将高奖励动作加入缓冲B；若缓冲已满，则替换奖励较低的动作：

$$\mathcal { B }  \{ \begin{array} { l l } { \mathcal { B } \cup \widetilde { \mathfrak { a } } _ { t } ^ { \mathrm { T M P C } } ( s ) , } & { \mathrm { i f ~ } | \mathcal { B } | < \mathrm { c a p a c i t y } , } \\ { \mathcal { B } \setminus \{ a \in \mathcal { B } \mid R ( s , a ) < R ( s , a ^ { \prime } ) \} \cup \{ a ^ { \prime } \} , } & { \mathrm { o t h e r w i s e } , \mathrm { f o r ~ e a c h ~ } a ^ { \prime } \in \widetilde { \mathfrak { a } } _ { t } ^ { \mathrm { T M P C } } ( s ) . } \end{array}$$

### 5.5 子目标条件聚合

从子目标条件化LLM生成的rollout中选择奖励≥阈值α的动作：

$$\widetilde {  Ḋ \boldsymbol Ḋ a Ḍ Ḍ } _ { t } ^ { \mathrm { T M P C } } ( s ) \gets  { \mathcal Ḋ G Ḍ } \left( \{ \tau _ { t } ^ { ( i ) } \} _ { i = 1 } ^ { K } , R ( \cdot ) ~ | ~ s ,  { \mathcal Ḋ B Ḍ } \right) : = \left\{  { \boldsymbol Ḋ a Ḍ } ~ | ~ R ( s , a ) \geq \alpha ~ \mathrm { a n d } ~ a \in \{ \tau _ { t } ^ { ( i ) } \} _ { i = 1 } ^ { K } \right\}$$

## 实验与分析

### 6.1 主要结果

**WMT'24语篇级文学翻译（zh→xx方向）**

Table 1展示了TMPC在WMT'24文学翻译任务上的定量结果。


![[assets/figures/papers/iclr26_0002_DsS3xRPSs5_Test-Time_Alignment_for_Large_Language_Models_vi/figures/003_Table_1.jpg]]
*Table 1: Results on the WMT’24 literary translation shared task (zh→xx directions). Results are grouped into SoTA and base models, training-time alignment methods, and test-time alignment methods. For test-time methods, the best-performing results are bold, and the second-best are underlined. Proposed methods are highlighted .*

![[assets/figures/papers/iclr26_0002_DsS3xRPSs5_Test-Time_Alignment_for_Large_Language_Models_vi/figures/003_Table_1.jpg]]

| 方向 | 方法 | SEGALE_comet | NA Ratio |
|------|------|-------------|----------|
| zh→en | **TMPC** | **94.62** | **0.00** |
| zh→en | GPT-4o | 94.58 | 0.00 |
| zh→de | **TMPC** | **91.73** | **0.00** |
| zh→de | GPT-4o | 91.70 | 0.00 |
| zh→ru | GPT-4o | 93.74 | 0.00 |
| zh→ru | **TMPC** | 91.53 | 0.00 |

TMPC在zh→en方向表现最强（骨干模型语言熟悉度更高），在zh→ru方向弱于GPT-4o（骨干模型俄语能力较弱）。

**长回复生成**

Figure 3展示了长回复生成的结果：左图为平均奖励，右图为GPT-4胜率。

![[assets/figures/papers/iclr26_0002_DsS3xRPSs5_Test-Time_Alignment_for_Large_Language_Models_vi/figures/004_Figure_3.jpg]]

TMPC在平均奖励和GPT-4胜率上均优于DPO和Best-of-20。

**MBPP程序合成**

Figure 4展示了MBPP程序合成上的pass rate比较。

![[assets/figures/papers/iclr26_0002_DsS3xRPSs5_Test-Time_Alignment_for_Large_Language_Models_vi/figures/006_Figure_4.jpg]]

TMPC达到61% pass rate，优于所有基线（Best-of-35、TPO）。

### 6.2 消融与鲁棒性分析

Table 2展示了TMPC的鲁棒性和敏感性分析。


![[assets/figures/papers/iclr26_0002_DsS3xRPSs5_Test-Time_Alignment_for_Large_Language_Models_vi/figures/007_Table_2.jpg]]
*Table 2: Robustness and sensitivity of TMPC. (a) Robustness to hyperparameter choices, with performance varying by less than 0.1 across different buffer and segment sizes. (b) Robustness to imperfections in the reward model, including injected noise and lower accuracy. (c) Robustness to the threshold used for selecting high-reward segments. (d) Ablation of TMPC’s two principles. Removing Principle 1 is approximated by disabling hindsight and making the buffer FIFO (First-In-First-Out); removing Principle 2 is approximated by minimizing subgoal conditioning (buffer size = 1).*

![[assets/figures/papers/iclr26_0002_DsS3xRPSs5_Test-Time_Alignment_for_Large_Language_Models_vi/figures/007_Table_2.jpg]]

关键发现：

- **移除原则1（事后排序）**导致平均奖励从4.595骤降至4.264。
- **移除原则2（子目标条件化，缓冲大小=1）**导致平均奖励从4.595降至4.393。
- TMPC对超参数选择鲁棒：缓冲和段大小变化导致平均奖励变化小于0.1。
- TMPC对奖励模型质量鲁棒：使用较弱RM（77.54%准确率）时平均奖励为4.332，注入噪声（sigma=1）时为4.457。
- TMPC对阈值α鲁棒：α=3时平均奖励4.573，α=5时4.584。

### 6.3 计算成本

Table 6展示了生成单个HH-RLHF长回复的端到端延迟和吞吐量。

![[assets/figures/papers/iclr26_0002_DsS3xRPSs5_Test-Time_Alignment_for_Large_Language_Models_vi/figures/012_Table_6.jpg]]

| 方法 | 延迟（秒/响应） | 吞吐量（响应/分钟） |
|------|----------------|-------------------|
| BaseLLaMA-3.1-8B | 8 | 7.50 |
| RE-Control | 40 | 1.50 |
| **TMPC** | **108** | **0.55** |
| ARGS | 363 | 0.17 |
| RAIN | 1930 | 0.03 |

TMPC的计算成本为每响应108秒，高于BaseLLaMA（8秒）和RE-Control（40秒），但低于ARGS（363秒）和RAIN（1930秒）。K个候选rollout可高度并行化。

### 6.4 与固定边界启发式方法的比较

Table 5展示了与固定边界启发式方法在WMT'24段落级MT上的比较。


![[assets/figures/papers/iclr26_0002_DsS3xRPSs5_Test-Time_Alignment_for_Large_Language_Models_vi/figures/011_Table_5.jpg]]
*Table 5: Comparison with fixed-boundary heuristics on WMT’24 paragraph-level MT. Sentence-level systems translate or rewrite each sentence independently with fixed boundaries. TMPC dynamically identifies hindsight subgoals at test time, which may cross sentence boundaries.*

![[assets/figures/papers/iclr26_0002_DsS3xRPSs5_Test-Time_Alignment_for_Large_Language_Models_vi/figures/011_Table_5.jpg]]

TMPC动态识别事后子目标，可能跨越句子边界，优于固定边界的句子级方法。

### 6.5 迭代性能

Figure 5展示了zh→en翻译的迭代性能，说明TMPC原则的重要性。

![[assets/figures/papers/iclr26_0002_DsS3xRPSs5_Test-Time_Alignment_for_Large_Language_Models_vi/figures/008_Figure_5.jpg]]

### 6.6 公平性说明

- 所有方法使用相同的LLaMA-3.1-8B-Instruct骨干模型进行公平比较。
- 翻译任务中，TMPC在zh→en方向表现最强（骨干模型语言熟悉度更高），在zh→ru方向弱于Tower-7B（骨干模型俄语能力较弱）。
- 计算成本：TMPC在HH-RLHF长回复生成上每响应108秒，高于BaseLLaMA（8秒）和RE-Control（40秒），但低于ARGS（363秒）和RAIN（1930秒）。K个候选rollout可高度并行化。

### 补充图表

![[assets/figures/papers/iclr26_0002_DsS3xRPSs5_Test-Time_Alignment_for_Large_Language_Models_vi/figures/009_Table_3.jpg]]
*Table 3: The statistics of winning translations for each language pairs evaluated by MetricX-24.*

![[assets/figures/papers/iclr26_0002_DsS3xRPSs5_Test-Time_Alignment_for_Large_Language_Models_vi/figures/010_Table_4.jpg]]
*Table 4: Robustness of TMPC on HH-RLHF-RLHF (3 iterations). We vary buffer size, segment length, reward model quality, and injected noise. Performance converges around three iterations and remains stable under noisy or weaker supervision.*

## 方法谱系与知识库定位

### 7.1 方法谱系

TMPC属于测试时对齐方法，其方法谱系如下：

- **训练时对齐**：DPO、SimPO、RLHF（需要微调模型参数）
- **测试时对齐**：
  - 引导解码（token级）：ARGS、RE-Control（受horizon诅咒影响）
  - 迭代优化（响应级）：TPO（受维度诅咒影响）
  - 树搜索：RAIN（计算成本高）
  - **TMPC（子目标级）**：平衡horizon诅咒与维度诅咒

### 7.2 关键差异

TMPC与现有方法的关键差异体现在四个维度：

| 维度 | 基线方法 | TMPC |
|------|---------|------|
| 动作粒度 | token级（引导解码）或完整响应级（迭代优化） | 子目标级（动态识别的高奖励中间段，可跨句子边界） |
| 规划方式 | 一次性全局优化（引导解码）或完整重写（迭代优化） | 滚动时域控制，迭代求解局部优化问题，利用子目标缓冲引导搜索 |
| 子目标识别 | 预定义硬边界（如句子级分割） | 事后动态识别，从rollout中回顾性提取高奖励段作为子目标 |
| 模型更新需求 | 需要微调或训练额外模型（如DPO、RLHF） | 无需任何模型学习或微调，冻结LLM作为提议分布 |

### 7.3 局限性

- TMPC受限于底层语言模型的表达能力，只能将生成引导至模型能力已支持的输出，当期望输出远离模型原始分布时可能效果不佳。
- TMPC的计算成本较高（HH-RLHF长回复每响应108秒），尽管K个候选rollout可并行化。
- TMPC在骨干模型语言能力较弱的语言对（如zh→ru）上表现不如专用模型（如Tower-7B）。

### 7.4 开放问题

- TMPC如何扩展到更长的生成任务（如整本书或长文档）？
- TMPC的子目标识别机制能否与更复杂的奖励模型（如多维度奖励）结合？
- TMPC的规划horizon H和迭代次数如何自适应确定？
- TMPC能否与其他测试时技术（如思维链、树搜索）结合以进一步提升性能？
- TMPC在更广泛的任务（如对话、摘要、创意写作）上的泛化能力如何？

## 原文 PDF

![[paperPDFs/ICLR_2026/Test_Time_Alignment_for_Large_Language_Models_via_Textual_Model_Predictive_Control.pdf]]
