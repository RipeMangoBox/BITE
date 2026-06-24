---
title: "$AutoDrive\\text{-}P^3$: Unified Chain of Perception–Prediction–Planning Thought via Reinforcement Fine-Tuning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AutoDrivetext_P3_Unified_Chain_of_PerceptionPredictionPlanning_Thought_via_Reinforcement_Fine_Tuning.pdf
aliases:
- AP
- "AutoDrive-P³"
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "核心调控杠杆是提出一种统一的、分阶段监督的强化学习算法（P³-GRPO），该算法通过层次化、渐进式的奖励机制，显式地对感知、预测和规划三个模块进行联合优化，并利用P³-CoT数据集进行冷启动监督微调，从而建立三者之间的因果协同关系。"
primary_logic: "核心洞见在于：自动驾驶的规划性能根本上依赖于准确的感知和可靠的预测，三者必须作为一个统一的链式推理过程进行协同优化，而非独立处理。通过将GRPO从仅优化规划扩展到显式涵盖感知、预测和规划，并设计相应的层次化奖励函数，可以迫使模型在提升感知和预测精度的同时，自然提升规划决策的可靠性和可解释性。"
claims:
- "AutoDrive-P³在nuScenes开放环基准上，详细思考模式实现了0.33 L2(m) Avg.和0.06 Collision (%) Avg.，优于所有基线方法。"
- "AutoDrive-P³在NAVSIMv1封闭环基准上，详细思考模式实现了90.6 PDMS，优于所有基线方法。"
- "P³-GRPO在感知和预测任务上带来了大幅提升，超越了所有基线，并显著提升了规划性能。"
- "去除KL散度项会导致模型性能严重下降并最终崩溃。"
---

# $AutoDrive\text{-}P^3$: Unified Chain of Perception–Prediction–Planning Thought via Reinforcement Fine-Tuning

