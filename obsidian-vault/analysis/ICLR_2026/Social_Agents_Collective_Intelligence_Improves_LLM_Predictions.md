---
title: "Social Agents: Collective Intelligence Improves LLM Predictions"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Social_Agents_Collective_Intelligence_Improves_LLM_Predictions.pdf
project_link: https://behavior-in-the-wild.github.io/social-agents
code_link: null
openreview_forum_id: 73J3hsato3
aliases:
- SA
- SACIILP
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "引入具有多样化人口和心理特征的合成角色代理（persona agents），并独立提示与聚合其预测，以模拟群体决策的多样性、独立性、去中心化和聚合四大支柱。"
primary_logic: "通过构建多样角色并独立提示，LLM 能够采样出内化于训练语料中的多元观点，聚合后抵消个体偏见，实现误差消除和鲁棒性提升，使集体预测更贴近真实人群分布。"
claims:
- "Social Agents 在网页喜爱度预测上显著超越基线，Pearson r 从 0.28 提升至 0.74，相对提升 164%。"
- "在广告点击率预测任务中，Social Agents 将 MAPE 从 72.45% 降至 47.60%（GPT-4o），误差降低约 34%。"
- "Social Agents 具有模型无关性，在 9 个视觉-语言模型上平均比 No-Persona 基线提升 23.9%。"
- "角色间的预测分布差异显著（Wasserstein 距离最高达 0.83），证实结构化的角色多样性是性能提升的关键，而非简单的重复采样。"
---

# Social Agents: Collective Intelligence Improves LLM Predictions

