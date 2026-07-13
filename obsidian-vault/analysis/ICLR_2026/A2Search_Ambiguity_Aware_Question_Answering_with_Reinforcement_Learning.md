---
title: "A$^2$Search: Ambiguity-Aware Question Answering with Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A2Search_Ambiguity_Aware_Question_Answering_with_Reinforcement_Learning.pdf
project_link: null
code_link: https://github.com/zfj1998/A2Search
aliases:
- 2SAAQARL
- A2SEARCH
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "将单一参考答案的精确匹配奖励替换为答案级F1（AnsF1）奖励，并自动构建包含多个验证后替代答案的训练数据，使模型能从奖励中学习适应多答案场景。"
primary_logic: "通过轨迹采样与证据验证自动发现歧义问题的替代答案，结合GRPO和AnsF1奖励，让模型在搜索过程中感知歧义并输出所有证据支持的答案，而非仅拟合基准参考答案。"
claims:
- "MuSiQue训练集中27.6%的样本存在不止一个有效答案，说明歧义广泛存在。"
- "A²SEARCH采用全自动管道，通过轨迹采样和证据验证检测歧义问题并收集替代答案。"
- "训练使用GRPO，奖励函数基于AnsF1，自然适配多个参考答案。"
- "Macro Avg (4 multi-hop benchmarks: HotpotQA, 2Wiki, MuSiQue, Bamboogle) 上 AnsF1@1 (Exact Match) = 48.4"
---

# A$^2$Search: Ambiguity-Aware Question Answering with Reinforcement Learning

