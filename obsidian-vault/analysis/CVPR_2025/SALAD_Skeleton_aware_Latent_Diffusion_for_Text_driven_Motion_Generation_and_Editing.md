---
title: "SALAD: Skeleton-aware Latent Diffusion for Text-driven Motion Generation and Editing"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation_and_Editing.pdf
project_link: https://seokhyeonhong.github.io/projects/salad/
code_link: null
aliases:
- SALAD
tags:
- CVPR_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "骨架-时间结构化潜空间与骨架/时间/交叉注意力机制的联合设计，使得模型能够显式建模关节-帧-词三元交互，并自然地产生可调制的交叉注意力图，从而在提升生成质量和对齐的同时，支持零样本运动编辑。"
primary_logic: "将运动数据分解为骨骼维度和时间维度，并在潜扩散过程中通过独立的注意机制分别处理这些维度及其与文本的细粒度交互，不仅能更准确地捕捉运动语义，还能利用交叉注意力图直接实现文本驱动的零样本运动编辑。"
claims:
- "在HumanML3D数据集上，SALAD取得了SOTA的文本-运动对齐（Top-3 R-Precision 0.857）和生成质量（FID 0.076），优于ReMoDiffuse和MoMask等先前最佳方法。"
- "消融实验表明，同时移除骨架-时间潜变量（ST-Latent）和交叉注意力（Cross-Attention）后，R-Precision从0.857降至0.752，FID从0.076升至0.345，验证了两个核心组件对生成质量和文本对齐的关键作用。"
- "交叉注意力图可视化表明，模型能够自动捕捉文本中特定词汇（如'jumping'）与相应身体部位及时间帧的对应关系。"
- "用户研究显示，SALAD的零样本编辑结果在保持原作、语义对齐和整体质量上均显著优于MDM和MotionFix，总体质量评分4.596。"
---

# SALAD: Skeleton-aware Latent Diffusion for Text-driven Motion Generation and Editing

