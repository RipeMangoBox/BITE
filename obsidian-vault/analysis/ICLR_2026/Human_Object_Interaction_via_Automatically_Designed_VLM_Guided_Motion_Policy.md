---
title: "Human-Object Interaction via Automatically Designed VLM-Guided Motion Policy"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Human_Object_Interaction_via_Automatically_Designed_VLM_Guided_Motion_Policy.pdf
openreview_forum_id: LfkPlFTfe0
aliases:
- VGRMDRH
- HOIADVGMP
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "使用VLM生成的细粒度时空二分图（RMD）自动构建目标状态与奖励函数，替代手动奖励设计，实现物理上合理的长视距交互。"
primary_logic: "人-物交互可抽象为人体部件与物体部件间的相对运动动力学；通过VLM引导的RMD表示，不仅可以推理离散接触，还能编码连续的运动动态，从而支持更自然和可泛化的运动策略学习。"
claims:
- "RMD能够自动构建目标状态和奖励函数，无需手动设计。"
- "在长视距多任务场景中，我们的方法在静态交互完成率上达到75.1%，远高于最佳基线UniHSI的37.2%。"
- "消融实验表明，移除RMD中的运动学关系编码或动态编码会显著降低性能。"
- "用户研究表明，所提方法在运动真实性和任务一致性上均优于现有方法（平均分数4.0 vs ≤3.4）。"
---

# Human-Object Interaction via Automatically Designed VLM-Guided Motion Policy

