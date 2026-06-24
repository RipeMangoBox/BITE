---
title: "UniEdit: A Unified Tuning-Free Framework for Video Motion and Appearance Editing"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/UniEdit_A_Unified_Tuning_Free_Framework_for_Video_Motion_and_Appearance_Editing.pdf
aliases:
- UniEdit
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过辅助运动参考分支在时序自注意力（SA-T）层中注入由目标文本引导的注意力图，从而将所需的运动模式传递到主编辑路径。
primary_logic: 预训练文本到视频生成器中的时序自注意力层编码了帧间依赖（运动），空间自注意力层编码了帧内依赖（内容/结构）。基于这一洞察，可以分别在两类注意力层中注入运动特征和源视频特征，实现解耦的运动编辑与内容保持。
claims:
- 时序自注意力层编码了帧间依赖关系（运动），空间自注意力层编码了帧内依赖关系（内容和结构）。
- 在时序自注意力层中注入来自运动参考分支的注意力图，可以有效使主编辑路径生成与目标提示对齐的运动。
- 在空间自注意力层中注入来自重建分支的值特征，能够保留源视频的非编辑内容。
- UniEdit 在帧一致性 CLIP 分数和文本对齐 CLIP 分数上均优于现有最先进方法。
---

# UniEdit: A Unified Tuning-Free Framework for Video Motion and Appearance Editing

