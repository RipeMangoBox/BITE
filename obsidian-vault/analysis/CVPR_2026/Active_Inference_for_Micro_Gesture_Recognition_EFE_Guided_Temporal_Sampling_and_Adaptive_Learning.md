---
title: "Active Inference for Micro-Gesture Recognition: EFE-Guided Temporal Sampling and Adaptive Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Active_Inference_for_Micro_Gesture_Recognition_EFE_Guided_Temporal_Sampling_and_Adaptive_Learning.pdf
project_link: null
code_link: null
aliases:
- AIMGREGTSAL
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 基于预期自由能（EFE）的主动时序/空间选择策略与基于MC Dropout的不确定性感知自适应样本加权（UMIX）机制。
primary_logic: 将微手势识别形式化为部分可观测马尔可夫决策过程下的主动推理问题，通过最小化变分自由能联合优化感知（特征提取）和行动（关键帧/区域选择），并引入不确定性驱动的数据增强以稳定噪声条件下的训练。
claims:
- 消融实验表明，分别添加不确定性感知、时序选择和空间选择模块均能提升基线准确率（50.49%→57.54%, 56.40%, 55.40%），三者结合达到63.47%（+12.98%）。
- 在SMG数据集上，UAAI以63.47%的RGB模态精度超越所有对比的RGB基线方法（如TRN 59.51%、TSM 58.69%），并将与最佳骨架方法MS-G3D（64.75%）的差距缩小至1.28个百分点。
- 蒙特卡洛采样数M=5在验证准确率、收敛速度和计算开销之间取得最优平衡。
- SMG 上 Accuracy (%) = 63.47
---

# Active Inference for Micro-Gesture Recognition: EFE-Guided Temporal Sampling and Adaptive Learning

> [!tip] 核心洞察
> 将微手势识别形式化为部分可观测马尔可夫决策过程下的主动推理问题，通过最小化变分自由能联合优化感知（特征提取）和行动（关键帧/区域选择），并引入不确定性驱动的数据增强以稳定噪声条件下的训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于主动推理的微手势识别：EFE引导的时序采样与自适应学习 |
| 英文题名 | Active Inference for Micro-Gesture Recognition: EFE-Guided Temporal Sampling and Adaptive Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.07559) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | UAAI |
| Dataset | SMG |

> [!tip] 效果简介
> - SMG 上，Accuracy (%) 63.47 vs 50.49 (无UAAI模块的基线) (+12.98)；Accuracy (%) 63.47 vs 59.51 (TRN, 最佳RGB基线) (+3.96)。

## 概述

微手势识别面临一个根本困境：现有深度模型被动处理全部时空信息，对瞬态、低幅度的局部运动缺乏敏感性，且无法量化预测不确定性，导致在低样本、噪声和跨个体场景下性能严重退化。本文提出**UAAI（Uncertainty-Aware Active Inference）**框架，将微手势识别形式化为部分可观测马尔可夫决策过程下的主动推理问题，通过最小化变分自由能联合优化感知（特征提取）与行动（关键帧/区域选择），并引入不确定性驱动的数据增强以稳定噪声条件下的训练。

核心思路围绕三个关键机制展开：**预期自由能（EFE）引导的时序选择**动态定位最具判别力的关键帧；**EFE引导的空间注意力**聚焦于降低不确定性的显著区域；**基于MC Dropout的不确定性感知混合增强（UMIX）**根据认知不确定性自适应重加权训练样本。三者统一在变分自由能最小化目标下协同工作。

在SMG数据集上，UAAI以**63.47%**的RGB模态准确率超越所有对比的RGB基线方法（如TRN 59.51%、TSM 58.69%），并将与最佳骨架方法MS-G3D（64.75%）的差距缩小至仅1.28个百分点。消融实验证实，三个模块各自独立均能带来显著增益（不确定性感知+7.05%、时序选择+5.91%、空间选择+4.91%），组合后达到+12.98%的累积提升。方法目前仅在单一数据集上验证，MC Dropout多次前向传递带来的计算开销也构成实时部署的潜在瓶颈，但其将主动推理引入微手势识别的技术路径为后续研究开辟了明确方向。

