---
title: "FRAMER: Frequency-Aligned Self-Distillation with Adaptive Modulation Leveraging Diffusion Priors for Real-World Image Super-Resolution"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FRAMER_Frequency_Aligned_Self_Distillation_with_Adaptive_Modulation_Leveraging_Diffusion_Priors_for_Real_World_Image_Super_Resolution.pdf
project_link: "https://cmlab-korea.github.io/FRAMER/"
code_link: null
aliases:
- FRAMER
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过引入频率对齐的自蒸馏训练方案（FRAMER），利用最终层特征图作为教师，将教师和学生特征通过FFT掩码分解为低频/高频带，并分别施加IntraCL（低频对比损失，用于稳定全局共享结构）和InterCL（高频对比损失，用于锐化实例特有细节），同时通过频率自适应权重（FAW）和频率对齐调制（FAM）动态调节各层各频带的蒸馏强度，从而将优化信号与网络内部频率...
primary_logic: 无需修改模型架构或推理过程，通过在训练时对扩散模型进行频率感知和层自适应的自蒸馏，即可即插即用地大幅提升真实图像超分辨率的感知质量和细节保真度。
claims:
- FRAMER在多个真实世界基准上显著提升感知和失真指标，如FRAMERU在DrealSR上将NIQE降低12.2%，MANIQA提高21.4%；FRAMERD在RealSR上将LPIPS降低10.4%，MANIQA提高22.9%。
- FRAMER显著加速了中间层的高频特征对齐（Layer 10–20），验证了“先低频后高频”层次结构的改善。
- FAW和FAM共同使用相较于单独使用或禁用取得了最佳性能，证实了自适应调制机制的有效性。
- 频率特定对比蒸馏（IntraCL + InterCL）在所有指标上均优于L2自蒸馏或无蒸馏基线，证明了频率分解和对比损失设计的优越性。
---

# FRAMER: Frequency-Aligned Self-Distillation with Adaptive Modulation Leveraging Diffusion Priors for Real-World Image Super-Resolution

> [!tip] 核心洞察
> 无需修改模型架构或推理过程，通过在训练时对扩散模型进行频率感知和层自适应的自蒸馏，即可即插即用地大幅提升真实图像超分辨率的感知质量和细节保真度。

