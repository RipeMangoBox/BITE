---
title: "Robust Fine-tuning of Vision-Language-Action Robot Policies via Parameter Merging"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Robust_Fine_tuning_of_Vision_Language_Action_Robot_Policies_via_Parameter_Merging.pdf
project_link: https://retain.yajatyadav.com
code_link: null
openreview_forum_id: uWJwQ5SZoM
aliases:
- RFTVLARPPM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "微调后策略与预训练策略之间的线性插值系数α（0≤α≤1），该系数控制保留预训练通用知识与适应目标任务特定知识之间的权衡。"
primary_logic: "对预训练策略和微调后策略的权重进行简单线性插值，可以在权重空间中找到一个既保留预训练模型泛化能力又具备目标任务专长的解决方案，从而使微调后的策略在分布外场景下显著提升鲁棒性，且不增加任何推理成本。"
claims:
- "RETAIN在DROID whiteboard任务的OOD评估中成功率约80%，而基线方法平均仅30–50%（Fig. 7）。"
- "RETAIN在DROID plates任务OOD评估中成功率超过60%（Fig. 7）。"
- "RETAIN在LIBERO三个任务的平均OOD性能上均优于所有基线方法（Fig. 8）。"
- "RETAIN的性能随预训练数据量增加而显著提升：使用更多数据预训练的模型在OOD场景下表现更好（Fig. 9）。"
---

# Robust Fine-tuning of Vision-Language-Action Robot Policies via Parameter Merging

