---
title: "Omni-Supervised Motion Editing: Balancing Change and Invariance through Positive-Negative Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Omni_Supervised_Motion_Editing_Balancing_Change_and_Invariance_through_Positive_Negative_Learning.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Shi_Omni-Supervised_Motion_Editing_Balancing_Change_and_Invariance_through_Positive-Negative_Learning_CVPR_2026_paper.html
project_link: null
code_link: https://github.com/rocket-ycyer/OmniME.git
aliases:
- OSMEBCITPNL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 正/负双分支监督（Positive/Negative Supervision）及其构成的三个组件：回顾性特征监督（多级DiT中间层监督）、运动保留机制（基于MotionSNR的加权保留损失）和三元组语义对齐（拉近正文本、推远负文本的对比损失）。
primary_logic: 将运动编辑形式化为同时施加正向修改约束和负向语义对齐约束的全监督学习问题；通过特征级（回顾性监督）、运动级（保留损失）和语义级（三元组损失）的多层监督，显式平衡变化与不变性。
claims:
- OmniME在MotionFix数据集上AvgR从20.88降至13.06，在STANCE Adjustment上从29.05降至22.77，均大幅超越先前方法。
- 消融研究（Table 3）表明，三个组件（回顾性监督、运动保留、三元组损失）均对性能有贡献，三者结合达到最佳。
- 定性比较（Figure 3, 4）显示OmniME在语义一致性、运动平滑性和源运动保留方面均优于SimMotionEdit。
- MotionFix 上 AvgR (lower is better) = 13.06
---

# Omni-Supervised Motion Editing: Balancing Change and Invariance through Positive-Negative Learning

