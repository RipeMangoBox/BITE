---
title: "From Observations to Events: Event-Aware World Models for Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/From_Observations_to_Events_Event_Aware_World_Models_for_Reinforcement_Learning.pdf
openreview_forum_id: OWkkFaq1IZ
aliases:
- EAWME
- FOEEAWMRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "世界模型是否明确捕获并预测观测流中反映有意义的时空变换的“事件”（动力学特征），通过事件预测器与通用事件分割器将表示空间约束到与决策相关的转变上。"
primary_logic: "将世界模型的训练目标从重建原始观测转向预测自动生成的事件流，通过信息瓶颈优化学习鲁棒、泛化且对关键动态敏感的紧凑表示，显著提升模型决策与泛化能力。"
claims:
- "EAWM consistently boosts the performance of strong MBRL baselines by 10%–45%, setting new state-of-the-art results across benchmarks."
- "Event prediction intrinsically constrains the representation space to meaningful spatio-temporal transitions through information bottleneck optimization."
- "EAWM surpasses existing model-free and model-based RL across 55 test tasks, encompassing both continuous and discrete control, as well as multi-modal observations."
- "We design a generic event segmentor (GES) to identify event boundaries, which enable robust representation learning responsive to the critical events for multimodal observations."
---

# From Observations to Events: Event-Aware World Models for Reinforcement Learning