> [!tip] 核心洞察
> 通过轨迹采样与证据验证自动发现歧义问题的替代答案，结合GRPO和AnsF1奖励，让模型在搜索过程中感知歧义并输出所有证据支持的答案，而非仅拟合基准参考答案。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | A²Search：模糊感知的强化学习问答系统 |
| 英文题名 | A$^2$Search: Ambiguity-Aware Question Answering with Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=3CPzUWIoNf) · [GitHub](https://github.com/zfj1998/A2Search) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | A2SEARCH |
| Dataset | Macro Avg (4 multi-hop benchmarks: HotpotQA, 2Wiki, MuSiQue, Bamboogle), HotpotQA, NQ (single-hop), AmbigQA (human-annotated ambiguity) |

> [!tip] 效果简介
> - Macro Avg (4 multi-hop benchmarks: HotpotQA, 2Wiki, MuSiQue, Bamboogle) 上，AnsF1@1 (Exact Match) 为 48.4，对比 46.2 (ReSearch-32B)，变化 +2.2。
> - HotpotQA 上，AnsF1@1 (Exact Match) 为 49.5 (A2SEARCH-7B)，对比 39.3 (ReSearch-7B)，变化 +10.2。
> - NQ (single-hop) 上，AnsF1@1 (Exact Match) 为 51.4 (A2SEARCH-7B)，对比 – (best baseline in Table 2)，变化 –。

## 概要

开放域问答（QA）系统的训练长期隐含一个假设：每个问题只对应唯一的标准答案。然而，真实世界的提问常常存在歧义——同一问题可由多个不同的答案有效回答，而现有方法难以感知并合理处理这类多答案场景。研究表明，仅在 MuSiQue 这一多跳QA基准的训练集中，就有 27.6% 的样本存在不止一个有效答案。当强化学**（RL）训练的奖励信号仍然基于单一参考答案的精确匹配时，模型无法从歧义中学习，反而会因奖励误导而性能受限。

为解决这一核心瓶颈，本文提出 **A²Search（Ambiguity‑Aware Question Answering with Reinforcement Learning）**，一种无需人工标注的模糊感知问答框架。其核心思路是：**将“答案唯一”的假设替换为“答案可多”的学习范式，并自动构建包含多个证据验证后的替代答案的训练数据**，使模型在学习搜索策略的过程中自然适应歧义。方法上，A²Search 通过轨迹采样与证据验证，自动检测歧义问题并挖掘替代答案；然后利用组相对策略优化（GRPO）进行训练，奖励函数从单一的精确匹配（EM）改为**答案级 F1（AnsF1）**，能够同时衡量模型输出与多个参考答案的匹配程度。一次 rollout 中，模型可自主决定输出一个或多个答案，并依据 AnsF1 奖励学会何时输出多个答案以覆盖不同证据支持的合理结果。

在四个多跳 QA 基准（HotpotQA、2Wiki、MuSiQue、Bamboogle）上，A²Search‑7B 取得了平均 AnsF1@1 得分 48.4%，超过了包括 32B 参数量的 ReSearch 在内的多个强基线；在 HotpotQA 上，相对于同尺寸的 ReSearch‑7B 提升高达 10.2 个百分点。在显式包含人工标注歧义的 AmbigQA 基准上，A²Search 的表现也优于直接在 AmbigQA 训练集上训练的模型，验证了其自动感知与处理歧义的能力。消融实验进一步表明，多答案训练数据与 AnsF1 奖励具有互补增益，奖励参数 α 控制在 0.4 时能在精确率与召回率之间取得平衡，而引入熵正则化可防止 RL 训练中策略过早确定性坍塌，保障对多样答案的探索。

综上，A²Search 提供了一种系统化的模糊感知问答方案：将歧义从训练障碍转化为可学习的信号，在多个搜索增强的 QA 场景下有效提升模型的鲁棒性与答案覆盖能力。



开放域多跳问答要求模型在多个文档间进行推理并定位答案，近年来基于搜索的强化学习范式（如 ReSearch）通过让智能体自主调用检索工具，显著提升了多步推理能力。然而，这类方法的训练普遍隐含一个关键假设：每个问题只存在唯一正确答案，奖励信号完全以模型输出与单一参考答案的精确匹配（Exact Match）为依据。现实世界中的信息需求往往具有内在歧义，同一问题在不同证据下可能存在多个合理的答案，而这一假设导致奖励信号在歧义场景下发生系统性失真——即使模型输出的是由证据充分支持的答案，只要与预设参考答案不一致，就会被判定为错误。

这一问题的严重性可以从 MuSiQue 训练集的实证分析中得到印证：高达 27.6% 的样本实际可被多个有效答案所满足，歧义并非边缘现象。在 Figure 1 展示的典型案例中，ReSearch 面对一个歧义问题时，多次 rollout 会给出不同答案，其中部分与参考不一致但仍被证据支撑，却因单一答案的奖励机制而受到惩罚。这种奖励信号的偏差不仅阻碍了模型对歧义的正确感知，更迫使模型在训练中盲目拟合单一参考，丧失了在搜索过程中表达不确定性与多样性的能力。

因此，一个关键缺口浮现：现有基于 RL 的问答系统缺乏对问题歧义的感知与适应机制，无法在单次推理中输出多个证据支持的答案以匹配真实的答案分布。这促使本文提出 A²SEARCH，其核心动机在于通过全自动管道发现歧义问题中的替代答案，并引入基于答案级 F1（AnsF1）的奖励函数，使模型能在搜索过程中自主判断是否有歧义、并生成全部有依据的答案，从而纠正奖励信号的系统偏差，使 RL 训练与多答案的真实场景对齐。



## 核心方法与创新机理

现有搜索增强强化学习QA方法（如ReSearch、Search-R1）的核心假设是**每个问题仅存在唯一正确答案**，训练奖励和评估均基于单一参考答案的精确匹配（EM）。然而，该假设与真实世界中大量存在的含歧义、多答案问题严重不符——论文分析显示 **MuSiQue 训练集中 27.6% 的样本实际上允许不止一个有效答案**（`our analysis finds that 27.6% of MuSiQue’s training examples admit more than one valid answer`）。这一瓶颈导致传统方法在面对歧义问题时 RL 奖励信号错误，模型无法学习分辨并输出多个证据支持的答案。

A²SEARCH 的核心创新在于**将歧义感知注入搜索强化学习的两个关键槽位：奖励函数与训练数据答案集合**，并使解码行为与之协同，从而无需人工标注即可学习输出多个正确答案。具体体现在以下三个已改变的槽位（changed slots）和一项自动化数据构建机制：

### 1. 奖励函数：从精确匹配（EM）到答案级 F1（AnsF1）
- **基准值**：传统搜索 RL 方法（如 ReSearch、SinSearch）采用基于单一参考答案的完全匹配（EM）或微调后的匹配奖励，多答案歧义直接被误判为错误。
- **创新值**：A²SEARCH 采用**答案级 F1（AnsF1）**作为结果奖励的核心度量，天然支持存在多个参考答案的场景（`outcome rewards are based on answer-level F1 (AnsF1), a metric that naturally accommodates multiple answers`）。奖励设计为：
  - 格式非法得 0；
  - 格式合法但未命中任何参考答案得 0.1；
  - 命中时奖励随 AnsF1 线性增加，参数 $\alpha$ 控制不完全匹配时的惩罚力度，从而**精确调节模型对输出精确率的重视程度**（`$R(q,\hat{ans}) = 1 - \alpha(1 - \mathrm{AnsF1})$` with $\alpha = 0.4$）。消融实验证实 $\alpha$ 过小会导致答案数量爆炸（奖励破解），过大则使模型退化为单答案输出（Figure 6）。

### 2. 训练数据中的答案集合：从单参考答案到多证据验证替代答案集
- **基准值**：传统方法中每个训练问题仅配有一个标准参考答案。
- **创新值**：A²SEARCH 通过**全自动管道自动检测歧义问题，并为每个歧义问题收集经过证据验证的替代答案**（`automated pipeline that detects ambiguous questions and gathers alternative answers via trajectory sampling and evidence verification`），最终构建包含多个替代答案的训练数据。该管道包含四个步骤（Figure 2）：
  1. **采样（Sampling）**：用多个搜索模型为每个问题生成大量轨迹，收集候选答案；
  2. **过滤（Filtering）**：剔除与原参考答案相同、无能力解决该问题以及重复的轨迹；
  3. **验证（Verification）**：由多个强 LLM 验证器进行多数投票，判断轨迹是否提供充分证据支持候选答案（`$\mathrm{Verify}(q,\tau,a\hat{n}s)=1$ if $\frac{1}{K}\sum z_k \geq \eta$`，缺省阈值 $\eta=3$，人类一致性达 96%）；
  4. **分组（Grouping）**：对语义等价的候选答案进行聚类，每组选取一个代表答案。

  该方法完全脱离人工标注，形成的训练答案集合使模型在 RL 优化中能同时接触到多条有效答案路径，从根本上解决“正确但不同”的答案被错误惩罚的问题。

### 3. 解码策略：从“每次只输出一个答案”到“单次 rollout 可输出多答案”
- **基准值**：现有搜索 QA 模型每次 rollout 仅输出一个答案，依赖多次 rollout 的多样性间接覆盖歧义。
- **创新值**：A²SEARCH 模型在单个 rollout 内**自主决定输出一个或多个答案**，并能从 AnsF1 奖励中学习何时应该多答案（`A2SEARCH explicitly resolves ambiguity by retrieving multiple answers within a single rollout`）。模型行为通过奖励塑造：当问题确有多答案时，输出一个以上答案可提升召回，从而获得更高奖励；当问题为单一答案时，模型则倾向于只输出一个答案，避免精确率损失。这一能力是所有 baselines 不具备的，使搜索过程能一次完成歧义消解。

### 辅助创新：训练稳定性与通用化
为保障上述创新在训练过程中的稳定性，A²SEARCH 在 GRPO 目标中加入了**自适应熵控制**，通过动态调节熵正则项权重 $\lambda$ 防止策略过早确定性坍塌（`entropy-regularized GRPO with adaptive entropy control`），使基于基础模型直接 RL 训练的版本亦能稳定收敛并提升验证集召回率（Figure 5）。

这三个插槽的创新相互耦合、缺一不可：多答案训练数据如果没有 AnsF1 奖励，则模型无法获得有效反馈；AnsF1 奖励若无多答案数据，模型虽能部分“挤出”歧义，但性能远低于完整框架（消融变体 A²SINSearch 与 RECALLSearch 的结果，Table 18）。最终，A²SEARCH‑7B 在四个多跳 QA 基准上比同等规模的 ReSearch 基线 AnsF1@1 平均提升 **+2.2 个百分点**（48.4 vs 46.2），并在歧义密集的 HotpotQA 上实现 **+10.2 的巨大跃升**，证实了相对基线的关键创新价值。



![[assets/figures/papers/iclr26_0004_3CPzUWIoNf_A2Search_Ambiguity-Aware_Question_Answering_with/figures/002_Figure_2.jpg]]
*Figure 2: Our pipeline for automatically identifying alternative answers in ambiguous questions*

A²Search 是一个全自动的歧义感知强化学习问答框架，其核心动机在于解决开放域多跳问答中长期被忽视的歧义问题——现有训练范式假设每条问题有且仅有一个正确答案，然而现实世界中的大量问题（例如 MuSiQue 训练集中高达 27.6% 的样本）都存在多个证据支持的有效答案。这种单一答案假设导致传统的精确匹配奖励信号错误，使模型在面对歧义问题时要么输出单一但可能并非用户意图的答案，要么在不同搜索轨迹中给出相互矛盾的结果（见图 1 的对比示例）。

A²Search 通过两条相互协同的机制打破这一瓶颈：**自动构建多答案训练数据**与**基于答案级 F1（AnsF1）的强化学习奖励**。整个框架由两阶段组成，二者的输入输出流依次串联——先离线构建歧义感知的训练数据，再在线利用该数据通过群体相对策略优化（GRPO）训练搜索型问答策略。

### 1. 自动替代答案发现流水线

给定一个原始 QA 数据集（每个问题最初仅配有一个标准参考答案），A²Search 首先运行一个四步证据驱动流水线，以全自动方式检测歧义问题并收集证据支持的其他正确答案（如图 2 所示）：

1. **采样（Sampling）**  
   利用多个异构的搜索型大模型（如 ReSearch 等）为每个问题生成大量搜索轨迹（共约 400 万条），从这些轨迹的最终输出中提取候选答案。该步的核心目的是通过不同模型和多次采样尽可能覆盖潜在的正确答案空间。

2. **过滤（Filtering）**  
   对采样得到的轨迹进行粗筛，剔除三类低质量轨迹：与原始参考答案完全相同的轨迹（避免冗余）、明显无法解决该问题的轨迹（例如格式错误或答案完全无关）、以及内容高度重复的轨迹。

3. **验证（Verification）**  
   由 $K$ 个强大的 LLM 验证器对每条候选轨迹进行二值判断——是否提供了足以支撑该候选答案的证据。验证采用多数投票机制，其决策函数为：
   $$\mathrm{Verify}(q, \tau, a) = \begin{cases} 1, & \text{if } \frac{1}{K} \sum_{k=1}^{K} z_k \geq \eta, \\ 0, & \text{otherwise}, \end{cases}$$
   其中 $z_k$ 为第 $k$ 个验证器的判断（1 表示支持），阈值 $\eta=3$ 经人类一致性评估选定，可达到 96% 的人类一致率（Table 8）。只有获得足够验证器支持的轨迹才会以 $1$ 标记，其答案被视为一个有效的替代答案。

4. **分组（Grouping）**  
   对通过验证的候选答案集合进行语义等价聚类，每组选取一个代表性答案，从而消除表面形式不同但指向同一实体的答案（例如别名或同义表述）。最终为每个歧义问题构建出一个包含多个独立证据支持的参考答案集合，并将这些替代答案合并到原始训练数据中，形成扩展后的多答案训练集。

该流水线的输入为原始 QA 数据集，输出为每条问题对应的一组参考答案（可由 1 个扩展至多个）。整个过程无需人工标注，完全自动化。

### 2. 歧义感知的强化学习训练

在构建好多答案训练数据后，A²Search 采用 GRPO 对搜索型问答策略进行训练，其核心改变体现在奖励函数和解码策略两个维度：

- **奖励函数**  
  传统的完全匹配（EM）奖励仅适应单一参考答案，而 A²Search 引入了基于答案级 F1（AnsF1）的奖励。对于一条生成的轨迹及其输出答案 $\hat{ans}$，奖励定义为：
  $$R(q, \hat{ans}) = \begin{cases} 0, & \text{格式无效}, \\ 0.1, & \text{格式有效但未命中任何参考答案}, \\ 1 - \alpha(1 - \mathrm{AnsF1}), & \text{格式有效且至少命中一个参考答案}. \end{cases}$$
  其中 $\alpha$ 是平衡精确率与召回率的关键参数，设置为 0.4（Figure 6）。该奖励天然适配多个参考答案，AnsF1 计算时仅统计命中的不同参考答案数，防止模型通过输出同一答案的多个表面变体进行奖励作弊。当模型给出多个答案时，精确率惩罚由 $\alpha$ 控制，召回率则通过命中更多参考答案来提升整体奖励，从而引导模型学会输出适当的答案数量。

- **解码策略**  
  与以往每次 rollout 仅输出一个答案不同，A²Search 的策略可以在单条轨迹中自主决定输出多个答案（由模型通过生成格式标记自行判断）。训练时，GRPO 的优化目标（简化形式）：
  $$\mathcal{I}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\} \sim \pi_{\theta_{\mathrm{old}}}} \frac{1}{G} \sum_i \left[ \min\left( \frac{\pi_\theta}{\pi_{\theta_{\mathrm{old}}}} A_i, \mathrm{clip}(\dots) A_i \right) \right]$$
  结合 AnsF1 奖励，使模型自然习得何时应当输出单一答案、何时输出多个证据支持的答案。消融实验证实，仅使用 AnsF1 奖励而不使用多答案数据（A2SINSearch）仍能挤出部分歧义，但性能远不及完整框架；同时取消多答案数据和 AnsF1 奖励则效果最差（Table 18），说明二者存在显著的协同互补性。

