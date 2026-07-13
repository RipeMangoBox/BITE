---
title: "Veritas: Generalizable Deepfake Detection via Pattern-Aware Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Veritas_Generalizable_Deepfake_Detection_via_Pattern_Aware_Reasoning.pdf
project_link: null
code_link: https://github.com/EricTan7/Veritas
openreview_forum_id: 5VXJPS1HoM
aliases:
- Veritas
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "模式感知奖励机制与两阶段训练（冷启动 SFT+MiPO 与 P-GRPO 探索）驱动多模态大语言模型内化人类取证思维模式（规划、自我反思），从而提升对未见伪造的泛化能力。"
primary_logic: "将人类分级取证思维（快速判断、规划、推理、自我反思）显式注入 MLLM，并通过模式感知的强化学习策略，实现端到端的透明且鲁棒的深度伪造检测。"
claims:
- "模式感知推理在跨伪造（CF）和跨域（CD）测试上分别比灵活推理带来 6.2% 和 3.3% 的增益。"
- "VERITAS 在四个评估场景上均达到SOTA，相比之前最佳方法平均提升 6.0%。"
- "在 P-GRPO 前应用 MiPO 可在 CF 和 CD 上分别带来 2.9% 和 2.1% 的增益。"
- "HydraFake Cross-Domain (CD) subset 上 Avg. Accuracy = 82.2"
---

# Veritas: Generalizable Deepfake Detection via Pattern-Aware Reasoning

