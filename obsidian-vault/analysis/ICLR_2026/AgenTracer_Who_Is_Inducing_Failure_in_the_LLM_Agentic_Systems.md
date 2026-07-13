---
title: "AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems?"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AgenTracer_Who_Is_Inducing_Failure_in_the_LLM_Agentic_Systems.pdf
project_link: null
code_link: https://github.com/bingreeky/AgenTracer
openreview_forum_id: l05DseqvuD
aliases:
- AgenTracer
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过反事实重放（Counterfactual Replay）系统性地替换错误动作为理想动作，定位最早的可修正错误步骤；同时利用程序化故障注入（Programmatic Fault Injection）在成功轨迹上合成故障，自动构建大规模标注数据集；再用多粒度强化学习（step-level + agent-level奖励）训练轻量级归因模型。"
primary_logic: "多智能体系统的失败可归因于最早的可修正错误步骤，而使用反事实干预和故障注入可以自动化地标注这些步骤；多粒度奖励（步骤级高斯奖励和智能体级二元奖励）引导的强化学习能够让轻量级模型（8B）超越巨型模型（如Gemini-2.5-Pro、Claude-4-Sonnet），实现精准且可操作的故障定位。"
claims:
- "在Who&When基准上，AgenTracer-8B以高达~18.18%的优势超越Gemini-2.5-Pro等巨型LLM，且以~12.21%超越DeepSeek-R1。"
- "在TracerTraj各子集（Code, MATH, Agentic）上，AgenTracer-8B在agent-level和step-level准确率方面均大幅领先所有基线，例如Code agent-level (w/o G) 72.21% vs. Gemini-2.5-Pro 66.92%。"
- "AgenTracer-8B能够为现有多智能体系统（MetaGPT、MaAS等）提供可操作的反馈，带来4.8%~14.2%的系统性能提升。"
- "消融实验证实step-level奖励对精确步骤定位至关重要（移除后Code step-level从18%降至12%），而agent-level奖励亦有正面贡献。"
---

# AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems?

