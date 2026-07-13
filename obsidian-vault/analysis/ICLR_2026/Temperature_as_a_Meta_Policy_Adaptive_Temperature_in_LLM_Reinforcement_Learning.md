---
title: "Temperature as a Meta-Policy: Adaptive Temperature in LLM Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Temperature_as_a_Meta_Policy_Adaptive_Temperature_in_LLM_Reinforcement_Learning.pdf
project_link: null
code_link: null
openreview_forum_id: AoTHU2OmS6
aliases:
- TTAMPO
- TAMPATLRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "可学习的元策略 π(T) 控制采样温度的选择，通过轨迹反馈动态调整温度分布。"
primary_logic: "每条轨迹都隐含地编码了使其似然最大化的“首选温度”，通过重用内循环的轨迹计算温度特定优势，可以无额外采样地在线更新温度元策略，使温度与策略优化目标对齐。"
claims:
- "TAMPO 在五个数学推理基准上的平均 Pass@1 和 Pass@8 均优于所有基线（固定温度和启发式调度 GRPO）。"
- "高优势轨迹与低优势轨迹的似然最优温度聚集在不同值，表明存在更能产生高奖励轨迹的最优温度区间。"
- "轨迹对数似然关于温度是单峰的，可以通过调整温度来增加特定轨迹的生成概率。"
- "Avg. over AIME24, MATH-500, AMC23, Minerva, OlympiadBench 上 Pass@1 = 44.5 (TAMPO)"
---

# Temperature as a Meta-Policy: Adaptive Temperature in LLM Reinforcement Learning

> [!tip] 核心洞察
> 每条轨迹都隐含地编码了使其似然最大化的“首选温度”，通过重用内循环的轨迹计算温度特定优势，可以无额外采样地在线更新温度元策略，使温度与策略优化目标对齐。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 温度作为元策略：大语言模型强化学习中的自适应温度控制 |
| 英文题名 | Temperature as a Meta-Policy: Adaptive Temperature in LLM Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=AoTHU2OmS6) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | TAMPO (Temperature Adaptive Meta Policy Optimization) |
| Dataset | Avg. over AIME24, MATH-500, AMC23, Minerva, OlympiadBench, ECQA (CommonsenseQA) |

> [!tip] 效果简介
> - Avg. over AIME24, MATH-500, AMC23, Minerva, OlympiadBench 上，Pass@1 为 44.5 (TAMPO)，对比 42.6 (GRPO T_s=1.2)，变化 +1.9。
> - Avg. over AIME24, MATH-500, AMC23, Minerva, OlympiadBench 上，Pass@8 为 63.8 (TAMPO)，对比 62.1 (GRPO T_s=1.2)，变化 +1.7。
> - ECQA (CommonsenseQA) 上，Pass@1 为 76.12 (TAMPO)，对比 75.07 (GRPO)，变化 +1.05。

## 概要

在大语言模型（LLM）的强化学习（RL）微调中，采样温度是控制策略探索-利用平衡的关键超参数。现有方法通常采用固定温度或简单的启发式调度（如从 0.9 线性增加到 1.5），无法适应训练过程中动态变化的探索需求，导致策略优化受限。本文提出 **TAMPO（Temperature Adaptive Meta Policy Optimization）**，将温度建模为一个可学习的元策略，通过轨迹反馈在线自适应地调整温度分布，无需额外采样开销。

TAMPO 的核心洞见在于：每条轨迹都隐含地编码了一个使其似然最大化的“首选温度”。通过重用内循环中已生成的轨迹，计算其在不同候选温度下的似然，并与轨迹优势信号结合，即可获得温度特定的优势估计。基于此，元策略将概率质量向产生高优势轨迹的温度方向倾斜，同时抑制效果不佳的温度，从而实现温度与策略优化目标的动态对齐。

在五个数学推理基准（AIME24、MATH-500、AMC23、Minerva、OlympiadBench）上，TAMPO 的平均 Pass@1 达到 44.5，平均 Pass@8 达到 63.8，均优于所有固定温度和启发式调度基线（Table 1）。在常识推理任务 ECQA 上，TAMPO 同样取得一致的性能提升（Table 4）。消融实验表明，EMA 系数 α=0.05 和元策略的 Top-p 采样（p=0.7）是实现稳定自适应的关键配置（Table 2, Table 3）。TAMPO 仅额外维护一个轻量级的温度优势列表，几乎不增加计算开销，且推理时丢弃元策略，保持了部署的简洁性。

