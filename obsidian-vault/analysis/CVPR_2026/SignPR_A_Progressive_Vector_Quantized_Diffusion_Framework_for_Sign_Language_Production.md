---
title: "SignPR: A Progressive Vector-Quantized Diffusion Framework for Sign Language Production"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SignPR_A_Progressive_Vector_Quantized_Diffusion_Framework_for_Sign_Language_Production.pdf
project_link: null
code_link: null
aliases:
- SignPR
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 结构上，通过两层离散表示（语义级与区域级）与渐进扩散（先生成语义姿态序列，再以文本和语义姿态为条件细化区域运动细节）进行渐进式结构细化；时间上，引入块级因果推理（InferRef）代替完全并行扩散，逐步强制时间顺序并允许对早期生成块进行迭代修正。
primary_logic: 手语姿态生成需同时兼顾全局语义表达与局部运动精度，将生成解耦为语义级先验与区域级细化，并结合时间因果约束，可有效解决语义‑运动‑时序三重挑战。
claims:
- SignPR在PHOENIX-14T数据集上相比MoMP等基线在BLEU-1、FID、MPJPE上均取得最优结果。
- 在CSL-Daily上，SignPR在BLEU-4和MPJPE上显著优于MoMP。
- 移除区域细化或时间推理会导致生成质量明显下降，证实各部分的关键作用。
- 块级因果推理（K=8）在ROUGE上相比并行推理提升+1.36，同时保持时间连贯性。
---

# SignPR: A Progressive Vector-Quantized Diffusion Framework for Sign Language Production

> [!tip] 核心洞察
> 手语姿态生成需同时兼顾全局语义表达与局部运动精度，将生成解耦为语义级先验与区域级细化，并结合时间因果约束，可有效解决语义‑运动‑时序三重挑战。

| 字段 | 内容 |
|------|------|
| 中文题名 | SignPR：一种渐进式向量量化扩散框架用于手语生成 |
| 英文题名 | SignPR: A Progressive Vector-Quantized Diffusion Framework for Sign Language Production |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_SignPR_A_Progressive_Vector-Quantized_Diffusion_Framework_for_Sign_Language_Production_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SignPR |
| Dataset | PHOENIX-14T, CSL-Daily, USTC-CSL Split-I |

> [!tip] 效果简介
> - PHOENIX-14T 上，BLEU-1↑ 31.91 vs 16.87 (MoMP) (+15.04)；FID↓ 2.15 vs 2.97 (MoMP) (-0.82)；MPJPE↓ 23.04 vs 23.50 (Sign-IDD) (-0.46)。
> - CSL-Daily 上，BLEU-4↑ 3.01 vs 2.14 (MoMP) (+0.87)；MPJPE↓ 44.22 vs 48.24 (MoMP) (-4.02)。
> - USTC-CSL Split-I 上，ROUGE↑ 95.48 vs 25.09 (PT-GN) (+70.39)。

## 概述

手语生成（Sign Language Production, SLP）旨在将口语文本直接转化为连续的手语姿态序列，是连接聋人与听人社群的关键桥梁技术。当前文本到手语姿态（Text2Pose）方法面临一个核心瓶颈：**语义一致性、运动精度与时间连贯性难以同时保证**。具体而言，以**T2S-GPT**（Yin et al., arXiv 2024）为代表的单token帧级模型缺乏精细动作细节；以**SOKE**（Zuo et al., ICCV 2025）为代表的独立区域建模方法破坏了跨区域的语义对齐，导致组合不一致；而基于并行扩散的方法（如**G2P-DDM**, Xie et al., AAAI 2024）缺乏显式时间控制，离散token的并行更新易产生抖动和不平滑过渡。

针对上述挑战，本文提出**SignPR**——一种渐进式向量量化扩散框架，其核心洞察在于：手语姿态生成需要同时兼顾全局语义表达与局部运动精度，将生成过程解耦为语义级先验与区域级细化，并结合时间因果约束，可有效解决语义‑运动‑时序三重挑战。

