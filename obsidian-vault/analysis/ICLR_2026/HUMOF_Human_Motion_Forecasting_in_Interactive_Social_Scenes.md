---
title: "HUMOF: Human Motion Forecasting in Interactive Social Scenes"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/HUMOF_Human_Motion_Forecasting_in_Interactive_Social_Scenes.pdf
openreview_forum_id: INy8guZqrm
aliases:
- HUMOF
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "由粗到细的交互推理模块与层次化表征的联合设计：通过多层Transformer中递进注入高层语义与低层几何特征，并结合自适应DCT重标定抑制早期高频分量。"
primary_logic: "通过层次化交互表征（高-低级语义/几何）和由粗到细的注入策略，辅以按层自适应抑制高频的DCT重标定，模型能够先聚焦全局上下文再进行局部细化，显著提升复杂动态场景下的人体运动预测精度。"
claims:
- "层次化交互表征（HSI和HHI）对运动预测性能有显著贡献，移除任一模块均导致误差上升。"
- "粗到细的交互特征注入策略优于仅使用单一层次的特征（粗粒度或细粒度），且优于同等多层次的均匀注入。"
- "自适应DCT重标定机制通过抑制早期高频更新，并适配不同样本，进一步提升了预测精度。"
- "所提方法在四个公开数据集（HIK, HOI-M^3, HUMANISE, GTA-IM）上均达到最优性能。"
---

# HUMOF: Human Motion Forecasting in Interactive Social Scenes

