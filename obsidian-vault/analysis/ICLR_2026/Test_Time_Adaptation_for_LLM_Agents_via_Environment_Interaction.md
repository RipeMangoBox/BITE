---
title: "Test-Time Adaptation for LLM Agents via Environment Interaction"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Test_Time_Adaptation_for_LLM_Agents_via_Environment_Interaction.pdf
project_link: null
code_link: https://github.com/r2llab/GTTA
openreview_forum_id: OH4PE0TDo0
aliases:
- SASDGD
- TTALAEI
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过测试时交互获取环境特定的句法与动态知识，并以轻量级适应向量（SA）或上下文世界模型（DG）的形式注入智能体决策过程。"
primary_logic: "仅利用无监督的测试时环境交互信号，即可通过参数化的在线句法适应和基于上下文的环境动态规则提取，在不依赖标注数据的情况下显著提升智能体在复杂未知环境中的泛化能力。"
claims:
- "动态基础（DG）在WebArena多站点任务上将GPT-4.1成功率从2%提升至23%。"
- "句法对齐（SA）和动态基础（DG）均能一致提升不同模型在多个基准上的性能。"
- "使用任务模型自身进行探索和动态提取可以达到与使用更强模型同等、甚至更好的效果。"
- "句法对齐的单步更新仅增加约3%的延迟开销，适合实时部署。"
---

# Test-Time Adaptation for LLM Agents via Environment Interaction

