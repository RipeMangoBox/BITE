---
title: "PC-Talk: Precise Facial Animation Control for Audio-Driven Talking Face Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PC_Talk_Precise_Facial_Animation_Control_for_Audio_Driven_Talking_Face_Generation.pdf
project_link: "https://bq-wang0511.github.io/PC-Talk/"
code_link: "https://github.com/mseitzer/pytorch-fid"
aliases:
- PT
- PC-Talk
tags:
- CVPR_2026
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/vision_multimodal_applications
core_operator: 通过预测隐式关键点的附加变形（唇音同步变形 D_l 和情感变形 D_e），并分解纯情感变形，实现对说话风格和情感的解耦与精细控制。
primary_logic: 将面部动画控制建模为对隐式关键点的变形预测和组合，通过风格感知的自回归变换器预测唇音同步变形，并通过从混合表情中减去中性表情分解出纯情感变形，从而在不牺牲唇音同步的前提下实现多样化的风格编辑和情感强度/区域控制。
claims:
- LAC模块支持从参考视频或预设选项提取说话风格，并能编辑特定唇部发音的形状。
- EMC模块通过分解纯情感变形，生成生动的表情，并可控制情感强度和不同面部区域的复合情感。
- 在HDTF和MEAD数据集上，PC-Talk在唇音同步、图像质量、情感准确率等指标上均达到SOTA性能。
- 用户研究表明，PC-Talk在唇音同步、图像质量、时间一致性和情感表达力等维度均获最高评分。
---

# PC-Talk: Precise Facial Animation Control for Audio-Driven Talking Face Generation