> [!tip] 核心洞察
> 对预训练策略和微调后策略的权重进行简单线性插值，可以在权重空间中找到一个既保留预训练模型泛化能力又具备目标任务专长的解决方案，从而使微调后的策略在分布外场景下显著提升鲁棒性，且不增加任何推理成本。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过参数合并实现视觉-语言-动作机器人策略的鲁棒微调 |
| 英文题名 | Robust Fine-tuning of Vision-Language-Action Robot Policies via Parameter Merging |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=uWJwQ5SZoM) · [Project](https://retain.yajatyadav.com) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | RETAIN |
| Dataset | DROID Whiteboard OOD Test Scenes, DROID Plates OOD Test Scenes, LIBERO 3-task Average OOD |

> [!tip] 效果简介
> - DROID Whiteboard OOD Test Scenes 上，成功率 (Success Rate) 为 ≈80% (RETAIN-co-FT)，对比 ≈40% (Task-FT平均)，变化 +40%。
> - DROID Plates OOD Test Scenes 上，成功率 (Success Rate) 为 >60% (RETAIN-co-FT)，对比 ≈30% (Task-FT平均)，变化 +30%。
> - LIBERO 3-task Average OOD 上，成功率 (Success Rate) 为 ≈85% (RETAIN-co-FT)，对比 ≈70% (Co-FT)，变化 +15%。

## 概要

将大规模预训练的通用机器人策略适配到特定下游任务时，面临一个核心瓶颈：**标准微调方法（如全参数微调 Task-FT）在仅使用少量目标演示数据（50–100 条）时，会导致策略严重过拟合**——微调后的策略迅速遗忘预训练获得的通用能力，并且无法将预训练知识迁移到目标任务的未见变体（OOD）上，在分布内（ID）性能与分布外（OOD）性能之间形成巨大鸿沟（Fig. 4）。

**RETAIN** 针对这一问题提出了一个极简的解决方案：**对预训练策略权重与微调后策略权重进行线性插值**，即 $\tilde{\theta} = (1 - \alpha) \cdot \theta_{\mathrm{pre}} + \alpha \cdot \theta_{\mathrm{ft}}$。其核心洞察在于，权重空间中的简单线性插值可以找到一个兼顾预训练泛化能力与目标任务专长的“折中解”，使微调后的策略在未见过的场景变体上显著提升鲁棒性，且不增加任何推理成本。

在方法定位上，RETAIN 属于**参数合并（parameter merging）范式**，区别于传统的全参数微调（Task-FT）、协同微调（Co-FT）、低秩适配（LoRA）和冻结部分模块（Freeze-FT）等方法。它不改变训练流程，仅在微调完成后对权重进行后处理式的合并操作，并可进一步扩展为模态感知合并（视觉、语言、动作模块各自独立合并系数）和连续多技能合并。

主要实验结果验证了该方法的有效性：
- 在 **DROID 真实机器人任务**（白板擦拭、盘子拾取）的 OOD 评估中，RETAIN 的成功率约 **80%** 和 **>60%**，分别比基线方法平均高出约 **40%** 和 **30%**（Fig. 7）。
- 在 **LIBERO 仿真环境**三个任务的平均 OOD 性能上，RETAIN 均优于所有基线方法（Fig. 8）。
- RETAIN 的性能随预训练数据量增加而显著提升（Fig. 9），且仅合并语言模型参数即可达到与合并全部参数相似的 OOD 性能（Fig. 11 右）。
- 在连续学习两个技能的场景中，RETAIN 能够顺序合并多个技能而不遗忘先前能力，显著优于顺序 Co-FT（Fig. 12）。

**方法局限**：当前对参数合并为何能显著提升泛化性缺乏完整的理论解释，合并系数 α 需在验证集上手动调节，且实验仅在基于 π0 架构的 VLA 策略上验证，泛化到其他架构尚待探索。

通用机器人策略的微调面临一个核心困境：标准微调方法（Task-FT）在使用少量目标演示数据时，会导致策略严重过拟合。如图 4 所示，随着训练步数增加，策略在非目标任务上的通用能力急剧下降，甚至在微调数据中的分布内（ID）场景也开始退化。更关键的是，微调后的策略无法将预训练获得的通用知识迁移到目标任务的未见变体（OOD）上——例如新的物体位置、实例、视角或光照条件——在 ID 与 OOD 性能之间存在巨大鸿沟。

这一瓶颈的根源在于，标准微调以行为克隆损失（公式 1）在窄分布的目标数据上优化参数，导致参数空间偏离预训练模型所编码的通用知识区域，从而丧失泛化性。即使采用协同微调（Co-FT，混合预训练数据与目标数据）或低秩适配（LoRA）等正则化手段，过拟合问题仍难以根除——精心调节学习率和训练步数同样会陷入过拟合（Fig. 16）。

现有微调范式本质上是在“适应目标任务”与“保留通用能力”之间做不可调和的权衡，缺乏一个简洁而有效的机制来同时兼顾两者。本文的动机正是填补这一缺口：能否在权重空间中找到一个既保留预训练模型泛化能力、又具备目标任务专长的解决方案，且不增加任何推理成本？

## 核心方法与创新机理

### 瓶颈洞察：标准微调的过拟合困境

当前通用VLA策略在少量目标演示数据上进行标准微调（Task-FT）时面临一个根本性瓶颈：策略迅速过拟合到微调数据中已见过的场景，同时丧失预训练阶段获得的通用能力。如Figure 4所示，随着训练步数增加，策略在非目标任务（GENERALIST）上的表现急剧下降，甚至在微调数据已见过的场景（ID）上也开始退化。更关键的是，微调后的策略无法将预训练的泛化知识迁移到目标任务的未见变体（OOD）上，导致ID性能与OOD性能之间存在巨大鸿沟。即使精心调节学习率和训练步数，这一过拟合现象仍难以避免（Figure 16）。

### 核心操控变量：合并系数α

RETAIN方法的核心操控变量是微调后策略与预训练策略之间的线性插值系数α（0 ≤ α ≤ 1）。该系数决定了最终策略在预训练通用知识与目标任务专长之间的权衡：
- α = 0：完全保留预训练策略
- α = 1：完全采用微调策略
- 0 < α < 1：在权重空间中线性混合两者

实验表明，α在0.5左右时在DROID任务上普遍表现良好，且该系数在独立的验证OOD场景上调优，随后在未参与调优的测试OOD场景上评估，确保了评估的公平性。

### 关键创新点：Changed Slots

RETAIN相对基线方法的本质创新体现在以下三个“changed slots”：

**1. 最终策略权重的获取方式（核心创新）**

| 方法 | 策略权重 |
|------|----------|
| 基线（Task-FT等） | 直接使用微调后的参数 $\theta_{\text{ft}}$ |
| RETAIN | 使用线性插值 $(1-\alpha) \cdot \theta_{\text{pre}} + \alpha \cdot \theta_{\text{ft}}$ |

这是RETAIN最根本的创新：不改变微调过程本身，而是对微调前后的权重进行简单的线性插值合并（公式2）。这一操作不增加任何推理成本，因为合并后的模型与原始模型具有完全相同的架构和参数量。核心洞察在于：权重空间中存在一条连接预训练策略和微调策略的线性路径，在该路径上可以找到一个既保留预训练模型泛化能力又具备目标任务专长的解。

**2. 模态感知合并（精细化控制）**

| 方法 | 合并策略 |
|------|----------|
| 基线（统一合并） | 所有模态（视觉、语言、动作）使用同一α |
| RETAIN | 为视觉、语言、动作模块分别设置合并系数 $\alpha_v, \alpha_l, \alpha_a$ |

如公式3所示，RETAIN允许对视觉编码器、语言模型主干和动作专家三个模块分别施加不同的合并系数。消融实验（Figure 11）揭示了一个重要发现：仅合并语言模型参数（$\alpha_l < 1$，而 $\alpha_a = \alpha_v = 1$）即可达到与合并全部参数相似的OOD性能，表明语言模型主干是控制泛化能力的关键模块。

**3. 微调数据配比策略（协同微调）**

| 方法 | 微调数据 |
|------|----------|
| Task-FT | 仅使用目标任务数据 |
| RETAIN co-FT | 混合预训练数据与目标任务数据进行协同微调后再合并 |

RETAIN在Task-FT和co-FT两种微调范式下均有效，但协同微调（co-FT）结合模型合并比仅使用模型合并（task-FT）在所有评估设置中效果更好（Figure 7, 8）。这表明在微调阶段保留对预训练数据的接触，能够为后续的权重合并提供更有利的初始条件。

### 连续技能合并能力

RETAIN进一步支持将多个新技能连续合并到通用策略中（公式4）：

$$\tilde{\theta}_n = (1 - \alpha) \cdot \tilde{\theta}_{n-1} + \alpha \cdot \theta_{\text{ft},n}$$

在顺序学习两个任务的实验中（Figure 12），RETAIN显著优于顺序Co-FT，能够在获取新技能的同时不遗忘先前学到的能力，展现出持续学习的潜力。

### 方法边界与待验证问题

尽管RETAIN在实验中展现出显著优势，仍需注意以下边界条件：
- 合并系数α需要针对每个任务和场景在验证集上手动调节，缺乏自动选择的启发式方法
- 实验仅在基于π0架构的VLA策略上进行，泛化到其他架构（如扩散策略）尚待验证
- 对模型合并为何能显著提升泛化性缺乏完整的理论解释，目前多基于线性模式连通性的经验假设

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_uWJwQ5SZoM/figures/001_Figure_1.jpg]]
*Figure 1: Naive approaches for finetuning of generalist policies narrowly improve target task performance on settings seen in the finetuning data, but fail to generalize or retain generality beyond the target task. We propose a simple solution: by averaging the generalist policy before and after finetuning, in weight space, we obtain finetuned policies that (1) significantly improve generalization ability to unseen variations of the target task, and (2) retain generalist capabilities on non-target tasks. Our approach RETAIN is a simple solution for robust policy finetuning*