> [!tip] 核心洞察
> 仅利用无监督的测试时环境交互信号，即可通过参数化的在线句法适应和基于上下文的环境动态规则提取，在不依赖标注数据的情况下显著提升智能体在复杂未知环境中的泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于环境交互的LLM智能体测试时自适应 |
| 英文题名 | Test-Time Adaptation for LLM Agents via Environment Interaction |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=OH4PE0TDo0) · [GitHub](https://github.com/r2llab/GTTA) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Syntactic Alignment (SA) and Dynamics Grounding (DG) |
| Dataset | WebArena (overall), WebArena Multi-site, BFCLv3, WebArena (GPT-4o mini) |

> [!tip] 效果简介
> - WebArena (overall) 上，Success rate 为 35.0%，对比 30.0%，变化 +5.0%。
> - WebArena Multi-site 上，Success rate 为 23.0%，对比 2.0%，变化 +21.0%。
> - BFCLv3 上，Success rate 为 64.0%，对比 55.5%，变化 +8.5%。

## 概要

**核心问题**：LLM智能体在未见环境中面临双重不匹配——句法层面（UI元素标签、响应格式等）与语义层面（状态转移因果模型缺失），导致产生无效动作和规划失败。

**核心思路**：通过测试时环境交互获取特定句法与动态知识，以两种互补机制注入智能体决策——**句法对齐（SA）**以轻量适应向量在线偏置输出分布，**动态基础（DG）**以上下文世界模型提供环境转移规则。两者均无需标注数据，仅依赖无监督的交互信号。

**方法定位**：SA属于测试时参数适应范式，通过对隐层表示添加可学习的偏置向量，以当前上下文的交叉熵损失进行单步梯度更新；DG属于上下文世界模型构建范式，通过人格引导探索、动态提取与过滤，生成自然语言环境规则并拼接入输入序列。两方法可独立或组合使用，覆盖句法与语义两个适应维度。

**关键结果**：
- DG在WebArena多站点任务上将GPT-4.1成功率从**2%提升至23%**（Table 3），整体平均从30%提升至35%（Table 2）。
- SA和DG在GPT-4.1、GPT-4o mini、Qwen2.5-14B-Instruct三个模型上均一致提升性能，覆盖WebArena、BFCLv3、Tau-Bench多个基准（Table 2）。
- SA的单步更新仅增加约**3%的延迟开销**（Table 4），适合实时部署。
- 使用任务模型自身进行探索和动态提取，效果等同甚至优于使用更强模型（Table 5：GPT-4o mini self 19.0% vs GPT-4.1 extractor 18.0%）。

**局限与开放问题**：简单组合SA与DG在某些场景下反而不如单独使用DG；当环境动态符合常识时DG提升有限；目前仅在函数调用和网页导航任务上验证，对其他智能体环境的泛化性尚待探索。如何设计元控制器自动决定适应策略、如何更高效地结合两方法，是后续研究的关键方向。



大语言模型（LLM）驱动的智能体在开放环境中执行复杂任务时，面临一个根本性瓶颈：**句法不匹配**与**语义不匹配**的双重挑战。句法不匹配表现为环境特定的UI元素标签、API响应格式等与模型预训练分布不一致，导致智能体产生格式错误或无效动作；语义不匹配则源于智能体缺乏对环境中状态转移因果模型的认知——例如，点击某个按钮会触发日期弹窗，而非直接跳转页面——使得规划过程基于错误的因果假设，最终导致任务失败。

现有应对方案存在明显缺口。零样本LLM智能体（如GPT-4.1、GPT-4o mini、Qwen2.5-14B-Instruct）直接部署时，在WebArena等多网站复杂基准上的成功率极低，尤其在跨站点任务上仅约2%。基于世界模型增强的方法（如**WMA**，Chae et al., 2025）需要预先收集大量交互轨迹来训练独立的状态预测模型，不仅依赖标注数据，且无法泛化到纯对话式或非网页类环境。测试时自适应方法（如熵最小化或自监督微调）虽能缓解分布偏移，但通常仅针对单一模型输出分布调整，未触及环境动态知识的获取与利用。

本文的核心洞察在于：**仅利用无监督的测试时环境交互信号，即可通过参数化的在线句法适应和基于上下文的环境动态规则提取，在不依赖标注数据的情况下显著提升智能体在复杂未知环境中的泛化能力。** 具体而言，句法不匹配可通过轻量级适应向量在线微调模型输出分布来解决；语义不匹配则可通过一次性的、人格引导的探索阶段，以自然语言形式提取环境状态转移规则，并作为上下文世界模型注入决策过程。这一思路将测试时自适应的边界从句法层面拓展至动态建模层面，为LLM智能体在未见环境中的可靠部署提供了新的范式。

**决定性证据**：在WebArena多站点任务上，动态基础（DG）将GPT-4.1的成功率从2%提升至23%（Table 3）；句法对齐（SA）的单步更新仅增加约3%的延迟开销（Table 4），适合实时部署。



## 核心方法与创新机理

本文的核心贡献在于提出了两种互补的测试时自适应策略——**句法对齐（Syntactic Alignment, SA）**与**动态基础（Dynamics Grounding, DG）**——分别针对LLM智能体在未知环境中面临的两类根本性失配问题，且均不依赖任何标注数据或额外模型训练。

### 问题定位：句法失配与语义失配

LLM智能体在未见环境中失败的两个关键瓶颈是：
1. **句法不匹配**：环境特定的UI元素标签、响应格式和动作语法与模型预训练分布不一致，导致智能体产生无效动作（如错误的函数调用格式或不可执行的点击指令）。
2. **语义不匹配**：智能体缺乏对环境状态转移因果模型的认知（例如“点击‘Go’按钮会弹出日期选择器”），导致规划时忽略关键的前提动作或做出错误的转移假设。

SA和DG分别以参数化和上下文注入的方式解决上述两类失配，形成互补的测试时自适应框架。

### 创新一：句法对齐（SA）——参数化的在线输出分布校准

SA的核心创新在于引入一个**轻量级自适应向量 $\delta \in \mathbb{R}^d$**（$d$ 为模型隐层维度），以极低的计算开销实现每步在线适应。

**Changed Slot：从冻结隐层到可微偏置**

基线方法中，LLM的logits直接由隐层表示 $H$ 经输出投影矩阵 $W_{LM}$ 计算得到，模型参数完全冻结。SA在此引入一个关键的结构性改变：

$$
\mathrm{logits}' = (H + \delta) W_{LM}^T \tag{Eq. 2}
$$

自适应向量 $\delta$ 作为加性偏置作用于最终隐层表示，在每步交互中通过交叉熵损失进行单步梯度更新：

$$
\delta_{\mathrm{new}} = \delta_{\mathrm{old}} - \eta \nabla_{\delta} \mathcal{L}_{\mathrm{CE}}(f_{\theta,\delta}(\mathcal{T}_{1:n-1}), \mathcal{T}_{2:n}) \tag{Eq. 3}
$$

此设计的关键特性：
- **无监督自监督信号**：利用当前上下文序列（任务指令、观测、历史动作）作为自监督目标，无需任何外部标注。
- **极低延迟开销**：单步更新仅增加约**3%的延迟**（Table 4），适合实时部署场景。
- **逐回合重置**：每个新回合开始时 $\delta$ 重置为零向量，避免跨任务的灾难性遗忘。

这一设计的深层洞察在于：环境特定的句法模式（如函数调用签名、页面元素命名规范）已隐含在交互上下文中，通过让模型“预测自身所见”，即可快速将输出分布校准至目标环境的格式空间。

### 创新二：动态基础（DG）——上下文世界模型的自动构建

DG的核心创新在于**将世界模型从需要离线训练的预测模型转化为可通过探索自动提取的自然语言规则**，并以上下文形式注入智能体决策。

**Changed Slot：从训练依赖的世界模型到上下文规则集**

基线方法（如WMA, Chae et al., 2025）需要收集大量交互轨迹来训练一个独立的状态转移预测模型，这不仅成本高昂，且对非网页类环境（如纯对话场景）不适用。DG通过四阶段流水线实现零训练的环境动态获取：

1. **人格引导的探索任务合成**：基于环境描述，利用LLM合成多样化的人格和探索目标，确保覆盖广泛的状态转移模式。
2. **探索与动态提取**：探索智能体与环境交互，收集状态转移日志，并由LLM从中提取自然语言动态规则。
3. **过滤与整合**：使用推理模型过滤低信息量的规则（如常识性转移），仅保留环境特有的因果动态（Table 7显示过滤后规则数量从334条降至18-53条）。
4. **上下文增强**：将过滤后的规则集 $E_{\mathrm{clean}}$ 拼接到测试时输入中：

$$
\mathcal{T}' = [\mathcal{T}; E_{\mathrm{clean}}] \tag{Eq. 4}
$$

此方法的关键优势在于：
- **零训练成本**：仅需约50次探索rollout，无需任何模型训练。
- **自提升能力**：消融实验（Table 5）表明，使用任务模型自身（GPT-4o mini）同时作为探索策略和动态提取器，成功率达到**19.0%**，优于使用更强模型GPT-4.1作为提取器的**18.0%**——这意味着DG使智能体具备了“自我教学”的能力。
- **跨环境泛化**：在WebArena多站点任务上，DG将GPT-4.1成功率从**2%提升至23%**（+21%），在BFCLv3函数调用基准上从55.5%提升至64.0%（+8.5%），验证了其对复杂状态转移场景的显著增益。

### 两种策略的互补性与当前局限

SA和DG分别从**格式对齐**和**因果认知**两个维度增强智能体，且均可独立部署。然而，简单的策略组合（同时使用SA和DG）在某些场景下反而不如单独使用DG，表明两者可能存在上下文冲突或过度适应的问题——这指向了一个重要的开放问题：如何设计原则性的集成方法，使两种自适应机制协同而非互斥。



![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_OH4PE0TDo0/figures/001_Figure_1.jpg]]
*Figure 1: Overview of syntactic alignment (SA). This figure includes an example of web navigation shopping task to illustrate how the agent adapts to new environment. (1) At the start of each episode, we initialize an adaptation vector δ as a zero vector and construct inputs to the LLM agent. (2) During task execution, the agent receives environment instructions and observations. (3) At each step, we update the adaptation vector using cross-entropy loss on the current input, and apply the adaptation vector as a bias to the LLM’s final hidden layer. This enables rapid alignment to environment-specific observation and action formats. (4) The LLM agent takes a new action with the updated vector, which s...*

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_OH4PE0TDo0/figures/002_Figure_2.jpg]]

