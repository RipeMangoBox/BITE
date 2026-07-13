---
title: "Speech World Model: Causal State–Action Planning with Explicit Reasoning for Speech"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Speech_World_Model_Causal_StateAction_Planning_with_Explicit_Reasoning_for_Speech.pdf
project_link: http://bit.ly/4pBJuWP
code_link: null
openreview_forum_id: YGUKPGO182
aliases:
- SWMS
- SWMCSAPERS
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "基于认知科学引入模块化因果图，将语音理解分解为WMA、ToM、SA、Prag四个模块并显式建模因果关系，形成结构化认知状态搜索空间。"
primary_logic: "通过因果图提供显式状态表示和推理链引导，可以降低状态搜索熵，使模型在部分标注下推断缺失状态，并在指令微调中大幅提升情绪识别等推理能力，实现小模型低训练成本下接近或超越商业大模型的性能。"
claims:
- "因果图在完全监督和半监督下均维持稳定的ACE和ICS，而随机图因果效应评分低且不稳定"
- "移除因果边（如ToM→SA）显著降低SA模块准确率，证明因果结构有效性"
- "半监督训练中，无标签模块通过因果子节点梯度传播可被学习，并推断出未标注状态"
- "在指令微调中，结合因果图状态引导的SWM模型在Model-as-Judge评分和情绪识别准确率上显著优于传统SLM和CoT基线"
---

# Speech World Model: Causal State–Action Planning with Explicit Reasoning for Speech

