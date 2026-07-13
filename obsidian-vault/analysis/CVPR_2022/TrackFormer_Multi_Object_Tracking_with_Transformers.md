---
title: "TrackFormer: Multi-Object Tracking with Transformers"
type: paper
paper_level: A
venue: CVPR
year: 2022
pdf_ref: paperPDFs/CVPR_2022/TrackFormer_Multi_Object_Tracking_with_Transformers.pdf
project_link: null
code_link: https://github.com/timmeinhardt/trackformer
aliases:
- TrackFormer
tags:
- CVPR_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/segmentation
core_operator: "引入自回归的 track queries，在 Transformer 解码器中通过注意力同时完成新目标检测（object queries）和已有目标的帧间关联（track queries），从而将数据关联转化为纯注意力操作。"
primary_logic: "将多目标跟踪建模为集合预测问题，利用 Transformer 的自注意力和编解码注意力，以静态对象查询检测新目标，以自回归轨迹查询在时间上传播身份和位置，实现端到端的检测与跟踪一体化，避免了额外的显式匹配、图优化或运动/外观建模。"
claims:
- "TrackFormer 通过注意力在帧间实现数据关联，演化一组跟踪预测贯穿整个视频序列。"
- "自回归的 track queries 嵌入了对象的空间位置和身份，从而在空间和时间上跟踪对象。"
- "TrackFormer 在 MOT17 和 MOT20 上取得了公共检测和私有检测的最优性能，并在 MOTS20 上取得了最优分割跟踪结果。"
- "MOT17 (public) 上 MOTA = 62.3"
---

# TrackFormer: Multi-Object Tracking with Transformers

