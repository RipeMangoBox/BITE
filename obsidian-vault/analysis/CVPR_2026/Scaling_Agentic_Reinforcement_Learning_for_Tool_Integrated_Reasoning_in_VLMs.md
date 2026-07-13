---
title: Scaling Agentic Reinforcement Learning for Tool-Integrated Reasoning in VLMs
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Scaling_Agentic_Reinforcement_Learning_for_Tool_Integrated_Reasoning_in_VLMs.pdf
project_link: null
code_link: "https://github.com/Lucanyc/VISTA-Gym"
aliases:
- VR
- SARLTIRV
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 通过构建标准化工具交互环境（VISTA-Gym），并对模型进行两阶段训练（模仿学习预热 + 在线强化学习），使模型学会在推理过程中动态地、正确地选择、调用和协调工具，从而将工具使用与推理过程紧密结合。
primary_logic: 将工具集成推理建模为POMDP，通过统一的任务和工具接口环境提供可执行的交互循环和可验证反馈，并利用GRPO群组相对策略优化算法，以稀疏、格式感知的奖励设计训练模型，使模型内化“思考→工具调用→答案”的协议，显著提升了工具使用能力和跨任务泛化能力。
claims:
- VISTA-R1-8B在11个视觉推理基准上超过同规模基线9.51%-18.72%（使用工具），即使不使用工具也超出2.03%-11.24%。
- 消融实验显示，同时结合推理与工具使用（VISTA-R1）准确率达71.14%，远高于仅推理（63.66%）或仅工具（48.40%）的变体。
- RL训练相比仅SFT带来+10.19%的额外提升，GRPO算法在多个变体中表现最鲁棒。
- 工具调用错误分析表明，经过VISTA-Gym训练后，多数工具调用与推理错误得到解决。
---

# Scaling Agentic Reinforcement Learning for Tool-Integrated Reasoning in VLMs

