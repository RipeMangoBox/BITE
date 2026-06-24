---
title: Aligning Multi-Character Narrative Image Generation with Multi-Aspect Human Preferences
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Aligning_Multi_Character_Narrative_Image_Generation_with_Multi_Aspect_Human_Preferences.pdf
project_link: null
code_link: null
aliases:
- AMCNIGMAHP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入基于批判的多维奖励模型 NIReward 和自适应支配偏好优化 ADPO，使生成过程直接对齐人类在提示跟随、身份一致性和视觉质量上的偏好。
primary_logic: 通过构建细粒度人类偏好数据集 NI-RLHF 并训练可解释批判的奖励模型，再以支配比较和自适应加权学习进行多维度平衡的偏好优化，解决了奖励信号的分布偏差、不可解释性和优化不平衡问题。
claims:
- NIReward 在身份一致性上的偏好准确率超过 GPT-4o-mini 高达 38.35%。
- ADPO 在提示跟随、身份一致性和视觉质量三个维度上全面超越 Diffusion-DPO 搭配传统奖励模型。
- 批判机制使视觉质量准确率提升 10.34%，整体可解释性显著增强。
- NI-Bench（身份一致性） 上 偏好预测准确率 = NIReward 85.10%
---

# Aligning Multi-Character Narrative Image Generation with Multi-Aspect Human Preferences

> [!tip] 核心洞察
> 通过构建细粒度人类偏好数据集 NI-RLHF 并训练可解释批判的奖励模型，再以支配比较和自适应加权学习进行多维度平衡的偏好优化，解决了奖励信号的分布偏差、不可解释性和优化不平衡问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向多方面人类偏好的多角色叙事图像生成对齐 |
| 英文题名 | Aligning Multi-Character Narrative Image Generation with Multi-Aspect Human Preferences |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Gao_Aligning_Multi-Character_Narrative_Image_Generation_with_Multi-Aspect_Human_Preferences_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | NIReward + ADPO |
| Dataset | NI-Bench（身份一致性） |

> [!tip] 效果简介
> - NI-Bench（身份一致性） 上，偏好预测准确率 NIReward 85.10% vs GPT-4o-mini (+38.35%)。
> - NI-Bench（生成质量） 上，NIReward 视觉质量分数 (V.Q.) ADPO + NIReward: 0.131 vs Diffusion-DPO + ImageReward 等最优传统奖励模型 (优于所有对比方法)。
> - 用户研究 上，人类偏好胜率 ADPO + NIReward 显著优于其他 DPO 方法 vs Diffusion-DPO 变体 (人类偏好显著偏向本方法)。

## 概述

多角色叙事图像生成面临三大核心挑战：**语义对齐差**（角色姿态与表情过拟合参考图像，偏离文本提示）、**身份混合**（面部特征融合导致角色区分度低）以及**美学缺陷**（如解剖结构不一致，见图1）。根本瓶颈在于，现有文本到图像扩散模型缺乏对提示跟随、身份一致性和视觉质量的多维人类偏好对齐，而通用自动评价指标（如CLIP、ArcFace）与人类感知严重不一致。

针对上述问题，本文提出两个因果性改进模块：**NIReward**——基于批判的多维奖励模型，以及**ADPO**——自适应支配偏好优化算法。NIReward 以多模态大语言模型为骨干，先生成可解释的文本批判，再据此产出多维偏好分数，解决了传统标量奖励模型不可解释、与人类偏好分布偏差大的问题。ADPO 则通过支配比较策略、拒绝采样和自适应加权学习，在多维度上平衡优化，避免了对易量化维度的过度优化。

核心实验证据表明：NIReward 在身份一致性上的偏好预测准确率超越 GPT-4o-mini 高达 **38.35%**（Table 1）；ADPO 搭配 NIReward 在提示跟随、身份一致性和视觉质量三个维度上全面超越 Diffusion-DPO 搭配传统奖励模型（Table 2）；批判机制使视觉质量准确率提升 **10.34%**（Table 4），验证了可解释推理路径对偏好建模的关键作用。用户研究进一步确认，本方法生成的结果更符合人类偏好（Figure 4）。

## 背景与动机

### 多角色叙事图像生成的核心挑战

文本到图像（T2I）扩散模型在单主体生成上已取得显著进展，但在**多角色叙事场景**下仍暴露出三个深层缺陷（Figure 1）：

