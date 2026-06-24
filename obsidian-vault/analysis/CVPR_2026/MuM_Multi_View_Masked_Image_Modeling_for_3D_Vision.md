---
title: "MuM: Multi-View Masked Image Modeling for 3D Vision"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MuM_Multi_View_Masked_Image_Modeling_for_3D_Vision.pdf
aliases:
- MuM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在训练中随机采样2至24个视图，统一施加75%的掩码率进行像素重建，并通过解码器中的交替帧注意力与全局注意力实现视图间信息交互。
primary_logic: 对称地将掩码图像建模扩展到任意多视图，无需指定参考视图即可隐式学习跨视图几何一致性；简单的像素重建目标配合多视图解码器，比语义导向的DINO系列更高效地训练出适用于3D视觉任务的几何特征。
claims:
- 在CO3Dv2、Re10K、MegaDepth多视图相机位姿估计中，MuM冻结编码器的AUC@30（71.5/50.8/73.0）大幅超越DINOv3（66.9/36.7/59.3）和CroCo v2（58.2/27.7/60.7）。
- 在DTU和ETH3D点云估计上，MuM冻结编码器的中值准确度（3.7/0.8）显著优于DINOv3（6.4/0.9）和CroCo v2（8.5/0.9）。
- 线性探测匹配中，MuM在MegaDepth-1500上达到EPE 10.2、鲁棒性94.2%，全面领先DINOv3（19.0/86.4）和CroCo v2（27.3/75.7）。
- 消融实验证明将MAE扩展为多视图是性能提升的关键（多视图MAE EPE 12.5 vs 单视图MAE 18.7）。
---

# MuM: Multi-View Masked Image Modeling for 3D Vision

> [!tip] 核心洞察
> 对称地将掩码图像建模扩展到任意多视图，无需指定参考视图即可隐式学习跨视图几何一致性；简单的像素重建目标配合多视图解码器，比语义导向的DINO系列更高效地训练出适用于3D视觉任务的几何特征。

