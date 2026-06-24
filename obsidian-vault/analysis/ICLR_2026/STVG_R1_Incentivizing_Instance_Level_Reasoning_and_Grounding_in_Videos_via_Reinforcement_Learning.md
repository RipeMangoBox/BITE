---
title: "STVG-R1: Incentivizing Instance-Level Reasoning and Grounding in Videos via Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/STVG_R1_Incentivizing_Instance_Level_Reasoning_and_Grounding_in_Videos_via_Reinforcement_Learning.pdf
openreview_forum_id: zuPxAZgT9F
aliases:
- SR
- STVG-R1
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "将复杂的逐帧坐标回归问题重新定义为基于视觉提示的紧凑实例ID识别任务，避免了直接学习跨模态坐标对齐，并利用强化学习的任务驱动奖励来联合优化时序精度、空间一致性和输出格式。"
primary_logic: "以对象为中心的视觉提示（在每个实例中心添加统一ID标记）为VLM提供了可解释的参考提示，使模型能够专注于实例识别而非坐标回归，从而在强化学习的奖励引导下，不仅提升了时空定位性能，还意外地泛化到多对象分割任务。"
claims:
- "在零样本设定下，视觉提示范式使多个通用VLM（Qwen2.5-VL-7B/72B, InternVL3-8B, Qwen3-VL-8B）的vIoU@0.3分别提升+12.5%, +6.0%, +3.6%, +28.3%。"
- "STVG-R1在HCSTVG-v2上比基座Qwen2.5-VL-7B的m IoU提升20.9%，并超越先前最佳模型SpaceVLLM，达到新的最佳结果。"
- "在未见的MeViS数据集上，仅用单对象STVG数据训练的STVG-R1取得了47.3% J&F，达到多对象视频对象分割的最佳性能。"
- "HCSTVG-v2 上 m_vIoU = 40.8"
---

# STVG-R1: Incentivizing Instance-Level Reasoning and Grounding in Videos via Reinforcement Learning

