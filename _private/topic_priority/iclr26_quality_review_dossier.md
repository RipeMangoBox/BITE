# ICLR 2026 Quality Review Dossier

## Candidate 1
- path: obsidian-vault/paper/ICLR_2026/P__BWCache_Accelerating_Video_Diffusion_Transformers_through_Block-Wise_Caching.md
- title: BWCache: Accelerating Video Diffusion Transformers through Block-Wise Caching
- issues: dup_caption_prefix, topic_placeholder, suspicious_short_formula:1, missing_figure_embed:10,12,14
- topic_row: [[T__ICLR_2026]]
- head_excerpt:
```md
---
title: "BWCache: Accelerating Video Diffusion Transformers through Block-Wise Caching"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/BWCache_Accelerating_Video_Diffusion_Transformers_through_Block-Wise_Caching.pdf
aliases:
- Block-Wise Caching (BWCache)
acceptance: accepted
paradigm: DiT块特征在扩散时间步上呈现U形变化模式，中间时间步高度相似，因此可以安全地缓存和重用，从而消除冗余计算。
---

# BWCache: Accelerating Video Diffusion Transformers through Block-Wise Caching

> [!tip] 核心洞察
> DiT块特征在扩散时间步上呈现U形变化模式，中间时间步高度相似，因此可以安全地缓存和重用，从而消除冗余计算。

| 字段 | 内容 |
|------|------|
| 中文题名 | BWCache：通过逐块缓存加速视频扩散Transformer |
| 英文题名 | BWCache: Accelerating Video Diffusion Transformers through Block-Wise Caching |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=5bJZtzTFYy) |
| Topic | [[T__ICLR_2026]] |
| Method | Block-Wise Caching (BWCache) |
| Dataset | Open-Sora (51帧, 480P), Open-Sora (51帧, 480P), Open-Sora-Plan (65帧, 512×512), Open-Sora-Plan (65帧, 512×512) |

> [!tip] 效果简介
> - Open-Sora (51帧, 480P) 上，Speedup 为 1.61×，对比 1.0× (原始)，变化 +0.61×。
> - Open-Sora (51帧, 480P) 上，VBench 为 80.03%，对比 80.12% (原始)，变化 -0.09%。
> - Open-Sora-Plan (65帧, 512×512) 上，Speedup 为 2.24×，对比 1.0× (原始)，变化 +1.24×。

## 概述

本文提出**BWCache (Block-Wise Caching)**，一种无需训练的即插即用方法，用于加速基于DiT (Diffusion Transformer) 的视频生成模型。核心思想是：在扩散时间步上，DiT块的特征变化呈现**U形模式**——中间时间步的特征高度相似，因此可以安全地缓存并重用这些块特征，从而消除冗余计算。BWCache通过一个基于相邻时间步块特征差异的相似性指标，动态决定是否触发缓存重用，并采用周期性重计算策略缓解潜在漂移。实验表明，BWCache在多个主流视频DiT模型（Open-Sora、Open-Sora-Plan、Latte、Wan 2.1、HunyuanVideo）上，在保持可比视觉质量的同时，实现了最高**2.6倍**的加速。

## 背景与动机
```
- table_lines:
```md
*Table 1: Table 1: Comparison of visual quality and efficiency on a single GPU. Video generation specifications: Open-Sora (51 frames, 480P), Open-Sora-Plan (65 frames, 512×512), Latte (16 frames, 512×512), Wan 2.1 (81 frames, 480P), HunyuanVideo (129 frames, 544P). LPIPS, SSIM, and PSNR are calculated against the original model results.*
*Table 2: Table 2: Inference efficiency when scaling to multiple GPUs with DSP.*
*Table 4: Table 4: Impact of different reuse rates.*
```
- formula_section_5_2:
```md
### 5.2 相似性指标

**相对L1距离**（Eq.(5)）：衡量块i在相邻时间步t和t+1之间的特征变化：
$$\mathrm{L1}_{\mathrm{rel}}(h_{t,i}) = \frac{\|h_{t,i} - h_{t+1,i}\|_1}{\|h_{t+1,i}\|_1}$$

**聚合相对L1距离**（Eq.(6)）：时间步t上所有N个DiT块的相对L1距离之和：
$$\mathrm{ARL1}(t) = \sum_{n=1}^N \mathrm{L1}_{\mathrm{rel}}(h_{t,i})$$

**BWCache相似性指标**（Eq.(7)）：触发缓存的条件——平均相对L1距离低于阈值δ：
$$\sum_{n=1}^N \mathrm{L1}_{\mathrm{rel}}(h_{t,i}) / N < \delta$$

```

## Candidate 2
- path: obsidian-vault/paper/ICLR_2026/P__Beyond_Masks_Efficient_Flexible_Diffusion_Language_Models_via_Deletion-Insertion_Processes.md
- title: Beyond Masks: Efficient, Flexible Diffusion Language Models via Deletion-Insertion Processes
- issues: dup_caption_prefix, topic_placeholder, suspicious_short_formula:1, missing_figure_embed:2
- topic_row: [[T__ICLR_2026]]
- head_excerpt:
```md
---
title: "Beyond Masks: Efficient, Flexible Diffusion Language Models via Deletion-Insertion Processes"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Beyond_Masks_Efficient_Flexible_Diffusion_Language_Models_via_Deletion-Insertion_Processes.pdf
aliases:
- Deletion-Insertion Diffusion language models (DID)
acceptance: accepted
paradigm: 通过将前向过程定义为独立标记删除，后向过程定义为基于学习到的插入分数的标记插入，DID模型能够原生支持变长序列，消除冗余计算，并实现内在的自校正机制。
---

# Beyond Masks: Efficient, Flexible Diffusion Language Models via Deletion-Insertion Processes

> [!tip] 核心洞察
> 通过将前向过程定义为独立标记删除，后向过程定义为基于学习到的插入分数的标记插入，DID模型能够原生支持变长序列，消除冗余计算，并实现内在的自校正机制。

| 字段 | 内容 |
|------|------|
| 中文题名 | 超越掩码：基于删除-插入过程的高效灵活扩散语言模型 |
| 英文题名 | Beyond Masks: Efficient, Flexible Diffusion Language Models via Deletion-Insertion Processes |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=VbvXjs5f72) |
| Topic | [[T__ICLR_2026]] |
| Method | Deletion-Insertion Diffusion language models (DID) |
| Dataset | WikiText, Lambada, OpenWebText (固定长度), OpenWebText (固定长度) |

> [!tip] 效果简介
> - WikiText 上，零样本困惑度（越低越好） 为 36.91，对比 38.27，变化 -1.36。
> - Lambada 上，零样本困惑度（越低越好） 为 48.00，对比 51.82，变化 -3.82。
> - OpenWebText (固定长度) 上，训练时间加速比（越高越好） 为 1.99×，对比 1.0×，变化 +0.99×。

## 概述

本文提出了一种新型扩散语言模型——**Deletion-Insertion Diffusion language models (DID)**，旨在解决现有掩码扩散语言模型（MDLM）中因大量非信息性`<MASK>`和`<PAD>`标记导致的计算效率低下问题。DID的核心创新在于将扩散过程从传统的掩码-去掩码范式彻底替换为删除-插入范式：前向过程逐步删除序列中的标记直至为空，后向过程从空序列开始逐步插入标记以重建完整序列。这一范式转换使得DID能够原生支持变长序列，消除冗余计算，并具备内在的自校正机制。实验结果表明，在固定长度设置下，DID实现了高达**1.99倍**的训练加速和**1.58倍**的推理加速；在变长设置下，加速比分别提升至**3.42倍**和**3.79倍**，同时生成质量显著优于现有基线模型。

## 背景与动机
```
- figure_lines:
```md
*Figure 1: (a) MDLMs, sequences padded to length 10.*
```
- table_lines:
```md
*Table 1: Table 1: Zero-shot language modeling perplexity. Results for diffusion models are perplexity upper bounds.*
*Table 2: Table 2: Generative perplexity (PPL, evaluated by GPT2 Large), unigram entropy, inference time (in seconds), speedup, and average generation length for fixed-length models under different total denoising steps.*
*Table 3: Table 3: Average training time (in seconds) per 50 steps (i.e. batches) on OpenWebText.*
```
- formula_section_5_2:
```md
### 5.2 后向插入过程与插入分数

后向过程的目标是学习前向过程的时间反转。为此，定义插入分数：

$$\bar{s}(\mathbf{x}_t, t)[i, v] = \frac{\mathbb{E}_{\mathbf{x}_0}\left[(1 - e^{-\bar{\sigma}(t)})^{|\mathbf{x}_0|} N(\mathrm{Ins}(\mathbf{x}_t, i, v), \mathbf{x}_0)\right]}{\mathbb{E}_{\mathbf{x}_0}\left[(1 - e^{-\bar{\sigma}(t)})^{|\mathbf{x}_0|} N(\mathbf{x}_t, \mathbf{x}_0)\right]}$$

该分数表示在位置i插入标记v的期望概率比。反向转移率可表示为插入分数的加权和：

$$\tilde{Q}_t(\mathbf{x}_t, \mathbf{y}) = \sum_{i \in I(\mathbf{x}_t, \mathbf{y})} \left( \frac{\sigma(t) e^{-\bar{\sigma}(t)}}{1 - e^{-\bar{\sigma}(t)}} \bar{s}(\mathbf{x}_t, t)[i, v(\mathbf{x}_t, \mathbf{y})] \right)$$

```

