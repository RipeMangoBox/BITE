---
title: "EfficientVPR: Toward Efficient Visual Place Recognition via Scene-Aware Prompt Tuning and Adaptive Feature Enhancement"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EfficientVPR_Toward_Efficient_Visual_Place_Recognition_via_Scene_Aware_Prompt_Tuning_and_Adaptive_Feature_Enhancement.pdf
project_link: null
code_link: "https://github.com/WiniTang/EfficientVPR"
aliases:
- EfficientVPR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 场景感知的视觉提示微调（SceneVPT）通过 CLS token 注意力权重动态筛选提示，在保留预训练知识的前提下实现样本自适应的特征引导；实例依赖的关键局部特征增强模块利用骨干语义先验强化样本特定局部特征，弥补单阶段方法对细节敏感度的不足。
primary_logic: 利用 ViT 的 CLS token 注意力值自适应地融合旧提示与新提示，无需额外模块即可实现实例级提示调整，既避免了灾难性遗忘又提升了任务适应性；以骨干处理后的提示为语义查询，通过交叉注意力增强多尺度全局特征与方向感知局部特征，从而在不使用重排序的情况下提升了局部判别力。
claims:
- 与同尺度 SOTA 方法相比，EfficientVPR 在 Pitts250k 等 7 个数据集上平均 R@1 达到最高，且特征维度仅为 BoQ 的 28%。
- SceneVPT 在消融实验中显著优于静态 VPT-deep 和顶层选择策略，在所有测试数据集上均获得提升。
- SGFS 模块在 AmsterTime 数据集上带来 6.8% 的 R@1 提升，且显著超越 BoQ 的特征聚合模块。
- 可视化分析显示，SceneVPT 能根据输入图像动态调整注意力区域，而 VPT-deep 和适配器方法无法实现这种灵活性。
---

# EfficientVPR: Toward Efficient Visual Place Recognition via Scene-Aware Prompt Tuning and Adaptive Feature Enhancement

> [!tip] 核心洞察
> 利用 ViT 的 CLS token 注意力值自适应地融合旧提示与新提示，无需额外模块即可实现实例级提示调整，既避免了灾难性遗忘又提升了任务适应性；以骨干处理后的提示为语义查询，通过交叉注意力增强多尺度全局特征与方向感知局部特征，从而在不使用重排序的情况下提升了局部判别力。

