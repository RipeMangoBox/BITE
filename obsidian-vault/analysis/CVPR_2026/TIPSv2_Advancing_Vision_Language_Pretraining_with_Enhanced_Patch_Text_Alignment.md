---
title: "TIPSv2: Advancing Vision-Language Pretraining with Enhanced Patch-Text Alignment"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TIPSv2_Advancing_Vision_Language_Pretraining_with_Enhanced_Patch_Text_Alignment.pdf
aliases:
- TIPSv2
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过在预训练中引入iBOT++损失，对可见tokens施加直接监督，强制模型保持局部语义对齐。
primary_logic: 蒸馏分析揭示，对所有patch tokens（而非仅masked tokens）进行监督，并配合随机初始化，能显著提升patch-text对齐。将这一思想融入预训练目标（iBOT++），同时保留masking机制，可以在不依赖蒸馏的情况下获得类似的对齐增强效果。
claims:
- 蒸馏中移除masking并随机初始化学生编码器能大幅提升patch-text对齐（零样本分割mIoU）。
- 将iBOT替换为iBOT++能在预训练中大幅提升零样本分割性能。
- iBOT++在消融研究中贡献了+14.1 ADE150 mIoU的提升。
- iBOT++能显著改善patch-text对齐，如图1所示。
---

# TIPSv2: Advancing Vision-Language Pretraining with Enhanced Patch-Text Alignment

> [!tip] 核心洞察
> 蒸馏分析揭示，对所有patch tokens（而非仅masked tokens）进行监督，并配合随机初始化，能显著提升patch-text对齐。将这一思想融入预训练目标（iBOT++），同时保留masking机制，可以在不依赖蒸馏的情况下获得类似的对齐增强效果。

