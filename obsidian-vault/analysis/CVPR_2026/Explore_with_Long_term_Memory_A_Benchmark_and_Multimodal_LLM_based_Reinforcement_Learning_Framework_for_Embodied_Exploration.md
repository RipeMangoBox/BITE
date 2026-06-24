---
title: "Explore with Long-term Memory: A Benchmark and Multimodal LLM-based Reinforcement Learning Framework for Embodied Exploration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Explore_with_Long_term_Memory_A_Benchmark_and_Multimodal_LLM_based_Reinforcement_Learning_Framework_for_Embodied_Exploration.pdf
project_link: "https://wangsen99.github.io/papers/lmee/"
code_link: null
aliases:
- Explore_with_Lon
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 通过强化学习训练（GRPO）多模态大语言模型主动调用记忆检索工具，并结合多任务奖励函数（动作预测、前沿选择、问题回答）促进探索。
primary_logic: 主动记忆检索与多任务强化学习相结合，使智能体能够在长距离任务中动态构建和利用情景记忆，实现认知与决策的统一，提升自主探索能力。
claims:
- MemoryExplorer在LMEE-Bench上总指标超越3D-Mem和RA-Mem，SR达23.53, SPL 14.99, Score 43.62, Acc 65.52。
- 引入记忆检索工具后，模型性能显著提升，证明了主动检索对长距离导航和记忆问答的关键作用。
- 多任务奖励函数中的动作-前沿一致性惩罚和工具使用惩罚提高了模型性能。
- LMEE-Bench (Total) 上 Success Rate (SR) = 23.53
---

# Explore with Long-term Memory: A Benchmark and Multimodal LLM-based Reinforcement Learning Framework for Embodied Exploration

