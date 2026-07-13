---
title: "AutoTool: Automatic Scaling of Tool-Use Capabilities in RL via Decoupled Entropy Constraints"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AutoTool_Automatic_Scaling_of_Tool_Use_Capabilities_in_RL_via_Decoupled_Entropy_Constraints.pdf
project_link: null
code_link: null
openreview_forum_id: zFkopTvclB
aliases:
- AutoTool
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "策略模型的熵（探索能力）与推理坍塌高度正相关；通过解耦短推理与长推理的熵约束，并对长推理路径自适应调节熵惩罚系数，可以控制思考长度。"
primary_logic: "利用解耦自适应熵约束策略，模型能够根据问题难度自动调整推理规模：对简单问题保持简洁输出，对复杂问题进行更长推理，从而同时提升准确率并大幅降低推理计算成本。"
claims:
- "直接 RL 训练在工具使用中导致响应长度随训练步数急剧下降（推理坍塌），与数学任务中长度随准确率提升的趋势相反。"
- "低熵与推理坍塌强正相关，且该现象独立于样本难度分布。"
- "解耦自适应熵约束策略在 BFCL 基准上相比 PubTool-SFT 提升 +11.95% 整体准确率，在 Multi-Turn 场景提升 +28.5%。"
- "AutoTool 相比蒸馏模型在准确率提升 9.8% 的同时，推理 token 成本削减约 81%。"
---

# AutoTool: Automatic Scaling of Tool-Use Capabilities in RL via Decoupled Entropy Constraints

> [!tip] 核心洞察
> 利用解耦自适应熵约束策略，模型能够根据问题难度自动调整推理规模：对简单问题保持简洁输出，对复杂问题进行更长推理，从而同时提升准确率并大幅降低推理计算成本。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AutoTool：通过解耦熵约束实现在强化学习中工具使用能力的自动扩展 |
| 英文题名 | AutoTool: Automatic Scaling of Tool-Use Capabilities in RL via Decoupled Entropy Constraints |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=zFkopTvclB) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | AutoTool |
| Dataset | BFCL, ACEBench |

> [!tip] 效果简介
> - BFCL 上，Overall Acc 为 70.12，对比 PubTool-SFT 58.17，变化 +11.95。
> - BFCL 上，Multi-Turn Acc 为 38.18，对比 PubTool-SFT 9.68，变化 +28.5。
> - BFCL 上，Overall Acc 为 70.12，对比 Base (Qwen2.5-7B-Instruct) 53.69，变化 +16.43。

## 概要

在工具使用（tool-use）任务中，大语言模型面临一个两难困境：直接强化学习（RL）训练会导致**推理坍塌**——模型的响应长度随训练步数急剧缩短，无法为复杂问题维持必要的长程推理；而蒸馏（distillation）模型虽然能保持长推理，却在简单问题上过度思考，产生大量冗余 token，造成严重的推理资源浪费。这一现象与数学推理任务中“准确率提升伴随响应长度自然增长”的趋势截然相反（Figure 1）。

本工作揭示了推理坍塌的核心机制：策略模型的**熵**（探索能力）与坍塌高度正相关，且该关联独立于样本难度分布（Figure 2）。低熵意味着模型过早收敛到确定性短输出，丧失了探索更长推理路径的能力。基于此，论文提出 **AutoTool**——一种通过**解耦自适应熵约束**实现推理规模自动扩展的强化学习训练范式。其核心思想是：对短推理和长推理路径施加差异化的熵约束，并对长路径自适应调节熵惩罚系数，使模型能根据问题难度自动决定“思考”与否及思考深度。

在方法定位上，AutoTool 构建了一条“暖启动 SFT → 解耦熵约束 RLVR → 自动思维奖励”的完整训练流水线。相比标准 GRPO 训练，其关键改进包括：在奖励函数中引入非对称设计以鼓励正确时的简洁输出、惩罚错误时的短响应；通过数据精炼剔除与模型学习轨迹不对齐的样本以提升训练稳定性；以及通过 `[mode]` 标签实现推理时可控制的 think / no_think 模式切换。

主要实验结果（基于 Qwen2.5-7B-Instruct 基座，BFCL 基准）表明：AutoTool 相比 PubTool-SFT 整体准确率提升 **+11.95%**，多轮对话场景提升 **+28.5%**；相比蒸馏模型在准确率提升 **9.8%** 的同时，推理 token 成本削减约 **81%**。消融实验证实，解耦熵约束、自适应系数和数据精炼三者均对最终性能有显著贡献。该方法在 1.5B 至 32B 多种模型规模上均展现出一致的泛化增益。



### 工具使用中的测试时扩展困境

大语言模型（LLM）在工具使用（Tool-Use）任务中展现出巨大潜力，但如何有效扩展其推理能力以应对复杂多轮交互仍然是一个核心挑战。现有训练范式主要面临两个相互矛盾的问题：**推理坍塌**（Reasoning Collapse）与**过度推理**（Over-Thinking）。

