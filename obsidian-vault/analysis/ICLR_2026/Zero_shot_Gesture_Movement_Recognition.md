---
title: "EMBRIDGE: ENHANCING GESTURE GENERALIZATION FROM EMG SIGNALS THROUGH CROSS-MODAL REPRESENTATION LEARNING"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Zero_shot_Gesture_Movement_Recognition.pdf
aliases:
- EMBRIDGE
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过将EMG表示与高质量的冻结姿态表示进行跨模态对齐，利用软对比学习（CASCLe）保留姿态空间的几何结构，并辅以掩码姿态重建损失，使EMG编码器捕获姿态相关的语义，从而提升零样本泛化能力。
primary_logic: 以冻结的预训练姿态编码器作为结构锚点，通过Q-Former提取姿态信息、掩码重建强制保留姿态内容、社区感知软对比学习对齐相对几何结构，构建了一个结构化的EMG表示空间，首次实现了可穿戴EMG信号的零样本手势分类。
claims:
- EMBridge在emg2pose未见手势零样本分类上超越所有基线，达到0.528的平衡准确率
- CASCLe软目标优于传统对比学习和标签平滑，移除任何组件均导致零样本性能下降
- 在仅使用40%配对数据时，EMBridge的零样本性能仍超过全量单模态基线的线性探测性能
- 框架在不增加参数量或额外传感器的情况下实现了零样本手势识别能力
---

# EMBRIDGE: ENHANCING GESTURE GENERALIZATION FROM EMG SIGNALS THROUGH CROSS-MODAL REPRESENTATION LEARNING

> [!tip] 核心洞察
> 以冻结的预训练姿态编码器作为结构锚点，通过Q-Former提取姿态信息、掩码重建强制保留姿态内容、社区感知软对比学习对齐相对几何结构，构建了一个结构化的EMG表示空间，首次实现了可穿戴EMG信号的零样本手势分类。

