---
title: Weakly Supervised Motion Learning for Co-speech Gesture Video Generation
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Weakly_Supervised_Motion_Learning_for_Co_speech_Gesture_Video_Generation.pdf
aliases:
- WSMLF
- WSMLCSGVG
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 通过可逆特征提取器将音频映射到隐式运动表征空间，替代显式姿态监督，实现纯音频-视频训练。
primary_logic: 仅用视频即可学习可泛化的运动表征，结合可逆流实现高效音频驱动手势合成，无需中间姿态标注。
claims:
- 在四个客观指标（FGD、Diversity、BAS、FVD）上均超越S2G、MYA、EchoMimicV2
- 移除可逆特征提取器导致FGD从1.47急剧升至45.73
- Stage 1运动编码器达到FGD 0.92和BAS 0.7601，代表最终模型性能上限
- 手部细化使平均手部置信度从88.73%提升至95.45%
---

# Weakly Supervised Motion Learning for Co-speech Gesture Video Generation

> [!tip] 核心洞察
> 仅用视频即可学习可泛化的运动表征，结合可逆流实现高效音频驱动手势合成，无需中间姿态标注。

| 字段 | 内容 |
|------|------|
| 中文题名 | 弱监督协同语音手势视频生成 |
| 英文题名 | Weakly Supervised Motion Learning for Co-speech Gesture Video Generation |
| 会议/期刊 | ICLR 2026 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | Weakly Supervised Motion Learning Framework |
| Dataset | PATS |

> [!tip] 效果简介
> - PATS (4 speakers) 上，FGD ↓ 1.11 vs 3.69 (S2G) (-2.58)；Diversity ↑ 282.89 vs 180.59 (S2G) (+102.30)；BAS ↑ 0.7526 vs 0.7280 (S2G) (+0.0246)。

## 概述

### 问题与瓶颈

协同语音手势视频生成（co-speech gesture video generation）旨在根据语音音频合成与说话内容同步的自然手势视频。传统方法（如 **S2G**、**MYA**、**EchoMimicV2**）通常采用两阶段流程：先从音频生成显式姿态表示（如关键点或密集姿态图），再通过姿态驱动视频生成。这一范式存在根本性瓶颈——训练依赖大量精确的姿态标注，标注过程耗时且易引入误差，导致生成的手势细节（尤其是手部区域）模糊、手指扭曲，且对说话人位置变化高度敏感。

### 核心思路

本文提出一种**弱监督运动学习框架（Weakly Supervised Motion Learning Framework）**，从根本上消除了对姿态标注的依赖。其核心洞察在于：**仅利用原始视频即可学习可泛化的隐式运动表征，结合可逆流模型实现高效的音频到运动映射，无需中间姿态监督。** 方法通过三个关键阶段实现这一目标：

1. **运动编码器**从视频中学习可泛化的运动表征（无姿态监督）；
2. **双塔架构**配合**可逆特征提取器**将音频映射到隐式运动空间，实现音频-运动对齐；
3. **视频扩散模型**注入运动表征以增强细节，并通过**基于策略梯度的初始噪声优化**对手部区域进行专门细化。

### 方法定位

从方法谱系看，该框架在以下维度实现了突破：

- **监督信号**：从“需要姿态标注”转向“仅需音频和视频”，大幅降低数据获取成本；
- **运动提取**：从“显式关键点/姿态图”转向“可泛化的隐式运动表征”，提升对细节的建模能力；
- **音频-运动映射**：从“生成式模型（扩散/VAE）或检索”转向“双塔+可逆流（RealNVP）直接映射”，实现高效对齐；
- **手部生成**：从“无专门细化”转向“基于强化学习的初始噪声优化”，显著改善手部质量。

### 主要结果

在PATS数据集（4位说话人）上的定量评估表明，该方法在四项客观指标上全面超越现有方法：

| 指标 | 本文方法 | S2G（最佳基线） | 提升 |
|------|---------|---------------|------|
| FGD ↓ | **1.11** | 3.69 | −2.58 |
| Diversity ↑ | **282.89** | 180.59 | +102.30 |
| BAS ↑ | **0.7526** | 0.7280 | +0.0246 |
| FVD ↓ | **626.58** | 816.03 | −189.45 |

