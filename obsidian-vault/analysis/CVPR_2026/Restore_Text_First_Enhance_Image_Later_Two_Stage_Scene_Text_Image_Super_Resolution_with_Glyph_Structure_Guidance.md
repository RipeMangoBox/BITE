---
title: "Restore Text First, Enhance Image Later: Two-Stage Scene Text Image Super-Resolution with Glyph Structure Guidance"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Restore_Text_First_Enhance_Image_Later_Two_Stage_Scene_Text_Image_Super_Resolution_with_Glyph_Structure_Guidance.pdf
project_link: null
code_link: null
aliases:
- TTIGSR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将字形结构恢复与图像增强显式解耦，并利用恢复的精确字形掩模作为全局超分的强结构约束。
primary_logic: 采用“文本优先、图像随后”的两阶段范式，第一阶段独立重建高质量字形结构，避免非文本区域干扰；第二阶段以该结构为条件引导整体图像超分，从而在保留笔画精度的同时实现背景与文本的和谐融合。
claims:
- TIGER 在 Real-CE 和 UZ-ST 上均实现了最优的图像质量和文本准确率，OCR-A 比强基线 TADiSR 分别高出 2.6% 和 6.4%。
- 消融实验证实，使用 TIGER 的文本恢复流水线比标准字体、SAM-TS 提取或常规 LDM 生成的方式更具优势，OCR-A 提升超过 8 个百分点。
- 即使省略 OCR 文本或输入随机文本，方法仍能保持高精度，表明第一阶段从 LR 图像本身恢复字形结构，对 OCR 依赖有限。
- Real-CE (×4) 上 OCR-A = 67.3%
---

# Restore Text First, Enhance Image Later: Two-Stage Scene Text Image Super-Resolution with Glyph Structure Guidance

> [!tip] 核心洞察
> 采用“文本优先、图像随后”的两阶段范式，第一阶段独立重建高质量字形结构，避免非文本区域干扰；第二阶段以该结构为条件引导整体图像超分，从而在保留笔画精度的同时实现背景与文本的和谐融合。

| 字段 | 内容 |
|------|------|
| 中文题名 | 先恢复文本，后增强图像：字形结构引导的两阶段场景文本图像超分辨率 |
| 英文题名 | Restore Text First, Enhance Image Later: Two-Stage Scene Text Image Super-Resolution with Glyph Structure Guidance |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.21590) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TIGER (Text–Image Guided supEr-Resolution) |
| Dataset | Real-CE, UZ-ST |

> [!tip] 效果简介
> - Real-CE (×4) 上，OCR-A 67.3% vs 64.7% (TADiSR) (+2.6%)；PSNR / SSIM / LPIPS / DISTS / FID 24.12 / 0.839 / 0.164 / 0.125 / 38.72 vs 23.83 / 0.790 / 0.286 / 0.154 / 44.42 (TADiSR) (+0.29 / +0.049 / -0.122 / -0.029 / -5.70)。
> - UZ-ST (Avg.) 上，OCR-A 43.0% vs 36.6% (TADiSR) (+6.4%)；PSNR / SSIM / LPIPS / DISTS / FID 25.48 / 0.830 / 0.196 / 0.156 / 20.01 vs 24.61 / 0.796 / 0.203 / 0.160 / 36.61 (TADiSR) (+0.87 / +0.034 / -0.007 / -0.004 / -16.60)。

## 概要

场景文本图像超分辨率（Scene Text Image Super-Resolution, STISR）面临一个根本性困境：通用图像超分模型（如 **Real-ESRGAN** (Zhang et al., ICCV 2021)、**SeeSR** (Wang et al., CVPR 2024)）追求整体视觉质量，却容易扭曲文字的字形结构；而文本专用超分模型（如 **DiffTSR** (Zhang et al., CVPR 2024)、**TADiSR**）虽提升了文本可读性，却常引入背景不一致或块效应。**现有方法无法同时兼顾文本可读性与图像视觉质量，二者形成不可调和的折衷。**

针对这一瓶颈，本文提出 **TIGER（Text–Image Guided supEr-Resolution）**，一种“先恢复文本，后增强图像”的两阶段框架。其核心调控机制在于**将字形结构恢复与图像增强显式解耦**：第一阶段在文本区域内独立重建精确的字形结构，避免非文本区域干扰；第二阶段以恢复的字形掩模作为强结构约束，引导全图超分，从而在保留笔画精度的同时实现文本与背景的和谐融合。

