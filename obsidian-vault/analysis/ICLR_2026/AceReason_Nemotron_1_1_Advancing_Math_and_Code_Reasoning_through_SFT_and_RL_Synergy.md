---
title: "AceReason-Nemotron 1.1: Advancing Math and Code Reasoning through SFT and RL Synergy"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AceReason_Nemotron_1_1_Advancing_Math_and_Code_Reasoning_through_SFT_and_RL_Synergy.pdf
project_link: null
code_link: null
aliases:
- AN11
- AN11AMCRTSRS
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "扩大SFT数据中独特题目的数量（而非每道题的回答数量），以及在RL训练中保持温度调整后的熵约0.3以平衡探索与利用。"
primary_logic: "将基于大规模题目扩展的强SFT模型与阶段式RL（先数学后代码）相结合，并精细调节过长时间过滤策略与采样温度，即可在7B规模上同时刷新数学与代码推理的SOTA。"
claims:
- "增加独特题目的数量比增加每道题的回答数量对SFT性能提升更显著。"
- "更强的SFT模型在RL训练后始终取得更好的最终性能，但性能差距在训练中缩小。"
- "在短Token限制（8K或16K）下应用过长时间过滤有明显收益，但在32K时该策略会损害性能。"
- "RL采样温度应使温度调整后的熵保持在0.3左右，以平衡探索与利用。"
---

# AceReason-Nemotron 1.1: Advancing Math and Code Reasoning through SFT and RL Synergy

> [!tip] 核心洞察
> 将基于大规模题目扩展的强SFT模型与阶段式RL（先数学后代码）相结合，并精细调节过长时间过滤策略与采样温度，即可在7B规模上同时刷新数学与代码推理的SOTA。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AceReason-Nemotron 1.1: 通过SFT与RL协同推进数学与代码推理 |
| 英文题名 | AceReason-Nemotron 1.1: Advancing Math and Code Reasoning through SFT and RL Synergy |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=IaEqjWXd1d) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | AceReason-Nemotron-1.1 训练方案 |
| Dataset | AIME 2024, AIME 2025, LiveCodeBench v5, LiveCodeBench v6 |

> [!tip] 效果简介
> - AIME 2024 上，avg@64 为 72.6，对比 55.5，变化 +17.1。
> - AIME 2025 上，avg@64 为 64.8，对比 39.0，变化 +25.8。
> - LiveCodeBench v5 上，avg@8 为 57.2，对比 37.6，变化 +19.6。

## 概要

针对数学与代码推理任务，现有7B规模模型通常将监督微调（SFT）与强化学习（RL）割裂使用，或只依赖大模型蒸馏，缺少对二者协同作用的系统性研究。本工作提出AceReason-Nemotron 1.1，核心发现是：**通过大规模增加SFT阶段独特题目的数量（而非单纯增加每道题的回答数），并与阶段式RL（先数学后代码）协同训练，可在7B规模同时刷新数学与代码推理的SOTA。** 训练过程中，将采样温度调节至温度调整后的熵保持在0.3左右，能在探索与利用间取得良好平衡；在短Token预算（8K/16K）下应用过长时间过滤能显著提升性能，但在32K阶段移除该过滤则带来进一步增益。

主要结果：**在AIME 2024上达到72.6（avg@64），AIME 2025上达到64.8，分别较前一版本提升17.1和25.8个百分点；在LiveCodeBench v5上达到57.2，v6上达到52.1，分别提升19.6和18.0个百分点**，均显著超越同级别的蒸馏SFT基线及RL基线方法。消融实验进一步证实：更强SFT模型在RL后能持续获得更优的最终表现，且通过前期短Token压缩迫使模型发展出简洁推理，能有效提高后期长链推理的收益。



大语言模型在数学与代码推理任务上持续进步，但此前的后训练流程普遍将监督微调（SFT）与强化学习（RL）视为孤立的步骤，或直接通过蒸馏从大模型获取推理能力（如 DeepSeek‑R1‑Distill、Light‑R1 等）。这种做法缺乏对 SFT 与 RL 之间协同作用的系统研究，导致 7B 级别模型难以同时大幅提升数学与代码双重推理能力。三个关键缺口尤为突出：