> [!tip] 核心洞察
> 将面部动画控制建模为对隐式关键点的变形预测和组合，通过风格感知的自回归变换器预测唇音同步变形，并通过从混合表情中减去中性表情分解出纯情感变形，从而在不牺牲唇音同步的前提下实现多样化的风格编辑和情感强度/区域控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | PC-Talk：面向音频驱动说话人脸生成的精确面部动画控制 |
| 英文题名 | PC-Talk: Precise Facial Animation Control for Audio-Driven Talking Face Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2503.14295) · [Project](https://bq-wang0511.github.io/PC-Talk/) · [Code](https://github.com/mseitzer/pytorch-fid) |
| Topic | #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/vision_multimodal_applications |
| Method | PC-Talk |
| Dataset | HDTF, MEAD |

> [!tip] 效果简介
> - HDTF (neutral, video input) 上，LSE-C (↑) 9.03 vs 8.92 (Wav2Lip) (+0.11)；FID (↓) 15.51 vs 15.78 (MuseTalk) (-0.27)。
> - HDTF (emotional) 上，Acc_emo (↑) 46.19 vs 45.21 (ED-Talk) (+0.98)；FID (↓) 24.05 vs 58.19 (ED-Talk) (-34.14)。
> - MEAD (emotional) 上，Acc_emo (↑) 72.32 vs 68.21 (EAT) (+4.11)。

## 概述

**问题瓶颈**：现有音频驱动说话人脸生成方法在唇音同步上取得了显著进展，但普遍缺乏对说话风格和情感的精细控制——生成的面部动画风格单一、情感表达不丰富，难以满足个性化定制需求（如不同说话习惯、情感强度调节及复合情感表达）。

**核心思路**：PC-Talk 将面部动画控制建模为对**隐式关键点**的变形预测与组合。具体而言，通过**唇音对齐控制模块（LAC）**预测唇音同步变形，实现多样化说话风格的适应与编辑；通过**情感控制模块（EMC）**从混合表情中减去中性表情，分解出纯情感变形，从而在不牺牲唇音同步的前提下，支持情感强度的连续调节和不同面部区域的复合情感控制。

**方法定位**：PC-Talk 采用基于隐式关键点的中间表示，区别于主流的 3D 形态模型路线（如 **SadTalker**, Zhang et al., CVPR 2023）或基于扩散模型的生成范式（如 **LatentSync**, Li et al., arXiv 2024）。在控制维度上，它首次将说话风格编辑和区域级情感控制统一到同一框架中，相较于仅做情感标签映射的 **EAMM**（Ji et al., SIGGRAPH 2022）或 **ED-Talk**（Tan et al., ECCV 2024），提供了更细粒度的操控能力。

**主要结果**：在 HDTF 和 MEAD 数据集上，PC-Talk 在唇音同步精度（LSE-C）、图像质量（FID）和情感准确率（Acc_emo）等指标上均达到 SOTA 水平。用户研究进一步表明，该方法在唇音同步、图像质量、时间一致性和情感表达力等主观维度上均获最高评分。

> **注意**：以下各节将依次展开方法设计、实验验证与分析讨论。Figure 1 展示了 LAC 与 EMC 两大控制类别的整体能力，Figure 2 给出了框架的完整流水线。定量对比的核心数据见 Table 1（中性场景）和 Table 2（情感场景）。

## 背景与动机

音频驱动的说话人脸生成旨在从语音信号中合成逼真的说话面部视频，在虚拟数字人、视频会议、影视制作等领域具有广泛应用。近年来，基于深度学习的生成模型在该任务上取得了显著进展，尤其是唇音同步（lip-sync）精度已达到较高水平。然而，现有方法仍面临一个核心瓶颈：**生成的面部动画风格单一、情感表达不丰富，缺乏对说话风格和情感的精细控制**。

具体而言，当前主流方法存在以下关键缺口：

1. **说话风格控制缺失**：大多数方法仅追求唇部运动与音频内容的时间对齐，忽略了不同说话者特有的发音习惯、唇部运动幅度和节奏模式，导致生成的动画缺乏个性化，难以满足数字人定制等场景对多样化说话风格的需求。

2. **情感表达粗糙且不可控**：现有情感说话脸生成方法通常直接从情感标签或参考图像中生成整体表情，缺乏对情感强度和面部区域独立控制的能力。例如，无法实现“仅眼部区域表现愤怒而唇部保持中性”的复合情感控制，也难以平滑调节情感的强弱程度。

3. **唇音同步与情感表达难以兼顾**：在增强情感表现力的同时，往往会牺牲唇音同步精度，导致唇部运动与音频内容失配。现有方法缺乏一种统一的框架，能够在保持高精度唇音同步的前提下，实现对说话风格和情感的独立、精细控制。

针对上述问题，**PC-Talk** 提出了一种基于隐式关键点变形组合的精确面部动画控制框架。其核心洞察在于：将面部动画控制建模为对隐式关键点的变形预测与组合过程。具体而言，PC-Talk 设计了两个关键模块——**唇音对齐控制模块（Lip-Audio Alignment Control, LAC）** 和**情感控制模块（EMotion Control, EMC）**——分别预测唇音同步变形 $D_l$ 和情感变形 $D_e$，并通过将二者叠加到原始关键点上，实现唇音同步与情感表达的解耦控制。LAC 模块通过风格感知的自回归变换器，从参考视频或预设选项中提取说话风格，并可对特定唇部发音进行风格编辑；EMC 模块则通过从混合表情中减去中性表情，分解出纯情感变形，从而支持情感强度调节和不同面部区域的复合情感生成。

## 核心创新

PC-Talk 的核心创新在于将面部动画控制建模为对**隐式关键点的变形预测与组合**，并以此为基础实现了**说话风格与情感的精细解耦控制**。与现有方法相比，该方法在两个关键维度上引入了根本性的变化。

### 从单一唇音同步到可编辑的说话风格控制

现有音频驱动方法（如 **Wav2Lip** (Prajwal et al., ACM MM 2020)、**VideoRetalking** (Cheng et al., SIGGRAPH Asia 2022)）主要关注唇音同步的准确性，但生成的说话风格单一，无法体现不同说话者的习惯（如特定唇部发音的幅度、速度差异）。PC-Talk 通过**唇音对齐控制模块 (LAC)** 改变了这一格局：

- **统一风格空间建模**：LAC 将说话风格编码为风格嵌入 $e_s$，支持从参考视频提取或从预设选项中选择，实现了风格的灵活注入。
- **风格编辑能力**：在风格空间内，用户可以针对特定唇部发音（如“p”、“b”等辅音）独立调整变形程度，模拟不同的说话习惯。实验表明，风格编辑程度在 0.8–1.2 范围内时，唇音同步性能保持稳定（Figure 5）。
- **更高精度的同步机制**：LAC 采用预训练的视听同步编码器和 Wav2Lip 启发的同步损失 $\mathcal{L}_{sync}$，替代了传统 ASR 模型（如 Whisper）。消融实验证实，替换为 Whisper 后 LSE-C 从 9.37 骤降至 6.23，证明专用编码器对同步精度至关重要（Table 3）。

### 从标签驱动到分解式情感生成

情感说话脸生成方法（如 **EAMM** (Ji et al., SIGGRAPH 2022)、**EAT** (Gan et al., ICCV 2023)）通常直接从情感标签或参考图像生成表情，难以控制情感强度，也无法实现不同面部区域的复合情感。PC-Talk 的**情感控制模块 (EMC)** 通过**纯情感变形分解**实现了精细控制：

- **减法分解机制**：EMC 的核心公式为 $D_e = \mathrm{CPred}(emo, e_a) - \mathrm{CPred}(\text{'neutral'}, e_a)$，即从情感表情的复合变形中减去中性表情的复合变形，得到纯粹的、与唇音同步无关的情感变形 $D_e$。这从根本上解耦了情感与唇部运动。
- **强度与区域控制**：分解后的纯情感变形支持强度调整，并可在不同面部区域（如眼部、嘴部）独立施加不同情感，实现复合情感表达。消融实验（Figure 4）显示，无分解时情感表达模糊，分解显著增强了表情表现力。
- **量化优势**：在 HDTF 数据集上，PC-Talk 的情感准确率 (Acc_emo) 达到 46.19，FID 降至 24.05，相比 **ED-Talk** (Tan et al., ECCV 2024) 的 45.21 和 58.19，实现了大幅领先（Table 2）。

### 语义化隐式关键点作为统一控制接口

上述两个模块的共同基础是**具有语义含义的隐式关键点**。与 **SadTalker** (Zhang et al., CVPR 2023) 等使用 3D 形态模型的方法不同，PC-Talk 通过地标约束训练隐式关键点，使其具备可解释的语义（如对应眼角、嘴角等），并直接在关键点空间上施加唇音同步变形 $D_l$ 和情感变形 $D_e$。驱动关键点的计算为 $K_d = K_{ori} + D_l + D_e$，这种加性组合使得风格和情感控制可以独立运作、互不干扰，构成了整个框架的“因果旋钮”。

## 整体框架

PC-Talk 将说话人脸生成中的精细控制问题建模为对**隐式关键点（implicit keypoints）**的变形预测与组合。其核心洞察在于：唇音同步与情感表达可以分解为两类独立的变形量，分别由专门的模块预测后叠加到同一组关键点上，再通过变形与渲染生成最终图像。这一设计使得风格与情感的解耦控制成为可能，同时不牺牲唇音同步精度。

### 框架总览

整个 pipeline 由五个核心模块串联构成，数据流从参考图像和音频出发，最终输出驱动后的人脸图像。

**Figure 2**（框架总览图）展示了完整的数据流：参考图像首先经过运动提取器得到原始隐式关键点 $K_{ori}$，随后 LAC 模块和 EMC 模块分别预测唇音同步变形 $D_l$ 和情感变形 $D_e$，两者相加得到驱动关键点 $K_d$，最后通过变形模块和解码器渲染出结果图像。

### 模块关系与输入输出流

1. **运动提取器（Motion Extractor）**  
   从参考图像中提取原始隐式关键点 $K_{ori}$，其计算基于典范关键点 $K_c$、旋转矩阵 $R$、表情变形 $\delta$、缩放因子 $s$ 和平移向量 $t$：
   $$K_{ori} = s \cdot ( K_{c} \cdot R + \delta ) + t \tag{1}$$
   这些隐式关键点通过地标约束训练，具有明确的语义含义，为后续变形预测提供了结构化的中间表示。

2. **唇音对齐控制模块（LAC Module）**  
   以音频特征 $e_a$、风格嵌入 $e_s$ 和原始关键点 $K_{ori}$ 为输入，通过风格感知的自回归变换器预测唇音同步变形 $D_l$：
   $$D_{l} = \mathrm{ExpPredictor}( e_{a}, e_{s}, K_{ori} ) \tag{4}$$
   LAC 模块支持从参考视频或预设选项提取说话风格，并可对特定唇部发音的形状进行编辑。

3. **情感控制模块（EMC Module）**  
   通过分解纯情感变形来生成生动的表情。其关键操作是从情感表情的复合变形中减去中性表情的复合变形，得到纯情感变形 $D_e$：
   $$D_{e} = \mathrm{CPred}( emo, e_{a} ) - \mathrm{CPred}( \text{'neutral'}, e_{a} ) \tag{5}$$
   这一分解机制使得情感强度可调，并支持不同面部区域的独立情感控制与复合情感合成。

4. **驱动关键点合成**  
   将原始关键点与两类变形直接相加，得到驱动关键点：
   $$K_{d} = K_{ori} + D_{l} + D_{e} \tag{2}$$
   这种加性组合方式保证了唇音同步与情感表达在关键点空间的解耦。

5. **变形模块（Warping Module）与解码器（Decoder）**  
   利用 $K_{ori}$ 和 $K_d$ 之间的对应关系计算光流场，对外观特征 $f_a$ 进行变形，再通过解码器生成最终图像 $I_{res}$：
   $$I_{res} = \mathrm{Decoder}( \mathrm{Warp}( f_{a}, K_{ori}, K_{d} ) ) \tag{3}$$

### 设计优势

相较于现有方法多使用 3D 形态模型或语义利用不足的隐式关键点，PC-Talk 的中间表示具有明确的语义含义，且直接在关键点层面施加变形，避免了在像素空间或特征空间进行复杂耦合操作。LAC 与 EMC 的并行设计使得两类控制可以独立训练、独立推理，同时通过共享的 $K_{ori}$ 和加性组合实现无缝集成。

### 补充图表

![[assets/figures/papers/paper_list_l999_https_arxiv_org_abs_2503_14295/figures/002_Figure_2.jpg]]
*Figure 2: Our framework PC-Talk is designed for precise control in talking face generation. It achieves this control by first predicting a deformation of implicit keypoints and then rendering it into a final talking image. We utilize a Lip-Audio alignment Control (LAC) module to estimate lip-sync deformations*

## 核心模块与公式推导

PC-Talk 的核心控制机制建立在**隐式关键点变形预测与组合**之上。给定参考图像，运动提取器首先估计一组具有语义含义的隐式关键点，随后两个独立的控制模块分别预测唇音同步变形和情感变形，二者叠加后驱动外观特征的变形与最终渲染。

### 3.1 隐式关键点表示

框架采用具有语义含义的隐式关键点作为中间表示。给定参考图像，运动提取器计算原始隐式关键点 $K_{ori}$：

$$K_{ori} = s \cdot ( K_{c} \cdot R + \delta ) + t \tag{1}$$

其中 $K_c$ 为典范关键点，$R$ 为旋转矩阵，$\delta$ 为表情变形，$s$ 为缩放因子，$t$ 为平移向量。这些关键点通过地标约束训练，使其具备明确的语义对应关系。

驱动关键点 $K_d$ 由原始关键点叠加两类变形得到：

$$K_{d} = K_{ori} + D_{l} + D_{e} \tag{2}$$

其中 $D_l$ 为唇音同步变形，$D_e$ 为情感变形。变形模块基于 $K_{ori}$ 与 $K_d$ 计算光流场，对外观特征 $f_a$ 进行变形，最终由解码器生成输出图像：

$$I_{res} = \mathrm{Decoder}( \mathrm{Warp}( f_{a}, K_{ori}, K_{d} ) ) \tag{3}$$

### 3.2 唇音对齐控制模块（LAC）

LAC 模块的核心是一个风格感知的自回归变换器，根据音频特征 $e_a$、风格嵌入 $e_s$ 和原始关键点 $K_{ori}$ 预测唇音同步变形：

$$D_{l} = \mathrm{ExpPredictor}( e_{a}, e_{s}, K_{ori} ) \tag{4}$$

**风格控制机制**：风格嵌入 $e_s$ 可从参考视频提取，也可从预设选项中选择。通过统一建模的风格空间，该模块支持对特定唇部发音的形状进行编辑，实现不同说话习惯的模拟。

**训练损失**：LAC 模块的总损失由五项组成：

$$\mathcal{L}_{LAC} = \mathcal{L}_{sync} + \lambda_{kp}\mathcal{L}_{kp} + \lambda_{reg}\mathcal{L}_{reg} + \lambda_{vel}\mathcal{L}_{vel} + \lambda_{style}\mathcal{L}_{style} \tag{6}$$

其中同步损失 $\mathcal{L}_{sync}$ 采用预训练的视听同步编码器，计算视频嵌入与音频嵌入的余弦相似度：

$$\mathcal{L}_{sync} = - \frac{ \mathbf{S}_{v}( I_{gt:gt+4} )^{\mathbf{T}} \cdot \mathbf{S}_{a}( a_{gt:gt+4} ) }{ \| \mathbf{S}_{v}( I_{gt:gt+4} ) \|_{2} \| \mathbf{S}_{a}( a_{gt:gt+4} ) \|_{2} } \tag{7}$$

消融实验表明，将该同步编码器替换为 Whisper 后，LSE-C 从 9.37 骤降至 6.23，验证了自定义视听同步编码器对唇音同步精度的决定性作用（Table 3）。

### 3.3 情感控制模块（EMC）

EMC 模块的核心创新在于**纯情感变形的分解**。给定情感标签 $emo$ 和音频特征 $e_a$，首先通过复合预测器 $\mathrm{CPred}$ 分别预测情感表情和中性表情的复合变形，二者相减得到纯情感变形：

$$D_{e} = \mathrm{CPred}( emo, e_{a} ) - \mathrm{CPred}( \text{'neutral'}, e_{a} ) \tag{5}$$

**分解的必要性**：复合变形中同时包含唇音同步和情感信息，直接使用会导致唇音与情感相互干扰。通过减去中性表情的复合变形，可剥离出仅反映情感变化的纯变形分量，从而在不牺牲唇音同步的前提下生成生动的表情。

**控制能力**：基于纯情感变形，EMC 模块支持两项精细控制——（1）**强度调整**：通过缩放 $D_e$ 的幅度控制情感表达强度；（2）**区域复合情感**：对不同面部区域独立施加不同情感类别的变形，实现如“眼睛愤怒+嘴部微笑”的复合情感表达。消融实验（Figure 4）证实，去除分解步骤后情感表达显著模糊，验证了该机制对表情表现力的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l999_https_arxiv_org_abs_2503_14295/figures/001_Figure_1.jpg]]
*Figure 1: PC-Talk separates talking face control into two categories: Lip-Audio Alignment Control (LAC) for adapting and editing diverse speaking styles to simulate different talking habits, and EMotion Control (EMC) for generating expressive faces with adjustable intensity and region-specific compound emotions*

