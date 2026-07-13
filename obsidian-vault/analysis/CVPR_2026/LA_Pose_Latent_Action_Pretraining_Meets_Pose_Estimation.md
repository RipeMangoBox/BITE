---
title: "LA-Pose: Latent Action Pretraining Meets Pose Estimation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LA_Pose_Latent_Action_Pretraining_Meets_Pose_Estimation.pdf
project_link: "https://la-pose.github.io"
code_link: null
aliases:
- LP
- LA-Pose
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 逆动力学模型自监督学习得到的潜在动作（latent action），编码了帧间运动变化信息，可作为运动中心化（motion-centric）的紧凑表示。
primary_logic: 将从大规模无标注驾驶视频中自监督预训练学到的潜在动作特征重新用于相机姿态估计，替代传统直接依赖3D监督的方式，在仅使用少量标注数据的情况下实现准确的姿态预测，并具有良好的泛化能力。
claims:
- LA-Pose在Waymo和PandaSet基准上比前馈方法（如VGGT、MapAnything）姿态精度提升超过10%，AUC@5分别达到91.4%和86.3%。
- 潜在动作维度消融实验显示，较小的瓶颈（如50-D）虽导致预训练重构损失更高，但促进学习紧凑的运动中心化表示，从而提升下游姿态估计性能。
- 冻结预训练编码器相比微调能更好地保留运动先验，在未见数据集PandaSet上泛化能力显著更强。
- LA-Pose在不同帧率下均显著优于VGGT，即使在1fps极低帧率下仍保持稳定预测。
---

# LA-Pose: Latent Action Pretraining Meets Pose Estimation