> [!tip] 核心洞察
> 将运动编辑形式化为同时施加正向修改约束和负向语义对齐约束的全监督学习问题；通过特征级（回顾性监督）、运动级（保留损失）和语义级（三元组损失）的多层监督，显式平衡变化与不变性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 全监督正负学习运动编辑：平衡变化与不变性 |
| 英文题名 | Omni-Supervised Motion Editing: Balancing Change and Invariance through Positive-Negative Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Shi_Omni-Supervised_Motion_Editing_Balancing_Change_and_Invariance_through_Positive-Negative_Learning_CVPR_2026_paper.html) · [Code](https://github.com/rocket-ycyer/OmniME.git) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | OmniME |
| Dataset | MotionFix, STANCE Adjustment |

> [!tip] 效果简介
> - MotionFix 上，AvgR (lower is better) 13.06 vs 20.88 (previous best) (-7.82)。
> - STANCE Adjustment 上，AvgR (lower is better) 22.77 vs 29.05 (previous best) (-6.28)。

## 概要

**问题瓶颈**：文本驱动的人体运动编辑任务中，现有方法难以在依据自然语言指令精确修改目标区域的同时，保持未编辑区域的运动一致性。其根本原因在于缺乏对编辑区域与保留区域的显式区分机制，导致运动扭曲和语义对齐不佳。

**核心洞察**：本文提出**全监督正负学习框架 OmniME**，将运动编辑形式化为同时施加正向修改约束与负向语义对齐约束的学习问题。该方法通过三个互补组件的协同——**回顾性特征监督**（多级 DiT 中间层监督）、**运动保留机制**（基于 MotionSNR 的加权保留损失）和**三元组语义对齐**（拉近正文本、推远负文本的对比损失）——在特征级、运动级和语义级三个层次上显式平衡“变化”与“不变性”。

**方法定位**：OmniME 的架构以 Fusion Transformer 融合源动作与文本特征，经 8 块 DiT 组成的去噪网络生成目标运动。相比仅依赖最终层监督的 **SimMotionEdit**（Li et al., CVPR 2025），OmniME 在第 2、4、6 个 DiT 块引入回顾性特征监督以稳定训练；相比无显式高/低变化筛选的保留策略，OmniME 通过 MotionSNR 识别细微变化样本并选择性施加保留损失；相比可能缺乏负样本监督的语义对齐方式，OmniME 采用三元组损失同时拉近正样本、推远负样本。

**主要结果**：在 MotionFix 数据集上，OmniME 将 AvgR 从此前最优的 20.88 降至 **13.06**（降幅 7.82）；在 STANCE Adjustment 数据集上，AvgR 从 29.05 降至 **22.77**（降幅 6.28），均大幅超越先前方法。消融实验证实三个组件各自贡献且联合使用达到最佳性能。用户感知研究进一步表明，OmniME 在语义对齐、运动保留、过渡平滑性和整体自然度四个维度上均优于 SimMotionEdit。

**核心瓶颈：文本驱动运动编辑中的“变化-不变性”失衡**

文本驱动的人体运动编辑旨在根据自然语言指令修改给定的源运动序列，同时保持未编辑区域的运动完整性。这一任务的核心困难在于：现有方法难以在“依据指令修改目标区域”与“保持未编辑区域不变”之间取得精确平衡。具体而言，当前方法缺乏对编辑区域与保留区域的显式区分机制，导致两个典型问题——**运动扭曲**（未指定修改的关节或帧发生非预期变化）和**语义对齐不佳**（生成运动未能准确反映文本指令的语义意图）。这一瓶颈使得编辑结果在物理合理性和用户意图一致性上均存在明显不足。

**现有方法的局限**

当前运动编辑方法可大致分为两类：一类以 **MDM**（Tevet et al., ICLR 2023）为代表的纯扩散生成模型，虽能根据文本生成运动，但缺乏对源运动信息的有效利用，难以保证未编辑区域的保真度；另一类方法如 **TMED** 和 **SimMotionEdit**（Li et al., CVPR 2025）引入了源运动条件，但在监督信号设计上仍存在结构性缺陷——它们通常仅依赖最终层的生成损失，或使用单一的相似性预测辅助监督，未能从多层级、多语义角度同时约束“变化”与“不变性”。这导致模型在面对细微编辑需求时容易过度修改，而在需要显著语义变化时又难以充分响应文本指令。

**本文动机：将运动编辑形式化为全监督正负学习问题**

为从根本上解决上述失衡问题，本文提出将运动编辑重新定义为一种**全监督正负学习（Omni-Supervised Positive-Negative Learning）**问题。其核心思想是：编辑过程应同时接受“正向修改约束”（驱使目标区域向文本指令对齐）和“负向不变性约束”（抑制非目标区域的非预期变化），并通过**特征级、运动级和语义级**三个层次的显式监督实现这一平衡。这一框架不再将运动编辑视为简单的条件生成，而是将其建模为在正样本（应发生的改变）和负样本（应避免的改变）之间进行对比学习的结构化任务，从而为平衡变化与不变性提供了系统性的解决方案。

## 核心方法与创新机理

### 问题瓶颈与创新动机

文本驱动的运动编辑面临一个核心矛盾：如何在依据自然语言指令修改目标区域的同时，保持未编辑区域的运动一致性。现有方法（如 **SimMotionEdit** (Li et al., CVPR 2025)、**TMED** 等）缺乏对编辑区域与保留区域的显式区分机制，导致两个典型失败模式——要么过度修改破坏源运动的整体结构，要么修改不足无法满足文本指令的语义要求。这一瓶颈的根源在于，现有方法将运动编辑隐含地视为单向的“修改”任务，而忽略了“不修改”同样需要主动的监督信号。

OmniME 的核心洞察是将运动编辑重新形式化为一个**全监督的正负学习问题**：正向约束确保编辑区域与文本指令对齐，负向约束确保未编辑区域与源运动保持一致。这种“变化与不变性”的显式平衡，构成了方法设计的底层逻辑。

### 相对 Baseline 的关键创新点

OmniME 在三个关键维度上对现有框架进行了系统性改进，形成了互为补充的监督体系。

**创新点一：回顾性特征监督（Retrospective Feature Supervision）**

现有方法（包括 SimMotionEdit）仅在扩散 Transformer（DiT）的最终层施加预测损失，中间层缺乏直接的监督信号，导致深层梯度传播不稳定、中间表示容易偏离目标运动分布。OmniME 在第 2、4、6 个 DiT 块上附加轻量预测头，将隐藏表示映射回运动空间，并与目标运动计算重建损失：

$$\mathcal{L}_{\mathrm{retro}} = \sum_{l \in \{2,4,6\}} \lambda_l \mathcal{L}^{(l)}, \quad \mathcal{L}^{(l)} = \frac{1}{BTJ} \sum_{b,t} \| \hat{\mathbf{x}}_{b,t}^{(l)} - \mathbf{x}_{b,t} \|_2^2$$

这一设计的因果机制在于：中间层监督迫使网络在去噪过程中更早地形成与目标一致的特征表示，从而提升训练稳定性和最终生成质量。消融实验（Table 3）证实，移除该组件会导致检索性能显著下降。

**创新点二：基于 MotionSNR 的运动保留机制（Motion Preservation Mechanism）**

此前的保留损失通常不加区分地应用于所有样本，忽略了不同编辑样本在“变化程度”上的本质差异——对于需要大幅修改的样本施加过强的保留约束反而会损害编辑效果。OmniME 引入 MotionSNR（运动信噪比）作为自适应触发机制：

$$\mathrm{MotionSNR} = \frac{\sum_{x \in T^{R}} x}{\sum_{x \in B^{R}} x}$$

MotionSNR 按帧相似度排序后，取前 κ 帧相似度之和与后 κ 帧相似度之和的比值。高 MotionSNR 值表示运动仅发生细微变化（源-目标高度相似），此时施加保留损失既能强化运动结构保持，又不会干扰必要的编辑。保留损失仅在 MotionSNR 超过阈值 τ 时激活：

$$\mathcal{L}_{\mathrm{presv}} = \mathbb{I}(\mathbf{MotionSNR}(\mathbf{x}, \mathbf{m}) > \tau) \cdot \frac{1}{T} \sum_{i=1}^{T} \| m_i - x_i \|_2^2$$

这一条件化机制使得保留监督从“无差别约束”升级为“自适应聚焦”，集中学习细微变化场景下的运动保持能力。

**创新点三：三元组语义对齐（Triplet-based Semantic Alignment）**

现有方法的语义对齐通常仅依赖正向文本条件（即编辑指令），缺乏对“不应出现的运动语义”的显式排斥。OmniME 引入三元组损失，同时利用正文本（编辑指令）和负文本（随机采样的其他指令），在嵌入空间中拉近运动与正文本、推远运动与负文本：

$$\mathcal{L}_{\mathrm{triplet}} = \frac{1}{B} \sum_{i=1}^{B} [ \| \mathbf{z}_m^i - \mathbf{z}_p^i \|_2^2 - \| \mathbf{z}_m^i - \mathbf{z}_n^i \|_2^2 + \alpha ]_+$$

这一设计的因果机制是：负文本提供了“语义排斥力”，迫使模型学习更精细的运动-文本对应关系，而非仅仅满足于正向条件匹配。消融实验（Table 3）表明，三元组损失的加入能持续提升检索性能，验证了负向语义监督在运动编辑中的必要性。

### 创新协同与因果链路

三个创新点并非孤立设计，而是形成了从特征级、运动级到语义级的**多层监督体系**：回顾性特征监督在中间层稳定特征表示，为后续的保留和语义约束提供可靠的表示基础；MotionSNR 条件化的保留损失在运动层面保护源结构；三元组损失在语义层面强化编辑精度。三者共同作用于总损失函数：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{diff}} + \lambda_{\mathrm{cls}} \mathcal{L}_{\mathrm{cls}} + \lambda_{\mathrm{retro}} \mathcal{L}_{\mathrm{retro}} + \lambda_{\mathrm{preserve}} \mathcal{L}_{\mathrm{preserve}} + \lambda_{\mathrm{triplet}} \mathcal{L}_{\mathrm{triplet}}$$