在数学推理领域，直接强化学习（RL）训练能够使模型的响应长度随着准确率提升而自然扩展，实现有效的测试时扩展（Test-Time Scaling, TTS）。然而，这一规律在工具使用任务中完全失效。如 **Figure 1(b)** 所示，直接 RL 训练（以 GRPO 为代表）导致模型的响应长度随训练步数急剧下降——模型倾向于输出越来越短的推理轨迹，最终坍塌为几乎不包含思考过程的简短响应。这种“推理坍塌”现象严重限制了模型在复杂多轮工具调用场景中的表现。

与此同时，另一种主流方案——蒸馏模型（Distilled SFT）——虽然通过模仿长推理轨迹获得了更强的推理能力，却走向了另一个极端。如 **Figure 1(c)** 所示，蒸馏模型对所有问题（包括简单问题）都生成长篇推理，输出 token 成本相比基座 SFT 模型增加超过 10 倍，造成严重的推理资源浪费。这种“一刀切”的长推理策略在计算效率上显然不可持续。

### 推理坍塌的深层机制

为探究推理坍塌的成因，研究者对训练动态进行了细粒度分析。如 **Figure 2** 所示，将训练数据按难度划分为 Easy、Medium、Hard 三个子集后发现：尽管 Easy 和 Medium 子集在准确率上成功收敛，Hard 子集却未能收敛；更关键的是，**响应长度的坍塌在所有三个难度子集中均一致发生**（Figure 2(c)），且与策略模型的熵（Entropy）下降趋势高度同步（Figure 2(d)）。这表明：

1. **推理坍塌独立于样本难度分布**——不是“只对难题放弃思考”，而是对所有问题都系统性缩短推理。
2. **低熵与推理坍塌呈强正相关**——策略熵的快速下降是坍塌的直接信号。当模型熵过低时，生成策略趋于确定性，丧失了探索不同推理路径的能力，从而无法维持有效的长推理。

进一步的干预实验证实了这一因果链条。如 **Figure 3** 所示，直接对响应长度施加惩罚（Length Penalty）并不能缓解低熵问题，反而可能导致训练不稳定；而引入**熵约束**（Entropy Constraint）可以部分恢复响应长度，说明熵是控制推理长度的有效“因果旋钮”。

### 现有方法的缺口

综合来看，工具使用领域的测试时扩展面临以下方法缺口：

- **直接 RL 训练**（如 GRPO）会导致推理坍塌，无法自动扩展推理规模，在 Multi-Turn 等复杂场景中表现极差（如 **Table 1** 所示，GRPO 在 Multi-Turn 上仅 8.38%，远低于蒸馏 SFT 的 16.95%）。
- **蒸馏 SFT** 虽然提升了推理能力，但缺乏自适应机制，对所有问题无差别地生成长推理，推理成本过高。
- **固定熵约束**虽然能部分缓解坍塌，但对熵惩罚系数高度敏感（**Table 1**），且无法区分简单问题与复杂问题对推理规模的不同需求——统一的熵约束要么抑制了简单问题的效率，要么无法充分保护复杂问题的探索能力。

### 本文动机

基于上述分析，本文的核心动机是：**设计一种能够根据问题难度自动调整推理规模的训练范式**，使模型对简单问题保持简洁输出，对复杂问题进行充分推理，从而同时提升准确率并大幅降低推理计算成本。这一目标要求方法能够：

1. **解耦**短推理与长推理的熵约束，避免目标冲突。
2. **自适应**调节长推理路径的熵惩罚强度，防止过度约束或约束不足。
3. 在 RL 训练过程中维持策略的探索能力，从根本上防止推理坍塌。



## 核心方法与创新机理

AutoTool 的核心创新在于揭示并解决了工具使用任务中强化学习（RL）训练特有的**推理坍塌**问题，并提出了一套**解耦自适应熵约束**策略，使模型能够根据问题难度自动调节推理规模。

### 问题发现：工具使用 RL 中的推理坍塌

与数学推理任务中 RL 训练能有效延长推理链路的趋势不同，在工具使用任务中直接应用 GRPO 训练会导致**响应长度随训练步数急剧下降**（Figure 1b），即推理坍塌。进一步分析表明，这一坍塌现象**独立于样本难度分布**——在简单、中等、困难三个子集上均出现响应长度下降（Figure 2c），且**低熵与推理坍塌呈强正相关**（Figure 2d）。这意味着，策略模型的探索能力丧失是导致模型无法维持有效推理的核心瓶颈。

### 方法创新：三个关键 changed slots

#### 1. 解耦自适应熵约束（核心算法创新）

**Baseline（标准 GRPO）**：无额外熵正则，策略优化仅依赖奖励信号。