> [!tip] 核心洞察
> 将从大规模无标注驾驶视频中自监督预训练学到的潜在动作特征重新用于相机姿态估计，替代传统直接依赖3D监督的方式，在仅使用少量标注数据的情况下实现准确的姿态预测，并具有良好的泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | LA-Pose: 潜在动作预训练与相机姿态估计 |
| 英文题名 | LA-Pose: Latent Action Pretraining Meets Pose Estimation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.27448) · [Project](https://la-pose.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | LA-Pose |
| Dataset | Waymo, PandaSet |

> [!tip] 效果简介
> - Waymo 上，AUC@5 (%) ↑ 91.4 vs 74.8 (VGGT) (+16.6)；ATE-S (×10⁻² RMSE) ↓ 1.20 vs 1.43 (VGGT) (-0.23)；ATE-M (m RMSE) ↓ 0.88 vs 4.74 (MapAnything) (-3.86)。
> - PandaSet 上，AUC@5 (%) ↑ 86.3 vs 75.0 (VGGT) (+11.3)；ATE-S (×10⁻² RMSE) ↓ 1.13 vs 0.99 (VGGT) (+0.14)；ATE-M (m RMSE) ↓ 0.86 vs 7.28 (MapAnything) (-6.42)。

## 概要

### 问题与瓶颈

前馈式相机姿态估计方法近年来取得了显著进展，但其性能严重依赖大规模高质量的3D标注数据。在自动驾驶场景中，获取精确的相机姿态真值需要昂贵的传感器套件和人工标定，导致标注数据规模受限，制约了方法的可扩展性和跨场景泛化能力。这一数据瓶颈构成了当前前馈姿态估计方法的核心制约因素。

### 核心思想

LA-Pose 提出了一条不同于传统“更多标注数据”的路径：**将自监督潜在动作预训练与相机姿态估计深度结合**。其核心洞察在于，从大规模无标注驾驶视频中通过逆动力学模型学到的潜在动作（latent action），天然编码了帧间运动变化的紧凑表示。这些潜在动作本质上是一种**运动中心化**（motion-centric）的视觉特征，可以被重新用于下游的姿态估计任务，从而大幅降低对3D标注数据的依赖。

具体而言，LA-Pose 采用两阶段框架：（1）**潜在动作预训练**阶段，在数百万无标注驾驶视频上训练逆-前向动力学模型，以自监督方式学习编码帧间运动的潜在动作；（2）**姿态后训练**阶段，在冻结的预训练编码器之上附加轻量姿态估计头部，仅使用少量高质量3D标注数据进行微调。这种设计使得模型能够从海量无标注数据中汲取运动先验，同时仅需极少的标注样本即可实现精准的姿态预测。

### 方法定位

在方法谱系上，LA-Pose 位于**自监督表示学习**与**前馈式几何估计**的交叉点。与现有前馈方法（如 **VGGT**（Wang et al., CVPR 2025）、**MapAnything**（Keetha et al., 2025））直接依赖大规模3D监督不同，LA-Pose 将 **Genie** 架构中的潜在动作机制重新用于几何任务。其关键改造包括：引入瓶颈压缩将潜在动作维度从1536压缩至50以促进紧凑表示学习；使用预训练VQ-VAE码本替代像素预测以简化训练；以及设计专用的姿态估计头部从潜在动作中解码相对姿态、视场角和度量尺度。

### 主要结果

在 Waymo 和 PandaSet 两个基准上，LA-Pose 以**显著更少的标注数据**取得了领先性能：

- **Waymo 基准**：AUC@5 达到 91.4%，相比 VGGT 的 74.8% 提升超过 16 个百分点；度量尺度轨迹误差 ATE-M 为 0.88m，远低于 MapAnything 的 4.74m。
- **PandaSet 基准**（未见数据集）：AUC@5 达到 86.3%，相比 VGGT 提升 11.3 个百分点；ATE-M 为 0.86m，展现了优异的跨数据集泛化能力。

消融实验进一步揭示了方法的关键特性：紧凑的潜在维度（50-D）虽导致预训练重构损失升高，却促进了下游姿态估计性能的提升；冻结预训练编码器相比微调能更好地保留运动先验，在未见数据集上泛化能力显著增强；LA-Pose 在不同帧率下均保持稳定预测，即使在 1fps 的极低帧率下仍显著优于 VGGT。

### 局限与开放问题

当前方法在倒车等罕见运动模式下性能退化，中等曲率轨迹（平缓转弯）上的姿态估计精度较低（AUC@5 仅 78.32），因帧间视觉变化微弱导致潜在动作辨别力不足。此外，方法目前仅针对驾驶场景验证，向其他动态场景的泛化能力、完全无监督条件下的度量尺度恢复等问题仍有待探索。



### 问题背景：前馈式相机姿态估计的标注瓶颈

相机姿态估计是3D视觉、自动驾驶和增强现实中的基础任务。近年来，前馈式方法通过直接回归相机参数，在速度和简洁性上展现出显著优势。然而，这类方法的性能高度依赖大规模、高质量的3D标注数据——包括精确的相机外参、深度图和点云。在驾驶场景中，获取此类标注需要昂贵的传感器套件（如LiDAR、高精度IMU）和复杂的人工校准流程，导致标注数据的规模和多样性严重受限。这一瓶颈直接制约了前馈式姿态估计方法的可扩展性和跨场景泛化能力。

### 现有方法缺口：标注依赖与泛化困境

当前主流的前馈式姿态估计基线，如**VGGT**（Wang et al., CVPR 2025）、**Rig3R**（Li et al., 2025）和**MapAnything**（Keetha et al., 2025），均在训练过程中消耗了大量带有3D真值的标注序列。这些方法虽然在域内测试集上表现优异，但面临两个根本性挑战：

1. **标注成本不可持续**：扩展至新场景、新传感器配置或新地理区域时，重新采集和标注数据的成本极高。
2. **泛化能力受限**：过度依赖标注数据中的场景分布，导致在未见环境（如不同城市、天气条件或道路类型）下性能退化明显。

### 核心动机：从无标注视频中学习运动先验

本文的核心动机源于一个关键观察：**互联网规模的驾驶视频中蕴含着丰富的帧间运动信息，这些信息可以以完全自监督的方式被提取和编码**。如果能从数百万小时的无标注驾驶视频中学习到紧凑、可迁移的运动表示，就能大幅降低对3D标注的依赖，同时提升模型的泛化能力。

LA-Pose正是基于这一动机，将**潜在动作（latent action）**——一种从逆动力学模型中自监督学习到的帧间运动编码——重新定位为姿态估计的核心特征。通过在无标注视频上进行大规模预训练，再在少量有标注数据上进行轻量后训练，LA-Pose实现了“标注高效”与“强泛化”的统一。



## 核心方法与创新机理

LA-Pose 的核心创新在于将**大规模自监督潜在动作预训练**与**相机姿态估计**相统一，构建了一个“预训练即运动感知”的两阶段框架。其关键洞察是：逆动力学模型从无标注驾驶视频中自监督学习到的**潜在动作（latent action）**，本质上编码了帧间运动变化的紧凑表示，可直接重新用作相机姿态估计器的输入特征，从而大幅降低对昂贵3D标注数据的依赖。

### 1. 潜在动作的角色转换：从世界模型到姿态估计

在基线方法（如 **Genie**）中，潜在动作通常作为世界模型的动作条件信号，用于驱动视频生成或策略网络中的动作代理。LA-Pose 改变了这一用途：**将潜在动作重新用作相机姿态估计器的输入特征**，编码帧间相对运动信息。

> **Changed Slot**: 潜在动作的用途  
> **Baseline**: 作为世界模型的动作条件信号（用于视频生成）或策略网络中的动作代理  
> **Proposed**: 作为相机姿态估计器的输入特征，编码帧间运动  
> **证据**: “LA-Pose repurposes latent actions as inputs to a lightweight pose-estimation head post-trained on a limited set of high-quality 3D annotations.”

这一角色转换使得模型能够从**百万级无标注驾驶视频**中提取运动中心化（motion-centric）的紧凑表示，仅需少量带有3D标注的序列进行轻量后训练，即可实现准确的姿态预测。

### 2. 逆动力学模型的瓶颈压缩设计

LA-Pose 在逆动力学模型中引入了一个关键的架构改进：**在潜在动作空间中加入瓶颈压缩层**。具体而言，使用一对三层 MLP 将潜在动作维度从 1536 压缩至 50，再解压回 1536。

> **Changed Slot**: 逆动力学模型瓶颈设计  
> **Baseline**: Genie 使用原始维度的潜在动作（无专门压缩）  
> **Proposed**: 引入一对三层 MLP 将潜在动作维度从 1536 压缩至 50 再解压回 1536  
> **证据**: “We further include a pair of three-layer MLPs that compress and de-compress the latent action dimension from 1536 to 50 back to 1536”

消融实验（Table 2）证实了这一设计的有效性：50-D 瓶颈虽然导致预训练重构损失更高（交叉熵从 3.29 升至 3.89），但在下游姿态估计中 AUC@5 与 1536-D 几乎持平，且度量尺度平移误差 ATE-M 从 1.94 降至 1.62。这表明**紧凑的瓶颈强制模型学习更本质的运动信息，同时抑制了信息泄露**，从而提升了迁移效果。

### 3. 前向动力学模型的简化预测目标

与 Genie 训练额外的视频分词器并直接预测像素不同，LA-Pose 采用了更简洁的设计：**使用冻结的预训练 VQ-VAE 码本作为前向动力学模型的预测目标**。

> **Changed Slot**: 前向动力学模型预测目标  
> **Baseline**: Genie 训练额外的视频分词器和前向模型直接预测像素  
> **Proposed**: 使用冻结的预训练 VQ-VAE 码本作为预测目标，简化训练  
> **证据**: “Second, we use a pretrained VQ-VAE codebook as the prediction target.”

这一简化不仅降低了训练复杂度，还使得前向模型仅作为预训练阶段的辅助任务存在——推理时该模块被完全丢弃，不增加部署开销。

### 4. 两阶段训练范式：预训练与后训练的分离

LA-Pose 采用**两阶段训练框架**：第一阶段在大规模无标注驾驶视频上进行自监督潜在动作预训练；第二阶段在少量高质量3D标注数据上训练轻量姿态估计头部。

> **Changed Slot**: 训练范式  
> **Baseline**: Genie 仅进行潜在动作预训练，不包含特定任务头部  
> **Proposed**: 两阶段框架：大规模自监督预训练 + 少量标注数据的轻量姿态后训练  
> **证据**: “LA-Pose has two stages of training: latent action pretraining and camera pose post-training”

关键实验发现（Figure 5）：**冻结预训练编码器**相比微调能更好地保留运动先验，在未见数据集 PandaSet 上泛化能力显著更强。这表明预训练阶段学到的运动表示具有跨数据集的迁移能力，而微调会破坏这种通用性。

### 创新总结

LA-Pose 的四项 changed slots 共同构成了一个完整的创新链条：通过**瓶颈压缩**获得紧凑的运动表示，通过**简化预测目标**降低预训练成本，通过**角色转换**将潜在动作重新用于姿态估计，最终通过**两阶段训练**实现“大规模预训练 + 少量标注微调”的高效范式。这一设计使得 LA-Pose 在使用远少于基线方法的标注数据的情况下，在 Waymo 和 PandaSet 基准上姿态精度提升超过 10%（AUC@5 分别达 91.4% 和 86.3%）。



LA-Pose 采用两阶段训练框架，将大规模自监督潜在动作预训练与相机姿态估计统一起来。其核心设计思路是：**从海量无标注驾驶视频中学习紧凑的运动中心化表示（潜在动作），再将其重新用作轻量姿态估计器的输入特征**，从而在仅使用少量高质量 3D 标注数据的情况下实现准确且可泛化的前馈式姿态预测。

### 两阶段训练流程

框架由两个串联的训练阶段构成，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l2529_https_arxiv_org_abs_2604_27448/figures/002_Figure_2.jpg]]
*Figure 2: Our framework consists of two stages: latent action pretraining and camera pose post-training. In the pretraining stage (top), an inverse–forward dynamics model learns latent actions from consecutive video frames by predicting future tokens through a self-supervised inverse-dynamics objective. These latent actions encode compact, motion-centric representations of frame-to-frame dynamics. In the posttraining stage (bottom left), we attach a lightweight pose estimation head to the pretrained inverse dynamics encoder. The head predicts relative camera translation, rotation (quaternion), field-of-view, and metric scale from the latent actions*