| 字段 | 内容 |
|------|------|
| 中文题名 | TIPSv2：通过增强Patch-文本对齐推进视觉-语言预训练 |
| 英文题名 | TIPSv2: Advancing Vision-Language Pretraining with Enhanced Patch-Text Alignment |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.12012) · [Project](https://gdm-tipsv2.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TIPSv2 |
| Dataset | PASCAL Context, PASCAL VOC, ADE20K |

> [!tip] 效果简介
> - PASCAL Context (PC59) 上，mIoU (Zero-shot Seg) 37.1 vs 33.5 (+3.6)。
> - PASCAL VOC (VOC21) 上，mIoU (Zero-shot Seg) 44.4 vs 30.5 (+13.9)。
> - ADE20K (ADE150) 上，mIoU (Zero-shot Seg) 24.7 vs 20.8 (+3.9)。

## 概述

**问题瓶颈**：现有视觉-语言预训练模型在密集patch表示与文本嵌入的对齐方面表现较差，一个反直觉的现象是——大规模模型在patch-text对齐上甚至弱于小模型（如TIPS ViT-g教师模型在零样本分割上的mIoU仅为2.6，而被其蒸馏出的ViT-L学生模型达到20.8，见Table 1）。这一退化在SigLIP2系列中同样被观察到（Table 14），揭示出单纯扩大模型规模并不能自动改善局部语义对齐。

**核心思路**：TIPSv2从蒸馏分析中提炼出一个关键洞察——对所有patch tokens（而非仅masked tokens）施加直接监督，并配合随机初始化学生编码器，能显著提升patch-text对齐。将这一思想转化为预训练目标**iBOT++**：在masked image modeling中，visible tokens也直接参与softmax交叉熵损失，强制模型保持局部语义一致性，同时保留75%的masking机制以维持整体表征质量。

**方法定位**：TIPSv2在TIPS（Maninis et al., ICLR 2025）的基础上进行三方面改进——(1) 以iBOT++替代原有iBOT损失，扩展patch级监督范围；(2) 采用head-only EMA策略，仅对投影头做指数移动平均，减少约42%训练参数；(3) 引入多粒度文本增强，交替使用Gemini和PaliGemma合成标题。该方法属于“对比学习+自监督”联合预训练范式，与CLIP、SigLIP2、DINOv2/v3等主流视觉编码器形成直接对比。

**主要结果**：在零样本语义分割任务上，TIPSv2 ViT-L/14相比TIPS ViT-L/14在PASCAL VOC上提升+13.9 mIoU（30.5→44.4），在ADE20K上提升+3.9 mIoU（20.8→24.7）；相比SigLIP2 SO/14，VOC上领先+17.6 mIoU（Table 5）。消融实验表明，iBOT++单独贡献+14.1 ADE150 mIoU的提升（Table 4）。在全局图文检索、图像唯一任务（深度估计、语义分割等）上，TIPSv2在多数指标上取得最优或次优（Table 6, 7），且在4/6任务上超越更大规模的DINOv3（Table 8）。值得注意的是，TIPSv2在零样本分割中使用简单的上采样协议，而SILC和DINOv2依赖更昂贵的滑动窗口TCL协议，仍取得更优性能。

## 背景与动机

### 视觉-语言预训练中的密集对齐困境

视觉-语言预训练（VLP）已在全局图像-文本对齐任务上取得显著进展，以**CLIP**（Radford et al., ICML 2021）为代表的对比学习方法能够学习强大的全局表示。然而，这些模型在**密集patch-文本对齐**方面表现薄弱——即图像中每个局部patch与对应文本概念之间的语义对应关系。这种局部对齐能力对于零样本分割、开放词汇检测等密集预测任务至关重要。

现有方法试图通过结合自监督学习来改善这一问题。**TIPS**（Maninis et al., ICLR 2025）将对比学习与DINO全局自蒸馏和iBOT patch级掩码图像建模相结合，但TIPS中iBOT损失仅对被masked的patch tokens施加监督（见Eq 2中mask指示变量 $m_i$），可见tokens完全不参与该损失。这种设计使得模型在patch-文本对齐上存在根本性缺陷。

### 反直觉的蒸馏现象：大模型对齐退化

一个关键的观察来自蒸馏实验：**TIPS ViT-L学生模型在零样本分割上显著超越其ViT-g教师模型**（Table 1）。具体而言，TIPS ViT-g（教师）在ADE150零样本分割上仅取得2.6 mIoU，而蒸馏出的ViT-L学生却达到20.8 mIoU。类似的退化模式在**SigLIP2**（Tschannen et al., arXiv 2025）系列中同样出现：更大的模型反而表现出更差的patch-文本对齐（Table 14）。

这一现象揭示了核心瓶颈：**大规模VLP模型在预训练过程中，密集patch表示与文本嵌入之间的对齐会系统性退化**。模型容量的增大并未自动转化为更好的局部语义理解，反而可能因全局对比目标的支配性而抑制了局部表示的学习。

### 蒸馏分析揭示的对齐机制

为了理解学生模型为何能超越教师，论文对蒸馏过程进行了系统的消融分析（Table 2）。关键发现包括：

1. **移除masking至关重要**：在蒸馏过程中将mask比例设为0.0（即不使用masking），零样本分割性能大幅提升。这表明标准的masked image modeling范式——仅对被masked tokens施加监督——限制了对齐能力。

2. **随机初始化优于预训练初始化**：学生编码器从随机初始化开始训练，而非继承教师权重，能获得更好的patch-文本对齐。这暗示教师模型中的局部表示已经“锁定”在次优状态，需要重新学习。

3. **对所有tokens的直接监督是因果杠杆**：蒸馏分析的核心洞察在于，当对所有patch tokens（而非仅masked tokens）施加softmax交叉熵损失，并配合随机初始化时，patch-文本对齐得到根本性增强。这正是后续iBOT++设计的思想源头。

### 本文动机与目标

基于上述分析，TIPSv2旨在解决以下核心问题：**如何在预训练阶段（而非蒸馏阶段）直接强化patch-文本对齐，使得大规模模型也能保持强大的密集表示能力？**

论文提出将蒸馏中的发现“翻译”回预训练目标，通过三个关键改进构建TIPSv2：

- **iBOT++**：将iBOT损失扩展为对所有tokens（masked和visible）施加监督，在预训练中直接强制局部语义对齐。
- **Head-only EMA**：简化EMA机制以降低训练开销，同时保持自监督损失的稳定性。
- **多粒度文本增强**：引入Gemini合成的详细描述，增加文本监督的多样性。

核心假设是：**通过对可见tokens施加直接的patch级监督，可以在不依赖蒸馏的情况下，使预训练模型获得与蒸馏学生相当甚至更强的密集对齐能力**。Figure 1通过零样本分割可视化直观展示了这一改进的显著效果。

## 核心创新

TIPSv2 的核心创新源于一个反直觉的发现：在视觉-语言预训练中，蒸馏得到的小模型在 patch-文本对齐能力上可以显著超越其大模型教师。基于这一观察，论文提出三项关键改进，将蒸馏中的有效机制转化为可直接在预训练中使用的技术。

### 1. iBOT++：全 token 监督的掩码图像建模

**问题根因**：标准 iBOT 损失（式 2）仅对被掩码的 patch token 施加监督，而可见 token 不参与损失计算。蒸馏分析（Table 2）揭示，当移除 masking 并对所有 patch token 施加监督时，零样本分割性能大幅提升——从 masking ratio 0.75 时的 mIoU 不足 10，跃升至无 masking 时的 ADE150 20.0 / VOC21 30.8。这表明显式的全 token 监督是 patch-文本对齐的关键瓶颈。

**技术方案**：iBOT++ 将 iBOT 损失中的 mask 指示器 $m_i$ 移除，使损失函数变为：

$$\mathcal{L}_{\mathrm{iBOT}++} = - \sum_{i=1}^{N} h_t(f_t(I)_i)^T \log h_s(f_s(I_{\mathrm{mask}})_i)$$

该损失对全部 $N$ 个 patch token（包括可见和被掩码部分）施加 softmax 交叉熵监督。与蒸馏场景不同，预训练中教师编码器 $f_t$ 仍由 EMA 更新，学生 $f_s$ 接收被掩码的图像，但教师对完整图像的所有 patch 都提供目标信号。

**关键证据**：
- 将 TIPS ViT-g 中的 iBOT 替换为 iBOT++，零样本分割性能全面跃升：PC59 从 14.2→28.6（+14.4），ADE150 从 3.5→17.6（+14.1），VOC21 从 29.1→37.2（+8.1）（Table 3）。
- 累积消融中，iBOT++ 单独贡献了 ADE150 上 +14.1 mIoU 的提升（Table 4）。
- 定性结果（Figure 1, Figure 9）显示 iBOT++ 显著改善了 patch-文本对齐质量。

**关键设计选择**：iBOT++ 保留了 75% 的 masking 比例。消融实验（Table 12）表明，75% 的 mask ratio 对整体性能和 patch-文本对齐至关重要——过低或过高的 masking 比例均会导致性能下降。

### 2. Head-only EMA：精简的自蒸馏机制

**问题根因**：标准 DINO/iBOT 框架需要维护完整的教师编码器 EMA 副本，这使训练参数量翻倍。论文发现在自监督损失中，EMA 的核心作用集中在投影头而非编码器本体。

**技术方案**：Head-only EMA 将 EMA 更新仅应用于投影头 $h_t$，而编码器部分直接复用学生编码器（$f_t = f_s$）。这一简化在 ViT-B 上减少了约 42% 的训练参数，同时保持了自蒸馏损失的有效性。

**关键证据**：累积消融（Table 4）显示，引入 head-only EMA 后，ADE150 零样本分割从 17.6 小幅提升至 19.1，同时 Flickr 检索性能也有改善。这表明精简 EMA 不仅降低了资源消耗，还对 patch-文本对齐有正向贡献。

**局限性**：完全移除 EMA 会导致训练不稳定，因此在投影头上保留 EMA 是必要的最低配置。

### 3. 多粒度文本增强

**问题根因**：此前 TIPS 仅使用 PaliGemma 生成的合成描述作为文本监督，描述粒度和多样性有限。

**技术方案**：引入 Gemini 模型生成的更详细、更全面的图像描述，与 PaliGemma 描述随机交替使用，为第二个 CLS token 提供多粒度的文本监督信号（Figure 4）。

**关键证据**：在 iBOT++ 基础上叠加多粒度文本增强（Table 4），ADE150 mIoU 从 17.6 提升至 18.1，同时 Flickr 检索 Recall@1 从 65.2 提升至 67.9。这表明多粒度文本描述增强了模型对图像语义的鲁棒理解。

### 创新之间的因果关系

三项创新并非孤立存在。蒸馏分析（Table 2）是 iBOT++ 的直接灵感来源——蒸馏中“无 mask + 随机初始化学生”的成功经验被转化为预训练中的全 token 监督机制。Head-only EMA 则在保持 iBOT++ 有效性的前提下降低了训练开销。多粒度文本增强进一步丰富了语义监督信号，与 iBOT++ 的细粒度 patch 监督形成互补。三者共同构成了 TIPSv2 的完整预训练方案（Figure 3）。

## 整体框架

TIPSv2 的预训练框架建立在 TIPS（Maninis et al., ICLR 2025）之上，将对比图像-文本学习与自监督学习统一在一个端到端的训练流程中。整体损失函数由三个分量构成：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{CLIP}} + \mathcal{L}_{\mathrm{DINO}} + \mathcal{L}_{\mathrm{iBOT}++}
$$