RETAIN 的整体流程围绕一个核心操作展开：**对预训练通用策略与目标微调策略进行权重空间线性插值**，从而在不增加推理成本的前提下，将预训练模型的泛化能力与微调模型的任务专长融合为单一策略。

### 策略架构基础

RETAIN 建立在当前主流的视觉-语言-动作（VLA）通用策略架构之上，该架构由三个模块串联构成（Figure 2）：

1. **视觉编码器（Vision Encoder）**：处理来自机器人视角的视觉输入，提取场景特征表示。
2. **语言模型主干（Language Model Backbone）**：作为核心融合模块，接收视觉编码器输出的特征与任务语言指令，生成跨模态的中间表示。该模块是 RETAIN 后续分析中影响最大的参数组（Figure 11）。
3. **动作专家/解码器（Action Expert/Decoder）**：基于语言模型主干的输出，生成最终的动作序列（如末端执行器位姿、夹爪开合等）。

### 微调范式

给定预训练策略权重 $\theta_{\text{pre}}$，RETAIN 考虑两种微调范式：

- **任务微调（Task-FT）**：仅使用目标任务演示数据 $\mathfrak{D}_{\eta}$ 进行行为克隆，损失函数为标准负对数似然：
  $$\mathcal{L}_{\mathrm{BC}}(\boldsymbol{\theta};\mathfrak{D}) := -\frac{1}{|\mathfrak{D}|}\sum_{(s_t,a_t,T)\in\mathfrak{D}}\log\pi_{\boldsymbol{\theta}}(a_t\mid s_t,T)$$
  此范式面临严重过拟合风险——策略迅速遗忘预训练获得的通用能力，在分布外（OOD）场景下性能急剧下降（Figure 4）。