| 字段 | 内容 |
|------|------|
| 中文题名 | FRAMER：面向真实世界图像超分辨率的频率对齐自适应调制自蒸馏框架 |
| 英文题名 | FRAMER: Frequency-Aligned Self-Distillation with Adaptive Modulation Leveraging Diffusion Priors for Real-World Image Super-Resolution |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.01390) · [Project](https://cmlab-korea.github.io/FRAMER/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FRAMER |
| Dataset | RealSR, DrealSR, RealLR200, RealLQ250 |

> [!tip] 效果简介
> - RealSR 上，PSNR↑ FRAMERU: 24.81 vs PiSA-SR: 24.02 (+3.3%)；PSNR↑ FRAMERD: 23.23 vs DiT4SR: 21.94 (+5.9%)；MANIQA↑ FRAMERU: 0.484 vs PiSA-SR: 0.412 (+17.5%)。
> - DrealSR 上，NIQE↓ FRAMERU: 5.386 vs PiSA-SR: 6.136 (-12.2%)；NIQE↓ FRAMERD: 5.959 vs DiT4SR: 6.780 (-12.1%)。
> - RealLR200 上，MUSIQ↑ FRAMERU: 73.38 vs PiSA-SR: 71.95 (+2.0%)。

## 概要

真实世界图像超分辨率（Real-ISR）的核心挑战在于从严重退化的低分辨率输入中恢复可信的高频细节。当前基于扩散模型的方法虽在感知质量上表现突出，却普遍受困于**低频偏差（LF bias）**——标准噪声预测损失天然偏向幅值占优的低频成分，而网络内部又呈现“先低频后高频”的层次结构，导致负责高频细化的深层长期欠优化。这直接造成恢复结果缺乏锐利纹理，边缘模糊或产生伪影。

针对这一瓶颈，本文提出 **FRAMER**（Frequency-Aligned Self-Distillation with Adaptive Modulation Leveraging Diffusion Priors），一种**即插即用的训练框架**。其核心思路是：在训练时以扩散模型最终层特征图为教师，将中间层特征通过2D FFT分解为低频（LF）和高频（HF）带，分别施加**频率对齐的对比自蒸馏损失**——低频用 IntraCL 稳定全局共享结构，高频用 InterCL 锐化实例特有细节；同时引入**频率自适应权重（FAW）**与**频率对齐调制（FAM）**，根据各层与教师的频率幅度差异及当前对齐程度动态调节蒸馏强度。整个过程不修改骨干网络架构，也不增加任何推理开销。

实验表明，FRAMER 在多个真实世界基准上显著且一致地提升感知与失真指标：在 RealSR 上，FRAMER_U 相较基线 PiSA-SR 的 MANIQA 提升 17.5%，NIQE 在 DrealSR 上降低 12.2%；FRAMER_D 相较 DiT4SR 的 MANIQA 提升 22.9%，LPIPS 降低 10.4%。消融研究进一步证实了频率特定对比损失设计和自适应调制模块各自的有效性，且额外训练成本极低（约 3% 内存、7% 时间）。

真实世界图像超分辨率（Real-ISR）旨在从包含未知复杂退化的低分辨率图像中恢复高分辨率细节，其核心挑战在于高频纹理的忠实重建。近年来，基于扩散模型的方法——如基于U-Net的**SeeSR**（Ren et al., CVPR 2024）、**PiSA-SR**（Lu et al., CVPR 2025）和基于DiT的**DreamClear**（Cao et al., NeurIPS 2024）、**DiT4SR**（Xie et al., ICCV 2025）——凭借强大的生成先验在感知质量上取得了显著突破。然而，这些方法在标准噪声预测损失的训练下，普遍存在一个深层瓶颈：**低频偏差（LF bias）**，即模型倾向于重建低频全局结构，而对高频细节的恢复不足。

这一偏差的根源可从两个层面理解。其一，自然图像的频率分布本身低频成分占优，低分辨率输入进一步加剧了这一不平衡。如Figure 2所示，对特征图进行2D FFT后，低频（LF）环内的幅度密度分布宽广且量级更大，而高频（HF）环内的幅度则集中在小值窄带内。标准噪声预测损失作为频率无关的统一目标，会自然偏向于降低总体损失的低频成分，导致高频信号的训练严重不足。

其二，扩散模型内部存在深度的“**先低频后高频**”层次结构。Figure 3通过测量各中间层与最终层特征图在LF和HF频带的余弦相似度揭示了这一现象：在U-Net和DiT骨干中，早期层已快速与最终层的LF特征对齐，而HF相似度直到后期层才急剧上升。这意味着常规频率无关损失向早期层提供了冗余的低频梯度，而负责高频细化的后期层却缺乏足够的优化信号，形成高频层欠优化的恶性循环。

现有方法对此问题的应对存在明显缺口：要么依赖架构修改或推理阶段的额外处理，要么在训练中保持频率无关的统一监督，未能从根本上抵消扩散模型内部的频率层次偏差。这引出了一个关键动机——**能否在不修改模型架构、不增加推理开销的前提下，通过训练时的频率感知策略，系统性地纠正低频偏差？**

FRAMER正是基于这一动机，提出了一种即插即用的频率对齐自蒸馏训练框架，利用扩散模型内部最终层特征图作为教师，通过频带分解和对比学习，将优化信号与网络内部的频率层次对齐，从而有效释放扩散先验在高频细节重建上的潜力。

## 核心方法与创新机理

FRAMER的核心创新在于**首次揭示并系统性地解决了扩散模型在真实图像超分辨率中的“低频偏差”（LF bias）问题**，并据此设计了一套完全即插即用的训练框架。该框架无需修改模型架构或推理过程，仅通过在训练时引入频率感知的层自适应自蒸馏机制，即可显著提升细节保真度和感知质量。

### 1. 问题诊断：扩散模型的低频偏差

标准扩散模型在真实图像超分辨率中存在严重的高频细节重建不足，其根源在于两个相互叠加的低频偏差机制：

- **数据层面的频率不平衡**：自然图像的频率分布本身低频占优，低分辨率输入进一步加剧了这一不平衡（Figure 2）。标准的噪声预测损失在优化时会自然偏向于降低总体损失的低频成分，导致高频信号的训练梯度相对不足。
- **网络内部的“先低频后高频”层次结构**：扩散模型的U-Net或DiT骨干网络在去噪过程中呈现出深度的频率学习层次——早期层迅速学习低频特征，而高频特征的对齐在后期层才突然上升（Figure 3）。常规的频率无关损失向早期层提供了冗余的低频梯度，而负责高频细化的后期层却缺乏足够的优化信号，形成了“低频层过优化、高频层欠优化”的结构性偏差。

### 2. 解决方案：频率对齐的自蒸馏框架

FRAMER通过以下三个关键设计，将优化信号与网络内部的频率层次精确对齐，有效抵消了上述低频偏差：

#### 2.1 频率分解与对比自蒸馏

FRAMER以扩散模型的最终层特征图作为教师，通过2D FFT掩码将教师和所有中间层学生的特征图分解为低频（LF）和高频（HF）两个频带，并针对不同频带的特性设计了差异化的对比损失：

- **IntraCL（低频对比损失）**：针对低频特征跨样本高度相似的特点（Figure 5a），IntraCL仅在同一图像内进行对比——将学生LF特征拉向教师，同时推离同一网络中随机采样的其他层LF特征，不使用跨批次负样本。这种设计稳定了全局共享结构的学习，避免了跨样本负样本可能引入的语义混淆。

  $$\mathcal { L } _ { \mathrm { I n t r a C L } } ^ { ( i ) } = - \log \frac { \exp \left( s _ { + , \mathrm { L F } } ^ { ( i ) } \right) } { \exp \left( s _ { + , \mathrm { L F } } ^ { ( i ) } \right) + \exp \left( s _ { - , \mathrm { L F } } ^ { ( i ) } \right) }$$

- **InterCL（高频对比损失）**：针对高频特征跨样本差异大、实例特异性强的特点（Figure 5b），InterCL在拉近学生HF特征与教师的同时，推离两类负样本——同一图像内的随机层HF负样本和批次中其他图像的HF负样本。这种设计强化了模型对实例特有细节的判别能力，有效锐化了高频纹理。

  $$\mathcal { L } _ { \mathrm { I n t e r C L } } ^ { ( i ) } = - \log \frac { \exp \left( s _ { + , \mathrm { H F } } ^ { ( i ) } \right) } { \exp \left( s _ { + , \mathrm { H F } } ^ { ( i ) } \right) + \exp \left( s _ { - , \mathrm { H F } } ^ { ( i ) } \right) + S _ { \mathrm { n e g } } ^ { ( i ) } }$$

消融实验证实，将IntraCL专用于低频、InterCL专用于高频的组合优于将同一种损失同时用于两个频带的配置（Table 4），验证了频率特定损失设计的必要性。

#### 2.2 频率自适应权重（FAW）

为将蒸馏信号与网络的“先低频后高频”层次结构对齐，FRAMER引入了频率自适应权重（FAW）。FAW根据各中间层相对于最终层的频率幅度差异，自适应地为每层计算LF和HF的蒸馏权重：

$$\mathbf { w } _ { \mathrm { L F } } ^ { ( i ) } = \frac { 1 } { 1 + \Delta _ { \mathrm { L F } } ^ { ( i ) } } , \quad \mathbf { w } _ { \mathrm { H F } } ^ { ( i ) } = \frac { 1 } { 1 + \Delta _ { \mathrm { H F } } ^ { ( i ) } }$$

其中 $\Delta$ 为各层与最终层的频率幅度差异。差异越大，权重越小——这意味着早期层因其LF特征已接近最终层而获得较强的LF蒸馏信号，而后期层因其HF特征尚未对齐而获得较强的HF蒸馏信号，从而实现了优化信号与网络内部频率学习进度的精确匹配。

#### 2.3 频率对齐调制（FAM）

在训练初期，中间层特征尚未与教师建立有效对齐，此时施加过强的蒸馏信号可能导致训练不稳定甚至模型崩溃。FAM通过当前学生-教师对齐得分（余弦相似度）门控FAW权重，在特征尚未对齐时自动抑制蒸馏强度：

$$\tilde { w } _ { \mathrm { L F } } ^ { ( i ) } = w _ { \mathrm { L F } } ^ { ( i ) } \cdot \mathrm { s t o p g r a d } ( a _ { \mathrm { L F } } ^ { ( i ) } ) , \quad \tilde { w } _ { \mathrm { H F } } ^ { ( i ) } = w _ { \mathrm { H F } } ^ { ( i ) } \cdot \mathrm { s t o p g r a d } ( a _ { \mathrm { H F } } ^ { ( i ) } )$$

FAM使用stop-gradient操作，确保对齐得分仅用于门控权重而不参与梯度回传，避免了对齐目标与蒸馏目标的冲突。训练初期稳定性分析（Figure 8）表明，完整FRAMER（含FAW和FAM）在训练早期即能有效防止模型崩溃，而单独使用FAW或FAM的变体则出现不稳定或非相干结构。

### 3. 最终训练目标

每层经FAM门控的蒸馏损失与标准噪声预测损失共同构成总训练目标：

$$\mathcal { L } _ { \mathrm { t o t a l } } = \mathcal { L } _ { \mathrm { n o i s e } } + \sum _ { i = 1 } ^ { N } \left( \tilde { w } _ { \mathrm { L F } } ^ { ( i ) } \mathcal { L } _ { \mathrm { I n t r a C L } } ^ { ( i ) } + \tilde { w } _ { \mathrm { H F } } ^ { ( i ) } \mathcal { L } _ { \mathrm { I n t e r C L } } ^ { ( i ) } \right)$$

### 4. 与基线方法的关键差异

FRAMER相对于现有方法的changed slots清晰体现了其创新本质：

| 维度 | 基线方法 | FRAMER |
|------|----------|--------|
| **训练损失目标** | 单一噪声预测损失 | 噪声预测损失 + 频率对齐对比自蒸馏 |
| **特征分解** | 无频率分解 | 2D FFT掩码分解为LF/HF频带 |
| **教师选择** | 无（所有层接受标准监督） | 最终层为教师，中间层为学生 |
| **自适应调制** | 无（固定等权重损失） | FAW + FAM动态调节各层各频带蒸馏强度 |

这些差异使得FRAMER在不改变推理过程的前提下，仅引入约3%的内存和7%的训练时间开销（Figure 6），即可在多个真实世界基准上显著超越基线方法——例如FRAMERD在RealSR上将MANIQA提升22.9%，FRAMERU在DrealSR上将NIQE降低12.2%（Table 1）。

FRAMER 是一种即插即用的训练框架，在不修改扩散骨干网络架构和推理过程的前提下，通过频率对齐的自蒸馏机制来缓解扩散模型在真实图像超分辨率中的低频偏差问题。其整体 pipeline 如图 4(a) 所示，核心思想可概括为：**以最终层特征图为教师，将中间层特征图按频率分解后，分别施加低频对比损失和高频对比损失，并通过自适应调制模块动态调节各层各频带的蒸馏强度**。

### 训练流程

训练时，给定一张高分辨率图像 $R$，首先通过随机退化管道生成对应的低分辨率输入 $I_{LR}$，并利用 LLaVA 生成语义描述文本作为条件。扩散骨干网络（U-Net 或 DiT）接收 $I_{LR}$、噪声 $Z_T$ 和文本条件，执行去噪过程。FRAMER 仅在训练阶段介入，在标准噪声预测损失 $\mathcal{L}_{\text{noise}}$ 之外，为每一中间层添加辅助蒸馏损失：

$$
\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{noise}} + \sum_{i=1}^{N} \mathcal{L}_{\text{FRAMER}}^{(i)}
$$

