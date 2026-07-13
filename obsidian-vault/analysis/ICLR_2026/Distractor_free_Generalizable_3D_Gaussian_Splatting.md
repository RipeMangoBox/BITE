---
title: Distractor-free Generalizable 3D Gaussian Splatting
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Distractor_free_Generalizable_3D_Gaussian_Splatting_d5b1fa086266.pdf
project_link: null
code_link: null
aliases:
- DDFG3GS
- DFG3GS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用参考视图重渲染的非干扰区域作为可靠指引，过滤查询视图中的假阳性干扰物掩码，并通过掩码损失排除干扰区域，稳定训练。
primary_logic: 由参考视图推理出的3DGS在非干扰区域的重渲染结果高度准确，该性质可用于指导查询视图中的干扰物掩码过滤，实现前馈式干扰物掩码预测，无需额外监督。
claims:
- 重新渲染的参考非干扰区域从3DGS（由参考推理）通常准确且鲁棒，因此可用作指导，过滤查询视图中误分类的干扰物区域。
- DGGS利用基于参考的掩码预测和细化模块，结合3D一致性和语义先验，有效消除干扰物对训练损失的影响。
- 消融实验显示，添加基于参考的掩码预测后PSNR从17.11提升至20.35，验证了参考过滤的关键作用。
- RobustNeRF (平均五个场景) 上 PSNR ↑ = 21.74
---

# Distractor-free Generalizable 3D Gaussian Splatting

> [!tip] 核心洞察
> 由参考视图推理出的3DGS在非干扰区域的重渲染结果高度准确，该性质可用于指导查询视图中的干扰物掩码过滤，实现前馈式干扰物掩码预测，无需额外监督。

