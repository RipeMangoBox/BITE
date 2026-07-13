---
title: "FlashLips: 100-FPS Mask-Free Latent Lip-Sync using Reconstruction Instead of Diffusion or GANs"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FlashLips_100_FPS_Mask_Free_Latent_Lip_Sync_using_Reconstruction_Instead_of_Diffusion_or_GANs.pdf
project_link: null
code_link: null
aliases:
- FlashLips
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将唇形同步解耦为紧凑的低维唇部姿势控制向量与单步确定性重建：用纯重建损失取代GAN/扩散，并用自监督去除推理时的显式掩码依赖。
primary_logic: 对于唇形同步这类高度条件化的任务，一个低维解耦的唇部姿势表示配合自细化重建损失，足以在单步前馈中实现高保真实时编辑，无需任何对抗训练或扩散过程。
claims:
- U-Net 变体在单张 NVIDIA H100 GPU 上实现超过 100 FPS 的推理速度，且在唇形同步准确性和视觉质量上达到甚至超越更大、更慢的基线模型。
- 在重建和交叉音频两种协议下，FlashLips 的 FID、FVD、LipScore 等关键指标均达到最优或次优，同时推理速度远超扩散类方法（例如比 KeySync 快 30.4 倍）。
- 嘴唇编码器消融证实 12 维向量（8D 冻结表情编码器 + 4D 口部残差）在重建质量与身份解耦之间取得最佳折衷。
- Reconstruction (HDTF, CelebV-HQ, CelebV-Text) 上 FID↓ = 4.43 (Transformer) / 4.75 (U-Net)
---

# FlashLips: 100-FPS Mask-Free Latent Lip-Sync using Reconstruction Instead of Diffusion or GANs

> [!tip] 核心洞察
> 对于唇形同步这类高度条件化的任务，一个低维解耦的唇部姿势表示配合自细化重建损失，足以在单步前馈中实现高保真实时编辑，无需任何对抗训练或扩散过程。

| 字段 | 内容 |
|------|------|
| 中文题名 | FlashLips：基于重建的100-FPS无掩码唇形同步 |
| 英文题名 | FlashLips: 100-FPS Mask-Free Latent Lip-Sync using Reconstruction Instead of Diffusion or GANs |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zinonos_FlashLips_100-FPS_Mask-Free_Latent_Lip-Sync_using_Reconstruction_Instead_of_Diffusion_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | FlashLips |
| Dataset | Reconstruction, Inference Speed |

> [!tip] 效果简介
> - Reconstruction (HDTF, CelebV-HQ, CelebV-Text) 上，FID↓ 4.43 (Transformer) / 4.75 (U-Net) vs 5.30 (LatentSync) (−0.87 / −0.55)；FVD↓ 12.31 (Transformer) / 15.20 (U-Net) vs 36.47 (LatentSync) (−24.16 / −21.27)；LipScore↑ 0.71 (Transformer) vs 0.55 (LatentSync) (+0.16)。
> - Inference Speed (same clip, 5 warm-up + 10 runs) 上，FPS↑ 109.41 (U-Net) vs 3.60 (KeySync) (≈30.4×)。

## 概要

唇形同步（lip-sync）旨在根据任意音频驱动人脸视频中的嘴唇运动，使其与语音内容高度吻合。现有方法普遍依赖**迭代生成（扩散模型）或对抗训练（GAN）**，导致推理成本高昂、训练不稳定，并需借助显式嘴唇掩码等复杂预处理，严重阻碍实时部署。**FlashLips** 针对这一瓶颈，提出了一种基于**纯重建损失的单步确定性编辑**框架，将唇形同步解耦为两个阶段：首先学习一个紧凑的**低维唇部姿势控制向量**，然后通过单步前馈网络在 VAE 潜在空间中完成高保真编辑，全程无需掩码、无需扩散或对抗训练。

核心结论包括：
- **实时推理**：U-Net 变体在单张 NVIDIA H100 GPU 上达到 **>100 FPS**，比基于扩散的 KeySync 快约 30.4 倍（Table 2）。
- **视觉质量与同步精度**：在重建和交叉音频两种协议下，FlashLips 的 FID（4.43/4.75）、FVD（12.31/15.20）、LipScore（0.71）等关键指标均达到最优或次优，匹配甚至超越更大、更慢的基线模型（Table 1, Figure 2）。
- **简约控制空间**：仅 12 维唇部姿势向量（8D 冻结表情编码器 + 4D 口部残差）即可在重建质量与身份解耦之间取得最佳折衷（Table 5）。

方法上，FlashLips 将唇形同步重新定义为**图像重建任务**而非生成任务：Stage 1（LipsChange）通过掩码重建与自细化伪对训练，实现无掩码的单步潜在空间编辑；Stage 2 则利用流匹配从音频预测唇部姿势向量，驱动 Stage 1 完成同步。这一设计在方法谱系中位于**确定性重建路线**，与 DiffDub（Liu et al., ICASSP 2024）、LatentSync 等扩散范式，以及 Wav2Lip（Prajwal et al., ACM MM 2020）等 GAN 范式形成鲜明对比。