> [!tip] 核心洞察
> 以对象为中心的视觉提示（在每个实例中心添加统一ID标记）为VLM提供了可解释的参考提示，使模型能够专注于实例识别而非坐标回归，从而在强化学习的奖励引导下，不仅提升了时空定位性能，还意外地泛化到多对象分割任务。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | STVG-R1：通过强化学习激励视频中的实例级推理与定位 |
| 英文题名 | STVG-R1: Incentivizing Instance-Level Reasoning and Grounding in Videos via Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=zuPxAZgT9F); [Project](https://stvg-r1.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | STVG-R1 |
| Dataset | HCSTVG-v2, HCSTVG-v1, MeViS, ST-Align (STVG) |

> [!tip] 效果简介
> - HCSTVG-v2 上，m_vIoU 为 40.8，对比 19.3 (Qwen2.5-VL-7B)，变化 +21.5。
> - HCSTVG-v1 上，vIoU@0.3 为 66.7，对比 28.2 (Qwen2.5-VL-7B)，变化 +38.5。
> - MeViS 上，J&F 为 47.3，对比 45.2 (VideoGlaMM)，变化 +2.1。

## 概述

时空视频定位（Spatial-Temporal Video Grounding, STVG）要求模型根据自然语言查询，在视频中同时定位目标对象的时序区间和空间轨迹。现有视觉-语言模型（VLM）在该任务上面临一个根本性瓶颈：**跨模态错位导致的严重幻觉问题**——模型需要逐帧输出边界框坐标，这种密集回归范式极易产生时序不一致甚至无效的预测，使得通用VLM在STVG上表现远逊于专用模型。

STVG-R1 的核心洞察在于**将逐帧坐标回归重新定义为基于视觉提示的紧凑实例级识别问题**。具体而言，该方法在每个候选对象的中心叠加带有唯一数字ID的视觉标记，使VLM只需输出目标ID和时序区间，而无需学习跨模态坐标对齐。这一范式转换配合基于GRPO的强化学习训练，通过时序IoU奖励、空间一致性奖励和格式奖励的联合优化，驱动模型在推理过程中自主提升定位精度。

**关键实证发现：**

- **视觉提示范式本身在零样本设定下即带来显著增益**：在HCSTVG-v1上，Qwen2.5-VL-7B、Qwen2.5-VL-72B、InternVL3-8B、Qwen3-VL-8B的vIoU@0.3分别提升+12.5%、+6.0%、+3.6%、+28.3%（Section 1 INTRODUCTION）。
- **STVG-R1在HCSTVG-v2上达到新的最佳结果**：m_vIoU为40.8%，较基座模型Qwen2.5-VL-7B的19.3%提升+21.5%，并超越先前最佳模型SpaceVLLM（Table 1）。
- **意外泛化到多对象分割**：仅用单对象STVG数据训练的STVG-R1，在未见过的MeViS数据集上取得47.3% J&F，达到多对象视频对象分割的最佳性能（Table 3）。

**方法定位：** STVG-R1属于训练无关视觉提示 + 强化学习微调的混合范式。与需要可训练对齐模块的LLaVA-ST和依赖分割token解码器的VideoGlaMM不同，STVG-R1的视觉提示由现成检测器（YOLOv12）和分割跟踪器（SAM2）生成，无需针对STVG任务训练任何感知模块；强化学习仅作用于VLM的策略模型（Qwen2.5-VL-7B），通过任务驱动奖励引导其学会利用视觉提示进行精准的实例识别和时序定位。

**局限与待验证方向：** 视觉提示的质量受限于检测器和跟踪器的性能，且轻微遮挡视频内容；纯时序任务上视觉提示非必需；训练数据局限于两个STVG数据集，更大规模场景下的泛化性有待进一步验证。

## 背景与动机

时空视频定位（Spatial-Temporal Video Grounding, STVG）要求模型根据自然语言查询，同时定位目标对象在视频中的时间区间和每一帧的空间位置。该任务的核心挑战在于：模型必须建立跨模态的时间-空间联合理解，而非孤立地处理时序或空间线索。

**现有范式的瓶颈。** 当前主流的视觉-语言模型（VLM）在STVG任务上存在根本性的跨模态错位问题。如图Figure 2所示，现有方案大致分为两类：（a）基于对齐增强的范式——VLM输出时间戳和逐帧边界框坐标，再通过可训练的对齐模块将文本语义与视觉坐标关联；（b）基于解码器的范式——VLM生成分割token，再由专门的可训练解码器将其转化为掩码。这两种范式的共同缺陷在于，它们都试图让VLM直接学习跨模态的坐标或token对齐，而VLM本质上是为语义理解而非密集坐标回归设计的。这导致了严重的幻觉问题：逐帧输出的边界框坐标常常不一致，甚至产生无效预测。例如，通用VLM Qwen2.5-VL-7B在零样本条件下可能仅输出一个无时间戳的边界框，而专门设计的LLaVA-ST虽然能逐帧输出框，却缺乏对时序区间的整体推理能力（Figure 1）。

**范式转换的动机。** 本文的核心洞察是：将复杂的逐帧坐标回归问题重新定义为基于视觉提示的紧凑实例级识别问题。具体而言，与其让VLM学习“对象在每帧的坐标是多少”，不如让VLM回答“哪个标记的对象是目标”——这恰好是VLM擅长的语义匹配任务。通过在每个候选实例的中心叠加带有唯一数字ID的视觉提示，VLM只需输出目标ID和时序区间，即可完成时空定位。这种以对象为中心的视觉提示范式无需任何可训练的坐标对齐模块，将跨模态错位问题从“语义-坐标对齐”降维为“语义-ID匹配”，从根本上规避了幻觉的来源。

## 核心创新

STVG-R1 的核心创新在于将复杂的时空视频定位（STVG）从**逐帧密集坐标回归**重新定义为**基于视觉提示的紧凑实例ID识别**问题，并通过强化学习驱动任务导向的联合优化。这一范式转换体现在三个紧密耦合的 changed slots 上。

### 范式转换：从坐标回归到实例ID识别

传统方法要求 VLM 直接输出每帧的边界框坐标（如 **LLaVA-ST-7B**）或生成分割 token 再经可训练解码器恢复掩码（如 **VideoGlaMM**），这导致严重的跨模态错位和幻觉——通用 VLM 在零样本下常输出无效坐标或忽略时间戳（Figure 1）。STVG-R1 的核心洞察是：**以对象为中心的视觉提示为 VLM 提供了可解释的参考锚点**，使模型只需从候选实例中选择正确的 ID，而非凭空生成空间坐标。这一重新定义使多个通用 VLM 在零样本设定下获得显著提升：Qwen2.5-VL-7B 的 vIoU@0.3 从 28.2% 跃升至 40.7%（+12.5%），Qwen3-VL-8B 甚至提升 +28.3%（Section 1）。

### 视觉提示范式：训练无关的实例锚定

STVG-R1 在每个视频帧上叠加带有唯一数字 ID 的视觉提示（红色数字，字号 20），提示位于各实例中心。该范式具有三个关键属性：

1. **训练无关**：视觉提示由现成的 YOLOv12 检测器和 SAM2 分割跟踪器自动生成，无需训练任何对齐模块或解码器（Figure 2c）。
2. **时序一致性**：通过 SAM2 双向传播和周期性重检测（IoU 匹配），同一实例在整个视频中保持相同的数字 ID，确保跨帧可追溯。
3. **紧凑可解释**：VLM 的输出从密集坐标序列压缩为 `Target ID: [ID], Time range: [start, end]`，大幅降低了输出空间的复杂度。

消融实验证实，红色数字提示在零样本设定下优于字母提示和混合类型：字母提示的时序定位略好（m_tIoU 39.0 vs 38.0），但数字提示的空间精度更高（m_vIoU 19.8 vs 18.3），且字号 20 在可见性和遮挡之间取得最佳平衡（Table 5）。

### 强化学习驱动：任务导向的复合奖励

STVG-R1 首次将强化学习引入 STVG 任务，采用 GRPO（Group Relative Policy Optimization）算法，以 Qwen2.5-VL-7B 为策略模型，设计了三项任务驱动的奖励函数：

- **时序 IoU 奖励** $r_t(o)$：预测时间区间与真实区间的交并比，驱动模型精确定位事件发生的起止时刻。
- **空间一致性奖励** $r_s(o)$：当预测的实例 ID 正确且该 ID 出现在预测时段内时给予 1，否则为 0。这一**稀疏奖励**设计直接对齐“选择单个正确实例”的目标，消融实验表明其优于耦合奖励（m_vIoU 39.1 vs 38.3）和连续空间奖励（m_vIoU 39.1 vs 38.6）。
- **格式奖励** $r_f(o)$：鼓励模型遵循 `<think>...</think><answer>...</answer>` 的结构化输出格式。但消融实验显示，由于 Qwen2.5-VL 天然支持这些 token，移除 $r_f$ 几乎不影响优化动态（Figure 15），说明该组件在基座模型上的实际收益有限。

总奖励 $R(o) = r_t(o) + r_s(o) + r_f(o)$ 联合优化时序精度、空间一致性和输出格式。GRPO 通过组内归一化优势函数 $A_i$ 和 PPO 风格的裁剪目标稳定更新策略，使模型在强化学习后 m_vIoU 进一步提升 20.9%（HCSTVG-v2，Table 1）。

### 关键瓶颈的因果机制

STVG-R1 的因果操纵杆在于**将跨模态对齐的负担从 VLM 转移到预处理管道**。视觉提示在输入侧完成了“像素→实例”的映射，VLM 只需在语义空间进行“查询→实例ID”的匹配，避开了直接学习跨模态坐标对齐这一核心瓶颈。这一设计的决定性证据包括：(1) 零样本视觉提示即可大幅提升多个 VLM 的性能；(2) 强化学习进一步带来 20%+ 的绝对增益；(3) 仅用单对象 STVG 数据训练的模型意外泛化到多对象视频分割任务，在 MeViS 上取得 47.3% J&F 的最佳结果（Table 3），说明视觉提示范式本身赋予了模型处理多实例场景的能力。

## 整体框架

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_zuPxAZgT9F/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of paradigms: (a) VLM produces both timestamps and frame-level coordinates with a trainable alignment block; (b) VLM generates segmentation tokens, which are then processed by a trainable decoder; (c) our method uses training-free object-centric visual prompted video for spatial-temporal video grounding*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_zuPxAZgT9F/figures/003_Figure_3.jpg]]
*Figure 3: An illustration of our proposed STVG-R1 framework. Each object is assigned a unique ID via visual prompts, and the policy model is trained with spatial, temporal, and template rewards*