**AutoTool**：将推理路径解耦为短推理（short）和长推理（long）两类，施加差异化的熵约束：

- **短推理路径**使用固定系数 $\beta_s$，当熵低于阈值 $H_s$ 时激活熵惩罚；
- **长推理路径**使用自适应系数 $\beta_l$，根据实际熵与目标熵 $H_l$ 的偏差动态调整惩罚强度。

熵系数计算方式为：
$$\beta_i = \beta_s \cdot m_i \cdot \mathbb{I}\{H_i \leq H_s\} + \beta_l \cdot (1 - m_i) \cdot \mathbb{I}\{H_i \leq H_l\}$$

策略损失中加入解耦熵惩罚项：
$$\mathcal{L}_{\mathfrak{p}} = \frac{1}{N} \sum_{i=1}^{N} [ - \min( \rho_i \hat{A}_i, \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon) \cdot \hat{A}_i ) - \beta_i H_i ]$$

自适应系数 $\beta_l$ 通过额外损失更新：
$$\mathcal{L}_{\beta}^{l} = \frac{1}{\sum_j (1-m_j)} \sum_{i=1}^{N} (1-m_i) \cdot \beta_l \cdot (H_i - H_l)$$

**关键证据**：消融实验（Table 4）表明，移除解耦（使用统一熵约束）导致整体准确率下降 5.89%，多轮对话下降 10.53%；移除自适应系数（使用固定熵系数）导致整体准确率下降 2.34%。固定熵约束对系数敏感（Table 1），验证了自适应调节的必要性。

#### 2. 非对称自动思维奖励（奖励函数创新）

**Baseline**：仅基于答案正确性给予二元奖励。

**AutoTool**：设计非对称奖励函数，引导模型在正确时倾向简洁输出、在错误时鼓励深度思考：
$$\mathcal{R}_{\mathrm{answer}}(o_i) = \begin{cases} +1.0, & \text{if } o_i = y^*, \text{no-think}, \\ +0.5, & \text{if } o_i = y^*, \text{think}, \\ -0.5, & \text{if } o_i \neq y^*, \text{think}, \\ -1.0, & \text{if } o_i \neq y^*, \text{no-think} \end{cases}$$

该设计通过奖励差异显式编码了“简单问题无需思考、复杂问题值得思考”的偏好，与解耦熵约束形成协同。

#### 3. 暖启动 SFT + RL 数据精炼（数据策略创新）

**Baseline**：原始工具使用数据直接进入 RL 训练。

**AutoTool**：
- **暖启动 SFT**：构建混合长/短推理数据的 PubTool 数据集，使模型初步感知样本难度并学习自动选择 think/no_think 模式（Section 3.1）。
- **RL 数据精炼**：从 21k 样本下采样至 7k，剔除过易/过难样本，基于**奖励方差**筛选与模型学习轨迹高度对齐的高质量样本（Section B）：
  $$\operatorname{Var}(r) = \frac{1}{n-1} \sum_{i=1}^{n} (r_i - \mu_r)^2$$

**关键证据**：移除数据精炼导致整体准确率下降 6.43%，多轮对话下降 11.34%（Table 4），是影响最大的单一组件。数据精炼使准确率奖励提高 15%，训练波动显著减小（Figure 9）。

### 推理模式可控性

AutoTool 通过 `[mode]` 标签实现 think/no_think 可控推理（Figure 4），推理时可通过前缀切换模式。这使得模型既能在需要时进行深度思考，又能在简单场景下保持极低 token 成本——相比蒸馏模型 token 成本削减约 81%，同时准确率提升 9.8%（Figure 6）。



![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_zFkopTvclB/figures/013_Figure_4.jpg]]
*Figure 4: The overview of decoupled adaptive entropy constraint. It achieves automatic scaling by decoupling different reasoning modes through the application of differentiated entropy constraints. Adaptive entropy constraint strength for long reasoning. During the inference, the model can automatically or controllably switch inference modes by pre-pending a response prefix in Input tokens*

AutoTool 的整体框架围绕一个核心矛盾展开：直接强化学习（RL）训练在工具使用任务中会导致**推理坍塌**（reasoning collapse）——模型响应长度随训练步数急剧缩短，无法为复杂问题维持必要的探索能力；而蒸馏模型则在所有问题上均产生冗长推理，造成严重的 token 成本浪费。为解决这一问题，AutoTool 构建了一条“感知难度 → 解耦约束 → 自适应扩展”的完整训练管线。

### 管线总览

如图 4 所示，AutoTool 的完整管线由四个核心模块串联而成：