消融实验的因果验证（Table 3）表明：移除任一组件均导致性能退化，三者结合达到最佳（MotionFix 测试集 R@1: 32.02），证实了多层监督的互补性。定性比较（Figure 3, 4）进一步显示，OmniME 在语义一致性、运动平滑性和源运动保留三个维度上均优于 SimMotionEdit，验证了“正负学习”框架在平衡变化与不变性方面的有效性。

OmniME 将文本驱动的人体运动编辑形式化为一个**全监督正负学习（Omni-Supervised Positive-Negative Learning）**问题，其核心目标是：给定源运动序列和自然语言编辑指令，生成既忠实于文本语义修改、又最大限度保留未编辑区域运动结构的目标运动。框架的设计瓶颈在于**显式区分“需要改变的区域”与“必须保持不变的区域”**，并通过多层监督信号在变化与不变性之间取得平衡。

### 信息流与模块协作

整个 pipeline 的信息流可概括为“编码-融合-去噪-多级监督”四阶段，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_Omni_Supervised_Mo/figures/002_Figure_2.jpg]]
*Figure 2: Overview of OmniME: Unified Framework for Human Motion Editing. The source motion and text are first fed into a Fusion Transformer to integrate information and then passed through the Diffusion Transformer (DiT) for denoising and prediction. In Section 3.3, we compute source-target similarity scores and supervise motions with subtle changes. In Section 3.4, multiple intermediate outputs from the transformer blocks are supervised. In Section 3.5, both positive and negative texts are used to enforce contrastive supervision between motion and text. Finally, the main diffusion loss is applied to supervise the overall generation*

