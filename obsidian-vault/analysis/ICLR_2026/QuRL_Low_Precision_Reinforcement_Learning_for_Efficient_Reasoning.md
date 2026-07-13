---
title: "QuRL: Low-Precision Reinforcement Learning for Efficient Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/QuRL_Low_Precision_Reinforcement_Learning_for_Efficient_Reasoning.pdf
project_link: null
code_link: null
openreview_forum_id: eG0bpCwdKn
aliases:
- QQRL
- QuRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "对旧Actor模型进行量化（INT8/FP8）以加速rollout，同时通过自适应裁剪范围（ACR）和更新感知量化（UAQ）保持训练稳定性和策略梯度质量。"
primary_logic: "采用解耦PPO目标将行为策略（量化Actor）与近端策略（全精度Actor）分离，并引入自适应裁剪范围以防止因量化引起的策略分歧导致的训练崩溃；同时利用线性层的不变缩放属性放大权重更新相对于量化误差的信噪比，使量化模型能够有效跟踪RL训练动态。"
claims:
- "直接使用量化rollout的GRPO目标导致训练奖励崩溃，token裁剪比例异常升高。"
- "在1000步训练后，行为策略与近端策略间的KL散度从0.002增加到0.025（12倍），导致训练不稳定。"
- "权重量化误差远大于RL步间的权重更新量，尤其在训练初期，阻碍量化模型感知训练动态。"
- "QuRL w/ UAQ在DeepScaleR五个推理任务上达到55.48%的平均准确率，超过全精度基线1.7%。"
---

# QuRL: Low-Precision Reinforcement Learning for Efficient Reasoning

> [!tip] 核心洞察
> 采用解耦PPO目标将行为策略（量化Actor）与近端策略（全精度Actor）分离，并引入自适应裁剪范围以防止因量化引起的策略分歧导致的训练崩溃；同时利用线性层的不变缩放属性放大权重更新相对于量化误差的信噪比，使量化模型能够有效跟踪RL训练动态。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | QuRL：面向高效推理的低精度强化学习 |
| 英文题名 | QuRL: Low-Precision Reinforcement Learning for Efficient Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=eG0bpCwdKn) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | QuRL (Quantized Reinforcement Learning) |
| Dataset | GSM8K, AIME 2024, DeepScaleR (5 tasks avg), Throughput (Inference Speed) |

> [!tip] 效果简介
> - GSM8K 上，Accuracy (%) 为 53.55 (QuRL INT8)，对比 55.35 (RL BF16) | 48.78 (INT8 RL)，变化 -1.80 vs BF16, +4.77 vs INT8 RL。
> - AIME 2024 上，Avg@1 为 36.66 (QuRL w/o UAQ FP8)，对比 0.00 (INT8 RL)，变化 +36.66。
> - DeepScaleR (5 tasks avg) 上，Avg@32 (%) 为 55.48 (QuRL w/ UAQ INT8)，对比 56.40 (RL BF16) | 52.31 (INT8 RL)，变化 -0.92 vs BF16, +3.17 vs INT8 RL。

## 概要

在基于可验证奖励的强化学习（RL）训练大语言模型（LLM）推理能力时，rollout阶段因自回归解码特性消耗约70%的训练时间，成为制约训练效率的核心瓶颈。直接对旧Actor模型进行低精度量化（如INT8/FP8）以加速rollout是一种直观方案，但会引入策略分歧和梯度估计偏差，导致训练奖励崩溃（Figure 2）。QuRL（Quantized Reinforcement Learning）针对这一矛盾，提出了一套系统性的低精度RL训练框架，其核心思路是：**将行为策略（量化Actor）与近端策略（全精度Actor）解耦**，并通过自适应裁剪范围（ACR）和更新感知量化（UAQ）两项关键技术，在保持训练稳定性的同时实现显著的推理加速。

具体而言，QuRL采用解耦PPO目标，将rollout阶段的行为策略从全精度旧Actor替换为量化旧Actor，而梯度计算中的近端策略仍保持全精度，从而避免量化噪声直接污染策略梯度。针对量化导致的行为-近端策略分歧（KL散度在1000步内从0.002增至0.025，增长12倍），QuRL引入自适应裁剪范围（ACR），根据近端-行为策略比率动态调整裁剪下界，防止因量化引起的策略崩溃。此外，QuRL提出更新感知量化（UAQ），利用线性层Q/K/V投影的不变缩放属性，在RL训练前对权重施加缩放因子$s>1$，同时放大权重更新幅度并降低量化误差，产生$s^2$级的信噪比提升，使量化模型能够有效跟踪RL训练动态。