> [!tip] 核心洞察
> 将运动数据分解为骨骼维度和时间维度，并在潜扩散过程中通过独立的注意机制分别处理这些维度及其与文本的细粒度交互，不仅能更准确地捕捉运动语义，还能利用交叉注意力图直接实现文本驱动的零样本运动编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | SALAD：面向文本驱动运动生成与编辑的骨骼感知潜扩散模型 |
| 英文题名 | SALAD: Skeleton-aware Latent Diffusion for Text-driven Motion Generation and Editing |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2503.13836) · [Project](https://seokhyeonhong.github.io/projects/salad/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | SALAD |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top-3 ↑ 为 0.857 ± 0.002，对比 0.795 ± 0.004 (ReMoDiffuse)，变化 +0.062。
> - HumanML3D 上，FID ↓ 为 0.076 ± 0.002，对比 0.103 ± 0.004 (ReMoDiffuse)，变化 -0.027。
> - HumanML3D 上，MM-Dist ↓ 为 2.649 ± 0.009，对比 2.974 ± 0.016 (ReMoDiffuse)，变化 -0.325。

## 概要

文本驱动的三维人体运动生成旨在根据自然语言描述合成逼真的运动序列，在动画、游戏、虚拟现实等领域具有广泛应用。然而，现有方法普遍存在一个关键瓶颈：它们将运动姿态视为单一向量，并将文本压缩为单一特征向量，忽视了骨骼关节、时间帧和文本词之间的复杂交互关系。这种粗粒度的建模方式导致生成细节丢失，且无法利用预训练模型直接进行零样本编辑。

针对上述问题，本文提出 **SALAD**（Skeleton-aware Latent Diffusion），一种骨骼感知的潜扩散模型。其核心思路是将运动数据分解为骨骼维度和时间维度，并在潜扩散过程中通过独立的注意力机制分别处理这些维度及其与文本的细粒度交互。具体而言，SALAD 首先训练一个骨骼-时间变分自编码器（VAE），将运动序列映射到结构化的潜空间；随后在该潜空间上训练一个由时间注意力、骨骼注意力和交叉注意力组成的 Transformer 去噪器，显式建模关节-帧-词三元交互。这一设计不仅提升了生成质量和文本对齐，还自然地产生了可调制的交叉注意力图，从而支持零样本文本驱动运动编辑。

在 HumanML3D 和 KIT-ML 两个标准基准上的实验表明，SALAD 在文本-运动对齐和生成质量上均达到最优水平。在 HumanML3D 上，其 R-Precision Top-3 达到 0.857，FID 降至 0.076，显著优于 ReMoDiffuse 和 MoMask 等先前最佳方法。消融实验验证了骨骼-时间潜变量和交叉注意力机制对性能的关键贡献。用户研究进一步表明，SALAD 的零样本编辑结果在保持原作、语义对齐和整体质量上均显著优于 MDM 和 MotionFix 等基线方法。

文本驱动的三维人体运动生成旨在根据自然语言描述合成逼真的人体运动序列，在动画制作、游戏开发和人机交互等领域具有广泛应用。近年来，基于扩散模型的运动生成方法取得了显著进展，代表性工作包括**MDM**（Tevet et al.）将扩散模型引入运动生成、**MLD**（Chen et al.）提出潜扩散框架以提升效率、**MotionDiffuse**（Zhang et al.）实现细粒度文本控制，以及**ReMoDiffuse**（Zhang et al.）通过检索增强机制进一步提升了生成质量。然而，这些方法在运动表示和文本条件机制上存在一个共同的结构性缺陷。

### 现有方法的核心瓶颈

现有方法普遍将运动姿态视为单一向量，并将文本描述压缩为全局特征向量，这种做法忽视了运动生成中三类关键元素之间的复杂交互关系：**骨骼关节**（身体各部位的空间结构）、**时间帧**（运动的时序动态）和**文本词**（语义的细粒度描述）。具体而言：

1. **运动表示的扁平化**：将每帧姿态编码为单一向量，无法显式区分不同身体部位（如手臂、腿部、躯干）的独立运动特性。这导致模型难以捕捉“左手举起而右手保持下垂”这类涉及局部关节的精细语义。

2. **文本条件的全局化**：使用单一的句子级嵌入作为条件信号，丢失了词级语义与具体身体部位及时间帧之间的细粒度对应关系。例如，“先走路然后跳跃”中的时序逻辑和动作切换点无法被有效建模。

3. **编辑能力的缺失**：由于缺乏关节-帧-词之间的显式交互建模，预训练的扩散模型无法直接用于零样本运动编辑，通常需要额外的优化、掩码标注或微调步骤。

### 本文的核心洞察与动机

针对上述瓶颈，本文提出**SALAD**（Skeleton-aware Latent Diffusion），其核心洞察是：**将运动数据分解为骨骼维度和时间维度，并在潜扩散过程中通过独立的注意机制分别处理这些维度及其与文本的细粒度交互，不仅能更准确地捕捉运动语义，还能利用交叉注意力图直接实现文本驱动的零样本运动编辑**。

这一设计带来了三个关键突破：

- **骨架-时间结构化潜空间**：通过变分自编码器（VAE）将运动序列编码为解耦的骨架-时间潜变量，显式保留关节拓扑和时间动态信息。
- **三元交互建模**：在去噪Transformer中引入独立的时间注意力（TempAttn）、骨骼注意力（SkelAttn）和交叉注意力（CrossAttn）模块，分别建模帧间依赖、关节间依赖以及词-关节-帧的细粒度对齐。
- **零样本编辑能力**：训练完成后，交叉注意力图自然地编码了文本词与身体部位及时间帧的对应关系。通过调制这些注意力图（如词交换、注意力重加权、注意力镜像），无需任何额外训练即可实现文本驱动的运动编辑。

## 核心方法与创新机理

SALAD 的核心创新在于将运动生成从“整体姿态-全局文本”的粗粒度建模，推进到“关节-帧-词”三元交互的细粒度建模。这一转变通过三个相互协同的 **changed slots** 实现，共同构成了方法的因果开关（causal knob）。

### 1. 骨架-时间结构化潜空间（Motion Representation）

现有方法（如 **MDM**、**MLD**）将每一帧的姿态编码为单一向量，完全忽视了人体骨骼的拓扑结构。SALAD 通过骨架-时间变分自编码器（VAE）构建了一个解耦的潜空间，其核心操作是 **骨架-时间卷积（STConv）** 和 **骨架-时间池化（STPool）**：

$$
\mathrm{STConv}(\mathbf{h}) := \mathrm{SkelConv}(\mathbf{h}) + \mathrm{TempConv}(\mathbf{h})
$$

$$
\mathrm{STPool}(\mathbf{h}) := \mathrm{TempPool}(\mathrm{SkelPool}(\mathbf{h}))
$$

其中，SkelConv 在关节维度上进行图卷积以捕获空间拓扑关系，TempConv 在时间维度上进行 1D 卷积以捕获时序动态，两者相加实现了维度解耦但信息互补的特征提取。STPool 则先对关节池化保留拓扑，再对时间池化，从而在降低维度的同时维持结构完整性。这一设计使得潜变量天然具备“哪个关节、在何时”的结构化语义，为后续的细粒度注意力交互提供了基础。

### 2. 关节/时间/交叉三重注意力机制（Denoising Transformer Design）

传统方法（如 **ReMoDiffuse**）的去噪网络仅使用时间自注意力，文本条件通常以全局句子嵌入拼接的方式注入，无法建模词与身体部位的对应关系。SALAD 的去噪 Transformer 块包含三个独立的注意力模块：

- **时间注意力（TempAttn）**：捕获同一关节在不同时间帧之间的依赖关系。
- **骨骼注意力（SkelAttn）**：捕获同一时间帧内不同关节之间的空间依赖关系。
- **交叉注意力（CrossAttn）**：以冻结 CLIP 文本编码器提供的词级特征为条件，通过交叉注意力将文本语义细粒度地注入运动潜变量：

$$
\mathbf{z}_t^l \gets \mathbf{z}_t^l + \mathrm{FiLM}(\mathrm{CrossAttn}(\mathrm{LN}(\mathbf{z}_t^l), \mathrm{CLIP}(c)))
$$

每个模块后均接有 FiLM 层，根据扩散时间步进行特征调制。这种显式分离的设计，使模型能够同时学习“何时动哪个关节”与“哪个词控制哪个部位”的复杂映射关系。消融实验证实，同时移除 ST-Latent 和 Cross-Attention 后，R-Precision 从 0.857 骤降至 0.752，FID 从 0.076 飙升至 0.345（Table 3），验证了这两个组件对生成质量和文本对齐的关键作用。

### 3. 零样本运动编辑的交叉注意力调制（Zero-shot Editing Approach）

现有运动编辑方法（如 **MDM**、**MotionFix**）通常需要手动指定编辑掩码、额外的优化过程或微调。SALAD 的核心洞察在于：由于交叉注意力图直接编码了文本词与运动关节/帧之间的对应关系，通过调制这些注意力图即可实现零样本文本驱动的运动编辑，无需任何训练。具体支持四种编辑操作：

- **词交换（Word Swap）**：将源文本词对应的注意力图替换为目标词对应的注意力图。
- **提示细化（Prompt Refinement）**：在提示中添加新词，将其注意力图与原注意力图融合。
- **注意力重加权（Attention Re-weighting）**：放大或抑制特定词的注意力强度。
- **注意力镜像（Attention Mirroring）**：利用预定义的对称关节映射，将一侧关节的注意力值交换到镜像关节：

$$
(\operatorname{Edit}(\mathbf{M}_t, \mathbf{M}_t^*, t))_{i,j,k} := (\mathbf{M}_t)_{i, \mathcal{C}(j), k}
$$

用户研究（Table 4）表明，SALAD 的零样本编辑结果在保持原作、语义对齐和整体质量上均显著优于 MDM 和 MotionFix，总体质量评分达 4.596。交叉注意力图可视化（Figure 6 / Appendix Figure 3）进一步证实，模型能够自动捕捉文本中特定词汇（如 "jumping"）与相应身体部位及时间帧的对应关系，为编辑的可解释性提供了直观支撑。

### 4. 辅助创新：v-预测参数化（Diffusion Parametrization）

SALAD 采用 v-预测（velocity prediction）替代传统的 ε-预测或 x-预测：

$$
\mathbf{v}_t = \alpha_t \epsilon - \sigma_t \mathbf{x}
$$

这一参数化结合了噪声和干净样本的信息，在高噪声阶段具有更好的稳定性。消融实验（Appendix Table 2）表明，v-预测在 HumanML3D 上取得了更低的 FID（0.076）和更好的 MM-Dist，验证了其在运动扩散模型中的优势。

SALAD 的整体 pipeline 由三个核心阶段构成：**骨骼感知的变分自编码器（VAE）构建结构化潜空间**、**骨架-时间感知的潜扩散模型进行条件生成**、以及**基于交叉注意力调制的零样本运动编辑**。

### 阶段一：骨骼感知的潜空间构建

首先，一个 VAE 将原始运动序列映射到一个解耦了**空间（骨骼关节）**与**时间（帧）**维度的结构化潜空间。该 VAE 的编码器通过堆叠的骨架-时间卷积层（STConv）和骨架-时间池化层（STPool）逐步压缩运动特征，得到潜变量；解码器则通过对应的上采样层（STUnpool 和 STConv）从潜变量重建运动特征。这一设计使得潜空间本身即具备对骨骼拓扑和时间动态的感知能力，为后续扩散模型提供了结构化的生成空间。

### 阶段二：骨架-时间感知的潜扩散生成

在冻结的 VAE 潜空间之上，SALAD 训练一个潜扩散模型来实现文本到运动的生成。去噪器是一个 Transformer，其每一层由四个子模块顺序组成：**时间自注意力（TempAttn）**、**骨骼自注意力（SkelAttn）**、**交叉注意力（CrossAttn）** 和前馈网络（FFN）。时间自注意力和骨骼自注意力分别在时间维度和关节维度上建模长程依赖，交叉注意力则将冻结的 CLIP 文本编码器提供的词级特征融入运动潜变量。每个注意力子模块后均跟有 FiLM 层，根据扩散时间步进行特征调制。扩散过程采用 **v-prediction（速度预测）** 参数化，并在推理时结合无分类器引导（classifier-free guidance）来平衡生成质量与文本对齐。

### 阶段三：零样本运动编辑

SALAD 的交叉注意力机制自然地产生了文本词与运动关节/时间帧之间的细粒度对齐图。基于此，SALAD 在**无需任何额外训练或优化**的前提下，通过对生成过程中的交叉注意力图进行调制，实现了四种零样本文本驱动运动编辑操作：**词交换（word swap）**、**提示细化（prompt refinement）**、**注意力重加权（attention re-weighting）** 和**注意力镜像（attention mirroring）**。这种设计使得预训练的 SALAD 模型可直接用于编辑任务，无需引入额外的编辑模块或微调步骤。

### 输入输出流

- **输入**：文本描述（自然语言句子）。
- **文本编码**：冻结的 CLIP 文本编码器提取词级特征，作为交叉注意力的条件信号。
- **VAE 编码**：训练时将真实运动序列编码为骨架-时间结构化潜变量；推理时从随机噪声开始迭代去噪。
- **扩散去噪**：骨架-时间感知 Transformer 在潜空间中进行多步去噪，每步均通过时间、骨骼和交叉注意力联合建模关节-帧-词三元交互。
- **VAE 解码**：去噪后的潜变量经 VAE 解码器重建为运动特征序列，再转换为关节旋转或位置表示。
- **输出**：与输入文本语义对齐的 3D 人体运动序列。

### 补充图表

![[assets/figures/papers/paper_list_l20_SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation/figures/001_Figure_1.jpg]]
*Figure 1: Architecture of the skeleto-temporal VAE network. The encoder maps motion features into a skeleto-temporal latent space, and the decoder restores the skeleto-temporal latent variables into motion features*

### 骨架-时间变分自编码器（VAE）

SALAD的核心创新始于一个骨架感知的运动潜空间构建。传统方法将运动姿态视为单一向量，忽视了骨骼关节与时间帧之间的结构关系。SALAD通过骨架-时间卷积（STConv）和骨架-时间池化（STPool）操作，显式地将关节维度和时间维度解耦，构建了一个结构化的潜空间。

**骨架-时间卷积（STConv）** 将关节维度的图卷积与时间维度的1D卷积相加，使信息在相邻关节和相邻帧之间同时流动：

$$
\mathrm{STConv}(\mathbf{h}) := \mathrm{SkelConv}(\mathbf{h}) + \mathrm{TempConv}(\mathbf{h})
$$

其中 $\mathrm{SkelConv}$ 在关节维度上执行图卷积以捕捉骨骼拓扑关系，$\mathrm{TempConv}$ 在时间维度上执行1D卷积以捕捉时序动态。两者解耦但并行，避免了将关节-时间耦合为单一维度的信息混淆。

**骨架-时间池化（STPool）** 在编码器中逐步降低潜空间维度，先在关节维度上池化以保留骨骼拓扑，后在时间维度上池化：

$$
\mathrm{STPool}(\mathbf{h}) := \mathrm{TempPool}(\mathrm{SkelPool}(\mathbf{h}))
$$

这种先关节后时间的池化顺序确保了骨骼结构信息在降维过程中的保真度。

**VAE训练目标** 由四项损失组成，兼顾重建精度与潜空间正则化：

$$
\mathcal{L}_{\mathrm{VAE}} = \mathcal{L}_{\mathrm{m}} + \lambda_{\mathrm{pos}} \mathcal{L}_{\mathrm{pos}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}} + \lambda_{\mathrm{kl}} \mathcal{L}_{\mathrm{kl}}
$$

