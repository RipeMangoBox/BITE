---
title: "Novel Class Discovery for 3D Point Cloud Semantic Segmentation"
type: paper
paper_level: A
venue: CVPR
year: 2023
pdf_ref: paperPDFs/CVPR_2023/Novel_Class_Discovery_for_3D_Point_Cloud_Semantic_Segmentation.pdf
aliases:
- NNPS
- NCD3PCSS
tags:
- CVPR_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "在线伪标签分配策略：把聚类形式化为最优传输问题，通过Sinkhorn-Knopp算法在批次内等分约束下产生软伪标签，并辅以类别平衡队列与不确定性自适应筛选。"
primary_logic: "利用在线等分约束的最优传输聚类，配合队列存储历史特征以缓解批次内类别缺失和不平衡，再通过预测概率的百分位数阈值过滤低置信度点，逐步学习可靠的类原型，从而在无需离线全量聚类和前景/背景假设的条件下实现高质量3D新类语义分割。"
claims:
- "在SemanticPOSS上，NOPS的平均新类mIoU达到21.40，比EUMS†高6.5个点。"
- "在SemanticKITTI上，NOPS的平均新类mIoU达到22.84，比EUMS†高5.8个点。"
- "消融实验表明，逐步加入在线聚类(无预训练)、不确定性筛选和类别平衡队列能持续提升新类mIoU，最终完整模型取得最佳性能。"
- "SemanticPOSS (平均4个划分) 上 新类 mIoU = 21.40"
---

# Novel Class Discovery for 3D Point Cloud Semantic Segmentation