- **辅助稳定训练机制**  
  对于基础模型训练，A²Search 在 GRPO 目标中额外加入自适应熵正则化项以防止策略的过早确定性坍塌，通过动态调整权重系数维持一定的探索熵（公式见 Appendix A.2）。

### 3. 整体输入输出流与推理表现

训练阶段以扩展后的多答案数据集为输入，输出一个歧义感知的搜索型策略模型。推理阶段，对于输入问题，模型在单次 rollout 中即可通过检索、推理并最终输出一个或多个答案，答案数量完全由模型自主决定。相比基线（如 ReSearch）需多次采样才能覆盖多个有效答案且各次轨迹答案可能相左，A²Search 在单次 rollout 内即能显式解决歧义，直接给出所有证据支持的答案（Figure 1）。这一端到端的歧义感知设计使 A²Search-7B 在四个多跳基准上平均 AnsF1@1 达到 48.4%（超过 ReSearch-32B 的 46.2%），并在 HotpotQA 上提升达 +10.2 个百分点，展现出对真实世界问答歧义的有效适应能力。



A²SEARCH 框架的核心由两大模块构成：自动替代答案构建管道（数据层面）与基于答案级奖励的强化学习训练（训练层面）。两者协同解决开放域 QA 中的多答案歧义瓶颈——传统训练假设每个问题仅有唯一正确答案，导致奖励信号与真实世界不符。替代答案管道通过轨迹采样与证据验证识别歧义问题并收集有效替代答案；训练则采用 GRPO 与 AnsF1 奖励，使模型在一次 rollout 中自主决定是否输出多个答案。

