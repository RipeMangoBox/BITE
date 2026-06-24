---
title: "Dual-Scale World Memory for LLM Agents towards Hard-Exploration Problems"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Dual_Scale_World_Memory_for_LLM_Agents_towards_Hard_Exploration_Problems.pdf
openreview_forum_id: bH5uHIVtTe
aliases:
- GGLWM
- DSWMLATHEP
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入双尺度世界记忆（GLoW）：全局世界记忆维护价值排序的轨迹前沿（而非孤立状态），并通过LLM分析前沿提取关键状态的“成就价值(v)”和“潜力价值(v')”，实现原则性的状态选择，平衡利用与探索；局部世界记忆采用多路径优势反射（MAR），从同一状态采样多条轨迹，通过LLM比较轨迹差异来推断语义优势信号，从而在稀疏环境奖励下提供伪密集的进展指引。"
primary_logic: "将硬探索问题分解为状态选择和探索两个阶段，对应两种不同尺度的学习：全局尺度从历史轨迹中识别瓶颈和高潜力区域，局部尺度通过多轨迹对比降低方差，将稀疏奖励转化为语义优势信号，从而大幅提升LLM智能体在稀疏反馈环境下的探索效率和性能。"
claims:
- "全局世界记忆使用轨迹前沿而非状态存档，并由LLM进行价值分解以提取v和v'。"
- "局部世界记忆通过多路径优势反射（MAR）比较同一状态的多条轨迹，推断语义优势，将稀疏奖励转化为密集进展信号。"
- "GLoW在Jericho基准上以仅1000步交互达到LLM方法的SOTA，并在多个游戏上性能接近或超越使用80万步的RL方法。"
- "消融实验证实，移除MAR或全局世界记忆组件会导致性能显著下降，全部移除后性能退化至接近IGE基线。"
---

# Dual-Scale World Memory for LLM Agents towards Hard-Exploration Problems

> [!tip] 核心洞察
> 将硬探索问题分解为状态选择和探索两个阶段，对应两种不同尺度的学习：全局尺度从历史轨迹中识别瓶颈和高潜力区域，局部尺度通过多轨迹对比降低方差，将稀疏奖励转化为语义优势信号，从而大幅提升LLM智能体在稀疏反馈环境下的探索效率和性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向难探索问题的LLM智能体的双尺度世界记忆 |
| 英文题名 | Dual-Scale World Memory for LLM Agents towards Hard-Exploration Problems |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=bH5uHIVtTe); [GitHub](https://github.com/mnskim/glow) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | GLoW (Global-Local World Memory) |
| Dataset | Zork1 (Jericho), Deephome (Jericho), Enchanter (Jericho), Jericho – 10 games |

> [!tip] 效果简介
> - Zork1 (Jericho) 上，Maximum score (mean ± std) 为 73.0 ± 4.5，对比 43.3 ± 8.5 (IGE, LLM Go-Explore)，变化 +29.7。
> - Deephome (Jericho) 上，Maximum score (mean ± std) 为 75.0 ± 8.7，对比 77.7 ± 2.1 (XTX, RL SOTA)，变化 ‑2.7 (nearly matches RL SOTA)。
> - Enchanter (Jericho) 上，Maximum score (mean ± std) 为 61.7 ± 20.1，对比 52.0 (XTX, RL SOTA)，变化 +9.7 (surpasses RL SOTA)。

## 概述

硬探索问题（hard-exploration problems）的核心挑战在于：环境反馈极度稀疏，智能体需要在巨大的状态-动作空间中通过极少的外部奖励信号来发现通往目标的路径。以文本冒险游戏Zork1为例，其每步可能的动作数量高达 $O(697^5) = 1.64 \times 10^{14}$，而游戏仅在完成特定子任务时才给予少量分数奖励。现有LLM智能体方法（如**ReAct**（Yao et al., 2023）、**Reflexion**（Shinn et al., 2023））仅支持局部试错，而基于Go-Explore范式的方法（如**IGE**（Lu et al., 2025））虽维护状态存档以支持跨情节探索，但其状态选择阶段依赖启发式规则或LLM内部的模糊“有趣性”判断，缺乏对轨迹上下文的系统性价值估计。

本文提出**GLoW（Global-Local World Memory）**，一种面向LLM智能体的双尺度世界记忆框架，将硬探索问题显式分解为**全局学习**与**局部试错**两个互补阶段。其核心机制包括：

- **全局世界记忆**：维护一个按价值排序的轨迹前沿（trajectory frontier），保留高价值轨迹的完整时间上下文；通过LLM分析前沿，提取关键状态的“成就价值 $v$”和“潜力价值 $v'$”，实现原则性的状态选择，平衡利用与探索。
- **局部世界记忆**：采用多路径优势反射（Multi-path Advantage Reflection, MAR），从同一状态采样多条探索轨迹，通过LLM比较轨迹差异来推断语义优势信号，从而在稀疏环境奖励下提供伪密集的进展指引，降低探索方差。

在Jericho文本游戏基准上，GLoW以仅**1000步**环境交互即达到LLM方法的SOTA性能，在10款游戏中取得7款的最佳LLM成绩；在Deephome和Enchanter上，其性能接近或超越使用80万步交互的RL方法**XTX**（Tuyls et al., 2022）。消融实验证实，移除MAR或全局世界记忆组件均会导致性能显著下降，全部移除后退化至接近IGE基线水平，验证了双尺度设计的协同效应。

## 背景与动机

### 问题背景：硬探索问题的双重挑战

在文本游戏等复杂交互环境中，LLM智能体面临**硬探索问题**（hard-exploration problems）的严峻考验。这类问题的核心困难源于两个相互交织的挑战：

**全局学习缺失。** 硬探索任务通常需要智能体在漫长的交互过程中持续积累有价值的发现，并据此调整后续的探索方向。然而，现有LLM智能体缺乏一种有效机制来系统性地维护和利用这些跨时间尺度的发现——它们往往在单次尝试后便丢弃了宝贵的探索经验，无法从历史轨迹中识别瓶颈状态和高潜力区域。

**局部试错困难。** 这类环境通常只提供极为稀疏的反馈信号——智能体可能在数十甚至数百步操作后才获得一次奖励。在如此稀疏的奖励结构下，LLM智能体难以快速判断哪些动作真正推动了任务进展，哪些动作是无效的徘徊。以Jericho基准中的Zork1游戏为例，其词汇量为697个单词，每步可能的动作组合空间高达$O(697^5) = 1.64 \times 10^{14}$，在如此巨大的动作空间中仅凭稀疏的环境奖励进行试错学习几乎不可行。

### 现有方法的局限

当前应对硬探索问题的方法可归纳为三个主要范式，但各自存在结构性缺陷：

**RL-based方法**（如**DRRN**，He et al., 2016；**KG-A2C**，Ammanabrolu & Hausknecht, 2020；**XTX**，Tuyls et al., 2022）虽然在某些游戏上取得了较强性能，但需要海量环境交互——XTX在Jericho上使用了80万步交互，样本效率极低，难以推广到交互成本高昂的真实场景。

**MCTS-based方法**（如**MC-LAVE**，Jang et al., 2021；**MC-DML**，Shi et al., 2025）通过树搜索引入探索机制，但受限于搜索深度和宽度，在需要长期规划的硬探索任务中仍显不足。

**LLM-based方法**可进一步分为两类：
- **局部试错型**（如**ReAct**，Yao et al., 2023；**Reflexion**，Shinn et al., 2023）：仅支持单轨迹内的推理与反思，缺乏跨轨迹的全局学习能力。Reflexion虽能在多轮尝试间传递文本反馈，但其反思粒度粗糙，无法从历史轨迹中提取结构化的价值信息来指导状态选择。
- **Go-Explore型**（如**IGE**，Lu et al., 2025）：维护状态存档并从存档中选择有潜力的状态进行分支探索，形式上更接近硬探索的需求。然而，IGE的状态选择依赖于LLM内部的模糊“有趣性”判断，缺乏基于轨迹上下文的**原则性价值估计**；其探索阶段也未充分利用从同一状态出发的多条轨迹进行对比，难以在稀疏奖励下获得可靠的进展信号。

**核心瓶颈**在于：现有方法未能将硬探索问题系统性地分解为**状态选择**和**探索执行**两个阶段，并针对每个阶段设计专门的学习机制——选择阶段需要全局视野来识别高价值区域，探索阶段需要局部对比来降低稀疏反馈的方差。

### 本文动机：双尺度世界记忆

针对上述瓶颈，本文提出**GLoW（Global-Local World Memory）**框架，核心洞察在于：硬探索问题天然需要两种不同时间尺度的学习。

- **全局尺度**：从历史轨迹中识别瓶颈状态和高潜力区域，为状态选择提供原则性的价值估计，平衡利用（回到已知高分状态）与探索（前往潜力未明区域）。
- **局部尺度**：从同一状态出发采样多条轨迹，通过LLM比较轨迹差异来推断语义优势信号，将稀疏的环境奖励转化为伪密集的进展指引，从而在局部探索中快速修正策略。

GLoW通过**全局世界记忆**维护价值排序的轨迹前沿，并由LLM分析前沿以提取关键状态的“成就价值”与“潜力价值”；同时通过**局部世界记忆**中的多路径优势反射（MAR）机制，在同一状态下进行多轨迹对比以降低方差。这一双尺度架构使得LLM智能体能够在仅1000步交互的预算下，在Jericho基准上达到LLM方法的SOTA，并在多个游戏上性能接近甚至超越使用80万步交互的RL方法。

## 核心创新

GLoW的核心创新在于将硬探索问题解构为**全局价值学习**与**局部试错学习**两个互补尺度，并通过双尺度世界记忆实现二者的协同。相较于现有方法，GLoW在三个关键设计槽位上做出了根本性改变：

### 1. 全局记忆表征：从状态存档到轨迹前沿

现有方法（如IGE）维护的是孤立的**状态存档**，选择阶段依赖启发式规则或LLM内部的模糊“有趣性”判断，缺乏对轨迹上下文的原则性价值估计。GLoW将全局记忆重新定义为**轨迹前沿** $\mathcal{F}$——维护$k$条最高价值轨迹的完整时序上下文，而非孤立状态快照。轨迹价值定义为：

$$v(\tau_i) = \max_{t\in[1,T]} \sum_{j=1}^{t} r_j^i$$

即轨迹中任意时刻达到的最大累计奖励，适配Jericho的稀疏奖励结构。前沿更新遵循：

$$\mathcal{F}_{t+1} = \mathrm{top\text{-}k}(\mathcal{F}_t \cup \{\tau_{\mathrm{new}}\}, v)$$

这一改变的因果机制在于：保留完整轨迹上下文使LLM能够分析“如何到达高价值状态”以及“为何进展停滞”，从而为后续的价值分解提供信息基础。

### 2. 状态选择：从启发式选择到原则性价值分解

在状态选择阶段，现有方法或使用手工启发式（Go-Explore原始版本），或依赖模仿学习（XTX），或直接调用LLM的“promisingness”判断（IGE），均未对状态价值进行结构化分析。GLoW引入**LLM驱动的价值分解**，从轨迹前沿生成全局世界记忆：

$$W_{\mathrm{global}} = g_{\mathrm{LLM}}(\mathcal{F}) = \{(s_1, v_1, v'_1), \dots, (s_k, v_k, v'_k)\}$$

LLM被提示分析前沿中的每条轨迹，识别关键瓶颈状态，并为其标注两类价值：
- **成就价值 $v$**：该状态已实现的累计奖励，反映利用潜力；
- **潜力价值 $v'$**：该状态可能通向的未实现进展，反映探索潜力。

选择阶段将存档中的候选状态与$W_{\mathrm{global}}$中的高价值模式进行语义对齐，自然平衡利用与探索。消融实验证实，移除这一价值分解机制（即直接用原始前沿轨迹选择状态）会导致性能显著下降（如Zork1从73.0降至62.0，Deephome从75.0降至61.3），验证了原则性价值估计的有效性。

### 3. 探索机制：从单轨迹试错到多路径优势反射

现有LLM智能体（ReAct、Reflexion、IGE）在选定状态后仅执行单条探索轨迹，在稀疏环境反馈下难以快速修正策略。GLoW提出**多路径优势反射（MAR）**，从同一状态采样$n$条轨迹，通过LLM比较轨迹间的差异来推断**语义优势信号**，将稀疏环境奖励转化为伪密集的进展指引。

MAR的理论基础源于优势函数的方差降低性质：

$$\mathrm{Var}[\hat{A}_{\mathrm{multi}}(s^*)] \leq \frac{\mathrm{Var}[\hat{A}_{\mathrm{single}}(s^*)]}{m}$$

多轨迹优势估计的方差上限为单轨迹估计的$1/m$，这为MAR在稀疏奖励下提供稳定进展信号提供了理论支撑。探索策略融合局部世界记忆、先前轨迹和前沿成功策略：

$$\pi_{\mathrm{explore}}(a|s_t, h_t) = \mathrm{Agent}_{\mathrm{LLM}}(s_t, h_t, W_{\mathrm{local}}, T_s, \mathcal{F})$$

消融实验表明，将MAR替换为单轨迹Reflexion后，性能大幅退化（Zork1: 73.0→70.0，Deephome: 75.0→56.7，Ludicorp: 73.7→54.7），证实了多轨迹对比在稀疏反馈环境下的关键作用。

### 创新协同效应

三个槽位的改变并非独立生效，而是形成互补协同。全局世界记忆识别“哪些状态值得探索”，局部世界记忆学习“在这些状态下如何有效探索”。消融实验的最终验证是：当全部组件移除后（等价于IGE+多路径Reflexion），性能未超越IGE基线，证明GLoW的性能提升来自各创新组件的系统性协同，而非简单叠加。

## 整体框架

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_bH5uHIVtTe/figures/001_Figure_1.jpg]]
*Figure 1: (a) Select procedure in GLoW, (b) Illustration of selection with Global World Memory*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_bH5uHIVtTe/figures/002_Figure_2.jpg]]
*Figure 2: (a) Explore procedure in GLoW, (b) Illustration of exploration with Local World Memory*