> [!tip] 核心洞察
> 将多目标跟踪建模为集合预测问题，利用 Transformer 的自注意力和编解码注意力，以静态对象查询检测新目标，以自回归轨迹查询在时间上传播身份和位置，实现端到端的检测与跟踪一体化，避免了额外的显式匹配、图优化或运动/外观建模。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TrackFormer：基于Transformer的多目标跟踪 |
| 英文题名 | TrackFormer: Multi-Object Tracking with Transformers |
| 会议/期刊 | CVPR 2022 |
| Links | [paper](https://arxiv.org/abs/2101.02702) · [GitHub](https://github.com/timmeinhardt/trackformer) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/segmentation |
| Method | TrackFormer |
| Dataset | MOT17 (public), MOT17 (private), MOT20 (private), MOTS20 (private) |

> [!tip] 效果简介
> - MOT17 (public) 上，MOTA 为 62.3，对比 60.5 (CenterTrack)，变化 +1.8。
> - MOT17 (private) 上，MOTA 为 74.1，对比 67.8 (CenterTrack)，变化 +6.3。
> - MOT20 (private) 上，MOTA 为 68.6，对比 67.1 (GSDT)，变化 +1.5。

## 概要

多目标跟踪（MOT）的核心瓶颈在于检测与数据关联的割裂：传统方法将二者视为两个独立步骤，依赖手工设计的图优化或显式的外观/运动模型进行帧间匹配，缺乏一种统一的全局注意力机制来同时处理轨迹的初始化、身份保持与轨迹形成。TrackFormer（CVPR 2022）将多目标跟踪重新建模为集合预测问题，以Transformer的自注意力和编解码注意力统一检测与关联，从而消除了显式匹配、图优化及额外运动/外观建模的需求。

其核心机制是引入自回归的**track queries**：静态的object queries在每一帧中检测新出现的目标，而track queries则从上一帧的有效检测输出嵌入中继承身份与空间位置，通过Transformer解码器的交叉注意力在相邻帧特征上传播轨迹。这一设计将数据关联转化为纯粹的注意力操作，使模型能够端到端地同时完成目标检测与跟踪。

在MOT17和MOT20基准上，TrackFormer在公共检测与私有检测设置下均取得了当时的最优性能——私有检测下MOT17 MOTA达74.1（较CenterTrack提升6.3点），MOT20 MOTA达68.6；在MOTS20分割跟踪任务上也以54.9的MOTSA取得最优结果。消融实验表明，移除自回归注意力关联机制会导致IDF1骤降14.1点，验证了track queries的核心作用。该方法将MOT从“先检测后关联”的管道式范式推向了一体化的注意力跟踪范式，为后续基于Transformer的跟踪研究奠定了基础。



多目标跟踪（MOT）旨在从视频序列中定位所有感兴趣目标，并为其分配一致的身份标识，形成完整的时空轨迹。该任务在自动驾驶、视频监控和行为分析等场景中具有核心地位。传统上，MOT 被分解为两个独立步骤：首先在每帧中检测目标，然后通过数据关联将检测结果连接成轨迹。这种“检测后跟踪”（tracking-by-detection）范式长期主导了领域发展。

然而，这种分离式架构存在根本性瓶颈。数据关联步骤通常依赖手工设计的启发式规则或后处理优化——例如基于中心距离的贪婪匹配（如 **CenterTrack**，Zhou et al., ECCV 2020）、基于图神经网络的全局优化（如 **MPNTrack**，Braso & Leal-Taixe, CVPR 2020）、或基于外观相似度的准稠密匹配（如 **QuasiDense**，Pang et al., CVPR 2021）。这些方法将检测与关联视为解耦的模块，缺乏一种统一的注意力机制来同时处理新目标的初始化、已有目标的身份保持和轨迹的连续形成。具体而言，现有范式存在以下缺口：

1. **检测与关联割裂**：检测器输出的置信度和定位精度无法直接指导关联决策，关联模块也无法反向优化检测特征，导致信息流动单向且不充分。
2. **显式匹配的脆弱性**：贪婪匹配或图优化依赖于预定义的距离度量或外观模型，在密集场景、遮挡或快速运动条件下容易产生身份切换（ID switch）和轨迹碎片化。
3. **时序建模不足**：大多数方法仅利用当前帧特征进行检测，时序信息仅通过独立的外观或运动模型间接引入，缺乏端到端的时序特征融合机制。

近年来，Transformer 架构在目标检测中展现了强大的集合预测能力，通过自注意力和交叉注意力直接输出无序的检测集合，省去了非极大值抑制等后处理步骤。这启发了一个关键问题：**能否将多目标跟踪同样建模为集合预测问题，使数据关联本身成为注意力操作的自然产物？**

TrackFormer（CVPR 2022）正是在这一动机下提出的。其核心洞察是：将多目标跟踪转化为一个端到端的集合预测任务，利用 Transformer 解码器中的自回归轨迹查询（autoregressive track queries）在帧间传播目标身份和位置信息，从而将检测初始化、身份保持和轨迹关联统一为纯注意力机制，彻底消除了对显式匹配、图优化或独立外观/运动模型的依赖。



## 核心方法与创新机理

TrackFormer 的核心创新在于将多目标跟踪重新建模为**集合预测问题**，并引入**自回归 track query** 机制，使数据关联从显式的后处理步骤转变为 Transformer 解码器内部的纯注意力操作。这一设计从根本上改变了跟踪流程中检测与关联的耦合方式，形成了以下三个关键范式转换。

### 从检测后关联到注意力内关联

传统方法（如 **CenterTrack**（Zhou et al., ECCV 2020）、**MPNTrack**（Braso & Leal-Taixe, CVPR 2020））将多目标跟踪分解为两个独立步骤：先进行逐帧目标检测，再通过贪婪距离匹配或图优化完成帧间关联。TrackFormer 则通过自回归 track queries 在 Transformer 解码器中直接完成帧间关联——track query 携带前一帧目标的空间位置与身份信息，通过编解码交叉注意力在当前帧特征中寻找对应目标，无需任何后处理匹配步骤。消融实验表明，移除 track queries 并改用中心距离贪婪匹配后，MOTA 下降 3.0 点，IDF1 下降 14.1 点，验证了注意力关联机制的关键作用（Table 3）。

### 从独立初始化到自回归身份传播

在轨迹初始化方面，传统方法依赖每帧独立检测，再通过人工规则或匹配算法将检测结果串联为轨迹。TrackFormer 则采用双轨查询机制：**静态 object queries** 负责检测场景中新出现的目标，其输出嵌入随后被转换为下一帧的 **track queries**，自回归地延续身份。这一设计使得轨迹初始化、身份保持和帧间关联被统一在同一 Transformer 解码过程中，形成了“检测即跟踪”的闭环。

### 从单帧特征到双帧时序注意力

在时序建模方面，传统方法通常仅使用当前帧特征，或通过独立的外观/运动模型进行时序建模。TrackFormer 将前一帧与当前帧的特征图沿通道维度堆叠，并施加时间编码，使 queries 通过交叉注意力同时访问两帧特征。结合 track queries 的动态可变形参考点（根据前一帧边界框中心调整），模型能够在特征空间中显式地推理目标的时空位移，从而在拥挤场景下更稳定地保持身份一致性。



TrackFormer 将多目标跟踪建模为一个集合预测问题，通过编码器-解码器 Transformer 架构实现端到端的检测与跟踪一体化。其核心思想在于：将数据关联转化为 Transformer 解码器中的纯注意力操作，从而避免传统方法中检测与关联分离所带来的手工后处理步骤。

### 核心处理流程

TrackFormer 的在线跟踪流程分为四个连续步骤：

1. **CNN 骨干网络特征提取**：采用 ResNet-50 对每一帧图像独立提取特征图。
2. **Transformer 编码器**：对帧级特征图施加自注意力编码，生成具有全局上下文感知能力的增强帧表示。
3. **Transformer 解码器（含双类型查询）**：通过自注意力和编解码注意力解码两类查询嵌入——**静态 object queries** 负责检测新进入场景的目标，**自回归 track queries** 负责在帧间传播已有目标的身份与位置信息。解码器同时访问堆叠的前一帧与当前帧特征图，并通过时间编码区分两帧特征。
4. **MLP 预测头**：将解码器输出嵌入映射为边界框坐标和类别分数。

### 输入输出流

- **输入**：相邻两帧图像（帧 $t-1$ 和帧 $t$）。
- **查询初始化**：
  - *Object queries*：固定数量的可学习嵌入，用于在任意帧检测新目标。
  - *Track queries*：由上一帧有效目标检测的输出嵌入初始化而来，携带目标的身份和空间位置信息。对于 track queries，其可变形参考点会根据前一帧边界框中心进行动态调整。
- **输出**：每帧的目标边界框、类别预测及关联的身份标识。可选的**分割头**从编码特征和解码器输出嵌入生成空间注意力图，经上采样和卷积操作后输出实例级掩码预测。

### 训练范式

TrackFormer 在相邻两帧上训练，一次性优化整个 MOT 目标。训练过程分为两步：
1. 在帧 $t-1$ 上使用 $N_{\text{object}}$ 个 object queries 进行目标检测；
2. 在帧 $t$ 上使用全部 $N = N_{\text{object}} + N_{\text{track}}$ 个查询，同时完成对帧 $t-1$ 已检测目标的跟踪和新目标的检测。

这种设计使得模型能够在统一的 Transformer 框架内联合学习目标检测、轨迹初始化和帧间身份保持，无需额外的图优化或显式运动/外观建模。

### 补充图表

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2101_02702/figures/002_Figure_2.jpg]]
*Figure 2: TrackFormer casts multi-object tracking as a set prediction problem performing joint detection and tracking-by-attention. The architecture consists of a CNN for image feature extraction, a Transformer [51] encoder for image feature encoding and a Transformer decoder which applies self- and encoder-decoder attention to produce output embeddings with bounding box and class information. At frame t = 0 , , the decoder transforms $N _ { \mathrm { o b j e c t } }$ object queries (white) to output embeddings either initializing new autoregressive track queries or predicting the background class (crossed). On subsequent frames, the decoder processes the joint set of $N _ { \mathrm { o b j e c t } }$ +...