1. **语义对齐差（Prompt Following Failure）**：角色姿态与表情过度拟合参考图像，而非遵循文本提示的叙事要求。例如，老年男性的表情机械复制参考肖像，忽略了提示中描述的动作与情绪。
2. **身份混合（Identity Blending）**：多个角色的面部特征相互渗透，导致身份区分度低，无法保持独立、可辨识的角色身份。
3. **美学与解剖缺陷（Visual Quality Degradation）**：生成图像出现解剖不一致（如下半身渲染不完整），视觉质量显著下降。

这些问题的根源在于：现有个性化生成模型（如 **PhotoMaker**，Li et al., CVPR 2024）在将多个参考身份注入单一叙事场景时，缺乏对提示语义、身份边界和全局视觉质量的联合约束。

### 现有对齐方法的缺口

为将扩散模型与人类偏好对齐，已有工作引入基于人类反馈的强化学习（RLHF）或直接偏好优化（DPO）。然而，这些方法在多角色叙事生成中面临两个关键瓶颈：

**瓶颈一：通用奖励模型与人类感知偏好的严重不一致。** 现有自动评价指标（CLIP、ArcFace 等）和通用标量奖励模型（**ImageReward**，Xu et al., NeurIPS 2023；**HPSv2**；**PickScore**）仅输出单一标量分数，无法捕捉多角色场景下提示跟随、身份一致性和视觉质量三个维度的细粒度偏好。更重要的是，这些模型的偏好判断与人类感知存在系统性偏差——它们无法解释“为什么”一张图优于另一张，导致优化信号不可靠。

**瓶颈二：多维偏好优化的不平衡。** 标准 Diffusion-DPO（Wallace et al., CVPR 2024）使用固定权重 $\beta$ 且不对偏好对进行过滤。当面对三个相互竞争的优化维度时，模型容易过度优化某一维度（如提示跟随）而损害其他维度（如身份一致性），无法实现多维度的平衡对齐。

### 本文动机与核心思路

针对上述瓶颈，本文提出两条因果干预路径：

1. **构建可解释的多维奖励模型**：设计基于批判的奖励模型 **NIReward**，以多模态大语言模型（MLLM）为骨干，首先生成文本批判（解释优劣原因），再从批判中推导各维度的偏好分数。这解决了奖励信号的不可解释性和分布偏差问题。

2. **设计自适应支配偏好优化算法**：提出 **ADPO**（Adaptive Dominance-based Preference Optimization），通过支配比较策略仅选择在所有维度上均占优的偏好对，结合拒绝采样过滤低质量样本，并以自适应加权学习动态调整各维度的优化强度。这解决了多维优化中的不平衡问题。

两者协同工作：NIReward 提供可信的多维反馈，ADPO 利用该反馈进行平衡的偏好优化，最终使生成过程直接对齐人类在提示跟随、身份一致性和视觉质量上的复合偏好。

## 核心创新

本工作针对多角色叙事图像生成中“通用自动评价指标与人类感知偏好严重不一致”这一瓶颈，提出了**可解释的多维奖励模型 NIReward** 与**自适应支配偏好优化算法 ADPO**，形成从奖励信号构建到策略优化的完整对齐链路。核心创新可归结为三个关键组件的改变。

### 从标量奖励到基于批判的多维奖励

传统方法依赖通用标量奖励模型（如 ImageReward、HPSv2、PickScore）为 Diffusion-DPO 提供偏好信号。这些模型输出单一分值，既无法解释偏好来源，又在多角色叙事场景下与人类判断存在系统性偏差——尤其在身份一致性维度上，GPT-4o-mini 的偏好准确率仅为 46.75%（Table 1），远不足以支撑可靠的对齐训练。

NIReward 将奖励建模重构为“先批判、后评分”的两阶段范式。模型基于多模态大语言模型（MLLM）骨架，增设**批判头**（critique head）与**奖励头**（reward head）。推理时，批判头首先生成针对提示跟随、身份一致性和视觉质量的细粒度文本批判，奖励头再将这些可解释的推理路径纳入多维偏好分数的计算。这一设计使奖励信号从黑箱标量进化为可审计的多维向量，为后续优化提供了维度级支配性判断的基础。