消融实验揭示了各组件的决定性作用：移除可逆特征提取器导致FGD从1.47急剧恶化至45.73（Table 3）；手部细化将平均手部置信度从88.73%提升至95.45%（Table 5）；缺少运动信息使FVD从660.73飙升至2406.91（Table 6）。Stage 1运动编码器达到FGD 0.92和BAS 0.7601，代表最终模型的理论性能上限（Table 2）。

主观用户研究进一步验证了方法的优势：在身份保持、视觉质量、时序一致性和语音-手势同步性四个维度上均获得最高评分（3.53–3.73），且统计检验（t检验）表明优势显著（Table 7–9）。

## 背景与动机

协同语音手势（co-speech gesture）是人类沟通中不可或缺的非语言信号，能够增强表达力、传达情感并辅助语义理解。在虚拟人、数字人主播、游戏角色动画等应用中，高质量、音频同步的手势视频生成具有广泛需求。然而，实现这一目标面临两个核心挑战：**手势生成的准确性**与**训练数据的获取成本**。

传统方法通常采用两阶段流水线：先从音频预测人体姿态（如关键点或密集姿态表征），再基于姿态生成视频。例如，**S2G**（He et al., 2024）设计了专门的协同语音手势视频生成框架，**MYA**（Huang et al., 2024）和 **EchoMimicV2**（Meng et al., 2024）则将姿态图像引导的视频生成方法适配到该任务。这类范式虽然取得了一定进展，但存在一个根本性瓶颈：**依赖大量姿态标注**。

姿态标注的获取成本极高，不仅耗时费力，还容易引入标注错误。这些错误会在两阶段流水线中逐级放大：不准确的姿态预测导致生成视频中的手势失真，尤其是手部细节——手指形态模糊、扭曲等伪影频发（见 Figure 3 红圈标注）。此外，显式姿态表征对位置变化高度敏感，限制了模型在复杂场景下的泛化能力。

从因果机制来看，问题的症结在于：**显式姿态监督并非手势生成的必要条件，而是一种冗余的中间表征**。如果能直接从音频学习到可泛化的运动表征，并端到端地驱动视频生成，则有望同时解决标注成本高和手势质量差两大难题。

本文的核心动机正是基于这一洞察：**仅利用音频和视频数据，无需任何姿态标注，能否实现高质量的协同语音手势视频生成？** 为此，我们提出了一个弱监督运动学习框架，通过可逆特征提取器将音频映射到隐式运动表征空间，替代显式姿态监督，从根本上消除对姿态标注的依赖（见 Figure 1）。这一设计不仅大幅降低了数据获取门槛，还使模型能够学习更鲁棒、更丰富的运动表征，为后续的手势细节（尤其是手部）优化奠定了基础。

## 核心创新

本文的核心创新在于**彻底移除了协同语音手势视频生成对姿态标注的依赖**，构建了一个纯音频-视频驱动的弱监督学习框架。传统方法（如 **S2G** (He et al., 2024)、**MYA** (Huang et al., 2024)、**EchoMimicV2** (Meng et al., 2024)）在训练时均需额外的姿态标注（关键点或密集姿态），这不仅标注成本高昂，还容易引入标注误差，导致生成的手势细节（尤其是手部）出现模糊和畸变（Figure 1）。本文通过三个关键的“changed slots”实现了范式转变：

1.  **训练监督信号：从“显式姿态标注”到“隐式运动表征”**
    核心瓶颈在于姿态标注的获取与质量。本文的方案是完全放弃显式姿态监督，转而利用**可逆特征提取器**（基于RealNVP耦合层）将音频直接映射到从视频中学习的隐式运动表征空间，从而在训练中仅需音频和视频数据（Figure 1, Sec 3.2.2）。这直接绕开了姿态标注的成本与误差问题，是方法成立的根基。

2.  **运动提取：从“显式关键点”到“可泛化隐式运动表征”**
    传统方法依赖显式关键点运动或姿态图像作为中间表达。本文的**运动编码器**（Motion Encoder）以EVA-CLIP视觉模型初始化，仅通过视频输入和潜扩散模型损失（$\mathcal{L}_{\mathrm{LDM}}$）进行训练，学习到一个可泛化的隐式运动表征（Sec 3.2.1）。该表征不绑定特定人体结构，为后续的音频对齐提供了更鲁棒的基础。

