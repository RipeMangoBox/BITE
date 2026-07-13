---
title: "PromptDepth: Efficient and Promptable Geometric 3D Vision Model for Embodied Intelligence"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PromptDepth_Efficient_and_Promptable_Geometric_3D_Vision_Model_for_Embodied_Intelligence.pdf
project_link: "https://promptdepth.github.io"
code_link: null
aliases:
- PromptDepth
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过提示式统一解码器（PromptDPT）将多种密集预测任务（全景深度、实例深度、目标跟踪）统一为可提示的深度估计，配合实例标签分布平滑（ILDS）损失和格拉姆锚定（Gram Anchoring）正则化解锁几何与实例表示的联合训练。
primary_logic: 仅使用合成数据训练的PromptDepth，利用级联双路Transformer解码器根据任务令牌灵活生成不同类型的深度图，通过ILDS损失平衡密集预测中的标签分布，以及Gram Anchoring保持几何纹理并构建实例一致性，实现了在多个基准上的零样本SOTA性能。
claims:
- 在多个单目深度估计基准上零样本性能超越DPT、MiDaS等大模型，例如KITTI上σ_1.25达95.2，rel仅0.075。
- 立体深度估计在KITTI和Sintel上均优于现有在线方法VDA，RMSE降低19%以上。
- 在交互实例分割和视频目标跟踪任务中，以显著更低的延迟（单目39ms）达到优于SAM的组合方案。
- 消融实验证实ILDS损失和Gram Anchoring正则化是解决几何与实例任务冲突的关键，完整模型在深度和分割上均取得最优。
---

# PromptDepth: Efficient and Promptable Geometric 3D Vision Model for Embodied Intelligence

