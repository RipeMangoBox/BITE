---
title: "R1-Code-Interpreter: LLMs Reason with Code via Supervised and Multi-stage Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/R1_Code_Interpreter_LLMs_Reason_with_Code_via_Supervised_and_Multi_stage_Reinforcement_Learning.pdf
openreview_forum_id: FNlNH0iFOx
aliases:
- RCIRC
- R1-Code-Interpreter
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "基于改进潜力的多阶段课程学习：通过评估每个样本在不同代理策略下的正确率，计算p(1-p)作为改进潜力得分，并按此对样本排序，优先训练高潜力的样本，确保每个训练阶段的批次中包含最大化梯度信号的样本。"
primary_logic: "通过测量改进潜力来指导GRPO课程学习，能够有效解决多任务Code Interpreter训练中的信号稀疏问题，将RL性能增益从+3.4%提升至+9.3%，并使得开源模型R1-CI-14B在144个多样化推理和规划任务上超越GPT-4o。"
claims:
- "直接应用GRPO于多任务Code Interpreter训练时，平均性能提升仅为+3.4%，且许多任务得分极低（接近0）。"
- "理论分析表明，策略梯度范数的上界正比于p(1-p)，在p≈0或1时消失，导致优化停滞。"
- "采用基于改进潜力的多阶段课程学习后，RL增益提升至+9.3%，最终模型R1-CI-14B在测试集上达到72.4%的准确率。"
- "R1-CI-14B在37个测试任务上显著优于GPT-4o纯文本（58.6%）和GPT-4o自带Code Interpreter（70.9%）。"
---

# R1-Code-Interpreter: LLMs Reason with Code via Supervised and Multi-stage Reinforcement Learning