## Candidate 3
- path: obsidian-vault/paper/ICLR_2026/P__Boomerang_Distillation_Enables_Zero-Shot_Model_Size_Interpolation.md
- title: Boomerang Distillation Enables Zero-Shot Model Size Interpolation
- issues: dup_caption_prefix, topic_placeholder, suspicious_short_formula:1, missing_figure_embed:10,23,3
- topic_row: [[T__ICLR_2026]]
- head_excerpt:
```md
---
title: Boomerang Distillation Enables Zero-Shot Model Size Interpolation
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Boomerang_Distillation_Enables_Zero-Shot_Model_Size_Interpolation.pdf
aliases:
- Boomerang Distillation Enables Zero-Shot Model Size Interpolation
acceptance: accepted
paradigm: 在教师权重初始化和对齐蒸馏（特别是余弦距离损失）的条件下，将教师层块插回蒸馏后的学生模型可以零样本地生成性能平滑插值的中间尺寸模型，且无需额外训练。
---

# Boomerang Distillation Enables Zero-Shot Model Size Interpolation

> [!tip] 核心洞察
> 在教师权重初始化和对齐蒸馏（特别是余弦距离损失）的条件下，将教师层块插回蒸馏后的学生模型可以零样本地生成性能平滑插值的中间尺寸模型，且无需额外训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | 回旋镖蒸馏：零样本模型尺寸插值 |
| 英文题名 | Boomerang Distillation Enables Zero-Shot Model Size Interpolation |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=4ZU8v4s3IR) |
| Topic | [[T__ICLR_2026]] |
| Method | Boomerang Distillation |
| Dataset | 10个分类数据集（平均）, 3个生成数据集（平均）, WikiText, Qwen3-4B-Base 教师模型 |

> [!tip] 效果简介
> - 10个分类数据集（平均） 上，分类准确率 为 平滑插值，在中间尺寸上优于剪枝基线，对比 Naive Layer Pruning: 在小于4B参数时显著下降，变化 显著优于。
> - 3个生成数据集（平均） 上，精确匹配准确率 为 平滑插值，在较小模型上保持较高生成性能，对比 Naive Layer Pruning: 生成性能快速下降，变化 显著优于。
> - WikiText 上，困惑度 为 在学生和教师之间平滑插值，对比 Naive Layer Pruning: 随层数减少困惑度急剧上升，变化 显著优于。

## 概述

本文提出 **Boomerang Distillation**（回旋镖蒸馏），一种能够零样本（zero-shot）生成任意中间尺寸语言模型的高效方法。核心思想是：首先将大型教师模型通过层剪枝（layer pruning）初始化为一个小型学生模型，然后使用包含余弦距离对齐损失的蒸馏目标训练该学生模型；训练完成后，通过将学生层替换为对应的教师层块（student patching），无需任何额外训练即可生成一系列尺寸和性能平滑插值的中间模型。实验表明，该方法在多个模型族（Qwen3、Pythia、Llama-3.2）上均有效，相比朴素层剪枝和随机初始化蒸馏基线显著更优，且计算开销仅为独立蒸馏每个中间模型的 1/14.53 至 1/19.17。

## 背景与动机
```
- figure_lines:
```md
*Figure 1: Figure 1: Overview of boomerang distillation. ➀ In this example, the student model is initialized by dropping layers from the pretrained teacher model. ➁ The teacher model is distilled into the student model with cross-entropy loss, knowledge distillation loss, and cosine distance loss (Equation 1). ➂ After training the student model, a block of teacher layers corresponding to a student layer is inserted back into the model to get the zero-shot interpolated model.*
*Figure 2: Qwen3-4B-Base Distilled models Pruned models Interpolated models*
```
- table_lines:
```md
*Table 1: Table 1: The sizes of the initialized student models after pruning the layers from the teacher model. We note that the Pythia models do not employ weight tying, so their train and inference parameters are equivalent. On the other hand, the Qwen and Llama models weight tie their embedding layers and LM heads, so their inference-time parameters are higher than their training parameters. This is because both the embedding layer and LM head are used during inference.*
*Table 2: Table 2: Hyperparameters used to train the student model. We choose the training hyperparameters to align with the values used in Pythia training (Biderman et al., 2023) and set the KLDiv and cosine distance weights such that the cross entropy, KLDiv, and cosine distance loss are approximately equal in magnitude at the beginning of training.*
*Table 3: Table 3: Boomerang distillation provides significant computational speedup compared to individually distilling intermediate models. For Qwen3-4B-Base, Pythia-2.8B, and Llama-3.2-3B, we report the FLOPS required to individually distill each intermediate model versus boomerang distillation for the same number of training tokens (2.1B tokens). We can reduce FLOPs by 19.17x for Qwen, 17.01x for Pythia, and 14.53x for Llama using boomerang distillation.*
```
- formula_section_5_2:
```md
### 5.2 知识蒸馏目标

学生模型训练的总损失为（Equation 1）：

$$\mathcal{L}(x, \pmb{\theta}_S) = \mathcal{L}_{\mathrm{CE}}(x_j \mid x_{<j}; \pmb{\theta}_S) + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}}(x_{<j}; \pmb{\theta}_S) + \lambda_{\mathrm{cos}} \sum_{i=1}^M \mathcal{L}_{\mathrm{cos}}^{(i)}(x_{<j}; \pmb{\theta}_S)$$

其中：

- **交叉熵损失** $\mathcal{L}_{\mathrm{CE}}$：标准语言建模损失。
- **KL 散度损失**（知识蒸馏损失）：

$$\mathcal{L}_{\mathrm{KL}}(\boldsymbol{x}_{<j}; \boldsymbol{\theta}_S) = \boldsymbol{\tau}^2 \cdot \mathrm{KL}\big(\mathrm{softmax}(\boldsymbol{z}_j^T / \boldsymbol{\tau}) ~ \lVert ~ \mathrm{softmax}(\boldsymbol{z}_j^S / \boldsymbol{\tau})\big)$$

温度 τ 控制软化程度。

- **余弦距离损失**（对齐损失）：

$$\mathcal{L}_{\mathrm{cos}}^{(i)}(x_{<j}; \boldsymbol{\theta}_S) = 1 - \frac{\boldsymbol{x}_j^{(S,i)} \cdot \boldsymbol{x}_j^{(T,l_{i+1}-1)}}{||\boldsymbol{x}_j^{(S,i)}|| ~ ||\boldsymbol{x}_j^{(T,l_{i+1}-1)}||}$$

鼓励学生第 i 层隐藏状态接近对应教师块输出（第 ℓ_{i+1}-1 层）的隐藏状态。

```

## Candidate 4
- path: obsidian-vault/paper/ICLR_2026/P__Bridging_Degradation_Discrimination_and_Generation_for_Universal_Image_Restoration.md
- title: Bridging Degradation Discrimination and Generation for Universal Image Restoration
- issues: dup_caption_prefix, topic_placeholder, suspicious_short_formula:6, missing_figure_embed:2,9
- topic_row: [[T__ICLR_2026]]
- head_excerpt:
```md
---
title: Bridging Degradation Discrimination and Generation for Universal Image Restoration
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Bridging_Degradation_Discrimination_and_Generation_for_Universal_Image_Restoration.pdf
aliases:
- BDG (Bridging Degradation discrimination and Generation)
acceptance: accepted
paradigm: 通过多角度多尺度灰度共生矩阵（MAS-GLCM）实现细粒度退化判别，并将其特征与扩散模型的中间特征进行双向对齐，从而在单一模型中同时保留生成先验和退化判别能力，实现保真度与感知质量的平衡。
---

# Bridging Degradation Discrimination and Generation for Universal Image Restoration

> [!tip] 核心洞察
> 通过多角度多尺度灰度共生矩阵（MAS-GLCM）实现细粒度退化判别，并将其特征与扩散模型的中间特征进行双向对齐，从而在单一模型中同时保留生成先验和退化判别能力，实现保真度与感知质量的平衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | 桥接退化判别与生成：面向通用图像复原 |
| 英文题名 | Bridging Degradation Discrimination and Generation for Universal Image Restoration |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=hVFoiCDiMB) |
| Topic | [[T__ICLR_2026]] |
| Method | BDG (Bridging Degradation discrimination and Generation) |
| Dataset | 5D All-in-One (Deraining), 5D All-in-One (Low-light Enhancement), 5D All-in-One (Desnowing), 5D All-in-One (Dehazing) |

> [!tip] 效果简介
> - 5D All-in-One (Deraining) 上，PSNR 为 34.75，对比 31.03 (DiffUIR)，变化 +3.72。
> - 5D All-in-One (Low-light Enhancement) 上，PSNR 为 27.42，对比 25.12 (DiffUIR)，变化 +2.30。
> - 5D All-in-One (Desnowing) 上，PSNR 为 32.86，对比 32.86 (DiffUIR)，变化 0.00。

## 概述

本文提出BDG（Bridging Degradation discrimination and Generation）框架，旨在解决通用图像复原中退化判别能力与生成先验难以兼得的根本矛盾。核心创新包括：（1）提出多角度多尺度灰度共生矩阵（MAS-GLCM）实现细粒度退化判别；（2）设计三阶段扩散训练范式（生成预训练→桥接阶段→复原微调），通过双向特征对齐将退化判别信息注入扩散模型。实验表明，BDG在5D全合一复原任务中全面超越DiffUIR，在去雨任务上PSNR提升3.72 dB；在真实世界超分辨率任务中，在DIV2K-Val上PSNR达到24.1977，比第二好的扩散方法高出2.45 dB。

## 背景与动机
```
- table_lines:
```md
*Table 1: Table 1: MAS-GLCM has substantial capability in the classification of both types and levels of degradation.*
*Table 2: We train a 5D all-in-one image restoration model with simulated dataset following DiffUIR (Zheng et al., 2024). This model is validated on simulated and real-world scenarios. Table 2: All-in-one Image Restoration results. † means the methods are retrained within datasets we used for fair comparison. The best and second results are shown in red and blue respectively.*
*Table 3: Table 3: Real-world restoration results in four real-world degradation types under the zero-shot setting. The best and second results are shown in red and blue respectively.*
```
- formula_section_5_2:
```md
### 5.2 扩散模型采样公式

前向过程（Eq.3）：
$$x_t = x_{t-1} + \alpha_t x_{res} + \beta_t \epsilon_{t-1} - \delta_t x_{lq}$$

其中x_res = x_lq - x_hq为残差，α_t、β_t、δ_t分别为残差、噪声和低质量图像的系数。

采样公式（Eq.4，隐式概率模型）：
$$x_{t-1} = x_t - \alpha_t x_{res}^\theta - \frac{\beta_t^2}{\overline{\beta}_t} \epsilon^\theta + \delta_t x_{lq}$$

三个系数共同控制模型行为模式：
- 当α_t≡0且δ_t≡0时，模型仅具备生成能力（退化为VE SDE去噪公式）
- 当仅δ_t≡0时，模型进入桥接阶段，可同时保留生成先验并感知退化
- 当所有系数正常调度时，模型进入复原阶段，直接注入低质量图像以增强保真度

```

## Candidate 5
- path: obsidian-vault/paper/ICLR_2026/P__ACCORD_Alleviating_Concept_Coupling_through_Dependence_Regularization_for_Text-to-Image_Diffusion_Personalization.md
- title: ACCORD: Alleviating Concept Coupling through Dependence Regularization for Text-to-Image Diffusion Personalization
- issues: manual_review_placeholder, suspicious_short_formula:3, missing_figure_embed:12,14,15
- topic_row: Vision / Multimodal Applications, Image and Video Generation
- head_excerpt:
```md
---
title: "ACCORD: Alleviating Concept Coupling through Dependence Regularization for Text-to-Image Diffusion Personalization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ACCORD_Alleviating_Concept_Coupling_through_Dependence_Regularization_for_Text-to-Image_Diffusion_Personalization.pdf
aliases:
- "ACCORD: Alleviating Concept Coupling through Dependence Regularization for Text-to-Image Diffusion Personalization"
acceptance: accepted
paradigm: ""
---

# ACCORD: Alleviating Concept Coupling through Dependence Regularization for Text-to-Image Diffusion Personalization

> [!tip] 核心洞察
> 待人工复核。

| 字段 | 内容 |
|------|------|
| 中文题名 | ACCORD: Alleviating Concept Coupling through Dependence Regularization for Text-to-Image Diffusion Personalization |
| 英文题名 | ACCORD: Alleviating Concept Coupling through Dependence Regularization for Text-to-Image Diffusion Personalization |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=CKYsYlRdCM) |
| Topic | Vision / Multimodal Applications, Image and Video Generation |
| Method |  |
| Dataset |  |

## 概述

本文提出 **ACCORD**（Alleviating Concept Coupling through Dependence Regularization）框架，旨在解决文本到图像（Text-to-Image, T2I）扩散模型个性化微调中的**概念耦合**（concept coupling）问题。概念耦合指模型在微调后，将个性化目标概念（如特定背包）与参考图像中出现的无关概念（如女孩）错误绑定，导致生成图像违背文本提示。

ACCORD 首次将概念耦合形式化为统计依赖问题，识别出两个根本原因：**去噪依赖偏差**（Denoising Dependence Discrepancy）和**先验依赖偏差**（Prior Dependence Discrepancy）。针对这两个原因，论文提出两个即插即用的正则化损失：**去噪解耦损失**（Denoising Decouple Loss, DDLoss）和**先验解耦损失**（Prior Decouple Loss, PDLoss）。实验表明，ACCORD 在主体、风格和人脸个性化任务中均能实现保真度与文本控制之间的更优平衡。

## 背景与动机

文本到图像扩散模型（如 Stable Diffusion）通过在大规模图文对数据上训练，能够根据文本提示生成高质量图像。个性化微调旨在让模型学习特定概念（如用户宠物、特定风格），通常使用少量参考图像进行微调。

```
- figure_lines:
```md
*Figure 1: Illustration of the concept coupling problem. The target is a “backpack*”, but reference images always pair it with a “girl”. Standard finetuning incorrectly learns to bind these concepts, causing the model to generate the unwanted ’girl’ and violate the text prompt.*
```
- table_lines:
```md
*Table 1: Quantitative results on DreamBench. The “*” indicates results using per-subject/style loss weights, tuned on a small validation set. “Params.” indicates the number of tunable parameters. The W(in)/L(oss) rate is calculated by pairwise human comparison between the anonymous generated results of the baseline and Ours*, with ties omitted. ‘PA’ denotes percent agreement, namely the percentage of samples receiving consistent judgments from human annotators. The comparison methods improved based on the baseline are italicized. Lemma 2. For an observation \mathbf { c } _ { j } and condition \mathbf { c } _ { k } , the InfoNCE objective seeks to estimate a function \mathcal { F } ( \mathbf...*
*Table 2: Quantitative results on StyleBench. The “*” denotes adjusting DDLoss and PDLoss weights across different styles. “Gram-D” is the gram matrix distance.*
*Table 3: Ablation study on the effects of DDLoss, and PDLoss across backbones.*
```
- formula_section_5_2:
```md
### 5.2 概念耦合的形式化

概念耦合的特征为：

$$\mathbb{E}_{\mathbf{x}_\theta}[ |\log r(\mathbf{c}_p, \mathbf{c}_g | \mathbf{x}_{\theta,0}) - \log r(\mathbf{c}_s, \mathbf{c}_g) | ] \gg 0$$

其中 $\mathbf{c}_s$ 是 $\mathbf{c}_p$ 的超类（如“背包”是“背包*”的超类）。

```

