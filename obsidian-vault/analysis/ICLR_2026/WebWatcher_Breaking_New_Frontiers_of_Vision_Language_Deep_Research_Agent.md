---
title: "WebWatcher: Breaking New Frontiers of Vision-Language Deep Research Agent"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/WebWatcher_Breaking_New_Frontiers_of_Vision_Language_Deep_Research_Agent.pdf
project_link: null
code_link: https://github.com/Alibaba-NLP/DeepResearch/tree/main/WebAgent/WebWatcher
openreview_forum_id: 8jsaazdAb3
aliases:
- WebWatcher
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过高质量合成轨迹的监督微调（SFT）作为冷启动，结合群体相对策略优化（GRPO）强化学习，使小规模视觉-语言模型掌握跨模态工具集成与深度推理。"
primary_logic: "利用实体模糊掩码构建知识密集型多跳视觉问答数据，辅以真实网页工具交互轨迹训练，可使小型视觉-语言模型在复杂跨模态基准上超越提示驱动工作流及大模型。"
claims:
- "WebWatcher-32B 在 HLE 上平均准确率达 13.6%，显著超过参考基线 OmniSearch 的 9.3%。"
- "冷启动 SFT 对 RL 训练至关重要，仅用指令数据初始化的模型奖励几乎为零，而冷启动能显著提升初始分数。"
- "工具调用分布随基准变化自动适应，例如在信息检索密集型基准上 Web Text Search 占主导，而在视觉推理基准上 Web Image Search 比例上升，证明智能体并非过度依赖单一工具。"
- "BrowseComp-VL Level 2 上的错误分析显示，多模态问题（图像检索失败+OCR）占比 28%，推理错误占 21%，突出跨模态对齐与推理仍是关键难题。"
---

# WebWatcher: Breaking New Frontiers of Vision-Language Deep Research Agent