| 字段 | 内容 |
|------|------|
| 中文题名 | MuM：面向3D视觉的多视角掩码图像建模 |
| 英文题名 | MuM: Multi-View Masked Image Modeling for 3D Vision |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.17309) · [Code](https://github.com/davnords/mum) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MuM |
| Dataset | CO3Dv2, Re10K, MegaDepth, DTU |

> [!tip] 效果简介
> - CO3Dv2 上，AUC@30 (↑) 71.5 vs 66.9 (DINOv3) (+4.6)。
> - Re10K 上，AUC@30 (↑) 50.8 vs 36.7 (DINOv3) (+14.1)。
> - MegaDepth (pose) 上，AUC@30 (↑) 73.0 vs 59.3 (DINOv3) (+13.7)。

## 概述

**问题瓶颈**：现有的自监督视觉预训练方法在3D感知任务中存在根本性局限。单视图掩码自编码器（如MAE）缺乏跨视图几何理解能力；而专为3D设计的跨视图方法（如CroCo v2）依赖严格的共视性采样和参考视图，难以推广到任意多视图场景。语义导向的DINO系列虽在识别任务上表现优异，但学习的特征在几何理解上不足。

**核心方法**：MuM（Multi-View Masked Image Modeling）将掩码图像建模对称地扩展到任意多视图。其核心设计包括：（1）训练中随机采样2至24个视图，所有视图统一施加75%掩码率进行像素重建；（2）通过解码器中交替的帧注意力与全局注意力实现视图间信息交互，无需指定参考视图；（3）采用按patch归一化的像素值作为重建目标。这种简洁的设计使模型能够隐式学习跨视图几何一致性。

**主要结果**：在冻结编码器评测下，MuM在多项3D视觉任务上大幅超越现有方法：
- **多视图相机位姿估计**（Table 2）：CO3Dv2上AUC@30达71.5（DINOv3 66.9），Re10K上达50.8（DINOv3 36.7），MegaDepth上达73.0（DINOv3 59.3）。
- **点云估计**（Table 3）：DTU中值准确度3.7（DINOv3 6.4），ETH3D上0.8（DINOv3 0.9）。
- **线性探测密集匹配**（Table 4）：MegaDepth-1500上EPE降至10.2（DINOv3 19.0），鲁棒性提升至94.2%（DINOv3 86.4%）。

值得注意的是，MuM的训练计算量约为DINOv3的1/30，却在下游3D任务中实现了全面超越。消融实验（Table 10）进一步证实，将MAE从单视图扩展为多视图是性能提升的关键因素（多视图MAE EPE 12.5 vs 单视图MAE 18.7）。

**方法定位**：MuM属于生成式自监督学习范式，以像素重建为核心目标。与语义导向的DINO系列形成互补——MuM在几何密集任务（位姿估计、点云重建、特征匹配）上优势显著，但在语义识别任务（图像分类、语义分割）上仍落后于DINOv3。该方法为3D视觉预训练提供了一条高效、可扩展的技术路径。

## 背景与动机

3D视觉感知——从多张图像中恢复场景的几何结构和相机位姿——是自动驾驶、机器人导航和增强现实等应用的核心能力。近年来，基于前馈神经网络的重建流水线（如VGGT、MapAnything）取得了显著进展，但这些系统的性能高度依赖于底层视觉编码器提取特征的质量。因此，自监督预训练一个能够理解多视图几何关系的通用视觉编码器，成为推动3D视觉发展的关键问题。

现有的自监督学习方法在这一目标上存在明显局限。以**MAE**（He et al., CVPR 2022）为代表的掩码图像建模方法仅处理单视图，无法学习跨视图的几何对应关系。**CroCo v2**（Weinzaepfel et al., ICCV 2023）将掩码重建扩展到双视图，但要求指定一个参考视图，并对两个视图施加非对称掩码（90%和0%），这种设计难以推广到任意数量的视图。另一方面，以**DINOv2**和**DINOv3**为代表的语义导向方法，虽然在大规模数据上学习到了强大的视觉表征，但其训练目标（实例判别或自蒸馏）天然倾向于语义理解而非几何推理，导致在3D任务上的表现并不理想。

核心瓶颈在于：**缺乏一种能够对称地处理任意多视图输入、无需指定参考帧、且以几何一致性为隐式学习目标的预训练框架**。这直接限制了冻结编码器在相机位姿估计、点云重建和密集特征匹配等下游3D任务上的表现。

MuM正是针对这一缺口提出的。其核心动机是：将掩码图像建模从单视图或双视图对称地推广到任意多视图，通过一个简洁的像素重建目标，强制模型在多视图解码过程中隐式学习跨视图的几何对应关系。与语义预训练路线相比，这一设计在计算效率上具有显著优势——据论文报告，MuM的训练计算量仅为DINOv3的约1/30，却在多项3D视觉任务上实现了超越。

## 核心创新

MuM 的核心创新在于将掩码图像建模（Masked Image Modeling, MIM）从单视图或双视图对称地推广到任意多视图场景，从而在自监督预训练中隐式学习跨视图的几何一致性。其关键设计变更（changed slots）如下。

**1. 任意多视图的统一掩码重建**

现有方法受限于固定的视图数量与不对称的掩码策略：**MAE**（He et al., CVPR 2022）仅处理单视图，而 **CroCo v2**（Weinzaepfel et al., ICCV 2023）虽引入跨视图重建，但要求严格的共视性采样，且采用非对称掩码（参考视图 0%，目标视图 90%），并依赖参考视图作为条件。MuM 打破了这一限制——在训练中随机采样 2 至 24 个视图，对所有视图统一施加 75% 的掩码率进行像素重建。这一对称设计无需指定参考视图，使模型能够从任意视角组合中学习几何结构，而非依赖特定的视图配对关系。

**2. 无参考视图的对称解码器架构**

CroCo v2 的解码器以参考视图为条件进行交叉注意力，本质上是一种非对称的信息流向。MuM 提出交替的帧注意力（frame attention）与全局自注意力（global self-attention）机制，在所有视图的可见 token 之间进行完全对称的信息交互。消融实验（Table 11c）证实了这一设计的关键性：引入未掩码参考视图并未带来增益（EPE 11.9 vs 无参考 10.6），反而可能引入不必要的归纳偏置。此外，交替注意力仅在解码器中使用有效，若用于编码器则性能大幅下降（Decoder EPE 10.6 vs Encoder 16.7, Table 11d），表明编码器独立处理各视图、解码器负责跨视图融合的分工是最优的。

**3. 归一化像素重建目标**

与 MAE 和 CroCo v2 直接预测原始像素值不同，MuM 将重建目标改为按 patch 归一化的像素值（减去均值、除以标准差）。这一简单的修改带来了显著的性能提升（w/ norm EPE 10.6 vs w/o norm 13.4, Table 11f）。其因果机制在于，归一化消除了不同 patch 之间的亮度和对比度差异，使模型更专注于学习几何结构而非光照等外观变化，这对于跨视图的几何一致性学习尤为关键。

**4. 计算效率的突破**

上述设计的综合效果是训练效率的大幅提升。MuM 的 MAE 风格目标相比 DINO 系列的自蒸馏框架在概念和计算上都更为简洁，训练速度提升超过 3 倍（Table 10 消融实验）。在 64 张 A100 GPU 上仅需约三天即可完成预训练，而下游 3D 视觉任务的性能全面超越计算开销大得多的 DINOv3（约 30 倍训练计算量差距）。这证明了在 3D 视觉领域，简单的像素重建目标配合适当的多视图架构设计，比语义导向的实例判别目标更为高效。

## 整体框架

MuM 的整体预训练流程围绕一个对称的多视图掩码自编码器展开，核心思路是将单视图 MAE 的“掩码-重建”范式对称地扩展到任意数量的视图中，通过解码器中的跨视图信息交互隐式学习几何一致性。图1给出了流程概览。

**输入与掩码。** 对于同一场景，训练时随机采样 $n \in [2, 24]$ 帧图像。每一帧独立地按 patch 施加统一的 75% 掩码率，得到部分可见图像 $\tilde{I}_i = \overline{M}_i \odot I_i$，其中 $\overline{M}_i = 1 - M_i$。与 CroCo 的非对称掩码（一个视图 90% 掩码、另一个视图 0% 掩码）不同，MuM 对所有视图采用相同的掩码率，且不指定任何参考视图。

**编码器。** 被掩码后的各视图图像 $\tilde{I}_i$ 独立地送入一个 ViT-L 编码器，各自提取标记嵌入。编码器阶段没有跨视图通信——每个视图的可见 patch 完全独立编码，这保证了编码器输出的特征对任意数量和顺序的输入视图具有排列不变性。

**多视图解码器。** 编码器输出的所有视图标记被联合送入一个 ViT-B 解码器。解码器由 6 层交替的“帧注意力”和“全局注意力”块组成：帧注意力在单个视图内部执行自注意力，全局注意力则允许所有视图的所有标记相互关注。这种交替设计使得解码器能够在保留单视图细节的同时，建立跨视图的对应关系，且整个过程无需指定参考视图，架构完全对称。

**预测头与重建目标。** 解码器的输出嵌入通过一个线性预测头映射到 RGB 像素空间。重建目标 $f(I_i)$ 并非原始像素值，而是对每个 patch 内的像素进行归一化（减去均值、除以标准差）后的值。最终损失为所有视图中被掩码 patch 的预测与归一化目标之间的平方误差之和：

$$\mathcal{L}(\theta) = \sum_{i=1}^{n} \| M_i \odot (\phi_\theta(\tilde{I}_i) - f(I_i)) \|^2$$

**训练数据与采样。** 预训练数据集混合了多个多视图数据集，总计约 1946 万帧（Table 1）。训练时按一定概率混入 ImageNet 单图数据，以保持编码器对单视图语义任务的泛化能力。在 64 块 A100 GPU 上完成预训练大约需要三天。

**与基线方法的关键差异。** 相比于 CroCo v2 以参考视图为条件的交叉注意力解码器，MuM 的交替帧/全局注意力架构消除了对参考视图的依赖，使其能够自然地处理任意数量的视图。相比于 DINOv3 的语义导向自蒸馏训练，MuM 的像素重建目标在概念和计算上都更简洁——消融实验表明，MAE 目标的训练速度比 DINO 系列快 3 倍以上，且在几何密集型下游任务上表现更优。

## 核心模块与公式推导

### 整体架构

MuM的预训练流程由四个核心模块串联构成，如Figure 1所示：掩码与训练采样器、ViT-L编码器、多视图ViT-B解码器、线性预测头。给定同一场景的一组图像，所有视图首先被统一掩码，随后独立通过编码器提取标记嵌入；这些嵌入在解码器中通过跨视图注意力进行联合交互，最终由线性头映射回像素空间并计算重建损失。

### 核心公式

多视图掩码重建的损失函数定义为所有视图中被掩码patch的归一化像素重建误差之和：

$$ \mathcal{L}(\theta) = \sum_{i=1}^{n} \| M_i \odot (\phi_\theta(\tilde{I}_i) - f(I_i)) \|^2 $$

其中：
- $n$ 为采样视图数量，训练时在2至24之间随机采样；
- $I_i$ 为第 $i$ 个视图的原始图像；
- $M_i$ 为二值掩码矩阵，指示哪些patch被掩码（值为1表示被掩码）；
- $\tilde{I}_i = \overline{M}_i \odot I_i$ 为部分可见图像，$\overline{M}_i = 1 - M_i$ 为掩码的补集；
- $\phi_\theta$ 为编码器-解码器网络，输出对每个patch的像素预测；
- $f(I_i)$ 为目标表示，对每个patch内的像素值减去均值并除以标准差进行归一化。

该公式的关键设计在于：**所有视图使用统一的75%掩码率**，且损失在**所有视图的所有被掩码patch上对称求和**，无需指定参考视图。这与CroCo的非对称掩码策略（一个视图90%掩码、另一个视图0%掩码）形成根本区别。

### 各模块详解

**掩码与训练采样器**负责构造每次迭代的输入。它从同一场景的视频序列中均匀采样 $n \in [2, 24]$ 帧图像，对每帧独立施加75%的随机patch掩码。此外，采样器按一定概率混入ImageNet单图数据，以保持语义特征的泛化能力。预训练数据混合的规模统计见Table 1，总计约1946万帧。

**ViT-L编码器**独立处理每个被掩码的视图。每个视图的可见patch经过线性投影和位置编码后，送入标准的ViT-L自注意力层。编码器**不包含任何跨视图交互**——各视图的计算完全独立，这保证了架构的对称性和对任意视图数量的兼容性。

**多视图ViT-B解码器**是跨视图信息交互的核心。它由6层交替的帧注意力（frame attention）和全局自注意力（global self-attention）块组成。帧注意力仅在单个视图内部的标记之间计算，而全局自注意力将所有视图的标记拼接后统一计算注意力。这种交替设计使得解码器能够在保留视图内局部结构的同时，建立跨视图的几何对应关系。消融实验表明，将交替注意力用于编码器会导致性能大幅下降（EPE从10.6升至16.7），证明跨视图交互应限定在解码器中。

**线性预测头**将解码器输出的每个被掩码patch的嵌入线性映射到RGB像素值，与归一化目标 $f(I_i)$ 计算平方误差。归一化目标的使用被消融实验证实为关键设计——未归一化目标的EPE从10.6升至13.4。

### 与基线的关键差异

| 设计维度 | MAE | CroCo v2 | MuM |
|---------|-----|----------|-----|
| 视角数量 | 单视图 | 双视图 | 2-24个视图（随机采样） |
| 掩码策略 | 75%掩码率 | 非对称（90%和0%） | 所有视图统一75%掩码率 |
| 跨视图交互 | 无 | 以参考视图为条件的交叉注意力 | 交替帧注意力与全局自注意力，无参考视图 |
| 重建目标 | 原始像素值 | 原始像素值 | 按patch归一化的像素值 |
| 参考视图依赖 | 无 | 必需 | 无，对称架构 |

### 蒸馏微调损失

在冻结编码器的前馈3D重建评估中，MuM采用知识蒸馏将VGGT教师模型的能力迁移到学生网络。其损失函数为：

$$ \mathcal{L}(\theta) = \sum_{i}^{n} \|\mathcal{P}_t - \mathcal{P}_s\|^2 + \|\mathcal{C}_t - \mathcal{C}_s\|^2 + \|\mathcal{D}_t - \mathcal{D}_s\|^2 $$

其中 $\mathcal{P}$、$\mathcal{C}$、$\mathcal{D}$ 分别为世界点坐标、相机参数和深度图，下标 $t$ 和 $s$ 分别表示教师和学生预测。该损失在预训练数据上以无权重L2误差形式计算，使冻结编码器的特征快速适应多视图重建任务。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2511_17309/figures/019_Figure_6.jpg]]
*Figure 6: Attention map for query patch. We visualize the global attention map in the decoder for a query patch. We find that the attention score is highest for matching patches*