> [!tip] 核心洞察
> 通过测量改进潜力来指导GRPO课程学习，能够有效解决多任务Code Interpreter训练中的信号稀疏问题，将RL性能增益从+3.4%提升至+9.3%，并使得开源模型R1-CI-14B在144个多样化推理和规划任务上超越GPT-4o。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | R1-Code-Interpreter：通过监督与多阶段强化学习实现大语言模型的代码推理 |
| 英文题名 | R1-Code-Interpreter: LLMs Reason with Code via Supervised and Multi-stage Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=FNlNH0iFOx); [GitHub](https://github.com/yongchao98/R1-Code-Interpreter); [Project](https://huggingface.co/yongchao98) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | R1-Code-Interpreter (R1-CI) |
| Dataset | 37 Test Tasks (SymBench, BBH, Reasoning-Gym average), 37 Test Tasks |

> [!tip] 效果简介
> - 37 Test Tasks (SymBench, BBH, Reasoning-Gym average) 上，Accuracy (%) 为 72.4，对比 58.6 (GPT-4o All Text)，变化 +13.8。
> - 37 Test Tasks (SymBench, BBH, Reasoning-Gym average) 上，Accuracy (%) 为 72.4，对比 70.9 (GPT-4o Code Interpreter)，变化 +1.5。
> - 37 Test Tasks 上，Accuracy (%) 为 72.4，对比 44.1 (Qwen-2.5-14B All Text)，变化 +28.3。

## 概述

### 问题与瓶颈

大语言模型（LLM）在复杂推理与规划任务中常因缺乏精确计算支持而犯错，而将代码解释器（Code Interpreter）与LLM结合的多轮交互式推理框架虽能缓解此问题，却面临一个关键的训练瓶颈：在多任务强化学习（RL）训练中，由于任务异质性和有效样本稀缺，大量训练样本的解答正确率 $p$ 趋近于 0 或 1，导致 GRPO 的策略梯度信号消失（梯度范数上界正比于 $p(1-p)$），更新仅由 KL 正则项主导，使得标准 GRPO 训练仅带来微弱的性能提升（+3.4%）。

### 核心方法

**R1-Code-Interpreter (R1-CI)** 提出了一套完整的训练框架来解决上述瓶颈，其核心创新在于 **基于改进潜力的多阶段课程学习**：

1. **改进潜力测量**：使用四种预设计代理策略（All Text、All Code、Code Agent、CodeSteer）对每个训练样本多次采样，估计其正确率 $p_i$，并计算归一化改进潜力得分 $\Pi_i = 4p_i(1-p_i)$（最大化于 $p_i=0.5$）。
2. **多阶段课程学习**：按 $\Pi_i$ 将样本从高到低排序，划分为四个训练阶段，优先训练高潜力样本，确保每个批次中包含最大化梯度信号的样本。
3. **配套设计**：先用 SFT 合成数据进行预热（warm-start），再启动 GRPO；采用组合奖励（正确性 + 格式合规 + 效率惩罚）；将代码执行解耦至专用 CPU 沙箱以提升训练效率。

### 核心结论

- **RL 增益大幅提升**：多阶段课程学习将 RL 性能增益从 +3.4% 提升至 **+9.3%**（Table 3）。
- **开源模型超越闭源大模型**：最终模型 **R1-CI-14B** 在 37 个测试任务上达到 **72.4%** 的准确率，显著优于 GPT-4o 纯文本（58.6%）和 GPT-4o 自带 Code Interpreter（70.9%），同时较基座模型 Qwen-2.5-14B 纯文本（44.1%）提升 **+28.3%**（Figure 1a, Table 3）。
- **训练效率优化**：代码执行解耦至 CPU 沙箱使训练时间减少 **39%**。

### 方法谱系与知识库定位

R1-CI 属于 **代码增强推理型 LLM** 的训练方法，其核心贡献在于将 **课程学习** 与 **GRPO 强化学习** 相结合，并通过 **改进潜力** 这一可量化指标指导课程编排。相较于以下基线方法：

| 方法 | 推理范式 | 训练策略 |
|------|----------|----------|
| **All Text** | 纯文本思维链 | 无 RL |
| **All Code** | CoT 后输出代码作为最终答案 | 无 RL |
| **Code Agent (CI wo Fine-tune)** | 多轮代码解释器，未微调 | 无 RL |
| **CodeSteer** (Chen et al., 2025) | 额外引导代理控制的代码代理 | 无 RL |
| **GPT-4o Code Interpreter** | 闭源自带代码解释器 | 未知 |

R1-CI 通过 **SFT 预热 → 改进潜力测量 → 多阶段 GRPO 课程学习** 的管线，在开源模型上首次实现了对 GPT-4o 代码解释器的超越，验证了“以改进潜力驱动课程学习”这一策略在多任务代码推理 RL 训练中的有效性。

## 背景与动机

### 大语言模型推理的范式演进

大语言模型（LLM）在复杂推理与规划任务上取得了显著进展，但其推理范式仍存在根本性分歧。纯文本思维链（Chain-of-Thought, CoT）推理虽然展现出强大的逻辑推导能力，却受限于符号计算、精确搜索和状态空间探索等结构化操作——这些恰恰是代码执行所天然擅长的领域。相反，将代码作为最终答案输出的“全代码”范式虽然利用了计算能力，却牺牲了推理过程的可解释性和中间步骤的验证机会。

这一困境在GPT-4o等闭源模型中得到了部分缓解：其内置的Code Interpreter允许模型在多轮交互中交替进行文本推理与代码执行，从而将语言理解与计算能力有机融合。然而，如何将这种交互式代码推理能力有效地注入开源大语言模型，并使其在多样化的推理任务上超越闭源系统，仍是一个开放且极具挑战性的问题。

### 多任务强化学习训练的核心瓶颈

将Code Interpreter与开源LLM结合，并通过强化学习（RL）进行优化，面临一个深层困境：**任务异质性导致的梯度信号稀疏**。在涵盖144个推理与规划任务的训练集中，不同任务的难度和可解性差异巨大。当使用标准的组相对策略优化（Group Relative Policy Optimization, GRPO）进行训练时，大量样本的解答正确率 $p$ 趋近于0（完全无法解决）或1（已经完美解决）。

理论分析揭示了这一现象的数学本质：策略梯度范数的上界正比于 $p(1-p)$（见公式4.5），当 $p \approx 0$ 或 $p \approx 1$ 时，梯度信号几乎消失，策略更新仅由KL正则项主导。这导致标准GRPO训练在多任务Code Interpreter场景下仅能带来微弱的性能提升——实验表明平均增益仅为 **+3.4%**（Figure 3d, Section 4.2），训练奖励在早期短暂上升后迅速趋于平台（Figure 3a），许多任务的得分甚至始终为零。

### 核心洞察：以改进潜力引导课程学习

上述瓶颈的因果关键在于：**并非所有训练样本对策略优化具有同等价值**。一个样本的“改进潜力”取决于当前策略在该样本上的成功概率 $p$——当 $p = 0.5$ 时，模型处于最不确定的状态，此时梯度信号最为丰富，策略更新的边际收益最大。

基于这一洞察，本文提出了**改进潜力**（Improvement Potential）的量化指标：
$$\Pi_i = 4 p_i (1-p_i)$$
该指标在 $p_i = 0.5$ 时达到最大值1，在 $p_i = 0$ 或 $p_i = 1$ 时归零，精确刻画了每个训练样本在当前模型能力下的可优化空间。通过测量每个样本的 $\Pi_i$ 并按此排序，可以构建一个从高潜力到低潜力的多阶段课程，确保RL训练始终聚焦于能产生最大梯度信号的样本，从而从根本上解决信号稀疏问题。

### 本文动机

综上所述，本文的动机源于三个递进层次：

1. **能力缺口**：开源LLM在交互式代码推理能力上与GPT-4o等闭源系统存在显著差距，亟需有效的训练框架来弥合这一鸿沟。
2. **训练困境**：直接应用GRPO于多任务Code Interpreter训练时，任务异质性导致梯度信号稀疏，RL增益微乎其微，需要新的训练策略来释放RL的潜力。
3. **方法论突破**：通过量化“改进潜力”并以此指导课程学习，有望将RL性能增益从+3.4%大幅提升至+9.3%，使开源模型在多样化推理任务上超越GPT-4o。

## 核心创新

R1-Code-Interpreter (R1-CI) 的核心创新并非提出全新的算法，而是针对**多任务代码解释器强化学习训练中策略梯度信号消失**这一关键瓶颈，设计了一套系统性的解决方案。其创新点可归纳为以下三个环环相扣的层面：

### 1. 瓶颈洞察：多任务GRPO中的信号稀疏困境

标准GRPO在多任务代码解释器训练中面临严重的优化停滞。实验表明，直接对107个任务应用GRPO，平均性能提升仅为**+3.4%**，许多任务得分趋近于零（Figure 3d）。作者通过理论分析揭示了根本原因：在二元奖励（正确/错误）设定下，策略梯度范数的上界正比于 $p(1-p)$（Equation 4.5），其中 $p$ 为样本的正确率。当任务异质性导致大量样本的 $p$ 接近0或1时，策略梯度信号消失，模型更新几乎完全由KL正则项主导，从而陷入优化瓶颈。

### 2. 关键机制：基于改进潜力的多阶段课程学习

为解决上述信号稀疏问题，作者提出了**改进潜力（Improvement Potential, IP）** 的概念，定义为 $\Pi_i = 4p_i(1-p_i)$（Equation 4.6），在 $p_i=0.5$ 时取得最大值。其核心操作是：在GRPO训练前，使用四种预设计代理策略（Code Agent、CodeSteer、All Text、All Code，Table 2）对每个训练样本进行多次采样，估计其正确率 $p_i$ 和对应的 $\Pi_i$，然后按 $\Pi_i$ 从高到低将样本划分为四个阶段（$\Pi_i$ 范围分别为 $[0.64, 1.00]$、$[0.48, 0.64]$、$[0.32, 0.48]$、$[0.0, 0.32]$），依次进行课程训练。这一设计确保每个训练阶段的批次中包含最大化梯度信号的样本，使RL增益从 **+3.4% 跃升至 +9.3%**（Table 3）。

### 3. 系统协同：框架、环境与初始化的配套改进

课程学习的效果依赖于配套的系统设计：

- **多轮交互式代码解释器框架**：模型在文本推理与代码执行之间交替迭代（最多8次代码调用），执行结果以特殊token `Code Execution Results:` 注入生成流，实现真正的“推理-执行-反思”闭环。消融实验表明，该框架的泛化性能显著优于单轮文本或单轮代码框架（Figure 9a）。
- **CPU沙箱解耦执行**：将代码执行从GPU计算中解耦至专用64核CPU节点并行处理，训练时间减少**39%**（从4500 GPU小时降至1845 GPU小时），同时避免了GPU利用率低下的问题（Figure 12）。
- **SFT预热策略**：冷启动模型直接进行GRPO几乎无性能提升（Figure 15），因此先用GPT-4o合成的6.5k条正确多轮轨迹进行监督微调，使模型获得基本的代码解释器使用能力，为后续RL训练提供有效初始化。

最终，这套“SFT预热→IP测量→多阶段课程GRPO”的协同设计，使得开源14B模型R1-CI-14B在144个多样化推理与规划任务上达到**72.4%的准确率**，超越GPT-4o纯文本推理（58.6%）及其自带Code Interpreter（70.9%）（Table 3, Figure 1a）。

## 整体框架

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_FNlNH0iFOx/figures/003_Figure_1.jpg]]
*Figure 1: Training Code Interpreter-augmented reasoning models with multi-stage GRPO on 144 reasoning and planning tasks. (a) Our best model, R1-CI-14B, outperforms both GPT-4o (text-only) and GPT-4o with Code Interpreter. (b) Training reward and test scores improve steadily through the curriculum learning, then plateau at stage 4 after adding low-potential samples. (c) To assess sample effectiveness, we estimate improvement potential by repeatedly sampling answers with different agent frameworks and analyzing the correct/wrong distribution. GRPO begins with high-potential samples and gradually incorporates lower-potential ones*