## 背景与动机

微手势（Micro-Gesture）是一种持续时间短、运动幅度低、空间范围局限的手部动作，在情感计算、人机交互和心理健康评估中具有重要应用价值。然而，微手势的瞬态性与低幅运动特性使其在视频流中极易被淹没在无关背景和冗余帧中，形成**时空稀疏性**瓶颈——有效判别信号仅存在于极少数关键帧的局部区域，其余大部分时空信息对识别贡献微弱甚至引入噪声。

现有深度学习方法普遍采用被动处理范式：在时间维度上均匀采样或使用全部帧，在空间维度上通过全局平均池化或固定感受野提取特征，并对所有训练样本施加均匀损失权重。这种“一刀切”策略导致三个关键缺陷：

1. **判别信息稀释**：模型无法自适应聚焦于高信息量的关键帧与显著区域，大量低质量时空特征稀释了本就微弱的微手势信号。
2. **预测过度自信**：标准Softmax输出缺乏对认知不确定性（epistemic uncertainty）的量化，模型在噪声样本、标注模糊或低质量输入条件下仍产生高置信度错误预测，严重损害鲁棒性。
3. **低样本与跨个体脆弱性**：微手势数据集通常规模有限且个体差异显著，均匀训练策略使模型对困难样本和分布外个体缺乏针对性学习，泛化能力不足。

上述问题的本质在于：**现有模型缺乏对“观察什么”和“何时观察”的主动决策能力**。它们被设计为从固定时空范围内被动提取特征，而非像人类视觉系统那样动态选择信息丰富的观测点以降低不确定性。这一认知缺口在微手势识别中尤为致命——因为判别信息的稀疏性要求模型必须精确锁定关键时空位置，而非平均分配计算资源。

针对上述缺口，本文提出**基于主动推理的微手势识别框架UAAI**，其核心动机是将识别过程形式化为部分可观测马尔可夫决策过程（POMDP）下的主动推理问题。通过最小化变分自由能（Variational Free Energy, VFE）联合优化感知（特征提取）与行动（关键帧/区域选择），模型获得主动选择高信息量观测的内在驱动力。具体而言，UAAI引入三个关键机制：

- **预期自由能（EFE）引导的时序选择**：动态评估每一帧的信息增益与认知价值，选择使期望自由能最小的关键帧子集，从源头滤除冗余信息。
- **EFE引导的空间注意力**：通过学习空间注意力掩码聚焦于降低预测不确定性的显著区域，使特征提取精准作用于微手势发生的局部空间。
- **不确定性感知自适应增强（UMIX）**：基于MC Dropout量化样本级认知不确定性，对高不确定性样本施加更高权重并执行软混合增强，充当隐式正则化器以稳定噪声条件下的训练。

通过将感知、选择和不确定性建模统一在变分自由能最小化框架下，UAAI实现了从“被动处理”到“主动观测”的范式转变，为低样本、高噪声的微手势识别场景提供了原理性解决方案。

## 核心创新

本工作将微手势识别重新定义为部分可观测马尔可夫决策过程下的**主动推理**问题，核心创新在于将感知（特征提取）与行动（关键帧/区域选择）统一在**变分自由能最小化**的框架下联合优化，并引入**不确定性驱动的自适应学习**机制以应对噪声与低质量样本。相对于现有被动处理所有时空信息的方法，UAAI 框架通过三个关键 **changed slots** 实现了从“被动接收”到“主动选择”的范式转换。

### 1. EFE 引导的主动时序选择

现有方法（如 TSM、TRN）或均匀采样、或使用所有帧进行全局池化，对微手势的**瞬态、低幅运动**不敏感，大量冗余帧稀释了判别性信息。UAAI 将帧选择形式化为一个**预期自由能（Expected Free Energy, EFE）最小化**问题：

$$a_t^* = \arg\min_{a_t \in \mathcal{A}} \mathbb{G}_t(a_t)$$

其中 EFE 定义为认知价值与信息增益之差：