## 实验与分析

### 核心发现：MuM在多视角3D任务上全面超越语义预训练基线

MuM在冻结编码器协议下的多视角3D重建任务上取得了对现有最强基线的一致领先。Table 2显示，在CO3Dv2、Re10K和MegaDepth三个基准的多视角相机位姿估计中，MuM的AUC@30分别达到71.5、50.8和73.0，显著超越**DINOv3**（66.9/36.7/59.3）和**CroCo v2**（58.2/27.7/60.7）。在DTU和ETH3D的点云估计任务上（Table 3），MuM冻结编码器的中值准确度分别为3.7和0.8，远优于DINOv3（6.4/0.9）和CroCo v2（8.5/0.9）。这些结果表明，简单的多视图像素重建目标在训练计算量仅约为DINOv3的1/30的条件下，能够学到更强的几何理解能力。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2511_17309/figures/006_Table_3.jpg]]
*Table 3: Pointcloud estimation. Reporting median accuracy and completeness on DTU and ETH3D*

在密集特征匹配任务上，MuM的优势同样突出。Table 4显示，在MegaDepth-1500的线性探测匹配中，MuM（64×A100配置）达到EPE 10.2和鲁棒性94.2%，全面领先DINOv3（19.0/86.4）和CroCo v2（27.3/75.7）。在RoMa密集匹配框架中（Table 5），MuM的100-PCK@1px为12.5，优于DINOv3的13.8。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2511_17309/figures/008_Table_5.jpg]]
*Table 5: Comparison on RoMa. Dense matching measured in 100-percentage correct keypoints (PCK) (lower is better)*