> [!tip] 核心洞察
> 通过因果图提供显式状态表示和推理链引导，可以降低状态搜索熵，使模型在部分标注下推断缺失状态，并在指令微调中大幅提升情绪识别等推理能力，实现小模型低训练成本下接近或超越商业大模型的性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 语音世界模型：面向语音的因果状态-动作规划与显式推理 |
| 英文题名 | Speech World Model: Causal State–Action Planning with Explicit Reasoning for Speech |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=YGUKPGO182) · [Project](http://bit.ly/4pBJuWP) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Speech World Model (SWM) |
| Dataset | Model-as-Judge (M.J.) 多维语音理解评价, 推理中的情绪分类准确率, Model-as-Judge (M.J.) 综合评分, 边缘因果效应评估 |

> [!tip] 效果简介
> - Model-as-Judge (M.J.) 多维语音理解评价 上，Overall M.J. Score (0.6*Reasoning + 0.4*Response) 为 7.59 (SWM Qwen2-Audio CoT)，对比 5.18 (Qwen2-Audio-CoT)，变化 +2.41。
> - 推理中的情绪分类准确率 上，EA (%) 为 71.02 (SWM Qwen2-Audio)，对比 34.72 (Qwen2-Audio-CoT)，变化 +36.30。
> - Model-as-Judge (M.J.) 综合评分 上，Overall M.J. Score 为 7.81 (SWM Llama3.1-8b)，对比 8.12 (Gemini 2.5 Pro)，变化 -0.31 (远低于商用模型训练成本)。

## 概要

当前语音语言模型（Speech Language Models, SLMs）将语音理解视为单一黑盒，仅聚合孤立任务输出，忽略了语音成分间内在的因果依赖关系。这一设计导致推理能力薄弱、监督信号稀疏，且易产生幻觉。**SWM (Speech World Model)** 针对该瓶颈，受认知科学启发，引入模块化因果图，将语音理解显式分解为**世界模型激活 (WMA)**、**心理理论 (ToM)**、**言语行为 (SA)** 和**语用意图 (Prag)** 四个模块，并建模其间的因果关系，形成结构化的认知状态搜索空间。

核心思路是：因果图提供显式状态表示和推理链引导，降低状态搜索熵，使模型能在部分标注下推断缺失状态，并在指令微调中大幅提升推理能力。实验表明：

- **推理综合评分**：SWM (Qwen2-Audio CoT) 的 Model-as-Judge 综合得分为 7.59，远超传统 CoT 基线 Qwen2-Audio-CoT 的 5.18（Table 3）。
- **情绪识别**：SWM 的情绪分类准确率达 71.02%，而 Qwen2-Audio-CoT 仅 34.72%，提升超过 36 个百分点（Table 3）。
- **训练效率**：因果图训练收敛速度约为随机图的 5 倍（2.07h vs 10.39h），且仅需约 20 GPU 小时即可在部分指标上接近甚至超越 GPT-4o 和 Gemini 2.5 Pro 等商业大模型。
- **因果有效性**：因果图在完全监督和半监督下均维持高平均因果效应（ACE 23.57 vs 随机图 1.0）；移除 ToM→SA 等关键因果边会显著降低模块准确率，验证了因果结构的必要性（Table 1, Table 5）。

SWM 的方法定位可概括为：将语音理解从“隐式端到端生成”转变为“因果图引导的显式状态–动作推理”，在低训练成本下实现强推理性能。当前局限包括因果图结构依赖人工先验、标注依赖 LLM 教师模型，以及多语种泛化性尚未验证。

语音语言模型（Speech Language Models, SLMs）近年来取得了显著进展，代表性工作包括 **Qwen-Audio**（Chu et al., 2023）、**Qwen2-Audio**（Chu et al., 2024）和 **Voxtral**（Liu et al., 2025）等。这些模型通常采用端到端架构，将语音信号直接映射为文本响应，在语音识别、意图分类等任务上展现了强大的能力。

然而，当前 SLM 范式存在一个根本性的瓶颈：**语音理解被建模为单一黑盒过程，仅聚合孤立的任务输出，而忽略了语音成分之间的内在因果依赖关系**。具体而言，一段语音的语义理解涉及多个认知层面的交互——说话者的世界知识激活（WMA）、对听者心理状态的推断（ToM）、言语行为的选择（SA）以及语用意图的传达（Prag）——这些模块之间存在明确的因果链条，而非简单的共现关系。现有模型将这一复杂过程压缩为隐式特征变换，导致三个关键问题：

1. **推理能力薄弱**：缺乏显式的中间推理状态，模型难以进行多步因果推断，在需要深层理解的场景（如讽刺识别、情绪推理）中表现不佳。
2. **监督信号稀疏**：端到端训练仅依赖最终响应作为监督信号，中间认知状态完全不可观测，导致学习效率低下。
3. **幻觉倾向**：黑盒模型在缺乏结构化先验的情况下，容易产生与语音内容不一致的推断。

从认知科学的角度审视，人类语音理解本质上是一个模块化因果推理过程。说话者首先激活对当前世界状态的心理表征（WMA），进而推断听者的知识、信念和情绪状态（ToM），在此基础上选择特定的言语行为（SA），最终传达语用意图（Prag）。这一因果链为语音理解提供了天然的认知脚手架。

本文的核心动机在于：**将这一认知脚手架显式地注入语音语言模型，通过结构化因果图替代隐式黑盒推理**。具体而言，我们提出 Speech World Model（SWM），将语音理解分解为 WMA、ToM、SA、Prag 四个模块，并通过有向无环图（DAG）显式建模它们之间的因果关系。这一设计将原本无约束的自回归生成搜索空间，压缩为一个受因果图约束的低熵认知状态子空间，使模型能够在部分标注下推断缺失状态，并在指令微调中大幅提升推理能力。

从世界模型的统一视角来看（Figure 3），生成式世界模型和语言世界模型均为前向动态模型，而 SWM 的因果图提供了一种结构化、显式的动态建模方式。这一视角将 SWM 置于世界模型研究的谱系中，同时凸显其独特贡献：以因果结构而非黑盒序列建模来捕捉语音理解中的状态转移。

## 核心方法与创新机理

### 创新动机：从黑盒聚合到因果推理

当前语音语言模型（SLM）将语音理解建模为单一黑盒任务，仅聚合孤立的分类输出（如情绪、意图、言语行为），忽略了这些成分之间固有的因果依赖关系。这种扁平化建模带来三个瓶颈：

1. **推理能力薄弱**：模型缺乏对“说话者为何产生特定情绪、进而选择特定言语行为”的因果链建模，导致深层语义推理困难。
2. **监督信号稀疏**：多维度语音标注成本极高，部分模块往往缺乏直接标签，传统方法无法有效利用未标注模块。
3. **幻觉倾向**：缺乏结构化认知约束，模型在生成推理链时容易偏离真实的因果逻辑。

SWM 的核心创新在于将认知科学中的模块化因果图引入语音理解，将黑盒任务显式分解为四个因果关联的认知模块，并以此构建结构化的状态搜索空间，从根本上改变了语音推理的中间表示和训练范式。

### 关键创新点（Changed Slots）

#### 1. 推理中间表示：从隐式推理到显式因果状态

**Baseline 做法**：现有 SLM（如 **Qwen-Audio** (Chu et al., 2023)、**Qwen2-Audio** (Chu et al., 2024)、**Voxtral** (Liu et al., 2025)）依赖 LLM 隐层状态或 CoT 提示进行隐式推理，推理过程不可解释且缺乏结构化约束。

**SWM 做法**：引入概率因果模型 $ \mathcal{G} = (\mathcal{V}, \mathcal{E}) $，将语音理解分解为四个具有明确因果关系的认知模块（Section 3.1, Figure 2）：

- **WMA（世界模型激活）**：识别语音中的实体、动作和场景
- **ToM（心理理论）**：推断说话者的情绪和认知状态
- **SA（言语行为）**：识别话语的交际功能（请求、陈述、质问等）
- **Prag（语用意图）**：理解话语的深层语用目的

每个模块的状态 $S_v$ 由其父节点状态和因果影响决定：
$$S_v = f_v\big(\{S_u : u \in \mathrm{Pa}(v)\}, A_{uv}\big)$$

联合后验按因果图结构逐级分解：
$$p(Z|X) = p(z_{WMA}|X) \cdot p(z_{ToM}|X) \cdot p(z_{SA}|z_{WMA}, z_{ToM}, X) \cdot p(z_{Prag}|z_{SA}, z_{ToM}, z_{WMA}, X)$$

**效果差异**：因果图在完全监督和半监督下均维持稳定的平均因果效应（ACE=23.57）和干预一致性分数（ICS），而随机图基线因果效应评分低且不稳定（ACE≈1, ICS≈1）（Table 1, Table 2, Fig. 5）。在指令微调中，因果状态引导使情绪识别准确率从 34.72% 提升至 71.02%（Table 3），验证了显式因果状态表示对推理能力的决定性作用。

#### 2. 训练流程：从单阶段微调到两阶段因果-指令训练

**Baseline 做法**：传统 SLM 采用单阶段指令微调，直接学习从语音到响应的映射。

**SWM 做法**：设计两阶段训练流程（Section 3, Section 4.4）：

- **阶段一：因果图多任务训练**。在监督或半监督条件下训练因果图，学习模块间的因果依赖关系。监督损失仅对有标签节点计算交叉熵：
  $$\mathcal{L}_{\mathrm{sup}} = \sum_{i=1}^N \sum_{v \in \mathcal{V}} m_{i,v} \mathrm{CE}(y_{i,v}, S_{i,v})$$
  半监督条件下，无标签父节点通过有标签子节点的链式梯度得到更新：
  $$\frac{\partial \mathcal{L}_i}{\partial \theta_j} = \sum_{k: m_{i,k}=1, j \in \mathrm{Pa}(k)} \frac{\partial \mathcal{L}_{i,k}}{\partial \eta_{i,k}} \frac{\partial \eta_{i,k}}{\partial S_{i,j}} \frac{\partial S_{i,j}}{\partial \eta_{i,j}} \frac{\partial \eta_{i,j}}{\partial \theta_j} \neq 0$$
  训练采用边级教师强制混合信号稳定优化：
  $$\tilde{S}_{i,u} = \tau_{i,u\to v} \mathrm{onehot}(y_{i,u}) + (1 - \tau_{i,u\to v}) \mathrm{stopgrad}(S_{i,u}), \tau \sim \mathrm{Bernoulli}(p_{u\to v})$$

- **阶段二：指令微调**。将因果图推断的状态序列化，作为显式引导输入语言模型：
  $$\mathcal{L}_{\mathrm{IT}}(\theta) = -\sum_{(x,y)\in\mathcal{D}} \log p_\theta(y | \mathrm{Instr}, x, S_{WMA}, S_{ToM}, S_{SA}, S_{Prag})$$

**效果差异**：因果图训练收敛速度约为随机图的 5 倍（2.07h vs 10.39h），体现了结构化因果先验的优化效率（Section 4.4）。半监督训练中，无标签模块（如 WMA）通过因果子节点梯度传播仍可被学习，推断准确率达 34.8%（Table 1 semi-supervised rows, Section 3.1.4）。消融实验表明，教师强制概率在 0.3–1.0 范围内模型性能稳定，因果结构对监督信号强度不敏感（Table 5）。

#### 3. 推理链搜索空间：从无约束生成到因果约束子空间

**Baseline 做法**：传统 CoT 或自回归生成在无约束的 token 空间中搜索推理链，容易产生幻觉或偏离真实因果逻辑。

**SWM 做法**：因果图将推理搜索空间压缩为受因果结构约束的低熵认知状态子空间（Section 3.2, Appendix A.3.2）。每个模块的状态空间由预定义的离散类别构成，模块间的因果边限制了可能的状态转移路径，使得推理过程沿着符合认知先验的因果链展开。

**效果差异**：移除关键因果边（如 ToM→SA）显著降低 SA 模块准确率（Table 5 edge removal ablation），验证了因果结构对推理路径的约束有效性。随机图基线由于缺乏结构约束，ACE 和 ICS 在不同教师强制比率下剧烈波动，无法学习稳定的因果依赖（Table 2）。SWM 结合因果状态引导在 Model-as-Judge 综合评分上达到 7.59（Qwen2-Audio CoT），显著优于无因果约束的 CoT 基线 5.18（Table 3），以远低于 **Gemini 2.5 Pro** (Gemini Team, 2025) 的训练成本（仅 20 GPU 小时）接近其性能（8.12）。

### 创新边界与局限

当前因果图结构基于认知先验预定义，包含四个固定模块，尚不能自适应学习或调整结构以适配新领域。数据标注依赖 Vicuna-13b 教师模型，可能引入标签噪声和错误传播。实证评估主要集中在英语对话与语音助手场景，多语种、多文化背景下的泛化性尚未验证。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_YGUKPGO182/figures/002_Figure_2.jpg]]
*Figure 2: The Speech World Model pipeline with a running example, illustrating the “Causal Graph-Guided Explicit Reasoning” process. (1) Causal Graph Training: multimodal inputs (text x, acoustic a, prosody z) are encoded and fused to g = $\phi ( h _ { x } , h _ { a } , h _ { z }$ ) . Each node state $S _ { v }$ is inferred from its parents Pa(v) and fused feature g via Sv = softmax ( $f _ { v }$ ( g , $\{ S _ { u } \} _ { u \in \mathrm { P a } ( v ) }$ ) ) , yielding structured reasoning. (2) Instruction Tuning: these states are used as explicit guidance for the large (speech) language models to generate response y by maximizing $\begin{array} { r } { \mathcal { L } _ { \mathrm { I T } } = - \sum \log P _ {...$

Speech World Model (SWM) 的完整流水线由两个阶段构成：**因果图训练** 与 **指令微调**，其核心设计目标是将语音理解从单一黑盒映射重构为可解释的因果状态-动作规划过程（Figure 2）。

### 第一阶段：因果图训练

该阶段将语音理解分解为四个显式认知模块，并通过有向无环图（DAG）建模其间的因果依赖关系：

- **WMA**（World Model Activation）：识别语音所描述的行动或事件状态；
- **ToM**（Theory of Mind）：推断说话者的情绪与心理状态；
- **SA**（Speech Act）：判定言语行为类型（如提问、请求、陈述）；
- **Prag**（Pragmatic Intent）：理解语用意图与对话目标。

输入信号包含三种模态：文本转录 $x$、声学特征 $a$、韵律特征 $z$。三者经各自编码器提取后，通过融合模块 $\phi$ 生成联合表示 $g = \phi(h_x, h_a, h_z)$。每个节点的状态 $S_v$ 由其父节点状态 $\{S_u : u \in \mathrm{Pa}(v)\}$ 与融合特征 $g$ 共同决定，通过分类器 $f_v$ 输出离散类别分布：

$$S_v = \mathrm{softmax}\big(f_v(g, \{S_u\}_{u \in \mathrm{Pa}(v)})\big)$$

因果图结构将联合后验按 DAG 拓扑序逐级分解，使推理过程显式可追踪：

$$p(Z|X) = p(z_{WMA}|X) \cdot p(z_{ToM}|X) \cdot p(z_{SA}|z_{WMA}, z_{ToM}, X) \cdot p(z_{Prag}|z_{SA}, z_{ToM}, z_{WMA}, X)$$

训练支持完全监督与半监督两种设置。完全监督下，仅对有标签节点计算掩码交叉熵损失 $\mathcal{L}_{\mathrm{sup}}$；半监督下，无标签父节点通过有标签子节点的链式梯度反向传播获得更新信号（Figure 4A），使模型能在部分标注条件下推断缺失状态。为稳定训练，采用边级教师强制（teacher forcing），子节点输入为真实标签与预测分布的伯努利混合信号。

### 第二阶段：指令微调

因果图训练完成后，其输出的结构化状态序列 $S = \{S_{WMA}, S_{ToM}, S_{SA}, S_{Prag}\}$ 作为显式推理引导，注入下游语言模型（Llama3.1-8B 或 Qwen2-Audio）。模型基于指令模板、原始语音输入（多模态 SLM 场景）及因果图状态，最大化条件生成概率：

$$\mathcal{L}_{\mathrm{IT}}(\theta) = -\sum_{(x,y)\in\mathcal{D}} \log p_\theta(y \mid \mathrm{Instr}, x, S_{WMA}, S_{ToM}, S_{SA}, S_{Prag})$$

这一设计将因果图构建的低熵认知状态搜索空间直接嵌入生成过程，使模型在推理时无需依赖隐式的 CoT 启发式搜索，即可获得结构化的认知先验引导。

### 关键设计决策

- **模块化因果结构**：与随机全连接图相比，预定义的 DAG 提供了稀疏且可解释的依赖关系，收敛速度提升约 5 倍（2.07h vs 10.39h），且因果效应评分（ACE/ICS）在不同监督信号强度下保持稳定（Table 2）。
- **多模态融合**：门控融合机制在节点分类准确率与因果效应之间取得最佳平衡，优于纯注意力或 Transformer 融合（Table 5）。
- **半监督梯度流**：通过关闭无标签父节点到子节点的教师强制（$p = 0$），强制子节点依赖父节点预测分布，从而构建可微梯度通路，使未标注模块仍能被有效学习（Equation 5）。

整体而言，SWM 框架将语音理解从端到端黑盒转变为“感知—因果推理—响应”的显式流水线，为后续的推理能力提升与可解释性分析奠定了基础。

### 因果图模块定义

SWM将语音理解分解为四个显式认知模块，每个模块的状态建模为离散分类变量：

- **WMA（World Model Action）**：捕捉声学事件与场景上下文，回答“发生了什么”；
- **ToM（Theory of Mind）**：推断说话者的情绪与心理状态，回答“说话者感受如何”；
- **SA（Speech Act）**：识别言语行为类型（如请求、陈述、问候），回答“说话者在做什么”；
- **Prag（Pragmatic Intent）**：推断语用意图（如讽刺、抱怨、赞美），回答“说话者真正想表达什么”。

四个模块通过有向无环图 $\mathcal{G} = (\mathcal{V}, \mathcal{E})$ 连接，其中 $\mathcal{V} = \{\text{WMA}, \text{ToM}, \text{SA}, \text{Prag}\}$，边集 $\mathcal{E}$ 编码模块间的因果依赖关系。

### 状态转移函数

每个模块的状态由其父节点状态和因果影响（动作）共同决定：

$$S_v = f_v\big(\{S_u : u \in \mathrm{Pa}(v)\}, A_{uv}\big)$$

其中 $S_v$ 为节点 $v$ 的潜在状态，$\mathrm{Pa}(v)$ 为 $v$ 的父节点集合，$A_{uv}$ 表示从父节点 $u$ 到子节点 $v$ 的因果动作（即施加的因果影响）。该公式形式化了“父节点状态通过因果动作影响子节点状态”这一核心机制。

### 联合后验的因果分解

给定多模态输入 $X$（文本、声学、韵律特征），潜在状态 $Z = \{z_{\text{WMA}}, z_{\text{ToM}}, z_{\text{SA}}, z_{\text{Prag}}\}$ 的联合后验按因果图结构逐级分解：

$$p(Z|X) = p(z_{\text{WMA}}|X) \cdot p(z_{\text{ToM}}|X) \cdot p(z_{\text{SA}}|z_{\text{WMA}}, z_{\text{ToM}}, X) \cdot p(z_{\text{Prag}}|z_{\text{SA}}, z_{\text{ToM}}, z_{\text{WMA}}, X)$$

该分解体现了因果图的核心约束：WMA和ToM为根节点，仅依赖输入 $X$；SA以WMA和ToM为父节点；Prag位于最下游，以所有前三者为父节点。这一结构将原本无约束的联合分布搜索空间压缩为低熵的因果子空间，是模型推理效率提升的关键。

### 监督多任务训练损失

在因果图训练阶段，仅对存在标签的节点计算交叉熵损失，通过掩码 $m_{i,v}$ 指示标签可用性：

$$\mathcal{L}_{\mathrm{sup}} = \sum_{i=1}^N \sum_{v \in \mathcal{V}} m_{i,v} \, \mathrm{CE}(y_{i,v}, S_{i,v})$$

其中 $y_{i,v}$ 为样本 $i$ 在节点 $v$ 的真实标签，$S_{i,v}$ 为模型预测的类别分布。该掩码机制是实现半监督训练的基础——未标注节点的 $m_{i,v} = 0$，其损失不直接计算，而是通过下游子节点的梯度链式传播间接优化。

### 边级教师强制混合信号

为稳定训练并控制误差传播，子节点输入采用真实标签与预测分布的伯努利混合：

$$\tilde{S}_{i,u} = \tau_{i,u\to v} \, \mathrm{onehot}(y_{i,u}) + (1 - \tau_{i,u\to v}) \, \mathrm{stopgrad}(S_{i,u}), \quad \tau \sim \mathrm{Bernoulli}(p_{u\to v})$$

其中 $\tau$ 为二元随机变量，$p_{u\to v}$ 为教师强制概率；$\mathrm{stopgrad}(\cdot)$ 阻止预测分布的梯度回传。该设计使子节点在训练早期依赖真实标签加速收敛，后期逐渐过渡到父节点的预测分布，增强鲁棒性。

### 半监督梯度流

在半监督条件下，无标签父节点通过有标签子节点的链式梯度获得更新：

$$\frac{\partial \mathcal{L}_i}{\partial \theta_j} = \sum_{\substack{k: m_{i,k}=1 \\ j \in \mathrm{Pa}(k)}} \frac{\partial \mathcal{L}_{i,k}}{\partial \eta_{i,k}} \frac{\partial \eta_{i,k}}{\partial S_{i,j}} \frac{\partial S_{i,j}}{\partial \eta_{i,j}} \frac{\partial \eta_{i,j}}{\partial \theta_j} \neq 0$$

该公式保证了即使父节点 $j$ 无直接监督信号（$m_{i,j}=0$），只要其子节点 $k$ 有标签，梯度即可沿因果边反向传播至 $j$。这是因果图支持半监督学习、推断缺失状态的理论基础。

### 指令微调损失

因果图训练完成后，其推断的状态序列 $I(\mathcal{G}(x))$ 作为显式推理引导，注入语言模型进行指令微调。对于纯文本LLM（如Llama3.1-8B）：

$$\mathcal{L}_{\Pi}(\theta) = -\sum_{(x,y)\in\mathcal{D}} \log p_\theta(y \mid \mathrm{Instr}, I(\mathcal{G}(x)))$$

对于多模态SLM（如Qwen2-Audio），同时输入原始语音和因果图状态：

$$\mathcal{L}_{\mathrm{IT}}(\theta) = -\sum_{(x,y)\in\mathcal{D}} \log p_\theta(y \mid \mathrm{Instr}, x, S_{\text{WMA}}, S_{\text{ToM}}, S_{\text{SA}}, S_{\text{Prag}})$$

两式均以交叉熵损失最大化给定条件下的响应生成概率，区别在于后者保留了原始语音信号 $x$，使模型可同时利用声学信息和结构化认知状态。

## 实验与关键发现

### 核心结果：因果图的结构化推理优势

SWM的核心实验围绕两个层面展开：因果图自身的结构有效性与将该图作为显式推理引导注入语言模型后的下游任务增益。

**因果图的结构有效性验证。** 表1在完全监督和半监督两种设置下评估了因果图的节点分类准确率和边因果效应。在完全监督下，四个模块（WMA、ToM、SA、Prag）的准确率均达到较高水平，且平均因果效应（Ave. ACE）为23.57，干预一致性分数（Ave. ICS）为30.39。作为对照，随机图基线（Random Graph）的Ave. ACE和Ave. ICS均仅为1，表明其未学到任何稳定的因果依赖关系。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_YGUKPGO182/figures/008_Table_1.jpg]]
*Table 1: Performance evaluation of the causal graph on node accuracy and edge validity under different supervision settings. The gray background in the semi-supervised rows highlights the accuracy of modules that were left unlabeled during training, demonstrating the model’s ability to infer latent states via causal structure. The rightmost columns evaluate the strength of learned causal dependencies using verage Causal Effect (ACE) and Intervention Consistency Score (ICS)*

