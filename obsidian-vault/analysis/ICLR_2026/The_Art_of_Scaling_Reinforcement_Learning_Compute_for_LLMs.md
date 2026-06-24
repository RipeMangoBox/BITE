---
title: "The Art of Scaling Reinforcement Learning Compute for LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/The_Art_of_Scaling_Reinforcement_Learning_Compute_for_LLMs.pdf
openreview_forum_id: FMjeC9Msws
aliases:
- ASRLCL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过调节Sigmoid缩放定律中的渐进性能上限参数A（受损失类型、批次大小、FP32精度修复等影响）和计算效率参数B（受PipelineRL、损失聚合方式、优势归一化等影响），可以在给定计算预算下最大化最终性能，并实现从小规模实验推广大规模性能的预测性缩放。"
primary_logic: "RL训练的compute-performance曲线可用Sigmoid饱和函数拟合（R_C = R_0 + (A-R_0)/(1+(C_mid/C)^B)），其中A代表渐进性能上限，B和C_mid决定计算效率。经验表明：1）不同方法的上限A差异巨大，优先选择能提高A的组件（如CISPO损失、大批量、FP32精度）是关键；2）常见优化手段（如损失聚合、长度惩罚）主要影响效率参数，对A影响甚微；3）从早期训练数据拟合参数可以可靠外推至大规模训练，使RL缩放像预训练一样可预测。据此集成的SCALERL配方在10万GPU小时训练中实现了与预测一致的可扩展性，并超越了现有方法。"
claims:
- "SCALERL在iid验证集上达到渐进pass rate A=0.61，优于DeepSeek (GRPO)、Qwen-2.5 (DAPO)、Magistral和Minimax-M1等方法。"
- "在8B密集模型上，SCALERL的AIME-24 pass rate在10万GPU小时后达到~0.58，且与从5万小时拟合外推的曲线一致，验证了预测性缩放。"
- "使用CISPO损失函数替代DAPO，渐进性能A提升显著；FP32精度修复将A从0.52提升至0.61。"
- "Leave-One-Out实验证实，SCALERL集成的每个组件（PipelineRL、CISPO、FP32、零方差过滤等）均对最终性能有正向贡献，且主要影响计算效率B。"
---

# The Art of Scaling Reinforcement Learning Compute for LLMs

> [!tip] 核心洞察
> RL训练的compute-performance曲线可用Sigmoid饱和函数拟合（R_C = R_0 + (A-R_0)/(1+(C_mid/C)^B)），其中A代表渐进性能上限，B和C_mid决定计算效率。经验表明：1）不同方法的上限A差异巨大，优先选择能提高A的组件（如CISPO损失、大批量、FP32精度）是关键；2）常见优化手段（如损失聚合、长度惩罚）主要影响效率参数，对A影响甚微；3）从早期训练数据拟合参数可以可靠外推至大规模训练，使RL缩放像预训练一样可预测。据此集成的SCALERL配方在10万GPU小时训练中实现了与预测一致的可扩展性，并超越了现有方法。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 大规模语言模型强化学习计算扩展的艺术 |
| 英文题名 | The Art of Scaling Reinforcement Learning Compute for LLMs |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=FMjeC9Msws) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SCALERL |
| Dataset | iid validation set (Polaris-53k math, 1000 held-out prompts), AIME-24 (downstream math reasoning), AIME-24 (ablation: generation length scaling), iid validation (math) - batch size scaling |

> [!tip] 效果简介
> - iid validation set (Polaris-53k math, 1000 held-out prompts) 上，pass rate mean@16 (asymptotic A) 为 SCALERL: A = 0.61，对比 DeepSeek (GRPO): A < 0.5; Qwen-2.5 (DAPO): A ≈ 0.52; Magistral: A ≈ 0.53; Minimax-M1: A ≈ 0.58 (estimated from Figure 2)，变化 SCALERL achieves highest asymptote, surpassing all other methods。
> - AIME-24 (downstream math reasoning) 上，pass rate 为 SCALERL-8B Dense at 100k GPU hours: ~0.58; SCALERL-17B×16 MoE at 50k GPU hours: ~0.67 (visual summary)，对比 ProRL (Liu et al., 2025a) on 1.5B model (lower performance, not directly comparable at same model size)，变化 Scaling model size yields substantial improvement; MoE outperforms dense with less compute.。
> - AIME-24 (ablation: generation length scaling) 上，pass rate 为 SCALERL-34k (32k generation length): peak ~0.64 at 32k GPU hours，对比 SCALERL-14k (14k generation length): peak ~0.54 at 32k GPU hours，变化 Longer generation length raises asymptote A by ~0.10。

## 概述

### 问题瓶颈

在大语言模型的强化学习训练中，不同算法配方在不同计算预算下的表现差异巨大，但长期以来缺乏一个统一的预测性框架来系统评估这些方法。实践者往往依赖经验直觉选择RL训练策略，无法可靠地判断某种方法在小规模实验中的优势能否延续到大规模训练场景。核心瓶颈在于：**不同设计选择对渐进性能和计算效率的影响机制不明确**，导致RL缩放方法的选择缺乏科学规律支撑。

### 核心方法

本文提出 **SCALERL**，一个系统集成的最佳实践配方，并建立了基于 **Sigmoid 饱和函数**的预测性缩放框架：

$$R_C - R_0 = (A - R_0) \times \frac{1}{1 + (C_{\mathrm{mid}} / C)^B}$$

该函数将验证集上的期望奖励 $R_C$ 建模为训练计算量 $C$ 的函数。其中 $A$ 代表**渐进性能上限**，$B$ 为**缩放指数**（决定计算效率），$C_{\mathrm{mid}}$ 为达到总增益一半所需的计算量。核心洞察在于：不同方法对参数的影响路径截然不同——**损失函数、批次大小、FP32精度修复等主要提升渐进上限 $A$**，而 **PipelineRL 异步框架、损失聚合方式、优势归一化等主要影响计算效率 $B$**。更重要的是，从早期训练数据拟合的参数可以可靠外推至大规模训练，使RL缩放像预训练一样可预测。

SCALERL 集成了以下关键组件：PipelineRL-8 异步生成-训练分离框架、CISPO 截断重要性采样损失、FP32 精度修复（LM head）、Prompt 级损失聚合、批次级优势归一化、零方差过滤和 No-Positive-Resampling 课程策略。

### 方法谱系与知识库定位

SCALERL 建立在 GRPO（Shao et al., 2024）和 DAPO（Yu et al., 2025）的基础上，但通过系统消融找到了显著提升可扩展性的组合。与现有主流方法相比：

