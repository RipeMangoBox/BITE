---
title: "From Vicious to Virtuous Cycles: Synergistic Representation Learning for Unsupervised Video Object-Centric Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/From_Vicious_to_Virtuous_Cycles_Synergistic_Representation_Learning_for_Unsupervised_Video_Object_Centric_Learning.pdf
openreview_forum_id: bWoT6Z21rH
aliases:
- SRLS
- FVVCSRLUVOCL
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/classification_and_understanding
core_operator: "建立编码器与解码器之间的相互精炼循环：利用编码器的锐度去模糊解码器输出，同时利用解码器的空间一致性去噪编码器特征，并通过预热阶段的slot正则化防止初始slot崩溃，从而打破恶性循环。"
primary_logic: "将编码器尖锐但噪声大的注意力图与解码器连贯但模糊的重建图之间的冲突转化为协同关系，通过精心设计的三元对比目标实现编码器与解码器的相互完善。"
claims:
- "SRL利用编码器的锐度去模糊解码器输出，同时利用解码器的空间一致性去噪编码器特征。"
- "SRL引入的三元对比去模糊和去噪目标打破了恶性循环，建立了良性循环。"
- "MOVi-C (MSE) 上 FG-ARI↑ = 74.3"
- "MOVi-E (MSE) 上 FG-ARI↑ = 81.9"
---

# From Vicious to Virtuous Cycles: Synergistic Representation Learning for Unsupervised Video Object-Centric Learning

