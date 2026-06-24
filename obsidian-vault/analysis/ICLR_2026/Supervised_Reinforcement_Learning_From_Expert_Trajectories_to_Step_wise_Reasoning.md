---
title: "Supervised Reinforcement Learning: From Expert Trajectories to Step-wise Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Supervised_Reinforcement_Learning_From_Expert_Trajectories_to_Step_wise_Reasoning.pdf
openreview_forum_id: Uro84w2xz5
aliases:
- SRLS
- SRLFETSWR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "利用专家动作的逐步相似性作为密集奖励，引导模型在每一步与专家对齐，同时保留内部推理的灵活性。"
primary_logic: "即使在所有 rollout 均不正确的情况下，通过将问题分解为顺序行动并提供基于序列匹配的连续奖励，可以为模型提供持续的学习信号，从而克服 SFT 和 RLVR 各自的局限。"
claims:
- "SRL 在数学推理基准上显著优于 RLVR 和 SFT 基线，SRL 平均准确率达到 27.6%，而 RLVR 仅 24.5%。"
- "SRL → RLVR 两阶段训练进一步提升性能，AIME24 greedy 准确率从 RLVR 的 10.0% 提升至 20.0%。"
- "消融实验证明多步分解和动态采样对 SRL 至关重要，去除动态采样导致平均分从 27.6 降至 24.7。"
- "SRL 在软件工程任务（SWE-Bench-Verified）上也有效，oracle file edit 解决率 14.8%，远超 SWE-Gym-7B 的 8.4%。"
---

# Supervised Reinforcement Learning: From Expert Trajectories to Step-wise Reasoning

> [!tip] 核心洞察
> 即使在所有 rollout 均不正确的情况下，通过将问题分解为顺序行动并提供基于序列匹配的连续奖励，可以为模型提供持续的学习信号，从而克服 SFT 和 RLVR 各自的局限。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 监督强化学习：从专家轨迹到逐步推理 |
| 英文题名 | Supervised Reinforcement Learning: From Expert Trajectories to Step-wise Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Uro84w2xz5) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Supervised Reinforcement Learning (SRL) |
| Dataset | AIME24, Minerva Math, Overall Average (AMC23, AIME25, Minerva Math), SWE-Bench-Verified (Oracle File Edit) |

> [!tip] 效果简介
> - AIME24 上，Greedy Accuracy (%) 为 16.7 (SRL)，对比 10.0 (RL(VR))，变化 +6.7。
> - Minerva Math 上，Greedy Accuracy (%) 为 36.4 (SRL)，对比 33.8 (RL(VR))，变化 +2.6。
> - Overall Average (AMC23, AIME24, AIME25, Minerva Math) 上，Average Greedy Accuracy (%) 为 27.6 (SRL)，对比 24.5 (RL(VR))，变化 +3.1。

## 概述

**核心问题**：在竞赛级数学推理等复杂多步任务中，小模型难以采样到正确解（pass@k 接近零），导致基于可验证奖励的强化学习（RLVR）面临奖励信号极度稀疏的困境，而直接进行监督微调（SFT）则容易在长推理链上过拟合，甚至造成性能退化。

**方法定位**：本文提出 **监督强化学习（Supervised Reinforcement Learning, SRL）**，将问题求解重构为序列决策过程——模型在每一步首先生成内部推理独白（`<think>`），再输出具体“行动”，并以该行动与专家行动的序列相似度作为密集、连续的奖励信号。SRL 在方法谱系中位于 SFT 与 RLVR 之间：它保留了 RL 的探索灵活性和 SFT 对专家知识的利用，但通过逐步分解和序列匹配奖励，克服了二者在困难数据上的各自局限。与基于最终答案正确性的 RLVR 和基于完整轨迹的 SFT 不同，SRL 的核心改变在于**训练信号形式**（从二元正确性/逐 token 交叉熵变为连续相似度分数）、**问题表示**（从完整解答变为部分轨迹 + 下一步行动）以及**奖励密度**（从终点奖励变为每步奖励）。

**知识库定位**：SRL 建立在 GRPO 优化框架之上，与逆课程强化学习 **R³**（Xi et al., ICML 2024）等缓解稀疏奖励的工作形成互补——R³ 通过从终点逐步后退来寻找奖励，而 SRL 通过引入专家动作相似度直接提供每步信号。在软件工程任务上，SRL 将 SWE 任务同样建模为基于历史动作-观测对的序列决策，展示了该方法跨领域的迁移潜力。