- **DeepSeek (GRPO)**（Guo et al., 2025）使用 GRPO 损失和 PPO-off-policy-8，渐进性能 $A < 0.5$，训练不稳定且截断率升高。
- **Qwen-2.5 (DAPO)**（Yu et al., 2025）引入非对称裁剪和提示级聚合，$A \approx 0.52$，但对裁剪阈值敏感。
- **Magistral**（Rastogi et al., 2025）采用 PipelineRL 但保留 DAPO 损失，$A \approx 0.53$。
- **Minimax-M1**（MiniMax et al., 2025）使用 CISPO 损失和 FP32 精度修复，$A \approx 0.58$，是 SCALERL 最接近的参照。

SCALERL 通过组合 CISPO 损失、FP32 精度修复和优化后的训练配方，将渐进性能提升至 $A = 0.61$，在所有对比方法中达到最高上限。

### 主要结果

在 8B 密集模型上，SCALERL 经过 100,000 GPU 小时的训练，验证了预测性缩放的有效性：从 50,000 GPU 小时数据拟合的 Sigmoid 曲线（外推标记 ×）与继续训练至 100,000 小时的实际表现高度吻合。下游 AIME-24 评估同样呈现一致的缩放趋势，证明性能提升可泛化至训练分布之外。

**关键消融发现**：
- **FP32 精度修复**将渐进性能 $A$ 从 0.52 提升至 0.61，是最具影响力的单一改进。
- **CISPO 损失**相比 DAPO 显著提高渐进上限，且对超参数不敏感。
- **PipelineRL-8** 主要提升计算效率 $B$，对渐进上限影响较小。
- 将生成长度从 14k 扩展到 34k tokens，渐进性能 $A$ 额外提升约 0.10。
- 扩大批次大小（512 → 2048）将 $A$ 从 0.605 提升至 0.645。

Leave-One-Out 实验进一步证实，SCALERL 集成的每个组件均对最终性能有正向贡献，且主要通过影响计算效率 $B$ 发挥作用，所有变体在误差范围内达到相似的渐进上限。

> **注意**：部分基线方法（如 DAPO、MiniMax）因零方差过滤后的重采样机制使用了更大的实际批次大小（1280 vs 768），可能获得了一定的计算优势，但 SCALERL 仍在公平比较条件下表现最优。

## 背景与动机

### 推理语言模型的强化学习训练困境

大规模语言模型（LLM）的后训练阶段，强化学习（RL）已成为提升推理能力的关键技术。以GRPO（Shao et al., 2024）为代表的无批评家（critic-free）策略梯度方法，通过组内相对优势估计替代学习价值基线，大幅降低了RL训练的计算开销。然而，该领域面临一个核心瓶颈：**缺乏一套预测性框架来系统评估不同RL设计选择在计算预算下的可扩展性**。不同团队采用的损失函数、离策略设置、精度配置和聚合方式各异，但何种组合能在给定计算预算下最大化最终性能，以及这些选择如何影响渐进性能和计算效率，尚缺乏科学规律支撑——方法选择往往依赖经验试错，而非基于可外推的缩放定律。

### 现有方法的碎片化与不可比较性

当前主流的RL训练配方各自独立演进，形成了碎片化的设计空间。**DeepSeek**（Guo et al., 2025）采用GRPO损失配合对称裁剪与样本级平均聚合；**Qwen-2.5**（Yu et al., 2025）引入DAPO损失，解耦上下裁剪阈值并使用提示级聚合；**Magistral**（Rastogi et al., 2025）在DAPO基础上改用PipelineRL离策略算法；**Minimax-M1**（MiniMax et al., 2025）则集成了CISPO损失与FP32精度修复。这些方法在各自的实验设置下均报告了性能提升，但由于训练计算预算、模型规模和评估协议的不统一，难以直接比较其可扩展性优劣。更关键的是，在较小计算预算下表现优越的方法，在大规模计算外推时可能出现性能反转——这一现象在预训练缩放定律中已被充分认识，但在RL训练中尚未被系统研究。

### 预测性缩放框架的缺失

预训练领域已建立起成熟的缩放定律，能够从小规模实验外推大规模性能，指导计算资源的最优分配。然而，RL训练由于涉及在线生成、策略偏移和奖励稀疏等动态因素，其计算-性能关系更为复杂。现有工作缺乏一个统一的数学描述来刻画RL训练中验证奖励随计算量增长的饱和行为，也未能区分哪些设计选择影响渐进性能上限（asymptotic performance），哪些仅影响达到该上限的计算效率（compute efficiency）。这一认知缺口导致RL缩放方法的选择停留在经验层面，难以像预训练一样实现可预测的规模化扩展。

### 本文动机

针对上述问题，本文提出以**Sigmoid饱和函数**统一建模RL训练的compute-performance曲线，并系统消融影响曲线参数的关键设计选择。核心目标是：识别出能提升渐进性能上限A的组件（如损失函数、精度配置），以及主要影响计算效率B的组件（如离策略框架、聚合方式），从而构建一个可预测、可扩展的最佳实践配方**SCALERL**，并在10万GPU小时的大规模训练中验证其可预测性与有效性。

## 核心创新

本文的核心贡献在于将RL训练的compute-performance关系形式化为可预测的**Sigmoid缩放定律**，并基于该框架系统解耦了不同设计选择对渐进性能上限A和计算效率B的差异化影响，最终集成为**SCALERL**配方。其关键创新可归纳为两个层面：**预测性框架**与**组件级因果洞察**。

### 预测性缩放框架

SCALERL的核心方法论创新在于引入Sigmoid饱和函数来建模RL训练中iid验证集期望奖励$R_C$与训练计算量$C$之间的关系：

$$R_C - R_0 = (A - R_0) \times \frac{1}{1 + (C_{\mathrm{mid}} / C)^B}$$

其中$A$为渐进性能上限，$B$为缩放指数（控制曲线陡峭度），$C_{\mathrm{mid}}$为半程计算量（达到总增益50%所需的计算量），$R_0$为初始奖励。这一框架的实用价值在于：**从早期训练数据（如前1500 GPU小时）拟合的参数可以可靠外推至大规模训练**。在8B密集模型的10万GPU小时训练中，外推曲线（×标记）与实际训练轨迹高度吻合，验证了预测的可靠性（Figure 1）。

### 组件级因果洞察：上限A与效率B的分离

