---
title: "X-Portrait: Expressive Portrait Animation with Hierarchical Motion Attention"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/X_Portrait_Expressive_Portrait_Animation_with_Hierarchical_Motion_Attention.pdf
aliases:
- X-Portrait
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "采用隐式跨身份运动控制：直接从原始RGB驾驶帧学习身份解耦的运动信号，并结合局部补丁注意力模块增强微小表情传递。"
primary_logic: "利用预训练潜在扩散模型（SD1.5）作为生成骨干，通过跨身份ControlNet直接处理RGB图像作为运动条件，隐式学习身份无关运动表征，从而在保留身份特征的同时准确传递极端面部表情和大范围头部运动。"
claims:
- "X-Portrait 在自重建任务中达到最低 L1、最高 SSIM 和 LPIPS 以及最佳 FID。"
- "X-Portrait 在跨身份重演中取得最优身份相似度 (0.689)、图像质量 (67.569) 和最低表情/姿态误差 (0.070/3.37)。"
- "用户研究中 83.23% 的参与者在表情/姿态方面偏好 X-Portrait 优于 Face Vid2vid Plus。"
- "Ablation on Cross-Identity Training 上 ID Similarity↑ = 0.689 (full X-Portrait)"
---

# X-Portrait: Expressive Portrait Animation with Hierarchical Motion Attention

> [!tip] 核心洞察
> 利用预训练潜在扩散模型（SD1.5）作为生成骨干，通过跨身份ControlNet直接处理RGB图像作为运动条件，隐式学习身份无关运动表征，从而在保留身份特征的同时准确传递极端面部表情和大范围头部运动。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | X-Portrait：基于分层运动注意力的表现力肖像动画 |
| 英文题名 | X-Portrait: Expressive Portrait Animation with Hierarchical Motion Attention |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://arxiv.org/abs/2403.15931) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | X-Portrait |
| Dataset | Ablation on Cross-Identity Training, Ablation on Local Control Module, User Study (vs. Face Vid2vid Plus) |

> [!tip] 效果简介
> - Ablation on Cross-Identity Training 上，ID Similarity↑ 为 0.689 (full X-Portrait)，对比 0.015 (self-driven training)，变化 +0.674。
> - Ablation on Local Control Module 上，Expression/Pose Error↓ 为 0.070 / 3.37，对比 0.077 / 3.69 (w/o local control)，变化 Expression ↓9%, Pose ↓8.7%。
> - User Study (vs. Face Vid2vid Plus) 上，Expression/Pose Preference Rate 为 83.23%，对比 16.77%，变化 +66.46%。

## 概述

### 问题瓶颈

现有肖像动画方法普遍依赖显式运动表征——如2D/3D面部关键点或密集姿态图——作为运动控制信号。这种显式编码在压缩运动信息时不可避免地造成表达力损失：一方面，离散的关键点无法完整捕捉眼球转动、嘴角微颤等细微动态；另一方面，显式姿态图往往携带驾驶者的身份外观信息，导致生成结果出现严重的**外貌泄漏（appearance leakage）**——即参考肖像的身份特征被驾驶者外貌所侵蚀，表现为面部形状、五官比例向驾驶者漂移。这两个问题构成了领域长期存在的“运动保真度-身份一致性”权衡困境。

### 核心方法

X-Portrait 提出了一条根本不同的技术路径：**以隐式跨身份运动控制替代显式运动表征**。方法的关键在于两个相互耦合的设计决策：

1. **隐式运动编码**：不再从驾驶帧中提取关键点或姿态图，而是直接以原始RGB图像作为运动条件，输入到基于ControlNet的运动控制模块中。通过跨身份训练策略，该模块被强制学习从RGB信号中解耦出身份无关的纯粹运动表征——头部姿态与面部表情的动态信息被保留，而驾驶者的身份外观特征被抑制。