> [!tip] 核心洞察
> 核心洞见在于：自动驾驶的规划性能根本上依赖于准确的感知和可靠的预测，三者必须作为一个统一的链式推理过程进行协同优化，而非独立处理。通过将GRPO从仅优化规划扩展到显式涵盖感知、预测和规划，并设计相应的层次化奖励函数，可以迫使模型在提升感知和预测精度的同时，自然提升规划决策的可靠性和可解释性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AutoDrive-P³：通过强化微调实现感知-预测-规划统一思维链 |
| 英文题名 | $AutoDrive\text{-}P^3$: Unified Chain of Perception–Prediction–Planning Thought via Reinforcement Fine-Tuning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=CMU8GxwpUL); [GitHub](https://github.com/haha-yuki-haha/AutoDrive-P3); [Project](https://openi.pcl.ac.cn/OpenAIDriving/AutoDrive-P3) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | AutoDrive-P³ |
| Dataset | nuScenes, NAVSIMv1, NAVSIMv2 |

> [!tip] 效果简介
> - nuScenes 上，L2(m) Avg. 为 0.33，对比 0.34 (OmniDrive)，变化 -0.01。
> - nuScenes 上，Collision (%) Avg. 为 0.06，对比 0.21 (OmniDrive)，变化 -0.15。
> - NAVSIMv1 上，PDMS 为 90.6，对比 87.4 (WoTE)，变化 +3.2。

## 概述

AutoDrive-P³（AutoDrive-P³）解决的是基于视觉语言模型（VLM）的端到端自动驾驶中的核心瓶颈：现有方法要么跳过感知与预测直接输出规划，造成严重的领域差距并削弱决策能力；要么将感知、预测、规划作为碎片化独立模块处理，缺乏协同，导致规划性能低下。该工作的核心洞见在于，规划性能根本上依赖于准确的感知和可靠的预测，三者必须作为统一的链式推理过程进行协同优化，而非独立处理。

为此，论文提出了三项关键技术贡献：1）构建P³-CoT数据集，将感知、预测、规划组织成统一的链式推理格式，用于冷启动监督微调（SFT）；2）提出P³-GRPO算法，这是一种层次化、渐进式的强化学习方法，通过多组件奖励函数（格式奖励、感知奖励、预测奖励、规划奖励）显式地对三个模块进行联合优化，而非仅优化规划；3）引入双推理模式（详细思考与快速思考），在性能与效率之间提供灵活权衡。论文使用Qwen2.5-3B作为基础VLM，模型规模和训练数据量（约20k帧）远小于部分基线方法，但取得了更优或相当的性能。

在nuScenes开放环基准上，AutoDrive-P³的详细思考模式实现了0.33 L2(m) Avg.和0.06 Collision (%) Avg.，优于所有基线方法，包括此前最优的OmniDrive（0.34 L2, 0.21 Collision）。在NAVSIMv1封闭环基准上，详细思考模式达到了90.6 PDMS，优于此前最优的WoTE（87.4 PDMS）。消融实验证实，P³-GRPO在感知和预测任务上带来了大幅提升，超越了所有基线，并显著提升了规划性能；去除KL散度项会导致模型性能严重下降并最终崩溃。

## 背景与动机

端到端自动驾驶系统正经历从传统模块化流水线向视觉-语言模型（VLM）范式的转变。然而，现有基于VLM的方法暴露出两个关键瓶颈：其一，部分方法（如EMMA、VLM-AD）直接由感知输入跳至规划输出，跳过了对场景动态演变的显式预测环节，导致模型在未见场景中的决策能力显著下降——这种“感知→规划”的捷径造成了严重的领域差距（domain gap）；其二，另一类方法（如OmniDrive、DriveVLM）虽然能够分别输出感知、预测和规划的答案，但采用碎片化的问答对形式（fragmented Q-A pairs），各模块独立训练和推理，缺乏因果协同，使得预测结果无法有效约束规划决策，最终规划性能低下。

现有强化学习方法（如Plan-R1、AlphaDrive、AutoDrive-R²）仅将GRPO应用于规划模块的优化，感知和预测环节缺乏直接的奖励信号监督，这进一步割裂了三者之间的内在逻辑链条。其核心问题在于：自动驾驶的规划质量根本上取决于对环境的准确感知和对其他交通参与者未来行为的可靠预测，三者必须作为一个统一的链式推理过程进行联合优化，而非独立处理。

AutoDrive-P³的提出正是为了填补这一缺口。其核心调控杠杆是设计一种统一的、分阶段监督的强化学习算法（P³-GRPO），通过层次化、渐进式的奖励机制，显式地对感知、预测和规划三个模块进行联合优化，并辅以P³-CoT数据集进行冷启动监督微调。该方法的根本洞见在于：规划性能的提升不能仅通过优化规划损失来实现，而必须通过建立“感知精度→预测可靠性→规划安全性”的因果传导链，迫使模型在提升前两个环节精度的同时，自然增强最终决策的可解释性和鲁棒性。

## 核心创新

AutoDrive-P³的核心创新在于将自动驾驶的感知、预测与规划三个模块从碎片化、独立优化的模式，转变为一种**统一的、分阶段协同优化的链式推理框架**。这一转变通过三个关键设计实现，直接针对现有基于VLM的端到端自动驾驶系统的根本瓶颈：跳过低层次感知与预测直接输出规划导致的领域差距，以及模块间缺乏协同导致的性能低下。

**1. 统一的链式推理数据（P³-CoT）**：区别于现有方法使用碎片化的问答对分别处理感知、预测和规划任务，AutoDrive-P³构建了P³-CoT数据集。该数据集将三个任务组织成结构化的链式推理格式，强制要求模型的推理过程严格遵循“感知→预测→规划”的顺序，且前一阶段的结果才能用于后续阶段。这建立了三者之间的因果依赖关系，为后续的协同优化提供了数据基础。该数据集从nuScenes和NAVSIM中采样，利用Qwen2.5-VL-72B合成高质量的思考链数据，重点关注对驾驶决策有直接影响的关键对象。

**2. 层次化渐进式强化学习算法（P³-GRPO）**：这是核心的调控杠杆。现有基于GRPO的自动驾驶方法（如Plan-R1、AlphaDrive）仅对规划模块进行优化，而P³-GRPO将GRPO的优化范围显式扩展至感知、预测和规划三个模块，进行**联合优化**。其关键设计是**多组件奖励函数**（公式 `R(q,a) = λ_format·R_format + λ_perc·R_perc + λ_pred·R_pred + λ_plan·R_plan`），具体包括：
*   **感知奖励 (R_perc)**：基于平均IoU、精确率和召回率，衡量目标检测质量。
*   **预测奖励 (R_pred)**：结合行为标签正确性（由IoU加权）和检测质量，评估预测准确性。
*   **规划奖励 (R_plan)**：通过L2距离的指数变换量化轨迹质量。
*   **格式奖励 (R_format)**：确保输出符合结构化格式。

通过层次化的奖励机制，P³-GRPO迫使模型在提升感知和预测精度的同时，自然提升规划性能。消融实验（Table 10）表明，最优权重配置为`1:2:2:5`（格式:感知:预测:规划），过高的规划权重（如`1:1:1:7`）反而会因削弱感知预测的监督而损害最终性能。此外，保留KL散度项对于训练稳定性至关重要，去除它会导致模型崩溃。

**3. 双推理模式**：为平衡性能与效率，框架引入了“详细思考”和“快速思考”两种模式。详细模式生成完整的推理过程，在nuScenes上取得最优性能（L2: 0.33, Collision: 0.06）；快速模式遵循P³-CoT结构但仅输出结果，牺牲少量性能换取更快的推理速度（L2: 0.34, Collision: 0.08）。

**证据强度**：上述核心创新均有明确的实验支撑。P³-GRPO在感知和预测任务上带来了大幅提升，超越了所有基线，并显著提升了规划性能（5.4节消融研究）。在nuScenes开放环基准上，AutoDrive-P³的详细思考模式实现了0.33 L2(m) Avg.和0.06 Collision (%) Avg.，优于所有基线方法（Table 1）。在NAVSIMv1封闭环基准上，其PDMS达到90.6，同样最优（Table 2）。这些结果证明了统一链式推理与联合优化策略的有效性。

## 整体框架

![[assets/figures/papers/iclr26_0001_CMU8GxwpUL_AutoDrivetext-P3_Unified_Chain_of_PerceptionPred/figures/002_Figure_1.jpg]]
*Figure 1: The difference between A u t o D r i v e ${ \cdot } P ^ { 3 }$ and other paradigms. Our method combines an end-to-end training framework with a three-stage collaborative supervision form with VLM*

AutoDrive-P³ 的体系结构围绕一个核心设计理念展开：将自动驾驶的感知、预测与规划组织为统一的链式推理过程，并通过层次化强化学习进行端到端联合优化。其整体流程可概括为三个紧密耦合的模块：P³-CoT 数据集构建、冷启动监督微调（SFT）和 P³-GRPO 强化学习后训练（Figure 2, Figure 4）。

**数据与推理格式层**：系统首先从 nuScenes 和 NAVSIM 等现有数据集中采样，通过规则筛选与人工标注识别关键对象（定义为人类驾驶员会特别关注以防止潜在危险的对象），构建感知标签（边界框）、预测标签（行为动作）和规划标签（自车轨迹与指令）（Figure 3）。随后利用高级 VLM（Qwen2.5-VL-72B）生成结构化的链式推理数据，形成 P³-CoT 数据集。该数据集的核心约束是“前一阶段的结果才能用于下一阶段”，从而显式建模三阶段间的因果依赖关系，而非简单的任务拼接。

**冷启动与能力获取层**：以通用 VLM（Qwen2.5-3B）为基座，使用 P³-CoT 数据集进行监督微调（SFT），采用标准的负对数似然损失 $\mathcal{L}_{\mathrm{SFT}} = -\sum_{t=1}^{T} \log P(y_t | y_{<t}, x)$。此阶段的目标是弥合通用 VLM 与自动驾驶领域之间的差距，使其掌握结构化推理的输出格式和基本的驾驶知识。SFT 后的模型已具备生成感知-预测-规划链式答案的能力，但尚未实现三阶段间的协同优化。

**协同优化与调控层**：核心调控杠杆是提出的 P³-GRPO 算法。该算法将 GRPO（Group Relative Policy Optimization）从仅优化规划扩展到对感知、预测和规划三个模块进行**集体**优化。其关键机制在于层次化、渐进式的奖励函数设计：

$$R(q,a) = \lambda_{\mathrm{format}} \cdot R_{\mathrm{format}} + \lambda_{\mathrm{perc}} \cdot R_{\mathrm{perc}} + \lambda_{\mathrm{pred}} \cdot R_{\mathrm{pred}} + \lambda_{\mathrm{plan}} \cdot R_{\mathrm{plan}}$$

其中，感知奖励 $R_{\mathrm{perc}}$ 基于平均 IoU、精确率（P）和召回率（R）度量检测质量；预测奖励 $R_{\mathrm{pred}}$ 结合行为标签正确性（由 IoU 加权）与检测质量；规划奖励 $R_{\mathrm{plan}}$ 通过 L2 距离的指数变换 $R_{\mathrm{plan}} = 2/(1+e^{\mathrm{clip}(\mathrm{L2},0,L2_{\mathrm{max}})})$ 量化轨迹质量。这种设计迫使模型在提升感知和预测精度的同时，自然提升规划决策的可靠性。实验表明，奖励权重配置 1:2:2:5（格式:感知:预测:规划）在 nuScenes 上取得最佳规划性能（Table 10）。

**推理模式与输出流**：系统支持双推理模式。**详细思考模式**执行完整的感知-预测-规划链式推理，生成可解释的逐步推理过程和结构化输出；**快速思考模式**遵循 P³-CoT 结构但仅输出各模块的最终答案，省略推理过程（Figure 5）。这种设计在可解释性与推理效率之间提供了灵活权衡。

**核心因果机制**：与现有方法的关键区别在于，AutoDrive-P³ 打破了“碎片化决策”的瓶颈。传统 VLM 要么跳过感知/预测直接输出规划（造成领域差距），要么各模块独立运行缺乏协同。P³-GRPO 通过层次化奖励函数将三者的优化目标绑定——提升感知和预测的奖励会直接正向影响总奖励，从而迫使模型建立“准确感知 → 可靠预测 → 安全规划”的因果链。消融实验证实，P³-GRPO 在感知和预测任务上带来了大幅提升，并显著提升了规划性能（Section 5.4）。去除 KL 散度项会导致模型性能严重下降并最终崩溃，表明正则化在维持优化稳定性中的关键作用。

## 核心模块与公式推导

AutoDrive-P³ 的核心在于将感知、预测与规划组织为统一的链式推理过程，并通过分阶段监督的强化学习进行联合优化。其关键模块包括：P³-CoT 数据集、冷启动监督微调（SFT）以及 P³-GRPO 强化学习算法。

### 1. 问题形式化与基础框架

论文将自动驾驶规划问题形式化为给定自车状态 (E)、传感器数据 (S) 和驾驶指令 (C) 条件下的自车轨迹分布自回归分解：

$$P(\text{Traj} | E, S, C) = \prod_{t=0}^{T} P((x_t, y_t) | E, S, C, (x_0, y_0), \ldots, (x_{t-1}, y_{t-1}))$$

其中 $(x_t, y_t)$ 表示 t 时刻的轨迹点坐标。该分解为后续的链式推理提供了基础。

### 2. P³-CoT 数据集与冷启动

**P³-CoT 数据集** 是驱动整个框架的关键数据基础。其构建流程（图 3）为：从现有数据集（如 nuScenes, NAVSIM）采样，通过规则和人工筛选标注每帧中的“关键对象”（即人类驾驶员会特别关注以避免危险的对象），然后利用高级 VLM（Qwen2.5-VL-72B）生成统一的感知-预测-规划链式推理数据。该过程强制遵循因果链条：**只有前一阶段的结果才能用于下一阶段**，以建模模块间的连接。

**冷启动监督微调（SFT）** 使用 P³-CoT 数据集对基础 VLM 进行微调，使其获得自动驾驶领域知识和结构化推理能力。其损失函数为标准负对数似然：

$$\mathcal{L}_{\mathrm{SFT}} = -\sum_{t=1}^{T} \log P(y_t | y_{<t}, x)$$

其中 $x$ 是输入（图像+指令），$y_t$ 是目标序列的第 t 个 token。

### 3. P³-GRPO 强化学习算法

P³-GRPO 是论文的核心调控杠杆，它将 GRPO 算法从仅优化规划扩展到对感知、预测和规划三个模块进行联合优化。该算法基于 GRPO 框架，其基础目标函数为：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{q,\{o_i\} \sim \pi_{\theta_{\mathrm{old}}}(O|q)} \left[ \frac{1}{G} \sum_{i=1}^{G} \left( \mathcal{I}_i^R - \beta D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}}) \right) \right]$$