STVG-R1 将时空视频定位（STVG）从传统的逐帧坐标回归重新定义为**基于视觉提示的实例级识别问题**。其核心思路是：为视频中每个候选对象分配一个唯一且时序一致的数字 ID，并将这些 ID 以红色数字的形式叠加到视频帧上，随后让 VLM 直接输出目标对象的 ID 和时间区间，而非逐帧预测边界框坐标。

### 范式对比

现有 VLM 在 STVG 任务上主要采用两类范式（Figure 2）：

- **对齐式范式（Figure 2a）**：VLM 同时输出时间戳和逐帧坐标，通过一个可训练的跨模态对齐模块将文本-视觉特征映射到坐标空间。该方法要求模型学习复杂的跨模态坐标对齐，容易产生不一致甚至无效的预测。
- **解码器式范式（Figure 2b）**：VLM 生成分割 token，再由可训练的解码器将其转换为掩码序列。该方法引入了额外的解码器训练开销，且端到端优化仍面临跨模态错位问题。

STVG-R1 采用第三种范式（Figure 2c）：**免训练的以对象为中心的视觉提示**。该范式的关键洞察在于：通过将密集坐标回归问题转化为紧凑的实例识别问题，VLM 不再需要学习视觉特征到坐标空间的映射，而是利用视觉提示作为可解释的参考信号，专注于识别“哪个对象”和“何时发生”。

### 框架流程

STVG-R1 的整体框架如 Figure 3 所示，由四个核心模块串联构成：

**1. 视觉提示叠加与实例 ID 分配**

该模块负责将原始视频帧转换为视觉提示增强帧。具体流程为：
- 使用现成的目标检测器（YOLOv12）处理视频首帧，获取候选对象的边界框；
- 以这些检测框作为提示，驱动 SAM2 生成高质量的分割掩码，并通过双向传播完成全视频的实例跟踪；
- 引入周期性重检测机制（IoU 匹配），处理新出现或被遮挡后重现的对象；
- 在每个实例的掩码中心叠加红色数字 ID，生成增强帧 $\tilde{I}_t = I_t \oplus \mathcal{P}_t$。

对于训练数据，通过帧级 IoU 匹配和多数投票机制，自动确定与真实标注对应的目标对象 ID。

**2. VLM 策略模型**

以 Qwen2.5-VL-7B 作为策略模型 $\pi_\theta$，输入为视觉提示增强的视频序列 $\tilde{\nu}$ 和文本查询 $q$，输出为包含推理过程（`<think>` 标签内）和结构化答案（`<answer>` 标签内）的响应。答案格式为：“Target ID: [ID], Time range: [start time to end time]”。

**3. 奖励建模**