> [!tip] 核心洞察
> 将人类分级取证思维（快速判断、规划、推理、自我反思）显式注入 MLLM，并通过模式感知的强化学习策略，实现端到端的透明且鲁棒的深度伪造检测。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Veritas：基于模式感知推理的可泛化深度伪造检测 |
| 英文题名 | Veritas: Generalizable Deepfake Detection via Pattern-Aware Reasoning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=5VXJPS1HoM) · [GitHub](https://github.com/EricTan7/Veritas) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | VERITAS |
| Dataset | HydraFake Cross-Domain (CD) subset, HydraFake In-Domain (ID) subset, HydraFake 四个评估场景平均 |

> [!tip] 效果简介
> - HydraFake Cross-Domain (CD) subset 上，Avg. Accuracy 为 82.2，对比 72.8 (Gemini-2.5-Pro)，变化 +9.4%。
> - HydraFake In-Domain (ID) subset 上，Avg. Accuracy 为 97.3，对比 94.7 (Effort)，变化 +2.6%。
> - HydraFake 四个评估场景平均 上，Accuracy gain over previous best 为 AVG提升 6.0%，对比 previous best (small vision models, e.g., Effort/Co-SPY)，变化 +6.0%。

## 概要

深度伪造检测领域面临一个关键瓶颈：现有检测器在跨模型（Cross-Model）场景下泛化良好，但一旦面对**跨伪造类型（Cross-Forgery）**和**跨数据域（Cross-Domain）**的未见伪造，性能便大幅下降。更严重的是，多数方法仅输出二分类标签，缺乏透明、可信的推理过程，难以在取证场景中建立用户信任。

针对这一困境，VERITAS 提出了一种**模式感知推理框架**，将人类取证思维模式显式注入多模态大语言模型（MLLM）。其核心思路是：让模型像人类专家一样，经历“快速判断→规划→推理→自我反思→结论”的分级思维链条，并通过专门设计的强化学习策略驱动模型内化这一过程，从而实现端到端的透明且鲁棒的深度伪造检测。

在方法定位上，VERITAS 不同于传统小型视觉模型（如 **F3Net**（Qian et al., ECCV 2020）、**NPR**（Tan et al., CVPR 2024）、**Effort**（Yan et al., ICML 2025）等）依赖隐式特征判别，也超越了现有 MLLM 检测器（如 **FakeShield**、**FFAA**）仅做简单链式推理的做法。它通过**两阶段训练管道**——模式引导冷启动（SFT + MiPO）与模式感知探索（P-GRPO）——将推理质量与检测准确性统一优化，在 HydraFake 基准的四个评估场景上均达到 SOTA，相比此前最佳方法平均提升 **6.0%**。尤其在跨伪造类型和跨域场景下，模式感知推理相比灵活推理分别带来 **6.2%** 和 **3.3%** 的增益，验证了结构化思维模式对泛化能力的关键作用。

深度伪造生成技术的快速迭代使得合成图像在视觉质量与多样性上持续突破，从早期的面部交换、属性编辑扩展到人脸重光照、个性化生成与生成式换脸等新范式。这一趋势对检测器提出了严苛的泛化要求：模型不仅要应对训练中未见过的生成模型（跨模型泛化），更需在完全不同的伪造类型（跨伪造泛化）与数据域（跨域泛化）下保持可靠。

然而，现有检测器在这三层泛化挑战上呈现显著的性能分化。如 Figure 2 (d) 所示，大多数方法在跨模型场景下表现良好，但在跨伪造和跨域场景下性能急剧下降。深层瓶颈在于：**仅依赖统计特征匹配的小型视觉模型难以捕获伪造本质的因果线索，而通用多模态大语言模型虽具备推理能力，却缺乏面向深度伪造检测的结构化取证思维**。具体而言，通用 MLLM（如 Qwen2.5-VL-7B、InternVL3-8B）在 HydraFake 基准上的平均准确率仅约 51.2%，远低于专用小型模型（如 Effort 的 94.7%），暴露出其对伪造痕迹感知与逻辑推理的双重不足。

此外，现有 MLLM 检测器（如 FakeShield、M2F2-Det）普遍采用“先回答后解释”或简单链式思维，缺乏人类取证中“快速判断—规划—推理—自我反思”的分级认知结构。这导致两个关键缺陷：一是推理过程不透明，无法为决策提供可信依据；二是面对未见伪造时，模型倾向于记忆表面模式而非内化可迁移的推理策略。

上述缺口共同指向一个核心问题：**如何将人类取证思维模式显式注入 MLLM，使其在保持端到端可微训练的同时，习得透明、鲁棒且可泛化的深度伪造检测能力？** 本文正是围绕这一动机，提出模式感知推理框架 VERITAS，通过两阶段训练管道（模式引导冷启动与模式感知强化学习探索）驱动模型内化规划与自我反思能力，从而在跨伪造与跨域场景下实现显著泛化增益。

## 核心方法与创新机理

VERITAS 的核心创新在于将人类的**分级取证思维模式**显式注入多模态大语言模型（MLLM），并通过**模式感知的强化学习策略**驱动模型内化规划与自我反思能力，从而在跨伪造类型和跨数据域的极端场景下实现鲁棒且透明的深度伪造检测。

### 瓶颈突破：从“黑箱分类”到“透明推理”

现有深度伪造检测器面临两个结构性困境：其一，小型视觉模型在跨模型场景下泛化良好，但在跨伪造类型（Cross-Forgery）和跨数据域（Cross-Domain）场景下性能断崖式下降（图 2d）；其二，基于 MLLM 的检测器虽能提供文本解释，但其推理过程缺乏结构化引导，容易产生表面化、不可信的判断。VERITAS 的关键洞察在于：**将人类专家的分层取证思维——快速判断、区域规划、证据推理、自我反思——固化为可训练的思维模式，使模型从“猜测答案”转向“构建证据链”**。

### 方法创新：三个关键变更槽

相较于基线方法，VERITAS 在三个维度上实现了结构性变更：

**1. 推理策略：从灵活链式思维到五阶段模式感知推理**

现有 MLLM 检测器通常采用无约束的链式思维（Chain-of-Thought）或仅输出最终判断。VERITAS 引入五种显式思维模式标签：`<fast>`（快速判断）、`<planning>`（区域规划）、`<reasoning>`（证据推理）、`<reflection>`（自我反思）、`<conclusion>`（结论合成）。消融实验（Table 2）表明，这种模式感知推理在跨伪造和跨域测试上分别比灵活推理带来 **6.2%** 和 **3.3%** 的绝对精度增益，证明结构化思维模式对分布外泛化具有因果性贡献。

**2. 训练管道：从单阶段微调到两阶段“冷启动-探索”范式**

传统方法依赖单一阶段 SFT 或直接强化学习，容易导致推理模式退化或探索不足。VERITAS 设计了两阶段训练管道（图 3）：
- **模式引导冷启动**（Pattern-Guided Cold-Start）：先通过 SFT 注入五种思维模式格式（公式 1），再通过混合偏好优化 MiPO（公式 2）利用“非偏好数据”对齐推理质量——即让模型学习区分精确推理与表面推理。
- **模式感知探索**（Pattern-Aware Exploration）：在冷启动基础上，通过 P-GRPO 驱动模型自适应地选择是否进行规划与自我反思。

消融实验（图 4）证实，在 P-GRPO 前应用 MiPO 可在跨伪造和跨域上分别带来 **2.9%** 和 **2.1%** 的额外增益，验证了两阶段设计的必要性。

**3. 强化学习奖励设计：从纯准确率奖励到模式感知复合奖励**

传统 RL 仅以答案正确性作为奖励信号，无法区分“蒙对”与“真懂”。VERITAS 的模式感知奖励（公式 5）根据答案正确性（$\mathcal{C}$）与是否包含规划（$\mathcal{P}$）或自我反思（$\mathcal{R}$）模式进行差异化赋分：正确答案且包含规划/反思得最高奖励（2.0），正确答案但无结构化推理得基础奖励（1.0），错误答案则根据推理行为给予梯度惩罚。最终奖励（公式 6）进一步融合反思质量奖励 $R_{\mathrm{ref}}$ 和格式奖励 $R_{\mathrm{fmt}}$。消融实验（Table 3）显示，模式感知奖励在跨伪造和跨域场景下显著优于纯准确率奖励，证明奖励设计直接塑造了模型的泛化推理行为。

### 创新本质：从“数据驱动”到“认知模式驱动”

VERITAS 的创新并非简单的模块堆叠，而是通过**将人类认知模式编码为可优化的训练信号**，实现了三个层面的统一：SFT 注入思维结构，MiPO 对齐推理质量，P-GRPO 激励自适应探索。这种设计使得模型在 HydraFake 四个评估场景上平均超越此前最佳方法 **6.0%**（Table 1），尤其在跨域场景下比闭源模型 Gemini-2.5-Pro 高出 **9.4%**，验证了“模式感知推理”作为泛化能力的因果杠杆的有效性。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_5VXJPS1HoM/figures/016_Figure_9.jpg]]
*Figure 9: Construction pipeline of Pattern-Aware SFT data. (a) We first inspect a subset and summarize the artifacts into three clusters. (b) Then we introduce a multi-step strategy to generate pattern-aware reasoning data. (c) Annotated examples. The reasoning process evolves in complexity and depth (as highlighted in red), culminating in a final answer through synthesis of all evidence*

