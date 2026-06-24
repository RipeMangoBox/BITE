---
title: "Point Prompting: Counterfactual Tracking with Video Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Point_Prompting_Counterfactual_Tracking_with_Video_Diffusion_Models.pdf
project_link: https://point-prompting.github.io
openreview_forum_id: 6FFQ007qLX
aliases:
- PPCT
- PPCTVDM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/segmentation
core_operator: "利用SDEdit对输入视频进行反事实再生，并在扩散采样中引入以未编辑首帧为负向提示的引导（式5），迫使生成视频保留标记点；同时结合颜色重平衡与基于掩码的细化，确保标记稳定传播。"
primary_logic: "通过反事实建模（在首帧标记查询点并再生视频），可激发预训练视频扩散模型对运动轨迹的零样本理解；负向提示策略克服了模型强先验导致的标记消失问题，使生成器能利用其学习的物体永久性处理遮挡，从而在无需额外训练的情况下实现具有竞争力的点跟踪。"
claims:
- "我们的零样本方法在TAP-Vid DAVIS上AJ达到42.21，超过所有其他零样本基线（如SD-DINO的29.68），并接近自监督方法。"
- "移除反事实增强（负向提示）后AJ从48.60骤降至22.03，表明该模块对防止标记消失至关重要。"
- "使用更高分辨率的原始帧（original res.）比256×256提升AJ从42.21到48.60，说明输入分辨率与模型训练分布匹配的重要性。"
- "通过蒸馏生成的伪标签训练CoTracker，得到的快速跟踪器在TAP-Vid DAVIS上AJ达到37.17，与教师模型Wan2.1-1.3B的38.78接近。"
---

# Point Prompting: Counterfactual Tracking with Video Diffusion Models

> [!tip] 核心洞察
> 通过反事实建模（在首帧标记查询点并再生视频），可激发预训练视频扩散模型对运动轨迹的零样本理解；负向提示策略克服了模型强先验导致的标记消失问题，使生成器能利用其学习的物体永久性处理遮挡，从而在无需额外训练的情况下实现具有竞争力的点跟踪。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 点提示：基于视频扩散模型的反事实点跟踪 |
| 英文题名 | Point Prompting: Counterfactual Tracking with Video Diffusion Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=6FFQ007qLX) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/segmentation |
| Method | Point Prompting for Counterfactual Tracking |
| Dataset | TAP-Vid DAVIS, TAP-Vid Kinetics, TAP-Vid DAVIS (original res., Wan2.1-14B) |

> [!tip] 效果简介
> - TAP-Vid DAVIS 上，AJ ↑ 为 42.21 (zero-shot)，对比 29.68 (SD-DINO, best zero-shot baseline)，变化 +12.53。
> - TAP-Vid DAVIS 上，OA ↑ 为 82.90 (zero-shot)，对比 80.87 (Opt-CWM, best self-supervised baseline)，变化 +2.03。
> - TAP-Vid Kinetics 上，AJ ↑ 为 27.36，对比 16.47 (SD-DINO)，变化 +10.89。

## 概述

点跟踪是视觉理解的基础任务，要求对视频中任意查询点在所有帧中持续定位。现有零样本方法依赖从预训练模型中提取特征进行帧间匹配（如DIFT、SD-DINO），难以处理遮挡和长时运动，与有监督方法存在显著差距。视频扩散模型具有内在的时序一致性和物体持久性，但由于其强先验，直接插入不自然的视觉标记（如红点）会导致标记在生成中消失，无法直接用于跟踪。

本文提出**Point Prompting for Counterfactual Tracking**，一种零样本点跟踪方法。核心思路是利用SDEdit对输入视频进行反事实再生——在首帧查询点位置叠加红色圆点作为视觉提示，通过扩散再生将该标记传播到后续帧，再用颜色检测器提取轨迹。关键创新在于**负向提示策略**：以未编辑的首帧作为负向条件，在每一步去噪中减去其噪声估计（式5），迫使生成视频保留标记点，克服了模型强先验导致的标记消失问题。结合颜色重平衡与基于掩码的粗到细细化，该方法无需任何训练即可实现具有竞争力的点跟踪。

在TAP-Vid DAVIS基准上，该方法AJ达到42.21，超过所有零样本基线（如SD-DINO的29.68），并在遮挡准确率OA上达到82.90，超过最优自监督方法Opt-CWM。使用原始分辨率后AJ进一步提升至48.60。消融实验表明，移除反事实增强后AJ从48.60骤降至22.03，证实该模块是方法的核心驱动因子。此外，通过蒸馏生成的伪标签训练CoTracker，得到的快速跟踪器AJ达到37.17，与教师模型接近且速度提升数个量级。

