---
title: "Revolutionizing Reinforcement Learning Framework for Diffusion Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Revolutionizing_Reinforcement_Learning_Framework_for_Diffusion_Large_Language_Models.pdf
project_link: null
code_link: https://github.com/Gen-Verse/dLLM-RL
openreview_forum_id: KNAyc9DMe3
aliases:
- RRLFDLLM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "TraceRL optimizes diffusion LLMs on their own inference trajectories with PPO-style clipped losses and a diffusion-based value model."
primary_logic: "It collects denoising trajectories, aggregates steps with a shrinkage parameter, estimates step values with a diffusion value model, and updates the policy to match actual sampling paths."
claims:
- "TraceRL aligns training signals with structured diffusion decoding trajectories instead of random masking."
- "The diffusion value model reduces reward variance and supports process rewards along denoising steps."
- "The note reports MATH500 and LiveCodeBench gains for TraDo models over SDAR and several autoregressive baselines."
---

# Revolutionizing Reinforcement Learning Framework for Diffusion Large Language Models

> [!tip] 核心洞察
> Revolutionizing

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Revolutionizing Reinforcement Learning Framework for Diffusion Large Language Models |
| 英文题名 | Revolutionizing Reinforcement Learning Framework for Diffusion Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KNAyc9DMe3) · [GitHub](https://github.com/Gen-Verse/dLLM-RL) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method |  |
| Dataset | |

> [!tip] 效果简介
> 结果与证据沿用下文“实验与关键发现”中的现有记录；本轮不新增或外推论文事实。

## 概要

扩散大语言模型（Diffusion LLMs）通过并行生成文本，在推理效率上展现出超越自回归模型的潜力，但其在复杂推理任务上的性能仍落后于主流自回归模型。核心瓶颈在于：**训练阶段的随机掩码目标与推理阶段的结构化解码轨迹之间存在根本性失配**——训练时模型学习从任意随机掩码位置恢复被遮挡的 token，而推理时模型则沿特定的去噪轨迹逐步生成，这种不一致导致训练信号未能有效对齐推理行为。

针对这一问题，本文提出 **TraceRL**，一种轨迹感知的强化学习后训练框架。TraceRL 的核心洞察是：**将 DLM 自身的推理轨迹信息显式纳入训练过程**，使优化目标与推理时的实际去噪路径保持一致。具体而言，TraceRL 从模型推理过程中提取中间轨迹，通过引入收缩参数 $s$ 将连续步聚合为训练片段，并采用 PPO 风格的裁剪替代损失进行策略优化；同时，引入基于扩散过程的价值模型来稳定训练并自然容纳过程奖励信号。

实验表明，TraceRL 在数学推理和代码生成任务上取得显著提升。在 MATH500 基准上，基于 TraceRL 优化的 **TraDo-4B-Instruct**（静态采样）达到 **75.6%** 的准确率，较基线 SDAR-4B-Chat 的 70.2% 提升 **+5.4 个百分点**（Table 2）；8B 规模的 TraDo-8B-Instruct 在动态采样下达到 78.5%，超越 Qwen2.5-7B-Instruct 等自回归模型。在 LiveCodeBench-V2 上，TraDo-8B-Instruct 相较 Llama3.1-8B-Instruct 提升 6.6%。此外，TraceRL 支持灵活扩展至长链思维（long-CoT）场景，TraDo-8B-Thinking 在 MATH500 上可达 87.4%。

从方法谱系看，TraceRL 属于扩散模型后训练方法，区别于传统的随机掩码微调（random masking）和半自回归微调（semi-autoregressive fine-tuning），其关键创新在于**轨迹对齐的强化学习目标**和**扩散原生价值模型**的引入，为扩散大语言模型的推理能力提升提供了新的范式。

### 扩散语言模型的推理困境

扩散语言模型（Diffusion Language Models, DLMs）作为自回归模型之外的另一条生成范式，通过迭代去噪过程生成文本。其训练目标通常为证据下界（ELBO），在完全随机掩码的条件下优化模型从任意噪声状态恢复原始序列的能力：

$$q ( x _ { t } \mid x _ { 0 } ) = \prod _ { i } \Bigl ( ( 1 - t ) \delta _ { x _ { 0 } ^ { i } } + t \delta _ { [ \mathrm { M A S K } ] } \Bigr )$$

然而，这一训练范式与模型的实际推理轨迹之间存在根本性的错位。在推理时，DLMs 并非从完全随机的掩码状态开始去噪，而是沿着特定的、模型偏好的生成轨迹逐步揭示序列信息。这种训练-推理分布的不一致，构成了制约 DLM 推理能力提升的核心瓶颈。

### 现有微调方法的局限

针对上述问题，已有工作尝试通过微调来弥合训练与推理之间的鸿沟，但效果参差不齐。**Table 1** 中的实证研究揭示了关键发现：在全注意力模型（Dream-7B-Instruct）上，使用模型自身推理轨迹（trace l=16）进行优化可获得 54.4% 的准确率，而采用完全随机掩码目标仅能达到 39.6%。在半自回归（semi-autoregressive）设定下，同等计算量时半自回归目标的准确率（52.6%）同样远超完全随机目标（39.6%）。

这一对比表明，**训练目标与推理轨迹的一致性**是提升 DLM 推理能力的关键杠杆。然而，现有方法要么固守完全随机的训练范式，要么缺乏系统性的轨迹感知机制，无法在强化学习框架下将推理轨迹信息有效融入训练过程。

### 块扩散模型的结构特性

块扩散模型（Block Diffusion Models）通过块注意力机制（block-diffusion attention）在训练效率与采样效率之间取得了折中。这类模型天然适配半自回归微调目标，能够在保持训练效率的同时，使生成过程更贴近实际推理轨迹。但如何将这一结构优势转化为强化学习场景下的稳定训练信号，仍是一个开放问题。

### 本文动机

基于上述分析，本文的核心动机可归结为两点：

1. **轨迹对齐的必要性**：实验证据表明，将训练目标与模型自身的推理轨迹对齐，是释放 DLM 推理潜力的关键。这需要一种能够在强化学习框架中显式利用推理轨迹信息的方法。

2. **训练稳定性的需求**：扩散模型的迭代生成特性使得传统的奖励信号难以提供细粒度的过程监督。引入基于扩散的价值模型，有望在提供过程奖励的同时增强训练稳定性，从而支撑轨迹感知的强化学习范式。

这两点动机共同指向了 TraceRL 框架的设计原点：通过轨迹感知的强化学习，将推理轨迹信息系统性地融入 DLMs 的后训练过程。

## 核心方法与创新机理

TraceRL 的核心创新在于将扩散语言模型（DLM）的强化学习训练目标与模型自身的**推理轨迹（inference trajectory）**对齐，而非沿用传统 RL 方法中与推理过程脱节的随机掩码训练范式。这一设计转变由以下三个关键机制共同支撑：

### 轨迹感知的策略优化

传统 DLM 的 fine-tuning 使用完全随机的掩码模式（fully random masking），训练时模型被迫从任意位置恢复被掩码的 token，这与推理时从左到右逐步去噪的实际行为存在显著分布偏移。TraceRL 直接以模型在 rollout 过程中产生的中间轨迹为优化单元：给定问题 $Q$，模型通过扩散采样生成一条包含多个中间步骤的轨迹 $\tau$，策略损失基于该轨迹上的重要性采样比和 clipped surrogate objective 进行计算，同时引入 KL 散度惩罚项防止策略偏离参考模型过远。为控制计算开销，引入**收缩参数 $s$**，将每 $s$ 个连续步骤聚合为一个训练单元，在保持轨迹对齐精度的前提下提升训练效率。实验表明，较小的 $s$ 值（如 $s=1$）能更紧密地跟随推理轨迹，从而获得更高的准确率（Table 6）。

### 扩散式价值模型（Diffusion-based Value Model）

TraceRL 提出使用扩散模型本身作为价值网络，而非引入独立的价值估计器。这一设计的直接收益体现在训练稳定性上：价值模型通过 clipped MSE loss 对轨迹中各步骤的回报 $R_j$ 进行回归，其输出 $V_{\theta_v}(\tau)_j$ 被用于计算优势函数。在 SDAR-4B-Chat 上的实验显示，引入价值模型后训练过程中奖励的方差从 $6.6 \times 10^{-4}$ 降至 $3.6 \times 10^{-4}$（Figure 5a），降幅约 45.5%，显著平滑了优化曲线。此外，扩散式价值模型天然适合整合**过程奖励（process reward）**：通过 GAE（参数 $\gamma=0.99, \lambda=1$）将轨迹级别的稀疏奖励分解为逐步的密集信号，使模型在每个去噪步骤都能获得有效反馈，最终在 MATH500 上带来约 0.7 个百分点的额外提升（Figure 5b）。

### 架构通用的轨迹适配

TraceRL 的设计对全注意力（full-attention）和块注意力（block-attention）两种 DLM 架构均适用。对于块扩散模型，训练目标被切分为大小为 $B'$ 的 slice 以实现高效并行训练；同时 TraceRL 支持在推理时**放大块大小（block size enlargement）**——先在 $B=4$ 下进行 rollout，再以 $B=8$ 应用 TraceRL 优化，使 MATH500 准确率从 60.2 提升至 67.7（Table 3），缓解了大块推理直接应用时的性能退化问题。

### 与 baseline 的 changed slots 对比

相对于 SDAR 等 baseline 采用的半自回归 fine-tuning（semi-AR SFT）或完全随机掩码训练，TraceRL 的核心 changed slots 可归纳为：

| 维度 | Baseline（SDAR / 半自回归 SFT） | TraceRL |
|------|-------------------------------|---------|
| 训练信号来源 | 预定义的掩码模式（随机或半自回归） | 模型自身推理轨迹 |
| 训练-推理对齐 | 存在分布偏移 | 轨迹级别对齐 |
| 价值估计 | 无或独立价值网络 | 扩散式价值模型 |
| 奖励密度 | 仅结果奖励 | 支持过程奖励（GAE 集成） |
| 块大小适应性 | 固定块大小 | 支持训练后放大块大小 |

这些 changed slots 共同解释了 TraDo-4B-Instruct 在 MATH500 上以静态采样取得 75.6% 准确率、相较 SDAR-4B-Chat（70.2%）实现 +5.4 个百分点提升的因果路径：轨迹对齐确保了优化方向与推理行为一致，扩散式价值模型降低了训练方差并提供了密集的过程监督，而块大小放大进一步释放了推理效率与精度的权衡空间。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_KNAyc9DMe3/figures/001_Figure_1.jpg]]
*Figure 1: Trajectory illustration (left) and TraceRL overview (right, see details in Section 4). Right panel is an example of TraceRL with shrinkage parameter s = 2 , , sequence length L = 6 , and block size B = 3 (when using block diffusion). We aggregate s consecutive steps to perform trajectoryaware reinforcement learning. Integers inside the squares indicate trajectory information*

