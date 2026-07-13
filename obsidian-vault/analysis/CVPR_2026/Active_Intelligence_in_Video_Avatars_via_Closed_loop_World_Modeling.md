---
title: Active Intelligence in Video Avatars via Closed-loop World Modeling
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Active_Intelligence_in_Video_Avatars_via_Closed_loop_World_Modeling.pdf
project_link: "https://xuanhuahe.github.io/ORCA/"
code_link: null
aliases:
- OORCA
- AIVACLWM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入内部世界模型驱动的闭环OTAR循环，在每次生成后通过Reflect阶段验证预测结果与实际输出，并据此更新信念状态，从而防止生成误差的累积。
primary_logic: 将视频化身控制形式化为部分可观测马尔可夫决策过程（POMDP），将I2V模型作为世界模拟器，并采用层次化双系统架构分离高级策略规划与低级动作接地，使得智能体能够在部分可观测且高度随机的环境中实现稳健的多步任务执行。
claims:
- ORCA在L-IVA基准上的平均任务成功率(TSR)达71.0%，显著优于开环(62.3%)、反应式(50.9%)和VAGEN(61.2%)基线。
- ORCA获得最高的物理可行性评分(PPS) 3.72，验证了闭环状态跟踪对物体持久性和空间一致性的正面作用。
- 消融实验表明，移除信念状态跟踪(w/o Belief State)导致任务成功率大幅下降至0.67；移除反思(w/o Reflect)导致主题一致性下降和人类偏好负增长(-20.0%)。
- 人类评估通过Best-Worst Scaling排名ORCA显著高于所有基线，验证了主动智能在长程任务整体质量上的优势。
---

# Active Intelligence in Video Avatars via Closed-loop World Modeling