1. **数据准备与暖启动 SFT**：构建 PubTool 混合数据集（长推理与短推理轨迹混合），通过监督微调使基座模型初步感知样本难度，并学习自动选择 think / no_think 推理模式。
2. **RL 数据精炼**：对训练数据进行质量筛选，剔除过易或过难的样本，并基于奖励方差（reward variance）保留与模型学习轨迹高度对齐的高质量样本，将 RL 训练集从约 21k 压缩至 7k。
3. **解耦自适应熵约束 RLVR**：在 GRPO 算法基础上，对短推理路径和长推理路径施加差异化的熵约束，并对长路径的熵惩罚系数 β_l 进行自适应调节，以维持策略的探索能力。
4. **自动思维奖励模块**：通过格式奖励和非对称答案奖励引导模型正确使用 think/no_think 格式，鼓励在简单问题上保持简洁输出，在复杂或错误情况下触发更长推理。

### 模块间的输入输出流

管线以基座模型（如 Qwen2.5-7B-Instruct）和原始工具使用训练数据为起点。数据首先经过**数据准备模块**，通过多轮推理采样生成长/短混合轨迹，并标注 [mode] 标签以区分 think 与 no_think 模式，形成 PubTool 数据集。该数据集同时包含统计信息（如各子集上的思考率），用于后续分析。

暖启动 SFT 阶段，模型在 PubTool 混合数据上训练，输出一个具备初步难度感知能力的策略模型。这个 SFT 模型随后进入**RL 数据精炼模块**：对训练集中每个样本进行多次采样，计算奖励方差，剔除方差过高的“未对齐”样本，仅保留方差低、奖励信号稳定的样本。

精炼后的数据进入**解耦自适应熵约束 RLVR 模块**。该模块以 GRPO 为基座 RL 算法，在策略损失中引入解耦熵惩罚项：

- 对于短推理轨迹（m_i = 1），使用固定熵系数 β_s，当实际熵 H_i 低于目标熵 H_s 时激活惩罚；
- 对于长推理轨迹（m_i = 0），使用自适应系数 β_l，当 H_i 低于 H_l 时激活惩罚；同时，β_l 本身通过一个自适应损失函数根据实际熵与目标熵的偏差进行动态更新。

策略损失的形式为：

$$
\mathcal{L}_{\mathfrak{p}} = \frac{1}{N} \sum_{i=1}^{N} \left[ - \min\left( \rho_i \hat{A}_i, \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon) \cdot \hat{A}_i \right) - \beta_i H_i \right]
$$

其中 β_i 由解耦系数公式决定：

$$
\beta_i = \beta_s \cdot m_i \cdot \mathbb{I}\{H_i \leq H_s\} + \beta_l \cdot (1 - m_i) \cdot \mathbb{I}\{H_i \leq H_l\}
$$

同时，**自动思维奖励模块**提供非对称答案奖励信号，与格式奖励共同构成 RL 训练的奖励函数：

$$
\mathcal{R}_{\mathrm{answer}}(o_i) = 
\begin{cases} 
+1.0, & \text{if } o_i = y^*, \text{no-think}, \\ 
+0.5, & \text{if } o_i = y^*, \text{think}, \\ 
-0.5, & \text{if } o_i \neq y^*, \text{think}, \\ 
-1.0, & \text{if } o_i \neq y^*, \text{no-think} 
\end{cases}
$$

该奖励设计鼓励正确时的短响应、惩罚错误时的短响应，并在错误时激励模型切换到 think 模式进行更深入的推理。

### 推理时的可控性

训练完成后，AutoTool 模型支持两种推理模式：**自动模式**（模型根据问题难度自主选择 think/no_think）和**可控模式**（通过在输入前缀中插入 [mode] 标签强制指定推理模式）。这一设计使得模型在部署时可以根据实际场景灵活切换：在需要极致效率的场景下强制 no_think，在需要高精度的场景下允许自动扩展推理。

### 管线设计的因果逻辑

整个管线的设计遵循一条清晰的因果链：推理坍塌的直接原因是策略熵的持续下降（Figure 2d 表明低熵与坍塌强正相关），而熵的下降源于 GRPO 优化过程中策略分布逐渐收窄。通过解耦短/长推理路径的熵约束，AutoTool 在保持简单问题高效求解的同时，为复杂问题保留了必要的探索空间；自适应系数机制则进一步避免了固定熵约束对系数的敏感性（Table 1 显示固定 β 对性能影响显著），使长推理路径的熵惩罚强度能够根据实际需要动态调整。数据精炼作为基础支撑，通过剔除噪声样本降低了训练波动，使准确率奖励提高约 15%（Figure 9）。



### 3.1 数据准备与暖启动SFT

AutoTool 的训练流程始于数据层面的精心设计。研究者构建了名为 **PubTool** 的混合数据集（统计信息见 Table 2），其核心目标是通过暖启动监督微调（Warm-up SFT）使模型初步感知样本难度，并学习自动区分需要思考（think）与无需思考（no_think）的场景。

