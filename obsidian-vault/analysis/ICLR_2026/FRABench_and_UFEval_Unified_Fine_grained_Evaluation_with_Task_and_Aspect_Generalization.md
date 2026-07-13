---
title: "FRABench and UFEval: Unified Fine-grained Evaluation with Task and Aspect Generalization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/FRABench_and_UFEval_Unified_Fine_grained_Evaluation_with_Task_and_Aspect_Generalization.pdf
project_link: null
code_link: null
openreview_forum_id: 7WdY3Cojy9
aliases:
- FUUFGETAG
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "构建一个层次化的方面分类法（aspect taxonomy），并据此创建大规模细粒度评估数据集FRABench，然后在该数据集上训练一个统一的多任务多方面评估器UFEval，利用方面之间的内在关联实现泛化。"
primary_logic: "评估方面之间存在内在关联，联合学习多个视觉任务和多个评估方面可以产生协同效应，使得在部分方面上训练的评估器能够泛化到其他相关方面，甚至未见过的任务。"
claims:
- "在FRA-OOD上，UFEval在所有任务上均显著优于单任务评估器Themis和LLaVA-Critic，展示了强大的任务泛化能力。"
- "在未见过的方面上，UFEval仍保持高效评估，总体准确率在FRA-OOD上达86.2%（与GPT-4o一致性）和83.2%（与人类一致性）。"
- "联合学习多个视觉任务（IU、IG、ITIG）和多个方面能够逐步提升评估器的性能，验证了多任务协同效应。"
- "FRA-OOD NLG (Task Generalization) 上 Accuracy = 81.7"
---

# FRABench and UFEval: Unified Fine-grained Evaluation with Task and Aspect Generalization

> [!tip] 核心洞察
> 评估方面之间存在内在关联，联合学习多个视觉任务和多个评估方面可以产生协同效应，使得在部分方面上训练的评估器能够泛化到其他相关方面，甚至未见过的任务。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FRABench与UFEval：具备任务和方面泛化的统一细粒度评估 |
| 英文题名 | FRABench and UFEval: Unified Fine-grained Evaluation with Task and Aspect Generalization |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=7WdY3Cojy9) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | UFEval |
| Dataset | FRA-OOD NLG (Task Generalization), SummEval (Ave.), MT-Bench, VLRewardBench (General) |

> [!tip] 效果简介
> - FRA-OOD NLG (Task Generalization) 上，Accuracy 为 81.7，对比 50.4 (Qwen2VL-7B)，变化 +31.3。
> - SummEval (Ave.) 上，Kendall's tau 为 69.0，对比 59.3 (Prometheus 2)，变化 +9.7。
> - MT-Bench 上，Kendall's tau / diff 为 74.9 / 88.3，对比 43.6 / 37.7 (Themis)，变化 +31.3 / +50.6。

## 概要

现有的“MLLM-as-a-Judge”评估范式存在一个关键瓶颈：评估器通常针对特定任务和特定评估方面进行设计，缺乏向未见任务与未见方面的泛化能力。同时，社区缺少一个大规模、多模态的细粒度评估数据集来支撑统一评估器的训练。本文的核心洞察在于，不同评估方面之间存在内在关联——联合学习多个视觉任务和多个评估方面可以产生协同效应，使得评估器能够泛化到相关方面甚至全新任务。

基于这一认知，作者提出了两个核心贡献：**FRABench**，一个基于层次化方面分类法构建的大规模细粒度评估基准，包含60.4k成对样本和325k评估标签；以及**UFEval**，首个具备任务和方面泛化能力的统一细粒度评估器，通过在FRABench上对Qwen2-VL-7B-Instruct进行监督微调（SFT）得到。