其中 $\alpha=1.0$, $\beta=2.0$（见附录 A.9），实际训练时 $\mathcal{L}_{\mathrm{iBOT}}$ 被替换为 $\mathcal{L}_{\mathrm{iBOT}++}$。

### 模块架构与数据流

框架由以下核心模块组成，其关系如 Figure 3 所示：

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2604_12012/figures/005_Figure_3.jpg]]
*Figure 3: TIPSv2 pretraining overview. TIPSv2 introduces 3 improvements (highlighted in green borders) to the combined contrastive and self-supervised approach to pretrain vision encoders. iBOT++ is an enhanced masked image modeling loss. Head-only EMA enables memory-efficient self-supervised losses. Multi-granularity captions provide a range of possible textual descriptions for images, increasing the robustness of the model*

1. **Vision Transformer（ViT）图像编码器** — 将输入图像编码为全局嵌入 $f_s^g(I)$ 和 patch 级嵌入序列 $\{f_s(I)_i\}_{i=1}^N$。这是整个 pipeline 的共享骨干网络。

2. **Transformer 文本编码器** — 将文本描述编码为文本嵌入，用于与图像嵌入进行对比对齐。

3. **CLIP 对比损失 $\mathcal{L}_{\mathrm{CLIP}}$** — 对齐全局图像嵌入与文本嵌入，构成视觉-语言预训练的基础监督信号。

4. **DINO 自蒸馏损失 $\mathcal{L}_{\mathrm{DINO}}$** — 作用于全局级别，比较学生网络对局部裁剪的嵌入与教师网络对全局视图的嵌入：
   $$
   \mathcal{L}_{\mathrm{DINO}} = -\sum_{i=1}^{M} h_t(f_t^g(I))^T \log h_s(f_s^g(I_i))
   $$
   其中 $h_t$, $h_s$ 分别为教师和学生的投影头。

5. **iBOT++ 掩码图像建模损失 $\mathcal{L}_{\mathrm{iBOT}++}$** — 作用于 patch 级别，是 TIPSv2 的核心创新。与原始 iBOT 仅对被掩码的 patch 施加监督不同，iBOT++ 对**所有 patch tokens**（包括被掩码和可见的）施加 softmax 交叉熵损失：
   $$
   \mathcal{L}_{\mathrm{iBOT}++} = -\sum_{i=1}^{N} h_t(f_t(I)_i)^T \log h_s(f_s(I_{\mathrm{mask}})_i)
   $$
   其中 mask 比例固定为 75%（Table 12 消融实验证实该设置对整体性能和 patch-text 对齐至关重要）。这一修改直接回应了蒸馏分析中的核心发现：对所有 patch tokens 而非仅对被掩码 tokens 进行监督，是提升 patch-text 对齐的关键机制。