## 实验与分析

### 主实验结果

PC-Talk 在 HDTF 和 MEAD 两个数据集上进行了全面的定量评估，涵盖中性说话脸生成和情感说话脸生成两个场景。

**中性说话脸生成**（Table 1）：在 HDTF 数据集上，PC-Talk 在视频输入模式下取得了 LSE-C 9.03、LSE-D 6.69、FID 15.51 的成绩；在图像输入模式下取得了 LSE-C 9.37、LSE-D 6.44、FID 33.07 的成绩。与现有方法相比，PC-Talk 在唇音同步指标 LSE-C 上超越了 **Wav2Lip**（Prajwal et al., ACM MM 2020）的 8.92，在图像质量指标 FID 上优于 **MuseTalk**（Zhang et al., arXiv 2024）的 15.78，在时间一致性指标 FVD 上达到最优水平。值得注意的是，PC-Talk 在保持高唇音同步精度的同时，并未牺牲图像质量和时间一致性，这是区别于其他方法的显著优势。

**情感说话脸生成**（Table 2）：在 HDTF 数据集上，PC-Talk 取得了 Acc_emo 46.19、FID 24.05 的成绩。与 **ED-Talk**（Tan et al., ECCV 2024）相比，PC-Talk 在情感准确率上提升了 0.98 个百分点，同时 FID 大幅降低了 34.14（从 58.19 降至 24.05），表明生成图像质量显著更优。在 MEAD 数据集上，PC-Talk 的 Acc_emo 达到 72.32，超越 **EAT**（Gan et al., ICCV 2023）的 68.21 达 4.11 个百分点，同时 E-FID 仅为 1.88，情感表达质量优势明显。