该方法的主要局限在于计算成本高（生成50帧需7–30分钟），以及在静止点、对称混淆、标记消失等场景下容易出错，且对合成视频泛化差。这些限制可通过蒸馏和模型改进逐步缓解。

## 背景与动机

点跟踪是计算机视觉中的基础任务，旨在估计视频中指定物理点在每一帧的精确位置。这项能力支撑着运动分析、三维重建、视觉编辑等一系列下游应用。传统方法通常依赖大量标注数据进行监督训练，例如 **RAFT**（Teed & Deng, ECCV 2020）通过光流估计实现逐帧匹配，**TAPIR**（Doersch et al., 2023）和 **CoTracker3**（Karaev et al., 2024b）则直接针对点跟踪任务进行专门设计。这些方法在训练分布内表现优异，但泛化到新场景时往往受限。

近年来，零样本点跟踪方法试图摆脱对标注数据的依赖，转而从预训练模型中提取特征进行帧间匹配。代表性工作包括 **DIFT**（Tang et al., 2023）利用扩散模型的特征层进行稠密对应，以及 **SD-DINO**（Zhang et al., 2023a）融合扩散特征与 DINOv2 特征。然而，这类方法面临一个根本性瓶颈：**它们依赖静态的特征相似度匹配，难以处理遮挡和长时运动**。当目标点被遮挡后重新出现，外观可能发生显著变化，特征匹配器容易丢失目标或产生错误关联。

视频扩散模型的出现为解决上述瓶颈提供了新的可能。这类模型在大规模视频数据上训练，展现出强大的**时序一致性和物体持久性**——它们能够理解物体在运动中的连续性，甚至在遮挡后自然恢复。这暗示着，如果能将扩散模型的生成能力用于跟踪，或许可以绕过显式特征匹配的困境。

但直接使用扩散模型进行跟踪并非易事。一个直观的思路是在视频首帧的目标位置插入视觉标记（如红点），然后让扩散模型重新生成整个视频，期望标记随物体运动自然传播。然而，扩散模型具有**强先验**：它倾向于生成“自然”的视频内容，而一个不自然的彩色圆点会被视为需要“修复”的伪影，在生成过程中被逐渐抹除。这种标记消失现象使得简单的视觉提示策略无法直接奏效。

本文的核心动机正是突破这一困境：**如何激发预训练视频扩散模型对运动轨迹的零样本理解，同时克服其强先验导致的标记消失问题**。通过反事实建模——在首帧引入人为扰动（标记点）并迫使模型在再生中保留这一扰动——可以将跟踪问题转化为一个可控的视频生成问题。这种方法无需任何微调，完全依赖预训练模型的内部知识，为零样本点跟踪开辟了一条新路径。

## 核心创新

本工作提出**点提示反事实跟踪（Point Prompting for Counterfactual Tracking）**，其核心创新在于将预训练视频扩散模型重新定位为零样本点跟踪器，并通过三个关键机制克服了直接使用扩散模型进行跟踪的根本障碍。

### 创新一：反事实点提示传播

传统零样本点跟踪方法（如 **DIFT**（Tang et al., 2023）、**SD-DINO**（Zhang et al., 2023a）、**DINOv2+NN**（Oquab et al., 2023））依赖从预训练模型中提取特征进行帧间匹配，在遮挡和长时运动场景下匹配信号脆弱。本方法彻底改变了轨迹提取机制：**在首帧查询点位置叠加独特的红色圆点作为视觉标记，通过 SDEdit（Meng et al., 2021）对视频进行反事实再生，使标记自然传播到后续帧，再用简单的 HSV 颜色检测器提取轨迹**（Figure 1）。这一设计的深层洞察在于：视频扩散模型在训练中习得了物体的时序一致性和持久性，通过反事实扰动（插入标记点）可激发模型对运动轨迹的零样本理解，而无需任何额外训练。

### 创新二：负向提示反事实信号增强

直接插入标记并通过扩散模型生成面临一个关键瓶颈：**扩散模型的强先验倾向于消除不自然的视觉元素**，导致红点在生成过程中消失（Table 4 中移除反事实增强后 AJ 从 48.60 骤降至 22.03）。本方法引入**负向提示策略**作为反事实信号增强机制：以未编辑的首帧作为负向条件，在每一步去噪中计算增强噪声估计：

$$\tilde{\epsilon}_{\theta} \left( \mathbf{x}_t, \mathbf{c}_I \right) = (\lambda + 1) \cdot \epsilon_{\theta}( \mathbf{x}_t, \phi(\mathbf{c}_I) ) - \lambda \cdot \epsilon_{\theta} \left( \mathbf{x}_t, \mathbf{c}_I \right)$$