> [!tip] 核心洞察
> 预训练文本到视频生成器中的时序自注意力层编码了帧间依赖（运动），空间自注意力层编码了帧内依赖（内容/结构）。基于这一洞察，可以分别在两类注意力层中注入运动特征和源视频特征，实现解耦的运动编辑与内容保持。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniEdit：一个统一的免调优视频动作与外观编辑框架 |
| 英文题名 | UniEdit: A Unified Tuning-Free Framework for Video Motion and Appearance Editing |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2402.13185) · [Project](https://jianhongbai.github.io/UniEdit/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UniEdit |
| Dataset |  |

> [!tip] 效果简介
> - 视频帧一致性评估 上，Frame Consistency CLIP Score 98.37 vs 未提供具体基线值（最高为其他 SOTA 方法） (优于其他方法)。
> - 视频文本对齐评估 上，Textual Alignment CLIP Score 36.29 vs 未提供具体基线值 (优于其他方法)。
> - 用户偏好评估（帧一致性） 上，Frame Consistency User Preference 4.74 vs 未提供具体基线值 (优于其他方法)。

## 概述

**核心问题**：现有视频编辑方法主要面向外观编辑（如风格化、物体替换），却难以在时序维度上对运动进行编辑（例如将“弹吉他”变为“挥手”或“吃东西”）。其根本瓶颈在于这些方法缺乏运动先验，无法有效控制帧间依赖关系。

**核心洞察**：预训练文本到视频（T2V）生成模型中的**时序自注意力（SA-T）层编码了帧间依赖（即运动）**，而**空间自注意力（SA-S）层编码了帧内依赖（即内容与结构）**。这一发现为解耦运动编辑与内容保持提供了关键切入点。

**提出方法**：UniEdit 是一个统一的免调优（tuning-free）视频编辑框架，通过**在预训练 T2V 扩散模型的注意力层中注入特征**来分别控制运动与外观。其核心机制包括：
- 引入**辅助运动参考分支**，在 SA-T 层注入由目标文本引导的注意力图（查询 Q^m 与键 K^m），将所需运动模式传递到主编辑路径；
- 引入**辅助重建分支**，在 SA-S 层注入值特征 V^r，逐帧保留源视频的纹理与背景；
- 辅以**空间结构控制**与**掩膜引导协调**，进一步改善外观编辑的结构一致性与前景/背景区分。

**主要结果**：在帧一致性 CLIP 分数（98.37）、文本对齐 CLIP 分数（36.29）及用户偏好评估（帧一致性 4.74，文本对齐 4.88）上，UniEdit 均优于现有最先进方法，尤其在运动编辑任务上优势显著。

**方法定位**：UniEdit 属于**免调优的视频扩散模型特征注入**范式，区别于需要微调的 Tune-A-Video、Dreamix 等方法，也不同于仅面向外观编辑的 FateZero、Video-P2P 等零样本方案。其在方法谱系中的独特之处在于首次将时序自注意力注入与空间自注意力注入统一在同一框架中，实现运动与外观的解耦编辑。

## 背景与动机

### 视频编辑的现状与瓶颈

近年来，文本到图像（T2I）扩散模型的成功推动了图像编辑技术的快速发展。然而，将图像编辑能力扩展到视频领域面临着根本性挑战：视频编辑不仅需要逐帧保持视觉质量，还必须确保帧间的时序一致性。现有的视频编辑方法主要围绕**外观编辑**展开，例如风格化、物体替换或背景修改，其核心操作集中在空间维度上。

真正的瓶颈在于**运动编辑**——即改变视频中主体的动作模式（如将“弹吉他”变为“挥手”或“吃饭”），而保持主体外观和背景不变。这一任务要求模型在时序维度上精确操控帧间依赖关系，而现有方法对此几乎无能为力。造成这一困境的深层原因有二：

1. **缺乏运动先验**：大多数视频编辑方法直接沿用图像编辑的策略（如跨帧注意力传播或微调模型参数），并未显式建模运动模式。部分方法（如 **Tune-A-Video**、**Dreamix**）通过微调来适应目标运动，但微调过程难以在生成能力与内容保持之间取得平衡，且计算开销大。
2. **帧间依赖控制不足**：视频生成模型中的时序自注意力层天然编码了帧间依赖关系，但现有方法未能有效利用这一机制来注入目标运动，导致编辑结果要么运动不对齐，要么源内容发生漂移。

### 核心洞察：注意力层的双重角色

UniEdit 的核心洞察源于对预训练文本到视频（T2V）生成模型内部表征的深入分析：**时序自注意力（SA-T）层编码了帧间依赖关系（即运动），而空间自注意力（SA-S）层编码了帧内依赖关系（即内容和结构）**。这一发现为解耦运动编辑与内容保持提供了理论基础——如果能在 SA-T 层中注入目标运动特征，同时在 SA-S 层中保留源视频的内容特征，就有可能在免调优的条件下实现高质量的视频运动编辑。

Figure 6 的可视化实验为这一假设提供了实证支撑：SA-S 层中的空间查询图与视频帧的语义结构高度相关，而 SA-T 层中的跨帧时序注意力图与光流幅度高度一致，直接验证了两种注意力层分别编码“内容/结构”与“运动”的角色分工。

### 本文动机与目标

基于上述洞察，UniEdit 旨在构建一个**统一的免调优框架**，同时支持视频运动编辑和外观编辑。具体而言，本文试图回答以下关键问题：

- 如何在不微调预训练模型的前提下，将目标文本描述的运动模式注入到视频生成过程中？
- 如何在注入运动的同时，精确保持源视频中不应被编辑的内容（如背景、纹理）？
- 如何在一个框架中协调运动编辑与外观编辑，使其共享底层机制但又互不干扰？

通过将运动注入与内容保持分别定位到 SA-T 和 SA-S 层，并引入辅助分支提供特征来源，UniEdit 实现了运动与内容的解耦操控，为视频编辑领域提供了一个新的范式。

## 核心创新

UniEdit 的核心创新在于**首次在免调优框架下统一实现视频的运动编辑与外观编辑**，其关键在于对预训练文本到视频（T2V）扩散模型中两类自注意力机制的功能解耦与定向注入。

### 1. 瓶颈突破：从外观编辑到运动编辑

现有视频编辑方法（如 **FateZero**、**Video-P2P**、**Pix2Video**）主要面向外观编辑（风格化、物体替换、背景修改），其底层机制侧重于帧内空间特征的保持与修改。当面临运动编辑任务（如“弹吉他”变为“挥手”）时，这些方法暴露出根本性缺陷：**缺乏运动先验且无法有效控制帧间依赖关系**。部分方法（如 **Tune-A-Video**、**Dreamix**）虽尝试通过微调来改变运动，但需要在生成能力与内容保持之间进行艰难的权衡，且微调成本高昂。

UniEdit 的突破性洞察在于：**时序自注意力（SA-T）层编码了帧间依赖（即运动），而空间自注意力（SA-S）层编码了帧内依赖（即内容与结构）**。这一发现为解耦运动编辑与内容保持提供了理论基础（见 Figure 6 对注意力图与光流的可视化验证）。

### 2. 关键机制：双分支特征注入

基于上述洞察，UniEdit 设计了三个协同工作的路径（Figure 2）：

- **主编辑路径**：以 DDIM 逆向后得到的潜在表示 $z_T$ 为起点，在目标提示 $P_t$ 条件下执行去噪，生成最终编辑视频。
- **辅助重建分支**：以源提示 $P_s$ 为条件，从同一逆潜在 $z_T$ 出发去噪，生成源视频的特征。
- **辅助运动参考分支**：以目标提示 $P_t$ 为条件，生成与目标运动对齐的时序注意力图。

核心的 **changed slots** 体现在两个注入操作上：

**（1）运动注入（Motion Injection）—— 解决运动编辑难题**

在时序自注意力（SA-T）层中，将运动参考分支的查询 $Q^m$ 和键 $K^m$ 注入主编辑路径，替代原有的 $Q$、$K$：

$$\mathrm{SA-T}_{\mathrm{edit}}^{l} := \begin{cases} \mathrm{attn}(Q^{m}, K^{m}, V), & t > t_{1} \text{ and } l > l_{1} \\ \mathrm{attn}(Q, K, V), & \text{otherwise} \end{cases}$$

其中 $t_1$ 和 $l_1$ 在实际中均设为 0，意味着在所有去噪步和所有层中均执行运动注入。这一操作使得主编辑路径生成的帧间注意力模式与目标提示对齐，从而产生期望的运动（如挥手、进食），而无需任何模型微调。

**（2）内容保持（Content Preservation）—— 防止编辑过程中的内容漂移**

在空间自注意力（SA-S）层中，将重建分支的值特征 $V^r$ 注入主编辑路径：

$$\mathrm{SA-S}_{\mathrm{edit}}^{l} := \begin{cases} \mathrm{attn}(Q, K, V^{r}), & t > t_{0} \text{ and } l > l_{0} \\ \mathrm{attn}(Q, K, V), & \text{otherwise} \end{cases}$$

通过超参数 $t_0$ 和 $l_0$ 控制注入的时序和层级范围，逐帧保留源视频的纹理、背景等非编辑内容。消融实验（Figure 7）证实，移除该机制会导致严重的内容漂移；移除运动注入则导致运动与目标提示不对齐。

### 3. 辅助增强机制

**（1）空间结构控制（用于外观编辑）**

在外观编辑场景中，为保留源视频的粗粒度空间布局，在早期去噪步和深层中将重建分支的查询 $Q^r$ 和键 $K^r$ 注入空间自注意力：

$$\mathrm{SA-S}_{\mathrm{edit}}^{l} := \begin{cases} \mathrm{attn}(Q^{r}, K^{r}, V), & t < t_{2} \text{ and } l > l_{2} \\ \mathrm{attn}(Q, K, V), & \text{otherwise} \end{cases}$$

消融实验（Figure 8）表明，缺少该机制会导致视频空间布局发生不希望的变形。

**（2）掩膜引导协调**

利用前景/背景分割掩膜 $M_m$，通过掩膜引导注意力融合来改善背景一致性：

$$\mathrm{SA}_{\mathrm{mask}} := \mathrm{m-attn}(Q, K, V; M^{f}) \odot M_{m} + \mathrm{m-attn}(Q, K, V; M^{b}) \odot (1 - M_{m})$$

其中 $\mathrm{m-attn}(Q, K, V; M) = \mathrm{softmax}(\frac{QK^{T}}{\sqrt{d}} + M)V$，在 softmax 之前将掩膜 $M$ 加到注意力对数上以约束注意力区域。消融实验（Figure 9）证实该机制能进一步改善前景/背景的区分质量。

### 4. 创新性总结

UniEdit 的核心创新可归纳为 **“洞察—解耦—注入”** 三部曲：洞察预训练 T2V 模型中 SA-T 与 SA-S 的功能分工，将运动控制与内容保持解耦到不同的注意力层，通过双辅助分支的特征注入实现免调优的统一编辑。这一设计使得 UniEdit 在帧一致性 CLIP 分数（98.37）和文本对齐 CLIP 分数（36.29）上均超越现有最先进方法（Table 1），尤其在运动编辑任务上展现出显著优势（Figure 5）。

## 整体框架

UniEdit 遵循“先逆向后生成”（inversion-then-generation）的免调优编辑范式，其整体架构由三条并行的去噪路径构成：**主编辑路径（Main Editing Path）**、**辅助重建分支（Auxiliary Reconstruction Branch）** 和 **辅助运动参考分支（Auxiliary Motion-Reference Branch）**，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2402_13185/figures/002_Figure_2.jpg]]
*Figure 2: Overview of UniEdit. It follows an inversion-then-generation pipeline and consists of a main editing path, an auxiliary reconstruction branch and an auxiliary motion-reference branch. The reconstruction branch produces source features for content preservation, and the motion-reference branch yields text-guided motion features for motion injection. The source features and motion features are injected into the main editing path through spatial self-attention (SA-S) and temporal self-attention (SA-T) modules respectively (Sec. 4.1). We further introduce spatial structure control to retain the coarse structure of the source video (Sec. 4.2)*