在实验验证方面，QuRL在多个推理基准上展现出接近全精度训练的精度水平，同时获得显著的加速收益。在DeepScaleR五个推理任务的综合评测中，INT8 QuRL（含UAQ）达到55.48%的平均准确率，超过全精度基线1.7%（Table 3）。在GSM8K任务上，INT8 QuRL准确率为53.55%，虽略低于BF16基线的55.35%，但较朴素INT8 RL的48.78%提升4.77个百分点（Table 1）。在AIME 2024上，朴素INT8 RL准确率为0%，而QuRL（不含UAQ的FP8版本）达到36.66%（Table 2）。加速方面，INT8量化在7B模型上带来20-30%的推理加速，在32B模型上可达70-90%（Figure 8）。QuRL方法可兼容PPO、GRPO、DAPO等多种RL算法，且其量化策略介于后训练量化（PTQ）与量化感知训练（QAT）之间——在每次rollout前进行一次量化，无需通过梯度显式优化量化性能。

QuRL的主要局限在于：FP8 KV缓存量化因推理引擎支持不完善而未能采用；与全精度训练相比仍存在约1-2%的精度差距；ACR和UAQ引入的额外超参数（截断常数$C$、缩放因子$s$）需针对不同任务调整。未来方向包括探索更低精度（如4-bit）下的稳定性、自动化超参数选择，以及在更大规模模型和在线RLHF场景下的扩展性验证。



### 推理增强学习中的效率瓶颈

基于可验证奖励的强化学习（RL）已成为提升大语言模型推理能力的核心范式。典型的训练流程包含两个阶段：**Rollout生成**——旧Actor模型自回归采样产生完整推理轨迹；**策略更新**——基于轨迹的奖励信号计算梯度并更新模型参数。在这两个阶段中，Rollout因其自回归解码的串行特性，消耗了约**70%的训练时间**，成为制约整体训练效率的首要瓶颈。

### 现有加速方案的局限

针对Rollout效率问题，模型量化是一种直观的加速手段——将旧Actor的权重和激活从BF16压缩至INT8或FP8，利用低精度计算提升推理吞吐。然而，直接将量化模型用于RL训练的Rollout面临两个根本性困难：

**训练崩溃与策略分歧。** 如图Figure 2所示，直接使用量化Actor进行Rollout的GRPO训练会导致奖励信号崩溃，token裁剪比例异常升高。其根源在于，量化引入的策略偏差会随时间累积：训练1000步后，行为策略（量化Actor）与近端策略（全精度Actor）之间的KL散度从0.002急剧增长至0.025（约**12倍**），如Figure 3(a)所示。这种策略分歧使重要性采样比率的估计严重偏离真实值，最终引发训练不稳定。

**量化噪声掩盖权重更新。** 在RL训练中，相邻步间的权重更新量通常极小。然而，权重量化误差却远大于此更新量——尤其在训练初期，归一化量化误差可达到归一化权重更新的数个数量级以上（Figure 9）。这意味着量化模型几乎无法感知训练动态，其行为策略与全精度策略之间的差异持续扩大（Figure 4），导致梯度信号质量严重退化。

### 现有方法的不足

朴素低精度RL（INT8/FP8 RL）直接对旧Actor进行量化后Rollout，使用标准PPO/GRPO目标进行训练，但上述崩溃问题使其在多数任务上完全失效（如AIME 2024上准确率为0%，Table 2）。**FlashRL**（Liu et al., 2025）通过截断重要性采样（TIS）缓解了部分策略分歧，但仍未解决量化噪声对权重更新的根本性制约，在复杂推理任务上的性能恢复有限。

### 本文动机

上述分析揭示了两个关键的技术缺口：

1. **目标函数层面**：需要将行为策略（量化）与近端策略（全精度）解耦，并设计适应量化特性的裁剪机制，以控制策略分歧对梯度估计的破坏。
2. **量化操作层面**：需要在量化前对模型进行结构调整，使量化误差与权重更新幅度相匹配，从而让量化模型能够有效“感知”训练动态。

QuRL正是围绕这两个缺口展开：提出**解耦PPO目标**与**自适应裁剪范围（ACR）**以稳定训练，设计**更新感知量化（UAQ）**以提升权重更新的信噪比，最终在保持训练稳定性的前提下，实现低精度Rollout的高效推理加速。



## 核心方法与创新机理

QuRL 的核心创新并非简单地用低精度模型替代全精度 Actor 进行 rollout，而在于识别并系统性地解决了量化引入后强化学习训练中三个相互耦合的崩溃机制。以下按 changed slots 展开。

### 1. 行为策略量化：将 rollout 瓶颈转化为可控加速杠杆

**Changed Slot：行为策略**  
*Baseline*：全精度旧 Actor（`π_θ_old`）进行自回归 rollout。  
*Proposed*：将旧 Actor 一次性量化为低精度模型 `π_θ̂_old`（INT8/FP8）执行 rollout。