> [!tip] 核心洞察
> 多智能体系统的失败可归因于最早的可修正错误步骤，而使用反事实干预和故障注入可以自动化地标注这些步骤；多粒度奖励（步骤级高斯奖励和智能体级二元奖励）引导的强化学习能够让轻量级模型（8B）超越巨型模型（如Gemini-2.5-Pro、Claude-4-Sonnet），实现精准且可操作的故障定位。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AgentTracer：谁在诱导大语言模型智能体系统的失败？ |
| 英文题名 | AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems? |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=l05DseqvuD) · [GitHub](https://github.com/bingreeky/AgenTracer) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | AgenTracer |
| Dataset | Who&When (handcraft), Who&When (automated), TracerTraj-code, TracerTraj-MATH |

> [!tip] 效果简介
> - Who&When (handcraft) 上，Agent-level accuracy (w/o G) 为 63.82，对比 53.44 (DeepSeek-R1)，变化 +10.38。
> - Who&When (automated) 上，Step-level accuracy (w/ G) 为 42.86，对比 40.65 (Claude-4-Sonnet)，变化 +2.21。
> - TracerTraj-code 上，Agent-level accuracy (w/o G) 为 72.21，对比 66.92 (Gemini-2.5-Pro)，变化 +5.29。

## 概要

### 问题与瓶颈

大语言模型驱动的多智能体系统在实际部署中故障频发——失败率可高达86.7%——但现有的自动故障归因方法准确率极低（通常不足10%）。根本瓶颈在于两个方面：其一，缺乏大规模、高精度标注的故障轨迹数据，人工标注冗长的多智能体交互序列成本极高且难以规模化；其二，通用大语言模型难以从包含数十甚至上百步的交互序列中精准定位那个决定性的错误步骤，往往在噪声中迷失关键信号。

### 核心方法定位

**AgenTracer** 针对上述瓶颈提出了一个从数据构建到模型训练的全自动归因框架。其核心思路在于：多智能体系统的失败通常可归因于**最早的可修正错误步骤**——即如果将该步骤的动作替换为理想动作，系统就能从失败转为成功的最早时间点。围绕这一洞察，方法在两个层面展开：

- **数据层面**：通过**反事实重放**（Counterfactual Replay）系统性地替换失败轨迹中的错误动作为理想动作，定位最早的决定性错误步骤；同时利用**程序化故障注入**（Programmatic Fault Injection）在成功轨迹上合成故障，自动构建包含超过2000条高置信度标注的 **TracerTraj-2.5K** 数据集。
- **训练层面**：以轻量级开源模型 **QWEN3-8B** 为基础，采用基于GRPO的在线强化学习，设计**多粒度奖励**——步骤级高斯核奖励（预测步骤越接近真实决定性步骤奖励越高）与智能体级二元奖励（是否正确识别故障智能体）的加权组合——训练得到专用故障追踪器 **AgenTracer-8B**。

这一设计使得仅8B参数的轻量模型能够在故障归因任务上超越Gemini-2.5-Pro、Claude-4-Sonnet等巨型商业模型，同时保持极低的推理成本。

### 主要结果概览

在人工构建的 **Who&When** 基准上，AgenTracer-8B在智能体级准确率上以约18.18%的优势超越Gemini-2.5-Pro，以约12.21%超越DeepSeek-R1。在覆盖代码、数学和通用智能体任务的 **TracerTraj** 各子集上，AgenTracer-8B在多数设定下均取得最优或次优结果——例如在Code子集智能体级准确率达72.21%（w/o G设定），领先Gemini-2.5-Pro约5.3个百分点；在MATH子集步骤级准确率达57.63%，领先Claude-4-Sonnet约11.6个百分点。

更重要的是，AgenTracer-8B能够为现有的多智能体系统提供可操作的故障反馈。在MaAS和OWL等系统上，通过多轮自我演化，系统性能分别提升了14.2%和4.8%，显著优于Self-Refine、CRITIC等经典反射基线。

消融实验揭示了方法的关键设计因素：步骤级奖励对精确定位至关重要（移除后Code步骤级准确率从18%降至12%），而反事实修正数据比纯故障注入数据具有更高的内在训练价值，两者联合使用可实现互补增益。

### 多智能体系统的脆弱性

基于大语言模型（LLM）的多智能体系统正被广泛应用于代码生成、数学推理和复杂任务规划等场景。然而，这些系统在实际运行中表现出显著的脆弱性——失败率可高达86.7%。当多个智能体通过消息传递、工具调用和环境交互协同工作时，单个步骤的微小偏差便可能通过链条传播，最终导致整个系统崩溃。这类故障的隐蔽性和级联特性使得人工排查极为耗时，而随着系统规模和交互复杂度的增长，自动化故障定位的需求变得愈发迫切。

### 现有归因方法的根本瓶颈

当前，自动故障归因主要依赖两种范式：一是直接提示巨型LLM（如**GPT-4.1**、**Gemini-2.5-Pro**、**Claude-4-Sonnet**）对完整轨迹进行零样本推理；二是基于少量人工标注数据微调中小规模模型。然而，这两种路径均面临严重局限。

**零样本归因的准确率极低。** 在Who&When基准测试中，即便是最先进的商业模型，其agent-level归因准确率也普遍低于10%。根本原因在于，多智能体系统的交互轨迹通常包含数十甚至上百个步骤，涉及异构智能体之间的复杂信息流，通用LLM难以从冗长序列中精准定位那个决定性的错误步骤。模型往往倾向于将失败归咎于最后一个执行动作的智能体，或产生与真实因果链无关的猜测性解释。

**高质量标注数据的稀缺构成了更底层的瓶颈。** 故障归因的监督信号要求标注者不仅判断系统是否失败，还需精确标识哪个智能体在哪个步骤做出了导致失败的决定性错误动作。这类细粒度标注需要标注者深入理解任务语义、智能体角色分工和系统执行逻辑，人工成本极高。现有的少量标注数据远不足以支撑可靠模型的训练，而依赖巨型LLM进行推理又带来了高昂的计算开销和延迟。

### 核心动机与研究问题

上述困境揭示了一个根本性的方法论缺口：**如何在缺乏大规模人工标注的条件下，系统性地构建高保真度的故障归因训练数据，并训练出兼具精度与效率的轻量级归因模型？**

本文的工作围绕三个紧密关联的子问题展开：

1. **标注自动化**：能否利用LLM自身的分析能力，通过反事实干预和程序化故障注入，自动为成功和失败轨迹生成可靠的错误步骤标注？
2. **训练精细化**：如何设计奖励信号，使模型不仅能识别失败负责的智能体，还能精确锁定轨迹中的决定性错误步骤？
3. **效率与精度的平衡**：能否训练一个轻量级专用模型（如8B参数规模），使其在归因精度上超越巨型通用LLM，同时保持低推理成本？

解决这些问题，意味着多智能体系统将首次获得可操作的故障诊断能力——不仅知道“系统失败了”，还能明确“哪个智能体在何时做错了什么”，从而为自动修复、系统迭代和智能体行为的持续改进奠定基础。

## 核心方法与创新机理

AgenTracer 的核心创新并非提出全新的模型架构，而是通过**数据构造范式**与**训练奖励机制**的双重变革，将故障归因这一任务从巨型LLM的零样本推理，迁移至轻量级模型的精准专用化。其关键创新点可归结为以下三个“changed slots”：

### 1. 训练数据：从稀缺人工标注到大规模自动合成（TracerTraj-2.5K）

现有方法的根本瓶颈在于缺乏大规模、高精度的故障轨迹标注数据，导致通用LLM直接进行归因时准确率极低（不足10%）。AgenTracer 构建了一套完全自动化的数据标注流水线，通过两种互补机制系统性地生成训练信号（见 Algorithm 1）：

- **反事实重放（Counterfactual Replay）**：针对失败轨迹，利用分析器智能体 $\pi_{\mathrm{analyzer}}$ 对每一步动作提议“最小侵入式”的修正动作 $a_t'$，并重放后续轨迹。若系统由失败转为成功，则该步即被标记为**决定性错误步骤** $(i^*, t^*)$。通过搜索最早满足此条件的步骤，定位故障根因（公式 (4)、(5)）。由此构建的负样本集记为 $\mathcal{D}^-$。

- **程序化故障注入（Programmatic Fault Injection）**：针对成功轨迹，通过扰动算子 $\Pi$ 在选定步骤 $t$ 注入故障变体，若重放后系统失败，则 $(t, \mu(t))$ 自动成为已知的决定性错误对。由此构建的正样本集记为 $\mathcal{D}^+$。

合并 $\mathcal{D}^-$ 与 $\mathcal{D}^+$ 得到 **TracerTraj-2.5K** 数据集，包含超过 2000 条高置信度的轨迹-错误标注对，覆盖代码、数学与通用智能体三大领域（Table 3）。这一数据构造范式将故障归因从依赖昂贵人工标注的瓶颈中解放出来，是该工作的基石性创新。

### 2. 训练范式与奖励设计：多粒度强化学习

传统的提示方法或监督微调仅提供粗粒度的监督信号，难以引导模型在冗长的多智能体交互序列中精确定位故障步骤。AgenTracer 采用基于 GRPO 的在线强化学习，并设计了**多粒度奖励函数**，同时监督两个层级的归因准确性：

- **格式合规性门控** $\mathbb{I}_{\mathrm{format}}$：确保模型输出符合预期的结构化格式，不合规的预测直接置零奖励。
- **智能体级二元奖励** $r_{\mathrm{agent}}(\hat{i}_k)$：预测的负责智能体 $\hat{i}_k$ 与真实标签 $i^*$ 一致时给予正向信号。
- **步骤级高斯核奖励** $r_{\mathrm{step}}(\hat{t}_k) = \exp\left(-\frac{(\hat{t}_k - t^*)^2}{2\sigma^2}\right)$：预测步骤 $\hat{t}_k$ 与真实决定性步骤 $t^*$ 的偏差越大，奖励衰减越剧烈，以此施加细粒度的时序邻近性约束。

总奖励为 $R(\hat{p}_k) = \mathbb{I}_{\mathrm{format}} \cdot (\lambda \cdot r_{\mathrm{step}} + (1-\lambda) \cdot r_{\mathrm{agent}})$，并通过动态裁剪参数 $B_s$ 平衡探索与利用（公式 (10)-(12)）。消融实验（Figure 5、Figure 6）证实：**移除步骤级奖励会导致步骤准确率断崖式下降**（Code step-level 从 18% 降至 12%），而移除智能体级奖励仅造成中等性能损失，表明细粒度的步骤监督是模型精准定位的决定性因素。

### 3. 模型规模与效率：轻量级专用化

基线方法普遍依赖巨型LLM（如 **Gemini-2.5-Pro**、**Claude-4-Sonnet**、**DeepSeek-R1**）进行归因，推理成本高昂且延迟显著。AgenTracer 以 **QWEN3-8B**（Yang et al., 2025）为基座，通过上述自动化数据与多粒度RL训练，得到仅 **8B 参数**的专用故障追踪器 **AgenTracer-8B**。结果表明，该轻量级模型在 Who&When 基准上以高达 **~18.18%** 的优势超越 Gemini-2.5-Pro，以 **~12.21%** 超越 DeepSeek-R1（Table 1），在 TracerTraj 各子集上也全面领先（Table 2），实现了“小模型超越大模型”的专用化突破。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_l05DseqvuD/figures/005_Figure_2.jpg]]
*Figure 2: The overview of our proposed AgenTracer*