> [!tip] 核心洞察
> 将世界模型的训练目标从重建原始观测转向预测自动生成的事件流，通过信息瓶颈优化学习鲁棒、泛化且对关键动态敏感的紧凑表示，显著提升模型决策与泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 从观测到事件：面向强化学习的事件感知世界模型 |
| 英文题名 | From Observations to Events: Event-Aware World Models for Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=OWkkFaq1IZ); [GitHub](https://github.com/MarquisDarwin/EAWM) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Event-Aware World Model (EAWM) |
| Dataset | Atari 100K (26 games), DeepMind Control Suite 500K (10 hard tasks), DMC-GB2 Color Hard (6 tasks), DMC-GB2 Video Hard (6 tasks) |

> [!tip] 效果简介
> - Atari 100K (26 games) 上，Mean Human Normalized Score 为 EASimulus 1.818，对比 Simulus 1.609 (next best model-based)，变化 +0.209 (13.0%)。
> - DeepMind Control Suite 500K (10 hard tasks) 上，Mean Score 为 EADream 723.8，对比 DreamerV3 606.3，变化 +117.5 (19.4%)。
> - DMC-GB2 Color Hard (6 tasks) 上，Mean Score 为 EADream 750，对比 DreamerV3 456，变化 +294 (64.5%)。

## 概述

### 问题瓶颈

现有基于模型强化学习（MBRL）方法的核心瓶颈在于**过度依赖原始观测重建**。世界模型被训练来逐像素或逐维度地复现下一帧观测，这一目标导致三个连锁问题：其一，长时预测因误差累积而迅速偏离真实状态；其二，策略学习被大量与决策无关的视觉细节（纹理、颜色、背景）淹没，形成信息冗余；其三，模型易受光照变化、纹理漂移等虚假关联的干扰，难以聚焦于真正影响奖励和状态转移的关键动态事件。简言之，世界模型缺乏对“观测流中反映有意义时空变换的事件”的感知能力。

### 核心思路

EAWM（Event-Aware World Model）将世界模型的训练目标从“重建原始观测”转向“预测自动生成的事件流”。其因果调节变量是：**世界模型是否在表示空间中明确捕获并预测反映关键动态的“事件”**。为实现这一目标，EAWM引入两个协同机制——**事件预测器**（Event Predictor）将序列模型的输出约束到与决策相关的时空转变上，通过信息瓶颈优化学习紧凑且鲁棒的表示；**通用事件分割器**（Generic Event Segmentor, GES）自动识别事件边界，在边界处抑制事件预测损失并重新分配注意力到原始观测，从而避免边界模糊对表示学习的干扰。事件本身由多模态自动生成器从原始观测中导出，无需人工标注。

### 方法定位

EAWM是一个**即插即用的世界模型增强框架**，可应用于不同架构的MBRL基座。论文通过统一公式将DreamerV3（基于RSSM）和Simulus（基于Transformer）纳入同一框架，分别实现为**EADream**和**EASimulus**。在方法谱系中，EAWM区别于仅利用时序差分（如DyMoDreamer, Zhang et al., 2025）或单纯改进观测重建质量的方案，而是通过事件预测这一辅助任务，从根本上改变表示空间的结构。

### 主要结果

EAWM在**55个测试任务**上全面超越现有无模型和基于模型的强化学习方法，覆盖离散控制（Atari 100K, 26款游戏）、连续控制（DeepMind Control Suite 500K, 10项困难任务）以及多模态观测下的视觉泛化（DMC-GB2, 18个测试环境）。关键数据如下：

- **Atari 100K**：EASimulus取得1.818的平均人类归一化分数（HNS），较最强基线Simulus（1.609）提升**13.0%**。
- **DeepMind Control Suite**：EADream取得723.8的平均回报，较DreamerV3（606.3）提升**19.4%**。
- **DMC-GB2泛化测试**：在Color Hard和Video Hard环境中，EADream分别较DreamerV3提升**64.5%**和**39.1%**，且无需针对测试环境做任何调整。
- **整体提升幅度**：EAWM在强MBRL基线上实现**10%–45%**的一致性性能增益，在需要事件感知反应的任务（如Breakout提升55%，Acrobot Swingup提升115%）上尤为显著。

消融实验确认，移除事件预测器导致Atari 100K平均HNS下降约0.4，移除观测预测使DMC任务平均分数从737.2降至519.5，验证了事件感知机制的关键作用。方法额外训练开销仅11%–17%，在可控范围内。

## 背景与动机

基于模型的强化学习（MBRL）通过构建环境的世界模型，使智能体能够在想象的轨迹中学习行为，从而大幅提升样本效率。然而，当前最先进的MBRL方法——如 **DreamerV3**（Hafner et al., 2025）和 **Simulus**（Cohen et al., 2025）——在训练世界模型时，普遍以精确重建原始观测为核心目标。这种设计带来了三个深层瓶颈：

**长时预测的退化。** 世界模型在想象推演过程中，预测误差会随步数累积，导致远期帧的质量迅速下降。Figure 1 的定性对比显示，在想象第9步时，模型生成的帧与真实帧在物体位置上已出现明显偏差——然而，事件预测器仍能准确定位空间边界。这表明，逐像素重建目标迫使模型将容量浪费在纹理、颜色等对决策无关的细节上，而非捕获驱动状态转移的动力学特征。

**信息冗余与虚假变化干扰。** 原始观测流中充斥着大量与任务无关的波动——背景纹理的随机替换、光照条件的微小扰动、视频背景的动态变化——这些“虚假变化”在重建损失中占据主导地位，淹没了真正影响决策的关键动态信号。在视觉泛化基准 DMC-GB2 上，**DreamerV3** 在 Color Hard 和 Video Hard 测试环境中的平均得分分别仅为 456 和 343，而专门设计的视觉泛化方法 **SADA**（Almuzairee et al., 2024）虽有所改善，但仍未从根本上解决表示空间对虚假相关性的敏感性。

**缺乏对“事件”的感知。** 人类和动物在感知环境时，并不会逐帧重建视网膜上的全部信息。神经科学证据表明，上丘（SC）神经元专门处理动力学特征——即观测流中反映有意义时空变换的“事件”。然而，现有世界模型完全缺失这种事件感知能力：它们无法自动识别“何时发生了重要变化”，也无法将表示学习聚焦于这些关键转变。

上述瓶颈的根源在于一个共同的因果机制：**世界模型的训练目标被锁定在原始观测空间，而非决策相关的动力学空间。** 当模型被迫预测每一个像素值时，表示空间被低层次的视觉统计所主导；而当环境出现视觉分布偏移时，这些统计量失效，导致策略崩溃。因此，核心问题并非“如何更好地重建观测”，而是“如何让世界模型学会关注对决策真正重要的变化”。

本文提出的 **Event-Aware World Model（EAWM）** 框架正是针对这一因果缺口：将世界模型的训练目标从重建原始观测转向预测自动生成的事件流。通过引入事件预测器与通用事件分割器（GES），EAWM 在表示空间中施加信息瓶颈优化，使模型天然地聚焦于有意义的时空转变，从而在长时预测、视觉泛化和样本效率三个维度上实现一致且显著的提升。

## 核心创新

现有基于模型强化学习（MBRL）方法的核心瓶颈在于：世界模型的训练目标过度依赖原始观测重建，导致表示空间被纹理、颜色等与决策无关的虚假变化所主导，长时预测不准确，且缺乏对关键动态事件的感知能力。EAWM 的核心创新在于**将世界模型的训练目标从重建原始观测转向预测自动生成的事件流**，通过信息瓶颈优化将表示空间约束到有意义的时空转变上，从而学习鲁棒、泛化且对关键动态敏感的紧凑表示。

这一核心洞察通过四个紧密耦合的 changed slots 实现：

### 1. 自动化多模态事件生成器（Event Generation）

EAWM 不依赖人工标注，而是设计了统一的自动化事件生成器，将原始观测流转化为三类模态的事件信号：

- **视觉输入**：采用自适应高斯混合模型（AGMMs）对每个像素的对数亮度分布建模。当下一帧的亮度值与当前混合模型之间的马氏距离超过阈值，或模型对该像素的权重（确定性）过低时，触发事件。这有效抑制了噪声和缓慢亮度变化引起的误报。
- **有序数据**（如关节角度）：当归一化变化量超过阈值 $C_o$ 时产生事件。
- **名义数据**（如离散状态）：当类别标签发生变化时直接标记事件。

事件生成中的阈值（$C_I$、$C_o$）在所有基准测试中固定，未针对各任务单独调优，这既是方法简洁性的体现，也意味着存在进一步优化的空间。

### 2. 事件预测器（Event Predictor）

事件预测器是 EAWM 实现信息瓶颈优化的关键组件。它从序列模型的输出 $\mathbf{y}_t$ 和观测嵌入 $\mathbf{z}_t$ 出发，预测下一时刻每个模态的事件类别概率 $\hat{p}_i^{(m)}$。损失函数根据数据模态自适应选择：

- 有序数据使用交叉熵损失
- 视觉和名义数据使用焦点损失（Focal Loss），以缓解类别不平衡

$$
\mathcal{L}_{\mathrm{e}}^{(m)}(\theta) = \begin{cases} 
\sum_{i=1}^{N^m} \mathrm{CrossEntropy}(p_i^{(m)}, \hat{p}_i^{(m)}) & \text{if } m \in \mathscr{D}_o \\
\sum_{i=1}^{N^m} \mathrm{Focal}(p_i^{(m)}, \hat{p}_i^{(m)}) & \text{if } m \in \mathscr{D}_I \cup \mathscr{D}_n 
\end{cases}
$$

通过强制世界模型预测事件——而非重建所有像素——表示空间被自然地压缩到仅保留与动态变化相关的信息，形成信息瓶颈。消融实验（Figure 4a）证实：移除事件预测器导致两个世界模型（Simulus、EADream）在 Atari 100K 上的平均人类归一化分数下降约 0.4，验证了该组件的决定性作用。

### 3. 通用事件分割器（Generic Event Segmentor, GES）

GES 是一个**无额外可训练参数**的确定性门控函数，用于自动检测事件边界（即有意义观测片段的起止点）。其输入为事件比率 $\alpha_t^{(m)}$（当前帧中事件像素/维度占比），通过与阈值 $\alpha_{\mathrm{thr}}^{(m)}$ 比较输出门控信号：

- 当 $\alpha_t^{(m)} \geq \alpha_{\mathrm{thr}}^{(m)}$ 时，GES 判定当前处于事件密集区（边界），输出 0，**抑制事件预测损失**，同时通过事件感知观测损失将模型注意力重新分配到原始观测重建上。
- 当 $\alpha_t^{(m)} < \alpha_{\mathrm{thr}}^{(m)}$ 时，事件稀疏，GES 输出非零值，允许事件预测损失正常反向传播。

这一设计解决了事件预测与观测重建之间的注意力分配问题：在事件边界（剧烈变化区域），模型应关注原始观测以捕获完整上下文；在事件稀疏区域，模型应聚焦于事件预测以维持对关键动态的敏感性。EADream 和 EASimulus 分别采用了不同形式的 GES 函数（指示函数与反双曲正弦平滑函数），体现了该模块的架构灵活性。

### 4. 事件感知损失（Event-Aware Loss）

EAWM 的总损失由基础世界模型损失与事件感知损失加权求和：

$$
\mathcal{L}(\theta) \doteq \mathcal{L}_{\mathrm{WM}}(\theta) + \beta_o \mathcal{L}_o(\theta) + \beta_e \mathcal{L}_e(\theta)
$$

其中 $\mathcal{L}_o(\theta)$ 是事件感知的观测损失，受 GES 门控信号调制——在事件边界处增加对非事件区域的观测重建权重 $\omega$。$\mathcal{L}_e(\theta)$ 是事件预测损失，同样受 GES 门控。这种双重调制机制使得世界模型能够在“关注动态事件”和“重建完整观测”之间动态平衡。

### 方法定位

EAWM 并非独立的模型架构，而是一个**通用框架**，可赋予不同世界模型对抽象事件的通用理解能力。论文通过统一公式将 DreamerV3（RSSM 架构）和 Simulus（Transformer 架构）纳入同一框架，分别实现为 EADream 和 EASimulus，验证了方法的广泛适用性。相比 **DreamerV3**（Hafner et al., 2025）和 **Simulus**（Cohen et al., 2025），EAWM 仅增加了约 11-17% 的训练时间开销，却在 55 个测试任务上实现了 10%-45% 的性能提升，在 Atari 100K 上首次使 MBRL 方法达到超人级 IQM 分数。

## 整体框架

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_OWkkFaq1IZ/figures/006_Figure_3.jpg]]
*Figure 3: EAWM architecture that predicts the next observations and events. Given the length of the trajectory segment k , , the sequence model outputs $\mathbf { y } _ { t }$ , which summarizes the embeddings $\mathbf { Z } _ { t - 1 } = \left[ \mathbf { z } _ { t - k }$ , . . . , $\mathbf { z } _ { t - 1 } \right$] and $\mathbf { A } _ { t - 1 }$ = [ $\mathbf { a } _ { t - k }$ , . . . , $\mathbf { a } _ { t - 1 }$ ] . The observation predictor predicts the next observation $\hat { \mathbf { o } } _ { t }$ via the outputs of the sequence model $\mathbf { y } _ { t }$ and the outputs of the dynamics predictor $\hat { \mathbf { z } } _ { t }$ The representation model combines observation encodings with hidden states \...

