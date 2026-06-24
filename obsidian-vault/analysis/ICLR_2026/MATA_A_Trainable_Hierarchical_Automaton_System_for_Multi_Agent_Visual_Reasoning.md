---
title: "MATA: A Trainable Hierarchical Automaton System for Multi-Agent Visual Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MATA_A_Trainable_Hierarchical_Automaton_System_for_Multi_Agent_Visual_Reasoning.pdf
openreview_forum_id: fC27SxF4ba
aliases:
- MMAHTA
- MATA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "将高层智能体调度建模为有限状态自动机的可训练转移函数（基于SFT微调的LLM超智能体），使其能够依据共享记忆上下文动态选择下一状态，从而在不需要手工规则的情况下自主决定协作与竞争策略。"
primary_logic: "将多智能体视觉推理组织为分层确定性有限状态自动机：顶层状态是语义不同的特殊化智能体，底层智能体内部运行基于规则的可解释子自动机；通过展开转移轨迹树，用下游任务指标自底向上评分，将每个决策点转化为（当前记忆→最佳下一状态）的监督样本，并以此对大语言模型进行监督微调，使其学会全局最优的跨智能体状态转移策略。"
claims:
- "MATA将推理组织为由可训练超智能体控制的高层自动机，每个智能体内部使用基于规则的子自动机。"
- "超智能体通过LLM实现转移函数δ_θ，并基于轨迹数据集进行监督微调。"
- "通过展开转移轨迹树并自底向上评分，生成MATA-SFT-90K数据集，用于训练超智能体选择最优下一状态。"
- "MATA在GQA（64.9%）、OK-VQA（76.5%）和RefCOCO/RefCOCO+上取得最优结果，优于组合式和单片式基线。"
---

# MATA: A Trainable Hierarchical Automaton System for Multi-Agent Visual Reasoning