6. **Head-only EMA** — 大幅简化了传统的 EMA 学习设置。TIPSv2 仅在投影头 $h_t$ 上应用指数移动平均更新，而视觉编码器本身不再维护教师副本（即 $f_t = f_s$）。这一设计在 ViT-B 上减少了约 42% 的训练参数，同时保持甚至小幅提升零样本分割性能（ADE150 mIoU 从 18.1 提升至 19.1，Table 4）。

7. **多粒度标题采样** — 为第二个 CLS token 提供多样化的文本监督。训练时在详细的 Gemini 标题和简单的 PaliGemma 标题之间随机交替采样（Figure 4），增强模型对文本描述粒度变化的鲁棒性。

### 蒸馏流程（用于小模型）

对于 ViT-B、ViT-L、SO-400m 等较小模型，TIPSv2 从预训练好的 ViT-g 教师模型进行蒸馏。蒸馏过程与预训练共享相同的损失框架，但有两个关键修改：
- 教师网络 $f_t$ 被替换为冻结的大规模教师，而非 $f_s$ 的 EMA 副本；
- patch 级损失**不使用 masking**（mask ratio = 0.0），并采用随机初始化学生编码器。

Table 2 的消融实验表明，这一策略（无 masking + 随机初始化）是蒸馏出强 patch-text 对齐能力的关键：移除 masking 并将学生随机初始化后，ADE150 零样本分割 mIoU 从 5.9 跃升至 20.0（row (2) vs row (4)）。

## 核心模块与公式推导

### 3.1 预训练基础框架

TIPSv2 建立在 **TIPS**（Maninis et al., ICLR 2025）之上，该框架将对比图像-文本学习与自监督学习相结合。其核心架构包含两个编码器：一个视觉编码器（Vision Transformer, ViT）和一个文本编码器（Transformer），分别将图像和文本映射到共享嵌入空间。

总损失由三个分量加权求和构成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{CLIP}} + \alpha \mathcal{L}_{\mathrm{DINO}} + \beta \mathcal{L}_{\mathrm{iBOT}}$$

其中 $\alpha = 1.0$，$\beta = 2.0$（详见附录 A.9）。三个损失分量的作用如下：

- **$\mathcal{L}_{\mathrm{CLIP}}$**：全局对比损失，对齐图像的全局表示与文本嵌入。
- **$\mathcal{L}_{\mathrm{DINO}}$**：全局级自蒸馏损失，比较学生网络对局部裁剪的预测与教师网络对全局视图的嵌入。
- **$\mathcal{L}_{\mathrm{iBOT}}$**：Patch 级掩码图像建模（MIM）损失，仅对被掩码的 patch token 施加监督。

#### DINO 损失

$$\mathcal{L}_{\mathrm{DINO}} = - \sum_{i=1}^{M} h_t(f_t^g(I))^T \log h_s(f_s^g(I_i))$$

**变量含义**：
- $M$：局部裁剪数量
- $f_t^g(I)$：教师编码器对全局视图 $I$ 提取的全局嵌入
- $f_s^g(I_i)$：学生编码器对第 $i$ 个局部裁剪 $I_i$ 提取的全局嵌入
- $h_t, h_s$：教师和学生各自的投影头（projection head）
- 损失本质是教师全局嵌入与学生局部嵌入之间的交叉熵，强制学生从局部视角预测全局语义。

#### iBOT 损失

$$\mathcal{L}_{\mathrm{iBOT}} = - \sum_{i=1}^{N} m_i \, h_t(f_t(I)_i)^T \log h_s(f_s(I_{\mathrm{mask}})_i)$$

**变量含义**：
- $N$：patch token 总数
- $m_i \in \{0, 1\}$：掩码指示器，$m_i = 1$ 当且仅当第 $i$ 个 patch 被掩码
- $f_t(I)_i$：教师编码器对完整图像 $I$ 的第 $i$ 个 patch 嵌入
- $f_s(I_{\mathrm{mask}})_i$：学生编码器对被掩码图像 $I_{\mathrm{mask}}$ 的第 $i$ 个 patch 嵌入
- 损失仅对被掩码的 patch 施加，要求学生从被掩码的上下文中重建教师对该位置的表示。

### 3.2 蒸馏中的关键发现：从掩码到全监督

TIPSv2 的核心洞察来源于蒸馏实验。蒸馏过程与预训练类似，但有两处关键修改：
1. 教师网络 $f_t$ 替换为冻结的大模型，而非学生编码器的 EMA 副本；
2. Patch 级损失中不施加掩码（mask ratio = 0.0），即对所有 patch token 进行监督。

**Table 2** 的系统消融揭示了两个决定性因素：

| 配置 | PC59 mIoU | ADE150 mIoU |
|------|-----------|-------------|
| (1) 预训练初始化 + 冻结教师 + 掩码 | 6.9 | 0.3 |
| (2) 预训练初始化 + 冻结教师 + 无掩码 | 16.0 | 5.9 |
| (4) 随机初始化 + 冻结教师 + 无掩码 | **31.4** | **20.0** |