### 3.1 轨迹的集合预测建模

TrackFormer 将多目标跟踪形式化为集合预测问题。一条轨迹被定义为按时间排序的边界框序列：

$$T _ { k } = ( b _ { t _ { 1 } } ^ { k } , b _ { t _ { 2 } } ^ { k } , \dots )$$

其中 $b_t^k$ 表示第 $k$ 个身份在 $t$ 帧的边界框。模型的核心任务是在每一帧同时完成新目标的检测和已有目标的身份延续。

### 3.2 双查询机制：Object Queries 与 Track Queries

TrackFormer 的 Transformer 解码器接收两类查询嵌入：

- **静态 object queries**：固定学习得到的 $N_{\text{object}}$ 个查询，负责在任意帧检测新进入场景的目标。这些查询在每一帧保持相同的编码，使模型能够从零开始初始化轨迹。
- **自回归 track queries**：由上一帧的有效目标检测输出嵌入初始化，携带目标的空间位置和身份信息。每个新目标检测将其对应的输出嵌入传递给下一帧，形成自回归的跟踪查询。

这种设计的关键在于：track queries 的变形注意力参考点会根据上一帧边界框中心动态调整，使得交叉注意力能够聚焦于目标在下一帧可能出现的位置区域。

### 3.3 训练目标与匹配代价