> [!tip] 核心洞察
> 主动记忆检索与多任务强化学习相结合，使智能体能够在长距离任务中动态构建和利用情景记忆，实现认知与决策的统一，提升自主探索能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于长期记忆的探索：用于具身探索的基准与多模态大语言模型强化学习框架 |
| 英文题名 | Explore with Long-term Memory: A Benchmark and Multimodal LLM-based Reinforcement Learning Framework for Embodied Exploration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.10744) · [Project](https://wangsen99.github.io/papers/lmee/) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | MemoryExplorer |
| Dataset | LMEE-Bench, GOAT-Bench |

> [!tip] 效果简介
> - LMEE-Bench (Total) 上，Success Rate (SR) 23.53 vs 16.91 (3D-Mem) (+6.62)；Success weighted by Path Length (SPL) 14.99 vs 6.86 (3D-Mem) (+8.13)；MLLM-Score (QA) 43.62 vs 32.59 (3D-Mem) (+11.03)。
> - GOAT-Bench (Val Unseen) 上，Success Rate (SR) 46.40 vs 42.81 (RA-Mem) (+3.59)；SPL 28.03 vs 21.95 (RA-Mem) (+6.08)。

## 概述

具身智能体在未知环境中的自主探索是构建通用智能系统的关键能力。现有研究主要聚焦于目标导航和具身问答等任务，却忽视了探索过程本身的价值——智能体在长距离探索中积累的情景记忆未被有效利用，导致其无法主动调用历史经验优化决策，难以实现从“完成任务”到“终身学习”的跨越。

针对这一瓶颈，本文提出**长期记忆具身探索（Long-term Memory Embodied Exploration, LMEE）**新范式，将多目标导航过程中收集的情景记忆与基于记忆的问答统一起来，同步评估模型的认知推理与决策执行能力。在此基础上，本文提出**MemoryExplorer**框架——一种基于多模态大语言模型（MLLM）的强化学习探索方法。其核心机制是：通过GRPO强化微调训练模型主动调用外部记忆检索工具，结合多任务奖励函数（动作预测、前沿选择、问题回答），使智能体能够在长距离任务中动态构建并利用多模态情景记忆，实现认知与决策的统一。

实验结果表明，MemoryExplorer在LMEE-Bench上全面超越现有方法：相较于基于被动记忆的3D-Mem，成功率（SR）从16.91提升至23.53，路径加权成功率（SPL）从6.86提升至14.99，问答评分（MLLM-Score）从32.59提升至43.62，准确率（Acc）从41.38提升至65.52。在GOAT-Bench上也取得了46.40的SR和28.03的SPL，验证了方法的泛化性。消融实验进一步证实，主动记忆检索工具的引入是性能提升的关键，多任务奖励中的动作-前沿一致性惩罚和工具使用惩罚对训练稳定性有显著贡献。

从方法谱系看，MemoryExplorer位于“RL微调MLLM + 主动记忆检索”的交叉点（Figure 3），区别于无记忆的Explore-EQA（纯导航基线）、被动记忆的3D-Mem（对象过滤）和无RL的RA-Mem（主动检索但未微调）。其知识贡献在于：首次将强化学习引入MLLM的具身探索训练，通过可学习的主动记忆检索机制弥合了感知、记忆与决策之间的鸿沟。

## 背景与动机

### 具身探索中的记忆鸿沟

具身智能体在未知环境中自主探索并完成长期任务，是通向通用人工智能的关键能力之一。现有研究主要沿两条独立路径发展：一是目标导航，要求智能体在未见过的场景中定位指定物体；二是具身问答，要求智能体在探索后回答与环境相关的问题。然而，这两类任务都聚焦于任务完成的最终结果，忽视了探索过程本身的价值——智能体在探索中积累的丰富情景记忆，并未被系统性地用于优化后续决策。

这种“记忆鸿沟”构成了当前具身探索的核心瓶颈：智能体缺乏主动调用长期记忆的机制，无法将过去的探索经验转化为当前的认知优势。例如，在“先到厨房查看微波炉，再到卧室寻找闹钟”的多目标导航中，智能体需要记住微波炉的位置、外观以及周围环境，才能在后续回答“微波炉旁边有什么”时给出正确答案。现有的端到端策略网络或基于预训练多模态大语言模型的方法，要么缺乏显式记忆结构，要么仅采用被动的对象过滤机制，难以支撑这种跨时间尺度的记忆推理。

### 现有方法的局限

**无记忆的具身探索基线**如 Explore-EQA，仅依赖当前观测进行导航和问答，在长距离任务中性能急剧下降。**基于被动记忆的方法**如 3D-Mem，虽然引入了情景记忆库，但记忆检索仅通过对象类别过滤触发，智能体无法根据任务需求主动决定何时检索、检索什么。**引入主动检索但缺乏强化学习的方法**如 RA-Mem，允许模型生成查询调用记忆工具，但由于采用监督微调而非奖励驱动的优化，模型难以在探索效率与记忆利用之间取得最优平衡。

更深层的问题在于，现有基准无法统一评估智能体的认知与决策能力。导航指标衡量“能否到达”，问答指标衡量“能否记住”，但缺乏一个将两者耦合的评估框架，使得我们无法判断智能体是否真正“理解”了它所探索的环境。

### 本文动机与核心思路

针对上述缺口，本文提出 **长期记忆具身探索**这一新范式，并构建了 **LMEE-Bench** 基准——将多目标导航与基于记忆的问答统一为同一任务，要求智能体在完成导航后回答关于探索过程的问题。在此基础上，本文提出 **MemoryExplorer** 框架，核心思路是通过强化学习训练多模态大语言模型主动调用记忆检索工具，并结合多任务奖励函数促进探索。

MemoryExplorer 的关键设计在于：模型根据当前任务指令、多视图观测和目标导向问题，动态生成查询并调用外部记忆检索工具，通过 CLIP 特征余弦相似度从情景记忆库中检索 top-k 相关记忆；随后，模型综合当前信息与检索记忆，同时预测导航动作、前沿选择与问题答案。训练采用 GRPO 算法，奖励函数由动作正确性、前沿选择合理性、答案质量和格式规范性四部分加权构成，并引入动作-前沿一致性惩罚和工具使用缩放因子，引导模型在探索效率与记忆利用之间取得平衡。

这一设计使智能体能够在长距离任务中动态构建和利用情景记忆，实现认知与决策的统一，从而提升自主探索能力。

## 核心创新

MemoryExplorer 的核心创新在于将**主动记忆检索**与**多任务强化学习微调**深度耦合，使多模态大语言模型（MLLM）在未知环境中能够自主构建并利用情景记忆，实现认知与决策的统一。相较于现有基线，其关键改进体现在三个“changed slots”上。

### 从被动过滤到主动检索的记忆机制

现有基于 MLLM 的探索方法对记忆的利用存在明显局限：**Explore-EQA** 完全不使用记忆，仅依赖当前观测进行导航；**3D-Mem**采用被动记忆策略，仅通过对象类别过滤历史信息，无法根据任务需求动态调用相关记忆。MemoryExplorer 则赋予模型**主动检索**能力——模型根据当前任务指令、多视图观测和目标导向问题，自主生成查询文本，通过 CLIP 特征余弦相似度从情景记忆库中检索 top-k 最相关的多模态记忆（位置、文本描述、图像）。如 Table 6 消融实验所示，一旦引入记忆检索工具，模型性能获得显著提升，证明了主动检索对长距离导航和记忆问答的关键作用。

### 从零样本推理到 GRPO 强化微调的训练范式跃迁

**RA-Mem** 虽然支持主动记忆检索，但未经过面向探索的专门训练，模型缺乏在长程任务中有效调用记忆的策略。MemoryExplorer 在 RA-Mem 基础上引入基于 **GRPO**（Group Relative Policy Optimization）的强化学习微调，最大化期望奖励：

$$\operatorname*{max}_{\pi_{\theta}} \mathbb{E}_{(I,O,Q)\sim D,\ y\sim\pi_{\theta}(\cdot\vert I,O,Q;M)}\left[r_{\phi}(I,O,Q,y)\right] - \beta D_{\mathrm{KL}}(\pi_{\theta}(\cdot\vert I,O,Q;M)\parallel\pi_{\mathrm{ref}}(\cdot\vert I,O,Q;M))$$

这一设计使模型从“被动回忆”转向“主动调用”，在训练过程中逐步学会何时检索记忆、检索哪些记忆、以及如何利用检索结果优化决策。

### 多任务奖励函数中的因果调控机制

传统探索任务仅以任务完成作为奖励信号，无法为记忆调用提供精细的反馈。MemoryExplorer 设计了**多任务奖励函数**，将总奖励分解为动作预测、前沿选择、问题回答和输出格式四个子奖励的加权组合：

$$r_{\mathrm{total}} = w_{act} \cdot r_{\mathrm{action}} \cdot c + w_{front} \cdot r_{\mathrm{frontier}} \cdot c + w_{ans} \cdot r_{\mathrm{answer}} + w_{fmt} \cdot r_{\mathrm{format}}$$

其中两个关键设计构成了因果调控的“旋钮”：

- **动作-前沿一致性惩罚**（系数 $c$）：当模型预测的动作与所选前沿方向不一致时施加惩罚，迫使模型在导航决策中保持空间推理的连贯性。消融实验（Table 7）显示，移除一致性惩罚后 SR 从 23.53 降至 22.43。
- **工具使用缩放因子**（$\alpha$）：当模型成功调用记忆检索工具时，子奖励乘以 1.2 的放大系数；当工具调用失败时，则乘以 0.5–0.6 的衰减系数。这一机制直接引导模型学习有效的主动检索策略。

### 方法谱系与知识库定位

MemoryExplorer 处于**具身探索 + 多模态大语言模型 + 强化学习**的交叉点。在具身探索谱系中，它区别于纯导航方法（如 Explore-EQA）和被动记忆方法（如 3D-Mem）；在 MLLM 应用谱系中，它通过 GRPO 微调将通用视觉语言模型（Qwen2.5-VL-7B）转化为具有主动记忆能力的具身智能体。其技术路径可概括为：**情景记忆库构建 → CLIP 特征检索 → 多任务奖励引导的 GRPO 策略优化 → 认知-决策统一输出**（Figure 3）。这一框架为 MLLM 在具身场景中实现终身学习提供了可复用的范式。

## 整体框架

MemoryExplorer 的整体设计围绕一个核心闭环展开：**多模态大语言模型（MLLM）策略通过强化学习主动调用外部记忆检索工具，在长距离多目标导航中动态构建和利用情景记忆，同时回答基于记忆的问题**。图1给出了该框架的宏观视图——它将“多目标导航”与“基于记忆的问答”统一为一个任务范式，使智能体的认知（记忆与推理）与决策（探索与导航）能力得以联合评估与优化。

### 输入与输出流

在每一个决策步，MLLM 策略 $\pi_\theta$ 接收三类输入：
- **任务指令 $I$**：描述当前需要完成的多目标导航任务及目标相关问题；
- **多视图观察 $O$**：来自环境的 RGB 和深度图像；
- **目标导向问题 $Q$**：要求智能体基于已收集的情景记忆回答的具体问题（如“你见过红色的椅子吗？”）。

策略以**代码生成**的形式输出结构化响应，包含五个关键字段：`THOUGHT`（推理过程）、`CODE`（工具调用指令）、`ANSWER`（问题回答）、`FRONTIER`（前沿选择）和 `ACTION`（导航动作）。这种设计使模型的行为可解释、可验证，同时便于与外部工具交互。

### 核心模块与数据流

**1. 记忆检索工具（Memory Retrieval Tool）**
该工具是框架的关键创新点。当模型在 `CODE` 字段中生成检索调用时，系统提取当前状态的文本特征 $f_q$，通过 CLIP 余弦相似度从情景记忆库 $\mathcal{M}$ 中检索 top-k 相关记忆：
$$\mathcal{R} = \{ m_i \mid i \in \mathrm{top}\text{-}k(\cos(f_q, f_i^{(t,o)})) \}$$
检索到的记忆以多模态形式（位置坐标、文本描述、图像特征）返回给策略模型，作为后续决策的上下文。记忆库 $\mathcal{M}$ 在导航过程中持续增长，每条记忆存储第 $i$ 步的位置 $p_i$、文本特征 $f_i$ 和图像特征 $o_i$：
$$\mathcal{M} = \{ (p_i, f_i, o_i) \mid i = 1, \ldots, n \}$$

**2. 前沿选择器（Frontier Selector）**
该模块基于 DBSCAN 聚类算法对未探索区域的边界像素进行分组，生成候选前沿点。模型从这些候选中选择下一步的探索目标，实现结构化探索。

**3. 多任务奖励函数（Multi-Task Reward Function）**
训练信号由四个子奖励加权组合而成，并引入一致性惩罚和工具使用缩放因子：
$$r_{\mathrm{total}} = w_{act} \cdot r_{\mathrm{action}} \cdot c + w_{front} \cdot r_{\mathrm{frontier}} \cdot c + w_{ans} \cdot r_{\mathrm{answer}} + w_{fmt} \cdot r_{\mathrm{format}}$$
其中 $r_{\mathrm{action}}$、$r_{\mathrm{frontier}}$、$r_{\mathrm{answer}}$、$r_{\mathrm{format}}$ 分别评估动作准确性、前沿选择正确性、回答精度和输出格式完整性，取值范围均为 $[0,1]$。一致性系数 $c$ 惩罚动作与前沿选择之间的不一致，缩放因子 $\alpha$ 在工具调用成功时放大奖励（如 $\alpha=1.2$），失败时则衰减奖励。

**4. GRPO 策略优化**
策略模型 $\pi_\theta$ 通过 Group Relative Policy Optimization（GRPO）进行强化微调，优化目标为最大化期望奖励并约束与参考策略 $\pi_{\mathrm{ref}}$ 的 KL 散度：
$$\max_{\pi_\theta} \mathbb{E}_{(I,O,Q)\sim D,\ y\sim\pi_\theta(\cdot|I,O,Q;M)} \left[ r_\phi(I,O,Q,y) \right] - \beta D_{\mathrm{KL}}(\pi_\theta(\cdot|I,O,Q;M) \parallel \pi_{\mathrm{ref}}(\cdot|I,O,Q;M))$$

### 与基线方法的关键差异

MemoryExplorer 直接继承 RA-Mem 的主动记忆检索架构，但引入了两个决定性变化：
- **训练范式**：从预训练 MLLM 的直接推理（无微调）升级为基于 GRPO 的强化学习微调，使模型学会*何时*以及*如何*调用记忆检索工具；
- **奖励设计**：从单一的任务完成信号扩展为多任务、多粒度的奖励函数，配合一致性惩罚和工具使用缩放，显式引导模型在动作、前沿选择、问答和格式四个维度上优化。

消融实验证实，一旦引入记忆检索工具，模型性能即获得显著提升（Table 6），而动作-前沿一致性惩罚和工具使用惩罚的加入进一步将 SR 从 22.43 提升至 23.53（Table 7），验证了多任务奖励设计的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l2158_https_arxiv_org_abs_2601_10744/figures/004_Figure_3.jpg]]
*Figure 3: Illustration of training in MemoryExplorer. Given a task instruction, the multi-view observations, and a goal-oriented question. Model retrieves relevant multimodal memories from the episodic memory bank using tools, analyzes the current information alongside the retrieved memories to understand the progress of the long-term task, and performs ACTION prediction, FRONTIER selection, and question ANSWER. The policy model output response calculates the reward using a Multi-Task Reward function and is fine-tuned using GRPO*

