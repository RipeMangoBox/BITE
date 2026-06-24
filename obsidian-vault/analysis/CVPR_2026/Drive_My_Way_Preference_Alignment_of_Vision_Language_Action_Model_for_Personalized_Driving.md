---
title: "Drive My Way: Preference Alignment of Vision-Language-Action Model for Personalized Driving"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Drive_My_Way_Preference_Alignment_of_Vision_Language_Action_Model_for_Personalized_Driving.pdf
project_link: "https://dmw-cvpr.github.io/"
code_link: null
aliases:
- DMWD
- DMWPAVLAMPD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过用户嵌入（编码长期驾驶习惯）和风格感知动态奖励权重（响应短期指令）调节策略输出。
primary_logic: 利用对比学习将驾驶员档案与历史驾驶行为嵌入到共享潜在空间，通过条件化策略实现长期偏好对齐；引入残差动作解码器和风格感知的强化微调，使模型能够根据实时自然语言指令动态调整安全性、效率和舒适性之间的权衡。
claims:
- DMW 学习用户嵌入以编码长期驾驶行为，并在规划时将其作为策略的条件。
- 通过风格感知的强化微调，使用在安全性、舒适性和效率之间动态调整权重的奖励函数，实现实时适应。
- 在 Bench2Drive 上，DMW 在保守指令下取得最大 DS 和 SR 增益，同时在激进指令下实现 18.77% 的效率提升。
- 用户研究表明 DMW 生成的驾驶行为可被识别为每位驾驶员自己的风格，且对齐评分显著高于多目标基线 MORL-PD。
---

# Drive My Way: Preference Alignment of Vision-Language-Action Model for Personalized Driving