> [!tip] 核心洞察
> 仅使用合成数据训练的PromptDepth，利用级联双路Transformer解码器根据任务令牌灵活生成不同类型的深度图，通过ILDS损失平衡密集预测中的标签分布，以及Gram Anchoring保持几何纹理并构建实例一致性，实现了在多个基准上的零样本SOTA性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | PromptDepth：面向具身智能的高效可提示几何三维视觉模型 |
| 英文题名 | PromptDepth: Efficient and Promptable Geometric 3D Vision Model for Embodied Intelligence |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_PromptDepth_Efficient_and_Promptable_Geometric_3D_Vision_Model_for_Embodied_CVPR_2026_paper.html) · [Project](https://promptdepth.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | PromptDepth |
| Dataset | KITTI, Sintel, NYU, GraspNet |

> [!tip] 效果简介
> - KITTI (单目相对深度) 上，σ_1.25↑ / rel↓ 95.2 / 0.075 vs DPT (ViT-L) 90.1 / 0.100 (+5.1 σ_1.25 / -0.025 rel)。
> - Sintel (单目相对深度) 上，σ_1.25↑ / rel↓ 76.8 / 0.191 vs DA-AC 76.5 / 0.235 (+0.3 σ_1.25 / -0.044 rel)。
> - NYU (单目相对深度) 上，σ_1.25↑ / rel↓ 98.0 / 0.045 vs MiDaS 98.0 / 0.048 (同σ_1.25, rel改进0.003)。

## 概要

**问题瓶颈**：现有三维视觉模型难以在算力有限的具身平台上同时实现实时的场景理解与实例级交互。多任务通常依赖分离模型或高延迟的序列聚合方案，缺乏一个统一的、低延迟的前馈预测框架。

**核心方法**：PromptDepth 提出了一种可提示的密集预测范式。其核心是一个级联双路 Transformer 解码器（PromptDPT），根据任务令牌和视觉提示，将全景深度、实例深度、目标跟踪等任务统一为可提示的深度估计。训练中引入实例标签分布平滑（ILDS）损失和格拉姆锚定（Gram Anchoring）正则化，解决了几何与实例任务在联合训练中的严重冲突。

**关键结论**：
- **零样本深度估计**：仅使用合成数据训练，在 KITTI、Sintel、NYU 等基准上达到或超越 DPT、MiDaS 等大规模模型的零样本性能（KITTI σ₁.₂₅ 达 95.2，rel 仅 0.075）。
- **立体深度估计**：在 KITTI 和 Sintel 上均优于在线方法 VDA，RMSE 降低 19% 以上。
- **交互分割与跟踪**：以显著更低的延迟（单目 39 ms）在 GraspNet 等任务上大幅超越 SAM 的组合方案（mIoU +0.18，F-measure +0.21）。
- **消融验证**：ILDS 损失与 Gram Anchoring 正则化是解锁几何-实例联合训练的关键，单独移除任一组分均导致性能下降或训练崩溃。

**方法定位**：PromptDepth 属于前馈式可提示密集预测模型，介于单任务深度估计器（如 Depth Anything V2）与通用视觉基础模型（如 SAM）之间，以统一架构覆盖多类几何-实例任务，专为具身智能的低延迟需求设计。



三维视觉感知是具身智能系统在复杂环境中执行导航、抓取与交互任务的核心能力。理想的具身视觉模型需要同时回答两个问题：**场景的几何结构是什么**（全景深度），以及**场景中的物体在哪里、彼此如何区分**（实例级深度）。然而，现有方案在这两个需求之间陷入了根本性的权衡。

一方面，以 **MiDaS**（Ranftl et al., TPAMI 2020）、**DPT**（Ranftl et al., ICCV 2021）和 **Depth Anything V2**（Yang et al., NeurIPS 2024）为代表的单目深度估计模型在零样本几何重建上取得了显著进展，但它们输出的全景深度图缺乏实例区分能力，无法直接服务于目标导向的交互任务。另一方面，以 **SAM**（Kirillov et al., 2023）为代表的提示式分割模型擅长实例级掩码生成，却与几何深度估计彼此割裂——将二者简单组合意味着需要串联多个大模型，导致推理延迟急剧上升，难以满足具身平台对实时性的严苛要求。

这种**几何理解与实例感知的分离**构成了当前具身三维视觉的核心瓶颈。更具体地，该瓶颈体现在三个层面：

1. **任务冲突**：全景深度估计要求对场景中所有像素进行连续值回归，而实例深度仅在目标物体区域输出有效深度，背景区域为零。当试图在单一模型中联合训练这两类任务时，标签分布的巨大差异会导致优化冲突，甚至训练崩溃（见 Figure 5 的消融证据）。
2. **架构冗余**：现有方法通常为不同任务设计独立的解码器或完全分离的模型，缺乏一个统一的框架来根据交互意图灵活切换输出类型。
3. **数据稀缺**：真实世界中同时具备高精度几何标注和实例标注的数据极为稀少，而现有合成数据集往往缺少几何与实例的严格对齐，难以支撑联合训练。

**PromptDepth** 的动机正是打破上述僵局。其核心假设是：如果能够设计一个**可提示的统一解码器**，根据任务令牌和用户提示灵活生成不同类型的深度图，并辅以专门设计的损失函数和正则化策略来调和几何与实例任务之间的冲突，那么仅使用大规模合成数据训练的单一模型就有望在多个密集预测任务上同时达到领先水平，且推理延迟远低于多模型组合方案。这一思路将具身三维视觉从“多模型串联”推向“单模型可提示”的新范式。



## 核心方法与创新机理

PromptDepth 的核心创新在于将多种密集预测任务统一为一个**可提示的深度估计框架**，并通过两项关键训练技术解决几何与实例任务的内在冲突，从而在单次前馈推理中同时实现高质量的深度估计与交互式分割/跟踪。

### 1. 统一的可提示密集预测 Transformer（PromptDPT）

传统方法通常为全景深度、实例深度、目标跟踪等任务设计独立的多头解码器或完全分离的模型（如 **DPT** (Ranftl et al., ICCV 2021)、**SAM** (Kirillov et al., 2023) 与深度模型的组合）。PromptDepth 提出 **PromptDPT** 解码器，通过**任务令牌**和**视觉提示**动态调制输出，无需额外计算开销即可在不同任务间切换（Section 3.2）。

具体而言，PromptDPT 采用**级联双路 Transformer** 结构：
- **密集块**：处理视觉特征间的交叉注意力，实现几何对齐与掩码跟踪；
- **稀疏块**：根据任务令牌和提示点进行稀疏交互，调制密集预测。

这种设计使得模型能够根据输入的任务令牌灵活生成全景深度图、实例深度图或目标跟踪深度图，而无需为每个任务设计独立的网络分支。

### 2. 实例标签分布平滑损失（ILDS Loss）

联合训练全景深度与实例深度时，两类深度图的标签分布存在显著差异：全景深度图的值连续分布，而实例深度图中背景区域存在大量零值，导致标准损失函数难以同时优化两种任务。为此，PromptDepth 提出 **ILDS 损失**（Section 3.3）：

1. **分布平滑**：利用对称核函数对深度值的频率分布进行平滑，得到平滑后的密度估计 $\tilde{f}_{D}(d_{g}) = \int_{d_{m}^{*}} k(d_{m}^{*}, d_{g}) p(d_{m}^{*}) d_{m}^{*}$；
2. **自适应权重**：根据平滑密度为每个像素计算平衡权重 $w(d_{m}^{*}) = \frac{1}{\tilde{f}_{norm}(\arg\min_{d_{g}}(|d_{m}^{*} - d_{g}|))}$；
3. **加权损失**：最终损失为 $\mathcal{L}_{ilds} = \frac{1}{h*w} \sum_{i,j} w(d_{m}^{*}) * |d^{*} - \hat{d}^{*}|$。

ILDS 通过自适应地平衡全景深度与实例深度的像素权重，有效缓解了长尾分布带来的优化偏差（Figure 4）。

### 3. 格拉姆锚定正则化（Gram Anchoring）

几何特征与实例特征在联合训练中存在严重冲突——标准联合训练（无额外正则化）会导致训练崩溃（Figure 5）。PromptDepth 提出 **Gram Anchoring** 正则化，约束几何特征 $\mathbf{X}_G$ 与实例特征 $\mathbf{X}_S$ 在 patch 相似性上保持一致：

$$\mathcal{L}_{gram} = |\mathbf{X}_{G}^{T} \cdot \mathbf{X}_{G} - \mathbf{X}_{S}^{T} \cdot \mathbf{X}_{S}|$$

该正则化在保留几何纹理的同时构建实例一致性，是解锁几何与实例表示联合训练的关键（Table 4 消融实验证实）。

### 4. 仅使用合成数据的训练策略

与依赖大规模真实数据预训练的基线（如 **Depth Anything V2** (Yang et al., NeurIPS 2024)）不同，PromptDepth **仅使用自建合成数据引擎**训练，该引擎提供 1000 万对象的高保真、对齐的实例-几何数据对。这一策略使得模型在零样本条件下仍能取得 SOTA 性能，同时避免了真实数据中实例-几何标注难以获取的问题。

### 5. 极低延迟的单次前馈推理

相比基于序列聚合或迭代优化的高延迟方案（如 SAM 与深度模型的组合），PromptDepth 仅需**单次前馈推理**，在单目模式下延迟低至 **39ms**（RTX 4090），同时保持优于 SAM+Depth Anything V2 组合的分割精度（Table 5）。这一效率优势使其特别适用于算力有限的具身智能平台。



PromptDepth 是一个前馈神经网络，最多接收两帧对应的图像作为输入，输出与深度相关的多种密集预测图，包括全景深度、实例深度和视频目标跟踪深度。其核心设计目标是在具身智能平台上实现统一、低延迟的三维场景理解与交互式实例感知。

### 输入输出规范

模型输入为单帧或双帧图像对 $(I_1, I_2 \in \mathbb{R}^{w \times h \times 3})$，以及可选的视觉提示（点坐标 $p$ 和掩码 $m$）。根据任务令牌的不同，模型灵活输出：
- **单目全景深度**：仅使用 $I_1$，输出场景级相对深度图；
- **立体深度**：使用 $I_1$ 和 $I_2$，输出尺度对齐的立体深度图；
- **交互式实例深度**：在点或掩码提示下，输出指定实例的深度图；
- **视频目标跟踪深度**：结合两帧图像和前一帧的实例掩码，输出目标实例在后续帧中的深度图。

### 模块化流水线

PromptDepth 的流水线由四个核心模块串联构成，各模块职责分明且高度解耦：

1. **视觉编码器（Visual Encoder）**  
   采用对称结构、参数完全共享的 DINOv2 作为骨干网络。单帧或双帧图像分别经过编码器，生成视觉特征图 $F_1, F_2 \in \mathbb{R}^{W \times H \times C}$：
   $$F_{1} = \mathrm{VisEncoder}(I_{1}), \quad F_{2} = \mathrm{VisEncoder}(I_{2})$$

2. **提示编码器（Prompt Encoder）**  
   源自 SAM 的设计，将用户提供的点坐标和掩码编码为稀疏特征 $F_p$ 和密集特征 $F_m$：
   $$F_{p}, F_{m} = \mathrm{PromptEncoder}(p, m)$$

3. **可提示密集预测 Transformer（PromptDPT）**  
   这是模型的核心创新模块。一组可学习的任务令牌 $F_t$ 与提示特征 $F_p$ 拼接后，连同视觉特征 $F_1, F_2$ 一起输入级联双路 Transformer。该模块通过稀疏-密集交互机制，根据任务类型自适应调制特征表示：
   $$(F_{t}', F_{p}'), (F_{1}', F_{2}') = \mathrm{PromptDPT}([F_{t}, F_{p}], (F_{1}, F_{2}))$$
   级联双路 Transformer 的具体设计是：先经过一个密集双路块（dense two-way block）处理视觉特征间的交叉注意力，实现几何对齐和掩码跟踪；再经过一个稀疏双路块（sparse two-way block），根据任务令牌和提示点进行稀疏交互，调制最终的密集预测。

4. **输出投影头（Output Projection Head）**  
   将更新后的稀疏任务特征 $F_t'$ 与密集视觉特征 $F_1'$ 进行点积操作，生成最终的深度图 $\hat{d}$。

### 数据流总览

整个流水线的数据流如图 3 所示：视觉编码器并行处理输入图像，提示编码器处理交互信号，二者在 PromptDPT 中汇合。任务令牌作为“开关”，控制解码器输出不同类型的深度图，而无需额外的计算开销或模型分支。这种设计使得 PromptDepth 能够在单次前馈推理中完成从场景级深度到实例级深度的灵活切换，为实时具身应用提供了统一的几何感知基础。

> **注意**：本节描述的模块关系基于论文 Section 3.1-3.2 的公开描述，部分实现细节（如级联块内部的具体注意力配置）需参考原文获取完整信息。

### 补充图表

![[assets/figures/papers/paper_list_l2278_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptDepth_Effic/figures/002_Figure_2.jpg]]
*Figure 2: PromptDepth features a cascaded two-way transformer designed to manage interactions ranging from various purpose, thereby facilitating adaptable and interactive dense prediction tasks*



### 视觉编码器与提示编码器

PromptDepth 的前端由两个对称且共享参数的视觉编码器构成，骨干网络采用 DINOv2。对于单目任务仅输入一帧，立体或跟踪任务则输入两帧，分别得到特征图：

$$F_{1} = \mathrm{VisEncoder}(I_{1}), \quad F_{2} = \mathrm{VisEncoder}(I_{2})$$

其中 $I_{1}, I_{2} \in \mathbb{R}^{w \times h \times 3}$，输出特征 $F_{1}, F_{2} \in \mathbb{R}^{W \times H \times C}$。

当任务涉及实例级交互时，用户提供的点 $p$ 和掩码 $m$ 被送入源自 SAM 的提示编码器，生成稀疏提示特征 $F_{p}$ 和密集提示特征 $F_{m}$：

$$F_{p}, F_{m} = \mathrm{PromptEncoder}(p, m)$$

### PromptDPT：级联双路 Transformer

核心模块 PromptDPT 接收任务令牌 $F_{t}$（一组可学习嵌入，用于指定单目、立体、实例查询或跟踪任务）与提示特征 $F_{p}$，联合图像特征 $F_{1}, F_{2}$ 进行交互：

$$(F_{t}', F_{p}'), (F_{1}', F_{2}') = \mathrm{PromptDPT}([F_{t}, F_{p}], (F_{1}, F_{2}))$$

级联双路 Transformer 由**密集双路块**和**稀疏双路块**级联构成。密集块处理视觉特征间的交叉注意力，实现几何对齐与掩码跟踪；稀疏块则根据任务令牌和提示点进行稀疏交互，调制最终的密集预测。最终，输出投影头将稀疏任务特征与密集视觉特征进行点积，生成目标深度图。

### 尺度偏移不变损失（SSI Loss）

标准深度监督采用尺度偏移不变损失，对预测深度 $d$ 和真值 $\hat{d}$ 分别进行中位数对齐和尺度归一化后计算逐像素绝对误差：

$$\mathcal{L}_{ssi}(d, \hat{d}) = \frac{1}{h \cdot w} \sum_{i,j} |d^{*} - \hat{d}^{*}|$$

其中 $d^{*}$ 和 $\hat{d}^{*}$ 为归一化后的深度值。

### 实例标签分布平滑损失（ILDS Loss）

全景深度与实例深度在标签分布上存在显著差异——实例深度图中背景区域存在大量零值，直接联合训练会导致优化冲突。ILDS 通过自适应权重平衡两类像素的贡献。

首先对深度值的频率分布 $p(d_{m}^{*})$ 进行核平滑，得到平滑密度 $\tilde{f}_{D}$：

$$\tilde{f}_{D}(d_{g}) = \int_{d_{m}^{*}} k(d_{m}^{*}, d_{g}) \, p(d_{m}^{*}) \, d_{m}^{*}$$

其中 $k(\cdot, \cdot)$ 为对称核函数。随后为每个像素计算自适应权重，权重与其所属深度值的平滑密度成反比：

$$w(d_{m}^{*}) = \frac{1}{\tilde{f}_{norm}\big(\arg\min_{d_{g}}(|d_{m}^{*} - d_{g}|)\big)}$$

最终 ILDS 损失为带权重的逐像素绝对误差：

$$\mathcal{L}_{ilds} = \frac{1}{h \cdot w} \sum_{i,j} w(d_{m}^{*}) \cdot |d^{*} - \hat{d}^{*}|$$

### 格拉姆锚定正则化（Gram Anchoring）

几何任务与实例任务在隐空间中可能产生表征冲突。Gram Anchoring 通过约束几何特征 $X_{G}$ 与实例特征 $X_{S}$ 的 patch 相似性矩阵保持一致，维持几何纹理的同时构建实例语义对应：

$$\mathcal{L}_{gram} = \big| X_{G}^{T} \cdot X_{G} - X_{S}^{T} \cdot X_{S} \big|$$

消融实验证实，仅使用标准联合训练（无 $\mathcal{L}_{gram}$）会导致训练崩溃，而同时引入 $\mathcal{L}_{ilds}$ 和 $\mathcal{L}_{gram}$ 可在深度估计和交互分割上均取得最优性能（Table 4, Figure 5）。

### 补充图表

![[assets/figures/papers/paper_list_l2278_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptDepth_Effic/figures/003_Figure_3.jpg]]
*Figure 3: Overview of cascaded two-way transformer data flow*

![[assets/figures/papers/paper_list_l2278_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptDepth_Effic/figures/004_Figure_4.jpg]]
*Figure 4: We study the reacts of proposed ILDS. Dense map levels show significant distribution variability between panoptic depth (middle top) and instanced depth (middle bottom), the latter having substantial zeros for background. ILDS adaptively balances weights based on the smoothed distribution (plot) from the depth frequency (histogram) and generates weights for each map (right). Note that multiple instances are visualized here due to merging batched instances*



## 实验与关键发现

### 单目相对深度估计：零样本性能超越大模型

PromptDepth 在仅使用合成数据训练的条件下，于五个真实世界基准上对单目相对深度估计进行了零样本评估，所有输入均缩放至短边 518 像素。如 Table 1 所示，PromptDepth 以 ViT-B 规模的编码器取得了具有竞争力的结果：在 KITTI 上 $\sigma_{1.25}$ 达 **95.2**，相对误差 rel 仅 **0.075**，显著优于 **DPT** (ViT-L) 的 90.1/0.100；在 Sintel 上 rel 为 **0.191**，较 **DA-AC** 的 0.235 降低了 18.7%。在 NYU、ETH3D 和 Diode 上，PromptDepth 同样达到或超越了以 MiDaS、DPT、Depth Anything V2 等为代表的大规模模型，证明了合成数据驱动的零样本泛化能力。

![[assets/figures/papers/paper_list_l2278_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptDepth_Effic/figures/005_Table_1.jpg]]
*Table 1: Zero-shot performance on monocular relative depth estimation. Bold indicate the best results, while underlined represent the second-best. We compare the base version of ViT with many large and giant models, resizing input images to a short edge of 518*

### 立体深度估计：在线推理精度与效率双重领先

在立体深度估计任务中，PromptDepth 利用连续两帧进行在线推理，无需离线优化或全局对齐。Table 2 显示，在 KITTI 上 PromptDepth 取得 $\delta_1$ **0.950**、AbsRel **0.076**、RMSE **3.338**，全面优于在线方法 **VDA**（$\delta_1$ 0.942、RMSE 3.710），RMSE 降低约 10%。在 Sintel 上优势更为明显，RMSE 从 VDA 的 4.657 降至 **2.668**，降幅达 42.7%。这表明级联双路 Transformer 有效利用了帧间几何约束，在保持实时性的同时显著提升了深度精度。

![[assets/figures/papers/paper_list_l2278_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptDepth_Effic/figures/006_Table_2.jpg]]
*Table 2: online performance of Stereo Depth Estimation performance. We test on subsquent frame pairs for real-time purpose, that force predicted depth to be inherently aligned. Most of previous state-of-art works fall into sub-optimal with limited corresponding views*

### 交互实例分割与视频目标跟踪：低延迟下的高效感知

在具身智能的核心场景——交互式分割与目标跟踪中，PromptDepth 展现出显著的效率优势。Table 5 上半部分对比了单目模式下的 3D 实例感知几何任务：PromptDepth 以 **39.09 ms** 的总延迟完成深度估计与交互分割，而 **SAM + Depth Anything V2** 组合方案需 95.53 ms，延迟降低超过 59%。在 GraspNet 交互分割基准上，PromptDepth 的 mIoU 达 **0.7863**，F-measure 达 **0.8985**，J&F 达 **0.8424**，分别较 SAM 提升 0.1827、0.2056 和 0.1941。

![[assets/figures/papers/paper_list_l2278_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptDepth_Effic/figures/010_Table_5.jpg]]
*Table 5: Latency (ms) and Metrics comparison. All latency tests on RTX 4090 GPU with data type of float32*

Table 3 展示了零样本视频目标跟踪的半监督评估结果，PromptDepth 通过将深度有效区域（$d > 0$）的预测掩码作为前景，在多个序列上取得了可观的 J&F-Mean 指标，验证了统一框架在跟踪任务中的迁移能力。

![[assets/figures/papers/paper_list_l2278_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptDepth_Effic/figures/007_Table_3.jpg]]
*Table 3: Semi-supervised Evaluation of zero-shot video object tracking using J&F-Mean metrics. We sample the predicted mask from the valid depth region where d >ˆ 0 as the foreground*

### 消融实验：ILDS 损失与 Gram Anchoring 是联合训练的关键

几何深度估计与实例级分割任务的联合训练存在严重冲突。Table 4 的消融实验系统验证了所提组件的贡献：

![[assets/figures/papers/paper_list_l2278_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptDepth_Effic/figures/008_Table_4.jpg]]
*Table 4: Ablation study on the impact of proposed approach. We individually train depth estimation and interactive/tracking segmentation as singular tasks, compared by a joint training of both*

- **单独训练**：深度估计（KITTI Abs.rel 0.075）和交互分割（mIoU 67.1）分别达到最优，但无法统一。
- **标准联合训练（无 $L_{gram}$）**：训练崩溃，证实几何与实例任务在隐空间中相互干扰。
- **仅加入 Gram Anchoring（无 $L_{ilds}$）**：部分缓解冲突，但性能仍不及完整模型。
- **完整模型（$L_{ilds} + L_{gram}$）**：在深度估计（Abs.rel 0.075, $\delta_1$ 0.945）和交互分割（mIoU 67.1）上同时取得最优，证明 ILDS 损失通过自适应权重平衡了全景深度与实例深度的标签分布差异，而 Gram Anchoring 正则化约束了几何特征与实例特征在 patch 相似性上的一致性。

Figure 5 通过 PCA 可视化进一步揭示了不同训练策略下隐空间中 patch 相似性的变化：标准联合训练导致特征空间崩溃，Gram Anchoring 有效维持了几何纹理与实例一致性的结构。

![[assets/figures/papers/paper_list_l2278_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptDepth_Effic/figures/009_Figure_5.jpg]]
*Figure 5: PCA visualization on the similarity of patches in latent space guided by various training strategy*

### 推理延迟分析

Table 5 下半部分详细列出了各模块的延迟分解。在单目模式下，视觉编码器耗时 16.10 ms，PromptDPT 解码器耗时 18.27 ms，总延迟 39.09 ms；立体模式下总延迟 63.05 ms。所有测试均在 RTX 4090 GPU 上以 float32 精度进行，验证了 PromptDepth 作为前馈网络在具身平台上的实时推理能力。

### 失败模式与局限性

尽管 PromptDepth 在多个基准上取得了领先的零样本性能，其局限性仍需关注：

1. **域差异**：模型仅使用合成数据训练，在部分未见真实场景中可能出现深度边界模糊或实例分割不完整的情况，需要在实际部署中结合少量真实数据微调。
2. **长期跟踪能力缺失**：当前模型输入限于两帧，对于遮挡后重识别等需要长期记忆的跟踪任务尚未探索，限制了其在复杂长时间操作中的应用。
3. **细粒度 3D 重建任务未覆盖**：尚未验证在关键点跟踪和密集特征匹配等更细粒度 3D 重建任务中的性能，这些任务对特征分辨率和时序一致性提出了更高要求。

### 补充图表

![[assets/figures/papers/paper_list_l2278_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptDepth_Effic/figures/011_Figure_6.jpg]]
*Figure 6: Visualized comparison on real-time embodies manipulation scenario*



## 定位与知识库关联

### 1. 技术脉络与基线关系

PromptDepth 处于**单目/立体深度估计**、**交互式分割**与**视频目标跟踪**三个领域的交叉点。其核心创新并非提出全新的骨干网络，而是通过**提示式统一解码器（PromptDPT）** 将多种密集预测任务统一为可提示的深度估计，从而在单一前馈网络中实现多任务切换。

#### 1.1 深度估计基线

在单目相对深度估计任务上，PromptDepth 直接对标以下代表性工作：

- **MiDaS** (Ranftl et al., TPAMI 2020)：早期混合数据集训练的鲁棒单目深度估计模型，采用尺度不变损失。
- **DPT** (Ranftl et al., ICCV 2021)：基于 Vision Transformer 的密集预测架构，是 PromptDepth 视觉编码器（DINOv2）的架构前身。
- **Depth Anything V2** (Yang et al., NeurIPS 2024)：当前单目深度估计的强基线，利用大规模无标签数据。
- **DA-AC** (Depth Anything at Any Condition)：支持任意条件的深度估计变体。

从 Table 1 的零样本对比来看，PromptDepth 仅使用合成数据训练，在 KITTI 上 σ₁.₂₅ 达到 95.2（DPT ViT-L 为 90.1），rel 降至 0.075（DPT 为 0.100）；在 Sintel 上 rel 为 0.191（DA-AC 为 0.235）。值得注意的是，PromptDepth 使用的是 ViT-Base 规模的编码器，而多数基线使用 Large 甚至 Giant 模型，这突显了其**参数效率优势**。

在立体深度估计任务上，基线包括：

- **VDA (Visual Depth Anything)**：在线立体深度估计方法，在 KITTI 上 δ₁ 为 0.942，RMSE 为 3.710。PromptDepth 达到 δ₁ 0.950，RMSE 3.338，尤其在 Sintel 上 RMSE 从 4.657 降至 2.668（降幅约 43%）。
- **DUSt3R** (Wang et al., CVPR 2024) 和 **VGGT** (Wang et al., CVPR 2025)：侧重立体重建与视觉几何，但在有限视角的在线设置下表现次优。

#### 1.2 交互式分割与跟踪基线

在具身场景的交互式实例分割和视频目标跟踪任务上，PromptDepth 主要对比：

- **SAM** (Kirillov et al., 2023)：当前交互式分割的通用基础模型。Table 5 显示，在 GraspNet 上 PromptDepth 的 mIoU 达到 0.7863，F-measure 0.8985，J&F 0.8424，分别比 SAM 高出 0.1827、0.2056 和 0.1941。更重要的是，PromptDepth 单目推理仅需 **39.09 ms**，而 SAM + Depth Anything V2 组合方案需要 **95.53 ms**，效率提升超过 2 倍。

#### 1.3 关键区分点

与上述基线相比，PromptDepth 的根本差异在于：

| 维度 | 基线方案 | PromptDepth |
|------|----------|-------------|
| 任务架构 | 多模型组合或分离头 | 统一 PromptDPT 解码器 |
| 任务切换 | 需重新加载模型或推理 | 任务令牌动态调制 |
| 几何-实例联合 | 独立训练或后融合 | ILDS 损失 + Gram Anchoring 联合训练 |
| 数据依赖 | 大规模真实数据预训练 | 仅合成数据训练 |
| 推理延迟 | >100ms（组合方案） | 39ms（单目） |

### 2. 适用边界与局限

尽管 PromptDepth 在多个基准上展现了优异的零样本性能，但其适用边界受以下因素制约：

1. **合成数据的域差异**：模型仅使用自建合成数据引擎（约 1000 万对象）训练，虽具备强零样本泛化能力，但在极端光照、复杂天气等未见真实场景中可能存在域偏移。论文未提供在真实数据上微调后的性能对比，该点需进一步验证。

2. **两帧输入限制**：当前模型输入上限为两帧图像，对于需要长期时序记忆的跟踪任务（如目标被遮挡后的重识别）尚未探索。论文在开放问题中明确指出这一点。

3. **细粒度 3D 重建任务未覆盖**：尚未验证在关键点跟踪和密集特征匹配等更细粒度 3D 重建任务中的性能。这些任务对特征粒度和时序一致性的要求更高。

4. **实例深度与全景深度的语义边界**：ILDS 损失通过标签分布平滑平衡了两类深度图的训练，但在实例边界模糊或严重遮挡的情况下，自适应权重的鲁棒性缺乏定量消融。

### 3. 开放问题

基于论文的局限性和当前技术趋势，以下问题值得后续研究关注：

1. **长期记忆机制**：如何扩展 PromptDepth 以支持超过两帧的时序上下文？可能的路径包括引入可学习的记忆令牌或轻量级时序聚合模块。

2. **关键点跟踪与密集匹配**：在 3D 重建管线中，关键点跟踪和密集特征匹配是核心组件。PromptDepth 的 Gram Anchoring 已证明可以约束几何与实例特征的一致性，这一机制能否直接迁移到特征匹配任务？

3. **真实数据微调策略**：合成数据预训练 + 少量真实数据微调的半监督范式能否进一步提升域泛化能力？ILDS 损失在真实数据上的分布平滑效果是否依然有效？

4. **多模态提示扩展**：当前提示编码器源自 SAM，支持点和掩码提示。能否扩展至语言提示（如“抓取红色杯子”），使模型更自然地融入具身语言指令管线？

5. **Gram Anchoring 的理论解释**：论文通过 PCA 可视化（Figure 5）展示了 Gram Anchoring 对隐空间 patch 相似性的约束效果，但缺乏对该正则化项的理论分析（如收敛性质、与对比学习的联系）。

### 4. 知识库定位

在现有知识体系中，PromptDepth 可被定位为：

- **上游依赖**：视觉编码器（DINOv2）、提示编码器（SAM 架构）、尺度偏移不变损失（MiDaS/DPT 传统）。
- **同级竞争者**：Depth Anything V2（单目深度）、VDA（立体深度）、SAM（交互分割）。
- **潜在下游**：具身操作（抓取、导航）、实时 3D 场景理解、视频目标跟踪系统。
- **核心贡献**：首次证明通过**提示式统一解码器 + 实例几何联合训练**，可以在单一前馈网络中实现多任务密集预测，且仅需合成数据即可达到零样本 SOTA。



## 原文 PDF

![[paperPDFs/CVPR_2026/PromptDepth_Efficient_and_Promptable_Geometric_3D_Vision_Model_for_Embodied_Intelligence.pdf]]