半监督设置是验证因果结构价值的关键场景。当某一模块被设为无标签（表1中灰底行），模型需通过因果子节点的梯度传播来推断该模块的状态。结果显示：WMA作为隐变量时推断准确率为34.8%，ToM为43.3%，SA为34.4%。虽然绝对值不高，但考虑到这些模块完全无直接监督信号，这一结果表明因果结构确实提供了可用的归纳偏置。更重要的是，在半监督条件下，各因果边的ACE和ICS仍维持在稳定水平（图5），与完全监督下的趋势一致，证明学习到的因果依赖关系对监督信号的稀疏性具有鲁棒性。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_YGUKPGO182/figures/006_Figure_5.jpg]]
*Figure 5: ACE and ICS of each casual edge under both fully-supervised and semi-supervised training*

**随机图的失败模式。** 表2揭示了随机图基线的结构不稳定性。在不同教师强制概率（teacher-forcing probability）下，随机图的ACE和ICS呈混沌波动，且信息流模式缺乏一致性——最强和最弱的因果边随训练条件剧烈变化。这从反面证明，预定义的因果DAG结构并非冗余约束，而是引导模型收敛到稳定、可解释因果依赖关系的必要条件。因果图的训练收敛速度约为随机图的5倍（2.07小时 vs 10.39小时），进一步体现了结构化先验的优化效率。

