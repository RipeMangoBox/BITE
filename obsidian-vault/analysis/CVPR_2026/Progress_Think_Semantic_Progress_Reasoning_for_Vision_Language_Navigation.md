---
title: "Progress-Think: Semantic Progress Reasoning for Vision-Language Navigation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Progress_Think_Semantic_Progress_Reasoning_for_Vision_Language_Navigation.pdf
project_link: "https://horizonrobotics.github.io/robot_lab/progress-think"
code_link: null
aliases:
- PT
- Progress-Think
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 视觉观察与指令前缀的单调共进展结构（monotonic co-progression），即累积的观察历史在语义上对应于指令的连续前缀，使进度可以被建模为指令式语义对齐。
primary_logic: 利用指令本身的序列结构，通过自对齐进度预训练（SAPP）从部分轨迹和指令前缀的对齐中自监督地学习语义进度推理，无需昂贵的手动标注，并通过进度条件策略和联合优化使推理与决策一致。
claims:
- 视觉观察与指令语义表现出单调共进展，这是先前方法忽略的结构性质。
- 自对齐进度预训练（SAPP）通过前缀子集软交叉熵损失和单调排序损失，从指令本身推导显式自监督信号，实现无标注进度学习。
- 三阶段训练框架（SAPP、进度引导策略预训练、进度-策略联合微调）使进度推理与导航策略紧密结合，在R2R-CE和RxR-CE上达到最先进性能。
- R2R-CE Val-Unseen 上 SR↑ = 60.1
---

# Progress-Think: Semantic Progress Reasoning for Vision-Language Navigation

> [!tip] 核心洞察
> 利用指令本身的序列结构，通过自对齐进度预训练（SAPP）从部分轨迹和指令前缀的对齐中自监督地学习语义进度推理，无需昂贵的手动标注，并通过进度条件策略和联合优化使推理与决策一致。