主要结果如下：
- 在 **Real-CE**（×4）上，TIGER 的 OCR 准确率（OCR-A）达到 67.3%，比最强基线 **TADiSR** 高出 2.6 个百分点；图像质量指标全面领先（PSNR +0.29, SSIM +0.049, LPIPS -0.122, FID -5.70）（Table 2）。
- 在更具挑战的 **UZ-ST** 数据集上，TIGER 的 OCR-A 达到 43.0%，比 TADiSR 高出 6.4 个百分点，同时 FID 大幅降低 16.60（Table 2）。
- 消融实验证实，TIGER 的文本恢复流水线显著优于标准字体掩模、SAM-TS 提取掩模或常规扩散模型生成掩模等替代方案，OCR-A 提升超过 8 个百分点（Table 6）；即使输入随机 OCR 文本，方法仍保持高精度，表明第一阶段从低分辨率图像本身恢复字形结构，对 OCR 依赖有限（Table 10）。

在方法谱系上，TIGER 区别于单阶段联合生成的范式，开创性地将文本结构显式建模为可控制的中间表示，并以此驱动全局图像增强，为场景文本超分辨率提供了一条“结构优先、视觉随后”的新路径。



场景文本图像超分辨率（Scene Text Image Super-Resolution, STISR）面临一个根本性的两难困境：**文本可读性与图像视觉质量难以兼得**。通用图像超分模型（如 **Real-ESRGAN** (Zhang et al., ICCV 2021)、**HAT**、**SeeSR** (Wang et al., CVPR 2024) 等）在提升整体视觉质量的同时，往往扭曲字形结构，导致笔画粘连、断裂或变形；而专为文本设计的超分方法（如 **MARCONet**、**DiffTSR** (Zhang et al., CVPR 2024)、**TADiSR**）虽能改善字符识别准确率，却常引入背景不一致、块效应或伪影，使文本与周围场景产生割裂感。这一折衷的根源在于：**现有方法将文本恢复与图像增强耦合在单一阶段中处理**，非文本区域的干扰信息不可避免地渗入文本重建过程，反之亦然。

从数据集角度看，现有基准同样存在结构性缺陷。TextZoom 缺乏中文场景，CTR 不支持多行文本，而 Real-CE 的退化程度较为温和，无法充分检验方法在极端低质场景下的鲁棒性（见表 1）。这导致已有工作的评估覆盖面有限，难以反映真实世界应用中从严重退化图像恢复可读文本的挑战。

针对上述瓶颈，本文提出 **TIGER（Text–Image Guided supEr-Resolution）**，核心动机在于：**将字形结构恢复与图像增强显式解耦**，以“先恢复文本，后增强图像”的两阶段范式打破单阶段联合处理的固有局限。第一阶段独立重建高保真的文本字形结构，避免非文本区域的干扰；第二阶段以恢复的精确字形掩模作为强结构约束，引导整体图像超分，从而在保留笔画精度的同时实现文本与背景的和谐融合。这一设计从因果机制上切断了文本扭曲与背景伪影之间的相互干扰路径，为场景文本超分辨率提供了新的思路。



## 核心方法与创新机理

TIGER 的核心创新在于将场景文本图像超分辨率重新定义为 **“文本优先、图像随后”的两阶段解耦范式**，以此打破现有方法中文本可读性与图像视觉质量不可兼得的折衷瓶颈。与单阶段联合处理文本与背景的主流方案相比，TIGER 在四个关键维度上实现了结构性改变。

### 1. 框架范式：从单阶段联合生成到两阶段解耦

现有方法——无论是通用图像超分模型（如 **Real-ESRGAN**，Zhang et al., ICCV 2021；**SeeSR**，Wang et al., CVPR 2024）还是文本专用超分模型（如 **DiffTSR**，Zhang et al., CVPR 2024；**TADiSR**）——均采用单阶段联合生成策略，文本与背景在同一个前向过程中被同时处理。这种设计导致一个根本性矛盾：通用模型在增强图像时容易扭曲字形结构，而文本专用模型则因过度聚焦文字区域而引入背景不一致或块效应。

TIGER 通过显式解耦解决了这一矛盾（Fig. 2, Sec. 3.1）：
- **第一阶段（文本恢复）**：独立于背景，仅从低分辨率图像的文本区域重建高保真字形结构，避免非文本区域的干扰。
- **第二阶段（图像增强）**：以第一阶段恢复的精确字形掩模为条件，引导整幅图像的超分辨率重建，实现文本与背景的和谐融合。

这一解耦策略的因果逻辑在于：**字形结构的恢复是一个精细的局部任务，需要专注的建模能力；而图像整体增强是一个全局任务，需要上下文一致性。将两者分离，使每个阶段都能针对各自的目标进行优化，而非在单一模型中相互妥协。**