其中，$q$ 是问题，$o_i$ 是第 i 个响应，$G$ 是组大小，$\beta$ 是 KL 惩罚系数。$\mathcal{I}_i^R$ 是裁剪替代损失项：

$$\mathcal{I}_i^R = \min\left( \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{\mathrm{old}}}(o_i|q)} A_i, \ \mathrm{clip}\left( \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{\mathrm{old}}}(o_i|q)}, 1-\epsilon, 1+\epsilon \right) A_i \right)$$

其中优势 $A_i$ 通过组内归一化计算：$\hat{A}_{i,t} = \frac{R_i - \mathrm{mean}(\{R_j\}_{j=1}^{G})}{\mathrm{std}(\{R_j\}_{j=1}^{G})}$。

P³-GRPO 的关键创新在于其**多组件奖励函数**，该函数显式地对三个模块进行监督：

$$R(q,a) = \lambda_{\mathrm{format}} \cdot R_{\mathrm{format}} + \lambda_{\mathrm{perc}} \cdot R_{\mathrm{perc}} + \lambda_{\mathrm{pred}} \cdot R_{\mathrm{pred}} + \lambda_{\mathrm{plan}} \cdot R_{\mathrm{plan}}$$

各奖励函数设计如下：

*   **格式奖励 $R_{\mathrm{format}}$**：确保模型输出遵循预定义的 P³-CoT 结构化格式。
*   **感知奖励 $R_{\mathrm{perc}}$**：衡量目标检测质量，基于平均 IoU、精确率 (P) 和召回率 (R)：

    $$R_{\mathrm{perc}} = \left\{ \begin{array}{ll} 1.0, & \mathrm{if~}|\mathcal{B}_{\mathrm{gt}}|=0\mathrm{~and~}|\mathcal{B}_{\mathrm{pred}}|=0, \\ \mathrm{IoU}_{\mathrm{avg}} \cdot (0.5P+0.5R), & \mathrm{if~}|\mathcal{B}_{\mathrm{gt}}|>0\mathrm{~and~}|\mathcal{B}_{\mathrm{pred}}|>0, \\ 0.0, & \mathrm{otherwise}. \end{array} \right.$$

    其中 $\mathcal{B}_{\mathrm{gt}}$ 和 $\mathcal{B}_{\mathrm{pred}}$ 分别是真实和预测的边界框集合。

*   **预测奖励 $R_{\mathrm{pred}}$**：结合行为标签正确性（由 IoU 加权）和检测质量：

    $$R_{\mathrm{pred}} = \left( \frac{\sum_{(i,j)\in\mathcal{M}} \mathrm{IoU}_{ij} \cdot \mathbb{I}(s_i=s_j)}{\sum_{(i,j)\in\mathcal{M}} \mathrm{IoU}_{ij}} \right) \cdot \left( \mathrm{IoU}_{\mathrm{avg}} \cdot (0.5P+0.5R) \right)$$

    其中 $\mathcal{M}$ 是预测与真实对象的匹配集合，$s_i$ 是行为标签。

*   **规划奖励 $R_{\mathrm{plan}}$**：通过 L2 距离的指数变换量化轨迹质量：

    $$R_{\mathrm{plan}} = \frac{2}{1+e^{\mathrm{clip}(\mathrm{L2},0,L2_{\mathrm{max}})}}$$

    该函数将 L2 距离映射到 (1, 2] 区间，距离越小奖励越高，且对较大误差的惩罚呈指数级增长。

### 4. 奖励权重与 KL 散度的关键作用

消融实验（表 10）表明，奖励权重配置为 $\lambda_{\mathrm{format}}:\lambda_{\mathrm{perc}}:\lambda_{\mathrm{pred}}:\lambda_{\mathrm{plan}} = 1:2:2:5$ 时，在 nuScenes 上取得最佳规划性能（Avg. L2 0.33）。更重要的是，去除 KL 散度项 ($\beta D_{\mathrm{KL}}$) 会导致模型性能严重下降并最终崩溃（图 10），这验证了 KL 正则化在防止策略偏离参考模型过远方面的关键作用。

## 实验与分析

### 主结果：开放环与封闭环基准上的规划性能

AutoDrive-P³ 在 nuScenes 开放环基准和 NAVSIMv1/v2 封闭环基准上均取得了最先进的规划性能，验证了统一链式推理与联合强化学习的有效性。

**nuScenes 开放环基准 (Table 1)**：在详细思考模式下，AutoDrive-P³ 实现了平均 L2 误差 0.33 米和平均碰撞率 0.06%，全面超越了所有基线方法。相比最强的 VLM 基线 OmniDrive（L2: 0.34, 碰撞率: 0.21%），碰撞率降低了 71%，表明对感知和预测的联合优化直接提升了规划安全性。值得注意的是，AutoDrive-P³ 使用的 Qwen2.5-3B 模型规模远小于 OmniDrive 的 LLava-7B，且训练数据量仅为约 20k 帧（对比 OmniDrive 的 1000k 样本），体现了更高的样本效率。快速思考模式（L2: 0.34, 碰撞率: 0.08%）性能略低于详细思考模式，但推理延迟更低，为实际部署提供了效率-性能权衡选项。

![[assets/figures/papers/iclr26_0001_CMU8GxwpUL_AutoDrivetext-P3_Unified_Chain_of_PerceptionPred/figures/006_Table_1.jpg]]
*Table 1: Performance comparison on nuScenes Benchmark*

**NAVSIMv1/v2 封闭环基准 (Table 2, Table 3)**：AutoDrive-P³ 在 NAVSIMv1 上达到 90.6 PDMS，在 NAVSIMv2 上达到 89.9 EPDMS，均超越所有基线。在 NAVSIMv1 上，相比基于 BEV 世界模型的 WoTE（87.4 PDMS）和基于扩散模型的 DiffusionDrive（89.2 PDMS），分别提升了 3.2 和 1.4 个点。这一结果在封闭环设置中更具说服力，因为 PDMS/EPDMS 复合指标综合评估了导航合规性、驾驶能力、舒适性和安全性，反映了模型在模拟交互中的真实决策质量。需要手动验证的是，NAVSIM 基准的封闭环模拟器是否完全公平地评估了所有方法，特别是 VLM 方法的推理延迟是否被纳入评估。

![[assets/figures/papers/iclr26_0001_CMU8GxwpUL_AutoDrivetext-P3_Unified_Chain_of_PerceptionPred/figures/007_Table_2.jpg]]
*Table 2: Performance comparison on NAVSIMv1 benchmark*

![[assets/figures/papers/iclr26_0001_CMU8GxwpUL_AutoDrivetext-P3_Unified_Chain_of_PerceptionPred/figures/008_Table_3.jpg]]
*Table 3: Performance comparison on NAVSIMv2 benchmark*

### 消融研究：P³-GRPO 与训练策略的贡献

消融实验 (Table 4, Table 5) 揭示了各组件对最终性能的因果贡献，核心结论如下：

![[assets/figures/papers/iclr26_0001_CMU8GxwpUL_AutoDrivetext-P3_Unified_Chain_of_PerceptionPred/figures/009_Table_4.jpg]]
*Table 4: Ablation study on AutoDrive-P 3 on nuScenes Benchmark*

![[assets/figures/papers/iclr26_0001_CMU8GxwpUL_AutoDrivetext-P3_Unified_Chain_of_PerceptionPred/figures/010_Table_5.jpg]]
*Table 5: Ablation study on different training setting on nuScenes benchmark*

1.  **P³-GRPO 是性能提升的核心杠杆**：在 nuScenes 上，仅进行冷启动 SFT 后，模型平均 L2 为 0.37，碰撞率 0.14%。应用 P³-GRPO 后，L2 降至 0.33（-10.8%），碰撞率降至 0.06（-57.1%）。更重要的是，P³-GRPO 同时大幅提升了感知和预测性能（Table 4 中感知和预测指标超越所有基线），这直接证明了论文的核心洞察：规划性能的提升源于对感知和预测的显式、联合优化。没有 P³-GRPO，即使有 SFT，感知和预测的准确性也无法得到有效监督。

2.  **冷启动 SFT 是必要的初始化步骤**：如果跳过 SFT 直接进行 P³-GRPO，模型性能严重退化（L2 0.42, 碰撞率 0.19%）。这是因为基础 VLM 缺乏自动驾驶领域的结构化知识和 P³-CoT 的推理格式，GRPO 在随机初始化策略上难以有效探索。SFT 为 GRPO 提供了合理的起始策略分布。

3.  **KL 散度正则化是训练稳定性的必要条件**：去除 KL 散度项后，模型在训练过程中性能持续下降，最终导致模型崩溃 (Figure 10)。这验证了 GRPO 目标函数中 KL 惩罚项（$\beta D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}})$）对防止策略更新过大的关键作用，尤其是在奖励信号稀疏或噪声较大的自动驾驶任务中。

