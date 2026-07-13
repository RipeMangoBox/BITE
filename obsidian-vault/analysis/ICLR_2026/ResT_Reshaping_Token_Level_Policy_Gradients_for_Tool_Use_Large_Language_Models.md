---
title: "ResT: Reshaping Token-Level Policy Gradients for Tool-Use Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ResT_Reshaping_Token_Level_Policy_Gradients_for_Tool_Use_Large_Language_Models.pdf
project_link: null
code_link: https://github.com/1229095296/ResT_Tool_use_LLM
openreview_forum_id: gNZlaKRWki
aliases:
- ResT
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "基于熵的Token级梯度重新加权与课程学习，渐进地调节不同区域Token对梯度更新的贡献。"
primary_logic: "低熵的结构化Token是奖励的核心决定因素；通过熵感知的Token重新加权和从结构化Token到推理Token的课程转移，可实现稳定且样本高效的工具使用策略优化。"
claims:
- "理论分析表明策略梯度方差可被Token级熵上界控制，且最优重加权与熵成反比。"
- "在BFCL和API-Bank上，ResT大幅超越GRPO等基线，提升最高达8.76%。"
- "消融实验证实动态奖励、CoT梯度与课程学习均对最终性能有显著贡献。"
- "与GPT-4o等强基线对比，微调ResT的4B模型在BFCL多轮整体准确率上实现超越。"
---

# ResT: Reshaping Token-Level Policy Gradients for Tool-Use Large Language Models