GLoW（Global-Local World Memory）是一个面向硬探索问题的LLM智能体框架，其核心思想是将探索过程分解为**状态选择**与**局部探索**两个阶段，并对应两种不同尺度的世界记忆进行学习。框架包含四个核心模块，形成一个闭环的探索流程：

1. **轨迹前沿（Trajectory Frontier） $\mathcal{F}$**：维护迄今为止发现的 $k$ 条最高价值轨迹，每条轨迹的价值 $v(\tau_i)$ 定义为轨迹中任意时刻达到的最大累计奖励 $v(\tau_i) = \max_{t \in [1,T]} \sum_{j=1}^{t} r_j^i$。当新轨迹加入时，按价值排序保留 top-k：$\mathcal{F}_{t+1} = \mathrm{top-k}(\mathcal{F}_t \cup \{\tau_{\mathrm{new}}\}, v)$。

2. **全局世界记忆模块（Global World Memory）**：LLM分析轨迹前沿 $\mathcal{F}$，提取每条轨迹中关键状态的**成就价值 $v$**（已获得的奖励）和**潜力价值 $v'$**（预示未来进展的语义信号），生成 $W_{\mathrm{global}} = g_{\mathrm{LLM}}(\mathcal{F}) = \{(s_1, v_1, v'_1), \dots, (s_k, v_k, v'_k)\}$。在状态选择阶段，将存档中的候选状态与 $W_{\mathrm{global}}$ 中的高价值模式进行语义对齐，实现原则性的利用-探索平衡。

3. **局部世界记忆模块（Multi-path Advantage Reflection, MAR）**：从选定状态出发采样 $n$ 条探索轨迹，LLM通过比较多条轨迹的差异推断关键状态-动作对的语义优势信号，将稀疏环境奖励转化为伪密集的进展指引，生成局部世界记忆 $W_{\mathrm{local}}$。

4. **探索策略（Exploration Policy）**：LLM智能体融合局部世界记忆、先前探索轨迹和前沿成功策略进行动作生成：$\pi_{\mathrm{explore}}(a|s_t, h_t) = \mathrm{Agent}_{\mathrm{LLM}}(s_t, h_t, W_{\mathrm{local}}, T_s, \mathcal{F})$。

整体流程为：每轮迭代中，全局世界记忆从状态存档中选择一个高潜力状态，通过重放操作序列恢复到该状态，然后局部世界记忆驱动多路径探索，探索结果更新存档和轨迹前沿。两个模块形成互补——全局记忆负责识别瓶颈区域和规划探索方向，局部记忆负责在具体状态下高效试错，共同解决稀疏反馈下的探索效率问题。

## 核心模块与公式推导

GLoW的核心架构由两个互补的世界记忆模块构成，分别对应硬探索问题中全局学习与局部试错两个瓶颈。

### 全局世界记忆模块

该模块维护一个**轨迹前沿（Trajectory Frontier）** $\mathcal{F}$，存储探索过程中发现的$k$条最高价值轨迹，而非传统Go-Explore方法中的孤立状态存档。轨迹价值定义为轨迹中任意时刻达到的最大累计奖励：

$$v(\tau_i) = \max_{t\in[1,T]} \sum_{j=1}^{t} r_j^i$$

该定义适配Jericho的稀疏奖励结构——奖励仅在关键里程碑出现，因此轨迹价值捕获的是“到达过的最远点”，而非终点奖励。当前沿加入新轨迹时，按价值函数$v$保留前$k$条：

$$\mathcal{F}_{t+1} = \mathrm{top{-}k}(\mathcal{F}_t \cup \{\tau_{\mathrm{new}}\}, v)$$

核心创新在于LLM对轨迹前沿的**价值分解**。LLM分析$\mathcal{F}$中每条轨迹的完整时序上下文——包括如何到达高价值状态、进展为何停滞——从中提取关键状态，并标注两类价值：

$$W_{\mathrm{global}} = g_{\mathrm{LLM}}(\mathcal{F}) = \{(s_1, v_1, v'_1), \dots, (s_k, v_k, v'_k)\}$$

其中：
- $v$（成就价值）：该状态实际达到的最高累计奖励，反映已完成的进度；
- $v'$（潜力价值）：LLM基于轨迹上下文推断的该状态可能解锁的后续进展，反映未实现的潜力。

这种双价值分解使状态选择能够原则性地平衡利用（选取高$v$状态深入）与探索（选取高$v'$状态尝试突破瓶颈）。状态选择时，LLM将存档中的候选状态与$W_{\mathrm{global}}$中的高价值模式进行语义对齐，而非依赖启发式或模糊的“有趣性”判断。

### 局部世界记忆模块：多路径优势反射（MAR）

局部世界记忆的目标是在稀疏环境奖励下为探索策略提供伪密集的进展信号。其理论基础是优势函数：

$$A(s, a) = Q(s, a) - V(s)$$

优势函数通过将动作价值与状态基线比较来降低方差，但在稀疏奖励环境中，单条轨迹无法提供有意义的优势信号。MAR的核心机制是：从同一状态$s^*$采样$n$条探索轨迹，利用LLM比较轨迹间的语义差异来推断优势信号，从而将稀疏奖励转化为密集的进展指引。

MAR的理论支撑来自方差缩减界：

$$\mathrm{Var}[\hat{A}_{\mathrm{multi}}(s^*)] \leq \frac{\mathrm{Var}[\hat{A}_{\mathrm{single}}(s^*)]}{m}$$

即多轨迹优势估计的方差上界为单轨迹估计方差除以轨迹数$m$，为MAR在稀疏反馈下降低方差提供了理论保证。

MAR生成的局部世界记忆$W_{\mathrm{local}}$标注了关键状态-动作对的语义优势信号，指导LLM驱动的探索策略：

$$\pi_{\mathrm{explore}}(a|s_t, h_t) = \mathrm{Agent}_{\mathrm{LLM}}(s_t, h_t, W_{\mathrm{local}}, T_s, \mathcal{F})$$

其中$h_t$为当前历史，$T_s$为此前从该状态出发的探索轨迹集合，$\mathcal{F}$为轨迹前沿中的成功策略参考。

### 模块协同

全局与局部世界记忆形成互补闭环：全局模块通过价值分解识别瓶颈和高潜力区域，决定“从哪里探索”；局部模块通过多轨迹对比降低方差，将稀疏奖励转化为语义优势信号，决定“如何探索”。状态恢复通过重放存储的动作序列确定性回到目标状态，使智能体可在关键节点分支探索。

**动作空间规模**：Zork1的词汇量为697时，每步可能的动作组合达到$O(697^5) = 1.64 \times 10^{14}$，体现了硬探索问题中动作空间的组合爆炸特性，进一步说明了原则性探索引导的必要性。

## 实验与分析

### 核心瓶颈与实验设计逻辑

硬探索问题中，LLM智能体面临双重挑战：全局层面缺乏持续积累有价值发现的机制，局部层面稀疏环境反馈导致难以快速修正策略。GLoW将这一问题分解为状态选择与探索两个阶段，分别对应全局世界记忆和局部世界记忆两个尺度。实验设计围绕三个核心假设展开：(1) 轨迹前沿的价值分解能否实现原则性状态选择；(2) 多路径优势反射（MAR）能否将稀疏奖励转化为语义优势信号；(3) 双尺度协同能否在样本效率上超越RL和MCTS方法。

所有LLM方法统一使用1000步交互预算，混合动作空间（Jericho有效动作作为软约束，同时允许自由形式生成），各方法独立运行3次报告最大得分均值与标准差。RL和MCTS方法沿用原论文的大量交互步数（10万至160万步）。数据污染分析（Table 5）显示GPT-4.1系列模型对Jericho游戏的先验知识极少（平均准确率10.4%-13.0%），排除了记忆依赖。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_bH5uHIVtTe/figures/007_Table_5.jpg]]
*Table 5: Data contamination analysis: LLM accuracy (%) on navigation questions without seeing gameplay*