## 核心模块与公式推导

MemoryExplorer 是一个基于强化学习与主动记忆检索的具身探索模型，其核心由四个关键模块构成：**情景记忆库与检索工具**、**基于MLLM的策略网络**、**多任务奖励函数**以及**GRPO策略优化**。模型以任务指令 $I$、多视图观察 $O$ 和目标导向问题 $Q$ 为输入，通过策略 $\pi_\theta(I, O, Q; \mathcal{M})$ 输出动作、前沿选择和问题答案，其中 $\mathcal{M}$ 为情景记忆库。

### 情景记忆库与主动检索

记忆库存储智能体在探索过程中积累的多模态情景记忆，每个条目包含位置、文本特征和图像特征：

$$\mathcal{M} = \{ (p_i, f_i, o_i) \mid i = 1, \ldots, n \}$$

其中 $p_i$ 为第 $i$ 步的位置坐标，$f_i$ 为 CLIP 文本编码器提取的观测描述特征，$o_i$ 为 CLIP 视觉编码器提取的观测图像特征。

记忆检索工具是模型主动调用的外部接口。当模型生成查询文本后，系统提取其 CLIP 文本特征 $f_q$，与记忆库中每条记忆的文本特征 $f_i^{(t)}$ 和观测特征 $f_i^{(o)}$ 分别计算余弦相似度，取 top-k 最相关记忆：

