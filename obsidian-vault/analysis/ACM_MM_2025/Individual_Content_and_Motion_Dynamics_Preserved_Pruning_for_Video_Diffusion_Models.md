---
title: "Individual Content and Motion Dynamics Preserved Pruning for Video Diffusion Models"
type: paper
paper_level: A
venue: "ACM MM"
year: 2025
pdf_ref: paperPDFs/ACM_MM_2025/Individual_Content_and_Motion_Dynamics_Preserved_Pruning_for_Video_Diffusion_Models.pdf
aliases:
- VICMDPP
- ICMDPPVDM
tags:
- ACM_MM_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过FVD分析和视觉观察评估每个U-Net块的重要性，剪枝贡献较小的浅层块，保留关键深层块，同时使用个体内容蒸馏损失和多帧内容对抗损失来恢复微调后的生成质量。"
primary_logic: "深层对于运动动态至关重要，浅层对于个体内容更重要；针对性地保留深层、剪枝浅层能在几乎不损失视频质量的情况下显著减少模型参数和推理时间。"
claims:
- "替换深层块（如D.2、U.1）会导致FVD显著升高，表明这些块对运动动态至关重要。"
- "剪枝后的VDMini-I2V在FVD上接近于教师SF-V（198.13 vs 166.26），且延迟从512ms降至345ms（2.5×加速）。"
- "结合ICD和MCA损失进行再训练，将FVD从无ICMD时的~290降至198.13，验证了ICMD损失的有效性。"
- "移除D.2和U.1块导致生成的视频运动变得微弱，证实这些层对运动动态的关键作用。"
---

# Individual Content and Motion Dynamics Preserved Pruning for Video Diffusion Models