### 输入输出流

给定一段源视频与对应的源文本提示 $P_s$，以及描述期望编辑效果的目标文本提示 $P_t$，UniEdit 的处理流程如下：

1. **DDIM 逆推**：首先对源视频进行 DDIM 逆推，获得初始噪声潜在表示 $z_T$。该潜在表示作为三条路径共同的起点，确保了编辑结果与源视频在结构上的初始锚定。
2. **主编辑路径**：以 $z_T$ 为起点，在目标提示 $P_t$ 条件下执行去噪过程，生成最终的编辑视频。该路径是视频输出的唯一来源，所有来自辅助分支的特征均通过注意力层注入到此路径中。
3. **辅助重建分支**：同样以 $z_T$ 为起点，但在源提示 $P_s$ 条件下执行去噪。该分支的作用是“记住”源视频的内容——它在空间自注意力（SA-S）层中产生值特征 $V^r$，用于向主编辑路径提供逐帧的纹理和背景信息，实现内容保持。
4. **辅助运动参考分支**：以 $z_T$ 为起点，在目标提示 $P_t$ 条件下执行去噪。该分支的核心产出是与目标运动对齐的时序注意力图——具体而言，它在时序自注意力（SA-T）层中产生查询 $Q^m$ 和键 $K^m$，通过注入主编辑路径来传递所需的运动模式。