> [!tip] 核心洞察
> 将多智能体视觉推理组织为分层确定性有限状态自动机：顶层状态是语义不同的特殊化智能体，底层智能体内部运行基于规则的可解释子自动机；通过展开转移轨迹树，用下游任务指标自底向上评分，将每个决策点转化为（当前记忆→最佳下一状态）的监督样本，并以此对大语言模型进行监督微调，使其学会全局最优的跨智能体状态转移策略。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MATA：一种可训练的分层自动机系统用于多智能体视觉推理 |
| 英文题名 | MATA: A Trainable Hierarchical Automaton System for Multi-Agent Visual Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=fC27SxF4ba); [GitHub](https://github.com/ControlNet/MATA) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | MATA (Multi-Agent hierarchical Trainable Automaton) |
| Dataset | GQA, OK-VQA, RefCOCO, RefCOCO+ |

> [!tip] 效果简介
> - GQA 上，准确率 (%) 为 64.9 (MATA-General)，对比 63.8 (InternVL3.5-8B, 最高纯VLM基线)，变化 +1.1。
> - OK-VQA 上，准确率 (%) 为 76.5 (MATA-Domain-Specific)，对比 75.7 (InternVL3.5-8B, 最高纯VLM基线)，变化 +0.8。
> - RefCOCO 上，准确率 (%) 为 96.3 (MATA-Domain-Specific)，对比 96.2 (NAVER, 最强组合基线)，变化 +0.1。

## 概述

视觉推理任务要求模型整合感知、组合推理与知识检索，现有方法在此面临两难：端到端多模态大模型虽灵活但缺乏可解释性与纠错能力，而组合式系统虽可审计却依赖固定手工流水线或单一智能体，无法在互补（协作）与重叠（竞争）的异质智能体之间动态切换，导致复杂查询下性能受限且难以处理上游误差传播。

MATA（Multi-Agent hierarchical Trainable Automaton）将多智能体视觉推理建模为**分层确定性有限状态自动机**。其顶层是一个可训练的超自动机，状态对应语义不同的特殊化智能体；底层每个智能体内部运行基于规则的子自动机，确保微观执行的可靠性。核心创新在于：将高层智能体调度——即“下一步该由哪个智能体处理”——形式化为自动机的转移函数 $\delta_{\theta}$，并由一个基于大语言模型（LLM）的超智能体实现，通过监督微调（SFT）学会在共享记忆上下文中自主决策协作与竞争策略（Figure 1）。

为训练这一转移策略，MATA对每条图像-查询展开转移轨迹树，用下游任务指标自底向上评分，将每个决策点转化为“当前记忆 → 最佳下一状态”的监督样本，构建了 **MATA-SFT-90K** 数据集。超智能体在此数据集上进行SFT，学习全局最优的跨智能体状态转移（Equation 2–4）。

在GQA、OK-VQA、RefCOCO/RefCOCO+/RefCOCOg及Ref-Adv六个基准上，MATA取得最优或最具竞争力的结果：GQA准确率64.9%（优于最强纯VLM基线InternVL3.5-8B的63.8%），OK-VQA达76.5%，RefCOCO达96.3%，RefCOCO+达93.9%，域迁移设置Ref-Adv达77.3%（Table 2–4）。消融实验证实，可训练的超自动机结构相比穷举搜索提速4倍以上，且LLM转移策略与SFT各自带来显著增益（Table 5）；逐步增加子智能体持续提升准确率，验证了多智能体协作的有效性（Figure 4）。

**方法定位**：MATA属于组合式神经符号推理，与固定流水线方法（如ViperGPT）、单智能体RL控制方法（HYDRA，Ke et al., ECCV 2024）及手工规则多智能体系统（NAVER，Cai et al., 2025）形成对比。其独特之处在于将多智能体调度从手工设计提升为**可学习的自动机转移策略**，同时保留了基于规则的微观可解释性。当前局限包括轨迹树展开的计算开销随智能体数量增长而急剧增加，以及竞争性转移并非在所有子任务上均优于手工规则（如RefCOCOg上90.8 vs NAVER的91.6）。

## 背景与动机

视觉推理要求模型在理解图像内容的基础上进行复杂的逻辑推断、知识检索或空间定位。近年来，多模态大语言模型（MLLM）在视觉问答和指代表达理解等任务上取得了显著进展，但其推理过程本质上仍是端到端的黑箱映射——模型直接输出答案，缺乏可审计的中间步骤与纠错机制。当模型产生幻觉或推理错误时，几乎无法定位故障来源或进行针对性的修正。

另一类方法采用组合式（compositional）范式，将推理分解为感知、程序生成、验证等模块化步骤，通过显式的符号化中间表示提升可解释性。然而，现有组合式方法普遍依赖固定手工编排的线性流水线或单一智能体循环，存在两个关键瓶颈：

**瓶颈一：静态调度无法适应查询复杂度差异。** 传统线性流水线（如**ViperGPT**）对所有查询执行相同的模块序列，简单问题被过度处理，复杂问题则可能因缺乏多角度验证而失败。单智能体方法（如**HYDRA**（Ke et al., ECCV 2024）使用RL控制器、**DWIM**（Ke et al., ICCV 2025）使用工具感知推理）虽引入了一定灵活性，但本质上仍是单一角色在循环中自我修正，缺乏不同推理范式之间的动态切换能力。

**瓶颈二：多智能体协作缺乏可学习的竞争机制。** 多智能体系统（如**NAVER**（Cai et al., 2025））虽将推理组织为自动机，但其状态转移依赖手工编写的固定规则，无法根据任务上下文自主决定何时让智能体协作互补、何时让智能体竞争重新介入。当上游智能体的感知或推理结果存在误差时，下游模块缺乏有效的容错与纠正路径，导致误差传播累积。

上述瓶颈的根本原因在于：现有方法缺少一种能够在异质智能体之间进行**可训练的动态调度**的机制。具体而言，需要解决的核心问题是——如何让系统自主学会“在什么情况下调用哪个智能体，以及何时切换或回退”，而非依赖人工预设的静态规则。

MATA正是针对这一缺口提出的。其核心动机是将多智能体视觉推理重新建模为**分层有限状态自动机**：顶层状态是语义不同的特殊化智能体，底层每个智能体内部运行基于规则的确定性子自动机以保证微观可靠性，而连接这些状态的转移函数则由一个可训练的超智能体（基于LLM）通过学习获得。这种设计使得系统能够在协作（互补智能体接力）与竞争（失败后切换智能体重新介入）之间自主决策，同时通过共享记忆提供透明的执行审计轨迹。

## 核心创新

MATA 的核心创新在于将多智能体视觉推理重新建模为一类**可训练的分层有限状态自动机**，使系统能自主学会“何时协作、何时竞争”，而非依赖手工设计的固定流水线或单一智能体的循环调用。

### 瓶颈与因果调节变量

现有视觉推理方法在架构上分化为两个极端：端到端黑箱模型缺乏可解释性与纠错能力；组合式方法虽具备可审计的执行轨迹，但其顶层调度要么是**固定手工规则**（如 **NAVER** 的硬编码转移），要么是**单智能体循环**（如 **HYDRA** 的 RL 控制器）。这导致系统无法在互补（协作）与重叠（竞争）的异质智能体之间动态切换——当上游感知出错时，下游推理器被动接受错误输入，误差沿固定路径传播。

MATA 识别的**因果调节变量**是：将高层智能体调度建模为有限状态自动机的**可训练转移函数**。通过让一个基于 LLM 的超智能体依据共享记忆上下文自主决定下一状态，系统不再需要手工规则来编排智能体间的协作与竞争策略。

### 关键 changed slots

相较于组合式与单片式基线，MATA 在四个关键维度上实现了结构性改变：

**1. 高层转移策略：从手工规则到可学习转移函数**

基线方法（如 NAVER）的高层智能体调度依赖固定手工打造的转移规则；HYDRA 虽引入 RL 控制器，但本质上仍是单智能体在不同工具间的循环调用。MATA 将转移函数 $\delta_{\theta}$ 实现为一个基于 LLM 的可训练超智能体 $\mathcal{F}_{\theta}$，使用监督微调从转移轨迹中学习全局最优的跨智能体状态转移策略：

$$s_{t+1} = \delta_{\theta}(s_t, m_t), \quad s_{t+1} \in S$$

超智能体读取共享内存的快照 $m_t$，预测下一状态 $s_{t+1}$，实现从“规则驱动”到“数据驱动”的范式转变。

**2. 多智能体协作与竞争机制：从单角色硬编码到分层自动机内的动态博弈**

传统多智能体系统（如 MetaGPT、IdealGPT）将各智能体角色硬编码为固定流水线，智能体间无竞争关系。MATA 在分层自动机内设置三个语义不同的特殊化智能体——Oneshot Reasoner（快思考）、Stepwise Reasoner（慢思考）、Specialized Agent（快速感知）——它们共享内存协作，并在失败时竞争重新介入。超智能体通过状态转移决策，自主选择“先感知后推理”或“直接慢思考”等策略，实现协作与竞争的统一。

**3. 转移策略的监督信号：从无明确监督到轨迹树展开评分**

基线方法的顶层调度缺乏明确的转移监督信号——规则驱动方法依赖人工经验，提示驱动方法仅靠 LLM 的零样本能力。MATA 提出**转移轨迹树展开 + 自底向上评分**的监督范式：对每个图像-查询对，系统穷举遍历所有可能的下一状态分支，构建轨迹树 $\mathcal{T}$，然后从叶节点向上传播任务指标：

$$V(s) \triangleq \begin{cases} \mathrm{metric}(\hat{y}_s, y), & s \in \mathrm{Leaves}(\mathcal{T}), \\ \max_{s' \in \mathrm{Child}(s)} V(s'), & \text{otherwise}. \end{cases}$$

每个决策点被转化为监督对（当前记忆 → 最优下一状态），构成 **MATA-SFT-90K** 数据集，使超智能体通过 SFT 学习全局最优转移策略。

**4. 共享记忆：从隔离上下文到全局可审计的追加式记忆**

基线方法中，各智能体或模块的上下文相互隔离，仅记录局部程序历史。MATA 引入所有智能体和超智能体均可读写的**追加式共享内存**，存储感知结果、程序历史、验证反馈及任务元数据。这不仅为超智能体提供了透明的全局上下文用于转移决策，也使得整个推理过程具备完整的可审计性——任何决策点的依据均可追溯到共享记忆中的具体条目。

### 创新证据强度

上述 changed slots 均有高置信度证据支撑：可训练转移函数在消融实验中表现出决定性作用（Table 5：LLM Transition + SFT 相比 Random Transition 在 GQA 上提升 7.8 个百分点）；多智能体贡献通过逐步添加子智能体的实验得到验证（Figure 4：准确率从 61.5% 单调提升至 64.9%）；MATA-SFT-90K 数据集的生成流程在方法论中有完整的形式化定义（Equation 3-4）。跨域泛化实验（Table 6）进一步表明，学习到的转移策略在未见过的数据集上仍保持有效，非对角线性能接近对角线性能，验证了可训练转移策略的泛化性。

## 整体框架

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_fC27SxF4ba/figures/001_Figure_1.jpg]]
*Figure 1: Overview of MATA. (a) Linear pipelines (previous methods) execute modules in a fixed, manually designed order. (b) MATA organizes agents as states in a hyper automaton. A trainable hyper agent learns high-level transitions between agents (blue arrows), enabling collaboration and competition, while each agent runs a small rule-based sub-automaton for reliable micro-control (black arrows). (c) To train the hyper agent, we expand a transition-trajectory tree per image-query, score the leaves using task metrics, and convert each node’s snapshot into a supervised pair current memory → best next state for supervised finetuning (SFT), forming MATA-SFT-90K*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_fC27SxF4ba/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of MATA. A trainable hyper agent reads a snapshot of the shared memory, predicts the next state with an LLM State Controller. Its decision (blue arrows) routes control among agent states in the hyper automaton: Oneshot Reasoner, Stepwise Reasoner, and Specialized Agent. Each agent runs a rule-based sub-automaton that iterates until return to the hyper automaton. All agents read/write an append-only Shared Memory, enabling the hyper agent to access the current context for choosing the optimal next state. Lifecycle states INITIAL and FAILURE are shown outside the agents (see subsection 3.2 for details)*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_fC27SxF4ba/figures/003_Table_1.jpg]]
*Table 1: States of the hyper automaton. The table specifies the description and the triggering condition for each state. $\delta _ { \theta } \colon$ transition function of hyper automaton