**关键因果链条**：
- **移除掩码**（row 1→2）：将监督从仅 masked token 扩展到所有 token，零样本分割 mIoU 出现数量级提升。
- **随机初始化学生编码器**（row 2→4）：在无掩码基础上进一步大幅提升，表明预训练权重中已固化的表示反而会阻碍蒸馏过程中的 patch-text 对齐学习。

这一发现直接催生了 iBOT++ 的设计：将对所有 patch token 的直接监督融入预训练目标，而非仅在蒸馏阶段使用。

### 3.3 iBOT++：全 Patch 监督的掩码图像建模

iBOT++ 是对 iBOT 的简洁修改——将 patch 级损失从仅 masked token 扩展到**所有 token（masked + visible）**：

$$\mathcal{L}_{\mathrm{iBOT++}} = - \sum_{i=1}^{N} h_t(f_t(I)_i)^T \log h_s(f_s(I_{\mathrm{mask}})_i)$$

**与 iBOT 的核心差异**：
- iBOT 中 $m_i$ 掩码指示器被移除，损失对所有 $N$ 个 patch token 求和。
- 学生编码器仍以被掩码图像 $I_{\mathrm{mask}}$ 为输入（保留 masking 机制），但需预测教师对**完整图像**中每个 patch 的表示——包括那些在学生视角下可见的 patch。
- 这强制模型在可见 token 上也保持与教师表示的一致性，从而显著增强 patch-text 对齐。

**Table 3** 在 ViT-g 规模上验证了 iBOT++ 的效果：将 iBOT 替换为 iBOT++ 后，零样本分割 mIoU 从 3.5 跃升至 17.6（ADE150），PC59 从 14.2 提升至 28.6。

**Figure 2** 进一步揭示了机制：iBOT++ 训练中 visible token 的 patch 级损失持续下降，表明这些 token 成功“锚定”到教师的表示；而 iBOT 中 visible token 不受监督，其损失不会下降。

### 3.4 Head-Only EMA：精简的自监督训练

传统 DINO/iBOT 框架中，教师编码器 $f_t$ 通过学生编码器 $f_s$ 的指数移动平均（EMA）更新，需维护两份完整编码器参数。TIPSv2 提出 **Head-Only EMA**：

- 视觉编码器不再使用 EMA 教师，直接设置 $f_t = f_s$（学生和教师共享同一编码器）。
- EMA 仅应用于投影头网络 $h_t$，通过 $h_s$ 的 EMA 更新 $h_t$。

**效果**：在 ViT-B 上减少约 42% 的训练参数，同时保持甚至小幅提升零样本分割性能（ADE150 mIoU 从 17.6 提升至 19.1，Table 4）。论文指出完全移除 EMA 会导致训练不稳定，投影头上的 EMA 是维持训练稳定性的最小必要组件。

### 3.5 多粒度文本增强

为提升视觉编码器对多样化文本描述的鲁棒性，TIPSv2 引入多粒度标题采样策略：

- 除基线使用的 PaliGemma 合成标题外，额外引入 **Gemini** 模型生成的更详细、更全面的图像描述（Figure 4 展示了不同粒度标题的差异）。
- 训练时对第二个 CLS token 随机交替使用 Gemini 详细标题和 PaliGemma 简洁标题。
- 该策略在 Table 4 消融中进一步将 ADE150 mIoU 从 17.6 提升至 18.1，同时改善了 Flickr 图像检索性能。

### 补充图表

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2604_12012/figures/001_Figure_1.jpg]]
*Figure 1: TIPSv2’s improvement to the masked image modeling pretraining strategy. As part of our complete TIPSv2 method, we introduce iBOT++ (bottom), a simple modification to the well-known iBOT [68] self-supervised objective (top-left), where visible tokens also contribute directly to the loss. This enhancement dramatically improves patch-text alignment, as demonstrated by zero-shot image segmentation results (top-right)*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2604_12012/figures/004_Table_2.jpg]]
*Table 2: Initialization and masking ablations for distillation. Comparing TIPS ViT-L models re-trained with different strategies. We highlight best and second-best overall. Initialization is either from scratch (“Random”) or initialized from the teacher model (“Pretrained”). Update is either training ( ) or frozen ( ). The results show that removing masking and randomly initializing the student image encoder are critical for achieving strong patch-text alignment*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2604_12012/figures/006_Table_3.jpg]]
*Table 3: Zero-shot segmentation in pretraining. Comparing TIPS ViT-g with iBOT or iBOT++ methods, showing significant improvements with our novel iBOT++*

## 实验与分析

### 核心发现：蒸馏揭示Patch-文本对齐的关键瓶颈

TIPSv2的实验设计源于一个反直觉的观察：在零样本分割任务上，蒸馏得到的小模型反而显著优于其教师模型。如Table 1所示，TIPS ViT-L（从TIPS ViT-g蒸馏而来）在PASCAL Context、VOC和ADE20K上的mIoU分别达到33.5、30.5和20.8，而教师模型ViT-g仅为11.4、19.7和2.6。这一现象暗示，标准预训练流程中的某些设计阻碍了大规模模型的patch-文本对齐能力，而蒸馏过程恰好绕过了这些障碍。