本文提出一套面向LLM智能体的测试时自适应框架，核心组件为**句法对齐（Syntactic Alignment, SA）**与**动态基础（Dynamics Grounding, DG）**。两者分别解决智能体在未知环境中面临的两类根本性不匹配：**句法不匹配**（如UI元素标签、响应格式差异）和**语义不匹配**（环境状态转移因果模型缺失）。框架的整体输入输出流如下：

**输入构建**：每个交互步，智能体的输入序列由任务指令 $p$、当前观测 $o$ 和历史动作序列 $\{a\}_{i=1}^{T-1}$ 拼接而成：

$$\mathcal{T} = [p; o; \{a\}_{i=1}^{T-1}] \tag{1}$$

**句法对齐模块**：在模型推理时，引入一个轻量级适应向量 $\delta \in \mathbb{R}^d$（$d$ 为隐藏维度），将其作为偏置项加到最后隐藏层表示 $H$ 上，再通过输出投影矩阵 $W_{\mathrm{LM}}$ 获得修正后的logits：

$$\mathrm{logits}' = (H + \delta) W_{\mathrm{LM}}^T \tag{2}$$

$\delta$ 在每个episode开始时初始化为零向量。每一步执行后，利用当前上下文的自监督信号——即对输入序列 $\mathcal{T}_{1:n-1}$ 预测 $\mathcal{T}_{2:n}$ 的交叉熵损失——进行单步梯度下降更新：