R1-Code-Interpreter（R1-CI）是一个将代码解释器（Code Interpreter）深度集成到开源大语言模型推理过程中的训练框架。其核心目标是通过监督微调（SFT）与多阶段强化学习（GRPO），使模型学会在多轮文本推理与代码执行的交替中求解复杂的推理与规划任务。整体pipeline由五个关键模块串联而成，形成“任务准备→SFT预热→潜力测量→课程强化学习→评估”的闭环，如图1c所示。

### 任务准备与数据合成

框架的起点是**任务策展（Task Curation）**：从SymBench、Big-Bench-Hard（BBH）和Reasoning-Gym三个基准中收集并标准化144个推理与规划任务，其中107个用于训练，37个用于测试。随后进入**SFT数据合成**阶段：利用GPT-4o为每个训练任务生成多轮文本/代码交替的推理轨迹，并仅筛选出答案正确的样本，最终构建约6.5k条高质量多轮交互轨迹。这些轨迹显式展示了“文本推理→生成代码→执行代码→基于结果修正推理”的完整循环，为后续SFT提供了行为模板。

### 交互式推理引擎

在推理框架层面，R1-CI采用**多轮文本/代码交替的交互式代码解释器**。模型在每轮生成中可以选择输出自然语言推理或Python代码块；一旦检测到代码块，系统自动提取并在专用CPU沙箱中执行，将执行结果以特殊标记“Code Execution Results:”前缀追加回生成上下文。该循环最多允许8次代码调用，或直到模型输出最终答案标签`\boxed{...}`为止。这一设计使模型能够动态利用代码的计算能力来验证、修正和深化其文本推理。

