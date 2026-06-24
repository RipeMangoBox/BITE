---
title: "Inverse Reinforcement Learning with Dynamic Reward Scaling for LLM Alignment"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Inverse_Reinforcement_Learning_with_Dynamic_Reward_Scaling_for_LLM_Alignment.pdf
openreview_forum_id: K0Zh6mzTzc
aliases:
- DI
- IRLDRSLA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "动态奖励缩放机制，通过数据层面的语义相似度（数据硬度）和模型层面的奖励间隙（模型响应性）自适应地调整训练样本的权重，将优化重点放在困难且具有较高不确定性的样本上。"
primary_logic: "利用均衡的安全示范数据集通过逆强化学习(IRL)训练类别特定的影子奖励模型，并在组相对策略优化(GRPO)过程中引入基于数据硬度和模型响应性的动态奖励权重，能够显著提升LLM的安全对齐性能，同时维持甚至改善有用性。"
claims:
- "DR-IRL 在安全性 benchmark 上一致超过所有基线方法，同时保持或提高有用性。"
- "在七个有害类别中，DR-IRL 的拒绝率在每一个类别上都达到最高。"
- "去除所有硬度系数会导致 StrongReject 分数下降约 4 个百分点，验证了动态权重机制的关键作用。"
- "StrongReject (Llama-3.1-8B) 上 score = 0.9361"
---

# Inverse Reinforcement Learning with Dynamic Reward Scaling for LLM Alignment

> [!tip] 核心洞察
> 利用均衡的安全示范数据集通过逆强化学习(IRL)训练类别特定的影子奖励模型，并在组相对策略优化(GRPO)过程中引入基于数据硬度和模型响应性的动态奖励权重，能够显著提升LLM的安全对齐性能，同时维持甚至改善有用性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向大语言模型对齐的基于动态奖励缩放的逆向强化学习 |
| 英文题名 | Inverse Reinforcement Learning with Dynamic Reward Scaling for LLM Alignment |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=K0Zh6mzTzc) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | DR-IRL |
| Dataset | StrongReject (Llama-3.1-8B), XsTest (Llama-3.1-8B), WildChat (Llama-3.1-8B), StrongReject (Qwen-2-7B) |

> [!tip] 效果简介
> - StrongReject (Llama-3.1-8B) 上，score 为 0.9361，对比 0.8105 (GRPO)，变化 +0.1256。
> - XsTest (Llama-3.1-8B) 上，refusal rate 为 99.00%，对比 91.50% (GRPO)，变化 +7.50%。
> - WildChat (Llama-3.1-8B) 上，refusal rate 为 74.21%，对比 55.61% (GRPO)，变化 +18.60%。

## 概述

当前大语言模型（LLM）的安全对齐面临两个关键瓶颈：**安全数据集类别严重不平衡**，长尾威胁样本被主流方法忽视；**标准奖励模型是静态的**，不感知任务难度，导致优化效率低下，无法充分发挥对齐潜力。DR-IRL 针对这两个问题提出了一套统一解决方案。

**核心洞察**：利用均衡的安全示范数据集，通过逆强化学习（IRL）训练类别特定的影子奖励模型，并在组相对策略优化（GRPO）过程中引入基于数据硬度和模型响应性的动态奖励权重，能够显著提升 LLM 的安全对齐性能，同时维持甚至改善有用性。

**方法定位**：DR-IRL 在三个关键维度上区别于现有对齐方法——奖励模型从静态单一模型升级为七个类别特定的影子奖励模型（IRL 训练）；优势函数从标准 GRPO 组内归一化升级为引入联合硬度系数 α_{ji} = α_{ji}^D · α_j^M 的动态缩放；训练数据从偏好数据集替换为自动生成的均衡 CoD 安全示范数据集。

**主要结果**：在 Llama-3.1-8B 上，DR-IRL 的 StrongReject 分数达到 0.9361，相比 GRPO 提升 12.56 个百分点；在 Qwen-2-7B 上，StrongReject 分数从 0.5155 跃升至 0.8798，增幅达 36.43 个百分点。在七个有害类别中，DR-IRL 的拒绝率在每一个类别上都达到最高。消融实验证实，去除所有硬度系数会导致 StrongReject 分数下降约 4 个百分点，验证了动态权重机制的关键作用。

## 背景与动机

### 大语言模型安全对齐的核心瓶颈

