---
title: "EMO-R3: Reflective Reinforcement Learning for Emotional Reasoning in Multimodal Large Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EMO_R3_Reflective_Reinforcement_Learning_for_Emotional_Reasoning_in_Multimodal_Large_Language_Models.pdf
project_link: null
code_link: "https://github.com/xiaomi-research/emo-r3"
aliases:
- ER
- EMO-R3
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入结构化情感思维（SET）将推理过程显式分解为情感触发识别、人类情感反思、情感结论三个阶段，同时设计反思性情感奖励（RER）让模型自评推理的视觉-文本一致性和情感连贯性，二者共同将优化目标从单纯答案匹配转向对推理质量的对齐。
primary_logic: 通过将人类情感认知的直觉逻辑（感知触发→主观反应→综合判断）固化为可解释的推理链，并利用模型自反思能力对推理质量进行闭环反馈，多模态大模型能够更准确地理解视觉场景中的情感线索，并在不同情感领域之间实现稳健迁移。
claims:
- EMO-R3在域内（EmoSet、Emotion6）和域外多个基准上，相比GRPO及其变体（DAPO、R1-VL、Visual-RFT等）均取得最高总体准确率。
- 消融实验证实，结构化情感思维（SET）和反思性情感奖励（RER）各自对性能有正向贡献，两者结合效果最优。
- 轻量级冷启动策略（Cold-Start-Emo）在不使用思维链标注的前提下进一步提升了EMO-R3的域外泛化能力。
- DAPO因奖励过滤策略与离散情感推理评估不兼容，无法完成完整训练，验证了任务特定适配的必要性。
---

# EMO-R3: Reflective Reinforcement Learning for Emotional Reasoning in Multimodal Large Language Models

> [!tip] 核心洞察
> 通过将人类情感认知的直觉逻辑（感知触发→主观反应→综合判断）固化为可解释的推理链，并利用模型自反思能力对推理质量进行闭环反馈，多模态大模型能够更准确地理解视觉场景中的情感线索，并在不同情感领域之间实现稳健迁移。

