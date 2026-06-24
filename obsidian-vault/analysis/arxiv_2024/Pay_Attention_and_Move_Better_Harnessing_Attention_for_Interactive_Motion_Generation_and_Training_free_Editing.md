---
title: "Pay Attention and Move Better: Harnessing Attention for Interactive Motion Generation and Training-free Editing"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/Pay_Attention_and_Move_Better_Harnessing_Attention_for_Interactive_Motion_Generation_and_Training_free_Editing.pdf
aliases:
- PAMBHAIMGTFE
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过显式建模交叉注意力中的词级对应关系和自注意力中的帧间相似性，并直接操纵注意力图，可实现各种训练无关的编辑任务。
primary_logic: 交叉注意力图决定了动作执行的时间与语义位置，自注意力图捕捉运动帧之间的相似性模式；通过调整交叉注意力权重可控制动作强调/去强调或替换，通过操纵自注意力图可改变运动序列顺序或转移风格。
claims:
- 交叉注意力图在动作执行时高度激活对应的词（如“jump”），验证了词级对应关系。
- 自注意力图突出显示相似运动模式区域，反映重复或相似的子动作。
- 通过替换交叉注意力图可在原位替换动作，同时保留未编辑部分。
- 分离的词级交叉注意力建模显著提升了文本-运动对齐和细粒度控制。
---

# Pay Attention and Move Better: Harnessing Attention for Interactive Motion Generation and Training-free Editing

> [!tip] 核心洞察
> 交叉注意力图决定了动作执行的时间与语义位置，自注意力图捕捉运动帧之间的相似性模式；通过调整交叉注意力权重可控制动作强调/去强调或替换，通过操纵自注意力图可改变运动序列顺序或转移风格。