**自动替代答案构建管道（图 2）**
管道由四个顺序步骤组成，全自动运行，无需人工标注。

| 步骤 | 功能 |
|------|------|
| **采样（Sampling）** | 使用多个搜索模型为每个问题生成大量检索-推理轨迹，收集候选答案。 |
| **过滤（Filtering）** | 粗筛轨迹：移除输出与参考答案完全相同、无法解决该问题、以及重复的轨迹，减少后续计算量。 |
| **验证（Verification）** | 通过 $K$ 个 LLM 验证器进行多数投票，判定轨迹是否提供充分证据支持候选答案。只有证据确认的候选才作为替代答案进入下一步。 |
| **分组（Grouping）** | 对语义等价的候选答案进行聚类，每组选取一个代表答案，形成最终的多答案集合。 |

**验证投票公式**
验证阶段的核心是一个二元决策函数，确保替代答案的证据可信度：

$$
\mathrm{Verify}(q, \tau, a\hat{n}s) =
\begin{cases}
1, & \mathrm{if~} \frac{1}{K}\sum_{k=1}^{K} z_k \geq \eta, \\
0, & \mathrm{otherwise},
\end{cases}
$$

其中 $q$ 为问题，$\tau$ 为轨迹，$a\hat{n}s$ 为候选答案；$z_k \in \{0,1\}$ 为第 $k$ 个验证器的二元判决（0-不充分，1-充分）；$\eta$ 为多数投票阈值。默认使用 $K=4,\ \eta=3$，获得 96% 的人类一致性（Table 8）。该公式保证了替代答案不是偶然匹配，而是有跨验证器一致的支持证据链。

**基于 AnsF1 的奖励设计**
训练奖励函数完全脱离单一参考答案的完全匹配（EM）机制，改为答案级 F1（AnsF1）惩罚不完整匹配。奖励公式为：

$$
R(q, \hat{ans}) =
\begin{cases}
0, & \mathrm{if~format~invalid,} \\
0.1, & \mathrm{if~format~valid~and~hits=0,} \\
1 - \alpha(1 - \mathrm{AnsF1}), & \mathrm{if~format~valid~and~hits>0}.
\end{cases}
$$