### 2. 文本结构表示：从隐式条件到显式字形掩模

基线方法通常通过隐式交叉注意力机制将文本信息注入生成过程，或对超分结果进行后处理提取文本结构。这种隐式表示难以精确约束生成过程中的字形几何形态。

TIGER 的关键改变在于 **生成显式的高保真文本掩模**（二元结构图），并将其作为第二阶段 ControlNet 的强结构约束（Sec. 3.2, Sec. 3.3）。该掩模精确刻画了每个文字的位置、笔画粗细和结构轮廓，为图像增强阶段提供了确定性的空间引导。消融实验证实了这一设计的决定性作用：当使用空掩模引导时，OCR-A 从 67.3% 骤降至 59.5%（Sec. 5.3），表明文本结构信息是性能的核心驱动力。

### 3. 训练策略：从纯合成数据到混合-微调两阶段训练

现有方法通常仅在合成退化数据上训练，难以泛化至真实世界的复杂退化。TIGER 针对两阶段框架设计了差异化的训练策略（Sec. 3.2, Sec. 5.1）：
- **第一阶段**：先使用混合合成与真实数据训练，使文本恢复模型适应真实退化分布；随后仅用合成数据微调，强化字形结构的精确重建能力。
- **第二阶段**：基于 Stable Diffusion 3.5 的 ControlNet 架构，固定 VAE 编码器/解码器，仅训练 ControlNet 的可学习副本。

这一策略有效提升了文本掩模在真实场景下的质量，尤其针对严重退化图像（Sec. 5.3, Table 4）。

### 4. 图像增强方式：从无条件生成到字形掩模条件引导

基线扩散超分方法（如 DiffBIR、OSEDiff、DreamClear）通常在无条件或仅基于文本嵌入的条件下进行去噪生成，缺乏对文本区域的精确空间约束。TIGER 在第二阶段引入 **以文本掩模为条件的 ControlNet 引导超分**（Sec. 3.3, Eq. (4)）：

$$\hat{z}_{H} = z_{L} - \sigma_{t} \epsilon_{\phi} \big( z_{L}, \hat{z}_{m}, t, c_{Null} \big)$$

其中 $\hat{z}_{m}$ 为第一阶段恢复的文本掩模潜在表示，$z_{L}$ 为低分辨率图像的潜在表示。ControlNet 以 $\hat{z}_{m}$ 作为空间控制信号，在指定时间步对 $z_{L}$ 进行单步去噪，使生成过程在保留背景自然性的同时，严格遵循文本区域的结构约束。训练损失由图像重建损失（MSE + LPIPS）和边缘损失（Sobel 算子提取）加权组成（Eq. (5)–(7)），后者专门强化字形边缘的保真度。

### 创新点的因果链条

上述四个改变槽位构成了一个完整的因果链条：**解耦的框架范式**使得文本恢复与图像增强可以独立优化；**显式的字形掩模**为增强阶段提供了可操作的强约束；**混合-微调训练策略**确保了掩模在真实退化下的质量；**ControlNet 条件引导**则将结构约束精确地注入生成过程。这一链条最终在 Real-CE 和 UZ-ST 两个基准上实现了图像质量与文本准确率的双重最优（Table 2, Table 3），OCR-A 分别比最强基线 TADiSR 高出 2.6% 和 6.4%。



TIGER 采用“文本优先、图像随后”的两阶段解耦范式，将场景文本图像超分辨率拆分为**文本恢复阶段**与**图像增强阶段**，以突破现有方法中文本可读性与背景视觉质量不可兼得的瓶颈（Fig. 2）。

![[assets/figures/papers/paper_list_l2581_https_arxiv_org_abs_2510_21590/figures/003_Figure_2.jpg]]
*Figure 2: The framework of TIGER, which includes the Text Restoration stage (stage 1) and the Image Enhancement stage (stage 2). Stage 1 recover accurate glyph structures from text regions. Stage 2 uses them to guide full-image restoration for coherent text and background*

**阶段一：文本恢复。** 输入低分辨率图像 $x_L \in \mathbb{R}^{H \times W \times C}$，首先通过文本检测与 OCR 模块定位并识别文本区域及其语义内容。随后，裁剪出的文本区域经 VAE 编码器映射至潜在空间，送入基于扩散模型的 UNet 去噪网络。该网络以 LR 潜在嵌入和 OCR 文本嵌入 $c_{te}$ 为条件，通过多步迭代去噪，并行输出 RGB 文本重建与二值字形掩模的潜在表示。掩模由 VAE 解码器还原至像素空间，形成高保真文本结构图 $\hat{x}_m$。此阶段的核心设计在于：将文本结构提取从全局图像中剥离，避免非文本区域干扰，确保笔画几何的精确恢复。