TraceRL 是一个面向扩散大语言模型的轨迹感知强化学习后训练框架。其核心设计动机源于一项关键实证发现：**将训练目标与模型自身的推理轨迹对齐，能够显著提升推理性能**。具体而言，使用模型偏好的推理轨迹（即模型在推理过程中自然产生的中间状态序列）进行微调，在 MATH500 上可达到 54.4% 的准确率，而等计算量下的全随机掩码训练仅为 39.6%（Table 1）。这一发现构成了 TraceRL 整体 pipeline 的设计基础。

### Pipeline 总览

TraceRL 的完整 pipeline 由三个核心模块串联构成（Figure 1 右半部分）：

1. **轨迹收集**：使用当前策略模型（policy model）对给定的问题 $Q$ 进行推理采样，生成多条推理轨迹 $\{\tau_i\}_{i=1}^d$。每条轨迹记录了模型在扩散去噪过程中各中间步骤的 token 状态序列。

2. **轨迹感知优化**：将收集到的轨迹输入策略优化模块。该模块引入一个**收缩参数 $s$**，将轨迹中每 $s$ 个连续步骤聚合为一个优化单元，从而在保留轨迹结构信息的同时提升训练效率。策略损失采用带重要性采样的裁剪替代损失（clipped surrogate loss），并附加 KL 散度惩罚项以约束策略更新幅度。

