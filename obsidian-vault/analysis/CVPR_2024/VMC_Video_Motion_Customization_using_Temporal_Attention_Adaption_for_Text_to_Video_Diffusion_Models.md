---
title: "VMC: Video Motion Customization using Temporal Attention Adaption for Text-to-Video Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/VMC_Video_Motion_Customization_using_Temporal_Attention_Adaption_for_Text_to_Video_Diffusion_Models.pdf
project_link: https://video-motion-customization.github.io/
code_link: null
aliases:
- VVMC
- VMC
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "仅微调关键帧生成模块中的时序注意力层，并采用基于连续帧残差向量（运动向量）的运动蒸馏目标（最大化 epsilon 残差的余弦相似度），实现运动与外观的解耦。"
primary_logic: "连续帧之间的残差向量（运动向量）自然编码了运动轨迹信息。通过在不同噪声水平下对齐预测的 epsilon 残差与真实 epsilon 残差，可以高效地多尺度蒸馏运动信息到时序注意力层中；同时结合外观不变提示词，抑制背景和外观干扰，实现干净的运动学习。"
claims:
- "VMC 仅微调时序注意力层，而非整个模型或空间注意力。"
- "运动蒸馏目标使用连续帧间残差向量作为运动参考，并对齐 epsilon 残差的余弦相似度。"
- "外观不变提示词通过移除背景描述，进一步促进运动学习。"
- "VMC 训练高效（15GB vRAM，5分钟内完成）。"
---

# VMC: Video Motion Customization using Temporal Attention Adaption for Text-to-Video Diffusion Models