> [!tip] 核心洞察
> 人-物交互可抽象为人体部件与物体部件间的相对运动动力学；通过VLM引导的RMD表示，不仅可以推理离散接触，还能编码连续的运动动态，从而支持更自然和可泛化的运动策略学习。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于自动设计的VLM引导运动策略的人-物交互 |
| 英文题名 | Human-Object Interaction via Automatically Designed VLM-Guided Motion Policy |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=LfkPlFTfe0); [Project](https://vlm-rmd.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | VLM-Guided Relative Movement Dynamics (RMD) for HOI |
| Dataset | InterPlay (Static Interaction subset), InterPlay (Dynamic Interaction subset), InterPlay (Hybrid subset), Single-task: Reach |

> [!tip] 效果简介
> - InterPlay (Static Interaction subset) 上，Completion Rate (%) ↑ 为 75.1，对比 37.2 (UniHSI)，变化 +37.9。
> - InterPlay (Dynamic Interaction subset) 上，Completion Rate (%) ↑ 为 71.2，对比 52.5 (TokenHSI*)，变化 +18.7。
> - InterPlay (Hybrid subset) 上，Sub-step Completion Ratio (%) ↑ 为 71.8，对比 60.1 (TokenHSI*)，变化 +11.7。

## 概述

### 问题瓶颈

物理仿真环境中的人-物交互（Human-Object Interaction, HOI）运动合成面临两个核心瓶颈。其一，现有方法对高质量动捕数据的依赖性强，且需要针对每个具体任务手动设计奖励函数，难以规模化扩展到多样化的交互场景。其二，大多数方法仅支持静态物体，无法有效处理动态物体和铰接物体，也难以在长视距、多步骤的交互序列中保持连贯性与物理合理性。**UniHSI**（Xiao et al., 2024）虽然通过LLM自动生成目标和奖励，但其链式接触（Chain-of-Contacts）表示仅限于离散接触事件，缺乏对连续运动动态的编码能力。

### 核心方法

本文提出**VLM-Guided Relative Movement Dynamics（RMD）**，一个统一的物理基HOI框架。其核心思路是将人-物交互抽象为人体部件与物体部件之间的相对运动动力学，并通过视觉-语言模型（VLM）自动生成结构化的交互计划，进而驱动强化学习策略。

关键创新包括：
- **RMD表示**：一种细粒度时空二分图，编码人体部件与物体部件之间的相对运动模式（静止接触、接近、远离、无一致趋势），同时捕捉离散接触和连续运动动态。
- **VLM引导的自动设计**：VLM规划器接收高层次指令和环境顶视图，生成多步交互计划（RMD序列），框架据此自动构建目标状态和奖励函数，无需任何手动奖励工程。
- **长视距多任务调度**：通过阶段转换阈值自动切换子任务，实现从“走到物体旁”到“坐下”等完整交互序列的连贯执行。

### 主要结果

在InterPlay基准的长视距多任务场景中，所提方法在静态交互子集上的完成率达到**75.1%**，远超最佳基线UniHSI的37.2%（+37.9个百分点）；在动态交互子集上达到**71.2%**，领先TokenHSI的52.5%（+18.7个百分点）。单任务场景下，方法在搬运、推拉、开关、坐、躺、伸手等六类任务上均取得最优完成率和精度。消融实验证实，RMD中的运动学编码和动态编码对性能至关重要，移除任一项均导致显著下降。用户研究表明，所提方法在运动真实性（4.0±0.4）和任务一致性（4.1±0.3）上均优于对比方法（最高3.4±0.4）。

### 方法定位

与现有工作相比，本方法在八个关键维度上实现了全覆盖（Table 1），是首个同时支持铰接物体、动态物体、自动化奖励设计、长视距细粒度转换、HOI引导、多任务、高层规划和统一策略的框架。其核心区别在于用VLM引导的RMD替代了手动设计的接触链或关键姿势，将交互表示从离散事件层面提升到连续运动动力学层面。

## 背景与动机

### 问题背景：物理仿真中的人-物交互合成

在具身智能和角色动画领域，使物理仿真角色与三维环境中的物体进行自然、长视距的交互是一个核心挑战。这类交互——如搬起洗衣篮放入洗衣机、躺到床上、坐在桌前、推动沙发——要求角色不仅理解高层次的任务意图，还需在物理约束下生成连贯的、符合语义的运动序列。与纯运动学方法不同，基于物理仿真的方法必须同时处理接触动力学、平衡控制、物体操纵以及任务规划等多个耦合子问题。

### 现有方法的瓶颈

当前基于物理的人-物交互（Human-Object Interaction, HOI）合成方法主要存在以下结构性缺口：

**依赖昂贵数据与手动工程。** 基于运动模仿的方法（如**AMP**，Peng et al. 2021）需要高质量的动捕参考数据来训练对抗运动先验，但覆盖多样化交互场景的动捕数据获取成本极高。基于强化学习的方法（如**InterPhys**，Hassan et al. 2023；**TokenHSI**，Pan et al. 2025）则需要针对每个具体任务手动设计奖励函数和状态机，这种“奖励工程”不仅耗时，而且难以泛化到新任务和新物体。

**对动态和铰接物体的支持不足。** 多数现有方法假设交互对象是静态的（如固定的椅子、桌子），无法有效处理动态物体（如可推动的沙发）或铰接物体（如可打开的抽屉、门）。**UniHSI**（Xiao et al. 2024）虽然通过LLM实现了静态交互场景下的自动目标生成，但其“接触链”（Chain-of-Contacts, CoC）抽象仅编码离散的接触事件，缺失了对连续运动动态的建模能力，因而无法处理需要持续相对运动协调的动态交互。

**长视距多任务调度的缺失。** 现实中的交互往往是多步骤的——例如“拿起篮子、走到洗衣机前、放下篮子”——每一步涉及不同的子目标和运动模式。现有方法要么只能执行单任务策略，要么依赖手工设计的有限状态机进行任务切换，缺乏统一的、可自动生成的多步规划机制。

### 核心洞察与动机

本文的核心洞察是：人-物交互本质上可以抽象为**人体部件与物体部件之间的相对运动动力学**。无论是“手靠近杯子”还是“背靠向椅子”，交互的语义都可以通过人体关节/刚体与物体表面点之间的空间关系（接近、远离、静止接触）及其时间演化来刻画。这一抽象具有两个关键优势：

1. **统一表示能力**：离散接触和连续运动动态可以被编码在同一个时空二分图框架中，从而同时覆盖静态、动态和铰接物体的交互需求。
2. **可被VLM理解与生成**：这种结构化的部件级关系表示，恰好可以被视觉-语言模型（Vision-Language Model, VLM）基于其世界知识进行推理和规划，从而替代手动奖励设计。

基于上述洞察，本文提出**VLM引导的相对运动动力学（VLM-Guided Relative Movement Dynamics, RMD）**，旨在构建首个统一的、基于物理的HOI框架，利用VLM自动生成目标状态和奖励函数，驱动物理角色完成长视距、多类型的交互任务。

## 核心创新

本工作针对现有物理仿真人-物交互（HOI）方法的两个核心瓶颈——依赖昂贵动捕数据与手动奖励工程、无法有效处理动态对象和长视距交互——提出了首个统一的、基于VLM引导的物理仿真HOI框架。其关键创新在于引入了一种细粒度时空二分图表示**相对运动动力学（Relative Movement Dynamics, RMD）**，并以此作为VLM与强化学习策略之间的桥梁，实现了目标状态与奖励函数的全自动构建。

### 从离散接触到连续运动动态的表示升级

现有方法（如**UniHSI**的接触链CoC，Xiao et al., 2024）将人-物交互抽象为离散的接触事件序列，难以捕捉交互过程中人体部件与物体部件之间连续的运动趋势（如手部接近杯子、身体远离桌面）。本工作的核心洞察在于：人-物交互本质上可抽象为两组刚体——人体部件与物体部件——之间随时间演化的相对运动。

基于此，方法提出RMD表示，将交互形式化为一个带权时空二分图 $\mathcal{B} = (V, E, w)$，其中节点集 $V = P_H \cup P_O$ 包含人体部件和物体部件，边集 $E \subseteq P_H \times P_O$ 编码部件间的配对关系，而边权重 $w: E \to \{0, 1, 2, 3\}$ 则显式编码相对运动模式：0为静止接触、1为接近、2为远离、3为无一致趋势。这一设计将交互表示从“是否接触”升级为“如何运动”，为VLM提供了更丰富的语义锚点，也为策略学习提供了更细粒度的监督信号。

### 从手动奖励工程到VLM驱动的自动设计

传统物理仿真HOI方法需要针对每个任务手动设计奖励函数（如**InterPhys**、**TokenHSI**），或依赖LLM生成代码但需迭代搜索（如Eureka）。本工作通过VLM-Guided RMD Planner实现了目标状态与奖励函数的全自动生成：

- **自动目标状态构造**：VLM根据高层指令和环境顶视图，生成多步交互计划 $\mathcal{D} = \{\mathcal{G}_1, \ldots, \mathcal{G}_N\}$，其中每步 $\mathcal{G}_i = \{\mathcal{T}_H, \mathcal{T}_O, B\}$ 指定人体根目标位置、物体根目标位置和RMD二分图。这些结构化输出被直接转化为RL策略的目标状态 $\mathbf{g}_t = \{\mathbf{s}_t^{\mathrm{RMD}}, \mathbf{d}_t, \mathbf{h}_t, \mathbf{o}_t\}$，包含RMD状态、目的地、高度图和物体状态。

- **自动奖励设计**：基于VLM规划的RMD边权重，框架自动合成任务奖励 $r^G = \lambda_{\mathrm{RMD}} \cdot r_{\mathrm{RMD}} + \lambda_h \cdot r_d^{\mathrm{h}} + \lambda_o \cdot r_d^{\mathrm{o}}$。其中 $r_{\mathrm{RMD}}$ 鼓励每个人体-物体部件对遵循VLM指定的相对运动模式（接近、远离、静止接触等），$r_d^{\mathrm{h}}$ 和 $r_d^{\mathrm{o}}$ 分别鼓励人体根和物体根趋向目标位置。

这一设计消除了对手动奖励工程的依赖，同时使框架天然支持静态、动态和铰接物体交互——这是Table 1中唯一覆盖全部八项关键特性的方法。

### 面向长视距的多步规划与自动阶段切换

长视距交互需要协调多个子任务的有序执行。本工作通过VLM的多步规划能力，将复杂任务分解为RMD序列，并通过阶段转换机制实现自动切换：当当前子任务的任务奖励 $r^G$ 超过阈值0.9时，策略自动过渡到下一步交互计划。相比基于规则的有穷状态机（FSM），这种VLM驱动的调度方式无需手动定义状态转移条件，且能根据场景上下文灵活调整子任务顺序。

### 消融验证的关键设计选择

消融实验证实了RMD表示中几个关键设计的必要性：
- **多对多表示优于简化变体**：将RMD退化为一对一（one-one）或多对一（multi-one）表示会导致性能显著下降，尤其在需要全身协调的复杂交互（如躺下、坐下）上。这验证了同时建模多个人体部件与多个物体部件之间运动关系的必要性。
- **时空编码缺一不可**：移除运动学编码 $(\tilde{p}_t^{ij}, \tilde{v}_t^{ij})$ 或动态编码 $(w_t'^{ij})$ 均导致性能退化，表明同时捕捉空间关系与时序动态是RMD有效性的基础。

综上，本工作的核心创新不在于提出新的RL算法或VLM架构，而在于设计了RMD这一连接VLM语义理解与物理策略学习的表示层，使得“自动设计”成为可能，并在静态交互（完成率75.1% vs UniHSI 37.2%）和动态交互（71.2% vs TokenHSI 52.5%）上均取得显著提升。

## 整体框架

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_LfkPlFTfe0/figures/002_Table_1.jpg]]
*Table 1: Comparative analysis of key features between ours and other methods*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_LfkPlFTfe0/figures/003_Figure_2.jpg]]
*Figure 2: An overview of our architecture. Receiving instruction and environment context as input, the VLM-Guided RMD Planner generates a multi-step interaction plan in the form of RMD. Based on this plan, our framework automatically designs both goal states and reward functions, enabling the VLM-Guided Motion Policy to execute the interaction step by step*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_LfkPlFTfe0/figures/001_Figure_1.jpg]]
*Figure 1: Our framework automatically constructs both goal states and reward functions for diverse interaction tasks in reinforcement learning. By leveraging VLM guidance, the learned motion policy drives physics-based characters to perform coherent, long-horizon interactions with static and dynamic objects, producing natural and task-consistent behaviors*