### 强化学习训练与瓶颈发现

SFT预热后的模型进入**GRPO强化学习**阶段。训练目标为最大化期望奖励并最小化与参考策略的KL散度（公式4.1），其中奖励由三部分组成：正确性奖励（+1.0）、格式合规奖励（±0.1）和效率惩罚（超过6轮代码调用时-0.1）。然而，直接在多任务设定下应用标准GRPO时，研究者发现了一个关键瓶颈：由于任务异质性和有效样本稀缺，大量训练样本的解答正确率$p$接近0或1，导致GRPO的策略梯度信号消失——理论分析表明，策略梯度范数的上界正比于$p(1-p)$（公式4.5），在$p \approx 0$或1时趋近于零，此时参数更新仅由KL正则项主导，性能提升微弱（仅+3.4%）。

### 改进潜力测量与多阶段课程学习

为突破上述瓶颈，框架引入**改进潜力测量**模块：使用四种预设计的代理策略（Code Agent、CodeSteer、All Text、All Code）对每个训练样本重复采样20次，估计其经验正确率$p_i$，并计算归一化改进潜力得分$\Pi_i = 4p_i(1-p_i)$（公式4.6）。该得分在$p_i=0.5$时最大化，精确量化了每个样本能提供的策略梯度信号强度。

基于此，框架进入**多阶段课程GRPO**：按$\Pi_i$将训练样本划分为四个阶段——$[0.64, 1.00]$、$[0.48, 0.64]$、$[0.32, 0.48]$、$[0.0, 0.32]$——每个阶段运行150步GRPO，逐步从高潜力样本扩展到低潜力样本。这一课程设计确保每个训练批次的样本都能提供最大化的梯度信号，将RL性能增益从+3.4%提升至+9.3%。

### 代码执行解耦

为提升训练效率，框架将代码执行从GPU计算中**解耦至专用CPU沙箱**（五台64核CPU节点）。生成的代码在沙箱中并行执行，避免代码执行占用GPU并导致训练等待。这一架构优化使整体RL训练时间减少约39%。

### 最终评估

训练完成的模型进入**评估引擎**，在37个测试任务上基于规则自动评判任务完成情况。最终模型R1-CI-14B达到72.4%的测试准确率，显著优于GPT-4o纯文本推理（58.6%）和GPT-4o自带Code Interpreter（70.9%），验证了整个框架的有效性。

## 核心模块与公式推导

### 多轮代码解释器交互框架

R1-CI 的核心推理循环是一个文本推理与代码执行交替进行的交互式代理。模型在生成过程中，当检测到 Python 代码块时，系统自动提取并在专用沙箱中执行该代码，随后将执行结果（以 `Code Execution Results:` 为前缀的特殊标记）追加到当前生成序列中，模型据此继续推理。这一循环持续进行，直到满足以下两个终止条件之一：（1）达到最大代码调用次数（8 次），或（2）模型输出 `\boxed{...}` 包裹的最终答案（Section 3, Figure 2）。

### 训练管线模块

R1-CI 的训练管线由以下关键模块串联构成（Figure 1c）：

1. **任务整理（Task Curation）**：收集并标准化 144 个推理与规划任务，涵盖 SymBench、BBH、Reasoning-Gym 三个基准。
2. **SFT 数据合成（SFT Data Synthesis）**：利用 GPT-4o 生成多轮文本/代码交替轨迹，仅保留答案正确的样本，每个任务最多保留 70 条有效轨迹以防止训练坍塌。
3. **改进潜力测量（Improvement Potential Measurement）**：使用四种预设代理策略（All Text、All Code、Code Agent、CodeSteer，见 Table 2）对每个样本进行多次采样（共 20 次），估计其正确率 $p_i$ 和归一化改进潜力得分 $\Pi_i$。
4. **多阶段课程 GRPO（Multi-stage Curriculum GRPO）**：按 $\Pi_i$ 将样本分为四个阶段（$\Pi_i$ 范围分别为 $[0.64, 1.00]$、$[0.48, 0.64]$、$[0.32, 0.48]$、$[0.0, 0.32]$），每阶段训练 150 步，逐步纳入更低潜力的样本。
5. **代码执行沙箱（Code Execution Sandbox）**：在五台 64 核 CPU 节点上并行执行代码，将代码执行与 GPU 上的梯度计算解耦，使训练时间减少约 39%（Section 4.1, Section 5.4）。

### 核心公式

#### RL 优化目标