2. **分层运动注意力**：在全局运动控制的基础上，引入一个辅助ControlNet，专门作用于眼部、嘴部等局部区域的遮罩图像，增强模型对微小表情变化的注意力粒度。这使得单眼眨眼、撇嘴等精细动作得以被准确传递。

整个系统以冻结的预训练潜在扩散模型（Stable Diffusion 1.5）作为生成骨干，通过三个可训练模块——外观参考模块、运动控制模块、时序平滑模块——实现外观、运动、时间连贯性的解耦控制。

### 方法定位

在肖像动画的方法谱系中，X-Portrait 代表了一次从“显式运动建模”到“隐式运动学习”的范式转移。与基于3D关键点的 **Face Vid2Vid**（Wang et al., CVPR 2021）、基于深度感知的 **DaGAN**（Hong et al., CVPR 2022）、基于薄板样条的 **TPS**（Zhao and Zhang, CVPR 2022）等显式方法相比，X-Portrait 不依赖任何手工设计的运动中间表征。与同期基于扩散模型的 **FADM**（Zeng et al., CVPRW 2023）和 **MagicDance** 相比，X-Portrait 的差异化优势在于其跨身份训练机制和局部注意力设计，使其在身份保持和微表情传递两个维度上取得了突破性提升。

### 主要结果

定量实验（Table 1）表明，X-Portrait 在自重建任务中达到最低 L1 误差、最高 SSIM 和 LPIPS 以及最佳 FID；在跨身份重演任务中，身份相似度达到 0.689，图像质量得分 67.569，表情误差 0.070，姿态误差 3.37，全面超越所有基线方法。消融实验（Table 2）揭示了跨身份训练的决定性作用：若替换为自驱动训练，身份相似度从 0.689 骤降至 0.015，外貌泄漏极为严重。用户研究进一步验证了感知层面的优势——83.23% 的参与者在表情和姿态维度上偏好 X-Portrait 而非 Face Vid2vid Plus。

### 局限与展望

方法的主要局限在于：当预训练重演网络对极端表情（如嘴唇内翻、鼓腮）完全失效时，X-Portrait 的运动传递能力随之受限（Figure 5）；此外，模型目前不支持手势动画，且推理速度（24帧约30秒，A10 GPU）距离实时应用仍有差距。开放问题包括如何将手势纳入框架、如何消除偶发的时序抖动伪影、以及能否摆脱对预训练重演网络的依赖实现端到端训练。

## 背景与动机

肖像动画旨在从单张静态参考图像和一段驾驶视频中合成逼真且富有表现力的动态肖像。该技术在虚拟化身驱动、影视制作和远程通信等领域具有广泛应用前景。然而，现有方法在该任务上面临两个核心瓶颈：**运动表达力的损失**与**身份外貌的泄漏**。

当前主流方法普遍依赖显式运动表征作为中间桥梁。基于3D关键点的方法（如 **Face Vid2Vid**，Wang et al., CVPR 2021）和密集姿态图方法将面部动态压缩为稀疏或结构化的运动信号，再将其注入生成器。这种显式解耦虽然在概念上清晰，却不可避免地造成两方面损失：其一，稀疏关键点难以完整编码微表情（如单眼眨眼、撇嘴）和极端头部姿态的丰富动态信息，导致运动表达力不足；其二，显式运动表征在传递过程中容易将驾驶者的外貌特征（如脸型、五官比例）混入生成结果，造成严重的身份漂移——即所谓的外貌泄漏。

扩散模型在图像和视频生成领域展现出强大的先验能力，为肖像动画提供了新的可能。一些早期工作（如 **FADM**，Zeng et al., CVPRW 2023）尝试将扩散模型引入该任务，但仍沿用关键点或属性标签作为运动条件，未能从根本上突破显式表征的局限。核心矛盾在于：**如何在准确传递驾驶视频中全部运动信息的同时，严格保持参考图像的身份特征？**

