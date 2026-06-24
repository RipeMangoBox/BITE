---
title: "UniFusion: A Unified Image Fusion Framework with Robust Representation and Source-Aware Preservation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UniFusion_A_Unified_Image_Fusion_Framework_with_Robust_Representation_and_Source_Aware_Preservation.pdf
project_link: null
code_link: "https://github.com/dusongcheng/UniFusion"
aliases:
- UniFusion
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过引入DINOv3自监督语义先验实现模态一致性特征提取，并结合重建对齐损失与双层优化框架，可以解耦并平衡特征重建和融合目标，从而增强源信息保持和跨任务泛化。
primary_logic: 将图像融合与源信息重建构建为双层优化问题，利用DINOv3的强语义先验，能够将特征编码和融合策略解耦并协调优化，实现统一的、泛化性强的融合框架。
claims:
- UniFusion在多个红外-可见光融合基准（M3FD, TNO, RoadScene）上一致超越现有通用融合算法，尤其在VIF、Q_abf、Q_y等感知指标上提升显著。
- 消融实验证明，去除适配器、DINOv3编码器、重建对齐或双层优化任一组件均导致性能下降，其中适配器和双层优化的移除对信息保留指标影响最大。
- M3FD (红外-可见光融合) 上 MI ↑ = 4.268
- 将图像融合与源信息重建构建为双层优化问题，利用DINOv3的强语义先验，能够将特征编码和融合策略解耦并协调优化，实现统一的、泛化性强的融合框架。
---

# UniFusion: A Unified Image Fusion Framework with Robust Representation and Source-Aware Preservation