| 字段 | 内容 |
|------|------|
| 中文题名 | 关注并移动更好：利用注意力机制进行交互式运动生成与免训练编辑 |
| 英文题名 | Pay Attention and Move Better: Harnessing Attention for Interactive Motion Generation and Training-free Editing |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2410.18977) · [Project](https://lhchen.top/MotionCLR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MotionCLR |
| Dataset | HumanML3D, HVerb / HVerb-wild, Example-based motion generation |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top1 0.544 (MotionCLR*) vs 0.491 (MotionDiffuse) (+0.053)；FID 0.269 (MotionCLR*) vs 0.544 (MDM) (-0.275)。
> - HVerb / HVerb-wild 上，in-place replacement unedited part preserving (MPJPE, mm) 57.9 (HVerb) / 59.8 (HVerb-wild) vs 75.3 (MotionFix-C) / 120.2 (MotionFix-R) (~ -17.4 (HVerb) / -60.4 (HVerb-wild))。
> - Example-based motion generation 上，FID 0.427 vs 0.461 (Diffusion manipulation) (-0.034)。

## 概述

文本驱动的三维人体运动生成旨在从自然语言描述中合成逼真且多样化的动作序列。现有运动扩散模型通常将文本条件压缩为单一全局嵌入，缺乏对词级文本-运动对应关系的显式建模。这一瓶颈导致模型无法进行细粒度的交互式编辑——用户难以精确控制“何时、何处、以何种强度”执行特定动作。

**MotionCLR** 针对上述问题，提出了一种基于注意力机制可解释性与可操纵性的统一框架。其核心洞察在于：**(1) 交叉注意力图决定了动作执行的时间与语义位置**，词级激活模式天然编码了文本-运动的细粒度对应关系；**(2) 自注意力图捕捉运动帧之间的相似性模式**，反映了重复子动作和序列结构。基于这两类注意力图，MotionCLR 将运动生成与编辑统一为注意力图的生成与操纵问题，无需额外训练即可实现多种编辑任务。

在方法定位上，MotionCLR 区别于 **MDM**（Tevet et al., 2022b）等将文本作为单一令牌注入的范式，也不同于 **MotionDiffuse**（Zhang et al., 2024a）将时间步与文本条件混合的做法。其核心架构改动包括：分离的词级交叉注意力模块（不含时间步混合）、独立的时间步注入卷积模块，以及仅作用于运动特征的自注意力设计。这一设计使得注意力图天然具备可解释性，为后续免训练编辑提供了基础。

实验表明，MotionCLR 在 HumanML3D 基准上取得了有竞争力的生成性能（FID 0.269，R-Precision Top1 0.544），同时支持原位动作替换（HVerb 测试集上未编辑部分 MPJPE 57.9mm，显著优于 MotionFix 的 75.3mm）、动作强调/减弱、运动序列移位、风格迁移和基于样例的运动生成等多种编辑任务。消融实验证实，分离的词级交叉注意力是性能提升的关键——移除后 R-Precision Top1 从 0.544 降至 0.512，FID 从 0.269 升至 0.380。

**局限与展望：** 当前方法在处理生成模型幻觉方面仍然有限，动作计数在复杂序列中仍可能出错，编辑效果在极端权重调整下可能引入运动伪影。未来工作可探索将该范式扩展到语言对话式交互的运动生成，以及增强模型对生成幻觉的鲁棒性。

## 背景与动机

### 文本驱动运动生成的进展与瓶颈

文本驱动的人体运动生成旨在从自然语言描述中合成逼真的三维运动序列。近年来，扩散模型在该领域取得了显著进展，涌现出 **MDM**（Tevet et al., 2022b）、**MLD**（Chen et al., 2023）、**MotionDiffuse**（Zhang et al., 2024a）等一系列方法。这些方法通常将文本条件作为全局嵌入注入去噪过程，能够生成整体语义一致的运动。

然而，现有方法存在一个根本性瓶颈：**缺乏词级文本-运动对应关系的显式建模**。具体而言，文本条件通常被融合为单一特征向量，导致模型无法建立“具体词汇”与“具体运动帧”之间的细粒度关联。这一缺失直接限制了运动生成的交互性与可编辑性——用户无法精确指定“何时做出何种动作”，也无法对已生成的运动进行局部语义修改。

### 交互式运动编辑的需求与挑战

从应用角度看，角色动画、游戏开发和虚拟现实等场景对交互式运动编辑提出了强烈需求。用户期望能够：

- **原位替换动作**：将运动序列中的特定动作替换为另一动作，同时保留未编辑部分的时间位置和运动内容。
- **调整动作强度**：增强或减弱某个动作的表现幅度（如跳跃高度）。
- **改变动作顺序**：重新排列运动序列中不同子动作的先后次序。
- **迁移运动风格**：将一段运动的风格特征迁移到另一段运动上。

现有编辑方法如 **MotionFix**（Athanasiou et al., 2024）和 **MEOs**（Goel et al., 2024）依赖语言指令或额外训练，难以实现上述细粒度的免训练编辑。核心挑战在于：**如何在不需要额外训练的前提下，实现对运动序列中特定语义单元的精确定位与操纵**。

### 注意力机制的潜在能力

本文的核心洞察来源于对扩散模型中注意力机制的实证分析。如图 3 所示，在生成“a person jumps”运动时：

- **交叉注意力图**在动作执行时刻高度激活对应词汇“jump”，表明交叉注意力天然编码了词级文本-运动对应关系。
- **自注意力图**突出显示具有相似运动模式的帧区域，反映出重复或相似的子动作结构（如三次跳跃动作形成九个相似区域）。

这一发现揭示了注意力图的两个关键性质：**交叉注意力图决定了动作执行的时间位置与语义归属，自注意力图捕捉运动帧之间的时序相似性模式**。基于此，直接操纵注意力图即可实现多种训练无关的编辑任务——通过调整交叉注意力权重控制动作强调/去强调或替换，通过操纵自注意力图改变运动序列顺序或转移风格。

### 本文动机与贡献

基于上述分析，本文提出 **MotionCLR**，旨在通过显式建模词级交叉注意力和帧间自注意力，构建一个同时支持高质量运动生成与灵活免训练编辑的统一框架。核心动机在于：**将注意力机制从隐式的模型内部组件升级为显式的可控接口，使运动生成与编辑共享同一套注意力表示，从而实现交互式的、训练无关的运动操纵**。

## 核心创新

MotionCLR 的核心创新在于**显式建模词级文本-运动对应关系**，并由此衍生出一套**免训练的注意力图编辑范式**。与现有运动扩散模型将文本条件压缩为单一全局 token 或混合注入时间步的做法不同，MotionCLR 在架构层面进行了三项关键解耦（changed slots），从而实现了细粒度的语义控制。

### 1. 词级交叉注意力：从全局文本到逐词对应

现有方法（如 MDM，Tevet et al., 2022b）通常将文本嵌入融合为单个全局特征，导致模型无法区分不同词汇对运动的具体贡献。MotionCLR 的交叉注意力层以运动帧特征为 Query（$\mathbf{Q} = \mathbf{X} \mathbf{W}_Q$），以词级文本嵌入为 Key 和 Value（$\mathbf{K} = \mathbf{C} \mathbf{W}_K, \mathbf{V} = \mathbf{C} \mathbf{W}_V$），通过标准缩放点积注意力（$\mathbf{X}' = \mathsf{softmax}(\mathbf{QK}^{\top} / \sqrt{d}) \mathbf{V}$）计算每一帧与每个词之间的相似度。

这一设计的因果机制在于：**交叉注意力图决定了动作执行的时间与语义位置**。实证研究表明，在运动“跳跃”执行期间，交叉注意力图中词“jump”的激活显著增强（Fig. 3(B)），验证了词级对应关系的形成。消融实验进一步证实，移除分离的词级交叉注意力后，R-Precision Top1 从 0.544 降至 0.512，FID 从 0.269 升至 0.380（Table 7），说明该设计对文本-运动对齐质量具有决定性影响。

### 2. 时间步注入解耦：分离条件信号

在 MDM 等基线中，时间步嵌入常与文本特征混合后一同注入网络，导致两种条件信号相互干扰。MotionCLR 将时间步注入独立为专用的 Conv1d 模块，与文本条件注入完全解耦（Fig. 2(b)）。这一分离使得文本-运动交叉注意力能够专注于语义对应，而不受扩散时间步噪声的污染，为后续的注意力图操纵提供了干净的语义空间。

### 3. 自注意力纯化：仅建模帧间关系

传统方法将文本与运动 token 混合后送入自注意力，模糊了运动帧之间的内在相似性。MotionCLR 的自注意力仅以运动特征作为输入（$\mathbf{Q} = \mathbf{X} \mathbf{W}_Q, \mathbf{K} = \mathbf{X} \mathbf{W}_K, \mathbf{V} = \mathbf{X} \mathbf{W}_V$），纯粹建模帧间的时间相干性。这一设计使得自注意力图能够清晰反映相似运动模式的区域——例如，三次“跳跃”动作在自注意力图中对应九个高亮区域（Fig. 3(C)），为后续的序列移位和风格迁移编辑提供了可靠的基础。

### 4. 免训练编辑范式的统一基础

上述三项架构解耦共同构成了注意力图编辑的因果基础。由于交叉注意力图精确编码了词级语义的时间定位，**替换交叉注意力图**即可在原位将动作 A 替换为动作 B，同时保留未编辑部分的完整性（HVerb 上 MPJPE 仅 57.9 mm，较 MotionFix-C 的 75.3 mm 降低 17.4 mm）。通过缩放交叉注意力权重（$\mathbf{A}_{:,i} \times (1 + \alpha)$）可实现动作的**连续强度控制**（强调/去强调）。而纯化的自注意力图则支持**序列移位**和**风格迁移**——通过沿时间轴移动自注意力图来改变动作顺序，或通过混合不同运动的自注意力图来转移运动风格。所有编辑操作均无需额外训练，仅通过操纵预训练模型内部的注意力图即可完成。

## 整体框架

MotionCLR 的整体架构围绕一个类 U‑Net 的去噪网络构建，其核心原子单元为 **CLR 块（CLR Block）**。如 Figure 2(a) 所示，网络由多个下采样和上采样块堆叠而成，每个采样块包含两个 CLR 块，并在其前后分别执行下采样或上采样操作。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2410_18977/figures/002_Figure_2.jpg]]
*Figure 2: System overview of MotionCLR architecture. (a) The U-Net-like denoising network is with two CLR blocks before down/up-sampling. (b) The basic CLR block includes four layers, separating the timestep injection and the text condition. (c) The key component is the text-motion cross-attention at the word level*