本工作提出首个统一的基于物理的人-物交互（HOI）合成框架，利用视觉语言模型（VLM）的世界知识实现长视距交互，支持静态、动态和铰接对象。框架的核心创新在于引入**VLM引导的相对运动动力学（VLM-Guided Relative Movement Dynamics, RMD）**——一种细粒度时空二分图表示，用以自动构建强化学习所需的目标状态和奖励函数，从而消除手动奖励工程。

### 系统流水线

整体架构由四个关键模块串联构成，形成从高层指令到物理执行的端到端流程（图2）：

1. **VLM引导的RMD规划器（VLM-Guided RMD Planner）**  
   接收高层文本指令 $I$ 和环境顶视图上下文图像 $C$，利用GPT-4V生成结构化的多步交互计划 $\mathcal{D} = \{\mathcal{G}_1, \mathcal{G}_2, \ldots, \mathcal{G}_N\}$。每一步 $\mathcal{G}_i$ 包含人体根目标位置 $\mathcal{T}_H$、物体根目标位置 $\mathcal{T}_O$ 和 RMD 二分图 $B$。

2. **目标状态构造器（Goal State Constructor）**  
   将VLM输出的交互计划转化为目标条件化策略所需的目标状态表示 $\mathbf{g}_t$，包括RMD状态 $\mathbf{s}_t^{\mathrm{RMD}}$、目的地 $\mathbf{d}_t$、高度图 $\mathbf{h}_t$ 和物体状态 $\mathbf{o}_t$。