其中 $\mathcal{L}_{\text{FRAMER}}^{(i)}$ 为第 $i$ 层的频率对齐自蒸馏损失。推理时完全移除 FRAMER 模块，使用原始骨干网络，不增加任何推理开销。

### 模块关系与数据流

FRAMER 由四个核心模块串联构成，形成从特征分解到自适应调制的完整信号链：

1. **频率分解模块**：对中间层特征图进行 2D FFT，通过掩码将其分解为低频（LF）和高频（HF）两个频带。教师（最终层）和学生（中间层）的特征均经过相同的频率分解。

2. **IntraCL（低频对比损失）**：作用于 LF 频带。将学生 LF 特征拉近教师 LF 特征，同时推离同一图像内随机采样层的 LF 特征（无跨批次负样本），以稳定全局共享结构的表征学习。

3. **InterCL（高频对比损失）**：作用于 HF 频带。将学生 HF 特征拉近教师 HF 特征，同时推离同一图像内随机层的 HF 特征以及批次内其他图像的 HF 特征，以锐化实例特有的高频细节。

4. **FAW + FAM 自适应调制**：FAW（Frequency-based Adaptive Weight）根据各层相对于最终层的频率幅度差异，为每层的 LF/HF 分支计算基础蒸馏权重——幅度差异越大，权重越小。FAM（Frequency-based Alignment Modulation）进一步通过当前学生-教师对齐程度（余弦相似度）对 FAW 权重进行门控：当某频带尚未对齐时，抑制该频带的蒸馏信号，防止早期训练崩溃。经 FAM 调制后的最终层蒸馏损失为：