## Candidate 6
- path: obsidian-vault/paper/ICLR_2026/P__BranchGRPO_Stable_and_Efficient_GRPO_with_Structured_Branching_in_Diffusion_Models.md
- title: BranchGRPO: Stable and Efficient GRPO with Structured Branching in Diffusion Models
- issues: dup_caption_prefix, topic_placeholder, missing_figure_embed:3,6,7
- topic_row: [[T__ICLR_2026]]
- head_excerpt:
```md
---
title: "BranchGRPO: Stable and Efficient GRPO with Structured Branching in Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/BranchGRPO_Stable_and_Efficient_GRPO_with_Structured_Branching_in_Diffusion_Models.pdf
aliases:
- "BranchGRPO: Stable and Efficient GRPO with Structured Branching in Diffusion Models"
acceptance: accepted
paradigm: 通过树状rollout结构，在保持探索多样性的同时，利用共享前缀摊销计算成本；通过路径概率融合和深度归一化，将稀疏的终端奖励转化为密集的逐步骤优势信号，实现更稳定、更高效的策略优化。
---

# BranchGRPO: Stable and Efficient GRPO with Structured Branching in Diffusion Models

> [!tip] 核心洞察
> 通过树状rollout结构，在保持探索多样性的同时，利用共享前缀摊销计算成本；通过路径概率融合和深度归一化，将稀疏的终端奖励转化为密集的逐步骤优势信号，实现更稳定、更高效的策略优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | BranchGRPO：基于结构化分支的稳定高效扩散模型GRPO方法 |
| 英文题名 | BranchGRPO: Stable and Efficient GRPO with Structured Branching in Diffusion Models |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=T2nP2IQasd) |
| Topic | [[T__ICLR_2026]] |
| Method | BranchGRPO |
| Dataset | HPSv2.1 (FLUX.1-Dev), HPSv2.1 (FLUX.1-Dev), HPSv2.1 (FLUX.1-Dev), HPSv2.1 (FLUX.1-Dev) |

> [!tip] 效果简介
> - HPSv2.1 (FLUX.1-Dev) 上，HPS-v2.1 为 0.369，对比 0.360，变化 +0.009。
> - HPSv2.1 (FLUX.1-Dev) 上，PickScore 为 0.231，对比 0.227，变化 +0.004。
> - HPSv2.1 (FLUX.1-Dev) 上，ImageReward 为 1.625，对比 1.573，变化 +0.052。

## 概述

BranchGRPO是一种针对扩散模型GRPO（Group Relative Policy Optimization）训练的结构化改进方法。该方法通过将传统的顺序rollout重构为树状结构，在去噪过程中引入分支，共享前缀以摊销计算，并通过奖励融合与深度归一化将稀疏终端奖励转化为密集的逐步骤优势信号。实验表明，BranchGRPO在HPSv2.1图像对齐上比DanceGRPO提升高达16%的对齐分数，同时将每轮训练时间减少近55%；其混合变体BranchGRPO-Mix进一步将训练加速至DanceGRPO的4.7倍，且不降低对齐性能。

## 背景与动机
```
- table_lines:
```md
*Table 1: Table 1: Efficiency–quality comparison. The best and second-best results in each column are highlighted in bold and underline, respectively. NFE denotes the number of function evaluations of the denoiser. For branching methods, we report the average per-sample NFE, computed as the total function evaluations in the tree divided by the number of final samples.*
*Table 2: Table 2: Generalization on SD3.5-M and integration into GRPO-style training pipelines. Branch-GRPO consistently improves alignment quality and training efficiency.*
*Table 3: Table 3: Prompt-conditioned diversity under different branching schedules (new).*
```
- formula_section_5_2:
```md
### 5.2 分支采样（分裂步）

在分裂步生成K个相关子节点，使用共享噪声ξ_0和分支特定创新η_b，由相关性参数s控制：

$$z _ { i + 1 } ^ { ( b ) } = \mu _ { \theta } ( z _ { i } , t _ { i } ) \ + \ g _ { t _ { i } } \sqrt { h _ { i } } \xi _ { b } , \qquad \xi _ { b } = \frac { \xi _ { 0 } + s \eta _ { b } } { \sqrt { 1 + s ^ { 2 } } } , \quad b = 1 , \ldots , K$$

```

## Candidate 7
- path: obsidian-vault/paper/ICLR_2026/P__Bridging_the_Distribution_Gap_to_Harness_Pretrained_Diffusion_Priors_for_Super-Resolution.md
- title: Bridging the Distribution Gap to Harness Pretrained Diffusion Priors for Super-Resolution
- issues: dup_caption_prefix, topic_placeholder, missing_figure_embed:2,5,6
- topic_row: [[T__ICLR_2026]]
- head_excerpt:
```md
---
title: Bridging the Distribution Gap to Harness Pretrained Diffusion Priors for Super-Resolution
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Bridging_the_Distribution_Gap_to_Harness_Pretrained_Diffusion_Priors_for_Super-Resolution.pdf
aliases:
- DM-SR (Distribution Matching Super-Resolution)
acceptance: accepted
paradigm: 与其修改预训练扩散模型，不如将LR图像直接变换到扩散模型训练时见过的分布（即噪声-图像混合），从而在不微调扩散模型的前提下充分利用其生成先验，实现单步高质量超分辨率。
---

# Bridging the Distribution Gap to Harness Pretrained Diffusion Priors for Super-Resolution

> [!tip] 核心洞察
> 与其修改预训练扩散模型，不如将LR图像直接变换到扩散模型训练时见过的分布（即噪声-图像混合），从而在不微调扩散模型的前提下充分利用其生成先验，实现单步高质量超分辨率。

| 字段 | 内容 |
|------|------|
| 中文题名 | 弥合分布差距以利用预训练扩散先验进行超分辨率重建 |
| 英文题名 | Bridging the Distribution Gap to Harness Pretrained Diffusion Priors for Super-Resolution |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=66Ad0i78lW) |
| Topic | [[T__ICLR_2026]] |
| Method | DM-SR (Distribution Matching Super-Resolution) |
| Dataset | ImageNet, ImageNet, ImageNet, ImageNet |

> [!tip] 效果简介
> - ImageNet 上，BRISQUE 为 13.427，对比 最佳基线值未明确给出，变化 最佳。
> - ImageNet 上，LIQE 为 4.699，对比 最佳基线值未明确给出，变化 最佳。
> - ImageNet 上，CLIP-IQA 为 0.785，对比 最佳基线值未明确给出，变化 最佳。

## 概述

本文提出**分布匹配超分辨率（Distribution Matching Super-Resolution, DM-SR）**，一种无需微调预训练扩散模型即可实现单步高质量超分辨率的新方法。核心思想是：与其修改扩散模型以适应低分辨率（LR）输入，不如训练一个轻量级图像编码器，将LR图像直接映射到扩散模型训练时熟悉的噪声-图像混合分布。通过自适应预测与输入退化程度匹配的噪声水平（时间步），DM-SR在多个基准数据集上的感知质量指标（如BRISQUE, CLIPIQA, MUSIQ）达到最优，且推理速度极快（92 ms，与OSEDiff和InvSR相当，远快于StableSR的10000 ms）。

## 背景与动机
```
- figure_lines:
```md
*Figure 1: Figure 1: ×4 super-resolution comparison on various images. The left half of each image shows the bicubic upsampled input, and the right half shows the output from our DM-SR. Compared to previous methods, DM-SR produces the most perceptually pleasing results. (Zoom-in for best view)*
```
- table_lines:
```md
*Table 1: Table 1: × 4 SR non-reference metrics comparison on various benchmark datasets. Best numbers are denoted with bold.*
*Table 2: Table 2: (Left) × 4 SR reference metrics comparison on RealSR dataset. (Right) Efficiency Comparison of DM-SR with previous SR methods on SR task. Specifically, we upsample images of size \mathbb { R } ^ { 1 2 8 \times 1 2 8 \times 3 } using a single NVIDIA A100 GPU to measure the runtime of each method. Table 3: Comparison of DM-SR on Realset80 with various timesteps. Our final model adaptively predicts \hat { t } \in \ [ 0 , 5 0 0 ] from \mathbf { I } _ { \mathrm { L R } } instead of relying on fixed timesteps. Table 4: Comparison of DM-SR on Realset80 with various number of steps.Despite being controllable, single-step application still produces high-quality results.*
*Table 5: Table 5: Comparison of DM-SR on Realset80 with various ground truth for the timesteps. Our final model utilize normalized LPIPS score ∈ [0, 500] for the ground turth for the timesteps.*
```
- formula_section_5_2:
```md
### 5.2 图像编码

图像编码器 E_θ 采用预训练VAE编码器，通过ControlNet风格设计将预测时间步 t̂ 的特征注入各中间层。编码器将 I_LR 映射到潜在表示 X_SR^t̂，旨在匹配对应噪声HR潜在 X_HR^t̂ 的分布。

```

## Candidate 8
- path: obsidian-vault/paper/ICLR_2026/P__Why_We_Need_New_Benchmarks_for_Local_Intrinsic_Dimension_Estimation.md
- title: Why We Need New Benchmarks for Local Intrinsic Dimension Estimation
- issues: known_formula_suspect_lidl, suspicious_short_formula:2, missing_figure_embed:13,24,3
- topic_row: Representation, Self-Supervision & Transfer, Representation Learning
- head_excerpt:
```md
---
title: Why We Need New Benchmarks for Local Intrinsic Dimension Estimation
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Why_We_Need_New_Benchmarks_for_Local_Intrinsic_Dimension_Estimation.pdf
aliases:
- LID-Benchmarks基准测试框架
acceptance: accepted
paradigm: 在简单流形上的高精度并不能跨域迁移；最先进的LID估计方法在针对性的压力测试下会暴露出明显的失败模式，例如对非均匀密度、流形曲率、边界、薄流形和邻近流形等场景表现不佳。
---

# Why We Need New Benchmarks for Local Intrinsic Dimension Estimation

> [!tip] 核心洞察
> 在简单流形上的高精度并不能跨域迁移；最先进的LID估计方法在针对性的压力测试下会暴露出明显的失败模式，例如对非均匀密度、流形曲率、边界、薄流形和邻近流形等场景表现不佳。

| 字段 | 内容 |
|------|------|
| 中文题名 | 为什么局部内在维度估计需要新的基准 |
| 英文题名 | Why We Need New Benchmarks for Local Intrinsic Dimension Estimation |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=ZEf03Uunvk) |
| Topic | Representation, Self-Supervision & Transfer, Representation Learning |
| Method | LID-Benchmarks基准测试框架 |
| Dataset | Gaussians (IDR), Spheres (IDR), Spaghetti (IDR), Uniform (IDR) |

> [!tip] 效果简介
> - Gaussians (IDR) 上，MAE 为 ESS: 0.07，对比 NB: 0.81, LIDL: 12.24, FLIPD: 3.08，变化 ESS最佳，NB次之，LIDL和FLIPD误差大。
> - Spheres (IDR) 上，MAE 为 ESS: 0.09，对比 NB: 1.83, LIDL: 12.90, FLIPD: 3.24，变化 ESS最佳，NB次之，LIDL和FLIPD误差大。
> - Spaghetti (IDR) 上，MAE 为 ESS: 0.03，对比 NB: 1.12, LIDL: 9.53, FLIPD: 3.54，变化 ESS最佳，NB次之，LIDL和FLIPD误差大。

## 概述

本文系统性地指出现有局部本征维度（Local Intrinsic Dimension, LID）评估方法存在的根本性缺陷：现有基准要么使用过于简单的合成数据（已知LID但无法反映真实流形复杂度），要么使用真实数据集（复杂度足够但LID真值未知），导致无法可靠评估算法性能。为此，作者提出了一套全新的基准测试框架（LID-Benchmarks），通过逆域表示（Inverse Domain Representation, IDR）、单调嵌入（Monotonic Embedding, ME）、环境空间扩展（Ambient Space Extension, ASE）、辅助维度注入（Auxiliary Dimension Injection, ADI）和流形合成（Manifold Synthesis, MS）五种方法，系统性地对四种主流LID估计算法（ESS、NB、LIDL、FLIPD）进行了压力测试。实验结果表明，在简单流形上的高精度并不能跨域迁移；最先进的LID估计方法在针对性的压力测试下会暴露出明显的失败模式，例如对非均匀密度、流形曲率、边界、薄流形和邻近流形等场景表现不佳。

## 背景与动机
```
- figure_lines:
```md
*Figure 1: Few samples from Gaussian (IDR) dataset.*
```
- table_lines:
```md
*Table 1: Summary of our experiments. Columns: LID-estimation aspects tested by our benchmarks; rows: neural-based algorithms (ESS as a classical benchmark). Performance of methods was classified following the legend – H: high, M: moderate, L: low, O: out-of-range (unassessable) (more can be found in Sec. B). Gray color marks cells where similar aspects in the method’s original paper were investigated; parentheses give that paper’s reported performance (assumed H if absent). We show that algorithms that passed original simple tests for many of aspects did worse on our benchmarks; many aspects – especially on real-world datasets (RWD) – remain untested and some only partly explored.*
*Table 2: LID estimations with MAE for the datasets with known dimensionality.*
*Table 3: LID estimations for the modified real-world datasets with unknown dimensionality.*
```
- formula_section_5_2:
```md
### 5.2 LIDL算法原理

LIDL（Tempczyk et al., 2022）基于Wiener过程下概率密度变化率来估计LID。对于小扩散时间t，对数密度与对数t呈线性关系，其斜率为：

$$d - D$$

其中d是流形本征维度，D是环境空间维度。通过估计该斜率，可以反推出LID。

```