3. **奖励函数生成器（Reward Function Generator）**  
   基于VLM计划自动合成任务奖励 $r^G$，由三项组成：RMD对齐奖励 $r_{\mathrm{RMD}}$（鼓励人体-物体部件对遵循规划的运动模式）、人体目标奖励 $r_d^{\mathrm{h}}$ 和物体目标奖励 $r_d^{\mathrm{o}}$。总奖励 $r_t$ 进一步融合基于AMP判别器的风格奖励 $r^S$，以保障运动自然性。

4. **VLM引导的运动策略（VLM-Guided Motion Policy）**  
   采用目标条件化的PPO训练策略网络，输出PD控制器的目标关节位置，驱动物理角色（15个刚体部件、28个关节）执行交互。子任务间通过阈值机制自动切换：当任务奖励 $r^G$ 超过0.9时，策略转入下一个计划步。

### 核心表示：RMD二分图

框架的关键洞察在于将人-物交互抽象为人体部件与物体部件之间的相对运动动力学。RMD通过二分图 $\mathcal{B} = (V, E, w)$ 编码这一抽象，其中顶点集 $V = P_H \cup P_O$ 包含人体部件（如手、脚、躯干）和物体部件，边权重 $w: E \to \{0,1,2,3\}$ 表示四种相对运动模式：静止接触（0）、接近（1）、远离（2）和无一致趋势（3）。该表示不仅推理离散接触，还编码连续的运动动态，使得VLM能够生成语义扎根的、交互感知的运动引导。

### 关键特性对比

如表1所示，本框架是唯一同时支持以下全部特性的方法：铰接对象交互、自动化奖励设计、动态对象交互、细粒度长视距转换、HOI运动引导、多任务统一策略和高层规划。相比之下，**UniHSI**（Xiao et al., 2024）仅支持静态交互和自动化奖励设计，**TokenHSI**（Pan et al., 2025）和**InterPhys**（Hassan et al., 2023）则依赖手动奖励工程。

## 核心模块与公式推导

### 整体架构

本方法由三个核心模块构成流水线：**VLM引导的RMD规划器**（VLM-Guided RMD Planner）接收高层指令与环境上下文，生成多步交互计划；**目标状态构造器**与**奖励函数生成器**将计划自动转化为强化学习所需的目标表示与奖励信号；**VLM引导的运动策略**（基于PPO）在物理仿真中执行交互，并由基于AMP的风格判别器提供运动自然度奖励（Figure 2）。

### 关键表示：相对运动动力学二分图（RMD）