$$\delta_{\mathrm{new}} = \delta_{\mathrm{old}} - \eta \nabla_\delta \mathcal{L}_{\mathrm{CE}}\left(f_{\theta,\delta}(\mathcal{T}_{1:n-1}), \mathcal{T}_{2:n}\right) \tag{3}$$

该模块通过参数化方式快速将模型输出分布对齐到环境特定的句法格式，单步更新仅增加约3%的延迟开销（Table 4），适合实时部署。

**动态基础管线**：这是一条部署时一次性执行的离线管线，包含四个步骤（Figure 2）：
1. **人格与探索目标合成**：基于环境描述，利用LLM合成多样化的人格和探索任务。
2. **探索与动态提取**：探索智能体与环境交互，收集状态转移日志。
3. **过滤与整合**：使用推理模型过滤低信息量的动态规则，保留精炼的环境动态集合 $E_{\mathrm{clean}}$。
4. **上下文增强**：在测试时任务执行中，将 $E_{\mathrm{clean}}$ 拼接到输入序列中：

$$\mathcal{T}' = [\mathcal{T}; E_{\mathrm{clean}}] \tag{4}$$

通过将环境动态规则以自然语言形式注入上下文，智能体获得关于状态转移因果关系的显式知识，从而做出更明智的决策。

**模块关系与数据流**：SA和DG分别作用于模型内部表示和外部上下文两个层面。SA在每个交互步实时更新适应向量，直接修改logits分布；DG在部署前一次性完成探索，生成静态的环境动态规则集合，在测试时作为上下文前缀注入。两个模块可独立使用，也可组合——但简单组合在部分场景下反而不如单独使用DG，提示需要更原则性的集成方法。



### 3.1 输入构建

智能体在每个时间步的输入由任务指令、当前观测和历史动作拼接而成：

$$
\mathcal{T} = [p; o; \{a\}_{i=1}^{T-1}] \tag{1}
$$

其中 $p$ 为任务指令，$o$ 为当前环境观测，$\{a\}_{i=1}^{T-1}$ 为历史动作序列。该序列作为后续所有模块的统一输入基础。

### 3.2 句法对齐模块

句法对齐的核心思路是将当前上下文作为自监督信号，通过参数化方式在线调整模型输出分布，使其匹配目标环境的特定句法格式。

**适应向量注入**：引入一个轻量级适应向量 $\delta \in \mathbb{R}^d$（$d$ 为语言模型隐层维度），将其作为加性偏置作用于最终隐层表示 $H$，再通过输出投影矩阵 $W_{\mathrm{LM}}$ 计算修正后的 logits：

$$
\mathrm{logits}' = (H + \delta) W_{\mathrm{LM}}^{T} \tag{2}
$$