### CLR 块的内部结构

每个 CLR 块由四个功能解耦的模块依次构成（Figure 2(b)）：

1. **Conv1d 模块**：专门负责时间步注入（timestep injection），将扩散时间步信息以独立通道融入运动特征，与文本条件完全解耦。
2. **自注意力模块（Self‑Attention）**：仅以运动帧特征作为输入，建模帧与帧之间的时间相干性，捕捉运动序列内部的相似性模式。
3. **交叉注意力模块（Cross‑Attention）**：以运动特征为查询（Query），以词级文本嵌入为键（Key）和值（Value），在词粒度上显式建模文本‑运动对应关系。
4. **前馈网络（FFN）**：对融合后的特征进行非线性变换，增强表示能力。

### 关键设计决策

与现有运动扩散模型的架构相比，MotionCLR 做出了三项关键改变：

- **分离的词级交叉注意力**：将文本条件从传统方法中与时间步混合或压缩为单一令牌的方式，改为对每个词独立建模的交叉注意力机制。这使模型能够学习到细粒度的“哪个词在何时激活”的对应关系，是后续免训练编辑能力的基础。
- **独立的时间步注入通道**：时间步信息通过专用的 Conv1d 模块注入，而非与文本特征混合，避免了两种条件信号之间的干扰。
- **纯运动自注意力**：自注意力模块的输入仅为运动特征，不包含任何文本信息，确保自注意力图纯粹反映运动帧之间的时序相似性，为后续基于自注意力图的操作（如序列移位、风格迁移）提供了干净的信号源。