> [!tip] 核心洞察
> 将视频化身控制形式化为部分可观测马尔可夫决策过程（POMDP），将I2V模型作为世界模拟器，并采用层次化双系统架构分离高级策略规划与低级动作接地，使得智能体能够在部分可观测且高度随机的环境中实现稳健的多步任务执行。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过闭环世界建模实现视频化身的主动智能 |
| 英文题名 | Active Intelligence in Video Avatars via Closed-loop World Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.20615) · [Project](https://xuanhuahe.github.io/ORCA/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ORCA (Online Reasoning and Cognitive Architecture) |
| Dataset | L-IVA, Workshop |

> [!tip] 效果简介
> - L-IVA (Average over 5 scenarios) 上，Task Success Rate (TSR) 71.0% vs 62.3% (Open-Loop) (+8.7%)；Physical Plausibility Score (PPS) 3.72 vs 3.17 (Open-Loop) (+0.55)；Subject Consistency 0.93 vs 0.90 (Open-Loop) (+0.03)。
> - Workshop (Ablation subset) 上，Task Success Rate (TSR) 0.77 (ORCA Full) vs 0.67 (w/o Belief State) (+0.10)；Human Preference (BWS) 26.7% (ORCA Full) vs -20.0% (w/o Reflect) (+46.7%)。

## 概要

当前视频化身（video avatar）生成方法——无论是语音驱动还是姿态驱动——本质上是被动式的动画系统，缺乏对环境的语义理解和主动任务执行能力。尽管图像到视频（I2V）生成模型已取得显著进展，但在随机化生成环境中，这些方法无法进行闭环状态跟踪与验证，导致误差累积，难以自主完成长期目标导向的多步任务。

本文提出 **ORCA（Online Reasoning and Cognitive Architecture）**，一种通过闭环世界建模实现视频化身主动智能的框架。其核心洞察在于：将视频化身控制形式化为**部分可观测马尔可夫决策过程（POMDP）**，将I2V模型作为世界模拟器，并引入**内部世界模型（Internal World Model, IWM）**驱动的闭环推理循环，使智能体能够在部分可观测且高度随机的生成环境中实现稳健的多步任务执行。

ORCA 的方法定位体现在三个关键设计上：

1. **闭环 OTAR 循环**：区别于开环规划（Open-Loop）或简单的观察-行动循环（ReAct-style），ORCA 采用 Observe-Think-Act-Reflect 四阶段闭环，在每次生成后通过 Reflect 阶段验证预测结果与实际输出的一致性，据此更新信念状态，从而防止生成误差的累积。
2. **层次化双系统架构**：System 2 负责高层战略推理与状态预测，维护包含场景信息、历史记录和任务清单的信念状态 $\hat{s}_t$；System 1 将抽象子目标翻译为针对特定 I2V 模型的细粒度动作字幕，实现精确的动作接地（action grounding）。
3. **POMDP 形式化建模**：将长程视频化身任务（L-IVA）定义为包含状态、动作、转移、奖励、观察空间和观察函数的 POMDP 元组，为闭环决策提供理论框架。

在专门构建的 **L-IVA 基准**（覆盖 5 个场景类别、平均每任务 5.0 个子目标）上，ORCA 取得了显著优势：平均任务成功率（TSR）达 **71.0%**，较开环规划基线（62.3%）提升 8.7 个百分点，较 VAGEN-style 基线（61.2%）提升 9.8 个百分点；物理可行性评分（PPS）达 **3.72**，验证了闭环状态跟踪对物体持久性和空间一致性的正面作用；人类偏好评估（Best-Worst Scaling）中，ORCA 以 **28.7%** 的 BWS 得分显著高于所有基线。消融实验进一步证实，移除信念状态跟踪导致任务成功率大幅下降至 0.67，移除反思机制则导致人类偏好出现负增长（-20.0%），验证了各核心组件的必要性。

目前，ORCA 仍受限于基础模型的固有缺陷，包括 VLM 的时域采样损失和 3D 空间感知缺失，以及 I2V 模型在细粒度操作上的指令跟随弱和物体持久性问题。这些限制指明了未来工作的方向：增强 VLM 的视频理解与空间推理能力，以及通过反馈学习改进 I2V 模型的长期一致性。

视频化身（Video Avatar）的生成正从被动驱动的动画范式向主动任务执行范式演进。传统方法依赖语音或姿态信号驱动，仅能生成语义理解有限的被动动作，无法支持需要多步交互的复杂任务。近期研究尝试利用视觉-语言模型（VLM）为图像到视频（I2V）生成模型提供高层指令，使化身具备初步的任务执行能力。然而，这一技术路线面临一个核心瓶颈：**当前方法缺乏内部世界模型（Internal World Model, IWM），无法在随机化的生成环境中进行闭环状态跟踪与验证**。

具体而言，现有方法可归为三类范式，各自存在结构性缺陷：

- **开环规划（Open-Loop Planner）**：在执行前一次性规划完整动作序列，生成过程中无任何反馈机制。一旦I2V模型产生物理错误或对象丢失，误差将不可逆地累积，导致任务整体失败。
- **反应式智能体（Reactive Agent）**：采用观察-行动（observe-act）循环，如ReAct（Yao et al., 2023），每步仅基于当前观察做出反应。然而，缺乏对全局状态的信念跟踪和历史记忆，使得智能体容易陷入重复动作或遗忘已完成的子目标。
- **世界模型推理（VAGEN-style CoT, Wang et al., arXiv 2025）**：引入状态估计和转移预测，但假设环境是确定性的，未考虑I2V生成的固有随机性。当实际生成结果偏离预测时，缺乏反思（Reflect）与修正机制，信念状态会被污染并传播至后续步骤。

上述方法的共同缺陷在于：**将I2V模型视为确定性执行器，而忽略了其作为随机世界模拟器的本质**。在部分可观测且高度随机的生成环境中，智能体必须持续验证预测结果与实际输出的一致性，否则信念状态将迅速偏离真实世界状态，导致任务执行不可靠。

针对这一缺口，本文提出ORCA（Online Reasoning and Cognitive Architecture），将视频化身控制形式化为**部分可观测马尔可夫决策过程（POMDP）**，并将I2V模型作为世界模拟器。核心动机在于：赋予智能体一个可更新的内部世界模型，使其能够在闭环中持续跟踪状态、验证生成结果，并在必要时进行自适应重规划，从而在长程多步任务中实现稳健的执行能力。

## 核心方法与创新机理

ORCA 的核心创新在于将视频化身控制重新定义为**部分可观测马尔可夫决策过程（POMDP）**，并围绕“闭环世界建模”构建了完整的认知架构，从而解决了现有方法在随机化生成环境中无法进行长期目标导向任务的瓶颈。其关键创新点可概括为三个相互耦合的 changed slots：

### 1. 闭环 OTAR 执行范式：从开环规划到自适应验证

现有视频化身生成方法主要采用两种范式：**Open-Loop Planner** 预先规划完整动作序列后无反馈执行，或 **Reactive Agent**（如 ReAct, Yao et al., 2023）进行简单的观察-行动循环。这两种范式均缺乏对生成结果与预期状态之间偏差的检测与修正能力，导致误差沿时间步累积。

ORCA 引入了 **OTAR（Observe-Think-Act-Reflect）闭环循环**（Sec 3.2.1），其核心机制是在每次 I2V 生成后执行 **Reflect 阶段**：System 2 将生成结果 $o_{t+1}$ 与预测状态 $g_{\hat{s}}$ 进行比对验证，决定接受或拒绝当前输出，并在必要时触发修正或重规划。这一机制从根本上阻断了生成误差的累积路径——当 I2V 模型产生不符合预期的输出时，系统能够检测到偏差并自适应调整后续策略，而非将错误状态作为下一轮推理的基础。

消融实验为这一创新提供了决定性证据：移除 Reflect 机制后，人类偏好评分（BWS）出现 **-20.0%** 的负增长，且主题一致性显著下降（Table 2, Sec 5.4），证实了闭环验证对维持长程生成质量的关键作用。

### 2. 层次化双系统架构：分离战略推理与动作接地

现有方法通常采用**单层 VLM** 直接生成动作提示（如 VAGEN 的思维链推理），这导致高层任务规划与底层生成控制耦合在同一个推理过程中，难以兼顾全局一致性与局部精确性。

ORCA 采用**层次化双系统架构**（Sec 3.2.2），将认知过程分离为两个功能互补的子系统：

- **System 2（战略推理层）**：维护**信念状态** $\hat{s}_t$（包含场景信息、历史记录 $h_t$ 和任务清单 $C$），负责评估任务进展、分解意图为子目标 $g_t$，并预测执行后的下一个状态 $g_{\hat{s}}$。其策略函数为 $g_t, g_{\hat{s}} = \pi_{\mathrm{Sys2}}(\hat{s}_t, I)$。

- **System 1（动作接地层）**：接收 System 2 输出的抽象子目标和预测状态，将其翻译为**针对特定 I2V 模型 $G_{\theta}$ 的细粒度动作字幕** $a_t$。其接地策略为 $a_t = \pi_{\mathrm{Sys1}}(g_t, g_{\hat{s}}, o_t, \hat{s}_t)$。

这一分离设计的优势在于：System 2 可以专注于高层任务推理而不被生成细节干扰，System 1 则通过精心设计的提示工程将抽象意图转化为 I2V 模型能够精确执行的动作描述。消融实验表明，移除 System 1 的详细动作接地后，任务成功率和人类偏好均显著下降（Sec 5.4），验证了层次化分工对执行精度的贡献。

### 3. 信念状态驱动的内部世界模型：从无状态到持续状态跟踪

现有方法或**无显式状态跟踪**（如 Reactive Agent 仅基于当前观察决策），或将环境**假设为确定性**（如 VAGEN 进行状态估计和转移预测但忽略生成随机性）。这使得系统无法在部分可观测且高度随机的 I2V 生成环境中维持对任务进展的准确认知。

ORCA 将信念状态 $\hat{s}_t$ 作为内部世界模型的核心表示（Sec 3.2.2, Eq 3），通过 Observe 模块持续更新：$\hat{s}_t = f_{\mathrm{observe}}(o_t, \hat{s}_{t-1})$。信念状态不仅记录当前观察到的场景信息，还维护历史交互记录和任务清单完成状态，使系统始终知晓“已完成什么、还需做什么”。

这一创新的决定性证据来自消融实验：移除信念状态跟踪（w/o Belief State）后，任务成功率从 0.77 大幅下降至 0.67（Table 2, Sec 5.4），表明持续的状态跟踪是长程任务成功的基础保障。物理可行性评分（PPS）达到最高的 3.72（Table 1），也进一步验证了信念状态对维持物体持久性和空间一致性的正面作用。

### 创新协同效应

上述三个 changed slots 并非孤立存在，而是形成协同增强效应：**信念状态**为 System 2 的战略推理提供记忆基础，**双系统架构**将推理结果高效转化为可执行动作，**OTAR 闭环**则确保每一步执行结果都经过验证才更新信念状态。这一设计使得 ORCA 在 L-IVA 基准上的平均任务成功率（TSR）达到 **71.0%**，显著优于开环（62.3%）、反应式（50.9%）和 VAGEN（61.2%）基线，并在人类偏好评估中获得最高的 BWS 评分（28.7%），验证了闭环世界建模驱动的主动智能在长程视频化身任务上的显著优势。

ORCA（Online Reasoning and Cognitive Architecture）将长程视频化身控制形式化为部分可观测马尔可夫决策过程（POMDP），并以预训练的图像到视频（I2V）模型作为世界模拟器。其核心创新在于引入**内部世界模型（Internal World Model, IWM）**，通过闭环的 **OTAR 循环**（Observe-Think-Act-Reflect）在高度随机的生成环境中维持稳健的状态跟踪与自适应重规划。

### 层次化双系统架构

框架采用层次化双系统设计，分离高级策略规划与低级动作接地：

- **System 2（战略推理层）**：负责维护 IWM 的高层信念状态 $\hat{s}_t$，该状态包含场景信息、历史记录 $h_t$ 和任务清单 $C$。System 2 在 Observe、Think 和 Reflect 阶段运作，评估任务进展、分解意图为子目标，并预测下一个状态。
- **System 1（动作接地层）**：将 System 2 输出的抽象子目标 $g_t$ 和预测状态 $g_{\hat{s}}$ 翻译为针对特定 I2V 模型 $G_{\theta}$ 的精细动作字幕 $a_t$，通过提示工程确保生成指令的可执行性。

### OTAR 闭环循环

ORCA 的每一步生成均遵循以下闭环流程，以防止生成误差的累积：

1. **Observe（观察）**：System 2 分析最新生成的视频片段 $o_t$，更新信念状态中的场景变化和任务进展：
   $$\hat{s}_{t} = f_{\mathrm{observe}}(o_{t}, \hat{s}_{t-1})$$

2. **Think（思考）**：System 2 基于当前信念状态 $\hat{s}_t$、用户意图 $I$ 和观察 $o_t$，规划下一个动作并预测结果状态：
   $$g_{t}, g_{\hat{s}} = f_{\mathrm{think}}(\hat{s}_{t}, I, o_{t})$$

3. **Act（行动）**：System 1 将多模态意图转化为可执行的动作字幕 $a_t$，并调用 I2V 模型生成下一视频片段：
   $$v_{t+1} \sim G_{\theta}(o_{t}, a_{t})$$

4. **Reflect（反思）**：System 2 验证生成结果 $o_{t+1}$ 是否与预测状态 $g_{\hat{s}}$ 一致，决定接受或拒绝该生成，并在必要时触发修正或重规划：
   $$\delta_{t}, \mathrm{analysis} = f_{\mathrm{reflect}}(o_{t+1}, g_{t}, g_{\hat{s}})$$

该循环的关键在于 Reflect 阶段充当“验证器”，在每次生成后比对预测与实际输出，从而防止随机化生成导致的信念状态污染。Figure 2 展示了完整的框架总览。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2512_20615/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the ORCA framework. ORCA operates through a closed-loop OTAR cycle: Observe updates internal world state from generated clips, Think (System 2) decomposes tasks and predict next state, Act (System 1) translates subgoals into action captions for I2V generation, and Reflect verifies completion to accept/reject outcomes. This hierarchical dual-system architecture enables robust long-horizon task execution through continuous state tracking and adaptive replanning*

### 与基线的关键差异

| 维度 | 开环规划器 | 反应式智能体 (ReAct) | VAGEN 式 CoT | **ORCA** |
|------|-----------|---------------------|-------------|----------|
| 执行范式 | 预先规划完整序列，无反馈 | 简单 observe-act 循环 | 状态估计与转移预测，假设环境确定性 | **闭环 OTAR 循环，每步验证与自适应重规划** |
| 规划架构 | 单层 VLM 直接生成动作 | 单层 VLM 直接生成动作 | 单层世界模型推理 | **层次化双系统：System 2 战略推理 + System 1 动作接地** |
| 状态表示 | 无显式状态跟踪 | 仅基于当前观察 | 状态估计但无持续更新 | **信念状态 $\hat{s}_t$，包含场景信息、历史与任务清单** |
| 动作规范 | 抽象高层指令 | 抽象高层指令 | 抽象高层指令 | **针对特定 I2V 模型的细粒度动作字幕** |

### 实现细节

ORCA 无需训练，完全基于预训练模型构建。其 VLM 推理引擎采用 Gemini-2.5-Flash，同时服务于 System 1 和 System 2；I2V 生成模型采用 Wanx2.2 配合蒸馏 LoRA。所有基线方法在实验中共享相同的模型底座和计算预算，确保对比的公平性。

ORCA 将长程视频化身控制形式化为部分可观测马尔可夫决策过程（POMDP），其核心由四个闭环模块构成 OTAR 循环，并由层次化双系统架构驱动。

### 闭环 OTAR 循环

ORCA 在每个时间步执行 **Observe → Think → Act → Reflect** 四阶段循环（Figure 2），以在随机化生成环境中维持稳健的状态跟踪。

**Observe（观察）**：System 2 分析最新生成的视频片段 $o_t$，更新内部信念状态 $\hat{s}_t$，该状态包含场景信息、历史记录 $h_t$ 和任务清单 $C$：

$$\hat{s}_t = f_{\mathrm{observe}}(o_t, \hat{s}_{t-1}) \quad \text{(Eq. 3)}$$

**Think（思考）**：System 2 基于当前信念状态 $\hat{s}_t$、高层意图 $I$ 和最新观察 $o_t$，将意图分解为子目标，并预测执行后的下一个状态：

$$g_t, g_{\hat{s}} = f_{\mathrm{think}}(\hat{s}_t, I, o_t) \quad \text{(Eq. 4)}$$

其中 $g_t$ 为文本子目标命令，$g_{\hat{s}}$ 为预测的下一个信念状态。

**Act（行动）**：System 1 将 System 2 输出的抽象子目标 $g_t$ 和预测状态 $g_{\hat{s}}$，结合当前观察 $o_t$ 和信念状态 $\hat{s}_t$，翻译为针对特定 I2V 模型 $G_\theta$ 的细粒度动作字幕 $a_t$：

$$a_t = \pi_{\mathrm{Sys1}}(g_t, g_{\hat{s}}, o_t, \hat{s}_t) \quad \text{(Eq. 2)}$$

随后调用 I2V 模型生成下一视频片段：

$$v_{t+1} \sim G_\theta(o_t, a_t) \quad \text{(Eq. 5)}$$

**Reflect（反思）**：System 2 验证生成结果 $o_{t+1}$ 是否与预测状态 $g_{\hat{s}}$ 和子目标 $g_t$ 一致：

$$\delta_t, \mathrm{analysis} = f_{\mathrm{reflect}}(o_{t+1}, g_t, g_{\hat{s}}) \quad \text{(Eq. 6)}$$

根据验证结果，决定接受生成、触发修正或重新规划，从而防止生成误差在信念状态中累积。

### 层次化双系统架构

ORCA 采用认知双系统设计，分离战略推理与低级动作接地：

- **System 2**（慢速推理）：负责 Observe-Think-Reflect 阶段，维持内部世界模型（IWM）的高层信念状态，评估任务进展，规划子目标并预测状态转移。其策略可表示为：

$$g_t, g_{\hat{s}} = \pi_{\mathrm{Sys2}}(\hat{s}_t, I) \quad \text{(Eq. 1)}$$

- **System 1**（快速接地）：负责 Act 阶段，将 System 2 的多模态意图 $(g_t, g_{\hat{s}})$ 转化为针对特定 I2V 模型 $G_\theta$ 的详细动作字幕。该模块通过提示工程实现，无需训练，确保动作描述与生成模型的输入格式精确对齐。

### 关键公式汇总

| 公式 | 含义 | 所属阶段 |
|------|------|----------|
| $\hat{s}_t = f_{\mathrm{observe}}(o_t, \hat{s}_{t-1})$ | 根据观察更新信念状态 | Observe |
| $g_t, g_{\hat{s}} = f_{\mathrm{think}}(\hat{s}_t, I, o_t)$ | 规划子目标并预测下一状态 | Think |
| $a_t = \pi_{\mathrm{Sys1}}(g_t, g_{\hat{s}}, o_t, \hat{s}_t)$ | 将抽象意图翻译为动作字幕 | Act |
| $v_{t+1} \sim G_\theta(o_t, a_t)$ | I2V 模型生成下一视频片段 | Act |
| $\delta_t, \mathrm{analysis} = f_{\mathrm{reflect}}(o_{t+1}, g_t, g_{\hat{s}})$ | 验证生成结果与预测的一致性 | Reflect |

**核心机制**：Reflect 阶段是 ORCA 区别于开环和简单反应式方法的关键——它通过持续验证预测结果与实际输出，在信念状态更新前过滤低质量生成，从而阻断误差累积链路。消融实验证实，移除 Reflect 会导致主题一致性下降和人类偏好负增长（-20.0%，Table 2）；移除信念状态跟踪则使任务成功率从 0.77 降至 0.67。

## 实验与关键发现

### 核心实验设置

ORCA 是一个免训练的框架，其核心组件均基于预训练模型构建：视觉语言模型（VLM）采用 **Gemini-2.5-Flash**，同时承担 System 1（动作接地）和 System 2（战略推理与状态预测）的角色；图像到视频（I2V）生成模型采用 **Wanx2.2** 配合蒸馏 LoRA。所有基线方法均使用相同的 VLM 和 I2V 模型，并保持相同的计算预算与提示优化，确保对比的公平性。

评估在 **L-IVA 基准** 上展开。该基准包含 5 类场景（Garden、Kitchen、Workshop 等），共 100 个测试样本（92 张合成图像 + 8 张真实图像），每个任务平均包含 5.0 个子目标，覆盖了需要多步物体交互的多样化真实世界场景（图 3）。评估维度涵盖任务完成度、执行质量、视频生成质量和人类偏好四个层面。

### 主实验结果

**任务完成度与执行质量**。Table 1(a) 报告了各方法在 5 个场景上的任务成功率（TSR）和物理可行性评分（PPS）。ORCA 在所有场景上的平均 TSR 达到 **71.0%**，显著优于开环规划器（62.3%）、反应式智能体（50.9%）和 VAGEN 风格的思维链方法（61.2%）。在物理可行性方面，ORCA 以 **3.72** 的平均 PPS 位居第一，相比开环基线（3.17）提升了 0.55 分，验证了闭环状态跟踪对物体持久性和空间一致性的正面作用。

**视频质量与人类偏好**。Table 1(b) 从视频质量和人类偏好角度进一步验证了 ORCA 的优势。ORCA 在主题一致性（Subject Consistency）上取得最高的 **0.93**，这得益于 Reflect 阶段主动过滤低质量生成。在基于 Best-Worst Scaling（BWS）的人类评估中，ORCA 的 BWS 得分达到 **28.7%**，而开环规划器为 -7.52%，反应式智能体和 VAGEN 分别为 -8.45% 和 -12.73%。ORCA 在所有对比中均被人类标注者显著偏好，表明闭环主动智能在长程任务整体质量上具有明确优势。

**定性对比**。图 4 以“Transfer Plant”任务为例，展示了四种方法的生成效果差异。开环规划器无法检测执行错误，导致错误累积；反应式智能体缺乏世界状态知识，出现重复动作；VAGEN 在 I2V 生成错误后无法通过反思纠正，最终状态被破坏。相比之下，ORCA 成功完成了所有子目标，并保持了一致的执行质量。

### 消融实验

为验证 ORCA 各组件的独立贡献，作者在 Workshop 场景上进行了消融实验（Table 2），分别移除信念状态跟踪（w/o Belief State）、反思机制（w/o Reflect）和 System 1 的详细动作接地（w/o System 1）。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2512_20615/figures/006_Table_2.jpg]]
*Table 2: Ablation on ORCA components. Note: To ensure fair comparison within ablation variants, we re-evaluated the Workshop scene. Minor variations in absolute scores compared to Table 1 are due to the stochastic nature of human evaluation*