**在线更新**：在每个交互步，利用当前上下文序列 $\mathcal{T}_{1:n}$ 计算交叉熵损失，对 $\delta$ 执行单步梯度下降：

$$
\delta_{\mathrm{new}} = \delta_{\mathrm{old}} - \eta \nabla_{\delta} \mathcal{L}_{\mathrm{CE}}(f_{\theta,\delta}(\mathcal{T}_{1:n-1}), \mathcal{T}_{2:n}) \tag{3}
$$

其中 $\eta$ 为学习率，$f_{\theta,\delta}$ 为注入 $\delta$ 后的模型。每个新回合开始时，$\delta$ 被重置为零向量，以防止灾难性遗忘。

**效率特性**：单步更新仅增加约 3% 的延迟开销（Table 4），适合实时部署场景。

### 3.3 动态基础模块

动态基础通过一次性自动化探索，为智能体构建自然语言形式的上下文世界模型。该模块包含四个步骤：

1. **人格与探索目标合成**：基于环境描述，利用 LLM 合成多样化的人格和对应探索任务。
2. **探索与动态提取**：探索智能体与环境交互，收集状态转移日志。
3. **过滤与整合**：使用推理模型过滤低信息量规则，保留精简的环境动态集合 $E_{\mathrm{clean}}$。
4. **上下文增强**：在测试时任务执行中，将过滤后的动态规则拼接到输入序列：

$$
\mathcal{T}' = [\mathcal{T}; E_{\mathrm{clean}}] \tag{4}
$$

通过为智能体提供显式的环境状态转移知识，利用其上下文学习能力引导更准确的决策。

### 3.4 关键设计要点

- **SA 的轻量性**：仅引入一个与隐层维度等长的向量，不修改模型主体参数，保证极低的计算和存储开销。
- **DG 的一次性**：探索阶段仅需约 50 条探索轨迹，无需额外模型训练，为部署时一次性投入。
- **模块独立性**：SA 和 DG 可独立使用，但简单组合在部分场景下反而不如单独使用 DG，需要更原则性的集成方法。



## 实验与关键发现

### 核心瓶颈与因果机制

LLM智能体在未见环境中面临双重不匹配：**句法不匹配**（UI元素标签、响应格式等）导致产生无效动作；**语义不匹配**（缺失状态转移因果模型）导致规划失败。本文提出两条互补的测试时适应路径——句法对齐（SA）通过参数化在线微调解决句法不匹配，动态基础（DG）通过上下文世界模型解决语义不匹配。两者均仅依赖无监督的测试时环境交互信号。

### 主实验结果

**Table 2**汇总了WebArena、BFCLv3和Tau-Bench三个基准上的成功率。核心发现：

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_OH4PE0TDo0/figures/004_Table_2.jpg]]
*Table 2: Main results on WebArena, WebVoyager, BFCLv3, and Tau-Bench benchmarks. We report task success rates (%) for each model and adaptation method. For Tau-Bench, we average runs across 5 seeds and use a custom more stable codebase. Both test-time adaptation strategies improve performance. ”N/A” indicates not applicable—AWM requires training a web-specific world model on state transitions, which is not applicable to Tau-Bench (conversational only) or BFCLv3 (no explicit web-like state transition data); Dynamics grounding does not operate in conversational Tau-Bench as there is no explicit and fixed state transition rules in the environment*

- **DG带来一致且显著的提升**：GPT-4.1在WebArena上从30.0%提升至35.0%（+5.0%），在BFCLv3上从55.5%提升至64.0%（+8.5%）。GPT-4o mini在WebArena上从12.0%提升至18.0%（+6.0%），Qwen2.5-14B-Instruct从17.0%提升至20.0%（+3.0%）。
- **SA同样有效**：Qwen2.5-14B-Instruct在WebArena上通过SA达到18.0%（+1.0%），在BFCLv3上达到55.0%（+3.0%）。
- **跨模型泛化**：两种策略在GPT-4.1、GPT-4o mini和Qwen2.5-14B-Instruct三个模型上均表现出一致增益，验证了方法的模型无关性。