SCALERL的关键创新在于揭示了**不同设计选择对A和B的影响是高度可分离的**：

**影响渐进性能上限A的核心组件**（优先选择可提高A的组件是缩放策略的关键）：

- **CISPO损失函数**：替代DAPO损失后，渐进性能A显著提升。CISPO结合截断重要性采样与停止梯度（stop-gradient），对裁剪阈值不敏感，避免了DAPO因$\epsilon_{\max}$选择不当导致的性能退化（Figure 4b）。
- **FP32精度修复**：在训练器和生成器的LM head使用FP32计算logits，消除混合精度训练中的数值失配。这一修改将A从0.52提升至0.61，是单一贡献最大的改进（Figure 4c）。
- **更大batch size**：将batch size从512增至2048，A从0.605提升至0.645（Appendix Table 1）。

**主要影响计算效率B的组件**（对A影响甚微）：

- **PipelineRL-8异步框架**：通过连续流式生成rollouts并立即推送更新后的策略到生成器，大幅减少空闲时间，显著提升B（Figure 4a）。与PPO-off-policy-8相比，渐进性能A相似但效率更高。
- **Prompt级损失聚合**：每个prompt的所有生成取平均后再跨prompt平均，保证每个prompt对梯度更新贡献相等，达到最高渐进性能（Appendix Figure 10a）。
- **批次级优势归一化**：使用整个批次的奖励标准差对优势进行归一化，性能略优于prompt级归一化（Appendix Figure 10b）。
- **零方差过滤**：过滤掉所有生成结果奖励相同的prompt（无误梯度），避免无效计算，提升渐进性能（Appendix Figure 11a）。
- **No-Positive-Resampling**：根据历史pass rate移除已饱和的简单prompt（pass rate ≥ 0.9），将计算集中在有提升空间的样本上，提升可扩展性（Appendix Figure 11b）。

### 集成配方SCALERL

SCALERL将上述组件集成为一个异步RL配方：使用PipelineRL-8、强制截断控制生成长度、FP32 logits计算，并优化以下损失函数：

$$\mathcal{T}_{\mathrm{SCALERL}}(\theta) = \mathbb{E}_{\{y_i\}_{i=1}^G \sim \pi_{old}^{\theta}(\cdot|x)} \left[ \frac{1}{\sum_{g=1}^G |y_g|} \sum_{i=1}^G \sum_{t=1}^{|y_i|} \mathrm{sg}(\min(\rho_{i,t}, \epsilon)) \hat{A}_i^{\mathrm{norm}} \log \pi_{train}^{\theta}(y_{i,t}) \right]$$

该损失融合了prompt级聚合、批次级优势归一化、截断重要性采样（CISPO）、零方差过滤和No-Positive-Resampling条件（$0 < \mathrm{mean}(\{r_j\}_{j=1}^G) < 1$且$\mathrm{pass.rate}(x) < 0.9$）。Leave-One-Out实验（Figure 5）证实，SCALERL集成的每个组件均对最终性能有正向贡献，且SCALERL在所有变体中具有最高的计算效率。

### 相对于基线方法的差异化优势

与现有RL训练配方相比，SCALERL的创新体现在：

- **DeepSeek (GRPO)**（Guo et al., 2025）：使用GRPO损失和PPO-off-policy-8，渐进性能A < 0.5，且训练约6k GPU小时后因截断率升高而不稳定。
- **Qwen-2.5 (DAPO)**（Yu et al., 2025）：使用DAPO损失和提示级聚合，A ≈ 0.52，受限于损失函数对超参数的敏感性。
- **Magistral**（Rastogi et al., 2025）：类似DAPO但使用PipelineRL，A ≈ 0.53，未采用CISPO和FP32修复。
- **Minimax-M1**（MiniMax et al., 2025）：使用CISPO损失和FP32精度修复，A ≈ 0.58，但未集成零方差过滤和No-Positive-Resampling等效率优化。

SCALERL通过同时提升A（CISPO + FP32 + 大批量）和B（PipelineRL + 零方差过滤 + 课程学习），在iid验证集上达到A = 0.61，超越了所有对比方法（Figure 2）。

## 整体框架

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_FMjeC9Msws/figures/004_Figure_3.jpg]]
*Figure 3: Interpreting eq. (1). We provide an example fit illustrating the roles of parameters A, B , and $C _ { \mathrm { m i d } } ^ { \mathrm { ^ { - } } } . C _ { \mathrm { m i d } }$ determines the compute point at which half of the total gain is achieved - smaller values correspond to faster ascent toward the asymptote. B controls the curve’s steepness, with larger values indicating greater efficiency. A represents the asymptotic performance reached at large compute scales. Further discussion is provided in Appendix A.8

SCALERL 是一个面向大规模语言模型数学推理的异步强化学习训练配方。其核心设计围绕一个统一的预测性缩放框架展开：将 RL 训练中的 iid 验证集期望奖励（pass rate）建模为训练计算量 $C$ 的 Sigmoid 饱和函数：

$$R_C - R_0 = (A - R_0) \times \frac{1}{1 + (C_{\mathrm{mid}} / C)^B}$$

其中 $A$ 代表渐进性能上限，$B$ 为缩放指数（控制计算效率），$C_{\mathrm{mid}}$ 为半程计算量，$R_0$ 为初始奖励。这一函数形式使得从早期训练数据点拟合参数后，可以可靠地外推至大规模训练的性能表现——这正是 SCALERL 框架区别于以往经验性 RL 缩放方法的核心机制。

### 整体 Pipeline 架构

SCALERL 的 pipeline 由五个关键模块串联而成，形成从数据流到模型更新的闭环：

1. **异步生成-训练分离框架（PipelineRL-8）**：训练器（trainer）与生成器（generator）解耦运行。训练器每完成一次参数更新，立即将新权重推送到生成器；生成器持续流式产生 rollout 数据并写回经验池。这种连续流式设计将空闲时间降至最低，直接提升计算效率参数 $B$（Figure 4a）。

2. **强制截断（Forced Interruptions）**：当生成序列超过最大长度限制时，系统插入终止思考的提示词，强制模型停止推理并输出最终答案。该机制防止长度爆炸，保证训练稳定性。

3. **FP32 精度修复（LM head）**：在训练器和生成器的 LM head 层均使用 FP32 计算 logits，消除混合精度训练中 BF16/FP16 带来的数值失配问题。这一修复将渐进性能 $A$ 从 0.52 提升至 0.61（Figure 4c），是影响上限最显著的单一组件。