其中 $\phi(\mathbf{c}_I)$ 为编辑后的首帧条件，$\mathbf{c}_I$ 为原始首帧条件。该公式通过**线性外推两个条件（编辑/未编辑首帧）下的噪声估计**，迫使生成过程偏向包含标记的视频，同时远离未编辑版本（Figure 2）。从分数函数角度，这等效于在条件于编辑图像的同时通过调节因子 $\lambda$ 抑制未编辑条件的影响（式 6），类似于无分类器引导机制。消融实验证实该模块是方法的核心驱动因子。

### 创新三：粗到细的掩码约束细化

初始轨迹提取后，本方法进一步利用扩散模型的 inpainting 能力进行后处理优化：**构造以粗轨迹为中心的时空二值掩码 $\mathbf{m}$，仅在轨迹周围小区域内重新运行视频生成**，通过掩码约束的反向扩散（式 4）纠正时空错位：

$$\mathbf{x}_{t-1} = \mathbf{m} \odot \tilde{\mathbf{x}}_{t-1} + (1 - \mathbf{m}) \odot \mathbf{x}_{t-1}^{\mathrm{original}}$$

该设计使模型专注于局部区域的精细再生，同时保持其余视频内容不变（Figure 3）。消融实验表明，移除该细化步骤使 AJ 从 48.60 降至 42.70，验证了其对纠正生成伪影的有效性。

### 辅助创新：颜色重平衡

为抑制自然场景中与标记相似的色调导致的虚假检测，本方法在预处理阶段**降低标记颜色的饱和度**，消除环境中的同色干扰。关闭颜色重平衡后 AJ 降至 34.86（Table 4），证实其在复杂场景下的必要性。

### 创新总结

| 创新维度 | 基线方法 | 本方法 |
|---------|---------|--------|
| 轨迹提取机制 | 从预训练模型提取特征进行帧间匹配 | 首帧插入彩色标记，通过 SDEdit 再生成传播，颜色检测器提取 |
| 反事实信号增强 | 直接插入标记后生成（无负向提示） | 以未编辑首帧为负向提示，外推噪声估计 |
| 后处理优化 | 无细化或仅简单跟踪 | 掩码约束的局部精细再生 |
| 颜色预处理 | 直接使用原始视频颜色 | 降低标记颜色饱和度以消除干扰 |

这些创新共同使方法在 TAP-Vid DAVIS 上以零样本设定达到 AJ 42.21，显著超越所有其他零样本基线（最佳基线 SD-DINO 为 29.68），并在遮挡准确率（OA 82.90）上超过自监督方法 **Opt-CWM**（Stojanov et al., 2025）的 80.87（Table 1）。

## 整体框架

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_6FFQ007qLX/figures/005_Figure_1.jpg]]
*Figure 1: Prompting a diffusion model for tracking. (a) We use an off-the-shelf video diffusion model to perform point tracking. We add a small, distinctive marking—a red dot—to the first frame of an input video, then ask the diffusion model to regenerate the rest of the video using SDEdit (Meng et al., 2021), which propagates the marking to subsequent frames. (b) We then track the motion of this marking over time. This motion corresponds to the trajectory of the underlying physical point. The model successfully tracks through occlusion. Please see the webpage for more results: https://point-prompting.github.io*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_6FFQ007qLX/figures/006_Figure_2.jpg]]
*Figure 2: Enhancing the Counterfactual Signal. We use negative prompting to ensure that the generated video contains the marker. In each denoising step (Eq. 5), we condition the denoising on two images: (1) Edited First Frame: the first frame of the video with a marking added, and (2) Unedited First Frame: the original first frame of the video. We then subtract the weighted noise vector of the latter from the former*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_6FFQ007qLX/figures/007_Figure_3.jpg]]
*Figure 3: Tracking Enhancements. To improve point tracking in video, we introduce two enhancements: (1) Color Rebalancing: remove existing red hues to ensure the red marker remains a unique tracking cue; (2) Refinement: obtain initial trajectories with a color-based tracker, then refine them using an inpainting mask to correct temporal artifacts such as object shifts (as shown in white circles). This two-step procedure first produces coarse tracks and then refines them via mask-constrained reverse diffusion*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_6FFQ007qLX/figures/013_Table_4.jpg]]
*Table 4: Tracking Pipeline Ablations. Quantitative results on TAP-Vid DAVIS-First showing the impact of each stage in our pipeline (Fig. 3). The last row uses original pixel color instead of the red dot for tracking. Figure 4: Effect of denoising strength and radius on tracking performance*