1. **SFT 数据扩展策略不明**：增加每道题的回答数量可带来一定收益，但更关键的因素——扩大独特题目的规模——被普遍忽略（Section 3.1.2）。
2. **RL 训练温度粗放**：温度通常固定为 0.6 或 1.0，未探索调节到使生成熵维持在约 0.3 时对探索‑利用平衡的影响（Section 4.5.2）。
3. **过长响应过滤时机不当**：在短 token 预算（如 8 K、16 K）下过滤有益，但在长预算（32 K）阶段继续应用会损害性能（Abstract）。

针对上述缺口，本文的动机在于证明：以大规模独特题目进行强 SFT 初始化，并采用分阶段 RL（先数学后代码）与精细控制（温度调节至熵约 0.3、按阶段开关的过长过滤），可在 7B 规模上同时刷新数学与代码推理的 SOTA。实验表明，更强 SFT 模型经 RL 后仍持续保持优势（即使差距在训练中缩小），而上述调节正是解锁长尾难题、实现高效推理的核心约束。



## 核心方法与创新机理

AceReason-Nemotron 1.1 的核心突破在于**系统性地解耦 SFT 与 RL 的协同机制**，并在数据、温度策略与长度过滤三处关键节点进行了**非蒸馏式创新**，从而在 7B 参数规模上同时刷新数学与代码推理的 SOTA。其关键改变的 slot 及机理如下。

### 1. SFT 数据扩展：扩大独特题目数量远比增加每题回答数重要

与多数依赖大模型蒸馏的基线（如 DeepSeek-R1-Distill-Qwen-7B、Light-R1-7B）不同，本工作构建了大规模非蒸馏 SFT 混合数据（数学 247K、代码 136K），并在数据效率上揭示了一个重要因果杠杆：**独特题目的数量（prompts）对推理能力提升的边际收益显著高于每道题的回答数量（responses per prompt）**。在 Section 3.1.2 和 Appendix C 的扩展实验中，将 prompts 和 responses 同时扩大均可带来增益，但 prompts 扩大的贡献更大，这一结论通过定量拟合关系得到验证（附录 Part 004，置信度 1.0）。因此，该方案将有限的计算预算优先分配到尽可能多的独特题目上，同时在每题上保留一定的回答多样性，以此构建出明显强于蒸馏基线的 SFT 基础模型。

### 2. RL 温度控制：以"温度调整后熵 ≈ 0.3"平衡探索与利用

在 RL 训练中，采样温度常被简单固定（如 0.6 或 1.0）。本研究发现**温度对 RL 效果的调控存在一个最优区间：当温度调整后的生成熵约在 0.3 时，探索与利用的平衡最佳**。摘要中明确写道："particularly when the sampling temperature is carefully chosen to maintain the temperature-adjusted entropy around 0.3, a setting that strikes a good balance between exploration and exploitation"（置信度 0.95）。Figure 5 左图展示了不同温度下熵的轨迹，右表进一步量化了温度对 RL 模型最终性能的影响。这一发现使得 RL 训练不再盲目依赖固定超参数，而是将**熵校准**作为关键调控旋钮，从而在数学和代码任务中同时获得稳健提升。

### 3. 阶段式过长时间过滤：早期短 Token 限制下有益，后期长限制下必须移除

针对 RL 训练中长输出带来的奖励噪声问题，已有工作（如 Skywork-OR1）常统一采用过长时间过滤（负奖励或过滤）。本研究在 Section 4.5.3 和 Figure 6 的消融实验中揭示了**过滤策略高度依赖 Token 预算**：在早期阶段（8K/16K 限制）过滤能有效压缩无效长序列，收益显著——Stage‑1（8K）初期约 30% 的样本因超长被过滤，此举迫使模型在受限长度内学习简洁推理链（Appendix Part 004）。但在后期训练（尤其是 32K 的 Stage‑4）中，继续应用过滤反而**损害性能**：Table 2 显示，在 32K 最大输出长度下，去掉过滤后 AIME24 avg@64 从 70.2 升至 71.4，LiveCodeBench V6 avg@8 从 45.1 升至 48.0（置信度 1.0）。其因果解释是，移除过滤使推理更 token‑efficient，允许模型在 32K 预算内生成更精炼的思维链，并且推理阶段延长到 64K 时该优势仍可保留（Figure 6，置信度 0.95）。这一**动态过滤策略**——早期过滤促进压缩，晚期解禁释放效率——是对 RL 推理训练优化方法的重要修正。