UFEval在任务泛化评估中表现突出：在FRA-OOD上，NLG任务准确率达81.7%，较Qwen2VL-7B的50.4%提升31.3个百分点；在方面泛化评估中，与GPT-4o和人类判断的总体一致性分别达到86.2%和83.2%。在外部基准上，UFEval同样展现出竞争力——SummEval上Kendall's tau达69.0（超越Prometheus 2的59.3），MT-Bench上Kendall's tau达74.9（远超Themis的43.6）。消融实验进一步证实，多任务多方面联合训练是性能提升的关键驱动力：仅用IG数据训练时准确率为46.6%，联合IU和ITIG后提升至52.5%和50.1%，最终UFEval达到53.6%。

在方法谱系中，UFEval区别于GPT-4o、Claude-3.5等提示型模型，也与Themis（Hu et al., 2024b）、LLaVA-Critic（Xiong et al., 2024）等单任务微调评估器形成对比——后者仅覆盖有限任务和方面，而UFEval首次实现了跨NLG、IU、IG、ITIG四大任务类型及28个子任务的统一细粒度评估。其局限性主要体现在图像生成评估性能相对有限、对阴暗图像的Harmfulness误判倾向，以及数学推理任务上的薄弱表现。



### 问题背景：MLLM-as-a-Judge 的评估瓶颈

随着多模态大语言模型（MLLM）能力的快速提升，如何可靠地评估其输出质量已成为制约模型迭代的关键瓶颈。传统的单一数值评分（如整体质量分）无法揭示模型在具体维度上的优劣，而“MLLM-as-a-Judge”范式——即使用另一个（更强）模型作为评估器——虽然展现出了一定的细粒度评估潜力，但现有方法普遍存在两个根本性缺陷：

1.  **任务锁定**：现有评估器（如 **Themis**、**LLaVA-Critic**）通常针对单一视觉任务（如图像理解或图像生成）设计，无法跨任务泛化。当面对训练时未见过的任务类型时，其评估能力急剧退化。
2.  **方面锁定**：评估器所能评判的“方面”（aspect）由训练数据预先定义，缺乏对新评估维度的泛化能力。这意味着每新增一个评估维度（如“幽默性”或“文化敏感性”），都需要重新收集标注数据并训练新模型。

### 核心瓶颈：泛化能力的缺失

上述问题的本质在于：**现有的“MLLM-as-a-Judge”评估器无法泛化到未见过的任务和未见过的评估方面**。这一瓶颈源于两个层面的缺失：

-   **数据层面**：缺少一个大规模、多模态、覆盖广泛评估方面的细粒度评估数据集。现有数据集要么局限于特定任务，要么仅提供整体评分，无法支撑统一评估器的训练。
-   **机制层面**：不同评估方面之间存在内在关联（例如，文本生成的“连贯性”与图文交织生成的“图文一致性”共享部分底层语义判断能力），但现有方法采用孤立训练策略，未能利用这种协同效应。

### 本文动机：构建统一、可泛化的细粒度评估体系

针对上述瓶颈，本文提出了一套从数据到模型的完整解决方案：

-   **构建层次化方面分类法（Aspect Taxonomy）**：通过系统梳理自然语言生成（NLG）、图像理解（IU）、图像生成（IG）和图文交织生成（ITIG）四大类、28个子任务的评估需求，构建一棵包含通用方面（Universal Aspects, UAs）和任务特定方面（Task-specific Aspects, TAs）的方面树，显式建模方面之间的层级关系和内在关联。
-   **创建大规模细粒度评估数据集 FRABench**：基于方面分类法，通过混合人工标注与 GPT-4o 自动标注的方式，构建包含 60.4k 成对比较样本、325k 细粒度评估标签的多模态数据集，覆盖 4 大任务、28 个子任务。
-   **训练统一多任务多方面评估器 UFEval**：在 FRABench 上对 Qwen2-VL-7B-Instruct 进行监督微调（SFT），使单一模型能够同时处理多种视觉评估任务，并利用方面之间的内在关联实现对新任务、新方面的泛化。

### 核心洞见：多任务协同带来泛化能力