> [!tip] 核心洞察
> 低熵的结构化Token是奖励的核心决定因素；通过熵感知的Token重新加权和从结构化Token到推理Token的课程转移，可实现稳定且样本高效的工具使用策略优化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ResT：重塑工具使用大语言模型的Token级策略梯度 |
| 英文题名 | ResT: Reshaping Token-Level Policy Gradients for Tool-Use Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=gNZlaKRWki) · [GitHub](https://github.com/1229095296/ResT_Tool_use_LLM) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | ResT |
| Dataset | BFCL Multi-Turn, BFCL Single-Turn |

> [!tip] 效果简介
> - BFCL Multi-Turn 上，Overall Acc 为 50.38%，对比 GRPO 41.62%，变化 +8.76%。
> - BFCL Multi-Turn 上，Overall Acc 为 44.25%，对比 GRPO 38.88%，变化 +5.37%。
> - BFCL Multi-Turn 上，Overall Acc 为 50.38%，对比 GPT-4o 50.00%，变化 +0.38%。

## 概要

工具使用已成为大语言模型（LLM）与外部世界交互的核心能力，但通过强化学习（RL）训练工具调用策略时面临一个关键瓶颈：**稀疏的结局奖励与均匀的Token处理方式导致策略梯度方差高、训练效率低**。在多轮工具调用场景中，工具名、参数等结构化Token是决定任务成败的核心要素，其熵值通常较低；而推理链（CoT）Token的熵值较高，对最终奖励的边际贡献相对分散。然而，现有方法（如GRPO）对所有Token施加均匀的梯度权重，使得关键结构化Token的奖励信号被稀释，训练不稳定且样本效率低下。

针对上述问题，本文提出**ResT（Reshaping Token-Level Policy Gradients）**，一种基于熵感知的Token级策略梯度重塑方法。其核心思想是：**低熵的结构化Token是奖励的核心决定因素，通过熵感知的Token重新加权和从结构化Token到推理Token的课程转移，可实现稳定且样本高效的工具使用策略优化**。具体而言，ResT首先从理论上证明了策略梯度方差可被Token级熵的上界所控制，且最优重加权权重与熵成反比（Theorem 1, 2）。基于此，ResT将多轮工具调用分解为单步任务，对每个生成序列按功能区域（格式控制、工具名、参数、推理）计算平均熵，并据此对Token级梯度贡献进行重新加权——训练初期侧重低熵的结构化Token，随训练推进通过轻量级课程逐步将权重转移至高熵的推理Token。

在BFCL和API-Bank两个主流工具使用基准上，ResT展现出显著优势：在BFCL多轮整体准确率上，基于Qwen3-4B的ResT达到50.38%，**相较GRPO提升8.76个百分点**，并**以0.38%的优势超越GPT-4o**（50.00%）；在单轮场景下，ResT超越GPT-4o达4.11%。消融实验进一步证实，动态奖励缩放、CoT梯度更新和课程学习三者均对最终性能有实质性贡献——移除任一组件的性能下降幅度在4.36%至6.54%之间。训练动态分析表明，ResT在保持可比奖励水平的同时，实现了显著更低且更平滑的策略熵，验证了该方法在降低梯度方差和稳定训练方面的有效性。

工具使用能力是大型语言模型（LLM）在实际部署中的核心需求之一。然而，当前基于强化学习（RL）的工具使用策略优化面临一个关键瓶颈：**稀疏的结局奖励与均匀的Token处理方式导致策略梯度方差高、训练效率低下**。具体而言，工具调用任务中决定成败的关键结构化Token——如工具名称、参数键值——其奖励信号被大量高熵的推理文本所稀释，使得模型难以高效地从稀疏反馈中学习。

现有方法对此问题的应对存在明显缺口。主流的组相对策略优化（**GRPO**, Shao et al., 2024）通过组内相对奖励构造基线，消除了对独立价值网络的需求，但其策略梯度对所有Token一视同仁，未区分结构化控制Token与自由形式推理Token在奖励归因上的本质差异。监督微调（SFT）变体如**TSFT**（Huerta-Enochian & Ko, 2024）虽尝试对工具调用Token加重损失，但缺乏对策略探索过程中梯度质量的动态调节机制。这些方法的共同缺陷在于：未能利用Token级信息不对称来主动降低梯度估计的方差。

ResT的动机正源于此。其核心洞察是：**低熵的结构化Token是奖励的核心决定因素**——工具名和参数取值通常具有高度确定的格式，模型在这些位置的概率分布集中（低熵），而它们的正确与否直接决定了任务成败。ResT通过**熵感知的Token级梯度重新加权**与**课程学习**，渐进地调节不同区域Token对梯度更新的贡献：训练初期强调低熵的结构化Token以快速建立正确的工具调用模式，随后逐步将梯度权重转移至高熵的推理Token以优化决策逻辑。这一设计旨在同时实现稳定训练与样本高效的工具使用策略优化。

## 核心方法与创新机理

ResT的核心创新在于**将工具使用任务的策略梯度从均匀的Token级更新重塑为熵感知的差异化更新**，并通过三个紧密结合的“changed slots”实现这一目标：

### 1. 从稀疏结局奖励到逐轮分解的密集规则奖励

传统RL方法（如GRPO）仅依赖整个多轮对话的最终正确/错误信号，奖励稀疏且无法定位错误发生的具体步骤。ResT将多轮任务分解为单步子任务，并为每一步设计**动态缩放的规则奖励**：

- **格式匹配得分**（$S_{i,\mathrm{format}}$）：二进制完全匹配，要求工具调用的所有必填字段按序完整出现。
- **工具调用正确性得分**（$S_{i,\mathrm{acc}}$）：基于Jaccard相似度评估工具名和参数名的预测与真值重叠，并对参数值进行精确匹配，最终归一化为$[0,1]$区间的连续得分。

总奖励为两者的加权和，且奖励值根据任务难度动态缩放，使得每一步都能获得有效的监督信号。消融实验表明，移除动态奖励缩放使Qwen3-8B准确率下降**6.54%**（Table 3），验证了密集奖励对训练的关键作用。

### 2. 从均匀Token权重到熵感知的Token级梯度重塑

GRPO等基线方法对序列中所有Token赋予均匀的策略梯度贡献权重，忽略了不同功能区域Token对奖励的决定性差异。ResT的理论分析（Theorem 1, 2）揭示了两个关键洞察：

- **策略梯度方差上界**可被Token级熵控制：$\operatorname{Var}(g_i^{(\mathrm{rw})}) \leq \mathbb{E}[\hat{A}_i^2] \sum_{t} \beta_t (\tilde{w}_t)^2$，其中$\beta_t$与Token熵$H_t$相关。
- **最优重加权规则**与$\beta_t$成反比：$\tilde{w}_t^{\star} \propto 1/\beta_t$，实践中用区域平均熵近似为$\tilde{w}_t \propto 1/(1 - e^{-H_{\mathrm{avg}}})$。

基于此，ResT根据Token所属的功能区域（推理、工具名、参数、格式控制符）计算平均熵，对**低熵的结构化Token（如工具名、参数）赋予高权重**，对**高熵的推理Token赋予低权重**。这确保了奖励信号的关键决定因素——工具调用的正确性——在梯度更新中获得应有的强调。

### 3. 从静态权重到课程学习的渐进式知识转移

仅靠静态的熵感知权重可能导致模型过早锁定于结构化模式，忽视推理能力的培养。ResT引入**轻量级课程学习**，动态调整不同区域的权重：

- **训练初期**：重点强化低熵的结构化Token（格式、工具名、参数），快速建立正确的工具调用格式。
- **训练后期**：逐步提升高熵推理Token的权重，将学习重心从“调用什么工具”转移到“如何推理出正确的调用”。

消融实验证实，将课程学习替换为恒定权重导致准确率下降**4.86%**（Table 3），而SFT预热结合调优后的课程策略在Qwen3-1.7B上达到**17.62%**的BFCL Overall Acc（Table 4），验证了渐进式知识转移的必要性。

### 4. 移除KL正则化的隐式稳定性机制

与GRPO不同，ResT的目标函数中**移除了KL惩罚项**，转而依赖熵感知重加权、裁剪机制和课程学习的组合来隐式调节探索-利用平衡。实验表明（Figure A.1, Table A.1），该设计在保持训练稳定性的同时避免了额外超参数的调优负担。

### 创新总结

三个changed slots形成因果闭环：**密集的逐轮规则奖励**提供了丰富的学习信号；**熵感知的Token重加权**将这些信号精准导向对任务成功最关键的结构化Token；**课程学习**则确保模型在掌握工具调用格式后，仍能发展出必要的推理能力。这一组合使ResT在相同数据预算下，相比GRPO在BFCL上提升最高达**8.76%**，并在4B模型上超越GPT-4o。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_gNZlaKRWki/figures/001_Figure_1.jpg]]
*Figure 1: ResT decomposes multi-turn tool-use tasks into single-turn tasks and further reshapes the policy gradient according to the average entropy in different regions, enabling dense and effective reward signals*

