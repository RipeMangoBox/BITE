---
title: "Beyond Skeletons: Learning Animation Directly from Driving Videos with Same2X Training Strategy"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Beyond_Skeletons_Learning_Animation_Directly_from_Driving_Videos_with_Same2X_Training_Strategy.pdf
aliases:
- BSLADFDVSTS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "直接使用原始驾驶视频像素作为驱动信号，构建由姿态线索、人脸线索和位置线索组成的结构化驱动线索三元组，并通过CueFusion DiT块注入去噪过程；同时设计Same2X训练策略，利用同身份数据的内部特征对齐跨身份表示，稳定优化并加速收敛。"
primary_logic: "原始驾驶视频像素蕴含比简化的骨架图更丰富的运动与表情信息。通过合理的线索解耦（频域滤波去除外观细节、面部区域裁剪保留表情）与注入机制（自适应层归一化+门控残差）可以避免姿态估计的误差累积，并利用同身份数据的特征空间作为跨身份学习的内部指南，从而实现更鲁棒、更高效的人体动画生成。"
claims:
- "骨架图驱动的动画在复杂姿势下存在严重伪影，而DirectAnimator使用原始像素驱动可获得更真实、更准确的结果（图1左侧定性对比）。"
- "Same2X训练策略使跨身份（Stage 2）训练达到相同损失水平的速度提升了6.7倍（图1右侧训练曲线）。"
- "在TikTok和Unseen测试集上，DirectAnimator在FID、SSIM、PSNR、LPIPS等主要指标上全面超越现有方法（表1），达到最佳性能。"
- "DirectAnimator在姿态关键点一致性（PLC）和面部关键点一致性（FLC）两个几何度量上同样取得了最低误差（表2），证明其更准确地跟随驱动视频的姿态与表情。"
---

# Beyond Skeletons: Learning Animation Directly from Driving Videos with Same2X Training Strategy