SignPR的方法定位体现在三个关键设计上：**结构上**，通过双层离散表示（语义级token捕获整体动力学，四个区域级token分别建模身体、左右手和头部细节）与渐进扩散（先生成语义姿态序列，再以文本和语义姿态为条件细化区域运动）实现渐进式结构细化；**时间上**，引入块级因果推理（InferRef）代替完全并行扩散，逐步强制时间顺序并允许对早期生成块进行迭代修正，从而保证时序连贯性。

在PHOENIX-14T数据集上，SignPR取得了31.91的BLEU-1、2.15的FID和23.04的MPJPE，相比强基线**MoMP**（Saunders et al., ICCV 2021）的16.87、2.97、45.26均有显著提升（Table 1）。在CSL-Daily数据集上，BLEU-4从MoMP的2.14提升至3.01，MPJPE从48.24降至44.22（Table 2）。消融实验进一步证实，移除区域细化会导致姿态细节丢失，移除块级因果推理则引发运动不连续和抖动，验证了各模块的关键作用。

## 背景与动机

手语生成（Sign Language Production, SLP）旨在将口语文本直接转换为连续的手语姿态序列，是打破聋听沟通壁垒的关键技术。与需要中间Gloss标注的Text2Gloss2Pose（T2G2P）路线不同，Text2Pose（T2P）方法直接从文本端到端生成姿态，避免了昂贵的人工标注，因而更具实用价值。然而，现有T2P方法面临一个核心瓶颈：**难以同时保证语义一致性、运动精度和时间连贯性**。

具体而言，主流范式存在三类结构性缺陷。其一，**单token帧级模型**（如T2S-GPT，Yin et al., arXiv 2024）将每帧姿态压缩为单一离散token，虽能捕获全局语义，却丢失了手部、头部等局部区域的精细动作细节。其二，**独立区域建模方法**（如SOKE，Zuo et al., ICCV 2025）虽为不同身体部位分配独立token，但各区域独立生成破坏了跨区域语义对齐，导致组合不一致——例如左手与右手动作在语义上无法协调。其三，**并行扩散模型**（如G2P-DDM，Xie et al., AAAI 2024）一次性并行生成所有时间步的离散token，缺乏显式的时间因果约束，离散token的并行更新容易引入帧间抖动和不平滑过渡。

上述困境揭示了一个深层矛盾：手语姿态本质上是一个**全局语义表达**与**局部运动精度**强耦合的结构化时空序列。全局语义决定了“说什么”，要求整个身体姿态在语义层面保持一致；局部运动精度决定了“怎么说”，要求每个关节、每根手指的运动都准确无误。将这两个层次混为一谈进行建模，必然导致顾此失彼。

针对这一瓶颈，本文提出**SignPR**——一种渐进式向量量化扩散框架。其核心洞察是：**将手语姿态生成解耦为语义级先验与区域级细化，并引入时间因果约束，可系统性地解决语义‑运动‑时序三重挑战**。具体而言，SignPR在结构上采用双层离散表示（语义级与区域级），先生成语义姿态序列作为全局先验，再以文本和语义姿态为条件细化四个区域（身体、左手、右手、头部）的运动细节；在时间上引入块级因果推理（InferRef），将序列分块并按因果顺序逐步生成，同时允许对早期生成块进行迭代修正。这一“先粗后精、先因后果”的渐进式生成策略，从根本上改变了现有方法的建模范式。

## 核心创新

SignPR 的核心创新在于通过**渐进式结构细化**与**块级因果时序推理**两个维度，系统性地解决了现有 Text2Pose 方法中语义一致性、运动精度与时间连贯性难以兼得的瓶颈。

### 双层离散表示：语义级与区域级解耦

现有方法在姿态表示上存在两难困境：单 token 帧级模型（如 **T2S-GPT**，Yin et al., arXiv 2024）虽能保持全局语义，但缺乏对手部、头部等精细部位的运动细节刻画；而独立区域建模方法（如 **SOKE**，Zuo et al., ICCV 2025）虽能捕捉局部细节，却因各区域独立编码而破坏跨区域语义对齐，导致组合不一致。

