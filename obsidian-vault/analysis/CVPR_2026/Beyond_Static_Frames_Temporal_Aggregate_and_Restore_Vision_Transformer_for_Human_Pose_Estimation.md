---
title: "Beyond Static Frames: Temporal Aggregate-and-Restore Vision Transformer for Human Pose Estimation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Beyond_Static_Frames_Temporal_Aggregate_and_Restore_Vision_Transformer_for_Human_Pose_Estimation.pdf
project_link: null
code_link: "https://github.com/zgspose/TARViTPose"
aliases:
- TV
- BSFTARVTHPE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在ViT编码器后插入即插即用的时间建模模块（JTA和GRA），以关节为中心跨帧聚合特征并恢复增强的时空表示。
primary_logic: 为每个关节点分配可学习查询令牌，并利用根据热图生成的空间掩码进行掩码感知交叉注意力，可以精确对齐和聚合来自相邻帧的关节特定时间线索。随后通过全局恢复注意力将这些线索无缝融入当前帧的特征表示，从而显著提升姿态估计的鲁棒性和准确性。
claims:
- 相较于单帧基线ViTPose，TAR-ViTPose在PoseTrack2017上平均mAP提升 +2.3（ViT-B）
- 掩码感知注意力模块带来额外1.4 mAP的显著提升
- 在PoseTrack2017/2018/2021三个基准上均取得当前最优性能，同时运行帧率显著高于同类方法（如413 fps vs. 52 fps）
- PoseTrack2017 val 上 mAP = 84.0 (ViT-B)
---

# Beyond Static Frames: Temporal Aggregate-and-Restore Vision Transformer for Human Pose Estimation