### 温度在大语言模型生成中的核心作用

大语言模型（LLM）的生成过程通常通过温度参数 $T$ 控制输出分布的平滑程度。给定logits $z(o_{i,t} \mid s_{i,t})$，温度缩放后的采样策略为：

$$\pi_{\theta, T}(o_{i,t} \mid s_{i,t}) = \frac{\exp(z(o_{i,t} \mid s_{i,t}) / T)}{\sum_{o_{i,t}'} \exp(z(o_{i,t}' \mid s_{i,t}) / T)}$$

温度直接决定了探索（exploration）与利用（exploitation）的平衡：低温度使分布更尖锐，倾向于选择高概率token，促进利用；高温度使分布更平坦，增加低概率token的采样机会，促进探索。

### 强化学习训练中的温度困境

在大语言模型的强化学习（RL）训练中，这一平衡尤为关键。训练过程需要探索多样化的生成轨迹以发现高奖励路径，同时又要利用已学到的有效策略以稳定提升性能。然而，现有方法对温度的处理存在明显缺口：

- **固定温度**：大多数RL训练流程（如GRPO）采用固定的采样温度（例如 $T_s = 0.9$ 或 $T_s = 1.2$），无法适应训练过程中动态变化的探索需求。
- **启发式调度**：部分工作尝试手动设计温度调度策略（如从0.9线性增加到1.5），但这类调度缺乏对训练状态和轨迹质量的在线反馈，本质上是盲目的。

这种静态或启发式的温度控制，使得策略优化无法根据实际训练动态自适应地调整探索-利用平衡，成为制约LLM强化学习效果的一个瓶颈。

### 核心洞察：轨迹隐含温度偏好

本文的核心洞察在于：**每条生成轨迹都隐含地编码了使其似然最大化的“首选温度”**。具体而言，对于一条轨迹 $\tau_i$，其在温度 $T$ 下的平均对数似然为：

$$\ell_T(\tau_i) = \frac{1}{|\tau_i|} \sum_{t=1}^{|\tau_i|} \log \pi_{\theta, T}(o_{i,t} \mid s_{i,t})$$

轨迹对数似然关于温度呈现单峰性质（见Figure 2），这意味着存在一个特定的温度值使该轨迹的生成概率最大化。更重要的是，高优势轨迹与低优势轨迹的似然最优温度聚集在不同的温度区间（见Figure 4），表明存在更能产生高奖励轨迹的最优温度区间。

### 研究动机

基于上述观察，本文提出将温度本身视为一个可学习的**元策略（meta-policy）**，通过轨迹反馈动态调整温度分布。核心思路是：利用内循环中已生成的轨迹，计算其在各候选温度下的似然，结合轨迹优势信号推导温度特定优势，从而在不增加额外采样开销的前提下，在线更新温度元策略，使其与策略优化目标对齐。这一设计将温度从固定的超参数提升为训练过程中自适应演化的控制变量，有望突破现有方法的探索-利用平衡瓶颈。

## 核心方法与创新机理

TAMPO 的核心创新在于将采样温度从固定的超参数或启发式调度提升为**可学习的元策略（meta-policy）**，使其能够在线、自适应地响应训练过程中动态变化的探索-利用需求。

### 1. 温度作为元策略：从固定超参数到可学习控制变量

在基线方法（如 GRPO）中，采样温度通常被设定为固定值（如 $T_s=0.9$、$1.2$、$1.5$）或遵循预定义的启发式调度（如从 0.9 线性增加到 1.5）。这种方式隐含地假设了最优温度在训练过程中保持不变或单调变化，无法根据策略的实际优化状态进行动态调整。

TAMPO 改变了这一范式：**采样温度不再是一个外部给定的常数，而是由元策略 $\pi(T)$ 在离散候选集 $\mathcal{T} = \{0.6, 0.7, \ldots, 1.5\}$ 上采样得到的决策变量**。元策略本身通过轨迹反馈在线更新，使温度选择与策略优化目标直接对齐。

### 2. 零额外采样的温度优势估计

实现温度自适应的关键瓶颈在于如何评估不同温度的价值而不引入额外计算开销。TAMPO 的核心洞察是：**每条轨迹都隐含地编码了使其似然最大化的“首选温度”**。通过重用内循环（GRPO）已经生成的轨迹，计算每条轨迹在每个候选温度下的对数似然，并利用轨迹优势 $A_i$ 进行加权，即可得到温度特定的优势信号：