- $q$：输入问题；$\hat{ans}$：模型输出的答案集合（可含多个答案）。
- 格式无效（如未按指定结构输出）得 0 分。
- 格式有效但未命中任何参考答案（hits = 0）得 0.1 分，给予低信号鼓励继续搜索。
- 当命中至少一个参考答案时，奖励随 AnsF1 线性缩放：AnsF1 = 1 时得满分 1，AnsF1 越低惩罚越大（由 $\alpha$ 控制）。AnsF1 计算时仅统计不同参考答案的命中数，防止模型通过重复输出同一答案变体刷分。
- $\alpha$ 是平衡精确率与召回率的关键超参。消融实验表明 $\alpha=0.4$ 使模型生成适量答案；$\alpha$ 过小导致答案爆炸（reward hacking），$\alpha$ 过大使模型几乎只输出单答案（Figure 6）。

**GRPO 优化目标**
策略优化采用分组相对策略优化（GRPO），避免独立价值网络。目标函数为组内标准化优势的裁剪版本：

$$
\mathcal{I}(\theta) = \mathbb{E}_{x\sim\mathcal{D},\ \{y_i\}\sim\pi_{\theta_{\mathrm{old}}}}
\frac{1}{G}\sum_{i=1}^{G}
\left[
\min\left(
\frac{\pi_{\theta}}{\pi_{\theta_{\mathrm{old}}}}A_i,\ 
\mathrm{clip}\left(\frac{\pi_{\theta}}{\pi_{\theta_{\mathrm{old}}}}, 1-\epsilon, 1+\epsilon\right)A_i
\right)
\right].
$$

- $x$：输入问题；$\{y_i\}_{i=1}^{G}$：从旧策略 $\pi_{\theta_{\mathrm{old}}}$ 采样的 $G$ 个轨迹（rollout），组成一个分组。
- $A_i$：轨迹 $y_i$ 的相对优势，通过组内奖励标准化计算，避免绝对奖励信号不稳定。
- 策略比率 $\frac{\pi_{\theta}}{\pi_{\theta_{\mathrm{old}}}}$ 裁剪到 $[1-\epsilon, 1+\epsilon]$，防止过大的策略更新。
- 实际训练中，奖励 $R(q, \hat{ans})$ 被分配为结果奖励，通过 GRPO 隐式影响优势计算。

**熵正则化（Base 模型训练专用）**
当从基础模型开始 RL 训练时，策略容易过早确定性坍塌。为此，在目标中引入适应性熵正则化：

$$
\mathcal{I}(\theta)=\mathbb{E}_{x,\{y_i\}}\frac{1}{G}\sum_{i=1}^{G}
\left[
\min\left(
\frac{\pi_{\theta}}{\pi_{\theta_{\mathrm{old}}}}A_i,\ \mathrm{clip}(\cdots)A_i
\right) + \lambda \mathcal{H}_{\theta}(x, y_i)
\right],
$$

- $\mathcal{H}_{\theta}(x, y_i) = \frac{1}{|y_i|}\sum_{t=1}^{|y_i|} H\big(\pi_{\theta}(\cdot\mid x, y_{i,<t})\big)$，表示轨迹 $y_i$ 上每个位置的策略熵平均值。$H(p) = -\sum_a p(a)\log p(a)$。
- $\lambda$ 为自适应权重：设定目标熵 $h$，当当前熵低于目标时增大 $\lambda$（增加探索），反之减小 $\lambda$（降低随机性）。实验证实该机制显著提升验证集召回率（Figure 5）。

**模块间的因果链路**
- 数据管道提供多答案训练集 → AnsF1 奖励函数为多答案输出提供正确梯度信号 → GRPO 优化促使模型在歧义时一次输出多个证据支持的答案。
- 消融实验（Table 18）表明：若同时取消多答案数据和 AnsF1 奖励，召回能力大幅下降；仅使用 AnsF1 奖励而不用多答案数据（A2SINSearch）仍能挤出部分歧义，但效果远不如完整框架，证明两模块的互补性。
- 熵正则化仅在 Base 模型冷启动时使用，防止策略坍缩，为后续多答案学习保留必要的探索能力。

以上模块构成 A²SEARCH 从数据到训练、从证据到奖励的完整模糊感知强化学习机制。



## 实验与关键发现

本节首先说明评估协议与基准选择，然后报告 A²SEARCH 在多跳与通用 QA 场景中的**主结果**，接着通过若干**消融实验**揭示奖励设计、熵正则化、采样配置以及多答案数据的关键作用，最后讨论方法当前的**局限与失败模式**。

### 评估协议与基准

为公平评估歧义感知的问答能力，我们同时采用 **精确匹配（Exact Match，EM）** 与 **LMJudge** 两类指标。EM 检查预测答案是否与任意一个参考答案（含其别名）完全匹配，并在此基础上计算 **答案级 F1（AnsF1）** 与 **Recall@k**，以真实反映多答案场景下的性能。作为补充，LMJudge 通过 Qwen2.5‑32B‑Instruct 判断预测答案与参考答案的语义等价性，避免表面匹配的偏差。所有主实验均在 **四个多跳 QA 基准**（HotpotQA, 2WikiMultihopQA, MuSiQue, Bamboogle）与 **四个通用 QA 基准**（Natural Questions, TriviaQA, PopQA, AmbigQA）上进行，其中 AmbigQA 包含人工标注的多答案歧义问题，是检验歧义处理能力的直接试金石。