AgenTracer 的整体设计围绕一个核心命题展开：**多智能体系统的失败可以归因于最早的可修正错误步骤，而这一步骤可以通过反事实干预自动发现**。基于此，系统被组织为一条从数据构造到模型训练再到推理部署的完整流水线，其概览如 Figure 2 所示。

### 流水线总览

AgenTracer 包含五个主要模块，按执行顺序依次为：

1. **轨迹收集（Collection）**：在 6 个多智能体系统上执行 7 个基准任务，收集原始的成功轨迹与失败轨迹，构成原始数据池。
2. **反事实修正（Counterfactual Correction）**：对失败轨迹，利用分析器智能体 $\pi_{\mathrm{analyzer}}$ 为每一步提议局部修正动作，通过反事实重放系统性地定位最早的决定性错误步骤 $(i^*, t^*)$。
3. **程序化故障注入（Programmatic Fault Injection）**：对成功轨迹，在特定步骤施加扰动算子 $\Pi$ 生成故障变体；若导致系统失败，则该步骤即为已知的决定性错误，形成正向标注样本。
4. **数据集构建（TracerTraj-2.5K）**：合并反事实修正得到的负样本 $\mathcal{D}^-$ 与故障注入得到的正样本 $\mathcal{D}^+$，形成超过 2000 个高置信度的轨迹-错误对。
5. **多粒度强化学习训练（Multi-granular RL Training）**：以 QWEN3-8B 为基础模型，在 TracerTraj-2.5K 上采用 GRPO 进行在线强化学习，使用格式合规性、agent 级二元奖励和 step 级高斯核奖励联合优化，训练得到轻量级故障追踪器 **AgenTracer-8B**。