$$\mathbb{G}_t(a_t) = \mathbb{E}_{q(o_{t+1}, s_{t+1} \mid a_t)} \big[ D_{\mathrm{KL}}(q(s_{t+1}|o_{t+1}) || p(s_{t+1}|o_{t+1})) - \mathbb{H}[(p(o_{t+1}|s_{t+1},a_t))] \big]$$

模型在每一时刻动态选择使 EFE 最小的帧作为关键帧，从而**最大化信息增益、最小化状态不确定性**。这一机制使模型能够自适应地聚焦于微手势发生的关键时刻，而非平均对待所有帧。消融实验证实，仅添加时序选择模块即可将基线准确率从 50.49% 提升至 56.40%（+5.91%，Table 2），且 EFE 引导的选择策略优于均匀采样、随机采样等替代方案（Table 3）。

### 2. EFE 引导的空间注意力掩码

微手势的判别性信息通常集中在手指关节、指尖等**局部显著区域**，而现有方法多采用全局平均池化，缺乏显式的空间加权。UAAI 通过学习一个可微的空间注意力掩码来聚焦于降低 EFE 的显著区域：

$$\mathbf{M} = \sigma(\mathrm{Conv}([\mathbf{F}_{avg}; \mathbf{F}_{max}]))$$

该掩码通过通道维度的平均/最大池化、拼接、卷积和 Sigmoid 激活生成，其优化目标与变分自由能最小化一致——掩码聚焦于能最大程度降低预测不确定性的空间位置。消融实验中，仅添加空间选择模块将准确率提升至 55.40%（+4.91%，Table 2），可视化结果（Figure 3）进一步表明模型确实学习关注手指和手部区域。

### 3. 不确定性感知的自适应样本加权（UMIX）

标准训练对所有样本施加均匀损失，在噪声标注或低质量样本存在时，模型容易对错误信号**过度自信**。UAAI 通过 MC Dropout 量化认知不确定性：

$$u(I) = \max_k \mathrm{Var}_t[\hat{p}_t(y=k|I)]$$

并据此计算样本权重与混合增强：

$$w_i = \exp(-\alpha \cdot u(I_i)) + \beta$$

$$\tilde{x} = \lambda x_i + (1-\lambda) x_j, \quad \tilde{y} = \lambda y_i + (1-\lambda) y_j$$

最终损失函数为不确定性加权的混合交叉熵：

$$\mathcal{L} = \mathbb{E}_{(x_i,y_i),(x_j,y_j)}[ w_i \lambda \mathcal{L}_{ce}(\theta, \tilde{x}, y_i) + w_j (1-\lambda) \mathcal{L}_{ce}(\theta, \tilde{x}, y_j) ]$$

这一机制实现了**隐式正则化**：高不确定性样本的权重被压低，降低其对梯度更新的干扰；同时通过 Mixup 增强在样本空间中构建更平滑的决策边界。消融实验表明，仅添加不确定性感知增强即可将基线准确率从 50.49% 大幅提升至 57.54%（+7.05%，Table 2），是三个模块中**单模块增益最大**的。收敛曲线（Figure 5）显示，UMIX 使训练更加稳定，减少了验证损失波动。

### 4. 三个 changed slots 的协同效应

三个模块并非孤立设计，而是在**变分自由能最小化**的统一目标下协同工作：时序选择决定“何时看”，空间选择决定“看哪里”，UMIX 决定“如何学”。三者结合将准确率推至 63.47%（+12.98%，Table 2），显著超越仅使用单一或两两组合的配置。这种协同效应源于：
- EFE 引导的时序/空间选择为不确定性估计提供了更干净的输入特征；
- 不确定性反馈又隐式地引导模型在训练中优先学习高置信度样本的判别模式；
- 三者共同实现了感知-行动-学习的闭环优化，而非传统的分离式流水线。

### 5. 与现有范式的本质区别