训练在两帧相邻图像上进行，分两步计算损失：首先在 $t-1$ 帧用 object queries 进行目标检测，然后在 $t$ 帧用全部 $N = N_{\text{object}} + N_{\text{track}}$ 个查询同时完成跟踪和新目标检测。

对于未被 track identity 匹配的真值对象，通过最小代价注入映射分配给 object queries：

$$\hat{\sigma} = \underset{\sigma}{\arg \operatorname*{min}} \sum_{k_i \in K_{\mathrm{object}}} \mathcal{C}_{\mathrm{match}}(y_i, \hat{y}_{\sigma(i)})$$

成对匹配代价由类别概率和边界框代价组成：

$$\mathcal{C}_{\mathrm{match}} = -\lambda_{\mathrm{cls}} \hat{p}_{\sigma(i)}(c_i) + \mathcal{C}_{\mathrm{box}}(b_i, \hat{b}_{\sigma(i)})$$

边界框代价为 L1 距离与广义 IoU 代价的加权和：

$$\mathcal{C}_{\mathrm{box}} = \lambda_{\ell_1} ||b_i - \hat{b}_{\sigma(i)}||_1 + \lambda_{\mathrm{iou}} \mathcal{C}_{\mathrm{iou}}(b_i, \hat{b}_{\sigma(i)})$$

总损失为所有输出预测的损失之和：

$$\mathcal{L}_{\mathrm{MOT}}(y, \hat{y}, \pi) = \sum_{i=1}^{N} \mathcal{L}_{\mathrm{query}}(y, \hat{y}_i, \pi)$$

其中 $\pi$ 表示 track queries 与真值身份之间的固定匹配关系（由上一帧继承），$\mathcal{L}_{\mathrm{query}}$ 对已匹配的 track query 和通过 $\hat{\sigma}$ 匹配的 object query 分别施加分类和边界框回归损失。

### 3.4 时序特征融合

解码器的交叉注意力同时访问前一帧和当前帧的特征图。两帧特征图堆叠后施加时间特征编码，使查询能够区分来自不同帧的特征。这一设计让 track queries 在单次注意力操作中完成跨帧信息聚合，无需额外的运动模型或显式特征对齐。

### 3.5 分割跟踪扩展

当扩展到多目标跟踪与分割（MOTS）任务时，TrackFormer 在解码器输出嵌入和编码器图像特征之间生成空间注意力图，经上采样和卷积操作后得到实例级掩码预测。值得注意的是，MOTS 版本使用原始 DETR 注意力而非变形注意力，原因是单尺度特征图下变形注意力的稀疏采样会导致分割掩码质量下降。



## 实验与关键发现

### 核心实验设置

TrackFormer 的实验评估覆盖三个主流基准：MOT17、MOT20（多目标跟踪）和 MOTS20（多目标跟踪与分割）。模型采用 ResNet-50 作为 CNN 骨干，Transformer 编码器-解码器架构基于 Deformable DETR（Zhu et al., ICLR 2021）构建。训练在两帧相邻图像上进行，一次性优化整个 MOT 目标函数。对于私有检测设置，模型在 CrowdHuman 数据集上预训练后，在 MOT17 和 MOT20 训练集上微调；对于公共检测设置，直接使用官方提供的检测结果，并通过最小 IoU 阈值过滤低质量检测来初始化跟踪。分割跟踪扩展（MOTS）则使用原始 DETR 的全局注意力替代可变形注意力，原因是稀疏的可变形注意力图在单尺度特征图上生成的分割掩码质量较差，且全局注意力在单尺度下的内存消耗更可控。