$$\mathcal{R} = \{ m_i \mid i \in \text{top-}k(\cos(f_q, f_i^{(t, o)})) \}$$

检索到的记忆 $\mathcal{R}$ 以文本形式注入策略模型的上下文，使模型能够动态利用历史信息进行决策。这一主动检索机制是 MemoryExplorer 区别于被动记忆方法（如 3D-Mem 的对象类别过滤）的核心创新——模型学会了“何时检索”与“检索什么”，而非依赖预设规则。

### 多任务奖励函数

为引导模型同时优化导航探索与记忆问答，MemoryExplorer 设计了组合四个子奖励的多任务奖励函数：

$$r_{\text{total}} = w_{act} \cdot r_{\text{action}} \cdot c + w_{front} \cdot r_{\text{frontier}} \cdot c + w_{ans} \cdot r_{\text{answer}} + w_{fmt} \cdot r_{\text{format}}$$

各子奖励取值范围均为 $[0, 1]$：
- $r_{\text{action}}$：动作预测准确性奖励，衡量模型输出的导航动作与专家轨迹的一致性。
- $r_{\text{frontier}}$：前沿选择正确性奖励，评估模型选择的前沿点是否与任务目标方向一致。
- $r_{\text{answer}}$：问题回答质量奖励，对选择题采用准确率，对开放式回答采用 MLLM-Score 量化。
- $r_{\text{format}}$：输出格式完整性奖励，确保模型输出包含所有必需字段。