**Table 3**提供WebArena各网站的细分结果，揭示DG的真正价值所在：

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_OH4PE0TDo0/figures/005_Table_3.jpg]]
*Table 3: Success rates (%) on the WebArena benchmark across different websites and models. Both adaptation strategies improve performance over baselines. and dynamics grounding (DG) surpasses WMA on GPT-4o mini. DG improves success rate substantially on complex multi-site split*

- **多站点任务（Multi-site）是关键瓶颈**：GPT-4.1零样本在多站点任务上仅2.0%成功率，加入DG后跃升至23.0%（+21.0%）。这是本文最具决定性的证据——多站点任务要求智能体理解跨网站的因果依赖关系，DG提供的上下文动态规则直接弥补了这一能力缺口。
- **DG超越WMA**：GPT-4o mini搭配DG达到18.0%平均成功率，显著优于搭配WMA的13.5%。WMA需要预先收集轨迹训练世界模型，而DG的测试时动态提取不仅免训练，效果也更好。

### 效率与延迟分析

**Table 4**展示SA的延迟开销：在BFCLv3多轮任务上，单步SA更新仅增加3.0%的相对延迟，累积5步后总延迟增益为15.6%。这一开销在实时部署场景中可接受。DG作为一次性投入，仅需50次探索rollout且无需模型训练，计算成本集中在部署前。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_OH4PE0TDo0/figures/006_Table_4.jpg]]
*Table 4: Relative latency gain (%) of PA on BFCLv3 multiturn. LR fixed to 0.1*

### 消融实验

**探索策略与提取器的自洽性（Table 5）**：一项关键消融考察了探索策略和动态提取器使用不同模型的影响。结果表明，使用任务模型自身（self-configuration）进行探索和动态提取，可以达到甚至超越使用更强模型的效果——GPT-4o mini自配置达到19.0%，而使用GPT-4.1作为提取器仅18.0%。这意味着DG使弱模型能够通过测试时交互实现自提升，无需依赖外部强模型。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_OH4PE0TDo0/figures/007_Table_5.jpg]]
*Table 5: Ablation on exploration policy and dynamics extractor backbones on WebArena. Here we use different backbones of exploration policy and dynamics extractor. We found for dynamics grounding—using the same LLM agent (itself) improves the same as using a stronger one*

**动态过滤的必要性（Section 4.3）**：Table 7显示，原始提取的环境动态数量庞大（每网站334条），经过GPT-4.1推理模型过滤后锐减至18-53条。过滤带来的性能增益明确：在10个探索周期下，成功率从61.0%提升至64.0%（+3.0%）。不过，过滤依赖额外的推理模型调用，增加了pipeline开销。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_OH4PE0TDo0/figures/009_Table_7.jpg]]
*Table 7: Number of environment dynamics per website before and after filtering with GPT-4.1 as the exploration policy and dynamics extractor. Most environment dynamics are filtered out*

**SA超参数鲁棒性（Table 6）**：在Qwen2.5-Instruct 7B/14B/32B上系统扫描训练迭代次数（1-5步）和学习率（0.1/1.0）。SA总体上对超参数鲁棒，但极端设置会损害性能：7B模型在LR=1.0或5次迭代时成功率低于基线。最佳配置为LR=0.1、1-3次迭代，且更大模型（32B）的增益更显著（基线26.0%，最佳28.5%）。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_OH4PE0TDo0/figures/008_Table_6.jpg]]
*Table 6: Success rate (SR) of syntactic alignment across different Qwen2.5 instruct model sizes (7B, 14B, 32B) and training hyperparameters. Results are shown for varying numbers of training iterations and two learning rates (LR=0.1 and LR=1.0). Syntactic alignment adaptation generally improves SR over the baseline, with larger models and moderate learning rates yielding higher gains*

### 失败模式与局限

1. **策略组合的次优性**：简单同时使用SA和DG在部分场景下反而不如单独使用DG。分析推测是上下文冲突或过度适应导致——SA在线微调的分布偏移可能与DG提供的静态规则产生不一致。需要更原则性的集成方法。

2. **常识环境下的边际收益**：当环境动态符合LLM已有常识时，DG带来的提升有限，甚至可能因上下文变长而略微降低性能。这表明DG的价值集中在反常识或高度特异的环境动态上。