### 信息流与输入输出

整体信息流如下：
1. 输入为带噪声的运动序列和描述文本。
2. 文本通过 CLIP‑ViT‑B 编码器转换为词级嵌入。
3. 运动序列与文本嵌入一同进入 U‑Net 网络，在每个 CLR 块中依次经过时间步注入、自注意力建模帧间关系、交叉注意力建模词‑帧对应、FFN 变换。
4. 网络输出预测的噪声，通过迭代去噪最终生成干净的运动序列。

这种模块化解耦设计使得交叉注意力图和自注意力图具有明确的语义含义：交叉注意力图决定了“哪个动作在何时执行”，自注意力图反映了“哪些帧的运动模式相似”。正是基于这两种注意力图的显式可解释性，MotionCLR 实现了无需额外训练的动作替换、强调/减弱、序列移位、风格迁移等多种交互式编辑功能。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2410_18977/figures/058_Figure_30.jpg]]
*Figure 30: The illustration of motion style transfer process. (a) Direct generating style reference: The style information is generated directly using the query (Q), key (K), and value (V) from the style reference motion sequence (blue). (b) Direct generating content reference: The content information is generated directly from the content reference motion sequence (orange). (c) Generating transferred result: The final transferred motion sequence combines the style from the style reference sequence with the content from the content reference sequence, using Q from the style reference (blue) and K, V from the content reference (orange)*

## 核心模块与公式推导

### 3.1 CLR 基础模块

MotionCLR 采用 U-Net 风格的扩散去噪骨干，其核心原子单元为 **CLR 模块**（CLR Block）。如图 2(b) 所示，每个 CLR 模块由四个子层组成，设计上将时间步注入与文本条件注入完全解耦：

1.  **Conv1d 层**：独立负责时间步 `t` 的注入，不再与文本特征混合。这改变了 MDM 等基线中将时间步与文本嵌入融合为单一代币的做法，使得后续的文本-运动交互不再受时间噪声干扰。
2.  **自注意力层**：仅以运动特征 `X` 作为输入，建模帧间的时间连贯性。与部分基线混合文本和运动代币进行自注意力的设计不同，MotionCLR 的自注意力**不包含任何文本输入**，从而纯粹捕捉运动帧之间的相似性模式。
3.  **交叉注意力层**：这是实现细粒度控制的关键。它以运动特征为查询（Query），以**词级别**的文本嵌入 `C` 为键（Key）和值（Value），显式建模每个词与每帧运动之间的对应关系。这直接回应了现有方法缺乏词级文本-运动对应关系建模的瓶颈。
4.  **FFN 层**：标准的前馈变换模块。