### 输入输出流

在推理阶段，AgenTracer-8B 接收完整的执行轨迹与环境反馈作为输入，输出三个关键信息：

- **失败负责的智能体 ID**（agent-level attribution）
- **决定性错误步骤编号**（step-level attribution）
- **归因解释**（natural language explanation）

这一输出格式使得 AgenTracer 能够直接为现有多智能体系统（如 MetaGPT、MaAS、OWL 等）提供可操作的故障反馈，支撑系统的自我改进。

### 设计决策与权衡

流水线的两个数据构造路径——反事实修正与故障注入——在本质上形成互补。反事实修正（$\mathcal{D}^-$）从真实失败中提取因果信号，其标注质量取决于分析器智能体的修正能力；故障注入（$\mathcal{D}^+$）则从成功轨迹中合成故障，扩展数据规模与多样性，但其有效性受限于攻击者 LLM 的扰动质量。消融实验表明，反事实修正数据比纯故障注入数据更具内在价值，但二者联合使用可实现最佳性能（详见附录 D.2）。

在训练环节，多粒度奖励设计是平衡归因精度与模型轻量化的关键。step 级高斯奖励 $r_{\mathrm{step}}(\hat{t}_k) = \exp\left(-\frac{(\hat{t}_k - t^*)^2}{2\sigma^2}\right)$ 提供了细粒度的时序监督信号，而 agent 级二元奖励则确保智能体识别的准确性。消融实验证实，移除 step 级奖励会导致步骤准确率显著下降（Code 子集从 18% 降至 12%），而 agent 级奖励的移除仅造成中等性能损失，表明细粒度步骤监督是归因性能的主导因素。

### 问题形式化

AgenTracer 将多智能体系统建模为元组：

$$\mathcal{M} = \langle \mathcal{T}, \mathcal{S}, \mathcal{A}, \Psi, \mu \rangle$$

其中 $\mathcal{T}$ 为智能体索引集，$\mathcal{S}$ 为共享状态空间，$\mathcal{A}$ 为联合动作空间，$\Psi$ 为状态转移函数，$\mu(t)$ 为第 $t$ 步调度的活跃智能体。每一步的动作选择为：

$$a_t = \pi_{\mu(t)}(s_t, \mathcal{H}_t, \mathcal{Q})$$

即活跃智能体基于当前状态 $s_t$、历史 $\mathcal{H}_t$ 和用户查询 $\mathcal{Q}$ 选择动作 $a_t$。完整轨迹记为 $\tau = (s_0, a_0, s_1, a_1, ..., s_T)$，系统成功与否由评估函数 $\Omega(\tau) \in \{0, 1\}$ 判定。

### 决定性错误步骤的定位原理

核心洞见在于：多智能体系统的失败可归因于**最早的可修正错误步骤**。形式化定义为，对于失败轨迹 $\tau$（$\Omega(\tau)=0$），若在步骤 $t$ 将原始动作 $a_t$ 替换为理想动作 $a_t'$ 后系统转为成功（$\Omega(\mathcal{R}(\tau, t, a_t')) = 1$），则 $(i=\mu(t), t)$ 构成一个决定性错误对。所有此类候选对的集合为 $\mathcal{C}(\tau)$，根因定位为选取最早步序：

$$(i^*, t^*) = \arg \min_{(i,t) \in \mathcal{C}(\tau)} t$$

### 轨迹收集模块

给定 $M$ 个多智能体系统，每个系统 $m$ 在对应基准上执行任务并收集原始轨迹。按评估结果划分为成功轨迹集 $\mathcal{T}_{\text{succ}}^{(m)}$ 和失败轨迹集 $\mathcal{T}_{\text{fail}}^{(m)}$：

$$\mathcal{T}_{\text{succ}}^{(m)} = \{ \tau_j^{(m)} \mid \Omega(\tau_j^{(m)}) = 1 \}, \quad \mathcal{T}_{\text{fail}}^{(m)} = \{ \tau_j^{(m)} \mid \Omega(\tau_j^{(m)}) = 0 \}$$

### 反事实修正模块（处理失败轨迹）

对于每条失败轨迹 $\tau$，引入**分析器智能体** $\pi_{\text{analyzer}}$，为每一步 $t$ 提议局部修正动作：

$$a_t' \gets \pi_{\text{analyzer}}(s_t, a_t, \mathcal{H}_t, \mathcal{F}, \mathcal{G})$$