MATA 将多智能体视觉推理组织为一个**分层确定性有限状态自动机**，其核心设计理念是用可训练的高层调度替代手工规则，同时保留底层模块的可靠微控制。系统由三个关键层次构成：顶层超自动机、中层特殊化智能体、底层基于规则的子自动机，所有组件通过追加式共享内存进行通信。

### 架构总览

MATA 的形式化基础是一个 **Mealy 机**：

$$M_{\theta} = (S, S_0, \Sigma, \Lambda, \delta_{\theta}, \Gamma)$$

其中有限状态集 $S = S_{\mathrm{agent}} \cup S_{\mathrm{life}}$ 包含三类语义不同的推理智能体状态——**Oneshot Reasoner**（单次程序生成与验证）、**Stepwise Reasoner**（逐步 Python 推理与沙盒执行）、**Specialized Agent**（基于 VFM 的快速感知专家）——以及三个生命周期状态：**INITIAL**（推理起点）、**FINAL**（终止输出）和 **FAILURE**（容错上限触发）。输入字母表 $\Sigma$ 对应图像-查询对，输出字母表 $\Lambda$ 对应最终答案，转移函数 $\delta_{\theta}$ 由可训练的 LLM 超智能体实现，输出函数 $\Gamma$ 在 FINAL 状态下生成最终响应。

