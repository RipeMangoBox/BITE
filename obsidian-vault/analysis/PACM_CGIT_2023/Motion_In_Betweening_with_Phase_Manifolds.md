---
title: "Motion In-Betweening with Phase Manifolds"
type: paper
paper_level: A
venue: "PACM CGIT"
year: 2023
pdf_ref: paperPDFs/PACM_CGIT_2023/Motion_In_Betweening_with_Phase_Manifolds.pdf
aliases:
- MBPM
tags:
- PACM_CGIT_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "引入基于学习相位的流形（通过Periodic Autoencoder提取）作为控制信号，编码了运动的周期性结构，从而在时间上引导生成过程，大幅改善长时程泛化并减少歧义。"
primary_logic: "运动的周期性可以用学习到的相位变量表示，将这些相位输入到混合专家（MoE）网络中，可以有效地在时间和空间上聚类运动，允许网络在自回归生成过程中利用这种时间结构来合成更锐利、更连贯的过渡。"
claims:
- "在极端压力测试（10米距离，2秒内到达）中，使用学习相位的模型能够生成自然的跳跃动作，而其他基线出现漂移或脚部滑动。"
- "在LaFAN1测试集上，本文方法在30-120帧的不同过渡长度上的平均L2P误差（3.32）均优于RTN（3.93）和插值基线（6.56），尤其在120帧外推时优势明显（Ours 3.89 vs RTN 5.59）。"
- "消融实验证实，省略相位或使用手动接触相位会导致运动生动性（平均关节旋转/秒）显著下降，且脚部接触稳定性变差。"
- "双向控制方案显著降低了目标到达误差：步行任务位置误差从21.59 cm降至9.61 cm，旋转误差从18.94°降至11.23°。"
---

# Motion In-Betweening with Phase Manifolds