这一替换的动机来自硬效率瓶颈：rollout 阶段因自回归解码特性消耗约 70% 训练时间。通过 INT8 量化，7B 模型获得 20%–30% 推理加速，32B 模型在 A100 上加速 70%、H100 上加速 90%（Figure 8）。QuRL 的量化策略处于 PTQ 与 QAT 之间——在每次 rollout 前做一次性量化，不通过梯度下降显式优化量化性能，从而避免 QAT 的训练开销。

然而，直接量化行为策略会引发训练崩溃：朴素 INT8 RL 在 GSM8K 上仅获 48.78% 准确率，远低于全精度 BF16 RL 的 55.35%（Table 1），且在 AIME 2024 上完全失效（Avg@1 = 0.00%，Table 2）。

### 2. 解耦 PPO 目标与自适应裁剪范围：阻断策略分歧传导链

**Changed Slot：目标函数**  
*Baseline*：标准 PPO/GRPO 目标，行为策略与近端策略均为同一 `π_θ_old`。  
*Proposed*：解耦 PPO 目标，将行为策略 `π_θ_behav`（量化 Actor）与近端策略 `π_θ_prox`（全精度 Actor）分离。

$$ \mathcal{I}_{\mathrm{decoupled}}(\theta) = \tilde{\mathbb{E}}_{o \sim \pi_{\theta_{\mathrm{behav}}}} \left[ \frac{\pi_{\theta_{\mathrm{prox}}}(o_{i,t})}{\pi_{\theta_{\mathrm{behav}}}(o_{i,t})} \min\left( R_{i,t} A_{i,t}, \mathrm{clip}(R_{i,t}, 1-\epsilon, 1+\epsilon) A_{i,t} \right) \right] $$

**Changed Slot：重要性采样比率**  
*Baseline*：使用量化 Actor 的普通重要性采样比率（导致训练崩溃）。  
*Proposed*：截断重要性采样（TIS）+ 自适应裁剪范围（ACR）。

崩溃的因果链如下：量化引入的策略差异使行为策略与近端策略间的 KL 散度在 1000 步训练后从 0.002 飙升至 0.025（12 倍，Figure 3a），近端-行为策略比率的最大值可达 $10^5$（Figure 3b），导致梯度范数爆炸、奖励崩溃（Figure 2a）和 token 裁剪比例异常升高（Figure 2b）。

QuRL 的两层防御机制：
- **TIS** 用常数 $C$ 截断近端-行为比率 $\min(\pi_{\theta_{\mathrm{prox}}}/\pi_{\theta_{\mathrm{behav}}}, C)$，直接限制梯度范数上界。
- **ACR** 动态调整裁剪上界为 $(1+\epsilon)/r_{i,t}$，当行为策略概率被截断时，允许更多正优势 token 通过裁剪，缓解偏差梯度累积。

$$ \mathcal{I}_{\mathrm{ACR}}(\theta) = \tilde{\mathbb{E}}_{o \sim \pi_{\theta_{\mathrm{behav}}}} \left[ \min\left( \frac{\pi_{\theta_{\mathrm{prox}}}(o_{i,t})}{\pi_{\theta_{\mathrm{behav}}}(o_{i,t})}, C \right) \min\left( R_{i,t} A_{i,t}, \mathrm{clip}\left( R_{i,t}, (1-\epsilon), \frac{(1+\epsilon)}{r_{i,t}} \right) A_{i,t} \right) \right] $$

仅靠解耦 PPO 目标即可显著提升训练稳定性（Figure 2），而 ACR 进一步将 INT8 下与全精度的精度差距缩至约 2%、FP8 下缩至约 1%（Table 1）。

### 3. 更新感知量化：放大权重更新信噪比以跟踪训练动态

**Changed Slot：量化操作**  
*Baseline*：标准 PTQ，量化误差主导权重更新量。  
*Proposed*：更新感知量化（UAQ），利用线性层不变缩放属性，在 RL 训练前一次性调整权重。

第三个崩溃机制更为隐蔽：权重量化误差远大于 RL 步间的权重更新量，尤其在训练初期（Figure 9, Appendix A），导致量化模型无法感知训练动态。UAQ 利用线性层的不变缩放 $WX = (W/s) \cdot (sX)$，选择 $s>1$ 产生双重增益：
- 权重缩小 $s$ 倍使量化误差降低：$\hat{\theta}_{\mathrm{old}} - \theta_{\mathrm{old}} \propto |\theta_{\mathrm{old}}|/(s \cdot 2^b)$
- 激活放大 $s$ 倍使梯度幅值增大：$\theta - \theta_{\mathrm{old}} \propto s \cdot \alpha G$

两者结合产生 $s^2$ 级的信噪比提升。消融实验（Table 4）表明 $s=1.5$ 与学习率 $\alpha=10^{-6}$ 的组合获得最优 Avg@32（31.25），优于 $s=1$ 或 $s=2$ 的配置。UAQ 使 QuRL INT8 在 DeepScaleR 五任务上平均准确率达 55.48%，超过全精度基线 1.7%（Table 3）。