**主要结果**：
- 在数学推理基准（AMC23、AIME24、AIME25、Minerva Math）上，SRL 平均 greedy 准确率达 **27.6%**，显著优于 RLVR 的 24.5% 和 SFT 基线；SRL → RLVR 两阶段训练进一步提升至 **28.3%**。
- 在 AIME24 上，SRL → RLVR 的 greedy 准确率从 RLVR 的 10.0% 跃升至 **20.0%**，实现翻倍。
- 在软件工程任务 SWE-Bench-Verified 上，SRL 在 oracle file edit 设置下解决率达 **14.8%**，远超 SWE-Gym-7B 的 8.4%；端到端设置下亦达到 8.6% vs 4.2%。
- 消融实验证实，多步分解和动态采样是 SRL 的关键设计：去除动态采样导致平均分从 27.6 降至 24.7；将多步奖励替换为单步序列相似度或最终答案奖励，性能均出现明显下降。
- 方法在更小的 Qwen2.5-3B 模型上同样有效，SRL → RLVR 平均分从基线的 16.4 提升至 19.5。

**局限与开放问题**：SRL 依赖高质量的结构化专家动作分解，在动作边界模糊或任务难以结构化的领域适用性尚待验证；序列相似度作为奖励可能无法完全捕捉步骤的正确性，尤其在专家动作存在多种合理形式时。此外，能否减少对教师模型的依赖、探索语义相似度等更灵活的奖励函数，以及在大规模模型上的增益幅度，仍是值得进一步研究的方向。

## 背景与动机

### 大语言模型推理能力的训练范式

大语言模型在复杂推理任务上的能力提升，当前主要依赖两种训练范式：**监督微调（Supervised Fine‑Tuning, SFT）** 和 **可验证奖励的强化学习（Reinforcement Learning with Verifiable Rewards, RLVR）**。SFT 通过在完整推理轨迹上最大化 token 级似然来模仿专家行为，而 RLVR（通常基于 GRPO 等策略优化算法）则仅在最终答案正确时提供二元奖励信号，鼓励模型自主探索出通向正确答案的推理路径。

### 核心瓶颈：困难推理任务中的稀疏信号困境

当面对竞赛级数学推理等高度困难的任务时，两种范式均暴露出结构性缺陷。对于小规模模型，**采样到正确解的概率极低（pass@k 接近零）**，这直接导致两个后果：

1. **RLVR 的奖励信号极度稀疏**：模型在绝大多数 rollout 中只能接收到“错误”的二元反馈，缺乏有效的梯度信息来指导策略改进，学习近乎停滞。
2. **SFT 易对长推理链过拟合**：直接拟合完整的专家推理轨迹，模型倾向于记忆表面模式而非掌握逐步推理的逻辑，泛化性能反而可能劣于基模型（Figure 1 证实了这一点）。

这一困境的本质在于：**困难任务的正确解空间过于狭窄，仅凭最终结果的正确性无法为模型提供足够密集的学习信号**。

### 关键洞察：将问题求解重构为序列决策过程

本文的核心动机源于一个关键洞察：即使在所有 rollout 均不正确的情况下，如果能将复杂问题**分解为顺序步骤**，并在每一步将模型生成的动作与专家动作进行**逐步对齐**，就可以构造出连续的、稠密的奖励信号。这种信号不要求最终答案正确，而是衡量中间步骤与专家行为的相似程度，从而为模型提供持续的优化方向。

这一思路将问题求解重新定义为**序列决策过程**：模型在每个步骤接收部分轨迹作为上下文，生成内部推理独白后输出下一步行动，并通过与专家行动的相似度获得即时反馈。这种方式在保留模型内部推理灵活性的同时，克服了 SFT 和 RLVR 各自的局限——既不需要最终答案的正确性，也不强制逐 token 复制专家轨迹。

## 核心创新

本文的核心贡献在于提出**监督强化学习（Supervised Reinforcement Learning，SRL）**，一种将复杂推理任务重构为序列决策过程，并利用专家轨迹提供逐步密集奖励的训练框架。其关键创新围绕以下四个维度展开：

### 1. 训练信号形式：从二元正确性到序列相似性连续奖励

传统 RLVR 仅在最终答案正确时提供一次性二元奖励，在困难推理任务中（pass@k 接近零）几乎无法提供有效学习信号。SRL 将奖励信号替换为**生成行动与专家行动之间的序列相似性得分**：

$$R = \frac{2 \sum_{(i, j, n) \in \mathbf{MatchingBlocks}} n}{|S_1| + |S_2|}$$

该得分基于 Python `difflib.SequenceMatcher` 计算最长连续匹配块的比例，输出 0 到 1 之间的连续值。配合格式检查，最终奖励为：

$$r(\mathbf{y}_{\mathrm{step}_k}', \mathbf{y}_{\mathrm{step}_k}) = \begin{cases} R(\mathbf{y}_{\mathrm{step}_k}', \mathbf{y}_{\mathrm{step}_k}) & \mathrm{if~}\mathbf{y}'\mathrm{~follows~format}, \\ -1 & \mathrm{otherwise}. \end{cases}$$

