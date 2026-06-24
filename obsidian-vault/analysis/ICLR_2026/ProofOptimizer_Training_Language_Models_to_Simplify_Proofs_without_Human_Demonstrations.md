---
title: "ProofOptimizer: Training Language Models to Simplify Proofs without Human Demonstrations"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ProofOptimizer_Training_Language_Models_to_Simplify_Proofs_without_Human_Demonstrations.pdf
openreview_forum_id: huptrb4JTa
aliases:
- ProofOptimizer
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_dialog
core_operator: "利用Lean形式系统的可验证性提供可靠训练信号，通过专家迭代与强化学习训练专用证明简化模型，并结合推理时迭代缩短策略。"
primary_logic: "通过自动构建的证明简化数据、专家迭代和在线强化学习，可以训练出一个无需人工示例的专用证明简化语言模型，大幅压缩形式化证明长度，且优化目标（长度、心跳数）可灵活替换。"
claims:
- "ProofOptimizer集成符号化Lean Linter、7B参数语言模型和迭代推理时算法。"
- "训练同时采用专家迭代和强化学习，无需人类标注的简化数据。"
- "ProofOptimizer将miniF2F平均证明长度缩减87%，PutnamBench缩减57%，IMO 2025证明缩减超过50%。"
- "miniF2F 上 平均证明长度 = 75 (8轮迭代缩短后)"
---

# ProofOptimizer: Training Language Models to Simplify Proofs without Human Demonstrations