1. **运动与文本编码**：源运动序列以 207 维逐帧表示 $\mathbf{x}_i = [\mathbf{v}_i, \mathbf{o}_i, \mathbf{r}_i, \mathbf{p}_i]$ 输入（含全局速度、全局朝向、关节旋转和局部关节位置），文本指令通过 CLIP 编码器提取语义嵌入。两者分别形成运动 token 和文本 token。

2. **Fusion Transformer**：运动 token 与文本 token 在此模块中进行跨模态融合，生成联合表示。该模块的作用是为后续去噪网络提供已整合文本语义与运动结构信息的统一特征，而非简单的拼接。

3. **Diffusion Transformer (DiT)**：融合后的表示进入由 8 个顺序 DiT 块组成的去噪网络。DiT 是核心生成模块，负责从噪声中逐步恢复目标运动序列。与仅依赖最终层输出的方法不同，OmniME 在 DiT 的**第 2、4、6 块**上附加轻量预测头，将中间层隐藏表示映射回运动空间，形成**回顾性特征监督（Retrospective Feature Supervision）**信号。

4. **多级监督分支**：框架在三个层级施加约束——
   - **特征级**：回顾性监督损失 $\mathcal{L}_{\mathrm{retro}} = \sum_{l \in \{2,4,6\}} \lambda_l \mathcal{L}^{(l)}$，鼓励中间层表示与目标运动一致；
   - **运动级**：运动保留损失 $\mathcal{L}_{\mathrm{presv}}$，由 MotionSNR 计算器筛选高相似度样本后触发，强调在细微变化场景中保持源运动结构；
   - **语义级**：三元组损失 $\mathcal{L}_{\mathrm{triplet}}$，同时拉近运动嵌入与正文本嵌入、推远与负文本嵌入的距离。

### 正负学习的因果机制

框架的因果 knob 在于**正/负双分支监督**的协同设计：

- **正向监督（Positive Supervision）**：通过运动保留损失，对 MotionSNR 超过阈值 $\tau$ 的样本施加逐帧重建约束，确保编辑仅发生在文本指令指定的区域，未编辑区域保持源运动结构。MotionSNR 定义为帧相似度排序后前 $\kappa$ 帧之和与后 $\kappa$ 帧之和的比值——高值意味着运动仅发生细微变化，此时保留监督最为关键。

- **负向监督（Negative Supervision）**：三元组损失显式引入负文本样本，将运动嵌入推离不相关语义，避免编辑结果漂移到与指令无关的运动模式。这与仅使用正文本对齐的方法形成本质区别。

- **回顾性监督（Retrospective Supervision）**：作为正向监督的补充，在 DiT 中间层施加预测损失，缓解深层网络中的梯度消失问题，提升训练稳定性和生成质量。

最终，所有监督信号通过加权求和统一为总损失：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{diff}} + \lambda_{\mathrm{cls}} \mathcal{L}_{\mathrm{cls}} + \lambda_{\mathrm{retro}} \mathcal{L}_{\mathrm{retro}} + \lambda_{\mathrm{preserve}} \mathcal{L}_{\mathrm{preserve}} + \lambda_{\mathrm{triplet}} \mathcal{L}_{\mathrm{triplet}}$$