**注意**：UAQ 在高学习率场景（如 GSM8K PPO 实验的 $\alpha=10^{-5}$）下被禁用，因为此时权重更新幅度已足够大，额外放大反而可能破坏训练稳定性。



![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_eG0bpCwdKn/figures/001_Figure_1.jpg]]
*Figure 1: Overview of QuRL training. The sampling model $\theta _ { \mathrm { o l d } }$ is quantized to $\hat { \theta } _ { \mathrm { o l d } }$ for rollout

QuRL 的核心思路是将 RL 训练中耗时最长的 rollout 阶段从全精度计算替换为低精度（INT8/FP8）推理，同时通过三项关键设计保证训练稳定性和最终策略质量。图 1 给出了整体流程。

**Pipeline 总览** QuRL 的训练循环由六个模块构成闭环：

1. **量化旧 Actor**：在每一轮更新开始前，对当前全精度 Actor 参数 $\theta_{\mathrm{old}}$ 执行一次性量化，得到低精度副本 $\hat{\theta}_{\mathrm{old}} = Q(\theta_{\mathrm{old}})$。该量化位于 PTQ 与 QAT 之间——不通过梯度回传优化量化效果，但会在每轮 rollout 前重新执行。
2. **Rollout 生成**：使用量化后的 Actor 进行自回归解码，收集轨迹 $\{o_i\}$。由于矩阵乘法在低精度下显著加速，该阶段可节省 20%–90% 的训练时间（Figure 8）。
3. **解耦 PPO 目标**：轨迹由量化行为策略 $\pi_{\theta_{\mathrm{behav}}}$ 采样，但梯度计算以全精度近端策略 $\pi_{\theta_{\mathrm{prox}}}$ 为锚点。目标函数显式分离两者：
   $$
   \mathcal{I}_{\mathrm{decoupled}}(\theta) = \tilde{\mathbb{E}}_{o \sim \pi_{\theta_{\mathrm{behav}}}} \left[ \frac{\pi_{\theta_{\mathrm{prox}}}(o_{i,t})}{\pi_{\theta_{\mathrm{behav}}}(o_{i,t})} \min\left( R_{i,t} A_{i,t}, \mathrm{clip}(R_{i,t}, 1-\epsilon, 1+\epsilon) A_{i,t} \right) \right]
   $$
   这一分离是训练稳定性的第一道防线——直接使用量化 Actor 作为重要性采样基准会导致奖励崩溃和 token 裁剪比例异常升高（Figure 2）。
4. **自适应裁剪范围（ACR）**：针对行为策略与近端策略比率 $r_{i,t} = \pi_{\theta_{\mathrm{prox}}} / \pi_{\theta_{\mathrm{behav}}}$ 在训练中急剧增大（Figure 3(b) 显示可达 $10^5$）的问题，ACR 动态调整裁剪上界为 $(1+\epsilon)/r_{i,t}$，使被截断的正优势 token 仍能通过梯度更新。
5. **更新感知量化（UAQ）**：在 RL 训练开始前，对线性层的 Q/K/V 权重施加不变缩放（$W \leftarrow W/s$，对应激活缩放 $s$ 倍），选择 $s>1$ 以同时降低量化误差（$\propto |\theta_{\mathrm{old}}|/(s \cdot 2^b)$）并放大权重更新（$\propto s \cdot \alpha G$），产生 $s^2$ 级的信噪比提升。
6. **全精度策略更新**：梯度始终在全精度模型上累积和应用，确保策略表达能力不受量化精度限制。

**输入输出流** 每个训练步的输入为上一轮的全精度 Actor 参数，输出为更新后的全精度 Actor。中间数据流包括：量化参数 → 低精度 rollout 轨迹 → 基于行为/近端策略比率计算的优势估计与裁剪 → 梯度回传至全精度模型。

**方法定位** QuRL 并非简单的“量化后训练”，而是通过解耦目标、自适应裁剪和前置缩放三个机制协同，将量化引入的分布偏移从“训练崩溃”转化为“可控的精度-效率权衡”。这一框架在 PPO、GRPO、DAPO 三种 RL 算法上均得到验证（Section 5），表明其与具体 RL 目标的耦合度较低。



QuRL 的训练管线包含六个关键模块，围绕“量化旧 Actor 加速 rollout，全精度 Actor 稳定更新”这一核心思路展开。

### 1. 量化旧 Actor（Quantized Old Actor）

在每轮 RL 训练开始前，将旧 Actor 模型 $\theta_{\mathrm{old}}$ 的权重和激活一次性量化为低精度表示：

$$\hat{\theta}_{\mathrm{old}} = Q(\theta_{\mathrm{old}}, b)$$