### 唇形同步任务的实时化困境

唇形同步旨在根据任意音频驱动生成与语音内容精确对齐的人脸视频，是数字人、虚拟主播、影视配音等应用的核心技术。近年来，该领域的主导范式经历了从生成对抗网络（GAN）到扩散模型的快速迭代，代表性工作包括 **Wav2Lip**（Prajwal et al., ACM MM 2020）的专家判别器策略、**LatentSync** 的潜在空间扩散、**KeySync** 的关键帧插值扩散，以及 **SayAnything** 的条件视频扩散等。

然而，这些方法共享一个结构性瓶颈：**它们都依赖多步迭代生成或对抗训练**。扩散模型需要数十甚至上百步去噪推理，GAN 则面临训练不稳定与模式坍塌风险。这一范式选择直接导致三个连锁问题：

1. **推理成本高昂**：扩散类方法的单帧生成时间远超实时要求，例如 KeySync 在 NVIDIA H100 上的实测速度仅为 3.60 FPS，远低于 25 FPS 的实时阈值。
2. **预处理复杂**：多数方法在推理时需要显式的嘴唇区域掩码（mask）作为输入引导，这要求额外的人脸解析或分割步骤，进一步增加了管线延迟与工程复杂度。
3. **训练-推理不一致**：掩码依赖意味着训练与推理之间存在预处理差异，可能引入域偏移，影响实际部署的稳定性。

### 核心洞察：高度条件化任务的重建充分性

FlashLips 的作者提出了一个关键认知转变：**唇形同步本质上是一个高度条件化的局部编辑任务，而非开放式生成任务**。给定源人脸图像和音频信号，需要修改的仅仅是嘴唇区域的像素，其余身份、背景、光照等信息应当原样保留。

这一洞察引出了一个被现有方法普遍忽视的可能性：**一个低维解耦的唇部姿势表示，配合精心设计的重建损失，是否足以在单步前馈中完成高保真编辑？** 如果可以，那么扩散模型的迭代采样和 GAN 的对抗训练就并非必要——它们引入的计算开销和训练复杂度是可以被绕过的。

### 本文动机与设计哲学

基于上述分析，FlashLips 的设计围绕三个核心原则展开：

- **用重建取代生成**：以纯重建损失（L1、VGG 感知损失、身份保持损失）驱动编辑网络，完全摒弃 GAN 判别器与扩散去噪过程，实现单步确定性推理。
- **用自监督去除掩码**：通过自细化（self-refinement）伪对训练，让网络自主学习编辑定位能力，消除推理时对显式嘴唇掩码的依赖。
- **用解耦控制压缩搜索空间**：将唇形同步解耦为“控制什么”（低维唇部姿势向量）与“如何渲染”（单步潜在空间编辑器），使音频到唇形的映射成为一个紧凑的流匹配问题，而非高维图像生成问题。

这一设计哲学的直接产物是：FlashLips 的 U-Net 变体在单张 NVIDIA H100 上实现了 **109.41 FPS** 的推理速度——约为 KeySync 的 30.4 倍——同时在唇形同步准确性与视觉质量上达到甚至超越更大、更慢的基线模型（见 Table 1 和 Table 2）。



## 核心方法与创新机理

FlashLips 的核心创新可归结为三个相互耦合的“变更槽”（changed slots），它们共同将唇形同步从多步生成范式推向单步确定性编辑，从而在实时性、训练稳定性与部署简洁性上实现代际跨越。

### 1. 生成范式：从多步迭代到单步重建

现有主流方法普遍依赖**扩散模型**（如 **DiffDub** (Liu et al., ICASSP 2024)、**Diff2Lip** (Mukhopadhyay et al., WACV 2024)、**LatentSync**、**KeySync**）或 **GAN**（如 **Wav2Lip** (Prajwal et al., ACM MM 2020)）进行多步迭代生成或对抗训练。这带来了两个根本性瓶颈：扩散模型需要数十步去噪推理，GAN 训练则面临模式坍塌与判别器-生成器博弈的不稳定性。

FlashLips 将唇形同步重新定义为**纯重建损失驱动的单步确定性编辑**。其 Stage 1 编辑器（LipsChange）在 VAE 潜在空间中执行一次前馈即可完成唇部修改，训练过程仅使用 L1、VGG 感知损失及人脸身份保持损失的加权组合：

$$\mathcal{L}_{\mathrm{total}} = 0.1 \mathcal{L}_{L1}^{lat} + 0.1 \mathcal{L}_{L1_m}^{lat} + 10 \mathcal{L}_{L1_M}^{pix} + 100 \mathcal{L}_{L1_{\mathrm{lips}}}^{pix} + 50 \mathcal{L}_{VGG} + 5 \mathcal{L}_{VGG}^{face}$$