3. **扩散价值模型辅助**：框架引入一个基于扩散架构的价值模型（value model），用于估计轨迹中各步骤的状态价值。该价值模型通过裁剪回归损失进行训练，其扩散式设计天然支持过程奖励（process reward）的集成。价值模型的引入旨在降低训练过程中的奖励方差（实验表明方差可从 $6.6 \times 10^{-4}$ 降至 $3.6 \times 10^{-4}$，Figure 5a），从而稳定训练动态。

### 模块关系与数据流

三个模块之间形成闭环的数据流：

- **策略模型 → 轨迹**：策略模型以问题 $Q$ 为输入，通过扩散采样过程输出推理轨迹。对于全注意力 DLM，采用静态采样（temperature=0.1, block size=32）；对于块注意力 DLM，采用动态采样（temperature=1.0, 默认 block size=4）。
- **轨迹 → 策略优化**：收集到的轨迹经收缩参数 $s$ 聚合后，作为策略优化的经验数据。优化目标是最小化轨迹感知的策略损失 $\mathcal{T}_{policy}(\theta_p)$。
- **轨迹 → 价值模型训练**：同一批轨迹同时用于训练价值模型，价值模型学习预测各步骤的累积回报，其损失函数 $\mathcal{T}_{value}(\theta_v)$ 采用裁剪后的 MSE 形式。
- **价值模型 → 策略优化**：价值模型输出的状态价值估计用于计算优势函数（advantage），通过 GAE（参数 $\gamma=0.99, \lambda=1$）集成过程奖励信息，反馈至策略优化模块以降低梯度估计方差。

