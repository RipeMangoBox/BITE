---
title: "CoopDiff: Anticipating 3D Human-object Interactions via Contact-consistent Decoupled Diffusion"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/CoopDiff_Anticipating_3D_Human_object_Interactions_via_Contact_consistent_Decoupled_Diffusion.pdf
aliases:
- CoopDiff
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将人体和物体运动建模解耦为两个独立分支，并利用接触点作为共享锚点，通过接触一致性约束和人驱动交互模块桥接两个分支，从而实现更逼真的人-物交互预测。
primary_logic: 人体和物体具有不同的动力学特性，但通过共享的接触点可以实现联合一致的运动预测。接触点为解耦建模提供了天然的桥梁。
claims:
- 逐步添加解耦（Dcp）、接触注入（Cont）、一致性约束（CCC）和人驱动交互模块（HIM），所有指标持续改善，最终MPJPE-H从基线140降至123。
- 相比InterDiff，CoopDiff在BEHAVE数据集上穿透率（Pene.）大幅降低43%，表明交互更真实。
- 可视化显示CoopDiff预测的交互比InterDiff具有更少的互穿透、物体漂浮和无接触物体运动。
- BEHAVE 上 MPJPE-H ↓ = 123
---

# CoopDiff: Anticipating 3D Human-object Interactions via Contact-consistent Decoupled Diffusion

> [!tip] 核心洞察
> 人体和物体具有不同的动力学特性，但通过共享的接触点可以实现联合一致的运动预测。接触点为解耦建模提供了天然的桥梁。