这一设计直接消除了对抗训练和扩散过程，使推理速度达到 109.41 FPS（U-Net 变体，NVIDIA H100），较 KeySync 快约 30.4 倍，较 TalkLip 快 6.5 倍（Table 2）。与此同时，在 FID、FVD、LipScore 等关键指标上，FlashLips 的 Transformer 变体以 FID 4.43、FVD 12.31 达到最优，显著优于更大的扩散基线 LatentSync（FID 5.30, FVD 36.47）（Table 1）。

### 2. 控制信号：低维解耦的唇部姿势向量

传统方法通常从音频端到端直接生成图像或视频帧，控制信号与像素空间高度纠缠，导致编辑的可控性与泛化性受限。FlashLips 引入了一个**紧凑的 12 维唇部姿势向量**作为中间控制表示，将问题解耦为两个阶段：

- **Stage 1**：从唇部姿势向量到图像的确定性编辑；
- **Stage 2**：从音频到唇部姿势向量的流匹配预测。

唇部姿势向量由两部分构成（Figure 4）：冻结的表情编码器经 MLP 投影产生的 8 维向量（V1），以及口部裁剪 CNN 提取的 4 维残差（V2）。消融实验证实，8 维 V1 已接近重建质量饱和，添加 V2 虽进一步提升重建但会降低交叉音频场景下的身份保留度（ID）；12 维配置（8D V1 + 4D V2）在质量与解耦之间取得最佳折衷（Table 5）。

Stage 2 使用基于 wav2vec 2.0 特征的 Transformer，以流匹配目标从音频预测该低维向量：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{t, \epsilon, a} \left\| v_{\theta}(\mathbf{z}_t, t, \mathbf{c}) - \mathbf{u} \right\|_2^2$$

其中 $\mathbf{z}_t = (1 - t) \mathbf{\epsilon} + t \mathbf{z}_{\mathrm{lips}}$ 在噪声与目标唇部向量之间线性插值。这种低维中间表示使得音频到唇部运动的映射学习更加高效，同时为推理时替换控制源（如文本或手势驱动）保留了扩展空间。

### 3. 掩码依赖：自细化伪对训练实现无掩码推理

以 Wav2Lip 为代表的早期方法在推理时需要显式的嘴唇掩码预处理来限定编辑区域，这不仅增加了计算开销，还引入了掩码精度敏感性和边缘伪影风险。FlashLips 通过**自细化（self-refinement）**机制彻底消除了这一依赖。

具体而言，Stage 1 先以掩码重建方式训练基础编辑器（输入为掩码源潜在变量、投影参考潜在变量与唇部姿势向量的通道拼接 $\mathbf{z}_{\mathrm{input}} = \mathrm{Concat}\left[ \mathbf{z}_{\mathrm{masked}}, \overline{\mathbf{z}}_{\mathrm{ref}}, \mathbf{z}_{\mathrm{lips\ expanded}} \right]$，监督目标为原始源潜在变量与掩码源潜在变量的残差 $\mathbf{z}_{\mathrm{target}} = \mathbf{z}_{\mathrm{src}} - \mathbf{z}_{\mathrm{masked}}$）。随后，用该模型在训练数据上生成“伪对”（pseudo-pairs），再以这些伪对微调网络，使其学会在不依赖外部掩码的情况下自行定位唇部编辑区域。这一设计使推理流程完全掩码无关，大幅简化了部署管线。

### 4. 身份保留：多参考帧投影机制

FlashLips 的身份保留策略不同于常见的全局特征条件注入，而是采用**投影参考潜在变量 + 多参考帧动态选择**。消融实验表明，将参考帧数量从 1 增加到 4 可显著提升身份保留度（ID），同时对唇形同步度影响极小（Table 3, Table 4）。这为在保持编辑精度的前提下灵活权衡身份一致性提供了可控的调节旋钮。

**证据强度评估**：上述三项核心创新的有效性均得到定量消融与主实验的强支撑（置信度 0.95–0.98）。需注意，自细化机制在训练数据覆盖不足的边缘案例（如严重遮挡、极端头部旋转）上可能产生伪影，该点属于论文已声明的局限性，需在实际部署中进一步验证。



FlashLips 将唇形同步任务解耦为一个**两阶段级联框架**：Stage 1 在 VAE 潜在空间中完成单步确定性嘴唇编辑，Stage 2 从音频预测低维唇部姿势向量以驱动 Stage 1。两阶段独立训练、推理时串联，全程无需显式嘴唇掩码。

### 数据流与模块关系

整个 pipeline 的输入输出流如 **Figure 3** 所示，核心逻辑可概括为：