> [!tip] 核心洞察
> 利用在线等分约束的最优传输聚类，配合队列存储历史特征以缓解批次内类别缺失和不平衡，再通过预测概率的百分位数阈值过滤低置信度点，逐步学习可靠的类原型，从而在无需离线全量聚类和前景/背景假设的条件下实现高质量3D新类语义分割。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向三维点云语义分割的新类发现 |
| 英文题名 | Novel Class Discovery for 3D Point Cloud Semantic Segmentation |
| 会议/期刊 | CVPR 2023 |
| Links | [paper](https://arxiv.org/abs/2303.11610); [GitHub](https://github.com/LuigiRiz/NOPS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | NOPS (NOvel Point Segmentation) |
| Dataset | SemanticPOSS (平均4个划分), SemanticKITTI (平均4个划分) |

> [!tip] 效果简介
> - SemanticPOSS (平均4个划分) 上，新类 mIoU 为 21.40，对比 14.94，变化 +6.5。
> - SemanticKITTI (平均4个划分) 上，新类 mIoU 为 22.84，对比 17.04，变化 +5.8。

## 概述

三维点云语义分割中的新类发现（Novel Class Discovery, NCD）任务要求模型在仅利用基类标注样本的前提下，通过聚类无标注点云中的新类点来识别未知类别。将已有的2D NCD方法直接迁移至3D点云面临根本性障碍：3D数据缺乏前景/背景显著性概念，且每个场景可能同时包含多个新类，导致离线K‑Means聚类产生的伪标签质量低下、内存开销巨大，难以支撑在线学习与类别不平衡处理。

针对上述瓶颈，本文提出 **NOPS (NOvel Point Segmentation)** 方法。其核心调控机制在于将聚类形式化为最优传输问题，通过Sinkhorn‑Knopp算法在批次内等分约束下实时生成软伪标签，并辅以类别平衡队列存储历史特征以缓解批次间类别缺失与长尾分布，同时利用自适应分位数阈值过滤低置信度点，逐步学习可靠的类原型。这一设计使得NOPS无需离线全量聚类和前景/背景假设，即可实现高质量的3D新类语义分割。

在SemanticPOSS和SemanticKITTI两个基准数据集上，NOPS均显著优于专门为3D点云改编的基线方法EUMS†（Zhao et al., CVPR 2022）。SemanticPOSS上平均新类mIoU达到21.40，相较EUMS†提升6.5个点；SemanticKITTI上平均新类mIoU达到22.84，提升5.8个点。消融实验进一步证实，逐步引入在线聚类、不确定性筛选和类别平衡队列能够持续提升新类分割性能，验证了各组件的协同有效性。

## 背景与动机

点云语义分割是自动驾驶、机器人导航等三维场景理解任务的核心技术。然而，现实世界中物体类别不断涌现，完全依赖人工标注的闭集训练范式难以持续扩展。新类发现（Novel Class Discovery, NCD）旨在利用已标注基类的知识，从未标注数据中自动发现并分割出新语义类别，从而降低标注成本并提升模型的开放世界适应能力。

当前NCD研究主要集中在2D图像领域。以**EUMS**（Zhao et al., CVPR 2022）为代表的2D方法，通过离线K-Means聚类生成伪标签并结合自训练，在图像语义分割新类发现上取得了显著进展。然而，将这些方法迁移至3D点云面临三个根本性挑战：

**第一，3D数据缺乏前景/背景显著性概念。** 2D图像中，目标物体通常具有明确的前景-背景区分，这一先验可辅助聚类过程。但3D点云场景中，每个点都是三维空间中的等质采样，不存在天然的前景/背景语义边界，导致基于2D假设的聚类策略直接失效。

**第二，多新类共存与离线聚类的内存瓶颈。** 单个3D场景往往同时包含多个新类别，而2D NCD方法通常假设每张图像仅含单一新类。若将离线K-Means应用于3D全数据集特征，需要将所有场景的点级特征收集后统一聚类——在SemanticKITTI和SemanticPOSS等大规模数据集上，这将导致巨大的内存消耗和计算开销，难以实际部署。

**第三，批次内类别缺失与长尾分布。** 3D点云场景中，不同类别的点数差异悬殊（如地面点远超行人点），且单个训练批次内难以保证所有新类均出现。这种批次级的类别缺失和不平衡，使得传统基于批次内统计的聚类方法极易产生退化解——将所有点分配给同一类别。

上述挑战共同指向一个核心瓶颈：**在3D点云语义分割的新类发现中，如何在无需离线全量聚类、不依赖前景/背景假设的条件下，实现高质量且计算可行的在线新类学习？** 本文正是围绕这一问题展开，提出了在线伪标签分配策略NOPS（NOvel Point Segmentation），通过最优传输聚类、类别平衡队列与不确定性自适应筛选的协同设计，首次实现了面向3D点云的高效新类语义分割。

## 核心创新

NOPS 的核心创新在于将 3D 点云语义分割的新类发现（NCD）从依赖离线全量聚类的范式，转变为**在线等分约束的最优传输聚类**框架，并通过**类别平衡队列**与**不确定性自适应筛选**两个配套机制，系统性地解决了 3D 场景中类别缺失、长尾分布和伪标签噪声三大瓶颈。

### 创新一：在线等分约束的最优传输聚类

2D NCD 方法 **EUMS**（Zhao et al., CVPR 2022）在 3D 点云上存在根本性困难：3D 数据缺少前景/背景显著性概念，且每个场景可能同时包含多个新类，导致离线 K-Means 聚类产生的伪标签质量极差、内存消耗巨大。NOPS 将聚类形式化为一个最优传输问题：

$$\operatorname*{max}_{\boldsymbol{\mathsf{Q}}\in\mathcal{Q}} \ \mathrm{Tr}(\boldsymbol{\mathsf{Q}}^{\top}\boldsymbol{\mathsf{P}}^{\top}\boldsymbol{\mathsf{Z}}) + \epsilon H(\boldsymbol{\mathsf{Q}})$$

其中运输多面体的等分约束为：

$$\mathcal{Q} = \left\{ \boldsymbol{\mathbb{Q}} \in \mathbb{R}_{+}^{C_n \times m} | \boldsymbol{\mathbb{Q}} 1_m = \frac{1}{C_n} \boldsymbol{1}_{C_n}, \boldsymbol{\mathbb{Q}}^{\top} \boldsymbol{1}_{C_n} = \frac{1}{m} \boldsymbol{1}_m \right\}$$

该约束确保每个类原型在批次内被选中的次数平均为 $m/C_n$，从根本上避免了所有点被分配到同一类的退化解。通过 **Sinkhorn-Knopp 算法**迭代求解，得到软伪标签：

$$\mathsf{q}^{*} = \mathrm{diag}(\alpha) \exp\left( \frac{\mathsf{P}^{\top}\mathsf{Z}}{\epsilon} \right) \mathrm{diag}(\beta)$$

**关键改变**：将伪标签生成从“离线全数据集 K-Means → 硬伪标签”改为“在线批次内 Sinkhorn-Knopp → 软伪标签”，使聚类与特征学习同步进行，类原型 $\mathsf{P}$ 同时作为新类分割头 $f_n$ 的权重，实现端到端优化。

### 创新二：类别平衡队列缓解批次内类别缺失

在线聚类虽然高效，但单个批次内可能缺失部分新类或呈现严重不平衡。NOPS 引入**类别平衡队列** $Z_q$，存储历史批次中经过不确定性筛选的新类点特征，在每次聚类时与当前批次特征拼接使用。这一机制以极小的存储代价，有效缓解了批次级别的类别缺失和长尾分布问题，为在线聚类提供了统计稳定性。

### 创新三：不确定性自适应筛选过滤低置信度点

伪标签噪声是 NCD 的核心挑战。NOPS 设计了基于**自适应分位数阈值**的筛选函数：

$$\phi : ( { \mathcal { F } } _ { n } , { \hat { \mathcal { V } } } _ { n } ) \times p \mapsto ( { \bar { \mathcal { F } } } _ { n } )$$

对每个新类 $c$，计算其预测概率的第 $p$ 百分位数作为阈值 $\tau_c$，仅保留概率高于 $\tau_c$ 的点用于伪标签生成和队列更新。这一设计使筛选强度自适应于各类的学习难度：易学类自然获得更高置信度，难学类则动态调整门槛。

### 创新四：过聚类多头增强特征多样性

NOPS 采用多个新类分割头与过聚类头（$o=3$）协同训练，输出 $o \cdot C_n$ 个 logits。过聚类头迫使网络学习更丰富的特征表示，在推理时丢弃，仅保留主分割头。这一设计以零推理代价增强了特征的判别性和多样性。

### 消融验证

消融实验（Figure 4）系统验证了各组件的独立贡献：仅使用在线聚类（NP，无预训练）即可在新类上达到 20.26 mIoU；加入不确定性筛选（NP+）提升至 20.63；再引入类别平衡队列（NP++）达到 20.90；完整 NOPS 取得最佳性能。这证实了三个创新点之间存在正向协同效应。

## 整体框架

NOPS的整体pipeline围绕“双视图增强—共享特征提取—在线伪标签分配—双头预测—交换一致性优化”构建，核心设计目标是摆脱离线全量聚类对前景/背景假设和巨大内存的依赖，转而在每个批次内通过最优传输在线产生高质量的软伪标签。

### 数据流与模块关系

**输入层**：对原始点云 $\mathcal{X}$ 进行两次随机增强，生成两个视图 $\mathcal{X}'$ 和 $\mathcal{X}''$（Figure 2）。

**共享特征提取器 $f_\xi$**：采用MinkowskiUNet-34C作为骨干网络，从倒数第二层提取点级特征 $\mathcal{F}$。该骨干在两个视图之间共享权重，保证特征空间的一致性。

**在线伪标签分配模块**：这是NOPS区别于基线EUMS†的核心模块。将聚类形式化为最优传输问题，在运输多面体 $\mathcal{Q}$ 的等分约束下，通过Sinkhorn-Knopp算法迭代求解软分配矩阵 $\mathsf{q}^*$，为每个批次实时生成伪标签。该模块同时维护 $C_n$ 个类原型 $\mathsf{P}$，并直接将其用作新类分割头 $f_n$ 的权重，实现原型学习与分类器训练的一体化。

**双头预测层**：
- **基类分割头 $f_b$**：输出基类logits，使用真实标注进行监督。
- **新类分割头 $f_n$（含过聚类头）**：输出 $o \cdot C_n$ 个logits，其中 $o$ 为过聚类因子（设为3）。过聚类头仅在训练时增强特征多样性，推理时丢弃。

**类别平衡队列 $\mathrm{Z}_q$**：存储历史批次中经过不确定性筛选的新类点特征，作为当前批次在线聚类的补充数据，缓解批次内类别缺失和长尾分布问题。

**不确定性感知筛选 $\phi$**：对每个新类 $c$，计算其预测概率的 $p$-th 分位数作为自适应阈值 $\tau_c$，仅保留置信度高于该阈值的点用于伪标签生成和队列更新。

### 优化目标

整个网络通过交换预测一致性损失进行端到端训练：
$$\mathcal{L}(\mathcal{X}) = \ell(\hat{\mathcal{V}}', \tilde{\mathcal{V}}'') + \ell(\hat{\mathcal{V}}'', \tilde{\mathcal{V}}')$$
其中 $\hat{\mathcal{V}}'$ 和 $\hat{\mathcal{V}}''$ 分别为两个视图的预测，$\tilde{\mathcal{V}}'$ 和 $\tilde{\mathcal{V}}''$ 为对应的伪标签。该损失在基类和新类上均计算加权交叉熵，基类权重来自训练频率，新类权重均等。

### 与基线EUMS†的架构对比

EUMS†的pipeline（Figure 6）采用“预训练—全数据集下采样—离线K-Means聚类—微调”的串行流程：先用基类点预训练 $f_\xi$ 和 $f_b$，再对所有场景的新类点随机下采样并提取特征，在全量特征上执行K-Means产生硬伪标签，最后插入新分割头 $f_c$ 进行微调。这一流程在3D场景中面临两个根本性困难：①每个场景可能包含多个新类，离线聚类无法利用场景级上下文；②点云规模巨大，全量聚类内存消耗极高。

NOPS将上述离线串行流程重构为在线并行架构：伪标签生成与特征学习在同一批次内交替进行，无需预训练阶段，也不依赖前景/背景显著性假设。消融实验证实，逐步加入在线聚类（NP, 20.26 mIoU）、不确定性筛选（NP+, 20.63 mIoU）和类别平衡队列（NP++, 20.90 mIoU）能持续提升新类分割性能，完整NOPS取得最优（Figure 4）。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2303_11610/figures/002_Figure_2.jpg]]
*Figure 2: Overview of NOPS. We random augment the input point cloud twice and extract point-level features $\mathcal { F }$ with the shared model $f _ { \xi } . \mathcal { F }$ are used to obtain pseudo-labels in the online pseudo-labelling. We forward $\mathcal { F }$ to a novel $f _ { n }$ and a base $f _ { b }$ segmentation layer to output the novel and base predictions, respectively. We optimise our network by minimising a global objective function based on cross entropy