EAWM 并非一种独立的架构，而是一个可嵌入不同世界模型的通用框架，使其具备对抽象“事件”的通用理解能力。其核心设计思想是将世界模型的训练目标从单纯的观测重建扩展为同时预测自动生成的事件流，通过事件预测器与通用事件分割器（GES）将表示空间约束到与决策相关的时空转变上。

### 模块组成与数据流

EAWM 框架由八个功能模块构成，其前向数据流如 Figure 3 所示。给定长度为 $k$ 的轨迹片段，系统按以下顺序处理信息：

1. **序列模型（Sequence Model）**：以隐藏状态 $\mathbf{h}_{t-1}$、历史嵌入 $\mathbf{Z}_{t-1} = [\mathbf{z}_{t-k}, \dots, \mathbf{z}_{t-1}]$ 和动作序列 $\mathbf{A}_{t-1} = [\mathbf{a}_{t-k}, \dots, \mathbf{a}_{t-1}]$ 为输入，输出隐藏状态 $\mathbf{h}_t$ 和汇总输出 $\mathbf{y}_t$：
   $$\mathbf{h}_t, \mathbf{y}_t = \mathbf{F}_\theta(\mathbf{h}_{t-1}, \mathbf{Z}_{t-1}, \mathbf{A}_{t-1})$$