SignPR 提出**结构向量量化变分自编码器（S-VQVAE）**，将每一帧姿态同时压缩为两个层级的离散表示：
- **语义级 token**：通过 GCN 与 Transformer 编码器捕获全身整体动力学，建模全局语义表达；
- **区域级 token**：针对 body、left hand、right hand、head 四个区域分别编码，保留精细运动细节。

两个层级之间通过**结构一致性损失** $\mathcal{L}_{cons}$ 强制对齐——语义隐变量需能预测各区域 id，从而在保持全局语义的同时不丢失局部精度。这一设计从根本上改变了离散表示的粒度结构，为后续渐进式生成奠定了基础。

### 渐进式扩散生成：从语义先验到区域细化

传统离散扩散方法（如 **G2P-DDM**，Xie et al., AAAI 2024）一次性并行生成所有 latent token，缺乏从粗到细的结构化生成过程。SignPR 将扩散过程解耦为两个阶段：

1. **语义扩散**：以文本为条件，先生成语义 id 序列 $\hat{I}_0^{se}$，确立整体姿态的语义框架；
2. **区域扩散**：以文本和已生成的语义 id 序列为双重条件，进一步预测四个区域的精细 id 序列 $\hat{I}_0^{re}$。

区域扩散 U-Net 中额外引入**区域注意力（RT）**与**语义姿态交叉注意（CA_se）**，确保各区域在细化过程中保持全局语义一致性。这一从语义先验到运动细节的渐进式生成范式，将“全局语义表达”与“局部运动精度”的矛盾转化为互补的级联优化过程。

### 块级因果推理：时间连贯性的显式约束

并行扩散模型在生成序列时缺乏显式的时间因果约束，离散 token 的并行更新易产生帧间抖动和不平滑过渡。SignPR 提出 **InferRef（渐进式块级因果推理）**，在推理阶段将序列划分为多个时间块，每块生成时仅能关注历史块和块内 token，逐步强制因果顺序。更重要的是，该策略允许对早期生成的块进行迭代修正，在保持因果性的同时缓解误差累积。

消融实验表明，块大小 $K=8$ 在 ROUGE 指标上相比完全并行推理（$K=\infty$）提升 +1.36，同时有效消除了运动不连续和抖动现象。这一推理策略无需重新训练，可即插即用于现有扩散模型，为时序生成任务提供了轻量且有效的时间约束方案。

## 整体框架

SignPR 提出了一种**渐进式向量量化扩散框架**，将手语姿态生成解耦为结构渐进与时间渐进两条主线，以同时应对语义一致性、运动精度与时间连贯性三重挑战。整体 pipeline 如图 1 所示，包含三个核心阶段：

1. **结构化 VQVAE（S‑VQVAE）**：将连续姿态序列压缩为双层离散表示——语义级 token 捕获全身动力学，四个区域级 token（身体、左手、右手、头部）捕获局部运动细节。语义编码器与区域编码器之间通过结构一致性损失强制对齐，确保全局‑局部语义耦合。

2. **结构化离散扩散（S‑Diffusion）**：采用渐进式生成策略。首先以文本为条件，通过语义扩散 U‑Net 预测语义 id 序列 $\hat{I}^{se}$；再以文本和 $\hat{I}^{se}$ 为联合条件，通过区域扩散 U‑Net 预测四个区域的 id 序列 $\hat{I}^{re}$。区域 U‑Net 中额外引入区域注意力与语义姿态交叉注意力，以维持跨区域语义一致性。

3. **块级因果推理（InferRef）**：推理时，将序列划分为大小为 K 的块，逐块生成并允许每块关注所有历史块及块内 token。该策略在强制因果顺序的同时支持对早期块的迭代修正，从而抑制并行扩散常见的抖动与不平滑过渡。最终，去噪后的语义与区域 token 序列经码本查表恢复为连续姿态嵌入，由 S‑VQVAE 解码器重建完整姿态序列。