$$
\mathcal{L}_{\text{FRAMER}}^{(i)} = \tilde{w}_{\text{LF}}^{(i)} \mathcal{L}_{\text{IntraCL}}^{(i)} + \tilde{w}_{\text{HF}}^{(i)} \mathcal{L}_{\text{InterCL}}^{(i)}
$$

其中 $\tilde{w}_{\text{LF}}^{(i)}$ 和 $\tilde{w}_{\text{HF}}^{(i)}$ 分别为经 FAM 门控后的 LF 和 HF 权重。

### 设计逻辑

该框架的设计直接回应了扩散模型的两个低频偏差成因：（1）自然图像频率分布中低频占优，标准噪声预测损失偏向低频成分；（2）网络内部呈现“先低频后高频”的层次结构，早期层已稳定学习低频特征，而负责高频细化的后期层缺乏足够的优化信号。通过将蒸馏信号按频率分解并与网络层次对齐，FRAMER 将优化压力精准地导向欠优化的高频层，同时通过自适应调制避免早期层接收冗余的低频梯度，从而在不改变推理过程的前提下显著提升高频细节的保真度。

如图 6 所示，FRAMER 引入的训练开销极小（约 3% 内存，7% 时间），且完全不影响推理速度，验证了其作为即插即用训练方案的实用价值。

![[assets/figures/papers/paper_list_l875_https_arxiv_org_abs_2512_01390/figures/004_Figure_4.jpg]]
*Figure 4: FRAMER: Frequency-Aligned Self-Distillation with Adaptive Modulation Leveraging Diffusion Priors (inspired by Sec. 3.1). (a) Framework Overview. During training, from an High-Resolution image R, we create*

FRAMER 的核心设计围绕一个关键洞察展开：扩散模型内部存在“先低频后高频”的深度层次结构，而标准的噪声预测损失无法为负责高频细化的后期层提供足够的优化信号。为此，FRAMER 构建了一套频率感知的层自适应自蒸馏机制，包含四个紧密协作的模块。

### 频率分解与教师选择

FRAMER 在训练的每个去噪步骤中，将扩散骨干的最终层特征图作为教师，所有中间层作为学生。对每一层的特征图，通过 2D FFT 将其分解为低频（LF）和高频（HF）两个频带。具体而言，在频域中定义低频掩码 $M_{\mathrm{LF}}$ 和高频掩码 $M_{\mathrm{HF}}$，分别提取对应频率成分。这一分解是后续所有对比损失和自适应调制的基础。

### IntraCL：低频对比损失

低频成分在跨样本间表现出高度相似性（见 Figure 5），反映了共享的全局结构信息。为稳定低频结构学习，FRAMER 设计了 IntraCL（Intra Contrastive Loss），其核心思想是：在单张图像内部，将学生层的 LF 特征拉近教师层的 LF 特征，同时推远一个随机采样的同图其他层的 LF 特征。损失函数形式为：

$$\mathcal{L}_{\mathrm{IntraCL}}^{(i)} = -\log \frac{\exp\left(s_{+,\mathrm{LF}}^{(i)}\right)}{\exp\left(s_{+,\mathrm{LF}}^{(i)}\right) + \exp\left(s_{-,\mathrm{LF}}^{(i)}\right)}$$

其中 $s_{+,\mathrm{LF}}^{(i)}$ 表示第 $i$ 层学生 LF 特征与教师 LF 特征的余弦相似度，$s_{-,\mathrm{LF}}^{(i)}$ 表示学生 LF 特征与随机层负样本 LF 特征的余弦相似度。IntraCL 不使用跨批次负样本，仅依靠同图内的对比来稳定全局结构，避免过度锐化。

### InterCL：高频对比损失

高频成分在跨样本间相似度低、实例特异性强（见 Figure 5），需要更强的判别性优化信号。InterCL（Inter Contrastive Loss）将学生 HF 特征拉近教师 HF 特征，同时推离两类负样本：同图随机层 HF 特征和批次中其他图像的 HF 特征。损失函数为：