批判机制的引入带来了显著的准确率增益：在 NI-Bench 上，批判使提示跟随、身份一致性和视觉质量的偏好准确率分别提升 2.24%、0.5% 和 10.34%（Table 4），其中视觉质量维度的提升尤为突出，验证了文本推理路径对复杂美学判断的关键作用。

### 从任意偏好对到支配性偏好筛选

标准 Diffusion-DPO 直接使用人工标注的任意偏好对进行优化，隐含假设每个偏好对在所有维度上均一致地反映人类偏好。然而，在多维度评价体系下，一幅图像可能在提示跟随上胜出，却在身份一致性上劣于对手，这种“维度冲突”的偏好对会向优化过程注入噪声。

ADPO 的**支配比较策略**（Dominating Comparison Strategy）从根本上改变了偏好对的筛选逻辑：仅当获胜样本在提示跟随、身份一致性和视觉质量**所有三个维度**上的奖励分数均严格优于失败样本时，该偏好对才被纳入训练。这一约束确保每个训练样本传递的是无歧义的多维偏好信号。消融实验表明，将支配比较替换为平均分比较会导致性能显著下降，尤其在身份相似度指标上退化明显（Table 3），证实了维度级一致性筛选的必要性。

此外，ADPO 引入**拒绝采样**机制，要求获胜样本的奖励分数超过预设质量阈值，进一步过滤低质量偏好对，从源头减少噪声。

### 从固定权重到自适应加权学习

传统 Diffusion-DPO 使用固定权重 β 调节偏好优化的强度，对所有偏好对一视同仁。这种均匀处理忽视了偏好对之间置信度的天然差异——奖励间隔大的偏好对反映更强的偏好信号，理应获得更大的优化权重。

ADPO 的**自适应加权学习**将奖励间隔 a 映射为动态缩放因子 β(a)，其函数形式为：

$$\beta(a) = \beta \left(1 + \eta \left(1 - e^{-k(a - b)}\right)\right)$$

其中 b 为阈值，η 控制自适应范围，k 控制灵敏度。当奖励间隔 a 超过阈值 b 时，β(a) 随间隔增大而平滑增长，使高置信度偏好对获得更强的优化力度；反之，低置信度偏好对的权重趋近于基准值 β。

消融实验揭示了自适应加权的必要性：移除该机制（w/o AW）会导致模型过度优化提示跟随，同时损害身份一致性（Table 3），表明固定权重无法在多维度目标间维持平衡，而自适应机制通过奖励间隔这一自然置信度信号实现了维度间的动态协调。

### 创新链路总结

三个创新组件形成递进闭环：NIReward 提供可解释的多维奖励信号，使维度级支配判断成为可能；支配比较策略与拒绝采样从信号中提取高置信度、无冲突的偏好对；自适应加权学习则根据偏好对的置信度差异精细调控优化强度，避免多维度间的失衡。这一“可解释奖励 → 支配筛选 → 自适应优化”的链路，使生成过程直接对齐人类在提示跟随、身份一致性和视觉质量上的细粒度偏好，而非间接拟合单一标量分数。

## 整体框架

本工作提出了一套面向多角色叙事图像生成的偏好对齐框架，其核心由三个模块串联构成：**NI‑RLHF 数据集**、**NIReward 奖励模型**与 **ADPO 偏好优化算法**。整体流程如图 3 所示：首先基于 NI‑RLHF 数据集训练一个可解释的多维奖励模型 NIReward；随后在 ADPO 的“采样—评分—比较—优化”四阶段循环中，利用 NIReward 的多维支配信号对基础个性化生成模型进行偏好微调，最终使生成结果在提示跟随、身份一致性与视觉质量三个维度上同时逼近人类偏好。

**NI‑RLHF 数据集** 是整个框架的偏好信号来源。其构建分为两步（图 2）：  
1. **数据收集**：使用个性化文本到图像模型（以 **PhotoMaker** 为基础，Li et al., CVPR 2024）生成多角色叙事图像。  
2. **数据标注**：基于多模态大语言模型（MLLM）进行人工标注，为每对胜出/败出图像提供提示跟随、身份一致性与视觉质量三个维度的文本批判及偏好标签。  

该数据集为 NIReward 提供了细粒度的监督信号，使其不仅能输出标量奖励，还能生成与人工标注一致的文本批判。