> [!tip] 核心洞察
> 通过自动构建的证明简化数据、专家迭代和在线强化学习，可以训练出一个无需人工示例的专用证明简化语言模型，大幅压缩形式化证明长度，且优化目标（长度、心跳数）可灵活替换。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ProofOptimizer：无需人类示例训练语言模型简化证明 |
| 英文题名 | ProofOptimizer: Training Language Models to Simplify Proofs without Human Demonstrations |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=huptrb4JTa); [GitHub](https://github.com/ByteDance-Seed/Seed-Prover/blob/17f89e327e4f90f46b0af385efc233dbbe71f8bb/SeedProver/imo2025/IMO2025/P1.lean) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_dialog |
| Method | ProofOptimizer |
| Dataset | miniF2F, PutnamBench, Seed-Prover IMO 2025, miniF2F (单样本) |

> [!tip] 效果简介
> - miniF2F 上，平均证明长度 为 75 (8轮迭代缩短后)，对比 334 (原始Goedel-Prover-V2证明)，变化 -259 (缩减 87.9%)。
> - PutnamBench 上，平均证明长度 为 811 (8轮迭代缩短后)，对比 1468 (原始Goedel-Prover-V2证明)，变化 -657 (缩减 57.2%)。
> - Seed-Prover IMO 2025 上，证明长度 为 P3: 7907, P4: 14531, P5: 4002，对比 P3: 16377, P4: 29147, P5: 8658，变化 缩减 51.7%, 50.1%, 53.8%。

## 概述

形式化证明系统（如 Lean）为数学推理提供了严格的验证环境，但由强化学习训练证明器（如 Seed-Prover、Goedel-Prover）生成的证明往往极其冗长——miniF2F 上平均 334 个 token，PutnamBench 上平均 1468 个 token，IMO 2025 证明甚至可达数万 token。这些超长证明不仅难以阅读，更严重阻碍了形式化数学的规模化应用。**核心瓶颈在于：证明简化训练数据极度稀缺，现有方法（尤其是围绕现成大语言模型的 agent 型框架）难以可靠地压缩此类证明。**

ProofOptimizer 针对这一瓶颈提出了一个无需人工示例的专用证明简化框架。其**核心洞见**是：利用 Lean 形式系统的可验证性提供可靠训练信号，通过自动构建的简化数据、专家迭代与在线强化学习，训练一个专用的 7B 参数证明简化模型，并结合推理时迭代缩短策略，实现大幅度的证明压缩。整个系统由三个组件构成：符号化 Lean Linter（去除冗余策略）、专用证明简化语言模型（7B 参数）、以及迭代式推理时缩短算法。

训练采用两种范式：专家迭代中，模型生成简化候选，由 Lean 验证后纳入训练数据进行监督微调；强化学习中，证明长度和正确性作为奖励信号，采用异步 GRPO 算法进行在线优化。推理时，系统先通过 Linter 预处理，再反复采样多个候选简化并取最短有效结果，迭代直至收敛，并可选配测试时 RL 进一步压缩。

实验结果表明，ProofOptimizer 在三个基准上实现了显著的证明压缩：miniF2F 平均证明长度从 334 降至 75（缩减 87.9%），PutnamBench 从 1468 降至 811（缩减 57.2%），Seed-Prover 的 IMO 2025 证明长度缩减超过 50%。单样本简化（red@1）在 miniF2F 上达到 63.6%，远超通用大语言模型基线 Gemini-2.5-Pro 的 24.3%。

**关键局限**包括：RL 训练导致生成多样性显著下降（red@32 增益有限）；基于执行反馈的修复机制常产生更长证明，整体收益较低；以证明长度为唯一优化目标时可能生成执行缓慢的证明。这些局限性指明了未来改进方向，包括联合优化长度与执行效率、缓解 RL 多样性崩溃等。

## 背景与动机

形式化定理证明近年来取得了显著进展，基于强化学习（RL）训练的证明器（如Goedel-Prover、Seed-Prover）已能生成日益复杂的形式化证明。然而，这些证明器输出的证明往往极其冗长——例如，Seed-Prover为IMO 2025问题生成的证明可达数万token——严重阻碍了人类审阅、教学应用和证明库维护。

**核心瓶颈**在于：证明简化训练数据极度稀缺。现有方法主要依赖现成大语言模型（如GPT-4o）的agent型框架（如ImProver），通过脚手架式多轮交互来压缩证明。但这类方法存在两个根本缺陷：一是无法处理RL证明器产生的超长形式化证明，因为通用LLM的上下文窗口和推理能力难以胜任；二是依赖闭源API，无法进行针对性微调，且成本高昂。

**关键洞察**：Lean形式系统提供了可验证性——任何简化后的证明都可以被编译器精确验证其正确性。这一特性使得无需人类标注即可自动构建训练数据，并利用验证结果作为可靠的训练信号。基于此，ProofOptimizer提出了一条完全不同的路径：训练一个专用的证明简化语言模型，通过专家迭代（expert iteration）和在线强化学习，在合成数据上学会压缩证明，而无需任何人类简化示例。其优化目标——证明长度或执行心跳数——可灵活替换，适应不同场景需求。

实验表明，该思路具备显著的压缩潜力：ProofOptimizer将miniF2F上的平均证明长度从334 token缩减至75 token（87.9%），PutnamBench从1468 token缩减至811 token（57.2%），Seed-Prover的IMO 2025证明也缩减超过50%。

## 核心创新

ProofOptimizer 的核心创新在于将证明简化从依赖通用大模型的 agent 型框架，转向一个由形式化验证驱动的专用训练范式。这一转变通过三个关键 changed slots 实现。

**训练范式：从 agent 脚手架到专家迭代与在线强化学习。** 现有方法（如 ImProver）依赖现成 LLM（如 GPT-4o）的 API 进行证明简化，受限于模型能力且无法针对简化目标进行专门优化。ProofOptimizer 直接在 7B 参数模型上执行专家迭代和在线 GRPO 强化学习，训练信号完全由 Lean 编译器提供：专家迭代中，模型生成简化候选，由 Lean 验证正确性后纳入监督微调数据；强化学习中，奖励函数 $R(x, y) = \frac{|x| - |y|}{|x|}$ 仅在 $y$ 有效且不长于 $x$ 时给予相对缩短比例作为奖励，否则为 0。这一设计使训练无需任何人工标注的简化示例，从根本上解决了证明简化训练数据稀缺的瓶颈。

**复杂度度量：从单一证明长度到任意可计算指标。** 此前方法仅以证明长度（token 数）为优化目标。ProofOptimizer 将优化目标推广为任意可计算复杂度度量 $\mathcal{L}(x)$，在 $\tilde{p}^* = \underset{x \text{ proves } s}{\arg\min} \mathcal{L}(x)$ 框架下，支持将 $\mathcal{L}$ 替换为 Lean 心跳数等执行效率指标。实验表明，以心跳数为目标优化出的证明执行更快，同时仍实现可观的长度缩短，体现了优化目标的灵活替换能力。

**推理时策略：从单次采样到符号化预处理 + 迭代缩短 + 测试时 RL。** 基线方法通常只做单次或简单多次采样简化。ProofOptimizer 构建了三阶段推理管线：首先利用 Lean 的 `unusedTactic` linter 进行符号化代码检查，自动去除冗余策略完成预处理；随后执行迭代式证明缩短，每轮对当前最短证明采样多个候选简化，取最短有效结果，迭代直至收敛；最后可选地在评估集上继续执行在线 RL 微调（测试时 RL），进一步压缩证明长度。这一管线将 miniF2F 平均证明长度从 334 压缩至 75（缩减 87.9%），PutnamBench 从 1468 压缩至 811（缩减 57.2%），Seed-Prover 的 IMO 2025 证明缩减超过 50%。

三个 changed slots 的协同效应是 ProofOptimizer 取得显著压缩率的因果机制：形式化验证提供可靠训练信号，使专用模型摆脱对通用 LLM 的依赖；灵活的复杂度度量使优化目标可适配不同场景；多阶段推理管线则通过符号化预处理降低模型负担、迭代探索扩大搜索空间、测试时 RL 进一步压榨性能，形成从训练到推理的完整闭环。

## 整体框架

ProofOptimizer 的整体设计围绕一个核心洞察展开：形式化证明的可验证性（通过 Lean 编译器）可以作为可靠的训练信号，驱动一个专用语言模型学会简化证明，无需任何人工标注的简化示例。整个系统由三条正交但协同工作的管线构成，分别对应预处理、训练与推理时优化。

**输入**是任意来源的形式化证明（例如由 RL 训练的证明器如 Goedel-Prover-V2 或 Seed-Prover 生成的长证明），**输出**是经过多重压缩、仍通过 Lean 验证的有效证明。系统并不修改证明所陈述的定理本身，仅对证明脚本进行简化。

**三条管线的分工如下：**

1. **符号化预处理（Lean Linter）**：在模型介入之前，利用 Lean 的 `unusedTactic` linter 静态分析证明脚本，识别并删除对证明结论无贡献的冗余策略步骤。这一步是确定性的、零成本的，能初步缩短证明长度，为后续模型简化提供更干净的起点。

2. **训练时管线（专家迭代与在线强化学习）**：核心是一个 7B 参数的语言模型，在自动构建的证明简化数据集上训练。训练采用两种互补范式：
   - **专家迭代（Expert Iteration）**：模型对当前训练集中的证明采样多个简化候选，由 Lean 编译器筛选出最短的有效简化，将其加入下一轮监督微调的训练数据。这一过程迭代进行，逐步提升模型的多候选简化能力。
   - **在线强化学习（Online RL）**：采用异步 GRPO 算法，以证明长度的相对缩短比例作为奖励信号 $R(x, y) = \frac{|x| - |y|}{|x|}$（若 $y$ 有效且不长于 $x$，否则为 0），优势函数 $A_i = R_i - \frac{1}{k} \sum_{j<k} R_j$ 以 $k=8$ 个样本的平均奖励为基线。RL 训练显著提升单样本简化效果，但会牺牲生成多样性。

3. **推理时管线（迭代式证明缩短与测试时 RL）**：在评估阶段，对当前最短证明反复采样多个候选简化（典型配置为 6 轮每轮 64 次采样，随后 2 轮每轮 1024 次采样），取最短有效结果作为下一轮输入，迭代直到收敛。此外，可在评估集上继续执行在线 RL 微调（测试时 RL），进一步压缩证明长度。

**模块间的数据流**：原始证明首先经过 linter 预处理，然后送入训练后的简化模型。训练阶段，专家迭代和 RL 共享同一基础模型，但产生不同特性的变体（ProofOptimizer-ExpIt 擅长多候选场景，ProofOptimizer-RL 擅长单样本场景）。推理时，迭代缩短算法将模型的单次简化能力放大为渐进式压缩，测试时 RL 则直接在目标分布上调整模型参数。

该框架的一个关键特性是**复杂度度量的可替换性**：虽然默认优化目标是证明长度（token 数），但 $\mathcal{L}(x)$ 可替换为任意可计算度量，例如 Lean 心跳数（heartbeats），使得优化目标可以灵活地在简洁性与执行效率之间切换。

## 核心模块与公式推导

### 问题形式化

ProofOptimizer 将证明简化定义为一个可验证的优化问题。设 $s$ 为待证明的命题，$p$ 为已存在的形式化证明，$\mathcal{L}(x)$ 为任意可计算的复杂度度量（如证明长度或 Lean 心跳数）。证明简化的目标是在保持证明有效性的前提下最小化复杂度：

$$\tilde{p}^* = \underset{x \text{ proves } s}{\arg\min} \mathcal{L}(x)$$

这一形式化的关键特性在于 $\mathcal{L}$ 的灵活性——论文中主要使用证明长度（token 数），但实验表明该框架可直接替换为心跳数等执行开销指标，无需改动训练流程。

### 评估指标

为量化简化效果，论文定义了两个核心指标。给定原始证明 $p$ 和 $k$ 个候选简化 $\{y_i\}_{i=1}^k$，设 $l_i = |y_i|$ 为各候选的长度：

$$\min@k \triangleq \min_i \{ l_i \}$$

$$\text{red@k} \triangleq \max_i \left\{ \frac{|p| - l_i}{|p|} \right\} = 1 - \frac{\min@k}{|p|}$$

$\min@k$ 衡量 $k$ 次采样能获得的最短证明长度，$\text{red@k}$ 衡量相对原始证明的最大缩减比例。这两个指标分别反映模型的压缩能力和采样多样性——$\text{red@1}$ 主要受单样本质量影响，而 $\text{red@32}$ 同时依赖生成多样性。

### 系统架构三模块

ProofOptimizer 由三个协同组件构成：

1. **符号化 Lean Linter**：预处理模块，利用 Lean 编译器的 `unusedTactic` linter 自动识别并移除冗余策略。该步骤完全基于符号规则，不涉及语言模型，可零成本初步缩短证明。

2. **证明简化语言模型**：7B 参数规模，通过专家迭代或在线强化学习在合成数据上训练，是系统的核心决策模块。模型接收原始证明作为输入，输出简化后的证明。

3. **迭代式证明缩短算法**：推理时策略，对当前最短证明反复采样多个候选简化，取最短有效结果，迭代直到收敛。该算法将单次简化的收益通过多轮叠加放大。

### 训练范式

系统支持两种互补的训练范式，均利用 Lean 编译器的可验证性提供训练信号，无需人工标注的简化示例。

**专家迭代** 采用三步循环：对训练集中的每个证明 $x$，使用当前模型采样 4 个候选简化；通过 Lean 编译器筛选出最短的正确简化；将筛选后的数据加入训练集进行监督微调。迭代过程中设置长度约束（新证明长度 $\leq$ 原证明的 80%），确保训练数据质量。

**在线强化学习** 使用异步 GRPO 算法。奖励函数定义为相对缩短比例：

$$R(x, y) = \frac{|x| - |y|}{|x|}$$

其中 $y$ 必须通过 Lean 验证且 $|y| \leq |x|$，否则奖励为 0。优势函数以 $k=8$ 个样本的平均奖励为基线：

$$A_i = R_i - \frac{1}{k} \sum_{j<k} R_j$$

该设计不使用标准差归一化，直接以组内均值作为基线计算优势。

## 实验与分析

### 核心结果：证明长度的大幅压缩

ProofOptimizer 对由 RL 训练证明器生成的超长形式化证明表现出极强的压缩能力。在 miniF2F 基准上，原始 Goedel-Prover-V2 证明的平均长度为 334 tokens，经过 8 轮迭代缩短后降至 **75 tokens**，缩减幅度达 **87.9%**；在 PutnamBench 上，平均长度从 1468 降至 **811 tokens**，缩减 **57.2%**（Table 5, Figure 4 左图）。这一差异与两个数据集的证明长度分布直接相关：PutnamBench 证明的中位数和最大值均远高于 miniF2F（Table 10），表明当前模型对极长证明的压缩率仍有提升空间。

![[assets/figures/papers/iclr26_0012_huptrb4JTa_ProofOptimizer_Training_Language_Models_to_Simpl/figures/015_Figure_4.jpg]]
*Figure 4: Iterative Shortening: per-iteration improvement (left) and effect of proof length (right)*

![[assets/figures/papers/iclr26_0012_huptrb4JTa_ProofOptimizer_Training_Language_Models_to_Simpl/figures/034_Table_5.jpg]]
*Table 5: Min@64 (rounded to nearest integer) and reduction (%) of miniF2F and PutnamBench proofs across inference-time iterations. Iterations 1 − 6 are done with 64 samples, and 7 − 8 with 1024 samples*

对于更具挑战性的 IMO 2025 证明（由 Seed-Prover 生成），ProofOptimizer 同样将 P3、P4、P5 的证明长度分别从 16377、29147、8658 压缩至 7907、14531、4002，缩减率分别为 **51.7%、50.1%、53.8%**（Table 3）。值得注意的是，P1 的长度从 1040 降至 582（缩减 44.0%），绝对压缩量虽小，但相对比例仍可观。

![[assets/figures/papers/iclr26_0012_huptrb4JTa_ProofOptimizer_Training_Language_Models_to_Simpl/figures/016_Table_3.jpg]]
*Table 3: Iterative shortening achieves significant reduction for Seed-Prover’s IMO 2025 proofs*

在单样本设定下，ProofOptimizer-RL 的 Red@1 达到 **63.6%**（miniF2F），远超通用模型 Gemini-2.5-Pro 的 24.3%（Table 1），说明专用简化模型的即时输出质量显著优于现成 LLM 的提示工程方案。

![[assets/figures/papers/iclr26_0012_huptrb4JTa_ProofOptimizer_Training_Language_Models_to_Simpl/figures/002_Table_1.jpg]]
*Table 1: Min@k and Red@k throughout expert iteration and online RL. Our RL model has strong @1 results, while our ExpIt model has strong @32 results. RL metrics are Gaussian-smoothed*

### 训练范式的取舍：专家迭代 vs. 在线强化学习

Table 1 揭示了两种训练范式在单样本与多样本性能上的根本性分歧：

- **专家迭代（ProofOptimizer-ExpIt）** 在多样本场景下表现最佳：Red@32 达到 74.1%（miniF2F），Min@32 为 112。这表明 ExpIt 保持了较高的生成多样性，允许通过多次采样找到更短的证明。
- **在线 RL（ProofOptimizer-RL）** 在单样本场景下占优：Red@1 高达 63.6%，Min@1 仅 190（vs. ExpIt 的 241）。但 Red@32 仅微增至 74.0%，与 ExpIt 的 74.1% 几乎持平。

这一现象的根本原因在于 **GRPO 算法以牺牲多样性为代价优化 Red@1**。Figure 9 清晰显示，随着 RL 训练推进，Red@1 持续上升，而 Red@32 的增长几乎停滞。RL 训练中模型逐渐收敛到少数高奖励策略，丧失了探索多样化简化路径的能力。这一多样性崩溃（diversity collapse）在 PutnamBench 上表现为训练曲线的剧烈振荡（Figure 2b），暗示 RL 在该数据集上的优化过程不稳定。

![[assets/figures/papers/iclr26_0012_huptrb4JTa_ProofOptimizer_Training_Language_Models_to_Simpl/figures/033_Figure_9.jpg]]
*Figure 9: Reduction metrics @1 and @32 over the course of RL. GRPO maximizes red@1 at the cost of diversity, as red@32 only marginally increases in comparison*

测试时 RL（Test-Time RL）进一步将 Min@1 从 190 压至 **160**，Red@1 提升至 **72.5%**（Table 1），但同样未能改善 Red@32，证实了多样性退化是 RL 训练范式的内在特性，而非训练不充分所致。

### 迭代缩短的边际收益与采样规模效应

迭代式证明缩短（Iterative Proof Shortening）是推理时压缩的关键机制。Figure 4 左图显示，miniF2F 和 PutnamBench 的平均证明长度随迭代轮次单调递减，但边际收益逐渐衰减。前 6 轮使用每轮 64 次采样，第 7-8 轮将采样数提升至 1024 后，miniF2F 的 Min@64 从 78 进一步降至 75，PutnamBench 从 825 降至 811（Table 5），表明 **增加采样规模可带来对数线性增益**。

Table 6 和 Figure 10 量化了这一效应：在初始简化阶段，采样数从 1 增至 1024 时，miniF2F 的 Min@k 从 142 降至 110，Red@k 从 77.1% 升至 82.4%。增益曲线呈对数线性趋势，意味着通过暴力采样获取更短证明的成本效益逐渐降低。

### 执行反馈修复的低效性

执行反馈修复（execution-based repair）是理论上吸引人的补充策略：当简化候选未通过 Lean 验证时，调用 Goedel-Prover-V2-32B 尝试修复。然而实验结果揭示了这一策略的根本性缺陷。

Table 2 的逐步成功率分析表明，修复是流水线的主要瓶颈：miniF2F 上简化成功率为 62.2%（2840/4564），而修复后的最终有效证明率仅 4.8%（221/4564）；PutnamBench 上修复后有效证明率更低至 **1.8%**（24/1332）。Figure 3 进一步揭示了原因：**修复后的证明通常比原始证明更长**。在 PutnamBench 上，修复成功的证明中绝大多数长度超过了修复前的原始证明，使得修复机制在实际压缩效果上几乎无贡献。

Table 9 的完整对比证实了这一结论：添加修复后，miniF2F 的 Red@64×2 从 77.3% 微升至 77.3%（无变化），PutnamBench 从 35.3% 微升至 35.3%。修复策略未能带来实质性增益，反而增加了计算开销。

### 复杂度度量的可替换性：从证明长度到心跳数

ProofOptimizer 的优化目标 $\mathcal{L}(x)$ 不仅限于证明长度。当将 $\mathcal{L}$ 替换为 Lean 心跳数（heartbeats，反映执行成本）时，模型能有效优化执行效率。Table 11 显示，心跳优化在 miniF2F 上实现了 **57.0%** 的心跳缩减（从 24.2K 降至 10.4K），同时仍将证明长度从 334 降至 104（68.9% 缩减）；在 PutnamBench 上心跳缩减达 **45.5%**，长度缩减 37.5%。

![[assets/figures/papers/iclr26_0012_huptrb4JTa_ProofOptimizer_Training_Language_Models_to_Simpl/figures/055_Table_11.jpg]]
*Table 11: Comparison of Min@64 (rounded to nearest integer), reduction (%), Heartbeats@64 (in thousands), and reduction (%) across inference-time iterations for miniF2F and PutnamBench proofs. Iterations 1–6 use 64 samples, and 7–8 use 1024 samples. The first group shows the standard (length-optimized) setting; the second group shows the new (heartbeat-optimized) experiment*

Figure 7 提供了更细粒度的视角：50/75 个 PutnamBench 证明的执行时间获得了超过 10% 的加速。但需注意，部分简化证明的执行时间反而大幅增加（例如从 0.9s 增至 10.8s，或 4.9s 增至 74.6s）。这通常发生在模型用蛮力遍历（如区间分情况讨论）替代高效算法时，表明 **长度优化与执行效率优化之间存在张力**，单一度量优化可能损害另一维度。

### 消融：各组件贡献与基线对比

Table 4 对比了不同模型的证明草图（proof sketching）能力，ProofOptimizer 的 7B 模型在 compile@1 上达到 54.8%，显著优于 Qwen2.5-32B 的单样本基线（34.6%），说明专用训练对证明结构化理解有实质提升。

Figure 12 的定性对比显示，ProofOptimizer 生成的简化证明（绿色）在结构简洁性上明显优于 Gemini 2.5 Pro（黄色），后者倾向于保留更多冗余步骤。这与 Table 1 中 ProofOptimizer-RL 的 Red@1（63.6%）远超 Gemini-2.5-Pro（24.3%）的定量结果一致。

### 失败模式与局限性

1. **RL 多样性崩溃**：Red@32 几乎不随 RL 训练增长，模型丧失探索多样化简化策略的能力，在需要多角度尝试的复杂证明上可能受限。
2. **修复机制低效**：执行反馈修复产生的证明通常长于原始证明（Figure 3），导致修复流水线整体收益极低（Table 2）。
3. **长度-效率冲突**：以证明长度为目标时，可能生成记号短但执行慢的证明（如蛮力遍历），心跳优化虽能缓解此问题，但无法完全消除劣化案例。
4. **泛化边界未充分验证**：当前仅在 7B 模型和三个评估集上验证，对更大规模数学库或更长证明的泛化性能尚不明确。
5. **Lean 生态依赖**：整个工作流深度绑定 Lean 形式系统，无法直接迁移至 Coq、Isabelle 等其他证明助手。

## 方法谱系与知识库定位

### 与现有方法的关系

ProofOptimizer 处于形式化证明简化这一新兴方向的早期位置，其工作模式与现有方法存在明确的继承与分化关系。

**上游依赖：证明生成模型。** ProofOptimizer 不生成原始证明，而是作为后处理模块作用于已有证明。论文使用的输入证明来自 Goedel-Prover-V2-32B（miniF2F 和 PutnamBench）以及 Seed-Prover（IMO 2025），两者均为经过强化学习训练的形式化证明器。这种"生成-简化"解耦设计使得 ProofOptimizer 可以独立于证明生成器进行训练和评估，但也意味着其简化效果的上限受限于输入证明的质量——如果原始证明本身已接近最优，简化空间自然缩小。

**与 agent 型框架的对比：ImProver（Ahuja et al., 2024）。** ImProver 是直接可比的证明长度优化方法，其核心思路是利用现成大语言模型（如 GPT-4o）的 API，通过 agent 型脚手架进行证明简化。ProofOptimizer 与之的关键差异在于：(1) 训练范式——ProofOptimizer 使用 7B 参数模型进行专家迭代和在线强化学习，由 Lean 编译器提供验证与奖励信号，而非依赖闭源 API 的黑箱推理；(2) 复杂度度量——ProofOptimizer 将优化目标推广至任意可计算度量（证明长度和 Lean 心跳数均可替换），而 ImProver 仅关注 token 数；(3) 推理时策略——ProofOptimizer 引入符号化 linter 预处理和迭代式证明缩短，而 ImProver 采用单次采样或简单多次采样。在单样本简化指标（Red@1）上，ProofOptimizer-RL 达到 63.6%，远超 Gemini-2.5-Pro 的 24.3%，表明专用小模型的训练范式在精确简化任务上显著优于通用大模型的零样本/少样本推理。

**与通用大语言模型的关系：Gemini-2.5-Pro。** 论文将 Gemini-2.5-Pro 作为通用大语言模型基线，直接用于证明简化。实验结果表明，即使是最先进的通用模型，在形式化证明简化这一高度专业化任务上的表现也远不及经过针对性训练的 7B 模型。这验证了论文的核心主张：形式系统的可验证性使得专用小模型可以通过自动构建的训练数据获得超越通用大模型的领域能力。

### 适用边界与泛化条件

**形式系统依赖。** ProofOptimizer 的工作流深度依赖 Lean 形式环境：符号化 linter 使用 Lean 的 `unusedTactic` 检查器，训练信号完全由 Lean 编译器提供，推理时验证同样依赖 Lean。这意味着该方法无法直接迁移到其他证明助手（如 Coq、Isabelle）或编程语言环境。对于 Lean 生态之外的应用场景，需要重新构建等价的验证和反馈机制。

**模型规模与数据规模。** 当前验证仅在 7B 参数模型上进行，训练数据来自 Goedel-Pset-v1-Solved 数据集。论文未探索模型规模（如扩展到 32B 或更大）对简化效果的影响，也未验证在更大规模数学库（如 Mathlib 全库）上的泛化性能。对于更长、更复杂的证明（如数千行的大型定理证明），迭代缩短的计算开销和收敛行为尚不明确。

**证明类型偏好。** 从实验结果看，ProofOptimizer 对 RL 训练证明器生成的"超长"证明效果最为显著——miniF2F 上缩减 87.9% 的极端效果部分源于原始证明（平均 334 tokens）本身存在大量冗余。对于已经经过人工精炼的简洁证明，简化空间可能大幅缩小。论文未在人工编写的规范证明上评估该方法。

### 已知局限

**RL 训练的多样性崩溃。** 在线 GRPO 训练显著提升了单样本简化效果（Red@1 从 49.0% 升至 63.6%），但 Red@32 几乎不再增长（Figure 9, Table 1）。这表明 RL 优化使模型收敛到少数高奖励策略，丧失了生成多样化候选简化的能力。在需要多轮迭代缩短或探索非贪婪简化路径的场景下，这种多样性退化可能限制最终的压缩上限。论文未深入分析多样性崩溃的深层机制，也未提出缓解策略。

**执行反馈修复的低效性。** 论文尝试对不正确的简化候选进行执行反馈修复（repair），但修复后的证明经常比原始证明更长——修复后仅 4.8%（miniF2F）和 1.8%（PutnamBench）的证明短于之前的最短证明（Table 2, Figure 3）。这意味着修复机制在实际收益上几乎可以忽略，且引入了额外的计算开销。修复失败的主要原因可能是修复模型（Goedel-Prover-V2-32B）倾向于通过添加冗余步骤来确保正确性，而非进行真正的结构简化。

**长度优化与执行效率的冲突。** 当优化目标仅为证明长度时，模型可能生成记号短但执行慢的证明。论文报告了若干案例：简化后证明的执行时间从 0.9 秒增至 10.8 秒，或从 4.9 秒增至 74.6 秒。这通常是因为简化模型用蛮力遍历（如穷举区间情况）替代了高效算法，虽然减少了代码行数，但大幅增加了 Lean 内核的计算负担。将优化目标替换为心跳数（heartbeats）可以缓解此问题（Figure 7, Table 11），但心跳数优化与长度优化之间存在权衡，联合优化策略尚未被探索。

### 开放问题

1. **多样性保持机制。** RL 训练导致 Red@32 几乎不增长，是否存在训练策略（如熵正则化、种群训练、约束策略空间）可以在保持 Red@1 竞争力的同时恢复生成多样性？

2. **修复策略的重新设计。** 当前基于 Goedel-Prover 的修复几乎无正面收益。是否可以通过训练专用的修复模型、引入长度惩罚的修复目标、或使用更精确的错误定位来使修复机制变得有效？

3. **多目标优化。** 证明长度和心跳数分别对应简洁性和执行效率，两者之间存在非平凡权衡。如何设计联合奖励函数或帕累托优化策略，在可读性和执行速度之间取得可控折衷？

4. **劣化检测与预防。** 为什么某些简化证明的执行时间会激增（如 4.9s → 74.6s）？是否可以在推理时加入心跳数阈值过滤，自动拒绝执行效率严重劣化的简化候选？

5. **跨形式系统迁移。** 当前方法深度绑定 Lean。将"可验证性驱动的专家迭代 + RL"范式迁移到其他形式系统（如 Coq、Isabelle）需要哪些最小适配工作？Lean 的 `unusedTactic` linter 在其他系统中是否有等价工具？

6. **专家迭代的长度约束优化。** 训练中设定的约束（新证明长度 ≤ 原证明的 80%）是否是最优的？更宽松的约束可能增加训练数据量但降低数据质量，更严格的约束则相反。该超参数对最终模型性能的敏感性未被系统研究。

## 原文 PDF

![[paperPDFs/ICLR_2026/ProofOptimizer_Training_Language_Models_to_Simplify_Proofs_without_Human_Demonstrations.pdf]]