> [!tip] 核心洞察
> 利用实体模糊掩码构建知识密集型多跳视觉问答数据，辅以真实网页工具交互轨迹训练，可使小型视觉-语言模型在复杂跨模态基准上超越提示驱动工作流及大模型。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | WebWatcher：突破视觉-语言深度研究智能体的新前沿 |
| 英文题名 | WebWatcher: Breaking New Frontiers of Vision-Language Deep Research Agent |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=8jsaazdAb3) · [GitHub](https://github.com/Alibaba-NLP/DeepResearch/tree/main/WebAgent/WebWatcher) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | WebWatcher |
| Dataset | Humanity's Last Exam (HLE), BrowseComp-VL (Avg), LiveVQA, MMSearch |

> [!tip] 效果简介
> - Humanity's Last Exam (HLE) 上，Avg Accuracy (%) 为 13.6，对比 9.3，变化 +4.3。
> - BrowseComp-VL (Avg) 上，Accuracy (%) 为 27.0，对比 16.3，变化 +10.7。
> - LiveVQA 上，Accuracy (%) 为 58.7，对比 41.3，变化 +17.4。

## 概要

**问题瓶颈**：当前多模态深度研究智能体普遍依赖模板驱动的静态流水线，缺乏将视觉信息与文本推理灵活结合的能力，难以在复杂视觉-语言任务中进行跨模态工具集成与深度推理。

**核心方法**：WebWatcher 提出了一条从数据到训练的完整技术路线。首先通过实体掩码与图像检索构建知识密集型多跳视觉问答数据（BrowseComp-VL），再利用 GPT-4o 生成高质量工具使用轨迹进行监督微调（SFT）作为冷启动，最后通过群体相对策略优化（GRPO）强化学习使小规模视觉-语言模型掌握跨模态工具协同与深度推理能力。

**方法定位**：WebWatcher 将训练范式从“直接推理或静态提示工作流”转变为“合成轨迹 SFT + GRPO 强化学习”，工具集成从单一视觉或搜索工具扩展为 Web Text Search、Web Image Search、Webpage Visit、Code Interpreter 与 Internal OCR 五类工具协同。

**主要结果**：
- WebWatcher-32B 在 Humanity’s Last Exam（HLE）上平均准确率达 **13.6%**，显著超过开源搜索代理 OmniSearch 的 9.3%（Table 1）。
- 在 BrowseComp-VL 上平均准确率达 **27.0%**，较 OmniSearch 的 16.3% 提升 10.7 个百分点；在 LiveVQA 上达 **58.7%**，较最佳提示工作流（Gemini-2.5-flash 41.3%）提升 17.4 个百分点（Table 2）。
- 消融实验证实：冷启动 SFT 对 RL 训练至关重要，仅用指令数据初始化的模型奖励几乎为零；工具调用次数在 ≥3 时性能最优（Best Pass@3 达 19.09），过少或过多均导致性能下降。

**局限与展望**：训练轨迹依赖 GPT-4o 生成，成本高且可扩展性受限；多模态感知错误（图像检索失败、OCR 错误）占 BrowseComp-VL Level 2 错误的 28%，跨模态对齐仍是关键瓶颈；强化学习仅使用最终答案的格式与语义奖励，缺乏中间推理步骤的密集反馈。未来方向包括构建闭环数据飞轮以逐步替代 GPT-4o、设计中间过程奖励模型缓解奖励稀疏问题，以及将工具集成范式推广至视频、音频等更多模态。

### 多模态深度研究智能体的能力瓶颈

大型视觉-语言模型（VLMs）在图像理解、视觉问答等任务上取得了长足进步，但当面对需要结合视觉与文本信息进行多步推理、主动检索外部知识并灵活调用多种工具的复杂现实任务时，现有方法暴露出显著局限。当前主流的深度研究智能体大多依赖模板驱动的静态工作流：它们按照预设的步骤执行搜索、提取和总结，缺乏根据中间观察动态调整策略的能力。这种“提示驱动工作流”（Prompt Workflow）范式将推理过程固化在固定的提示模板中，无法像人类研究者那样在信息不足时主动发起新的检索、在遇到歧义时切换信息源、或在需要计算时调用代码解释器。

更深层的瓶颈在于**跨模态信息融合与工具调用的割裂**。现有方案要么聚焦于纯文本的搜索增强推理，要么局限于单次视觉理解，鲜有将视觉感知、文本检索、网页浏览、代码执行和光学字符识别（OCR）等能力有机整合到统一的推理循环中。这导致智能体在处理多模态知识密集型任务时——例如需要识别图片中的实体并检索其相关文本信息，或需要从图表中提取数据并进行数值计算——往往顾此失彼，无法形成完整的推理链条。

### 现有方法的缺口

从方法谱系来看，当前应对复杂多模态推理的路线主要有三条，但各自存在明显短板：

- **直接推理模型**（如 GPT-4o、Gemini-2.5-flash、Claude-3.7-Sonnet、Qwen-2.5-VL 系列）将视觉-语言模型作为黑盒使用，完全依赖模型内部知识回答问题。这类方法受限于训练数据的时效性和覆盖范围，在需要最新信息或专业领域知识时表现乏力，且缺乏可验证的推理过程。

- **提示驱动工作流**（如 o3、GPT-4.1 等推理模型配备工具调用提示）为模型提供了与 WebWatcher 相同的工具集（Web Text Search、Web Image Search、Webpage Visit、Code Interpreter、OCR），但工具调用策略完全由静态提示模板控制，无法根据任务难度和中间结果自适应调整。这种方式虽然比直接推理有所改进，但本质上仍是将复杂推理压缩进固定的模板框架，缺乏真正的自主探索能力。

- **搜索导向的多模态代理**（如 OmniSearch，Li et al., 2025d）虽然引入了工具调用，但主要围绕文本搜索构建，视觉理解能力有限，在需要深度视觉推理的场景中表现不佳。

上述方法的共同缺陷在于：**它们将工具调用视为外挂的辅助模块，而非推理过程的内在组成部分**。这导致智能体无法在“观察—思考—行动”的循环中持续优化信息获取策略，也难以根据视觉线索动态调整搜索方向。

### 本文的核心动机

针对上述瓶颈，本文提出一个核心洞察：**通过让视觉-语言模型在高质量工具使用轨迹上进行监督微调（SFT）作为冷启动，再结合群体相对策略优化（GRPO）强化学习进行泛化训练，可以使小规模模型掌握跨模态工具集成与深度推理能力，在复杂基准上超越提示驱动工作流乃至更大规模的模型。**

这一动机源于以下关键观察：

1. **工具调用是可学习的推理行为**：人类研究者在面对复杂问题时，会自然地交替进行“观察图像—检索信息—阅读网页—计算验证”等操作。如果能够将这种多工具协同的推理过程以轨迹数据的形式注入模型训练，模型就有可能内化这种推理模式，而非机械地执行预设步骤。

2. **合成数据可以突破训练瓶颈**：高质量的多模态工具使用轨迹难以通过人工标注大规模获取。WebWatcher 通过实体模糊掩码技术，从超链接图自动构建知识密集型多跳视觉问答数据，并利用 GPT-4o 生成 ReAct 格式的工具调用轨迹，再经过严格的两阶段过滤保证数据质量。这使得大规模训练成为可能。

3. **强化学习提升泛化能力**：监督微调教会模型“如何正确使用工具”，但真实场景中的问题分布远比训练数据多样。GRPO 强化学习通过基于群体相对优势的策略优化，让模型在探索中学会将工具调用能力泛化到未见过的任务类型，同时通过格式奖励和语义准确奖励的加权组合引导模型保持输出规范。

WebWatcher 的设计目标不是构建一个更大的模型，而是**探索如何让相对小型的视觉-语言模型（7B/32B）通过后训练获得超越大模型的深度研究能力**。这一方向对降低部署成本、提升推理效率、以及推动开源社区的多模态智能体研究具有重要意义。

## 核心方法与创新机理

WebWatcher 的核心创新在于将多模态深度研究智能体从**模板驱动的静态工作流**升级为**具备跨模态工具集成与深度推理能力的学习型智能体**。其关键突破体现在三个维度：

### 从静态提示到可学习的工具调用策略

现有方法（如 GPT-4o Prompt Workflow、OmniSearch）依赖预设的提示模板来编排工具调用，缺乏对任务复杂性的动态适应能力。WebWatcher 通过 **SFT + GRPO 强化学习**的两阶段训练范式，使模型自主掌握*何时调用何种工具*的策略。消融实验证实，工具调用次数在 ≥3 时性能最优（Best Pass@3 达 19.09），过少或过多均导致性能下降（Table 3），说明模型学会了有效的工具预算分配。

### 从单模态工具到多工具协同

此前的工作通常仅集成单一视觉工具或单一搜索工具，难以应对需要跨模态信息融合的复杂查询。WebWatcher 统一配备五类工具：**Web Text Search、Web Image Search、Webpage Visit、Code Interpreter 和 Internal OCR**。工具调用分布随基准特性自动适应——在信息检索密集型基准上 Web Text Search 占主导，而在视觉推理基准上 Web Image Search 比例显著上升（Fig. 4），证明智能体并非过度依赖单一工具，而是形成了任务感知的工具选择能力。

### 从浅层 VQA 到知识密集型多跳推理数据构建

传统 VQA 数据集多为浅层单跳推理，无法支撑深度研究所需的复杂推理训练。WebWatcher 提出了**实体模糊掩码**的数据生成策略：从超链接图遍历构建文本 QA，对关键实体进行模糊化处理（如替换为“this entity”），再通过图像检索将文本 QA 转换为多模态 VQA，经两阶段过滤（Selector-Examiner）保证质量（Fig. 3）。这一流水线产出的 BrowseComp-VL 基准包含显式多跳推理（Level 1）和模糊化综合推理（Level 2）两个难度层级，为训练和评估提供了更贴近真实深度研究场景的数据基础。

### 冷启动 SFT：RL 训练的关键使能技术

一项决定性发现是：**仅用指令数据初始化的模型在 RL 训练中奖励几乎为零，而经过工具使用轨迹冷启动 SFT 的模型能显著提升初始分数**，并在 LiveVQA 上保持 0.06–0.18 的持续优势（Fig. 5）。这表明，对于视觉-语言模型而言，先通过监督学习显式教授工具调用模式和逐步推理过程，是后续强化学习能够有效展开的必要前提。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_8jsaazdAb3/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline for generating data, where multi-hop VQA pairs are built from hyperlink graphs, grounded with web images, filtered by selector–examiner checks, and transformed into Level 1 (explicit) and Level 2 (fuzzed) questions for multimodal reasoning*

WebWatcher 是一套面向视觉-语言深度研究智能体的训练与推理框架，其核心设计围绕“高质量合成轨迹冷启动 + 强化学习泛化”展开。整体 pipeline 由三个相互衔接的阶段构成：**数据构造流水线**、**监督微调 (SFT)** 和 **GRPO 强化学习**，并在推理时通过多工具执行引擎完成闭环决策。

### 数据构造流水线

框架的起点是构建大规模、知识密集型的多模态 VQA 数据。该流水线从权威源 (arXiv, GitHub, Wikipedia) 收集根 URL，递归遍历超链接图生成文本 QA 对，随后通过**实体掩码**将关键实体替换为模糊描述（如 “this entity”），迫使模型从上下文推断关系。为了引入视觉维度，系统利用 Google SerpApi 为每个保留的目标实体检索网页图像 (K=2)，将文本 QA 转换为多模态 VQA。所有样本经过两阶段过滤——Selector 检查问题可回答性、Examiner 验证答案一致性——以确保数据质量。最终产出分为 Level 1 (显式多跳推理) 和 Level 2 (模糊实体、更复杂的综合推理) 两个难度层级。

### 轨迹生成与监督微调

在获得高质量 VQA 实例后，框架使用 GPT-4o 为每个样本生成 ReAct 格式的**工具使用轨迹** $\tau = \{ (t_0, o_0), (t_1, o_1), \dots, (t_L, o_L) \}$，模拟逐步推理与工具调用的完整过程。轨迹经过答案匹配、步骤一致性和最小工具调用数量三重过滤后，作为 SFT 阶段的训练数据。SFT 的目标是最大化给定图像 $I$、问题 $q$ 和历史上下文下正确动作的对数似然：

$$\operatorname*{max}_{\theta} \sum_{i=1}^{K} \sum_{l=1}^{L_i} \log P_{\theta} ( t_l^{(i)} \mid I^{(i)}, q^{(i)}, t_{<l}^{(i)}, o_{<l}^{(i)} )$$

这一阶段教授模型基本的工具调用模式与跨模态推理行为，是后续 RL 训练不可或缺的冷启动。

### GRPO 强化学习

在 SFT 基础上，框架引入**群体相对策略优化 (GRPO)** 进行强化学习。GRPO 的核心在于用组内相对优势 $A_{\mathrm{rel}}(\tau^{(i)}) = R^{(i)} - \frac{1}{K} \sum_{j=1}^{K} R^{(j)}$ 替代对独立价值函数的依赖，并通过带 KL 惩罚的裁剪代理损失稳定策略更新：

$$\mathcal{L}_{\mathrm{GRPO}}(\boldsymbol{\theta}) = \mathbb{E}_{\boldsymbol{\tau}^{(i)} \in \mathcal{G}} \left[ \operatorname*{min} \left( \rho^{(i)} A_{\mathrm{rel}}(\boldsymbol{\tau}^{(i)}), \operatorname{clip}(\rho^{(i)}, 1-\epsilon, 1+\epsilon) A_{\mathrm{rel}}(\boldsymbol{\tau}^{(i)}) \right) \right] - \beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\theta_{\mathrm{old}}})$$

