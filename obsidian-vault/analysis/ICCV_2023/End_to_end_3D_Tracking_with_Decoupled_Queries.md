---
title: "End-to-end 3D Tracking with Decoupled Queries"
type: paper
paper_level: A
venue: ICCV
year: 2023
pdf_ref: paperPDFs/ICCV_2023/End_to_end_3D_Tracking_with_Decoupled_Queries.pdf
project_link: https://sites.google.com/view/dqtrack
code_link: null
aliases:
- EE3TDQ
tags:
- ICCV_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将单查询解耦为专门的对象查询和轨迹查询，使两个任务各自使用独立的查询，从而消除表示冲突。"
primary_logic: "通过解耦查询，并设计可学习的关联模块与时间更新模块，在保持端到端紧凑流水线的同时，显著提升了3D跟踪的鲁棒性和准确性。"
claims:
- "与单查询方法相比，解耦查询在nuScenes验证集上带来4.0% AMOTA和7.4% mAP的提升。"
- "DQTrack在nuScenes测试集上达到52.3% AMOTA，超越所有先前学习型跟踪器，例如比PF-Track高8.9% AMOTA。"
- "nuScenes test 上 AMOTA = 52.3%"
- "nuScenes val 上 AMOTA = 28.5%"
---

# End-to-end 3D Tracking with Decoupled Queries