数据准备包含两个关键步骤：
- **混合长/短推理数据**：将长推理轨迹与短推理轨迹混合用于 SFT 暖启动，使模型在训练初期即暴露于不同推理模式。
- **RL 数据精炼**：将原始 RL 数据集从 21k 样本下采样至 7k。具体操作包括剔除一半的过易样本和过难样本，并基于奖励方差优先保留与模型学习轨迹对齐的高质量样本。奖励方差定义为：

$$\operatorname{Var}(r) = \frac{1}{n-1} \sum_{i=1}^{n} (r_i - \mu_r)^2, \quad \mu_r = \frac{1}{n} \sum_{i=1}^{n} r_i$$

其中方差越低表示样本与模型当前学习轨迹越对齐。消融实验表明，移除数据精炼导致 BFCL 整体准确率下降 6.43%，多轮对话准确率下降 11.34%（Table 4），验证了高质量数据作为方法核心基础的地位。

### 3.2 解耦自适应熵约束 RLVR

AutoTool 的核心技术创新在于对 GRPO 算法引入**解耦自适应熵约束**，以对抗工具使用任务中直接 RL 训练导致的推理坍塌现象。

#### 3.2.1 熵约束的动机

初步分析揭示，策略模型的熵与推理坍塌呈现强正相关：随着训练步数增加，模型熵值急剧下降，响应长度同步萎缩（Figure 2(d)）。简单的长度惩罚无法缓解低熵问题（Figure 3(b)），而固定系数的熵约束虽能部分增加响应长度，但对系数高度敏感（Table 1），且无法区分不同推理模式的需求。

#### 3.2.2 解耦熵系数

为解决上述问题，AutoTool 将推理轨迹解耦为短推理（short）和长推理（long）两类，并对每类施加差异化的熵约束。对于第 $i$ 个样本，其熵惩罚系数 $\beta_i$ 计算如下：

$$\beta_i = \beta_s \cdot m_i \cdot \mathbb{I}\{H_i \leq H_s\} + \beta_l \cdot (1 - m_i) \cdot \mathbb{I}\{H_i \leq H_l\}$$

其中：
- $m_i \in \{0, 1\}$ 为轨迹类型指示器（$m_i=1$ 表示短轨迹，$m_i=0$ 表示长轨迹）；
- $H_i$ 为当前样本的策略熵；
- $H_s$ 和 $H_l$ 分别为短推理和长推理的目标熵阈值；
- $\beta_s$ 为短推理路径的固定熵惩罚系数；
- $\beta_l$ 为长推理路径的自适应熵惩罚系数；
- $\mathbb{I}\{\cdot\}$ 为指示函数，仅当当前熵低于目标阈值时激活惩罚。

该设计的核心思想是：对短推理路径施加固定约束以保持简洁性，对长推理路径则自适应调节约束强度以维持足够的探索能力。

#### 3.2.3 策略损失

带有解耦熵惩罚的样本级策略损失为：

$$\mathcal{L}_{\mathfrak{p}} = \frac{1}{N} \sum_{i=1}^{N} \left[ - \min\left( \rho_i \hat{A}_i, \mathrm{clip}(\rho_i, 1-\epsilon, 1+\epsilon) \cdot \hat{A}_i \right) - \beta_i H_i \right]$$

其中 $\rho_i$ 为重要性采样比率，$\hat{A}_i$ 为优势估计，$\epsilon$ 为裁剪范围。该损失在标准 GRPO 的裁剪替代目标基础上，减去了解耦的熵惩罚项 $\beta_i H_i$。

#### 3.2.4 自适应熵系数损失

为动态调整长推理路径的熵约束强度，引入自适应熵系数损失，仅在长轨迹上更新 $\beta_l$：

$$\mathcal{L}_{\beta}^{l} = \frac{1}{\sum_j (1-m_j)} \sum_{i=1}^{N} (1-m_i) \cdot \beta_l \cdot (H_i - H_l)$$

该损失根据实际熵 $H_i$ 与目标熵 $H_l$ 的偏差调整 $\beta_l$：当长轨迹的实际熵偏离目标水平时，$\beta_l$ 被相应修正，使模型在复杂问题上保持适当的探索-利用平衡。

消融实验证实了各组件的必要性：移除解耦（使用统一熵约束）导致整体准确率下降 5.89%，多轮对话下降 10.53%；移除自适应系数（使用固定熵系数）导致整体准确率下降 2.34%（Table 4）。超参数灵敏度分析表明，最优目标熵设置为 $H_s=0.1$、$H_l=0.2$（Table 6），最佳熵惩罚系数组合为 $\beta_s=0$、$\beta_l=1\times10^{-2}$（Table 7）。

### 3.3 自动思维奖励模块

为引导模型正确使用 think/no_think 模式并实现推理效率的自动扩展，AutoTool 设计了非对称答案奖励函数：