4. **CISPO 损失函数**：采用截断重要性采样与停止梯度（stop-gradient）结合的 REINFORCE 损失：

   $$\mathcal{I}_{\mathrm{CISPO}}(\theta) = \mathbb{E}_{\{y_i\}_{i=1}^G \sim \pi_{gen}(\cdot \vert x, \theta_{old})} \left[ \frac{1}{T} \sum_{i=1}^G \sum_{t=1}^{|y_i|} \mathrm{sg}(\min(\rho_{i,t}, \epsilon_{\max})) \hat{A}_i \log \left( \pi_{train}( y_{i,t} \vert x, y_{i<t}, \theta) \right) \right]$$

   相比 DAPO 损失，CISPO 对裁剪超参数不敏感，且能实现更高的渐进性能上限（Figure 4b）。

5. **数据筛选与课程学习**：
   - **零方差过滤**：丢弃所有生成结果奖励相同的 prompt（无有效梯度），避免无效计算。
   - **No-Positive-Resampling**：维护历史 pass rate 记录，永久移除 pass rate ≥ 0.9 的已饱和 prompt，将计算集中在有提升空间的样本上。

### 损失聚合与优势归一化

SCALERL 的最终损失函数 $\mathcal{T}_{\mathrm{SCALERL}}$ 融合了以下设计选择：

- **Prompt 级损失聚合**：每个 prompt 的所有生成取平均后再跨 prompt 平均，保证各 prompt 对梯度更新的贡献相等。消融实验表明 prompt 平均优于样本平均和 token 平均（Appendix Figure 10a）。
- **批次级优势归一化**：使用整个批次的奖励标准差对优势进行归一化（$\hat{A}_i^{\mathrm{norm}} = \hat{A}_i / \hat{A}_{\mathrm{std}}$），理论更合理，性能略优于 prompt 级归一化（Appendix Figure 10b）。

### 输入输出流

- **输入**：数学推理数据集（Polaris-53k，约 53k 个 prompt），每个 prompt 采样 $G$ 个完成结果（默认 $G=16$）。
- **生成阶段**：Generator 使用当前策略 $\pi_{gen}^{\theta_{old}}$ 对每个 prompt 生成 $G$ 个候选答案，经强制截断控制最大长度为 14,336 tokens。
- **奖励计算**：基于答案正确性的二元奖励（0/1），可选施加长度惩罚 $R_{\mathrm{length}}(y) = \mathrm{clip}(\frac{L_{\max} - |y|}{L_{\mathrm{cache}}} - 1, -1, 0)$。
- **训练阶段**：Trainer 从经验池读取 rollout 数据，计算 CISPO 损失并更新参数 $\theta$。更新后的权重立即推送至 Generator，形成异步闭环。
- **输出**：持续优化的策略模型，其 iid 验证集 pass rate 随计算量 $C$ 增长遵循可预测的 Sigmoid 曲线。

### 框架的核心运作逻辑

SCALERL 框架的核心洞察在于区分两类设计选择：**影响渐进上限 $A$ 的组件**（损失函数类型、批次大小、FP32 精度）和**主要影响计算效率 $B$ 的组件**（PipelineRL、损失聚合方式、优势归一化、零方差过滤等）。Leave-One-Out 实验（Figure 5）证实，各 LOO 变体最终达到的渐进奖励 $A$ 相近，但 SCALERL 集成方案在计算效率上显著领先——这正是通过系统性地选择提升 $A$ 和 $B$ 的组件组合实现的。

## 核心模块与公式推导

### 基础RL算法框架

SCALERL的基础算法源于GRPO（Shao et al., 2024），但移除了KL正则化项，并引入了DAPO的非对称裁剪机制（Yu et al., 2025）。给定一个prompt $x$，生成器策略 $\pi_{gen}^{\theta_{old}}$ 采样 $G$ 个完成结果 $\{y_i\}_{i=1}^G$，每个结果的奖励 $r_i$ 用于计算组归一化优势：

$$\hat{A}_i = r_i - \mathrm{mean}(\{r_j\}_{j=1}^G), \quad \hat{A}_i^G = \hat{A}_i / (\mathrm{std}(\{r_j\}_{j=1}^G) + \epsilon)$$

在token级别，重要性采样比率定义为当前训练策略与旧生成策略的概率比：

$$\rho_{i,t}(\theta) := \frac{\pi_{train}^{\theta}(y_{i,t} \mid x, y_{i,<t})}{\pi_{gen}^{\theta_{old}}(y_{i,t} \mid x, y_{i,<t})}$$

非对称裁剪函数为 $\mathrm{clip}_{\mathrm{asym}}(\rho, \epsilon^{-}, \epsilon^{+}) := \mathrm{clip}(\rho, 1-\epsilon^{-}, 1+\epsilon^{+})$。基础代理目标函数使用样本级平均聚合：

$$\mathcal{I}(\theta) = \mathbb{E}_{x \sim D, \{y_i\}_{i=1}^G \sim \pi_{gen}^{\theta_{old}}(\cdot|x)} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{|y_i|} \sum_{t=1}^{|y_i|} \min \left( \rho_{i,t}(\theta) \hat{A}_i^G, \mathrm{clip}_{\mathrm{asym}}(\rho_{i,t}(\theta), \epsilon^{-}, \epsilon^{+}) \hat{A}_i^G \right) \right]$$

### 核心改进模块

#### 1. 异步生成-训练分离框架（PipelineRL）

传统PPO-off-policy-k在生成rollouts时训练器处于空闲状态。PipelineRL将生成器和训练器解耦为连续流水线：训练器每次更新后立即将最新参数推送到生成器，生成器持续产生新rollouts。这大幅减少了空闲时间，在Figure 4a中表现为计算效率参数 $B$ 的显著提升，而对渐进性能上限 $A$ 的影响很小。

#### 2. CISPO损失函数

CISPO（MiniMax et al., 2025）将截断重要性采样与REINFORCE策略梯度结合，通过stop-gradient操作解耦重要性比率与梯度计算：

$$\mathcal{I}_{\mathrm{CISPO}}(\theta) = \mathbb{E}_{\{y_i\}_{i=1}^G \sim \pi_{gen}(\cdot \vert x, \theta_{add})} \left[ \frac{1}{T} \sum_{i=1}^G \sum_{t=1}^{|y_i|} \mathrm{sg}(\min(\rho_{i,t}, \epsilon_{\max})) \hat{A}_i \log \left( \pi_{train}( y_{i,t} \vert x, y_{i<t}, \theta) \right) \right]$$