## Candidate 9
- path: obsidian-vault/paper/ICLR_2026/P__3D-aware_Disentangled_Representation_for_Compositional_Reinforcement_Learning.md
- title: 3D-aware Disentangled Representation for Compositional Reinforcement Learning
- issues: suspicious_short_formula:3, missing_figure_embed:2,5
- topic_row: Reinforcement Learning, Planning & Agents, Deep RL
- head_excerpt:
```md
---
title: 3D-aware Disentangled Representation for Compositional Reinforcement Learning
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/3D-aware_Disentangled_Representation_for_Compositional_Reinforcement_Learning.pdf
aliases:
- 3D block-slot representation with block transformer policy
acceptance: accepted
paradigm: 通过块级（block-level）的属性分解和块级交叉注意力机制，策略可以基于静态属性（如颜色、形状）进行对象匹配，从而在未见过的属性组合和视角下实现稳定的组合泛化。
---

# 3D-aware Disentangled Representation for Compositional Reinforcement Learning

> [!tip] 核心洞察
> 通过块级（block-level）的属性分解和块级交叉注意力机制，策略可以基于静态属性（如颜色、形状）进行对象匹配，从而在未见过的属性组合和视角下实现稳定的组合泛化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向组合强化学习的3D感知解耦表示 |
| 英文题名 | 3D-aware Disentangled Representation for Compositional Reinforcement Learning |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=GE0IFoDx8a) |
| Topic | Reinforcement Learning, Planning & Agents, Deep RL |
| Method | 3D block-slot representation with block transformer policy |
| Dataset | Clevr3D, Clevr3D, Clevr3D, IsaacGym3D |

> [!tip] 效果简介
> - Clevr3D 上，PSNR 为 31.11，对比 31.57 (OSRT)，变化 -0.46。
> - Clevr3D 上，FG-ARI 为 0.942，对比 0.365 (OSRT)，变化 +0.577。
> - Clevr3D 上，D (Disentanglement) 为 0.867，对比 0.140 (OSRT)，变化 +0.727。

## 概述

本文提出了一种面向组合强化学习（Compositional Reinforcement Learning, GCRL）的3D感知解耦表示方法。核心贡献在于将对象中心表示（object-centric representation）中的每个对象槽（slot）进一步分解为多个属性块（block），并结合3D光场解码器，实现视角无关的3D位置与属性解耦。该方法在Clevr3D和IsaacGym3D数据集上，在对象分解（FG-ARI）、解耦质量（DCI）和组合泛化成功率等指标上显著优于OSRT、DLPv2、SNeRL等基线方法，尤其在未见过的视角和属性组合场景下展现出强大的泛化能力。

## 背景与动机
```
- figure_lines:
```md
*Figure 1: Overall structure of our method: Our proposed pipeline consists of two steps: representation learning and policy training. (a) Pre-training 3D block-slot encoder: The object slots are further decomposed into blocks of attributes. Then, the slot-mixer decoder mixes the object-centric representation to generate images at a query view. (b) Policy training with block transformer policy: We utilize the 3D block-slot encoder to extract a structured representation for the current observation and the goal image. The decomposed latent embedding serves as the input and the goal tokens, respectively, for our block transformer of the policy architecture.*
*Figure 4: Evaluation scenarios for compositional and out-of-distribution generalization: Composition generalization environments consist of objects with properties during training, but novel in their combinations. Out of such unseen combinations, we separately evaluate cases with objects of the same color when the factorization of attributes is unsuccessful. Out-of-distribution environments use objects with colors that were not present in the training set. Table 2: Performance of goal-conditioned RL: Our proposed 3D block-slot representation, combined with a block transformer (BT) policy, can effectively interpret goal conditions and exhibit superior performance in various scenarios. We com...*
```
- table_lines:
```md
*Table 1: 3D awareness with novel-view synthesis and decomposition performance: Our method outperforms OSRT across FG-ARI, disentanglement (D), completeness (C), and informativeness (I), while achieving comparable PSNR. The results indicate that our approach improves object decomposition and effectively disentangles information into latent vectors, while maintaining 3D-aware representation.*
*Table 3: Success rate of view-generalization: Our model, which leverages a pre-trained 3D blockslot representation and a block transformer (BT), effectively captures 3D object information in a viewpoint-agnostic manner and achieves state-of-the-art performance across diverse generalization settings. We evaluate generalization in goal-conditioned RL tasks under four viewpoints settings: ID Multi-View (in-distribution multi-view), ID Single-View (in-distribution single-view), OOD Multi-View (out-of-distribution multi-view), and OOD Single-View (out-of-distribution single-view). Results are computed over 400 randomly sampled goals per seed, with all reported metrics averaged over three random...*
*Table 4: Hyperparameters of OSRT and 3D block-slot attention used in our experiments.*
```
- formula_section_5_2:
```md
### 5.2 Slot Mixer加权聚合

根据查询光线特征x与槽矩阵Z的归一化点积相似度，计算加权平均：

$$\mathbf{w} = \mathrm{softmax}((W_k \mathbf{Z}^\top)^\top (W_q \mathbf{x})), \quad \bar{\mathbf{z}} = \mathbf{w}^\top \mathbf{Z}$$

```

## Candidate 10
- path: obsidian-vault/paper/ICLR_2026/P__3D_Scene_Prompting_for_Scene-Consistent_Camera-Controllable_Video_Generation.md
- title: 3D Scene Prompting for Scene-Consistent Camera-Controllable Video Generation
- issues: suspicious_short_formula:3, missing_figure_embed:2,3,5
- topic_row: Vision / Multimodal Applications, Image and Video Generation
- head_excerpt:
```md
---
title: 3D Scene Prompting for Scene-Consistent Camera-Controllable Video Generation
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/3D_Scene_Prompting_for_Scene-Consistent_Camera-Controllable_Video_Generation.pdf
aliases:
- 3DScenePrompt
acceptance: accepted
paradigm: 视频中的相邻性不仅是时间上的，也是空间上的。当相机重新访问相似视角时，生成帧可能与输入序列中很早的帧空间相邻。因此，模型应同时利用时间相邻帧（保证运动连续性）和空间相邻帧（保证场景一致性）。但空间条件必须仅提供静态场景结构，排除动态内容，因此需要构建仅包含静态几何的3D场景记忆。
---

# 3D Scene Prompting for Scene-Consistent Camera-Controllable Video Generation

> [!tip] 核心洞察
> 视频中的相邻性不仅是时间上的，也是空间上的。当相机重新访问相似视角时，生成帧可能与输入序列中很早的帧空间相邻。因此，模型应同时利用时间相邻帧（保证运动连续性）和空间相邻帧（保证场景一致性）。但空间条件必须仅提供静态场景结构，排除动态内容，因此需要构建仅包含静态几何的3D场景记忆。

| 字段 | 内容 |
|------|------|
| 中文题名 | 3D场景提示：面向场景一致且相机可控的视频生成 |
| 英文题名 | 3D Scene Prompting for Scene-Consistent Camera-Controllable Video Generation |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=3XxoBwMusJ) |
| Topic | Vision / Multimodal Applications, Image and Video Generation |
| Method | 3DScenePrompt |
| Dataset | RealEstate10K, RealEstate10K, RealEstate10K, RealEstate10K |

> [!tip] 效果简介
> - RealEstate10K 上，PSNR↑ 为 20.8932，对比 18.3044 (DFoT)，变化 +2.5888。
> - RealEstate10K 上，SSIM↑ 为 0.7171，对比 0.5960 (DFoT)，变化 +0.1211。
> - RealEstate10K 上，LPIPS↓ 为 0.2120，对比 0.3077 (DFoT)，变化 -0.0957。

## 概述

本文提出 **3DScenePrompt**，一个面向场景一致且相机可控的视频生成框架。该框架能够从任意长度的输入视频中生成下一个视频块，同时遵循用户指定的相机轨迹并保持与原始场景的一致性。核心创新在于**双时空滑动窗口策略**：模型同时利用时间相邻帧（保证运动连续性）和空间相邻帧（通过3D场景记忆检索与目标视角空间相邻的帧）作为条件。为了构建仅包含静态几何的3D场景记忆，论文引入了一个三阶段动态掩码流水线，显式分离静态场景与动态物体。该方法在RealEstate10K和DynPose-100K数据集上显著优于现有基线，特别是在空间一致性（PSNR提升2.59dB）和几何一致性（MEt3R误差降低77%）方面表现突出。该工作发表于ICLR 2026。

## 背景与动机
```
- figure_lines:
```md
*Figure 1: Teaser. Our framework generates the next video chunk that follows a user-specified camera trajectory while maintaining scene consistency. Our dual spatio-temporal conditioning jointly leverages the last few frames to ensure temporal continuity and the rendered point cloud to enforce spatial consistency.*
```
- table_lines:
```md
*Table 1: Evaluation of spatial and geometric consistency. We compare DFoT and our framework on the RealEstate10K (Zhou et al., 2018) and DynPose-100K (Rockwell et al., 2025) datasets. For spatial consistency, we evaluate PSNR, SSIM, and LPIPS on revisited camera trajectories, while for geometric consistency, we report the MEt3R (Asim et al., 2025) metric.*
*Table 2: Camera controllability evaluation.*
*Table 3: Evaluation of video generation quality. We assess the quality of generated videos using FVD and VBench++ scores. For FVD, lower values indicate higher video quality. For VBench++ scores, higher values indicate better performance. All VBench++ scores are normalized.*
```
- formula_section_5_2:
```md
### 5.2 双时空条件

输出视频条件于时间窗口（最后w帧）和空间检索帧（T帧）：

$$\mathbf{V}_{\mathrm{out}} = \mathcal{F}(\tilde{\mathbf{V}}_{\mathrm{in}}, T, \mathbf{C}), \quad \text{where} \quad \tilde{\mathbf{V}}_{\mathrm{in}} = \{\text{Temporal}(w)\} \cup \{\text{Spatial}(T)\}$$

```