> [!tip] 核心洞察
> 通过构建多样角色并独立提示，LLM 能够采样出内化于训练语料中的多元观点，聚合后抵消个体偏见，实现误差消除和鲁棒性提升，使集体预测更贴近真实人群分布。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Social Agents: 群体智慧提升大语言模型预测 |
| 英文题名 | Social Agents: Collective Intelligence Improves LLM Predictions |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=73J3hsato3) · [Project](https://behavior-in-the-wild.github.io/social-agents) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Social Agents |
| Dataset | Tweet Engagement Prediction, Ad CTR Prediction (Creative industry), Webpage Likability Prediction, Long-Term Video Memorability Prediction |

> [!tip] 效果简介
> - Tweet Engagement Prediction 上，Accuracy (%) 为 86.90 (GPT-4o Social Agents)，对比 70.27 (No-Persona GPT-4o)，变化 +23.68%。
> - Ad CTR Prediction (Creative industry) 上，MAPE (%) 为 47.60 (GPT-4o Social Agents)，对比 72.45 (No-Persona GPT-4o)，变化 -34.3%。
> - Webpage Likability Prediction 上，Pearson r 为 0.74 (GPT-4o Social Agents)，对比 0.28 (No-Persona GPT-4o)，变化 +164.3%。

## 概要

**核心问题**：单一大语言模型（LLM）在预测类任务中输出缺乏人群多样性，其预测分布与真实人类群体的判断存在系统性偏差，尤其在需要多元视角的网页喜爱度、广告点击率等任务上表现不稳定。

**核心方法**：本文提出 **Social Agents** 框架，将群体智慧（Wisdom of Crowds）原则操作化为多智能体系统。通过构建具有多样化人口统计特征（年龄、性别）和心理画像（兴趣、价值观）的合成角色代理（persona agents），独立提示并聚合其预测，以模拟群体决策的多样性、独立性、去中心化和聚合四大支柱。

**核心洞察**：LLM 训练语料中内化了多元社会观点，但单次调用无法有效提取。通过结构化角色提示，模型能够采样出不同人群视角的预测，聚合后个体偏见相互抵消，使集体预测分布更贴近真实人群。

**关键结果**：
- 在网页喜爱度预测上，Social Agents 将 Pearson 相关系数从 0.28 提升至 0.74，相对提升 164%（Table 5）。
- 在广告点击率预测中，平均绝对百分比误差（MAPE）从 72.45% 降至 47.60%，误差降低约 34%（Table 3）。
- 方法具有模型无关性，在 9 个视觉-语言模型上平均比 No-Persona 基线提升 23.9%。
- 消融实验证实，性能提升源于结构化的角色异质性，而非简单的重复采样或温度调节；角色间的预测分布差异显著（Wasserstein 距离最高达 0.83），验证了多样性设计的关键作用（Figure 7）。

**方法定位**：Social Agents 属于提示工程与多智能体聚合的交叉方法，无需任务特定微调，可与任意骨干 LLM 结合使用。相较于传统单次调用或简单多次采样，该方法通过注入结构化社会多样性，在低构念感知判断和高构念推理任务上均展现出显著增益。

大语言模型（LLM）在广泛的行为预测任务中展现出强大的零样本与少样本能力，但单一 LLM 调用存在一个根本性瓶颈：其输出缺乏真实人群的多样性，忽略了群体智慧（Wisdom of Crowds）效应，导致预测分布与真实人群判断之间存在系统性偏差。这一问题在需要多元视角和主观判断的任务中尤为突出——例如预测某则广告的点击率、评估网页的喜爱度或判断视频的长期记忆度时，单一“专家”提示下的 LLM 输出往往仅反映某种平均化的立场，无法捕捉不同人口群体之间的观点异质性。

现有方法的缺口体现在三个层面。其一，标准提示策略将 LLM 视为一个同质的推理引擎，通过领域专家角色或少量示例来引导输出，但未能模拟真实社会中由年龄、性别、兴趣、价值观等维度构成的认知多样性。其二，即便对同一 LLM 进行多次独立调用（如 No-Persona 基线的重复采样），其预测分布也迅速饱和，无法产生结构化的异质判断——这已被消融实验证实：Crowds Within 方法（同一角色多次调用）远弱于 Social Agents（Table 16, Appendix A.7），说明单纯增加推理次数不能替代角色多样性。其三，任务特定的预训练模型（如 LCBM、Henry、Behavior-LLaVA）虽然在各自领域表现优异，但需要大规模标注数据和专项训练，缺乏跨任务的通用性。

本文的核心动机正是弥合这一缺口：能否将群体智慧原则系统性地注入 LLM 的推理过程，使模型能够采样出内化于训练语料中的多元观点，并通过独立聚合来抵消个体偏见？这一思路的理论基础来自 Surowiecki（2004）提出的群体智慧四原则——**观点多样性**（diversity of opinion）、**独立性**（independence）、**去中心化**（decentralization）和**聚合**（aggregation）。Social Agents 框架将这四原则映射为可操作的 LLM 代理机制：通过构建具有多样化人口和心理特征的合成角色（persona agents），让每个角色独立评估刺激并输出定量评分与定性理据，最终聚合为集体预测。其核心洞察在于，LLM 在预训练过程中已经内化了不同人群的认知模式与偏好分布，关键在于设计合适的提示机制来“唤醒”这些潜在的多元视角，而非依赖单一的最优提示。

## 核心方法与创新机理

### 瓶颈洞察：单一 LLM 缺乏群体多样性

单一 LLM 以“领域专家”身份进行预测时，输出本质上是个体判断，忽略了**群体智慧（Wisdom of Crowds）**中多样性、独立性、去中心化和聚合四大支柱。这导致预测分布与真实人群判断之间存在系统性偏差——在需要多元审美、价值观或经验判断的任务中，单次 LLM 调用无法采样到训练语料中内化的多元观点，个体偏见无法通过聚合抵消，预测稳定性不足。

### 核心机制：结构化角色代理 + 独立提示 + 均值聚合

Social Agents 的核心创新在于将群体智慧原则**结构化地注入 LLM 推理流程**，通过三个关键设计槽位的改变实现：

**1. 预测生成单元：从单一专家到 N 个独立角色代理**

基线方法（No-Persona）以单一 LLM 调用生成预测，提示中仅包含任务描述和领域专家身份。Social Agents 则从 **Persona Agent Factory** 中选取具有明确人口统计特征（年龄、性别）和心理画像特征（兴趣、价值观、审美偏好）的合成角色，为每个角色实例化独立的 LLM 代理。每个代理基于其角色立场独立接收提示并生成预测与简短理据，彼此之间完全隔离，确保独立性和去中心化（Figure 2, Section 2）。

**2. 提示构建模板：四段式结构化提示**

提示从基线中的简单任务描述升级为四段式拼接结构（Appendix A.1.1）：

$$P_i = \mathrm{System}(\mathcal{S}) \oplus \mathrm{Persona}(\mathcal{D}_i) \oplus \mathrm{Task}(\mathcal{C}, \mathcal{T}) \oplus \mathrm{Format}(\mathcal{F})$$

其中系统指令定义 LLM 行为边界，角色画像注入人口和心理特征，任务上下文提供刺激材料和目标，格式规范约束输出结构。这一结构化设计使角色信息成为模型推理的**条件变量**而非装饰性前缀，是角色多样性得以生效的关键。

**3. 聚合方式：从无聚合到均值聚合**

基线方法无聚合步骤，直接输出单次预测。Social Agents 对 N 个角色代理的数值输出计算均值作为群体估计：

$$\hat{S} = \frac{1}{N} \sum_{i=1}^{N} s_i$$

消融实验表明，均值聚合在多数任务中优于中位数聚合（CTR 任务 MAPE：47.60 vs 54.96，Table 12），且性能提升源于**角色异质性**而非简单增加推理次数——No-Persona 多次调用迅速饱和，而 Social Agents 在 N≈10 时达到最优（Figure 6, Appendix A.3.3）。

### 决定性证据

角色多样性的因果作用得到了严格验证：

- **跨角色预测分布差异显著**：角色间 Wasserstein 距离最高达 0.83，年龄群体间呈现清晰聚类（Figure 7, Appendix A.3.4），证明结构化角色设计产生了真实的观点多样性，而非表面风格差异。
- **“群内重复”远弱于 Social Agents**：同一角色多次调用（Crowds Within）的性能显著低于不同角色聚合（Table 16, Appendix A.7），确证异质性而非采样次数是性能提升的因果杠杆。
- **模型无关性**：在 9 个视觉-语言模型上，Social Agents 平均比 No-Persona 基线提升 23.9%（Section 3.2, Appendix A.2.1），表明框架不依赖特定模型架构或规模。
- **温度鲁棒性**：CTR 预测 MAPE 在温度 0.3–0.9 范围内仅波动约 0.2 个百分点（Tables 17–18, Appendix A.8），说明性能增益来自角色结构化设计而非随机采样。

### 与现有方法的本质区别

Social Agents 不同于传统集成方法（如多次采样取平均）或多代理辩论框架。其核心差异在于：**角色画像作为先验知识注入**，引导 LLM 从训练语料中采样特定人群的认知分布，而非依赖随机性产生多样性。这使得聚合后的集体预测更贴近真实人群分布——在网页喜爱度预测上，Social Agents 与人类判断分布的 KDE 重叠达 78.4%，远超 No-Persona 基线的 61.5%（Figure 4）。

### 已知局限

该方法存在明确的适用边界：极低参数模型（如 LLaMA 3.1 8B）可能无法充分理解角色画像，导致性能无提升甚至下降（Tables 10–11）；高构念抽象推理任务（如长期视频记忆度）的性能仍落后于专项训练的专家模型 **Henry**（SI et al., 2023），说明群体智慧模拟在需要深层因果推理的任务中面临挑战；情感分类等任务中，角色聚合偶尔引入噪声（Table 9），提示并非所有任务类型同等受益于角色多样性。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_73J3hsato3/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the Social Agents workflow for Ad Click-Through Rate (CTR) Prediction. Given an advertisement (top-left), our framework computes its embeddings and retrieves the top-K semantically similar ads from a repository of ad embeddings. These serve as few-shot examples that aid CTR prediction. A Persona Agent Factory (bottom-left) contains personas defined by demographic attributes (e.g., age, gender) and traits (e.g., interests, occupation), following templates in Appendix Table 2. From this pool, the moderator selects a diverse panel of N personas and instantiates separate LLM agents for each. Each persona agent outputs a CTR percentile (0-100) with a brief rationale. The right-hand s...*

Social Agents 框架将“群体智慧”（Wisdom of Crowds）原则操作化为一个多代理协作系统，其核心思想是：通过构建多样化的人口与心理画像角色代理，独立提示并聚合其预测，使 LLM 能够采样出内化于训练语料中的多元观点，从而抵消个体偏见、逼近真实人群分布。

### 框架总览

整个 pipeline 由五个核心模块串联构成，形成“角色选取 → 独立预测 → 聚合输出”的闭环工作流（Figure 2）。

**1. Persona Agent Factory（角色代理工厂）**  
该模块存储并管理一组预定义的多样化角色画像。每个画像包含人口统计信息（如年龄、性别）和心理特征（如兴趣、价值观、审美偏好），构成角色代理的“身份基础”。论文默认使用 10 个基于年龄与性别交叉构建的角色（Table 2），覆盖从 18-24 岁到 55+ 的不同群体，每个群体配有对应的心理特质描述。

**2. Moderator（协调器）**  
协调器从工厂中选取一组多样化的角色，实例化对应的 LLM 代理，并将目标查询分配给每个代理。它控制整个独立提示流程，确保代理之间无交互、无信息泄露，以严格满足群体智慧所需的“独立性”与“去中心化”条件。

**3. Persona Agents（角色代理）**  
每个角色代理独立接收结构化提示，基于其特定的人口与心理立场对刺激（如广告、网页、视频）进行判断，输出定量预测值（如 CTR 百分位数 0-100）和简短的定性理由。所有代理使用同一骨干 LLM，仅通过角色画像实现条件化差异。

**4. Aggregator（聚合器）**  
聚合器对 N 个角色代理的数值预测进行均值聚合，输出最终的群体评分：

$$\hat{S} = \frac{1}{N} \sum_{i=1}^{N} s_i$$

默认采用均值聚合；消融实验表明，均值在多数任务上优于中位数（如 CTR 任务 MAPE 47.60 vs 54.96，均显著优于 No-Persona 基线的 72.45）。

**5. Collective Rationale Synthesizer（群体理据合成器，可选）**  
该模块将各角色代理的分布式定性理由合成为一段统一的群体解释文本，增强框架的可解释性。此模块为可选组件，不影响核心预测性能。

### 提示构建模板

每个角色代理 $i$ 的完整提示由四段式结构化拼接构成：

$$P_i = \mathrm{System}(\mathcal{S}) \oplus \mathrm{Persona}(\mathcal{D}_i) \oplus \mathrm{Task}(\mathcal{C}, \mathcal{T}) \oplus \mathrm{Format}(\mathcal{F})$$

- **System（系统指令）**：定义代理的角色定位与行为边界。
- **Persona（角色画像）**：注入该代理的人口与心理特征 $\mathcal{D}_i$。
- **Task（任务上下文与目标）**：提供任务描述 $\mathcal{T}$ 及必要的上下文 $\mathcal{C}$（如 5-shot 示例）。
- **Format（输出格式规范）**：约束输出结构，确保预测值与理由的可解析性。

该模板可灵活适配不同任务：仅需修改任务特定组件（Task 与 Format），而保持角色画像描述一致，即可将框架迁移至新的行为预测任务。

### 输入输出流

以广告点击率（CTR）预测为例（Figure 2），完整工作流如下：

1. **输入**：一张广告图像。
2. **嵌入检索**：计算广告的嵌入向量，从广告嵌入库中检索语义最相似的 Top-K 广告作为 few-shot 示例。
3. **角色选取**：协调器从角色工厂中选取 N 个多样化角色（默认 N=10），实例化对应的 LLM 代理。
4. **独立推理**：每个角色代理接收包含 few-shot 示例的结构化提示，独立输出 CTR 百分位数（0-100）及简短理由。
5. **聚合输出**：协调器对各代理预测取均值，生成单一 CTR 百分位数，并与真实 CTR 对比评估。

### 关键设计决策

- **独立提示而非多轮对话**：代理之间零交互，避免“群体思维”（groupthink），确保观点多样性的真实表达。
- **固定角色池而非动态生成**：预定义的角色画像保证了实验的可复现性与角色多样性的一致性；消融实验表明，结构化角色异质性是性能提升的核心驱动因素，而非简单的重复采样（Crowds Within 方法远弱于 Social Agents）。
- **温度鲁棒性**：Social Agents 对采样温度不敏感，CTR MAPE 在 0.3-0.9 温度范围内仅波动约 0.2 个百分点，表明框架的稳定性不依赖于特定的随机性水平。

Social Agents 框架将“群体智慧”原则工程化为五个核心模块，形成一条从角色采样到集体决策的流水线。以下逐一说明各模块功能及其关键公式。

### 1. Persona Agent Factory（角色代理工厂）

工厂存储并管理一组预定义的角色画像，每个画像包含人口统计信息（年龄、性别）和心理特征（兴趣、价值观、审美偏好）。这些画像构成了框架多样性的基础——不同画像对应不同的认知立场与判断倾向，使后续代理能够从异质视角评估同一刺激。论文默认使用 10 个角色（Table 2），覆盖 18–24 至 55+ 五个年龄段与性别组合。

### 2. Moderator（协调器）

协调器从工厂中选取一组多样化角色，为每个角色实例化一个 LLM 代理，并分配目标查询。关键在于协调器确保各代理被**独立提示**——代理之间不存在交互或信息传递，以此满足群体智慧中“独立性”与“去中心化”的要求。

### 3. Persona Agents（角色代理）

每个角色代理接收一个结构化提示，独立生成定量预测 $s_i$ 及简短定性理由。提示由四部分拼接而成：

$$P_i = \mathrm{System}(\mathcal{S}) \oplus \mathrm{Persona}(\mathcal{D}_i) \oplus \mathrm{Task}(\mathcal{C}, \mathcal{T}) \oplus \mathrm{Format}(\mathcal{F})$$

其中：
- $\mathrm{System}(\mathcal{S})$：系统指令，定义代理的通用行为边界；
- $\mathrm{Persona}(\mathcal{D}_i)$：角色 $i$ 的人口与心理画像；
- $\mathrm{Task}(\mathcal{C}, \mathcal{T})$：任务上下文 $\mathcal{C}$ 与目标 $\mathcal{T}$（如“预测该广告的点击率百分位”）；
- $\mathrm{Format}(\mathcal{F})$：输出格式规范，约束代理返回数值预测与理据。

该四段式模板使框架可适配不同任务——仅需修改任务相关组件，角色画像保持一致。

### 4. Aggregator（聚合器）

聚合器对各代理的独立预测进行数值聚合，默认采用均值聚合：

$$\hat{S} = \frac{1}{N} \sum_{i=1}^{N} s_i$$

其中 $N$ 为角色数量，$s_i$ 为第 $i$ 个代理的预测分数，$\hat{S}$ 为最终的群体估计值。消融实验表明，均值聚合在多数任务（CTR 预测、网页喜爱度、记忆度）上优于中位数聚合——例如 CTR 任务中均值 MAPE 为 47.60，中位数为 54.96，均大幅优于 No-Persona 基线的 72.45（Table 12–14）。

### 5. Collective Rationale Synthesizer（集体理据合成器，可选）

该模块将各代理的分布式定性理由合成为一段统一的群体解释文本，增强框架的可解释性。论文未给出其具体实现公式，属于可选增强组件。

### 关键公式补充

实验评估中涉及以下核心指标：

**平均绝对百分比误差（MAPE）**，用于 CTR 与 ROAS 预测：

$$\mathrm{MAPE} = \frac{1}{n} \sum_{i=1}^{n} \left| \frac{A_i - P_i}{A_i} \right| \times 100\%$$

其中 $A_i$ 为真实值，$P_i$ 为预测值。

**皮尔逊相关系数**，用于网页喜爱度预测：

$$r = \frac{\sum_{i=1}^{n} (A_i - \bar{A})(P_i - \bar{P})}{\sqrt{\sum_{i=1}^{n} (A_i - \bar{A})^2} \sqrt{\sum_{i=1}^{n} (P_i - \bar{P})^2}}$$

**斯皮尔曼等级相关系数**，用于长期视频记忆度预测：

$$\rho = 1 - \frac{6 \sum_{i=1}^{n} d_i^2}{n(n^2 - 1)}$$

其中 $d_i$ 为第 $i$ 个样本的预测排序与真实排序之差。

**准确率**，用于推文互动与行为属性分类：

$$\mathrm{Accuracy} = \frac{1}{n} \sum_{i=1}^{n} \mathbf{1}[y_i = \hat{y}_i]$$

## 实验与关键发现

### 核心性能增益

Social Agents 在覆盖低、中、高三个构念水平的 8 项任务上均显著超越 No-Persona 基线。图 3 展示了相对性能对比：Social Agents 在低构念任务上平均提升 42.1%，中等构念任务提升 153%，高构念任务提升 12%。其中网页喜爱度预测的相对提升最为突出，达到 164%。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_73J3hsato3/figures/003_Figure_3.jpg]]
*Figure 3: Performance Comparison of Social Agents (Best Model) over 5-shot Best Model and Models Finetuned on Task-Specific Data across eight tasks. Across eight tasks, Social Agents (Best Model) consistently improve over the 5-shot Best Model and often exceed models finetuned on task-specific data, despite not being trained for those tasks. Here, Best Model refers to whichever base model achieves the strongest results, whether used within Social Agents or in the 5-shot baseline. Performance of Social Agents (Best Model) and finetuned baselines is reported relative to a 5-shot Best Model reference (fixed at 1.00). For Models Finetuned on Task Specific Data, we use: Large Content Behavior Models (LCBM...*

**网页喜爱度预测**（Table 5）是最具代表性的案例。GPT-4o 的 No-Persona 基线仅取得 Pearson r = 0.28，而 Social Agents 将相关性推升至 0.74，相对提升 164.3%。同时，均方根误差（RMSE）和平均百分比误差（MPE）均大幅下降。这一改善的根源在于角色多样性：图 4 的误差分布 KDE 图显示，Social Agents 的预测误差分布与人类判断分布的重叠度达到 78.4%，远高于 No-Persona 基线的 61.5%，说明聚合后的集体判断更贴近真实人群偏好。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_73J3hsato3/figures/009_Table_5.jpg]]
*Table 5: Webpage Likability Prediction. Performance evaluated using Pearson correlation (r, higher is better), Mean Percentage Error (MPE, lower is better), Root Mean Squared Error (RMSE, lower is better), and Accuracy (%, higher is better). Social Agents consistently outperform No-Persona baselines across all metrics. Social Agents outperform the No-Persona baseline across all models, with individual improvements of 74.29% (LLaMA 3.2 90B Vision), 55.26% (Qwen2.5 VL 72B), and 164.29% (GPT-4o). Overall improvement percentages represent the relative improvement of Social Agents over No-Persona (averaged across all models) for each metric. Positive gains are shown in green. Best models are denoted in g...*

