---
title: Test-Time Perturbation Tuning with Delayed Feedback for Vision-Language-Action Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Test_Time_Perturbation_Tuning_with_Delayed_Feedback_for_Vision_Language_Action_Models.pdf
project_link: null
code_link: "https://github.com/zhoujiahuan1991/CVPR2026-PDF"
aliases:
- PLDFP
- TTPTDFVLAM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 测试时通过两个互补机制介入：① 基于预测不确定性的自适应数据增强与动作投票，打破固定的伪相关模式；② 由延迟环境反馈驱动的轻量扰动头（P head），实时调整动作 logits，纠正过度自信的误判，而不修改基础模型。
primary_logic: 无需微调基础模型即可在测试时有效提升 VLA 决策性能：利用模型自身的不确定性有节制地扩大观察分布，并结合延迟反馈信号进行有监督的 logit 扰动更新，可以缓解传统的自监督 TTA（如熵最小化）在模型错误时加剧偏差的风险，从而实现更稳定、准确的测试时适应。
claims:
- PDF 在 LIBERO 四个子套件上取得了最高的平均成功率和最优的平均排名（0.77 SR, 2.5 mean rank），超越了包括微调模型在内的所有对比方法。
- 与只进行样本过滤的 TTA 方法 MG‑Select 相比，PDF 的平均成功率提升近 6 个百分点，突显了不确定性加权的动作投票和延迟反馈扰动学习的联合优势。
- 在 Atari‑57 上，PDF 将 Human Normalized Score 从基线 Jat 的 0.97 提升至 1.07，57 款游戏中 47 款获得正向提升，平均改善幅度达 11.28%。
- 消融实验表明，移除延迟反馈（PDF w/o DF）会导致物体操作和长期任务的成功率大幅下降（如 Object 套件降至 0.50），证明反馈驱动的扰动学习对鲁棒性至关重要。
---

# Test-Time Perturbation Tuning with Delayed Feedback for Vision-Language-Action Models