### 主实验结果

**Table 1** 展示了GLoW与RL、MCTS和LLM三类基线在10个Jericho游戏上的对比。核心发现如下：

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_bH5uHIVtTe/figures/003_Table_1.jpg]]
*Table 1: Comparison of RL-based, MCTS-based, and LLM-based methods on Jericho benchmark games. We report mean ± standard deviation over 3 runs following prior works (Tuyls et al., 2022; Shi et al., 2025). Bold indicates best overall performance, and underline indicates second-best. Steps shows total environment interactions. The color of game names indicates original game difficulty categories from Hausknecht et al. (2020): extreme, difficult, and possible. GLoW achieves stateof-the-art among LLM-based approaches in 7/10 games, and is overall best among all compared approaches in 3/10, second-best in 5/10*

**LLM方法SOTA**：GLoW在7/10游戏上取得LLM方法中的最佳性能，远超ReAct、Reflexion、ICRL和IGE。在Zork1上达到73.0±4.5，相比IGE（43.3±8.5）提升29.7分，相比ICRL（51.7）提升21.3分。GLoW在8/10游戏上显著优于IGE，验证了双尺度世界记忆相比Go-Explore启发式选择的优势。

**接近或超越RL SOTA**：GLoW在Deephome上达到75.0±8.7，接近RL方法XTX的77.7±2.1（差距仅2.7分）；在Enchanter上达到61.7±20.1，超越XTX的52.0；在Ludicorp上达到73.7±11.0，接近XTX的78.8。考虑到GLoW仅使用1000步，而XTX使用80万步（800倍差距），这一结果体现了双尺度记忆在样本效率上的根本性优势。