本方法的核心思路是将点跟踪问题转化为视频扩散模型的可控再生任务：通过在输入视频的首帧查询点位置叠加一个独特的彩色标记（红色圆点），然后利用预训练视频扩散模型对该视频进行反事实再生（counterfactual regeneration），使标记随物体运动自动传播到后续帧，最后通过简单的颜色检测器提取完整轨迹。整个pipeline由五个模块串联构成，形成“标记插入→扩散传播→颜色跟踪→后处理优化”的闭环。

### 输入与输出

- **输入**：一段原始视频（$F$帧）和首帧上的一个查询点坐标 $(u_0, v_0)$。
- **输出**：该查询点在所有帧中的轨迹 $\{(\hat{u}_k, \hat{v}_k)\}_{k=0}^{F-1}$，以及每帧的可见性估计。

### Pipeline 模块关系

#### 1. 标记插入（Marker Insertion）
在首帧的查询点位置叠加一个纯红色圆点作为反事实扰动。该标记是后续所有操作的“锚点”——扩散模型需要学会将这个视觉提示与物体运动绑定，颜色检测器则依赖它来定位每一帧的跟踪目标。标记的半径和颜色饱和度需精心选择：半径过大会破坏局部结构，过小则难以在扩散过程中存活；颜色饱和度需通过后续的颜色重平衡模块进一步抑制自然场景中的相似色调。

#### 2. SDEdit 传播与负向提示增强（SDEdit Propagation with Negative Prompting）
这是整个pipeline的核心驱动模块。将插入标记后的视频通过 SDEdit 进行再生：先向视频潜变量添加中等强度的噪声（Eq. 3），然后在反向去噪过程中条件于编辑后的首帧，使模型生成一个“包含标记且保持原视频内容”的新视频。

关键创新在于**负向提示策略**（Eq. 5）：在每一步去噪时，同时计算两个噪声估计——一个条件于编辑首帧（含标记），另一个条件于未编辑的原始首帧（无标记）。通过将前者减去后者的加权差值，迫使采样过程远离“无标记”的样本分布，从而克服扩散模型强先验导致的标记消失问题。这一机制从分数函数角度可解释为在条件于编辑图像的同时，通过调节因子 $\lambda$ 抑制未编辑条件的影响（Eq. 6），类似于无分类器引导的推广形式。

#### 3. 颜色检测器（Color-based Tracker）
在再生视频的每一帧中，于上一帧预测位置周围的局部搜索窗（半径 $r$）内检测红色像素（HSV空间），取检测到的红色区域中心作为当前帧的轨迹点。若搜索窗内无红色像素，则判定该点被遮挡，将上一帧位置向前传播。该模块简单高效，但严重依赖标记颜色的唯一性——这正是颜色重平衡模块存在的理由。

#### 4. 颜色重平衡（Color Rebalancing）
在标记插入前，对原始视频进行颜色预处理：降低标记颜色通道的饱和度，抑制自然场景中与标记相近的色调（如红色物体、肤色等）。这一步确保再生后的视频中，红色标记是唯一的强红色信号源，从而大幅减少颜色检测器的虚假检测。

#### 5. 粗到细细化（Coarse-to-Fine Refinement）
颜色检测器输出的轨迹可能存在时空错位（如标记漂移到相邻物体上）。精细化模块利用扩散模型的 inpainting 能力进行修正：构造一个时空二值掩码 $\mathbf{m}$，仅在初始轨迹周围的小区域内允许模型修改（Eq. 4），其余区域保持原始视频信号。重新运行一次掩码约束的扩散再生，使标记位置在局部区域内得到纠正。这一“先粗后精”的策略显著提升了轨迹的时空一致性。

### 模块间的因果流

整个pipeline的信息流是严格单向的：标记插入为扩散传播提供反事实信号；负向提示确保该信号在扩散过程中不被模型先验“抹除”；颜色重平衡为颜色检测器创造干净的检测环境；粗到细细化则纠正前序步骤积累的定位误差。消融实验（Table 4）证实了这一链条的脆弱性：移除负向提示会导致性能崩溃（AJ 从 48.60 骤降至 22.03），关闭颜色重平衡会使 AJ 降至 34.86，去掉精细化则降至 42.70，而仅用原始像素颜色（无标记点）跟踪的 AJ 仅为 11.26——每个模块的缺失都会在因果链上产生不可恢复的误差放大。

## 核心模块与公式推导

### 3.1 视频扩散模型与SDEdit基础

