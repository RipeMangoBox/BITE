---
title: "UTPTrack: Towards Simple and Unified Token Pruning for Visual Tracking"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UTPTrack_Towards_Simple_and_Unified_Token_Pruning_for_Visual_Tracking.pdf
project_link: null
code_link: "https://github.com/EIT-NLP/UTPTrack"
aliases:
- UTPTrack
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 联合剪枝搜索区域、动态模板和静态模板，利用注意力引导的相似度评分和令牌类型感知（边界框先验）策略，实现统一冗余建模。
primary_logic: 通过联合建模所有组件的冗余，复用注意力权重估计令牌重要性，并对静态模板引入目标边界框空间先验，可以在几乎不损失精度的情况下大幅减少视觉令牌数量，同时适用于 RGB 和统一跨模态跟踪。
claims:
- UTPTrack 是首个在一流 Transformer 中联合压缩 SR、DT 和 ST 的统一令牌剪枝框架。
- UTPTrack 在 RGB 跟踪中剪枝 65.4% 视觉令牌且保持 99.7% 基线性能，在统一跟踪中剪枝 67.5% 令牌且保持 100.5% 基线性能。
- 跨组件联合剪枝策略在多种压缩率下均优于单独剪枝，且高压缩率时优势扩大。
- 令牌类型感知策略通过边界框先验稳定静态模板剪枝，Soft bonus 提供最佳性能。
---

# UTPTrack: Towards Simple and Unified Token Pruning for Visual Tracking

> [!tip] 核心洞察
> 通过联合建模所有组件的冗余，复用注意力权重估计令牌重要性，并对静态模板引入目标边界框空间先验，可以在几乎不损失精度的情况下大幅减少视觉令牌数量，同时适用于 RGB 和统一跨模态跟踪。

