---
title: "HINT: HIERARCHICAL INTERACTION MODELING FOR AUTOREGRESSIVE MULTI-HUMAN MOTION GENERATION"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Motion_Generation.pdf
aliases:
- HINT
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用滑动窗口自回归扩散框架，在规范化潜在空间中解耦个体运动表示与交互关系，并通过层次化条件（局部与全局）引导生成过程。
primary_logic: 将每个参与者的运动转换到各自的局部坐标（规范化潜在空间），并显式提供参与者间的相对刚体变换作为条件，使得潜在空间专注于运动语义，并易于扩展到任意人数；同时利用滑动窗口聚合局部历史、文本和时序索引以及全局序列位置和组合命令，实现细粒度交互建模和长序列连贯性。
claims:
- 在InterHuman数据集上，HINT的FID达到3.100，大幅优于之前最佳方法InterMask的5.154。
- 移除规范化潜在空间（改用联合多人潜在空间）导致重构FID从0.307升至7.783。
- 移除任一局部或全局条件均导致FID显著升高、R@Top3下降，验证层次化条件不可或缺。
- InterHuman 上 FID↓ = 3.100 ± .035
---

# HINT: HIERARCHICAL INTERACTION MODELING FOR AUTOREGRESSIVE MULTI-HUMAN MOTION GENERATION

> [!tip] 核心洞察
> 将每个参与者的运动转换到各自的局部坐标（规范化潜在空间），并显式提供参与者间的相对刚体变换作为条件，使得潜在空间专注于运动语义，并易于扩展到任意人数；同时利用滑动窗口聚合局部历史、文本和时序索引以及全局序列位置和组合命令，实现细粒度交互建模和长序列连贯性。