$c$ 为**动作-前沿一致性系数**：当动作方向与所选前沿方向不一致时，$c$ 取小于 1 的值，对 $r_{\text{action}}$ 和 $r_{\text{frontier}}$ 施加惩罚，迫使模型学习协调导航意图与空间目标。此外，系统引入**工具使用缩放因子** $\alpha$：当模型成功调用记忆检索工具时，各子奖励乘以 $\alpha = 1.2$ 以鼓励主动检索；当工具调用失败时，$r_{\text{answer}}$ 和 $r_{\text{format}}$ 的 $\alpha$ 降至 0.5，$r_{\text{action}}$ 和 $r_{\text{frontier}}$ 降至 0.6，抑制无效工具依赖。

消融实验（Table 7）证实，移除一致性惩罚后 SR 从 23.53 降至 22.43，验证了该设计的必要性。权重配置 $w_{act} = 0.2, w_{front} = 0.2, w_{ans} = 0.4, w_{fmt} = 0.2$ 经网格搜索确认为最优（Table 8）。

### GRPO 策略优化

MemoryExplorer 采用 Group Relative Policy Optimization (GRPO) 对策略模型 $\pi_\theta$ 进行强化微调，优化目标为：

$$\max_{\pi_\theta} \mathbb{E}_{(I, O, Q) \sim D, \, y \sim \pi_\theta(\cdot \vert I, O, Q; \mathcal{M})} \left[ r_\phi(I, O, Q, y) \right] - \beta D_{\text{KL}}(\pi_\theta(\cdot \vert I, O, Q; \mathcal{M}) \parallel \pi_{\text{ref}}(\cdot \vert I, O, Q; \mathcal{M}))$$

其中 $r_\phi$ 为上述多任务奖励函数，$\beta$ 控制与参考策略 $\pi_{\text{ref}}$（初始预训练 MLLM）的 KL 散度惩罚强度，防止策略在微调中过度偏离原始语言能力。GRPO 通过组内相对比较更新策略，无需训练额外的价值网络，降低了计算开销。训练基于 EasyR1 框架实现，基座模型为 Qwen2.5-VL-7B。

训练过程监控（Figure 5）显示，奖励曲线在约 200 步后趋于收敛，工具使用率从初始的随机调用逐步稳定至合理水平，表明模型通过强化学习习得了有效的主动检索策略。

## 实验与分析

### 核心实验设置

MemoryExplorer 基于 **Qwen2.5-VL-7B** 实现，采用 **EasyR1** 框架进行 GRPO 强化微调。训练数据为 LMEE 数据集的 1,816 个任务（Table 1），测试集包含 166 个任务，按轨迹长度和目标数量划分为 Easy、Medium、Hard 三个难度等级（Table 9）。评估指标包括导航指标 **Success Rate (SR)** 与 **Success weighted by Path Length (SPL)**，以及问答指标 **MLLM-Score**（对开放式回答的语义质量评分）和 **Accuracy (Acc)**（选择题正确率）。所有 MLLM 方法均在相同的前沿探索框架和 50 步限制下评估，导航成功判定标准为距目标 1m 内，确保了对比公平性。

![[assets/figures/papers/paper_list_l2158_https_arxiv_org_abs_2601_10744/figures/002_Table_1.jpg]]
*Table 1: Comparison to popular embodied exploration benchmarks*

### 主实验结果