| 维度 | 现有方法 | UAAI |
|------|----------|------|
| 时序处理 | 被动使用所有帧或均匀采样 | EFE 引导的主动关键帧选择 |
| 空间注意 | 全局平均池化或无显式加权 | EFE 引导的可学习空间注意力掩码 |
| 样本利用 | 均匀损失（标准交叉熵） | MC Dropout 不确定性感知的自适应加权与混合 |
| 优化目标 | 仅最小化分类损失 | 联合最小化变分自由能（感知+行动） |

这一范式转换使 UAAI 在仅使用 RGB 模态的情况下达到 63.47% 的准确率，超越所有对比的 RGB 基线方法（如 TRN 59.51%、TSM 58.69%），并将与最佳骨架方法 MS-G3D（64.75%）的差距缩小至仅 1.28 个百分点（Table 1）——而骨架方法使用了额外的深度与关节坐标信息。

## 整体框架

UAAI 将微手势识别形式化为**部分可观测马尔可夫决策过程下的主动推理问题**，在一个统一的变分自由能最小化目标下联合优化感知（特征提取与分类）与行动（关键帧/关键区域的选择）。其核心洞察是：现有深度模型被动处理所有时空信息，对微手势的瞬态低幅运动与局部特征不敏感，且缺乏预测不确定性，导致在低样本、噪声和跨个体条件下性能严重退化。UAAI 通过引入**预期自由能（EFE）引导的主动选择策略**与**不确定性感知的自适应样本加权机制**，从两个层面打破这一瓶颈。

整体 pipeline 由四个核心模块串联构成，如图 Figure 2 所示：

![[assets/figures/papers/paper_list_l1052_https_arxiv_org_abs_2603_07559/figures/002_Figure_2.jpg]]
*Figure 2: Overall Framework. The framework enhances micro-gesture recognition performance through EFE-based temporal and spatial selection and uncertainty-aware augmentation under the active inference mechanism*

1. **EFE-guided Temporal Selection（时序选择）**：输入为视频帧序列。模块基于预期自由能最小化原则，动态评估每一帧的信息增益与认知价值，从中选择最具判别力的关键帧子集。该过程将帧选择形式化为动作选择问题，通过最小化期望自由能 $a_t^* = \arg\min_{a_t \in \mathcal{A}} \mathbb{G}_t(a_t)$ 来决定保留哪些帧，从而抑制冗余背景帧对微手势特征的干扰。

2. **EFE-guided Spatial Selection（空间选择）**：在选定的关键帧上，模块通过学习空间注意力掩码 $\mathbf{M} = \sigma(\mathrm{Conv}([\mathbf{F}_{avg}; \mathbf{F}_{max}]))$ 聚焦于能最大程度降低不确定性的显著区域（如手指、手部轮廓）。该掩码通过通道级平均/最大池化、拼接、卷积和 Sigmoid 激活以可微分方式生成，使空间选择与分类目标端到端联合优化。

3. **MC Dropout Uncertainty Estimation（不确定性估计）**：将 Dropout 作为贝叶斯近似，在训练和推理中通过 $T$ 次随机前向传递量化认知不确定性。对于输入样本 $I$，其不确定性得分定义为各类别预测方差的最大值：$u(I) = \max_k \mathrm{Var}_t[\hat{p}_t(y=k|I)]$。该得分反映了模型对当前样本预测的置信度缺失程度。

4. **UMIX Uncertainty-Aware Augmentation（不确定性感知增强）**：根据不确定性得分自适应地重加权训练样本，权重计算为 $w_i = \exp(-\alpha \cdot u(I_i)) + \beta$，使高不确定性（低质量/噪声）样本对损失的贡献被压低。同时引入软样本混合（Mixup）作为隐式正则化器，混合后的输入与标签分别为 $\tilde{x} = \lambda x_i + (1-\lambda) x_j$，$\tilde{y} = \lambda y_i + (1-\lambda) y_j$，最终训练损失为不确定性加权的混合交叉熵（Eq. 13）。

