---
title: "W2W: Language-Model-Based Trajectory Prediction with Reinforcement Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/W2W_Language_Model_Based_Trajectory_Prediction_with_Reinforcement_Learning.pdf
project_link: null
code_link: "https://github.com/VoyagerXu21/W2W"
aliases:
- WWW
- W2W
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 采用两阶段训练范式：第一阶段利用交叉熵进行监督微调以学习输出格式和交互语义，第二阶段使用 PPO 强化学习直接优化组合了 ADE 误差和 off-road 惩罚的任务奖励，从而将优化目标与预测精度和场景可行性对齐。
primary_logic: 通过行为驱动的文本化交互线索和任务级奖励塑造，语言模型可以在保持输出可解析性的同时，直接优化轨迹预测的准确性和场景合规性。
claims:
- 引入交互语义（companion/following/obstacle）后，W2W-SFT 相比无交互的 W2W-Base 在 ETH/UCY 上 ADE 降低 5.4%，FDE 降低 5.6%。
- 相比仅 SFT，增加 RL 阶段后 W2W 进一步降低 ADE/FDE 2.8%/5.3%，并将 off-road 率降低 21.7%。
- SFT 将输出格式执行率（FER）提升至接近 100%，生成稳定的结构化文本以便后续解析。
- 在 ETH/UCY 和 SDD 上，W2W 在 LM-based 方法中取得最佳平均 ADE/FDE，验证了 RL 对齐的有效性。
---

# W2W: Language-Model-Based Trajectory Prediction with Reinforcement Learning

> [!tip] 核心洞察
> 通过行为驱动的文本化交互线索和任务级奖励塑造，语言模型可以在保持输出可解析性的同时，直接优化轨迹预测的准确性和场景合规性。

