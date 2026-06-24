---
title: "Plug, Play, and Fortify: A Low-Cost Module for Robust Multimodal Image Understanding Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Plug_Play_and_Fortify_A_Low_Cost_Module_for_Robust_Multimodal_Image_Understanding_Models.pdf
openreview_forum_id: 7KluEfmiXG
aliases:
- MWAMM
- PPFLCMRMIUM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "在频域中量化模态偏好（FRM），并根据该偏好动态调整每个模态在梯度更新或损失中的权重（MWAM），从而重新平衡优化过程。"
primary_logic: "模态之间的支配关系可以在频域中被有效识别和量化：模型决策主要依赖低频分量，因此富含低频信息的模态会在训练中占据主导地位。通过在梯度或损失空间中施加与FRM成反比的权重，可以抑制主导模态、提升弱势模态的学习，使模型优化轨迹更加均衡，从而显著提高缺失模态场景下的鲁棒性。"
claims:
- "缺失深度模态导致性能暴跌，甚至低于仅用RGB训练的单模态模型，证实某些模态被训练过程严重忽略。"
- "FRM与模态支配程度高度相关：模态组合的FRM越高，模型在该组合下的不同缺失场景中平均PCR越低。"
- "仅利用低频信息定义模态偏好会导致性能下降，证明高频分量不可忽略，验证了FRM设计的必要性。"
- "MWAM在各种任务（分割、分类、检测）、不同主干网络（CNN、ViT）以及多种模态组合上均能一致提升性能，降低PCR。"
---

# Plug, Play, and Fortify: A Low-Cost Module for Robust Multimodal Image Understanding Models