定性对比（Figure 3）进一步验证了量化结果：其他方法普遍存在牙齿模糊、唇形不准确、情感表达错误等问题，而 PC-Talk 生成的说话脸在唇部细节清晰度、唇形准确性和情感表达力方面均表现更佳。

![[assets/figures/papers/paper_list_l999_https_arxiv_org_abs_2503_14295/figures/005_Figure_3.jpg]]
*Figure 3: Comparison with other baselines. We highlight flaws of other methods using colorful bounding boxes, including blurry teeth, inaccurate lip shapes, and incorrect emotional expressions. Please zoom in to check details*

### 消融实验

**唇音对齐消融**（Table 3）：将预训练的视听同步编码器替换为 Whisper 后，LSE-C 从 9.37 骤降至 6.23，降幅达 3.14，证明自定义的视听同步编码器对唇音同步精度至关重要。该编码器通过同步损失（Eq. 7）直接优化视频嵌入与音频嵌入的余弦相似度，比通用 ASR 模型更能捕捉细粒度的唇音对应关系。

**情感分解消融**（Figure 4）：移除情感分解机制后，生成的表情趋于模糊，缺乏表现力。具体而言，无分解时模型直接从情感标签预测复合变形，导致情感特征与中性表情特征混合，难以产生清晰的情感表达。通过从情感表情的复合变形中减去中性表情的复合变形（Eq. 5），纯情感变形能够独立作用于关键点，显著增强情感表达力。