奖励函数 $R(o)$ 由三个分量求和构成：
- **时序 IoU 奖励** $r_t(o)$：预测时间区间与真实区间的交并比；
- **空间一致性奖励** $r_s(o)$：当预测的 ID 正确且该 ID 出现在预测时段内时给予 1，否则为 0；
- **格式奖励** $r_f(o)$：验证输出是否符合 `<think>...<answer>...` 的结构化格式。

**4. GRPO 优化**

采用组相对策略优化（GRPO）更新策略模型。对每个输入采样 $n$ 个响应，计算组内归一化优势函数，并使用带裁剪和 KL 惩罚的 PPO 目标函数进行优化，鼓励高奖励响应、抑制低奖励响应。

### 关键设计决策

- **视觉提示设计**：消融实验（Table 5）表明，红色数字提示（字号 20）在零样本设定下优于其他颜色和字符类型，被采纳为默认配置。
- **掩码过滤**：按类别每帧过滤掉面积小于最大掩码 1/3 的小实例，在数据质量和零样本性能之间取得最佳平衡（Table 6）。
- **稀疏空间奖励**：分离的稀疏空间奖励优于耦合奖励和连续空间奖励，因为其更直接地对齐“选择单个正确实例”的目标（Section 4.5）。

该框架的突出优势在于：视觉提示叠加是**免训练的**，不引入额外参数；强化学习的奖励设计直接联合优化时序精度、空间一致性和输出格式；且以对象为中心的提示使 VLM 的推理过程具有可解释性——模型可以“看到”并“推理”候选对象，而非盲目回归坐标。

## 核心模块与公式推导

### 3.1 视觉提示增强与范式重构

STVG-R1 的核心创新在于将逐帧坐标回归重新定义为基于视觉提示的紧凑实例识别问题。给定原始视频帧 $I_t$，首先通过视觉提示生成模块获得一组提示标记 $\mathcal{P}_t$，并将其叠加到原始帧上：

$$\tilde{I}_{t} \triangleq I_{t} \oplus \mathcal{P}_{t}, \quad \mathcal{P}_{t} = \{ p_{1}^{t}, \ldots, p_{K_{t}}^{t} \}$$

其中 $K_t$ 为第 $t$ 帧中检测到的候选实例数量，每个提示 $p_k^t$ 以红色数字形式标记在对应实例的中心位置。为控制显存消耗，所有帧被缩放至总像素预算约 $R = 1.6 \times 10^6$，满足 $H' \times W' \approx R / (2D)$，其中 $D$ 为视频时长（以 2 FPS 采样）。

增强后的视频序列 $\tilde{\nu}$ 与文本查询 $q$ 一同输入 VLM 策略模型 $\pi_\theta$（默认采用 **Qwen2.5-VL-7B**），模型联合预测时序区间 $[t_s, t_e]$ 和对应的目标对象标识符 $i$。这一范式从密集的逐帧边界框回归转变为紧凑的实例识别任务，避免了跨模态坐标对齐的固有困难。

### 3.2 实例 ID 分配与预处理管道

预处理管道由三个组件串联构成：**对象检测与跟踪**、**ID 分配**和**后处理修复**。

**检测与跟踪**：首帧 $I_1$ 经 YOLOv12 检测器处理，检测结果作为 SAM2 的提示，生成高质量分割掩码并沿时间轴双向传播。管道中引入周期性重检测机制，通过 IoU 匹配将新检测结果与已跟踪掩码进行关联——仅当几何重叠持续低于阈值时才创建新实例 ID。

**帧级 ID 分配**：对每一帧 $t$，选择与真实边界框 $g_t$ 的 IoU 最高的候选框对应的 ID：

$$\iota_{t} = \arg \max_{k \in \{1, \dots, K_{t}\}} \mathrm{IoU}(g_{t}, b_{k}^{t})$$

**多数投票确定目标 ID**：跨所有帧统计每个 ID 被选中的频次，得票最高者即为最终目标对象 ID：

$$A = \arg \max_{i} \sum_{t=1}^{T} \mathbf{1}[\iota_{t} = i]$$

在推理阶段，轻量级 ID 修复步骤进一步解决偶发的重识别不一致问题。全局检测失败率低于 1%，重检测和 ID 修复机制有效缓解了该风险。

### 3.3 复合奖励函数设计

STVG-R1 采用任务驱动的复合奖励函数，将准确度奖励分解为时序 IoU 奖励和空间一致性奖励，并与格式奖励相加：

$$R(o) = r_{t}(o) + r_{s}(o) + r_{f}(o)$$

**时序 IoU 奖励**量化预测区间 $[t_s, t_e]$ 与真实区间 $[t_s', t_e']$ 的重叠程度：

$$r_{t}(o) = \frac{ [t_s, t_e] \cap [t_s^{\prime}, t_e^{\prime}] }{ [t_s, t_e] \cup [t_s^{\prime}, t_e^{\prime}] }$$

**空间一致性奖励**采用稀疏二值设计，当预测的实例 ID $i$ 等于真实 ID $i^*$ 且该 ID 在预测时段内出现时给予 1，否则为 0：

$$r_{s}(o) = \begin{cases} 1, & \text{if } i = i^{*} \text{ and } i \text{ appears in } [t_s, t_e], \\ 0, & \text{otherwise}. \end{cases}$$