- **移除信念状态跟踪**：任务成功率从完整 ORCA 的 0.77 大幅下降至 0.67，表明信念状态 $ \hat{s}_t $ 所维护的场景信息、历史记录 $ h_t $ 和任务清单 $ C $ 对于多步任务的一致性执行至关重要。
- **移除反思机制**：主题一致性下降，BWS 得分出现 **-20.0%** 的负增长。这说明 Reflect 阶段的验证与重规划机制是防止生成误差污染信念状态的关键屏障。
- **移除 System 1 的详细动作接地**：任务成功率和人类偏好均下降，验证了将抽象子目标翻译为针对特定 I2V 模型的细粒度动作字幕对于生成质量的重要性。

### 失败模式分析

尽管 ORCA 整体表现优异，其性能仍受限于底层基础模型的能力边界。图 6 归纳了四类典型失败案例：

1. **时域信息丢失**：VLM 采用离散帧采样，可能错过“瞬移”等瞬时伪影，导致 Reflect 阶段产生假阳性接受。
2. **缺乏 3D 空间感知**：VLM 无法准确判断场景深度，可能误判物体的可达性，生成无法执行的指令。
3. **弱指令跟随能力**：对于“点燃酒精灯”等细粒度操作，I2V 模型即使多次重试仍无法生成正确的物理交互。
4. **物体持久性问题**：I2V 模型固有的幻觉可能导致关键物体在生成片段中突然消失，破坏信念状态的正确性。