**广告点击率预测**（Table 3）同样验证了方法的有效性。在创意和房地产两个行业数据集上，Social Agents 将 GPT-4o 的 MAPE 从 72.45% 降至 47.60%，误差降低约 34.3%。LLaMA 3.3 70B 和 Qwen3 32B 也分别实现了 26.6% 和 23.3% 的平均 MAPE 降幅。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_73J3hsato3/figures/008_Table_3.jpg]]
*Table 3: Ad Click-Through Rate (CTR) Prediction. Results on datasets we constructed from Creative and Real Estate industries listed in the Forbes Fortune 500, evaluated using MAPE (lower is better) and 3-way and 10-way accuracy (higher is better). Social Agents reduce prediction error compared to No-Persona baselines, with average MAPE reductions of 26.6% (LLaMA 3.3 70B), 23.3% (Qwen3 32B), and 32.8% (GPT-4o) across both industries. Compared to LCBM, Social Agents achieve a further 33.2% lower MAPE in the creative industry. We report the average improvements across all metrics: Social Agents compared to No-Persona (averaged over all models) and Social Agents compared to LCBM (averaged over zero-shot...*

**推文互动预测**（Table 4）中，GPT-4o 的 Social Agents 取得了 86.90% 的准确率，较 No-Persona 基线的 70.27% 提升 23.68%，甚至超越了任务特定微调模型 LCBM（Khandelwal et al., 2024）的 85.99%。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_73J3hsato3/figures/007_Table_4.jpg]]
*Table 4: Tweet Engagement Prediction. Performance evaluated using Accuracy (%, higher is better). Social Agents outperform the No-Persona baseline across all models, with individual improvements of 23.68% (GPT-4o), 17.78% (Qwen3 32B), and 23.79% (LLaMA 3.3 70B). Our approach achieves performance closely comparable to that of fine-tuned LCBMs, with Social Agents (GPT-4o) surpassing the average LCBM performance by 1.92% (averaged across both variants). Positive gains are shown in green. Best models are denoted in green , and runner-ups in blue*