奖励信号由格式正确性 $r_{\mathrm{f}}$ 和答案语义准确性 $r_{\mathrm{a}}$ 加权组成：$R = w r_{\mathrm{f}} + (1 - w) r_{\mathrm{a}}$，其中 $w=0.2$。消融实验 (Fig. 5) 表明，冷启动 SFT 对 RL 训练至关重要——仅用指令数据初始化的模型奖励几乎为零，而冷启动能显著提升初始分数并在 LiveVQA 上保持 0.06–0.18 的优势。

### 多工具执行引擎

推理时，WebWatcher 通过 ReAct 循环调度五类工具：**Web Text Search**、**Web Image Search**、**Webpage Visit**、**Code Interpreter** 和 **Internal OCR**。模型在每个步骤根据当前观察决定调用何种工具，接收返回结果后迭代决策，直至生成最终答案。工具调用分布随基准自动适应——在信息检索密集型基准上 Web Text Search 占主导，而在视觉推理基准上 Web Image Search 比例显著上升 (Fig. 4)，证明智能体具备跨任务工具选择能力，而非过度依赖单一工具。

### 关键瓶颈与局限

尽管框架设计完整，仍存在若干结构性瓶颈：训练轨迹依赖 GPT-4o 生成，成本高且可能引入模型偏差；RL 仅使用最终答案的格式与语义奖励，缺乏对中间推理步骤的密集反馈，奖励稀疏问题突出；多模态感知错误（图像检索失败、OCR 错误）占 BrowseComp-VL Level 2 错误案例的 28% (Fig. 7)，跨模态对齐仍是核心难题。