| 字段 | 内容 |
|------|------|
| 中文题名 | UTPTrack：面向视觉跟踪的简单统一令牌剪枝框架 |
| 英文题名 | UTPTrack: Towards Simple and Unified Token Pruning for Visual Tracking |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23734) · [Code](https://github.com/EIT-NLP/UTPTrack) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UTPTrack |
| Dataset | LaSOT, LaSOT_ext, TrackingNet, GOT-10k, All 10 unified tracking benchmarks, LaSOT, RGB-based tracking |

> [!tip] 效果简介
> - LaSOT, LaSOT_ext, TrackingNet, GOT-10k (RGB-based tracking) 上，Average relative performance 100.2% (UTPTrack-O256, 18.8% tokens pruned) vs 100% (OSTrack256, no pruning) (+0.2%)。
> - All 10 unified tracking benchmarks (RGB, RGB-D, RGB-T, RGB-E, RGB-Lang) 上，Average relative performance 99.8% (UTPTrack-S224, 25.6% tokens pruned) vs 100% (SUTrack224, no pruning) (-0.2%)。
> - All 10 unified tracking benchmarks 上，Average relative performance 99.5% (UTPTrack-S224, 48.0% tokens pruned) vs 100% (SUTrack224) (-0.5%)。

## 概述

### 问题背景

单流（One-Stream）Transformer 跟踪器通过联合处理搜索区域（SR）、动态模板（DT）和静态模板（ST）实现了强大的跟踪性能，但其计算开销随视觉令牌数量线性增长。现有的令牌剪枝方法（如 **CE**、**ToMe**、**EViT**、**DynamicViT**）通常孤立地处理搜索区域，忽略跨组件依赖，导致次优剪枝和精度下降。特别是，静态模板和动态模板中的冗余令牌未被有效利用，而跨组件注意力交互中蕴含的丰富相似度信息也未得到充分挖掘。

### 核心方法

**UTPTrack** 提出了首个在一流 Transformer 中联合压缩 SR、DT 和 ST 的统一令牌剪枝框架。其核心思想是：通过复用注意力权重估计令牌重要性，并引入令牌类型感知策略（利用目标边界框空间先验），实现对视觉令牌冗余的联合建模与高效剪枝。

具体而言，UTPTrack 包含三个关键模块：
- **候选消除模块（CE）**：基于静态模板中心令牌的注意力相似度剪枝搜索区域冗余令牌；
- **动态模板消除（DTE）**：剪枝动态模板中与静态模板中心令牌相似度低的噪声令牌；
- **静态模板消除（STE）**：剪枝静态模板中的背景令牌，并借助令牌类型感知策略（TTA）利用边界框先验稳定剪枝过程。

在统一跨模态跟踪中，UTPTrack 进一步引入文本引导剪枝（TG），结合 CLIP-L 文本令牌与视觉令牌的注意力交互，引导搜索区域和模板令牌的重要性估计。

### 核心结论

UTPTrack 在几乎不损失精度的情况下大幅减少视觉令牌数量。在 RGB 跟踪中，**剪枝 65.4% 视觉令牌且保持 99.7% 基线性能**；在统一跨模态跟踪中，**剪枝 67.5% 令牌且保持 100.5% 基线性能**。跨组件联合剪枝策略在多种压缩率下均优于单独剪枝，且高压缩率时优势扩大。令牌类型感知策略通过 Soft bonus 提供精细的前景覆盖估计，实现 99.8% 的平均性能保持率。

### 方法定位

UTPTrack 属于**视觉跟踪中的令牌剪枝方法**，与现有方法（如 CE、ToMe、EViT、DynamicViT）的关键区别在于：
1. **联合剪枝**：首次同时压缩 SR、DT 和 ST 三个组件，而非孤立处理；
2. **注意力引导**：直接复用 Transformer 层中的注意力权重，无需额外参数预测令牌重要性；
3. **空间先验增强**：对静态模板引入边界框引导的令牌类型感知策略，稳定剪枝并避免丢弃前景令牌；
4. **跨模态扩展**：通过文本引导剪枝无缝适配统一跨模态跟踪（RGB-D/T/E/Lang）。

该方法基于单流跟踪器 **OSTrack**（RGB）和 **SUTrack**（统一）构建，在 12 层 ViT 和 24 层 HiViT 主干上验证，支持 224/256/384 分辨率输入，覆盖 4 个 RGB 基准和 10 个统一跟踪基准。

## 背景与动机

视觉目标跟踪是计算机视觉的基础任务，旨在根据初始帧给定的目标模板，在后续帧中持续定位目标位置。近年来，基于单流 Transformer 的跟踪器——如 **OSTrack** 和 **SUTrack**——将搜索区域、动态模板和静态模板的令牌拼接后送入统一的自注意力模块，实现了优异的跟踪精度。然而，这种全令牌交互范式带来了显著的计算开销：视觉令牌数量随模板数量和搜索区域分辨率线性增长，导致自注意力复杂度呈二次方膨胀，严重制约了跟踪器的实时部署能力。

### 现有令牌压缩方法的局限

为缓解上述效率瓶颈，研究者借鉴图像分类领域的令牌剪枝与合并策略，尝试在跟踪器中移除冗余视觉令牌。代表性工作包括 **CE (Candidate Elimination)**、**ToMe**、**EViT** 和 **DynamicViT** 等。然而，这些方法存在一个共同的结构性缺陷：**孤立地处理搜索区域令牌，完全忽略了动态模板和静态模板中同样存在的冗余，更未考虑三类令牌之间的跨组件依赖关系**。具体而言：

- **搜索区域剪枝**：仅依据搜索区域内部或与静态模板的局部相似度进行裁剪，未利用动态模板提供的最新目标外观信息。
- **模板保留**：动态模板和静态模板通常被完整保留，即使其中大量背景令牌对跟踪任务贡献甚微。
- **跨组件冗余**：搜索区域、动态模板和静态模板共享相似的目标外观特征，孤立剪枝无法建模这种跨组件冗余，导致次优的压缩效果和精度损失。

### 统一跨模态跟踪的额外挑战

随着 **SUTrack** 等统一跟踪框架的兴起，跟踪器需要同时处理 RGB、RGB-D、RGB-T、RGB-E 和 RGB-Language 等多种模态输入。在语言引导的跟踪场景中，文本令牌为定位目标提供了额外的语义线索。然而，现有剪枝方法完全无法利用文本令牌与视觉令牌之间的注意力交互来指导冗余评估，错失了进一步提升压缩效率的机会。

### 本文动机

针对上述问题，本文提出 **UTPTrack**——首个在一流 Transformer 中**联合压缩搜索区域、动态模板和静态模板**的统一令牌剪枝框架。核心动机包括：

1. **联合建模跨组件冗余**：通过复用注意力权重，同时评估三类视觉令牌的重要性，实现全局最优的令牌保留决策。
2. **引入空间先验稳定模板剪枝**：静态模板剪枝面临误删前景令牌的风险，利用目标边界框提供的空间先验可有效抑制这一风险。
3. **扩展至文本引导剪枝**：在统一跟踪中，利用 CLIP 文本编码器输出的语言令牌与视觉令牌的交互，为语言引导场景提供更精准的令牌重要性估计。

通过上述设计，UTPTrack 在几乎不损失精度的前提下，大幅削减视觉令牌数量——在 RGB 跟踪中剪枝 65.4% 的视觉令牌且保持基线 99.7% 的性能，在统一跟踪中剪枝 67.5% 的令牌且保持基线 100.5% 的性能，为高效视觉跟踪提供了简洁而统一的解决方案。

## 核心创新

UTPTrack 的核心创新在于首次提出面向一流（one-stream）Transformer 跟踪器的**跨组件统一令牌剪枝框架**，其关键思想是：搜索区域（SR）、动态模板（DT）和静态模板（ST）之间存在深层冗余依赖，孤立剪枝会破坏这种跨组件信息流，导致次优的精度-效率权衡。UTPTrack 通过三个相互协同的机制突破这一瓶颈。

### 1. 跨组件联合剪枝（Cross-Component Joint Pruning）

现有令牌剪枝方法（如 **CE** 、**ToMe** 、**EViT** 、**DynamicViT** ）通常仅对搜索区域单独剪枝，忽略了动态模板和静态模板中的冗余。UTPTrack 首次将三个组件纳入统一的剪枝框架——**Candidate Elimination Module (CE)** 负责剪枝搜索区域、**Dynamic Template Elimination (DTE)** 剪枝动态模板、**Static Template Elimination (STE)** 剪枝静态模板。三个模块共享一个核心设计原则：利用静态模板的中心令牌（center token）作为查询锚点，通过注意力相似度评估各组件令牌的重要性。

这一联合策略的因果效应在控制预算实验中得到了直接验证：在相同令牌保留率下，UTPTrack 的跨组件联合剪枝始终优于仅剪枝搜索区域的基线方法，且**压缩率越高，性能差距越大**。在高分辨率 RGB 跟踪（OSTrack384）上，UTPTrack 剪枝 65.4% 视觉令牌，MACs 降低 31.3%，同时保持基线性能的 99.7%；在统一跟踪（SUTrack384）上，剪枝 67.5% 令牌，MACs 降低 28.4%，保持 100.5% 基线性能。

### 2. 令牌类型感知剪枝（Token Type-Aware Pruning, TTA）

静态模板剪枝面临一个独特挑战：目标前景令牌可能被注意力机制误判为低重要性而遭丢弃。UTPTrack 的解决方案是引入**边界框空间先验**——利用静态模板已知的目标边界框生成前景掩码，为每个 patch 分配前景分数作为奖励（bonus），与注意力重要性评分融合后指导剪枝。

这一设计的关键洞察是：TTA **不替代**注意力重要性估计，而是**稳定**静态模板剪枝过程。消融实验表明，三种奖励策略中 **Soft bonus**（取 patch 内前景像素占比的均值）表现最优，达到平均性能的 99.8%，优于 Full bonus（99.3%）和 All bonus（99.1%）。Soft bonus 的优势在于提供更细粒度的前景覆盖估计，并产生更平滑的边界过渡，避免硬阈值带来的不稳定性。

### 3. 文本引导剪枝（Text-Guided Pruning）

针对统一跨模态跟踪场景，UTPTrack 进一步提出文本引导剪枝机制。在统一跟踪的一流架构中，CLIP-L 编码的文本令牌与所有视觉令牌通过注意力交互。UTPTrack 创新性地**联合使用静态模板中心令牌和语言令牌**来估计视觉令牌重要性：

$$\omega_{x} = \phi\left( \mathrm{softmax}\left(\frac{Q_{sz'}K_{x}^T}{\sqrt{d_k}}\right) + \mathrm{softmax}\left(\frac{Q_{t}K_{x}^T}{\sqrt{d_k}}\right) \right)$$

这一设计使得剪枝过程能够感知语言语义，在 RGB-Language 跟踪等场景中更具判别力。消融实验证实，将语言线索注入动态模板剪枝即可达到 100.0% 的相对基线性能，与未剪枝基线持平。

### 4. 剪枝调度与架构无关性

UTPTrack 的剪枝模块以**轻量级 CTEM（Candidate or Template Elimination Module）**形式插入 Transformer 编码器的选定层，无需重新训练或结构修改。对于 12 层 ViT 主干，最优配置（#3）为：CE 在层 [3, 6, 9] 执行，DTE 在层 [4, 7, 10] 执行。这一手工选择的调度策略在当前主干上取得了最佳性能-效率权衡，但其泛化到其他架构深度仍需进一步验证。

总体而言，UTPTrack 的创新本质在于**将令牌剪枝从单组件的孤立操作提升为跨组件的统一冗余建模**，并通过注意力复用和空间先验注入，在不牺牲跟踪精度的前提下实现显著的效率增益。

## 整体框架

UTPTrack 构建在一流 Transformer 跟踪器之上，其核心设计思想是**联合压缩搜索区域（Search Region, SR）、动态模板（Dynamic Template, DT）和静态模板（Static Template, ST）三类视觉令牌**，而非像现有方法那样孤立地处理各组件。整体 pipeline 如图 2 所示，包含两条并行的跟踪管线：

**RGB 跟踪管线**：输入为搜索区域图像块 $\mathbf{x}$、静态模板图像块 $\mathbf{z}$ 以及动态模板图像块 $\mathbf{dz}$。三者经 patch embedding 后分别得到令牌序列 $\mathbf{E_x}$、$\mathbf{E_{sz}}$ 和 $\mathbf{E_{dz}}$，拼接后送入 ViT 骨干网络 $\mathcal{F}$，最终由预测头 $\varphi$ 输出目标边界框 $\mathbf{B}$：
$$\mathbf{B} = \varphi\left(\mathcal{F}(\mathrm{Concat}(\mathbf{E_x}, \mathbf{E_{sz}}, \mathbf{E_{dz}}))\right)$$

**统一跟踪管线**：在 RGB 管线基础上，额外引入语言令牌 $\mathbf{E_{text}}$（由 CLIP-L 文本编码器提取），与三类视觉令牌拼接后共同处理：
$$\mathbf{B} = \varphi\left(\mathcal{F}(\mathrm{Concat}(\mathbf{E_x}, \mathbf{E_{sz}}, \mathbf{E_{dz}}, \mathbf{E_{text}}))\right)$$

### 核心剪枝模块：CTEM

UTPTrack 在 ViT 编码器的选定层中插入轻量级的 **Candidate or Template Elimination Module（CTEM）**，负责对三类视觉令牌进行渐进式剪枝。CTEM 包含三个子模块：

- **Candidate Elimination（CE）**：以静态模板中心令牌为锚点，计算每个 SR 令牌与中心令牌的注意力相似度作为重要性分数，剪除低相关度的背景令牌。
- **Dynamic Template Elimination（DTE）**：同样基于 DT 令牌与 ST 中心令牌的注意力相似度，剪除动态模板中的噪声令牌（如遮挡、形变引入的干扰）。
- **Static Template Elimination（STE）**：在保留中心令牌的前提下，剪除静态模板中与中心令牌相似度低的背景令牌。STE 额外集成了**令牌类型感知（Token Type-Aware, TTA）**策略：利用静态模板的已知目标边界框生成前景掩码 $\mathbf{M}$，为每个 patch 计算前景覆盖分数作为奖励项（默认采用 Soft bonus $b_{\mathrm{soft}}^{(k)} = m_{\mathrm{avg}}^{(k)}$），叠加到注意力重要性分数上，从而抑制误删前景令牌的风险。

对于统一跟踪管线，CTEM 还启用了**文本引导剪枝（Text-Guided Pruning, TG）**：将语言令牌与 ST 中心令牌的注意力联合用于计算视觉令牌的重要性：
$$\omega_{x} = \phi\left(\mathrm{softmax}\left(\frac{Q_{sz'}K_{x}^T}{\sqrt{d_k}}\right) + \mathrm{softmax}\left(\frac{Q_{t}K_{x}^T}{\sqrt{d_k}}\right)\right)$$

### 剪枝调度

剪枝并非在每一层执行，而是按预设层位置触发。对于 12 层 ViT 主干（RGB 跟踪器），CE 在层 [3, 6, 9] 执行，DTE 在层 [4, 7, 10] 执行，STE 在后续层中配合 TTA 完成静态模板压缩。这一调度方案（配置 #3）经消融实验验证为性能-效率最优折衷（Table 13）。对于 24 层 HiViT 主干（统一跟踪器），CTEM 位置另有适配配置（Table 6）。

![[assets/figures/papers/paper_list_l953_https_arxiv_org_abs_2602_23734/figures/008_Table_6.jpg]]
*Table 6: Ablation Study on CTEM Location for Unified Trackers with a 24-layer HiViT backbone*

### 训练目标

RGB 跟踪器采用分类 focal loss、GIoU loss 和 L1 回归损失的加权组合：
$$\mathcal{L}_{\mathrm{RGB}} = \lambda_{\mathrm{cls}}\mathcal{L}_{\mathrm{cls}} + \lambda_{\mathrm{giou}}\mathcal{L}_{\mathrm{giou}} + \lambda_{L_1}\mathcal{L}_{L_1}$$

统一跟踪器在此基础上增加任务识别交叉熵损失 $\mathcal{L}_{\mathrm{task}}$：
$$\mathcal{L}_{\mathrm{Unified}} = \mathcal{L}_{\mathrm{RGB}} + \lambda_{\mathrm{task}}\mathcal{L}_{\mathrm{task}}$$

整体框架的关键优势在于**跨组件联合建模冗余**：CE、DTE、STE 共享统一的注意力引导重要性评估机制，使得三类令牌的剪枝决策相互协调，避免了孤立剪枝导致的信息断裂。在高压缩率下，这一联合策略的优势尤为显著——随着保留令牌比例下降，UTPTrack 与其他方法的性能差距持续扩大。

### 补充图表

![[assets/figures/papers/paper_list_l953_https_arxiv_org_abs_2602_23734/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of the proposed UTPTrack. UTPTrack supports both RGB-based and unified tracking. It adopts a one-stream transformer that jointly processes tokens from the search region (SR), dynamic template (DT), and static template (ST). A lightweight Candidate or Template Elimination Module (CTEM) is inserted into encoder layers to prune redundant tokens from all three sources. In the figure, D/T/E denote depth, thermal, and event modalities, respectively*

## 核心模块与公式推导

### 3.1 一流 Transformer 注意力基础

UTPTrack 基于单流（one-stream）Transformer 架构，将搜索区域（Search Region, SR）、静态模板（Static Template, ST）和动态模板（Dynamic Template, DT）的令牌拼接后联合处理。其核心操作为标准的缩放点积注意力：

$$\text{Attention}(Q,K,V) = \text{Softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

其中 $Q$、$K$、$V$ 分别为查询、键和值矩阵，$d_k$ 为键向量的维度。拼接后的令牌序列包含 SR、ST、DT 三个组件，注意力权重矩阵可展开为分块形式：

$$A = \text{Softmax}\left(\frac{1}{\sqrt{d_k}}\begin{bmatrix} Q_x K_x^T & Q_x K_{sz}^T & Q_x K_{dz}^T \\ Q_{sz} K_x^T & Q_{sz} K_{sz}^T & Q_{sz} K_{dz}^T \\ Q_{dz} K_x^T & Q_{dz} K_{sz}^T & Q_{dz} K_{dz}^T \end{bmatrix}\right)$$

其中下标 $x$、$sz$、$dz$ 分别对应搜索区域、静态模板和动态模板。这一分块注意力矩阵中，$Q_{sz} K_x^T$ 和 $Q_{sz} K_{dz}^T$ 子块直接度量了 ST 中心令牌与 SR/DT 令牌之间的相似度，为后续剪枝提供了无需额外计算的注意力引导信号。

### 3.2 候选/模板消除模块（CTEM）

UTPTrack 在选定的编码器层中插入轻量级的候选或模板消除模块（Candidate or Template Elimination Module, CTEM），利用模型自身的注意力图来评估令牌重要性并执行剪枝。CTEM 包含三个子模块，分别针对不同组件：

**候选消除模块（Candidate Elimination, CE）**：针对搜索区域（SR）的冗余令牌。通过计算每个 SR 令牌与静态模板中心令牌的注意力相似度来度量其重要性，保留高相似度令牌，剪除低相似度令牌。其直觉在于：与目标模板中心高度相关的搜索区域令牌更可能包含目标信息。

**动态模板消除（Dynamic Template Elimination, DTE）**：针对动态模板（DT）中的噪声令牌。同样基于 DT 令牌与 ST 中心令牌的相似度，剪除相关性低的令牌。动态模板在跟踪过程中累积更新，可能引入背景噪声或遮挡物信息，DTE 旨在过滤这些干扰。

**静态模板消除（Static Template Elimination, STE）**：针对静态模板（ST）中的背景令牌。计算每个 ST 令牌与中心令牌的相似度，剪除低相关性的背景令牌，但始终保留中心令牌以确保目标锚点的完整性。

### 3.3 令牌类型感知剪枝（Token Type-Aware Pruning, TTA）

仅依赖注意力相似度进行 ST 剪枝存在风险：静态模板中的前景令牌可能与中心令牌的注意力并不突出，容易被误剪。为解决这一问题，UTPTrack 引入令牌类型感知剪枝策略，利用静态模板的目标边界框（bounding box）生成空间先验，对前景区域令牌施加奖励。

给定静态模板的边界框 $B$，首先生成二值前景掩码：

$$M(i,j) = 1 \text{ if } (i,j) \text{ is inside } B, \ 0 \text{ otherwise.}$$

其中 $(i,j)$ 为像素坐标。将掩码按 ViT 的 patch 划分后，计算每个 patch $k$ 的前景分数。UTPTrack 默认采用 **Soft bonus** 策略，使用 patch 内掩码像素的平均值作为奖励：

$$b_{\text{soft}}^{(k)} = m_{\text{avg}}^{(k)} = \frac{1}{P^2}\sum \mathbf{M}(i,j), \quad (i,j)\in\mathbf{M}_{\text{patch}}^{(k)}$$

其中 $P$ 为 patch 大小。该奖励值被整合到注意力引导的消除模块中，以降低前景令牌被剪除的概率。Soft bonus 提供了细粒度的前景覆盖估计，边界过渡平滑，在消融实验中达到 99.8% 的平均性能（Table 15）。

![[assets/figures/papers/paper_list_l953_https_arxiv_org_abs_2602_23734/figures/019_Table_15.jpg]]
*Table 15: Ablation Study on bonus for Unified Trackers*

论文还探索了另外两种奖励策略：
- **Full bonus**：$b_{\text{full}}^{(k)} = 1$ 当 patch 完全位于边界框内，否则为 0；
- **All bonus**：$b_{\text{all}}^{(k)} = 1$ 当 patch 中任意像素位于边界框内，否则为 0。

实验表明 Soft bonus 优于 Full（99.3%）和 All（99.1%）策略，验证了细粒度前景估计对稳定剪枝的重要性。

### 3.4 文本引导剪枝（Text-Guided Pruning, TG）

在统一跟踪（unified tracking）场景中，UTPTrack 额外引入语言令牌（来自 CLIP-L 文本编码器）作为引导信号。语言令牌与所有视觉令牌通过注意力交互，其注意力权重可反映视觉令牌与语言描述的相关性。

文本引导的重要性得分定义为：

$$\omega_{x} = \phi\left( \text{softmax}\left(\frac{Q_{sz'}K_{x}^T}{\sqrt{d_k}}\right) + \text{softmax}\left(\frac{Q_{t}K_{x}^T}{\sqrt{d_k}}\right) \right)$$

其中 $Q_{sz'}$ 为静态模板中心令牌的查询向量，$Q_t$ 为语言令牌的查询向量，$K_x$ 为搜索区域令牌的键向量，$\phi$ 为聚合函数。该公式联合利用视觉模板中心令牌和语言令牌的注意力来估计 SR 令牌的重要性，使剪枝过程同时感知视觉目标和语言语义。

消融实验（Table 7）表明，将语言线索仅注入 DT 剪枝即可达到 100.0% 的相对性能（与未剪枝基线持平）；注入全部三个组件（SR、DT、ST）可进一步提升跨模态场景下的剪枝鲁棒性。

![[assets/figures/papers/paper_list_l953_https_arxiv_org_abs_2602_23734/figures/011_Table_7.jpg]]
*Table 7: Ablation study of selectively injecting language cues into different components for text-guided token pruning. Average performance is reported relative to the baseline of unified trackers*

### 3.5 剪枝调度与配置

CTEM 模块并非在所有编码器层执行，而是按照预设的调度插入。对于 12 层 ViT 主干（RGB 跟踪），经过消融确定的最优配置为：CE 在层 [3, 6, 9] 执行，DTE 在层 [4, 7, 10] 执行（配置 #3，Table 13）。STE 在更深的层执行以确保静态模板剪枝的稳定性。对于 24 层 HiViT 主干（统一跟踪），CTEM 位置的消融结果见 Table 6。

这种渐进式、分层的剪枝调度设计，使得网络浅层保留较多令牌以提取充分特征，深层逐步压缩冗余，在性能与效率之间取得平衡。渐进剪枝分析（Figure 4）显示，随着保留率降低和 CE、DTE、STE 逐步启用，性能在多数阶段保持在基线 1–2% 偏差范围内。

### 补充图表

![[assets/figures/papers/paper_list_l953_https_arxiv_org_abs_2602_23734/figures/018_Table_14.jpg]]
*Table 14: Effect of spatial priors in attention-guided pruning*

## 实验与分析

### 核心性能与效率权衡

UTPTrack 在 RGB 跟踪与统一跨模态跟踪两个场景下均展现出“大幅压缩令牌 + 几乎无损精度”的独特能力。在默认压缩配置下，**UTPTrack-O384** 将视觉令牌数减少 65.4%，MACs 降低 31.3%（从 78G 降至 53G），同时保持基线性能的 99.7%；**UTPTrack-S384** 在统一跟踪中令牌减少 67.5%，MACs 降低 28.4%，性能保持在基线的 100.5%（见 Figure 3 高分辨率组）。低分辨率场景下，UTPTrack-O256 令牌剪枝 64.8%，MACs 从 34.5G 降至 23.9G（-30.7%），性能保持在 99.7%；UTPTrack-S224 令牌剪枝 69.4%，MACs 从 22.8G 降至 16.2G（-28.9%），性能保持在 100.0%（见 Figure 3 低分辨率组）。

![[assets/figures/papers/paper_list_l953_https_arxiv_org_abs_2602_23734/figures/004_Figure_3.jpg]]
*Figure 3: Performance comparison of UTPTrack and other pruning methods under each method’s default compression settings at two resolutions. Top (High Resolution): 384 (RGB and Unified). Bottom (Low Resolution): 256 (RGB), and 224 (Unified)*

**关键洞察**：UTPTrack 的“剪枝不降精度”特性并非偶然——其跨组件联合剪枝策略在搜索区域（SR）、动态模板（DT）和静态模板（ST）三者之间协同识别冗余，避免了孤立剪枝导致的精度崩塌。在控制预算实验中（Table 2 和 Table 3），随着令牌保留率从 87.2% 逐步降至 35.4%，UTPTrack 的相对性能始终优于 CE（Candidate Elimination）、ToMe、EViT、DynamicViT 等剪枝/合并方法，且压缩率越高优势越显著。

### 控制预算实验：RGB 跟踪

Table 2 报告了基于 OSTrack256 的 RGB 跟踪控制预算对比。在三种令牌保留率（87.2%、65.6%、52.0%）下，UTPTrack-O256 的平均相对性能分别为 **100.2%、99.7%、99.3%**，全面优于其他方法。以 LaSOT 的 AUC 为例，在 65.6% 令牌保留率下，UTPTrack-O256 达到 68.2，甚至略高于无剪枝基线 OSTrack256 的 67.9（+0.3）。相比之下，CE 方法在同等压缩率下出现明显精度下降，ToMe 和 DynamicViT 的表现也不及 UTPTrack。

![[assets/figures/papers/paper_list_l953_https_arxiv_org_abs_2602_23734/figures/005_Table_2.jpg]]
*Table 2: Performance comparisions under different vision token configurations across RGB-based tracking. All methods are applied on the same base model OSTrack256. The average performance listed is calculated across all four benchmarks*

### 控制预算实验：统一跟踪

Table 3 报告了基于 SUTrack224 的统一跟踪控制预算对比，覆盖 RGB、RGB-D、RGB-T、RGB-E、RGB-Lang 共 10 个基准。在 71.4% 令牌保留率下，UTPTrack-S224 平均相对性能为 99.8%（下降仅 0.2%）；在 52.0% 保留率下为 99.5%（下降 0.5%）；即使压缩至 35.4% 保留率（Table 17），平均相对性能仍保持在 99.3%（下降 0.7%）。这一稳定性在跨模态场景中尤为突出：RGB-D、RGB-T、RGB-E 等模态下的性能退化幅度与 RGB 模态基本一致，表明联合剪枝策略对模态差异具有鲁棒性。

![[assets/figures/papers/paper_list_l953_https_arxiv_org_abs_2602_23734/figures/006_Table_3.jpg]]
*Table 3: Performance comparisons under different vision token compression configurations across unified tracking. All methods are applied on the same base model SUTrack224. The best result are bolded and the second best results are underlined in all following tables. The average performance listed is calculated across all 10 benchmarks. TrackingNet is abbreviated as TrkNet for brevity*

### 消融实验：组件贡献

**Table 4（RGB 跟踪消融）** 和 **Table 5（统一跟踪消融）** 系统验证了三个消除模块的独立贡献。逐步添加 CE（搜索区域剪枝）、DTE（动态模板剪枝）和 STE（静态模板剪枝），每一步都带来可测量的令牌压缩收益，而性能退化始终控制在 1–2 个百分点以内。移除任一模块均导致性能下降，证实三者缺一不可。

**令牌类型感知剪枝（TTA）** 是稳定 ST 剪枝的关键。Table 14 显示，纯注意力引导剪枝已显著优于随机剪枝，但加入空间先验（边界框掩码）后性能进一步提升。在奖励策略消融（Table 15）中，**Soft bonus**（基于 patch 内前景像素比例的平均值）达到 99.8% 平均性能，优于 Full bonus（99.3%）和 All bonus（99.1%）。Soft bonus 的优势在于提供更细粒度的前景覆盖估计，产生更平滑的边界过渡，避免硬边界导致的误丢弃。

**文本引导剪枝消融**（Table 7）针对统一跟踪中的语言模态。将语言线索注入 DT 剪枝即可达到 100.0% 相对性能（与无剪枝基线持平）；同时注入 CE 和 STE 也能保持极高性能。这表明 CLIP-L 文本令牌与视觉令牌的交叉注意力确实捕获了语言相关的显著性信息，且 DT 是语言引导收益最大的组件。

### 渐进剪枝分析

Figure 4 展示了随着保留率下降、逐步启用 CE → DTE → STE 过程中性能与令牌数的变化曲线。在 RGB 跟踪和统一跟踪中，性能曲线在大部分压缩阶段保持在基线 1–2% 以内，直到极高压缩率（保留率 < 30%）才出现较明显下降。这验证了 UTPTrack 的调度策略——在 ViT 的浅层（第 3、4 层）启动 CE 和 DTE，在中层（第 6、7 层）和深层（第 9、10 层）继续剪枝——能够在信息充分传播后再消除冗余，避免过早丢弃关键令牌。

![[assets/figures/papers/paper_list_l953_https_arxiv_org_abs_2602_23734/figures/010_Figure_4.jpg]]
*Figure 4: Ablation Study on Progressive Pruning. Performance and the number of vision tokens are reported as the keep ratio decreases and CE, DTE, and STE are progressively enabled for the RGB-based tracker (top) and unified tracker (bottom)*

### 剪枝位置消融

Table 13（RGB 跟踪）和 Table 6（统一跟踪）对 CTEM 插入位置进行了消融。在 12 层 ViT 主干上，配置 #3（CE 在层 [3, 6, 9]，DTE 在层 [4, 7, 10]）在性能-效率权衡上最优。过早剪枝（如层 1–2）会破坏早期特征提取，过晚剪枝（如层 10–12）则压缩收益有限。对于 24 层 HiViT 主干（Table 6），最优配置遵循类似的“均匀间隔、交替剪枝”原则。

### 效率分析

Table 8 报告了 GPU（NVIDIA 1080Ti）和 CPU（Intel Xeon Gold 6226R）上的延迟与训练时间。UTPTrack 的 CTEM 模块引入的每层延迟极低，整体推理速度在 GPU 上接近甚至略快于基线（因令牌减少降低了后续层的计算量）。训练时间与基线相当，因为剪枝操作本身是轻量级的，无需额外可学习参数。

![[assets/figures/papers/paper_list_l953_https_arxiv_org_abs_2602_23734/figures/012_Table_8.jpg]]
*Table 8: Efficiency comparison. Lat.: per-layer backbone latency. GPU: NVIDIA 1080Ti; CPU: Intel Xeon Gold 6226R@2.90GHz*

### 失败模式与局限性

1. **极高压缩率下的回归精度退化**：当令牌保留率低于 30% 时，零填充策略对边界框回归精度的影响开始显现。被剪枝的令牌位置被填充为零，这在高压缩率下可能导致空间信息损失，尤其影响小目标和快速运动场景的定位精度。

2. **剪枝配置的手工依赖性**：当前最优的剪枝层配置（如 #3）是针对特定 ViT 主干手动搜索得到的。该方法可能无法直接泛化到其他架构（如 Swin Transformer 或不同深度的 ViT），需要针对新主干重新进行消融搜索。

3. **文本引导剪枝的鲁棒性未充分验证**：实验假设语言描述是精确且可用的。当语言描述模糊、错误或缺失时，文本引导剪枝的性能退化程度尚未被系统评估。此外，CLIP-L 文本编码器带来约 85M 额外参数，对轻量化部署构成一定负担。

4. **嵌入式设备实时性未验证**：尽管在桌面级 GPU 上展示了良好的加速效果，但在资源极度受限的嵌入式平台（如移动端 NPU、边缘计算设备）上的实时性尚未评估。

5. **长时跟踪中的模板更新**：令牌类型感知先验依赖于初始帧的边界框标注。在长时跟踪场景中，目标外观可能发生显著变化，静态模板的边界框先验是否需要随时间自适应调整，目前仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l953_https_arxiv_org_abs_2602_23734/figures/007_Table_4.jpg]]
*Table 4: Ablation Study on RGB-based Trackers. ∆ denotes the averaged performance change from the to row above*

![[assets/figures/papers/paper_list_l953_https_arxiv_org_abs_2602_23734/figures/009_Table_5.jpg]]
*Table 5: Ablation Study on Unified Trackers. ∆ denotes the average performance change from the row above*

## 方法谱系与知识库定位

### 与基线方法的关系

UTPTrack 直接建立在单流 Transformer 跟踪器的基础上，其核心基线为 **OSTrack**（RGB 跟踪）和 **SUTrack**（统一跨模态跟踪）。这两个基线均采用拼接搜索区域（SR）、静态模板（ST）和动态模板（DT）令牌的单流架构，不做任何令牌剪枝。UTPTrack 的贡献在于首次将令牌剪枝从孤立组件扩展为跨组件联合压缩，即同时处理 SR、DT 和 ST 三类视觉令牌。

在令牌剪枝方法谱系中，UTPTrack 与以下工作形成对照：

- **CE（Candidate Elimination）**：仅在搜索区域上执行剪枝，不涉及动态模板和静态模板。UTPTrack 将其作为候选消除模块（CE）的基础，但额外引入了 DTE 和 STE，并在跨组件注意力引导下统一调度。
- **ToMe**：通过令牌合并减少冗余，而非直接丢弃。UTPTrack 采用更激进的剪枝策略，在保持精度的前提下实现了更高的压缩率。
- **EViT** 和 **DynamicViT**：通用视觉 Transformer 的令牌剪枝方法，未针对跟踪任务中的多组件结构进行专门设计。UTPTrack 与之不同之处在于：（1）利用跟踪特有的静态模板中心令牌作为跨组件相似度参考；（2）引入边界框空间先验稳定静态模板剪枝；（3）在统一跟踪中引入文本引导的剪枝机制。

从跟踪范式角度看，UTPTrack 属于**单流跟踪器**的轻量化扩展。与两流跟踪器（如 Siamese 系列）不同，单流设计天然支持跨组件注意力交互，这为 UTPTrack 复用注意力权重进行令牌重要性估计提供了基础。该方法无需重新训练或修改主干结构，可作为插件适配任何基于 Transformer 的跟踪器。

### 适用边界

UTPTrack 的适用边界由以下几个维度定义：

**架构兼容性**：实验在 12 层 ViT 主干（RGB 跟踪）和 24 层 HiViT 主干（统一跟踪）上验证。剪枝层配置（如 CE 在层 [3, 6, 9]、DTE 在层 [4, 7, 10]）是针对这些特定主干手工选择的。对于不同深度或不同注意力模式的 Transformer 架构，该配置可能需要重新搜索。

**跟踪模态**：UTPTrack 覆盖 RGB 跟踪和统一跨模态跟踪（RGB-D、RGB-T、RGB-E、RGB-Lang）。在 RGB 跟踪中，剪枝仅依赖视觉注意力；在统一跟踪中，文本引导剪枝依赖 CLIP-L 文本编码器（额外 +85M 参数），这可能在资源受限场景下成为部署瓶颈。

**压缩率范围**：控制预算实验覆盖了从轻度压缩（保留约 87% 令牌）到重度压缩（保留约 35% 令牌）的范围。在 65%–70% 令牌剪枝率下，UTPTrack 仍能保持 99.3%–99.7% 的基线性能。但在极端压缩率（>70%）下，零填充策略对边界框回归精度的影响缺乏严格的理论分析，实际部署需谨慎验证。

**实时性**：实验在 NVIDIA 1080 Ti GPU 和 Intel Xeon Gold 6226R CPU 上测量延迟，UTPTrack-O384 的 GPU FPS 从 40 提升至 47。但未在资源极度受限的嵌入式设备（如移动端 NPU、边缘计算平台）上进行实时性评估，该场景下的适用性需要进一步验证。

### 局限与开放问题

**已知局限**：

1. **剪枝配置的手工选择**：CTEM 的插入层位置和保留率是人工设定的固定配置，缺乏自适应机制。不同主干或不同任务可能需要重新调参，泛化成本较高。
2. **文本引导的鲁棒性未验证**：当语言描述不精确、部分缺失或与视觉内容不一致时，文本引导剪枝的性能是否会退化，论文未提供消融分析。
3. **长时跟踪的模板更新**：令牌类型感知剪枝依赖静态模板的边界框先验。在长时跟踪中，目标外观可能发生剧烈变化，初始边界框先验是否会随时间失效，需要进一步研究。
4. **零填充的理论分析缺失**：剪枝后令牌位置用零填充以保持序列长度不变，这种操作对后续注意力计算和边界框回归头的理论影响尚未被严格分析。

**开放问题**：

1. 该联合剪枝框架是否可以适配到其他跟踪范式，如基于相关滤波的跟踪器或两流 Transformer 跟踪器？单流架构的跨组件注意力是 UTPTrack 的核心依赖，迁移到其他范式可能需要重新设计重要性估计机制。
2. 是否可以利用元学习或强化学习动态选择剪枝层和保留率，以替代当前的人工固定配置？这可以显著降低部署调参成本。
3. 在更高压缩率（>80%）下，是否可以通过引入令牌重建损失或知识蒸馏来进一步稳定精度？
4. 对于 RGB-Lang 跟踪，是否可以探索更轻量的文本编码器替代 CLIP-L，以降低统一跟踪变体的参数量开销？

## 原文 PDF

![[paperPDFs/CVPR_2026/UTPTrack_Towards_Simple_and_Unified_Token_Pruning_for_Visual_Tracking.pdf]]