其中 $\mathrm{sg}(\cdot)$ 为stop-gradient操作，$\epsilon_{\max}$ 为截断上限。Figure 4b的消融显示，CISPO和GSPO的渐进性能上限 $A$ 显著高于DAPO，且CISPO在训练后期保持更长的近线性奖励增长区间，对超参数不敏感。

#### 3. FP32精度修复

在混合精度训练中，LM head的logits默认使用BF16/FP16计算，导致训练器和生成器之间的数值失配，使重要性采样比率失准。SCALERL在训练器和生成器的LM head均强制使用FP32计算logits。Figure 4c显示，这一修复将渐进性能 $A$ 从0.52提升至0.61，是影响 $A$ 最大的单一设计选择。

#### 4. 损失聚合与优势归一化

- **Prompt级损失聚合**：每个prompt的所有生成结果先取平均，再跨prompt平均，保证每个prompt对梯度更新的贡献相等。Appendix Figure 10a显示，prompt平均的渐进性能优于样本平均和token平均。
- **批次级优势归一化**：使用整个批次的奖励标准差对优势进行归一化，而非仅在prompt组内。Appendix Figure 10b显示三种归一化方式（prompt级、batch级、无归一化）性能相似，batch级略优。

#### 5. 零方差过滤与课程学习

- **零方差过滤**：当某个prompt的所有生成结果奖励相同时（如全部正确或全部错误），优势均为零，该prompt对训练无梯度贡献。SCALERL过滤掉这些零方差prompt，仅保留有梯度信号的样本。
- **No-Positive-Resampling**：维护每个prompt的历史pass rate，将pass rate ≥ 0.9的已饱和prompt从后续训练中永久移除，将计算集中在仍有提升空间的样本上。

#### 6. 强制截断

在生成超过最大长度限制时，插入终止思考的提示词（如""），强制模型停止推理并输出最终答案，防止长度爆炸导致的训练不稳定。

### SCALERL最终损失函数

综合以上组件，SCALERL的最终损失函数为：

$$\mathcal{T}_{\mathrm{SCALERL}}(\theta) = \mathbb{E}_{\{y_i\}_{i=1}^G \sim \pi_{old}^{\theta}(\cdot|x)} \left[ \frac{1}{\sum_{g=1}^G |y_g|} \sum_{i=1}^G \sum_{t=1}^{|y_i|} \mathrm{sg}(\min(\rho_{i,t}, \epsilon)) \hat{A}_i^{\mathrm{norm}} \log \pi_{train}^{\theta}(y_{i,t}) \right]$$

其中 $\hat{A}_i^{\mathrm{norm}}$ 为批次级归一化优势，且仅对满足 $0 < \mathrm{mean}(\{r_j\}_{j=1}^G) < 1$ 且 $\mathrm{pass.rate}(x) < 0.9$ 的prompt计算损失。该损失融合了prompt级聚合、截断重要性采样、零方差过滤和No-Positive-Resampling条件。

### 长度惩罚奖励

对正确回答的过长完成结果施加惩罚，鼓励简洁推理：

$$R_{\mathrm{length}}(y) = \mathrm{clip}\left(\frac{L_{\max} - |y|}{L_{\mathrm{cache}}} - 1, -1, 0\right)$$

其中 $L_{\max}$ 为最大生成长度，$L_{\mathrm{cache}}$ 为缓存长度阈值。该惩罚仅应用于正确回答的trace，且被限制在 $[-1, 0]$ 范围内。

## 实验与分析

### 主结果：SCALERL的可预测缩放与性能优势

SCALERL的核心主张在于，RL训练的compute-performance曲线可以用一个Sigmoid饱和函数可靠拟合，从而实现从早期训练数据外推大规模性能的预测性缩放。这一主张在10万GPU小时级别的实验中得到了验证。

在8B密集模型上，SCALERL在iid验证集（Polaris-53k数学数据集，1000个held-out prompts）上训练至10万GPU小时。研究者使用前5万小时的数据点拟合Sigmoid曲线（公式1），并将外推曲线（图1中的×标记）与实际延长训练至10万小时的结果进行对比，发现外推预测与实际性能高度吻合。下游AIME-24评测同样表现出与训练曲线一致的缩放趋势，表明性能提升泛化到了训练分布之外。

在方法对比中（图2），SCALERL取得了最高的渐进pass rate上限 **A = 0.61**，显著超越现有主流RL配方：

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_FMjeC9Msws/figures/003_Figure_2.jpg]]
*Figure 2: SCALERL is more scalable than prevalent RL methods. We fit sigmoid curves (Equation 1) on iid validation dataset to commonly-used training recipes like DeepSeek (GRPO) (Guo et al., 2025), Qwen-2.5 (DAPO) (Yu et al., 2025), Magistral (Rastogi et al., 2025), and Minimax-M1 (MiniMax et al., 2025), and compare them with SCALERL. SCALERL surpasses all other methods, achieving an asymptotic reward of A = 0 . 6 1 . Stars denote evaluation points; solid curves show the fitted curve over the range used for fitting; dashed curves extrapolate beyond it. We validate the predictability by running each method for longer ($^ { 6 6 } \times ^ { 7 }$ markers), which align closely with the extrapolated curves...*

- **DeepSeek (GRPO)** (Guo et al., 2025)：A < 0.5，且因截断率升高在约6k GPU小时后训练不稳定
- **Qwen-2.5 (DAPO)** (Yu et al., 2025)：A ≈ 0.52
- **Magistral** (Rastogi et al., 2025)：A ≈ 0.53
- **Minimax-M1** (MiniMax et al., 2025)：A ≈ 0.58（估计值）

值得注意的是，DAPO和MiniMax由于零方差过滤后重新采样的机制，实际使用的batch size为1280，大于SCALERL的768，这给予了它们一定优势，但SCALERL仍表现最优。所有方法均在相同的8B密集模型和训练数据上评估，拟合曲线使用同一验证集的前1.5k GPU小时后数据点，确保比较的公平性。

在更大规模模型上，SCALERL-17B×16 MoE在仅5万GPU小时的训练下，AIME-24 pass rate达到约0.67（图1），显著优于8B密集模型在10万小时下的约0.58，验证了模型规模扩展带来的实质收益。