| 字段 | 内容 |
|------|------|
| 中文题名 | HINT：用于自回归多人运动生成的分层交互建模 |
| 英文题名 | HINT: HIERARCHICAL INTERACTION MODELING FOR AUTOREGRESSIVE MULTI-HUMAN MOTION GENERATION |
| 会议/期刊 | arXiv 2026 |
| Links |  [paper](https://arxiv.org/abs/2601.20383)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | HINT |
| Dataset | InterHuman, InterX |

> [!tip] 效果简介
> - InterHuman 上，FID↓ 3.100 ± .035 vs 5.154 (InterMask) (-2.054)；R@Top3↑ 0.672 ± .004 vs 0.683 (InterMask) (-0.011)；MMDist↓ 4.979 ± .053 vs 3.790 (InterMask) (+1.189)。
> - InterX 上，FID↓ 0.278 ± .012 vs 0.399 (InterMask) (-0.121)；R@Top3↑ 0.682 ± .003 vs 0.705 (InterMask) (-0.023)；MMDist↓ 4.007 ± .016 vs 3.705 (InterMask) (+0.302)。

## 概述

**问题瓶颈**：现有多人运动生成方法（如InterGen、in2IN、InterMask）以离线方式一次性生成固定长度、固定人数的运动序列，无法处理变长文本描述和动态人数变化的交互场景，且难以捕捉长程依赖性。

**核心思路**：HINT提出滑动窗口自回归扩散框架，在**规范化潜在空间**中将个体运动表示与交互关系解耦——将每个参与者的运动转换到各自的局部坐标，显式提供参与者间的相对刚体变换作为条件，使潜在空间专注于运动语义并可扩展到任意人数。同时通过**层次化条件**（局部历史、文本与时序索引，以及全局序列位置和组合命令）引导扩散去噪过程，实现细粒度交互建模与长序列连贯生成。

**方法定位**：HINT是首个将自回归生成与扩散模型结合用于多人交互运动生成的在线框架。相比离线方法（InterMask、InterGen、in2IN等），它支持流式、变长、变人数的生成；相比在线变体（InterMask*、DART†），它在运动质量和交互合理性上显著领先。

**主要结果**：
- 在InterHuman数据集上，HINT的FID达到**3.100**，大幅优于之前最优离线方法InterMask的5.154（Table 1）。
- 在InterX数据集上，FID为**0.278**，同样优于InterMask的0.399。
- 消融实验证实：移除规范化潜在空间导致重构FID从0.307升至7.783（Table 3）；移除任一局部或全局条件均使FID显著升高、R@Top3下降（Table 2）。
- 用户研究（Figure 4）和定性对比（Figure 5）表明HINT在复杂交互区域表现更优。

**局限与开放问题**：HINT在文本-运动对齐（R@Top3、MMDist）上略逊于离线方法；目前仅在两人数据集上训练，多人场景为零样本扩展；推理速度约1.1秒/16帧，尚未达到实时。未来可探索结合场景与物体交互、在超长序列上的误差累积控制，以及多人数据微调策略。

## 背景与动机

### 多人运动生成的任务演进

生成逼真、语义一致且可交互的多人类运动是计算机视觉与图形学中的核心挑战，其应用涵盖虚拟现实、游戏角色动画、人机交互与具身智能仿真。早期工作主要聚焦于**单人运动生成**，代表性的扩散方法如 **MDM** 和 **T2M** 在文本到单人运动任务上取得了显著进展，但这类方法天然缺乏对多主体间空间关系与交互语义的建模能力。

近年来，研究者开始将注意力转向**双人/多人交互运动生成**，涌现出一批基于离线（single-shot）范式的方法：**ComMDM** 引入通信机制来协调双人运动，**InterGen** 采用共享注意力实现交互感知，**MoMat-MoGen** 结合运动匹配与生成，**in2IN** 提出双层提示条件，**InterMask** 则利用掩码标记预测框架在 InterHuman 和 InterX 数据集上取得了当时最优的 FID 指标。然而，这些方法共享一个根本性约束——它们均以**一次前向传播生成固定长度、固定人数的运动序列**，无法应对实际应用中常见的变长文本描述和动态人数变化的交互场景。

### 现有方法的核心瓶颈

经分析，现有离线方法存在三个相互关联的瓶颈：

1. **固定长度与固定人数的生成范式**：现有方法（如 InterGen、in2IN、InterMask）将运动生成建模为单步（single-shot）过程，输出序列长度在训练时即已确定。这使得模型无法处理开放式的、持续演进的交互场景——例如，当文本指令在生成过程中发生变化，或交互参与者中途加入/退出时，离线方法缺乏相应的机制来动态调整生成策略。

2. **长程依赖性捕捉困难**：多人交互运动天然具有长程时空依赖——一个参与者的当前动作往往是对数秒前对方行为的响应。离线方法需要一次性建模完整序列的全局依赖，随着序列长度增长，注意力机制的计算复杂度呈平方级增长，且远距离帧之间的信息传递效率下降，导致长序列的连贯性难以保证。

3. **世界坐标系下的耦合表示**：现有方法通常将所有参与者的运动编码在统一的**世界坐标系**中，这使得运动表示同时编码了个体运动语义和参与者间的空间关系。这种耦合导致两个问题：（a）潜在空间需要额外学习空间变换的不变性，增加了优化难度；（b）当参与者人数变化时，联合潜在空间的维度结构需要重新设计，难以零样本扩展到更多人的场景。

### 本文动机与核心思路

针对上述瓶颈，**HINT** 提出了一套从表示空间到生成范式的系统性重构，其核心动机可概括为三个递进的层次：

- **解耦个体运动与交互关系**：将每个参与者的运动转换到各自的**规范化局部坐标系**（canonicalized latent space），使潜在空间专注于运动语义本身；同时，显式提供参与者间的相对刚体变换（旋转和平移）作为条件信号，由扩散模型负责建模交互关系。这一设计使运动表示与参与人数解耦，理论上可零样本扩展到任意人数。

- **自回归滑动窗口实现流式生成**：将长序列生成分解为重叠窗口的逐段预测，每个窗口内由交互感知扩散模型预测未来 $K$ 帧，条件于历史运动与文本。这种自回归扩散混合范式使得 HINT 能够支持**变长序列生成**和**在线文本更新**，突破了离线方法的固定长度限制。

- **层次化条件引导细粒度交互建模**：在滑动窗口内部，HINT 聚合**局部条件**（历史运动嵌入、相对历史嵌入、步索引、词级文本嵌入）和**全局条件**（序列位置索引、组合命令嵌入），从时空和语义多个尺度引导去噪过程，确保局部动作的交互合理性与全局序列的叙事连贯性。

Figure 2 直观对比了传统离线方法与 HINT 自回归框架的架构差异：前者一次性生成固定长度序列，后者通过滑动窗口逐步预测未来帧，实现开放式生成。Figure 3 进一步展示了 HINT 在双人交互生成中的完整流程——从规范化潜在空间的构建，到滑动窗口自回归生成，再到交互感知扩散模型内部的层次化条件融合。

通过上述设计，HINT 在 InterHuman 数据集上取得了 **FID 3.100** 的指标，相较于此前最优的离线方法 InterMask（FID 5.154）实现了约 40% 的相对提升，同时在 InterX 数据集上也展现出一致的性能优势（FID 0.278 vs 0.399）。值得指出的是，HINT 在文本-运动对齐指标（R@Top3、MMDist）上略逊于离线方法，这是自回归范式缺乏全局优化的固有代价，也是后续研究可改进的方向。

## 核心创新

HINT 针对现有多人运动生成方法“单次生成固定长度、固定人数序列”的根本瓶颈，提出了三项紧密耦合的创新，构成一个支持**在线、变长、变人数**的自回归生成框架。

### 1. 规范化潜在空间（Canonicalized Latent Space）

现有方法（如 InterGen、InterMask）通常在**世界坐标系**下建立统一的多人潜在空间，导致个体运动表示与空间交互关系高度纠缠。当人数变化或场景扩展时，这种耦合使模型难以泛化。

HINT 的核心思路是**解耦个体运动与交互关系**：将每个参与者 $i$ 的运动独立转换到其自身的局部规范坐标系：

$$\bar{\mathbf{M}}_{(i)}^{\mathbf{c}} = \mathbf{R}_{(i)} \mathbf{M}_{(i)} \bar{\mathbf{\Lambda}} + \mathbf{T}_{(i)}$$

同时显式编码参与者之间的相对刚体变换 $\mathbf{R}^{ij}$ 和 $\mathbf{T}^{ij}$ 作为交互条件。这一设计使潜在空间专注于运动语义本身，而空间关系由条件分支显式提供，天然支持任意人数扩展——新增参与者只需计算其相对于已有参与者的刚体变换，无需修改模型结构。

消融实验提供了强证据：移除规范化潜在空间（改用联合多人潜在空间）后，重构 FID 从 **0.307 急剧恶化至 7.783**（Table 3），验证了解耦设计对生成质量的决定性作用。

### 2. 滑动窗口自回归扩散框架

传统方法采用单次前向生成（single-shot），输出长度固定，无法处理在线交互场景中持续变化的文本指令和动态人数。HINT 引入**滑动窗口自回归策略**：将长序列切分为重叠窗口，逐窗口预测未来 $K$ 帧：

$$\hat{\mathbf{M}}^{t:t+K} \sim p_\theta(\mathbf{M}^{t:t+K} \mid \hat{\mathbf{M}}^{1:t-1}, T^{1:t+K})$$

这一范式转变的关键收益是**流式生成能力**——模型可在推理时持续接收新文本指令，动态调整生成目标，支持开放长度的交互序列。同时，所有参与者共享同一个去噪网络权重，通过对称条件机制处理任意数量个体，避免了为不同人数设计独立分支的复杂性。

### 3. 层次化运动条件（Hierarchical Motion Condition, HMC）

为在自回归框架下实现细粒度交互建模，HINT 设计了**局部-全局双层条件体系**：

- **局部条件**：包括当前窗口的历史运动嵌入、时序步索引嵌入、转换到目标坐标系的伙伴历史嵌入（相对历史嵌入），以及词级文本嵌入（通过 Text Cross-Attention 注入）。这些条件提供窗口内的即时时空和语义上下文。
- **全局条件**：包括序列位置索引与总帧数嵌入（通过 AdaLN 注入），以及组合命令嵌入（通过 Text Cross-Attention 注入）。这些条件提供长程时序定位和整体语义指导。

消融实验（Table 2）表明，移除任一条件均导致 FID 显著升高：历史运动嵌入（+1.497）、相对历史嵌入（+1.474）、序列索引与总帧数嵌入（+0.443）、组合命令嵌入（+0.241）、词级文本嵌入（+0.195）、步索引（+0.124）。这验证了**层次化条件对于自回归交互生成不可或缺**，其中历史与相对历史嵌入的贡献最为突出，说明交互上下文的时空对齐是多人运动连贯性的关键瓶颈。

## 整体框架

HINT 将多人运动生成建模为一个**滑动窗口自回归扩散过程**，其核心设计目标是在支持变长文本和动态人数变化的条件下，实现连贯的长序列交互生成。整体 pipeline 由三个关键模块串联构成：**Motion VAE（运动变分自编码器）**、**Interaction-Aware Diffusion（交互感知扩散模型）** 和 **Sliding-Window Autoregressive Process（滑动窗口自回归过程）**，三者协同工作，形成“编码-条件生成-流式拼接”的完整链路。

### 输入输出流

系统的输入包括两部分：**历史运动序列**和**文本描述**。对于 $N$ 个参与者、$T$ 帧的运动序列，其形式化表示为：

$$\mathbf{M}^{1:T} = \{ \mathbf{m}_{(i)}^t \in \mathbb{R}^d \mid i=1,\dots,N; t=1,\dots,T \}$$

其中 $d$ 为每帧的运动表征维度。在自回归范式下，模型递归地预测未来 $K$ 帧：

$$\hat{\mathbf{M}}^{t:t+K} \sim p_\theta(\mathbf{M}^{t:t+K} \mid \hat{\mathbf{M}}^{1:t-1}, T^{1:t+K})$$

输出为预测的 $K$ 帧运动，这些帧与已生成的历史帧拼接后，滑动窗口向前推进，形成流式生成循环。

### 模块关系与数据流

**Motion VAE** 作为 pipeline 的前置模块，承担两个职责：其一，将每个参与者的原始运动从世界坐标转换到各自的局部规范坐标（canonicalized latent space），解耦个体运动表示与交互关系；其二，通过编码器 $E$ 将规范化的运动压缩为紧凑的潜在向量 $\mathbf{z}_{(i)}^{\mathbf{f}}$，并在训练后冻结。这一规范化潜在空间是 HINT 能够将权重共享于任意人数参与者的基础——每个代理的运动都在自己的局部坐标系中编码，而参与者间的相对刚体变换（旋转 $\mathbf{R}^{ij}$ 和平移 $\mathbf{T}^{ij}$）被显式提取并作为后续条件注入，从而将潜在空间解放出来专注于运动语义本身。

**Interaction-Aware Diffusion** 是生成的核心引擎。它在 Motion VAE 定义的潜在空间中执行扩散去噪，融合**层次化条件（Hierarchical Motion Condition, HMC）** 来引导未来运动潜在表示的生成。HMC 将时间、空间和语义线索组织为两个层级：

- **局部条件**：包括目标参与者的历史运动嵌入、时序步索引、伙伴历史运动（经坐标系变换后）的嵌入，以及词级文本嵌入（通过 Text Cross-Attention 注入）。
- **全局条件**：包括全局序列索引与总帧数（通过 AdaLN 注入），以及组合命令嵌入（同样通过 Text Cross-Attention 注入），为整个序列提供宏观语义和时序位置信息。

这些条件通过交叉注意力和自适应层归一化等机制逐层融入扩散去噪网络，使模型在每一步生成时都能感知精细的局部交互动态和全局序列进度。

**Sliding-Window Autoregressive Process** 负责将长序列切分为重叠窗口，逐窗口调用 Interaction-Aware Diffusion 生成 $K$ 帧，再将各窗口的输出拼接为完整序列。这一策略绕开了传统单次生成方法对固定长度的依赖，使 HINT 能够处理开放时长和动态人数变化的场景。

### 训练与损失

训练分为两个阶段。第一阶段训练 Motion VAE，目标为最小化重建损失与 KL 散度：

$$\mathcal{L}_{\mathrm{VAE}} = \sum_i \mathcal{L}_{\mathrm{rec}}(\hat{\mathbf{M}}_{(i)}, \mathbf{M}_{(i)}) + \beta \mathcal{L}_{\mathrm{KL}}(q_\phi(\mathbf{z}_{(i)}^{\mathbf{f}} \mid \mathbf{M}_{(i)}^{\mathbf{c}}) \mid\mid p(\mathbf{z}_{(i)}^{\mathbf{f}}))$$

第二阶段训练 Interaction-Aware Diffusion，总损失在扩散去噪损失 $\mathcal{L}_{\mathrm{diff}}$ 的基础上，加入三项交互正则项以增强生成运动的物理合理性和交互质量：

$$\mathcal{L} = \mathcal{L}_{\mathrm{diff}} + \lambda_{\mathrm{aff}} \mathcal{L}_{\mathrm{aff}} + \lambda_{\mathrm{dist}} \mathcal{L}_{\mathrm{dist}} + \lambda_{\mathrm{ori}} \mathcal{L}_{\mathrm{ori}}$$

其中 $\mathcal{L}_{\mathrm{aff}}$ 为关节亲和度约束，$\mathcal{L}_{\mathrm{dist}}$ 为跨人距离约束，$\mathcal{L}_{\mathrm{ori}}$ 为相对朝向约束。这些正则项显式编码了多人交互中的空间关系先验。

### 架构对比

Figure 2 清晰展示了 HINT 与传统单次生成方法的架构差异。现有方法（如 InterGen、in2IN、InterMask）以单次前向传播生成固定长度的完整序列，无法适应变长文本和动态人数。HINT 则通过将自回归策略与扩散模型集成，在滑动窗口内利用历史运动和文本逐步合成未来运动，从而支持开放式、可变长度的流式生成。

![[assets/figures/papers/paper_list_l1701_HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Mo/figures/002_Figure_2.jpg]]
*Figure 2: Architecture Comparison. (a) Conventional Single-shot Methods: Existing approaches (e.g., InterGen, in2IN, InterMask) generate motion sequences in a single shot with fixed length. (b) HINT: Our framework integrates autoregressive and diffusion modeling to support streaming generation. Within a sliding window, the Interaction-Aware Diffusion leverages history and text to progressively synthesize future motions, thereby supporting open-ended, variable-length generation*

### 补充图表

![[assets/figures/papers/paper_list_l1701_HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Mo/figures/003_Figure_3.jpg]]
*Figure 3: Overview of HINT in two-human interaction generation. (a) Canonicalized latent space. (b) Within this latent space, motion is generated in a sliding-window autoregressive manner, where the Interaction-Aware Diffusion predicts the next K frames. (c) The detailed architecture of the Interaction-Aware Diffusion, in which hierarchical conditions guide the generation process*

## 核心模块与公式推导

### 3.1 自回归多人运动生成框架

HINT 将多人运动生成建模为自回归预测问题。给定 $N$ 个参与者、$T$ 帧的运动序列：

$$
\mathbf{M}^{1:T} = \{ \mathbf{m}_{(i)}^t \in \mathbb{R}^d \mid i=1,\dots,N;\; t=1,\dots,T \}
$$

其中 $\mathbf{m}_{(i)}^t$ 表示第 $i$ 个参与者在时刻 $t$ 的 $d$ 维姿态表示。在每一自回归步中，模型基于已生成的历史运动 $\hat{\mathbf{M}}^{1:t-1}$ 和文本描述 $T^{1:t+K}$，预测未来 $K$ 帧：

$$
\hat{\mathbf{M}}^{t:t+K} \sim p_\theta(\mathbf{M}^{t:t+K} \mid \hat{\mathbf{M}}^{1:t-1}, T^{1:t+K}) \tag{2}
$$

为提升效率，HINT 联合预测 $K$ 个未来时间步，而非逐帧生成。

### 3.2 规范化潜在空间

HINT 的核心创新在于将每个参与者的运动从世界坐标系转换到各自的局部规范坐标系，实现个体运动表示与交互关系的解耦。对于参与者 $i$，其规范化运动表示为：

$$
\bar{\mathbf{M}}_{(i)}^{\mathbf{c}} = \mathbf{R}_{(i)} \mathbf{M}_{(i)} \bar{\mathbf{\Lambda}} + \mathbf{T}_{(i)}
$$

其中 $\mathbf{R}_{(i)}$ 和 $\mathbf{T}_{(i)}$ 分别为参与者 $i$ 的旋转矩阵和平移向量。参与者 $i$ 与 $j$ 之间的相对刚体变换显式编码为：

$$
\mathbf{R}^{ij} = \mathbf{R}_{(i)} \mathbf{R}_{(j)}^{\top}, \quad \mathbf{T}^{ij} = \mathbf{T}_{(i)} - \mathbf{R}^{ij} \mathbf{T}_{(j)} \tag{4}
$$

基于 Transformer 的 Motion VAE 编码器 $E$ 将规范化后的未来运动编码为潜在向量 $\mathbf{z}_{(i)}^{\mathbf{f}} \in \mathbb{R}^l$：

$$
\mathbf{z}_{(i)}^{\mathbf{f}} \sim q_\phi(\mathbf{z}_{(i)}^{\mathbf{f}} \mid \mathbf{M}_{(i)}^{\mathbf{c}})
$$

Motion VAE 的训练目标为：

$$
\mathcal{L}_{\mathrm{VAE}} = \sum_i \mathcal{L}_{\mathrm{rec}}(\hat{\mathbf{M}}_{(i)}, \mathbf{M}_{(i)}) + \beta \mathcal{L}_{\mathrm{KL}}(q_\phi(\mathbf{z}_{(i)}^{\mathbf{f}} \mid \mathbf{M}_{(i)}^{\mathbf{c}}) \mid\mid p(\mathbf{z}_{(i)}^{\mathbf{f}})) \tag{9}
$$

包含重建损失和 KL 散度正则项。训练完成后，VAE 参数冻结，后续扩散过程在潜在空间中操作。

### 3.3 层次化运动条件

HINT 的层次化运动条件策略将时间、空间和语义线索组织为局部条件与全局条件两个层级：

- **局部条件**：包括历史运动嵌入、步索引嵌入、相对历史嵌入（将伙伴历史转换到目标坐标系）以及词级文本嵌入。词级文本嵌入通过交叉注意力注入潜在特征：

  $$
  \mathbf{z}_A^{\mathrm{word}} = \mathrm{CrossAttn}(\mathbf{z}_A^{\mathrm{part}}, \mathbf{E}_{\mathrm{word}}, \mathbf{E}_{\mathrm{word}})
  $$

- **全局条件**：包括序列索引与总帧数嵌入（通过 AdaLN 注入扩散网络），以及组合命令嵌入（通过文本交叉注意力注入）：

  $$
  \mathbf{z}_A^{\mathrm{com}} = \mathrm{CrossAttn}(\mathbf{z}_A^{\mathrm{part}}, \mathbf{e}, \mathbf{e})
  $$

### 3.4 交互感知扩散与正则化

交互感知扩散模块在潜在空间中进行去噪，融合层次化条件生成未来运动潜在表示。总损失函数为：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{diff}} + \lambda_{\mathrm{aff}} \mathcal{L}_{\mathrm{aff}} + \lambda_{\mathrm{dist}} \mathcal{L}_{\mathrm{dist}} + \lambda_{\mathrm{ori}} \mathcal{L}_{\mathrm{ori}} \tag{10}
$$