### 训练动态：几何能力与语义能力的分化

Figure 2揭示了MuM预训练过程中几何匹配能力和语义分割能力的分化趋势。在500K训练步数内，线性探测密集匹配性能（以EPE衡量）持续提升，而语义分割性能（以mIoU衡量）在早期达到峰值后趋于平稳甚至略有下降。这一动态说明，像素重建目标天然有利于几何特征的学习，但对语义特征的获取存在瓶颈——这解释了MuM在语义任务（Table 9，ImageNet-1K分类和ADE20K分割）上落后于DINOv3的根本原因。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2511_17309/figures/011_Table_9.jpg]]
*Table 9: Semantic tasks. We train an attentive probe on frozen features for classification (IN1K, accuracy), and evaluate semantic segmentation (ADE20K, mIoU) using logistic regression and k-NN. The performance of the pixel reconstruction objectives lag behind the highly semantic DINOv2 and v3 models*

### 消融实验：多视图扩展是性能提升的关键

Table 10的SSL目标消融直接验证了核心因果机制：将单视图MAE扩展为多视图MAE是性能提升的决定性因素。在MegaDepth上训练100K步后，多视图MAE的线性探测EPE为12.5，而单视图MAE高达18.7。相比之下，DINO和iBOT等语义导向目标在几何匹配上的表现明显更差（EPE分别为21.4和21.3）。这一消融确立了“多视图掩码重建”作为MuM方法有效性的根本来源。