### 轨迹定义与数据生成流水线

WebWatcher 的训练数据构建围绕**实体模糊掩码**展开，核心思路是将知识密集型多跳问答转化为需要跨模态工具调用的推理任务。数据生成流水线（Figure 3）包含以下关键模块：

1. **超链接图遍历与文本 QA 生成**：从权威源（arXiv、GitHub、Wikipedia）收集根 URL，递归遍历超链接构建知识图，利用 GPT-4o 合成 Level 1（显式多跳）的问答对。超链接树节点数由 $ (k^{\tilde{d}+1} - 1) / (k' - 1) $ 给出，其中 $d$ 为遍历深度，$k$ 为分支因子。

2. **实体掩码与模糊化**：通过两阶段框架（节点选择 + 查询生成与实体掩码）构建 Level 2 问答对。目标实体 $\hat{B}$ 在问题 $q_t$ 中被替换为视觉引用标记 $r_{vis}$（如“this entity”、“the object in the image”），生成变换后的 VQA 查询 $q$，迫使模型从上下文中推断实体关系。

3. **视觉接地**：对每个保留的目标实体，通过 Google SerpApi 检索 $K=2$ 张网页图像，将纯文本 QA 转化为多模态 VQA。

4. **质量过滤**：采用两阶段过滤流水线——Selector 检查问答对的可回答性与一致性，Examiner 验证图像与问题的语义对齐——确保训练样本的高质量。

### 轨迹自动标注与过滤

给定 BrowseComp-VL 中的 VQA 实例 $(I, q, a)$，使用 GPT-4o 生成 ReAct 格式的工具使用轨迹，模拟逐步人类推理过程。每条轨迹定义为动作-观察对的序列：

$$
\tau = \{ (t_0, o_0), (t_1, o_1), \dots, (t_L, o_L) \} \tag{1}
$$

其中 $t_l$ 为第 $l$ 步的工具调用动作，$o_l$ 为返回的观察结果。轨迹经过三重过滤：答案匹配度、步骤一致性和最小工具调用数量，确保训练轨迹的可靠性和推理深度。

### 监督微调（SFT）目标

SFT 阶段最大化给定图像、问题和历史上下文中正确动作的对数似然，教授模型工具调用与推理模式：

$$
\operatorname*{max}_{\theta} \sum_{i=1}^{K} \sum_{l=1}^{L_i} \log P_{\theta} ( t_l^{(i)} \mid I^{(i)}, q^{(i)}, t_{<l}^{(i)}, o_{<l}^{(i)} ) \tag{2}
$$

其中 $K$ 为轨迹数量，$L_i$ 为第 $i$ 条轨迹的长度，$\theta$ 为模型参数。该目标使模型学会在给定当前图像、问题和完整交互历史的条件下，预测正确的下一步动作。

### GRPO 强化学习目标

RL 阶段采用群体相对策略优化（GRPO），无需单独的价值函数。核心机制是**组内相对优势**：

$$
A_{\mathrm{rel}}(\tau^{(i)}) = R^{(i)} - \frac{1}{K} \sum_{j=1}^{K} R^{(j)} \tag{3}
$$

其中 $R^{(i)}$ 为第 $i$ 条轨迹的总奖励，$K$ 为组大小。该优势函数通过减去组内平均奖励来归一化，消除对价值函数估计的依赖。

GRPO 的裁剪代理损失结合 KL 惩罚，稳定策略更新：

$$
\mathcal{L}_{\mathrm{GRPO}}(\boldsymbol{\theta}) = \mathbb{E}_{\boldsymbol{\tau}^{(i)} \in \mathcal{G}} \left[ \operatorname*{min} \left( \rho^{(i)} A_{\mathrm{rel}}(\boldsymbol{\tau}^{(i)}), \operatorname{clip}(\rho^{(i)}, 1-\epsilon, 1+\epsilon) A_{\mathrm{rel}}(\boldsymbol{\tau}^{(i)}) \right) \right] - \beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\theta_{\mathrm{old}}}) \tag{4}
$$