VERITAS 的核心是一个两阶段训练管道，旨在将多模态大语言模型（MLLM）的能力通过**模式感知推理**锚定到深度伪造检测任务上。该框架的关键瓶颈在于：现有检测器在跨伪造类型（CF）和跨数据域（CD）场景下泛化性能骤降，且缺乏透明可信的推理过程。VERITAS 的因果调节变量是**模式感知奖励机制与两阶段训练**，驱动模型内化人类取证思维模式（规划、自我反思），从而提升对未见伪造的泛化能力。

整体管道如 Figure 3 所示，分为两个阶段：

1. **模式引导冷启动**：首先通过监督微调将五种结构化思维模式注入模型，随后引入混合偏好优化策略对齐推理质量。
2. **模式感知探索**：通过群组相对策略优化与模式感知奖励，激励模型自适应地进行规划与自我反思，最终输出端到端的透明决策。

输入为单张待检测图像，输出为包含 `<fast>`、`<planning>`、`<reasoning>`、`<reflection>`、`<conclusion>` 五种模式标签的结构化推理链及最终真伪判断。

### 阶段一：模式引导冷启动

该阶段包含两个步骤，分别解决 MLLM 在深度伪造检测中的两个固有问题：一是缺乏对细微伪造痕迹的感知能力，二是推理过程与人类专家思维模式不一致。

**SFT 模式注入**：为缓解 MLLM 难以检测细微伪影的问题，VERITAS 构建了一个多步标注管道。首先人工检查子集并归纳出三类伪影：可感知的结构异常、细微的低层伪影、违反物理规律的认知错误。随后将标注解耦为三个专门且连贯的步骤，生成带有五种思维模式标签的推理数据。SFT 损失函数为：

$$\mathcal { L } _ { 1 } = - \mathbb { E } _ { ( \pmb { q } , \pmb { s } ) \sim \mathcal { D } _ { 1 } } \sum _ { t = 1 } ^ { T } \log \pi _ { \theta } \big ( \pmb { s } _ { t } \mid \pmb { q } , \pmb { s } _ { < t } \big )$$

该阶段使模型初步掌握五种思维模式的格式与基本推理逻辑。

**MiPO 推理对齐**：为对齐推理质量，VERITAS 引入混合偏好优化策略。不同于传统 DPO 使用单一非偏好样本，MiPO 构建混合非偏好数据，鼓励模型进行更精确和细粒度的推理。MiPO 损失函数为：

$$\mathcal { L } _ { 2 } = - \mathbb { E } _ { ( q , s _ { w } , s _ { l } ) \sim \mathcal { D } _ { 2 } } \left[ \log \sigma \left( \beta \log \frac { \pi _ { \theta } ( s _ { w } | q ) } { \pi _ { \theta _ { \mathrm { s g r } } } ( s _ { w } | q ) } - \beta \log \frac { \pi _ { \theta } ( s _ { l } | q ) } { \pi _ { \theta _ { \mathrm { s g r } } } ( s _ { l } | q ) } \right) \right]$$

其中 $s_w$ 为偏好响应，$s_l$ 为非偏好响应，$\pi_{\theta_{sgr}}$ 为参考模型，$\beta$ 控制偏差强度。

### 阶段二：模式感知探索

冷启动后，VERITAS 进入模式感知强化学习阶段，核心创新在于**模式感知奖励**设计，激励模型在推理中自适应地使用规划与自我反思模式。

**P-GRPO 目标函数**：采用带裁剪优势与 KL 惩罚的群组相对策略优化：