**长期视频记忆度预测**（Table 7）作为高构念任务，Social Agents（GPT-4o）取得了 Spearman ρ = 0.41，优于 No-Persona 基线的 0.33（提升 24.2%），但仍落后于专项训练的 Henry 模型（SI et al., 2023），说明抽象推理任务对群体智慧模拟的挑战更大。

**行为属性分类**（Table 9）中，Social Agents 在主题、情感、说服、动作、原因五个维度上均有提升，其中原因分类准确率从 76.92% 提升至 85.71%（+11.4%），且以零样本方式大幅超越微调模型 Behavior-LLaVA（Singh et al., 2025）。

### 模型无关性

Social Agents 的增益不依赖于特定模型架构或规模。在 9 个视觉-语言模型上的测试表明，Social Agents 平均比 No-Persona 基线提升 23.9%。从 GPT-4o 到 LLaMA 3.3 70B、Qwen3 32B，所有测试模型均一致受益。但存在模型尺度下限：Table 10 和 Table 11 显示，极低参数模型如 LLaMA 3.1 8B 未能从 Social Agents 中稳定获益，表明角色理解能力需要一定的模型容量支撑。相比之下，Qwen2.5 VL 7B 仍能获得明显提升，说明模型架构和训练数据的质量同样重要。

### 消融实验：多样性而非重复采样

