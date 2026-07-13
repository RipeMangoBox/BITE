---
title: GestureLSM Latent Shortcut based Co Speech Gesture Generation with Spatial Temporal Modeling
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/GestureLSM_Latent_Shortcut_based_Co_Speech_Gesture_Generation_with_Spatial_Temporal_Modeling.pdf
code_link: null
project_link: https://andypinxinliu.github.io/GestureLSM
aliases:
- GLSBCSGGSTM
tags:
- ICCV_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: GestureLSM
primary_logic: GestureLSM
claims:
- GestureLSM
---

# GestureLSM Latent Shortcut based Co Speech Gesture Generation with Spatial Temporal Modeling

> [!tip] 核心洞察
> GestureLSM

| 字段 | 内容 |
|------|------|
| 中文题名 | GestureLSM Latent Shortcut based Co Speech Gesture Generation with Spatial Temporal Modeling |
| 英文题名 | GestureLSM Latent Shortcut based Co Speech Gesture Generation with Spatial Temporal Modeling |
| 会议/期刊 | ICCV 2025 |
| Links |  [paper](https://arxiv.org/abs/2501.18898) · [Project](https://andypinxinliu.github.io/GestureLSM)|
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method |  |
| Dataset |  |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

语音驱动的共语手势生成旨在从语音信号中合成与说话内容节奏同步、语义一致的自然人体手势。现有方法在生成质量与推理速度之间面临两难权衡：扩散模型虽能产生高质量手势，但迭代采样过程导致推理延迟过高；单步回归方法速度快，却在手势多样性与真实感上存在明显不足。

GestureLSM 针对这一瓶颈，提出了一种基于**潜在捷径建模（Latent Shortcut Model）** 的快速共语手势生成框架。其核心思路是将手势生成问题从高维原始运动空间迁移到低维离散潜在空间，并引入流匹配（Flow Matching）直接建模潜在速度场，从而在极少采样步数内完成高质量生成。

具体而言，该方法包含三个关键设计：
1. **空间-时间解耦注意力**：将人体划分为多个身体区域并分别量化为离散 Token，通过先空间后时间的注意力机制显式建模区域间协同与运动时序，确保全身手势的连贯性。
2. **潜在捷径学习**：在量化潜在空间中，利用流匹配对线性插值路径的速度场进行回归，使模型学习从噪声到目标手势的“捷径”映射，大幅压缩推理步数。
3. **偏态时间采样**：采用 Beta 分布对时间步进行偏态采样，重点强化模型在生成末端（$t \to 1$）的预测能力，有效提升最终手势质量。

在 BEAT2 基准上，GestureLSM 取得了 **FGD 4.088×10⁻¹** 的最优结果，相较次优方法 EMAGE（5.256×10⁻¹）降低 1.168，同时在单张 NVIDIA A100 上实现了最快的推理速度。用户研究进一步表明，该方法在真实感、同步性与平滑度三个维度上均以显著优势领先现有方法。消融实验证实：交叉注意力融合优于拼接/相加、RVQ 优于 VQ 与乘积量化、空间-时间注意力顺序优于其他排列、分类器自由引导尺度为 2 时性能最佳。

综上，GestureLSM 通过“离散潜在空间 + 流匹配捷径 + 空间-时间解耦建模”的组合策略，在生成质量与推理效率之间取得了新的最优平衡点，为实时共语手势生成提供了可行范式。

语音驱动的手势生成（co-speech gesture generation）旨在从语音和文本脚本中合成与说话内容同步的全身人体手势，是虚拟人、数字代理等应用中的关键任务。现有方法主要面临两个核心瓶颈：**生成质量与推理速度之间的权衡**，以及**对身体各部位时空交互建模的不足**。

在生成范式方面，主流方法多基于扩散模型（diffusion models）或自回归（autoregressive）架构。扩散模型虽然生成质量较高，但通常需要大量采样步骤，导致推理速度缓慢，难以满足实时交互需求。自回归方法推理速度较快，但容易累积误差，且难以显式建模身体各部位之间的空间依赖关系。Figure 2 直观地展示了这一困境：GestureLSM 在 BEAT2 数据集上以 FGD 衡量生成质量的同时，实现了最快的推理速度（在单张 NVIDIA A100 上测量），而其他基线方法在质量-速度的 Pareto 前沿上均处于劣势。

在时空建模方面，人体手势涉及手部、上半身、腿部等多个身体部位，这些部位之间存在复杂的协同关系。现有方法通常将全身手势视为一个整体进行建模，缺乏对身体部位间空间交互的显式学习，导致生成的手势在局部细节和整体协调性上存在不足。

针对上述问题，本文提出 **GestureLSM**，其动机可概括为两个层面：

1. **高效采样**：引入流匹配（flow matching）替代传统扩散过程，通过显式建模潜在速度空间，大幅减少推理所需的采样步数，从而在保持生成质量的同时显著提升推理速度。

2. **细粒度时空建模**：将身体不同部位的运动通过残差向量量化（RVQ）离散化为 token，并利用空间注意力和时间注意力机制显式学习各身体部位 token 之间的交互关系，实现连贯的全身手势生成。

## 核心方法与创新机理

GestureLSM 的核心创新在于将**空间-时间解耦注意力**与**潜空间捷径学习**相结合，在保证生成质量的同时大幅提升推理速度。相对于现有基线方法（如 EMAGE），其关键改变槽位体现在以下三个层面。

### 1. 空间-时间解耦注意力机制

现有方法通常将全身关节展平为单一序列进行建模，忽略了不同身体部位之间的结构化交互。GestureLSM 将身体运动显式划分为手部、上半身和腿部等区域，并通过**先空间、后时间**的解耦注意力来捕获依赖关系：

- **空间注意力**（Spatial Attention）：在同一帧内，跨不同身体区域计算注意力，确保各部位动作的协调性。其形式为 $\mathcal{A}_s = \mathrm{SoftMax}(\frac{Q_s K_s}{\sqrt{d}} + \mathbf{P}) V_s$，其中 $Q_s, K_s, V_s \in \mathbb{R}^{n \times d}$（$n$ 为身体区域数，$d$ 为特征维度），$\mathbf{P}$ 为空间位置编码。
- **时间注意力**（Temporal Attention）：对每个身体区域独立地沿时间轴计算注意力，建模运动的时序演进。其形式为 $\mathcal{A}_t = \mathrm{SoftMax}(\frac{Q_t K_t}{\sqrt{d}} + \mathbf{P}) V_t$，其中 $Q_t, K_t, V_t \in \mathbb{R}^{T \times d}$（$T$ 为时间步数）。

消融实验（Table 2a）证实了这一设计的必要性：移除空间注意力后 FGD 从 4.088 升至 8.232，移除时间注意力后 FGD 飙升至 22.412，表明时间一致性对生成质量的影响更为关键。此外，直接将空间-时间注意力合并为单一注意力（即展平所有特征）反而无法有效学习部位交互（Table 2b），进一步验证了解耦设计的合理性。

### 2. 潜空间捷径模型与流匹配

GestureLSM 引入**潜空间捷径模型**（Latent Shortcut Model）来实现高效生成。其核心思路是：在量化后的离散潜空间上，通过流匹配（Flow Matching）显式建模潜变量的速度场，使模型能够以极少的采样步数完成生成。

具体而言，运动数据经 RVQ（Residual Vector Quantization）量化为离散 token 后，流匹配定义线性插值路径 $x_t = (1-t)x_0 + t x_1$ 及对应速度 $v_t = x_1 - x_0$，模型通过最小化 $\mathcal{L}^{\mathrm{F}}(\theta) = \mathbb{E}_{x_0,x_1\sim\mathcal{D}}[\|\bar{v}_\theta(x_t,t)-(x_1-x_0)\|^2]$ 来学习从噪声到数据的映射。此外，模型通过**自一致性约束**强制长时运动预测与短时运动之和保持一致，从而保证运动轨迹的连贯性。

在时间步采样策略上，论文发现 Beta 分布采样（左偏，强调 $t \to 1$ 的区域）能显著提升生成质量（Table 2c, Figure 5），这有效缓解了流匹配在 $t$ 接近 1 时预测失效的问题。

### 3. 多模态条件融合

GestureLSM 采用双路编码器分别处理语音的低层起始信息（振幅）和 BERT 提取的高层语义文本特征，融合后通过多层交叉注意力注入手势表征——手势特征作为 Query，语音特征作为 Key 和 Value。这种设计使条件信号能够细粒度地引导各身体区域的运动生成，是实现语音-手势同步性的关键。

**证据强度说明**：上述创新点均有消融实验和定量结果支撑（FGD 从次优基线 5.256 降至 4.088，Table 1），置信度较高。但论文未提供 venue/year 元数据，部分基线方法的具体版本需对照原文确认。

GestureLSM 的整体 pipeline 围绕“条件融合 → 空间-时间建模 → 量化潜变量学习 → 流匹配采样”四个核心阶段展开，如 **Figure 3** 所示。系统输入为语音信号与文本脚本，输出为与语音同步的全身高保真手势序列。

![[assets/figures/papers/paper_list_l1887_GestureLSM_Latent_Shortcut_based_Co_Speech_Gesture_Generation_with_Spati/figures/003_Figure_3.jpg]]
*Figure 3: The pipeline of GesutureLSM. (1) Our GestureLSM generate full-body gestures from speech and text scripts. The concatenated audio and text features are fused into gesture features via cross-attention. The condition fused gesture features are adopted to decode gesture latents with our proposed spatial-temporal decoder. The optimization objective is based on the flow matching (as shown in Figure 4 for details.) (2) The gesture latents are from pretrained RVQ (Residual Vector Quantization) models. (3) The details of spatial-temporal attention, which integrates with position encoding to learn the interaction of body regions*

### 条件编码与跨模态融合

语音信号从两个层级进行表征：低层级的 onset 信息通过振幅刻画，高层级语义则借助 **BERT** 从转录文本中提取。两类特征分别经专用音频编码器与文本编码器处理后进行拼接，形成统一的语音表征。该融合表征随后通过多层交叉注意力注入手势特征——手势特征作为 Query，语音特征同时担任 Key 与 Value，实现条件信息向手势空间的映射。

### 空间-时间手势生成器

条件融合后的手势特征进入手势生成器，该模块采用**空间注意力在前、时间注意力在后**的级联结构。空间注意力在单帧内捕捉不同身体区域（手部、上肢、下肢）的交互关系，确保各区域的协调一致；时间注意力则沿时间维度对每个身体区域独立建模，学习运动的时序演进。两者均引入位置编码以增强结构信息。

空间注意力与时间注意力的计算形式分别为：

$$
\mathcal{A}_s = \mathrm{SoftMax}\left(\frac{Q_s K_s}{\sqrt{d}} + \mathbf{P}\right) V_s
$$

$$
\mathcal{A}_t = \mathrm{SoftMax}\left(\frac{Q_t K_t}{\sqrt{d}} + \mathbf{P}\right) V_t
$$

其中 $Q_s, K_s, V_s \in \mathbb{R}^{n \times d}$ 对应 $n$ 个身体区域、$d$ 维特征的空间注意力输入，$Q_t, K_t, V_t \in \mathbb{R}^{T \times d}$ 对应 $T$ 个时间步的时间注意力输入，$\mathbf{P}$ 为各自的位置编码。

### 量化潜变量与流匹配

手势生成器的输出经编码器 $\mathcal{E}$ 映射为连续潜变量 $\mathbf{v}_t$，随后通过残差向量量化将局部身体运动转化为离散 token：

$$
\tilde{\mathbf{v}}_t = \mathcal{Q}(\mathbf{v}_t), \quad \mathcal{Q}(\mathbf{v}_t) = \mathbf{c}_i, \quad i = \arg\min_i \|\mathbf{c}_i - \mathbf{v}_t\|_2
$$

解码器 $\mathcal{D}$ 负责从量化后的潜变量 $\{\tilde{\mathbf{v}}_t\}$ 重建身体关节信息：

$$
\{\tilde{\mathbf{b}}_t\} = \mathcal{D}(\{\tilde{\mathbf{v}}_t\}) \equiv \mathcal{D}(\mathcal{Q}(\mathcal{E}(\{\mathbf{b}_t\})))
$$

在量化潜空间上，GestureLSM 引入**流匹配**实现高效采样。其核心思想是显式建模潜变量速度空间：给定噪声 $x_0$ 与数据 $x_1$，通过线性插值 $x_t = (1-t)x_0 + t x_1$ 定义轨迹，速度定义为 $v_t = x_1 - x_0$。模型通过回归经验速度进行训练：

$$
\mathcal{L}^{\mathrm{F}}(\theta) = \mathbb{E}_{x_0,x_1\sim\mathcal{D}}\left[\|\bar{v}_\theta(x_t,t) - (x_1 - x_0)\|^2\right]
$$

此外，GestureLSM 在运动轨迹上施加自一致性约束，确保长时间跨度的整体运动与各短时段的运动之和保持一致。

### 时间步采样策略

时间步采样分布对生成质量有显著影响。实验表明，采用 Beta 分布进行采样可获得最低的训练损失；同时，当 $t$ 接近 1 时施加左偏斜的强调，能够显著提升生成质量。

### 整体流程

GestureLSM 的生成流程如下：首先将语音信号与文本脚本分别编码并融合，得到条件特征；随后通过交叉注意力将条件信息注入手势特征；最后在量化后的隐空间中进行生成。整个过程可概括为三个核心阶段：**多模态条件编码**、**时空手势生成**、**隐式捷径建模**。

---

### 多模态条件编码

语音信号从两个层面进行表征（第 3.1 节）：

- **低层起始信息**：以振幅（amplitude）为特征，捕捉语音的节奏与重音线索。
- **高层语义信息**：使用 BERT 从转录文本中提取语义特征。

两类特征分别通过专用的音频编码器和文本编码器处理后拼接，得到融合的语音表征。该融合表征随后通过多层交叉注意力注入手势特征：手势特征作为 Query，语音特征同时作为 Key 和 Value。这一设计使手势生成能够同时感知语音的韵律节奏和语义内容。

---

### 时空手势生成器

手势生成器对量化后的身体区域 Token 分别施加空间注意力和时间注意力，以显式建模身体部位之间的交互关系（第 3.2 节）。

**空间注意力**在同一帧内跨身体区域计算，确保各部位动作的协调性：

$$
\mathcal{A}_s = \mathrm{SoftMax}\left(\frac{Q_s K_s}{\sqrt{d}} + \mathbf{P}\right) V_s
$$

其中 $Q_s, K_s, V_s \in \mathbb{R}^{n \times d}$，$n$ 为身体区域数，$d$ 为特征维度，$\mathbf{P}$ 为空间位置编码。

**时间注意力**对每个身体区域独立地沿时间维度计算，建模动作的时序演进：

$$
\mathcal{A}_t = \mathrm{SoftMax}\left(\frac{Q_t K_t}{\sqrt{d}} + \mathbf{P}\right) V_t
$$

其中 $Q_t, K_t, V_t \in \mathbb{R}^{T \times d}$，$T$ 为时间步数，$\mathbf{P}$ 为时间位置编码。

两个注意力模块按“先空间、后时间”的顺序施加：先在每帧内协调身体部位，再沿时间轴平滑动作序列。

---

### 隐式捷径模型

GestureLSM 在量化手势隐空间上构建生成过程，核心机制包括向量量化与流匹配。

**向量量化**：将编码后的身体运动向量 $\mathbf{v}_t$ 映射到码本中最近的条目，得到离散 Token（第 3.1 节）：

$$
\tilde{\mathbf{v}}_t = \mathcal{Q}(\mathbf{v}_t), \quad \mathcal{Q}(\mathbf{v}_t) = \mathbf{c}_i, \quad i = \arg\min_i \|\mathbf{c}_i - \mathbf{v}_t\|_2
$$

解码器从量化向量重建身体关节信息：

$$
\{\tilde{\mathbf{b}}_t\} = \mathcal{D}(\{\tilde{\mathbf{v}}_t\}) \equiv \mathcal{D}(\mathcal{Q}(\mathcal{E}(\{\mathbf{b}_t\})))
$$

**流匹配**：在隐空间中定义线性插值路径 $x_t = (1-t)x_0 + t x_1$，其中 $x_0$ 为噪声，$x_1$ 为目标数据，速度场为 $v_t = x_1 - x_0$。模型通过回归经验速度进行训练（第 3.3 节）：

$$
\mathcal{L}^{\mathrm{F}}(\theta) = \mathbb{E}_{x_0,x_1\sim\mathcal{D}}\left[\|\bar{v}_\theta(x_t,t)-(x_1-x_0)\|^2\right]
$$

流匹配的引入使模型能够显式建模隐空间的速度场，从而以更少的采样步数实现高效生成。

---

### 时间戳采样策略

训练时的时间戳 $t \in [0,1]$ 采样分布对生成质量有显著影响。实验发现，当 $t$ 接近 1 时模型预测效果较差（图 5 右）。为补偿这一不足，采用 Beta 分布进行左偏采样，使训练时更侧重 $t$ 接近 1 的区间。该策略在训练损失和最终生成质量上均优于均匀采样等其他方案（表 2c）。

![[assets/figures/papers/paper_list_l1887_GestureLSM_Latent_Shortcut_based_Co_Speech_Gesture_Generation_with_Spati/figures/005_Figure_5.jpg]]
*Figure 5: Time Sampling Comparison. For various time sampling schedules, beta schedule performs the best, i.e., lowest training loss, with skewed pattern (left) to counteract the ineffectiveness of model prediction when t approaches 1 (right)*

## 实验与关键发现

### 主实验结果

GestureLSM 在 BEAT2 基准上取得全面最优。Table 1 显示，其 FGD 为 4.088（×10⁻¹），较次优方法 EMAGE 的 5.256 降低 1.168，Beat Constancy（BC）达 0.714（×10⁻¹），在所有对比方法中最接近真实标注。同时，GestureLSM 在单张 NVIDIA A100 上的平均每句推理时间（AIST）亦为最短，在 Figure 2 的质量-速度散点图中处于左上角最优区域，实现了生成质量与推理效率的双重领先。

![[assets/figures/papers/paper_list_l1887_GestureLSM_Latent_Shortcut_based_Co_Speech_Gesture_Generation_with_Spati/figures/007_Table_1.jpg]]
*Table 1: The quantitative results on BEAT. Frechet Gesture Distance (FGD) multiplied by*

![[assets/figures/papers/paper_list_l1887_GestureLSM_Latent_Shortcut_based_Co_Speech_Gesture_Generation_with_Spati/figures/002_Figure_2.jpg]]
*Figure 2: Our GestureLSM achieves significant generation quality improvement over baseline methods with fastest inference speed. The inference time is computed on one NVIDIA A100 while the generation quality is from FGD on BEAT2*

主观评估进一步验证了客观指标的可靠性。Figure 6 的定性对比表明，GestureLSM 生成的肢体动作更自然，局部身体区域间的交互更协调。Figure 7 的用户调研显示，该方法在真实感（realness）、同步性（synchrony）和平滑度（smoothness）三个维度上的平均意见分（MOS）均显著高于其他方法，与语音的对齐程度优势尤为明显。

### 消融实验

**空间-时间注意力机制。** Tab. 2a 揭示了双维度注意力的关键作用：移除空间注意力后 FGD 升至 8.232，移除时间注意力后 FGD 飙升至 22.412，表明时间建模对运动连贯性的贡献更大。同时施加空间与时间注意力并辅以位置编码时取得最优。Tab. 2b 进一步说明，单纯的空间-时间注意力（即不区分维度地展平特征）并未改善交互学习，推测原因是展平操作增加了特征复杂性，削弱了结构化建模的优势。

**时间戳采样分布。** Tab. 2c 和 Figure 5 对比了多种时间采样策略。Beta 分布采样取得最低训练损失，且左偏态（强调 $t$ 接近 1 的区域）能显著提升生成质量。这一发现与流匹配模型在 $t \to 1$ 时预测难度增大的特性一致——左偏采样通过增加该区域的训练密度来补偿模型能力瓶颈。

**其他消融。** Tab. 3 补充了语音特征类型、无分类器引导（CFG）尺度、手势表示形式、注意力序列顺序以及采样分布偏度的影响，为模块选择提供了完整证据链。

### 关键图表结论

- **Table 1**：全指标 SOTA，FGD 4.088，BC 0.714，推理速度最快。
- **Figure 2**：质量-速度联合对比，GestureLSM 处于帕累托前沿。
- **Tab. 2a**：时间注意力不可替代（FGD 从 4.088 升至 22.412），空间注意力次之（升至 8.232）。
- **Figure 5 / Tab. 2c**：Beta 左偏采样是流匹配训练的关键调优手段。
- **Figure 6 / Figure 7**：定性与用户调研双重验证生成动作的自然度和语音同步性。

### 失败模式与局限性

当前证据未直接报告具体的失败案例或生成崩溃模式。从消融实验中可推断：若缺乏时间注意力，模型几乎丧失运动生成能力（FGD > 22），表明长程时序依赖是该方法的核心脆弱点。此外，Tab. 2b 提示，不当的特征展平设计会破坏空间-时间结构化建模的收益，设计时需谨慎处理维度组织。以上推断需结合论文原文中的定性错误分析进行人工验证。

![[assets/figures/papers/paper_list_l1887_GestureLSM_Latent_Shortcut_based_Co_Speech_Gesture_Generation_with_Spati/figures/010_Table_2.jpg]]
*Table 2: Ablations of our method. We exam the each module contribution, model architecture design, time stamp distribution , model type analysis, speed up comparison and number of sampling steps. Bold indicates the best performance*

![[assets/figures/papers/paper_list_l1887_GestureLSM_Latent_Shortcut_based_Co_Speech_Gesture_Generation_with_Spati/figures/013_Table_3.jpg]]
*Table 3: Additional ablations of our method. We exam the speech feature, classifier free guidance scale, gesture representation, sequence order for the attention and the skewness for the sampling distribution. Bold indicates the best performance*

## 定位与知识库关联

### 1. 与主流基线的关系

GestureLSM 在 BEAT2 基准上与现有方法进行了系统对比。Table 1 显示，其 FGD 达到 **4.088**（×10⁻¹），显著优于次优方法 **EMAGE** 的 5.256，降幅约 22%。在节拍一致性（BC）上，GestureLSM 以 **0.714**（×10⁻¹）取得与真实数据最接近的结果。Figure 2 进一步表明，该方法在生成质量（FGD）与推理速度两个维度上同时占据优势，推理时间在单张 NVIDIA A100 上测量。

从方法谱系看，GestureLSM 处于**离散潜变量生成**与**流匹配**两条技术路线的交汇点。其核心设计——将全身肢体区域经 RVQ 量化为离散 token，再通过空间-时间注意力建模区域交互——与以下工作形成对比：

- **基于 VQ-VAE 的姿势生成方法**：GestureLSM 继承了将连续运动映射到离散码本的思想，但将其从单一身体表示扩展到多区域（手部、上半身、腿部）的独立量化，从而在 token 层面显式编码身体部位的拓扑结构。
- **基于扩散/流匹配的生成方法**：GestureLSM 采用流匹配（flow matching）而非 DDPM 类扩散，通过显式建模潜变量速度场 $v_t = x_1 - x_0$ 实现更高效的采样。这与近期流向生成的工作共享理论基础，但其创新在于将流匹配作用于**量化后的离散潜变量空间**，而非连续姿态空间。
- **基于注意力的序列建模方法**：GestureLSM 的空间注意力 $\mathcal{A}_s$ 在单帧内跨身体区域计算，时间注意力 $\mathcal{A}_t$ 沿时间轴独立作用于每个区域，这种解耦设计避免了将时空特征扁平化为一维序列时丢失结构信息的问题。

### 2. 适用边界

当前验证的适用边界主要受以下因素约束：

- **数据集**：所有定量结果均基于 BEAT2 数据集获得，未见在其他数据集（如 Trinity、TED Gesture）上的迁移验证。BEAT2 以英语演讲场景为主，对多语言、多风格场景的泛化性需手动核实。
- **模态输入**：方法依赖语音振幅（低层起始信息）和 BERT 文本特征（高层语义）的双通道输入。在仅有语音而无文本转写的场景下，性能是否可维持尚未验证。
- **全身手势**：方法设计针对全身手势生成（包含腿部），消融实验（Tab. 2a）表明移除空间注意力后 FGD 恶化至 8.232，移除时间注意力后恶化至 22.412，说明该方法对时空建模组件高度依赖。对于仅需上半身或仅需手部手势的场景，简化版本是否可行有待验证。
- **推理步数**：Tab. 2f 显示该方法支持减少采样步数以加速推理，但步数与质量的权衡曲线仅在 BEAT2 上验证，在不同场景下的最优步数配置需手动调整。

### 3. 局限与开放问题

**已识别的局限**：

1. **空间-时间注意力的联合使用问题**：Tab. 2b 表明，单纯将时空注意力合并（不区分空间/时间维度）并不能改善交互学习效果，作者将其归因于特征扁平化带来的复杂性。这意味着该方法的增益高度依赖于空间和时间注意力的解耦设计，对架构变体敏感。
2. **时间采样的敏感性**：Figure 5 和 Tab. 2c 显示，Beta 分布的时间采样策略（左偏，强调 $t \to 1$ 区域）对生成质量有显著影响。这暗示模型在靠近数据端的预测有效性存在固有不足，需要通过偏斜采样来补偿，可能在某些极端运动模式下表现不稳定。
3. **量化误差的传播**：RVQ 量化步骤 $\tilde{\mathbf{v}}_t = \mathcal{Q}(\mathbf{v}_t)$ 引入的离散化误差如何影响后续流匹配的潜变量捷径学习，论文未做深入分析。

**开放问题**：

- 潜变量捷径模型（Latent Shortcut Model, Figure 4）中自一致性约束的理论性质未在分析中展开——该约束是否等价于某种正则化，或是否可与其他一致性模型建立形式化联系，需手动核实。
- 该方法在 BEAT2 上的优势是否可迁移到其他生成质量指标（如 HumanML3D 的 FID、动作多样性指标）未见报告。
- 空间注意力中位置编码 $\mathbf{P}$ 的具体形式及其对全身区域交互的贡献未做消融，该设计是否为性能关键因素需进一步确认。

## 原文 PDF

![[paperPDFs/ICCV_2025/GestureLSM_Latent_Shortcut_based_Co_Speech_Gesture_Generation_with_Spatial_Temporal_Modeling.pdf]]