> [!tip] 核心洞察
> 通过层次化交互表征（高-低级语义/几何）和由粗到细的注入策略，辅以按层自适应抑制高频的DCT重标定，模型能够先聚焦全局上下文再进行局部细化，显著提升复杂动态场景下的人体运动预测精度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 交互式社交场景中的人体运动预测 |
| 英文题名 | HUMOF: Human Motion Forecasting in Interactive Social Scenes |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=INy8guZqrm); [GitHub](https://github.com/scy639/HUMOF) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HUMOF |
| Dataset | HIK, HOI-M^3, HUMANISE (Seen), GTA-IM |

> [!tip] 效果简介
> - HIK 上，Mean Path Error (mm) 为 180.7，对比 SAST 189.0，变化 8.3。
> - HOI-M^3 上，Mean Path Error (mm) 为 174.6，对比 SAST 184.8，变化 10.2。
> - HUMANISE (Seen) 上，Mean Path Error (mm) 为 41.7，对比 MutualDistance 57.8，变化 16.1。

## 概述

在动态社交场景中预测人体运动面临两大核心挑战：模型必须同时建模人-人交互与人-场景交互，且需要有效整合全局语义上下文与局部几何细节。现有方法——无论是仅关注场景的 **ContactAware**（Mao et al., 2022）、**GIMO**（Zheng et al., 2022）、**STAG**（Scofano et al., 2023）、**MutualDistance**（Xing et al., 2025），还是仅关注社交的 **T2P**（Jeong et al., 2024）、**IAFormer**（Xiao et al., 2025），乃至同时考虑两者的 **SAST**（Mueller et al., 2024）——均缺乏由粗到细的层次化交互推理机制，难以在复杂动态场景下实现精准预测。

本文提出 **HUMOF**，通过三个关键设计解决上述瓶颈：

1. **层次化交互表征**：同时建模人-人交互（HHI）和人-场景交互（HSI），并在高层语义（身体级/粗粒度场景）与低层几何（关节级/细粒度场景）两个层级显式编码交互距离。
2. **由粗到细的交互推理**：在多层 Transformer 中递进注入交互特征——早期层接收高层语义令牌以建立全局上下文，后期层逐步注入低层几何令牌以细化局部细节。
3. **自适应 DCT 重标定**：通过可学习的样本自适应向量与预定义的高频抑制向量逐元素相乘，在早期层抑制高频分量更新，末层完全放开，使模型优先学习平滑的全局运动趋势。

实验表明，HUMOF 在四个公开数据集（**HIK**、**HOI-M³**、**HUMANISE**、**GTA-IM**）上均达到最优性能（Table 1, Table 2）。消融研究（Table 3）验证了层次化表征、由粗到细注入策略以及自适应 DCT 重标定各自对性能的显著贡献。值得注意的是，该方法无需预定义语义标签或实例分割，直接处理原始点云，具备良好的实际部署潜力。

## 背景与动机

在拥挤的室内外场景中预测人体未来运动，是自动驾驶、人机交互、AR/VR等应用的核心能力。真实动态场景中的运动预测面临双重挑战：**人-人交互**（如擦肩而过、结伴行走、转向避让）与**人-场景交互**（如绕过桌椅、伸手取物、倚靠墙壁）往往同时发生且相互耦合（Figure 1）。然而，现有方法在这两类交互的联合建模上存在明显缺口。

**现有方法的瓶颈**在于：场景感知方法（如 **ContactAware**（Mao et al., 2022）、**GIMO**（Zheng et al., 2022）、**STAG**（Scofano et al., 2023）、**MutualDistance**（Xing et al., 2025））专注于人-场景交互，但缺乏对多人体社交上下文的显式建模；社交感知方法（如 **T2P**（Jeong et al., 2024）、**IAFormer**（Xiao et al., 2025））致力于捕捉人-人交互，却忽视了场景几何的约束。少数同时考虑两者的方法（如 **SAST**（Mueller et al., 2024））虽试图弥合这一鸿沟，但其依赖预定义语义标签或实例分割，且采用扩散机制导致推理速度极慢（约2秒/样本），难以满足实时性需求。

更深层的问题在于**交互推理的粒度与层次**。真实交互行为天然具有层次性：高层语义（如“走向桌子”）提供全局意图，低层几何（如“手与桌面的精确距离”）决定局部细节。现有方法要么仅使用单一粒度的特征，要么将所有交互信息一次性注入模型，缺乏从全局上下文到局部细化的**由粗到细推理过程**。此外，在频域视角下，运动预测的早期阶段应优先确定整体趋势（低频分量），而非过早拟合高频细节——这一归纳偏置在现有方法中未被显式利用。

综上，本文的核心动机是：**设计一种层次化交互表征与由粗到细推理机制相结合的方法**，使其能够在不依赖语义标签的前提下，同时高效建模人-人与-人-场景交互，并在复杂动态场景中实现精确且鲁棒的运动预测。

## 核心创新

HUMOF 的核心创新在于构建了一套**层次化交互表征**与**由粗到细的交互推理机制**，系统性地解决了现有方法在复杂动态场景中无法同时有效建模人-人交互与人-场景交互的瓶颈。其关键设计体现为以下三个紧密耦合的 changed slots。

### 1. 层次化交互表征：从高层语义到低层几何

现有方法通常采用单一层级的交互表征——例如仅使用关节级特征（如 **ContactAware**, Mao et al., 2022）或缺乏显式的场景交互编码（如 **IAFormer**, Xiao et al., 2025）。HUMOF 则构建了多维度的层次化表征，将交互信息分解为**高层语义**（身体级/粗粒度场景）与**低层几何**（关节级/细粒度场景）两个层次。

具体而言，在人-人交互（HHI）模块中，模型通过**自编码**捕获交互者的独立运动信息，同时基于最近关节间的最小距离序列构建**关系编码**，二者拼接形成身体级与关节级的 HHI 令牌（Equation 2）。在人-场景交互（HSI）模块中，模型摒弃了对预定义语义标签的依赖（如 **SAST** 需真实实例分割，Mueller et al., 2024），转而采用整体点云表示，通过 PointNet++ 的集合抽象层构造不同粒度的场景交互令牌（Figure 3(b)）。消融实验表明，移除 HSI 或 HHI 中的任一子模块均导致路径与姿态误差显著上升（Table 3(a)），验证了层次化表征中各组件不可替代的独立贡献。

### 2. 由粗到细的交互特征注入策略

传统方法通常一次性注入所有交互特征，或未考虑粗细粒度的注入顺序。HUMOF 提出了一种**由粗到细的注入策略**：在 6 层 Interaction-Perceptive Transformer 中，早期层注入高层语义令牌以建立全局上下文，随着层数加深逐步注入低层几何令牌以进行局部细化（Figure 3(c)）。

消融实验（Table 3(b)）证实了这一策略的有效性：仅使用粗粒度特征或仅使用细粒度特征，性能均显著劣于多层级特征；而采用由粗到细的注入策略，相比多层级均匀注入能进一步降低误差。值得注意的是，不同注入排布的变体对性能影响较小（Table 5），表明该策略具有良好的鲁棒性。

### 3. 自适应 DCT 重标定：频率域的层次化控制

为从频率域支撑由粗到细的推理过程，HUMOF 引入了**自适应 DCT 重标定机制**（Equation 4）。该机制在每层 Transformer 中，将预定义的按层衰减的高频抑制向量 $\mathbf{v}^{(l)}$ 与样本自适应向量 $\pmb{\alpha}(\tilde{\mathbf{X}})$ 逐元素相乘，得到当前层的重标定向量。早期层的高频分量被大幅抑制，迫使模型聚焦于低频的粗粒度运动模式；随着层数加深，抑制逐渐减弱，在末层完全放开，允许精细的高频细节被恢复。

样本自适应向量通过 MLP 从当前层关节特征的平均池化中学习，使得重标定强度能够根据不同输入样本动态调整。消融实验（Table 3(c)）表明，相比静态重标定，自适应机制带来了额外的性能增益，验证了频率域层次化控制与由粗到细注入策略之间的协同效应。

### 创新协同效应

上述三个 changed slots 并非孤立存在，而是形成了从**表征构建**到**特征注入**再到**频率调控**的完整因果链条：层次化表征提供了不同粒度的交互信息源，由粗到细的注入策略决定了信息何时进入推理过程，自适应 DCT 重标定则在频率域约束了模型在各阶段可更新的信息频段。三者联合设计使得模型能够先聚焦全局语义上下文，再进行局部几何细节的细化，从而在 HIK、HOI-M³、HUMANISE、GTA-IM 四个公开数据集上均达到最优性能（Table 1, Table 2）。

## 整体框架

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_INy8guZqrm/figures/003_Figure_3.jpg]]
*Figure 3: Detailed architecture of HUMOF. Our method takes inputs from three aspects: the past motions of the target person, a 3D point cloud for the scene, and motion sequences of interactive persons. The interactions are comprehensively encoded by (a) Hierarchical Human-Human Interaction Representation and (b) Hierarchical Human-Scene Interaction Representation, respectively. Thereafter, the hierarchical representations are leveraged by (c), a Coarse-to-Fine Interaction Reasoning Module, to predict future motions for the target person. Details of the Interaction-Perceptive Transformer layer in (c) are shown on the top right*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_INy8guZqrm/figures/002_Figure_2.jpg]]
*Figure 2: HUMOF Overview*