| 字段 | 内容 |
|------|------|
| 中文题名 | W2W：基于语言模型的轨迹预测与强化学习 |
| 英文题名 | W2W: Language-Model-Based Trajectory Prediction with Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_W2W_Language-Model-Based_Trajectory_Prediction_with_Reinforcement_Learning_CVPR_2026_paper.html) · [Code](https://github.com/VoyagerXu21/W2W) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | W2W (Write-to-Walk) |
| Dataset | ETH-UCY, SDD |

> [!tip] 效果简介
> - ETH-UCY (AVG) 上，ADE/FDE 0.21/0.29 vs LMTraj (best LM-based) (competitive / see Table 3)。
> - SDD 上，ADE/FDE 7.42/10.13 vs LMTraj (best LM-based) (competitive / see Table 3)。

## 概要

轨迹预测是自动驾驶与移动机器人领域的关键任务，要求模型根据观测历史推断未来运动。传统方法将预测建模为回归问题，直接输出坐标序列；近期基于语言模型（LM）的范式则将轨迹文本化，利用预训练语言模型的序列建模能力进行生成。然而，现有 LM-based 方法存在一个核心瓶颈：**监督微调仅优化文本似然，训练目标与轨迹预测的真实评价指标（如 ADE/FDE）及场景合规性之间存在错配**。同时，输入提示中缺乏对社会交互语义的显式编码，限制了语言模型对多行人运动规律的利用。

针对上述问题，本文提出 **W2W（Write-to-Walk）**，一种两阶段训练框架，其核心洞察在于：通过行为驱动的文本化交互线索和任务级奖励塑造，语言模型可以在保持输出可解析性的同时，直接优化轨迹预测的准确性和场景合规性。具体而言，**第一阶段**执行全参数监督微调（SFT），使用交叉熵损失使 T5-Small 学习结构化输出格式和交互语义；**第二阶段**引入基于 PPO 的强化学习对齐，冻结骨干网络、仅更新 LoRA 适配器，直接优化由 ADE 误差和 off-road 惩罚组合而成的任务奖励。这一设计将优化目标从“说得像”切换为“走得对”。

在方法定位上，W2W 属于 LM-based 轨迹预测阵营，与 **LMTraj**、**GUIDE-COT** 等同类方法相比，其关键差异在于：（1）训练目标从纯 SFT 扩展为 SFT+RL 两阶段对齐；（2）交互语义编码从简单坐标/ID 升级为基于距离-航向启发式的 companion/following/obstacle 三类行为标签；（3）场景约束通过二值语义掩码在奖励函数中显式施加 off-road 惩罚，而非仅依赖文本描述。与深度学习基线如 **Social-STGCNN**（Mohamed et al., CVPR 2020）、**Trajectron++**（Salzmann et al., ECCV 2020）、**Social-VAE**（Xu et al., ECCV 2022）和 **AgentFormer**（Yuan et al., ICCV 2021）相比，W2W 以语言模型为骨干，开辟了文本-轨迹联合建模的新路径。

实验结果表明，W2W 在 ETH/UCY 和 SDD 两个标准基准上取得了 LM-based 方法中的最佳平均 ADE/FDE，验证了 RL 对齐的有效性。消融研究进一步揭示：引入交互语义后，W2W-SFT 相比无交互的 W2W-Base 在 ETH/UCY 上 ADE 降低 5.4%、FDE 降低 5.6%（Table 1）；增加 RL 阶段后，W2W 相比仅 SFT 进一步降低 ADE/FDE 2.8%/5.3%，并将 off-road 率降低 21.7%（Table 2）。此外，SFT 将输出格式执行率（FER）提升至接近 100%（Figure 4），确保了后续解析的稳定性。

总体而言，W2W 提供了一种将语言模型的生成能力与任务级奖励对齐的可行方案，为 LM-based 轨迹预测建立了“先学会回答、再学会行走”的训练范式。其局限在于交互分类依赖手工启发式规则，场景约束仅限于静态可行驶区域，尚未在真实平台上验证。这些方向为后续研究留下了明确的改进空间。

轨迹预测是自动驾驶与智能体导航的核心任务，其目标是根据观测历史预测行人的未来位置。现有方法主要分为两类：基于深度学习的回归模型，如 **Social-STGCNN**（Mohamed et al., CVPR 2020）、**Trajectron++**（Salzmann et al., ECCV 2020）、**Social-VAE**（Xu et al., ECCV 2022）和 **AgentFormer**（Yuan et al., ICCV 2021），它们通过精心设计的网络架构来建模时空交互，在 ETH/UCY 和 SDD 等基准上取得了显著进展。然而，这些方法通常需要针对特定场景进行专用设计，泛化能力受限。

近年来，语言模型（LM）的涌现能力为统一轨迹预测提供了新范式。以 **LMTraj** 和 **GUIDE-COT** 为代表的 LM-based 方法将轨迹坐标文本化，借助预训练语言模型进行生成式预测。但这一范式面临两个关键瓶颈：

**目标不匹配**：监督微调（SFT）仅优化 token 级交叉熵损失，即最大化文本似然，而非直接最小化轨迹预测的核心指标——平均位移误差（ADE）和终点位移误差（FDE）。同时，SFT 无法显式施加场景合规性约束，导致预测轨迹可能穿越不可行驶区域。

**交互语义缺失**：现有 LM-based 方法的输入提示仅包含轨迹坐标和行人 ID，未编码行人间的社会交互关系（如结伴、跟随、避障），限制了语言模型对群体运动规律的利用。这从根本上削弱了模型在密集场景中的预测能力。

针对上述缺口，W2W（Write-to-Walk）提出了一种两阶段训练范式：第一阶段通过 SFT 学习结构化输出格式和交互语义，确保生成文本可解析；第二阶段引入基于 PPO 的强化学习，直接优化组合了 ADE 误差和 off-road 惩罚的任务奖励，将优化目标与预测精度和场景可行性对齐。该方法在保持 LM 输出可解析性的同时，实现了对轨迹预测准确性和场景合规性的直接优化。

## 核心方法与创新机理

W2W 的核心创新在于将**语言模型轨迹预测的优化目标与任务指标直接对齐**，并首次在 LM-based 预测框架中显式编码**行为驱动的交互语义**。具体体现为以下三个关键改变：

### 1. 训练目标：从文本似然到任务奖励的对齐

传统 LM-based 方法（如 LMTraj、GUIDE-COT）仅通过监督微调（SFT）优化交叉熵损失，即最大化文本序列的似然：

$$\mathcal{L}_{\mathrm{SFT}} = -\sum_{t} \log p_{\theta}(y_{t} \mid y_{<t}, x)$$

这一目标与轨迹预测的真实评估指标（ADE/FDE）以及场景合规性之间**存在根本性不匹配**：生成格式正确的文本并不等同于预测准确的轨迹。

W2W 引入**两阶段训练范式**来解决这一瓶颈：
- **第一阶段（SFT）**：全参数微调 T5-Small，使用交叉熵损失学习输出格式和交互语义，将格式执行率（FER）提升至接近 100%（Figure 4），确保后续可解析。
- **第二阶段（RL 对齐）**：冻结 T5-Small 骨干，仅更新 LoRA 适配器，利用 PPO 直接优化**组合任务奖励**：

$$r(x, \hat{y}) = r_{\mathrm{L2}} + r_{\mathrm{occ}}$$

其中精度奖励为负平均位移误差 $r_{\mathrm{L2}} = -\lambda_{\mathrm{L2}} \frac{1}{T} \sum_{t=1}^{T} \|\hat{\pmb{\tau}}_{t} - {\pmb{\tau}}_{t}^{\star}\|_{2}$，场景合规奖励为 off-road 惩罚 $r_{\mathrm{occ}} = -\lambda_{\mathrm{occ}} \sum_{t=1}^{T} \mathbf{1}[M_{\mathrm{scene}}(\hat{\pmb{\tau}}_{t}) = 1]$。

这一改变将优化目标从“文本像不像”转变为“轨迹准不准、合不合规”，是 W2W 性能提升的**因果杠杆**。消融实验（Table 2）表明，增加 RL 阶段后 ADE/FDE 进一步降低 2.8%/5.3%，off-road 率降低 21.7%。

### 2. 交互语义编码：从坐标序列到行为类型

现有 LM-based 方法在输入提示中仅编码轨迹坐标和 ID，**未显式利用行人间的社会交互信息**，限制了语言模型对群体运动规律的理解。

W2W 提出**交互感知提示构建**：基于距离/航向启发式方法，将行人间的空间关系分类为三种交互类型：
- **Companion（同行）**：持续接近且航向相似
- **Following（跟随）**：目标跟随前方邻居
- **Obstacle（避障）**：快速接近或静态近距离邻居

这些交互语义被嵌入固定格式的自然语言提示中（Figure 3），使语言模型在生成预测时能显式参考社会关系。消融实验（Table 1）证实，引入交互语义后 W2W-SFT 相比无交互的 W2W-Base 在 ETH/UCY 上 ADE 降低 5.4%，FDE 降低 5.6%。

### 3. 场景约束施加：从文本描述到可微分惩罚

先前工作或忽略场景约束，或仅在提示中加入简单文本描述。W2W 将场景约束**直接嵌入奖励函数**：通过二值语义掩码 $M_{\mathrm{scene}}$ 对预测点落入非可行驶区域施加逐点惩罚 $r_{\mathrm{occ}}$，使 RL 优化过程能直接感知并规避不可行驶区域。值得注意的是，提示消融（Table 4）显示，在输入中额外加入场景描述文本反而降低性能，说明**奖励中的结构化约束比文本描述更有效**。

### 创新总结

| 改变维度 | 基线做法 | W2W 做法 | 效果证据 |
|---------|---------|---------|---------|
| 训练目标 | 仅交叉熵 SFT | SFT + PPO 优化 ADE/off-road 组合奖励 | ADE↓2.8%, FDE↓5.3%, ORR↓21.7% (Table 2) |
| 交互编码 | 仅坐标和 ID | 行为驱动的 companion/following/obstacle 分类 | ADE↓5.4%, FDE↓5.6% (Table 1) |
| 场景约束 | 无或文本描述 | 二值掩码 off-road 惩罚嵌入奖励 | 提示中加入文本描述反而降低性能 (Table 4) |

这些改变共同构成了 W2W 的**核心洞察**：通过行为驱动的文本化交互线索和任务级奖励塑造，语言模型可以在保持输出可解析性的同时，直接优化轨迹预测的准确性和场景合规性。

**需注意的局限性**：交互分类基于手工启发式规则，可能无法捕获复杂社会意图；场景约束仅限于静态可行驶区域掩码，未考虑动态障碍物等现实约束。

W2W 将轨迹预测重新定义为文本生成任务，并通过**两阶段训练**解决语言模型在预测精度与场景合规性上的目标错位问题。整体框架由三个功能模块串联构成：**交互感知提示构建** → **监督微调** → **RL 对齐**，其信息流与训练关系如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2667_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_W2W_Language_Model/figures/002_Figure_2.jpg]]
*Figure 2: Overview of W2W. The framework consists of interaction-aware prompt construction, supervised fine-tuning (SFT), and RL alignment with PPO and LoRA*