### 模块间关系与特征注入

三条路径之间的协同通过两类自注意力层中的特征注入实现，其详细关系如 Figure 3 所示：

- **空间自注意力（SA-S）层中的内容保持**：在去噪步 $t > t_0$ 且层深度 $l > l_0$ 的条件下，主编辑路径的 SA-S 层将其值 $V$ 替换为重建分支的值 $V^r$，即 $\mathrm{attn}(Q, K, V^r)$。这一操作使主路径在生成新内容时能够直接引用源视频的帧内特征，从而保留非编辑区域的纹理、背景和物体身份。
- **时序自注意力（SA-T）层中的运动注入**：主编辑路径的 SA-T 层将其查询 $Q$ 和键 $K$ 替换为运动参考分支的 $Q^m$ 和 $K^m$，即 $\mathrm{attn}(Q^m, K^m, V)$。由于时序自注意力编码了帧间依赖关系（即运动信息），这一注入操作使主路径生成的帧间变化模式与目标提示对齐，实现从“弹吉他”到“挥手”等运动编辑。在实际设置中，控制注入范围的超参数 $t_1$ 和 $l_1$ 均设为 0，意味着运动注入作用于所有去噪步和所有层。

### 外观编辑的扩展机制

对于外观编辑场景（如风格化、物体替换、背景修改），UniEdit 在 SA-S 层中引入额外的**空间结构控制**：在早期去噪步（$t < t_2$）和深层（$l > l_2$）中，将主编辑路径的查询和键替换为重建分支的 $Q^r$ 和 $K^r$，即 $\mathrm{attn}(Q^r, K^r, V)$。这一机制在去噪初期锚定了源视频的粗粒度空间布局，防止外观编辑过程中出现结构崩塌。

### 掩膜引导协调

为进一步改善前景与背景的区分，UniEdit 引入**掩膜引导协调**模块。该模块利用从运动参考分支注意力图中提取的前景/背景分割掩膜 $M_m$，通过掩膜引导注意力 $\mathrm{m-attn}(Q, K, V; M) = \mathrm{softmax}(\frac{QK^T}{\sqrt{d}} + M)V$ 分别计算前景和背景的注意力输出，再按掩膜权重融合：

$$
\mathrm{SA}_{\mathrm{mask}} := \mathrm{m-attn}(Q, K, V; M^f) \odot M_m + \mathrm{m-attn}(Q, K, V; M^b) \odot (1 - M_m)
$$

这一机制有效抑制了前景运动编辑对背景区域的干扰，提升了整体编辑质量。

### 关键设计理念

整个框架的设计根植于一个核心洞察：预训练文本到视频扩散模型中的**时序自注意力层编码了帧间依赖（运动）**，而**空间自注意力层编码了帧内依赖（内容与结构）**。基于这一解耦特性，UniEdit 通过在两类注意力层中分别注入来自不同辅助分支的特征，实现了运动编辑与内容保持的分离控制——这是其能够统一处理运动编辑和外观编辑的根本原因。

## 核心模块与公式推导

