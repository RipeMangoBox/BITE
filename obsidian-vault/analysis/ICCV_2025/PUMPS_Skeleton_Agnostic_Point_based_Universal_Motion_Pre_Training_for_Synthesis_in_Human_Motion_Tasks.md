---
title: PUMPS Skeleton Agnostic Point based Universal Motion Pre Training for Synthesis in Human Motion Tasks
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Synthesis_in_Human_Motion_Tasks.pdf
project_link: null
code_link: https://github.com/MiniEval/PUMPS
aliases:
- PUMPS_Skeleton_A
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在解码器中引入高斯噪声向量作为点标识，并使用线性分配损失替代Chamfer距离，从而在保持时间一致性的同时避免点注意力计算。
primary_logic: 通过将点采样过程中的噪声向量机制融入解码器，并利用匈牙利算法进行点配对重建，可以高效地学习骨架无关的运动表示，并实现统一运动合成预训练。
claims:
- 高斯噪声向量能够赋予点云解码器点标识感知能力，从而在无点注意力的情况下生成时间一致的轨迹。
- 线性分配损失（匈牙利算法）有效解决了Chamfer距离导致的点分布崩溃问题，显著降低了重建误差。
- 在无监督预训练设置下，PUMPS在关键帧插值和运动过渡任务上超越了现有有监督方法。
- Keyframe interpolation (5-frame intervals, 121-frame sequences) 上 L2P↓ = 0.137
---

# PUMPS Skeleton Agnostic Point based Universal Motion Pre Training for Synthesis in Human Motion Tasks