### 超自动机与状态转移

高层调度遵循以下转移规则：

$$s_{t+1} = \delta_{\theta}(s_t, m_t), \quad s_{t+1} \in S$$

超智能体 $\mathcal{F}_{\theta}$ 在每一步读取共享内存快照 $m_t$ 和当前状态 $s_t$，预测下一状态 $s_{t+1}$。这一设计使得系统能够在**协作**（不同智能体互补解决子问题）与**竞争**（一个智能体失败后另一个重新介入）之间动态切换，无需手工编写转移规则。例如，对于简单查询，超智能体优先调用 Specialized Agent 进行快速感知，仅在失败或低置信度时才升级到 Stepwise 或 Oneshot Reasoner；对于复杂多步推理，则直接路由到慢思维智能体。

### 共享内存机制

所有智能体和超智能体均可读写一个**追加式共享内存**，其结构化记录包括：
- 感知结果（目标检测、深度估计等 VFM 输出）
- 程序历史（生成代码、执行输出、沙盒反馈）
- 验证反馈（各子自动机的校验结果）
- 任务元数据（原始查询、图像标识）

这一设计产生透明可审计的执行历史，使超智能体能够在任意决策点获取完整上下文，同时也为后续的转移轨迹数据生成提供了结构化快照。

### 子自动机的微控制

每个智能体内部运行一个**基于规则的确定性子自动机**，形成微观循环：代码生成 → 验证 → 解释/迭代。例如，Stepwise Reasoner 的子自动机逐步生成 Python 代码并在沙盒中执行，若验证失败则自动修正；Specialized Agent 内置验证器可自动调整感知参数。这种设计保证了微观层面的可靠性，将高层可训练策略的探索风险限制在状态转移层面。