### 与现有 pipeline 的关键差异

相比 **SimMotionEdit**（Li et al., CVPR 2025）仅使用最终层监督和相似性引导损失，OmniME 的 pipeline 在三个关键 slot 上进行了改造：

| 设计维度 | 基线做法 | OmniME 做法 |
|---------|---------|------------|
| 监督层级 | 仅 DiT 最终层 | 第 2、4、6 块附加回顾性预测头 |
| 保留损失触发 | 相似性引导，无显式筛选 | MotionSNR 阈值筛选，仅对高 SNR 样本施加 |
| 语义对齐 | 可能使用对比损失或无负样本 | 三元组损失，显式推远负样本 |

消融实验（Table 3）证实，移除任一组件均导致检索性能下降，三者结合在 MotionFix 测试集上达到 R@1 32.02 的最优性能。

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_Omni_Supervised_Mo/figures/001_Figure_1.jpg]]
*Figure 1: OmniME is a positive–negative learning framework for text-driven human motion editing. Given a source motion and a natural-language instruction, OmniME edits the source motion to produce the desired target motion while balancing change and invariance*

OmniME 将文本驱动的人体运动编辑形式化为一个全监督的正负学习问题，其核心在于通过**特征级、运动级、语义级**三个层次的监督信号，显式地平衡编辑过程中的“变化”与“不变性”。整个框架由五个关键模块协同构成。

### 运动表示与编辑目标

每一帧人体运动被表示为一个 207 维向量，涵盖全局速度、全局朝向、关节旋转和局部关节位置：

$$ \mathbf{x}_i = [\mathbf{v}_i, \mathbf{o}_i, \mathbf{r}_i, \mathbf{p}_i] \in \mathbb{R}^{207} \tag{1} $$

编辑过程的核心思想是引入一个**保留因子** $\mathbf{m}$，将源运动 $\mathbf{X}$ 与编辑内容 $\tilde{\mathbf{X}}$ 进行加权融合：

$$ \mathbf{M} = \mathbf{m} \odot \mathbf{X} + (1 - \mathbf{m}) \odot \tilde{\mathbf{X}} \tag{2} $$

这一形式化定义是整个框架的基石：$\mathbf{m}$ 显式地控制了哪些区域需要保留、哪些区域需要修改，使得“变化”与“不变性”的平衡成为一个可学习的目标。

### 融合 Transformer 与扩散 Transformer

框架的生成主干由 **Fusion Transformer** 和 **Diffusion Transformer (DiT)** 两部分组成（Figure 2）。源运动序列与文本指令首先进入 Fusion Transformer，将多模态信息融合为统一的联合表示；随后，该表示被送入由 8 个顺序块构成的 DiT 进行去噪与运动预测。DiT 是核心生成模块，其输出直接决定了最终的运动质量。

### 回顾性特征监督

传统方法通常仅在 DiT 的最终层施加监督信号，而 OmniME 在 DiT 的第 2、4、6 个中间块上附加轻量预测头，迫使中间层表示也与目标运动保持一致。回顾性特征监督损失定义为中间层预测损失的加权和：

$$ \mathcal{L}_{\mathrm{retro}} = \sum_{l \in \{2,4,6\}} \lambda_l \mathcal{L}^{(l)}, \quad \mathcal{L}^{(l)} = \frac{1}{BTJ} \sum_{b,t} \| \hat{\mathbf{x}}_{b,t}^{(l)} - \mathbf{x}_{b,t} \|_2^2 \tag{4, 5} $$

其中 $\hat{\mathbf{x}}^{(l)} = f^{(l)}(\mathbf{h}^{(l)})$ 是第 $l$ 层隐藏表示 $\mathbf{h}^{(l)}$ 经预测头映射回运动空间的结果。这一多级监督机制提升了训练稳定性，并增强了中间特征与最终目标的一致性。

### 运动保留机制