- **协同微调（Co-FT）**：在微调时混合预训练数据 $\mathfrak{D}_{\text{pre}}$ 与目标任务数据 $\mathfrak{D}_{\eta}$，以缓解灾难性遗忘。实验表明，Co-FT 结合模型合并的结果在所有评估设置中均优于 Task-FT 结合合并（Figure 7, 8）。

### 核心合并机制

RETAIN 的核心操作是将微调后的策略权重 $\theta_{\text{ft}}$ 与预训练权重 $\theta_{\text{pre}}$ 进行线性插值，得到最终部署的策略权重 $\tilde{\theta}$：

$$\tilde{\theta} = (1 - \alpha) \cdot \theta_{\mathrm{pre}} + \alpha \cdot \theta_{\mathrm{ft}}$$

其中 $\alpha \in [0, 1]$ 是**合并系数**，控制预训练通用知识与目标任务专长之间的权衡。当 $\alpha = 0$ 时，策略退化为原始预训练策略；当 $\alpha = 1$ 时，策略退化为纯微调策略。实验发现 $\alpha$ 在 0.5 左右时在 DROID 任务上普遍表现良好，具体值需在独立验证 OOD 场景上调优。

### 模态感知合并

考虑到 VLA 策略中不同模块的异构性，RETAIN 进一步引入模态特定合并系数，为视觉（$\alpha_v$）、语言（$\alpha_l$）、动作（$\alpha_a$）模块分别设置独立的插值权重：

$$\tilde{\binom{\tilde{\theta}_v}{\tilde{\theta}_a}} = \left[1 - \left(\begin{array}{l}\alpha_v\\ \alpha_l\\ \alpha_a\end{array}\right)\right] \cdot \left(\begin{array}{l}\theta_{\mathrm{pre,v}}\\ \theta_{\mathrm{pre,l}}\\ \theta_{\mathrm{pre,a}}\end{array}\right) + \left(\begin{array}{l}\alpha_v\\ \alpha_l\\ \alpha_a\end{array}\right) \cdot \left(\begin{array}{l}\theta_{\mathrm{ft,v}}\\ \theta_{\mathrm{ft,l}}\\ \theta_{\mathrm{pre,a}}\end{array}\right)$$

消融实验揭示了一个关键发现：**仅合并语言模型主干参数（$\alpha_l < 1$，$\alpha_v = \alpha_a = 1$）即可达到与合并全部参数相似的 OOD 性能**（Figure 11 右），表明语言模型主干是承载泛化能力的关键参数组。

### 连续技能合并

RETAIN 支持将多个技能顺序合并到通用策略中，通过迭代应用合并公式实现连续学习：

$$\tilde{\theta}_n = (1 - \alpha) \cdot \tilde{\theta}_{n-1} + \alpha \cdot \theta_{\mathrm{ft},n}$$

其中 $\tilde{\theta}_{n-1}$ 是合并前 $n-1$ 个技能后的策略权重，$\theta_{\mathrm{ft},n}$ 是仅在第 $n$ 个任务上微调的权重。实验表明，RETAIN 在顺序学习两个任务时显著优于顺序 Co-FT，不会遗忘先前获得的能力（Figure 12）。

### 输入输出流

整体推理流程为：给定观测图像 $s_t$ 和任务指令 $T$，视觉编码器提取特征后送入语言模型主干进行跨模态融合，动作专家根据融合表示生成动作 $a_t$。RETAIN **不改变推理管线**，仅在部署前通过权重空间插值生成最终策略参数，因此不增加任何推理时延或计算开销。

### 问题形式化

给定预训练通用策略 $\pi_{\boldsymbol{\theta}_{\text{pre}}}$ 和一个包含少量演示数据的目标任务数据集 $\mathfrak{D}_{\eta}$，微调的目标是使策略适应新任务。标准的行为克隆损失函数定义为：

