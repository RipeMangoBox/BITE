---
title: "SDTrack: A Baseline for Event-based Tracking via Spiking Neural Networks"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SDTrack_A_Baseline_for_Event_based_Tracking_via_Spiking_Neural_Networks.pdf
project_link: null
code_link: "https://github.com/YmShan/SDTrack"
aliases:
- SDTrack
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过全局轨迹提示（GTP）保留多方向运动信息并累积全局轨迹，结合内在位置学习（IPL）免除额外位置编码，并设计全脉冲驱动的Transformer骨干，实现高效能和高精度的跟踪。
primary_logic: 将事件流编码为包含累积极性和历史轨迹的三通道帧，联合IPL隐式学习位置信息，使全SNN Transformer架构在极低功耗下实现与ANN方法相当甚至更优的跟踪精度。
claims:
- GTP通过累积正负极性并记录轨迹信息，提供了增强的时空表示。
- IPL让网络无需显式位置编码即可有效学习位置信息。
- SDTrack是全脉冲驱动的Transformer跟踪器，在多个基准上达到最优，且功耗极低。
- "FE108 上 AUC / PR = 59.0% (AUC) / 91.3% (PR) [SDTrack-Tiny]"
---

# SDTrack: A Baseline for Event-based Tracking via Spiking Neural Networks