### 主结果概览

- **多跳基准上的显著提升。** 在精确匹配设定下，A²SEARCH‑7B 在四个多跳基准上取得宏平均 **AnsF1@1 48.4%**，以 7B 参数量超越了 32B 的 ReSearch（46.2%）以及全部同规模基线（表 1）。更为突出的是，在歧义集中的 **HotpotQA** 上，A²SEARCH‑7B 达到 **49.5 AnsF1@1**，相较 ReSearch‑7B（39.3）提升 **+10.2 个百分点**，表明其多答案机制有效缓解了单答案强假设造成的性能低估。
- **通用 QA 上的竞争力。** 在单跳基准 Natural Questions 上，A²SEARCH‑7B 获得 **51.4 AnsF1@1**（表 2）；在含人工标注多答案的 **AmbigQA** 上，A²SEARCH‑7B 取得 **48.1 AnsF1@1**，甚至超过了直接在 AmbigQA 训练集上微调的专用模型，证明从无标注歧义数据中学习比“清洗后”人工标注更具泛化性。
- **多答案输出的行为证据。** 图 1 中的 rollout 实例直观展示了差异：对于同一歧义问题，单答案搜索基线在不同次 rollout 中给出不同答案，其中某些虽然符合证据但偏离单一参考答案；而 A²SEARCH **在单次 rollout 内即可输出多个有效答案**，自然覆盖证据支持的多种事实。

![[assets/figures/papers/iclr26_0004_3CPzUWIoNf_A2Search_Ambiguity-Aware_Question_Answering_with/figures/004_Table_1.jpg]]
*Table 1: Main results on four multi-hop QA benchmarks under the Exact Match metric. We report AnsF1/Recall@k with k rollouts. For AbgSearch and $\mathbf { A } ^ { 2 } \mathbf { S } \mathbf { E } \mathbf { A } \mathbf { R } \mathbf { C } \mathbf { H }$ , only @1 is reported, reflecting their ability to produce multiple answers within a single rollout. For the remaining baselines, where each rollout generates only one answer and thus AnsF1@1 = Recall@1, we additionally include AnsF1/Recall@3 to evaluate their performance when more rollouts are available. The best result in each comparison group is shown in bold, and the second best is underlined

![[assets/figures/papers/iclr26_0004_3CPzUWIoNf_A2Search_Ambiguity-Aware_Question_Answering_with/figures/008_Table_2.jpg]]
*Table 2: Main results with the Exact Match metric on four general QA benchmarks, using the same notations as Table 1. For AmbigQA, where questions may have multiple reference answers, AnsF1@1 and Recall@1 are not equivalent in this setting, and both are therefore reported*

### 关键设计消融

我们通过一系列消融实验量化各设计决策的贡献。

#### 奖励参数 α 与多答案行为

奖励函数中参数 **α** 控制对非完美 AnsF1 的惩罚力度，是平衡精确率与召回率的扭结（图 6）。当 **α=0.4** 时，模型生成适中数目的答案，验证集答案数保持稳定，精确率与召回率取得最佳平衡。**α 过小**（如 0.2）使奖励对额外输出不敏感，导致模型在训练过程中答案数量爆炸式增长（单次 rollout 可达 13 个以上），表现出典型的奖励破解（reward hacking）；**α 过大**（如 0.8）则迫使模型几乎只输出一个答案，丧失多答案能力。这一对照说明 AnsF1 奖励的 α 参数是使模型自发学习“何时输出多个答案”的关键杠杆。

![[assets/figures/papers/iclr26_0004_3CPzUWIoNf_A2Search_Ambiguity-Aware_Question_Answering_with/figures/024_Figure_6.jpg]]
*Figure 6: Effect of α in reward design on validation performance and the model’s answer count*

#### 多答案数据与 AnsF1 奖励的协同

系统消融实验（表 18 及相关分析）对比了三个变体：
- **A²SEARCH（完整框架）**：同时使用多答案训练数据与 AnsF1 奖励；
- **A²SINSearch**：仅使用 AnsF1 奖励，但训练数据保持单一参考答案；
- **RECALLSearch**：完全移除多答案数据与 AnsF1 奖励，仅用传统精确匹配奖励与单答案数据。

![[assets/figures/papers/iclr26_0004_3CPzUWIoNf_A2Search_Ambiguity-Aware_Question_Answering_with/figures/033_Table_18.jpg]]
*Table 18: Ablation study results on eight QA benchmarks. We report AnsF1@1 for single-answer models and AnsF1 / Precision / Recall at @1 for the models that produce multiple answers*

结果表明：仅凭 AnsF1 奖励（A²SINSearch）可从单答案数据中挤出部分歧义，但性能远不及完整框架；当同时撤除多答案数据与 AnsF1 奖励时（RECALLSearch），效果最差。这证实 **多答案训练数据与 AnsF1 奖励形成强互补**——前者为 RL 提供充足的奖励信号多样性，后者使模型能从这些信号中习得适应歧义。

#### 熵正则化防止策略坍塌

在基础模型上进行 GRPO 训练时，我们引入了带自适应权重 λ 的熵正则项（公式见 §A.2），以防止策略过早确定性坍塌。**图 5** 显示，使用熵控制（EC）的配置在验证集上始终获得更高的召回率，且熵值未见崩溃；无熵控制的基线则在训练约 400 步后熵急剧下降，召回增益提前停滞。因此，熵控制对于维持探索、提升多答案召回至关重要。