4.  **奖励权重配置影响性能平衡**：Table 10 显示，奖励权重比例 $\lambda_{\mathrm{format}}:\lambda_{\mathrm{perc}}:\lambda_{\mathrm{pred}}:\lambda_{\mathrm{plan}} = 1:2:2:5$ 在 nuScenes 上取得了最佳规划性能（Avg. L2 0.33）。将规划权重从 5 增加到 7（1:1:1:7）反而导致规划性能下降（L2 0.34），说明过度强调规划奖励可能破坏感知和预测的学习，进而间接损害规划。这证实了三阶段之间的因果链关系：规划依赖于感知和预测，不能独立优化。

### 推理模式与效率

Figure 5 展示了双推理模式在 nuScenes 上的运行时间。详细思考模式由于生成完整的链式推理过程，延迟较高；快速思考模式仅输出最终答案，延迟显著降低。性能差距（L2: 0.33 vs 0.34, Collision: 0.06 vs 0.08）表明，完整的推理过程确实有助于提升决策质量，但快速模式仍优于大多数基线，为实际应用提供了可行的低延迟选项。

### 失败模式与局限性

尽管取得了 SOTA 性能，AutoDrive-P³ 仍存在以下可识别的失败模式：
- **推理幻觉**：论文明确指出推理过程中存在幻觉现象，例如模型可能错误地识别或描述不存在的物体，这在高动态或遮挡场景中尤为突出。
- **奖励权重的手工设计**：当前的奖励权重（1:2:2:5）是在 nuScenes 上手动调优得到的，其跨数据集（如 NAVSIM）的泛化性和最优性需要手动验证。Table 10 的消融表明权重敏感，但缺乏自适应机制。
- **场景多样性限制**：P³-CoT 数据集仅基于 nuScenes 和 NAVSIM，其场景分布（如 Figure 7, Figure 8 所示的目标类别和动作分布）可能无法覆盖长尾驾驶场景（如极端天气、非常规交通参与者），限制了模型在更广泛环境中的泛化能力。
- **多模态融合缺失**：当前方法仅依赖视觉输入，未利用激光雷达、雷达等传感器，这在高光照变化或恶劣天气条件下可能成为鲁棒性瓶颈。