1. **潜在动作预训练（Latent Action Pretraining）**：在数百万无标注驾驶视频上，以完全自监督的方式训练逆动力学–前向动力学模型。该阶段基于 Genie 架构（Bruce et al., 2024）并做了针对性简化：使用冻结的预训练 VQ-VAE 码本作为预测目标，替代直接预测像素；引入瓶颈 MLP 将潜在动作维度从 1536 压缩至 50 再解压回 1536，以促进学习紧凑的运动表示。预训练完成后，前向动力学模型被丢弃，仅保留逆动力学编码器。

2. **相机姿态后训练（Camera Pose Post-Training）**：在预训练好的逆动力学编码器之上附加一个轻量姿态估计头部，使用少量带有 3D 标注的驾驶序列进行监督微调。姿态头部接收潜在动作 token 和可学习的度量尺度 token，通过非因果自注意力 Transformer 处理，直接输出帧间相对位姿（平移、旋转四元数）、视场角（FoV）和度量尺度。

### 模块组成与数据流

框架包含四个核心模块，按数据流顺序依次为：

| 模块 | 功能 | 输入 | 输出 | 使用阶段 |
|------|------|------|------|----------|
| **图像分词器** (Image Tokenizer) | 将连续帧序列转换为视觉 token，基于 ViT 编码器并加入正弦时间编码 | 连续视频帧 | 视觉 token 序列 | 预训练 |
| **逆动力学模型** (Inverse Dynamics Model) | 使用 ST-Transformer 编码器和可学习查询 token，从相邻两帧中聚合信息生成潜在动作 token | 两帧的视觉 token | 潜在动作 token（$15 \times 1536$） | 预训练 + 后训练 |
| **前向动力学模型** (Forward Dynamics Model) | 利用潜在动作预测未来帧的 VQ-VAE 码本 logits，提供自监督训练信号 | 潜在动作 + 当前帧 token | 下一帧码本 logits | 仅预训练 |
| **姿态估计头部** (Pose Estimation Head) | 在逆动力学编码器之上加入 Transformer，处理潜在动作 token 和度量尺度 token，输出位姿参数 | 潜在动作 token + 度量尺度 token | 相对平移、旋转四元数、FoV、度量尺度 | 仅后训练 |