![[assets/figures/papers/paper_list_l2487_https_openaccess_thecvf_com_content_CVPR2026_html_Zinonos_FlashLips_100/figures/003_Figure_3.jpg]]
*Figure 3: Overview of FlashLips. Stage 1 trains a one-step latent-space editor: first via masked reconstruction, then via a mask-free self-refinement step that learns to localize edits without segmentation. Stage 2 trains an audio-to-lips model that predicts the lips-pose vector used in Stage 1. At inference, predicted lip poses drive the LipsChange network to produce lip-synced frames in a single pass*

1. **嘴唇姿势提取**：给定源人脸图像，Lips Encoder（**Figure 4**）提取一个紧凑的 12 维唇部姿势向量 $\mathbf{z}_{\text{lips}}$（8 维冻结表情编码器 + 4 维口部 CNN 残差），该向量解耦地编码了嘴唇的形状与开合状态。

2. **音频到姿势预测**（Stage 2）：一个基于 wav2vec 2.0 特征的 Transformer 以流匹配（flow matching）目标训练，从输入语音片段预测目标唇部姿势向量。流匹配在噪声与目标向量之间线性插值 $\mathbf{z}_t = (1 - t) \boldsymbol{\epsilon} + t \mathbf{z}_{\text{lips}}$，使模型学习速度场 $v_\theta$，损失为：
   $$\mathcal{L}_{\text{FM}} = \mathbb{E}_{t, \epsilon, a} \left\| v_{\theta}(\mathbf{z}_t, t, \mathbf{c}) - \mathbf{u} \right\|_2^2$$

3. **潜在空间编辑**（Stage 1, LipsChange）：将掩码后的源潜在变量 $\mathbf{z}_{\text{masked}}$、投影参考潜在变量 $\overline{\mathbf{z}}_{\text{ref}}$ 以及空间扩展的唇部姿势向量在通道维度拼接：
   $$\mathbf{z}_{\text{input}} = \text{Concat}\left[ \mathbf{z}_{\text{masked}}, \overline{\mathbf{z}}_{\text{ref}}, \mathbf{z}_{\text{lips expanded}} \right]$$
   网络预测目标残差 $\hat{\mathbf{z}}_{\text{target}}$，监督信号为真实残差 $\mathbf{z}_{\text{target}} = \mathbf{z}_{\text{src}} - \mathbf{z}_{\text{masked}}$，最终重建源潜在变量：
   $$\hat{\mathbf{z}}_{\text{src}} = \mathbf{z}_{\text{masked}} + \hat{\mathbf{z}}_{\text{target}}$$

4. **自细化无掩码推理**：Stage 1 首先在带掩码的重建任务上预训练，随后用自身生成的伪对（pseudo-pairs）进行自细化微调，使模型学会在无显式掩码的条件下将编辑自动限制在嘴唇区域。推理时直接输入完整图像，无需任何分割预处理。

### 训练范式与损失设计

Stage 1 完全摒弃 GAN 的对抗训练和扩散模型的迭代去噪，仅使用加权重建损失进行单步确定性编辑。总损失由六项组成：
$$\mathcal{L}_{\text{total}} = 0.1 \mathcal{L}_{L1}^{\text{lat}} + 0.1 \mathcal{L}_{L1_m}^{\text{lat}} + 10 \mathcal{L}_{L1_M}^{\text{pix}} + 100 \mathcal{L}_{L1_{\text{lips}}}^{\text{pix}} + 50 \mathcal{L}_{\text{VGG}} + 5 \mathcal{L}_{\text{VGG}}^{\text{face}}$$
其中 $\mathcal{L}_{L1}^{\text{lat}}$ 和 $\mathcal{L}_{L1_m}^{\text{lat}}$ 作用于潜在空间，$\mathcal{L}_{L1_M}^{\text{pix}}$ 和 $\mathcal{L}_{L1_{\text{lips}}}^{\text{pix}}$ 分别约束下脸部和嘴唇区域的像素级重建，VGG 感知损失与人脸身份保持损失则保障视觉质量和身份一致性。

### 身份保留机制

与基线方法通过参考帧或全局特征条件注入身份信息不同，FlashLips 采用**投影参考潜在变量 + 多参考帧动态选择**策略。消融实验（**Table 3, Table 4**）证实，将参考帧数量从 1 增加到 4 可显著提升身份保留度（ID），而对唇形同步度影响极小。



FlashLips 将唇形同步解耦为两个顺序阶段：**Stage 1 潜在空间编辑器 (LipsChange)** 与 **Stage 2 音频到唇部姿势 Transformer**。核心设计理念是用低维解耦的唇部姿势向量替代端到端的像素生成，使 Stage 1 成为纯重建驱动的单步确定性编辑，彻底摒弃 GAN 和扩散过程。

### Stage 1：单步潜在空间编辑器

Stage 1 在预训练 VAE 的潜在空间中工作，分两个子阶段训练。

**子阶段一：掩码重建。** 给定源帧潜在变量 $\mathbf{z}_{\mathrm{src}}$，首先用嘴唇掩码将其部分遮盖得到 $\mathbf{z}_{\mathrm{masked}}$。网络的输入为通道维度的拼接：