## 核心模块与公式推导

NOPS 的核心由三个紧密协作的模块构成：**在线伪标签分配**、**类别平衡队列**和**不确定性感知筛选**。它们共同解决了将 2D 新类发现方法迁移到 3D 点云时面临的关键瓶颈——离线 K-Means 聚类伪标签质量差、内存消耗巨大，且难以应对批次内类别缺失与长尾分布。

### 在线伪标签分配：最优传输形式化

传统方法（如 EUMS†）依赖离线 K-Means 对全数据集特征进行聚类，这不仅需要随机下采样来缓解内存压力，还引入了前景/背景显著性假设，而这一假设在 3D 点云场景中并不成立——每个场景可能同时包含多个新类。NOPS 将聚类形式化为一个**最优传输问题**，在批次内实时求解，从根本上规避了离线全量聚类的弊端。

具体而言，给定一个批次中 $m$ 个新类点的特征矩阵 $\boldsymbol{\mathsf{Z}} \in \mathbb{R}^{d \times m}$ 和 $C_n$ 个可学习的类原型 $\boldsymbol{\mathsf{P}} \in \mathbb{R}^{d \times C_n}$，目标是找到一个软分配矩阵 $\boldsymbol{\mathsf{Q}} \in \mathbb{R}^{C_n \times m}$，使得点特征与类原型之间的相似度最大化，同时引入熵正则项 $\epsilon H(\boldsymbol{\mathsf{Q}})$ 来控制分配的平滑度：