### 架构设计消融：关键设计选择的影响

Table 11系统性地消融了MuM的架构和训练设计选择：

- **掩码率**：75%的掩码率效果最佳（EPE 10.6），65%和85%分别降至13.3和12.7。过低的掩码率使任务过于简单，过高则信息不足。
- **参考视图**：未掩码的参考视图并未带来增益，反而略微损害性能（w/ ref. EPE 11.9 vs w/o ref. 10.6），验证了MuM对称架构的合理性。
- **交替注意力位置**：仅在解码器中使用交替注意力有效（EPE 10.6），若用于编码器则性能大幅下降（EPE 16.7），说明编码器保持视图独立处理对特征学习至关重要。
- **位置编码**：现代轴向RoPE位置编码优于可学习绝对位置嵌入（EPE 10.6 vs 12.1）。
- **像素归一化**：按patch归一化（减去均值、除以标准差）的像素目标显著优于未归一化目标（EPE 10.6 vs 13.4）。

### 单视图任务：几何任务有增益，但未超越语义预训练

在单视图深度估计（Table 7）和表面法线估计（Table 8）上，MuM的性能介于DINOv3和CroCo v2之间。例如，在NYUd深度估计上，MuM的RMSE为0.41，优于CroCo v2（0.44）但不及DINOv3（0.37）。这表明像素重建目标对单视图几何任务也有一定增益，但实例判别损失的语义特征在这些任务上仍有优势。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2511_17309/figures/010_Table_7.jpg]]
*Table 7: Depth estimation with frozen features. We report performance when training a linear classifier on top of the frozen features. We report the RMSE metric on the 2 datasets*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2511_17309/figures/012_Table_8.jpg]]
*Table 8: Surface normal estimation. We estimate surface normals with a DPT probe, following Probe3D [24], and report percentage recall at different angular thresholds and RMSE*