### 下游指令微调：推理能力的跃升

表3展示了将因果图状态作为显式引导注入语言模型后的指令微调结果。核心指标为Overall M.J. Score（由GPT-4o裁判的加权综合评分，$0.6 \times R_s + 0.4 \times R_p$）。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_YGUKPGO182/figures/009_Table_3.jpg]]
*Table 3: Performance comparison against open-source and proprietary baselines. We report results under both Direct and CoT prompting styles. The Overall M.J. Score is the primary metric, calculated as a weighted aggregate ( 0 . 6 $\times R _ { s }$ + 0 . 4 $\times R _ { p }$ ) to balance the Reasoning Score (Rs) and the final Response Score ( $R _ { p }$ ) . . The Reasoning Breakdown columns provide granular metrics, where EM and EA denote emotion mention rate and emotion classification accuracy, respectively. R-Len indicates the average length of the generated response in words

**与开源SLM基线的对比。** SWM（Qwen2-Audio）在CoT提示风格下取得7.59的Overall M.J. Score，而使用相同CoT数据微调的Qwen2-Audio-CoT基线仅为5.18，提升幅度达+2.41。这一对比直接消除了数据质量差异的影响，将性能增益归因于因果图提供的显式状态引导。在Direct风格下，SWM（Llama3.1-8b）达到7.81，显著高于Qwen-Audio（2.39）、Qwen2-Audio（4.33）和Voxtral（4.14）等开源SLM。