$$\mathcal{A}_i^{(T_k)} = \hat{\ell}_{T_k}(\tau_i) \cdot A_i$$

这一公式的因果逻辑是：若一条轨迹具有正优势（$A_i > 0$），则使其生成概率最大化的温度应当被强化；反之，若轨迹具有负优势（$A_i < 0$），则该温度应被抑制。Figure 4 的实证分析验证了这一假设：高优势轨迹与低优势轨迹的似然最优温度聚集在不同区间，表明存在更能产生高奖励轨迹的最优温度区域。

由于轨迹似然计算仅涉及对已生成 token 的 logit 重新缩放（无需重新采样），TAMPO 的元策略更新几乎不引入额外计算开销。元策略本身仅维护一个温度优势列表，在推理时被完全丢弃。

### 3. 基于反馈的自适应探索-利用平衡

传统方法通过固定温度或熵正则化间接控制探索-利用平衡，缺乏在线反馈机制。TAMPO 通过以下机制实现了基于反馈的自适应平衡：

- **批聚合与 EMA 平滑**：将批次内所有轨迹的温度特定优势聚合后，通过指数移动平均（$\alpha=0.05$）平滑，在降低方差和保持响应性之间取得平衡。
- **最小-最大归一化**：对平滑优势进行归一化得到合法的概率分布 $\pi_s(T_k)$，直接作为下一轮温度采样的元策略。
- **核采样探索**：从元策略分布中采样温度时采用 top-p 采样（$p=0.7$），在温度空间引入适度的分布式探索，避免过早收敛到次优温度。

### 4. 与基线的本质区别

| 维度 | 基线（GRPO 固定/调度温度） | TAMPO |
|------|---------------------------|-------|
| 温度设定 | 外部给定，固定或启发式调度 | 可学习的元策略，在线动态更新 |
| 探索-利用控制 | 间接控制，无反馈信号 | 基于轨迹优势的直接反馈控制 |
| 额外计算开销 | 无 | 极低（仅复用已有轨迹计算似然） |
| 温度空间探索 | 无 | 核采样实现分布式温度探索 |

实验表明，TAMPO 在五个数学推理基准上的平均 Pass@1（44.5）和 Pass@8（63.8）均优于所有固定温度和启发式调度基线，验证了自适应温度元策略的有效性。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_AoTHU2OmS6/figures/001_Figure_1.jpg]]
*Figure 1: Overview of Temperature Adaptive Meta Policy Optimization (TAMPO). The framework operates through a hierarchical two-loop process. In the inner loop, the LLM policy is optimized with critic-free RL (e.g., GRPO) using rollouts sampled at the temperature chosen by the metapolicy. In the outer loop, the meta-policy is updated by evaluating trajectory likelihoods under virtual temperatures, deriving temperature-specific advantages ( $\mathcal { A } _ { i } ^ { ( T _ { k } ) } = \hat { \ell } _ { T _ { k } } ( \tau _ { i } ) \cdot \boldsymbol { A } _ { i }$ for trajectory $\tau _ { i }$ w.r.t. virtual temperature $T _ { k }$ ) , and reinforcing those that yield high-advantage rollouts (see §3). This d...

TAMPO 的核心设计是将采样温度从固定的超参数提升为一个可学习的**元策略（meta-policy）**，通过一个分层双循环架构，使温度能够根据训练过程中的轨迹反馈在线自适应调整。该框架由内循环和外循环两个协同工作的模块组成，整体流程如 Figure 1 所示。

### 内循环：LLM 策略优化

内循环负责主体任务——优化大语言模型的策略参数 $\theta$。在每一轮迭代中，元策略 $\pi(T)$ 首先从一个离散的候选温度集合 $\mathcal{T} = \{T_1, \ldots, T_K\}$ 中采样一个温度 $T$，然后 LLM 策略 $\pi_{\theta, T}$ 在该温度下对一批提示（prompts）进行 rollout 采样，生成多条轨迹。这些轨迹通过 critic-free 的强化学习算法（如 GRPO）进行优势估计和策略更新。

GRPO 的轨迹级优势 $A_i$ 通过组内奖励标准化计算：

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, \dots, r_G\})}{\operatorname{std}(\{r_1, \dots, r_G\})}$$