其中：
- $\mathcal{L}_{\mathrm{diff}}$ 为扩散去噪损失；
- $\mathcal{L}_{\mathrm{aff}}$ 为关节亲和度损失，约束交互关节的空间一致性；
- $\mathcal{L}_{\mathrm{dist}}$ 为跨人距离约束，防止参与者间不合理的穿透或分离；
- $\mathcal{L}_{\mathrm{ori}}$ 为相对朝向约束，保持交互时的合理相对朝向。

三个正则项通过超参数 $\lambda_{\mathrm{aff}}$、$\lambda_{\mathrm{dist}}$、$\lambda_{\mathrm{ori}}$ 加权，共同引导生成过程产生物理合理的多人交互运动。

### 3.5 滑动窗口自回归推理

推理阶段，HINT 将长序列切分为重叠的滑动窗口，逐窗口调用交互感知扩散生成 $K$ 帧未来运动，并与已生成序列拼接。该策略支持流式、变长生成，同时通过窗口重叠保持序列连贯性。所有参与者共享同一组去噪网络权重，条件输入采用对称设计，使框架可零样本扩展到任意人数。

## 实验与分析

### 主实验与定量结果

HINT 在 InterHuman 与 InterX 两个双人交互数据集上系统评估了运动质量（FID）、文本-运动匹配度（R@Top3、MMDist）和多样性（Diversity），并与离线单次生成方法及在线自回归变体进行了对比。所有指标均运行 20 次不同随机种子，报告 95% 置信区间（Table 1）。