## Candidate 11
- path: obsidian-vault/paper/ICLR_2026/P__A2Search_Ambiguity-Aware_Question_Answering_with_Reinforcement_Learning.md
- title: A$^2$Search: Ambiguity-Aware Question Answering with Reinforcement Learning
- issues: suspicious_short_formula:3, missing_figure_embed:2,6,7
- topic_row: Vision / Multimodal Applications, Language, Speech and Dialog
- head_excerpt:
```md
---
title: "A$^2$Search: Ambiguity-Aware Question Answering with Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A2Search_Ambiguity-Aware_Question_Answering_with_Reinforcement_Learning.pdf
aliases:
- A2SEARCH
acceptance: accepted
paradigm: 通过自动化的轨迹采样和证据验证发现替代答案，并采用答案级F1（AnsF1）奖励函数，使模型能够在一个rollout内感知歧义并输出多个有效答案，从而显著提升多答案场景下的性能。
---

# A$^2$Search: Ambiguity-Aware Question Answering with Reinforcement Learning

> [!tip] 核心洞察
> 通过自动化的轨迹采样和证据验证发现替代答案，并采用答案级F1（AnsF1）奖励函数，使模型能够在一个rollout内感知歧义并输出多个有效答案，从而显著提升多答案场景下的性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | A²Search：基于强化学习的歧义感知问答 |
| 英文题名 | A$^2$Search: Ambiguity-Aware Question Answering with Reinforcement Learning |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=3CPzUWIoNf) |
| Topic | Vision / Multimodal Applications, Language, Speech and Dialog |
| Method | A2SEARCH |
| Dataset | 多跳基准（MuSiQue, HotpotQA, 2Wiki, Bamboogle）, 多跳基准（MuSiQue, HotpotQA, 2Wiki, Bamboogle）, 多跳基准, 通用QA基准（NQ, TriviaQA, PopQA, AmbigQA） |

> [!tip] 效果简介
> - 多跳基准（MuSiQue, HotpotQA, 2Wiki, Bamboogle） 上，Macro-Avg AnsF1/Recall@1 (Exact Match) 为 48.4 (A2SEARCH-7B)，对比 46.2 (ReSearch-32B)，变化 +2.2。
> - 多跳基准（MuSiQue, HotpotQA, 2Wiki, Bamboogle） 上，Macro-Avg AnsF1/Recall@1 (LMJudge) 为 62.7 (A2SEARCH-7B)，对比 60.7 (ReSearch-32B)，变化 +2.0。
> - 多跳基准 上，Macro-Avg AnsF1/Recall@1 (Exact Match) 为 43.1 (A2SEARCH-3B)，对比 39.3 (ReSearch-7B)，变化 +3.8。

## 概述

本文提出 **A²Search**，一个无需人工标注的强化学习框架，旨在解决开放域问答系统中问题的固有歧义问题。核心思路是：通过自动流水线检测歧义问题并收集替代答案，然后使用基于答案级F1（AnsF1）奖励的组相对策略优化（GRPO）训练模型，使其能够在一个rollout内感知歧义并输出多个有效答案。

实验结果表明，A²Search-7B在四个多跳QA基准上的平均AnsF1@1达到48.4%，超越了包括更大规模模型ReSearch-32B（46.2%）在内的所有强基线。在LMJudge评估下，A²Search-7B的平均AnsF1@1达到62.7%，同样优于ReSearch-32B的60.7%。即使在3B参数规模下，A²Search-3B也取得了43.1%的AnsF1@1，显著优于ReSearch-7B的39.3%。
```
- figure_lines:
```md
*Figure 1: Rollout examples on an ambiguous question from MuSiQue. ReSearch yields different answers across rollouts, some diverging from the reference yet still evidence-supported, whereas A2SEARCH explicitly resolves ambiguity by retrieving multiple answers within a single rollout.*
```
- table_lines:
```md
*Table 1: Main results on four multi-hop QA benchmarks under the Exact Match metric. We report AnsF1/Recall@k with k rollouts. For AbgSearch and \mathbf { A } ^ { 2 } \mathbf { S } \mathbf { E } \mathbf { A } \mathbf { R } \mathbf { C } \mathbf { H } , only @1 is reported, reflecting their ability to produce multiple answers within a single rollout. For the remaining baselines, where each rollout generates only one answer and thus AnsF1@1 = Recall@1, we additionally include AnsF1/Recall@3 to evaluate their performance when more rollouts are available. The best result in each comparison group is shown in bold, and the second best is underlined.*
*Table 2: Main results with the Exact Match metric on four general QA benchmarks, using the same notations as Table 1. For AmbigQA, where questions may have multiple reference answers, AnsF1@1 and Recall@1 are not equivalent in this setting, and both are therefore reported.*
*Table 3: Ambiguity taxonomy and definitions. Examples of these types are listed in Table 12.*
```
- formula_section_5_2:
```md
### 5.2 GRPO目标函数（无KL惩罚）

A²Search采用GRPO算法，最大化带有归一化优势的裁剪替代目标，无KL惩罚项：

$$\mathcal{J}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^{G} \sim \pi_{\theta\mathrm{old}}(\cdot|x)} \frac{1}{G} \sum_{i=1}^{G} \left[ \min\left( \frac{\pi_\theta(y_i|x)}{\pi_{\theta\mathrm{old}}(y_i|x)} A_i, \mathrm{clip}\left( \frac{\pi_\theta(y_i|x)}{\pi_{\theta\mathrm{old}}(y_i|x)}, 1-\epsilon, 1+\epsilon \right) A_i \right) \right]$$

其中归一化优势为：

$$A_i = (r_i - \mathrm{mean}(\{r_j\}_{j=1}^{G})) / \mathrm{std}(\{r_j\}_{j=1}^{G})$$

```

## Candidate 12
- path: obsidian-vault/paper/ICLR_2026/P__ARES_Multimodal_Adaptive_Reasoning_via_Difficulty-Aware_Token-Level_Entropy_Shaping.md
- title: ARES: Multimodal Adaptive Reasoning via Difficulty-Aware Token-Level Entropy Shaping
- issues: suspicious_short_formula:6, missing_figure_embed:10,2,3
- topic_row: Vision / Multimodal Applications, Vision Models & Multimodal
- head_excerpt:
```md
---
title: "ARES: Multimodal Adaptive Reasoning via Difficulty-Aware Token-Level Entropy Shaping"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ARES_Multimodal_Adaptive_Reasoning_via_Difficulty-Aware_Token-Level_Entropy_Shaping.pdf
aliases:
- ARES (multimodal Adaptive Reasoning via difficulty-aware token-level Entropy reward Shaping)
acceptance: accepted
paradigm: 通过将令牌级熵聚合为滑动窗口统计量（窗口熵），可以可靠地识别推理关键时刻；减少HWE令牌对简单问题有益，增加HWE令牌对解决困难问题至关重要。基于此，ARES通过自适应冷启动和自适应熵策略优化（AEPO）动态分配推理努力。
---

# ARES: Multimodal Adaptive Reasoning via Difficulty-Aware Token-Level Entropy Shaping

> [!tip] 核心洞察
> 通过将令牌级熵聚合为滑动窗口统计量（窗口熵），可以可靠地识别推理关键时刻；减少HWE令牌对简单问题有益，增加HWE令牌对解决困难问题至关重要。基于此，ARES通过自适应冷启动和自适应熵策略优化（AEPO）动态分配推理努力。

| 字段 | 内容 |
|------|------|
| 中文题名 | ARES：基于难度感知的令牌级熵塑形的多模态自适应推理 |
| 英文题名 | ARES: Multimodal Adaptive Reasoning via Difficulty-Aware Token-Level Entropy Shaping |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=2g945Ngc7l) |
| Topic | Vision / Multimodal Applications, Vision Models & Multimodal |
| Method | ARES (multimodal Adaptive Reasoning via difficulty-aware token-level Entropy reward Shaping) |
| Dataset | MathVision, MMMU-Pro, AIME25, MathVerse-V |

> [!tip] 效果简介
> - MathVision 上，Accuracy 为 51.9，对比 32.9 (best open-source)，变化 +19.0。
> - MMMU-Pro 上，Accuracy 为 54.8，对比 43.3 (best open-source)，变化 +11.5。
> - AIME25 上，Accuracy 为 61.7，对比 3.3 (most 7B baselines)，变化 +58.4。

## 概述

ARES（multimodal Adaptive Reasoning via difficulty-aware token-level Entropy reward Shaping）是一种针对多模态大推理模型（MLRM）的两阶段训练框架，旨在解决现有模型在推理过程中“简单问题过度思考、困难问题探索不足”的核心矛盾。该方法通过引入**窗口熵**（window entropy）作为推理关键时刻的可靠检测信号，结合自适应冷启动（Adaptive Cold-Start, AdaCS）和自适应熵策略优化（Adaptive Entropy Policy Optimization, AEPO）两个阶段，实现基于问题难度的动态推理努力分配。实验结果表明，ARES-7B在MathVision上超过最佳开源模型+19.0，在MMMU-Pro上超过+11.5，在AIME25上达到61.7（大多数7B基线低于3.3）。

## 背景与动机
```
- figure_lines:
```md
*Figure 1: (a) Difficulty modulates the exploratory effort along the reasoning path*
```
- table_lines:
```md
*Table 1: Performance comparison of various MLLMs on diverse multimodal reasoning benchmarks. Within each model group (3B and 7B), the best results are highlighted in bold, and the second-best are underlined. Scores in italics indicate that they are not reported in the original work and are obtained using the VLMEvalKit (Duan et al., 2025) for evaluation. MathVerse-V, DynaMath-W and WeMath-S denotes the vision-only, worst, and strict settings, respectively.*
*Table 2: Accuracy and response length comparison across multimodal and textual benchmarks. We report both accuracy (Acc) and average response length (Len) for five model variants (ARES-CS-Vanilla, ARES-CS-7B, ARES-CS-Vanilla-GRPO, ARES-CS-Vanilla-RL, and ARES-RL-7B) on six benchmarks. Visualization of these results is provided in Figure 8 (accuracy) and Figure 9 (response length) in Appendix.*
*Table 3: Ablation study of Dynamic KL Loss and Entropy Reward. Building upon our Cold Start stage. Best results per column are bold and second-best are underlined.*
```
- formula_section_5_2:
```md
### 5.2 在线难度分桶

基于pass@8准确率将问题分为三个难度桶：
$$d(x) = \begin{cases} \mathsf{easy}, & \mathsf{pass@8}(x) \ge 6, \\ \mathsf{medium}, & 3 \le \mathsf{pass@8}(x) < 6, \\ \mathsf{hard}, & \mathsf{pass@8}(x) \le 2 \end{cases}$$

其中 $\mathsf{pass@8}(x) = \frac{1}{8} \sum_{k=1}^{8} \mathbf{1}\{\mathrm{correct}(y^{(k)}, x)\}$。

```