![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_FMjeC9Msws/figures/002_Figure_1.jpg]]
*Figure 1: Predicatably Scaling RL compute to 100,000 GPU Hours (a) We run SCALERL for 100k GPU hours on an 8B dense model, and 50k GPU hours on a 17Bx16 MoE (Scout). We fit a sigmoid curve (Equation (1)) on pass rate (mean@16) on iid validation dataset up to 50k (and 16k) GPU hours and extrapolate to 100k (and 45k) on the 8B (Scout MoE) models respectively. We trained for 7400 steps for 8B and 7100 steps for Scout, which is 3.5× larger than ProRL (Liu et al., 2025a). The extrapolated curve (× markers) closely follows extended training, demonstrating both stability at large compute and predictive fits–establishing SCALERL as a reliable candidate for RL scaling. (b) Downstream evaluation on AIME-24 sho...*

### Sigmoid缩放定律：参数含义与解释框架

SCALERL的分析框架建立在Sigmoid compute-performance曲线上：

$$R_C - R_0 = (A - R_0) \times \frac{1}{1 + (C_{\mathrm{mid}} / C)^B}$$

其中三个参数具有明确的工程含义（图3）：
- **A（渐进性能上限）**：在大计算极限下的饱和性能，是最终优化的目标
- **B（缩放指数）**：控制曲线的陡峭程度，B越大表示计算效率越高，能更快接近上限
- **C_mid（半程计算量）**：达到总增益一半所需的计算量，C_mid越小说明早期提升越快

这一框架的核心洞见是：**不同设计选择对A和B的影响是分离的**。提升A的组件（如损失函数选择、FP32精度修复、大批量）直接决定最终性能天花板；而影响B的组件（如PipelineRL、损失聚合方式、优势归一化）主要决定达到该天花板的效率。因此，方法设计的优先级应当是先追求高A，再优化B——因为一个低效但高上限的方法最终会超越高效但低上限的方法（图9）。

### 关键组件消融：渐进性能上限A的决定因素

#### FP32精度修复：最关键的单项改进

在LM head层使用FP32精度计算logits，是SCALERL中影响最大的单项设计选择。图4c显示，仅将训练器和生成器的LM head从BF16/FP16切换为FP32，就将渐进性能A从**0.52提升至0.61**，提升幅度达0.09。这一修复解决了混合精度训练中重要性采样比率（IS ratio）的数值失配问题：当logits在BF16下计算时，训练策略和生成策略之间的概率比率出现系统性偏差，导致梯度估计质量下降。附录A.19中的详细分析（图21-23）进一步验证了IS比率在FP32下恢复准确性。

在17B×16 MoE模型上的Leave-One-Out实验（图7b）中，FP32修复同样将A从0.700提升至0.710，且缩放指数B从1.97提升至2.30，证实该改进在不同模型规模下均有效。

#### 损失函数：CISPO vs DAPO vs GSPO

损失函数的选择直接影响渐进性能上限。图4b比较了三种损失函数：
- **DAPO**（非对称裁剪，ε_low=0.2, ε_high=0.26）：A较低，B=1.77
- **GSPO**（Zheng et al., 2025a）：A显著高于DAPO
- **CISPO**（截断重要性采样+停止梯度）：A最高，B=2.01，且对裁剪阈值ε_max不敏感

CISPO的优势源于其结合了截断重要性采样与REINFORCE的策略梯度形式：

$$\mathcal{I}_{\mathrm{CISPO}}(\theta) = \mathbb{E}_{\{y_i\}_{i=1}^G \sim \pi_{gen}(\cdot \vert x, \theta_{add})} \left[ \frac{1}{T} \sum_{i=1}^G \sum_{t=1}^{|y_i|} \mathrm{sg}(\min(\rho_{i,t}, \epsilon_{\max})) \hat{A}_i \log \left( \pi_{train}( y_{i,t} \vert x, y_{i<t}, \theta) \right) \right]$$

其中停止梯度算子sg(·)使截断后的IS比率仅作为权重而不参与梯度计算，这避免了DAPO中非对称裁剪对超参数的敏感性（附录图19a显示，改变ε_max会根本性地改变A值）。GSPO在性能上与CISPO接近，但CISPO在训练后期表现出更持久的近线性奖励增长，因此被选为最终方案。

#### 批次大小与生成长度：以计算换上限

更大的批次大小和更长的生成长度都遵循“早期看似更差，但最终上限更高”的模式。

批次大小消融（附录表1）显示：

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_FMjeC9Msws/figures/029_Table_1.jpg]]

- bs512：A = 0.605
- bs2048：A = 0.645，提升了约0.04

生成长度消融（图6a，图17）显示：

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_FMjeC9Msws/figures/032_Figure_17.jpg]]
*Figure 17: Scaling RL batch size and generation length. larger batch size and generation length are slower in training but settles at a higher asymptote. These show an inverse trend initially where smaller values seem better at lower compute budget, but reach a higher asymptotic performance at larger scale*

- 14k生成长度：在32k GPU小时处达到约0.54的峰值
- 34k生成长度：在32k GPU小时处达到约0.64的峰值，A提升约0.10

这两项改进的共同机制是：更大的批次提供了更稳定的梯度估计，更长的生成长度允许模型进行更充分的推理链探索。两者都以更高的单步计算成本为代价，但在大计算预算下，最终性能的增益证明了这一投资的合理性。在最大规模的10万小时实验中，SCALERL使用了batch size 2048来稳定训练并确保外推的可靠性。

### 计算效率B的优化：PipelineRL与聚合策略

#### 异步框架：PipelineRL vs PPO-off-policy

图4a比较了两种异步off-policy RL设置：
- **PPO-off-policy-k**：每k步更新一次生成策略
- **PipelineRL-k**：trainer更新后立即推送到generator，连续流式生成rollouts

两种设置在渐进性能A上相似，但PipelineRL显著提高了计算效率B。这是因为PipelineRL减少了训练过程中的空闲时间：generator无需等待trainer完成整个更新周期即可获取最新策略权重。在SCALERL中，PipelineRL-8（8步off-policyness）被选为默认配置。

#### 损失聚合与优势归一化

损失聚合方式（附录图10a）的比较显示：
- **Prompt平均**（每个prompt的所有生成取平均后再跨prompt平均）：达到最高渐进性能
- **样本平均**（每个rollout等权）：性能次之
- **Token平均**：性能最低

Prompt平均的优势在于保证每个prompt对梯度更新的贡献相等，避免生成数量多的简单prompt主导训练。

优势归一化方法（附录图10b）的比较显示，prompt级、batch级和无归一化三者性能相似，batch级略优。Batch级归一化使用整个批次的奖励标准差进行缩放，理论上更合理，因为它保留了不同prompt难度差异的信息。

### Leave-One-Out验证：各组件的协同效应