![[assets/figures/papers/paper_list_l1701_HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Mo/figures/004_Table_1.jpg]]
*Table 1: Results on InterHuman and InterX. → denotes closer to ground truth is better, ↑ / ↓ means higher/lower is better, ± indicates the 95% confidence interval. Bold denotes the best result. InterMask* is the online version of InterMask, while DART† is the two-human version of DART*

**InterHuman 数据集**上，HINT 的 FID 达到 3.100 ± .035，较之前最优离线方法 InterMask 的 5.154 大幅降低 2.054，表明生成运动的真实感和自然度显著提升。在 R@Top3 指标上，HINT 为 0.672 ± .004，略低于 InterMask 的 0.683（差距 0.011），MMDist 为 4.979 ± .053，高于 InterMask 的 3.790（差距 +1.189），说明在文本-运动对齐精度上离线方法仍具微弱优势——这是自回归框架未进行全局优化的固有代价。Diversity 方面，HINT 为 7.950 ± .032，与 InterMask 的 7.944 近乎一致，表明生成运动保持了与真实数据相当的多样性。

**InterX 数据集**上，HINT 的 FID 为 0.278 ± .012，优于 InterMask 的 0.399（降低 0.121），再次验证了运动质量的提升。R@Top3 为 0.682 ± .003，略低于 InterMask 的 0.705（差距 0.023）；MMDist 为 4.007 ± .016，高于 InterMask 的 3.705（差距 +0.302），与 InterHuman 上的相对格局一致。Diversity 为 8.886 ± .066，与 InterMask 的 9.046 接近。