> [!tip] 核心洞察
> 通过将点采样过程中的噪声向量机制融入解码器，并利用匈牙利算法进行点配对重建，可以高效地学习骨架无关的运动表示，并实现统一运动合成预训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | PUMPS：骨架无关的通用点云人体运动预训练合成方法 |
| 英文题名 | PUMPS Skeleton Agnostic Point based Universal Motion Pre Training for Synthesis in Human Motion Tasks |
| 会议/期刊 | ICCV 2025 |
| Links | [Code](https://github.com/MiniEval/PUMPS) · [paper](https://arxiv.org/abs/2507.20170) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PUMPS |
| Dataset | Keyframe interpolation, Motion transition |

> [!tip] 效果简介
> - Keyframe interpolation (5-frame intervals, 121-frame sequences) 上，L2P↓ 0.137 vs 0.186 (CITL) (-0.049)。
> - Motion transition (15-frame intervals, between 15-frame windows) 上，L2P↓ 0.168 vs 0.255 (CITL) (-0.087)。
> - Keyframe interpolation (5-frame intervals) 上，NPSS↓ 0.249 vs 0.536 (CITL) (-0.287)。

## 概要

人体运动合成长期受限于对特定骨架表示（如SMPL、Human3.6M等）的依赖，导致模型难以在不同骨架拓扑间泛化。现有基于点云的运动表示方法虽具备骨架无关的潜力，但在时间点云（Temporal Point Cloud, TPC）重建中面临两个根本性瓶颈：**时间点标识性缺失**——解码器无法在无点注意力机制的情况下区分不同时间步的对应点，导致轨迹混乱；以及**点分布崩溃**——常用的Chamfer距离损失倾向于将所有预测点拉向输入点云的聚类中心，丧失空间覆盖能力。此外，传统方法依赖昂贵的时空注意力机制，计算效率低下。

PUMPS（Point-based Universal Motion Pre-training for Synthesis）针对上述瓶颈提出了一个两阶段预训练框架。其核心创新在于：**在解码器中引入高斯噪声向量作为点标识**，模拟点云采样过程中的随机性，使解码器在无需逐点注意力的条件下即可感知点的身份，从而生成时间一致的轨迹；同时，**采用基于匈牙利算法的线性分配损失替代Chamfer距离**，通过寻找预测点与真实点之间的最优一一配对来监督重建，从根本上避免了点向聚类中心塌缩的问题。这一设计使得PUMPS能够高效学习骨架无关的运动表示，并支持统一的运动合成预训练。

在无监督预训练设置下，PUMPS在关键帧插值和运动过渡任务上展现出超越有监督方法的性能。具体而言，在5帧间隔的关键帧插值任务上，PUMPS的L2P误差为0.137，显著优于有监督基线CITL（Mo et al., CVPR 2023）的0.186；在15帧间隔的运动过渡任务上，PUMPS的L2P误差为0.168，相比CITL的0.255降低了约34%。消融实验进一步证实，线性分配损失、序列级dropout和旋转位置嵌入（RoPE）是性能提升的关键组件。预训练特征在下游任务微调中同样表现突出，使运动去噪模型的MPJPE降低约25%，验证了其作为通用运动先验的迁移能力。



### 人体运动合成的瓶颈：骨架依赖与表示泛化

人体运动合成是计算机视觉与图形学中的核心问题，涵盖关键帧插值、运动过渡、运动去噪、2D-to-3D运动估计等任务。传统方法通常将运动表示为特定骨架（skeleton）上的关节旋转序列，这使得模型与特定的骨骼拓扑结构深度绑定。一旦骨架结构发生变化（例如从SMPL人体模型切换到四足动物骨架），整个模型就需要重新设计和训练，难以实现跨骨架的泛化。这一“骨架依赖”问题严重制约了运动合成模型的通用性和可复用性。

### 时间点云表示：机遇与挑战

为突破骨架依赖的瓶颈，研究者开始探索将运动表示为**时间点云（Temporal Point Cloud, TPC）**——即从骨骼表面采样得到的一系列3D点帧序列。TPC作为骨架无关的表示，天然具有跨骨架泛化的潜力。然而，TPC的重建面临两个根本性挑战：

1. **时间点标识性缺失**：点云本身是无序集合，同一物体在不同帧中的对应点之间缺乏显式的标识关联。若不解决这一标识性问题，解码器生成的轨迹将出现点漂移和时序不一致，导致运动抖动或变形。
2. **点分布崩溃**：在训练点云自编码器时，常用的Chamfer距离损失倾向于将所有预测点拉向目标的聚类中心，造成生成的点云塌缩为少数几个位置，丧失几何细节和运动信息。

现有方法（如基于FoldingNet的架构）试图通过点注意力（point-wise attention）机制来隐式建立点对应关系，但这类时空注意力计算复杂度高，难以扩展到长序列或大规模点云场景。

### 现有无监督预训练的空白

在运动合成领域，有监督方法（如**CITL**，Mo et al., CVPR 2023）在关键帧插值等任务上表现优异，但需要成对的输入-输出运动数据进行训练，数据获取成本高且泛化能力有限。无监督/自监督预训练在NLP和图像领域已取得巨大成功（如BERT、MAE），但在运动合成中仍缺乏有效的通用预训练框架。现有的点云预训练方法（如**Point-BERT**，Yu et al., CVPR 2022；**MAE**，He et al., CVPR 2022）主要面向静态物体，无法直接处理时间点云序列中的时序动态建模需求。

### 本文动机

针对上述问题，PUMPS旨在实现**骨架无关的通用点云人体运动预训练**，核心动机包括：

- **解耦骨架依赖**：通过TPC表示彻底摆脱特定骨骼拓扑的约束，使单一预训练模型能够服务于多种下游运动任务。
- **高效的点标识机制**：设计一种无需点注意力的点标识感知解码器，在保持线性计算复杂度的同时生成时间一致的轨迹。
- **解决点崩溃问题**：提出新的重建损失函数，从根本上避免Chamfer距离导致的点分布塌缩。
- **建立运动预训练范式**：通过自监督掩码运动补全预训练，学习可迁移的潜在运动表示，在下游任务中通过微调即可超越有监督方法。



## 核心方法与创新机理

PUMPS 的核心创新在于通过**噪声向量驱动的点标识机制**和**线性分配重建损失**，在无需点注意力计算的前提下实现了时间一致且骨架无关的运动表示学习。相较于现有方法，PUMPS 在三个关键环节上做出了根本性改变：

### 1. 噪声向量驱动的点标识机制

传统点云解码器（如 FoldingNet）依赖点注意力或 Chamfer 距离隐式处理点对应关系，这不仅计算开销大，而且难以维持时间点云（TPC）中点的轨迹一致性——这是 TPC 重建面临的核心瓶颈：时间维度上的点标识性缺失会导致点分布崩溃，即所有预测点向聚类中心塌缩。

PUMPS 将点云采样过程中的噪声向量机制融入解码器设计：对于每个待生成的点，引入一个从标准正态分布采样的 $|z|$ 维高斯噪声向量 $z \sim \mathcal{N}(0,1)$，并将其附加到每个时间步的潜在向量序列中。这一设计的核心洞察在于：**噪声向量作为点的唯一标识符**，使解码器能够在无点注意力的情况下感知点身份，从而实现以轨迹为中心的 TPC 生成（Sec. 3.2）。这本质上模拟了点云采样过程中每个采样点具有独立采样标识的物理过程，但将其转化为可学习的生成机制。

### 2. 线性分配损失替代 Chamfer 距离

Chamfer 距离是点云重建中最常用的损失函数，但在 TPC 重建中会导致严重的点分布崩溃问题——解码器倾向于将所有预测点生成到输入点云的局部聚类中心，而非形成有意义的点对应关系。

PUMPS 提出使用**基于匈牙利算法的线性分配损失**：在给定输入点云 $\mathcal{P}$ 和预测点云 $\mathcal{P}'$ 后，通过匈牙利方法求解最优的唯一点对匹配集合 $H(\mathcal{P}, \mathcal{P}') = \{(p_0, p'_{h_0}), (p_1, p'_{h_1}), \ldots\}$，然后在这些最优点对之间计算均方误差：

