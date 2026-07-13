---
title: "MagicMotion: Controllable Video Generation with Dense-to-Sparse Trajectory Guidance"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/MagicMotion_Controllable_Video_Generation_with_Dense_to_Sparse_Trajectory_Guidance.pdf
project_link: https://quanhaol.github.io/magicmotion-site/
code_link: null
aliases:
- MagicMotion
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "渐进式稠密到稀疏训练策略与潜在分割损失（Latent Segment Loss）。该策略让模型在掩膜、边界框、稀疏框三种条件下逐步迁移知识，分割损失则在稀疏训练时通过潜在空间掩膜预测增强对物体精细形状的感知，从而显著提升轨迹控制精度。"
primary_logic: "通过从稠密分割掩膜到稀疏边界框的三阶段渐进训练，并引入轻量级分割头在潜在空间施加像素级形状监督，可在不显著增加计算开销的前提下，使视频生成模型在多种轨迹输入下均能保持物体形状一致性与运动精准度。"
claims:
- "在MagicBench基准上，MagicMotion在全部四项指标上均大幅优于所有对比方法，例如FID较Tora降低11.21，Mask IoU提升32.62%。"
- "移除渐进训练或潜在分割损失后，模型在MagicBench和DAVIS上的轨迹控制精度（MIoU/B.IoU）均显著下降。"
- "使用自建MagicData训练比使用MeViS+MOSE组合数据集在各项指标上均有提升，说明高质量带轨迹标注的视频数据对模型至关重要。"
- "渐近训练策略使得模型在仅提供稀疏边界框条件下（Stage3）仍能预测出合理的潜在分割掩膜，从而在无完整标注帧上保持物体形状。"
---

# MagicMotion: Controllable Video Generation with Dense-to-Sparse Trajectory Guidance