**在线自回归对比**：HINT 在所有指标上均大幅优于在线自回归基线 InterMask* 和 DART†，验证了规范化潜在空间与层次化条件设计的有效性，而非仅依赖滑动窗口策略本身。

**用户研究**（Figure 4）：在 HINT、DART† 和 InterMask 三者之间进行人工偏好评估，HINT 在运动质量和交互合理性上获得显著偏好，进一步佐证了定量指标的提升具有感知层面的意义。

### 消融实验

消融实验围绕 HINT 的两大核心设计展开：规范化潜在空间（Canonicalized Latent Space）和层次化运动条件（Hierarchical Motion Condition）。

#### 规范化潜在空间（Table 3）

![[assets/figures/papers/paper_list_l1701_HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Mo/figures/008_Table_3.jpg]]
*Table 3: Ablation of the Canonicalized Latent Space on InterHuman*

移除规范化潜在空间，改用联合多人世界坐标潜在空间，导致重构 FID 从 0.307 急剧恶化至 7.783。这一结果直接证明了将每个参与者的运动转换到各自局部坐标系的必要性——联合空间难以解耦个体运动语义与交互关系，导致潜在表示的信息瓶颈严重退化。

#### 层次化运动条件（Table 2）

![[assets/figures/papers/paper_list_l1701_HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Mo/figures/007_Table_2.jpg]]
*Table 2: Ablations HINT’s key components on InterHuman. L/G indicates local/global conditions*