大语言模型（LLM）在广泛部署中面临严峻的安全挑战，对齐技术旨在使模型行为符合人类价值与安全规范。当前主流的对齐范式——如基于人类反馈的强化学习（RLHF）和直接偏好优化（DPO）——虽然在有用性上取得了显著进展，但在安全性维度上仍存在两个根本性的结构缺陷。

**第一个瓶颈是安全训练数据的类别失衡。** 现有的偏好数据集和安全语料库通常呈现严重的长尾分布：常见的有害类别（如仇恨言论）获得大量标注样本，而罕见但高危的威胁类别（如生物安全、隐私侵犯）则样本稀疏。这种不平衡导致奖励模型和安全策略对长尾威胁的识别能力不足，在实际部署中形成可被利用的薄弱环节。Figure 1 直观地对比了现有对齐方法在这一问题上的局限——静态的、基于非均衡数据训练的奖励模型难以覆盖多样化的安全边界。

**第二个瓶颈是标准奖励模型的静态性。** 传统对齐方法使用固定的奖励模型对所有训练样本赋予统一的优化信号，完全忽略了任务难度的差异。这意味着模型在简单样本（如已能正确拒绝的常规有害提示）和困难样本（如需要微妙判断的对抗性提示）上获得相同的优化力度，导致训练效率低下：大量计算资源浪费在模型已经掌握的简单样本上，而真正需要突破的困难样本却得不到充分学习。这种静态奖励机制从根本上限制了对齐潜力的释放。

### 现有方法的缺口

近期的对齐研究尝试从多个角度解决上述问题。**GRPO**（Shao et al., 2024）通过组内相对比较消除了对显式价值函数的需求，但依然依赖静态奖励模型。**STAIR**（Zhang et al., 2025）引入了安全感知的过程奖励，但仍未解决数据失衡和难度自适应的问题。**SACPO**（Wachi et al., 2024）尝试分步优化安全约束，但其优化目标中任务难度仍然是隐式的。这些方法的共同缺口在于：它们要么忽视了训练数据的类别均衡性，要么缺乏根据任务难度动态调整优化信号的机制。

### 本文动机

针对上述双重瓶颈，本文提出了一种全新的对齐框架 **DR-IRL**（Dynamic Reward scaling via Inverse Reinforcement Learning）。核心动机源于两个关键洞察：

1. **均衡的示范数据替代偏好标注。** 通过逆强化学习（IRL），可以利用精心构建的、覆盖七个有害类别的均衡安全示范数据集来训练类别特定的影子奖励模型，从而从根本上解决长尾威胁被忽视的问题。与依赖昂贵偏好标注的传统方法不同，IRL 直接从专家示范中推断奖励函数，更忠实地捕捉人类安全价值。

2. **动态奖励缩放实现难度自适应优化。** 在 GRPO 优化过程中，引入基于数据硬度和模型响应性的动态奖励权重。数据硬度通过文本编码器衡量生成回复与示范回复的语义相似度，识别内容层面的困难样本；模型响应性通过影子奖励模型的奖励间隙评估模型对特定样本的区分能力。两者以乘积形式联合作用，确保只有那些内容上困难且模型高度不确定的样本才会被重点优化，从而实现高效的难度自适应对齐。

## 核心创新

DR-IRL 的核心创新在于将**逆强化学习（IRL）**与**动态奖励缩放**相结合，针对当前 LLM 安全对齐中的两个关键瓶颈——安全数据集类别不平衡和静态奖励模型——提出了系统性的改进方案。

### 关键改进槽位

**1. 奖励模型：从静态单一模型到类别特定的影子奖励模型**

传统对齐方法（如 GRPO、PPO）依赖单一的静态奖励模型，该模型通常基于偏好数据训练，将异构的安全意图压缩为单一标量，导致奖励信号相互干扰。DR-IRL 替换为**七个类别特定的影子奖励模型**，每个模型通过最大似然逆强化学习（ML-IRL）在均衡的 Chain-of-Draft（CoD）安全示范数据集上独立训练。这一设计使得每个影子奖励模型专注于单一有害类别（如侮辱、犯罪、隐私侵犯等），从而锐化奖励间隙并稳定 GRPO 的优化过程。

**2. 优势缩放：从标准组归一化到联合硬度系数动态加权**