**与MCTS方法对比**：GLoW在Zork1（73.0 vs MC-DML 48.66）、Deephome（75.0 vs 67.0）和Ludicorp（73.7 vs 19.67）上均显著超越MC-DML，表明基于LLM的价值分解和多轨迹对比比MCTS中的先验引导更有效。

**Table 4** 展示了GLoW在更强模型GPT-4.1上的可扩展性：在6个Extreme/Difficult游戏中，GLoW在4个游戏上超越所有先前方法，在5/6游戏上超越XTX。Enchanter达到98.3±4.7，Zork1达到103.0±6.8，Deephome达到114.7±27.8，显示GLoW性能随模型能力提升而持续增长。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_bH5uHIVtTe/figures/006_Table_4.jpg]]
*Table 4: Results comparing GPT-4.1 mini and GPT-4.1 on Extreme/Difficult games. We include XTX, the strongest RL baseline, for reference*

### 消融实验

**Table 2** 系统消融了GLoW的三个核心组件：

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_bH5uHIVtTe/figures/004_Table_2.jpg]]
*Table 2: Ablation study on GLoW components. We evaluate the contribution of: (1) Local world memory through MAR, (2) Global world memory for state selection, (3) trajectory frontier F*

**移除局部世界记忆（MAR）**：将MAR替换为单轨迹Reflexion后，性能显著下降。Deephome从75.0降至56.7（-18.3），Ludicorp从73.7降至54.7（-19.0），Enchanter从61.7降至51.7（-10.0）。这证实了MAR的多轨迹优势反射机制比简单的自我反思更有效——通过比较同一状态的多条轨迹，MAR能推断出Reflexion无法捕捉的语义优势信号。