$$\mathcal{L}_{\mathrm{BC}}(\boldsymbol{\theta};\mathfrak{D}) := -\frac{1}{|\mathfrak{D}|}\sum_{(s_t,a_t,T)\in\mathfrak{D}}\log\pi_{\boldsymbol{\theta}}(a_t\mid s_t,T) \tag{1}$$

其中 $s_t$ 为观测状态，$a_t$ 为动作，$T$ 为任务描述。直接在该损失上微调（Task-FT）会导致严重过拟合：策略在微调数据见过的场景（ID）上表现尚可，但在目标任务未见变体（OOD）上急剧退化，同时丧失预训练的通用能力（Fig. 4）。

### RETAIN 核心机制：权重空间线性插值

RETAIN 的核心操作极其简洁：对预训练策略权重 $\boldsymbol{\theta}_{\text{pre}}$ 和微调后策略权重 $\boldsymbol{\theta}_{\text{ft}}$ 进行线性插值，得到最终部署的策略权重 $\tilde{\boldsymbol{\theta}}$：

$$\tilde{\boldsymbol{\theta}} = (1 - \alpha) \cdot \boldsymbol{\theta}_{\text{pre}} + \alpha \cdot \boldsymbol{\theta}_{\text{ft}} \tag{2}$$

其中 $\alpha \in [0,1]$ 是合并系数，控制预训练通用知识与目标任务专长之间的权衡。当 $\alpha=0$ 时退化为原始预训练策略，$\alpha=1$ 时退化为完全微调策略。该操作不引入任何额外推理成本，仅在权重层面进行一次线性组合。

### 模态感知合并

现代 VLA 策略通常由三个功能模块组成（Fig. 2）：视觉编码器（Vision Encoder）、语言模型主干（Language Model Backbone）、动作专家/解码器（Action Expert/Decoder）。RETAIN 扩展为模态感知合并，为不同模块设置独立的合并系数：

$$\begin{pmatrix}\tilde{\boldsymbol{\theta}}_v \\ \tilde{\boldsymbol{\theta}}_l \\ \tilde{\boldsymbol{\theta}}_a\end{pmatrix} = \left[1 - \begin{pmatrix}\alpha_v \\ \alpha_l \\ \alpha_a\end{pmatrix}\right] \cdot \begin{pmatrix}\boldsymbol{\theta}_{\text{pre},v} \\ \boldsymbol{\theta}_{\text{pre},l} \\ \boldsymbol{\theta}_{\text{pre},a}\end{pmatrix} + \begin{pmatrix}\alpha_v \\ \alpha_l \\ \alpha_a\end{pmatrix} \cdot \begin{pmatrix}\boldsymbol{\theta}_{\text{ft},v} \\ \boldsymbol{\theta}_{\text{ft},l} \\ \boldsymbol{\theta}_{\text{ft},a}\end{pmatrix} \tag{3}$$

消融实验揭示了一个关键发现：**仅合并语言模型主干参数（$\alpha_l < 1$，$\alpha_v = \alpha_a = 1$）即可达到与合并全部参数相似的 OOD 性能**（Fig. 11 右），表明语言模型是承载跨任务泛化能力的核心模块。

### 连续技能合并

RETAIN 天然支持顺序学习多个任务而不遗忘先前能力。给定第 $n$ 个任务的微调权重 $\boldsymbol{\theta}_{\text{ft},n}$，迭代合并公式为：

$$\tilde{\boldsymbol{\theta}}_n = (1 - \alpha) \cdot \tilde{\boldsymbol{\theta}}_{n-1} + \alpha \cdot \boldsymbol{\theta}_{\text{ft},n}, \quad n \in \{1, \dots, N\} \tag{4}$$

其中 $\tilde{\boldsymbol{\theta}}_0 = \boldsymbol{\theta}_{\text{pre}}$。实验表明，在连续学习两个技能的场景下，RETAIN 在所有任务和评估类型上均显著优于顺序 Co-FT（Fig. 12），验证了该方法在持续学习场景中的有效性。

### 微调数据配比