**LMEE-Bench 结果（Table 2）。** MemoryExplorer 在所有指标上全面超越基线方法。在 Total 难度下，SR 达到 **23.53**，较 3D-Mem（16.91）提升 **+6.62**，较 RA-Mem（20.96）提升 **+2.57**；SPL 达到 **14.99**，较 3D-Mem（6.86）提升 **+8.13**，较 RA-Mem（12.18）提升 **+2.81**。问答能力提升更为显著：MLLM-Score 达到 **43.62**，较 3D-Mem（32.59）提升 **+11.03**；Acc 达到 **65.52**，较 3D-Mem（41.38）提升 **+24.14**。这表明强化学习驱动的主动记忆检索对长距离导航和记忆问答均有实质性增益。

值得注意的是，Explore-EQA（无记忆的纯导航基线）在 Easy 难度上 SR 为 21.01，但在 Hard 难度下降至 4.95，而 MemoryExplorer 在 Hard 难度下 SR 仍有 16.17，体现了记忆机制在复杂长距离任务中的关键作用。

**GOAT-Bench 结果（Table 3）。** 在 GOAT-Bench 的 Val Unseen 划分上，MemoryExplorer 同样取得最优：SR 为 **46.40**（RA-Mem 42.81，+3.59），SPL 为 **28.03**（RA-Mem 21.95，+6.08）。这验证了方法在不同基准上的泛化能力。

### 消融实验

**问题类型消融（Table 4）。** 将训练中的多选题替换为简单问题时，SR 从 23.53 降至 20.80，Score 从 43.62 降至 41.33。多选题训练迫使模型在导航过程中更精细地关注环境细节，从而同时提升导航和问答性能。

**训练任务设计消融（Table 6）。** 引入记忆检索工具后，模型性能获得显著跃升——这直接证明了主动检索对长距离导航和记忆问答的核心作用。若移除记忆检索工具，模型退化为仅依赖当前观察进行决策，无法有效利用历史信息。

**奖励设计消融（Table 7）。** 多任务奖励函数中的动作-前沿一致性惩罚（action–frontier consistency penalty）和工具使用惩罚（tool-usage penalty）均对性能有正向贡献。移除一致性惩罚后，SR 从 23.53 降至 22.43，Score 从 43.62 降至 40.19。一致性惩罚确保模型在预测动作和选择前沿时保持空间逻辑一致，避免“说一套做一套”的决策冲突。

**奖励权重消融（Table 8）。** 最优权重配置为 $w_{act}=0.2$、$w_{front}=0.2$、$w_{ans}=0.4$、$w_{fmt}=0.2$，回答子奖励权重最高，体现了任务对记忆问答的侧重。

**子集与全量一致性（Table 5）。** 因资源限制，主评估使用子集（约 30% 任务），但全量测试结果与子集趋势一致，结论稳健。

### 训练动态

Figure 5 展示了训练过程中的奖励曲线和工具使用率变化。随着训练进行，总奖励逐步上升，同时工具调用比例趋于稳定，表明模型学会了在何时主动检索记忆而非盲目调用。

![[assets/figures/papers/paper_list_l2158_https_arxiv_org_abs_2601_10744/figures/009_Figure_5.jpg]]
*Figure 5: Training reward curve and tool usage percentage*

### 答案质量分布

Figure 6 展示了不同类型问题上的答案质量分布。模型在“存在性判断”类问题上表现最佳，而在“计数”和“空间关系推理”类问题上仍有较大提升空间，这与视觉-语言模型的空间理解能力瓶颈一致。

![[assets/figures/papers/paper_list_l2158_https_arxiv_org_abs_2601_10744/figures/010_Figure_6.jpg]]
*Figure 6: Answer quality across different question types*

### 失败模式分析

论文通过 Figure 10-12 展示了三类典型失败案例：

1. **数据歧义导致答案错误（Figure 10）。** 训练数据生成过程中存在的标签歧义（如同一物体在不同视角下被赋予不同语义描述）可能导致模型检索到正确记忆后仍输出错误答案。
2. **错误记忆检索（Figure 11）。** 当查询特征与目标记忆的 CLIP 相似度不足时，模型可能检索到不相关的记忆条目，进而误导决策。
3. **记忆正确但描述错误（Figure 12）。** 模型成功检索到相关记忆，但在生成最终回答时出现语言表述偏差，反映了 MLLM 生成能力与检索精度之间的解耦问题。

### 真实世界验证

论文在 ROSMASTER X3 机器人平台（Figure 7）上进行了真实世界测试（Figure 8），验证了 MemoryExplorer 从仿真到现实的迁移潜力。完整任务执行流程见 Figure 9。

![[assets/figures/papers/paper_list_l2158_https_arxiv_org_abs_2601_10744/figures/011_Figure_7.jpg]]
*Figure 7: ROSMASTER X3*

### 方法谱系与知识库定位