本文的核心假设是：**评估方面之间存在内在关联，联合学习多个视觉任务和多个评估方面可以产生协同效应**。这种协同效应使得在部分方面上训练的评估器能够泛化到其他相关方面，甚至扩展到训练时完全未见过的任务类型。后续实验将通过任务泛化评估（在 FRA-OOD 上测试）和方面泛化评估（在未见过的 TAs 上测试）来系统验证这一假设。



## 核心方法与创新机理

### 问题瓶颈

现有“MLLM-as-a-Judge”评估器普遍存在两个结构性缺陷：**任务锁定**与**方面锁定**。以**Themis**（Hu et al., 2024b）和**LLaVA-Critic**（Xiong et al., 2024）为代表的微调评估器仅针对单一任务（如IU或IG）设计，无法泛化到其他任务类型；同时，它们评估的方面数量有限，缺乏对未见方面的判断能力。此外，缺乏大规模、多模态的细粒度评估数据集来支撑统一评估器的训练，使得跨任务、跨方面的泛化成为当前领域的核心瓶颈。

### 核心洞察：评估方面的内在关联

本文的核心洞察在于：**评估方面之间存在内在关联，联合学习多个视觉任务和多个评估方面可以产生协同效应**。具体而言，一个在“图像理解（IU）”任务上学会评估“准确性”和“完整性”的模型，其习得的判别能力可以迁移到“图像生成（IG）”任务中的“保真度”和“一致性”评估上。这种关联使得在部分方面上训练的评估器能够泛化到其他相关方面，甚至完全未见过的任务。Figure 5的消融实验直接验证了这一机制：仅使用IG数据训练时，Qwen2VL-7B在IG任务上仅达到46.6%准确率；联合IU和ITIG训练后提升至52.5%和50.1%；最终UFEval达到53.6%，多任务协同效应显著。

### 关键创新：Changed Slot

与基线方法的本质差异体现在一个核心操作上——**将Qwen2-VL-7B-Instruct在FRABench上进行监督微调（SFT）**，使其从一个通用多模态语言模型转变为一个统一的多任务多方面评估器。具体对比：

- **基线值**：Qwen2-VL-7B-Instruct（无微调）仅能通过提示进行通用评估，在FRA-OOD的NLG任务上准确率仅为50.4%（Table 2）。
- **提出值**：UFEval（Qwen2-VL-7B-Instruct在FRABench上SFT）在相同条件下达到81.7%，提升31.3个百分点。

这一微调操作之所以有效，依赖于两个配套创新：

1. **层次化方面分类法（Aspect Taxonomy）**：将评估方面组织为通用方面（UAs）和任务特定方面（TAs）两棵子树，通过双向匹配策略构建层次结构。这一分类法使得评估器能够识别方面之间的语义关联，为泛化提供结构化先验。

2. **FRABench数据集**：基于上述分类法构建的大规模细粒度评估数据集，包含60.4k个成对样本和325k个评估标签，覆盖NLG、IU、IG、ITIG四类任务下的28个子任务。该数据集通过混合人类标注和GPT-4o标注构建，为统一评估器的训练提供了必要的数据基础。

### 泛化机制

UFEval的泛化能力体现在两个维度：

- **任务泛化**：使用已见的通用方面（UAs）评估未见任务。在FRA-OOD上，UFEval在NLG、IU、IG、ITIG四个任务上分别达到81.7%、90.4%、69.0%、83.1%的准确率（与GPT-4o一致性），显著优于单任务评估器Themis和LLaVA-Critic（Table 2）。

- **方面泛化**：在完全未见过的任务特定方面（TAs）上，UFEval仍保持高效评估，总体准确率达86.2%（与GPT-4o一致性）和83.2%（与人类一致性）（Table 2）。这得益于多任务联合训练中习得的跨方面判别能力。