### 3.2 核心注意力公式

MotionCLR 中自注意力和交叉注意力的数学形式均基于缩放点积注意力（Scaled Dot-Product Attention），其通用输出为：

$$
\mathbf{X}' = \mathsf{softmax}\left(\frac{\mathbf{QK}^{\top}}{\sqrt{d}}\right) \mathbf{V}
$$

其中 `d` 为嵌入维度，`Q`、`K`、`V` 分别为查询、键、值矩阵。两种注意力的关键区别在于投影的来源不同：

**自注意力**
自注意力旨在衡量运动帧之间的相似性，并选出最相似的帧特征。其查询、键、值均来自运动特征 `X` 的线性投影：

$$
\mathbf{Q} = \mathbf{X} \mathbf{W}_Q, \quad \mathbf{K} = \mathbf{X} \mathbf{W}_K, \quad \mathbf{V} = \mathbf{X} \mathbf{W}_V
$$

**交叉注意力**
交叉注意力负责决定在每一帧应激活哪个词，并将该词的语义特征放置到对应帧上。它以运动特征为查询，以词级文本嵌入 `C` 为键和值：

$$
\mathbf{Q} = \mathbf{X} \mathbf{W}_Q, \quad \mathbf{K} = \mathbf{C} \mathbf{W}_K, \quad \mathbf{V} = \mathbf{C} \mathbf{W}_V
$$

这一分离的词级建模是 MotionCLR 实现训练无关编辑的因果杠杆。图 3 的可视化实证表明：交叉注意力图在动作执行时显著激活对应词（如 “jump”），而自注意力图则突出显示相似运动模式的区域（如三次跳跃动作对应的九个高亮区块）。消融实验（Table 7）进一步验证，移除分离的词级交叉注意力后，R-Precision Top1 从 0.544 降至 0.512，FID 从 0.269 升至 0.380，证实了该模块对文本-运动对齐和生成质量的决定性作用。

### 3.3 编辑操作中的注意力操纵公式

基于上述注意力机制的可解释性，MotionCLR 通过直接操纵注意力图实现多种免训练编辑任务：

-   **动作强调与去强调**：通过缩放交叉注意力图中特定动词 `i` 的注意力值来控制动作强度。对于权重因子 `α`，`α > 0` 表示强调，`α < 0` 表示去强调：
    $$
    \mathbf{A}_{:,i} \leftarrow \mathbf{A}_{:,i} \times (1 + \alpha)
    $$
    需要注意的是，极端调整（如 `α ↑ 1.0`）可能引入运动伪影（Figure 17），此为当前方法的一个已知局限。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2410_18977/figures/026_Figure_17.jpg]]
*Figure 17: Additional visualization results for different (de-)emphasis weights. The self-attention maps show how varying the different weights (e.g., ↓ 0.05, ↓ 0.10, ↑ 0.33, and ↑ 1.00) affect the emphasis on motion*

-   **原位动作替换**：将编辑后运动的交叉注意力图直接替换为参考运动的交叉注意力图，利用值矩阵（文本特征）与替换后注意力图的乘法得到输出，从而在保留未编辑部分的同时完成动作替换。

-   **序列顺序移位**：通过沿时间轴平移自注意力图来调整运动序列的顺序，利用自注意力对帧间顺序的敏感性实现动作重排。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2410_18977/figures/003_Figure_3.jpg]]
*Figure 3: Empirical study of attention mechanisms. We use “a person jumps. 2 as an example. (A) Keyframes and the root trajectory of generated motion. The character jumps*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2410_18977/figures/004_Figure_4.jpg]]
*Figure 4: (c) Motion sequence shifting via shifting self-attention map. We adjust the sequence order of the motion sequence via shifting the attention map along the temporal axis. Figure 4: Diagram of motion editing via manipulating attention maps*

## 实验与分析

### 生成性能主结果