其中 $\mathcal{L}_{\mathrm{m}}$ 为运动特征的L1重建损失，$\mathcal{L}_{\mathrm{pos}}$ 和 $\mathcal{L}_{\mathrm{vel}}$ 分别为关节位置和关节速度的辅助L1损失，$\mathcal{L}_{\mathrm{kl}}$ 为KL散度正则化项。消融实验（Appendix C.5, Table 4）表明，移除位置和速度辅助损失后，FID从0.003升至0.012，MPJPE从0.016升至0.024，验证了这两项损失对重建质量的关键作用。

### 骨架感知去噪器

在潜空间中，SALAD的去噪器通过堆叠的Transformer块对扩散过程中的噪声潜变量进行去噪。每个Transformer块由四个核心组件构成：时间注意力（TempAttn）、骨骼注意力（SkelAttn）、交叉注意力（CrossAttn）和前馈网络（FFN），且每个模块后均跟随FiLM层进行扩散时间步的条件调制。

**交叉注意力机制** 将CLIP编码的词级文本特征融入运动潜变量，实现细粒度的文本-运动对齐：

$$
\mathbf{z}_t^l \gets \mathbf{z}_t^l + \mathrm{FiLM}(\mathrm{CrossAttn}(\mathrm{LN}(\mathbf{z}_t^l), \mathrm{CLIP}(c)))
$$