ResT 的整体设计围绕一个核心矛盾展开：工具使用任务中，稀疏的结局奖励和均匀的 Token 处理方式导致策略梯度方差高、训练效率低，尤其关键的结构化 Token（工具名、参数）的奖励信号被稀释。为解决这一问题，ResT 构建了一个从任务分解到梯度重塑的完整流水线，其运作逻辑可概括为“分解—评分—重加权—优化”四步闭环。

**任务分解模块**首先将多轮工具调用对话分解为独立的单步任务。这一设计的动机在于：多轮交互的全局奖励信号过于稀疏，无法为中间步骤提供有效监督；分解后，每一步均可获得即时、细粒度的反馈，从而将稀疏的结局奖励转化为逐轮的密集信号（见 Section 3.2 引言及 Section 4.1）。

**规则奖励计算模块**为每个单步任务生成两类得分：格式匹配得分和工具调用正确性得分。格式得分采用二进制完全匹配——当且仅当所有必需字段按序完整出现时得 1 分（Equation 10）。工具调用正确性得分则基于 Jaccard 相似度计算工具名和参数名的匹配程度，并对参数值进行精确匹配，最终归一化为一个介于 0 到 1 之间的标量（Equation 13）。总奖励为两者的加权和。值得注意的是，该奖励函数完全基于规则，无需训练额外的奖励模型，但也因此无法捕捉语义等价但语法不同的正确输出。

**组优势估计模块**沿用 GRPO 的组内相对奖励思想：对每个输入采样一组响应，计算组内标准化优势 $\hat{A}_i$（Equation 15），以此作为后续策略梯度更新的方向信号。

**熵感知 Token 重新加权与课程调整模块**是 ResT 的核心创新。其理论依据在于：策略梯度方差可被 Token 级熵的上界所控制，且最优重加权权重与各 Token 的方差贡献成反比（Theorem 2, Equation 7）。实践中，ResT 使用区域平均熵作为方差贡献的代理，按 $\tilde{w}_t \propto 1/(1 - e^{-H_{\mathrm{avg}}})$ 初始化权重（Equation 9），使得低熵的结构化 Token（工具名、参数）获得更高权重，而高熵的推理 Token 初始权重较低。随后，课程学习机制根据训练进度动态调整各区域的权重分配，逐步将学习重点从结构化 Token 转移至推理 Token，实现从“学会调用”到“学会推理”的渐进式能力构建。