温度 $T$ 通过缩放 token logits 来控制采样分布的平滑程度：

$$\pi_{\theta, T}(o_{i,t} \mid s_{i,t}) = \frac{\exp(z(o_{i,t} \mid s_{i,t}) / T)}{\sum_{o_{i,t}'} \exp(z(o_{i,t}' \mid s_{i,t}) / T)}$$

内循环的输出包括更新后的策略参数 $\theta$，以及为外循环提供核心反馈信号的轨迹及其奖励。

### 外循环：元策略更新

外循环是 TAMPO 的核心创新所在，它**完全复用内循环已生成的轨迹**，无需额外采样即可更新温度元策略。这一设计的关键洞察在于：每条轨迹都隐含地编码了一个使其似然最大化的“首选温度”。

具体而言，外循环对每条轨迹 $\tau_i$，在所有候选温度 $T_k \in \mathcal{T}$ 下重新计算其对数似然：

$$\ell_T(\tau_i) = \frac{1}{|\tau_i|} \sum_{t=1}^{|\tau_i|} \log \pi_{\theta, T}(o_{i,t} \mid s_{i,t})$$

经过 sparsemax 归一化后，得到 $\hat{\ell}_{T_k}(\tau_i)$，代表轨迹 $\tau_i$ 对温度 $T_k$ 的相对偏好强度。

随后，将归一化似然与内循环的轨迹优势 $A_i$ 相乘，得到**温度特定优势**：

$$\mathcal{A}_i^{(T_k)} = \hat{\ell}_{T_k}(\tau_i) \cdot A_i$$

这一操作的直觉是：若一条轨迹获得了高优势（$A_i > 0$），则其似然最优的温度应被“奖励”；反之，若轨迹为低优势（$A_i < 0$），则该温度应被“惩罚”。通过这种方式，元策略将概率质量向能够产生高优势轨迹的温度区间集中。

### 聚合与平滑

为获得稳定的温度优势估计，外循环首先在批次内聚合所有轨迹的温度特定优势：

$$\mathcal{A}_{\mathcal{B}}^{(T_k)} = \frac{1}{|\mathcal{B}| G} \sum_{b=1}^{|\mathcal{B}|} \sum_{i=1}^{G} \mathcal{A}_{b,i}^{(T_k)}$$

然后通过指数移动平均（EMA）平滑跨步的波动：

$$\bar{\mathcal{A}}_s^{(T_k)} = (1 - \alpha) \bar{\mathcal{A}}_{s-1}^{(T_k)} + \alpha \mathcal{A}_{\mathcal{B}}^{(T_k)}$$

其中 $\alpha = 0.05$ 在降低方差与保持响应性之间取得了最佳平衡（见 Table 2 消融实验）。

最后，对 EMA 平滑后的优势进行最小-最大归一化，得到合法的元策略概率分布：

$$\pi_s(T_k) = \frac{\tilde{A}_s^{(T_k)}}{\sum_{j=1}^{K} \tilde{A}_s^{(T_j)}}, \quad \tilde{A}_s^{(T_k)} = \frac{\bar{A}_s^{(T_k)} - \min_j \bar{A}_s^{(T_j)}}{\max_j \bar{A}_s^{(T_j)} - \min_j \bar{A}_s^{(T_j)}}$$

### 温度采样与推理

在下一轮内循环中，元策略通过 top-p 核采样（$p=0.7$）从 $\pi_s(T)$ 中抽取温度，适度的分布式探索有助于元策略发现更优的温度区间（Table 3 消融实验证实 $p=0.7$ 优于贪婪解码和其他 $p$ 值）。推理阶段，元策略被完全丢弃，模型仅使用训练好的策略参数进行解码，不引入额外开销。

### 输入输出流总结

整个 TAMPO 框架的输入输出流可概括为：

1. **输入**：训练提示集 $\mathcal{D}$，候选温度集合 $\mathcal{T}$，基模型参数 $\theta_0$
2. **内循环**：元策略采样温度 $T$ → LLM 在该温度下生成轨迹 → 计算奖励与 GRPO 优势 → 更新策略参数 $\theta$
3. **外循环**：复用内循环轨迹 → 计算各候选温度下的轨迹似然 → 推导温度特定优势 → EMA 平滑与归一化 → 更新元策略 $\pi(T)$
4. **输出**：优化后的策略参数 $\theta$，元策略在训练后丢弃