### 关键设计决策

**瓶颈压缩**：逆动力学模型中的瓶颈 MLP（1536 → 50 → 1536）是方法的关键创新之一。消融实验（Table 2）表明，较小的潜在维度（50-D）虽导致预训练重构损失更高，但能迫使模型学习更紧凑、更具判别力的运动中心化表示，从而在下游姿态估计中取得相当甚至更优的性能——50-D 潜在动作的 AUC@5 与 1536-D 几乎持平，而 ATE-M 从 1.94 降至 1.62，表明压缩有效缓解了信息泄露问题。

**冻结 vs 微调**：后训练阶段冻结预训练的逆动力学编码器，仅训练姿态头部。实验（Figure 5）显示，冻结骨干网络能更好地保留预训练阶段学到的运动先验，在未见数据集 PandaSet 上泛化能力显著优于微调方案，尤其在预训练数据规模较小时差异更为明显。

**度量尺度预测**：姿态头部通过可学习的度量尺度 token 显式预测尺度因子 $s = \mathrm{mean}_i(\|\mathbf{t}_i\|_2)$，并输出尺度无关的相对平移 $\tilde{\mathbf{t}}_i = \mathbf{t}_i / \max(s, \epsilon)$（$\epsilon=1.0$ 保证数值稳定），使模型能够在有标注数据上恢复绝对尺度，同时保持对尺度变化的鲁棒性。

### 补充图表

![[assets/figures/papers/paper_list_l2529_https_arxiv_org_abs_2604_27448/figures/001_Figure_1.jpg]]
*Figure 1: Overview of LA-Pose. We introduce a two-stage framework that unifies large-scale latent action pretraining with camera pose estimation. From millions of unlabeled driving videos, an inverse–forward dynamics model learns latent actions that encode interframe motion in a fully self-supervised manner. When visualized in T-SNE space, these latent actions exhibit structured clusters that align closely with true ego-motion distributions. We then re-purpose these representations through lightweight supervised post-training on limited 3D-annotated data, enabling feed-forward pose prediction that is both accurate and highly generalizable. LA-Pose achieves state-of-the-art pose estimation while requi...*



### 整体两阶段框架

LA-Pose 采用“大规模自监督预训练 + 少量有标注数据轻量后训练”的两阶段范式。预训练阶段，逆动力学模型与前向动力学模型联合从连续视频帧中学习潜在动作（latent action）——一种紧凑的、以运动为中心的帧间变化表示；后训练阶段，在冻结的预训练逆动力学编码器之上附加轻量姿态估计头部，仅使用有限的 3D 标注序列进行监督微调，输出相机相对姿态及度量尺度。

### 图像分词器

图像分词器将输入帧序列转化为视觉 token 序列。其主干为 Vision Transformer 编码器，对每一帧独立提取 patch 特征，并注入正弦时间编码以保留帧序信息。该模块在预训练阶段与前向动力学模型共享一个冻结的预训练 VQ-VAE 码本作为预测目标——这是对原始 Genie 架构的关键简化之一：不再训练额外的视频分词器，而是直接复用现成的离散视觉码本，降低了预训练复杂度。