$$\operatorname*{max}_{\boldsymbol{\mathsf{Q}}\in\mathcal{Q}} \ \mathrm{Tr}(\boldsymbol{\mathsf{Q}}^{\top}\boldsymbol{\mathsf{P}}^{\top}\boldsymbol{\mathsf{Z}}) + \epsilon H(\boldsymbol{\mathsf{Q}})$$

其中，运输多面体 $\mathcal{Q}$ 施加了**等分约束**，确保每个类原型在批次内被选中的次数平均为 $m/C_n$，从而避免所有点被分配到同一类的退化解：

$$\mathcal{Q} = \left\{ \boldsymbol{\mathbb{Q}} \in \mathbb{R}_{+}^{C_n \times m} \mid \boldsymbol{\mathbb{Q}} 1_m = \frac{1}{C_n} \boldsymbol{1}_{C_n},\ \boldsymbol{\mathbb{Q}}^{\top} \boldsymbol{1}_{C_n} = \frac{1}{m} \boldsymbol{1}_m \right\}$$

该问题通过 **Sinkhorn-Knopp 算法**迭代求解，得到标准化指数形式的最优软分配：

$$\mathsf{q}^{*} = \mathrm{diag}(\alpha) \exp\left( \frac{\mathsf{P}^{\top}\mathsf{Z}}{\epsilon} \right) \mathrm{diag}(\beta)$$

