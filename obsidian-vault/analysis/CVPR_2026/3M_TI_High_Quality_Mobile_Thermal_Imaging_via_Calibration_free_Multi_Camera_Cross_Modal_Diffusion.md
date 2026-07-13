---
title: "3M-TI: High-Quality Mobile Thermal Imaging via Calibration-free Multi-Camera Cross-Modal Diffusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/3M_TI_High_Quality_Mobile_Thermal_Imaging_via_Calibration_free_Multi_Camera_Cross_Modal_Diffusion.pdf
project_link: null
code_link: "https://github.com/work-submit/3MTI"
aliases:
- 3T
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在VAE潜在空间中利用交叉模态自注意力（CSM）实现无需像素级标定的RGB与热成像特征对齐与融合，并结合位姿不对齐数据增强策略提升鲁棒性。
primary_logic: 在VAE的连续、解耦潜在空间中，通过跨模态自注意力隐式对齐多模态特征，避免像素级标定；借助扩散模型生成先验恢复高保真细节；不对齐增强迫使模型学习鲁棒对应关系，克服训练数据与实际部署间的域差距。
claims:
- 3M-TI在公开数据集上取得了最佳的感知质量（LPIPS、MANIQA、MUSIQ），显著优于传统方法和扩散方法。
- 在真实手机采集的无标定数据上，3M-TI的无参考指标（MUSIQ 30.62）大幅领先其他方法，证明了免标定方案的实用性。
- 下游目标检测任务中，3M-TI增强的热图像取得了最高的F1分数（0.4724），甚至略微超过RGB参考结果。
- 消融实验证实跨模态自注意力（CSM）和位姿不对齐增强是3M-TI性能的关键贡献因子；移除它们导致细节丢失和鲁棒性下降。
---

# 3M-TI: High-Quality Mobile Thermal Imaging via Calibration-free Multi-Camera Cross-Modal Diffusion

> [!tip] 核心洞察
> 在VAE的连续、解耦潜在空间中，通过跨模态自注意力隐式对齐多模态特征，避免像素级标定；借助扩散模型生成先验恢复高保真细节；不对齐增强迫使模型学习鲁棒对应关系，克服训练数据与实际部署间的域差距。