**模块间的输入输出流**：原始视频帧序列首先进入时序选择模块，输出稀疏的关键帧集合；关键帧随后经过空间选择模块，被赋予空间注意力掩码以突出显著区域；掩码加权后的特征送入分类骨干网络进行前向传递；MC Dropout 模块对每次前向传递的预测分布进行多次采样，输出不确定性得分；UMIX 模块利用该得分对训练样本进行重加权与混合，产生最终的训练损失信号。整个框架的优化目标统一在变分自由能最小化框架下：$\mathcal{F} = \mathbb{E}_{q(s|o)} [ -\log p(o|s) ] + \mathrm{KL}[q(s|o) \| p(s|o)]$，其中第一项对应分类准确度，第二项对应模型复杂度约束。

### 补充图表

![[assets/figures/papers/paper_list_l1052_https_arxiv_org_abs_2603_07559/figures/001_Figure_1.jpg]]
*Figure 1: Overview of existing methods and UAAI*

## 核心模块与公式推导

UAAI 框架将微手势识别形式化为部分可观测马尔可夫决策过程（POMDP）下的主动推理问题，其核心思想是在统一的变分自由能（VFE）最小化原则下联合优化感知（特征学习）与行动（观测选择）。框架包含三个关键模块：EFE 引导的时序选择、EFE 引导的空间选择，以及基于 MC Dropout 的不确定性感知增强（UMIX）。

### 变分自由能与预期自由能

主动推理的核心目标是最小化变分自由能 $\mathcal{F}$，其分解为准确度项与复杂度项：

$$\mathcal{F} = \mathbb{E}_{q(s|o)} [ -\log p(o|s) ] + \mathrm{KL}[q(s|o) \| p(s|o)]$$

其中 $q(s|o)$ 为近似后验，$p(o|s)$ 为观测似然，KL 散度项约束近似后验与先验的偏离。在行动选择层面，智能体通过最小化预期自由能（Expected Free Energy, EFE）$\mathbb{G}_t(a_t)$ 来选择最优动作：

$$a_t^* = \arg\min_{a_t \in \mathcal{A}} \mathbb{G}_t(a_t)$$

$$\mathbb{G}_t(a_t) = \mathbb{E}_{q(o_{t+1}, s_{t+1} \mid a_t)} \big[ D_{\mathrm{KL}}(q(s_{t+1}|o_{t+1}) || p(s_{t+1}|o_{t+1})) - \mathbb{H}[(p(o_{t+1}|s_{t+1},a_t))] \big]$$

EFE 由两项构成：认知价值项（KL 散度，衡量后验与先验的差异，即信息增益）与实用价值项（负熵，衡量观测不确定性）。最小化 EFE 等价于选择能最大化信息增益同时最小化预期不确定性的观测动作。

### EFE 引导的时序选择

在微手势视频中，并非所有帧都包含判别性信息。时序选择模块将帧选择形式化为主动推理中的动作选择：智能体在每个时间步决定是否选取当前帧作为关键帧。观测似然通过似然矩阵建模：

$$A_{a_t}(i,j) = p(o=j | s=i)$$

该矩阵编码了在动作 $a_t$ 下观测 $o$ 与隐状态 $s$ 之间的映射关系。通过计算各候选帧对应的 EFE 值，模型动态选择使 EFE 最小的帧子集，从而聚焦于最具信息量的时序片段。消融实验（Table 2）表明，单独添加时序选择模块将基线准确率从 50.49% 提升至 56.40%（+5.91%）。

### EFE 引导的空间选择

空间选择模块通过学习空间注意力掩码，使模型聚焦于能最大程度降低不确定性的显著区域。整体 EFE 被近似为空间局部贡献之和：

$$G_t \approx \sum_i G_{t,i}$$

空间注意力掩码通过通道池化与卷积操作生成：

$$\mathbf{M} = \sigma(\mathrm{Conv}([\mathbf{F}_{avg}; \mathbf{F}_{max}]))$$

其中 $\mathbf{F}_{avg}$ 和 $\mathbf{F}_{max}$ 分别为沿通道维度的平均池化和最大池化特征，$[\cdot;\cdot]$ 表示通道拼接，$\mathrm{Conv}$ 为卷积操作，$\sigma$ 为 Sigmoid 激活函数。该可微分掩码使模型能够端到端地学习空间注意力分布，与 EFE 最小化目标一致。消融实验（Table 2）显示，单独添加空间选择模块将准确率提升至 55.40%（+4.91%）。