运动保留机制的核心创新在于**选择性施加保留约束**——并非对所有样本一视同仁，而是仅对运动变化细微的样本施加逐帧重建损失。为此，OmniME 引入了 **MotionSNR** 指标。首先计算源运动帧与目标运动帧之间的相似度，并按相似度排序；MotionSNR 定义为前 $\kappa$ 帧相似度之和与后 $\kappa$ 帧相似度之和的比值：

$$ \mathrm{MotionSNR} = \frac{\sum_{x \in T^{R}} x}{\sum_{x \in B^{R}} x} \tag{8} $$

MotionSNR 值越高，表明运动仅发生了细微变化，更适合应用保留监督。运动保留损失仅在 MotionSNR 超过阈值 $\tau$ 时激活：

$$ \mathcal{L}_{\mathrm{presv}} = \mathbb{I}(\mathbf{MotionSNR}(\mathbf{x}, \mathbf{m}) > \tau) \cdot \frac{1}{T} \sum_{i=1}^{T} \| m_i - x_i \|_2^2 \tag{9} $$

这一门控机制使得模型能够集中学习细微变化的编辑模式，避免对大幅修改区域施加不合理的保留约束。

### 三元组语义对齐

在语义层面，OmniME 采用三元组损失同时利用正文本和负文本进行对比监督。给定运动嵌入 $\mathbf{z}_m$、对应正文本嵌入 $\mathbf{z}_p$ 和随机负文本嵌入 $\mathbf{z}_n$，三元组损失的目标是拉近运动与正文本的距离，同时推远与负文本的距离：

$$ \mathcal{L}_{\mathrm{triplet}} = \frac{1}{B} \sum_{i=1}^{B} \left[ \| \mathbf{z}_m^i - \mathbf{z}_p^i \|_2^2 - \| \mathbf{z}_m^i - \mathbf{z}_n^i \|_2^2 + \alpha \right]_+ \tag{11} $$

其中 $\alpha$ 为间隔超参数。相比仅使用正样本的对比损失，三元组损失通过显式的负样本推开机制，强化了运动-文本之间的语义对齐，有效抑制了编辑结果与无关语义的混淆。

### 总体优化目标

最终，OmniME 的总体损失函数整合了扩散损失、分类损失、回顾性特征损失、运动保留损失和三元组语义对齐损失：

$$ \mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{diff}} + \lambda_{\mathrm{cls}} \mathcal{L}_{\mathrm{cls}} + \lambda_{\mathrm{retro}} \mathcal{L}_{\mathrm{retro}} + \lambda_{\mathrm{preserve}} \mathcal{L}_{\mathrm{preserve}} + \lambda_{\mathrm{triplet}} \mathcal{L}_{\mathrm{triplet}} \tag{12} $$

各 $\lambda$ 系数控制不同监督信号的相对强度。这五个损失项分别从**生成质量、特征一致性、运动结构保持、语义对齐**四个维度施加约束，构成了完整的全监督正负学习框架。

## 实验与关键发现

OmniME的性能通过两个主流文本驱动运动编辑基准数据集——**MotionFix**和**STANCE Adjustment**——进行系统评估。实验设计围绕三个核心问题展开：全监督正负学习框架是否带来实质性的性能提升；三个互补组件各自贡献如何；方法在不同数据集间的泛化能力如何。

### 主实验结果

**MotionFix数据集。** 表1报告了生成运动到目标运动的检索性能。OmniME在所有指标上均显著超越先前方法。与先前最优方法相比，AvgR从20.88降至13.06，降幅达7.82，表明编辑后的运动与目标运动在语义空间中的对齐程度大幅提升。在Batch R@1指标上，OmniME达到77.29，远超**SimMotionEdit**（Li et al., CVPR 2025）等强基线。值得注意的是，**MDM**（Tevet et al., ICLR 2023）和**MDM-BP**等无源运动信息或未在编辑数据集上充分训练的基线表现明显较弱，这验证了源运动信息和针对性编辑训练的必要性。

**STANCE Adjustment数据集。** 表2的结果呈现一致趋势。OmniME将AvgR从29.05降至22.77，降幅达6.28。该数据集的编辑难度更高（涉及姿态调整等细粒度变化），但OmniME仍然保持显著优势，证明了框架在不同编辑类型下的鲁棒性。

### 消融实验