### 输入输出流

**输入**：一段观测时长内的多行人轨迹坐标序列。
**输出**：未来预测时长的轨迹坐标序列，以结构化文本形式生成后经解析器还原为数值坐标。

核心转换发生在**交互感知提示构建**阶段：观测轨迹首先被文本化，随后通过基于距离/航向/方位的启发式分类器为每个目标行人标注其与邻居的交互类型——仅保留三种语义类别：**companion**（同行：持续接近且航向相似）、**following**（跟随：目标跟随前方邻居）、**obstacle**（障碍：快速接近或静止的近距离邻居）。这些交互标签与轨迹文本一起填入固定模板，形成自然语言提示，作为语言模型的输入。

### 两阶段训练

**阶段一：监督微调**。以 T5-Small 为骨干，进行全参数端到端微调，损失函数为 token 级交叉熵：

$$
\mathcal{L}_{\mathrm{SFT}} = -\sum_{t} \log p_{\theta}(y_t \mid y_{<t}, x)
$$

该阶段的目标是让模型学会**输出格式**和**交互语义**——即“如何回答”。实验表明，SFT 将输出格式执行率提升至接近 100%，生成稳定可解析的结构化文本。

**阶段二：RL 对齐**。冻结 T5-Small 骨干，仅更新 LoRA 适配器，使用 PPO 直接优化组合了精度与场景合规的任务奖励：