该框架的轻量性体现在元策略仅维护一个温度优势列表（$K$ 个标量），几乎不增加训练计算开销，且无需为温度适应生成额外轨迹。

TAMPO 将温度视为一个可学习的元策略，通过分层双循环架构实现采样温度的在线自适应。其核心由内循环策略优化与外循环元策略更新两个模块构成，二者共享轨迹数据，无需额外采样。

### 内循环：LLM 策略优化

内循环负责在元策略选定的温度下优化 LLM 策略参数 $\theta$。给定一个问题 $q$，元策略 $\pi$ 从候选温度集合 $\mathcal{T} = \{T_1, \ldots, T_K\}$ 中采样一个温度 $T$，策略模型 $\pi_{\theta,T}$ 在该温度下生成 $G$ 条轨迹，并计算每条轨迹的奖励 $r_i$。

轨迹优势通过组内标准化计算（GRPO 方式）：

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, \dots, r_G\})}{\operatorname{std}(\{r_1, \dots, r_G\})}$$

其中 $A_i$ 表示轨迹 $\tau_i$ 相对于同组其他轨迹的相对优势。策略 $\pi_{\theta,T}$ 在温度 $T$ 下对 token $o_{i,t}$ 的采样分布为：

$$\pi_{\theta, T}(o_{i,t} \mid s_{i,t}) = \frac{\exp(z(o_{i,t} \mid s_{i,t}) / T)}{\sum_{o_{i,t}'} \exp(z(o_{i,t}' \mid s_{i,t}) / T)}$$

温度 $T$ 通过对 logits $z(\cdot)$ 的缩放控制采样的随机性：低温度使分布更尖锐（偏向利用），高温度使分布更平坦（偏向探索）。内循环使用 critic-free RL（如 GRPO）更新 $\theta$，最大化期望优势并施加 KL 正则化。

### 外循环：元策略更新

外循环重用内循环产生的轨迹，在不增加额外采样开销的前提下更新温度元策略。其核心洞察是：每条轨迹在不同温度下的对数似然编码了该轨迹的“首选温度”，通过将轨迹优势与温度特定似然结合，可以评估每个候选温度对高奖励轨迹生成的贡献。

**轨迹似然计算。** 对于每条轨迹 $\tau_i$ 和每个候选温度 $T_k$，计算轨迹在该温度下的平均对数似然：

$$\ell_{T_k}(\tau_i) = \frac{1}{|\tau_i|} \sum_{t=1}^{|\tau_i|} \log \pi_{\theta, T_k}(o_{i,t} \mid s_{i,t})$$

该似然关于温度呈单峰性质（见 Figure 2），意味着存在一个似然最优温度，通过调整温度可以增加特定轨迹的生成概率。为消除不同温度下似然尺度差异的影响，对似然进行 sparsemax 归一化得到 $\hat{\ell}_{T_k}(\tau_i)$。

**温度特定优势。** 将归一化似然与轨迹优势相乘，得到温度 $T_k$ 对轨迹 $\tau_i$ 的优势贡献：

$$\mathcal{A}_i^{(T_k)} = \hat{\ell}_{T_k}(\tau_i) \cdot A_i$$

这一设计的直觉在于：正优势轨迹（$A_i > 0$）会强化其似然最优温度，负优势轨迹（$A_i < 0$）则惩罚其似然最优温度，从而将概率质量推向更可能产生高奖励轨迹的温度区间。Figure 4 的实验证据表明，高优势与低优势轨迹的似然最优温度确实聚集在不同区间，验证了温度自适应的必要性。

**批聚合与 EMA 平滑。** 在一个批次 $\mathcal{B}$ 内聚合所有轨迹的温度特定优势：

$$\mathcal{A}_{\mathcal{B}}^{(T_k)} = \frac{1}{|\mathcal{B}| G} \sum_{b=1}^{|\mathcal{B}|} \sum_{i=1}^{G} \mathcal{A}_{b,i}^{(T_k)}$$

为降低批次间的方差，使用指数移动平均（EMA）平滑温度优势估计：

$$\bar{\mathcal{A}}_s^{(T_k)} = (1 - \alpha) \bar{\mathcal{A}}_{s-1}^{(T_k)} + \alpha \mathcal{A}_{\mathcal{B}}^{(T_k)}$$