**阶段二：图像增强。** 以阶段一生成的文本掩模 $\hat{x}_m$ 作为强结构约束，引导全图超分。具体而言，LR 图像与文本掩模分别经 VAE 编码得到潜在表示 $z_L$ 和 $\hat{z}_m$，共同输入 ControlNet 网络。ControlNet 在指定时间步 $t$ 对 $z_L$ 执行单步去噪，更新公式为：

$$\hat{z}_H = z_L - \sigma_t \epsilon_\phi(z_L, \hat{z}_m, t, c_{Null})$$

其中 $c_{Null}$ 为空文本嵌入，$\epsilon_\phi$ 为 ControlNet 预测的噪声。去噪后的潜在表示 $\hat{z}_H$ 经 VAE 解码器还原为最终高分辨率图像 $\hat{x}_H$。该阶段以恢复的字形掩模为条件，使超分过程在保留笔画精度的同时，实现文本与背景的和谐融合，避免块效应或纹理不一致。

**数据流与模块关系。** 两阶段间通过文本掩模 $\hat{x}_m$ 实现信息传递：阶段一输出的掩模既是文本结构的显式表征，又是阶段二 ControlNet 的控制条件。训练策略上，阶段一先混合合成数据与真实数据训练，再仅用合成数据微调，以提升对真实世界退化的鲁棒性；阶段二则采用重建损失（MSE + LPIPS）与边缘损失（Sobel 算子）联合监督，强化字形边界。

### 补充图表

![[assets/figures/papers/paper_list_l2581_https_arxiv_org_abs_2510_21590/figures/001_Figure_1.jpg]]
*Figure 1: We present TIGER (Text–Image Guided supEr-Resolution), a novel framework for scene text super-resolution. Its ‘text-first, image-later’ paradigm ensures accurate glyph restoration and consistently high overall image fidelity and visual quality*



TIGER 将场景文本超分辨率分解为两个顺序执行的阶段，每个阶段承担明确的功能边界。以下逐一拆解关键模块及其数学形式。

### 阶段一：文本恢复（Text Restoration）

该阶段的目标是从低分辨率（LR）图像的文本区域中重建高保真的字形结构，输出包含 RGB 文本图像和对应的二值文本掩模（glyph mask）。其核心由四个模块串联构成：

1. **文本检测与 OCR 模块**：定位 LR 图像中的文本区域并识别文本内容，为后续扩散模型提供文本条件嵌入 $\pmb{c}_{te}$。
2. **VAE 编码器**：将裁剪后的文本区域编码到潜在空间，得到 LR 潜在表示 $\tilde{z}_L$。
3. **UNet 去噪网络**：以 $\tilde{z}_L$ 和 $\pmb{c}_{te}$ 为条件，通过迭代去噪同时预测 RGB 文本潜在表示和文本掩模潜在表示。该网络采用 IDM（Instruction-based Diffusion Model）架构。
4. **VAE 解码器**：将去噪后的掩模潜在表示解码回像素空间，得到文本掩模 $\hat{x}_m$。

阶段一的训练由两项损失加权驱动：

$$
\mathcal{L} = \lambda_{td} \mathcal{L}_{td} + \lambda_{Seg} \mathcal{L}_{Seg} \tag{1}
$$

**文本控制扩散损失** $\mathcal{L}_{td}$ 为标准扩散去噪损失，条件包含 LR 潜在变量和文本嵌入：

$$
\mathcal{L}_{\epsilon} = \mathbb{E}_{z_0, \tilde{z}_L, c_{te}, t, \epsilon \sim \mathcal{N}(0,1)} \left[ \lVert \epsilon - \epsilon_{\theta}(z_t, \tilde{z}_L, \pmb{c}_{te}, t) \rVert_2^2 \right] \tag{2}
$$

其中 $z_0$ 为干净潜在表示，$z_t$ 为加噪后的潜在表示，$\epsilon_{\theta}$ 为 UNet 预测的噪声。

**分割导向损失** $\mathcal{L}_{Seg}$ 用于监督文本掩模的生成质量，融合 MSE、Focal Loss 和 Dice Loss 三种损失：