为追查根因，作者对蒸馏过程进行了系统消融（Table 2）。实验从标准蒸馏设置（冻结教师、masking比例0.75、学生从教师初始化）出发，逐步改变三个关键变量：
- **移除masking**（mask ratio 0.0）将ADE150 mIoU从0.3提升至5.9，但整体性能仍然较弱。
- **随机初始化学生**（而非从教师权重初始化）进一步将性能推至PC59 31.4、ADE150 20.0，接近最终TIPS ViT-L水平。
- **冻结学生编码器**则导致性能崩溃，表明学生必须被训练以适应该无mask监督信号。

核心结论是：**对所有patch tokens（而非仅masked tokens）施加监督，并配合随机初始化，是patch-文本对齐的关键**。这一发现直接催生了iBOT++的设计——将蒸馏中的“无mask全token监督”思想融入预训练目标。

### 主实验结果：密集与全局对齐的全面提升

TIPSv2在密集图像-文本对齐任务上展现了统治级性能。如Table 5所示，TIPSv2 L/14在所有零样本分割基准上均取得最优：PASCAL Context 37.1 mIoU（vs TIPS L/14 33.5）、PASCAL VOC 44.4（vs TIPS 30.5）、ADE20K 24.7（vs TIPS 20.8）。值得注意的是，SILC和DINOv2使用了更昂贵的滑动窗口TCL协议，而TIPSv2仅需简单的上采样即可超越它们。与SigLIP2 SO/14相比，TIPSv2在VOC21上的领先幅度高达+17.6 mIoU，进一步验证了其patch-文本对齐的优越性。

在全局图像-文本对齐任务上（Table 6），TIPSv2在7项评估中的5项取得最优或次优。在图像唯一任务上（Table 7），TIPSv2在9项评估中的7项取得最优或次优，涵盖语义分割、深度估计、表面法线预测等，展现了强大的通用视觉表征能力。

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2604_12012/figures/010_Table_6.jpg]]
*Table 6: Global image-text evaluations, where TIPSv2 achieves best or second-best in 5 out of 7 cases. We highlight the best and second-best number of each column*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2604_12012/figures/011_Table_7.jpg]]
*Table 7: Image-only evaluations, where TIPSv2 achieves the best or second-best performance in 7 out of 9 evaluations. We highlight the best and second-best number of each column*

与DINOv3的对比（Table 8）尤为关键：在最大可比规模ViT-L下，TIPSv2在6项指标中的4项领先，而DINOv3使用了更大的ViT-7B模型和20亿张精筛图像进行训练。这证明了视觉-语言联合预训练在数据效率上的优势。

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2604_12012/figures/012_Table_8.jpg]]
*Table 8: Comparison between DINOv3 and TIPSv2, on largest comparable model size ViT-L. TIPSv2 achieves superior performance on 4 out of 6 metrics. We highlight the best performing model for each task*

### 消融实验：各组件的独立贡献

Table 4以累积方式量化了TIPSv2各组件的贡献（ViT-g，100k步，分辨率224）：

- **基线TIPS**：ADE150 mIoU仅3.5，Flickr检索R@1为75.8。
- **+iBOT++**：ADE150 mIoU飙升至17.6（+14.1），证实了全token监督对patch-文本对齐的决定性作用。Flickr检索也提升至77.1。
- **+多粒度文本标题**：ADE150进一步提升至18.1，同时Flickr检索跃升至80.5。这表明丰富的文本描述不仅增强了密集对齐，也改善了全局检索。
- **+Head-only EMA**：ADE150达到19.1，Flickr检索81.6，同时训练参数量减少约42%（ViT-B上测量）。该设计在保持性能的同时显著降低了资源消耗。

关于masking比例的消融（Table 12）表明，iBOT++的最佳masking比例为75%。降低masking至50%或0%会导致零样本分割性能下降，说明保留一定程度的masking对于维持patch-文本对齐的鲁棒性至关重要。

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2604_12012/figures/015_Table_12.jpg]]
*Table 12: Masking ablation for iBOT++ pretraining. We conduct an ablation study on TIPS [33] ViT-L models to determine the optimal masking ratio for iBOT++ pretraining. The results show that 75% masking ratio is critical for achieving strong performance across all evaluations, particularly enhancing patch-text alignment. The model achieving the best overall performance is highlighted*

### 跨架构泛化：iBOT++的通用性

iBOT++并非仅适用于TIPS框架。Table 9显示，将iBOT++应用于标准CLIP（ViT-L）后，零样本分割ADE150 mIoU从iBOT的3.4提升至17.2，同时ImageNet分类和Flickr检索也有显著增益。结合head-only EMA后（Table 10），性能进一步提升至ADE150 18.0。在ViT-g规模的双CLS token设置下（Table 11），iBOT++同样带来了跨任务的全面改善。这些结果表明，iBOT++的全token监督策略是一种通用的patch-文本对齐增强方法。

### 定性分析：特征图的语义聚焦

PCA特征图可视化提供了直观的对齐质量证据。Figure 5对比了ViT-g级别的TIPS、TIPSv2和SigLIP2：TIPSv2的特征图更平滑，物体边界清晰，语义区域一致。Figure 7在ViT-L级别对比DINOv2、DINOv3和TIPSv2：DINOv3特征更平滑，但TIPSv2捕捉了更多语义聚焦的细节——例如窗户集中聚类、狗的眼睛和牵引绳清晰可辨。Figure 8在更大规模（ViT-g/7B）下进一步确认了这一趋势。零样本分割的可视化对比（Figure 6和Figure 9）直接展示了iBOT++相对于iBOT在patch-文本对齐上的质变：无需任何后处理，TIPSv2的逐patch分类结果已接近真实分割标注。