其中 $Q(\cdot, b)$ 为通用 $b$ 位量化函数，其参数表示为：

$$Q(\theta, b) = \alpha \times (-1)^{\mathrm{sign}} \times 2^{d} \times \left(1 + \sum_{i=1}^{b-1-e} \frac{m_i}{2^i}\right)$$

式中 $\alpha$ 为缩放因子，$\mathrm{sign}$ 为符号位，$d$ 为指数，$m_i$ 为尾数位。量化后的模型 $\hat{\theta}_{\mathrm{old}}$ 用于后续 rollout 推理加速。QuRL 的量化策略介于 PTQ 与 QAT 之间：仅在 rollout 前做一次性量化，不通过梯度下降显式优化量化性能。

### 2. Rollout 生成（Rollout Generation）

利用量化 Actor $\pi_{\hat{\theta}_{\mathrm{old}}}$ 进行自回归解码，生成轨迹 $\{o_i\}$ 用于优势估计和策略梯度计算。由于自回归解码是 RL 训练的主要时间瓶颈（约占 70%），低精度矩阵乘法直接带来 20%–90% 的推理加速（Figure 8）。

### 3. 解耦 PPO 目标（Decoupled PPO Objective）

标准 GRPO 目标使用旧 Actor $\pi_{\theta_{\mathrm{old}}}$ 同时作为采样策略和重要性采样参考策略：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{q \sim P(q), o \sim \pi_{\theta_{\mathrm{old}}}} \left[ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|o_i|} \sum_{t=1}^{|o_i|} \min\left( R_{i,t} A_{i,t}, \mathrm{clip}(R_{i,t}, 1-\epsilon, 1+\epsilon) A_{i,t} \right) \right] \tag{1}$$

当旧 Actor 被量化后，直接代入 $\hat{\theta}_{\mathrm{old}}$ 会导致训练崩溃（Figure 2）。QuRL 将行为策略（量化 Actor $\pi_{\theta_{\mathrm{behav}}}$）与近端策略（全精度 Actor $\pi_{\theta_{\mathrm{prox}}}$）分离：

$$\mathcal{I}_{\mathrm{decoupled}}(\theta) = \tilde{\mathbb{E}}_{o \sim \pi_{\theta_{\mathrm{behav}}}} \left[ \frac{\pi_{\theta_{\mathrm{prox}}}(o_{i,t})}{\pi_{\theta_{\mathrm{behav}}}(o_{i,t})} \min\left( R_{i,t} A_{i,t}, \mathrm{clip}(R_{i,t}, 1-\epsilon, 1+\epsilon) A_{i,t} \right) \right] \tag{4}$$

其中 $\theta_{\mathrm{behav}} = \hat{\theta}_{\mathrm{old}}$（量化模型），$\theta_{\mathrm{prox}} = \theta_{\mathrm{old}}$（全精度模型）。该解耦使得重要性采样比率 $\frac{\pi_{\theta_{\mathrm{prox}}}}{\pi_{\theta_{\mathrm{behav}}}}$ 能正确反映量化引入的分布偏移，显著提升训练稳定性。

### 4. 截断重要性采样与自适应裁剪范围（TIS + ACR）

解耦后，近端-行为策略比率 $r_{i,t} = \frac{\pi_{\theta_{\mathrm{prox}}}(o_{i,t})}{\pi_{\theta_{\mathrm{behav}}}(o_{i,t})}$ 仍可能因量化误差而剧烈波动（Figure 3(b) 显示最大值可达 $10^5$）。QuRL 引入截断重要性采样（TIS）：

$$\mathcal{I}_{\mathrm{TIS}}(\theta) = \tilde{\mathbb{E}}_{o \sim \pi_{\theta_{\mathrm{behav}}}} \left[ \min\left( r_{i,t}, C \right) \min\left( R_{i,t} A_{i,t}, \mathrm{clip}(R_{i,t}, 1-\epsilon, 1+\epsilon) A_{i,t} \right) \right] \tag{5}$$

其中 $C$ 为截断上界。进一步，为缓解被截断的正优势 token 无法参与更新的问题，提出自适应裁剪范围（ACR），动态调整裁剪上界：

$$\mathcal{I}_{\mathrm{ACR}}(\theta) = \tilde{\mathbb{E}}_{o \sim \pi_{\theta_{\mathrm{behav}}}} \left[ \min\left( r_{i,t}, C \right) \min\left( R_{i,t} A_{i,t}, \mathrm{clip}\left( R_{i,t}, (1-\epsilon), \frac{1+\epsilon}{r_{i,t}} \right) A_{i,t} \right) \right] \tag{9}$$

当行为策略被截断时，ACR 将裁剪上界放大至 $\frac{1+\epsilon}{r_{i,t}}$，允许更多正优势 token 通过裁剪，减少有偏梯度估计。