### 主实验结果

**Table 1** 汇总了 TrackFormer 在 MOT17 和 MOT20 测试集上的表现，区分了公共检测与私有检测两种设定。在 MOT17 公共检测设定下，TrackFormer 取得 62.3 MOTA，较 **CenterTrack**（Zhou et al., ECCV 2020）的 60.5 提升 1.8 点；在私有检测设定下，TrackFormer 达到 74.1 MOTA，显著超越 CenterTrack 的 67.8（+6.3 MOTA），同时优于 **QuasiDense**（Pang et al., CVPR 2021，68.7 MOTA）、**FairMOT**（Zhang et al., IJCV 2021，73.7 MOTA）和 **MPNTrack**（Braso & Leal-Taixe, CVPR 2020，58.8 MOTA）等方法。在 MOT20 私有检测设定下，TrackFormer 以 68.6 MOTA 超越 **GSDT**（Wang et al., 2021）的 67.1，取得最优性能。

分割跟踪方面，**Table 2** 显示 TrackFormer 在 MOTS20 测试集上达到 54.9 MOTSA，较 **Track R-CNN**（Voigtlaender et al., ICCV 2019）的 52.6 提升 2.3 点，同样为当时最优。

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2101_02702/figures/007_Table_2.jpg]]
*Table 2: Comparison of multi-object tracking and segmentation methods evaluated on the MOTS20 [52] train and test sets. We indicate methods which first perform tracking-by-detection (TbD) on SDP [62] detections and then apply a Mask R-CNN [17]. Table 3. Ablation study on TrackFormer components. We report MOT17 [30] training set private results on a 50-50 frame split. The last row without (w$\o$) all components is only trained for object detection and associates tracks via greedy matching as in [69]*

**公平性注意**：公共检测设定下，TrackFormer 与 CenterTrack 均对检测结果进行了过滤——TrackFormer 使用最小 IoU 要求，CenterTrack 使用中心距离过滤。**Table A.1** 的对比表明，在 TrackFormer 上使用 IoU 过滤替代中心距离过滤后，IDF1 从 61.0 提升至 63.4（+2.4 点），说明过滤策略的选择对公平比较有实质影响。

### 消融实验

**Table 3** 在 MOT17 训练集的 50-50 帧划分上进行了系统的组件消融，揭示了几个关键发现：

**自回归注意力关联的核心作用**：移除 track queries 并改用中心距离贪婪匹配后，MOTA 下降 3.0 点，IDF1 更是骤降 14.1 点。这直接证明了基于 Transformer 注意力的帧间关联机制是 TrackFormer 性能的核心驱动力，远非简单的后处理匹配所能替代。

**轨迹重识别机制的有效性**：加入 track query 重识别（re-identification）模块后，IDF1 提升 1.4 点。该机制允许模型在短时遮挡后通过注意力重新找回丢失的轨迹，虽然提升幅度有限，但验证了在 Transformer 框架内嵌入身份保持能力的可行性。

**分割联合训练的影响**：**Table 4** 展示了在 MOTS20 训练集上联合训练跟踪与分割的效果。结果表明，联合训练不仅使模型具备了分割能力，还对纯跟踪指标产生了积极影响，说明分割任务提供的像素级监督信号有助于学习更鲁棒的目标表示。

### 失败模式与局限性

尽管 TrackFormer 在多个基准上取得了最优性能，其设计仍存在若干可识别的失败模式：

1. **两帧训练窗口的限制**：模型仅在相邻两帧上训练，缺乏对更长时序上下文的显式建模能力。这导致在长时间遮挡或大幅非线性运动场景下，track queries 的自回归传播可能累积误差，造成轨迹中断或身份切换。

2. **重识别的短时局限**：轨迹查询的重识别机制仅适用于短时遮挡场景。对于目标消失超过数帧后重新出现的长时丢失情况，模型缺乏有效的全局重识别能力，难以恢复原有身份。

3. **公共检测设定的依赖**：在公共检测设定下，TrackFormer 需要额外的 IoU 过滤步骤来抑制低质量检测，这不仅引入了超参数敏感性，也使得与其他方法的直接对比变得复杂——不同方法采用的过滤策略差异可能影响性能排序。