**NIReward 奖励模型** 建立在 MLLM 骨干之上，包含一个批判头（critique head）和一个奖励头（reward head）。其推理采用两阶段过程：首先生成文本批判 $s$，再将批判 $s$ 与图像、提示、参考图像等条件一并送入奖励头，输出多维偏好分数。训练时，批判头通过交叉熵损失 $\mathcal{L}_{\mathrm{critique}}$ 对齐人工批判，奖励头通过批判引导的成对奖励损失 $\mathcal{L}_{\mathrm{reward}}$ 学习偏好排序，总损失为 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{critique}} + \gamma \mathcal{L}_{\mathrm{reward}}$。这一设计使奖励信号具备可解释性，并在视觉质量维度上将偏好准确率提升了 10.34%。

**ADPO 偏好优化算法** 解决传统 Diffusion‑DPO 的两大缺陷：对易量化维度的过优化倾向，以及对所有偏好对平等对待导致的高噪声学习。ADPO 在每轮迭代中执行四个阶段：  
1. **采样（Sample）**：从当前模型中生成候选图像。  
2. **评分（Score）**：用 NIReward 对候选图像在提示跟随、身份一致性、视觉质量三个维度上分别打分。  
3. **支配比较（Dominating Comparison）**：仅当胜出图像在所有维度上均严格优于败出图像时，才构成有效偏好对；同时通过拒绝采样（Rejection Sampling）滤除胜出图像质量低于预设阈值的对。  
4. **自适应加权优化（Adaptive Weighted Learning）**：将多维奖励边际 $a$ 映射为自适应缩放因子 $\beta(a)$，使高置信度偏好对获得更大优化权重，从而在 Diffusion‑DPO 目标函数中实现多维度平衡的偏好学习。

整个框架的输入为文本提示 $y$ 与参考图像 $c$，经过 PhotoMaker 基础模型生成初始图像，再由 NIReward 提供多维批判与奖励，最终通过 ADPO 迭代微调模型参数，输出对齐人类偏好的多角色叙事图像。

### 补充图表

![[assets/figures/papers/paper_list_l982_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Aligning_Multi_Cha/figures/003_Figure_3.jpg]]
*Figure 3: The overview of proposed NIReward training and ADPO. During the NIReward Training, NIReward learns to provide critiques and rewards based on annotated winning/losing image pairs; and ADPO aligns the model with human preferences through sampling, scoring, dominating comparison, and preference optimization*

## 核心模块与公式推导

### 1. NIReward：基于批判的多维奖励模型

NIReward 是一个构建在多模态大语言模型（MLLM）骨干之上的奖励模型，其核心设计在于将传统的标量奖励扩展为**可解释的多维偏好信号**。模型包含两个关键头部：

- **批判头（Critique Head）**：负责生成对输入图像的文本批判，解释图像在提示跟随、身份一致性和视觉质量上的表现。
- **奖励头（Reward Head）**：以生成的批判为条件，输出各维度的偏好分数。

推理时采用两阶段流程：首先根据指令 $q$、生成图像 $x$、文本提示 $y$ 和参考图像 $c$ 生成批判 $s$，随后奖励头结合批判 $s$ 计算最终的多维奖励 $r$。

#### 关键公式

**批判损失** 用于将批判头与人工标注的批判对齐：

$$\mathcal{L}_{critique} = - \mathbb{E}_{x, y, c, s} \left[ \sum_{t=1}^{|s|} \log \pi_{\phi}(s_t \mid s_{<t}, x, y, c, q) \right] \tag{Eq. 2}$$

其中 $\pi_{\phi}$ 为批判头的生成策略，$s_t$ 为批判文本的第 $t$ 个 token，$q$ 为评估指令。

**批判引导的奖励损失** 以人工标注的批判 $s$ 为条件进行成对比较：

$$\mathcal{L}_{reward} = - \mathbb{E}_{x^w, x^l, y, c} \left[ \log \sigma \left( r(x^w, y, c, q, s) - r(x^l, y, c, q, s) \right) \right] \tag{Eq. 3}$$

其中 $x^w$ 和 $x^l$ 分别为胜出和失败样本，$\sigma$ 为 sigmoid 函数。

**NIReward 总损失** 为批判损失与奖励损失的加权和：

$$\mathcal{L}_{total} = \mathcal{L}_{critique} + \gamma \mathcal{L}_{reward} \tag{Eq. 4}$$

