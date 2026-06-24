---
title: "MedCLIPSeg: Probabilistic Vision-Language Adaptation for Data-Efficient and Generalizable Medical Image Segmentation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MedCLIPSeg_Probabilistic_Vision_Language_Adaptation_for_Data_Efficient_and_Generalizable_Medical_Image_Segmentation.pdf
project_link: "https://tahakoleilat.github.io/MedCLIPSeg"
code_link: null
aliases:
- MedCLIPSeg
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入概率视觉语言适配器（PVL Adapter），对跨模态注意力的 Key 和 Value 进行变分建模，实现置信度加权的双向交互与蒙特卡洛不确定性采样。
primary_logic: 通过将 CLIP 的预训练表示与概率化、双向的视觉-文本融合相结合，并辅以软补丁级对比损失，可在保持参数高效的同时，使分割模型在低数据量和域偏移下获得更准确的预测和可解释的逐像素不确定性图。
claims:
- 移除 PVL 适配器导致 ID DSC 下降 7.9%，OOD DSC 下降 23.8%，表明概率双向融合是实现鲁棒多模态对齐的核心。
- 将概率注意力替换为确定性注意力使 OOD DSC 降低 15.9%，直接证实不确定性感知公式的价值。
- MedCLIPSeg 在 16 个数据集、5 种成像模态和 6 个器官上全面超越现有方法，10% 训练数据下比 SOTA CAT-Seg 高 2‑3% DSC。
- 16 datasets, 5 modalities, 6 organs (average) 上 ID DSC (%) = 89.11
---

# MedCLIPSeg: Probabilistic Vision-Language Adaptation for Data-Efficient and Generalizable Medical Image Segmentation

> [!tip] 核心洞察
> 通过将 CLIP 的预训练表示与概率化、双向的视觉-文本融合相结合，并辅以软补丁级对比损失，可在保持参数高效的同时，使分割模型在低数据量和域偏移下获得更准确的预测和可解释的逐像素不确定性图。