标准 GRPO 仅对组内奖励进行归一化处理，不做额外的难度感知加权。DR-IRL 引入**联合硬度系数** $\alpha_{ji} = \alpha_{ji}^D \cdot \alpha_j^M$，从两个维度动态缩放组优势函数：

- **数据硬度** $\alpha_{ji}^D$：通过文本编码器计算生成回复与示范回复的余弦相似度，量化样本本身的难易程度。相似度越高，样本越容易，系数越大。
- **模型响应性** $\alpha_j^M$：利用影子奖励模型的奖励间隙衡量模型当前对数据的区分能力。模型对某类样本的奖励间隙越大，说明其区分能力越强，响应性系数越大。

乘积形式实现了严格的 AND 门控——只有内容上困难（$\alpha^D$ 小）且模型不确定（$\alpha^M$ 小）的样本才会被显著强调，从而将优化重点集中在高价值样本上。

**3. 训练数据：从偏好数据集到均衡的 CoD 安全示范数据集**

传统方法依赖偏好标注数据（如 UltraFeedback、SafeRLHF），存在类别不平衡问题，长尾威胁类别通常被忽视。DR-IRL 使用 LLM 自动生成覆盖七个有害类别的均衡 CoD 拒绝示范数据集，作为 IRL 训练的示范数据。CoD 提示相比 CoT 在保证准确性的同时大幅减少 token 消耗和推理延迟（Qwen-2-7B 上 token 从 1,289 降至 162），使得大规模生成均衡安全数据成为可能。

### 创新机制的核心逻辑

DR-IRL 的因果链条可概括为：**均衡的类别特定示范数据 → 类别特定影子奖励模型 → 数据硬度与模型响应性双维度难度估计 → 动态缩放的组优势函数 → 聚焦困难且不确定样本的 GRPO 优化**。这一设计同时解决了数据层面（类别不平衡）和优化层面（静态奖励、无难度感知）的双重瓶颈，从而在安全性与有用性之间实现了更优的权衡。

## 整体框架

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_K0Zh6mzTzc/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of DR-IRL. First, we construct a balanced safety dataset covering N harm categories through designed CoD prompt templates. Next, we train a specialized shadow reward model for each category, using this dataset as demonstration data. Finally, we use these reward models to align the LLM via GRPO, dynamically scaling optimization by task difficulty at both data and model level—measuring data hardness with text encoder cosine similarity and model responsiveness with reward gaps*

DR-IRL 的整体流水线由三个顺序耦合的模块构成：**均衡安全示范数据构建 → 类别特定影子奖励学习 → 动态难度感知的 GRPO 优化**。图 2 给出了完整的端到端架构示意。

**数据构建层**：针对现有安全数据集中长尾威胁类别被忽视的问题，DR-IRL 首先通过设计的 Chain-of-Draft (CoD) 提示模板，自动生成覆盖七个有害类别的均衡拒绝示范数据集。该数据集作为后续逆强化学习的示范信号，替代了传统方法中昂贵的人工偏好标注。

**奖励建模层**：在获得均衡示范数据后，DR-IRL 为每个有害类别独立训练一个影子奖励模型。训练采用最大似然逆强化学习（ML-IRL）框架，其核心是一个双层优化问题——上层最大化示范数据的对数似然，下层在学到的奖励函数下优化策略：

$$
\begin{array}{rl} \underset{\theta}{\mathrm{max}} \ell(\theta) := \mathbb{E}_{(x,y)\sim\mathcal{D}}[\log\pi_{\theta}(y|x)] \quad \mathrm{s.t.} \ \pi_{\theta} := \mathrm{argmax}_{\pi} \mathbb{E}_{x\sim\mathcal{H},y\sim\pi(\cdot|x)}\big[r(x,y;\theta) - \beta D_{\mathrm{KL}}(\pi(\cdot|x)||\pi_{\mathrm{ref}}(\cdot|x))\big], \end{array}
$$

该问题可等价转化为极小极大形式，通过对比真实示范响应与生成响应的奖励差异来优化：

$$
\operatorname* {max}_{\theta}\operatorname* {min}_{\pi}\mathbb{E}_{(x,y)\sim\mathcal{D},\widetilde{y}\sim\pi(\cdot|x)}\bigg[\frac{r(x,y;\theta)-r(x,\widetilde{y};\theta)}{\beta}+D_{\mathrm{KL}}(\pi(\cdot|x)\|\pi_{\mathrm{ref}}(\cdot|x))\bigg]
$$