MemoryExplorer 处于**具身探索 + 多模态大语言模型 + 强化学习**的交叉点。其直接前身是 RA-Mem（主动记忆检索但无 RL），核心增量在于引入 GRPO 强化微调，使模型自主学会“何时检索”和“如何利用检索结果”。与 3D-Mem（被动对象过滤，**Jiao et al., 2024**）相比，MemoryExplorer 将记忆从静态知识库升级为动态可查询的情景记忆系统。在方法谱系上，该工作上承基于前沿探索的经典导航框架，下接 MLLM 驱动的具身推理，为终身探索学习提供了可训练的范式。

### 补充图表

![[assets/figures/papers/paper_list_l2158_https_arxiv_org_abs_2601_10744/figures/005_Table_2.jpg]]
*Table 2: Experiments on LMEE-Bench. Score represents the MLLM-Score for open-ended answers, and Acc represents the accuracy rate of the answer choices*

![[assets/figures/papers/paper_list_l2158_https_arxiv_org_abs_2601_10744/figures/008_Table_3.jpg]]
*Table 3: Experiments on GOAT-Bench. Evaluated on the “Val Unseen” split. Methods denoted by * are from GOAT-Bench, and those with † are evaluated on the subset. All MLLM-based exploration methods are implemented based on Qwen2.5-VL-7B*

![[assets/figures/papers/paper_list_l2158_https_arxiv_org_abs_2601_10744/figures/007_Table_4.jpg]]
*Table 4: Ablation study on question type*

![[assets/figures/papers/paper_list_l2158_https_arxiv_org_abs_2601_10744/figures/013_Table_6.jpg]]
*Table 6: Ablation study on training task setting*

![[assets/figures/papers/paper_list_l2158_https_arxiv_org_abs_2601_10744/figures/014_Table_7.jpg]]
*Table 7: Ablation study on reward design*

![[assets/figures/papers/paper_list_l2158_https_arxiv_org_abs_2601_10744/figures/015_Table_8.jpg]]
*Table 8: Ablation study on hyperparameters*

![[assets/figures/papers/paper_list_l2158_https_arxiv_org_abs_2601_10744/figures/012_Table_5.jpg]]
*Table 5: Experiments on subset and full-set LMEE-Bench*

## 方法谱系与知识库定位

### 1. 任务范式定位：从目标导航到记忆增强的具身探索

MemoryExplorer 所处的具身探索研究谱系，可以从任务范式、记忆机制和学习策略三个维度进行定位。

在任务范式层面，现有研究主要聚焦于目标导航（Goal Navigation）和具身问答（Embodied Question Answering, EQA）两条相对独立的路径。目标导航类方法（如 GOAT-Bench 所涵盖的工作）关注智能体在未知环境中定位指定目标的能力，但通常不要求智能体对探索过程本身进行记忆和反思。具身问答方法则要求智能体在导航过程中回答环境相关问题，但其记忆机制多为隐式的、基于循环网络或地图构建的短期记忆。**本工作提出的 Long-term Memory Embodied Exploration (LMEE) 范式，首次将多目标导航过程中的情景记忆收集与基于记忆的问答评估相统一**，填补了“探索过程记忆化”与“认知能力可评估化”之间的空白。如 Table 1 所示，LMEE-Bench 在任务类型、记忆需求和评估维度上均区别于现有基准。

### 2. 方法演化链：从无记忆到主动记忆检索

MemoryExplorer 的方法演化可以沿着一条清晰的基线链追溯：

- **Explore-EQA**：无记忆的具身探索基线，仅执行导航任务，不涉及任何记忆存储或检索。其性能上限受限于当前观测，无法利用历史信息优化长距离决策。

- **3D-Mem**：基于被动记忆的 MLLM 探索方法。该方法通过对象类别过滤（object filtering）存储和调用记忆，但记忆检索是被动的、基于规则的，缺乏对任务上下文的主动适配能力。在 LMEE-Bench 上，3D-Mem 的 SR 为 16.91，SPL 为 6.86，Score 为 32.59。

- **RA-Mem**：引入主动记忆检索的 MLLM 方法，允许模型根据当前状态生成查询并检索相关记忆。但 RA-Mem 仍基于预训练 MLLM 直接推理，未经过针对探索任务的微调。其 SR 为 20.96，SPL 为 12.18，Score 为 35.52，相较 3D-Mem 有显著提升，但仍有优化空间。

- **MemoryExplorer**：在 RA-Mem 的基础上引入两个关键改进：(1) **基于 GRPO 的强化学习微调**，使模型通过多任务奖励函数（含动作、前沿选择、回答、格式四部分子奖励）学习主动探索和记忆检索策略；(2) **多任务奖励中的一致性惩罚和工具使用缩放因子**，引导模型在调用记忆检索工具时保持动作-前沿一致性。这一演化使 MemoryExplorer 在 LMEE-Bench 上达到 SR 23.53、SPL 14.99、Score 43.62，相较 3D-Mem 分别提升 +6.62、+8.13、+11.03，相较 RA-Mem 亦有显著增益。