4. **数据需求较高**：模型依赖 CrowdHuman 等大规模目标检测数据集进行预训练，对训练数据的规模和多样性有较高要求，在标注数据稀缺的场景下迁移能力可能受限。

### 关键图表结论

- **Figure 1（概览图）**：展示了 TrackFormer 如何通过 object queries 和自回归 track queries 在 Transformer 中联合推理轨迹初始化、身份保持和时空轨迹，是理解“tracking-by-attention”范式的最佳入口。
- **Figure 2（架构图）**：详细说明了从 CNN 特征提取、Transformer 编码器编码、到解码器通过两类查询进行集合预测的完整流程，以及两帧训练的两步损失计算策略。
- **Table 3（消融表）**：是理解各组件贡献的核心证据，尤其揭示了注意力关联对 IDF1 的决定性影响（14.1 点的降幅），远大于对 MOTA 的影响。
- **Figure 3（定性对比）**：在 MOTS20 上对比了 TrackFormer 与 Track R-CNN 的分割跟踪效果，直观展示了 Transformer 方法在遮挡和拥挤场景下的身份保持优势。

### 补充图表

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2101_02702/figures/010_Table.jpg]]
*Table: A.2. We report private TrackFormer results on each individual sequence evaluated on the MOT17 test set. To follow the official MOT17 format, we display the same results per public detection set. The arrows indicate low or high optimal metric values. Table A.3. We report TrackFormer results on each individual sequence and set of public detections evaluated on the MOT17 test set. We apply our minimum Intersection over Union (IoU) public detection filtering. The arrows indicate low or high optimal metric values*

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2101_02702/figures/003_Table_1.jpg]]
*Table 1: Comparison of multi-object tracking methods on the MOT17 [30] and MOT20 [13] test sets. We report private as well as public detection results and separate between online and offline approaches. Both TrackFormer and Center-Track filter tracks by requiring a minimum IoU with public detections. For a detailed discussion on the fairness of such a filtering, we refer to the appendix. We indicated additional training Data: CH=CrowdHuman [45], PD=Parallel Domain [50], 6M=6 tracking datasets as in [66], JTA [14], M=Market1501 [67] and C=CUHK03 [27]. Runtimes (FPS) are self-measured*


![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2101_02702/figures/006_Table_4.jpg]]
*Table 4: We demonstrate the effect of jointly training for tracking and segmentation on a 4-fold split on the MOTS20 [52] train set. We evaluate with regular MOT metrics, i.e., matching to ground truth with bounding boxes instead of masks*



![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2101_02702/figures/012_Table.jpg]]
*Table: A.4. We report private TrackFormer results on each individual sequence evaluated on the MOT20 test set. The arrows indicate low or high optimal metric values*

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2101_02702/figures/013_Table.jpg]]
*Table: A.5. We present TrackFormer tracking and segmentation results on each individual sequence of the MOTS20 test set. MOTS20 is evaluated in a private detections setting. The arrows indicate low or high optimal metric values. Table A.6. We report the original per-sequence CenterTrack MOT17 test set results with Center Distance (CD) public detection filtering. The results do not reflect the varying object detection performance of DPM, FRCNN and SDP, respectively. The arrows indicate low or high optimal metric values*



## 定位与知识库关联

### 1. 与基线方法的关系

TrackFormer 的核心贡献在于将多目标跟踪重新定义为集合预测问题，从而将检测与数据关联统一到单一 Transformer 架构中。这一设计使其与当时主流的跟踪范式形成明确对比。

**相对于 tracking-by-detection 基线**：传统方法如 **Tracktor++** (Bergmann et al., ICCV 2019) 和 **CenterTrack** (Zhou et al., ECCV 2020) 将检测与关联解耦。Tracktor++ 利用检测器的回归能力在帧间传播边界框，但需额外训练 ReID 模型进行身份保持；CenterTrack 通过中心点位移回归和贪婪距离匹配实现关联。TrackFormer 的 track queries 以自回归方式在解码器中通过注意力完成关联，避免了启发式贪婪匹配或额外 ReID 网络。在 MOT17 私有检测设置下，TrackFormer 的 MOTA 达到 74.1，较 CenterTrack 的 67.8 提升 6.3 点。