### 逆动力学模型

逆动力学模型是潜在动作学习的核心。它接收连续两帧的视觉 token 序列，通过一个时空 Transformer（ST-Transformer）编码器进行跨帧信息聚合。具体地，模型引入一个 1536 维的可学习查询 token，与两帧的视觉 token 拼接后送入 ST-Transformer，经自注意力机制从帧间差异中蒸馏出运动信息，最终输出 15 个 1536 维的潜在动作 token。这些 token 构成了对帧间动力学变化的紧凑编码。

为强化潜在动作的运动中心化特性，LA-Pose 在逆动力学模型中引入了一个关键的结构性约束——瓶颈压缩。一对三层 MLP 将潜在动作维度从 1536 压缩至 50，再解压回 1536：

$$\text{latent action}_{\text{compressed}} = \text{MLP}_{\text{enc}}(z), \quad \hat{z} = \text{MLP}_{\text{dec}}(\text{latent action}_{\text{compressed}})$$

其中 $z \in \mathbb{R}^{15 \times 1536}$ 为压缩前的潜在动作 token。50-D 的瓶颈迫使模型丢弃与运动无关的视觉细节，仅保留对帧间位姿变化至关重要的信息。消融实验证实，虽然更小的瓶颈导致预训练重构损失升高，但下游姿态估计性能反而提升——50-D 潜在动作在 AUC@5 上接近 1536-D，同时 ATE-M 从 1.94 降至 1.62，验证了紧凑表示可有效抑制信息泄露、增强迁移能力。

### 前向动力学模型

前向动力学模型仅在预训练阶段使用，推理时被完全丢弃。它以潜在动作和当前帧的 VQ-VAE 码本索引为输入，通过一个轻量 MLP 头部预测下一帧在共享码本上的 logits 分布。预训练损失为交叉熵：

$$\mathcal{L}_{\text{pretrain}} = -\sum_{k} \log p(c_k^{\text{next}} | \text{latent action}, c^{\text{curr}})$$

其中 $c_k^{\text{next}}$ 为下一帧第 $k$ 个 token 的真实码本索引。该自监督目标不依赖任何 3D 标注，仅通过“预测未来”的代理任务驱动逆动力学模型学习有意义的帧间运动表示。

### 姿态估计头部

后训练阶段，姿态估计头部附加于冻结的逆动力学编码器之上。头部引入一个可学习的度量尺度 token $\mathbf{s} \in \mathbb{R}^{1536}$，与 15 个潜在动作 token 拼接后送入一个非因果自注意力 Transformer。Transformer 输出经独立 MLP 分支分别预测：

- **相对平移** $\mathbf{t}_i \in \mathbb{R}^3$ 与**旋转四元数** $\mathbf{q}_i \in \mathbb{R}^4$（7-D 相对姿态）
- **视场角**（field-of-view）
- **度量尺度** $s$

度量尺度定义为所有帧平移分量的平均 L2 范数：

$$s = \mathrm{mean}_i(\|\mathbf{t}_i\|_2)$$

为解耦尺度估计与姿态预测，训练时对平移分量做尺度无关归一化：

$$\tilde{\mathbf{t}}_i = \frac{\mathbf{t}_i}{\max(s, \epsilon)}$$

其中 $\epsilon = 1.0$ 用于数值稳定，防止静止序列中分母过小。该归一化使姿态头部在训练初期即可专注于学习运动方向，而度量尺度 token 则通过独立分支逐步恢复绝对尺度信息。

### 关键设计决策的因果逻辑

1. **冻结 vs. 微调**：冻结预训练骨干网络保留了从百万级无标注视频中习得的运动先验，在未见数据集（PandaSet）上泛化能力显著优于微调——尤其在预训练数据规模较小时，微调会破坏通用运动表示，导致 ATE-M 显著上升。
2. **瓶颈压缩**：50-D 瓶颈并非单纯的计算优化，而是通过信息瓶颈强制潜在动作丢弃场景外观等与运动无关的变量，使其成为真正的“运动中心化”表示。这解释了为何更小的维度反而带来更强的下游性能。
3. **VQ-VAE 码本作为预测目标**：相比 Genie 直接预测像素，使用离散码本将预测空间从高维像素流形压缩到有限类别分布，降低了预训练难度，同时保留了足够的运动判别信息。

### 补充图表

![[assets/figures/papers/paper_list_l2529_https_arxiv_org_abs_2604_27448/figures/006_Figure_5.jpg]]
*Figure 5: Comparison of pose post-training with frozen and finetuned inverse-dynamics encoders. The x-axis shows pretraining data scale. The y-axis reports metric-scale ATE-M (↓). Both settings perform similarly on Waymo, while the frozen backbone generalizes markedly better to the unseen PandaSet*