其中 $\alpha$ 控制平滑强度。消融实验（Table 2）表明 $\alpha=0.05$ 在降低方差与保持响应性之间取得最佳平衡。

**元策略归一化与采样。** 对 EMA 平滑后的优势进行最小-最大归一化，得到合法的概率分布：

$$\pi_s(T_k) = \frac{\tilde{A}_s^{(T_k)}}{\sum_{j=1}^{K} \tilde{A}_s^{(T_j)}}, \quad \tilde{A}_s^{(T_k)} = \frac{\bar{A}_s^{(T_k)} - \min_j \bar{A}_s^{(T_j)}}{\max_j \bar{A}_s^{(T_j)} - \min_j \bar{A}_s^{(T_j)}}$$

下一轮内循环的温度从 $\pi_s(T_k)$ 中使用 top-p 核采样（$p=0.7$）抽取，以在温度探索与利用之间保持适度平衡。消融实验（Table 3）证实 $p=0.7$ 优于贪婪解码（$p=0$）及更大或更小的 $p$ 值。

### 计算开销

元策略模型极其轻量：仅维护一个长度为 $K$ 的温度优势列表，训练时几乎不引入额外计算开销，推理时直接丢弃。所有实验均使用相同的基模型、训练数据、训练步数和超参数，TAMPO 的增益完全来自温度的自适应调度。

## 实验与关键发现

### 核心瓶颈与因果机制

在大语言模型的强化学习（RL）训练中，采样温度 $T$ 直接控制着策略的探索-利用平衡：低温倾向于利用已有知识，高温则鼓励探索。然而，现有方法通常将温度设为固定值或采用启发式调度，无法响应训练过程中动态变化的探索需求。TAMPO 的核心洞察在于：**每条轨迹都隐含地编码了使其似然最大化的“首选温度”**（Figure 2 展示了轨迹似然关于温度的单峰性质），通过重用内循环的轨迹计算温度特定优势，可以在不产生额外采样开销的前提下，在线更新温度元策略，使温度选择与策略优化目标对齐。

Figure 4 给出了这一机制的经验证据：在三种固定采样温度下，高优势轨迹（$A > 0$）与低优势轨迹（$A < 0$）的似然最优温度分布呈现明显分离，表明存在更能产生高奖励轨迹的最优温度区间。TAMPO 正是通过元策略 $\pi(T)$ 将概率质量持续导向这些高优势温度区间，同时抑制低效温度。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_AoTHU2OmS6/figures/011_Figure_4.jpg]]
*Figure 4: Distribution of trajectory likelihood-optimal temperatures under three fixed training temperatures, respectively. Green curve corresponds to the likelihood-optimal temperatures of positiveadvantage trajectories ( A > 0 ) , red curve to negative-advantage trajectories ( A \< 0 ) , and blue curve to the sampled fixed temperature. Figure 5: System prompt for the policy model*

### 主要结果

Table 1 报告了 TAMPO 与各基线在五个数学推理基准上的对比。TAMPO 使用 DeepSeek-R1-Distill-Qwen-1.5B 作为基模型，在 open-s1 数据集上训练 200 步，与所有 GRPO 变体保持完全相同的训练配置。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_AoTHU2OmS6/figures/003_Table_1.jpg]]
*Table 1: Comparison of TAMPO with baselines on math reasoning using 1.5B models, evaluated with Pass@1 and Pass@8. DS-Qwen-1.5B denotes DeepSeek-R1-Distill-Qwen-1.5B (Guo et al., 2025), which serves as the base model for all training on the open-s1 dataset. GRPO ( T _ { s } : 0 . 9 ) indicates a baseline trained with GRPO at a fixed sampling temperature of 0.9. The maximum response length is set to 6k tokens. Best results are in bold, and second-best results are underlined*

**数学推理综合表现**：TAMPO 在五个基准上的平均 Pass@1 达到 44.5，优于最佳固定温度基线 GRPO ($T_s=1.2$) 的 42.6（+1.9）；平均 Pass@8 达到 63.8，优于 GRPO ($T_s=1.2$) 的 62.1（+1.7）。值得注意的是，TAMPO 同时超越了启发式调度基线 GRPO ($T_s=0.9 \to 1.5$) 的 43.3（Pass@1）和 62.6（Pass@8），表明在线学习的温度适应比预设的线性调度更有效。