**相对于图优化基线**：**MPNTrack** (Braso & Leal-Taixe, CVPR 2020) 将跟踪建模为图上的最小代价流问题，通过消息传递网络学习关联。**GSM** (Liu et al., IJCAI 2020) 则利用图相似度模型进行匹配。TrackFormer 摒弃了显式的图构建与优化步骤，数据关联完全由 Transformer 解码器中的交叉注意力隐式完成，这简化了流程但牺牲了全局图约束的显式建模能力。

**相对于联合检测与 ReID 基线**：**FairMOT** (Zhang et al., IJCV 2021) 和 **QuasiDense** (Pang et al., CVPR 2021) 在检测分支上耦合 ReID 特征学习，通过外观相似度进行关联。TrackFormer 不显式学习外观嵌入，而是依赖 track queries 中编码的时空位置信息进行身份传播。这一差异在 IDF1 指标上尤为显著——消融实验表明，移除 track queries 改用中心距离匹配后，IDF1 骤降 14.1 点，说明注意力关联对身份保持至关重要。

### 2. 适用边界

TrackFormer 的设计假设决定了其适用范围的边界：

- **在线跟踪场景**：方法仅依赖当前帧与前一帧，属于严格在线方法。这一设计使其适用于实时应用，但也限制了其对长时序上下文的利用。
- **两帧训练窗口**：模型仅在相邻两帧上训练，这意味着它学习的是短时运动模式。对于长时间遮挡或大幅非线性运动，模型缺乏足够的时序感受野来维持稳定预测。
- **检测质量依赖**：TrackFormer 的跟踪能力内嵌于检测框架中，其性能高度依赖目标检测的质量。在公共检测设置下，需要额外的 IoU 过滤步骤来抑制低质量检测，这引入了与 CenterTrack 等方法的处理差异，影响了公平比较。
- **数据需求**：模型需要大量目标检测数据（如 CrowdHuman）进行预训练，对标注资源的依赖较高。

### 3. 关键局限

从方法设计和实验结果中可识别以下局限：

1. **长时遮挡处理不足**：track query 的重识别机制仅适用于短时遮挡（消融显示 IDF1 提升 1.4 点），对于目标消失数帧后重新出现的场景，自回归传播的身份信息可能已严重退化。
2. **缺乏显式运动建模**：track queries 不显式编码速度或加速度信息，其参考点仅基于前一帧边界框中心进行动态调整。在快速移动或相机大幅运动时，注意力可能无法有效聚焦于正确区域。
3. **公共检测公平性问题**：Table A.1 显示，TrackFormer 使用最小 IoU 过滤时 IDF1 为 63.4，而 CenterTrack 使用中心距离过滤时为 61.0，过滤策略的差异使得直接比较需要谨慎解读。
4. **分割跟踪的内存与质量权衡**：在 MOTS 扩展中，因可变形注意力的稀疏特征图导致分割掩码质量下降，TrackFormer 被迫回退到原始 DETR 注意力，这限制了其在密集场景下的扩展性。

### 4. 开放问题

基于上述分析，以下问题值得进一步探索：

- **多帧训练扩展**：如何将两帧训练扩展至多帧序列，使 track queries 能够利用更长的时序上下文，同时保持在线推理的约束？
- **显式运动编码**：track query 嵌入是否可以显式编码运动信息（如速度、加速度），从而在遮挡期间进行更稳定的位置预测？
- **密集场景的身份稳定性**：在极度拥挤的场景中，多个 track queries 的注意力可能相互干扰，如何设计更鲁棒的查询交互机制以抑制身份切换？
- **时序数据增强**：传统空间增强（如随机裁剪、翻转）难以直接施加到 track query 嵌入空间，如何设计适合 Transformer 跟踪框架的时序增强策略？
- **与图方法的融合**：TrackFormer 的注意力关联与图优化方法各有优势，是否存在将全局图约束注入 Transformer 解码过程的混合方案？



## 原文 PDF

![[paperPDFs/CVPR_2022/TrackFormer_Multi_Object_Tracking_with_Transformers.pdf]]