## 方法谱系与知识库定位

AutoDrive-P³ 的定位是 VLM 端到端自动驾驶中“链式推理”范式的代表，其核心贡献在于将此前被割裂的感知、预测、规划三个阶段，通过统一的强化学习框架进行联合优化。要理解其位置与边界，需将其置于两条并行的发展脉络中：一是端到端自动驾驶方法本身的技术演进，二是 VLM 在该领域的应用深化。

**与基线方法的关系：从碎片化到链式协同**

此前端到端自动驾驶方法可大致分为两类。第一类以 UniAD、ST-P3、VAD 为代表，它们虽然也包含感知、预测、规划模块，但各模块独立训练或使用不同的损失函数，缺乏模块间的因果协同。第二类是直接基于 VLM 的方法，如 OmniDrive、DriveVLM、EMMA、VLM-AD 等，其中一部分直接输出规划结果，跳过了感知和预测的中间推理；另一部分虽然能生成分阶段的答案，但采用碎片化的问答对，各阶段仍被当作独立任务处理。AutoDrive-P³ 针对这两个瓶颈，提出了两个关键改变：一是构建了 P³-CoT 数据集，将感知、预测、规划组织成统一的链式推理格式，用于冷启动监督微调；二是提出了 P³-GRPO 算法，通过层次化、渐进式的奖励机制，显式地对三个模块进行联合强化学习优化。