核心洞察在于：人-物交互可抽象为人体部件集合与物体部件集合之间随时间演化的相对运动。将人体部件集合定义为 $P_H = \{p_{h_1}, p_{h_2}, ..., p_{h_m}\}$，物体部件集合定义为 $P_O = \{p_{o_1}, p_{o_2}, ..., p_{o_n}\}$，则交互的细粒度时空结构可形式化为二分图：

$$\mathcal{B} = (V, E, w), \quad V = P_H \cup P_O, \quad E \subseteq P_H \times P_O, \quad w: E \to \{0, 1, 2, 3\}$$

其中边权重 $w$ 编码该人体-物体部件对之间的相对运动模式：
- **0**：静止接触（stationary contact）
- **1**：接近（approaching）
- **2**：远离（separating）
- **3**：无一致趋势（no consistent trend）

每个交互步 $\mathcal{G}_i = \{\mathcal{T}_H, \mathcal{T}_O, B\}$ 指定人体根目标位置 $\mathcal{T}_H$、物体根目标位置 $\mathcal{T}_O$ 和该步的RMD图 $B$。VLM规划器输出的多步交互计划为 $\mathcal{D} = \{\mathcal{G}_1, \mathcal{G}_2, \ldots, \mathcal{G}_N\}$。

### 目标状态自动构造

对于RMD图中的每条边 $(i,j) \in E$，首先计算人体关节 $i$ 与物体表面点 $j$ 之间的相对位置和相对速度：

$$\tilde{\mathbf{p}}_{ij} = \mathbf{p}_{o_j}^p - \mathbf{p}_{h_i}^p, \quad \tilde{\mathbf{v}}_{ij} = \mathbf{p}_{o_j}^v - \mathbf{p}_{h_i}^v$$

RMD状态向量通过堆叠所有边的相对位置、相对速度以及边权重的独热编码 $\mathbf{w}_{ij}'$ 得到：

$$\mathbf{s}_t^{\mathrm{RMD}} = \operatorname{concat}_{(i,j) \in E} \left[ \tilde{\mathbf{p}}_{ij}, \tilde{\mathbf{v}}_{ij}, \mathbf{w}_{ij}' \right] \in \mathbb{R}^{|E| \times (3+3+4)}$$

完整的目标状态表示由RMD状态、人体目的地 $\mathbf{d}_t$、高度图 $\mathbf{h}_t$ 和物体状态 $\mathbf{o}_t$ 拼接而成：

$$\mathbf{g}_t = \big\{ \mathbf{s}_t^{\mathrm{RMD}}, \mathbf{d}_t, \mathbf{h}_t, \mathbf{o}_t \big\}$$

### 奖励函数自动设计

任务奖励 $r^G$ 由三项加权合成：RMD对齐奖励、人体目的地奖励和物体目的地奖励。

人体和物体目的地奖励鼓励根节点趋向VLM指定的目标位置：

$$r_d^{\mathrm{h}} = \exp\left( - \left\| x_t^{\mathrm{h}} - \mathbf{d}_t^{h} \right\|^2 \right), \quad r_d^{\mathrm{o}} = \exp\left( - \left\| x_t^{\mathrm{o}} - \mathbf{d}_t^{o} \right\|^2 \right)$$

RMD奖励对所有人体-物体部件对进行加权求和，每对奖励 $r_{\mathrm{rmd}}$ 根据VLM规划的边权重 $w_{ij}$ 采用不同的函数形式（完整定义见附录C Eq. 16），分别鼓励静止接触时无相对滑动、接近时以适当速度靠近、远离时以适当速度分开：

$$r_{\mathrm{RMD}} = \sum_{(i,j) \in E} \lambda_{ij} \cdot r_{\mathrm{rmd}} \big( \tilde{\mathbf{p}}_{ij}, \tilde{\mathbf{v}}_{ij}, w_{ij} \big)$$

综合任务奖励为：

$$r^G \left( \mathbf{s}_t, \mathbf{g}_t, \mathbf{s}_{t+1} \right) = \lambda_{\mathrm{RMD}} \cdot r_{\mathrm{RMD}} + \lambda_h \cdot r_d^{\mathrm{h}} + \lambda_o \cdot r_d^{\mathrm{o}}$$

每时间步的总奖励由任务奖励与AMP风格判别器提供的风格奖励 $r^S$ 加权构成：

$$r_t = \alpha_{\mathrm{task}} \, r^G \left( \mathbf{s}_t, \mathbf{g}_t, \mathbf{s}_{t+1} \right) + \alpha_{\mathrm{style}} \, r^S \left( \mathbf{s}_t, \mathbf{s}_{t+1} \right)$$

### 多步调度机制

策略采用目标条件化的PPO训练。当某步的任务奖励 $r^G$（取值范围 $[0,1]$）超过阈值0.9时，策略自动切换至VLM规划的下一个交互步，实现无需手工状态机的长视距任务调度。消融实验表明该阈值敏感：过高（如0.95）会导致完成率大幅下降，0.90为最优设置（Table 6）。

## 实验与分析

### 核心实验设计

实验围绕三个层次展开：(1) 长视距多任务场景下与前沿物理基线的综合对比；(2) 单任务场景下的精度与成功率评估；(3) RMD表示各组件、VLM选择、阶段转换阈值的消融研究。所有方法统一使用Proximal Policy Optimization（PPO）训练，物理角色由15个刚体部件和28个关节构成，通过PD控制器驱动。评估数据集按交互对象类型划分为静态交互（Static）、动态交互（Dynamic）和混合场景（Hybrid）三个子集。

### 长视距多任务场景：主结果

**Table 2** 报告了核心对比结果。在静态交互子集上，本方法达到 **75.1%** 的完整任务完成率（Completion Rate），远超最强基线UniHSI（Xiao et al., 2024）的37.2%（+37.9个百分点）。子步骤完成率（Sub-step Completion Ratio）为86.2%，子步骤精度（Sub-step Precision）为7.7 cm，三项指标均显著领先。在动态交互子集上，完成率达到 **71.2%**，相比TokenHSI（Pan et al., 2025）的52.5%提升18.7个百分点。混合场景下，子步骤完成率为71.8%，较TokenHSI的60.1%提升11.7个百分点。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_LfkPlFTfe0/figures/004_Table_2.jpg]]
*Table 2: Comparison with baselines in a long-horizon multi-task scenario*