**情绪识别的突破性提升。** 在推理过程中的情绪分类准确率（EA）上，SWM（Qwen2-Audio）达到71.02%，而Qwen2-Audio-CoT基线仅为34.72%，提升高达+36.30个百分点。这一结果甚至超越了商用大模型GPT-4o（45.16%），直接验证了因果图中ToM→SA因果边对情绪到言语行为推理的显式建模价值。

**与商用大模型的成本效率对比。** SWM（Llama3.1-8b）的Overall M.J. Score（7.81）略低于Gemini 2.5 Pro（8.12），差距仅为-0.31，但SWM的训练成本仅为20 GPU小时（A6000），远低于商用大模型的训练投入。在情绪识别这一关键推理维度上，SWM已实现对商用模型的超越。

### 消融研究：因果边与融合机制的关键作用

表5和表6分别报告了完全监督和半监督下的消融结果。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_YGUKPGO182/figures/011_Table_5.jpg]]
*Table 5: Ablation study on the Causal Graph under the fully-supervised setting. We investigate the impact of different fusion mechanisms (Gated, attention, transformer), teacher-forcing probabilities (p), and the removal of specific causal edges. The baseline model from the main text is highlighted*

**融合机制的影响。** 在完全监督下（表5），门控融合（Gated）在节点准确率和因果效应之间取得最佳平衡，被选为默认配置。注意力融合（Attention）和Transformer融合虽略微提高了Ave. ACE，但导致节点分类准确率下降，表明更强的特征交互可能引入噪声，损害模块的判别能力。