### 训练与推理流程

超智能体的训练采用**离线监督微调**范式：

$$\theta \gets \arg \min_{\theta} \mathcal{L}_{\mathrm{SFT}}(\theta; \mathcal{D})$$

训练数据 $\mathcal{D}$ 来自 **MATA-SFT-90K** 数据集，其构建过程为：对每个图像-查询对，展开转移轨迹树（系统性地遍历每个决策点的所有可能下一状态），用下游任务指标自底向上评分：

$$V(s) \triangleq \begin{cases} \mathrm{metric}(\hat{y}_s, y), & s \in \mathrm{Leaves}(\mathcal{T}), \\ \max_{s' \in \mathrm{Child}(s)} V(s'), & \text{otherwise}. \end{cases}$$

然后从每个节点的子状态中选择最优下一状态作为 SFT 标签：

$$s_t^\star \in \arg \max_{s \in \mathrm{Child}(s_t)} V(s)$$

最终将每个决策点转化为监督对（当前记忆 → 最佳下一状态），使超智能体学会全局最优的跨智能体转移策略。推理时，超智能体基于微调后的 LLM（如 Qwen3-4B）实时预测转移，最大步数限制为 $T=15$ 以防止无限循环。

## 核心模块与公式推导

### 分层自动机架构

MATA将多智能体视觉推理形式化为一个分层确定性有限状态自动机，其核心包含两个控制层级：

1. **超自动机（Hyper Automaton）**：顶层由可训练的超智能体控制，负责在语义不同的特殊化智能体之间进行高层状态转移。超自动机被建模为Mealy机：
   $$\mathcal{M}_\theta = (S, S_0, \Sigma, \Lambda, \delta_\theta, \Gamma)$$
   其中 $S$ 为有限状态集，$S_0$ 为初始状态，$\Sigma$ 为输入字母表，$\Lambda$ 为输出字母表，$\delta_\theta$ 为可学习的转移函数，$\Gamma$ 为输出函数。

2. **子自动机（Sub-Automaton）**：每个智能体内部运行基于规则的确定性微循环，执行代码生成→验证→解释/迭代的可靠流程，确保微观操作的可解释性与稳定性。

### 状态空间定义

超自动机的状态集 $S = S_{\text{agent}} \cup S_{\text{life}}$ 由两类状态组成：

- **智能体状态** $S_{\text{agent}} = \{\text{ONESHOT}, \text{STEPWISE}, \text{SPECIALIZED}\}$：
  - **ONESHOT Reasoner**：单次程序生成与验证的快速思考智能体，适用于中等复杂度的可解查询。
  - **STEPWISE Reasoner**：逐步生成并执行Python程序的慢思考智能体，用于多步组合推理，含沙盒验证。
  - **Specialized Agent**：利用视觉基础模型进行快速感知（目标检测、深度估计等）的系统1智能体，内建验证器自动调整参数。

- **生命周期状态** $S_{\text{life}} = \{\text{INITIAL}, \text{FINAL}, \text{FAILURE}\}$：管理推理开始、终止输出、容错和重试上限。

### 核心转移机制

#### 状态转移函数

超自动机的转移由可训练的LLM超智能体 $\mathcal{F}_\theta$ 实现：
$$s_{t+1} = \delta_\theta(s_t, m_t), \quad s_{t+1} \in S$$

其中 $s_t$ 为当前状态，$m_t$ 为共享记忆在时刻 $t$ 的快照。超智能体读取当前记忆上下文，预测下一状态，实现在协作（互补）与竞争（重叠）智能体之间的动态切换。

#### 共享记忆

所有智能体和超智能体共享一个追加式结构的内存，记录感知结果、程序历史、验证反馈及任务元数据。该设计使得超智能体能够基于完整的可审计上下文做出转移决策，同时保证执行历史的透明性。

### 超智能体训练

#### 监督微调目标

超智能体参数 $\theta$ 通过在转移轨迹数据集 $\mathcal{D}$ 上进行监督微调来学习：
$$\theta \gets \arg \min_\theta \mathcal{L}_{\mathrm{SFT}}(\theta; \mathcal{D})$$

训练样本为（当前记忆 → 最佳下一状态）对，使超智能体学会全局最优的跨智能体转移策略。

#### 轨迹树构建与自底向上评分