$$\mathcal{L}_{\mathrm{rec}} = \sum_{0 \leq k < |\mathcal{P}|} || p_k - p'_{h_k} ||_2^2$$

这一改变从根本上改变了优化目标的性质：Chamfer 距离鼓励“覆盖”，而线性分配损失强制“一一对应”，从而在保持点云整体分布的同时，建立了明确的点级别对应关系。消融实验（Table 2）证实，移除线性分配后重建误差显著上升。

### 3. 序列级 Dropout 与旋转位置嵌入

在正则化策略上，PUMPS 引入了两项关键改进：

- **序列级 Dropout**：传统逐元素 Dropout 会随机丢弃序列中不同位置的不同特征，破坏时序连续性。PUMPS 采用序列级 Dropout 策略——同一特征维度在整个时间序列上被统一遮盖，从而在正则化特征重要性的同时保持运动动态的稳定性（Sec. 3.1）。消融实验表明，逐元素 Dropout 会导致运动轨迹的不连续抖动。

- **旋转位置嵌入（RoPE）**：解码器 $\Phi^{\mathrm{dec}}$ 使用旋转自注意力（RoPE）替代传统的正弦位置嵌入，以更有效地建模时间序列中的相对位置关系，提升时序建模的准确性（Sec. 3.2）。

### 创新总结

上述三个 changed slots 构成了 PUMPS 方法的核心技术贡献：噪声向量机制解决了点标识问题，线性分配损失解决了点对应优化问题，序列级正则化策略保证了时序一致性。这三者协同作用，使得 PUMPS 能够在无监督预训练设置下，在关键帧插值（L2P: 0.137 vs. CITL 0.186）和运动过渡（L2P: 0.168 vs. CITL 0.255）任务上超越现有有监督方法（Table 1）。



PUMPS采用**两阶段预训练范式**，依次训练自编码器与潜在运动合成器，构建一个骨架无关的通用运动表示。其核心设计围绕**时序点云（Temporal Point Cloud, TPC）**展开——将运动序列表示为一组带有时序一致性的点云帧，从而摆脱对特定骨架拓扑的依赖。

### 管道总览

整个框架由三个主要模块串联构成（图1）：

1. **点云帧编码器 Φ^enc**：将单帧点云压缩为正则化的潜在向量。
2. **TPC重建解码器 Φ^dec**：从潜在向量序列重建完整的TPC，是赋予模型点标识感知能力的关键。
3. **潜在运动合成器 Φ^LMS**：在潜在空间中进行掩码运动补全预训练，赋予模型运动先验。

预训练分两步进行：首先联合训练Φ^enc和Φ^dec，以TPC重建为目标学习紧凑的运动表示；随后冻结Φ^enc，仅训练Φ^LMS，通过掩码潜在序列预测来学习时序动态。这种解耦设计使得学到的表示既可零样本用于运动合成任务，也可作为强先验微调至下游任务。

### 输入输出流

**输入**：一段运动序列被转换为TPC表示。具体而言，从骨架姿态$x$采样得到点云$\mathcal{P}_{x} = \{p_0, p_1, ..., p_{|\mathcal{P}|-1}\}$，每个点$p$包含3D位置坐标和one-hot身体部位分组信息。论文采用256个点，点沿骨骼以均匀分布$\mathcal{U}_{[0.025, 0.075]}$偏移采样。