$$\mathcal { L } _ { 3 } = - \mathbb { E } _ { ( q , a ) \sim \mathcal { D } _ { 3 } , \{ o _ { i } \} _ { i = 1 } ^ { G } \sim \pi _ { \theta _ { \mathrm { o d d } } } ( \cdot | q ) } \frac { 1 } { \sum _ { i = 1 } ^ { G } \displaystyle \sum _ { | o _ { i } | } \sum _ { i = 1 } ^ { G } \sum _ { t = 1 } ^ { \left[ \operatorname* { m i n } \big ( r _ { i , t } ( \theta ) A _ { i , t } , \mathrm { c l i p } ( r _ { i , t } ( \theta ) , 1 - \epsilon , 1 + \epsilon ) A _ { i , t } \big ) - \beta ^ { \prime } D _ { \mathrm { K L } } \big [ \pi _ { \theta } \| \pi _ { \theta _ { \mathrm { c o h } } } \big ] \right] }$$

其中概率比与归一化优势定义为：

$$r _ { i , t } ( \theta ) = \frac { \pi _ { \theta } ( o _ { i , t } \mid I , o _ { i , < t } ) } { \pi _ { \theta _ { \mathrm { o l d } } } ( o _ { i , t } \mid I , o _ { i , < t } ) } , \quad A _ { i , t } = \frac { R _ { i } - \operatorname* { m e a n } ( \{ R _ { 1 } , \dots , R _ { G } \} ) } { \operatorname* { s t d } ( \{ R _ { 1 } , \dots , R _ { G } \} ) }$$

**模式感知奖励**：奖励函数根据答案正确性（$\mathcal{C}$）及是否包含规划（$\mathcal{P}$）、自我反思（$\mathcal{R}$）模式进行差异化赋值：

$$R _ { \mathrm { p a t t e r n } } = \left\{ \begin{array} { l l } { \ 2 . 0 , } & { \mathrm { i f } \ \mathcal { C } = 1 \ \wedge ( \mathcal { P } = 1 \vee \mathcal { R } = 1 ) , } \\ { \ 1 . 0 , } & { \mathrm { i f } \ \mathcal { C } = 1 \ \wedge \mathcal { P } = 0 \wedge \mathcal { R } = 0 , } \\ { \ 0 . 0 , } & { \mathrm { i f } \ \mathcal { C } = 0 \ \wedge \mathcal { P } = 0 \wedge \mathcal { R } = 0 , } \\ { - 0 . 5 , } & { \mathrm { i f } \ \mathcal { C } = 0 \ \wedge \mathcal { P } = 1 \wedge \mathcal { R } = 0 , } \\ { - 1 . 0 , } & { \mathrm { i f } \ \mathcal { C } = 0 \ \wedge \mathcal { R } = 1 . } \end{array} \right.$$

最终奖励由模式奖励、反思质量奖励（仅当答案正确时激活）和格式奖励加权求和：

$$R = R _ { \mathrm { p a t t e r n } } + \lambda _ { 1 } R _ { \mathrm { r e f } } \cdot \mathbb { I } ( \mathscr { C } = 1 ) + \lambda _ { 2 } R _ { \mathrm { f m t } }$$

### 关键消融证据

- **模式感知推理 vs. 灵活推理**：在 CF 和 CD 上分别带来 **+6.2%** 和 **+3.3%** 的增益（Table 2），验证了结构化思维模式对 OOD 泛化的关键作用。
- **MiPO 前置效果**：在 P-GRPO 前应用 MiPO 可在 CF 上带来 **+2.9%**、CD 上 **+2.1%** 的提升（Figure 4），表明冷启动阶段的推理对齐对后续 RL 探索至关重要。
- **模式感知奖励 vs. 纯准确率奖励**：尤其在 CF 和 CD 场景下优势显著（Table 3），证实了奖励设计中显式鼓励规划与反思的必要性。

VERITAS 的训练管线由两个阶段构成：模式引导冷启动（Pattern-Guided Cold-Start）与模式感知探索（Pattern-Aware Exploration），如 Figure 3 所示。冷启动阶段负责将人类分级取证思维模式内化到多模态大语言模型中，探索阶段则通过强化学习激励模型自适应地选择推理粒度。

### 4.1 模式引导冷启动

冷启动阶段包含两个子步骤：监督微调（SFT）格式注入与混合偏好优化（MiPO）推理对齐。

**SFT 格式注入** 的目标是让模型学会以五种结构化思维模式组织输出——`<fast>`（快速判断）、`<planning>`（规划）、`<reasoning>`（推理）、`<reflection>`（自我反思）、`<conclusion>`（结论）。SFT 数据通过多步标注管线构建：首先人工检查子集，将伪造痕迹归纳为三类（可感知结构异常、细微低级伪影、违反物理规律的认知偏差，见 Figure 9(a)），然后将标注解耦为三个专业化步骤生成模式感知推理数据（Figure 9(b)(c)）。SFT 损失为标准的自回归交叉熵：

$$\mathcal{L}_{1} = -\mathbb{E}_{(\pmb{q}, \pmb{s}) \sim \mathcal{D}_{1}} \sum_{t=1}^{T} \log \pi_{\theta}(\pmb{s}_{t} \mid \pmb{q}, \pmb{s}_{<t}) \tag{1}$$

其中 $\pmb{q}$ 为输入图像与问题，$\pmb{s}$ 为目标响应序列，$\pi_{\theta}$ 为策略模型。

**MiPO 推理对齐** 在 SFT 之后引入，用于对齐推理质量。其核心思想是构建混合非偏好数据：偏好样本 $s_w$ 为高质量推理轨迹，非偏好样本 $s_l$ 来自多个来源（包括错误答案、缺乏精细推理的正确答案等），迫使模型学习更精确、细粒度的推理。MiPO 损失采用 DPO 风格的目标函数：

$$\mathcal{L}_{2} = -\mathbb{E}_{(q, s_{w}, s_{l}) \sim \mathcal{D}_{2}} \left[ \log \sigma \left( \beta \log \frac{\pi_{\theta}(s_{w} \mid q)}{\pi_{\theta_{\mathrm{sgr}}}(s_{w} \mid q)} - \beta \log \frac{\pi_{\theta}(s_{l} \mid q)}{\pi_{\theta_{\mathrm{sgr}}}(s_{l} \mid q)} \right) \right] \tag{2}$$

其中 $\pi_{\theta_{\mathrm{sgr}}}$ 为参考模型（SFT 后的冻结副本），$\beta$ 为控制偏离强度的超参数。如 Figure 1 所示，通过学习混合拒绝轨迹，模型相比纯 SFT 冷启动能产生更精确的推理。

### 4.2 模式感知探索（P-GRPO）

第二阶段引入模式感知群组相对策略优化（Pattern-Aware GRPO），激励模型在模式粒度上自适应地执行规划与自我反思。

**P-GRPO 目标函数** 采用带裁剪优势与 KL 惩罚的 PPO 风格损失：

$$\mathcal{L}_{3} = -\mathbb{E}_{(q, a) \sim \mathcal{D}_{3}, \{o_{i}\}_{i=1}^{G} \sim \pi_{\theta_{\mathrm{odd}}}(\cdot \mid q)} \frac{1}{\sum_{i=1}^{G} \sum |o_{i}|} \sum_{i=1}^{G} \sum_{t=1}^{|o_{i}|} \left[ \min(r_{i,t}(\theta) A_{i,t}, \operatorname{clip}(r_{i,t}(\theta), 1-\epsilon, 1+\epsilon) A_{i,t}) - \beta' D_{\mathrm{KL}}[\pi_{\theta} \| \pi_{\theta_{\mathrm{coh}}}] \right] \tag{3}$$

其中概率比 $r_{i,t}(\theta)$ 与归一化优势 $A_{i,t}$ 定义为：

$$r_{i,t}(\theta) = \frac{\pi_{\theta}(o_{i,t} \mid I, o_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,t} \mid I, o_{i,<t})}, \quad A_{i,t} = \frac{R_{i} - \operatorname{mean}(\{R_{1}, \dots, R_{G}\})}{\operatorname{std}(\{R_{1}, \dots, R_{G}\})} \tag{4}$$

$G$ 为每组采样数，$\pi_{\theta_{\mathrm{old}}}$ 为旧策略，$\pi_{\theta_{\mathrm{coh}}}$ 为冷启动后的冻结参考模型，$\beta'$ 控制 KL 惩罚强度。

**模式感知奖励** 是 P-GRPO 的核心创新。奖励根据答案正确性 $\mathcal{C}$ 以及是否包含规划模式 $\mathcal{P}$、自我反思模式 $\mathcal{R}$ 进行分档：

$$R_{\mathrm{pattern}} = \begin{cases}
2.0, & \text{if } \mathcal{C}=1 \wedge (\mathcal{P}=1 \vee \mathcal{R}=1), \\
1.0, & \text{if } \mathcal{C}=1 \wedge \mathcal{P}=0 \wedge \mathcal{R}=0, \\
0.0, & \text{if } \mathcal{C}=0 \wedge \mathcal{P}=0 \wedge \mathcal{R}=0, \\
-0.5, & \text{if } \mathcal{C}=0 \wedge \mathcal{P}=1 \wedge \mathcal{R}=0, \\
-1.0, & \text{if } \mathcal{C}=0 \wedge \mathcal{R}=1.
\end{cases} \tag{5}$$

其设计逻辑是：正确答案且包含规划或反思给予最高奖励（2.0），单纯正确答案给予基准奖励（1.0），错误答案无规划/反思时中性（0.0），错误答案带规划轻微惩罚（-0.5），错误答案带反思则严厉惩罚（-1.0），以此抑制模型在错误路径上的无效反思。

**最终奖励组合** 将模式奖励、反思质量奖励（仅当答案正确时生效）和格式奖励加权求和：

$$R = R_{\mathrm{pattern}} + \lambda_{1} R_{\mathrm{ref}} \cdot \mathbb{I}(\mathscr{C}=1) + \lambda_{2} R_{\mathrm{fmt}} \tag{6}$$

其中 $R_{\mathrm{ref}}$ 由独立的奖励模型评估反思质量，$R_{\mathrm{fmt}}$ 确保输出符合预定义格式（见 Figure 8），$\lambda_{1}$、$\lambda_{2}$ 为平衡权重。这一设计使得模型在追求正确答案的同时，被显式激励去执行结构化规划与高质量自我反思，从而在跨伪造类型和跨数据域场景下获得更强的泛化能力（CF +6.2%，CD +3.3%，Table 2）。

## 实验与关键发现

### 核心瓶颈与实验动机

现有深度伪造检测器在跨模型（Cross-Model）场景下泛化良好，但在跨伪造类型（Cross-Forgery, CF）和跨数据域（Cross-Domain, CD）场景下性能大幅下降（Figure 2d）。VERITAS 的设计目标正是通过模式感知推理，将多模态大语言模型（MLLM）的推理能力注入检测任务，以提升对未见伪造的泛化能力，同时提供透明、可信的决策过程。

### 主实验结果

Table 1 报告了 HydraFake 数据集上四个评估场景的全面对比。VERITAS 在所有场景上均达到 SOTA 水平，相比此前最佳方法平均提升 **6.0%**。关键结论如下：

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_5VXJPS1HoM/figures/004_Table_1.jpg]]
*Table 1: Performance comparison (Acc.) on HydraFake dataset. In-domain (ID) results are averaged. To ensure fair comparisons with MLLM-based detectors, 1) we exclude ID set in their average results and 2) further restrict the training scope of our method to FF++, StyleGAN, StableDiffusion XL and FFHQ (similar to FFAA), yielding “VERITAS-MINI”. The best results are bolded and second best are underlined. More metrics in Appendix A.5*