UniEdit 的核心操作围绕视频扩散模型中两类自注意力层展开：**空间自注意力（SA-S）** 编码帧内依赖（内容与结构），**时序自注意力（SA-T）** 编码帧间依赖（运动）。基于这一洞察，方法通过三条分支的协同与特征注入，实现解耦的运动编辑与内容保持。

---

### 标准注意力操作

所有注入操作均基于缩放点积注意力，其定义为：

$$
\mathsf{attn}(Q, K, V) = \mathsf{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V \tag{1}
$$

其中 $Q$、$K$、$V$ 分别为查询、键和值，$d$ 为隐藏维度。

---

### 内容保持：空间自注意力值注入

为保留源视频的非编辑内容（纹理、背景），引入辅助重建分支（以源提示 $P_s$ 为条件），将其在 SA-S 层中产生的值特征 $V^r$ 注入主编辑路径：

$$
\mathrm{SA\text{-}S}_{\mathrm{edit}}^{l} :=
\begin{cases}
\mathsf{attn}(Q, K, V^{r}), & t > t_{0} \;\text{and}\; l > l_{0} \\[4pt]
\mathsf{attn}(Q, K, V), & \text{otherwise}
\end{cases} \tag{2}
$$

**机制**：主编辑路径的查询 $Q$ 和键 $K$ 保持不变（确保编辑方向由目标提示 $P_t$ 引导），仅将值 $V$ 替换为重建分支的 $V^r$。注入仅在去噪步 $t > t_0$ 且层 $l > l_0$ 时触发——早期去噪步和浅层保留原值，以维持编辑灵活性；深层注入则锁定内容细节。这一设计使编辑结果逐帧继承源视频的纹理特征。

---

### 运动注入：时序自注意力查询-键注入

为实现运动编辑（如“弹吉他”变为“挥手”），引入辅助运动参考分支（以目标提示 $P_t$ 为条件），将其在 SA-T 层中产生的查询 $Q^m$ 和键 $K^m$ 注入主编辑路径：

$$
\mathrm{SA\text{-}T}_{\mathrm{edit}}^{l} :=
\begin{cases}
\mathsf{attn}(Q^{m}, K^{m}, V), & t > t_{1} \;\text{and}\; l > l_{1} \\[4pt]
\mathsf{attn}(Q, K, V), & \text{otherwise}
\end{cases} \tag{3}
$$

**机制**：注入 $Q^m$ 和 $K^m$ 实质上是将运动参考分支生成的时序注意力图传递给主编辑路径。由于 SA-T 层的注意力权重刻画了帧间依赖关系，这一注入使主路径的去噪过程遵循目标提示所描述的运动模式。实践中 $t_1$ 和 $l_1$ 均设为 0，即全步全层注入，确保运动信息充分传递。

---

### 空间结构控制：外观编辑的结构保持

对于外观编辑任务（如风格化、物体替换），还需保持源视频的粗粒度空间结构。此时在 SA-S 层中注入重建分支的查询 $Q^r$ 和键 $K^r$：

$$
\mathrm{SA\text{-}S}_{\mathrm{edit}}^{l} :=
\begin{cases}
\mathsf{attn}(Q^{r}, K^{r}, V), & t < t_{2} \;\text{and}\; l > l_{2} \\[4pt]
\mathsf{attn}(Q, K, V), & \text{otherwise}
\end{cases} \tag{4}
$$

**机制**：与内容保持的值注入不同，此处替换 $Q$ 和 $K$ 使注意力图与源视频一致，从而在早期去噪步（$t < t_2$）和深层（$l > l_2$）锁定空间布局。后期去噪步恢复原 $Q$、$K$，允许目标提示引导外观变化。

---

### 掩膜引导协调

为进一步改善前景/背景一致性，引入掩膜引导注意力。首先定义掩膜注意力：

$$
\mathsf{m\text{-}attn}(Q, K, V; M) = \mathsf{softmax}\left(\frac{QK^T}{\sqrt{d}} + M\right)V \tag{5}
$$

其中 $M$ 为注意力掩膜，在 softmax 前加到注意力对数上以约束注意力区域。随后进行掩膜引导的自注意力融合：

$$
\mathrm{SA}_{\mathrm{mask}} := \mathsf{m\text{-}attn}(Q, K, V; M^{f}) \odot M_{m} \;+\; \mathsf{m\text{-}attn}(Q, K, V; M^{b}) \odot (1 - M_{m}) \tag{6}
$$

其中 $M_m$ 为运动分支产生的前景掩膜，$M^f$ 和 $M^b$ 分别为前景和背景的注意力掩膜。该融合策略使前景和背景区域各自遵循对应的注意力约束，缓解前景编辑对背景的干扰。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2402_13185/figures/003_Figure_3.jpg]]
*Figure 3: Detailed illustration of the relationship between the main editing path, the auxiliary reconstruction branch and the auxiliary motion-reference branch. The content preservation, motion injection and spatial structure control are achieved by the fusion of Q (query), K (key), V (value) features in spatial self-attention (SA-S) and temporal selfattention (SA-T) modules*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2402_13185/figures/007_Figure_6.jpg]]
*Figure 6: Visualization of spatial query in SA-S (second row), cross-frame temporal attention maps in SA-T (third row), and the magnitude of optical flow (fourth row)*