其中 $\rho^{(i)}$ 为新旧策略的概率比，$\epsilon$ 为裁剪范围，$\beta$ 控制 KL 惩罚强度。

### 奖励设计

总奖励由格式正确性和答案语义准确性加权组成：

$$
R = w r_{\mathrm{f}} + (1 - w) r_{\mathrm{a}} \tag{5}
$$

其中 $r_{\mathrm{f}}$ 为格式奖励（检查输出是否符合 ReAct 格式），$r_{\mathrm{a}}$ 为语义准确奖励（通过 LLM-as-Judge 评估答案正确性），权重 $w=0.2$。该设计确保了模型在遵循工具调用规范的同时，追求答案的语义正确性。

### 多工具执行引擎

推理时，WebWatcher 在 ReAct 循环中调度五种工具：Web Text Search、Web Image Search、Webpage Visit、Code Interpreter 和 Internal OCR。模型根据当前观察和历史上下文自主决定调用何种工具，观察结果返回后迭代决策，直至生成最终答案。Figure 4 显示工具调用分布随基准自适应变化：信息检索密集型基准上 Web Text Search 占主导，视觉推理基准上 Web Image Search 比例上升，证明智能体并非过度依赖单一工具。

### 关键消融发现

冷启动 SFT 对 RL 训练至关重要。Figure 5 显示，仅用指令数据初始化的模型奖励停滞在接近零水平，而冷启动能显著提升初始分数，并在 LiveVQA 上保持 0.06–0.18 的持续优势。工具调用次数消融（Table 3）表明，调用次数 $\geq 3$ 时 Best Pass@3 达到 19.09，过少或过多均降低性能，验证了适度工具交互对深度推理的必要性。