整个框架的输入为口语文本，输出为对应的 2D 手语姿态序列；长度预测器根据文本预先确定目标帧数。图 2 展示了 S‑VQVAE 与 S‑Diffusion 的详细模块关系，图 3 进一步给出了语义与区域去噪 U‑Net 的内部结构。

### 补充图表

![[assets/figures/papers/paper_list_l1002_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_SignPR_A_Progressi/figures/002_Figure_2.jpg]]
*Figure 2: The progressive vector-quantized diffusion framework with S-VQVAE and S-Diffusion modules*

## 核心模块与公式推导

SignPR 的核心由四个模块构成：**结构化 VQVAE (S-VQVAE)**、**语义扩散 U-Net**、**区域扩散 U-Net** 以及 **块级因果推理 (InferRef)**。整体流程遵循“先语义后区域”的渐进式扩散范式。

### 3.1 S-VQVAE：双层离散表示

S-VQVAE 将连续姿态序列 $\mathbf{X} = \{ x^s \}_{s=1}^{S}$（每帧 $x^s \in \mathbb{R}^{J \times 2}$ 为 $J$ 个关键点的 2D 坐标）压缩为两层离散 token 序列：**语义级 id** 和 **区域级 id**。区域集定义为 $\mathcal{P} := \{ \mathrm{body}, \text{right hand}, \text{left hand}, \text{head} \}$。

**语义编码器** 由一层 GCN 和两层 Transformer 组成，提取整帧动力学特征；**四个区域编码器** 各自包含 GCN 与 Transformer，聚焦对应身体部位的精细运动。语义隐变量 $z^{se,s}$ 通过最近邻查找映射到语义码本 $\mathcal{C}^{se}$：

$$i^{se,s} = \arg\min_j \| z^{se,s} - \mathcal{C}_j^{se} \|_2 \quad (1)$$

四个区域隐变量同理映射到各自区域码本，得到 $i^{p,s}$。

**结构一致性损失** $\mathcal{L}_{cons}$ 从语义隐变量 $\hat{z}^{se,s}$ 预测区域 id，强制两层表示对齐：

$$\mathcal{L}_{cons} = \frac{1}{S}\sum_{s=1}^{S}\sum_{p\in\mathcal{P}}\mathcal{L}_{CE}\big(\phi_p(\hat{z}^{se,s}), i^{p,s}\big) \quad (2)$$

其中 $\phi_p$ 为区域 $p$ 的线性预测头，$\mathcal{L}_{CE}$ 为交叉熵损失。S-VQVAE 的总训练损失为：

$$\mathcal{L}_{total} = \mathcal{L}_{recon} + \lambda_{cons} \mathcal{L}_{cons} + \mathcal{L}_{commit} + \mathcal{L}_{quant} \quad (3)$$

包含重建 L1 损失、结构一致性损失、编码器承诺损失与码本量化损失。

### 3.2 S-Diffusion：渐进式离散扩散

S-Diffusion 分两阶段生成姿态 token 序列：先以文本 $c$ 为条件预测语义 id 序列 $\hat{I}_0^{se}$，再以文本和 $\hat{I}_0^{se}$ 为条件预测区域 id 序列 $\hat{I}_0^{re}$。序列长度由轻量两层 Transformer 长度预测器根据文本给出。

**语义扩散 U-Net** 每个 block 包含时序自注意力 (TA)、文本交叉注意力 (CA) 和前馈网络 (FFN)，均配备自适应层归一化 (AdaLN)：

$$z_t^{se} \gets z_t^{se} + \text{AdaLN}\big(\text{TA}(z_t^{se}, t^{se})\big)$$
$$z_t^{se} \gets z_t^{se} + \text{AdaLN}\big(\text{CA}(z_t^{se}, c)\big)$$
$$z_t^{se} \gets z_t^{se} + \text{AdaLN}\big(\text{FFN}(z_t^{se})\big)$$

最终预测原始语义 id 序列：

$$\hat{I}_0^{se} = \phi_g(I_t^{se}, t^{se}, c) \quad (4)$$