R1-CI 的强化学习目标是在代码解释器 $\mathcal{C}$ 的条件下最大化期望奖励，同时约束策略与参考策略的 KL 散度：

$$
\operatorname*{max}_{\pi_{\theta}} \mathbb{E}_{x\sim D, y\sim \pi_{\theta}(\cdot|x;\mathcal{C})} [r_{\phi}(x,y)] - \beta \mathbb{D}_{\mathrm{KL}}[\pi_{\theta}(y|x;\mathcal{C}) \| \pi_{\mathrm{ref}}(y|x;\mathcal{C})]
$$

其中 $\pi_{\theta}$ 为当前策略，$\pi_{\mathrm{ref}}$ 为参考策略（SFT 后的模型），$r_{\phi}$ 为奖励函数，$\beta$ 为 KL 惩罚系数（Equation 4.1）。

#### GRPO 损失函数

采用 Group Relative Policy Optimization（GRPO），对每个问题采样 $G$ 条轨迹，以组内相对优势进行策略更新：

$$
\mathcal{I}_{\mathrm{GRPO}}(\theta)=\mathbb{E}_{x\sim D, y_{1:G}\sim\pi_{\mathrm{ref}}(\cdot|x;\mathcal{C})} \Bigg[ \frac{1}{G}\sum_{i=1}^{G}\frac{1}{|y_i|}\sum_{t=1}^{|y_i|} \min\Bigl( \frac{\pi_{\theta}(y_{i,t}|x,y_{i,<t};\mathcal{C})}{\pi_{\mathrm{ref}}(y_{i,t}|y_{i,<t};\mathcal{C})} \hat{A}_{i,t}, \mathrm{clip}(\dots,1-\epsilon,1+\epsilon)\hat{A}_{i,t} \Bigr) \Bigg] - \beta \mathbb{D}_{\mathrm{KL}}[\pi_{\theta}\|\pi_{\mathrm{ref}}]
$$

其中 $\hat{A}_{i,t}$ 为序列级优势广播至 token 级的结果。训练时仅对 LLM 生成的 token 计算策略梯度，代码执行结果 token 被屏蔽（Equation 4.2, Section 4.1）。

#### 奖励设计

总奖励 $R$ 为三项的加权组合（Section 4.1）：
- **正确性**：答案正确得 $+1.0$，否则得 $0$。
- **格式合规**：正确使用 `\boxed{...}` 格式得 $+0.1$，否则得 $-0.1$。
- **效率惩罚**：代码调用次数超过 6 次时扣减 $-0.1$。

#### 策略梯度信号消失的理论分析

将 GRPO 梯度分解为策略项与 KL 正则项（省略裁剪以简化）：

$$
\nabla_{\theta} \mathcal{I}_{\mathrm{GRPO}}(\theta) = \frac{1}{G}\sum_{i=1}^{G}(r_i - \bar{r}) v_i - \beta \nabla_{\theta} \mathbb{D}_{\mathrm{KL}}[\pi_{\theta}\|\pi_{\mathrm{ref}}]
$$

其中 $v_i$ 为对数概率梯度。在二值奖励（正确/错误）假设下，优势的期望方差为：

$$
\mathbb{E}\big[(r_i - \bar{r})^2\big] = p(1-p)\bigg(1 - \frac{1}{G}\bigg)
$$

进一步推导可得策略梯度范数的上界：

$$
\mathbb{E}\left[ \left\| \frac{1}{G}\sum_{i=1}^{G}(r_i - \bar{r})v_i \right\|^2 \right] \leq p(1-p)\left(1 - \frac{1}{G}\right)\mathbb{E}\left[ \frac{1}{G}\sum_{i=1}^{G}\|v_i\|^2 \right]
$$

该上界由 $p(1-p)$ 控制：当样本正确率 $p$ 接近 0 或 1 时，策略梯度信号消失，优化仅由 KL 正则项驱动，导致训练停滞（Equation 4.5, Section 4.2）。这正是多任务 GRPO 训练中性能增益微弱（仅 $+3.4\%$）的根本原因。

#### 改进潜力得分

为量化每个样本对策略更新的贡献潜力，定义归一化改进潜力得分：

$$
\Pi_i = 4 p_i (1-p_i)
$$

其中 $p_i = \frac{1}{N}\sum_{j=1}^{N} y_{i,j}$ 为使用四种代理策略共 $N=20$ 次采样中答案正确的比例。$\Pi_i$ 在 $p_i=0.5$ 时取得最大值 1.0，在 $p_i=0$ 或 $1$ 时取得最小值 0，精确刻画了该样本所能提供的最大梯度信号强度（Equation 4.6, Section 4.3）。

## 实验与分析

### 核心瓶颈：多任务GRPO的策略梯度信号消失