其中 $\mathbf{z}_t^l$ 为第 $l$ 层的潜变量，$\mathrm{LN}$ 为层归一化，$\mathrm{CLIP}(c)$ 为文本 $c$ 的词级特征，$\mathrm{FiLM}$ 根据扩散时间步 $t$ 进行特征调制。这一设计使得模型能够自动学习文本中特定词汇与对应身体部位及时间帧的关联（见Figure 6的注意力图可视化）。

### 扩散参数化与采样

SALAD采用**v-prediction（速度预测）**参数化，而非传统的 $\epsilon$-prediction或 $x$-prediction：

$$
\mathbf{v}_t = \alpha_t \epsilon - \sigma_t \mathbf{x}
$$

其中 $\epsilon$ 为噪声，$\mathbf{x}$ 为干净样本，$\alpha_t$ 和 $\sigma_t$ 为扩散调度系数。消融实验（Appendix C.3, Table 2）表明，v-prediction在HumanML3D上取得了更低的FID（0.076）和更好的MM-Dist，验证了速度预测在高噪声阶段的稳定性优势。

采样时，SALAD使用**无分类器引导（Classifier-Free Guidance）**来平衡文本条件与无条件预测：

$$
\hat{\mathbf{v}}_\theta(\mathbf{z}_t, t, c) := \mathbf{v}_\theta(\mathbf{z}_t, t, \emptyset) + w \left( \mathbf{v}_\theta(\mathbf{z}_t, t, c) - \mathbf{v}_\theta(\mathbf{z}_t, t, \emptyset) \right)
$$