### 3. 核心机制创新点

MemoryExplorer 的核心创新可归纳为以下三个相互耦合的机制：

**主动记忆检索工具**：模型通过生成代码调用外部记忆检索工具，利用 CLIP 特征余弦相似度从情景记忆库中检索 top-k 相关记忆。该工具使模型能够动态构建对长期任务进展的理解，而非仅依赖当前观测。消融实验（Table 6）证实，一旦引入记忆检索工具，模型性能获得显著提升，证明主动检索对长距离导航和记忆问答的关键作用。

**多任务奖励函数**：总奖励由动作、前沿、回答、格式四部分子奖励加权构成，并乘以一致性系数 $c$：
$$r_{\mathrm{total}} = w_{act} \cdot r_{\mathrm{action}} \cdot c + w_{front} \cdot r_{\mathrm{frontier}} \cdot c + w_{ans} \cdot r_{\mathrm{answer}} + w_{fmt} \cdot r_{\mathrm{format}}$$
其中 $c$ 为动作-前沿一致性惩罚系数，当动作预测与前沿选择不一致时降低奖励。消融实验（Table 7）表明，去除一致性惩罚后 SR 从 23.53 降至 22.43，验证了该设计的有效性。奖励权重的最优配置为 $w_{act}=0.2, w_{front}=0.2, w_{ans}=0.4, w_{fmt}=0.2$（Table 8）。

**GRPO 策略优化**：采用 Group Relative Policy Optimization (GRPO) 算法，通过最大化期望奖励并约束与参考策略的 KL 散度来更新策略模型 $\pi_\theta$：
$$\max_{\pi_\theta} \mathbb{E}_{(I,O,Q) \sim D,\ y \sim \pi_\theta(\cdot|I,O,Q;M)} \left[ r_\phi(I,O,Q,y) \right] - \beta D_{\mathrm{KL}}(\pi_\theta(\cdot|I,O,Q;M) \parallel \pi_{\mathrm{ref}}(\cdot|I,O,Q;M))$$
这一范式使模型能够在保持预训练能力的同时，学习面向探索任务的主动决策策略。

### 4. 适用边界与局限

**适用场景**：MemoryExplorer 适用于需要长期记忆和主动探索的室内具身任务，尤其是多目标导航和基于记忆的问答场景。其在 GOAT-Bench（Val Unseen）上达到 SR 46.40、SPL 28.03，证明了方法在标准导航基准上的泛化能力。

**已知局限**：

1. **推理效率瓶颈**：MLLM 推理速度慢，无法满足实时具身任务的执行需求。论文明确指出需要开发更轻量的模型以支持实际部署。

2. **长时记忆的准确性与效率**：当前方法在处理需要长期记忆的挑战性任务上仍显不足。失败案例分析（Figure 10-12）揭示了三种典型失效模式：(a) 数据歧义导致答案错误；(b) 错误记忆检索；(c) 记忆正确但描述错误。这表明记忆存储和检索的准确性及效率需进一步提升。

3. **数据依赖性**：LMEE-Bench 基于 HM3DSem 场景构建，训练集 1,816 个任务、测试集 166 个任务。模型在分布外场景（如多楼层、动态环境）上的表现未经验证。

4. **记忆相似度计算的精度上限**：记忆检索依赖 CLIP 特征余弦相似度，可能无法捕捉细粒度的场景语义差异，导致检索到语义相关但任务无关的记忆。

### 5. 开放问题与未来方向

1. **长时记忆的存储与检索效率**：如何设计更高效的记忆压缩、索引和检索机制，以支持更大规模、更长时间跨度的具身任务？是否可引入层次化记忆结构或遗忘机制？

2. **场景泛化能力**：MemoryExplorer 能否扩展到多楼层、动态环境或开放词汇场景？这需要验证模型在未见场景类型和语义分布上的鲁棒性。

3. **记忆匹配精度的提升**：当前依赖 CLIP 特征的相似度计算，可否引入更精细的场景理解模块（如 3D 场景图、对象关系建模）以提高匹配准确性？

4. **自适应记忆调用策略**：主动记忆调用的频率和策略如何根据任务难度自适应调整？是否可以在训练过程中学习“何时检索”的元策略，而非固定使用 top-k 检索？

5. **与经典方法的融合**：MemoryExplorer 的强化学习微调范式与经典地图构建方法（如语义建图、拓扑图）之间是否存在互补性？将结构化环境表征与 MLLM 的情景记忆相结合，可能进一步提升长距离导航的准确性和效率。

## 原文 PDF

![[paperPDFs/CVPR_2026/Explore_with_Long_term_Memory_A_Benchmark_and_Multimodal_LLM_based_Reinforcement_Learning_Framework_for_Embodied_Exploration.pdf]]