$$\mathcal{R}_{\mathrm{answer}}(o_i) = \begin{cases} +1.0, & \text{if } o_i = y^*, \text{no-think}, \\ +0.5, & \text{if } o_i = y^*, \text{think}, \\ -0.5, & \text{if } o_i \neq y^*, \text{think}, \\ -1.0, & \text{if } o_i \neq y^*, \text{no-think} \end{cases}$$

其中 $o_i$ 为模型输出，$y^*$ 为正确答案。该奖励函数的非对称设计体现了三个核心激励方向：
- **鼓励正确时的短响应**：正确答案且使用 no-think 模式获得最高奖励（+1.0），正确答案但使用 think 模式仅获 +0.5，促使模型在简单问题上避免冗余思考；
- **惩罚错误时的短响应**：错误答案且使用 no-think 模式获得最低惩罚（-1.0），错误答案但使用 think 模式仅获 -0.5，激励模型在不确定时进入思考模式；
- **错误时鼓励思考**：通过 -0.5 vs -1.0 的梯度差，引导模型在面临困难问题时自动切换到长推理模式。

此外，模型通过 `[mode]` 标签实现可控推理：推理时可通过在输入 token 前添加相应前缀来显式切换 think 或 no_think 模式（Figure 4），为部署场景提供了灵活的推理模式控制能力。

### 3.4 推理效率评估指标

为全面衡量模型在准确率与计算成本之间的权衡，AutoTool 引入了计算单元准确率指标：

$$\mathrm{ACU} = \frac{\mathrm{Accuracy}}{\#\mathrm{Params} \times \#\mathrm{Tokens}}$$

该指标同时考虑模型参数量和输出 token 数，提供了一个统一的推理效率度量。在 BFCL 基准上，AutoTool 以强制 no-think 推理模式取得最优 ACU 分数 0.97（Figure 6），相比蒸馏模型在准确率提升 9.8% 的同时将推理 token 成本削减约 81%（~183 tokens vs ~966 tokens）。



## 实验与关键发现

### 核心瓶颈与因果验证

AutoTool 的设计源于对工具使用任务中**推理坍塌（Reasoning Collapse）**现象的因果分析。在标准 GRPO 训练下，模型在工具使用任务中的响应长度随训练步数急剧下降（Figure 1b），这与数学推理任务中“长度随准确率提升而增长”的趋势截然相反。进一步分析表明，这一坍塌现象**独立于样本难度分布**——在 Easy、Medium、Hard 三个子集上均发生（Figure 2c），且与策略熵的下降呈强正相关（Figure 2d）。这一发现揭示了核心因果机制：**低熵直接导致推理坍塌**，而非数据分布不均。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_zFkopTvclB/figures/003_Figure_1.jpg]]
*Figure 1: The training paradigms for TTS in tool-use: (a) direct RL enables scaling up response length as accuracy improves in mathematical tasks; but (b) it fails to scale in tool-use tasks, where reasoning collapses into short trajectories; (c) scaled-up models (e.g., distillation models) incur significant token costs, as they require lengthy reasoning trajectories for all queries*

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_zFkopTvclB/figures/007_Figure_2.jpg]]
*Figure 2: Impact of difficulty distributions. Easy and Medium converged successfully, while Hard failed (a, b). However, collapse occurred across all three subsets (c), with the same trend observed in entropy (d). This indicates that data distribution has no correlation with collapse, whereas low entropy exhibits a strong positive correlation*

初步实验验证了熵约束的必要性：在 GRPO 中引入固定熵惩罚（Table 1）可部分缓解坍塌，但效果对系数 $\\beta$ 高度敏感（$\\beta=1e-1$ 时取得最大正向增益，其他系数效果有限）；而直接施加长度约束则完全无法缓解低熵问题，未能提升测试性能（Figure 3b）。这确立了**解耦自适应熵约束**作为核心调控变量的因果基础。

### 主实验结果

#### BFCL 基准测试

Table 3 展示了 AutoTool 在 BFCL 基准上的主结果。以 Qwen2.5-7B-Instruct 为基座，AutoTool 取得 **70.12% 的整体准确率**，相比 PubTool-SFT 提升 **+11.95 个百分点**，相比基座模型提升 **+16.43 个百分点**。在 Multi-Turn 子任务上，AutoTool 达到 38.18%，相比 PubTool-SFT 的 9.68% 提升 **+28.5 个百分点**，这一巨大增益验证了解耦熵约束对多轮交互稳定性的关键作用。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_zFkopTvclB/figures/015_Table_3.jpg]]
*Table 3: Comparison on the BFCL benchmark. Overall Acc denotes the average performance on three subsets. * indicates a single-turn tool use model; † denotes models trained on PubTool data with a specific method. The subscript denotes the thinking rate*