其中 $\gamma$ 为平衡两项目标的权重因子。

### 2. ADPO：自适应支配偏好优化

ADPO 旨在解决传统 DPO 方法在多维度偏好对齐中的两个核心问题：**过度优化易量化维度**（如提示跟随）而忽视细微因素（如身份一致性），以及**对所有偏好对均等对待**导致低质量样本干扰优化。

ADPO 包含四个关键阶段：**采样（Sample）→ 评分（Score）→ 支配比较（Compare）→ 优化（Optimize）**。

#### 核心机制

- **支配比较策略（Dominating Comparison Strategy）**：胜出样本 $x_0^i$ 必须在所有维度 $k$ 上严格优于失败样本 $x_0^j$，即 $r(x_0^i, y, c, q_k) > r(x_0^j, y, c, q_k)$ 对所有 $k$ 成立。这确保仅使用高置信度的偏好对进行优化。
- **拒绝采样（Rejection Sampling）**：胜出样本需超过预设的质量阈值 $th$，进一步过滤低质量偏好对。
- **自适应加权学习（Adaptive Weighted Learning）**：将奖励间隔 $a$（胜出与失败样本在各维度上的分数差）作为偏好置信度的自然信号，动态调整 DPO 中的缩放因子。

#### 关键公式

**自适应缩放因子** 基于奖励间隔 $a$ 动态计算：

$$\beta(a) = \beta \left( 1 + \eta \left( 1 - e^{-k(a - b)} \right) \right) \tag{Eq. 8}$$

其中 $\beta$ 为基础权重，$b$ 为阈值，$\eta$ 控制自适应范围，$k$ 控制对间隔变化的灵敏度。当 $a > b$ 时，$\beta(a)$ 增大，强化高置信度偏好对的影响。

**ADPO 目标函数** 将自适应权重 $\beta(a)$ 和条件嵌入 $\hat{c}$（融合文本提示与参考图像）整合进扩散模型的 DPO 框架：

$$\mathcal{L}(\theta) = - \mathbb{E}_{(x_0^w, x_0^l) \sim \mathcal{D}, t \sim \mathcal{U}(0,T), x_t^w \sim q(x_t^w | x_0^w), x_t^l \sim q(x_t^l | x_0^l)} \log \sigma \left( -\beta(a) T \omega(\lambda_t) \left( \| \epsilon^w - \epsilon_{\theta}(x_t^w, t, \hat{c}) \|_2^2 - \| \epsilon^w - \epsilon_{\mathrm{ref}}(x_t^w, t, \hat{c}) \|_2^2 - ( \| \epsilon^l - \epsilon_{\theta}(x_t^l, t, \hat{c}) \|_2^2 - \| \epsilon^l - \epsilon_{\mathrm{ref}}(x_t^l, t, \hat{c}) \|_2^2 ) \right) \right) \tag{Eq. 9}$$

其中 $\epsilon_{\theta}$ 为当前模型预测的噪声，$\epsilon_{\mathrm{ref}}$ 为参考模型预测的噪声，$T$ 为扩散步数，$\omega(\lambda_t)$ 为信噪比相关的权重函数。

### 3. 模块间因果链条

NIReward 提供的**可解释批判**解决了传统奖励模型的“黑箱”问题——消融实验表明，批判机制使视觉质量准确率提升 10.34%（Table 4）。ADPO 的**支配比较**和**自适应加权**则解决了多维偏好优化中的不平衡问题：移除自适应加权（w/o AW）会导致提示跟随过度优化而损害身份一致性；替换支配比较为平均分（Avg. Score）则显著降低身份相似度（Table 3）。两者协同实现了从“单一标量信号”到“可解释多维信号”，再到“平衡优化”的完整对齐链路。

### 补充图表

![[assets/figures/papers/paper_list_l982_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Aligning_Multi_Cha/figures/002_Figure_2.jpg]]
*Figure 2: NI-RLHF construction pipeline. It consists of two stages: (1) Data Collection: generate multi-character images using personalized T2I models. (2) Data Annotation: MLLM-based human annotation of prompt following, identity consistency, and visual quality*

## 实验与分析

### 核心瓶颈与评估体系