## 实验与分析

### 主实验结果

UniEdit 在视频编辑的两个核心维度——帧一致性（Frame Consistency）和文本对齐（Textual Alignment）上均达到最优水平。定量评估采用 CLIP Score 和用户偏好打分两种方式，结果汇总于 Table 1。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2402_13185/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison (CLIP Score and User Preference) with state-of-the-art video editing techniques*

在帧一致性 CLIP Score 上，UniEdit 取得 **98.37**，优于所有对比方法；在文本对齐 CLIP Score 上，UniEdit 取得 **36.29**，同样领先。用户偏好评估进一步验证了这一优势：帧一致性的用户评分达到 **4.74**，文本对齐的用户评分达到 **4.88**，均显著高于基线方法。这表明 UniEdit 在保持源视频内容一致性的同时，能更精准地生成与目标文本描述对齐的运动。

定性对比（Figure 5、Figure 10–11）显示，现有方法在运动编辑场景下普遍存在明显缺陷：**Tune-A-Video** 和 **Dreamix** 等基于微调的方法虽能改变运动，但往往导致内容漂移或背景失真；**FateZero**、**Pix2Video**、**Video-P2P** 等外观编辑方法在运动编辑任务上几乎完全失效，无法产生与目标提示对应的动作变化。UniEdit 则通过解耦的运动注入与内容保持机制，在运动编辑上显著优于基线，同时保持源视频的纹理、背景和结构完整性。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2402_13185/figures/005_Figure_5.jpg]]
*Figure 5: Comparison with state-of-the-art methods for both video motion and appearance editing. It shows that UniEdit achieves better source content preservation, and outperforms baselines in motion editing by a large margin*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2402_13185/figures/011_Figure_10.jpg]]
*Figure 10: More comparison with state-of-the-art methods*

### 消融实验

为验证各组件的独立贡献，论文进行了系统的消融研究：

- **内容保持与运动注入的贡献**（Figure 7）：分别移除内容保持模块（即停止在 SA-S 层中注入重建分支的 V^r 特征）或运动注入模块（即停止在 SA-T 层中注入运动参考分支的 Q^m、K^m），均导致编辑质量显著下降。移除内容保持会导致纹理漂移和背景失真；移除运动注入则使生成视频的动作与目标提示不对齐。这证实了两个组件均为必需。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2402_13185/figures/008_Figure_7.jpg]]
*Figure 7: The proposed content preservation and motion injection both contribute to the final results*

- **空间结构控制的作用**（Figure 8）：在外观编辑场景下，移除空间结构控制（即停止在早期去噪步和深层 SA-S 层中用 Q^r、K^r 替换主路径的 Q、K）会导致视频的空间布局发生变形，表明该机制对于维持源视频的粗粒度结构至关重要。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2402_13185/figures/009_Figure_8.jpg]]
*Figure 8: Ablation on spatial structure control and controllable video editing*

- **掩膜引导协调的贡献**（Figure 9）：引入掩膜引导的注意力融合（Eq. 5–6）能够进一步改善前景与背景的区分，提升编辑结果的背景一致性。消融结果显示，移除该模块后，前景编辑区域与背景之间的过渡变得不自然。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2402_13185/figures/010_Figure_9.jpg]]
*Figure 9: Ablation on mask-guided coordination*

### 关键图表结论

- **Figure 6** 提供了注意力机制假设的直接证据：空间自注意力（SA-S）中的查询特征与帧内内容结构高度相关，而时序自注意力（SA-T）中的跨帧注意力图与光流（optical flow）的幅度分布高度一致。这从实证角度支撑了“SA-T 编码帧间运动依赖、SA-S 编码帧内内容依赖”的核心洞察。