![[assets/figures/papers/iclr26_0004_3CPzUWIoNf_A2Search_Ambiguity-Aware_Question_Answering_with/figures/012_Figure_5.jpg]]
*Figure 5: Effect of entropy control on validation performance and the model’s entropy value*

#### 采样温度与 Rollout 规模

在构建训练数据的轨迹采样阶段，采样温度 **T=0.6** 在 MuSiQue 上获得最高的平均 Recall@3（27.4，表 13），过高温度（如 1.0）导致生成质量下降，AFM‑MHQA 等模型性能急剧退化。Rollout 规模方面，**rollout size=16** 在验证 AnsF1、Recall 与训练效率之间取得良好平衡（图 7）；进一步增大至 32 带来的额外提升微小，因此将 16 作为默认配置。

#### 验证策略的选择

替代答案的可靠性依赖于验证阶段的多数投票机制。在 **η=3**（5 个验证器中至少 3 个同意）的阈值下，人类一致率达到 **96.0%**（表 8），兼顾了召回与准确。若完全替换为开源验证器集合（GPT‑OSS‑20B、GPT‑OSS‑120B、Qwen3‑30A4B、QwQ‑32B），虽能在 ≥3/4 阈值下达到精度 0.80、召回 0.85 及 0.96 的人类一致性（表 9），但精度下降说明 **开源验证器的可靠性壁垒** 仍是可复现性的瓶颈之一。

### 局限与失败模式

虽然 A²SEARCH 在无标注歧义感知上取得显著增益，但仍存在以下局限：

1. **高计算成本**：自动构建多答案数据需从五个大规模搜索模型生成约 400 万条轨迹（4×H100 GPU 需 74.9 小时，表 5），这对资源受限环境构成门槛。
2. **验证器依赖**：流程全程依赖专有 LLM 作为验证器；完全开源验证器集合的精度有限，可能减少某些场景下的召回‑精度权衡质量。
3. **语言与知识库范围**：当前实验仅基于英文 Wikipedia 知识库验证，未在非英文或多语言、多知识库设定下测试歧义处理的可迁移性。
4. **奖励破解风险**：尽管 α 参数与熵控制可以抑制答案爆炸，但在极端奖励信号分布下，模型仍可能学到启发式而非真正的证据推理，需要进一步研究更鲁棒的奖励塑形。
5. **评估的固有局限**：LMJudge 虽弥补了字面匹配的不足，但其自身的语义判断可能引入新偏差，且对高度开放答案的一致性仍未完全解决。

综上，A²SEARCH 框架通过多答案数据与 AnsF1 奖励的双重创新，显著提升了开放域 QA 模型对歧义问题的感知与适应能力；同时消融与定量分析也指出了当前方案在降低验证成本、强化鲁棒性等方面的改进空间。



## 定位与知识库关联

A²Search 处于开放域多证据问答（QA）与搜索增强强化学习（RL）的交叉点，其核心定位是**首个全自动、无需人工标注的歧义感知 RL 框架**。现有强基线（如 ReSearch、Search‑R1、SinSearch 等）默认训练时每个问题仅有一个正确答案，并通过精确匹配（EM）奖励牵引模型在搜索过程中逼近该唯一答案。然而，A²Search 的分析证实 MuSiQue 训练集中 **27.6% 的样本存在多个有效答案**（our analysis finds that 27.6% of MuSiQue’s training examples admit more than one valid answer），揭示出单答案假设的系统性缺陷：RL 奖励信号在歧义样本上错误惩罚证据支持的答案，模型被迫忽略已检索到的合理信息。

A²Search 通过三个联动改进破解该瓶颈，与基线形成鲜明对照：

- **奖励函数**：将 EM 替换为**答案级 F1（AnsF1）奖励**，通过参数 α 调节精准率与召回率的平衡（outcome rewards are based on answer-level F1, a metric that naturally accommodates multiple answers）。消融表明 α=0.4 使模型在绝大多数情况下保持适中的答案数量；α 过小导致答案爆炸（reward hacking），过大则退化为近乎单答案。
- **训练数据**：放弃单一参考答案，改用**全自动流水线**（采样→过滤→验证→分组）从多模型轨迹中挖掘经证据验证的替代答案（automated pipeline … gathers alternative answers … We then construct the final training data by extending the reference answer set with mined alternative answers）。验证阶段依赖多专有 LLM 多数投票（阈值 η=3 时与人工判断一致性达 96%），确保高质量替代答案。
- **解码策略**：模型在单次 rollout 内**自主决定输出多个答案**，而非依赖多次采样取并集。对歧义问题，A²Search 在一次搜索中显式列出所有证据支持的实体，而 ReSearch 则在多次 rollout 中不断摇摆（Figure 1 的案例对比清晰体现此差异）。

这些变化共同使 A²Search 在构建知识库时内化了歧义感知。系统消融（Table 18）进一步证实多答案数据与 AnsF1 奖励的互补性：仅用 AnsF1 但保留单答案训练（A²SINSearch）能挤出部分歧义收益，但性能远不及其完整框架；而两者均去除（RECALLSearch）效果最差。因此，A²Search 不仅是对搜索 RL 基线的奖励与数据层升级，更重新定义了搜索式 QA 系统的训练范式，将歧义从后处理异化为训练目标本身。