UFEval 的评估流水线由两个核心步骤构成：**方面选择（Aspect Selection）** 与 **评估执行（Evaluating）**，其设计目标是在统一框架下实现对多模态输出的细粒度、可泛化评估。

**方面选择阶段**：给定一个评估任务（包含指令、图像等输入内容及待评估的模型响应），系统首先根据任务属性（属于 NLG、IU、IG 还是 ITIG）和输出模态，从事先构建的层次化方面分类法（aspect taxonomy）中选取适用的评估方面。该分类法由一个根节点“overall”统领，其下分为两个子树——**通用方面（Universal Aspects, UAs）** 和 **任务特定方面（Task-specific Aspects, TAs）**。UAs 跨任务共享（如 Helpfulness、Harmfulness），TAs 则与具体子任务绑定（如 IG 下的 Aesthetics）。方面之间的层次关系通过双向匹配策略（bidirectional matching strategy）自动构建，确保分类法兼具系统性与可扩展性。

**评估执行阶段**：UFEval 接收选定的方面列表以及原始输入内容，逐方面生成反馈文本，并给出成对比较评分（pairwise comparison），最终汇总为整体评估结果。框架采用成对比较而非逐点打分，旨在减少上下文偏差并便于后续用于奖励模型训练。

UFEval 本身以 **Qwen2-VL-7B-Instruct** 为基座，在 FRABench 数据集上通过监督微调（SFT）训练得到。FRABench 是支撑整个框架的关键数据基础，包含 60.4k 个成对样本，覆盖 28 个子任务，共产生 325k 个细粒度评估标签（由人工标注与 GPT-4o 标注混合生成）。这一数据构造流程与方面分类法的设计共同赋予了 UFEval 对未见任务和未见方面的泛化能力——模型在训练中接触的是部分 UAs 和 TAs 的组合，但联合学习多个视觉任务和多个评估方面所产生的协同效应，使其能够将评估能力迁移到训练时未曾见过的任务-方面组合上。

> **证据强度说明**：上述流水线描述基于 Figure 1 的示意及 Section 3 的方法论阐述，数据规模来自 Section 1 和 Section 3.2.1 的明确声明。方面分类法的构建细节（双向匹配策略、UA/TA 划分）在 Section 3.1.2 中有详细说明，置信度较高。泛化能力的具体实验证据见 Table 2 及相关消融实验，此处仅描述框架设计逻辑，不展开量化结果。



### 评估流水线模块

UFEval的评估流水线由两个核心模块构成：

**方面选择（Aspect Selection）**：根据输入任务的任务属性（task property）和输出模态（output modality），从层次化的方面分类法（aspect taxonomy）中自动选择适当的评估方面。该分类法将方面组织为通用方面树（Universal Aspects, UAs）和任务特定方面树（Task-specific Aspects, TAs），其中UAs适用于所有任务类型，TAs则针对特定任务定制。

**UFEval评估（UFEval Evaluating）**：基于输入内容（包括指令、图像和成对响应）及选定的方面，生成细粒度反馈和评分，完成成对评估。该模块的核心是经过FRABench数据集监督微调（SFT）的Qwen2-VL-7B-Instruct模型，使其能够同时处理NLG、IU、IG和ITIG四类任务的多方面评估。

### 关键公式

#### DPO损失函数（多模态语言模型对齐）

在利用UFEval构造偏好数据进行模型对齐时，对于多模态大语言模型（MLLMs）采用以下DPO损失：

$$L(\theta) = -\mathbb{E}_{(x,y_w,y_l)\sim D} \left[ \log \sigma \left( \beta_u \log \frac{\pi_\theta(y_w|x)}{\pi_{\mathrm{ref}}(y_w|x)} - \beta_u \log \frac{\pi_\theta(y_l|x)}{\pi_{\mathrm{ref}}(y_l|x)} \right) \right]$$