其中 $\mathcal{F}$ 为环境反馈（如编译器报错、工具调用异常），$\mathcal{G}$ 为真实答案。分析器的设计原则是仅修正局部错误而不泄露完整解，从而保证反事实干预的保真度。随后沿轨迹从前向后进行反事实重放：将每一步的原始动作替换为 $a_t'$ 并继续执行，首个满足 $\Omega=1$ 的步骤即为决定性错误步骤 $(i^*, t^*)$。由此得到的负样本数据集记为 $\mathcal{D}^-$。

### 程序化故障注入模块（处理成功轨迹）

对于成功轨迹 $\tau$，选取步骤 $t$ 并通过**扰动算子** $\Pi$ 对动作 $a_t$ 进行定向破坏（如篡改参数、替换工具调用、注入逻辑错误等），生成故障变体动作 $\tilde{a}_t = \Pi(a_t)$。若扰动后轨迹 $\mathcal{R}(\tau, t, \tilde{a}_t)$ 失败（$\Omega=0$），则 $(t, \mu(t))$ 即为已知的决定性错误对。由此得到的正样本数据集记为 $\mathcal{D}^+$。

最终数据集 $\mathcal{D}_{\text{tracer}} = \mathcal{D}^+ \cup \mathcal{D}^-$ 包含超 2000 条高置信度轨迹-错误对标注，覆盖代码、数学和通用智能体三大领域。

### 多粒度强化学习训练模块

以 **QWEN3-8B**（Yang et al., 2025）为基础模型，采用 **GRPO**（Group Relative Policy Optimization, Guo et al., 2025）在线强化学习训练 AgenTracer-8B。核心损失函数为：

$$\mathcal{L}_{\text{RL}} = - \mathbb{E}_{\tau, \{\hat{p}_k\}_{k=1}^{G}} \left[ \frac{1}{G} \sum_{k=1}^{G} \min(\rho_k A_k, \text{clip}(\rho_k, 1-B_s, 1+B_s) A_k) \right]$$

其中 $G$ 为每组采样数，$\rho_k$ 为重要性采样比，$A_k$ 为优势函数，$B_s$ 为动态裁剪参数，随训练步数 $s$ 从 $B_{\text{max}}$ 线性衰减至 $B_{\text{min}}$，平衡探索与利用。

**多粒度奖励设计**是训练的核心创新，总奖励由格式合规性门控：

$$R(\hat{p}_k) = \mathbb{I}_{\text{format}} \cdot \Big( \lambda \cdot r_{\text{step}}(\hat{t}_k) + (1-\lambda) \cdot r_{\text{agent}}(\hat{i}_k) \Big)$$

其中 $\mathbb{I}_{\text{format}}$ 为格式合规性的二值指示函数（输出必须包含指定 XML 标签），$\lambda$ 为步骤级与智能体级奖励的加权系数。

**智能体级奖励** $r_{\text{agent}}$ 为二值奖励：预测的负责智能体 $\hat{i}_k$ 与真实 $i^*$ 一致时为 1，否则为 0。

**步骤级奖励**采用高斯核函数，对预测步骤 $\hat{t}_k$ 与真实决定性步骤 $t^*$ 的偏差进行连续惩罚：

$$r_{\text{step}}(\hat{t}_k) = \exp\left( - \frac{(\hat{t}_k - t^*)^2}{2\sigma^2} \right)$$

$\sigma$ 控制惩罚的锐度：$\sigma$ 越小，远离真实步骤的预测受到的惩罚越重，迫使模型精确定位。消融实验证实，移除步骤级奖励后，步骤级准确率从 18% 骤降至 12%（Code 子集），而移除智能体级奖励仅造成中等下降（72.2% → 68.9%），表明细粒度步骤监督是归因精度的关键驱动因素。

### 推理归因模块

训练完成后，AgenTracer-8B 接收完整轨迹 $\tau$ 及环境反馈，在单次前向传播中输出负责智能体 ID $\hat{i}$、决定性错误步骤编号 $\hat{t}$ 及自然语言解释，无需访问真实解 $\mathcal{G}$（w/o G 设定）。

## 实验与关键发现

### 核心实验设置

实验在两个基准上评估故障归因性能：**Who&When**（手工构建的精确标注集）和 **TracerTraj**（大规模自动标注数据集，覆盖代码、数学、通用智能体三个领域）。评估采用“all-at-once”设定，即将完整轨迹一次性输入模型进行归因。每个单元格报告两个值：左侧为 **w/ G**（归因模型可访问真实成功轨迹作为参考），右侧为 **w/o G**（仅基于失败轨迹本身进行归因），分别衡量有/无理想对照时的归因上限与实际部署能力。指标分为 **agent-level accuracy**（是否正确识别故障负责智能体）和 **step-level accuracy**（是否精确定位决定性错误步骤）。

### 主结果：AgenTracer-8B 全面超越巨型模型