类别特定的影子奖励模型设计（7RW）在相近计算预算下显著优于单一共享奖励模型——单一模型将异质安全意图压缩为单一标量，产生奖励干扰；而类别专用模型则能锐化奖励间隙，稳定 GRPO 更新过程。

**动态优化层**：在 GRPO 的组相对策略优化框架中，DR-IRL 引入了联合硬度系数 $\alpha_{ji}$ 对优势函数进行动态缩放。该系数由两个正交维度构成：

- **数据硬度 $\alpha_{ji}^D$**：通过文本编码器计算生成回复与示范回复的余弦相似度，量化样本内容层面的难易程度。值越大表示样本越容易，模型对该样本的置信度越高：

$$\alpha_{ji}^D = \frac{\sigma(\delta_{ji})}{\sigma(\bar{\delta}_j)}, \quad \delta_{ji}=1-W_{ji}$$

- **模型响应性 $\alpha_j^M$**：利用影子奖励模型的奖励间隙，过滤异常值后衡量模型当前对数据的区分能力：

$$\alpha_j^M = \frac{\sigma(\bar{\mathcal{R}}_{\mathcal{P}_j^{\theta}})}{\sigma(\bar{\mathcal{R}}_j)}$$

两者以乘积形式组合 $\alpha_{ji} = \alpha_{ji}^D \cdot \alpha_j^M$，构成严格的 AND 门控——只有内容上困难**且**模型当前不确定的样本才会被强调，从而将优化重心聚焦于最具学习价值的区域。最终，缩放后的组优势函数为：

$$A_i^j = \alpha_j(q) \cdot \frac{R_{j,i} - \operatorname*{mean}(\{R_{j,1},R_{j,2},\dots,R_{j,G}\})}{\mathrm{std}(\{R_{j,1},R_{j,2},\dots,R_{j,G}\})}$$

该流水线的关键因果机制在于：均衡示范数据解决了长尾威胁的覆盖问题，类别特定奖励模型消除了跨类别的奖励干扰，而动态硬度缩放则将优化资源从已掌握的简单样本重新分配至困难且高不确定性的样本，三者协同实现了安全-有用性前沿的一致推进。

## 核心模块与公式推导

DR-IRL 的核心由三个递进模块构成：**影子奖励学习**、**双维度硬度测量**、**动态优势缩放**。以下逐一展开其关键公式与变量含义。

### 3.1 影子奖励学习：最大似然逆强化学习

DR-IRL 用逆强化学习（IRL）替代传统偏好标注训练静态奖励模型。具体而言，针对 7 个有害类别分别构建均衡的 Chain-of-Draft（CoD）安全示范数据集，通过最大似然 IRL 框架训练类别特定的影子奖励模型。其双层优化问题为：

$$
\begin{array}{rl} \underset{\theta}{\mathrm{max}} \ell(\theta) := \mathbb{E}_{(x,y)\sim\mathcal{D}}[\log\pi_{\theta}(y|x)] \quad \mathrm{s.t.} \ \pi_{\theta} := \mathrm{argmax}_{\pi} \mathbb{E}_{x\sim\mathcal{H},y\sim\pi(\cdot|x)}\big[r(x,y;\theta) - \beta D_{\mathrm{KL}}(\pi(\cdot|x)||\pi_{\mathrm{ref}}(\cdot|x))\big] \end{array}
$$

其中 $\mathcal{D}$ 为安全示范数据集，$\mathcal{H}$ 为有害提示分布，$r(x,y;\theta)$ 是参数化奖励函数，$\beta$ 控制 KL 惩罚强度，$\pi_{\mathrm{ref}}$ 为参考策略。上层最大化示范数据的对数似然，下层在奖励约束下优化策略，二者通过奖励函数 $\theta$ 耦合。

为便于优化，该问题可转化为等价的极小极大形式：

$$
\operatorname* {max}_{\theta}\operatorname* {min}_{\pi}\mathbb{E}_{(x,y)\sim\mathcal{D},\widetilde{y}\sim\pi(\cdot|x)}\bigg[\frac{r(x,y;\theta)-r(x,\widetilde{y};\theta)}{\beta}+D_{\mathrm{KL}}(\pi(\cdot|x)\|\pi_{\mathrm{ref}}(\cdot|x))\bigg]
$$