> [!tip] 核心洞察
> 通过解耦查询，并设计可学习的关联模块与时间更新模块，在保持端到端紧凑流水线的同时，显著提升了3D跟踪的鲁棒性和准确性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于解耦查询的端到端3D多目标跟踪 |
| 英文题名 | End-to-end 3D Tracking with Decoupled Queries |
| 会议/期刊 | ICCV 2023 |
| Links | [paper](https://openaccess.thecvf.com/content/ICCV2023/papers/Li_End-to-end_3D_Tracking_with_Decoupled_Queries_ICCV_2023_paper.pdf) · [Project](https://sites.google.com/view/dqtrack) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DQTrack |
| Dataset | nuScenes test, nuScenes val, nuScenes val (PETRv2 encoder) |

> [!tip] 效果简介
> - nuScenes test 上，AMOTA 为 52.3%，对比 43.4% (PF-Track)，变化 +8.9%。
> - nuScenes val 上，AMOTA 为 28.5%，对比 24.5% (SinQuery)，变化 +4.0%。
> - nuScenes val (PETRv2 encoder) 上，AMOTA 为 44.6%，对比 约39.8% (MUTR3D* from Table 1)。

## 概要

### 1. 问题与瓶颈

端到端3D多目标跟踪的核心挑战在于如何在一个紧凑的流水线中同时完成**身份无关的检测**和**身份相关的跟踪**。先前基于查询（query）的跟踪方法（如 **MUTR3D**, Zhang et al., CVPR 2022）采用**单一共享查询**来同时处理这两个任务，导致检测与跟踪的表示冲突，损害了整体性能。而传统的tracking-by-detection方法（如 **CenterTrack**, Yin et al., CVPR 2021）则依赖启发式的后处理匹配（如IoU或距离匹配），破坏了端到端的可微性，且匹配精度有限。

### 2. 核心方法

本文提出 **DQTrack**，核心思想是将单查询**解耦**为专门的对象查询（object query）和轨迹查询（track query），使检测和跟踪各自使用独立的表示，从根源上消除表示冲突。在此基础上，设计了两个关键模块：

- **可学习关联模块**：通过嵌入交互和查询关联，融合外观与运动特征，计算可微的轨迹-对象亲和度矩阵，实现端到端的可学习匹配。
- **时间更新模块**：利用指数移动平均（EMA）分别更新轨迹查询的外观表示和对象嵌入，同时基于速度预测更新轨迹位置，保持时序表示的最新与平滑。

该方法在保持端到端紧凑流水线的同时，显著提升了3D跟踪的鲁棒性和准确性。

### 3. 主要结果

- 在 **nuScenes 测试集**上，DQTrack 达到 **52.3% AMOTA**，超越所有先前基于学习的跟踪器，比 PF-Track 高出 **8.9% AMOTA**（Table 2）。
- 在 **nuScenes 验证集**上，与单查询方法相比，解耦查询带来 **4.0% AMOTA** 和 **7.4% mAP** 的提升（Table 3）。

### 4. 方法定位

DQTrack 属于**端到端查询式跟踪**范式，在方法谱系中处于 tracking-by-detection 和 tracking-with-query 之后的新一代方法。其解耦查询设计使其区别于：

- **CenterTrack** 等 tracking-by-detection 方法：后者依赖不可微的启发式匹配。
- **MUTR3D** 等单查询跟踪方法：后者使用同一查询处理检测与跟踪，存在表示冲突。
- **TransTrack**（Sun et al., arXiv 2020）：虽采用解耦查询，但使用不可微的IoU匹配，而 DQTrack 实现了完全可微的关联。

### 5. 知识库定位

DQTrack 在3D多目标跟踪知识体系中贡献了以下增量：

- **查询设计**：从单共享查询演进为解耦的对象查询与轨迹查询。
- **关联机制**：从启发式后处理演进为基于外观-运动融合的可学习关联。
- **时序更新**：引入EMA机制对轨迹外观和对象嵌入进行平滑更新，增强时序一致性。

这些设计共同构成了一个紧凑、可微且高性能的端到端3D跟踪框架。

### 3D多目标跟踪的范式瓶颈

基于视觉的3D多目标跟踪旨在从连续的多视角图像序列中持续定位和识别场景中的物体，是自动驾驶感知系统的核心组件。现有方法可归纳为两种主流范式：**tracking-by-detection** 和 **tracking-with-query**，二者各自存在根本性缺陷。

**Tracking-by-detection** 方法（如 **CenterTrack**，Yin et al., CVPR 2021）将检测与跟踪解耦为两个独立阶段：首先在每帧进行目标检测，然后通过启发式匹配规则（如IoU或距离阈值）关联帧间检测框。这种范式虽然简单，但依赖不可微的后处理，使得整个流水线无法端到端优化，检测器无法感知跟踪需求，匹配错误会逐帧累积。

**Tracking-with-query** 方法（如 **MUTR3D**，Zhang et al., CVPR 2022）尝试将跟踪融入端到端的可学习框架中，使用统一的查询（query）同时完成检测和跟踪两个任务。然而，这一设计引入了**表示冲突**（representation conflict）的核心瓶颈：同一个查询嵌入既要编码身份无关的物体检测信息，又要承载身份相关的轨迹关联信息。这两种需求在特征空间中相互拉扯——检测要求对当前观测的精确响应，而跟踪要求跨帧的身份一致性——导致单一查询在两个任务上都难以达到最优。

### 解耦查询的核心动机

Figure 1 清晰地对比了三种范式的差异。Tracking-by-detection（1a）将检测与关联割裂，引入不可微的启发式步骤；Tracking-with-query（1b）虽然实现了端到端学习，但单查询的表示冲突成为性能天花板；本文提出的**解耦查询**（decoupled-query）范式（1c）则从根本上重新设计了查询机制：将单一查询拆分为专门的**对象查询**（object query）和**轨迹查询**（track query），使检测和跟踪各自使用独立的表示空间，从而消除任务间的表示冲突。

这一解耦设计并非简单的查询拆分，而是需要配套解决两个关键问题：**如何建立对象与轨迹之间的可微关联**，以及**如何跨帧更新轨迹表示以保持身份一致性**。这正是DQTrack的核心贡献所在——通过可学习的关联模块和时间更新模块，在保持端到端可微的前提下，让解耦后的查询能够有效协作。

### 现有方法的量化缺口

在nuScenes数据集上，先前方法的性能差距显著。Tracking-by-detection方法受限于启发式匹配的次优性，而单查询方法受困于表示冲突。DQTrack通过解耦查询，在nuScenes验证集上相较单查询方法**SinQuery**（即MUTR3D的跟踪部分）获得**4.0% AMOTA**的绝对提升（Table 3），并在测试集上达到**52.3% AMOTA**，超越所有先前基于学习的方法，比**PF-Track**高出**8.9% AMOTA**（Table 2）。这些量化结果直接验证了表示冲突是限制先前方法性能的关键瓶颈，而解耦查询是针对该瓶颈的有效因果干预。

## 核心方法与创新机理

DQTrack 的核心创新在于**将基于查询的跟踪中单一共享查询解耦为专门的对象查询（Object Query）和轨迹查询（Track Query）**，从而消除检测与跟踪任务之间的表示冲突。这一设计从根本上改变了先前方法的查询范式，并驱动了后续可学习关联与时间更新模块的协同设计。

### 1. 查询解耦：从单查询到双查询

在先前基于查询的跟踪方法（如 **MUTR3D**, Zhang et al., CVPR 2022）中，同一个查询嵌入同时承担“当前帧有哪些物体”（身份无关的检测）和“这些物体与历史轨迹的对应关系”（身份相关的跟踪）两个任务。这种设计导致**表示冲突**：检测需要聚焦于物体的通用外观与位置，而跟踪则需要身份判别性特征，单一嵌入难以同时满足两种需求，最终损害整体性能。

DQTrack 将这一单查询拆分为两个独立的查询：
- **对象查询 $Q_O$**：专注于当前帧的物体检测，生成对象嵌入 $E_O^t$。
- **轨迹查询 $Q_T$**：维护历史轨迹的身份表示，用于跨帧关联。

这一解耦设计（Figure 1c）的因果效应在 Table 3 中得到直接验证：与单查询方法（SinQuery）相比，解耦查询在 nuScenes 验证集上带来 **4.0% AMOTA 和 7.4% mAP** 的显著提升，证明消除表示冲突对检测和跟踪均有实质性收益。

### 2. 可学习关联：替代启发式匹配

传统 tracking-by-detection 方法（如 **CenterTrack**, Yin et al., CVPR 2021）依赖 IoU 或距离等启发式后处理进行数据关联，不可微且难以与检测联合优化。**TransTrack** (Sun et al., arXiv 2020) 虽采用了查询解耦，但仍使用不可微的 IoU 匹配。

DQTrack 设计了**全可微的关联模块**，包含两个关键子设计：
- **嵌入交互（Embedding Interaction）**：通过独立的 FFN 分别处理对象嵌入和轨迹嵌入，促进两类嵌入之间的信息交互，增强身份感知能力。Table 4 消融显示，该模块带来 **0.7% AMOTA** 的提升。
- **查询关联（Query Association）**：融合外观特征（Hadamard 积）和运动特征（L2 距离），通过 MLP 和 Softmax 计算可微的轨迹-对象亲和度矩阵 $P_T^t$（Equation 1）。Table 5 表明，同时使用外观和运动特征比仅用运动特征提升 **1.6% AMOTA**，比仅用外观特征提升 **3.2% AMOTA**，验证了多模态特征融合对关联精度的重要性。

### 3. 时间更新：EMA 机制保持表示一致性

DQTrack 引入基于指数移动平均（EMA）的时间更新策略，从外观和几何两个层面刷新轨迹表示：
- **轨迹查询更新**：通过 EMA 将当前匹配到的对象嵌入融合到轨迹外观查询中（Equation 2），更新速率 $\alpha=0.5$ 时最优（Table 7）。
- **对象嵌入更新**：通过 EMA 融合历史更新嵌入与当前解码器输出（Equation 3），更新速率 $\beta=0.3$ 时最优，相对不更新提升 **1.6% AMOTA** 和 **1.2% mAP**（Table 9）。

这种轻量级的时间更新机制在保持端到端可微性的同时，有效缓解了遮挡和外观变化导致的身份漂移问题。

### 创新总结

DQTrack 的三个 changed slots 构成了一条紧凑的因果链：**查询解耦**消除了任务冲突，为后续模块提供了干净的表示基础；**可学习关联**利用解耦后的专门嵌入实现高精度、可微的轨迹匹配；**EMA 时间更新**则维持了跨帧表示的一致性。三者协同使 DQTrack 在 nuScenes 测试集上达到 **52.3% AMOTA**，超越所有先前学习型跟踪器（Table 2），相比 PF-Track 提升 **8.9% AMOTA**。

DQTrack 的端到端流水线遵循“编码-解码-关联-更新”四阶段结构，其核心设计在于将传统单查询跟踪范式中的共享查询显式解耦为**对象查询（object query）**与**轨迹查询（track query）**，从而消除检测与跟踪任务间的表示冲突。Figure 2 给出了完整的框架概览。

![[assets/figures/papers/paper_list_l18_https_openaccess_thecvf_com_content_ICCV2023_papers_Li_End_to_end_3D_Tra/figures/002_Figure_2.jpg]]
*Figure 2: The framework of DQTrack for 3D object tracking. In particular, input images are first processed with the encoder and transformed to BEV space. Then, the transformer decoder takes the object query, as well as the value from BEV space, and outputs encoded object embedding. In learnable association, we facilitate identity awareness with embedding interaction and fuse appearance with motion embedding, which provides better affinity representation for trajectory association. And the temporal update is designed to refresh track query from appearance and geometry aspects for the next frame*

### 编码与 BEV 转换

多视角输入图像首先经过一个可替换的编码器（如 DETR3D、PETRv2 等，见 Table 1）提取特征，随后转换到统一的鸟瞰图（BEV）空间，得到 BEV 特征 $ \mathbf{X}_{\mathrm{B}}^{t} $。这一步骤将多视角的 2D 信息融合为 3D 空间中的统一表示，为后续的检测与关联提供空间一致性基础。

### 对象嵌入生成

在每一帧 $ t $，Transformer 解码器以**可学习的对象查询** $ \mathbf{Q}_{\mathrm{O}} $ 作为输入，与 BEV 特征 $ \mathbf{X}_{\mathrm{B}}^{t} $ 进行交叉注意力交互，输出对象嵌入 $ \mathbf{E}_{\mathrm{O}}^{t} \in \mathbb{R}^{M \times \omega} $，其中 $ M $ 为检测到的对象数量，$ \omega $ 为嵌入维度。该嵌入同时支撑检测框预测和后续的轨迹关联，是连接检测与跟踪的关键桥梁。

### 可学习关联模块

关联模块是 DQTrack 区别于启发式匹配的核心创新（Figure 3）。其输入包含两部分：来自解码器的**对象嵌入** $ \mathbf{E}_{\mathrm{O}}^{t} $ 和历史累积的**轨迹查询** $ \mathbf{Q}_{\mathrm{T}}^{t} $。模块内部包含两个关键子步骤：

1. **嵌入交互（Embedding Interaction）**：通过独立的 FFN 分别处理对象嵌入和轨迹查询，生成外观嵌入 $ \mathbf{E}_{\mathrm{A}}^{t} $、$ \mathbf{Q}_{\mathrm{A}}^{t} $ 与运动嵌入 $ \mathbf{E}_{\mathrm{M}}^{t} $、$ \mathbf{Q}_{\mathrm{M}}^{t} $，并促使两者之间进行信息交互，增强身份感知能力。
2. **查询关联（Query Association）**：融合外观特征（Hadamard 积）与运动特征（L2 距离），经 MLP 和 softmax 生成可微的亲和度矩阵 $ P_{\mathrm{T}}^{t} $：

$$P_{\mathrm{T}}^{t} = \sigma\big(\mathrm{MLP}(\mathbf{Q}_{\mathrm{A}}^{t} \odot \mathbf{E}_{\mathrm{A}}^{t} + \mathrm{FFN}(\mathrm{L2}(\mathbf{Q}_{\mathrm{M}}^{t}, \mathbf{E}_{\mathrm{M}}^{t})))\big)$$

该矩阵直接表示轨迹与对象间的匹配概率，使得整个关联过程可端到端优化。

### 时间更新模块

时间更新模块（Figure 4）负责将当前帧的关联结果反馈到轨迹状态中，为下一帧提供更新后的查询。更新从两个维度进行：

- **轨迹查询更新**：运动部分通过速度预测进行位置传播（$ \mathbf{Q}_{\mathrm{UM}}^{t} = \mathbf{Q}_{\mathrm{M}}^{t} + \Delta t \times P_{\mathrm{V}}^{t} $），外观部分则使用指数移动平均（EMA）融合匹配到的对象嵌入：

$$\mathbf{Q}_{\mathrm{UA}}^{t} = \alpha \times \mathbf{Q}_{\mathrm{A}}^{t} + (1 - \alpha) \times \mathbf{E}_{\mathrm{T}}^{t}[H_{\mathrm{T}}^{t}]$$

- **对象嵌入更新**：为增强时序一致性，对象嵌入同样采用 EMA 机制，融合上一帧的更新嵌入与当前解码器输出：

$$\mathbf{E}_{\mathrm{U}}^{t} = \beta \times \mathbf{E}_{\mathrm{U}}^{t-1} + (1 - \beta) \times \mathbf{E}_{\mathrm{O}}^{t}$$

更新后的轨迹查询 $ \mathbf{Q}_{\mathrm{T}}^{t+1} $ 由更新后的外观和运动查询拼接而成，同时根据匈牙利匹配结果进行新轨迹的初始化与缺失轨迹的移除（阈值 $ \delta = 7 $），形成闭环的时序推理。

### 优化目标

整个流水线在 $ D $ 帧序列上联合优化，总损失为检测损失、跟踪交叉熵损失与最大熵正则化损失的加权和：

$$\mathcal{L} = \sum_{t}^{D} (\lambda_{\mathrm{Det}} \mathcal{L}_{\mathrm{Det}}^{t} + \lambda_{\mathrm{Track}} \mathcal{L}_{\mathrm{Track}}^{t} + \lambda_{\mathrm{Reg}} \mathcal{L}_{\mathrm{Reg}}^{t})$$

这种端到端的训练方式使得检测器、关联模块和时间更新模块能够协同优化，避免了传统 tracking-by-detection 方法中检测与关联分离带来的次优性问题。

DQTrack 的端到端可微跟踪流水线由三个核心模块构成：**可学习关联**、**时间更新** 和 **整体优化目标**。以下逐一展开其关键公式与变量含义。

---

### 可学习关联

可学习关联模块的目标是生成轨迹与当前帧检测对象之间的可微亲和度矩阵 $P_{\mathrm{T}}^{t}$，以替代传统 IoU 匹配或匈牙利算法的启发式后处理。该模块包含两个子步骤：**嵌入交互** 和 **查询关联**。

**嵌入交互** 将轨迹查询 $\mathbf{Q}_{\mathrm{T}}^{t}$ 与对象嵌入 $\mathbf{E}_{\mathrm{O}}^{t}$ 分别送入独立的 FFN，生成外观嵌入 $\mathbf{Q}_{\mathrm{A}}^{t}, \mathbf{E}_{\mathrm{A}}^{t}$ 和运动嵌入 $\mathbf{Q}_{\mathrm{M}}^{t}, \mathbf{E}_{\mathrm{M}}^{t}$，并通过交互操作增强身份判别力（见 Figure 3）。

**查询关联** 融合外观和运动特征，预测亲和度矩阵：

$$P_{\mathrm{T}}^{t} = \sigma\big(\mathrm{MLP}(\mathbf{Q}_{\mathrm{A}}^{t} \odot \mathbf{E}_{\mathrm{A}}^{t} + \mathrm{FFN}(\mathrm{L2}(\mathbf{Q}_{\mathrm{M}}^{t}, \mathbf{E}_{\mathrm{M}}^{t})))\big) \tag{1}$$

变量含义：
- $\mathbf{Q}_{\mathrm{A}}^{t} \in \mathbb{R}^{N \times C}$：$N$ 条轨迹的外观查询嵌入
- $\mathbf{E}_{\mathrm{A}}^{t} \in \mathbb{R}^{M \times C}$：$M$ 个检测对象的外观嵌入
- $\odot$：逐元素乘积（Hadamard product），捕获外观相似性
- $\mathbf{Q}_{\mathrm{M}}^{t}, \mathbf{E}_{\mathrm{M}}^{t}$：运动嵌入，通过 L2 距离度量位置差异
- $\mathrm{FFN}$：前馈网络，将 L2 距离映射为标量相似度
- $\mathrm{MLP}$：多层感知机，融合外观与运动特征
- $\sigma$：沿轨迹维度的 softmax，输出 $P_{\mathrm{T}}^{t} \in [0,1]^{N \times M}$

**消融证据**：Table 5 显示，同时使用外观和运动特征比仅用运动特征提升 **1.6% AMOTA**，比仅用外观特征提升 **3.2% AMOTA**，验证了双流融合设计的必要性。

---

### 时间更新

时间更新模块负责将匹配后的轨迹表示传播到下一帧，包含**轨迹查询更新**和**对象嵌入更新**两条路径（见 Figure 4）。

**轨迹查询更新** 分为外观更新和运动更新。外观更新采用指数移动平均（EMA），根据匈牙利匹配结果 $H_{\mathrm{T}}^{t}$ 融合当前对象嵌入：

$$\mathbf{Q}_{\mathrm{UA}}^{t} = \alpha \times \mathbf{Q}_{\mathrm{A}}^{t} + (1 - \alpha) \times \mathbf{E}_{\mathrm{T}}^{t}[H_{\mathrm{T}}^{t}] \tag{2}$$

其中 $\mathbf{E}_{\mathrm{T}}^{t}[H_{\mathrm{T}}^{t}]$ 表示根据匹配索引从对象嵌入中选取的对应嵌入，$\alpha$ 为更新速率。运动更新则基于匀速假设，将预测速度乘以时间间隔叠加到当前运动查询：$\mathbf{Q}_{\mathrm{UM}}^{t} = \mathbf{Q}_{\mathrm{M}}^{t} + \Delta t \times \mathbf{P}_{\mathrm{V}}^{t}$。

**对象嵌入更新** 同样采用 EMA，融合上一帧的更新嵌入与当前帧解码器输出：

$$\mathbf{E}_{\mathrm{U}}^{t} = \beta \times \mathbf{E}_{\mathrm{U}}^{t-1} + (1 - \beta) \times \mathbf{E}_{\mathrm{O}}^{t} \tag{3}$$

其中 $\beta$ 控制历史信息的保留程度。

**消融证据**：Table 7 显示 $\alpha = 0.5$ 时最优，相对不更新提升 **1.1% AMOTA**；Table 9 显示 $\beta = 0.3$ 时最优，相对不更新提升 **1.6% AMOTA** 和 **1.2% mAP**。这证实了 EMA 机制在平滑表示、增强关联鲁棒性方面的关键作用。

---

### 整体优化目标

DQTrack 在连续 $D$ 帧上进行端到端训练，总损失为各帧检测损失、跟踪损失和正则化损失的加权和：

$$\mathcal{L} = \sum_{t}^{D} (\lambda_{\mathrm{Det}} \mathcal{L}_{\mathrm{Det}}^{t} + \lambda_{\mathrm{Track}} \mathcal{L}_{\mathrm{Track}}^{t} + \lambda_{\mathrm{Reg}} \mathcal{L}_{\mathrm{Reg}}^{t}) \tag{4}$$

其中：
- $\mathcal{L}_{\mathrm{Det}}^{t}$：标准检测损失（分类 + 回归）
- $\mathcal{L}_{\mathrm{Track}}^{t} = \mathrm{CE}(P_{\mathrm{T}}^{t}, Y_{\mathrm{T}}^{t})$：交叉熵跟踪损失，$Y_{\mathrm{T}}^{t}$ 为身份对应真值
- $\mathcal{L}_{\mathrm{Reg}}^{t}$：最大熵正则化，防止关联矩阵过于尖锐，提升泛化性

**消融证据**：Table 8 显示，轨迹查询增强带来 **0.4% AMOTA** 提升，熵正则化进一步贡献 **0.6% AMOTA**；Table 10 显示使用 3 帧训练（$D=3$）获得最佳 **28.5% AMOTA**，显著优于 2 帧或 4 帧。

## 实验与关键发现

### 核心性能：在nuScenes测试集与验证集上的SOTA表现

DQTrack在nuScenes测试集上达到了**52.3% AMOTA**，显著超越了当时所有基于学习的相机3D跟踪器（Table 2）。与之前最强的学习型方法PF-Track（43.4% AMOTA）相比，DQTrack的绝对提升高达**+8.9% AMOTA**，这一优势是在不使用NMS或测试时增强等后处理技巧的端到端方式下取得的，体现了方法本身的设计有效性。

![[assets/figures/papers/paper_list_l18_https_openaccess_thecvf_com_content_ICCV2023_papers_Li_End_to_end_3D_Tra/figures/006_Table_2.jpg]]
*Table 2: Comparisons with leading camera-based methods on the nuScenes test set. We evaluate our model in an end-to-end manner without bells-and-whistles like NMS or test-time augmentation, which could bring potential improvement*

在nuScenes验证集上，DQTrack同样展现出强竞争力（Table 1）。使用简单的立体视觉解码器时，DQTrack达到28.5% AMOTA；当编码器升级为PETRv2（V2-99骨干），性能跃升至**44.6% AMOTA**，同时检测指标mAP达到45.0%，NDS达到54.5%。值得注意的是，这一配置下的IDS（身份切换次数）仅为**885**，远低于MUTR3D*的2060，表明解耦查询设计对长期身份保持的实质性帮助。推理速度方面，DQTrack在单张A100 GPU上达到**15.1 FPS**，在精度与效率之间取得了良好平衡。

![[assets/figures/papers/paper_list_l18_https_openaccess_thecvf_com_content_ICCV2023_papers_Li_End_to_end_3D_Tra/figures/005_Table_1.jpg]]
*Table 1: Comparisons with previous methods on the nuScenes val set. We report results with traditional work [31, 19, 21] and the simple stereo-based decoder. TBD and Geo represent the tracking-by-detection manner and the geometry-based matching in [38]. FPS is evaluated in a single NVIDIA A100 GPU from input images to tracking results. * denotes results from [41]*

### 范式对比消融：解耦查询 vs. 单查询 vs. TBD

Table 3的范式对比消融直接验证了论文的核心主张。在nuScenes验证集上，使用相同骨干的条件下：

- **Tracking-by-detection**（TBD，基于[38]）：24.1% AMOTA，24.0% mAP
- **单查询方法**（SinQuery，基于[41]）：24.5% AMOTA，28.2% mAP
- **DQTrack（解耦查询）**：**28.5% AMOTA**，**35.6% mAP**

解耦查询相比单查询带来**+4.0% AMOTA**和**+7.4% mAP**的提升。这一结果清晰地表明：单查询中检测与跟踪任务的表示冲突确实损害了性能，而将对象查询与轨迹查询解耦后，两个子任务各自获得了更优的表示空间，同时提升了检测精度和关联质量。

### 可学习关联模块的消融分析

**嵌入交互的有效性**（Table 4）：在查询关联前引入嵌入交互（Embedding Interaction）模块，使轨迹查询与对象嵌入进行信息交互，带来**+0.7% AMOTA**的提升（从27.8%到28.5%）。这表明嵌入交互有助于缩小轨迹与当前观测之间的表示鸿沟，为后续的亲和度计算提供了更具判别力的特征。

**外观与运动特征的互补性**（Table 5）：查询关联模块可以仅使用外观特征、仅使用运动特征，或融合两者。实验结果显示：

- 仅运动特征：26.9% AMOTA
- 仅外观特征：25.3% AMOTA
- **融合外观+运动：28.5% AMOTA**

融合方案比仅用运动特征提升**+1.6% AMOTA**，比仅用外观特征提升**+3.2% AMOTA**。这一结果表明，外观特征（Hadamard积交互）和运动特征（L2距离）在关联决策中具有互补作用：运动特征提供几何一致性约束，外观特征提供语义身份线索，二者融合才能达到最优匹配精度。

**对象嵌入来源的影响**（Table 6）：对象嵌入 $\mathbf{E}_{\mathrm{O}}^{t}$ 可以来自Transformer解码器输出，也可直接取自BEV特征。使用解码器输出比直接使用BEV特征提升**+2.1% AMOTA**和**+1.4% NDS**。解码器通过交叉注意力机制已从BEV空间中提取了与对象查询高度相关的特征，这种经过筛选的表示更适合后续的关联与跟踪。

### 时间更新模块的消融分析

**轨迹查询更新速率 $\alpha$**（Table 7）：公式(2)中的EMA更新速率 $\alpha$ 控制轨迹外观查询对历史表示与当前观测的依赖程度。$\alpha=0.5$ 时达到最优AMOTA 28.5%，相比不使用时间更新（$\alpha=0$，即完全依赖当前观测）提升**+1.1% AMOTA**。$\alpha$ 过大（接近1.0）或过小（接近0.0）均导致性能下降，说明平衡历史平滑与当前响应对于保持轨迹表示质量至关重要。

**对象嵌入更新速率 $\beta$**（Table 9）：公式(3)中的 $\beta$ 控制对象嵌入在时间上的平滑程度。$\beta=0.3$ 时最优，相比不更新（$\beta=0$）提升**+1.6% AMOTA**和**+1.2% mAP**。这一提升幅度大于轨迹查询更新的贡献，说明在对象侧进行时间平滑同样重要——它使得关联模块接收到的对象表示更加稳定，减少了因单帧噪声导致的误匹配。

### 训练策略消融

**轨迹查询增强与熵正则化**（Table 8）：训练时向轨迹查询中添加假阳性查询（aug）模拟遮挡/误检场景，带来**+0.4% AMOTA**提升。进一步施加最大熵正则化（reg），防止关联矩阵过拟合到确定性匹配，额外提升**+0.6% AMOTA**。两项策略合计贡献约+1.0% AMOTA，验证了它们在提升关联鲁棒性方面的作用。

**训练帧数 $D$**（Table 10）：使用3帧训练达到最优28.5% AMOTA，优于2帧（27.3%）和4帧（27.4%）。2帧不足以学习充分的时序模式，而4帧可能引入过长的时间跨度，增加了优化难度或引入了不相关的历史信息。3帧在时序上下文丰富性与训练稳定性之间取得了最佳平衡。

### 主要失败模式与局限

1. **嵌入更新模块的泛化限制**：当前的对象嵌入EMA更新仅在基于立体视觉的编码器上验证有效（Table 9），尚未扩展到DETR3D、PETRv2等更先进的预训练模型。这一模块能否在不同编码器架构上一致受益，需要进一步验证。

![[assets/figures/papers/paper_list_l18_https_openaccess_thecvf_com_content_ICCV2023_papers_Li_End_to_end_3D_Tra/figures/012_Table_9.jpg]]
*Table 9: Results with different rates for embedding update on the nuScenes val set. $\beta$ denotes the rate in Equation (3)*

2. **遮挡场景的鲁棒性不足**：模型对严重遮挡的应对主要依赖训练时的假阳性查询增强（Table 8），这是一种模拟策略。在真实的高动态、高遮挡场景中，模型的关联失败率和身份切换可能显著上升，但缺乏专门的实验评估。

![[assets/figures/papers/paper_list_l18_https_openaccess_thecvf_com_content_ICCV2023_papers_Li_End_to_end_3D_Tra/figures/013_Table_8.jpg]]
*Table 8: Results with different optimization strategies. aug and reg indicate query augmentation and entropy regulation*

3. **轨迹生命周期管理的启发式依赖**：轨迹的出生（$\tau=0.2$）、匹配（$\mu=0.1$）和终止（$\delta=7$）阈值均为人工设定（Algorithm 1）。这些超参数在不同场景密度和运动模式下可能不是最优的，缺乏自适应的生命周期管理机制。

4. **运动模型的简化假设**：轨迹位置更新基于匀速运动假设（$\mathbf{Q}_{\mathrm{UM}}^{t} = \mathbf{Q}_{\mathrm{M}}^{t} + \Delta t \times \mathbf{P}_{\mathrm{V}}^{t}$），在急转弯或加减速场景下可能产生较大的运动预测误差，进而影响关联精度。

![[assets/figures/papers/paper_list_l18_https_openaccess_thecvf_com_content_ICCV2023_papers_Li_End_to_end_3D_Tra/figures/007_Table_3.jpg]]
*Table 3: Results with different trackers on the nuScenes val set. TBD denotes the tracking-by-detection method in [38]. SinQuery indicates the single-query approach in [41]*


## 定位与知识库关联

### 1. 在3D多目标跟踪范式中的位置

DQTrack的核心贡献在于对“基于查询的跟踪”范式的继承与重构。其方法谱系可沿两条主线追溯：

- **从“检测后跟踪”到“联合检测跟踪”**：早期工作如 **CenterTrack** (Yin et al., CVPR 2021) 将跟踪简化为基于距离的贪婪匹配，依赖启发式后处理。DQTrack通过可学习的关联模块消除了这一手工设计瓶颈，使关联过程完全可微。

- **从“单查询”到“解耦查询”**：**MUTR3D** (Zhang et al., CVPR 2022) 首次将检测与跟踪统一到Transformer查询框架中，但使用同一查询同时处理身份无关的检测和身份相关的跟踪，导致表示冲突。DQTrack的直接前身可追溯至 **TransTrack** (Sun et al., arXiv 2020)，后者虽采用了检测查询与轨迹查询的分离设计，但其关联仍依赖不可微的IoU匹配。DQTrack将解耦查询与可学习关联结合，首次在端到端流水线中同时消除表示冲突和手工匹配。

### 2. 与同期/后续工作的关系

DQTrack发表于ICCV 2023，其解耦查询设计为后续工作提供了可复用的架构模板。在nuScenes测试集上，DQTrack以52.3% AMOTA超越所有先前学习型跟踪器，例如比PF-Track高8.9% AMOTA（Table 2）。这一性能差距表明，解耦查询相较于单查询或纯检测后匹配具有结构性优势。

在编码器兼容性方面，DQTrack在立体视觉解码器、DETR3D解码器和PETRv2解码器上均进行了验证（Table 1），展示了方法对主流BEV感知骨干的即插即用能力。这使其区别于许多仅针对单一编码器设计的跟踪方法。

### 3. 适用边界与局限

尽管DQTrack在nuScenes基准上表现优异，其适用边界和已知局限如下：

1. **嵌入更新模块的编码器泛化受限**：对象嵌入的EMA更新（Equation 3）仅在基于立体视觉的编码器上进行了验证，尚未扩展到DETR3D或PETRv2等预训练模型，限制了该模块的通用性。

2. **轨迹生命周期管理依赖人工阈值**：轨迹的出生、匹配和终止仍依赖预设阈值（如缺失帧阈值δ=7），缺乏自适应的生命周期管理机制。在严重遮挡或目标频繁进出视野的场景下，固定阈值可能导致身份切换增加或轨迹碎片化。

3. **运动模型的简化假设**：轨迹位置更新基于匀速运动假设（Δ_t × P_V^t），在高度动态或非线性运动场景（如急转弯、突然加减速）下可能产生定位偏差。

4. **训练帧数的敏感依赖**：消融实验（Table 10）显示，使用3帧训练最优，2帧或4帧均导致性能下降，表明模型对时间窗口长度较为敏感，可能需要针对不同场景重新调参。

### 4. 开放问题

以下问题在论文中未被充分回答，构成未来研究方向：

- **密集场景下的关联精度**：可学习关联模块在极速运动或大量轨迹同时存在时的计算开销和匹配精度如何？当前实验主要在nuScenes相对稀疏的交通场景下进行，未在更拥挤环境（如行人密集区）中验证。

- **跨模态扩展**：DQTrack能否直接扩展到激光雷达点云的3D跟踪中？解耦查询和可学习关联的架构是否对模态敏感，仍需验证。

- **运动模型升级**：是否有更优的运动模型（如基于学习的运动预测或卡尔曼滤波的端到端版本）替代当前的匀速假设，以进一步提升定位精度？

- **真实遮挡场景的鲁棒性**：模型在严重遮挡下的鲁棒性仅通过训练时的假阳性查询增强模拟，缺乏真实遮挡场景下的详尽评估和针对性设计。

## 原文 PDF

![[paperPDFs/ICCV_2023/End_to_end_3D_Tracking_with_Decoupled_Queries.pdf]]