**重加权 PPO 目标优化模块**将上述 Token 级权重嵌入裁剪后的 PPO 目标，形成最终损失函数（Equation 19）。值得关注的是，ResT 有意移除了 GRPO 中原有的 KL 惩罚项，转而依靠熵感知重加权、裁剪机制和课程学习三者共同维持训练稳定性。消融实验表明，在保持其他组件不变的情况下，省略 KL 惩罚的训练过程依然稳定且性能最佳（Figure A.1, Table A.1），这暗示熵感知重加权本身已能有效调节探索与利用的平衡。

综上，ResT 的流水线通过“分解获取密集信号→规则评分提供结构化反馈→熵感知重加权降低方差→课程学习引导能力迁移”的因果链条，实现了工具使用策略优化的稳定性与样本效率的双重提升。整个框架的输入为多轮工具调用对话，输出为经 Token 级重加权策略梯度优化后的模型参数，各模块间的数据流关系可参照 Figure 1 的示意。

### 理论动机：Token级梯度方差与熵的关系

ResT的设计起点是对策略梯度估计量方差的理论分析。对于包含 $G$ 条轨迹的小批量，策略梯度估计量 $\widehat{\nabla J}^{(k)}$ 的方差可分解为：

$$\operatorname{Var}(\widehat{\nabla J}^{(k)}) = \frac{1}{G} \operatorname{Var}(g_i^{(k)})$$

其中 $g_i^{(k)} = \sum_t \nabla_\theta \log \pi_\theta(a_t^{(i)}|s_t^{(i)}) \hat{A}_i$ 是单条轨迹的梯度贡献。核心洞察在于：每个时间步的评分函数 $\|s_t\|^2$ 的期望与Token熵 $H_t$ 存在上界关系：

$$\mathbb{E}[\|s_t\|^2] \leq 1 - e^{-H_t}$$

这表明**低熵Token（如工具名、参数名）的梯度方差贡献更小，而高熵Token（如自由推理文本）的方差贡献更大**。基于此，引入Token级重加权 $\tilde{w}_t$ 后，梯度估计量的方差上界为：

$$\operatorname{Var}(g_i^{(\mathrm{rw})}) \leq \mathbb{E}[\hat{A}_i^2] \sum_{t} \beta_t (\tilde{w}_t)^2$$

其中 $\beta_t$ 表征各Token的方差贡献。在归一化约束 $\sum_t \tilde{w}_t = T$ 下，最小化该上界的最优权重具有闭式解：

$$\tilde{w}_t^{\star} = \frac{T}{\sum_u \beta_u^{-1}} \cdot \frac{1}{\beta_t}$$

即**最优Token权重与方差贡献 $\beta_t$ 成反比**。由于 $\beta_t$ 难以直接估计，实践中采用区域平均熵作为代理，得到可操作的熵感知重加权规则：

$$\tilde{w}_t \propto \frac{1}{1 - e^{-H_{\mathrm{avg}}}}$$

这一规则使得结构化、低熵的控制Token获得更高权重，而开放式推理Token获得较低权重。

---

### 奖励信号设计：从稀疏结局到逐轮密集评分

传统工具使用RL仅依赖稀疏的结局奖励（整体正确/错误），导致有效学习信号极度稀缺。ResT将多轮对话分解为单步任务后，为每步设计基于规则的密集奖励，由两部分加权组合：

**格式匹配得分** $S_{i,\mathrm{format}}$ 为二值评分：

$$S_{i,\mathrm{format}} = \begin{cases} 1, & \text{if all required fields are complete in order} \\ 0, & \text{otherwise} \end{cases}$$

**工具调用正确性得分** $S_{i,\mathrm{acc}}$ 基于Jaccard相似度与精确值匹配归一化计算：

$$S_{i,\mathrm{acc}} = \frac{r_{\mathrm{name}} + r_{\mathrm{para}} + r_{\mathrm{value}}}{1 + |G| + \sum |\mathbf{v}(G_i)|}$$