**领域泛化**：Table 4 展示了 TAMPO 在常识推理基准 ECQA 上的迁移结果。使用 Qwen2.5-3B-Instruct 作为基模型时，TAMPO 的 Pass@1 达到 76.12%，相比 GRPO 的 75.07% 提升了 1.05 个百分点，验证了该方法在数学推理之外的泛化能力。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_AoTHU2OmS6/figures/007_Table_4.jpg]]
*Table 4: ECQA results evaluated with Pass@1 and Pass@8*

### 消融实验

**EMA 系数 $\alpha$ 的影响**（Table 2）：指数移动平均系数控制着温度优势估计的平滑程度。$\alpha=0.05$ 在降低方差和保持响应性之间取得了最佳平衡，平均 Pass@1 达到 44.5；$\alpha=0.01$ 因平滑过强导致响应迟缓，性能降至 41.6；$\alpha=0.10$ 则因平滑不足引入过多噪声，性能为 43.6。这一结果表明，温度元策略的更新需要适度的历史平滑来稳定训练。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_AoTHU2OmS6/figures/004_Table_2.jpg]]
*Table 2: Influence of the EMA coefficient α for our TAMPO. We report the performance on Pass@1*

**元策略采样策略的影响**（Table 3）：TAMPO 从元策略分布中采样温度时采用核采样（Nucleus Sampling）。Top-p=0.7 在探索与利用之间取得了最优平衡，平均 Pass@1 达到 44.5；贪婪解码（p=0）因缺乏探索而性能最低（40.9）；过大的 p=0.9（43.0）和过小的 p=0.5（42.2）均导致性能下降。这说明温度选择本身也需要适度的分布式探索，而非始终选择当前最优温度。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_AoTHU2OmS6/figures/005_Table_3.jpg]]
*Table 3: Influence of sampling strategy on meta-policy. We report the performance on Pass@1*

### 公平性与计算开销

所有方法均使用相同的基模型、训练数据集、训练步数、学习率调度、批大小和 rollout 数。TAMPO 仅额外维护一个轻量级的温度优势列表（候选温度数 $K=10$），元策略更新完全重用内循环的已有轨迹，不产生额外采样。推理时元策略被丢弃，因此不增加推理开销。

### 局限与待验证方向

1. **模型规模**：当前实验仅在 1.5B 和 3B 参数量的模型上进行，更大规模模型上的效果未知。
2. **候选温度离散化**：候选温度集合 $\{0.6, 0.7, \dots, 1.5\}$ 是预定义的，最优温度可能不在集合内，且手动设定可能引入偏差。
3. **RL 算法兼容性**：TAMPO 目前集成于 GRPO 框架，与其他 RL 算法（如 PPO）的兼容性未经验证。
4. **任务覆盖**：仅在数学推理和常识推理任务上测试，未在代码生成、安全对齐等领域验证。

## 定位与知识库关联

### 1. 与现有温度控制策略的关系

在大语言模型强化学习（LLM RL）的实践中，采样温度长期被视为一个需要手动设定的静态超参数。主流做法可归为三类：

1. **固定温度训练**：在整个训练周期内维持一个恒定的温度值。例如，**GRPO** (Shao et al., 2024; Guo et al., 2025) 的常见配置包括 $T_s = 0.9$（低温度，偏向利用）、$T_s = 1.2$（中等温度）和 $T_s = 1.5$（高温度，偏向探索）。这种方法的根本缺陷在于，训练过程中策略的成熟度和对探索的需求是动态变化的，单一温度无法在全周期内同时兼顾早期探索与后期收敛。

2. **启发式温度调度**：通过预定义的规则调整温度，如从 $T_s = 0.9$ 线性增加到 $T_s = 1.5$。**GRPO ($T_s=0.9 \to 1.5$)** 在 Table 1 中的平均 Pass@1 为 42.6，与固定温度最优基线持平，表明静态调度虽然引入了变化，但缺乏对训练动态的反馈感知，本质上仍是一种开环控制。

3. **熵正则化**：通过在损失函数中加入熵奖励项间接影响探索程度。这类方法（如 PPO 中的 entropy bonus）通过策略本身的熵来调节探索，但温度对采样分布的影响是全局性的——它不仅影响分布的平坦程度，还改变了不同 token 之间的相对概率排序——而熵正则化仅在局部调整策略的确定性，两者作用于不同层面。