$$\mathcal{L}_{\mathrm{InterCL}}^{(i)} = -\log \frac{\exp\left(s_{+,\mathrm{HF}}^{(i)}\right)}{\exp\left(s_{+,\mathrm{HF}}^{(i)}\right) + \exp\left(s_{-,\mathrm{HF}}^{(i)}\right) + S_{\mathrm{neg}}^{(i)}}$$

其中 $S_{\mathrm{neg}}^{(i)}$ 聚合了批次内所有其他图像作为负样本的相似度得分。通过引入跨批次负样本，InterCL 直接抵消低频偏差，为高频成分提供有针对性的优化信号，帮助模型恢复精细的纹理和边缘细节。

### FAW：频率自适应权重

网络内部存在深度的频率层次结构：早期层已较好地学习低频特征，而高频特征在后期层才逐渐对齐（见 Figure 3）。为将蒸馏损失与这一层次对齐，FAW（Frequency-based Adaptive Weight）根据各层相对于最终层的频率幅度差异，自适应地计算每层 LF/HF 的蒸馏权重。首先计算每层各频带的平均幅度：

$$E_{\mathrm{LF}}^{(i)} = \frac{\sum\left(|\mathbf{F}^{(i)}| \odot M_{\mathrm{LF}}\right)}{\sum M_{\mathrm{LF}} + \varepsilon}, \quad E_{\mathrm{HF}}^{(i)} = \frac{\sum\left(|\mathbf{F}^{(i)}| \odot M_{\mathrm{HF}}\right)}{\sum M_{\mathrm{HF}} + \varepsilon}$$

然后计算各层与最终层（第 $n$ 层）的幅度差异 $\Delta_{\mathrm{LF}}^{(i)} = |E_{\mathrm{LF}}^{(i)} - E_{\mathrm{LF}}^{(n)}|$ 和 $\Delta_{\mathrm{HF}}^{(i)} = |E_{\mathrm{HF}}^{(i)} - E_{\mathrm{HF}}^{(n)}|$。权重由幅度差异的倒数决定——差异越大，说明该层在该频带尚未对齐，权重应越小：

$$\mathbf{w}_{\mathrm{LF}}^{(i)} = \frac{1}{1 + \Delta_{\mathrm{LF}}^{(i)}}, \quad \mathbf{w}_{\mathrm{HF}}^{(i)} = \frac{1}{1 + \Delta_{\mathrm{HF}}^{(i)}}$$

这一设计使得低频蒸馏在早期层获得较高权重，而高频蒸馏在后期层获得较高权重，实现了优化信号与网络内部频率层次的自然对齐。

### FAM：频率对齐调制

在训练早期，学生层与教师层的特征对齐程度较低，直接施加 FAW 权重可能导致训练不稳定甚至模型崩溃。FAM（Frequency-based Alignment Modulation）通过当前学生-教师对齐程度对 FAW 权重进行门控。首先计算各层 LF/HF 特征与教师对应特征的余弦相似度作为对齐得分 $a_{\mathrm{LF}}^{(i)}$ 和 $a_{\mathrm{HF}}^{(i)}$，然后通过 stop-gradient 操作进行门控：

$$\tilde{w}_{\mathrm{LF}}^{(i)} = w_{\mathrm{LF}}^{(i)} \cdot \mathrm{stopgrad}(a_{\mathrm{LF}}^{(i)}), \quad \tilde{w}_{\mathrm{HF}}^{(i)} = w_{\mathrm{HF}}^{(i)} \cdot \mathrm{stopgrad}(a_{\mathrm{HF}}^{(i)})$$

当对齐得分较低时，FAM 自动抑制该层的蒸馏强度，防止早期崩溃；随着训练推进、对齐程度提升，蒸馏强度自然增强（见 Figure 9）。最终，第 $i$ 层的蒸馏损失为：

![[assets/figures/papers/paper_list_l875_https_arxiv_org_abs_2512_01390/figures/015_Figure_9.jpg]]
*Figure 9: Visualization of FAW/FAM weights across layers. (a) Early training phase and (b) Late training phase. The visualizations confirm the intended behavior: HF supervision is relatively weak across most layers early on, and strengthens across more layers later in the training process*

$$\mathcal{L}_{\mathrm{FRAMER}}^{(i)} = \tilde{w}_{\mathrm{LF}}^{(i)} \mathcal{L}_{\mathrm{IntraCL}}^{(i)} + \tilde{w}_{\mathrm{HF}}^{(i)} \mathcal{L}_{\mathrm{InterCL}}^{(i)}$$

总训练目标为标准噪声预测损失与所有中间层蒸馏损失之和：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{noise}} + \sum_{i=1}^{N} \mathcal{L}_{\mathrm{FRAMER}}^{(i)}$$

消融实验（Table 5）证实，FAW 和 FAM 共同使用在所有指标上均取得最佳性能：单独使用 FAW 易产生过度锐化伪影，单独使用 FAM 则感知质量不足，二者协同才能实现结构连贯性与感知真实感的最优平衡。

![[assets/figures/papers/paper_list_l875_https_arxiv_org_abs_2512_01390/figures/002_Figure_2.jpg]]
*Figure 2: Band-wise magnitude densities with shared bins. For each feature map, we compute the 2D FFT and collect magnitudes |F | within LF and HF rings. We plot mean ± σ densities over samples for log(1+|F |) using common bin edges (HF: red or yellow, LF: blues). LF magnitudes span a broader and heavier range, whereas HF magnitudes concentrate narrowly near small values, indicating LF dominance that biases unified training toward LF and undertrains HF details. All statistics are computed on the 100- image DIV2K [1] test set. Densities integrate to 1; any right-edge spike is due to percentile clipping used only for visualization*

