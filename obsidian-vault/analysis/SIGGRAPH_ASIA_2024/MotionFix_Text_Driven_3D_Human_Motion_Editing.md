---
title: "MotionFix: Text-Driven 3D Human Motion Editing"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2024/MotionFix_Text_Driven_3D_Human_Motion_Editing.pdf
paper_link: https://arxiv.org/abs/2408.00712
project_link: https://motionfix.is.tue.mpg.de
aliases:
- TTDMEDM
- MotionFix
tags:
- SIGGRAPH_ASIA_2024
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "引入半自动收集的 MotionFix 三元组数据集，以训练条件扩散模型 TMED，该模型同时以源运动和编辑文本为条件。"
primary_logic: "利用 TMR 嵌入空间检索相似运动对，通过人工标注编辑文本构建大规模运动编辑数据集，从而可以训练一个编辑扩散模型，该模型比仅仅基于文本-运动对的重新设计的基线模型表现更优。"
claims:
- "TMED 在生成到目标检索指标上大幅领先所有基线"
- "增加 MotionFix 训练数据量能持续提升性能"
- "定性结果表明 TMED 能处理多种编辑类型，而基线则无法忠实遵循源运动或编辑文本"
- "MotionFix 测试集 上 R@1 (生成→目标检索) = 62.90"
---

# MotionFix: Text-Driven 3D Human Motion Editing