3.  **音频-运动映射：从“生成式检索”到“双塔+可逆流直接映射”**
    不同于使用扩散模型、VAE或检索等方式，本文采用**双塔架构**（音频编码器+运动编码器）配合**可逆特征提取器**（RealNVP），通过联合优化MSE、intra-/inter-对比损失和流损失（$\mathcal{L} = \alpha \mathcal{L}_{\mathrm{MSE}} + \beta \mathcal{L}_{\mathrm{Intra}} + \gamma \mathcal{L}_{\mathrm{Inter}} + \delta \mathcal{L}_{\mathrm{Flow}}$），实现了音频到运动表征的精确、可逆的对齐（Sec 3.2.2）。消融实验（Table 3）证实，移除该可逆模块会导致FGD从1.47急剧恶化至45.73，证明了该映射机制的核心作用。

4.  **手部细节：从“无专门处理”到“基于策略梯度的初始噪声优化”**
    针对手部生成这一长期难点，本文提出在采样阶段对扩散模型的初始高斯噪声参数$\mu$和$\sigma$进行基于策略梯度的优化（$\mathcal{L} = - \log p(\boldsymbol{z}_t) \cdot \boldsymbol{r}$），无需额外网络模块即可显著提升手部质量（Sec 3.3）。该设计使平均手部置信度从88.73%提升至95.45%（Table 5），补足了扩散模型在精细部位生成的短板。

## 整体框架

本文提出一种**弱监督运动学习框架**，仅以音频和视频作为训练输入，从根本上规避了传统方法对姿态标注（关键点/密集姿态）的依赖。框架由三个序贯阶段和一个采样时的手部细化策略构成，如 Figure 2 所示。

### 三阶段流水线

**Stage 1 — 运动学习**：在仅有视频输入的条件下，训练一个运动编码器（Motion Encoder）学习可泛化的隐式运动表征。该编码器以预训练的 EVA-CLIP 视觉模型为初始化，并通过线性层降维以控制内存开销。训练时仅优化运动编码器，目标为潜扩散模型的噪声预测均方误差损失 $\mathcal{L}_{\mathrm{LDM}}$。

**Stage 2 — 音频-运动映射**：冻结运动编码器，引入双塔架构实现音频与运动表征的对齐。音频编码器提取 MFCC 和 HuBERT 特征，经时序自注意力融合后，与运动编码器输出的运动表征通过可逆特征提取器（基于 RealNVP 耦合层）映射到联合空间。该阶段的总损失为四项的加权组合：

$$
\mathcal{L} = \alpha \mathcal{L}_{\mathrm{MSE}} + \beta \mathcal{L}_{\mathrm{Intra}} + \gamma \mathcal{L}_{\mathrm{Inter}} + \delta \mathcal{L}_{\mathrm{Flow}}
$$

其中 $\mathcal{L}_{\mathrm{Intra}}$ 和 $\mathcal{L}_{\mathrm{Inter}}$ 分别为片段内和跨片段的对比损失，$\mathcal{L}_{\mathrm{Flow}}$ 为归一化流的负对数似然损失。

**Stage 3 — 特征精化**：基于 I2VGen-XL 的视频扩散模型，通过交叉注意力注入 Stage 2 输出的运动表征，对视频细节进行增强。该阶段显著提升 FVD 指标（从 932.56 降至 660.73），改善视觉质量。

### 手部细化策略

在采样阶段，将扩散模型的初始高斯噪声参数 $\mu$ 和 $\sigma$ 视为可学习参数，采用策略梯度方法进行优化。具体而言，以 $\mathcal{N}(\mu, \sigma^2)$ 为策略 $\pi$，采样的潜变量 $\boldsymbol{z}_t$ 为动作，通过负对数概率与手部检测置信度奖励 $\boldsymbol{r}$ 的乘积构建损失：

$$
\mathcal{L} = -\log p(\boldsymbol{z}_t) \cdot \boldsymbol{r}
$$

该策略将平均手部置信度从 88.73% 提升至 95.45%，有效改善了手部模糊和手指畸变等常见伪影。

### 数据流与模块关系

推理时，音频经音频编码器提取特征后，通过可逆特征提取器的逆向过程映射到运动表征空间，再经视频扩散模型和手部细化生成最终视频帧。整个流程不引入任何姿态标注，实现了从音频到视频的端到端驱动。

### 补充图表