为生成监督信号，MATA对每个图像-查询对展开转移轨迹树 $\mathcal{T}$，系统性地遍历每个可能的下一状态选项。对树中每个节点 $s$ 进行自底向上评分：
$$V(s) \triangleq \begin{cases} \mathrm{metric}(\hat{y}_s, y), & s \in \mathrm{Leaves}(\mathcal{T}), \\ \max_{s' \in \mathrm{Child}(s)} V(s'), & \text{otherwise}. \end{cases}$$

叶节点使用下游任务指标（如准确率）评分，内部节点取其所有子节点中的最大值向上传播。

#### 最优状态选择

从当前状态 $s_t$ 的子状态中，选择具有最大传播评分的状态作为SFT标签：
$$s_t^\star \in \arg \max_{s \in \mathrm{Child}(s_t)} V(s)$$

通过该机制构建的MATA-SFT-90K数据集，使超智能体能够从轨迹树的成功分支中学习最优转移策略，而非依赖手工规则。

## 实验与分析

### 主实验结果

MATA 在视觉问答与指代表达理解两类任务上均取得最优或竞争性结果，验证了可训练多智能体自动机在复杂视觉推理中的有效性。

在 **GQA** 数据集上，MATA-General 达到 64.9% 准确率，MATA-Domain-Specific 达到 64.7%，分别超出最强纯视觉语言模型基线 InternVL3.5-8B（63.8%）1.1 和 0.9 个百分点（Table 2）。在 **OK-VQA** 上，MATA-Domain-Specific 以 76.5% 领先 InternVL3.5-8B（75.7%）0.8 个百分点，MATA-General 为 76.0%（Table 3）。值得关注的是，MATA 在所有组合式基线中均表现最优，显著超越单智能体组合推理方法 **HYDRA**（Ke et al., ECCV 2024）和手工转移规则的多智能体自动机 **NAVER**（Cai et al., 2025）。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_fC27SxF4ba/figures/004_Table_2.jpg]]
*Table 2: Performance on GQA dataset. Table 3: Performance on OK-VQA dataset*

在指代表达理解任务上，MATA 的优势更为突出（Table 4）。在 RefCOCO 上，MATA-General 达到 96.3%，MATA-Domain-Specific 为 96.2%，与最强组合基线 NAVER（96.2%）持平或略优；在 RefCOCO+ 上，MATA-General 以 93.9% 显著领先 NAVER（92.8%）1.1 个百分点。更具说服力的是域迁移场景：在无训练集的 Ref-Adv 上，MATA-General 达到 77.3%，超出 NAVER（75.4%）1.9 个百分点，表明学习到的转移策略具有良好的跨域泛化能力。仅在 RefCOCOg 上 MATA（90.8%）略低于 NAVER（91.6%），说明竞争性多智能体转移并非在所有子数据集上均一致优于手工规则。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_fC27SxF4ba/figures/005_Table_4.jpg]]
*Table 4: Quantitative comparison (accuracy) on referring expression comprehension task on RefCOCO, RefCOCO+, RefCOCOg (Kazemzadeh et al., 2014) and Ref-Adv (Akula et al., 2020) set. Note there is no training set in Ref-Adv, so all scores are domain-transfer. Agentic types: non-agentic/non-specified; single-agent; multi-agent*

### 消融实验

消融实验围绕超自动机结构、转移策略和子智能体配置三个维度展开，系统揭示了各组件的贡献。

**超自动机与转移策略**（Table 5）：移除超自动机结构（Exhaustive Ensemble，即穷举运行所有智能体并投票）在 GQA 上仅得 58.5%，推理时间高达 34.58 秒；引入超自动机但使用随机转移策略（Random Transition）性能进一步降至 57.1%，表明无序切换反而引入噪声。使用 LLM 作为转移控制器但未经 SFT 微调（LLM Transition w/o SFT）提升至 58.5%，仍远低于完整模型。完整的 MATA（HA + LLM Transition + SFT）在 GQA 上达到 64.9%，推理时间压缩至 8.01 秒——相比穷举搜索提速 4.3 倍，同时准确率提升 6.4 个百分点。这一对比直接证明了**可训练转移策略是性能与效率双重提升的核心控制变量**。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_fC27SxF4ba/figures/006_Table_5.jpg]]
*Table 5: Ablation of hyper agent. In this table, we report the accuracy for all VQA and referring expression comprehension benchmarks, and the inference time per query (tested on GQA). HA: Hyper Automaton. Transition: Transition policy (δθ). SFT: Supervised finetuning. Refer to subsection 4.2 for details*