2. **表示模型（Representation Model）**：从当前观测 $\mathbf{o}_t$ 和隐藏状态 $\mathbf{h}_t$ 采样得到嵌入 $\mathbf{z}_t$：
   $$\mathbf{z}_t \sim q_\theta(\mathbf{z}_t \mid \mathbf{o}_t, \mathbf{h}_t)$$

3. **动力学预测器（Dynamics Predictor）**：从序列模型输出 $\mathbf{y}_t$ 预测下一时刻嵌入 $\hat{\mathbf{z}}_t$：
   $$\hat{\mathbf{z}}_t \sim p_\theta(\hat{\mathbf{z}}_t \mid \mathbf{y}_t)$$

4. **观测预测器（Observation Predictor）**：结合 $\mathbf{y}_t$ 和 $\hat{\mathbf{z}}_t$ 预测下一观测 $\hat{\mathbf{o}}_t$。

5. **奖励预测器（Reward Predictor）**与**持续预测器（Continuation Predictor）**：分别从 $\mathbf{y}_t$ 和嵌入预测奖励与回合终止标志。

6. **事件预测器（Event Predictor）**：从 $\mathbf{y}_t$ 和 $\hat{\mathbf{z}}_t$ 预测事件类别 $\hat{\mathbf{e}}_t$，是框架的事件感知核心。

7. **通用事件分割器（Generic Event Segmentor, GES）**：基于观测变化自动识别事件边界（即有意义片段的起止点），输出门控信号 $g(\alpha_t^{(m)}, \alpha_{\text{thr}}^{(m)})$，用于调节事件预测损失和观测损失，且不引入额外可训练参数。

智能体的状态 $\mathbf{s}_t$ 定义为序列模型输出 $\mathbf{y}_t$ 与观测嵌入 $\mathbf{z}_t$ 的整合。行为学习完全基于世界模型生成的想象轨迹，无需额外的环境交互。

### 事件生成与多模态处理

EAWM 采用自动化多模态事件生成器，根据数据类型采用不同策略：