HUMOF 的整体流程围绕“层次化交互表征”与“由粗到细的交互推理”两个核心设计展开，其输入包含三类信息：目标人物的历史运动序列 $\mathbf{X}^{1:H}$、场景的 3D 点云 $\boldsymbol{S} = \{s_1, \cdots, s_N\}$，以及 $K$ 个交互者的历史运动序列。模型最终输出目标人物在未来 $T$ 帧的完整运动序列，涵盖根关节的全局路径与所有关节的局部姿态。

整个 pipeline 由五个模块串联构成（见 Figure 2 与 Figure 3）：

**1. Motion Encoder（运动编码器）**  
对目标人物及每个交互者的历史运动序列，先通过离散余弦变换（DCT）将时域关节轨迹映射到频域，再经由图卷积网络（GCN）提取关节间的空间依赖，最后叠加可学习的位置嵌入 $\mathcal{P}$ 以区分不同关节。该模块输出每个关节的频域特征令牌 $\tilde{\mathbf{X}}$，作为后续交互推理的基础表征（Equation 1）。

**2. Hierarchical HHI Representation（层次化人-人交互表征）**  
针对每个交互者，分别构建自编码（Self-Encoding）与关系编码（Relation-Encoding）两条并行分支。自编码分支对交互者自身的运动进行独立编码，捕捉其运动意图；关系编码分支则计算交互者各关节与目标人物最近关节之间的最小欧氏距离序列，经 DCT 后形成显式的交互距离特征。两者拼接后，分别在身体级（body-level）和关节级（joint-level）两个粒度上形成 HHI 令牌（Section 3.2.1）。

**3. Hierarchical HSI Representation（层次化人-场景交互表征）**  
以场景原始点云为输入，首先计算每个场景点与目标人物各关节在历史帧上的交互距离时间序列，经 DCT 后作为逐点的交互特征。随后，通过 PointNet++ 的多层集合抽象（Set Abstraction）逐级聚合，构造出从细粒度到粗粒度的层次化场景交互令牌。该过程无需预定义语义标签或实例分割，可直接处理原始点云（Section 3.2.2）。