消融实验表明，这种分离的稀疏空间奖励优于耦合奖励（$R(o) = r_t(o) + r_s(o)$，m_vIoU 降至 38.3%）和连续空间奖励（$r_s = \frac{1}{|T_{\cap}|} \sum_{t \in T_{\cap}} \mathrm{IoU}(\hat{B}_t, B_t^*)$，m_vIoU 降至 38.6%），因为稀疏设计更精确地对齐了“选择单个正确实例”的目标，避免了额外噪声。

**格式奖励** $r_f(o)$ 用于约束输出结构，但由于 Qwen2.5-VL 天然支持 `<think>` 和 `<answer>` 标记，该奖励对优化动态影响微小——移除 $r_f$ 后的训练曲线几乎与完整奖励设置一致（Figure 15）。

### 3.4 GRPO 策略优化

训练采用组相对策略优化（GRPO），在每组 $n$ 个采样响应中计算归一化优势函数：

$$A_{i} = \frac{ R(o_i) - \operatorname{mean}(\{R(o_j)\}_{j=1}^{n}) }{ \operatorname{std}(\{R(o_j)\}_{j=1}^{n}) }$$

优化目标为带有裁剪和 KL 正则化的策略梯度：

$$\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{(\tilde{\nu}, q) \sim \mathcal{D}} \left[ \frac{1}{n} \sum_{i=1}^{n} \Big( \min\big( \frac{\pi_{\theta}(o_i|q)}{\pi_{\theta_{\mathrm{old}}}(o_i|q)} A_i, \mathrm{clip}(\frac{\pi_{\theta}(o_i|q)}{\pi_{\theta_{\mathrm{old}}}(o_i|q)}, 1 - \epsilon, 1 + \epsilon) A_i \big) - \beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}}) \Big) \right]$$

其中 $\epsilon$ 为裁剪参数，$\beta$ 控制 KL 正则化强度，$\pi_{\mathrm{ref}}$ 为冻结的参考策略。裁剪项防止策略更新过大，KL 惩罚约束策略偏离参考模型过远，二者共同保证训练稳定性。训练在 8×A100 GPU 上进行，数据仅包含单对象 STVG 数据集（HCSTVG 和 VidSTG）。

## 实验与分析

### 核心瓶颈与因果机制

STVG-R1的突破性表现源于对时空视频定位（STVG）任务中两个根本瓶颈的精准干预。**瓶颈一**：通用视觉-语言模型（VLM）在密集预测任务中存在严重的跨模态错位——直接输出逐帧坐标时，模型难以建立文本查询与空间位置的稳定映射，导致坐标漂移、时序不一致甚至无效预测（如Qwen2.5-VL-7B零样本仅输出单个无时间戳的边界框，见Figure 1）。**瓶颈二**：现有专用VLM虽引入对齐模块或分割令牌，但需要额外的可训练组件，且仍受限于逐帧回归的固有困难。

**因果旋钮**：STVG-R1将复杂的逐帧坐标回归重新定义为基于视觉提示的紧凑实例ID识别问题。具体而言，在每个候选实例中心叠加红色数字ID标记，使VLM只需识别“目标对象是几号”而非“目标每帧在哪”。这一范式转换从根本上避开了跨模态坐标对齐的困难，将模型能力聚焦于其擅长的识别任务。

**核心洞察**：以对象为中心的视觉提示为VLM提供了可解释的参考锚点。在强化学习的奖励引导下，模型不仅学会了精确的实例识别，还意外地泛化到多对象分割任务——这验证了视觉提示范式赋予了模型一种“以对象为中心”的理解能力，而非简单的模式匹配。

### 主实验结果

#### HCSTVG基准：全面超越先前方法

Table 1汇总了HCSTVG-v1和HCSTVG-v2上的核心结果。STVG-R1在HCSTVG-v2验证集上达到**m_vIoU 40.8%**，相比基座模型Qwen2.5-VL-7B（19.3%）提升**+21.5个百分点**，并超越先前最佳模型SpaceVLLM-7B，确立新的最优结果。在HCSTVG-v1测试集上，STVG-R1的vIoU@0.3达到**66.7%**，较Qwen2.5-VL-7B零样本（28.2%）提升**+38.5个百分点**。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_zuPxAZgT9F/figures/004_Table_1.jpg]]
*Table 1: Performance comparison with state-of-the-art models on HCSTVG-v1 test set and HCSTVG-v2 val set (%). The results of GroundingGPT-7B are reported from SpaceVLLM, while those of InternVL3-8B, Qwen2.5-VL-7B, Qwen2.5-VL-72B and Qwen3-VL-8B are generated by our experiments. The best and second-best results are shown in bold and underlined*

视觉提示范式的零样本有效性在多个通用VLM上得到验证：在HCSTVG-v1上，视觉提示使InternVL3-8B、Qwen2.5-VL-7B、Qwen2.5-VL-72B和Qwen3-VL-8B的vIoU@0.3分别提升**+3.6%、+12.5%、+6.0%和+28.3%**。Qwen3-VL-8B的显著提升（+28.3%）暗示新一代VLM对视觉提示的响应更为敏感，这可能与其更强的指令遵循能力相关。