**超智能体 LLM 规模**（Figure 3）：将超智能体的 LLM 状态控制器从 0.5B 逐步增加到 4B，在 GQA 和 OK-VQA 上均呈现单调的性能提升趋势，表明更强的语言模型能更准确地从共享记忆中捕捉上下文线索，做出更优的转移决策。

**子智能体数量**（Figure 4）：在 GQA 上，从仅使用 Specialized Agent（61.5%）逐步引入 Oneshot Reasoner（64.5%）和 Stepwise Reasoner（64.9%），准确率持续提升，验证了三种异质智能体在感知、快思考和慢思考维度的互补性。

### 跨域泛化分析

Table 6 展示了转移策略在不同训练-测试域组合下的泛化能力。对角线上的域内训练结果与跨域迁移（非对角线）结果接近，例如在 GQA 上训练而在 OK-VQA 上测试，或在 RefCOCO 上训练而在 RefCOCO+ 上测试，性能下降有限。最后一行报告了在完整 MATA-SFT-90K 数据集上联合训练（General）的结果，在所有测试域上均达到或接近最优。这表明通过轨迹树展开与自底向上评分生成的监督信号，超智能体学到的是**任务无关的状态转移逻辑**，而非对特定数据集的过拟合。

### 失败模式与局限性

尽管 MATA 在多数基准上表现优异，但仍存在以下可识别的失败模式：

1. **RefCOCOg 上的性能回退**：MATA（90.8%）略低于 NAVER（91.6%），说明当查询本身更适合固定流水线时，竞争性多智能体转移可能引入不必要的调度开销或错误的路由决策。
2. **状态空间扩展的计算瓶颈**：当前数据生成流水线依赖对三个智能体状态空间的近穷举搜索来构建转移轨迹树，这在三智能体规模下可处理，但当引入更多特化智能体（如不同感知模态）时，轨迹树将呈指数增长，数据收集成本急剧上升。
3. **离线训练的静态局限**：超智能体的 SFT 训练完全离线完成，无法利用推理过程中的实时反馈进行纠错。当遇到训练分布外的查询模式时，转移策略可能做出次优决策且缺乏在线自适应机制。

## 方法谱系与知识库定位

### 1. 与现有工作的关系

MATA 位于**组合式神经符号推理**与**多智能体协作**的交汇点，其核心贡献在于将原本由手工规则或单一控制器驱动的多智能体调度，升级为**可训练的分层有限状态自动机**。

**相对于单智能体组合推理：** 现有方法如 **HYDRA**（Ke et al., ECCV 2024）使用强化学习控制器在固定模块序列中做选择，**DWIM**（Ke et al., ICCV 2025）则赋予单智能体工具感知能力。这些方法本质上仍是单一角色在循环中自我修正，缺乏不同认知特质的智能体之间的**分工与竞争**。MATA 引入三个语义不同的特殊化智能体（Oneshot Reasoner、Stepwise Reasoner、Specialized Agent），分别对应快思考、慢思考和快速感知，使系统能够在不同难度的查询上动态分配最合适的认知资源。

**相对于多智能体自动机：** **NAVER**（Cai et al., 2025）同样将多智能体组织为自动机，但其状态转移规则是**手工打造的固定策略**，无法根据查询复杂度或上游失败动态调整。MATA 的关键突破在于将转移函数 $\delta_\theta$ 实现为基于 LLM 的可训练超智能体（Qwen3-4B），使其能够从转移轨迹数据中**学习全局最优的跨智能体调度策略**，而非依赖人工预设的启发式规则。

**相对于纯端到端模型：** 与 **InternVL3.5-8B**、**Qwen2.5-VL-7B**、**GPT-4o** 等单片多模态大模型相比，MATA 不追求在单一黑箱中隐式完成所有推理，而是通过显式的状态转移轨迹和共享记忆保留了完整的**可审计性与可解释性**。每个智能体内部运行基于规则的子自动机（代码生成→验证→迭代），确保微观层面的可靠性，而高层调度则由可训练的 LLM 完成。

**相对于模块化编程方法：** **ViperGPT** 等训练自由组合推理方法虽具备模块化优势，但缺乏对模块间转移策略的优化学习。MATA 通过 MATA-SFT-90K 数据集将转移策略的训练形式化为标准的监督微调问题，使得调度策略可以随数据和智能体的增加而持续改进。