性能提升的核心驱动力是结构化的角色异质性，而非简单地增加推理调用次数。图 6 展示了关键消融结果：

- **No-Persona 多次调用迅速饱和**：在 CTR 和网页喜爱度两个任务上，No-Persona 基线在 5-10 次调用后性能即趋于平稳。
- **Social Agents 在 N≈10 时达到最优**：随着角色数量增加，性能持续提升，在约 10 个角色时接近饱和，20-30 个角色时达到最佳 MAPE。

这一发现被 Table 16 进一步证实：Crowds Within（同一角色多次调用）方法远弱于 Social Agents，直接证明角色间的异质性才是群体智慧生效的关键机制。

图 7 的角色间预测分歧热力图提供了更微观的证据。不同年龄和性别角色的预测分布间存在显著差异，Wasserstein 距离最高达 0.83，且呈现按年龄聚类的模式——相邻年龄组分歧较小，年轻女性与年长男性组之间分歧最大。这证实角色画像确实诱导出了结构化的认知差异，而非表面风格变化。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_73J3hsato3/figures/019_Figure_7.jpg]]
*Figure 7: Inter-Persona Prediction Divergence on the Webpage Likability Prediction task. The heatmap shows clear clustering by age, with adjacent age groups exhibiting lower divergence (lighter cells along the diagonal) and sharp separations between younger females and older male groups (darkest cells, up to 0.83). Divergences between male and female personas within the same age bracket are comparatively smaller. Each cell reports the pairwise Wasserstein distance between predicted webpage-likability prediction distributions for GPT-4o when prompted with personas from different age and gender groups, where larger values indicate greater divergence in predictions*