**4. Coarse-to-Fine Interaction Reasoning Module（由粗到细的交互推理模块）**  
该模块由 6 层 Interaction-Perceptive Transformer 堆叠而成，是 HUMOF 的核心推理引擎。每层 Transformer 先对目标人物的关节令牌执行自注意力（Self-Attention），再以关节令牌为 Query、以交互令牌（HHI 与 HSI）为 Key 和 Value 执行交叉注意力（Cross-Attention），从而将交互信息融入运动表征。其关键创新在于**由粗到细的注入策略**：早期层注入高层语义交互令牌（身体级 HHI、粗粒度 HSI），引导模型建立全局交互上下文；深层逐步注入低层几何交互令牌（关节级 HHI、细粒度 HSI），实现局部细节的精细化。此外，每层还引入**自适应 DCT 重标定机制**（Adaptive DCT Rescaling），通过将预定义的高频抑制向量 $\mathbf{v}^{(l)}$ 与样本自适应向量 $\pmb{\alpha}(\tilde{\mathbf{X}})$ 逐元素相乘，在早期层抑制高频细节的更新幅度，迫使模型优先聚焦低频、粗粒度的运动模式，最后一层则完全放开高频更新（Equation 4）。

**5. Motion Decoder（运动解码器）**  
将第 6 层 Transformer 输出的关节令牌依次通过 GCN 解码器和逆离散余弦变换（IDCT），恢复为时域运动序列 $\hat{\mathbf{X}}$。损失函数由路径损失 $\ell_{\mathrm{path}}$ 和局部姿态损失 $\ell_{\mathrm{local}}$ 两部分 L2 距离构成，分别监督根关节轨迹与其余关节的局部姿态。

综上，HUMOF 通过“频域运动编码 → 层次化交互表征构造 → 由粗到细的注意力融合与频域调控 → 时域解码”这一信息流，实现了对复杂动态场景中多尺度交互的递进式建模。

## 核心模块与公式推导

### 3.1 运动编码器

HUMOF首先将目标人物的历史运动序列转换到频域，以获取紧凑的时空表征。运动编码器由离散余弦变换（DCT）和图卷积网络（GCN）串联构成，如Figure 3(c)左侧所示。给定目标人物的历史关节运动序列 $\mathbf{X} \in \mathbb{R}^{J \times H \times 3}$（$J$个关节，$H$帧历史），编码过程为：

$$
\tilde{\mathbf{X}} = \mathbf{GCN}(\mathrm{DCT}(\mathbf{X})) + \mathcal{P}
$$