> [!tip] 核心洞察
> 利用 TMR 嵌入空间检索相似运动对，通过人工标注编辑文本构建大规模运动编辑数据集，从而可以训练一个编辑扩散模型，该模型比仅仅基于文本-运动对的重新设计的基线模型表现更优。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionFix：文本驱动的三维人体运动编辑 |
| 英文题名 | MotionFix: Text-Driven 3D Human Motion Editing |
| 会议/期刊 | SIGGRAPH Asia 2024 |
| Links | [paper](https://arxiv.org/abs/2408.00712); [Project](https://motionfix.is.tue.mpg.de) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | TMED (Text-Driven Motion Editing Diffusion Model) |
| Dataset | MotionFix 测试集, 数据规模消融（MotionFix 训练数据比例） |

> [!tip] 效果简介
> - MotionFix 测试集 上，R@1 (生成→目标检索) 为 62.90，对比 4.03 (MDM) / 39.10 (MDM-BP)，变化 比最强基线提升 +23.80。
> - MotionFix 测试集 上，R@1 (生成→源检索) 为 46.10，对比 2.47 (MDM) / 34.65 (MDM-BP)，变化 适度高于基线以维持源保真度。
> - 数据规模消融（MotionFix 训练数据比例） 上，R@1 (生成→目标检索) 为 10%: 19.25, 50%: 47.08, 100%: 62.90，对比 n/a，变化 从 10% 到 100% 显著提升。

## 概述

**问题瓶颈**：文本驱动的三维人体运动编辑面临双重挑战——缺乏包含源运动、目标运动与编辑文本的三元组训练数据，以及如何设计能同时忠实遵循源运动并精确执行编辑指令的生成模型。现有文本到运动生成方法仅以文本为条件，无法显式建模源运动约束，导致编辑结果偏离源运动或忽略编辑意图。

**核心思路**：MotionFix 提出一套半自动数据构建流程，利用 TMR 运动嵌入空间检索相似运动对，再通过人工标注编辑文本，构建首个大规模文本驱动运动编辑数据集 MotionFix（包含 6,730 个三元组）。基于该数据集，作者设计并训练了条件扩散模型 **TMED**（Text-Driven Motion Editing Diffusion Model），同时以源运动和编辑文本为条件，并引入独立的双条件 classifier-free guidance 机制，分别控制文本一致性与源运动保真度。

**方法定位**：TMED 建立在 MDM（Tevet et al., ICLR 2023）文本到运动扩散框架之上，关键改进在于：(1) 训练数据从文本-运动对升级为源运动-目标运动-编辑文本三元组；(2) 模型条件从单一文本扩展为源运动与编辑文本双条件；(3) 运动表示采用 SMPL 参数、6D 旋转等规范化形式直接回归。与仅从文本或仅从源运动初始化的重设计基线（MDM_S、MDM-BP、MDM-BP_S）相比，TMED 通过端到端学习条件编辑分布，从根本上解决了源运动信息利用不足的问题。

**主要结果**：在 MotionFix 测试集上，TMED 的生成到目标检索 R@1 达到 **62.90**，相比最强基线 MDM-BP（39.10）提升 **+23.80**；生成到源检索 R@1 为 46.10，在维持源保真度的同时显著优于所有基线。数据规模消融实验表明，训练数据从 10% 增至 100% 时性能持续提升，验证了 MotionFix 数据集的价值。定性结果（Figure 5、Figure 7）显示 TMED 能处理空间修改、时间调整、速度变化等多种编辑类型，而基线方法往往无法兼顾编辑指令与源运动忠实度。

**局限与开放问题**：模型在处理细节丰富但运动差异微妙的编辑指令时可能失败；当源-目标运动 TMR 相似度较低时，生成结果可能偏离源运动。现有评估主要依赖检索指标，对编辑保真度和运动质量的衡量仍不充分。未来方向包括提升对复杂多步指令的泛化能力、扩展至长序列连续编辑，以及结合物理约束生成更符合动力学的编辑结果。

## 背景与动机

### 问题背景

三维人体运动生成是计算机视觉与图形学中的核心课题，近年来基于扩散模型的文本到运动生成取得了显著进展，如 **MDM**（Tevet et al., ICLR 2023）等模型已能根据自然语言描述生成高质量的运动序列。然而，在实际创作与交互场景中，用户往往并非从零开始生成运动，而是希望对一段已有运动进行局部或全局的修改——例如“将手臂举过头顶”、“放慢动作速度”或“镜像这个动作”。这种**文本驱动的运动编辑**任务要求模型同时满足两个约束：忠实保留源运动中未提及的部分，并精确执行编辑文本所描述的修改。

### 现有方法缺口

直接将文本到运动生成模型重新用于编辑任务面临根本性困难。标准的文本到运动扩散模型（如 MDM）仅以文本为条件，无法感知源运动的结构信息，因此生成的编辑结果往往与源运动完全无关（Table 2 中 MDM 的生成→源检索 R@1 仅为 2.47）。一些测试时改造策略试图弥补这一缺口：例如从源运动初始化扩散过程（MDM_S），或利用 GPT 推断需要编辑的身体部位并对未编辑部位进行掩码替换（MDM-BP、MDM-BP_S）。然而，这些方法缺乏对“如何根据编辑文本修改源运动”的显式学习，其性能上限受限于预训练文本-运动模型的固有偏差。

更深层的瓶颈在于**训练数据的缺失**：现有运动-文本数据集（如 HumanML3D、KIT-ML）仅包含单段运动与其描述的配对，缺乏“源运动—目标运动—编辑文本”的三元组标注，使得直接训练运动编辑模型无从谈起。

### 本文动机

为突破上述瓶颈，本文提出了一套系统性的解决方案：

1. **构建首个文本驱动运动编辑数据集 MotionFix**：利用 TMR 运动嵌入空间检索相似运动对，通过半自动流程筛选并辅以人工标注编辑文本，形成 6,730 个三元组（源运动、目标运动、编辑文本），覆盖身体部位修改、时序变化、速度调整、风格转换等多种编辑类型（Table 1, Figure 2）。

2. **训练条件扩散编辑模型 TMED**：以源运动和编辑文本为联合条件，训练一个 Transformer 去噪器直接回归目标运动的 SMPL 参数。通过推导条件概率分解，TMED 在采样时引入独立的文本引导尺度 $s_L$ 和源运动引导尺度 $s_{M_S}$，实现对编辑忠实度与源保真度的精细控制（Eq. (5)）。

这一设计将运动编辑从“测试时技巧”提升为“有监督学习问题”，为文本驱动的运动编辑建立了可扩展的范式。

## 核心创新

MotionFix 的核心创新在于**数据与模型的双重重构**，将文本驱动的人体运动编辑从一个缺乏训练数据的“重定向”问题转变为一个可学习的条件生成任务。其关键洞察是：利用 TMR 文本-运动嵌入空间检索相似运动对，并通过人工标注编辑文本构建大规模三元组数据集，从而可以训练一个直接以源运动和编辑文本为条件的扩散模型。

### 数据层面的创新：从文本-运动对到编辑三元组

现有运动数据集（如 HumanML3D、KIT-ML）仅提供文本-运动对，无法直接支持“给定源运动 + 编辑文本 → 目标运动”的监督学习。MotionFix 通过半自动流程填补了这一空白（Table 1）：

- **相似运动对检索**：在 TMR 嵌入空间中，对每个运动检索与其相似但不同的候选运动，过滤掉过于相似（7%）和差异过大（55%）的对，保留具有可编辑差异的运动对。
- **人工标注编辑文本**：对筛选后的运动对，由标注者撰写描述从源运动到目标运动变化的自然语言指令，形成（源运动、目标运动、编辑文本）三元组。
- **数据集规模**：最终构建了包含 6,730 个三元组的 MotionFix 数据集，词汇量 1,479，覆盖身体部位修改、时间变化、速度调整、风格转换等多种编辑类型（Figure 2）。

这一数据构建策略是方法有效性的根基——消融实验（Table 3）表明，仅使用 10% 训练数据时，TMED 的生成→目标检索 R@1 仅为 19.25，而使用完整数据时跃升至 62.90，验证了数据规模对编辑性能的关键作用。

### 模型层面的创新：双条件扩散与独立引导

TMED 在 MDM（Tevet et al., ICLR 2023）文本到运动扩散框架的基础上进行了三个关键改造（Figure 3 左）：

1. **双条件输入**：去噪 Transformer 同时接收编辑文本（经冻结 CLIP ViT-B/32 编码）和源运动（经线性投影至 512 维），二者通过可学习的 SEP token 在序列中分隔。这与 MDM 仅以文本为条件形成根本差异。

2. **独立 Classifier-Free Guidance 尺度**：采样时，TMED 使用**两个独立的引导尺度** $s_{M_S}$（源运动引导）和 $s_L$（文本引导）来控制编辑行为。修改后的分数估计为：
   $$\tilde{e}_{\theta}(M_T, s_{M_S}, s_L) = e_{\theta}(M_T, \emptyset, \emptyset) + s_{M_S} \cdot (e_{\theta}(M_T, M_S, \emptyset) - e_{\theta}(M_T, \emptyset, \emptyset)) + s_L \cdot (e_{\theta}(M_T, M_S, L) - e_{\theta}(M_T, M_S, \emptyset))$$
   这一设计允许在源运动忠实度和编辑文本遵循度之间进行精细权衡（Figure 4 热力图分析显示，极端尺度值会导致性能下降，需保持平衡）。

3. **规范化运动表示**：直接回归 SMPL 参数，每帧维度 $d_p=207$（包含 6D 旋转、局部关节位置、全局平移和朝向），相比以往基于关节位置的表示提供了更结构化的运动编码。

### 与基线方法的本质差异

为验证上述创新的必要性，作者设计了多种基于 MDM 重定向的基线（Figure 3 右），这些基线仅从文本-运动对预训练模型出发，在测试时引入源运动信息：

- **MDM**：仅使用编辑文本，完全忽略源运动。
- **MDM_S**：从源运动初始化扩散过程，而非从纯噪声开始。
- **MDM-BP**：使用 GPT 自动标注需编辑的身体部位，仅对编辑部位进行扩散去噪，其余部位从源运动复制。
- **MDM-BP_S**：结合源运动初始化和身体部位掩码。

这些基线的共同缺陷在于**缺乏对“源运动条件”的显式学习**——它们要么不利用源运动，要么以启发式方式注入源信息，但从未在训练中学习如何根据源运动调整生成。Table 2 的结果鲜明地揭示了这一鸿沟：TMED 的生成→目标检索 R@1 达到 62.90，而最强基线 MDM-BP 仅为 39.10（差距 +23.80）；在源运动忠实度（生成→源检索 R@1）上，TMED 也以 46.10 领先于 MDM-BP 的 34.65。定性对比（Figure 7）进一步显示，基线方法往往无法同时满足编辑指令和源运动忠实度，而 TMED 能更好地兼顾二者。

综上，MotionFix 的核心创新可概括为：**以数据构建驱动模型设计，通过三元组数据集使扩散模型学会“源运动+编辑文本→目标运动”的条件映射，并以双引导机制实现可控编辑**。这一思路从根本上改变了文本驱动运动编辑的范式——从测试时的启发式重定向转向训练时的条件生成学习。

## 整体框架

MotionFix 提出了一个完整的文本驱动三维人体运动编辑流水线，其核心由**数据构建**与**条件扩散模型**两大阶段构成。

### 数据构建流水线

由于此前不存在支持文本驱动运动编辑的训练数据，作者设计了一套半自动数据收集方法。该方法首先利用 **TMR 运动嵌入空间**（Text-to-Motion Retrieval）检索相似的运动对：对于 HumanML3D 数据集中的每个运动，在 TMR 嵌入空间中检索其最近邻，形成候选源-目标运动对。随后，通过人工标注为每对运动撰写编辑文本描述，描述从源运动变化到目标运动所需的修改。经过质量筛选（约 7% 的运动对被认为过于相似而被剔除，约 55% 被认为差异过大），最终构建了包含 **6730 个三元组**（源运动、目标运动、编辑文本）的 **MotionFix 数据集**，并按 80%/5%/15% 划分为训练/验证/测试集（Table 1）。

### 模型流水线

在 MotionFix 数据集的基础上，作者设计了 **TMED（Text-Driven Motion Editing Diffusion Model）**，这是一个以源运动和编辑文本为双重条件的扩散模型。其整体架构如 Figure 3（左）所示，包含以下核心模块：

![[assets/figures/papers/paper_list_l6_MotionFix_Text_Driven_3D_Human_Motion_Editing/figures/004_Figure_3.jpg]]
*Figure 3: Models overview: (left) We illustrate our TMED model during training. We noise the target motion for ?? steps, and the transformer model is trained to denoise it back by one step. The conditions – text and source motion – are appended to the input. CLIP backbone is frozen, while components denoted in pink are learned during training. At test time, the iterative diffusion process is initialized from random noise instead of the noised target. (right) Our MDM-BP baseline is repurposed from a pretrained text-to-motion generation model to be used only at test time for motion editing. The model is initialized from random noise and the body parts not to be edited according to GPT are copied from t...*

1. **运动表示**：每个运动帧被表示为 207 维特征向量 $d_p = 207$，包含 3 维全局平移、12 维全局朝向（6D 旋转表示）以及 192 维身体姿态（21 个关节的 6D 旋转 + 22 个关节的局部位置，去除根旋转后的相对表示）。

2. **文本编码器 $E_L$**：使用冻结的 CLIP ViT-B/32 骨干网络提取编辑文本的特征表示。

3. **运动编码器 $E_M$**：将每帧 207 维的运动特征通过线性投影映射至 512 维嵌入空间。

4. **时间步编码器 $E_T$**：将扩散时间步 $t$ 转换为正弦位置嵌入后，经前馈网络映射为条件向量。

5. **Transformer 去噪器 $D$**：核心去噪模块基于 Transformer 编码器架构。在训练时，目标运动 $M_T$ 被加噪 $t$ 步后，与源运动 $M_S$、文本条件 $L$ 以及时间步嵌入一同输入 Transformer。源运动与目标运动的帧序列通过一个可学习的 **SEP Token**（分离标记）进行分隔。训练目标为预测原始目标运动：
   $$\mathbb{E}_{\epsilon \sim N(0,1), t, L, M_S} \left\| D\left(M_T^t; t, L, M_S\right) - M_T \right\|$$
   其中 $M_T^t$ 表示加噪后的目标运动。

### 推理时的双重引导采样

在推理阶段，TMED 从纯噪声初始化，通过迭代去噪生成编辑后的运动。为了在采样过程中独立控制文本一致性与源运动保真度，作者推导了具有独立尺度因子的 **classifier-free guidance** 分数估计：

$$\tilde{e}_{\theta}(M_T, s_{M_S}, s_L) = e_{\theta}(M_T, \emptyset, \emptyset) + s_{M_S} \cdot (e_{\theta}(M_T, M_S, \emptyset) - e_{\theta}(M_T, \emptyset, \emptyset)) + s_L \cdot (e_{\theta}(M_T, M_S, L) - e_{\theta}(M_T, M_S, \emptyset))$$

其中 $s_{M_S}$ 控制源运动的保真度，$s_L$ 控制编辑文本的遵循程度。这一设计允许用户在生成时灵活权衡“保持源运动特征”与“忠实执行编辑指令”之间的平衡（Figure 4 的热力图分析表明，两者需保持适度平衡，极端值均会导致性能下降）。

### 输入输出流总结

- **输入**：源运动 $M_S$（$N$ 帧 × 207 维）、编辑文本 $L$、随机噪声。
- **条件注入**：文本经冻结 CLIP 编码，源运动经线性投影后与加噪目标运动在帧维度拼接，通过 SEP Token 分隔。
- **去噪过程**：Transformer 在时间步、文本、源运动三重条件下逐步去噪。
- **输出**：编辑后的目标运动 $M_T$，与源运动具有相同的 SMPL 参数化表示，可直接用于下游动画应用。

## 核心模块与公式推导

### 运动表示

TMED 将人体运动表示为 SMPL 参数的直接回归。每帧运动向量维度 $d_p = 207$，由三部分组成：全局平移（3维）、全局朝向（12维）以及身体姿态（192维）。身体姿态采用 6D 旋转表示（共 21 个关节，$6 \times 21 = 126$ 维），并附加去除根旋转后的局部关节位置（22 个关节，$22 \times 3 = 66$ 维），合计 192 维。这一规范化表示相比以往基于关节位置的方法，能更紧凑地编码运动信息，同时便于扩散模型直接回归 SMPL 参数。

### 模型架构

TMED 是一个以源运动 $M_S$ 和编辑文本 $L$ 为条件的 Transformer 去噪扩散模型，其架构基于 MDM（Tevet et al., ICLR 2023）扩展而来，核心模块包括：

- **文本编码器 $E_L$**：使用冻结的 CLIP ViT-B/32 提取编辑文本的特征表示，在训练过程中不更新参数。
- **运动编码器 $E_M$**：将每帧运动特征（维度 207）通过线性投影映射至 512 维，作为 Transformer 的输入。
- **时间步编码器 $E_T$**：将扩散时间步 $t$ 转换为正弦位置嵌入，再经前馈网络映射，注入 Transformer 以使模型感知噪声水平。
- **SEP 标记**：一个可学习的分离标记，用于在输入序列中分隔目标运动帧与源运动帧，帮助模型区分两类运动信息。
- **Transformer 去噪器 $D$**：通过 Transformer 编码器，在时间步 $t$、编辑文本 $L$ 和源运动 $M_S$ 的条件下，对加噪的目标运动 $M_T^t$ 进行一步去噪，预测干净的目标运动 $M_T$。

训练时，目标运动 $M_T$ 被逐步加噪 $T$ 步，模型学习从 $M_T^t$ 恢复 $M_T$；测试时，扩散过程从随机噪声初始化，迭代去噪生成编辑后的运动。架构概览见 Figure 3（左）。

### 训练损失

TMED 的训练目标是最小化去噪器输出与真实目标运动之间的均方误差：

$$\mathbb{E}_{\epsilon \sim \mathcal{N}(0,1), t, L, M_S} \left\| D\left(M_T^t; t, L, M_S\right) - M_T \right\|$$

其中 $\epsilon$ 为标准高斯噪声，$t$ 为扩散时间步，$L$ 为编辑文本条件，$M_S$ 为源运动条件，$M_T^t$ 为加噪后的目标运动，$D(\cdot)$ 为 Transformer 去噪器的预测输出。

### 条件概率分解

为理解双条件扩散模型的工作机理，论文将目标运动 $M_T$ 在源运动 $M_S$ 和文本 $L$ 条件下的概率进行展开：

$$P(M_T \mid M_S, L) = \frac{P(L \mid M_S, M_T) \, P(M_S \mid M_T) \, P(M_T)}{P(L, M_S)}$$

取对数后得到三项分解：

$$\log P(M_T \mid M_S, L) = \log P(L \mid M_S, M_T) + \log P(M_S \mid M_T) + \log P(M_T) - \log P(L, M_S)$$

三项分别对应：**文本一致性**（给定源和目标运动时编辑文本的似然）、**源保真度**（给定目标运动时源运动的似然）以及**运动先验**（目标运动的无条件概率）。这一分解为后续设计双条件 classifier-free guidance 提供了理论依据。

### 双条件引导采样

在采样阶段，TMED 采用具有独立尺度因子的双条件 classifier-free guidance 分数估计，以分别控制文本条件与源运动条件对生成过程的影响强度：

$$\tilde{e}_{\theta}(M_T, s_{M_S}, s_L) = e_{\theta}(M_T, \emptyset, \emptyset) + s_{M_S} \cdot \big(e_{\theta}(M_T, M_S, \emptyset) - e_{\theta}(M_T, \emptyset, \emptyset)\big) + s_L \cdot \big(e_{\theta}(M_T, M_S, L) - e_{\theta}(M_T, M_S, \emptyset)\big)$$

其中 $e_{\theta}(\cdot)$ 为模型预测的分数函数，$s_{M_S}$ 为源运动引导尺度，$s_L$ 为文本引导尺度，$\emptyset$ 表示对应条件置空。通过调节 $s_{M_S}$ 和 $s_L$，可在源运动忠实度与编辑文本遵循度之间取得平衡。消融实验（Figure 4）表明，两个引导尺度需保持适度平衡，极端取值会导致某一维度性能显著下降。

## 实验与分析

### 主实验结果

TMED 在 MotionFix 测试集上展现出显著的编辑能力优势。表 2 报告了各模型在生成运动到目标运动检索（Generated-to-Target Retrieval）和生成运动到源运动检索（Generated-to-Source Retrieval）上的 R@1 指标。

在生成→目标检索上，TMED 的 R@1 达到 **62.90**，远超所有基线方法。具体而言，仅使用编辑文本的标准文本到运动扩散模型 MDM（Tevet et al., ICLR 2023）仅获得 4.03，表明单纯依赖文本条件无法有效定位目标运动。从源运动初始化扩散过程的变体 MDM_S 提升至 18.58，但仍远不及 TMED。结合 GPT 身体部位掩码的 MDM-BP 达到 39.10，是基线中的最强结果，而 TMED 在此基础上进一步提升了 **+23.80** 个百分点。这一差距的核心原因在于：基线方法仅在测试时通过启发式策略（初始化或掩码）注入源运动信息，而 TMED 在训练阶段就显式学习源运动与编辑文本的联合条件分布。

在生成→源检索上，TMED 的 R@1 为 **46.10**，适度高于最强基线 MDM-BP 的 34.65。这一指标衡量生成运动对源运动的忠实度——过高的源检索分数意味着模型未充分执行编辑，过低的分数则意味着模型偏离源运动过远。TMED 在该指标上的表现表明其能在执行编辑的同时较好地保持源运动的整体结构。

### 数据规模消融实验

表 3 展示了 MotionFix 训练数据规模对 TMED 性能的影响。当仅使用 10% 的训练数据时，生成→目标检索的 R@1 为 19.25；使用 50% 数据时提升至 47.08；使用全部数据时达到 62.90。这一单调递增的趋势表明：（1）TMED 的编辑能力确实来源于对三元组数据的学习，而非模型架构的固有优势；（2）MotionFix 数据集的规模仍有扩展空间，增加数据量有望进一步提升性能。

### 双条件引导尺度分析

TMED 在采样时使用两个独立的 classifier-free guidance 尺度：源运动引导尺度 $s_{M_S}$ 和文本引导尺度 $s_L$。图 4 以热力图形式展示了这两个尺度在 $[1, 5]$ 范围内对生成→目标检索和生成→源检索 R@1 的影响。

热力图揭示了一个关键权衡：当 $s_L$ 过高而 $s_{M_S}$ 过低时，生成→目标检索性能下降，说明模型过度追求文本一致性而忽略了源运动约束；反之，当 $s_{M_S}$ 过高而 $s_L$ 过低时，生成→源检索性能虽高，但生成→目标检索显著下降，说明模型过度保守地保留源运动而未能执行编辑。最优性能出现在两个尺度保持适度平衡的区域。这一发现验证了公式 (5) 中双条件引导设计的必要性——单一引导尺度无法同时控制文本一致性和源保真度这两个相互制约的目标。

### 定性结果与基线对比

图 5 展示了 TMED 在多种编辑类型上的生成结果，包括空间编辑（如“将手臂举过头顶”）、时间编辑（如“减速”）、风格编辑和重复动作编辑等。生成运动（蓝色）与源运动（红色）的叠加可视化显示，TMED 能够精确修改指定的身体部位或运动属性，同时保持未编辑部分的运动轨迹。

图 7 的基线定性对比进一步揭示了 TMED 的优势。MDM_S（从源运动初始化扩散）倾向于生成与源运动高度相似但未充分执行编辑的运动；MDM-BP_S（结合初始化和身体部位掩码）在某些情况下能保留未编辑部位，但对编辑指令的响应不够精确；MDM-BP（仅使用身体部位掩码，从纯噪声开始）在文本一致性上有所改善，但容易在非编辑部位引入不自然的运动伪影。TMED 在编辑精度和源忠实度之间取得了更好的平衡。

### 失败模式分析

图 6 揭示了 TMED 的两类典型失败模式：

1. **复杂编辑指令下的欠编辑**：当编辑文本描述详细且源运动与目标运动之间的差异微妙时，模型可能无法正确生成满足所有指令约束的编辑。例如，涉及多个身体部位协调变化的复杂描述可能导致模型仅部分执行编辑或产生模糊的运动修改。

2. **低相似度源运动下的源偏离**：尽管生成运动在语义上遵循了编辑文本，但当源运动与目标运动在 TMR 嵌入空间中的相似度较低时，模型可能过度偏离源运动的结构。这表明 TMED 对源运动条件的依赖强度受限于训练数据中运动对的相似度分布。

这些失败模式指向了当前方法的局限性：模型在训练过程中学习的是 MotionFix 数据集中运动对的编辑模式，对于数据分布之外的编辑类型或相似度过低的运动对，其泛化能力有限。此外，现有的检索式评估指标（R@1）主要衡量生成运动与目标运动在嵌入空间中的接近程度，可能无法完全捕捉编辑的精确度和运动质量，这是评估体系本身的一个固有限制。

### 补充图表

![[assets/figures/papers/paper_list_l6_MotionFix_Text_Driven_3D_Human_Motion_Editing/figures/007_Figure_4.jpg]]
*Figure 4: Guidances of conditions: We illustrate the R@1 performance of TMED for generated-to-target (left) and generated-to-source (right) retrieval benchmarks for $s _ { L } , s _ { M _ { S } } \in \left$[ 1 , 5 $\right$]

![[assets/figures/papers/paper_list_l6_MotionFix_Text_Driven_3D_Human_Motion_Editing/figures/009_Figure_6.jpg]]
*Figure 6: Failure cases: We show four failure examples from our model. For each sample, we provide the source motion (red) overlaid both with the generation (blue, left) or the ground-truth target motion (green, right). In the top row, we observe that the model may fail to generate the edited motions when the edit text is detailed and the motions differences are subtle. In the bottom row, although the generated motions follow the edit text, they diverge from the source motions*

![[assets/figures/papers/paper_list_l6_MotionFix_Text_Driven_3D_Human_Motion_Editing/figures/002_Table_1.jpg]]
*Table 1: Comparison with existing datasets: MotionFix is the first dataset supporting the task of text-based motion editing*

![[assets/figures/papers/paper_list_l6_MotionFix_Text_Driven_3D_Human_Motion_Editing/figures/005_Table_2.jpg]]
*Table 2: Results on the MotionFix benchmark (test set): We first evaluate several variants of our text-to-motion synthesis baseline (MDM) on the motion editing task. Subscript ?? denotes models that denoise the source motion initialization (init) instead of starting the diffusion from noise. BP indicates GPT-based body part labeling described in Section 4 to mask the source body parts which are kept unchanged during diffusion. Our model TMED effectively learns how to utilize the source motion conditioning, thanks to the MotionFix training data. See text for detailed comments*

![[assets/figures/papers/paper_list_l6_MotionFix_Text_Driven_3D_Human_Motion_Editing/figures/006_Table_3.jpg]]
*Table 3: Effect of training data size in MotionFix: We observe significant performance improvement as we increase the amount of training data*

![[assets/figures/papers/paper_list_l6_MotionFix_Text_Driven_3D_Human_Motion_Editing/figures/011_Table.jpg]]
*Table: A.1. Statistics of the MotionFix textual data: There are relatively low number of duplicate texts (given 6730 triplets and 5992 unique texts). The vocabulary is diverse (1479 unique words) and the average number of words per text (8.46) has a good trade-off between conciseness and expressiveness*

![[assets/figures/papers/paper_list_l6_MotionFix_Text_Driven_3D_Human_Motion_Editing/figures/013_Table_2.jpg]]
*Table 2: Fig. A.1. Word frequencies in the MotionFix dataset: On the left, we display a word cloud for the text annotations in in the dataset. Most frequent words appear in larger fonts. Examples of such words are ‘hand’, ‘arm’ referring to body parts, ‘instead’ referring to the source motion, ‘higher’, ‘lower’, ‘opposite’, ‘slower’ referring to spatial, directional or speed edits. On the right, we show the histogram of the 30 most frequent words in the data. Table A.2. Results on the MotionFix benchmark using the whole test set as a gallery: We evaluate the models in Table 2 of the main paper on the full test set of 1013 samples (as opposed to a random subset of 32). While the retrieval metrics are...*

![[assets/figures/papers/paper_list_l6_MotionFix_Text_Driven_3D_Human_Motion_Editing/figures/014_Table.jpg]]
*Table: A.3. Text-based motion editing benchmark on MotionFix test set with different training data sizes. We observe that the performance increases significantly when more data are used during training*

![[assets/figures/papers/paper_list_l6_MotionFix_Text_Driven_3D_Human_Motion_Editing/figures/015_Table.jpg]]
*Table: 14 • Nikos Athanasiou, Alpár Cseke, Markos Diomataris, Michael J. Black, and Gül Varol*

## 方法谱系与知识库定位

### 一、任务定位与核心瓶颈

MotionFix 首次将 **文本驱动的三维人体运动编辑** 定义为一个独立任务：给定源运动序列 $M_S$ 和自然语言编辑指令 $L$，生成编辑后的目标运动 $M_T$，使其同时满足对编辑文本的忠实遵循和对源运动未编辑部分的保真度保持。该任务区别于传统的文本到运动生成（text-to-motion generation），后者的输入仅为文本，无需考虑与源运动的一致性。

该任务面临的核心瓶颈是 **训练数据的缺失**：现有运动-文本数据集（如 HumanML3D、KIT-ML）仅提供文本-运动对，缺乏源运动-目标运动-编辑文本的三元组，无法直接支持条件编辑模型的训练。此外，如何设计模型架构使其能够同时以源运动和编辑文本为条件，并在两者之间取得平衡，也是关键挑战。

### 二、与基线方法的关系

为评估 TMED 的有效性，作者基于当前最先进的文本到运动扩散模型 **MDM**（Tevet et al., ICLR 2023）构建了四个递进式基线，形成一个从纯生成到逐步引入源信息的基线谱系：

| 基线 | 条件输入 | 扩散初始化 | 源信息引入方式 |
|------|---------|-----------|---------------|
| **MDM** | 仅编辑文本 | 随机噪声 | 无 |
| **MDM_S** | 仅编辑文本 | 源运动加噪 | 通过初始化隐式注入 |
| **MDM-BP** | 编辑文本 + GPT 身体部位掩码 | 随机噪声 | 仅通过掩码保护未编辑部位 |
| **MDM-BP_S** | 编辑文本 + GPT 身体部位掩码 | 源运动加噪 | 初始化 + 掩码双重引入 |

其中，下标 `_S` 表示从源运动初始化扩散过程（而非从纯噪声开始），`BP` 表示利用 GPT 自动标注需要编辑的身体部位，并在扩散过程中将未编辑部位从源运动复制到生成结果中。MDM-BP_S 是基线中最强的变体，结合了源初始化和部位掩码两种机制。

TMED 与这些基线的本质区别在于 **训练范式**：基线均为测试时重利用（test-time repurposing），未在运动编辑三元组上训练；而 TMED 在 MotionFix 数据集上端到端训练，学习显式地利用源运动条件。这一差异在定量结果中体现为巨大性能差距——TMED 在生成→目标检索 R@1 上达到 62.90，而最强基线 MDM-BP 仅为 39.10（Table 2）。

### 三、方法谱系中的位置

**上游依赖：**
- **运动表示**：采用 SMPL 参数化，使用 6D 旋转表示和相对平移，直接回归 SMPL 参数（维度 $d_p = 207$），继承了 MDM 的表示框架。
- **文本编码**：使用冻结的 CLIP ViT-B/32 提取文本特征，与 MDM 一致。
- **扩散框架**：基于 DDPM 的 Transformer 去噪架构，采用余弦噪声调度，训练 1000 个 epoch。
- **数据集构建**：依赖 **TMR**（Text-to-Motion Retrieval）嵌入空间检索相似运动对，数据集质量受 TMR 表示能力的约束。

**平行/下游关系：**
- 与同期运动编辑方法（如基于运动修复或运动混合的方法）相比，TMED 是首个将文本驱动运动编辑形式化为条件扩散模型的工作，为后续研究提供了数据集和基线。
- 该方法可潜在地与物理模拟、运动动力学约束结合，以提升编辑结果的运动学合理性（论文未实现，列为开放问题）。

### 四、适用边界

**适用场景：**
- 短序列人体运动的局部或全局编辑，包括空间修改（如“将手臂举过头顶”）、时间修改（如“放慢速度”）、风格转换（如“镜像”）等。
- 编辑文本为简洁的自然语言指令，运动差异在 TMR 嵌入空间中有可辨识的相似性。

**不适用/高风险场景：**
- **复杂多步指令**：当编辑文本过于详细且运动差异微妙时，模型可能无法正确执行编辑（Figure 6 顶部行）。
- **低源-目标相似度**：当 TMR 相似度较低时，生成的编辑可能偏离源运动（Figure 6 底部行），表明模型对嵌入空间质量敏感。
- **长序列连续编辑**：当前模型针对固定长度短序列设计，未验证迭代编辑或长序列编辑能力。
- **物理约束严格场景**：模型未结合物理模拟，可能生成运动学上不合理的运动。

### 五、局限与开放问题

**已识别的局限：**
1. **数据依赖**：模型仅在 MotionFix 数据集（6730 个三元组）上训练，泛化能力受限于数据集的规模和多样性。
2. **评估指标不足**：现有评估主要依赖运动检索指标（R@1），可能无法完全衡量编辑的保真度和运动质量，缺乏直接评估文本-运动一致性和源保真度的指标。
3. **TMR 嵌入敏感**：数据构建和评估均依赖 TMR 嵌入空间，对嵌入的表示能力敏感。
4. **部位检测依赖外部模型**：基线中的身体部位掩码依赖 GPT 自动标注，可能引入不完美标注的噪声。

**开放问题：**
- 如何提高模型对完全未见过的编辑文本和复杂多步指令的泛化能力？
- 能否扩展至更长运动序列的连续或迭代编辑？
- 如何结合更强的时空感知机制，减少模型对源运动的无意识发散？
- 是否可以自动检测或推断需要编辑的身体部位，以避免依赖外部不完美的自动标注？
- 该方法能否与物理模拟或动力学约束结合，生成更符合物理规律的编辑？

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2024/MotionFix_Text_Driven_3D_Human_Motion_Editing.pdf]]