#### ST-Align基准：空间-时间联合定位的稳健性

在ST-Align基准（Table 2）上，STVG-R1在STVG任务上达到m_vIoU **23.4%**，以微弱优势（+0.6%）超越LLaVA-ST-7B（22.8%）。值得注意的是，LLaVA-ST引入了额外的对齐令牌和训练模块，而STVG-R1完全依赖训练无关的视觉提示和强化学习优化，在更简洁的架构下取得了更优性能。这一结果验证了范式转换的有效性：无需复杂的坐标对齐机制，实例ID识别即可实现更鲁棒的空间-时间联合定位。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_zuPxAZgT9F/figures/005_Table_2.jpg]]
*Table 2: Performance comparison with state-of-the-art models on ST-Align benchmark (%). The results of Qwen2.5-VL-7B are generated by our experiments*

#### MeViS零样本泛化：涌现的多对象分割能力

最令人意外的发现来自MeViS数据集（Table 3）。尽管STVG-R1仅在**单对象**STVG数据（HCSTVG和VidSTG）上训练，其在多对象视频对象分割任务上达到**J&F 47.3%**，超越此前最佳模型VideoGlaMM（45.2%）和VISA（43.5%）。这一零样本泛化能力并非设计目标，而是视觉提示范式的涌现特性：模型学会了“关注标记对象”的通用能力，而非记忆特定任务模式。这为视觉提示作为密集预测任务的通用接口提供了有力证据。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_zuPxAZgT9F/figures/006_Table_3.jpg]]
*Table 3: Performance comparison with state-of-theart models on MeViS (%). The results of TrackGPT are generated by VISA*

#### 时序定位：纯时序任务的竞争力

在Charades-STA和TVGBench（Table 4）上，STVG-R1分别达到tIoU@0.5的**52.5%**和**27.4%**，超越TimeSuite（48.7%/24.4%）。然而，Table 10的消融显示，移除视觉提示后STVG-R1在Charades-STA上的tIoU@0.3从72.2%微升至**73.2%**，tIoU@0.5从52.1%升至**52.5%**。这表明视觉提示对纯时序任务并非必需，甚至可能因轻微遮挡而微弱降低性能。这一发现界定了视觉提示范式的适用边界：在空间定位为核心的任务中不可或缺，在纯时序任务中可选择性省略。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_zuPxAZgT9F/figures/007_Table_4.jpg]]
*Table 4: Performance comparison with state-of-the-art models on Charades-STA and TVGBench (%). The results marked with ∗ represent models training on corresponding dataset, while others indicate zero-shot settings*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_zuPxAZgT9F/figures/019_Table_10.jpg]]
*Table 10: Comparison of STVG-R1 with and without visual prompts on temporal grounding benchmarks Charades-STA and TVGBench (%). Adding visual prompts slightly affects temporal performance, showing that object-centric prompts are less critical for temporal-only tasks*

### 消融实验与设计选择

#### 模块贡献：视觉提示与强化学习的协同效应

Table 7的模块消融揭示了各组件的贡献层级。在HCSTVG-v1上，基础Qwen2.5-VL-7B零样本的m_vIoU仅为19.5%；添加视觉提示（VisualPrompt）提升至**28.2%**（+8.7%）；进一步应用GRPO强化学习（VisualPrompt+GRPO）跃升至**39.1%**（+19.6%总提升）。值得注意的是，监督微调（VisualPrompt+SFT）仅达到30.4%，远低于GRPO的39.1%。这表明强化学习的任务驱动奖励（时序IoU + 空间一致性）比监督微调更有效地引导模型学习精确的实例识别和时序定位，验证了奖励设计的因果作用。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_zuPxAZgT9F/figures/010_Table_7.jpg]]
*Table 7: Ablation study with different modules on HCSTVG-v1 and HCSTVG-v2*

#### 视觉提示设计：红色数字的最优性

Table 5系统比较了提示类型和大小。红色数字提示（font size 20）在零样本设定下达到最佳m_vIoU **28.2%**和vIoU@0.3 **43.4%**。字母提示（大写）的时序定位略优（m_tIoU 40.0% vs 数字的39.0%），但空间精度显著落后（m_vIoU 25.2% vs 28.2%）。这一差异可能源于VLM在预训练中对数字序列的更强先验。混合提示（数字+大写字母）并未带来增益（m_vIoU 27.6%），暗示一致性比多样性更重要。提示大小方面，font size 10-30性能稳定，但过小（难以识别）或过大（严重遮挡）均导致性能下降。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_zuPxAZgT9F/figures/008_Table_5.jpg]]
*Table 5: Ablation study on visual prompt designs on HCSTVG-v1 with zero-shot Qwen2.5-VL-7B. U-Letters denotes uppercase letters, L-Letters denotes lowercase letters, and Mix refers to a combination of numbers and uppercase letters*

#### 掩码过滤阈值：数据质量与覆盖的权衡