这一设计使模型即使在所有 rollout 均未产生正确答案时，仍能从每一步的局部对齐中获得学习信号，从根本上解决了 RLVR 的奖励稀疏问题。

### 2. 问题表示：从完整解答到多步部分轨迹

SRL 将完整解答分解为步骤行动（step actions），并构造 N-1 个部分轨迹作为训练输入。具体而言，给定一个包含 N 步的专家解答，每一步之前的已执行步骤构成上下文，模型需在该上下文中首先生成内部独白（`<think>` 标记内），然后输出下一步行动。这一表示转换使得模型学习的是**逐步推理的决策过程**，而非简单模仿完整解答的 token 序列。

与 SFT 在完整轨迹上进行 token 级交叉熵训练不同，SRL 保留了模型在内部推理过程中的灵活性——只要最终行动与专家行动相似即可获得奖励，而非强制每个 token 与专家一致。

### 3. 奖励密度：从终端奖励到每步密集反馈

RLVR 仅在序列末端提供一次奖励，而 SRL 在**每一步**都基于生成行动与专家行动的匹配度计算连续奖励。消融实验（Table 3）证实了这一设计的决定性作用：多步 SRL 平均准确率达到 27.6%，而将序列相似度作为单步整体奖励（one-step）仅得 25.9%，最终答案奖励（RLVR）更低至 24.5%。这表明密集的逐步引导是 SRL 性能增益的核心来源。

### 4. 动态采样策略：从全量保留到方差过滤

SRL 引入基于奖励方差的动态采样机制，仅保留奖励标准差大于阈值 ε 的样本：

$$\sqrt{\frac{\sum_{i=1}^{G}(r(\mathbf{o}_i, \mathbf{y}) - \bar{r})^2}{G}} > \epsilon$$

其直觉是：若一批 rollout 的奖励方差过小（所有尝试的相似度趋同），该样本对策略更新的信息量极低。消融实验（Table 2）表明，去除动态采样导致平均分从 27.6 降至 24.7，验证了该组件对维持有效学习信号的关键作用。与 DAPO 风格过滤全对/全错 rollout 的做法相比，SRL 的方差过滤更精细地识别了“无信息梯度”的样本。

### 方法谱系与知识库定位

SRL 处于 SFT 与 RLVR 的交叉地带：它继承了 SFT 利用专家数据提供结构化引导的优势，又保留了 RL 通过探索和奖励塑造策略的灵活性。与 **R³**（Xi et al., ICML 2024）的逆课程强化学习不同，SRL 不依赖逐步后退寻找稀疏奖励，而是通过序列匹配直接提供密集信号。与 s1K-7B 等蒸馏方法相比，SRL 不要求模型直接拟合完整推理链，而是学习在局部上下文中做出与专家对齐的决策。

## 整体框架

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_Uro84w2xz5/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of SRL as compared to RL(VR) and SFT. (a) RL(VR) takes a query as input and performs k rollouts. The final answer correctness is used as the reward. (b) SFT uses both a query x and a complete teacher response y as input, training with a per-token loss to maximize the probability p ( $\mathbf { y } \vert \mathbf { x }$ ) . (c) SRL also uses a query and a teacher response. It breaks the response into step actions and, at each step, uses the previous steps as context. The model generates a next step action along with its step-wise inner thoughts, and the reward $r _ { k }$ is based on the similarity between the model’s and the teacher’s action

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_Uro84w2xz5/figures/003_Figure_3.jpg]]
*Figure 3: Given a solution trajectory, we take each summarized step as an action to be learned and take the partial solution before the step as the context of our newly created data. The model is then prompted to generate its thinking process followed by the action for the current step. A reward ( r _ { 2 } in the figure) is then calculated based on the similarity between the model’s and the expert’s action*

**Supervised Reinforcement Learning (SRL)** 是一种将复杂问题求解重构为序列决策过程的训练框架。其核心设计围绕三个相互耦合的模块展开：专家轨迹分解与数据构造、策略生成（含内部独白）、以及序列相似性奖励计算。这三个模块共同构成一条从静态专家数据到密集逐步学习信号的完整 pipeline。

### Pipeline 总览

SRL 的输入是一组“问题—完整专家解答”对，输出是一个经过强化学习优化的策略模型。整个流程可以概括为以下步骤：