![[assets/figures/papers/paper_list_l1909_Weakly_Supervised_Motion_Learning_for_Co_speech_Gesture_Video_Generation/figures/001_Figure_1.jpg]]
*Figure 1: During training, previous methods (Corona et al., 2024; Huang et al., 2024; He et al., 2024; Li et al., 2025) often require additional pose annotations, which are time-consuming and prone to labeling errors. In contrast, our approach relies solely on audio and video data, eliminating the need for pose supervision*

![[assets/figures/papers/paper_list_l1909_Weakly_Supervised_Motion_Learning_for_Co_speech_Gesture_Video_Generation/figures/002_Figure.jpg]]

## 核心模块与公式推导

### 3.1 基础组件公式

#### 3.1.1 潜扩散模型（LDM）损失

本文的视频生成骨干基于潜扩散模型（Latent Diffusion Model, LDM），其训练目标为标准噪声预测均方误差：

$$
\mathcal{L}_{\mathrm{LDM}} = \mathbb{E}_{z,\epsilon \sim \mathcal{N}(0,1),t} \left[ \| \epsilon - \epsilon_{\theta}(z_t, t, c) \|_2^2 \right]
$$

其中 $z$ 为潜空间编码，$\epsilon$ 为标准高斯噪声，$t$ 为扩散时间步，$c$ 为条件信号，$\epsilon_{\theta}$ 为噪声预测网络。该损失在 Stage 1 中用于训练运动编码器（仅优化编码器参数），在 Stage 3 中用于特征精化阶段的视频生成训练。

#### 3.1.2 归一化流基础

可逆特征提取器基于 RealNVP 架构的耦合层实现。耦合层正变换定义为：

$$
\mathbf{y}_a = \mathbf{x}_a, \quad \mathbf{y}_b = \mathbf{x}_b \odot \exp(s(\mathbf{x}_a)) + t(\mathbf{x}_a)
$$

其中 $\mathbf{x} = (\mathbf{x}_a, \mathbf{x}_b)$ 为输入分割，$\mathbf{y} = (\mathbf{y}_a, \mathbf{y}_b)$ 为输出，$s(\cdot)$ 和 $t(\cdot)$ 为任意可学习神经网络（尺度函数和平移函数），$\odot$ 表示逐元素乘法。该耦合层的雅可比行列式可高效计算，使得逆向过程（$\mathbf{x} = f^{-1}(\mathbf{y})$）同样可行。

归一化流的训练目标为负对数似然损失：

$$
\mathcal{L}_{\mathrm{Flow}} = -\log p(\mathbf{z}) - \sum_{i=1}^{L} \log \left| \det \frac{\partial f_i(\mathbf{x})}{\partial \mathbf{x}} \right|
$$

其中 $p(\mathbf{z})$ 为隐空间先验分布（通常为标准高斯），$f_i$ 为第 $i$ 个耦合层变换，$L$ 为总层数。该损失确保可逆映射将运动表征变换到与音频特征对齐的联合空间，同时保持概率密度可追踪。

#### 3.1.3 策略梯度优化

手部细化阶段将初始噪声优化建模为强化学习问题，采用策略梯度更新：

$$
\nabla_{\theta} J(\theta) = \mathbb{E}_{\tau \sim \pi_{\theta}} \left[ \sum_{t=0}^{T} \nabla_{\theta} \log \pi_{\theta}(a_t | s_t) r_t \right]
$$

其中 $\theta$ 为可学习参数（此处为高斯分布的均值 $\mu$ 和标准差 $\sigma$），$\pi_{\theta}$ 为策略（即 $\mathcal{N}(\mu, \sigma^2)$），$a_t$ 为采样动作（即采样的潜变量 $\mathbf{z}_t$），$r_t$ 为奖励信号（基于手部检测置信度）。通过最大化期望奖励来优化噪声分布，使扩散模型在手部区域生成更高质量的结果。

### 3.2 关键模块设计

#### 3.2.1 运动编码器（Stage 1）

运动编码器从预训练的 EVA-CLIP 视觉模型初始化，并附加线性层降维以优化内存效率。在 Stage 1 中，仅运动编码器参与训练，优化目标为 $\mathcal{L}_{\mathrm{LDM}}$。该阶段学习从视频帧中提取可泛化的隐式运动表征，无需任何姿态标注监督。根据 Table 2，Stage 1 模型达到 FGD 0.92 和 BAS 0.7601，代表最终模型的性能上限。