### 5. 更新感知量化（Update-Aware Quantization, UAQ）

RL 训练中，权重更新量 $\theta - \theta_{\mathrm{old}}$ 通常远小于量化误差 $\hat{\theta}_{\mathrm{old}} - \theta_{\mathrm{old}}$（尤其在训练初期，Figure 9），导致量化模型难以感知训练动态。UAQ 利用线性层的不变缩放属性：

$$W X = \left( \frac{W}{s} \right) \cdot (s X)$$

在 RL 训练前对 Q/K/V 层权重除以 $s$（$s > 1$），激活乘以 $s$，保持前向输出不变。该操作同时产生两个效果：

- **降低量化误差**：$\hat{\theta}_{\mathrm{old}} - \theta_{\mathrm{old}} \propto \frac{|\theta_{\mathrm{old}}|}{s \cdot 2^b}$
- **放大权重更新**：$\theta - \theta_{\mathrm{old}} \propto s \cdot \alpha G$

两者结合产生 $s^2$ 级的信噪比提升，使量化模型能有效跟踪 RL 训练动态。消融实验（Table 4）表明 $s=1.5$ 与学习率 $\alpha=10^{-6}$ 的组合获得最优 Avg@32 性能（31.25）。

### 6. 全精度策略更新（Policy Update）

梯度计算和参数更新始终在全精度 Actor $\theta$ 上进行，仅 rollout 阶段使用量化模型加速。这确保了策略优化过程不受量化噪声累积影响，同时保持了低精度推理的效率优势。



## 实验与关键发现

### 效率瓶颈与训练稳定性诊断

QuRL的出发点源于一个明确的效率观察：在基于可验证奖励的RL训练中，rollout阶段由于自回归解码特性，消耗约70%的训练时间。将旧Actor量化为INT8/FP8进行rollout是最直接的加速方案，但朴素实现会导致训练崩溃。**Figure 2**展示了这一失败模式：直接使用量化rollout的GRPO目标使训练奖励迅速下降，token裁剪比例异常升高至1.5%后骤降至零——这表明策略更新完全失效。进一步分析（**Figure 3(a)**）揭示，训练1000步后行为策略（量化Actor）与近端策略（全精度Actor）间的KL散度从0.002增加到0.025（12倍），这种策略分歧是训练不稳定的根本原因。同时，**Figure 3(b)**显示近端-行为策略比率的最大值可达$10^5$量级，导致梯度估计产生巨大偏差。


![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_eG0bpCwdKn/figures/003_Figure_2.jpg]]
*Figure 2: Comparison of (a) training rewards and (b) token clipped fraction under different training objective or quantization*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_eG0bpCwdKn/figures/005_Figure_3.jpg]]
*Figure 3: Training dynamics of QuRL. (a) Training collapses after 1000 steps due to increased KL divergence between behavior and proximal policy, and (b) the maximum value of the proximal-tobehavior policy ratio*

另一个关键问题在于权重量化噪声与RL权重更新之间的尺度失配。**Figure 9**（附录）的可视化表明，归一化权重量化误差远大于RL步间的归一化权重更新量，尤其在训练初期，这意味着量化模型几乎无法感知训练动态，导致行为策略无法有效跟踪近端策略的演化。

### 主实验结果

#### GSM8K（PPO算法，7B模型）

**Table 1**展示了GSM8K准确率对比。全精度RL（BF16）达到55.35%的基线准确率，而朴素INT8 RL降至48.78%，性能损失显著。QuRL INT8将准确率恢复至53.55%，与BF16基线的差距缩小至仅1.8个百分点；QuRL FP8进一步达到54.28%，几乎追平全精度训练。值得注意的是，朴素FP8 RL完全失败（0%准确率），而QuRL FP8仍保持竞争力，验证了方法在不同量化格式下的鲁棒性。该实验中UAQ被禁用，因为PPO的高学习率（$10^{-5}$）已提供足够的权重更新幅度。


![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_eG0bpCwdKn/figures/009_Table_1.jpg]]
*Table 1: Comparison of GSM8k accuracy*

#### AIME 2024（DAPO算法）

**Table 2**报告了AIME 2024的Avg@1和Avg@32结果。朴素INT8 RL的Avg@1为0%，训练完全崩溃。QuRL w/o UAQ FP8达到36.66%的Avg@1，成功恢复了有效训练。在Avg@32指标上，QuRL w/ UAQ INT8达到40.52%，与BF16基线的43.33%差距控制在3个百分点以内，而朴素INT8 RL仅为0%。


![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_eG0bpCwdKn/figures/011_Table_2.jpg]]
*Table 2: Comparison of AIME 2024 accuracy*

#### DeepScaleR多任务推理（GRPO算法）