### 聚合策略与鲁棒性

默认的均值聚合在多数任务上优于中位数聚合。Table 12 显示，在 CTR 预测任务上，均值聚合的 MAPE 为 47.60%，优于中位数聚合的 54.96%（但两者均大幅优于基线 72.45%）。网页喜爱度和记忆度预测任务上也呈现类似趋势（Table 13、Table 14）。

Social Agents 对温度参数表现出极强的鲁棒性。Table 17 和 Table 18 显示，在 0.3 至 0.9 的温度范围内，CTR 预测的 MAPE 仅波动约 0.2 个百分点，记忆度预测的 Spearman ρ 稳定在 0.41。这一特性降低了超参数调优的负担。

### 公平性分析

图 5 揭示了值得关注的公平性问题：女性角色预测与人类判断的相关性略高于同龄男性角色；年轻群体（18-24 岁）的相关性最强（r 最高 0.71），而 55 岁以上群体的相关性骤降至 0.22-0.25。这一趋势很可能反映了 LLM 训练数据中老年群体覆盖不足的问题。当前角色池以年龄和性别为主要维度，尚未充分涵盖种族、社会经济地位等敏感属性，可能限制预测的公平性。

### 失败模式

并非所有任务均等受益于角色多样性。情感分类的某些子任务中，Social Agents 的表现出现下降，角色聚合可能引入了额外噪声。此外，高构念任务（如长期视频记忆度）的绝对性能仍落后于专项训练的专家模型，表明抽象推理任务对群体智慧模拟具有天然挑战。低参数模型的失效案例（LLaMA 8B/11B）也提示该方法存在模型容量门槛。