**Who&When 基准**（Table 1）：AgenTracer-8B 在 agent-level 准确率上显著领先所有基线。在 handcraft 子集 w/o G 设定下，AgenTracer-8B 达到 **63.82%**，超越 **DeepSeek-R1**（53.44%，+10.38%）和 **Gemini-2.5-Pro**（45.64%，+18.18%），以 8B 参数规模击败了参数量大数十倍的闭源模型。在 automated 子集 w/o G 设定下，AgenTracer-8B 的 agent-level 准确率为 **63.73%**，同样领先于 **Claude-4-Sonnet**（60.31%，+3.42%）和 **Gemini-2.5-Pro**（55.55%，+8.18%）。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_l05DseqvuD/figures/006_Table_1.jpg]]
*Table 1: Performance comparison on the Who&When benchmark. For each subset, evaluation is conducted at both the agent and step levels. Each cell reports two values: the left corresponds to the setting w/ G (the failure tracer has access to ground truth trajectory), and the right corresponds to w/o G. The best and second-best results are bolded and underlined, respectively*

step-level 准确率方面，Who&When 手工子集本身难度极高（轨迹短、错误步骤少），所有模型的 step-level 准确率均较低（AgenTracer-8B 约 20.68%），但 automated 子集上 AgenTracer-8B 以 **37.30%**（w/o G）领先于 **Claude-4-Sonnet**（38.83%，-1.53%，此处略逊）和 **Gemini-2.5-Pro**（31.74%，+5.56%）。**关键发现**：当提供真实成功轨迹作为对照（w/ G）时，所有模型性能提升有限，说明当前方法的核心瓶颈并非缺乏理想参考，而是从冗长交互序列中精准定位错误步骤的固有难度。

**TracerTraj 子集**（Table 2）：在代码、数学、通用智能体三个领域，AgenTracer-8B 在 agent-level 上全面领先。Code 子集 w/o G 下 agent-level 准确率达 **72.21%**，超越 **Gemini-2.5-Pro**（66.92%，+5.29%）；MATH 子集 w/o G 下 agent-level 准确率 **66.11%**，超越 **Claude-4-Sonnet**（60.98%，+5.13%）；Agentic 子集 w/o G 下 agent-level 准确率 **50.58%**，超越 **DeepSeek-R1**（48.47%，+2.11%）。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_l05DseqvuD/figures/007_Table_2.jpg]]
*Table 2: Performance comparison on different subsets of TracerTraj. For each subset, accuracy is reported at the agent/step levels. Each cell reports two values: the left corresponds to the setting w/ G, and the right w/o G. The best and second-best results are bolded and underlined, respectively*

step-level 准确率上，AgenTracer-8B 的优势更为突出：MATH 子集 w/o G 下达到 **57.63%**，大幅超越 **Claude-4-Sonnet**（46.03%，+11.60%）和 **Gemini-2.5-Pro**（27.40%，+30.23%）；Code 子集 w/o G 下为 **18.23%**，Agentic 子集 w/o G 下为 **34.77%**。**注意**：在 Agentic 子集 w/ G 设定下，AgenTracer-8B 的 agent-level 准确率（53.28%）略低于 **Claude-4-Sonnet**（55.20%，-1.92%），表明在特定领域和设定下巨型模型仍具竞争力。

与基础模型 **QWEN3-8B** 相比，AgenTracer-8B 在 TracerTraj-agentic 的 step-level 准确率上提升了 **22.68%**，充分验证了多粒度强化学习训练的有效性。

### 自我演化实验：赋能现有多智能体系统

Figure 3 展示了 AgenTracer-8B 作为故障诊断器对现有多智能体系统的性能提升效果。在 **MaAS + MATH-500** 上，经过 4 轮自我改进后，AgenTracer-8B 将系统准确率从初始的约 53% 提升至约 **67%**（+14.21%）；在 **OWL + GAIA** 上，准确率提升约 **4.8%**。相比之下，传统的反思基线方法效果有限甚至有害：**Self-Refine** 在 MaAS + MATH-500 上仅带来约 2% 的提升，而 **CRITIC** 在 OWL + GAIA 上甚至导致性能下降（第 2 轮 -4.9%，第 3 轮 -5.5%）。这证明精准的故障步骤定位（而非笼统的自我反思）是系统自我改进的关键。

### 消融实验：多粒度奖励的必要性

**训练数据消融**（Table 6）：仅使用反事实修正数据 **D-** 训练的模型在 automated agent-level 上达到 60.31%，优于仅使用故障注入数据 **D+** 的 55.55%，表明从真实失败轨迹中学习到的错误模式更具内在价值。但两者联合使用达到最优的 **63.73%**，验证了互补增益——D- 提供真实故障分布，D+ 扩展数据多样性和覆盖范围。


**奖励设计消融**（Figure 5, Figure 6）：移除 step-level 奖励后，Code 子集的 step-level 准确率从 **18% 骤降至 12%**，MATH 子集从 **35% 降至 27%**，证明细粒度步骤监督对精确定位至关重要。移除 agent-level 奖励仅造成 agent-level 准确率小幅下降（Code: 72.2% → 68.9%），表明 agent 级标签提供辅助但非主导的指导。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_l05DseqvuD/figures/014_Figure_5.jpg]]
*Figure 5: Ablation results at the agent level under w/o G setting. Removing agent-level reward yields only a moderate performance decrease, indicating that agent-level supervision provides some but not dominant guidance in failure attribution*

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_l05DseqvuD/figures/015_Figure_6.jpg]]
*Figure 6: Ablation results at the step level under w/o G. Removing step-level reward significantly decreases step-level accuracy, emphasizing the essential role of fine-grained, step-wise supervision for accurate error localization*