其中 $r_{\mathrm{name}}$ 为预测工具名集合与真值工具名集合的Jaccard相似度，$r_{\mathrm{para}}$ 为各工具参数名集合的Jaccard相似度之和，$r_{\mathrm{value}}$ 为参数值精确匹配的计数。该设计使得即使工具调用部分正确，也能获得成比例的正向反馈，从而提供密集的梯度信号。

---

### 熵感知Token重加权与课程学习

ResT将生成序列按功能划分为四个区域：推理（CoT）、工具名、参数、最终响应。每个区域的初始权重由区域平均熵决定——低熵的结构化区域获得更高初始权重。权重归一化方式为：

$$\bar{w} := \frac{1}{|T|} \sum_{t=1}^{T} \hat{w}_t, \quad w_t = \frac{\hat{w}_t}{\bar{w} + \delta}$$

其中 $\delta$ 为防止除零的小常数。

**课程学习**是ResT的关键机制：训练初期重点强化低熵的结构化Token（工具名、参数），确保模型快速掌握正确的工具调用格式；随着训练推进，逐步提升推理Token的权重，使模型学会在正确调用工具的同时生成高质量的推理链。这一从结构化Token到推理Token的渐进转移，在消融实验中贡献了4.86%的性能提升（移除课程学习后Qwen3-8B准确率下降4.86%）。

---

### 重加权PPO目标与KL正则化的移除

ResT的最终优化目标为Token级重加权的裁剪PPO损失：

$$\mathcal{L}_{\mathrm{ResT}}(\theta) = -\frac{1}{G} \sum_{i} \sum_{t} \frac{\omega_t}{T} \cdot \min\left(r_{i,t} \hat{A}_i, \mathrm{clip}(r_{i,t}, 1-\epsilon, 1+\epsilon) \hat{A}_i\right)$$

其中 $r_{i,t}$ 为新旧策略的概率比，$\hat{A}_i$ 为组优势估计（利用组内相对奖励计算标准化优势），$\omega_t$ 为经课程学习调整后的Token权重。

值得注意的是，ResT**显式移除了GRPO中的KL惩罚项**。设计者认为，熵感知重加权、裁剪机制与课程学习的组合已能充分调控探索-利用平衡，无需额外的KL正则化。消融实验证实，省略KL惩罚后训练仍稳定且性能最佳（Table A.1），进一步验证了这一设计选择。

---

### 核心模块流程总结

ResT的完整训练流程包含五个关键模块：

1. **多轮到单轮分解**：将多轮对话拆解为单步任务，为每步提供独立监督
2. **规则奖励计算**：基于格式匹配和工具调用正确性计算密集得分
3. **组优势估计**：利用组内相对奖励计算标准化优势
4. **熵感知Token重加权与课程调整**：根据区域平均熵初始化权重，按训练进度动态调度
5. **重加权PPO目标优化**：基于Token级重加权和裁剪计算损失并更新参数

这一流水线使得ResT在稀疏结局奖励的工具使用场景中，实现了稳定且样本高效的策略优化。

## 实验与关键发现

### 主实验结果

ResT在BFCL多轮和API-Bank两个基准上均展现出相对于现有方法的显著优势。Table 1报告了BFCL多轮基准的核心结果：在Qwen3-4B-2507上，ResT取得50.38%的整体准确率，较**GRPO**（Shao et al., 2024）的41.62%提升8.76个百分点，较**Dr.GRPO**（Liu et al., 2025c）的45.75%提升4.63个百分点。这一优势在更大规模的模型上同样保持——Qwen3-14B上ResT达到44.25%，GRPO为38.88%，提升5.37个百分点。值得注意的是，基于Qwen3-4B-2507微调的ResT在BFCL多轮整体准确率上以0.38个百分点的微弱优势超越GPT-4o（50.00%），在单轮任务上则领先GPT-4o达4.11个百分点。