$$
r(x, \hat{y}) = r_{\mathrm{L2}} + r_{\mathrm{occ}}
$$

其中精度奖励为负平均位移误差：

$$
r_{\mathrm{L2}} = -\lambda_{\mathrm{L2}} \frac{1}{T} \sum_{t=1}^{T} \left\| \hat{\boldsymbol{\tau}}_t - \boldsymbol{\tau}_t^{\star} \right\|_2
$$

场景合规奖励对预测点落入非可行驶区域进行累加惩罚：

$$
r_{\mathrm{occ}} = -\lambda_{\mathrm{occ}} \sum_{t=1}^{T} \mathbf{1}[M_{\mathrm{scene}}(\hat{\boldsymbol{\tau}}_t) = 1]
$$

每步奖励进一步引入 KL 惩罚以约束策略偏离参考模型，终态附加上述任务奖励。该阶段让模型学会“如何行走”——在保持输出可解析性的前提下，直接优化预测精度与场景可行性。

### 模块关系与设计逻辑

三个模块形成**串行依赖**：提示构建决定语言模型接收的语义信息量；SFT 为 RL 提供格式稳定、语义合理的初始策略；RL 在 SFT 策略邻域内通过任务奖励进行对齐，弥补监督微调仅优化文本似然而非轨迹预测误差的根本性缺陷。消融实验证实了这一设计的有效性：引入交互语义后 ADE/FDE 分别降低 5.4%/5.6%；增加 RL 阶段后进一步降低 2.8%/5.3%，同时 off-road 率降低 21.7%。

W2W 将多行人轨迹预测重新表述为文本生成任务，其核心由三个模块级联构成，如图 2 所示。

**交互感知提示构建 (Interaction-aware Prompt Construction)。** 该模块将原始轨迹观测转换为结构化的自然语言提示。具体而言，对目标行人与每个邻居，基于距离、航向和方位角的启发式规则将交互关系分类为三种类型：**companion**（持久邻近且航向相似）、**following**（目标跟随前方邻居）和 **obstacle**（快速接近或静态邻近）。分类结果与观测坐标、行人 ID 和场景语义掩码一同填入固定模板（图 3），形成语言模型的输入 $x$。