值得注意的是，UniHSI虽具备基于LLM的自动目标与奖励生成能力，但其离散接触链（Chain-of-Contacts）表示无法有效处理动态对象和需要从坐/卧姿态恢复的交互，导致在静态子集上完成率不足40%。InterPhys（Hassan et al., 2023）虽支持动态对象，但依赖手动奖励工程和对抗运动先验，在长视距序列中运动不稳定，完成率仅约30%。TokenHSI通过任务分词器实现了多技能调度，但缺乏细粒度的交互引导，在需要精确空间对齐的任务（如坐下、躺下后的起身恢复）上表现不佳。

### 单任务场景：精度与成功率

**Table 3** 展示了六个代表性单任务（Carry、Push、Open、Sit、Lie、Reach）上的详细对比。本方法在所有任务上均达到最高或可比性能。在需要恢复过程的静态交互任务（Sit、Lie）上，完成率和成功率优势尤为突出：UniHSI在Sit任务上成功率为0%，因其缺乏从坐姿恢复的机制；InterPhys虽能完成部分动作，但产生不自然的运动伪影（见 **Figure 3** 定性可视化）。在Reach任务上，本方法精度为1.9 cm，略优于UniHSI的2.1 cm，表明RMD表示在简单导航任务上同样有效。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_LfkPlFTfe0/figures/005_Table_3.jpg]]
*Table 3: Comparison with baselines in a single-task scenario*

### 消融研究：RMD表示的关键组件

**Table 3** 下半部分报告了RMD表示结构的消融实验：

- **多对多 → 多对一（multi-one）**：将物体简化为单一部件表示后，在Sit和Lie任务上性能显著下降，因为坐/躺动作需要人体多个部件（臀部、背部、手部）与物体多个部件（座面、靠背、扶手）之间的协调运动。多对一表示无法捕捉这种细粒度的空间关系。
- **多对一 → 一对一（one-one）**：进一步将交互限制为单个人体部件与单个物体部件的动态建模，性能进一步恶化，证实复杂交互需要全身边缘的联合表示。
- **移除运动学编码（w.o. $P_{ij}$, $V_{ij}$）**：去掉相对位置 $\tilde{\mathbf{p}}_{ij}$ 和相对速度 $\tilde{\mathbf{v}}_{ij}$ 后，策略失去了空间感知能力，无法判断人体部件与物体部件之间的距离和运动方向，导致完成率大幅下降。
- **移除动态编码（w.o. $W_{ij}$）**：去掉边权重 $w_{ij}$ 的独热编码后，策略无法区分接近、远离、静止接触等运动模式，在需要精细时序协调的任务上表现恶化。

这些消融结果一致表明：RMD的时空二分图结构——同时编码运动学关系和动态模式——是其有效性的因果瓶颈。仅保留其中任一组件都会导致性能的实质性退化。

### VLM规划器消融：模型选择与提示设计