MotionCLR在HumanML3D基准上达到了与最先进方法可比的生成质量。如Table 1所示，采用DDIM采样的MotionCLR*在R-Precision Top-1上达到0.544，显著优于MotionDiffuse（0.491）；在FID上达到0.269，相比MDM（0.544）大幅降低。这表明，通过显式建模词级文本-运动对应关系，模型在文本-运动对齐和运动质量两个维度上均取得了有竞争力的表现。

值得注意的是，MotionCLR并非为追求极致生成指标而设计——其核心架构选择（分离的词级交叉注意力、独立的时间步注入、纯运动帧的自注意力）主要服务于后续的免训练编辑能力。在此前提下，生成性能仍能与专为生成优化的方法（如MoMask、ReMoDiffuse）持平或超越，验证了架构设计的合理性。

### 词级对应关系的定量验证

Table 2通过IoU指标量化了交叉注意力激活与运动执行之间的一致性。在HVerb测试集上，交叉注意力激活边界框（E1）与基于根轨迹速度的边界框之间的IoU达到74.3%；在更具挑战性的HVerb-wild测试集上为73.5%。E1、E2、E3三个设置之间的高度一致性表明，交叉注意力确实捕获了细粒度的词级文本-运动对应关系，而非偶然相关。

这一验证为后续基于注意力操纵的编辑方法提供了关键基础：编辑操作的有效性依赖于注意力图与运动语义之间的可靠映射。

### 免训练编辑任务评估

**原位动作替换（In-place Motion Replacement）** 的定量结果见Table 3。在HVerb测试集上，MotionCLR的未编辑部分MPJPE仅为57.9mm，显著低于MotionFix-C（75.3mm）和MotionFix-R（120.2mm）；在HVerb-wild上，MotionCLR（59.8mm）相比MotionFix-R（120.2mm）的优势更为突出。这表明通过替换交叉注意力图，模型能够在目标位置精确替换动作，同时最大限度地保留非编辑区域的运动内容。

**基于示例的运动生成（Example-based Motion Generation）** 通过操纵自注意力图实现。如Table 5所示，MotionCLR在自注意力空间中进行编辑的FID（0.427）优于在每个扩散步直接编辑运动空间的方法（0.461），同时保持了更高的多样性。这验证了自注意力图捕获帧间相似性模式的有效性——通过替换自注意力图可以转移运动纹理（如风格），而通过在去噪过程中固定自注意力图可以实现基于示例的多样化生成。

**运动风格迁移**的结果见Table 6。在生成过程中编辑（Gen.）和DDIM反演后编辑（Inv.）两种设置下，MotionCLR均取得了优于基线的FID和多样性指标。DDIM反演引入的生成质量损失可忽略（FID: 0.269 vs. 0.299），证明了在真实运动上应用编辑的可行性。

### 消融实验

**架构设计消融**（Table 7）揭示了关键设计选择的影响：
- 移除分离的词级交叉注意力建模（将文本嵌入融合为单一token）后，R-Precision Top-1从0.544降至0.512，FID从0.269升至0.380。这直接证实了词级对应关系建模对文本-运动对齐和生成质量的关键作用。
- 该消融也间接验证了时间步与文本条件分离注入的必要性——传统方法将时间步与文本特征混合，模糊了词级对应关系。

**编辑层与步骤消融**（Table 8）考察了操纵不同注意力层和扩散步骤对编辑质量的影响：
- 操纵更多层（1-18层 vs. 仅1层或1-9层）和更多扩散步骤（1-9步 vs. 仅1步）可实现更好的语义一致性和生成质量（FID=0.330）。
- 该结果揭示了编辑效果与操纵范围之间的权衡：过少的层/步骤可能无法充分传递编辑信号，而过多的操纵可能引入不必要的干扰。论文最终选择1-18层和1-9步作为默认编辑设置。

### 动作计数能力

Figure 15比较了基于注意力图与基于根轨迹的动作计数错误率。注意力图方法的计数错误率显著低于根轨迹方法，验证了交叉注意力激活比运动学特征更可靠地反映动作执行。然而，在复杂运动序列中仍可能产生计数错误，这是当前方法的已知局限之一。

### 失败模式与局限