> [!tip] 核心洞察
> 深层对于运动动态至关重要，浅层对于个体内容更重要；针对性地保留深层、剪枝浅层能在几乎不损失视频质量的情况下显著减少模型参数和推理时间。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 个体内容与运动动态保持的视频扩散模型剪枝 |
| 英文题名 | Individual Content and Motion Dynamics Preserved Pruning for Video Diffusion Models |
| 会议/期刊 | ACM MM 2025 |
| Links | [paper](https://arxiv.org/abs/2411.18375) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VDMini (Individual Content and Motion Dynamics Preserved Pruning) |
| Dataset | UCF101 (I2V), UCF |

> [!tip] 效果简介
> - UCF101 (I2V) 上，FVD ↓ 为 198.13，对比 166.26，变化 +31.87 (FVD increase)。
> - 在 I2V 推理上，延迟从 512ms 降至 345ms，实现 2.5× 加速；ICMD 损失将 FVD 从约 290 降至 198.13。

## 概述

视频扩散模型（VDM）在生成高质量视频方面取得了显著进展，但其庞大的模型规模和极高的推理延迟严重制约了实际部署。现有加速方法（如一致性蒸馏、少步采样）虽能降低采样步数，却未触及模型结构本身的冗余。本文揭示了一个关键瓶颈：**U-Net 的不同层对视频生成的贡献存在本质差异——深层（低分辨率块）对多帧运动动态至关重要，而浅层（高分辨率块）主要贡献于单帧内容质量。** 直接进行无差别剪枝极易破坏运动一致性，导致生成视频出现微弱的运动或时序闪烁。

基于这一发现，作者提出了 **VDMini**，一种面向视频扩散模型的个体内容与运动动态保持剪枝框架。其核心调控逻辑是：通过 FVD 指标和视觉分析评估每个 U-Net 块的重要性，**系统性地剪枝贡献较小的浅层块，同时保留对运动动态关键的深层块**（如 D.2 和 U.1）。为恢复剪枝后的生成质量，VDMini 引入了 **ICMD 一致性损失**，包含用于单帧内容蒸馏的 ICD 损失和用于多帧运动保持的 MCA 对抗损失。

在方法谱系上，VDMini 属于**结构化剪枝 + 知识蒸馏**的混合压缩范式。与通用剪枝方法（如 DepGraph, Fang et al., CVPR 2023）和幅度剪枝不同，VDMini 的剪枝策略由视频特有的“内容-运动”解耦分析驱动，而非单纯依赖参数重要性或依赖图。其教师模型为原始未剪枝的 VDM（如 SF-V, Zhang et al., NeurIPS 2024；T2V-Turbo-v2；HunyuanVideo），学生模型为剪枝后的轻量级 U-Net。

实验表明，VDMini 在 I2V 任务上实现了 **2.5 倍加速**（SF-V 延迟从 512ms 降至 345ms），FVD 从 166.26 变为 198.13，性能接近教师模型；在 T2V 任务上分别实现了 1.4 倍（T2V-Turbo-v2）和 1.25 倍（HunyuanVideo）加速。消融实验证实，ICMD 损失将剪枝后模型的 FVD 从约 290 降至 198.13，验证了其有效性。

## 背景与动机

视频扩散模型（Video Diffusion Models, VDMs）在图像到视频（I2V）和文本到视频（T2V）生成任务上取得了显著进展，但其推理过程需要庞大的计算资源，严重阻碍了实际部署。核心瓶颈在于：VDM的U-Net骨干网络层数深、参数多，导致单次推理延迟高，而现有模型压缩方法（如结构化剪枝**DepGraph** (Fang et al., CVPR 2023) 或权重幅度剪枝）直接套用到VDM时，往往无法保持视频特有的运动一致性，生成质量下降明显。

本文的关键观察是：VDM中不同深度的层对生成质量的贡献存在本质差异。深层（如U-Net的DownBlock.2、UpBlock.1）对多帧运动动态至关重要——实验表明，替换这些深层块会导致FVD（Fréchet Video Distance）显著升高，且生成的视频运动变得微弱（Figure 1(a), Figure A6）。相反，浅层主要负责单帧的个体内容生成，对运动一致性的贡献相对有限。这一发现揭示了一个直接的剪枝策略：**保留对运动动态关键的深层，剪枝贡献冗余的浅层**，从而在参数和延迟大幅降低的前提下，尽可能维持视频生成质量。

然而，仅靠结构性剪枝仍会导致微调后的生成质量下降。为此，本文提出**个体内容与运动动态一致性损失（ICMD Loss）**，包含两个互补组件：**个体内容蒸馏损失（ICD Loss）**用于对齐学生模型与教师模型在单帧层面的中间特征，保持逐帧内容质量；**多帧内容对抗损失（MCA Loss）**则通过时空判别器（SpatioHead和TemporalHead）在对抗训练中保持跨帧运动一致性。两者协同，使剪枝后的轻量模型VDMini在I2V任务上实现2.5倍加速（延迟从512ms降至345ms），FVD仅从166.26小幅升至198.13，逼近教师模型SF-V（Zhang et al., NeurIPS 2024）的水平。

## 核心创新

VDMini 的核心创新在于**首次揭示了视频扩散模型中深层与浅层 U-Net 块在功能上的分工差异**，并据此设计了一套“保留深层、剪枝浅层”的结构化剪枝策略，配合专门设计的 **ICMD 一致性损失（Individual Content and Motion Dynamics Consistency Loss）** 进行微调恢复。

### 关键洞察：深层管运动，浅层管内容

通过对 SF-V 模型各 U-Net 块进行移除/替换实验并测量 FVD 变化（Figure 1(a)），作者发现了一个清晰的规律：
- **浅层块（高分辨率层）** 被移除时 FVD 上升幅度相对较小，表明其主要贡献于单帧的个体内容生成。
- **深层块（低分辨率层，尤其是 D.2 和 U.1）** 被移除时 FVD 显著飙升，且生成的视频运动变得微弱甚至消失（Figure A6），证实这些块对多帧运动动态至关重要。

这一发现直接驱动了剪枝决策：**剪掉冗余的浅层块，保留关键的深层块**。具体而言，VDMini 在 DownBlocks 和 UpBlocks 中剪除第二个 ResBlock-Attention 对，但**刻意保留 D.2 和 U.1 这两个深层块**，同时完全移除 MidBlock（Section 3.2, Table A4）。

### 剪枝后微调：ICMD 一致性损失

直接剪枝会导致生成质量下降，但仅靠原始任务损失（如重建损失 + 对抗损失）进行微调，FVD 仍高达约 290（Table 4）。VDMini 提出了 **ICMD 一致性损失**，由两部分组成：

1. **个体内容蒸馏损失（ICD Loss）**：在教师 U-Net 和学生 U-Net 的多个中间层之间计算 L2 距离，强制剪枝后模型在**逐帧内容**上与原始模型对齐。
2. **多帧内容对抗损失（MCA Loss）**：引入一个包含 SpatioHead 和 TemporalHead 的判别器，以对抗方式让学生模型生成的视频在多帧运动动态上逼近教师模型，从而**保持运动一致性**。

消融实验（Table 4）表明，单独使用 ICD 或 MCA 均能改善 FVD，但**两者联合使用（即完整的 ICMD 损失）才能将 FVD 从约 290 降至 198.13**，接近教师模型 SF-V 的 166.26。

### 辅助加速：VAE 解码器压缩

除了 U-Net 剪枝，VDMini 还对 VAE 解码器进行了层级剪枝和通道剪枝（移除 MidBlock 和 UpBlock.3，压缩通道数），将解码器参数量从 63.58M 降至 39.17M，延迟从 2832ms 降至 840.5ms（Appendix A, Table A1），在几乎不损失重建质量的前提下进一步加速整体推理。

## 整体框架

![[assets/figures/papers/paper_list_l12_Individual_Content_and_Motion_Dynamics_Preserved_Pruning_for_Video_Diffu/figures/002_Figure_2.jpg]]
*Figure 2: The proposed VDMini framework for Video Di usion Model Compression. Left: The retraining process with the proposed ICMD loss, where $\mathcal { L } _ { I C D }$ is the knowledge distillation loss for individual content consistency, and ${ \mathcal { L } } _ { M C A }$ is the adversarial loss for multi-frame content consistency. $\mathcal { L } _ { T a s k }$ is the task-specific loss function adopted in the base model. Right: The teacher model is pruned by blocks to obtain the student model (i.e.,VDMini). The second Block (ResBlock, AttentionBlock) in the DownBlock and UpBlock are removed (Except for the second last DownBlock and UpBlock), and the innermost Blocks (MidBlock, DownBlock, and UpBlock...

VDMini 的整体框架围绕“结构剪枝 + 蒸馏微调”两阶段范式构建，目标是在保持视频生成质量的前提下，显著压缩视频扩散模型（VDM）的推理延迟与参数规模。

**核心管线** 由以下模块串联构成：

1. **条件编码**：输入图像或文本提示经由 CLIP Encoder 编码为条件特征，注入后续去噪过程。
2. **VAE 编码**：输入视频帧通过 VAE Encoder 压缩至潜在空间，得到潜在表示 $x_t$。
3. **学生 U-Net 去噪**：剪枝后的轻量级 Student U-Net（即 VDMini 骨干）接收噪声潜在 $x_t$、时间步 $t$ 及条件特征，执行单步/少步去噪预测。其结构由原始 Teacher U-Net 经块级剪枝得到：移除浅层 DownBlocks 和 UpBlocks 中的冗余 ResBlock-Attention 对，同时删去 MidBlock 及部分深层低分辨率块（详见 Table A4）。
4. **压缩 VAE 解码**：去噪后的潜在表示输入 Compressed VAE Decoder，通过层剪枝（移除 MidBlock 和 UpBlock.3）与通道剪枝联合压缩，将潜在噪声重建为视频帧输出。

**微调阶段的训练流** 引入 ICMD 一致性损失，在教师-学生框架下进行知识迁移：

- **ICD Loss Module**：逐帧计算 Student U-Net 与 Teacher U-Net 中间层特征之间的 L2 距离，强制学生模型保留单帧内容质量。
- **MCA Discriminator**：包含 SpatioHead 和 TemporalHead 的判别器，对教师和学生生成的多帧特征进行对抗判别，以保持跨帧运动动态。学生 U-Net 同时接收 MCA 生成器损失和原始任务损失（如 SF-V 的重建+对抗损失，或 T2V-Turbo-v2 的一致性损失）进行联合优化。

整体而言，VDMini 通过“浅层剪枝 + 深层保留”的非对称压缩策略降低骨干网络计算量，再借助 ICD 蒸馏与 MCA 对抗损失恢复剪枝带来的内容与运动质量损失，最终在 I2V 和 T2V 任务上分别实现 2.5× 和 1.4× 的推理加速（Figure 2 给出了框架总览）。

## 核心模块与公式推导

### 核心模块

**1. 剪枝后的 Student U-Net (VDMini)**
基于块重要性分析（Figure 1），对教师 U-Net 进行结构性剪枝：浅层（高分辨率）的冗余块被移除，深层（低分辨率）的关键块被保留。具体而言，DownBlocks 和 UpBlocks 中除 D.2 和 U.1 外的第二个 ResBlock-Attention 对被剪枝，MidBlock 被完全移除（Section 3.2, Table A4）。这一设计的因果逻辑在于：深层块对多帧运动动态至关重要，浅层块主要贡献于个体帧内容，剪枝浅层可在几乎不损失运动质量的前提下大幅降低参数量与推理时间。

**2. 压缩 VAE Decoder**
原始 VAE Decoder 推理开销极大（63.58M 参数，解码 14×72×128 的视频隐变量需 2832ms）。VDMini 对其同时施加层剪枝与通道剪枝：移除 MidBlock 和 UpBlock.3，并压缩通道数，得到 39.17M 参数的轻量解码器，延迟降至 840.5ms（Appendix A, Table A1, Figure A1）。该模块独立于 U-Net 剪枝，进一步加速端到端推理。

**3. ICD 损失模块**
ICD（Individual Content Distillation）损失在微调阶段对齐学生 U-Net 与教师 U-Net 的中间层特征，逐帧蒸馏个体内容信息。其核心机制是最小化两个模型在对应层上的特征距离，确保剪枝后单帧生成质量不退化。

**4. MCA 判别器**
MCA（Multi-frame Content Adversarial）损失引入一个包含 SpatioHead 和 TemporalHead 的判别器（Figure 2），对学生生成的多帧内容施加对抗训练。生成器试图欺骗判别器，判别器则区分学生与教师的输出，从而在对抗博弈中保持跨帧运动动态的一致性。

### 关键公式推导

**ICD 损失（Individual Content Distillation Loss）**

$$\mathcal{L}_{ICD} = \mathbb{E}\left[\sum_{l=1}^{L} d\left(f_{l}^{stu}(\boldsymbol{x}_{t}, t), f_{l}^{tea}(\boldsymbol{x}_{t}, t)\right)\right]$$

其中：
- $\boldsymbol{x}_{t}$ 为扩散时间步 $t$ 的噪声输入；
- $f_{l}^{stu}$、$f_{l}^{tea}$ 分别为学生和教师 U-Net 在第 $l$ 层的中间特征；
- $d(\cdot,\cdot)$ 为距离度量（实际采用 L2 距离）；
- $L$ 为用于蒸馏的总层数。

该损失直接约束学生模型在特征空间上逼近教师模型，逐帧保持内容质量。

**MCA 生成器损失（Multi-frame Content Adversarial Generator Loss）**

$$\mathcal{L}_{MCA}^{gen} = -\mathbb{E}\left[\log D_{\phi}\left(f^{stu}(x_{t}, t), \sigma_{t'}\right)\right]$$

**MCA 判别器损失（Hinge Loss 形式）**

$$\mathcal{L}_{MCA}^{disc} = \mathbb{E}\left[\max(0, 1 + D_{\phi}(f^{stu}(x_{t}), \sigma_{t'}))\right] + \mathbb{E}\left[\max(0, 1 - D_{\phi}(f^{tea}(x_{t}, t), \sigma_{t'}))\right]$$

其中：
- $D_{\phi}$ 为 MCA 判别器，以 U-Net 输出特征和噪声水平 $\sigma_{t'}$ 作为输入；
- $f^{stu}$、$f^{tea}$ 分别为学生和教师 U-Net 的最终输出特征；
- 判别器采用 hinge loss，增强训练稳定性。

MCA 损失通过对抗训练迫使学生的多帧输出在运动模式上与教师不可区分，从而弥补剪枝造成的运动动态损失。

**整体微调目标**

$$\mathcal{L}_{total} = \mathcal{L}_{Task} + \lambda_{ICD} \cdot \mathcal{L}_{ICD} + \lambda_{MCA} \cdot (\mathcal{L}_{MCA}^{gen} + \mathcal{L}_{MCA}^{disc})$$

其中 $\mathcal{L}_{Task}$ 为原始任务损失（I2V 为重建+对抗损失，T2V 为一致性损失），$\lambda_{ICD}$ 和 $\lambda_{MCA}$ 为平衡超参数（典型设置 $\lambda_{ICD}=0.1$，$\lambda_{MCA}=1$，见 Table 5）。该组合损失在保留任务目标的同时，通过蒸馏和对抗两个维度恢复剪枝后的生成质量。

## 实验与分析

### 核心性能验证

VDMini的核心目标是在保持视频生成质量的前提下，显著降低推理延迟。实验在I2V和T2V两大任务、多个骨干模型上验证了该方法的有效性。

**I2V任务**：以**SF-V**（Zhang et al., NeurIPS 2024）为教师模型，VDMini-I2V在UCF101数据集上取得了FVD=198.13，与教师模型（FVD=166.26）差距可控（Table 2）。更重要的是，模型参数从SF-V的约2.5B压缩至约1.5B（~40%参数减少），推理延迟从512ms降至345ms，实现了**2.5倍加速**。与25步**SVD**（Blattmann et al., 2023）相比，VDMini-I2V在相近FVD下实现了约37倍加速。在VBench-I2V的主观一致性指标上，VDMini-I2V达到97.51%，与教师模型基本持平（Table 1）。

![[assets/figures/papers/paper_list_l12_Individual_Content_and_Motion_Dynamics_Preserved_Pruning_for_Video_Diffu/figures/003_Table_1.jpg]]
*Table 1: Evaluation of VDMini-I2V on the VBench-I2V dataset. In this table, we compare the performance of the unpruned model SF-V and VDMini-I2V with and without the motion consistency loss ${ \mathcal { L } } _ { M C A }$ . The metrics are divided into two categories: I2V subject and background consistency, and motion smoothness, dynamic degree, aesthetic quality, and imaging quality. The results show that VDMini-I2V achieves comparable performance to SF-V while being more e cient*

![[assets/figures/papers/paper_list_l12_Individual_Content_and_Motion_Dynamics_Preserved_Pruning_for_Video_Diffu/figures/004_Table_2.jpg]]
*Table 2: Comparison with the existing methods. VDMini-I2V achieves a comparable FVD score with SF-V and 16-step SVD*

**T2V任务**：在**T2V-Turbo-v2**上，VDMini-T2V将推理延迟从2554ms降至1662ms，加速1.4倍；在DiT架构的**HunyuanVideo**上，VDMini-T2V-HY实现1.25倍加速，VBench-T2V总分仅从83.24微降至82.42（0.82%性能损失，Table 6）。

![[assets/figures/papers/paper_list_l12_Individual_Content_and_Motion_Dynamics_Preserved_Pruning_for_Video_Diffu/figures/007_Table_6.jpg]]
*Table 6: Comparison of VDMini-T2V with other methods on VBench-T2V in terms of Quality Score, Semantic Score, Total Score, and Latency*

### 剪枝策略对比

Table 3将VDMini的剪枝策略与两种通用剪枝基线进行了对比：**DepGraph**（Fang et al., CVPR 2023）和**Magnitude Pruning**。在相同参数压缩比下，DepGraph和Magnitude Pruning的FVD分别严重退化至~350和~400以上，而VDMini保持FVD=198.13。这表明，基于U-Net深层/浅层功能差异的针对性剪枝远优于不考虑视频时空特性的通用剪枝方法。

![[assets/figures/papers/paper_list_l12_Individual_Content_and_Motion_Dynamics_Preserved_Pruning_for_Video_Diffu/figures/005_Table_3.jpg]]
*Table 3: Comparison with other baseline pruning approaches. DepGraph [18] explicitly models the dependency between layers and comprehensively groups coupled parameters for pruning, while Magnitude Pruning aims to remove the smallest magnitude weights in the network. L2 and Taylor are the criteria for importance estimation*

### 损失函数消融

Table 4的消融实验揭示了ICMD损失各组分的关键作用：
- **无ICMD损失**（仅任务损失微调）：FVD约290，视频质量严重退化。
- **仅ICD损失**（个体内容蒸馏）：FVD降至约230，验证了逐帧特征对齐对内容恢复的有效性。
- **仅MCA损失**（多帧内容对抗）：FVD约250，说明对抗训练对运动动态保持有独立贡献。
- **ICD + MCA联合**：FVD进一步降至198.13，证明两者互补——ICD恢复单帧质量，MCA保持跨帧运动一致性。

![[assets/figures/papers/paper_list_l12_Individual_Content_and_Motion_Dynamics_Preserved_Pruning_for_Video_Diffu/figures/008_Table_4.jpg]]
*Table 4: E ectiveness of the ICMD Loss. We conduct ablation studies to validate the e ectiveness of the ICMD loss used during the finetuning stage. As shown in Table 4, enabling $\mathcal { L } _ { I C D }$ and ${ \mathcal { L } } _ { M C A }$ individually results in FVD scores of 224.24 and 257.99, respectively. When both $\mathcal { L } _ { I C D }$ and ${ \mathcal { L } } _ { M C A }$ are combined, the FVD score improves significantly to 198.13. These results highlight the substantial contribution of the ICMD loss to the overall performance of the model

Table 5的超参数敏感性分析显示，λ_ICD=0.1、λ_MCA=1时FVD最优；偏差过大会导致内容失真或运动模糊。

### 关键架构决策的验证

Figure 1(a)的块重要性分析是剪枝决策的实证基础：移除或替换深层块（如D.2、U.1）导致FVD急剧升高，而浅层块（如D.0、U.3）的影响相对较小。这直接支撑了“保留深层、剪枝浅层”的核心策略。Figure A6进一步通过可视化证实：移除D.2和U.1块后，生成视频的运动幅度显著减弱，验证了这些层对运动动态的关键作用。

![[assets/figures/papers/paper_list_l12_Individual_Content_and_Motion_Dynamics_Preserved_Pruning_for_Video_Diffu/figures/001_Figure_1.jpg]]
*Figure 1: (a) FVD score by removing or replacing the blocks in the U-Net. (Note that a high FVD score means the block is more important.) (b) Time and Parameters of the blocks in the U-Net*

![[assets/figures/papers/paper_list_l12_Individual_Content_and_Motion_Dynamics_Preserved_Pruning_for_Video_Diffu/figures/016_Figure.jpg]]
*Figure: A4: Block-wise FVD score by removing or replacing the blocks in the U-Net. Figure A5: Block-wise inference time and parameter count in the U-Net. Figure A6: Visual analysis of the pruned SF-V*

VAE解码器的压缩（附录Table A1）将解码器参数从63.58M降至39.17M，延迟从2832ms降至840.5ms，而图像质量指标（PSNR/SSIM）几乎无损（Table A2），说明VAE解码器存在显著冗余。

![[assets/figures/papers/paper_list_l12_Individual_Content_and_Motion_Dynamics_Preserved_Pruning_for_Video_Diffu/figures/013_Table.jpg]]
*Table: A1: Comparison of the model architecture and inference latency between SF-V and our proposed VDMini-I2V. Table A2: Quantitative comparison of the image quality metrics on the UCF101 dataset between the original VAE decoder and the compressed VAE decoder*

### 失败模式与局限

尽管VDMini在多数场景下表现良好，但分析中仍存在若干需注意的边界：
- **FVD差距**：VDMini-I2V与教师SF-V之间仍有约32的FVD差距（198.13 vs 166.26），在需要极高运动精度的场景下可能显现质量退化。
- **架构依赖性**：剪枝策略基于U-Net的深层/浅层功能差异假设，对DiT架构的HunyuanVideo加速比仅为1.25倍，说明该方法在非U-Net架构上的收益有限。
- **超参数敏感性**：λ_ICD和λ_MCA需针对不同教师模型调整，缺乏自动化调参机制。

### 补充图表

![[assets/figures/papers/paper_list_l12_Individual_Content_and_Motion_Dynamics_Preserved_Pruning_for_Video_Diffu/figures/014_Table.jpg]]

![[assets/figures/papers/paper_list_l12_Individual_Content_and_Motion_Dynamics_Preserved_Pruning_for_Video_Diffu/figures/015_Table.jpg]]
*Table: A3: Comparison of the model architecture and inference latency between T2V-Turbo-v2 and our proposed VDMini-T2V*

![[assets/figures/papers/paper_list_l12_Individual_Content_and_Motion_Dynamics_Preserved_Pruning_for_Video_Diffu/figures/017_Table.jpg]]
*Table: A4: The detailed architecture of the compressed U-Net used in VDMini*

## 方法谱系与知识库定位

### 与现有剪枝范式的差异

VDMini 的核心策略是**层级重要性感知的结构化剪枝**，这与通用剪枝方法存在本质区别。

- **DepGraph** (Fang et al., CVPR 2023) 通过显式建模层间依赖关系，将耦合参数分组后进行结构化剪枝，其目标是通用的网络压缩，不区分不同深度层对视频生成质量贡献的差异。实验表明，在相同参数削减量下，DepGraph 在 UCF101 上的 FVD 显著高于 VDMini-I2V（Table 3），原因在于它可能无差别地移除了对运动动态至关重要的深层块。
- **Magnitude Pruning** 基于权重幅值进行非结构化剪枝，完全不考虑视频扩散模型中深层与浅层的功能分化，其 FVD 退化更为严重（Table 3），验证了“一刀切”式剪枝在视频生成任务中的不适用性。

VDMini 的关键突破在于通过 FVD 分析和视觉观察（Figure 1(a), Figure A6）建立了因果认知：**深层块（如 D.2、U.1）对多帧运动动态至关重要，浅层块对个体帧内容贡献更大**。基于此，剪枝策略有选择地移除浅层冗余块，保留深层关键块，从而在参数削减与运动一致性之间取得平衡。

### 与快速采样方法的互补定位

VDMini 的加速路径与减少采样步数的方法（如一致性模型、渐进式蒸馏）正交。Table 2 显示，VDMini-I2V 基于 1-step SF-V 教师模型，在保持可比 FVD（198.13 vs 166.26）的同时将延迟从 512ms 降至 345ms（2.5× 加速）。相较于 SVD 的 25 步采样（延迟 12728ms，FVD 242.02），VDMini-I2V 实现了约 37× 的端到端加速。这表明 VDMini 可与少步推理方法叠加，进一步压缩推理成本。

### ICMD 损失的定位

ICMD 损失由两个组件构成：**Individual Content Distillation (ICD) Loss** 和 **Multi-frame Content Adversarial (MCA) Loss**。

- **ICD Loss** 属于特征蒸馏范式，最小化学生与教师 U-Net 中间层特征之间的 L2 距离（Equation 4），逐帧保持个体内容质量。
- **MCA Loss** 引入包含 SpatioHead 和 TemporalHead 的判别器（Figure 2），以对抗训练方式保持多帧运动动态（Equation 5-6）。这与传统的视频判别器不同之处在于，它直接作用于扩散模型的中间特征，而非最终生成的视频帧，从而更高效地引导剪枝后模型的运动一致性恢复。

消融实验（Table 4）证实了二者的协同效应：单独使用 ICD Loss 或 MCA Loss 时 FVD 约 230–250，联合使用后 FVD 降至 198.13，验证了“个体内容蒸馏 + 多帧对抗”组合对恢复剪枝后生成质量的有效性。

### 适用边界与局限

**适用边界**：

- **架构范围**：已验证于基于 U-Net 的 I2V 模型（SF-V, Zhang et al., NeurIPS 2024）和 T2V 模型（T2V-Turbo-v2），以及基于 DiT 的 T2V 模型（HunyuanVideo）。在 HunyuanVideo 上仅实现 1.25× 加速且 VBench-T2V 总分下降 0.82%（Table 6），表明该方法对 DiT 架构的加速收益有限，深层/浅层功能分化的假设可能需要针对不同骨干网络重新验证。
- **任务范围**：当前验证限于 I2V 和 T2V 任务，尚未在更复杂的视频编辑、视频预测等任务上进行测试。
- **压缩粒度**：剪枝以 U-Net 块为单位（如 ResBlock + TransformerBlock 对），属于粗粒度结构化剪枝。更细粒度的通道剪枝仅在 VAE Decoder 上应用（Appendix A, Figure A1）。

**局限与开放问题**：

- **深层保护策略的泛化性**：论文未提供在不同视频扩散模型上自动识别“关键深层块”的系统方法。当前依赖 FVD 分析和视觉观察的手动评估（Figure 1, Figure A6），对于新模型架构需要重复该流程，成本较高。
- **运动复杂场景的边界**：Table 1 显示 VDMini-I2V 在 VBench-I2V 的 Motion Smoothness 指标上为 97.51%，与教师 SF-V 接近，但缺乏在快速运动、遮挡、场景切换等极端条件下的详细分析。
- **VAE Decoder 压缩的独立验证**：VAE Decoder 的压缩（移除 MidBlock 和 UpBlock.3，通道剪枝）将解码延迟从 2832ms 降至 840.5ms（Table A1），但该模块的压缩策略与 U-Net 剪枝策略的交互效应未被消融——无法区分端到端加速中二者的各自贡献。
- **训练成本**：ICMD 损失需要教师模型参与前向传播以提供中间特征和判别器目标，微调阶段的计算开销未被量化报告。对于大规模 DiT 模型，这一开销可能显著。

## 原文 PDF

![[paperPDFs/ACM_MM_2025/Individual_Content_and_Motion_Dynamics_Preserved_Pruning_for_Video_Diffusion_Models.pdf]]