**监督微调 (Supervised Fine-Tuning, SFT)。** 采用 T5-Small 编码器-解码器架构进行全参数端到端微调，目标是学习稳定的输出格式和交互语义。SFT 使用教师强制下的 token 级交叉熵损失：

$$ \mathcal { L } _ { \mathrm { S F T } } = - \sum _ { t } \log p _ { \theta } ( y _ { t } \mid y _ { < t } , x ) \tag{Eq. 3} $$

其中 $y_t$ 为第 $t$ 个输出 token，$y_{<t}$ 为前缀，$\theta$ 为模型参数。SFT 使输出格式执行率 (FER) 提升至接近 100%（图 4），生成可解析的结构化轨迹文本。

**RL 对齐 (RL Alignment with PPO + LoRA)。** 第二阶段冻结 T5-Small 骨干，仅更新 LoRA 适配器，通过 PPO 直接优化任务奖励。任务奖励由两项组成：

**精度奖励**——负的平均位移误差 (ADE)：

$$ { r } _ { \mathrm { L 2 } } = - \lambda _ { \mathrm { L 2 } } \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \left\| \hat { \pmb { \tau } } _ { t } - { \pmb { \tau } } _ { t } ^ { \star } \right\| _ { 2 } \tag{Eq. 4} $$

其中 $\hat{\pmb{\tau}}_t$ 为预测坐标，$\pmb{\tau}_t^\star$ 为真值，$T$ 为预测步数，$\lambda_{\mathrm{L2}}$ 为权重系数。

**场景合规奖励**——对预测点落入非可行驶区域的惩罚：

$$ r _ { \mathrm { { o c c } } } = - \lambda _ { \mathrm { { o c c } } } \sum _ { t = 1 } ^ { T } \mathbf { 1 } [ M _ { \mathrm { { s c e n e } } } ( \hat { \pmb { \tau } } _ { t } ) = 1 ] \tag{Eq. 5} $$

其中 $M_{\mathrm{scene}}$ 为二值语义掩码（不可行驶区域为 1），$\lambda_{\mathrm{occ}}$ 为惩罚权重。

**组合任务奖励：**

$$ r ( x , \hat { y } ) = r _ { \mathrm { L 2 } } + r _ { \mathrm { o c c } } \tag{Eq. 6} $$

PPO 优化中，每步奖励进一步引入截断 KL 惩罚以约束策略不偏离参考模型过远：

$$ r _ { t } ^ { \mathrm { s t e p } } = - \beta \left[ \mathrm { K L } _ { t } \big ( \pi _ { \theta } \| \pi _ { \mathrm { r e f } } \big ) \right] _ { + } ^ { \delta } + \mathbf { 1 } [ t = T _ { y } ] \, r ( x , \hat { y } ) \tag{Eq. 7} $$

其中 $\pi_\theta$ 为当前策略，$\pi_{\mathrm{ref}}$ 为 SFT 参考策略，$\beta$ 和 $\delta$ 为截断参数，$T_y$ 为输出序列长度。最终通过 clipped PPO 目标更新策略参数。

**因果机制。** SFT 阶段建立了可解析的输出格式和交互语义基础；RL 阶段则通过复合奖励将优化目标从文本似然直接对齐到轨迹精度和场景合规性，这是性能提升的关键因果旋钮。

## 实验与关键发现

### 实验设置与评估协议

W2W 在两个标准轨迹预测基准上评估：**ETH-UCY**（五个子场景：ETH、HOTEL、UNIV、ZARA1、ZARA2）和**SDD**（Stanford Drone Dataset）。ETH-UCY 采用留一法交叉验证，SDD 使用标准 train/val/test 分割。所有实验统一使用观测时长 $T_{\text{obs}}=8$（3.2 秒）和预测时长 $T_{\text{pred}}=12$（4.8 秒）。

主指标为**平均位移误差（ADE）**和**最终位移误差（FDE）**。为评估语言模型输出的可解析性和场景合规性，还引入两个辅助指标：
- **FER (Format Execution Rate)**：生成文本可被成功解析的比例，反映输出格式稳定性；
- **ORR (Off-Road Rate)**：预测点落入非可行驶区域的比例，反映场景合规性。