$$\mathbf{z}_{\mathrm{input}} = \mathrm{Concat}\left[ \mathbf{z}_{\mathrm{masked}}, \overline{\mathbf{z}}_{\mathrm{ref}}, \mathbf{z}_{\mathrm{lips\ expanded}} \right] \tag{1}$$

其中 $\overline{\mathbf{z}}_{\mathrm{ref}}$ 是从参考帧提取并投影的参考潜在变量（用于身份保留），$\mathbf{z}_{\mathrm{lips\ expanded}}$ 是空间扩展后的唇部姿势向量（用于驱动嘴唇运动）。监督目标是原始源潜在变量与掩码潜在变量的残差：

$$\mathbf{z}_{\mathrm{target}} = \mathbf{z}_{\mathrm{src}} - \mathbf{z}_{\mathrm{masked}} \tag{2}$$

网络预测残差 $\hat{\mathbf{z}}_{\mathrm{target}}$，最终重建的源潜在变量为：

$$\hat{\mathbf{z}}_{\mathrm{src}} = \mathbf{z}_{\mathrm{masked}} + \hat{\mathbf{z}}_{\mathrm{target}} \tag{3}$$

**子阶段二：自细化无掩码编辑。** 掩码重建模型虽然能修改嘴唇，但推理时仍需显式嘴唇掩码。为解决此问题，FlashLips 用已训练的重建模型生成自监督伪对：将掩码重建输出作为“伪目标”，原始帧作为“伪源”，在无掩码条件下微调网络。这让模型学会自动定位编辑区域，实现推理时完全无掩码。

**损失函数。** Stage 1 的总损失为六项加权求和：

$$\mathcal{L}_{\mathrm{total}} = 0.1 \mathcal{L}_{L1}^{lat} + 0.1 \mathcal{L}_{L1_m}^{lat} + 10 \mathcal{L}_{L1_M}^{pix} + 100 \mathcal{L}_{L1_{\mathrm{lips}}}^{pix} + 50 \mathcal{L}_{VGG} + 5 \mathcal{L}_{VGG}^{face} \tag{9}$$

各项含义：$\mathcal{L}_{L1}^{lat}$ 为潜在空间 L1 损失，$\mathcal{L}_{L1_m}^{lat}$ 为掩码区域潜在空间 L1 损失，$\mathcal{L}_{L1_M}^{pix}$ 为下半脸像素 L1 损失，$\mathcal{L}_{L1_{\mathrm{lips}}}^{pix}$ 为嘴唇区域像素 L1 损失（权重最高，100），$\mathcal{L}_{VGG}$ 为 VGG 感知损失，$\mathcal{L}_{VGG}^{face}$ 为人脸身份保持损失。全部为重建类损失，无对抗项。

### 唇部编码器：12D 解耦姿势向量

唇部编码器（Figure 4）将人脸图像压缩为紧凑的 12 维唇部姿势向量，作为 Stage 1 的控制信号。其设计分为两个互补分支：

![[assets/figures/papers/paper_list_l2487_https_openaccess_thecvf_com_content_CVPR2026_html_Zinonos_FlashLips_100/figures/004_Figure_4.jpg]]
*Figure 4: Lips Encoder. A frozen expression encoder with an MLP projector and a mouth-crop CNN produce an 8D+4D lips vector. A distilled ResNet-34 replicates this mapping on inference*

- **V1（冻结表情编码器 + MLP 投影）：** 使用预训练的表情识别网络提取特征，经 MLP 投影到 8 维。消融实验（Table 5）表明，8 维时重建质量已接近饱和。
- **V2（口部裁剪 CNN 残差）：** 对嘴唇区域裁剪后经小型 CNN 提取 4 维残差向量，补充 V1 可能遗漏的唇部细节。

最终 12 维向量为 V1 的 8 维与 V2 的 4 维拼接。推理时，该编码器被蒸馏为轻量 ResNet-34，直接输出 12 维向量。

### Stage 2：流匹配驱动的音频到唇部姿势

Stage 2 将唇形同步转化为条件生成问题：从语音特征预测唇部姿势向量序列。模型以 wav2vec 2.0 特征为条件，采用流匹配目标训练。

在流匹配框架中，时间步 $t \in [0,1]$ 时，插值潜在向量定义为：

$$\mathbf{z}_t = (1 - t) \boldsymbol{\epsilon} + t \mathbf{z}_{\mathrm{lips}} \tag{10}$$

其中 $\boldsymbol{\epsilon} \sim \mathcal{N}(0, I)$ 为随机噪声，$\mathbf{z}_{\mathrm{lips}}$ 为真实唇部姿势向量。Transformer 预测速度场 $v_\theta(\mathbf{z}_t, t, \mathbf{c})$，其中 $\mathbf{c}$ 为音频条件。流匹配损失为：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{t, \boldsymbol{\epsilon}, a} \left\| v_{\theta}(\mathbf{z}_t, t, \mathbf{c}) - \mathbf{u} \right\|_2^2 \tag{12}$$