**编码**：Φ^enc采用PointTransformer架构，通过4层最远点采样（farthest-first pooling）逐层加倍特征维度并将点数压缩至1/4，最终输出512维的潜在向量$v_x \in \mathbb{R}^{|v|}$。编码器对每帧独立操作，生成潜在向量序列$\mathcal{V}$。

**解码与重建**：Φ^dec接收潜在向量序列，通过旋转位置嵌入（RoPE）的自注意力机制建模时序关系。其关键创新在于**高斯噪声向量机制**：为每个点引入一个$|z|$维的高斯噪声向量$z \sim \mathcal{N}(0,1)$，将其附加到每帧的潜在向量上。这些噪声向量充当点标识符，使解码器无需点注意力即可生成时间一致的轨迹。解码器最终输出重建的TPC $\mathcal{P}'$。

**损失函数**：重建损失采用基于匈牙利算法的**线性分配MSE**，而非传统的Chamfer距离：
$$\mathcal{L}_{\mathrm{rec}} = \sum_{0 \leq k < |\mathcal{P}|} || p_k - p_{h_k}' ||_2^2$$
其中$(p_k, p_{h_k}')$为匈牙利算法确定的最优点对。这一设计有效避免了Chamfer距离导致的点向聚类中心塌缩问题。

**预训练**：Φ^LMS以掩码自编码的方式在潜在空间进行运动补全训练。给定部分掩码的潜在序列，合成器预测被遮蔽的潜在向量，损失为预测值与真实值之间的MSE：
$$\mathcal{L}_{\mathrm{LMS}} = \sum_{0 \leq f < |\mathcal{V}|} || v_f - w_f ||_2^2$$

### 关键设计决策

| 设计要素 | 传统做法 | PUMPS方案 | 作用 |
|---------|---------|----------|------|
| 点标识机制 | 点注意力或Chamfer距离隐式处理 | 可学习高斯噪声向量作为显式点标识 | 避免点注意力计算，实现高效轨迹中心生成 |
| 重建损失 | Chamfer距离 | 匈牙利算法线性分配MSE | 防止点分布崩溃，降低重建误差 |
| 时序建模 | 正弦位置嵌入 | 旋转位置嵌入（RoPE） | 提升时序建模准确性 |
| 正则化策略 | 逐元素dropout | 序列级dropout | 保持运动动态连续性，避免不稳定轨迹 |

整体而言，PUMPS通过“噪声向量点标识+线性分配损失”这一因果机制，在无需骨架先验和点注意力的条件下，实现了高效且时间一致的TPC重建，为后续的运动合成预训练奠定了表示基础。

### 补充图表

![[assets/figures/papers/paper_list_l1894_PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Sy/figures/001_Figure_1.jpg]]
*Figure 1: Overview of PUMPS pre-training, zero-shot evaluation, and fine-tuning pipelines. PUMPS consists of an auto-encoder (encoder-decoder modules) and latent synthesis component, which are pre-trained successively*



PUMPS 采用两阶段流水线：自编码器阶段学习点云帧的潜在表示并重建 TPC，潜在运动合成阶段在冻结的编码器特征上进行掩码运动补全预训练（Figure 1）。以下聚焦自编码器的三个核心模块及其关键公式。

### 点云帧编码器 Φ^enc

编码器将单帧点云映射为正则化的潜在向量。给定从姿态 $x$ 采样的点云 $\mathcal{P}_{x} = \{p_0, p_1, ..., p_{|\mathcal{P}|-1}\}$，其中每个点 $p$ 包含 3D 位置和 one-hot 身体部位分组，Φ^enc 采用 PointTransformer 架构，通过 4 层 farthest-first pooling 逐步聚合特征：每层特征维度翻倍，点数量缩减至 1/4，最终输出一个 $|v|$ 维的潜在向量 $v_x \in \mathbb{R}^{|v|}$（Sec. 3.1）。在具体实现中，TPC 由 256 个点组成，点沿骨骼以均匀分布 $\mathcal{U}_{[0.025, 0.075]}$ 的偏移量采样，最终得到 512 维特征向量（Sec. 4.2）。

### TPC 重建解码器 Φ^dec

解码器从潜在向量序列重建 TPC，其核心创新在于通过高斯噪声向量赋予点标识感知能力，同时避免点注意力机制的计算开销。具体流程（Figure 2）：

![[assets/figures/papers/paper_list_l1894_PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Sy/figures/002_Figure_2.jpg]]
*Figure 2: Training strategy of the PUMPS auto-encoder components*

1. **时序变换**：Φ^dec 使用旋转自注意力（RoPE）对潜在序列进行时序感知变换，得到变换后的序列 $T$。
2. **噪声向量注入**：对每个点引入一个 $|z|$ 维的高斯噪声向量 $z \in \mathbb{R}^{|z|} \sim \mathcal{N}(0,1)$，将其附加到 $T$ 中的每个潜在向量上。该噪声向量在解码过程中充当点的采样标识符，使模型能够在无点注意力的条件下生成时间一致的轨迹。
3. **点云生成**：通过 MLP 将增强后的特征解码为预测点云 $\mathcal{P}'$。

### 线性分配重建损失

传统点云重建广泛使用 Chamfer 距离，但该损失倾向于使预测点向聚类中心塌缩，导致点分布崩溃。PUMPS 提出基于匈牙利算法的线性分配损失来解决这一问题。

给定真实点云 $\mathcal{P}$ 和预测点云 $\mathcal{P}'$，匈牙利算法求解最优唯一匹配对集合 $H(\mathcal{P}, \mathcal{P}') = \{(p_0, p_{h_0}'), (p_1, p_{h_1}'), \ldots\}$，重建损失定义为匹配点对之间的均方误差：