1. **轨迹分解**：将每条专家解答按逻辑步骤切分为 $N$ 个行动（action），并构造 $N-1$ 条部分轨迹——每条部分轨迹以前 $k$ 步为上下文，第 $k+1$ 步为目标行动。
2. **策略生成**：给定部分轨迹作为输入，模型首先生成内部推理独白（`<think>` 标签内），然后输出对当前步骤的行动预测。
3. **奖励计算**：利用 Python `difflib.SequenceMatcher` 计算生成行动与专家行动之间的序列相似度 $R$，并结合格式合规性给出最终奖励 $r$——格式正确时 $r = R$，否则 $r = -1$。
4. **动态采样**：对每个训练样本进行 $G$ 次 rollout，计算奖励的标准差；仅保留标准差大于阈值 $\epsilon$ 的样本，过滤掉信息量低的更新。
5. **策略优化**：以 GRPO 为目标函数，使用上述逐步奖励更新策略模型。

### 模块关系与数据流

下图（对应原文 Figure 3）描述了从原始解答到训练实例的转换逻辑：

- **专家轨迹分解模块**接收完整解答，输出步骤化的行动序列和对应的部分轨迹。这是 SRL 区别于 RLVR（仅在最终答案处提供稀疏二元奖励）的结构性基础。
- **策略生成模块**在每个部分轨迹上执行推理与行动生成。与 SFT 不同，模型不是被动拟合完整解答的每个 token，而是主动生成内部独白后再“承诺”一个行动——这保留了模型在推理路径上的灵活性。
- **序列相似性奖励模块**将生成的行动与专家行动进行最长连续匹配块比对，输出一个连续值奖励。该奖励在每一步都提供，从而将 RLVR 的稀疏奖励转化为密集学习信号。
- **动态采样模块**作为质量控制闸门：当一批 rollout 的奖励方差过低（即模型对该样本的行为已趋于一致），该样本被丢弃，避免无效的梯度更新。

### 与基线框架的关键差异

| 维度 | SFT | RLVR | SRL |
|------|-----|------|-----|
| 输入形式 | 完整问题 + 完整解答 | 仅问题 | 部分轨迹（上下文 + 目标步骤） |
| 输出形式 | 逐 token 拟合完整解答 | 完整解答（多次 rollout） | 内部独白 + 下一步行动 |
| 奖励信号 | token 级交叉熵（无显式奖励） | 最终答案二元正确性（稀疏） | 每步行动与专家行动的序列相似度（密集连续） |
| 学习目标 | 最大化 $p(\mathbf{y}\|\mathbf{x})$ | GRPO 优化（组归一化优势） | GRPO 优化（逐步奖励 + 动态采样） |

SRL 的关键创新在于将“专家轨迹”同时作为监督信号的来源和奖励函数的参照系：它既不像 SFT 那样强制模型复制专家的每一步推理，也不像 RLVR 那样仅依赖最终答案的正确性——后者在复杂多步推理任务中因 pass@k 接近零而几乎无法提供有效学习信号。通过将解答分解为顺序行动并在每一步给予基于序列匹配的连续奖励，SRL 在保留模型推理自主性的同时，提供了持续且平滑的优化梯度。

## 核心模块与公式推导

### 4.1 瓶颈与设计动机

在复杂多步推理任务（如竞赛级数学证明、软件工程修复）中，小模型面临一个结构性困境：直接从问题采样到正确解的通过率（pass@k）近乎为零。这导致两个连锁失效：**RLVR** 依赖最终答案正确性作为奖励，信号极度稀疏，策略难以获得有效梯度；**SFT** 在长推理链上直接拟合完整轨迹，容易过拟合表面模式而丧失泛化能力。SRL 的核心洞察在于：即使所有 rollout 都不正确，只要将问题求解分解为顺序行动序列，并在每一步提供与专家行动的相似性信号，就能为模型注入持续的学习梯度。

### 4.2 核心模块

SRL 框架由五个紧密耦合的模块构成，其整体流程如 Figure 3 所示。

**模块一：专家轨迹分解与数据构造。** 给定一条包含 $N$ 个步骤的完整专家解答，SRL 将其解析为 $N$ 个行动（action），并构造 $N-1$ 条部分轨迹作为训练输入。每条部分轨迹以前 $k$ 步的上下文为条件，要求模型生成第 $k+1$ 步的行动。这种构造将单条完整解答扩展为多个有监督的训练实例，大幅提升了数据利用率。

**模块二：策略生成（含内部独白）。** 在每一步，模型首先在 `<think>` 标签内生成内部推理独白，然后输出当前步的行动。这一设计保留了模型内部推理的灵活性——模型不必逐字复制专家推理，只需在行动层面与专家对齐。

**模块三：序列相似性奖励计算。** 这是 SRL 区别于 RLVR 的关键。奖励函数基于生成行动 $\mathbf{y}'_{\text{step}_k}$ 与专家行动 $\mathbf{y}_{\text{step}_k}$ 之间的序列匹配度：

$$R = \frac{2 \sum_{(i, j, n) \in \mathbf{MatchingBlocks}} n}{|S_1| + |S_2|}$$