- **Figure 4、12–17** 展示了 UniEdit 在多种编辑场景下的广泛适用性，包括动作编辑（如“弹吉他→挥手”“弹吉他→进食”）、风格化、刚性与非刚性物体替换、背景修改等。结果表明方法在不同场景下均能保持源视频内容的一致性。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2402_13185/figures/004_Figure_4.jpg]]
*Figure 4: Examples edited by UniEdit. For each case, the upper frames come from the source video, and the lower frames indicate the edited results with the target prompt. We encourage the readers to watch the videos and make evaluations*

### 方法局限与失败模式

尽管 UniEdit 在运动与外观编辑上表现优异，但论文明确指出以下局限：

1. **不支持同步运动与外观编辑**：当前框架无法在单次推理中同时进行运动编辑和外观编辑，两类任务需分别执行。
2. **超参数需手动调节**：多个时序/层级的注入超参数（如 t₀、l₀、t₁、l₁、t₂、l₂）缺乏自动化确定方案，实际使用中需人工调试。
3. **掩膜质量依赖**：掩膜引导协调的效果受限于前景/背景分割的准确性，从注意力图或外部分割模型获取的掩膜质量波动可能影响最终结果。
4. **基础模型依赖性**：方法以 LaVie 作为基础 T2V 模型实例化，对预训练模型的训练分布和版本存在依赖，迁移到其他视频扩散模型（如 SVD、VideoCrafter）尚待验证。
5. **极端场景未充分测试**：在极端背景动态或大幅度运动变换的场景下，编辑质量可能下降，论文未对此类情况进行系统评估。

### 待解决问题

论文提出的开放问题包括：如何在一个统一框架中同时执行动作和外观编辑；如何自动确定多个超参数以降低人工调参负担；如何将方法扩展到更长视频和更复杂的运动编辑；以及能否将统一的编辑能力迁移到其他视频扩散模型。这些问题指向了该方向的后续研究空间。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2402_13185/figures/012_Figure_11.jpg]]
*Figure 11: More comparison with state-of-the-art methods*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2402_13185/figures/017_Figure_16.jpg]]
*Figure 16: More motion editing results of UniEdit*

## 方法谱系与知识库定位

### 1. 问题定位与核心瓶颈

视频编辑任务长期存在“外观”与“运动”两大分支各自为战的局面：外观编辑（如风格化、目标替换）已在免调优（tuning‑free）路径上取得显著进展，而运动编辑（如“弹吉他→挥手”）则因缺乏显式的运动先验和帧间依赖控制手段，一直依赖微调（fine‑tuning）或帧间传播，难以在保持源内容的同时生成与目标文本对齐的新运动。UniEdit 的核心瓶颈判断是：**预训练文本到视频（T2V）扩散模型中的时序自注意力（SA‑T）层天然编码了帧间依赖（即运动），空间自注意力（SA‑S）层编码了帧内依赖（即内容/结构）**（Section 1，置信度 0.95）。基于这一洞察，UniEdit 将运动编辑和外观编辑统一到同一免调优框架下，通过在 SA‑T 层注入目标文本引导的运动注意力图、在 SA‑S 层注入源视频的内容特征，实现了运动‑内容的解耦控制。

### 2. 与基线工作的关系

UniEdit 的基线覆盖了视频外观编辑、运动编辑及通用视频编辑三大类，其与各基线的关系可从“控制维度”和“是否需要微调”两个轴来定位。

**（1）外观编辑基线：**  
- **MasaCtrl**（图像编辑方法，经改造后用于视频外观编辑）和 **FateZero**（零样本视频外观编辑）均以空间自注意力特征注入实现内容保持，但缺少对时序维度的运动控制。  
- **Pix2Video** 和 **Video‑P2P** 分别采用帧间传播和局部外观编辑策略，在处理大幅运动时容易出现内容漂移或空间布局变形。  

UniEdit 在继承上述方法“空间自注意力注入保持内容”这一有效策略的同时，将其规范化为**辅助重建分支在 SA‑S 层注入值特征 $V^r$**（Eq. 2），并额外引入**空间结构控制**（Eq. 4，在早期去噪步和深层中用 $Q^r, K^r$ 替换主路径的查询和键），从而在大幅运动场景下仍能保持源视频的粗粒度空间结构。

**（2）运动编辑基线：**  
- **Tune‑A‑Video** 和 **Dreamix** 通过微调模型来改变运动模式，但微调会破坏预训练生成能力，且难以在运动编辑与内容保持之间取得平衡。  

UniEdit 完全免除了微调，转而采用**辅助运动参考分支在 SA‑T 层注入查询 $Q^m$ 和键 $K^m$**（Eq. 3，$t_1$ 和 $l_1$ 在实际中均设为 0），使主编辑路径直接继承由目标文本引导的帧间注意力模式。这一“注意力图注入”机制是 UniEdit 区别于所有运动编辑基线的核心因果旋钮。