该形式的核心机制是**对比真实示范响应 $y$ 与策略生成响应 $\widetilde{y}$ 的奖励差**，驱动奖励模型学习区分安全与有害回复。

### 3.2 双维度硬度测量

DR-IRL 从数据层面和模型层面分别量化任务难度，形成联合硬度系数。

**数据硬度（Data Hardness）** 衡量生成回复与示范回复的语义差异。给定提示 $q$，策略生成响应 $S_{ji}$，示范响应 $\widetilde{S}_{ji}$，通过文本编码器 $\Phi$ 计算子句级余弦相似度：

$$
s_{k,l} = \cos(\Phi(S_{ji}^k), \Phi(\widetilde{S}_{ji}^\ell))
$$

取每个子句的最大匹配相似度并求均值，得到整体相似度 $W_{ji}$：

$$
W_{ji} = \frac{1}{K} \sum_{k=1}^{K} s_k^{\max}, \quad s_k^{\max} = \max_{1 \leq \ell \leq L} s_{k,l}
$$

定义差异度 $\delta_{ji}=1-W_{ji}$，数据硬度系数 $\alpha_{ji}^D$ 为归一化后的差异度：

$$
\alpha_{ji}^D = \frac{\sigma(\delta_{ji})}{\sigma(\bar{\delta}_j)}
$$

其中 $\sigma$ 为 sigmoid 函数，$\bar{\delta}_j$ 为组内平均差异度。$\alpha_{ji}^D$ 越大表示样本越容易（高置信度、低不确定性），越小表示样本越困难。

**模型响应性（Model Responsiveness）** 评估模型当前对数据的区分能力。定义奖励间隙 $\mathcal{R}_{ji}$ 为影子奖励模型对生成响应与示范响应的评分差。先通过方差阈值 $\tau$ 过滤异常值：

$$
\mathcal{M}_{ji} = \left\{ \begin{array}{ll} {1,} & {(\mathcal{R}_{ji} - \bar{\mathcal{R}}_{j})^2 \leq \tau} \\ {0,} & {(\mathcal{R}_{ji} - \bar{\mathcal{R}}_{j})^2 > \tau} \end{array} \right.
$$

过滤后的平均奖励间隙为：

$$
\bar{\mathcal{R}}_{\mathcal{P}_j^{\theta}} = \frac{1}{M - T} \sum_{i=1}^{M} \mathcal{M}_{ji} \bar{\mathcal{R}}_{ji}
$$

模型响应性系数定义为过滤后与原始奖励间隙的 sigmoid 比值：

$$
\alpha_j^M = \frac{\sigma(\bar{\mathcal{R}}_{\mathcal{P}_j^{\theta}})}{\sigma(\bar{\mathcal{R}}_j)}
$$

$\alpha_j^M$ 越大表示模型对当前提示组的区分能力越强，即模型响应性越高。

**联合硬度系数** 采用乘积组合，实现严格的 AND 门控——只有内容上困难且模型不确定的样本才会被强调：

$$
\alpha_{ji} = \alpha_{ji}^D \cdot \alpha_j^M
$$

### 3.3 动态优势缩放

在 GRPO 优化阶段，将联合硬度系数注入组优势函数，实现动态奖励缩放。对于第 $j$ 个提示的第 $i$ 个响应，缩放后的优势为：

$$
A_i^j = \alpha_j(q) \cdot \frac{R_{j,i} - \operatorname*{mean}(\{R_{j,1},R_{j,2},\dots,R_{j,G}\})}{\mathrm{std}(\{R_{j,1},R_{j,2},\dots,R_{j,G}\})}
$$

其中 $R_{j,i}$ 为影子奖励模型打分，分子为组内去均值归一化，$\alpha_j(q)$ 为提示 $q$ 对应的联合硬度系数。该设计使困难样本获得更大的优势权重，引导策略优先学习高价值的安全拒绝行为，同时避免在已充分掌握的简单样本上过度优化。

## 实验与分析

### 安全-有用性前沿推进

DR-IRL 在两个模型家族上一致推进了安全-有用性前沿。Table 1 显示，在 Llama-3.1-8B 上，DR-IRL 取得最高 StrongReject 分数 0.9361，较 GRPO 基线提升 0.1256；WildChat 拒绝率达到 74.21%，提升 18.60 个百分点；XsTest 拒绝率 99.00%，提升 7.50 个百分点。在 Qwen-2-7B 上，StrongReject 从 GRPO 的 0.5155 跃升至 0.8798（+0.3643），GSM8k 有用性指标同时从 82.87% 提升至 89.70%（+6.83%）。这表明动态奖励缩放机制不仅强化了安全拒绝能力，还通过优化聚焦改善了推理性能。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_K0Zh6mzTzc/figures/003_Table_1.jpg]]
*Table 1: Comparison of DR-IRL and baseline methods on 4 harmlessness and 4 helpfulness benchmarks*