其中 $\mathrm{DCT}(\cdot)$ 将时域运动变换到频域，$\mathbf{GCN}(\cdot)$ 提取关节间的空间依赖关系，$\mathcal{P} \in \mathbb{R}^{J \times C'}$ 为可学习的位置嵌入，用于区分不同关节的身份。输出 $\tilde{\mathbf{X}}$ 是频域关节令牌，作为后续交互推理模块的核心输入。

### 3.2 层次化交互表征

HUMOF的核心设计在于从两个维度构建层次化的交互表征：人-人交互（HHI）和人-场景交互（HSI），每个维度均包含高层语义（身体级/粗粒度场景）与低层几何（关节级/细粒度场景）两个层次。

#### 3.2.1 层次化人-人交互表征（HHI）

对于第 $k$ 个交互者，HHI表征由两个互补的子模块构成（Figure 3a）：

**自编码（Self-Encoding）**：将交互者的历史运动独立地通过运动编码器，获得其自身的频域关节令牌 $\tilde{\mathbf{Y}}^{(k)}$，用于描述交互者的独立运动模式。身体级令牌 $\tilde{\mathbf{c}}_{\text{body}}^{(k)}$ 通过对关节令牌进行平均池化得到。

**关系编码（Relation-Encoding）**：显式建模目标人物与交互者之间的几何距离关系。对于第 $t$ 帧，交互者第 $j$ 个关节与目标人物最近关节之间的映射距离定义为：

$$
\mathbf{D}_{j}^{(k)t} = \phi\left(\min_{i \in [1,J]} \| \mathbf{y}_{j}^{(k)t} - \mathbf{x}_{i}^{t} \|_{2}^{2} \right)
$$

其中 $\phi(\cdot)$ 为非线性映射函数。对所有历史帧计算后得到距离时间序列，再经DCT变换到频域，获得关系编码 $\tilde{\mathbf{D}}_{j}^{(k)}$。身体级关系编码 $\tilde{\mathbf{D}}_{\text{body}}^{(k)}$ 同样通过池化得到。

最终，第 $k$ 个交互者的身体级HHI令牌由自编码与关系编码拼接而成：$\tilde{\mathbf{O}}_{\text{body}}^{(k)} = \mathrm{concat}(\tilde{\mathbf{c}}_{\text{body}}^{(k)}, \tilde{\mathbf{D}}_{\text{body}}^{(k)})$。关节级HHI令牌以相同方式构建。

#### 3.2.2 层次化人-场景交互表征（HSI）

HSI表征基于场景的3D点云 $\boldsymbol{S} = \{s_1, \dots, s_N\}$ 构建，无需预定义语义标签（如Figure 3b所示）。对于每个场景点 $s_n$，首先计算其与目标人物第 $j$ 个关节在所有 $H$ 帧上的交互距离时间序列：

$$
m_j = \{ \phi( \| s_n - \mathbf{x}_j^1 \|_2^2 ), \cdots, \phi( \| s_n - \mathbf{x}_j^H \|_2^2 ) \} \in \mathbb{R}^H
$$

对所有关节聚合后经DCT变换，得到该点的交互特征 $\tilde{f}_n^{(0)}$。随后，利用PointNet++的集合抽象层 $\{\mathcal{G}^{(0)}, \dots, \mathcal{G}^{(b)}\}$ 对点云进行层次化下采样和特征聚合，产生不同粒度的场景交互令牌：$\mathcal{G}^{(0)}$ 输出细粒度（低层几何）令牌，$\mathcal{G}^{(b)}$ 输出粗粒度（高层语义）令牌。

### 3.3 由粗到细的交互推理模块

该模块由6层交互感知Transformer堆叠而成，核心包含三个机制：

**由粗到细的特征注入**：高层交互令牌（身体级HHI、粗粒度HSI）被注入到早期Transformer层，低层令牌（关节级HHI、细粒度HSI）逐步注入到更深层（Figure 3c）。这使得模型先建立全局交互上下文，再进行局部几何细节的细化。

**交互感知Transformer层**：每层首先对目标人物的关节令牌 $\tilde{\mathbf{X}}^{(l)}$ 进行自注意力（SA），然后以关节令牌为查询（Query）、交互令牌为键值（Key-Value）进行交叉注意力（CA），实现交互信息的融合。

**自适应DCT重标定**：为配合由粗到细的推理策略，在频域对关节令牌的更新幅度进行逐层调控。第 $l$ 层的重标定向量定义为：

$$
\mathbf{v}'(\tilde{\mathbf{X}})^{(l)} = \mathbf{v}^{(l)} \odot \boldsymbol{\alpha}(\tilde{\mathbf{X}}), \quad \boldsymbol{\alpha}(\tilde{\mathbf{X}}) = \mathbf{MLP}\left(\frac{\sum_{j=1}^{J} \tilde{\mathbf{x}}_j^{(l)}}{J}\right)
$$

其中 $\mathbf{v}^{(l)}$ 为预定义的静态高频抑制向量（早期层抑制高频DCT系数，末层完全放开），$\boldsymbol{\alpha}(\tilde{\mathbf{X}})$ 为样本自适应向量，由关节令牌平均池化后经MLP生成。两者逐元素相乘，实现对不同频率成分更新幅度的联合调控。

### 3.4 运动解码器与损失函数

第6层Transformer输出的关节令牌 $\tilde{\mathbf{X}}^{(6)}$ 经GCN解码和逆离散余弦变换（IDCT）恢复为时域运动序列：

$$
\hat{\mathbf{X}} = \mathrm{IDCT}(\mathrm{GCN}(\tilde{\mathbf{X}}^{(6)})) \in \mathbb{R}^{J \times (H+T) \times 3}
$$

训练损失由路径损失和局部姿态损失组成。路径损失衡量预测根关节位置与真值之间的均方误差：

$$
\ell_{\mathrm{path}} = \frac{1}{T} \sum_{t=H+1}^{H+T} \| \mathbf{X}_{\mathrm{root}}^{t} - \hat{\mathbf{X}}_{\mathrm{root}}^{t} \|_{2}^{2}
$$

局部姿态损失衡量预测的非根关节姿态与真值之间的均方误差：

$$
\ell_{\mathrm{local}} = \frac{1}{T(J-1)} \sum_{t=H+1}^{H+T} \sum_{j=1}^{J-1} \| \mathbf{X}_{\mathrm{local},j}^{t} - \hat{\mathbf{X}}_{\mathrm{local},j}^{t} \|_{2}^{2}
$$

总损失为两者之和。

### 3.5 关键设计决策的因果机制

消融实验（Table 3）系统验证了上述模块的因果贡献：

- **层次化表征的必要性**（Table 3a）：移除HSI或HHI的任一部分（自编码或关系编码）均导致路径误差和姿态误差显著上升，证实了人-场景交互与人-人交互的互补性，以及显式距离编码对隐式自编码的补充作用。
- **由粗到细注入策略的优越性**（Table 3b）：仅使用粗粒度或细粒度单层特征的效果均劣于多层级特征；而在多层级特征中，由粗到细的递进注入策略又显著优于均匀注入，表明“先全局后局部”的推理顺序对复杂动态场景建模至关重要。
- **自适应DCT重标定的增益**（Table 3c）：静态高频抑制向量已能带来性能提升，而样本自适应向量的引入进一步增强了模型对不同运动模式的适配能力，验证了频域调控机制的有效性。

## 实验与分析

### 1 主实验结果

HUMOF在四个公开数据集上均达到最优性能，覆盖了动态社交场景（HIK、HOI-M³）与静态场景（HUMANISE、GTA-IM）两大类测试条件。

**动态场景数据集。** 在HIK与HOI-M³上，HUMOF在路径误差（Mean Path Error）和姿态误差（Mean Pose Error）上全面超越所有对比方法（Table 1）。具体而言，HIK上路径误差降至 **180.7 mm**，较此前最优的社交-场景感知方法SAST（189.0 mm）降低8.3 mm；HOI-M³上路径误差降至 **174.6 mm**，较SAST（184.8 mm）降低10.2 mm。值得注意的是，HUMOF是唯一一个在HOI-M³可视化案例中正确捕捉到“转向交互者”意图并预测出正确运动方向的方法（Figure 4）。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_INy8guZqrm/figures/004_Table_1.jpg]]
*Table 1: Comparisons on datasets with dynamic scenes. We compare with scene-aware methods, ContactAware, GIMO, STAG, and MutualDistance, social-aware method, IAFormer and T2P, and social-scene-aware method SAST*