- **跨域泛化优势显著**：在最具挑战性的 Cross-Domain（CD）子集上，VERITAS 达到 **82.2%** 准确率，超越此前最佳的 Gemini-2.5-Pro（72.8%）达 **+9.4%**（Table 13）。在 Cross-Forgery（CF）子集上同样表现突出。
- **域内性能不妥协**：在 In-Domain（ID）子集上，VERITAS 达到 **97.3%**，超越此前最佳的小型视觉模型 Effort（94.7%）达 +2.6%（Table 10）。
- **通用 MLLM 基线表现不佳**：Qwen2.5-VL-7B 仅获 51.2% 准确率，InternVL3-8B（VERITAS 基座模型）同样表现有限，说明通用 MLLM 的零样本/少样本推理能力远不足以胜任深度伪造检测。
- **公平比较设计**：为与 MLLM 检测器公平对比，计算平均结果时排除 In-Domain 集，并进一步将 VERITAS 的训练范围限制为 FF++、StyleGAN、StableDiffusion XL 和 FFHQ，得到 VERITAS-MINI，确保训练数据量可比。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_5VXJPS1HoM/figures/017_Table_10.jpg]]
*Table 10: Performance comparison on the In-Domain (ID) subset of HydraFake dataset. The best results are bolded and the second best are underlined. We report Accuracy (Acc.), Precision (P.) and Recall (R.) and the averaged results (Avg.) are reported in Accuracy*

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_5VXJPS1HoM/figures/020_Table_13.jpg]]
*Table 13: Performance comparison on the Cross-Domain (CD) subset of HydraFake dataset. The best results are bolded and the second best are underlined. We report Accuracy (Acc.), Precision (P.) and Recall (R.) and the averaged results (Avg.) are reported in Accuracy*