这些失败模式揭示了当前框架的上限瓶颈：ORCA 的闭环推理可以有效检测和纠正部分错误，但当底层 VLM 的感知能力或 I2V 模型的生成精度不足时，系统仍会失效。未来的改进方向包括增强 VLM 的时空理解能力，以及通过微调或反馈学习提升 I2V 模型的指令跟随精度和长期一致性。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2512_20615/figures/005_Table_1.jpg]]
*Table 1: Main Results on L-IVA Benchmark. All metrics are evaluated per scenario. (a) Task completion metrics. (b) Video quality and human preference. Best in bold*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2512_20615/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative Comparison on Transfer Plant Task. We compare four methods on long-horizon video generation. Top: Ground truth subgoals for reference. Red boxes indicate execution failures or error accumulation. Open-Loop planner cannot detect execution errors. Reactive agent lacks world state knowledge, leading to repetitive actions. VAGEN’s I2V errors corrupt the final state without reflection. ORCA (Ours) successfully completes all subgoals with consistent execution quality*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2512_20615/figures/003_Figure_3.jpg]]
*Figure 3: L-IVA Benchmark Overview. Top: Statistical analysis showing (left) balanced scene distribution across 5 categories, (center) data source composition with 92 synthetic and 8 real images, and (right) task complexity distribution averaging 5.0 sub-goals per task. Bottom: Representative scenes from our benchmark including Garden, Kitchen, and livestream scenarios, demonstrating diverse real-world settings requiring multi-step object interactions*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2512_20615/figures/007_Figure_5.jpg]]
*Figure 5: Overview of the L-IVA Benchmark Construction Pipeline. (a) Our data curation process employs a hybrid strategy: Pipeline A sources real-world images from Pexels, filtered by scene affordance and annotated via Gemini-2.5-Pro. Pipeline B utilizes a goal-first design for synthetic data, where scenes are generated by Nanobanana to strictly align with intended interactions. (b) A representative scene image (e.g., ”Checking beehives”) from the benchmark. (c) The corresponding structured metadata (YAML), including object inventory, high-level intention, subgoals, and reference prompts*