| 字段 | 内容 |
|------|------|
| 中文题名 | 3M-TI：基于免校准多相机跨模态扩散的高质量移动热成像 |
| 英文题名 | 3M-TI: High-Quality Mobile Thermal Imaging via Calibration-free Multi-Camera Cross-Modal Diffusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.19117) · [Code](https://github.com/work-submit/3MTI) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | 3M-TI |
| Dataset | Public RGB-Thermal Datasets, Real-World Smartphone Dataset, Downstream Object Detection |

> [!tip] 效果简介
> - Public RGB-Thermal Datasets (IRVI, LLVIP, M3FD, PBVS) 上，Perceptual Metrics (LPIPS, MANIQA, MUSIQ) Best / superior to all baselines vs CoReFusion, SwinFuSR, CoRPLE, SwinPaste, SeeSR, OSEDiff, DifIISR (significant improvement over second-best)。
> - Real-World Smartphone Dataset 上，MUSIQ 30.62 (3M-TI) vs Second-best among compared methods (value not explicitly reported in text) (highest score)。
> - Downstream Object Detection (LLVIP) 上，F1-score 0.4724 (3M-TI) vs Other SR methods and reference RGB (best overall (slightly surpasses RGB reference))。

## 概要

**问题瓶颈**：移动端热成像受限于微型传感器，空间分辨率低、纹理细节严重缺失；现有超分辨率方法要么难以恢复精细结构，要么依赖繁琐的跨相机像素级标定，在实际部署中几乎不可行。

**核心调控**：3M-TI 在 VAE 潜在空间中引入**跨模态自注意力（Cross-Modal Self-Attention, CSM）**，将 RGB 与热成像的潜在特征隐式对齐并融合，完全规避像素级标定；同时辅以**位姿不对齐数据增强**，模拟多相机视差与时间偏移，提升模型对真实场景的鲁棒性。

**关键洞见**：VAE 连续、解耦的潜在空间使多模态特征可在无需像素对应的情况下通过自注意力建立隐式对齐；扩散模型的生成先验则进一步恢复高保真热纹理细节；不对齐增强迫使模型学习鲁棒的跨模态对应关系，弥合训练数据与实际部署之间的域差距。

**方法定位**：3M-TI 是一步式跨模态扩散超分辨率框架，在扩散 UNet 中用 CSM 替换原始自注意力层，结合 LoRA 高效微调 UNet 与 VAE 解码器，并引入零初始化的跳跃连接以保持结构一致性。相比 **CoReFusion**（Kasliwal et al., CVPR 2023）、**SwinFuSR/SwinPaste**（Zhong et al., CVPR 2025）、**DifIISR**（Li et al., CVPR 2025）等 RGB 引导的热成像超分方法，以及 **SeeSR**（Wu et al., CVPR 2024）、**OSEDiff**（Wu et al., NeurIPS 2024）等通用扩散超分方法，3M-TI 的核心差异在于**免标定跨模态潜在对齐**与**不对齐鲁棒性设计**。

**主要结果**：
- 在公开 RGB-热成像数据集（IRVI、LLVIP、M3FD、PBVS）上，3M-TI 在感知质量指标 **LPIPS、MANIQA、MUSIQ** 上全面领先（Table 1）。
- 在真实手机采集的无标定数据上，3M-TI 的 MUSIQ 达到 **30.62**，显著优于其他方法（Table 2）。
- 下游目标检测任务中，3M-TI 增强的热图像取得最高 F1 分数 **0.4724**，甚至略超 RGB 参考结果（Table 3）。
- 消融实验证实，CSM 与不对齐增强是性能的关键贡献因子，移除后细节丢失、鲁棒性明显下降（Table 4）。

**待验证问题**：论文未提供移动端推理速度与内存占用分析，实际部署效率仍需验证；极端视差或剧烈旋转下 CSM 的对齐可靠性、以及 RGB 失效场景下的生成安全性，也需进一步考察。

热成像在安防监控、自动驾驶、夜间感知等场景中具有不可替代的价值。然而，高分辨率热像仪体积庞大、成本高昂，难以集成到智能手机等移动平台上。受限于微型化传感器的物理尺寸，移动端热成像的空间分辨率与纹理细节严重不足，这构成了**核心瓶颈**：移动热成像硬件微型化导致空间分辨率与纹理细节严重缺失，现有超分辨率方法要么无法恢复精细结构，要么依赖繁琐的跨相机像素级标定，难以实际部署。

现有RGB引导的热图像超分辨率方法大致可分为两类。一类是基于卷积或Transformer的回归方法，如**CoReFusion**（Kasliwal et al., CVPR 2023）、**CoRPLE**（Li et al., ECCV 2024）、**SwinFuSR**和**SwinPaste**（Zhong et al., CVPR 2025），它们通常假设RGB与热成像图像已经过精确的像素级对齐。然而，在多相机移动系统中，RGB与热成像相机之间存在固有的视差和时间偏移，精确标定过程繁琐且在消费级设备上难以实现。另一类是基于扩散模型的方法，如**SeeSR**（Wu et al., CVPR 2024）、**OSEDiff**（Wu et al., NeurIPS 2024）和**DifIISR**（Li et al., CVPR 2025），它们利用扩散先验生成更丰富的细节，但同样依赖对齐良好的输入对，且对跨模态特征融合的设计考虑不足。

上述方法的共同缺陷在于：**对像素级标定的刚性依赖**使得它们在实际多相机移动系统中难以部署，同时缺乏对跨模态特征对齐与融合的专门设计，导致在真实场景下性能显著退化。

针对这一困境，本文提出**3M-TI**，一种面向免校准多相机移动热成像的跨模态扩散框架。其核心动机在于：将RGB与热成像的对齐问题从像素空间转移到VAE的连续、解耦潜在空间中，利用跨模态自注意力隐式学习多模态对应关系，从而彻底规避像素级标定的需求；同时借助扩散模型的生成先验恢复高保真热纹理细节，并通过位姿不对齐数据增强策略提升模型对真实部署中视差与时间偏移的鲁棒性。

## 核心方法与创新机理

3M‑TI 的核心创新在于**在 VAE 潜在空间中通过跨模态自注意力实现免标定的 RGB‑热成像特征融合**，并结合**位姿不对齐数据增强**与**高效 LoRA 微调**，解决了移动端多相机热成像超分辨率中“标定依赖”与“细节恢复不足”两大瓶颈。

### 跨模态自注意力（CSM）：隐式对齐替代像素级标定

传统的 RGB 引导热成像超分辨率方法（如 **CoReFusion** (Kasliwal et al., CVPR 2023)、**SwinFuSR** / **SwinPaste** (Zhong et al., CVPR 2025)）通常假设 RGB 与热成像图像已精确配准，或依赖显式的像素级标定流程，这在移动端多相机系统中难以保证。3M‑TI 的 **跨模态自注意力模块（Cross‑Modal Self‑Attention, CSM）** 直接替换扩散 UNet 中原有的自注意力层，在 VAE 的连续、解耦潜在空间中执行联合自注意力计算。

具体而言，RGB 和热成像的潜在表示被拼接为张量 $\{ z_{RGB}^{0}, z_{th}^{0} \} \in \mathbb{R}^{B \times M \times C \times H \times W}$（其中 $M=2$），随后重排为 $\mathbb{R}^{B \times (M \times H \times W) \times C}$，将所有像素视为 token 并合并为单一序列。自注意力计算完成后，再恢复为 $\mathbb{R}^{(B \times M) \times C \times H \times W}$ 的原始形状。这一设计使模型能够同时捕获**跨模态（RGB‑热成像）的引导信息**与**模态内（热‑热）的结构依赖**，无需任何显式标定即可隐式学习多尺度对应关系。

消融实验证实，CSM 在 PSNR / SSIM / LPIPS 上均优于原始自注意力、特征拼接和标准交叉注意力等变体（Table 4），是 3M‑TI 性能的关键贡献因子。

### 位姿不对齐增强：弥合训练与部署的域差距

多相机系统固有的视差与时间偏移导致训练数据（通常为配准图像对）与实际部署场景之间存在显著的域差距。3M‑TI 引入**位姿不对齐数据增强策略**，对 RGB 图像施加可控的空间变换（随机平移、缩放、旋转和透视变形），模拟真实多相机采集中的几何与时间不对齐。

消融实验表明，移除此增强后模型对几何偏移的鲁棒性显著下降，高频细节出现可见退化（Table 4）。该策略迫使模型在训练阶段即学习鲁棒的跨模态对应关系，是 3M‑TI 在真实手机采集的无标定数据上取得最高无参考质量分数（MUSIQ 30.62, Table 2）的重要保障。

### 高效 LoRA 微调与结构保持设计

为降低扩散模型在 RGB‑热成像双模态任务上的训练成本，3M‑TI 采用 **LoRA 低秩适配** 对 UNet（秩 16）和 VAE 解码器（秩 4）进行微调，仅需单张 NVIDIA A800 GPU 约 4 小时即可完成训练。此外，从 VAE 编码器到解码器的**零初始化跳跃连接**被引入以增强结构一致性，消融实验中移除该连接会导致几何失真（如圆形车轮变形），验证了其对结构保真度的贡献。

### 与现有扩散超分辨率方法的关系

相较于通用扩散超分辨率方法 **SeeSR** (Wu et al., CVPR 2024) 和 **OSEDiff** (Wu et al., NeurIPS 2024)，3M‑TI 的差异化在于面向**跨模态、免标定**场景的专门设计；相较于红外专用扩散方法 **DifIISR** (Li et al., CVPR 2025)，3M‑TI 进一步利用了 RGB 语义引导（通过 RAM 文本提示）和不对齐鲁棒性机制。这些 changed slots 共同构成了 3M‑TI 在感知质量指标（LPIPS、MANIQA、MUSIQ）上全面领先 baseline 的方法论基础。

3M-TI 是一套面向免标定、非同步多相机系统的跨模态扩散框架，其核心目标是从一张低分辨率热成像图像和一张未标定的高分辨率可见光参考图中，重建出纹理清晰、结构保真的高分辨率热图像。整个 pipeline 围绕三个关键挑战展开：RGB 与热成像相机之间的视差与时间偏移、异构模态特征的融合，以及训练数据规模与多样性的不足。

**输入与预处理。** 系统接收一对未标定的 RGB-热成像图像。RGB 图像首先通过 **Recognize Anything Model (RAM)** 提取语义标签，作为文本条件注入扩散模型；随后，对 RGB 图像施加**位姿不对齐增强**——包括随机平移、缩放、旋转和透视变换——以模拟真实部署中多相机视差与时间偏移造成的空间错位。这一增强策略是 3M-TI 免标定能力的关键保障。

**潜在空间编码。** 增强后的 RGB 图像与低分辨率热成像图像分别送入一个冻结的 VAE 编码器，映射到连续、解耦的潜在表示。两个潜在张量被拼接为一个联合张量，其形状为 $\mathbb{R}^{B \times M \times C \times H \times W}$，其中 $M=2$ 表示两种模态。这一拼接操作将多模态信息统一在同一潜在空间中，为后续的跨模态交互奠定基础。

**扩散 UNet 与跨模态自注意力。** 拼接后的潜在张量进入扩散 UNet 的去噪过程。3M-TI 的核心创新在于将 UNet 中原有的自注意力层替换为**跨模态自注意力模块（CSM）**。CSM 首先将潜在张量重塑为 $\mathbb{R}^{B \times (M \times H \times W) \times C}$，将每个像素视为一个 token，并将所有模态的 token 拼接为一个长序列；随后在该序列上执行联合自注意力，使模型能够同时捕获模态间（RGB-热成像）的引导信息和模态内（热成像自身）的结构依赖关系；注意力计算完成后，张量恢复为 $\mathbb{R}^{(B \times M) \times C \times H \times W}$ 的形状。这一设计无需像素级标定，在潜在空间中隐式学习多尺度跨模态对应关系。

**结构保持与解码重建。** 为了缓解扩散生成中常见的几何失真，3M-TI 在 VAE 编码器与解码器之间引入了一条**零初始化跳跃连接**，将编码器的下采样特征直接传递至解码器，增强结构一致性。去噪后的潜在表示最终由 VAE 解码器重建为高分辨率热图像。

**高效训练策略。** 整个框架采用低秩适配（LoRA）进行微调：UNet 的 LoRA rank 设为 16，VAE 解码器的 LoRA rank 设为 4。训练损失为 L2 损失与 LPIPS 感知损失的组合，权重 $\lambda=1$。在单张 NVIDIA A800 (80 GB) GPU 上，以 batch size 4 和 Adam 优化器（学习率 $2 \times 10^{-5}$）训练约 4 小时（8000 次迭代）即可收敛。

综上，3M-TI 的 pipeline 通过“不对齐增强→VAE 潜在编码→跨模态自注意力融合→跳跃连接保结构→VAE 解码重建”的串联设计，实现了无需标定的高质量移动热成像增强。

![[assets/figures/papers/paper_list_l2433_https_arxiv_org_abs_2511_19117/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the 3M-TI architecture. (a) 3M-TI framework. The core of 3M-TI is a one-step diffusion-based model equipped with a cross-modal self-attention module (CSM) and a misalignment augmentation strategy. LoRA fine-tuning is applied to both the UNet and the VAE decoder. (b) Cross-modal self-attention module (CSM). Two rearrangement layers are inserted before and after the original self-attention layers to capture cross-modal correspondences. (c) Misalignment augmentation. A data augmentation strategy designed to enhance model robustness against camera parallax and temporal misalignment between RGB and thermal inputs*

![[assets/figures/papers/paper_list_l2433_https_arxiv_org_abs_2511_19117/figures/001_Figure_1.jpg]]
*Figure 1: A smartphone-based mobile imaging system integrating calibration-free and synchronization-free RGB and thermal cameras. The proposed 3M-TI method delivers superior thermal image quality compared with state-of-the-art restoration approaches*

### 3.1 整体框架

3M-TI 是一个基于单步扩散模型的跨模态热成像重建框架，其输入为一幅低分辨率热图像与一幅未经标定的高分辨率 RGB 参考图像，输出为高保真高分辨率热图像。框架由三个核心设计支撑：**跨模态自注意力模块（CSM）** 实现免标定的特征对齐与融合；**不对齐数据增强策略** 模拟多相机视差与时序偏移，提升部署鲁棒性；**LoRA 低秩适配** 实现高效微调。

### 3.2 跨模态自注意力模块（CSM）

CSM 是 3M-TI 的核心创新，直接替换扩散 UNet 中原有的自注意力层。其关键思想是：在 VAE 的连续、解耦潜在空间中，将 RGB 与热成像的潜在特征在 token 维度拼接，执行联合自注意力，使模型同时捕捉**跨模态（RGB→热成像）引导**与**模态内（热成像→热成像）结构依赖**，从而隐式学习多尺度对应关系，无需任何像素级标定。

具体操作流程如下：

1. **潜在编码与拼接**：将 RGB 和热图像分别通过冻结的 VAE 编码器，得到潜在表示后沿模态维度拼接，形成张量：
   $$
   \{ z_{RGB}^{0}, z_{th}^{0} \} \in \mathbb{R}^{B \times M \times C \times H \times W}
   $$
   其中 $B$ 为批次大小，$M=2$ 表示 RGB 与热成像两个模态，$C$ 为通道数，$H \times W$ 为潜在空间分辨率。

2. **Token 化重排**：将上述张量重排为自注意力所需的形式，把每个空间位置的像素视为一个 token，并将所有模态的 token 拼接为一个长序列：
   $$
   \mathbb{R}^{B \times (M \times H \times W) \times C}
   $$
   此时序列长度为 $M \times H \times W$，自注意力计算在全体 RGB 与热成像 token 之间进行，实现跨模态信息交互。

3. **自注意力与形状恢复**：执行标准自注意力后，将输出重排回原始批次-模态-空间形状：
   $$
   \mathbb{R}^{(B \times M) \times C \times H \times W}
   $$
   随后分离 RGB 与热成像分支，仅热成像分支继续参与后续去噪与解码。

消融实验证实，CSM 在 PSNR/SSIM/LPIPS 指标上均优于原始自注意力、特征拼接和标准交叉注意力等替代方案（Table 4），是 3M-TI 性能的关键贡献因子。

### 3.3 不对齐数据增强

为克服训练数据（通常为像素级对齐的公开数据集）与实际部署中多相机视差、时序偏移之间的域差距，3M-TI 对 RGB 图像施加可控空间变换，包括随机平移、缩放、旋转和透视变形。该策略迫使模型在训练阶段即学习鲁棒的跨模态对应关系，而非依赖精确对齐。消融实验表明，移除该增强会显著降低模型对几何与时序偏移的鲁棒性，导致高频细节丢失。

### 3.4 结构保持与高效微调

- **跳跃连接**：在 VAE 编码器与解码器之间引入零初始化跳跃连接，将编码器下采样特征传递至解码器，增强重建热图像的结构一致性，缓解几何畸变。
- **LoRA 微调**：对扩散 UNet（秩 16）和 VAE 解码器（秩 4）施加低秩适配，大幅降低可训练参数量。训练仅需单张 NVIDIA A800（80 GB）GPU 约 4 小时（8000 次迭代）。
- **语义提示**：利用 Recognize Anything Model（RAM）从 RGB 图像提取语义标签，作为扩散模型的文本条件输入，提供高层语义引导。

### 3.5 训练损失

3M-TI 采用组合损失函数，平衡像素级保真度与感知质量：
$$
\mathcal{L} = \mathcal{L}_2 + \lambda \cdot \mathcal{L}_{\mathrm{LPIPS}}
$$
其中 $\mathcal{L}_2$ 为均方误差损失，$\mathcal{L}_{\mathrm{LPIPS}}$ 为感知损失，权重 $\lambda=1$。该损失在公开数据集和真实手机采集数据上均取得了最佳的感知质量指标（LPIPS、MANIQA、MUSIQ）。

## 实验与关键发现

### 核心定量结果：感知质量与真实场景泛化

3M‑TI在两类场景下均表现出显著优势：**（1）公开多模态数据集**上的感知质量全面领先，**（2）真实手机采集的无标定数据**上展现出最强的实用泛化能力。

**公开数据集评估**（Table 1）覆盖IRVI、LLVIP、M3FD、PBVS四个RGB‑热成像基准，对比方法包括传统UNet方案**CoReFusion**（Kasliwal et al., CVPR 2023）、Swin Transformer架构的**SwinFuSR**与**SwinPaste**（Zhong et al., CVPR 2025）、轮廓波增强方法**CoRPLE**（Li et al., ECCV 2024），以及扩散超分方法**SeeSR**（Wu et al., CVPR 2024）、**OSEDiff**（Wu et al., NeurIPS 2024）和**DifIISR**（Li et al., CVPR 2025）。3M‑TI在感知指标LPIPS、MANIQA、MUSIQ上均取得最优，表明其重建结果在结构相似性和人类感知质量两个维度上同时超越所有基线。值得注意的是，这一优势并非以牺牲保真度为代价——消融实验（Table 4）显示完整模型在PSNR/SSIM上也达到最佳平衡。

**真实手机数据集评估**（Table 2）是验证免标定方案实用性的关键证据。该数据集由多相机手机系统采集，RGB与热成像之间存在真实的视差与时间偏移，且无像素级标定信息。3M‑TI的MUSIQ达到30.62，在所有对比方法中最高，证明跨模态自注意力（CSM）与不对齐增强策略使模型在训练分布之外的部署场景下仍能保持鲁棒的对齐与生成质量。

### 下游任务验证：检测与分割

热成像超分辨率的最终价值在于支撑下游视觉任务。在LLVIP数据集的**目标检测**任务中（Table 3），以YOLOv11为检测器，3M‑TI增强的热图像取得F1分数0.4724，不仅超越所有超分方法，甚至略微超过RGB参考图像的检测结果。这一反直觉的发现表明，3M‑TI不仅恢复了空间细节，还可能增强了热模态特有的目标‑背景对比度，使检测器获益。定性可视化（Figure 5）进一步显示，3M‑TI减少了误检（红色框）和漏检，验证了其在实际安防与自动驾驶场景中的潜力。分割任务（Figure 6）同样表明3M‑TI输出能够支撑更精细的像素级理解。

![[assets/figures/papers/paper_list_l2433_https_arxiv_org_abs_2511_19117/figures/009_Table_3.jpg]]
*Table 3: Detection performance comparison across different methods, reference RGB, and GT, evaluated by Precision, Recall, F1- score, and IoU*

![[assets/figures/papers/paper_list_l2433_https_arxiv_org_abs_2511_19117/figures/007_Figure_5.jpg]]
*Figure 5: Visualization of detection results, where green bounding boxes indicate the correct detection, red bounding boxes indicate the wrong detection*

![[assets/figures/papers/paper_list_l2433_https_arxiv_org_abs_2511_19117/figures/008_Figure_6.jpg]]
*Figure 6: Visualization of segmentation results, where different colors represent different object categories*

### 消融实验：关键组件贡献

Table 4系统拆解了3M‑TI各设计的独立贡献，结论清晰：

- **跨模态自注意力（CSM）** 是性能核心。相比原始单模态自注意力、特征拼接、标准交叉注意力三种替代方案，CSM在所有指标上均最优。其机制——将RGB与热成像的潜在token拼接后进行联合自注意力——使模型同时捕获跨模态引导与热成像模态内的结构依赖，避免了标准交叉注意力中单向查询带来的信息瓶颈。
- **位姿不对齐增强** 被移除后，模型对几何与时序偏移的鲁棒性显著下降，高频细节丢失。这验证了训练阶段的随机平移、缩放、旋转和透视变换确实迫使模型学习隐式对齐能力，而非过拟合于完美配准的训练对。
- **RGB参考分支** 被移除后，重建结果明显模糊（如自行车辐条和灌木纹理），证实跨模态引导对细节恢复不可或缺。
- **跳跃连接** 被移除后，几何结构保真度下降（如圆形车轮变形），表明VAE编码器‑解码器间的零初始化跳跃连接对维持结构一致性至关重要。

### 失败模式与待验证问题

论文未系统报告定量失败案例，但以下边界条件需人工验证或进一步研究：
- 当RGB参考完全失效（全黑、过曝、遮挡）时，扩散模型是否会产生不符合热物理规律的虚假纹理，目前缺乏实验证据。
- 真实手机数据集的评估仅依赖无参考指标MUSIQ，缺少用户主观研究或热物理一致性度量，结论的可靠性需要补充验证。
- 相机视差过大（超大基线）或剧烈旋转场景下CSM的对齐能力未单独压力测试，实际极限未知。

![[assets/figures/papers/paper_list_l2433_https_arxiv_org_abs_2511_19117/figures/010_Table_4.jpg]]
*Table 4: Ablation study of 3M-TI components. Gray cells indicate the best result for each metric*

## 定位与知识库关联

### 1. 在热成像超分辨率谱系中的位置

移动端热成像超分辨率（SR）长期受困于硬件微型化带来的低空间分辨率与纹理缺失。现有方法可大致分为两条技术路线：

**传统多模态融合路线**以 RGB 图像为引导，通过显式的像素级对齐或特征融合来增强热图像。代表性工作包括 **CoReFusion**（Kasliwal et al., CVPR 2023）采用 UNet 架构进行 RGB 引导的热成像 SR，**CoRPLE**（Li et al., ECCV 2024）引入 Contourlet 残差提示增强，以及 **SwinFuSR** 和 **SwinPaste**（Zhong et al., CVPR 2025）基于 Swin Transformer 改进多模态融合。这些方法的共同瓶颈在于：它们或依赖繁琐的跨相机像素级标定，或无法有效恢复精细结构，在真实非标定场景下性能退化严重。

**扩散模型路线**利用生成先验提升感知质量。**SeeSR**（Wu et al., CVPR 2024）和 **OSEDiff**（Wu et al., NeurIPS 2024）在可见光 SR 中展示了扩散模型的高保真生成能力，**DifIISR**（Li et al., CVPR 2025）则将扩散模型引入红外图像 SR。但这些方法要么未处理跨模态融合问题，要么仍假设输入已精确对齐，未解决移动多相机系统固有的视差与时间偏移。

3M-TI 的关键突破在于**将跨模态对齐从像素空间迁移至 VAE 潜在空间**，通过跨模态自注意力（CSM）隐式学习 RGB 与热成像特征的多尺度对应关系，彻底绕过了像素级标定的需求。这一设计使其在方法谱系中占据“免标定跨模态扩散 SR”的新位置——既继承了扩散模型的生成先验优势，又通过潜在空间对齐解决了多模态融合的核心障碍。

### 2. 与基线方法的关键差异

| 维度 | 基线方法 | 3M-TI 的差异 |
|------|----------|-------------|
| **对齐方式** | 像素级标定或显式特征拼接 | VAE 潜在空间中 CSM 隐式对齐，无需标定 |
| **数据增强** | 对齐图像对，无刻意不对齐 | 位姿不对齐增强（平移、缩放、旋转、透视变换）模拟真实视差 |
| **训练效率** | 全参数训练 | LoRA 微调 UNet（rank 16）和 VAE 解码器（rank 4） |
| **结构保持** | 无显式跳跃连接 | 零初始化跳跃连接从 VAE 编码器到解码器 |

CSM 的设计尤为关键：它将 RGB 和热成像的潜在 token 拼接后执行联合自注意力，使模型能够同时捕捉**跨模态引导**（RGB→热成像）和**模态内结构依赖**（热成像→热成像）。消融实验证实，CSM 在 PSNR/SSIM/LPIPS 上均优于原始自注意力、特征拼接和标准交叉注意力（Table 4）。

位姿不对齐增强则是应对“训练-部署域差距”的核心策略。通过随机施加可控空间变换，迫使模型学习鲁棒的跨模态对应关系，而非记忆精确的像素位置。消融实验表明，移除该增强后模型对几何和时间偏移的鲁棒性显著下降，高频细节丢失严重。

### 3. 适用边界

3M-TI 的设计假设以下条件成立：
- **RGB 参考可用且质量可接受**：当 RGB 图像严重退化（如极低光照、强眩光）或完全不可用时，模型可能生成不符合物理规律的虚假热纹理。消融中移除 RGB 分支导致重建显著模糊（如自行车辐条和灌木纹理丢失），验证了 RGB 引导的必要性。
- **视差和偏移在训练增强范围内**：位姿不对齐增强覆盖了平移、缩放、旋转和透视变换，但超大基线或剧烈旋转场景下的对齐可靠性尚未验证。
- **场景在训练分布内**：训练数据覆盖白天和夜间，但极端天气（烟雾、大雨、沙尘）下的泛化能力未充分讨论。
- **RAM 能提取有效语义**：文本提示依赖 Recognize Anything Model 从 RGB 中识别物体标签。对于缺乏可识别物体的场景（如纯纹理表面），语义提示可能失效或误导扩散生成。

### 4. 局限与开放问题

1. **推理效率未量化**：论文未提供在移动设备上的推理速度与内存占用分析。尽管采用一步扩散和 LoRA 微调降低了训练成本，实际部署效率仍需验证。

2. **无 RGB 引导时的安全性**：在全黑或 RGB 失效场景下，扩散模型是否会产生违背热物理规律的“幻觉”纹理？该问题对安防、自动驾驶等安全关键应用至关重要。

3. **极端视差下的对齐鲁棒性**：CSM 的隐式对齐能力存在上限。当相机基线极大或旋转角度超出增强范围时，对齐可能失败，导致结构失真。

4. **多帧/多视角扩展**：当前方法处理单对 RGB-热成像输入。融合多视角或多帧序列是否可进一步提升质量与鲁棒性，是一个值得探索的方向。

5. **RAM 语义提示的敏感性**：RAM 生成的标签质量直接影响文本条件。对于特定场景（如缺乏可识别物体），提示可能缺失或错误，存在误导扩散生成的风险。论文未对此进行消融分析。

6. **真实手机数据的定量基准有限**：Table 2 仅报告了无参考指标 MUSIQ，缺乏在真实场景下的全参考评估（因无 GT），结论的确定性受限于无参考指标的可靠性。

## 原文 PDF

![[paperPDFs/CVPR_2026/3M_TI_High_Quality_Mobile_Thermal_Imaging_via_Calibration_free_Multi_Camera_Cross_Modal_Diffusion.pdf]]