其中 $\mathbf{MatchingBlocks}$ 是两序列的最长连续匹配块集合，$n$ 为每个匹配块的长度，$|S_1|$ 和 $|S_2|$ 分别为两序列的总元素数。该公式本质上是两个序列中匹配元素占总元素的比例，取值范围 $[0, 1]$。实现上采用 Python `difflib.SequenceMatcher` 计算。

最终奖励加入格式惩罚：

$$r(\mathbf{y}_{\text{step}_k}', \mathbf{y}_{\text{step}_k}) = \begin{cases} R(\mathbf{y}_{\text{step}_k}', \mathbf{y}_{\text{step}_k}) & \text{if } \mathbf{y}' \text{ follows format}, \\ -1 & \text{otherwise}. \end{cases}$$

若生成输出遵循指定格式（如正确的标签包裹），奖励即为序列相似度 $R$；否则惩罚为 $-1$。

**模块四：动态采样。** 并非所有训练样本都提供同等信息量的学习信号。SRL 对每个样本采样 $G$ 条 rollout，计算其奖励标准差，仅保留标准差大于阈值 $\epsilon$ 的样本：

$$\sqrt{\frac{\sum_{i=1}^{G}(r(\mathbf{o}_i, \mathbf{y}) - \bar{r})^2}{G}} > \epsilon$$

该机制过滤掉奖励方差过低的样本（如所有 rollout 均与专家高度一致或高度不一致），确保每次更新都来自有区分度的对比信号。消融实验（Table 2）表明，移除动态采样导致平均分从 27.6 降至 24.7，验证了其关键作用。

**模块五：GRPO 优化。** SRL 沿用 GRPO 的目标函数进行策略更新。对于每个保留样本的 $G$ 条 rollout，优势函数 $\hat{A}_{i,t}$ 定义为组内标准化奖励：

$$\hat{A}_{i,t} = \frac{\tilde{r}_i - \text{mean}(\tilde{r})}{\text{std}(\tilde{r})}$$

策略更新采用裁剪比率和 KL 散度惩罚：

$$\mathcal{L}_{\text{GRPO}} = \mathbb{E}\left[ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|\mathbf{o}_i|} \sum_{t=1}^{|\mathbf{o}_i|} \min\left( \frac{p_{\theta}(o_{i,t} \mid \mathbf{x}, \mathbf{o}_{i,<t})}{p_{\theta_{\text{old}}}(o_{i,t} \mid \mathbf{x}, \mathbf{o}_{i,<t})} \hat{A}_{i,t}, \text{clip}(\cdot, 1-\varepsilon, 1+\varepsilon) \hat{A}_{i,t} \right) - \beta D_{\text{KL}}[p_{\theta} \parallel p_{\text{ref}}] \right]$$

### 4.3 关键设计选择

**多步分解 vs. 单步序列相似性。** Table 3 的消融实验直接对比了三种奖励粒度：最终答案奖励（RLVR，平均 24.5）、单步整体序列相似性（25.9）、多步分解 SRL（27.6）。多步分解的优势在于每一步都提供局部对齐信号，避免了单步整体匹配时模型在长序列中迷失方向的问题。

**动态采样 vs. DAPO 风格过滤。** RLVR 基线已采用 DAPO 的过滤策略（丢弃全对/全错的 rollout），SRL 的动态采样在此基础上进一步基于奖励方差筛选。Table 2 验证了这一额外过滤的增益，表明在稠密奖励场景下，方差阈值比简单的极端值过滤更有效。

**两阶段训练：SRL → RLVR。** SRL 提供的稠密信号使模型初步学会结构化推理，随后切换至 RLVR 利用最终答案正确性进行精调。Table 1 显示，SRL → RLVR 在 AIME24 上将 greedy 准确率从 RLVR 单独训练的 10.0% 提升至 20.0%，说明两阶段训练产生了协同效应。

### 4.4 局限与待验证假设

序列相似性奖励基于字符串匹配，当专家行动存在多种合理表达形式时，可能低估模型生成的质量。此外，方法依赖高质量专家轨迹的结构化分解，在动作边界模糊的领域（如开放域创作）适用性尚未验证。不同相似度函数（如语义嵌入匹配 vs. 字符串匹配）的影响也是待探索的开放问题。

## 实验与分析

### 4.1 数学推理主实验

我们以 Qwen2.5-7B-Instruct 为基模型，在具有挑战性的 s1k 数据集上统一对比了 SFT、RLVR（基于 GRPO）和 SRL 三种训练范式。所有方法均使用相同的训练数据，并按验证集最佳检查点进行评估，采用统一的 greedy 解码和 Avg@32 指标。**Table 1** 汇总了核心结果（参见 **Figure 1** 的可视化对比）。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_Uro84w2xz5/figures/004_Table_1.jpg]]
*Table 1: Evaluation results across competition-level math benchmarks. We take Qwen2.5-7B-Instruct as the base model and report the performance of different training schemes (SFT, RLVR via GRPO, and SRL) using the same set of training data. The bold numbers indicate the best results among the open-source models and the underscored numbers represent the second-best results*