## Candidate 13
- path: obsidian-vault/paper/ICLR_2026/P__ARFlow_Auto-regressive_Optical_Flow_Estimation_for_Arbitrary-Length_Videos_via_Progressive_Next-Frame_Forecasting.md
- title: ARFlow: Auto-regressive Optical Flow Estimation for Arbitrary-Length Videos via Progressive Next-Frame Forecasting
- issues: suspicious_short_formula:3, missing_figure_embed:3
- topic_row: Vision / Multimodal Applications, Vision Models & Multimodal
- head_excerpt:
```md
---
title: "ARFlow: Auto-regressive Optical Flow Estimation for Arbitrary-Length Videos via Progressive Next-Frame Forecasting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ARFlow_Auto-regressive_Optical_Flow_Estimation_for_Arbitrary-Length_Videos_via_Progressive_Next-Frame_Forecasting.pdf
aliases:
- "ARFlow: Auto-regressive Optical Flow Estimation for Arbitrary-Length Videos via Progressive Next-Frame Forecasting"
acceptance: accepted
paradigm: 将光流估计建模为自回归的下一帧预测问题，利用历史光流序列的时序一致性，通过多步长时间建模同时捕获长程和短程运动，从而突破固定分组限制，实现线性时间复杂度和恒定空间复杂度的可扩展多帧光流估计。
---

# ARFlow: Auto-regressive Optical Flow Estimation for Arbitrary-Length Videos via Progressive Next-Frame Forecasting

> [!tip] 核心洞察
> 将光流估计建模为自回归的下一帧预测问题，利用历史光流序列的时序一致性，通过多步长时间建模同时捕获长程和短程运动，从而突破固定分组限制，实现线性时间复杂度和恒定空间复杂度的可扩展多帧光流估计。

| 字段 | 内容 |
|------|------|
| 中文题名 | ARFlow：通过渐进式下一帧预测实现任意长度视频的自回归光流估计 |
| 英文题名 | ARFlow: Auto-regressive Optical Flow Estimation for Arbitrary-Length Videos via Progressive Next-Frame Forecasting |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=iJ7cyttpVj) |
| Topic | Vision / Multimodal Applications, Vision Models & Multimodal |
| Method | ARFlow |
| Dataset | MPI-Sintel (Clean), MPI-Sintel (Final), KITTI-2015, Spring |

> [!tip] 效果简介
> - MPI-Sintel (Clean) 上，EPE (All) 为 0.96，对比 1.03 (GMFlow+)，变化 -0.07。
> - MPI-Sintel (Final) 上，EPE (All) 为 1.78，对比 1.91 (MEMFOF)，变化 -0.13。
> - KITTI-2015 上，Fl (All) 为 2.85，对比 2.94 (MEMFOF)，变化 -0.09。

## 概述

ARFlow（Auto-regressive Optical Flow Estimation for Arbitrary-Length Videos via Progressive Next-Frame Forecasting）提出了一种全新的自回归多帧光流估计范式。与现有基于固定分组（group-wise）的多帧光流方法不同，ARFlow将光流估计建模为逐帧的自回归下一帧预测问题，通过记忆库存储历史光流序列，并利用多步长（stride 1, 2, 4）时间Transformer预测下一帧初始光流，再通过GRU迭代细化，实现任意长度视频的恒定内存（约2.1GB）处理。该方法在KITTI-2015和Spring官方基准上排名第一，在MPI-Sintel (Final)基准上排名第二（所有开源方法中），并可作为通用插件提升现有光流方法的性能。

## 背景与动机
```
- figure_lines:
```md
*Figure 1: (B) Sequence-to-sequence multi-frame pipeline*
```
- table_lines:
```md
*Table 1: Benchmark results on MPI-Sintel and KITTI-15. We report endpoint-error (EPE) on Sintel (Butler et al., 2012) and Fl on KITTI-15 (Geiger et al., 2013).*
*Table 2: Benchmark results on Spring. Runtime and maximum GPU memory usage were evaluated using an NVIDIA RTX 3090 GPU. Best results are respectively highlighted as first , second . OOM indicates out of memory. ∗ indicates scene flow methods.*
*Table 3: Zero-shot Generalization. ARFlow achieves the best cross-dataset generalization on KITTI-15 (train).*
```
- formula_section_5_2:
```md
### 5.2 GRU迭代细化

从当前图像对提取上下文特征和GRU初始隐藏状态，并预测初始光流：

$$c, h^0 = \mathrm{ContextNetwork}(I_t, I_{t+1}), \quad f^0 = \mathrm{FlowHead}(h^0)$$

对于第一帧对，使用上下文网络预测的流；否则使用AFI模块预测的初始流：

$$f_{t,t+1}^0 = \begin{cases} f^0, & \text{when } t=0; \\ f_{t,t+1}, & \text{otherwise} \end{cases}$$

第k次迭代的输出流为上一次迭代流加上残差流：

$$f_{t,t+1}^k = f_{t,t+1}^{k-1} + \Delta f_{t,t+1}^k$$

```

## Candidate 14
- path: obsidian-vault/paper/ICLR_2026/P__A_Balanced_Neuro-Symbolic_Approach_for_Commonsense_Abductive_Logic.md
- title: A Balanced Neuro-Symbolic Approach for Commonsense Abductive Logic
- issues: suspicious_short_formula:2, missing_figure_embed:2,3,4
- topic_row: Vision / Multimodal Applications, Language, Speech and Dialog
- head_excerpt:
```md
---
title: A Balanced Neuro-Symbolic Approach for Commonsense Abductive Logic
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Balanced_Neuro-Symbolic_Approach_for_Commonsense_Abductive_Logic.pdf
aliases:
- ARGOS (Abductive Reasoning with Generalization Over Symbolics)
acceptance: accepted
paradigm: 通过将LLM的常识知识与逻辑求解器的符号推理能力相结合，并利用骨干图（backbone）高效引导搜索，可以在不限制常识命题形式和内容的前提下，实现有效的溯因推理。
---

# A Balanced Neuro-Symbolic Approach for Commonsense Abductive Logic

> [!tip] 核心洞察
> 通过将LLM的常识知识与逻辑求解器的符号推理能力相结合，并利用骨干图（backbone）高效引导搜索，可以在不限制常识命题形式和内容的前提下，实现有效的溯因推理。

| 字段 | 内容 |
|------|------|
| 中文题名 | 一种平衡的神经符号方法用于常识溯因逻辑 |
| 英文题名 | A Balanced Neuro-Symbolic Approach for Commonsense Abductive Logic |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=RCsBoUr72G) |
| Topic | Vision / Multimodal Applications, Language, Speech and Dialog |
| Method | ARGOS (Abductive Reasoning with Generalization Over Symbolics) |
| Dataset | FOLIO, CLUTRR, QUAIL, ProntoQA |

> [!tip] 效果简介
> - FOLIO 上，准确率 为 81%，对比 71% (SC20)，变化 +10%。
> - CLUTRR 上，准确率 为 80%，对比 69% (SC20)，变化 +11%。
> - QUAIL 上，准确率 为 82%，对比 70% (SC20)，变化 +12%。

## 概述

本文提出了一种名为 **ARGOS (Abductive Reasoning with Generalization Over Symbolics)** 的神经符号方法，旨在解决现有系统无法处理的**常识溯因推理**问题。核心挑战在于：传统神经符号系统仅能进行纯演绎推理，无法补全问题中未明确陈述但人类常识可补全的缺失信息。ARGOS 通过将大语言模型（LLM）的常识知识与逻辑求解器的符号推理能力相结合，并利用 SAT 问题的**骨干图（backbone）**高效引导搜索，实现了有效的溯因推理。在 FOLIO、CLUTRR、QUAIL 等多个基准上，ARGOS 显著优于现有技术，例如在 FOLIO 数据集上使用 Llama 8B 模型达到 81% 的准确率，相比 Self-Consistency 的 71% 提升了 10 个百分点。

## 背景与动机
```
- figure_lines:
```md
*Figure 1: An example from a children’s comprehension exercise booklet 1. Left: the problem phrased in human language. Right: the same problem translated to first-order-logic.*
```
- table_lines:
```md
*Table 1: Binary classification accuracy (True/False) of all methods on the datasets, using the chosen language models. Bolded text indicates that the method has the best performance, and that its performance is better than the next-best-performing method in a statistically significant way (p-value < 0.005 according to a Wilcoxon pair-wise rank test). Small-font numbers to the right indicate the bounds of the 95% confidence interval, derived via a bootstrap approach. RQ1: How useful are the scoring and backbone-tracking elements? In Table 2, we test the importance of two elements of ARGOS: (i) score thresholding and (ii) backbone computation. The ablation of each element in isolation results...*
*Table 3: Average number of COT calls required by each method.*
*Table 4: Ablating the SC-solver on ARGOS. ARGOS-Symbolic denotes the ablated version of ARGOS.*
```
- formula_section_5_2:
```md
### 5.2 文字评分函数

为了优先选择最相关的文字，定义了文字评分函数：

$$\text{scoreB}(L) = \# \{ L' \in B \mid L' \text{ has an entity in common with } L \}$$

该函数计算骨干图中与文字 $L$ 共享实体的文字数量。

```

## Candidate 15
- path: obsidian-vault/paper/ICLR_2026/P__A_Biologically_Plausible_Dense_Associative_Memory_with_Exponential_Capacity.md
- title: A Biologically Plausible Dense Associative Memory with Exponential Capacity
- issues: suspicious_short_formula:3, missing_figure_embed:10,11,2
- topic_row: Vision / Multimodal Applications, Neuroscience, Cognitive Science
- head_excerpt:
```md
---
title: A Biologically Plausible Dense Associative Memory with Exponential Capacity
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Biologically_Plausible_Dense_Associative_Memory_with_Exponential_Capacity.pdf
aliases:
- Threshold-based Dense Associative Memory (TDAM)
acceptance: accepted
paradigm: "通过使用阈值激活函数，隐藏神经元可以编码多个记忆共享的基本组件，使得所有 $2^{N_h}$ 种隐藏层二元状态都成为稳定不动点，从而在 $N_v \\gg N_h$ 条件下实现指数级存储容量。"
---

# A Biologically Plausible Dense Associative Memory with Exponential Capacity

> [!tip] 核心洞察
> 通过使用阈值激活函数，隐藏神经元可以编码多个记忆共享的基本组件，使得所有 $2^{N_h}$ 种隐藏层二元状态都成为稳定不动点，从而在 $N_v \gg N_h$ 条件下实现指数级存储容量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 具有指数容量的生物学合理稠密联想记忆 |
| 英文题名 | A Biologically Plausible Dense Associative Memory with Exponential Capacity |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=mRZOayQL1i) |
| Topic | Vision / Multimodal Applications, Neuroscience, Cognitive Science |
| Method | Threshold-based Dense Associative Memory (TDAM) |
| Dataset | MNIST, MNIST, MNIST, MNIST |

> [!tip] 效果简介
> - MNIST 上，存储记忆数 为 60,000，对比 50 (Krotov-Hopfield 模型)，变化 +59,950。
> - MNIST 上，召回准确率（可见层） 为 98%，对比 90% (Model B)，变化 +8%。
> - MNIST 上，分类准确率（可见层） 为 98%，对比 99% (原始图像)，变化 -1%。

## 概述

本文提出了一种基于阈值激活函数的密集联想记忆模型（Threshold-based Dense Associative Memory, TDAM），在保持生物可解释性的同时，实现了与隐藏神经元数量呈指数关系的存储容量。该模型发表于 ICLR 2026，核心创新在于将隐藏神经元的激活函数从幂律函数、softmax 或球面归一化等非线性函数替换为简单的 Heaviside 阶跃函数，从而允许分布式表示。理论分析表明，当可见神经元数量远大于隐藏神经元数量（$N_v \gg N_h$）时，有效权重矩阵 $J_{\mu\nu}$ 趋近于单位矩阵，使得所有 $2^{N_h}$ 种隐藏层二元状态都成为稳定不动点。在 MNIST 数据集上，仅用 50 个隐藏神经元即可存储 60,000 张图像，召回准确率达 98%；在 CIFAR-10 数据集上，用 500 个隐藏神经元存储 50,000 张图像，学习到 49,982 个唯一极小值。

## 背景与动机
```
- figure_lines:
```md
*Figure 1: a*
*Figure 1: b Figure 1: Capacity versus the number of hidden units, N _ { h } , with N _ { v } = 1 0 0 N _ { h } and \tau _ { v } = 2 0 \tau _ { h } . (a) Capacity for different thresholds, θ. The highest storage capacity is achieved when the threshold is set to its optimal theoretical value , \theta = 0 . 5 . (b) The effect of noise in the visible layer ( \epsilon _ { i } ^ { v } in Eq. (12a)), shown for different noise variances, demonstrates the large basin of attraction of the fixed points.*
```
- table_lines:
```md
*Table 2: Architecture and Parameters of the CNN Classifier*
*Table 3: Architecture and Parameters of the MLP Classifier*
*Table 4: And from a biological perspective, the nonlinearity used in Model A is not plausible, because the power-law activation causes hidden neuron activity to reach unrealistically high values during recall. Models B and C also rely on non-local activation functions, which would require additional circuit mechanisms to implement. In contrast, our model maintains bounded activity, and the nonlinearity is fully local. Table 4: Nonlinearities used in the Dense Associative Memory models from Krotov and Hopfield (2021) and in our model, and a comparison of their recall performance. Recall performance is the percentage of recalled digits that are classified correctly.*
```
- formula_section_5_2:
```md
### 5.2 稳定性保证

系统的雅可比矩阵为下三角结构（Appendix A.2）：
$$\mathbf{A} = \begin{bmatrix} -\mathbf{I}_{N_v} & \mathbf{0} \\ \mathbf{A}_{hv} & -\mathbf{I}_{N_h} \end{bmatrix}$$

所有对角元均为 -1，且由于 Heaviside 阶跃函数的导数几乎处处为零，非对角块 $\mathbf{A}_{vh} = 0$，因此所有不动点都是稳定的。

```