## 定位与知识库关联

### 问题定位：从被动动画到主动智能的视频化身

当前视频化身生成方法主要分为两类：**语音驱动**和**姿态驱动**的动画方法。这些方法将化身视为被动的信号转换器，仅将输入信号映射为面部或身体运动，缺乏对场景语义、物体交互和任务目标的理解（见 Figure 1）。另一条技术路线是**基于图像到视频（I2V）的生成方法**，利用扩散模型根据初始图像和文本指令生成视频片段。然而，现有 I2V 方法在长程任务生成中面临根本性瓶颈：**缺乏内部世界模型（Internal World Model, IWM）**，无法在随机化生成环境中进行闭环状态跟踪与验证，导致无法自主完成长期目标导向的任务。

ORCA 的核心洞察是将视频化身控制形式化为**部分可观测马尔可夫决策过程（POMDP）**，将 I2V 模型作为世界模拟器，并采用层次化双系统架构分离高级策略规划与低级动作接地。这一形式化使得智能体能够在部分可观测且高度随机的环境中实现稳健的多步任务执行。

### 基线方法谱系与 ORCA 的差异化

ORCA 与三类基线方法形成对比，每类代表不同的执行范式：

**1. 开环规划器（Open-Loop Planner）**

开环方法在任务开始时一次性规划完整动作序列，随后按序执行，无任何反馈机制。这类方法假设环境完全可预测，但 I2V 模型固有的生成随机性使得执行偏差逐步累积，最终导致任务失败。在 L-IVA 基准上，开环规划器的平均任务成功率仅为 62.3%，物理可行性评分 3.17。