**分析器与攻击者主干消融**（Table 4, Table 5）：更强的分析器 LLM 显著提升反事实修正质量——**DeepSeek-V3.1-Terminus** 的 Pass@1 修正成功率达 **54%**，而 **Qwen3-32B** 仅为 **26%**。攻击者方面，**DeepSeek-V3.1-Terminus** 的故障注入 Pass@1 成功率为 **57%**，而安全对齐过强的 **GPT-5-Mini** 几乎完全拒绝生成攻击，限制了数据多样性。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_l05DseqvuD/figures/016_Table_4.jpg]]
*Table 4: Analyzer ablation across different analyzer LLM backbones*

### 稳定性与失败模式

多轮运行稳定性分析（Table 7）显示，各模型在 Who&When 基准上的精度波动较小（标准差通常在 2~3% 范围内），AgenTracer-8B 的优势在统计上是稳定的。

**主要失败模式**：
1. **长链依赖任务**：当错误步骤与最终失败的因果关系跨越多个中间步骤时，模型倾向于归因于离失败最近的步骤而非最早的决定性错误。
2. **领域偏移**：在训练中未见过的智能体框架或工具类型上，归因准确率下降（当前仅在 MetaGPT、AutoGen 等框架上验证）。
3. **多故障点场景**：方法假设存在单个最早的可修正错误步骤，对同时存在的多个独立故障点或级联故障的归因能力有限。
4. **w/o G 设定下的 step-level 瓶颈**：缺乏理想轨迹对照时，Code 子集的 step-level 准确率仅 18.23%，表明从纯失败轨迹中推断“应该做什么”仍极具挑战。

## 定位与知识库关联

### 问题定位：多智能体故障归因的自动化困境

当前LLM驱动的多智能体系统（如MetaGPT、AutoGen、MaAS等）在复杂任务中故障频发，失败率可达86.7%。然而，现有的自动故障归因方法准确率极低（通常<10%），其根本瓶颈并非模型容量不足，而是**缺乏大规模高精度标注的故障轨迹数据**。通用LLM难以从冗长的多步交互序列中精准定位决定性错误步骤——这构成了本工作的核心动机。

### 方法谱系：从手工标注到自动化合成

AgenTracer在方法谱系中占据了一个独特位置：它并非直接与某类故障归因基线竞争，而是**重新定义了数据获取范式**。传统方法依赖少量人工标注的故障轨迹或零样本推理，而AgenTracer通过两条互补路径实现自动化标注：

1. **反事实重放（Counterfactual Replay）**：对失败轨迹，利用分析器智能体（π_analyzer）为每一步提议局部修正动作，通过系统性地替换错误动作为理想动作，定位最早的可修正错误步骤(t*, i*)。这本质上是**因果推断中的反事实干预**在智能体轨迹上的应用。

2. **程序化故障注入（Programmatic Fault Injection）**：对成功轨迹，通过扰动算子Π在步骤t生成故障变体；若导致系统失败，则(t, μ(t))即为已知的决定性错误。这借鉴了软件测试中的**故障注入**思想，但将其扩展到LLM智能体的语义层面。

这两条路径的协同使得AgenTracer能够构建TracerTraj-2.5K——一个超过2000条高置信度轨迹-错误对的数据集，覆盖代码（MBPP+、KodCode）、数学推理（MATH、GSM8K）和通用智能体任务（GAIA、HotpotQA）三个领域。

### 训练范式：多粒度强化学习的创新

在模型训练层面，AgenTracer-8B以**QWEN3-8B**（Yang et al., 2025）为基础模型，采用GRPO（Guo et al., 2025）在线强化学习框架。其核心创新在于**多粒度奖励设计**：

- **格式合规性**：二值门控，确保输出结构正确
- **Agent级识别准确性**：二元奖励，判断负责智能体是否正确
- **Step级高斯核奖励**：$r_{\mathrm{step}}(\hat{t}_k) = \exp\left(-\frac{(\hat{t}_k - t^*)^2}{2\sigma^2}\right)$，预测步骤与真实决定性步骤越近，奖励越高

总奖励函数为：
$$R(\hat{p}_k) = \mathbb{I}_{\mathrm{format}} \cdot \left( \lambda \cdot r_{\mathrm{step}}(\hat{t}_k) + (1-\lambda) \cdot r_{\mathrm{agent}}(\hat{i}_k) \right)$$

这种设计使得轻量级模型（8B参数）能够在归因精度上超越巨型商业模型。消融实验（Figure 5, Figure 6）证实：移除step-level奖励导致步骤准确率显著下降（Code: 18%→12%，MATH: 35%→27%），而移除agent-level奖励仅造成中等下降（Code agent-level: 72.2%→68.9%），表明**细粒度步骤监督是核心驱动力**。