**静态场景数据集。** 在HUMANISE可见场景子集上，HUMOF的路径误差仅为 **41.7 mm**，较MutualDistance（57.8 mm）大幅降低16.1 mm；在GTA-IM上，路径误差为 **62.9 mm**，较MutualDistance（72.0 mm）降低9.2 mm（Table 2）。该结果表明，即便在场景元素不移动的条件下，层次化交互表征仍能带来显著精度增益。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_INy8guZqrm/figures/006_Table_2.jpg]]
*Table 2: Comparisons on datasets with static scenes. Results with * are from MutualDitance*

**长时预测与分布质量。** 在HOI-M³的10秒长时预测任务中，HUMOF的NPSS降至 **0.227**，优于IAFormer的0.246（Table 12）；FID得分降至 **0.0164**，优于IAFormer的0.0170（Table 13），表明预测运动的分布更接近真实数据。

**公平性说明。** 为公平对比，研究团队对场景感知方法（ContactAware、GIMO、STAG、MutualDistance）通过拼接多人信息至解码器输入来引入多人上下文；对社交感知方法（T2P、IAFormer）则利用HUMOF提取的人-场景交互特征作为额外输入。SAST在除GTA-IM外的数据集上均使用真实实例分割结果以最大化其性能。HUMOF本身不依赖任何预定义语义标签或实例分割，可直接处理原始点云。

---

### 2 消融实验

消融实验从三个核心设计维度验证了HUMOF各组件的贡献（Table 3）。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_INy8guZqrm/figures/011_Table_3.jpg]]
*Table 3: Ablations studies*

**层次化交互表征。** 移除人-场景交互模块（HSI）或人-人交互模块（HHI，包括自编码与关系编码）均导致路径误差和姿态误差显著上升（Table 3a）。这表明高层语义与低层几何的双层表征对复杂交互建模不可或缺。

**由粗到细的注入策略。** 仅使用粗粒度特征（仅注入高层令牌）或仅使用细粒度特征，效果均劣于多层级特征；而在多层级特征的基础上，采用由粗到细的逐层注入策略进一步优于均匀注入（Table 3b）。这验证了“先全局上下文、后局部细节”的推理顺序对运动预测的有效性。附录中不同注入排布变体的实验表明该策略具有较好的鲁棒性（Table 5）。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_INy8guZqrm/figures/010_Table_5.jpg]]
*Table 5: (b) Injection Strategy*

**自适应DCT重标定。** 应用静态高频抑制向量即可提升精度，而加入样本自适应向量后带来额外增益（Table 3c）。这证明按层抑制高频细节、并在末层完全放开的频域调控机制，能够有效配合由粗到细的推理过程。