表3在MotionFix数据集上系统拆解了三个核心组件的贡献。完整模型（Test Set R@1: 32.02）与移除任一组件相比均有明显优势：

- **移除回顾性特征监督（w/o Retrospective Supervision）**：性能显著下降。这表明仅依赖最终层损失不足以提供充分的训练信号，第2、4、6个DiT块上的中间层监督对稳定训练和提升生成质量至关重要。
- **移除运动保留机制（w/o Motion Preservation）**：性能同样受损。基于MotionSNR的加权保留损失能够精准识别细微变化样本，在不干扰大幅编辑的前提下有效保持未编辑区域的运动结构。
- **移除三元组语义对齐（w/o Triplet Loss）**：语义对齐能力减弱。正负文本的对比监督强化了运动嵌入与文本嵌入之间的细粒度对应，仅靠扩散损失难以实现同等水平的语义一致性。

三个组件协同作用，共同支撑了OmniME在变化与不变性之间的平衡能力。

### 定性分析与用户感知研究

图3和图4分别展示了MotionFix和STANCE Adjustment数据集上的定性编辑结果。与SimMotionEdit相比，OmniME生成的编辑运动在三个维度上表现更优：（1）**语义一致性**——编辑区域准确响应文本指令，未出现语义偏移或遗漏；（2）**运动平滑性**——编辑帧与相邻帧之间的过渡自然，无抖动或突变；（3）**源运动保留**——未编辑区域的动作形态得以完整保持，未受编辑操作污染。

图5的用户感知研究从四个维度量化了主观评价。在语义对齐、运动保留、过渡平滑性和整体自然度四个维度上，OmniME在两个数据集上均获得更高评分。这一结果与定量指标相互印证，说明客观性能提升转化为了可感知的视觉质量改善。

### 跨数据集泛化

表4报告了跨数据集泛化实验：在MotionFix上训练、在STANCE Adjustment上测试。OmniME在该设置下仍保持领先，表明框架学习到的编辑能力具有较好的迁移性，未对特定数据集的分布产生过度拟合。

### 局限性

当前分析材料中未提供明确的失败模式或局限性讨论。从方法设计推断，基于MotionSNR阈值的保留损失触发机制依赖于帧级相似度计算的准确性，在运动变化极为剧烈或源-目标对应关系模糊的场景下，MotionSNR的判别能力可能减弱，导致保留监督施加不当。此外，三元组损失中负样本的随机采样策略可能引入语义上不够“困难”的负样本，限制对比学习的效率上限。以上推断需结合原始论文的局限性声明进行手动验证。

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_Omni_Supervised_Mo/figures/003_Table_1.jpg]]
*Table 1: MotionFix dataset. [6] Comparison of retrieval performance (Generated-to-Target). R@k indicates recall at top-k (↑ higher is better, ↓ lower is better). * : no explicit text conditioning in the DiT stage*

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_Omni_Supervised_Mo/figures/004_Table_2.jpg]]
*Table 2: STANCE Adjustment dataset. [28] Comparison of retrieval performance (Generated-to-Target). R@k indicates recall at top-k (↑ higher is better, ↓ lower is better). * : no explicit text conditioning in the DiT stage*

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_Omni_Supervised_Mo/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative comparison between our method and SimMotionEdit[34] on the MotionFix [6] dataset. Our results surpass SimMotionEdit in terms of semantic consistency, motion smoothness, and source motion preservation*