在 InterHuman 上逐一移除各条件组件，以 FID 变化衡量其贡献：

**局部条件**：
- 移除历史运动嵌入（w/o History Motion Embedding）：FID 升高 1.497
- 移除相对历史嵌入（w/o Relative History Embedding）：FID 升高 1.474
- 移除词级文本嵌入（w/o Word-level Text Embedding）：FID 升高 0.195
- 移除步索引嵌入（w/o Step Index Embedding）：FID 升高 0.124

**全局条件**：
- 移除序列索引及总帧数嵌入（w/o Sequence Index & Total Frames）：FID 升高 0.443
- 移除组合命令嵌入（w/o Compositional Command Embedding）：FID 升高 0.241

历史运动嵌入和相对历史嵌入的影响最为显著，表明对过去交互上下文的建模是生成连贯多人运动的核心。全局条件中，序列位置信息的贡献大于组合语义命令，说明长序列中的时序定位对自回归生成质量至关重要。移除任一条件均导致 R@Top3 下降（详细数据见 Table C-4），验证了层次化条件设计在文本-运动对齐上的协同作用。

### 定性分析与可视化

Figure 5 展示了 InterMask、InterMask*、DART† 和 HINT 在复杂交互场景下的定性对比。HINT 在精细交互区域（如握手、拥抱、共同操作物体）表现更优，生成的运动保持了参与者的个体姿态特征和相对空间关系。Figure A-1 展示了三人运动生成的零样本扩展结果，表明基于规范化潜在空间的对称权重设计使模型能够泛化到训练时未见的人数配置。