> [!tip] 核心洞察
> 利用对比学习将驾驶员档案与历史驾驶行为嵌入到共享潜在空间，通过条件化策略实现长期偏好对齐；引入残差动作解码器和风格感知的强化微调，使模型能够根据实时自然语言指令动态调整安全性、效率和舒适性之间的权衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | Drive My Way：面向个性化驾驶的视觉-语言-动作模型的偏好对齐 |
| 英文题名 | Drive My Way: Preference Alignment of Vision-Language-Action Model for Personalized Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.25740) · [Project](https://dmw-cvpr.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Drive My Way (DMW) |
| Dataset | Bench2Drive, Personalized Driving Dataset, User Study |

> [!tip] 效果简介
> - Bench2Drive 上，Driving Score (Conservative style) 82.72 vs 78.18 (SimLingo) (+4.54)；Efficiency (Aggressive style) 281.56 vs 247.60 (SimLingo) (+33.96 (+13.7%))。
> - Personalized Driving Dataset (PDD) 上，Alignment Score (ID drivers D1/D2) 0.92 / 0.92 vs 0.42 / 0.58 (MORL-PD) (+0.50 / +0.34)。
> - User Study (Emergency Scenario) 上，Average Rating (Aggressive instruction) DMW ~8.4 (average of E1-E5) vs SimLingo ~7.1 (average of E1-E5) (Significantly higher)。

## 概述

### 问题背景与瓶颈

端到端自动驾驶系统近年来取得了显著进展，但其优化目标仍集中于通用驾驶能力或依赖固定的驾驶模式。这种“一刀切”的范式存在一个根本性瓶颈：**系统无法适应不同驾驶员的个人偏好，也难以响应自然语言表达的实时驾驶意图**。例如，一位习惯平稳跟车的驾驶员与一位偏好果断超车的驾驶员，对同一交通场景的期望行为截然不同。现有方法要么完全忽略驾驶员个性化，要么仅将指令映射到预定义的激进/中性/保守模式，缺乏对长期驾驶习惯的建模和对短期指令的灵活响应能力。

### 核心思路

**Drive My Way (DMW)** 提出了一种视觉-语言-动作（VLA）模型的偏好对齐框架，通过两个互补机制实现端到端的个性化驾驶：

1. **长期偏好对齐**：从驾驶员的文本档案（描述年龄、驾龄、驾驶风格偏好等）中学习用户嵌入，利用对比学习将该嵌入与历史驾驶行为嵌入对齐到共享潜在空间。规划时，VLA 策略以用户嵌入为条件，使模型持续输出符合该驾驶员长期习惯的行为。

2. **短期指令适应**：引入风格感知的动态奖励函数，通过大语言模型（LLM）根据场景上下文和用户指令推断安全性、效率、舒适性三个维度的奖励权重，经专家审核后用于强化微调。这使得模型能够在同一场景下，根据“请快速超车”或“请保持安全距离”等自然语言指令实时调整行为权衡。

技术上，DMW 在 SimLingo VLA 主干的基础上增加了残差动作解码器：基础动作由运动预测器从路点导出，个性化残差（离散的速度和转向调整量）通过可学习的查询与 MLP 头输出，二者相加得到最终控制量。这种设计在保留安全规划能力的同时，实现了轻量级的个性化微调。

### 方法谱系与知识库定位

DMW 处于 **VLA 端到端自动驾驶** 与 **人类偏好对齐** 的交叉点。其方法定位如下：

- **VLA 主干**：基于 **SimLingo**（语言引导的端到端规划器），继承其视觉-语言融合和路点预测能力。
- **个性化基线对比**：
  - **StyleDrive**：将指令映射到固定风格模式，缺乏长期偏好建模和动态权重调整。
  - **MORL-PD**：多目标强化学习个性化方法，以驾驶员偏好向量为条件，但未利用自然语言档案和对比学习。
  - **DMW-Vanilla**：DMW 的消融变体，使用固定奖励权重替代风格感知动态权重。
- **关键技术来源**：对比学习采用 InfoNCE 损失（借鉴 SimCLR 等表征学习范式）；强化微调采用 GRPO（Group Relative Policy Optimization）；用户档案编码基于 DeBERTaV3 语言模型。

### 关键结果摘要

在 Bench2Drive 闭环评测中，DMW 在保守指令下取得 **82.72** 的 Driving Score（较 SimLingo 的 78.18 提升 +4.54），在激进指令下实现 **281.56** 的效率指标（较 SimLingo 的 247.60 提升 13.7%）。用户研究表明，DMW 生成的驾驶行为可被识别为每位驾驶员自己的风格，对齐评分显著高于 MORL-PD（ID 驾驶员上达到 0.92 vs. 0.42–0.58）。消融实验证实，风格感知动态权重是区分不同指令下驾驶行为的关键，而自适应平均池化对保持用户嵌入的多样性至关重要。

### 局限与开放问题

当前工作主要在 CARLA 仿真环境中验证，个性化数据集仅覆盖 30 名驾驶员和 20 种场景。风格感知奖励的生成依赖 LLM 推理与专家审核，扩展至大规模用户时面临可扩展性挑战。此外，模型无法处理训练集之外的全新驾驶风格或极端偏好，sim-to-real 迁移、跨文化适应性、用户意图模糊性等问题仍需进一步探索。

## 背景与动机

端到端自动驾驶系统近年来取得了显著进展，特别是视觉-语言-动作（VLA）模型的出现，使得车辆能够理解自然语言指令并生成相应的驾驶动作。然而，现有系统面临一个根本性瓶颈：它们仅优化通用的驾驶目标（如安全到达目的地），或依赖固定的驾驶模式（如“激进”、“保守”），缺乏对**个人驾驶偏好**和**自然语言意图**的真正适应能力。

这一缺口在实际驾驶场景中尤为突出。不同驾驶员对安全性、效率和舒适性之间的权衡存在显著差异——例如，一位驾驶员可能倾向于保持较大跟车距离并平缓变道，而另一位则偏好更紧凑的跟车和果断的超车。现有系统无法捕捉这种长期形成的个人驾驶风格，也无法根据实时的自然语言指令（如“我赶时间，请快一点”或“今天不着急，开稳一些”）动态调整驾驶行为。

从技术层面看，现有方法的不足体现在三个关键维度：

1. **缺乏用户特定条件化**：当前 VLA 策略不区分驾驶员身份或历史行为，对所有用户输出相同的驾驶策略。
2. **动作空间缺乏个性化机制**：驾驶动作直接从通用运动规划器导出，没有为个人风格调整预留空间。
3. **奖励信号缺乏风格感知**：训练过程中的奖励函数采用固定权重，无法根据上下文和用户指令动态调整安全性、效率和舒适性之间的权衡。

针对这些问题，**Drive My Way（DMW）**提出了一种端到端的个性化驾驶框架。其核心思路是：通过对比学习将驾驶员档案与历史驾驶行为嵌入到共享的潜在空间，利用用户嵌入作为策略的条件实现长期偏好对齐；同时引入残差动作解码器和风格感知的强化微调，使模型能够根据实时自然语言指令动态调整驾驶风格。这一设计使得 DMW 既能学习并复现驾驶员长期形成的驾驶习惯，又能灵活响应短期的风格指令，从而在保持安全性的前提下实现真正的个性化驾驶。

## 核心创新

Drive My Way (DMW) 的核心创新在于将**长期驾驶偏好**与**短期自然语言指令**统一到端到端视觉-语言-动作（VLA）策略中，使自动驾驶系统从“通用最优”走向“个性化适配”。相较于现有 VLA 骨干 **SimLingo** 仅进行语言引导的通用规划，以及 **StyleDrive** 将指令硬映射到预设的激进/中性/保守模式，DMW 通过三个相互耦合的机制实现了根本性突破。

**1. 用户嵌入驱动的长期偏好对齐**

DMW 引入了一个长期偏好编码器（基于 DeBERTaV3），将驾驶员的文本档案（如年龄、驾龄、风格自述）编码为连续的用户嵌入 $z_p^m$。同时，路线处理器通过时序多头自注意力机制从历史驾驶轨迹中提取行为嵌入 $z_{b,t}^m$。二者通过 InfoNCE 对比损失在共享潜在空间中对齐：

$$\mathcal{L}_t^m = -\log \frac{\exp\left(\text{sim}(z_p^m, z_{b,t}^m) / \tau\right)}{\sum_{j=1}^M \exp\left(\text{sim}(z_p^j, z_{b,t}^m) / \tau\right)}$$

这一设计的因果机制在于：**拉近同一驾驶员的档案语义与其实际行为表征，推远不同驾驶员之间的表征**，从而使学习到的用户嵌入能够编码驾驶员的长期习惯（如跟车距离偏好、变道果断程度）。该嵌入作为 VLA 策略的条件输入，使规划过程天然携带驾驶员身份信息——这是 **MORL-PD** 等仅依赖偏好向量的基线无法实现的细粒度对齐。

**2. 残差动作解码器实现安全约束下的个性化微调**

DMW 的动作输出采用了“基础动作 + 残差”的双通道架构。运动预测器从路点导出基础动作 $a_t^{\text{base}}$（油门、转向），保证安全导航的下限；残差解码器则通过可学习查询与 MLP 输出离散的速度变化和转向变化 $a_t^{\Delta}$，最终动作由二者叠加：

$$a_t \doteq a_t^{\text{base}} + a_t^{\Delta}$$

这一设计的核心洞察是：**个性化不应以牺牲安全为代价**。基础动作提供了由路点规划保障的安全轨迹，残差仅在安全边界内进行风格化调整。相比直接端到端输出个性化动作的方案，该解耦架构显著降低了强化微调过程中的策略崩溃风险，同时保持了风格调整的灵活性。

**3. 风格感知的动态奖励权重实现短期指令适应**

DMW 的强化微调采用 Group Relative Policy Optimization（GRPO），但其关键创新在于奖励函数的**风格感知动态权重机制**。总奖励由安全性、效率和舒适性三个分量加权构成：

$$\mathcal{R}(s_t, a_t) = w_s \cdot R_{\text{safety}} + w_e \cdot R_{\text{efficiency}} + w_c \cdot R_{\text{comfort}}$$

不同于 **DMW-Vanilla** 使用固定权重导致风格区分度丧失，DMW 利用 LLM 从场景描述和用户指令中推理出适配的权重与阈值（如安全性阈值 $\beta_{\text{safety}}$），并经专家审核精炼。例如，在“激进”指令下，效率权重 $w_e$ 被调高、舒适权重 $w_c$ 被压低，同时安全阈值适度放宽但仍保持下限约束。这一机制使同一策略网络能够根据实时指令在安全-效率-舒适的帕累托前沿上动态滑动，而非像 **StyleDrive** 那样在离散模式间僵硬切换。

**三个创新的协同效应**

上述三个 changed slot 并非孤立运作：用户嵌入提供了“谁在开车”的长期先验，残差解码器提供了“如何个性化”的安全动作空间，动态奖励权重提供了“此刻想要什么风格”的实时调节信号。三者在 VLA 策略中共同作用，使得 DMW 在 Bench2Drive 上同时实现了保守指令下的最高驾驶得分（DS 82.72 vs. SimLingo 78.18）和激进指令下 18.77% 的效率提升，且用户研究证实其生成的驾驶行为可被识别为驾驶员自身的风格——这是现有基线无法同时达成的能力组合。

## 整体框架

Drive My Way (DMW) 的整体框架围绕一个预训练的 VLA（视觉-语言-动作）骨干网络构建，通过两条互补的路径实现个性化驾驶：**长期偏好对齐**和**短期指令适应**。如 Figure 3 所示，系统接收多模态输入，经过一系列模块处理后输出最终的个性化控制动作。

![[assets/figures/papers/paper_list_l2383_https_arxiv_org_abs_2603_25740/figures/003_Figure_3.jpg]]
*Figure 3: An overview of the DMW framework with a pretrained VLA backbone. The model takes in front-view camera images, instructions, route target points, and user profile as inputs, while the motion predictor outputs route and speed waypoints, which derive the base action (throttle, steer angle). The residual decoder outputs a discrete residual applied to the base to produce the final personalized action*

### 输入层

框架的输入端包含四类信息：

- **前视图相机图像**：提供当前驾驶场景的视觉感知。
- **自然语言指令**：表达驾驶员短期的风格意图（如“开得激进一些”或“保持平稳舒适”）。
- **路径目标点**：来自导航系统的未来路径点序列，指示期望的行驶路线。
- **用户档案文本**：结构化的驾驶员偏好描述（如“偏好低速平稳驾驶”或“习惯快速变道”），用于编码长期驾驶习惯。

### 核心处理流程

整个处理流程可分为以下几个关键阶段：

**1. 感知编码与多模态融合**

前视图图像和自车状态信息首先通过感知编码器（Vision + Ego-state Encoder）转换为多模态 Token。这些 Token 与语言指令、路径目标点以及用户嵌入（User Embedding）一同输入 VLA 骨干网络。骨干网络采用 **SimLingo**（即 InternVL2-1B）架构，负责在语言引导下进行时空推理，并输出运动查询（Motion Queries）。

**2. 长期偏好编码**

用户档案文本经由一个基于 **DeBERTaV3** 的长期偏好编码器（Long-term Preference Encoder）处理，生成一个紧凑的用户嵌入向量。该嵌入编码了驾驶员的长期驾驶风格（如激进程度、舒适偏好等），并在规划阶段作为策略的条件输入，使模型能够“记住”特定驾驶员的习惯。用户嵌入通过对比学习（InfoNCE 损失）与驾驶员历史行为嵌入对齐，确保语义层面的偏好与实际的驾驶行为保持一致。

**3. 基础动作生成**

运动查询被送入运动预测器（Motion Predictor），输出路径路点和目标速度。这些路点经过 PID 控制器转换为基础动作 $a_t^{\text{base}}$（包括油门/刹车和转向角），形成一个安全但缺乏个性化的初始规划。

**4. 个性化残差叠加**

这是 DMW 实现个性化的关键机制。框架引入一个残差解码器（Residual Decoder），该模块由可学习查询、MLP 和分类头组成，接收 VLA 骨干网络的中间特征，输出离散的速度调整量和转向调整量作为残差 $a_t^{\Delta}$。最终执行的动作是基础动作与残差之和：

$$a_t \doteq a_t^{\text{base}} + a_t^{\Delta}$$

这种残差设计使得模型可以在保持基础安全规划的前提下，通过微调实现个性化控制，避免因过度个性化而破坏安全性。

**5. 风格感知的奖励驱动微调**

在强化微调阶段，系统采用 GRPO（Group Relative Policy Optimization）算法优化策略。与传统固定权重奖励不同，DMW 使用一个风格感知奖励生成器，利用大语言模型（如 GPT-5）根据场景描述和用户指令推理出安全性、效率和舒适性三个维度的动态权重和阈值，并经专家审核后形成最终的奖励函数：

$$\mathcal{R}(s_t, a_t) = w_s \cdot R_{\text{safety}} + w_e \cdot R_{\text{efficiency}} + w_c \cdot R_{\text{comfort}}$$

这种动态权重机制使得模型能够根据实时指令灵活调整行为——在“保守”指令下优先保证安全性，在“激进”指令下则允许更高的效率但需接受一定的舒适度下降。

### 模块间的信息流

整个框架的信息流是端到端的：**感知编码器 → VLA 骨干网络（融合用户嵌入和指令） → 运动预测器（基础动作） + 残差解码器（个性化调整） → 最终动作**。长期偏好编码器与路线处理器（Route Processor）之间通过对比学习建立语义对齐，而风格感知奖励则在微调阶段提供与指令一致的优化信号。两条路径——长期嵌入条件和短期奖励权重——共同作用，使 DMW 既能保持驾驶员一致的风格特征，又能响应实时的指令变化。

### 补充图表

![[assets/figures/papers/paper_list_l2383_https_arxiv_org_abs_2603_25740/figures/001_Figure_1.jpg]]
*Figure 1: Drive My Way (DMW) achieves end-to-end personalized driving via both long-term preference alignment and shortterm style instruction adaptation*

## 核心模块与公式推导

### 整体框架与动作解耦

DMW 以预训练 VLA 模型 **SimLingo** 为骨干，在保持其安全规划能力的前提下引入个性化机制。框架的核心设计是将最终动作分解为两部分：

$$a_{t} \doteq a_{t}^{\mathrm{base}} + a_{t}^{\Delta}$$

其中 $a_{t}^{\mathrm{base}}$ 为基础动作，由 Motion Predictor 从预测的路径点和目标速度导出，负责保证基本的行驶安全与路线遵循；$a_{t}^{\Delta}$ 为个性化残差，由新增的 **残差解码器（Residual Decoder）** 输出。残差解码器通过可学习查询与 MLP 生成离散的速度变化量和转向变化量，以类别分布的形式叠加到基础动作上。这种解耦设计使得个性化微调不会破坏预训练策略的安全边界，同时允许驾驶风格在动作空间中获得精细的表达。

### 长期偏好编码与对比学习

为实现对驾驶员长期习惯的适应，DMW 引入了两个关键模块：

- **长期偏好编码器（Long-term Preference Encoder）**：基于 DeBERTaV3 将驾驶员的文本档案 $P^{m}$ 编码为用户嵌入 $z_{p}^{m}$。
- **路线处理器（Route Processor）**：通过时序多头自注意力机制，将一段历史驾驶轨迹窗口编码为行为嵌入 $z_{b,t}^{m}$。

二者通过对比学习在共享潜在空间中对齐，损失函数采用 InfoNCE：

$$\mathcal{L}_{t}^{m} = -\log \frac{\exp\left(\sin(z_{p}^{m}, z_{b,t}^{m}) / \tau\right)}{\sum_{j=1}^{M} \exp\left(\sin(z_{p}^{j}, z_{b,t}^{m}) / \tau\right)}$$

其中 $\sin(\cdot,\cdot)$ 为余弦相似度，$\tau$ 为温度系数，$M$ 为驾驶员总数。该损失的核心机制是：对于驾驶员 $m$ 在时刻 $t$ 的行为嵌入 $z_{b,t}^{m}$，拉近其与自身用户嵌入 $z_{p}^{m}$ 的距离，同时推远与其他驾驶员嵌入 $z_{p}^{j}(j \neq m)$ 的距离。训练收敛后，用户嵌入能够捕获驾驶员的长期风格特征，并在规划时作为策略的条件输入。

### 风格感知的动态奖励函数

短期指令适应通过强化微调实现，其核心是风格感知的奖励函数。总奖励为安全性、效率和舒适性三个维度的加权和：

$$\mathcal{R}(s_{t}, a_{t}) = w_{s} \cdot R_{\mathrm{safety}} + w_{e} \cdot R_{\mathrm{efficiency}} + w_{c} \cdot R_{\mathrm{comfort}}$$

其中安全性奖励基于碰撞时间（TTC）的二元指示器：

$$R_{\mathrm{safety}} = \mathbb{I}_{\mathrm{safety}}(\mathrm{TTC}_{t} \geq \beta_{\mathrm{safety}})$$

权重 $w_{s}, w_{e}, w_{c}$ 和阈值 $\beta_{\mathrm{safety}}$ 并非固定值，而是根据场景描述和用户指令中的风格标签 $S \in \{\text{Conservative}, \text{Neutral}, \text{Aggressive}\}$ 动态生成。具体流程为：利用 LLM（如 GPT-5）从场景描述和指令中推理出初始权重与阈值，再经专家审核修正，确保奖励函数准确反映指令语义。例如，激进指令下效率权重升高、安全阈值放宽，保守指令下则相反。这种动态调节机制使得同一策略能够在不同指令下表现出差异化的驾驶风格——在 Bench2Drive 上，DMW 在保守指令下取得最高驾驶分（DS 82.72），在激进指令下相比 SimLingo 实现 18.77% 的效率提升，而安全分仅下降 3.89%。

### 动作归一化

在长期偏好对齐阶段，为消除不同驾驶员动作尺度差异对奖励计算的影响，DMW 引入了动作归一化。对于目标驾驶员 $m$ 的示范动作 $a_{t}^{\bar{m}}$，以通用用户档案 $P^{u}$ 为基准进行缩放：

$$\tilde{a}_{t}^{m} = \frac{\bar{a}^{m}}{\bar{a}^{u}} \cdot a_{t}^{\bar{m}}$$

其中 $\bar{a}^{m}$ 和 $\bar{a}^{u}$ 分别为驾驶员 $m$ 和通用用户在整条路线上的平均动作统计量。归一化后的动作作为行为相似度奖励的参考目标，确保对齐信号不受绝对动作幅度的干扰。

### 补充图表

![[assets/figures/papers/paper_list_l2383_https_arxiv_org_abs_2603_25740/figures/004_Figure_4.jpg]]
*Figure 4: The contrastive learning mechanism on the long-term preference encoder and route processor*

![[assets/figures/papers/paper_list_l2383_https_arxiv_org_abs_2603_25740/figures/005_Figure_5.jpg]]
*Figure 5: The fine-tuning process and reward generation for shortterm instruction alignment*

## 实验与分析

### 实验设置与评估基准

DMW 的实验验证在两个核心维度展开：一是基于 CARLA 模拟器的闭环驾驶评测，二是面向真实驾驶员个性化对齐的用户研究。闭环评测采用 **Bench2Drive** 基准，该基准提供 220 个测试场景，涵盖不同交通密度和道路拓扑。模型接收前视图相机图像、导航路径点、驾驶风格指令和用户档案作为输入，输出油门/转向动作。评估指标包括 **Driving Score (DS)**、**Success Rate (SR)**、**Comfort** 和 **Efficiency**。个性化对齐评测则基于作者自建的 **Personalized Driving Dataset (PDD)**，包含 30 名驾驶员在 20 种场景下的轨迹和档案数据，采用 **Alignment Score (AS)** 和用户评分衡量长期偏好匹配度。

基线方法包括：
- **SimLingo**：VLA 骨干模型，具备语言引导的规划能力，但无个性化机制
- **StyleDrive**：将指令映射到预定义的激进/中性/保守模式，缺乏用户级差异
- **MORL-PD**：基于多目标强化学习的个性化基线，通过驾驶员偏好向量进行条件化
- **DMW-Vanilla**：DMW 的消融变体，使用固定奖励权重替代风格感知的动态权重

### 闭环驾驶性能：风格指令适应

表 1 展示了 Bench2Drive 上不同风格指令下的闭环驾驶指标。DMW 在所有风格下均取得最高的 Driving Score 和 Success Rate，同时展现出清晰的风格敏感性：

| 风格指令 | 方法 | DS ↑ | SR ↑ | Comfort ↑ | Efficiency ↑ |
|---------|------|------|------|-----------|-------------|
| Conservative | SimLingo | 78.18 | 78.18 | 31.32 | 233.72 |
| Conservative | StyleDrive | 80.93 | 80.93 | 34.16 | 233.01 |
| Conservative | DMW-Vanilla | **83.12** | **83.12** | **36.14** | 229.47 |
| Conservative | **DMW** | 82.72 | 82.72 | 34.62 | 230.04 |
| Aggressive | SimLingo | 78.18 | 78.18 | 31.32 | 247.60 |
| Aggressive | StyleDrive | 79.01 | 79.01 | 23.58 | 266.93 |
| Aggressive | DMW-Vanilla | 80.60 | 80.60 | 28.83 | 254.80 |
| Aggressive | **DMW** | 79.50 | 79.50 | 21.62 | **281.56** |

**核心发现一：风格感知的动态权重实现了精确的权衡调节。** 在激进指令下，DMW 的 Efficiency 达到 281.56，相比 SimLingo 的 247.60 提升 13.7%，而 DS 仅下降 3.89%（从 82.72 到 79.50）。相比之下，SimLingo 在激进指令下 DS 不降反平（78.18→78.18），表明其无法根据指令调整驾驶策略。StyleDrive 虽能实现效率提升（266.93），但其 Comfort 大幅下降至 23.58，说明其风格切换过于粗糙，缺乏精细的权衡控制。

**核心发现二：固定权重的 DMW-Vanilla 丧失了风格敏感性。** DMW-Vanilla 在保守和激进指令下均取得较高的 DS 和 SR，但其 Comfort 在不同风格间变化幅度较小（36.14→28.83），Efficiency 提升有限（229.47→254.80）。这证实了风格感知的动态奖励权重对于实现指令驱动的行为差异化至关重要。

**核心发现三：残差解码器保障了安全底线。** 尽管激进指令下 Comfort 下降至 21.62，DMW 的 SR 仍维持在 79.50，说明残差动作解码器在基础动作之上叠加个性化调整时，未破坏由路点导出的安全规划。

### 长期偏好对齐：驾驶员档案嵌入

表 2 展示了不同驾驶员档案（D1-D5）在有无风格指令下的驾驶指标。每位驾驶员具有独特的长期偏好（如 D1 偏好保守，D5 偏好激进），DMW 通过用户嵌入条件化实现了对这些偏好的自动适应。

| 驾驶员 | 风格指令 | DS | SR | Comfort | Efficiency | AS | Rating |
|--------|---------|-----|-----|---------|-------------|-----|--------|
| D1 (保守) | 无 | 82.72 | 82.72 | 34.62 | 230.04 | 0.92 | 8.4 |
| D5 (激进) | 无 | 79.50 | 79.50 | 21.62 | 281.56 | 0.88 | 8.1 |

**核心发现：用户嵌入编码了可泛化的驾驶风格。** 即使在没有显式风格指令的情况下，DMW 仍能根据用户嵌入自动调整驾驶行为——保守型驾驶员 D1 获得更高的 Comfort（34.62）和更低的 Efficiency（230.04），而激进型驾驶员 D5 则呈现出相反的指标分布。对齐评分（AS）在 0.88-0.92 之间，表明对比学习成功地将用户档案与驾驶行为映射到了共享潜在空间。

### 个性化对齐用户研究

表 3 对比了 DMW 和 MORL-PD 在 PDD 上的对齐评分。MORL-PD 作为多目标强化学习基线，通过驾驶员偏好向量进行条件化，但缺乏语言理解和用户档案嵌入。

| 驾驶员 | DMW AS | MORL-PD AS | 提升 |
|--------|--------|-----------|------|
| D1 (ID) | 0.92 | 0.42 | +0.50 |
| D2 (ID) | 0.92 | 0.58 | +0.34 |
| D3 (OOD) | 0.88 | 0.45 | +0.43 |
| D4 (OOD) | 0.85 | 0.39 | +0.46 |

**核心发现：对比学习嵌入优于偏好向量条件化。** DMW 在所有驾驶员上均大幅超越 MORL-PD，对齐评分提升 0.34-0.50。更重要的是，对于未在训练集中出现的 OOD 驾驶员（D3、D4），DMW 仍保持 0.85-0.88 的 AS，表明用户嵌入具有一定的泛化能力，而非简单记忆训练样本。

表 6 的用户研究进一步验证了主观体验。在紧急场景下，五位评估者对激进指令下的轨迹进行 0-10 评分，DMW 的平均分约为 8.4，显著高于 SimLingo 的约 7.1。评估者一致认为 DMW 的轨迹更好地体现了指令中要求的果断超车和快速通过意图。

### 消融实验：自适应平均池化的关键作用

表 4 报告了移除自适应平均池化（AAP）对用户嵌入的影响。AAP 用于将变长的路线历史编码为固定维度的行为嵌入，是对比学习的关键组件。

| 变体 | AS (D1) | AS (D2) | AS (D3) |
|------|---------|---------|---------|
| DMW (含 AAP) | 0.92 | 0.92 | 0.88 |
| DMW (无 AAP) | 0.64 | 0.71 | 0.52 |

移除 AAP 导致所有驾驶员的 AS 大幅下降（降幅 0.21-0.36），OOD 驾驶员 D3 的降幅最大。这表明 AAP 通过聚合时序信息增强了行为嵌入的表达能力，使其能够捕获驾驶风格的细微差异。简单的平均池化或取最后时刻嵌入无法充分保留长序列中的风格特征。

### 失败模式与局限性分析

**1. 风格混淆边界。** 当指令与用户长期偏好冲突时（如要求保守型驾驶员执行激进超车），DMW 的行为可能出现不一致。模型需要在用户嵌入（长期偏好）和风格指令（短期需求）之间进行隐式权衡，当前架构缺乏显式的冲突解决机制。

**2. OOD 泛化上限。** 尽管 DMW 对 OOD 驾驶员表现出一定的泛化能力，但 AS 仍低于 ID 驾驶员（0.85-0.88 vs. 0.92）。对于训练集中未出现的极端驾驶风格（如极度激进或极度犹豫），模型可能无法准确对齐。

**3. 仿真到真实的鸿沟。** 所有实验均在 CARLA 模拟器中进行，真实世界中的传感器噪声、动态障碍物交互和社交驾驶规范可能暴露模型的脆弱性。用户嵌入在真实驾驶数据上的迁移能力尚未验证。

**4. 奖励设计的可扩展性。** 风格感知奖励依赖 LLM 推理和专家审核，当扩展到数百名驾驶员和数千种场景时，人工审核成本将变得不可接受。自动化的奖励校准机制是未来工作的关键方向。

**5. 数据集规模限制。** PDD 仅包含 30 名驾驶员和 20 种场景，可能无法覆盖所有驾驶风格和复杂交通情境。更大规模、更多样化的个性化驾驶数据集对于推动该领域发展至关重要。

### 补充图表

![[assets/figures/papers/paper_list_l2383_https_arxiv_org_abs_2603_25740/figures/006_Table_1.jpg]]
*Table 1: Bench2Drive closed-loop driving metrics with different style instructions. We compare SimLingo and StyleDrive under different style instructions with our policy fine-tuning with fixed rewards weights (DMW-Vanilla) and style-aware rewards weights (DMW)*

![[assets/figures/papers/paper_list_l2383_https_arxiv_org_abs_2603_25740/figures/007_Table_2.jpg]]
*Table 2: Driving metrics with and without style instructions, for each driver profile with a different long-term preference. Note that for Alignment Score (AS) and Ratings, we compute their value regardless of the style since it only measures long-term alignment*

![[assets/figures/papers/paper_list_l2383_https_arxiv_org_abs_2603_25740/figures/012_Table_6.jpg]]
*Table 6: User study ratings (0-10) evaluating how well trajectories match intended instructions. Five evaluators (E1-E5) rate trajectories from SimLingo [42], StyleDrive [11], and DMW*

![[assets/figures/papers/paper_list_l2383_https_arxiv_org_abs_2603_25740/figures/009_Figure_6.jpg]]
*Figure 6: Driving preference under aggressive and conservative instructions. Red waypoints denote distance parametrized (every 1 m) navigation path and green waypoints denote time parametrized (every 0.25 s) trajectory*

![[assets/figures/papers/paper_list_l2383_https_arxiv_org_abs_2603_25740/figures/010_Table_5.jpg]]
*Table 5: Driving metrics across all scenario types*

![[assets/figures/papers/paper_list_l2383_https_arxiv_org_abs_2603_25740/figures/008_Figure.jpg]]
*Figure: Something on the roadside block the way… “Quickly swerve into the adjacent lane to pass the hazard without braking.” “Please wait for a safe chance; I don‘t like rushing past hazards.” Something leading to a hard-brake… “Don't lose speed - assert our position but avoid collisions.” “Let merging car/crossing person go; give them space, keep the ride calm.”*

![[assets/figures/papers/paper_list_l2383_https_arxiv_org_abs_2603_25740/figures/011_Figure.jpg]]
*Figure: Bad road conditions / Opposite vehicle invades Parked obstacle / Turn at non-signalized junction*

## 方法谱系与知识库定位

### 1. 核心问题与基线对比

DMW 试图解决的瓶颈是：现有端到端自动驾驶系统（包括 VLA 模型）仅优化通用驾驶目标或依赖固定的驾驶模式（如激进/保守二选一），缺乏对**个人长期驾驶偏好**和**实时自然语言意图**的适应能力。DMW 的因果调节旋钮在于：通过用户嵌入编码长期习惯，并通过风格感知的动态奖励权重响应短期指令，从而在安全性、效率和舒适性之间实现可调节的权衡。

DMW 的基线体系可划分为三个层次：

- **VLA 骨干基线 — SimLingo**：DMW 直接采用 SimLingo 作为其 VLA 骨干网络（见 Section 5.1），该模型具备语言引导的规划能力，但不包含任何个性化机制。DMW 在其基础上插入了用户嵌入条件化和残差动作解码器，使原本通用的规划器能够输出个性化动作。在 Bench2Drive 闭环评测中，SimLingo 在保守风格下 Driving Score 为 78.18，DMW 提升至 82.72（+4.54）；在激进风格下，DMW 的效率指标从 247.60 提升至 281.56（+13.7%），证明个性化模块带来了显著增益（Table 1）。

- **固定风格条件基线 — StyleDrive**：StyleDrive 将自然语言指令映射到预定义的 Aggressive/Neutral/Conservative 三种固定模式，缺乏对驾驶员个体差异的建模。DMW 与之相比，不仅支持连续的风格调节，还能通过用户嵌入捕捉同一风格指令下不同驾驶员的差异化表现。Table 1 显示，StyleDrive 在各风格下的 DS 和 SR 均低于 DMW，且无法在激进指令下实现与 DMW 同等的效率提升（DMW Aggressive 效率 281.56 vs. StyleDrive 约 250 区间）。

- **多目标强化学习个性化基线 — MORL-PD**：该方法通过对每名驾驶员设置偏好向量来实现个性化，但缺乏语言接口和动态权重调整能力。在个性化驾驶数据集（PDD）上的对齐评分（Alignment Score）对比中，DMW 在 ID 驾驶员 D1/D2 上分别达到 0.92/0.92，而 MORL-PD 仅为 0.42/0.58（Table 3），差距显著。用户研究进一步表明，DMW 生成的驾驶行为可被识别为驾驶员自身的风格，对齐评分显著高于 MORL-PD。

- **消融变体 — DMW-Vanilla**：使用固定奖励权重的 DMW 变体。Table 1 显示，DMW-Vanilla 虽然整体 DS 和 SR 较高，但导致激进与保守指令下的驾驶行为区分度降低，丧失了风格敏感性。这验证了风格感知动态奖励权重是 DMW 实现短期指令适应的关键设计。

### 2. 技术谱系与创新定位

DMW 的方法设计可定位于以下技术谱系的交叉点：

- **VLA 规划器谱系**：DMW 继承自 SimLingo 的语言引导规划框架，属于将视觉、语言和动作整合到统一 Transformer 架构的端到端自动驾驶路线。与 UniAD、VAD 等纯视觉端到端方法相比，DMW 引入了语言作为风格调节的接口；与 DriveGPT4、DriveLM 等语言辅助驾驶方法相比，DMW 将语言的作用从场景理解扩展到了个性化偏好表达。

- **偏好对齐谱系**：DMW 的核心技术——对比学习嵌入 + 强化微调——借鉴了 LLM 领域的 RLHF/DPO 范式，但将其迁移到了物理动作空间。具体而言，长期偏好对齐采用 InfoNCE 对比损失将驾驶员档案与历史行为嵌入到共享潜在空间（Eq. 1），这与表示学习中的度量学习思路一致；短期指令适应则采用 Group Relative Policy Optimization（GRPO）进行强化微调，奖励函数由 LLM 推理生成并经专家审核（Fig. 5），形成了一条从语言指令到物理驾驶行为的对齐链路。

- **残差学习谱系**：DMW 引入的残差动作解码器（Section 5.2，Fig. 3）将最终动作分解为基础动作（由路点导出）和个性化残差（由可学习查询 + MLP + 分类头输出），即 $a_t \doteq a_t^{\mathrm{base}} + a_t^{\Delta}$。这种设计在保持安全规划能力的同时，允许模型在不破坏基础驾驶行为的前提下进行个性化微调，与 residual RL、residual policy learning 等方法共享设计哲学。

### 3. 适用边界与局限

DMW 的适用边界和局限需要明确认知：

- **仿真局限性**：所有实验均在 CARLA 模拟环境中进行，未在真实车辆上验证泛化能力。sim-to-real 差距是该类方法的共性挑战，DMW 尚未提供相关证据。

- **数据覆盖范围有限**：个性化数据集仅包含 30 名驾驶员和 20 种场景。该规模可能无法覆盖所有驾驶风格和复杂交通场景，模型对训练集之外的全新驾驶风格或极端偏好的泛化能力未经验证。

- **奖励生成的可扩展性瓶颈**：风格感知奖励依赖 LLM（如 GPT-5）推理和专家审核（Section 5.4），这一流程在扩展到更多用户时面临可扩展性挑战。专家审核环节的人力成本、LLM 推理的一致性、以及不同文化和交通法规背景下奖励权重的适用性，均是待验证的问题。

- **用户意图的模糊性处理**：当前框架假设用户指令是明确且一致的，未涉及用户意图的模糊性、多模态需求（如同时要求安全和效率）以及突发情绪变化等复杂场景。这些场景下的模型行为需要进一步研究。

### 4. 开放问题

从 DMW 的当前局限出发，可识别以下开放问题：

1. **规模化对齐**：如何将 DMW 扩展到更大规模的驾驶员群体（如数千人）并保持对齐能力？对比学习的 batch 规模、用户嵌入的多样性保持（消融实验已证明自适应平均池化的关键作用，Table 4）以及强化微调的样本效率，均需要进一步优化。

2. **sim-to-real 迁移**：如何弥合从仿真到真实世界的差距？域随机化、真实数据微调、以及 sim-to-real 的奖励函数适配是潜在方向，但 DMW 尚未涉及。

3. **跨文化适应性**：LLM 生成的奖励权重在不同文化和交通法规背景下的适用性如何？例如，某些地区对“激进”驾驶的定义和容忍度可能与训练数据中的设定存在显著差异。

4. **动态意图处理**：如何处理用户意图的模糊性、多模态需求以及突发情绪变化？这可能需要引入不确定性建模、交互式查询机制或在线学习组件。

5. **安全-个性化权衡的边界**：在不牺牲安全性的前提下，个性化程度的上限在哪里？DMW 在激进指令下 DS 从 82.72 降至 79.50（Table 1），表明存在安全-效率的 trade-off，但该 trade-off 的理论边界和实际约束尚未被系统研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/Drive_My_Way_Preference_Alignment_of_Vision_Language_Action_Model_for_Personalized_Driving.pdf]]