### 消融实验

#### 模式感知推理 vs. 灵活推理

Table 2 直接对比了模式感知推理与灵活推理（vanilla CoT）的效果。模式感知推理在 CF 和 CD 上分别带来 **+6.2%** 和 **+3.3%** 的显著增益，在 CM 上亦有 +4.1% 提升，验证了结构化思维模式对 OOD 泛化的关键作用。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_5VXJPS1HoM/figures/005_Table_2.jpg]]
*Table 2: Effect of the proposed Table 3: Ablations on the reward Table 4: Ablations on different pattern-aware reasoning. functions in P-GRPO. base models and model sizes*

#### 训练阶段消融

Figure 4 展示了不同训练阶段组合的效果。在 P-GRPO 前应用 MiPO 冷启动可在 CF 上带来 **+2.9%**、CD 上 **+2.1%** 的提升，证明混合偏好优化（MiPO）对后续强化学习探索具有重要的初始化作用。纯 RL（无冷启动）或仅 SFT 冷启动均无法达到同等性能。

#### 奖励函数设计

Table 3 消融了 P-GRPO 中的奖励函数。模式感知奖励（R_pattern）相比纯准确率奖励在 CF 上提升 **+4.0%**、CD 上提升 **+2.3%**，验证了显式激励规划与自我反思模式的有效性。反思质量奖励（R_ref）和格式奖励（R_fmt）的加入进一步带来增益。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_5VXJPS1HoM/figures/006_Table_3.jpg]]