**瓶颈验证：** 直接对该困难数据集进行 SFT 导致性能退化——基模型平均准确率为 24.6%，而 SFT（R1 reasoning）降至 20.3%，SFT（R1 outline）进一步降至 17.0%。这表明在长推理链上，SFT 容易过拟合于专家表述，丧失泛化能力。

**RLVR 的局限：** RLVR 将平均准确率恢复至 24.5%，仅略低于基模型，增益有限。其核心问题在于：当模型难以采样到正确解（pass@k 接近零）时，二元正确性奖励过于稀疏，无法提供有效的逐步学习信号。

**SRL 的有效性：** SRL 在所有基准上一致优于 RLVR，平均准确率达到 27.6%（+3.1%）。在 AIME24 上，SRL 的 greedy 准确率为 16.7%，显著高于 RLVR 的 10.0% 和 R³ 的 13.3%。这验证了逐步相似性奖励能够克服稀疏奖励的瓶颈，即使在 rollout 全部错误的情况下也能提供持续的学习信号。

**两阶段训练的进一步提升：** SRL → RLVR 流水线将平均准确率推至 28.3%（greedy 27.1%），在 AIME24 上 greedy 准确率达到 20.0%，较纯 RLVR 翻倍。这表明 SRL 阶段提供的密集引导为后续 RLVR 阶段建立了更优的策略初始化。

### 4.2 消融实验：动态采样

**Table 2** 展示了动态采样对 SRL 的关键作用。移除动态采样后，SRL 平均分从 27.6 降至 24.7（降幅 2.9%），其中 AIME24 greedy 从 16.7% 降至 13.3%，AIME25 greedy 从 20.0% 降至 16.7%。动态采样通过过滤奖励方差低于阈值 ε 的样本，避免了低信息量样本对策略更新的稀释，确保每一步的学习信号都具有足够的区分度。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_Uro84w2xz5/figures/005_Table_2.jpg]]
*Table 2: The effect of dynamic filtering on SRL. Filtering out samples with less meaningful updates provides non-trivial performance improvement. DS stands for dynamic sampling*

### 4.3 消融实验：奖励粒度与函数形式

**Table 3** 系统对比了不同奖励密度和函数形式的影响：

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_Uro84w2xz5/figures/006_Table_3.jpg]]
*Table 3: Model Performance of different reward functions and density. For sequence similarity reward, we implement it with the entire expert output as a one-step supervision. The model benefits from our multi-step decomposition on the small set of challenging training data*

- **最终答案奖励（RLVR）**：平均 24.5%，作为基线。
- **单步序列相似性奖励**：将完整专家输出作为一步进行匹配，平均 25.9%，较 RLVR 提升 1.4%。这证明序列相似性本身比二元正确性更具信息量。
- **多步分解 SRL**：平均 27.6%，较单步序列相似性再提升 1.7%，较 RLVR 提升 3.1%。在 Minerva Math 上，多步 SRL 达到 36.4%，而单步序列相似性仅 33.8%，最终答案奖励为 33.8%。

**因果机制**：多步分解将问题求解重构为顺序决策过程，每一步的奖励直接衡量生成行动与专家行动的匹配度（使用 `difflib.SequenceMatcher` 计算序列相似度 $R$）。这种逐步密集反馈使得模型即使在最终答案错误的情况下，也能在中间步骤获得正向学习信号，从而克服了 SFT 的过拟合和 RLVR 的稀疏奖励问题。

### 4.4 模型规模泛化

**Table 4** 将实验扩展至更小的 Qwen2.5-3B-Instruct 基模型。SRL → RLVR 流水线将平均准确率从基线的 16.4 提升至 19.5（+3.1%），与 7B 模型上的增益幅度一致。在 AIME24 上，greedy 准确率从 6.7% 提升至 10.0%。这表明 SRL 的逐步引导机制在较小模型上同样有效，且增益幅度具有跨规模的稳定性。

### 4.5 软件工程任务迁移

为验证 SRL 在数学之外的泛化能力，我们将其应用于 SWE-Bench-Verified 软件工程基准（**Table 5**）。实验使用 Qwen2.5-Coder-7B-Instruct 作为基模型，从 Yang et al. (2025) 的 5000 条专家 agent 轨迹中构建了 134k 个逐步训练实例（参见 **Figure 4** 的任务适配示意）。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_Uro84w2xz5/figures/008_Table_5.jpg]]
*Table 5: Performance of SRL on SWE-Bench-Verified. Results in the table are using greedy decoding*