### 公平性说明与局限

论文在比较中保持了较好的公平性：SILC和DINOv2使用了更昂贵的TCL协议，但TIPSv2仍以简单上采样胜出；与DINOv3对比时使用了最大可比规模ViT-L。然而，需注意以下几点：
- TIPSv2仅在WebLI数据集上训练，数据多样性可能限制其在特定领域的表现。
- iBOT++的最佳masking比例固定为75%，该值可能依赖于特定任务和架构组合。
- 完全移除EMA会导致训练不稳定，head-only EMA仍需在投影头上保留EMA机制。
- 多粒度文本增强依赖外部模型Gemini Flash的标题质量，其性能上限受制于该模型的描述能力。

### 补充图表

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2604_12012/figures/007_Table_4.jpg]]
*Table 4: Ablation studies for TIPSv2’s pretraining technique. Ablations are cumulative, running on a fixed schedule of 100k steps at resolution 224, for fair comparisons. We highlight the best and second-best number of each column*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2604_12012/figures/009_Table_5.jpg]]
*Table 5: Dense image-text evaluations, where TIPSv2 outperforms others in all cases, even though SILC and DINOv2 use the more expensive TCL protocol [6]. We highlight the best and second-best number of each column*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2604_12012/figures/002_Table_1.jpg]]
*Table 1: Zero-shot segmentation with a large teacher model and its distilled student. Surprisingly, the TIPS ViT-L model, which is a student distilled from the TIPS ViT-g teacher, significantly surpasses it*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2604_12012/figures/014_Table_9.jpg]]
*Table 9: Applying iBOT++ to CLIP, on a ViT-L backbone. iBOT++ significantly enhances CLIP performance across several tasks, beyond what can be obtained with iBOT*

## 方法谱系与知识库定位

### 1. 方法谱系：从TIPS到TIPSv2的演进

TIPSv2并非从零构建的全新框架，而是对前代工作**TIPS**（Maninis et al., ICLR 2025）的直接继承与增强。TIPS本身已建立起一个融合对比学习与自监督学习的预训练范式，其核心损失函数由三部分组成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{CLIP}} + \mathcal{L}_{\mathrm{DINO}} + \mathcal{L}_{\mathrm{iBOT}}$$

其中 $\mathcal{L}_{\mathrm{CLIP}}$ 负责全局图像-文本对齐，$\mathcal{L}_{\mathrm{DINO}}$ 提供全局级自蒸馏，$\mathcal{L}_{\mathrm{iBOT}}$ 则承担patch级的掩码图像建模。TIPSv2保留了这一整体框架，但在三个关键组件上进行了针对性改进，形成了从“组合式预训练”到“增强型组合式预训练”的演进。

#### 1.1 iBOT → iBOT++：patch级监督范式的根本转变

最核心的改进发生在patch级自监督损失上。原始iBOT损失仅对被掩码的patch token施加监督：

$$\mathcal{L}_{\mathrm{iBOT}} = -\sum_{i=1}^{N} m_i \, h_t(f_t(I)_i)^T \log h_s(f_s(I_{\mathrm{mask}})_i)$$

其中 $m_i$ 为掩码指示器，仅当第 $i$ 个patch被掩码时才参与损失计算。TIPSv2提出的iBOT++移除了这一限制，将监督扩展到所有patch token：

$$\mathcal{L}_{\mathrm{iBOT++}} = -\sum_{i=1}^{N} h_t(f_t(I)_i)^T \log h_s(f_s(I_{\mathrm{mask}})_i)$$

这一修改看似简单，实则改变了patch级表示学习的根本机制：可见token也被强制与教师模型的对应token对齐，从而在预训练阶段就建立起更一致的局部语义表示。这一设计并非凭空产生，而是源于对蒸馏过程的深入分析——论文发现，在蒸馏中移除masking并随机初始化学生编码器能大幅提升patch-text对齐（Table 2，零样本分割mIoU从约6.9跃升至31.4）。iBOT++正是将这一蒸馏发现“翻译”回预训练目标的产物。

#### 1.2 全网络EMA → Head-only EMA：效率驱动的架构简化

TIPS继承自DINO系列的指数移动平均（EMA）机制原本需要同时维护教师编码器 $f_t$ 和学生编码器 $f_s$ 两套完整参数。TIPSv2提出仅对投影头 $h_t$ 施加EMA更新，而将编码器本身设置为 $f_t = f_s$。这一简化在ViT-B上减少了约42%的训练参数量，同时保持了零样本分割性能（甚至小幅提升至19.1 mIoU，Table 4）。需要注意的是，完全移除EMA会导致训练不稳定，因此投影头上的EMA仍是必要组件。

#### 1.3 单粒度文本 → 多粒度文本增强

TIPS使用PaliGemma合成标题作为文本监督来源。TIPSv2引入了多粒度标题策略：在训练过程中随机交替使用详细的Gemini标题和简洁的PaliGemma标题来监督第二个CLS token。这一设计旨在让视觉编码器适应不同粒度的文本描述，从而提升表示的鲁棒性。该策略在ADE150零样本分割上带来+0.5 mIoU的增益，同时改善了Flickr检索性能（Table 4）。