**移除全局世界记忆的状态选择**：直接使用原始前沿轨迹选择状态（不经LLM价值分解）导致性能明显降低。Zork1从73.0降至62.0（-11.0），Deephome从75.0降至61.3（-13.7）。这表明LLM从轨迹前沿中提取成就价值v和潜力价值v'的原则性分解，是实现有效状态选择的关键。

**移除轨迹前沿F**：进一步退化至纯状态存档后，Zork1降至61.7，Enchanter降至53.3。这说明保留完整轨迹上下文（而非孤立状态）对于LLM理解“如何到达高价值状态”和“为何进展停滞”至关重要。

**组件协同效应**：全部组件移除后（等价于IGE+多路径Reflexion），性能未超越IGE基线（Zork1 44.3，Deephome 71.3），证明GLoW的性能提升来自各组件的协同效应，而非简单的多路径探索。

### 探索参数n的权衡

**Table 3** 展示了每状态探索次数n对全局-局部学习平衡的影响。n=1时MAR关闭，性能最低（Zork1 66.0）；n=5时局部学习过度，状态选择频率降低（最少仅3次选择），性能同样下降。n=3在全局探索覆盖度与局部学习深度之间取得最佳平衡——既保证了足够的局部轨迹进行优势反射（n-1=2条局部轨迹加前沿轨迹），又维持了合理的状态选择频率（最少6次选择）。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_bH5uHIVtTe/figures/005_Table_3.jpg]]
*Table 3: Controlling the focus on global (less explorations per state but more frequent state selection) vs local learning (more explorations per state). The results demonstrate n { = } 3 explorations from promising states strikes a good balance between the two*