#### 3.2.2 音频-运动对齐（Stage 2）

音频编码器提取 MFCC 和 HuBERT 特征，通过时序自注意力机制融合。可逆特征提取器（基于 RealNVP 耦合层）将运动表征映射到音频-运动联合空间，并支持从音频到运动的逆向生成。

Stage 2 的联合训练损失为四项损失的加权组合：

$$
\mathcal{L} = \alpha \mathcal{L}_{\mathrm{MSE}} + \beta \mathcal{L}_{\mathrm{Intra}} + \gamma \mathcal{L}_{\mathrm{Inter}} + \delta \mathcal{L}_{\mathrm{Flow}}
$$

各项含义如下：
- **$\mathcal{L}_{\mathrm{MSE}}$**：音频嵌入与运动嵌入之间的均方误差，提供直接的回归监督。
- **$\mathcal{L}_{\mathrm{Intra}}$**：片段内对比损失，对同一视频片段内的音频嵌入 $\mathbf{o}_{i,k}$ 和运动嵌入 $\mathbf{m}_{f_{i,k}}$ 进行正样本对齐，温度参数为 $\kappa$。
- **$\mathcal{L}_{\mathrm{Inter}}$**：片段间对比损失，在批次内区分不同片段的音频-运动对，增强表征判别性。
- **$\mathcal{L}_{\mathrm{Flow}}$**：归一化流负对数似然损失，确保可逆映射的概率密度可追踪。

Table 4 的消融实验验证了各损失项的必要性，组合使用 Intra、Inter 和 MSE 损失可达到最佳性能平衡。

#### 3.2.3 视频扩散模型与特征精化（Stage 3）

基于 I2VGen-XL 的特征精化阶段，通过交叉注意力机制将 Stage 2 生成的隐式运动表征注入扩散模型，增强生成视频的细节质量。该阶段显著改善 FVD（从 932.56 降至 660.73，Table 2），但对 FGD 和 BAS 的改善幅度较小。

#### 3.2.4 手部细化

采样阶段通过策略梯度优化高斯参数 $\mu$ 和 $\sigma$，损失函数为：

$$
\mathcal{L} = -\log p(\mathbf{z}_t) \cdot \mathbf{r}
$$

其中 $p(\mathbf{z}_t)$ 为当前噪声分布下采样潜变量 $\mathbf{z}_t$ 的概率，$\mathbf{r}$ 为基于手部检测置信度的奖励信号。该损失通过负对数概率与奖励的乘积来引导噪声优化方向，使扩散模型在手部区域生成更精细的结果。Table 5 显示手部细化将平均手部置信度从 88.73% 提升至 95.45%。

### 3.3 各阶段关系与信息流

三阶段训练遵循冻结-顺序优化策略：
1. **Stage 1**：仅训练运动编码器，学习视频到运动表征的映射。
2. **Stage 2**：冻结运动编码器，训练音频编码器和可逆特征提取器，建立音频到运动表征的双向映射。
3. **Stage 3**：冻结前两阶段模块，训练视频扩散模型进行特征精化，并在采样时施加手部细化。

Table 3 的消融实验表明，移除可逆特征提取器导致 FGD 从 1.47 急剧升至 45.73，FVD 从 932.56 升至 2156.39，验证了可逆映射在音频-运动对齐中的关键作用。Table 6 进一步证明，完全移除运动信息输入（仅用音频训练）导致 FVD 从 660.73 恶化至 2406.91，确认运动表征对视频质量的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l1909_Weakly_Supervised_Motion_Learning_for_Co_speech_Gesture_Video_Generation/figures/006_Figure_4.jpg]]
*Figure 4: As shown, Stage 1 and Stage 2 produce well-aligned gestures but lack fine-grained details. Removing the invertible feature extractor in Stage 2 results in misaligned gestures and degraded visual quality. While Stage 3 enhances visual quality, it still struggles with hand generation. By applying our hand refinement method, the final model generates high-quality videos. Please zoom in for better visibility of details. Video results are shown in Supplementary Material*

## 实验与分析

### 主实验结果