> [!tip] 核心洞察
> 将事件流编码为包含累积极性和历史轨迹的三通道帧，联合IPL隐式学习位置信息，使全SNN Transformer架构在极低功耗下实现与ANN方法相当甚至更优的跟踪精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | SDTrack：基于脉冲神经网络的事件跟踪基线 |
| 英文题名 | SDTrack: A Baseline for Event-based Tracking via Spiking Neural Networks |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2503.08703) · [Code](https://github.com/YmShan/SDTrack) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | SDTrack Pipeline |
| Dataset | FE108 |

> [!tip] 效果简介
> - FE108 上，AUC / PR 59.0% (AUC) / 91.3% (PR) [SDTrack-Tiny] vs 57.4% (AUC) / 89.3% (PR) [Spike-driven Transformer V3] (+1.6% (AUC) / +2.0% (PR))。

## 概要

基于事件相机的目标跟踪因其高时间分辨率和高动态范围优势，在快速运动和极端光照场景下展现出巨大潜力。然而，现有方法大多采用**ANN-SNN混合架构**，未能充分发挥脉冲神经网络（SNN）的能效优势；同时，这些方法普遍缺乏搜索区域与模板之间的交叉相关建模，且事件聚合方式无法充分捕获全局轨迹信息，导致时空表征能力不足。

针对上述瓶颈，本文提出**SDTrack**——首个全脉冲驱动的Transformer跟踪流水线。其核心设计包含三个关键创新：

1. **全局轨迹提示（GTP）**：将异步事件流聚合为三通道事件帧，分别累积正极性、负极性和全局轨迹信息，从而保留多方向运动线索并增强时空表示能力。
2. **内在位置学习（IPL）**：通过将模板帧与搜索帧对角拼接、其余区域零填充，使网络无需显式位置编码即可隐式学习位置信息。
3. **全SNN Transformer骨干**：采用脉冲自注意力（SSA）实现模板-搜索交叉相关，构建完全由脉冲驱动的特征提取与交互架构。

在FE108、FELT和VisEvent三个事件跟踪基准上，SDTrack以仅**19.61M参数**和**8.16mJ**的理论推理能耗，取得了与领先ANN方法相当甚至更优的跟踪精度。具体而言，SDTrack-Tiny在FE108上达到**59.0% AUC**和**91.3% PR**，较全脉冲基线Spike-driven Transformer V3分别提升1.6%和2.0%（Table 3）。该方法在弱曝光、过曝光及相似物干扰等挑战性场景下亦展现出更强的鲁棒性。

> **方法定位**：SDTrack属于全脉冲事件跟踪范式，区别于OSTrack（Ye et al., ECCV 2022）等ANN Transformer方法和STNet（Zhang et al., CVPR 2022）等混合架构方法。其GTP事件聚合和IPL位置学习策略为SNN跟踪提供了新的设计思路。

> **局限提示**：目前仅在三个事件数据集上验证，且理论能耗计算尚未在真实神经形态芯片上确认；GTP的超参数（α=30, β=0.8）依赖手动调节，自适应机制有待探索。



**事件相机**通过异步记录对数亮度变化，输出高时间分辨率、低延迟、高动态范围的稀疏事件流，使其在高速运动与极端光照条件下具有天然优势。然而，传统基于人工神经网络（ANN）的跟踪器（如 **OSTrack**（Ye et al., ECCV 2022）、**STARK**（Yan et al., ICCV 2021）、**MixFormer**（Cui et al., CVPR 2022））依赖密集的帧级计算，难以继承事件数据在能效与速度上的潜力。

**脉冲神经网络（SNN）** 以稀疏脉冲为信息载体，与事件数据的稀疏性高度契合，理论上可实现极低功耗的神经形态计算。但现有基于SNN的事件跟踪方法面临两个核心瓶颈：

1. **架构混合化**：多数工作（如 **STNet**（Zhang et al., CVPR 2022）、**SNNTrack**（Zhang et al., TIP 2025））采用ANN-SNN混合架构，脉冲仅在部分层中使用，未能充分发挥SNN的全脉冲计算能效优势。
2. **时空表征不足**：现有事件聚合方式（如Event Frame仅记录最新极性、Time-Surface仅编码局部时间衰减）无法充分捕获全局轨迹信息；同时，模板与搜索区域之间缺乏交叉相关建模，限制了时空特征的表达能力。

针对上述缺口，本文提出 **SDTrack**——首个全脉冲驱动的Transformer跟踪流水线。其核心动机在于：通过设计全局轨迹提示（Global Trajectory Prompt, GTP）增强事件帧的时空表征，联合内在位置学习（Intrinsic Position Learning, IPL）免除显式位置编码，并构建全SNN Transformer骨干，在保持极低功耗的前提下实现与ANN方法相当甚至更优的跟踪精度。



## 核心方法与创新机理

SDTrack 的核心创新在于：**首次构建了完全由脉冲驱动的 Transformer 跟踪流水线**，并通过三个紧密协同的“变更槽”（changed slots）——事件聚合方式、位置编码和骨干架构——系统性地解决了现有事件跟踪方法在能效与时空表征上的瓶颈。

### 从混合架构到全脉冲驱动：架构级变更

现有基于事件的跟踪方法（如 **STNet**，Zhang et al., CVPR 2022；**SNNTrack**，Zhang et al., TIP 2025）多采用 ANN-SNN 混合架构，即前端用 SNN 处理事件、后端用 ANN 进行特征交互与预测。这种设计虽利用了 SNN 的低功耗特性，却未能充分发挥其能效优势——ANN 组件中的浮点乘累加操作（MAC）仍是能耗的主要来源。

SDTrack 将整个骨干网络替换为**全 SNN Transformer**，包括 SNN Conv Module 和 SNN Transformer Module。这一变更的因果机制在于：所有特征提取与交互均在脉冲域完成，推理时仅需稀疏的累加操作（AC），理论能耗大幅降低。论文报告 SDTrack-Tiny 仅需 **8.16 mJ** 即可完成一次推理，参数量为 19.61M（Table 1）。与 Spike-driven Transformer V3（Yao et al., NeurIPS 2024/arXiv 2024）相比，SDTrack-Tiny 在 FE108 上 AUC 提升 +1.6%、PR 提升 +2.0%（Table 3），证明全脉冲驱动不仅可行，且精度更具竞争力。

### 事件聚合：从瞬时极性到全局轨迹提示（GTP）

传统事件聚合方法（如 Event Frame 仅记录最新极性，或 Time-Surface）存在两个根本缺陷：一是丢弃了时间区间内累积的运动信息；二是无法捕获目标的全局轨迹，导致在快速往返运动等场景下时空表征退化（Figure 3 展示了这一失效模式）。

GTP（Global Trajectory Prompt）将事件流编码为**三通道帧**：
- **通道 1**（正极性累积）：$h_i^1(x,y) = \alpha \cdot \sum_{t_k \in L} \delta(x - x_k, y - y_k) \delta(p_k - 1)$
- **通道 2**（负极性累积）：$h_i^2(x,y) = \alpha \cdot \sum_{t_k \in L} \delta(x - x_k, y - y_k) \delta(p_k + 1)$
- **通道 3**（全局轨迹）：$h_i^3(x,y) = h_{i-1}^3(x,y) \cdot \beta + \alpha \cdot \sum_{j=1}^{2} C(h_{i-1}^j(x,y), h_i^j(x,y))$，其中 $C(\cdot)$ 为新增事件指示函数，$\beta$ 控制历史轨迹的衰减速率。

这一设计的因果逻辑在于：通道 1 和 2 保留了时间区间内**所有**运动信息（而非仅最新状态），通道 3 通过递归累积新增事件位置，显式编码了目标的运动轨迹。三者联合为后续 Transformer 提供了丰富的时空先验。消融实验（Figure 4）表明，GTP 在 FE108 上显著优于 Event Frame、Time-Surface 等聚合方法，且最优超参数为 $\alpha=30$、$\beta=0.8$（Figure 6）。

### 位置编码：从显式编码到内在位置学习（IPL）

Transformer 架构通常依赖显式位置编码（可学习编码或正弦编码）来注入空间信息。SDTrack 提出的 IPL（Intrinsic Position Learning）**完全移除了显式位置编码**，通过将模板帧 $\mathbf{Z}$ 和搜索帧 $\mathbf{X}$ 对角拼接：

$$\mathrm{IPL}(\mathbf{X}, \mathbf{Z}) = \begin{bmatrix} \mathbf{X} & \mathbf{O}_1 \\ \mathbf{O}_2 & \mathbf{Z} \end{bmatrix}$$

零填充区域（$\mathbf{O}_1, \mathbf{O}_2$）在拼接矩阵中形成了自然的空间隔离，后续 SNN Conv Block 的卷积操作隐式地学习到模板与搜索区域的相对位置关系。消融实验（Table 2, Experiment 2）显示，移除 IPL 导致 PR 从 91.30% 降至 89.66%（-2.04%），证明了这一设计的有效性。Figure 7 的注意力图可视化进一步揭示：IPL 使网络在模板区域产生更集中的梯度响应，而传统位置编码的注意力分布相对弥散。

### 特征交互：从独立提取到脉冲自注意力交叉相关

ANN 跟踪器（如 **OSTrack**, Ye et al., ECCV 2022；**MixFormer**, Cui et al., CVPR 2022）已广泛使用交叉注意力实现模板-搜索特征交互，但现有 SNN 跟踪方法多采用双分支独立提取后简单融合的策略，缺乏显式的交叉相关建模。

SDTrack 在 SNN Transformer Module 中引入**脉冲自注意力（SSA）**：

$$\mathrm{SSA}(\mathbf{Q}_s, \mathbf{K}_s, \mathbf{V}_s) = \mathbf{Q}_s \mathbf{K}_s^{\top} \mathbf{V}_s * \mathbf{s}$$

其中 $\mathbf{Q}_s, \mathbf{K}_s, \mathbf{V}_s$ 均为脉冲张量，$\mathbf{s}$ 为缩放因子。SSA 使模板和搜索特征在脉冲域直接进行相关性计算，填补了 SNN 跟踪中特征交互的空白。这一设计是 SDTrack 在精度上逼近甚至超越 ANN 方法的关键机制之一。

### 跟踪头：从角点头到脉冲中心头

SDTrack 采用**脉冲版中心预测头（Center Head）**替代传统的角点头（Corner Head，如 **STARK** 所用，Yan et al., ICCV 2021）。消融实验（Table 2, Experiment 8）表明，Center Head 在 FE108 上 AUC 达 58.81%，优于 Corner Head 的 57.70%。同时，Table 4 显示卷积决策层的引入仅增加 0.0004 mJ 的功耗，几乎不损害能效优势。

### 创新协同与边界

上述创新并非孤立存在：GTP 提供的三通道时空表征使 IPL 的对角拼接能捕获更丰富的位置线索；全 SNN 骨干的低发放率特性使 SSA 的计算开销可控；Center Head 的轻量设计则保证了端到端的低功耗推理。然而，GTP 的超参数（$\alpha, \beta$）目前需手动调节，不同场景下的自适应机制仍有待探索；此外，SDTrack 未利用 RGB 信息，在纹理极弱的纯事件场景下可能仍面临挑战。



SDTrack 构建了一条**全脉冲驱动**的单目标跟踪流水线，其核心设计目标是在极低功耗下实现与先进 ANN 方法相当甚至更优的跟踪精度。流水线由四个关键模块级联构成：**全局轨迹提示（Global Trajectory Prompt, GTP）**、**内在位置学习（Intrinsic Position Learning, IPL）**、**SNN 卷积模块**和**SNN Transformer 模块**，最后通过**脉冲中心预测头**输出跟踪结果。

### 数据流与模块关系

整体数据流如图 2 所示。给定模板事件流和搜索事件流，系统首先通过 GTP 将异步稀疏的事件流聚合为三通道的事件帧，分别编码正极性累积、负极性累积和全局轨迹信息。随后，IPL 将模板帧和搜索帧进行对角拼接，形成统一的输入矩阵，无需引入额外的显式位置编码参数。该拼接矩阵依次经过 SNN 卷积模块进行初步脉冲特征提取，再通过 SNN Transformer 模块实现模板与搜索特征之间的交叉相关建模。最后，SNN 跟踪头预测目标的中心位置和尺度，输出边界框。

![图2: SDTrack流水线整体架构]()

### 模块功能概要

**GTP（全局轨迹提示）** 是事件聚合的关键创新。与仅记录最新极性的事件帧（Event Frame）或时间表面（Time-Surface）不同，GTP 通过三个通道分别累积正极性事件数、负极性事件数，并以前一帧轨迹衰减后叠加当前帧新增事件指示的方式记录全局轨迹信息。这使得聚合帧不仅保留了短时多向运动信息，还捕获了长时间窗口内的运动历史，为后续跟踪提供了更丰富的时空线索。

**IPL（内在位置学习）** 将模板帧 $\mathbf{Z}$ 和搜索帧 $\mathbf{X}$ 对角拼接为 $\begin{bmatrix} \mathbf{X} & \mathbf{O}_1 \\ \mathbf{O}_2 & \mathbf{Z} \end{bmatrix}$，其余区域用零矩阵填充。这种设计使网络能通过后续卷积层的感受野隐式地学习空间位置关系，消融实验表明移除 IPL 会导致 PR 下降 2.04%（91.30% → 89.66%）。

**SNN 卷积模块**由多个 SNN Conv Block 堆叠而成，每个 Block 采用可分离卷积与残差连接，对拼接图像进行脉冲特征提取。**SNN Transformer 模块**则通过脉冲自注意力（SSA）实现模板与搜索特征的交叉相关建模，弥补了现有脉冲跟踪方法中缺乏模板-搜索交互的不足。

**脉冲中心预测头**直接输出目标中心位置和尺度，相比角点头（Corner Head）在 FE108 上 AUC 提升约 1.1%（58.81 vs 57.70），且决策层的额外功耗极低（仅 +0.0004 mJ）。

### 训练与推理特性

SDTrack 的完整流水线在训练和推理中**不使用数据增强**（如颜色抖动、随机裁剪）和**后处理**（如哈宁窗惩罚），以端到端方式运行。骨干网络先在 ImageNet-1K 上预训练，再在事件跟踪数据集上通过配对匹配任务微调。当时间步数 $T>1$ 时，事件流被均匀划分为 $T$ 份以执行 GTP 聚合。理论能耗计算综合考虑了 MAC 操作和 AC 操作的 FLOPs 以及脉冲发放率，SDTrack-Tiny 版本在 VisEvent 数据集上的推理能耗仅为 8.16 mJ。

### 补充图表

![[assets/figures/papers/paper_list_l2138_https_arxiv_org_abs_2503_08703/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the SDTrack Pipeline. Upon receiving template and search event streams, GTP aggregates them into event frames, which are then concatenated into a unified matrix by IPL. Following SNN Conv Block processing, the matrix undergoes restoration and tokenization. The template features, after cross-correlation with search features, are fed into the SNN Tracking Head for target position and scale prediction. The detailed design of each module is illustrated in the middle and bottom panels*



### 3.1 脉冲神经元基础模型

SDTrack 采用统一的脉冲神经元动力学模型，所有 SNN 模块均基于 leaky integrate-and-fire (LIF) 神经元构建。膜电位更新遵循：

$$
\mathbf{U}[t] = \mathbf{H}[t-1] + \frac{1}{\tau}(\mathbf{X}[t] - (\mathbf{H}[t-1] - \mathbf{U}_{rest}))
$$

其中，$\mathbf{U}[t]$ 为时刻 $t$ 的膜电位，$\mathbf{H}[t-1]$ 为上一时刻发放脉冲后的复位电位，$\mathbf{X}[t]$ 为当前输入，$\tau$ 为膜时间常数，$\mathbf{U}_{rest}$ 为静息电位。当膜电位超过阈值 $\mathbf{U}_{thr}$ 时，神经元发放脉冲：

$$
\mathbf{S}[t] = f(\mathbf{U}[t] - \mathbf{U}_{thr})
$$

其中 $f(\cdot)$ 为阶跃函数（前向为二值化，反向通过代理梯度传播）。发放脉冲后执行硬复位：

$$
\mathbf{H}[t] = \mathbf{U}[t] (1 - \mathbf{S}[t])
$$

这一简洁的 LIF 模型构成了后续所有 SNN Conv Block 和 SNN Transformer 模块的计算基础。

### 3.2 Global Trajectory Prompt (GTP)

GTP 是 SDTrack 的核心事件聚合方法，将异步事件流编码为三通道事件帧，以保留多向运动信息和全局轨迹线索。

**第一通道（正极性累积）**：对时间区间 $L$ 内所有正极性事件 $(p_k = +1)$ 进行累积：

$$
h_i^1(x,y) = \alpha \cdot \sum_{t_k \in L} \delta(x - x_k, y - y_k) \delta(p_k - 1)
$$

**第二通道（负极性累积）**：对称地累积负极性事件 $(p_k = -1)$：

$$
h_i^2(x,y) = \alpha \cdot \sum_{t_k \in L} \delta(x - x_k, y - y_k) \delta(p_k + 1)
$$

其中 $\alpha$ 为缩放系数，控制事件计数的幅度范围。

**第三通道（全局轨迹累积）**：该通道通过递归方式记录目标的运动轨迹信息：

$$
h_i^3(x,y) = h_{i-1}^3(x,y) \cdot \beta + \alpha \cdot \sum_{j=1}^{2} C(h_{i-1}^j(x,y), h_i^j(x,y))
$$

其中 $\beta \in (0,1)$ 为衰减因子，使历史轨迹逐渐消退；$C(\cdot, \cdot)$ 为新增事件指示函数：

$$
C(h_{i-1}^j, h_i^j) = \mathbb{I}(h_{i-1}^j = 0 \ \mathrm{and} \ h_i^j \neq 0)
$$

该函数在上一帧对应通道为 0 且当前帧非 0 时返回 1，表示该像素位置出现了新事件。通过跨帧累积，第三通道隐式编码了目标的运动轨迹，为跟踪器提供额外的时空定位线索。超参数经实验确定为 $\alpha = 30$、$\beta = 0.8$（见 Figure 6）。

### 3.3 Intrinsic Position Learning (IPL)

传统 Transformer 跟踪器依赖显式位置编码注入空间信息，但 SNN 中脉冲信号的二值特性使得加性位置编码效果受限。IPL 通过结构化的输入拼接方式，使网络隐式学习位置信息，无需引入额外参数。

具体操作：将搜索帧 $\mathbf{X}$ 与模板帧 $\mathbf{Z}$ 进行对角拼接：

$$
\mathrm{IPL}(\mathbf{X}, \mathbf{Z}) = \begin{bmatrix} \mathbf{X} & \mathbf{O}_1 \\ \mathbf{O}_2 & \mathbf{Z} \end{bmatrix}
$$

其中 $\mathbf{O}_1$、$\mathbf{O}_2$ 为零矩阵，分别填充搜索帧右侧和模板帧左侧。拼接后的统一矩阵被送入 SNN Conv Module。由于模板和搜索区域在空间上被固定在对角位置，后续卷积操作可通过感受野自然地感知二者的相对位置关系，实现隐式位置编码。消融实验表明，移除 IPL 使 PR 下降 2.04%（91.30% → 89.66%，Table 2），验证了该设计的有效性。

### 3.4 SNN Conv Module

SNN Conv Block 对 IPL 输出的拼接矩阵进行脉冲特征提取，采用残差结构：

$$
\mathbf{U}' = \mathbf{U} + \mathrm{SNNSepConv}(\mathbf{U})
$$

其中 $\mathrm{SNNSepConv}$ 为脉冲驱动的可分离卷积，包含深度卷积和逐点卷积，每层卷积后跟随 LIF 神经元。多个 SNN Conv Block 堆叠构成完整的 SNN Conv Module，逐步提取层次化脉冲特征。经过 Conv Module 处理后，拼接矩阵被恢复为独立的搜索特征和模板特征，并通过 tokenization 送入后续的 SNN Transformer Module。

### 3.5 SNN Transformer Module

该模块通过脉冲自注意力（Spike Self-Attention, SSA）实现模板特征与搜索特征的交叉相关建模，这是 SDTrack 区别于以往 ANN-SNN 混合跟踪器的关键设计。SSA 的计算流程为：

$$
\mathrm{SSA}(\mathbf{Q_s}, \mathbf{K_s}, \mathbf{V_s}) = \mathbf{Q_s} \mathbf{K_s}^{\top} \mathbf{V_s} * \mathbf{s}
$$

其中 $\mathbf{Q_s}$、$\mathbf{K_s}$、$\mathbf{V_s}$ 分别为脉冲形式的查询、键、值矩阵，$\mathbf{s}$ 为缩放因子。由于脉冲信号为 0/1 二值，矩阵乘法可退化为累加操作，大幅降低计算能耗。SSA 后接脉冲 MLP 进一步进行特征变换，整个 Transformer Module 完全由脉冲驱动，不涉及浮点乘加。

### 3.6 训练损失函数

SDTrack 采用组合损失进行端到端训练：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{cls}} + \lambda_{\mathrm{iou}} \mathcal{L}_{\mathrm{iou}} + \lambda_{\mathcal{L}1} \mathcal{L}_1
$$

其中 $\mathcal{L}_{\mathrm{cls}}$ 为分类损失（用于区分前景/背景），$\mathcal{L}_{\mathrm{iou}}$ 为 IoU 回归损失，$\mathcal{L}_1$ 为 L1 回归损失。权重设定为 $\lambda_{\mathrm{iou}} = 2$，$\lambda_{\mathcal{L}1} = 5$。训练过程中不使用数据增强（如颜色抖动、随机裁剪）和后处理（如哈宁窗惩罚），保证了与 ANN 方法的公平对比。

### 补充图表

![[assets/figures/papers/paper_list_l2138_https_arxiv_org_abs_2503_08703/figures/003_Figure_3.jpg]]
*Figure 3: Example of event stream and event aggregation. The upper shows an event stream of a suspended object moving rightward then leftward from center in a short time. The lower displays results using various event aggregation methods for this stream*

![[assets/figures/papers/paper_list_l2138_https_arxiv_org_abs_2503_08703/figures/012_Figure_7.jpg]]
*Figure 7: Revealing why IPL outperforms traditional positional encoding. SDTrack-Tiny without IPL serves as baseline. Left: template and search inputs. Right: Attention Map from the last attention module and Template Gradient Response Map (TGRM)*



## 实验与关键发现

### 主要结果

SDTrack 在三个事件跟踪基准（FE108、FELT、VisEvent）上进行了系统评估，与当前主流的 ANN 和 SNN 跟踪器进行了全面对比（Table 1）。SDTrack-Base 在 FE108 上取得 59.9% AUC 和 91.5% PR，在 FELT 上取得 40.0% AUC 和 51.4% PR，在 VisEvent 上同样达到领先水平。值得注意的是，SDTrack-Tiny 仅以 19.61M 参数量和 8.16mJ 的理论推理能耗，在 FE108 上达到 59.0% AUC 和 91.3% PR，相比全脉冲驱动的 **Spike-driven Transformer V3**（Yao et al., NeurIPS 2024）提升了 1.6% AUC 和 2.0% PR。

![[assets/figures/papers/paper_list_l2138_https_arxiv_org_abs_2503_08703/figures/004_Table_1.jpg]]
*Table 1: Comparison with standard SOT pipelines on three event-based tracking benchmarks. * denotes results directly adopted from their respective benchmark reports. Energy consumption is measured on the VisEvent dataset. The best two results are shown in red and blue*

在 VisEvent 数据集上，SDTrack 与其他流程的 AUC、参数量和能耗的综合对比（Figure 1）显示，SDTrack 在精度-效率权衡上具有明显优势。AUC 和 PR 曲线（Figure 5）进一步验证了 SDTrack 在不同阈值下的鲁棒表现。

![[assets/figures/papers/paper_list_l2138_https_arxiv_org_abs_2503_08703/figures/006_Figure_5.jpg]]
*Figure 5: AUC (left) and PR (right) plot on the VisEvent dataset. Best viewed with zooming in*

![[assets/figures/papers/paper_list_l2138_https_arxiv_org_abs_2503_08703/figures/001_Figure_1.jpg]]
*Figure 1: SDTrack versus other pipelines on VisEvent dataset: AUC, inference parameter count, and energy consumption*

### 消融实验

Table 2 系统消融了 SDTrack 各核心组件的贡献：

![[assets/figures/papers/paper_list_l2138_https_arxiv_org_abs_2503_08703/figures/008_Table_2.jpg]]
*Table 2: Ablation studies*

- **IPL 的有效性**：移除 IPL 导致 PR 从 91.30% 下降至 89.66%（-2.04%），验证了内在位置学习对空间信息捕获的关键作用。Figure 7 的注意力图可视化揭示，IPL 相比传统显式位置编码能产生更聚焦的模板-搜索相关响应，梯度响应图也更为清晰。

- **GTP 超参数选择**：GTP 包含两个关键超参数——极性累积缩放系数 α 和轨迹衰减因子 β。通过实验评估（Figure 6），α=30、β=0.8 被确定为最优配置。在 β 的选择过程中，α 保持为 30。

![[assets/figures/papers/paper_list_l2138_https_arxiv_org_abs_2503_08703/figures/007_Figure_6.jpg]]
*Figure 6: Selection of GTP hyperparameters. During the selection process of β, α is consistently set to 30*

- **事件聚合方法对比**：Figure 4 展示了不同事件聚合方法在 FE108 上的性能对比，GTP 通过同时保留多向运动信息和全局轨迹线索，显著优于仅记录最新极性的 Event Frame 或 Time-Surface 等传统方法。

![[assets/figures/papers/paper_list_l2138_https_arxiv_org_abs_2503_08703/figures/005_Figure_4.jpg]]
*Figure 4: Performance comparison of various event aggregation methods on the FE108 dataset*

- **跟踪头设计**：Center Head 相比 Corner Head 表现更优（AUC 58.81 vs 57.70），且卷积决策层的额外功耗极低（仅 +0.0004 mJ，Table 4），验证了脉冲版中心预测头在精度和效率上的双重优势。

![[assets/figures/papers/paper_list_l2138_https_arxiv_org_abs_2503_08703/figures/011_Table_4.jpg]]
*Table 4: Effect of Decision Layer Design on SDTrack Performance. Experiments are conducted on FE108 using tiny model*

- **预训练的重要性**：无预训练（Experiment 9）导致性能大幅下降至 AUC 47.80%、PR 74.50%，表明 ImageNet-1K 预训练对于脉冲 Transformer 骨干的特征学习至关重要。

### 候选架构对比

Table 3 对比了不同脉冲 Transformer 骨干架构在统一 SDTrack 框架下的表现。SDTrack-Tiny 采用 I-LIF 神经元实现了最低的参数量和能耗，同时保持有竞争力的精度。这一结果说明，SDTrack 的全脉冲驱动设计（包括 SNN Conv Module 和 SNN Transformer Module 的脉冲自注意力机制）能够有效替代混合 ANN-SNN 架构，充分发挥 SNN 的能效优势。

![[assets/figures/papers/paper_list_l2138_https_arxiv_org_abs_2503_08703/figures/009_Table_3.jpg]]
*Table 3: Comparison with candidate architectures. All settings are aligned with SDTrack*

### 定性分析

Figure 8 展示了 SDTrack 与 **OSTrack**（Ye et al., ECCV 2022）、**STARK**（Yan et al., ICCV 2021）在长序列跟踪中的可视化对比。在目标经历欠曝光、过曝光以及相似物体干扰等挑战性场景下，SDTrack 展现出更稳定的跟踪能力，这得益于 GTP 对全局轨迹信息的累积和 IPL 对位置信息的隐式学习。

![[assets/figures/papers/paper_list_l2138_https_arxiv_org_abs_2503_08703/figures/010_Figure_8.jpg]]
*Figure 8: Visualized comparisons of our approach with other excellent trackers OSTrack and STARK during long-sequence tracking. Our method performs better when the target suffers from underexposure, overexposure, and similar object interference*

### 局限性与待验证问题

尽管 SDTrack 在三个基准上取得了领先结果，以下方面仍需注意：

1. **硬件部署未验证**：理论能耗计算基于 MAC/AC 操作统计和 45nm 工艺假设，尚未在真实神经形态芯片上验证实际延迟和功耗。该结论需要硬件实测支持。
2. **超参数泛化性**：GTP 的 α 和 β 在当前实验设置下经手动调节确定（α=30, β=0.8），不同场景或数据集可能需要重新调参，自适应机制有待研究。
3. **场景覆盖有限**：仅在 FE108、FELT、VisEvent 上评估，长时间遮挡、极度快速运动等极端场景下的性能未知。
4. **纯事件挑战**：在纹理极弱的纯事件场景下，缺乏 RGB 辅助信息可能仍存在跟踪失败风险。



## 定位与知识库关联

### 与ANN跟踪基线的继承与分化

SDTrack的方法骨架明显继承自基于Transformer的ANN单目标跟踪范式，但其核心贡献在于将整个流水线脉冲化，并针对事件数据特性重新设计了输入表示与位置编码策略。

**架构继承关系**：SDTrack的骨干网络设计直接对标 **OSTrack**（Ye et al., ECCV 2022）和 **STARK**（Yan et al., ICCV 2021）等ANN Transformer跟踪器，采用模板-搜索帧联合输入的范式。与 **MixFormer**（Cui et al., CVPR 2022）的混合注意力机制不同，SDTrack选择了更简洁的拼接-自注意力路线，通过脉冲自注意力（SSA）实现模板与搜索区域的特征交叉相关。跟踪头方面，SDTrack采纳了中心预测头（Center Head）而非角点头（Corner Head），消融实验表明前者在FE108上带来约1.1%的AUC提升（58.81 vs 57.70），这与ANN跟踪领域从角点预测向中心点预测迁移的趋势一致。

**关键分化点**：SDTrack与上述ANN方法存在三个本质差异。第一，整个骨干由脉冲神经元构建，膜电位更新遵循统一动力学方程 $$$\mathbf{U}[t] = \mathbf{H}[t-1] + \frac{1}{\tau}(\mathbf{X}[t] - (\mathbf{H}[t-1] - \mathbf{U}_{rest}))$$$ ，脉冲生成由阈值判定 $$$\mathbf{S}[t] = f(\mathbf{U}[t] - \mathbf{U}_{thr})$$$ 。第二，位置信息通过内在位置学习（IPL）隐式获取，无需显式位置编码参数。第三，事件输入不再依赖传统Event Frame或Time-Surface，而是通过全局轨迹提示（GTP）累积多方向运动和全局轨迹信息。这三项设计共同使SDTrack在保持竞争精度的同时，将推理能耗压缩至8.16mJ（Tiny版本）。

### 与现有SNN/脉冲跟踪方法的差异

SDTrack并非首个将SNN引入事件跟踪的工作，但它首次构建了全脉冲驱动的Transformer跟踪流水线。

**相对于混合架构的突破**：**STNet**（Zhang et al., CVPR 2022）采用ANN-SNN混合架构，部分模块仍依赖浮点运算；**SNNTrack**（Zhang et al., TIP 2025）虽引入自适应膜时间常数，但同样未实现全脉冲化。SDTrack的关键推进在于：从GTP事件聚合、IPL位置学习、SNN卷积模块到SNN Transformer模块，整个前向过程均由脉冲驱动，仅在最终的跟踪头决策层保留少量浮点操作（卷积决策层的额外功耗仅+0.0004 mJ）。这一设计使得SDTrack-Tiny在FE108上以59.0% AUC超越Spike-driven Transformer V3（Yao et al., NeurIPS 2024 / arXiv 2024）的57.4% AUC，同时参数量仅19.61M。

**事件聚合方法的范式革新**：传统事件聚合方法（如Event Frame仅记录最新极性，Time-Surface编码局部时空表面）无法充分捕获全局轨迹信息。GTP的三通道设计——正极性累积 $h_i^1(x,y) = \alpha \cdot \sum_{t_k \in L} \delta(x - x_k, y - y_k) \delta(p_k - 1)$ 、负极性累积 $h_i^2(x,y) = \alpha \cdot \sum_{t_k \in L} \delta(x - x_k, y - y_k) \delta(p_k + 1)$ 以及全局轨迹累积 $h_i^3(x,y) = h_{i-1}^3(x,y) \cdot \beta + \alpha \cdot \sum_{j=1}^{2} C(h_{i-1}^j(x,y), h_i^j(x,y))$ ——在FE108上的消融实验（Figure 4）验证了其对多种聚合方法的优势。轨迹通道通过衰减因子β（最优值0.8）保留历史运动信息，新增事件指示函数 $C(h_{i-1}^j, h_i^j) = \mathbb{I}(h_{i-1}^j = 0 \ \mathrm{and} \ h_i^j \neq 0)$ 仅在像素从无事件变为有事件时触发叠加，有效抑制噪声累积。

### 适用边界与已知局限

SDTrack在三个事件跟踪基准（FE108、FELT、VisEvent）上取得了最优或次优结果，但其适用边界存在以下约束：

**超参数敏感性**：GTP的性能依赖于两个关键超参数的手动调节——极性累积缩放系数α（最优值30）和轨迹衰减因子β（最优值0.8）。Figure 6展示了参数选择过程，但不同场景（如目标运动速度差异极大、事件噪声水平不同）可能需要重新调参，缺乏自适应机制。

**预训练依赖性**：消融实验（Table 2, Experiment 9）表明，移除ImageNet-1K预训练导致性能急剧下降（AUC从58.81降至47.80，PR从91.30降至74.50）。这意味着SDTrack对预训练权重有较强依赖，从头训练可能难以收敛到可用的精度水平。

**硬件验证缺失**：论文中的能耗计算基于理论公式 $E = T \cdot \bigl( E_{\mathrm{MAC}} \cdot \sum_i \mathrm{FL}_{\mathrm{SNNConv}}^i + E_{\mathrm{AC}} \cdot (\sum_j \mathrm{FL}_{\mathrm{SNNConv\&FC}}^j \cdot fr^j) + \sum_k \mathrm{FL}_{\mathrm{SSA}}^k \bigr)$ ，假设45nm CMOS工艺下的MAC和AC操作能耗常数。该估算未在真实神经形态芯片（如Loihi、Speck）上验证，实际延迟和功耗可能因芯片架构、片上通信开销等因素偏离理论值。

**场景泛化性未知**：现有评估仅覆盖三个数据集，未涉及长时间遮挡、极度快速运动、纯纹理缺失等极端场景。Figure 8的定性结果表明SDTrack在欠曝光、过曝光和相似物干扰下优于OSTrack和STARK，但这些场景的定量统计显著性未报告。此外，SDTrack未利用RGB信息辅助跟踪，在纹理极弱的纯事件场景下可能仍存在挑战。

### 开放问题

1. **神经形态芯片部署**：SDTrack在真实神经形态硬件（如Speck、Loihi 2）上的实际推理延迟、功耗和精度退化程度如何？理论能耗估算中的AC操作发放率假设是否与硬件行为一致？

2. **多模态SNN跟踪**：将RGB帧与事件流融合的脉冲驱动跟踪器能否进一步提升鲁棒性？特别是在事件纹理缺失的场景下，RGB信息的补充可能至关重要，但如何设计低功耗的多模态脉冲融合机制仍是开放挑战。

3. **GTP的自适应参数化**：能否通过学习的方式动态调整α和β，使GTP适应不同运动速度和场景噪声水平？这可能需要引入轻量的元学习或条件参数生成模块，但需谨慎控制额外开销。

4. **长时跟踪与重检测**：SDTrack目前聚焦于短时单目标跟踪，未涉及目标丢失后的重检测机制。全脉冲驱动的长时跟踪框架（含目标重识别模块）将是一个有价值但更具挑战的方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/SDTrack_A_Baseline_for_Event_based_Tracking_via_Spiking_Neural_Networks.pdf]]