**Table 3**汇总了DeepScaleR在五个数学推理任务（AIME24、AMC、MATH、Minerva、Olympiad）上的Avg@32平均准确率。QuRL w/ UAQ INT8达到55.48%，不仅大幅超越朴素INT8 RL的52.31%（+3.17个百分点），甚至超过全精度BF16基线的56.40%仅差0.92个百分点——在五个任务平均意义上实现了准全精度性能。QuRL w/o UAQ INT8为53.78%，UAQ带来的增益约为1.7个百分点。


![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_eG0bpCwdKn/figures/013_Table_3.jpg]]
*Table 3: Comparison of Avg@32 accuracy across various math reasoning tasks of DeepScaleR*

#### 推理加速效果

**Figure 8**量化了INT8量化的实际加速收益。在7B模型上，INT8带来20%~30%的吞吐量提升；在32B模型上，加速效果更为显著——A100上提升70%，H100上提升90%。这一加速直接作用于占总训练时间约70%的rollout阶段，整体训练效率改善显著。

### 消融实验：UAQ缩放因子与学习率

**Table 4**针对UAQ的两个关键超参数——缩放因子$s$和学习率$\alpha$——进行了消融。固定$\alpha=10^{-6}$时，$s=1.5$获得最高的Avg@32（31.25），优于$s=1$（27.88）和$s=2$（29.62）。固定$s=1$时，$\alpha=10^{-6}$（27.88）优于更高的学习率$1.5\times10^{-6}$（26.56）和$2\times10^{-6}$（25.81）。结果表明，适中的缩放因子（$s>1$）通过同时降低量化误差和放大权重更新，产生了$s^2$级的信噪比提升；但过高的学习率反而损害性能，可能因为权重更新幅度超出量化模型的跟踪能力。

### 收敛性分析

**Figure 6**（INT8）和**Figure 7**（FP8）展示了各方法在GSM8K上的训练收敛曲线。全精度RL在约50步后迅速收敛至~0.55准确率并保持稳定。朴素INT8 RL在初期短暂上升后即出现剧烈波动和下降，验证了训练崩溃。QuRL INT8的收敛轨迹与全精度RL高度一致，仅在终值上略低约2个百分点。FlashRL（Liu et al., 2025）作为对比基线，其INT8收敛曲线介于朴素RL和QuRL之间，但仍存在明显波动。FP8实验呈现类似模式：朴素FP8 RL完全无法收敛，QuRL FP8则稳定收敛并接近BF16性能。

### 失败模式与局限性

1. **精度差距残余**：尽管QuRL大幅缩小了量化训练的精度差距，但与全精度训练相比仍存在约1%~2%的性能下降（如GSM8K上53.55% vs 55.35%，DeepScaleR上55.48% vs 56.40%）。这一残余差距可能源于量化引入的不可约噪声。

2. **高学习率场景下UAQ失效**：GSM8K PPO实验中使用学习率$10^{-5}$时UAQ被禁用，因为权重更新幅度已足够大，额外的缩放反而可能破坏训练稳定性。UAQ的有效性依赖于适当的权重更新幅度。

3. **FP8 KV缓存量化未采用**：由于vLLM中FP8 KV缓存支持不完善，实验未采用FP8 KV缓存量化，这可能低估了FP8的完整加速潜力。

4. **超参数敏感性**：自适应裁剪范围（ACR）的截断参数$C$和UAQ的缩放因子$s$需要针对不同任务进行调整，增加了调参负担。如何自动化选择这些参数仍是开放问题。

5. **模型规模与任务泛化性**：当前实验覆盖7B至32B模型和数学推理任务，在更大规模模型（70B+）及在线RLHF等更复杂场景下的表现尚未验证。



## 定位与知识库关联

### 问题定位与核心瓶颈

QuRL 瞄准的是基于可验证奖励的强化学习训练中一个明确的效率瓶颈：rollout 阶段的自回归解码消耗约 70% 的训练时间，而这一阶段使用的是旧 Actor 模型进行推理。现有加速方案通常依赖更大的硬件集群或模型蒸馏，QuRL 则选择了一条不同的路径——对旧 Actor 进行量化以加速推理，同时通过一系列训练稳定化技术保持策略梯度质量。

该方法处于后训练量化（PTQ）与量化感知训练（QAT）之间的独特位置：与 QAT 不同，QuRL 不通过梯度下降显式优化量化性能，而是利用 RL 训练本身来隐式地使模型适应量化；与 PTQ 不同，QuRL 在量化后仍进行全精度权重更新，使模型能够持续感知训练动态。

### 与基线方法的关系

**全精度 RL（BF16）** 是 QuRL 的性能上界参照。QuRL 的目标并非超越全精度训练，而是在大幅加速 rollout 的同时将精度损失控制在可接受范围内。在 DeepScaleR 五个推理任务上，QuRL w/ UAQ (INT8) 达到 55.48% 的平均准确率，与 BF16 基线的 56.40% 仅差 0.92 个百分点（Table 3）。