**因果边移除的影响。** 移除特定因果边（表5，edge removal部分）的消融直接验证了因果结构的必要性。移除ToM→SA边导致SA模块准确率显著下降，证实了从心理状态推断到言语行为建模的因果依赖关系。这一发现与主实验中情绪识别的大幅提升相互印证。

**半监督下的鲁棒性。** 表6显示，在半监督条件下，将特定模块的输入从多模态融合特征$g$替换为纯文本特征$h_{text}$时，性能依然保持鲁棒。这表明因果结构本身——而非多模态特征的丰富性——是半监督学习成功的主要驱动力。

**教师强制概率的稳定性。** 表5还考察了教师强制概率$p$在0.0到1.0范围内的变化。结果显示，因果图的节点准确率和因果效应评分在该范围内保持稳定，表明模型对监督信号的强度不敏感，结构化先验提供了足够的正则化。

### 评估的公平性说明

需注意以下评估局限性：Model-as-Judge评分依赖GPT-4o作为裁判模型，可能引入其固有的偏好偏见；训练数据标签由Vicuna-13b教师模型生成，标签噪声或分布偏移可能影响性能上限；实验数据以英语对话场景为主，多语种泛化性尚未验证；训练成本优势基于小模型和特定GPU配置，与商用大模型在数据规模和计算量上不具备完全可比性。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_YGUKPGO182/figures/014_Figure_6.jpg]]
*Figure 6: ACE and ICS of each casual edge for ablation study (fusion mechanisms and teacher-forcing probabilities) on casual graph under fully-supervised setting*