方法构建于预训练视频扩散模型之上。扩散模型的前向过程向干净潜变量 $`\mathbf{x}_0`$ 逐步注入高斯噪声：

$$
\mathbf{x}_t = \sqrt{\alpha_t} \mathbf{x}_{t-1} + \sqrt{1 - \alpha_t} \epsilon, \quad \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I}) \tag{1}
$$

其中 $`\alpha_t`$ 控制噪声调度。反向去噪过程利用模型 $`\boldsymbol{\epsilon}_\theta`$ 预测噪声，从 $`\mathbf{x}_t`$ 恢复 $`\mathbf{x}_{t-1}`$：

$$
\mathbf{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t, c) \right) + \sigma_t \mathbf{z} \tag{2}
$$

其中 $`c`$ 为条件信号（首帧或文本）。为对已有视频施加可控修改，采用SDEdit策略：向真实视频潜变量添加中等程度噪声作为再生起点：

$$
\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon \tag{3}
$$

随后在条件于编辑首帧的情况下执行反向去噪，使模型在保留视频结构的同时传播标记点。

### 3.2 反事实标记传播：负向提示增强

核心挑战在于：视频扩散模型的强先验倾向于抹除不自然的视觉标记（如红点），导致标记在生成帧中消失。为解决这一问题，方法引入**负向提示增强的噪声估计**（Figure 2）。

在每个去噪步骤中，同时计算两种条件下的噪声估计：
- $`\epsilon_\theta(\mathbf{x}_t, \phi(\mathbf{c}_I))`$：条件于**编辑首帧** $`\phi(\mathbf{c}_I)`$（含标记点）
- $`\epsilon_\theta(\mathbf{x}_t, \mathbf{c}_I)`$：条件于**未编辑首帧** $`\mathbf{c}_I`$（原始帧）

通过线性外推构造增强噪声估计：

$$
\tilde{\epsilon}_{\theta} \left( \mathbf{x}_t, \mathbf{c}_I \right) = (\lambda + 1) \cdot \epsilon_{\theta}( \mathbf{x}_t, \phi(\mathbf{c}_I) ) - \lambda \cdot \epsilon_{\theta} \left( \mathbf{x}_t, \mathbf{c}_I \right) \tag{5}
$$

其中 $`\lambda`$ 为引导强度。该操作迫使生成分布偏离未编辑版本，偏向包含标记的样本。从分数函数角度，式(5)等价于：

$$
\nabla_{\mathbf{x}_t} \log( p_{\lambda} (\mathbf{x}_t) ) = \nabla_{\mathbf{x}_t} \log \left( p(\mathbf{x}_t \mid \phi(\mathbf{c}_I)) \left[ \frac{p(\phi(\mathbf{c}_I) \mid \mathbf{x}_t)}{p(\mathbf{c}_I \mid \mathbf{x}_t)} \right]^{\lambda} \right) \tag{6}
$$

即通过调节因子 $`\lambda`$ 抑制未编辑条件的影响，机制上类似于无分类器引导（classifier-free guidance）。

### 3.3 粗到细的掩码约束细化

初始传播获得的轨迹可能存在时空错位。为此引入**基于inpainting的粗到细细化**（Figure 3）：在初步轨迹周围构建时空二值掩码 $`\mathbf{m} \in \mathbb{R}^{F \times H \times W}`$，每帧掩码在估计位置半径 $`r`$ 内取值为1。重新执行视频再生时，通过掩码约束反向扩散只在指定区域修改：

$$
\tilde{\mathbf{x}}_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_\theta \right) + \sigma_t \mathbf{z}
$$

$$
\mathbf{x}_{t-1}^{\mathrm{original}} = \sqrt{\bar{\alpha}_{t-1}} \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_{t-1}} \epsilon
$$

$$
\mathbf{x}_{t-1} = \mathbf{m} \odot \tilde{\mathbf{x}}_{t-1} + (1 - \mathbf{m}) \odot \mathbf{x}_{t-1}^{\mathrm{original}} \tag{4}
$$

其中 $`\tilde{\mathbf{x}}_{t-1}`$ 为去噪预测，$`\mathbf{x}_{t-1}^{\mathrm{original}}`$ 为原始加噪信号。掩码区域外保持原始内容不变，仅允许轨迹邻域内进行精细调整，从而纠正生成过程中可能出现的物体位移或标记漂移。

### 3.4 颜色重平衡与轨迹提取

为减少自然场景中与标记颜色相似的像素干扰，在标记插入前对视频进行**颜色重平衡**：降低标记颜色通道的饱和度，抑制环境中相同色调的出现。标记传播完成后，在HSV色彩空间中检测红色像素，结合自适应搜索窗（半径 $`r`$，中心为前一帧位置）提取点轨迹。若搜索窗内未检测到红色像素，判定目标被遮挡，传播上一帧已知位置。