**区域扩散 U-Net** 在语义 U-Net 基础上额外引入 **区域注意力 (RT)** 和 **语义姿态交叉注意力 (CA_se)**，以 $\hat{I}_0^{se}$ 为条件保持全局一致性：

$$\hat{I}_0^{re} = \phi_l(I_t^{re}, t^{re}, c, \hat{I}_0^{se}) \quad (6)$$

消融实验证实，交叉注意力 (CA) 是集成语义姿态条件的最优方式，优于拼接和加法（Table 7）。

![[assets/figures/papers/paper_list_l1002_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_SignPR_A_Progressi/figures/012_Table_7.jpg]]
*Table 7: Effect of regional diffusion conditioning*

### 3.3 InferRef：块级因果推理

标准 VQ-Diffusion 采用完全并行去噪，缺乏时间因果约束，易产生抖动。InferRef 将序列按块大小 $K$ 分块，每块生成时仅关注历史块及块内 token，逐步强制因果顺序。该策略无需重新训练，并允许对早期生成块进行迭代修正。实验表明 $K=8$ 在 ROUGE 上达到最优 32.86，相比并行推理（$K=\infty$）提升 +1.36（Table 8）。

**推理流程**：语义扩散和区域扩散均应用 InferRef 后，得到最终去噪 token 序列 $\hat{I}_0^{se}$ 和 $\hat{I}_0^{re}$，通过码本查找映射回语义嵌入和区域嵌入，经 S-VQVAE 解码器重建为连续姿态序列。

## 实验与分析

### 主实验结果

SignPR在三个主流手语生成基准上均取得了最优性能，验证了渐进式向量量化扩散框架的有效性。

**PHOENIX-14T数据集**（Table 1）：SignPR在语义质量和运动精度上全面超越现有方法。BLEU-1达到31.91，相比最强T2P基线MoMP（Saunders et al., ICCV 2021）的16.87提升+15.04；FID降至2.15（MoMP为2.97），表明生成姿态的分布更接近真实数据；MPJPE降至23.04，略优于Sign-IDD（Tang et al., AAAI 2025）的23.50。值得注意的是，SignPR作为纯Text2Pose方法，在BLEU-1上甚至超过了部分依赖Gloss中间表示的T2G2P方法，证实了直接文本到姿态建模的潜力。

**CSL-Daily数据集**（Table 2）：在中文手语场景下，SignPR的BLEU-4达到3.01（MoMP为2.14），MPJPE降至44.22（MoMP为48.24），降幅达-4.02mm。该数据集词汇量更大、表达更复杂，SignPR的双层离散表示有效缓解了语义-运动解耦不足的问题。

**USTC-CSL数据集**（Table 3）：在Split-I设定下，SignPR的ROUGE达到95.48，相比渐进式Transformer基线PT-GN（Saunders et al., ECCV 2020）的25.09提升+70.39，幅度极为显著。这得益于语义级token对整体动力学的有效捕捉，以及区域级token对精细动作的补充。

### 消融实验

消融实验系统性地验证了SignPR各核心组件的贡献。

**结构化VQVAE的作用**（Table 4 & Table 5）：S-VQVAE的重建质量是生成性能的上限。Table 4显示，语义+区域双层结构（带独立区域码本）的重建ROUGE（rROUGE）显著优于单一语义层或共享区域码本的变体。Table 5进一步表明，用Transformer替换GCN编码器会导致ROUGE下降，证明GCN对人体骨骼图结构的归纳偏置在手语姿态建模中不可或缺。移除结构一致性损失$\mathcal{L}_{cons}$同样造成性能损失，验证了语义-区域对齐约束对跨层级信息传递的关键作用。

**渐进式扩散的贡献**（Table 6）：移除区域细化分支（即仅使用语义扩散生成姿态）后，生成结果仅保留粗略的整体结构，但丢失了手部、头部等精细动作细节（定性对比见Figure 5）。定量上，该变体在所有指标上均明显劣于完整SignPR，证实区域级扩散对运动精度的必要性。