- **视觉输入**：使用自适应高斯混合模型（AGMMs）对每个像素的对数亮度建模，当新观测与模型之间存在较大马氏距离（“惊讶”）或低权重（“不确定”）时触发事件，有效抑制噪声或缓慢亮度变化引起的误报。
- **有序数据**：当归一化变化超过阈值 $C_o$ 时产生事件。
- **名义数据**：当类别发生变化时产生事件。

事件定义为三元值 $p_i \in \{+1, -1, 0\}$，分别表示正事件、负事件和无事件。事件预测损失按模态区分：有序数据使用交叉熵，视觉和名义数据使用焦点损失（Focal Loss），以应对类别不平衡。

### 损失函数设计

EAWM 的总损失由基础世界模型损失 $\mathcal{L}_{\text{WM}}(\theta)$ 与事件感知损失 $\mathcal{L}_{\text{EA}}(\theta)$ 加权求和：
$$\mathcal{L}(\theta) \doteq \mathcal{L}_{\text{WM}}(\theta) + \mathcal{L}_{\text{EA}}(\theta) = \mathcal{L}_{\text{WM}}(\theta) + \beta_o \mathcal{L}_o(\theta) + \beta_e \mathcal{L}_e(\theta)$$

其中 $\mathcal{L}_o(\theta)$ 为事件感知的观测损失——当 GES 检测到事件边界时，通过权重 $\omega$ 将注意力重新分配到无事件区域；$\mathcal{L}_e(\theta)$ 为事件预测损失。GES 通过确定性门控函数 $g(\alpha_t^{(m)}, \alpha_{\text{thr}}^{(m)})$ 在事件边界处抑制事件预测，使模型在边界时刻更关注原始观测重建。

### 实例化：EADream 与 EASimulus

EAWM 的通用性体现在其对不同世界模型架构的统一适配：

- **EADream**：基于 DreamerV3，采用 RSSM-OP 动态模型（直接从先验状态预测未来观测），GES 使用简单的指示函数 $g(\alpha_t^{(m)}, \alpha_{\text{thr}}^{(m)}) = \mathbb{I}(\alpha_t^{(m)} < \alpha_{\text{thr}}^{(m)})$。其观测编码器结构如 Table 3 所示，以 CBAM 注意力模块起始，经四阶段卷积（4×4 核、stride=2、通道数 32→256）配合 LayerNorm+SiLU，最终 Flatten 为 4096 维嵌入。

- **EASimulus**：基于 Transformer 架构的 Simulus，GES 输出随事件稀疏度增加而增大，以更好凸显稀疏事件。

两种实例化均在各自基准上取得显著提升，验证了框架的广泛适用性。训练开销方面，EADream 仅比 DreamerV3 增加约 11–13%，EASimulus 比 Simulus 增加约 14–17%，在可接受范围内。

## 核心模块与公式推导

### 3.1 事件感知世界模型（EAWM）框架

EAWM并非一个独立的模型架构，而是一个可嵌入不同世界模型的通用框架。其核心设计思想是将世界模型的训练目标从单纯重建原始观测，转向同时预测自动生成的事件流，从而通过信息瓶颈优化将表示空间约束到与决策相关的有意义的时空变换上。

框架由以下关键模块构成（参见Figure 3）：

- **表示模型（Representation Model）**：将当前观测 $\mathbf{o}_t$ 与序列模型的隐状态 $\mathbf{h}_t$ 编码为嵌入向量 $\mathbf{z}_t$：
  $$\mathbf{z}_t \sim q_\theta(\mathbf{z}_t \mid \mathbf{o}_t, \mathbf{h}_t)$$

- **序列模型（Sequence Model）**：基于历史嵌入 $\mathbf{Z}_{t-1} = [\mathbf{z}_{t-k}, \dots, \mathbf{z}_{t-1}]$ 和动作 $\mathbf{A}_{t-1} = [\mathbf{a}_{t-k}, \dots, \mathbf{a}_{t-1}]$，输出隐状态 $\mathbf{h}_t$ 和汇总输出 $\mathbf{y}_t$：
  $$\mathbf{h}_t, \mathbf{y}_t = \mathbf{F}_\theta(\mathbf{h}_{t-1}, \mathbf{Z}_{t-1}, \mathbf{A}_{t-1})$$

- **动力学预测器（Dynamics Predictor）**：从序列输出 $\mathbf{y}_t$ 预测下一个嵌入：
  $$\hat{\mathbf{z}}_t \sim p_\theta(\hat{\mathbf{z}}_t \mid \mathbf{y}_t)$$

- **观测预测器（Observation Predictor）**：结合 $\mathbf{y}_t$ 和 $\hat{\mathbf{z}}_t$ 预测下一观测 $\hat{\mathbf{o}}_t$。