> [!tip] 核心洞察
> 将图像融合与源信息重建构建为双层优化问题，利用DINOv3的强语义先验，能够将特征编码和融合策略解耦并协调优化，实现统一的、泛化性强的融合框架。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniFusion：兼顾鲁棒表示与源感知保持的统一图像融合框架 |
| 英文题名 | UniFusion: A Unified Image Fusion Framework with Robust Representation and Source-Aware Preservation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.14214) · [Code](https://github.com/dusongcheng/UniFusion) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UniFusion |
| Dataset | M3FD |

> [!tip] 效果简介
> - M3FD (红外-可见光融合) 上，MI ↑ 4.268 vs 3.776 (CDDFuse) (+0.492)。

## 概述

图像融合旨在将来自不同传感器或拍摄设置的互补信息整合为一幅信息更丰富的图像，但现有方法普遍受限于**任务特定的架构设计**与**深层特征传播中的信息损失**，难以在多样条件下稳健地编码和保持异构信号。UniFusion 将图像融合与源信息重建构建为一个**双层优化问题**，利用冻结的 DINOv3 自监督语义先验实现模态一致的特征提取，并通过重建对齐损失将特征编码与融合策略解耦并协调优化，从而增强源信息保持和跨任务泛化能力。

在方法定位上，UniFusion 相对于现有的通用融合模型（如 **CDDFuse** (Zhao et al., CVPR 2023)、**TC-MoA** (Zhu et al., CVPR 2024)、**SwinFusion** (Ma et al., IEEE/CAA JAS 2022) 等）做出了三处关键改变：用冻结的 DINOv3 ViT 骨干结合轻量级多层适配器替代特定任务的 CNN/Transformer 编码器；以多个交叉注意力模块动态建模跨模态依赖性，取代简单的特征拼接或自注意力；将训练目标从单一的融合损失扩展为融合损失与自监督 L1 重建对齐损失的联合，并通过双层优化交替更新内层重建参数和外层融合参数。

主要实验结果（Table 1）显示，UniFusion 在 M3FD、TNO、RoadScene 等多个红外-可见光融合基准上一致超越现有通用融合算法，尤其在 MI（M3FD 上 4.268 vs. CDDFuse 的 3.776）、VIF、Q_abf、Q_y 等感知指标上提升显著。消融实验（Table 2）进一步证实，移除适配器、DINOv3 编码器、重建对齐或双层优化任一组件均导致性能下降，其中适配器和双层优化的移除对信息保留指标影响最大，验证了各模块在源感知保持中的因果作用。

## 背景与动机

图像融合旨在将来自不同传感器或成像条件的多幅源图像整合为一幅信息更丰富、更鲁棒的单一表示，从而为下游视觉任务提供高质量的输入。该领域涵盖红外–可见光融合、多曝光融合、多聚焦融合和医学图像融合等多种任务，核心挑战在于如何在保留各模态关键信息的同时生成视觉自然、语义连贯的融合结果。

近年来，深度学习极大地推动了图像融合的发展。基于卷积神经网络（CNN）和Transformer的方法通过设计精巧的编码器–融合器–解码器架构，在特定任务上取得了令人瞩目的性能。然而，现有方法存在一个根本性的瓶颈：**它们普遍依赖任务特定的架构和深层特征传播，导致在多样化成像条件下难以稳健地编码异构信号，造成模态表示不一致和信息损失**。具体而言，大多数方法将特征提取和融合策略紧密耦合，使得模型在面对不同模态组合时缺乏灵活性和泛化能力。深层网络中的信息衰减进一步加剧了源图像关键细节的丢失，限制了融合质量的进一步提升。

从方法谱系来看，现有融合框架可大致分为三类。第一类是基于分解的方法，如 **DeFuse**（Liang et al., ECCV 2022）和 **CDDFuse**（Zhao et al., CVPR 2023），它们将图像显式分解为基部和细节分量再分别融合，虽在一定程度上提升了信息保持能力，但分解过程本身可能引入伪影且对模态差异敏感。第二类是端到端的统一融合网络，如 **U2Fusion**（Xu et al., TPAMI 2020）和 **SwinFusion**（Ma et al., IEEE/CAA JAS 2022），它们通过统一的网络架构处理多种融合任务，但在面对跨模态语义鸿沟时，其特征编码器难以提取模态一致的表征。第三类方法尝试引入自适应机制，如 **TC-MoA**（Zhu et al., CVPR 2024）通过任务定制化混合适配器增强灵活性，但其优化目标仍将编码和融合捆绑在一起，未能从根本上解耦这两个相互制约的学习过程。

上述方法的共同缺陷指向一个核心问题：**缺乏一种能够在多样条件下稳健提取模态一致性特征，同时有效保留各源图像关键信息的机制**。当编码器被迫同时服务于特征提取和融合目标时，模态特定的语义信息往往在深层传播中被稀释或扭曲，导致融合结果在信息丰富度和视觉保真度之间难以兼得。

UniFusion的提出正是为了突破这一瓶颈。其核心洞察在于：**将图像融合与源信息重建构建为双层优化问题，利用强语义先验将特征编码和融合策略解耦并协调优化，从而实现统一的、泛化性强的融合框架**。通过引入冻结的DINOv3自监督语义骨干作为模态一致性特征提取器，UniFusion能够为异构输入提供鲁棒的语义锚点；同时，通过内层重建对齐和外层融合优化的双层架构，模型得以在保留模态特定信息与整合互补信息之间取得精细平衡。这一设计从根本上改变了传统融合框架中编码与融合目标相互干扰的局面，为通用图像融合提供了一条新的技术路径。

## 核心创新

UniFusion 的核心创新在于将图像融合重新构建为一个**双层优化问题**，通过解耦特征重建与融合目标，系统性地解决了现有通用融合方法中模态一致性表示缺失与源信息损失两大瓶颈。其关键改动体现在三个紧密耦合的“changed slots”上。

### 1. 模态一致性特征提取：冻结 DINOv3 + 轻量适配器

现有融合方法（如 **SwinFusion** (Ma et al., IEEE/CAA JAS 2022)、**CDDFuse** (Zhao et al., CVPR 2023)）通常依赖任务特定的 CNN 或 Transformer 编码器，这些编码器在深层特征传播过程中容易丢失模态特有的精细信息，且缺乏跨模态的语义一致性先验。

UniFusion 用**冻结的 DINOv3 ViT 骨干网络**替代传统编码器，直接注入自监督预训练获得的强语义先验，使不同模态的特征在语义空间天然对齐。在此基础上，引入**轻量级多层适配器**对 ViT 的多层级特征进行层次化重标定，动态调制模态特定信息，而非让编码器自行“摸索”跨模态对应关系。消融实验证实，移除适配器会导致模型无法平衡双模态表示，空间特征整合的连贯性显著受损（Table 2, Section 4.6）；用标准 Transformer 替换 DINOv3 编码器则使高层次语义先验缺失，融合图像的感知质量明显下降。

### 2. 动态跨模态交互：交叉注意力融合

基线方法普遍采用直接特征拼接、相加或简单自注意力进行特征交互，难以显式建模跨模态依赖关系。UniFusion 在融合阶段部署**四个交叉注意力模块**，对适配后的双模态特征进行逐层动态交互。这一设计使融合网络能够根据输入内容自适应地选择性地整合互补信息，而非采用固定的融合策略。该改动与 DINOv3 特征提取器协同工作——语义对齐的表示降低了交叉注意力学习跨模态对应关系的难度。

### 3. 解耦优化策略：重建对齐损失 + 双层优化

这是 UniFusion 最根本的方法论创新。传统方法（如 SwinFusion）使用单一融合损失联合优化编码器与融合器，导致特征提取和融合目标相互干扰，难以有效保留源信息。

UniFusion 在融合损失之外引入**自监督 L1 重建对齐损失**，并构建双层优化框架：
- **内层优化**：以较大学习率 $\eta_L$ 快速更新重建相关参数 $\phi$，最小化重建损失 $\mathcal{L}_{\mathrm{rec}}$，迫使适配特征保持模态特定的语义信息；
- **外层优化**：以较小学习率 $\eta_U$ 缓慢更新融合参数 $\theta$，在重建约束下优化融合损失 $\mathcal{L}_{\mathrm{fuse}}$，并施加指数移动平均正则化以稳定训练。

这一解耦机制使得特征编码和融合策略能够协调优化而非相互妥协。消融实验给出了最有力的因果证据：**移除双层优化（w/o Bilevel Optimization）** 导致信息丰富度（MI）和视觉质量（VIF）出现最显著的衰退（Table 2），表明解耦重建与融合目标对源信息保持至关重要；**去除重建对齐（w/o Reconstruction）** 则使编码特征丧失模态特定语义，纹理清晰度与跨模态互补性降低（Figure 8）。

## 整体框架

UniFusion 将图像融合建模为一个双层优化问题，通过解耦特征重建与融合策略，实现统一的、泛化性强的融合框架。其核心洞察在于：利用 DINOv3 自监督预训练模型提供的强语义先验，将模态一致性特征提取与源信息保持分别交由内层重建和外层融合协同优化，从而克服现有方法因任务特定架构和深层特征传播导致的信息损失。

框架整体结构如 Figure 2 所示，由四条关键流水线构成：

![[assets/figures/papers/paper_list_l952_https_arxiv_org_abs_2603_14214/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed UniFusion framework*

1. **DINOv3 语义骨干**：两个冻结的 DINOv3 ViT 模型分别对输入图像 $I_x$ 和 $I_y$ 提取多层级语义特征，为跨模态对齐提供一致性先验。该设计替代了传统任务特定的 CNN 或 Transformer 编码器，使特征空间天然具备稳健的语义结构。

2. **多层适配器**：轻量级层次化特征重标定模块接收 DINOv3 的多级输出，将其转换为模态对齐的嵌入 $z_x, z_y$。适配器是连接异构模态的关键桥梁——消融实验表明，移除适配器后模型无法动态调制模态特定信息，导致 MI、VIF 等指标显著下降，空间特征整合的连贯性受损。

3. **交叉注意力融合模块**：由四个 Cross-Attention Block 组成，以适配后的特征 $z_x, z_y$ 为输入，动态建模跨模态依赖性，生成融合表示并最终输出融合图像 $I_f = F(z_x, z_y; \theta)$。这与基线方法中简单的特征拼接或自注意力形成对比，使融合过程具备显式的模态交互建模能力。

4. **重建分支**：每个模态配备一个轻量重建分支（四个 Transformer Block 加投影头），从校准特征图 $\hat{\mathbf{F}}_m$ 重建原始模态图像 $\bar{I}_m = R_m(\hat{\mathbf{F}}_m)$。该分支仅在训练时存在，通过自监督 L1 重建对齐损失强制编码特征保留模态特定语义。消融实验证实，去除重建对齐会导致纹理清晰度与跨模态互补性明显下降，编码特征丧失模态特定表示。

上述模块通过**双层优化循环**协同运作：内层以较大学习率 $\eta_L$ 快速更新重建相关参数 $\phi$，最小化重建损失 $\mathcal{L}_{\mathrm{rec}}$；外层以较小学习率 $\eta_U$ 缓慢更新融合参数 $\theta$，最小化融合损失 $\mathcal{L}_{\mathrm{fuse}}$。这种交替梯度下降策略有效解耦了重建与融合目标——消融实验表明，移除双层优化后信息丰富度和视觉质量的衰退最为显著，证明解耦对信息保持至关重要。此外，对融合参数施加指数移动平均 $\theta_{t+1}^{\mathrm{EMA}} = \alpha \theta_t^{\mathrm{EMA}} + (1-\alpha) \theta_{t+1}$，进一步增强了训练稳定性。

整体而言，UniFusion 的输入输出流为：双模态图像 → DINOv3 特征提取 → 适配器特征重标定 → 交叉注意力融合 → 融合图像输出；训练时同步经重建分支恢复源图像，通过双层优化协调两个目标。所有对比方法均采用与 **SwinFusion**（Ma et al., IEEE/CAA JAS 2022）一致的融合损失函数，在相同的数据预处理和训练迭代数下评估，保证了公平性。

## 核心模块与公式推导

UniFusion 将图像融合构建为一个双层优化问题，其核心由四个模块协同完成：**DINOv3语义骨干**、**多层适配器**、**交叉注意力融合模块**和**重建分支**。以下逐一阐述各模块的功能与关键公式。

### DINOv3语义骨干与多层适配器

框架采用两个**冻结的DINOv3 ViT骨干**分别从红外和可见光模态中提取多层级语义特征（Section 3.2）。冻结的DINOv3提供了跨模态一致的高层语义先验，避免了传统编码器在深层传播中的信息损失。为将通用语义特征适配到特定融合任务，每个模态配备一个**轻量级多层适配器**（Adapter），对ViT输出的多级特征进行层次化重标定，生成模态对齐的嵌入表示。适配器的作用在于动态调制模态特定信息，充当异构模态之间的关键桥梁。

### 交叉注意力融合模块

适配后的特征通过**四个交叉注意力模块（Cross-Attention Block）**进行融合（Section 3.1, 4.1）。该模块动态建模跨模态依赖性，而非简单地拼接或相加特征。交叉注意力机制使两路特征能够相互查询和增强，从而生成信息互补的融合表示。

### 重建分支与重建对齐损失

每个模态的校准特征图 $\hat{\mathbf{F}}_m$ 被送入一个轻量级**重建分支** $R_m$，该分支由四个Transformer Block和一个投影头构成，将特征解码回原始图像空间：

$$\bar{I}_m = R_m(\hat{\mathbf{F}}_m) \tag{Eq. 1}$$

重建分支通过自监督的L1重建对齐损失 $\mathcal{L}_{\mathrm{rec}}$ 约束编码特征保留模态特定语义，防止融合过程中源信息的丢失。

### 双层优化框架

UniFusion 的核心创新在于将特征编码与融合策略解耦为**双层优化问题**（Section 3.4）。令编码器 $E$（含DINOv3骨干与适配器）的参数为 $\phi$，融合网络 $F$ 的参数为 $\theta$，则编码与重建过程为：

$$z_x, z_y = E(I_x, I_y; \phi), \quad \hat{I}_x = R_x(z_x; \phi), \quad \hat{I}_y = R_y(z_y; \phi) \tag{Eq. 2}$$

融合过程为：

$$I_f = F(z_x, z_y; \theta) \tag{Eq. 3}$$

双层优化目标形式化为：

$$\phi^* = \arg\min_{\phi} \mathcal{L}_{\mathrm{rec}}(\phi), \quad \theta^* = \arg\min_{\theta} \mathcal{L}_{\mathrm{fuse}}(\theta; \phi^*) \tag{Eq. 4}$$

其中**内层优化**最小化重建损失 $\mathcal{L}_{\mathrm{rec}}$，学习模态感知的鲁棒表示；**外层优化**最小化融合损失 $\mathcal{L}_{\mathrm{fuse}}$（采用与SwinFusion一致的融合损失函数），自适应整合互补信息。

### 一阶交替更新与EMA正则化

为高效近似求解双层优化，UniFusion 采用**一阶交替梯度下降**，内层以较大学习率 $\eta_L$ 快速更新重建参数，外层以较小学习率 $\eta_U$ 缓慢更新融合参数：

$$\begin{array}{rl} \phi_{t+1} = \phi_t - \eta_L \nabla_{\phi_t} \mathcal{L}_{\mathrm{rec}}(\phi_t), \\ \theta_{t+1} = \theta_t - \eta_U \nabla_{\theta_t} \mathcal{L}_{\mathrm{fuse}}(\theta_t; \phi_{t+1}) \end{array} \tag{Eq. 5}$$

此外，对融合参数施加**指数移动平均（EMA）**以增强训练稳定性：

$$\theta_{t+1}^{\mathrm{EMA}} = \alpha \theta_t^{\mathrm{EMA}} + (1-\alpha) \theta_{t+1} \tag{Eq. 6}$$

该交替更新策略有效解耦了重建与融合目标，使模型在保持模态特定语义的同时实现高质量的跨模态信息整合。

### 补充图表

![[assets/figures/papers/paper_list_l952_https_arxiv_org_abs_2603_14214/figures/010_Figure_8.jpg]]
*Figure 8: Visualization of encoded features and fusion results with and without the reconstruction alignment module (“Ours” vs “w/o Rec”). The feature maps are extracted from the encoders for the visible and infrared modalities, respectively*

## 实验与分析

### 主实验结果

UniFusion 在红外–可见光融合、多曝光融合、多聚焦融合及医学图像融合四个主流场景上，与近五年代表性的通用融合方法进行了系统对比，包括基于分解的 **CDDFuse** (Zhao et al., CVPR 2023)、耦合对比学习网络 **CoCoNet** (Liu et al., IJCV 2024)、自监督分解网络 **DeFuse** (Liang et al., ECCV 2022)、Swin Transformer 驱动的 **SwinFusion** (Ma et al., IEEE/CAA JAS 2022)、统一无监督网络 **U2Fusion** (Xu et al., TPAMI 2020)、任务定制混合适配器方法 **TC-MoA** (Zhu et al., CVPR 2024) 以及 **UMFusion** 等。所有方法均采用与 SwinFusion 一致的融合损失函数，在相同的 128×128 随机裁剪预处理和 10k 训练迭代下评估，保证公平性。

在红外–可见光融合基准 **M3FD** 上，UniFusion 取得了 MI 4.268，相比此前最优的 CDDFuse（MI 3.776）提升 +0.492，同时在 VIF（0.899）、Q_abf（0.637）和 Q_y（0.982）等感知质量指标上均达到最优（Table 1）。在 **TNO** 和 **RoadScene** 数据集上，该方法同样在多数指标上保持领先，尤其在衡量边缘保持和结构相似性的 Q_abf 与 Q_y 上优势稳定，表明 DINOv3 语义先验与交叉注意力融合模块能有效保留源图像的互补结构信息。

![[assets/figures/papers/paper_list_l952_https_arxiv_org_abs_2603_14214/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on M3FD, TNO, RoadScene, and MEFB datasets. The best and second best results are highlighted in bold and underline*

在多曝光融合数据集 **MEFB** 上，UniFusion 的 MI 达到 6.861，VIF 达到 1.484，CC 为 0.906，PSNR 为 59.219，四项指标均为最优（Table 1）。多聚焦融合数据集 **MFIF** 的分布图（Figure 3）显示，UniFusion 在五项评价指标上的中位数和均值均稳定处于前两名，且无需针对该任务进行任何微调。医学图像融合数据集 **MIF** 的分布图同样表明，该方法在跨临床案例的泛化稳定性上优于对比方法，高 median 值反映出可靠的融合质量一致性（Figure 3）。

![[assets/figures/papers/paper_list_l952_https_arxiv_org_abs_2603_14214/figures/004_Figure_3.jpg]]
*Figure 3: Quantitative comparison on MIF (top) and MFIF (bottom) datasets. The plots illustrate the distribution of all test samples across five evaluation metrics, where “–” and “◦” indicate the median and mean values, respectively*

### 消融实验

为验证各核心组件的独立贡献，作者在 M3FD、MEFB 和 MFIF 三个数据集上进行了系统消融，分别移除适配器（w/o Adapter）、用标准四层 Transformer 替换 DINOv3 编码器（w/o DINOv3 Encoder）、去除重建对齐分支（w/o Reconstruction）以及移除双层优化机制（w/o Bilevel Optimization）。定量结果汇总于 Table 2。

![[assets/figures/papers/paper_list_l952_https_arxiv_org_abs_2603_14214/figures/009_Table_2.jpg]]
*Table 2: Ablation studies on M3FD, MEFB and MFIF datasets. The best and second best results are highlighted in bold*

- **移除适配器**：MI、VIF 等指标出现明显下降。适配器作为异构模态之间的关键桥梁，其缺失导致模型无法动态调制模态特定信息，空间特征整合的连贯性受损，融合图像在细节保留和跨模态平衡上均劣于完整模型（Table 2, Figure 7）。
- **替换 DINOv3 编码器**：用标准 Transformer 替代冻结的 DINOv3 ViT 骨干后，高层次语义先验缺失，融合图像的感知质量下降。这表明 DINOv3 自监督预训练提供的丰富语义表征对于引导不同模态特征对齐、提升整体视觉质量不可或缺（Table 2）。
- **去除重建对齐**：编码特征丧失了部分模态特定语义表征，导致纹理清晰度与跨模态互补性降低。Figure 8 的可视化对比清晰展示了 w/o Rec 变体在可见光与红外模态特征图中丢失了细粒度结构信息，而完整模型（Ours）保持了更忠实的模态特性。
- **移除双层优化**：这是对信息保持指标（MI）和视觉质量指标（VIF）影响最大的消融项。去除双层优化后，重建目标与融合目标被耦合在单一损失中联合优化，导致特征解耦不充分，训练过程不稳定，信息丰富度和视觉保真度均出现更显著的衰退（Table 2）。这直接验证了将特征重建与融合策略解耦为双层优化问题的核心设计动机。

![[assets/figures/papers/paper_list_l952_https_arxiv_org_abs_2603_14214/figures/008_Figure_7.jpg]]
*Figure 7: Visual comparison of fusion results for different ablation variants on representative samples from the M3FD dataset*

### 关键图表结论

- **Table 1**：UniFusion 在四个基准数据集、多项感知指标上一致超越现有通用融合算法，尤其在红外–可见光融合的 MI、VIF、Q_abf 和多曝光融合的 MI、VIF、PSNR 上优势显著。
- **Table 2**：消融实验证实适配器、DINOv3 编码器、重建对齐和双层优化四个组件对最终性能均有正向贡献，其中适配器和双层优化的移除导致最严重的性能退化。
- **Figure 3**：分布图揭示了 UniFusion 在多聚焦和医学融合任务上的稳定泛化能力，高 median 值和紧凑分布表明其跨样本一致性优于对比方法。
- **Figure 7 & Figure 8**：视觉消融对比直观展示了各组件对空间特征整合和模态特定信息保持的影响，重建对齐模块对于维持纹理细节和跨模态互补性尤为关键。

### 补充图表

![[assets/figures/papers/paper_list_l952_https_arxiv_org_abs_2603_14214/figures/005_Figure_4.jpg]]
*Figure 4: Visual comparison of infrared and visual image fusion results with SOTA methods on M3FD (top) and T&R (bottom) datasets*

![[assets/figures/papers/paper_list_l952_https_arxiv_org_abs_2603_14214/figures/006_Figure_5.jpg]]
*Figure 5: Visual comparison of medical image fusion results with SOTA methods on MIF dataset*

![[assets/figures/papers/paper_list_l952_https_arxiv_org_abs_2603_14214/figures/007_Figure_6.jpg]]
*Figure 6: Visual comparison of multi-exposure image fusion and multi-focus image fusion results with SOTA methods on MEFB and MFIF datasets*

## 方法谱系与知识库定位

### 统一融合框架的演进脉络

图像融合领域长期面临一个核心矛盾：**任务特定架构的性能优势**与**通用框架的泛化需求**之间的张力。早期方法如 **U2Fusion**（Xu et al., TPAMI 2020）率先提出统一无监督融合范式，试图以单一网络覆盖多类融合任务，但其特征提取仍依赖浅层CNN，缺乏对异构模态信号的结构化理解。随后，基于分解的方法如 **DeFuse**（Liang et al., ECCV 2022）和 **CDDFuse**（Zhao et al., CVPR 2023）通过将融合过程拆解为“分解-融合-重建”流水线，显著提升了信息保留能力，CDDFuse更一度成为通用融合的SOTA。与此同时，基于Transformer的 **SwinFusion**（Ma et al., IEEE/CAA JAS 2022）将Swin Transformer引入跨域融合，增强了长程依赖建模，但其深层特征传播仍存在信息损失风险。

**UniFusion的定位**：在上述谱系中，UniFusion并非对分解范式或Transformer架构的简单延续，而是从**优化结构**层面进行了根本性重构。其关键区分在于：

1. **从“联合优化”到“双层解耦”**：现有方法（包括CDDFuse、SwinFusion、TC-MoA等）普遍采用单层联合优化，将特征编码与融合目标捆绑训练。UniFusion则通过双层优化（Eq. 4-5）将重建目标（内层）与融合目标（外层）解耦，使得特征学习不再被融合损失“污染”，从而保留了更完整的模态特定信息。

2. **从“任务定制编码器”到“冻结语义先验+轻量适配”**：与SwinFusion的任务特定Swin Transformer或CDDFuse的手工分解编码器不同，UniFusion采用冻结的DINOv3 ViT作为跨模态一致性先验，仅通过轻量适配器进行领域调制。这一设计避免了深层特征传播中的信息损失，同时显著降低了任务切换时的重训练成本。

3. **与TC-MoA的对比**：**TC-MoA**（Zhu et al., CVPR 2024）同样追求通用融合能力，但其核心是通过任务定制化混合适配器在固定骨干上动态调整。UniFusion与TC-MoA的根本差异在于：TC-MoA的适配器服务于融合目标本身，而UniFusion的适配器服务于**重建对齐**——即先确保编码特征能完整恢复源图像，再进行融合。这一“先重建、后融合”的顺序约束是UniFusion在信息保留指标上超越TC-MoA的关键机制。

### 适用边界与任务覆盖

UniFusion在以下融合任务上展示了统一框架的有效性：

- **红外-可见光融合**（M3FD、TNO、RoadScene）：这是验证信息保留能力的主要战场。UniFusion在MI（4.268 vs. CDDFuse的3.776）、VIF、Q_abf等感知指标上取得一致优势（Table 1）。
- **医学图像融合**（MIF数据集上的PET-MRI融合）：分布图（Figure 3）显示UniFusion在中位数和均值上均保持高位，表明其跨临床案例的稳定性。
- **多曝光融合**（MEFB）：在MI（6.861）、VIF（1.484）、PSNR（59.219）上达到SOTA。
- **多聚焦融合**（MFIF）：无需任务特定微调即位列前二（Figure 3底部）。

**适用边界的推断**：从方法设计出发，UniFusion的适用性依赖于DINOv3语义先验的有效性。对于与自然图像统计分布差异极大的模态（如深度图、某些医学成像模态），冻结的DINOv3骨干可能无法提供有效的语义先验，此时重建对齐的正则化效果可能减弱。论文未在非自然图像分布的场景上进行验证（如SAR-光学融合、遥感多光谱融合），这一边界需要进一步实验确认。

### 局限与开放问题

**已确认的消融证据**（Table 2, Figure 7-8）揭示了各组件的贡献与失效模式：

- **移除适配器**（w/o Adapter）：模型无法动态调制模态特定信息，导致空间特征整合连贯性受损，MI和VIF显著下降。
- **替换DINOv3为标准Transformer**（w/o DINOv3 Encoder）：高层语义先验缺失，融合图像的感知质量退化，表明DINOv3的预训练语义对跨模态对齐至关重要。
- **去除重建对齐**（w/o Reconstruction）：编码特征丧失模态特定语义（Figure 8可视化证实），纹理清晰度和跨模态互补性降低。这是信息损失的直接证据。
- **移除双层优化**（w/o Bilevel Optimization）：信息丰富度（MI）和视觉质量（VIF）出现最显著衰退，说明解耦重建与融合目标对信息保持的贡献超过其他任何单一组件。

**论文未明确讨论的局限**：

1. **计算开销**：双DINOv3编码器（即使冻结）和双层优化的交替更新机制引入了额外的推理和训练成本。论文未报告与CDDFuse、SwinFusion等方法的参数量、FLOPs或推理时间对比，这对实际部署至关重要。
2. **双层优化的收敛性**：Eq. (5)的一阶交替近似依赖于内层学习率$\eta_L$大于外层$\eta_U$的启发式设定，但论文未讨论该近似在理论上与真实双层优化的差距，也未分析不同学习率比例对收敛稳定性的影响。
3. **DINOv3版本依赖性**：框架性能与DINOv3的语义质量强绑定。若未来DINO系列更新导致特征分布变化，当前适配器设计是否需要重新训练或调整，论文未给出指引。

**开放问题**：

- 重建对齐损失（L1重建）是否可能过度约束特征空间，从而在某些场景下抑制有利于融合的跨模态变换？论文未探索重建损失与融合损失之间的权重平衡。
- 双层优化的内层更新步数固定为1步近似，增加内层迭代步数是否能进一步提升特征质量？这涉及训练效率与性能的权衡，论文未进行敏感性分析。
- UniFusion的框架设计是否可扩展至超过两种模态的融合场景（如红外-可见光-深度三模态融合）？交叉注意力模块的扩展方案和计算成本变化尚未讨论。

## 原文 PDF

![[paperPDFs/CVPR_2026/UniFusion_A_Unified_Image_Fusion_Framework_with_Robust_Representation_and_Source_Aware_Preservation.pdf]]