在API-Bank测试集（Table 2）上，ResT在所有模型尺寸上均取得最优整体准确率：Qwen3-1.7B为64.99%，4B为68.68%，8B为70.69%，14B为69.35%。相较于GRPO，ResT在API-Bank上的最大提升幅度为3.02个百分点。跨模型族的泛化能力在Llama3.2-3B-Instruct上得到验证（Table D.2），ResT以62.81%的整体准确率优于GRPO的59.13%。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_gNZlaKRWki/figures/004_Table_2.jpg]]
*Table 2: API-Bank Test Results. The results presented correspond to the highest score achieved by each method with its optimal hyperparameter settings. The evaluation dataset consists of 399 samples for Level 1, 67 for Level 2, and 131 for Level 3. Best in bold*

Figure F.1的训练动态曲线揭示了ResT稳定性的内在机制：相比GRPO，ResT的策略熵显著更低且更平滑，同时维持可比的奖励水平和更长的响应长度。这表明熵感知的Token重新加权有效抑制了策略的过度探索，在不牺牲性能的前提下实现了更稳定的训练。

### 消融实验

Table 3系统拆解了ResT各组件的贡献。在Qwen3-8B上，移除动态奖励缩放导致准确率下降6.54个百分点；禁用CoT区域的梯度更新使准确率降低4.36个百分点；将课程学习替换为恒定权重则带来4.86个百分点的性能损失。三个组件的消融结果一致表明，动态奖励、CoT梯度与课程学习对最终性能均有不可替代的贡献。

Table 4进一步考察了初始化策略与课程对齐的交互效应。在Qwen3-1.7B上，冷启动ResT（无SFT预热）达到15.75%的整体准确率；SFT预热配合原始课程提升至15.25%；而SFT预热配合调优课程（Tuned Curriculum）取得最优的17.62%，相比基础模型（8.62%）提升超过一倍。这一结果表明SFT初始化和课程学习之间存在协同效应——SFT为模型提供了合理的初始策略分布，使得后续的熵感知梯度重塑能够更有效地发挥作用。

关于KL正则化的角色，Table A.1显示ResT在移除KL惩罚项后仍保持最佳性能（50.38%），而引入KL损失（β=0.003）反而使准确率略微降至50.25%，更高的β值则进一步损害性能。这一发现验证了ResT的设计选择：熵感知的Token重新加权、裁剪机制与课程学习的组合足以维持训练稳定性，无需额外的KL约束。

### 关键图表结论

- **Table 1 & Table 2**：ResT在BFCL和API-Bank上一致超越GRPO、Dr.GRPO等强基线，且在4B规模上达到与GPT-4o可比甚至更优的水平。
- **Table 3**：动态奖励缩放是贡献最大的单一组件（下降6.54%），课程学习次之（下降4.86%），CoT梯度更新紧随其后（下降4.36%）。
- **Table 4**：SFT预热与调优课程的组合产生协同增益，验证了分阶段训练策略的有效性。
- **Figure F.1**：ResT通过熵感知加权实现更低更平滑的策略熵，从训练动态角度解释了其稳定性优势。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_gNZlaKRWki/figures/003_Table_1.jpg]]
*Table 1: BFCL multi-turn results (updated June 14, 2025). Metrics computed with official scripts. TSFT scales loss on tool-call tokens. RSFT scales loss on reasoning tokens. Best in bold*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_gNZlaKRWki/figures/005_Table_3.jpg]]
*Table 3: API-Bank Test Results for Relaxations. No dynamic reward denotes no dynamic scaling reward value. No gradients for CoT denotes no gradient update for chain-of-thought. No curriculum learning assigns a constant weight to each segment. Best in bold*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_gNZlaKRWki/figures/006_Table_4.jpg]]
*Table 4: Ablation study on ResT initialization strategies and curriculum alignment on the BFCL benchmark with Qwen3-1.7B. SFT warm-starting combined with a Tuned Curriculum (Tuned Curr.) achieves the best performance, demonstrating a synergistic effect. Average performance is calculated using the official scripts*

### 失败模式与局限

尽管ResT在结构化工具调用任务上表现优异，其设计存在以下边界：

1. **区域划分依赖**：方法假设输出可清晰划分为推理、工具调用和最终响应区域。当模型输出格式不规范或工具调用嵌入在自由文本中时，基于规则的区域划分可能失效，导致权重分配失准。

2. **规则奖励的语义盲区**：奖励函数完全基于格式匹配和Jaccard相似度，无法捕捉语义等价但语法不同的正确输出。例如，参数值的同义表达可能被错误判为不匹配。