## 实验与分析

### 核心实验结果

本方法在零样本设定下全面超越现有零样本基线，并与自监督方法形成竞争。Table 1 汇总了 TAP-Vid DAVIS 和 Kinetics 两个基准上的完整对比。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_6FFQ007qLX/figures/008_Table_1.jpg]]
*Table 1: TAP-Vid Benchmark Results. We report results on the TAP-Vid First benchmark. Our zero-shot method outperforms all other zero-shot baselines and is competitive with self-supervised and supervised trackers. On TAP-Vid DAVIS-First, it matches self-supervised methods in AJ and exceeds them in occlusion accuracy, highlighting strong object permanence from generative modeling*

**TAP-Vid DAVIS 上的表现。** 方法在 Average Jaccard（AJ）上达到 **42.21**，显著优于最佳零样本基线 SD-DINO 的 29.68（+12.53），并超过自监督方法 Opt-CWM 的 40.16。在遮挡准确率（OA）上，本方法达到 **82.90**，超过所有零样本和自监督方法，体现了视频扩散模型内在的物体持久性先验在处理遮挡时的优势。在位置精度 $\delta_{\mathrm{avg}}^x$ 上，本方法为 57.29，与自监督方法 TAPNext（57.69）基本持平。

**TAP-Vid Kinetics 上的泛化能力。** 在更具挑战性的 Kinetics 基准上，本方法 AJ 为 **27.36**，同样大幅领先 SD-DINO（16.47，+10.89），且 OA 达到 76.86，超过所有零样本和自监督方法。这表明反事实点提示策略在长视频场景中仍能稳定传播标记。

**与有监督方法的差距。** 本方法作为零样本方法，与有监督方法（如 TAPIR 的 AJ 56.2、CoTracker3 的 AJ 76.5）仍有差距，但考虑到未使用任何标注数据或微调，这一结果已具备显著竞争力。

### 关键消融分析

Table 4 系统拆解了跟踪管线各模块的贡献，揭示了方法的因果驱动因子。

**反事实增强是核心驱动模块。** 移除负向提示（w/o counterfactual enhancement）后，AJ 从 48.60 骤降至 **22.03**，OA 从 85.75 暴跌至 61.19。这一崩溃性下降证实：直接通过 SDEdit 插入标记点而不施加反事实引导，视频扩散模型的强先验会导致标记在生成过程中消失——这是方法要解决的核心瓶颈。负向提示（式 5）通过线性外推编辑帧与未编辑帧的噪声估计，迫使生成分布远离“无标记”的原始视频，是方法有效的必要条件。

**粗到细细化纠正时空错位。** 移除 inpainting 细化步骤后，AJ 从 48.60 降至 **42.70**。这表明首轮生成的粗轨迹存在时空错位（如标记点漂移到相邻物体上），通过掩码约束的局部再生（式 4）能有效纠正这些伪影，将性能提升约 6 个 AJ 点。

**颜色重平衡抑制虚假检测。** 关闭颜色重平衡后，AJ 降至 **34.86**。自然场景中与标记颜色相近的色调（如红色物体）会导致颜色检测器产生虚假匹配，降低饱和度预处理能显著抑制这类干扰。

**视觉标记提示的必要性。** 仅使用原始像素颜色进行跟踪（tracker only），AJ 仅为 **11.26**，证实了插入显式视觉标记是整个方法的基础前提——没有标记，扩散模型无法“理解”跟踪任务。

### 生成模型与分辨率的影响

Table 2 和 Table 3 分别考察了视频扩散模型选择和输入分辨率对跟踪性能的影响。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_6FFQ007qLX/figures/011_Table_2.jpg]]
*Table 2: Video Model Ablations. Wan2.1-1.3B and 14B (Wang et al., 2025) outperform CogVideoX (Yang et al., 2024b), showing that stronger video models improve tracking performance*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_6FFQ007qLX/figures/010_Table_3.jpg]]
*Table 3: Image Resolution Ablations. Comparing input resolutions for Wan2.1. Upscaling with (Zhou et al., 2024) improves tracking by better aligning with the model’s training distribution*

**更强生成模型带来更高跟踪精度。** 在 Wan2.1-1.3B、Wan2.1-14B、Wan2.2-14B 和 CogVideoX 的对比中，Wan2.2-14B 取得最优结果（AJ 48.78），Wan2.1-14B 紧随其后（AJ 48.60），而 CogVideoX 仅为 24.15。性能排序与各模型的视频生成质量正相关，表明生成模型的时序一致性和物体持久性能力直接决定了标记传播的可靠性。