> [!tip] 核心洞察
> 无需微调基础模型即可在测试时有效提升 VLA 决策性能：利用模型自身的不确定性有节制地扩大观察分布，并结合延迟反馈信号进行有监督的 logit 扰动更新，可以缓解传统的自监督 TTA（如熵最小化）在模型错误时加剧偏差的风险，从而实现更稳定、准确的测试时适应。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向视觉-语言-动作模型的延迟反馈测试时扰动学习 |
| 英文题名 | Test-Time Perturbation Tuning with Delayed Feedback for Vision-Language-Action Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zang_Test-Time_Perturbation_Tuning_with_Delayed_Feedback_for_Vision-Language-Action_Models_CVPR_2026_paper.html) · [Code](https://github.com/zhoujiahuan1991/CVPR2026-PDF) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Perturbation learning with Delayed Feedback (PDF) |
| Dataset | LIBERO, Atari-57 |

> [!tip] 效果简介
> - LIBERO (Spatial, Object, Goal, Long) 上，成功率 (Success Rate) 0.77 (平均) vs 0.69 (复现 OpenVLA, 平均) (+7.4%)。
> - Atari-57 上，Human Normalized Score (HNS) 1.07 vs 0.97 (Jat) (+0.10 / +10.3%)。

## 概述

视觉-语言-动作模型（VLA）在机器人操控中展现出强大的语义理解与泛化潜力，但现有模型普遍存在**轨迹过拟合**（trajectory overfitting）问题：模型过度依赖动作与实体之间的伪相关性，倾向于复现记忆中的动作序列，而非真正理解任务语义。这导致模型对物体姿态、位置等微小环境变化极为脆弱——即使目标被遮挡，机械臂仍会机械地重复训练时习得的动作轨迹（见 Figure 1）。

针对这一瓶颈，本文提出 **PDF（Perturbation learning with Delayed Feedback）**，一种无需验证器的测试时适应（TTA）框架。PDF 的核心思路是：在测试时冻结基础 VLA 的全部参数，仅通过两个互补机制介入决策过程——① **基于不确定性的自适应数据增强与动作投票**，利用模型自身的预测熵动态分配增强预算，打破固定的伪相关模式；② **延迟反馈引导的扰动学习**，在回合结束后利用成功/失败信号更新一个轻量的扰动头（P head），纠正过度自信的错误决策，而不修改基础模型。与传统自监督 TTA（如熵最小化）在模型错误时可能加剧偏差不同，PDF 的反馈驱动机制能够有效抑制虚假高置信度，引导模型向正确方向调整（见 Figure 2）。

在 **LIBERO** 四个子套件（Spatial、Object、Goal、Long）上，PDF 取得了 **0.77 的平均成功率**和 **2.5 的平均排名**，超越包括微调模型在内的所有对比方法，较复现的 OpenVLA 基线提升 **7.4 个百分点**（见 Table 1）。在 **Atari-57** 上，PDF 将 Human Normalized Score 从基线 Jat 的 0.97 提升至 **1.07**，57 款游戏中 **47 款获得正向提升**，平均改善幅度达 **11.28%**（见 Figure 4）。消融实验进一步证实，延迟反馈与数据增强两个组件缺一不可——移除延迟反馈后，Object 套件成功率从 0.72 骤降至 0.50（见 Table 2）。

PDF 的贡献在于揭示了一条无需微调基础模型即可有效提升 VLA 测试时决策性能的路径：利用模型自身的不确定性有节制地扩大观察分布，并结合延迟反馈进行有监督的 logit 扰动更新，在保持计算高效（仅更新 9M 参数，无需基础模型梯度）的同时，实现了更稳定、准确的测试时适应。

## 背景与动机

### 视觉-语言-动作模型的轨迹过拟合困境

视觉-语言-动作模型（VLAs）将大规模预训练的视觉与语言理解能力引入机器人操作，展现出令人瞩目的泛化潜力。然而，这类模型面临一个深层且隐蔽的瓶颈：**轨迹过拟合（trajectory overfitting）**。模型在模仿学习过程中，过度关注动作与实体之间的**伪相关性**（spurious correlations），倾向于复现记忆中的专家动作序列，而非真正理解语义任务目标。这导致模型对物体姿态、光照、背景布局等微小环境变化极为脆弱——即使任务语义完全不变，仅因目标物体的位置或朝向发生细微偏移，模型便可能机械地重复错误的操作轨迹。

Figure 1 直观地揭示了这一现象：在目标物体被遮挡的情况下，机械臂仍模仿专家轨迹执行抓取动作；注意力图显示模型完全忽略了任务目标，而数据增强后注意力重新聚焦于正确物体，决策也随之纠正。这表明，轨迹过拟合并非简单的感知失败，而是模型在**决策层面**形成了顽固的伪相关行为模式。

### 现有测试时适应的局限

针对上述问题，测试时适应（Test-Time Adaptation, TTA）提供了一条无需重新训练即可提升推理性能的路径。然而，主流的自监督 TTA 方法——如熵最小化——在 VLA 场景中可能适得其反。当模型对错误动作产生过度自信时，熵最小化会进一步放大错误 logits，加剧偏差而非纠正它（Figure 2）。另一方面，基于验证器的 TTA 方法依赖额外的奖励模型或成功检测器进行动作筛选，这引入了外部组件的不确定性和计算开销。

### 本文动机与核心思路

本文的核心洞察在于：**无需微调基础模型，通过测试时的两个互补机制即可有效缓解轨迹过拟合**。具体而言：

1. **利用模型自身的不确定性**有节制地扩大观察分布——当模型对当前决策犹豫时，施加更强的数据增强以打破伪相关模式；当模型自信时，则保持轻量扰动以维持效率。

2. **引入延迟环境反馈**作为监督信号，驱动一个轻量的可学习扰动头（P head）实时修正动作 logits。与自监督 TTA 不同，这种反馈驱动的适应能够纠正过度自信的误判，将模型拉回正确决策方向。

这两个机制共同构成了 **PDF（Perturbation learning with Delayed Feedback）**——一个无验证器的 TTA 框架，在保持 VLA 全部参数冻结的前提下，仅更新 9M 参数的扰动头，实现了稳定、高效的测试时性能提升。

## 核心创新

PDF 的核心创新在于对 VLA 测试时适应范式的双重重构：将传统的**自监督熵最小化**替换为**不确定性感知的动作投票**与**延迟反馈驱动的扰动学习**，在完全冻结基础模型的前提下实现稳健的决策修正。其与 baseline 的关键差异体现在以下四个 changed slots 上。

### 从无适应到不确定性感知的测试时策略

基线 VLA（如 **OpenVLA**（Kim et al., CoRL 2024））在测试时直接使用冻结模型进行单步推理，对物体姿态、光照等微小环境变化缺乏抵抗力。PDF 引入**基于不确定性的自适应数据增强与动作投票**机制：首先通过 LM head 输出的归一化熵量化当前决策的不确定性（Equation 1），再据此动态分配增强预算（Equation 2）——高不确定性时施加更多视角扰动，低不确定性时减少计算开销。这种“有节制地扩大观察分布”的策略，打破了模型对记忆轨迹中动作-实体伪相关的过度依赖。

### 从单次 argmax 到双头协同与多数投票

基线 VLA 的动作决策仅依赖 LM head 输出的 logits 进行单次 argmax，当模型对错误动作过度自信时缺乏纠错手段。PDF 引入一个可学习的**扰动头（P head）**，与冻结的 LM head 并行工作，二者输出加权求和形成修正后的 logits：

$$\tilde { z } _ { t } = h _ { \phi } ( f _ { t } ) + \lambda h _ { \theta } ( f _ { t } )$$

在此基础上，对多个增强视图生成的候选动作进行**多数投票**，产生最终执行的单一动作。这一设计使得即使 LM head 在个别视图上产生错误 logits，投票机制也能通过跨视图一致性将其抑制。消融实验（Table 3）表明，维度级投票在 LIBERO 上优于动作级投票，因为它允许不同视图在单个动作维度上达成共识，更有效地缓解轨迹过拟合。

### 从全参数更新到仅 9M 参数的轻量适应

与需要全参数微调或访问基础模型梯度的 baseline（如 **OpenVLA-DPO**（Chen et al., Arxiv 2025）使用 93–130M 可训练参数）不同，PDF 冻结 VLA 的所有组件——视觉编码器、因果 Transformer、LM head——**仅在线更新 P head 的 9M 参数**，且无需基础模型的梯度访问。这带来了两个关键优势：一是计算效率极高，适应过程轻量可部署；二是避免了全参数更新可能引入的灾难性遗忘，保持基础模型的通用能力不被破坏。

### 从无反馈/即时奖励到延迟反馈引导的扰动学习

传统 TTA 方法（如熵最小化）在测试时完全依赖自监督信号，当模型对错误行为过度自信时反而会放大偏差（Figure 2 直观展示了这一现象——红色错误 logits 被进一步推高）。PDF 利用**回合结束后的延迟反馈**（成功/失败或累积奖励）通过 REINFORCE 型损失指导 P head 更新：

$$\mathcal { L } _ { \mathrm { P D F } } = - ( r - b ) \log \pi _ { \phi } + \lambda _ { \mathrm { K L } } \mathbb { I } [ r > b ] \mathrm { K L } ( \pi _ { \phi } \parallel \tilde { \pi } )$$

该损失由两项组成：REINFORCE 项利用奖励信号引导扰动头向成功方向更新；KL 正则项在成功回合中约束扰动幅度，防止过度偏离原始策略。消融实验（Table 2）证实，移除延迟反馈（PDF w/o DF）导致 Object 套件成功率从 0.72 骤降至 0.50，Goal 从 0.85 降至 0.77，证明反馈驱动的扰动学习对纠正伪相关决策不可或缺。损失消融（Figure 6）进一步表明，REINFORCE 项与 KL 正则项缺一不可，其中 KL 正则项的贡献更为显著。

### 创新边界与局限

PDF 并未从根本上消除轨迹过拟合，而是通过测试时扰动减轻其负面影响。延迟反馈仅在回合结束后可用，导致适应在长周期任务中存在显著滞后，无法支持每步即时纠正。在极端分布偏移或完全未见过的物体属性下，不确定性估计与投票机制的可靠性仍需进一步验证。

## 整体框架

PDF 的整体设计围绕一个核心原则展开：**冻结 VLA 全部基础参数，仅在测试时通过轻量的外部扰动头与不确定性感知的决策机制来提升鲁棒性**。图 3 给出了完整的信息流与优化闭环。

### 测试时推理流程

在每个时间步，系统接收像素观测 $o_t$ 和文本指令 $c_t$，构成多模态状态 $s_t = (o_t, c_t)$。推理过程分为四个阶段：

1. **不确定性估计**：VLA 的 LM head 输出动作 logits 后，PDF 计算归一化动作熵作为不确定性度量：
   $$\mathcal{U}_t = -\frac{1}{\log K}\sum_{k=1}^{K} p(a_k \mid s_k) \log p(a_k \mid s_k)$$
   该值反映了模型对当前决策的自信程度——熵越高，模型越“犹豫”，越需要借助外部干预来避免伪相关陷阱。

2. **自适应数据增强**：根据不确定性动态分配增强预算 $N_t = N_{\max} \cdot \mathcal{U}_t$。高不确定性时施加更多视角变换（如色彩抖动、裁剪等），迫使模型从不同观察中提取共识；低不确定性时减少扰动以节省计算。这与传统 TTA 固定增强策略的关键区别在于：**增强强度由模型自身的困惑程度驱动，而非盲目施加**。

3. **双头决策与动作投票**：原始观测与增强视图经视觉编码器和因果 Transformer 编码为联合特征 $f_t$ 后，分别送入两个决策头：
   $$\tilde{z}_t = h_{\phi}(f_t) + \lambda h_{\theta}(f_t)$$
   其中 $h_{\phi}$ 为冻结的 LM head，$h_{\theta}$ 为可学习的扰动头（P head，仅 9M 参数）。最终 logits $\tilde{z}_t$ 经 softmax 产生候选动作分布，通过多数投票选出单一执行动作。

4. **滚动缓冲区存储**：每个时间步的特征 $f_t$ 和 logits $\tilde{z}_t$ 被存入缓冲区，供回合结束后的延迟反馈优化使用。

### 延迟反馈优化闭环

回合结束后，环境返回二元成功/失败信号或累积奖励 $r$。PDF 利用这一**延迟反馈**通过 REINFORCE 型损失更新 P head：
$$\mathcal{L}_{\mathrm{PDF}} = -(r - b)\log\pi_{\phi} + \lambda_{\mathrm{KL}} \mathbb{I}[r > b] \mathrm{KL}(\pi_{\phi} \parallel \tilde{\pi})$$

该损失包含两个互补项：**REINFORCE 项**利用奖励信号 $r$ 与基线 $b$ 的差异提供梯度方向，鼓励成功轨迹的动作分布；**条件 KL 正则项**仅在 $r > b$ 时激活，约束扰动头不过度偏离基础模型的原始输出，防止灾难性遗忘。这种“奖励引导 + 置信度约束”的双重机制，使 PDF 能够纠正 VLA 的过度自信误判（图 2 示意），同时避免传统熵最小化 TTA 在模型错误时放大偏差的风险。

### 关键设计取舍

- **参数效率**：仅 P head 参与梯度更新，基础 VLA 完全冻结，无需访问基座模型的梯度，参数量仅为对比方法（93–130M）的约十分之一。
- **反馈滞后性**：延迟反馈仅在回合结束时可用，意味着 P head 的更新是跨回合的——当前回合的决策不受本轮反馈影响，这在长周期任务中存在固有滞后，是方法的一个结构性限制。
- **无验证器依赖**：与 MG-Select 等需要外部验证器的方法不同，PDF 的反馈直接来自环境，降低了部署门槛。

### 补充图表

![[assets/figures/papers/paper_list_l2422_https_openaccess_thecvf_com_content_CVPR2026_html_Zang_Test_Time_Perturb/figures/003_Figure_3.jpg]]
*Figure 3: The overall framework of our proposed PDF. At test time, the VLA receives pixel observation ot and instruction ct. Action-logit uncertainty Ut is estimated to allocate an adaptive augmentation budget*

## 核心模块与公式推导

PDF 框架由两个核心机制构成：**基于不确定性的动作投票**和**延迟反馈引导的自适应扰动学习**。整个测试时流程如图 3 所示，基础 VLA 模型的所有参数（视觉编码器、因果 Transformer、LM head）保持冻结，仅在线更新一个轻量的扰动头。

### 不确定性估计与自适应增强预算

VLA 在测试时接收像素观测 $o_t$ 和文本指令 $c_t$，构成多模态状态 $s_t = (o_t, c_t)$。LM head 输出动作分布后，PDF 计算归一化的 Shannon 熵作为决策不确定性的度量：

$$\mathcal{U}_t = -\frac{1}{\log K} \sum_{k=1}^{K} p(a_k \mid s_k) \log p(a_k \mid s_k) \tag{1}$$

其中 $K$ 为动作空间维度，归一化因子 $1/\log K$ 将熵值约束在 $[0, 1]$ 区间。高熵表示模型对当前决策缺乏信心，暗示可能陷入了轨迹过拟合导致的伪相关模式。

基于此不确定性，PDF 动态分配数据增强预算：

$$N_t = N_{\max} \cdot \mathcal{U}_t \tag{2}$$

$N_{\max}$ 是预设的最大增强视图数。当模型不确定性低时，几乎不施加扰动，保持推理效率；当不确定性高时，生成更多增强视图以扩大观察分布、打破伪相关。消融实验（Figure 5）证实，固定使用过大增强预算反而损害性能，验证了自适应分配的必要性。

### 扰动头与最终动作 Logits

原始观测与 $N_t$ 个增强视图共同输入视觉编码器和因果 Transformer，得到多模态特征 $f_t$。冻结的 LM head $h_\phi$ 和可学习的扰动头 $h_\theta$ 分别处理该特征，产生修正后的 logits：

$$\tilde{z}_t = h_\phi(f_t) + \lambda h_\theta(f_t) \tag{3}$$

其中 $\lambda$ 为扰动强度系数。扰动头 $h_\theta$ 仅含约 9M 参数，无需访问基础模型的梯度，显著降低了测试时适应的计算开销。

### 多数投票与动作选择

对每个增强视图，从 $\tilde{z}_t$ 解码候选动作。所有候选动作通过多数投票产生最终执行动作 $a_t$。对于 LIBERO 等机器人操作任务，采用**维度级投票**（dimension-wise voting）——对动作向量的每个维度（如末端执行器的位移、旋转分量）分别投票；对于 Atari 等离散动作空间，采用**动作级投票**（action-wise voting）。Table 3 的对比表明，维度级投票在 LIBERO 上更有效地缓解轨迹过拟合，因为它允许不同视图在单个动作分量上达成跨视图一致。

### 延迟反馈引导的扰动头更新

每个回合结束后，环境返回延迟反馈 $r$（LIBERO 中为 0/1 成功信号，Atari 中为累积奖励）。PDF 利用滚动缓冲区中存储的历史特征和 logits，通过以下损失函数更新扰动头：

$$\mathcal{L}_{\mathrm{PDF}} = -(r - b) \log \pi_\phi + \lambda_{\mathrm{KL}} \mathbb{I}[r > b] \mathrm{KL}(\pi_\phi \parallel \tilde{\pi}) \tag{5}$$

损失由两项组成：
- **REINFORCE 型策略梯度项**：$-(r - b) \log \pi_\phi$，其中 $b$ 为基线奖励，当 $r > b$ 时增强当前策略的概率，反之抑制。
- **条件 KL 散度正则项**：仅在回合成功（$r > b$）时激活，约束扰动后的策略 $\pi_\phi$ 不过度偏离原始策略 $\tilde{\pi}$，防止灾难性遗忘。

Figure 6 的消融实验表明，两项缺一不可：移除 REINFORCE 项或 KL 正则项均导致五个基准上的整体性能退化，其中 KL 正则项的贡献更为显著。Table 2 进一步证实，完全移除延迟反馈（PDF w/o DF）会使 Object 套件成功率从 0.72 骤降至 0.50，Goal 套件从 0.85 降至 0.77，说明反馈驱动的扰动学习对纠正物体操作和长期任务中的伪相关决策至关重要。

### 补充图表

![[assets/figures/papers/paper_list_l2422_https_openaccess_thecvf_com_content_CVPR2026_html_Zang_Test_Time_Perturb/figures/002_Figure_2.jpg]]
*Figure 2: Comparison between traditional self-supervised testtime adaptation (TTA) and our PDF. Dashed bars indicate logits before adaptation; solid bars indicate logits after adaptation. Red bars denote incorrect-action logits; green bars denote correctaction logits. When VLAs become overconfident in incorrect behaviors, entropy-minimization-based TTA can amplify these errors by further boosting the wrong logits. In contrast, PDF corrects such misbehaviors by jointly mitigating the overconfidence issue and elevating the logits of correct actions, guiding the model toward accurate decisions*

## 实验与分析

### 4.1 实验设置

PDF 在两个性质迥异的决策基准上接受评估：**LIBERO**（真实机器人操作的仿真环境，包含 Spatial、Object、Goal、Long 四个子套件，每个套件 10 个任务）和 **Atari-57**（57 款经典街机游戏的集合）。LIBERO 以任务成功率（Success Rate, SR）作为评价指标；Atari-57 采用人类归一化分数（Human Normalized Score, HNS）衡量。基础模型方面，LIBERO 实验基于 **OpenVLA**（Kim et al., CoRL 2024），Atari-57 实验基于 **Jat**（Gallouédec et al., Arxiv 2024）。对比基线包括前沿 TTA 方法 **MG-Select**（Jang et al., Arxiv 2025）、偏好优化方法 **OpenVLA-DPO**（Chen et al., Arxiv 2025）以及针对 LIBERO 微调的 **SFT-4LIBERO**（Li et al., Arxiv 2025）等。

PDF 的核心效率优势在于：仅需更新 9M 参数的 P head，无需访问基础模型梯度，而对比基线通常需要 93–130M 参数的全量梯度。这得益于 PDF 在测试时冻结 VLA 的所有参数（视觉编码器、Transformer、LM head），仅在线优化轻量的扰动头 $h_\theta$。

### 4.2 主实验结果

#### LIBERO 基准

PDF 在 LIBERO 四个子套件上取得了全面的领先优势。如 Table 1 所示，PDF 的平均成功率达到 **0.77**，不仅大幅超越复现的 OpenVLA 基线（平均 0.69，提升 **+7.4%**），还超越了所有对比方法，包括需要微调的 SFT-4LIBERO 和 OpenVLA-DPO。在平均排名（mean rank）上，PDF 以 2.5 的分数位列第一，表明其在各套件上的表现均衡且稳定。

![[assets/figures/papers/paper_list_l2422_https_openaccess_thecvf_com_content_CVPR2026_html_Zang_Test_Time_Perturb/figures/004_Table_1.jpg]]
*Table 1: Performance comparison on the LIBERO benchmark (Spatial, Object, Goal, Long). † denotes reproduced results and SR indicates Success Rate (%). Blue numbers indicate SOTA within each task suite*

尤其值得关注的是与 MG-Select 的对比：MG-Select 作为纯样本过滤的 TTA 方法，平均成功率为 0.71；PDF 在此基础上进一步提升了近 **6 个百分点**。这一差距突显了 PDF 两大组件的联合优势——不确定性加权的动作投票打破了伪相关模式，而延迟反馈引导的扰动学习则纠正了过度自信的误判，二者协同产生的增益远非单一的样本过滤策略所能企及。

#### Atari-57 基准

在 Atari-57 上，PDF 将基线 Jat 的 HNS 从 0.97 提升至 **1.07**，增幅达 **+10.3%**。如 Figure 4 所示，57 款游戏中 **47 款获得正向提升**，平均改善幅度为 **11.28%**。提升最大的游戏为 BOXING（+60.25%），而下降最多的为 BATTLE ZONE（−10.72%）。这一结果说明 PDF 的测试时适应策略具有广泛的泛化性，在离散动作空间和连续帧输入的街机游戏环境中同样有效。

![[assets/figures/papers/paper_list_l2422_https_openaccess_thecvf_com_content_CVPR2026_html_Zang_Test_Time_Perturb/figures/005_Figure_4.jpg]]
*Figure 4: Human normalized score changes across 57 Atari games. Blue bars show performance improvements, orange bars indicate degradation. Games are sorted by improvement magnitude, with BOXING (+60.25%) showing maximum gain and BATTLE ZONE (- 10.72%) showing maximum decline. 47/57 games demonstrate positive performance changes, with 11.28% mean improvement*

### 4.3 核心组件消融

Table 2 系统拆解了 PDF 的两个核心组件——数据增强（DA）与延迟反馈（DF）——各自的贡献。

![[assets/figures/papers/paper_list_l2422_https_openaccess_thecvf_com_content_CVPR2026_html_Zang_Test_Time_Perturb/figures/008_Table_2.jpg]]
*Table 2: Performance comparison of OpenVLA and PDF variants (with and without Delayed Feedback (DF) and Data Augmentation (DA)) across LIBERO benchmark suites (Spatial, Object, Goal, and Long). Reported as success rates over 10 tasks with average performance*

| 方法 | Spatial | Object | Goal | Long | 平均 |
|------|---------|--------|------|------|------|
| OpenVLA（基线） | 0.84 | 0.55 | 0.79 | 0.59 | 0.69 |
| PDF w/o DF + DA | 0.88 | 0.60 | 0.83 | 0.60 | 0.73 |
| PDF w/ DA only | 0.88 | 0.61 | 0.83 | 0.60 | 0.73 |
| **PDF（完整）** | **0.89** | **0.72** | **0.85** | **0.59** | **0.76** |

移除延迟反馈（PDF w/o DF）后，Object 套件成功率从 0.72 骤降至 0.50，Goal 套件从 0.85 降至 0.77。这组数据直接印证了分析中的核心论断：**延迟反馈引导的扰动学习对纠正物体操作和长期任务中的伪相关决策不可或缺**。仅靠数据增强（DA only）无法弥补反馈信号的缺失——增强可以打破部分伪相关模式，但缺乏反馈指导时，模型无法区分哪些打破是有益的、哪些是破坏性的。

数据增强预算的消融实验（Figure 5）进一步揭示了一个反直觉发现：**增强预算并非越大越好**。随着增强数量从 0 增加到 4，所有五个基准（LIBERO 四个子套件 + Atari）的性能均出现单调下降。这验证了不确定性感知的自适应预算分配机制的必要性——过度的数据扰动会引入噪声，淹没原始观测中的有效信息，反而损害决策质量。

![[assets/figures/papers/paper_list_l2422_https_openaccess_thecvf_com_content_CVPR2026_html_Zang_Test_Time_Perturb/figures/006_Figure_5.jpg]]
*Figure 5: Performance degradation under increasing data augmentation budgets. All five benchmarks (LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, LIBERO-Long, and Atari) show performance decline as augmentation budget increases from 0 to 4, indicating that excessive data augmentation harms model effectiveness*

### 4.4 损失函数消融

PDF 损失函数包含两个关键成分：REINFORCE 型策略梯度项和条件 KL 散度正则项。Figure 6 的消融结果表明，**二者缺一不可**。移除任一成分均导致五个基准上的总体性能退化，其中 KL 正则项的贡献更为显著。

![[assets/figures/papers/paper_list_l2422_https_openaccess_thecvf_com_content_CVPR2026_html_Zang_Test_Time_Perturb/figures/007_Figure_6.jpg]]
*Figure 6: Performance comparison across five benchmarks shows that both the KL divergence and the REINFORCE-style term contribute to the full PDF model’s superior performance. Removing either component results in degraded performance, with KL divergence showing greater impact on final results*

KL 散度项的作用机制值得深入分析：它仅在反馈信号为正（$r > b$）时激活，约束扰动头输出不偏离基础模型太远。这一设计有效防止了 REINFORCE 项在稀疏奖励场景下的过度更新——当模型偶然获得成功反馈时，REINFORCE 项可能过度放大该次决策的权重，而 KL 正则化则起到“信任区域”的作用，保障了适应的稳定性。

### 4.5 投票策略对比

Table 3 对比了维度级投票（dim-wise voting）与动作级投票（action-wise voting）两种策略。维度级投票对动作的每个分量独立进行多数投票，而动作级投票则对整个动作元组投票。在 LIBERO 上，维度级投票在多数任务上表现更优，原因在于它允许不同增强视图在动作的各个分量上达成跨视图共识，更精细地缓解了轨迹过拟合。在 Atari 上，由于动作空间是离散的单一维度，两种策略等价。

![[assets/figures/papers/paper_list_l2422_https_openaccess_thecvf_com_content_CVPR2026_html_Zang_Test_Time_Perturb/figures/009_Table_3.jpg]]
*Table 3: Performance comparison of dim-wise voting and actionwise voting across Atari and LIBERO tasks*

### 4.6 定性分析

Figure 7 展示了 OpenVLA 与 PDF 在三个具体任务上的行为对比。在“Pick up cream cheese”任务中，OpenVLA 反复执行错误的抓取动作（红色拇指标记），而 PDF 在经历短暂探索后迅速锁定正确目标并成功完成操作（绿色拇指标记）。在“Pick up black bowl”任务中，PDF 展现出更强的状态感知能力——当目标物体位置发生变化时，PDF 能够调整抓取策略，而非机械复现记忆中的轨迹。这些可视化证据直接支撑了论文的核心主张：PDF 通过不确定性感知增强与延迟反馈扰动学习，使 VLA 的决策从“轨迹复现”转向“目标导向”。

![[assets/figures/papers/paper_list_l2422_https_openaccess_thecvf_com_content_CVPR2026_html_Zang_Test_Time_Perturb/figures/010_Figure_7.jpg]]
*Figure 7: Visual comparison of OpenVLA and PDF on three tasks. The green thumb indicates that the agent performed the correct action, while the red thumb indicates an incorrect action. The box represents the target entity, with green indicating that the target entity has been operated correctly and red indicating incorrect operation*

### 4.7 失败模式与局限

尽管 PDF 在多数场景下表现优异，但其存在两个明确的局限：

1. **长周期任务的适应滞后**：延迟反馈仅在回合结束后可用，这意味着在 Long 套件等多步任务中，扰动头在整个回合期间无法获得任何指导信号。Table 2 中 PDF 在 Long 套件上仅与基线持平（0.59 vs 0.59），印证了这一局限——当任务步数过长时，基于回合级反馈的适应难以对早期决策产生有效影响。

2. **极端分布偏移下的脆弱性**：PDF 并未从根本上消除轨迹过拟合，只是减轻了其负面影响。在完全未见过的物体属性或极端视觉扰动下，不确定性估计本身可能失效（模型对错误决策也高度自信），此时自适应增强与扰动学习均无法有效介入。

### 4.8 小结

综合来看，PDF 在两个性质迥异的基准上均实现了显著且一致的性能提升，消融实验完整验证了不确定性感知增强、延迟反馈扰动学习以及 KL 正则化三者各自的必要性与协同效应。其 9M 参数的轻量适应机制和无需基础模型梯度的特性，使其在部署效率和实用性上具有明显优势。

### 补充图表

![[assets/figures/papers/paper_list_l2422_https_openaccess_thecvf_com_content_CVPR2026_html_Zang_Test_Time_Perturb/figures/001_Figure_1.jpg]]
*Figure 1: Evidence of trajectory overfitting and the effectiveness of data augmentation. In the first row, the gripper imitates expert trajectories regardless of task success. In the second row, it still reproduces similar actions when the target is masked. The third row shows that the gripper overlooks the target in attention maps. In contrast, after data augmentation, the gripper refocuses on the target and makes correct decisions*

## 方法谱系与知识库定位

**问题定位：轨迹过拟合与测试时适应的困境**

视觉-语言-动作模型（VLAs）在机器人操作中面临一个深层瓶颈——轨迹过拟合（trajectory overfitting）：模型过度依赖动作与实体之间的伪相关性，倾向于复现记忆中的动作序列，而非真正理解语义任务目标。Figure 1 的定性证据揭示了这一现象的严重性：机械臂即使在被遮挡目标的情况下仍模仿专家轨迹，注意力图也忽视了目标物体。这种过拟合导致 VLA 对物体姿态等微小环境变化极为脆弱。

现有的测试时适应（TTA）方法试图缓解这一问题，但多依赖自监督信号（如熵最小化）进行模型更新。Figure 2 揭示了一个关键缺陷：当 VLA 对错误行为过度自信时，熵最小化反而会进一步放大错误的 logits，加剧偏差。此外，前沿的 TTA 方法如 **MG-Select**（Jang et al., Arxiv 2025）虽然无需验证器，但仅通过样本过滤来提升决策质量，缺乏对模型内部决策机制的主动纠正能力。

**方法定位：无验证器的双机制测试时扰动学习**

PDF 在方法谱系中占据一个独特位置——它既不同于需要全参数微调的 VLA 训练方法（如 **OpenVLA-DPO**，Chen et al., Arxiv 2025；**SFT-4LIBERO**，Li et al., Arxiv 2025），也不同于纯自监督的 TTA 范式。PDF 的核心创新在于将测试时适应分解为两个互补机制：

1. **不确定性感知的动作投票**：利用模型自身的预测熵（式 1）动态分配数据增强预算（式 2），通过多增强视图的多数投票打破固定的伪相关模式。这不同于 MG-Select 的被动过滤——PDF 主动扩大观察分布，同时用不确定性作为“节制阀”避免过度增强损害性能（Figure 5 证实增强预算过大会导致性能下降）。

2. **延迟反馈驱动的扰动学习**：引入一个轻量的可学习扰动头（P head），仅 9M 参数，在回合结束后利用延迟反馈（成功/失败或累积奖励）通过 REINFORCE 型损失（式 5）进行更新。这一设计与传统 TTA 形成鲜明对比：PDF 不修改基础模型（视觉编码器、Transformer、LM head 全部冻结），而是通过 logit 层面的扰动修正来纠正过度自信的误判。

**与基线方法的关键差异**

Table 1 的系统对比凸显了 PDF 的方法论优势。在 LIBERO 四个子套件上，PDF 以 0.77 的平均成功率和 2.5 的平均排名超越所有对比方法——包括需要全参数微调的 OpenVLA-DPO 和 SFT-4LIBERO。与同为测试时方法的 MG-Select 相比，PDF 的平均成功率提升近 6 个百分点（0.77 vs 0.71），这一差距主要源于 PDF 的联合机制：不确定性加权投票提供了更鲁棒的候选动作生成，而延迟反馈扰动学习则针对性地纠正了 MG-Select 无法处理的系统性决策偏差。

在 Atari-57 上的跨领域验证进一步确认了 PDF 的泛化能力。以 **Jat**（Gallouédec et al., Arxiv 2024）为基线，PDF 将 Human Normalized Score 从 0.97 提升至 1.07，57 款游戏中 47 款获得正向提升，平均改善幅度达 11.28%（Figure 4）。值得注意的是，PDF 仅使用 9M 可训练参数且无需访问基座模型梯度，而对比基线需要 93–130M 参数的全梯度访问——这体现了 PDF 在计算效率与适应能力之间的独特平衡。

**消融实验揭示的机制重要性**

Table 2 的消融实验为 PDF 的双机制设计提供了因果证据。移除延迟反馈（PDF w/o DF）导致物体操作套件成功率从 0.72 骤降至 0.50，目标导向套件从 0.85 降至 0.77——这证明仅靠数据增强和投票无法解决需要语义理解的决策错误，延迟反馈的监督信号对于纠正伪相关决策不可或缺。

Figure 6 进一步拆解了 PDF 损失函数（式 5）的两个成分：REINFORCE 型策略梯度项和条件 KL 散度正则化项。去除任一成分均导致五个基准上的整体性能退化，其中 KL 正则项的贡献更为显著。这一发现揭示了 PDF 成功的关键：KL 散度约束了扰动头在成功轨迹上的更新幅度，防止过度偏离基础模型的先验知识，从而在纠正错误与保持稳定性之间取得平衡。

**适用边界与局限**

PDF 的设计决定了其适用边界。首先，PDF 并未从根本上消除轨迹过拟合——它通过测试时扰动来减轻其负面影响，但在极端分布偏移或完全未见过的物体属性下，基础模型的表征能力仍然是上限。其次，延迟反馈仅在回合结束后可用，这意味着在长周期任务中存在显著的适应滞后：P head 的更新无法支持每步即时纠正，在需要快速在线适应的场景中可能受限。

此外，PDF 的有效性依赖于两个前提条件：（1）基础 VLA 模型本身具备一定的任务能力，不确定性估计才能提供有意义的信号；（2）环境能够提供明确的回合级反馈信号（成功/失败或累积奖励）。在完全无反馈的开放环境或连续控制问题中，PDF 的延迟反馈机制将无法运作，此时仅剩不确定性投票机制，其有效性有待验证。

**开放问题**

PDF 的提出引出了若干值得探索的方向。最根本的问题是：如何从训练阶段就消除轨迹过拟合，而不是仅依靠测试时扰动来缓解？这可能需要重新审视 VLA 的训练数据构建和表征学习目标。其次，PDF 的自适应扰动思想能否推广到其他多模态基础模型（如视觉-语言模型 VLMs）的推理环节？VLA 的决策不确定性估计和 logit 扰动修正机制在概念上具有通用性，但需要针对不同模态和任务结构进行适配。最后，在延迟反馈不可用的场景中，能否设计替代的监督信号（如基于世界模型的模拟反馈）来驱动 P head 的在线更新，从而扩展 PDF 的适用范围？

## 原文 PDF

![[paperPDFs/CVPR_2026/Test_Time_Perturbation_Tuning_with_Delayed_Feedback_for_Vision_Language_Action_Models.pdf]]