**朴素 INT8/FP8 RL** 是将旧 Actor 直接量化后进行 rollout 的简单方案。该方法在实验中出现严重训练不稳定性：训练奖励在若干 RL 步后崩溃，token 裁剪比例异常升高后骤降至零（Figure 2）。在 AIME 2024 上，INT8 RL 的 Avg@1 为 0.00%（Table 2），表明直接量化方案完全失效。QuRL 通过解耦 PPO 目标、自适应裁剪范围和更新感知量化三项技术，将 INT8 RL 的 DeepScaleR 平均准确率从 52.31% 提升至 55.48%（Table 3）。

**FlashRL**（Liu et al., 2025）是同期采用截断重要性采样的量化 RL 方法。在 DeepScaleR 的 INT8 实验中，FlashRL 达到 54.28% 的平均准确率，低于 QuRL w/ UAQ 的 55.48%（Table 3）。QuRL 在截断重要性采样的基础上进一步引入了自适应裁剪范围，动态调整裁剪上界以缓解被截断正优势 token 的梯度偏差问题。

### 方法谱系中的技术贡献

QuRL 的技术贡献可分解为三个递进的组件：

1. **解耦 PPO 目标**：将行为策略（量化 Actor）与近端策略（全精度 Actor）分离，使重要性采样比率基于两者计算，而非直接使用量化模型自身。这一设计防止了量化误差直接污染策略梯度估计。实验表明，在 1000 步训练后，行为策略与近端策略间的 KL 散度从 0.002 增加到 0.025（12 倍），若不加以控制将导致训练崩溃（Figure 3a）。

2. **自适应裁剪范围（ACR）**：在截断重要性采样的基础上，ACR 根据近端-行为比率 $r_{i,t}$ 动态调整裁剪上界为 $(1+\epsilon)/r_{i,t}$。当行为策略概率被截断时，固定的裁剪上界会阻止正优势 token 通过，ACR 通过放大上界来解决这一问题。

3. **更新感知量化（UAQ）**：利用线性层的不变缩放属性 $WX = (W/s) \cdot (sX)$，在 RL 训练前对 Q/K/V 层权重进行一次性缩放（$s>1$）。缩放因子 $s$ 同时降低量化误差（$\propto 1/s$）并放大权重更新（$\propto s$），产生 $s^2$ 级的信噪比提升。消融实验表明，$s=1.5$ 与学习率 $\alpha=10^{-6}$ 的组合获得最高的 Avg@32（31.25），优于 $s=1$ 或 $s=2$（Table 4）。

### 适用边界与局限

1. **精度下限**：尽管 QuRL 大幅缩小了量化训练的精度差距，但与全精度训练相比仍存在约 1-2% 的性能下降。在 GSM8K 上，QuRL INT8 的 53.55% 低于 BF16 的 55.35%（Table 1）。

2. **UAQ 的适用条件**：当学习率较高时（如 GSM8K PPO 实验中使用 $10^{-5}$），UAQ 被禁用，因为此时权重更新幅度本身已足够大，额外的缩放可能导致训练不稳定。UAQ 的有效性依赖于适当的权重更新幅度。

3. **FP8 KV 缓存**：由于 vLLM 中 FP8 KV 缓存支持不完善，实验未采用该优化，可能影响整体加速效果的上界。

4. **超参数敏感性**：ACR 和 UAQ 引入额外超参数（截断参数 $C$、缩放因子 $s$），可能需针对不同任务进行调整。论文未提供这些参数的自动选择机制。

5. **模型规模验证范围**：当前实验覆盖 7B 至 32B 模型，在更大规模模型（如 70B+）上的扩展性尚未验证。

### 开放问题

- 能否将 QuRL 拓展到更低精度（如 4-bit）而不显著损失性能？当前 INT8/FP8 的量化误差已被 UAQ 有效抑制，但 4-bit 的量化噪声量级可能超出 UAQ 的补偿能力。
- 如何自动选择 UAQ 中的缩放因子 $s$ 和截断参数 $C$，以减少人工调参并提升方法在不同任务间的迁移性？
- 在更大规模模型（70B+）和更多样化任务（如代码生成、多模态推理）上的扩展性如何？
- 解耦 PPO 中近端策略与行为策略的差异可否通过其他重要性采样方法（如自适应重要性采样）进一步减小，从而降低对截断参数 $C$ 的依赖？
- QuRL 在在线 RLHF 场景下的表现与稳定性是否仍然保持？当前验证集中于离线可验证奖励任务，人类反馈引入的奖励噪声可能与量化噪声产生交互效应。



## 原文 PDF

![[paperPDFs/ICLR_2026/QuRL_Low_Precision_Reinforcement_Learning_for_Efficient_Reasoning.pdf]]