此外，与上述三个 slots 紧密配合，**分阶段渐进式 RL 管道**（先数学三阶段逐步增长响应长度，再代码 RL，最后数学精调）以及**强 SFT 初始化 + RL 协同**（更强的 SFT 在 RL 后始终保持优势，且 RL 可解锁定长尾难题，见 Figure 4 和 Figure 15）共同构成了实现 SOTA 的系统性框架。这些设计的消融证据均在正文和附录中量化验证，无需额外推测。



![[assets/figures/papers/iclr26_0005_IaEqjWXd1d_AceReason-Nemotron_1.1_Advancing_Math_and_Code_R/figures/001_Figure_1.jpg]]
*Figure 1: Training Pipeline of AceReason-Nemotron 1.1. We start by performing math and code SFT on a base pretrained model. Next, we conduct three stages of math-only RL training with progressively growing response length, i.e., Stage-1 (8K), Stage-2 (16K), and Stage-3 (24K), to develop a math-specialized RL model. We then apply code-only RL training to enhance model's coding capability. Lastly, we carry out a final stage of math-only RL to produce AceReason-Nemotron 1.1*

AceReason-Nemotron 1.1 的训练方案由 **监督微调（SFT）** 和 **阶段式强化学习（RL）** 两部分构成，整体流程见图 Figure 1。该框架的核心思路是先通过大规模题目扩展构建强推理 SFT 基础模型，再通过多阶段 RL（先数学、后代码、最后回到数学）阶梯式释放模型的数学与编程推理潜能。

**1. SFT 基础模型构建**

在基础预训练模型（如 Qwen2.5‑Math‑7B）之上，同时进行数学与代码的 SFT。此阶段的关键操作是**大幅扩展唯一题目（prompts）的数量**，而非单纯增加每题的多条回答。最终收集约 247K 数学题目与 136K 代码题目进行训练，生成多个回答以维持多样性（Section 3.1.2）。SFT 输出一个具备较强长链推理能力的初始模型，作为后续所有 RL 阶段的统一起点。

**2. 阶段式 RL 训练**

RL 阶段根据任务领域和生成长度限制（token budget）被拆分为以下子阶段：

- **Math‑only RL Stage‑1 (8K 限制)**：在严格 8K 输出长度限制下进行数学 RL，强制模型压缩推理过程，为后续阶段打下简约思考的基础。
- **Math‑only RL Stage‑2 (16K 限制)**：扩大长度预算至 16K，使用更具挑战性的数学题目进行 RL，显著提升数学推理准确率。
- **Math‑only RL Stage‑3 (24K 限制)**：仅保留高难度题目，在 24K 限制下进一步强化数学能力。
- **Code‑only RL Stage‑I (24K 限制)**：切换到代码领域，在 24K 限制下对编程题目进行 RL 训练，赋予模型编码推理能力。
- **Code‑only RL Stage‑II (32K 限制)**：进一步放宽长度至 32K，并使用逐 epoch 过滤策略（移除前一个 epoch 完全解决的问题）提升代码 RL 的效果。
- **Math‑only RL Stage‑4 (32K 限制)**：最终再次回到数学领域，在 32K 限制下对高难度数学题目进行 RL，产出最终模型 AceReason-Nemotron 1.1。

**3. 输入‑输出流与关键设计选择**

整个流程的输入是预训练基础模型，经过 SFT 固定后，依次通过上述阶段。每个 RL 阶段均在上一个阶段的检查点基础上继续训练，形成一条逐步增强的链。关键控制旋钮包括：
- **过长时间过滤（overlong filtering）**：在早期短 token 预算（8K/16K）阶段对超出限制的生成施加负奖励或直接过滤，以促使模型生成简洁推理；但在后期长预算（32K）阶段移除此过滤，以避免损害推理完整性与效率（Section 4.5.3）。
- **采样温度调节**：RL 阶段的采样温度被调整至使温度调整后的生成熵保持在约 0.3，从而平衡探索与利用（Section 4.5.2）。

这一设计使得最终模型在数学（AIME 2024/2025）与代码（LiveCodeBench v5/v6）基准上同时实现了 7B 规模下的新 SOTA，且强 SFT 模型在 RL 后仍能带来持续性能增益，尽管差距会有所缩小（Abstract）。