## 实验与关键发现

### 核心结果：多模态深度研究智能体的全面突破

WebWatcher 在 Humanity‘s Last Exam (HLE) 及 BrowseComp-VL 等四个挑战性基准上进行了系统评估。所有提示驱动工作流基线均配备了与 WebWatcher 相同的工具集（Web Text/Image Search、Visit、Code Interpreter、OCR），确保对比公平。

**HLE 基准结果**（Table 1）：WebWatcher-32B 取得 13.6% 的平均准确率，显著超过开源搜索导向多模态代理 **OmniSearch** (Li et al., 2025d) 的 9.3%（+4.3 个百分点），并在生物学子领域达到 33.8% 的突出表现。WebWatcher-7B 亦达到 10.6%，展现出良好的参数效率。相比之下，直接推理基线（GPT-4o、Gemini-2.5-flash 等）的平均准确率仅为 2.6%–6.5%，提示驱动工作流（含 o3、GPT-4.1 等）亦未突破 10%。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_8jsaazdAb3/figures/004_Table_1.jpg]]
*Table 1: Main results on HLE. All accuracy scores are reported as percentages. Avg signifies the average accuracy score of three inference runs across different subtopics*

**四个挑战基准结果**（Table 2）：WebWatcher-32B 在 BrowseComp-VL 上取得 27.0% 的平均准确率（Level 1: 28.4%，Level 2: 25.0%），较 OmniSearch 的 16.3% 提升 +10.7 个百分点。在 LiveVQA 上达到 58.7%，超越最佳提示工作流 Gemini-2.5-flash 的 41.3%（+17.4 个百分点）；在 MMSearch 上取得 55.3%，较 OmniSearch 的 49.7% 提升 +5.6 个百分点。值得注意的是，在 SimpleVQA 上 WebWatcher-32B 的 59.0% 低于 o3 Prompt Workflow 的 70.3%（-11.3 个百分点），提示该方法在浅层视觉问答场景下存在工具调用的冗余开销。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_8jsaazdAb3/figures/005_Table_2.jpg]]
*Table 2: Main results on four challenging benchmarks. All accuracy scores are reported as percentages. Avg signifies the average score of three inference across two difficult levels*

**人类基线对比**（Table 4）：在 BrowseComp-VL 上，人类标注者使用相同工具集，每个问题由至少两位标注者独立作答。人类在 Level 1 上准确率为 33.2%（高于 WebWatcher-32B 的 28.4%），但在 Level 2 上仅为 18.0%（低于 WebWatcher-32B 的 25.0%），表明 Level 2 的模糊化实体和多跳推理对人类同样极具挑战。智能体在可解案例上的平均耗时仅 0.3–0.5 分钟，远低于人类的 14.7–20.0 分钟，凸显其效率优势。

### 工具调用分布：自适应多工具协同

Figure 4 展示了四个基准上的外部工具调用分布，揭示了智能体的自适应行为模式。在信息检索密集型基准（HLE、BrowseComp-VL）上，Web Text Search 占主导地位；而在视觉推理密集的 LiveVQA 上，Web Image Search 的比例显著上升。Webpage Visit 和 Code Interpreter 在需要深入页面解析或数值计算的场景中被选择性激活。这一分布自适应特性证明智能体并非过度依赖单一工具，而是根据任务需求动态调度多工具协同。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_8jsaazdAb3/figures/014_Figure_4.jpg]]
*Figure 4: The percentage of external tool calls in the four benchmarks. The height of each bar denotes the fraction of total calls made to that tool within the corresponding benchmark. Internal OCR is not included since only external tools are counted here. Score on HLE Benchmark*

### 消融实验：工具调用次数与冷启动的关键作用

