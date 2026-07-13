---
title: in2IN Leveraging individual Information to Generate Human INteractions
type: paper
paper_level: A
venue: CVPRW
year: 2024
pdf_ref: paperPDFs/CVPRW_2024/in2IN_Leveraging_individual_Information_to_Generate_Human_INteractions.pdf
project_link: https://pabloruizponce.github.io/in2IN
code_link: null
aliases:
- ILIIGHI
tags:
- CVPRW_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入个体动作的文本描述作为额外条件，并通过多权重无分类器引导（Multi-weight CFG）和模型组合方法（DualMDM），可独立调节交互整体与个体动作的生成权重，从而控制个体动作的多样性与交互的连贯性。
primary_logic: 将交互生成条件分解为整体交互描述和个体动作描述，并在扩散模型中分别处理自注意力（个体内动态）和交叉注意力（个体间动态），同时利用单人类运动先验的模型组合，可以在保持交互连贯性的同时显著提高个体动作的多样性和可控性。
claims:
- in2IN在InterHuman数据集上达到SOTA，R-Precision Top1为0.455，FID为5.177。
- 多权重CFG消融发现最佳权重组合为w_c=3, w_I=3, w_i=1。
- DualMDM的指数调度器(λ=0.00875)在个体多样性(EID)与交互质量(R-Precision, FID)之间取得最佳平衡。
- InterHuman 上 R-Precision Top1 = 0.455 (in2IN)
---

# in2IN Leveraging individual Information to Generate Human INteractions

> [!tip] 核心洞察
> 将交互生成条件分解为整体交互描述和个体动作描述，并在扩散模型中分别处理自注意力（个体内动态）和交叉注意力（个体间动态），同时利用单人类运动先验的模型组合，可以在保持交互连贯性的同时显著提高个体动作的多样性和可控性。