其中：
- $x$ 为输入（包含图像和文本指令）
- $y_w$ 和 $y_l$ 分别为偏好对中的获胜响应和失败响应
- $\pi_\theta$ 为当前策略模型，$\pi_{\mathrm{ref}}$ 为参考模型
- $\beta_u$ 为控制偏好强度的温度参数（在IU任务DPO中设为 $0.1$）
- $\sigma$ 为sigmoid函数

该损失通过最大化获胜响应相对于失败响应的对数概率比，使模型倾向于生成符合人类偏好的输出。

#### DPO损失函数（扩散模型对齐）

对于图像生成扩散模型（如SDXL-Turbo）的偏好对齐，采用以下DPO损失：

$$L(\theta) = -\mathbb{E}_{(x_0^w,x_0^l)\sim\mathcal{D}_{Gen}, t\sim\mathcal{U}(0,T), x_t^w\sim q(x_t^w|x_0^w), x_t^l\sim q(x_t^l|x_0^l)} \log \sigma \left( -\beta_g T \omega(\lambda_t) \left( \|\epsilon^w - \epsilon_\theta(x_t^w,t)\|_2^2 - \|\epsilon^w - \epsilon_{\mathrm{ref}}(x_t^w,t)\|_2^2 - \left( \|\epsilon^l - \epsilon_\theta(x_t^l,t)\|_2^2 - \|\epsilon^l - \epsilon_{\mathrm{ref}}(x_t^l,t)\|_2^2 \right) \right) \right)$$

其中：
- $x_0^w$ 和 $x_0^l$ 分别为偏好对中的获胜图像和失败图像
- $t \sim \mathcal{U}(0,T)$ 为均匀采样的时间步
- $x_t^w$ 和 $x_t^l$ 为对应加噪后的隐变量
- $\epsilon^w$ 和 $\epsilon^l$ 为真实噪声
- $\epsilon_\theta$ 为当前模型预测噪声，$\epsilon_{\mathrm{ref}}$ 为参考模型预测噪声
- $\beta_g$ 为偏好强度参数（在IG任务DPO中设为 $5000$）
- $\omega(\lambda_t)$ 为信噪比相关的权重函数

该损失通过比较获胜图像和失败图像上的噪声预测误差差异，引导扩散模型生成更符合人类偏好的图像。



## 实验与关键发现

### 评估设置与基线

为验证UFEval的任务泛化与方面泛化能力，论文构建了两类测试集：**FRA-OOD**（以GPT-4o标注为基准）和**FRA-OOD-H**（以人工标注为基准）。测试时，任务泛化评估使用UFEval见过的通用方面（Universal Aspects, UAs）搭配未见过的任务；方面泛化评估则使用未见过的任务中的未见过的方面，并进一步细分为上下文泛化（12个方面）和新颖方面泛化（15个方面）两个维度。

对比基线涵盖两类模型：
- **提示型模型**：GPT-4o、Claude-3.5、Qwen3-VL-8B、Qwen2-VL-72B-Instruct、Qwen2-VL-7B-Instruct。
- **微调评估器**：Themis-8B（Hu et al., 2024b）、LLaVA-Critic-7B（Xiong et al., 2024）、Auto-J（Li et al., 2023b）、Prometheus 2（Kim et al., 2024a）、ImageReward（Xu et al., 2023a）、VisionReward（Xu et al., 2024）、Q-Eval（Zhang et al., 2025）、CIGEval（Wang et al., 2025a）。

UFEval基于Qwen2-VL-7B-Instruct在FRABench训练集上进行SFT微调。所有MLLM-as-a-Judge评估使用统一的提示模板，训练集与测试基准之间无数据重叠。

### 任务与方面泛化核心结果

Table 2报告了泛化评估的核心结果。在**任务泛化**维度上，UFEval在FRA-OOD的四个任务上均显著优于单任务微调评估器：