RETAIN 支持两种微调范式：
- **Task-FT**：仅使用目标任务数据 $\mathfrak{D}_{\eta}$ 进行微调，然后合并。
- **Co-FT**：在微调时混合预训练数据 $\mathfrak{D}_{\text{pre}}$ 与目标任务数据 $\mathfrak{D}_{\eta}$，再进行合并。

实验一致表明，Co-FT 结合模型合并（RETAIN-co-FT）在所有评估设置中均优于仅使用模型合并（RETAIN-task-FT）（Fig. 7, 8），说明在微调阶段保留对预训练数据的接触有助于维持权重空间中的线性连通性。

## 实验与关键发现

### 核心瓶颈与因果机制

标准微调（Task-FT）在少量目标演示数据上训练时，策略迅速过拟合：随着训练步数增加，通用能力（GENERALIST）和分布外（OOD）性能急剧下降，甚至在微调数据已见过的场景（ID）上也开始退化（Fig. 4）。这一现象揭示了核心瓶颈——微调后策略的权重空间中，适应目标任务的局部解与保留预训练泛化能力的解之间存在巨大鸿沟。

RETAIN通过一个简洁的因果控制变量解决此问题：微调后策略与预训练策略之间的线性插值系数α（0≤α≤1）。该系数直接控制保留预训练通用知识与适应目标任务特定知识之间的权衡。核心洞察在于：对预训练策略和微调后策略的权重进行简单线性插值，可以在权重空间中找到一个既保留预训练模型泛化能力又具备目标任务专长的解决方案，且不增加任何推理成本。

### 主实验结果

**DROID真实环境实验**（Fig. 7）：在两个任务上，RETAIN-co-FT在OOD评估中显著优于所有基线方法。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_uWJwQ5SZoM/figures/009_Figure_7.jpg]]
*Figure 7: RETAIN results on two DROID tasks, whiteboard (top) and plates (bottom). RE-TAIN significantly outperform baselines in OOD evaluation and is competitive in ID evaluations, showing that it is able to learn new skills robustly and can generalize to its variations using pretrained knowledge. RETAIN also does best on generalist evaluations, showing that it is best at retaining abilities to solve old tasks. We tune merging coefficient α on one “val” OOD scene, and use the same value for two other “test” OOD scenes*

- **白板（whiteboard）任务**：RETAIN-co-FT在OOD测试场景中成功率约80%，而Task-FT基线平均仅约40%，提升约40个百分点。
- **盘子（plates）任务**：RETAIN-co-FT在OOD评估中成功率超过60%，Task-FT基线平均约30%，提升约30个百分点。
- 在通用能力（Generalist）评估上，RETAIN同样表现最优，证明其能有效保留预训练获得的旧任务解决能力。
- ID性能方面，RETAIN与基线方法保持竞争力。

**LIBERO仿真环境实验**（Fig. 8）：三个任务的平均OOD性能上，RETAIN-co-FT均优于所有基线方法（如Co-FT约70%，RETAIN-co-FT约85%），趋势与DROID实验一致。值得注意的是，LIBERO上的OOD提升幅度小于DROID，这一差异的原因尚需进一步分析。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_uWJwQ5SZoM/figures/010_Figure_8.jpg]]
*Figure 8: RETAIN results averaged over the three LIBERO tasks. Similar trend as Fig. 7*

**预训练数据量扩展性**（Fig. 9）：RETAIN的性能随预训练数据量增加而显著提升。使用DROID-All + PI（最大预训练数据量）训练的模型，其OOD性能接近ID性能水平，表明更大规模的预训练数据为参数合并提供了更丰富的泛化知识基础。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_uWJwQ5SZoM/figures/011_Figure_9.jpg]]
*Figure 9: RETAIN performs better on OOD tasks when the pretrained generalist policy is trained on more data. OOD performance is averaged across three plates scenes*

### 关键消融实验

**协同微调（co-FT）的作用**：在所有评估设置中，协同微调结合模型合并（RETAIN-co-FT）始终优于仅使用模型合并（RETAIN-task-FT）（Fig. 7, 8）。这表明在微调阶段混合预训练数据，为后续的权重插值提供了更有利的优化轨迹。