**Table 5** 比较了不同VLM后端和提示策略的影响。GPT-4V在完整提示设计下表现最优（完成率53.8%，子步骤完成率71.8%）。使用简化提示后，GPT-4V性能下降，说明结构化的RMD输出格式和上下文描述对规划质量至关重要。LLaVA-1.6和Qwen-VL-Max的开源替代方案性能明显低于GPT-4V，但Qwen-VL-Max略优于LLaVA-1.6，表明更大规模VLM的语义理解能力与RMD规划质量正相关。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_LfkPlFTfe0/figures/016_Table_5.jpg]]
*Table 5: Comparison of VLM choice and prompt designs*

### 阶段转换阈值敏感性

**Table 6** 考察了任务奖励阈值（决定何时切换到下一交互步骤）的影响。阈值0.90达到最佳平衡：过低（0.80）导致子步骤执行不充分，精度下降；过高（0.95）使策略难以满足严苛的完成条件，完成率从53.8%骤降。这一敏感性揭示了当前设计中VLM规划器与物理策略之间的目标不匹配问题——VLM生成的理想化RMD目标可能无法在物理仿真中完美达成。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_LfkPlFTfe0/figures/017_Table_6.jpg]]
*Table 6: Comparison of threshold choice*

### 用户研究：运动真实性与任务一致性

**Table 7** 报告了用户研究结果。参与者在5分制下评估运动真实性（Motion Realism）和任务一致性（Task Consistency）。本方法获得 **4.0±0.4**（运动真实性）和 **4.1±0.3**（任务一致性），均显著高于所有基线方法（最高分别为TokenHSI的3.4±0.4和UniHSI的3.0±0.3）。这表明RMD引导的运动不仅物理上合理，在人类感知层面也更自然、更符合任务语义。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_LfkPlFTfe0/figures/018_Table_7.jpg]]
*Table 7: Comparison of motion realism and task consistency*

### 失败模式分析

综合定量结果和定性观察，主要失败模式包括：

1. **VLM规划错误**：在混合任务上，VLM生成的RMD边权重标签错误率约14.7%，导致奖励信号与实际需求不匹配，策略无法完成指定交互模式。
2. **部件分解失败**：对于语义常见但形态新颖的物体，自动部件分解约7%的不合理情况，导致RMD图结构本身存在缺陷。
3. **阈值敏感导致的提前/延迟切换**：阶段转换阈值设置不当会引发子步骤截断（过早切换）或长时间停滞（无法满足阈值），在长视距序列中错误累积效应明显。
4. **恢复动作的物理不稳定**：虽然本方法在坐/躺恢复任务上优于基线，但在极端姿态下仍偶发摔倒或穿模，说明AMP风格先验对非常规姿态的覆盖有限。

### 关键图表结论

- **Table 1**：本方法是唯一同时支持铰接对象、自动奖励设计、动态对象、细粒度长视距转换、HOI引导、多任务、高层规划和统一策略的全覆盖框架。
- **Figure 3**：定性对比可视化直观展示了InterPhys的非自然运动（手臂扭曲）、UniHSI的不完整交互（无法从坐姿恢复）与本方法类人运动质量的差异。
- **Table 4**：完整超参数配置可供复现参考，关键设置包括4096并行环境、PPO clip ε=0.2、AMP序列长度10、RMD奖励权重 $\lambda_{\text{RMD}}=0.5$。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_LfkPlFTfe0/figures/015_Table_4.jpg]]
*Table 4: Hyperparameters for RMD*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

#### 1.1 物理仿真驱动的HOI方法

本文工作建立在物理仿真驱动的人-物交互（HOI）运动合成这一研究脉络之上，该脉络的核心目标是在物理引擎中生成自然、物理上合理且任务一致的交互运动。早期代表性工作如 **AMP**（Peng et al., 2021）通过对抗运动先验（adversarial motion prior）实现了通用的人类运动合成，但主要关注运动风格模仿而非任务导向的交互。

在任务导向的物理HOI领域，**InterPhys**（Hassan et al., 2023）引入了对抗运动先验来处理静态和动态物体的交互，但其奖励函数依赖手动设计，且缺乏对长视距多步骤交互的自动规划能力。**TokenHSI**（Pan et al., 2025）通过任务分词器（task tokenizer）实现了多技能物理HOI，支持静态和动态物体，但其任务调度仍依赖基于规则的状态机，缺乏高层语义规划。**UniHSI**（Xiao et al., 2024）首次提出统一的接触链（Chain-of-Contacts, CoC）抽象，利用LLM自动生成目标和奖励函数，但该方法仅适用于静态物体交互，且离散的接触事件表示难以编码连续的运动动态。

