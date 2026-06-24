---
title: "A General Spatio-Temporal Backbone with Scalable Contextual Pattern Bank for Urban Continual Forecasting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_General_Spatio_Temporal_Backbone_with_Scalable_Contextual_Pattern_Bank_for_Urban_Continual_Forecasting.pdf
aliases:
- GSTBSCPBUCF
- STBP
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/time_series
core_operator: "可扩展的上下文模式库（Contextual Pattern Bank）与冻结的通用时空骨干网络之间的协同机制。模式库通过参数扩展增量更新，并通过门控和注意力机制与骨干网络交互，在保留通用知识的同时适应新场景。"
primary_logic: "将通用时空骨干网络与可扩展上下文模式库分离：骨干网络负责提取频域稳定表征和建模动态空间相关性，并在增量训练中冻结以保留通用知识；模式库通过参数扩展增量更新，捕获节点级别的异质性和相关性，从而在避免灾难性遗忘的同时实现高效适应。"
claims:
- "STBP在PEMS-Stream、CA-Stream和AIR-Stream三个数据集上的平均MAE分别比最佳基线降低21.44%、21.93%和2.35%。"
- "在PEMS-Stream数据集上，STBP的平均MAE为12.31±0.07，RMSE为20.52±0.11，MAPE为15.65±0.21，均优于所有基线。"
- "在CA-Stream数据集上，STBP的平均MAE为15.77±0.09，RMSE为25.70±0.16，MAPE为16.20±0.08，均优于所有基线。"
- "在AIR-Stream数据集上，STBP的平均MAE为23.64±0.23，RMSE为37.76±0.30，MAPE为29.70±0.35，均优于所有基线。"
---

# A General Spatio-Temporal Backbone with Scalable Contextual Pattern Bank for Urban Continual Forecasting