$$\mathcal{L}_{\mathrm{rec}} = \sum_{0 \leq k < |\mathcal{P}|} || p_k - p_{h_k}' ||_2^2$$

该损失强制每个预测点与唯一的真实点配对，从根本上避免了点向少数聚类中心聚集的问题。消融实验（Table 2）表明，移除线性分配（改用 Chamfer 距离）会导致重建误差显著上升，验证了该设计的因果作用。

### 潜在运动合成器 Φ^LMS 与预训练损失

在自编码器预训练完成后，冻结 Φ^enc，使用 Φ^LMS 进行掩码运动补全预训练（Figure 3）。给定部分掩码的潜在向量序列，Φ^LMS 预测完整的潜在序列。预训练损失为预测潜在向量 $w_f$ 与真实潜在向量 $v_f$ 之间的 MSE：

![[assets/figures/papers/paper_list_l1894_PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Sy/figures/003_Figure_3.jpg]]
*Figure 3: Motion completion pre-training for the latent motion synthesiser*

$$\mathcal{L}_{\mathrm{LMS}} = \sum_{0 \leq f < |\mathcal{V}|} || v_f - w_f ||_2^2$$

该预训练使 Φ^LMS 学会在潜在空间中补全运动序列，为零样本关键帧插值和运动过渡奠定基础。微调实验表明，预训练特征使下游去噪模型的 MPJPE 降低约 25%（Sec. 5.2），证明了迁移学习的有效性。

### 正则化策略：序列级 Dropout

PUMPS 在 Φ^dec 中采用序列级 dropout 策略：同一特征维度在整个时间序列上被统一遮盖，而非逐元素随机丢弃。这一设计保持了时序连续性，避免了逐元素 dropout 导致的运动动态不稳定。消融实验（Table 2）证实，逐元素 dropout 会显著恶化重建质量，而序列级 dropout 能够稳定运动轨迹的生成。



## 实验与关键发现

### 核心实验设计

PUMPS 在三个层次上验证其有效性：TPC 重建质量、无监督运动合成能力，以及预训练特征在下游任务中的迁移价值。实验使用 AMASS 数据集，TPC 表示采用 256 个点，点云从骨骼上以均匀分布 $\sigma \sim \mathcal{U}_{[0.025, 0.075]}$ 采样偏移生成。编码器 $\Phi^{\mathrm{enc}}$ 采用 4 层最远优先池化，每层特征维度翻倍、点数缩减至 1/4，最终输出 512 维潜在向量。评估指标包括 L2 位置误差（L2P）、L2 四元数误差（L2Q）、标准化功率谱相似度（NPSS）、平均关节位置误差（MPJPE）和平均关节速度误差（MPJVE）。

### 主实验结果