TAMPO 的核心差异在于将温度从“被调节的超参数”提升为“可学习的元策略”。它不预设温度的变化轨迹，而是通过在线反馈——即轨迹在候选温度下的似然与该轨迹实际获得的优势——来动态更新温度的概率分布。这使温度控制从开环调度转变为闭环自适应。

### 2. 与分层强化学习的关系

TAMPO 的双循环架构在形式上与分层强化学习（Hierarchical RL）有相似之处：外循环选择温度（高层动作），内循环在该温度下优化策略（底层执行）。但存在两个关键区别：

- **无额外采样成本**：传统分层 RL 的高层策略需要独立的 rollout 来评估其决策质量。TAMPO 通过复用内循环已生成的轨迹，计算其在所有候选温度下的似然和温度特定优势（$\mathcal{A}_i^{(T_k)} = \hat{\ell}_{T_k}(\tau_i) \cdot A_i$，Eq. 9），使元策略更新无需任何额外生成。
- **极轻量的元策略参数**：元策略仅维护一个长度为 $K$（候选温度数，默认 $K=10$）的优势列表，通过指数移动平均（EMA，Eq. 11）和最小-最大归一化（Eq. 12）更新。推理时元策略被完全丢弃，不引入任何推理开销。

### 3. 适用边界

基于现有实验证据，TAMPO 的适用边界可初步界定如下：

- **已验证的任务域**：数学推理（AIME24、MATH-500、AMC23、Minerva、OlympiadBench）和常识推理（ECQA）。在数学推理上，TAMPO 在 1.5B 模型上的平均 Pass@1 达到 44.5，相比最优固定温度基线提升 1.9 个百分点（Table 1）；在 ECQA 上 Pass@1 达到 76.12%，相比 GRPO 提升 1.05 个百分点（Table 4）。
- **已验证的模型规模**：1.5B（DeepSeek-R1-Distill-Qwen-1.5B）和 3B（Qwen2.5-3B-Instruct）。更大规模模型上的效果尚未验证。
- **已验证的 RL 框架**：仅与 GRPO 集成。GRPO 的 critic-free 特性（通过组内标准化计算优势）恰好与 TAMPO 的轨迹复用机制契合，但与其他 RL 算法（如 PPO、REINFORCE）的兼容性未经验证。
- **候选温度集合**：预定义的离散集合 $\{0.6, 0.7, \dots, 1.5\}$，步长 0.1。最优温度若落在集合之外（如需要 $T=0.65$ 或 $T=1.55$），当前方法无法精确表达。此外，该集合对所有任务和训练阶段保持不变，缺乏自适应扩展能力。

### 4. 局限与开放问题

**已识别的局限**：

1. **离散温度空间的粒度限制**：候选温度集合是手动预定义的。Figure 4 显示正优势轨迹与负优势轨迹的似然最优温度聚集在不同区间，但当前离散化可能无法精确匹配最优温度，且不同任务可能需要不同的温度范围和粒度。

2. **模型规模验证不足**：所有实验均在 1.5B 和 3B 参数模型上完成。更大规模模型（如 7B、70B）的采样分布特性可能不同，温度对探索-利用平衡的影响机制也可能发生变化。

3. **任务域泛化性待验证**：仅在数学推理和常识推理上测试。代码生成、安全对齐、多轮对话等场景中，温度的作用机制和最优调度策略可能显著不同。

4. **与策略熵正则化的交互未探索**：TAMPO 通过元策略控制温度来调节探索，而许多 RL 方法同时使用熵正则化。两者的共同作用是否会相互干扰或产生协同效应，尚无实验证据。

**待解决的开放问题**：

- 能否将温度空间从离散扩展到连续，通过可微分的方式（如重参数化梯度）直接优化温度？这可以消除离散化的粒度限制。
- 候选温度集合能否根据训练进程和任务特性自动调整？例如，在训练早期自动扩展高温区域以增强探索，后期收窄至低温区域以促进收敛。
- 在更复杂的奖励结构（如基于人类偏好的 RLHF）中，温度元策略是否仍然有效？奖励信号的稀疏性和噪声特性可能与数学推理中的规则奖励存在本质差异。
- 温度元策略与策略本身的熵正则化是否存在冗余或冲突？能否在统一的优化框架下联合学习？

## 原文 PDF

![[paperPDFs/ICLR_2026/Temperature_as_a_Meta_Policy_Adaptive_Temperature_in_LLM_Reinforcement_Learning.pdf]]