### 消融实验：交互语义的有效性

Table 1 对比了带交互语义的 **W2W-SFT** 与无交互线索的 **W2W-Base**。两者均仅经过 SFT 阶段，区别在于 W2W-SFT 的提示中包含基于距离/航向启发式分类的三种交互类型（companion/following/obstacle），而 W2W-Base 仅使用轨迹坐标和 ID。

![[assets/figures/papers/paper_list_l2667_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_W2W_Language_Model/figures/005_Table_1.jpg]]
*Table 1: Comparisons between W2W-SFT and W2W-Base, which does not consider interaction cues*

**核心结论**：引入交互语义后，W2W-SFT 在 ETH/UCY 上的平均 ADE 降低 5.4%，FDE 降低 5.6%。这表明，即使在大语言模型内部，显式编码社会交互关系也有助于模型学习行人的运动规律，而非仅依赖坐标序列的统计模式。

### 消融实验：RL 对齐阶段的有效性

Table 2 对比了仅 SFT 的 **W2W-SFT** 与两阶段（SFT + RL）的完整 **W2W**。RL 阶段冻结 T5-Small 骨干，仅更新 LoRA 适配器，使用 PPO 优化组合了精度奖励 $r_{\mathrm{L2}}$ 和 off-road 惩罚 $r_{\mathrm{occ}}$ 的任务奖励。

![[assets/figures/papers/paper_list_l2667_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_W2W_Language_Model/figures/006_Table_2.jpg]]
*Table 2: Comparisons between W2W-SFT and W2W, where W2W uses RL as the second-stage training. ORR↓ and FER↑ are auxiliary metrics for scene compliance and output parsability, respectively*

**核心结论**：
- W2W 相比 W2W-SFT，ADE 进一步降低 2.8%，FDE 降低 5.3%；
- **ORR 大幅降低 21.7%**，证明 RL 阶段通过 off-road 惩罚有效将场景约束注入生成策略；
- FER 在 SFT 阶段已接近 100%（Figure 4），RL 阶段未损害输出可解析性。

这表明两阶段设计的关键因果机制：SFT 负责学习“如何回答”（稳定输出格式和交互语义），RL 负责学习“如何行走”（直接优化预测精度和场景合规性），二者分工明确且互补。

### 主要结果：与深度学习和 LM 基线的对比

Table 3 给出了 ETH-UCY 和 SDD 上的完整对比。基线包括：
- **深度学习基线**：Social-STGCNN (Mohamed et al., CVPR 2020)、Trajectron++ (Salzmann et al., ECCV 2020)、Social-VAE (Xu et al., ECCV 2022)、AgentFormer (Yuan et al., ICCV 2021)；
- **LM 基线**：LMTraj、GUIDE-COT。

**ETH-UCY 结果**：W2W 取得平均 ADE/FDE 0.21/0.29，在 LM 方法中达到最佳，与最强深度学习基线（AgentFormer 和 Social-VAE）相比具有竞争力。

**SDD 结果**：W2W 取得 ADE/FDE 7.42/10.13，同样在 LM 方法中领先。值得注意的是，SDD 包含俯拍视角的行人和车辆，场景复杂度更高，W2W 仍能保持有效预测，说明文本化交互表示具有一定的场景泛化性。

**性能归因**：论文分析指出，改进主要源于：(1) 任务奖励直接将优化目标与 ADE 和场景合规对齐，而非仅优化文本似然；(2) PPO 在 SFT 策略邻域内进行受约束更新，配合 LoRA 低秩适配，防止策略崩溃。

### 输入提示消融：场景描述 vs. 交互语义

Table 4 消融了输入提示的不同组成：
- **W2W-SFT+**：包含场景描述文本 + 无交互语义；
- **W2W-SFT***：无场景描述 + 无交互语义；
- **W2W-SFT**：无场景描述 + 有交互语义。