### 2. 适用边界与能力范围

**任务域适配：** MATA 当前在三个任务族上验证了有效性——开放知识视觉问答（GQA、OK-VQA）、指代表达理解（RefCOCO/+/g）以及对抗性指代（Ref-Adv）。跨域泛化实验（Table 6）表明，在 VQA 数据上训练的转移策略可以直接迁移到指代任务上，且性能损失有限（域迁移精度接近域内训练），说明学到的调度策略具有一定的**任务无关性**。

**智能体规模约束：** 当前系统仅包含三个功能智能体，覆盖了感知、快思考和慢思考的谱系。对于更细粒度的特化（如不同感知模态的分离、多跳推理的进一步分解），框架在概念上可扩展，但轨迹树搜索的计算开销会随状态数指数增长——这是当前方法的一个硬性约束。

**基础模型依赖：** MATA 的性能上限受限于其底层工具模型（如 InternVL2.5-8B 用于 VQA、Florence2-L 用于感知）。超智能体的转移策略学习是在固定工具能力的前提下优化调度，而非提升单工具的上限。消融实验（Figure 3）表明，超智能体的 LLM 规模从 0.5B 提升到 4B 带来单调的精度增益，说明转移策略的质量本身也受模型容量影响。

### 3. 已知局限与失效模式

**数据生成的可扩展性瓶颈：** 转移轨迹数据集的构建依赖于对状态空间的**近穷举搜索**——在每个决策点展开所有可能的下一状态分支，运行完整推理管线到终止，再用下游指标自底向上评分。这在三个智能体规模下可行，但当状态数增长时，轨迹树将面临组合爆炸。论文明确指出这是当前方法的主要局限，并提出了蒙特卡洛采样或值函数近似作为潜在缓解方向，但尚未实现。

**训练成本：** 超智能体的 SFT 需要多次运行完整推理管线来记录轨迹，每次运行都涉及多个智能体的代码生成、执行和验证。这一数据收集过程的计算开销显著高于传统的单模型 SFT 数据生成。

**非一致优于手工规则：** 在 RefCOCOg 上，MATA 的精度（90.8）略低于 NAVER（91.6），说明竞争性多智能体转移并非在所有子数据集上都优于精心设计的手工规则。这可能是因为 RefCOCOg 的指代表达更长、更复杂，手工规则在某些情况下恰好命中了更优的调度路径，而学习到的策略在该分布上尚未充分泛化。

**竞争机制的计算冗余：** 当超智能体在失败后调度竞争性智能体重新介入时，会产生额外的推理开销。虽然消融实验（Table 5）表明超自动机结构将推理时间从穷举搜索的 34.58 秒降至约 8 秒，但相比单智能体方法仍有一定的时间代价。

### 4. 开放问题与未来方向

1. **轨迹树搜索的规模化：** 当智能体数量从 3 扩展到 N 时，穷举搜索不可行。是否可以用蒙特卡洛树搜索（MCTS）替代穷举展开，或训练一个值函数网络来近似 $V(s)$，从而将数据生成从指数复杂度降为多项式复杂度？

2. **在线学习与强化微调：** 当前转移策略的训练完全离线（SFT on MATA-SFT-90K）。能否将训练范式扩展到在线强化学习，使超智能体在部署过程中根据执行反馈实时调整转移策略？这将使系统具备从推理失败中持续自我改进的能力。

3. **更广泛的任务泛化：** MATA 的分层自动机框架是否适用于视频推理（需要时序感知智能体）、多模态文档理解（需要 OCR 与布局感知智能体）、或具身视觉推理（需要动作规划智能体）？这些场景下智能体类型的定义和转移策略的学习可能需要新的设计。

4. **竞争与协作的精细调度：** 当前竞争机制是失败驱动的重新介入。是否存在更精细的调度策略——例如基于置信度阈值的软切换、多智能体并行执行后投票融合——能在精度和效率之间取得更好的平衡？

5. **超智能体的可解释性：** 虽然 MATA 的共享记忆提供了可审计的执行历史，但超智能体自身的转移决策（LLM 生成的下一个状态）仍是一个黑箱。能否让超智能体输出其转移决策的自然语言理由，从而进一步增强系统的端到端可解释性？

## 原文 PDF

![[paperPDFs/ICLR_2026/MATA_A_Trainable_Hierarchical_Automaton_System_for_Multi_Agent_Visual_Reasoning.pdf]]