现有文本到图像扩散模型在多角色叙事生成中面临三重挑战：**语义对齐差**（人物姿态与表情过度拟合参考图像而偏离提示词）、**身份混合**（角色面部特征相互渗透）、**美学缺陷**（肢体解剖错误或渲染不完整）。更关键的是，通用自动评价指标（如 CLIP 分数、ArcFace 相似度）与人类感知偏好严重不一致，导致优化方向偏离真实需求。为此，本研究构建了细粒度人类偏好数据集 **NI-RLHF**，并基于此设计了专用评估基准 **NI-Bench**，从提示跟随、身份一致性和视觉质量三个维度衡量生成质量与奖励模型的偏好预测能力。

### 奖励模型偏好准确率对比

Table 1 展示了各奖励模型在 NI-Bench 上的偏好预测准确率。NIReward 在所有三个维度上均达到最优：提示跟随 86.07%、身份一致性 85.10%、视觉质量 82.52%，综合准确率显著超越现有方法。尤其在身份一致性维度上，NIReward 比 GPT-4o-mini 高出 38.35 个百分点，验证了基于批判的推理路径对细粒度身份判断的关键作用。相比之下，传统标量奖励模型（ImageReward、HPSv2、PickScore）在视觉质量上表现尚可，但在身份一致性上大幅落后，说明其缺乏对角色身份保持的建模能力。

![[assets/figures/papers/paper_list_l982_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Aligning_Multi_Cha/figures/004_Table_1.jpg]]
*Table 1: Preference accuracy on NI-Bench. The best results are in bold and the second-best results are underlined. N/A denotes Not Applicable*

### 偏好优化生成结果

Table 2 报告了不同偏好优化方法的定量生成结果。以 PhotoMaker（Li et al., CVPR 2024）为基础模型，ADPO 搭配 NIReward 在提示跟随、身份一致性和视觉质量三个维度上均优于 Diffusion-DPO 搭配传统奖励模型（ImageReward、HPSv2、PickScore）的所有变体。具体而言，ADPO + NIReward 的视觉质量分数达到 0.131，提示跟随和身份一致性指标也全面领先。值得注意的是，DPOK（Fan et al., NeurIPS 2023）和 D3PO（Yang et al., CVPR 2024）等无独立奖励模型的方法在身份一致性上表现较弱，表明显式的多维奖励信号对多角色场景至关重要。

![[assets/figures/papers/paper_list_l982_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Aligning_Multi_Cha/figures/005_Table_2.jpg]]
*Table 2: Quantitative preference optimization results.“Baseline”: base diffusion model.“Aes”: Aesthetic Score.“P.F.”: Prompt Following,“I.C.”: Identity Consistency,“V.Q.”: Visual Quality. Bold: best results; underlined: second-best*

### 用户研究

Figure 4 的用户研究结果进一步证实，人类评估者在成对比较中显著偏好 ADPO + NIReward 生成的图像，胜率超过所有对比的 DPO 变体。这表明 NIReward 的多维奖励信号和 ADPO 的支配比较策略共同作用，使生成结果在主观感知层面更贴近人类偏好。

![[assets/figures/papers/paper_list_l982_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Aligning_Multi_Cha/figures/007_Figure_4.jpg]]
*Figure 4: User Study of ADPO compared to other methods*

### 消融实验

#### 批判机制的有效性

Table 4 的消融结果表明，移除批判机制后，NIReward 在提示跟随、身份一致性和视觉质量上的准确率分别下降 2.24%、0.5% 和 10.34%。视觉质量维度的降幅最大，说明可解释的文本批判对美学判断尤为重要——模型需要显式的推理路径来评估解剖合理性、光照一致性等复杂视觉属性。

![[assets/figures/papers/paper_list_l982_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Aligning_Multi_Cha/figures/008_Table_4.jpg]]
*Table 4: Ablation result of critique-based reward modeling*

#### ADPO 各组件贡献

Table 3 系统消融了 ADPO 的四个关键组件：

![[assets/figures/papers/paper_list_l982_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Aligning_Multi_Cha/figures/006_Table_3.jpg]]
*Table 3: Ablation results of ADPO. The best results are in bold and the second-best results are underlined*