**（3）统一框架的优势：**  
在定量对比中（Table 1，置信度 0.98），UniEdit 在帧一致性 CLIP 分数（98.37）和文本对齐 CLIP 分数（36.29）上均优于所列基线；用户偏好评估中，帧一致性和文本对齐分别达到 4.74 和 4.88。定性对比（Figure 5）进一步表明，UniEdit 在运动编辑上对基线形成了大幅领先，同时在外观编辑中保持了更好的源内容一致性。

### 3. 方法谱系中的位置

UniEdit 处于**免调优视频扩散模型编辑**的交叉点上，其方法论贡献在于首次将“运动编辑”和“外观编辑”统一为一个**基于注意力解耦的三分支架构**：

- **主编辑路径**：以 DDIM 逆向后得到的潜在 $z_T$ 为起点，在目标提示 $P_t$ 条件下执行去噪，生成最终编辑视频。  
- **辅助重建分支**：以源提示 $P_s$ 为条件，从同一 $z_T$ 出发去噪，为内容保持提供 $V^r$ 特征。  
- **辅助运动参考分支**：以目标提示 $P_t$ 为条件，生成与目标运动对齐的时序注意力图，注入主路径的 SA‑T 层。  

三个分支共享同一初始噪声 $z_T$，通过**在 SA‑S 和 SA‑T 层中分别注入值和查询/键特征**，实现了对“内容”和“运动”的独立控制。这一设计将视频编辑从“修改像素/潜在”的范式提升到“操纵注意力图”的范式，与图像编辑中的 Prompt‑to‑Prompt 等方法在思想上同源，但将其扩展到了时空维度。

此外，UniEdit 还引入了**掩膜引导协调**（Eq. 5–6），利用前景/背景分割掩膜 $M_m$ 对注意力进行空间约束，进一步改善背景一致性。这一机制使得 UniEdit 在局部编辑场景中具备了可控性，与基于掩膜的图像编辑方法形成呼应。

### 4. 适用边界与局限

尽管 UniEdit 在运动与外观编辑上展现了统一的免调优能力，其适用边界和局限同样明确：

- **不支持运动与外观同时编辑**：当前框架在单次推理中只能执行运动编辑或外观编辑之一，无法同时改变动作和纹理/风格。  
- **超参数依赖人工调节**：SA‑S 和 SA‑T 注入的时序/层级超参数（$t_0, l_0, t_1, l_1, t_2, l_2$）需手动设定，缺乏自动化方案，影响易用性和可复现性。  
- **掩膜质量敏感**：掩膜引导协调依赖前景/背景分割的准确性，从注意力图或外部模型获得的分割质量可能成为性能瓶颈。  
- **基础模型依赖**：UniEdit 以 LaVie 为实例化基础模型（Section 5.1），对基础 T2V 模型的训练分布和版本存在依赖；迁移到其他视频扩散模型（如 SVD、VideoCrafter）尚未验证。  
- **极端动态场景未充分测试**：极端背景动态或大范围运动变换可能导致编辑质量下降，这一边界条件尚未系统评估。

### 5. 开放问题与后续方向

从 UniEdit 的局限出发，可提炼出以下开放问题：

1. **联合运动‑外观编辑**：如何在一个统一的框架中同时执行动作和外观编辑，使“弹吉他的熊猫”变为“挥手的金属风格熊猫”？  
2. **超参数自动确定**：能否通过学习或启发式策略自动确定多个注入超参数，以减轻人工调参负担？  
3. **长视频与复杂运动扩展**：如何将该方法扩展到更长的视频和更复杂的运动编辑，同时保持时序一致性？  
4. **跨模型迁移**：UniEdit 的注意力注入策略能否泛化到其他视频扩散模型（如 SVD、VideoCrafter）？不同模型的 SA‑T/SA‑S 层语义是否具有一致的“运动/内容”编码特性？  
5. **更精细的运动控制**：当前运动注入以全时序注意力图替换的方式实现，能否引入更细粒度的运动控制（如运动幅度、速度、局部运动）？

这些开放问题指向了视频编辑从“单一维度免调优”向“多维度联合可控”演进的关键路径，UniEdit 所建立的“注意力解耦‑注入”框架为后续研究提供了可扩展的基础架构。

## 原文 PDF

![[paperPDFs/arxiv_2024/UniEdit_A_Unified_Tuning_Free_Framework_for_Video_Motion_and_Appearance_Editing.pdf]]