### 失败模式与局限性

GLoW在实验中暴露出两类结构性失败模式：

**状态选择的保守性**：在Zork1中，智能体反复选择早期低分状态，未能识别前沿状态已拥有所需物品，导致重复已完成的子任务。这反映了LLM在全局价值分解时对“潜力价值v'”的估计存在偏差——未能准确识别哪些状态已无进一步探索价值。

**多步依赖推理不足**：在Deephome中，智能体激活发电机后未利用新解锁的铁路系统，直接尝试后续目标而失败。这暴露出GLoW对多阶段路径的系统性推理缺陷——即使局部探索发现了新能力，全局记忆也未能将“能力获取”与“路径解锁”建立因果关联。

此外，状态恢复依赖环境确定性，当前实现不适用于随机环境。LLM推理成本较高（Table 6-7显示每次运行消耗数百万输入令牌），虽然样本效率卓越，但API成本高于简单基线。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_bH5uHIVtTe/figures/008_Table_6.jpg]]
*Table 6: Comparison of LLM API costs with GPT-4.1-mini. We report the average token consumption and costs across 6 games (Zork1, Zork3, Deephome, Ludicorp, Detective, Temple)*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_bH5uHIVtTe/figures/009_Table_7.jpg]]
*Table 7: Comparison of LLM API costs with GPT-4.1. We report the average token consumption and costs across the same 6 games*