> [!tip] 核心洞察
> 将编码器尖锐但噪声大的注意力图与解码器连贯但模糊的重建图之间的冲突转化为协同关系，通过精心设计的三元对比目标实现编码器与解码器的相互完善。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 从恶性到良性循环：无监督视频对象中心学习的协同表征学习 |
| 英文题名 | From Vicious to Virtuous Cycles: Synergistic Representation Learning for Unsupervised Video Object-Centric Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=bWoT6Z21rH); [GitHub](https://github.com/hynnsk/SRL) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/classification_and_understanding |
| Method | Synergistic Representation Learning (SRL) |
| Dataset | MOVi-C (MSE), MOVi-E (MSE), YouTube-VIS 2021 (MSE), MOVi-C (MAE loss) |

> [!tip] 效果简介
> - MOVi-C (MSE) 上，FG-ARI↑ 为 74.3，对比 SlotContrast (no explicit value extracted)，变化 See Table 1。
> - MOVi-E (MSE) 上，FG-ARI↑ 为 81.9，对比 SlotContrast (no explicit value extracted)，变化 See Table 1。
> - YouTube-VIS 2021 (MSE) 上，FG-ARI↑ 为 42.9，对比 SlotContrast (no explicit value extracted)，变化 See Table 1。

## 概述

无监督视频对象中心学习面临一个根本性的困境：编码器产生的注意力图虽然尖锐但包含大量噪声，而解码器生成的重建图虽然空间连贯却边界模糊。这两者之间的冲突形成了一个**恶性循环**——编码器的噪声特征迫使解码器通过空间平均化产生更模糊的输出，而模糊的解码器重建图又缺乏高频细节，无法为编码器提供精确的监督信号，进而导致编码器特征中的噪声持续累积。

本文提出**协同表征学习（Synergistic Representation Learning, SRL）**，将这一冲突转化为协作关系。核心思路是建立编码器与解码器之间的**相互精炼循环**：利用编码器的尖锐注意力图去模糊解码器输出，同时利用解码器的空间一致性掩码去噪编码器特征。具体而言，SRL 引入三元排序对比损失，将每个 patch 划分为正样本、半正样本和负样本三个层次，分别对解码器和编码器施加去模糊和去噪约束。此外，在训练预热阶段通过 slot 正则化防止初始 slot 坍缩，为后续协同优化奠定基础。

实验结果表明，SRL 在多个基准数据集上显著优于现有方法。在 MOVi-C 上，SRL 的 FG-ARI 达到 74.3，相比复现的 SlotContrast 提升 5.5 个百分点，mBO 提升 8.8 个百分点；在真实场景数据集 YouTube-VIS 2021 上，FG-ARI 提升 18.5 个百分点。消融研究进一步验证了去模糊对比损失、去噪对比损失和 slot 正则化预热各自的关键贡献，以及分层对比目标设计的必要性。

## 背景与动机

### 核心问题：编码器-解码器冲突引发的恶性循环

在无监督视频对象中心学习中，基于 slot attention 的模型通常遵循编码器-解码器架构：编码器从视频帧中提取特征并通过迭代注意力竞争将 patch 分配到固定数量的 slot 中，解码器则从 slot 表征重建输入。然而，这一流程存在一个根本性的内部冲突。

编码器产生的注意力图（attention maps）具有**尖锐但噪声多**的特性——它能够捕捉到对象边界的细节，但同时包含大量高频噪声。相反，解码器生成的重建掩码（decoder masks）则呈现出**空间连贯但模糊**的特点——掩码在对象内部保持一致性，但在边界处缺乏锐度。这种差异并非偶然，而是形成了一个自我强化的**恶性循环**（vicious cycle），如 Figure 1(a) 所示：

1. **编码器→解码器方向**：编码器输出的噪声特征使得解码器的重建任务成为不适定问题（ill-posed），迫使解码器通过空间平均化来产生更平滑但更模糊的输出，以抵消输入噪声的影响。
2. **解码器→编码器方向**：模糊的解码器重建图产生的梯度信号缺乏高频细节，无法为编码器提供精确的监督信息来精炼其尖锐但噪声多的特征。

这一恶性循环的后果是：编码器的噪声无法被抑制，解码器的模糊无法被纠正，两者相互拖累，最终导致对象分割质量受限。

### 现有方法的缺口

现有视频 slot-based 方法主要沿着两个方向改进，但均未直接解决上述恶性循环：

- **仅依赖重建损失的方法**（如 SAVi、STEVE）：使用 MSE 重建损失训练解码器，本质上会鼓励解码器产生模糊的平均化输出，这正是恶性循环的催化剂。
- **引入时序对比学习的方法**（如 SlotContrast）：在 slot 层面引入跨帧对比学习以增强时序一致性，但**对比学习仅作用于 slot 表征层面**，并未触及编码器特征与解码器掩码之间的冲突。编码器的噪声特征和解码器的模糊掩码仍然各自为政，恶性循环持续存在。

简言之，现有方法要么加剧了模糊问题，要么绕开了核心冲突而未加以利用。

### 本文动机：将冲突转化为协同

SRL（Synergistic Representation Learning）的核心洞察在于：**编码器的尖锐性与解码器的空间连贯性并非只能相互对抗，它们可以成为相互完善的资源**。具体而言：

- 编码器的尖锐注意力图可以作为**伪标签**，指导解码器学习清晰的语义边界（去模糊）。
- 解码器的空间连贯掩码可以作为**伪标签**，帮助编码器抑制噪声、增强特征一致性（去噪）。

基于这一洞察，SRL 通过精心设计的三元对比目标，将原本的恶性循环转化为**良性循环**（virtuous cycle，Figure 1(b)）：编码器为解码器提供锐度监督，解码器为编码器提供空间一致性监督，两者交替精炼、协同提升。此外，为防止训练初期 slot 坍缩（即多个 slot 收敛到相同表征），SRL 引入 slot 正则化预热阶段，为后续的协同优化奠定坚实基础。

## 核心创新

SRL 的核心创新在于识别并打破了视频对象中心学习中编码器与解码器之间的**恶性循环**，并构建了一个**协同表征学习的良性循环**。其关键洞察是：编码器产生尖锐但噪声多的注意力图，而解码器产生平滑但模糊的重建图——这两者之间存在根本性冲突。SRL 将这种冲突转化为协同关系，通过三个相互关联的机制实现编码器与解码器的相互精炼。

### 1. 去模糊对比损失（De-blurring Contrastive Loss）

**Baseline 缺陷**：传统方法仅使用 MSE 重建损失训练解码器。MSE 损失倾向于对高频细节进行平均化，导致解码器输出语义边界模糊，无法为编码器提供精确的监督信号。

**SRL 创新**：引入三元排序对比损失（Eq. 4），利用编码器的尖锐注意力图作为伪标签来引导解码器产生清晰边界。具体而言，将每个 patch 的锚点特征与所有其他 patch 划分为三类：
- **正集合** $\mathcal{P}_{t,i}^{\mathrm{dec}}$：锚点自身
- **半正集合** $\mathcal{Q}_{t,i}^{\mathrm{dec}}$：编码器注意力标签相同的其他 patch
- **负集合** $\mathcal{N}_{t,i}^{\mathrm{dec}}$：其余所有 patch

两级排序对比损失强制解码器特征与自身锚点最近、与同组 patch 较近、与不同组 patch 远离，从而利用编码器的锐度去模糊解码器输出。消融实验（Table 3）证实，单独加入 $\mathcal{L}^{\mathrm{CL-dec}}$ 可使 mBO 从 31.4 提升至 33.2。

### 2. 去噪对比损失（De-noising Contrastive Loss）

**Baseline 缺陷**：编码器仅依赖主干网络特征，缺乏空间一致性约束，导致注意力图含有大量噪声，这些噪声特征进一步恶化解码器的重建质量。

**SRL 创新**：引入对称的三元排序对比损失（Eq. 6），利用解码器掩码的空间连贯性去净化编码器特征。半正集合 $\mathcal{Q}_{t,i}^{\mathrm{enc}}$ 由解码器掩码伪标签相同的 patch 构成（Eq. 5），这些 patch 在空间上更可能属于同一对象。对比损失强制编码器特征向空间一致的半正样本靠拢，远离负样本。消融实验（Table 3）表明，单独加入 $\mathcal{L}^{\mathrm{CL-enc}}$ 可使 FG-ARI 从 70.8 提升至 73.0。

### 3. Slot 正则化预热（Slot Regularization Warm-up）

**Baseline 缺陷**：Slot 初始化随机，训练初期易发生 slot 坍缩——多个 slot 收敛到相似表示，丧失对象分离能力。

**SRL 创新**：在训练初期（$\eta < 0.1$）引入 KL 散度正则化（Eq. 9），通过检测冗余 slot 对并重置专业化程度较低的 slot 的注意力，强制 slot 差异化。该阶段之后关闭正则化，进入稳定期（$0.1 \le \eta < 0.2$），再启动对比学习阶段（$\eta \ge 0.2$）。三阶段训练调度（Eq. 10）确保 slot 在良性循环启动前已建立良好的语义空间。消融实验（Table 3）证实，正则化与对比损失结合可使 FG-ARI 达到 74.3、mBO 达到 34.5，且性能对阶段切换时刻不敏感（Figure B3）。

### 4. 分层对比目标设计

与标准对比学习仅使用正/负二分类不同，SRL 的**半正集合**是关键设计选择。消融实验（Table 4）显示，移除半正集合导致 FG-ARI 骤降 7.1 点，证明分层结构对于处理编码器-解码器特征空间中的模糊性至关重要。半正集合为模型提供了“软”正样本，在保持语义一致性的同时容忍一定程度的特征差异，从而在锐度与平滑之间建立桥梁。

## 整体框架

![[assets/figures/papers/iclr26_0010_bWoT6Z21rH_From_Vicious_to_Virtuous_Cycles_Synergistic_Repr/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Synergistic Representation learning. The typical pipeline (top) suffers from a conflict between the encoder’s sharp but noisy features (v¯) and the decoder’s spatially coherent but blurry features (z¯). Our framework breaks this cycle by forcing the two modules to synergistically refine one another: (1) Deblurring path: Encoder’s sharp attention map is used to refine the blurry decoded features and (2) Denoising path: Decoder’s coherent masks provide a robust signal to denoise the encoder’s noisy features. Finally, slot regularization during warm-up establishes a solid foundation for this process by ensuring diverse slot specialization*

![[assets/figures/papers/iclr26_0010_bWoT6Z21rH_From_Vicious_to_Virtuous_Cycles_Synergistic_Repr/figures/001_Figure_1.jpg]]
*Figure 1: (a) Vicious cycle in video object-centric learning. Noisy inputs from the encoder render the decoder’s reconstruction task ill-posed, reinforcing its tendency to produce blurry, low-frequency outputs. In turn, the corrupted gradient from these blurry outputs lacks the high-frequency detail required to refine the encoder’s sharp but noisy features. (b) Virtuous cycle of synergistic representation learning. Our framework transforms this conflict into collaboration. We leverage the encoder’s sharp attention maps to deblur the decoder output while denoising the encoder features with the decoder’s spatially coherent masks*

SRL 的整体框架围绕一个核心矛盾展开：编码器产生的 slot attention 图具有尖锐的语义边界，但充满噪声；解码器通过重建产生的掩码空间连贯，但语义边界模糊。传统 pipeline 中，这两者形成恶性循环——编码器的噪声特征使解码器的重建任务不适定，迫使其产生更模糊的低频输出；而模糊的解码器梯度又缺乏高频细节，无法为编码器提供精确的监督信号（Figure 1a）。

SRL 将这一冲突转化为协同关系，建立了编码器与解码器之间的**相互精炼循环**（Figure 1b, Figure 2）。整个 pipeline 由以下模块串联构成，并通过三阶段训练调度实现从初始化到协同优化的平滑过渡。

### 模块关系与数据流

**输入与特征提取。** 给定视频帧序列，首先通过冻结的预训练骨干网络（默认 DINO-v2）提取 patch 级特征。这些特征具有较高的语义锐度，但包含显著的空间噪声，成为后续 slot attention 的输入。

**Slot Attention 编码。** 特征进入 Slot Attention 模块，通过迭代竞争注意力机制将 patch 分组到固定数量 $S$ 的 slot 中。该模块输出两个关键表征：(1) **slot attention 图** $\mathbf{Attn} \in \mathbb{R}^{S \times T \times N}$，为每个 patch 分配对各 slot 的软归属权重，边界尖锐但含噪声；(2) **编码器特征** $\bar{\mathbf{v}}$，即 slot 对 patch 特征的加权聚合，继承了注意力的锐度与噪声特性。

**MLP 解码器重建。** 编码器特征通过 MLP 解码器进行空间广播，重建输入帧。解码器输出 $\mathbf{Mask} \in \mathbb{R}^{S \times T \times N}$ 为每个 patch 提供 slot 归属的软掩码，以及解码器特征 $\bar{\mathbf{z}}$。由于 MSE 重建损失的平均化效应，解码器掩码空间连贯但对象边界模糊。

**去模糊对比学习模块。** 该模块利用编码器注意力图的锐度来锐化解码器输出。具体而言，以编码器注意力图的硬伪标签 $l^{\mathbf{Attn}}$ 为引导，将所有 patch 划分为三元集合：正样本 $\mathcal{P}^{\mathrm{dec}}$（锚点自身）、半正样本 $\mathcal{Q}^{\mathrm{dec}}$（与锚点共享同一注意力标签的 patch）、负样本 $\mathcal{N}^{\mathrm{dec}}$（其余 patch）。通过两级排序对比损失 $\mathcal{L}^{\mathrm{CL-dec}}$（Eq. 4），强制解码器特征在表征空间中与自身最近、与同组 patch 较近、与异组 patch 远离，从而锐化语义边界。

**去噪对比学习模块。** 对称地，该模块利用解码器掩码的空间连贯性来净化编码器特征。以解码器掩码的硬伪标签 $l^{\mathbf{Mask}}$ 定义半正样本集 $\mathcal{Q}^{\mathrm{enc}}$（Eq. 5），构造编码器侧的三元对比损失 $\mathcal{L}^{\mathrm{CL-enc}}$（Eq. 6）。这迫使编码器将空间上属于同一解码器掩码的 patch 拉近，抑制噪声引起的碎片化。

**Slot 正则化预热模块。** 在训练初期，slot 初始化随机且易坍缩为冗余表示。该模块通过检测最相似的 slot 对（基于 slot 向量内积），识别专业化程度较低的冗余 slot，并对其施加 KL 散度正则化，强制其注意力分布趋向均匀（Eq. 9），从而在预热阶段建立差异化的 slot 语义空间。

### 三阶段训练调度

SRL 采用基于训练进度比例 $\eta$ 的分阶段损失调度（Eq. 10）：

- **阶段一（$\eta < 0.1$）：Slot 正则化。** 仅启用 $\mathcal{L}^{\mathrm{reg}}$，强制 slot 差异化，防止初始坍缩。
- **阶段二（$0.1 \leq \eta < 0.2$）：稳定期。** 关闭正则化，仅使用基础重建损失 $\mathcal{L}^{\mathrm{base}}$，让 slot 在无外部干预下巩固。
- **阶段三（$\eta \geq 0.2$）：协同对比学习。** 同时启用来模糊损失 $\mathcal{L}^{\mathrm{CL-dec}}$ 和去噪损失 $\mathcal{L}^{\mathrm{CL-enc}}$，建立编码器-解码器的良性循环。

总损失为 $\mathcal{L} = \mathcal{L}^{\mathrm{base}} + \mathcal{L}^{\mathrm{stage}}$，其中 $\mathcal{L}^{\mathrm{base}}$ 为 MSE（或 MAE）重建损失。消融实验表明，SRL 对该调度的时间边界不敏感，性能平滑且稳定（Figure B3）。

## 核心模块与公式推导

### 3.1 基础流水线

SRL 建立在标准的 slot-based 视频对象中心学习流水线之上。给定一段包含 $T$ 帧的视频，首先通过冻结的 DINO-v2 预训练骨干网络提取每帧的 patch 特征。这些特征随后被送入 Slot Attention 模块，通过迭代的竞争注意力机制将 $N$ 个 patch 分组到固定数量 $S$ 个 slot 中。每个 slot 通过 MLP 解码器重建输入，产生两个关键输出：slot 注意力图 $\mathbf{Attn} \in \mathbb{R}^{S \times T \times N}$ 和解码掩码 $\mathbf{Mask} \in \mathbb{R}^{S \times T \times N}$。

这两个输出之间存在根本性冲突：编码器产生的注意力图尖锐但噪声多，解码器产生的掩码空间连贯但边界模糊。这一冲突构成了恶性循环的核心——噪声编码器特征迫使解码器通过平均化产生模糊输出，而模糊的解码器重建图缺乏高频细节，无法为编码器提供精确的监督信号（见 Figure 1a）。

### 3.2 伪语义标签生成

为建立编码器与解码器之间的协同精炼，SRL 首先从两个模块的原始输出中提取硬伪标签：

$$l_{t,i}^{\mathbf{Attn}} = \arg\max_{s \in \{1,\dots,S\}} \mathbf{Attn}_{s,t,i}, \quad l_{t,i}^{\mathbf{Mask}} = \arg\max_{s \in \{1,\dots,S\}} \mathbf{Mask}_{s,t,i}$$

其中 $l_{t,i}^{\mathbf{Attn}}$ 和 $l_{t,i}^{\mathbf{Mask}}$ 分别为第 $t$ 帧第 $i$ 个 patch 从 slot 注意力图和解码掩码中分配的 slot 索引。这两组伪标签是后续去模糊和去噪对比学习的核心监督信号来源。

### 3.3 去模糊对比学习模块

#### 三元划分策略

去模糊模块的目标是利用编码器注意力图的锐度来锐化解码器输出。为此，SRL 将全体 patch 集合 $\mathcal{U}$ 划分为三个层次：

$$\mathcal{U} = \mathcal{P}_{t,i}^{\mathrm{dec}} \cup \mathcal{Q}_{t,i}^{\mathrm{dec}} \cup \mathcal{N}_{t,i}^{\mathrm{dec}}$$

- **正样本集 $\mathcal{P}_{t,i}^{\mathrm{dec}}$**：仅包含锚点 patch $(t,i)$ 自身。
- **半正样本集 $\mathcal{Q}_{t,i}^{\mathrm{dec}}$**：包含与锚点共享相同编码器注意力标签的所有 patch，即 $\mathcal{Q}_{t,i}^{\mathrm{dec}} = \{ (t',j) \mid l_{t',j}^{\mathbf{Attn}} = l_{t,i}^{\mathbf{Attn}} \}$。这些 patch 在编码器视角下属于同一对象，为解码器提供"应该被分到同一组"的结构化约束。
- **负样本集 $\mathcal{N}_{t,i}^{\mathrm{dec}}$**：其余所有 patch，即 $\mathcal{N}_{t,i}^{\mathrm{dec}} = \mathcal{U} \setminus (\mathcal{P}_{t,i}^{\mathrm{dec}} \cup \mathcal{Q}_{t,i}^{\mathrm{dec}})$。

这一划分的关键在于：编码器的尖锐边界信息通过半正样本集传递给解码器，迫使解码器在特征空间中区分"同组但可能被模糊边界混淆"的 patch 与"真正属于其他对象"的 patch。

#### 两级排序对比损失

基于上述划分，SRL 设计了两级排序对比损失，强制解码器特征 $z_{t,i}$ 满足层次化的距离关系：

$$\mathcal{L}_{t,i}^{\mathrm{CL-dec}} = -\log \frac{\exp(z_{t,i} \cdot y_{t,i} / \tau)}{\sum_{n \in \mathcal{Q}_{t,i}^{\mathrm{dec}} \cup \mathcal{N}_{t,i}^{\mathrm{dec}}} \exp(z_{t,i} \cdot y_n / \tau)} - \frac{1}{|\mathcal{Q}_{t,i}^{\mathrm{dec}}|} \sum_{q \in \mathcal{Q}_{t,i}^{\mathrm{dec}}} \log \frac{\exp(z_{t,i} \cdot y_q / \tau)}{\sum_{n \in \mathcal{N}_{t,i}^{\mathrm{dec}}} \exp(z_{t,i} \cdot y_n / \tau)}$$

其中 $y$ 表示解码器重建特征，$\tau$ 为温度系数。

- **第一项**：标准对比损失，将锚点 $z_{t,i}$ 拉向自身重建 $y_{t,i}$，同时推离所有半正样本和负样本。这确保解码器对每个 patch 的重建保持判别性。
- **第二项**：半正样本排序损失，强制锚点与半正样本 $y_q$ 的相似度高于与负样本的相似度。这一项是去模糊的核心机制——它利用编码器提供的"同组"信息，惩罚解码器在对象边界处产生的模糊特征。

### 3.4 去噪对比学习模块

#### 半正样本集定义

去噪模块的目标是利用解码器掩码的空间连贯性来净化编码器特征。与去模糊模块对称，SRL 使用解码器掩码的伪标签定义半正样本集：

$$\mathcal{Q}_{t,i}^{\mathrm{enc}} = \{ (t', j) \mid l_{t',j}^{\mathbf{Mask}} = l_{t,i}^{\mathbf{Mask}} \}$$

这些 patch 在解码器视角下共享相同的 slot 标签，意味着它们在空间上连贯且语义一致。编码器特征中偏离这一连贯性的噪声将被对比损失抑制。

#### 编码器对比损失

去噪对比损失采用与去模糊损失相同的两级排序结构，但作用于编码器特征 $\pmb{v}$：

$$\mathcal{L}_{t,i}^{\mathrm{CL-enc}} = -\frac{1}{|\mathcal{P}_{t,i}^{\mathrm{enc}}|} \sum_{p \in \mathcal{P}_{t,i}^{\mathrm{enc}}} \log \frac{\exp(\pmb{v}_{t,i} \cdot \pmb{v}_p / \tau)}{\sum_{n \in \mathcal{Q}_{t,i}^{\mathrm{enc}} \cup \mathcal{N}_{t,i}^{\mathrm{enc}}} \exp(\pmb{v}_{t,i} \cdot \pmb{v}_n / \tau)} - \frac{1}{|\mathcal{Q}_{t,i}^{\mathrm{enc}}|} \sum_{q \in \mathcal{Q}_{t,i}^{\mathrm{enc}}} \log \frac{\exp(\pmb{v}_{t,i} \cdot \pmb{v}_q / \tau)}{\sum_{n \in \mathcal{N}_{t,i}^{\mathrm{enc}}} \exp(\pmb{v}_{t,i} \cdot \pmb{v}_n / \tau)}$$

这里正样本集 $\mathcal{P}_{t,i}^{\mathrm{enc}}$ 为锚点自身的不同增强视图，负样本集 $\mathcal{N}_{t,i}^{\mathrm{enc}}$ 为既不与锚点共享注意力标签也不共享掩码标签的 patch。第二项利用解码器的空间连贯性信号，将编码器特征拉向同组 patch，从而抑制噪声。

### 3.5 Slot 正则化预热模块

在训练初期，slot 初始化随机，极易发生坍缩——多个 slot 收敛到相同的表示，导致对象分割失败。SRL 通过 KL 散度正则化强制 slot 差异化，并在后续阶段关闭该约束。

#### 冗余 Slot 检测

首先，在序列的最后一个时间步 $T$ 寻找最相似的 slot 对：

$$(\hat{i}, \hat{j}) = \underset{1 \leq i < j \leq S}{\mathrm{argmax}} (\pmb{s}_{T,i} \cdot \pmb{s}_{T,j})$$

其中 $\pmb{s}_{T,i}$ 为第 $i$ 个 slot 在时间步 $T$ 的表示向量。

#### 专业化分数与正则化

对检测到的相似 slot 对，选择注意力分布更接近均匀分布（即专业化程度较低）的 slot 进行正则化：

$$m^{\mathrm{low}} = \underset{m \in \{\hat{i}, \hat{j}\}}{\arg\min} \frac{1}{T} \sum_{t=1}^{T} D^{\mathrm{KL}}(\mathbf{Attn}_{m,t} \| \mathbf{U})$$

其中 $\mathbf{U}$ 为均匀分布，$D^{\mathrm{KL}}$ 为 KL 散度。该 slot 的注意力被重置，强制其探索不同的对象区域。

### 3.6 三阶段训练调度

SRL 的总损失由基础重建损失和阶段性损失组成：

$$\mathcal{L} = \mathcal{L}^{\mathrm{base}} + \mathcal{L}^{\mathrm{stage}}$$

其中 $\mathcal{L}^{\mathrm{base}}$ 为标准的 MSE 重建损失（亦可替换为 MAE 损失，见 Table B1）。阶段性损失根据训练进度比例 $\eta$ 动态切换：

$$\mathcal{L}^{\mathrm{stage}} = \begin{cases} \lambda^{\mathrm{reg}} \mathcal{L}^{\mathrm{reg}}, & \text{if } \eta < 0.1, \\ 0, & \text{if } 0.1 \le \eta < 0.2, \\ \lambda^{\mathrm{CL}} \mathcal{L}^{\mathrm{CL}}, & \text{if } \eta \ge 0.2, \end{cases}$$

其中 $\mathcal{L}^{\mathrm{CL}} = \mathcal{L}^{\mathrm{CL-enc}} + \mathcal{L}^{\mathrm{CL-dec}}$ 为去噪和去模糊对比损失之和。

- **阶段一（$\eta < 0.1$）**：仅启用 slot 正则化 $\mathcal{L}^{\mathrm{reg}}$，确保 slot 在训练初期建立差异化的语义空间，防止坍缩。
- **阶段二（$0.1 \le \eta < 0.2$）**：关闭正则化，仅使用重建损失进行稳定过渡，让 slot 在无外部干预的情况下巩固已学到的表示。
- **阶段三（$\eta \ge 0.2$）**：启用对比学习，建立编码器与解码器之间的协同精炼循环。

消融实验表明，SRL 对该调度边界不敏感——改变正则化停止时刻或对比学习启动时刻均能稳定超越基线（Figure B3）。

## 实验与分析

### 恶性循环的实证验证

SRL 的核心动机源于对现有视频对象中心学习框架中“恶性循环”的识别。如 Figure B4 定性分析所示，在仅使用 MSE 重建损失的基线模型中，编码器产生的注意力图（Attn）虽然尖锐但充满噪声，迫使解码器在重建时进行空间平均，产生模糊的输出掩码（Mask）。这种模糊的重建图又因缺乏高频细节，无法为编码器提供精确的监督信号，导致编码器特征中的噪声持续存在甚至放大。这一循环在训练过程中不断强化，最终使得模型无法学习到清晰的语义边界。

### 主实验结果

SRL 在多个合成与真实视频数据集上均显著优于现有方法。Table 1 报告了在 MOVi-C、MOVi-E 和 YouTube-VIS 2021 三个基准上的定量结果：

![[assets/figures/papers/iclr26_0010_bWoT6Z21rH_From_Vicious_to_Virtuous_Cycles_Synergistic_Repr/figures/003_Table_1.jpg]]
*Table 1: Experimental results. Results are averaged across 3 runs. † is our reproduced version*

- **MOVi-C**：SRL 达到 74.3 FG-ARI 和 34.5 mBO，相比复现的 SlotContrast 分别提升 5.5% 和 8.8%。
- **MOVi-E**：SRL 达到 81.9 FG-ARI 和 29.3 mBO，在更复杂的多对象场景中保持稳定优势。
- **YouTube-VIS 2021**：SRL 达到 42.9 FG-ARI 和 35.6 mBO，相比 SlotContrast 提升 18.5% FG-ARI 和 8.2% mBO，表明在真实世界视频中协同优化同样有效。

在对象动力学预测的下游任务中（Table 2），将冻结的 SRL 预训练模型集成到 SlotFormer 框架后，在 MOVi-C 上达到 68.9 FG-ARI 和 27.4 mBO，持续优于基于重建和 SlotContrast 的预训练方案。

### 损失函数鲁棒性

SRL 的协同优化机制不依赖于特定的重建损失。Table B1 显示，当使用 MAE 损失替代 MSE 时，SRL 仍取得 74.57 FG-ARI 和 34.28 mBO，相比 SlotContrast 的 73.24 FG-ARI 和 27.54 mBO，mBO 提升尤为显著（+6.74）。Figure B1 的定性对比进一步证实，SRL 在 MAE 损失下产生的掩码具有更清晰的语义边界。

### 跨数据集迁移

SRL 学习的对象表征展现出良好的迁移能力：
- **DAVIS 2017**（Table B2）：SRL 达到 48.2 J 和 36.8 F&J，相比 SlotContrast 分别提升 11.7 和 7.5 点。
- **YTVIS-2019 跨数据集**（Table B3，在 YTVIS-2021 上训练）：SRL 达到 20.4 FG-ARI 和 53.3 mBO，相比 SlotContrast 提升 3.8 FG-ARI 和 10.0 mBO。

### 静态图像泛化

SRL 同样适用于静态图像。如 Table B8 所示，在 COCO 数据集上，SRL 相比基线在 ARI 上提升 2.3 点，在 mBO 上提升 0.6 点。这表明编码器锐度与解码器平滑性之间的冲突是 slot attention 架构的固有属性，而非视频时序的附带现象。

### 组件消融

Table 3 的组件消融研究揭示了各模块的独立贡献与协同效应：

![[assets/figures/papers/iclr26_0010_bWoT6Z21rH_From_Vicious_to_Virtuous_Cycles_Synergistic_Repr/figures/005_Table_3.jpg]]
*Table 3: Component ablation study*

- **去模糊对比损失（ℒ^CL-dec）**：单独使用时将 mBO 从 31.4 提升至 33.2，验证了其锐化解码器边界的有效性。
- **去噪对比损失（ℒ^CL-enc）**：单独使用时将 FG-ARI 从 70.8 提升至 73.0，表明解码器的空间连贯性信号能有效净化编码器特征。
- **Slot 正则化预热（ℒ^reg）**：与对比损失结合后，FG-ARI 达到 74.3，mBO 达到 34.5，证明良好的 slot 初始化是后续协同优化的基础。

### 分层对比目标消融

Table 4 分析了三元对比目标中正集合、半正集合和时域采样的重要性：

![[assets/figures/papers/iclr26_0010_bWoT6Z21rH_From_Vicious_to_Virtuous_Cycles_Synergistic_Repr/figures/006_Table_4.jpg]]
*Table 4: Ablation study of hierarchical contrastive objective. Pos., S.Pos., and Time indicate whether the positive set P, the semi-positive set $\mathcal { Q }$ , and the temporal sampling strategy are used or not*

- 移除半正集合（即仅使用正/负二分类对比）导致 FG-ARI 下降 7.1 点（从 74.3 降至 67.2），mBO 下降 3.1 点。这表明半正集合提供的“同组但非自身”的中间梯度信号对于学习鲁棒表征至关重要。
- 移除时域采样策略同样导致显著性能下降，验证了跨帧对比对于捕捉时序一致性的必要性。

### 训练调度鲁棒性

Figure B3 展示了 SRL 对训练阶段切换时刻的鲁棒性：
- 改变 slot 正则化的停止时刻（Figure B3a），FG-ARI 和 mBO 在所有调度下均大幅超过基线。
- 改变对比学习的启动时刻（Figure B3b），性能同样保持平滑稳定。

这表明三阶段训练策略（Eq. 10）的设计具有良好的容错性，无需针对特定数据集进行精细调整。

### 失败模式与局限性

尽管 SRL 在多数场景下表现优异，但仍存在以下失败模式：

- **严重遮挡场景**：如 Figure A3 所示，当对象之间存在严重遮挡或复杂交互时，分割性能会下降，模型可能将多个对象合并或错误分割。
- **小目标发现**：对小目标的发现和表示能力有限，这源于 slot attention 的竞争机制天然倾向于分配给占据更大空间区域的对象。
- **Slot 数量敏感性**：slot 正则化预热阶段的长度可能需要根据具体数据集进行微调，极端情况下仍可能出现 slot 坍缩或过度碎片化。

### 骨干网络鲁棒性

SRL 在不同预训练骨干上均表现一致。使用 Franca ViT-B/14（Table B5, B6）和 MoSiC ViT-B/14（Table B7）时，SRL 持续优于 SlotContrast，验证了协同优化框架对特征提取器的鲁棒性。

### 补充图表

![[assets/figures/papers/iclr26_0010_bWoT6Z21rH_From_Vicious_to_Virtuous_Cycles_Synergistic_Repr/figures/017_Table_5.jpg]]
*Table 5: Table B1: Experimental results using MAE loss for reconstruction*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

SRL 的核心突破在于识别并打破视频对象中心学习中编码器与解码器之间的**恶性循环**：编码器产生的注意力图尖锐但噪声多，而解码器通过 MSE 重建产生的掩码平滑但模糊——模糊的解码器输出缺乏高频细节，无法为编码器提供精确的监督信号，反过来又迫使解码器进一步平均化，形成自我强化的退化循环（Figure 1, Figure B4）。

SRL 将这一冲突转化为**协同关系**：利用编码器的锐度去模糊解码器输出，同时利用解码器的空间一致性去噪编码器特征，通过精心设计的三元对比目标实现相互完善。

### 与基线方法的关系

**SlotContrast** 是 SRL 最直接的对标基线。SlotContrast 在 slot attention 框架上引入时域对比学习，将同一 slot 在不同帧的 patch 作为正样本，但未解决编码器-解码器冲突。SRL 在此基础上做了三个关键改进：

1. **去模糊对比损失** ($\mathcal{L}^{\mathrm{CL-dec}}$)：SlotContrast 仅使用 MSE 重建损失训练解码器，导致边界模糊。SRL 引入三元排序对比损失（Eq. 4），利用编码器的尖锐注意力图构造正集合 $\mathcal{P}_{t,i}^{\mathrm{dec}}$、半正集合 $\mathcal{Q}_{t,i}^{\mathrm{dec}}$ 和负集合 $\mathcal{N}_{t,i}^{\mathrm{dec}}$，强制解码器特征与自身锚点最近、与同组 patch 较近、与异组 patch 远离，从而锐化语义边界。

2. **去噪对比损失** ($\mathcal{L}^{\mathrm{CL-enc}}$)：SlotContrast 仅依赖主干特征，无额外去噪目标。SRL 利用解码器掩码的伪标签 $l_{t,i}^{\mathbf{Mask}}$ 定义空间一致的半正集合（Eq. 5），通过三元对比损失（Eq. 6）净化编码器特征中的噪声。

3. **Slot 正则化预热** ($\mathcal{L}^{\mathrm{reg}}$)：SlotContrast 无显式正则化，slot 初始化随机且易坍缩。SRL 在训练初期（$\eta < 0.1$）使用 KL 散度正则化（Eq. 9）识别并重置冗余 slot，强制 slot 差异化，并在后续阶段关闭。

**SAVi / STEVE / VideoSAUR** 等早期方法仅依赖重建损失或简单的时序一致性约束，未显式建模编码器-解码器冲突。SRL 的消融实验（Table 3）表明，单独添加去噪损失使 FG-ARI 从 70.8 提升至 73.0，单独添加去模糊损失使 mBO 从 31.4 提升至 33.2，三者组合达到 FG-ARI 74.3、mBO 34.5。

### 适用边界与泛化能力

**数据集覆盖**：SRL 在合成视频（MOVi-C, MOVi-E）、真实视频（YouTube-VIS 2021, DAVIS 2017）和静态图像（COCO）上均验证有效。跨数据集迁移（YTVIS-2019, trained on YTVIS-2021）显示 FG-ARI 从 16.6 提升至 20.4，mBO 从 43.3 提升至 53.3（Table B3），表明学习到的表征具有一定泛化性。

**骨干网络鲁棒性**：SRL 使用 DINO-v2、Franca、MoSiC 等不同预训练骨干均表现稳定，说明方法不依赖特定特征提取器。

**损失函数鲁棒性**：使用 MAE 损失替代 MSE 时，SRL 仍显著优于 SlotContrast（MOVi-C: FG-ARI 74.57 vs 73.24, mBO 34.28 vs 27.54, Table B1）。

**训练调度鲁棒性**：slot 正则化停止时刻和对比学习启动时刻的选择对最终性能影响平滑（Figure B3），表明三阶段训练策略（Eq. 10）不需要精细调参。

**静态图像适用性**：SRL 的编码器-解码器冲突存在于 slot attention 架构本身，独立于时序维度，因此在 COCO 图像数据上同样有效（ARI +2.3, mBO +0.6, Table B8）。

### 已知局限与失败模式

1. **遮挡与复杂交互**：在包含严重遮挡或复杂对象交互的场景中，分割性能仍可能下降（Figure A3 失败案例）。三元对比目标的半正集合依赖于伪标签的准确性，当遮挡导致注意力图或掩码标签错误时，去模糊和去噪信号可能被误导。

2. **小目标发现能力有限**：slot attention 的竞争机制天然倾向于主导对象，对小目标的表示能力不足。SRL 未引入显式的小目标增强策略。

3. **预热阶段敏感性**：slot 正则化预热阶段的长度可能需要根据具体数据集微调，尽管 Figure B3 显示一定鲁棒性，但极端设置下仍可能影响 slot 初始化质量。

4. **架构依赖**：SRL 的协同优化目前仅在 slot-based 架构上验证，尚未在非 slot-based 架构（如 GAN、扩散模型）或更复杂的现实世界视频数据集上验证泛化性。

### 开放问题

1. **跨架构扩展**：SRL 的编码器-解码器协同优化框架能否推广到其他生成式架构（如扩散模型、GAN），利用类似的对比去模糊/去噪机制提升生成质量？

2. **噪声传播的显式建模**：当前方法通过对比损失隐式去噪，是否可以通过显式建模和抑制编码器噪声在解码器中的传播路径来进一步提升去噪效果？

3. **小目标增强**：如何在保持 slot 竞争机制的同时增强对小目标的发现和表示能力？可能的路径包括多尺度 slot 或注意力偏置。

4. **多模态协同预训练**：在无监督预训练中，协同表征学习可否与文本、运动等多模态信息结合，进一步提升对象发现的语义一致性？

5. **长视频与开放世界**：SRL 在 YouTube-VIS 上的性能（FG-ARI 42.9）虽显著优于基线，但绝对值仍不高，表明在开放世界长视频中的对象发现仍面临挑战，需要进一步研究 slot 数量的自适应调整和在线学习策略。

## 原文 PDF

![[paperPDFs/ICLR_2026/From_Vicious_to_Virtuous_Cycles_Synergistic_Representation_Learning_for_Unsupervised_Video_Object_Centric_Learning.pdf]]