1. **极端权重调整引入伪影**：在运动强调/去强调任务中，当缩放因子α接近1.0时，可能产生不自然的运动伪影（Figure 17）。这表明注意力图的线性缩放策略在极端值下可能破坏去噪过程的稳定性。

2. **动作计数在复杂场景中的误差**：尽管注意力图方法优于根轨迹方法，但在包含多个连续或重叠动作的序列中，计数精度仍有提升空间。

3. **生成幻觉问题**：当前方法对生成模型的幻觉现象（如生成文本中未指定的动作）缺乏有效的检测和纠正机制，需要进一步研究。

4. **数据依赖性**：模型性能受限于训练数据的质量和多样性，在分布外文本或稀有动作上的表现有待验证。

### 公平性说明

所有生成基线均使用官方或开源实现，在相同数据集和评估协议下比较。编辑评估构建了专用测试集（HVerb和HVerb-wild），由研究人员标注动词边界，确保了评估的客观性和可复现性。DDIM反演与原始生成的结果差异可忽略（FID: 0.269 vs. 0.299），证明了编辑GT运动的可行性，避免了反演过程引入系统性偏差。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2410_18977/figures/005_Table_1.jpg]]
*Table 1: Comparison with different methods on the HumanML3D dataset. The baselines include diffusion-based methods and state-of-the-art methods. The “†” notation denotes the DPM-solver sampling inference design choice and “∗” is the DDIM sampling choice. As DPM-solver and DDIM present comparable performance, without specification, we set the DDIM sampling as our default choice. The comparison shows that MotionCLR is with comparable performance with state-of-the-art methods*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2410_18977/figures/007_Table_3.jpg]]
*Table 3: In-place motion replacement. ∗The “R” and “C” settings represent “Replace A as B” and “Change A with B” prompts of MotionFix. The light gray text is the comparison group, denoting the upper bound of the performance. The bold numbers are the best results excepting the comparison group. The significant metric margin over baselines shows the good performance of the method, even some methods requiring specific training*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2410_18977/figures/021_Table_7.jpg]]
*Table 7: Ablation studies between different technical design choices*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2410_18977/figures/022_Table_8.jpg]]
*Table 8: The ablation study of manipulating different attention layers on the HVerb-wild test set. The “begin” and “end” represent the beginning and the final layer/step for manipulation. The bottom row denotes our design choice for motion editing*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2410_18977/figures/024_Figure_15.jpg]]
*Figure 15: Action counting error rate comparison. Root trajectory (Traj.) vs. attention map (Ours)*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2410_18977/figures/006_Table_2.jpg]]
*Table 2: IoU (%) metrics on different settings. High coherence among E1, E2, and E3 shows the fine-grained text-motion modeling in cross attention*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2410_18977/figures/020_Table_6.jpg]]
*Table 6: Comparison of motion style transfer across baselines. The “Gen.” and “Inv.” settings represent the editing during generation and DDIM inversion Song et al. [2021] (following Raab et al. [2024a]) settings*

## 方法谱系与知识库定位

### 技术路线与基线定位

MotionCLR 继承了扩散模型驱动的人体运动生成范式，其直接技术祖先可追溯至 **MDM**（Tevet et al., 2022b），后者首次将扩散模型引入运动生成领域。与 MDM 将文本条件融合为单一全局 token 的做法不同，MotionCLR 的关键突破在于将文本-运动交互从全局嵌入解耦为**词级交叉注意力**建模。这一设计使模型获得了细粒度的语义对应能力，从而支撑了一系列训练无关的编辑操作。

在生成性能层面，MotionCLR 与同期最先进方法处于同一梯队：在 HumanML3D 基准上，其 R-Precision Top1 达到 0.544，优于 **MotionDiffuse**（Zhang et al., 2024a）的 0.491；FID 降至 0.269，较 MDM 的 0.544 有显著改善（Table 1）。值得注意的是，MotionCLR 并非以追求极致生成指标为首要目标——其核心贡献在于通过架构设计使注意力图本身成为可解释、可操纵的控制界面。