**2. 反应式智能体（Reactive Agent）**

反应式方法（如 **ReAct**，Yao et al., 2023）采用观察-行动循环，每步根据当前观察做出反应，但缺乏显式的信念状态和反思机制。这类方法无法追踪历史交互和任务进展，容易产生重复动作或遗漏子目标。其任务成功率进一步下降至 50.9%，验证了无状态跟踪的局限性。

**3. 基于世界模型推理的方法（VAGEN-style CoT）**

**VAGEN**（Wang et al., arXiv 2025）引入了世界模型推理，通过链式思维（CoT）进行状态估计和转移预测。然而，VAGEN 假设环境是确定性的，缺乏对生成结果的实际验证。当 I2V 模型产生意外输出时，VAGEN 的错误状态预测会污染后续推理，导致任务失败。其任务成功率为 61.2%，虽优于开环和反应式方法，但仍显著低于 ORCA。

**ORCA 的关键差异化**体现在三个维度：

- **执行范式**：从开环或简单观察-行动循环升级为**闭环 OTAR 循环**（Observe-Think-Act-Reflect），每步进行结果验证与自适应重规划（见 Figure 2）。Reflect 阶段通过验证生成结果与预测状态的一致性，决定接受或拒绝输出，从而防止生成误差的累积。

- **规划架构**：从单层 VLM 直接生成动作提示升级为**层次化双系统架构**。System 2 负责战略推理与状态预测，维持信念状态 $\hat{s}_t$（包含场景信息、历史记录 $h_t$ 和任务清单 $C$）；System 1 将抽象子目标翻译为精细的、I2V 专用的动作字幕 $a_t$，通过提示工程适配特定 I2V 模型 $G_{\theta}$。