![[assets/figures/papers/paper_list_l2667_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_W2W_Language_Model/figures/009_Table_4.jpg]]
*Table 4: Comparisons of different input tokens. W2W-SFT+ includes scene-description text in the input; W2W-SFT* excludes it; and W2W-SFT also excludes scene-description text while adding explicit interaction semantics*

**反直觉发现**：加入场景描述文本反而降低性能。W2W-SFT（无场景描述，有交互语义）取得最佳 ADE/FDE 0.21/0.30，而 W2W-SFT+（有场景描述）性能更差。这表明当前的场景文本化方式可能引入噪声或分散模型对关键交互线索的注意力，场景约束更适合通过 RL 阶段的 off-road 掩码奖励间接施加，而非作为文本提示的一部分。

### 奖励权重消融

Figure 5 探索了不同奖励权重设置 $(\lambda_{\mathrm{L2}}, \lambda_{\mathrm{occ}})$ 的影响。**RW-C 设置（以精度项为主导）**取得最佳或接近最佳的 ADE/FDE。这表明精度奖励是主要驱动力，off-road 惩罚作为辅助正则项，过度强调场景合规可能牺牲预测精度。

![[assets/figures/papers/paper_list_l2667_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_W2W_Language_Model/figures/008_Figure_5.jpg]]
*Figure 5: Comparisons of different reward weight settings*

### 可视化分析

Figure 6 展示了有无交互数据的 SFT 预测轨迹对比。黄色区域标出了两种模型预测差异显著的位置，直观展示了交互语义对预测行为的影响——尤其在行人密集或路径交叉的场景中，交互线索帮助模型做出更符合社会规范的预测。

![[assets/figures/papers/paper_list_l2667_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_W2W_Language_Model/figures/011_Figure_6.jpg]]
*Figure 6: Visualization of SFT with interaction data. Red: predicted trajectories; Blue: observed trajectory; Green: ground truth; Yellow: regions/trajectories where predictions differ between models trained with and without interaction data*

Figure 7 对比了 W2W 与 W2W-SFT 的预测轨迹。橙色圆圈标出预测分歧区域，RL 对齐后的预测更贴近真实轨迹（绿色），且在靠近不可行驶区域时表现出更好的场景合规性。

### 局限性与失败模式

1. **交互分类粗糙**：当前仅基于距离/航向启发式区分三种交互类型，无法捕获更复杂的社会意图（如让路、结伴分离等），可能在高密度场景中失效。
2. **场景约束静态**：off-road 惩罚仅基于二值语义掩码，未考虑动态障碍物、交通规则等现实约束，在真实自动驾驶场景中可能不足。
3. **数据集规模有限**：仅在 ETH-UCY 和 SDD 上验证，未在更大规模、更多样化的真实场景中测试，泛化性有待验证。
4. **提示设计的敏感性**：场景描述文本的引入反而降低性能，说明当前提示工程策略存在不稳定性，需要更系统的设计原则。

### 方法谱系与知识库定位

W2W 处于**语言模型驱动的轨迹预测**这一新兴方向，与 LMTraj 和 GUIDE-COT 同属将轨迹预测重新定义为文本生成的范式。其核心创新在于：(1) 首次将 RL 对齐引入 LM 轨迹预测，使优化目标与任务指标直接挂钩；(2) 提出行为驱动的文本化交互线索，将社会交互显式编码为自然语言。相比传统深度学习回归方法（如 Social-STGCNN、Trajectron++、AgentFormer），W2W 利用预训练语言模型的序列建模能力，但通过两阶段训练解决了“文本似然 ≠ 预测精度”的目标不匹配问题。

## 定位与知识库关联

### 1. 与已有工作的关系

**LM-based 轨迹预测谱系。** 将轨迹预测重构为序列生成任务是近年来兴起的方向，代表性工作包括 **LMTraj** 和 **GUIDE-COT**（具体作者/会议在本文中未给出，需手动核实）。这些方法通常采用监督微调（SFT）将轨迹坐标序列化为文本并由语言模型生成，但存在一个核心瓶颈：**优化目标与任务指标不匹配**——SFT 仅最大化文本似然，未能直接最小化 ADE/FDE 等轨迹预测误差，也无法保证场景合规性。