其中 $\alpha$ 和 $\beta$ 是重归一化向量。求解得到的 $\mathsf{q}^{*}$ 即作为新类点的在线软伪标签。此外，NOPS 采用**多头过聚类**策略，使用 $o$ 个新类分割头（输出 $o \cdot C_n$ 个 logits）协同训练以增强特征多样性，这些过聚类头在推理时被丢弃。

### 类别平衡队列：缓解批次内类别缺失

在线聚类虽然高效，但单个批次内可能不包含所有新类，导致类原型更新偏向频繁出现的类别。为此，NOPS 引入一个**类别平衡队列** $\boldsymbol{\mathsf{Z}}_q$，存储来自历史批次的新类点特征。在每次迭代中，队列中的历史特征与当前批次特征拼接后共同参与 Sinkhorn-Knopp 聚类，从而为缺失类别提供“虚拟样本”，缓解类别不平衡对原型学习的负面影响。

### 不确定性感知筛选：过滤低置信度伪标签

伪标签的质量直接影响模型训练。NOPS 设计了一个**自适应分位数阈值筛选函数** $\phi$，根据模型对新类点的预测概率动态过滤低置信度样本：

$$\phi : ( { \mathcal { F } } _ { n } , { \hat { \mathcal { V } } } _ { n } ) \times p \mapsto ( { \bar { \mathcal { F } } } _ { n } )$$

对于每个新类 $c$，计算其预测概率的第 $p$ 百分位数作为阈值 $\tau_c$，仅保留概率高于 $\tau_c$ 的点用于伪标签生成和队列更新。这一机制确保只有高置信度的点参与聚类与训练，有效抑制噪声伪标签的传播。

### 交换预测一致性损失

整个网络通过**交换预测一致性损失**进行端到端优化。对输入点云进行两次随机增强得到两个视图 $\mathcal{V}'$ 和 $\mathcal{V}''$，分别计算其伪标签 $\tilde{\mathcal{V}}'$ 和 $\tilde{\mathcal{V}}''$，然后交叉计算加权交叉熵：

$$\mathcal { L } ( \mathcal { X } ) = \ell ( \hat { \mathcal { V } } ^ { \prime } , \tilde { \mathcal { V } } ^ { \prime \prime } ) + \ell ( \hat { \mathcal { V } } ^ { \prime \prime } , \tilde { \mathcal { V } } ^ { \prime } )$$

其中 $\hat{\mathcal{V}}$ 为模型预测。该损失强制两个增强视图在伪标签空间下保持一致性，驱动特征提取器 $f_\xi$ 和类原型 $\boldsymbol{\mathsf{P}}$ 的联合学习。基类分割头 $f_b$ 则使用真实标注计算标准交叉熵损失，二者联合优化实现基类知识的保持与新类结构的发现。

## 实验与分析

### 实验设置

本文在SemanticKITTI和SemanticPOSS两个大规模室外3D点云语义分割数据集上验证NOPS。为构建新类发现场景，作者将每个数据集的语义类别划分为基类（有标注）和新类（无标注），并设计了四种不同的划分方案（Table 1和Table 2），以覆盖不同新类数量和类别组合的挑战。

所有实验采用MinkowskiUNet-34C作为骨干网络，使用SGD优化器（动量0.9，权重衰减0.0001），学习率调度采用线性预热加余弦退火策略（$lr_{max}=10^{-2}$，$lr_{min}=10^{-5}$）。评估指标为新类mIoU，同时报告全监督训练的性能上界作为参考。

基线方法EUMS†是作者将2D新类发现方法EUMS（Zhao et al., CVPR 2022）专门适配到3D点云的版本：对每个场景的无标注点随机下采样后提取特征，在全数据集上运行K-Means聚类生成硬伪标签，再通过最近邻传播和微调完成新类学习。这一基线本身已包含过聚类和熵建模等增强策略，确保对比的公平性。

### 主要结果

**在SemanticPOSS上**，NOPS在四个划分中的三个显著优于EUMS†（Table 3）。平均新类mIoU达到21.40，比EUMS†的14.94高出6.5个点。其中POSS-40划分的改进最为显著（+18.3 mIoU），POSS-31提升9.0 mIoU。仅在POSS-32上NOPS略低于EUMS†（差距0.6 mIoU），该划分的新类包含“trunk”、“fence”和“pole”等细长结构，点云稀疏且类间外观相似，对伪标签质量提出了更高要求。