与蒸馏模型（PubTool-Distilled）相比，AutoTool 在准确率上领先 9.8 个百分点的同时，推理 token 成本从约 966 tokens 降至约 183 tokens，削减约 **81%**（Figure 6）。这表明 AutoTool 成功实现了“简单问题简洁回答、复杂问题深入推理”的自动扩展目标，避免了蒸馏模型在所有问题上均产生冗长推理的浪费。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_zFkopTvclB/figures/020_Figure_6.jpg]]
*Figure 6: Inference efficiency analysis results, including performance, token cost, ACU*

与前沿 API 模型对比，AutoTool（~7B）的整体准确率（70.12%）已接近 GPT-4o（69.71%）和 Gemini-2.5-Pro（69.35%），并在 Multi-Turn 场景（38.18%）上显著超越 o3-2025-04-16（22.75%）。

#### 跨基准泛化

在 ACEBench 上（Figure 5），AutoTool 取得 **83.2%** 的准确率，相比 GRPO（76.7%）提升 6.5 个百分点，相比蒸馏模型（77.6%）提升 5.6 个百分点，验证了方法在工具使用任务上的跨基准泛化能力。

#### 多尺寸泛化

Figure 11 展示了 AutoTool 在不同模型架构和参数规模上的泛化性能。在 LLaMA-3.1-8B、Qwen2.5-1.5B/3B/7B/32B 上，AutoTool 均取得一致的性能提升，其中 Qwen2.5-32B 提升幅度最大（+15.1 个百分点），表明解耦自适应熵约束策略具有良好的可扩展性。

### 消融实验

Table 4 系统消融了 AutoTool 的三个核心组件：

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_zFkopTvclB/figures/021_Table_4.jpg]]
*Table 4: The strategy ablation performance (↑ = increase, ↓ = decrease, values are relative percentage changes from the Our (w/. all) model)*

1. **移除数据精炼**：导致整体准确率下降 **6.43%**，Multi-Turn 下降 **11.34%**，是所有消融中影响最大的操作。这验证了基于奖励方差筛选高对齐样本的数据精炼是方法的核心基础。Figure 9 进一步显示，数据精炼使训练过程中的准确率奖励提高约 15%，并显著减小训练波动。

2. **移解除耦（使用统一熵约束）**：导致整体准确率下降 **5.89%**，Multi-Turn 下降 **10.53%**。这证明对长/短推理路径施加差异化熵约束是必要的，统一约束无法有效平衡两种推理模式的需求。

3. **移除自适应系数（使用固定熵系数）**：导致整体准确率下降 **2.34%**。虽然影响相对较小，但自适应调节对于稳定多轮交互和避免目标干扰仍然重要。

### 超参数灵敏度分析

Table 6 展示了目标熵的灵敏度分析。在短推理目标熵 $H_s$ 和长推理目标熵 $H_l$ 的 3×3 组合中，最优设置为 $H_s=0.1, H_l=0.2$，取得整体准确率 70.1%。过高的目标熵（如 $H_s=0.5$）会导致性能下降，表明过强的熵约束会干扰策略优化。

Table 7 展示了熵惩罚系数的灵敏度分析。较低的短路径系数 $\\beta_s$ 通常表现更好，最佳组合 $\\beta_s=0, \\beta_l=1e-2$ 取得整体准确率 71.4%。这表明对短推理路径施加熵惩罚可能不必要，而对长路径施加适度惩罚（$1e-2$）最为有效。

### 推理效率分析

AutoTool 引入的计算单元准确率（ACU）指标综合衡量准确率、模型参数量和输出 token 数。Figure 6 显示，AutoTool 在强制 no-think 推理模式下取得最优 ACU 分数（0.97），远超蒸馏模型（~0.1）和 GRPO（~0.75）。这进一步验证了 AutoTool 在推理效率上的显著优势——通过自动选择推理模式，在保持高准确率的同时大幅压缩 token 开销。

### 失败模式与局限

尽管 AutoTool 在工具使用任务上取得了显著进展，仍存在以下局限：

1. **规模验证不足**：主要实验在 ~7B 参数规模上进行，虽然在 1.5B~32B 上展示了泛化趋势（Figure 11），但未在更大规模（如 70B+）上验证可扩展性。
2. **任务通用性未验证**：方法仅在工具使用任务上验证，未在数学推理、代码生成等其他复杂推理任务上测试。工具使用中推理坍塌的深层机制是否与其他领域共享，仍是开放问题。
3. **RL 算法依赖性**：当前方法基于 GRPO 算法实现，与 PPO、DAPO 等 RL 算法的兼容性尚未验证。
4. **推理坍塌的根本原因**：尽管建立了低熵与坍塌的因果关系，但为何工具使用任务中 RL 训练导致熵快速下降而数学任务中不会，其深层机制仍不清楚。



## 定位与知识库关联

### 工具使用LLM的训练范式演进