与同属 GRPO 路线的 Plan-R1、AlphaDrive、AutoDrive-R² 相比，AutoDrive-P³ 的关键差异在于奖励函数的覆盖范围——后者仅对规划模块进行 GRPO 优化，而 P³-GRPO 将奖励信号扩展到了感知和预测阶段。从消融实验（Table 4）来看，这种扩展带来了显著收益：P³-GRPO 在感知和预测任务上大幅超越所有基线，并显著提升了规划性能。与基于扩散模型的 DiffusionDrive 和基于 BEV 世界模型的 WoTE 相比，AutoDrive-P³ 在封闭环基准 NAVSIMv1/v2 上取得了更高性能（PDMS 90.6 vs. 87.4，EPDMS 89.9 vs. 86.2），且使用的是纯视觉输入和更小的模型（Qwen2.5-3B）。

**适用边界与条件**

AutoDrive-P³ 的适用性受制于几个前提条件。首先，该方法依赖高质量的链式推理数据进行冷启动，而 P³-CoT 数据集目前仅基于 nuScenes 和 NAVSIM 构建，每帧关键对象数平均不到 2 个（nuScenes 0.97，NAVSIM 2.08），场景多样性和规模有限。其次，P³-GRPO 的奖励权重（1:2:2:5）是在特定数据集上手工调优的，Table 10 显示不同权重配置对最终性能有显著影响（如权重 1:1:1:7 导致 Avg. L2 从 0.33 退化为 0.34），这意味着该方法在新场景中可能需要重新进行权重搜索。第三，系统目前主要依赖视觉输入，未充分利用激光雷达、雷达等其他传感器模态，在恶劣天气或光照不足条件下的鲁棒性存疑。