![[assets/figures/papers/paper_list_l1701_HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Mo/figures/005_Figure_5.jpg]]
*Figure 5: Visual comparisons of InterMask, InterMask*, DART† and HINT on InterHuman. HINT performs better in regions with complex interactions*

### 失败模式与局限

1. **文本-运动对齐精度**：HINT 在 R@Top3 和 MMDist 上略逊于离线单次生成方法（如 InterMask），这是自回归框架缺乏全局优化的固有局限，错误可能在长序列中累积。
2. **多人泛化**：模型仅在两人数据上训练，虽然可零样本扩展到三人（Figure A-1），但未在大型多人数据集上验证，多人交互质量可能随人数增加而退化。
3. **推理速度**：当前推理速度约 1.1s/16 帧，虽适用于在线生成场景，但尚未达到实时交互要求。
4. **交互范围**：目前仅限于人体间交互，未与场景物体或环境上下文结合，限制了在更广泛交互场景中的应用。

### 实验设置要点

所有对比方法使用统一的评估协议。在线变体 InterMask* 和 DART† 基于与 HINT 相同的滑动窗口设置重新训练，确保公平比较。训练超参数与模型配置详见 Table B-1 和 Table B-2。

### 补充图表

![[assets/figures/papers/paper_list_l1701_HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Mo/figures/006_Figure_4.jpg]]
*Figure 4: User study between HINT, DART† and InterMask*

![[assets/figures/papers/paper_list_l1701_HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Mo/figures/001_Figure_1.jpg]]
*Figure 1: Visualization of three-human motion generation results of HINT. By continuously updating the text guidance, HINT can autoregressively generate coherent, plausible human motions*

![[assets/figures/papers/paper_list_l1701_HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Mo/figures/009_Figure.jpg]]
*Figure: A-1: Additional examples of three-human motion generation result*

![[assets/figures/papers/paper_list_l1701_HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Mo/figures/010_Table.jpg]]
*Table: B-1: Parameters of Motion VAE and Interaction-Aware Diffusion. Table B-2: Training hyperparameters for Motion VAE and Interaction-Aware Diffusion*

![[assets/figures/papers/paper_list_l1701_HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Mo/figures/011_Table.jpg]]
*Table: C-3: Detailed R-precision results on InterHuman and InterX. Bold denotes the best result for each setting*

![[assets/figures/papers/paper_list_l1701_HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Mo/figures/012_Table.jpg]]
*Table: C-4: Detailed R-precision results of ablation studies on InterHuman. L and G indicate local and global conditions, respectively*

## 方法谱系与知识库定位

### 方法谱系：从离线生成到在线自回归交互建模

HINT 处于多人运动生成从“离线单次生成”向“在线自回归生成”范式转换的关键节点。现有方法可大致分为两条技术路线：