Table 6显示，掩码过滤阈值θ=1/3在数据质量与零样本性能间取得最佳平衡（m_vIoU 27.4%）。更激进的过滤（θ=1/2）虽提升数据质量上限（m_vIoU上界39.5% vs 1/3的38.0%），但零样本性能下降（26.8%），因为过强的过滤移除了部分有效的小目标实例，损害了训练数据的多样性。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_zuPxAZgT9F/figures/009_Table_6.jpg]]
*Table 6: Experimental results of mask filtering thresholds on HCSTVG-v1. Values before ‘/’ denote the upper bound, and those after ‘/’ are zero-shot results with Qwen2.5-VL-7B*

#### 空间奖励设计：稀疏优于连续

奖励函数的消融（Section 4.5）揭示了关键设计原则。分离的稀疏空间奖励（正确ID=1，否则=0）达到m_vIoU **39.1%**，优于耦合奖励（38.3%）和连续空间奖励（38.6%）。连续奖励将空间奖励定义为预测框与真值框的逐帧IoU均值，引入了不必要的坐标回归噪声，反而干扰了ID识别的核心目标。稀疏奖励的优越性验证了“选择正确实例”比“精确回归坐标”更符合视觉提示范式的本质。

#### 预处理组件：重检测的关键作用

Table 11显示，去除重检测组件（w/o re-detection）严重损害vIoU（从66.7%降至显著更低水平），而去除反向跟踪（w/o backward tracking）影响较小。这是因为重检测负责发现新出现的目标和恢复跟踪丢失的实例，对维持ID一致性至关重要。全局检测失败率低于1%，但重检测机制确保了这些边缘情况的鲁棒处理。

### 失败模式与局限性

1. **检测器依赖性**：视觉提示的质量完全受限于YOLOv12+SAM2的性能。当目标类别不在检测器词表中时（如Figure 10中的鱼），虽然一致性ID设计仍可保证定位，但语义误分类不可避免。这提示未来工作可探索开放词汇检测器或VLM自生成提示。

2. **视觉遮挡的微弱代价**：Table 9显示视觉提示对MME-VideoOCR基准的总体影响微小（总分59.4→58.9），但在纯时序任务上移除提示反而带来微弱提升（Table 10）。这说明提示的遮挡效应虽小但存在，在不需要空间定位的场景下可省略。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_zuPxAZgT9F/figures/012_Table_9.jpg]]
*Table 9: Evaluation results on MME-VideoOCR. ‘TR’ denotes Text Recognition, ‘VTQA’ Visualshoulder of the man. Text QA, ‘TG’ Text Grounding, ‘AR’ Attribute Recognition, ‘CDT’ Change Detection & Tracking, ‘STP’ Special Text Parsing, ‘CFTU’ Cross-Frame Text Understanding, ‘TBR’ Text-Based Reason-1 1 1 2 1 ing, ‘TBVU’ Text-Based Video Understanding, and ‘RVT’ Robust Video Testing*

3. **训练数据规模有限**：仅使用HCSTVG和VidSTG两个数据集训练，尽管泛化能力出色（MeViS 47.3% J&F），但在更大规模、更多样场景下的性能上限尚未探明。

4. **格式奖励的冗余性**：Figure 15显示，移除格式奖励r_f的训练曲线与完整奖励几乎一致。这是因为Qwen2.5-VL原生支持`<think>`和`<answer>`令牌，格式奖励成为冗余设计。这一发现提示在VLM的强化学习中，格式奖励的必要性取决于基座模型的指令遵循能力。

5. **计算资源需求**：训练需要8×A100 GPU，对硬件条件有一定要求，可能限制了更广泛社区的复现和扩展。

### 图表核心结论

- **Figure 1**：定性对比直观展示了范式转换的效果——Qwen2.5-VL-7B输出无时间戳的单个框，LLaVA-ST限于逐帧单框，而STVG-R1通过实例ID识别实现了精确的时空定位。
- **Table 1**：STVG-R1在HCSTVG-v1/v2上全面超越先前方法，视觉提示使多个VLM的零样本性能显著提升，Qwen3-VL-8B的+28.3%提升尤为突出。
- **Table 3**：仅用单对象数据训练的STVG-R1在多对象分割任务上达到47.3% J&F，验证了视觉提示范式的涌现泛化能力。
- **Table 7**：GRPO强化学习贡献了总提升的约55%（19.5%→39.1%中的10.9%来自GRPO），远超SFT的增益，验证了奖励设计的因果作用。
- **Table 10**：视觉提示在纯时序任务上可省略，界定了范式适用边界。

### 补充图表

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_zuPxAZgT9F/figures/011_Table_8.jpg]]
*Table 8: Ablation study with different modules on ST-Align*

## 方法谱系与知识库定位

### 范式变革：从密集坐标回归到实例识别

时空视频定位（Spatial-Temporal Video Grounding, STVG）的核心瓶颈在于视觉-语言模型（VLM）在密集预测任务中的跨模态错位——逐帧输出边界框坐标极易产生不一致甚至无效的预测，导致严重的幻觉问题。现有方法大致沿两条路线演进：

**路线一：对齐增强型VLM。** 以 **SpaceVLLM-7B** 和 **LLaVA-ST-7B** 为代表，在通用VLM基础上引入可训练的对齐模块或额外对齐token，使模型能输出时间戳与帧级坐标。这类方法保留了逐帧回归的范式，仍受限于跨模态坐标对齐的固有困难——LLaVA-ST每帧仅能输出单个边界框，而Qwen2.5-VL-7B在零样本条件下甚至输出无时间戳的单一无效框（Figure 1）。