### 不确定性感知增强（UMIX）

为应对噪声和低质量样本导致的过度自信问题，UMIX 模块通过 MC Dropout 量化认知不确定性，并据此自适应地重加权训练样本。对于输入 $I$，进行 $T$ 次随机前向传递，计算各类别预测方差的极大值作为不确定性分数：

$$u(I) = \max_k \mathrm{Var}_t[\hat{p}_t(y=k|I)]$$

其中 $\hat{p}_t(y=k|I)$ 为第 $t$ 次前向传递中类别 $k$ 的预测概率。样本权重根据不确定性指数衰减：

$$w_i = \exp(-\alpha \cdot u(I_i)) + \beta$$

其中 $\alpha$ 控制衰减速率，$\beta$ 为权重下界。高不确定性样本获得较低权重，降低其对训练的负面影响。UMIX 进一步将不确定性加权与 Mixup 增强结合：

$$\tilde{x} = \lambda x_i + (1-\lambda) x_j, \quad \tilde{y} = \lambda y_i + (1-\lambda) y_j$$

其中 $\lambda \sim \mathrm{Beta}(\alpha, \alpha)$（$\alpha=0.4$）。最终训练损失为不确定性加权的混合交叉熵：

$$\mathcal{L} = \mathbb{E}_{(x_i,y_i),(x_j,y_j)}[ w_i \lambda \mathcal{L}_{ce}(\theta, \tilde{x}, y_i) + w_j (1-\lambda) \mathcal{L}_{ce}(\theta, \tilde{x}, y_j) ]$$

该机制充当隐式正则化器，在不稳定样本上平滑损失景观。消融实验（Table 2）表明，单独添加 UMIX 将准确率从 50.49% 提升至 57.54%（+7.05%），是三个模块中增益最大的组件。蒙特卡洛采样数 $M=5$ 在验证准确率、收敛速度与计算开销之间取得最优平衡（Figure 6, Table 4）。

## 实验与分析

### 主实验结果

UAAI 在 SMG 数据集上与 12 个基线方法进行了对比，涵盖 RGB 模态与骨架模态。**Table 1** 报告了各方法的准确率。UAAI 仅使用 RGB 输入即达到 **63.47%** 的准确率，显著超越所有 RGB 基线：相较于此前最佳的 **TRN**（59.51%）提升 **+3.96** 个百分点，较 **TSM**（58.69%）提升 +4.78 个百分点，较 **C3D**（51.84%）提升 +11.63 个百分点。与利用额外骨架模态的最强方法 **MS-G3D**（64.75%）相比，差距缩小至仅 **1.28** 个百分点。这一结果表明，主动推理驱动的时序/空间选择与不确定性感知增强，在仅使用 RGB 的条件下已能逼近多模态骨架方法的性能上限。