**关键帧插值与运动过渡。** Table 1 报告了在 121 帧运动序列上的零样本合成性能。在 5 帧间隔的关键帧插值任务上，PUMPS 取得 L2P = 0.137，相比有监督的 **CITL**（Mo et al., CVPR 2023）的 0.186 降低 26.3%；NPSS 从 0.536 降至 0.249，降幅达 53.5%。在 15 帧间隔的运动过渡任务上，PUMPS 的 L2P = 0.168，较 CITL 的 0.255 降低 34.1%。值得注意的是，PUMPS 在无监督预训练设置下即超越了专门为此任务设计的有监督方法，验证了 TPC 表示与潜在运动合成器联合预训练的有效性。定性可视化（Figure 4）显示，PUMPS 生成的中间帧在肢体末端位置和整体运动轨迹上与真值高度吻合，而 CITL 在长间隔过渡时出现明显的关节漂移。

**2D-to-3D 运动估计。** Table 3 展示了在 128 帧序列上的微调结果。使用 PUMPS 预训练特征初始化的模型，MPJPE 相比从头训练降低约 40%，MPJVE 降低约 30%。这一迁移效率表明，自编码器学到的骨架无关潜在空间编码了丰富的运动动态先验，即使在下游任务需要适配特定骨架结构时仍能提供有效的初始化。Figure 6 的定性示例显示，预训练模型在舞蹈动作的 3D 重建中能更好地保持肢体比例和运动流畅性。

**运动去噪。** Table 4 报告了去噪性能。PUMPS 预训练特征使去噪模型的 MPJPE 降低约 25%（见 Sec. 5.2），加速度误差同步改善。Figure 7 的轨迹可视化显示，PUMPS 微调模型在恢复下落动作时能有效抑制高频抖动，同时保留真实的运动轨迹。

### 组件消融分析

Table 2 系统消融了自编码器的四个关键设计选择，以线性分配点距离（Lrec）作为评估指标：

![[assets/figures/papers/paper_list_l1894_PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Sy/figures/006_Table_2.jpg]]
*Table 2: Component ablation results of the PUMPS auto-encoder architecture, measured in linearly assigned point distances (Lrec)*

| 消融变体 | Lrec |
|---------|------|
| PUMPS 完整模型 | **0.0029** |
| 无线性分配（改用 Chamfer 距离） | 显著升高 |
| 逐元素 dropout（替代序列级 dropout） | 升高 |
| 正弦位置嵌入（替代 RoPE） | 升高 |

**线性分配损失的核心作用。** 移除匈牙利配对机制、改用 Chamfer 距离后，重建误差大幅上升。Chamfer 距离倾向于将所有预测点拉向输入点云的局部聚类中心，导致点分布崩溃——多个预测点坍缩到同一目标点，丧失了点标识性和时间一致性。线性分配通过强制建立唯一的点对点匹配，从根本上避免了这一退化。

**序列级 dropout 的时序稳定性。** 逐元素 dropout 在每一帧独立随机丢弃特征，破坏了运动序列的时间连续性，导致重建轨迹出现不连续跳变。序列级 dropout 在整个时间维度上统一丢弃同一特征，保留了运动动态的平滑性，验证了时序一致性正则化对 TPC 重建的重要性。

**旋转位置嵌入（RoPE）的优势。** 相比正弦位置嵌入，RoPE 通过旋转矩阵编码相对位置关系，更自然地捕捉帧间时序依赖，在重建精度上表现更优。

### TPC 重建质量对比

Figure 5 将 PUMPS 与 **FoldingNet** 的 TPC 重建结果进行可视化对比。FoldingNet 采用基于折叠的解码策略，生成的点云缺乏清晰的时间轨迹结构，点在不同帧之间出现身份混淆和轨迹交叉。PUMPS 借助噪声向量机制和线性分配损失，生成的点云保持了稳定的点标识性，每个点的运动轨迹清晰可辨，验证了“噪声向量即采样标识”这一核心设计理念。

![[assets/figures/papers/paper_list_l1894_PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Sy/figures/007_Figure_5.jpg]]
*Figure 5: TPC reconstructions comparisons between our method and FoldingNet [62], from the same TPC motion representation*

### 失败模式与局限性

1. **计算效率瓶颈。** 线性分配（匈牙利算法）的计算复杂度随点数增加而增长，在 256 点规模下可接受，但扩展到更大点云或实时应用时可能成为限制因素。论文未探索近似匹配策略以降低计算开销。

2. **骨架微调鸿沟。** 尽管预训练是骨架无关的，微调到 2D-to-3D 估计等任务时仍需针对目标骨架结构进行调整，预训练表示不能完全消除下游适配成本。

