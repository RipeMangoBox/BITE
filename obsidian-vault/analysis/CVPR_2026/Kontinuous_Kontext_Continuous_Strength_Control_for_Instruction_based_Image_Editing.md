---
title: "Kontinuous Kontext: Continuous Strength Control for Instruction-based Image Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Kontinuous_Kontext_Continuous_Strength_Control_for_Instruction_based_Image_Editing.pdf
project_link: "https://snapresearch.github.io/kontinuouskontext/"
code_link: null
aliases:
- KK
- KKCSCIBIE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 调制空间（modulation space）中的文本令牌调制参数；通过将标量编辑强度与编辑指令嵌入映射为调制参数的偏移量，可以校准地控制编辑强度。
primary_logic: 编辑强度信息天然存在于扩散Transformer模型的调制空间中，通过一个轻量级的投影网络（strength projector）将强度标量与指令嵌入映射到该空间的偏移量，即可实现统一、连续的强度控制，而无需为每种编辑属性单独训练模型。
claims:
- 直接缩放文本令牌的调制参数（v∈0.5~1.3）可产生不同强度的编辑，但变化与强度并非线性对齐，表明调制空间可编码强度但需要校准。
- 使用带文本嵌入条件的强度投影器（strength projector）在调制空间注入标量强度，产生了平滑的编辑轨迹，在δ_smooth和CLIP-dir上显著优于文本空间注入和去除文本条件的变体。
- 在PIEbench基准测试和用户研究中，Kontinuous Kontext在编辑平滑度、保真度和指令跟随方面均显著优于基于插值的基线（如Diffmorpher, Freemorph, WAN-Video）和领域特定方法（如ConceptSliders, MARBLE）。
- PIEbench 上 δ_smooth↓ = 0.329
---

# Kontinuous Kontext: Continuous Strength Control for Instruction-based Image Editing