> [!tip] 核心洞察
> 通过从稠密分割掩膜到稀疏边界框的三阶段渐进训练，并引入轻量级分割头在潜在空间施加像素级形状监督，可在不显著增加计算开销的前提下，使视频生成模型在多种轨迹输入下均能保持物体形状一致性与运动精准度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MagicMotion: 基于从稠密到稀疏轨迹引导的可控视频生成 |
| 英文题名 | MagicMotion: Controllable Video Generation with Dense-to-Sparse Trajectory Guidance |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2503.16421) · [Project](https://quanhaol.github.io/magicmotion-site/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | MagicMotion |
| Dataset | MagicBench, DAVIS |

> [!tip] 效果简介
> - MagicBench 上，FID ↓ 为 15.06，对比 26.27，变化 -11.21。
> - MagicBench 上，FVD ↓ 为 112.69，对比 245.23，变化 -132.54。
> - MagicBench 上，Mask IoU % ↑ 为 91.57，对比 58.95，变化 +32.62。

## 概要

**核心问题**：现有轨迹可控视频生成方法仅支持单一轨迹格式（如点、光流或边界框），在稀疏轨迹条件下难以保持物体形状一致性与精准运动控制；同时缺乏公开大规模训练数据集与按物体数量分层的评估基准，导致多物体复杂场景下性能受限。

**方法定位**：MagicMotion 提出一种从稠密到稀疏的渐进式轨迹控制框架，支持掩膜、边界框、稀疏框三种轨迹输入。其核心机制包括：Trajectory ControlNet（由 DiT 块可训练副本与零初始化卷积构成）将轨迹条件注入基础视频生成模型；三阶段渐进训练策略（Stage1 掩膜 → Stage2 密集边界框 → Stage3 稀疏边界框）使模型逐步迁移知识；以及潜在分割损失（Latent Segment Loss），通过轻量级分割头在潜在空间施加像素级形状监督，在稀疏训练条件下增强对物体精细形状的感知。

**关键发现**：在自建 MagicBench 基准上，MagicMotion 在 FID、FVD、Mask IoU、Box IoU 四项指标上均大幅优于所有对比方法（如相较于 Tora，FID 降低 11.21，Mask IoU 提升 32.62%）。消融实验表明，移除渐进训练或潜在分割损失后，轨迹控制精度显著下降；使用自建 MagicData 训练相比使用公开数据集组合（MeViS+MOSE）在各指标上均有提升，说明高质量带轨迹标注的视频数据对模型至关重要。此外，渐进训练策略使模型在仅提供稀疏边界框条件下仍能预测出合理的潜在分割掩膜，从而在无完整标注帧上保持物体形状。

近年来，扩散模型（Diffusion Models）的快速发展大幅提升了图像到视频（Image-to-Video, I2V）生成的质量。然而，让生成视频中的物体按照用户指定的轨迹运动，仍然是一个核心挑战。现有的轨迹可控视频生成方法通常只能处理单一格式的轨迹条件——例如仅支持光流、点轨迹或边界框——这严重限制了用户输入的灵活性。更关键的是，在仅提供稀疏轨迹（如少数关键帧上的边界框）的场景下，这些方法普遍难以维持物体的形状一致性与精准的运动控制，导致生成结果出现形变、漂移或物体丢失等问题。

这一瓶颈的深层原因来自两个方面。其一，缺乏公开的大规模、高质量、带轨迹标注的视频训练数据集，使得模型难以学习复杂场景下的物体运动规律。其二，现有评估基准未按受控物体数量进行分层，导致方法在简单场景上的表现掩盖了其在多物体复杂场景下的性能缺陷。

针对上述缺口，MagicMotion 提出了一个统一的轨迹可控视频生成框架，其核心动机在于：通过一种从稠密到稀疏的渐进式训练策略，让模型能够同时兼容掩膜（Mask）、密集边界框（Box）和稀疏边界框（Sparse Box）三种粒度的轨迹输入，从而在保持生成质量的同时，显著提升对稀疏轨迹条件的鲁棒性。

## 核心方法与创新机理

MagicMotion 的核心创新在于解决了现有轨迹可控视频生成方法的两大瓶颈：**单一轨迹格式的刚性限制**与**稀疏条件下物体形状一致性差**的问题。现有方法（如基于光流的 **Motion-I2V**、基于点的 **DragAnything** 或仅支持边界框的 **Tora**）均只能处理一种轨迹条件，且在仅提供稀疏边界框时，物体形状极易发生扭曲或丢失。MagicMotion 通过以下三个紧密耦合的“changed slots”实现了突破：

### 1. 轨迹条件注入方式：Trajectory ControlNet

不同于仅依赖文本或图像条件的基线方法，MagicMotion 引入了一个 **Trajectory ControlNet** 分支。该分支由预训练 DiT 块的可训练副本构成，将轨迹图（掩膜、边界框或稀疏框）编码后，通过零初始化卷积层逐层注入到基础模型的对应 DiT 块中（Figure 2）。这种设计使得模型能够灵活接收任意形式的轨迹输入，而无需改变基础视频生成模型的架构。

### 2. 训练流程：从稠密到稀疏的三阶段渐进训练

MagicMotion 摒弃了直接使用单一格式轨迹训练的方式，采用三阶段渐进式训练策略：
- **Stage 1**：使用稠密分割掩膜训练，建立对物体精确形状的理解。
- **Stage 2**：使用密集边界框训练，继承 Stage 1 权重，将形状知识迁移到框级轨迹。
- **Stage 3**：使用稀疏边界框训练（少于 10 帧有标注），继承前两阶段权重，使模型在仅有极少量轨迹信息时仍能保持物体形状一致性。

这一策略的因果机制在于：模型在从稠密到稀疏的知识迁移过程中，学会了从稀疏轨迹中推断出物体完整的形状与运动信息。**决定性证据**显示，移除渐进训练后，生成结果出现头部形状扭曲、转身时出现第二张脸等严重缺陷（Figure 7）；定量上，在 MagicBench 上 Mask IoU 下降 1.39–2.39 个百分点（Table 3）。

### 3. 辅助损失函数：潜在分割损失（Latent Segment Loss）

这是 MagicMotion 最精巧的设计。在 Stage 2/3 训练时，模型仅接收边界框或稀疏框作为轨迹条件，缺乏像素级的形状监督。为此，MagicMotion 引入了一个轻量级分割头，从 DiT 多层特征中预测潜在空间的分割掩膜，并以欧氏距离与真实掩膜轨迹的潜在编码计算损失：

$$\mathcal{L}_{seg} = \mathbb{E}_{t, \epsilon \sim \mathcal{N}(0, I), z_0} \left[ \| Z_{segment} - Z_{mask} \|_2^2 \right]$$

总损失函数为：

$$\mathcal{L} = \mathcal{L}_{diffusion} + \lambda \cdot \mathcal{L}_{seg}$$

其中 $\lambda$ 在 Stage 1 为 0，在 Stage 2/3 为 0.5。这一设计的关键在于：分割头仅在训练时使用，不增加推理开销，却能在稀疏轨迹条件下为模型提供稠密的形状监督信号。**决定性证据**表明，移除该损失后，物体形状感知能力显著下降（如手臂残缺、口红变成矩形，Figure 8）；在 MagicBench 上 Mask IoU 下降 1.96–4.75 个百分点（Table 3）。更重要的是，即使在仅提供稀疏边界框的 Stage 3，模型仍能预测出合理的潜在分割掩膜（Figure 12），证明了该机制的因果有效性。

### 创新协同效应

这三个 changed slots 并非孤立存在，而是形成了一个正向反馈闭环：Trajectory ControlNet 提供了统一的轨迹条件接口，渐进训练策略使得模型能从稠密到稀疏逐步泛化，而潜在分割损失则在稀疏阶段提供了关键的形状监督信号。三者协同作用，使得 MagicMotion 在 MagicBench 基准上相比最强基线 **Tora** 实现了 Mask IoU 提升 32.62%、FID 降低 11.21 的显著优势（Table 1）。

![[assets/figures/papers/paper_list_l2_MagicMotion_Controllable_Video_Generation_with_Dense_to_Sparse_Trajector/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MagicMotion Architecture (text prompt and encoder are omitted for simplicity). MagicMotion employs a pretrained 3D VAE to encode the input trajectory, first-frame image, and training video into latent space. It has two separate branches: the video branch processes video and image tokens, and the trajectory branch uses Trajectory ControlNet to fuse trajectory and image tokens, which is later integrated to the video branch through a zero-initialized convolution layer. Besides, diffusion features from DiT blocks are concatenated and processed by a trainable segment head to predict latent segmentation masks, which contribute to our latent segment loss*

MagicMotion 的整体 pipeline 围绕一个预训练的图像到视频（I2V）扩散 Transformer（DiT）基础模型构建，通过外挂的轨迹控制分支与辅助分割监督，实现对多种轨迹条件的统一响应。其核心设计遵循“条件编码—特征融合—潜在空间监督”的信息流路径。

**输入与编码。** 系统接收三路输入：首帧图像 $I \in \mathbb{R}^{H \times W \times 3}$、轨迹条件图 $C \in \mathbb{R}^{T \times H \times W \times 3}$（可为掩膜、边界框或稀疏框）以及对应的训练视频 $V \in \mathbb{R}^{T \times H \times W \times 3}$。三路数据统一由预训练的 3D VAE 压缩至共享潜在空间，得到视频潜在表示与轨迹潜在表示（Figure 2）。

**双分支架构。** 潜在空间中的处理分为两条并行的 DiT 分支：
- **视频分支**：即冻结的基础 I2V 模型（CogVideoX-5B-I2V 或 Wan2.1 1.3B），负责视频潜在表示的扩散去噪与生成。
- **轨迹分支（Trajectory ControlNet）**：由基础模型所有 DiT 块的可训练副本构成，接收轨迹潜在表示与图像潜在表示，经逐层处理后，通过零初始化卷积层将条件特征逐层注入视频分支对应的 DiT 块。这一设计使得轨迹条件能够以残差方式渐进地调制生成过程，而不会破坏基础模型的先验知识。

**潜在分割监督。** 在 Stage2 和 Stage3 训练阶段，系统额外引入一个轻量级分割头（Segment Head）。该模块接收 DiT 多层扩散特征 $Z_{feature}$，在潜在空间中预测分割掩膜 $Z_{segment}$，并与真实掩膜轨迹的潜在表示 $Z_{mask}$ 计算欧氏距离作为潜在分割损失 $\mathcal{L}_{seg}$。该损失仅在训练时使用，不增加推理开销。

**数据流闭环。** 训练时，总损失为扩散损失与潜在分割损失的加权和：

$$\mathcal{L} = \mathcal{L}_{diffusion} + \lambda \cdot \mathcal{L}_{seg}$$

其中 $\lambda=0$（Stage1）或 $\lambda=0.5$（Stage2/3）。推理时，仅需提供首帧图像与任意形式的轨迹条件图，模型即可生成物体沿指定路径运动的高质量视频。

**模块关系总结。** 3D VAE 负责跨模态潜在空间对齐，Trajectory ControlNet 负责将轨迹条件转化为对基础模型的调制信号，Segment Head 则在稀疏轨迹训练阶段提供像素级形状监督，三者协同实现了从稠密掩膜到稀疏边界框的渐进式轨迹控制能力。

MagicMotion 的核心架构由四个关键模块构成：3D VAE 编码器、基础 DiT 视频生成模型、Trajectory ControlNet 轨迹条件注入分支，以及轻量级 Segment Head 分割头。各模块协同工作，实现从稠密到稀疏的多层级轨迹可控视频生成。

### 3D VAE 编码器

模型采用预训练的 3D VAE 将输入图像、训练视频和轨迹条件图统一压缩到潜在空间。给定输入图像 $I \in \mathbb{R}^{H \times W \times 3}$ 和轨迹条件图 $C \in \mathbb{R}^{T \times H \times W \times 3}$，编码器将其映射为潜在表示，供后续 DiT 模块处理。这种统一编码方式使得不同模态的信息能够在同一特征空间中进行融合。

### 基础 DiT 视频生成模型

MagicMotion 以 CogVideoX-5B-I2V 和 Wan2.1 1.3B 作为基础图像到视频生成模型。两者均基于 DiT（Diffusion Transformer）架构，采用 3D-Full Attention 机制，负责从噪声潜在表示中逐步恢复出目标视频 $V \in \mathbb{R}^{T \times H \times W \times 3}$。基础模型在训练期间保持冻结，仅 Trajectory ControlNet 和 Segment Head 参与训练。

### Trajectory ControlNet

轨迹条件的注入采用类似 ControlNet 的设计。Trajectory ControlNet 由基础模型中所有预训练 DiT 块的可训练副本构成，其输出经零初始化卷积层处理后，逐层加回基础模型对应的 DiT 块输出中。零初始化卷积确保训练初期轨迹分支不干扰基础模型的生成能力，随后逐步学习将轨迹信息融入扩散去噪过程。

### Segment Head 与潜在分割损失

Segment Head 是一个轻量级分割头，接收来自 DiT 多层特征的拼接结果，直接在潜在空间预测分割掩膜 $Z_{segment}$。其监督信号来自真实掩膜轨迹经 3D VAE 编码后的潜在表示 $Z_{mask}$，损失函数为欧氏距离：

$$\mathcal{L}_{seg} = \mathbb{E}_{t, \epsilon \sim \mathcal{N}(0, I), z_0} \left[ \| Z_{segment} - Z_{mask} \|_2^2 \right]$$

### 损失函数

模型训练采用速度预测范式的扩散损失：

$$\mathcal{L}_{diffusion} = \mathbb{E}_{t, \epsilon \sim \mathcal{N}(0, I), x_0} \left[ \| x_0 - (\sqrt{\alpha_t} x_t - \sqrt{1-\alpha_t} v_\theta) \|_2^2 \right]$$

其中 $x_0$ 为原始视频，$x_t$ 为加噪后的视频，$v_\theta$ 为模型预测的速度场，$\alpha_t$ 为噪声调度参数。

总损失为扩散损失与潜在分割损失的加权组合：

$$\mathcal{L} = \mathcal{L}_{diffusion} + \lambda \cdot \mathcal{L}_{seg}$$

其中权重 $\lambda$ 在 Stage1（掩膜训练阶段）设为 0，在 Stage2（密集边界框）和 Stage3（稀疏边界框）设为 0.5。这一设计使得模型在稀疏轨迹训练阶段仍能通过潜在空间的分割监督保持对物体精细形状的感知能力，而在稠密掩膜阶段则完全依赖轨迹条件本身提供形状信息。

## 实验与关键发现

### 实验设置

MagicMotion 在自建的 **MagicData** 数据集上进行训练，该数据集通过自动标注流水线（Curation Pipeline + Filtering Pipeline）构建，将前景物体标注数量限制在 1 至 3 个，标注面积比约束在 0.008 至 0.83 之间，光流得分阈值设为 2.0。训练采用 AdamW 优化器，学习率 $1 \times 10^{-5}$，每 GPU batch size 为 1，在 4 块 NVIDIA A100-80G GPU 上完成。推理时默认使用 50 步去噪，引导尺度为 6，Trajectory ControlNet 权重为 1.0。

评估在两个基准上进行：自建的 **MagicBench**（按受控物体数量 1 至 5+ 分 6 组独立评估）和公开数据集 **DAVIS**。所有方法统一使用各视频的前 49 帧进行评估；对于不支持 49 帧生成的方法，均匀采样至其最大帧数。掩膜或边界框类方法直接使用标注框作为输入，点/光流类方法（如 Motion-I2V、ImageConductor 等）则使用掩膜中心点作为轨迹。评价指标包括 FID、FVD（视频质量）以及 Mask IoU、Box IoU（轨迹控制精度）。

### 主实验结果

在 MagicBench 基准上，MagicMotion 在所有四项指标上均大幅领先现有方法。以 Stage1-CogVideoX 版本为例，FID 达到 **15.06**，较 Tora 的 26.27 降低 11.21；FVD 达到 **112.69**，较 Tora 的 245.23 降低 132.54；Mask IoU 达到 **91.57%**，较 Tora 的 58.95% 提升 32.62 个百分点（Table 1）。在 DAVIS 数据集上，MagicMotion 同样表现优异：FID 为 45.06（Tora 为 51.75），Mask IoU 为 81.33%（Tora 仅为 37.98%），轨迹控制精度提升超过 43 个百分点。

按受控物体数量分组评估的结果（Figure 4, Table 5-7）显示，MagicMotion 在 1 至 5+ 个物体的各难度层级上均保持领先，尤其在多物体复杂场景下的优势更为显著，验证了渐进训练策略对复杂场景的泛化能力。定性对比（Figure 5）进一步表明，MagicMotion 能够使物体精准沿给定轨迹运动，而其他方法在轨迹跟踪和形状保持上均出现明显缺陷（如物体漂移、形状扭曲等）。

![[assets/figures/papers/paper_list_l2_MagicMotion_Controllable_Video_Generation_with_Dense_to_Sparse_Trajector/figures/015_Table_5.jpg]]
*Table 5: Quantitative Comparison results on MagicBench with moving objects number equals to 1 / 2*

![[assets/figures/papers/paper_list_l2_MagicMotion_Controllable_Video_Generation_with_Dense_to_Sparse_Trajector/figures/017_Table_6.jpg]]
*Table 6: Quantitative Comparison results on MagicBench with moving objects number equals to 3 / 4*

![[assets/figures/papers/paper_list_l2_MagicMotion_Controllable_Video_Generation_with_Dense_to_Sparse_Trajector/figures/018_Table_7.jpg]]
*Table 7: Quantitative Comparison results on MagicBench with moving objects number equals to 5 / above 5*

### 消融实验

消融实验围绕三个关键设计展开：MagicData 数据集、渐进训练策略（Progressive Training, PT）和潜在分割损失（Latent Segment Loss, LSL）。

**MagicData 数据集的影响**（Table 2, Figure 6）：使用 MagicData 训练相比使用 MeViS+MOSE 组合数据集，在 MagicBench 上 Mask IoU 提升约 3.22%，Box IoU 提升约 2.79%。定性结果显示，不使用 MagicData 时模型会生成意外冗余物体（如额外出现一个小孩），说明高质量带轨迹标注的视频数据对模型至关重要。

![[assets/figures/papers/paper_list_l2_MagicMotion_Controllable_Video_Generation_with_Dense_to_Sparse_Trajector/figures/008_Table_2.jpg]]
*Table 2: Ablation Study on MagicData. The model trained with MagicData outperforms the one trained without it across all metrics*

**渐进训练策略的影响**（Table 3, Figure 7）：移除渐进训练后，模型在 MagicBench 上的 Mask IoU 从 76.61% 降至 74.61%（下降 2.0 个百分点），DAVIS 上的 Mask IoU 从 53.94% 降至 49.22%（下降 4.72 个百分点）。定性结果表现为生成物体的形状明显扭曲，如头部变形、转身时出现第二张脸。

**潜在分割损失的影响**（Table 3, Figure 8）：移除 LSL 后，MagicBench 上的 Mask IoU 从 76.61% 降至 74.65%（下降 1.96 个百分点），DAVIS 上的 Mask IoU 从 53.94% 降至 49.19%（下降 4.75 个百分点）。定性结果显示物体形状感知能力下降，出现手臂残缺、口红变形为矩形等异常。值得注意的是，即使在仅提供稀疏边界框的条件下（Stage3），MagicMotion 仍能预测出合理的潜在分割掩膜（Figure 12），这解释了 LSL 在稀疏轨迹场景下对形状保持的关键作用。

### 应用扩展

除标准轨迹控制外，MagicMotion 还展示了相机运动控制（Figure 9）和视频编辑（Figure 10）等扩展应用。通过设置特定的轨迹条件，模型可实现可控的相机运动；结合 FLUX 编辑首帧图像后，Stage1 可驱动前景物体沿原始视频轨迹运动。同一输入图像配合不同轨迹条件（Figure 11）可生成多样化的运动视频，体现了方法的灵活性和泛化能力。

### 待验证问题

尽管 MagicMotion 在现有基准上表现优异，以下问题仍需进一步验证：在物体严重遮挡或快速运动场景下，稀疏框轨迹能否保持稳健的形状预测；MagicData 自动化标注流水线产生的标注噪声对最终性能的定量影响；该框架在实时或低延迟推理场景下的可行性。

![[assets/figures/papers/paper_list_l2_MagicMotion_Controllable_Video_Generation_with_Dense_to_Sparse_Trajector/figures/011_Table_4.jpg]]
*Table 4: Comparisons on each method’s backbone*

## 定位与知识库关联

### 轨迹可控视频生成的方法演进

轨迹可控视频生成旨在根据用户指定的运动路径驱动图像中的物体产生符合预期的运动，其核心挑战在于同时实现精准的运动控制与物体形状的一致性保持。现有方法按轨迹表示形式可划分为几个主要分支：

**基于光流的控制**：早期工作如 **Motion‑I2V** 和 **ImageConductor** 将光流作为运动引导信号，通过在扩散模型中注入密集的光流场来控制像素级运动。这类方法能提供细粒度的运动信息，但对光流估计的精度高度敏感，且在稀疏标注条件下难以泛化。

**基于点的拖拽式控制**：**DragAnything** 和 **DragNUWA** 等采用用户指定的稀疏点轨迹作为控制信号，通过特征拖拽或跨模态融合实现物体移动。这类方法的优势在于交互简便，但稀疏点提供的形状信息极为有限，导致物体在运动过程中容易出现形状扭曲或身份丢失。**LeViTor** 则引入3D关键点轨迹，试图通过三维几何约束增强控制精度。

**基于边界框的控制**：**SG‑I2V** 探索了无需训练的边界框引导方案，通过在推理阶段修改注意力图来实现物体位置控制；而 **Tora** 则采用基于轨迹导向的扩散Transformer架构，将边界框轨迹作为条件直接注入生成过程。然而，这些方法通常仅支持单一轨迹格式，在仅提供稀疏边界框（如少于10帧有标注）时，难以保持物体的精细形状。

### MagicMotion 的定位与突破

MagicMotion 在上述谱系中占据了一个独特位置：它首次通过统一的架构同时支持三种从稠密到稀疏的轨迹表示——分割掩膜、密集边界框和稀疏边界框。这一能力源于两个核心设计：

1. **渐进式稠密到稀疏训练策略**：模型分三阶段训练，Stage1使用完整的分割掩膜轨迹，Stage2过渡到密集边界框，Stage3仅在少于10帧上提供边界框标注。每阶段继承前阶段的权重，使模型能够从稠密标注中习得形状先验，并逐步迁移到稀疏条件。这种课程式学习策略与直接从稀疏条件训练（如Tora）形成根本差异——后者缺乏稠密信号的引导，在形状保持上存在天然劣势。

2. **潜在分割损失**：在Stage2和Stage3中，引入轻量级分割头从DiT多层特征预测潜在空间的分割掩膜，并以欧氏距离监督（$L = L_{diffusion} + \lambda \cdot L_{seg}$，$\lambda=0.5$）。这一设计使模型即使在仅接收稀疏边界框的条件下，仍能隐式地推断物体的完整形状掩膜，从而在潜在空间层面维持形状一致性。消融实验证实，移除该损失后，MagicBench上的Mask IoU下降1.96个百分点，DAVIS上下降4.75个百分点，且出现手臂残缺、口红变形为矩形等典型失败模式。

### 适用边界与局限

尽管MagicMotion在MagicBench和DAVIS上取得了显著优势，其适用边界仍需审慎界定：

- **数据依赖性**：模型性能高度依赖自建的MagicData数据集。消融实验表明，使用MeViS+MOSE组合数据集替代MagicData时，MagicBench上的Mask IoU下降约3.22%，且定性结果中出现意外生成额外物体（如多余小孩或手臂）的现象。这意味着MagicData的自动化标注流水线所产出的轨迹质量对模型至关重要，但其标注噪声的定量影响尚未被系统评估。

- **遮挡与快速运动**：论文未提供在严重遮挡或快速运动场景下的专门评测。在稀疏框条件下，模型虽能预测出合理的潜在分割掩膜（Figure 12），但当物体被大面积遮挡或运动幅度超出训练分布时，该预测机制的鲁棒性仍存疑。

- **轨迹表示的扩展性**：当前框架支持掩膜、边界框和稀疏框三种表示，但能否扩展到更抽象的轨迹形式（如关键点骨架、语义路径描述）尚未验证。

### 开放问题

1. 在物体严重遮挡或快速运动场景下，稀疏框轨迹是否能保持稳健的形状预测？潜在分割损失在这些极端条件下的行为尚未被刻画。

2. 渐进训练策略是否可推广到更多层级的轨迹表示，例如从骨架到边界框再到掩膜的多粒度课程？

3. MagicData自动化标注流水线引入的标注噪声（如SAM2的掩膜误差、跟踪漂移）对最终性能的定量影响如何？是否存在标注质量与模型性能之间的相变临界点？

4. 该框架能否与基于文本的轨迹描述（如“从左向右移动然后旋转”）相结合，实现更自然的混合模态交互？

5. 当前架构基于CogVideoX‑5B和Wan2.1 1.3B，推理需50步扩散采样，实时或低延迟应用场景下的可行性尚未探索。

## 原文 PDF

![[paperPDFs/ICCV_2025/MagicMotion_Controllable_Video_Generation_with_Dense_to_Sparse_Trajectory_Guidance.pdf]]