| 字段 | 内容 |
|------|------|
| 中文题名 | CoopDiff：基于接触一致解耦扩散的3D人-物交互预测 |
| 英文题名 | CoopDiff: Anticipating 3D Human-object Interactions via Contact-consistent Decoupled Diffusion |
| 会议/期刊 | arXiv 2025 |
| Links |  [paper](https://arxiv.org/abs/2508.07162)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | CoopDiff |
| Dataset | BEHAVE, HOI |

> [!tip] 效果简介
> - BEHAVE 上，MPJPE-H ↓ 123 vs 140 (InterDiff) (-17 (↓12.1%))；Trans.Err. ↓ 106 vs 123 (InterDiff) (-17 (↓13.8%))；Rot.Err. ↓ 200 vs 226 (InterDiff) (-26 (↓11.5%))。
> - HOI 上，MPJPE-H ↓ 100 vs 105 (InterDiff) (-5)；MPJPE-O ↓ 83 vs 84 (InterDiff) (-1)；Trans.Err. ↓ 58 vs 60 (InterDiff) (-2)。

## 概述

预测未来的人-物交互（Human-Object Interaction, HOI）是具身智能与环境理解中的关键任务。现有方法通常使用单一模型联合预测人体与物体的未来运动，但忽视了二者在运动模式上的本质差异——人体关节高度结构化且运动复杂多样，而物体仅涉及刚性平移与旋转（见 Figure 1）。这种统一建模策略容易导致不精确甚至不真实的交互结果，例如人体与物体相互穿透、物体漂浮或无接触下的物体漂移。

针对上述瓶颈，本文提出 **CoopDiff**，一个基于接触一致解耦扩散的3D人-物交互预测框架。其核心洞察在于：人体与物体具有截然不同的动力学特性，但二者通过共享的**接触点**天然关联，这为解耦建模提供了桥梁。CoopDiff 采用双分支扩散架构，分别对人体结构化运动与物体刚性运动进行独立建模，并将接触点作为共享锚点注入两个分支；同时引入**接触一致性约束（Contact Consistency Constraint, CCC）** 对齐两分支的接触预测，确保运动一致性；进一步通过**人驱动交互模块（Human-driven Interaction Module, HIM）** 将人体动态作为条件控制传递给物体分支，增强交互真实感。

在 BEHAVE 和 Human-Object Interaction 两个标准数据集上的实验表明，CoopDiff 显著优于先前最优方法 **InterDiff**（Xu et al., ICCV 2023）。在 BEHAVE 数据集上，人体关节位置误差（MPJPE-H）从 140 降至 123（↓12.1%），物体平移误差（Trans.Err.）从 123 降至 106（↓13.8%），旋转误差（Rot.Err.）从 226 降至 200（↓11.5%）；尤为突出的是，穿透率（Pene.）从 164 大幅降至 94（↓42.7%），表明 CoopDiff 生成的交互在物理真实性上具有质的提升。消融实验进一步验证了解耦建模、接触注入、一致性约束以及人驱动交互模块各自的有效性，逐步叠加这些组件后所有指标持续改善。

## 背景与动机

### 问题背景

3D人-物交互（Human-Object Interaction, HOI）预测任务旨在根据历史观测，预测未来一段时间内人体和物体在三维空间中的运动轨迹。这一任务在机器人操作、虚拟现实、人机协作等场景中具有重要应用价值。然而，准确预测人-物交互面临一个核心挑战：**人体与物体的运动模式存在本质差异**。如Figure 1所示，人体关节高度结构化，不同关节的运动轨迹复杂且多样化；而物体通常仅涉及刚性平移和旋转，运动模式相对简单。这种动力学特性的显著差异使得联合建模两者变得困难。

### 现有方法缺口

当前主流方法（如**InterDiff**，Xu et al., ICCV 2023）采用单一扩散模型同时预测人体和物体的运动。这种联合建模策略忽视了人体与物体在动力学上的根本不同，导致以下问题：

- **预测精度不足**：单一模型难以同时捕捉高度结构化的人体运动和刚性的物体运动，导致人体关节位置误差（MPJPE-H）和物体平移/旋转误差较大。
- **交互真实感差**：联合建模缺乏对人-物接触关系的显式约束，导致预测结果中出现互穿透（interpenetration）、物体漂浮（object floating artifacts）、无接触情况下物体异常移动等不真实交互（Figure 6）。

### 核心洞察与动机

本文的核心洞察是：**人体和物体虽然具有不同的动力学特性，但通过共享的接触点可以实现联合一致的运动预测。接触点为解耦建模提供了天然的桥梁。** 基于这一洞察，本文提出CoopDiff框架，核心动机包括：

1. **解耦建模**：将人体和物体运动预测分解为两个独立分支，使每个分支专注于各自独特的运动模式。
2. **接触作为桥梁**：将人-物接触点作为共享锚点，同时注入两个分支，通过接触一致性约束对齐两者的预测，确保运动协调一致。
3. **人驱动交互**：将人体动态作为条件控制引入物体分支，模拟真实世界中“人操纵物体”的交互模式，进一步提升交互真实感。

## 核心创新

CoopDiff 的核心创新在于从根本上改变了人-物交互（HOI）运动预测的建模范式。现有方法（如 **InterDiff**, Xu et al., ICCV 2023）普遍采用单一扩散模型联合预测人体和物体的未来运动，这忽略了二者在运动模式上的本质差异：人体关节高度结构化且运动多样，而物体仅涉及刚性平移和旋转（见 Figure 1）。这种联合建模策略导致预测结果中出现大量不真实的交互，如相互穿透、物体漂浮或无接触下的物体移动。

CoopDiff 通过以下三个关键的 **changed slots** 系统性地解决了上述瓶颈：

**1. 运动预测模型架构：从单分支联合建模到双分支解耦扩散**

CoopDiff 将人体和物体的运动建模解耦为两个独立的扩散分支——人体动力学分支（Human Dynamics Branch）和物体动力学分支（Object Dynamics Branch），分别捕捉各自独特的运动模式。消融实验（Table 3）表明，仅引入解耦建模（Dcp）即可将 MPJPE-H 从基线 **InterDiff** 的 140 降至 133，验证了该设计的有效性。

**2. 接触信息利用方式：从无显式利用到作为共享锚点注入并施加一致性约束**

CoopDiff 将人-物接触点作为共享锚点，分别注入两个分支进行额外的接触预测。在此基础上，通过接触一致性约束（Contact Consistency Constraint, CCC）对齐两个分支预测的接触点，确保人体和物体的运动在接触区域保持连贯一致。损失函数定义为：

$$L_{consistency} = \sum_{i=1}^{T_p+T_f} M_i \odot \| \hat{C}_H^i - \hat{C}_O^i \|^2$$

在解耦并注入接触信息（Dcp+Cont）的基础上加入 CCC，使 MPJPE-H 从 130 进一步降至 126，穿透率（Pene.）从 97 降至 96（Table 3）。

**3. 人-物交互引导机制：从无显式引导到人驱动交互模块（HIM）**

为增强人-物运动之间的交互真实感，CoopDiff 设计了人驱动交互模块（Human-driven Interaction Module, HIM）。该模块将人体动力学分支学习到的动态知识作为条件控制，注入到物体动力学建模中，使物体运动更紧密地跟随人体操控。HIM 被构建为物体动力学模型的可训练副本，通过零初始化的全连接层将人体特征注入物体分支的中间特征。加入 HIM 后，模型达到最优性能（MPJPE-H 123），且在可视化中显著减少了轻微穿透并实现了更真实的接触（Figure 8）。

整体训练损失为三个损失的加权和：

$$L_{all} = \lambda_H L_{human} + \lambda_O L_{object} + \lambda_C L_{consistency}$$

此外，CoopDiff 采用了非对称的接触聚合设计——物体分支提前聚合接触信息，而人体分支不聚合——以适应二者不同的动态特性。消融实验（Table 4）证实，该非对称结构优于人体对齐或物体对齐的对称变体。

## 整体框架

CoopDiff 的整体框架围绕一个核心洞察构建：**人体与物体在运动模式上存在本质差异**——人体关节高度结构化且运动多样，而物体仅涉及刚性平移与旋转（见 Figure 1）。为应对这一差异，CoopDiff 采用**双分支扩散架构**，将人体运动与物体运动解耦至两个独立分支进行建模，同时以**人-物接触点作为共享锚点**桥接两个分支，确保运动预测的一致性。

![[assets/figures/papers/paper_list_l1677_CoopDiff_Anticipating_3D_Human_object_Interactions_via_Contact_consisten/figures/001_Figure_1.jpg]]
*Figure 1: Visualization results illustrating the difference between human and object dynamics in HOI. We visualize the motions of various human joints and object parts. Lines with varied colors indicate the trajectories of joints corresponding to human body and object. As shown, the articulated human body is highly structured with diverse movements across joints, whereas object motion typically involves rigid translations or rotations*

### 框架概览

框架由四个核心模块组成，其输入输出流如下（见 Figure 2）：

![[assets/figures/papers/paper_list_l1677_CoopDiff_Anticipating_3D_Human_object_Interactions_via_Contact_consisten/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of CoopDiff framework. CoopDiff employs a dual-branch diffusion to separately model the distinct motion patterns of humans and objects. For both branches, we additionally integrate contact points as shared anchors and feed them into branches for additional contact prediction. These contact predictions across branches are aligned with a consistency constraint to ensure coherent human-object dynamics modeling. To further enhance coherence between human-object dynamics, we devise a human-driven interaction module that incorporates human dynamics as conditional control to object dynamics modeling*

1. **人体动力学分支（Human Dynamics Branch）**：接收历史人体运动序列与接触点信息，预测未来人体姿态及人体侧的接触点位置。
2. **物体动力学分支（Object Dynamics Branch）**：接收历史物体刚性运动与接触点信息，预测未来物体的平移、旋转及物体侧的接触点位置。
3. **接触一致性约束（Contact Consistency Constraint, CCC）**：对齐两个分支预测的接触点，通过损失函数强制人体与物体在接触区域的空间一致性。
4. **人驱动交互模块（Human-driven Interaction Module, HIM）**：将人体分支学习到的动态特征作为条件控制注入物体分支，使物体运动受人体操控行为的引导。

### 数据流与模块关系

具体而言，给定一段历史观测的人-物交互序列，系统首先提取人体姿态 $h$、物体刚性运动 $o$（包含平移 $L_o$ 与旋转 $R$）以及接触点 $C$。两个分支在前向扩散过程中对各自输入加噪，随后通过 Transformer 解码器预测去噪后的干净运动。

- **人体分支**以加噪的 $[h_t, C_t]$ 为输入，经过 $L$ 层 Transformer 解码器，在历史条件 $\mathcal{E}_H(y_H)$ 的引导下重建干净的人体运动与接触点 $[h_0, C_0]$。
- **物体分支**以加噪的 $o_t$ 为输入，通过两个交叉注意力层分别融入历史信息和接触信息 $C^{1:T_p}$，再经线性投影输出干净物体运动 $o_0$。物体侧的接触预测 $\hat{C}_O$ 则由预测的旋转 $\hat{R}$ 与平移 $\hat{L}_o$ 结合真实接触点云 $p$ 计算得到：$\hat{C}_O = \hat{R} \cdot p + \hat{L}_o$。

两个分支的输出在**接触一致性约束**下进行对齐，损失函数为：
$$L_{\text{consistency}} = \sum_{i=1}^{T_p+T_f} M_i \odot \| \hat{C}_H^i - \hat{C}_O^i \|^2$$
其中 $M_i$ 为接触掩码，$T_p$ 和 $T_f$ 分别为历史与未来帧数。该约束确保人体与物体在接触区域的空间位置一致，从而缓解穿透与漂浮等不真实交互。

**人驱动交互模块（HIM）** 进一步强化人-物运动的耦合。HIM 是物体分支的可训练副本，其权重初始化为零。它将人体分支的中间特征通过全连接层 $Z$ 注入物体分支的每一层，使物体运动预测显式地依赖于人体动态。这种“人体作为操控者”的设计更贴合真实世界中的人-物交互场景。

### 训练目标

整体训练损失为三个子损失的加权和：
$$L_{\text{all}} = \lambda_H L_{\text{human}} + \lambda_O L_{\text{object}} + \lambda_C L_{\text{consistency}}$$
其中 $L_{\text{human}}$ 和 $L_{\text{object}}$ 分别为人体与物体分支的重建损失，$L_{\text{consistency}}$ 为接触一致性损失，$\lambda_H$、$\lambda_O$、$\lambda_C$ 为平衡系数。

### 关键设计选择

框架在接触信息的聚合方式上采用了**非对称结构**：物体分支提前聚合接触特征，而人体分支不做额外聚合。消融实验（Table 4）表明，这种非对称设计优于人体对齐或物体对齐的对称变体，验证了适应人体与物体各自动态特性差异的必要性。

## 核心模块与公式推导

### 3.1 数据表示

在介绍核心模块之前，首先明确运动预测任务的数据表示。给定观测到的人-物交互（HOI）历史序列，模型需要预测未来的人体和物体运动。

- **人体运动**：表示为 SMPL-H 模型的姿态参数序列，包含全局平移 $L_h$ 和关节旋转。
- **物体运动**：表示为刚性变换序列，包含物体质心平移 $L_o$ 和相对旋转 $R$。物体表面顶点 $V$ 可通过 $V = R \cdot P + L_o$ 计算，其中 $P$ 为物体点云。
- **接触点**：定义为人体表面与物体表面在交互过程中相互接触的点集，是连接两个分支的关键共享锚点。

### 3.2 人体动力学分支

人体动力学分支采用基于 Transformer 解码器的扩散模型架构，专门建模人体关节的高度结构化运动（Figure 3(a)）。

![[assets/figures/papers/paper_list_l1677_CoopDiff_Anticipating_3D_Human_object_Interactions_via_Contact_consisten/figures/003_Figure_3.jpg]]
*Figure 3: Contact-aware human and object dynamics branch*

**模块设计**：预测器 $\mathcal{D}_H$ 接收加噪后的人体运动与接触点的拼接向量 $[h_t, C_t]$ 作为输入，结合扩散时间步 $t$ 和人体条件编码 $\mathcal{E}_H(y_H)$（包含历史运动信息），通过 $L$ 层 Transformer 解码器逐步去噪，最终恢复干净的人体运动 $h_0$ 和人体侧接触点 $C_0$。

**训练损失**：人体分支的优化目标为最小化预测值与真实值之间的均方误差：

$$L_{human} = \| \mathcal{D}_H([h_t, C_t], t, \mathcal{E}_H(y_H)) - [h_0, C_0] \|^2 \quad \text{(Eq.1)}$$

其中 $h_t$ 和 $C_t$ 分别表示时间步 $t$ 的加噪人体运动和接触点，$h_0$ 和 $C_0$ 为对应的干净真实值。

### 3.3 物体动力学分支

物体动力学分支同样采用 $L$ 层 Transformer 预测器 $\mathcal{D}_O$，但针对物体仅涉及刚性平移和旋转的特性进行了专门设计（Figure 3(b)）。

**模块设计**：与人体分支不同，物体分支通过两个交叉注意力层分别注入历史物体运动信息和接触信息 $C^{1:T_p}$（来自人体分支预测的接触序列）。预测器从加噪物体运动 $o_t$ 出发，结合扩散时间步 $t$ 和物体条件编码 $\mathcal{E}_O(y_O)$，恢复干净物体运动 $o_0$。

**训练损失**：物体分支的优化目标为：

$$L_{object} = \| \mathcal{D}_O(o_t, t, C^{1:T_p}, \mathcal{E}_O(y_O)) - o_0 \|^2 \quad \text{(Eq.2)}$$

其中 $o_t$ 为加噪物体运动，$o_0$ 为干净真实值，$C^{1:T_p}$ 为从人体分支获取的接触点序列。

### 3.4 接触一致性约束

接触一致性约束（Contact Consistency Constraint, CCC）是桥接两个分支的核心机制。

**动机**：虽然两个分支独立建模人体和物体运动，但二者预测的接触点应在空间上保持一致——人体接触点和物体接触点应位于同一空间位置。

**实现**：物体侧接触点 $\hat{C}_O$ 通过预测的物体运动参数计算得到：$\hat{C}_O = \hat{R} \cdot p + \hat{L}_o$，其中 $p$ 为真实接触点。随后，通过加权掩码约束对齐两个分支的接触预测：

$$L_{consistency} = \sum_{i=1}^{T_p+T_f} M_i \odot \| \hat{C}_H^i - \hat{C}_O^i \|^2 \quad \text{(Eq.3)}$$

其中 $\hat{C}_H^i$ 和 $\hat{C}_O^i$ 分别为人体和物体分支在第 $i$ 帧预测的接触点，$M_i$ 为接触掩码（有接触区域为1，无接触区域为0），$T_p$ 和 $T_f$ 分别为历史和未来帧数。

### 3.5 人驱动交互模块

人驱动交互模块（Human-driven Interaction Module, HIM）将人体动力学知识显式注入物体运动建模，模拟真实场景中“人操控物体”的交互模式（Figure 4）。

![[assets/figures/papers/paper_list_l1677_CoopDiff_Anticipating_3D_Human_object_Interactions_via_Contact_consisten/figures/004_Figure_4.jpg]]
*Figure 4: The Human-driven Interaction Module (HIM). The modules Z in gray represent the Fully-Connected (FC) layers whose weights and bias are initialized to zeros*

**模块设计**：HIM 构造为物体动力学模型的可训练副本。具体而言，将人体分支 Transformer 解码器各层的中间特征提取出来，通过零初始化的全连接层（FC layer）$Z$ 进行线性变换后，逐层注入到 HIM 对应层的中间特征中。这种设计使得物体运动预测能够感知人体动态变化，从而生成更协调的交互运动。

### 3.6 整体训练损失

整个 CoopDiff 框架通过加权组合三个损失函数进行端到端训练：

$$L_{all} = \lambda_H L_{human} + \lambda_O L_{object} + \lambda_C L_{consistency} \quad \text{(Eq.4)}$$

其中 $\lambda_H$、$\lambda_O$、$\lambda_C$ 分别为人体动力学损失、物体动力学损失和接触一致性损失的权重系数。三个损失项共同优化，确保人体运动精度、物体运动精度以及二者之间的交互一致性。

## 实验与分析

### 主要结果

CoopDiff 在两个标准基准数据集上均取得了最优性能，尤其在交互真实感指标上优势显著。

在 BEHAVE 数据集上，CoopDiff 相较于先前最优方法 **InterDiff**（Xu et al., ICCV 2023）在所有评估指标上均实现大幅提升（Table 1）：人体关节位置误差 MPJPE-H 从 140 降至 123（↓12.1%），物体平移误差 Trans.Err. 从 123 降至 106（↓13.8%），物体旋转误差 Rot.Err. 从 226 降至 200（↓11.5%）。更为突出的是，穿透率 Pene. 从 164 降至 94，降幅高达 42.7%，表明 CoopDiff 生成的交互在物理合理性上远超现有方法。与 InterRNN、InterVAE、HO-GCN、CAHMP 等基线相比，CoopDiff 同样保持全面领先。

![[assets/figures/papers/paper_list_l1677_CoopDiff_Anticipating_3D_Human_object_Interactions_via_Contact_consisten/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons on the BEHAVE dataset (Bhatnagar et al. 2022). Text in bold denotes the best results. Our method significantly outperforms other approaches*

在 Human-Object Interaction（HOI）数据集上（Table 2），CoopDiff 在所有评估指标上均取得最佳结果：MPJPE-H 为 100（InterDiff 为 105），MPJPE-O 为 83（InterDiff 为 84），Trans.Err. 为 58（InterDiff 为 60），Rot.Err. 为 118（InterDiff 为 120）。虽然在该数据集上的提升幅度相对 BEHAVE 较小，但 CoopDiff 仍然一致优于所有对比方法，验证了其泛化能力。

![[assets/figures/papers/paper_list_l1677_CoopDiff_Anticipating_3D_Human_object_Interactions_via_Contact_consisten/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparisons on the Human-Object Interaction dataset (Wan et al. 2022). We evaluate the model on the test set that was not seen during training. Text in bold denotes the best results*

定性可视化（Figure 6）进一步揭示了 CoopDiff 的优势：InterDiff 的预测结果中频繁出现互穿透、物体漂浮以及无接触情况下物体异常运动等不真实交互（红框标注），而 CoopDiff 生成的交互更加准确和逼真。

![[assets/figures/papers/paper_list_l1677_CoopDiff_Anticipating_3D_Human_object_Interactions_via_Contact_consisten/figures/010_Figure_6.jpg]]
*Figure 6: Visualization of future interactions predicted by our method against InterDiff on the BEHAVE dataset. The results produced by InterDiff contain some unrealistic interactions (highlighted in red boxes), such as interpenetration, object floating artifacts, and moving objects in the absence of contact. In contrast, our CoopDiff generates more accurate and realistic interactions. The history and ground-truth HOIs are in gray and the predictions are in color. Best viewed in color*

### 消融实验

为验证各核心组件的贡献，论文在 BEHAVE 数据集上进行了逐步消融（Table 3），以 InterDiff 作为基线。

![[assets/figures/papers/paper_list_l1677_CoopDiff_Anticipating_3D_Human_object_Interactions_via_Contact_consisten/figures/009_Table_3.jpg]]
*Table 3: Quantitative analysis of key designs on BEHAVE. We investigate the effectiveness of Decoupled human-object dynamics modeling (Dcp), Contact injection (Cont) to dualbranch diffusion, Contact Consistency Constraint (CCC) and Human-driven Interaction Module (HIM). We report the results of InterDiff (Xu et al. 2023) as our Baseline*

**解耦建模（Dcp）**：仅将单一扩散模型替换为人体-物体双分支解耦架构，MPJPE-H 即从 140 降至 133，验证了分别建模人体结构化关节运动和物体刚性运动这一策略的有效性。

**接触注入（Cont）**：在解耦基础上向两个分支注入接触点信息，MPJPE-H 进一步从 133 降至 130，同时穿透率下降，表明接触信息作为共享锚点有助于提升运动预测精度。

**接触一致性约束（CCC）**：加入跨分支接触对齐损失后，MPJPE-H 从 130 降至 126，穿透率从 97 降至 96。该约束通过强制人体和物体分支预测的接触点一致，有效增强了人-物运动的协同性。

**人驱动交互模块（HIM）**：最终加入 HIM 后，所有指标达到最优（MPJPE-H 123），证明了将人体动态作为条件控制注入物体建模能够进一步提升交互真实感。Figure 8 的定性分析显示，HIM 模块减少了轻微穿透并促进了真实接触的实现。

**非对称结构设计**：Table 4 对比了三种变体——人体对齐对称结构、物体对齐对称结构以及 CoopDiff 的非对称结构（物体分支提前聚合接触信息、人体分支不聚合）。结果表明，非对称设计在所有指标上均优于两种对称变体，验证了根据不同动力学特性定制分支结构的必要性。

### 接触一致性建模对比

Figure 5 将 CoopDiff 的接触一致性建模与 CHOIS、HOI-Diff 以及直接对齐最近邻人-物点的方法进行了对比。CoopDiff 通过跨分支共享接触锚点并施加一致性约束，在接触区域实现了更连贯的人-物动态，优于其他接触引导方法。

![[assets/figures/papers/paper_list_l1677_CoopDiff_Anticipating_3D_Human_object_Interactions_via_Contact_consisten/figures/008_Figure_5.jpg]]
*Figure 5: Comparisons of our contact consistency modeling against other contact-guided approaches, including CHOIS (Li et al. 2024a), HOI-Diff (Peng et al. 2025), and direct alignment of the nearest human-object points1*

### 关键图表结论汇总

| 图表 | 核心结论 |
|------|---------|
| Table 1 | BEHAVE 上全面超越 InterDiff，穿透率降低 42.7% |
| Table 2 | HOI 数据集上所有指标均取得最优 |
| Table 3 | 解耦→接触注入→CCC→HIM 逐步增益，MPJPE-H 从 140 降至 123 |
| Table 4 | 非对称分支结构优于对称设计 |
| Figure 6 | 定性展示 CoopDiff 减少穿透、漂浮等不真实交互 |
| Figure 8 | HIM 模块促进接触区域真实交互，减少轻微穿透 |

![[assets/figures/papers/paper_list_l1677_CoopDiff_Anticipating_3D_Human_object_Interactions_via_Contact_consisten/figures/006_Table_4.jpg]]
*Table 4: Analysis of the asymmetric structure on BEHAVE dataset. CoopDiff with asymmetric structure outperforms human-aligned and object-aligned symmetric variants*

![[assets/figures/papers/paper_list_l1677_CoopDiff_Anticipating_3D_Human_object_Interactions_via_Contact_consisten/figures/012_Figure_8.jpg]]
*Figure 8: Visual analysis on mitigating unrealistic interactions. With our contact-consistent modeling, humans and objects exhibit more coherent dynamics near the contact regions. The HIM module further promotes realistic interactions, which reduces slight penetration and facilitates achieving authentic contact. The red dots denote visible contact points outputted by CoopDiff*

### 公平性说明

所有方法在相同的标准基准数据集（BEHAVE 和 HOI）上使用统一的训练/测试划分和评估指标进行对比，确保比较的公平性。

## 方法谱系与知识库定位

### 1. 核心瓶颈与因果机制

现有3D人-物交互（HOI）预测方法面临一个根本性瓶颈：**人体与物体在运动模式上存在显著差异**——人体关节高度结构化且运动多样，而物体仅涉及刚性平移和旋转（见Figure 1）。以往方法（如**InterDiff**, Xu et al., ICCV 2023）采用单一扩散模型联合预测两者运动，忽略了这种动力学差异，导致预测结果中出现穿透、物体漂浮等不真实交互。

CoopDiff的核心洞察在于：**人体和物体具有不同的动力学特性，但通过共享的接触点可以实现联合一致的运动预测**。接触点为解耦建模提供了天然的桥梁。基于此，CoopDiff引入了一个因果调节机制：
- **解耦建模**：分别构建人体动力学分支和物体动力学分支，各自捕捉其特有的运动模式；
- **接触锚点桥接**：将接触点作为共享锚点注入两个分支，并通过接触一致性约束（Contact Consistency Constraint, CCC）对齐两个分支的接触预测；
- **人驱动交互**：通过人驱动交互模块（Human-driven Interaction Module, HIM），将人体动态作为条件控制传递给物体分支建模。

消融实验（Table 3）系统验证了这一因果链的每个环节：逐步添加解耦（Dcp）、接触注入（Cont）、一致性约束（CCC）和HIM模块，所有指标持续改善，最终MPJPE-H从基线140降至123。

### 2. 方法谱系与基线关系

CoopDiff处于**基于扩散模型的HOI运动预测**这一方法谱系中，其直接对标与超越的核心基线是**InterDiff**（Xu et al., ICCV 2023）。下表梳理了CoopDiff与相关方法的关键差异：

| 方法 | 运动建模方式 | 接触信息利用 | 人-物交互引导 |
|------|-------------|-------------|---------------|
| **InterRNN** | 循环网络联合预测 | 未显式使用 | 无 |
| **InterVAE** | 变分自编码器联合预测 | 未显式使用 | 无 |
| **HO-GCN** | 图卷积联合预测 | 未显式使用 | 无 |
| **CAHMP** | 联合预测 | 未显式使用 | 无 |
| **InterDiff** (Xu et al., ICCV 2023) | 单一扩散模型联合预测 | 未使用接触点 | 无显式引导 |
| **CHOIS** (Li et al., 2024a) | 接触引导方法 | 接触引导生成 | 与本文接触一致性建模对比（Figure 5） |
| **HOI-Diff** (Peng et al., 2025) | 接触引导扩散 | 接触引导生成 | 与本文接触一致性建模对比（Figure 5） |
| **CoopDiff** (本文) | **双分支扩散解耦建模** | **接触点作为共享锚点+一致性约束** | **HIM模块将人体动态注入物体分支** |

CoopDiff相对于**InterDiff**的三个关键改进槽位：

1. **运动预测模型架构**：从单一扩散模型联合预测，转变为双分支扩散分别建模人体和物体运动（Sec. 3.2-3.3）。仅此解耦操作（Dcp only），MPJPE-H即从140降至133（Table 3），验证了解耦的有效性。

2. **接触信息利用方式**：从“未使用接触点或仅用于后处理校正”，转变为“接触点作为共享锚点注入两个分支，并施加一致性损失以桥接运动”（Sec. 3.4）。在解耦基础上注入接触信息（Dcp+Cont），MPJPE-H进一步从133降至130，穿透率同步降低。

3. **人-物交互引导机制**：从“无显式引导”，转变为“HIM模块将人体动态作为条件控制传递给物体分支建模”（Sec. 3.5）。加入HIM后，MPJPE-H最终降至123（Table 3）。

此外，CoopDiff还对比了其他接触引导方法如**CHOIS**和**HOI-Diff**（Figure 5），验证了其接触一致性建模的优越性。非对称结构消融（Table 4）表明，物体分支提前聚合接触信息、人体分支不聚合的非对称设计，优于对称变体，进一步验证了适应各自动态特性的必要性。

### 3. 适用边界与局限

根据论文提供的分析信息，CoopDiff在以下条件下表现出显著优势：
- **数据集**：在BEHAVE和Human-Object Interaction两个标准基准上均取得最优结果，使用统一的训练/测试划分和评估指标，确保了公平比较。
- **评估指标**：在人体关节误差（MPJPE-H）、物体平移误差（Trans.Err.）、旋转误差（Rot.Err.）和穿透率（Pene.）上全面超越InterDiff。尤其在BEHAVE数据集上，穿透率大幅降低42.7%（从164降至94），表明交互物理真实感显著提升。
- **定性表现**：可视化结果（Figure 6, Figure 8）显示CoopDiff预测的交互相比InterDiff具有更少的互穿透、物体漂浮和无接触物体运动。

**需注意的局限与开放问题**：当前分析中未提供论文明确指出的局限性或开放问题。以下为基于方法设计的合理推断，需读者结合原文验证：
- 双分支架构依赖接触点作为桥接锚点，在无接触或接触稀疏的交互场景（如人与物体仅有短暂、轻微接触）中，接触一致性约束的有效性可能下降。
- HIM模块将人体动态作为条件控制传递给物体分支，这一设计隐含假设人体是交互的主动驱动方。对于物体主动作用于人体的场景（如被物体撞击），该假设的适用性需进一步检验。
- 论文未报告在极端长时预测或高度动态交互场景下的性能退化分析，实际部署边界尚不明确。

### 4. 知识库定位

CoopDiff的核心贡献在于**将HOI运动预测从“联合建模”范式推进到“解耦-桥接”范式**，其方法论贡献可归纳为：

- **解耦建模思想**：认识到人体与物体的动力学差异，分别建模各自的运动模式，这一思想可推广至其他涉及异构智能体的交互建模任务。
- **接触作为桥接机制**：将接触点从单纯的交互表征提升为跨分支对齐的共享锚点，并通过一致性损失显式约束，为多智能体运动协调提供了新的技术路径。
- **人驱动交互模块**：通过将人体动态作为条件控制注入物体分支，实现了非对称的交互引导，这与真实世界中人类通常作为操控者的角色一致。

在HOI预测的知识图谱中，CoopDiff位于**扩散生成模型**与**物理感知交互建模**的交叉点，连接了运动预测、接触建模和交互真实感三个研究方向。其解耦-桥接框架为后续研究提供了可扩展的架构模板——例如，可替换分支内部的生成模型类型，或引入更精细的接触物理约束。

## 原文 PDF

![[paperPDFs/arxiv_2025/CoopDiff_Anticipating_3D_Human_object_Interactions_via_Contact_consistent_Decoupled_Diffusion.pdf]]