**架构超参数。** 增加场景采样点数或Transformer层数可提升性能，但边际收益递减，6层为默认设置（Table 6, Table 7）。在交互信息不完整（人-人或人-场景信息缺失）的情况下，HUMOF仍优于基准方法（Table 8），显示出对输入缺失的鲁棒性。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_INy8guZqrm/figures/013_Table_8.jpg]]

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_INy8guZqrm/figures/014_Table_6.jpg]]
*Table 6: Ablation study on different number of sampled point of the static scene on GTA-IM dataset*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_INy8guZqrm/figures/015_Table_7.jpg]]
*Table 7: Ablation study on different number of Transformer layers on GTA-IM dataset*

---

### 3 失败模式与局限性

尽管HUMOF在整体指标上表现优异，但存在以下可识别的失败模式：

1. **突发动作预测困难。** 对于突然的弯腰、起身走开等运动模式切换，所有方法均表现不佳（Figure 10）。这类案例涉及意图层面的突变，纯运动学线索难以提前捕捉。

2. **交互建模范式的单一性。** 当前交互表征完全基于距离度量，忽略了方向等几何关系。尽管实验表明显式SE(3)编码并未带来增益（原因尚不明确），但这可能限制了模型在需要精确相对朝向的场景中的表现。

3. **联合多人体预测的协调性不足。** 在联合预测多个体运动时，HHI模块仅依赖历史运动序列，无法显式感知其他个体的未来预测，导致迭代预测中可能出现个体间运动协调性的偏差。

4. **物理穿透的残余。** 尽管HUMOF在穿透率与运动精度之间取得了良好平衡（Table 14），但未采用基于网格的几何建模来进一步抑制穿透现象。

---

### 4 关键图表结论摘要

- **Table 1 & Table 2：** HUMOF在四个数据集上均达到SOTA，动态场景下优势尤为显著。
- **Table 3：** 层次化表征、由粗到细注入、自适应DCT重标定三者各自独立贡献显著，联合使用效果最优。
- **Figure 4：** 定性结果显示HUMOF能正确捕捉社交意图（如转向交互者），而对比方法倾向于维持原方向。
- **Figure 6 & Figure 7：** 在场景遮挡和输入噪声增加的情况下，HUMOF的性能退化幅度小于对比方法，表明层次化交互表征对不完整和噪声输入具有较强鲁棒性。
- **Figure 10：** 失败案例集中于运动模式的突然切换，提示未来需引入意图推理或额外模态（如注视信息）。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_INy8guZqrm/figures/005_Table_2.jpg]]
*Table 2: HUMANISE Dataset Wang et al. (2022)*

### 补充图表

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_INy8guZqrm/figures/009_Table_4.jpg]]
*Table 4: (a) Hierarchical Representations*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_INy8guZqrm/figures/012_Table_4.jpg]]
*Table 4: Runtime analysis on $\mathrm { H O I - M ^ { 3 } }$ Dataset*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

HUMOF 的核心贡献在于首次将**层次化交互表征**与**由粗到细的交互推理**联合引入人体运动预测领域，解决了现有方法在复杂动态场景中未能同时建模人-人交互与人-场景交互的瓶颈问题。其方法定位可从以下三个维度理解：

**相对于场景感知方法。** 早期工作如 **ContactAware** (Mao et al., 2022)、**GIMO** (Zheng et al., 2022)、**STAG** (Scofano et al., 2023) 和 **MutualDistance** (Xing et al., 2025) 主要关注人-场景交互，但缺乏对多人社交上下文的显式建模。HUMOF 在场景表示上同样采用点云输入，但通过 PointNet++ 的集合抽象层构造了多粒度的层次化场景表征，无需依赖预定义语义标签或实例分割——这与 **SAST** (Mueller et al., 2024) 形成鲜明对比，后者需要真实实例分割结果作为输入才能发挥最佳性能。

**相对于社交感知方法。** **T2P** (Jeong et al., 2024) 和 **IAFormer** (Xiao et al., 2025) 虽能建模多人交互，但缺乏对场景几何的感知能力。HUMOF 的人-人交互模块不仅通过注意力机制隐式建模，还引入了显式的**交互距离关系编码**：基于最近关节的最小距离序列经 DCT 变换后与独立运动自编码拼接，形成身体级和关节级的层次化 HHI 令牌。这种显式距离编码是 HUMOF 区别于纯注意力交互建模的关键设计。