**路线二：分割token解码型VLM。** 以 **VideoGlaMM** 为代表，VLM生成分割token，再由可训练解码器转化为掩码。该方法将空间定位外包给专用解码器，但解码器仍需大量标注数据训练，且与VLM的语义理解存在断层。

STVG-R1的因果旋钮在于**将逐帧坐标回归重新定义为基于视觉提示的紧凑实例ID识别问题**。这一范式转换绕开了直接学习跨模态坐标对齐的难题：通过在每个实例中心叠加统一的数字ID标记（红色数字，字体大小20），VLM只需识别“哪个ID对应查询描述的事件”，而非生成坐标序列。该设计使模型专注于实例识别这一更符合VLM语言推理能力的任务，同时保持了可解释性——数字标记直接作为视觉参考提示。

### 与专用模型的对比定位

在专用模型谱系中，**TubeDETR**（Yang et al., CVPR 2022）基于视觉-语言预训练（VLP）架构，是典型的检测-跟踪联合建模路线；**VISA**（Yan et al., ECCV 2024）则利用大语言模型进行视频对象分割。STVG-R1区别于这两类方法的关键在于**训练策略的革新**：首次将GRPO（组相对策略优化）强化学习引入STVG任务，通过任务驱动的复合奖励函数联合优化时序精度、空间一致性和输出格式。

奖励设计体现了对STVG任务结构的深刻理解：
- **时序IoU奖励** $r_t(o)$ 量化预测区间与真实区间的交并比；
- **空间一致性奖励** $r_s(o)$ 采用稀疏二元信号——仅当预测ID正确且出现在预测时段内时给予1，否则为0。消融实验表明，这种稀疏空间奖励优于耦合奖励（m_vIoU从39.1降至38.3）和连续空间奖励（降至38.6），因为其更精准地对齐了“选择单个正确实例”的目标；
- **格式奖励** $r_f(o)$ 的实际收益有限——Qwen2.5-VL天然支持`<think>`和`<answer>` token，移除$r_f$后优化动态几乎一致（Figure 15），表明该组件对基座模型存在冗余。

### 适用边界与跨任务泛化

STVG-R1的适用边界由其核心设计决定：

**强适用场景：**
- **时空联合定位**：在HCSTVG-v1/v2和ST-Align上均达到SOTA，基座Qwen2.5-VL-7B的m_vIoU提升超过20%（Table 1, Table 7）；
- **多对象分割的零样本泛化**：仅用单对象STVG数据训练，在MeViS上达到47.3% J&F，超越专用分割模型VideoGlaMM（45.2%）（Table 3）。这一意外泛化能力源于以对象为中心的视觉提示赋予了VLM跨实例的识别能力。

**弱适用或需谨慎的场景：**
- **纯时序定位**：在Charades-STA和TVGBench上，视觉提示非必需甚至微弱降低性能（Table 10），因为时序任务不依赖空间实例区分；
- **OCR密集场景**：MME-VideoOCR基准上，视觉提示叠加导致总分从59.4微降至58.9（Table 9），表明数字标记对文字识别存在轻微干扰；
- **检测器词表外类别**：YOLOv12的类别词表限制导致语义误分类，尽管一致性ID设计保证了定位可用性，但语义标签可能不准确。

### 局限与开放问题

**已知局限：**
1. **上游依赖瓶颈**：对象检测器（YOLOv12）和跟踪器（SAM2）的性能直接决定视觉提示质量。虽然全局检测失败率低于1%，且通过重检测和ID修复机制缓解，但检测器未见类别仍是系统上限的硬约束；
2. **视觉遮挡代价**：红色数字标记轻微遮挡视频内容，在纯时序任务上移除提示反而带来微弱提升，暗示存在更优的提示设计空间；
3. **计算资源需求**：GRPO训练需要8×A100 GPU，限制了轻量化部署的可能性；
4. **训练数据覆盖**：仅使用HCSTVG和VidSTG两个数据集，尽管泛化表现强劲，但更多样场景（如第一人称视频、电影风格视频）的验证主要停留在定性层面（Figure 13, Figure 14）。

**开放问题：**
- 以对象为中心的视觉提示范式能否直接迁移至其他密集预测任务，如动作定位、多对象跟踪或人物交互检测？
- 是否存在更优的提示设计（动态形状、自适应颜色编码、半透明叠加），在减少视觉遮挡的同时进一步提升识别精度？
- 强化学习奖励函数能否与更细粒度的评估指标（如vIoU@0.7）进行直接联合优化，以提升高精度场景下的表现？
- 在无现成检测器或分割模型的条件下，能否通过VLM自身生成视觉提示实现端到端训练，从而消除上游依赖瓶颈？
- 在更大规模、更多样化的视频数据上进行强化学习，是否会涌现出更复杂的推理行为（如时序因果推理、多对象关系建模）？

## 原文 PDF

![[paperPDFs/ICLR_2026/STVG_R1_Incentivizing_Instance_Level_Reasoning_and_Grounding_in_Videos_via_Reinforcement_Learning.pdf]]