![[assets/figures/papers/paper_list_l2529_https_arxiv_org_abs_2604_27448/figures/007_Table_2.jpg]]
*Table 2: Ablation on latent action dimension. Comparison between different latent dimensions under the post-training setting on Waymo. Larger latent spaces yield lower reconstruction loss during pre-training but enable information leakage, leading to degraded downstream pose estimation. Pre-training losses at 100k and 200k steps are measured as cross-entropy on the VQ-VAE code prediction*



## 实验与关键发现

### 主要结果

LA-Pose 在两个主流驾驶场景相机姿态估计基准上均取得了最优性能，且仅使用了极少量的 3D 标注数据。Table 1 汇总了 Waymo 和 PandaSet 上的定量对比。

![[assets/figures/papers/paper_list_l2529_https_arxiv_org_abs_2604_27448/figures/003_Table_1.jpg]]
*Table 1: Pose estimation results, reporting area under the curve at an error threshold of 5° (AUC@5), the average aligned trajectory error in scale units (ATE-S RMSE), and in meters (ATE-M RMSE). As Rig3R was trained on the complete PandaSet dataset, it is excluded from the PandaSet evaluation*

**Waymo 基准**：LA-Pose 在 AUC@5 指标上达到 **91.4%**，相比前馈式基线 **VGGT** (Wang et al., CVPR 2025) 的 74.8% 提升了 **+16.6 个百分点**；在尺度无关的平移误差 ATE-S 上，LA-Pose 取得 1.20×10⁻² RMSE，优于 VGGT 的 1.43×10⁻²。在度量尺度平移误差 ATE-M 上，LA-Pose 的 0.88m 相比 **MapAnything** (Keetha et al., 2025) 的 4.74m 降低了 **3.86m**，差距显著。

**PandaSet 基准（未见数据集）**：LA-Pose 的 AUC@5 达到 **86.3%**，比 VGGT 的 75.0% 高出 **+11.3 个百分点**；ATE-M 为 0.86m，而 MapAnything 高达 7.28m，差距达 6.42m。值得注意的是，LA-Pose 在 PandaSet 上的 ATE-S（1.13×10⁻²）略高于 VGGT（0.99×10⁻²），但考虑到 PandaSet 是完全未见的域外数据，且 LA-Pose 未在该数据集上进行任何微调，这一微小的尺度误差差距是可接受的。

**公平性说明**：Rig3R 因在完整 PandaSet 上训练，故在 PandaSet 评估中被排除。所有基线方法均使用了远超 LA-Pose 的监督 3D 标注数据——VGGT 和 MapAnything 包含大量非驾驶场景的密集几何标签，而 LA-Pose 仅使用 Waymo、nuScenes、Argoverse 的少量标注序列进行后训练。

Figure 3 的定性可视化进一步印证了定量结论：LA-Pose（绿色）预测的相机轨迹与真值（红色）高度吻合，在 Waymo 和 PandaSet 场景中均表现出稳定且时间一致的位姿估计，而 VGGT（青色）和 Rig3R（品红）在部分序列中出现明显漂移。