当前训练工具使用大语言模型主要遵循三条技术路线：

**监督微调（SFT）** 通过模仿高质量标注示例中的推理模式来训练模型，代表性工作包括 **Hammer2.1-7b**（Lin et al., 2024）、**ToolACE-8B**（Liu et al., 2024）和 **xLAM-7b-r**（Zhang et al., 2024a）。这类方法的瓶颈在于：模型仅能复现训练数据中的推理模式，难以在测试时根据问题难度自适应扩展推理规模。

**基于直接偏好优化的强化学习** 通过构造偏好对来对齐模型的工具使用行为，但该方法依赖高质量偏好数据，且无法直接利用可验证的二元奖励信号。

**基于可验证奖励的强化学习（RLVR）** 是近年来最具扩展性的范式。以 **DeepSeek-R1-0528**（DeepSeek-AI, 2025a）为代表的工作利用GRPO算法在数学推理中解锁了模型的测试时推理能力，实现了推理长度随准确率同步增长。在工具使用领域，**Tool-N1-7B**（Zhang et al., 2025b）和 **ToolRL-7B**（Qian et al., 2025）尝试将RLVR引入单轮工具使用场景，但AutoTool的初步研究揭示了一个关键瓶颈：直接RL训练在工具使用任务中会导致**推理坍塌**——响应长度随训练步数急剧下降，与数学任务中长度随准确率提升的趋势截然相反（Figure 1(b)）。

### 自适应推理的跨领域脉络

自适应推理策略的核心思想是让模型根据问题难度自动选择合适的推理模式，避免“一刀切”的推理开销。在数学推理领域，**Thinkless**（Fang et al., 2025）和 **Adactrl**（Huang et al., 2025）已探索了类似思路，但这些方法尚未在工具使用场景中得到验证。AutoTool首次将自适应推理引入工具使用RLVR训练，其关键创新在于：通过解耦短推理与长推理的熵约束，并引入自适应熵系数调节机制，使模型能够在RL训练过程中自主学习难度感知的推理模式切换。

### 方法适用边界

AutoTool的适用边界由以下因素界定：

1. **任务类型边界**：当前验证集中在工具使用任务（BFCL、API-Bank、ACEBench），尚未在数学推理、代码生成等复杂推理任务上进行验证。工具使用任务中推理坍塌的深层机制与数学推理存在本质差异，该方法在其他领域的可迁移性需要进一步实验确认。

2. **模型规模边界**：主要实验在~7B参数规模（Qwen2.5-7B-Instruct）上完成。虽然Figure 11展示了在1.5B至32B多个规模上的泛化趋势，但更大规模模型（如70B+）上的表现尚未验证。

3. **RL算法兼容性边界**：目前仅与GRPO算法结合验证，尚未测试与PPO、DAPO等其他RL算法的兼容性。不同算法的优势估计和策略更新机制可能影响解耦熵约束的有效性。

4. **数据依赖边界**：方法依赖暖启动SFT阶段构建的混合长/短推理数据，以及RL阶段的数据精炼策略。数据质量和分布直接影响模型的难度感知能力和训练稳定性。

### 局限与开放问题

**已验证的局限性：**

- 仅在~7B参数规模上完成系统验证，不同模型架构（如LLaMA系列、DeepSeek系列）的可扩展性证据不足。
- 方法的通用性未在工具使用以外的复杂推理任务上得到验证。
- 目前依赖GRPO算法，与其他RL算法的兼容性未知。

**开放问题：**

1. **推理坍塌的深层机制**：工具使用任务中为何出现推理坍塌，而数学推理中未出现？低熵与坍塌之间的因果关系方向是什么？熵约束能否完全防止坍塌并保持测试时扩展性？

2. **跨任务泛化能力**：解耦自适应熵约束策略能否推广到数学推理、代码生成等任务？这些任务中是否也存在类似的“简单问题过度思考”问题？

3. **规模扩展性**：该方法在不同模型架构和参数规模（特别是70B+级别）上能否取得一致的增益？是否存在规模相关的相变点？

4. **算法兼容性**：与PPO、DAPO等RL算法结合是否依旧有效？不同算法的优势估计偏差是否会影响熵约束的调节效果？

5. **推理模式切换的粒度**：当前方法通过[mode]标签实现粗粒度的think/no_think切换，是否可能存在更细粒度的推理深度控制（如部分思考、多步推理的中间退出）？

**需要人工验证的点：** 论文中关于“推理坍塌独立于样本难度分布”的结论（Figure 2）基于特定数据集划分，该现象的普遍性需要在更多工具使用基准上进行交叉验证。



## 原文 PDF

![[paperPDFs/ICLR_2026/AutoTool_Automatic_Scaling_of_Tool_Use_Capabilities_in_RL_via_Decoupled_Entropy_Constraints.pdf]]