| 字段 | 内容 |
|------|------|
| 中文题名 | MedCLIPSeg：面向数据高效和可泛化医学图像分割的概率视觉语言自适应框架 |
| 英文题名 | MedCLIPSeg: Probabilistic Vision-Language Adaptation for Data-Efficient and Generalizable Medical Image Segmentation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Koleilat_MedCLIPSeg_Probabilistic_Vision-Language_Adaptation_for_Data-Efficient_and_Generalizable_Medical_Image_CVPR_2026_paper.html) · [Project](https://tahakoleilat.github.io/MedCLIPSeg) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MedCLIPSeg |
| Dataset | 16 datasets, 5 modalities, 6 organs |

> [!tip] 效果简介
> - 16 datasets, 5 modalities, 6 organs (average) 上，ID DSC (%) 89.11 vs 81.21 (-7.9% (去除 PVL Adapter))；OOD DSC (%) 79.02 vs 55.22 (-23.8% (去除 PVL Adapter))；OOD DSC (%) 79.02 vs 63.12 (-15.9% (确定性注意力变体))。
> - 多数据集平均 (10% 训练数据) 上，DSC 81.10 vs ~78.10 (CAT-Seg 估计值) (+2.5% (较 CAT-Seg 提升约 2‑3%))。

## 概述

医学图像分割长期受困于标注稀缺、特征模糊与跨域漂移三重挑战。现有视觉语言模型（VLM）虽然具备强大的语义理解能力，但其密集定位能力薄弱，且确定性跨模态注意力机制容易产生过度自信的预测，难以在保证数据效率的同时提供可靠的域外泛化和可解释的不确定性估计。

**MedCLIPSeg** 针对上述瓶颈，提出以 **概率视觉语言适配器（PVL Adapter）** 为核心的自适应框架。该方法冻结 CLIP 预训练编码器，仅训练轻量的 PVL 适配器和投影层，通过对跨模态注意力的 Key 与 Value 进行变分建模，实现置信度加权的双向视觉-文本融合，并借助蒙特卡洛采样生成逐像素不确定性图。同时引入软补丁级对比损失，细化图像与文本的密集语义对齐。

在 16 个数据集、5 种成像模态和 6 个器官上的系统评估表明，MedCLIPSeg 在数据效率和域泛化两个维度均显著超越现有方法。仅使用 10% 训练数据时，其 DSC 较当前最优的 **CAT-Seg**（Cho et al., 2023）提升约 2–3 个百分点。消融实验进一步揭示：移除 PVL 适配器导致域内 DSC 下降 7.9%、域外 DSC 骤降 23.8%；将概率注意力替换为确定性注意力则使域外 DSC 降低 15.9%，直接证实不确定性感知机制是实现鲁棒多模态对齐的关键。

该方法在保持参数高效的同时，首次将可解释的逐像素不确定性图纳入文本驱动的医学分割流程，为低资源场景下的可靠临床辅助提供了新的技术路径。

## 背景与动机

医学图像分割是临床诊断与治疗规划的关键步骤，但其自动化面临三重结构性挑战。**标注稀缺**：像素级标注高度依赖专家且耗时，严重制约全监督方法的可扩展性。**特征模糊**：病灶边界不清、组织对比度低，使得纯视觉模型容易产生过度自信的错误预测。**跨域漂移**：不同成像设备、采集协议和患者群体间的分布偏移，导致模型在未见目标域上性能急剧退化。这三者相互耦合，使同时追求数据效率、不确定度量化和域泛化能力成为医学分割领域的核心瓶颈。

近年来，视觉语言模型（VLM）的兴起为缓解标注依赖提供了新路径。以 CLIP 为代表的预训练模型通过大规模图文对比学习，获得了丰富的跨模态语义对齐能力。将其适配到分割任务时，现有工作大致分为两类：一类采用确定性交叉注意力将文本条件注入视觉特征（如 **DenseCLIP**，Rao et al., 2022；**LAVT**，Yang et al., 2022），另一类通过侧适配网络实现开放词汇分割（如 **SAN**，Xu et al., 2023；**CAT-Seg**，Cho et al., 2023）。然而，这些方法存在两个根本性缺陷。

**第一，密集定位能力薄弱。** CLIP 的预训练目标面向图像级全局对齐，其视觉编码器的补丁级表征缺乏细粒度语义定位能力。直接将冻结的 CLIP 特征用于像素级预测，会导致分割边界模糊和语义错位。**第二，确定性融合导致过度自信。** 现有方法将跨模态注意力视为确定性映射，忽视了视觉-文本交互中固有的歧义性。当面临域外数据或模糊区域时，确定性注意力会赋予不可靠特征过高的置信度，表现为校准不良的预测和显著的域外性能下降（Figure 1 底部可靠性曲线所示）。

上述缺陷在医学场景中被进一步放大。医学图像的模态多样性（CT、MRI、超声、内镜、皮肤镜）和器官异质性使得跨域泛化尤为困难。同时，临床部署要求模型不仅能给出分割结果，还需提供可解释的不确定性估计，以支持医生的审慎决策。现有医学 VLM 分割方法（如 **LViT**，Li et al., 2023；**BiomedParse**，Zhao et al., 2024）虽然引入了语言引导，但均未对跨模态交互中的不确定性进行显式建模，无法同时满足数据效率、域泛化和可靠性三个需求。

针对上述缺口，本文提出 **MedCLIPSeg**，其核心动机在于：**将概率建模引入视觉语言适配过程，使跨模态融合具备不确定性感知能力**。具体而言，通过对 CLIP 深层编码器中的 Key 和 Value 进行变分建模，学习置信度加权的双向注意力，使模型在低数据量和域偏移条件下，既能保持参数高效（冻结 CLIP 预训练参数），又能生成更准确的分割掩膜和可解释的逐像素不确定性图。这一设计从原理上区别于确定性适配范式，为医学图像分割的鲁棒性和可信度提供了新的技术路线。

## 核心创新

MedCLIPSeg 的核心创新在于将 **概率建模** 引入视觉语言模型的跨模态融合过程，同时保持 CLIP 预训练参数的冻结，从而在数据高效和域泛化两个维度上实现突破。其创新点可凝练为三个相互耦合的 **changed slots**，分别对应融合机制、不确定性估计和训练目标的重构。

### 1. 从确定性交叉注意力到概率视觉语言适配器（PVL Adapter）

现有 CLIP 适配方法（如 **LAVT**（Yang et al., 2022）、**DenseCLIP**（Rao et al., 2022））通常采用确定性单向交叉注意力进行模态融合，这导致模型对跨模态关联产生过度自信，尤其在域偏移下表现脆弱。MedCLIPSeg 提出 **概率视觉语言适配器（PVL Adapter）** ，对跨模态注意力的 Key 和 Value 进行变分建模，实现置信度加权的双向交互。

具体而言，PVL Adapter 将 Key 和 Value 建模为高斯分布 $\\mathcal{N}(\\mu, \\sigma^2)$，并通过重参数化技巧进行采样。注意力得分的计算同时考虑均值相似度 $S_{\\mu}$ 和方差惩罚项 $S_{\\sigma}^2$：

$$S_{\\mu} = \\frac{Q K_{\\mu}^{\\top}}{\\sqrt{D_a}}, \\quad S_{\\sigma}^2 = \\frac{Q^{\\circ 2} (K_{\\sigma}^2)^{\\top}}{D_a}$$

最终注意力权重通过带方差惩罚的 softmax 得到：

$$A = \\operatorname{softmax}\\left(S_{\\mu} - \\beta S_{\\sigma}\\right)$$

其中 $\\beta = 2.35$ 控制惩罚强度，使高不确定性的 token 被自动降权。这一机制的本质是将 **认知不确定性（epistemic uncertainty）** 直接编码到注意力计算中，而非事后估计。

消融实验提供了决定性证据：**移除 PVL Adapter 导致 ID DSC 下降 7.9%，OOD DSC 下降 23.8%**；将概率注意力替换为确定性注意力使 **OOD DSC 降低 15.9%**。这表明概率双向融合是实现鲁棒多模态对齐的核心组件，而非锦上添花的附加模块。

### 2. 从确定性预测到蒙特卡洛不确定性量化

传统分割模型仅输出确定性 logits，无法提供预测的置信度信息。MedCLIPSeg 通过对 Value 分布的蒙特卡洛采样，同时生成分割掩膜和逐像素不确定性图：

$$V_{\\mathrm{sample}} = V_{\\mu} + \\epsilon \\odot V_{\\sigma}, \\quad \\epsilon \\sim \\mathcal{N}(0, I)$$

多次采样后的均值作为最终分割结果，方差则构成可解释的不确定性图。这种设计同时捕获了 **数据噪声（aleatoric uncertainty）** 和 **模型认知不确定性（epistemic uncertainty）**，且无需额外的后处理模块。可视化结果显示，不确定性在病灶边界处达到峰值，并在跨域数据上保持一致性校准，验证了其可靠性。

### 3. 从硬监督到软补丁级对比损失

现有方法通常仅依赖分割损失（Dice + BCE），忽略了图像补丁与文本 token 之间的细粒度语义对齐。MedCLIPSeg 引入 **软补丁级对比损失（Soft Patch-level Contrastive Loss）** ，以文本相似度矩阵 $G$ 作为软目标，引导视觉补丁嵌入与文本描述的精细匹配：

$$\\mathcal{L}_{\\mathrm{soft}}(\\mathrm{P}, \\mathrm{G}) = -\\frac{1}{B}\\sum_i\\sum_j \\mathrm{G}_{ij} \\log(\\operatorname{softmax}(\\mathrm{P}_i)_j)$$

消融实验证实，排除该损失导致 HM DSC 降低 1.92%，表明其对于维持跨模态细粒度对齐具有不可替代的作用。

### 创新耦合效应

上述三个 changed slots 并非孤立存在，而是形成正向反馈循环：概率注意力为对比损失提供更可靠的软目标，对比损失反过来约束概率分布的语义一致性，而蒙特卡洛采样则为整个流程提供不确定性感知的闭环验证。这种耦合使得 MedCLIPSeg 在 **10% 训练数据下比 SOTA CAT-Seg 高出 2–3% DSC**，并在 16 个数据集、5 种成像模态、6 个器官上全面超越现有方法。

## 整体框架

MedCLIPSeg 的整体流水线围绕“冻结预训练编码器 + 轻量概率视觉语言适配器 + 软对比损失”三个支柱构建，形成一条从多模态输入到分割掩膜与不确定性图的双向融合通路。

**输入与编码阶段**。流水线接收两类输入：医学图像 $X_v$ 和描述目标结构的自然语言提示 $X_t$。图像经冻结的 CLIP 视觉编码器 $E_v$（UniMedCLIP ViT‑B/16）编码为补丁嵌入序列 $Z_v \in \mathbb{R}^{B \times (P+1) \times D}$；文本经冻结的文本编码器 $E_t$（PubMedBERT）编码为 token 序列 $Z_t \in \mathbb{R}^{B \times L \times D}$。冻结编码器的目的是保留 CLIP 在大规模预训练中习得的通用视觉‑语言对齐能力，避免微调带来的灾难性遗忘。

**核心融合模块：PVL Adapter**。视觉与文本表征进入概率视觉语言适配器（Probabilistic Vision‑Language Adapter），这是整个框架的因果旋钮。PVL Adapter 在 CLIP 的多个深层编码层之间插入，对跨模态注意力的 Key 和 Value 进行变分建模：Key 被参数化为均值 $K_\mu$ 和标准差 $K_\sigma$ 的高斯分布，由此计算出注意力得分的均值 $S_\mu$ 和方差 $S_\sigma^2$。最终注意力权重 $A$ 由置信度加权 softmax 给出：

$$A = \operatorname{softmax}\left(S_\mu - \beta S_\sigma\right)$$

其中 $\beta = 2.35$ 控制方差惩罚的强度，使高不确定性的 token 被自动降权。Value 同样被建模为分布，通过重参数化技巧采样 $V_{\mathrm{sample}} = V_\mu + \epsilon \odot V_\sigma$（$\epsilon \sim \mathcal{N}(0, I)$），经残差门控 $Y = g \odot O_{\mathrm{proj}} + (1-g) \odot X$ 与原始查询混合，实现置信度加权的双向视觉‑文本交互。多次蒙特卡洛采样 Value 不仅生成均值分割掩膜，还产生逐像素的不确定性图（aleatoric + epistemic），这是确定性融合方法无法提供的。

**分割头与损失**。融合后的视觉补丁嵌入 $\tilde{\mathbf{V}}$ 与投影后的文本 [EOS] 嵌入 $\tilde{\mathbf{t}}$ 进行点积，经上采样得到原图尺寸的分割 logits：

$$\mathbf{M} = \mathrm{Upsample}_{H \times W}\left(\tilde{\mathbf{V}} \cdot \tilde{\mathbf{t}}^{\top}\right)$$

训练目标由两部分组成：标准分割损失（Dice + BCE）与软补丁级对比损失 $\mathcal{L}_{\mathrm{soft}}$。后者以文本嵌入间的相似度矩阵为软目标，引导图像补丁与文本 token 的细粒度语义对齐，弥补了传统分割损失在跨模态密集预测中的不足。

**整体数据流**可概括为：`(图像, 文本) → 冻结编码器 → PVL Adapter（概率双向注意力 × 多层）→ 点积相似度 → 上采样 → (分割掩膜, 不确定性图)`。该设计使 MedCLIPSeg 在仅训练 PVL Adapter 和投影层（保持 CLIP 参数冻结）的前提下，实现了数据高效、域可泛化且自带不确定性量化的文本驱动医学图像分割。

### 补充图表

![[assets/figures/papers/paper_list_l764_https_openaccess_thecvf_com_content_CVPR2026_html_Koleilat_MedCLIPSeg_Pr/figures/001_Figure_1.jpg]]
*Figure 1: (Top): Comparison between deterministic and probabilistic cross-modal fusion techniques in CLIP adaptation for text-driven segmentation. Probabilistic formulation models variability in visual–textual representations as distributions, enabling more robust feature alignment. (Bottom): Robustness and Reliability plots over ID and OOD data show improved generalization, with smaller out-of-domain performance drops and better calibration of predicted confidence, reflected by lower Brier scores*

![[assets/figures/papers/paper_list_l764_https_openaccess_thecvf_com_content_CVPR2026_html_Koleilat_MedCLIPSeg_Pr/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed MedCLIPSeg framework for text-driven medical image segmentation. The model extends CLIP with vision and language encoders connected via PVL Adapters, which perform confidence-weighted image–text fusion at multiple deep layers. Segmentation and uncertainty maps arise from the mean and entropy of posterior samples, with a soft patch-level contrastive loss*

## 核心模块与公式推导

MedCLIPSeg 的核心由四个模块构成：冻结的视觉与文本编码器、概率视觉语言适配器（PVL Adapter）、像素-文本相似度映射，以及软补丁级对比损失。其中，PVL Adapter 是整条流水线的关键创新——它对跨模态注意力的 Key 和 Value 进行变分建模，实现置信度加权的双向交互与蒙特卡洛不确定性采样。

### 3.1 冻结编码器与输入表示

框架沿用 CLIP 的双塔结构，但完全冻结预训练参数。给定图像 $X_v$ 和文本提示 $X_t$，视觉编码器 $E_v$ 输出包含 $P$ 个补丁 token 和 1 个 [CLS] token 的序列，文本编码器 $E_t$ 输出 $L$ 个 token 的序列：

$$Z _ { v } = E _ { v } ( X _ { v } ) \in \mathbb R ^ { B \times ( P + 1 ) \times D }$$

$$Z _ { t } = E _ { t } ( X _ { t } ) \in \mathbb { R } ^ { B \times L \times D }$$

其中 $B$ 为批次大小，$D$ 为嵌入维度。视觉编码器采用 UniMedCLIP ViT-B/16，文本编码器采用 PubMedBERT，两者在训练期间保持冻结。

### 3.2 概率视觉语言适配器（PVL Adapter）

PVL Adapter 是框架的核心组件，插入在 CLIP 的多个深层编码层之间，执行置信度加权的双向图像-文本融合。其关键机制是对 Key 和 Value 进行变分参数化，而非使用确定性点估计。

**Key 的变分建模与置信度加权注意力。** 给定查询 $Q$，Key 被建模为高斯分布 $\mathcal{N}(K_\mu, K_\sigma^2)$。注意力得分的均值与方差分别计算为：

$$S _ { \mu } = \frac { Q K _ { \mu } ^ { \top } } { \sqrt { D _ { a } } } , \quad S _ { \sigma } ^ { 2 } = \frac { Q ^ { \circ 2 } ( K _ { \sigma } ^ { 2 } ) ^ { \top } } { D _ { a } }$$

其中 $D_a$ 为注意力头维度，$\circ 2$ 表示逐元素平方。最终注意力权重通过带方差惩罚的 softmax 获得：

$$A = \{ A _ { i j } \} = \operatorname{softmax} \left( S _ { \mu } - \beta S _ { \sigma } \right)$$

等价地，可写为带惩罚因子的形式：

$$A _ { i j } = \frac { \exp { \left( S _ { \mu , i j } \right) } / \omega _ { i j } } { \sum _ { r } \exp { \left( S _ { \mu , i r } \right) } / \omega _ { i r } } , \quad \omega _ { i j } = \exp { \left( \beta S _ { \sigma , i j } \right) }$$

惩罚因子 $\beta = 2.35$（对应高斯分布的半高全宽），使高方差的 Key 对应的注意力权重被压低，从而实现“置信度加权”——模型自动降低对不确定跨模态配对的依赖。

**Value 的变分建模与蒙特卡洛采样。** Value 同样被建模为高斯分布 $\mathcal{N}(V_\mu, V_\sigma^2)$。通过重参数化技巧进行采样：

$$V _ { \mathrm { s a m p l e } } = V _ { \mu } + \epsilon \odot V _ { \sigma } , \quad \epsilon \sim \mathcal { N } ( 0 , I )$$

多次采样可生成不同的 Value 实现，进而产生多个分割掩膜。掩膜的均值作为最终预测，方差则构成逐像素的不确定性图（同时捕获 aleatoric 和 epistemic 不确定性）。

**残差门控与双向交互。** 跨模态融合的输出通过可学习的门控 $g$ 与原始查询进行残差混合：

$$Y = g \odot O _ { \mathrm { p r o j } } + ( 1 - g ) \odot X$$

PVL Adapter 在视觉到文本、文本到视觉两个方向上对称执行上述操作，形成双向交互——视觉特征引导文本理解的细化，文本语义反过来增强视觉特征的判别力。

### 3.3 像素-文本相似度与分割 logits

融合后的视觉补丁嵌入 $\tilde{\mathbf{V}}$ 与投影后的文本 [EOS] 嵌入 $\tilde{\mathbf{t}}$ 进行点积，并经上采样恢复到原图尺寸，得到最终分割 logits：

$$\mathbf{M} = \mathrm{Upsample}_{H \times W}(\tilde{\mathbf{V}} \cdot \tilde{\mathbf{t}}^{\top})$$

其中 $\tilde{\mathbf{V}} = \psi(Z_v^{[\mathrm{Patches}]})$ 通过投影层 $\psi$ 对补丁嵌入进行上缩放，$\tilde{\mathbf{t}} = \phi(Z_t^{[\mathrm{EOS}]})$ 通过投影层 $\phi$ 对文本 [EOS] token 进行变换。

### 3.4 软补丁级对比损失

为细化图像-文本的密集对齐，引入软补丁级对比损失。首先计算文本相似度矩阵作为软目标：

$$G = \operatorname{softmax}(\mathbf{p}_t \cdot \mathbf{p}_t^{\top} / \tau)$$

其中 $\mathbf{p}_t$ 为文本提示的嵌入，$\tau$ 为温度参数。随后以 $G$ 为目标，对视觉补丁的预测分布 $P$ 计算交叉熵：

$$\mathcal{L}_{\mathrm{soft}}(\mathrm{P}, \mathrm{G}) = -\frac{1}{B}\sum_i\sum_j \mathrm{G}_{ij} \log(\operatorname{softmax}(\mathrm{P}_i)_j)$$

该损失引导视觉补丁在语义空间中的分布与文本语义结构保持一致，从而提升密集预测的跨模态对齐质量。总训练目标为分割损失（Dice + BCE）与 $\mathcal{L}_{\mathrm{soft}}$ 的加权和。

> **注意：** 以上公式均来自论文 Section 3.1–3.4 的原始推导，变量含义以论文定义为准。未在原文中出现的推导细节不应被额外补充。

### 补充图表

![[assets/figures/papers/paper_list_l764_https_openaccess_thecvf_com_content_CVPR2026_html_Koleilat_MedCLIPSeg_Pr/figures/003_Figure_3.jpg]]
*Figure 3: Illustrations of PVL Adapter and AttnPVL*

## 实验与分析

### 实验设置概述

MedCLIPSeg 以 UniMedCLIP ViT‑B/16 为视觉编码器、PubMedBERT 为文本编码器，冻结全部预训练参数，仅训练 PVL 适配器与投影层。所有模型使用 Adam 优化器、余弦退火调度，初始学习率 $3\times10^{-4}$，批量大小 24，训练 100 轮（EUS 数据集为 10 轮）。评估覆盖 16 个数据集、5 种成像模态、6 个器官，从数据效率、域泛化、不确定性质量三个维度展开。

---

### 数据效率：极少标注下的性能边界

**Table 1** 报告了不同训练数据比例下各方法的平均 DSC 与 NSD。MedCLIPSeg 在全部数据量级上均取得最优或次优结果：

- **10% 训练数据**：MedCLIPSeg 达到 81.10 DSC / 83.94 NSD，较当前 SOTA 开放词汇分割方法 **CAT‑Seg**（Cho et al., 2023）高出约 2–3 个 DSC 点。这一优势在仅使用 1% 数据时更加显著——MedCLIPSeg 的 DSC 为 74.46，而 CAT‑Seg 降至 69.37，差距拉大到约 5 个点。
- **100% 训练数据**：MedCLIPSeg 取得 88.66 DSC / 91.35 NSD，在所有对比方法中排名第一，超越 **nnUNet**（Isensee et al., 2021）等全监督专用分割框架。

**瓶颈解读**：传统全监督方法（U‑Net、TransUNet、Swin‑UNet 等）在数据量骤减时性能急剧退化，而 MedCLIPSeg 通过冻结 CLIP 预训练表示并引入概率双向融合，以极少的可训练参数维持了强泛化能力。这说明 **跨模态语义先验比单纯增加网络容量更能抵抗标注稀疏**。

---

### 域泛化：跨模态、跨器官的鲁棒性

**Table 2** 展示了源域训练、目标域零样本评估的跨域分割结果。MedCLIPSeg 在绝大多数迁移对上取得最优 DSC：

- **超声跨域**：以 BUSI 为源域、BUSUC 为目标域时，MedCLIPSeg 达到 84.4 DSC，显著优于第二名 **HiFormer**（Heidari et al., 2023）的 74.0。
- **内窥镜跨域**：Kvasir‑SEG → CVC‑ClinicDB 迁移中，MedCLIPSeg 取得 90.2 DSC，比 **CAT‑Seg** 高出约 4 个点。
- **MRI 跨器官**：BTMRI → CHAOS (肝脏) 场景下，MedCLIPSeg 达到 88.0 DSC，较 **LViT**（Li et al., 2023）提升约 3 个点。
- **皮肤镜跨域**：ISIC 2017 → ISIC 2018 迁移中，MedCLIPSeg 以 92.5 DSC 排名第一。

**关键发现**：MedCLIPSeg 的 OOD 性能衰减幅度远小于所有对比方法。确定性注意力变体在域偏移下 DSC 骤降 15.9 个百分点（见消融部分），直接证实 **概率化跨模态注意力是域泛化的核心使能因素**——它通过方差惩罚抑制了分布外样本上的过度自信匹配。

---

### 消融实验：因果链的严格验证

**Table 3** 的消融实验揭示了各组件对性能的因果贡献：

| 消融操作 | ID DSC 变化 | OOD DSC 变化 | 因果含义 |
|---------|------------|-------------|---------|
| 移除 PVL Adapter | **–7.9%** | **–23.8%** | 概率双向融合是鲁棒多模态对齐的第一性组件 |
| 概率注意力 → 确定性注意力 | 轻微下降 | **–15.9%** | 不确定性感知对域外泛化不可或缺，对域内影响有限 |
| 排除软补丁级对比损失 $\mathcal{L}_{\mathrm{soft}}$ | –1.92% (HM DSC) | — | 软对比损失在维持细粒度跨模态对齐中起辅助但正向作用 |
| 取消双向交互机制 | 进一步降低 | — | 视觉与文本特征的相互精炼对分割质量有增益 |

**因果链归纳**：PVL Adapter 提供跨模态融合的骨架 → 概率化 Key/Value 建模赋予该骨架不确定性感知能力 → 软对比损失在骨架之上细化图像-文本对齐。三者缺一不可，其中概率化注意力是 OOD 泛化的**决定性因果旋钮**。

---

### 不确定性图质量与校准

**Figure 4** 展示了 MedCLIPSeg 在域内（蓝色框）和域外（红色框）数据上的分割掩膜与逐像素不确定性图。不确定性在病灶边界处达到峰值，且在不同数据集间保持一致的分布模式，表明模型对自身预测的置信度具有良好的校准性。

定量校准指标（Brier 分数）显示，MedCLIPSeg 的概率化输出比确定性变体更接近真实准确率，这源于 Value 分布的蒙特卡洛采样同时捕获了**偶然不确定性**（数据噪声）和**认知不确定性**（模型知识边界）。

---

### 文本提示设计的敏感性

**Table 4** 考察了不同文本提示模板对分割性能的影响。实验表明：

- 包含解剖部位和成像模态信息的提示（如 “ultrasound breast mass”）优于仅包含目标类别的简短提示。
- 提示中的语义歧义（如 “lesion” vs “tumor”）会导致 DSC 波动 1–3 个点，说明 **提示工程是当前框架的性能杠杆之一**。
- 这一敏感性也暴露了方法的一个现实局限：在缺乏标准化提示模板的临床场景中，需要自动提示优化策略来保证稳定性。

---

### 预训练模型选择的影响

**Table 5** 比较了不同预训练视觉语言模型作为骨干时的分割性能。UniMedCLIP（医学领域预训练）在所有指标上优于通用域 CLIP（OpenAI）和 BioMedCLIP，验证了 **领域对齐的预训练表示对下游医学分割的迁移效率至关重要**。这一结果与冻结骨干、仅训练适配器的设计哲学一致——预训练质量直接决定了适配器的性能上限。

---

### 失败模式与局限

1. **3D 数据未验证**：当前实验全部基于 2D 切片，方法在体积数据上的扩展性及计算效率仍是开放问题。
2. **提示依赖**：如 Table 4 所示，性能对文本提示设计敏感，在缺乏领域知识的低资源场景下可能退化。
3. **不确定性图的临床效用未评估**：尽管生成了可解释的不确定性图，但未进行医生可用性研究或与临床决策流程的集成测试。
4. **极端域偏移**：在部分跨模态迁移对（如 CT → 超声）上，性能仍存在明显下降，说明概率化机制虽能缓解但无法完全消除模态鸿沟。

![[assets/figures/papers/paper_list_l764_https_openaccess_thecvf_com_content_CVPR2026_html_Koleilat_MedCLIPSeg_Pr/figures/006_Table_4.jpg]]
*Table 4: Effect of text prompt design*

---

### 小结

MedCLIPSeg 在 16 个数据集、5 种模态上的系统评估表明：**概率视觉语言适配器是实现数据高效、域可泛化医学图像分割的关键架构创新**。消融实验严格证明，PVL Adapter 的移除会导致 OOD DSC 下降 23.8%，而将概率注意力替换为确定性注意力会使 OOD DSC 降低 15.9%——这两个数字共同锚定了“不确定性感知跨模态融合”作为方法核心价值的因果地位。

### 补充图表

![[assets/figures/papers/paper_list_l764_https_openaccess_thecvf_com_content_CVPR2026_html_Koleilat_MedCLIPSeg_Pr/figures/004_Table_1.jpg]]
*Table 1: Data-efficiency evaluation: This table reports the average DSC and NSD (%) when varying the fraction of training data across different segmentation methods. Best results are in bold, and second-best are underlined*

![[assets/figures/papers/paper_list_l764_https_openaccess_thecvf_com_content_CVPR2026_html_Koleilat_MedCLIPSeg_Pr/figures/005_Table_2.jpg]]
*Table 2: Domain generalization: Models are trained on a source dataset and evaluated on OOD target datasets without adaptation. DSC (%) values are reported where the best results are in bold, and second-best are underlined*

![[assets/figures/papers/paper_list_l764_https_openaccess_thecvf_com_content_CVPR2026_html_Koleilat_MedCLIPSeg_Pr/figures/008_Figure_5.jpg]]
*Figure 5: Layer-wise interventions (left) and confidence weighting (β) (right) ablations averaged on ID and OOD data*

![[assets/figures/papers/paper_list_l764_https_openaccess_thecvf_com_content_CVPR2026_html_Koleilat_MedCLIPSeg_Pr/figures/009_Table_5.jpg]]
*Table 5: Effect of pre-trained vision–language models*

![[assets/figures/papers/paper_list_l764_https_openaccess_thecvf_com_content_CVPR2026_html_Koleilat_MedCLIPSeg_Pr/figures/007_Figure_4.jpg]]
*Figure 4: Segmentation and uncertainty visualizations. Uncertainty peaks along lesion boundaries and remains consistent across diverse datasets, indicating reliable calibration and generalization. ID data are in blue while OOD data are in red*

## 方法谱系与知识库定位

### 1. 技术脉络与基线关系

MedCLIPSeg 处于**视觉语言模型（VLM）驱动的医学图像分割**这一交叉领域。其直接技术谱系可沿两条主线追溯：

**（1）从通用分割到 VLM 适配的分割范式**

传统医学分割以全监督 CNN 为基石，代表工作包括 **U-Net**（Ronneberger et al., 2015）、**Attention U-Net**（Oktay et al., 2018）、**UNet++**（Zhou et al., 2018）以及自动配置框架 **nnUNet**（Isensee et al., 2021）。Transformer 兴起后，**TransUNet**（Chen et al., 2021）、**Swin-UNet**（Cao et al., 2022）、**UNETR**（Hatamizadeh et al., 2022）和 **HiFormer**（Heidari et al., 2023）等混合架构进一步提升了特征建模能力。然而，这些方法均依赖大量像素级标注，且缺乏对文本语义的自然利用。

CLIP 的出现催生了文本驱动分割的新范式。**CLIPSeg**（Lüddecke et al., 2022）和 **CRIS**（Wang et al., 2022）率先将 CLIP 用于指代分割，但仅做轻量解码器适配，密集定位能力有限。**DenseCLIP**（Rao et al., 2022）、**Zeg-CLIP**（Zhou et al., 2023）和 **SAN**（Xu et al., 2023）通过语言引导的密集预测或侧适配网络提升了开放词汇分割性能。当前 SOTA **CAT-Seg**（Cho et al., 2023）在通用开放词汇分割上表现突出。MedCLIPSeg 在 10% 训练数据下比 CAT-Seg 高出约 2–3% DSC（Table 1），证明了概率双向融合在数据效率上的优势。

**（2）医学 VLM 分割的专用化探索**

医学领域的文本驱动分割起步较晚。**LViT**（Li et al., 2023）引入语言-视觉 Transformer，**Ariadne's Thread**（Zhong et al., 2023）利用文本提示分割感染区域，**BiomedParse**（Zhao et al., 2024）结合生物医学知识解析，**EoMT-CLIP**（Pan et al., 2025）尝试证据学习驱动的分割。这些工作虽将文本信息引入医学分割，但跨模态融合仍以确定性注意力为主，缺乏对不确定性的显式建模。另一方面，**MedSAM**（Ma et al., 2024）作为医学通用分割模型，虽性能强大，但依赖空间提示（框/点）而非自然语言，与 MedCLIPSeg 的文本驱动范式形成互补。

**关键差异点**：MedCLIPSeg 的核心区分度在于**概率视觉语言适配器（PVL Adapter）**——对跨模态注意力的 Key 和 Value 进行变分建模，实现置信度加权双向交互与蒙特卡洛不确定性采样。消融实验直接证实：移除 PVL 适配器导致 ID DSC 下降 7.9%，OOD DSC 下降 23.8%（Table 3）；将概率注意力替换为确定性注意力使 OOD DSC 降低 15.9%（Table 3）。这说明概率双向融合是实现鲁棒多模态对齐的核心因果机制，而非简单的架构堆叠。

### 2. 适用边界与局限

**已验证的适用范围：**
- **数据模态**：覆盖 5 种成像模态（MRI、CT、超声、内窥镜、皮肤镜），在 16 个数据集、6 个器官上进行了系统验证。
- **数据效率**：在 10%–100% 训练数据比例下均保持优势，特别适合标注稀缺场景。
- **域泛化**：在跨域 OOD 设定下显著优于确定性基线，不确定性图沿病灶边界峰值分布且跨数据集一致（Figure 4）。

**明确局限（需人工验证的边界）：**
1. **维度限制**：当前评估集中在 2D 医学图像数据集，尚未在 3D 体积数据或动态视频场景中验证方法的有效性。概率变分建模在 3D 下的计算开销和注意力机制的可扩展性是未知数。
2. **临床可用性未验证**：尽管提出了可解释的不确定性图，但未深入讨论其在临床工作流中的实际可用性和医生接受度。Brier score 等校准指标虽有所改善，但缺乏放射科医生的用户研究。
3. **提示依赖性**：框架依赖适当的自然语言提示，Table 4 显示提示设计对分割性能有显著影响，表明自动提示优化是必要的后续方向。当前需要人工设计文本模板，在开放场景下可能成为瓶颈。
4. **骨干网络绑定**：Table 5 显示不同预训练 VLM 对性能有影响，当前最优配置基于 UniMedCLIP ViT-B/16 + PubMedBERT，泛化到其他 VLM 骨干时性能可能波动。

### 3. 开放问题

1. **3D 扩展与计算效率**：如何将概率视觉语言融合扩展到 3D 医学图像（如 CT 体积），同时保持可接受的计算效率？变分注意力在 3D token 序列上的内存和计算复杂度可能成为瓶颈。

2. **不确定性驱动的临床闭环**：能否将逐像素不确定性图与临床决策过程直接结合，形成闭环反馈调节？例如，高不确定性区域可自动触发医生复核或主动学习采样。

3. **下游任务迁移**：在下游任务（如病变检测、生存预测、治疗效果评估）中，不确定性感知的跨模态表征能否带来额外收益？当前仅验证了分割任务本身。

4. **自适应提示生成**：如何设计自适应的文本提示生成策略，以进一步减少对人工提示模板的依赖？这可能涉及与 LLM 的集成或基于图像内容的自动提示优化。

5. **多模态融合深度与层间干预**：Figure 5 显示层间干预策略对性能有影响，但最优的 PVL 适配器插入层数和位置选择机制尚不明确，是否存在任务自适应的动态路由策略值得探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/MedCLIPSeg_Probabilistic_Vision_Language_Adaptation_for_Data_Efficient_and_Generalizable_Medical_Image_Segmentation.pdf]]