3. **探索覆盖的局限性**：DG的探索阶段依赖LLM合成的人格来生成探索任务，可能覆盖不完整或引入偏见。过滤步骤虽然缓解了噪声问题，但依赖额外的推理模型，增加了部署开销。

4. **任务范围限制**：当前验证限于函数调用（BFCLv3）和网页导航（WebArena），Tau-Bench上的DG不适用（因为对话环境缺乏显式的状态转移规则）。在更广泛的多模态或具身智能体场景中的泛化性尚不明确。

### 证据强度总结

| 核心主张 | 证据锚点 | 置信度 |
|---------|---------|--------|
| DG将多站点任务成功率从2%提升至23% | Table 3 | 0.98 |
| SA和DG均跨模型一致提升性能 | Table 2 | 0.95 |
| 自配置达到与强模型同等效果 | Table 5 | 0.95 |
| SA单步更新仅增加3%延迟 | Table 4, Section 4.2 | 0.95 |
| 过滤动态提升成功率+3.0% | Section 4.3 | 0.90 |

### 待验证与开放问题

- **元控制器设计**：如何根据环境复杂度自动决定采用SA、DG或两者组合，是方法实际部署的关键。当前需要人工选择策略。
- **更高效的动态发现**：50次探索rollout在部分场景下可能成本过高，探索更高效的动态发现与利用方式是降低部署门槛的方向。
- **更广泛场景验证**：在具身智能体、多模态环境中的有效性需要通过额外实验确认。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_OH4PE0TDo0/figures/003_Table_1.jpg]]
*Table 1: Number of tasks per website in the WebArena benchmark. The benchmark consists of six websites, including a multisite category for tasks that require interacting across multiple websites (from the six sites), for a total of 812 tasks*

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_OH4PE0TDo0/figures/010_Table_8.jpg]]
*Table 8: Number of functions available in each BFCLv3 environment*



## 定位与知识库关联

### 1. 问题定位：从静态零样本到测试时环境适应

传统LLM智能体在零样本设定下直接部署到新环境时，面临双重不匹配瓶颈：**句法不匹配**（环境特定的UI元素标签、API响应格式和动作语法与模型训练分布不一致，导致无效动作生成）和**语义不匹配**（环境状态转移的因果模型缺失，智能体无法预测动作后果，规划频繁失败）。现有解决方案大致分为两条路径：

- **上下文学习方法**：通过精心设计的提示词或示例引导智能体适应新环境，但受限于上下文窗口长度，且无法系统性地覆盖环境的因果动态。
- **世界模型方法**：如 **WMA**（Chae et al., 2025），通过收集交互轨迹训练专门的下一状态预测模型，为智能体提供环境动态知识。但该方法需要大量标注轨迹和额外模型训练，部署成本高，且不适用于纯对话或函数调用等非网页环境（如Tau-Bench、BFCLv3）。

本文提出的**句法对齐（Syntactic Alignment, SA）**和**动态基础（Dynamics Grounding, DG）**两条互补策略，在测试时利用无监督环境交互信号，以极低成本填补了这一空白。SA通过参数化的在线分布适配解决句法匹配问题，DG通过上下文世界模型构建解决语义匹配问题，二者均无需标注数据或额外模型训练。

### 2. 方法谱系中的位置

#### 2.1 句法对齐（SA）的知识库定位

SA的核心机制——在测试时通过无监督目标更新模型参数以匹配当前分布——可追溯到测试时训练（Test-Time Training, TTT）和测试时适应（Test-Time Adaptation, TTA）的研究脉络。在LLM领域，相关工作包括通过熵最小化或自监督学习更新模型参数或引导向量（steering vectors）的方法。SA的独特贡献在于：

- **参数效率**：仅引入单个轻量适应向量 $`\delta \in \mathbb{R}^d`$（d为模型隐层维度），作为最终隐层表示的加性偏置，而非更新全部模型参数。这使得单步更新仅增加约3%的延迟开销（Table 4），适合实时部署。
- **无灾难遗忘**：每个新episode开始时将 $`\delta`$ 重置为零向量，避免跨任务的知识干扰。
- **自监督信号**：以当前上下文序列（任务指令、观测和动作历史）的下一token预测交叉熵损失作为训练目标，无需外部标注。