### 架构适配性

TraceRL 的一个关键特性是其**架构无关性**：同一套框架可同时适用于全注意力 DLM 和块注意力 DLM。对于块扩散模型，训练目标可被切片为 $B'$ 大小的训练块以支持高效并行训练；此外，TraceRL 还支持在推理时使用较小 block size（如 $B=4$）进行 rollout，而在训练时适配更大的 block size（如 $B=8$），从而在保持采样效率的同时提升训练效果（Table 3 表明此策略可在 MATH500 上达到 67.7% 准确率）。

> **注意**：关于收缩参数 $s$ 的具体选取策略以及扩散价值模型相比标准价值网络的计算开销，原文未给出定量分析，需结合附录或后续工作进一步确认。

### 扩散语言模型基础

TraceRL 建立在掩码扩散语言模型（Masked Diffusion Language Models）之上。其前向过程将真实 token 逐步替换为 `[MASK]`：

$$q(x_t \mid x_0) = \prod_{i=1}^{n} \operatorname{Cat}\Bigl(x_t^i; (1-t)\delta_{x_0^i} + t\delta_{[\mathrm{MASK}]}\Bigr)$$

其中 $t \in [0,1]$ 控制掩码比例，$x_0$ 为原始序列，$x_t$ 为加噪后的序列。全注意力 DLM 的训练目标为证据下界（ELBO）：

$$\mathcal{I}_{full}(x_0, Q, \theta) = \int_0^1 \frac{1}{t|x_0|} \mathbb{E}_{q(x_t|x_0)}\left[\sum_{i: x_t^i=[\mathrm{MASK}]} \cdots \right]$$

该目标对序列中所有被掩码位置进行随机重建，称为 **全随机掩码目标**（fully random masking objective）。

### 半自回归微调目标

块扩散模型（Block Diffusion Models）天然支持半自回归（semi-autoregressive）微调，其训练目标 $\mathcal{I}_{semi}(x, Q, \theta)$ 使模型在生成后续 token 时以先前的上下文为条件。全注意力模型则需将数据切片为块后再应用该目标。这一设计是 TraceRL 中轨迹对齐的基础。

### TraceRL 核心模块

TraceRL 包含三个关键组件：**策略优化目标**、**扩散价值模型** 和 **收缩机制**。

#### 收缩机制

推理过程中 DLM 产生的中间轨迹步数较多，直接逐步优化效率低下。引入收缩参数 $s$，将每 $s$ 个连续步骤聚合为一个训练单元，在保持轨迹信息的同时提升训练效率。