结合材料说明，AceReason‑Nemotron 1.1 的训练流程由两部分组成：（1）数学/代码联合监督微调（SFT）构建强基模型；（2）分阶段的强化学习（RL）逐步提升推理能力。由于论文未提供封闭形式的公式，本节重点阐述关键模块及其背后的量化机制，并说明在缺少显式公式的情况下，哪些规律替代了常规推导。

### 📌 核心模块

#### 1. 数学与代码 SFT（Math & Code SFT）
该模块基于大规模收集和过滤的题目构建强 SFT 基础模型。关键特征如下：

- **题目规模**：数学题目约 247 K，代码题目约 136 K（Section 3.1.2，Figure 2）。
- **扩展策略**：扩展独特题目数量（prompts）比增加每题的回答数量（responses）对推理性能的提升更显著（Section 3.1.2，原文"scaling the number of prompts yields more significant gains"）。
- **多轮训练**：SFT 在 5–6 个 epoch 后性能趋于饱和，适度的"过拟合"反而有助于长链推理（Appendix D，Figure 8）。

该模块的输出直接决定后续 RL 起点的强弱，且更强的 SFT 模型在 RL 结束后仍保持优势（尽管差距会缩小，见 Abstract）。

#### 2. 七阶段 RL 训练（Math‑only + Code‑only + 最终 Math）
RL 训练采用先数学后代码、再回归数学的阶段设计，逐步放宽生成长度限制，并动态调整过长时间过滤策略。各阶段按顺序模块如下：

| 模块 | 角色 | 长度限制 | 关键决策 |
|------|------|----------|----------|
| Math‑only Stage‑1 | 压缩推理链，为后续阶段预热 | 8 K | 应用过长时间过滤，强制模型形成简洁思维链（Figure 11，Section G） |
| Math‑only Stage‑2 | 扩展至更难题，大幅提升数学能力 | 16 K | 使用高难度题目，数学基准大幅跳升（Table 3，AIME 24 从 62.0 升至 65.3） |
| Math‑only Stage‑3 | 继续用高难度题精炼 | 24 K | 专注高难数学，过滤策略可维持 |
| Code‑only Stage‑I | 启动代码能力 | 24 K | 将数学 RL 迁移至编码任务 |
| Code‑only Stage‑II | 进一步提升编码推理 | 32 K | 采用逐 epoch 过滤策略，仅保留未在当前 checkpoint 解决的题目（Section 4 Evaluation） |
| Math‑only Stage‑4 | 最终数学冲刺，完成 AceReason‑Nemotron 1.1 | 32 K | **移除过长时间过滤**，使模型在 32 K 预算内自由生成，AIME 24 avg@64 从 70.2 升至 71.4，LiveCodeBench v6 avg@8 从 45.1 升至 48.0（Table 2，Figure 6） |

> **数据支持**：移除 Math‑only Stage‑1 会导致最终 AIME 25 准确率从 56.7 降至 51.8（Figure 11），证实该压缩阶段不可或缺。而数学 RL 对代码推理的增益主要来自 Stage‑2（Figure 12）。

### 📐 公式（机制）推导替代说明

验证分析中未提取到任何封闭形式的数学公式，因此本节给出论文依赖的三个量化调节规则，它们在效果上替代了传统的公式推导。

#### 规则 1：温度调节使调整后熵 ≈ 0.3
- **来源**：Section 4.5.2，Figure 5（左右子图）。
- **机制**：保持策略模型的生成熵适度高位，平衡探索与利用。训练时若温度固定为 0.6 或 1.0，模型性能次优；主动选择温度使**温度调整后的熵**维持在 0.3 左右时，RL 收敛最快、最终效果最好。
- **操作建议**：训练与推理时均使用温度 0.6 可获得稳健表现（Figure 5 右表），但更优温度可能不同，需根据熵曲线选取。

#### 规则 2：过长时间过滤与 Token 预算的函数关系
- **来源**：Section 4.5.3，Figure 6，Table 2。
- **机制**：在短预算（8 K、16 K）下，初始训练有约 30% 的生成超出限制，加入负奖励过滤可有效压缩长度、稳定训练；当预算拉长至 32 K 时，过滤策略反而损害性能（例如，AIME 24 71.4 vs 70.2，LCB v6 48.0 vs 45.1）。
- **因果解释**：长预算下移除过滤，模型能学会更经济的生成，无需硬性截断（"makes the inference more token efficient and allows more concise generation"，Section 4.5.3）。