| 任务 | UFEval | Themis | LLaVA-Critic | Qwen2VL-7B |
|------|--------|--------|--------------|------------|
| NLG  | 81.7   | —      | —            | 50.4       |
| IU   | 90.4   | —      | —            | —          |
| IG   | 69.0   | —      | —            | —          |
| ITIG | 83.1   | —      | —            | —          |

UFEval在FRA-OOD上总体准确率达85%（GPT-4o一致性），在FRA-OOD-H上达83%（人工一致性），而单任务评估器Themis和LLaVA-Critic因缺乏跨任务训练数据，在这些未见任务上表现显著下降。

在**方面泛化**维度上，UFEval在未见过的方面上仍保持高效评估：FRA-OOD上总体准确率86.2%（GPT-4o一致性），FRA-OOD-H上83.2%（人工一致性）。Figure 3的可视化对比显示，UFEval在黑色区域（未见过的任务特定方面）仍能维持较高准确率，而提示型模型和单任务评估器在这些区域出现明显的性能塌陷。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_7WdY3Cojy9/figures/093_Figure.jpg]]
*Figure: 3. Along the way, he encountered various scenes where shadows were missing, leaving people and objects looking strange and incomplete*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_7WdY3Cojy9/figures/095_Figure.jpg]]
*Figure: 3. Shadow when I was playing with him in the park! Mr. Shadow is such a bad influence!" Jack tried to ignore them, but his parents noticed that something seemed wrong and decided it would be better if he had no more imaginary friends since they only brought trouble for everyone involved and distracted from what really mattered: schoolwork, eating right (he needed a haircut), sports practice, going outside, and being. 4. spending time with his family. Jack’s parents talked to him about the negative effect imaginary friends had on children in particular and explained that there would be a better way for them both if he gave up Mr. Shadow, but it seemed hopeless because every place he looked a...*

### 多任务MLLM-as-a-Judge评估

Table 3、4、5分别展示了NLG、IU、IG任务上的MLLM-as-a-Judge评估结果。

**NLG任务**（Table 3）：UFEval在SummEval平均Kendall's tau上达69.0，超过GPT-4o（65.3）和Prometheus 2（59.3），与Claude-3.5（69.6）持平。在MT-Bench上，UFEval的tau/diff达74.9/88.3，虽低于GPT-4o（83.5/92.7）和Claude-3.5（90.7/95.1），但远超Themis（43.6/37.7）和Auto-J（38.3/24.4）。在MANS上，UFEval的diff达69.3，略优于GPT-4o（68.5）。

**IU任务**（Table 4）：UFEval在VLRewardBench的General子集上diff达46.4，超过LLaVA-Critic（42.0），并在WildVision和MLLM-as-a-Judge基准上展现出全面的优势，验证了多视觉任务联合训练带来的协同增益。

**IG任务**（Table 5）：UFEval在GenAI-Bench上tau/diff达53.6/65.5，超过ImageReward（48.6/64.9）。但在IG任务上整体性能提升幅度相对有限，论文将此归因于底层多模态语言模型的视觉语义理解不足。

### 消融实验：多任务与多方面协同效应

Figure 5和Table 5中的多任务变体训练结果揭示了核心机制：**联合学习多个视觉任务和多个评估方面产生显著的协同效应**。

- 仅使用IG数据训练时，Qwen2VL-7B在IG任务上准确率为46.6%；加入IU数据联合训练后提升至52.5%；再加入ITIG数据后进一步提升至50.1%；最终UFEval达到53.6%。
- 多方面训练的增益更为显著：Qwen2VL-7B在单方面IG评估时仅有35.9%准确率，而UFEval达到77.0%（Table 51）。

这表明评估方面之间的内在关联使得模型能够从相关方面的训练中迁移知识，从而在未见过的方面上实现泛化。

### DPO对齐应用验证

为验证UFEval生成评估数据的实际价值，论文将其用于DPO偏好对齐训练：