Figure 3 展示了七个有害类别上的逐类拒绝率：DR-IRL 在每一个类别上都达到最高或竞争性最高拒绝率，验证了类别特定的影子奖励模型对长尾威胁类别的有效覆盖。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_K0Zh6mzTzc/figures/005_Figure_3.jpg]]
*Figure 3: Category-wise refusal rates across 7 types of harmful prompts. DR-IRL consistently achieves higher or competitive refusal accuracy compared to baselines*

### 动态硬度系数的消融分析

Figure 4 揭示了硬度系数的因果作用。去除所有硬度系数（No Hardness）导致 StrongReject 分数下降约 4 个百分点，直接验证了动态权重机制的关键贡献。进一步分解显示：

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_K0Zh6mzTzc/figures/008_Figure_4.jpg]]
*Figure 4: Ablation on hardness coefficients (Llama-3.1-8B)*

- **数据硬度项 α^D**：主要提升拒绝精度。抑制该项主要损害安全指标，说明文本编码器余弦相似度有效识别了内容层面的难易样本。
- **模型响应性项 α^M**：主要稳定通用能力。去除该项导致有用性指标出现较大波动，表明奖励间隙过滤机制对维持模型在非安全任务上的表现至关重要。

Table 3 比较了乘积组合规则与加权和变体。乘积形式（α^D·α^M）在所有模型-指标组合上均取得最高分，验证了 AND 门控设计的有效性——只有内容上困难且模型不确定的样本才会被强调，从而稳定了 GRPO 更新过程。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_K0Zh6mzTzc/figures/007_Table_3.jpg]]
*Table 3: Product vs. weighted-sum hardness combination. Higher is better for all three metrics*

### 类别特定影子奖励模型的价值

Table 2 在相似计算预算下对比了单一奖励模型与七个类别特定影子奖励模型。7RW 方案（约 120 GPU 小时）在所有四个安全基准上均显著优于单一 RW（约 100 GPU 小时）：StrongReject 从 0.9182 提升至 0.9361，WildChat 从 71.68% 提升至 74.21%。这一结果支持了核心设计选择：单一奖励模型将异质安全意图压缩为单一标量会导致奖励干扰，而类别特定模型则锐化了奖励间隙并稳定了策略更新。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_K0Zh6mzTzc/figures/006_Table_2.jpg]]
*Table 2: Single vs. per-category shadow reward models under similar compute*

### 越狱攻击鲁棒性

Table 4 展示了三种越狱攻击下的拒绝率。DR-IRL 在 AutoDAN（59.00%）、GCG（96.98%）和 DRA（64.92%）上均取得最高拒绝率，相比 STAIR 基线在 AutoDAN 上提升超过 30 个百分点。这表明通过逆强化学习从均衡安全示范中学习的影子奖励模型，对未见过的对抗攻击模式具有更强的泛化拒绝能力。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_K0Zh6mzTzc/figures/009_Table_4.jpg]]
*Table 4: Refusal rates (%) under three jailbreak attack methods (higher is better) on LLaMA-3.1 8B*

### 难度加权机制的通用性

Table 5 验证了动态硬度系数可迁移至其他对齐方法。将难度加权应用于 DPO（DPO-S）和 PPO（PPO-S）后，两者在 StrongReject、XsTest 和 WildChat 上均一致超越原始基线。这表明数据硬度和模型响应性的联合度量作为一种通用优化策略，不依赖于特定的 GRPO 框架。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_K0Zh6mzTzc/figures/010_Table_5.jpg]]
*Table 5: Effect of difficulty-weighted updates across methods (WildChat is refusal rate, higher is better)*

### 失败模式与局限性

尽管 DR-IRL 在安全指标上表现突出，仍存在以下局限：