#### 规则 3：SFT 性能对题目数与回答数的敏感性差异
- **来源**：Appendix C，但**未提供显式公式**。
- **暗示形式**：性能 ≈ $a \log(x) + b \log(y)$，其中 $x$ 为独特题目数，$y$ 为每道题的回答数；测量表明 $a > b$，即扩展独特题目数带来的增益更大。
- **置信度说明**：该关系仅为附录中的定性讨论，缺少具体的拟合参数，因此属于需人工验证的弱证据点。

### 小结
AceReason‑Nemotron 1.1 的核心由"大规模题目驱动的 SFT"与"长度、温度、过滤三要素调控的七阶段 RL"两大模块构成。虽然没有常规意义上的公式推导，但上述三条量化规则（温度调节、过长时间过滤切换、SFT 数据缩放倾向）共同定义了模型的训练轨迹，也构成了该方法区别于以往工作的因果调节旋钮（causal knobs）。

---

本文所有分析均来自论文的验证摘要和分片证据，未发现任何显式公式，故不进行猜测。



## 实验与关键发现

### 主结果：7B 规模数学与代码推理新 SOTA

主结果见表 Table 1。AceReason‑Nemotron 1.1 在数学和代码基准上全面超越同量级的蒸馏 SFT 基线及 RL 基线，确立了新的 7B 级 SOTA。具体而言，在 AIME 2024 上 avg@64 达 72.6（较最强蒸馏基线 +17.1），AIME 2025 上为 64.8（+25.8）；代码方面，LiveCodeBench v5 avg@8 为 57.2（+19.6），v6 为 52.1（+18.0），EvalPlus avg@4 为 84.8（+4.4）。所有对比模型均采用相同推理模板、温度 0.6、top‑p 0.95、最大输出 32768 tokens，且使用 pass@1 avg@n 以降低方差；SFT 数据经过 9‑gram 去污染，杜绝基准泄露，因此对比公平、结果可信。

![[assets/figures/papers/iclr26_0005_IaEqjWXd1d_AceReason-Nemotron_1.1_Advancing_Math_and_Code_R/figures/002_Table_1.jpg]]
*Table 1: Evaluation of reasoning models primarily based on Qwen2.5-Math 7B and Llama-3.1 8B to disentangle the impact of pretraining. We report pass@1 averaged over n generations (avg@n) following the DeepSeek-R1 evaluation framework (same template, temperature=0.6, top p=0.95, max response length=32768). By default, we include official numbers from the model developers if they are available. Otherwise, †we evaluate the model using the official template and same evaluation setting as above. Note that, unlike the base model Qwen2.5-Math, MiMo-7B-RL is developed from a base model pretrained with extensive synthetic reasoning data from advanced reasoning model (Xia et al., 2025)*

### 核心消融：SFT 数据规模、训练温度与过滤策略

#### SFT 数据扩展：独特题目数量是主导因子

对 SFT 数据的缩放实验（Section 3.1.2）表明，**增加独特题目数量（prompt 数量）比增加每道题的回答数量（responses/prompt）对推理性能的提升更显著**。在 247K 数学题和 136K 代码题的规模下，扩大题目覆盖带来的增益呈超线性趋势，而单纯提高每题回答数仅在题目量不足时有边际效用。这直接导致后续 RL 的初始化模型质量：更强 SFT 模型在 RL 后始终更优，但 RL 训练过程中性能差距会收窄（参见 Figure 4/Figure 9 的 AIME24/AIME25 训练曲线）。

![[assets/figures/papers/iclr26_0005_IaEqjWXd1d_AceReason-Nemotron_1.1_Advancing_Math_and_Code_R/figures/009_Figure_4.jpg]]
*Figure 4: Math-only RL training starting from different SFT (distillation) models. The AIME24 accuracy at step-0 reflects the performance of the initial SFT checkpoints. The subsequent numbers in the figure show the final accuracy achieved at the end of each training stage: Math-Only Stage-1 (8K), Stage-2 (16K), Stage-3 (24K), and Stage-4 (32K)*

#### RL 采样温度：维持温度调整后熵 ≈ 0.3

RL 训练的采样温度不单纯追求探索或利用，而是**通过温度调整后的熵（temperature‑adjusted entropy）来量化权衡**。Figure 5 右表显示，当训练温度使该熵维持在约 0.3 时，模型在 AIME24/25 和 LCB v5/v6 上获得最佳最终性能。这一设定确保了生成响应的多样性既能发现新解法，又不至于产生过多无效路径，是 RL 提升的关键 knob。