**在SemanticKITTI上**，NOPS在所有四个划分上全面超越EUMS†（Table 4）。平均新类mIoU达到22.84，比EUMS†的17.04高出5.8个点。值得注意的是，即使在全监督上界的绝对差距较大的划分（如KITTI-43，全监督仅31.49 mIoU），NOPS仍保持了对EUMS†的稳定领先（+4.7 mIoU），表明在线聚类策略在不同难度分布下具有鲁棒性。

**定性分析**（Figure 3, Figure 7-14）进一步揭示了两种方法的行为差异：EUMS†的预测在新类区域呈现明显的混杂和碎片化——例如在POSS-31中，建筑物立面被错误地切分为多个类别的混合体；而NOPS能够输出更一致、更完整的新类分割结果，伪标签的等分约束有效抑制了“全部点坍缩到同一类”的退化现象。

### 消融实验

为验证各组件的独立贡献，作者在SemanticPOSS上进行了系统的消融研究（Figure 4）。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2303_11610/figures/008_Figure_4.jpg]]
*Figure 4: Ablation study with different components and initialisation strategies on SemanticPOSS. In P, OC and Q, we initialise the model after base pre-training, and use different configurations of the over-clustering heads and of our queue balancing. In NP NP+, ${ \mathsf { N P } }$ { + } { + } and Full, we begin with Q, we avoid pre-training, and we use φ and $\tau _ { c }$ incrementally. See Sec. 6 for definition of methods

**从预训练基线出发的消融**（P, OC, Q系列）表明：在基类预训练后引入过聚类头（OC）和类别平衡队列（Q）能逐步提升新类mIoU，但增益有限——因为预训练阶段仅使用基类点，特征空间对新类缺乏判别性。

**从零开始的在线聚类消融**（NP, NP+, NP++, Full系列）揭示了核心机制的真实贡献：
- **NP**（纯在线聚类，无预训练，无不确定性筛选，无队列）：新类mIoU已达20.26，超过EUMS†的14.94，证明在线Sinkhorn-Knopp聚类本身已大幅优于离线K-Means；
- **NP+**（加入不确定性筛选）：提升至20.63，说明自适应分位数阈值能有效过滤低置信度噪声点；
- **NP++**（进一步加入类别平衡队列）：提升至20.90，队列存储的历史特征缓解了批次内类别缺失问题；
- **Full NOPS**（完整模型）：取得最佳性能，验证了三个组件间的协同效应。

**不确定性阈值参数p的敏感性**（Table 5）：p值控制筛选的严格程度。POSS-40（新类为“building”等大面积类别）受益于较低的p值（宽松筛选），因为大面积类别点云密集、特征稳定；而POSS-33（新类包含“bicyclist”、“person”等小目标）在p=0.7时达到最佳14.38 mIoU，需要更严格的筛选以避免小目标的特征被背景噪声淹没。多数划分在p=0.5时取得最优。

### 失败模式与局限性

尽管NOPS在多数场景下表现优异，仍存在以下不足：

1. **细长/稀疏结构的挑战**：在POSS-32划分中NOPS略逊于EUMS†，该划分的新类（trunk、fence、pole）均为点云极度稀疏的细长结构，Sinkhorn-Knopp的等分约束可能导致这些少数类被强行分配到过多的伪标签，引入噪声。这表明当前在线聚类策略在处理极端稀疏几何结构时仍有改进空间。

2. **新类数量的先验依赖**：NOPS需要预知新类数量$C_n$来设置原型数量和运输多面体的维度。当$C_n$未知或新类以增量形式出现时，方法需要重新训练，缺乏灵活性。

3. **类别不平衡损失的非最优性**：当前使用的加权交叉熵损失（基类按频率加权，新类等权）在处理3D点云固有的长尾分布时可能不够精细，更先进的类不平衡处理技术（如focal loss、重采样策略）有望进一步提升性能。