本文提出的VLM引导的相对运动动力学（RMD）框架在以下关键维度上推进了现有工作：

- **交互表示粒度**：从UniHSI的离散接触事件链升级为细粒度时空二分图RMD，编码人体部件与物体部件之间的连续相对运动模式（静止接触、接近、远离、无一致趋势），使表示既能推理离散接触，也能捕捉运动动态。
- **自动化程度**：从InterPhys的手动奖励工程和TokenHSI的基于规则调度，升级为VLM自动生成的多步交互计划（RMD序列）及对应的目标状态与奖励函数，消除了人工设计瓶颈。
- **对象覆盖范围**：从UniHSI仅支持静态物体，扩展至同时支持静态、动态和铰接物体的统一框架。

#### 1.2 VLM/LLM在具身智能中的应用

本文位于VLM/LLM赋能具身智能这一新兴交叉领域。与Eureka等利用LLM迭代搜索生成奖励代码的方法不同，本文的VLM规划器直接输出结构化的RMD二分图，避免了迭代搜索的计算开销和不确定性。与SayCan等将LLM用于高层任务规划的工作相比，本文的VLM输出直接转化为物理仿真中的状态表示和奖励信号，实现了语义规划到物理执行的端到端桥接。

### 2. 适用边界

#### 2.1 适用场景

本方法适用于以下场景：
- **单人单物交互**：当前框架仅支持单个物理角色与单个物体的交互，未涉及多智能体协调或多物体操作。
- **已知物体部件分解**：RMD表示依赖物体部件（parts）的预定义分解。对于结构已知的物体（如家具、门、抽屉），该方法可直接适用。
- **VLM可感知的环境**：VLM规划器需要顶视图环境图像作为输入，因此适用于室内家居等结构化场景。

#### 2.2 不适用或需谨慎使用的场景

- **新颖但语义常见的物体**：论文报告对新颖物体的部件分解存在约7%的不合理情况，表明方法在未见物体类别上的泛化性尚需提升。
- **极高精度要求**：阶段转换阈值对性能敏感（最优阈值为0.90），过高阈值（如0.95）会导致完成率大幅下降，说明方法在需要极高精度的场景下鲁棒性有限。
- **VLM规划器与物理策略分离训练**：当前VLM规划器与强化学习策略分开训练，可能存在愿景-执行差距（goal misalignment），在需要实时动态调整的复杂场景中可能表现不佳。

### 3. 局限性与已知失效模式

1. **VLM规划器的标签错误**：在混合任务（hybrid tasks）上，VLM规划器的RMD标签错误率约14.7%，这直接限制了复杂长视距任务的成功率。错误主要源于VLM对空间关系和运动动态的推理能力有限。

2. **阶段转换的脆弱性**：策略的阶段切换依赖任务奖励是否超过固定阈值（0.9）。消融实验（Table 6）表明，阈值从0.90降至0.85或升至0.95均导致性能下降，说明该方法对阈值选择敏感，缺乏自适应切换机制。

3. **单人单物的限制**：当前框架未建模多智能体交互或同时操作多个物体的场景，限制了其在更复杂社会交互场景中的应用。

4. **物理保真度与运动多样性的权衡**：方法依赖AMP风格判别器保证运动自然性，但判别器基于参考运动数据集训练，可能限制生成运动的多样性，尤其在训练数据中未覆盖的交互模式上。

5. **VLM推理的计算开销**：虽然VLM规划器避免了在线迭代搜索，但GPT-4V等大型VLM的推理延迟和成本仍是实际部署的瓶颈。

### 4. 待解决的开放问题

1. **多智能体与社会交互扩展**：如何将RMD表示从单人单物扩展至多人多物的社会动态场景，编码智能体间的相对运动关系？

2. **生成先验的融合**：能否结合扩散模型等生成式先验，在保持物理合理性的同时丰富交互运动的多样性和表现力？

3. **VLM规划器的层次化推理**：如何增强VLM在长视距任务上的时间推理与分层规划能力，减少标签错误率（当前14.7%）？

4. **端到端联合优化**：是否可以通过端到端训练联合优化VLM规划器和物理控制器，减少愿景与执行间的差距？这涉及离散符号规划与连续控制的联合学习这一开放挑战。

5. **跨领域迁移**：RMD表示是否可应用于移动机器人领域的物理仿真任务，如机器人操作或人-机器人协作？这需要验证RMD在非人形运动学结构上的泛化能力。

## 原文 PDF

![[paperPDFs/ICLR_2026/Human_Object_Interaction_via_Automatically_Designed_VLM_Guided_Motion_Policy.pdf]]