- **状态表示**：从无显式状态跟踪升级为**信念状态持续更新机制**。System 2 在每次 Observe 阶段根据最新生成视频片段 $o_t$ 更新信念状态 $\hat{s}_t = f_{\mathrm{observe}}(o_t, \hat{s}_{t-1})$，并在 Reflect 阶段验证后才正式接受状态更新，防止错误状态污染后续决策。

### 适用边界与基础模型依赖

ORCA 是**免训练**框架，其能力边界受限于底层基础模型的性能：

- **VLM 能力依赖**：ORCA 使用 Gemini-2.5-Flash 作为 System 1 和 System 2 的视觉语言模型。框架的观察、推理和反思质量直接取决于 VLM 的视觉理解和逻辑推理能力。

- **I2V 模型依赖**：视频生成使用 Wanx2.2 配合蒸馏 LoRA。ORCA 的闭环机制可以过滤低质量生成，但无法从根本上改善 I2V 模型本身的物理交互精度。

- **计算预算**：所有基线方法使用相同的 VLM 和 I2V 模型，并采用相同的计算预算和提示优化，确保公平比较。

### 已知局限与失败模式

ORCA 的局限性主要源于基础模型的能力边界，定性分析（Figure 6）揭示了四类典型失败模式：

**1. VLM 时域采样损失导致假阳性接受**