| 字段 | 内容 |
|------|------|
| 中文题名 | 无干扰物的泛化三维高斯泼溅 |
| 英文题名 | Distractor-free Generalizable 3D Gaussian Splatting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=G33Iemmj3Z) · [paper](https://arxiv.org/abs/2408.00714) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DGGS (Distractor-free Generalizable 3D Gaussian Splatting) |
| Dataset | RobustNeRF, Arcdetriomphe, Mountain |

> [!tip] 效果简介
> - RobustNeRF (平均五个场景) 上，PSNR ↑ 21.74 vs 15.45 (Mvsplat) (+6.29)；SSIM ↑ 0.758 vs 0.515 (Mvsplat) (+0.243)；LPIPS ↓ 0.237 vs 0.426 (Mvsplat) (-0.189)。
> - Arcdetriomphe 上，PSNR ↑ 20.32 (DGGS-TR) vs 14.96 (Mvsplat) (+5.36)。
> - Mountain 上，PSNR ↑ 16.37 (DGGS-TR) vs 13.73 (Mvsplat) (+2.64)。

## 概要

真实场景中广泛存在的干扰物（如行人、车辆等瞬态物体）破坏了泛化三维高斯泼溅（3D Gaussian Splatting, 3DGS）中参考视图与查询视图之间的三维一致性，导致训练不稳定，并在新视角合成时产生伪影和空洞。本文提出 **DGGS（Distractor-free Generalizable 3D Gaussian Splatting）**，一种无需场景特定优化、前馈式地预测干扰物掩码并实现无干扰物重建的泛化3DGS框架。

核心思路源于一个关键观察：由参考视图推理出的3DGS在非干扰区域的重渲染结果通常高度准确且鲁棒。基于这一性质，DGGS 利用参考视图的非干扰区域作为可靠指引，过滤查询视图中被误分类为干扰物的区域，从而在无需额外监督的条件下实现前馈式掩码预测。方法上，DGGS 将基于参考的掩码预测与细化模块嵌入泛化3DGS训练流程，通过掩码损失排除干扰区域对训练目标的污染；推理阶段则引入参考评分与干扰物剪枝机制，进一步抑制残余伪影。

在 RobustNeRF 基准的五个场景上，DGGS 相较通用泛化3DGS基线 **Mvsplat**（Chen et al., ECCV 2024）平均 PSNR 提升 6.29 dB（21.74 vs. 15.45），SSIM 提升 0.243，LPIPS 降低 0.189。消融实验证实，基于参考的掩码预测是性能跃升的关键驱动因素——引入该模块后 PSNR 从 17.11 跃升至 20.35，叠加掩码细化与推理策略后最终达到 21.74。方法的主要局限在于多参考视图间存在大面积共同遮挡时无法推理正确几何，且不具备生成式补全能力，共同遮挡区域可能产生散斑伪影。

### 泛化三维高斯泼溅与干扰物挑战

新视角合成（Novel View Synthesis, NVS）旨在从一组稀疏的输入图像重建三维场景并渲染任意视角。三维高斯泼溅（3D Gaussian Splatting, 3DGS）以其显式表征和实时渲染能力成为该领域的主流方法。然而，传统3DGS需要针对每个场景进行逐场景优化（per-scene optimization），耗时且无法泛化。以**Mvsplat**（Chen et al., ECCV 2024）和**Pixelsplat**（Charatan et al., CVPR 2024）为代表的泛化3DGS方法，通过前馈网络直接从多视图图像预测高斯原语属性，实现了跨场景的快速重建，无需场景特定的迭代优化。

然而，泛化3DGS的训练和推理面临一个关键瓶颈：**真实世界数据中普遍存在的干扰物（distractors）**——行人、车辆、气球等非静态物体。这些干扰物破坏了参考视图与查询视图之间的三维一致性假设：模型在训练时被迫拟合在不同视图中位置不一致的瞬态物体，导致训练不稳定；在推理时，干扰物被错误地编码为场景几何的一部分，产生伪影和空洞（holes），严重降低渲染质量。

### 现有方法的局限

针对干扰物问题，已有方法主要分为两类：

**场景特定方法**通过逐场景优化来识别和排除干扰物。例如，**RobustNeRF**（Sabour et al., CVPR 2023）利用渲染残差阈值生成鲁棒掩码；**NeRF-HuGS**（Chen et al., CVPR 2024）结合启发式规则与语义分割；**On-the-go**（Ren et al., CVPR 2024）引入DINO特征的不确定性估计；**SLS**（Sabour et al., arXiv 2024）使用扩散先验生成掩码。这些方法虽然有效，但需要针对每个场景进行耗时优化，无法直接应用于泛化3DGS的前馈推理范式。

**泛化方法**则面临更严峻的挑战：由于缺乏场景特定的优化过程，模型必须在训练阶段学会区分干扰物与静态场景。直接集成场景特定掩码方法到泛化框架中，往往因缺乏针对性的训练信号而效果有限。核心困难在于，泛化模型需要在没有任何场景特定监督的情况下，仅依赖参考-查询视图间的几何一致性来推断干扰物掩码。

### 本文动机与核心思路

DGGS的出发点是利用泛化3DGS的一个关键性质：**由参考视图推理出的3DGS，在非干扰区域的重渲染结果通常是准确且鲁棒的**。这一性质意味着，参考视图的非干扰区域可以作为可靠指引，用于过滤查询视图中被误分类为干扰物的目标区域。

基于此，DGGS设计了一个前馈式干扰物掩码预测与细化模块，利用参考视图的三维一致性和语义先验，在训练阶段自动生成高质量的干扰物掩码，并通过掩码损失排除干扰区域对训练的负面影响。在推理阶段，DGGS进一步引入两阶段框架：先粗重建并评分候选参考视图，再基于评分选择最优视图并执行干扰物剪枝，从而系统性地抑制干扰物引起的伪影。整个流程无需额外的干扰物标注或场景特定优化，实现了端到端的无干扰物泛化三维重建。

## 核心方法与创新机理

DGGS 的核心创新在于将“干扰物掩码预测”从启发式阈值或外部模型依赖，转变为**由参考视图重渲染一致性驱动的自监督过程**。其关键洞察是：从参考视图推理出的 3DGS 在非干扰区域的重渲染结果高度准确且鲁棒，这一性质可反过来指导查询视图中干扰物掩码的过滤与细化，无需任何额外监督信号。

### 创新点一：基于参考重渲染的掩码预测与细化（Changed Slot: 干扰物掩码预测）

传统泛化 3DGS 方法（如 **Mvsplat**，Chen et al., ECCV 2024）仅依赖查询视图的 MSE 损失进行训练，对干扰物毫无抵抗力。一个直观的改进是引入启发式鲁棒掩码 $\mathcal{M}_{Rob}$，通过渲染残差阈值过滤干扰区域（式 4），但该方法存在严重缺陷：**目标区域常被误分类为干扰物**（Fig. 3 中无参考过滤的掩码演化清晰展示了这一问题）。

DGGS 的突破在于引入 **Reference-based Mask Prediction** 模块（Sec. 4.1.1），其运作机制如下：

1. **参考非干扰掩码生成**：对每个参考视图 $\mathbf{I}_i$，计算其重渲染残差，低于阈值 $\rho_{Ref}$ 的像素构成非干扰掩码 $\mathcal{M}_{Ref_i}$（式 5）。由于参考视图的 3DGS 推理不涉及查询视图中的干扰物，该掩码在非干扰区域高度可靠。

2. **多视图一致性过滤**：将各参考非干扰掩码通过深度 $\mathbf{D}_i$ 和相机参数 $\mathbf{P}_i, \mathbf{P}_T$ 扭曲到查询视角，得到投影查询掩码 $\mathcal{M}_{Qry_i}$（式 5）。对所有投影掩码取交集并与原始鲁棒掩码合并，得到 $\mathcal{M}_Q$，从而有效过滤 $\mathcal{M}_{Rob}$ 中的假阳性干扰物标记。

3. **视差解耦与实体填充**：$\mathcal{M}_Q$ 中仍可能包含因视差导致的不可见区域。DGGS 通过扭曲全 1 掩码并取并集来显式标识这些区域 $\mathcal{M}_D$（式 6），将其从干扰物掩码中解耦。随后，利用预训练实体分割模型对参考掩码进行细化 $\mathcal{M}_{Ref_i}^{En}$，填充被误判为干扰物的完整实体，得到最终掩码 $\mathcal{M}$。

**因果机制**：该创新的因果链条为“参考重渲染可靠性 → 参考非干扰掩码 → 多视图投影一致性过滤 → 查询掩码提纯”。消融实验（Table 2）提供了强因果证据：在基础模型（PSNR 15.45）上添加鲁棒掩码后 PSNR 仅提升至 17.11，而加入基于参考的掩码预测后跃升至 20.35，验证了参考过滤的核心作用。

### 创新点二：掩码引导的损失函数重构（Changed Slot: 损失函数）

基线方法仅使用查询视图的无掩码 MSE 损失（式 2），干扰物区域的梯度会破坏训练稳定性。DGGS 将损失函数重构为：

$$\arg \min_{\boldsymbol{\theta}} \mathcal{M} \odot \|\mathbf{I}_T - \mathcal{G}(\mathbf{P}_T)\|_2^2 + \mathcal{L}_A$$

其中 $\mathcal{M}$ 为最终干扰物掩码，对查询损失进行像素级加权，排除干扰区域。$\mathcal{L}_A$ 为辅助损失（式 7），针对查询视图中被遮挡但参考视图中可见的区域，通过反向扭曲 $(1-\mathcal{M})$ 与参考实体掩码 $\mathcal{M}_{Ref_i}^{En}$ 的交集提供额外监督。这一设计解决了纯掩码损失在遮挡区域缺乏监督信号的问题，消融中移除辅助损失导致 PSNR 从 21.02 降至 20.64。

### 创新点三：两阶段推理与干扰物剪枝（Changed Slot: 推理策略）

传统泛化 3DGS 一次性使用固定数量的相邻视图进行推理，当参考视图中存在大量干扰物时，重建质量急剧下降。DGGS 提出**两阶段 Distractor-free Generalizable Inference** 框架（Fig. 4, Sec. 4.2）：

1. **第一阶段（粗重建 + 参考评分）**：从场景图像池中采样相邻参考视图进行粗重建，基于预测的干扰物掩码为池中所有图像计算质量评分，筛选出干扰物最少、视差最小的候选视图。

2. **第二阶段（精细重建 + 干扰物剪枝）**：基于评分选择最优 $N$ 个视图进行精细重建，并根据参考掩码从 3D 高斯原语中移除干扰物区域对应的属性，抑制残余伪影。

消融显示（Table 2），参考评分机制将 PSNR 从 21.02 提升至 21.47，干扰物剪枝进一步推至 21.74。这一策略的瓶颈在于：当多个参考视图间存在大范围共同遮挡时，评分机制无法找到干净的参考，性能会退化（见 Fig. 16 失败案例）。

DGGS 的整体设计围绕一个核心观察展开：由参考视图推理出的 3DGS 在非干扰区域的重渲染结果通常准确且鲁棒。这一性质被系统性地利用，构建了一个无需额外监督的前馈式干扰物掩码预测与训练框架，同时辅以两阶段推理策略来抑制残余伪影。

### 训练流水线

训练阶段以随机采样的参考-查询视图对为输入，图 2 展示了完整的数据流：

1. **基础属性预测与鲁棒掩码生成**：给定 $N$ 张参考视图 $\{\mathbf{I}_i\}_{i=1}^N$ 及其相机参数，DGGS 首先通过泛化 3DGS 的编码器-解码器结构预测 3D 高斯原语的属性 $\mathcal{G}$，并同步生成启发式鲁棒掩码 $\mathcal{M}_{Rob}$。该掩码基于渲染残差阈值和核运算，提供对干扰物区域的初步估计。

2. **基于参考的掩码预测**（Reference-based Mask Prediction）：将参考视图重渲染的非干扰区域作为可靠指引，过滤 $\mathcal{M}_{Rob}$ 中的假阳性。具体而言，对每张参考视图 $\mathbf{I}_i$，计算其重渲染残差并二值化得到参考非干扰掩码 $\mathcal{M}_{Ref_i}$，随后通过深度和相机参数将其扭曲到查询视角，形成投影查询掩码 $\mathcal{M}_{Qry_i}$。对所有投影掩码取交集后与原始 $\mathcal{M}_{Rob}$ 合并，得到初步过滤的查询掩码 $\mathcal{M}_Q$。

3. **掩码细化**（Mask Refinement）：$\mathcal{M}_Q$ 中仍可能包含因视差导致的误差区域（即参考视图中不可见的部分）。DGGS 通过扭曲全 1 掩码并取并集来显式解耦视差误差掩码 $\mathcal{M}_D$，将其从 $\mathcal{M}_Q$ 中移除。随后，利用预训练的实体分割模型对参考掩码进行实体级填充，填补因干扰物遮挡而被误判的非干扰区域，得到最终掩码 $\mathcal{M}$。

4. **联合损失监督**：训练目标为掩码加权的查询视图重建损失与辅助损失之和。掩码 $\mathcal{M}$ 对查询视图的 MSE 损失进行像素级加权，使干扰物区域不参与梯度回传；辅助损失 $\mathcal{L}_A$ 则针对查询视图中被遮挡但在参考中可见的区域，提供额外的监督信号，防止模型在不可见区域产生退化。

### 推理流水线

推理阶段采用两阶段策略，如图 4 所示：

- **第一阶段（粗重建与参考评分）**：从场景图像池中采样相邻参考视图，利用训练好的 DGGS 进行粗粒度 3DGS 重建，同时为池中所有图像计算干扰物掩码和质量评分。评分机制基于预测掩码中非干扰区域的比例和视差范围，筛选出干扰物最少、视差最小的候选参考视图。

- **第二阶段（精细重建与干扰物剪枝）**：根据评分结果重新选择最优的 $N$ 张参考视图，执行精细的 3DGS 重建。在此基础上，干扰物剪枝模块利用参考掩码，从 3D 高斯原语中移除对应干扰物区域的属性，进一步抑制残余伪影和空洞。

### 关键设计决策

- **无额外监督**：整个掩码预测流程完全依赖参考视图自身的 3D 一致性，无需人工标注或场景特定优化。
- **模块化解耦**：掩码预测、细化、参考评分和干扰物剪枝各自承担独立功能，消融实验（Table 2）验证了每个模块的独立贡献——从基础鲁棒掩码的 PSNR 17.11 逐步提升至完整 DGGS 的 21.74。
- **失效边界**：当多个参考视图之间存在大范围共同遮挡时，DGGS 无法推理被遮挡区域的正确几何，可能产生散斑伪影；该场景下需要手动验证重建质量。

DGGS 的核心由四个关键模块构成：**基于参考的掩码预测**、**掩码细化**、**参考评分机制** 和 **干扰物剪枝**。这些模块协同工作，在不依赖场景特定优化或额外监督的前提下，实现了前馈式的干扰物掩码预测与鲁棒的三维重建。

### 基础泛化3DGS公式

给定 $N$ 个参考视图 $\{ \mathbf{I}_i \}_{i=1}^N$ 及其相机参数 $\{ \mathbf{P}_i \}_{i=1}^N$，泛化3DGS模型 $\theta$ 直接推理出三维高斯原语属性 $\mathcal{G}$，并在查询视图 $\mathbf{P}_T$ 上通过 alpha 混合生成渲染图像：

$$\hat { C } = \mathcal { G } \left( \mathbf { P } \right) = \sum _ { m \in M } \hat { c } _ { m } \alpha _ { m } \prod _ { j = 1 } ^ { m - 1 } ( 1 - \alpha _ { j } )$$

其中 $\hat{c}_m$ 和 $\alpha_m$ 分别表示第 $m$ 个高斯原语的颜色与不透明度。标准训练目标是最小化查询图像 $\mathbf{I}_T$ 与渲染结果之间的 L2 损失：

$$\arg \operatorname* { m i n } _ { \theta } \left\| \mathbf { I } _ { T } - \mathcal { G } \left( \mathbf { P } _ { T } \right) \right\| _ { 2 } ^ { 2 }$$

然而，当场景中存在干扰物时，上述损失会迫使模型拟合瞬态物体，破坏参考-查询视图间的三维一致性。

### 启发式鲁棒掩码

为解决干扰物问题，DGGS 首先引入一个启发式鲁棒掩码 $\mathcal{M}_{Rob}$，通过渲染误差阈值和形态学核运算生成初始干扰物区域标识：

$$\mathcal { M } _ { R o b } = \mathbb { 1 } \left\{ \mathcal { C } \left( \mathbb { 1 } \left\{ \left. \mathbf { I } _ { T } - \mathcal { G } \left( \mathbf { P } _ { T } \right) \right. _ { 2 } < \rho _ { 1 } \right\} \right) > \rho _ { 2 } \right\}$$

该掩码对查询损失进行像素级加权，排除干扰物区域对训练的负面影响：

$$\arg \operatorname* { m i n } _ { \pmb { \theta } } \mathcal { M } _ { R o b } \odot \left\| \mathbf { I } _ { T } - \mathcal { G } \left( \mathbf { P } _ { T } \right) \right\| _ { 2 } ^ { 2 }$$

但 $\mathcal{M}_{Rob}$ 存在严重缺陷：它倾向于将目标区域误分类为干扰物（假阳性），因为渲染误差不仅来自干扰物，还可能源于几何重建不准确。

### 基于参考的掩码预测

DGGS 的核心洞察是：由参考视图推理出的 3DGS 在**非干扰区域**的重渲染结果通常准确且鲁棒。因此，可以利用参考视图的非干扰区域作为可靠指引，过滤查询视图中误分类的假阳性干扰物区域。

首先，对每个参考视图 $i$，计算其重渲染非干扰掩码 $\mathcal{M}_{Ref_i}$：

$$\mathcal { M } _ { R e f _ { i } } = \mathbb { 1 } \left\{ \left. \mathbf { I } _ { i } - \mathcal { G } \left( \mathbf { P } _ { i } \right) \right. _ { 2 } ^ { 2 } < \rho _ { R e f } \right\}$$

其中 $\rho_{Ref}$ 为参考渲染误差阈值。该掩码标识了参考视图中渲染误差低于阈值的像素，即非干扰区域。

随后，通过深度 $\mathbf{D}_i$ 和相机参数将 $\mathcal{M}_{Ref_i}$ 扭曲投影到查询视角，得到投影查询掩码 $\mathcal{M}_{Qry_i}$：

$$\mathcal { M } _ { Q r y _ { i } } = \mathcal { W } _ { i \to T } \left( \mathcal { M } _ { R e f _ { i } } , \mathbf { D } _ { i } , \mathbf { P } _ { i } , \mathbf { P } _ { T } , \mathbf { U } \right)$$

其中 $\mathcal{W}_{i \to T}$ 表示从参考视角 $i$ 到查询视角 $T$ 的扭曲函数，$\mathbf{U}$ 为相机内参。

最后，对所有投影查询掩码取交集，并与原始鲁棒掩码合并，得到参考过滤后的掩码 $\mathcal{M}_Q$：

$$\mathcal { M } _ { Q } = \left\{ \bigcap _ { i = 1 } ^ { N } \mathcal { M } _ { Q r y _ { i } } \right\} \bigcup \mathcal { M } _ { R o b }$$

这一过滤机制有效移除了 $\mathcal{M}_{Rob}$ 中的假阳性区域，因为若某像素在多个参考视图中均被确认为非干扰区域，则其在查询视图中被误判为干扰物的可能性极低。

### 掩码细化

掩码细化模块解决两个遗留问题：**视差引起的误差区域**和**实体不完整**。

**视差误差掩码** $\mathcal{M}_D$ 通过扭曲全1掩码并取并集来标识所有参考视角中均不可见的区域：

$$\mathcal { M } _ { D } = \bigcup _ { i = 1 } ^ { N } \left\{ \mathcal { W } _ { i \to T } \left( \mathcal { M } _ { i } ^ { 1 } , \mathbf { D } _ { i } , \mathbf { P } _ { i } , \mathbf { P } _ { T } , \mathbf { U } \right) \right\}$$

其中 $\mathcal{M}_i^1$ 为全1矩阵。$\mathcal{M}_D$ 将这些视差误差区域从掩码中解耦，避免因几何遮挡导致的误判。

同时，DGGS 引入预训练的**实体分割模型**对参考掩码 $\mathcal{M}_{Ref_i}$ 进行细化，得到 $\mathcal{M}_{Ref_i}^{En}$。当预测的干扰物区域超过像素数阈值时，该模型能够填充完整的实体边界，防止干扰物掩码碎片化。

### 辅助损失与最终训练目标

为强化对被遮挡区域的监督，DGGS 设计了辅助损失 $\mathcal{L}_A$，聚焦于查询视图中被遮挡但参考中可见的区域：

$$\mathcal { L } _ { A } = \sum _ { N } ^ { i = 1 } \mathcal { W } _ { T  i } { ( 1 - \mathcal { M } ) } \odot \mathcal { M } _ { R e f _ { i } } ^ { E n } \odot \| \mathbf { I } _ { i } - \mathcal { G } ( \mathbf { P } _ { i } ) \| _ { 2 } ^ { 2 }$$

其中 $\mathcal{W}_{Ti}$ 将查询掩码反向扭曲到参考视角，$(1-\mathcal{M})$ 标识查询视图中的被遮挡区域，$\mathcal{M}_{Ref_i}^{En}$ 确保仅对参考中可见的实体区域施加监督。

最终训练目标联合掩码重建损失和辅助损失：

$$\arg \operatorname* { m i n } _ { \pmb { \theta } } \mathcal { M } \odot \left\| \mathbf { I } _ { T } - \mathcal { G } \left( \mathbf { P } _ { T } \right) \right\| _ { 2 } ^ { 2 } + \mathcal { L } _ { A }$$

其中 $\mathcal{M}$ 为经过参考过滤和掩码细化后的最终干扰物掩码。

### 两阶段推理框架

推理阶段，DGGS 采用两阶段策略。第一阶段进行粗重建，并利用**参考评分机制**对场景图像池中的所有候选视图计算掩码覆盖率和质量分数；第二阶段基于评分选择最优的 $N$ 个参考视图，并通过**干扰物剪枝**从三维高斯原语中移除干扰物区域对应的属性，抑制残余伪影。这一设计在不增加 GPU 显存的前提下实现了参考视图的动态重选与干扰物抑制。

## 实验与关键发现

### 核心实验设置

所有重新训练的基线方法在相同的数据集、超参数和评估协议下进行公平比较：训练迭代次数统一为10K，图像分辨率下采样至192×256。评估时，On-the-go数据集使用其“extra”视图，RobustNeRF数据集使用“clean”视图，并排除Crab1场景以避免干扰物泄漏。集成干扰物掩码的基线方法（如RobustNeRF、NeRF-HuGS等）均按其原始设计嵌入到**Mvsplat**（Chen et al., ECCV 2024）的查询渲染损失中，确保比较基准一致。

### 主实验结果

在RobustNeRF数据集的五个场景上，DGGS在所有指标上均显著超越现有方法（Table 1）。与基线**Mvsplat**相比，DGGS的PSNR从15.45提升至21.74（+6.29），SSIM从0.515提升至0.758（+0.243），LPIPS从0.426降至0.237（-0.189）。这一提升幅度远超其他集成掩码策略的变体：**Mvsplat + RobustNeRF**（Sabour et al., CVPR 2023）仅达到17.11 PSNR，**Mvsplat + NeRF-HuGS**（Chen et al., CVPR 2024）为16.93，**Mvsplat + On-the-go**（Ren et al., CVPR 2024）为17.01，**Mvsplat + SLS**（Sabour et al., arXiv 2024）为17.03。值得注意的是，DGGS的前馈掩码预测甚至优于需要场景特定优化的方法，验证了其泛化能力的有效性。

在更广泛的场景测试中，DGGS同样表现稳健：Arcdetriomphe场景上PSNR达20.32（Mvsplat为14.96），Mountain场景上达16.37（Mvsplat为13.73），分别提升5.36和2.64 dB。

### 消融实验：各组件贡献

Table 2的消融实验系统性地揭示了DGGS各组件的因果贡献链：

**训练组件消融。** 从基础鲁棒掩码（M_Rob）出发，PSNR为17.11。添加基于参考的掩码预测（Reference-based Mask Prediction）后，PSNR跃升至20.35（+3.24），这是整个方法中单步增益最大的改进，直接验证了利用参考视图重渲染非干扰区域来过滤查询掩码的核心洞察。进一步添加掩码细化模块（Mask Refinement，含视差解耦和实体分割），PSNR提升至21.02（+0.67），构成DGGS-TR的完整训练方案。

**推理组件消融。** 在DGGS-TR基础上，引入参考评分机制（Reference Scoring）后PSNR从21.02提升至21.47（+0.45），证明通过重新选择干扰物最少、视差最小的参考视图可有效缓解参考中干扰物对重建质量的影响。最终添加干扰物剪枝策略（Distractor Pruning），PSNR达到21.74（+0.27），构成完整的DGGS。该剪枝模块在精细推理阶段根据参考掩码从3D高斯原语中移除干扰物区域对应的属性，有效抑制残余伪影。

**辅助模块消融。** 移除参考实体分割（w/o Reference Entity Seg）导致PSNR降至20.79，移除辅助损失（w/o Aux Loss）降至20.64，表明两者均有正向贡献。但论文指出，预训练分割模型并非不可替代——在不严重损害重建质量的前提下可替换为其他分割方案，这降低了方法对外部模型的刚性依赖。

### 推理效率分析

DGGS的两阶段推理策略在提升质量的同时引入了额外的计算开销（Table 4）。不过，论文指出可通过降低第一阶段粗重建的分辨率来缓解效率问题，在保持掩码预测和参考评分有效性的前提下减少计算量。

![[assets/figures/papers/paper_list_l79_https_openreview_net_forum_id_G33Iemmj3Z/figures/006_Table_4.jpg]]
*Table 4: Comparison on Efficiency*

### 失败模式分析

尽管DGGS在多数场景下表现优异，仍存在明确的失效边界：

1. **大范围共同遮挡。** 当多个参考视图之间存在大面积共同遮挡时，DGGS无法推理出被遮挡区域的正确几何，因为其核心机制依赖于参考视图间的3D一致性——共同遮挡区域在所有参考中均不可见，缺乏有效的几何线索。
2. **无生成式补全能力。** DGGS不具备生成式补全功能，共同遮挡区域可能产生散斑伪影（Figure 16展示了此类失败案例）。这源于方法本质上是基于可见区域的掩码过滤和剪枝，而非对缺失内容进行生成式填充。
3. **两阶段推理延迟。** 相比单阶段方法，两阶段推理引入了额外延迟，尽管可通过降低第一阶段分辨率部分缓解。

### 关键图表结论

- **Figure 5** 的定性比较显示，重新训练的基线方法在未见场景中普遍存在干扰物伪影和空洞，而DGGS的重建结果更为干净完整。
- **Figure 6** 对比了DGGS的前馈掩码预测与场景特定方法的掩码质量，表明DGGS无需逐场景优化即可达到甚至超越后者的掩码精度。
- **Figure 7** 展示了预训练模型、DGGS-TR与完整DGGS的定性差异，验证了推理阶段参考评分和干扰物剪枝对消除残余伪影的必要性。
- **Figure 8** 的推理策略消融直观展示了参考重选择和干扰物剪枝各自对重建质量的改善效果。
- **Figure 10** 分析了不同输入条件下的性能变化及参考非干扰阈值ρ_Ref的敏感性，为超参数选择提供了经验依据。

![[assets/figures/papers/paper_list_l79_https_openreview_net_forum_id_G33Iemmj3Z/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative Comparison of Re-trained Existing Methods across unseen scenes*

![[assets/figures/papers/paper_list_l79_https_openreview_net_forum_id_G33Iemmj3Z/figures/010_Figure_8.jpg]]
*Figure 8: Ablation for Inference Strategy*

![[assets/figures/papers/paper_list_l79_https_openreview_net_forum_id_G33Iemmj3Z/figures/011_Figure_7.jpg]]
*Figure 7: Qualitative Comparison of Pre-trained Models, DGGS-TR and DGGS*

![[assets/figures/papers/paper_list_l79_https_openreview_net_forum_id_G33Iemmj3Z/figures/014_Figure_10.jpg]]
*Figure 10: Performance Comparison under Different Inputs, and Ablation Studies for*

![[assets/figures/papers/paper_list_l79_https_openreview_net_forum_id_G33Iemmj3Z/figures/004_Figure_4.jpg]]
*Figure 4: Distractor-free Generalizable Inference Framework. DGGS initially samples adjacent references from the scene-images pool and leverages trained DGGS for coarse 3DGS. Based on the Reference Scoring mechanism, masks and quality scores are computed for all pool images. These masks and scores subsequently guide reference selection and Distractor Pruning for fine 3DGS*

## 定位与知识库关联

### 问题定位：泛化3DGS中的干扰物瓶颈

DGGS解决的核心问题是**泛化3DGS在真实世界数据上的训练稳定性与推理鲁棒性**。现有泛化3DGS方法（如 **Mvsplat** (Chen et al., ECCV 2024)、**Pixelsplat** (Charatan et al., CVPR 2024)）在干净的多视图数据上表现优异，但一旦训练数据或推理场景中存在干扰物（行人、车辆等瞬态物体），参考-查询视图间的3D一致性被破坏，导致训练信号被污染、推理时产生伪影和空洞。这一瓶颈的根源在于：泛化3DGS的前馈推理机制缺乏场景特定的优化能力来“遗忘”干扰物区域。

### 与现有干扰物处理方法的关系

现有干扰物处理方案可归为三类，DGGS与它们的关系如下：

**（1）场景特定掩码方法**：**RobustNeRF** (Sabour et al., CVPR 2023)、**NeRF-HuGS** (Chen et al., CVPR 2024)、**On-the-go** (Ren et al., CVPR 2024)、**SLS** (Sabour et al., arXiv 2024) 等方法通过迭代优化或扩散先验为每个场景生成干扰物掩码，再用于监督辐射场训练。这些方法需要场景特定的优化循环，无法直接嵌入泛化3DGS的前馈推理管线。DGGS将这些方法作为基线集成到Mvsplat的查询渲染损失中进行对比（Table 1），结果显示DGGS的前馈掩码预测在PSNR上领先最优场景特定方法约6.29 dB，证明**3D一致性引导的前馈掩码可以替代场景特定优化**。

**（2）启发式鲁棒掩码**：最简单的干扰物处理策略是通过渲染残差阈值生成二值掩码（Eq.4）。DGGS的消融实验（Table 2）显示，仅使用启发式鲁棒掩码的PSNR仅为17.11，且存在严重的**目标区域误分类**问题——静态场景结构常被错误标记为干扰物（Figure 3）。DGGS的**Reference-based Mask Prediction**模块通过参考视图的重渲染非干扰区域对查询掩码进行过滤，将PSNR提升至20.35，验证了跨视图3D一致性过滤的关键作用。

**（3）语义分割辅助**：DGGS在掩码细化阶段引入了预训练的**实体分割模型**（Entity Segmentation Model, Qi et al., 2022），用于填充被误分类的实体区域。消融实验显示，移除实体分割后PSNR从21.02降至20.79，但论文同时指出该预训练模型可被替代而不严重损害重建质量，说明语义先验是增强手段而非核心依赖。

### 方法边界与适用条件

DGGS的有效性依赖于以下条件：

1. **参考视图覆盖度**：当多个参考视图之间存在大范围共同遮挡时，DGGS无法推理出被遮挡区域的正确几何，因为其核心机制依赖参考视图间的3D一致性。此时可能产生散斑伪影，且不具备生成式补全能力。

2. **干扰物密度上限**：DGGS假设参考视图中存在足够的非干扰区域用于掩码过滤。在极端动态场景（大部分区域被干扰物覆盖）下，仅依靠3D一致性的方法可能失效，这是论文明确列出的开放问题。

3. **推理效率折衷**：两阶段推理框架（Reference Scoring + Distractor Pruning）相比单阶段方法增加了计算开销（Table 4），尽管可通过降低第一阶段分辨率缓解。

### 技术谱系定位

DGGS在泛化3DGS领域的技术贡献可定位为**训练与推理阶段的干扰物鲁棒性增强模块**。其核心创新——利用参考视图重渲染的非干扰区域作为掩码过滤指引——是一种**无额外监督的自监督机制**，不改变底层泛化3DGS的架构（如Mvsplat的编码器-解码器结构），而是通过修改损失函数（Eq.8：掩码加权MSE + 辅助损失）和推理策略（两阶段参考选择与剪枝）来提升鲁棒性。这种“即插即用”的设计使其理论上可适配其他泛化3DGS基线。

### 开放问题

1. **端到端整合**：当前参考评分与掩码预测是两个解耦的模块，可否将其整合为一个端到端可训练模块以进一步优化推理速度？
2. **极端动态场景**：在大部分区域被干扰物覆盖的场景下，仅依靠3D一致性的方法是否仍有效，还是需要引入时序先验？
3. **在线分割替代**：当前实体分割模型必须在训练前预计算并缓存，有无可能设计一个轻量级、在线可训练的分割模块以降低对额外模型的依赖？

## 原文 PDF

![[paperPDFs/ICLR_2026/Distractor_free_Generalizable_3D_Gaussian_Splatting_d5b1fa086266.pdf]]
