---
title: "AToM: Aligning Text-to-Motion Model at Event-Level with GPT-4Vision Reward"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/AToM_Aligning_Text_to_Motion_Model_at_Event_Level_with_GPT_4Vision_Reward.pdf
aliases:
- AToM
tags:
- CVPR_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "利用视觉-语言大模型（GPT-4V）生成细粒度事件级对齐奖励信号，并通过强化学习（IPO）微调基础动作生成模型。"
primary_logic: "通过设计任务相关提示并让GPT-4V对生成的多个动作序列进行三个维度（完整性、时间、频率）评分，构建细粒度偏好数据集MotionPrefer，使用该数据集以LoRA和IPO损失对MotionGPT进行微调，能够显著提升文本-动作生成的事件级对齐质量。"
claims:
- "AToM框架由三个阶段构成：数据集构建、GPT-4V奖励范式设计和强化学习微调。"
- "MotionPrefer数据集包含5,276个提示和47.1K个动作样本，是首个提供完整性、时间顺序和频率三个细粒度维度标注的偏好数据集。"
- "在时间顺序任务上，AToM的MM Dist从5.652降至5.576，FID从0.655降至0.613（相比于MotionGPT）。"
- "人类评估显示AToM在三个子任务上的胜率分别为74.4%（时间）、70.0%（频率）、84.4%（完整性）。"
---

# AToM: Aligning Text-to-Motion Model at Event-Level with GPT-4Vision Reward