3. **拓扑信息丢失。** TPC 点云表示丢弃了骨骼拓扑信息，在需要精确关节角度或骨骼长度约束的任务中可能表现不足。论文未评估在运动学约束下的重建保真度。

4. **长序列生成的未探索空间。** PUMPS 的潜在运动合成器基于掩码重建，未与扩散模型等先进生成框架结合，在极长序列或开放式运动生成场景下的能力未知。

### 补充图表

![[assets/figures/papers/paper_list_l1894_PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Sy/figures/004_Table_1.jpg]]
*Table 1: Keyframe interpolation (left) and motion transition (right)*

![[assets/figures/papers/paper_list_l1894_PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Sy/figures/005_Figure_4.jpg]]
*Figure 4: Keyframe interpolation (left) and motion transition (right) examples on a 61-frame sequence. We leave 15 frames between keyframes for interpolation, and 31 frames between 15-frame windows for transition. For visibility purposes, only every 5th frame is shown. Grey regions indicate frames provided by the input. The ground truth is overlaid in each row for direct comparison*

![[assets/figures/papers/paper_list_l1894_PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Sy/figures/008_Table_3.jpg]]
*Table 3: 2D-to-3D motion estimation method comparisons on 128- frame sequences, using MPJPE (top) and MPJVE (bottom)*

![[assets/figures/papers/paper_list_l1894_PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Sy/figures/009_Figure_6.jpg]]
*Figure 6: Motion estimation on a dance motion sample, given a sequence of 2D keypoints (top row). Predictions are rotated by*

![[assets/figures/papers/paper_list_l1894_PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Sy/figures/010_Table_4.jpg]]
*Table 4: Motion denoising method comparisons on 128-frame sequences, using MPJPE (top) and acceleration error (bottom)*

![[assets/figures/papers/paper_list_l1894_PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Sy/figures/011_Figure_7.jpg]]
*Figure 7: Motion denoising examples given a noisy falling motion sequence (top row). Though only every 5th frame is shown, all frames are included in the trajectory representation (grey lines)*



## 定位与知识库关联

### 1. 方法脉络与基线关系

PUMPS 处于**骨架无关运动表示学习**与**点云序列建模**的交叉点，其核心贡献在于构建了一个无需骨架先验的统一运动预训练范式。该方法与以下几条技术脉络形成对比或继承关系：

**（1）相对于有监督运动合成方法**

传统运动合成方法通常依赖于特定骨架的参数化表示（如 SMPL、Human3.6M 骨架），导致模型难以跨骨架泛化。**CITL**（Mo et al., CVPR 2023）作为基于 Transformer 的关键帧插值有监督基线，在 5 帧间隔的关键帧插值任务上达到 L2P 0.186，而 PUMPS 在无监督预训练设置下将该指标降至 0.137（降低 26.3%）；在 15 帧间隔的运动过渡任务上，PUMPS 的 L2P 为 0.168，显著优于 CITL 的 0.255（降低 34.1%）。这说明骨架无关的点云预训练表示能够捕获更通用的运动动态，即便不依赖特定骨架标注也能超越有监督方法。

**（2）相对于点云重建方法**

在 TPC（Temporal Point Cloud）重建层面，PUMPS 直接回应了传统点云解码器（如 **FoldingNet**）在处理时序点云时的两个核心缺陷：点标识缺失和点分布崩溃。FoldingNet 使用 Chamfer 距离作为重建损失，但该损失倾向于将所有预测点推向目标点云的聚类中心，导致生成的点云失去结构多样性。PUMPS 通过两项关键设计解决了这一问题：

- **线性分配损失**：采用匈牙利算法确定预测点与目标点之间的最优一一配对，然后计算配对的 MSE 损失。消融实验（Table 2）表明，移除线性分配（退化为 Chamfer 距离）会导致重建误差显著上升。
- **高斯噪声向量作为点标识**：在解码器的潜在序列中附加可学习的高斯噪声向量 $z \in \mathbb{R}^{|z|} \sim \mathcal{N}(0,1)$，使每个点获得独特的“身份签名”，从而在无需点注意力机制的情况下生成时间一致的轨迹。

**（3）相对于掩码预训练方法**

PUMPS 的预训练策略借鉴了掩码自编码的思想，但与 **MAE**（He et al., CVPR 2022）和 **Point-BERT**（Yu et al., CVPR 2022）存在本质差异。MAE 和 Point-BERT 的掩码策略作用于原始信号空间（图像 patch 或点云局部区域），而 PUMPS 的掩码作用于编码后的潜在向量序列。这种设计使得预训练任务（关键帧插值、运动过渡、运动预测）直接对应于下游运动合成任务，避免了“预训练-微调”之间的任务鸿沟。