1. **计算开销**：每类单独训练影子奖励模型比单一奖励模型增加约 20% GPU 时间。在极细粒度类别或资源受限场景下，可扩展性受限。
2. **编码器依赖**：数据硬度系数依赖于文本编码器的语义表示质量。编码器能力不足时，余弦相似度可能无法准确反映真实的任务难度，导致权重分配偏差。
3. **模型规模验证不足**：实验限于 3B–8B 规模的开源模型，尚未在更大规模模型（如 70B+）或封闭商用模型上全面验证动态缩放机制的收益是否持续。

### 关键图表结论速览

- **Table 1**：DR-IRL 在两个模型家族上全面超越所有基线，同时维持或提升有用性。
- **Figure 3**：七个有害类别上 DR-IRL 均取得最高拒绝率，无类别盲区。
- **Figure 4**：去除硬度系数导致 StrongReject 下降约 4 个百分点；α^D 主控安全精度，α^M 主控通用稳定性。
- **Table 2**：类别特定影子奖励模型在相似计算量下显著优于单一奖励模型。
- **Table 3**：乘积组合规则在所有指标上优于加权和变体。
- **Table 4**：DR-IRL 对三种越狱攻击均具有最强拒绝能力。
- **Table 5**：难度加权机制可迁移至 DPO 和 PPO，一致提升安全性。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_K0Zh6mzTzc/figures/011_Table_6.jpg]]
*Table 6: Training Hyperparameters*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_K0Zh6mzTzc/figures/012_Table_7.jpg]]
*Table 7: Comparison of CoD and CoT prompting*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_K0Zh6mzTzc/figures/013_Table_8.jpg]]
*Table 8: Pairwise-accuracy (%) of reward models on seven harm categories with Llama-3.1-8B*

## 方法谱系与知识库定位

### 瓶颈驱动的设计动机

DR-IRL 的核心设计源于对当前 LLM 安全对齐方法两个结构性缺陷的回应。第一，安全数据集普遍存在类别不平衡——长尾威胁（如隐私侵犯、精神操纵）往往被主流偏好数据忽视，导致模型在这些类别上拒绝能力薄弱。第二，标准奖励模型是静态的：无论样本难度如何，所有训练实例在 GRPO 优化中享有相同的权重，这使得模型将大量优化预算浪费在已经掌握或过于简单的样本上，而未能充分聚焦于困难且高不确定性的边界案例。

DR-IRL 通过两个因果调节旋钮解决上述瓶颈：**数据层面**，通过构建均衡的七类 CoD 安全示范数据集，为每个有害类别单独训练影子奖励模型；**优化层面**，引入基于语义相似度（数据硬度）和奖励间隙（模型响应性）的动态奖励缩放机制，使 GRPO 的优势函数自适应地聚焦于困难样本。

### 与基线方法的谱系关系

DR-IRL 的基线谱系覆盖了当前 LLM 对齐的主要范式，可从奖励建模方式和优化策略两个维度进行定位。

**偏好优化家族**：**DPO**（Rafailov et al., 2023）及其安全感知变体 **SACPO**（Wachi et al., 2024）通过直接在偏好数据上优化策略来绕过显式奖励建模。DR-IRL 与这些方法的根本区别在于保留了显式奖励模型，但通过 IRL 而非偏好标注来训练——这避免了对大规模人工偏好标签的依赖，同时保持了奖励信号的细粒度。消融实验（Table 5）表明，将难度加权机制应用于 DPO 和 PPO 均能一致提升安全性，说明动态缩放作为优化层面的改进具有跨范式的通用性。

**过程奖励家族**：**STAIR**（Zhang et al., 2025）引入安全感知的过程奖励，在生成过程中提供逐步的安全信号。DR-IRL 与 STAIR 的区别在于奖励信号的粒度：STAIR 关注生成步骤，DR-IRL 关注样本难度。两者并非互斥，但 DR-IRL 的类别特定影子奖励模型提供了更结构化的安全分解。

**GRPO 基线**：**GRPO**（Shao et al., 2024）是 DR-IRL 最直接的优化框架基础。DR-IRL 在 GRPO 上的改进可分解为两个正交的槽位替换：(1) 将静态单一奖励模型替换为七个类别特定的 IRL 训练影子奖励模型；(2) 在组优势函数中注入联合硬度系数 $\alpha_{ji} = \alpha_{ji}^D \cdot \alpha_j^M$。消融实验（Figure 4）表明，仅替换奖励模型（IRL 变体）已带来显著提升，但去除硬度系数会导致 StrongReject 分数下降约 4 个百分点，验证了动态缩放机制的独立贡献。