其中 $w$ 为引导强度，控制文本条件对生成过程的影响程度。Figure 5的消融实验展示了不同 $w$ 值下FID与R-Precision的权衡关系。

### 零样本编辑的注意力调制

SALAD的交叉注意力图天然编码了文本词与骨骼关节、时间帧的对应关系，使得零样本文本驱动运动编辑成为可能。其中**注意力镜像（Attention Mirroring）**操作用于对称身体部位的编辑，通过交换关节 $j$ 与其镜像关节 $\mathcal{C}(j)$ 的注意力值实现：

$$
(\operatorname{Edit}(\mathbf{M}_t, \mathbf{M}_t^*, t))_{i,j,k} := (\mathbf{M}_t)_{i, \mathcal{C}(j), k}
$$

该操作无需额外训练或优化，仅通过修改生成过程中的交叉注意力图即可实现编辑，是SALAD区别于MDM、MotionFix等需要手动掩码或微调的编辑方法的核心优势。

## 实验与关键发现

### 主实验结果

SALAD 在两个主流文本驱动运动生成基准上进行了评估，并与多个代表性方法进行了全面比较。**Table 1** 展示了在 HumanML3D 和 KIT-ML 测试集上的定量结果。

![[assets/figures/papers/paper_list_l20_SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation results on the test sets of HumanML3D (top) and KIT-ML (bottom). ↑ and ↓ denote that higher and lower values are better, respectively, while → denotes that the values closer to the real motion are better. Methods above the dotted line are auto-regressive models based on VAE or VQ-VAE, while those below are diffusion-based generative models. Red and blue colors indicate the best and the second best results, respectively*

![[assets/figures/papers/paper_list_l20_SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation/figures/015_Table_1.jpg]]
*Table 1: Quantitative evaluation results with different CFG weight values on the test sets of HumanML3D (top) and KIT-ML (bottom). ↑ and ↓ denote that higher and lower values are better, respectively, while → denotes that the values closer to the real motion are better. Red and blue colors indicate the best and the second best results, respectively*

在 **HumanML3D** 数据集上，SALAD 在文本-运动对齐和生成质量两个核心维度均取得了最优或次优结果：

- **文本-运动对齐**：Top-3 R-Precision 达到 **0.857 ± 0.002**，显著优于此前最佳的 ReMoDiffuse（0.795 ± 0.004），提升幅度达 +0.062。这表明骨骼感知的交叉注意力机制能更精确地将文本语义映射到对应的身体部位和时间帧。
- **生成质量**：FID 降至 **0.076 ± 0.002**，优于 ReMoDiffuse 的 0.103 ± 0.004 和 MoMask 的 0.083，在扩散类方法中排名第一。MM-Dist 同样取得最优（2.649），进一步验证了生成运动与文本描述的整体一致性。
- **多样性**：Diversity 指标（9.679）接近真实数据分布（9.503），MultiModality 为 2.793，表明模型在保持高对齐精度的同时并未牺牲生成多样性。

在 **KIT-ML** 数据集上，SALAD 的 Top-3 R-Precision（0.810）和 MM-Dist（2.460）均为最优，但 FID（0.296）高于 ReMoDiffuse（0.155）和 MoMask（0.204），说明在小规模数据集上的生成质量仍有提升空间。

**定性对比**（**Figure 4**）显示，当输入文本包含多个动作描述（如"人向前走，然后转身，最后坐下"）时，MDM 和 MoMask 往往遗漏部分动作，而 SALAD 能完整呈现所有文本指定的动作序列，验证了骨骼-时间-文本三元交互建模的有效性。

### 消融实验

**Table 3** 对 SALAD 的两个核心组件进行了消融分析：

| 消融设置 | R-Precision Top-3 ↑ | FID ↓ |
|---------|-------------------|------|
| 完整 SALAD | 0.857 | 0.076 |
| 移除 ST-Latent | 0.821 | 0.218 |
| 移除 Cross-Attention | 0.811 | 0.159 |
| 同时移除两者 | 0.752 | 0.345 |

同时移除骨架-时间潜变量（ST-Latent）和交叉注意力（Cross-Attention）后，R-Precision 从 0.857 骤降至 0.752，FID 从 0.076 恶化至 0.345，降幅分别达 12.3% 和 354%。单独移除任一组件的性能退化也显著，证实了两个模块对生成质量和文本对齐的关键作用——ST-Latent 提供了结构化的运动表示，Cross-Attention 实现了细粒度的文本-运动交互。

**扩散参数化**（Appendix Table 2）的消融表明，v-prediction 参数化（FID 0.076）优于 x-prediction（FID 0.089）和 ε-prediction（FID 0.085），验证了速度预测在高噪声扩散阶段提供更稳定训练信号的假设。

**FiLM 层**（Appendix Table 3）：移除基于扩散时间步的 FiLM 调制后，HumanML3D 上 FID 从 0.076 升至 0.087，R-Precision 同步下降，表明时间步条件特征调制对生成质量有正向贡献。

**VAE 辅助损失**（Appendix Table 4）：关节位置和速度的 L1 重构损失对运动重建质量至关重要——移除后 FID 从 0.003 升至 0.012，MPJPE 从 0.016 升至 0.024，证实了在潜空间之外引入显式运动学约束的必要性。

**CFG 权重**（**Figure 5**）：无分类器引导权重 w 在 2.5-3.5 范围内取得最佳 FID-R-Precision 权衡，过高权重会导致多样性下降和生成伪影。

### 交叉注意力可解释性

**Figure 6** 和 Appendix Figure 3 对交叉注意力图进行了可视化。每行对应一个身体部位（如左臂、右腿），每列代表时间帧，注意力强度反映文本词与运动区域的关联程度。结果表明：

- 当文本包含"jumping"时，腿部和足部关节在跳跃发生的时间帧上呈现高注意力响应。
- "waving hand"激活手臂关节的注意力，且左右手响应与文本描述一致。
- 注意力图呈现稀疏且有结构的特点，表明模型自动习得了文本词-身体部位-时间帧的细粒度对齐，无需显式监督。

这种可解释的交叉注意力图是后续零样本编辑能力的基础。

### 零样本运动编辑评估

**Table 4** 报告了用户研究结果，比较 SALAD 与 MDM 和 MotionFix 在三个编辑维度上的表现（5分制）：

| 方法 | 原作保持 ↑ | 语义对齐 ↑ | 整体质量 ↑ |
|-----|-----------|-----------|-----------|
| MDM | 3.698 | 3.723 | 3.648 |
| MotionFix | 3.923 | 4.118 | 3.967 |
| SALAD | **4.612** | **4.584** | **4.596** |

SALAD 在所有维度上均显著优于基线方法，整体质量评分 4.596。**Figure 7** 展示了四种注意力调制编辑策略的定性效果：词交换（如将"walk"替换为"run"）、提示细化（添加"quickly"等副词）、注意力重加权（增强特定词的注意力强度）和注意力镜像（对称身体部位的动作迁移）。编辑结果在保持未编辑部分不变的同时，精确修改了目标动作属性，无需任何微调或优化步骤。

### 失败模式与局限

1. **小数据集生成质量**：在 KIT-ML 上 FID（0.296）落后于 ReMoDiffuse（0.155），表明骨骼感知建模的优势在数据量不足时可能被检索增强等方法抵消。
2. **真实运动编辑**：当前编辑能力仅限于生成运动，对真实运动序列的编辑需要额外的扩散反演步骤，尚未实现端到端支持。
3. **骨骼拓扑泛化**：STConv 和 STPool 的图结构假设与训练数据拓扑一致，扩展到不同关节数量的非人形骨架需要重新设计骨骼池化层次。
4. **对称编辑灵活性**：注意力镜像依赖预定义的对称关节映射，无法处理非标准对称关系或用户自定义的关节对应。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|---------|
| Table 1 | HumanML3D 上 R-Precision 0.857、FID 0.076，全面超越此前 SOTA |
| Figure 4 | SALAD 能完整呈现多动作文本序列，基线方法常遗漏动作 |
| Table 3 | ST-Latent + Cross-Attention 联合移除导致 FID 恶化 354% |
| Figure 6 | 交叉注意力图自动捕捉文本词-身体部位-时间帧的细粒度对齐 |
| Table 4 | 零样本编辑整体质量 4.596/5，显著优于 MDM 和 MotionFix |

![[assets/figures/papers/paper_list_l20_SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation/figures/008_Table_2.jpg]]
*Table 2: Quantitative results on the quality and accuracy of reconstructed motion features of VAE models from different methods, along with the number of trainable parameters, measured on the test set of HumanML3D. Table 3. Ablation studies on the VAE and denoiser*

![[assets/figures/papers/paper_list_l20_SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation/figures/011_Table_4.jpg]]
*Table 4: User study results. The red color indicates the best result. grained control in both generation and editing*

![[assets/figures/papers/paper_list_l20_SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation/figures/017_Table_3.jpg]]
*Table 3: Ablation results showing the effect of FiLM layers on the test sets of HumanML3D (top) and KIT-ML (bottom)*

![[assets/figures/papers/paper_list_l20_SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation/figures/018_Table_4.jpg]]
*Table 4: Ablation results showing the effect of FiLM layers on the test sets of HumanML3D (top) and KIT-ML (bottom)*

### 补充图表

![[assets/figures/papers/paper_list_l20_SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation/figures/007_Table.jpg]]

![[assets/figures/papers/paper_list_l20_SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation/figures/016_Table_2.jpg]]
*Table 2: Quantitative results on different diffusion parametrizations*

## 定位与知识库关联

### 与既有方法的谱系关系

SALAD 处于文本驱动运动生成（Text-to-Motion）从单一向量表征走向结构化潜空间建模的关键转折点。其方法谱系可沿两条主线追溯。

**运动表征的演化**：早期工作如 **T2M** 将运动姿态压缩为单一向量，依赖自回归 VAE 框架生成序列。**AttT2M** 和 **ParCo** 分别引入骨架感知和部位感知的 VQ-VAE，开始关注运动的结构化分解，但仍将文本压缩为全局特征向量。**MoMask** 进一步用掩码 Transformer 提升生成质量，但同样未在文本-运动交互层面进行细粒度建模。SALAD 的关键突破在于将运动表征显式分解为骨骼维度和时间维度，构建骨架-时间结构化潜空间，使关节、帧和文本词三者之间的细粒度交互成为可能。

**扩散模型的引入**：**MDM** 率先将扩散模型用于运动生成，直接对原始运动数据进行去噪。**MLD** 将扩散过程迁移到潜空间以提升效率，但其潜空间仍为单一向量。**MotionDiffuse** 和 **ReMoDiffuse** 分别在细粒度控制和检索增强方面做出贡献，ReMoDiffuse 在 HumanML3D 上取得了此前的 SOTA 结果（Top-3 R-Precision 0.795, FID 0.103）。SALAD 在潜扩散框架的基础上，通过骨架-时间-文本三元注意力机制和 v-prediction 参数化，将文本-运动对齐和生成质量同时推至新高。

**零样本编辑的新范式**：在运动编辑领域，**MDM** 和 **MotionFix** 等基线依赖手动掩码、优化或微调。SALAD 首次利用预训练扩散模型中自然产生的交叉注意力图，通过词交换、提示细化、注意力重加权和注意力镜像四种调制策略，实现完全无需训练的零样本文本驱动编辑。这一思路与图像生成领域 Prompt-to-Prompt 的注意力操控范式一脉相承，但在运动生成领域属首次系统性应用。

### 适用边界

SALAD 的设计假设与训练数据中的骨骼拓扑一致，因此**直接适用于人形骨架的运动生成与编辑**。在 HumanML3D 和 KIT-ML 两个标准数据集上，其生成质量和文本对齐均达到或接近最优水平。

然而，以下边界条件需注意：
- **骨骼拓扑依赖性**：当前骨骼池化策略基于预定义的关节邻接关系，无法直接泛化到具有不同关节数量或连接方式的非人形骨架（如四足动物、多足机器人）。
- **数据集规模敏感性**：在 KIT-ML（约 3,911 条运动）上的 FID 为 0.296，仍高于 ReMoDiffuse 的 0.155，表明小数据集上的生成质量尚有提升空间。
- **编辑范围限制**：零样本编辑仅适用于生成的运动序列，对真实运动捕获数据的编辑需要额外的扩散反演步骤，该能力尚未实现。
- **对称编辑的刚性**：注意力镜像依赖预定义的对称关节映射表，无法灵活处理非对称或部分对称的编辑需求。

### 局限与开放问题

**已识别的局限**：
1. 真实运动编辑的缺失：SALAD 的注意力调制编辑仅作用于从噪声生成的合成运动，对真实运动序列的编辑需引入反演机制，当前框架未包含此能力。
2. 小数据集性能差距：KIT-ML 上 FID 未达最优，可能源于骨架-时间潜空间的表达能力在小样本下未能充分释放，或 VAE 重建质量受数据量限制。
3. 多样性权衡：SALAD 在追求高文本对齐和生成质量的同时，Diversity 和 MultiModality 指标并非全面领先，提示存在对齐-多样性权衡（alignment-diversity trade-off）。
4. 骨骼通用性不足：STPool 中的骨骼池化操作依赖特定拓扑，限制了跨骨骼类型的迁移。

**值得探索的开放问题**：
1. **对齐-多样性平衡**：如何在保持 0.857 R-Precision 和 0.076 FID 的同时，进一步提升生成运动的多样性和多模态覆盖，是文本驱动生成领域的共性挑战。
2. **多角色与人群扩展**：SALAD 的骨架-时间-文本三元交互框架能否自然扩展到多角色交互、人群动画甚至更长文本序列的描述，需要验证。
3. **真实运动编辑的反演路径**：将 DDIM 反演或基于优化的反演方法引入 SALAD 框架，以实现对真实运动捕获数据的零样本编辑，具有显著的应用价值。
4. **注意力图的可解释性挖掘**：交叉注意力图已展示出文本词与身体部位/时间帧的对应关系，能否利用这一可解释性自动发现文本-运动的新关联，或引导更复杂的组合式编辑操作？
5. **跨骨骼泛化**：通过图神经网络或动态骨骼池化策略，使 SALAD 适应任意骨骼拓扑，将显著扩展其应用场景至机器人运动规划、动物动画等领域。

### 知识库定位

SALAD 在文本驱动运动生成领域的方法论贡献可归纳为三点，构成其知识库定位的核心坐标：

1. **结构化潜空间设计范式**：将运动表征从单一向量解耦为骨架-时间张量，为后续工作提供了“维度解耦 + 结构化注意力”的模板。
2. **注意力驱动的零样本编辑**：首次证明扩散模型中的交叉注意力图可直接用于运动编辑，为运动编辑领域开辟了无需训练的新路径。
3. **v-prediction 在运动扩散中的验证**：消融实验证实 v-prediction 参数化在运动生成中优于传统的 x-prediction 和 ε-prediction，为运动扩散模型的参数化选择提供了经验依据。

该工作适合作为文本驱动运动生成、运动编辑、以及扩散模型结构化应用的参考文献，尤其对关注骨骼感知建模和零样本操控的研究者具有参考价值。

## 原文 PDF

![[paperPDFs/CVPR_2025/SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation_and_Editing.pdf]]