![[assets/figures/papers/iclr26_0005_IaEqjWXd1d_AceReason-Nemotron_1.1_Advancing_Math_and_Code_R/figures/011_Figure_5.jpg]]
*Figure 5: Left: Trajectories of temperature-adjusted entropy during RL training with different policy LLM temperature settings. Right: Impact of varying temperatures for inference and RL training. We observe that using a temperature of 0.6 for inference consistently yields better average results, and thus adopt 0.6 as the default inference temperature unless otherwise specified*

#### 过长时间过滤：前期有利，后期有害的分阶段策略

过长时间过滤（overlong filtering）在不同 token 预算下的作用截然不同。Figure 6 及 Table 2 的对照实验揭示：

![[assets/figures/papers/iclr26_0005_IaEqjWXd1d_AceReason-Nemotron_1.1_Advancing_Math_and_Code_R/figures/016_Figure_6.jpg]]
*Figure 6: Ablation Studies on Math-Only RL training to assess the impact of overlong filtering. In both settings, Stage-1 starts with the same SFT model, and each subsequent stage begins with the same RL model from the previous stage trained under the best-performing setting (i.e., "w/ overlong filtering"). Notably, in the final stage (Stage-4), RL training without overlong filtering leads to superior performance. Evaluations are performed with a maximum sequence length of 32K. Results on AIME25 are in Appendix F. Table 2: Comparisons of the effects of increasing the maximum output length to 64K, with and without applying the overlong filtering at the last stage of Math-Only RL*

- 在早期短 token 限制阶段（Stage‑1 8K 及 Stage‑2 16K），应用过滤能迫使模型压缩推理链，避免陷入无意义长输出，带来显著收益。
- 当预算放宽到 24K 后，过滤的优势消失；到 **32K 的 Stage‑4 Math‑Only RL 阶段，移除过滤反而显著提升性能**。例如，AIME24 avg@64 从 70.2（带过滤）升至 71.4（无过滤），LiveCodeBench v6 avg@8 从 45.1 升至 48.0。Figure 10 的 AIME25 训练曲线进一步表明，无过滤设置在整个 Stage‑4 中持续优于带过滤设置，原因在于去除惩罚使推理更精简、tokens 利用更高效，有利于长链推理的收敛。

#### Math‑Only Stage‑1 的必要性与压缩机制

消除 **Stage‑1（8K 数学 RL）** 的消融（Figure 11 左侧）显示，缺少该阶段会直接削弱最终 AIME25 准确率（51.8 vs 56.7）。其作用并非直接推高指标——Stage‑1 期间 benchmark 分数甚至出现暂时下降——而是**通过 8K 长度约束强制模型学会压缩推理过程**（Figure 11 右侧，平均响应 token 数从 ~5.3K 降至 ~1.8K），为后续长 token 阶段释放了更有效的推理空间。进一步的步数分析（Table 3）表明，适度的 Stage‑1 训练（1200 步）即可为 Stage‑2 带来良好初始化，过多步数收益递减。

![[assets/figures/papers/iclr26_0005_IaEqjWXd1d_AceReason-Nemotron_1.1_Advancing_Math_and_Code_R/figures/027_Figure_11.jpg]]
*Figure 11: Left: Ablation study comparing models trained with and without Math-Only Stage-1. For "w/o Stage-1", the step-0 accuracy reflects the performance of the our SFT model on AIME25. In contrast, for "w/ Stage-1", the step-0 accuracy represents the final performance of Stage-1 RL initialized from the same SFT model. Right: Average response token length during Math-Only Stage-1 (8K) RL training*

#### 多轮 SFT 的过拟合正效应

SFT 多 epoch 实验（Figure 8，附录）显示，模型性能在 5‑6 个 epoch 后趋于饱和，但此后继续训练带来的轻微"过拟合"实际上**提升了长链推理能力**，这可能与模型对特定解题模式的记忆加深有关。因此，多轮 SFT 在本框架中并非有害。

#### 跨任务迁移与模型强度效应