#### 策略目标

策略网络 $\theta_p$ 的优化采用带重要性采样的截断代理损失，并附加 KL 散度惩罚项：

$$\mathcal{T}_{policy}(\theta_p) = \mathbb{E}_{\substack{Q \sim D_{max} \\ \{\tau_i\}_{i=1}^d \sim \pi_{mad}(\cdot|Q)}} \left[ \cdots \right]$$

其中 $\pi_{mad}$ 为当前策略，$D_{max}$ 为数据集，$\tau_i$ 为采样的推理轨迹。重要性采样比率经过裁剪以稳定训练，KL 惩罚约束策略更新幅度。

#### 扩散价值模型

TraceRL 引入一个基于扩散架构的价值模型 $V_{\theta_v}$，其训练使用截断均方误差损失：

$$\mathcal{T}_{value}(\theta_v) = \frac{1}{2} \mathbb{E}_{\tau} \left[ \frac{1}{|\tau|} \sum_{j \in \tau} \max\left( (V_{\theta_v}(\tau)_j - R_j)^2, (V_j^{\mathrm{clip}} - R_j)^2 \right) \right]$$

其中 $R_j$ 为轨迹中第 $j$ 步的回报，$V_j^{\mathrm{clip}}$ 为裁剪后的旧价值估计。该价值模型的作用体现在两方面：
- **降低训练方差**：实验显示奖励方差从 $6.6 \times 10^{-4}$ 降至 $3.6 \times 10^{-4}$（降幅约 45.5%），显著稳定训练过程；
- **容纳过程奖励**：通过 GAE（Generalized Advantage Estimation）整合轨迹级过程奖励，GAE 参数设置为 $(\gamma, \lambda) = (0.99, 1)$。

#### 块扩散训练的切片优化

对于块扩散模型，TraceRL 将训练目标从 $\sum_{i=1}^{|\tau|} f(\tau(i))$ 切片为 $B'$ 大小的训练单元，实现高效的并行训练。

### 关键设计选择

- **收缩参数 $s$ 的影响**：较小 $s$ 值使优化更紧密地跟随推理轨迹，性能更优。$s=1$ 在 MBPP 上取得最高准确率 37.0，但每步 GPU 耗时最高（3.7 A100 小时/步）；$s=4$ 最快（2.1 GPU 小时/步）但准确率最低。
- **块大小适配**：TraceRL 可将推理时的块大小从 $B=4$ 扩展至 $B=8$，避免直接扩大块大小导致的性能下降（MATH500 上从 67.4 降至 60.2），适配后恢复至 67.7。

## 实验与关键发现

### 主实验结果

TraceRL 在数学推理与代码生成任务上均取得了显著的性能提升。在 MATH500 基准上，**TraDo-4B-Instruct** 以静态采样达到 75.6% 的准确率，较基线 **SDAR-4B-Chat**（70.2%）提升 **+5.4 个百分点**（Table 2）。更大规模的 **TraDo-8B-Instruct** 在动态采样下进一步将 MATH500 准确率推至 78.5%，而采用长思维链（long-CoT）的 **TraDo-8B-Thinking** 更达到 87.4%。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_KNAyc9DMe3/figures/003_Table_2.jpg]]
*Table 2: The main benchmark results across different math and coding tasks. “Static” denotes static sampling, and “Dynamic” denotes dynamic sampling. The long-CoT model TraDo-8B-Instruct is evaluated using dynamic sampling with threshold 0.9*

在代码基准 LiveCodeBench-V2 上，TraceRL 同样展现出强劲的迁移能力：TraDo-8B-Instruct 以动态采样取得 25.9% 的准确率，较基线实现 7.4% 的增益。对于全注意力架构的扩散语言模型，TraceRL 在 LiveCodeBench-V2 上达到 25.0%（Figure 4）。

值得注意的是，**4B 规模的 TraDo-Instruct 模型在 MATH500 上的表现已超越 7B 级别的自回归模型 Qwen2.5-7B-Instruct**，验证了轨迹感知强化学习对小模型推理能力的有效提升。

### 轨迹对齐的因果机制