**Oracle File Edit 设置**：SRL 解决率达到 14.8%，远超 SWE-Gym-7B 的 8.4%（相对提升 74%），也显著优于基模型 Qwen2.5-Coder-Instruct 的 3.8%。

**End-to-End 设置**：SRL 解决率为 8.6%，较 SWE-Gym-7B 的 4.2% 翻倍，较基模型的 0.0% 实现了从零到有效的突破。

这一结果验证了 SRL 框架的跨领域迁移能力——只要能将任务分解为顺序行动并定义逐步相似性奖励，SRL 即可提供有效的学习信号。

### 4.6 失败模式与局限性

尽管 SRL 在数学推理和软件工程任务上取得了显著增益，仍存在以下局限：

1. **专家数据依赖**：SRL 需要借助强大的教师模型（如 DeepSeek R1）进行动作分解和数据转换，性能上限受制于教师模型的能力。当教师动作本身存在错误或次优时，相似性奖励可能引导模型学习次优策略。

2. **动作边界模糊**：序列相似性奖励基于字符串匹配（`difflib.SequenceMatcher`），当专家动作存在多种合理表达形式时，该奖励可能无法准确捕捉语义等价性。在开放域创作等动作边界不清晰的任务上，SRL 的适用性尚未验证。

3. **格式约束的刚性**：最终奖励函数对格式错误施加 -1 惩罚，这可能导致模型在格式探索上过于保守，抑制了推理风格的多样性。

4. **在线 rollout 成本**：SRL 仍需在线采样多个 rollout 以计算奖励方差和优势函数，训练成本与 RLVR 相当，未显著降低计算开销。

### 4.7 关键图表结论汇总

- **Figure 1 / Table 1**：SRL 在所有数学推理基准上一致优于 SFT 和 RLVR，SRL → RLVR 两阶段训练达到最优性能。
- **Figure 2**：SRL 与 RLVR、SFT 的框架对比——SRL 的核心创新在于将完整解答分解为逐步行动，并在每一步提供基于序列相似性的连续奖励。
- **Figure 3**：SRL 的数据构建与奖励计算流程——从专家轨迹中提取部分轨迹作为上下文，模型生成内部独白和下一步行动，奖励基于生成行动与专家行动的匹配度。
- **Table 2**：动态采样是 SRL 的关键组件，移除后平均性能下降 2.9%。
- **Table 3**：多步分解优于单步序列相似性奖励，后者又优于最终答案奖励，验证了逐步密集反馈的因果作用。
- **Table 5**：SRL 在 SWE-Bench-Verified 上显著超越专用基线 SWE-Gym-7B，证明方法的跨领域泛化能力。

## 方法谱系与知识库定位

### 问题定位：小模型在困难推理任务中的学习信号瓶颈

在复杂多步推理任务（如竞赛级数学证明、软件工程修复）中，小模型面临一个核心困境：**pass@k 接近零**——即使进行多次 rollout，模型也几乎无法采样到完全正确的解答。这直接导致两类主流训练范式的失效：

- **监督微调（SFT）** 在完整推理轨迹上进行 token 级交叉熵训练，但当训练数据难度远超模型当前能力时，模型倾向于死记硬背长推理链而非习得可泛化的推理模式，甚至出现性能退化（Figure 1 中 SFT 低于基模型）。
- **可验证奖励的强化学习（RLVR）** 仅在最终答案处提供二元正确性信号。当所有 rollout 均错误时，奖励信号完全稀疏，GRPO 的优势函数退化为噪声，模型无法获得有效梯度。

这一瓶颈的因果本质是：**奖励信号的密度与模型当前能力不匹配**。SFT 的逐 token 监督虽然密集，但缺乏探索空间；RLVR 虽然允许探索，但奖励过于稀疏。SRL 的设计正是在这两极之间寻找一个可调节的连续谱。

### 方法谱系中的位置：SRL 与相关工作的关系

SRL 的核心操作是将问题求解重构为**序列决策过程**，并在每一步提供基于与专家动作相似度的连续奖励。这一设计使其在方法谱系中占据一个独特位置，与以下工作形成对比或互补：

| 方法 | 奖励密度 | 奖励形式 | 探索自由度 | 与 SRL 的关系 |
|------|----------|----------|------------|---------------|
| **SFT** | 逐 token | 交叉熵（离散） | 无 | SRL 的监督信号来源，但 SRL 用序列相似度替代逐 token 匹配，保留内部独白的灵活性 |
| **RLVR**（GRPO） | 仅最终答案 | 二元正确性 | 完全自由 | SRL 保留 GRPO 优化框架，但将奖励密度从终点扩展到每一步 |
| **R³**（Xi et al., ICML 2024） | 逐步后退 | 稀疏奖励 | 受限 | 同为逐步奖励，但 R³ 通过逆课程从终点后退寻找稀疏奖励，SRL 则直接利用专家动作提供密集信号 |
| **s1K-7B** | — | — | — | 官方蒸馏基线，SRL 使用相同 s1k 数据但以 RL 方式训练，性能显著优于该基线 |