**分辨率对齐训练分布至关重要。** 将 DAVIS 视频从 256×256 上采样至模型原生分辨率后，AJ 从 42.21 提升至 45.48；直接使用原始高分辨率帧（original res.）进一步将 AJ 推至 **48.60**。这一趋势说明，输入分辨率与模型训练分布的对齐程度显著影响再生质量——分辨率不匹配会引入额外的分布偏移，损害标记传播的时空一致性。

### 蒸馏：从生成式跟踪到快速推理

Table 5 展示了将生成式跟踪器蒸馏为专用快速模型的结果。以 Wan2.1-1.3B 为教师模型，在 1000 段无标注 Kinetics 视频上生成伪标签轨迹，训练 CoTracker 作为学生模型。蒸馏后的 CoTracker 在 TAP-Vid DAVIS 上 AJ 达到 **37.17**，与教师模型的 38.78 接近（差距仅 1.61），同时推理速度提升数个量级。这证明视频扩散模型生成的轨迹包含可迁移的运动知识，且蒸馏是缓解高计算成本（单次生成 7–30 分钟）的有效路径。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_6FFQ007qLX/figures/015_Table_5.jpg]]
*Table 5: Distilling the generator. We distill our method to CoTracker which achieves performance close to the teacher Wan2.1 and runs orders of magnitude faster*

### 失败模式分析

Figure 7 归纳了四类典型生成失败场景，这些失败揭示了方法的根本局限：

1. **静止点混淆。** 当查询点相对于图像边界保持静止时（如镜头污点），红点不会随物体运动，模型将其视为固定标记而非跟踪目标。这源于模型无法区分“应跟随物体运动的点”与“图像空间中的固定点”。

2. **对称混淆。** 在左右对称的物体（如人体左右肢体）上，标记点可能从一侧跳变到对称的另一侧。这很可能源于扩散模型潜变量空间的压缩表示——对称部位在潜空间中特征相近，导致去噪过程产生歧义。

3. **标记消失。** 在连续帧间红点直接消失，即使有负向提示增强，模型在某些极端情况下仍无法维持标记的可见性。

4. **边界歧义。** 当标记点位于物体边界附近时，红点可能漂移到背景区域，表明模型对前景/背景边界的空间定位存在不确定性。

此外，方法在 TAP-Vid Kubric 等计算机生成视频上性能大幅下降，因为现有视频扩散模型主要训练于真实视频，对合成数据的分布外泛化能力有限。

### 补充图表

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_6FFQ007qLX/figures/009_Table_2.jpg]]

## 方法谱系与知识库定位

### 1. 技术脉络与基线对比

本工作处于**零样本点跟踪**与**视觉生成模型应用**的交叉地带。传统点跟踪方法依赖从预训练模型中提取稠密特征进行帧间匹配，代表性工作包括基于扩散特征的 **DIFT**（Tang et al., 2023）和融合DINO与扩散特征的 **SD-DINO**（Zhang et al., 2023a），以及直接使用 **DINOv2** 特征做最近邻匹配的基线（Oquab et al., 2023）。这些方法的共同瓶颈在于：特征匹配本质上是局部相似性搜索，缺乏对物体持久性和遮挡的显式建模，导致长时遮挡下的轨迹断裂。

本文的核心突破在于**将跟踪问题转化为反事实视频生成问题**：不依赖特征匹配，而是通过在首帧插入视觉标记点（红点），利用预训练视频扩散模型的时序一致性来“再生”包含标记的完整视频，再通过简单的颜色检测器提取轨迹。这一范式转变的关键洞察是：视频扩散模型在训练中习得了物体的永久性（object permanence）——即使目标被遮挡，模型仍“知道”该物体在空间中的持续存在——这正是传统特征匹配方法所缺失的因果机制。

与本文最接近的自监督方法是 **Opt-CWM**（Stojanov et al., 2025），同样采用反事实建模思路，但Opt-CWM需要针对特定场景训练世界模型，而本文完全零样本，直接利用现成的视频扩散模型。在TAP-Vid DAVIS基准上，本文方法以AJ=42.21显著超越所有零样本基线（SD-DINO为29.68），且遮挡准确率OA=82.90甚至超过自监督方法Opt-CWM（80.87），验证了生成式先验在处理遮挡上的独特优势。