## 定位与知识库关联

### 核心思想溯源与差异化

SWM 的核心思想源于认知科学对语音理解过程的模块化分解，将语音理解视为一个由**世界模型激活**（WMA）、**心理理论**（ToM）、**言语行为**（SA）和**语用意图**（Prag）四个认知模块构成的因果推理过程。这一思路与当前主流的语音语言模型（SLM）形成了根本性的范式差异。

现有开源 SLM，如 **Qwen-Audio**（Chu et al., 2023）、**Qwen2-Audio**（Chu et al., 2024）和 **Voxtral**（Liu et al., 2025），将语音理解视为端到端的单一黑盒映射，仅聚合孤立的任务输出，忽略了语音成分间的内在因果依赖关系。这些模型依赖 LLM 隐层状态或 CoT 提示进行隐式推理，其推理链搜索空间是无约束的自回归生成或启发式搜索，缺乏结构化的认知引导。SWM 的关键差异化在于：

1. **显式因果状态表示**：将隐式推理替换为因果图推断的显式分类状态（WMA、ToM、SA、Prag）及因果链，形成受因果图约束的低熵认知状态子空间。
2. **两阶段训练范式**：将单阶段指令微调扩展为“因果图多任务训练（监督/半监督） + 指令微调”的两阶段流程，使得 LLM 在生成响应前先获得结构化的认知状态引导。