### 模型能力的影响

**Table 8** 显示GLoW性能随模型能力单调增长：GPT-4.1-nano在Zork1上仅43.0，GPT-4.1-mini达到73.0，GPT-4.1达到103.0。较小模型在潜力价值v'的估算上存在明显退化（如未能推断出关键地点），表明全局世界记忆的价值分解能力是模型依赖的瓶颈。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_bH5uHIVtTe/figures/010_Table_8.jpg]]
*Table 8: Impact of model capability on GLoW performance. Scores are mean ± standard deviation over 3 runs*

## 方法谱系与知识库定位

### 硬探索问题的历史谱系与GLoW的定位

硬探索问题（hard-exploration problems）的核心矛盾在于稀疏环境反馈与巨大动作空间之间的张力。以Jericho文本游戏为例，Zork1的词汇量为697，单步有效动作空间可达 $O(697^5) = 1.64 \times 10^{14}$，而奖励仅在完成特定子目标时才出现。这一特性使传统RL方法不得不依赖海量交互来碰触稀疏奖励信号。

**RL-based方法**代表了第一代解决方案。**DRRN** (He et al., 2016) 采用基于价值的深度强化学习处理选择式游戏，但难以应对自由文本生成的动作空间。**KG-A2C** (Ammanabrolu & Hausknecht, 2020) 引入动态知识图谱作为状态表示，**RC-DQN** (Guo et al., 2020) 结合阅读理解与DQN，均试图通过结构化表示缓解探索困难。最具代表性的是 **XTX** (Tuyls et al., 2022)，它将Go-Explore范式与模仿学习和好奇心驱动的DQN探索相结合，在多个Jericho游戏上建立了RL的SOTA，但需要高达80万步的环境交互。

**MCTS-based方法**通过树搜索结构化探索。**MC-LAVE** (Jang et al., 2021) 将语言驱动探索与蒙特卡洛树搜索结合，**MC-DML** (Shi et al., 2025) 进一步引入LLM作为动作先验和跨试验记忆。然而，MCTS方法在文本游戏的组合爆炸动作空间下仍面临搜索效率瓶颈。

**LLM-based方法**代表了范式转移：利用LLM的常识推理能力替代随机探索。**ReAct** (Yao et al., 2023) 将推理与行动交织，**Reflexion** (Shinn et al., 2023) 通过跨episode的自我反思改进策略，**ICRL** (Song et al., 2026) 将历史轨迹作为上下文进行上下文强化学习。这些方法在局部试错上有效，但缺乏跨episode的全局学习机制。

**Go-Explore范式**在LLM时代的延续是理解GLoW定位的关键。Go-Explore的核心思想是“先回到有希望的状态，再探索”，分为选择（Select）和探索（Explore）两个阶段。**IGE** (Lu et al., 2025) 首次将Go-Explore与LLM智能体结合，使用LLM判断状态的“有趣性”进行选择，再用ReAct进行单轨迹探索。然而，IGE在**选择阶段**依赖LLM内部的模糊判断，缺乏对轨迹上下文的系统性价值估计；在**探索阶段**仅执行单轨迹探索，无法利用多轨迹对比降低稀疏奖励下的方差。

**GLoW的突破**在于同时升级了Go-Explore的两个阶段：

