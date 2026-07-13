---
title: "A Cognitive Process-Inspired Architecture for Subject-Agnostic Brain Visual Decoding"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Cognitive_Process_Inspired_Architecture_for_Subject_Agnostic_Brain_Visual_Decoding.pdf
project_link: null
code_link: https://github.com/xmed-lab/VCFLOW
aliases:
- VCFAV
- CPIASABVD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/neuroscience_cognitive_science
core_operator: "通过显式建模腹侧-背侧双流视觉通路，并引入基于重分配模块的跨被试对比学习，将语义特征与被试特定特征解耦，从而提取被试不变的表征。"
primary_logic: "将fMRI脑特征按早期视觉区、腹侧流、背侧流拆分，分别与CLIP不同层级的嵌入对齐（低层、高层、视频嵌入），再通过重分配适配器分离语义与被试特定信息，实现无需重训练即可泛化到新被试。"
claims:
- "VCFLOW在50-way分类任务上达到14.0%，相比GLFA∗（9.6%）相对提升46%。"
- "VCFLOW在SSIM上达到0.396，相比GLFA∗（0.137）提升189%。"
- "VCFLOW在视频50-way分类上达到18.2%，相比NEURONS∗（16.1%）提升13%。"
- "VCFLOW仅需10秒即可生成一段重建视频，无需任何重训练。"
---

# A Cognitive Process-Inspired Architecture for Subject-Agnostic Brain Visual Decoding