从世界模型的统一视角（Figure 3）来看，SWM 的因果图位于生成式世界模型（Garrido et al., 2024）和语言世界模型之间：前者是前向动态模型，后者依赖语言描述进行推理，而 SWM 的因果图提供了这些动态过程的结构化、显式表达。

### 与 CoT 基线的关系

值得注意的是，论文将 **Qwen2-Audio-CoT** 作为微调基线，以消除数据质量差异对性能对比的影响。该基线使用与 SWM 相同的 CoT 数据（由 Vicuna-13b-v1.5 教师模型生成）进行微调，但未引入因果图结构。Table 3 显示，Qwen2-Audio-CoT 的 Overall M.J. Score 仅为 5.18，而 SWM（Qwen2-Audio）达到 7.59（+2.41），情绪分类准确率更是从 34.72% 跃升至 71.02%（+36.30%）。这一对比直接证明了因果图的显式引导——而非数据质量——是性能提升的核心驱动力。

### 与商用大模型的定位关系

SWM 在性能上展现出与商用大模型 **GPT-4o**（OpenAI, 2024）和 **Gemini 2.5 Pro**（Gemini Team, 2025）可竞争的能力。SWM（Llama3.1-8b）的 Overall M.J. Score 为 7.81，略低于 Gemini 2.5 Pro CoT 的 8.12（-0.31），但训练成本仅约 20 GPU 小时（A6000），远低于商用大模型的数据规模和计算量投入。在情绪识别这一关键推理能力上，SWM（Qwen2-Audio）的 71.02% 准确率显著超越 GPT-4o 的 45.16%，说明因果图提供的结构化认知先验在特定推理维度上具有超越大规模参数化模型的潜力。

### 适用边界与局限

1. **模块固定性**：当前因果图仅包含四个预定义认知模块，更丰富多样的内部状态可能进一步增强语音理解能力。因果图结构为基于认知先验的预定义 DAG，尚不能自适应地学习或调整结构以适配新领域。
2. **数据依赖**：数据标注与合成流水线依赖 Vicuna-13b 教师模型，可能引入标签噪声和错误传播。半监督训练虽能推断缺失状态，但 Table 1 显示无标签模块的准确率（WMA: 34.8%, ToM: 43.3%, SA: 34.4%）仍显著低于有监督情况，说明完全无标注场景下的推理能力有限。
3. **语言与场景局限**：实证评估主要集中在英语对话与语音助手场景（MELD、IEMOCAP、SLURP 等），在多语种、多文化及复杂真实交互环境下的泛化性尚未得到验证。
4. **评估偏差**：Model-as-Judge 评估采用 GPT-4o 作为裁判模型，可能引入其固有的偏好偏见，且与商用大模型在数据规模和计算量上不具备完全可比性。

### 开放问题

1. **自适应因果结构学习**：如何让模型自动学习最优的因果图结构，而无需依赖人工定义的认知先验？当前随机图消融（Table 2）显示无结构全连接图无法学习稳定因果依赖（ACE 和 ICS 均接近 1），说明结构先验是必要的，但如何从数据中发现结构仍是一个开放挑战。
2. **动态交互扩展**：所提框架能否扩展到多轮对话、多人交互等更复杂的动态因果推理场景？当前因果图假设单轮语音输入，未建模对话状态的时间演化。
3. **标注效率提升**：如何减少对 LLM 生成标签的依赖，提高在真实少量标注数据下的半监督学习效率？当前半监督设置仍依赖部分模块的有监督信号进行梯度传播。
4. **跨模态迁移**：显式因果状态表示作为一种通用认知先验，能否迁移到视频理解、多模态情感分析等其他任务？因果图的模块化设计理论上具有任务无关性，但实证验证尚缺。
5. **规模化效率保持**：在更大规模、更多样化的数据集上训练时，结构化因果图是否依然能保持其效率和可解释性优势？当前实验规模相对有限（最大数据集 SLURP 约 72K 样本），大规模下的因果效应稳定性和收敛速度优势需要进一步验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Speech_World_Model_Causal_StateAction_Planning_with_Explicit_Reasoning_for_Speech.pdf]]