**（4）相对于运动先验方法**

**Pose-NDF**（Tiwari et al., ECCV 2022）和 **HuMoR**（Rempe et al., ICCV 2021）分别通过神经距离场和 VAE 学习运动先验，但它们仍依赖于特定的骨架参数化。PUMPS 的骨架无关特性使其能够直接应用于不同骨架结构的运动数据，无需重新训练或骨架重定向。在运动去噪任务上，PUMPS 预训练特征使微调后的去噪模型 MPJPE 降低约 25%（Sec. 5.2），验证了骨架无关预训练表示的迁移有效性。

### 2. 技术适用边界

PUMPS 的适用边界由以下设计选择决定：

**（1）点云分辨率与计算效率**

线性分配（匈牙利算法）的时间复杂度为 $O(n^3)$，其中 $n$ 为点云点数。PUMPS 默认使用 256 个点，在此规模下计算开销可控，但若扩展到更大规模点云（如密集人体网格采样或多人场景），线性分配损失将成为计算瓶颈。这一限制在实时应用或高分辨率点云场景中尤为突出。

**（2）骨架无关性的代价**

虽然点云表示天然具有骨架无关的优势，但同时也丢失了骨骼拓扑信息（如关节父子关系、骨骼长度约束）。在需要精确关节角度或物理合理性约束的任务（如物理仿真、运动学逆解算）中，PUMPS 的纯点云表示可能无法满足精度要求。此外，在微调到特定任务（如 2D-to-3D 估计）时，仍需针对目标骨架结构进行调整，骨架无关性仅在预训练阶段完全成立。

**（3）序列长度与运动长期依赖**

PUMPS 的潜在运动合成器 $\Phi^{\mathrm{LMS}}$ 基于 Transformer 架构，其自注意力的计算复杂度随序列长度平方增长。论文中的实验主要针对 121 帧和 128 帧序列，对于更长时间跨度的运动生成（如数分钟的动作序列），模型可能面临注意力窗口限制和长期依赖建模不足的问题。

### 3. 局限与开放问题

**已知局限：**

1. **线性分配的可扩展性**：匈牙利算法的 $O(n^3)$ 复杂度限制了 TPC 点数的上限，难以直接应用于需要高密度点采样的场景。
2. **骨架拓扑信息的丢失**：点云表示放弃了骨骼结构先验，在需要精确关节角度的任务中存在先天不足。
3. **生成框架的集成**：论文未探索将 PUMPS 与扩散模型等高级生成框架结合，其在长序列生成和多样化运动合成方面的潜力有待挖掘。

**开放问题：**

1. **线性分配损失的理论机制**：尽管实验证明线性分配损失优于 Chamfer 距离，但其在优化过程中如何具体避免点崩溃的理论分析仍不明确。是否可以通过最优传输理论（Optimal Transport）提供更严格的理论保证？
2. **序列级 dropout 的正则化原理**：消融实验表明，逐元素 dropout 会导致不稳定的运动动态，而序列级 dropout（同一特征在整个时间序列上被遮盖）能保持连续性。这一现象背后的动力学机制值得深入分析——是否因为序列级 dropout 强制模型学习更鲁棒的时序特征而非依赖单帧线索？
3. **预训练表示的更高效利用**：PUMPS 目前采用全量微调的方式迁移到下游任务。适配器（Adapter）或提示学习（Prompt Tuning）等参数高效微调策略能否在保持性能的同时进一步降低迁移成本？
4. **TPC 表示的任务泛化性**：TPC 表示是否能够扩展到动作识别、运动风格迁移、运动质量评估等更广泛的运动相关任务？这些任务对点标识和时序一致性的需求可能与运动合成存在差异。
5. **与扩散模型的协同设计**：基于注意力机制的架构能否有效应用于扩散框架中的运动合成？PUMPS 的噪声向量机制是否可以为扩散模型的去噪过程提供结构化的条件信号？



## 原文 PDF

![[paperPDFs/ICCV_2025/PUMPS_Skeleton_Agnostic_Point_based_Universal_Motion_Pre_Training_for_Synthesis_in_Human_Motion_Tasks.pdf]]