> [!tip] 核心洞察
> 将通用时空骨干网络与可扩展上下文模式库分离：骨干网络负责提取频域稳定表征和建模动态空间相关性，并在增量训练中冻结以保留通用知识；模式库通过参数扩展增量更新，捕获节点级别的异质性和相关性，从而在避免灾难性遗忘的同时实现高效适应。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向城市持续预测的通用时空骨干网络与可扩展上下文模式库 |
| 英文题名 | A General Spatio-Temporal Backbone with Scalable Contextual Pattern Bank for Urban Continual Forecasting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=LHSea6DI8U); [GitHub](https://github.com/Aoyu-Liu/STBP) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/time_series |
| Method | STBP |
| Dataset | PEMS-Stream, CA-Stream |

> [!tip] 效果简介
> - PEMS-Stream 上，MAE Avg. 为 12.31±0.07，对比 15.67 (EAC)，变化 -21.44%。
> - PEMS-Stream 上，RMSE Avg. 为 20.52±0.11，对比 25.30 (EAC)，变化 -18.89%。
> - PEMS-Stream 上，MAPE Avg. 为 15.65±0.21，对比 19.14 (EAC)，变化 -18.23%。

## 概述

本文聚焦于**城市持续时空预测**（Continual Spatio-Temporal Forecasting, CSTF）问题，其核心挑战在于：随着时间推移，传感器网络会动态扩展（节点增加、分布漂移），模型必须在适应新数据的同时不遗忘已学知识。现有方法在骨干网络建模能力（如堆叠图卷积与时间卷积）与稳定性-适应性平衡机制（如直接参数扩展或提示拼接）上存在瓶颈，导致难以处理长期分布漂移和动态变化的时空相关性。

针对此，论文提出**STBP**（Spatio-Temporal Backbone with Pattern bank），其核心洞察在于将**通用时空骨干网络**与**可扩展上下文模式库**分离设计。骨干网络（包含频域网络FreNet和双流线性图注意力DLGA）负责提取频域稳定表征并建模动态空间相关性，在初始训练后**冻结**以保留通用知识；上下文模式库则通过**参数增量扩展**（无压缩）捕获节点级别的异质性与相关性，并通过门控与注意力机制与骨干网络交互，在避免灾难性遗忘的同时实现高效适应。该方法将骨干网络更新策略从全参数微调改为冻结+模式库扩展，将空间相关性建模从二次复杂度图注意力降为线性复杂度，并引入频域网络显式提取稳定成分。

在三个真实流式数据集（PEMS-Stream、CA-Stream、AIR-Stream）上的实验表明，STBP在所有指标上均超越现有持续学习方法（如EAC、STRAP等）。具体地，其在PEMS-Stream上的平均MAE为12.31±0.07（比最佳基线EAC降低21.44%），在CA-Stream上为15.77±0.09（降低21.93%），在AIR-Stream上为23.64±0.23（降低2.35%）。消融实验证实，移除DLGA模块或模式库参数扩展均会导致性能显著下降，验证了各组件的必要性。

## 背景与动机

城市时空数据（如交通流量、空气质量）的持续预测（Continual Spatio-Temporal Forecasting, CSTF）面临一个根本性矛盾：数据分布和传感器网络拓扑结构随时间动态演化，但模型必须在保留历史知识的同时高效适应新场景。现有方法在这一问题上存在两个关键瓶颈。

**瓶颈一：骨干网络建模能力不足。** 现有的CSTF方法（如TrafficStream、STKEC）通常采用堆叠图卷积和时间卷积作为骨干网络。这类架构在处理静态或缓慢变化的时空相关性时尚可应对，但在面对节点数量动态增长（如PEMS-Stream数据集从655个节点扩展到871个）、新增节点带来全新分布模式（MMD测试显示CA-Stream数据集新增节点分布漂移显著，MMD=0.3361, p=0.0010）的场景时，其有限的容量难以同时捕获长期稳定的周期性模式与快速变化的局部相关性。

**瓶颈二：稳定性-适应性平衡机制缺失。** 持续学习要求模型在新数据上适应（适应性）而不遗忘旧知识（稳定性）。现有方法在实现这一平衡时存在明显缺陷：全参数微调（如GWNet、STID的增量版本）导致灾难性遗忘；而基于回放（TrafficStream）或提示池压缩（EAC）的方法，则在压缩过程中不可避免地丢失历史信息。EAC采用的“扩展-压缩”策略虽然比纯回放更高效，但其压缩步骤本质上是一种有损操作，无法完全保留所有历史模式。

**本文的核心洞察**在于将通用时空骨干网络与可扩展的上下文模式库（Contextual Pattern Bank）解耦。骨干网络负责提取频域稳定表征（通过FFT和可学习频域嵌入）和建模动态空间相关性（通过线性图注意力），并在初始训练后冻结以保留通用知识。模式库则通过纯参数增量扩展（无压缩）更新，通过门控和注意力机制与骨干交互，捕获节点级别的异质性和相关性。这一设计使得模型在避免灾难性遗忘的同时实现高效适应——实验证据表明，基于冻结骨干的轻量级提示适应（如STBP、EAC、STRAP）比全参数微调获得更高的平均精度。

**现有方法的缺口**还体现在计算效率上：传统图注意力机制的二次复杂度（O(N²)）在大规模节点扩展场景下难以承受。STBP通过随机特征映射将注意力复杂度降至线性（O(N)），同时引入模式库作为额外键，在不牺牲建模能力的前提下实现了可扩展性。

## 核心创新

STBP 的核心创新在于将**通用时空骨干网络**与**可扩展上下文模式库 (Contextual Pattern Bank)** 解耦并协同，从而在持续学习场景中同时解决骨干网络建模能力不足与稳定性-适应性平衡机制缺失两大瓶颈。

**关键因果机制**：冻结的骨干网络负责提取通用时空表征，而模式库通过参数增量扩展来捕获节点级别的异质性和动态相关性。这种分离使得模型在避免灾难性遗忘的同时，能够高效适应新场景。

**具体创新点（Changed Slots）** 如下：

1.  **骨干网络更新策略**：现有持续方法（如 TrafficStream, STKEC）通常在增量阶段对骨干网络进行全参数微调或直接扩展参数，导致灾难性遗忘。STBP 在初始训练后**冻结骨干网络**，仅通过**上下文模式库的参数扩展**进行适应。此举确保了从历史数据中学到的通用知识（如频域稳定成分）得以保留。
2.  **空间相关性建模**：现有方法多依赖固定邻接矩阵或二次复杂度的图注意力。STBP 提出**双流线性图注意力 (DLGA)**，基于随机特征映射将复杂度降至 $O(N)$，并引入模式库作为额外键，从而高效捕捉动态变化的拓扑结构。消融实验证实移除 DLGA 会导致性能显著下降。
3.  **分布漂移处理**：现有方法依赖回放或正则化，缺乏对数据中长期趋势、周期等稳定成分的显式提取。STBP 引入**频域网络 (FreNet)**，通过 FFT 和可学习频域嵌入提取稳定低频成分，抑制高频噪声，从而更鲁棒地应对分布漂移。
4.  **知识保留机制**：现有方法（如 EAC 的提示池压缩）在压缩过程中可能丢失历史信息。STBP 的上下文模式库采用**纯参数增量扩展，无压缩**，通过门控和注意力机制与骨干交互，更完整地保留了历史知识。

**核心证据**：在 PEMS-Stream、CA-Stream 和 AIR-Stream 三个数据集上，STBP 的平均 MAE 分别比最佳基线（EAC）降低 **21.44%**、**21.93%** 和 **2.35%**。在少样本场景（10%数据）下，PEMS-Stream 和 CA-Stream 上的 MAE 分别降低 **12.22%** 和 **13.32%**。

## 整体框架

![[assets/figures/papers/iclr26_0002_LHSea6DI8U_A_General_Spatio-Temporal_Backbone_with_Scalable/figures/002_Figure_2.jpg]]
*Figure 2: The overall workflow and architecture of STBP*

STBP（Spatio-Temporal Backbone with Pattern Bank）的整体架构由两个解耦的核心组件构成：一个**冻结的通用时空骨干网络**（General Spatio-Temporal Backbone）和一个**可扩展的上下文模式库**（Contextual Pattern Bank）。这一设计的核心动机在于打破现有持续时空预测方法中骨干网络建模能力不足与稳定性-适应性平衡缺失的双重瓶颈。骨干网络在初始阶段训练完成后即被冻结，以保留从历史数据中习得的通用知识；上下文模式库则通过纯参数增量扩展（无压缩）在后续增量周期中持续更新，从而在避免灾难性遗忘的同时实现对新场景的高效适应。

**输入输出流与模块关系**：整个 pipeline 以流式时空图序列 $\mathbb{G} = \{G_\tau\}_{\tau=1}^{\mathcal{T}}$ 和历史观测 $\mathbf{X}_\tau$ 作为输入，输出未来信号预测 $\hat{\mathbf{Y}}_\tau = f_{\boldsymbol{\theta}}(G_\tau, \mathbf{X}_\tau)$。数据流依次经过以下模块：

1. **频域网络（FreNet）**：作为第一级处理模块，将输入时空数据映射到高维表示。通过 FFT 和可学习的频域嵌入 $\mathbf{F}_\tau$ 提取稳定成分（如周期性和趋势），同时抑制高频噪声，操作形式化为 $\mathbf{H}_\tau^f = \mathrm{IFFT}(\mathrm{FFT}(\mathbf{H}_\tau) \odot \mathbf{F}_\tau)$。这一设计直接针对分布漂移问题：频域稳定表征为后续的持续学习提供了跨周期不变的特征基础。

2. **双流线性图注意力（DLGA）**：在 FreNet 输出的基础上捕捉动态空间相关性。DLGA 采用基于随机特征映射 $\phi$ 的线性注意力机制，将标准二次复杂度 $O(N^2)$ 降低为线性 $O(N)$。其核心创新在于引入双流设计：注意力计算不仅考虑节点间的原始关系 $\phi(\mathbf{Q})\phi(\mathbf{K})^\top$，还引入模式库作为额外键 $\phi(\mathbf{Q})\phi(\mathbf{P}_\tau^{(2)})^\top$，从而评估输入模式与存储知识之间的关系。这一机制使得模型能够动态适应拓扑变化（如新增节点），同时利用历史模式知识。

3. **上下文模式库（Contextual Pattern Bank）**：由三组可训练参数 $\mathbf{P}_\tau^{(0)}$、$\mathbf{P}_\tau^{(1)}$、$\mathbf{P}_\tau^{(2)}$ 组成，分别通过不同的交互机制与骨干网络协同工作。模式库在每个增量周期通过拼接新参数 $\mathbf{P}_\tau' = \mathbf{P}_{\tau-1} \parallel \Delta\mathbf{P}_\tau$ 进行扩展，不进行任何压缩操作，从而完全保留历史知识。与骨干网络的交互通过提示引导机制（Prompt-Based Guidance）实现：$\mathbf{P}_\tau^{(0)}$ 作为门控缩放因子，$\mathbf{P}_\tau^{(1)}$ 通过门控函数 $\mathbf{H}_\tau' = \mathbf{P}_\tau^{(1)} \cdot h_\theta(\mathbf{H}_\tau \cdot (1 + \mathbf{P}_\tau^{(0)}))$ 自适应建模节点异质性，$\mathbf{P}_\tau^{(2)}$ 则作为 DLGA 的额外键参与空间相关性建模。

**关键设计权衡**：该架构的核心洞察在于将通用知识提取与场景自适应分离。骨干网络中的 FreNet 负责提取域不变频率模式，DLGA 负责动态捕捉拓扑变化，两者在增量阶段冻结，确保稳定性；模式库通过参数扩展捕获节点级别的异质性和相关性，提供适应性。消融实验（Figure 4）证实，移除 DLGA 模块会导致性能显著下降，验证了动态空间相关性捕捉的必要性；而模式库的参数扩展对于缓解灾难性遗忘至关重要。对比实验表明，在冻结骨干网络上进行轻量级提示适应比全参数微调获得更高的平均精度，这验证了骨干冻结策略的有效性。

**效率特征**：DLGA 的线性注意力机制将计算复杂度从 $O(N^2)$ 降至 $O(N)$，使得 STBP 在面对 CA-Stream 数据集从 480 节点扩展到 1698 节点的剧烈拓扑变化时仍能保持高效。效率对比实验（Figure 8）显示，STBP 的平均训练时间显著低于未使用线性注意力的版本和重新训练版本。

## 核心模块与公式推导

STBP 的核心架构由两大模块构成：一个**冻结的通用时空骨干网络**（General Spatio-Temporal Backbone）和一个**可扩展的上下文模式库**（Contextual Pattern Bank）。其核心设计理念是将通用知识提取与增量适应解耦。

### 问题定义与符号体系

持续时空预测问题被形式化为一个随时间演化的图序列：

$$\mathbb { G } = { \left\{ { G } _ { \tau } \right\} } _ { \tau = 1 } ^ { \tau }$$

其中每个增量周期 $\tau$ 对应一个图 $G_\tau$。给定当前图 $G_\tau$ 和历史观测 $\mathbf{X}_\tau$，模型 $f_{\boldsymbol{\theta}}$ 预测未来信号 $\hat{\mathbf{Y}}_\tau$：

$$\hat { \mathbf Y } _ { \tau } = f _ { \boldsymbol \theta } ( G _ { \tau } , { \mathbf X } _ { \tau } )$$

优化目标是在每个周期 $\tau$ 上最小化期望损失，求得最优参数 $\boldsymbol{\theta}_\tau^*$：

$$\boldsymbol { \theta } _ { \tau } ^ { * } = \arg \operatorname* { m i n } _ { \boldsymbol { \theta } } \mathbb { E } _ { ( G _ { \tau } , \mathbf { X } _ { \tau } , \mathbf { Y } _ { \tau } ) \sim \mathcal { D } _ { \tau } } \left[ \mathcal { L } \left( f _ { \boldsymbol { \theta } } ( G _ { \tau } , \mathbf { X } _ { \tau } ) , \mathbf { Y } _ { \tau } \right) \right]$$

### 骨干网络：频域稳定表征与线性图注意力

骨干网络包含两个核心子模块，均在初始训练后冻结：

**1. 频域网络（FreNet）**：通过傅里叶变换提取时域中的稳定成分（如周期性和趋势），抑制高频噪声。其核心操作为：

$$\mathbf { H } _ { \tau } ^ { f } = \mathrm { I F F T } ( \mathrm { F F T } ( \mathbf { H } _ { \tau } ) \odot \mathbf { F } _ { \tau } )$$

其中 $\mathbf{F}_\tau$ 是可学习的频域嵌入，通过逐元素乘操作 $\odot$ 对频域分量进行加权，再通过逆傅里叶变换（IFFT）得到稳定特征 $\mathbf{H}_\tau^f$。这一机制直接对应论文中“提取稳定成分”的瓶颈解决策略。

**2. 双流线性图注意力（DLGA）**：用于捕捉动态空间相关性，其核心创新在于将标准二次复杂度 $O(N^2)$ 的图注意力近似为线性复杂度 $O(N)$。近似公式为：

$$\mathrm { A t t e n t i o n } ( \mathbf { Q } , \mathbf { K } , \mathbf { V } , \mathbf { P } _ { \tau } ^ { ( 2 ) } ) \approx ( \phi ( \mathbf { Q } ) \phi ( \mathbf { K } ) ^ { \top } + \phi ( \mathbf { Q } ) \phi ( \mathbf { P } _ { \tau } ^ { ( 2 ) } ) ^ { \top } ) \mathbf { V }$$

这里 $\phi$ 是随机特征映射函数，将查询 $\mathbf{Q}$ 和键 $\mathbf{K}$ 映射到低维空间。关键创新在于引入了模式库的第三组参数 $\mathbf{P}_\tau^{(2)}$ 作为额外的键，使注意力机制不仅能捕捉节点间的相关性，还能评估输入模式与存储知识的关系。消融实验证实，移除 DLGA 会导致性能显著下降（置信度 0.95）。

### 上下文模式库：参数增量扩展与提示引导

模式库 $\mathbf{P}_\tau$ 由三组可训练参数构成：$\mathbf{P}_\tau^{(0)}$、$\mathbf{P}_\tau^{(1)}$、$\mathbf{P}_\tau^{(2)}$，分别负责门控调制、特征变换和注意力键扩展。其增量更新策略是纯参数扩展，无压缩：

$$\mathbf { P } _ { \tau } ^ { \prime } = \mathbf { P } _ { \tau - 1 } \parallel \Delta \mathbf { P } _ { \tau }$$

即通过拼接新参数 $\Delta\mathbf{P}_\tau$ 扩展模式库，完整保留历史知识（置信度 0.95）。这与基线方法 EAC 的“扩展-压缩”策略形成对比——论文明确论证了压缩可能导致历史信息丢失。

模式库与骨干网络的交互通过提示引导机制实现，其门控函数为：

$$\mathbf { H } _ { \tau } ^ { \prime } = \mathbf { P } _ { \tau } ^ { ( 1 ) } \cdot h _ { \theta } \big ( \mathbf { H } _ { \tau } \cdot ( 1 + \mathbf { P } _ { \tau } ^ { ( 0 ) } ) \big )$$

其中 $\mathbf{H}_\tau$ 是骨干网络的隐藏表示，$\mathbf{P}_\tau^{(0)}$ 作为门控调制因子，$\mathbf{P}_\tau^{(1)}$ 作为特征变换矩阵，$h_\theta$ 是映射函数。这一机制使模式库能够自适应建模节点级别的异质性和相关性。

整体预测形式化为：

$$\hat { \mathbf Y } _ { \tau } = \mathcal { M } _ { \boldsymbol \theta } ( \mathbf X _ { \tau } , \mathbf P _ { \tau } )$$

即骨干网络 $\mathcal{M}_\theta$ 联合输入 $\mathbf{X}_\tau$ 和模式库 $\mathbf{P}_\tau$ 进行预测。

### 评估指标

论文使用三个标准指标评估性能：

$$\mathrm{MAE} = \frac{1}{n} \sum_{i=1}^n |y_i - \hat{y}_i|$$

$$\mathrm{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2}$$

$$\mathrm{MAPE} = \frac{1}{n} \sum_{i=1}^n \left|\frac{y_i - \hat{y}_i}{y_i}\right| \times 100\%$$

### 关键机制总结

STBP 的核心因果链为：骨干网络（FreNet + DLGA）提取稳定的频域表征和动态空间相关性 → 冻结骨干网络以保留通用知识 → 模式库通过参数增量扩展捕获节点级异质性和新分布 → 门控和注意力机制实现模式库与骨干的协同。这一设计直接针对现有方法在“骨干网络建模能力不足”和“稳定性-适应性平衡缺失”两个瓶颈。

## 实验与分析

### 主实验结果

STBP在三个持续时空预测基准数据集上均取得了最优的平均性能。在PEMS-Stream数据集上，STBP的平均MAE为12.31±0.07，RMSE为20.52±0.11，MAPE为15.65±0.21，相比最佳基线EAC分别降低了21.44%、18.89%和18.23%（Table 1）。在CA-Stream数据集上，STBP的平均MAE为15.77±0.09，RMSE为25.70±0.16，MAPE为16.20±0.08，相比EAC分别降低了21.93%、17.58%和19.68%（Table 1）。在AIR-Stream数据集上，STBP的平均MAE为23.64±0.23，RMSE为37.76±0.30，MAPE为29.70±0.35，相比EAC分别降低了2.35%、0.19%和6.51%（Table 1）。这些结果表明，STBP在交通流（PEMS-Stream和CA-Stream）和空气质量（AIR-Stream）两种不同的城市预测场景中均具有显著的性能优势，且改善幅度在节点扩张幅度最大的CA-Stream上最为突出。

![[assets/figures/papers/iclr26_0002_LHSea6DI8U_A_General_Spatio-Temporal_Backbone_with_Scalable/figures/004_Table_1.jpg]]
*Table 1: Main experimental results. Bold: best, underline: second best. Table 2: Comparison of few-shot forecasting performance*

### 少样本预测性能

在仅使用10%训练数据的少样本场景下，STBP依然保持了最优性能。在PEMS-Stream 10%设置下，STBP的MAE为13.58±0.05，RMSE为22.24±0.13，相比最佳基线EAC分别降低了12.22%和8.55%（Table 2）。在CA-Stream 10%设置下，STBP的MAE为17.11±0.03，RMSE为27.48±0.16，相比EAC分别降低了13.32%和16.42%（Table 2）。这一结果验证了冻结骨干网络结合可扩展模式库的策略在数据稀缺条件下的鲁棒性——骨干网络保留的通用时空知识弥补了少量样本的信息不足。

![[assets/figures/papers/iclr26_0002_LHSea6DI8U_A_General_Spatio-Temporal_Backbone_with_Scalable/figures/005_Table_2.jpg]]

### 消融实验

消融实验（Figure 4）揭示了各核心模块的关键贡献：
1. **动态空间相关性建模**：移除DLGA模块导致性能显著下降，验证了其利用随机特征映射实现线性复杂度注意力机制的有效性。DLGA通过将模式库作为额外键，使模型能够动态评估输入模式与存储知识的关系，这是捕捉节点拓扑变化的核心机制。
2. **模式库参数扩展**：移除模式库的参数扩展（即仅微调而不扩展）导致灾难性遗忘加剧，性能接近全参数微调基线。这表明纯参数增量扩展（无压缩）对于完整保留历史知识至关重要，与EAC的"扩展-压缩"策略形成对比——压缩过程可能导致信息丢失。
3. **骨干网络冻结策略**：轻量级提示适应（如EAC、STRAP、STBP）在冻结骨干网络上获得的平均精度高于全参数微调。这一现象的根本原因在于：全参数微调在增量阶段会覆盖骨干网络学习到的频域稳定表征，而冻结策略将知识保留与适应能力解耦。

### 模式库可视化分析

t-SNE可视化（Figure 3）显示，STBP的上下文模式库能够有效区分和整合不同的时空模式。新加入节点引入的新模式被纳入现有模式簇中，表明模式库具有自适应的归纳能力。这种能力不依赖于特定的时空数据模态——在PEMS-Stream、CA-Stream和AIR-Stream上均观察到类似的聚类行为。

### 效率分析

STBP的线性图注意力（DLGA）将计算复杂度从二次降低到线性。效率对比（Figure 8）显示，STBP的训练时间显著低于不使用线性注意力的版本（STBP O(N²)）和移除模式库的重新训练版本（Retrain）。这一优势在大规模节点扩张场景（如CA-Stream从480扩张到1698）下尤为关键。

### 失败模式与局限性

尽管STBP在三个数据集上表现优异，但存在以下失败模式：
1. **跨领域泛化**：当前持续学习方法（包括STBP）通常假设增量任务来自相似领域。当源域和目标域之间存在显著结构差异时（如从交通流预测迁移到空气质量预测），特征空间不对齐和灾难性遗忘加剧的双重挑战尚未被验证。
2. **单任务限制**：STBP目前仅支持单任务持续学习设置，无法处理多任务交替学习场景。
3. **AIR-Stream上的边际改善**：STBP在AIR-Stream上的MAE改善仅为2.35%，远低于PEMS-Stream和CA-Stream。这可能是因为AIR-Stream的节点扩张幅度较小（1087→1202），且空气质量数据的空间相关性模式不如交通流数据复杂，导致模式库的增量扩展优势未能充分体现。该假设需要进一步验证。

### 补充图表

![[assets/figures/papers/iclr26_0002_LHSea6DI8U_A_General_Spatio-Temporal_Backbone_with_Scalable/figures/019_Table_3.jpg]]
*Table 3: The notations that are commonly used in the manuscript*

![[assets/figures/papers/iclr26_0002_LHSea6DI8U_A_General_Spatio-Temporal_Backbone_with_Scalable/figures/020_Table_4.jpg]]
*Table 4: Overview of continual spatio-temporal forecasting datasets*

![[assets/figures/papers/iclr26_0002_LHSea6DI8U_A_General_Spatio-Temporal_Backbone_with_Scalable/figures/021_Table_5.jpg]]
*Table 5: Topological dynamics and evaluation purposes of the datasets*

## 方法谱系与知识库定位

STBP 在持续时空预测（CSTF）方法谱系中的定位，核心在于将“通用骨干网络”与“可扩展上下文模式库”解耦，从而同时解决了现有方法在骨干建模能力不足和稳定性-适应性平衡机制缺失两个瓶颈。

**与基线方法的关系**。STBP 的对比基线覆盖了 CSTF 领域的代表性方法。TrafficStream 是首个 CSTF 方法，依赖历史数据回放和参数平滑；STKEC 引入影响力知识扩展和记忆增强知识巩固；PECPM 基于模式匹配；STRAP 采用检索增强学习和即插即用提示；EAC 使用动态提示池扩展与压缩。STBP 与这些方法的关键区别在于：EAC 等提示池方法在压缩阶段可能丢失历史信息，而 STBP 的上下文模式库采用纯参数增量扩展（无压缩），更完整地保留历史知识。在骨干网络更新策略上，STBP 冻结骨干网络，仅通过模式库的参数扩展适应新场景，而传统方法（如 TrafficStream、STKEC）在增量阶段对骨干网络进行全参数微调或直接扩展参数。实验证据表明，在冻结骨干网络上进行轻量级提示适应（如 EAC、STRAP、STBP）比全参数微调获得更高的平均精度（置信度 0.9）。

**适用边界**。STBP 的优势在节点规模变化显著且分布漂移明显的场景中最为突出。在 PEMS-Stream（节点从 655 扩展到 871，7 个增量周期）和 CA-Stream（节点从 480 扩展到 1698，4 个周期）上，STBP 的平均 MAE 分别比最佳基线 EAC 降低 21.44% 和 21.93%（置信度 0.95）。在 AIR-Stream（节点从 1087 扩展到 1202）上，MAE 降低幅度仅为 2.35%（置信度 0.95），表明当节点扩展幅度较小时，STBP 的相对优势减弱。少样本场景（10% 数据）下，STBP 在 PEMS-Stream 和 CA-Stream 上的 MAE 分别降低 12.22% 和 13.32%（置信度 1.0），验证了其在小样本条件下的鲁棒性。消融实验证实，移除 DLGA 模块会导致性能显著下降（置信度 0.95），模式库的参数扩展对缓解灾难性遗忘至关重要（置信度 0.9）。

**局限与开放问题**。STBP 当前存在几个明确的边界条件。首先，它仅支持单任务持续学习设置，无法直接处理多任务或跨领域场景。其次，尽管 DLGA 通过随机特征映射将图注意力复杂度从二次降至线性（公式：$\mathrm{Attention}(\mathbf{Q},\mathbf{K},\mathbf{V},\mathbf{P}_\tau^{(2)}) \approx (\phi(\mathbf{Q})\phi(\mathbf{K})^\top + \phi(\mathbf{Q})\phi(\mathbf{P}_\tau^{(2)})^\top)\mathbf{V}$），但其在源域和目标域之间存在显著结构差异时的鲁棒性尚未验证。第三，当前持续学习方法（包括 STBP）通常假设增量任务来自相似领域，这与现实世界中动态异构的环境存在差距，跨领域分布漂移会带来特征空间不对齐和灾难性遗忘加剧的双重挑战。

由此引出的开放问题包括：如何将 STBP 扩展到跨领域持续时空预测？在跨领域场景下，如何引入显式的领域自适应机制以更好地区分领域特定特征和共享特征？能否探索跨领域共享的上下文模式库以在保持效率的同时增强适应性？以及如何将 STBP 与大型语言模型（LLMs）结合以提升时空和时间序列预测的性能？这些问题的解决将决定 STBP 从受控实验环境向真实城市部署场景迁移的可能性。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_General_Spatio_Temporal_Backbone_with_Scalable_Contextual_Pattern_Bank_for_Urban_Continual_Forecasting.pdf

![[paperPDFs/ICLR_2026/A_General_Spatio_Temporal_Backbone_with_Scalable_Contextual_Pattern_Bank_for_Urban_Continual_Forecasting.pdf]]