## 实验与关键发现

### 主实验结果

FRAMER在多个真实世界超分辨率基准上对感知质量和像素保真度均实现了跨架构的显著提升。Table 1汇总了在RealSR、DrealSR、RealLR200和RealLQ250四个数据集上的量化比较，方法按架构类型分组（Swin-based、U-Net-based、DiT-based）。

在U-Net骨干上，**FRAMERU**以**PiSA-SR**（Lu et al., CVPR 2025）为基线。在RealSR上，PSNR从24.02提升至24.81（+3.3%），MANIQA从0.412提升至0.484（+17.5%）；在DrealSR上，NIQE从6.136降至5.386（-12.2%），MANIQA从0.402提升至0.488（+21.4%）。在无GT的RealLR200和RealLQ250上，MUSIQ和MANIQA分别获得2.0%和9.6%的相对提升。

在DiT骨干上，**FRAMERD**以**DiT4SR**（Xie et al., ICCV 2025）为基线。在RealSR上，PSNR从21.94提升至23.23（+5.9%），MANIQA从0.459提升至0.564（+22.9%），LPIPS从0.413降至0.370（-10.4%）；在DrealSR上，NIQE从6.780降至5.959（-12.1%）。在RealLR200上MUSIQ提升2.8%，在RealLQ250上MANIQA提升7.7%。

图Figure 1的定性比较进一步验证了上述量化结果：FRAMER生成的边缘更清晰，细节更丰富，视觉效果更自然。值得强调的是，这些提升是在**不修改模型架构、不增加推理开销**的前提下实现的——FRAMER仅作为训练时的即插即用框架，推理阶段与原始骨干完全一致。

### 消融研究

#### 蒸馏目标的选择

Table 2比较了不同蒸馏目标对性能的影响。以无蒸馏的噪声预测损失为基线，L2自蒸馏在部分感知指标上有所改善，但频率特定的对比蒸馏（+CL-Freq Distill.）在所有指标上均取得最优结果。这验证了将特征分解为低频和高频带并分别施加对比损失的策略，相较于简单的最小化特征距离，能更有效地传递频率感知的监督信号。

#### 对比组件的设计

Table 3消融了对比学习的核心组件。采用最终层作为教师并结合随机层负样本的配置取得了最佳性能，验证了“最终层特征图包含最丰富的去噪信息”这一设计动机。移除随机层负样本或改用固定层教师均导致性能下降，表明随机负采样对于构建有效的对比学习空间至关重要。

#### 低频/高频损失的最优组合

Table 4探索了IntraCL和InterCL在低频和高频带上的分配策略。将IntraCL用于低频且InterCL用于高频的组合优于将同一种损失同时用于两个频带的配置。这一结果与图Figure 5揭示的频率特性一致：低频特征跨样本相似度高（共享结构信息），适合仅使用同图内负样本的IntraCL来稳定全局结构学习；高频特征跨样本相似度低（实例特有细节），需要引入跨图负样本的InterCL来锐化细节辨别能力。

#### 自适应调制机制的有效性

Table 5系统消融了FAW（频率自适应权重）和FAM（频率对齐调制）的贡献。完整方案（FAW + FAM）在所有指标上取得最佳结果。单独使用FAW虽然优于无自适应调制，但在某些情况下可能导致过度锐化伪影（图Figure 10）；单独使用FAM则感知质量提升不足。两者协同工作时，FAM通过当前对齐程度门控FAW权重，在训练早期抑制未对齐层的蒸馏信号（图Figure 9a），防止模型崩溃（图Figure 8），在训练后期逐步释放HF监督强度（图Figure 9b），实现了稳定且高效的频率层次对齐。

#### 训练成本与稳定性

图Figure 6显示，FRAMER引入的额外训练开销极小：内存增加约3%，每迭代时间增加约7%。考虑到其即插即用特性，推理成本与原始骨干完全一致。图Figure 8的可视化分析表明，在训练初期（1k–5k迭代），无自适应调制的蒸馏变体出现不稳定或结构不连贯现象，而完整FRAMER方案展现出稳定的优化轨迹，有效防止了早期模型崩溃。

### 内部频率层次的对齐效果

图Figure 7通过层间余弦相似度定量验证了FRAMER对网络内部频率层次的改善效果。在基线DiT4SR中，HF特征在中间层（Layer 10–20）的对齐显著滞后于LF特征，呈现明显的“先低频后高频”层次结构。FRAMER显著加速了这些中间层的HF特征对齐，使HF相似度曲线整体上移，验证了频率对齐蒸馏有效抵消了网络内部的频谱偏差。

### 跨范式泛化验证

Table 7展示了FRAMER在一步式扩散模型和GAN增强扩散模型上的泛化性能。无论底层扩散范式如何变化，FRAMER均能一致提升保真度和感知指标，证明了该训练框架的通用性。

### 用户研究

Table 8的用户研究结果显示，在同架构组内比较中，FRAMERU和FRAMERD分别获得了最高的胜率，表明人类评估者在感知质量上显著偏好FRAMER的恢复结果。

### 失败模式与局限性