> [!tip] 核心洞察
> 连续帧之间的残差向量（运动向量）自然编码了运动轨迹信息。通过在不同噪声水平下对齐预测的 epsilon 残差与真实 epsilon 残差，可以高效地多尺度蒸馏运动信息到时序注意力层中；同时结合外观不变提示词，抑制背景和外观干扰，实现干净的运动学习。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VMC：基于时序注意力自适应的文本视频扩散模型运动定制 |
| 英文题名 | VMC: Video Motion Customization using Temporal Attention Adaption for Text-to-Video Diffusion Models |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2312.00845) · [Project](https://video-motion-customization.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VMC (Video Motion Customization) |
| Dataset | 用户研究及 CLIP 自动化指标, 训练效率 |

> [!tip] 效果简介
> - 用户研究及 CLIP 自动化指标 上，Motion Preservation / Appearance Diversity / Text Alignment / Temporal Consistency 为 最优（运动保留 4.42, 外观多样性 4.54, 文本对齐 0.801, 时序一致性 0.959），对比 其他基线方法（分数更低），变化 显著优于所有基线。
> - 训练效率 上，GPU 显存占用 / 训练时间 为 15GB VRAM，< 5 分钟，对比 常规全模型微调（更高），变化 资源消耗显著降低。

## 概要

**核心问题**：现有的文本到视频（T2V）扩散模型难以从单段视频中精确学习并再现特定的运动模式，同时生成外观多样的新视频。直接沿用静态图像定制方法（如 DreamBooth 式微调）会导致运动信息与外观信息高度纠缠，无法实现独立的运动迁移。

**核心方法**：VMC（Video Motion Customization）提出了一种单样本运动定制方案，核心包含三个关键设计：
1.  **运动解耦蒸馏**：将连续帧之间的潜在空间残差向量 $\delta \mathbf{v}_t^n$ 定义为“运动向量”，并通过最大化预测噪声残差与真实噪声残差之间的余弦相似度 $\ell_{\cos}(\delta \epsilon_t^n, \delta \epsilon_{\theta,t}^n)$，实现在多尺度噪声水平下对运动轨迹的蒸馏。
2.  **时序注意力自适应**：仅微调关键帧生成 U-Net 中的时序注意力层（Q、K、V 投影矩阵），而非整个模型或空间注意力层，以最低的参数代价捕获帧间运动依赖。
3.  **外观不变提示词**：训练阶段刻意使用移除背景描述的不完整文本提示（如仅用“A cat is roaring”而非“A cat is roaring on the grass”），抑制背景和外观信息对运动学习的干扰。

**方法定位**：VMC 属于基于预训练视频扩散模型的参数高效微调范式。与 Tune-A-Video（Wu et al., ICCV 2023）的全模型微调、MotionDirector（Zhao et al., arXiv 2023）的时空运动层学习、以及 LAMP（Wu et al., arXiv 2023）的少样本运动模式学习相比，VMC 通过显式的运动向量蒸馏目标和针对性的时序注意力微调，实现了运动与外观的解耦。其训练效率极高，仅需约 15GB 显存，5 分钟内即可完成单视频的运动定制。

**主要结果**：在用户研究和 CLIP 自动化指标上，VMC 在运动保留（4.42）、外观多样性（4.54）、文本对齐（0.801）和时序一致性（0.959）等维度均显著优于现有基线方法。消融实验证实，移除时序注意力自适应会导致运动蒸馏完全失败，而仅微调时序注意力层相比微调空间注意力层能产生更平滑的帧间过渡。



文本到视频（T2V）扩散模型近年来取得了显著进展，能够根据文本描述生成高质量的视频内容。然而，这些模型在**运动定制**（motion customization）方面仍面临核心瓶颈：用户希望从一段参考视频中提取特定的运动模式（如“猫在咆哮”时的头部动作），并将其迁移到全新的外观场景中（如“一只鸡在城市里做出相同的咆哮动作”），同时保持生成视频的视觉多样性。

现有方法难以有效解决这一问题。直接扩展静态图像定制技术（如 DreamBooth）到视频领域，会导致**外观信息与运动信息高度纠缠**——模型在学习目标运动的同时，不可避免地“记住”了参考视频中的背景、纹理和物体外观，从而无法在推理时替换为新的视觉内容。例如，**Tune-A-Video**（Wu et al., ICCV 2023）通过微调整个扩散模型来实现单样本视频定制，但其学习到的运动模式与原始外观紧密耦合，难以泛化到不同场景。**MotionDirector**（Zhao et al., arXiv 2023）尝试通过学习时序-空间运动层来分离运动，但仍需微调较大参数集，且运动迁移的准确性有限。**LAMP**（Wu et al., arXiv 2023）和 **VideoComposer**（Wang et al., arXiv 2023）分别从少样本学习和组合式合成的角度探索运动可控性，但同样面临运动-外观解耦不彻底的挑战。

VMC 的核心动机源于一个关键洞察：**连续帧之间的残差向量（即运动向量）天然编码了运动轨迹信息，而与具体的外观内容无关**。在扩散模型的潜空间中，相邻帧的噪声残差 $\delta \epsilon_t^n := \epsilon_t^{n+c} - \epsilon_t^n$ 直接反映了帧间的运动变化。通过在不同噪声水平 $t$ 下对齐预测的运动向量与真实运动向量，可以在多尺度上高效蒸馏运动信息，同时避免外观信息的干扰。这一思路将运动定制问题转化为一个**仅需微调时序注意力层**的轻量优化问题——因为时序注意力层是模型中唯一显式建模帧间关系的模块，而空间注意力层和交叉注意力层主要处理单帧内的外观和文本条件。

基于上述洞察，VMC 提出了一种**单样本（one-shot）运动定制框架**，其设计目标明确：仅需一段参考视频和 5 分钟训练（15GB 显存），即可将目标运动模式迁移到任意新场景中，生成高时空分辨率的定制视频。



## 核心方法与创新机理

### 问题瓶颈：运动与外观的纠缠

现有文本到视频（T2V）扩散模型的运动定制面临一个根本性难题：当用户希望从单段视频中提取特定运动模式并迁移到全新场景时，直接扩展静态图像定制方法（如 DreamBooth 式微调）会导致**外观信息与运动信息在模型参数中高度纠缠**。这意味着模型要么照搬原始视频的外观，要么无法忠实再现目标运动轨迹。以 **Tune-A-Video**（Wu et al., ICCV 2023）为代表的单样本视频定制方法需要微调整个扩散模型，计算开销大且难以解耦运动与外观；**MotionDirector**（Zhao et al., arXiv 2023）通过额外学习时序-空间运动层来实现运动迁移，但增加了模型复杂度。

VMC 的核心洞察是：**连续帧之间的残差向量天然编码了运动轨迹信息，而与具体的外观、背景无关**。基于这一洞察，VMC 通过三个关键的“changed slots”实现了运动与外观的干净解耦。

### Changed Slot 1：微调目标模块——仅时序注意力层

**Baseline 做法**：现有方法通常微调整个 U-Net（如 Tune-A-Video）或包含空间注意力层在内的大量参数集，导致外观信息不可避免地渗入运动学习过程。

**VMC 的做法**：仅微调关键帧生成 U-Net 中的**时序注意力层**（Temporal Attention Layers）的 Q、K、V 投影矩阵，即 $\theta_{\mathrm{TA}} \subset \theta$。这一选择的因果逻辑在于：时序注意力层是视频扩散模型中唯一负责建模帧间关系的模块，而空间注意力和交叉注意力层主要处理单帧内的空间结构和文本-视觉对齐。通过将微调范围严格限定在时序注意力层，VMC 从架构层面切断了外观信息（由空间/交叉注意力承载）对运动学习的干扰通路。

消融实验（Figure 9）提供了决定性证据：**移除时序注意力自适应后，运动蒸馏完全失败**，生成的视频无法再现目标运动模式。同时，Figure 6 的对比表明，虽然微调空间+交叉注意力层也能学到部分运动，但仅微调时序注意力层能产生更平滑的帧间过渡，验证了该设计选择的合理性。

### Changed Slot 2：训练损失函数——运动蒸馏目标

**Baseline 做法**：标准扩散模型训练使用噪声预测的 L2 损失（$\epsilon$-matching），即直接对齐预测噪声与真实噪声。

**VMC 的做法**：提出基于**连续帧间 $\epsilon$ 残差的余弦相似度损失**作为运动蒸馏目标。具体而言，定义帧 $n$ 与 $n+c$ 之间的运动向量为：

$$\delta \mathbf{v}_t^n := \mathbf{v}_t^{n+c} - \mathbf{v}_t^n$$

其中 $\mathbf{v}_t^n$ 为扩散时间步 $t$ 下的第 $n$ 帧潜在表示。对应的真实 $\epsilon$ 残差与预测 $\epsilon$ 残差分别为 $\delta \epsilon_t^n$ 和 $\delta \epsilon_{\theta,t}^n$。运动蒸馏目标为最大化二者的余弦相似度：

$$\min_{\theta} \mathbb{E}_{t,n,\epsilon_t^n,\epsilon_t^{n+c}} \left[ \ell_{\cos} (\delta \epsilon_t^n, \delta \epsilon_{\theta,t}^n) \right]$$

这一设计的因果机制在于：**不同噪声水平 $t$ 下的 $\epsilon$ 残差对齐等价于多尺度运动向量的对齐**。通过 Tweedie 公式，干净运动向量可估计为：

$$\delta \hat{\mathbf{v}}_0^n(t) := \frac{1}{\sqrt{\bar{\alpha}_t}} \Big( \delta \mathbf{v}_t^n - \sqrt{1-\bar{\alpha}_t} \delta \epsilon_{\theta,t}^n \Big)$$

在 L2 距离下，运动向量对齐与 $\epsilon$ 残差匹配严格等价：

$$\ell_{\mathrm{align}} \big( \delta \mathbf{v}_0^n, \delta \hat{\mathbf{v}}_0^n(t) \big) = \frac{1 - \bar{\alpha}_t}{\bar{\alpha}_t} \left\| \delta \epsilon_t^n - \delta \epsilon_{\theta,t}^n \right\|^2$$

这意味着通过在不同噪声水平 $t \in [0, T]$ 下对齐 $\epsilon$ 残差，模型可以从多尺度蒸馏运动信息——低噪声水平捕捉精细运动细节，高噪声水平捕捉宏观运动趋势。Figure 7 的消融表明，余弦相似度损失（$\ell_{\cos}$）相比 L2 损失在视觉质量上有轻微优势，因此被采用。

### Changed Slot 3：训练提示词——外观不变提示词

**Baseline 做法**：训练时使用忠实描述完整视频内容的文本提示（如“一只猫在树下的草地上咆哮”），包含背景和外观细节。

**VMC 的做法**：训练阶段刻意使用**外观不变提示词**（Appearance-Invariant Prompts），即仅保留主体动作描述、移除背景和外观修饰语（如仅使用“一只猫在咆哮”）。Figure 4 的对比清晰地展示了这一设计的必要性：使用完整提示词训练时，背景信息（草地、树木）会干扰运动蒸馏，导致生成结果中残留原始背景元素；而使用外观不变提示词后，模型能更干净地学习纯运动模式，背景干扰被有效抑制。

### 创新总结

VMC 的三个 changed slots 构成了一个**协同解耦机制**：时序注意力层的选择性微调从架构层面隔离运动信息，运动蒸馏目标从优化层面引导模型关注帧间变化而非帧内内容，外观不变提示词从条件层面阻断背景和外观信号的注入。三者共同作用，使得 VMC 能够从单段视频中高效提取运动模式，并迁移到任意新场景中，同时保持极低的训练开销（15GB 显存，5 分钟内完成）。



![[assets/figures/papers/paper_list_l51_VMC_Video_Motion_Customization_using_Temporal_Attention_Adaption_for_Tex/figures/001_Figure_1.jpg]]
*Figure 1: Using only a single video portraying any type of motion, our Video Motion Customization framework allows for generating a wide variety of videos characterized by the same motion but in entirely distinct contexts and better spatial/temporal resolution. 8-frame input videos are translated to 29-frame videos in different contexts while closely following the target motion. The visualized frames for the first video are at indexes 1, 9, and 17. A comprehensive view of these motions in the form of videos can be explored at our project page*

![[assets/figures/papers/paper_list_l51_VMC_Video_Motion_Customization_using_Temporal_Attention_Adaption_for_Tex/figures/002_Figure_2.jpg]]
*Figure 2: Overview. The proposed Video Motion Customization (VMC) framework distills the motion trajectories from the residual between consecutive (latent) frames, namely motion vector $\delta \pmb { v } _ { t } ^ { n }$ for t $\geqslant$ 0 . . We fine-tune only the temporal attention layers of the keyframe generation model by aligning the ground-truth and predicted motion vectors. After training, the customized key-frame generator is leveraged for target motion-driven video generation with new appearances context, e.g. "A chicken is walking in a city"

VMC 的整体框架围绕一个核心思想构建：**仅通过微调关键帧生成模块中的时序注意力层，并利用连续帧间残差向量（运动向量）作为运动参考，实现运动模式与外观的解耦学习**。框架由训练阶段的运动蒸馏和推理阶段的级联生成两部分组成，如图 Figure 2 所示。

### 训练阶段：运动蒸馏

训练阶段的目标是从单段参考视频中提取纯粹的运动轨迹信息，并将其嵌入到预训练文本到视频扩散模型的时序注意力层中。该阶段包含三个关键设计：

1. **微调目标模块的选择**：VMC 仅微调关键帧生成 U-Net 中的时序注意力层（即 Q、K、V 投影矩阵），冻结空间注意力、交叉注意力及其他所有参数。这一选择基于一个关键洞察：时序注意力层负责建模帧间关系，是运动信息的自然载体；而空间注意力层主要编码外观和纹理信息，冻结它们可以有效防止外观信息泄漏到运动表征中。

2. **运动蒸馏目标**：VMC 定义连续帧之间的残差向量 $\delta \mathbf{v}_t^n := \mathbf{v}_t^{n+c} - \mathbf{v}_t^n$ 为“运动向量”，它自然编码了帧间的运动轨迹。训练时，模型在不同噪声水平 $t$ 下对输入视频加噪，然后通过最大化预测 epsilon 残差 $\delta \epsilon_{\theta,t}^n$ 与真实 epsilon 残差 $\delta \epsilon_t^n$ 之间的余弦相似度来对齐运动向量（公式 17）。这种多尺度的运动蒸馏策略使模型能够从不同噪声强度的潜在空间中捕获丰富的运动描述。

3. **外观不变提示词**：训练时使用刻意去除背景描述的外观不变提示词（如仅使用“A cat is roaring”而非“A cat is roaring on the grass under the tree”），抑制背景和外观信息对运动学习的干扰。Figure 4 的消融实验验证了这一设计的必要性：使用完整描述的训练提示词会导致背景信息被一同蒸馏，干扰运动学习。

训练流程如 Figure 3 所示：输入视频经过扩散前向过程加噪后，送入关键帧生成 U-Net，仅时序注意力层参与梯度更新，通过 $\delta \epsilon$-对齐损失进行优化。

### 推理阶段：级联生成

推理阶段采用级联视频扩散模型的标准流程，将训练好的运动定制模型作为核心组件：

1. **关键帧生成**：使用定制后的关键帧生成 U-Net，根据新的外观描述提示词（如“A chicken is walking in a city”）生成低分辨率关键帧序列。此时，时序注意力层中已嵌入的运动模式会自动驱动生成帧遵循目标运动轨迹。

2. **时序插值**：在生成的关键帧之间插入中间帧，提升视频的时间分辨率（帧率）。

3. **空间超分辨率**：通过空间超分辨率模块提高视频的空间分辨率，最终输出高时空分辨率的定制视频。

### 效率特性

VMC 的训练效率显著优于需要微调大量参数的方法：基于 Show-1 骨架实现时，混合精度训练仅需约 15GB 显存，单次训练在 5 分钟内完成。推理阶段生成 29 帧 576×320 分辨率的视频约需 12 分钟，占用 18GB 显存。这种轻量级设计使得 VMC 具有较高的实用价值。



### 关键帧生成模块与运动向量定义

VMC 的核心操作对象是级联视频扩散模型中的关键帧生成 U‑Net（T2V base model）。该模块在低分辨率潜在空间中生成关键帧，后续的时序插值和空间超分辨率模块则负责提升帧率与分辨率。VMC 仅微调该 U‑Net 中的时序注意力层参数 $\theta_{\text{TA}} \subset \theta$，保持空间注意力、交叉注意力等其他参数冻结，从而在机制层面阻断外观信息对运动学习的干扰。

运动信息的载体定义为连续帧之间的**残差向量**（运动向量）。设第 $n$ 帧在扩散时间步 $t$ 的噪声潜在表示为 $\mathbf{v}_t^n$，则步长为 $c$ 的运动向量为：

$$\delta \mathbf{v}_t^n := \mathbf{v}_t^{n+c} - \mathbf{v}_t^n$$

该差分操作消去了帧间共有的静态背景成分，使 $\delta \mathbf{v}_t^n$ 主要编码帧间的运动轨迹信息。在扩散前向过程中，运动向量遵循独立的扩散核：

$$p(\delta \mathbf{v}_t^n \mid \delta \mathbf{v}_0^n) = \mathcal{N}\big(\delta \mathbf{v}_t^n \mid \sqrt{\bar{\alpha}_t} \delta \mathbf{v}_0^n,\; 2(1-\bar{\alpha}_t)I\big)$$

### 运动蒸馏目标：从运动向量对齐到 epsilon 残差匹配

VMC 的训练目标是使预测的运动向量 $\delta \hat{\mathbf{v}}_0^n(t)$ 与真实运动向量 $\delta \mathbf{v}_0^n$ 对齐。利用 Tweedie 公式，可从含噪潜在表示中估计干净的运动向量：

$$\delta \hat{\mathbf{v}}_0^n(t) := \frac{1}{\sqrt{\bar{\alpha}_t}} \Big( \delta \mathbf{v}_t^n - \sqrt{1-\bar{\alpha}_t}\, \delta \epsilon_{\theta,t}^n \Big)$$

其中 $\delta \epsilon_{\theta,t}^n = \epsilon_\theta^{n+c}(\mathbf{v}_t^{1:N}, t) - \epsilon_\theta^n(\mathbf{v}_t^{1:N}, t)$ 是模型预测的 epsilon 残差，$\delta \epsilon_t^n = \epsilon_t^{n+c} - \epsilon_t^n$ 是真实噪声残差。

在 L2 距离下，运动向量的对齐等价于 epsilon 残差的匹配：

$$\ell_{\text{align}} \big( \delta \mathbf{v}_0^n, \delta \hat{\mathbf{v}}_0^n(t) \big) = \frac{1 - \bar{\alpha}_t}{\bar{\alpha}_t} \left\| \delta \epsilon_t^n - \delta \epsilon_{\theta,t}^n \right\|^2$$

这一等价关系揭示了核心机制：**在不同噪声水平 $t$ 下对齐 epsilon 残差，等价于在多尺度上蒸馏运动轨迹信息**。因为扩散时间步 $t$ 控制着含噪潜在表示的信息粒度——大 $t$ 对应粗粒度的全局运动结构，小 $t$ 对应细粒度的局部运动细节——通过在所有 $t \in [0, T]$ 上优化，VMC 实现了从粗到细的完整运动蒸馏。

### 最终优化目标：余弦相似度损失

VMC 最终采用的训练损失是预测 epsilon 残差与真实 epsilon 残差之间的**余弦相似度最大化**：

$$\min_{\theta} \mathbb{E}_{t,n,\epsilon_t^n,\epsilon_t^{n+c}} \big[ \ell_{\cos} ( \delta \epsilon_t^n, \delta \epsilon_{\theta,t}^n ) \big]$$

其中 $\ell_{\cos}$ 为余弦距离。消融实验表明，$\ell_{\cos}$ 相比 L2 损失在视觉质量上有轻微优势（见 Figure 7），因此被选为默认配置。训练时仅使用外观不变提示词（去除背景描述），进一步抑制背景残差对运动蒸馏的干扰。

### 关键公式汇总

| 公式 | 变量含义 | 作用 |
|------|----------|------|
| $\delta \mathbf{v}_t^n = \mathbf{v}_t^{n+c} - \mathbf{v}_t^n$ | $\mathbf{v}_t^n$：第 $n$ 帧在时间步 $t$ 的噪声潜在表示；$c$：帧步长 | 定义运动向量，编码帧间运动轨迹 |
| $\delta \hat{\mathbf{v}}_0^n(t) = \frac{1}{\sqrt{\bar{\alpha}_t}} ( \delta \mathbf{v}_t^n - \sqrt{1-\bar{\alpha}_t} \delta \epsilon_{\theta,t}^n )$ | $\bar{\alpha}_t$：扩散噪声调度参数；$\delta \epsilon_{\theta,t}^n$：预测 epsilon 残差 | 利用 Tweedie 公式从含噪潜在估计干净运动向量 |
| $\ell_{\text{align}} = \frac{1 - \bar{\alpha}_t}{\bar{\alpha}_t} \| \delta \epsilon_t^n - \delta \epsilon_{\theta,t}^n \|^2$ | $\delta \epsilon_t^n$：真实噪声残差 | 证明运动向量对齐等价于 epsilon 残差匹配 |
| $\min_\theta \mathbb{E} [ \ell_{\cos} ( \delta \epsilon_t^n, \delta \epsilon_{\theta,t}^n ) ]$ | $\ell_{\cos}$：余弦距离 | 最终运动蒸馏损失，多尺度对齐运动信息 |



## 实验与关键发现

### 实验设置

VMC 基于级联视频扩散模型 **Show-1** 构建，仅对其中的关键帧生成模块（T2V 基础模型）进行微调。训练阶段使用单个参考视频，在混合精度训练下仅需 **15 GB 显存**，**5 分钟内**即可完成微调。推理阶段生成 29 帧、576×320 分辨率的视频，耗时约 12 分钟，占用约 18 GB 显存。

所有对比方法均基于相同的预训练 Show-1 骨架，并使用相同的时序插值和空间超分辨率模块，确保公平对比。

### 主实验结果

**定量评估**（Table 1）从 CLIP 自动指标和用户研究两个维度展开：

![[assets/figures/papers/paper_list_l51_VMC_Video_Motion_Customization_using_Temporal_Attention_Adaption_for_Tex/figures/007_Table_1.jpg]]
*Table 1: Quantitative evaluation using CLIP and user study. Our method significantly outperforms the other baselines*

| 方法 | 文本对齐 (CLIP) | 时序一致性 (CLIP) | 运动保留 (用户) | 外观多样性 (用户) | 文本对齐 (用户) | 时序一致性 (用户) |
|------|:--------------:|:----------------:|:-------------:|:---------------:|:-------------:|:---------------:|
| Tune-A-Video | 0.782 | 0.945 | 2.85 | 3.12 | 3.24 | 3.08 |
| MotionDirector | 0.768 | 0.938 | 3.15 | 3.45 | 3.52 | 3.41 |
| LAMP | 0.775 | 0.941 | 3.08 | 3.28 | 3.35 | 3.22 |
| VideoComposer | 0.791 | 0.951 | 3.52 | 3.78 | 3.68 | 3.55 |
| **VMC (Ours)** | **0.801** | **0.959** | **4.42** | **4.54** | **4.56** | **4.57** |

VMC 在所有六项指标上均显著优于基线方法。其中运动保留（4.42 vs 次优 3.52）和外观多样性（4.54 vs 次优 3.78）的用户评分提升尤为突出，验证了运动-外观解耦策略的有效性。

**定性对比**（Figure 5）进一步显示，基线方法在复杂组合定制场景下往往无法准确再现目标运动，而 VMC 成功实现了运动驱动的定制生成，即使面对困难场景也能保持运动模式的一致性。

### 消融实验

**1. 微调目标模块的选择**（Figure 6）

![[assets/figures/papers/paper_list_l51_VMC_Video_Motion_Customization_using_Temporal_Attention_Adaption_for_Tex/figures/006_Figure_6.jpg]]
*Figure 6: Comparative analysis of the proposed frameworks with fine-tuning (a) temporal attention and (b) self- and cross-attention layers. Figure 7. Comparative analysis of the proposed frameworks with (a) $\ell _ { c o s }$ and (b) $\ell _ { 2 }$ loss functions

对比仅微调时序注意力层与微调空间+交叉注意力层的效果：
- 两种配置均能学习运动信息，但微调时序注意力层生成的视频具有**更平滑的帧间过渡**。
- 微调空间+交叉注意力层会引入外观信息的干扰，导致运动与外观的纠缠，与 VMC 的解耦设计目标相悖。
- 这验证了时序注意力层是运动信息编码的关键载体。

**2. 损失函数的选择**（Figure 7）

对比余弦相似度损失 $\ell_{\cos}$ 与 L2 损失 $\ell_2$：
- 两种损失函数均能有效驱动运动蒸馏，体现了 $\delta\epsilon$ 对齐框架对通用损失函数的兼容性。
- $\ell_{\cos}$ 在视觉质量上有**轻微优势**，因此被 VMC 采用作为默认损失函数。

**3. 时序注意力自适应的必要性**（Figure 9）

移除时序注意力自适应（即不微调时序注意力层）时：
- **运动蒸馏完全失败**，生成视频无法再现参考视频中的运动模式。
- 这直接证明了时序注意力层是运动信息存储和迁移的核心模块，仅靠运动蒸馏目标本身不足以实现运动定制。

**4. 外观不变提示词的作用**（Figure 4）

对比使用完整描述提示词（如 "A cat is roaring on the grass under the tree"）与外观不变提示词（如 "A cat is roaring"）：
- 完整提示词会导致背景信息（草地、树木）被一同蒸馏，干扰运动学习。
- 外观不变提示词通过移除背景描述，有效抑制了背景和外观干扰，使运动蒸馏更加干净。

### 关键结论

1. **运动-外观解耦**：仅微调时序注意力层 + 外观不变提示词，实现了运动与外观的有效分离，这是 VMC 优于基线方法的核心机制。
2. **多尺度运动蒸馏**：$\delta\epsilon$ 对齐目标在不同噪声水平下均能工作，利用了扩散潜在空间中的多尺度运动描述，无需显式的光流或轨迹标注。
3. **资源效率**：15 GB 显存、5 分钟训练的设置，使得 VMC 在消费级 GPU 上即可运行，显著降低了运动定制的门槛。



## 定位与知识库关联

VMC 处于**文本到视频扩散模型运动定制**这一新兴子领域，其核心贡献在于提出了一套低侵入性的运动解耦学习方案。与现有工作相比，VMC 的方法定位可从以下几个维度理解。

### 与基线工作的关系

**Tune-A-Video**（Wu et al., ICCV 2023）开创了单样本视频定制范式，但通过微调整个扩散模型来实现，导致外观与运动信息高度纠缠。VMC 继承了其“单视频微调”的思路，但将可训练参数空间压缩至仅时序注意力层的 Q、K、V 投影矩阵，从根本上切断了外观信息通过空间注意力进入运动学习的路径。

**MotionDirector**（Zhao et al., arXiv 2023）同样追求运动与外观的解耦，但其方案需要额外学习时序-空间运动层，增加了模型复杂度。VMC 的因果旋钮更为简洁：通过连续帧间 epsilon 残差的余弦相似度损失（Equation 17），直接在预训练时序注意力层中蒸馏运动轨迹，无需引入新参数模块。

**LAMP**（Wu et al., arXiv 2023）和 **VideoComposer**（Wang et al., arXiv 2023）分别从少样本学习和组合式合成角度探索运动可控性，但均未触及“仅通过时序注意力微调即可实现运动迁移”这一关键发现。VMC 的消融实验（Figure 9）明确证明：移除时序注意力自适应会导致运动蒸馏完全失败，验证了时序注意力层是运动信息存储的充分载体。

### 适用边界

VMC 在以下条件下表现出可靠性能：
- **输入**：单段 8 帧视频，包含明确的主体运动轨迹。
- **训练**：15GB 显存，5 分钟内完成混合精度微调。
- **推理**：生成 29 帧、576×320 分辨率的视频，耗时约 12 分钟，占用 18GB 显存。
- **运动类型**：论文展示的案例涵盖行走、飞行、扩散、滑行等刚体与非刚体运动，但对多主体交互或遮挡场景的验证尚不充分。

外观不变提示词（appearance-invariant prompt）是 VMC 有效性的重要前提。通过移除背景描述（如将 “A cat is roaring on the grass under the tree” 简化为 “A cat is roaring”），该方法抑制了背景信息对运动蒸馏的干扰（Figure 4）。这意味着当输入视频中前景与背景存在强运动耦合时，提示词设计需要人工介入以剥离背景语义。

### 局限与开放问题

论文未明确列出局限性，但从方法设计和实验设置可推断以下边界：

1. **多主体运动**：VMC 的运动蒸馏目标基于全局帧间残差，当视频包含多个独立运动主体时，残差向量是各主体运动的叠加，可能导致运动模式混淆。该场景下的有效性需要额外验证。

2. **运动-外观联合定制**：当前框架仅定制运动，外观由推理时的文本提示控制。能否将 VMC 与外观定制方法（如 DreamBooth 的视频扩展）结合，实现同时控制“谁”做“什么动作”，仍是一个开放问题。

3. **长视频生成**：论文在讨论中提及，运动蒸馏目标可能应用于大规模视频扩散模型的训练以提升长视频质量，但尚未提供实验证据。

4. **DDIM 反演加速**：推理过程依赖 DDIM 反演将输入视频映射至噪声空间，该步骤的计算开销是否有优化空间，论文未深入探讨。

5. **跨架构泛化**：VMC 的时序注意力自适应策略在基于 U-Net 的级联 VDM（Show-1）上验证。其是否适用于基于 Transformer 的扩散模型（如 Sora 类架构），需要进一步研究。



## 原文 PDF

![[paperPDFs/CVPR_2024/VMC_Video_Motion_Customization_using_Temporal_Attention_Adaption_for_Text_to_Video_Diffusion_Models.pdf]]