SRL 与 RLVR 的关系尤为关键：两者使用相同的 GRPO 优化目标（含裁剪策略比和 KL 散度惩罚），区别仅在于奖励函数的设计。SRL 可视为 RLVR 的**奖励密度增强版本**，而 SRL → RLVR 的两阶段训练（先用密集奖励引导，再切换至最终答案奖励精调）进一步验证了这一关系：在 AIME24 上，两阶段 greedy 准确率从 RLVR 单独训练的 10.0% 提升至 20.0%（Table 1），说明 SRL 提供的初始引导有效克服了 RLVR 的冷启动问题。

### 适用边界与关键假设

SRL 的有效性依赖于以下前提条件，这些条件同时界定了其适用边界：

1. **可分解的专家动作**：任务必须能够被分解为有明确边界的步骤序列。在数学推理中，步骤对应于解题的阶段性结论；在软件工程中，步骤对应于工具调用和代码编辑操作（Figure 4）。当动作边界模糊（如开放域创作）时，序列相似度奖励可能失效。

2. **高质量教师模型**：SRL 依赖强大的教师模型（如 DeepSeek R1）进行数据转换和步骤总结。教师本身的能力上限构成了 SRL 的性能天花板——若教师在某些步骤上存在系统性偏差，SRL 会将此偏差作为奖励信号传播。

3. **字符串级相似度的有效性**：SRL 使用 Python `difflib.SequenceMatcher` 计算最长连续匹配块比例作为奖励：
   $$R = \frac{2 \sum_{(i, j, n) \in \mathbf{MatchingBlocks}} n}{|S_1| + |S_2|}$$
   这一硬匹配方式在数学公式和代码等结构化输出上有效，但无法捕捉语义等价但形式不同的正确解答。当专家动作存在多种合理形式时，奖励可能低估模型的实际能力。

4. **动态采样的阈值敏感性**：SRL 通过奖励标准差阈值 $\epsilon$ 过滤低信息样本：
   $$\sqrt{\frac{\sum_{i=1}^{G}(r(\mathbf{o}_i, \mathbf{y}) - \bar{r})^2}{G}} > \epsilon$$
   消融实验（Table 2）表明，去除动态采样导致平均分从 27.6 降至 24.7，说明该机制对性能至关重要。但 $\epsilon$ 的选择可能对任务和数据分布敏感，论文未报告其调优过程。

### 已知局限与开放问题

**已确认的局限**（来自论文实验范围）：

- **任务领域受限**：实验集中在竞赛数学（AMC23、AIME24/25、Minerva Math）和软件工程（SWE-Bench-Verified），尚未在更广泛的开放生成任务上验证。
- **模型规模有限**：主要实验在 Qwen2.5-7B 上进行，虽在 3B 模型上验证了泛化性（Table 4，平均分从 16.4 提升至 19.5），但未探索 70B 以上规模。
- **数据依赖性**：需要 5000 条专家轨迹（SWE 任务）或 s1k 数据集进行训练，数据构造本身需要人工或教师模型的介入。

**待探索的开放问题**：

1. **动作定义的泛化**：在动作边界模糊的领域（如创意写作、对话生成）中，如何定义“步骤”和计算相似度？语义相似度（如基于嵌入的匹配）是否能替代字符串匹配？

2. **减少对结构化专家数据的依赖**：能否直接从任务环境中学习动作分解，而非依赖预标注的专家轨迹？例如，利用任务本身的验证器自动识别关键步骤。

3. **与离线 RL 的结合**：SRL 当前需要在线 rollout 计算奖励，成本较高。是否可以将 SRL 的逐步奖励与离线 RL 方法（如 DPO 的逐步变体）结合，降低训练开销？

4. **奖励函数的选择空间**：不同相似度函数（编辑距离、BLEU、语义嵌入余弦相似度）对性能的影响尚未系统研究。Table 3 仅比较了“最终答案奖励 vs 单步序列相似度 vs 多步序列相似度”，未涉及相似度计算方式本身的变体。

5. **与推理长度扩展的交互**：Figure 5 显示 SRL 训练改变了模型的推理长度分布，但 SRL 是否能在推理时通过增加 rollout 步数持续提升性能（即 test-time scaling），仍需进一步验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Supervised_Reinforcement_Learning_From_Expert_Trajectories_to_Step_wise_Reasoning.pdf]]