X-Portrait 的动机正是针对这一矛盾提出隐式运动控制范式。该方法的核心洞察是：利用预训练潜在扩散模型（Stable Diffusion 1.5）作为生成骨干，通过跨身份 ControlNet 直接从原始 RGB 驾驶帧学习身份解耦的运动信号，从而绕开显式运动表征的信息瓶颈。同时，针对微表情等局部细微运动难以被全局注意力充分捕获的问题，引入基于局部补丁的辅助注意力机制加以增强。这一设计旨在实现运动表达力与身份保持之间的平衡——这是此前方法未能有效解决的关键缺口。

## 核心创新

### 问题瓶颈：显式运动表征的“外貌泄漏”与表达力损失

现有肖像动画方法普遍依赖显式运动表征作为驱动信号，例如 **Face Vid2Vid**（Wang et al., CVPR 2021）和 **DaGAN**（Hong et al., CVPR 2022）使用 3D 面部关键点或密集姿态图，**TPS**（Zhao and Zhang, CVPR 2022）则基于薄板样条变换。这类设计存在一个根本性缺陷：显式表征在提取过程中不可避免地丢失了微表情细节（如单眼眨眼、撇嘴等），同时将驱动者的身份信息（如脸型、五官比例）耦合进运动信号，导致生成结果出现严重的**外貌泄漏**——生成人物的面部特征向驱动者漂移，身份一致性被破坏。

X-Portrait 的核心洞察在于：**绕过显式运动表征，直接从原始 RGB 驾驶帧中隐式学习身份解耦的运动信号**，从而在保留参考肖像身份特征的同时，准确传递从细微表情到极端头部姿态的全部动态。

### 关键机制：跨身份隐式运动控制

X-Portrait 的方法创新围绕三个相互协同的 changed slots 展开：

**1. 运动控制输入：从显式关键点到隐式 RGB 控制图像**