### 失败模式与局限

1. **语义任务性能不足**：MuM在ImageNet-1K分类和ADE20K分割上明显落后于DINOv3（Table 9），因为像素重建目标天然不适合学习高层语义特征。
2. **直接余弦相似度匹配表现不佳**：在不需要线性探头的原始特征匹配中，MuM等生成式方法的特征不如DINOv3紧凑（Table 13），通常需要额外的线性探头才能释放潜力。
3. **单视图几何任务未能超越DINOv3**：尽管优于CroCo v2，MuM在深度和法线估计上仍不及语义预训练的DINOv3，说明多视图像素重建目标对单视图几何任务的迁移增益有限。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2511_17309/figures/002_Figure_2.jpg]]
*Figure 2: Training dynamics. Dense matching with a linear probe and semantic segmentation performance during 500K steps of training*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2511_17309/figures/005_Table_2.jpg]]
*Table 2: Multi-view camera pose estimation. Evaluating AUC@30 (Ò) for 10 random frames*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2511_17309/figures/007_Table_4.jpg]]
*Table 4: Comparison on dense feature matching through linear probing. End-point-error (EPE) and robustness (R) on MegaDepth-1500 [34, 52] and ScanNet-1500 [15, 46]*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2511_17309/figures/013_Table_10.jpg]]
*Table 10: SSL objective ablation. We evaluate different objectives by training each on MegaDepth for 100K steps and report linear probing matching performance. Reformulating MAE to multiple views is fast and gives robust matches. Time denotes the number of hours of training on an 8ˆA100 node*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2511_17309/figures/004_Table_1.jpg]]
*Table 1: Dataset mixture and sample sizes for MuM pre-training*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2511_17309/figures/009_Table_6.jpg]]
*Table 6: Two-view relative pose estimation. Comparing AUC@ for different encoders through finetuning*

## 方法谱系与知识库定位

### 与基线的差异化定位

MuM 的核心贡献在于将掩码图像建模（MIM）从单视图或双视图范式对称地推广到任意多视图场景，从而在几何理解能力上实现对现有自监督方法的系统性超越。其方法谱系可沿两条主线展开：**掩码自编码器**与**语义导向的自监督学习**。

**与 MAE 的关系**。MAE（He et al., CVPR 2022）奠定了高掩码率像素重建的预训练范式，但严格局限于单视图。MuM 将 MAE 的“编码器-解码器”架构继承并多视图化：编码器仍独立处理每个被掩码视图，解码器则通过交替的帧注意力与全局注意力实现跨视图信息交互。消融实验直接验证了这一扩展的关键性——将 MAE 改造为多视图后，密集匹配的 EPE 从 18.7 降至 12.5（Table 10），而完整的 MuM 进一步降至 10.6。这表明**多视图交互是性能跃升的主因，而非简单的目标函数改进**。

**与 CroCo v2 的关系**。CroCo v2（Weinzaepfel et al., ICCV 2023）是专为 3D 视觉设计的跨视图掩码重建方法，但其设计存在两个结构性限制：(1) 仅支持双视图，且要求严格的共视性采样；(2) 采用非对称掩码策略（参考视图 0% 掩码、目标视图 90% 掩码），以参考视图为条件的交叉注意力进行重建。MuM 在三个关键维度上突破了这些限制：

| 设计维度 | CroCo v2 | MuM |
|---------|----------|-----|
| 视角数量 | 双视图（固定参考视图） | 2–24 视图（无参考视图） |
| 掩码策略 | 非对称（0% / 90%） | 对称统一 75% |
| 跨视图注意力 | 以参考视图为条件的交叉注意力 | 交替帧注意力 + 全局自注意力 |

消融实验证实了这些设计选择的合理性：添加未掩码参考视图并未带来增益（EPE 11.9 vs. 无参考 10.6，Table 11c）；75% 掩码率优于 65% 和 85%（Table 11b）。对称架构使 MuM 无需指定参考视图即可隐式学习跨视图几何一致性，这是其能够泛化到任意多视图下游任务的结构性原因。