> [!tip] 核心洞察
> 将fMRI脑特征按早期视觉区、腹侧流、背侧流拆分，分别与CLIP不同层级的嵌入对齐（低层、高层、视频嵌入），再通过重分配适配器分离语义与被试特定信息，实现无需重训练即可泛化到新被试。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 受认知过程启发的跨被试脑视觉解码架构 |
| 英文题名 | A Cognitive Process-Inspired Architecture for Subject-Agnostic Brain Visual Decoding |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=H1GLFKk0xE) · [GitHub](https://github.com/xmed-lab/VCFLOW) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/neuroscience_cognitive_science |
| Method | Visual Cortex Flow Architecture (VCFLOW) |
| Dataset | cc2017 |

> [!tip] 效果简介
> - cc2017 上，50-way (frame-based semantic-level) 为 14.0%，对比 9.6% (GLFA∗)，变化 +45.8%。
> - cc2017 上，2-way (frame-based semantic-level) 为 77.9%，对比 74.8% (GLFA∗)，变化 +4.1%。
> - cc2017 上，SSIM (frame-based pixel-level) 为 0.396，对比 0.137 (GLFA∗)，变化 +189.1%。

## 概要

现有fMRI到视频解码方法严重依赖被试特定训练（每名被试需超过12小时），无法直接应用于未见过的被试，这严重限制了临床可扩展性。针对这一瓶颈，本文提出**Visual Cortex Flow Architecture (VCFLOW)**，一种受认知过程启发的跨被试（subject-agnostic）脑视觉解码框架，发表于ICLR 2026。

VCFLOW的核心洞察在于：通过显式建模腹侧-背侧双流视觉通路，将fMRI脑特征按早期视觉区、腹侧流、背侧流拆分，分别与CLIP不同层级的嵌入（低层、高层、视频嵌入）对齐，并引入基于重分配模块（SARA）的跨被试对比学习，将语义特征与被试特定特征解耦，从而提取被试不变的表征。该方法由三个模块组成：**HCAM**（层次化认知对齐模块）、**SARA**（跨被试重分配适配器）和**HED**（层次化显式解码器）。

在cc2017数据集上的实验表明，VCFLOW在跨被试设定下显著优于现有方法：在50-way分类任务上达到14.0%（相对GLFA\*提升46%），SSIM达到0.396（相对GLFA\*提升189%），视频50-way分类达18.2%（相对NEURONS\*提升13%）。与全被试特定方法NEURONS相比，平均性能仅下降7%，但推理时无需任何重训练，仅需约10秒即可生成一段重建视频。该方法首次实现了无需重训练即可泛化到新被试的fMRI到视频解码，为临床可扩展性提供了实质性优势。



现有fMRI到视频解码方法的核心瓶颈在于其严重的被试依赖性。以NEURONS为代表的典型方法，每名新被试需要超过12小时的个体化训练数据才能构建专用模型，这一要求极大地限制了该方法在临床场景中的可扩展性——面对新患者时，高昂的数据采集和模型训练成本使其难以落地。虽然GLFA等方法尝试通过数据级功能对齐（functional alignment）实现被试自适应，但其仍需要所有被试（包括测试被试）的fMRI数据进行预训练，并非严格的被试无关设定。更根本的问题在于，现有方法未能有效区分fMRI信号中被试特异性的神经活动模式与跨被试共享的语义表征，导致在未见被试上的泛化能力严重不足。

针对这一缺口，本文的核心动机是设计一种**被试无关（subject-agnostic）**的脑视觉解码架构，使得模型在从未见过某被试任何数据的情况下，仍能直接对其fMRI信号进行视频重建。这一目标需要解决两个核心挑战：其一，如何从fMRI信号中提取跨被试共享的语义表征，同时剥离被试特定的噪声模式；其二，如何在缺乏被试特定训练数据的前提下，保持与全被试特定方法相当的重建质量。

本文提出的VCFLOW架构从认知神经科学的双流视觉通路理论中汲取灵感，将大脑视觉皮层按功能分为早期视觉区（处理低级特征如边缘、朝向、颜色）、腹侧流（处理高级抽象语义）和背侧流（编码动态特征与空间表征）。基于这一划分，VCFLOW设计了三个核心模块：层次化认知对齐模块（HCAM）将fMRI信号按上述三区拆分，分别与CLIP不同层级的嵌入对齐；被试无关重分配适配器（SARA）通过对比学习将语义特征与被试特定特征解耦，提取被试不变的表征；层次化显式解码器（HED）则针对不同语义维度设计分割、分类、字幕、模糊视频重建等显式任务，实现多层次的互补解码。

这一设计的关键洞察在于：通过显式建模视觉皮层的功能分区结构，并利用CLIP预训练模型的多层级语义空间作为桥梁，可以将fMRI信号中跨被试共享的语义信息与被试个体的神经活动模式分离开来。实验结果表明，VCFLOW在50-way语义分类任务上达到14.0%，相比被试无关基线GLFA∗（9.6%）相对提升46%；在SSIM指标上达到0.396，相比GLFA∗（0.137）提升189%。更重要的是，VCFLOW在推理时仅需10秒即可生成一段重建视频，无需任何重训练，且相比全被试特定方法NEURONS，平均性能仅下降7%——这一代价在临床可扩展性的巨大收益面前是可接受的。



## 核心方法与创新机理

VCFLOW 的核心创新在于将**脑认知通路的结构先验**与**跨被试特征解耦**相结合，从根本上改变了 fMRI 到视频解码的范式——从“为每个被试训练专用模型”转向“一个模型适用于所有未见过的被试”。这一转变的关键瓶颈在于：现有方法（如 NEURONS）严重依赖被试特定训练（每名被试需超过12小时），无法直接泛化到新被试，严重限制了临床可扩展性。

VCFLOW 的因果机制通过三个模块化的 changed slots 实现：

1.  **fMRI 特征提取方式**：从“全脑信号直接映射到 CLIP 空间”改为“按视觉皮层功能分区进行层次化对齐”。具体地，将 fMRI 信号拆分为**早期视觉区**（对齐 CLIP 低层特征，捕获边缘、方向、颜色等感知属性）、**腹侧流**（对齐 CLIP 高层特征，处理抽象语义）和**背侧流**（对齐 CLIP 视频嵌入，编码动态特征与空间表征）。这一设计直接利用了人脑视觉系统的双流通路结构（Figure 2），使得不同脑区的功能特性能被更精确地建模。

2.  **跨被试泛化策略**：从“数据级功能对齐（GLFA）”或“被试特定编码器（NEURONS）”改为**基于重分配模块（SARA）的语义-被试特征解耦 + 跨被试对比学习**。SARA 通过一个可学习的重分配层（Redistribution Layer）将输入特征扩展为语义 token（`T_sem`）和被试特定 token（`T_subj`），然后利用三项损失函数进行优化：`L_align`（BiMixCo 损失对齐语义 token 与 CLIP 嵌入）、`L_subj`（被试分类损失确保 `T_subj` 携带被试身份信息）、`L_generic`（对称 InfoNCE 损失对齐不同被试间的语义 token）。这一设计的关键洞察是：通过显式分离语义与被试特定信息，模型学到的语义表征对被试身份不敏感，从而无需重训练即可泛化到新被试。

3.  **解码器设计**：从“隐式对齐 CLIP 视觉特征”或“单一显式任务”改为**层次化显式解码器（HED）**，对早期视觉、腹侧、背侧特征分别设计**分割**、**分类**、**字幕**、**模糊视频重建**等显式任务。消融实验（Table 6）表明，HED 提供了最显著的增益，尤其在高层语义和重建质量上——移除 HED 后 50-way 分类准确率从 14.2% 降至 10.0%。

**证据强度**：上述三个 changed slots 均有明确的实验支撑。Table 1 显示 VCFLOW 在 50-way 分类任务上达到 14.0%，相比 GLFA∗（9.6%）相对提升 46%；SSIM 达到 0.396，相比 GLFA∗（0.137）提升 189%。Table 2 的消融实验进一步验证了每个模块的贡献：移除 HCAM 后 50-way 从 14.2% 降至 10.7%；移除 SARA 后降至 7.52%；移除 HED 后降至 10.0%。**需要注意的是**，当前实验仅在 cc2017 数据集（3 名被试）上验证，更大规模被试上的泛化表现需要手动验证。



![[assets/figures/papers/iclr26_0002_H1GLFKk0xE_A_Cognitive_Process-Inspired_Architecture_for_Su/figures/003_Figure_3.jpg]]
*Figure 3: The overall framework of VCFLOW consists of three core components: (1) Hierarchical Cognitive Alignment Module (HCAM), (2) Subject-Agnostic Redistribution Adapter (SARA), and (3) Hierarchical Explicit Decoder (HED). VCFLOW learns three types of semantic representations through HCAM, which are then fused with subject-agnostic common features extracted by SARA. These enriched representations are subsequently decoded by HED to explicitly reconstruct information across multiple semantic levels*

VCFLOW 是一个端到端的跨被试脑视觉解码架构，其核心设计受认知科学中腹侧-背侧双流视觉通路启发。整个 pipeline 由三个模块串联而成，形成从 fMRI 体素到视频重建的完整数据流。

**模块一：层次化认知对齐模块（HCAM）**。该模块将全脑 fMRI 信号按功能 ROI 划分为三个成分：早期视觉区（对应低层感知特征，如边缘、朝向、颜色）、腹侧流（对应高层语义特征）和背侧流（对应动态特征与空间表征）。每个成分通过可学习的 Cross-Attention 模块与 CLIP 不同层级的嵌入对齐——早期视觉区对齐 CLIP 低层特征，腹侧流对齐高层特征，背侧流对齐视频嵌入。对齐采用 BiMixCo 损失，在统一语义空间中建立 fMRI 信号与视觉语义的映射。此模块的输出为三种层次化语义嵌入：`F_early`、`F_ventral`、`F_dorsal`。

**模块二：跨被试重分配适配器（SARA）**。这是实现被试无关泛化的关键瓶颈突破点。SARA 接收 HCAM 输出的语义嵌入，通过重分配层（Redistribution Layer）沿 token 维度扩展特征（公式：`E_exp = Expand(E) ∈ R^{B×S×(L+L_redis)×C}`），然后分离出语义 token `T_sem` 和被试特定 token `T_subj`（公式：`[T_sem, T_subj] = Redistribution(E_exp)`）。SARA 的训练目标由三项损失加权组合：`L_align`（BiMixCo 损失，对齐语义 token 与 CLIP 嵌入）、`L_subj`（被试分类损失，强制 `T_subj` 编码被试身份）、`L_generic`（对称 InfoNCE 损失，对齐不同被试间的语义 token，使语义表征跨被试不变）。通过这种解耦，SARA 将个体特定语义映射到公共的被试不变语义空间，使得测试时新被试的 fMRI 信号无需任何微调即可直接映射到该空间。

**模块三：层次化显式解码器（HED）**。HED 接收 SARA 输出的被试不变语义特征，设计四个显式解码任务以互补方式重建视频：概念识别（`L_cls`，多标签分类预测帧中关键概念）、场景描述（`L_caption`，GPT-2 前缀语言建模生成字幕）、模糊视频重建（`L_motion`，MAE 损失重建低分辨率运动信息）、分割任务（`L_seg`）。这些任务分别对应不同语义维度的解码，最终融合输出高保真重建视频。

**数据流总结**：fMRI 体素序列 → HCAM（ROI 划分 + CLIP 层次对齐）→ 三种语义嵌入 → SARA（重分配层解耦语义与被试特征）→ 被试不变语义 token → HED（四个显式解码任务融合）→ 重建视频。整个推理过程仅需约 10 秒（Figure 1），无需任何重训练，相比传统被试依赖方法（每名被试需超过 12 小时训练）实现了质的飞跃。在 cc2017 数据集（3 名被试）上的定量结果表明，VCFLOW 在 50-way 分类任务上达到 14.0%（相对 GLFA∗ 提升 46%），SSIM 达到 0.396（相对 GLFA∗ 提升 189%），视频 50-way 分类达到 18.2%（相对 NEURONS∗ 提升 13%），且与全被试特定方法 NEURONS 相比平均性能仅下降 7%（Table 1, Table 4）。



VCFLOW 的整体架构由三个核心模块组成：**层次化认知对齐模块 (HCAM)**、**跨被试重分配适配器 (SARA)** 和**层次化显式解码器 (HED)**。其设计动机源于对腹侧-背侧双流视觉通路的功能拆分：早期视觉区负责边缘、朝向、颜色等低层级特征，腹侧流处理高层级抽象语义，背侧流编码动态与空间表征（Figure 2）。通过将fMRI信号与CLIP不同层级的嵌入进行显式对齐，VCFLOW实现了跨被试的语义解耦。

### 1. 层次化认知对齐模块 (HCAM)

HCAM 的核心操作是基于功能ROI的体素划分。从全脑fMRI序列 $\mathbf{X} \in \mathbb{R}^{B \times S \times V}$（$B$为批次，$S$为被试数，$V$为体素数）中，通过预定义的ROI索引集合 $\mathcal{T}_{\mathrm{ROIs}}$ 提取对应体素子集：

$$
\mathbf{X}_{\mathrm{ROIs}} = \mathbf{X}[:, :, \mathcal{T}_{\mathrm{ROIs}}] \in \mathbb{R}^{B \times S \times V_{\mathrm{ROIs}}}
$$

该模块将fMRI特征拆分为三个分支：早期视觉区对齐CLIP低层特征（感知与结构属性），腹侧流对齐CLIP高层特征（抽象语义），背侧流对齐CLIP视频嵌入（动态信息）。各分支通过可学习的交叉注意力模块（Cross-Attention）进行特征融合，并采用BiMixCo损失（Kim et al., 2020）进行层次化对齐。该损失的具体形式为双向混合对比损失（参见附录A.1），其核心操作是对两个fMRI信号进行线性混合：

$$
\mathcal{V}_{c}^{*} = mix(\mathcal{V}_{c}, \mathcal{V}_{m_{c}}) = \lambda_{c} \cdot \mathcal{V}_{c} + (1 - \lambda_{c}) \mathcal{V}_{m_{c}}
$$

其中 $\lambda_{c} \sim \mathrm{Beta}(\alpha, \alpha)$ 为混合系数。BiMixCo损失通过对称地计算混合样本与原始样本之间的相似性，增强了特征表示的鲁棒性。

### 2. 跨被试重分配适配器 (SARA)

SARA 模块通过重分配层（Redistribution Layer）实现语义-被试特征解耦。首先，沿token维度扩展输入特征，加入 $L_{\mathrm{redis}}$ 个重分配token：

$$
\mathbf{E}_{\mathrm{exp}} = \mathrm{Expand}(\mathbf{E}) \in \mathbb{R}^{B \times S \times (L + L_{\mathrm{redis}}) \times C}
$$

重分配层通过自注意力机制将原始特征中的语义信息重新分配到语义token $\mathbf{T}_{\mathrm{sem}}$ 中，将被试特定信息分配到被试token $\mathbf{T}_{\mathrm{subj}}$ 中：

$$
[\mathbf{T}_{\mathrm{sem}}, \mathbf{T}_{\mathrm{subj}}] = \operatorname{Redistribution}(\mathbf{E}_{\mathrm{exp}})
$$

SARA 的训练包含三个损失项（公式中的 $\lambda$ 为超参数）：

$$
\mathcal{L}_{\mathrm{SARA}} = \lambda_{\mathrm{align}} \mathcal{L}_{\mathrm{align}} + \lambda_{\mathrm{subj}} \mathcal{L}_{\mathrm{subj}} + \lambda_{\mathrm{generic}} \mathcal{L}_{\mathrm{generic}}
$$

其中：
- **语义对齐损失** $\mathcal{L}_{\mathrm{align}} = \mathrm{BiMixCo}(\mathbf{T}_{\mathrm{sem}}, \mathbf{F}_{\mathrm{clip}})$：通过BiMixCo损失将语义token与CLIP嵌入对齐。
- **被试分类损失** $\mathcal{L}_{\mathrm{subj}}$：通过分类器迫使 $\mathbf{T}_{\mathrm{subj}}$ 包含被试身份信息，促进语义token $\mathbf{T}_{\mathrm{sem}}$ 中被试信息的剥离。
- **跨被试对齐损失** $\mathcal{L}_{\mathrm{generic}}$：对称InfoNCE损失，用于对齐不同被试间的语义token：

$$
\mathcal{L}_{\mathrm{generic}} = \frac{1}{2(S-1)} \sum_{i=2}^{S} \left[ \mathrm{InfoNCE}(\mathbf{T}_{i-1,\mathrm{sem}}^{\mathrm{norm}}, \mathbf{T}_{i,\mathrm{sem}}^{\mathrm{norm}}) + \mathrm{InfoNCE}(\mathbf{T}_{i,\mathrm{sem}}^{\mathrm{norm}}, \mathbf{T}_{i-1,\mathrm{sem}}^{\mathrm{norm}}) \right]
$$

该损失迫使来自不同被试但语义相同的token在特征空间中接近，是实现被试无关泛化的关键因果机制。

### 3. 层次化显式解码器 (HED)

HED 对HCAM输出的三种特征（$\mathbf{F}_{\mathrm{early}}, \mathbf{F}_{\mathrm{ventral}}, \mathbf{F}_{\mathrm{dorsal}}$）分别设计显式任务，通过多任务学习实现互补信息的协同重建。具体损失包括：

- **概念识别损失** $\mathcal{L}_{cls} = \mathcal{L}_{ce}(\mathcal{D}_{cls}(\bar{e}^{v}), \mathcal{C})$：交叉熵损失，从视觉嵌入 $\bar{e}^{v}$ 中预测帧的关键概念 $\mathcal{C}$。
- **场景描述损失** $\mathcal{L}_{caption} = -\frac{1}{|\mathcal{S}|} \sum_{i=1}^{|\mathcal{S}|} \log \mathcal{D}_{caption}(s_i | s_{<i}, e^t)$：负对数似然损失，基于文本嵌入 $e^t$ 生成字幕。
- **模糊视频重建损失** $\mathcal{L}_{motion} = \frac{1}{F} \sum_{i=1}^{F} |y_{c,i}^{motion} - y_{c,i}^{\prime}|$：平均绝对误差损失，重建视频的运动信息。

此外，消融研究（Table 5, Table 6）表明，SARA中的三个损失项和HED中的四个显式任务均对最终性能有贡献。HCAM的移除导致50-way分类从14.2%降至10.7%（Table 2），证实了层次化认知对齐的必要性。



## 实验与关键发现

### 主结果：定量比较

VCFLOW在cc2017数据集（3名被试）上的主要实验结果汇总于Table 1。在**被试无关**设定下（即训练时完全排除测试被试的fMRI数据），VCFLOW在所有指标上均显著超越两个被试无关基线：GLFA∗（数据级功能对齐的被试无关版本）和NEURONS∗（全被试特定方法NEURONS的被试无关适配版本）。

![[assets/figures/papers/iclr26_0002_H1GLFKk0xE_A_Cognitive_Process-Inspired_Architecture_for_Su/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of VCFLOW with representative methods. All results are based on subjects provided by the cc2017 dataset (Wen et al., 2018). GLFA∗ refers to GLFA results with test subject data excluded during pretraining. NEURONS∗ refers to the NEURONS model adapted to a subject-agnostic setting by modifying its data processing pipeline and encoder components. w/o Pretrain indicates whether the encoder is pretrained using the fMRI data of the test subject*

**语义级帧分类**：在50-way分类任务上，VCFLOW达到14.0%，相对GLFA∗（9.6%）提升46%，相对NEURONS∗（10.1%）提升38.6%。2-way分类上，VCFLOW达77.9%，同样领先GLFA∗（74.8%）和NEURONS∗（74.9%）。

**像素级帧重建**：SSIM指标上，VCFLOW达到0.396，相对GLFA∗（0.137）提升189%，相对NEURONS∗（0.380）提升4.2%。PSNR上，VCFLOW为10.478，相对GLFA∗（9.614）提升9.0%，相对NEURONS∗（9.614）提升9.0%。SSIM的大幅提升表明VCFLOW在结构保真度上具有压倒性优势。

**视频级语义**：视频50-way分类上，VCFLOW达18.2%，相对NEURONS∗（16.1%）提升13%，相对GLFA∗（17.0%）提升7.1%。CLIP-pcc（时空一致性）达0.940，略优于NEURONS∗（0.931）。

**与全被试特定方法的差距**：Table 4显示，VCFLOW与全被试特定方法NEURONS（每名被试需>12小时训练）相比，平均性能仅下降7%。这意味着VCFLOW在几乎零训练代价（推理仅需10秒）下，仅牺牲了7%的性能，验证了其被试无关策略的有效性。

![[assets/figures/papers/iclr26_0002_H1GLFKk0xE_A_Cognitive_Process-Inspired_Architecture_for_Su/figures/010_Table_4.jpg]]
*Table 4: Comparison of VCFLOW with GLFA (Li et al., 2024) and NEURONS (Wang et al., 2025) across subjects. GLFA adopts subject-adaptive pretraining by using fMRI data from all subjects, while NEURONS is trained and evaluated on the same subject*

### 消融实验

Table 2对VCFLOW的三大核心模块——HCAM、SARA、HED——进行了逐级消融。移除任一模块均导致性能显著下降，其中HED的移除带来的损失最大（50-way从14.2%降至10.0%），表明层次化显式解码对高层语义和重建质量的贡献最为关键。

![[assets/figures/papers/iclr26_0002_H1GLFKk0xE_A_Cognitive_Process-Inspired_Architecture_for_Su/figures/007_Table_2.jpg]]
*Table 2: Ablations on the key components of VCFLOW, and all results are from subject 1*

Table 5针对SARA模块内部的三个损失项进行消融：语义对齐损失（L_align）、被试分类损失（L_subj）、跨被试对齐损失（L_generic）。移除L_align后50-way从14.2%降至7.52%，降幅最大；移除L_generic后降至9.67%，说明跨被试对比学习是被试无关泛化的核心机制。

![[assets/figures/papers/iclr26_0002_H1GLFKk0xE_A_Cognitive_Process-Inspired_Architecture_for_Su/figures/011_Table_5.jpg]]
*Table 5: Ablations on the components of SARA, and all results are from subject 1*

Table 6针对HED模块的四个显式子任务进行消融：L_caption（字幕）、L_cls（分类）、L_seg（分割）、L_motion（模糊视频重建）。移除L_caption后50-way从14.2%降至10.0%，移除L_motion后降至12.8%，表明字幕生成和运动重建是互补的语义通道。

### ROI划分方案对比

Table 3比较了两种ROI划分方案：Scheme A（按早期视觉区、腹侧流、背侧流拆分）与Scheme B（统一全脑映射）。Scheme A在所有指标上均优于Scheme B（50-way: 14.2% vs 12.7%），验证了认知通路启发的层次化对齐策略的有效性。

![[assets/figures/papers/iclr26_0002_H1GLFKk0xE_A_Cognitive_Process-Inspired_Architecture_for_Su/figures/009_Table_3.jpg]]
*Table 3: Comparison of ROI partitioning schemes on subject 1*

### 定性分析与失败模式

Figure 5的定性比较显示，VCFLOW相比GLFA在语义保真度和时间一致性上均更优，能捕捉细粒度语义（如物体纹理、颜色）并保持运动信息。

Figure 8揭示了两种主要失败模式：（1）**罕见对象类别**：当刺激视频中的主要对象属于训练集中极少出现的类别时，模型难以有效学习其语义；（2）**复杂交织语义**：当视频语义过于复杂且多对象交互时，模型难以恢复最显著的语义成分。这些失败模式指向了训练数据多样性不足和语义解耦能力的局限性。

### 关键结论

VCFLOW在严格被试无关设定下，以仅7%的性能代价换取了零重训练的跨被试泛化能力，在50-way分类上相对GLFA∗提升46%，SSIM提升189%。核心贡献来自三个模块的协同：HCAM的认知通路对齐、SARA的语义-被试特征解耦、HED的多层次显式解码。失败模式主要集中于数据稀有的边缘场景。



## 定位与知识库关联

### 与现有方法的关系

VCFLOW 的核心创新在于首次将 fMRI 到视频重建问题置于 **被试无关** 设定下，这与现有方法形成了根本性对比。现有主流方法可分为两类：

1. **全被试特定方法**：以 NEURONS 为代表，其训练过程需要每名被试超过 12 小时的 fMRI 数据采集和模型训练，遇到新患者时必须从头训练。VCFLOW 在推理时仅需约 10 秒即可生成重建视频，无需任何重训练，牺牲的性能仅为平均 7%（相对 NEURONS 全被试特定版本）。

2. **被试自适应方法**：以 GLFA 为代表，通过数据级功能对齐（functional alignment）将不同被试的 fMRI 信号映射到公共空间，但 GLFA 在预训练时仍需使用所有被试（包括目标测试被试）的数据。其严格被试无关版本 GLFA∗（排除测试被试数据后）性能大幅下降——VCFLOW 在 50-way 分类上达到 14.0%，相对 GLFA∗ 的 9.6% 提升 46%；在 SSIM 上达到 0.396，相对 GLFA∗ 的 0.137 提升 189%。

VCFLOW 在视频级指标上同样达到 SOTA：50-way 视频分类 18.2%，相对 NEURONS∗（16.1%）提升 13%；CLIP-pcc 达到 0.940，略优于 NEURONS∗ 的 0.931。

### 方法学差异的因果机制

VCFLOW 与 baseline 的差异可归因于三个核心改变：

1. **fMRI 特征提取方式**：baseline（如 NEURONS）使用全脑 fMRI 信号直接映射到 CLIP 空间；VCFLOW 将 fMRI 信号按早期视觉区、腹侧流、背侧流拆分，分别对齐 CLIP 的低层特征（感知结构）、高层特征（抽象语义）和视频嵌入（动态信息）。消融实验证实，移除 HCAM 模块后 50-way 从 14.2% 降至 10.7%，表明层次化对齐是性能提升的关键瓶颈。

2. **跨被试泛化策略**：GLFA 依赖数据级功能对齐，NEURONS 直接使用被试特定编码器；VCFLOW 通过重分配模块（SARA）将语义特征与被试特定特征显式解耦，并引入跨被试对比学习（对称 InfoNCE 损失 L_generic）。消融表明，SARA 的三个损失（L_align、L_subj、L_generic）均贡献性能提升，其中 L_generic 对跨被试泛化起核心作用。

3. **解码器设计**：baseline 通常隐式对齐 CLIP 视觉特征或使用单一任务；VCFLOW 的层次化显式解码器（HED）对早期视觉、腹侧、背侧特征分别设计分割、分类、字幕、模糊视频重建四个显式任务。消融表明 HED 提供最显著的增益，尤其在高层语义和重建质量上，四个显式任务均贡献性能。

### 适用边界

- **数据条件**：当前仅在 cc2017 数据集（3 名被试）上验证，更大规模被试（如 >10）上的表现尚待探索。训练使用了 DIR 和 GOD 数据集进行 fMRI-to-image 预训练。
- **任务范围**：仅适用于 fMRI 到视频重建，且假设刺激视频为自然视频。对非自然刺激（如图形、文字）的解码能力未验证。
- **被试要求**：需要被试的视觉皮层 ROI 划分（早期视觉区、腹侧流、背侧流），这对脑损伤患者可能构成额外限制。
- **计算资源**：虽然推理仅需 10 秒，但训练阶段需要多任务联合优化和渐进式学习策略，计算成本高于简单 baseline。

### 已知局限

1. **罕见类别失效**：在跨被试设定下，当刺激视频中的主要对象属于非常罕见的类别时，模型难以有效学习其语义。这可能是由于训练数据中长尾分布的语义表示不足。
2. **复杂交织语义退化**：当刺激视频中的语义过于复杂且相互交织时，模型难以恢复最显著的语义成分。这暗示当前的特征解耦机制在处理高度耦合的多语义场景时存在局限。
3. **数据规模限制**：仅 3 名被试的训练数据可能限制了模型的泛化能力，尤其是被试间的大脑解剖和功能结构差异可能未被充分建模。
4. **性能差距**：相比全被试特定方法 NEURONS，VCFLOW 平均性能下降 7%，说明被试无关泛化仍存在信息损失，解耦机制尚未完全消除被试特定噪声。

### 开放问题

1. **罕见对象解码**：如何通过数据增强（如 MixCo 的参数优化）、外部知识注入或长尾学习策略提升对罕见类别的解码能力？
2. **复杂语义场景**：能否通过注意力机制或层次化语义解析更好地处理交织语义？当前 HED 的四个显式任务是否足以覆盖所有语义维度？
3. **规模扩展性**：在更多被试（如 >10）上的被试无关泛化表现如何？是否需要更复杂的被试对齐策略？
4. **渐进式学习策略**：不同周期长度 T 对性能的影响如何？正弦权重调度是否最优，还是存在更有效的调度函数？
5. **MixCo 参数敏感性**：不同 Beta 分布参数对 MixCo 数据增强效果的影响尚待系统分析，这可能影响跨被试对比学习的稳定性。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Cognitive_Process_Inspired_Architecture_for_Subject_Agnostic_Brain_Visual_Decoding.pdf

![[paperPDFs/ICLR_2026/A_Cognitive_Process_Inspired_Architecture_for_Subject_Agnostic_Brain_Visual_Decoding.pdf]]