**条件集成方式**（Table 7）：在区域扩散中，以交叉注意力（CA）将语义姿态条件$\hat{I}_0^{se}$集成到去噪U-Net的效果最佳，优于拼接和加法。这表明交叉注意力能更灵活地建模语义先验与区域细节之间的非线性依赖关系。

**块级因果推理**（Table 8）：完全并行去噪（$K=\infty$，即无因果约束）导致生成序列出现明显的运动不连续和抖动（Figure 6定性展示）。引入块级因果推理后，时间连贯性显著改善。块大小$K=8$在ROUGE上达到最优32.86，相比并行推理提升+1.36；过小的$K$限制了上下文建模能力，过大的$K$则削弱因果约束的效果。

### 关键图表结论

- **Table 1 & Table 2**：SignPR在PHOENIX-14T和CSL-Daily上均以显著优势超越MoMP等强基线，在语义保真度（BLEU）和运动精度（MPJPE）两个维度上同时取得最优。
- **Table 5 & Table 6**：GCN编码器、结构一致性损失、区域细化分支三者缺一不可，任意组件的移除均导致生成质量明显下降。
- **Table 8 & Figure 6**：块级因果推理是解决离散扩散模型时间不连贯问题的有效手段，$K=8$在语义质量和时序平滑性之间取得最佳平衡。
- **Figure 5 & Figure 7**：定性可视化直观展示了区域细化对姿态细节（尤其是手部动作）的贡献，以及SignPR相比MoMP在整体运动质量上的优势。

![[assets/figures/papers/paper_list_l1002_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_SignPR_A_Progressi/figures/005_Table_1.jpg]]
*Table 1: Comparison of SLP performance on the PHOENIX-14T dataset*

![[assets/figures/papers/paper_list_l1002_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_SignPR_A_Progressi/figures/006_Table_2.jpg]]
*Table 2: Comparison of SLP performance on the CSL-Daily*

![[assets/figures/papers/paper_list_l1002_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_SignPR_A_Progressi/figures/007_Figure_5.jpg]]
*Figure 5: Visualization results with/without regional refinement*

![[assets/figures/papers/paper_list_l1002_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_SignPR_A_Progressi/figures/009_Figure_6.jpg]]
*Figure 6: Visualization results with/without temporal refinement*

![[assets/figures/papers/paper_list_l1002_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_SignPR_A_Progressi/figures/010_Figure_7.jpg]]
*Figure 7: Qualitative comparison of generated poses from SignPR, the variant (w/o regional) of SignPR and MoMP*

![[assets/figures/papers/paper_list_l1002_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_SignPR_A_Progressi/figures/011_Table_5.jpg]]
*Table 5: Effect of components in proposed S-VQVAE*

![[assets/figures/papers/paper_list_l1002_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_SignPR_A_Progressi/figures/013_Table_8.jpg]]
*Table 8: Ablation on the block-wise causal inference*

![[assets/figures/papers/paper_list_l1002_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_SignPR_A_Progressi/figures/015_Table_6.jpg]]
*Table 6: Effect of structural diffusion on generation quality. Note: ✓∗ indicates using shared regional codebook across regions*

### 已知局限与开放问题

尽管SignPR在多个基准上表现优异，仍存在以下待验证和待改进的方向：

1. **模态局限性**：当前验证仅限于2D姿态生成，3D姿态生成或端到端视频生成场景下的有效性尚未评估。
2. **块大小自适应**：块大小$K=8$为手动设定，缺乏对序列长度的自适应机制，可能限制不同时长手语序列的最优推理。
3. **大规模词汇泛化**：在多语种或超大规模词汇场景下，语义和区域码本的容量需求及泛化能力有待进一步验证。
4. **推理效率**：渐进式扩散和块级因果推理增加了推理步骤，实时性表现尚未讨论，可能成为实际部署的瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l1002_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_SignPR_A_Progressi/figures/008_Table_3.jpg]]
*Table 3: Comparison of SLP performance on the USTC-CSL*

![[assets/figures/papers/paper_list_l1002_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_SignPR_A_Progressi/figures/014_Table_4.jpg]]
*Table 4: Effect of structural VQVAE on reconstruction quality. Note: Metrics with prefix ’r’ reflect VQVAE reconstruction quality. ’✓*’ indicates shared regional codebook across regions*