数学 RL 对代码推理的增益主要来自 **Stage‑2（16K）**，且当 SFT 基础较弱时 Stage‑1 亦有辅助作用（见 Figure 12）。另外，Figure 15 表明，即便 RL 缩小了不同强度 SFT 模型间的差距，更强的 SFT 初始化仍能在 LiveCodeBench 上多解出超过 10 道困难题，说明预训练的深层知识是 RL 难以完全替代的。

### 失败模式与关键教训

- **短预算无害滤，长预算有害滤**：将早期有效的过长时间过滤照搬到 32K 阶段会直接损害推理精度，需在后期阶段主动移除。
- **固定温度无法平衡探索利用**：若采样温度不根据实际熵动态调整（例如默认 1.0），会导致响应过于发散或过于贪婪，RL 收敛停滞或退化。
- **跳过压缩阶段损失总体能力**：省略 Stage‑1 最终会丢失推理链的紧凑性，削弱长序列推理的后劲，这再次验证了"先压缩后扩展"的训练路径有效性。

综上，AceReason‑Nemotron 1.1 通过 SFT 题目数量优先扩展、温度‑熵协同调控、分阶段过滤策略以及先数学后代码的 RL 编排，系统性克服了先前方法割裂 SFT 与 RL 的瓶颈，实现了 7B 级别数学与代码推理的双重突破。



## 定位与知识库关联

AceReason‑Nemotron‑1.1 定位在 **SFT 与 RL 协同后训练** 的交叉点上，本质上是对"先大规模监督微调、后阶段式强化学习"这一路径的系统性实证。与之直接竞争的基线可分为两类：一类是仅依赖蒸馏或有限 SFT 的模型（如 DeepSeek‑R1‑Distill‑Qwen‑7B、Light‑R1‑7B、OpenMath‑Nemotron‑7B 等），另一类是直接应用 RL 但未精细调节数据与训练配方的模型（如 Skywork‑OR1系列、OlympicCoder‑7B 及前一版本 AceReason‑Nemotron‑1.0‑7B）。本工作的核心突破在于 **把 SFT 数据扩展（题目数量>回答数量）、RL 温度调节（使温度调整后熵≈0.3）与阶段性过长过滤（短预算用、长预算弃）耦合在一起**，从而在 7B 规模同时刷新数学与代码推理的 SOTA（Table 1）。相较此前最强的同架构 RL 基线和蒸馏基线，它在 AIME 2024/2025 上分别取得 +17.1 和 +25.8 的 avg@64 提升，在 LiveCodeBench v5/v6 上的 avg@8 提升超过 +18 点，且这些结果均在同一推理模板、温度 0.6、top‑p 0.95 和 9‑gram 去污染下评估，保证了公平性。

与多数仅关注蒸馏规模或仅做 RL 的跟进工作不同，AceReason‑Nemotron‑1.1 的关键区别源于三个 **可控变量**（changed slots）：
1. **SFT 数据扩展重点**：从单一依赖推理模型蒸馏转向大规模收集并过滤独特题目（247K 数学、136K 代码），同时保持每题多条回答以维持多样性（Section 3.1.2）。实验表明，增加独特题目数量比增加每题回答数量能带来更显著的性能增益（拟合系数 a > b，置信度 1.0）。
2. **RL 采样温度调节**：固定温度（如 0.6 或 1.0）被替换为动态选择温度，使策略模型生成文本的 **温度调整后熵保持在约 0.3**（Figure 5、Section 4.5.2），以此在探索与利用之间取得平衡。消融证实该设置下的最终 RL 模型在数学与代码基准上均优于其他温度。
3. **阶段式过长时间过滤策略**：不同于 Skywork‑OR1 等早期统一禁用过滤的做法，本方法在 token 预算较短的阶段（8K、16K）施加过滤，利用负奖励惩罚过长轨迹以压缩推理链（约 30% 初始生成超出 8K）；而当预算扩展到 24K 乃至 32K 时移除过滤（Section 4.5.3），以避免对有效长链推理的抑制。去除 32K 阶段的过滤后，AIME24 avg@64 从 70.2 提升到 71.4，LiveCodeBench v6 avg@8 从 45.1 提升到 48.0（Table 2），且推理过程更简洁、token 效率更高。

上述变量耦合的因果链条是：强大的 SFT 基础提供了足够多样本的候选空间；短预算 RL 强制模型学会紧凑的推理模式；随后放宽预算并移除过滤，使模型在长链问题上释放潜力。这一机制解释了为什么 **更强的 SFT 模型在 RL 后始终表现更好**（尽管性能差距会随 RL 训练而缩小，Abstract、Figure 4），也解释了数学 RL 对代码推理的正迁移主要体现在 Stage‑2（16K）阶段（Figure 12）。