TraceRL 的核心设计在于将训练目标与模型自身的推理轨迹对齐。Table 1 的实证分析揭示了这一机制的关键性：

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_KNAyc9DMe3/figures/002_Table_1.jpg]]
*Table 1: We explore how effectively different methods tune the model to learn CoT reasoning and thereby improve reasoning accuracy under non-CoT prompts. 2000 datapoints were generated using Qwen2.5 models and filtered for quality. l denotes the length of each step in the complete trace.$^ { \ast \epsilon } \times m ^ { \prime \prime }$ indicates that we apply m independent random maskings to augment the dataset for a fair comparison. “Token forward” denotes the number of tokens processed by the model, representing computational load/time. “Token trained” refers to the number of tokens directly contributing to the optimization objective. We report accuracy on MATH500. The block-attention model used h...

- 使用模型**自身偏好的推理轨迹**（trace l=16）进行全注意力微调，准确率达到 54.4%，显著优于半自回归方式（53.4%，semi-ar ×2）和完全随机掩码方式（39.6%，fully random ×1）。
- 在等量计算负载下，半自回归目标（52.6%）相比完全随机目标（39.6%）在全注意力模型上提升了 13 个百分点，表明**保持轨迹结构**比单纯增加计算量更为关键。

这一发现直接支撑了 TraceRL 的设计选择：通过在强化学习过程中采样并利用模型的中间推理轨迹，而非随机掩码，使优化方向与推理行为保持一致。

### 价值模型的作用

扩散价值模型（diffusion-based value model）的引入对训练稳定性和最终性能产生了可测量的影响：

- **方差控制**：在 4B 模型的数学任务训练中，加入价值模型后奖励方差从 $6.6 \times 10^{-4}$ 降至 $3.6 \times 10^{-4}$，降幅约 45%（Figure 5a），有效抑制了训练波动。
- **过程奖励集成**：价值模型天然支持轨迹级过程奖励（process reward），使用 GAE 参数 $(\gamma, \lambda) = (0.99, 1)$ 时，训练曲线上升更快且最终准确率更高（Figure 5b，约 0.630 vs 0.623）。
- **消融对比**：Figure 3 显示，带有价值模型的 TraceRL（红色曲线）在块扩散模型的数学任务上始终优于无价值模型版本（黄色曲线），验证了价值函数在策略优化中的引导作用。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_KNAyc9DMe3/figures/005_Figure_3.jpg]]
*Figure 3: RL method ablations on block diffusion models for math RL tasks. The red and yellow curves represent TraceRL with and without a value model, respectively. The blue curve corresponds to training with a random masking objective in each block, similar to the semi-autoregressive approach. The green curve represents training with an additional complementary mask within block*

### 块大小自适应

TraceRL 支持在不牺牲性能的前提下扩大推理块大小，从而提升采样效率。Table 3 展示了这一能力：

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_KNAyc9DMe3/figures/010_Table_3.jpg]]
*Table 3: Adapting block size from B = 4 to 8 on reasoning tasks with TraceRL. Reported values are accuracies of these baselines under dynamic sampling with threshold 0.9*

- 直接将块大小从 $B=4$ 扩大到 $B=8$ 会导致 MATH500 准确率从 67.4% 降至 60.2%。
- 使用 TraceRL 进行轨迹对齐训练后，$B=8$ 的模型准确率恢复至 **67.7%**，与原始 $B=4$ 模型持平，同时获得更高的加速比。

这一结果表明 TraceRL 能够解耦推理效率与模型性能之间的权衡，为实际部署提供了灵活性。

### 收敛速度与加速效果

TraceRL 在收敛速度上展现出优势。Figure 4 的训练曲线表明，在全注意力模型的代码任务上，TraceRL 相比基线方法收敛更快且最终性能最佳。Table 4 报告了各模型的加速比：TraDo-4B-Instruct 在 MATH500 上达到最高加速比 2.63，在 LiveBench 上为 1.61，表明轨迹感知训练在保持推理质量的同时有效减少了总采样步数。

### 关键超参数分析