X-Portrait 摒弃了传统的面部关键点或姿态图，转而使用一个预训练的肖像重演网络 $\mathcal{F}$（具体为 Face Vid2Vid Plus）生成跨身份控制图像 $I_C = \mathcal{F}(I_{S'}, I_D)$。其中 $I_{S'}$ 是与参考肖像不同身份的随机帧，$I_D$ 是驾驶帧。该控制图像 $I_C$ 作为条件输入到运动控制模块，其关键性质在于：它保留了 $I_D$ 的完整运动信息（头部姿态与面部表情），但面部纹理来自 $I_{S'}$，从而天然实现了身份与运动的解耦。

**2. 训练策略：从自驱动到跨身份训练**

传统方法采用自驱动训练（源帧与驾驶帧为同一身份），这使得模型学会直接从驾驶帧复制外貌特征。X-Portrait 的跨身份训练方案强制运动控制模块从 $I_C$ 中隐式推导身份无关的运动信号，而非依赖纹理线索。消融实验（Table 2）给出了决定性证据：当移除跨身份训练、退化为自驱动方案时，身份相似度从 **0.689 骤降至 0.015**，外貌泄漏极为严重。

**3. 局部运动注意力：增强微表情传递**

全局运动控制对大幅头部转动效果良好，但眼部、嘴部等局部区域的细微动态容易被忽略。X-Portrait 引入一个辅助 ControlNet，条件于仅暴露眼部和嘴部补丁的遮罩控制图像 $I_C^l$，引导模型将运动注意力聚焦于这些关键局部区域。消融实验（Table 2）表明，移除该模块后表情误差从 **0.070 升至 0.077**（↑9%），姿态误差从 **3.37 升至 3.69**（↑8.7%），验证了局部注意力对捕捉微表情的因果作用。

### 外貌泄漏的系统性抑制

上述创新共同构成了一条完整的因果链：跨身份训练切断身份信息从驾驶帧泄漏的路径，隐式 RGB 控制图像提供身份解耦的运动载体，局部控制模块确保微小表情不被全局运动淹没。此外，训练时对 $I_C$ 和 $I_C^l$ 施加随机异构缩放，进一步破坏可能残留的身份形状线索（Figure 3(c) 展示了缩放策略对脸型、眼部大小保持的改善）。

### 方法定位

X-Portrait 在肖像动画领域首次将**预训练潜在扩散模型（Stable Diffusion 1.5）**作为生成骨干，通过跨身份 ControlNet 实现隐式运动控制。与同期基于扩散的方法如 **FADM**（Zeng et al., CVPRW 2023）和 **MagicDance** 相比，X-Portrait 的独特优势在于完全不依赖任何显式运动表征，而是让模型从跨身份 RGB 图像对中自主学习运动与身份的分离——这一设计从根本上解决了外貌泄漏问题，同时释放了极端表情和大范围姿态的传递能力。

## 整体框架

![[assets/figures/papers/paper_list_l29_X_Portrait_Expressive_Portrait_Animation_with_Hierarchical_Motion_Attent/figures/002_Figure_2.jpg]]
*Figure 2: Overview of X-Portrait . For the task of portrait animation, X-Portrait leverages a frozen pre-trained LDM as a rendering backbone, and incorporates three auxiliary trainable modules for disentangled control of appearance ${ \mathcal { R } }$ , motion C and temporal smoothness M. Specifically, R extracts the source appearance and background context from a reference image $I _ { S }$ , and C derives the motion of head pose and facial expression from a driving frame $I _ { D }$ . During training, we leverage a pre-trained network $\mathcal { F }$ to generate cross-identity control images $I _ { C }$ as conditional input to our control modules C. To better capture subtle expressions, we enhance the atte...

X-Portrait 以冻结的预训练潜在扩散模型（Stable Diffusion 1.5）作为生成骨干，在此基础上引入三个可训练的辅助模块，分别负责外观控制、运动控制和时间平滑，实现对参考肖像的表现力动画生成。整体架构如 Figure 2 所示。

**外观参考模块 $\mathcal{R}$** 从源图像 $I_S$ 中提取身份特征和背景上下文信息。该模块通过自注意力交叉查询机制，将提取的外观特征注入主干 U‑Net，在生成过程中建立输入与输出之间的局部空间对应关系，从而保持身份一致性。

**跨身份运动控制模块 $\mathcal{C}$** 是框架的核心创新。与依赖显式面部关键点或密集姿态图的传统方法不同，该模块直接以 RGB 控制图像 $I_C$ 作为条件输入。$I_C$ 由预训练重演网络 $\mathcal{F}$（基于 **Face Vid2Vid**，Wang et al., CVPR 2021）生成：

$$I_C = \mathcal{F}(I_{S'}, I_D)$$

其中 $I_{S'}$ 是从不同身份视频中随机选取的源帧，$I_D$ 为驾驶帧。这种跨身份训练策略迫使控制模块隐式学习身份解耦的运动信号（头部姿态与面部表情），从根本上抑制了外貌泄漏问题。

**局部运动控制模块** 以辅助 ControlNet 的形式实现，条件于局部遮罩图像 $I_C^l$（仅暴露眼部与嘴部区域）。该模块将运动注意力细化到面部局部补丁，增强对眼球位置、唇形等微小表情动态的捕捉能力。

**时序模块 $\mathcal{M}$** 采用时序 Transformer 结构，保证生成帧间的时间连贯性。训练时，对 $I_C$ 和 $I_C^l$ 施加随机异构缩放，进一步减少驾驶图像的身份信息泄漏。

推理阶段，模型采用提示漫游策略增强时序平滑性，并利用潜在一致性模型加速去噪过程。不同于从随机噪声出发，推理时对源图像 $I_S$ 施加前向扩散过程获得初始化噪声，为生成提供结构引导。整个流程支持直接以原始驾驶视频帧作为输入，无需任何预处理步骤。

## 核心模块与公式推导

### 3.1 生成骨干：冻结的潜在扩散模型

X-Portrait 采用预训练的潜在扩散模型（SD1.5）作为冻结的渲染骨干，其训练目标为标准去噪损失：

$$L_{ldm} = \mathbb{E}_{z_0, t, \epsilon \sim N(0,1)} \left[ \| \epsilon - \epsilon_\theta(z_t, t) \|_2^2 \right]$$

其中 $z_0$ 为编码到潜在空间的真实图像，$z_t$ 为加噪后的潜在表示，$\epsilon_\theta$ 为去噪网络。在此冻结骨干之上，X-Portrait 引入三个可训练的辅助模块，分别负责外观、运动和时间维度的解耦控制（Figure 2）。

### 3.2 外观参考模块 $\mathcal{R}$

外观参考模块 $\mathcal{R}$ 从源参考图像 $I_S$ 中提取身份特征与背景上下文信息。该模块通过自注意力交叉查询机制，将源图像的外观特征注入主干 U-Net 的生成过程，建立输入与输出之间局部化的空间对应关系，从而在动画生成中严格保持身份一致性。

### 3.3 跨身份运动控制模块 $\mathcal{C}$

这是 X-Portrait 的核心创新。传统方法依赖显式运动表征（如面部关键点或密集姿态图），导致运动表达力损失和外貌泄漏。X-Portrait 的运动控制模块 $\mathcal{C}$ 直接以 RGB 图像作为条件输入，隐式学习身份解耦的运动信号。

训练时，利用预训练的肖像重演网络 $\mathcal{F}$（基于 **Face Vid2Vid**，Wang et al., CVPR 2021）生成跨身份控制图像：

$$I_C = \mathcal{F}(I_{S'}, I_D)$$

其中 $I_{S'}$ 是从另一身份视频中随机选取的帧，$I_D$ 为驾驶帧。该跨身份训练方案迫使控制模块 $\mathcal{C}$ 从 $I_C$ 中隐式推导出与身份无关的头部姿态与面部表情运动，从而在推理时可直接以任意驾驶视频的 RGB 帧作为条件输入，无需任何预处理。

### 3.4 局部运动控制模块（辅助 ControlNet）

为增强对细微面部运动的捕捉能力，X-Portrait 引入一个辅助 ControlNet，条件于局部遮罩图像 $I_C^l$。$I_C^l$ 仅保留 $I_C$ 中眼部与嘴部周围的局部补丁区域，引导运动注意力集中于这些关键部位。消融实验（Table 2）表明，移除该模块后表情误差从 0.070 上升至 0.077（↑9%），姿态误差从 3.37 上升至 3.69（↑8.7%），验证了局部注意力对微表情传递的关键作用。

### 3.5 随机异构缩放策略

为抑制跨身份训练中驾驶图像外貌向生成结果的泄漏，X-Portrait 对 $I_C$ 和 $I_C^l$ 施加随机异构缩放增强。该策略通过破坏控制图像与目标图像之间的精确空间对齐，迫使模型从缩放不变的运动线索中学习，而非依赖外貌纹理匹配。消融实验（Figure 3(c)、Table 2）证实，该策略显著改善了身份保持效果——移除后身份相似度从 0.689 骤降至 0.015。

### 3.6 时序模块 $\mathcal{M}$

时序模块 $\mathcal{M}$ 采用时序 Transformer 架构，对连续帧间的潜在表示进行建模，保证生成视频的时间连贯性。推理阶段进一步结合提示漫游（prompt traveling）策略与潜在一致性模型（LCM）加速采样，24 帧生成约需 30 秒（A10 GPU）。

## 实验与分析

### 主实验结果

X-Portrait 在自重建（self reenactment）和跨身份重演（cross reenactment）两项任务上均全面超越现有方法。Table 1 报告了 256×256 分辨率下的定量对比：

![[assets/figures/papers/paper_list_l29_X_Portrait_Expressive_Portrait_Animation_with_Hierarchical_Motion_Attent/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons of X-Portrait with SOTA baselines in self and cross reenactment tasks, evaluated on an image resolution of 256 × 256*

**自重建任务**衡量模型在源身份与驾驶身份相同时的保真度。X-Portrait 在全部四项指标上取得最优：L1 误差 0.033、SSIM 0.829、LPIPS 0.133、FID 14.553。这表明模型能够以极高的精度重建源图像的外观细节和结构信息。

**跨身份重演任务**是评估的核心——将驾驶视频的运动迁移到不同身份的源肖像上。X-Portrait 的身份相似度（ID Similarity）达到 0.689，图像质量（Image Quality）达到 67.569，均显著优于所有基线。表情误差仅 0.070，姿态误差仅 3.37，均为最低值。相比之下，基于 GAN 的方法（如 **Face Vid2Vid** (Wang et al., CVPR 2021)、**DaGAN** (Hong et al., CVPR 2022)）在身份保持和运动精度之间存在明显的权衡，而 X-Portrait 的隐式运动控制机制有效打破了这个瓶颈。

**用户研究**进一步验证了感知层面的优势。在盲测对比中，83.23% 的参与者在表情和姿态传递方面偏好 X-Portrait 而非 **Face Vid2vid Plus**（Supplementary Section C）。这一压倒性偏好率说明模型在真实用户感知中的表现力远超竞争方法。

### 消融实验

Table 2 和 Figure 3 系统拆解了三个关键设计的作用：

![[assets/figures/papers/paper_list_l29_X_Portrait_Expressive_Portrait_Animation_with_Hierarchical_Motion_Attent/figures/007_Table_2.jpg]]
*Table 2: Quantitative ablation*

**跨身份训练（Cross-Identity Training）** 是身份保持的基石。当移除跨身份训练、退化为自驱动训练（即用同一身份的地面真值驾驶帧作为运动条件）时，身份相似度从 0.689 骤降至 0.015——模型几乎完全丧失了身份保持能力，出现严重的外貌泄漏（Figure 3a）。这一消融直接验证了核心因果机制：仅靠缩放增强无法阻止模型从驾驶帧中复制身份特征，必须通过跨身份图像对强制模型学习身份解耦的运动表征。

**局部运动控制模块（Local Motion Control）** 对微表情传递至关重要。移除该辅助 ControlNet 后，表情误差从 0.070 上升至 0.077（相对增加 10%），姿态误差从 3.37 上升至 3.69（相对增加 9.5%）。Figure 3b 的视觉对比显示，没有局部注意力引导时，眼部眨眼、嘴角微动等细微动态会丢失或失真。该模块通过仅在眼部、嘴部局部遮罩图像 $I_C^l$ 上施加条件，有效增强了模型对这些关键区域的注意力。

**随机异构缩放（Random Heterogeneous Scaling）** 是抑制外貌泄漏的辅助机制。在跨身份训练基础上加入该策略后，身份保持得到进一步改善（Figure 3c），尤其是在头型、眼距等几何特征上减少了驾驶身份的漂移。缩放策略通过对控制图像 $I_C$ 和 $I_C^l$ 施加随机的非均匀缩放变换，破坏了驾驶帧中残留的身份几何线索。

### 失败模式与局限

Figure 5 展示了 X-Portrait 的典型失败案例。当预训练重演网络 $\mathcal{F}$（即 **Face Vid2vid Plus**）完全无法为特定极端表情生成相关运动线索时——例如嘴唇内翻（turning lips inwards）或鼓腮（puffing cheeks）——模型的表情传递能力受到根本性限制。这是因为训练数据中的控制图像 $I_C$ 本身就缺乏这些表情的有效表征，ControlNet 无法从中学习到对应的运动模式。

此外，模型目前存在以下已知局限：
- **手势动画缺失**：框架仅处理面部区域，无法传递手势信息。
- **时序抖动伪影**：尽管时序模块 $\mathcal{M}$ 和提示漫游策略提升了连贯性，偶尔仍会出现轻微的帧间抖动。
- **推理速度**：借助潜在一致性模型（LCM）加速后，生成 24 帧仍需约 30 秒（A10 GPU），距离实时应用仍有差距。

### 关键图表结论

- **Table 1**：X-Portrait 在自重建和跨身份重演两个维度均取得 SOTA 性能，验证了隐式运动控制范式在身份保持和运动精度上的双重优势。
- **Table 2**：跨身份训练是身份保持的决定性因素（ID Similarity 从 0.015 到 0.689），局部控制模块和随机缩放分别贡献了微表情精度和外貌泄漏抑制的增量收益。
- **Figure 3**：视觉消融直观展示了外貌泄漏（a）、局部细节丢失（b）和身份漂移（c）的退化模式，与定量结果高度一致。
- **Figure 5**：失败案例揭示了当前方法对预训练重演网络 $\mathcal{F}$ 的依赖性——这是系统性能的上限瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l29_X_Portrait_Expressive_Portrait_Animation_with_Hierarchical_Motion_Attent/figures/010_Figure.jpg]]
*Figure: (a)*

![[assets/figures/papers/paper_list_l29_X_Portrait_Expressive_Portrait_Animation_with_Hierarchical_Motion_Attent/figures/011_Figure_1.jpg]]
*Figure 1: (a) is the result of X-Portrait with a single reference image from (b), while (c) with both reference images. X-Portrait seamlessly accommodates multiple images as reference, producing animations with better captured personalized appearance traits in (c). Please find the differences in hair, ear and face shape. Figure 2: User study example. A and B represent synthesized outputs from different methods*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

X-Portrait 的核心突破在于用**隐式跨身份运动控制**替代了传统肖像动画中依赖显式运动表征的范式。这一转变使其在方法谱系中处于从“结构化运动解耦”向“数据驱动隐式解耦”演进的关键节点。

**早期基于关键点/密集姿态的方法**构成了该领域的第一代基线。**Face Vid2Vid**（Wang et al., CVPR 2021）通过3D面部关键点驱动GAN生成，但其运动表达受限于关键点的稀疏性，难以捕捉眨眼、撇嘴等微表情。**DaGAN**（Hong et al., CVPR 2022）引入深度感知来增强姿态估计，**TPS**（Zhao and Zhang, CVPR 2022）使用薄板样条进行空间变形，**MCNet**（Hong and Xu, ICCV 2023）则尝试用记忆补偿网络改善时序一致性。这些方法的共同瓶颈在于：显式运动表征（2D/3D关键点或密集姿态图）本身就是一种有损压缩，必然导致细微表情信息的丢失；更致命的是，当驾驶帧与源肖像身份不同时，这种显式表征会携带驾驶者的外貌特征，造成严重的**外貌泄漏（appearance leakage）**——即生成结果的五官形状、脸型等身份特征向驾驶者漂移。

**基于扩散模型的方法**代表了第二代尝试。**FADM**（Zeng et al., CVPRW 2023）将扩散模型引入肖像动画，但仍依赖属性引导（attribute-guided）的显式条件。**MagicDance**将扩散模型扩展到人物动画，但同样未从根本上解决身份与运动的解耦问题。这些方法虽然利用了扩散模型的生成先验，却未充分发挥其从原始RGB信号中隐式学习解耦表征的潜力。

X-Portrait 的关键差异在于**三个架构创新**：第一，它直接用原始RGB驾驶帧作为运动条件，通过跨身份ControlNet隐式学习身份无关的运动信号，跳过了显式关键点提取这一信息瓶颈；第二，引入**局部补丁注意力模块**（auxiliary ControlNet），在眼部、嘴部等关键区域施加细粒度运动引导，解决了全局条件难以捕捉微表情的难题；第三，采用**跨身份训练策略**，利用预训练重演网络 $\mathcal{F}$（即Face Vid2vid Plus）生成交叉身份的控制图像 $I_C = \mathcal{F}(I_{S'}, I_D)$，强制模型学习身份解耦的运动表征。消融实验（Table 2）给出了最直接的证据：当跨身份训练被替换为自驱动训练时，身份相似度从0.689骤降至0.015，说明模型几乎完全依赖驾驶帧的身份信息来生成结果，而非从参考图像提取身份特征。

### 2. 适用边界与局限

X-Portrait 的有效性高度依赖于其训练管线中的两个外部组件：预训练重演网络 $\mathcal{F}$ 和潜在扩散模型（SD1.5）。这定义了其能力边界和失效模式。

**对 $\mathcal{F}$ 的依赖是首要瓶颈。** 如 Figure 5 所示，当 $\mathcal{F}$ 完全无法为极端表情（如嘴唇内翻、鼓腮）生成任何相关的运动线索时，X-Portrait 的表情传递能力受限。这意味着模型的上限被 $\mathcal{F}$ 的能力所约束——如果 $\mathcal{F}$ 在特定姿势或表情下退化，训练数据质量随之下降，进而影响模型性能。这是一个结构性的局限：X-Portrait 并未从第一性原理学习运动表征，而是蒸馏了 $\mathcal{F}$ 的运动知识。

**手势动画的缺失**是另一个明确的能力边界。当前框架仅处理面部区域，无法传递手部动作，这限制了其在全身人物动画场景中的应用。

**时序一致性**方面，虽然模型引入了时序Transformer模块（$\mathcal{M}$）和推理时的提示漫游（prompt traveling）策略，但生成结果偶尔仍出现轻微的抖动伪影（jittering artifacts）。这表明当前的时序建模尚不足以完全消除帧间不连贯。

**推理效率**是实际部署的障碍。即使借助潜在一致性模型（LCM）加速，生成24帧仍需约30秒（A10 GPU），远未达到实时应用的要求。

### 3. 开放问题

X-Portrait 揭示的方法论方向——利用扩散模型从RGB信号中隐式学习身份解耦的运动表征——提出了几个值得追踪的开放问题：

1. **端到端的跨身份运动学习**：当前框架依赖预训练网络 $\mathcal{F}$ 生成控制图像，这引入了外部依赖和数据质量瓶颈。能否设计一种无需 $\mathcal{F}$ 的端到端训练方案，直接从原始视频对中学习身份解耦的运动表征？这可能涉及对比学习或解耦变分自编码器的思想。

2. **手势与面部的联合动画**：将手势动画纳入框架需要处理更大的空间范围和更复杂的运动模式。这不仅是增加一个控制模块的问题，还涉及如何在不引入额外外貌泄漏的前提下，同时解耦面部身份、面部运动、手部身份和手部运动。

3. **时序伪影的根本消除**：当前的抖动伪影表明，简单的时序Transformer可能不足以建模长程时空一致性。结合先进的时空注意力机制（如video diffusion model中的3D attention）或显式的光流约束，可能是消除这一问题的方向。

4. **高分辨率下的身份保持**：现有评估均在256×256分辨率下进行。在512×512或更高分辨率下，身份保持和运动精度的变化趋势尚不明确——更高分辨率可能暴露当前方法在细节纹理保持方面的不足，也可能为微表情传递提供更精细的空间。

5. **跨风格泛化的理论理解**：X-Portrait 在写实照片、素描、动漫等多种风格间展现出良好的泛化能力（Figure 4），但其内在机制尚缺乏理论解释。理解扩散先验如何在不同视觉域之间建立运动对应关系，可能为通用人物动画提供更坚实的方法论基础。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/X_Portrait_Expressive_Portrait_Animation_with_Hierarchical_Motion_Attention.pdf]]