| 组件 | IGE（基线） | GLoW（本文） | 核心改进 |
|------|-----------|------------|---------|
| 全局记忆表示 | 状态存档 + LLM内部“有趣性”判断 | 轨迹前沿 $\mathcal{F}$ + LLM价值分解生成 $W_{\mathrm{global}} = \{(s_i, v_i, v'_i)\}$ | 从孤立状态到完整轨迹上下文；从模糊判断到原则性价值估计（成就价值 $v$ + 潜力价值 $v'$） |
| 状态选择 | LLM.select_promising（启发式） | 将存档状态与 $W_{\mathrm{global}}$ 中的高价值模式对齐 | 平衡利用与探索，基于可解释的价值信号 |
| 探索机制 | 单轨迹ReAct | 多路径优势反射（MAR）：从同一状态采样 $n$ 条轨迹，LLM比较轨迹差异推断语义优势 | 将稀疏奖励转化为伪密集进展信号；方差降低至单轨迹的 $1/m$ |

### 方法边界与适用条件

**适用场景**：
- 稀疏奖励环境，奖励仅在完成特定子目标时出现
- 环境状态可被文本或符号化表示，便于LLM进行语义分析
- 环境具有确定性，支持通过重放操作序列回到目标状态
- 交互预算受限（千步级别），但可接受较高的LLM推理成本

**不适用场景**：
- **随机环境**：GLoW当前的状态恢复机制依赖环境确定性，通过重放存储的动作序列回到目标状态。在随机环境中，相同动作序列可能产生不同结果，导致状态恢复失败。
- **实时性要求高的任务**：每次状态选择和MAR分析都需要大量LLM调用，延迟较高。
- **多步依赖关系复杂的任务**：GLoW在Deephome中暴露出对多阶段路径的系统性推理缺陷——智能体激活发电机后未能识别新解锁的铁路系统，直接尝试后续目标而失败。这表明当前方法在需要多步因果推理的场景中存在瓶颈。

### 局限性与开放问题

**已验证的局限性**（来自论文实验观察）：

1. **状态选择的保守性**：在Zork1中观察到智能体反复选择早期低分状态，未能识别前沿状态已拥有所需物品，导致重复已完成子任务。这表明LLM对全局世界记忆的分析有时过于保守，未能充分信任已取得的进展。

2. **多步依赖关系推理不足**：如前述Deephome案例，智能体在获取关键能力（激活发电机）后，未能规划利用该能力的中间路径。这暴露了当前架构在系统性多步推理上的结构性缺陷。

3. **状态恢复的环境假设**：当前实现假设环境可重放操作回到目标状态，限制了在随机环境中的适用性。

4. **LLM推理成本**：虽然样本效率卓越（仅1000步交互），但每次运行消耗数百万输入令牌。以GPT-4.1-mini为例，GLoW在6个游戏上的平均API成本高于ReAct和IGE基线。成本主要来自全局世界记忆的LLM分析和MAR的多轨迹比较。

5. **验证领域单一**：仅在Jericho文本游戏上验证，尚未在其他硬探索领域（如具身导航、复杂规划、开放世界游戏）中测试泛化性。

**开放问题**（来自论文讨论与自然延伸）：

1. **如何增强多步依赖关系的系统性推理？** 当智能体获得关键能力后，如何自动识别该能力解锁的新路径，并规划中间步骤？这可能需要在全局世界记忆中引入因果图或依赖关系显式建模。

2. **状态恢复机制如何扩展到随机环境？** 一个可能的方向是将“回到目标状态”视为目标导向的子任务，由LLM智能体自主规划返回路径，而非依赖确定性重放。

3. **双尺度世界记忆架构能否泛化到其他领域？** 该架构的核心思想——全局尺度识别瓶颈和高潜力区域，局部尺度通过多轨迹对比降低方差——在理论上适用于任何稀疏反馈的序列决策问题。在具身导航、机器人操作、开放世界游戏中的验证是重要的下一步。

4. **如何在保持推理质量的前提下降低令牌消耗？** 当前全局世界记忆的LLM分析每次都需要处理完整的轨迹前沿，成本随前沿大小线性增长。可能的优化方向包括：轨迹摘要压缩、增量更新机制、或使用更小的专用模型进行价值分解。

5. **潜力价值 $v'$ 的估算在小模型上的退化问题**：实验显示，较小模型（如GPT-4.1-nano）在全局分析中未能推断出关键地点，导致 $v'$ 的估算质量明显下降。如何提升较小模型在全局分析中的表现，或设计更鲁棒的价值分解提示策略，是降低方法门槛的关键。

6. **全局与局部学习的自适应平衡**：当前通过固定参数 $n$（每状态探索次数）控制全局-局部平衡。能否设计自适应机制，根据探索进展动态调整 $n$？例如，当检测到高潜力状态时增加局部探索深度，当全局覆盖不足时增加状态选择频率。

## 原文 PDF

![[paperPDFs/ICLR_2026/Dual_Scale_World_Memory_for_LLM_Agents_towards_Hard_Exploration_Problems.pdf]]