在监督方法侧，**TAPIR**（Doersch et al., 2023）和 **CoTracker3**（Karaev et al., 2024b）仍保持领先（AJ分别为56.2和60.6），但本文的蒸馏实验表明：将生成式跟踪器的伪标签用于训练CoTracker，可获得AJ=37.17的快速跟踪器，接近教师模型Wan2.1-1.3B的38.78，且推理速度提升数个量级。这揭示了生成模型作为“数据工厂”为判别式跟踪器提供监督信号的潜力。

### 2. 核心机制与消融支撑

方法的核心驱动因子是**反事实信号增强**（负向提示）。消融实验（Table 4）提供了决定性证据：移除该模块后，AJ从48.60骤降至22.03，性能崩溃。其因果机制通过式（5）实现：

$$\tilde{\epsilon}_{\theta} (\mathbf{x}_t, \mathbf{c}_I) = (\lambda + 1) \cdot \epsilon_{\theta}(\mathbf{x}_t, \phi(\mathbf{c}_I)) - \lambda \cdot \epsilon_{\theta}(\mathbf{x}_t, \mathbf{c}_I)$$

即在每一步去噪中，将条件于编辑首帧（含标记）和原始首帧（无标记）的噪声估计进行线性外推，迫使生成分布远离“无标记”版本。从分数函数角度（式6），这等效于在条件于编辑图像的同时，通过调节因子$\lambda$抑制未编辑条件的影响，与无分类器引导（classifier-free guidance）的机理同源。若无此机制，扩散模型的强先验会将红色标记视为“不自然的扰动”而在生成中逐渐抹除。

**粗到细细化**（coarse-to-fine refinement）是第二大贡献模块：移除后AJ从48.60降至42.70。其作用在于纠正初始生成中的时空错位——模型可能将标记点置于语义正确但像素偏移的位置。通过构建仅覆盖轨迹周围小区域的时空掩码$\mathbf{m}$，并利用式（4）的inpainting约束重新生成，可在保持背景不变的前提下精细调整标记位置。**颜色重平衡**（移除后AJ降至34.86）则是工程层面的必要补充，通过降低红色通道饱和度抑制自然场景中的相似色调干扰。

### 3. 适用边界与局限

**计算成本**是首要瓶颈：生成50帧视频需7–30分钟（单张A40/L40S GPU），无法实时应用。蒸馏方案（如蒸馏至CoTracker）缓解了推理速度问题，但蒸馏本身仍需先运行完整的生成管线获取伪标签。

**生成失败模式**（Figure 7）揭示了方法的根本局限：
- **静止点问题**：当查询点对应的物理点静止时，红色标记可能如同镜头污点般固定在画面中，模型无法区分“应跟踪的静止物体”与“画面叠加物”。
- **对称混淆**：对称物体（如左右肢体）在潜空间压缩后特征高度相似，导致标记在对称部位间跳转。
- **标记消失**：在连续帧中红色圆点逐渐淡化直至消失，表明负向提示并非在所有情形下都能完全克服模型先验。
- **边界歧义**：标记点位于物体边界时，可能漂移到背景区域。

这些失败模式与视频扩散模型的**潜空间压缩损失**和**训练数据分布偏置**密切相关。由于现有视频扩散模型（如Wan2.1、CogVideoX）主要训练于真实场景视频，方法在**合成数据**（如TAP-Vid Kubric）上性能大幅下降，这是当前生成式方法的共性局限。

此外，当前设计仅支持**单点跟踪**，多点需多次独立运行，缺乏多轨迹间的一致性约束。

### 4. 开放问题

1. **跨模型蒸馏的泛化性**：蒸馏方案目前仅在Wan2.1-1.3B至CoTracker上验证，能否推广到CogVideoX等其他架构并维持竞争力，尚待检验。

2. **反事实增强的效率优化**：当前负向提示需在每步去噪中执行两次模型前向传播（编辑条件与原始条件），是否有更高效的替代策略（如对条件嵌入进行操作而非噪声空间外推）可降低计算开销？

3. **密集预测的扩展**：点提示思路能否自然推广到密集光流估计或多点联合跟踪？多点情形下需解决标记间相互干扰和轨迹一致性问题。

4. **域适应的可行性**：对于计算机生成视频，能否通过轻量级的提示工程调整（如修改颜色映射策略）或少量领域数据的生成微调来提升鲁棒性？

5. **生成与判别闭环**：能否将点提示思路与自监督学习结合，让跟踪器在推理过程中同时优化其内部表示？这将使模型从“一次性生成”转向“迭代式精化”，可能进一步缩小与监督方法的差距。

## 原文 PDF

![[paperPDFs/ICLR_2026/Point_Prompting_Counterfactual_Tracking_with_Video_Diffusion_Models.pdf]]