其中真实速度 $\mathbf{u} = \mathbf{z}_{\mathrm{lips}} - \boldsymbol{\epsilon}$。推理时，从随机噪声出发，用 ODE 求解器沿学习到的速度场积分，得到预测的唇部姿势向量，直接馈入 Stage 1 驱动编辑。

### 关键设计决策

**身份保留机制：** 通过投影参考潜在变量 $\overline{\mathbf{z}}_{\mathrm{ref}}$ 注入身份信息。消融实验（Tables 3, 4）表明，将参考帧数量从 1 增加到 4 可显著提升身份保留度（ID），而对唇形同步度影响极小。

**生成范式转变：** 从 GAN/扩散的多步迭代生成变为纯重建损失驱动的单步确定性编辑，这是实现 100+ FPS 推理速度的根本原因。U-Net 变体在单张 NVIDIA H100 上达到 109.41 FPS，比基于扩散的 KeySync 快约 30.4 倍（Table 2）。



## 实验与关键发现

### 核心性能：重建与交叉音频

FlashLips 在重建和交叉音频两种协议下，对 HDTF、CelebV-HQ、CelebV-Text 三个数据集随机抽取的 100 个重建视频和 100 对交叉音频样本进行了系统评估。Table 1 汇总了与 9 类代表性基线的全指标对比。

![[assets/figures/papers/paper_list_l2487_https_openaccess_thecvf_com_content_CVPR2026_html_Zinonos_FlashLips_100/figures/005_Table_1.jpg]]
*Table 1: Quantitative Comparison. Comparison on reconstruction and cross-audio scenarios over 100 randomly sampled reconstruction videos and 100 cross-audio pairs from HDTF, CelebV-HQ, and CelebV-Text. Best results are bold; second-best are underlined*

**重建场景**中，FlashLips-Transformer 在全部六项指标上达到最优或次优：FID 降至 4.43，FVD 降至 12.31，LipScore 达到 0.71，ID 保持 0.86。FlashLips-U-Net 以 FID 4.75、FVD 15.20 紧随其后，两者均显著优于最强的扩散基线 LatentSync（FID 5.30、FVD 36.47、LipScore 0.55）。这一差距表明，纯重建损失驱动的单步编辑不仅未牺牲质量，反而在时间一致性（FVD）上获得了数量级优势——这源于确定性编辑天然避免了扩散模型的多步采样抖动。

**交叉音频场景**中，方法排名整体保持，但各方法 LipScore 均有所下降，反映了跨身份音频-唇形映射的固有难度。FlashLips-Transformer 的 LipScore 为 0.63，仍处于第一梯队。值得注意的是，基于 GAN 的 Wav2Lip（Prajwal et al., ACM MM 2020）在交叉音频 LipScore 上表现强劲，但其 FID 和 FVD 显著劣化，暴露出对抗训练在视觉质量上的局限。

### 推理速度：从迭代到实时的跨越

Table 2 报告了在单张 NVIDIA H100 GPU 上、经 5 次预热后 10 次运行取平均的 FPS 对比。FlashLips-U-Net 以 **109.41 FPS** 登顶，较第二快的 MuseTalk（约 31 FPS）提速约 3.5 倍，较扩散类方法 KeySync（3.60 FPS）提速约 **30.4 倍**。FlashLips-Transformer 亦达到 66.84 FPS，仍远超所有非实时基线。

![[assets/figures/papers/paper_list_l2487_https_openaccess_thecvf_com_content_CVPR2026_html_Zinonos_FlashLips_100/figures/006_Table_2.jpg]]
*Table 2: Inference Speed. Speed comparison in frames per second (FPS). “Speedup” denotes the inference speed gain of our fastest model (FlashLips – U-Net) over each method. Measured on the same clip: 5 warm-ups, then 10 runs to average FPS*

速度优势的根源在于两阶段解耦设计：推理时，Stage 2 仅需预测一个 12 维唇部姿势向量，Stage 1 执行单次前馈编辑，整个管线无需扩散去噪迭代或 GAN 生成器多步推理，也无需嘴唇掩码预处理。这一结果直接验证了论文的核心主张——对于高度条件化的唇形同步任务，低维控制信号配合确定性重建足以替代昂贵的生成范式。

### 消融实验：控制空间与身份保留的权衡

**参考帧数量消融**（Table 3 和 Table 4）显示，将参考潜在变量从 1 帧增加到 4 帧，可显著提升身份保留度（ID），而对唇形同步度（LipScore）影响极小。这表明多参考帧为身份特征提供了更丰富的统计信息，而唇部编辑的局部性使得控制信号与身份信息在通道拼接后能被有效解耦。