- **收缩参数 $s$**：Table 6 显示，$s=1$（即不聚合轨迹步）在 MBPP 上取得最高准确率 37.0%，但单步训练耗时 3.7 A100 GPU 小时；$s=4$ 将耗时降至 2.1 小时，但准确率下降至 33.0%。较小的 $s$ 值使优化更紧密地跟随推理轨迹，与核心设计原则一致。
- **GAE 参数**：Table 5 表明，在 SDAR-1.7B 上，不同 $(\gamma, \lambda)$ 组合（$(0.99, 1.0)$、$(1.0, 1.0)$、$(1.0, 0.0)$）均将 MATH500 准确率从基线的 61.1% 提升至 63.0%–63.4%，差异不显著，说明 TraceRL 对该超参数不敏感。

### 失败模式与局限

论文未明确报告失败案例或错误分析。当前证据主要集中在正向性能增益上，以下方面需进一步验证：

- 长思维链模型（TraDo-8B-Thinking）在 AIME2024 上平均响应长度达 19,397 tokens（Table 7），虽取得高准确率，但推理成本显著增加，实际部署时需权衡延迟与精度。
- 在 LiveCodeBench-V2 上，扩散模型的绝对准确率（25.9%）仍低于部分自回归基线，表明代码生成任务上仍有提升空间。
- 缺乏对推理错误类型（如逻辑断裂、计算错误、幻觉）的分类分析，无法判断 TraceRL 具体改善了推理链的哪些环节。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_KNAyc9DMe3/figures/009_Figure_5.jpg]]
*Figure 5: Comparison of training with and without a value model. (a) Incorporating a value model reduces training fluctuations during training. This experiment is conducted on SDAR-4B-Chat. (b) A value model enables integration of trajectory-level process rewards, yielding faster optimization than relying solely on outcome rewards. This is conducted on SDAR-1.7B-Chat*

## 定位与知识库关联

### 1. 方法谱系：从扩散语言模型 RL 到轨迹感知优化

TraceRL 处于**扩散语言模型（Diffusion Language Models, DLMs）后训练增强**这一新兴谱系中。该谱系的核心瓶颈在于：DLMs 的推理过程天然产生中间轨迹（intermediate traces），但现有 RL 微调方法（如基于随机掩码的半自回归微调）并未显式利用这些轨迹信息进行优化，导致训练目标与推理轨迹之间存在错位。

**谱系上游**可追溯至两个基础组件：
- **掩码扩散语言模型（Masked DLMs）**：如 LLaDA（Nie et al., 2024）和 Dream（He et al., 2024），建立了基于随机掩码的生成框架，其训练目标为证据下界（ELBO）$\mathcal{I}_{full}(x_0, Q, \theta)$。
- **块扩散模型（Block Diffusion Models）**：如 SDAR（Arriola et al., 2025; Cheng et al., 2025），通过块扩散注意力机制结合了自回归训练效率和扩散采样效率，并天然支持半自回归微调。

**TraceRL 的差异化定位**在于：它是首个将 RL 优化目标与 DLM 推理轨迹显式对齐的框架。与直接使用随机掩码目标进行微调的方法不同，TraceRL 通过收缩参数 $s$ 聚合连续推理步，在轨迹级别上应用裁剪代理损失（clipped surrogate loss）和 KL 惩罚，使策略优化紧密跟随模型自身的推理偏好轨迹。

**与基线方法的关键区分**：
- 相较于**半自回归微调**（semi-autoregressive SFT），TraceRL 不仅利用了块结构，还引入了轨迹级别的价值估计和策略梯度优化。
- 相较于**随机掩码 RL 训练**（random masking objective in each block），TraceRL 的轨迹感知设计在 MATH500 上带来约 5.4% 的绝对精度提升（4B 模型，Table 2）。
- 相较于**标准 PPO 类方法**，TraceRL 的扩散价值模型（diffusion-based value model）天然适配 DLM 的生成过程，可直接容纳过程奖励（process rewards），训练方差从 $6.6 \times 10^{-4}$ 降至 $3.6 \times 10^{-4}$（Figure 5(a)）。

### 2. 适用边界与架构限制