| 字段 | 内容 |
|------|------|
| 中文题名 | in2IN：利用个体信息生成人类交互动作 |
| 英文题名 | in2IN Leveraging individual Information to Generate Human INteractions |
| 会议/期刊 | CVPRW 2024 |
| Links | [Project](https://pabloruizponce.github.io/in2IN) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | in2IN + DualMDM |
| Dataset | InterHuman |

> [!tip] 效果简介
> - InterHuman 上，R-Precision Top1 0.455 (in2IN) vs 0.449 (MoMat-MoGen) (+0.006)；FID 5.177 (in2IN) vs 5.674 (MoMat-MoGen) (-0.497)；EID (Extrinsic Individual Diversity) 1.680 (DualMDM exponential λ=0.00875) vs 1.238 (in2IN without DualMDM, λ=0) (+0.442)。

## 概要

现有的人类交互动作生成方法通常仅依赖对整体交互的文本描述（例如“两人相互踢腿”）作为条件，这导致生成的交互动作缺乏对每个参与者个体动作的细粒度控制，难以区分和调控交互中不同人的行为差异，从而限制了生成结果的个体多样性。针对这一瓶颈，本文提出 **in2IN**，一种基于扩散模型的双人交互动作生成框架，其核心思路是将条件信号分解为整体交互描述和每个个体的细粒度动作描述，并通过条件注入策略的重新设计，使模型能够同时建模个体内动态（自注意力）和个体间动态（交叉注意力）。

在此基础上，本文进一步提出了两种互补的技术手段：**多权重无分类器引导**（Multi-Weight CFG），允许在采样过程中独立调节完整条件、仅交互条件和仅个体条件的引导权重，从而精细控制生成行为；以及 **DualMDM**，一种模型组合方法，通过时间依赖的权重调度器将交互模型与单人类运动先验的输出相融合，在保持交互连贯性的同时显著提升个体动作的多样性。

实验结果表明，in2IN 在 InterHuman 数据集上达到了当前最优水平：R-Precision Top1 为 0.455，FID 为 5.177，均优于此前最优方法 MoMat-MoGen（Zhang et al., ICCV 2023）的 0.449 和 5.674。消融实验进一步验证了多权重 CFG 的最优权重组合（$w_c=3, w_I=3, w_i=1$）以及 DualMDM 指数调度器（$\lambda=0.00875$）在个体多样性与交互质量之间的最佳平衡。



### 人类交互动作生成的任务与挑战

生成逼真的人类交互动作是计算机视觉与图形学中的核心挑战，其应用涵盖虚拟现实、机器人交互、游戏动画等场景。与单人类运动生成不同，双人交互生成需要同时建模两个个体的**个体内动态**（intra-personal dynamics）与**个体间动态**（inter-personal dynamics），二者相互耦合，使问题复杂度显著提升。

近年来，基于扩散模型的运动生成方法取得了显著进展。从单人类生成（如 **MDM**，Tevet et al., ICLR 2023）到多人类交互组合（如 **ComMDM**，Shafir et al., arXiv 2023），再到专门的双人交互生成（如 **InterGen**，Liang et al., arXiv 2023；**MoMat-MoGen**，Zhang et al., ICCV 2023），研究者逐步将文本条件引入交互生成，使模型能够根据自然语言描述生成对应的交互动作。

### 现有方法的核心瓶颈

尽管已有方法在交互生成质量上取得了进步，但一个关键瓶颈仍未解决：**现有数据集和条件策略缺乏对个体动作的细粒度文本描述**。具体而言：

- **数据集层面**：主流交互数据集（如 InterHuman）仅提供整体交互描述（如“两个人正在握手”），而不包含对每个个体具体动作的单独描述（如“人物A伸出右手向前”与“人物B伸出右手回应”）。
- **模型层面**：现有方法将整体交互描述作为唯一条件注入扩散模型，模型无法区分和控制交互中每个人的个体动作，导致生成的交互缺乏**个体多样性**——即不同个体在交互中的动作趋于同质化，难以展现个性化的运动风格。

这一瓶颈的因果机制在于：当模型仅以整体描述为条件时，个体内动态被隐式地交由自注意力层从数据中自主学习，缺乏明确的监督信号。这使得模型倾向于生成“平均化”的个体动作，牺牲了个体层面的多样性与可控性。

### 本文动机

针对上述瓶颈，本文提出 **in2IN** 方法，核心动机可概括为两个层面：

1. **条件分解**：将交互生成的条件从单一的整体交互描述，分解为**整体交互描述 + 每个个体的个体动作描述**，使模型能够显式地建模个体内动态。
2. **独立控制**：通过多权重无分类器引导（Multi-Weight CFG）和模型组合方法（DualMDM），实现对交互整体质量与个体动作多样性的**独立调节**，从而在保持交互连贯性的前提下，显著提升个体动作的多样性和可控性。

这一动机的技术直觉在于：自注意力层天然适合建模个体内部的运动依赖，而交叉注意力层适合建模个体间的协调关系。将个体描述注入自注意力、交互描述注入交叉注意力，形成了一种与问题结构高度匹配的条件注入策略。



## 核心方法与创新机理

in2IN 的核心创新在于将**交互生成的条件空间从单一的整体交互描述分解为“整体交互描述 + 个体动作描述”**，并在扩散模型的架构、采样策略和模型组合三个层面围绕这一分解进行了系统性改造。具体而言，其创新体现在以下五个 **changed slots** 上：

### 1. 条件文本的细粒度分解

现有方法（如 **InterGen**、**MoMat-MoGen**）仅使用整体交互描述（例如“两个人握手”）作为生成条件，这导致模型无法区分交互中每个人的具体动作，生成的个体动作缺乏多样性和可控性。in2IN 将条件文本扩展为两部分：**整体交互描述**（用于建模人际动态）和**每个交互个体的个体动作描述**（用于建模个体内动态）。为获得个体描述，作者利用 LLM 为 InterHuman 数据集自动生成了细粒度的个体动作文本标注（Section 1 Introduction）。

### 2. 注意力机制的条件分离注入

in2IN 采用 **Siamese Transformer** 架构（共享参数的两个副本分别处理两个交互个体的噪声运动），并在注意力层中实现了条件注入的分离：
- **自注意力模块**：建模个体内动态，以该个体的**个体动作文本描述**作为条件；
- **交叉注意力模块**：建模个体间动态，以**整体交互文本描述**作为条件，同时接收另一交互个体的自注意力输出和噪声运动。

这一设计（Figure 2）使得模型能够显式区分“我自己的动作”和“我们之间的交互”，从而在保持交互连贯性的同时提升个体动作的精确控制。

### 3. 多权重无分类器引导（Multi-Weight CFG）

标准 CFG 仅使用单一权重对完整条件和无条件输出进行双采样引导。in2IN 提出了**多权重 CFG**，对三个条件分量分别设置独立的引导权重：$w_c$（完整条件）、$w_I$（仅交互条件）、$w_i$（仅个体条件），采样函数为：

$$G^I(x^t, t, c) = G(x^t, t, \emptyset) + w_c \cdot (G(x^t, t, c) - G(x^t, t, \emptyset)) + w_I \cdot (G(x^t, t, c_I) - G(x^t, t, \emptyset)) + w_i \cdot (G(x^t, t, c_i) - G(x^t, t, \emptyset))$$

这使得在推理时可以独立调节交互整体质量和个体动作多样性的权重。消融实验（Figure 4）表明，单独最优权重为 $w_c=4, w_I=4, w_i=2$，而联合最优组合为 $w_c=3, w_I=3, w_i=1$。代价是每个去噪步需要**四重采样**，相比标准 CFG 的双重采样增加了计算开销。

### 4. DualMDM：交互模型与个体先验的组合

in2IN 进一步提出了 **DualMDM** 方法，将交互扩散模型与**单人类运动先验**（在 HumanML3D 上训练）的输出进行组合，以增强个体动作的多样性。其核心公式为：

$$G^{I,i}(x^t, t, c) = G^{\mathrm{I}}(x^t, t, c) + w \cdot (G^{\mathrm{i}}(x^t, t, c_i) - G^{\mathrm{I}}(x_t, t, c))$$

该方法将交互模型 $G^{\mathrm{I}}$ 的输出与个体先验 $G^{\mathrm{i}}$ 的输出按权重 $w$ 混合。与传统恒定权重不同，DualMDM 引入了**时间依赖的权重调度器** $w(t)$，在去噪早期给予个体先验更大权重以注入多样性，后期则回归交互模型以保证连贯性。

### 5. 权重调度器的设计

DualMDM 测试了四种调度函数（Figure 3, Equation 4）：

$$\begin{array}{ll} \mathrm{constant} & w(t) = \lambda \\ \mathrm{linear} & w(t) = t / T \\ \mathrm{exponential} & w(t) = e^{-\lambda \cdot (T - t)} \\ \mathrm{inverse exponential} & w(t) = 1 - e^{-\lambda \cdot (T - t)} \end{array}$$

其中 $t$ 为当前去噪步，$T$ 为总去噪步，$\lambda$ 调节变化速度。实验（Table 2）表明，**指数调度器**（$\lambda=0.00875$）在个体多样性（EID）与交互质量（R-Precision, FID）之间取得了最佳平衡：EID 从 1.238（无 DualMDM）提升至 1.680，同时保持了有竞争力的交互质量指标。

---

**总结**：in2IN 的创新链条是“条件分解 → 架构适配 → 采样策略 → 模型组合”的递进关系。条件分解是因果旋钮，注意力分离注入和多权重 CFG 是架构与采样层面的实现手段，DualMDM 则通过引入外部单人类运动先验进一步放大了个体多样性。这一系列改造使 in2IN 在 InterHuman 数据集上达到 SOTA（R-Precision Top1 0.455, FID 5.177），尤其在个体动作的可控性和多样性上显著超越了仅使用整体交互描述的基线方法。



in2IN 的整体生成流程围绕一个核心设计展开：**将交互条件分解为整体交互描述与个体动作描述，并在扩散模型的注意力机制中分别注入，从而解耦个体内动态与个体间动态**。基于此，论文进一步提出 DualMDM 模型组合方法，将双人交互模型与单人类运动先验融合，以提升个体动作的多样性。

### 输入与条件表示

系统的输入由两类文本描述构成：

- **整体交互描述** $c_I$：描述两人之间的交互行为（如“一个人拥抱另一个人”）。
- **个体动作描述** $c_i$：为交互中的每个个体提供细粒度的动作说明（如“人物A张开双臂向前走”）。这些个体描述通过 LLM 自动为 InterHuman 数据集生成，作为训练时的额外条件。

文本编码器采用冻结的 CLIP-ViTL/14 模型，将上述描述映射为条件嵌入。

### Siamese Transformer 去噪器

核心生成模型是一个基于 Transformer 的扩散模型，采用 **Siamese（孪生）配置**：两个共享参数的 Transformer 副本分别处理交互中两个人的噪声运动输入 $x_a^t$ 和 $x_b^t$，各自输出去噪后的运动 $x_a^0$ 和 $x_b^0$。每个 Transformer 由 8 层多头注意力组成，隐空间维度为 1024，注意力头数为 8。

条件注入通过两种注意力机制实现分工（见 Figure 2）：

![[assets/figures/papers/paper_list_l1707_in2IN_Leveraging_individual_Information_to_Generate_Human_INteractions/figures/002_Figure_2.jpg]]
*Figure 2: in2IN diffusion model. Our proposed architecture consists of a Siamese Transformer that generates the denoised motion of each individual in the interaction*

- **自注意力（Self-Attention）**：建模**个体内动态**。自注意力层仅接收当前人物的噪声运动及其对应的个体动作描述作为条件，捕捉单个人物自身的运动模式。
- **交叉注意力（Cross-Attention）**：建模**个体间动态**。交叉注意力层以整体交互描述为条件，同时接收自注意力的输出以及交互中另一人物的噪声运动，实现两人之间的信息交互与协调。

这种设计使得个体内部的动作连贯性由个体描述驱动，而两人之间的交互协调性由交互描述驱动，从架构层面实现了条件解耦。

### 多权重无分类器引导（Multi-Weight CFG）

在采样阶段，in2IN 引入一种扩展的无分类器引导机制，对三种条件分别赋予独立的引导权重：

$$
G^I(x^t, t, c) = G(x^t, t, \emptyset) + w_c \cdot (G(x^t, t, c) - G(x^t, t, \emptyset)) + w_I \cdot (G(x^t, t, c_I) - G(x^t, t, \emptyset)) + w_i \cdot (G(x^t, t, c_i) - G(x^t, t, \emptyset))
$$

其中 $w_c$ 控制完整条件（交互+个体）的引导强度，$w_I$ 控制仅交互条件的引导强度，$w_i$ 控制仅个体条件的引导强度。通过调节这三个权重，可以在生成时独立控制交互整体质量与个体动作细节的相对重要性。消融实验确定的最优联合权重组合为 $w_c=3$、$w_I=3$、$w_i=1$。

该机制的一个代价是每个去噪步需要**四重采样**（无条件、完整条件、仅交互、仅个体），相比标准 CFG 的双重采样增加了计算开销。

### DualMDM 模型组合

为进一步提升个体动作的多样性，in2IN 引入 DualMDM——一种将交互扩散模型 $G^{\mathrm{I}}$ 与单人类运动先验 $G^{\mathrm{i}}$ 组合的采样方法：

$$
G^{I,i}(x^t, t, c) = G^{\mathrm{I}}(x^t, t, c) + w \cdot (G^{\mathrm{i}}(x^t, t, c_i) - G^{\mathrm{I}}(x_t, t, c))
$$

其中单人类运动先验 $G^{\mathrm{i}}$ 在 HumanML3D 数据集上独立训练，为个体动作提供额外的多样性来源。组合权重 $w$ 不是常数，而是随去噪步 $t$ 变化的**时间依赖调度器** $w(t)$，论文测试了四种调度策略：

$$
\begin{array}{ll} \mathrm{constant} & w(t) = \lambda \\ \mathrm{linear} & w(t) = t / T \\ \mathrm{exponential} & w(t) = e^{-\lambda \cdot (T - t)} \\ \mathrm{inverse exponential} & w(t) = 1 - e^{-\lambda \cdot (T - t)} \end{array}
$$

其中 $T$ 为总去噪步数，$\lambda$ 控制变化速率。实验表明，指数调度器（$\lambda=0.00875$）在个体多样性（EID）与交互质量（R-Precision、FID）之间取得了最佳平衡。

### 整体流程总结

1. 输入整体交互描述与两个个体的个体动作描述，经 CLIP 编码为条件嵌入。
2. Siamese Transformer 在扩散去噪过程中，通过自注意力注入个体条件、交叉注意力注入交互条件，分别生成两人的去噪运动。
3. 采样时采用多权重 CFG，独立调节各条件的引导强度。
4. 可选地，通过 DualMDM 将交互模型输出与单人类运动先验组合，以权重调度器控制个体多样性的注入程度。
5. 最终输出两人的运动序列。



### 3.1 条件分解与注意力注入

in2IN 的核心设计在于将交互生成的条件分解为两个层级：**整体交互描述**（interaction description）和**个体动作描述**（individual description）。这一分解直接映射到模型架构的注意力机制中。

模型采用**孪生 Transformer（Siamese Transformer）** 结构，两个参数共享的副本分别处理交互中每个人的含噪运动序列。每个 Transformer 块内部依次执行：

1. **自注意力（Self-Attention）**：建模个体内动态（intra-personal dynamics），以该个体的文本描述作为条件注入。
2. **交叉注意力（Cross-Attention）**：建模个体间动态（inter-personal dynamics），以整体交互描述作为条件注入，同时接收另一人的含噪运动信息。

这种“自注意力用个体描述、交叉注意力用交互描述”的条件注入策略，使得模型能够同时保持交互的连贯性和个体动作的可控性。

### 3.2 多权重无分类器引导（Multi-Weight CFG）

标准无分类器引导（CFG）仅区分有条件与无条件两个采样路径，无法对交互条件与个体条件进行独立加权。in2IN 提出**多权重 CFG**，引入三个独立的引导权重，分别对应完整条件、仅交互条件和仅个体条件。

采样函数定义为：

$$
G^I(x^t, t, c) = G(x^t, t, \emptyset) + w_c \cdot (G(x^t, t, c) - G(x^t, t, \emptyset)) + w_I \cdot (G(x^t, t, c_I) - G(x^t, t, \emptyset)) + w_i \cdot (G(x^t, t, c_i) - G(x^t, t, \emptyset))
$$

其中：
- $G(x^t, t, \emptyset)$ 为无条件去噪输出；
- $G(x^t, t, c)$ 为完整条件（交互+个体）下的输出；
- $G(x^t, t, c_I)$ 为仅交互条件下的输出；
- $G(x^t, t, c_i)$ 为仅个体条件下的输出；
- $w_c$、$w_I$、$w_i$ 分别控制完整条件、仅交互、仅个体的引导强度。

该公式的直觉是：通过调节三个权重，可以在交互连贯性（由 $w_I$ 主导）与个体多样性（由 $w_i$ 主导）之间进行精细权衡。代价是每个去噪步需进行**四重采样**（quadruple sampling），而非标准 CFG 的双重采样，推理计算量翻倍。

消融实验表明，单独最优权重为 $w_c=4$、$w_I=4$、$w_i=2$，而联合最优组合为 $w_c=3$、$w_I=3$、$w_i=1$（见 Figure 4）。

### 3.3 DualMDM：交互模型与个体先验的组合

为进一步提升个体动作多样性，in2IN 提出 **DualMDM**，将交互扩散模型 $G^{\mathrm{I}}$ 与单人类运动先验 $G^{\mathrm{i}}$ 的输出进行组合。其核心公式为：

$$
G^{I,i}(x^t, t, c) = G^{\mathrm{I}}(x^t, t, c) + w \cdot (G^{\mathrm{i}}(x^t, t, c_i) - G^{\mathrm{I}}(x^t, t, c))
$$

该公式的含义是：以交互模型的输出为基础，按权重 $w$ 叠加个体先验与交互模型之间的残差。当 $w=0$ 时，退化为纯交互模型；当 $w$ 增大时，个体先验的影响增强，个体多样性提升，但可能削弱交互连贯性。

### 3.4 时间依赖的权重调度器

DualMDM 的关键创新在于将恒定权重 $w$ 替换为**时间依赖的权重调度器 $w(t)$**，使组合权重随去噪步数 $t$ 变化。论文测试了四种调度函数（$T$ 为总去噪步数，$\lambda$ 为调节参数）：

$$
\begin{array}{ll} 
\mathrm{constant} & w(t) = \lambda \\ 
\mathrm{linear} & w(t) = t / T \\ 
\mathrm{exponential} & w(t) = e^{-\lambda \cdot (T - t)} \\ 
\mathrm{inverse\ exponential} & w(t) = 1 - e^{-\lambda \cdot (T - t)} 
\end{array}
$$

其中**指数调度器**（exponential）在去噪早期赋予个体先验较大权重以注入多样性，在去噪后期权重衰减以让交互模型主导运动细节的精细化。实验表明，$\lambda=0.00875$ 的指数调度器在个体多样性（EID）与交互质量（R-Precision、FID）之间取得了最佳平衡（见 Table 2）。

### 补充图表

![[assets/figures/papers/paper_list_l1707_in2IN_Leveraging_individual_Information_to_Generate_Human_INteractions/figures/003_Figure_3.jpg]]
*Figure 3: Different weights schedulers tested for DualMDM: Exponential , Inverse Exponential, Constant, and Linear*



## 实验与关键发现

### 主实验结果

in2IN 在 InterHuman 数据集上的人类交互运动生成任务中达到当前最优水平。Table 1 给出了与现有方法的全面定量对比。在文本-运动匹配度指标 R-Precision Top 1 上，in2IN 达到 **0.455**，超越了此前最优方法 MoMat-MoGen（Zhang et al., ICCV 2023）的 0.449，提升幅度为 +0.006。在生成质量指标 FID 上，in2IN 取得 **5.177**，较 MoMat-MoGen 的 5.674 降低了 0.497，表明生成运动的分布更接近真实数据。值得注意的是，当 in2IN 在采样阶段仅使用交互条件权重 $w_I$ 而关闭个体条件时（即退化为仅依赖整体交互描述的生成方式），R-Precision Top 1 降至 0.437，FID 升至 5.423，这从侧面验证了个体动作描述作为额外条件对生成质量的贡献。

![[assets/figures/papers/paper_list_l1707_in2IN_Leveraging_individual_Information_to_Generate_Human_INteractions/figures/005_Table_1.jpg]]
*Table 1: Comparison of our model (in2IN) to the state of the art in human-human interaction motion generation on the InterHuman dataset. *in2IN model only using wI (conditioning only on the interaction during sampling). All evaluations have been executed 10 times to elude the randomness of the generation ± indicates the 95% confidence interval. We highlight the best and the second best results*

与更早的基线方法相比，in2IN 的优势更为显著：TEMOS（Petrovich et al., ECCV 2022）的 R-Precision Top 1 仅为 0.353，T2M（Guo et al., CVPR 2022）为 0.378，MDM（Tevet et al., ICLR 2023）为 0.320，ComMDM（Shafir et al., arXiv 2023）为 0.351，InterGen（Liang et al., arXiv 2023）为 0.423。所有评估均执行 10 次以消除生成随机性的影响，表中报告的 ± 值表示 95% 置信区间。

### 消融研究

#### 多权重 CFG 权重消融

多权重无分类器引导（Multi-Weight CFG）的三个权重 $w_c$（完整条件）、$w_I$（仅交互条件）、$w_i$（仅个体条件）对生成质量有显著且独立的影响。Figure 4 展示了各权重单独消融时对 R-Precision 和 FID 的影响曲线。在隔离测试中（其他权重置零，$w_c$ 消融时 $w_I = w_i = 0$；$w_I$ 和 $w_i$ 消融时 $w_c = 1$ 且另一权重为 0），各权重的单独最优值分别为 $w_c = 4$、$w_I = 4$、$w_i = 2$。

![[assets/figures/papers/paper_list_l1707_in2IN_Leveraging_individual_Information_to_Generate_Human_INteractions/figures/004_Figure_4.jpg]]
*Figure 4: R-Precision and FID for the different weights on the Multi-Weight CFG tested in isolation. Each column ablates a different weight*

然而，联合优化三个权重时，通过验证子集上的网格搜索发现最佳组合为 **$w_c = 3$、$w_I = 3$、$w_i = 1$**。这一组合并非各权重单独最优值的简单叠加，表明权重之间存在交互效应——过高的个体权重 $w_i$ 可能破坏交互的整体连贯性，需要适度调低以维持交互质量与个体多样性之间的平衡。

#### DualMDM 调度器消融

Table 2 对比了四种权重调度器在个体多样性与交互质量之间的权衡表现。新引入的 Extrinsic Individual Diversity（EID）指标衡量生成个体运动集合与真实个体运动集合之间的 Wasserstein 距离差异，数值越高表示个体多样性越丰富。

![[assets/figures/papers/paper_list_l1707_in2IN_Leveraging_individual_Information_to_Generate_Human_INteractions/figures/006_Table_2.jpg]]
*Table 2: EID and interaction metrics of different weight schedulers: Exponential, Inverse Exponential, Constant [36], and Linear. Bold represents the best value for each scheduler*

在恒定、线性、指数和逆指数四种调度器中，**指数调度器**（exponential，$\lambda = 0.00875$）取得了最佳平衡：EID 达到 **1.680**，相较不使用 DualMDM 的 in2IN 基线（$\lambda = 0$，EID = 1.238）提升了 **+0.442**，同时 R-Precision 和 FID 的退化幅度最小。恒定调度器虽在交互质量指标上表现稳定，但 EID 提升有限；线性调度器在去噪后期赋予个体先验过高权重，导致交互连贯性下降；逆指数调度器则因在早期过度依赖个体先验而损害了整体交互结构。

这一结果表明，在去噪过程的早期阶段（$t$ 接近 $T$），交互模型应主导生成以确定交互的整体框架；随着去噪推进，逐步引入个体运动先验的影响可以在不破坏交互结构的前提下丰富个体动作细节。指数调度器天然具备这种“先整体后局部”的权重分配特性，因此优于其他调度策略。

### 失败模式与局限性

尽管 in2IN + DualMDM 在定量指标上表现优异，方法仍存在若干已知局限：

1. **个体描述-运动不对齐风险**：扩展 InterHuman 数据集时使用的 LLM 自动生成个体描述可能产生幻觉，即生成的文本描述与实际运动不完全对应。这会导致模型在训练过程中学到错误的文本-运动映射，削弱个体控制的精度。该问题在复杂交互场景下尤为突出，但论文未提供系统性的对齐错误率分析。

2. **EID 指标缺乏感知验证**：EID 作为个体多样性的代理度量，仅基于运动特征的统计分布差异计算，尚未经过人类感知研究验证。其数值提升是否真正对应人类可感知的个体动作多样性增强，仍是一个开放问题。

3. **推理计算开销增加**：多权重 CFG 需要在每个去噪步进行四重采样（无条件、完整条件、仅交互条件、仅个体条件），而标准 CFG 仅需双重采样。这使推理时间显著增加，在实时或大规模生成场景中可能成为瓶颈。

4. **个体运动先验质量依赖**：DualMDM 的性能受限于所集成的单人类运动先验模型。该先验在 HumanML3D 上训练，与 InterHuman 的标注风格和运动分布可能存在域差异，且其自身生成质量未达到单人类运动生成的最佳水平，限制了组合方法的上限。

5. **仅验证双人交互场景**：当前方法架构专为两人交互设计（Siamese Transformer 的双分支结构），扩展到三人及以上多人交互时，交叉注意力的配对计算复杂度将呈二次增长，且多权重 CFG 的条件组合空间将更加复杂，方法扩展性尚未验证。

### 关键图表结论

**Table 1** 确立了 in2IN 在 InterHuman 数据集上的 SOTA 地位，同时通过消融行（仅使用 $w_I$ 的 in2IN 变体）揭示了个体条件对性能的贡献。

**Table 2** 系统论证了指数调度器在 DualMDM 中的最优性，为时间依赖的模型组合权重设计提供了经验依据。

**Figure 4** 可视化了多权重 CFG 各权重的独立效应，揭示了 $w_i$ 对交互质量的非线性影响——适度的个体引导提升多样性，过强则损害连贯性，这一发现为条件权重的调参提供了直觉指导。



## 定位与知识库关联

### 1. 与现有工作的关系

**in2IN** 的提出建立在双人交互动作生成领域两条主线的交汇点上：一是基于扩散模型的文本到运动生成，二是多人类运动组合技术。

**扩散式交互生成演进。** 早期的文本到运动生成方法如 **TEMOS** (Petrovich et al., ECCV 2022) 和 **T2M** (Guo et al., CVPR 2022) 仅处理单人运动，未涉及交互建模。**MDM** (Tevet et al., ICLR 2023) 将扩散模型引入运动生成，但其原始设计同样面向单人场景。**InterGen** (Liang et al., arXiv 2023) 首次将扩散模型扩展到双人交互生成，而 **MoMat-MoGen** (Zhang et al., ICCV 2023) 作为当前最优基线，在 InterHuman 数据集上建立了性能标杆。in2IN 在 MoMat-MoGen 的基础上实现了超越（R-Precision Top1 从 0.449 提升至 0.455，FID 从 5.674 降至 5.177），其核心改进不在于扩散架构的根本革新，而在于条件空间的分解——将原本单一的整体交互描述拆分为“整体交互 + 个体动作”的双层条件结构。

**模型组合技术的继承与改造。** in2IN 提出的 **DualMDM** 直接继承了 **ComMDM** (Shafir et al., arXiv 2023) 中 DiffusionBlending 的模型组合范式，即通过加权混合两个扩散模型的输出来实现运动合成。关键改造在于两点：其一，将组合对象从“两个单人模型”替换为“交互模型 + 单人运动先验”，使得组合目标从空间拼装转向个体多样性的注入；其二，将恒定的组合权重 $w$ 替换为时间依赖的权重调度器 $w(t)$，使得去噪早期（结构形成阶段）以交互模型为主导、去噪后期（细节丰富阶段）逐步引入个体先验的影响。这一调度策略的引入是 DualMDM 相对于原始 DiffusionBlending 的核心贡献。

**条件注入机制的差异化。** 在注意力层面的条件注入上，in2IN 采用了与现有方法不同的策略：自注意力模块接收个体描述作为条件，负责建模个体内动态（intra-personal dynamics）；交叉注意力模块接收整体交互描述作为条件，负责建模个体间动态（inter-personal dynamics）。这种“自注意力-个体 / 交叉注意力-交互”的分工设计，使得模型能够显式解耦两类信息流，而此前的方法通常将同一文本条件同时注入两个注意力模块，或仅依赖交叉注意力处理交互关系。

### 2. 适用边界

**数据依赖性。** in2IN 的训练和评估均基于 InterHuman 数据集，该数据集提供双人交互运动的 3D 关节点序列及整体交互文本描述。方法的核心前提是能够获取每个个体的细粒度动作描述——论文通过 LLM 自动为 InterHuman 扩展了此类标注。这意味着在缺乏可靠个体描述生成手段的数据集上（如仅有整体标签的交互数据集），in2IN 的完整条件框架难以直接复用。

**交互人数限制。** 当前架构的 Siamese Transformer 设计、自注意力与交叉注意力的分工，以及多权重 CFG 的采样策略，均针对两人交互场景定制。扩展到三人及以上的多人类交互，需要重新设计注意力拓扑（例如，交叉注意力需要处理多对多的个体间关系而非简单的一对一交换），且多权重 CFG 的采样复杂度将随人数线性增长。

**计算开销约束。** 多权重 CFG 要求每个去噪步进行四重采样（无条件、完整条件、仅交互条件、仅个体条件），相比标准 CFG 的双重采样增加了一倍推理计算量。在需要实时或低延迟生成的场景中，这一开销可能构成瓶颈。

**先验质量依赖。** DualMDM 的个体多样性增益依赖于单人运动先验的质量。论文使用的先验模型在 HumanML3D 上训练，其运动风格和标注粒度与 InterHuman 存在域差异。若个体先验本身生成质量不足，DualMDM 的组合效果将受到限制。

### 3. 局限与开放问题

**标注可靠性风险。** 使用 LLM 自动为 InterHuman 生成个体动作描述是方法可行性的关键前提，但这一过程存在幻觉风险——LLM 可能生成与真实运动不对应的描述。论文未报告描述-动作对齐的人工验证结果，这意味着个体控制精度的上限受制于自动标注的质量。开发更可靠的个体描述获取方式（如人工标注或基于多模态信息的自动生成）是提升方法鲁棒性的重要方向。

**个体多样性度量的有效性。** 论文提出的 EID（Extrinsic Individual Diversity）指标定义为生成集与随机采样集之间 Wasserstein 距离的代理度量，但该指标尚未经过人类感知研究的验证。EID 的提升是否真正对应于人类观察者感知到的个体动作多样性增加，目前缺乏定量证据。建立 EID 与人类感知之间的映射关系，是验证方法实际效果的必要步骤。

**调度器参数的自适应选择。** DualMDM 的指数调度器在 $\lambda = 0.00875$ 时取得了最佳平衡，但这一参数是通过网格搜索在验证子集上确定的。对于不同的交互-个体描述组合，最优 $\lambda$ 可能存在差异。如何实现调度器参数的自动、自适应选择（例如基于描述语义复杂度或交互类型的动态调整）是一个开放问题。

**架构扩展性。** 当前 Siamese Transformer 的参数共享策略和交叉注意力的一对一交换设计，难以直接泛化至三人及以上的多人类交互。扩展时需要解决的核心问题包括：如何定义多对多的个体间注意力拓扑，如何在保持参数效率的同时处理可变人数的交互，以及多权重 CFG 的采样策略如何随人数扩展而不导致计算量爆炸。

**推理效率优化。** 四重采样的计算开销可以通过知识蒸馏（将多条件模型蒸馏为单次前向模型）或条件缓存技术（复用无条件输出）来降低，但这些方案在交互生成场景下的可行性和对生成质量的影响尚未被探索。

**先验模型的升级路径。** 论文使用的单人运动先验并非该领域的最优模型（如基于 Transformer VAE 或 MoMask 等更先进的架构）。将更强的单人运动先验集成到 DualMDM 框架中，可能需要解决运动表示不统一（如关节点表示与 SMPL 参数表示之间的转换）和条件空间不兼容等问题。



## 原文 PDF

![[paperPDFs/CVPRW_2024/in2IN_Leveraging_individual_Information_to_Generate_Human_INteractions.pdf]]