与提示词工程或上下文示例方法相比，SA通过参数化方式直接修改模型输出分布，对句法变化的适应更系统且不消耗宝贵的上下文窗口空间。

#### 2.2 动态基础（DG）的知识库定位

DG定位于**上下文世界模型**这一新兴方向。与需要离线训练的WMA不同，DG将世界模型构建转化为一次性的测试时自动化流程：

- **探索阶段**：通过人格引导（persona-driven）合成多样化的探索任务，由LLM智能体自主与环境交互，收集状态转移日志。
- **动态提取**：LLM从交互日志中提取自然语言形式的环境动态规则（如“点击Go按钮会弹出日期选择器”）。
- **过滤与整合**：使用推理模型过滤低信息量规则，保留因果性强的状态转移知识。
- **上下文增强**：将过滤后的规则集 $`E_{\text{clean}}`$ 拼接到任务输入中，通过LLM的上下文学习能力引导智能体做出转移感知的决策。

DG的关键优势在于：仅需约50次探索rollout，无需任何模型训练；且消融实验表明（Table 5），使用智能体自身模型同时作为探索策略和动态提取器，可以达到与使用更强模型（如GPT-4.1）同等甚至更好的效果（GPT-4o mini self: 19.0% vs GPT-4.1 extractor: 18.0%），实现了**自我提升**。

### 3. 适用边界与局限性

#### 3.1 已知适用场景

- **网页导航**（WebArena, WebVoyager）：SA和DG均有效，DG在多站点复杂任务上增益尤为显著（GPT-4.1 Multi: 2.0% → 23.0%）。
- **函数调用**（BFCLv3）：DG通过探索API文档生成环境动态，成功率达64.0%（+8.5%）。
- **对话式任务**（Tau-Bench）：仅SA适用，因为纯对话环境不存在显式的固定状态转移规则，DG不适用。

#### 3.2 已知局限

1. **策略组合次优**：简单的SA+DG组合在部分场景下反而不如单独使用DG，需要更原则性的集成方法。
2. **常识环境增益有限**：当环境动态符合模型已有常识时，DG带来的提升有限，甚至可能因上下文变长而略微降低性能。
3. **泛化边界未验证**：目前仅在函数调用和网页导航任务上验证，对其他类型智能体环境（如多模态、具身智能体）的泛化性尚不明确。
4. **探索成本与覆盖**：DG的探索阶段依赖LLM合成的人格，可能覆盖不完整或引入偏见；动态过滤依赖额外的推理模型，增加了计算开销。
5. **SA超参数敏感性**：虽然SA对超参数总体鲁棒，但极端学习率（LR=1.0）或过多训练迭代（5步）会降低性能（Table 6），需要在部署时进行适度调参。

### 4. 开放问题

1. **自适应策略选择**：如何设计一个元控制器，根据环境复杂度自动决定何时采用在线句法适应或动态基础，以及如何动态分配计算预算？
2. **策略原则性集成**：SA和DG分别从参数化和上下文两个层面注入环境知识，如何在保留两者优势的同时更有效地结合，避免上下文冲突或过度适应？
3. **探索效率提升**：当前DG需要固定数量的探索rollout，如何更高效地发现和利用环境动态（如主动学习、不确定性引导的探索），以进一步降低探索成本？
4. **跨模态泛化**：在更广泛的多模态（视觉-语言）和具身智能体场景中，测试时适应策略的有效性和泛化能力如何？SA的隐层偏置机制能否直接迁移到多模态架构？
5. **动态更新与遗忘平衡**：SA的episode级重置策略避免了跨任务干扰，但在长期部署中是否丢失了有用的环境知识？能否设计更细粒度的记忆与遗忘机制？



## 原文 PDF

![[paperPDFs/ICLR_2026/Test_Time_Adaptation_for_LLM_Agents_via_Environment_Interaction.pdf]]