在多任务代码解释器强化学习训练中，直接应用GRPO面临一个根本性困境。当训练集包含107个异质性任务时，平均性能提升仅为**+3.4%**，远低于在单一任务（如Game24）上获得的+27.4%提升（Figure 3d）。大量训练样本的正确率*p*接近0或1，导致GRPO的策略梯度信号消失。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_FNlNH0iFOx/figures/008_Figure_3.jpg]]
*Figure 3: GRPO training without curriculum learning. (a) Training rewards increase slightly in the early steps, then plateau. (b) In the 14B setting, test scores across individual tasks (colored lines) show diverse trends, while the average score (bold black line) rises slightly before plateauing, mirroring (a). (c) Training curve on the single task Game24. (d) Average score improvement vs. number of tasks for GRPO training*

理论分析揭示了这一现象的数学根源。对于二元奖励（正确/错误），策略梯度范数的上界为：

$$\mathbb{E}\left[\left\|\frac{1}{G}\sum_{i=1}^{G}(r_i-\bar{r})v_i\right\|^2\right] \leq p(1-p)\left(1-\frac{1}{G}\right)\mathbb{E}\left[\frac{1}{G}\sum_{i=1}^{G}\|v_i\|^2\right]$$

该上界正比于$p(1-p)$，在$p=0.5$时达到最大，在$p\to 0$或$p\to 1$时消失（Equation 4.5）。这意味着对于模型已经完美解决（*p*≈1）或完全无法解决（*p*≈0）的任务，策略梯度项趋近于零，参数更新仅由KL正则项主导，导致优化停滞。Figure 3b直观地展示了这一现象：在多任务训练中，大量任务的得分始终徘徊在10分以下（通常为0），训练奖励在早期小幅上升后迅速进入平台期。

### 解决方案：基于改进潜力的多阶段课程学习

为解决上述瓶颈，R1-CI提出**改进潜力**（Improvement Potential）度量：

$$\Pi_i = 4p_i(1-p_i)$$

其中$p_i$为样本*i*在四种预设计代理策略（All Text、All Code、Code Agent、CodeSteer，见Table 2）下各采样5次共20次试验中的正确率。$\Pi_i$在$p_i=0.5$时达到最大值1，精确量化了每个样本对GRPO梯度信号的贡献潜力。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_FNlNH0iFOx/figures/011_Table_2.jpg]]
*Table 2: Four pre-designed agents used in the measurement of improvement potential*

基于此，训练样本按$\Pi_i$被划分为四个阶段（Figure 4）：
- **Stage 1**：$\Pi_i \in [0.64, 1.00]$，高潜力样本
- **Stage 2**：$\Pi_i \in [0.48, 0.64]$
- **Stage 3**：$\Pi_i \in [0.32, 0.48]$
- **Stage 4**：$\Pi_i \in [0.0, 0.32]$，低潜力样本

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_FNlNH0iFOx/figures/010_Figure_4.jpg]]
*Figure 4: Multi-stage curriculum learning with the guid- Figure 5: Score distribution across 144 training and testing ance of measured improvement potential for each sample. tasks for the four compared methods*

每个阶段运行150步，逐步将训练分布从高潜力样本扩展到全量数据集。Figure 4显示，训练奖励和测试得分在前两个阶段显著上升，每次合并新样本时奖励出现短暂下降后恢复上升，而在第四阶段几乎无额外收益——表明低潜力样本对训练的边际贡献有限。

### 主要实验结果

Table 3汇总了各方法在144个任务（107训练+37测试）上的性能。核心发现如下：

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_FNlNH0iFOx/figures/012_Table_3.jpg]]
*Table 3: Scores of compared methods on 144 tasks across three benchmarks SymBench (SymB.), Big-Bench-Hard (BBH), and Reasoning-Gym (Rea.G.). Best result for each dataset is bold. We abbreviate R1-Code-Interpreter as R1-CI, Curriculum Learning as CL, and Improvement Potential as IP*

**R1-CI-14B在37个测试任务上达到72.4%的平均准确率**，显著超越：
- Qwen-2.5-14B纯文本基线（44.1%）：**+28.3个百分点**
- GPT-4o纯文本推理（58.6%）：**+13.8个百分点**
- GPT-4o自带Code Interpreter（70.9%）：**+1.5个百分点**

Figure 1a直观展示了R1-CI-14B相对于GPT-4o两种变体的优势。值得注意的是，R1-CI-14B以14B参数量超越了GPT-4o这一更大规模的闭源模型，证明了代码解释器增强与多阶段课程学习的有效性。

**多阶段课程学习将RL增益从+3.4%提升至+9.3%**。Table 3中R1-CI（w/ CL+IP）与R1-CI（w/o CL）的对比量化了这一贡献：在14B规模下，无课程学习的GRPO仅将SFT基线的测试准确率从63.1%提升至66.5%（+3.4%），而引入改进潜力引导的课程学习后进一步提升至72.4%（+9.3%）。

**改进潜力排序优于难度排序**。Table 3中R1-CI与R1-CI（wo IP）的对比表明，基于$\Pi_i$的课程学习优于基于问题难度的排序，验证了“最大化梯度信号”这一设计原则的正确性。

### 关键消融实验