**与 DINO 系列的关系**。DINOv3 和 DINOv2 基于教师-学生自蒸馏框架，其实例判别损失天然适合学习语义特征，在图像分类和语义分割上表现卓越。MuM 在几何密集型任务（多视图位姿估计、点云重建、密集匹配）上全面超越 DINOv3，但在语义任务上明显落后（Table 9）。这揭示了两种预训练目标的根本性分工：**像素重建目标擅长学习几何结构，实例判别目标擅长学习语义类别**。值得注意的是，MuM 的训练计算量约为 DINOv3 的 1/30，却在 3D 任务上取得了更好的效果，凸显了简单重建目标在几何特征学习中的高效性。

### 适用边界

MuM 的优势集中在**需要跨视图几何理解的任务**上：

- **多视图前馈重建**：冻结编码器在 CO3Dv2、Re10K、MegaDepth 上的相机位姿估计（AUC@30 分别达 71.5、50.8、73.0）和 DTU、ETH3D 上的点云估计（中值准确度 3.7/0.8）均大幅领先 DINOv3 和 CroCo v2。
- **密集特征匹配**：线性探测下 MegaDepth-1500 的 EPE 达 10.2、鲁棒性 94.2%；在 RoMa 匹配器中替换编码器后，100-PCK@1px 降至 12.5。
- **双视图相对位姿估计**：微调后在不同数据集上均取得最优 AUC（Table 6）。

MuM 的**性能边界**同样清晰：

- **语义任务**：ImageNet-1K 分类和 ADE20K 语义分割上显著弱于 DINOv3（Table 9），因为像素重建目标无法提供实例级别的语义判别信号。
- **单视图几何估计**：在单视图深度估计和表面法线估计上，MuM 优于 CroCo v2 和 MAE，但不及 DINOv3（Table 7、Table 8），表明多视图预训练对单视图几何任务的迁移增益有限。
- **直接特征匹配**：在不使用线性探头的情况下，MuM 的原始特征在余弦相似度匹配中不如 DINOv3 紧凑（Table 13），说明生成式预训练的特征空间需要额外的适配层才能释放潜力。

### 局限与开放问题

**已明确的局限**：

1. **语义-几何跷跷板**：像素重建目标与语义理解之间存在固有张力。MuM 在语义任务上的落后并非训练不充分，而是目标函数本身的特性使然。这一局限在 Figure 2 的训练动态中清晰可见——密集匹配性能持续提升的同时，语义分割性能在后期趋于停滞甚至微降。

2. **特征紧凑性不足**：生成式自监督学习的特征通常需要线性探头或微调才能在下游任务中发挥最佳效果，直接使用余弦相似度进行匹配时表现不如判别式方法。这限制了 MuM 在零样本匹配等场景中的直接部署。

3. **大规模端到端验证缺失**：MuM 的评估主要基于冻结编码器或线性探测，尚未在 VGGT 级别的完整前馈重建流水线中进行端到端联合训练验证，其实际部署的计算效率和最终效果仍有待评估。

**开放问题**：

1. **几何-语义联合预训练**：能否将多视图掩码重建目标与自蒸馏框架（如 DINO）结合，在统一架构中同时获得强几何特征和丰富语义特征？Figure 2 中两条曲线的分化趋势暗示，简单的多任务联合训练可能存在目标冲突，需要更精细的损失平衡或阶段性训练策略。

2. **大规模重建流水线集成**：MuM 学到的特征直接嵌入 VGGT 或 MapAnything 等前馈重建流水线，是否能进一步提升大规模 3D 重建的质量？蒸馏微调实验（Table 2、Table 3 中 MuM† 行）已初步验证了这一方向，但完整的端到端训练仍有待探索。

3. **零样本跨视图匹配**：Figure 6 显示解码器的全局注意力图能够隐式定位匹配 patch，这是否意味着可以从注意力图中直接提取零样本匹配（类似 ZeroCo），从而避免复杂的后处理流程？这一方向有望将 MuM 从特征提取器升级为端到端的匹配器。

4. **规模扩展的边际收益**：进一步增加训练视图数量和模型规模，能否缩小在单视图几何估计任务上与 DINOv3 的差距？当前 MuM 在单视图任务上的表现介于 DINOv3 和 CroCo v2 之间，更大规模的预训练是否能够突破这一瓶颈尚不明确。

## 原文 PDF

![[paperPDFs/CVPR_2026/MuM_Multi_View_Masked_Image_Modeling_for_3D_Vision.pdf]]