$$
\mathcal{L}_{Seg} = \| \boldsymbol{x}_{0}^{\prime m} - \boldsymbol{x}_{0}^{m} \|_2^2 + \lambda_{Focal} \mathrm{FocalLoss}(\boldsymbol{x}_{0}^{\prime m}, \boldsymbol{x}_{0}^{m}) + \lambda_{Dice} \mathrm{DiceLoss}(\boldsymbol{x}_{0}^{\prime m}, \boldsymbol{x}_{0}^{m}) \tag{3}
$$

其中 $\boldsymbol{x}_{0}^{\prime m}$ 为预测的文本掩模，$\boldsymbol{x}_{0}^{m}$ 为真实文本掩模。MSE 项保证像素级精度，Focal Loss 缓解前景-背景类别不平衡，Dice Loss 直接优化掩模区域的重叠度。

### 阶段二：图像增强（Image Enhancement）

阶段二以阶段一输出的文本掩模 $\hat{x}_m$ 为结构约束，对整幅 LR 图像进行超分辨率增强。核心模块为 **ControlNet 网络**，它接收两个条件输入：LR 图像的潜在表示 $z_L$ 和文本掩模的潜在表示 $\hat{z}_m$。ControlNet 在指定时间步 $t$ 执行单步去噪，使用空文本嵌入 $c_{Null}$ 以避免额外语义干扰：

$$
\hat{z}_H = z_L - \sigma_t \epsilon_{\phi} \big( z_L, \hat{z}_m, t, c_{Null} \big) \tag{4}
$$

其中 $\epsilon_{\phi}$ 为 ControlNet 预测的噪声，$\sigma_t$ 为当前时间步的噪声强度。去噪后的潜在表示 $\hat{z}_H$ 经 VAE 解码器还原为最终高分辨率图像 $\hat{x}_H$。

阶段二的训练损失由图像重建损失和边缘损失组成：

**图像重建损失** $\mathcal{L}_{img}$ 为 MSE 与 LPIPS 的加权和：

$$
\mathcal{L}_{img} = \lambda_{l2} \| x_H - \hat{x}_H \|_2^2 + \lambda_{LPIPS} \mathrm{LPIPS}(x_H, \hat{x}_H) \tag{5}
$$

**边缘损失** $\mathcal{L}_{edge}$ 使用 Sobel 算子提取图像边缘，显式强化字形结构的锐度：

$$
\mathcal{L}_{edge} = \| \mathrm{Sobel}(x_H) - \mathrm{Sobel}(\hat{x}_H) \|_2^2 \tag{6}
$$

阶段二总损失为两者加权：

$$
\mathcal{L} = \mathcal{L}_{img} + \lambda_{edge} \mathcal{L}_{edge} \tag{7}
$$

### 设计要点

- **解耦训练策略**：阶段一先在混合合成与真实数据上训练，再用纯合成数据微调，以提升对真实世界退化的文本掩模恢复质量（见 Sec. 3.2）。
- **ControlNet 的 tile-based 推理**：阶段二基于 Stable Diffusion 3.5，采用分块推理策略处理高分辨率输出，保证显存效率（见 Sec. 5.1）。
- **文本掩模作为显式结构约束**：区别于隐式交叉注意力或后处理提取，TIGER 显式生成高保真二值掩模，使阶段二的超分过程有明确的空间引导信号。消融实验证实，空掩模引导使 OCR-A 从 67.3% 降至 59.5%，验证了该约束的关键性（见 Sec. 5.3）。



## 实验与关键发现

### 实验设置与基准

TIGER 在两阶段训练中采用差异化策略：第一阶段使用 IDM 架构，在裁剪的文本区域上联合优化分割损失与重建损失；第二阶段基于 Stable Diffusion 3.5，采用分块推理策略以处理高分辨率输入。为保证公平比较，所有对比方法的预训练模型均在 Real-CE 和 UZ-ST 训练集上微调——其中 MARCONet 和 DiffTSR 的输出与 HAT 的结果融合以模拟真实部署场景。

评估指标覆盖图像质量与文本准确率两个维度：图像质量采用 PSNR、SSIM、LPIPS、DISTS、FID 五项指标；文本准确率采用基于 Levenshtein 距离的 OCR-A 度量（详见 Eq. (8)），该指标同时惩罚识别错误与多余/缺失字符。

### 主实验结果

**整体性能对比。** Table 2 汇总了 Real-CE（×4）和 UZ-ST（平均）两个基准上的全面对比。TIGER 在所有六项指标上均达到最优：在 Real-CE 上，OCR-A 达到 67.3%，较最强基线 TADiSR 的 64.7% 提升 2.6 个百分点；图像质量方面，LPIPS 从 0.286 降至 0.164，FID 从 44.42 降至 38.72，降幅分别达 42.7% 和 12.8%。在退化更严重的 UZ-ST 上，TIGER 的 OCR-A 优势扩大至 6.4 个百分点（43.0% vs. 36.6%），FID 从 36.61 骤降至 20.01，降幅超过 45%，表明两阶段解耦策略在极端退化场景下具有更强的鲁棒性。