### 与基线的差异化定位

AgenTracer-8B在Who&When基准上对比了8个基线模型，涵盖不同规模和技术路线：

| 基线模型 | 类型 | 规模 | 核心差异 |
|---------|------|------|---------|
| **QWEN3-8B/32B** (Yang et al., 2025) | 开源通用LLM | 8B/32B | 直接提示归因，无专门训练 |
| **LLAMA-3.2-3B** (Grattafiori et al., 2024) | 开源轻量LLM | 3B | 极小规模，归因能力有限 |
| **QWEN3-CODER-480B** (Yang et al., 2025) | 开源代码优化LLM | 480B | 大规模但非归因专用 |
| **GPT-4.1** (OpenAI, 2025) | 闭源商业模型 | 未公开 | 通用能力强但归因精度低 |
| **DeepSeek-R1** (Guo et al., 2025) | 推理增强LLM | 未公开 | 推理链增强但非归因优化 |
| **Gemini-2.5-Pro** (Comanici et al., 2025) | 闭源商业模型 | 未公开 | 多模态能力强但归因精度不足 |
| **Claude-4-Sonnet** (Anthropic, 2025) | 闭源商业模型 | 未公开 | 安全对齐强，归因竞争力较高 |

关键发现：AgenTracer-8B在Who&When handcraft子集上以agent-level准确率63.82超越DeepSeek-R1的53.44（+10.38）和Gemini-2.5-Pro的45.64（+18.18）；在TracerTraj-MATH step-level上以57.63超越Claude-4-Sonnet的46.03（+11.60）。这证明了**专用训练+精细奖励**比**模型规模**更关键。

### 适用边界与局限

尽管AgenTracer表现优异，其适用边界需明确认知：

1. **数据构建依赖强LLM**：分析器智能体的质量直接影响反事实修正准确率（DeepSeek-V3.1-Terminus Pass@1 54% vs. Qwen3-32B 26%），而攻击者LLM的故障注入成功率也因模型而异（DeepSeek-V3.1-Terminus Pass@1 57%）。安全对齐过强的模型（如GPT-5-Mini）可能完全拒绝生成攻击，限制数据多样性。

2. **单故障点假设**：当前方法只定位单个最早的决定性错误步骤，对于同时存在的多个独立故障点或级联故障的归因能力有限。公式$(i^*, t^*) = \arg\min_{(i,t) \in \mathcal{C}(\tau)} t$隐含了“最早修正即可恢复”的假设。

3. **领域泛化未验证**：TracerTraj数据集主要覆盖代码、数学与一般智能体任务，对物理模拟、具身智能等领域的泛化性尚待验证。迁移到全新智能体拓扑或未见过的工具类型时可能面临分布偏移。

4. **w/o G设定仍有提升空间**：在缺乏真实解的情况下，AgenTracer-8B在Who&When automated step-level (w/o G)上以37.30略低于Claude-4-Sonnet的38.83，表明无监督归因仍是开放挑战。

5. **特定设定下巨型模型仍具竞争力**：在TracerTraj-agentic w/ G设定下，AgenTracer-8B的agent-level准确率53.28略低于Claude-4-Sonnet的55.20，模型容量与归因精度的平衡仍有优化空间。

### 开放问题与未来方向

1. **多模态扩展**：能否将AgenTracer扩展到视觉+语言的智能体系统？当前实验主要聚焦文本和代码任务。

2. **无监督归因**：如何在缺乏真实解（ground truth）的情况下进行可靠归因？w/o G设定下的性能提升是核心挑战。

3. **多故障点归因**：当轨迹中存在多个相互依赖的故障点时，如何扩展模型以进行集合级别的因果归因？

4. **人机协同**：能否结合人类反馈或交互式修正来持续提升归因模型的精度？

5. **实时集成**：该方法能否被无缝集成到动态智能体框架中，实现实时故障报警和自我修复？Figure 3已初步展示了4.8%~14.2%的系统性能提升，但实时性尚未验证。

6. **弱模型蒸馏**：如何减少对高质量分析器和攻击者LLM的依赖？通过弱模型蒸馏或自标注的迭代提升是可能的路径。

### 知识库定位总结

AgenTracer处于**LLM智能体可靠性工程**与**自动化数据标注**的交叉点。它继承并扩展了因果推断中的反事实干预思想、软件测试中的故障注入技术、以及强化学习中的细粒度奖励设计，形成了一套从数据合成到模型训练的完整pipeline。其核心贡献不在于提出全新的模型架构，而在于**重新定义了多智能体故障归因的数据获取和训练范式**，证明了轻量级专用模型可以在特定任务上超越巨型通用模型。

## 原文 PDF

![[paperPDFs/ICLR_2026/AgenTracer_Who_Is_Inducing_Failure_in_the_LLM_Agentic_Systems.pdf]]