### 2. 在视觉-语言预训练谱系中的定位

#### 2.1 与纯对比学习方法的区别

**CLIP**（Radford et al., ICML 2021）和**SigLIP2**（Tschannen et al., arXiv 2025）代表了纯对比学习路线。这类方法仅通过图像级对比损失对齐全局表示，缺乏对patch级局部语义的显式建模。TIPSv2的独特之处在于同时维护全局对比损失和patch级自监督损失，使模型在保持强全局对齐能力的同时获得密集的局部语义理解。实验证据表明，TIPSv2 L/14在零样本分割VOC21上达到44.4 mIoU，而SigLIP2 SO/14仅为26.8（Table 5），差距高达+17.6。

值得注意的是，论文揭示了纯对比学习方法中一个反直觉的现象：在SigLIP2系列中，小模型在零样本分割上反而优于大模型（Table 14），说明大规模对比预训练可能反而损害了patch-text对齐。TIPSv2通过iBOT++显式强制所有patch token与文本空间对齐，有效规避了这一问题。

#### 2.2 与纯自监督方法的区别

**DINOv2**（Oquab et al., TMLR 2024）和**DINOv3**（Simeoni et al., arXiv 2025）代表了纯视觉自监督路线。这些方法在图像唯一任务（如语义分割、深度估计）上表现优异，但缺乏与文本模态的直接对齐能力。TIPSv2通过保留CLIP损失，在全局图像-文本检索和分类任务上保持了竞争力（Table 6，7项评估中5项最佳或次佳），同时在图像唯一任务上也取得了7/9项最佳或次佳的成绩（Table 7）。

在同等规模ViT-L下与DINOv3的对比中（Table 8），TIPSv2在4/6项指标上领先，且训练数据量更少（WebLI vs DINOv3的2B curated images）。PCA特征图定性对比显示，DINOv3的特征更平滑，但TIPSv2的特征更具语义聚焦性（Figure 7, Figure 8）。

#### 2.3 与组合式预训练方法的关系

**PE-core**（Bolya et al., arXiv 2025）同样探索了感知编码器与文本的对齐，但其具体技术路线与TIPSv2的iBOT++机制不同。TIPSv2在零样本分割上的优势（Table 5）表明，对所有patch token施加直接监督的策略在密集对齐任务上更为有效。

### 3. 适用边界与局限

#### 3.1 数据依赖性

TIPSv2的预训练仅在WebLI数据集上进行，该数据集的数据分布和多样性可能成为模型泛化能力的上限。论文未探索在其他大规模多模态数据集（如LAION、DataComp）上的训练效果，因此在不同数据分布下的表现需要进一步验证。

#### 3.2 掩码比例的超参数敏感性

iBOT++的最佳masking比例固定为75%（Table 12）。该比例对整体性能和patch-text对齐至关重要，但其最优性可能依赖于特定任务和架构。论文未系统探索不同masking比例在不同下游任务上的迁移效果，这在实际部署中可能构成调参负担。

#### 3.3 EMA机制的不可完全移除性

尽管head-only EMA大幅减少了训练参数，但完全移除EMA会导致训练不稳定。这一现象暗示EMA在自蒸馏框架中扮演着超越简单参数平滑的角色，其深层机制值得进一步研究。

#### 3.4 文本增强的外部依赖性

多粒度文本增强依赖Gemini Flash作为外部合成标题模型。标题质量直接影响视觉编码器的学习效果，因此TIPSv2的性能上限部分受限于外部模型的能力。当无法获取高质量合成标题时，该增强策略的收益可能下降。

#### 3.5 模型规模的不完全对等

在部分对比中，模型规模不完全一致（如TIPSv2 g/14约1.1B参数 vs 其他模型的ViT-G约1.8B参数）。尽管论文尽可能采用最大可比较规模，但仍需注意规模差异对公平性判断的潜在影响。

### 4. 开放问题

1. **iBOT++的适用范围**：论文展示了iBOT++应用于CLIP的消融实验（Table 9-11），证明其可独立于TIPSv2框架发挥作用。但iBOT++是否适用于其他视觉-语言架构（如BLIP系列、LLaVA系列），以及是否能在更大规模数据上保持增益，仍待探索。

2. **masking比例的自适应机制**：当前固定75%的masking比例可能不是全局最优解。是否存在基于图像内容或训练阶段动态调整masking比例的策略，值得进一步研究。

3. **蒸馏与预训练的统一理论**：论文发现蒸馏中移除masking能大幅提升对齐，并将这一发现转化为预训练中的iBOT++。但蒸馏和预训练在patch-text对齐上的内在联系尚未被完全揭示，是否存在更统一的框架来理解这两种训练范式，是值得深入的理论问题。

4. **head-only EMA的稳定性机制**：为何投影头上的EMA足以维持训练稳定而编码器上的EMA可以完全移除？这一现象可能暗示自蒸馏中的表示一致性主要通过投影头而非编码器主干来维持，其理论解释有待进一步挖掘。

## 原文 PDF

![[paperPDFs/CVPR_2026/TIPSv2_Advancing_Vision_Language_Pretraining_with_Enhanced_Patch_Text_Alignment.pdf]]