**文本区域专项评估。** Table 3 聚焦于文本区域的图像质量与 OCR-A 相对 LR 的提升量（ΔOCR-A）。TIGER 在 Real-CE 上实现 ΔOCR-A +2.5%，在 UZ-ST 上实现 +1.3%，均为正增益且优于所有基线。值得注意的是，部分通用超分方法（如 Real-ESRGAN、HAT）在文本区域出现负的 ΔOCR-A，即超分后文本可读性反而低于 LR 输入，印证了“通用超分扭曲字形结构”这一核心瓶颈。

**定性对比。** Figure 4 的可视化结果表明，基于 GAN 的方法（Real-ESRGAN、HAT）倾向于产生模糊或扭曲的笔画，扩散模型基线（SeeSR、DiffBIR 等）虽能生成更自然的纹理，但文本区域常出现笔画断裂或伪影。TIGER 凭借显式的字形结构约束，在保持笔画精度的同时实现了文本与背景的和谐融合。

### 消融实验

**文本掩模引导的有效性。** Table 6 在固定第二阶段为基线的条件下，系统比较了四种文本掩模来源对最终 OCR-A 的影响：
- **空掩模引导**：OCR-A 从 67.3% 骤降至 59.5%，证实文本结构信息是第二阶段超分的关键条件。
- **标准字体渲染**：使用标准字体在检测位置渲染的掩模，OCR-A 进一步降至 55.3%，说明仅靠位置信息而缺乏真实字形纹理无法有效引导超分。
- **SAM-TS 提取**：从 LR 图像直接提取退化结构的掩模，OCR-A 为 57.9%，虽优于标准字体但仍远低于 TIGER 的 67.1%，表明“恢复优于提取”——第一阶段主动重建字形结构比被动提取退化结构更为有效。
- **常规 LDM 生成**：使用未针对文本优化的潜扩散模型直接生成掩模，性能同样显著低于 TIGER 流水线。

Figure 5 的定性消融结果直观展示了不同掩模策略对最终输出文本质量的影响：TIGER 恢复的掩模保持了清晰的笔画边界和正确的字形拓扑，而替代方案普遍存在笔画粘连、断裂或位置偏移。