本文在自采集的PATS数据集（4位演讲者）上，与三类代表性方法进行了全面对比：专门设计的协同语音手势视频生成方法 **S2G**（He et al., 2024）、姿态图像引导视频生成方法 **MYA**（Huang et al., 2024），以及零样本音频驱动视频生成方法 **EchoMimicV2**（Meng et al., 2024）。为保障公平性，所有基线均在相同训练/测试划分下微调；对MYA和EchoMimicV2，先通过DiffSHEG生成姿态图像作为输入。

**Table 1** 展示了四项客观指标的定量对比。本文方法在所有指标上均取得最优：

- **FGD ↓**：1.11，较次优的S2G（3.69）降低2.58，表明生成手势与真实手势分布高度一致。
- **Diversity ↑**：282.89，较S2G（180.59）提升102.30，证明手势多样性显著增强。
- **BAS ↑**：0.7526，较S2G（0.7280）提升0.0246，反映音频-手势同步性更优。
- **FVD ↓**：626.58，较S2G（816.03）降低189.45，视频整体时序质量明显改善。

**Figure 3** 的定性对比进一步揭示了先前方法的典型失败模式：S2G、MYA和EchoMimicV2生成的手部区域出现模糊、手指扭曲等明显伪影（红圈标注），而本文方法生成的手势清晰、细节丰富，且与真实视频的时空对齐更准确。

主观用户研究（**Table 7–9**）在四个主观指标上进一步验证了上述优势，t检验（**Table 8**）表明本文方法相对于所有基线的提升具有统计显著性。

![[assets/figures/papers/paper_list_l1909_Weakly_Supervised_Motion_Learning_for_Co_speech_Gesture_Video_Generation/figures/012_Table_7.jpg]]
*Table 7: Quantitative comparison with previous works on four subjective metrics. Bold text indicates the best performance*

![[assets/figures/papers/paper_list_l1909_Weakly_Supervised_Motion_Learning_for_Co_speech_Gesture_Video_Generation/figures/013_Table_8.jpg]]
*Table 8: Statistical Comparison of Methods*

### 消融实验

消融实验围绕三个核心设计展开，系统验证了各模块的因果贡献。

**各阶段贡献分析（Table 2）**。Stage 1运动编码器仅用视频训练，取得FGD 0.92和BAS 0.7601，代表最终模型的性能上限。Stage 2引入音频-运动对齐后，FGD升至1.47，FVD从901.25升至932.56，说明对齐过程引入了轻微性能损失，但换取了音频驱动能力。Stage 3特征精化阶段将FVD从932.56大幅降至660.73，同时小幅改善其他指标，证明视频扩散模型对细节增强至关重要。最终模型（Stage 3 + 手部细化）达到FGD 1.11、FVD 626.58，在所有指标上取得最佳平衡。

**可逆特征提取器的必要性（Table 3）**。移除Stage 2中的可逆特征提取器后，FGD从1.47急剧升至45.73，FVD从932.56恶化至2156.39，所有指标均严重下降。这一结果有力证明：RealNVP耦合层构建的音频-运动联合空间是高效对齐的关键，直接映射无法学习有效的跨模态对应。**Figure 4**的定性对比显示，无此模块时手势与音频完全失配，视觉质量严重退化。

**运动信息的必要性（Table 6）**。仅用音频训练（无运动编码器输入）时，FVD从660.73急剧升至2406.91，证明运动表征是高质量视频生成的必要输入，纯音频信号无法提供足够的时序和空间引导。

**损失函数组合分析（Table 4）**。Stage 2中联合使用MSE、Intra-对比和Inter-对比损失优于任意子集，验证了多粒度对齐（帧级、片段内、片段间）的互补性。

**手部细化效果（Table 5）**。基于策略梯度的初始噪声优化将平均手部置信度从88.73%提升至95.45%，**Figure 4**的定性结果也显示手部细节从模糊、残缺改善为清晰、完整。

### 失败模式与局限性

尽管整体性能优越，本文方法存在以下已知局限：