- **奖励预测器（Reward Predictor）** 与 **持续预测器（Continuation Predictor）**：分别预测奖励和episode终止信号。

- **事件预测器（Event Predictor）**：从序列输出和嵌入中预测事件类别，是EAWM的核心新增模块。

- **通用事件分割器（Generic Event Segmentor, GES）**：自动检测事件边界，门控事件预测损失并调整观测损失，不引入任何额外可训练参数。

### 3.2 事件生成

EAWM采用自动化的事件生成器，针对不同模态的观测数据生成事件标签。

**视觉事件**：基于自适应高斯混合模型（AGMMs），对每个像素 $(x_i, y_i)$ 的对数亮度 $L_t(x_i, y_i)$ 建模为 $K$ 个高斯分布的混合：
$$p(L_t(x_i, y_i)) = \sum_{k=1}^{K} w_{k,t,i} \mathcal{N}(L_t(x_i, y_i); \mu_{k,t,i}, \Sigma_{k,t,i})$$

当模型对下一帧的亮度感到“惊讶”（马氏距离大）或“不确定”（权重低）时触发事件。触发条件为：
$$p_i = \begin{cases} +1, & \text{if } L_t(x_i,y_i) - L_{t-1}(x_i,y_i) > C_I \\ -1, & \text{if } L_t(x_i,y_i) - L_{t-1}(x_i,y_i) < -C_I \\ 0, & \text{otherwise} \end{cases}$$
其中 $C_I$ 为亮度变化阈值，马氏距离定义为：
$$D_{k,i} = \left( L_{t+1}(x_i, y_i) - \mu_{k,t,i} \right)^{\top} \Sigma_{k,t,i}^{-1} (L_{t+1}(x_i, y_i) - \mu_{k,t,i})$$

**有序数据事件**：对有序观测维度，当归一化变化超过阈值 $C_o$ 时触发：
$$p_i = \begin{cases} +1, & \text{if } (o_t(i) - o_{t-1}(i)) / \text{Range}(o_i) > C_o \\ -1, & \text{if } (o_t(i) - o_{t-1}(i)) / \text{Range}(o_i) < -C_o \\ 0, & \text{otherwise} \end{cases}$$

**名义数据事件**：当类别标签发生变化时直接触发事件。

### 3.3 事件预测损失与GES门控

**事件预测损失**：事件预测器对每个模态 $m$ 输出预测 $\hat{p}_i^{(m)}$，损失函数根据数据类型选择：
$$\mathcal{L}_{\mathrm{e}}^{(m)}(\theta) = \begin{cases} \sum_{i=1}^{N^m} \mathrm{CrossEntropy}(p_i^{(m)}, \hat{p}_i^{(m)}) & \text{if } m \in \mathscr{D}_o \\ \sum_{i=1}^{N^m} \mathrm{Focal}(p_i^{(m)}, \hat{p}_i^{(m)}) & \text{if } m \in \mathscr{D}_I \cup \mathscr{D}_n \end{cases}$$
其中 $\mathscr{D}_o$ 为有序数据，$\mathscr{D}_I$ 为视觉数据，$\mathscr{D}_n$ 为名义数据。对视觉和名义数据使用Focal Loss以缓解类别不平衡。总事件损失为各模态损失的加权和：
$$\mathcal{L}_{\mathrm{e}}'(\theta) \doteq \sum_{m=1}^{M} \beta_{\mathrm{e}}^{(m)} \mathcal{L}_{\mathrm{e}}^{(m)}(\theta)$$

**通用事件分割器（GES）**：GES基于事件占比 $\alpha_t^{(m)}$（事件像素占总像素的比例）与阈值 $\alpha_{\mathrm{thr}}^{(m)}$ 的关系，输出门控信号 $g(\alpha_t^{(m)}, \alpha_{\mathrm{thr}}^{(m)})$。当 $\alpha_t^{(m)}$ 超过阈值时，GES判定当前帧处于事件边界，此时抑制事件预测损失，并将观测损失的权重重新分配到无非事件区域。GES为确定性函数，不引入可训练参数。

**总损失函数**：EAWM的总损失由基础世界模型损失 $\mathcal{L}_{\mathrm{WM}}$ 和事件感知损失 $\mathcal{L}_{\mathrm{EA}}$ 组成：
$$\mathcal{L}(\theta) \doteq \mathcal{L}_{\mathrm{WM}}(\theta) + \beta_o \mathcal{L}_o(\theta) + \beta_e \mathcal{L}_e(\theta)$$
其中 $\mathcal{L}_o$ 为经GES调整的事件感知观测损失，$\mathcal{L}_e$ 为经GES门控的事件预测损失，$\beta_o$ 和 $\beta_e$ 为权重系数。智能体的行为完全从世界模型生成的想象轨迹中学习，无需额外的环境交互。