4. **队列机制的固定容量**：类别平衡队列$Z_q$的容量是固定的超参数，其最优值可能随数据集规模和类别分布变化，目前缺乏自适应的容量调整机制。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2303_11610/figures/010_Figure_5.jpg]]
*Figure 5: Histograms representing the number of points belonging to each class in SemanticKITTI [4] and SemanticPOSS [24]. Each class has been assigned the colour of the split in which it has to be considered novel (unlabelled)*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2303_11610/figures/003_Table_1.jpg]]
*Table 1: SemanticKITTI splits, is defined as $\mathrm { K I T T I } { - n } ^ { i }$ , where n is the number of novel classes and i is the split index*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2303_11610/figures/004_Table_2.jpg]]
*Table 2: SemanticPOSS splits, defined as $\mathrm { P O S S } { - n ^ { i } }$ , where n is the number of novel classes and i is the split index*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2303_11610/figures/005_Table_3.jpg]]
*Table 3: Novel class discovery results on SemanticPOSS. NOPS outperforms EUMS† on three out of four splits. Full supervision: model trained with labels for base and novel classes. EUMS†: baseline described in Sec. 4. Highlighted values are the novel classes in each split*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2303_11610/figures/006_Table_4.jpg]]
*Table 4: Novel class discovery results on SemanticKITTI. NOPS outperforms EUMS† on all four splits. Full supervision: model trained with annotations for base and novel classes. EUMS†: baseline described in Sec. 4. Highlighted values are the novel classes in each split*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2303_11610/figures/009_Table_5.jpg]]
*Table 5: Ablation study showing how different values of p affect the performance on SemanticPOSS. The lower p is, the less severe the selection of the features, resulting in better performances for $\mathrm { P O S S – 4 } ^ { 0 }$ . Differently, POSS-33 benefits from an higher value of p, which leads to a more vigorous filtering of the features. POSS- $3 ^ { 1 }$ and POSS-32 show the best performances with p = 0.5*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2303_11610/figures/016_Figure_11.jpg]]
*Figure 11: Qualitative comparison on SemanticKITTI from KITTI-50. EUMS† [41] outputs are completely or partially wrong for the novel classes. NOPS improves the performance by providing correct and more homogeneous predictions*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2303_11610/figures/017_Figure_12.jpg]]
*Figure 12: Qualitative comparison on SemanticKITTI from KITTI-51. EUMS† [41] outputs are completely or partially wrong for the novel classes. NOPS improves the performance by providing correct and more homogeneous predictions*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2303_11610/figures/018_Figure_13.jpg]]
*Figure 13: Qualitative comparison on SemanticKITTI from KITTI-52. EUMS† [41] outputs are completely or partially wrong for the novel classes. NOPS improves the performance by providing correct and more homogeneous predictions*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2303_11610/figures/019_Figure_14.jpg]]
*Figure 14: Qualitative comparison on SemanticKITTI from KITTI-43. EUMS† [41] outputs are completely or partially wrong for the novel classes. NOPS improves the performance by providing correct and more homogeneous predictions*

## 方法谱系与知识库定位

### 从2D到3D新类发现的迁移瓶颈

NOPS的核心动机源于将2D语义分割新类发现方法迁移至3D点云时暴露出的根本性不适配。论文选择 **EUMS**（Zhao et al., CVPR 2022）作为2D代表性方法，并专门为其设计了3D适配版本EUMS†作为基线。EUMS的原始设计依赖两个关键假设：（1）图像中存在明确的前景/背景显著性概念，可用于基于熵的不确定性建模；（2）通过在全数据集上离线执行K-Means聚类生成伪标签。然而，3D点云场景天然缺乏前景/背景的语义区分（如建筑物立面与道路在几何上并无显著差异），且每个场景可能同时包含多个新类，导致离线聚类面临双重困境：随机下采样后在全量特征上运行K-Means不仅内存消耗巨大，而且聚类质量严重退化。

这一瓶颈直接催生了NOPS的设计转向：放弃离线全量聚类范式，转而采用在线批次级聚类策略。论文明确指出，在线聚类能够实时更新类原型，避免了对全数据集特征的依赖，从而在根本上绕过了3D数据的规模与复杂性障碍。

### 方法谱系中的关键设计锚点

NOPS的方法定位可以从三个核心技术锚点来理解，每个锚点都对应着对基线缺陷的针对性改进：

**锚点一：在线最优传输聚类替代离线K-Means。** EUMS†依赖离线K-Means在随机下采样后的全量特征上生成硬伪标签，这不仅计算代价高，而且硬分配缺乏对不确定性的建模。NOPS将聚类形式化为最优传输问题，通过Sinkhorn-Knopp算法在批次内等分约束下产生软伪标签。具体而言，运输多面体约束 $\mathcal{Q} = \{ \mathbb{Q} \in \mathbb{R}_{+}^{C_n \times m} | \mathbb{Q} 1_m = \frac{1}{C_n} \boldsymbol{1}_{C_n}, \mathbb{Q}^{\top} \boldsymbol{1}_{C_n} = \frac{1}{m} \boldsymbol{1}_m \}$ 确保每个类原型在批次内被均匀分配，避免了将所有点分配给同一类的退化解。这一设计借鉴了自监督学习中的SwAV等工作，但将其首次引入3D点云新类发现场景。