1. **运动表征继承限制**。方法继承了ReenactAnything隐式运动提取的局限性，对训练分布外的复杂运动（如大幅度身体移动、摄像机晃动）泛化能力未充分验证——训练数据仅包含正面视频。
2. **低帧率时序一致性**。模型运行于7 FPS，时间连续性可能受限，快速手势或唇部运动可能出现抖动。
3. **手部细化的独立贡献未分离**。消融仅对比Stage 3与最终模型，手部细化对FGD、FVD等全局指标的定量增益未单独报告。
4. **唇音同步未专门优化**。当前框架未显式建模唇部运动与音频的对应关系，零样本泛化至新说话者时唇同步质量可能下降。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|---------|
| **Table 1** | 四项客观指标全面超越S2G、MYA、EchoMimicV2，FGD降至1.11 |
| **Table 2** | Stage 1（FGD 0.92）为性能上限；Stage 3将FVD从932.56降至660.73；手部细化进一步提升 |
| **Table 3** | 移除可逆特征提取器导致FGD从1.47飙升至45.73，验证其必要性 |
| **Table 5** | 手部细化将手部置信度从88.73%提升至95.45% |
| **Table 6** | 无运动信息时FVD从660.73恶化至2406.91，验证运动表征的必要性 |
| **Figure 3** | 先前方法手部存在模糊、扭曲伪影，本文方法生成清晰高质量手势 |
| **Figure 4** | 各阶段定性对比：无特征提取器时手势失配，手部细化消除手指残缺 |