W2W 的关键推进在于**将任务级奖励显式注入训练过程**：在 SFT 习得输出格式和交互语义后，引入基于 PPO 的强化学习阶段，直接优化由 ADE 误差项和 off-road 惩罚项组合而成的程序化奖励（公式 (6)）。这使得语言模型在保持输出可解析性的同时，其优化方向首次与轨迹预测的精度和场景可行性对齐。

**与深度学习方法的对比。** 在 ETH/UCY 和 SDD 基准上，W2W 与经典深度学习基线形成竞争关系：**Social-STGCNN**（Mohamed et al., CVPR 2020）基于图卷积建模社会交互，**Trajectron++**（Salzmann et al., ECCV 2020）采用 CVAE 框架融合异构输入，**Social-VAE**（Xu et al., ECCV 2022）和 **AgentFormer**（Yuan et al., ICCV 2021）分别从变分推断和 Transformer 角度推进了交互建模。W2W 在 LM-based 方法中取得最佳平均 ADE/FDE，验证了 RL 对齐策略的有效性，但与最优深度学习方法的差距仍需关注（详见 Table 3）。

**交互编码的差异化。** 与 LMTraj 等仅将轨迹坐标和 ID 序列化为文本的做法不同，W2W 在输入提示中引入**行为驱动的交互语义**：基于距离/航向启发式分类器将相邻行人标注为 companion、following 或 obstacle 三种类型。这一设计的因果效应在消融实验中得到验证——W2W-SFT 相比无交互的 W2W-Base 在 ETH/UCY 上 ADE 降低 5.4%，FDE 降低 5.6%（Table 1）。

### 2. 适用边界

W2W 的设计决策划定了其适用边界：

- **静态场景约束。** 场景合规性仅通过二值语义掩码在奖励函数中施加 off-road 惩罚，这意味着 W2W 可以处理“行人不应走入建筑物/绿化带”这类静态可行驶区域约束，但**无法处理动态障碍物、交通信号灯、社会规则（如靠右行走）等时变或语义层面的约束**。
- **启发式交互分类。** 交互类型的判定依赖手工设计的距离/航向规则，而非学习得到的交互表征。这使得 W2W 在简单交互场景（并排行走、跟随、避让迎面行人）中表现良好，但在复杂社会行为（如群体决策、意图协商）中可能遗漏关键信息。
- **数据集覆盖。** 当前验证仅限 ETH/UCY 和 SDD 两个标准行人轨迹预测数据集，均为固定俯视视角、相对稀疏的行人场景。在密集人群、车辆-行人混合、或真实自动驾驶感知输入条件下的泛化能力未经检验。

### 3. 局限与开放问题

**已知局限。**
1. 交互分类仅基于简单启发式，可能无法捕获更复杂的社会行为或意图。
2. 场景约束仅限于静态二值可行驶区域掩码，未考虑动态障碍物、交通规则等现实约束。
3. 仅在两个标准数据集上验证，未在真实自动驾驶或机器人平台上部署测试。

**开放问题。**
1. **交互分类能否通过学习获得？** 当前手工启发式可替换为可学习的交互编码器，或利用语言模型自身的注意力机制隐式捕获交互，这有望提升对复杂社会行为的建模能力。
2. **RL 奖励能否扩展到动态约束？** 将速度限制、避碰距离、交通规则等纳入奖励函数，可能使预测轨迹更接近真实人类行为，但需要设计可微或可采样的约束评估器。
3. **场景约束表示能否集成到语言模型内部？** 当前场景信息仅通过奖励函数间接施加，若将场景的向量化表示或文本描述注入提示/模型骨干，可能实现更紧耦合的场景感知预测。
4. **如何扩展到更大规模的真实场景？** 在 nuScenes、Waymo Open Dataset 等自动驾驶基准上验证，是判断该方法能否从行人预测迁移到通用轨迹预测的关键一步。

> **注意：** 上述开放问题中部分方向（如可学习交互分类、动态约束奖励设计）在原文中作为未来工作提及，但其可行性和具体方案尚未经验证，需后续研究确认。

## 原文 PDF

![[paperPDFs/CVPR_2026/W2W_Language_Model_Based_Trajectory_Prediction_with_Reinforcement_Learning.pdf]]