**局限与失败模式**

论文自身指出了几个关键局限。推理过程中的幻觉现象仍需进一步缓解——这在 VLM 生成结构化输出时尤为突出，错误的目标检测或行为预测会级联影响后续规划。推理时间仍有减少空间，特别是详细思考模式需要生成完整的推理步骤，这在实时性要求高的场景中可能成为瓶颈。更重要的是，当前实验均在开环（nuScenes）或模拟封闭环（NAVSIM）中进行，尚未在具有真实世界交互的封闭环设置中部署，这意味着方法在面对真实驾驶中的长尾事件、对手方策略变化等动态交互时，其行为尚未被验证。

去除 KL 散度正则化会导致模型性能严重下降并最终崩溃（Figure 10），这揭示了 P³-GRPO 的一个脆弱性：强化学习优化过程中，模型容易偏离参考策略，而 KL 项是维持训练稳定的关键。此外，双推理模式（详细思考 vs. 快速思考）的性能差异（nuScenes 上 L2: 0.33 vs. 0.34, Collision: 0.06 vs. 0.08）表明，推理深度与规划质量之间存在正相关，但这也意味着在效率与性能之间需要做出权衡。

**开放问题**

几个关键问题尚未解决。P³-GRPO 的奖励权重设计是否可以在不同数据集和场景中自适应调整？当前的手工调优方式限制了方法的通用性。如何有效融合多模态传感器数据以提升感知鲁棒性？该方法是否可以扩展到更复杂的驾驶任务，如多车协同或路径规划？最后，如何将系统部署到具有真实世界交互的封闭环设置中，并验证其在长尾事件和对手方策略变化下的行为可靠性？这些问题的回答将决定 AutoDrive-P³ 能否从基准测试的领先者转变为实际部署的可行方案。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/AutoDrivetext_P3_Unified_Chain_of_PerceptionPredictionPlanning_Thought_via_Reinforcement_Fine_Tuning.pdf

![[paperPDFs/ICLR_2026/AutoDrivetext_P3_Unified_Chain_of_PerceptionPredictionPlanning_Thought_via_Reinforcement_Fine_Tuning.pdf]]