**唇部运动尺度与风格编辑分析**（Figure 5）：唇部运动尺度在 0.8 附近时唇音同步性能最优，过大的运动尺度会导致唇形失真，过小则唇部运动不够充分。风格编辑程度在 0.8-1.2 范围内性能保持稳定，表明 LAC 模块的风格编辑机制具有良好的鲁棒性，能够在保持唇音同步的前提下实现多样化的说话风格编辑。

### 效率分析

Table 4 展示了各方法的推理效率（帧/秒）。PC-Talk 在保证高质量生成的同时，推理速度处于竞争水平。具体效率数据需要对照原文 Table 4 确认，但分析表明该方法适用于实时或近实时应用场景。

![[assets/figures/papers/paper_list_l999_https_arxiv_org_abs_2503_14295/figures/008_Table_4.jpg]]
*Table 4: Efficiency Comparison (frame per second)*

### 用户研究

Table 5 报告了用户研究结果（1-5 分制）。PC-Talk 在五个评估维度上均获得最高评分：唇音同步、图像质量、时间一致性、情感表达力和整体真实感。这一结果与定量指标高度一致，从主观感知层面验证了 PC-Talk 在精细面部动画控制方面的优势。

![[assets/figures/papers/paper_list_l999_https_arxiv_org_abs_2503_14295/figures/011_Table_5.jpg]]
*Table 5: User Study results. The rating is on scale of 1-5, with the higher rank demonstrate better results*