图5的Leave-One-Out实验从SCALERL出发，每次将一个设计选择回退到基线版本，重新训练并拟合缩放曲线。主要发现：

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_FMjeC9Msws/figures/008_Figure_5.jpg]]
*Figure 5: Leave-One-Out (LOO) Experiments: Starting from SCALERL, we revert one design choice at a time to its baseline counterpart and re-train. Most LOO variants reach a similar asymptotic reward, with SCALERL outperforming slightly overall. The main difference in these methods lies in efficiency. To highlight this, we re-arrange Equation (1) into $\mathcal { F } ( R _ { c }$ ) = $C ^ { B }$ , where $\begin{array} { r } { \mathcal { F } ( R _ { c } ) = C _ { \mathrm { m i d } } ^ { B } / \left( \frac { A - R _ { 0 } } { R _ { c } - R _ { 0 } } - 1 \right) } \end{array}$ , and plot log $\mathcal { F } ( R _ { c }$ ) vs. log C. This makes slope B directly visible, showing that SCALERL has the highest compute...

- **所有LOO变体在误差范围内达到相似的渐进性能A**，SCALERL整体略优
- **主要差异体现在计算效率B上**：SCALERL具有最高的计算效率

通过重新排列Sigmoid公式为 $\mathcal{F}(R_c) = C^B$ 并绘制 $\log \mathcal{F}(R_c)$ vs $\log C$，斜率B直接可视化为直线的倾斜度。SCALERL的斜率最大，证实其集成的各项组件（PipelineRL、CISPO、FP32、零方差过滤、No-Positive-Resampling等）在效率维度上产生了正向协同效应。

### 零方差过滤与课程学习

两项辅助机制进一步提升了可扩展性：

**零方差过滤**（附录图11a）：过滤掉所有生成结果奖励相同的prompt（即pass rate为0或1的prompt），因为这些样本贡献零策略梯度。过滤后达到更高的渐进性能，因为它避免了无效计算占用训练预算。

**No-Positive-Resampling**（附录图11b）：维护历史pass rate记录，永久移除pass rate ≥ 0.9的已饱和简单prompt。这一课程学习策略将计算集中在仍有提升空间的样本上，同时提升了渐进性能A和可扩展性。

### 多任务扩展与泛化

SCALERL的缩放框架不仅适用于单一数学任务。在数学+代码的联合RL训练中（图16），数学和代码验证集上的性能均遵循可预测的Sigmoid缩放曲线，且多任务设置下的数学性能与纯数学训练相当。这表明该框架具有良好的任务泛化性。


![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_FMjeC9Msws/figures/030_Figure_16.jpg]]
*Figure 16: SCALERL scales predictably on math and code. We report both the code and math validation set performance on the joint math+code RL run; along with the math only SCALERL run as a reference. These results demonstrate that our sigmoidal compute–performance relationship holds across task mixtures, and that SCALERL’s scalability generalizes beyond a single domain training*

在下游评测方面，SCALERL在AIME-25和MATH-500上的表现（附录图26）与AIME-24的趋势一致，进一步验证了性能提升并非过拟合于特定评测集。

### 公平性说明与实验局限

**基线比较的公平性**：如前所述，DAPO和MiniMax因零方差过滤后的重采样机制，实际batch size（1280）大于SCALERL（768），这可能给予了它们一定优势。DeepSeek (GRPO)在约6k GPU小时后因截断率升高而训练不稳定，未完全收敛到最佳性能，因此其A值可能被低估。

**拟合的可靠性**：研究者通过3次独立运行测量了SCALERL的拟合方差（图7a），渐进性能A的误差范围约为±0.02，表明缩放曲线的拟合具有合理的可重复性。

**generations per prompt的影响**：在中等batch size下，将每prompt生成数从8调整至32并相应调整prompt数量以保持总batch固定，拟合的缩放曲线基本不变（附录图15），表明在中等规模下这一分配是二阶因素。但在更大batch规模下，更清晰的差异可能会出现，这留待未来工作探索。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_FMjeC9Msws/figures/007_Figure_4.jpg]]
*Figure 4: (a) Comparing “compute-scaling” of asynchronous off-policy RL setups. We report only the B (scaling exponent) and A (asymptotic pass rate) parameters of the fitted sigmoid curve (Equation 1). PipelineRL-k is much more efficient and slightly better in the large compute limit. (b) Comparing loss functions: DAPO (Yu et al., 2025), GSPO (Zheng et al., 2025a), and CISPO (MiniMax et al., 2025). We find CISPO/GSPO achieve a higher asymptotic reward compared to DAPO. (b) Using FP32 precision in the final layer (LM head) gives a considerable boost in the asymptotic reward*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_FMjeC9Msws/figures/013_Figure_7.jpg]]
*Figure 7: (a) Variance in scaling fits. We train 3 independent runs of SCALERL to measure variance. We observe a ±0.02 error margin for asymptotic performance A. (b) FP32 LOO on Scout: Comparing SCALERL on Scout with and without FP32 precision fix at the LM Head. SCALERL performs better with the FP32 fix*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_FMjeC9Msws/figures/028_Figure_15.jpg]]
*Figure 15: Scaling to (a) different number of generations per prompt, (b) Downstream performance of different number of generations per prompt*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_FMjeC9Msws/figures/034_Figure_18.jpg]]
*Figure 18: Downstream performance of (a) different number of generations per prompt, on AIME, (b) LiveCodeBench (Jan-June 2025) performance on math+code run, (c) AIME-24 performance on math+code run*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_FMjeC9Msws/figures/036_Figure_19.jpg]]
*Figure 19: (a)Comparing upper clipping ratio of DAPO loss function. Change of $\epsilon _ { m a x }$ fundamentally changes the asymptotic performance value A. (b) CISPO clipping ratio ablations*


## 方法谱系与知识库定位

### 1. 与基线方法的关系

SCALERL 并非从零构建的全新算法，而是在现有主流 RL 训练配方基础上，通过系统化消融和参数化缩放分析，逐步集成最优组件而形成的“最佳实践配方”。其与各基线方法的关系可归纳如下：

- **继承自 DeepSeek (GRPO)**（Guo et al., 2025）：SCALERL 的基础算法框架源于 GRPO——一种不使用 KL 正则化项的策略优化方法。在此基础上，SCALERL 保留了非对称 DAPO 裁剪机制，但将损失函数从 GRPO 的原始形式替换为 CISPO，并将 off-policy 设置从 PPO-off-policy 升级为 PipelineRL-8。