> [!tip] 核心洞察
> 编辑强度信息天然存在于扩散Transformer模型的调制空间中，通过一个轻量级的投影网络（strength projector）将强度标量与指令嵌入映射到该空间的偏移量，即可实现统一、连续的强度控制，而无需为每种编辑属性单独训练模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | 连续上下文：面向指令引导图像编辑的连续强度控制 |
| 英文题名 | Kontinuous Kontext: Continuous Strength Control for Instruction-based Image Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.08532) · [Project](https://snapresearch.github.io/kontinuouskontext/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Kontinuous Kontext |
| Dataset | PIEbench |

> [!tip] 效果简介
> - PIEbench 上，δ_smooth↓ 0.329 vs 0.371 (Diffmorpher) (−0.042)；CLIP-Dir↑ 0.241 vs 0.181 (Diffmorpher) (+0.06)；δ_smooth↓ 0.329 vs 0.365 (Freemorph) (−0.036)。
> - PIEbench (face/stylization subset) 上，δ_smooth↓ 0.098 vs 0.143 (ConceptSliders) (−0.045)；CLIP-Dir↑ 0.382 vs 0.186 (ConceptSliders) (+0.196)。
> - PIEbench (material subset) 上，δ_smooth↓ 0.350 vs 2.577 (MARBLE) (−2.227)。

## 概要

指令驱动的图像编辑模型近年来取得了显著进展，用户仅需通过自然语言指令即可对图像进行修改。然而，现有方法存在一个关键瓶颈：它们仅能通过文本指令控制编辑的**内容**（“编辑什么”），却缺乏对编辑**程度**（“编辑多少”）的精细、连续控制。用户只能获得离散的“有编辑/无编辑”二元结果，无法像操作滑块一样平滑地调节编辑强度——例如，无法将“增加微笑”的指令从微妙的嘴角上扬连续过渡到灿烂的笑容。

针对这一问题，本文提出了 **Kontinuous Kontext**，一种统一的、面向指令引导图像编辑的连续强度控制方法。该方法的核心洞察在于：编辑强度信息天然存在于扩散Transformer（DiT）模型的调制空间（modulation space）中。通过一个轻量级的强度投影器（strength projector），将标量编辑强度与编辑指令嵌入共同映射为调制参数的偏移量，即可实现对编辑强度的校准控制，而无需为每种编辑属性单独训练模型。

该方法在 PIEbench 基准测试上展现出显著优势：在编辑平滑度（δ_smooth）上达到 0.329，相比基于插值的基线方法 **Diffmorpher**（0.371）和 **Freemorph**（0.365）分别降低 11.3% 和 9.9%；在指令跟随能力（CLIP-Dir）上达到 0.241，分别超越上述方法 33.1% 和 27.5%。与领域特定方法相比，Kontinuous Kontext 以统一的架构超越了需要逐属性训练的 **ConceptSliders** 和 **MARBLE**，在面部/风格化子集上 CLIP-Dir 领先 **ConceptSliders** 达 105.4%（0.382 vs 0.186），在材料编辑子集上 δ_smooth 仅为 **MARBLE** 的 13.6%（0.350 vs 2.577）。

在方法谱系上，Kontinuous Kontext 属于**推理时连续控制**与**参数高效微调**的交叉范式：它以 **Flux Kontext**（DiT架构的指令编辑模型）为基座，通过训练秩-4 LoRA适配器和4层MLP强度投影器实现强度注入，区别于基于LoRA权重插值（ConceptSliders）、扩散特征空间插值（Freemorph）或视频帧插值（WAN-Video）的编辑后插值路线。该方法也存在明确局限：对本质上离散的编辑（如物体插入/移除）不适用，继承了基模型在精确几何变换上的弱点，且无法实现编辑强度的外推（s > 1 时编辑效果不再增强）。



### 指令驱动图像编辑的现状与瓶颈

指令驱动的图像编辑（instruction-driven image editing）允许用户通过自然语言描述对图像进行修改，极大地降低了编辑门槛。以 **Flux Kontext** 为代表的最新模型基于扩散Transformer（DiT）架构，能够根据文本指令生成高质量的编辑结果。然而，这类模型存在一个根本性局限：**它们仅通过文本指令控制编辑的“内容”，却无法控制编辑的“程度”**。用户只能得到离散的“有编辑/无编辑”二值结果，缺乏对编辑强度的精细、连续调节能力。

例如，当用户希望“将头发染成金色”时，现有模型只能输出完全染色的结果，而无法实现从“微染”到“全染”的平滑过渡。这种“全有或全无”的控制模式严重限制了图像编辑的实用性和创造性表达。

### 现有连续控制方法的碎片化困境

针对特定编辑属性的连续控制，已有一些领域特定方法被提出：

- **基于LoRA权重插值的方法**：如 **ConceptSliders**，为每种编辑属性（如年龄、表情）单独训练低秩适配器（LoRA），通过插值适配器权重实现强度控制。但该方法需要为每种属性独立训练模型，缺乏通用性。
- **基于扩散特征空间插值的方法**：如 **MARBLE**，专注于材料属性编辑，同样局限于特定领域。
- **编辑后插值方法**：如 **Diffmorpher**（基于LoRA权重插值）、**Freemorph**（基于扩散特征空间插值）和 **WAN-Video**（视频帧插值模型），这些方法先生成全强度编辑，再通过插值生成中间状态。然而，插值过程往往引入伪影、身份不一致或突变跳跃，且无法与编辑指令建立语义对齐。

上述方法的共同缺陷在于：**它们要么是领域特定的（需要为每种编辑属性单独训练），要么依赖不可靠的后处理插值，缺乏一个统一的、可校准的连续强度控制框架**。

### 核心洞察：调制空间编码编辑强度

本文的关键发现源于一个简单实验：在 Flux Kontext 的推理过程中，直接缩放文本令牌的调制参数（modulation parameters）——即控制文本信息如何注入扩散网络的缩放和偏移系数——可以产生不同强度的编辑效果（Fig. 6a, Fig. 14）。这一现象揭示了**编辑强度信息天然存在于扩散Transformer的调制空间中**。

然而，直接缩放存在明显问题：**编辑变化与强度标量之间并非线性对齐**，用户无法通过标量值精确预测编辑程度。这表明调制空间虽然能编码强度，但需要专门的校准机制，将用户友好的标量输入映射为恰当的调制参数偏移量。

### 本文动机与目标

基于上述洞察，本文提出 **Kontinuous Kontext**，旨在实现**统一的、连续的编辑强度控制**。核心思路是：

1. **统一性**：不针对每种编辑属性单独训练，而是构建一个通用框架，适用于任意指令驱动的编辑任务。
2. **连续性**：通过一个标量编辑强度 $s \in [0, 1]$，实现从无编辑（$s=0$）到完全编辑（$s=1$）的平滑过渡。
3. **可校准性**：设计一个轻量级的**强度投影器（strength projector）**，将标量强度与编辑指令嵌入共同映射为调制空间的偏移量，确保用户输入的强度值与实际编辑程度之间建立可靠的对应关系。

通过将连续强度控制注入指令驱动编辑模型，Kontinuous Kontext 填补了“编辑内容”与“编辑程度”之间的控制鸿沟，为图像编辑提供了更细粒度的表达维度。



## 核心方法与创新机理

Kontinuous Kontext 的核心创新在于**首次将标量编辑强度作为显式控制维度引入指令驱动的图像编辑模型**，并通过调制空间注入机制实现统一、连续的强度控制。与现有方法相比，其关键突破体现在以下三个层面。

### 1. 编辑强度：从离散二元到连续标量

现有指令驱动编辑模型（如 Flux Kontext）仅通过文本指令控制编辑**内容**，编辑程度呈现“全有或全无”的二元状态——要么不编辑，要么执行完整编辑。用户无法精细调节编辑的强弱程度。Kontinuous Kontext 将编辑控制从离散的二元决策扩展为**连续标量空间**：模型额外接受一个标量编辑强度 $s \in [0, 1]$ 作为输入，与编辑指令配对后，实现对编辑程度的平滑调节。

这一改变量（changed slot）的核心意义在于：用户无需反复调整文本指令来逼近期望效果，而是通过单一强度参数即可遍历从“无编辑”（$s=0$）到“完整编辑”（$s=1$）的整个连续谱系。Figure 1 展示了该方法在多种编辑属性（如发型颜色、材质变换、风格化）上产生的平滑编辑轨迹。

### 2. 控制空间：从文本空间到调制空间

如何将标量强度注入模型是关键设计选择。直观方案是将强度信息注入文本空间——例如将强度投影器的输出作为额外的文本令牌（text-space conditioning）。然而，消融实验表明，这一方案导致编辑突变，平滑度指标 $\delta_{\text{smooth}}$ 高达 1.468（Table 2），远差于完整方案（0.329）。**文本空间并非平滑的强度控制空间**——文本令牌的离散语义特性使其难以编码连续变化的编辑程度。

Kontinuous Kontext 的核心洞察是：**编辑强度信息天然存在于扩散 Transformer（DiT）模型的调制空间（modulation space）中**。在 Flux Kontext 等 DiT 架构中，文本令牌通过调制参数（scale 和 shift）影响特征变换。一个简单的验证实验（Figure 6a, Figure 14）表明，直接缩放文本令牌的调制参数（$v \in [0.5, 1.3]$）可以产生不同强度的编辑，但变化与强度并非线性对齐——这说明调制空间可以编码强度，但需要学习校准。

基于此洞察，该方法设计了一个**强度投影器（strength projector）**：一个轻量级 MLP 网络，将标量强度 $s$ 和池化 CLIP 文本嵌入映射为调制参数的偏移量 $(\Delta y_{\text{scale}}, \Delta y_{\text{shift}})$，叠加到原有调制参数上（Figure 6b）。这一设计将强度控制从文本空间迁移到调制空间，实现了校准的、平滑的强度调节。

### 3. 统一框架：从领域特定到通用控制

现有连续编辑控制方法（如 **ConceptSliders**、**MARBLE**）采用领域特定策略：为每种编辑属性（如年龄、微笑程度、材质粗糙度）单独训练 LoRA 权重或 Adapter，通过插值这些专用权重来实现连续控制。这种方案存在两个根本局限：（1）每个新属性需要独立训练，无法泛化；（2）权重插值空间未必与编辑强度的感知变化线性对齐。

Kontinuous Kontext 通过**统一的强度投影器 + LoRA 适配**方案解决了这一问题。强度投影器以编辑指令的文本嵌入为条件，使其能够根据不同的编辑语义自适应地调节调制参数偏移量。这意味着**同一个投影器可以处理任意编辑指令的强度控制**，无需为每种属性单独训练。在 PIEbench 基准测试中，该方法在面部/风格化子集上以 $\delta_{\text{smooth}} = 0.098$ 显著优于 ConceptSliders（0.143），在材质子集上以 $\delta_{\text{smooth}} = 0.350$ 大幅优于 MARBLE（2.577）（Table 1b），验证了统一框架的有效性。

### 4. 创新总结

| 改变维度 | 基线方法 | Kontinuous Kontext |
|---------|---------|-------------------|
| 编辑强度控制 | 无；仅文本指令控制内容 | 标量 $s \in [0,1]$ 显式控制编辑程度 |
| 控制信息注入空间 | — | 调制空间（调制参数偏移量） |
| 强度-指令耦合 | — | 强度投影器以文本嵌入为条件，统一处理任意指令 |
| 训练添加模块 | 无额外模块 | 4层MLP投影器 + 秩-4 LoRA适配注意力投影矩阵 |
| 泛化能力 | 领域特定方法需每属性单独训练 | 单一模型覆盖所有编辑属性的连续控制 |

**需要手动验证的点**：论文未提供与 ConceptSliders、MARBLE 等基线方法的详细架构对比（如参数量、训练数据规模），建议在阅读完整论文时核实这些方法的实现细节，以确保公平性评估的准确性。



Kontinuous Kontext 的整体 pipeline 围绕一个核心目标展开：在指令驱动的图像编辑模型中引入**标量编辑强度**这一连续控制维度，使用户能够像调节“滑块”一样精细控制编辑的程度。整个框架分为两个关键阶段：**合成数据集构建**与**强度感知模型训练**。

### 数据生成流程

由于不存在天然的“不同强度编辑”配对数据，方法首先构建一个合成数据集。该流程包含三个步骤（Figure 3）：

![[assets/figures/papers/paper_list_l2320_https_arxiv_org_abs_2510_08532/figures/003_Figure_3.jpg]]
*Figure 3: Data generation. Our pipeline consists of three steps: (a) We generate an edit instruction for each source image using a pretrained VLM, then apply Flux Kontext, an instruction-driven editing model, to produce a full-strength edit. (b) We synthesize intermediate-strength edits using a diffusion-based morphing method [6], which inverts both the source and edited images into the diffusion latent space and interpolates their features. (c) To compensate for inconsistencies in the morphing sequence (Fig. 5), we filter the samples based on the inversion quality and uniformity of the sequence*

1. **全量编辑生成**：对于每张源图像，使用预训练的视觉语言模型（VLM）自动生成编辑指令，然后通过 Flux Kontext（一个基于 DiT 架构的指令驱动编辑模型）生成对应的全强度编辑结果（s=1）。
2. **中间强度合成**：利用基于扩散的特征空间插值方法 Freemorph，将源图像与全量编辑图像反演至扩散潜在空间，并在特征层进行插值，从而合成从 s=0 到 s=1 的 N+1 帧中间编辑序列。编辑强度定义为均匀离散集合 $\{s_i = i/N \mid i = 0, \ldots, N\}$。
3. **数据过滤**：由于 Freemorph 生成的中继帧可能存在物体残缺、突变跳跃或反演错误等不一致性（Figure 5），方法引入过滤机制。通过计算相邻帧间的 DreamSim 距离序列 $D = \{d_{0,1}, d_{1,2}, \dotsc, d_{N-1,N}\}$ 并进行均匀性检验，剔除低质量序列，确保训练数据具有平滑的编辑轨迹。

![[assets/figures/papers/paper_list_l2320_https_arxiv_org_abs_2510_08532/figures/005_Figure_5.jpg]]
*Figure 5: Generating intermediate images with Freemorph can introduce inconsistencies such as incomplete objects, abrupt jumps, or errors from diffusion inversion. We filter such cases to obtain a clean dataset with smooth trajectories*

### 模型架构与强度注入机制

模型构建于 Flux Kontext 之上，其核心创新在于**通过调制空间注入编辑强度信息**。

**调制空间分析**：初步实验表明（Figure 6a），直接用一个标量 v∈(0.5, 1.3) 缩放 Flux Kontext 中文本令牌的调制参数（modulation parameters），可以产生不同强度的编辑变化。然而，这种变化与用户期望的编辑强度并非线性对齐——缩放值与感知强度之间存在失配，说明调制空间天然编码了强度信息，但需要专门的校准机制将其转化为可解释的连续控制。

**强度投影器**：基于上述洞察，方法设计了一个轻量级的**强度投影器**（strength projector），将标量编辑强度 s 和编辑指令的池化 CLIP 文本嵌入共同映射为调制参数的偏移量（Δy_scale, Δy_shift）。这些偏移量被注入到 Flux Kontext 原有的文本令牌调制参数上，从而实现对编辑强度的校准控制（Figure 6b）。强度投影器是一个 4 层 MLP，与应用于注意力投影矩阵的秩-4 LoRA 适配器共同训练。

### 训练目标

模型采用标准的流匹配损失进行训练，其中引入标量编辑强度 s 作为额外条件：

$$\mathcal{L}_{\theta} = \mathbb{E}_{t \sim p(t), x, e, s, y_s} \left[ \| v_{\theta}(y_s^t, t, e, x, s) - (\epsilon - x) \|_2^2 \right]$$

训练时，基模型 Flux Kontext 的大部分参数保持冻结，仅更新强度投影器和 LoRA 适配器的参数。

### 输入输出流

- **输入**：源图像、编辑指令文本、标量编辑强度 s∈[0,1]
- **处理**：编辑指令经 CLIP 文本编码器提取池化嵌入，与强度标量 s 共同送入强度投影器；投影器输出调制参数偏移量，注入 Flux Kontext 的文本令牌调制空间；LoRA 适配器对注意力投影矩阵进行低秩调整以适配新的控制信号
- **输出**：对应指定强度的编辑图像

这种设计使得 Kontinuous Kontext 成为一个**统一的连续强度控制框架**，无需为每种编辑属性单独训练模型。用户只需调节标量 s，即可在同一条编辑指令下获得从无编辑到全编辑之间的平滑过渡。

### 补充图表

![[assets/figures/papers/paper_list_l2320_https_arxiv_org_abs_2510_08532/figures/001_Figure_1.jpg]]
*Figure 1: Kontinuous Kontext produces smooth edit trajectories across diverse attributes given an image, instruction, and an edit scalar strength. Unlike prior methods that require attribute-specific training, ours is a unified approach to enable fine-grained control*



### 关键模块设计

Kontinuous Kontext 的核心架构建立在 **Flux Kontext** 之上——一个基于扩散Transformer（DiT）的指令驱动图像编辑模型。为引入连续编辑强度控制，方法在基模型上增加两个轻量级模块：

- **强度投影器（Strength Projector）**：一个4层MLP网络，接收标量编辑强度 $s$ 和来自CLIP文本编码器的池化文本嵌入作为输入，输出调制参数的偏移量 $(\Delta y_{\text{scale}}, \Delta y_{\text{shift}})$。这些偏移量直接作用于文本令牌的调制参数，从而在调制空间中注入编辑强度信息。

- **LoRA适配层**：对Flux Kontext的注意力投影矩阵施加秩-4的低秩适配（LoRA），与强度投影器共同训练，使基模型能适应强度条件信号的引入。

架构设计的核心洞察来自一个简单实验：直接用标量 $v \in (0.5, 1.3)$ 缩放文本令牌的调制参数可以产生不同强度的编辑效果，但变化与强度并非线性对齐（Fig. 6a, Fig. 14）。这表明调制空间天然编码了编辑强度信息，但需要专门的校准模块将用户可解释的强度值映射为精确的调制参数偏移。

![[assets/figures/papers/paper_list_l2320_https_arxiv_org_abs_2510_08532/figures/016_Figure_14.jpg]]
*Figure 14: Inference time control in modulation space. We conducted a simple experiment by scaling the text modulation parameters with values of*

### 关键公式

**流匹配损失（Flow Matching Loss）**

模型训练使用标准的流匹配损失，引入标量编辑强度 $s$ 作为条件：

$$\mathcal{L}_{\theta} = \mathbb{E}_{t \sim p(t), x, e, s, y_s} \left[ \| v_{\theta}(y_s^t, t, e, x, s) - (\epsilon - x) \|_2^2 \right]$$

其中：
- $t$：扩散时间步，服从分布 $p(t)$
- $x$：源图像
- $e$：编辑指令的文本嵌入
- $s$：标量编辑强度，$s \in [0, 1]$
- $y_s^t$：在时间步 $t$ 加噪后的目标编辑图像
- $v_{\theta}$：参数为 $\theta$ 的速度场预测网络
- $\epsilon - x$：流匹配的目标速度（从噪声 $\epsilon$ 指向源图像 $x$）

该损失函数使模型学会根据不同的强度标量 $s$ 预测相应的编辑方向，从而实现连续强度控制。

**编辑强度离散化**

在数据生成阶段，编辑强度被离散化为均匀间隔的 $N+1$ 个值：

$$\{ s_i = i / N \mid i = 0, \ldots, N \}$$

其中 $s_0 = 0$ 对应源图像（无编辑），$s_N = 1$ 对应完整编辑。相邻强度间图像的距离序列定义为：

$$D = \{ d_{0,1}, d_{1,2}, \dotsc, d_{N-1,N} \}$$

该序列用于后续的数据过滤，确保合成轨迹的平滑性。

**平滑度度量（二阶三角形赤字）**

评估编辑轨迹平滑度的核心指标为二阶三角形赤字：

$$\delta_{\text{smooth}} = \delta^{2}(\text{DreamSim}) = \max_{i} \frac{\Delta_i}{d(y_{s_i}, y_{s_{i+2}})}$$

其中 $\Delta_i$ 为相邻三帧间的三角形赤字，$d(\cdot, \cdot)$ 为DreamSim感知距离。该度量捕捉编辑序列的二阶一致性：值越小表示相邻编辑间的过渡越平滑。用户研究验证了该度量与人类对平滑度的偏好高度一致（Fig. 15）。

**CLIP方向相似度聚合**

评估指令跟随能力的指标为所有编辑强度下CLIP方向相似度的加权平均：

$$D_{\text{clip-dir}} = \frac{\sum_{i=0}^{N} (d_i / s_i)}{N}$$

其中 $d_i$ 为在强度 $s_i$ 处编辑方向与文本指令方向的CLIP空间余弦相似度。该指标衡量编辑过程是否始终沿着指令指定的语义方向推进。

### 补充图表

![[assets/figures/papers/paper_list_l2320_https_arxiv_org_abs_2510_08532/figures/006_Figure_6.jpg]]
*Figure 6: Model architecture. (a) In a simple experiment, we scale the text-token modulation parameters in Flux Kontext with a scalar to generate edit variations. This perturbation produces edits of varying strengths, revealing that modulation parameters can govern edit strength. (b) Building on this insight, we design a lightweight projector network that maps a scalar edit strength s to offsets of the text modulation parameters, enabling precise control over edit strength*

![[assets/figures/papers/paper_list_l2320_https_arxiv_org_abs_2510_08532/figures/007_Figure_7.jpg]]
*Figure 7: Adding text embeddings into the slider projector improves smoothness of edit transitions*



## 实验与关键发现

### 核心实验设置

我们基于 **PIEbench** 基准进行评估。该基准原本包含多种编辑类别，我们排除了“添加/移除物体”这类本质上离散的编辑任务，最终保留 540 张图像用于测试。评价体系围绕两个核心维度构建：

- **编辑平滑度（δ_smooth）**：采用基于 DreamSim 距离的二阶三角形赤字度量。该指标衡量相邻三帧编辑结果之间的局部一致性——值越小，表示编辑过渡越平滑、无突变。用户研究（Figure 15）证实，该二阶度量与人类对平滑度的偏好高度对齐，优于一阶距离度量。
- **指令跟随度（CLIP-Dir）**：在所有编辑强度下计算 CLIP 方向相似度的加权平均，评估编辑轨迹与文本指令的整体对齐程度。

![[assets/figures/papers/paper_list_l2320_https_arxiv_org_abs_2510_08532/figures/017_Figure_15.jpg]]
*Figure 15: We performed one user study where we compute the alignment of the users scores given for smoothness of the sequence with the different variations of smoothness metrics. We found*

训练数据通过合成管线生成：首先用 VLM 为源图像生成编辑指令，由 Flux Kontext 产生完整强度编辑，再借助 Freemorph 在扩散潜空间中进行特征插值以生成中间强度样本，最后经过反转质量与序列均匀性过滤，剔除不一致的编辑序列。

### 主实验结果

#### 与编辑后插值基线的比较

我们将 Kontinuous Kontext 与三类编辑后插值方法进行对比：基于 LoRA 权重插值的 **Diffmorpher**、基于扩散特征空间插值的 **Freemorph**，以及将编辑视为视频帧插值任务的 **WAN-Video**。这些基线均先生成完整强度编辑，再通过各自机制产生中间强度结果。

**Table 1a** 展示了定量对比。在编辑平滑度上，我们的方法取得了最优的 δ_smooth = 0.329，显著优于 Diffmorpher（0.371）和 Freemorph（0.365），而对 WAN-Video（0.853）的优势更为明显（降低 0.524）。这表明扩散特征空间或权重空间的线性插值无法保证编辑的平滑过渡，而我们的调制空间注入策略从根本上解决了这一问题。

在指令跟随度上，我们取得了 CLIP-Dir = 0.241，优于 Diffmorpher（0.181）和 Freemorph（0.189），但略低于 WAN-Video（0.269）。WAN-Video 作为视频模型虽然能产生更平滑的视觉过渡，但其编辑轨迹可能偏离原始指令的语义方向。我们的方法在平滑度与指令对齐之间取得了更好的平衡。

#### 与领域特定方法的比较

我们进一步与需要为每种编辑属性单独训练的领域特定方法对比。**Table 1b** 展示了分领域结果：

- 在人脸/风格化编辑子集上，我们的统一方法取得了 δ_smooth = 0.098，优于 **ConceptSliders** 的 0.143；CLIP-Dir 达到 0.382，几乎是 ConceptSliders（0.186）的两倍。ConceptSliders 虽然支持连续控制，但需要为每个属性训练独立的 LoRA 权重，且编辑方向容易偏离指令意图。
- 在材质编辑子集上，我们的方法取得 δ_smooth = 0.350，远优于 **MARBLE** 的 2.577，但在 CLIP-Dir 上略低（0.101 vs. 0.157）。MARBLE 作为材质编辑专用方法，在指令对齐上具有领域优势，但其编辑轨迹存在严重的突变问题。

**Figure 9** 的视觉对比直观展示了这些差异：我们的方法在保持身份一致性的同时，实现了平滑的编辑过渡；而插值方法常出现中间帧的身份漂移，领域特定方法则在强度变化时产生跳变。

### 消融研究：调制空间注入的因果验证

**Table 2** 和 **Figure 18** 展示了架构消融结果，系统验证了调制空间注入策略的有效性。

#### 注入空间的选择：调制空间 vs. 文本空间

我们将强度投影器的输出作为额外的文本令牌注入（text-space condn），即让标量强度信息通过文本交叉注意力影响编辑过程。该变体取得了极差的 δ_smooth = 1.468（完整方案为 0.329），表明文本空间不是平滑的强度控制空间。原因在于，文本令牌的语义空间具有离散性——微小的嵌入偏移可能导致注意力分布的突变，进而产生编辑跳变。调制空间则直接控制特征缩放与偏移，天然支持连续变化。

#### 文本嵌入条件的必要性

移除强度投影器中的池化文本嵌入输入（w/o text projector），使投影器仅依据标量强度 s 产生固定的调制偏移。该变体的 δ_smooth 恶化至 1.092，CLIP-dir 降至 0.141。这说明编辑指令的语义信息对于校准强度控制至关重要：相同的强度标量对于“微笑”和“变成油画风格”需要完全不同的调制偏移幅度。文本嵌入条件使投影器能够学习指令语义与调制参数偏移之间的映射关系。

#### 数据过滤的影响

去除数据过滤步骤（w/o filtering）后，δ_smooth 从 0.329 升至 0.483，CLIP-dir 从 0.241 降至 0.228。合成数据中的噪音序列（反转失败、中间帧不一致）会误导模型学习错误的强度-编辑映射，验证了基于反转质量和序列均匀性过滤的必要性。

#### 完整方案的因果链路

完整方案（Ours）在调制空间中注入强度信息，并通过文本嵌入条件化的投影器产生校准的调制偏移，同时辅以 LoRA 适配注意力投影矩阵。这一设计实现了最佳的 δ_smooth = 0.329 和 CLIP-dir = 0.241，验证了“调制空间编码强度 + 投影器校准映射”这一核心洞察的正确性。

### 推理时基线的局限性

**Table 3** 对比了两种无需训练的推理时控制策略：调整分类器自由引导尺度（CFG-scale）和调整交叉注意力权重（Attention reweighting）。这两种方法虽然可以改变编辑程度，但完全无法实现平滑控制——δ_smooth 分别高达 152.205 和 120.760。这是因为 CFG 尺度和注意力权重对编辑的影响是非线性和非单调的，无法建立与用户期望强度的稳定映射。

### 用户研究

**Figure 10** 显示了成对比较的用户研究结果。我们的方法在编辑平滑度、图像保真度和指令跟随三个维度上均显著优于所有基线。用户对平滑度的偏好与 δ_smooth 度量高度一致，进一步验证了该自动指标的有效性。

### 失败模式分析

#### 外推编辑强度（s > 1）

如 **Figure 24** 所示，当编辑强度超出训练分布（s > 1）时，模型无法产生额外的编辑效果。在大多数情况下，模型要么重复 s = 1 时的完整编辑结果，要么反而减少编辑程度。这是因为训练数据中强度始终在 [0, 1] 范围内，投影器未学习到外推所需的调制偏移映射。这一限制源于数据驱动的学习范式本身，而非架构缺陷。

#### 离散编辑的不适用性

对于本质上离散的编辑任务（如插入或移除物体），不存在自然的连续过渡空间，因此本方法不适用。这一限制在实验设计阶段即被排除（PIEbench 中移除了 add/remove 类别）。

#### 基模型几何能力的继承

Kontinuous Kontext 继承了 Flux Kontext 在精确几何操作上的弱点，例如无法实现准确的物体旋转或平移。尽管 **Figure 8** 展示了在“熊猫变哈士奇”等几何变换上的连续控制能力，但编辑的几何精度仍受限于基模型本身的能力边界。

### 补充图表

![[assets/figures/papers/paper_list_l2320_https_arxiv_org_abs_2510_08532/figures/010_Figure_9.jpg]]
*Figure 9: Visual Comparison. We evaluate against (a) image interpolation methods, where we first generate a full strength edit with Flux-Kontext and interpolate to obtain intermediate edits, and (b) domain-specific methods, which train separate LoRAs/Adapters for each attribute. Our generalized method achieves superior slider control with consistent image identity and smooth edit transitions*

![[assets/figures/papers/paper_list_l2320_https_arxiv_org_abs_2510_08532/figures/011_Table_2.jpg]]
*Table 2: Ablation studies*

![[assets/figures/papers/paper_list_l2320_https_arxiv_org_abs_2510_08532/figures/012_Figure_10.jpg]]
*Figure 10: User study win-rates (%) of our method against baselines in pairwise comparisons*

![[assets/figures/papers/paper_list_l2320_https_arxiv_org_abs_2510_08532/figures/021_Figure_18.jpg]]
*Figure 18: Ablation over architecture of Kontinuous Kontext*

![[assets/figures/papers/paper_list_l2320_https_arxiv_org_abs_2510_08532/figures/009_Table_1.jpg]]
*Table 1: Baseline comparison*



## 定位与知识库关联

### 任务定位：指令驱动图像编辑的连续控制维度

本文解决的问题处于**指令驱动图像编辑**与**连续属性控制**的交叉地带。传统指令驱动编辑模型（如本文所基于的 **Flux Kontext**）仅接受“图像+文本指令”作为输入，输出一个确定的编辑结果，缺乏对编辑程度的精细调节能力。另一方面，连续属性控制方法（如 **ConceptSliders**、**MARBLE**）虽然能实现平滑的编辑强度调节，但需要为每一种编辑属性单独训练适配器或 LoRA 权重，不具备跨属性的统一性。Kontinuous Kontext 在这两个方向之间开辟了一个新定位：**通过统一的标量强度输入，实现对任意文本指令编辑的连续强度控制**，无需为每种编辑属性重复训练。

### 基线方法谱系

论文将现有方法划分为两条技术路线，并在定量和定性实验中进行了系统对比：

**路线一：编辑后插值方法。** 这类方法先用指令模型生成完整编辑（强度 s=1），再通过插值技术生成中间状态，属于“事后”方案。
- **Diffmorpher**：基于 LoRA 权重插值，在源模型和编辑模型之间进行参数融合产生中间编辑。
- **Freemorph**：基于扩散特征空间的插值，将源图和编辑图反演至扩散潜空间后进行特征插值。
- **WAN-Video (WAN-2.1)**：将编辑任务视为视频帧插值问题，利用视频生成模型在源图与编辑图之间生成过渡帧。

**路线二：领域特定连续控制方法。** 这类方法为特定编辑属性设计专用控制机制，属于“事前”方案。
- **ConceptSliders**：通过 LoRA 权重插值实现对特定概念的连续属性控制（如年龄、表情），但每个属性需单独训练 LoRA。
- **MARBLE**：专注于材料属性的连续编辑控制，通过专用适配器调节材质参数（如金属度、粗糙度）。

此外，论文还考察了两种**推理时基线**：
- **CFG-scale baseline**：通过调整分类器自由引导尺度来改变编辑程度。
- **Attention reweighting baseline**：通过调整交叉注意力权重来影响编辑强度。

### 核心技术决策与差异化

Kontinuous Kontext 的核心技术决策可归纳为“**在调制空间而非文本空间注入强度控制**”，这一选择直接决定了其相对于基线的优势：

| 设计维度 | 编辑后插值方法 | 领域特定方法 | Kontinuous Kontext |
|---------|-------------|------------|-------------------|
| 控制时机 | 事后（编辑后再插值） | 事前（训练时注入） | 事前（训练时注入） |
| 控制空间 | 图像/特征空间 | LoRA权重空间 | 调制参数空间 |
| 属性泛化性 | 通用（但质量依赖插值） | 单一属性 | 通用（统一标量控制） |
| 训练开销 | 无需训练 | 每属性单独训练 | 一次训练，跨属性泛化 |

关键洞察在于：论文通过初步实验发现，直接缩放 Flux Kontext 中文本令牌的调制参数（v∈0.5~1.3）确实能产生不同强度的编辑（Fig. 6a, Fig. 14），但变化与用户期望的强度并非线性对齐，表明**调制空间天然编码了编辑强度信息，但需要校准**。基于此，论文设计了轻量级的强度投影器（Strength Projector），将标量强度 s 与池化 CLIP 文本嵌入共同映射为调制参数的偏移量（Δy_scale, Δy_shift），在原有调制参数上叠加，实现了校准后的连续控制。

### 适用边界与局限

**适用场景：**
- 存在自然连续过渡的编辑属性：如风格化程度、颜色变化、年龄调整、表情强度、材料属性变化等。
- 需要统一控制接口的多属性编辑场景：单一模型即可覆盖多样化编辑指令的强度调节。
- 对编辑平滑度有较高要求的应用：如交互式图像编辑工具中的滑块控制。

**已知局限（论文明确指出的失败模式）：**

1. **离散编辑不适用。** 对于本质上不存在连续过渡的编辑类型，如物体的插入或移除，该方法缺乏自然的强度定义，无法产生有意义的中间状态。

2. **继承基模型的几何编辑弱点。** 由于建立在 Flux Kontext 之上，该方法继承了基模型在精确几何操作上的不足，如准确的物体旋转、平移等操作难以实现平滑的连续控制。

3. **编辑强度外推失败。** 当输入强度 s>1（即要求超出训练分布的最大编辑程度）时，模型无法产生一致的额外编辑效果。论文明确报告（Fig. 24）：在大多数外推情况下，模型要么重复 s=1 的完整编辑结果，要么反而减少编辑程度，表明投影器学到的是 [0,1] 区间内的插值映射，而非可外推的编辑方向。

4. **合成数据集的固有噪音。** 训练数据依赖 Freemorph 生成的中间强度编辑序列，尽管经过均匀性过滤，仍可能包含插值伪影或不一致的编辑轨迹，影响训练监督质量。

### 开放问题与后续方向

1. **编辑强度的外推控制。** 如何使模型在 s>1 时产生超出训练分布的更强编辑效果？这可能需要探索调制空间中的方向性编辑向量，而非仅在 [0,1] 区间内插值。

2. **多维连续控制。** 调制空间是否可支持更多维度的连续控制？例如，引入空间变化的强度场（图像不同区域不同编辑强度）或时间维度的强度曲线，将单一标量扩展为更丰富的控制信号。

3. **视频编辑的扩展。** 如何将该方法扩展到基于视频的连续编辑，实现时序一致的编辑强度调节？这涉及调制参数在时间维度上的平滑传播。

4. **复杂几何变换的连续控制。** 如何提升模型对几何编辑（如姿态变化、视角转换、结构变形）的连续控制能力？当前方法在几何编辑上的平滑度仍有限，可能需要更专门的几何表示或约束。

5. **与推理时控制方法的融合。** 论文中的 CFG-scale 和 attention reweighting 基线虽然平滑度极差（δ_smooth 分别为 152.205 和 120.760，Table 3），但它们在特定场景下可能提供互补的控制维度，如何将训练时的调制空间控制与推理时的引导机制有机融合值得探索。

### 知识库定位总结

Kontinuous Kontext 在方法谱系中的核心贡献是**发现了调制空间作为连续编辑强度控制接口的潜力**，并通过轻量级投影器实现了校准后的统一控制。它既避免了编辑后插值方法的身份不一致和突变问题（δ_smooth 从 0.371 降至 0.329，Table 1a），又克服了领域特定方法需要为每个属性单独训练的局限性。该方法为指令驱动图像编辑引入了一个新的连续控制维度，其“调制空间注入”的设计范式可能对更广泛的生成模型可控性研究具有启发意义。



## 原文 PDF

![[paperPDFs/CVPR_2026/Kontinuous_Kontext_Continuous_Strength_Control_for_Instruction_based_Image_Editing.pdf]]