![[assets/figures/papers/paper_list_l2581_https_arxiv_org_abs_2510_21590/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative Results of Ablation Study with stage 2 fixed as the baseline*

**OCR 依赖度分析。** Table 5 和 Table 10 检验了第一阶段对 OCR 识别结果的依赖程度。当 OCR 输入为空文本时，方法仍能保持较高精度；即使在 100% 随机 OCR 输出的极端条件下，TIGER 仍优于 TADiSR。这一结果表明，第一阶段主要从 LR 图像的视觉特征中恢复字形结构，对 OCR 语义信息的依赖有限，从而降低了对 OCR 引擎性能的敏感度。

**训练策略消融。** 第一阶段的“先混合合成与真实数据、后仅用合成数据微调”的两阶段训练策略被证实对真实世界退化场景下的文本掩模质量有显著提升（Sec. 3.2），该设计缓解了真实数据标注不足的问题，同时避免了合成数据分布偏移带来的过拟合风险。

### 数据集有效性验证

Table 4 验证了 UZ-ST 数据集的价值：在 Real-CE 上训练的模型直接迁移至 UZ-ST 时性能显著下降，而在 UZ-ST 上微调后 OCR-A 明显回升，证明 UZ-ST 所引入的极端退化分布对推动场景文本超分辨率研究具有不可替代的作用。

![[assets/figures/papers/paper_list_l2581_https_arxiv_org_abs_2510_21590/figures/009_Table_4.jpg]]
*Table 4: Validation on the effectiveness of UZ-ST. Finetuning improves OCR-A, proving effectiveness*

### 失败模式与局限性

尽管 TIGER 在整体指标上表现优异，但仍存在以下局限：
1. **推理效率**：第一阶段为标准扩散模型，需多步采样，推理速度慢于单步方法（如 OSEDiff、DreamClear），制约实时应用场景。
2. **OCR 错误传播**：在严重退化导致 OCR 检测遗漏或识别完全错误的极端情况下，恢复的字形结构可能偏离真实语义，尽管消融实验表明该影响有限，但未完全消除。
3. **多语言泛化**：当前验证以中文场景为主，对复杂多语言混合排版（如阿拉伯文、印地语等书写系统差异较大的文字）的支持尚待系统考察。

### 补充图表

![[assets/figures/papers/paper_list_l2581_https_arxiv_org_abs_2510_21590/figures/005_Table_2.jpg]]
*Table 2: Evaluation results on image quality and text accuracy. Numbers in bold indicate the best performance. TIGER performs best*

![[assets/figures/papers/paper_list_l2581_https_arxiv_org_abs_2510_21590/figures/006_Table_3.jpg]]
*Table 3: Evaluation of image quality on text regions and text accuracy compared to LR (∆ OCR-A). TIGER achieves the best performance*

![[assets/figures/papers/paper_list_l2581_https_arxiv_org_abs_2510_21590/figures/010_Table_6.jpg]]
*Table 6: Ablation study on Real-CE with stage 2 fixed as the baseline. From top to bottom, we compare the performance of using text masks rendered with a standard font, extracted using SAM-TS, reconstructed with latent diffusion model conditioned on LR, and reconstructed with our text restoration pipeline. Our pipeline faithfully restores glyph structures, yielding the highest accuracy*

![[assets/figures/papers/paper_list_l2581_https_arxiv_org_abs_2510_21590/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative Evaluation on Real-CE and UZ-ST*

![[assets/figures/papers/paper_list_l2581_https_arxiv_org_abs_2510_21590/figures/011_Table_5.jpg]]
*Table 5: Ablation on OCR prediction. The model remains strong with null or random OCR text, indicating limited reliance on OCR*

![[assets/figures/papers/paper_list_l2581_https_arxiv_org_abs_2510_21590/figures/015_Table_10.jpg]]
*Table 10: Ablation on the effect of stochastic OCR outputs on the performance of our method. The performance gains as the randomness of the OCR output drops. Even under 100% random OCR output, our method still outperforms TADiSR, proving low reliance on OCR*

![[assets/figures/papers/paper_list_l2581_https_arxiv_org_abs_2510_21590/figures/004_Figure_3.jpg]]
*Figure 3: Overview of UZ-ST (UltraZoom-Scene Text). (a) Real-CE LRs show only mild degradation (red box), while UZ-ST LRs exhibit stronger degradation (red box), enabling a more comprehensive evaluation. (b) Coarse-to-fine alignment: images are sorted by focal length, each warped to the next higher-focal neighbor using an estimated homography matrix, then refined to the 200 mm GT*

![[assets/figures/papers/paper_list_l2581_https_arxiv_org_abs_2510_21590/figures/014_Table_9.jpg]]
*Table 9: Efficiency analysis*



## 定位与知识库关联

### 1. 核心瓶颈与范式转换

现有场景文本图像超分辨率（STISR）方法面临一个根本性折衷：**通用图像超分模型**（如 **Real-ESRGAN** (Zhang et al., ICCV 2021)、**HAT**、扩散模型类的 **SeeSR** (Wang et al., CVPR 2024)、**SupIR**、**DiffBIR**、**OSEDiff**、**DreamClear**、**TSD-SR**、**DiT4SR**）虽能生成视觉上自然的背景，却容易扭曲或模糊字形结构，导致文本不可读；而**文本专用超分模型**（如 **MARCONet**、**DiffTSR** (Zhang et al., CVPR 2024)、**TADiSR**）虽提升了字符识别准确率，却常引入背景不一致、块效应或纹理失真，牺牲了整体图像质量。这两类方法均采用**单阶段联合生成**范式，试图在同一个前向过程中同时解决文本可读性与图像保真度，因而不可避免地陷入此消彼长的困境。

TIGER 的核心突破在于**将字形结构恢复与图像增强显式解耦**，提出了“文本优先、图像随后”（text-first, image-later）的两阶段范式。这一设计将因果控制点从“隐式约束”转变为“显式结构引导”：第一阶段独立重建高保真文本掩模，避免非文本区域的干扰；第二阶段以该掩模为强结构条件，通过 ControlNet 引导全局超分，实现笔画精度与背景和谐的兼顾。

### 2. 关键设计差异与知识增量

与现有方法相比，TIGER 在以下四个关键维度上做出了实质性改变：

| 设计维度 | 现有方法 | TIGER 方案 | 证据锚点 |
|---------|---------|-----------|---------|
| **框架范式** | 单阶段联合生成（文本与图像同时处理） | 两阶段解耦：文本恢复阶段 + 图像增强阶段 | Sec. 1, Sec. 3.1, Fig. 2 |
| **文本结构表示** | 隐式交叉注意力或后处理提取 | 显式生成高保真文本掩模（二元结构图） | Sec. 3.2, Sec. 5.3 |
| **训练数据使用** | 仅用合成数据训练 | 两阶段策略：先混合合成与真实数据，后仅用合成数据微调 | Sec. 3.2, Sec. 5.1 |
| **图像增强方式** | 无条件或基于文本嵌入的生成 | 以文本掩模为条件的 ControlNet 引导超分 | Sec. 3.3, Eq. (4) |

其中最具区分度的设计是**文本掩模的生成方式**。消融实验（Table 6, Sec. 5.3）系统比较了四种掩模来源：标准字体渲染、SAM-TS 提取、常规 LDM 生成、以及 TIGER 的文本恢复流水线。结果显示，TIGER 的恢复流水线使 OCR-A 达到 67.1%，比 SAM-TS 提取（57.9%）和标准字体（55.3%）分别高出 9.2 和 11.8 个百分点。这表明，仅靠退化图像中提取的粗糙结构或理想字体模板均不足以提供有效的超分引导——**必须通过专门的生成模型从 LR 输入中恢复精确的字形结构**。

### 3. 方法适用边界与局限

尽管 TIGER 在 Real-CE 和 UZ-ST 两个基准上全面超越现有方法，其设计仍存在明确的适用边界：

1. **推理效率瓶颈**：第一阶段采用标准扩散模型，需要多步采样完成文本恢复，推理速度慢于单步方法（如 OSEDiff 等基于蒸馏的方案），制约了实时应用场景的部署。Table 9 的效率分析提供了具体数据支撑，但本报告未获取到详细数值，需读者自行查阅原文。

2. **OCR 依赖的风险传播**：文本恢复阶段依赖 OCR 模块进行文本检测与识别。在严重退化场景下，OCR 的错误（漏检、误识别）可能传播到后续阶段。Table 5 和 Table 10 的消融实验表明，即使输入空文本或 100% 随机 OCR 输出，TIGER 仍优于 TADiSR，说明第一阶段主要从图像本身恢复结构，对 OCR 的依赖有限。但这一结论仅在现有测试集上成立，对于 OCR 输出完全错误且图像退化极端的边界情况，结构恢复的保真度仍需进一步验证。

3. **语言与排版泛化性未充分验证**：当前实验以中文场景为主（UZ-ST 专门补充了中文、多行文本和极端退化场景），Figure 9 展示了多语言效果，但复杂多语言混合排版（如阿拉伯文从右向左书写、印地语连字结构）的泛化能力尚待系统评估。

### 4. 开放问题与未来方向

基于 TIGER 的设计逻辑和当前局限，以下开放问题值得后续工作关注：

- **第一阶段加速**：能否将文本恢复阶段的扩散过程蒸馏为单步或轻量化模型，在保持字形恢复精度的前提下大幅提升推理速度？
- **极端退化下的鲁棒性**：当 OCR 输出完全错误时，恢复的文本结构是否会偏离真实语义？是否需要引入额外的语义校验或闭环修正机制？
- **跨书写系统泛化**：方法对非中文文字（日语、韩语）之外的其他书写系统（阿拉伯文、印地语、泰文等）的泛化能力如何？是否需要针对不同字形特征调整掩模生成策略？
- **框架可扩展性**：当前设计聚焦于“恢复已有文本”，在处理无文本区域插入新文本的需求时，该两阶段框架是否可直接扩展，还是需要引入额外的文本渲染模块？

### 5. 在知识库中的定位

TIGER 在 STISR 领域的方法谱系中占据了一个独特位置：它是**首个将文本结构恢复与图像增强显式解耦的两阶段扩散框架**。与 TADiSR（文本感知扩散超分，当前最强单阶段基线）相比，TIGER 在 Real-CE 上 OCR-A 提升 2.6%（67.3% vs. 64.7%），在 UZ-ST 上提升 6.4%（43.0% vs. 36.6%），同时在全部图像质量指标（PSNR、SSIM、LPIPS、DISTS、FID）上均取得最优。这一结果表明，**“先恢复文本，后增强图像”的范式转换**是解决文本可读性与图像质量折衷问题的有效路径，为后续工作提供了可复用的架构模板和明确的改进方向（加速第一阶段、增强 OCR 鲁棒性、拓展语言覆盖）。



## 原文 PDF

![[paperPDFs/CVPR_2026/Restore_Text_First_Enhance_Image_Later_Two_Stage_Scene_Text_Image_Super_Resolution_with_Glyph_Structure_Guidance.pdf]]