## 定位与知识库关联

### 与现有基线的结构化关系

**Social Agents** 的核心贡献在于将群体智慧原则系统性地注入 LLM 预测流程，其方法定位可从以下对比维度加以理解：

- **vs. No-Persona 基线（单次专家提示）**：这是全文最主要的对比对象。No-Persona 以领域专家身份单次调用 LLM，输出单一预测，完全缺乏人群多样性。Social Agents 将预测生成单元从单一调用替换为 N 个独立角色代理，并通过均值聚合抵消个体偏见。在网页喜爱度预测上，Pearson r 从 0.28 跃升至 0.74（相对提升 164%）；在广告 CTR 预测上，MAPE 从 72.45% 降至 47.60%（误差降低约 34%）。关键消融实验证实，性能提升源于结构化的角色异质性，而非简单的推理次数增加——No-Persona 多次调用迅速饱和，而 Social Agents 在 N≈10 时达到最优（Figure 6, Appendix A.3.3）。

- **vs. Crowds Within（同一角色多次调用）**：该方法对同一无角色 LLM 进行多次采样并聚合，模拟“人群内部”的随机性。Social Agents 在所有任务上显著优于 Crowds Within（Table 16, Appendix A.7），证明角色画像带来的结构化异质性是性能增益的核心驱动力，而非温度采样引入的随机波动。