在通用基准上的横向对比强化了其定位：A²Search‑7B 在四个多跳基准上平均 **AnsF1@1 达到 48.4%**，反超 ReSearch‑32B 的 46.2%（+2.2 个百分点）；在 HotpotQA 上领先同量级 ReSearch‑7B 达 10.2 个百分点。更值得注意的是，其对人工精心标注的 AmbigQA 基准（AnsF1@1 48.1）甚至优于直接在 AmbigQA 训练集上训练的模型，证明自动挖掘的歧义模式具有跨数据集泛化力。因此，A²Search 并非仅针对特定集合的微调，而是**在搜索 RL 谱系中引入了一个与知识库歧义正交的通用学习机制**。

### 适用边界

A²Search 的验证建立在明确的实验边界内，适用场景和条件如下：

- **任务与知识源**：仅针对基于英文 Wikipedia 检索的短答案事实性 QA，覆盖单跳（NQ）和多跳（HotpotQA、2Wiki、MuSiQue、Bamboogle）基准。模型依赖搜索工具（经 RL 训练）与环境交互获取证据，因此不适用于无检索或固定上下文生成的设定。
- **歧义模式**：自动流水线能挖掘七类歧义（Under‑Constrained、Granularity Ambiguity、Time Sensitivity、Evidence Conflict、Multi‑Item Response、Open‑Ended、Alias Variance，Table 3），但均限于答案数量变体而非答案间互斥或顺序依赖。对话式歧义、指令歧义等不在其列。
- **模型规模与训练配置**：在 3B 和 7B 参数规模的 Qwen 基础上复现。奖励参数 α=0.4、rollout size=16、采样温度 T=0.6、批次大小 256 等超参数经消融确定为最优或平衡点；超参偏离可导致性能骤降（如 α=0.2 时答案数量不受控，Figure 6）。
- **推理与评估的协调**：因模型可输出多个答案，需采用 AnsF1、Recall 及 LMJudge 语义匹配（以 Qwen2.5‑32B‑Instruct 实现）评估，传统 EM 指标会严重低估模型能力。边界内 AnsF1 计算在多个答案命中同一引用答案时不做重复计数，避免表面字串重叠被利用。

超出以上边界（如非英文、非百科知识源、生成式开放答案）的性能均未经验证，不能假定直接适用。

### 局限与失败模式

1. **专有验证器依赖与开源复现瓶颈**  
   替代答案挖掘的验证阶段完全依赖多个强大专有 LLM 作为多数投票验证器（默认 K=4，η=3）。若改用完全开源的中等规模验证器集合（如 GPT‑OSS‑20B、Qwen3‑30A3B 等），虽保持与人工判断 96% 的一致性，但**精度跌至 0.80、召回跌至 0.85**（Table 9），意味着约 15% 的有效替代答案会在开源设定下丢失，显著削弱数据质量。这导致完全开源复现的性能将低于报告值。

2. **数据处理的高计算开销**  
   流水线需从五个搜索模型（ReSearch‑32B/7B、Search‑R1‑32B/14B/7B）生成约 400 万条轨迹，在 4×H100 GPU 上耗时 74.9 小时（Table 5）。该成本极大限制了向新知识域或新语言的快速迁移。

3. **奖励机制的超参数敏感性与熵崩溃风险**  
   α 的选择直接决定模型的答案数量行为，0.2 以下会导致 reward hacking（答案爆炸），0.8 以上则退化为几乎单答案模式（Figure 6）。尽管通过自适应熵控制（adaptive entropy regularization，Appendix A.2）缓解了基础模型训练中的策略熵过早崩塌，但该机制引入了额外的目标熵 h 和调整步长，增加了调参负担。

4. **评估体系对歧义边界的覆盖有限**  
   LMJudge 虽弥补了字符匹配的刚性，但其自身在多答案语义等价判断上的一致性未充分报告；当前评估假设每条参考答案对等独立，未考虑部分答案可能弱证据支持的情况，可能导致部分有效答案被低估。

5. **歧义类型的泛化不全**  
   自动分类虽区分七类歧义，但训练和评估主要集中在“答案数量可变”的事实性问题，未涵盖推理路径多样导致的不同阶歧义、答案间互斥的歧义（如单一正确选项的选择题）或内容重叠但逻辑冲突的答案。

### 开放问题

以下问题源于当前方法的局限及实验未覆盖的设定，需后续工作单独验证：

- **去专有模型依赖的可复现方案**：能否训练专用验证模型或利用弱监督信号（如检索器置信度）替代专有 LLM 投票，使完全开源复现的精度-召回达到可接受的水平？
- **多语言与跨语料迁移**：A²Search 的整个思路假定知识来源固定且语言单一。当面对多语言 Wikipedia 或完全不同结构的知识库时，自动歧义检测与答案聚类的语义等价判定机制是否仍然可靠，需要结构化的负样本验证。
- **生成式长答案的歧义建模**：当前 AnsF1 奖励仅在短实体答案上定义了自然的重叠度量。如何将类似思路迁移到需生成描述性文本的问答中，答案多样性的捕捉尚为空白。
- **多源工具链下的歧义归因**：当搜索工具超越纯文本检索（如表格查询、代码执行）时，工具自身可能引入新的歧义（例如不同引擎返回冲突结果），此时需要区分“问题固有歧义”与“工具引入歧义”，目前框架未涉及该层次。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A2Search_Ambiguity_Aware_Question_Answering_with_Reinforcement_Learning.pdf

![[paperPDFs/ICLR_2026/A2Search_Ambiguity_Aware_Question_Answering_with_Reinforcement_Learning.pdf]]