与专注于编辑的基线相比，**MotionFix**（Athanasiou et al., 2024）和 **MEOs**（Goel et al., 2024）依赖语言指令或外部编辑模块来实现运动修改，而 MotionCLR 的编辑能力内生于生成过程：通过直接操纵交叉注意力图实现原位动作替换，或通过缩放注意力权重实现动作强调/减弱。在 HVerb 测试集上，MotionCLR 的原位替换未编辑部分保留误差（MPJPE）为 57.9 mm，显著低于 MotionFix-C 的 75.3 mm（Table 3），表明注意力操纵策略在保持运动上下文一致性方面具有明显优势。

### 架构设计的三个关键解耦

MotionCLR 的 CLR 块（Figure 2）实现了三项对基线架构的关键改造：

1. **时间步注入与文本条件解耦**：基线方法（如 MDM）通常将时间步嵌入与文本特征混合后注入网络，而 MotionCLR 采用独立的 Conv1d 模块处理时间步信息，使文本交叉注意力不受扩散时间步的干扰。这一设计确保了交叉注意力图在不同去噪阶段保持语义一致性，是编辑操作可靠性的基础。

2. **自注意力仅建模运动帧间关系**：与将文本和运动 token 混合输入自注意力的方案不同，MotionCLR 的自注意力仅接收运动特征。这使得自注意力图纯粹反映帧间运动模式的相似性，为基于自注意力图移位的序列重排（Figure 4c）和风格迁移提供了干净的信号源。

3. **词级交叉注意力的分离建模**：这是方法的核心因果开关。消融实验（Table 7）表明，移除分离的词级交叉注意力后，R-Precision Top1 从 0.544 降至 0.512，FID 从 0.269 升至 0.380，验证了该设计对文本-运动对齐和生成质量的关键作用。

### 适用边界与局限

尽管 MotionCLR 在交互式编辑方面展现了独特能力，其适用性受以下边界约束：

- **生成幻觉问题**：论文明确指出方法在处理生成模型幻觉方面仍然有限。当文本描述的动作在训练数据中缺乏对应的高质量运动样本时，注意力操纵可能放大而非修正生成偏差。
- **极端权重调整的伪影**：在动作强调/减弱任务中，当缩放因子 α 接近 1.0 时，运动可能出现不自然的抖动或幅度失真（Figure 17），这表明注意力图的线性缩放与运动动力学的非线性之间存在固有张力。
- **复杂序列的动作计数误差**：虽然交叉注意力图在动作计数任务上优于基于根轨迹的方法（Figure 15），但在包含多个连续或重叠动作的复杂序列中仍可能产生计数错误。
- **数据依赖性**：模型的词级对应能力受限于训练数据的语义多样性和标注质量。对于训练集中罕见的动词或动作组合，交叉注意力的激活模式可能不够可靠。

### 开放问题

1. **对话式交互扩展**：当前方法要求用户明确指定编辑目标（如替换动词、调整权重），如何将注意力操纵机制嵌入语言对话式交互框架，使模型能够理解“跳得更高一点”这类自然语言指令，是向实用化迈进的关键问题。

2. **编辑最优参数的自适应确定**：消融实验（Table 8）显示，操纵不同数量的注意力层（1-18 层）和扩散步骤（1-9 步）会显著影响编辑质量，但最优配置因任务而异。能否设计自适应机制，根据编辑类型和运动内容自动选择操纵范围？

3. **多模态注意力一致性**：当前方法仅利用文本-运动交叉注意力，而 CLIP 嵌入本身已包含视觉-语言对齐先验。探索如何引入视觉模态的注意力约束，可能进一步提升编辑的语义保真度。

4. **更大规模预训练的潜力**：论文采用 CLIP-ViT-B 作为文本编码器，且训练数据限于 HumanML3D 等中小规模运动数据集。若将架构迁移至更大规模的运动-文本配对数据，并结合更强的语言模型，词级对应关系的鲁棒性和泛化能力有望显著提升，但计算成本和注意力图可解释性之间的平衡需要审慎评估。

## 原文 PDF

![[paperPDFs/arxiv_2024/Pay_Attention_and_Move_Better_Harnessing_Attention_for_Interactive_Motion_Generation_and_Training_free_Editing.pdf]]