### 失败模式与局限性

尽管 PC-Talk 在多数指标上取得 SOTA 性能，但分析中未明确报告具体的失败案例。根据方法设计推断，潜在局限可能包括：情感分解依赖于预定义的情感类别，对细粒度情感（如惊奇、厌恶）的泛化能力有待验证；隐式关键点虽然在语义上有一定含义，但在极端姿态或遮挡场景下的鲁棒性需要进一步检验。这些方面需要手动对照原文进行验证。

### 补充图表

![[assets/figures/papers/paper_list_l999_https_arxiv_org_abs_2503_14295/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparisons with state-of-the-art methods*

![[assets/figures/papers/paper_list_l999_https_arxiv_org_abs_2503_14295/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparisons on emotional talking face generation*

![[assets/figures/papers/paper_list_l999_https_arxiv_org_abs_2503_14295/figures/006_Figure_4.jpg]]
*Figure 4: Ablation study on emotion decomposition*

![[assets/figures/papers/paper_list_l999_https_arxiv_org_abs_2503_14295/figures/007_Table_3.jpg]]
*Table 3: Ablation Study on lip-audio alignment*

![[assets/figures/papers/paper_list_l999_https_arxiv_org_abs_2503_14295/figures/009_Figure_5.jpg]]
*Figure 5: Lip-sync performance with different lip movement scales and speaking style editing across each lip articulation*

![[assets/figures/papers/paper_list_l999_https_arxiv_org_abs_2503_14295/figures/010_Figure_6.jpg]]
*Figure 6: Emotion and Speaking Style Interpolation*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

PC-Talk 的核心贡献在于将面部动画控制分解为“唇音同步变形”与“情感变形”两个可独立操控的维度，并通过隐式关键点的变形预测与组合实现精确控制。这一思路与现有工作形成了清晰的继承与超越关系。

**唇音同步维度**：现有方法如 **Wav2Lip** (Prajwal et al., ACM MM 2020) 通过预训练同步判别器实现了高精度的唇音同步，但缺乏对说话风格的建模；**VideoRetalking** (Cheng et al., SIGGRAPH Asia 2022) 和 **MuseTalk** (Zhang et al., arXiv 2024) 在视频编辑和实时推理方面有所推进，但同样未涉及风格控制。PC-Talk 继承了 Wav2Lip 的同步损失设计思想（采用预训练的视听同步编码器计算余弦相似度损失 $\mathcal{L}_{sync}$），但在此基础上引入了风格感知的自回归变换器（LAC 模块），通过风格嵌入 $e_s$ 统一建模不同说话习惯，并支持对特定唇部发音的形状进行编辑。

**情感表达维度**：早期情感说话脸方法如 **EAMM** (Ji et al., SIGGRAPH 2022) 和 **EAT** (Gan et al., ICCV 2023) 主要从标签或参考图像直接生成表情，缺乏对情感强度和区域复合情感的精细控制。**ED-Talk** (Tan et al., ECCV 2024) 尝试解耦情感与唇音同步，但情感表达仍不够灵活。PC-Talk 的 EMC 模块通过“纯情感变形分解”（$D_e = \mathrm{CPred}(emo, e_a) - \mathrm{CPred}(\text{'neutral'}, e_a)$）实现了关键突破：从混合表情中减去中性表情，得到不含唇音耦合的纯情感变形，从而支持情感强度的连续调节和不同面部区域的独立情感控制（如眼睛区域愤怒、嘴部区域微笑的复合情感）。

**中间表示层面**：相较于 **SadTalker** (Zhang et al., CVPR 2023) 等基于 3D 形态模型的方法，以及 **EchoMimic** (Chen et al., arXiv 2024)、**Hallo-v2** (Cui et al., arXiv 2024)、**Sonic** (Ji et al., CVPR 2025) 等基于地标或隐式特征的方法，PC-Talk 采用具有语义含义的隐式关键点作为中间表示（通过地标约束训练），并直接在其上施加变形 $K_d = K_{ori} + D_l + D_e$，再通过变形模块和解码器渲染最终图像。这种设计在保持唇音同步精度的同时，为风格和情感的独立操控提供了自然的接口。

### 2. 适用边界与局限

根据论文提供的实验设置和量化结果，PC-Talk 的适用边界可归纳如下：

- **输入模态**：支持视频输入和单张图像输入两种模式。视频输入时姿态源来自视频本身，图像输入时姿态从预定义模板中随机选取。在 HDTF 数据集上，视频输入模式取得了 LSE-C 9.03、FID 15.51 的最优结果。
- **情感类别**：在 HDTF 和 MEAD 数据集上验证了多种情感类别的生成能力，情感准确率分别达到 46.19 和 72.32。但论文未明确测试更细粒度的情感类别（如惊奇、厌恶），其泛化能力需要手动验证。
- **风格编辑范围**：消融实验表明，唇部运动尺度在 0.8 附近时唇音同步最佳，风格编辑程度在 0.8–1.2 范围内性能稳定。超出此范围的效果未在论文中报告。
- **推理效率**：论文提供了效率对比（Table 4），但未讨论实时推理时的时延优化空间。对于高分辨率（4K）视频生成、动态背景或多人场景的适用性，论文未涉及，属于开放问题。

### 3. 开放问题

基于论文的方法设计和实验覆盖范围，以下问题值得后续关注：

1. **未见说话者的泛化能力**：风格和情感控制模块是否能在训练集未覆盖的说话者上保持稳定性能，论文未提供跨身份泛化实验。
2. **更细粒度情感类别的分解有效性**：纯情感变形分解方法是否适用于“惊奇”、“厌恶”等更微妙的情感类别，需要进一步验证。
3. **实时推理时延优化**：当前框架采用自回归变换器预测变形序列，推理时使用重叠窗口保证时序一致性，但时延能否进一步降低以满足实时交互需求，论文未深入讨论。
4. **高分辨率和复杂场景扩展**：方法是否适用于 4K 视频生成、动态背景或多人场景，论文未涉及，属于明显的适用边界外问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/PC_Talk_Precise_Facial_Animation_Control_for_Audio_Driven_Talking_Face_Generation.pdf]]