**自奖励方法**：**Self-Rewarding**（Wu et al., 2024）通过模型自身生成偏好数据来迭代改进。DR-IRL 与之共享“减少外部标注依赖”的理念，但通过 IRL 框架提供了更原则化的奖励学习方式，而非依赖模型自生成的潜在噪声信号。

### 方法谱系中的定位

DR-IRL 处于**奖励建模增强**与**优化动态调整**的交叉点。在奖励建模维度，它属于 IRL 驱动的显式奖励方法，区别于偏好优化（DPO 系列）和过程奖励（STAIR 系列）。在优化维度，它属于难度感知的强化学习对齐，区别于静态优势估计的标准 GRPO/PPO。Table 5 的跨方法验证表明，难度加权更新（DPO-S, PPO-S）一致优于其静态对应版本，但 DR-IRL 的完整流水线（类别特定 IRL 奖励 + 乘积组合硬度系数）在所有安全指标上均达到最优，说明奖励质量与动态缩放的协同效应是性能上界的关键。

### 适用边界与局限

1. **计算可扩展性**：每类单独训练影子奖励模型使 GPU 时间增加约 20%（Table 2：7RW 约 120 GPU h vs. 单 RW 约 100 GPU h）。在极细粒度类别（如数十种攻击策略）或资源严重受限场景下，这一开销可能成为瓶颈。论文尚未探索奖励模型共享或参数高效微调策略来缓解此问题。

2. **文本编码器依赖性**：数据硬度系数 $\alpha^D$ 依赖于文本编码器的语义相似度计算。编码器能力不足时，相似度估计的噪声可能影响权重分配的质量。论文未对不同编码器选择的敏感性进行分析，这一点需要人工验证。

3. **模型规模验证范围**：实验限于 3B–8B 规模的开源模型（Llama-3.1 和 Qwen-2 系列）。虽然 Figure 5 在 3B 模型上验证了安全-有用性 trade-off 的鲁棒性，但尚未在 70B+ 或封闭商用模型（如 GPT-4、Claude）上全面验证。更大模型的奖励间隙分布可能与 8B 规模不同，影响 $\alpha^M$ 的有效性。

4. **安全语料库的覆盖完备性**：均衡的 CoD 数据集覆盖七类有害类别，但可能遗漏微妙的文化暗示、混合意图的灰色地带提示以及罕见的对抗模式。Table 4 的越狱攻击实验（AutoDAN、GCG、DRA）虽然展示了 DR-IRL 的鲁棒性，但攻击类型有限，未覆盖更复杂的多轮越狱或上下文注入攻击。

### 开放问题

1. **细粒度威胁扩展**：DR-IRL 能否进一步扩展到更细粒度的威胁分类（如自定义攻击策略、领域特定的安全约束）并保持计算效率？类别数量的线性增长可能使影子奖励模型的训练成本不可接受，需要探索层次化奖励建模或共享编码器架构。

2. **语料库的对抗完备性**：均衡的安全语料库是否能覆盖微妙的文化暗示和罕见的对抗模式？自动生成的安全示范可能继承 LLM 自身的安全盲区，形成系统性漏洞。对抗性数据增强或人机协同标注可能是必要的补充方向。

3. **奖励-免费方法的适用性**：动态奖励缩放机制是否同样适合奖励-免费对齐方法（如 DPO 变体）而无需显式奖励模型？Table 5 中 DPO-S 的提升表明难度加权在偏好优化中也有价值，但如何在缺乏显式奖励间隙的情况下定义模型响应性 $\alpha^M$ 仍是一个开放的设计问题。

4. **训练动态的理论理解**：乘积组合规则 $\alpha^D \cdot \alpha^M$ 在实验上优于加权和（Table 3），其“AND 门控”的解释具有直觉吸引力，但缺乏对训练动态（如收敛速度、梯度方差）的理论分析。理解硬度系数如何影响策略更新的偏差-方差 trade-off 可能指导更优的组合规则设计。

## 原文 PDF

![[paperPDFs/ICLR_2026/Inverse_Reinforcement_Learning_with_Dynamic_Reward_Scaling_for_LLM_Alignment.pdf]]