**锚点二：类别平衡队列缓解批次内类别缺失。** 在线聚类虽然高效，但单个批次可能不包含所有新类，导致类原型更新偏向频繁出现的类别。NOPS引入类别平衡队列 $Z_q$，存储历史批次中经过不确定性筛选的高置信度特征，在聚类时与当前批次特征拼接使用。这一机制使得即使在当前批次中完全缺失某类点时，该类原型仍能通过队列中的历史特征获得更新信号，有效缓解了3D场景中普遍存在的类别长尾分布问题。

**锚点三：不确定性自适应筛选过滤低质量伪标签。** EUMS†虽然使用了基于熵的不确定性建模，但该机制高度依赖前景/背景假设，在3D场景中效果有限。NOPS转而采用更通用的自适应分位数阈值策略：对每个新类 $c$，计算其预测概率的 $p$-th 百分位数作为阈值 $\tau_c$，仅保留概率高于 $\tau_c$ 的点用于伪标签生成和队列更新。这一筛选函数 $\phi : ( \mathcal{F}_n, \hat{\mathcal{V}}_n ) \times p \mapsto ( \bar{\mathcal{F}}_n )$ 不依赖任何前景/背景先验，完全由数据驱动的置信度分布决定。

### 适用边界与局限

NOPS的有效性建立在两个前提之上，这些前提也构成了其适用边界：

1. **新类数量 $C_n$ 需预先已知。** 方法中的过聚类头设计、最优传输的等分约束、以及类原型的维度均显式依赖 $C_n$。当新类数量未知或以增量形式出现时，NOPS无法直接适用。论文将此列为明确局限，并指出支持未知类数量的发现是未来方向。

2. **基类与新类共享特征空间。** NOPS假设基类预训练阶段学到的特征表示对新类具有足够的泛化性，使得在线聚类能够发现语义上有意义的分组。当基类与新类在几何或外观上差异极大时，特征空间的迁移性可能不足，但论文未对此进行消融分析。

此外，论文承认当前使用的类别平衡损失可能并非最优，更先进的类不平衡处理技术（如focal loss的变体或重加权策略）有望进一步提升性能，尤其是在极端长尾的划分上。

### 与相关工作的关系定位

在2D新类发现领域，EUMS代表了基于离线聚类和不确定性建模的主流范式。NOPS通过引入在线聚类和自适应筛选，实际上将3D新类发现推向了与自监督对比学习更紧密的交叉地带——其核心机制（Sinkhorn-Knopp聚类、队列存储、交换预测）与SwAV、MoCo等方法存在明显的设计亲缘性。然而，NOPS并非简单移植：它将对比学习中的实例级判别任务改造为语义级新类发现任务，通过显式建模类原型和过聚类头来捕获类内多样性，这是对自监督范式的关键适配。

在3D点云语义分割领域，NOPS是首个将新类发现问题形式化并提出完整解决方案的工作。此前的方法要么依赖全监督，要么聚焦于域适应或开集识别，而非在无新类标注的条件下主动发现语义类别。因此，NOPS在3D视觉中的定位更接近于问题定义者而非改进者，其方法框架为后续工作提供了可扩展的基础架构。

### 开放问题

1. **未知新类数量的发现机制。** 当前方法对 $C_n$ 的依赖限制了其在开放世界场景中的应用。如何设计能够动态估计新类数量并自适应调整聚类结构的机制，是一个具有挑战性的方向。

2. **增量式新类学习。** 现实场景中新类往往以增量形式出现（如自动驾驶中不断遇到新的障碍物类型）。NOPS的离线训练范式要求同时访问所有新类数据，无法支持增量发现。将在线聚类框架扩展至持续学习设定，需要解决灾难性遗忘和原型动态扩展等问题。

3. **极端类别不平衡的损失设计。** 3D点云中类别频率差异可达数个数量级（如SemanticKITTI中“道路”与“摩托车手”的点数之比），当前简单的等权交叉熵损失在极端不平衡下可能失效。如何设计对长尾分布鲁棒的聚类损失，是提升新类发现质量的关键。

4. **点云特有的几何先验利用。** NOPS当前仅依赖点级特征进行聚类，未显式利用3D空间中的几何连续性、法向量或局部邻域结构。将这些几何先验融入聚类过程，可能进一步提升伪标签质量，尤其是在几何结构清晰但外观相似的类别上。

## 原文 PDF

![[paperPDFs/CVPR_2023/Novel_Class_Discovery_for_3D_Point_Cloud_Semantic_Segmentation.pdf]]