| 字段 | 内容 |
|------|------|
| 中文题名 | EMBridge：通过跨模态表示学习增强EMG手势泛化 |
| 英文题名 | EMBRIDGE: ENHANCING GESTURE GENERALIZATION FROM EMG SIGNALS THROUGH CROSS-MODAL REPRESENTATION LEARNING |
| 会议/期刊 | ICLR 2026 |
| Links | [arXiv](https://arxiv.org/abs/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | EMBridge |
| Dataset | emg2pose unseen gestures, emg2pose in-dist. gestures, NinaPro in-dist. gestures |

> [!tip] 效果简介
> - emg2pose unseen gestures 上，Balanced Accuracy (Zero-shot) 0.528 vs 0.481 (CPEP) (+0.047)。
> - emg2pose in-dist. gestures 上，Balanced Accuracy (Zero-shot) 0.777 vs 0.763 (Q-Former) (+0.014)。
> - NinaPro in-dist. gestures 上，Balanced Accuracy (Zero-shot) 0.692 vs 0.618 (Q-Former-LS) (+0.074)。

## 概述

**问题瓶颈**：表面肌电（EMG）信号因高噪声、高变异性和数据规模有限，导致单模态自监督学习（如EMG‑MAE）难以获得具有判别力和泛化性的表示空间——尤其在未见手势上，EMG嵌入缺乏语义结构，无法支撑零样本分类。

**核心思路**：EMBridge提出以冻结的高质量姿态编码器作为结构锚点，通过跨模态表示学习将EMG嵌入空间对齐到姿态空间的几何结构上。框架由三个组件构成：查询Transformer（Q‑Former）从EMG编码器中提取姿态信息特征；掩码姿态重建损失（MPRL）强制查询捕获被掩码的姿态token内容；社区感知软对比学习（CASCLe）利用姿态嵌入的k‑means聚类构建软目标，保留姿态空间的相对几何关系。这一非对称设计仅优化EMG侧，首次在可穿戴EMG上实现了零样本手势分类。

**关键实证**：在emg2pose未见手势零样本分类上，EMBridge达到0.528的平衡准确率，超越所有基线（最佳基线CPEP为0.481）；每用户平均F1分数达0.522，较CPEP提升14.2%。消融实验表明，移除Q‑Former、MPRL或CASCLe均导致零样本性能下降，CASCLe的软目标优于传统InfoNCE和标签平滑。在仅使用40%配对数据时，EMBridge的零样本性能仍超过全量单模态基线的线性探测性能。框架在不增加参数量或额外传感器的条件下实现了未见手势的零样本识别能力。

## 背景与动机

表面肌电图（sEMG）通过非侵入式传感器记录肌肉电活动，是实现可穿戴手势交互的关键信号源。然而，EMG信号固有的高噪声、高变异性和有限的数据规模，使得从单模态信号中学习具有判别性和泛化性的表示极为困难。如图1(a)所示，即使采用相同的掩码自编码器（MAE）预训练，姿态嵌入在语义空间中有序分布、按手势类别清晰分离，而EMG嵌入则杂乱无章——这一结构性鸿沟直接限制了EMG单模态模型在未见手势上的表现，成为本领域的核心瓶颈。

现有方法大致分为两类。单模态自监督预训练方法（如**EMG-MAE**）仅利用EMG信号进行掩码重建，虽能捕获局部时序模式，但缺乏语义引导，难以构建全局结构化的表示空间。有监督的EMG-姿势回归模型（如**emg2pose**、**Vemg2pose**、**NeuroPose**，Salter et al., 2024）虽引入了姿态信息，但采用端到端回归范式，训练目标聚焦于逐帧重建精度而非表示空间的语义结构，且未见手势的泛化能力受限于回归任务的封闭性假设。

多模态对比学习为弥合跨模态差距提供了新思路。**CPEP**（Cui et al., 2025）通过投影层将EMG和姿态嵌入对齐到共享空间，采用标准InfoNCE损失拉近配对样本、推远非配对样本。然而，这种硬目标对比存在根本缺陷：它将所有非配对样本视为同等负样本，完全忽略了姿态空间中丰富的几何结构——语义相近的姿态被无差别排斥，导致对齐后的EMG表示空间丢失了姿态空间的相对几何关系，限制了零样本泛化的上限。

EMBridge的核心动机正源于此：**以冻结的高质量姿态编码器作为结构锚点，通过跨模态表示学习将姿态空间的语义结构“注入”到EMG编码器中**。其关键洞察在于——不应仅对齐单个样本对，而应对齐两个模态空间的相对几何结构。这意味着，若两个姿态在嵌入空间中语义邻近，其对应的EMG表示也应保持相似的邻近关系。通过这一结构化对齐，EMG编码器得以捕获姿态相关的语义信息，从而首次实现可穿戴EMG信号的零样本手势分类能力，且不增加额外参数量或传感器需求。

## 核心创新

EMBridge 的核心创新在于构建了一套**结构化的跨模态对齐机制**，将冻结的高质量姿态表示空间作为几何锚点，通过三个相互协同的组件重塑 EMG 表示空间，从而首次实现可穿戴 EMG 信号的零样本手势分类。

### 1. 非对称对齐架构：以冻结姿态编码器为锚点

与传统的对称式跨模态对比学习（如 CLIP 风格的 InfoNCE 对齐）不同，EMBridge 采用**非对称对齐架构**（changed slot: 对齐架构）。姿态编码器在预训练后完全冻结，仅优化 EMG 侧参数。这一设计的因果逻辑在于：同一 MAE 预训练范式下，姿态嵌入天然具备语义结构化、类间分离清晰的特性，而 EMG 嵌入则高度混杂（见 Figure 1(a)）。冻结姿态编码器使其成为不可动摇的几何锚点，强制 EMG 编码器向结构化的姿态空间靠拢，而非双向妥协导致表示退化。

在此架构中，引入了一个**查询 Transformer（Q-Former）** 作为信息瓶颈：4 个自注意力块叠加 2 个交叉注意力层，以一组可学习查询向量从 EMG 编码器的输出中提取姿态相关信息。消融实验证实，移除 Q-Former（退化为 CPEP + CASCLe）导致未见手势零样本平衡准确率从 0.528 降至 0.494（Table 3），验证了该瓶颈结构的必要性。

### 2. 社区感知软对比学习（CASCLe）：保留姿态空间的相对几何结构

传统对比学习使用 one-hot 硬目标，仅将配对样本视为正例，忽略了样本间丰富的语义相似度层级（changed slot: 对比学习目标）。CASCLe 的核心洞察是：**对齐的不应仅是实例级的配对关系，更应是跨模态空间的相对几何结构**。

具体而言，CASCLe 首先对冻结姿态编码器的嵌入进行离线 k-means 聚类，构建姿态社区。对每个姿态样本，计算其到各簇中心的亲和度向量，经稀疏化（仅保留 top-k 最近簇）后，通过温度缩放生成软目标分布 $\tilde{y}_{ij}$——即姿态 $j$ 是姿态 $i$ 语义邻居的概率（Equation 4）。最终以交叉熵损失使 EMG-姿态相似度矩阵匹配该软目标分布（Equation 5）。

消融实验表明，CASCLe 的软目标策略显著优于标签平滑（0.528 vs 0.511）和 SoftCLIP 变体（0.510），移除 CASCLe 仅保留 InfoNCE 使性能降至 0.509（Table 3）。这证明保留姿态空间的社区结构——而非简单软化标签——是提升泛化的关键。

### 3. 掩码姿态重建损失（MPRL）：强制查询携带姿态内容

作为辅助学习目标（changed slot: 辅助学习目标），MPRL 随机掩码部分姿态 token，要求 Q-Former 的输出查询向量通过一个轻量解码器 $g(\cdot)$ 重建被掩码的 token（Equation 2）。该损失强制可学习查询不仅对齐姿态嵌入的全局语义，更需捕获细粒度的姿态内容信息。移除 MPRL 使零样本性能从 0.528 降至 0.516（Table 3），验证了其对查询质量的补充作用。

### 4. 三组件协同：从实例对齐到结构对齐的范式跃迁

三个组件的协同机制可概括为：**Q-Former 决定“从 EMG 中提取什么”，CASCLe 决定“对齐到什么结构”，MPRL 确保“提取的信息包含姿态内容”**。总训练目标为三者的加权组合：

$$\mathcal{L} = \mathcal{L}_{\mathrm{InfoNCE}} + \alpha \mathcal{L}_{\mathrm{CASCLe}} + \lambda \mathcal{L}_{\mathrm{MPRL}}$$

这一设计使 EMG 表示空间从单模态 MAE 预训练后的杂乱无章，转变为继承姿态空间语义结构的可迁移表示。在仅使用 40% 配对数据时，EMBridge 的零样本性能仍超过全量单模态基线的线性探测性能（Figure 3(c)），证明了结构化对齐的高数据效率。

**需手动验证的点**：论文未提供各损失权重 $\alpha$、$\lambda$ 的具体取值及其调参过程，该信息需从原文补充材料或代码中确认。

## 整体框架

EMBridge 的核心思想是**以冻结的姿态编码器为结构锚点，通过跨模态对齐将 EMG 表示空间结构化**，从而赋予单模态 EMG 编码器零样本手势分类能力。整体 pipeline 由三个关键模块串联构成：查询 Transformer（Querying Transformer, Q-Former）、掩码姿态重建损失（Masked Pose Reconstruction Loss, MPRL）和社区感知软对比学习损失（Community-Aware Soft Contrastive Learning, CASCLe）。

**输入输出流**：给定成对数据集 $\mathcal{D} = \{ (\mathbf{x}_i, \mathbf{p}_i, y_i) \}_{i=1}^{N}$，其中 $\mathbf{x}_i$ 为 EMG 信号序列，$\mathbf{p}_i$ 为对应的姿态序列，$y_i$ 为手势标签。EMG 信号和姿态序列分别经过预训练的单模态 MAE 编码器（Transformer encoder，patch 长度 $S=200$，掩码比 0.5）映射为 $d$ 维 token 嵌入。随后，**Q-Former** 以一组可学习查询（learnable queries）从 EMG 编码器的输出中提取姿态信息特征，通过 4 个自注意力块加 2 个交叉注意力层实现信息瓶颈压缩。在训练阶段，Q-Former 的输出同时驱动两个损失：**MPRL** 对随机掩码的姿态 token 进行 MSE 重建，强制查询携带姿态内容信息；**CASCLe** 则利用离线 k-means 聚类构建的姿态社区结构生成软目标，对齐跨模态嵌入空间的相对几何关系。最终训练目标为三项损失的加权组合：

$$\mathcal{L} = \mathcal{L}_{\mathrm{InfoNCE}} + \alpha \mathcal{L}_{\mathrm{CASCLe}} + \lambda \mathcal{L}_{\mathrm{MPRL}}$$

**非对称对齐策略**：框架采用非对称设计——姿态编码器完全冻结，仅优化 EMG 侧的编码器和 Q-Former。这一设计使姿态空间成为不可动摇的语义锚点，EMG 表示被强制向该锚点对齐，从而间接获得姿态空间中的语义结构和类别分离性（Figure 1a 展示了 MAE 预训练后姿态嵌入已具有良好的手势聚类结构，而 EMG 嵌入则杂乱无章）。

**下游推理**：预训练完成后，EMBridge 支持两种下游手势分类范式：**线性探测（LP）** 在冻结编码器上训练随机初始化的线性分类头；**零样本分类（ZS）** 则直接在嵌入空间中检索 top-k 最近邻姿态，通过 KNN 投票预测手势标签，无需任何已见手势的标注数据。值得注意的是，在 LP 中 EMBridge 采用查询平均策略（而非选择与配对姿态相似度最大的查询），论文指出这可能是其在未见手势 LP 上略低于 CPEP 的原因，但避免了数据泄漏风险。

**与基线的关键差异**：相比 CPEP（Cui et al., 2025）等对称 InfoNCE 对齐基线，EMBridge 的改动集中在三个“槽位”：对齐架构从投影层升级为 Q-Former 非对称瓶颈；对比目标从硬 one-hot 升级为社区感知软目标；并额外引入掩码重建作为辅助任务。这些改动不增加参数量或额外传感器，却首次实现了可穿戴 EMG 信号的零样本手势分类（Table 2, ZS unseen 0.528 vs. CPEP 0.481）。

### 补充图表

![[assets/figures/papers/paper_list_l1645_Zero_shot_Gesture_Movement_Recognition/figures/001_Figure_1.jpg]]
*Figure 1: (a) Motivation for cross-modal representation learning: using the same MAE pre-training, pose embeddings are semantically structured and well-separated across gestures (colors), whereas EMG embeddings are not. This motivates leveraging pose as guidance to structure the EMG representation space. (b) Detailed architecture of EMBridge. Only one transformer block (self-attention, cross-attention, and feed-forward layers) is shown for clarity, the model uses four such blocks*

## 核心模块与公式推导

EMBridge 的核心由三个模块构成：**查询Transformer (Q-Former)**、**掩码姿态重建损失 (MPRL)** 和**社区感知软对比学习 (CASCLe)**。三个模块协同工作，以冻结的姿态编码器为锚点，将EMG表示空间结构化对齐到姿态语义空间。

---

### 查询Transformer (Q-Former)

Q-Former 作为信息瓶颈，从EMG编码器输出中提取姿态相关信息。其结构包含4个自注意力块和2个交叉注意力层，使用一组可学习的查询向量与EMG编码器的输出进行交叉注意力交互。与对称架构（如CLIP）不同，EMBridge采用非对称设计：姿态编码器冻结，仅在EMG侧优化参数。

Q-Former输出的查询token与冻结姿态编码器产生的姿态嵌入通过**实例级对比损失 (InfoNCE)** 进行对齐：

$$\mathcal{L}_{\mathrm{InfoNCE}} = -\frac{1}{B}\sum_{i=1}^{B}\sum_{j=1}^{B} I_{ij} \log q_{ij}$$

其中 $B$ 为批量大小，$I_{ij}$ 是指示函数（当 $i=j$ 时取1），$q_{ij}$ 是第 $i$ 个查询token与第 $j$ 个姿态嵌入的归一化相似度。该损失强制选出的查询token与对应的姿态嵌入匹配。

---

### 掩码姿态重建损失 (MPRL)

MPRL 作为辅助任务，强制Q-Former的查询向量捕获姿态token级别的信息。具体而言，随机掩码姿态序列中的部分token，Q-Former的输出通过一个轻量解码器 $g(\cdot)$ 重建被掩码的token：

$$\mathcal{L}_{\mathrm{MPRL}} = \frac{1}{|\mathcal{M}|} \sum_{m \in \mathcal{M}} \| g(H_{P}[m]) - P[m] \|_{2}^{2}$$

其中 $\mathcal{M}$ 是被掩码的姿态token索引集合，$H_P[m]$ 是Q-Former输出的第 $m$ 个姿态位置表示，$P[m]$ 是真实的姿态token。该MSE损失确保查询向量中保留了足够的姿态内容信息。

---

### 社区感知软对比学习 (CASCLe)

传统InfoNCE使用硬目标（one-hot），忽略了姿态空间中样本间的语义邻近关系。CASCLe通过构建软目标来保留姿态空间的相对几何结构。

**构建过程：**

1. **离线聚类**：对预训练Pose-MAE产生的姿态嵌入进行k-means聚类，获得 $N_c$ 个簇中心 $C$。
2. **姿态-簇亲和度计算**：计算每个姿态嵌入与簇中心的余弦相似度，得到亲和度矩阵 $S_{p,c}$。
3. **稀疏化**：仅保留每个姿态的top-k最近簇，其余置零：

$$[S_{p,c}]_{ij} \gets \begin{cases} [S_{p,c}]_{ij}, & j \in \mathrm{TopK}(S_{p,c}[i,:]), \\ 0, & \mathrm{otherwise}. \end{cases}$$

4. **姿态-姿态相似度**：基于稀疏化后的亲和度向量计算姿态间的余弦相似度 $\bar{S}_{p,p}$。
5. **软目标生成**：通过温度参数 $\tau_s$ 将相似度转为概率分布：

$$\tilde{y}_{ij} = \frac{\exp(\bar{S}_{p,p}[i,j] / \tau_s)}{\sum_{k \ne i} \exp(\bar{S}_{p,p}[i,k] / \tau_s)}, \quad j \ne i$$

其中 $\tilde{y}_{ij}$ 表示姿态 $j$ 是姿态 $i$ 的语义邻居的概率。

6. **CASCLe损失**：以软目标为监督信号，计算交叉熵：

$$\mathcal{L}_{\mathrm{CASCLe}} = -\frac{1}{B} \sum_{i=1}^{B} \sum_{j=1}^{B} \tilde{y}_{ij} \log q_{ij}$$

---

### 总训练目标

三个损失加权组合为最终优化目标：

$$\mathcal{L} = \mathcal{L}_{\mathrm{InfoNCE}} + \alpha \mathcal{L}_{\mathrm{CASCLe}} + \lambda \mathcal{L}_{\mathrm{MPRL}}$$

其中 $\alpha$ 和 $\lambda$ 为平衡系数。InfoNCE负责实例级对齐，CASCLe保留社区级几何结构，MPRL强化姿态内容提取，三者互补构建结构化的跨模态表示空间。

### 补充图表

![[assets/figures/papers/paper_list_l1645_Zero_shot_Gesture_Movement_Recognition/figures/002_Figure_2.jpg]]
*Figure 2: Unlike conventional contrastive loss that relies on one-hot targets, (a). CASCLe constructs soft targets based on community-level similarity. Each community is represented by affinities to cluster centroids, and pose–pose similarity is computed from affinity vectors. Soft targets used in CASCLe are shown in (b), computed from a batch of 64 samples for clearer visualization*

## 实验与分析

### 数据集与评估协议

实验在两个公开数据集上进行：**emg2pose** 和 **NinaPro**。emg2pose 数据集包含 6 种手势，其中 4 种作为分布内（in-distribution）手势用于训练和对齐，2 种作为未见（unseen）手势用于评估零样本泛化能力（Table 1）。NinaPro 数据集用于验证跨数据集的迁移性。评估协议包含两种设置：

![[assets/figures/papers/paper_list_l1645_Zero_shot_Gesture_Movement_Recognition/figures/003_Table_1.jpg]]
*Table 1: Dataset splits with gesture and user counts. Four unseen gestures evaluated out of six total*

- **线性探测（Linear Probing, LP）**：冻结编码器，仅训练随机初始化的线性分类头。
- **零样本分类（Zero-Shot, ZS）**：基于嵌入空间的 k-近邻检索投票机制——对每个 EMG 样本检索其 top-k 个最近邻姿态样本，取这些姿态对应手势标签的众数作为预测结果。

### 主实验结果

**Table 2** 报告了核心对比结果。在 emg2pose 数据集的未见手势零样本分类上，EMBridge 达到 **0.528** 的平衡准确率，显著超越所有基线方法，比最强的多模态对比基线 **CPEP**（Cui et al., 2025）的 0.481 高出 **+0.047**。在分布内手势的零样本分类上，EMBridge 以 0.777 优于 Q-Former 的 0.763。在 NinaPro 数据集上，EMBridge 的零样本准确率达到 0.692，比 Q-Former-LS 的 0.618 提升 **+0.074**，表明框架具有良好的跨数据集泛化能力。

**Figure 3** 进一步揭示了 EMBridge 的优势来源：
- **Figure 3(a)** 的混淆矩阵显示，EMBridge 在未见手势的逐类 F1 分数上全面优于 CPEP 和 Q-Former（如 Class 1: 0.513 vs 0.439/0.494；Class 3: 0.504 vs 0.436/0.458），说明模型并非仅在易分类别上取得提升。
- **Figure 3(b)** 的逐用户分析表明，EMBridge 在所有用户上均保持一致的性能优势，平均 F1 达到 0.522，比 CPEP 的 0.457 相对提升 **+14.2%**，证明改进具有跨用户鲁棒性。
- **Figure 3(c)** 的数据效率实验显示，当仅使用 **40%** 的配对数据进行训练时，EMBridge 的零样本性能（约 0.45）仍超过全量数据下单模态基线 **EMG-MAE** 的线性探测性能（虚线标注），验证了跨模态对齐对数据效率的显著提升。

![[assets/figures/papers/paper_list_l1645_Zero_shot_Gesture_Movement_Recognition/figures/005_Figure_3.jpg]]
*Figure 3: (a) Confusion matrices from ZS on unseen gestures, with per-class F1 scores shown beside row labels. (b) Per-user ZS performance on unseen gestures. (c) Data efficiency analysis via ZS on in-dist. and unseen gestures. Dotted lines indicate LP performance of unimodal baselines*

**Figure 8** 的小样本实验进一步证实，EMBridge 在线性探测中只需极少量标注样本（如 5-shot）即可达到较高准确率，且随样本数增加性能稳定提升。

### 消融研究

**Table 3** 系统消融了 EMBridge 各组件和软对比目标设计的贡献，所有实验均在 emg2pose 未见手势零样本设置下进行：

| 消融配置 | ZS Unseen 准确率 | 性能损失 |
|---------|-----------------|---------|
| EMBridge（完整） | 0.528 | — |
| 移除 Q-Former（退化为 CPEP + CASCLe） | 0.494 | -0.034 |
| 移除 MPRL | 0.516 | -0.012 |
| 移除 CASCLe（仅保留 InfoNCE） | 0.509 | -0.019 |
| CASCLe 替换为标签平滑 | 0.511 | -0.017 |
| CASCLe 替换为 SoftCLIP 变体 | 0.510 | -0.018 |

**关键发现：**
1. **Q-Former 是最关键的组件**：移除后性能下降 0.034，验证了非对称查询架构在提取姿态相关信息中的核心作用。
2. **CASCLe 软对比目标优于传统软化策略**：标签平滑和 SoftCLIP 变体均无法达到 CASCLe 的性能（0.511、0.510 vs 0.528），说明基于姿态社区结构生成的软目标比简单的标签软化更有效。
3. **MPRL 提供稳定的辅助增益**：移除掩码姿态重建损失使性能下降 0.012，证明强制查询捕获姿态 token 信息有助于表示学习。
4. **三组件协同作用**：同时移除多个组件会导致性能进一步下降，说明三者之间存在互补效应。

### 超参数敏感性

**Figure 4** 分析了关键超参数的影响：
- **可学习查询数量**：16 个查询达到最佳性能。8 个查询信息不足，32 个查询可能导致过拟合，性能反而下降。
- **CASCLe 的 top-k 邻居数**：随着 k 增加（从 1 到 5），零样本性能逐步提升后趋于饱和，表明适度的社区范围扩展有助于捕获语义邻近关系，但过大范围会引入噪声。
- **软目标温度 τ_s 和簇数 k_c**：Figure 9 展示了不同参数下的软目标分布，温度控制软目标的尖锐程度，簇数影响社区划分粒度，两者共同决定软目标的质量。

![[assets/figures/papers/paper_list_l1645_Zero_shot_Gesture_Movement_Recognition/figures/012_Figure_9.jpg]]
*Figure 9: Soft targets from a batch of 64 samples for clearer visualization. We vary the value of temperature*

**Table 4** 显示批量大小对零样本性能的影响：较大的批量（如 128）通过提供更丰富的负样本和更稳定的社区结构估计，带来性能提升，但计算成本也随之增加。

### 失败模式与局限性

1. **线性探测的次优表现**：在 emg2pose 未见手势的线性探测中，EMBridge（0.505）略低于 CPEP（0.538）。论文将此归因于查询平均策略的次优选择——为避免数据泄漏，EMBridge 对所有查询取平均而非选择与配对姿态相似度最大的查询。若改用最大相似度选择，可能缩小这一差距，但需验证是否引入泄漏风险。

2. **零样本检索的敏感性**：当前零样本分类依赖 KNN 投票，对支持集的类别分布和噪声敏感。在类别不平衡或支持集质量较差时，检索结果可能偏向多数类。

3. **社区划分的刚性**：CASCLe 使用离线 k-means 硬聚类构建社区，限制了社区边界的柔性表达。姿态嵌入空间中可能存在模糊归属的样本，硬分配会引入噪声软目标。

4. **模态依赖性**：框架依赖成对的 EMG-姿态数据进行预训练，未利用大规模未配对姿态数据。在仅使用 40% 配对数据时虽有优势，但完全无配对数据的场景下无法应用。

5. **评估范围有限**：实验仅覆盖两个公开数据集，迁移至不同穿戴设备、不同电极配置或真实噪声环境下的鲁棒性有待验证。

### 可视化分析

**Figure 6** 和 **Figure 7** 分别展示了分布内和未见手势嵌入的 t-SNE 可视化。EMBridge 的嵌入在两种设置下均形成更紧凑、类间分离更清晰的簇结构，而单模态基线的嵌入则呈现重叠和分散。这直观验证了跨模态对齐有效结构化了 EMG 表示空间，使手势语义在嵌入空间中更可区分——即使是训练中未见的手势类别。

### 补充图表

![[assets/figures/papers/paper_list_l1645_Zero_shot_Gesture_Movement_Recognition/figures/004_Table_2.jpg]]
*Table 2: Comparison of gesture classification results across unimodal and multi-modal models. Results are reported on the emg2pose dataset and the NinaPro dataset*

![[assets/figures/papers/paper_list_l1645_Zero_shot_Gesture_Movement_Recognition/figures/006_Table_3.jpg]]
*Table 3: Ablation of EMBridge: individual component impact and soft contrastive objectives*

![[assets/figures/papers/paper_list_l1645_Zero_shot_Gesture_Movement_Recognition/figures/007_Figure_4.jpg]]
*Figure 4: Sensitivity to hyper-parameters. Dashed lines indicate the values used in the best setup*

![[assets/figures/papers/paper_list_l1645_Zero_shot_Gesture_Movement_Recognition/figures/009_Figure_6.jpg]]
*Figure 6: t-SNE visualization of embeddings from in-dist. gestures, colored by gesture class labels*

![[assets/figures/papers/paper_list_l1645_Zero_shot_Gesture_Movement_Recognition/figures/010_Figure_7.jpg]]
*Figure 7: t-SNE visualization of embeddings from unseen gestures, colored by gesture class labels*

![[assets/figures/papers/paper_list_l1645_Zero_shot_Gesture_Movement_Recognition/figures/011_Figure_8.jpg]]
*Figure 8: Few-shot evaluation of EMBridge. X-axis is the number of training samples within each class (n-shot) during linear probing. For each number of shots, we repeat random sampling five times to obtain a more reliable estimate of performance. We report the average balanced accuracy, with the standard deviation indicated as a shaded region*

![[assets/figures/papers/paper_list_l1645_Zero_shot_Gesture_Movement_Recognition/figures/013_Table_4.jpg]]
*Table 4: Impact of batch size on zero-shot classification performance of unseen gestures*

## 方法谱系与知识库定位

### 1. 核心瓶颈与设计动机

EMG手势识别面临的核心瓶颈在于：EMG信号固有的高噪声、高用户间变异性和有限的数据规模，导致单模态自监督预训练（如EMG-MAE）学到的表示缺乏判别性和语义结构。即使使用相同的MAE预训练范式，姿态嵌入空间呈现出清晰的按手势类别分离的几何结构，而EMG嵌入空间则高度混杂（Figure 1a）。这一观察构成了EMBridge跨模态表示学习的基本动机：以冻结的高质量姿态编码器作为结构锚点，引导EMG编码器学习具有语义判别力的表示空间。

### 2. 与现有方法的关系定位

#### 2.1 单模态基线

EMBridge直接对比了以下单模态方法：
- **EMG-MAE**：仅使用EMG信号进行掩码自编码预训练，无跨模态监督。其在未见手势上的零样本分类完全失效（平衡准确率接近随机水平），因为缺乏将EMG模式映射到语义手势类别的机制。
- **NeuroPose / emg2pose / Vemg2pose / PoseT**（Salter et al., 2024）：有监督的EMG-姿态回归模型，通过回归手部关键点来间接实现手势理解。这些方法依赖大量标注的姿态数据，且泛化能力受限于训练时见过的动作模式。

#### 2.2 跨模态对齐基线

EMBridge与以下多模态对齐方法构成直接对比：
- **CPEP**（Cui et al., 2025）：采用对称InfoNCE损失，通过投影层将EMG和姿态嵌入对齐到共享空间。其核心局限在于使用one-hot硬目标，无法建模姿态空间中的细粒度语义关系。
- **CPEP-LS**：CPEP的标签平滑变体，将InfoNCE目标以0.1的平滑因子软化。这是一种朴素的软目标策略，未利用姿态空间的几何结构。
- **Q-Former**：将CPEP的简单投影层替换为Q-Former架构，但仍使用标准InfoNCE损失。该变体验证了仅改进架构而不改进对比目标的效果有限。
- **Q-Former-LS**：Q-Former的标签平滑版本。

#### 2.3 方法谱系中的关键改进槽位

EMBridge相对于上述基线在三个关键设计槽位上做出了差异化改进：

| 设计槽位 | 基线方法 | EMBridge | 改进依据 |
|---------|---------|----------|---------|
| **对齐架构** | 对称InfoNCE（CPEP）或仅投影层 | 非对称Q-Former，冻结姿态编码器，仅在EMG侧优化 | 避免破坏姿态空间的预训练结构，降低优化难度 |
| **对比学习目标** | 标准InfoNCE硬目标 | 社区感知软对比学习（CASCLe） | 保留姿态空间的相对几何结构，提供更丰富的监督信号 |
| **辅助学习目标** | 无辅助任务 | 掩码姿态重建损失（MPRL） | 强制Q-Former的可学习查询捕获姿态内容信息，而非仅对齐全局表示 |

消融实验（Table 3）验证了每个改进槽位的独立贡献：移除Q-Former（降级为CPEP+CASCLe）使零样本未见手势准确率降至0.494；移除MPRL降至0.516；移除CASCLe（仅保留InfoNCE）降至0.509。完整框架达到0.528。

#### 2.4 软对比学习的谱系定位

CASCLe的软目标策略与现有软对比学习方法有本质区别：
- **标签平滑（Label Smoothing）**：对所有负样本赋予均匀的小概率，不区分语义相似度。Table 3显示CASCLe（0.528）优于Q-Former-LS（0.511）和CPEP-LS（0.510）。
- **SoftCLIP**：基于表示相似度构建软目标，但直接在连续嵌入空间计算，易受噪声影响。CASCLe通过离线k-means聚类构建离散社区，再基于社区亲和度计算姿态间语义邻近度，有效降低了噪声（Figure 2）。

### 3. 适用边界与已知局限

#### 3.1 模态依赖性
EMBridge当前仅使用姿态作为跨模态指导，未探索RGB、视频等其他高质量模态。框架的跨模态对齐机制理论上可扩展至其他模态组合（如RGB-EMG），但需验证不同模态间的语义对齐可行性。

#### 3.2 数据依赖性
框架依赖成对的EMG-姿态数据进行预训练。大规模未配对姿态数据（仅姿态、无对应EMG）在当前设计中未被利用，这限制了数据效率的进一步提升空间。Figure 3(c)显示，在仅使用40%配对数据时，EMBridge的零样本性能仍超过全量单模态基线的线性探测性能，表明框架具有较好的数据效率，但仍需一定量的配对数据。

#### 3.3 社区建模的刚性
CASCLe的软目标构建基于k-means硬聚类，每个姿态被分配到固定的社区。这种离散化策略虽然降低了噪声，但也限制了社区划分的柔性和表达能力。Figure 4(f)显示随着top-k邻居数增加性能趋于饱和，暗示当前社区结构的信息容量存在上限。替换为高斯混合模型等概率建模方法可能提升软目标的质量。

#### 3.4 零样本检索机制的敏感性
零样本分类采用检索加KNN投票策略，预测为top-k近邻姿态标签的众数。该机制对支持集的类别分布和噪声较为敏感，且k值选择影响性能（Figure 4相关分析）。此外，在线性探测中，EMBridge使用查询平均策略（而非选择与配对姿态相似度最大的查询），导致未见手势的LP性能略低于CPEP（0.505 vs 0.538），论文承认这可能是一个次优选择。

#### 3.5 评估范围
当前评估仅限于两个公开数据集（emg2pose和NinaPro），迁移至更多真实场景、不同穿戴设备或不同电极配置的鲁棒性有待验证。两个数据集的未见手势评估均基于4个手势类别（Table 1），更大规模手势集合上的零样本泛化能力尚不明确。

### 4. 开放问题

1. **未配对数据的利用**：如何利用大量未配对的姿态数据对单模态编码器进行预训练或协同训练，以进一步提升EMG表示质量？当前框架仅使用配对数据，未开发的姿态单模态数据可能提供额外的语义先验。

2. **跨模态扩展**：本框架能否扩展至其他模态组合（如RGB-EMG、视频-EMG），以实现更丰富的跨模态手势理解？不同模态间的对齐难度和语义互补性需要系统研究。

3. **社区建模的改进**：将k-means硬聚类替换为高斯混合模型等概率建模方法，能否构建更精细的软目标并改善对齐效果？在线聚类或端到端可微分聚类也是可能的方向。

4. **查询选择策略的优化**：若在EMBridge的线性探测阶段改用最大相似度查询选择而非查询平均，能否在不引入泄漏风险的情况下提升未见手势的LP性能？这需要在数据泄漏防护和性能之间寻找平衡点。

5. **部署效率**：如何将零样本手势识别能力部署到资源受限的可穿戴设备上，同时保持实时性和低功耗？Q-Former的额外计算开销和检索式分类的存储需求是实际部署需要解决的问题。

6. **手势空间的可扩展性**：当前评估仅覆盖4个未见手势，当手势类别数量大幅增加时，零样本检索的判别力是否会显著下降？社区结构能否有效扩展到更大规模的手势空间？

## 原文 PDF

![[paperPDFs/ICLR_2026/Zero_shot_Gesture_Movement_Recognition.pdf]]