## Candidate 16
- path: obsidian-vault/paper/ICLR_2026/P__A_Fano-Style_Accuracy_Upper_Bound_for_LLM_Single-Pass_Reasoning_in_Multi-Hop_QA.md
- title: A Fano-Style Accuracy Upper Bound for LLM Single-Pass Reasoning in Multi-Hop QA
- issues: suspicious_short_formula:1, missing_figure_embed:2,3,4
- topic_row: Vision / Multimodal Applications, Language, Speech and Dialog
- head_excerpt:
```md
---
title: A Fano-Style Accuracy Upper Bound for LLM Single-Pass Reasoning in Multi-Hop QA
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Fano-Style_Accuracy_Upper_Bound_for_LLM_Single-Pass_Reasoning_in_Multi-Hop_QA.pdf
aliases:
- InfoQA
acceptance: accepted
paradigm: 单次推理范式存在不可逾越的准确率上界：当β > C+1时，准确率上限为(C+1)/β，呈双曲衰减。多跳问答的链式结构同时引发容量危机（β超线性增长）和误差累积危机（小误差沿链放大），因此必须采用容量感知的多轮调用范式来规避这一理论极限。
---

# A Fano-Style Accuracy Upper Bound for LLM Single-Pass Reasoning in Multi-Hop QA

> [!tip] 核心洞察
> 单次推理范式存在不可逾越的准确率上界：当β > C+1时，准确率上限为(C+1)/β，呈双曲衰减。多跳问答的链式结构同时引发容量危机（β超线性增长）和误差累积危机（小误差沿链放大），因此必须采用容量感知的多轮调用范式来规避这一理论极限。

| 字段 | 内容 |
|------|------|
| 中文题名 | LLM单次推理在多跳问答中的Fano式准确率上界 |
| 英文题名 | A Fano-Style Accuracy Upper Bound for LLM Single-Pass Reasoning in Multi-Hop QA |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=dPAcHrG4rl) |
| Topic | Vision / Multimodal Applications, Language, Speech and Dialog |
| Method | InfoQA |
| Dataset | Synthetic Multi-Hop QA Benchmark, Synthetic Multi-Hop QA Benchmark, Synthetic Multi-Hop QA Benchmark, Synthetic Multi-Hop QA Benchmark (Qwen3-8B) |

> [!tip] 效果简介
> - Synthetic Multi-Hop QA Benchmark 上，Average F1 (2-4 hop) 为 0.86，对比 0.75 (S-C), 0.73 (CoT)，变化 +0.11 vs S-C, +0.13 vs CoT。
> - Synthetic Multi-Hop QA Benchmark 上，Average F1 (4-hop) 为 0.80，对比 0.61 (S-C), 0.57 (CoT)，变化 +0.19 vs S-C, +0.23 vs CoT。
> - Synthetic Multi-Hop QA Benchmark 上，Average F1 at 8k context (2-4 hop) 为 0.76，对比 0.10 (Direct), 0.30 (ReAct)，变化 +0.66 vs Direct, +0.46 vs ReAct。

本文发表于 ICLR 2026，首次从信息论角度为 LLM 单次推理（single-pass reasoning）在多跳问答（Multi-Hop QA）中的准确率建立了严格的数学上界。核心贡献包括：(1) 基于 Fano 不等式推导出单次推理的准确率上界定理（Theorem 1），揭示了当任务信息需求 β 超过模型输出容量 C 时准确率必然崩溃的“准确率悬崖”（Accuracy Cliff）现象；(2) 提出信息需求模型 β(h, L) = β₀ + αLγ^(h-1)，刻画了跳数 h 和上下文长度 L 对信息需求的超线性放大效应；(3) 提出容量感知的多轮调用框架 InfoQA，通过任务分解、显式工作流和迭代查询收缩规避理论极限。在合成多跳 QA 基准上，InfoQA 在 Qwen3-14B 上 2-4 跳平均 F1 达 0.86，显著超越单次推理基线（S-C 0.75, 
```
- figure_lines:
```md
*Figure 1: Comparison of single-pass and multi-call reasoning paradigms. Single-pass reasoning is constrained by the limited output capacity of LLMs, making it difficult to solve long-context and multi-hop problems. Multi-call reasoning mitigates this by decomposing tasks into sequentially dependent sub-steps, ensuring high per-step accuracy and a reliable reasoning chain.*
```
- table_lines:
```md
*Table 1: Statistics of our synthetic multi-hop QA benchmark.*
*Table 2: Average F1 scores of Qwen3-14B across different reasoning depths and context lengths. We compare InfoQA with single-pass baselines: Chain-of-Thought (CoT), Self-Refine (S-R), Self-Consistency (S-C), ReAct, Plan-and-Solve (P&S), Self-Ask (S-A), and InfoQA with ablation: w/o Capacity-Aware Task Decomposition (D.) and w/o Pruning Past Reasoning Trace (P.).*
*Table 3: Fitted parameters of the plug-in accuracy bound (MAE minimization) of Qwen3-14B. Larger C indicates higher effective single-pass capacity; smaller \gamma indicates weaker hop inflation.*
```

## Candidate 17
- path: obsidian-vault/paper/ICLR_2026/P__A_Probabilistic_Hard_Concept_Bottleneck_for_Steerable_Generative_Models.md
- title: A Probabilistic Hard Concept Bottleneck for Steerable Generative Models
- issues: suspicious_short_formula:2, missing_figure_embed:2,3,7
- topic_row: Generative Models & Diffusion, Generative Models and Autoencoders
- head_excerpt:
```md
---
title: A Probabilistic Hard Concept Bottleneck for Steerable Generative Models
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Probabilistic_Hard_Concept_Bottleneck_for_Steerable_Generative_Models.pdf
aliases:
- Variational Hard Concept Bottleneck (VHCB)
acceptance: accepted
paradigm: 通过将概念表示为硬二进制变量（而非软概率），并利用纠错码（ECC）和重叠平滑变换实现稳定训练，VHCB在无需显式干预损失的情况下缓解了概念泄漏，同时其概率公式支持从指定概念配置直接生成。
---

# A Probabilistic Hard Concept Bottleneck for Steerable Generative Models

> [!tip] 核心洞察
> 通过将概念表示为硬二进制变量（而非软概率），并利用纠错码（ECC）和重叠平滑变换实现稳定训练，VHCB在无需显式干预损失的情况下缓解了概念泄漏，同时其概率公式支持从指定概念配置直接生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向可操控生成模型的概率化硬概念瓶颈 |
| 英文题名 | A Probabilistic Hard Concept Bottleneck for Steerable Generative Models |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=Kcb6WufAco) |
| Topic | Generative Models & Diffusion, Generative Models and Autoencoders |
| Method | Variational Hard Concept Bottleneck (VHCB) |
| Dataset | CelebA-HQ (StyleGAN2), CelebA-HQ (StyleGAN2), CelebA-HQ (StyleGAN2), CelebA-HQ (StyleGAN2) |

> [!tip] 效果简介
> - CelebA-HQ (StyleGAN2) 上，概念推理准确率 (Acc) 为 0.855，对比 0.857，变化 -0.002。
> - CelebA-HQ (StyleGAN2) 上，概念推理余弦相似度 (Cosine Sim) 为 0.804，对比 0.763，变化 +0.041。
> - CelebA-HQ (StyleGAN2) 上，解耦准确率 (Disent. Acc) 为 0.927，对比 0.901，变化 +0.026。

## 概述

本文提出了一种**变分硬概念瓶颈（Variational Hard Concept Bottleneck, VHCB）**层，用于增强生成模型的可操控性。现有概念瓶颈生成模型（CBGM）使用确定性映射将模型内部表示映射到软概念（soft concepts），导致概念泄漏（concept leakage）并限制可操控性；同时，确定性方法无法对概念空间建模生成过程，因此只能对已有输入进行概念修改，无法从指定概念配置直接生成。VHCB层基于二进制VAE（Coded DVAE）构建，将概率估计的二进制潜变量映射到硬概念（hard concepts），并引入无监督侧通道s（二进制，5比特）以处理概念不完备性。通过将概念表示为硬二进制变量（而非软概率），并利用纠错码（ECC）和重叠平滑变换实现稳定训练，VHCB在无需显式干预损失的情况下缓解了概念泄漏，同时其概率公式支持从指定概念配置直接生成。实验表明，VHCB在概念推理、c与s的解耦、单概念干预、汉明距离干预以及生成质量（FID）上全面优于CB-AE基线。

## 背景与动机
```
- figure_lines:
```md
*Figure 1: Block diagram of (a) the general architecture of CBGMs, and (b) the VHCB layer. Note that the Error-Correcting Code (ECC) in the VHCB layer is a deterministic transformation that enables effective inference.*
```
- table_lines:
```md
*Table 1: Concept inference and disentanglement between c and s. Evaluation on 1k random samples generated by a StyleGAN2 pretrained on CelebA-HQ. Figure 3: Qualitative evaluation of the disentanglement between s and c with the VHCB layer and StyleGAN2 models pretrained on CelebA-HQ.*
*Table 2: Steerable Generation. Evaluation of generation from specific concept configurations using a StyleGAN2 pretrained on CelebA-HQ. Random samples concept sets uniformly at random, while Patterns samples them according to their empirical frequency in the training data.*
*Table 3: Test-time interventions. Evaluation of single-concept activation (i → a), deactivation (a → i), and interventions guided by training concept patterns (minimum Hamming distance) using a StyleGAN2 pretrained on CelebA-HQ.*
```
- formula_section_5_2:
```md
### 5.2 纠错码（ECC）保护

c和s分别使用独立的ECC保护，增加汉明距离并实现错误纠正：
- c → v_c，v_c ∈ {0,1}^{K'}，K' > K
- s → v_s，v_s ∈ {0,1}^{L'}，L' > L

推理时通过软多数投票（soft majority voting）纠正编码器错误。

```