**工具调用次数消融**（Table 3）：当工具调用次数 ≥3 时，Best Pass@3 达到 19.09，性能最优。过少（1–2 次）导致信息获取不足，过多（≥5 次）则引入噪声和效率损失，呈现倒 U 型关系。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_8jsaazdAb3/figures/006_Table_3.jpg]]
*Table 3: Performance across different tool call counts*

**冷启动 SFT 的关键性**（Figure 5）：仅用指令数据初始化的模型在 RL 训练中奖励停滞在接近零的水平，几乎无法从 GRPO 中获益。而经过工具使用轨迹冷启动 SFT 的模型初始分数显著提升，并在 LiveVQA 上保持 0.06–0.18 的持续优势。这一结果确证了高质量合成轨迹的监督微调是 RL 有效训练的**必要条件**——它教会模型基本的工具调用模式和推理结构，为后续策略优化提供了可优化的初始策略。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_8jsaazdAb3/figures/016_Figure_5.jpg]]
*Figure 5: Performance comparison using cold start in RL training on three benchmarks*

**Pass@k 扩展性**（Figure 6）：WebWatcher-32B 在 HLE 上的 Pass@k 随 k 增加而单调提升，k=32 时达到 41.9%，但 Token 成本线性增长（Table 7），存在明显的收益递减。

### 失败模式分析：跨模态对齐仍是核心瓶颈

Figure 7 展示了 BrowseComp-VL Level 2 上 100 个失败轨迹的错误分布：

- **文本检索错误**占比最高（32%），包括查询不精确、搜索结果不相关等；
- **多模态感知错误**占 28%，涵盖图像检索失败和 OCR 识别错误，突显跨模态对齐仍是关键难题；
- **推理错误**占 21%，表现为多跳逻辑链断裂或错误综合；
- 其余失败来自工具调用格式错误、超时等。

这一分布揭示了当前瓶颈的层次结构：信息获取的可靠性（文本+视觉检索）是推理质量的上限约束，而跨模态对齐的脆弱性进一步放大了这一约束。

### 评估可靠性保障

LLM-as-Judge 与人类专家的一致性达 99.4%（Cohen‘s κ 0.91，Table 8），保证了自动评测的可靠性。BrowseComp-VL 的 QA 对由三位博士级专家独立验证，初始一致率为 89.3%（Cohen’s κ 0.86），问题质量高度可靠。

## 定位与知识库关联

### 与基线方法的关系

WebWatcher 的核心突破在于将视觉-语言模型的推理能力从“模板驱动”推向“自主工具集成”。传统方案大致分为三类：

**直接推理模型**（如 GPT-4o、Gemini-2.5-flash、Claude-3.7-Sonnet、Qwen-2.5-VL 系列）完全依赖模型内部知识，不调用外部工具。在 HLE 基准上，这些模型的平均准确率仅为 2.6%–6.5%（Table 1），暴露了纯参数化知识在复杂跨模态任务中的根本局限。

**提示驱动工作流**（Prompt Workflow）为上述模型配备了与 WebWatcher 完全相同的工具集（Web Text Search、Web Image Search、Webpage Visit、Code Interpreter、OCR），但依赖静态提示模板来编排工具调用序列。在 BrowseComp-VL 上，最强提示工作流（o3）的平均准确率为 16.3%，而 WebWatcher-32B 达到 27.0%，提升 10.7 个百分点（Table 2）。这表明，即使工具相同，缺乏从轨迹中学习到的动态决策能力，提示驱动方案仍难以应对需要灵活切换工具和跨模态推理的深度研究任务。

**开源搜索导向代理**，以 **OmniSearch**（Li et al., 2025d）为代表，是当前最相关的开源基线。OmniSearch 基于 GPT-4o 构建，侧重文本搜索，在 HLE 上平均准确率为 9.3%。WebWatcher-32B 在同一基准上达到 13.6%（Table 1），提升 4.3 个百分点。关键差异在于：WebWatcher 通过合成轨迹的监督微调（SFT）和群体相对策略优化（GRPO）强化学习，使小型视觉-语言模型（7B/32B）内化了跨模态工具协同能力，而非依赖大规模专有模型的提示编排。

在 BrowseComp-VL 的人类基线对比中（Table 4），WebWatcher-32B 在 Level 2 上以 25.0% 超过人类专家的 18.0%，但在 Level 1 上（28.4% vs 33.2%）仍落后。这揭示了一个重要边界：当任务涉及明确的实体和关系链时，人类的先验知识仍具优势；但当问题经过实体模糊化处理后，智能体的系统化搜索能力反而更具鲁棒性。