> [!tip] 核心洞察
> 为每个关节点分配可学习查询令牌，并利用根据热图生成的空间掩码进行掩码感知交叉注意力，可以精确对齐和聚合来自相邻帧的关节特定时间线索。随后通过全局恢复注意力将这些线索无缝融入当前帧的特征表示，从而显著提升姿态估计的鲁棒性和准确性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 超越静态帧：面向人体姿态估计的时间聚合与恢复视觉Transformer |
| 英文题名 | Beyond Static Frames: Temporal Aggregate-and-Restore Vision Transformer for Human Pose Estimation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.05929) · [Code](https://github.com/zgspose/TARViTPose) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TAR-ViTPose |
| Dataset | PoseTrack2017 val, PoseTrack2018 val, PoseTrack21 val, Runtime |

> [!tip] 效果简介
> - PoseTrack2017 val 上，mAP 84.0 (ViT-B) vs 81.7 (ViTPose) (+2.3)；mAP 86.8 (ViT-H) vs 85.6 (DSTA ViT-H) (+1.2)；mAP 81.9 (ViT-S) vs 77.3 (HRNet-W48) (+4.6)。
> - PoseTrack2018 val 上，mAP 84.2 (ViT-H) vs 82.4 (ViTPose ViT-H) (+1.8)。
> - PoseTrack21 val 上，mAP 84.1 (ViT-H) vs 82.0 (ViTPose ViT-H) (+2.1)。

## 概要

**核心问题**：现有基于Vision Transformer（ViT）的姿态估计方法对视频进行逐帧独立处理，完全忽略帧间的时间连贯性，导致在运动模糊、遮挡和散焦等挑战性场景下预测不稳定、抖动明显。

**方法定位**：TAR‑ViTPose 在 ViTPose 单帧基线之上，以即插即用方式插入两个时间建模模块——**关节中心时间聚合（Joint‑centric Temporal Aggregation, JTA）** 与**全局恢复注意力（Global Restoring Attention, GRA）**。JTA 为每个关节点分配可学习查询令牌，利用掩码感知交叉注意力精确对齐并聚合相邻帧中的关节特定时间线索；GRA 再将这些聚合线索注入当前帧的特征表示，恢复增强的时空表征。整个流程继承 ViTPose 的 ViT 编码器与轻量解码器，不改变原有结构，仅增加少量时间建模参数。

**核心结论**：
- 相较单帧基线 ViTPose，TAR‑ViTPose 在 PoseTrack2017 验证集上平均 mAP 提升 **+2.3**（ViT‑B），在 PoseTrack2018 和 PoseTrack21 上分别提升 **+1.8** 和 **+2.1**（ViT‑H），三个基准均取得当前最优性能。
- 掩码感知注意力模块带来额外 **+1.4 mAP** 的显著增益（Table 6）。
- 方法在保持高精度的同时，运行帧率显著高于同类视频姿态估计方法（如 ViT‑S 达到 **413 fps**，对比 DSTA 的 52 fps，约 8 倍加速）。

**证据强度**：上述结论由多组消融实验和跨基准对比支持，置信度较高；但方法未显式强制帧间时间一致性，在严重遮挡场景下可能仍存在轻微的时间不一致，需在实际部署中关注。



### 问题背景：视频人体姿态估计的时序挑战

人体姿态估计的目标是从图像或视频中精确地定位人体关键点的空间坐标。在静态图像领域，基于Vision Transformer（ViT）的方法已取得显著进展，通过强大的全局上下文建模能力实现了高精度关键点定位。然而，当这些方法被直接逐帧应用于视频时，一个根本性的瓶颈暴露出来：**它们将每一帧视为独立的静态图像，完全忽略了帧与帧之间固有的时间连贯性**。

这种“静态帧”处理范式在真实世界的视频场景中暴露出严重的脆弱性。当视频中出现**运动模糊、部分遮挡、散焦或复杂姿态**时，单帧图像所能提供的视觉线索严重不足，导致预测结果出现抖动、漂移甚至完全错误。现有方法缺乏一种机制来利用相邻帧中的互补信息来增强当前帧的表示，从而无法在挑战场景下维持稳定可靠的姿态估计。

### 现有方法的缺口

当前视频姿态估计方法主要分为两类，但各自存在明显局限：

- **单帧方法**（如ViTPose）：以ViT编码器提取每帧的潜在特征，再通过轻量解码器回归关键点热图。这种流水线完全独立地处理每一帧，虽然架构简洁、推理高效，但在时间维度上没有任何信息交换，无法应对单帧信息不足的挑战场景。

- **现有视频方法**（如DSTA、Poseidon）：尝试通过Transformer架构融合多帧特征，引入跨帧注意力机制来捕捉时间依赖。然而，这些方法通常采用**无差别的全局特征融合策略**——将所有帧的所有空间位置进行密集的交叉注意力计算。这种设计存在两个关键缺陷：
  1. **计算冗余**：对大量与人体姿态无关的背景区域也进行了不必要的注意力计算，导致推理速度显著下降（例如DSTA仅52 fps）。
  2. **对齐不精确**：缺乏关节级别的细粒度对齐机制，无法精确地将某一帧中特定关节的特征与另一帧中同一关节的特征进行匹配和聚合。

### 本文动机：即插即用的关节中心时间建模

基于上述分析，本文的核心动机是：**能否在不改变现有ViT姿态估计架构主体的情况下，以即插即用的方式引入高效的时间建模能力？**

具体而言，我们希望设计一种时间建模模块，使其满足以下设计原则：

1. **架构兼容性**：直接插入现有ViTPose编码器与解码器之间，复用预训练权重，无需重新设计整个流水线。
2. **关节中心对齐**：为每个关键点分配专门的时间聚合机制，精确地对齐和聚合来自相邻帧的关节特定特征，而非进行无差别的全局融合。
3. **高效计算**：通过空间掩码引导注意力仅聚焦于关节相关区域，大幅减少冗余计算，维持高推理帧率。
4. **特征还原**：将聚合的时间线索无缝融入当前帧的特征表示，而非直接从中回归关键点，确保增强后的特征仍能充分利用原有的解码器设计。

这一动机直接催生了本文提出的**TAR-ViTPose**（Temporal Aggregate-and-Restore Vision Transformer），其核心创新在于**关节中心时间聚合（JTA）** 与**全局恢复注意力（GRA）** 两个模块的协同设计：JTA通过可学习的关节查询令牌和掩码感知交叉注意力实现帧间关节特征的精确对齐与聚合；GRA则将聚合的时间信息注入当前帧的特征序列，恢复全局上下文，最终通过原有的轻量解码器生成鲁棒且准确的姿态估计结果。



## 核心方法与创新机理

TAR‑ViTPose 的核心创新在于将视频时序建模以**即插即用**的方式注入单帧 ViT 姿态估计框架，形成一个“时间聚合‑恢复”范式，其关键改动槽位（changed slots）如下。

### 1. 时间建模槽位：从逐帧独立到帧间协同

**基线 (ViTPose)**：ViT 编码器独立处理每一帧，解码器仅依赖当前帧的潜在特征回归热图，完全忽略时间维度。

**提出方案 (TAR‑ViTPose)**：在 ViT 编码器与轻量解码器之间插入两个串联的时间模块——**关节中心时间聚合 (Joint‑centric Temporal Aggregation, JTA)** 与 **全局恢复注意力 (Global Restoring Attention, GRA)**，利用相邻帧的时间线索增强当前帧的特征表示（Fig. 1‑2; Sec. 3.1）。该设计保持编码器和解码器的结构与预训练权重不变，实现了零侵入的时序增强。

### 2. 关节特征聚合槽位：从无关节设计到掩码感知关节查询

**基线**：无任何关节特定的特征聚合机制。

**提出方案**：为每个关节点分配一个可学习的查询令牌 $Q$，通过 JTA 中的掩码感知交叉注意力，强制每个查询令牌仅关注其对应关节在相邻帧中的空间区域（Sec. 3.2）。具体而言：
- 利用解码器输出的热图生成二进制空间掩码 $M$（Eq. 3），掩码阈值 $\phi=0.2$ 用于抑制无关背景区域；
- 在每一层交叉注意力中，将掩码 $M$ 加至注意力 logits，使查询令牌的注意力严格聚焦于对应关节位置（Eq. 4）。

这一设计实现了**帧间关节级精确对齐与聚合**，是性能提升的核心驱动力。

### 3. 特征还原槽位：从直接解码到全局上下文恢复

**基线**：ViT 编码器的输出特征直接送入解码器。

**提出方案**：JTA 输出的聚合时间令牌 $\widetilde{Q}$ 并不直接用于回归关键点，而是通过 GRA 中的单层交叉注意力注入当前帧的特征序列 $F_i^{\mathrm{out}}(t)$（Eq. 5），恢复全局空间上下文后再送入解码器。消融实验表明，若省略 GRA 而直接从关节查询令牌回归关键点，性能骤降 **13.7 mAP**（Table 5），证明将时间特征恢复到当前帧空间表示的必要性。

### 4. 训练策略槽位：预训练继承与模块解耦

**基线**：在 COCO 上预训练整个 ViTPose 模型，再微调至目标数据集。

**提出方案**：编码器与解码器继承 ViTPose 在 COCO 上的预训练权重，而 JTA 和 GRA 模块随机初始化，端到端训练 30 轮（Sec. 4.1）。这种解耦策略使得时间模块可以灵活适配不同规模的 ViT 骨干网络（ViT‑S/B/L/H），同时充分利用已有的强单帧先验。

### 创新本质的因果机制

上述四个槽位改动共同构成了一个因果链：**时间聚合（JTA）→ 关节级对齐（掩码感知注意力）→ 上下文恢复（GRA）→ 鲁棒解码**。其中，掩码感知注意力是精度增益的关键杠杆——消融实验表明，引入掩码感知注意力可额外带来 **+1.4 mAP** 的提升（Table 6）；而 GRA 则是防止信息瓶颈的结构性保障，缺失时将导致性能崩溃。该因果链使得 TAR‑ViTPose 在 PoseTrack2017/2018/2021 三个基准上均取得最优性能，同时保持 **413 fps** 的高推理效率（Table 3）。



TAR‑ViTPose 在单帧基线 **ViTPose** 之上构建了一个即插即用的时间建模流水线，其核心思想是：**以当前帧的姿态估计为目标，显式聚合相邻帧的时间线索，并将增强后的时空表示恢复到当前帧的特征序列中**。整个流水线由五个模块串联而成，形成“编码→聚合→恢复→解码→掩码生成”的闭环。

### 输入与输出定义

对于视频中的第 *i* 个个体，给定以其为中心裁剪的时序片段 $\mathbf{S}_i = \langle X_i(t-T), \dots, X_i(t), \dots, X_i(t+T) \rangle$，目标是估计当前帧 $X_i(t)$ 的 $N$ 个关键点热图：

$$
\left\{ H_i^j(t) \right\}_{j=1}^{N} = \mathrm{HPE}(\mathbf{S}_i)
$$

其中 $T$ 为时间跨度，默认 $T=2$（即使用前后各两帧，共四帧辅助帧）。

### 模块关系与数据流

1. **ViT Encoder（特征提取）**  
   每一帧 $X_i(\tau)$ 独立通过冻结或微调的 ViT 编码器，得到潜在特征序列 $F_i^{\mathrm{out}}(\tau)$。该模块完全继承 ViTPose 的架构与预训练权重，不引入任何时序操作。

2. **Joint‑centric Temporal Aggregation（JTA，关节中心时间聚合）**  
   这是整个框架的核心创新之一。JTA 引入 $N$ 个可学习的关节查询令牌 $Q$，每个令牌对应一个关键点。它通过多层掩码感知交叉注意力，在所有帧的特征序列 $\{F_i^{\mathrm{out}}(\tau)\}_{\tau=t-T}^{t+T}$ 上更新这些查询令牌，得到聚合后的时间令牌 $\widetilde{Q}$：

   $$
   \widetilde{Q} = \mathrm{JTA}\left(Q, \{F_i^{\mathrm{out}}(\tau)\}_{\tau=t-T}^{t+T}\right)
   $$

   为了强制关节级对齐，JTA 利用从解码热图生成的二进制空间掩码 $M^j(\tau)$，使每个关节查询只关注其对应关节区域：

   $$
   M_{x,y}^{j}(\tau) = \begin{cases} 0 & \text{if } \overline{H}_{x,y}^{j}(\tau) \geq \phi \\ -\infty & \text{otherwise} \end{cases}
   $$

   第 $l$ 层掩码交叉注意力的更新公式为：

   $$
   Q^{l} = \mathrm{softmax}\left( f_q(Q^{l-1}) f_k(F_i^{\mathrm{out}})^{\top} + M \right) f_v(F_i^{\mathrm{out}}) + Q^{l-1}
   $$

3. **Global Restoring Attention（GRA，全局恢复注意力）**  
   聚合后的时间令牌 $\widetilde{Q}$ 携带着来自相邻帧的关节特定线索，但尚未与当前帧的空间表示融合。GRA 通过单层交叉注意力，将 $\widetilde{Q}$ 注入当前帧的特征序列 $F_i^{\mathrm{out}}(t)$，产生增强的特征 $\widehat{F}_i^{\mathrm{out}}(t)$：

   $$
   \widehat{F}_i^{\mathrm{out}}(t) = \mathrm{CrossAttn}\left( F_i^{\mathrm{out}}(t), \widetilde{Q}, \widetilde{Q} \right)
   $$

   这一步至关重要：消融实验表明，若直接从 $\widetilde{Q}$ 回归关键点而省略 GRA，性能会骤降 **13.7 mAP**（Table 5），证明 GRA 是将时间特征“归还”到当前帧空间表示的必要环节。

4. **Lightweight Decoder（轻量解码器）**  
   增强后的特征 $\widehat{F}_i^{\mathrm{out}}(t)$ 被送入与 ViTPose 完全相同的轻量解码器（两层反卷积 + 1×1 卷积），回归出当前帧的最终关键点热图 $H_i(t)$。该解码器不增加任何参数。

5. **Mask Construction（掩码生成）**  
   解码器输出的热图 $\overline{H}(\tau)$ 同时用于生成下一轮 JTA 所需的二进制掩码（阈值 $\phi=0.2$）。这形成了一个从解码器回到 JTA 的信息闭环，使掩码能够根据当前预测动态调整注意力范围。

### 训练与推理策略

- **权重继承**：ViT 编码器和轻量解码器直接加载 ViTPose 在 COCO 上的预训练权重；JTA 和 GRA 模块随机初始化，端到端训练 30 轮。
- **损失函数**：仅对当前帧 $t$ 计算预测热图与真值热图之间的均方误差：

  $$
  \mathcal{L} = \sum_i \sum_{j=1}^{N} \left\| H_i^j(t) - G_i^j(t) \right\|_2^2
  $$

- **推理效率**：由于 JTA 只在紧凑的关节查询令牌上操作（而非全帧特征序列），且 GRA 仅需单层交叉注意力，整个时间建模模块的计算开销极低。以 ViT‑S 为例，TAR‑ViTPose 在单张 A6000 上达到 **413 fps**，约为同类方法 DSTA 的 8 倍（Table 3）。

### 与基线的架构差异

相较于逐帧独立处理的 ViTPose（Fig. 1a），TAR‑ViTPose 的唯一改动是在 ViT 编码器与轻量解码器之间插入了 JTA + GRA 时间建模模块（Fig. 1b）。这一设计使得任何 ViTPose 变体（ViT‑S/B/L/H）均可无缝升级为视频姿态估计模型，无需修改编码器或解码器的任何参数。

### 补充图表

![[assets/figures/papers/paper_list_l1009_https_arxiv_org_abs_2603_05929/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between the baseline ViTPose pipeline (a) and our TAR-ViTPose (b). (a) ViTPose adopts a ViT encoder to extract latent features from the input image, which are then fed into a lightweight decoder to regress keypoint heatmaps. (b) Our method enhances the current-frame representation by aggregating temporal cues from adjacent frames, achieving plug-and-play temporal modeling within the original ViTPose architecture*

![[assets/figures/papers/paper_list_l1009_https_arxiv_org_abs_2603_05929/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of the proposed Temporal Aggregate-and-Restore Vision Transformer (TAR-ViTPose). The objective is to estimate the human pose of the current frame*



TAR‑ViTPose 的核心思想是在 ViT 编码器之后插入一个即插即用的时间建模模块，利用相邻帧的时间线索增强当前帧的特征表示，而不是改变原有的编码器‑解码器结构。该模块由两个关键子模块组成：**Joint‑centric Temporal Aggregation (JTA)** 和 **Global Restoring Attention (GRA)**。

### 问题形式化

给定一段以人为中心的视频片段 $\mathbf{S}_i$，目标是估计当前帧 $t$ 中该人的 $N$ 个关键点热图：

$$
\left\{ H_i^j(t) \right\}_{j=1}^{N} = \mathrm{HPE}(\mathbf{S}_i)
$$

其中 $H_i^j(t)$ 表示个体 $i$ 在时刻 $t$ 的第 $j$ 个关键点的预测热图。视频片段包含当前帧及其前后各 $T$ 帧，即 $\langle X_i(t-T), \ldots, X_i(t), \ldots, X_i(t+T) \rangle$。

### 编码器特征提取

每一帧首先通过 ViT 编码器独立提取潜在特征表示 $\{F_i^{\mathrm{out}}(\tau)\}_{\tau=t-T}^{t+T}$。编码器与轻量解码器均继承 ViTPose 在 COCO 上的预训练权重，时间模块则随机初始化。

### Joint‑centric Temporal Aggregation (JTA)

JTA 的目标是跨帧精确对齐和聚合关节特定的时间特征。其核心机制是为每个关节点分配一个可学习的查询令牌 $Q \in \mathbb{R}^{N \times d}$，并通过掩码感知交叉注意力，使每个查询令牌仅关注相邻帧中对应关节区域的特征。

JTA 的整体操作定义为：

$$
\widetilde{Q} = \mathrm{JTA}\left(Q, \{F_i^{\mathrm{out}}(\tau)\}_{\tau=t-T}^{t+T}\right)
$$

**掩码构建** 是实现关节级对齐的关键。首先利用轻量解码器从各帧特征生成粗糙的热图 $\overline{H}(\tau)$，然后根据阈值 $\phi$ 生成二进制空间掩码：

$$
M_{x,y}^{j}(\tau) = \begin{cases} 0 & \text{if } \overline{H}_{x,y}^{j}(\tau) \geq \phi \\ -\infty & \text{otherwise} \end{cases}
$$

当热图像素值高于阈值 $\phi$ 时，掩码值为 $0$（允许注意力）；否则为 $-\infty$（完全抑制注意力）。这使得注意力被强制约束在对应关节的空间邻域内。

**掩码感知特征‑关节注意力** 在 JTA 的每一层中执行。第 $l$ 层的查询令牌更新公式为：

$$
Q^{l} = \mathrm{softmax}\left( f_q(Q^{l-1}) f_k(F_i^{\mathrm{out}})^{\top} + M \right) f_v(F_i^{\mathrm{out}}) + Q^{l-1}
$$

其中 $f_q$、$f_k$、$f_v$ 分别为查询、键、值的线性投影，$M$ 为拼接所有帧和所有关节的掩码矩阵。残差连接保留了上一层的查询信息。JTA 堆叠 6 层交叉注意力层，默认掩码阈值 $\phi=0.2$。

### Global Restoring Attention (GRA)

JTA 输出的聚合查询令牌 $\widetilde{Q}$ 浓缩了跨帧的关节特定时间信息，但这些信息需要被重新注入当前帧的空间特征表示中，才能被解码器有效利用。GRA 通过单层交叉注意力完成这一“恢复”操作：

$$
\widehat{F}_i^{\mathrm{out}}(t) = \mathrm{CrossAttn}\left( F_i^{\mathrm{out}}(t), \widetilde{Q}, \widetilde{Q} \right)
$$

其中当前帧特征 $F_i^{\mathrm{out}}(t)$ 作为查询，聚合的时间令牌 $\widetilde{Q}$ 同时作为键和值。消融实验表明，若省略 GRA 而直接从 $\widetilde{Q}$ 回归关键点，性能骤降 13.7 mAP（70.3 vs. 84.0），证明 GRA 将时间特征恢复到当前帧空间表示的必要性。

### 解码与损失函数

增强后的特征 $\widehat{F}_i^{\mathrm{out}}(t)$ 送入与 ViTPose 相同的轻量解码器（两层反卷积 + 1×1 卷积），生成最终的关键点热图。训练损失为预测热图与真值热图之间的像素级均方误差：

$$
\mathcal{L} = \sum_i \sum_{j=1}^{N} \left\| H_i^j(t) - G_i^j(t) \right\|_2^2
$$

其中 $G_i^j(t)$ 为第 $j$ 个关键点的高斯热图真值。

### 补充图表

![[assets/figures/papers/paper_list_l1009_https_arxiv_org_abs_2603_05929/figures/010_Figure_4.jpg]]
*Figure 4: Visualization of attention heatmaps for joint query tokens with (b) and without (a) mask-aware attention. Given a current frame Xi(t) and a neighboring frame Xi(t −T ), we visualize the attention heatmaps of three different joint query tokens with respect to the features of Xi(t − T ). See Supp. Material for more*



## 实验与关键发现

### 主实验结果

TAR‑ViTPose 在三个主流视频姿态估计基准上均取得当前最优性能，同时保持极高的推理效率。在 PoseTrack2017 验证集上，以 ViT‑B 为骨干时，TAR‑ViTPose 达到 84.0 mAP，相较单帧基线 ViTPose 提升 **+2.3 mAP**（Table 1）。当骨干扩展至 ViT‑H 时，性能进一步提升至 86.8 mAP，超越先前最优视频方法 DSTA（85.6 mAP）1.2 个百分点（Table 2）。若使用真实边界框，ViT‑H 版本可达 90.3 mAP，为当前该基准上的最高记录。

![[assets/figures/papers/paper_list_l1009_https_arxiv_org_abs_2603_05929/figures/003_Table_1.jpg]]
*Table 1: Comparison with the ViTPose baseline (mAP) on Pose-Track2017 val. set*

![[assets/figures/papers/paper_list_l1009_https_arxiv_org_abs_2603_05929/figures/005_Table_2.jpg]]
*Table 2: Comparison with the SOTAs on PoseTrack2017 val. set. ‘†’ indicates an end-to-end method without bounding box detection, and ‘#’ indicates that the ViT backbone used is not specified. Similar to FAMI-Pose [25] and DSTA [14], our proposed TAR-ViTPose sets the temporal span T to 2, which includes two preceding and two succeeding frames, totaling four auxiliary frames*

跨基准泛化能力同样显著。在 PoseTrack2018 验证集上，ViT‑H 版本取得 84.2 mAP，较 ViTPose 基线提升 +1.8 mAP（Table 7）；在 PoseTrack21 验证集上达到 84.1 mAP，提升 +2.1 mAP（Table 8）。与同期最优方法相比，TAR‑ViTPose 在 PoseTrack2018 和 PoseTrack21 上均保持领先（Tables 9, 10），证实时间聚合‑恢复范式在不同数据分布下的鲁棒性。

![[assets/figures/papers/paper_list_l1009_https_arxiv_org_abs_2603_05929/figures/011_Table_7.jpg]]
*Table 7: Comparison with the ViTPose baseline (mAP) on Pose-Track2018 val. set*

![[assets/figures/papers/paper_list_l1009_https_arxiv_org_abs_2603_05929/figures/012_Table_8.jpg]]
*Table 8: Comparison with the ViTPose baseline (mAP) on Pose-Track21 val. set*

效率方面，TAR‑ViTPose 在 NVIDIA A6000 上以 ViT‑S 骨干实现 **413 fps**，约为 DSTA（52 fps）的 8 倍，且显著快于其他视频姿态估计方法（Table 3）。该效率优势源于其即插即用设计：时间模块仅作用于 ViT 编码器输出的潜在特征，无需修改编码器或解码器的推理路径。

![[assets/figures/papers/paper_list_l1009_https_arxiv_org_abs_2603_05929/figures/006_Table_3.jpg]]
*Table 3: Runtime frame rate (FPS), measured on an A6000. All methods utilize the same two auxiliary frames as in [24]*

### 消融实验

**时间建模策略的选择。** 为验证关节中心时间聚合（JTA）的必要性，实验对比了三种替代方案：无时间建模（单帧基线）、全局自注意力（对所有帧的特征令牌做自注意力）、以及所提出的 JTA（Table 4）。全局自注意力仅带来 0.5 mAP 的边际提升（82.8 vs. 82.3），而 JTA 达到 84.0 mAP，额外提升 1.2 mAP。这表明无差别的全局时间融合无法有效对齐关节级线索，而 JTA 通过可学习关节查询令牌实现了精确的帧间关节特征聚合。

**JTA 与 GRA 的协同作用。** 剥离实验（Table 5）揭示了两个模块的因果依赖关系。若移除 GRA、直接从关节查询令牌回归关键点热图，性能骤降至 70.3 mAP（‑13.7），证明 GRA 将聚合的时间特征恢复到当前帧空间表示是不可或缺的环节。单独使用 GRA 而无 JTA 则退化为 82.3 mAP，与基线持平，说明时间聚合与空间恢复必须协同工作才能产生增益。

**掩码感知注意力的贡献。** 在 JTA 中引入掩码感知注意力（mask‑aware attention）带来 **+1.4 mAP** 的提升（84.0 vs. 82.6，Table 6）。注意力热图可视化（Figure 4）进一步证实：无掩码时，关节查询令牌的注意力分散在背景和非对应关节区域；引入掩码后，注意力精确聚焦于相邻帧中对应关节的空间位置，实现了可靠的帧间关节对齐。

**辅助帧数量。** 随着辅助帧从 1 帧增加到 4 帧（T=2），ViT‑B 的 mAP 从 83.2 单调提升至 84.0（Table 14），验证了更长时间上下文对姿态估计的持续收益。

**模块深度配置。** JTA 堆叠 6 层交叉注意力、GRA 使用 1 层交叉注意力达到最佳精度‑效率平衡（Tables 12, 13）。进一步增加层数未带来显著性能提升，但增加了计算开销。

**掩码阈值敏感性。** 掩码阈值 ϕ=0.2 提供最佳性能（Table 11）。阈值过高会导致有效关节区域被抑制，过低则引入背景噪声，均会削弱关节对齐的精度。

### 定性分析

Figure 3 展示了 TAR‑ViTPose 与 ViTPose、DCPose、DSTA、Poseidon 在遮挡、运动模糊和散焦等挑战场景下的对比。TAR‑ViTPose 在这些困难情况下产生更稳定、更准确的姿态预测，而单帧方法 ViTPose 及部分视频方法在模糊或遮挡区域出现明显错误预测（红色实线圆圈标注）。更多定性结果见 Figure 5，涵盖 PoseTrack 数据集和野外视频，进一步验证了方法在复杂姿态和极端条件下的鲁棒性。

![[assets/figures/papers/paper_list_l1009_https_arxiv_org_abs_2603_05929/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison of a) our TAR-ViTPose, b) ViT-Pose [41], c) DCPose [24], d) DSTA [14], and e) Poseidon [27], featuring challenges such as occlusion, motion blur, and defocus. The first two columns are from the PoseTrack datasets, while the last two columns are from in-the-wild videos. Inaccurate predictions are marked with red solid circles. Zoom in for clarity*

### 失败模式与局限性

尽管 TAR‑ViTPose 在多数场景下表现鲁棒，但存在以下已知局限：

- **严重遮挡下的时间不一致性。** 方法未显式强制帧间时间一致性约束，在极端遮挡场景下可能产生轻微的时间抖动或预测不稳定。这是当前设计的结构性限制，而非训练不足所致。
- **未解决姿态跟踪问题。** 本工作聚焦于单帧姿态估计的鲁棒性提升，未扩展到多人姿态跟踪或身份一致性维护。将框架与跟踪模块集成为未来工作方向。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Table 1 | 相较 ViTPose 基线，TAR‑ViTPose 在 ViT‑S/B/L/H 四个规模上均取得一致提升（+1.6 至 +2.3 mAP） |
| Table 2 | ViT‑H 版本在 PoseTrack2017 上以 86.8 mAP（检测框）/ 90.3 mAP（真实框）达到最优 |
| Table 3 | ViT‑S 版本推理速度 413 fps，约为 DSTA 的 8 倍 |
| Table 4 | 关节中心时间聚合（JTA）优于全局自注意力，提升 1.2 mAP |
| Table 5 | GRA 是性能的关键使能器：移除后性能骤降 13.7 mAP |
| Table 6 | 掩码感知注意力贡献 +1.4 mAP，是实现精确关节对齐的核心机制 |
| Figure 4 | 掩码使关节查询令牌的注意力从分散变为精确聚焦于对应关节区域 |

![[assets/figures/papers/paper_list_l1009_https_arxiv_org_abs_2603_05929/figures/007_Table_4.jpg]]
*Table 4: Ablation of different temporal modeling strategies*

![[assets/figures/papers/paper_list_l1009_https_arxiv_org_abs_2603_05929/figures/009_Table_5.jpg]]
*Table 5: Effect of JTA and GRA in our temporal modeling*

### 补充图表

![[assets/figures/papers/paper_list_l1009_https_arxiv_org_abs_2603_05929/figures/019_Table_14.jpg]]
*Table 14: Different number of auxiliary frames. ‘-’ indicates previous frames while ‘+’ indicates subsequent frames*



## 定位与知识库关联

### 与单帧基线的关系

TAR‑ViTPose 直接继承自 **ViTPose**（Xu et al., NeurIPS 2022）的单帧架构：ViT 编码器提取潜在特征，轻量解码器（两层反卷积 + 1×1 卷积）回归关键点热图。两者的根本差异在于**时间建模槽位**——ViTPose 逐帧独立处理视频，完全忽略帧间时间连贯性；TAR‑ViTPose 在 ViT 编码器之后插入即插即用的时间模块（JTA 和 GRA），在不改变原有编码器‑解码器参数的前提下，利用相邻帧的时间线索增强当前帧的特征表示。这一设计使得编码器与解码器可直接复用 ViTPose 在 COCO 上的预训练权重，时间模块则随机初始化后端到端训练 30 轮，最大程度保留了单帧基线的强先验。

### 与视频姿态估计方法的关系

在视频姿态估计谱系中，TAR‑ViTPose 属于**基于 Transformer 的多帧特征融合**路线，但与同类方法存在关键差异：

- **DSTA**（Shi et al., ECCV 2022）同样采用 Transformer 跨帧融合，但使用无差别的全局自注意力在整个时空特征序列上建模，缺乏关节特定的对齐机制，且计算开销较大（ViT‑S 下仅 52 fps）。TAR‑ViTPose 以关节为中心的掩码感知交叉注意力取代全局自注意力，在 ViT‑S 下达到 413 fps 的运行帧率，同时精度显著更高（81.9 vs. 77.3 mAP，HRNet‑W48 基线）。
- **Poseidon**（Zhao et al., CVPR 2023）通过交叉注意力融合多帧特征并复用 ViTPose 解码器，与 TAR‑ViTPose 共享“编码器‑时间模块‑解码器”的整体范式。但 Poseidon 缺少关节特定的特征对齐设计，而 TAR‑ViTPose 的核心创新——可学习关节查询令牌与掩码感知注意力——实现了帧间关节级别的精确对齐，这是其性能优势的关键来源。
- **FAMI‑Pose**（Liu et al., AAAI 2024）和 **DCPose**（Liu et al., CVPR 2021）分别代表基于光流引导和可变形卷积的视频姿态估计路线，与 TAR‑ViTPose 的纯注意力时间聚合范式形成互补。

### 适用边界与局限

TAR‑ViTPose 的适用边界受以下因素制约：

1. **时间一致性未显式约束**：方法通过跨帧特征聚合隐式利用时间信息，但未在损失函数或架构中显式强制帧间姿态一致性。在严重遮挡场景下，相邻帧可能同时缺失同一关节的视觉证据，此时聚合机制无法提供有效补充，可能产生轻微的时间不一致预测。
2. **姿态跟踪问题未覆盖**：本工作仅提供单帧姿态估计的鲁棒框架，未解决跨帧身份关联与轨迹构建问题。在多人密集场景中，需依赖外部检测器提供人员边界框，且不涉及人员 ID 的跨帧维护。
3. **边界框依赖**：与多数视频姿态估计方法一致，TAR‑ViTPose 需要预先检测的人员边界框作为输入。边界框质量直接影响姿态估计精度，这在 Tables 2、9、10 中通过区分检测框与真实边界框的结果已明确体现。
4. **辅助帧数量与效率权衡**：消融实验表明，辅助帧数从 1 增至 4 持续提升性能（ViT‑B 从 83.2 到 84.0 mAP），但更多帧带来的边际收益与计算开销之间的平衡点尚未充分探索。

### 开放问题

1. **多人姿态跟踪扩展**：如何将 JTA/GRA 模块与身份一致性约束集成，构建端到端的多人姿态跟踪框架，是目前最直接的延伸方向。
2. **复杂运动模式鲁棒性**：在快速动作、密集人群遮挡、大幅度姿态变化等更具挑战的运动模式下，当前关节查询令牌的对齐精度是否仍然可靠，需要进一步验证。
3. **跨任务泛化能力**：JTA/GRA 的“聚合‑恢复”范式本质上是一种通用的时空特征增强策略，其是否可推广到其他视频密集预测任务（如视频目标分割、动作识别、视频超分辨率）是一个值得探索的开放问题。
4. **掩码感知注意力的替代方案**：当前掩码依赖解码热图的阈值二值化，这一过程引入了解码器预测质量的依赖。是否存在更直接的空间引导机制（如可学习的空间先验或基于特征的注意力偏置）值得研究。



## 原文 PDF

![[paperPDFs/CVPR_2026/Beyond_Static_Frames_Temporal_Aggregate_and_Restore_Vision_Transformer_for_Human_Pose_Estimation.pdf]]