## Candidate 18
- path: obsidian-vault/paper/ICLR_2026/P__A_Reward-Free_Viewpoint_on_Multi-Objective_Reinforcement_Learning.md
- title: A Reward-Free Viewpoint on Multi-Objective Reinforcement Learning
- issues: suspicious_short_formula:3, missing_figure_embed:16,2,3
- topic_row: Reinforcement Learning, Planning & Agents, Deep RL
- head_excerpt:
```md
---
title: A Reward-Free Viewpoint on Multi-Objective Reinforcement Learning
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Reward-Free_Viewpoint_on_Multi-Objective_Reinforcement_Learning.pdf
aliases:
- MORL-FB
acceptance: accepted
paradigm: MORL可视为RFRL的特例，利用RFRL学习任意奖励函数最优策略的能力，为MORL提供结构化辅助任务，从而提升样本效率和泛化性能。
---

# A Reward-Free Viewpoint on Multi-Objective Reinforcement Learning

> [!tip] 核心洞察
> MORL可视为RFRL的特例，利用RFRL学习任意奖励函数最优策略的能力，为MORL提供结构化辅助任务，从而提升样本效率和泛化性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 多目标强化学习的无奖励视角 |
| 英文题名 | A Reward-Free Viewpoint on Multi-Objective Reinforcement Learning |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=IwiwmY3Mzz) |
| Topic | Reinforcement Learning, Planning & Agents, Deep RL |
| Method | MORL-FB |
| Dataset | HalfCheetah2d, HalfCheetah2d, Walker2d, Walker2d |

> [!tip] 效果简介
> - HalfCheetah2d 上，UT (×10^3) 为 7.69 ± 0.08，对比 6.85 ± 0.01 (Q-Pensieve)，变化 +0.84。
> - HalfCheetah2d 上，HV (×10^8) 为 1.24 ± 0.00，对比 1.13 ± 0.00 (Q-Pensieve)，变化 +0.11。
> - Walker2d 上，UT (×10^3) 为 2.36 ± 0.01，对比 1.92 ± 0.18 (GPI-LS)，变化 +0.44。

本文提出 **MORL-FB**，一种将无奖励强化学习（Reward-Free RL, RFRL）的 Forward-Backward (FB) 表示方法引入多目标强化学习（Multi-Objective RL, MORL）的新框架。核心洞察在于：MORL 可视为 RFRL 的特例，利用 RFRL 学习任意奖励函数最优策略的能力，为 MORL 提供结构化辅助任务，从而提升样本效率和泛化性能。MORL-FB 在 MO-Gymnasium 连续控制任务中，在 Utility (UT) 和 Hypervolume (HV) 指标上显著优于所有基线方法，并实现了零样本跨目标迁移。

# 2. 背景与动机

传统 MORL 方法在训练时仅针对线性标量化奖励函数学习策略，限制了知识共享和泛化能力，尤其是在偏好样本有限的情况下表现不佳。RFRL 的目标是学习一个能够适应任意奖励函数的最优策略集，而 MORL 的奖励函数被限制为预定义奖励向量的加权和。因此，MORL 可视为 RFRL 的一个特例（Alegre et al., 2022）。
```
- figure_lines:
```md
*Figure 1: A motivating experiment on Deep Sea Treasure. (a)(b) Training performance (UT and HV defined in the sequel) of MORL-FB under different batch sizes for \hat { z } _ { \lambda } . (c) KDE contour of return vector distributions of \pi ( \cdot , z ) induced by \hat { z } _ { \lambda } (with various batch sizes b) and \hat { z } \sim \mathcal { N } ( 0 , \mathbb { T } ^ { d _ { z } } ) This shows that \hat { z } _ { \lambda } corresponds to learning for more diverse and relevant behavior in MORL than z _ { \lambda } and the z sampling strategy of the original FB. The detailed configuration is provided in Appendix C.*
```
- table_lines:
```md
*Table 1: Hyperparameters of PGMORL.*
*Table 2: PPO hyperparameters used in PGMORL.*
*Table 3: Augmentation strength of CAPQL.*
```

## Candidate 19
- path: obsidian-vault/paper/ICLR_2026/P__A_Statistical_Benchmark_for_Diffusion-Posterior-Sampling_Algorithms.md
- title: A Statistical Benchmark for Diffusion-Posterior-Sampling Algorithms
- issues: suspicious_short_formula:4, missing_figure_embed:3,4,6
- topic_row: Representation, Self-Supervision & Transfer, Representation Learning
- head_excerpt:
```md
---
title: A Statistical Benchmark for Diffusion-Posterior-Sampling Algorithms
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Statistical_Benchmark_for_Diffusion-Posterior-Sampling_Algorithms.pdf
aliases:
- 基于Lévy过程的统计基准框架（Statistical Benchmark for DPS Algorithms）
acceptance: accepted
paradigm: 通过将Gibbs方法嵌入反向扩散过程，可以任意精度地蒙特卡洛估计去噪后验的期望和协方差等对象，从而将DPS算法本身的误差与学习组件的近似误差分离开来，实现算法误差的隔离与量化。
---

# A Statistical Benchmark for Diffusion-Posterior-Sampling Algorithms

> [!tip] 核心洞察
> 通过将Gibbs方法嵌入反向扩散过程，可以任意精度地蒙特卡洛估计去噪后验的期望和协方差等对象，从而将DPS算法本身的误差与学习组件的近似误差分离开来，实现算法误差的隔离与量化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 扩散后验采样算法的统计基准 |
| 英文题名 | A Statistical Benchmark for Diffusion-Posterior-Sampling Algorithms |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=zDI2G8t0of) |
| Topic | Representation, Self-Supervision & Transfer, Representation Learning |
| Method | 基于Lévy过程的统计基准框架（Statistical Benchmark for DPS Algorithms） |
| Dataset | Denoising, Deconvolution, Imputation, Partial Fourier |

> [!tip] 效果简介
> - Denoising 上，MMSE optimality gap (dB) 为 DiffPIR (best DPS)，对比 ℓ2 / ℓ1，变化 DiffPIR typically best among DPS; for BL(0.1,1): DiffPIR 0.72±1.10 vs ℓ2 5.28±1.88。
> - Deconvolution 上，MMSE optimality gap (dB) 为 DiffPIR (best DPS)，对比 ℓ2 / ℓ1，变化 DiffPIR often exceeds ℓ2 and ℓ1 baselines; for BL(0.1,1): DiffPIR 1.09±2.22 vs ℓ2 7.25±2.67。
> - Imputation 上，MMSE optimality gap (dB) 为 DiffPIR (best DPS)，对比 ℓ2 / ℓ1，变化 DiffPIR best among DPS; for BL(0.1,1): DiffPIR 0.24±1.14 vs ℓ2 5.28±1.88。

## 概述

本文提出了一种用于评估扩散后验采样（DPS）算法的统计基准框架。现有DPS算法的评估通常依赖于下游感知指标（如SSIM、FID）或过于简化的高斯混合先验，这些方法无法反映真实信号中常见的重尾/稀疏增量分布，从而可能高估后验采样质量。该框架使用离散化Lévy过程作为测试信号，其增量分布（高斯、拉普拉斯、Student-t、伯努利-拉普拉斯）具有可控的稀疏性和重尾性，且后验可通过高效的Gibbs方法获得金标准样本，从而支持分布级别的直接比较。通过将Gibbs方法嵌入反向扩散过程，可以任意精度地蒙特卡洛估计去噪后验的期望和协方差等对象，从而将DPS算法本身的误差与学习组件的近似误差分离开来。基准在去噪、去卷积、插值和部分傅里叶测量四种逆问题上，使用MMSE最优性间隙和后验覆盖测试评估了C-DPS、DiffPIR和DPnP等流行算法。

## 背景与动机
```
- figure_lines:
```md
*Figure 1: Unconditional reverse-diffusion trajectories obtained by DDPM using the arbitrary-precision Monte Carlo denoiser. Rows: Increment distributions. Columns: Diffusion times. Line styles: Different random states.*
```
- table_lines:
```md
*Table 1: MMSE optimality gap in decibel (mean ± standard deviation; lower is better; 0 is a perfect reconstruction) of various estimation methods over the test set. Bold: best among DPS algorithms.*
*Table 2: Univariate distributions used throughout this work. Parameters appear in the order they are specified in this table, e.g. Gauss ( \mu , \sigma ^ { 2 } )*
*Table 3: Latent variable representations and conditional distributions for common distributions.*
```
- formula_section_5_2:
```md
### 5.2 扩散模型基础

前向扩散SDE为：

$$\mathrm{d}\mathbf{X}_t = \mathbf{f}(\mathbf{X}_t, t) \mathrm{d}t + g(t) \mathrm{d}\mathbf{W}_t$$

反向SDE为：

$$\mathrm{d}\mathbf{X}_t = \left( \mathbf{f}(\mathbf{X}_t, t) - g^2(t) \nabla \log p_{\mathbf{X}_t}(\mathbf{X}_t) \right) \mathrm{d}t + g(t) \mathrm{d}\mathbf{W}_t$$

Tweedie公式将得分函数与MMSE去噪器联系起来：

$$\nabla \log p_{\mathbf{X}_t}(\mathbf{x}) = -\sigma(t)^{-2} \left( \mathbf{x} - \alpha(t) \mathbb{E}[\mathbf{X}_0 \mid \mathbf{X}_t = \mathbf{x}] \right)$$

DDPM离散反向步为：

$$\mathbf{X}_{t-1} = \frac{1}{\sqrt{1-\beta_t}} \left( \mathbf{X}_t + \beta_t \nabla \log p_{\mathbf{X}_t}(\mathbf{X}_t) \right) + \sqrt{\beta_t} \mathbf{Z}_t$$

```

## Candidate 20
- path: obsidian-vault/paper/ICLR_2026/P__A_Statistical_Learning_Perspective_on_Semi-dual_Adversarial_Neural_Optimal_Transport_Solvers.md
- title: A Statistical Learning Perspective on Semi-dual Adversarial Neural Optimal Transport Solvers
- issues: suspicious_short_formula:1, missing_figure_embed:6,7
- topic_row: Generative Models & Diffusion, Generative Models and Autoencoders
- head_excerpt:
```md
---
title: A Statistical Learning Perspective on Semi-dual Adversarial Neural Optimal Transport Solvers
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Statistical_Learning_Perspective_on_Semi-dual_Adversarial_Neural_Optimal_Transport_Solvers.pdf
aliases:
- 极小极大二次最优传输求解器的统计学习分析框架
acceptance: accepted
paradigm: 通过误差分解定理（Theorem 4.1）将OT映射的L^2误差上界表示为内/外估计误差与逼近误差之和，进而利用Rademacher复杂度（Theorem 4.2）和神经网络逼近能力（Theorem 4.3, 4.6）证明：只要选择适当的神经网络类和足够的样本量，泛化误差可以任意小（Theorem 4.9, Corollary 4.10）。
---

# A Statistical Learning Perspective on Semi-dual Adversarial Neural Optimal Transport Solvers

> [!tip] 核心洞察
> 通过误差分解定理（Theorem 4.1）将OT映射的L^2误差上界表示为内/外估计误差与逼近误差之和，进而利用Rademacher复杂度（Theorem 4.2）和神经网络逼近能力（Theorem 4.3, 4.6）证明：只要选择适当的神经网络类和足够的样本量，泛化误差可以任意小（Theorem 4.9, Corollary 4.10）。

| 字段 | 内容 |
|------|------|
| 中文题名 | 半对偶对抗神经最优传输求解器的统计学习视角 |
| 英文题名 | A Statistical Learning Perspective on Semi-dual Adversarial Neural Optimal Transport Solvers |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=FJTdyG8jeJ) |
| Topic | Generative Models & Diffusion, Generative Models and Autoencoders |
| Method | 极小极大二次最优传输求解器的统计学习分析框架 |
| Dataset | Korotin et al. (2021b) 合成数据集 |

> [!tip] 效果简介
> - Korotin et al. (2021b) 合成数据集 上，||T̂ - T*||_{L^2(P)}^2 为 OT求解器（神经网络），对比 线性估计器，变化 OT求解器误差显著低于所有基线方法。

## 概述

本文从统计学习理论的角度，系统分析了基于极小极大（minimax）优化的神经最优传输（Optimal Transport, OT）求解器的泛化误差。现有基于神经网络的OT求解器在实践中广泛使用，但缺乏严格的理论泛化保证。本文的核心贡献在于：针对二次成本（Wasserstein-2）的极小极大半对偶OT问题，提出了一个完整的误差分解框架，将泛化误差分解为估计误差（由经验分布代替真实分布引起）和逼近误差（由受限函数类引起），并分别利用Rademacher复杂度和神经网络逼近定理给出上界。最终证明，通过选择适当的神经网络类和足够的样本量，泛化误差可以任意小，收敛率为 $O(1/\sqrt{N}) + O(1/\sqrt{M})$。

## 背景与动机

### 2.1 最优传输问题
```
- figure_lines:
```md
*Figure 2: Continuous setup of OT problem.*
*Figure 3: Convergence rates of the OT solver learned with the quadratic transport cost and a limited number of empirical training samples.*
*Figure 4: Empirical approximation error of the OT solver learned with the quadratic transport cost and using shallow NN architectures.*
```
- formula_section_5_2:
```md
### 5.2 Rademacher复杂度上界（Theorem 4.2）

$$\mathcal{E}^{E} \leq 8 \mathcal{R}_{p,N}(\mathcal{H}) + 8 \mathcal{R}_{q,M}(\mathcal{F})$$

其中 $\mathcal{R}_{q,M}(\mathcal{F}) \stackrel{\mathrm{def}}{=} \frac{1}{M} \mathbb{E} \left\{ \sup_{\varphi, Y} \sum_{m=1}^M \varphi(y_m) \sigma_m \right\}$ 是函数类 $\mathcal{F}$ 的Rademacher复杂度。

```