#### 基座模型与规模

Table 4 显示，更大规模的基座模型带来更高的跨伪造准确率（InternVL3-14B CF 92.2 vs. InternVL3-2B CF 87.3），但 VERITAS 的训练框架在不同基座模型上均能带来一致提升。

#### 训练数据策略

Table 19 表明，P-GRPO 阶段采用平衡采样策略（ID 97.3, CF 90.3）优于随机采样。此外，将约 1/3 的未见 AIGIBench 数据加入 P-GRPO 阶段可在 CF 上带来额外 **+3.8%** 的提升（Section A.5.4），提示适度暴露未见分布有助于强化探索。

#### 推理质量评估

Table 7 通过评分和成对 ELO 评级评估推理质量。VERITAS 的推理过程在准确性、精细度和可解释性上均优于基线 MLLM 检测器，支持其“透明决策”的设计主张。

### 鲁棒性分析

Table 8 测试了压缩、模糊和缩放等扰动下的鲁棒性。VERITAS 在各类退化条件下保持相对稳定的检测性能，但极端模糊场景仍存在性能下降，属于已知局限。

### 失败模式分析

根据 Figure 22 和论文讨论，VERITAS 的主要失败模式包括：

- **低分辨率真实图像误判**：在 FF++、Facevid2vid 等低分辨率子集上，真实图像易被误判为伪造，原因是细节缺失导致自我反思机制失效。
- **未见伪造类型召回不足**：对 face relighting 等训练中未见的伪造类型，检测召回率偏低。
- **专有模型泛化有限**：对 Adobe Firefly、StarryAI 等专有生成模型的召回率仍有待提升。
- **极端跨域条件**：极端光照变化、严重模糊等场景下检测并非完全可靠。

### 关键图表索引

- **Table 1**：HydraFake 四场景全面对比，VERITAS 平均领先 6.0%。
- **Table 2**：模式感知推理消融，CF +6.2%，CD +3.3%。
- **Table 3**：奖励函数消融，模式感知奖励在 OOD 场景显著优于纯准确率奖励。
- **Figure 4**：训练阶段消融，MiPO + P-GRPO 组合最优。
- **Table 10–13**：ID / CM / CF / CD 各子集详细结果。
- **Table 14**：跨基准对比（AIGIBench + HydraFake-CD）。
- **Figure 22**：失败案例分析。

## 定位与知识库关联

### 1. 基线谱系与 VERITAS 的定位

VERITAS 处于传统小模型检测器与通用多模态大语言模型（MLLM）的交叉地带，其核心贡献在于将人类分级取证思维显式注入 MLLM 的训练过程。

**传统小模型基线**构成了深度伪造检测的经典范式。这些方法在跨模型（CM）场景下通常表现良好，但在跨伪造类型（CF）和跨数据域（CD）场景下泛化能力急剧下降（Figure 2d）。代表性工作包括：**F3Net**（Qian et al., ECCV 2020）、**UniFD**（Ojha et al., CVPR 2023）、**IID**（Huang et al., CVPR 2023）、**FreqNet**（Tan et al., AAAI 2024）、**ProDet**（Cheng et al., NIPS 2024）、**NPR**（Tan et al., CVPR 2024）、**AIDE**（Yan et al., ICLR 2025）、**Co-SPY**（Cheng et al., CVPR 2025）、**D3**（Yang et al., CVPR 2025）以及 **Effort**（Yan et al., ICML 2025）。其中 Effort 在 HydraFake 的 In-Domain（ID）子集上达到 94.7% 的准确率，是此前的最强小模型基线。

**通用 MLLM 基线**包括 **Qwen2.5-VL-7B**（Bai et al., 2025）、**InternVL3-8B**（Zhu et al., 2025，也是 VERITAS 的基座模型）、**MiMo-VL-7B**、**GLM-4.1V-9B-Thinking**（Hong et al., 2025），以及闭源模型 **GPT-4o**（Hurst et al., 2024）和 **Gemini-2.5-Pro**（Comanici et al., 2025）。这些模型在深度伪造检测任务上表现不佳——Qwen2.5-VL-7B 仅取得 51.2% 的平均准确率，Gemini-2.5-Pro 在跨域场景下仅 72.8%。这说明通用 MLLM 的推理能力未经专门适配时，无法有效迁移到深度伪造检测的细粒度取证需求上。