| 字段 | 内容 |
|------|------|
| 中文题名 | Progress-Think: 面向视觉语言导航的语义进度推理 |
| 英文题名 | Progress-Think: Semantic Progress Reasoning for Vision-Language Navigation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.17097) · [Project](https://horizonrobotics.github.io/robot_lab/progress-think) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Progress-Think |
| Dataset | R2R-CE Val-Unseen, RxR-CE Val-Unseen |

> [!tip] 效果简介
> - R2R-CE Val-Unseen 上，SR↑ 60.1 vs - (-)；SPL↑ 53.6 vs - (-)；NE↓ 4.68 vs - (-)。
> - RxR-CE Val-Unseen (跨数据集) 上，SR↑ 27.5 vs - (-)。
> - R2R-CE Val-Unseen (消融) 上，SR↑ 43.8 (语义进度) vs - (-)。

## 概述

视觉语言导航（VLN）要求智能体根据自然语言指令在连续环境中完成长程移动。当前主流的视觉-语言-动作（VLA）模型虽然在单步决策上表现良好，但其根本瓶颈在于**缺乏对视觉观察与指令语义之间单调共进展的建模**——随着智能体逐步观察环境，所完成的指令语义前缀应当单调延伸，而现有方法无法捕获这一结构化对应关系，导致进度信号模糊、长程行为不连贯且缺乏可解释性。

Progress-Think 的核心洞察在于：**视觉观察与指令语义之间存在单调共进展（monotonic co-progression）**，即累积的观察历史在语义上对应于指令的连续前缀。这一结构特性使得进度可以被建模为指令式的语义对齐，而无需依赖昂贵的手动子目标标注。

基于此，Progress-Think 提出**语义进度推理**框架，将 VLN 解耦为两个互补组件：进度推理模块（Progress Reasoning Module, PRM）和进度引导的 VLA 模块（Progress-Guided VLA, PG-VLA）。PRM 接收观察历史，显式预测已完成指令部分的语义文本；PG-VLA 则以该进度估计为条件生成导航动作。整个框架通过三阶段无标注训练实现：

1. **自对齐进度预训练（SAPP）**：利用指令本身的序列结构，通过前缀子集软交叉熵损失和单调排序损失，从部分轨迹与指令前缀的对齐中自监督地学习语义进度推理。
2. **进度引导策略预训练**：冻结 PRM，以预测进度为条件进行有监督动作预测训练。
3. **进度-策略联合微调（PPCF）**：通过 GRPO 强化学习联合优化 PRM 和 PG-VLA，引入动作奖励、格式奖励和进度长度奖励，使推理与决策一致。

在实验验证上，Progress-Think 在 **R2R-CE Val-Unseen** 上取得 SR 60.1、SPL 53.6、NE 4.68 的最先进性能；在跨数据集的 **RxR-CE** 上同样表现突出（SR 27.5），且仅使用单目 RGB 输入，不依赖外部数据。消融研究表明，语义进度变体显著优于数值进度回归和指令推理，SAPP 与 PPCF 的联合训练对成功率（SR）和路径效率（SPL）均有正向贡献。

**方法定位**：Progress-Think 属于辅助推理型 VLA 方法，区别于 **Navila**（Cheng et al., arXiv 2024）、**Navid-4D**（Liu et al., 2025）、**StreamVLN**（Wei et al., arXiv 2025）等主流 VLA 模型，以及 **Aux-Think**（Wang et al., arXiv 2025）等辅助推理方法。其核心差异在于引入显式的语义进度推理模块，并通过自监督对齐实现无标注训练，而非依赖隐式学习或粗粒度数值回归。

## 背景与动机

视觉语言导航（VLN）要求智能体在真实感环境中，依据自然语言指令完成从起点到终点的连续移动。近年来，基于视觉-语言-动作（VLA）的大模型方法将导航建模为序列预测问题，在单目RGB输入下取得了显著进展。然而，现有VLA导航模型在长程任务中仍表现出行为不连贯、缺乏可解释性的弱点——其根源在于**缺乏对视觉观察与指令语义之间单调共进展的建模**。

具体而言，人类在导航时会持续将所见场景与指令的已完成部分对齐，形成“我已走到哪一步”的语义进度感知。这种感知是**单调共进展（monotonic co-progression）**的：随着观察历史的累积，已完成的指令前缀在语义上单调扩展，后续进度始终建立在前序进度的基础之上（Figure 1）。这一结构性质为精确定位任务进度提供了天然锚点，但被现有方法普遍忽略。

当前VLA导航模型的进度信号要么完全隐式地融入循环状态，缺乏显式可解释性；要么退化为粗粒度的数值完成率回归，无法捕捉指令内部的细粒度语义进展。部分辅助推理型方法（如**Aux-Think**，Wang et al., arXiv 2025）尝试引入显式推理，但依赖昂贵的手动子目标标注，难以规模化。这些缺口导致模型在长程导航中容易偏离指令意图，且难以诊断失败原因。

Progress-Think 的核心动机正是利用上述单调共进展结构，将进度建模为**指令式语义对齐**——即预测当前观察历史所对应的指令前缀文本。这一设计将进度从隐式状态或数值标量提升为可读的语义描述，使导航策略能够以预测进度为条件进行决策。为实现无标注的语义进度学习，Progress-Think 从指令本身的序列结构推导自监督信号，避免了对手动标注的依赖，并通过三阶段训练框架将进度推理与导航策略紧密结合，最终在保持推理效率的同时达到最先进的导航性能。

## 核心创新

Progress-Think 的核心创新在于将视觉语言导航（VLN）中的任务进度从隐式信号或粗粒度数值回归提升为**显式的语义进度推理**。该方法基于一个此前被忽视的结构性洞察：视觉观察与指令语义之间存在**单调共进展（monotonic co-progression）**——随着观察历史的累积，其在语义上对应的指令前缀也单调地向前延伸（见图1）。这一性质使得进度可以被自然地建模为“已完成指令部分”的语言文本，而非一个抽象的标量。

围绕这一洞察，Progress-Think 在以下四个关键维度上相对于现有 VLA 导航模型（如 **Navila** Cheng et al., arXiv 2024；**Navid-4D** Liu et al., 2025；**StreamVLN** Wei et al., arXiv 2025）形成了结构性改变：

### 1. 进度表示：从隐式/数值到显式语义推理
现有 VLA 模型通常不包含显式的进度模块，进度信息隐式地编码在策略网络中，或通过数值进度回归作为辅助任务。Progress-Think 引入独立的**进度推理模块（Progress Reasoning Module, PRM）**，直接输出指令式进度文本 $\hat{\mathcal{T}}_t$，即当前已完成的指令语义前缀。这一文本形式的进度不仅为导航决策提供了可解释的中间表示，还作为条件输入显式地引导动作生成。

### 2. 训练监督信号：从昂贵标注到自监督对齐
语义进度的学习通常需要细粒度的子目标标注，成本高昂。Progress-Think 提出**自对齐进度预训练（Self-Aligned Progress Pretraining, SAPP）**，完全从指令本身的序列结构推导监督信号。其核心机制是通过**前缀子集软交叉熵损失** $\mathcal{L}_{\mathrm{prefix}}$ 和**单调排序损失** $\mathcal{L}_{\mathrm{mono}}$ 的组合，在部分轨迹片段与指令前缀之间建立可微对齐，无需任何人工标注即可自监督地学习进度推理能力。

### 3. 策略条件输入：从双模态到三模态条件
传统 VLA 策略仅以视觉观察和语言指令为条件。Progress-Think 的**进度引导 VLA 模块（Progress-Guided VLA Module, PG-VLA）**额外将预测的语义进度 $\hat{\mathcal{T}}_t$ 作为条件输入，形成三模态条件 $a_{t:t+K-1} = \pi_{\theta}(\mathcal{O}_t, o_t, \mathcal{T}, \hat{\mathcal{T}}_t)$。这使得动作预测能够显式地感知当前任务完成状态，从而提升长程导航的连贯性。

### 4. 强化学习优化目标：从标准策略梯度到进度感知联合优化
在第三阶段的**进度-策略联合微调（Progress-Policy Co-Finetuning, PPCF）**中，Progress-Think 采用 GRPO 框架对 PRM 和 PG-VLA 进行联合优化。与传统策略梯度或行为克隆不同，PPCF 引入了三项奖励信号：动作奖励 $r_{\mathrm{act}}$（最长正确动作前缀）、格式奖励 $r_{\mathrm{fmt}}$ 和**进度长度奖励** $r_{\mathrm{len}}$（惩罚超过指令长度的进度预测）。消融实验表明，进度长度奖励在所有指标上带来一致改善（见表4），验证了进度约束对策略优化的正向作用。

## 整体框架

Progress-Think 将视觉语言导航（VLN）解耦为两个互补组件：**进度推理模块（Progress Reasoning Module, PRM）** 和 **进度引导的 VLA 模块（Progress-Guided VLA Module, PG-VLA）**，如图 Figure 2 所示。框架的核心设计动机源于一个被先前方法忽视的结构性质：视觉观察与指令语义之间存在**单调共进展（monotonic co-progression）**——随着智能体累积观察，指令中被完成的前缀在时间上单调延伸（Figure 1）。基于这一洞察，PRM 接收观察历史，显式预测当前已完成的指令式语义进度文本，而非隐式学习或数值回归；PG-VLA 则以观测、指令和该预测进度为条件生成导航动作，使决策与语义进度保持一致。

![[assets/figures/papers/paper_list_l2408_https_arxiv_org_abs_2511_17097/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the Progress-Think framework and annotation-free training pipeline. Compared with the vanilla Vision-Language-Action (VLA) model, Progress-Think introduces a Progress Reasoning Module to infer task progress and guide action generation. The model is trained in three stages: (1) Self-Aligned Progress Pretraining for progress pretraining with*

训练流程分为三个阶段，全程无需手动进度标注：

1. **自对齐进度预训练（Self-Aligned Progress Pretraining, SAPP）**：通过可微对齐机制，从部分轨迹与指令前缀的软匹配中自监督地训练 PRM。该阶段使用前缀子集软交叉熵损失 $\mathcal{L}_{\mathrm{prefix}}$ 和单调排序损失 $\mathcal{L}_{\mathrm{mono}}$，组合为 $\mathcal{L}_{\mathrm{SAPP}} = \mathcal{L}_{\mathrm{prefix}} + \mathcal{L}_{\mathrm{mono}}$，使模型学会从视觉历史中推断语义进度。
2. **进度引导策略预训练（Progress-Guided Policy Pretraining）**：冻结已训练的 PRM，以有监督交叉熵损失 $\mathcal{L}_{\mathrm{Policy}}$ 训练 PG-VLA，使其在预测进度条件下学习多步动作预测。
3. **进度-策略联合微调（Progress-Policy Co-Finetuning, PPCF）**：采用 GRPO 框架联合优化 PRM 和 PG-VLA，通过动作奖励 $r_{\mathrm{act}}$、格式奖励 $r_{\mathrm{fmt}}$ 和进度长度奖励 $r_{\mathrm{len}}$ 的组合信号，使推理与决策在强化学习层面保持一致。

相比标准 VLA 模型，Progress-Think 的输入输出流增加了显式的进度推理通道：每步先由 PRM 生成进度文本 $\hat{\mathcal{T}}_t$，再将其作为 PG-VLA 的条件输入，与观察历史 $\mathcal{O}_t$、当前观察 $o_t$ 和完整指令 $\mathcal{T}$ 一起预测未来 $K$ 步动作 $a_{t:t+K-1}$。这种解耦设计使进度推理可独立预训练，同时通过联合微调确保推理质量直接影响策略性能。

## 核心模块与公式推导

Progress-Think 将视觉语言导航（VLN）解耦为两个互补组件：**进度推理模块（Progress Reasoning Module, PRM）** 和 **进度引导的 VLA 模块（Progress-Guided VLA Module, PG-VLA）**，并通过三阶段训练框架实现无标注的语义进度学习。

### 进度推理模块（PRM）

PRM 的核心功能是：给定截至当前步 $t$ 的观测历史 $\mathcal{O}_t$ 和当前视觉观测 $o_t$，预测一个语义进度文本 $\hat{\mathcal{T}}_t$，该文本以指令式语言描述智能体已完成的任务部分：

$$\hat{\mathcal{T}}_t = \mathbf{F}_P(\mathcal{O}_t, o_t) \tag{1}$$

这一设计的因果机制在于：视觉观察与指令语义之间存在**单调共进展（monotonic co-progression）**——随着观测的累积，其在语义上对应的指令前缀单调延伸。PRM 正是利用这一结构性质，将进度建模为指令文本的连续前缀，而非抽象的数值标量。

### 自对齐进度预训练（SAPP）

由于获取细粒度的子目标标注成本高昂，Progress-Think 通过 SAPP 从指令本身的序列结构中推导自监督信号。其核心由两个损失函数构成。

**前缀子集软交叉熵损失** 鼓励预测的进度文本与指令的某个前缀在语义上对齐。首先定义在指令前缀长度 $k$ 上的软对齐分布：

$$p_{\theta}(k \mid \mathcal{O}_t, \mathcal{T}) \propto \exp\left(-\frac{\mathrm{CE}(\hat{\mathcal{T}}_{t,1:k}, \mathcal{T}_{1:k})}{\tau}\right) \tag{2}$$

其中 $\mathrm{CE}(\cdot,\cdot)$ 为交叉熵，$\tau$ 为温度系数。基于此，前缀子集软交叉熵损失为：

$$\mathcal{L}_{\mathrm{prefix}} = \mathbb{E}_t \Bigg[ -\tau \log \sum_k \exp\left(-\frac{\mathrm{CE}(\hat{\mathcal{Z}}_{t,1:k}, \mathcal{Z}_{1:k})}{\tau}\right) \Bigg] \tag{3}$$

该损失通过软注意力机制，允许模型在指令前缀长度上学习一个可微分的对齐分布，而非硬性指定某个固定截断点。

**单调排序损失** 强制进度预测在时间上单调递增——若 $t_i < t_j$，则预测的进度前缀长度不应缩短：

$$\mathcal{L}_{\mathrm{mono}} = \mathbb{E}_{(i,j): t_i < t_j} \left[ \max(0, \hat{k}_{t_i} - \hat{k}_{t_j}) \right] \tag{4}$$

SAPP 的总损失为两者之和：

$$\mathcal{L}_{\mathrm{SAPP}} = \mathcal{L}_{\mathrm{prefix}} + \mathcal{L}_{\mathrm{mono}} \tag{5}$$

### 进度引导的 VLA 模块（PG-VLA）

在获得进度估计后，PG-VLA 将预测的语义进度作为额外条件输入，生成 $K$ 步导航动作：

$$a_{t:t+K-1} = \pi_{\theta}(\mathcal{O}_t, o_t, \mathcal{T}, \hat{\mathcal{T}}_t) \tag{6}$$

策略预训练阶段冻结 PRM，使用有监督交叉熵损失优化 PG-VLA：

$$\mathcal{L}_{\mathrm{policy}} = -\log \pi_{\theta}(a_{t:t+K-1}^{*} \mid \mathcal{O}_t, o_t, \mathcal{T}, \hat{\mathcal{T}}_t) \tag{7}$$

### 进度-策略联合微调（PPCF）

第三阶段通过 GRPO 联合优化 PRM 和 PG-VLA，使进度推理与导航决策相互一致。奖励函数由三项组成：

- **动作奖励**：奖励最长正确动作前缀：

$$r_{\mathrm{act}} = \sum_{i=0}^{K-1} \prod_{j=0}^{i} \mathbb{1}[a_{t+j} = a_{t+j}^{*}] \tag{8}$$

- **格式奖励**：确保输出动作格式有效：

$$r_{\mathrm{fmt}} = 1 \text{ if valid, else } 0 \tag{9}$$

- **进度长度奖励**：惩罚超出指令总长度的进度预测：

$$r_{\mathrm{len}} = \begin{cases} 1, & \text{if } |\hat{\mathcal{T}}_t| \leq |\mathcal{T}| \\ -\beta(|\hat{\mathcal{T}}_t| - |\mathcal{T}|), & \text{otherwise} \end{cases} \tag{10}$$

最终奖励为三项之和：

$$r_t = r_{\mathrm{act}} + r_{\mathrm{fmt}} + r_{\mathrm{len}} \tag{11}$$

GRPO 中的优势函数对组内奖励进行归一化：

$$A^{(n)} = \frac{r^{(n)} - \operatorname{mean}(r_t)}{\operatorname{std}(r_t)} \tag{12}$$

PPCF 的优化目标为：

$$\mathcal{L}_{\mathrm{PPCF}} = -\mathbb{E}_n\left[\min\left(\rho^{(n)} A^{(n)}, \mathrm{clip}(\rho^{(n)}, 1-\epsilon, 1+\epsilon) A^{(n)}\right)\right] \tag{13}$$

其中重要性比率同时考虑了策略和进度模块的更新：

$$\rho^{(n)} = \frac{\pi_{\boldsymbol{\theta}}(a_{t}^{(n)} \mid \mathcal{O}_t, o_t, \hat{\mathcal{Z}}_{t}^{(n)})}{\pi_{\boldsymbol{\theta}_{\mathrm{old}}}(a_{t}^{(n)} \mid \mathcal{O}_t, o_t, \hat{\mathcal{Z}}_{t}^{(n)})} \cdot \frac{\mathbf{F}_{p}(\hat{\mathcal{Z}}_{t}^{(n)} \mid \mathcal{O}_t, o_t)}{\mathbf{F}_{p_{\mathrm{old}}}(\hat{\mathcal{Z}}_{t}^{(n)} \mid \mathcal{O}_t, o_t)} \tag{14}$$

这一联合重要性采样设计使得 RL 信号能够同时反向传播至策略网络和进度推理模块，从而保证推理与决策的端到端一致性。消融实验证实，进度长度奖励在 PPCF 中带来了所有指标的一致改善（Table 4），验证了显式约束进度预测长度的必要性。

## 实验与分析

### 核心实验设置

Progress-Think 基于公开的 **R2R-CE** 和 **RxR-CE** 数据集进行训练与评估，所有模型均使用 **NVILA-2B** 作为主干网络初始化，采用单目 RGB 输入，且不依赖任何外部数据（如真实世界网页数据或通用 VQA 数据集），确保对比公平性。训练数据从 R2R-CE、RxR-CE 和 ScaleVLN 训练集构建，每阶段产生约 1200K 个状态-动作对。三阶段训练在 8 张 NVIDIA H20 GPU 上进行：第一阶段约需 8 小时，第二、三阶段各约 60 小时。策略模块预测接下来 K=3 步动作，遵循先前 VLN 工作的多步预测设计。

### 主实验结果

#### R2R-CE 基准性能

在 **R2R-CE Val-Unseen** 上，Progress-Think 取得了最先进的综合性能（Table 1）：成功率 **SR 60.1**，路径效率 **SPL 53.6**，导航误差 **NE 4.68**，Oracle 成功率 **OSR 63.6**。值得注意的是，该方法仅使用单目 RGB 输入即超越了依赖深度传感器（Depth）和全景视图（Pano.）的先前方法，同时不使用 LLM 的变体（†）也展现出明显优势。这表明语义进度推理为导航策略提供了有效的结构化引导信号。

![[assets/figures/papers/paper_list_l2408_https_arxiv_org_abs_2511_17097/figures/003_Table_1.jpg]]
*Table 1: Comparison of different methods on the R2R-CE Val-Unseen split. Observations used include single RGB camera (S.RGB), depth sensor (Depth) and panoramic view (Pano.). † indicates methods without using LLMs. External data refers to sources beyond the navigation simulator, such as real-world web data, general VQA datasets, and other similar resources*

#### 跨数据集泛化

在 **RxR-CE Val-Unseen** 上（Table 2），Progress-Think 仅使用 R2R-CE 训练集即取得 **SR 27.5** 的跨数据集泛化性能，达到最先进水平。该结果验证了自对齐进度预训练（SAPP）所学习的语义进度对齐能力具有任务无关的迁移性——进度推理模块捕获的是观察-指令间的单调共进展结构，而非特定数据集的语言风格。

![[assets/figures/papers/paper_list_l2408_https_arxiv_org_abs_2511_17097/figures/004_Table_2.jpg]]
*Table 2: Unseen-Dataset generalization performance on the RxR-CE Val-Unseen split. All results are obtained only training on the R2R-CE training set*

### 消融实验与分析

#### 进度表示变体的影响

Table 3 对比了三种进度表示方式：**语义进度**（本文方法）、**数值进度回归**和**指令推理**。语义进度变体在 SR 上达到 **43.8**，显著优于数值回归和指令推理基线。数值回归仅学习粗粒度的完成百分比，缺乏细粒度的语义定位能力；指令推理则缺少与观察历史的显式对齐机制。语义进度通过指令式文本前缀直接编码“已完成哪些子目标”，使策略模块能够精确感知当前任务阶段。

![[assets/figures/papers/paper_list_l2408_https_arxiv_org_abs_2511_17097/figures/006_Table_3.jpg]]
*Table 3: Comparison of different progress variants*

#### SAPP 与 PPCF 的联合消融

Table 4 系统解耦了训练框架各组件的作用。仅使用 SAPP（前缀子集软交叉熵损失 + 单调排序损失）已能获得可观的导航性能；在此基础上引入 PPCF 进一步提升了 SR 和 SPL。PPCF 内部，仅使用动作奖励和格式奖励（AR+FR）已带来增益，而加入**进度长度奖励**（PLR）在所有指标上产生一致改善，说明显式惩罚过长进度预测有助于防止推理漂移，使进度估计与真实任务完成度保持校准。

![[assets/figures/papers/paper_list_l2408_https_arxiv_org_abs_2511_17097/figures/005_Table_4.jpg]]
*Table 4: Unified ablation study on SAPP and PPCF. SAPP: Self-Aligned Progress Pretraining (Prefix: prefix-soft CE loss, Mono: monotonic ordering loss). PPCF uses two reward configurations: AR+FR (Action Reward + Format Reward) and PLR (Progress-Length Reward)*

#### 动作步数的影响

Table 5 考察了执行动作步数 K 的影响。执行所有三个预测动作步骤（K=3）获得最佳性能，验证了多步预测在 VLA 导航中的有效性——更长的动作视野使策略能够规划更连贯的运动轨迹，同时进度推理为多步决策提供了稳定的语义锚点。

![[assets/figures/papers/paper_list_l2408_https_arxiv_org_abs_2511_17097/figures/007_Table_5.jpg]]
*Table 5: Ablation on executed action steps*

### 效率与模型规模

Table 6 对比了模型规模与推理效率。Progress-Think 在保持相对紧凑的模型体积的同时，取得了领先的 SR 和 SPL，表明语义进度推理模块带来的额外计算开销可控，且其提供的结构化引导有效提升了决策质量，避免了盲目增加模型容量带来的效率损失。

![[assets/figures/papers/paper_list_l2408_https_arxiv_org_abs_2511_17097/figures/009_Table_6.jpg]]
*Table 6: Comparison of model size and inference efficiency on R2R-CE val-unseen*

### 定性分析

Figure 3 展示了不同模型在典型场景下的进度推理质量对比。Progress-Think 能够更准确地从历史观察中推断已完成的指令部分，而基线方法常出现进度跳跃或语义错位。Figure 4 的进度粒度分析进一步揭示了语义进度推理在细粒度子目标定位上的优势——模型能够区分指令中相邻但语义不同的子步骤，而非仅输出粗粒度的完成状态。

![[assets/figures/papers/paper_list_l2408_https_arxiv_org_abs_2511_17097/figures/008_Figure_3.jpg]]
*Figure 3: Qualitative comparison of progress reasoning quality. Across two representative scenes, we compare how different models infer navigation progress from historical observations. GPT-4o and NVILA[20] often produce generic or instruction-misaligned descriptions and occasionally exhibit hallucinations, limiting their usefulness for tracking progress and making it difficult for the agent to align its behavior with the intended navigation steps. Our ablated variants (without monotonic loss or without Progress-Policy Co-Finetuning) capture partial progress but tend to be less consistent and concrete, leading to incomplete guidance. In contrast, the full Progress-Think model produces concise, instru...*

![[assets/figures/papers/paper_list_l2408_https_arxiv_org_abs_2511_17097/figures/010_Figure_4.jpg]]
*Figure 4: Granularity analysis on R2R-CE*

### 公平性说明

所有实验均基于公开数据集和统一主干网络，对比方法均采用单目 RGB 输入且不依赖外部数据。Progress-Think 的性能增益完全来自语义进度推理框架和自监督训练机制，而非数据或模型容量的优势。

## 方法谱系与知识库定位

### 视觉语言导航中的进度建模谱系

**问题背景**。视觉语言导航（VLN）要求智能体根据自然语言指令在连续环境中移动。近年来，视觉语言动作（VLA）模型将导航建模为序列预测任务，主流方法包括 **Navila**（Cheng et al., arXiv 2024）、**Navid-4D**（Liu et al., 2025）、**StreamVLN**（Wei et al., arXiv 2025）和 **Uni-Navid**（Zhang et al., arXiv 2024）。这些方法将视觉观察与指令直接映射为动作，但**缺乏对任务完成进度的显式建模**。进度信号要么被隐式地编码在循环状态中，要么通过粗粒度的数值完成率回归来近似——后者在消融实验中表现远逊于语义进度（Table 3，SR从43.8降至更低），因为它无法捕捉指令语义与视觉观察之间的细粒度对应关系。

**辅助推理路线的局限**。与Progress-Think最接近的路线是**辅助推理型VLA方法**，如 **Aux-Think**（Wang et al., arXiv 2025）。这类方法引入额外的推理模块来辅助决策，但推理内容通常是通用的场景描述或常识推理，而非专门针对**任务进度**的语义定位。Progress-Think的关键区分在于：它将推理目标精确锁定在“智能体已完成指令的哪一部分”这一问题上，从而使推理输出可以直接作为策略的条件输入。

### 核心结构洞察：单调共进展

Progress-Think的方法论基础是一个被先前工作忽略的结构性质：**视觉观察与指令语义之间存在单调共进展（monotonic co-progression）**（Figure 1）。随着智能体沿路径推进，累积的观察历史在语义上对应于指令的一个连续前缀，且该前缀随时间单调扩展——后续的进度（红色）始终建立在先前进度（蓝色）之上。

这一洞察将进度建模从“回归一个标量”转变为“预测一个指令式文本前缀”，从而将问题转化为**视觉历史与指令前缀之间的语义对齐问题**。这一定义使得进度推理可以天然地利用指令本身的序列结构作为自监督信号，无需昂贵的手动子目标标注。

### 训练范式对比

| 维度 | 主流VLA方法 | Progress-Think |
|------|------------|----------------|
| 进度表示 | 隐式或数值回归 | 显式指令式语义文本 |
| 进度监督 | 依赖标注或粗粒度目标 | SAPP自监督对齐 |
| 策略条件 | 仅视觉+指令 | 额外加入预测进度 |
| 强化学习目标 | 标准策略梯度 | 进度感知GRPO联合优化 |

**自监督进度学习的独特性**。SAPP通过两个损失函数从部分轨迹中自举进度推理能力：前缀子集软交叉熵损失（公式3）鼓励预测的进度文本与指令的某个前缀软对齐；单调排序损失（公式4）强制进度在时间上单调递增。这种设计使得模型可以从任意长度的部分轨迹中学习，而不需要知道“当前应该完成到指令的哪一步”——对齐是通过可微分的软分布自动推断的。

**联合优化的必要性**。仅靠SAPP预训练后再冻结PRM进行策略训练（Table 4），性能明显低于进一步执行PPCF联合微调。PPCF通过GRPO同时优化PRM和PG-VLA，其中进度长度奖励（公式10）惩罚超出指令总长度的过度预测，确保推理与决策的一致性。消融实验表明，移除PPCF或进度长度奖励均会导致SR和SPL的显著下降。

### 适用边界与局限

**输入模态边界**。Progress-Think在单目RGB输入下即达到SOTA（R2R-CE Val-Unseen SR 60.1，SPL 53.6），甚至超越了使用深度传感器或全景视图的方法（Table 1）。这表明语义进度推理在一定程度上补偿了感知信息的不足。但其在极端视觉退化场景（如黑暗、强遮挡）下的鲁棒性尚未得到验证。

**跨数据集泛化**。在仅使用R2R-CE训练集的情况下，Progress-Think在RxR-CE Val-Unseen上取得SR 27.5（Table 2），展现了较强的泛化能力。但RxR-CE的指令风格更长、更口语化，SR绝对值仍远低于R2R-CE，说明语义进度推理对指令风格变化仍有一定敏感性。

**计算开销**。Table 6显示Progress-Think在模型大小和推理效率上与基线方法可比，三阶段训练总时长约128小时（8×H20 GPU），其中SAPP仅需8小时，主要开销在策略预训练和PPCF阶段。对于资源受限的场景，SAPP的轻量性是一个优势，但完整的PPCF联合优化可能是必需的。

**未探索的维度**。当前工作未讨论以下问题：（1）语义进度推理在非导航类具身任务（如物体操作）中的迁移性；（2）多语言指令下的进度对齐能力；（3）进度推理的可解释性如何转化为人机交互中的信任建立。这些是开放的研究方向。

### 在知识库中的定位

Progress-Think处于**VLA导航 × 自监督表示学习 × 推理增强决策**的交汇点。其核心贡献——利用指令序列结构实现无标注的语义进度推理——填补了VLA方法中“任务进度显式建模”的空白。与Aux-Think等通用辅助推理方法相比，Progress-Think的推理目标更聚焦、监督信号更自洽；与数值进度回归等朴素基线相比，语义进度提供了更丰富的条件信息和更强的泛化能力。该方法为未来将结构化任务知识注入VLA模型提供了一条可复用的技术路径：**利用任务定义本身的结构（如指令序列）作为自监督信号的来源**。

## 原文 PDF

![[paperPDFs/CVPR_2026/Progress_Think_Semantic_Progress_Reasoning_for_Vision_Language_Navigation.pdf]]