## 方法谱系与知识库定位

### 1. 问题定位：语义‑运动‑时序的三重瓶颈

手语生成（Sign Language Production, SLP）中的文本到姿态（Text2Pose, T2P）任务长期面临一个核心瓶颈：如何同时保证**语义一致性**（生成的姿态序列能准确表达文本含义）、**运动精度**（手部、肢体等局部细节准确）和**时间连贯性**（动作过渡平滑自然）。现有方法往往只能顾及其中一到两个方面，导致整体生成质量受限。

具体而言，三类代表性方案各自存在结构性缺陷：

- **单token帧级建模**（如 **T2S-GPT**, Yin et al., arXiv 2024）将每帧姿态压缩为单个离散token，虽能保持时序连贯，但单一token难以承载手语中左右手独立运动、头部姿态等精细空间细节，导致运动精度不足。
- **独立区域建模**（如 **SOKE**, Zuo et al., ICCV 2025）为不同身体区域分配独立token以增强细节表达，但区域间缺乏显式的语义对齐约束，容易产生左右手动作不协调、肢体与头部语义不一致等组合错误。
- **并行扩散生成**（如 **G2P-DDM**, Xie et al., AAAI 2024；**Sign-IDD**, Tang et al., AAAI 2025）采用离散扩散模型一次性并行预测所有帧的latent token，虽能捕获全局上下文，但缺乏显式的时间因果约束，离散token的并行独立更新易导致相邻帧间出现抖动和不平滑过渡。

SignPR的核心洞察在于：手语姿态生成需要将全局语义表达与局部运动精度解耦处理，并引入时间因果约束来保证连贯性。这一洞察直接催生了其“结构‑时间”双重渐进细化框架。

### 2. 方法谱系中的位置：渐进式离散扩散

SignPR在方法谱系中处于**离散扩散生成模型**与**层次化人体运动建模**的交汇点，其直接对话的基线体系如下表所示：

| 方法 | 范式 | 离散表示粒度 | 生成顺序 | 时间约束 |
|------|------|-------------|---------|---------|
| **MoMP** (Saunders et al., ICCV 2021) | 混合运动基元 | 连续基元组合 | 自回归 | 隐式（自回归） |
| **T2S-GPT** (Yin et al., arXiv 2024) | 自回归VQ | 单token/帧 | 逐帧自回归 | 显式因果 |
| **G2P-DDM** (Xie et al., AAAI 2024) | 离散扩散 | 单token/帧 | 完全并行 | 无 |
| **SOKE** (Zuo et al., ICCV 2025) | 检索增强VQ | 区域token（无全局一致性） | 逐帧自回归 | 显式因果 |
| **Sign-IDD** (Tang et al., AAAI 2025) | 离散扩散 | 图标解耦 | 完全并行 | 无 |
| **SignPR** (本文) | 渐进式离散扩散 | 双层（语义级+区域级） | 语义→区域渐进 | 块级因果 |

SignPR相对于上述基线做出了三个关键的结构性改变：

**（1）离散表示层级：从单层到双层语义‑区域解耦**

基线方法（T2S-GPT、G2P-DDM）使用单一token表示整帧姿态，SOKE虽引入区域token但缺乏全局语义一致性约束。SignPR提出**结构化VQVAE（S-VQVAE）**，将每帧姿态编码为两个层级：
- **语义级token** $i^{se,s}$：捕获全身整体动力学，码本大小 $K^{se}$；
- **四个区域级token** $i^{p,s}, p \in \{\text{body}, \text{right hand}, \text{left hand}, \text{head}\}$：分别捕获各区域的精细运动细节。

两层之间通过**结构一致性损失** $\mathcal{L}_{cons}$ 强制对齐——语义隐变量需能预测对应区域的离散id，从而保证全局语义与局部细节的结构化对应关系。

**（2）生成顺序：从并行到语义先验→区域细化的渐进式扩散**