**模态特定合并分析**（Fig. 11）：对视觉编码器、语言模型主干、动作专家分别设置合并系数（α_v, α_l, α_a）的网格搜索显示，语言模型参数α_l对OOD性能的影响最大。更重要的是，仅合并语言模型参数（α_a=α_v=1, α_l<1）即可达到与合并全部参数相似的OOD性能（Fig. 11右），这大幅简化了实际部署中的超参数搜索空间。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_uWJwQ5SZoM/figures/016_Figure_11.jpg]]
*Figure 11: Language model parameters have the most influence in modality-specific merging. Left: Merged model’s OOD performance over a grid search of $\alpha _ { a } , \alpha _ { v } , \alpha _ { l }$ , , and $\alpha _ { l }$ has the most impact. Middle: OOD performance of $\alpha _ { a }$ and $\alpha _ { v }$ averaged over different $\alpha _ { l }$ . , and higher values are better. Right: Merging only the language model parameters ( $\alpha _ { a } = \alpha _ { v }$ = 1 , $\alpha _ { l }$ < 1 ) performs similarly to merging all parameters

**合并系数敏感性**（Fig. 10）：在LIBERO的不同OOD类型（位置变化、位置+干扰物变化、背景变化）上，OOD性能随α的变化曲线显示，位置变化类OOD对α最敏感，在α≈0.5时性能提升最为显著。在DROID任务上，α在0.5左右普遍表现良好（Section A.8.1）。

**连续技能合并**（Fig. 12）：RETAIN能够连续合并多个技能而不遗忘先前能力。在顺序学习两个任务（Plates→Whiteboard）时，RETAIN在所有任务和评估类型上均显著优于顺序Co-FT，证明参数合并策略天然支持持续学习场景。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_uWJwQ5SZoM/figures/017_Figure_12.jpg]]
*Figure 12: RETAIN enables continual adaptation to a sequence of two skills. Evaluation results show the performance of the final policy after sequentially finetuning on two tasks, evaluated on different scenes. OOD performance averaged across two test scenes*

**标准微调的过拟合不可逆性**（Fig. 16）：即使精心调节学习率和训练步数，标准微调仍会过拟合并丧失泛化能力，说明仅靠超参数调优无法解决根本问题。

### 失败模式与局限性

尽管RETAIN显著提升了OOD鲁棒性，部分场景下策略仍可能因动作执行不精确或语义理解错误而失败（Fig. 24, 25）。此外，合并系数α需要针对每个任务和场景在验证集上手动调节，缺乏自动选择的启发式方法。当前实验仅在基于π0架构的VLA策略上进行，泛化到其他架构（如扩散策略）尚待验证。

## 定位与知识库关联

### 方法定位与核心差异

RETAIN 的核心操作是在权重空间中对预训练通用策略与目标任务微调策略进行线性插值，公式为 $\tilde{\theta} = (1 - \alpha) \cdot \theta_{\mathrm{pre}} + \alpha \cdot \theta_{\mathrm{ft}}$（公式2）。这一操作与现有微调范式形成了根本性差异：标准方法直接使用微调后的参数 $\theta_{\mathrm{ft}}$ 作为最终策略，而 RETAIN 通过引入合并系数 $\alpha$（$0 \leq \alpha \leq 1$）在权重空间中重新定位解的位置，从而在保留预训练泛化能力与获取目标任务专长之间建立显式权衡。

**Task-FT**（全参数微调）是最直接的对比基线，仅使用目标数据集进行行为克隆，无任何正则化约束。其核心失败模式是严重过拟合：即使精心调节学习率与训练步数，策略的通用能力仍随训练急剧退化，且无法将预训练知识迁移到目标任务的未见变体上（Figure 4、Figure 16）。**Co-FT**（Fu et al., 2024）通过在微调时混合预训练数据来缓解遗忘，但实验表明其在 OOD 场景下的提升远不及 RETAIN（Figure 7、8），且 RETAIN-co-FT（协同微调后再合并）在所有评估设置中均优于单独使用 Co-FT。**LoRA**（Hu et al., 2022）通过低秩适配器限制参数更新幅度，**Freeze-FT** 则冻结语言模型主干仅微调视觉编码器和动作专家，两者均试图通过约束参数空间来保留预训练知识，但在 DROID 和 LIBERO 的 OOD 评估中成功率普遍仅 30–50%，远低于 RETAIN 的约 80%（Figure 7）。**Scratch**（从头训练）和 **Base**（未微调的预训练策略）分别作为性能下界和参考上限。