> [!tip] 核心洞察
> 模态之间的支配关系可以在频域中被有效识别和量化：模型决策主要依赖低频分量，因此富含低频信息的模态会在训练中占据主导地位。通过在梯度或损失空间中施加与FRM成反比的权重，可以抑制主导模态、提升弱势模态的学习，使模型优化轨迹更加均衡，从而显著提高缺失模态场景下的鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 即插即用与加固：面向鲁棒多模态图像理解的轻量级模块 |
| 英文题名 | Plug, Play, and Fortify: A Low-Cost Module for Robust Multimodal Image Understanding Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=7KluEfmiXG); [GitHub](https://github.com/a6103121/MWAM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Multimodal Weight Allocation Module (MWAM) |
| Dataset | BRATS2020 (脑肿瘤分割), NYU-Depth V2 (语义分割), CASIA-SURF (多模态分类), DroneVehicle (多模态检测) |

> [!tip] 效果简介
> - BRATS2020 (脑肿瘤分割) 上，Average Dice / Average PCR 为 GSS+MWAM: 87.56 / 4.44，对比 GSS: 86.41 / 5.30，变化 +1.15 / -0.86。
> - NYU-Depth V2 (语义分割) 上，Average MIoU / Average PCR 为 MMANet+MWAM: 45.81 / 12.66，对比 MMANet: 41.32 / 16.22 (推测baseline均值)，变化 +4.49 / -3.56。
> - CASIA-SURF (多模态分类) 上，Average Acc / Average PCR 为 SF-MD+MWAM (MMANet†): 97.03 / 2.02，对比 SF-MD: 92.85 / 5.43，变化 +4.18 / -3.41。

## 概述

多模态模型在训练中存在隐式的**模态偏好**：模型会偏向某些富含低频信息的模态，导致其他模态优化不充分。当这些“弱势”模态在推理时缺失，模型性能会发生**灾难性崩溃**——例如在CASIA-SURF数据集上，缺失深度模态时准确率暴跌至80.10%（-10.96），甚至低于仅用深度模态训练的单模态模型（97.29%）。这一现象揭示了训练过程中模态优化的严重失衡。

核心发现是：**模态间的支配关系可以在频域中被有效识别和量化**。模型决策主要依赖低频分量，因此低频信息丰富的模态会在训练中占据主导地位。基于此，本文提出**频率比率度量（Frequency Ratio Metric, FRM）**，通过计算低频与高频分量的L1比值来量化每个模态的偏好程度，并设计了**多模态权重分配模块（Multimodal Weight Allocation Module, MWAM）**——一个即插即用的轻量级模块，在训练过程中根据FRM动态调整各模态在梯度更新或损失函数中的权重，权重与FRM成反比，从而抑制主导模态、提升弱势模态的学习。

MWAM的核心优势在于：推理时完全拆离，不引入任何额外参数和计算；训练时仅增加可忽略的FLOPs和内存开销。实验覆盖分割、分类、检测、细粒度分类、动作识别等多种视觉任务，在CNN（RFNet、ResNet18）和ViT（mmFormer）架构上均验证有效。主要结果包括：BRATS2020脑肿瘤分割上GSS+MWAM平均Dice达87.56%（+1.15），PCR降至4.44（-0.86）；NYU-Depth V2语义分割上MMANet+MWAM平均MIoU提升4.49个百分点；CASIA-SURF多模态分类上平均准确率达97.03%（+4.18），PCR降至2.02（-3.41）；DroneVehicle多模态检测上mAP50从0.558提升至0.723。消融实验证实混合干预（梯度编辑+损失加权）效果最优，FRM的比率设计显著优于仅用低频或直接加和的规则。

## 背景与动机

### 多模态学习中的模态支配困境

多模态深度模型的核心优势在于融合不同传感器的互补信息。然而，训练过程中存在一个被长期忽视的瓶颈：模型会自发地偏爱某些模态，导致其他模态优化不充分。当这些“弱势”模态在推理时缺失，模型性能会发生灾难性崩溃——甚至劣于仅用剩余模态训练的单模态模型。

这一现象在CASIA-SURF数据集上得到了系统验证（Table 1）。以RGB+Depth+IR三模态联合训练的模型为例，当Depth模态缺失时，准确率从91.06%暴跌至80.10%（-10.96%），而单独使用Depth训练的单模态模型却能达到97.29%的准确率。这表明Depth模态在联合训练中几乎被完全忽略，模型过度依赖RGB和IR模态的决策信号。

### 频域视角下的模态偏好可量化性

为什么某些模态会在训练中占据主导地位？理论分析（Theorem 3.2）给出了关键线索：沿神经正切核（NTK）特征向量方向解耦时，训练收敛速率由对应特征值$\lambda_i$和学习率$\eta$决定：

$$\mathrm{Decay Rate} \propto (1 - \eta \lambda_{i})$$

大特征值对应低频函数，收敛更快。这意味着富含低频信息的模态会在优化过程中获得先发优势，进而主导共享梯度信号，形成“富者愈富”的马太效应。

实验证据直接支持这一论断。Figure 1展示了不同频率分量对模型训练的影响：保留低频信息的模态使训练损失下降更快、验证准确率更高；而仅保留高频分量的模态则优化缓慢、性能显著偏低。这揭示了一个核心洞察：**模态之间的支配关系可以在频域中被有效识别和量化**。

### 现有模态平衡方法的局限

针对模态偏好问题，已有方法主要分为两类：

- **梯度编辑方法**（如OGM-GE）：通过比较各模态分支的梯度差异，动态缩放梯度更新幅度。但其在空间域内通过特征级L1范数或梯度差异量化模态偏好，未能捕捉频域中低频主导与高频细节的结构性差异。
- **损失加权方法**（如LFM）：根据模态性能差异调整损失权重。但固定权重或启发式规则缺乏对模态偏好动态变化的适应性。

此外，现有方法通常仅在梯度或损失单一层面进行干预，缺乏系统性的多层面协同机制。

### 本文动机与核心思路

上述分析指向一个明确的研究缺口：**需要一种能够在频域中精确量化模态偏好，并据此动态调整优化过程的方法**。

本文提出频率比度量（Frequency Ratio Metric, FRM），通过在频域中计算低频与高频分量的比值，综合评估每个模态的偏好程度。基于FRM，设计即插即用的多模态权重分配模块（Multimodal Weight Allocation Module, MWAM），以与FRM成反比的权重在梯度编辑和损失加权两个层面同时干预训练过程，重新平衡各模态的优化轨迹，从而显著提升缺失模态场景下的鲁棒性。

该方法的关键优势在于：推理时完全拆离，不引入任何额外参数和计算开销；兼容CNN与ViT等多种主干架构；可无缝集成至现有缺失模态鲁棒方法中，进一步提升其性能上限。

## 核心创新

MWAM 的核心创新在于将模态偏好的量化与再平衡从空间域迁移至**频域**，并构建了三个相互耦合的 changed slots，形成“度量→权重→干预”的闭环。

### 1. 模态偏好量化域：从空间特征到频域 FRM

现有模态平衡方法（如 OGM-GE、LFM）通常在空间域内通过特征 L1 范数或梯度差异来感知模态主导程度。MWAM 的关键突破在于发现**模态支配关系可以在频域中被有效识别和量化**：模型决策主要依赖低频分量，因此富含低频信息的模态会在联合训练中占据主导地位（Figure 1 证实仅保留低频的训练损失更低，而仅保留高频的训练损失在约 30 epoch 即饱和）。

基于此，MWAM 引入**频率比度量（Frequency Ratio Metric, FRM）**：

$$FRM(x_{m_{i}}) = \sum_{a=0}^{w-1}\sum_{b=0}^{h-1} \left| \frac{ I_{m_{i}}^{low}(a,b) }{ I_{m_{i}}^{high}(w-1-a, h-1-b) + \sigma } \right|$$

该公式计算低频分量与高频分量（加稳定项 σ 防除零）的 L1 比值之和，同时兼顾低频主导性与高频细节信息。消融实验（Table 8）直接验证了这一设计的必要性：仅使用低频 L1 范数（Eq.3）的变体平均 Acc 比标准 MWAM 低 1.06%，而纳入高频比值的 FRM（Eq.4）高出标准基线 0.97%。

### 2. 权重分配机制：从固定/启发式到 FRM 驱动的动态反比权重

现有方法或采用固定权重，或基于启发式规则（如 OGM-GE 使用梯度比）进行干预。MWAM 的权重分配与 FRM 成**反比关系**——FRM 越高的模态（即富含低频信息的主导模态），获得的干预权重越低，从而抑制其主导性、提升弱势模态的学习强度。

具体实现上，MWAM 首先通过**FRM Bank** 对连续 mini-batch 的 FRM 序列进行指数移动平均平滑（Eq.2, ω=0.5），降低小批量波动对权重稳定性的影响：

$$\hat{F}_{m_{i}}^{j} = \begin{cases} F_{m_{i}}^{j} & j=0 \\ \omega \hat{F}_{m_{i}}^{j-1} + (1-\omega) F_{m_{i}}^{j} & j=1,..,nt-n \end{cases}$$

随后，将平滑后的 FRM 比例 T（当前模态 FRM 与所有模态平均 FRM 的比值，Eq.6）输入变形 sigmoid 函数（Eq.5），动态生成各模态的权重 $K_m$。Table 9 的参数敏感性分析表明，该函数对四个超参数在合理范围内不敏感（avg Acc 稳定在 95.87–97.08），具有良好的鲁棒性。

### 3. 干预层面：从单一干预到梯度-损失混合干预

现有方法通常仅在梯度层面（如 OGM-GE）或损失层面（如 LFM）进行单一干预。MWAM 将权重 $K_m$ **同时作用于梯度编辑和辅助头损失加权两个层面**（Figure 3），形成混合干预策略：

- **梯度编辑**：将 $K_m$ 应用于主干网络各模态分支的梯度更新，直接调控优化方向（参数无关）；
- **损失加权**：将 $K_m$ 加权于轻量辅助头的分类损失，从损失空间施加额外约束。

Table 5 的消融实验明确给出了混合干预的优势：混合策略平均 Acc 达 96.41、PCR 仅 2.97，优于纯梯度干预（95.93/3.09）和纯损失干预（96.06/3.61），证明两个干预层面具有互补性。

### 关键证据链

上述三个 changed slots 的创新性由以下决定性证据支撑：

1. **FRM 与模态支配力的因果关系**（Table 1）：模态组合的 FRM 越高（如 RGB+Depth+IR 达 $2.45\times10^{10}$），模型在缺失模态场景下的 PCR 越低；缺失 Depth 时 Acc 暴跌至 80.10%（-10.96），甚至低于仅用 Depth 训练的单模态模型（97.29%），证实训练中 Depth 被严重忽略。

2. **跨任务、跨架构的泛化性**（Tables 2–4, 12, 22）：MWAM 在分割（BRATS2020 Dice +1.15）、语义分割（NYU-Depth V2 MIoU +4.49）、分类（CASIA-SURF Acc +4.18）、检测（DroneVehicle mAP50 +0.165）和细粒度分类（Stanford Dogs +9.10）上均一致提升性能并降低 PCR，且兼容 CNN（RFNet, ResNet18）和 ViT（mmFormer）架构。

3. **推理零开销**（Table 6）：MWAM 在推理时完全拆离，不引入任何额外参数和计算，训练时仅增加可忽略的 FLOPs 和内存开销。

## 整体框架

![[assets/figures/papers/iclr26_0012_7KluEfmiXG_Plug_Play_and_Fortify_A_Low-Cost_Module_for_Robu/figures/005_Figure_2.jpg]]
*Figure 2: Architecture and application of our proposed MWAM. (a): Main structure of the MWAM. (b): FRM bank, designed to handle modality exceptions. Its update mechanism is governed by Eq. 2. (c): An illustration of the integration of MWAM into a multimodal host model. The calculation rules of FRM follow Eq. 4, which requires flipping and aligning the high-frequency components*

MWAM 是一种即插即用的训练期模块，其整体 pipeline 由三个核心阶段构成：**频域偏好量化**、**历史平滑与权重生成**、以及**训练干预**。该模块在推理时完全拆离，不引入任何额外参数或计算开销。

### 输入分块与频域变换

给定一个多模态输入样本，MWAM 首先对每个模态分支的输入图像进行分块处理：将图像切分为 $p \times p$ 的非重叠块（默认 $p=8$），对每个块应用离散余弦变换（DCT），将其从空间域映射到频域。随后，从每个变换后的块中提取左上角 $q \times q$ 区域作为低频分量，右下角 $q \times q$ 区域作为高频分量，并将所有块的低频/高频分量分别重组为全局频率特征图 $I_{m_i}^{low}$ 和 $I_{m_i}^{high}$。

### FRM 计算与平滑

基于提取的频率分量，MWAM 计算频率比度量（Frequency Ratio Metric, FRM），以量化每个模态在频域中的偏好程度：

$$FRM(x_{m_{i}}) = \sum_{a=0}^{w-1}\sum_{b=0}^{h-1} \left| \frac{ I_{m_{i}}^{low}(a,b) }{ I_{m_{i}}^{high}(w-1-a, h-1-b) + \sigma } \right|$$

该公式以低频与高频分量的 L1 比值之和作为模态偏好指标：富含低频信息的模态获得更高的 FRM 值，反映其在训练中更易占据主导地位。分母中的稳定项 $\sigma$ 防止除零。

由于单个 mini-batch 的 FRM 可能波动较大，MWAM 引入 FRM Bank 机制，通过指数移动平均对连续批次的 FRM 序列进行平滑：

$$\hat{F}_{m_i}^{j} = \begin{cases} F_{m_i}^{j} & j=0 \\ \omega \hat{F}_{m_i}^{j-1} + (1-\omega) F_{m_i}^{j} & j=1,..,nt-n \end{cases}$$

其中 $\omega=0.5$ 控制历史信息的保留程度，平滑后的 $\hat{F}_{m_i}^{j}$ 用于后续权重计算。

### 动态权重生成

基于平滑后的 FRM，MWAM 计算每个模态当前批次的相对比例 $T$：

$$T = \frac{\mathit{FRM}(x_{m_{i}}^{j})}{\frac{1}{M}\sum_{c=1}^{M} \mathit{FRM}(x_{m_{c}}^{j}) + \sigma}$$

随后通过变形 sigmoid 函数将 $T$ 映射为各模态的干预权重 $K_{m_i}$：

$$K_{m_{i}}^{j}(x_{m_{i}}^{j}) = \alpha - \frac{\beta}{1 + e^{-\lambda(T - \gamma)}}$$

权重与 FRM 成反比关系：FRM 越高的主导模态获得越小的权重，FRM 越低的弱势模态获得越大的权重，从而实现优化过程中的模态再平衡。

### 训练干预

MWAM 支持两种可选的训练干预机制（Figure 3），可单独或混合使用：

- **梯度编辑（参数无关）**：将权重 $K_{m_i}$ 直接作用于主干网络各模态分支的梯度更新，抑制主导模态的梯度、增强弱势模态的梯度。
- **辅助头损失加权**：在模型末端附加轻量级辅助分类头，以 $K_{m_i}$ 加权各模态分支的辅助损失，从损失空间引导优化方向。

消融实验（Table 5）表明，混合干预（梯度编辑 + 损失加权）效果最优：在 CASIA-SURF 数据集上平均 Acc 达 96.41、PCR 降至 2.97，显著优于纯梯度干预（95.93/3.09）和纯损失干预（96.06/3.61）。

### 与主模型集成

MWAM 作为一个独立模块，通过截获各模态分支的输入和梯度流与主模型集成（Figure 2c）。它不修改主模型的网络结构，仅需在训练循环中插入 FRM 计算和权重分配步骤。该方法已验证适配 CNN（RFNet、ResNet18）和 ViT（mmFormer）架构，兼容早期融合与晚期融合策略，并可进一步提升已有缺失模态鲁棒方法的性能上限。

## 核心模块与公式推导

### 3.1 模态偏好瓶颈的理论根源

多模态模型在完整数据上训练时，不同模态分支通过共享分类器耦合。当某一模态分支的优化信号显著强于其他分支时，该模态会主导共享梯度，导致弱势模态优化不充分。NTK理论分析表明，训练动态沿特征向量方向解耦后，收敛速率由对应特征值决定：

$$\mathrm{Decay Rate} \propto (1 - \eta \lambda_i)$$

大特征值对应低频函数，主导模态恰是富含低频信息的模态。这从理论上解释了模态偏好的成因，也为在频域中量化模态支配关系提供了依据。

### 3.2 MWAM整体架构

MWAM是一个即插即用的训练期模块，动态为多模态宿主模型的每个模态分支分配引导权重。其核心流程为：输入分块与DCT变换 → 低/高频分量提取 → FRM计算 → FRM Bank平滑 → 权重分配函数 → 训练干预。

**输入分块与DCT变换**：将每个模态的输入图像切分为 $p \times p$ 的非重叠块（默认 $p=8$），对每块应用离散余弦变换（DCT），获得频域表示。

**低/高频分量提取**：从每块的DCT系数中，提取左上 $q \times q$ 块作为低频成分 $I_{m_i}^{low}$，右下 $q \times q$ 块作为高频成分 $I_{m_i}^{high}$，重组为全局频率特征图。消融实验表明 $q=2$ 时性能最优。

### 3.3 频率比度量（FRM）——核心公式

模态偏好首先可直观定义为仅低频的L1范数（作为基线对比）：

$$MP(x_{m_i}) = \sum_{a=0}^{w-1}\sum_{b=0}^{h-1} | I_{m_i}^{low}(a,b) |$$

但仅用低频信息会导致性能下降（Table 8：平均Acc比标准MMANet低1.06%），因为完全忽略高频分量会丢失细节信息。因此提出综合考虑低频主导性与高频细节的频率比度量：

$$FRM(x_{m_i}) = \sum_{a=0}^{w-1}\sum_{b=0}^{h-1} \left| \frac{ I_{m_i}^{low}(a,b) }{ I_{m_i}^{high}(w-1-a, h-1-b) + \sigma } \right|$$

其中 $\sigma$ 为稳定项，防止除零。该度量以低频与高频的比值之和量化模态偏好：FRM越高，该模态在训练中的主导性越强。Table 8验证了该设计相比仅低频规则、直接加和、加权和等替代方案，平均Acc提升0.80%以上，PCR降低1.24以上。

### 3.4 FRM Bank——平滑更新机制

单批次的FRM存在波动，通过指数移动平均进行平滑以增强稳定性：

$$\hat{F}_{m_i}^{j} = \begin{cases} F_{m_i}^{j} & j=0 \\ \omega \hat{F}_{m_i}^{j-1} + (1-\omega) F_{m_i}^{j} & j=1,..,nt-n \end{cases}$$

其中 $\omega=0.5$ 控制历史权重，$nt$ 为总批次数，$n$ 为预热阶段批次数。平滑后的FRM用于后续权重计算。

### 3.5 动态权重分配函数

基于平滑FRM，首先计算当前模态FRM与所有模态平均FRM的比值：

$$T = \frac{\mathit{FRM}(x_{m_i}^{j})}{\frac{1}{M}\sum_{c=1}^{M} \mathit{FRM}(x_{m_c}^{j}) + \sigma}$$

随后通过变形sigmoid函数将比值 $T$ 映射为权重 $K_{m_i}$：

$$K_{m_i}^{j}(x_{m_i}^{j}) = \alpha - \frac{\beta}{1 + e^{-\lambda(T - \gamma)}}$$

其中 $\alpha$、$\beta$ 控制权重范围，$\lambda$ 控制陡峭度，$\gamma$ 控制偏移。权重与FRM成反比：FRM高的主导模态获得较小权重，FRM低的弱势模态获得较大权重，从而实现优化再平衡。超参数在合理范围内不敏感（Table 9：平均Acc稳定在95.87%-97.08%）。

### 3.6 训练干预机制

MWAM通过两种可选机制施加权重：

- **梯度编辑**：将权重 $K_{m_i}$ 应用于各模态分支的参数梯度更新，抑制主导模态的优化步长，放大弱势模态的梯度信号。该机制完全无参数。
- **损失加权**：通过轻量辅助头为每个模态分支计算独立损失，用 $K_{m_i}$ 加权后求和，从损失层面重新平衡优化目标。

消融实验（Table 5）表明，混合干预（梯度编辑+损失加权）效果最优：平均Acc 96.41、PCR 2.97，优于纯梯度干预（95.93/3.09）和纯损失干预（96.06/3.61）。推理时MWAM完全拆离，不引入任何额外参数或计算开销。

## 实验与分析

### 1. 模态偏好与性能崩溃的因果诊断

多模态模型在完整模态下训练后，面对缺失模态推理时会出现严重的性能崩溃。Table 1 在 CASIA-SURF 数据集上揭示了这一现象的核心因果链条：模型在训练过程中会系统性地偏爱某些富含低频信息的模态，导致其他“弱势”模态优化不充分；当这些弱势模态在推理时缺失，模型性能急剧下降，甚至劣于仅用该弱势模态训练的单模态模型。

![[assets/figures/papers/iclr26_0012_7KluEfmiXG_Plug_Play_and_Fortify_A_Low-Cost_Module_for_Robu/figures/001_Table_1.jpg]]
*Table 1: Analysis of model performance under various incomplete modality conditions on the CASIA-SURF dataset. Performance is quantified using Accuracy (Acc) and Performance Collapse Rate (PCR). Multi-modal refers to models trained on complete data but evaluated with missing modalities during inference. Uni-modal indicates models trained and evaluated using only a single modality. FRM is the Frequency Ratio Metric detailed in Section 4.2*

具体而言，当同时使用 RGB、Depth、IR 三种模态训练时，缺失 Depth 模态导致准确率暴跌至 80.10%（下降 10.96 个百分点），而仅用 Depth 训练的单模态模型却能达到 97.29% 的准确率。这一反直觉的现象证实：Depth 模态在联合训练中被严重忽略，模型并未真正学会利用其信息。相比之下，缺失 RGB 模态的性能下降幅度最小（仅 -0.48%），表明 RGB 模态主导了训练过程。

FRM（Frequency Ratio Metric）与模态支配程度高度相关。Table 1 显示：三种模态组合的 FRM 最高（2.45×10^10），对应最高的平均准确率和最低的平均 PCR；仅 RGB 模态的 FRM 最低，对应的平均性能也最差。这验证了 FRM 作为模态偏好量化指标的有效性。

### 2. 核心模块消融：干预层面与频率度量

Table 5 的消融实验明确了 MWAM 的最优干预策略。以 SF-MD 为基础框架，在 CASIA-SURF 数据集上比较四种配置：

![[assets/figures/papers/iclr26_0012_7KluEfmiXG_Plug_Play_and_Fortify_A_Low-Cost_Module_for_Robu/figures/015_Table_5.jpg]]
*Table 5: Impact of constraints at different levels on model performance metrics. We use SF-MD as the baseline framework and conduct experiments on the SURF dataset*

- **无 MWAM（w/o MWAM）**：平均 Acc 92.85%，PCR 5.43。
- **仅损失加权（Loss）**：平均 Acc 96.06%，PCR 3.61。
- **仅梯度编辑（Gradient）**：平均 Acc 95.93%，PCR 3.09。
- **混合干预（Hybrid, Loss+Gradient）**：平均 Acc **96.41%**，PCR **2.97**。

混合干预在准确率和鲁棒性上均优于任一单独干预策略。Figure 4 的训练损失曲线进一步佐证：混合干预的收敛过程更为稳定，损失下降轨迹平滑，避免了纯梯度或纯损失干预在训练后期的震荡。

Table 8 验证了 FRM 公式设计的必要性。在 MMANet 上比较四种频率度量规则：

![[assets/figures/papers/iclr26_0012_7KluEfmiXG_Plug_Play_and_Fortify_A_Low-Cost_Module_for_Robu/figures/019_Table_8.jpg]]
*Table 8: Comparison of the impact of FRM calculation rules on model performance. In the table, ”w/o MWAM” is vanilla MMANet, ”w/o High-Freq.” is in the form of an $L _ { 1 }$ -Norm sum using the low-frequency components, as in Eq. 3, ”w/ High-Freq.” is using our FRM as in $\mathrm { E q . 4 }$ , ”Direct $\mathbf { S u m } ^ { \mathbf { \mathfrak { S } } }$ is a directly summed $L _ { \mathrm { 1 } } \mathrm { - N o r m }$ of the low-frequency and high-frequency components, as shown in Eq. 27, and ”Weighted $\mathbf { S u m } ^ { \mathbf { \mathfrak { S } } }$ is the L1-Norm weighted sum of the low-frequency and high-frequency components, as shown in Eq. 28. All experiments were conducted in the same environme...

- **仅用低频（w/o High-Freq., Eq.3）**：平均 Acc 96.06%，PCR 3.61——甚至略低于不使用 MWAM 的基线（96.06% / 3.61），因为仅靠低频信息无法有效区分模态偏好。
- **直接求和（Direct Sum）**：平均 Acc 96.23%，PCR 3.26——提升有限。
- **加权求和（Weighted Sum）**：平均 Acc 96.21%，PCR 3.35——与直接求和相近。
- **频率比率法（w/ High-Freq., Eq.4）**：平均 Acc **97.03%**，PCR **2.02**——显著优于所有替代规则。

这证实了高频分量在模态偏好量化中不可忽略：仅关注低频会丢失模态间区分性信息，而比率法通过低-高频比值兼顾了低频主导性与高频细节，实现了最优的偏好度量。

Table 7 分析了频率采样窗口大小 q 的影响。q=2 时性能最优（avg Acc 97.03%）；q=1 时略低（96.99%），因为采样窗口过小导致高频信息不足；q=4 时性能退化至 96.06%，因为窗口过大引入了冗余信息。这表明适中的频率选择窗口对 FRM 的有效性至关重要。

### 3. 跨任务、跨架构的主结果验证

**脑肿瘤分割（BRATS2020）**：Table 2 显示，MWAM 在三种不同基础模型上均能一致提升性能。以 GSS 为例，集成 MWAM 后平均 Dice 从 86.41 提升至 87.56（+1.15），平均 PCR 从 5.30 降至 4.44（-0.86）。值得注意的是，GSS+MWAM 的性能超越了 LS3M 等更复杂的方法，表明 MWAM 作为一种轻量级插件可进一步提升已有鲁棒方法的上限。

![[assets/figures/papers/iclr26_0012_7KluEfmiXG_Plug_Play_and_Fortify_A_Low-Cost_Module_for_Robu/figures/008_Table_2.jpg]]
*Table 2: Performance comparison of multimodal robust solutions on BRATS2020 dataset. † denotes the integration of our proposed MWAM with the corresponding base model. Bold and italics indicate the best value and the second best value for each row in turn. Due to space constraints, we present only a subset of the comparison results here. More results are provided in Table 15, which includes several advanced methods, including HeMIS , Robust Seg, M3AE, LS3M, and A2FSeg*

**语义分割（NYU-Depth V2）**：Table 3 显示，MMANet+MWAM 的平均 MIoU 达到 45.81（基线约 41.32），平均 PCR 降至 12.66（基线约 16.22）。ESANet-MD+MWAM 同样获得显著增益，验证了 MWAM 在实时分割架构上的兼容性。

**多模态分类（CASIA-SURF）**：Table 4 显示，SF-MD+MWAM（以 MMANet† 表示）的平均 Acc 达到 97.03%，PCR 降至 2.02，相比 SF-MD 基线（92.85% / 5.43）提升显著。

![[assets/figures/papers/iclr26_0012_7KluEfmiXG_Plug_Play_and_Fortify_A_Low-Cost_Module_for_Robu/figures/010_Table_4.jpg]]
*Table 4: Performance comparison of multimodal robust solutions on SURF dataset. Due to space constraints, we present only a subset of the comparison results here. Comprehensive results are provided in Appendix A.14*

**目标检测（DroneVehicle）**：Table 12 显示，T-yolov8n+MWAM 的平均 mAP50 达到 0.723，相比基线（0.558）提升 0.165，验证了 MWAM 在检测任务上的有效性。

**细粒度分类**：Table 22 显示，ResNet18+MWAM 在 Stanford Dogs 上达到 47.27%（基线 38.17%），在 FGVC Aircraft 上达到 70.29%（基线 56.51%），分别提升 9.10 和 13.78 个百分点。

**动作识别（视频-光流）**：Table 11 显示，MWAM 在视频-光流双模态分类任务上优于 OGM-GE 和 LFM 等模态平衡方法，进一步验证了跨模态泛化能力。

### 4. 计算开销与鲁棒性分析

Table 6 的计算开销分析表明：MWAM 在推理时完全拆离，不引入任何额外参数和计算；训练时仅增加可忽略的 FLOPs 和内存开销。这确保了 MWAM 作为即插即用模块的实用性。

Table 10 的批量大小鲁棒性实验显示：即使在 batch size=1 的极端情况下，MWAM 仍能维持正常训练（avg Acc 75.77%，PCR -0.32），表明 FRM 银行的历史平滑机制（Eq.2）有效缓解了小批量带来的度量波动。

Table 9 的参数敏感性分析表明：权重分配函数（Eq.5）的四个超参数在合理范围内对性能影响不敏感，avg Acc 稳定在 95.87%-97.08% 之间，降低了实际部署中的调参负担。

### 5. 失败模式与已知局限

尽管 MWAM 在多数场景下表现鲁棒，但分析揭示了以下局限：

1. **初始状态敏感性**：MWAM 在从头训练时增益显著，但在利用预训练权重微调时提升幅度较小。这表明 FRM 的初始估计质量影响后续权重分配的有效性。
2. **极端高频噪声退化**：当输入经过大幅平滑滤波时，高频信息被严重抑制，FRM 的分母趋近于零（即使有 σ 稳定项），导致偏好度量失效，方法可能退化至接近基线的性能。
3. **固定超参数限制**：Eq.5 中的 α、β、λ、γ 在所有任务中保持固定，未根据训练阶段或任务特性自适应调整，可能限制了进一步提升的空间。

## 方法谱系与知识库定位

### 问题定位：模态偏好导致的鲁棒性坍塌

多模态学习中的一个隐蔽瓶颈在于：训练过程中，模型会自发地偏向某些富含低频信息的“易学”模态，导致其他模态的编码器优化严重不足。当这些被忽视的“弱势”模态在推理时缺失，模型性能会发生剧烈坍塌——甚至劣于仅用剩余模态训练的单模态模型。Table 1 给出了一个典型证据：在 CASIA-SURF 数据集上，完整模态训练的多模态模型在缺失深度模态时准确率暴跌至 80.10%（下降 10.96 个百分点），而仅用深度模态训练的单模态模型却能达到 97.29%。这直接证实了某些模态在训练过程中被系统性忽略。

MWAM 的核心洞察在于：这种模态间的支配关系可以在**频域**中被有效识别和量化。模型决策主要依赖低频分量（Figure 1 显示，保留低频信息的配置训练损失更低），因此富含低频信息的模态会在训练中占据主导地位。通过在梯度或损失空间中施加与频域偏好度量成反比的权重，可以抑制主导模态、提升弱势模态的学习，使模型优化轨迹更加均衡。

### 与现有模态平衡方法的关系

MWAM 并非孤立的解决方案，而是对现有模态平衡方法体系的系统性改进。其差异化体现在三个关键维度：

**1. 模态偏好量化域：从空间域到频域。** 早期方法如 OGM-GE 在空间域内通过梯度差异量化模态偏好，LFM 则直接在损失层面进行启发式平衡。MWAM 将量化域迁移至频域，通过频率比度量（FRM, Eq.4）同时捕捉低频主导性与高频细节。Table 8 的消融实验验证了这一设计的必要性：仅使用低频信息（Eq.3）会使平均准确率下降 1.06%，而完整的 FRM 设计（Eq.4）比标准 MMANet 高出 0.97%。这证明高频分量不可忽略，单纯的低频度量会导致信息损失。

**2. 权重分配机制：从固定/启发式到动态反比映射。** OGM-GE 使用梯度比作为权重依据，本质上是一种启发式规则。MWAM 在每个 mini-batch 根据 FRM 动态计算权重（Eq.5, Eq.6），权重与 FRM 成反比，并通过 FRM Bank 的历史平滑（Eq.2, ω=0.5）增强稳定性。Table 5 的消融实验表明，这种动态反比映射与混合干预策略结合时效果最优。

**3. 干预层面：从单一到混合。** 现有方法通常仅对梯度（如 OGM-GE）或仅对损失（如 LFM）进行干预。MWAM 可选地在梯度编辑和辅助头损失加权两个层面同时干预。Table 5 显示，混合干预（Hybrid）的平均准确率达 96.41、PCR 仅 2.97，优于纯梯度干预（95.93/3.09）和纯损失干预（96.06/3.61）。Figure 4 的训练损失曲线进一步佐证了混合策略的收敛优势。

### 作为插件式增强模块的定位

MWAM 的设计哲学是“即插即用与加固”（Plug, Play, and Fortify），这意味着它不替代现有方法，而是作为增强模块提升已有方案的上限。这一特性在多处实验中得到了验证：

- **BRATS2020 脑肿瘤分割**：GSS 本身已是先进的鲁棒分割方法，集成 MWAM 后平均 Dice 从 86.41 提升至 87.56，PCR 从 5.30 降至 4.44（Table 2）。GSS+MWAM 的组合甚至超越了 LS3M 等更复杂的方法（Table 15）。
- **NYU-Depth V2 语义分割**：MMANet+MWAM 的平均 MIoU 达到 45.81，PCR 降至 12.66，显著优于 MMANet 基线（Table 3）。
- **CASIA-SURF 多模态分类**：SF-MD+MWAM（即 MMANet†）的平均准确率达 97.03，PCR 仅 2.02，较 SF-MD 基线的 92.85/5.43 有大幅提升（Table 4）。
- **跨架构验证**：MWAM 同时适配 CNN（RFNet, ResNet18）和 ViT（mmFormer）架构，兼容早期融合与晚期融合策略（Table 2, Table 22）。

### 适用边界与任务泛化

MWAM 的适用边界已通过多任务、多模态组合的广泛实验得到初步界定：

**已验证的任务类型**：语义分割（BRATS2020, NYU-Depth V2）、多模态分类（CASIA-SURF）、目标检测（DroneVehicle，Table 12）、细粒度分类（Stanford Dogs, FGVC Aircraft，Table 22）、视频动作识别（视频-光流，Table 11）。在 DroneVehicle 检测任务上，T-yolov8n+MWAM 的 mAP50 达到 0.723，较基线提升 0.165（Table 12）；在细粒度分类上，ResNet18+MWAM 在 Dogs 和 Aircraft 上分别提升 9.10 和 13.78 个百分点（Table 22）。

**已验证的模态组合**：RGB-Depth、RGB-Depth-IR、RGB-红外、视频-光流、多光谱等。Table 13-14 进一步对比了 MWAM 与其他模态平衡方法在成对模态场景下的表现。

**推理时零开销**：MWAM 在推理时完全拆离，不引入任何额外参数和计算。Table 6 显示，训练时仅增加可忽略的 FLOPs 和内存开销，推理耗时测量针对的是 MWAM 模块隔离状态。

### 已知局限与开放问题

尽管 MWAM 在多个维度上表现出一致性增益，但其设计仍存在若干已知局限和待探索的开放问题：

**1. 频域解耦粒度不足。** FRM 模块目前仅通过整体频率比度量模态偏好，未能显式解耦每个模态内部的频域贡献分布。这意味着当某个模态同时包含大量低频和高频信息时，FRM 可能无法精确反映其真实的“易学性”。如何进一步解耦模态内部的频率成分，从而更精确地诊断和消除模态偏好，仍是一个开放问题。

**2. 权重分配函数的自适应性。** Eq.5 采用固定超参数（α, β, λ, γ），尽管 Table 9 的参数敏感性分析表明在合理范围内性能稳定（avg Acc 95.87-97.08），但这些参数可能需要根据任务或训练阶段自适应调整。能否将固定缩放因子替换为可学习或自适应的机制，是进一步提升性能的潜在方向。

**3. 预训练权重的初始状态敏感性。** MWAM 在从头训练时增益显著，但在利用预训练权重微调时提升幅度较小。这暗示 FRM 的初始估计可能受到预训练模型已有偏好的影响。如何缓解 MWAM 对初始训练状态的敏感性，使其在预训练权重上也能获得稳定增益，是一个待解决的实际问题。

**4. 极端高频噪声下的退化风险。** 当输入数据经过大幅平滑或存在极端高频噪声干扰时，FRM 的分母项可能不稳定，导致权重分配策略退化。Table 18-21 和 Figure 10 展示了不同滤波器类型和核大小下的性能变化，暗示需要更精细的频率选择性来应对极端场景。

**5. 大规模模态数量的可扩展性。** 当前实验主要覆盖 2-3 种模态组合。当模态数量超过三种或模型规模极大时，FRM 的计算效率和分配策略是否仍然有效，尚未得到验证。批量大小消融（Table 10）显示 MWAM 在 batch size=1 时仍能维持正常训练（avg Acc 75.77），但模态数量增加带来的 FRM Bank 管理复杂度仍是一个开放问题。

**6. 频率采样窗口的理论最优性。** Table 7 显示 q=2 时性能最佳（avg Acc 97.03），q=1 略低（96.99），q=4 性能退化（96.06）。这一经验最优值是否具有任务无关的普适性，还是需要根据数据特性自适应选择，缺乏理论指导。

## 原文 PDF

![[paperPDFs/ICLR_2026/Plug_Play_and_Fortify_A_Low_Cost_Module_for_Robust_Multimodal_Image_Understanding_Models.pdf]]