| 字段 | 内容 |
|------|------|
| 中文题名 | EMO-R3：面向多模态大语言模型情感推理的反思强化学习 |
| 英文题名 | EMO-R3: Reflective Reinforcement Learning for Emotional Reasoning in Multimodal Large Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23802) · [Code](https://github.com/xiaomi-research/emo-r3) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | EMO-R3 |
| Dataset | EmoSet, Emotion6 (in-domain) 及多个域外情感理解基准 |

> [!tip] 效果简介
> - EmoSet, Emotion6 (in-domain) 及多个域外情感理解基准 上，准确率 (Accuracy) 60.50 (rollout 4) / 60.42 (rollout 8) (Table 1) vs GRPO及其他变体 (具体数值见Table 1) (EMO-R3在所有设置下均优于所有对比方法，获最高总体准确率)。
> - 多域情感理解基准（含域外泛化） 上，准确率 (Accuracy) 62.13 (EMO-R3 + Cold-Start-Emo, Table 2) vs EMO-R3 without Cold-Start-Emo (Cold-Start-Emo显著提升域外平均准确率)。
> - 验证集训练过程稳定性 上，训练/测试准确率曲线 训练过程稳定收敛 vs DAPO训练失败，无法完成 (DAPO因奖励过滤不匹配导致训练中断，验证EMO-R3设计的合理性)。

## 概要

多模态大语言模型（MLLMs）在情感理解任务中面临一个关键瓶颈：通用的强化学习优化方法（如 **GRPO** (Shao et al., arXiv 2024)）使用单一的“思考”指令，无法引导模型进行结构化的情感推理，导致推理路径与最终答案之间关联薄弱，视觉情感信号捕捉不稳定且可解释性差；而传统的监督微调（SFT）受限于封闭的离散标签空间，泛化能力不足。

针对这一问题，本文提出 **EMO-R3**（Reflective Reinforcement Learning for Emotional Reasoning）框架，其核心调控逻辑包含两个协同组件：**结构化情感思维（Structured Emotional Thinking, SET）** 将推理过程显式分解为“情感触发识别 → 人类情感反思 → 情感结论”三个阶段，使推理链可解释且贴近人类情感认知的直觉逻辑；**反思性情感奖励（Reflective Emotional Reward, RER）** 则让模型自评推理的视觉-文本一致性（图像内容与触发描述是否匹配）和情感连贯性（基于前两步推理预测的情感是否与真实标签一致），从而将优化目标从单纯的答案匹配转向对推理质量的闭环对齐。此外，一个轻量级的冷启动策略（Cold-Start-Emo）在不依赖思维链标注的前提下，通过少量 SFT 样本进行任务初始化对齐，进一步稳定训练并提升域外泛化能力。

实验结果表明，EMO-R3 在域内（EmoSet、Emotion6）和多个域外情感理解基准上均取得最高总体准确率，一致优于 GRPO 及其变体（DAPO、R1-VL、Visual-RFT 等）。消融研究证实 SET 和 RER 各自对性能有正向贡献，且二者结合效果最优。特别地，DAPO 因其奖励过滤策略与离散情感推理评估不兼容而无法完成完整训练，从反面验证了任务特定适配的必要性。

多模态大语言模型（MLLMs）在视觉感知和文本理解方面取得了显著进展，但在情感推理这一高度主观的任务上仍面临根本性挑战。情感理解要求模型不仅能识别图像中的物体和场景，还需要捕捉微妙的情感线索——如面部表情、姿态、色彩氛围和场景语义——并将其整合为连贯的情感判断。这一过程本质上需要可解释的推理链，而非简单的模式匹配。

当前主流方法存在两类典型局限。**监督微调（SFT）**依赖人工标注的情感标签训练模型，但受限于封闭的标签空间和有限的类别体系，导致泛化能力薄弱。如 Figure 1(a) 所示，SFT 在域内样本（如“风景–敬畏”）上表现良好，但面对域外或未见过的情感组合（如“运动–惊讶”）时推理能力急剧退化，且其黑箱式预测缺乏可解释性。另一方面，基于强化学习的 **GRPO**（Group Relative Policy Optimization；Shao et al., arXiv 2024）通过奖励信号引导模型探索更优策略，在一定程度上改善了泛化性，但其核心瓶颈在于：通用的单一“思考”（think）指令无法引导模型进行结构化的情感推理，导致生成的推理路径与最终答案之间关联薄弱。如 Figure 1(b) 所示，GRPO 的思考过程可能反复摇摆，最终预测“恐惧”而推理却指向“愉悦”，暴露出视觉情感信号捕捉不稳定、可解释性差的根本缺陷。

这一瓶颈的深层原因在于：情感认知本身遵循“感知触发→主观反应→综合判断”的直觉逻辑，而现有方法未能将这一认知结构显式地编码到模型的推理过程中。同时，GRPO 的奖励函数仅包含准确率奖励和格式奖励，缺乏对推理质量的直接反馈信号，使得优化目标停留在答案匹配层面，而非推理过程的对齐。

针对上述问题，本文提出 **EMO-R3**（Reflective Reinforcement Learning for Emotional Reasoning），核心思路是通过两个关键设计将优化目标从单纯的答案匹配转向对推理质量的对齐：（1）**结构化情感思维（Structured Emotional Thinking, SET）**，将推理过程显式分解为情感触发识别、人类情感反思、情感结论三个阶段，为模型提供可解释的推理框架；（2）**反思性情感奖励（Reflective Emotional Reward, RER）**，利用模型自反思能力对推理的视觉-文本一致性和情感连贯性进行闭环评估，使奖励信号直接反映推理质量。此外，轻量级冷启动策略（Cold-Start-Emo）在不使用思维链标注的前提下实现任务初始化对齐，进一步稳定训练并提升域外泛化能力。

## 核心方法与创新机理

EMO-R3的核心创新在于将**人类情感认知的直觉逻辑**固化为可解释的推理链，并利用**模型自反思能力**对推理质量进行闭环反馈，从而将多模态大语言模型的优化目标从单纯的答案匹配转向对推理过程质量的对齐。

### 1. 结构化情感思维（Structured Emotional Thinking, SET）

通用GRPO方法使用单一的“think”指令引导模型生成推理轨迹，缺乏对情感推理过程的结构化约束，导致推理路径与最终答案关联弱，模型对视觉情感信号的捕捉不稳定且可解释性差。EMO-R3提出**三阶段结构化情感思维提示**，将推理过程显式分解为：

1. **情感触发识别（Emotional Trigger Identification）**：识别图像中引发情感反应的具体视觉元素；
2. **人类情感反思（Human Emotional Reflection）**：基于识别到的触发物，推理人类可能产生的主观情感反应；
3. **情感结论（Emotional Conclusion）**：综合前两步推理，得出最终的情感类别判断。

这一设计将人类情感认知的直觉逻辑（感知触发→主观反应→综合判断）固化为模型必须遵循的推理范式，使得每一步推理都具有明确的功能定位和可解释性。与通用“think”指令相比，SET为模型提供了情感推理的认知脚手架，强制模型建立从视觉证据到情感判断的因果链条。

### 2. 反思性情感奖励（Reflective Emotional Reward, RER）

GRPO及其变体的奖励函数通常仅包含准确率奖励（$\mathcal{R}_{\mathrm{acc}}$）和格式奖励（$\mathcal{R}_{\mathrm{format}}$），无法评估推理过程本身的质量。EMO-R3引入**反思性情感奖励**，利用模型的自反思能力对推理质量进行闭环评估，包含两个互补的反馈信号：

- **图像-文本一致性奖励（$\mathcal{R}_{\mathrm{cons}}$）**：将第一步推理生成的“情感触发描述”反馈给模型自身，令其判断该描述是否与图像内容一致。若模型自评为“Yes”，则获得正向奖励。该机制强制模型的推理必须根植于可验证的视觉证据，抑制幻觉式的情感归因。

- **情感连贯性奖励（$\mathcal{R}_{\mathrm{coh}}$）**：将基于前两步推理预测的情感类别与真实标签进行比对，判断推理链条是否导向正确的情感结论。该奖励确保推理的因果逻辑与最终判断之间保持连贯性，而非仅依赖答案匹配。

反思性情感奖励取两者的均值：$\mathcal{R}_{\mathrm{RER}} = \frac{1}{2}(\mathcal{R}_{\mathrm{cons}} + \mathcal{R}_{\mathrm{coh}})$，并与准确率奖励、格式奖励加权组合为综合奖励函数：
$$\mathcal{R}_{\mathrm{overall}} = (1 - \lambda_1 - \lambda_2)\mathcal{R}_{\mathrm{acc}} + \lambda_1\mathcal{R}_{\mathrm{RER}} + \lambda_2\mathcal{R}_{\mathrm{format}}$$
其中 $\lambda_1 = \lambda_2 = 0.1$。

### 3. 冷启动策略（Cold-Start-Emo）

通用GRPO直接从预训练模型开始强化学习优化，面临预训练先验与下游情感任务之间的分布偏移问题。EMO-R3提出**轻量级冷启动策略**：使用少量**无思维链标注**的样本进行监督微调初始化，提前对齐模型的输出格式与情感任务的基本范式。该策略无需昂贵的思维链标注成本，却能在正式GRPO训练前为模型提供任务感知的初始先验，有效稳定训练过程并提升域外泛化能力。

### 创新点总结

| 改进槽位 | 基线方案 | EMO-R3方案 | 核心作用 |
|---------|---------|-----------|---------|
| 思考提示格式 | 单一“think”指令 | 三阶段结构化提示（触发识别→情感反思→结论） | 建立可解释的推理因果链，提升视觉情感信号捕捉能力 |
| 奖励函数构成 | 仅$\mathcal{R}_{\mathrm{acc}}$ + $\mathcal{R}_{\mathrm{format}}$ | 增加$\mathcal{R}_{\mathrm{RER}}$（含$\mathcal{R}_{\mathrm{cons}}$和$\mathcal{R}_{\mathrm{coh}}$） | 引入推理质量的自反思闭环反馈，对齐视觉证据与情感判断 |
| 冷启动策略 | 直接从预训练模型开始GRPO | 少量无CoT标注样本的轻量级SFT初始化 | 稳定训练过程，提升域外泛化能力 |

消融实验证实，SET和RER各自对性能有正向贡献，且两者结合效果最优；Cold-Start-Emo在EMO-R3基础上进一步提升域外平均准确率至62.13%。值得注意的是，GRPO变体**DAPO**（Yu et al., arXiv 2025）因其奖励过滤策略与离散情感推理评估不兼容，训练过程直接中断，从反面验证了任务特定适配的必要性。

EMO-R3 的整体框架围绕一个核心问题展开：**通用强化学习（GRPO）的单一思考指令无法引导多模态大模型进行结构化的情感推理，且其推理路径与最终答案关联弱，导致模型对视觉情感信号捕捉不稳定、可解释性差**。为解决这一问题，EMO-R3 将人类情感认知的直觉逻辑（感知触发 → 主观反应 → 综合判断）固化为可解释的推理链，并利用模型自反思能力对推理质量进行闭环反馈，从而将优化目标从单纯答案匹配转向对推理质量的对齐。

### 框架总览

EMO-R3 的架构由两大核心创新模块和一个可选初始化模块组成，整体嵌入 GRPO 优化循环中（见 Figure 2）。给定一张图像 $I$ 和文本查询 $T$，模型 $\mathcal{M}_{\theta}$ 生成包含三阶段推理与最终答案的结构化输出 $o = \mathcal{M}_{\theta}(I, T)$，最终情感预测 $\hat{\mathcal{E}}$ 由解析函数 $\mathcal{F}_a(o)$ 从输出中提取。

![[assets/figures/papers/paper_list_l2657_https_arxiv_org_abs_2602_23802/figures/002_Figure_2.jpg]]
*Figure 2: Architecture illustration of EMO-R3. The upper part presents the Structured Emotional Thinking prompt, which consists of three consecutive thinking steps followed by a final answer. The lower part illustrates the Reflective Emotional Reward mechanism, where multiple rollout samples are evaluated based on image–text consistency and emotional coherence, and are jointly optimized with the original Format and Accuracy rewards under the GRPO framework*

**结构化情感思维（Structured Emotional Thinking, SET）** 位于框架的上游，负责将推理过程显式分解为三个连续阶段：**情感触发识别**（识别图像中引发情感的关键视觉元素）、**人类情感反思**（基于触发元素推断可能引发的人类情感反应）、**情感结论**（综合前两步得出最终情感类别）。这一结构化提示替代了通用 GRPO 中单一的 “think” 指令，使推理过程具备可解释性和情感导向性。

**反思性情感奖励（Reflective Emotional Reward, RER）** 位于框架的下游反馈端，由两个子模块组成：**图像-文本一致性奖励**（$\mathcal{R}_{\mathrm{cons}}$）判断推理中的情感触发描述是否与图像内容一致；**情感连贯性奖励**（$\mathcal{R}_{\mathrm{coh}}$）判断基于前两步推理得出的情感类别是否与真实情绪标签一致。RER 的最终值取两者平均：$\mathcal{R}_{\mathrm{RER}} = \frac{1}{2} (\mathcal{R}_{\mathrm{cons}} + \mathcal{R}_{\mathrm{coh}})$。

**GRPO 优化循环** 将上述模块整合为统一的强化学习训练流程。在每次迭代中，模型对同一输入采样 $G$ 个 rollout 样本，每个样本的奖励由三部分加权组成：

$$\mathcal{R}_{\mathrm{overall}} = (1 - \lambda_1 - \lambda_2) \mathcal{R}_{\mathrm{acc}} + \lambda_1 \mathcal{R}_{\mathrm{RER}} + \lambda_2 \mathcal{R}_{\mathrm{format}}$$

其中 $\mathcal{R}_{\mathrm{acc}}$ 为预测标签与真实标签是否一致的二值准确率奖励，$\mathcal{R}_{\mathrm{format}}$ 检查输出是否符合预设的步骤及 `\boxed{}` 格式。组内奖励经标准化为零均值单位方差后计算优势 $\hat{A}_i = \frac{r_i - \mu}{\sigma}$，模型参数通过最大化截断比例期望并减去 KL 散度惩罚来更新：

$$\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{q \sim \rho_Q} \mathbb{E}_{o \sim \pi_{\mathrm{old}}(\cdot|q)} \left[ \frac{1}{G} \sum_{i=1}^{G} f_{\epsilon} \left( \frac{\pi_{\theta}(o_i|q)}{\pi_{\mathrm{old}}(o_i|q)}, \hat{A}_i \right) \right] - \beta \mathbb{D}_{KL}[\pi_{\theta}||\pi_{\mathrm{ref}}]$$

**冷启动策略（Cold-Start-Emo）** 作为可选的前置模块，使用少量无思维链标注的样本进行轻量级 SFT 初始化，以提前对齐预训练先验与下游情感任务。消融实验证实，Cold-Start-Emo 能有效稳定训练并进一步提升域外泛化能力，且无需依赖思维链标注。

### 与基线方法的根本差异

相比 GRPO 及其变体，EMO-R3 的核心差异体现在两个“改变槽位”上：

| 模块 | 基线做法 | EMO-R3 做法 | 关键作用 |
|------|----------|-------------|----------|
| 思考提示格式 | 单一 “think” 指令，无结构化指导 | 三阶段结构化提示：情感触发识别 → 人类情感反思 → 情感结论 | 引导模型进行可解释的情感推理，强化视觉-情感关联 |
| 奖励函数构成 | 仅准确率奖励 + 格式奖励 | 额外增加反思性情感奖励（图像-文本一致性 + 情感连贯性） | 提供推理质量闭环反馈，对齐视觉线索与情感结论 |

值得注意的是，GRPO 变体 **DAPO**（Yu et al., arXiv 2025）因采用奖励过滤策略，与离散情感推理评估不兼容，在训练过程中无法完成完整训练（见 Figure 3），这从反面验证了 EMO-R3 任务特定适配的必要性。

### 数据流与模块交互

整个框架的数据流可概括为：图像和文本输入 → SET 引导生成结构化推理轨迹 → GRPO 采样多个 rollout → RER 对推理质量进行自反思评估 → 综合奖励信号回传更新模型参数。这一闭环设计使得模型不仅被优化为“答对”，更被优化为“推理得对”——即推理过程与视觉内容一致、情感推导连贯。

EMO-R3 的核心架构由两个相互咬合的创新模块构成：**结构化情感思维（Structured Emotional Thinking, SET）** 和 **反思性情感奖励（Reflective Emotional Reward, RER）**，二者共同运行在 GRPO 优化框架之上。以下逐一拆解各模块的关键公式与变量含义。

### 3.1 GRPO 基座优化框架

EMO-R3 的策略优化建立在 Group Relative Policy Optimization（GRPO）之上。GRPO 是 PPO 的一种变体，通过组内相对优势估计来稳定训练。其目标函数为：

$$
\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{q \sim \rho_Q} \mathbb{E}_{o \sim \pi_{\mathrm{old}}(\cdot|q)} \left[ \frac{1}{G} \sum_{i=1}^{G} f_{\epsilon} \left( \frac{\pi_{\theta}(o_i|q)}{\pi_{\mathrm{old}}(o_i|q)}, \hat{A}_i \right) \right] - \beta \mathbb{D}_{KL}[\pi_{\theta}||\pi_{\mathrm{ref}}]
$$

其中，$q$ 为从查询分布 $\rho_Q$ 中采样的输入，$o_i$ 为旧策略 $\pi_{\mathrm{old}}$ 对同一查询生成的第 $i$ 条输出，$G$ 为组内采样数。$f_{\epsilon}$ 是截断函数，约束新旧策略的概率比在 $[1-\epsilon, 1+\epsilon]$ 范围内。优势 $\hat{A}_i$ 经组内标准化计算：

$$
\hat{A}_i = \frac{r_i - \mu}{\sigma}, \quad \mu = \frac{1}{G} \sum r_i, \quad \sigma = \sqrt{\frac{1}{G} \sum (r_i - \mu)^2}
$$

式中 $r_i$ 为第 $i$ 条输出的总奖励，$\mu$ 和 $\sigma$ 分别为组内均值和标准差。标准化后的优势使梯度更新不受奖励绝对尺度的影响，提升训练稳定性。最后一项 $\beta \mathbb{D}_{KL}[\pi_{\theta}||\pi_{\mathrm{ref}}]$ 为 KL 散度惩罚，防止新策略 $\pi_{\theta}$ 偏离参考策略 $\pi_{\mathrm{ref}}$ 过远。

### 3.2 结构化情感思维（SET）

SET 将模型的推理输出 $o$ 显式分解为三个连续的思考步骤，引导模型像人类一样进行情感推理。给定输入图像 $I$ 和文本提示 $T$，模型 $\mathcal{M}_{\theta}$ 生成结构化输出：

$$
o = \mathcal{M}_{\theta}(I, T), \quad \hat{\mathcal{E}} = \mathcal{F}_a(o)
$$

其中 $\mathcal{F}_a$ 为答案提取函数，从输出中解析最终情感预测 $\hat{\mathcal{E}}$。三阶段推理结构为：
1. **情感触发识别**：识别图像中引发情感的关键视觉元素；
2. **人类情感反思**：基于触发元素推断人类可能产生的主观情感反应；
3. **情感结论**：综合前两步推理，得出最终情感类别。

这一结构化提示替代了通用 GRPO 中单一的 “think” 指令，使推理过程可解释、可审计。

### 3.3 反思性情感奖励（RER）

RER 是 EMO-R3 的核心创新，它让模型在训练时自评推理质量，形成闭环反馈。RER 由两个子奖励组成：

**图像-文本一致性奖励** 判断第一步推理（情感触发描述）是否与图像内容一致：

$$
\mathcal{R}_{\mathrm{cons}} = \begin{cases} 1, & \text{if } \hat{y}_{\mathrm{cons}} = \mathrm{Yes}; \\ 0, & \text{otherwise.} \end{cases}
$$

其中 $\hat{y}_{\mathrm{cons}}$ 是模型对 “推理是否准确描述了图像内容” 的自评结果。

**情感连贯性奖励** 判断基于前两步推理预测的情绪是否与真实标签 $\mathcal{E}^{*}$ 一致：

$$
\mathcal{R}_{\mathrm{coh}} = \begin{cases} 1, & \text{if } \hat{y}_{\mathrm{coh}} = \mathcal{E}^{*}; \\ 0, & \text{otherwise.} \end{cases}
$$

最终，反思性情感奖励取两者的均值：

$$
\mathcal{R}_{\mathrm{RER}} = \frac{1}{2} (\mathcal{R}_{\mathrm{cons}} + \mathcal{R}_{\mathrm{coh}})
$$

### 3.4 综合奖励与冷启动

EMO-R3 的完整奖励函数将准确率奖励 $\mathcal{R}_{\mathrm{acc}}$、反思性情感奖励 $\mathcal{R}_{\mathrm{RER}}$ 和格式奖励 $\mathcal{R}_{\mathrm{format}}$ 进行加权融合：

$$
\mathcal{R}_{\mathrm{overall}} = (1 - \lambda_1 - \lambda_2) \mathcal{R}_{\mathrm{acc}} + \lambda_1 \mathcal{R}_{\mathrm{RER}} + \lambda_2 \mathcal{R}_{\mathrm{format}}
$$

其中 $\lambda_1 = \lambda_2 = 0.1$。准确率奖励为二值信号——预测标签与真实标签一致时为 1，否则为 0；格式奖励检查输出是否包含规定的推理步骤和 `\boxed{}` 答案框。

此外，EMO-R3 引入轻量级 **Cold-Start-Emo** 策略：在 GRPO 训练前，使用少量无思维链标注的样本进行监督微调初始化，提前对齐预训练先验与下游情感任务，进一步稳定训练并提升域外泛化能力。

## 实验与关键发现

### 核心性能对比

EMO-R3在域内（EmoSet、Emotion6）和多个域外情感理解基准上，与当前最先进的GRPO变体进行了系统对比。**Table 1**展示了详细结果：EMO-R3在rollout 4和rollout 8两种设置下分别取得60.50和60.42的总体准确率，在所有对比方法中均获最高。这一结果验证了结构化情感思维（SET）与反思性情感奖励（RER）相结合的有效性——通用GRPO（**GRPO**，Shao et al., arXiv 2024）及其变体虽在视觉推理任务上有所改进，但缺乏对情感推理的结构化适配，导致推理路径与答案关联弱、视觉情感信号捕捉不稳定。

![[assets/figures/papers/paper_list_l2657_https_arxiv_org_abs_2602_23802/figures/003_Table_1.jpg]]
*Table 1: Performance comparison with the state-of-the-art GRPO variants on the emotional reasoning tasks across in-domain and out-of-domain settings. * denotes models without post-training. Datasets marked with the superscript I, e.g. EmoSetI and Emotion6I , denote the in-domain training dataset. We mark the Best in bold across different methods. Please refer to Sec. 4.2 for details*

值得注意的是，**DAPO**（Yu et al., arXiv 2025）在训练过程中因奖励过滤策略与离散情感推理评估不兼容而无法完成完整训练（**Figure 3**）。该失败模式从反面证实：情感推理任务需要任务特定的奖励设计，通用强化学习策略的直接迁移存在根本性适配障碍。其他变体如**R1-VL**（Zhang et al., arXiv 2025）、**Visual-RFT**（Liu et al., arXiv 2025）和**R1-Omni**（Zhao et al., arXiv 2025）虽能完成训练，但在情感推理的准确性和泛化性上均不及EMO-R3。

![[assets/figures/papers/paper_list_l2657_https_arxiv_org_abs_2602_23802/figures/004_Figure_3.jpg]]
*Figure 3: Training and testing accuracy during the training process. DAPO fails to conduct complete training. A more detailed analysis of this failure is provided in Sec. 4.2*

### 冷启动策略的增益

**Table 2**展示了轻量级冷启动策略（Cold-Start-Emo）的效果。该策略仅使用少量无思维链标注的样本进行监督微调初始化，即可在EMO-R3基础上进一步提升域外泛化能力，最终总体平均准确率达到62.13。这表明，在强化学习优化之前，通过少量样本对预训练先验进行任务对齐，能有效稳定训练过程并提升最终性能，且无需依赖昂贵的思维链标注数据。

### 消融实验：SET与RER的贡献

**Table 3**的消融实验揭示了各组件的独立贡献：

1. **仅使用SET**：在原始GRPO基础上引入结构化情感思维，性能即有显著提升。这证实了将推理过程显式分解为情感触发识别→人类情感反思→情感结论三个阶段，能够有效引导模型进行可解释的情感推理，而非依赖通用思考指令。

2. **SET + RER**：在SET基础上引入反思性情感奖励，带来额外的显著增益。RER的两个子模块——图像-文本一致性奖励（$\mathcal{R}_{\mathrm{cons}}$）和情感连贯性奖励（$\mathcal{R}_{\mathrm{coh}}$）——分别从视觉对齐和推理连贯性两个维度提供反馈信号，使模型能够自评推理质量并进行闭环优化。

3. **完整EMO-R3**（SET + RER + Cold-Start-Emo）：三者结合达到最优性能，验证了“结构化推理引导 + 反思性质量反馈 + 轻量任务初始化”这一组合策略的协同效应。

### 训练稳定性与失败分析

**Figure 3**记录了DAPO在训练过程中的准确率曲线。由于DAPO采用奖励过滤策略（仅保留高奖励样本进行更新），而情感推理任务中离散标签空间下的奖励分布特性导致有效训练样本被过度过滤，最终训练中断。这一失败模式揭示了情感推理强化学习的关键约束：奖励设计必须与任务评估特性兼容，简单的过滤式策略优化在此类主观推理任务中不可行。相比之下，EMO-R3的反思性奖励通过模型自评估生成连续的反馈信号，避免了奖励稀疏性问题，训练过程稳定收敛。

### 训练效率分析

**Figure 5**展示了EMO-R3训练过程中反思性奖励的额外计算开销占比。由于RER需要在训练时对每个rollout样本进行额外的前向评估（将推理文本反馈回模型进行自评），训练计算量有所增加。但论文指出，该开销未显著影响推理阶段的成本——推理时仅需执行结构化思维提示，无需额外的反思评估步骤。具体的效率-性能权衡需参考原图数值进行进一步分析。

### 案例研究

**Figure 4**对比了GRPO与EMO-R3在EmoSet数据集上的情感推理输出。GRPO的推理过程与最终答案之间关联弱（如推理中提及“amusement”但预测为“fear”），而EMO-R3通过三阶段结构化推理，使情感触发识别、人类情感反思和最终结论之间形成连贯的逻辑链条，显著提升了推理的可解释性和准确性。具体案例细节需参考原图进行人工验证。

![[assets/figures/papers/paper_list_l2657_https_arxiv_org_abs_2602_23802/figures/005_Table_2.jpg]]
*Table 2: Experiment on Cold-Start-Emo*

![[assets/figures/papers/paper_list_l2657_https_arxiv_org_abs_2602_23802/figures/006_Table_3.jpg]]
*Table 3: Ablative study of Structured Emotional Thinking (SET) and Reflective Emotional Reward (RER). Please see Sec. 4.3*

![[assets/figures/papers/paper_list_l2657_https_arxiv_org_abs_2602_23802/figures/007_Figure_4.jpg]]
*Figure 4: Case study between GRPO and EMO-R3 on the EmoSet dataset. Please see Sec. 4.4 for details*

## 定位与知识库关联

### 1. 与基线方法的关系

EMO-R3 的核心贡献在于将通用强化学习优化框架适配到情感推理这一特定主观任务上，其设计动机直接源于对现有方法瓶颈的诊断。

**与 GRPO 及其变体的关系。** 通用 **GRPO**（Shao et al., arXiv 2024）采用单一的“think”指令引导模型进行自由形式推理，并仅依赖准确率奖励 $\mathcal{R}_{\text{acc}}$ 和格式奖励 $\mathcal{R}_{\text{format}}$ 进行优化。这一范式在情感推理中暴露出两个关键缺陷：推理过程缺乏结构化，导致模型难以捕捉视觉情感信号；推理路径与最终答案之间关联弱，使优化目标无法有效对齐推理质量（见 Figure 1 的动机说明）。EMO-R3 直接针对这两个缺陷进行改造：一方面通过**结构化情感思维（SET）**将推理显式分解为情感触发识别、人类情感反思、情感结论三个阶段，替代通用思考提示；另一方面引入**反思性情感奖励（RER）**，在原有奖励基础上增加图像-文本一致性奖励 $\mathcal{R}_{\text{cons}}$ 和情感连贯性奖励 $\mathcal{R}_{\text{coh}}$，将优化目标从单纯的答案匹配转向对推理质量的对齐。

在 GRPO 的多个变体中，**DAPO**（Yu et al., arXiv 2025）采用了奖励过滤策略，但该策略与离散情感推理评估不兼容，导致训练过程中模型无法完成完整训练（见 Figure 3 的训练曲线），验证了任务特定适配的必要性。**R1-VL**（Zhang et al., arXiv 2025）和 **Visual-RFT**（Liu et al., arXiv 2025）分别通过逐步 GRPO 优化和视觉强化微调扩展了 GRPO 的应用场景，但并未针对情感推理的主观性和可解释性需求进行专门设计。**R1-Omni**（Zhao et al., arXiv 2025）虽将 GRPO 应用于全模态情感识别，但在结构化推理和反思性反馈方面缺乏显式建模。Table 1 的性能对比表明，EMO-R3 在域内（EmoSet、Emotion6）和域外多个基准上均取得最高总体准确率，验证了结构化推理与反思奖励组合设计的有效性。

**与监督微调（SFT）的关系。** 传统 SFT 依赖人工标注的离散情感标签进行训练，受限于封闭标签空间和有限的情感类别，导致泛化能力差、可解释性不足。EMO-R3 通过强化学习框架突破了这一限制，使模型能够在开放推理空间中学习情感理解能力。值得注意的是，EMO-R3 提出的**冷启动策略（Cold-Start-Emo）**使用少量无思维链标注的样本进行轻量级 SFT 初始化，在保留强化学习泛化优势的同时，有效稳定了训练过程并进一步提升了域外泛化能力（Table 2），实现了监督信号与强化学习之间的互补。

**与 AffectGPT 的关系。** **AffectGPT**（Lian et al., arXiv 2025）同样探索了基于大语言模型的多模态情感理解，但侧重于端到端的生成式情感推理，缺乏对推理过程的结构化约束和反思性质量评估机制。EMO-R3 的结构化思维和反思奖励框架可视为对这类情感推理模型的通用增强方案。

### 2. 适用边界与局限

**任务边界。** EMO-R3 当前的设计主要针对静态图像和离散情感类别的情感推理任务。其结构化情感思维的三阶段分解（触发识别→人类反思→情感结论）基于人类对静态视觉场景的情感认知逻辑，尚未扩展到动态视频、语音等多模态序列或连续情感维度（如 Valence-Arousal 空间）下的可解释情感推理。

**计算开销。** 反思性情感奖励机制要求模型在训练时进行额外的前向评估——将生成的推理文本反馈回模型以判断图像-文本一致性和情感连贯性。这增加了训练计算开销，但论文通过效率分析（Figure 5）表明，这一额外开销在总训练时间中占比较小，且不会增加推理阶段的成本。

**冷启动依赖。** Cold-Start-Emo 策略仍需依赖少量 SFT 数据（尽管无需思维链标注），在完全无监督的开放场景中，如何从零开始引导情感推理能力的涌现仍有待验证。

### 3. 开放问题与未来方向

1. **动态情感推理扩展。** 如何将 EMO-R3 的反思性推理框架扩展到交互式对话中的实时情感跟踪或顺序情感动态建模？这需要将三阶段结构化思维适配到时序依赖的情感推理场景，并设计相应的时序一致性奖励。

2. **反思性奖励的泛化能力。** 反思性情感奖励机制的核心思想——利用模型自反思评估推理质量——能否泛化为通用的主观推理质量评估器？这一机制可能被应用于美学评估、幽默理解、讽刺检测等其他高度主观的多模态任务，但需要验证图像-文本一致性和情感连贯性奖励在非情感场景中的适用性及其变体设计。

3. **无监督情感推理涌现。** 能否完全消除对冷启动 SFT 的依赖，通过更精妙的奖励设计或课程学习策略从零开始引导情感推理能力的涌现？这需要探索如何在完全无标注的条件下，引导模型自主发现结构化的情感推理模式。

## 原文 PDF

![[paperPDFs/CVPR_2026/EMO_R3_Reflective_Reinforcement_Learning_for_Emotional_Reasoning_in_Multimodal_Large_Language_Models.pdf]]