**离线单次生成路线** 以固定长度、固定人数的运动序列为目标，通过共享注意力或通信机制建模人际交互。代表性工作包括：
- **ComMDM**：基于通信的双人扩散模型；
- **InterGen**：基于共享注意力的交互生成；
- **MoMat-MoGen**：运动匹配与生成结合的方法；
- **in2IN**：双层级提示驱动的交互生成；
- **InterMask**：基于掩码令牌预测的交互生成方法，在 HINT 出现前保持 InterHuman 数据集上的 SOTA（FID 5.154）。

这些方法的共同瓶颈在于：生成范式为单次前向传播，无法处理变长文本描述和动态人数变化的流式交互场景，且长程依赖建模能力受限于固定上下文窗口。

**在线自回归路线** 试图通过滑动窗口或递归预测突破固定长度限制。HINT 在该路线上的直接对比对象包括：
- **InterMask***：InterMask 的在线适配版本，采用与 HINT 相同的滑动窗口设置重新训练；
- **DART†**：DART 方法向双人运动生成的在线扩展。

HINT 的核心区分点在于 **规范化潜在空间** 与 **层次化条件策略** 的协同设计。与 InterMask* 和 DART† 仅将离线架构套入滑动窗口不同，HINT 在表示层面将每个参与者的运动转换到各自的局部坐标系（规范化潜在空间），并显式提供参与者间的相对刚体变换作为条件，使潜在空间专注于运动语义本身。这一设计使得 HINT 的共享权重扩散模型可以零样本扩展到任意人数，而无需为不同人数重新训练专用分支。

### 适用边界

1. **输入模态**：HINT 当前仅支持文本驱动的多人运动生成，未融合语音、音乐或场景几何等其他模态。
2. **交互类型**：仅限于人体-人体交互，未涉及人体-物体或人体-场景交互。规范化潜在空间仅编码人体骨架运动，相对刚体变换仅描述参与者之间的空间关系。
3. **数据规模**：模型在两人交互数据集（InterHuman、InterX）上训练，虽然可零样本扩展到三人及以上场景，但多人交互质量未在大型多人数据集上系统验证。
4. **序列长度**：滑动窗口策略支持变长生成，但自回归误差累积效应在超长序列（>1000帧）上的表现尚未有定量分析。
5. **推理速度**：约 1.1 秒/16 帧的推理速度适用于在线生成，但尚未达到实时交互要求。

### 已知局限

1. **文本-运动对齐弱于离线方法**：作为自回归方法，HINT 未进行全局优化，在 R@Top3 和 MM Dist 指标上略逊于 InterMask 等离线方法（InterHuman 上 R@Top3 0.672 vs 0.683，MMDist 4.979 vs 3.790），表明局部窗口条件难以完全补偿全局语义对齐的损失。

2. **多人扩展缺乏系统验证**：虽然规范化潜在空间理论上支持任意人数，但交叉注意力模块仅在两人数据上训练，在多人场景下的交互质量可能退化。如何在缺乏多人标注数据的情况下微调该模块仍是开放问题。

3. **交互建模局限于空间关系**：当前交互条件仅编码相对刚体变换（旋转和平移），无法捕捉更细粒度的交互语义（如“A 扶住 B 的手臂”中的接触点信息）。交互正则项（关节亲和度、跨人距离约束、相对朝向约束）仅提供弱监督。

4. **对遮挡和缺失观测的鲁棒性未知**：规范化潜在空间依赖完整的骨架观测来计算局部坐标系，在真实采集场景中常见的遮挡或关节点缺失情况下的鲁棒性尚未被检验。

### 开放问题

1. **场景与物体交互的扩展**：如何将规范化潜在空间框架扩展到包含物体和环境的场景中？可能的路径包括引入物体坐标系下的条件编码，或联合学习人体-物体相对变换。

2. **超长序列的误差累积控制**：在超过 1000 帧的生成中，滑动窗口策略的误差累积机制和长程依赖保持能力如何？是否需要引入全局重规划或周期性校正机制？

3. **多人数据的弱监督/零样本适配**：如何在缺乏多人运动捕捉数据的情况下，通过预训练单人模型和少量配对数据微调交叉注意力模块，以提升多人场景下的交互质量？

4. **规范化潜在空间的鲁棒性边界**：在部分观测、噪声骨架或快速运动场景下，局部坐标系的估计精度对生成质量的影响程度如何？是否需要引入不确定性建模或自适应坐标选择策略？

5. **实时交互生成的可行性**：当前 1.1 秒/16 帧的推理速度距离实时应用仍有差距。模型压缩、蒸馏或采样步数缩减对交互质量的影响需要系统评估。

## 原文 PDF

![[paperPDFs/arxiv_2026/HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Motion_Generation.pdf]]