![[assets/figures/papers/paper_list_l5_https_openaccess_thecvf_com_content_CVPR2026_html_Shi_Omni_Supervised_Mo/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison between our method and SimMotionEdit[34] on the STANCE Adjustment [28] dataset. Our results surpass SimMotionEdit in terms of semantic consistency, motion smoothness, and source motion preservation*

## 定位与知识库关联

### 1. 问题定位：文本驱动运动编辑的核心瓶颈

文本驱动的人体运动编辑任务要求模型依据自然语言指令修改源运动序列，同时保持未指定修改区域的运动不变性。现有方法面临的核心瓶颈在于：缺乏对“应修改区域”与“应保留区域”的显式区分机制，导致编辑结果出现运动扭曲、语义对齐不佳以及源运动结构被意外破坏等问题。OmniME将这一问题形式化为**全监督正负学习**——同时施加正向修改约束和负向不变性约束，通过特征级、运动级和语义级的三层监督显式平衡变化与不变性。

### 2. 基线谱系与OmniME的差异化定位

文本驱动运动编辑的方法谱系可从监督粒度和约束类型两个维度进行梳理。

**无源运动条件的扩散基线。** **MDM**（Tevet et al., ICLR 2023）作为通用运动扩散模型，在编辑时缺乏源运动信息的注入通道，导致生成结果与源运动的结构一致性难以保证。**MDM-BP**虽引入源运动作为条件，但未在文本编辑数据集上进行针对性训练，其编辑能力受限于预训练分布。

**单级监督的编辑基线。** **TMED**和**MotionReFit**等基线同时利用源运动和文本指令，但在监督信号的设计上停留在最终输出层，缺乏对中间表示的有效约束。**SimMotionEdit**（Li et al., CVPR 2025）通过相似性预测辅助监督将编辑性能推进了一步，但其监督仍集中于DiT的最后一层，且运动保留损失缺乏对“细微变化”与“大幅修改”的差异化处理。

**OmniME的三层差异化监督。** OmniME在以下三个关键维度上区别于前述基线：

| 监督维度 | 基线做法 | OmniME改进 | 因果机制 |
|---------|---------|-----------|---------|
| **特征级** | 仅最终层监督（SimMotionEdit） | 在第2、4、6个DiT块添加回顾性特征预测头，与最终层损失加权求和 | 多级中间监督迫使网络在去噪过程中保持对目标运动结构的逐步逼近，提升训练稳定性和生成质量 |
| **运动级** | 相似性引导损失，无显式高/低变化筛选 | 计算MotionSNR，仅对高SNR（细微变化）样本施加保留损失 | 避免在需要大幅修改的帧上施加过强的保留约束，使保留损失集中于真正需要保持不变的细微编辑场景 |
| **语义级** | 可能使用对比损失或无负样本监督 | 三元组损失（Triplet Loss），同时拉近正文本、推远负文本 | 负样本文本的显式排斥力强化了运动-文本语义对齐的判别性，防止编辑结果在语义空间中坍缩到模糊区域 |

### 3. 知识库定位：全监督正负学习的贡献边界

OmniME的核心知识贡献在于**将运动编辑从“条件生成”重新定义为“正负约束联合优化”**，其适用边界和局限如下。

**适用边界。** 该方法适用于具有明确源-目标配对和文本指令标注的编辑场景。其MotionSNR机制假设细微编辑与大幅修改可通过帧级相似度的分布特征（前κ帧与后κ帧相似度之比）有效区分，这一假设在MotionFix和STANCE Adjustment数据集上得到验证。三元组语义对齐依赖预训练CLIP模型提供的文本嵌入空间，因此编辑指令需要落在CLIP的语义覆盖范围内。

**局限与开放问题。** 论文未明确报告方法在以下场景的表现边界：（1）长时序运动（远超训练序列长度）的编辑稳定性；（2）多轮连续编辑中的误差累积问题；（3）对分布外文本指令（如抽象隐喻性描述）的泛化能力。此外，MotionSNR阈值τ的设定依赖数据集特性，跨数据集的阈值迁移策略尚未被系统研究。消融实验（Table 3）虽验证了三个组件的独立贡献，但组件间的交互效应（如回顾性监督是否放大了三元组损失的梯度信号）仍需进一步分析。

**与后续工作的潜在关联。** OmniME的正负学习框架为运动编辑提供了一个可扩展的约束模板——未来工作可在三个方向上延伸：（1）将MotionSNR机制替换为可学习的门控网络，实现动态保留权重分配；（2）将三元组损失扩展为结构化对比损失，引入更细粒度的语义对齐（如身体部位级文本-运动对应）；（3）将回顾性监督的思想推广至其他扩散模型架构，验证其在非DiT结构上的有效性。

## 原文 PDF

![[paperPDFs/CVPR_2026/Omni_Supervised_Motion_Editing_Balancing_Change_and_Invariance_through_Positive_Negative_Learning.pdf]]