> [!tip] 核心洞察
> 原始驾驶视频像素蕴含比简化的骨架图更丰富的运动与表情信息。通过合理的线索解耦（频域滤波去除外观细节、面部区域裁剪保留表情）与注入机制（自适应层归一化+门控残差）可以避免姿态估计的误差累积，并利用同身份数据的特征空间作为跨身份学习的内部指南，从而实现更鲁棒、更高效的人体动画生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 超越骨架：利用Same2X训练策略直接从驾驶视频学习动画 |
| 英文题名 | Beyond Skeletons: Learning Animation Directly from Driving Videos with Same2X Training Strategy |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=HdEpZE3wFa); [Project](https://directanimator.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DirectAnimator |
| Dataset | TikTok, Unseen |

> [!tip] 效果简介
> - TikTok 上，FID↓ 为 25.87，对比 30.39 (StableAnimator)，变化 -4.52。
> - TikTok 上，SSIM↑ 为 0.806，对比 0.749 (StableAnimator)，变化 +0.057。
> - TikTok 上，FVD↓ 为 142.60，对比 140.62 (StableAnimator, best baseline)，变化 +1.98 (worse)。

## 概述

现有人体图像动画方法普遍依赖姿态估计器（如OpenPose/DWPose）抽取骨架图作为驱动信号，这类中间表示在遮挡、复杂体态或自遮挡场景下极易产生前后混淆、手部错位、肢体缺失等错误，进而导致生成伪影与身份保持困难。本文提出**DirectAnimator**，直接以原始驾驶视频像素为驱动源，规避姿态估计的误差累积。为此，方法设计了由姿态线索（Pose Cue）、人脸线索（Face Cue）和位置线索（Location Cue）组成的结构化驱动线索三元组，并通过**CueFusion DiT块**（基于自适应层归一化与门控残差连接）将这些线索注入去噪过程；同时引入**Same2X训练策略**，利用同身份数据的内部特征对齐为跨身份训练提供稳定指南，显著加速收敛。在TikTok和Unseen测试集上的实验表明，DirectAnimator在FID、SSIM、PSNR、LPIPS等主流质量指标，以及姿态关键点一致性（PLC）和面部关键点一致性（FLC）两个几何度量上均全面超越StableAnimator、MimicMotion等现有最优骨架驱动方法。图1的定性对比显示，原始像素驱动在复杂运动下大幅减少伪影；训练曲线则表明Same2X策略使跨身份阶段达到相同损失水平的速度提升约6.7倍。消融研究证实了驱动线索三元组各组分、CueFusion注入机制以及Same2X对齐损失的关键作用。该方法将人体动画生成从显式姿态估计范式转向直接的原始视频驱动，为后续研究开辟了新的技术路径。

## 背景与动机

人体图像动画的目标是根据参考人物图像和一段驱动视频，生成与驱动运动一致且保持参考身份的视频。现有主导范式依赖姿态估计器（如 OpenPose、DWPose）从驱动视频中提取 2D 骨架图、DensePose 或 SMPL 等中间表示作为驱动信号。这类骨架驱动信号在遮挡、复杂体态或自遮挡下极易出错——常见故障模式包括前-后混淆、手部错位、肢体缺失等——这些误差直接传递到生成过程，导致明显的伪影以及难以维持的参考身份一致性（Figure 1 左侧对比）。即便采用关键点置信度、ReferenceNet 等增强设计（如 MimicMotion、AnimateAnyone、StableAnimator），骨架估计的质量瓶颈依然是生成稳定性和真实感的核心短板。

这一瓶颈的本质在于：人为简化的骨架图无法充分表达原始视频像素中蕴含的丰富运动、表情与交互信息。在严重遮挡或复杂姿态下，丢失的细粒度线索迫使生成模型在缺失信息处“猜测”，进而产生结构错乱和身份漂移。与此同时，现有基于 DiT 的人体动画方法通常将驱动特征简单拼接或通过交叉注意力注入，难以有效保证驱动控制的稳定性和位姿对齐的精度。另一方面，跨身份训练（参考与驱动为不同人物）普遍采用标准的去噪损失，缺乏对同一身份特征空间的显式利用，导致训练效率低下和收敛缓慢。

针对上述缺口，本文提出 DirectAnimator，其核心动机是用**原始驾驶视频像素直接替代骨架图作为驱动信号**，从而绕过姿态估计器的误差累积。通过对原始像素进行结构化解耦——提取去除外观细节的姿态线索（Pose Cue）、保留表情的面部线索（Face Cue）和实现空间对齐的位置线索（Location Cue）——构成“驱动线索三元组”，并设计 CueFusion DiT 块以自适应层归一化和门控残差的方式将其注入去噪过程，实现对运动和表情的可靠控制。进一步，Same2X 训练策略利用同一身份数据的内部特征对齐来引导跨身份训练，显著加速收敛（达到相同损失水平的速度提升 6.7 倍，Figure 1 右侧训练曲线），并提高跨身份泛化能力。这些设计共同构成了从“骨架驱动”到“像素驱动”的范式转换，旨在实现更鲁棒、更高效的人体动画生成。

## 核心创新

DirectAnimator 的核心创新在于从根本上突破了人体图像动画领域对显式姿态估计器的依赖，以**原始驾驶视频像素**替代传统骨架图作为驱动信号，构建了一套从驱动表示、注入机制到训练策略的系统性革新链条。该创新链条直接瞄准了现有骨架驱动方法在遮挡、自遮挡及复杂体态下的根本瓶颈：姿态估计器（如 OpenPose/DWPose）输出的 2D 骨架图存在前-后混淆、手部错位、肢体缺失等系统性错误，这些中间表示的误差会不可逆地传递至生成网络，造成严重的生成伪影与身份漂移。DirectAnimator 通过以下三个关键 **changed slots** 绕开了这一误差链条。

### 1. 驱动信号范式转换：从骨架图到结构化 **驱动线索三元组** (Driving Cue Triplet)

现有方法普遍将姿态估计器输出的骨架图（或 DensePose/SMPL）作为唯一的驱动信号，而骨架图本身是对运动信息的极度压缩和噪声敏感的中间表示。DirectAnimator 提出直接从原始驾驶视频像素中提取**姿态线索 (Pose Cue)、人脸线索 (Face Cue) 和位置线索 (Location Cue)** 组成的三元组。其核心洞察是：原始像素蕴含远比骨架图更丰富、更鲁棒的运动与表情信息，但需通过合理的表示解耦来剥离外观细节、保留关键可控信息。

- **姿态线索**：利用 Grounded SAM 对驾驶视频进行前景分割，并在频域施加低通滤波以抑制纹理、衣物褶皱等高频外观细节，同时保留人体轮廓和肢体结构的大尺度运动信息（Figure 2a, Section 3.1）。这一步本质上在用信号处理手段代替显式关键点检测，完全避免了关键点估计误差的产生。
- **人脸线索**：直接裁剪并居中对齐驾驶视频中的人脸区域（通过 InsightFace），以保留细腻的表情细节（图 3 所示）。相比从骨架图中提取稀疏面部关键点，原始人脸像素能传递更丰富的表情信息，从而在后续生成中实现更忠实的表情复现。
- **位置线索**：生成软化的人体与面部掩膜，用于空间对齐，确保生成的人体动作与驾驶视频保持位置一致性。

这一驱动表示的范式转换从根本上切断了姿态估计误差的传播路径。定性与定量证据均表明其有效性（Figure 1-left 的对比可见骨架图伪影与原始像素驱动的准确生成；Table 3 消融实验中，将姿态线索替换回骨架图导致 FID 从 27.61 显著恶化到 30.84）。

### 2. 条件注入机制革新：**CueFusion DiT 块** (CueFusion DiT Block)

骨架驱动方法通常将骨架特征与扩散模型中的特征进行直接拼接或交叉注意力注入，这些方式在处理经 3D VAE 编码后的特征时往往缺乏足够的条件控制力与稳定性。DirectAnimator 设计了专用的 **CueFusion DiT (CF-DiT) 块**（Figure 2b），在标准的 DiT 块中引入一种**时间条件化的自适应层归一化 (AdaLN) + 门控残差**的混合调制机制：

- 首先，使用时间嵌入 $e_t$ 通过 MLP 联合生成姿态线索和人脸线索各自的尺度因子 $\alpha$、偏移因子 $\beta$ 和门控因子 $\gamma$（公式 1）。
- 接着，对归一化后的线索嵌入 $e_p$ / $e_f$ 施加学习到的尺度和偏移：$e_p^M = \text{LN}(e_p) \cdot (1+\alpha_p) + \beta_p$，实现时间步感知的自适应特征调制（公式 2）。
- 最后，通过可学习的门控残差连接 $e_p^G = e_p + \gamma_p \cdot e_p^M$ 将原始线索嵌入与调制后的嵌入进行融合（公式 3），使每个 DiT 块既能接收强条件控制，又能保留原始线索信息，避免过调制导致的退化。

这种机制同时融合了 AdaLN 的灵活时间控制和残差连接的信息保持能力。消融实验（Table 5）充分证明了该设计的必要性：将 CF-DiT 块替换为直接拼接（DC Injection）或交叉注意力注入（CA Injection）分别导致 FID 恶化 3.07 和 4.69，FVD 等指标同样大幅劣化，表明简单的注入策略无法充分利用所提取的三元组线索。

### 3. 训练策略突破：**Same2X 训练策略** (Same2X Training Strategy)

人体图像动画的终极挑战在于**跨身份训练**——参考图像与驾驶视频来自不同人物时，没有成对真值可供监督，训练极不稳定且收敛缓慢。此前的方法通常在预对齐的骨架图上直接应用标准去噪损失，缺乏对跨身份特征空间的引导。

DirectAnimator 提出了 **Same2X 训练策略**，将训练分为两个阶段：

- **Stage 1（同身份预训练）**：使用同身份（Same-ID）数据训练一个教师模型，驾驶视频与参考图像共享身份特征，模型只需学习“复制”自身运动，优化简单且特征空间规整。
- **Stage 2（跨身份微调）**：使用同身份模型的内部特征作为锚点，对跨身份学生模型施加 **Same2X 对齐损失**（公式 4）。该损失最大化学生与教师在第 $D$ 个 DiT 块中对应 patch 嵌入之间的余弦相似度，迫使学生在特征空间内模仿教师模型的动力学，从而传递可靠的表征先验。同时，由于跨身份场景缺乏真实驱动线索，DirectAnimator 使用第三方模型（如 StableAnimator 生成伪姿态线索，Face-Adapter 生成伪人脸线索）来合成“伪驱动线索”作为训练输入。

Same2X 策略实现了**训练效率与质量的同步跃升**：Figure 1-right 显示，在跨身份阶段达到相同损失水平的速度提升了 **6.7 倍**；消融实验（Table 3, S8 vs Ours）表明，移除 Same2X 对齐损失后 FID 从 27.61 飙升至 32.21，身份相似度 FIS 从 0.638 急降至 0.368，验证了跨身份特征对齐的核心作用。而且，相同身份数据的内部特征比标准去噪目标提供了更稳定、更具语义意义的优化信号，这是该策略能在极少训练步数（40K 步）下超越多数需要 100K–300K 步的基线方法的关键原因（Table 1）。

这三个创新 slot 并非孤立设计，而是形成了一条因果关系闭环：**新的驱动表示（Cue Triplet）提供了丰富而鲁棒的运动/表情信号 → 精心设计的注入模块（CF-DiT）高效融合这些信号而不损伤去噪过程的稳定性 → 训练策略（Same2X）解决了跨身份场景下特征分布漂移和优化困难的根本问题**。三者共同实现了 DirectAnimator 在 FID、SSIM、PSNR、LPIPS（Table 1）以及姿态/人脸关键点一致性 PLC/FLC（Table 2）上对骨架驱动方法的全面超越，同时也将单帧预处理时间控制在可接受的 31ms 量级（Table 7），使其在推理阶段仍具竞争力。

## 整体框架

![[assets/figures/papers/iclr26_0013_HdEpZE3wFa_Beyond_Skeletons_Learning_Animation_Directly_fro/figures/004_Figure_2.jpg]]
*Figure 2: Overview of DirectAnimator. (a) We replace the skeleton maps with our proposed driving cue triplet: Pose Cue ( C _ { P o s e } ) , Face Cue ( C _ { F a c e } ) , and Location Cue ( C _ { L o c a t i o n } ) . A frozen VAE encoder maps the reference image, pose cue, and face cue into the latent space. Pose and face latents are each concatenated with their corresponding masks from the location cue. These features are then patchified and fed into the CF-DiT Block. (b) The CF-DiT Block injects pose and face cues via Adaptive LayerNorm with time-conditioned modulation, and uses gated residuals to ensure stable and controllable denoising*

DirectAnimator 彻底摒弃了传统人体动画方法对显式姿态估计器（如 OpenPose / DWPose）的依赖，改由原始驾驶视频的像素直接提取驱动信号。其整体架构如图 2 所示，核心由四个模块串联构成：**驱动线索提取**（Driving Cue Extraction）、**3D VAE 编码与分块**、**CueFusion DiT 块**以及 **Same2X 训练策略**。给定一张参考图像 $I_{\text{ref}}$ 和一段驾驶视频 $V_{\text{drv}}$，模型输出一序列动画帧，使其肢体运动与面部表情忠实跟随驾驶视频，同时保持参考图中的身份纹理。

**输入输出流**。首先，驱视频经过驱动线索提取模块，被抽象为一个结构化的**驱动线索三元组**：姿态线索 $C_{\text{Pose}}$、人脸线索 $C_{\text{Face}}$ 和位置线索 $C_{\text{Location}}$。参考图像 $I_{\text{ref}}$ 与两个视觉线索 $C_{\text{Pose}}$, $C_{\text{Face}}$ 分别由冻结的 3D VAE 编码器映射为潜变量，并与对应的掩码（由位置线索提供）拼接，随后被分块（patchify）成视觉 token 序列，送入级联的 CueFusion DiT 块中。在每个去噪步骤，姿态和人脸线索通过自适应层归一化与门控残差机制注入，控制生成内容；位置线索则以直接拼接的方式维持空间对齐。最终，去噪后的潜变量经 3D VAE 解码器恢复为像素空间的人体动画帧。

**驱动线索提取** 是为了在消除高频外观细节的同时，保留运动与表情的本质信息（见图 3）。姿态线索 $C_{\text{Pose}}$ 首先利用 Grounded SAM 分割出驾驶视频中的前景人体区域，再对前景帧施加频域低通滤波，抑制纹理、衣着褶皱等细节，仅保留肢体轮廓和整体姿态变化。人脸线索 $C_{\text{Face}}$ 通过 InsightFace 检测面部区域后，对其进行裁剪、放大和居中，从而向模型输入富含表情细节的原始面部像素，远超稀疏关键点的表达能力。位置线索 $C_{\text{Location}}$ 则依据人体和面部的分割掩码生成软化后的对齐掩码，为后续的潜变量拼接提供粗略的空间定位。

**CueFusion DiT 块** 是驱动信息注入去噪过程的控制核心（图 2b）。不同于将驱动特征直接与噪声潜变量拼接或采用交叉注意力注入，每个 CF‑DiT 块同时接收身份潜变量 token 序列与姿态/人脸线索的 patch 嵌入。首先，时间嵌入 $e_t$ 通过一个带 SiLU 激活的多层感知机生成六组调制因子——姿态/人脸各自的尺度 $\alpha_p/\alpha_f$、偏移 $\beta_p/\beta_f$ 与门控 $\gamma_p/\gamma_f$（公式 1）。随后，对线索嵌入施加时间条件化的自适应层归一化：
$$e_p^M = \text{LN}(e_p) \cdot (1+\alpha_p) + \beta_p, \quad e_f^M = \text{LN}(e_f) \cdot (1+\alpha_f) + \beta_f$$
并将调制后的嵌入经门控残差与原始嵌入融合：
$$e_p^G = e_p + \gamma_p \cdot e_p^M, \quad e_f^G = e_f + \gamma_f \cdot e_f^M$$
此设计使每个 DiT 块同时接收原始线索信息与时间条件化调制信息，从而在保证稳定去噪的同时实现对运动与表情的精细控制。位置线索则被直接拼接到潜变量上，以确保生成结果的空间对齐。

**Same2X 训练策略** 为上述框架提供了从“同身份”到“跨身份”高效泛化的训练基础（图 4）。训练分为两阶段：**第一阶段**在同身份数据上训练一个“教师”模型，学习驱动像素与目标外观之间的直接映射；**第二阶段**训练跨身份的“学生”模型，其驱动线索由 StableAnimator（生成伪姿态线索）和 Face‑Adapter（生成伪人脸线索）合成。学生模型除标准去噪损失外，还被引入 **Same2X 对齐损失** $\mathcal{L}_{\text{S2X}}$，该损失最大化学生与教师在选定 DiT 块中对应 patch 嵌入的余弦相似度（公式 4），迫使跨身份模型在特征空间中模仿同身份模型的动力学。这一内部指南不仅大幅加速了训练收敛（同等损失水平下训练快了 6.7 倍），还显著提升了跨身份动画的质量与稳定性。

## 核心模块与公式推导

DirectAnimator 绕过传统姿态估计器，直接从驾驶视频的原始像素中学习动画生成，其核心设计由三个相互协同的模块构成：（1）结构化驱动线索三元组（Driving Cue Triplet）的提取；（2）基于时间条件化自适应层归一化与门控残差的 CueFusion DiT 块；（3）利用同身份特征对齐引导跨身份训练的 Same2X 训练策略。这些模块共同解决了姿态估计误差累积导致的伪影，以及跨身份训练不稳定、收敛缓慢两大瓶颈（图1左侧定性对比，图1右侧 6.7 倍训练加速）。

---

### 1. 驱动线索三元组：从原始像素到结构化运动表示

为替代容易出错的骨架图，DirectAnimator 将驾驶视频像素解耦为三个互补的线索（图2(a)、图3）：

- **姿态线索（Pose Cue）**：使用 Grounded SAM 分割人体前景，后在频域施加低通滤波，滤除高频纹理细节，仅保留全局身体姿态与形状信息。从而避免纹理干扰，降低前景-背景混淆。
- **人脸线索（Face Cue）**：由 InsightFace 检测人脸区域并放大居中，直接保留原始面部表现力，避免仅靠稀疏关键点无法捕捉细腻表情的缺陷。
- **位置线索（Location Cue）**：以软化的身体与面部掩码给出空间对齐参考，辅助模型进行参考‑驾驶之间的几何一致映射。

这些线索不具有强归纳偏置的显式骨架，而是将信息量更丰富的原始像素以解耦、去噪的方式送入后续模块，造成**驱动信号引入误差大幅降低**（表3消融：移除任一线索均导致 FID 上升和 SSIM 下降）。

---

### 2. CueFusion DiT 块：时间条件化的线索注入

线索不能被简单拼接或当作交叉注意力键值，否则会破坏预训练生成骨干的去噪平衡。CueFusion DiT 块（图2(b)）通过**调制‑门控双路径**实现稳定而可控的注入。其关键公式如下：

**调制因子生成**（Section 3.1，Eq 1）：

$$
\alpha _ { p } , \beta _ { p } , \gamma _ { p } , \alpha _ { f } , \beta _ { f } , \gamma _ { f } = M L P ( S i L U ( e _ { t } ) )
$$

式中 $e_t$ 为扩散时间步嵌入，MLP 经 SiLU 激活后同时输出姿态（下标 $p$）与人脸（下标 $f$）线索的尺度因子 $\alpha$、偏移因子 $\beta$ 以及门控系数 $\gamma$。这些因子均依赖于时间步，使线索注入强度随着去噪进程自适应调整。

**自适应层归一化调制**（Eq 2）：

$$
e _ { p } ^ { M } = L N ( e _ { p } ) \cdot ( 1 + \alpha _ { p } ) + \beta _ { p }, \quad e _ { f } ^ { M } = L N ( e _ { f } ) \cdot ( 1 + \alpha _ { f } ) + \beta _ { f }
$$

其中 $e_{p}, e_{f}$ 分别是姿态与人脸线索的 patch 嵌入，$LN(\cdot)$ 为 LayerNorm。$\alpha$ 负责缩放特征动态范围，$\beta$ 实现方向性偏移，二者联合完成条件化调制。

**门控残差连接**（Eq 3）：

$$
e _ { p } ^ { G } = e _ { p } + \gamma _ { p } \cdot e _ { p } ^ { M }, \quad e _ { f } ^ { G } = e _ { f } + \gamma _ { f } \cdot e _ { f } ^ { M }
$$

$\gamma$ 作为门控权重，控制调制信息 $e^{M}$ 的加入比例，而原始的 $e_p, e_f$ 直接保留为残差路径。这一设计使每个 DiT 块能同时接收未经调制的原始身份流和经时间条件强化的运动/表情流，既保留生成骨干的身份保真度，又增强了姿势和表情的可控性。

**实验支撑**：替换为直接拼接（DC Injection）或交叉注意力注入（CA Injection）分别使 FID 增加 3.07 和 4.69，且 FVD 大幅恶化（表5），证明门控残差与自适应调制是该注入机制发挥效能的关键。

---

### 3. Same2X 训练策略：同身份特征引导跨身份对齐

跨身份训练中，驾驶与参考来自不同个体，直接优化易陷入局部震荡。Same2X 策略引入一个在**同身份数据**上预训练的“教师”模型，通过特征对齐损失约束“学生”模型（跨身份）的内部表示，无需额外数据标注（图4）。其对齐损失定义为（Section 3.2，Eq 4）：

$$
\mathcal{L}_{S2X}(\theta_S, \theta_X) := - \mathbb{E}_{\mathbf{x},c,\epsilon,t}\left[ \frac{1}{N} \sum_{n=1}^N \sin\left( h_s^{[D\_n]}, h_x^{[D\_n]} \right) \right]
$$

其中 $\theta_S$、$\theta_X$ 分别为教师（同ID）和学生（跨ID）的参数；$h_{s}^{[D\_n]}$ 和 $h_{x}^{[D\_n]}$ 为第 $D$ 个 DiT 块中第 $n$ 个 patch 的嵌入向量；$\sin(\cdot,\cdot)$ 表示余弦相似度；$N$ 为 patch 总数。该损失最大化二者特征的平均相似度，从而将同身份模型已经学得的**运动‑身份解耦先验**平滑迁移至跨身份场景。

该损失与标准去噪损失联合优化，实现收敛速度提升 6.7 倍（图1右），并显著提高质量：移除 Same2X 后 FID 从 27.61 飙升至 32.21，FIS 从 0.638 跌至 0.368（表3）。对齐深度 $D=10$ 和正则化系数 $\lambda=0.5$ 为最优超参，过度对齐会损害生成质量（表4）。

---

### 4. 小结

三个模块构成完整的因果链条：**线索三元组**为模型提供低噪声的驱动信号，**CueFusion 注入**保证信号在去噪过程中的稳定传递，**Same2X 训练**克服了跨身份学习的不稳定性。三者叠加使得 DirectAnimator 在 TikTok 和 Unseen 基准上全面超越现有骨架驱动方法（FID 降低 4‑5 点，表1），同时姿态与面部关键点一致性误差降至最低（PLC、FLC，表2）。尽管推理延迟较传统方法略高（49 帧约 152 秒），且依赖分割等前处理模型，该框架为摆脱显式姿态估计、充分利用原始视频信息开辟了新方向。

## 实验与分析

DirectAnimator 在 TikTok 与 Unseen 两个标准测试集上被全面评估，并与代表性骨架驱动方法 (StableAnimator、MimicMotion、AnimateAnyone、UniAnimate-DiT 等) 进行对比。评测涵盖视觉质量 (FID、SSIM、PSNR、LPIPS、L1)、身份/时序一致性 (FIS/FTS、FVD)、以及几何一致性 (关键点误差 PLC、面部关键点误差 FLC)。若无特殊说明，所有实验均以 4×H20 GPU 在 512² 分辨率下训练 40K 步完成。

### 1. 主结果：直接像素驱动全面超越骨架中间表示

**整体视觉质量与身份保持**  
如 Table 1 所示，DirectAnimator 在两个测试集上取得最优 FID (TikTok 25.87，Unseen 27.62)，相比此前最强的 StableAnimator 分别降低 4.52 与 5.33。SSIM 与 PSNR 同样达到最高 (SSIM: 0.806/0.708; PSNR: 30.12/29.41)，表明重建纹理与结构更保真。FIS 与 FTS 指标上 DirectAnimator 亦优于所有对比方法，反映其更强的面部身份保持与时间一致性。唯一逊色的指标是 FVD——在 TikTok 上与 StableAnimator 接近但略高 (142.60 vs. 140.62)，而在 Unseen 上则显著领先 (276.34 vs. 365.52)，说明在未见人物上时间相干性优势更大。值得注意的是，DirectAnimator 仅训练 40K 步，远少于多数基线 (100K–300K 步)，其训练效率优势显著。


![[assets/figures/papers/iclr26_0013_HdEpZE3wFa_Beyond_Skeletons_Learning_Animation_Directly_fro/figures/008_Table_1.jpg]]
*Table 1: Quantitative comparison on the TikTok and Unseen datasets. Bold text indicates the best result, while underlined text indicates the second-best. ↑ denotes that higher values are better. FIS and FTS stand for Face Identity Similarity and Face Temporal Similarity, respectively. In the table, a / b denotes results on TikTok and Unseen, respectively*

**几何一致性：姿态与面部跟随更准确**  
Table 2 报告了基于估计关键点的几何误差。DirectAnimator 取得最低的 PLC (TikTok 0.071，Unseen 0.092) 和最低的 FLC (TikTok 0.037，Unseen 0.057)，而最佳基线 MimicMotion 的 PLC 分别为 0.162/0.179，FLC 分别为 0.050/0.075。这表明直接从原始视频像素学习运动与表情，比依赖从出错骨架回归更精准地复现驾驶信号。


![[assets/figures/papers/iclr26_0013_HdEpZE3wFa_Beyond_Skeletons_Learning_Animation_Directly_fro/figures/011_Table_2.jpg]]
*Table 2: Pose and facial landmark consis- Table 3: Ablation study for driving cues and Same2X tency on TikTok / Unseen. training strategy*

**定性证据与失败模式**  
Figure 5 (TikTok 与 Unseen 样本) 中，StableAnimator 因骨架前‑后混淆、手部错误、肢体缺失而产生严重伪影；DirectAnimator 用原始像素驱动的结果更真实、身份保持更好。但 limitations 明确指出，**运动模糊会导致肢体末端细节丢失，严重时结构错乱**。此外，底层生成骨干 (CogVideoX1.5) 的限制使得部分困难案例仍存在纹理瑕疵与身份保持不完美；而伪驱动线索（由 StableAnimator/Face‑Adapter 合成）可能引入原生成模型的伪影，在跨身份训练阶段影响质量上限。

### 2. Same2X 训练策略：6.7 倍加速与跨身份对齐的关键作用

Figure 1(右) 的训练曲线对比显示，启用 Same2X 策略后，跨身份阶段达到相同损失水平仅需 1/6.7 的步数，证明同身份特征对齐有效传递了内部知识。消融实验中，**移除 Same2X 策略 (Table 3, S8)** 导致 FID 从 27.61 急剧上升至 32.21，FIS 从 0.638 降至 0.368，FVD 从 180.52 恶化至 284.69，是单组件贡献最大的因素。进一步的超参数分析 (Table 4) 显示，对齐深度 D=10 与正则化系数 λ=0.5 为最优；继续增大 D 会过约束特征空间并损害生成质量。


![[assets/figures/papers/iclr26_0013_HdEpZE3wFa_Beyond_Skeletons_Learning_Animation_Directly_fro/figures/003_Figure_1.jpg]]
*Figure 1: Our proposed driving cue provides a more robust representation for complex motions and self-occlusions. Left: Errors in skeleton maps such as front-back confusion, inaccurate hand localization, and missing limbs result in noticeable artifacts in StableAnimator outputs. In contrast, DirectAnimator uses raw pixels from the driving video as driving signals, generating accurate and realistic frames. Right: The Same2X training strategy significantly improves training efficiency in cross-ID scenarios (Stage 2), reaching the same loss level 6.7× faster than training without it*

![[assets/figures/papers/iclr26_0013_HdEpZE3wFa_Beyond_Skeletons_Learning_Animation_Directly_fro/figures/012_Table_3.jpg]]

### 3. 驱动线索与注入机制消融

**线索三元组必要性**  
Table 3 逐项剥离驱动线索：  
- 移除 Face Cue (S1) 或不对面部进行中心放大 (S2) 导致 FID 分别增至 30.83 / 29.32，SSIM 与 PSNR 同步下降，验证了**面部原始像素对于表情传输的不可替代性**。  
- 移除 Pose Cue 的低通滤波 (S3) 或完全替换为骨架图 (S4) 均造成 FID 上升(30.08 / 30.18)，FIS 与 FVD 变差，说明**频域滤波压制外观细节、保留粗粒度运动轮廓是有效解耦关键**；直接回归骨架图则丧失了像素丰富的运动信息。  
- 移除 Location Cue (S5) 导致 FID 激增至 31.83、SSIM 仅 0.617，表明空间对齐线索对跨身份生成不可或缺。  

**CueFusion DiT 块设计**  
与两种常见注入方式相比 (Table 5)：  

![[assets/figures/papers/iclr26_0013_HdEpZE3wFa_Beyond_Skeletons_Learning_Animation_Directly_fro/figures/014_Table_5.jpg]]
*Table 5: Ablation study for the design of CF-DiT block*

- 直接拼接 (DC Injection) 使 FID 由 27.61 升至 30.68，FVD 从 180.52 升至 259.37；  
- 交叉注意力注入 (CA Injection) 进一步恶化 (FID 32.30, FVD 316.91)。  
这证明**时间条件自适应层归一化与门控残差连接**在保持身份特征的同时有效注入驱动信息，比简单拼接或注意力更具鲁棒性。

### 4. 伪数据质量重于数量

Table 6 检验了跨身份训练中的伪驱动线索质量影响。使用经过质量过滤的 500 样本伪集 (Ours) 在 FID、FIS、FVD 上全面优于未过滤的 5000 样本集 (FID: 27.61 vs 30.11)，说明**伪数据质量对最终性能的影响远超数据量**。摘要中还需注意，伪数据合成依赖于第三方模型，若该模型存在身份泄露或伪影，仍有传递风险。

### 5. 推理效率与计算成本

Table 7 给出单次 49 帧生成在 H20 GPU 上的耗时对比：DirectAnimator 预处理需 31 ms（Grounded SAM 分割等），总生成时间 152.80 s；StableAnimator 仅需 9.6 ms 预处理与 91.63 s 生成。这一差异源于 DirectAnimator 从视频帧提取三种线索的前处理开销，以及 DiT 骨干本身的推理成本，属于实际部署中需权衡的劣势。

## 方法谱系与知识库定位

DirectAnimator 在人体图像动画（HIA）方法谱系中属于**端到端原始像素驱动**的新范式。现有主流方法——包括 StableAnimator、MimicMotion、AnimateAnyone 与 UniAnimate-DiT——均以姿态估计器（如 OpenPose、DWPose）输出的 2D 骨架图作为核心驱动信号。这类中间表示在遮挡、自遮挡或复杂体态下极易出错（前后混淆、手部错位、肢体缺失），直接导致生成帧中出现明显伪影与身份漂移（Figure 1 左）。DirectAnimator 而非沿用骨架驱动，而是直接将原始驾驶视频像素抽象为三项**结构化驱动线索三元组**：姿态线索（Pose Cue，经前景分割与频域低通滤波）、面部线索（Face Cue，裁剪并居中的面部区域）与位置线索（Location Cue，软化的人体/面部掩码），并通过 CueFusion DiT 块以时间条件自适应 LayerNorm 与门控残差的方式注入去噪过程（Figure 2）。这一设计从根本上绕过显式姿态估计的误差累积，使得模型能够从原始信号中学习更丰富的运动与表情信息。

在与基线的定量对比中，DirectAnimator 在 TikTok 与 Unseen 测试集上的 FID、SSIM、PSNR、LPIPS 等主要感知指标全面超越 StableAnimator、MimicMotion、UniAnimate-DiT 等方法（Table 1）。尤其在几何对齐层面，其姿态关键点一致性（PLC）与面部关键点一致性（FLC）误差均为最低（Table 2），说明在复杂姿态和表情跟随上比骨架驱动方法更为精准。值得注意的是，该效果并非以更大算力换取：DirectAnimator 的总训练步数（40K 步）远少于多数对比方法（100K–300K 步），这得益于其 Same2X 训练策略——通过同身份预训练建立内部特征空间，再以 S2X 对齐损失引导跨身份训练，使 Stage 2 达到相同损失水平的速度提升 **6.7 倍**（Figure 1 右）。然而，在推理效率上，该方法生成 49 帧需要约 152 秒，明显慢于 StableAnimator 的 91 秒，且预处理耗时要高（约 31 ms vs. 9.6 ms，Table 7），这在实际部署中是需要权衡的因素。

**适用边界与当前局限**  
尽管 DirectAnimator 在标准基准上表现出色，其实际适用仍面临若干约束。

1. **运动模糊鲁棒性有限**：当驾驶视频存在严重运动模糊时，生成帧的手部末端等局部细节会明显退化，极端情况下甚至出现肢体结构错乱。  
2. **生成骨干固有限制**：最终输出质量受制于底层生成模型 CogVideoX1.5 的基础能力，复杂场景下仍可能出现纹理瑕疵或身份保持不完美。  
3. **对显式位置线索的依赖**：训练过程中位置线索（Location Cue）承担了显式的空间对齐功能，这与人类隐式理解运动模式的机制存在本质差距，可能限制模型在无掩码场景下的泛化性。  
4. **伪驱动线索引入的噪声**：跨身份训练阶段所需的伪姿态与伪面部线索由 StableAnimator 与 Face‑Adapter 合成（Figure 8），这些第三方模型自带的伪影、身份泄露等问题会传递至 DirectAnimator，约束训练质量的上限。Table 6 显示，对伪数据进行质量过滤（500 高质量样本）的效果显著优于无过滤的大规模使用（5 000 样本），说明伪数据质量比数量更重要，也印证了该环节的敏感性。  
5. **推理延迟较高**：一次 49 帧的推理需约 152 秒，在需要低延迟的交互式应用中体验不佳。

**开放问题**  
上述局限映射出若干关键开放方向：

- **隐式空间对齐机制**：能否设计完全端到端的隐式对齐方案，移除显式的 Location Cue，让模型自主学习驱动帧与参考帧之间的空间对应关系？  
- **高质量伪数据流水线**：通过更精准的运动迁移模型和自动化质量筛选模块，是否可以系统性提升伪驱动线索的保真度，从而突破当前跨身份训练的瓶颈？  
- **细粒度手部表征增强**：引入专门的手部姿态估计器或高分辨率手部编码，作为额外驱动线索，能否大幅改善手部动画的几何准确度与真实感？  
- **更强生成骨干的潜力**：将 DirectAnimator 框架迁移至更大规模、更高分辨率的视频生成基础模型（如更高参数的 DiT）后，纹理清晰度和身份保持的上限能提升多少？  
- **无伪标签的自监督跨身份训练**：在何种数据规模与训练范式下，可以完全摒弃第三方模型的合成标签，仅利用原始视频的自监督信号完成高质量的跨身份动画学习？

> 对于推理延迟与部分细节退化问题，原文并未提供根因分析，其改善路径仍以推测为主，需后续实验验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Beyond_Skeletons_Learning_Animation_Directly_from_Driving_Videos_with_Same2X_Training_Strategy.pdf]]