- **支配比较策略替换为平均分**：将 Dominating Comparison Strategy 改为对各维度取平均分后，身份相似度（ID Sim）显著下降，表明跨维度联合支配条件能有效过滤掉部分维度退化但平均分仍高的劣质样本。
- **移除拒绝采样**：取消 Rejection Sampling 后所有指标均降低，说明质量阈值过滤对排除低质量偏好对、稳定训练至关重要。
- **移除自适应加权**：固定 β 权重会导致提示跟随过度优化，同时损害身份一致性。这验证了基于奖励间隔的自适应缩放因子 β(a) 能动态平衡各维度的优化强度，避免单维度过拟合。
- **完整 ADPO**：在所有消融变体中取得最优结果，证实了四阶段流程（采样、评分、支配比较、自适应加权学习）的协同必要性。

### 定性分析

Figure 5 展示了不同 DPO 方法的定性生成比较。在“女人做沙拉而老人切菜”的叙事场景中，ADPO + NIReward 生成的图像在角色身份保持（两人面部特征清晰可辨且与参考一致）、动作语义对齐（切菜与做沙拉的动作准确）和整体视觉质量（肢体完整、光照自然）上均优于 Diffusion-DPO 变体。相比之下，使用传统奖励模型的方法常出现身份混合或动作与提示词不匹配的问题，与定量结果相互印证。

### 小结

综合而言，NIReward 通过批判引导的多维奖励建模，解决了通用奖励模型在多角色叙事场景中的分布偏差和不可解释性问题；ADPO 通过支配比较、拒绝采样和自适应加权，实现了多维度偏好的平衡优化。两者协同使生成模型在自动指标和人类评估上均显著超越现有 DPO 方法。

### 补充图表

![[assets/figures/papers/paper_list_l982_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Aligning_Multi_Cha/figures/001_Figure_1.jpg]]
*Figure 1: Challenges in multi-character narrative image generation: (a) Characters display portrait poses with the elderly man’s expression overfitting to reference rather than aligning with the prompt; (b) Low facial distinctiveness with blended identity features; (c) Anatomical inconsistency shown in the girl’s incompletely rendered lower body*

## 方法谱系与知识库定位

### 1 问题定位：多角色叙事生成中的奖励信号困境

本工作处于**文本到图像扩散模型的人类偏好对齐**与**多角色个性化生成**的交叉点。其核心瓶颈在于：通用自动评价指标（CLIP、ArcFace 等）在多角色叙事场景下与人类感知偏好存在严重不一致——提示跟随、身份一致性、视觉质量三个维度的评价信号既不可解释，又存在分布偏差，导致现有偏好优化方法难以有效平衡多维度需求。

### 2 与基线方法的关系

#### 2.1 基础生成模型

本方法以 **PhotoMaker**（Li et al., CVPR 2024）作为基础个性化图像生成模型。PhotoMaker 提供了多角色参考图像注入的架构基础，但其原生输出在上述三个维度上仍存在姿态过拟合、身份混合和解剖错误等问题（见 Figure 1）。

#### 2.2 奖励模型谱系

NIReward 的基线可划分为两类：

**通用标量奖励模型**：包括 **ImageReward**（Xu et al., NeurIPS 2023）、HPSv2 和 PickScore。这些模型输出单一标量分数，缺乏对多维度偏好的细粒度建模能力，且在身份一致性等特定维度上与人类判断差距显著——Table 1 显示 NIReward 在身份一致性上的偏好准确率超过 GPT-4o-mini 达 38.35%。

**基于 MLLM 的评判方法**：GPT-4o-mini 作为代表性的多模态大语言模型评判器，虽然具备一定的可解释性，但在身份一致性等需要细粒度视觉理解的维度上准确率有限。NIReward 通过引入专门的批判头和奖励头，以人工标注的批判文本作为中间推理路径，实现了可解释性与准确性的双重提升。

#### 2.3 偏好优化算法谱系

**Diffusion-DPO**（Wallace et al., CVPR 2024）：将直接偏好优化从语言模型迁移至扩散模型，是本工作的核心优化基座。但标准 Diffusion-DPO 存在两个关键局限：一是使用固定权重 $\beta$ 处理所有偏好对，无法区分高置信度与低置信度样本；二是依赖单一标量奖励，难以平衡多维度偏好。

**DPOK**（Fan et al., NeurIPS 2023）：基于强化学习的人类反馈微调方法，需要在线采样和奖励评估，计算开销大且训练不稳定。

**D3PO**（Yang et al., CVPR 2024）：无单独奖励模型的 DPO 变体，直接使用人类偏好对进行优化，但缺乏对偏好质量的筛选机制。