**SFT预热是GRPO有效性的前提**。Figure 15对比了热启动（先SFT后GRPO）与冷启动（直接GRPO）的效果：冷启动模型在GRPO训练中几乎无性能提升，即使训练数据已按改进潜力校准。这表明SFT阶段为模型提供了与代码解释器交互的基本能力，是后续RL优化的必要基础。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_FNlNH0iFOx/figures/028_Figure_15.jpg]]
*Figure 15: Warm- vs. cold-start. With GRPO, a warm start (preceded by SFT) outperforms a cold start for Qwen-14B model as the base model. The model without prior SFT process gets barely performance lifting during training, even though the training data also has been calibrated by improvement potential for multi-stage training*

**多轮代码解释器框架优于单轮变体**。Figure 9a显示，在SFT阶段，多轮Code Interpreter框架在测试任务上的泛化性能明显优于单轮All Text和单轮All Code框架，后者在训练集上表现尚可但在测试集上差距显著。

**SFT数据质量至关重要**。Figure 9b表明，在SFT数据中包含错误答案会降低模型性能并增加方差；省略提示词变化或去除多轮交互强调同样损害效果。

**高改进潜力样本驱动有效学习**。Figure 14将相同数量的样本按$\Pi_i$范围分为三组（[0.64-1.00]、[0.48-0.64]、[0.32-0.48]）分别训练：高潜力组展现出持续上升的训练奖励和更高的BBH测试得分，直接验证了改进潜力引导的有效性。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_FNlNH0iFOx/figures/027_Figure_14.jpg]]
*Figure 14: GRPO training using datasets grouped by improvement potential: Group 1 [0.64–1.00], Group 2 [0.48–0.64], and Group 3 [0.32–0.48]. Each group contains the same number of samples drawn from the same Reasoning Gym and SymBench tasks, but with different improvement potential ranges. Models were evaluated on BBH for fair comparison. Models trained on higher-potential samples show consistently rising training rewards and achieve higher BBH test scores*

**Qwen-2.5基座优于DeepSeek蒸馏模型**。Table 5的基座模型消融显示，在代码生成任务上，Qwen-2.5系列在SFT和各类训练框架下均一致优于DeepSeek蒸馏模型。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_FNlNH0iFOx/figures/029_Table_5.jpg]]
*Table 5: Ablation studies on using DeepSeek-distilled reasoning models as the base model*

**代码执行解耦至CPU沙箱减少39%训练时间**。通过将代码执行从GPU迁移至五台64核CPU节点的专用沙箱（Section 4.1），总训练时间从4500 GPU小时降至1845 GPU小时。Figure 12展示了无沙箱时GPU利用率的剧烈波动和频繁空闲。

**RL算法选择具有鲁棒性**。Figure 7对比了GRPO、PPO和Reinforce++三种RL算法，三者在训练奖励和测试得分上表现相当，表明课程学习框架对底层RL算法不敏感。

### 涌现行为分析

GRPO训练催生了若干涌现行为（Figure 6）：
- **代码自检**：Figure 6a显示，训练后包含代码自检的回答轨迹比例大幅上升，模型学会通过代码执行验证推理结果。
- **高效交互**：Figure 6b表明，大多数问题在4次代码交互内解决，保持了推理过程的经济性。
- **响应长度稳定**：Figure 6c显示，与先前RL训练导致响应长度膨胀的观察不同，R1-CI的平均响应长度在训练过程中保持稳定。

### 分布外泛化

Figure 13展示了在SymBench和Reasoning-Gym上训练、在BBH上测试的OOD泛化实验。两阶段GRPO训练后的模型在BBH上的表现与原R1-CI-14B（在包含BBH的全量数据上训练）相当，表明课程学习框架能有效泛化至未见任务分布。

Table 4进一步报告了在GPQA Diamond和AIME 24&25上的OOD性能：R1-CI-14B分别达到50.2和42.0，显著超越Qwen-2.5基线和CodeSteer变体。R1-CI-7B同样展现出跨任务泛化能力（GPQA 39.0，AIME 15.0）。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_FNlNH0iFOx/figures/024_Table_4.jpg]]
*Table 4: Performance of R1-CI-14B and R1-CI-7B in OOD tasks: Graduate-Level Google-Proof Q&A (GPQA, Diamond) (Rein et al., 2024), and American Invitational Mathematics Examination (AIME 24&25)*

### 失败模式与局限

尽管整体性能优异，部分任务仍得分极低甚至为零（Figure 5的得分分布显示R1-CI在低分段仍有少量任务），表明基座LLM的固有能力瓶颈无法仅通过训练框架完全克服。此外，Figure 4中第四阶段几乎无收益的现象暗示，对于极低改进潜力的样本，当前方法缺乏有效的学习机制——这可能是未来工作的方向。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_FNlNH0iFOx/figures/030_Table_6.jpg]]
*Table 6: The evaluated capabilities of all 144 tasks, classified as Execution, Planning, and Reasoning tasks. The classification is based on human experts’ knowledge and also the classification in original datasets if it exists*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_FNlNH0iFOx/figures/031_Table_6.jpg]]
*Table 6: (continued from previous page)*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_FNlNH0iFOx/figures/032_Table_6.jpg]]
*Table 6: (continued from previous page)*