### 适用边界

WebWatcher 的适用场景具有明确的边界条件：

**信息检索密集型任务**是 WebWatcher 的优势区间。工具调用分布（Figure 4）显示，在 HLE 和 BrowseComp-VL 上 Web Text Search 占主导地位（约 60%–70%），而在 LiveVQA 和 MMSearch 等视觉推理密集型基准上，Web Image Search 的调用比例显著上升。这种自适应分布表明，智能体并非过度依赖单一工具，而是根据任务需求动态调整策略。

**简单视觉问答**是 WebWatcher 的劣势区间。在 SimpleVQA 上，WebWatcher-32B 的准确率（59.0%）显著低于 o3 提示工作流（70.3%）（Table 2）。原因在于 SimpleVQA 任务通常只需单步推理，工具调用引入的额外延迟和潜在错误反而降低了效率。这暗示 WebWatcher 的架构更适合需要多跳推理和外部知识检索的复杂任务。

**工具调用次数**存在最优区间。消融实验（Table 3）表明，当工具调用次数 ≥3 时，Best Pass@3 达到 19.09%；过少（=1 时仅 12.27%）或过多（≥6 时降至 17.57%）均导致性能下降。这反映了深度研究任务中“探索-利用”权衡：过少调用导致信息不足，过多调用引入噪声和错误累积。

### 局限与开放问题

**训练数据瓶颈**：合成轨迹依赖 GPT-4o 生成，成本高且可扩展性受限。这不仅是工程问题，更可能引入模型偏差——GPT-4o 的推理模式成为 WebWatcher 的“认知天花板”。如何构建闭环数据飞轮，逐步用开源模型替代 GPT-4o 生成训练轨迹，同时保持轨迹质量，是当前未解决的关键挑战。

**跨模态感知错误**：BrowseComp-VL Level 2 的错误分析（Figure 7）显示，多模态感知问题（图像检索失败 + OCR 错误）占比 28%，文本检索错误占 32%，推理错误占 21%。图像检索失败往往源于查询与目标图像之间的语义鸿沟，而 OCR 错误则暴露了当前视觉编码器在细粒度文字识别上的不足。这些错误并非工具调用策略所能解决，而是底层视觉-语言对齐的根本瓶颈。

**奖励稀疏性**：GRPO 强化学习仅使用最终答案的格式奖励（$r_f$）和语义准确奖励（$r_a$）的加权和（$R = w r_f + (1-w) r_a$，$w=0.2$，Eq. 5），缺乏对中间推理步骤的密集反馈。这导致长轨迹中的策略梯度信号极为稀疏，限制了复杂多步推理的稳定性和效率。设计中间过程奖励模型（process reward model）以提供步骤级反馈，是提升 RL 训练效果的重要方向。

**任务难度上限**：BrowseComp-VL Level 2 的人类准确率仅 18%（Table 4），表明任务本身极为困难。WebWatcher 在该级别上超越人类，但绝对准确率仍仅 25%，说明当前方法距离可靠解决此类深度研究任务仍有较大差距。

### 开放问题

1. **数据飞轮闭环**：如何系统化地用开源模型替代 GPT-4o 生成训练轨迹，在降低成本的同时保持轨迹质量？这需要设计自动化的轨迹质量评估机制和迭代自提升框架。

2. **模态泛化**：WebWatcher 的工具集成范式能否推广到视频、音频等模态，构建通用的多媒体深度研究智能体？这涉及工具接口的标准化和跨模态轨迹的统一表示。

3. **持续学习**：在动态变化的 Web 环境中，如何让智能体持续学习新工具和新型信息源，避免知识陈旧？这需要探索在线 RL 或元学习策略，使智能体能够从交互中自适应更新。

4. **过程奖励设计**：如何构建有效的中间过程奖励模型，以缓解 RL 的奖励稀疏问题？这涉及对推理步骤的自动评估和密集反馈信号的生成。

5. **检索鲁棒性**：文本检索错误占比最高（32%），如何通过查询改写、多源融合、检索结果验证等策略显著降低信息检索失败率？这需要将检索增强生成（RAG）领域的最新进展与智能体的工具调用策略深度融合。

## 原文 PDF

![[paperPDFs/ICLR_2026/WebWatcher_Breaking_New_Frontiers_of_Vision_Language_Deep_Research_Agent.pdf]]