## 实验与分析

### 核心性能验证

EAWM在两个主流基准上均刷新了最强基线。在**Atari 100K**（26款游戏）上，EASimulus的均值人类归一化分数（HNS）达到**1.818**，较原版Simulus（1.609）提升13.0%，成为首个在MBRL方法中达到超人级IQM分数的模型（Table 1）。在**DeepMind Control Suite 500K**的10个困难任务上，EADream以**723.8**的均值分数和**805.3**的中位数分数全面超越DreamerV3（606.3），提升幅度达19.4%（Table 2）。


![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_OWkkFaq1IZ/figures/007_Table_1.jpg]]
*Table 1: Game scores and human normalized aggregate metrics on the 26 games of the Atari 100K benchmark. We highlight the highest and the second highest scores among all baselines in bold and with underscores, respectively. The results on Atari 100k are based on the established re-implementation of the original version of DreamerV3 (Hafner et al., 2023) in PyTorch using the default hyperparameters. We follow the official implementation of Simulus (Cohen et al., 2025) and reproduce the results based on the suggested hyperparameters. All results of our experiments are reported over 5 seeds*

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_OWkkFaq1IZ/figures/008_Table_2.jpg]]
*Table 2: Scores achieved across ten challenging tasks from DeepMind Control Suite with a budget of 500K interactions. We highlight the highest and the second highest scores among all baselines in bold and with underscores, respectively*

### 泛化能力与鲁棒性

在视觉干扰基准**DMC-GB2**上，EADream未做任何针对性调整，仅凭事件感知机制即展现出强泛化能力：在Color Hard（6任务）上均值分数从456提升至**750**（+64.5%），在Video Hard（6任务）上从343提升至**477**（+39.1%），显著优于专门设计的视觉泛化方法**SADA**（Almuzairee et al., 2024）。这一结果表明，事件预测通过信息瓶颈优化将表示空间约束到有意义的时空转变上，有效抑制了纹理、颜色等虚假变化的干扰。

### 消融实验：关键组件贡献

消融实验揭示了两个核心组件的因果作用：

- **移除事件预测器**：在6款Atari游戏上，Simulus和EADream的均值HNS均下降约**0.4**（Figure 4a），证实事件预测信号对学习鲁棒表示至关重要。
- **移除观测预测**：在4个DMC任务上，平均分数从**737.2骤降至519.5**（Figure 5），说明即使有事件预测，保留观测重建作为辅助目标仍对维持表示质量不可或缺。


![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_OWkkFaq1IZ/figures/012_Figure_5.jpg]]
*Figure 5: Ablation studies on key components of EAWM on DeepMind Control Suite*

### 超参数鲁棒性

方法对关键超参数不敏感。在事件阈值$C_I$和事件权重$\omega$的不同取值下，EADream始终显著优于DreamerV3（Tables 14–15），表明事件生成与损失加权机制具有良好的稳定性，无需针对每个任务精细调参。

### 训练开销

EADream的训练时间仅比DreamerV3多**11–13%**，EASimulus比Simulus多约**14–17%**，在可接受范围内，未引入显著的计算负担。

### 定性分析

Figure 1展示了EAWM在想象步第9步的预测效果：尽管想象帧在物体位置上可能与真实值存在偏差，事件预测器仍能**一致地定位空间边界**。这直观验证了事件预测并非简单复制观测重建的结果，而是独立捕获了反映关键动态的时空转变——这正是EAWM在长时预测和策略学习中保持鲁棒性的核心机制。

### 补充图表

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_OWkkFaq1IZ/figures/005_Figure_2.jpg]]
*Figure 2: Overview. EAWM surpasses existing model-free and model-based RL across 55 test tasks, encompassing both continuous and discrete control, as well as multi-modal observations. (a) Mean human-normalized scores and the 95% stratified bootstrap confidence intervals (Agarwal et al., 2021) on the 26 tasks of Atari 100K. (b) Percentage of scores against the maximum score in Craftax. (c) Mean returns on 10 challenging tasks from DeepMind Control Suite. (d) Mean returns over 6 tasks on 3 test environments from DMC-GB2*

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_OWkkFaq1IZ/figures/010_Figure_4.jpg]]
*Figure 4: Ablation studies on key components of EAWMs with 5 random seeds over 6 Atari games: Assault, Breakout, Gopher, Krull, and Ms Pacman, Up N Down. The results show Simulus with the solid lines and EADream with the dashed lines*


## 方法谱系与知识库定位