**嘴唇编码器设计消融**（Table 5）揭示了质量-解耦的核心权衡：
- **V1（冻结表情编码器）**：在 8 维时重建质量趋于饱和，继续增加维度收益递减。
- **V2（添加口部 CNN 残差）**：单独使用可提升重建精度，但在交叉音频场景下身份保留度（ID）下降，说明口部残差编码了部分身份相关信息，削弱了控制空间与身份的分离。
- **12 维组合（8D V1 + 4D V2）**：在重建质量与交叉音频身份保留之间取得最佳折衷，被采纳为最终配置。

这一消融的深层含义是：唇部姿势控制空间需要在“表达能力”与“身份解耦”之间精确调谐——过强的表达能力会挟带身份信息，在跨身份驱动时产生伪影；过弱则无法覆盖唇形变体。

### 失败模式与局限

论文明确指出的局限包括：
1. **遮挡与极端姿态**：对严重遮挡、大幅头部旋转或极端表情的鲁棒性尚未充分验证。自细化过程依赖自我生成的伪对，在训练数据覆盖不足的边缘案例上可能产生伪影。
2. **表达丰富度受限**：当前 12 维唇部控制空间可能不足以编码韵律和情感等非言语信息，限制了生成唇形在自然度和表现力上的上限。
3. **两阶段误差累积**：Stage 2 的唇部向量预测误差会直接传导至 Stage 1 的编辑结果，在音频-唇形映射歧义较大的场景下可能出现不自然的唇部运动。

这些局限需要在部署时结合具体应用场景进行手动验证，尤其是涉及野外视频或高表现力需求的任务。

### 补充图表