> [!tip] 核心洞察
> 通过设计任务相关提示并让GPT-4V对生成的多个动作序列进行三个维度（完整性、时间、频率）评分，构建细粒度偏好数据集MotionPrefer，使用该数据集以LoRA和IPO损失对MotionGPT进行微调，能够显著提升文本-动作生成的事件级对齐质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | AToM：基于GPT-4Vision奖励的事件级文本-动作对齐框架 |
| 英文题名 | AToM: Aligning Text-to-Motion Model at Event-Level with GPT-4Vision Reward |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2501.05557) · [Project](https://atom-motion.github.io/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | AToM |
| Dataset | Temporal (时间顺序), Temporal, Human evaluation (Temporal), Human evaluation (Frequency) |

> [!tip] 效果简介
> - Temporal (时间顺序) 上，MM Dist (↓) 为 5.576，对比 5.652 (MotionGPT)，变化 -0.076。
> - Temporal 上，FID (↓) 为 0.613，对比 0.655 (MotionGPT)，变化 -6.4%。
> - Human evaluation (Temporal) 上，Win rate vs MotionGPT 为 AToM 74.4%，对比 MotionGPT 25.6% (隐含)，变化 +48.8%。

## 概述

### 问题瓶颈

文本驱动的动作生成模型已在通用场景下取得了显著进展，但在**细粒度事件级对齐**上仍存在明显短板。具体表现为三个方面：**动作完整性**（生成的动作是否完整覆盖文本中的所有子动作）、**时间顺序**（动作执行顺序是否与文本描述一致）以及**动作频率**（重复动作的次数是否匹配）。现有方法如**MotionGPT**（Jiang et al., NeurIPS 2023）主要依赖粗粒度的条件生成训练，缺乏针对上述维度的显式优化信号，导致模型在复杂时序描述下的生成质量不可靠。同时，高质量、细粒度的偏好数据严重匮乏，现有偏好数据集要么规模极小，要么仅提供整体性评分，无法支撑事件级的精细化对齐训练。

### 核心方法

**AToM** 提出了一种基于视觉-语言大模型奖励的事件级文本-动作对齐框架，核心思路是利用 **GPT-4Vision** 自动生成细粒度的对齐评分，并以此为奖励信号通过强化学习微调基础动作生成模型。整个框架由三个阶段构成：

1. **数据集构建**：通过 GPT-4 按任务类型（完整性、时间顺序、频率）生成多样化文本提示，再经 MotionGPT 生成多个候选动作序列，形成初始的文本-动作对。
2. **GPT-4V 奖励标注**：将动作序列渲染为视频，以固定帧间隔采样为静态图像序列，输入 GPT-4V 进行三维度（完整性、时间顺序、频率）对齐评分，构建细粒度偏好数据集 **MotionPrefer**（包含 5,276 个提示和 47.1K 个动作样本）。
3. **强化学习微调**：基于 MotionPrefer 中的偏好对，采用 **IPO 损失**（Identity Preference Optimization）结合 **LoRA** 参数高效微调策略，对 MotionGPT 进行优化，使模型在事件级对齐维度上产生显著提升。

### 方法谱系与知识库定位

AToM 处于**文本-动作生成**与**基于人类/大模型反馈的强化学习微调**的交叉点。其直接基线包括：

- **MotionGPT**（Jiang et al., NeurIPS 2023）：预训练文本-动作生成模型，作为微调基线和主要对比对象，不包含显式的事件级对齐机制。
- **InstructMotion**（Sheng et al., CVPR 2024）：首个基于 RLHF 的文本-动作对齐方法，但依赖人工标注的粗粒度偏好信号，数据规模和细粒度程度均受限。

AToM 的关键差异化在于：用 GPT-4V **自动标注**替代人工标注，实现了**三维度细粒度偏好数据**的大规模构建，并通过 **IPO + LoRA** 的微调策略在参数效率和对齐效果之间取得平衡。这一技术路线与当前“利用大模型作为自动评估器/标注器，再以强化学习微调生成模型”的范式（如 InstructGPT、DPO 系列）一脉相承，但在动作生成这一特定模态上首次实现了事件级细粒度对齐的系统性方案。

### 主要结果

在时间顺序、动作频率、动作完整性三个子任务上，AToM 相对于 MotionGPT 均取得了显著提升：

- **自动化指标**：在时间顺序任务上，MM Dist 从 5.652 降至 5.576，FID 从 0.655 降至 0.613（降幅 6.4%）。
- **人类评估**：AToM 在三个子任务上的胜率分别达到 **74.4%**（时间顺序）、**70.0%**（频率）和 **84.4%**（完整性），表明人类评估者强烈偏好 AToM 的生成结果。
- **消融实验**：LoRA 微调使 MM Dist 从 6.425 降至 5.576，FID 从 2.131 降至 0.613，top-1 检索准确率从 0.128 提升至 0.199（提升 55.5%）；IPO 损失策略在 FID 指标上优于 DPO 等替代方案；逐帧图像序列输入和适当的帧采样间隔（8 帧）对 GPT-4V 评分质量至关重要。

### 局限与开放问题

当前验证仅限于 HumanML3D 数据集和 MotionGPT 单一模型架构，对其他数据集和扩散模型（如 MDM、MLD）的泛化性未知。GPT-4V 的评分准确性与人类判断的系统相关性尚未量化，且依赖商业 API 带来了成本与可复现性问题。此外，对于包含更多动作事件或更长序列的复杂描述，事件级对齐性能的退化程度尚待探索。如何进一步降低对闭源大模型的依赖，实现完全开源可复现的训练流程，是该方向的重要开放挑战。

## 背景与动机

文本驱动的三维人体动作生成旨在根据自然语言描述合成逼真且语义一致的人体运动序列。随着扩散模型与自回归语言模型的发展，如**MotionGPT**（Jiang et al., NeurIPS 2023）等方法在整体动作质量上取得了显著进展。然而，现有模型普遍存在一个关键瓶颈：**细粒度的事件级对齐能力不足**。

具体而言，当文本描述涉及多个动作事件的组合时（如“先走两步，再跳起来转身”），模型往往难以准确捕捉三个核心维度：

1. **动作完整性**：是否覆盖了文本中所有提及的动作事件。
2. **时间顺序**：动作事件的执行顺序是否与文本描述一致。
3. **频率**：重复性动作的次数是否与文本匹配（如“拍手三次”）。

这一瓶颈的根源在于两个层面。其一，预训练阶段使用的文本-动作数据缺乏针对上述维度的细粒度标注，模型无法从现有监督信号中学习到事件级的语义对应关系。其二，该领域长期缺乏高质量、多维度的偏好数据，使得直接通过强化学习优化事件级对齐变得困难。尽管**InstructMotion**（Sheng et al., CVPR 2024）首次将基于人类反馈的强化学习引入文本-动作对齐任务，但其依赖人工标注的粗粒度偏好信号，标注成本高且难以扩展到多维度细粒度评估。

为突破上述局限，AToM提出利用视觉-语言大模型GPT-4Vision的细粒度理解能力，自动构建包含完整性、时间顺序和频率三维度评分的偏好数据集，并据此对基础动作生成模型进行强化学习微调，从而系统性地提升事件级对齐质量。

## 核心创新

AToM 的核心创新在于首次将**视觉-语言大模型（GPT-4Vision）引入文本-动作生成的细粒度事件级对齐优化**，通过三个紧密耦合的“changed slots”实现了从数据构建到模型优化的闭环。

### 1. 细粒度三维度偏好数据自动构建

现有文本-动作生成模型（如 **MotionGPT**, Jiang et al., NeurIPS 2023）缺乏专门的事件级偏好数据，而首个基于 RLHF 的方法 **InstructMotion**（Sheng et al., CVPR 2024）仅依赖人工标注的粗粒度整体偏好信号。AToM 的关键突破在于：

- **利用 GPT-4 自动生成任务相关的多样化文本提示**：针对完整性、时间顺序、频率三个事件级维度，通过设计任务标签和连词集合，引导 GPT-4 生成覆盖广泛语义的提示数据集 $\mathbb{D}_{\mathrm{prompt}}$（Section 3.1, Equation 1）。
- **利用 GPT-4Vision 进行三维度细粒度评分**：将 MotionGPT 生成的多个候选动作序列渲染为视频，以每 8 帧为间隔采样为静态帧序列 $F$，输入 GPT-4Vision，根据任务特定的评分规则（Table 4）对动作-文本对齐程度进行三个维度的独立打分，生成奖励信号 $\mathbb{D}_{\mathrm{reward}}$（Section 3.2, Equation 5）。
- **构建首个细粒度偏好数据集 MotionPrefer**：整合动作序列、文本描述和三维度评分，形成包含 5,276 个提示和 47.1K 个动作样本的偏好数据集 $\mathbb{D}_{\mathrm{motionprefer}}$（Table 3）。与现有数据集（Table 1）相比，MotionPrefer 首次提供了完整性、时间顺序和频率三个细粒度维度的标注，填补了该领域的空白。

### 2. 基于 GPT-4Vision 奖励信号的强化学习微调

AToM 将 GPT-4Vision 的细粒度评分转化为可优化的奖励信号，并通过强化学习驱动模型的事件级对齐能力提升：

- **偏好对构造策略**：从 MotionPrefer 中按子任务筛选，对同一提示下的动作对，仅当评分差超过阈值 $\delta$ 时才纳入训练集 $D$，确保偏好信号的可靠性（Section 3.3, Algorithm 1）。消融实验证实，仅保留评分高于 3 的样本作为正例，可使 MM Dist 从 5.640 降至 5.576，FID 从 0.693 降至 0.613（Table 6b）。
- **IPO 损失优化**：采用 IPO（Identity Preference Optimization）损失函数 $\mathbb{E}_{(m_w, m_l, p) \sim D} \left( h_{\pi}(m_w, m_l, p) - \frac{1}{2\beta} \right)^2$，其中 $h_{\pi}$ 为获胜动作与失败动作的对数概率比率（Section 3.3, Equation 8）。相比 DPO 等其他 RL 策略，IPO 在 FID 指标上表现更优（Figure 5）。
- **参数高效微调**：通过 LoRA 对 MotionGPT 进行微调，以极少的计算资源实现显著性能提升。消融实验表明，LoRA 微调使 MM Dist 从 6.425 降至 5.576，FID 从 2.131 降至 0.613，top-1 准确率从 0.128 提升至 0.199（Table 6c）。

### 3. 事件级对齐的因果机制

AToM 的性能提升源于一个清晰的因果链条：**GPT-4Vision 提供了传统自动指标无法捕捉的事件级语义对齐信号**，而 IPO 强化学习将这一信号有效注入生成模型。具体表现为：

- 在时间顺序任务上，AToM 的 MM Dist 从 MotionGPT 的 5.652 降至 5.576，FID 从 0.655 降至 0.613（Table 5）。
- 人类评估中，AToM 在时间、频率、完整性三个子任务上的胜率分别达到 74.4%、70.0% 和 84.4%（Figure 4），证明 GPT-4Vision 奖励信号与人类判断高度一致。

### 创新边界与待验证问题

AToM 的创新目前受限于以下边界条件，需在实际应用中审慎评估：

- **模型与数据集的泛化性**：仅在 HumanML3D 数据集和 MotionGPT 模型上验证，对其他运动生成架构（如扩散模型 MDM、MLD）的适用性未知。
- **GPT-4Vision 评分的可靠性**：评分准确性和一致性与人类标注的系统对比尚未进行，可能存在未知偏差。
- **商业 API 依赖**：框架依赖闭源的 GPT-4V API，存在成本、可复现性和访问稳定性的问题，如何实现完全开源的训练流程仍是开放问题。
- **细粒度维度的覆盖范围**：当前仅聚焦三个事件级维度，未涉及运动风格、情感等其他细粒度属性。

## 整体框架

AToM 框架由三个顺序衔接的阶段构成，形成一条从数据构建到模型优化的闭环流水线（Figure 2）。

![[assets/figures/papers/paper_list_l2_AToM_Aligning_Text_to_Motion_Model_at_Event_Level_with_GPT_4Vision_Rewar/figures/003_Figure_2.jpg]]
*Figure 2: The framework of AToM. AToM encompasses three stages: (1) A motion generation process using task-specific prompts constructed by LLM; (2) Evaluation of alignment score for text-motion pairs using a predefined reward paradigm based on LVLM; (3) A fine-tuning mechanism based on LoRA and RL strategy that enhances the original motion generator using the dataset MotionPrefer*

**第一阶段：合成数据构建。** 框架首先利用 GPT-4 作为提示构建器，根据任务标签（时间顺序、频率、完整性）和连词集合生成多样化的文本提示集 $\mathbb{D}_{\mathrm{prompt}}$。这些提示被送入预训练的动作生成器 MotionGPT，为每条提示生成多个候选动作序列，形成初始的动作-文本对集合 $\mathbb{D}_{\mathrm{motion}}$。这一阶段的输出是未经标注的合成数据池，为后续偏好标注提供了原始素材。

**第二阶段：GPT-4Vision 奖励标注。** 动作序列通过渲染器转换为视频 $\mathbb{D}_{\mathrm{motion-video}}$，随后以 8 帧为间隔采样为静态帧序列 $F$。这些帧序列与对应的文本提示以及任务特定的评分规则（Table 4）一同输入 GPT-4Vision，由视觉-语言大模型在完整性、时间顺序和频率三个维度上评估动作与文本的对齐程度，输出奖励分数 $\mathbb{D}_{\mathrm{reward}}$。最终构建出包含动作序列、文本描述和三维度评分的偏好数据集 $\mathbb{D}_{\mathrm{motionprefer}}$（MotionPrefer），总计 5,276 条提示和 47.1K 个动作样本（Table 3）。

**第三阶段：强化学习微调。** 从 MotionPrefer 中按子任务筛选数据，将同一提示下的动作序列按评分差阈值 $\delta$ 配对，构建偏好训练集 $D$。在 MotionGPT 上引入 LoRA 进行参数高效微调，优化目标为 IPO（Identity Preference Optimization）损失函数：

$$\mathbb{E}_{(m_w, m_l, p) \sim D} \left( h_{\pi}(m_w, m_l, p) - \frac{1}{2\beta} \right)^2$$

其中 $h_{\pi}$ 为策略模型 $\pi$ 与参考模型 $\pi_{ref}$ 在胜者动作 $m_w$ 和败者动作 $m_l$ 上的对数概率比率。这一阶段的核心机制在于：GPT-4Vision 提供的事件级细粒度奖励信号通过 IPO 损失反向传导至动作生成器，使其学会在三个事件维度上更好地对齐文本描述。

**模块间的数据流关系：** 提示构建器 → MotionGPT 动作生成器 → 动作渲染与帧采样器 → GPT-4V 评分器 → 偏好数据构造算法 → LoRA 微调 + IPO RL。整个流水线中，GPT-4Vision 的评分环节是连接数据构建与模型优化的关键瓶颈——其评分质量直接决定了偏好数据的可靠性和最终微调效果的上限。

## 核心模块与公式推导

AToM框架由三个顺序衔接的核心模块构成，形成“数据构建→奖励标注→偏好优化”的闭环，其整体流程如Figure 2所示。

**模块一：GPT-4提示构建器与MotionGPT动作生成器（数据构建阶段）**

该模块负责构建细粒度偏好数据集的原始素材。首先，针对时间顺序（Temporal）、动作频率（Frequency）和动作完整性（Integrity）三个事件级子任务，利用GPT-4根据任务标签 $\mathrm{X}_{\mathrm{task}}$ 和连词集合 $\mathrm{X}_{\mathrm{conj}}$ 生成多样化的文本提示：

$$\mathbb{D}_{\mathrm{prompt}} \sim \mathrm{M}_{\mathrm{Language}}(\mathrm{I}_{\mathrm{prompt}} | \mathrm{X}_{\mathrm{task}}, \mathrm{X}_{\mathrm{conj}}) \tag{1}$$

其中 $\mathrm{I}_{\mathrm{prompt}}$ 为任务特定的提示构建指令（示例见Table 2）。随后，将生成的提示集 $\mathbb{D}_{\mathrm{prompt}}$ 输入预训练的文本-动作生成模型MotionGPT，为每条提示生成多个候选动作序列：

$$\mathbb{D}_{\mathrm{motion}} \sim \mathrm{M}_{\mathrm{Motion}}(\mathbb{D}_{\mathrm{prompt}}) \tag{2}$$

**模块二：动作渲染与帧采样器 + GPT-4V评分器（奖励标注阶段）**

此模块将动作序列转化为视觉-语言大模型可理解的表示，并获取细粒度对齐评分。首先，将动作数据 $\mathbb{D}_{\mathrm{motion}}$ 渲染为视频序列：

$$\mathbb{D}_{\mathrm{motion-video}} \sim \mathrm{R}_{\mathrm{motion}}(\mathbb{D}_{\mathrm{motion}}) \tag{3}$$

随后以8帧为间隔对视频进行采样，提取静态帧序列 $F$：

$$F = \{f_0, f_8, \dots\} = \mathrm{Sampler}(\mathbb{D}_{\mathrm{motion-video}}, 8) \tag{4}$$

将帧序列 $F$、原始文本提示及任务特定的评分规则 $\mathrm{I}_{\mathrm{score}}$（详见Table 4）输入GPT-4V，由视觉-语言大模型评估动作与文本在对应维度上的对齐程度，输出奖励分值：

$$\mathbb{D}_{\mathrm{reward}} = \mathrm{M}_{\mathrm{VL}}\left((F, \mathbb{D}_{\mathrm{prompt}}), \mathrm{I}_{\mathrm{score}}\right) \tag{5}$$

由此构成包含动作、文本、评分的三元组偏好数据集：

$$\mathbb{D}_{\mathrm{motionprefer}} = \{\mathbb{D}_{\mathrm{motion}}, \mathbb{D}_{\mathrm{prompt}}, \mathbb{D}_{\mathrm{reward}}\} \tag{6}$$

**模块三：偏好数据构造算法 + LoRA微调与IPO强化学习（偏好优化阶段）**

基于 $\mathbb{D}_{\mathrm{motionprefer}}$，通过算法1构造用于强化学习的偏好对训练集 $D$：针对每个子任务，按提示分组后，仅选取评分差超过阈值 $\delta$ 的动作对作为正例（胜者 $m_w$）和负例（败者 $m_l$），并过滤掉评分低于3的低质量样本。

微调采用参数高效的LoRA策略，优化目标为IPO（Identity Preference Optimization）损失。定义策略模型 $\pi$ 与参考模型 $\pi_{ref}$ 的对数概率比率函数：

$$h_{\pi}(m_w, m_l, p) = \log\left(\frac{\pi(m_w|p)\pi_{ref}(m_l|p)}{\pi(m_l|p)\pi_{ref}(m_w|p)}\right) \tag{7}$$

IPO损失函数最小化 $h_{\pi}$ 与目标值 $\frac{1}{2\beta}$ 的平方误差：

$$\mathbb{E}_{(m_w, m_l, p) \sim D} \left( h_{\pi}(m_w, m_l, p) - \frac{1}{2\beta} \right)^2 \tag{8}$$

其中 $\beta$ 为控制偏好强度的超参数。该损失直接对偏好对进行优化，避免了传统RLHF中显式奖励建模的中间步骤。

**关键设计决策的因果机制：**
- **逐帧采样（8帧间隔）**：消融实验（Figure 6）表明，较短的采样间隔（4或8帧）在匹配距离和top-1准确率上优于16帧，8帧在信息完整性与计算开销间取得最佳平衡。
- **评分过滤机制**：仅保留评分高于3的样本作为正例，可有效剔除GPT-4V判定为低质量的生成结果，使MM Dist从5.640降至5.576，FID从0.693降至0.613（Table 6b）。
- **LoRA微调**：相比全量微调或无微调，LoRA在保持参数效率的同时显著提升检索准确率（top-1从0.128提高到0.199）并大幅降低FID（从2.131降至0.613）（Table 6c）。
- **IPO vs. DPO**：在相同条件下，IPO损失在FID指标上优于DPO（Figure 5），表明其对偏好分布的建模更适合本任务的优化目标。

## 实验与分析

### 核心瓶颈与因果机制

当前文本-动作生成模型（如MotionGPT）在细粒度事件级对齐上存在显著短板，具体表现为三个维度：**动作完整性**（是否遗漏或冗余动作）、**时间顺序**（动作先后关系是否正确）、**动作频率**（重复次数是否匹配）。其根本瓶颈在于缺乏高质量、多维度的偏好数据来指导模型优化。AToM通过引入视觉-语言大模型GPT-4V作为自动评分器，构建了首个覆盖上述三维度的细粒度偏好数据集MotionPrefer，并利用IPO强化学习损失对MotionGPT进行LoRA微调，从而直接提升事件级对齐质量。

### 主实验结果

#### 定量评估

Table 5展示了AToM在时间顺序（Temporal）、动作频率（Frequency）、动作完整性（Integrity）三个子任务以及通用任务（General）上的自动化指标对比。在时间顺序任务上，AToM将MM Dist从MotionGPT的5.652降至**5.576**，FID从0.655降至**0.613**（降幅6.4%），top-1检索准确率从0.128提升至**0.199**。在通用任务上，AToM取得了最低的MM Dist（**3.943**）和最优的FID（**0.177**），验证了事件级对齐优化对整体生成质量的正面溢出效应。

值得注意的是，AToM♠（将三个子任务的偏好数据混合后随机抽取约3.5K对，以匹配InstructMotion的数据规模）在通用任务上同样优于InstructMotion，确保了与现有RLHF方法的公平对比。

#### 人类评估

Figure 4报告了人类判断下AToM相对于MotionGPT的胜率。在三个子任务上，AToM分别取得了**74.4%**（时间顺序）、**70.0%**（动作频率）和**84.4%**（动作完整性）的胜率，其中完整性任务的提升最为显著（+68.8个百分点），表明GPT-4V在该维度上的评分信号与人类偏好高度一致。

![[assets/figures/papers/paper_list_l2_AToM_Aligning_Text_to_Motion_Model_at_Event_Level_with_GPT_4Vision_Rewar/figures/008_Figure.jpg]]

![[assets/figures/papers/paper_list_l2_AToM_Aligning_Text_to_Motion_Model_at_Event_Level_with_GPT_4Vision_Rewar/figures/009_Figure.jpg]]

#### 定性分析

Figure 3提供了预训练MotionGPT与微调后AToM的生成样例对比。在完整性任务中，MotionGPT倾向于遗漏提示中的部分动作，而AToM能够完整复现所有指定动作；在时间顺序任务中，AToM生成的动作序列严格遵循文本描述的时间先后关系；在频率任务中，AToM对动作重复次数的控制更为精确。

### 消融实验

Table 6系统分析了三个关键设计选择的影响：

**(a) 运动注入方式：** 对比了静态图像、视频和逐帧图像序列三种GPT-4V输入表示。逐帧图像序列（Frame-by-Frame）在MM Dist（5.576）、top-1准确率（0.199）和FID（0.613）上均表现最优，验证了细粒度帧级信息对事件级对齐评估的必要性。

**(b) 评分过滤：** 在构建偏好对时，仅保留评分高于3分的样本作为正例（w/ Score Filtering），相比无过滤策略，MM Dist从5.640进一步降至**5.576**，FID从0.693降至**0.613**，表明过滤低质量样本可有效提升训练信号的纯度。

**(c) LoRA微调：** 引入LoRA进行参数高效微调，相比全量微调或无微调，top-1准确率从0.128跃升至**0.199**，FID从2.131骤降至**0.613**，同时MM Dist从6.425降至5.576。这一结果说明LoRA在保持预训练知识的同时，能够有效吸收偏好优化信号。

Figure 5对比了不同强化学习策略的微调效果。IPO损失在FID指标上优于DPO等替代方案，验证了IPO在偏好优化场景下的稳定性优势。

Figure 6探索了帧采样间隔的影响。较短的采样间隔（4帧或8帧）在匹配距离和top-1准确率上显著优于16帧间隔，最终选择8帧作为计算效率与对齐精度的最佳平衡点。

### 失败模式与局限性

尽管AToM在事件级对齐上取得了显著提升，但存在以下局限：

1. **泛化边界未验证：** 所有实验均在HumanML3D数据集和MotionGPT模型上进行，该框架在其他数据集（如KIT-ML）或其他架构（如MDM、MLD等扩散模型）上的迁移能力未知。
2. **评分可靠性未标定：** GPT-4V的评分准确性和一致性与人类标注的系统对比缺失，可能存在系统性偏差，尤其是在边界模糊的样本上。
3. **维度覆盖有限：** 实验聚焦于完整性、时间顺序和频率三个维度，未涉及运动风格、情感表达等其他细粒度属性，事件级对齐的完整图景有待扩展。
4. **API依赖风险：** 框架依赖商业闭源API（GPT-4V），存在成本波动、访问稳定性及可复现性问题，限制了大规模部署和开源社区的直接复现。

### 开放问题

- GPT-4Vision的评分与人类判断在事件级对齐上的相关性如何？缺乏系统的人机一致性研究。
- AToM框架能否应用于扩散模型（如MDM、MLD）或其他运动生成架构？
- 对于包含更多动作事件或更长序列的复杂描述，事件级对齐性能的退化程度如何？
- Pick-a-Move数据集的确切数据量未见公开，其与MotionPrefer的公平对比有待验证。
- 如何进一步降低对闭源大模型API的依赖，实现完全开源的训练流程？

### 补充图表

![[assets/figures/papers/paper_list_l2_AToM_Aligning_Text_to_Motion_Model_at_Event_Level_with_GPT_4Vision_Rewar/figures/011_Figure_4.jpg]]
*Figure 4: Win rates of AToM fine-tuned compared to MotionGPT by human judgments in three tasks. Figure 5. Performance distribution of different reinforcement learning strategies after generative model finetuning*

![[assets/figures/papers/paper_list_l2_AToM_Aligning_Text_to_Motion_Model_at_Event_Level_with_GPT_4Vision_Rewar/figures/010_Figure_3.jpg]]
*Figure 3: Generated qualitative samples comparison of pretrained model MotionGPT and finetuned model AToM*

![[assets/figures/papers/paper_list_l2_AToM_Aligning_Text_to_Motion_Model_at_Event_Level_with_GPT_4Vision_Rewar/figures/002_Table_1.jpg]]
*Table 1: Statistics of existing preference datasets for text-tomotion generative models. “Fine Grained” represents containing preference regarding multiple aspects or not*

![[assets/figures/papers/paper_list_l2_AToM_Aligning_Text_to_Motion_Model_at_Event_Level_with_GPT_4Vision_Rewar/figures/005_Table_3.jpg]]
*Table 3: Details of amounts of MotionPrefer dataset*

![[assets/figures/papers/paper_list_l2_AToM_Aligning_Text_to_Motion_Model_at_Event_Level_with_GPT_4Vision_Rewar/figures/006_Table_4.jpg]]
*Table 4: Scoring rules for sub-tasks*

![[assets/figures/papers/paper_list_l2_AToM_Aligning_Text_to_Motion_Model_at_Event_Level_with_GPT_4Vision_Rewar/figures/007_Table_5.jpg]]
*Table 5: Comparison of AToM with baselines in different tasks. AToM♠ represents the process of mixing preference data from three tasks and randomly selecting a subset of preference data (approximately 3.5K pairs) that matches the size of the RLHF framework InstructMotion, ensuring fair comparison with the baseline model*

![[assets/figures/papers/paper_list_l2_AToM_Aligning_Text_to_Motion_Model_at_Event_Level_with_GPT_4Vision_Rewar/figures/012_Table_6.jpg]]
*Table 6: Ablation studies for motion injection methods, score filtering, and LoRA utilization on the test set*

## 方法谱系与知识库定位

### 1. 基线关系与差异化定位

AToM 的核心对标基线是 **MotionGPT**（Jiang et al., NeurIPS 2023），后者作为预训练文本-动作生成模型，同时也是 AToM 微调的起点。MotionGPT 采用原始条件生成训练范式，缺乏显式的事件级对齐机制和偏好优化信号。AToM 在其基础上引入了三个关键差异化模块：细粒度偏好数据构建、GPT-4Vision 自动奖励标注、以及基于 IPO 损失的强化学习微调。

与 **InstructMotion**（Sheng et al., CVPR 2024）——首个将 RLHF 引入文本-动作对齐的工作——相比，AToM 的差异化体现在两个层面。第一，偏好数据的粒度：InstructMotion 依赖人工标注的粗粒度整体偏好信号，而 AToM 通过 GPT-4Vision 自动生成覆盖完整性、时间顺序和频率三个维度的细粒度评分。第二，数据规模与公平性：AToM♠ 变体将三个子任务的偏好数据混合后随机抽取约 3.5K 对，以匹配 InstructMotion 的数据规模，确保在同等条件下进行公平对比。

### 2. 方法谱系中的位置

AToM 处于“视觉-语言大模型驱动的生成模型对齐”这一交叉地带。其方法谱系上游包括：

- **运动生成模型**：以 MotionGPT 为代表的基于 VQ-VAE 和语言模型架构的文本-动作生成方法；
- **偏好优化方法**：IPO（Identity Preference Optimization，Azar et al., 2024）作为 RLHF 的变体，相较于 DPO 在 AToM 的 FID 指标上表现更优；
- **视觉-语言大模型应用**：GPT-4Vision 作为自动评估器，替代人工标注提供奖励信号。

下游可扩展方向包括：将该框架应用于扩散模型（如 MDM、MLD）或其他运动生成架构，以及探索更细粒度的属性对齐（如运动风格、情感）。

### 3. 适用边界与局限

**适用边界**：
- 当前验证范围限于 **HumanML3D 数据集**和 **MotionGPT 模型**，泛化到其他数据集和运动生成架构的性能未知；
- 实验聚焦于三个特定的事件级维度（完整性、时间顺序、频率），未涉及其他细粒度属性；
- 依赖商业 API（GPT-4Vision），存在成本、可复现性和访问稳定性的约束。

**已知局限**：
- GPT-4Vision 的评分准确性和一致性与人类标注的系统对比尚未开展，可能存在系统性偏差；
- 对于包含更多动作事件或更长序列的复杂描述，事件级对齐性能的退化程度未经验证；
- 完全开源的训练流程尚未实现，对闭源大模型 API 的依赖构成可复现性瓶颈。

### 4. 开放问题

1. **评分可靠性**：GPT-4Vision 的评分与人类判断在事件级对齐上的相关性如何？这是决定该方法能否替代人工标注的关键问题。
2. **架构泛化**：AToM 框架能否应用于扩散模型（如 MDM、MLD）或其他运动生成架构？当前仅验证了基于语言模型的 MotionGPT。
3. **复杂度扩展**：对于包含更多动作事件或更长序列的复杂描述，事件级对齐性能的退化程度如何？需要进一步实验验证。
4. **开源可行性**：如何进一步降低对闭源大模型 API 的依赖，实现完全开源的训练流程？这是社区推广的重要前提。
5. **数据公平性**：Pick-a-Move 数据集的确切数据量未见公开，其与 MotionPrefer 的公平对比有待验证。

## 原文 PDF

![[paperPDFs/CVPR_2025/AToM_Aligning_Text_to_Motion_Model_at_Event_Level_with_GPT_4Vision_Reward.pdf]]