尽管FRAMER在感知质量上达到了SOTA水平，图Figure 11揭示了生成式模型固有的权衡：在极端退化下（如复杂的绳纹结构），FRAMERD生成的细节虽然感知上远优于基线，但可能与GT存在细微的结构偏差。这反映了感知真实感和像素忠实度之间的根本性张力。此外，该方法依赖于扩散模型的多步采样，推理速度受限于原始骨干，但FRAMER本身未引入额外推理开销。

![[assets/figures/papers/paper_list_l875_https_arxiv_org_abs_2512_01390/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison of real-world image super-resolution methods. We evaluate both fidelity metrics (PSNR↑, SSIM↑, LPIPS↓) and perceptual quality metrics (NIQE↓, MANIQA↑, MUSIQ↑). Methods are grouped by architecture type (Swin-based, U-Netbased, DiT-based). Best and Second best results are highlighted. The green percentages for our FRAMER models indicate the relative improvement over their respective baselines, PiSA-SR (for FRAMERU) and DiT4SR (for FRAMERD)*

![[assets/figures/papers/paper_list_l875_https_arxiv_org_abs_2512_01390/figures/007_Table_2.jpg]]
*Table 2: Ablation on the distillation objective. Metrics are on RealSR. The best per column is in bold*

![[assets/figures/papers/paper_list_l875_https_arxiv_org_abs_2512_01390/figures/012_Figure_6.jpg]]
*Figure 6: Comparison of Training Cost (Memory and Time). We measure the GPU memory usage and time per iteration for DiT4SR and FRAMERD on an NVIDIA H200 GPU with a batch size of 16. FRAMER introduces only a marginal training overhead ( 3% memory, 7% time) while maintaining identical inference costs due to its plug-and-play nature*

## 定位与知识库关联

### 1. 问题定位：扩散模型在真实图像超分中的低频偏差

真实世界图像超分辨率（Real-ISR）的核心挑战在于从严重退化、噪声和模糊的低分辨率输入中恢复出逼真且忠实于原图的高频细节。近年来，基于扩散先验的方法（如 **ResShift** (Yue et al., NeurIPS 2023)、**SeeSR** (Ren et al., CVPR 2024)、**PiSA-SR** (Lu et al., CVPR 2025)、**DreamClear** (Cao et al., NeurIPS 2024)、**DiT4SR** (Xie et al., ICCV 2025)）凭借预训练文本到图像（T2I）扩散模型强大的生成先验，在感知质量上大幅超越了传统的基于回归的方法（如 **SwinIR** (Liang et al., ICCV 2021)）。

然而，FRAMER 的工作揭示了一个被普遍忽视的瓶颈：**标准扩散模型的噪声预测损失存在严重的低频偏差（LF bias）**。其成因有二：

1.  **数据层面的频率不平衡**：自然图像的能量谱本身低频成分占绝对优势，低分辨率输入进一步加剧了这种不平衡。标准的 $L_2$ 或 $L_1$ 噪声预测损失在优化时会天然地偏向于能最大程度降低总体损失的低频成分，导致高频信号在训练中得不到充分优化（见 Figure 2 的频率幅度密度分布）。
2.  **网络内部的“先低频后高频”层次结构**：通过对 U-Net 和 DiT 各层特征图与最终层特征图在低频和高频上的余弦相似度分析，FRAMER 发现扩散去噪网络内部存在深度的频率层次——早期层已稳定学习并传递低频结构信息，而高频细节的精细化处理集中在后期层。然而，频率无关的统一损失函数会向早期层提供冗余的低频梯度，同时后期负责高频细化的层却缺乏足够的优化信号，导致高频层欠优化（见 Figure 3 的层间相似度曲线）。

这一发现将 Real-ISR 的性能瓶颈从“生成能力不足”重新定义为“**训练信号与网络内部频率处理层次之间的错配**”，为后续工作指明了新的优化方向。

### 2. 核心贡献：频率对齐的自蒸馏与自适应调制

FRAMER 的核心贡献在于提出了一套**无需修改模型架构或推理过程的即插即用训练方案**，通过频率感知和层自适应的自蒸馏，将优化信号与扩散网络内部的频率层次对齐，从而系统性地抵消低频偏差。其知识库定位可分解为以下几个关键创新点：

#### 2.1 频率分解与对比自蒸馏

与传统的知识蒸馏（通常使用 $L_2$ 损失对齐师生特征）不同，FRAMER 引入了**频率分解的自蒸馏**机制：

-   **教师选择**：以去噪网络的最终层特征图作为教师，所有中间层作为学生。这一选择的依据是最终层已融合了完整的去噪信息，且在频率上最为均衡（见 Table 3 的消融实验，最终层教师优于其他层）。
-   **频率分解**：通过 2D FFT 将师生特征图分解为低频（LF）和高频（HF）两个频带，并针对不同频带的特性设计了差异化的对比损失：
    -   **IntraCL（低频对比损失）**：用于稳定全局共享结构的学习。它仅使用同图内的正样本（教师）和随机层负样本，不引入跨批次负样本。这是因为低频特征在不同图像间具有高度相似性（见 Figure 5 的相似度矩阵），引入跨图负样本可能导致结构信息的错误排斥。
    -   **InterCL（高频对比损失）**：用于锐化实例特有的高频细节。它在同图随机层负样本的基础上，额外引入了批次中其他图像的高频特征作为负样本。由于高频特征具有强实例特异性（见 Figure 5），跨图负样本能有效促使学生特征与教师对齐，同时远离其他图像的无关细节，避免过度锐化。

Table 2 的消融实验证实，这种频率特定的对比蒸馏（+CL-Freq Distill.）在所有指标上均显著优于 $L_2$ 自蒸馏和无蒸馏基线。Table 4 进一步验证了“低频用 IntraCL、高频用 InterCL”的组合是最优的，将同一种损失同时用于两个频带会导致性能下降。

#### 2.2 频率自适应调制（FAW 与 FAM）

为了进一步将蒸馏强度与网络内部的频率层次对齐，FRAMER 引入了两个自适应调制模块：

-   **FAW（频率自适应权重）**：根据每层相对于最终层的频率幅度差异，为每层的 LF 和 HF 蒸馏损失计算自适应权重。幅度差异越大，说明该层在该频带上的特征与教师差距越大，权重越小。这实现了“早期层弱监督、后期层强监督”的层次化训练。
-   **FAM（频率对齐调制）**：通过当前学生-教师特征的对齐程度（余弦相似度）门控 FAW 权重。在训练初期，当学生特征尚未与教师对齐时，FAM 会抑制蒸馏信号的强度，防止因强行对齐导致的训练崩溃。随着训练进行，对齐程度提高，FAM 逐渐释放完整的蒸馏权重。

Table 5 的消融实验表明，FAW 和 FAM 共同使用取得了最佳性能。单独使用 FAW 可能导致过度锐化伪影，单独使用 FAM 则感知质量不足（见 Figure 10 的定性对比）。Figure 9 的权重可视化进一步证实了 FAW/FAM 的预期行为：训练早期，HF 监督在大多数层上较弱；训练后期，HF 监督在更多层上增强。

### 3. 方法谱系定位

FRAMER 在 Real-ISR 方法谱系中的定位如下：

-   **相对于基于回归的方法**（如 SwinIR）：FRAMER 继承了扩散模型强大的生成先验，在感知质量上有代际优势。
-   **相对于基于扩散的 Real-ISR 方法**（如 ResShift、SeeSR、PiSA-SR、DreamClear、DiT4SR）：FRAMER 不修改骨干网络架构或采样过程，而是通过**训练时的频率感知自蒸馏**来提升性能。它是对现有扩散 SR 方法的**正交增强**，可以即插即用地应用于 U-Net 和 DiT 等不同架构的骨干网络。
-   **相对于知识蒸馏方法**：FRAMER 属于**自蒸馏**范畴（教师和学生来自同一网络），但其创新在于引入了**频率分解**和**对比学习**，而非传统的 $L_2$ 特征匹配。此外，**层自适应调制（FAW/FAM）** 使其能够感知并利用网络内部的频率层次结构。
-   **相对于频率感知的图像恢复方法**：已有工作（如 FouriScale）在推理时通过频率约束来减少扩散模型的生成伪影。FRAMER 则是在**训练时**通过频率对齐来从根本上改善模型的特征学习，两者是互补的。

### 4. 适用边界与局限性

尽管 FRAMER 在多个基准上取得了 SOTA 性能，其适用边界和局限仍需明确：

-   **生成式模型的固有幻觉**：FRAMER 无法完全消除扩散模型固有的幻觉问题。在极端退化下，恢复的纹理可能与原始纹理存在细微的结构偏差（如 Figure 11 所示的绳纹结构），这反映了感知真实感和像素忠实度之间的根本权衡。在需要严格像素级保真度的任务（如医学影像、卫星遥感）中，需谨慎使用。
-   **推理速度**：FRAMER 仅修改训练过程，不增加推理开销，因此其推理速度与原始扩散骨干网完全一致。这意味着它继承了扩散模型多步采样的速度瓶颈，与一步式方法相比仍有差距。但 Table 7 表明，FRAMER 同样可以泛化到一步式扩散模型上并取得一致提升。
-   **训练开销**：FRAMER 引入的额外训练开销很小（约 3% 内存，7% 时间，见 Figure 6），在工程上具有高度可行性。
-   **超参数敏感性**：FAW 和 FAM 模块中的频率阈值等超参数对最终性能的敏感性如何，论文未进行系统消融，需要手动验证。

### 5. 开放问题

FRAMER 为后续研究开辟了若干方向：

1.  **训练-推理频率协同**：如何将训练时的频率对齐自蒸馏与推理时的频率约束采样（如 FouriScale）相结合，以进一步减少生成式伪影并提高细节忠实度？
2.  **跨任务泛化**：FRAMER 的自蒸馏框架能否扩展到其他生成式恢复任务，如视频超分辨率、去模糊、去雾等？这些任务中是否也存在类似的频率层次结构？
3.  **更大规模模型的适配**：在更大型的扩散模型（如 Stable Diffusion XL、Flux）上应用 FRAMER 的效果如何？FAW/FAM 模块是否需要针对不同深度的网络进行调节？
4.  **频率阈值的自适应学习**：当前 FAW 的频率掩码阈值是预定义的，是否可以设计可学习的频率分解策略，使模型自适应地确定最优的 LF/HF 分界？
5.  **与提示工程的协同**：FRAMER 使用 LLaVA 生成文本提示，频率对齐训练是否可以通过更精细的提示工程（如引入频率相关的文本描述）获得进一步提升？

## 原文 PDF

![[paperPDFs/CVPR_2026/FRAMER_Frequency_Aligned_Self_Distillation_with_Adaptive_Modulation_Leveraging_Diffusion_Priors_for_Real_World_Image_Super_Resolution.pdf]]