![[assets/figures/papers/paper_list_l1052_https_arxiv_org_abs_2603_07559/figures/003_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art methods on the SMG dataset in different modalities. * denotes our framework*

### 消融实验

为量化各模块的独立贡献与协同效应，论文进行了系统消融（**Table 2**）。基线模型（无任何 UAAI 模块）准确率为 **50.49%**。

![[assets/figures/papers/paper_list_l1052_https_arxiv_org_abs_2603_07559/figures/004_Table_2.jpg]]
*Table 2: Module Ablation Experiments*

- **仅添加不确定性感知增强（UMIX）**：准确率提升至 **57.54%**（+7.05%），为单模块增益最大项，表明对噪声/低质量样本的自适应重加权是性能提升的核心驱动力。
- **仅添加 EFE 引导的时序选择**：准确率提升至 **56.40%**（+5.91%），验证了动态关键帧选择对捕获微手势瞬态信息的有效性。
- **仅添加 EFE 引导的空间选择**：准确率提升至 **55.40%**（+4.91%），说明聚焦手部显著区域可稳定特征提取。
- **三模块组合**：准确率达到 **63.47%**（+12.98%），增益超过各模块独立增益之和，表明时序选择、空间注意力与不确定性增强之间存在显著的协同效应。

### 帧选择策略对比

**Table 3** 对比了不同帧选择方法。EFE 引导的主动选择策略优于均匀采样、随机采样等被动策略，验证了基于预期自由能最小化的选择机制能够识别最具判别力的关键帧，而非无差别处理所有时序信息。

### 蒙特卡洛采样数的影响

**Figure 6** 与 **Table 4** 展示了不同蒙特卡洛采样数 M 下的准确率曲线与训练开销。M=5 在验证准确率、收敛速度与计算开销之间取得最优平衡：更大的 M 值虽略微提升不确定性估计精度，但训练时间显著增加，而边际准确率增益递减。这一发现为实际部署中的效率-性能权衡提供了经验依据。

### 收敛性分析

**Figure 4** 显示 UAAI 在约 40 个 epoch 后稳定收敛，准确率与损失曲线平滑，未出现严重过拟合。**Figure 5** 进一步对比了有无 UMIX 的收敛曲线：引入 UMIX 后，训练初期收敛速度更快，且验证损失波动显著减小，证实不确定性驱动的样本混合充当了有效的隐式正则化器，抑制了对噪声样本的过度拟合。

### 主动观测可视化

**Figure 3** 的可视化结果表明，模型通过 EFE 引导的空间注意力成功聚焦于手指尖端、指间区域等微手势的关键部位，而非背景或无关区域。这为空间选择模块的实际效果提供了定性支撑。

### 局限性与待验证问题

尽管 UAAI 在 SMG 数据集上表现优异，以下局限需注意：

1. **跨数据集泛化未验证**：所有实验仅在 SMG 单一数据集上进行，方法在其他微手势数据集或真实场景中的有效性尚待检验。
2. **计算开销**：不确定性估计依赖 MC Dropout 的多次前向传递（M=5），增加了训练与推理成本，可能不适用于严格实时场景。
3. **MDP 简化假设**：主动时序选择基于部分可观测 MDP 的简化设定，实际部署中帧选择的延迟效应与环境反馈未被建模。
4. **模态扩展性未知**：当前仅使用 RGB 模态，主动推理框架能否有效融合骨架、深度等多模态信息以进一步提升性能，仍需探索。
5. **鲁棒性边界**：UMIX 在严重标注错误或开放集条件下的表现尚未评估，不确定性权重机制在分布外样本上的行为值得进一步研究。

### 补充图表

![[assets/figures/papers/paper_list_l1052_https_arxiv_org_abs_2603_07559/figures/005_Table_3.jpg]]
*Table 3: Comparison of frame selection methods*

![[assets/figures/papers/paper_list_l1052_https_arxiv_org_abs_2603_07559/figures/006_Figure_3.jpg]]
*Figure 3: Active Observation Visualization*

![[assets/figures/papers/paper_list_l1052_https_arxiv_org_abs_2603_07559/figures/007_Figure_4.jpg]]
*Figure 4: Convergence curves of UAAI under different training epochs. The upper row shows accuracy curves, and the lower row shows corresponding loss curves. The model converges stably after around 40 epochs*

![[assets/figures/papers/paper_list_l1052_https_arxiv_org_abs_2603_07559/figures/008_Figure_5.jpg]]
*Figure 5: Convergence curves with and without the UMIX*

![[assets/figures/papers/paper_list_l1052_https_arxiv_org_abs_2603_07559/figures/009_Figure_6.jpg]]
*Figure 6: Accuracy and loss Curves under different Monte Carlo sampling numbers M*

![[assets/figures/papers/paper_list_l1052_https_arxiv_org_abs_2603_07559/figures/010_Table_4.jpg]]
*Table 4: Training cost under different M*

## 方法谱系与知识库定位

**主动推理与微手势识别的交叉定位。** 现有微手势识别方法可大致分为两类：基于骨架的方法（如 **ST-GCN**、**2S-GCN**、**Shift-GCN**、**MS-G3D**、**GCN-NAS**）和基于RGB视频的方法（如 **C3D**、**TSN**、**TSM**、**TRN**、**MA-Net**、**MSTCN-VAE**、**Video Mamba**）。这两类方法的共同假设是模型被动接收全部时空信息，通过增大感受野或图拓扑来捕获微手势的细微运动。UAAI的方法论突破在于将微手势识别从“被动感知”范式迁移到“主动推理”范式——将识别过程形式化为部分可观测马尔可夫决策过程（POMDP）下的变分自由能最小化问题。这一框架的理论根源来自Karl Friston的主动推理理论，但在计算机视觉的动作识别领域尚属罕见的系统性应用。

**与不确定性感知学习的谱系关系。** 在训练样本加权方面，UAAI的UMIX模块与现有的不确定性感知学习（如MC Dropout、Deep Ensembles、Loss Weighting by Predictive Variance）存在继承与差异。继承之处在于使用MC Dropout的预测方差作为认知不确定性的代理量；差异之处在于UAAI将不确定性得分同时作用于样本混合权重和Mixup正则化，形成双重自适应机制。与标准Mixup（Zhang et al., ICLR 2018）的均匀Beta采样不同，UMIX的混合权重由不确定性指数衰减函数 $w_i = \exp(-\alpha \cdot u(I_i)) + \beta$ 调制，使高不确定性样本的混合更保守，低不确定性样本的混合更激进。这一设计在噪声鲁棒性方面的理论优势在于：高不确定性样本的标签可能不可靠，过度混合会放大噪声传播，而低不确定性样本的标签可信度高，混合可有效扩充决策边界。

**时序选择策略的对比定位。** 在关键帧选择方面，UAAI的EFE引导时序选择与现有的硬注意力（如基于强化学习的帧采样）、软注意力（如Non-local、Transformer自注意力）和均匀采样策略形成对比（Table 3）。EFE选择的独特之处在于其选择标准直接与任务目标对齐——最小化预期自由能等价于最大化信息增益减去风险，而非仅依赖注意力权重或启发式重要性分数。这使得选择过程具有贝叶斯最优性的理论保证，但代价是需要维护似然矩阵 $A_{a_t}(i,j) = p(o=j | s=i)$ 并计算期望自由能 $\mathbb{G}_t(a_t)$。

**适用边界与局限。** UAAI的适用边界受到以下因素制约：(1) **数据集单一性**——目前仅在SMG数据集上验证，该数据集为实验室受控环境下的孤立微手势，跨数据集、跨场景（如野外、多人交互）的泛化能力未经验证；(2) **计算开销**——不确定性估计需要 $T=5$ 次MC前向传递，训练时每步增加约5倍的前向计算量（Table 4），推理时若保留不确定性估计则同样存在延迟，不适合严格实时（<10ms）场景；(3) **POMDP简化假设**——主动时序选择基于离散动作空间和简化的状态转移模型，实际应用中帧选择的延迟效应、环境动态变化和长期规划未纳入建模；(4) **模态限制**——当前框架仅使用RGB模态，虽然已将RGB与骨架方法的差距缩小至1.28个百分点（63.47% vs. 64.75%的MS-G3D），但未探索EFE引导的多模态主动融合。

**开放问题。** (1) 主动推理框架能否扩展到多模态输入（如RGB+骨架+深度），通过EFE联合选择模态和时空区域？(2) 在严重标注错误（label noise > 30%）或开放集条件下，UMIX的不确定性权重机制是否仍能保持鲁棒性，还是需要引入分布外检测模块？(3) 在线实时微手势识别中，如何在EFE计算的精度与决策延迟之间取得平衡——是否可以用轻量化的EFE近似（如摊销推理网络）替代精确的期望自由能计算？(4) 该框架在更复杂的日常手势交互场景（如连续手语、驾驶员手势控制）中的有效性和适应性如何？这些问题的探索将决定主动推理范式在视频理解领域的扩散深度。

## 原文 PDF

![[paperPDFs/CVPR_2026/Active_Inference_for_Micro_Gesture_Recognition_EFE_Guided_Temporal_Sampling_and_Adaptive_Learning.pdf]]