![[assets/figures/papers/paper_list_l2487_https_openaccess_thecvf_com_content_CVPR2026_html_Zinonos_FlashLips_100/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of Quantitative Evaluation. Comparison of eight lip-sync models in the cross-audio setting on seven key metrics. Results are normalized, with the best-performing model scaled to the outer edge, and the worst towards the center*

![[assets/figures/papers/paper_list_l2487_https_openaccess_thecvf_com_content_CVPR2026_html_Zinonos_FlashLips_100/figures/009_Table_5.jpg]]
*Table 5: Lips Encoder Ablation. V1 (frozen expression encoder) saturates near 8D; adding a lips-crop residual (V2) improves reconstruction but reduces cross-audio ID. The 12D setting (V1 8D + V2 4D) offers the best quality–disentanglement trade-off*

![[assets/figures/papers/paper_list_l2487_https_openaccess_thecvf_com_content_CVPR2026_html_Zinonos_FlashLips_100/figures/007_Table_3.jpg]]
*Table 3: Reference Latent Ablation (Transformer). Ablation of the number of reference latents for the Transformer base model on a subset of metrics. Full ablations are in Table C.5*

![[assets/figures/papers/paper_list_l2487_https_openaccess_thecvf_com_content_CVPR2026_html_Zinonos_FlashLips_100/figures/008_Table_4.jpg]]
*Table 4: Reference Latent Ablation (U-Net). Ablation of the number of reference latents for the U-Net base model on a subset of metrics. Full ablations are provided in Table C.5*

![[assets/figures/papers/paper_list_l2487_https_openaccess_thecvf_com_content_CVPR2026_html_Zinonos_FlashLips_100/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative Comparison – Cross Audio. Comparison with other lip-sync methods for cross-audio. The top two rows show the source and audio-driving videos, followed by lip-synced outputs from each method*

![[assets/figures/papers/paper_list_l2487_https_openaccess_thecvf_com_content_CVPR2026_html_Zinonos_FlashLips_100/figures/001_Figure_1.jpg]]
*Figure 1: FlashLips Results. Selected results of source and driver pairs, generated using our transformer-based model*



## 定位与知识库关联

### 1. 范式转移：从迭代生成到单步重建

FlashLips 的核心贡献在于对唇形同步任务生成范式的根本性重构。现有主流方法可分为两大阵营：

**扩散模型阵营**以多步去噪实现高质量生成，但推理成本高昂。典型代表包括 **DiffDub** (Liu et al., ICASSP 2024)、**Diff2Lip** (Mukhopadhyay et al., WACV 2024)、**LatentSync**（基于潜在扩散模型）、**KeySync**（基于关键帧插值与掩码策略的扩散方法）以及 **SayAnything**（基于条件视频扩散）。这些方法在唇形同步准确性和视觉质量上表现优异，但其迭代采样机制导致推理速度成为实时部署的瓶颈——例如 KeySync 在 NVIDIA H100 上仅能达到 3.60 FPS。

**GAN 阵营**以 **Wav2Lip** (Prajwal et al., ACM MM 2020) 为代表，通过专家判别器实现单步前馈推理，避免了扩散的迭代成本。然而 GAN 训练的不稳定性、模式坍塌风险以及对显式嘴唇掩码的依赖，限制了其在复杂场景下的鲁棒性和易用性。

FlashLips 通过**纯重建损失驱动的单步确定性编辑**，从根本上绕开了上述两难困境：既不需要扩散的多步采样，也不需要 GAN 的对抗训练。其 Stage 1 编辑器（LipsChange）在 VAE 潜在空间中执行单次前向传播即可完成唇部修改，配合自细化（self-refinement）伪对训练实现完全无掩码推理。这一设计使其 U-Net 变体在单张 H100 GPU 上达到 **109.41 FPS**，比 KeySync 快约 30.4 倍（Table 2），同时重建 FID 为 4.75，优于 LatentSync 的 5.30（Table 1）。

### 2. 控制信号解耦：从端到端生成到姿势驱动编辑

传统唇形同步方法通常直接从音频端到端生成图像或视频帧，音频特征与视觉生成的耦合使得身份保留和编辑可控性成为持久挑战。**TalkLip** (Wang et al., CVPR 2023) 引入对比学习与唇读专家来增强音频-嘴唇对齐，**IP-LAP** (Zhong et al., CVPR 2023) 则利用身份先验与中间关键点来保持人物特征，但这些方法仍在端到端框架内运作。

FlashLips 将控制信号显式解耦为**低维唇部姿势向量**（12D：8D 冻结表情编码器 + 4D 口部 CNN 残差），形成两阶段流水线：
- **Stage 1**：唇部姿势向量 → 潜在空间编辑（LipsChange）
- **Stage 2**：音频（wav2vec 2.0 特征）→ 唇部姿势向量（基于流匹配的 Transformer）

这一解耦带来三重优势：
1. **编辑可控性**：唇部姿势成为显式中间表示，可独立操控或插值；
2. **训练效率**：Stage 1 仅需图像数据（约 500 小时），Stage 2 在更小的音频-视觉数据集上训练，大幅降低对配对音视频数据的依赖；
3. **身份保持**：身份信息通过投影参考潜在变量（projected reference latents）注入编辑器，与唇部控制信号分离。

消融实验证实，12D 向量在重建质量与身份解耦之间取得最佳折衷：8D 冻结表情编码器（V1）在重建质量上接近饱和，添加 4D 口部残差（V2）虽提升重建但降低交叉音频场景下的身份保留度（Table 5）。

### 3. 身份保留机制对比

FlashLips 的身份保留策略与现有方法存在显著差异：
- **Wav2Lip** 等早期方法依赖全局特征条件注入，身份信息与唇部编辑在特征空间中纠缠；
- **MuseTalk** 等实时方法通过时空采样保持时序一致性，但对参考帧的利用较为隐式；
- FlashLips 采用**投影参考潜在变量 + 多参考帧动态选择**，将身份信息作为显式条件输入编辑器。消融实验表明，将参考帧数量从 1 增加到 4 可显著提升身份保留度（ID），对唇形同步度影响极小（Tables 3 and 4）。

### 4. 适用边界与局限性

尽管 FlashLips 在标准基准上表现优异，其当前设计存在明确边界：

1. **鲁棒性边界**：对严重遮挡、大幅头部旋转或极端表情的鲁棒性尚未充分验证。自细化过程依赖自我生成的伪对，可能在训练数据覆盖不足的边缘案例上产生伪影。

2. **表达丰富度限制**：当前 12D 唇部控制空间可能不足以编码韵律和情感等非言语信息。与能够生成丰富表情的扩散方法（如 LatentSync）相比，FlashLips 在表达细腻度上可能存在差距。

3. **两阶段解耦的扩展性**：虽然解耦设计在唇形同步任务上取得成功，但其能否扩展至全身动画或动态背景的视频编辑任务仍是开放问题。

### 5. 开放问题与后续方向

基于上述分析，FlashLips 框架指向以下研究方向：

1. **鲁棒性增强**：如何将遮挡感知机制或头部运动补偿模块集成到单步编辑器中，使其适应真实场景中的非理想条件？

2. **控制空间扩展**：能否将韵律和情感感知信号集成到唇部姿势向量中，在保持实时性的同时实现更自然的唇形同步？这可能需要在 Stage 2 的流匹配框架中引入额外的条件分支。

3. **框架泛化**：两阶段“姿势预测 + 潜在编辑”范式是否可以推广至全身动画生成、动态背景替换或更广泛的视频编辑任务？这需要验证低维控制表示在更复杂运动模式下的表达能力。

4. **与实时方法的深度融合**：FlashLips 的 100+ FPS 推理速度使其可与 **MuseTalk** 等实时方法直接竞争，但两者在身份保持机制和编辑粒度上的差异值得进一步对比研究。



## 原文 PDF

![[paperPDFs/CVPR_2026/FlashLips_100_FPS_Mask_Free_Latent_Lip_Sync_using_Reconstruction_Instead_of_Diffusion_or_GANs.pdf]]