VLM 处理视频时采用离散帧采样，可能错过瞬时伪影（如物体的“瞬移”现象）。当 I2V 模型产生不自然的物体位置跳变但采样帧恰好未捕获时，Reflect 模块可能错误接受该生成结果，导致信念状态被污染。

**2. VLM 缺乏 3D 空间感知**

当前 VLM 缺乏深度和空间关系理解，可能误判物体可达性。例如，当目标物体位于场景深处或被遮挡时，VLM 可能生成无法执行的指令（如“拿起远处的工具”），而实际物理交互需要化身移动到合适位置。

**3. I2V 模型细粒度指令跟随能力弱**

对于精细操作任务（如“点燃酒精灯”），I2V 模型即使多次重试仍可能无法生成正确的物理交互。ORCA 的 Reflect 机制可以检测失败并触发重规划，但无法突破 I2V 模型本身的能力上限。

**4. I2V 模型固有的物体持久性问题**

生成式模型存在物体突然消失或多余物体出现的幻觉问题。关键物体的消失会直接影响信念状态的正确性，进而导致后续子目标无法完成。

### 开放问题与未来方向

基于上述局限，以下方向值得进一步探索：

1. **增强 VLM 的时空感知能力**：如何通过视频理解增强（如更高帧率采样、时序注意力机制）或 3D 感知模块（如深度估计、点云融合）来提升 VLM 在长程生成中的异常检测精度？

2. **改进 I2V 模型的指令跟随精度**：能否通过强化微调（RL fine-tuning）或人类反馈学习（RLHF）来提升 I2V 模型对细粒度动作字幕的执行精度和长期物体一致性？

3. **框架扩展至复杂动态场景**：ORCA 当前在室内可控场景中验证，如何扩展到室外环境或大规模、多视角动态场景？这需要更强的空间推理和更鲁棒的状态跟踪机制。

4. **多智能体协作场景**：当多个化身需要在共享环境中协作时，如何设计世界模型的共享与协调机制？信念状态是否需要部分共享或分层维护？

5. **主动学习与自我改进**：ORCA 的 Reflect 阶段产生的验证信号（接受/拒绝）是否可以作为反馈信号，用于在线微调 I2V 模型或优化 System 1 的动作接地策略，实现持续自我改进？

## 原文 PDF

![[paperPDFs/CVPR_2026/Active_Intelligence_in_Video_Avatars_via_Closed_loop_World_Modeling.pdf]]