RETAIN 与上述方法的本质区别在于：它不是通过限制微调过程本身来防止遗忘，而是承认微调必然导致参数偏离，随后通过插值“拉回”到保留泛化能力的位置。这一设计使得 RETAIN 不增加任何推理成本，且与微调方式（task-FT 或 co-FT）正交兼容。

### 与模型合并文献的关联

RETAIN 在方法层面属于模型合并（model merging）范式，与自然语言处理和视觉领域的权重插值工作共享技术基因。其核心假设——微调前后的策略在权重空间中存在线性模式连通性（linear mode connectivity），使得插值路径上的解兼具双方优势——与 Wortsman et al. (2022) 在 CLIP 模型上的发现一致。但 RETAIN 首次将该范式引入机器人 VLA 策略微调场景，并揭示了两个领域特有的洞见：（1）在 VLA 架构中，仅合并语言模型主干参数即可达到与合并全部参数相似的 OOD 性能（Figure 11 右），这意味着泛化能力主要编码在语言模型中；（2）合并系数 $\alpha$ 在 0.5 左右时在 DROID 任务上普遍表现良好（Section A.8.1），但不同 OOD 类型对 $\alpha$ 的敏感度不同（Figure 10）。

### 适用边界与局限

**架构依赖性**：当前实验仅在基于 π0 架构的 VLA 策略上进行验证，该架构由视觉编码器、语言模型主干和动作专家/解码器组成（Figure 2）。RETAIN 在其他 VLA 架构（如扩散策略、Transformer 变体）上的有效性尚待验证。

**系数选择成本**：合并系数 $\alpha$（以及模态特定系数 $\alpha_v, \alpha_l, \alpha_a$）需要针对每个任务和场景在验证 OOD 场景上手动调优，缺乏自动选择的启发式方法。论文在 DROID 实验中仅在 $\{0.25, 0.5, 0.75\}$ 中搜索，虽然该范围已能取得显著效果，但更精细的调优可能进一步提升性能。

**理论解释不足**：对模型合并为何能够显著提升泛化性缺乏完整的理论解释，目前多基于线性模式连通性的经验假设。论文未深入分析权重空间中插值路径的损失景观（loss landscape）特性，也未解释为何语言模型参数主导合并效果。

**任务范围限制**：当前工作主要关注行为克隆的微调范式，未探索在在线强化学习或交互式模仿学习场景中应用 RETAIN。此外，尽管 RETAIN 展示了连续合并多个技能的能力（Figure 12），但实验仅涉及两个任务的顺序学习，更多任务的累积效应尚不明确。

**已知失败模式**：在部分情况下 RETAIN 策略仍可能因动作执行不精确或语义理解错误而失败（Figure 24、25），说明参数合并并不能完全弥补微调数据不足带来的根本性局限。

### 开放问题

1. **理论根基**：模型参数合并为何能显著提升泛化性的深层理论原因是什么？线性模式连通性在 VLA 策略空间中的成立条件与边界是什么？
2. **自动化系数选择**：能否为合并系数 $\alpha$ 设计一种无需验证集的自动选择策略，例如基于权重空间几何特性或梯度信息？
3. **架构泛化**：RETAIN 在其他 VLA 架构（如扩散策略、ACT、RT 系列）上的有效性如何？不同架构的哪些模块是合并的关键？
4. **学习范式扩展**：是否可以将 RETAIN 扩展到在线强化学习或交互式模仿学习场景，在探索与利用的循环中动态调整合并系数？
5. **多任务累积效应**：当连续合并更多任务（$N > 2$）时，迭代合并公式 $\tilde{\theta}_n = (1 - \alpha) \cdot \tilde{\theta}_{n-1} + \alpha \cdot \theta_{\mathrm{ft},n}$ 是否仍能保持稳定？是否存在遗忘累积效应？
6. **预训练数据质量与合并效果的关系**：Figure 9 显示更多预训练数据显著提升 RETAIN 的 OOD 性能，但数据质量、多样性与合并效果之间的定量关系尚未被系统研究。

## 原文 PDF

![[paperPDFs/ICLR_2026/Robust_Fine_tuning_of_Vision_Language_Action_Robot_Policies_via_Parameter_Merging.pdf]]