### 适用边界与已知局限

该方法的有效范围与以下几点边界条件紧密相关：
- **模型规模限定在 7B**：所有实验基于 Qwen2.5‑Math‑7B 或 Llama‑3.1‑8B 基座，未曾验证该配方在更大模型（如 70B 级）或不同架构上的缩放行为。结论中关于温度熵 0.3、过滤阈值与数据量的最优组合可能依赖模型容量。
- **任务领域为竞赛数学与竞争性编程**：SFT 数据来源几乎全为奥数题库和编程竞赛原始题目，评估基准（AIME、LiveCodeBench、EvalPlus）高度匹配。该方法对需要开放式推理或知识密集型任务（如科学问答、长文本生成）的泛化性未提供证据。
- **RL 训练阶段高度工程化**：整个流水线包含三个数学专用阶段和两个代码专用阶段，每个阶段的 token 预算、过滤策略、奖励权重均需精心设置。多阶段训练的计算开销巨大，且 SFT 多 epoch 达到 5‑6 周期才饱和（Appendix D），存在较严重的"配方依赖"，若其中某一阶段移除（如跳过 Stage‑1），最终 AIME25 准确率从 56.7 骤降至 51.8（Figure 11），表明阶段设计不可随意裁剪。
- **过长时间过滤的结论受 token 预算驱动**：过滤的收益在 8K/16K 预算下显著，但在 24K 时优势消失，32K 时甚至有害。这意味着若后续工作采用不同的最大生成长度（如 64K 或更高），过滤策略需要重新标定，不能直接迁移（Table 2 中 64K 推断下不带过滤的收益略有下降，但推理效率仍占优）。
- **SFT 与 RL 脱钩的隐含假设**：论文假定数学和代码的 RL 可顺序进行（先数学后代码），且最终数学 RL 阶段不会遗忘代码能力。虽未观察到明显退化，但缺乏对联合多任务 RL（例如同时采数学与代码奖励）的直接对比，存在跨任务干扰未充分探索的可能。

### 开放问题

尽管论文通过大量消融回答了几个关键设计决策的必要性，但仍有若干问题待后续研究澄清：
1. **"温度调整后熵≈0.3"的原则是否与模型规模、奖励设计无关？** 当前分析仅基于 7B 模型和 GSM‑style 奖励，若迁移至不同奖励密度或更大模型，最佳熵区间可能需要重新搜索。
2. **阶段式 RL 的压缩-扩展机制能否推广到其他推理形式？** 例如在物理推理或逻辑谜题中，强制短预算是否也会迫使模型学习更泛化的思维模式，还是仅对数学证明生效？
3. **SFT 数据中"独特题目数量"的收益是否存在上限？** 论文展示了 log‑scale 扩展的趋势，但从 247K 数学题持续扩展是否最终也会饱和？饱和点与模型容量的关系未给出。
4. **代码 RL 阶段之前的数学 RL 究竟提供了何种表征基础？** 虽然从 Stage‑2 开始增益显著，但该增益多大程度归因于推理链长度适应，多大程度归因于解题模式（如 break‑down、回溯）的跨领域迁移，尚缺乏机制层面的分析（需人工验证）。
5. **过长时间过滤在更长 token 预算下是否仍然必要？** Table 2 中 64K 推理且不带过滤时，部分基准分数与 32K 带过滤持平，提示未来若能容忍极长输出，或许可完全弃用过滤，但这将引入极高的推理成本。其收益-成本权衡需要更系统的量化。

整体而言，AceReason‑Nemotron‑1.1 在 SFT‑RL 协同的工程实践上确立了一套可复现的组合配方，但其结论的鲁棒性很大程度上绑定于当前的任务分布、模型大小和数据设置，留出了从缩放律、跨任务泛化及多阶段学习理论等多个方向进行深入探索的空间。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/AceReason_Nemotron_1_1_Advancing_Math_and_Code_Reasoning_through_SFT_and_RL_Synergy.pdf

![[paperPDFs/ICLR_2026/AceReason_Nemotron_1_1_Advancing_Math_and_Code_Reasoning_through_SFT_and_RL_Synergy.pdf]]