**MLLM 专用检测器基线**包括 **FakeShield**（Xu et al., 2024b）、**M2F2-Det**（Guo et al., 2025b）、**SIDA**（Huang et al., 2025a）、**FakeVLM**（Wen et al., 2025c）和 **FFAA**（Huang et al., 2024）。这些工作率先尝试将 MLLM 用于深度伪造检测，但缺乏结构化的推理模式引导和面向泛化性的强化学习设计。

VERITAS 在上述谱系中的定位是：**以 MLLM 为基座，通过模式感知的两阶段训练（冷启动 SFT+MiPO 与 P-GRPO 探索），将人类分层取证思维内化为模型的推理策略**。其关键创新在于三个可验证的“变更槽位”：

| 变更槽位 | 基线做法 | VERITAS 做法 | 证据锚点 |
|---------|---------|-------------|---------|
| 推理策略 | 未使用结构化思维模式或简单链式思维 | 引入五种模式感知推理模式（`<fast>`、`<planning>`、`<reasoning>`、`<reflection>`、`<conclusion>`） | Figure 3, Table 2 |
| 训练管道 | 单一阶段 SFT 或直接 RL | 两阶段：模式引导冷启动（SFT + MiPO）与模式感知探索（P-GRPO） | Figure 3, Section 4 |
| RL 奖励设计 | 仅基于答案正确性 | 模式感知奖励（结合正确性与规划/反思模式）与反思质量奖励 | Equation 5-6, Table 3 |

### 2. 因果机制与证据链

VERITAS 的性能优势可归因于一条清晰的因果链：

1. **模式注入（SFT）**：通过多步标注管道（Figure 9）构建包含五种思维模式标签的 SFT 数据，使基座模型 InternVL3-8B 初步掌握结构化推理的格式与节奏。
2. **推理对齐（MiPO）**：利用混合非偏好数据（包含错误推理轨迹）进行偏好优化，使模型学会区分精细推理与粗糙推理。消融实验表明，在 P-GRPO 前应用 MiPO 可带来 CF +2.9% 和 CD +2.1% 的增益（Figure 4）。
3. **模式感知探索（P-GRPO）**：通过模式感知奖励函数（Equation 5）激励模型在正确回答时自适应地使用规划（`#P`）和自我反思（`#R`）模式，同时对错误回答中的反思进行惩罚。模式感知奖励相比纯准确率奖励在 CF 和 CD 场景下提升显著（Table 3）。
4. **最终效果**：模式感知推理相比灵活推理在 CF 上提升 6.2%，在 CD 上提升 3.3%（Table 2）。VERITAS 在 HydraFake 四个评估场景上平均超越此前最佳方法 6.0%（Table 1），在 CD 子集上超越 Gemini-2.5-Pro 达 9.4%（82.2 vs 72.8）。

### 3. 适用边界与失效模式

VERITAS 的适用边界由以下限制条件定义：

- **低分辨率真实图像**：在 FF++、Facevid2vid 等低分辨率子集上，模型对真实图像的误判率较高。当图像严重缺失细节时，自我反思机制可能失效，导致将真实图像误判为伪造。
- **未见伪造类型**：在 face relighting 等训练中未覆盖的伪造类型上，合成图像的检测错误集中。专有模型（如 Adobe Firefly、StarryAI）上的召回率仍有待提高。
- **极端域偏移**：在极端光照变化、严重模糊等跨域泛化的极端情况下，模型并非完全可靠（Table 8 的鲁棒性测试提供了压缩、模糊、缩放下的一定韧性，但未覆盖所有退化类型）。
- **推理深度与计算成本的权衡**：P-GRPO 阶段需要生成 G 个候选响应（Table 18 对 G 的消融显示 G=8 为较优设置），推理成本高于单次前向的传统检测器。Table 16 的效率分析提供了推理时间对比，但实际部署中如何动态调整推理深度仍是一个开放问题。

### 4. 开放问题

论文明确指出了以下待解决问题：

1. **低分辨率子集的性能提升**：如何针对 FF++、Facevid2vid 等低质量数据改进检测能力？
2. **MLLM 与小模型的协作**：能否构建一个协作系统，让 MLLM 处理高分辨率图像的细粒度推理，同时由小型视觉模型高效处理低分辨率或简单样本？
3. **统一基准与框架**：当前评估集中在图像域，如何建立一个统一的图像-视频深度伪造检测基准与框架？
4. **推理成本控制**：在实际部署中，如何根据输入复杂度自适应地平衡推理深度与计算成本？

此外，从实验设置中可以观察到一个值得注意的细节：将约 1/3 的未见 AIGIBench 数据加入 P-GRPO 阶段可在 CF 上带来额外 3.8% 的提升（Section A.5.4）。这暗示 VERITAS 的泛化能力部分依赖于 RL 阶段对目标域分布的部分暴露，其真正的 zero-shot 泛化上限仍需在更严格的数据隔离条件下验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Veritas_Generalizable_Deepfake_Detection_via_Pattern_Aware_Reasoning.pdf]]