- **继承自 Qwen-2.5 (DAPO)**（Yu et al., 2025）：SCALERL 沿用了 DAPO 的非对称裁剪策略（$\epsilon_{\text{low}}=0.2$, $\epsilon_{\text{high}}=0.26$），但发现 DAPO 损失函数在渐进性能上限 $A$ 上显著弱于 CISPO/GSPO（Figure 4b），因此将其替换。此外，DAPO 使用的提示级优势归一化被 SCALERL 替换为批次级归一化，后者在理论上更合理且性能略优。

- **继承自 Minimax-M1**（MiniMax et al., 2025）：SCALERL 直接采纳了 Minimax-M1 的两个关键设计——CISPO 损失函数和 FP32 精度修复。CISPO 通过截断重要性采样与停止梯度结合，对裁剪阈值不敏感，显著提升了渐进性能 $A$；FP32 精度修复则解决了训练器和生成器在 LM head 上的数值失配问题，将 $A$ 从 0.52 提升至 0.61（Figure 4c）。SCALERL 在此基础上进一步集成了零方差过滤和 No-Positive-Resampling 等机制。

- **继承自 Magistral**（Rastogi et al., 2025）：Magistral 率先将 PipelineRL 作为 off-policy 算法引入 RL 训练。SCALERL 沿用了这一设计，并验证了 PipelineRL 在计算效率 $B$ 上的显著优势——它通过异步生成-训练分离框架减少了空闲时间，使训练更快逼近渐进性能上限（Figure 4a）。

**关键区分点**：SCALERL 与上述方法的本质差异不在于引入全新组件，而在于其“预测性缩放”方法论。通过 Sigmoid 缩放定律 $R_C = R_0 + (A-R_0)/(1+(C_{\text{mid}}/C)^B)$，SCALERL 将不同设计选择的影响分解为对渐进性能上限 $A$ 和计算效率 $B$ 的独立调制，从而实现了从小规模实验外推大规模性能的能力。这一框架使得 SCALERL 在 10 万 GPU 小时的训练中，实际性能与从 5 万小时拟合外推的曲线高度吻合（Figure 1），验证了其作为“可靠缩放候选”的定位。

### 2. 适用边界

SCALERL 的有效性建立在以下前提之上，超出这些边界时需谨慎推广：

- **任务类型**：当前验证集中在可验证数学推理任务（Polaris-53k 数学数据集，AIME-24 下游评估）。对于开放域生成、对话等缺乏明确二元奖励信号的任务，Sigmoid 缩放曲线的拟合和外推能力尚未得到验证。

- **模型规模**：主要实验在 8B 密集模型和 17B×16 MoE 模型上完成。尽管 MoE 模型展现出更高的渐进性能和更优的计算效率（Figure 1），但 SCALERL 在更大规模（如 100B+）模型上的缩放行为仍需进一步验证。

- **训练数据分布**：iid 验证集上的 pass rate 缩放曲线能否泛化到分布外（OOD）测试集，论文明确指出这是开放问题。Figure 1b 显示 AIME-24 下游性能与 iid 验证集缩放趋势一致，但更广泛的 OOD 泛化性有待确认。

- **计算预算**：Sigmoid 拟合依赖于训练早期（前 1.5k GPU 小时）的数据点来外推长期行为。对于计算预算极低（无法收集足够拟合点）或极高（接近饱和区域）的场景，预测精度可能下降。论文中 SCALERL 在 10 万 GPU 小时处的外推与实测吻合，但更远距离的外推可靠性未被证明。

- **超参数敏感性**：SCALERL 的 CISPO 损失对裁剪阈值不敏感，但其他组件（如批次大小、生成长度）对渐进性能 $A$ 有显著影响。例如，将生成长度从 14k 提升至 32k tokens 可将 $A$ 提升约 0.10（Figure 6a），但代价是计算速度变慢。这意味着 SCALERL 的“最优”配置依赖于具体的计算预算约束。

### 3. 局限与开放问题

**已知局限**：

1. **组件影响的非独立性**：Leave-One-Out 实验（Figure 5）显示，大多数 LOO 变体在渐进性能 $A$ 上与 SCALERL 相似，主要差异体现在计算效率 $B$ 上。这表明 SCALERL 的组件之间存在一定的功能冗余，单独移除某一组件不会导致性能崩溃。但这也意味着 SCALERL 的“最优性”是增量式的——它通过多个小幅改进的累积获得优势，而非依赖单一突破性设计。

2. **FP32 精度修复的必要性**：FP32 精度修复是提升 $A$ 最有效的单一改动（从 0.52 到 0.61），但这增加了计算开销。论文未量化 FP32 带来的额外计算成本与性能收益之间的权衡关系。

3. **批次大小的二阶效应**：在中等批次（768）下，每个 prompt 的生成数量（8/16/24/32）对缩放曲线影响甚微（Appendix A.14），论文认为这是“二阶选择”。但在更大批次下，这一分配策略的重要性可能上升，目前缺乏系统研究。

**开放问题**：

1. **跨预训练规模、模型容量和 RL 训练数据的联合缩放定律**：当前 Sigmoid 缩放定律仅建模 RL 训练计算与性能的关系。能否将预训练计算量、模型参数量、RL 训练数据量统一纳入一个预测框架，是论文明确提出的未来方向。

2. **结构化奖励与生成式验证器下的最优计算分配**：SCALERL 依赖二元正确性奖励。当使用结构化奖励（如部分正确性评分）或生成式验证器时，Sigmoid 缩放曲线的形式是否仍然适用，以及如何优化计算分配，是未解决的问题。

3. **多轮 RL 和智能体交互场景的推广**：论文指出将缩放框架扩展到多轮 RL、智能体交互和长程推理是重要的研究方向。这些场景的奖励稀疏性和交互复杂性可能使 Sigmoid 饱和假设失效。

4. **OOD 泛化的预测性缩放**：Figure 1b 仅展示了 AIME-24 这一下游任务的缩放趋势。能否为 OOD 泛化性能建立类似的预测性缩放定律，是 RL 训练从“拟合训练分布”走向“真正泛化”的关键瓶颈。

> **注意**：上述开放问题均来自论文自身的讨论（§6 RELATED WORK 及 Conclusion），尚未有后续工作提供解答。若需补充最新进展，建议手动检索相关 follow-up 文献。

## 原文 PDF

![[paperPDFs/ICLR_2026/The_Art_of_Scaling_Reinforcement_Learning_Compute_for_LLMs.pdf]]