- **vs. 任务特定微调模型**：Social Agents 在多个任务上展现出与专项训练模型竞争甚至超越的能力。在推文互动预测中，GPT-4o Social Agents（86.90% 准确率）超越微调模型 **LCBM**（Khandelwal et al., 2024）的 85.99%；在长期视频记忆度预测中，Social Agents（Spearman ρ=0.41）仍落后于专项模型 **Henry**（SI et al., 2023）的 ρ=0.47，表明高构念抽象推理任务对群体智慧模拟更具挑战。在行为属性分类中，Social Agents 以零样本方式超越微调模型 **Behavior-LLaVA**（Singh et al., 2025）高达 55.3 个百分点（Table 9）。

- **vs. 传统机器学习基线**：在 ROAS 和网页喜爱度预测中，Social Agents 同样优于 **XGBoost** 等传统方法，验证了群体智慧框架在结构化预测任务上的通用优势。

### 适用边界与局限

尽管 Social Agents 在多数任务上表现强劲，其适用边界已通过系统消融得到初步刻画：

1. **模型尺度下限**：小模型（如 Qwen2.5 VL 7B）仍可从 Social Agents 获益，但极低参数模型（LLaMA 3.1 8B）可能无法充分理解角色画像，导致性能无提升甚至下降（Tables 10-11, Appendix A.3.1）。这暗示角色提示机制存在模型能力阈值。

2. **任务构念水平的调节效应**：Social Agents 在低构念任务（如 CTR 预测，MAPE 降低 34.3%）和中构念任务（如网页喜爱度，Pearson r 提升 164%）上增益最大，而在高构念任务（如长期视频记忆度，Spearman ρ 仅从 0.33 提升至 0.41）上增益相对有限。抽象推理任务对群体智慧模拟的响应较弱，可能因为角色画像主要捕捉偏好多样性而非推理多样性。

3. **任务类型的适用性分化**：情感分类等任务中，部分 LLM 配置下 Social Agents 表现下降，角色多样性可能引入噪声（见 fairness_notes）。并非所有预测任务都同等受益于角色聚合——当任务本身不依赖多元主观判断时，角色多样性可能成为干扰源。

4. **角色池覆盖的局限性**：当前角色池仅以年龄和性别为主要维度，未充分涵盖种族、社会经济地位等敏感属性。公平性分析显示，年轻群体（18-24）的预测与人类判断相关性最强（r 最高 0.71），而 55+ 群体相关性降至 0.22-0.25，反映训练数据中老年群体覆盖不足（Figure 5）。这可能限制预测在特定人口群体上的公平性。

5. **实验设置的约束**：所有实验在 5-shot 设置下进行，且未与真实人群分布校准。更大规模的示例检索或人口加权聚合可能带来额外增益，但尚未探索。

### 开放问题

Social Agents 框架开辟了若干值得深入探索的方向：

- **角色画像的系统设计方法论**：当前 10 个角色基于年龄和性别的手工设计，如何系统性地构建角色池以最大化群体智慧效应？角色数量、组合方式与任务构念水平之间的最优关系仍不明确。Figure 6 显示性能在 N≈20-30 时趋于饱和，但这是否适用于所有任务类型尚无定论。

- **与真实人口分布的校准**：Social Agents 能否与真实世界的人口统计分布（如收入、教育、地域）进行加权校准，以进一步提升预测的准确性与公平性？当前均值聚合隐含假设所有角色等权重，这可能偏离实际人群结构。

- **跨模型与跨模态的通用性**：虽然已在 9 个视觉-语言模型上验证模型无关性（平均提升 23.9%），但在更广泛的开源/闭源 LLM 以及其他多模态任务（如视频问答、风险预测）上的通用性仍需系统评估。

- **角色提示的内在机理**：LLM 是否真正捕捉到了对应人群的认知模式，还是仅产生了表面风格差异？Figure 7 显示角色间预测分布差异显著（Wasserstein 距离最高达 0.83），且呈现按年龄聚类的模式，这暗示角色提示确实触发了深层表征差异，但其认知机制仍需进一步解构。

- **动态与交互式扩展**：当前框架为静态单轮预测，能否扩展到实时交互式决策或在线学习场景？例如，利用流式反馈动态调整角色权重，或引入角色间的受控交互以模拟社会讨论过程，可能进一步丰富群体智慧的模拟维度。

## 原文 PDF

![[paperPDFs/ICLR_2026/Social_Agents_Collective_Intelligence_Improves_LLM_Predictions.pdf]]