**架构适用性**：TraceRL 声称适用于全注意力（full-attention）和块注意力（block-attention）两类 DLM 架构。实验覆盖了 Dream-7B（全注意力）、LLaDA-8B（全注意力）和 SDAR-4B/8B（块注意力）等代表性模型。但需注意，全注意力模型在应用 TraceRL 时需要额外的数据切片操作以适配块训练，这可能引入计算开销。

**任务域限制**：当前验证集中在数学推理（MATH500、AIME2024、GSM8K）和代码生成（LiveCodeBench-V2、LiveBench、MBPP）等需要链式推理（CoT）的任务。TraceRL 的核心假设——推理轨迹包含可被 RL 利用的结构化信息——在这些领域中自然成立，但在开放式对话、翻译等任务上的适用性尚未验证。

**模型规模限制**：实验覆盖 1.7B、4B、7B、8B 参数规模。在 4B 模型上观察到 5.4% 的 MATH500 提升，在 8B 模型上观察到 7.4% 的 LiveCodeBench-V2 提升。但缺乏更大规模（如 70B+）或更小规模（<1B）的验证，轨迹信息的价值是否随模型规模单调递增仍需进一步研究。

**采样策略依赖**：TraceRL 在动态采样（dynamic sampling）下进行 rollout 训练，但评估同时报告了静态采样（static sampling, temperature=0.1）和动态采样（temperature=1.0）两种设置。动态采样提供更快的推理速度，静态采样提供更高精度，这种双重评估策略增加了结果的可信度，但也意味着实际部署时需要根据场景选择采样模式。

### 3. 已知局限与开放问题

**已知局限**：
1. **收缩参数 $s$ 的精度-效率权衡**：较小的 $s$ 值（如 $s=1$）带来更高精度（MBPP 37.0），但训练成本显著增加（3.7 GPU小时/步）；较大的 $s$ 值（如 $s=4$）加速训练（2.1 GPU小时/步）但精度下降（MBPP 34.2，Table 6）。论文未提供 $s$ 的自适应选择策略。
2. **块大小扩展的上限**：TraceRL 可将块大小从 $B=4$ 扩展到 $B=8$ 并保持精度（MATH500 67.7，Table 3），但进一步扩展到 $B=16$ 或更大是否仍有效，论文未探索。
3. **价值模型的额外开销**：扩散价值模型的训练和推理开销相对于策略网络的比例未量化报告，这在资源受限场景下可能成为瓶颈。

**开放问题**：
1. **轨迹质量与 RL 效率的关系**：TraceRL 依赖模型自身的推理轨迹进行优化，但若初始模型的轨迹质量较差（如随机猜测），RL 是否仍能有效改进？论文未探索冷启动场景下的轨迹自举（trajectory bootstrapping）问题。
2. **多轮推理与长程依赖**：当前实验主要关注单轮 CoT 推理，TraceRL 在多轮对话、工具调用等需要跨轮轨迹优化的场景中是否有效，尚待验证。
3. **与 AR 模型 RL 方法的可迁移性**：TraceRL 的轨迹感知设计是否可反向迁移至自回归模型的 RL 微调（如 GRPO），形成统一框架，是一个有意义的理论问题。
4. **过程奖励的质量敏感性**：扩散价值模型支持过程奖励，但过程奖励的标注质量对训练稳定性和最终性能的影响未进行消融分析。GAE 参数 $(\gamma, \lambda)$ 的选择在实验中显示为 $(0.99, 1)$ 最优（Table 5），但其最优性是否依赖任务和模型规模，缺乏系统验证。

### 4. 知识库定位总结

TraceRL 在 DLM 后训练谱系中占据**轨迹感知 RL** 这一新兴节点，填补了从“随机掩码微调”到“推理轨迹对齐优化”的方法空白。其核心贡献在于证明了**训练目标与推理轨迹的显式对齐**是提升 DLM 推理能力的关键杠杆。当前证据强度较高（Table 2 的多基准验证、Figure 5 的方差分析、Table 3 的块大小扩展实验），但适用边界和开放问题表明该方法仍处于实验室验证阶段，距离通用部署尚有距离。

## 原文 PDF

![[paperPDFs/ICLR_2026/Revolutionizing_Reinforcement_Learning_Framework_for_Diffusion_Large_Language_Models.pdf]]