### 方法定位与核心创新

EAWM并非一种独立的模型架构，而是一个**通用的事件感知框架**，可赋予不同类型的世界模型对抽象事件的理解能力。其核心创新在于将世界模型的训练目标从重建原始观测转向预测自动生成的事件流，通过信息瓶颈优化将表示空间约束到与决策相关的时空转变上。

EAWM在现有基于模型强化学习的谱系中引入了一个关键的因果调节旋钮：**世界模型是否明确捕获并预测观测流中反映有意义时空变换的“事件”**。这一设计直接针对现有方法（如DreamerV3、Simulus）的根本瓶颈——过度依赖原始观测重建，导致长时预测不准确、策略学习信息冗余，且易受纹理、颜色等虚假变化干扰。

### 与基线方法的关系

**DreamerV3**（Hafner et al., 2025）是EAWM的主要改造基础之一。EADream在DreamerV3的RSSM架构上增加了事件预测器和通用事件分割器，并将动力学模型修改为直接从先验状态预测观测（RSSM-OP）。在DeepMind Control Suite 500K的10个困难任务上，EADream将DreamerV3的平均分数从606.3提升至723.8（+19.4%）；在DMC-GB2 Color Hard上，提升幅度达64.5%（750 vs 456）。

**Simulus**（Cohen et al., 2025）是另一个被EAWM增强的强基线。Simulus本身是基于Transformer的世界模型，EASimulus在其基础上集成事件预测与GES后，在Atari 100K的26个游戏上取得了1.818的平均人类标准化分数（HNS），较Simulus的1.609提升了13.0%，并首次在基于模型的方法中达到超人类的IQM分数。

**HarmonyDream**作为DreamerV3的此前最优变体，在Atari 100K上被EADream超越。**DyMoDreamer**（Zhang et al., 2025）同样利用时间差分信息，但EAWM通过事件预测的信息瓶颈优化实现了更本质的表示约束。

在视觉泛化基准DMC-GB2上，**SADA**（Almuzairee et al., 2024）是专门设计的视觉泛化方法，而EADream未做任何针对性调整即直接迁移，在Color Hard和Video Hard上均显著超越SADA。

在模型无关方法方面，EAWM在Atari 100K上超越了**DIAMOND**和**REM**，在DMC上超越了**CURL**和**DrQ-v2**；在基于模型的方法中，同样超越了**TD-MPC2**。

### 适用边界

EAWM的适用性已在以下维度得到验证：

- **控制类型**：离散控制（Atari 26个游戏）和连续控制（DeepMind Control Suite 10个任务、Craftax）
- **观测模态**：视觉输入（图像）、有序数据（向量观测）、名义数据（离散状态），以及多模态组合
- **世界模型架构**：基于RSSM的Dreamer变体和基于Transformer的Simulus，表明框架对不同序列建模骨干具有通用性
- **数据效率**：100K（Atari）、500K（DMC）、1M（Craftax）交互预算下均有效
- **视觉干扰**：颜色随机化和视频背景替换下表现出鲁棒性

当前框架的边界在于：事件生成中的阈值$C_I$和$C_o$在所有基准测试中固定，未针对各任务单独优化；GES目前为确定性门控函数，尚未用神经网络直接建模。

### 局限与未解决问题

1. **GES的表达能力受限**：通用事件分割器当前为确定性门控函数$g(\alpha_t, \alpha_{thr})$，不引入额外可训练参数。虽然这保证了简洁性和鲁棒性，但限制了其自适应建模事件边界的表达能力。用神经网络直接建模GES是明确的改进方向。

2. **跨任务事件知识共享未实现**：EAWM尚未构建能够同时解决多类任务的统一世界模型。不同任务间的事件常识（如物体运动、碰撞等动力学特征）如何有效共享仍是一个开放挑战。

3. **训练开销增加**：EADream训练时间比DreamerV3多约11-13%，EASimulus比Simulus多约14-17%。虽然可控，但在大规模部署时仍需关注。

4. **事件生成阈值固定**：$C_I$和$C_o$在所有基准上使用统一值，可能未达到各任务的最优配置。自适应阈值机制值得探索。

5. **神经科学机制待探索**：论文指出上丘（SC）神经元如何处理动力学特征的具体机制仍待研究，这暗示事件感知的生物学基础尚未完全映射到计算模型。

6. **与大规模预训练模型的结合**：将EAWM的事件感知机制与大型预训练视觉-语言模型结合，以增强跨模态泛化与基础能力，是一个有前景但尚未探索的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/From_Observations_to_Events_Event_Aware_World_Models_for_Reinforcement_Learning.pdf]]