3. **多轮分解的信息损失**：将多轮对话分解为单步任务虽然提供了密集监督，但可能丢失跨步依赖信息。在需要长程规划或错误恢复的复杂场景中，这一简化可能限制策略的全局最优性。

4. **真实环境泛化未验证**：当前评估局限于BFCL和API-Bank两个受控基准，在真实世界的动态工具调用场景中的效果仍需进一步实证。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_gNZlaKRWki/figures/020_Figure_9.jpg]]
*Figure 9: Figure F.1: Learning curves for ResT and GRPO during training steps. The training dynamics show that ResT achieves a significantly lower and smoother policy entropy compared to GRPO, while maintaining comparable reward performance and longer responses*

## 定位与知识库关联

### 工具使用LLM的强化学习基线谱系

ResT的方法设计建立在工具使用LLM的强化学习训练框架之上，其核心基线包括监督微调（SFT）和组相对策略优化（GRPO）两类。

在SFT方向，除了标准SFT外，**TSFT**（Huerta-Enochian & Ko, 2024）通过对工具调用Token加重损失来强调结构化输出，而**RSFT**则对推理Token加重损失。这两种加权SFT变体分别代表了“重视工具调用”和“重视推理”两种直觉策略，但均缺乏对Token重要性的动态、自适应判断。

在RL方向，**GRPO**（Shao et al., 2024）是无批评家（critic-free）的组相对策略优化方法，通过组内奖励标准化计算优势函数，并包含KL惩罚项以约束策略偏离。**Dr.GRPO**（Liu et al., 2025c）进一步移除了GRPO中的标准差归一化，改用均值中心化的估计器。这些方法在工具使用任务中面临共同瓶颈：稀疏的结局奖励导致策略梯度方差高，且所有Token被均匀处理，使得关键结构化Token（如工具名、参数）的奖励信号被稀释。

ResT相对于上述基线的关键改进体现在三个维度：

1. **奖励信号**：从稀疏的结局奖励转变为逐轮分解的、基于规则的格式与工具调用正确性得分（动态缩放），提供更密集的监督信号。
2. **Token贡献权重**：从均匀权重（仅由重要性采样比率决定）转变为基于区域平均熵的Token重新加权，并引入课程学习动态调整不同区域的权重。低熵的结构化Token（工具名、参数）在训练初期获得更高权重，而高熵的推理Token权重随训练逐步提升。
3. **KL正则化**：移除了GRPO中的KL惩罚项，依赖熵感知重新加权与裁剪机制维持训练稳定性。消融实验证实，该设计选择在保持训练稳定的同时取得了最佳性能。

### 适用边界与局限

ResT的设计依赖于以下前提条件，这些条件界定了其适用边界：

1. **任务可分解性**：方法需要将多轮对话分解为单步任务以提供逐步监督。对于无法清晰分解为独立步骤的连续对话场景，该分解可能丢失跨步依赖信息。
2. **明确的工具调用格式**：奖励函数完全基于规则（格式匹配得分和Jaccard相似度），要求输出具有结构化的工具调用字段。对于完全自由形式的对话或需要语义等价判断的任务，规则奖励可能无法捕捉语法不同但语义正确的输出。
3. **Token区域可划分**：熵感知重新加权依赖于将Token划分为推理、工具调用、最终响应等功能区域。当工具集动态变化或任务边界模糊时，区域划分和权重初始化可能需要重新设计。

### 开放问题

1. **向开放式语言Agent的推广**：如何将熵引导的Token重新加权推广至使用学习式或偏好奖励模型的开放式语言Agent任务，是方法泛化的重要方向。
2. **课程学习的自动化**：当前课程学习依赖预设的权重调度策略。能否根据在线熵估计自适应地调度权重变化，使课程学习完全自动化，值得进一步探索。
3. **复杂规划与错误恢复的鲁棒性**：该方法在多步规划、工具调用失败后的错误恢复等更复杂场景中的鲁棒性尚未充分验证。
4. **动态工具集的适应性**：当可用工具集在推理时动态变化时，Token区域划分和权重初始化策略是否需要重新设计，是一个实际部署中需要解决的问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/ResT_Reshaping_Token_Level_Policy_Gradients_for_Tool_Use_Large_Language_Models.pdf]]