> [!tip] 核心洞察
> 将工具集成推理建模为POMDP，通过统一的任务和工具接口环境提供可执行的交互循环和可验证反馈，并利用GRPO群组相对策略优化算法，以稀疏、格式感知的奖励设计训练模型，使模型内化“思考→工具调用→答案”的协议，显著提升了工具使用能力和跨任务泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向视觉-语言模型集成工具推理的规模化智能体强化学习 |
| 英文题名 | Scaling Agentic Reinforcement Learning for Tool-Integrated Reasoning in VLMs |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.19773) · [Code](https://github.com/Lucanyc/VISTA-Gym) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | VISTA-R1 |
| Dataset | ChartQA, Geometry3K, MapQA, 11-dataset overall average |

> [!tip] 效果简介
> - ChartQA 上，ACC 91.92 (InternVL3-8B) vs 77.32 (InternVL3-8B), best baseline ~85.92 (GPT-5) (+14.60 over InternVL3-8B; +1.16 over GPT-5)。
> - Geometry3K 上，ACC 61.27 (InternVL3-8B) vs 47.09 (InternVL3-8B) (+14.18)。
> - MapQA 上，ACC 68.45 (InternVL3-8B) vs 34.70 (InternVL3-8B) (+33.75)。

## 概要

视觉-语言模型（VLMs）在复杂多模态推理中日益重要，但现有开源VLMs在集成外部视觉工具时暴露出根本性瓶颈：直接暴露工具反而导致准确率显著下降（Figure 1），而单纯的内在推理（CoT）对复杂视觉问答的增益有限。错误分析表明，核心问题在于模型缺乏“何时调用工具、调用哪个工具、如何调用工具”的动态决策能力，以及工具执行后正确整合信息进行推理的能力（Table 1）。

针对这一瓶颈，本文提出 **VISTA-Gym**——一个标准化、可扩展的交互式训练环境，以及基于其训练的智能体 **VISTA-R1**。核心思路是将工具集成推理建模为部分可观测马尔可夫决策过程（POMDP），通过统一的Gymnasium式API将7类推理任务、13个公开数据集与26种视觉工具封装为可执行交互循环，并采用两阶段训练范式：先以行为克隆（BC）在过滤后的专家轨迹上预热，再通过群组相对策略优化（GRPO）进行多轮在线强化学习，配合稀疏、格式感知的组合奖励，使模型内化“思考→工具调用→答案”的协议。

主要结果上，以InternVL3-8B为骨干的 **VISTA-R1-8B** 在11个视觉推理基准上平均准确率达71.14%，较同规模基线InternVL3-8B（57.49%）提升13.65个百分点，在ChartQA（91.92 vs 77.32）、Geometry3K（61.27 vs 47.09）、MapQA（68.45 vs 34.70）等任务上提升尤为显著，甚至超过部分商用模型（如GPT-5的ChartQA 85.92）。消融实验进一步证实，同时启用推理与工具使用（71.14%）远优于仅推理（63.66%）或仅工具（48.40%）的变体；RL训练在SFT预热基础上额外贡献+10.19%的提升，GRPO算法在多种RL变体中表现最鲁棒。

在方法谱系中，VISTA-R1区别于 **VTool-R1**、**R1-VL**、**R1-Onevision**、**Perception-R1** 等近期工具/推理集成基线，其关键创新在于：(1) 构建了首个面向视觉工具集成推理的大规模交互式训练环境VISTA-Gym，而非仅在静态数据上训练；(2) 采用BC+在线RL的两阶段训练范式，使模型在真实交互反馈中学习动态工具协调；(3) 设计了格式感知的稀疏奖励，显式约束“思考-工具调用-答案”的结构化输出。该方法在知识库中定位为“面向VLM的工具增强推理智能体训练框架”，为开源模型缩小与商用模型在工具集成推理上的差距提供了可复现的训练方案。



### 视觉推理的范式瓶颈：从“看”到“算”的断裂

视觉-语言模型（VLMs）在图像描述、物体识别等感知任务上已取得显著进展，但在需要精确量化、空间计算或结构化解析的复杂视觉推理任务（如几何问题求解、图表问答、地图分析）中，其表现仍远逊于人类。根本原因在于，VLMs的推理能力受限于其静态的视觉嵌入——模型只能“看”图像，却无法“计算”图像。例如，在几何问题中，模型需要测量角度、计算线段长度；在图表问答中，需要提取数据点并进行数值比较；在地图分析中，需要计算距离和方位。这些操作本质上超出了纯视觉编码的能力边界，必须借助外部工具（如OCR引擎、数学求解器、目标检测器）来完成。

### 工具集成的“反直觉”陷阱：暴露即退化

一个直观的解决方案是直接向VLMs提供工具访问权限。然而，本研究通过大规模错误分析（Table 1，500个错误样本）揭示了一个关键悖论：**未经专门训练的VLMs在获得工具后，准确率反而显著下降**（Figure 1，w/ T 条件）。具体而言，工具调用失败呈现六种典型模式：

- **E2（工具选择错误）**：开源模型InternVL3-8B的错误率高达44.8%，而商用模型GPT-5仅为0.0%，表明开源模型在工具选择上存在严重缺陷。
- **E4（工具执行后推理错误）**：GPT-5和InternVL3-8B的错误率分别为39.6%和57.4%，说明即使工具调用正确，模型也难以有效利用返回结果进行后续推理。
- **E6（感知错误）**：InternVL3-8B的错误率达64.8%，反映其基础视觉理解能力不足。

这些错误模式揭示了一个深层问题：工具并非“即插即用”的增强模块，而是一个需要与推理过程动态协调的交互对象。直接暴露工具而不提供推理指导，模型会陷入工具选择的随机性、工具结果的误用，甚至因工具返回的噪声信息而偏离正确的推理路径。

### 现有方法的缺口：静态推理与粗糙工具暴露

当前主流方法存在两类根本性缺陷：

1. **纯推理方法**（如Chain-of-Thought）：虽能提升模型的自洽性，但无法突破视觉编码的信息瓶颈。Figure 1显示，仅启用推理（w/ R）在复杂VQA任务上的增益有限，因为模型仍缺乏精确计算的能力。

2. **粗糙工具暴露方法**：要么仅提供单一工具（如OCR），要么将工具结果作为静态上下文注入，缺乏交互式、多轮的工具协调机制。即使提供工具选择先验知识并交错推理与工具执行（w/ T&R），性能改善也高度依赖任务类型和模型规模，小型开源模型尤其挣扎。

更关键的是，现有的开源VLMs（如InternVL3、Qwen2.5-VL）在未经过专门训练的情况下，**完全不具备将推理与工具使用动态协调的能力**。Table 3显示，不经RL训练时，直接增强工具（w/ Tools）反而导致准确率下降，而交错推理与工具（w/ T&R）的提升也十分有限。这表明，工具集成推理（Tool-Integrated Reasoning, TIR）并非模型固有的涌现能力，而是一种需要专门训练才能获得的技能。

### 本文动机：构建可训练的TIR智能体

基于上述分析，本文的核心动机是：**将工具集成推理从“提示工程”升级为“训练范式”**。具体而言，需要解决三个关键挑战：

1. **统一的环境与接口**：构建标准化的交互环境，将多样化的视觉推理任务和工具封装为统一的API，使模型能在一致的框架下学习工具使用。

2. **可扩展的训练机制**：设计两阶段训练策略——首先通过模仿学习使模型掌握工具调用的语法与格式，再通过在线强化学习深化其工具集成推理能力，使模型内化“思考→工具调用→答案”的协议。

3. **稀疏但有效的奖励设计**：在缺乏中间步骤标注的情况下，设计格式感知的组合奖励，引导模型避免重复、保持结构有效，并最终给出正确答案。

这一动机的落脚点是：通过规模化智能体强化学习，使小型开源VLM获得超越其体量的工具增强推理能力，甚至在某些任务上媲美大规模商用模型。



## 核心方法与创新机理

### 1. 从“静态工具暴露”到“交互式工具推理”的范式转变

现有视觉-语言模型（VLM）在工具使用上存在根本性缺陷：**直接向模型暴露工具而不提供推理指导，反而导致准确率显著下降**。如图1所示，当基础VLM被直接赋予工具调用能力（w/ T）时，性能出现明显退化；而仅依靠内在推理（w/ R）在复杂视觉问答上的增益也十分有限。对500个错误样本的深入分析（Table 1）揭示了失败的核心模式：模型在“是否调用工具”“何时调用”“调用哪个工具”“如何选择模式和参数”等环节（E1–E5）出现大量错误，而调用工具后的推理错误（E6）则进一步放大了问题。这说明，**工具本身并非即插即用的增益模块，而是对模型的推理-行动协调能力提出了更高要求**。

VISTA-R1的核心创新在于将工具集成推理（Tool-Integrated Reasoning, TIR）建模为一个**部分可观测马尔可夫决策过程（POMDP）**，并通过VISTA-Gym交互环境实现闭环训练。在这一框架下，模型不再被动接受工具输出，而是在标准化的Gymnasium式API（`reset()` / `step()`）中主动选择、调用工具，并根据执行结果动态调整后续推理。这一范式转变使工具从“干扰项”变为“推理的有机延伸”。

### 2. 关键方法槽位变更

| 方法槽位 | 基线做法 | VISTA-R1 做法 | 创新本质 |
|:---|:---|:---|:---|
| **训练范式** | 静态视觉嵌入下的纯文本推理（无工具或粗糙工具暴露） | 两阶段训练：模仿学习（BC）预热 → 多轮在线强化学习（GRPO）在交互环境中训练 | 将VLM训练从“静态输入-输出映射”升级为“交互式序列决策优化” |
| **工具使用方式** | 直接暴露工具但不提供推理指导，或仅使用单一工具 | 模型在标准化API下动态选择26种工具，在思维链指导下交错进行工具调用与推理 | 从“工具作为外部插件”变为“工具作为推理循环的内生组件” |
| **奖励设计** | 仅基于最终答案正确性 | 稀疏、格式感知的组合奖励：重复惩罚 + 格式奖励 + 正确性奖励 | 从“结果导向”变为“过程-结果双重约束”，强制模型内化“思考→工具调用→答案”协议 |

### 3. 两阶段训练：BC预热 + GRPO在线强化学习

VISTA-R1的训练分为两个互补阶段，分别解决工具使用的不同瓶颈：

**阶段一：模仿学习预热（Behavioral Cloning）**。首先使用GPT-5生成工具执行轨迹，仅保留最终答案与真值完全匹配的正确轨迹；随后用Qwen3-VL-235B-A22B-Thinking将简洁的理由替换为扩展的思维链，形成高质量的“思考-行动”交错序列。BC阶段最大化这些专家轨迹的似然：

$$\mathcal{L}_{\mathrm{BC}}(\theta) = \mathbb{E}_{(x,\tau)\sim\mathcal{D}}\left[\sum_{t=0}^{T-1}\log \pi_{\theta}(a_t|x,c_{t-1},g_t) + \sum_{t=0}^{T}\log \pi_{\theta}(g_t|x,c_{t-1})\right]$$

这一阶段使模型掌握工具调用的格式与语法，为后续RL提供稳定的策略初始化。消融实验表明，SFT预热单独带来**+3.46%**的提升（Figure 4a）。

**阶段二：GRPO在线强化学习**。BC预热后，模型在VISTA-Gym环境中进行多轮在线RL训练。采用GRPO（Group Relative Policy Optimization）算法，其核心优势在于保留所有rollout并使用群组归一化优势进行低方差信用分配：

$$\widehat{A}_{i,k} = \frac{R(\tau_i) - \operatorname{mean}(\{R(\tau_1),\cdots,R(\tau_G)\})}{\operatorname{std}(\{R(\tau_1),\cdots,R(\tau_G)\})}$$

$$\mathcal{L}_{\mathrm{GRPO}}(\boldsymbol{\theta}) = \frac{1}{G}\sum_{i=1}^{G}\frac{1}{|\tau_i|}\sum_{k=1}^{|\tau_i|}\min[r_{i,k}(\boldsymbol{\theta})\cdot\widehat{A}_{i,k}, \cdots]$$

其中重要性比率 $r_{i,k}(\theta) = \frac{\pi_{\theta}(\tau_{i,k}|\tau_{i,<k})}{\pi_{\mathrm{old}}(\tau_{i,k}|\tau_{i,<k})}$ 在token级别控制策略更新幅度。RL阶段在SFT基础上再贡献**+10.19%**的提升（Figure 4a），表明基础模型并不具备鲁棒的工具集成推理能力，RL是解锁这一能力的关键。

### 4. 稀疏格式感知奖励：强制“思考→工具→答案”协议

VISTA-R1的奖励设计是其训练成功的重要创新。与仅依赖最终答案正确性的传统做法不同，该工作设计了稀疏、格式感知的组合奖励：

$$R(U) = R_{\mathrm{rep}}(U) + R_{\mathrm{format}}(U) + R_{\mathrm{correct}}(U)$$

其中 $R_{\mathrm{correct}}(U) = \mathbb{I}\{\widehat{y} = y\}$ 仅在输出无重复且格式正确时才给予正奖励。这一设计的核心洞察是：**仅在结构有效且无重复的生成中分配正向正确性信号，可以有效抑制模型通过重复或格式错误来“投机取巧”**，从而强制模型内化“思考→工具调用→答案”的规范协议。

### 5. 推理与工具的协同增益：1+1>2

VISTA-R1最具说服力的创新证据来自消融实验：**同时启用推理与工具使用（完整VISTA-R1）准确率达71.14%，远高于仅推理（63.66%）或仅工具先验（48.40%）的变体**（Table 2, Section 6.3）。这表明推理与工具之间存在显著的**协同效应**——推理指导工具的正确选择与使用，工具执行结果反过来为推理提供精确的感知信息，二者相互增强，形成正向循环。单纯的工具暴露（48.40%）甚至低于基础模型，进一步验证了“无推理指导的工具是干扰项”这一核心发现。

### 6. 可扩展的交互式训练设施

VISTA-Gym本身也是一项工程创新。它基于Ray构建高并发微服务架构，将计算密集型的VLM工具封装为HTTP服务，支持异步训练与多线程采样。该环境统一了7大类推理任务（覆盖13个公开数据集）和26种视觉工具（分为感知、图表理解、图表形式化、数学求解器四大家族），为工具集成推理的规模化训练提供了标准化基础设施。多任务与多工具训练的消融实验表明，这种多样性设计有效缓解了过拟合，提升了跨任务泛化能力（Figure 4d,e）。



VISTA-R1 的整体 pipeline 围绕一个核心洞察展开：将视觉-语言模型的工具集成推理（Tool-Integrated Reasoning, TIR）建模为部分可观测马尔可夫决策过程（POMDP），并通过一个标准化、可执行的交互环境——**VISTA-Gym**——对模型进行两阶段训练，使其内化“思考→工具调用→答案”的推理协议。

### 问题建模：工具集成推理即 POMDP

论文将 VLM 在工具辅助下的推理过程形式化为一个多轮交互轨迹 $\tau$。给定输入 $x$（图像与问题），模型 $\pi_\theta$ 生成一个交错着思考（$g_t$）、工具调用动作（$a_t$）与工具返回观察（$o_t$）的序列，最终输出预测答案 $\hat{y}$：

$$\tau = (g_0, a_0, o_0, \cdots, o_{T-1}, g_T, \hat{y}) \sim \pi_\theta(\tau|x)$$

该轨迹的概率可分解为思考生成与动作生成的乘积：

$$\pi_\theta(\tau|x) = \pi_\theta(g_T|x, c_{T-1}) \cdot \prod_{t=0}^{T-1} \pi_\theta(a_t|x, c_{t-1}, g_t) \cdot \pi_\theta(g_t|x, c_{t-1})$$

其中 $c_{t-1}$ 表示截至 $t-1$ 步的历史上下文。这一形式化将工具选择、调用与推理的协调统一在同一个序列决策框架下，为后续的模仿学习与强化学习提供了统一的优化目标。

### 系统架构：VISTA-Gym 交互环境

VISTA-Gym 是整个训练与评估的基础设施，其架构如 **Figure 2** 所示，由三个核心模块构成：

![[assets/figures/papers/paper_list_l2723_https_arxiv_org_abs_2511_19773/figures/003_Figure_2.jpg]]
*Figure 2: Overview of VISTA-Gym. VISTA-Gym contains a comprehensive suite of reasoning-intensive VQA tasks and tools in an interactive execution environment, scaling visual-centric tool-integrated agentic training for VLM agents*

1. **多模态推理任务套件**：覆盖 7 大类视觉推理任务，来自 13 个公开数据集（包括图表理解、几何推理、地理空间分析、科学问答、文档理解等），提供统一的训练与评估基准。
2. **标准化工具接口**：抽象出 26 个视觉工具，分为感知、图表理解、图表形式化、数学求解器四大家族。模型通过统一的 API 动态选择并调用工具，工具执行后返回结构化观察。
3. **可执行交互循环**：遵循 Gymnasium 风格的 `reset()` / `step()` API。每个 episode 是一个 POMDP 实例：环境接收模型的工具调用动作，执行对应工具并返回观察，形成多轮交互。动作空间严格受可用工具集的约束。

### 两阶段训练流程

VISTA-R1 的训练分为两个阶段，形成“预热→强化”的递进范式：

- **阶段一：行为克隆（BC）预热**。使用 GPT-5 生成工具执行轨迹，仅保留最终答案与真值完全匹配的样本；随后用 **Qwen3-VL-235B-A22B-Thinking** 将简洁推理替换为扩展的思考链，形成稠密的专家轨迹数据集 $\mathcal{D}$。BC 阶段最大化交错 thought–action 序列的似然：

  $$\mathcal{L}_{\mathrm{BC}}(\theta) = \mathbb{E}_{(x,\tau)\sim\mathcal{D}}\left[\sum_{t=0}^{T-1}\log \pi_\theta(a_t|x,c_{t-1},g_t) + \sum_{t=0}^{T}\log \pi_\theta(g_t|x,c_{t-1})\right]$$

  此阶段使模型掌握工具调用的格式、语法与基本模式，为后续 RL 探索提供稳定的策略初始化。

- **阶段二：在线强化学习（GRPO）**。在 VISTA-Gym 环境中进行多轮在线 RL 训练。每个输入 $x$ 采样 $G$ 条 rollout 轨迹，使用群组相对策略优化（GRPO）进行策略更新。其核心损失函数为：

  $$\mathcal{L}_{\mathrm{GRPO}}(\boldsymbol{\theta}) = \frac{1}{G}\sum_{i=1}^{G}\frac{1}{|\tau_i|}\sum_{k=1}^{|\tau_i|}\min\left[r_{i,k}(\boldsymbol{\theta})\cdot\widehat{A}_{i,k},\; \text{clip}(r_{i,k}(\boldsymbol{\theta}), 1-\epsilon, 1+\epsilon)\cdot\widehat{A}_{i,k}\right]$$

  其中重要性比率 $r_{i,k}(\theta) = \frac{\pi_\theta(\tau_{i,k}|\tau_{i,<k})}{\pi_{\mathrm{old}}(\tau_{i,k}|\tau_{i,<k})}$ 为 token 级别的新旧策略概率比，优势函数 $\widehat{A}_{i,k}$ 采用群组归一化：

  $$\widehat{A}_{i,k} = \frac{R(\tau_i) - \operatorname{mean}(\{R(\tau_1),\cdots,R(\tau_G)\})}{\operatorname{std}(\{R(\tau_1),\cdots,R(\tau_G)\})}$$

  这种群组归一化的优势估计降低了方差，使信用分配对任务难度具有自适应性。

### 奖励设计：稀疏格式感知的组合奖励

RL 阶段的奖励信号是推动模型内化“思考→工具调用→答案”协议的关键。每个 rollout 的最终奖励为三项之和：

$$R(U) = R_{\mathrm{rep}}(U) + R_{\mathrm{format}}(U) + R_{\mathrm{correct}}(U)$$

- **重复惩罚** $R_{\mathrm{rep}}(U)$：抑制模型生成重复文本。
- **格式奖励** $R_{\mathrm{format}}(U)$：检查输出是否符合预定义的结构化格式（包含思考标签、工具调用语法、答案标签等）。
- **正确性奖励** $R_{\mathrm{correct}}(U) = \mathbb{I}\{\hat{y} = y\}$：仅当预测答案与真值完全匹配时给予正向奖励。

这一稀疏、格式感知的奖励设计确保正向奖励仅分配给无重复、结构有效且答案正确的生成结果，从而引导模型在探索中自发形成合理的推理-工具协调策略。

### 可扩展训练设施

为支撑大规模在线 RL 训练，VISTA-Gym 基于 **Ray** 构建了高并发微服务架构，将计算密集型的 VLM 工具封装为 HTTP 服务，支持异步训练与多线程并行采样。这一设施使得在 8 块 H200 GPU 上即可完成完整的 BC+RL 训练流程，同时兼容多种 VLM 骨干（如 InternVL3、Qwen2.5-VL 等）。

### 输入输出流总结

整个 pipeline 的端到端数据流可概括为：输入图像与问题 → VLM 骨干生成思考 → 动态选择并调用工具（通过 VISTA-Gym 标准化接口） → 环境执行工具并返回观察 → 模型基于观察继续推理 → 循环直至生成最终答案。训练信号来自 RL 阶段的稀疏组合奖励，驱动模型在交互中习得何时调用何种工具、如何解读工具返回、以及如何将工具结果融入推理链的能力。



### 1. 问题形式化：将工具集成推理建模为 POMDP

VISTA-R1 将视觉-语言模型（VLM）的工具集成推理（Tool-Integrated Reasoning, TIR）过程建模为一个部分可观测马尔可夫决策过程（POMDP）。给定输入 $x$，模型策略 $\pi_\theta$ 生成一条由思考（thoughts）、动作（actions）和观察（observations）交错构成的轨迹 $\tau$：

$$\tau = (g_0, a_0, o_0, \cdots, o_{T-1}, g_T, \hat{y}) \sim \pi_\theta(\tau | x)$$

其中，$g_t$ 表示第 $t$ 步的思考（最终步 $g_T$ 产出答案 $\hat{y}$），$a_t$ 为工具调用动作，$o_t$ 为环境返回的观察。该轨迹的概率可分解为思考生成与动作选择的乘积：

$$\pi_{\theta}(\tau | x) = \pi_{\theta}(g_T | x, c_{T-1}) \cdot \prod_{t=0}^{T-1} \pi_{\theta}(a_t | x, c_{t-1}, g_t) \cdot \pi_{\theta}(g_t | x, c_{t-1})$$

这里 $c_{t-1}$ 表示截至 $t-1$ 步的上下文。这一形式化为后续的模仿学习与强化学习提供了统一的概率框架。

### 2. 训练框架：两阶段训练器

VISTA-R1 采用两阶段训练策略，逐步引导模型内化“思考→工具调用→答案”的交互协议。

**第一阶段：行为克隆预热（Behavioral Cloning, BC）**  
利用经过过滤和稠密化的专家轨迹数据集 $\mathcal{D}$，最大化交错思考-动作序列的似然。BC 目标函数为：

$$\mathcal{L}_{\mathrm{BC}}(\theta) = \mathbb{E}_{(x,\tau)\sim\mathcal{D}}[\log \pi_{\theta}(\tau|x)] = \mathbb{E}\left[\sum_{t=0}^{T-1}\log \pi_{\theta}(a_t|x,c_{t-1},g_t) + \sum_{t=0}^{T}\log \pi_{\theta}(g_t|x,c_{t-1})\right]$$

专家轨迹由 GPT-5 生成，仅保留最终答案与真值完全匹配的轨迹，并由 Qwen3-VL-235B-A22B-Thinking 将简略推理替换为扩展思维链，以提供更丰富的学习信号。此阶段使模型掌握工具调用的格式、语法与基本协调能力。

**第二阶段：在线强化学习（Online RL）**  
在 BC 预热基础上，采用群组相对策略优化（Group Relative Policy Optimization, GRPO）进行多轮在线 RL 训练。GRPO 损失函数为：

$$\mathcal{L}_{\mathrm{GRPO}}(\boldsymbol{\theta}) = \frac{1}{G}\sum_{i=1}^{G}\frac{1}{|\tau_i|}\sum_{k=1}^{|\tau_i|}\min\left[r_{i,k}(\boldsymbol{\theta})\cdot\widehat{A}_{i,k}, \ \text{clip}(r_{i,k}(\boldsymbol{\theta}), 1-\epsilon, 1+\epsilon)\cdot\widehat{A}_{i,k}\right]$$

其中，$G$ 为每轮的 rollout 数量，$|\tau_i|$ 为第 $i$ 条轨迹的 token 长度。重要性采样比率 $r_{i,k}$ 定义为新旧策略在 token 级别的概率比：

$$r_{i,k}(\theta) = \frac{\pi_{\theta}(\tau_{i,k} | \tau_{i,<k})}{\pi_{\mathrm{old}}(\tau_{i,k} | \tau_{i,<k})}$$

优势估计 $\widehat{A}_{i,k}$ 采用群组归一化，以降低方差并实现难度自适应的信用分配：

$$\widehat{A}_{i,k} = \frac{R(\tau_i) - \operatorname{mean}(\{R(\tau_1),\cdots,R(\tau_G)\})}{\operatorname{std}(\{R(\tau_1),\cdots,R(\tau_G)\})}$$

GRPO 保留所有 rollout 并使用群组归一化优势，相比 PPO 和 DAPO 表现出更鲁棒的性能（见 Figure 4b）。

### 3. 奖励设计：稀疏、格式感知的组合奖励

为引导模型遵循“思考→工具调用→答案”的结构化协议，VISTA-R1 设计了稀疏且格式感知的组合奖励函数。单条 rollout $U$ 的最终奖励为三项之和：

$$R(U) = R_{\mathrm{rep}}(U) + R_{\mathrm{format}}(U) + R_{\mathrm{correct}}(U)$$

- **重复惩罚 $R_{\mathrm{rep}}(U)$**：抑制模型生成重复或无意义的文本片段。
- **格式奖励 $R_{\mathrm{format}}(U)$**：检查输出是否符合预定义的结构化模板（包含思考块、工具调用块和最终答案块）。
- **正确性奖励 $R_{\mathrm{correct}}(U)$**：仅当输出无重复且格式正确时，才评估最终答案是否正确：

$$R_{\mathrm{correct}}(U) = \mathbb{I}\{\widehat{y} = y\}$$

此设计确保正向奖励仅授予那些结构有效且答案正确的生成，从而引导模型内化完整的交互协议，而非仅追求最终答案的偶然正确。

### 4. 交互环境：可执行工具接口

VISTA-Gym 提供标准化的 Gymnasium 风格 API（`reset()` / `step()`），将 26 种视觉工具抽象为四大家族（感知、图表理解、图表形式化、数学求解器），并严格约束动作空间为可用工具集。环境执行工具调用并返回观察，形成多轮交互循环，为上述训练框架提供可验证的反馈信号。

### 补充图表

![[assets/figures/papers/paper_list_l2723_https_arxiv_org_abs_2511_19773/figures/001_Figure_1.jpg]]
*Figure 1: Directly augmenting VLMs with tools significantly degrades accuracy (w/ T), yet intrinsic reasoning offers limited gains on complex VQA (w/ R). Supplying tool-selection prior knowledge and interleaving reasoning with tool execution improve performance (w/ T&R); gains are task-dependent for commercial VLMs, while small open-source VLMs remain particularly struggling*

![[assets/figures/papers/paper_list_l2723_https_arxiv_org_abs_2511_19773/figures/004_Figure_3.jpg]]
*Figure 3: Top tool call distribution of different tasks in SFT data*



## 实验与关键发现

### 核心瓶颈与因果验证

实验围绕一个核心瓶颈展开：**现有视觉-语言模型（VLM）在未经过专门训练时，工具调用本身会严重损害推理准确性**。Figure 1 揭示了这一现象——直接向 VLM 暴露工具（w/ T）导致准确率显著下降，而即使开启内在推理（w/ R）对复杂视觉问答的增益也有限。Table 1 对 500 个错误样本的归因分析进一步量化了失败模式：开源模型 InternVL3-8B 的主要错误集中在**工具调用模式错误（E2，44.8%）**、**工具执行后推理错误（E6，64.8%）**和**工具参数选择错误（E4，57.4%）**，而商业模型 GPT-5 的错误更多分布在**工具调用必要性判断错误（E1，12.8%）**和**工具执行后推理错误（E6，28.1%）**。这表明，无论模型规模大小，**“何时调用工具、调用哪个工具、如何传参、如何整合工具返回结果”** 是现有 VLM 的共性短板，工具反而成为干扰项。

![[assets/figures/papers/paper_list_l2723_https_arxiv_org_abs_2511_19773/figures/002_Table_1.jpg]]
*Table 1: Error pattern identification and distribution from 500 error samples. Note that one case may contain multiple error types*

VISTA-R1 通过两阶段训练（模仿学习预热 + 在线 GRPO 强化学习）直接作用于这一因果链条。消融实验（Table 2）给出了决定性证据：完整方法（推理 + 工具 + RL）在 11 个数据集上平均准确率达 **71.14%**，而剥离工具（仅推理）降至 **63.66%**，剥离推理（仅工具先验）骤降至 **48.40%**。这组对比说明，**推理与工具使用之间存在强协同效应，单独启用任何一方都无法替代另一方的贡献**。

![[assets/figures/papers/paper_list_l2723_https_arxiv_org_abs_2511_19773/figures/005_Table_2.jpg]]
*Table 2: Main results (acc%) on five in-distribution and six out-of-distribution VQA benchmarks. † indicates results reported from the original papers. w/o Tools excludes tool access from both training and inference stage; w/o Reasoning removes RL training stage*

### 主实验结果

Table 2 展示了 VISTA-R1 在 5 个分布内和 6 个分布外视觉推理基准上的全面表现。以 InternVL3-8B 为骨干的 VISTA-R1-8B 相比同规模基线取得了一致且显著的提升：

- **分布内任务**：ChartQA 上达到 **91.92%**（InternVL3-8B 基线 77.32%，提升 +14.60），Geometry3K 上达到 **61.27%**（基线 47.09%，提升 +14.18），MapQA 上达到 **68.45%**（基线 34.70%，提升 +33.75）。MapQA 的巨幅提升尤为突出，说明地理空间推理对工具（如地图解析、坐标定位）的依赖度极高，而 VISTA-R1 成功习得了这一能力。
- **分布外任务**：VISTA-R1-8B 在 6 个分布外基准上的表现已**与更大规模的商业模型可比**，例如在多个任务上接近或超越 GPT-o3 和 Claude-4.5-Sonnet。即使完全移除工具（w/o Tools），VISTA-R1-8B 仍比基线高出 2.03%–11.24%，说明 RL 训练不仅教会了模型“使用工具”，还强化了其内在推理能力。

跨骨干泛化性同样得到验证：使用 Qwen2.5-VL-7B 骨干时，ChartQA 达到 90.08%；使用 InternVL3-2B 时达到 88.55%，表明 VISTA-Gym 训练框架不依赖于特定模型架构。

### 训练阶段与算法消融

两阶段训练的贡献在 Figure 4a 中量化：**SFT 预热带来 +3.46% 的提升，而后续 RL 在 SFT 基础上再贡献 +10.19%**。这一结果与 Table 3 形成呼应——Table 3 显示，在未经过 RL 训练时，直接暴露工具（w/ Tools）反而导致准确率下降，而仅提供工具选择先验并交错推理（w/ T&R）虽有改善但仍有限。这说明 **RL 是将工具从“干扰源”转化为“能力放大器”的关键环节**，仅靠监督微调无法使模型内化动态工具协调策略。

![[assets/figures/papers/paper_list_l2723_https_arxiv_org_abs_2511_19773/figures/007_Table_3.jpg]]
*Table 3: Effect of reasoning and tool-use results without RL training. w/ Tools refers to directly augmenting VLMs with tools significantly degrades accuracy; w/ Reasoning refers to CoT reasoning without tools. w/ T&R refers to a different setting compared to TIR, only supplying tool-selection prior knowledge and interleaving reasoning with tool execution improve performance*

RL 算法选择方面，Figure 4b 比较了 GRPO、PPO 和 DAPO 三种算法。GRPO 表现最鲁棒，其优势源于**保留所有 rollout 并使用群组归一化优势进行低方差信用分配**，使训练对难度波动具有自适应性。相比之下，PPO 和 DAPO 在部分任务上出现性能震荡。

### 奖励设计与数据多样性

奖励函数的稀疏、格式感知设计是训练成功的重要支撑。最终奖励 $R(U) = R_{\mathrm{rep}}(U) + R_{\mathrm{format}}(U) + R_{\mathrm{correct}}(U)$ 将正向奖励仅分配给**无重复、结构有效且答案正确**的生成结果，强制模型遵循“思考→工具调用→答案”的协议。Figure 4 的消融表明，移除任意一个奖励组件都会导致性能下降，验证了组合奖励的必要性。

![[assets/figures/papers/paper_list_l2723_https_arxiv_org_abs_2511_19773/figures/006_Figure_4.jpg]]
*Figure 4: Ablation studies and diversity analysis with InternVL3-8B as backbone VLM*

多任务与多工具训练对泛化能力的影响在 Figure 4d 和 4e 中得到验证。**多任务训练相比单任务训练显著缓解了过拟合**，而工具多样性训练使模型在面对新工具组合时表现更稳定。Table 5 提供了 VISTA-Gym 中 13 个数据集的统计概况，覆盖图表理解、几何推理、地理空间、科学问答、文档理解等 7 大类任务。

![[assets/figures/papers/paper_list_l2723_https_arxiv_org_abs_2511_19773/figures/012_Table_5.jpg]]
*Table 5: Dataset statistics in VISTA-Gym*

### 失败模式修复与课程学习

Figure 6（原文 Section 6.4）对工具调用错误的追踪显示，经过 VISTA-Gym 训练后，**绝大多数工具调用失败和工具执行后推理错误得到解决**。这直接回应了 Table 1 中识别的瓶颈——E2（工具调用模式错误）和 E6（工具执行后推理错误）在训练后大幅减少。

尾部补丁课程学习（tail-patch curriculum）的策略效果在 Figure 7 中展示：**将性能从 69.54% 推至 71.27%**。该方法聚焦于“困难但可学习”的样本（即模型当前成功率低但并非完全不可解的尾部样本），避免了在已掌握样本上的无效训练和在完全无法解决样本上的浪费。

![[assets/figures/papers/paper_list_l2723_https_arxiv_org_abs_2511_19773/figures/009_Figure_7.jpg]]
*Figure 7: Training scaling from easy to hard*

### 轨迹质量与案例研究

Figure 5 揭示了专家思维轨迹质量与长度的关系：**过短或过长的轨迹质量均较低，存在一个最优长度区间**，说明有效的工具集成推理需要适度的思考深度而非简单堆砌 token。Figure 8 的人类评估研究进一步证实，经过 RL 训练后的轨迹在连贯性、工具调用合理性和推理逻辑上均显著优于仅 SFT 的轨迹。

![[assets/figures/papers/paper_list_l2723_https_arxiv_org_abs_2511_19773/figures/008_Figure_5.jpg]]
*Figure 5: Quality of expert thinking trajectories by length*

![[assets/figures/papers/paper_list_l2723_https_arxiv_org_abs_2511_19773/figures/010_Figure_8.jpg]]
*Figure 8: Human study on trajectory quality*

Table 4 提供了几何推理任务的案例研究，展示了 VISTA-R1-8B 在实际推理过程中的工具使用模式：模型能够自主选择适当的几何解析工具，将视觉输入转化为结构化表示，在此基础上进行逻辑推导并得出正确答案。这些案例直观体现了“感知→解析→推理”的闭环能力。

![[assets/figures/papers/paper_list_l2723_https_arxiv_org_abs_2511_19773/figures/011_Table_4.jpg]]
*Table 4: Case studies on geometric reasoning tasks with VISTA-R1-8B trained in VISTA-Gym*

### 实验公平性与局限说明

本文未专门讨论模型公平性或偏见问题，实验主要聚焦于推理准确率的提升。训练计算开销较大，需 8 块 H200 GPU，且在适配不同骨干模型（如 InternVL3）时需要定制化处理视觉编码器与工具接口的对接。当前 Verifier 主要依赖终端正确性和结构有效性，缺乏对中间步骤语义的细粒度奖励，这可能限制了更复杂的长期工具集成推理策略的探索空间。



## 定位与知识库关联

### 与基线的关系

VISTA-R1 在视觉-语言模型（VLM）的**工具集成推理**（Tool-Integrated Reasoning, TIR）这一新兴方向上，与多条基线形成对比与超越。

**1. 商用 API 模型：工具暴露反而有害。**
GPT-5、GPT-o3、Claude-4.5-Sonnet 等商用 VLM 在直接暴露工具（w/ T）时，准确率反而显著下降（Figure 1）。即使提供工具选择先验并交错推理（w/ T&R），增益也因任务而异，且小型开源模型在该设定下仍严重挣扎。VISTA-R1-8B 在 11 个视觉推理基准上的整体均分（71.14%）已可比肩 GPT-o3 和 Claude-4.5-Sonnet 等更大规模的商用模型（Table 2），证明**规模化智能体强化学习可弥补参数差距**。

**2. 开源 VLM 骨干：工具使用能力近乎为零。**
InternVL3、Qwen2.5-VL、LLaVA-OneVision-1.5 等骨干模型在未经专门训练时，工具调用错误率极高——错误模式分析显示，InternVL3-8B 在“工具调用时机/方式”（E2）上错误率达 44.8%，“后工具推理错误”（E6）达 64.8%（Table 1）。VISTA-R1 在 InternVL3-8B 上取得 71.14% 的均分，较其原始骨干（57.49%）提升 **+13.65%**（Table 2），在 MapQA 上甚至实现 **+33.75%** 的飞跃。

**3. 同方向的开源 TIR 基线：VISTA-R1 显著领先。**
VTool-R1、R1-VL、R1-Onevision、Perception-R1 等近期工作同样探索 VLM 的推理与工具结合，但 VISTA-R1-8B 在可比较规模下超出这些基线 **9.51%–18.72%**（使用工具），即使不使用工具也超出 **2.03%–11.24%**（Table 2）。核心差异在于：VISTA-Gym 提供了统一的交互环境与可验证反馈，使 GRPO 强化学习能够端到端地内化“思考→工具调用→答案”协议，而非仅依赖静态的监督微调。

### 适用边界

VISTA-Gym 与 VISTA-R1 的适用边界由以下几个维度界定：

- **任务域**：覆盖 7 大类视觉推理任务（图表理解、几何推理、地理空间、科学、文档、自然图像、数学），涉及 13 个公开数据集。在分布外（OOD）基准上，VISTA-R1 仍保持竞争力，表明**跨任务泛化能力**较强，但未测试完全脱离视觉推理的场景（如纯文本推理或 embodied AI）。
- **工具生态**：当前标准化接口封装了 26 种视觉工具，分属感知、图表理解、图表形式化、数学求解器四大家族。对于需要更细粒度操作（如像素级编辑、视频流处理）或工具数量远超当前规模的场景，适用性未经验证。
- **模型规模**：主要实验在 2B–8B 参数规模的开源 VLM 上完成。更大规模模型（如 70B+）的训练开销与收益曲线尚未探索。
- **训练资源**：RL 阶段需 8 块 H200 GPU，且对 InternVL3 等特定架构需定制化处理。资源受限场景下，仅 SFT 预热可提供 +3.46% 的提升，但无法解锁 RL 带来的 +10.19% 额外增益（Figure 4a）。

### 局限与开放问题

**已识别的局限：**

1. **奖励稀疏性**：当前 Verifier 仅依赖终端正确性（答案匹配）和结构有效性（格式校验），缺乏对中间步骤语义的细粒度奖励。这限制了模型在长周期、多步工具编排任务中的探索效率与策略优化空间。
2. **工具生态广度**：26 种工具虽已覆盖主要视觉推理需求，但距离通用视觉智能体所需的工具谱系仍有差距，例如缺少 3D 场景理解、视频时序推理、交互式标注等工具类别。
3. **计算开销**：在线 RL 训练需要 8×H200 GPU 的高并发微服务架构（Ray），且异步训练与多线程采样的工程复杂度较高，限制了在更广泛研究团体中的可复现性。
4. **架构适配成本**：不同 VLM 骨干（如 InternVL3 与 Qwen2.5-VL）在工具调用格式、视觉嵌入接口等方面存在差异，迁移训练需要定制化适配。

**待探索的开放问题：**

1. **更丰富的逐步奖励**：引入过程监督（process reward model）或中间步骤验证器，能否进一步促进长周期工具集成推理的策略学习？
2. **更大规模与更广动作空间**：将 VISTA-Gym 范式扩展到 70B+ 参数 VLM 或更丰富的工具动作空间时，GRPO 的群组归一化优势是否仍能保持低方差特性？
3. **无完美专家轨迹的 RL 探索**：当前 BC 预热依赖 GPT-5 生成并过滤的专家轨迹。若移除这一依赖，RL 能否自主探索出更优甚至超越人类先验的工具使用策略？
4. **跨模态扩展**：VISTA-Gym 的 POMDP 建模与可执行交互循环设计，能否迁移到视频理解、具身智能等多模态时序决策场景？



## 原文 PDF

![[paperPDFs/CVPR_2026/Scaling_Agentic_Reinforcement_Learning_for_Tool_Integrated_Reasoning_in_VLMs.pdf]]