- **IU DPO**（Table 6）：使用UFEval生成偏好数据对LLaVA-Next-7B进行DPO，在LLaVABen.Wild上得分61.4，优于使用LLaVA-Critic数据的60.1。DPO训练使用学习率$5 \times 10^{-7}$，$\beta_u = 0.1$。
- **IG DPO**（Table 7）：从Pick-a-Pic提取提示和对应图像对，用UFEval构建偏好数据训练SDXL-Turbo，使用$\beta_g = 5000$、batch size 32在8张A100 GPU上训练3个epoch。在HPSv2上达到29.9，优于直接在原始Pick-a-Pic数据集上训练的基线。

### 失败模式与局限性

论文明确指出了UFEval的几个关键失败模式：

1. **IG任务性能瓶颈**：UFEval在图像生成评估上提升有限，根本原因在于底层多模态语言模型（Qwen2-VL-7B-Instruct）缺乏足够的主动视觉语义理解能力，难以精确判断生成图像的细粒度质量差异。
2. **Harmfulness误判**：在判断有害内容时，UFEval对阴暗或阴沉色调的图像存在过度敏感，倾向于将其误判为有害内容。这可能需要更细粒度的方面定义或增加针对性训练数据来解决。
3. **逻辑推理短板**：在数学推理等需要强逻辑能力的任务上，UFEval表现较差，这反映了当前多模态语言模型在符号推理上的通用局限。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_7WdY3Cojy9/figures/044_Figure_14.jpg]]
*Figure 14: Comparison of UFEval-72B on FRA-ID and FRA-ID-H. The top shows alignment with GPT-4o using FRA-ID, the bottom shows alignment with human annotators using FRA-ID-H. Each point is the average accuracy (with ties) for an aspect shared across sub-tasks of the same task*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_7WdY3Cojy9/figures/046_Figure_15.jpg]]
*Figure 15: Comparison of UFEval-72B on FRA-OOD and FRA-OOD-H. The blue-colored aspects indicate unseen TAs, whereas the black-colored aspects represent seen UAs. The ’ow/ unseen’ designation in the table represents evaluations conducted exclusively on unseen aspects, with accuracy metrics computed only for unseen TAs*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_7WdY3Cojy9/figures/072_Figure.jpg]]
*Figure: Comparison of Alpha Values Distribution*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_7WdY3Cojy9/figures/075_Table_57.jpg]]
*Table 57: Statistics of Aspect-level Correlation*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_7WdY3Cojy9/figures/076_Figure_19.jpg]]
*Figure 19: Heatmap of Kendall’s Tau (τ ) correlations between evaluation aspects across different tasks. (Part 1)*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_7WdY3Cojy9/figures/077_Figure_20.jpg]]
*Figure 20: Heatmap of Kendall’s Tau (τ ) correlations between evaluation aspects across different tasks. (Part 2)*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_7WdY3Cojy9/figures/078_Figure_21.jpg]]
*Figure 21: Heatmap of Kendall’s Tau (τ ) correlations between evaluation aspects across different tasks. (Part 3)*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_7WdY3Cojy9/figures/079_Figure_22.jpg]]
*Figure 22: Heatmap of Kendall’s Tau (τ ) correlations between evaluation aspects across different tasks. (Part 4)*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_7WdY3Cojy9/figures/092_Figure.jpg]]
*Figure: Response 1*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_7WdY3Cojy9/figures/094_Figure.jpg]]
*Figure: 2. My cousin says Mr. Shadow stole her favorite toy" or "My best friend saw Mr. 1. Show scenes of Oliver chasing his shadow and the moment he reclaims the stolen shadows. A boy named Jack had an imaginary friend, Mr. Shadow, who would follow him around wherever he went in school or at home when no one else was watching. At first it didn’t bother Jack much, but soon after that people started talking about their own experiences with Mr. Shadow too! "I don’t believe*



## 定位与知识库关联

### 1. 在“MLLM-as-a-Judge”评估器谱系中的位置