> [!tip] 核心洞察
> 运动的周期性可以用学习到的相位变量表示，将这些相位输入到混合专家（MoE）网络中，可以有效地在时间和空间上聚类运动，允许网络在自回归生成过程中利用这种时间结构来合成更锐利、更连贯的过渡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于相位流形的运动插值 |
| 英文题名 | Motion In-Betweening with Phase Manifolds |
| 会议/期刊 | PACM CGIT 2023 |
| Links | [paper](https://doi.org/10.1145/3606921) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | Motion In-Betweening with Phase Manifolds |
| Dataset | LaFAN1 (Subject 5 test set), Quadruped dataset [Zhang et al. 2018] |

> [!tip] 效果简介
> - LaFAN1 (Subject 5 test set) 上，L2P (average over 30-120 frames) 为 3.32，对比 RTN: 3.93，变化 -0.61 (lower is better)。
> - LaFAN1 (Subject 5 test set) 上，L2P (average over 30-120 frames) 为 3.32，对比 Interpolation: 6.56，变化 -3.24。
> - Quadruped dataset [Zhang et al. 2018] 上，L2P @60 frames (1 second) 为 0.51，对比 Interpolation: 1.26，变化 -0.75。

## 概述

运动插值（Motion In-Betweening）旨在给定起始与目标关键帧的条件下，自动生成中间过渡姿态序列。现有方法在短过渡时长上表现尚可，但当过渡时间延长时，由于时间信息的模糊性，生成的运动往往趋于平滑、缺乏细节，甚至出现不自然的漂移或脚部滑动。其根本瓶颈在于缺乏有效的时间表示来引导生成过程并保持时间相干性。

本文提出**基于相位流形的运动插值**方法，核心思路是利用运动的周期性结构作为控制信号。具体而言，系统通过一个**Periodic Autoencoder**从运动捕捉数据中无监督地学习相位流形，将运动在时间维度上的周期性编码为振幅与相位变量。这些相位变量被送入一个**混合专家（Mixture-of-Experts, MoE）网络**——包含门控网络与运动预测网络——在空间和时间上对运动进行聚类，从而在自回归生成过程中利用时间结构合成更锐利、更连贯的过渡。

主要结论如下：

- **长时程泛化能力显著提升**：在LaFAN1测试集上，本文方法在30-120帧的不同过渡长度上平均L2P误差为3.32，优于强神经基线**RTN**（Harvey et al., TOG 2020）的3.93和简单插值基线的6.56。尤其在120帧外推场景下，本文方法L2P仅3.89，而RTN升至5.59，证明相位流形提供了有效的时间外推能力（Table 3）。
- **极端压力测试下生成自然动作**：在目标帧距离起始帧10米、需在2秒内到达的极端条件下，使用学习相位的模型能够生成自然的跳跃动作，而其他基线出现漂移或脚部滑动（Fig. 7）。
- **消融实验验证相位与双向控制的关键作用**：省略相位或使用手动接触相位会导致运动生动性（平均关节旋转/秒）显著下降，脚部接触稳定性变差（Table 1, Fig. 6）；双向控制方案将目标到达误差大幅降低——步行任务位置误差从21.59 cm降至9.61 cm，旋转误差从18.94°降至11.23°（Table 2）。
- **跨形态泛化**：在四足动物数据集上，本文方法在60帧过渡长度上L2P为0.51，优于插值基线（1.26）和Transformer基线（0.63）（Table 6）。

在方法谱系上，本文继承了混合专家运动控制框架，但通过引入学习到的相位流形作为时间先验，将运动插值从“纯空间插值”提升为“时间结构引导的生成”。相比RTN等基于全连接网络的确定性预测方法，本文的MoE结构与相位条件化机制在长时间过渡上展现出更强的鲁棒性与运动质量。

## 背景与动机

运动插值（Motion In-Betweening）是角色动画中的核心任务：给定起始姿态和目标姿态，以及期望的过渡时长，生成中间帧序列，使角色自然地从起始状态过渡到目标状态。这一技术在游戏、影视和虚拟现实中有广泛应用，能够显著减少动画师手动关键帧的工作量。

现有方法面临的核心瓶颈在于**时间信息模糊性**。当过渡时间较长时，仅依赖起始和目标两帧的空间信息不足以唯一确定中间的运动模式——角色可以选择步行、奔跑、跳跃等多种方式到达目标，而缺乏有效的时间结构引导会导致网络生成平滑但缺乏细节的“平均”运动，表现为动作模糊、脚步滑动、运动生动性下降。这一问题在极端过渡条件下（如长距离、短时间）尤为突出，现有方法往往产生漂移或物理上不合理的姿态。

以主流神经基线 **RTN**（Harvey et al., TOG 2020）为例，该方法采用自回归生成框架，但在超过训练窗口长度（如120帧）时性能显著退化，L2P误差从短过渡的较好水平上升至5.59，表明其时间外推能力有限。简单的线性/球面插值基线则完全忽略了运动动力学，在30-120帧范围内的平均L2P误差高达6.56，生成的运动缺乏任何生物力学合理性。

本文的动机正是针对上述时间信息缺失问题，探索一种能够**编码运动周期性结构**的表示方法，将其作为控制信号注入生成过程，从而在自回归框架中保持时间相干性。核心假设是：运动的周期性（如步态循环、跳跃节奏）可以用低维相位变量有效表征，这些相位不仅能够区分不同运动模式，还能在时间维度上提供稳定的引导，使网络在长时程生成中保持锐利、连贯的运动细节。

## 核心创新

本文的核心创新在于通过**学习到的相位流形（Phase Manifolds）**为运动插值任务引入了有效的时间表示，解决了现有方法在长过渡时间下因时间信息模糊而导致的运动平滑、不自然问题。这一创新通过三个关键的技术槽位变更实现，并与基线方法形成鲜明对比。

**相位特征的引入（核心因果旋钮）**  
现有方法（如**RTN** Harvey et al., TOG 2020）或简单插值基线缺乏有效的时间引导信号，仅依赖帧间姿态信息进行预测，导致在长时程生成中出现漂移和细节丢失。本文方法引入由**Periodic Autoencoder**从运动捕捉数据中无监督提取的相位流形 $\mathcal{P}_i = A_i \cdot \begin{pmatrix} \sin \Theta_i \\ \cos \Theta_i \end{pmatrix}$，将运动的周期性结构编码为振幅 $A_i$ 和相位 $\Theta_i$ 的组合。这一相位特征作为控制信号输入网络，在时间和空间上聚类运动模式，使模型在自回归生成过程中能够保持时间相干性。消融实验证实，使用学习相位相比无相位或手动接触相位，显著提升了运动生动性（平均关节旋转/秒）并减少了脚部滑动（Table 1, Fig. 6）。在极端压力测试（10米距离，2秒内到达）中，仅学习相位模型能生成自然的跳跃动作，而其他设置出现漂移或滑动（Fig. 7）。

**混合专家（MoE）架构的适配**  
基线方法通常采用标准全连接网络进行预测。本文采用MoE结构，由门控网络（Gating Network）根据输入的相位特征动态计算8个专家权重，生成运动预测网络（Motion Prediction Network）的参数。这一设计使网络能够根据当前运动相位自适应地组合不同的运动模式，而非使用固定参数处理所有运动类型。门控网络与相位特征的耦合是产生锐利、连贯过渡的关键机制（Fig. 2, Section 3）。

**双向控制方案**  
传统方法仅从角色自身坐标系（自我中心）或目标坐标系（目标中心）进行单向预测，难以精确到达目标姿态。本文提出双向控制方案，同时预测自我中心和目标中心的姿态与轨迹，并通过时间驱动的混合参数 $\lambda$ 进行平滑过渡：$(1-\lambda) \mathrm{Y}_{i+1}^{S} + \lambda T_{i+1} \mathrm{Y}_{i+1}^{\hat{S}}$。这一设计使角色在过渡过程中自然逼近目标帧。消融实验表明，双向控制将步行任务的位置误差从21.59 cm降至9.61 cm，旋转误差从18.94°降至11.23°（Table 2），显著提升了目标到达精度。

**辅助输出与控制约束**  
相比仅预测下一帧姿态的基线，本文网络额外预测未来1秒内的相位更新（频率和振幅）、脚部接触标签，并通过逆运动学（IK）后处理修正末端效应器位置以减少滑动伪影。此外，模型支持通过单热动作标签控制运动风格（如强制爬行而非步行，Fig. 8），以及通过轨迹混合参数 $\tau$ 控制角色沿用户指定路径运动（$T = \mathcal{I}(T^{*}, T^{+}, \tau)$），提升了系统的可控性和实用价值（Table 4）。

这些创新共同使本文方法在LaFAN1测试集上取得了显著优于RTN和插值基线的性能，尤其在120帧外推场景下优势明显（L2P 3.89 vs RTN 5.59, Table 3），证明了相位流形提供的时间结构对长时程泛化的关键作用。

## 整体框架

![[assets/figures/papers/paper_list_l42_https_doi_org_10_1145_3606921/figures/016_Figure_10.jpg]]
*Figure 10: Sequences of keyframes along artificial paths (left) created with the authoring tool (right). Fig. 11. Generated in-between motion sequences of a quadruped character between target frames using the proposed framework and authoring tool*

![[assets/figures/papers/paper_list_l42_https_doi_org_10_1145_3606921/figures/002_Figure_2.jpg]]
*Figure 2: The architecture of the system is composed of the gating network and the motion prediction network. The gating network takes as input the phase segments that are learned by the Periodic Autoencoder and computes the blending coefficients to generate the motion prediction network. The motion prediction network takes as input the current pose, trajectory, contacts and the control variables of the target frame to predict the motion in the next frame*

本文提出的运动插值系统采用**混合专家（Mixture-of-Experts, MoE）**架构，由两个核心网络模块构成：**门控网络（Gating Network）** 和 **运动预测网络（Motion Prediction Network）**，如图 Figure 2 所示。系统以自回归方式逐帧生成从起始关键帧到目标关键帧的过渡运动。

### 核心机制：相位流形引导的混合专家

系统的关键设计在于利用**学习到的相位流形**作为时间控制信号来驱动整个生成过程。具体而言：

- **相位流形**由预训练的 Periodic Autoencoder 从运动捕捉数据中无监督提取，编码了运动的周期性结构信息。每个时间窗口的相位流形 $\mathcal{P}_i$ 由振幅 $A_i$ 和相位 $\Theta_i$ 计算得到：
  $$\mathcal{P}_i = A_i \cdot \begin{pmatrix} \sin \Theta_i \\ \cos \Theta_i \end{pmatrix}$$

- **门控网络**接收这些相位片段作为输入，计算 8 个专家权重的混合系数。相位信息使得网络能够按照运动的时间和空间特征对运动进行聚类，不同的专家权重自然对应不同的运动阶段和类型。

- **运动预测网络**是一个 3 层全连接网络，其参数由门控网络动态生成。该网络接收当前帧的完整状态（角色姿态、根轨迹、接触信息及目标帧控制变量），在专家权重的指导下预测下一帧的运动状态。

### 双向控制方案

为确保角色能精确到达目标姿态，系统采用**双向控制方案（Bi-directional Control Scheme）**，如 Figure 9 所示。在每一帧预测中，网络同时生成两种预测：

- **自我中心预测**（$\mathrm{Y}_{i+1}^{S}$）：相对于角色自身坐标系
- **目标中心预测**（$\mathrm{Y}_{i+1}^{\hat{S}}$）：相对于目标帧坐标系

两者通过时间驱动的混合参数 $\lambda$ 进行融合：
$$(1-\lambda) \mathrm{Y}_{i+1}^{S} + \lambda T_{i+1} \mathrm{Y}_{i+1}^{\hat{S}}$$
其中 $T_{i+1}$ 为坐标变换矩阵。$\lambda$ 随时间从 0 平滑过渡到 1，使得角色在过渡初期保持自身运动特性，后期逐渐向目标姿态对齐。消融实验证实，该方案将步行任务的位置误差从 21.59 cm 降至 9.61 cm，旋转误差从 18.94° 降至 11.23°（Table 2）。

### 输入输出流

系统在帧 $i$ 的完整输入向量 $X_i$ 包含五个组成部分：
$$X_i = \{ X_i^{\mathcal{R}}, X_i^S, X_i^{\mathcal{T}}, X_i^C, X_i^{\mathcal{P}} \}$$
分别为根轨迹、角色状态、目标状态、接触标签和运动相位。

输出向量 $Y_{i+1}$ 包含下一帧的预测信息：
$$Y_{i+1} = \{ Y_{i+1}^R, Y_{i+1}^{\hat{R}}, Y_{i+1}^S, Y_{i+1}^{\hat{S}}, Y_{i+1}^C, Y_{i+1}^{\mathcal{P}} \}$$
涵盖未来根轨迹、预测姿态、接触标签以及未来 1 秒内的相位更新（频率和振幅）。

### 后处理与可选控制

- **逆运动学（IK）后处理**：利用预测的脚部接触标签对末端效应器执行 IK 修正，减少脚部滑动伪影。
- **轨迹混合控制**：用户可通过参数 $\tau$ 将期望轨迹 $T^*$ 与模型预测轨迹 $T^+$ 混合（$T = \mathcal{I}(T^*, T^+, \tau)$），实现沿人工路径的运动控制。
- **动作风格约束**：通过额外的单热动作标签，用户可在运行时指定期望的运动风格（如强制爬行而非步行）。

整个框架以端到端方式训练，Phase Autoencoder 作为预处理阶段独立训练。训练数据来自 LaFAN1 数据集（64 个序列，约 399,139 帧，30 fps），使用 Subject 1-4 训练、Subject 5 测试的标准分割。

## 核心模块与公式推导

### 2.1 系统架构概述

本文系统采用混合专家（Mixture-of-Experts, MoE）架构，由门控网络和运动预测网络两个核心模块组成（Fig. 2）。门控网络接收由Periodic Autoencoder预提取的相位片段作为输入，动态计算8个专家权重混合系数，用于生成运动预测网络的参数。运动预测网络则接收当前姿态、轨迹、接触信息和目标帧控制变量，在专家权重指导下自回归地预测下一帧的运动状态。整个系统以端到端方式训练，使用从运动捕捉数据中提取的相位信息和姿态数据。

### 2.2 相位流形模块

相位流形是本文的核心技术创新，用于编码运动的周期性时间结构。给定由Periodic Autoencoder从运动数据中无监督提取的振幅 $A_i$ 和相位 $\Theta_i$，相位流形通过以下公式计算：

$$\mathcal{P}_i = A_i \cdot \begin{pmatrix} \sin \Theta_i \\ \cos \Theta_i \end{pmatrix}$$

**变量含义**：
- $\mathcal{P}_i$：第 $i$ 帧的相位流形向量，将一维相位映射到二维流形空间
- $A_i$：振幅通道，控制相位流形的幅度，反映运动的强度特征
- $\Theta_i$：相位值，编码运动在周期中的时间位置

该公式将一维相位值 $\Theta_i$ 通过正弦和余弦函数映射到二维单位圆上，再乘以振幅 $A_i$ 进行缩放。这种表示使得不同运动类型的周期性结构能够在统一的流形空间中被刻画和区分（Fig. 3），为门控网络提供时间聚类的依据。相位流形作为控制信号输入门控网络，使网络能够在自回归生成过程中保持时间相干性，从而在长过渡时间下仍能合成锐利、连贯的运动。

### 2.3 双向控制方案

为提升目标姿态的到达精度，系统采用双向控制方案，同时从自我中心空间和目标中心空间进行预测，并通过时间驱动的混合参数进行融合（Fig. 9）。混合公式为：

$$(1-\lambda) \mathrm{Y}_{i+1}^{S} + \lambda T_{i+1} \mathrm{Y}_{i+1}^{\hat{S}}$$

**变量含义**：
- $\mathrm{Y}_{i+1}^{S}$：在自我中心空间 $S$（以角色当前根节点为参考系）中预测的下一帧状态
- $\mathrm{Y}_{i+1}^{\hat{S}}$：在目标中心空间 $\hat{S}$（以目标帧根节点为参考系）中预测的下一帧状态
- $T_{i+1}$：坐标变换矩阵，将目标中心空间的预测映射回自我中心空间
- $\lambda$：时间驱动的混合参数，在过渡过程中从0逐渐增加到1，使角色自然逼近目标帧

该方案的核心机制是：在过渡初期（$\lambda \approx 0$），角色主要遵循自我中心的运动预测，保持运动的自然性；随着时间推移（$\lambda \to 1$），目标中心的预测权重逐渐增大，驱动角色精确到达目标姿态。

### 2.4 输入输出向量构成

系统在每一帧 $i$ 接收完整的输入向量 $X_i$，由五个分量组成：

$$X_i = \{ X_i^{\mathcal{R}}, X_i^S, X_i^{\mathcal{T}}, X_i^C, X_i^{\mathcal{P}} \}$$

其中 $X_i^{\mathcal{R}}$ 为根轨迹信息，$X_i^S$ 为角色状态（姿态），$X_i^{\mathcal{T}}$ 为目标状态，$X_i^C$ 为接触标签，$X_i^{\mathcal{P}}$ 为运动相位特征。

对应地，系统预测下一帧 $i+1$ 的输出向量 $Y_{i+1}$：

$$Y_{i+1} = \{ Y_{i+1}^R, Y_{i+1}^{\hat{R}}, Y_{i+1}^S, Y_{i+1}^{\hat{S}}, Y_{i+1}^C, Y_{i+1}^P \}$$

其中 $Y_{i+1}^R$ 和 $Y_{i+1}^{\hat{R}}$ 分别为自我中心和目标中心的未来根轨迹预测，$Y_{i+1}^S$ 和 $Y_{i+1}^{\hat{S}}$ 为对应的姿态预测，$Y_{i+1}^C$ 为预测的下一帧接触标签（覆盖双脚、双手和髋部共5个关键关节），$Y_{i+1}^P$ 为未来1秒内（7个时间采样点）的相位更新（频率和振幅）。

### 2.5 可选控制约束

系统支持运行时通过轨迹混合参数 $\tau$ 控制角色沿用户指定路径运动：

$$T = \mathcal{I}(T^{*}, T^{+}, \tau)$$

其中 $T^{*}$ 为用户指定的期望轨迹，$T^{+}$ 为模型预测的轨迹，$\mathcal{I}$ 为线性或球面插值函数。当 $\tau=1.0$ 时，角色完全遵循用户路径；$\tau=0$ 时则完全依赖模型自主预测。此外，模型可通过额外的单热动作标签在训练时学习风格控制，从而在运行时指定期望的运动类型（如强制爬行而非步行，Fig. 8）。

## 实验与分析

### 核心瓶颈验证：长时程过渡中的时间模糊性

本文的核心主张是，现有运动插值方法在长过渡时间下性能下降，其根本原因在于**时间信息的模糊性**导致运动趋于平滑、不自然。表3（Table 3）的定量结果直接支撑了这一瓶颈：在LaFAN1测试集上，当过渡长度从30帧延长至120帧时，简单插值基线（Interpolation）的L2P误差从4.52急剧恶化至11.62，RTN（Harvey et al., TOG 2020）也从3.13上升至5.59。相比之下，本文方法在120帧外推时L2P仅为3.89，且在整个30–120帧范围内的平均值（3.32）显著优于RTN（3.93）和插值基线（6.56）。这表明，**基于相位流形的时间表示**有效缓解了长时程生成中的歧义问题，提供了稳定的时间外推能力。


![[assets/figures/papers/paper_list_l42_https_doi_org_10_1145_3606921/figures/009_Table_3.jpg]]
*Table 3: Comparison on the in-betweening stability for multiple transition lengths with different methods. Proc. ACM Comput. Graph. Interact. Tech., Vol. 6, No. 3, Article 37. Publication date: August 2023*

### 相位流形的消融证据

消融实验（Table 1, Fig. 6）系统验证了学习到的相位（Learned Phases）作为因果旋钮的有效性。Table 1量化了不同运动过渡类别下的平均关节旋转/秒（运动生动性），结果显示：使用学习相位的模型在快速冲刺急转弯（152.4 vs. 接触相位149.0 vs. 无相位147.3）、爬行（45.3 vs. 42.9 vs. 39.6）等类别上均产生更高的关节旋转速率。Fig. 6进一步从脚部接触稳定性角度证实，学习相位产生的脚部滑动伪影最少。这些结果表明，**手动定义的接触相位无法替代从数据中无监督学习到的周期性结构表示**，后者能够更精细地编码运动的时间相干性，从而引导网络生成更锐利、更生动的过渡动作。


![[assets/figures/papers/paper_list_l42_https_doi_org_10_1145_3606921/figures/005_Table_1.jpg]]
*Table 1: The average joint rotations per second for different classes of motion transitions. The control variables are extracted from the test data with a transition duration time between 1 and 3 seconds*

### 双向控制方案的关键作用

双向控制方案（bi-directional control）是确保目标到达精度的关键设计。Table 2的消融数据显示，在30帧过渡窗口下，加入双向控制后，步行任务的位置误差从21.59 cm降至9.61 cm，旋转误差从18.94°降至11.23°；其他任务（如跑步、坐下）也呈现一致改善。该方案通过时间相关的混合参数λ（见Eq. 2），在自我中心预测和目标中心预测之间平滑过渡，使角色能够自然逼近目标姿态，而非在末端突然“跳变”。


![[assets/figures/papers/paper_list_l42_https_doi_org_10_1145_3606921/figures/008_Table_2.jpg]]
*Table 2: The average positional error (in cm) and rotational error (in degree) produced by the model with/without bi-directional control for different tasks in 30 frames transitions windows, following reference control signals in the testing set. The error is measured after the in-betweening time on all joints correspondingly*

### 极端压力测试：定性证据

Fig. 7展示了最具说服力的定性证据——一个极端前向案例：目标帧距离起始帧10米，需在2秒内到达。在此压力条件下，使用学习相位的模型能够生成自然的跳跃动作，而使用接触相位或无相位的模型则出现明显的漂移或脚部滑动。这一结果与Table 3的定量外推能力形成交叉验证，共同证明**相位流形提供的时间结构是模型泛化至训练分布之外的关键**。

### 可选控制约束的效果

Table 4评估了通过轨迹混合参数τ控制路径的效果：当τ=1.0（完全沿用户指定路径运动）时，脚部滑动从0.432降至0.388，位置偏差和骨骼误差也有所改善。Fig. 8展示了动作标签（action labels）的控制效果——通过单热标签可强制角色在过渡中执行爬行而非步行，验证了框架对运动风格的运行时可控性。


![[assets/figures/papers/paper_list_l42_https_doi_org_10_1145_3606921/figures/011_Table_4.jpg]]
*Table 4: Impact of controlling the future trajectory through predefined paths on the ground using the authoring tool. The paths with their target frames at each control point are the same as shown in Fig. 10. The in-betweening time between the poses is 2 seconds. The control parameters ?? enables to perform realistic motion transitions along artificial paths, enabling better target accuracy and motion quality*

### 跨形态泛化：四足动物实验

Table 6报告了在四足动物数据集（Zhang et al., 2018）上的结果：本文方法在60帧（1秒）过渡长度上的L2P为0.51，优于插值基线（1.26）和Transformer基线（Qin et al., ACM Trans. Graph. 2022, 0.63）。这表明，**基于相位流形的混合专家架构不依赖于特定骨架形态**，其学习到的周期性时间表示具有跨形态的可迁移性。


![[assets/figures/papers/paper_list_l42_https_doi_org_10_1145_3606921/figures/014_Table_6.jpg]]
*Table 6: Qualitative results on quadruped dataset [Zhang et al. 2018]. The models are trained with a maximum transition length of 60 frames (1 second)*

### 用户研究：实用价值验证

Table 5的用户研究由两位专业动画师完成，结果显示：使用本文工具完成跑步循环、躺下到行走、行走到爬行三个过渡任务的平均时间分别从5.24小时、7.61小时、9.5小时降至6.5分钟、9.7分钟、7.9分钟。这一数量级的时间压缩验证了框架在实际动画生产流程中的实用价值。


![[assets/figures/papers/paper_list_l42_https_doi_org_10_1145_3606921/figures/013_Table_5.jpg]]
*Table 5: The average time taken by two professional animators to complete three animation transitions in our user study*

### 已知失败模式与局限

尽管整体性能优越，本文方法存在以下明确局限：
- **目标到达精度不完美**：由于网络压缩，末端效应器位置可能存在偏差，需追加逆运动学（IK）后处理修正脚部滑动。
- **生成受限于训练分布**：无法合成与训练集差异过大的运动模式，缺乏对未见运动类型的泛化能力。
- **确定性输出**：相同关键帧输入始终产生相同过渡，无法提供多样化变体。
- **缺乏环境交互**：当前框架仅基于纯运动学数据，不涉及障碍物、地形等环境约束。
- **过渡时长需手动指定**：模型无法自行推断合理时长，需用户提供。

### 待验证的开放问题

以下问题需要进一步研究验证：
- 能否利用扩散模型从相同关键帧合成多样化且自然的运动变体？
- 如何整合环境感知，使角色在过渡时能与障碍物或地形交互？
- 是否存在更高效的结构化相位表示，能够进一步减少网络压缩误差并提升目标到达精度？
## 方法谱系与知识库定位

### 1. 核心问题与因果机制

**真实瓶颈**：现有运动插值方法在过渡时间超过训练窗口时性能急剧退化——时间信息的模糊性导致生成的运动趋于平滑、不自然，缺乏有效的时间表示来引导生成过程并保持时间相干性。

**因果旋钮**：本文引入基于学习相位的流形作为控制信号。该流形通过**Periodic Autoencoder**（Starke et al., 2022）从运动捕捉数据中无监督提取，编码了运动的周期性结构（振幅 $A_i$ 和相位 $\Theta_i$），从而在时间上引导自回归生成过程，大幅改善长时程泛化并减少歧义。

**核心洞察**：运动的周期性可以用学习到的相位变量表示。将这些相位输入到**混合专家（MoE）网络**中，可以有效地在时间和空间上聚类运动——门控网络根据相位特征动态计算8个专家权重，生成运动预测网络的参数，使网络在自回归生成过程中利用这种时间结构来合成更锐利、更连贯的过渡。

### 2. 方法差异点（Changed Slots）

本文方法相对于既有工作的关键差异体现在以下五个技术槽位：

| 技术槽位 | 基线取值 | 本文取值 | 证据锚点 |
|---------|---------|---------|---------|
| 运动相位特征 | 无相位或手动定义的接触相位 | 由Periodic Autoencoder学习到的相位流形 $\mathcal{P}_i = A_i \cdot (\sin\Theta_i, \cos\Theta_i)$ | Section 3.1, 4.1 |
| 网络结构 | 标准全连接网络 | MoE结构：门控网络+运动预测网络，8个专家权重动态混合 | Section 3, 4 |
| 控制方案 | 单向预测（仅自我中心或目标中心） | 双向控制方案，通过时间相关的 $\lambda$ 参数平滑混合自我中心与目标中心预测 | Section 3.2, Eq. 2 |
| 输出预测 | 仅预测下一帧姿态和根轨迹 | 额外预测未来1秒内的相位更新（频率和振幅）、接触标签，并应用IK后处理 | Section 4.2, 5 |
| 可选约束 | 无额外约束 | 通过单热动作标签控制运动风格；通过轨迹混合参数 $\tau$ 控制沿用户路径运动 | Section 5.4 |

### 3. 与基线方法的关系

**RTN**（Harvey et al., TOG 2020）：作为主要神经基线，RTN采用标准全连接网络进行运动插值，缺乏相位引导和双向控制。在LaFAN1测试集上，本文方法在30-120帧的平均L2P误差为3.32，优于RTN的3.93；尤其在120帧外推时，本文方法L2P仅3.89，而RTN升至5.59（Table 3），证明相位流形提供了有效的时间外推能力。

**Interpolation（线性/球面插值）**：作为简单基线，在相同测试条件下L2P为6.56，显著劣于本文方法（3.32），且在长过渡时误差急剧增大（120帧时达11.62）。

**Transformer**（Qin et al., ACM Trans. Graph. 2022）：在四足动物数据集上，本文方法在60帧（1秒）过渡的L2P为0.51，优于Transformer的0.63和插值的1.26（Table 6），验证了相位引导的MoE结构在跨形态运动上的泛化能力。

### 4. 适用边界

- **数据依赖边界**：生成结果受限于LaFAN1训练数据的运动模式分布，无法合成与训练集差异过大的运动类型。
- **时间边界**：过渡持续时间需由用户手动指定合理值，模型无法自行推断最佳时长。
- **环境交互边界**：当前框架仅基于纯运动学数据，不涉及与环境的交互（如障碍物、地形），角色无法在过渡中感知或响应环境约束。
- **精度边界**：由于网络压缩，目标姿态的到达精度可能不够完美，需追加逆运动学（IK）后处理来修正末端效应器位置，减少脚部滑动伪影。
- **多样性边界**：系统为确定性生成，无法为相同关键帧提供多样化的运动变体。
- **交互边界**：尚未扩展到多角色交互运动插值场景。

### 5. 局限与开放问题

**已知局限**：
1. 训练数据依赖性导致生成模式受限。
2. 目标到达精度受网络压缩影响，需IK补偿。
3. 过渡时长不可自动推断。
4. 缺乏环境感知与交互能力。
5. 确定性输出缺乏多样性。
6. 不支持多角色交互。

**开放问题**：
1. **环境感知整合**：如何在运动插值中整合环境感知，使角色在过渡时能与障碍物或地形交互？
2. **随机时长学习**：能否以随机方式学习过渡时间的分布，从而实现非固定时长的生成？
3. **多样化生成**：能否利用扩散模型等生成式技术，从相同关键帧合成多样化且自然的运动变体？
4. **多角色扩展**：如何将框架扩展到多角色交互场景，支持协作或对抗性动作的插值？
5. **相位表示优化**：是否存在更高效的结构化相位表示，能够进一步减少网络压缩误差并提升目标到达精度？

## 原文 PDF

![[paperPDFs/PACM_CGIT_2023/Motion_In_Betweening_with_Phase_Manifolds.pdf]]