| 字段 | 内容 |
|------|------|
| 中文题名 | EfficientVPR：基于场景感知提示微调与自适应特征增强的高效视觉地点识别 |
| 英文题名 | EfficientVPR: Toward Efficient Visual Place Recognition via Scene-Aware Prompt Tuning and Adaptive Feature Enhancement |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Tang_EfficientVPR_Toward_Efficient_Visual_Place_Recognition_via_Scene-Aware_Prompt_Tuning_CVPR_2026_paper.html) · [Code](https://github.com/WiniTang/EfficientVPR) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | EfficientVPR |
| Dataset | Pitts250k-test, MSLS-val, AmsterTime, SVOX Night |

> [!tip] 效果简介
> - Pitts250k-test 上，R@1 95.4 vs — (BoQ 约94.4) (+1.0% (vs BoQ))。
> - MSLS-val 上，R@1 — vs — (FoL 约91.0) (+2.0% (vs FoL))。
> - AmsterTime 上，R@1 — vs — (BoQ) (+5.0% (vs BoQ))。

## 概要

视觉地点识别（Visual Place Recognition, VPR）旨在根据查询图像在参考数据库中检索同一地点的图像。现有单阶段方法在应对极端视角变化、光照剧变和场景外观变迁时，面临一个核心瓶颈：要么依赖大容量模型，要么引入计算密集型的重排序阶段，导致推理效率低、内存占用高，且普遍缺乏对样本特定判别区域的自适应关注。

**EfficientVPR** 针对这一问题提出了一个轻量级单阶段框架，其核心设计包含两项关键创新：

1. **场景感知视觉提示微调（SceneVPT）**：在保留预训练知识的前提下，利用 ViT 的 CLS token 注意力权重动态筛选和融合可学习提示，实现样本自适应的特征引导，无需额外模块即可避免灾难性遗忘。
2. **实例依赖的关键局部特征增强模块**：通过多尺度交互注意力（MsIA）、方向感知局部增强（OLE）和语义引导特征选择（SGFS）三部分协同，以骨干处理后的提示为语义查询，强化多尺度全局特征与方向感知局部特征中的样本特定判别区域。

在方法谱系中，EfficientVPR 定位于单阶段全局描述子方法，但与 **NetVLAD**（Arandjelovic et al., CVPR 2016）、**CosPlace**（Berton et al., CVPR 2022）、**MixVPR**（Ali-bey et al., WACV 2023）、**SALAD**（Izquierdo and Civera, CVPR 2024）、**BoQ**（Ali-Bey et al., CVPR 2024）等代表性工作相比，其关键差异在于以 SceneVPT 替代常见的适配器微调，并显式引入了实例依赖的局部特征增强机制，从而在不使用重排序的情况下提升对细节的判别力。

实验结果表明，基于 DINOv2-small 骨干（约 25M 参数），EfficientVPR 在 Pitts250k、MSLS、AmsterTime、SVOX Night 等 7 个数据集上取得了同尺度模型中最高的平均 R@1，且特征维度仅为 BoQ 的 28%。在效率方面，总推理延迟约 3.1 ms，实现了精度与速度的有利权衡。消融实验证实，SceneVPT 在所有测试数据集上均显著优于静态 VPT-deep，SGFS 在 AmsterTime 上带来 6.8% 的 R@1 提升，且可视化分析显示该方法能根据输入图像动态调整注意力区域（见 **Figure 6**）。



视觉地点识别（Visual Place Recognition, VPR）旨在根据查询图像从大规模地理参考数据库中检索最相似的地点图像，是自动驾驶、机器人导航与增强现实等应用的核心感知能力。近年来，基于深度学习的 VPR 方法取得了显著进展，但现有方案在效率与鲁棒性之间仍存在根本性张力。

**单阶段方法的效率瓶颈**。以 NetVLAD（Arandjelovic et al., CVPR 2016）、CosPlace（Berton et al., CVPR 2022）、MixVPR（Ali-bey et al., WACV 2023）、EigenPlaces（Berton et al., ICCV 2023）、CricaVPR（Lu et al., CVPR 2024）、SALAD（Izquierdo and Civera, CVPR 2024）和 BoQ（Ali-Bey et al., CVPR 2024）为代表的单阶段方法，通过端到端聚合全局描述子实现快速检索，避免了重排序的计算开销。然而，当面临剧烈视角变化、季节更替、光照极端或场景翻新等环境扰动时，这些方法往往缺乏对样本特定判别区域的精细感知能力——它们要么依赖大容量骨干网络（如 DINOv2-L）来弥补判别力不足，要么生成高维描述子以保留更多信息，导致推理延迟和内存占用居高不下。

**两阶段方法的计算代价**。以 R2Former（Zhu et al., CVPR 2023）、SelaVPR（Lu et al., ICLR 2024）和 FoL（Wang et al., AAAI 2025）为代表的两阶段方法，在初始检索后引入重排序阶段，利用局部特征匹配或跨图像关联来提升精度。尽管这类方法在极端场景下表现更强，但其重排序过程通常涉及计算密集型的特征比对或注意力操作，使得单次查询的延迟远超实时性要求，难以部署于资源受限的边缘平台。

**核心瓶颈**。现有单阶段 VPR 方法在应对极端环境变化时，要么采用大容量模型，要么使用计算密集型重排序，导致推理效率低、内存占用高，且缺乏对样本特定判别区域的自适应关注。这一瓶颈的根源在于：微调策略（如 adapter-based fine-tuning）对所有输入施加统一的参数调整，无法根据每张图像的内容动态分配特征提取资源；同时，局部特征增强机制要么缺失，要么与全局描述子割裂，难以在不引入重排序的前提下弥补单阶段方法对细节敏感度的不足。

**本文动机**。针对上述问题，EfficientVPR 提出了一条轻量化单阶段路线：在保留 DINOv2-small（约 25M 参数）这一高效骨干的前提下，通过场景感知的视觉提示微调（SceneVPT）实现样本自适应的特征引导，并辅以实例依赖的关键局部特征增强模块，在不使用重排序的条件下提升局部判别力。其核心洞察在于：利用 ViT 的 CLS token 注意力值自适应地融合旧提示与新提示，无需额外模块即可实现实例级提示调整，既避免了灾难性遗忘又提升了任务适应性；以骨干处理后的提示为语义查询，通过交叉注意力增强多尺度全局特征与方向感知局部特征，从而弥补单阶段方法对关键区域的感知盲区。如 Figure 1 所示，EfficientVPR 在更低特征维度下取得了 7 个数据集上的最高平均 R@1，验证了“轻量骨干 + 自适应微调 + 语义引导局部增强”这一技术路线的有效性。



## 核心方法与创新机理

EfficientVPR 的核心创新围绕一个中心洞察展开：**利用 ViT 的 CLS token 注意力值自适应地融合旧提示与新提示，无需额外模块即可实现实例级提示调整，既避免了灾难性遗忘又提升了任务适应性；以骨干处理后的提示为语义查询，通过交叉注意力增强多尺度全局特征与方向感知局部特征，从而在不使用重排序的情况下提升了局部判别力。** 基于此洞察，方法在两个关键维度上对现有 VPR 范式进行了改造。

### 1. 场景感知视觉提示微调（SceneVPT）

现有单阶段 VPR 方法在微调策略上主要采用适配器（Adapter）方案，如 **CricaVPR**（Lu et al., CVPR 2024）和 **SelaVPR**（Lu et al., ICLR 2024），这类方法通过插入额外可学习模块来适配下游任务，但缺乏对样本特定判别区域的自适应关注。SceneVPT 改变了这一范式：它从 VPT-deep 的静态提示机制出发，引入基于 CLS token 注意力权重的动态提示选择机制。

其核心机制如下：在第 $i$ 层，利用第 $i-1$ 层编码器中 CLS token 对所有提示的平均注意力权重 $s_j$，经归一化后得到 $s_j^{\prime} = s_j / \sum_{k=1}^{N_p} s_k$，再通过带可学习阈值 $\gamma$ 的 sigmoid 函数计算筛选权重：

$$\alpha_{ij} = \mathrm{sigmoid}(s_j^{\prime} - \gamma)$$

最终用于微调的提示 $\hat{\mathbf{P}}_{i-1}$ 由上一层的样本相关提示 $\mathbf{Z}_{i-1}^P$ 与新引入的可学习提示 $\mathbf{P}_i$ 按权重融合而成：

$$\hat{\mathbf{P}}_{i-1} = \alpha_i \cdot \mathbf{Z}_{i-1}^P + (1_{N_p} - \alpha_i) \cdot \mathbf{P}_i, \quad i \ge 2$$

这一设计的瓶颈突破在于：**无需额外模块**，仅利用 ViT 已有的自注意力结构即可实现实例级提示调整。当输入图像发生变化时，CLS token 对不同提示的关注度随之改变，从而自动保留与当前场景相关的旧提示、替换不相关部分。这既保留了预训练知识（避免灾难性遗忘），又实现了样本自适应的特征引导。

消融实验（Table 3）证实了这一设计的有效性：SceneVPT 在所有测试数据集上均显著优于 VPT-deep 和无提示基线。Table 4 进一步表明，基于注意力值的动态加权策略优于随机选择和 Top-k 硬选择策略，验证了“软筛选”保留更全面信息的优势。可视化分析（Figure 6）显示，SceneVPT 能根据输入图像动态调整注意力区域，而 VPT-deep 和适配器方法无法实现这种灵活性。

### 2. 实例依赖的关键局部特征增强

传统单阶段方法（如 **NetVLAD**、**CosPlace**、**MixVPR**、**BoQ** 等）主要依赖全局描述子，缺乏对样本特定局部判别区域的显式建模。EfficientVPR 通过三个协同子模块改变了这一局面：

- **多尺度交互注意力（MsIA）**：恢复骨干输出的空间结构，通过交叉注意力融合多尺度上下文信息，增强全局特征的表达能力。
- **方向感知局部增强（OLE）**：通过非对称卷积分别提取垂直和水平方向的局部描述子，并利用正交投影分解获得几何互补的特征：

  $$\mathbf{f}_h^{\prime} = \mathbf{f}_h - \frac{S}{\|\mathbf{f}_v^{\prime}\|_2 + \varepsilon} \cdot \mathbf{f}_v^{\prime}$$

  这一设计使局部特征对方向性变化具有更强的鲁棒性。
- **语义引导特征选择（SGFS）**：这是整个增强模块的“灵魂”。它以骨干处理后的提示特征 $\mathbf{f}_g^{\prime}$ 作为语义查询，通过交叉注意力对多尺度和方向感知局部特征进行筛选增强：

  $$\mathbf{f}_l^{\prime} = \mathrm{Attention}(\mathbf{f}_g^{\prime}, \mathbf{f}_l, \mathbf{f}_l)$$

  由于 $\mathbf{f}_g^{\prime}$ 本身已通过 SceneVPT 获得了样本特定的语义信息，SGFS 能够自适应地强化与当前查询最相关的局部区域，而抑制无关或误导性特征。

消融实验（Table 5）表明，SGFS 在 AmsterTime 数据集上带来 **6.8% 的 R@1 提升**。Table 6 进一步显示，SGFS 的样本自适应查询机制显著优于使用 BoQ 块替换的方案，证明了语义引导相比静态聚合的优越性。这一设计使得 EfficientVPR 在不使用两阶段重排序的情况下，弥补了单阶段方法对细节敏感度的不足。

### 3. 轻量化骨干选择

与 **R2Former**（Zhu et al., CVPR 2023）、**FoL**（Wang et al., AAAI 2025）等方法使用 DINOv2-L 等大容量骨干不同，EfficientVPR 选择 **DINOv2-small**（约 25M 参数）作为基础网络。这一选择本身并非创新，但与 SceneVPT 和 SGFS 的协同设计使其成为可能：轻量骨干通过动态提示微调获得任务适应性，通过语义引导增强弥补容量不足带来的判别力损失。最终，EfficientVPR 在特征维度仅为 BoQ 的 28% 的条件下，取得了 DINOv2-S 同类模型中的 SOTA 性能（Table 1, Table 2）。

### 创新总结

EfficientVPR 的三个 changed slots——微调策略（SceneVPT）、局部特征增强（MsIA+OLE+SGFS）、骨干选择（DINOv2-S）——并非孤立改进，而是围绕“实例自适应”这一核心洞察的协同设计。SceneVPT 提供样本特定的语义线索，SGFS 利用这些线索增强局部判别力，轻量骨干则确保整体效率。这种“轻量化骨干 + 动态提示微调 + 语义引导增强”的组合，为单阶段 VPR 方法在效率与精度之间找到了新的平衡点。



EfficientVPR 是一个轻量化的单阶段视觉地点识别框架，其核心设计目标是在保持强判别力的同时实现高推理效率与低特征维度。如图 2 所示，整个 pipeline 由 DINOv2-small 骨干、场景感知视觉提示微调模块（SceneVPT）以及实例依赖的关键局部特征增强模块三大部分串联构成。

**输入-输出流**：给定一张查询图像，首先由冻结的 DINOv2-small 骨干提取 patch tokens 与 CLS token。SceneVPT 模块在骨干的每一层 Transformer 编码器中动态注入并筛选可学习提示（prompts），利用 CLS token 对提示的注意力权重实现样本自适应的提示融合，从而在保留预训练通用知识的前提下为下游任务提供场景特定的特征引导。随后，精炼后的提示特征与骨干输出的多尺度 patch 特征一同进入局部增强阶段：多尺度交互注意力（MsIA）恢复空间结构并融合跨尺度上下文，方向感知局部增强器（OLE）通过非对称卷积与正交投影提取几何互补的局部描述子，语义引导特征选择器（SGFS）以骨干处理后的提示为语义查询，通过交叉注意力对多尺度和方向感知局部特征进行样本特定的关键区域强化。最终，增强后的全局与局部特征经线性投影压缩至 3456 维，用于高效的图像检索。

**模块关系**：SceneVPT 是框架的“任务适配引擎”，负责在不引入额外模块的前提下实现实例级的提示调整，避免灾难性遗忘的同时提升任务适应性。MsIA 与 OLE 构成“多尺度-方向协同提取”子流水线，分别从全局结构完整性和局部几何互补性两个维度丰富特征表示。SGFS 则充当“语义筛选器”，利用 SceneVPT 输出的样本依赖语义线索，精准增强与当前查询最相关的判别性局部区域——这正是 EfficientVPR 在不使用重排序的条件下仍能有效应对极端视角变化和外观漂移的关键机制（参见 Figure 4 中的失败案例与缓解效果示意）。

**效率设计**：整个框架基于仅约 25M 参数的 DINOv2-small 构建，特征维度仅为 BoQ 的 28%，在 Pitts250k-test 上的单查询总延迟仅 3.1 ms（Table 2），实现了精度-效率的显著权衡。

### 补充图表

![[assets/figures/papers/paper_list_l2153_https_openaccess_thecvf_com_content_CVPR2026_html_Tang_EfficientVPR_Towa/figures/002_Figure_2.jpg]]
*Figure 2: The overall architecture of our one-stage method. To maintain strong discriminative power while ensuring lightweight efficiency, we employ DINOv2-small as the backbone with SceneVPT for fine-tuning, preserving generalizable features while adapting to instance-specific characteristics. During feature enhancement, EfficientVPR uses MsIA and OLE to extract multi-scale global features and orientation-aware local features respectively, while SGFS performs instance-specific local feature enhancement of key regions based on sample-dependent semantic cues obtained from backbone*

![[assets/figures/papers/paper_list_l2153_https_openaccess_thecvf_com_content_CVPR2026_html_Tang_EfficientVPR_Towa/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of viewpoint-induced matching failure. The first two images depict the same location, while the third shows a different but similar place. Dramatic viewpoint shifts and seasonal appearance variations cause trees in the query image (red border in the first picture) to become non-overlapping regions absent in the correct reference match. Current one-stage methods tend to be misled by these irrelevant features, producing false matches to incorrect locations with visually similar nonoverlapping elements (red border in the third picture). By enhancing the discriminative representation of task-relevant and samplespecific key local regions and structural information, our method effec...*



### 场景感知视觉提示微调（SceneVPT）

SceneVPT 是 EfficientVPR 的核心微调策略，其本质是在 VPT-deep 的基础上引入**样本自适应的动态提示选择机制**，仅利用 ViT 自身的 CLS token 注意力权重即可实现，无需额外模块。

**动机**：传统 VPT-deep 在所有层使用固定的可学习提示，无法根据输入图像的特性动态调整；而适配器方法（如 CricaVPR、SelaVPR 所用）虽然可微调，但参数量较大且缺乏对样本特定判别区域的显式关注。

**机制**：在第 $i$ 层，SceneVPT 利用第 $i-1$ 层编码器中 CLS token 到各提示 token 的平均注意力权重 $s_j$，先进行归一化：

$$s_j^{\prime} = s_j / \sum_{k=1}^{N_p} s_k \quad \text{(Eq. 2)}$$

随后通过可学习阈值 $\gamma$ 计算每个提示的筛选权重：

$$\pmb{\alpha}_{ij} = \mathrm{sigmoid}(s_j^{\prime} - \gamma) \quad \text{(Eq. 1)}$$

最终，当前层使用的提示 $\hat{\mathbf{P}}_{i-1}$ 由上一层的输出提示 $\mathbf{Z}_{i-1}^{P}$ 与新引入的可学习提示 $\mathbf{P}_i$ 按权重融合：

$$\hat{\mathbf{P}}_{i-1} = \pmb{\alpha}_i \cdot \mathbf{Z}_{i-1}^{P} + (\mathbf{1}_{N_p} - \pmb{\alpha}_i) \cdot \mathbf{P}_i, \quad i \ge 2 \quad \text{(Eq. 5)}$$

其中 $\pmb{\alpha}_i \in \mathbb{R}^{N_p}$，$\mathbf{1}_{N_p}$ 为全 1 向量。第 $i$ 层编码器的完整输入为：

$$[\mathbf{Z}_i^{CLS}, \mathbf{Z}_i^{P}, \mathbf{Z}_i] = L_i([\mathbf{Z}_{i-1}^{CLS}, \hat{\mathbf{P}}_{i-1}, \mathbf{Z}_{i-1}]), \quad i \ge 2 \quad \text{(Eq. 4)}$$

**因果机制**：当某提示的 CLS 注意力分数 $s_j^{\prime}$ 高于阈值 $\gamma$ 时，$\alpha_{ij} \to 1$，该提示被保留；反之则被新提示替换。这使得模型能**动态保留与当前样本相关的旧知识，同时注入新的任务适应能力**，避免灾难性遗忘。

---

### 多尺度交互注意力（MsIA）

MsIA 旨在恢复 ViT patch token 的空间结构，并通过交叉注意力融合多尺度上下文信息。它将 DINOv2-small 输出的 patch tokens 重塑为 2D 空间网格，利用不同扩张率的卷积提取多尺度特征图，再以全局平均池化后的特征为查询，通过交叉注意力聚合多尺度信息，得到结构感知的全局描述子。

---

### 方向感知局部增强器（OLE）

OLE 通过非对称卷积分别提取垂直和水平方向的局部特征。设垂直方向精炼后的描述子为 $\mathbf{f}_v^{\prime}$，水平特征为 $\mathbf{f}_h$，二者之间的空间相关性为 $S$。为获得几何互补的局部特征，OLE 通过正交投影移除水平特征中与垂直描述子相关的分量：

$$\mathbf{f}_h^{\prime} = \mathbf{f}_h - \frac{S}{\|\mathbf{f}_v^{\prime}\|_2 + \varepsilon} \cdot \mathbf{f}_v^{\prime} \quad \text{(Eq. 6)}$$

其中 $\varepsilon$ 为防止除零的小常数。这一操作确保 $\mathbf{f}_h^{\prime}$ 与 $\mathbf{f}_v^{\prime}$ 在特征空间中正交，从而捕捉方向互补的判别信息。

---

### 语义引导特征选择器（SGFS）

SGFS 是实例依赖关键局部特征增强的核心模块。它首先对 SceneVPT 最后一层输出的提示特征 $\mathbf{Z}_L^P$ 进行自注意力精炼，得到语义查询：

$$\mathbf{f}_g^{\prime} = \mathbf{Z}_L^P + \mathrm{Attention}(\mathbf{Z}_L^P, \mathbf{Z}_L^P, \mathbf{Z}_L^P) \quad \text{(Eq. 8)}$$

随后，以 $\mathbf{f}_g^{\prime}$ 为查询，对 MsIA 和 OLE 输出的多尺度与方向感知局部特征 $\mathbf{f}_l$ 进行交叉注意力增强：

$$\mathbf{f}_l^{\prime} = \mathrm{Attention}(\mathbf{f}_g^{\prime}, \mathbf{f}_l, \mathbf{f}_l) \quad \text{(Eq. 9)}$$

**因果机制**：精炼后的提示特征 $\mathbf{f}_g^{\prime}$ 蕴含了与当前样本和任务最相关的语义先验。以它为查询，交叉注意力机制自动筛选并增强局部特征中与任务相关的关键区域，抑制背景噪声和视角变化带来的干扰区域，从而在不使用重排序的情况下提升局部判别力。消融实验表明，SGFS 在 AmsterTime 数据集上带来 **6.8% 的 R@1 提升**（Table 5），且显著优于使用 BoQ 块替换的方案（Table 6）。

---

### 特征压缩

最终，增强后的全局和局部特征经拼接后通过线性投影压缩至 3456 维，在保持判别力的同时大幅降低内存占用——仅为 BoQ 特征维度的 **28%**（Table 2）。

### 补充图表

![[assets/figures/papers/paper_list_l2153_https_openaccess_thecvf_com_content_CVPR2026_html_Tang_EfficientVPR_Towa/figures/003_Figure_3.jpg]]
*Figure 3: SceneVPT Overview. Our SceneVPT extends VPTdeep via adaptive prompt selection, dynamically adjusting to input characteristics based solely on the backbone’s CLS token*



## 实验与关键发现

### 主实验结果与效率分析

EfficientVPR 在七个公开 VPR 基准上进行了全面评估，涵盖大规模检索（Pitts250k-test、MSLS-val）、长期时间跨度（AmsterTime）、昼夜与天气变化（SVOX Night/Overcast/Snow）以及多视角匹配（Eynsham）等典型挑战场景。所有对比均基于 DINOv2-small 骨干，以确保公平性；对于未在 DINOv2-S 上报告结果的方法（如 SALAD、BoQ、FoL），作者进行了统一复现。

**精度表现。** 如 Table 1 所示，EfficientVPR 在 DINOv2-S 同尺度模型中建立了新的最优水平。在 Pitts250k-test 上达到 **95.4% R@1**，较 BoQ（约 94.4%）提升 1.0 个百分点；在 MSLS-val 上较两阶段方法 FoL 提升约 2.0%；在极具挑战性的 AmsterTime 和 SVOX Night 数据集上，分别以 **5.0%** 和 **4.5%** 的显著优势超越 BoQ 和 FoL。七个数据集的平均 R@1 达到最高，较次优方法 BoQ 高出约 1.0%（Table 2）。

**效率优势。** EfficientVPR 在精度领先的同时保持了极低的计算开销。其最终特征维度仅 **3456-D**，为 BoQ（约 12352-D）的 28%，为 SALAD（约 8448-D）的 41%（Figure 1）。在 Pitts250k-test 上的总推理延迟仅为 **3.1 ms**（Table 2），与 SALAD（约 2.4 ms）处于同一量级，但特征维度更低、精度更高。内存占用方面，在包含 18871 张数据库图像的 MSLS-val 上，EfficientVPR 仅需约 260 MB，显著低于同精度水平的两阶段方法。

**定性分析。** Figure 5 展示了在极端视角变化、建筑翻新、剧烈光照变化和严重遮挡等挑战场景下的检索结果。EfficientVPR 在这些困难案例中均能正确匹配，而对比方法常因非重叠区域的视觉相似性产生误匹配。Figure 4 进一步揭示了方法有效性的机理：当视角剧变导致查询图像中的树木等元素在正确匹配图像中不可见时，传统单阶段方法易被这些无关特征误导；EfficientVPR 通过增强任务相关的关键局部区域判别表示，有效缓解了此问题。

### 消融研究

#### SceneVPT 消融

**提示微调策略。** Table 3 系统比较了不同微调策略的影响。在移除 SGFS（替换为线性层）的条件下，SceneVPT 在所有测试数据集上均优于无提示（No prompt）、VPT-shallow 和 VPT-deep。VPT-deep 虽引入了可学习提示，但由于缺乏样本自适应能力，性能提升有限；SceneVPT 通过动态筛选机制，在保留预训练知识的同时实现实例级特征引导，带来稳定且一致的增益。

**Token 选择策略。** Table 4 对比了三种提示选择方式：随机选择（Random）、仅保留 Top-k 高注意力提示（k=4，经多轮优化）以及本文的自适应加权方法。结果显示，自适应加权策略在所有数据集上均取得最优性能。随机选择破坏了提示的语义连贯性，Top-k 硬截断则丢失了可能包含互补信息的低注意力提示；而本文方法通过 sigmoid 门控对所有提示进行软加权，既保留了关键提示的主导作用，又维持了信息的完整性。

#### 实例依赖局部增强模块消融

**子模块贡献。** Table 5 通过逐一移除或替换子模块，验证了 MsIA、OLE 和 SGFS 的各自贡献。完整模型在所有数据集上均优于任何消融变体。其中，SGFS 的贡献最为突出——在 AmsterTime 数据集上，移除 SGFS 导致 R@1 下降 **6.8%**（Table 5），凸显了语义引导特征选择在应对极端时间跨度场景时的关键作用。

**SGFS vs. BoQ 块。** Table 6 将 SGFS 模块替换为 BoQ 的特征聚合块进行对比。结果表明，SGFS 在所有数据集上均显著优于 BoQ 块。BoQ 块采用固定的可学习查询进行全局聚合，缺乏对样本特定区域的关注；而 SGFS 以骨干处理后的提示特征作为语义查询，通过交叉注意力机制自适应地增强与当前样本相关的关键局部特征，从而在保持高效的前提下大幅提升判别力。

#### 图像尺寸消融

**推理尺寸。** Table 7 显示，在固定训练尺寸 266×266 的条件下，推理尺寸从 266×266 增大至 322×322 可带来稳定的性能提升；继续增大至 448×448 时，性能趋于饱和甚至略有下降。这表明适度增大推理分辨率有助于捕获更细粒度的空间信息，但过大尺寸可能引入噪声或超出骨干的有效感受野范围。

**训练尺寸。** Table 8 进一步探究了训练尺寸与推理尺寸的匹配关系。在固定推理尺寸 322×322 的条件下，训练尺寸 266×266 取得了最佳综合性能。过小的训练尺寸（224×224）导致信息损失，而过大的训练尺寸（322×322）可能使模型过度适应特定分辨率，泛化能力下降。

### 可视化分析

**注意力动态调整。** Figure 6（原文引用）的可视化结果表明，SceneVPT 能够根据输入图像的内容动态调整注意力区域。与 VPT-deep 和适配器方法固定的提示模式不同，SceneVPT 在不同场景图像上呈现出差异化的注意力分布：对包含显著地标的图像，注意力集中于建筑物等判别性区域；对纹理较弱的自然场景，注意力则分散至更广的上下文区域。这种灵活性是 SceneVPT 性能优势的直观解释。

### 局限性与失败模式

尽管 EfficientVPT 在多个基准上取得了领先性能，但仍存在以下局限：

1. **骨干泛化性未验证。** 所有实验均基于 DINOv2-small 骨干，该方法在更大容量骨干（如 DINOv2-L）或其他预训练模型（如 CLIP、MAE）上的迁移效果尚不明确。若更换骨干，SceneVPT 的提示选择机制可能需要重新调优超参数。

2. **训练数据覆盖不足。** 训练仅使用 GSV-Cities 数据集，该数据集以街景为主，对极端天气（暴风雪、浓雾）、纯夜视、严重遮挡等场景的覆盖有限。在 SVOX Snow 等数据集上，EfficientVPR 虽优于同尺度方法，但与使用更大骨干的两阶段方法仍存在差距，提示训练数据分布可能是瓶颈之一。

3. **超参数人工设定。** 提示数量 $N_p$、可学习阈值 $\gamma$ 的初始值以及 MsIA/OLE 的结构均需人工设定，缺乏自动化搜索机制。在不同应用场景下，这些超参数可能需要重新调整，增加了部署成本。

4. **长期部署中的特征漂移。** 论文未探讨模型在长期部署中面对环境渐变（如季节更替、城市建设）时的特征遗忘问题。SceneVPT 的动态提示机制虽具备一定自适应能力，但若环境分布持续偏移，可能需要在线更新策略以避免性能退化。

> **注意：** 上述部分局限性（如骨干泛化性、训练数据覆盖）在原文中有明确提及；关于特征漂移和自动化搜索的讨论则来自对方法机理的推演，需结合实际部署场景进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l2153_https_openaccess_thecvf_com_content_CVPR2026_html_Tang_EfficientVPR_Towa/figures/001_Figure_1.jpg]]
*Figure 1: Comparison with SOTA methods: average R@1 over 7 datasets and descriptor dimensionality. Our method achieves the best performance with lower feature dimensions compared to approaches with similarly-scale*

![[assets/figures/papers/paper_list_l2153_https_openaccess_thecvf_com_content_CVPR2026_html_Tang_EfficientVPR_Towa/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison on challenging cases. Green boxes: correct matches; red boxes: errors. Drastic viewpoint changes along with domain shift (1th row), renovation-induced visual changes (2nd row), extreme lighting variations (3rd row), and severe occlusion coupled with time shift (4th row)*

![[assets/figures/papers/paper_list_l2153_https_openaccess_thecvf_com_content_CVPR2026_html_Tang_EfficientVPR_Towa/figures/013_Figure_6.jpg]]
*Figure 6: Visualization of fine-tuning methods. The first and third row visualizes features extracted by backbones fine-tuned with different methods. The second and fourth row shows their retrieval results (green boxes: correct matches; red boxes: errors). Frozen backbones attend to excessive task-irrelevant information. VPT-shallow improves but still has this issue. In the first group, street features are non-discriminative, whereas in the second group, they become discriminative features. Our SceneVPT enables dynamic adjustment of attention regions based on input images, while both VPT-deep and adapter-based methods fail to achieve this adaptability effectively*

![[assets/figures/papers/paper_list_l2153_https_openaccess_thecvf_com_content_CVPR2026_html_Tang_EfficientVPR_Towa/figures/006_Table_1.jpg]]
*Table 1: Comparison with SOTA methods on seven benchmarks. The best results are highlighted in bold and the second best are underlined. † Since the paper of SALAD, BoQ and FoL did not report their results on DINOv2-S, we additionally reproduced these results. ‡ CricaVPR utilizes a cross-image encoder architecture that exhibits instability with varying inference batch sizes. Consequently, we additionally provides results under the single query image scenario*

![[assets/figures/papers/paper_list_l2153_https_openaccess_thecvf_com_content_CVPR2026_html_Tang_EfficientVPR_Towa/figures/007_Table_2.jpg]]
*Table 2: Comprehensive comparison with SOTA methods across model scales. † denotes the original version of the method reported by the authors. ”Train Time” denotes train time per epoch. Memory footprint (Memory) is calculated on the MSLS-val dataset, which includes 18871 database images. Latency is measured on Pitts250k-test, using the same CPU and GPU (RTX A800) and is averaged over 5 identical runs. ”Avg. Acc.” denotes the average R@1 across seven datasets*

![[assets/figures/papers/paper_list_l2153_https_openaccess_thecvf_com_content_CVPR2026_html_Tang_EfficientVPR_Towa/figures/009_Table_3.jpg]]
*Table 3: Ablation on SceneVPT. Given that SGFS relies on prompts peocessed by the backbone, it is replaced with a linear layer in all experiments of this set. All test images are resized to 266 × 266*

![[assets/figures/papers/paper_list_l2153_https_openaccess_thecvf_com_content_CVPR2026_html_Tang_EfficientVPR_Towa/figures/011_Table_4.jpg]]
*Table 4: Ablation on token selection strategy. Random: randomly select prompts. Top-k: preserve only the top-k prompts with the highest attention scores (k=4, optimized through multiple trials). In contrast, our approach dynamically weights all tokens based on their attention values, effectively preserving more comprehensive information. Results demonstrate the superiority of our adaptive method across all datasets. All test images are resized to 266 × 266*

![[assets/figures/papers/paper_list_l2153_https_openaccess_thecvf_com_content_CVPR2026_html_Tang_EfficientVPR_Towa/figures/012_Table_5.jpg]]
*Table 5: Ablation on instance-dependent key local feature enhancement module. We analyzed the role of each sub-module in the instance-dependent key local feature enhancement module by removing or replacing key components. All test images are resized to 266 × 266*

![[assets/figures/papers/paper_list_l2153_https_openaccess_thecvf_com_content_CVPR2026_html_Tang_EfficientVPR_Towa/figures/008_Table_6.jpg]]
*Table 6: Ablation on SGFS. ”with BoQ block” refers to the variant where the SGFS module is replaced with a BoQ block, while ”with SGFS” means our full model that retains SGFS. All test images are resized to 266 × 266*



## 定位与知识库关联

### 1. 与单阶段 VPR 方法的关系

EfficientVPR 处于单阶段（one-stage）视觉地点识别（VPR）的研究脉络中，其核心目标是仅通过全局描述子实现高效检索，避免两阶段方法中计算密集型的重排序（re-ranking）步骤。与现有单阶段方法相比，EfficientVPR 在以下几个关键维度上进行了差异化设计：

**特征聚合范式演进。** 早期单阶段方法如 **NetVLAD**（Arandjelovic et al., CVPR 2016）通过可训练的 VLAD 聚合层将 CNN 特征映射为紧凑全局描述子，但其对极端视角和外观变化的鲁棒性有限。**SFRS**（Ge et al., ECCV 2020）引入细粒度区域监督来增强语义判别力，**CosPlace**（Berton et al., CVPR 2022）则从分类引导的角度重新组织特征空间。近年来，基于 ViT 的聚合方法成为主流：**MixVPR**（Ali-bey et al., WACV 2023）通过特征混合聚合多层特征，**EigenPlaces**（Berton et al., ICCV 2023）专注于视角鲁棒训练，**SALAD**（Izquierdo and Civera, CVPR 2024）利用最优传输理论进行特征分配，**BoQ**（Ali-Bey et al., CVPR 2024）则通过可学习的查询袋式聚合实现了当时 DINOv2-S 骨干下的最优性能。EfficientVPR 在 BoQ 的基础上进一步推进：其 SGFS 模块以样本自适应的语义查询替代 BoQ 的静态查询机制，在 AmsterTime 数据集上带来 6.8% 的 R@1 提升（Table 5、Table 6），且特征维度仅为 BoQ 的 28%（Table 2），在效率与精度之间实现了更优的平衡。

**跨图像相关性的替代路径。** **CricaVPR**（Lu et al., CVPR 2024）通过跨图像编码器在推理时利用批次内图像间的相关性来增强描述子，但该设计导致推理结果对批次大小敏感，在单查询图像场景下性能不稳定。EfficientVPR 完全避免了跨图像依赖，所有特征增强均在单图像内完成，保证了推理的一致性和可复现性。

### 2. 与两阶段方法的边界

两阶段 VPR 方法通常先通过全局描述子进行粗检索，再对候选集进行局部特征匹配和几何验证。代表性工作包括 **R2Former**（Zhu et al., CVPR 2023）的统一检索-重排序框架、**SelaVPR**（Lu et al., ICLR 2024）的无缝预训练适配策略，以及 **FoL**（Wang et al., AAAI 2025）的局部判别区域重排序。这些方法在极端场景下通常能取得更高的 R@1，但代价是显著增加的计算开销——重排序步骤需要对候选图像逐一提取和匹配局部特征。EfficientVPR 的设计哲学是在不引入重排序的前提下，通过增强单阶段描述子本身的局部判别力来缩小这一性能差距。其核心机制是 OLE 模块的方向感知局部增强和 SGFS 模块的语义引导特征选择，二者协同弥补了单阶段方法对样本特定关键区域关注不足的固有缺陷（Figure 4 中的失败案例分析证实了这一点）。

需要注意的是，部分两阶段方法（如 FoL 的原始版本）使用 DINOv2-L 等更大容量骨干，其性能优势部分源于模型规模而非方法设计本身。EfficientVPR 在 DINOv2-S 骨干下与这些方法的 DINOv2-S 复现版本进行公平对比（Table 1 中的 † 标注），确保了比较的有效性。

### 3. 与参数高效微调（PEFT）方法的关系

EfficientVPR 的 SceneVPT 模块属于参数高效微调（PEFT）的研究范畴，但其设计理念与现有主流 PEFT 方法存在本质差异：

- **与 VPT 系列的关系。** **VPT**（Jia et al., ECCV 2022）通过在 ViT 各层输入前添加一组可学习的提示 token 来实现微调，其 VPT-deep 变体在所有层插入提示。SceneVPT 直接扩展了 VPT-deep，但引入了基于 CLS token 注意力权重的动态提示筛选机制：每层根据上一层的 CLS-提示注意力值，自适应地保留与当前样本相关的旧提示，并用新提示替换不相关的部分。消融实验（Table 3）表明，SceneVPT 在所有测试数据集上均显著优于 VPT-deep，验证了动态自适应提示的必要性。

- **与 Adapter 方法的关系。** 现有 VPR 方法（如 CricaVPR、SelaVPR）多采用 Adapter 类微调策略，在 Transformer 层中插入额外的可学习模块。SceneVPT 的优势在于：它直接复用 ViT 已有的注意力计算机制来生成提示筛选信号，无需引入额外的网络模块，从而在保持极低参数增量的同时实现了样本自适应的特征引导。Figure 6 的可视化分析证实，SceneVPT 能根据输入图像动态调整注意力区域，而 Adapter 方法无法实现这种灵活性。

- **与其他 PEFT 方法的潜在结合。** 论文未探索 SceneVPT 与 LoRA 等低秩适配方法的结合。这是一个开放问题：LoRA 的低秩分解可能进一步降低可训练参数量，而 SceneVPT 的动态提示机制可以提供任务相关的特征引导，二者在理论上具有互补性。

### 4. 适用边界与局限性

**已验证的适用范围。** 当前实验覆盖了 7 个标准 VPR 基准（Pitts250k-test、MSLS-val、AmsterTime、Eynsham、SVOX Night/Overcast/Snow），涵盖视角变化、季节变化、光照变化、翻修变化和遮挡等典型挑战。EfficientVPR 在这些场景下均展现了 DINOv2-S 同类方法中的最优或次优性能（Table 1、Table 2）。

**已知局限。**
1. **骨干泛化性未验证。** 所有实验均基于 DINOv2-small 骨干。虽然该方法的设计原则（动态提示筛选、语义引导特征增强）不依赖于特定骨干，但其在 DINOv2-L 或其他预训练模型（如 CLIP、MAE 预训练 ViT）上的有效性仍需实验验证。
2. **训练数据覆盖不足。** 训练仅使用 GSV-Cities 数据集，该数据集以街景为主，对极端天气（暴雪、浓雾）、夜间低照度、严重遮挡等场景的覆盖可能不足。在 SVOX Night 上的 +4.5% 提升（vs FoL）表明方法对光照变化有一定鲁棒性，但更极端的域外泛化能力尚未充分评估。
3. **超参数依赖人工设定。** 提示数量 N_p、SceneVPT 的阈值 γ、MsIA 和 OLE 的模块结构等关键超参数均通过人工选择或有限网格搜索确定，缺乏自动化的架构搜索机制。这限制了方法在不同应用场景下的快速适配能力。
4. **长期部署的概念漂移问题未涉及。** 在长期视觉地点识别中，环境外观随季节、天气和人为改造持续变化，可能导致特征空间漂移。论文未探讨模型的持续学习能力或特征遗忘问题。

### 5. 开放问题与未来方向

基于上述分析，以下几个方向值得进一步探索：

1. **跨架构泛化。** SceneVPT 的动态提示选择机制仅依赖 CLS token 的注意力权重，这一设计能否推广到其他视觉 backbone（如 CNN 中的特征图注意力）或 NLP 任务中的提示微调场景？
2. **PEFT 方法融合。** 将 SceneVPT 与 LoRA 或 IA³ 等低秩/轻量适配方法结合，能否在更少可训练参数下维持或提升性能？这需要在多个骨干和数据集上进行系统性的消融实验。
3. **多模态查询扩展。** SGFS 当前以骨干处理后的视觉提示作为语义查询。如果引入文本描述、语义地图等多模态信息作为查询，能否进一步增强跨域地点识别能力？这一方向与当前视觉-语言模型的快速发展高度契合。
4. **自动化架构搜索。** 能否通过神经架构搜索（NAS）或超参数优化（HPO）自动确定 MsIA 的多尺度分支数、OLE 的卷积核配置、N_p 的最优值等，以匹配不同部署场景的精度-效率约束？
5. **持续学习与概念漂移缓解。** 在长期部署中，如何通过回放缓冲区、特征蒸馏或提示库动态更新等机制，缓解环境变化带来的特征遗忘问题？SceneVPT 的可学习提示池为此提供了一种潜在的轻量级解决方案——仅更新提示而非整个模型参数。



## 原文 PDF

![[paperPDFs/CVPR_2026/EfficientVPR_Toward_Efficient_Visual_Place_Recognition_via_Scene_Aware_Prompt_Tuning_and_Adaptive_Feature_Enhancement.pdf]]