**相对于社交-场景联合感知方法。** **SAST** 是目前唯一同时考虑人-人和人-场景交互的方法，但其交互表征缺乏层次化粒度区分，且依赖语义分割。HUMOF 在 SAST 的基础上实现了三个关键突破：(1) 将交互表征从单一层级提升为高层语义（身体级/粗粒度场景）与低层几何（关节级/细粒度场景）的层次化组合；(2) 设计了由粗到细的注入策略，使早期 Transformer 层聚焦全局上下文，后期层逐步细化局部细节；(3) 引入自适应 DCT 重标定机制，通过预定义的高频抑制向量与样本自适应向量的逐元素乘积，在早期层抑制高频分量更新，引导模型优先学习低频的粗粒度运动趋势。

### 2. 关键设计决策的因果机制

消融实验（Table 3）揭示了各模块的因果贡献链：

- **层次化交互表征的因果作用**：同时移除 HSI 或 HHI 中的自编码/关系编码子模块均导致路径和姿态误差显著上升，表明高层语义与低层几何的互补性对复杂场景预测不可或缺。
- **由粗到细注入策略的因果作用**：仅使用粗粒度特征或仅使用细粒度特征的效果均劣于多层级特征；而采用由粗到细的注入策略进一步优于多层级均匀注入。这说明注入顺序本身具有因果效应——先全局后局部的信息流比同时暴露所有粒度更有效。
- **自适应 DCT 重标定的因果作用**：静态重标定（共享的高频抑制向量）已能带来增益，但样本自适应向量通过 MLP 从关节特征均值中学习实例级调节因子，进一步提升了精度。这表明不同样本对高频抑制的需求存在差异，固定策略无法覆盖这种多样性。

### 3. 适用边界与局限

**已知局限**（论文明确报告）：

1. **突发动作预测困难**：所有方法在突然的动作变化（如弯腰、突然起身走开）上均表现不佳（Figure 10），HUMOF 也不例外。这表明仅依赖历史运动序列和空间距离的交互建模，难以捕捉意图层面的突变。
2. **交互建模范式单一**：当前 HHI 和 HSI 均基于距离度量。尽管实验表明显式的 SE(3) 相对变换编码并未带来增益，但方向等几何关系是否可通过其他方式有效利用仍待探索。
3. **联合多人体预测缺乏协调**：在迭代预测多人体时，HHI 模块仅依赖历史运动序列，无法显式感知其他个体的未来预测，可能导致预测轨迹间缺乏协调性。
4. **物理穿透未显式约束**：方法未采用基于网格的几何建模来进一步降低人-物和人-人穿透，尽管当前方法已在穿透率与运动精度之间取得了良好平衡（Table 14）。

**适用边界推断**：

- **场景动态性**：方法在静态场景（HUMANISE、GTA-IM）和动态场景（HIK、HOI-M³）上均验证有效，且论文指出模型架构可原生处理动态场景元素而无需结构修改。但验证集中于人体运动，对移动家具、车辆等多样化动态物体的泛化能力尚待更大规模数据集检验。
- **交互信息完整性**：在交互信息不完整（人-人或人-场景信息缺失）的情况下，HUMOF 依然优于基准方法（Table 8），表明层次化表征具有一定的信息冗余和鲁棒性。
- **长时预测**：在 10 秒长时预测任务上（Table 12），HUMOF 的 NPSS 指标优于 IAFormer，但绝对误差仍较高，说明长时预测仍是开放挑战。

### 4. 开放问题

1. **意图推断与多模态融合**：如何结合人类注视信息等额外模态，以更好地推断交互意图并解决突发动作的预测难题？
2. **迭代式多人预测**：如何将 HHI 模块扩展为迭代式结构，使其在预测某一目标个体时能利用上一轮迭代中其他个体的预测运动，从而增强多人轨迹的协调性？
3. **SE(3) 编码的失效原因**：为什么显式的 SE(3) 相对变换编码未能提供性能增益？模型是否已通过时序距离模式隐式学习到了朝向和运动关系？这需要更深入的表征分析来回答。
4. **多样化动态物体的泛化**：在具备大量且多样化动态物体（如移动的家具、车辆）的更大规模数据集上，现有框架能否保持领先优势？层次化表征的粒度设计是否需要针对新物体类别进行调整？
5. **替代交互建模范式**：能否通过引入拓扑约束或力学模型等替代交互建模范式来进一步提升泛化性能，尤其是在物理穿透和接触合理性方面？

## 原文 PDF

![[paperPDFs/ICLR_2026/HUMOF_Human_Motion_Forecasting_in_Interactive_Social_Scenes.pdf]]