UFEval 处于“微调评估器”（Fine-tuned Evaluator）这一分支，其直接前身是通用视觉语言模型 **Qwen2-VL-7B-Instruct**（未提供引用），通过在大规模细粒度评估数据集 FRABench 上进行监督微调（SFT）获得评估能力。与之并列的微调评估器包括：

- **Themis-8B**（Hu et al., 2024b）：面向特定任务的微调评估器，缺乏任务和方面的泛化能力。
- **LLaVA-Critic-7B**（Xiong et al., 2024）：面向图像理解（IU）任务的微调评估器。
- **Prometheus 2**（Kim et al., 2024a）与 **Auto-J**（Li et al., 2023b）：主要面向自然语言生成（NLG）任务的评估器。
- **ImageReward**（Xu et al., 2023a）与 **VisionReward**（Xu et al., 2024）：面向图像生成（IG）任务的评估器。
- **Q-Eval**（Zhang et al., 2025）与 **CIGEval**（Wang et al., 2025a）：较新的评估器，覆盖部分视觉任务。

UFEval 与上述工作的核心差异在于：它是首个以统一模型覆盖 NLG、IU、IG、ITIG 四类任务、28 个子任务，并具备任务泛化和方面泛化能力的细粒度评估器。这一能力来源于其层次化方面分类法（aspect taxonomy）和 FRABench 数据集的多任务、多方面联合训练。

在提示型模型（Prompting Models）一侧，基线包括 **GPT-4o**、**Claude-3.5**、**Qwen2-VL-72B-Instruct** 和 **Qwen3-VL-8B**。这些模型通过提示工程直接进行评估，无需微调，但缺乏对细粒度方面的结构化理解，且在分布外任务和方面上的泛化能力显著弱于 UFEval（见 Table 2 结果）。

### 2. 适用边界与局限

**适用边界**：
- UFEval 在 NLG、IU、ITIG 任务上表现强劲，尤其在任务泛化和方面泛化场景下显著优于单任务评估器。
- 其生成的偏好数据可用于 DPO 训练，提升 MLLM（如 LLaVA-Next-7B）和扩散模型（如 SDXL-Turbo）的对齐效果，展示了作为“评估器即数据构造器”的下游价值。

**已知局限**：
1. **图像生成评估性能相对不足**：UFEval 在 IG 任务上的准确率（FRA-OOD 上 69.0%）明显低于 IU（90.4%）和 NLG（81.7%）。论文分析认为这源于底层多模态语言模型在主动视觉语义理解上的不足，而非评估框架本身的设计缺陷。
2. **Harmfulness 判断的过度敏感**：在判断内容有害性时，UFEval 对阴暗或阴沉图像存在系统性误判，倾向于将低亮度场景错误标记为有害内容。
3. **数学推理能力薄弱**：在需要强逻辑推理的任务（如数学问题评估）上表现较差，这是当前多模态语言模型的共性短板。

### 3. 开放问题

- **图像生成评估的改进路径**：能否通过引入更强的视觉编码器或专门的视觉语义对齐训练来弥补 IG 任务的性能差距？
- **方面粒度的优化空间**：更细粒度的方面定义或增加针对性训练数据是否能够减少 Harmfulness 误判？当前方面分类法的层次结构是否足够灵活以容纳新的评估维度？
- **模态扩展的可能性**：UFEval 的方面泛化机制——即通过方面之间的内在关联实现从已知方面到未知方面的迁移——在理论上不依赖特定模态。该框架能否扩展到音频、视频等更多模态的评估任务中？
- **评估器的自我改进循环**：UFEval 已展示了“评估→构造偏好数据→DPO 训练→模型提升”的闭环。是否存在“用提升后的模型生成更难样本→再训练评估器”的迭代改进路径？这需要进一步实验验证。



## 原文 PDF

![[paperPDFs/ICLR_2026/FRABench_and_UFEval_Unified_Fine_grained_Evaluation_with_Task_and_Aspect_Generalization.pdf]]