![[assets/figures/papers/paper_list_l1909_Weakly_Supervised_Motion_Learning_for_Co_speech_Gesture_Video_Generation/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison with previous works on four objective metrics*

![[assets/figures/papers/paper_list_l1909_Weakly_Supervised_Motion_Learning_for_Co_speech_Gesture_Video_Generation/figures/004_Figure_3.jpg]]
*Figure 3: The leftmost image in the GT column represents the first frame. Red circles highlight noticeable artifacts in prior methods. As shown, existing approaches suffer from issues such as blurry hands and distorted fingers. In contrast, our method produces high-quality videos. More importantly, our approach generates videos that are better aligned with the ground truth. Please zoom in for better visibility of details. Video results are shown in Supplementary Material*

![[assets/figures/papers/paper_list_l1909_Weakly_Supervised_Motion_Learning_for_Co_speech_Gesture_Video_Generation/figures/005_Table_2.jpg]]
*Table 2: Quantitative ablation study on different stages across four objective metrics. Ours: Stage 3 + hand refinement. *: Upper bound of our method*

![[assets/figures/papers/paper_list_l1909_Weakly_Supervised_Motion_Learning_for_Co_speech_Gesture_Video_Generation/figures/007_Table_3.jpg]]
*Table 3: Results of the model without the invertible feature extractor in Stage 2 across four objective metrics*

![[assets/figures/papers/paper_list_l1909_Weakly_Supervised_Motion_Learning_for_Co_speech_Gesture_Video_Generation/figures/010_Table_5.jpg]]
*Table 5: Results of the mean hand pose confidence score without or with hand refinement. Ours: Stage 3 + hand refinement*

![[assets/figures/papers/paper_list_l1909_Weakly_Supervised_Motion_Learning_for_Co_speech_Gesture_Video_Generation/figures/011_Table_6.jpg]]
*Table 6: Results of the model without motion information across four objective metrics*

### 补充图表

![[assets/figures/papers/paper_list_l1909_Weakly_Supervised_Motion_Learning_for_Co_speech_Gesture_Video_Generation/figures/009_Table_4.jpg]]
*Table 4: Comparisons of different loss functions in Stage 2 on four objective metrics*

## 方法谱系与知识库定位

### 任务定位与核心分歧

该工作属于**弱监督协同语音手势视频生成**，其核心分歧在于对训练监督信号的依赖：传统两阶段方法（先预测姿态关键点，再基于姿态驱动视频生成）需要大量精确的姿态标注（如2D/3D关键点或密集姿态），标注成本高昂且易引入累积误差，导致手部细节模糊、手指扭曲等伪影（Figure 1, Figure 3）。本文提出的**弱监督运动学习框架**将因果调节旋钮从“显式姿态监督”转向“隐式运动表征学习”，通过可逆特征提取器建立音频到运动空间的直接映射，实现纯音频-视频训练，从根本上绕开了姿态标注瓶颈。

### 与基线方法的关系

论文选取了三类代表性基线进行对比，均在同一PATS数据集上微调以确保公平性：

- **S2G**（He et al., 2024）：专门设计的协同语音手势视频生成方法，代表当前任务的主流方案。本文在四个客观指标上全面超越S2G：FGD从3.69降至1.11（↓69.9%），Diversity从180.59提升至282.89（↑56.6%），BAS从0.7280提升至0.7526，FVD从816.03降至626.58（↓23.2%）（Table 1）。定性对比中，S2G产生的手部模糊和手指扭曲问题在本文方法中得到显著改善（Figure 3）。

- **MYA**（Huang et al., 2024）：姿态图像引导的视频生成方法，适配到协同语音手势任务时需先生成姿态图像。本文在FGD（1.11 vs 2.94）和FVD（626.58 vs 1095.70）上优势明显，表明隐式运动表征比显式姿态图像更有效地保留了运动信息（Table 1）。

- **EchoMimicV2**（Meng et al., 2024）：零样本音频驱动视频生成方法，适配到此任务时同样依赖姿态图像。本文在Diversity（282.89 vs 196.18）和FVD（626.58 vs 854.08）上大幅领先，但BAS指标（0.7526 vs 0.7501）优势微弱，提示唇音同步可能不是本文的核心优化目标（Table 1）。

### 方法谱系中的技术继承与创新

**运动编码器**继承自**EVA-CLIP**（Sun et al., 2023）的视觉编码模型，通过添加线性层降维后，仅使用潜扩散模型损失（$\mathcal{L}_{\mathrm{LDM}}$）进行训练。这一设计将大规模预训练视觉模型的泛化能力注入运动表征学习，使Stage 1运动编码器达到FGD 0.92和BAS 0.7601，代表最终模型的性能上限（Table 2）。

**可逆特征提取器**基于**RealNVP**（Dinh et al., ICLR 2017）的耦合层架构，其正变换将运动表征映射到音频-运动联合空间，负变换支持从音频表征恢复运动表征。这一设计是方法的关键创新：移除可逆特征提取器导致FGD从1.47急剧升至45.73，FVD从932.56升至2156.39（Table 3），验证了其在音频-运动对齐中的不可替代性。

**视频扩散模型**基于**I2VGen-XL**的特征精化阶段，通过交叉注意力注入运动表征以增强细节。Stage 3特征精化使FVD从932.56降至660.73（↓29.1%），但对FGD和BAS的改善有限（Table 2），表明其主要贡献在于视觉质量而非运动精度。

**手部细化**采用基于策略梯度的初始噪声优化，将高斯参数$\mu$和$\sigma$作为可学习参数，通过负对数概率乘以奖励的损失函数（$\mathcal{L} = -\log p(\boldsymbol{z}_t) \cdot \boldsymbol{r}$）进行优化。该方法将平均手部置信度从88.73%提升至95.45%（Table 5），但手部细化对Stage 3的独立贡献未定量分离，其效果边界尚不清晰。

### 适用边界与局限

1. **训练数据分布限制**：训练数据仅包含正面视频，对大幅度摄像机晃动或身体运动的泛化能力未充分测试。论文明确指出方法继承了**ReenactAnything**隐式运动提取的局限性（Section 5）。

2. **时序一致性约束**：模型在7 FPS低帧率下运行，时间一致性可能受限。论文将视频增强技术集成列为重要开放问题。

3. **手部细化的独立贡献未量化**：消融实验仅对比Stage 3和最终模型（Stage 3 + 手部细化），无法分离手部细化对FGD、Diversity、BAS、FVD的独立贡献（Table 2 vs Table 5）。

4. **唇音同步非核心优化目标**：与EchoMimicV2的BAS差距仅0.0025（Table 1），提示当前方法在唇音对齐方面可能未做专门优化。

### 开放问题与未来方向

论文提出的开放问题包括：（1）如何集成视频增强技术以改善低帧率下的时序一致性；（2）基于策略梯度的初始噪声优化方法能否扩展到其他人体视频生成任务（如全身动作生成）；（3）如何在更大数据集和更大模型上训练，同时保持与基础扩散模型的竞争力；（4）能否提升唇音同步性能并实现零样本泛化至更多说话者；（5）如何将方法从正面视频扩展到多视角或自由运动场景。这些问题共同指向一个核心挑战：在保持弱监督优势的前提下，提升模型的泛化能力和时序一致性。

## 原文 PDF

![[paperPDFs/ICLR_2026/Weakly_Supervised_Motion_Learning_for_Co_speech_Gesture_Video_Generation.pdf]]