ADPO 在上述谱系中的定位是：**以多维支配比较替代标量比较，以自适应加权替代固定权重，以拒绝采样替代全量偏好对训练**。消融实验（Table 3）表明，将支配比较策略替换为平均分会导致性能显著下降，尤其在身份相似度上；移除拒绝采样在所有指标上降低有效性；不加自适应加权会过度优化提示跟随，同时损害身份一致性。

### 3 方法谱系图

```
多角色叙事图像生成的人类偏好对齐
│
├── 基础生成模型
│   └── PhotoMaker (Li et al., CVPR 2024) ──→ 本工作的优化基座
│
├── 奖励模型维度
│   ├── 通用标量奖励：ImageReward / HPSv2 / PickScore
│   │   └── 局限：单维度标量、不可解释、身份一致性差
│   ├── MLLM评判器：GPT-4o-mini
│   │   └── 局限：身份一致性准确率低
│   └── ★ NIReward（本工作）
│       └── 创新：批判头 + 奖励头 → 可解释的多维奖励
│
└── 偏好优化维度
    ├── Diffusion-DPO (Wallace et al., CVPR 2024)
    │   └── 局限：固定 β、单标量奖励、无偏好对过滤
    ├── DPOK (Fan et al., NeurIPS 2023)
    │   └── 局限：在线RL、训练不稳定
    ├── D3PO (Yang et al., CVPR 2024)
    │   └── 局限：无奖励模型引导
    └── ★ ADPO（本工作）
        └── 创新：支配比较 + 拒绝采样 + 自适应加权
```

### 4 适用边界

**场景适用性**：本方法专为多角色叙事图像生成设计，其核心假设是生成结果需要在提示跟随、身份一致性和视觉质量三个维度上同时满足人类偏好。对于单角色或无需身份保持的通用文本到图像生成任务，NIReward 的多维批判机制可能引入不必要的计算开销，但其批判引导的奖励建模思路具有向其他细粒度评估场景迁移的潜力。

**数据依赖性**：NI-RLHF 数据集的构建依赖 MLLM 辅助的人工标注流程（Figure 2），标注成本和质量控制是实际部署的关键约束。NIReward 的批判生成能力受限于人工标注批判的质量和覆盖范围。

**模型依赖性**：NIReward 基于 MLLM 骨干网络，其推理效率受限于骨干网络的规模；ADPO 的支配比较策略要求奖励模型能够输出多维分数，与标量奖励模型不兼容。

### 5 局限与开放问题

**论文未明确讨论的局限**：基于已验证分析，论文未提供关于方法局限性的显式讨论。以下为基于方法设计的合理推断，需人工验证：

- **计算开销**：NIReward 的两阶段推理（先生成批判，再计算奖励）相比标量奖励模型增加了推理延迟；ADPO 的采样-评分-比较-优化四阶段流程也比标准 Diffusion-DPO 需要更多的前向传播。
- **批判质量边界**：当生成图像与训练分布差异较大时，批判头的生成质量可能下降，进而影响奖励信号的可靠性。Table 4 显示批判机制对视觉质量的提升（10.34%）远大于身份一致性（0.5%），暗示批判在不同维度上的贡献不均衡。
- **支配比较的覆盖范围**：支配比较策略要求胜出样本在所有维度上均优于失败样本，这可能导致可用偏好对数量减少，在奖励信号稀疏的场景下影响优化效率。

**开放问题**：

1. **批判引导奖励的泛化性**：NIReward 的批判-奖励两阶段范式能否泛化到其他需要细粒度视觉理解的评估任务（如布局准确性、风格一致性），以及如何以较低成本扩展批判维度。
2. **多维支配的帕累托前沿**：ADPO 的支配比较策略本质上是寻找帕累托占优的偏好对，当多个维度存在冲突时（如提示跟随与视觉质量之间的权衡），帕累托前沿上的偏好对可能变得稀疏，如何在这种情况下保持优化稳定性值得进一步研究。
3. **自适应加权的理论性质**：自适应缩放因子 $\beta(a) = \beta(1 + \eta(1 - e^{-k(a-b)}))$ 引入了超参数 $b$、$\eta$、$k$，其对不同奖励分布和任务场景的敏感性缺乏理论分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/Aligning_Multi_Character_Narrative_Image_Generation_with_Multi_Aspect_Human_Preferences.pdf]]