## 方法谱系与知识库定位

### 代码增强推理的方法谱系

R1-Code-Interpreter 处于“大语言模型 + 外部代码执行”这一研究脉络中，其核心贡献在于将交互式代码解释器与开源的强化学习训练流程深度耦合，而非仅将其作为推理时的工具调用。与现有方法相比，R1-CI 的关键区分点体现在以下几个维度：

**推理框架的演进**。传统方法主要采用两种范式：纯文本思维链推理（All Text）和单轮代码生成（All Code，即在 CoT 推理后输出代码作为最终答案）。Code Agent（CI wo Fine-tune）引入了多轮代码交互，但未经过 SFT/GRPO 微调，其代码使用决策完全依赖预训练模型的先验能力。**CodeSteer**（Chen et al., 2025）进一步引入额外的引导代理来控制代码代理的行为，但仍未涉及端到端的强化学习优化。R1-CI 在此基础上，通过 SFT 合成数据预热 + 多阶段 GRPO 训练，使模型内化了“何时使用代码、如何解读执行结果、何时进行自我验证”的决策能力，实现了从外部引导到内生能力的转变。

**训练范式的差异**。在 RL 训练层面，R1-CI 面临的核心瓶颈具有普遍性：多任务 GRPO 训练中，由于任务异质性，大量样本的正确率 $p$ 接近 0 或 1，导致策略梯度信号消失（梯度范数上界正比于 $p(1-p)$）。这一发现不仅解释了为何直接应用 GRPO 仅带来 +3.4% 的微弱提升（Figure 3d），也揭示了现有 RL 训练方法在多任务代码推理场景中的根本局限。R1-CI 提出的基于改进潜力（Improvement Potential, $\Pi_i = 4p_i(1-p_i)$）的多阶段课程学习，通过优先训练高潜力样本，将 RL 增益提升至 +9.3%，为类似的多任务 RL 训练问题提供了一种可迁移的解决方案。

### 知识库定位与技术边界

**适用场景**。R1-CI 在 144 个多样化的推理与规划任务上展现出强大的性能，覆盖符号推理（SymBench）、复杂指令遵循（BBH）和算法推理（Reasoning-Gym）三大类别。其 14B 参数模型在 37 个测试任务上达到 72.4% 的准确率，显著优于 GPT-4o 纯文本推理（58.6%）和 GPT-4o 自带 Code Interpreter（70.9%）。在分布外（OOD）任务如 GPQA Diamond 和 AIME 24&25 上也展现出良好的泛化能力（Table 4, Figure 13），表明训练框架学到的代码推理策略具有一定的任务迁移性。

**技术边界与局限**。尽管整体性能优异，R1-CI 仍存在以下适用边界：

- **基座模型依赖性**。消融实验表明，Qwen-2.5 基座模型在代码生成任务上的训练效果优于 DeepSeek 蒸馏模型（Table 5），说明框架的有效性与基座模型的代码能力强相关。对于代码生成能力较弱的基座模型，SFT 预热阶段可能无法合成足够多的高质量正确轨迹，进而影响后续 GRPO 训练的起点。
- **低潜力样本的收益递减**。多阶段课程学习中，第四阶段（$\Pi_i \in [0.64, 1.00]$，即极低改进潜力样本）几乎不带来性能提升（Figure 4），且训练奖励在合并新样本时出现明显下降。这表明对于正确率极低或极高的任务，当前框架仍缺乏有效的优化手段——这些任务可能超出了模型的基础能力边界，或已接近性能上限。
- **任务覆盖的不均衡性**。训练任务集虽覆盖多个类别，但某些能力类别（如优化类任务）可能仍样本不足，这需要在实际应用中根据目标领域进行任务策展的调整。
- **SFT 预热的必要性**。冷启动模型（仅预训练，未经过 SFT）在 GRPO 中几乎无提升（Figure 15），说明代码解释器的有效使用需要先通过监督学习建立基本的代码生成和结果解读能力，这增加了训练流程的复杂度和对高质量合成数据的依赖。

### 开放问题

1. **极端难度任务的优化策略**：对于 $p \approx 0$ 的任务（模型几乎无法正确解答），当前的改进潜力引导策略无法提供有效梯度。是否需要引入更细粒度的过程奖励或子目标分解来突破这一瓶颈？
2. **代码推理的可解释性**：模型在 GRPO 训练中涌现出代码自我验证行为（Figure 6a），但这一行为的内部机制尚不清晰——模型是真正理解了验证逻辑，还是仅学会了模仿训练数据中的验证模式？
3. **跨模型规模的缩放特性**：当前实验覆盖 3B/7B/14B 参数规模，改进潜力课程学习在更大规模模型（如 70B+）上的效果是否仍然显著，以及课程阶段的划分策略是否需要调整，仍有待验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/R1_Code_Interpreter_LLMs_Reason_with_Code_via_Supervised_and_Multi_stage_Reinforcement_Learning.pdf]]