![[assets/figures/papers/paper_list_l2529_https_arxiv_org_abs_2604_27448/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative results of camera pose estimation. Comparison of predicted camera trajectories: Ours (green), Rig3R [21] (magenta), VGGT [31] (cyan), and ground truth (red). Camera frustums are visualized at timestamps 0, 5, 10, and 15, with trajectory lines connecting all camera positions in the sequence. The first six examples show results on the Waymo dataset, while the last six are from PandaSet. All trajectories are projected onto the xz plane for visualization clarity*

### 消融实验

**潜在动作维度的影响**：Table 2 揭示了潜在动作瓶颈设计的关键作用。当潜在动作维度从原始的 1536-D 压缩至 50-D 时，预训练阶段的前向预测交叉熵损失从 3.96 升至 4.70（100k 步），表明重构难度增加；然而，下游姿态估计的 AUC@5 几乎持平（1536-D 为 91.4%，50-D 为 91.2%），ATE-M 却从 1.94m 降至 **1.62m**。这一反直觉现象说明：较大的潜在空间虽然降低了预训练损失，但也引入了“信息泄露”——编码器可能将帧间外观细节而非纯粹的运动信息编码进潜在动作，从而损害下游迁移的泛化性。50-D 的紧凑瓶颈强制模型学习运动中心化的表示，验证了 **瓶颈压缩是提升位姿估计性能的有效因果调节旋钮**。

**冻结与微调预训练骨干**：Figure 5 展示了冻结与微调逆动力学编码器在不同预训练数据规模下的对比。在 Waymo（域内）上，两者性能接近；但在 PandaSet（域外）上，冻结骨干的 ATE-M 显著低于微调版本，且随着预训练数据规模减小，这一差距进一步拉大。这表明冻结策略更好地保留了大规模自监督预训练中习得的运动先验，对未见场景的泛化能力更强。

### 鲁棒性分析

**帧率鲁棒性**：Table 3 展示了 LA-Pose 与 VGGT 在不同帧采样率下的对比。LA-Pose 在 4.0fps、1.3fps 和 1.0fps 下分别取得 93.4%、88.6% 和 85.7% 的 AUC@5，ATE-S 始终低于 VGGT。尤其在 1.0fps 的极端低帧率下，VGGT 的 ATE-S 退化至 2.19×10⁻²，而 LA-Pose 仅为 1.16×10⁻²，降幅温和。这一时间鲁棒性源于潜在动作预训练阶段对多帧率视频的大规模学习，使得模型对时间稀疏采样不敏感。

### 失败模式与局限性

**轨迹曲率与加速度的影响**：Table 4 按轨迹曲率 $\kappa = d\psi / ds$ 和加速度分层分析了 AUC@5。LA-Pose 在中等曲率（0.01–0.1 m⁻¹）轨迹上性能最低，AUC@5 仅 **78.32%**，成为当前方法的主要失效模式。原因在于中等曲率对应平缓转弯，帧间视觉运动线索微弱，潜在动作的辨别力不足以精确推断相机姿态变化。相比之下，高曲率急转弯和直线行驶场景的视觉信号更强，性能明显更好。

**倒车场景**：Figure 6 展示了一个倒车场景的失败案例。由于后训练数据中倒车样本极为稀少，模型在该分布外条件下性能退化，预测轨迹与真值出现偏差。然而，预训练骨干仍能产生部分一致的轨迹，表明自监督预训练为长尾场景保留了基础运动理解能力。

**其他局限**：(1) 度量尺度预测完全依赖后训练中的有标注数据，在完全无监督条件下无法恢复绝对尺度；(2) 当前预训练仅覆盖驾驶场景，向室内机器人等动态场景的泛化能力未经验证；(3) 前向动力学模型和 VQ-VAE 编码器在预训练中增加了额外计算开销，尽管推理时被丢弃。

### 图表结论速览

- **Table 1**：LA-Pose 在 Waymo 和 PandaSet 上均以显著优势超越前馈式基线，仅需极少标注数据。
- **Table 2**：50-D 潜在动作瓶颈在几乎不牺牲 AUC@5 的前提下，将 ATE-M 降低 16.5%，验证了紧凑运动中心化表示的有效性。
- **Table 3**：LA-Pose 在 1fps 极低帧率下仍保持稳定预测，展现强时间鲁棒性。
- **Table 4**：中等曲率轨迹（0.01–0.1 m⁻¹）是当前方法的主要失效区间，AUC@5 降至 78.32%。
- **Figure 3**：定性可视化证实 LA-Pose 的轨迹预测在域内和域外场景中均与真值高度一致。
- **Figure 5**：冻结预训练骨干在未见数据集上泛化能力显著优于微调。
- **Figure 6**：倒车等长尾场景下性能退化，但预训练骨干保留了部分运动一致性。

![[assets/figures/papers/paper_list_l2529_https_arxiv_org_abs_2604_27448/figures/009_Table_3.jpg]]
*Table 3: Robustness to frame sampling rate. Comparison between LA-Pose and VGGT [31] under different frame rates on the Waymo benchmark. LA-Pose achieves consistently lower trajectory error (ATE-S) and higher pose accuracy (AUC@5)*

![[assets/figures/papers/paper_list_l2529_https_arxiv_org_abs_2604_27448/figures/010_Table_4.jpg]]
*Table 4: AUC@5 (%) across different trajectory curvatures and accelerations on the Waymo validation set*

![[assets/figures/papers/paper_list_l2529_https_arxiv_org_abs_2604_27448/figures/008_Figure_6.jpg]]
*Figure 6: Failure case under reverse motion. Performance degrades when the vehicle moves backward, a rare condition in the supervised training set. Despite this distribution gap, the pretrained backbone still produces partially consistent trajectories*

### 补充图表

![[assets/figures/papers/paper_list_l2529_https_arxiv_org_abs_2604_27448/figures/011_Figure_7.jpg]]
*Figure 7: Qualitative results under low frame rate (1 fps) on Waymo. Each example shows camera poses projected onto the xz plane, with frustums drawn at frames 0, 5, 10, and 15. LA-Pose (green) maintains stable and temporally consistent motion across the sequence, whereas VGGT [31] (cyan) exhibits noticeable drift and discontinuities under sparse temporal sampling*

![[assets/figures/papers/paper_list_l2529_https_arxiv_org_abs_2604_27448/figures/012_Figure_8.jpg]]
*Figure 8: Qualitative results on OpenDV–YouTube. Each example shows scenes from diverse cities and viewpoints collected from online YouTube driving videos. LA-Pose produces stable and temporally consistent trajectories across a wide variety of conditions, including urban streets, highways, and curved mountain roads. The results qualitatively demonstrate strong generalization from our pre-trained backbone to uncalibrated, in-the-wild videos*



## 定位与知识库关联

### 与前馈式相机姿态估计的关系

LA-Pose 直接对标当前前馈式相机姿态估计的新范式，在性能与数据效率上均形成显著对比。主要基线包括：

- **VGGT** (Wang et al., CVPR 2025)：前馈式相机姿态估计基线，依赖大量带有3D标注的数据进行端到端监督训练。在Waymo基准上AUC@5为74.8%，PandaSet上为75.0%。
- **MapAnything** (Keetha et al., 2025)：通用前馈式度量3D重建方法，使用密集几何标签训练。在Waymo上ATE-M为4.74m，PandaSet上为7.28m。
- **Rig3R** (Li et al., 2025)：基于稠密姿态ray map的前馈式3D重建方法，额外在KITTI等数据集上训练。

LA-Pose 与上述方法的根本区别在于**训练范式**：上述基线均依赖大规模3D标注数据进行直接监督学习，而LA-Pose采用两阶段框架——先在海量无标注驾驶视频上进行自监督潜在动作预训练，再在少量标注序列上后训练轻量姿态头部。这一范式转换带来两个关键优势：

1. **数据效率**：仅使用Waymo、nuScenes、Argoverse的少量标注序列进行后训练，却取得了超越使用数倍乃至数十倍标注数据训练的基线方法的性能。
2. **泛化能力**：在未见数据集PandaSet上，LA-Pose的AUC@5达86.3%，比VGGT的75.0%高出11.3个百分点；ATE-M仅0.86m，比MapAnything的7.28m低6.42m。

### 与Genie架构的继承与简化

LA-Pose 的预训练阶段直接继承自 **Genie** 架构（Bruce et al., 2024），但针对姿态估计目标进行了三项关键简化：

| 模块 | Genie 原始设计 | LA-Pose 改进 | 改进动机 |
|------|---------------|-------------|---------|
| 潜在动作维度 | 使用原始维度，无专门压缩 | 引入三层MLP瓶颈将1536维压缩至50维再解压 | 强制学习紧凑的运动中心化表示，抑制信息泄露 |
| 前向模型预测目标 | 训练额外视频分词器，直接预测像素 | 使用冻结的预训练VQ-VAE码本作为预测目标 | 简化训练流程，降低计算开销 |
| 下游任务 | 仅进行可能性动作预训练，无特定任务头部 | 两阶段框架：预训练 + 轻量姿态后训练 | 将运动先验迁移至具体几何感知任务 |

消融实验（Table 2）证实了瓶颈设计的关键作用：50维潜在动作在预训练交叉熵损失上虽高于1536维（表明重构更困难），但在下游姿态估计上ATE-M从1.94降至1.62，AUC@5几乎持平。这表明紧凑瓶颈迫使逆动力学模型丢弃与运动无关的视觉细节，学习更纯粹的运动表征。

### 适用边界与局限

**适用场景**：

- 驾驶场景下的前馈式相机姿态估计，包括城市街道、高速公路、弯曲山路等多种路况。
- 对帧率变化具有较强鲁棒性：在4.0fps到1.0fps范围内均保持稳定预测（Table 3），即使在1fps极低帧率下AUC@5仍达85.7%，而VGGT在低帧率下退化严重。
- 对未见数据集具有良好的零样本泛化能力（Figure 5），得益于冻结预训练骨干网络保留的运动先验。

**已知失效模式**：

1. **倒车场景**（Figure 6）：自车向后运动在后训练数据中极为罕见，导致性能退化。预训练骨干网络仍能产生部分一致的轨迹，表明大规模预训练数据扩展可能缓解此问题。
2. **中等曲率轨迹**（Table 4）：在曲率 $0.01 < \kappa < 0.1 \, \text{m}^{-1}$ 的平缓转弯场景中，AUC@5降至78.32%，成为当前方法的主要失效模式。根本原因在于帧间视觉运动线索微弱，潜在动作的辨别力不足。
3. **度量尺度依赖标注**：绝对尺度的恢复依赖于后训练阶段的有标注数据，在完全无监督条件下无法获取度量尺度。
4. **场景泛化未验证**：当前预训练仅覆盖驾驶场景，向室内机器人、人体动作捕捉等其他动态场景的泛化能力未经实验检验。

### 开放问题

1. **长尾覆盖**：能否通过扩展预训练数据集的规模和多样性（如增加倒车、急转弯等场景）来自动缓解长尾失效模式？
2. **跨领域迁移**：潜在动作表示是否可泛化至非驾驶领域的运动估计任务，如人体动作捕捉或机器人操作？
3. **表示压缩极限**：如何在进一步压缩潜在动作维度的同时不损失运动信息，以提升计算效率？
4. **任务扩展**：将自监督预训练与少量有监督微调的策略应用于其他几何感知任务（如深度估计、光流）的可行性？
5. **无监督尺度恢复**：在完全无3D标定的情况下，是否可通过自监督精调（如光度一致性约束）恢复度量尺度？



## 原文 PDF

![[paperPDFs/CVPR_2026/LA_Pose_Latent_Action_Pretraining_Meets_Pose_Estimation.pdf]]