G2P-DDM和Sign-IDD采用完全并行的扩散去噪，所有帧的所有token同时更新。SignPR将扩散过程解耦为两个阶段：
- **语义扩散**：先以文本 $c$ 为条件，预测语义token序列 $\hat{I}_0^{se}$，建立全局语义骨架；
- **区域扩散**：再以文本 $c$ 和已生成的语义序列 $\hat{I}_0^{se}$ 为联合条件，预测四个区域的token序列 $\hat{I}_0^{re}$。

这种“先全局后局部”的渐进策略使区域生成有了明确的语义锚点，有效避免了独立区域建模中的组合不一致问题。

**（3）时间推理：从完全并行到块级因果推理（InferRef）**

标准VQ-Diffusion在推理时对所有token进行完全并行的迭代去噪，缺乏时间因果约束。SignPR提出**InferRef**策略：将序列按时间分为大小为 $K$ 的块，每块的生成以所有历史块为条件（因果掩码），块内token则可并行去噪。这一策略在不重新训练模型的前提下，通过推理时的结构化注意力掩码逐步强制时间因果顺序，并允许对早期生成块进行迭代修正，从而消除并行扩散中的时序抖动。

### 3. 适用边界与局限

尽管SignPR在多个基准上取得了显著提升，其方法设计仍存在若干适用边界和未验证场景：

- **姿态维度局限**：当前验证仅限于2D姿态序列，3D姿态生成或端到端的视频生成（从文本直接生成手语视频）尚未评估。2D到3D的扩展需要处理深度模糊和更复杂的运动学约束，S-VQVAE的双层结构能否直接迁移尚不确定。
- **块大小自适应缺失**：InferRef的块大小 $K$ 目前为手动设定的超参数（实验中最优值为 $K=8$），缺乏根据序列长度或内容复杂度的自适应调整机制。对于极长或极短的手语序列，固定块大小可能导致因果约束过强或过弱。
- **多语种与词汇量扩展**：实验主要在PHOENIX-14T（德语手语）和CSL-Daily/USTC-CSL（中国手语）上进行，语义和区域码本的大小（$K^{se}$、$K^{re}$）针对特定数据集调优。当面对更大词汇量或多语种混合场景时，码本的表示能力和泛化性有待验证。
- **推理效率未讨论**：渐进式扩散（语义+区域两次扩散过程）加上InferRef的块级迭代推理，相比单次并行扩散（如G2P-DDM）增加了推理步骤和计算开销。论文未提供推理延迟的定量分析，实时应用场景下的可行性存疑。

### 4. 开放问题与后续方向

基于SignPR的设计逻辑和未覆盖场景，以下开放问题值得后续工作关注：

1. **自适应块大小机制**：能否设计一个轻量级的长度预测器或内容复杂度估计器，在推理时动态决定最优块大小 $K$，以平衡不同长度序列的因果约束强度与生成效率？
2. **3D姿态与视频端到端生成**：将S-VQVAE扩展到3D骨架（如增加深度维度的码本或采用图卷积的3D变体），并探索从离散姿态token直接解码视频帧的可能性，是通向实用手语生成系统的关键一步。
3. **跨语种泛化与码本共享**：在多语种手语数据上训练时，语义级码本是否可以在语种间共享（部分手语语义具有跨文化共性），而区域级码本需要语种特定？这涉及码本架构的重新设计。
4. **推理效率优化**：能否通过知识蒸馏将两阶段渐进扩散合并为单阶段条件生成，或设计缓存机制复用语义扩散的中间特征，以减少区域扩散的计算冗余？
5. **与Gloss监督的融合**：当前SignPR工作于纯Text2Pose设定（无Gloss中间表示），但手语生成领域存在大量Gloss标注数据。如何将Gloss作为可选的辅助条件融入渐进扩散框架（例如在语义扩散阶段引入Gloss交叉注意力），以进一步提升语义对齐精度，是一个自然的扩展方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/SignPR_A_Progressive_Vector_Quantized_Diffusion_Framework_for_Sign_Language_Production.pdf]]
