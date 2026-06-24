---
title: "PartMotionEdit: Fine-Grained Text-Driven 3D Human Motion Editing via Part-Level Modulation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/PartMotionEdit_Fine_Grained_Text_Driven_3D_Human_Motion_Editing_via_Part_Level_Modulation.pdf
aliases:
- PartMotionEdit
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将人体运动分解为五个预定义部件，并通过部件级相似度曲线监督与部件感知运动调制模块（PMM）显式预测每个部件的编辑权重，从而实现精细的局部编辑控制。
primary_logic: 通过部件分解和自适应部件权重调制，模型能够学习在不同编辑指令下对每个身体部件进行差异化编辑，使编辑过程可解释，且能同时保持全局运动连续性与文本语义一致性。
claims:
- 在MotionFix基准上，PartMotionEdit在生成-目标检索指标（R@1,R@2,R@3,AvgR等）方面全面优于已有方法，包括SimMotionEdit和MotionFix。
- 当同时启用PMM和PSM时，生成-目标批检索R@1从70.83提升至73.96，AvgR从2.31降至1.92，充分验证了部件调制和部件级监督机制的有效性。
- 移除BMI模块后，运动质量M-Score从-4.114下降至-4.432，R@1从73.96下降至72.08，说明双向跨模态交互对于精确的语义对齐至关重要。
- 通过部件分解和自适应部件权重调制，模型能够学习在不同编辑指令下对每个身体部件进行差异化编辑，使编辑过程可解释，且能同时保持全局运动连续性与文本语义一致性。
---

# PartMotionEdit: Fine-Grained Text-Driven 3D Human Motion Editing via Part-Level Modulation

> [!tip] 核心洞察
> 通过部件分解和自适应部件权重调制，模型能够学习在不同编辑指令下对每个身体部件进行差异化编辑，使编辑过程可解释，且能同时保持全局运动连续性与文本语义一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | PartMotionEdit：基于部件级调制的细粒度文本驱动3D人体运动编辑 |
| 英文题名 | PartMotionEdit: Fine-Grained Text-Driven 3D Human Motion Editing via Part-Level Modulation |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2512.24200) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PartMotionEdit |
| Dataset |  |

> [!tip] 效果简介
> - 在MotionFix基准上，PartMotionEdit在生成-目标检索指标（R@1,R@2,R@3,AvgR等）方面全面优于已有方法，包括SimMotionEdit和MotionFix。
> - 当同时启用PMM和PSM时，生成-目标批检索R@1从70.83提升至73.96，AvgR从2.31降至1.92，充分验证了部件调制和部件级监督机制的有效性。
> - 移除BMI模块后，运动质量M-Score从-4.114下降至-4.432，R@1从73.96下降至72.08，说明双向跨模态交互对于精确的语义对齐至关重要。

## 概述

文本驱动的3D人体运动编辑旨在根据自然语言指令修改给定的源运动序列。现有方法普遍采用全局建模策略，难以精确控制局部身体部件的运动变化。例如，**SimMotionEdit**（Li et al., CVPR 2025）虽然引入了运动相似度预测作为辅助任务，但其相似度计算基于全身姿态，未能分解到关节或部件粒度。当编辑指令涉及多个需要差异化处理的部件时（如“左手叉腰，同时抬起右腿”），全局方法容易造成非目标区域的意外扰动，导致局部编辑效果不佳。

**PartMotionEdit** 针对上述瓶颈，提出了基于部件级调制的细粒度运动编辑框架。其核心思路是将人体运动分解为五个预定义部件（躯干、左臂、右臂、左腿、右腿），并通过部件感知运动调制模块（Part-aware Motion Modulation, PMM）显式预测每个部件的编辑权重，实现对不同身体区域的差异化控制。同时，部件级相似度监督机制（Part-level Supervision Mechanism, PSM）在训练阶段提供细粒度的部件运动变化信号，引导模型学习可解释的编辑策略。此外，双向跨模态交互模块（Bidirectional Motion Interaction, BMI）通过双向注意力机制促进文本与运动特征的深度语义融合，确保编辑结果与文本指令的精确对齐。

在 **MotionFix** 基准（Athanasiou et al., SIGGRAPH Asia 2024）上的实验结果表明，PartMotionEdit在生成-目标检索指标上全面优于已有方法。消融研究进一步验证了各模块的关键作用：同时启用PMM和PSM使R@1从70.83提升至73.96，AvgR从2.31降至1.92；移除BMI后，运动质量M-Score从-4.114下降至-4.432，R@1下降至72.08。

在方法谱系上，PartMotionEdit继承并改进了文本条件扩散运动生成范式，其关键突破在于将全局运动相似度监督（SimMotionEdit的粒度）替换为部件级相似度曲线监督，并引入显式的部件感知调制机制替代纯全局特征生成。该方法可定位为细粒度可控运动编辑的代表性工作，为后续探索语义级部件分解和序列化编辑任务奠定了基础。

## 背景与动机

### 任务背景：文本驱动的3D人体运动编辑

3D人体运动编辑旨在根据自然语言指令修改给定的源运动序列，使其在保留非目标区域运动特征的同时，精确反映文本描述的语义变化。这一任务在动画制作、虚拟人交互和游戏开发等领域具有广泛应用前景。形式上，给定源运动序列 $M_{src} \in \mathbb{R}^{T \times D}$（其中 $T$ 为帧数，$D=207$ 为每帧特征维度，包含3维全局平移、12维全局朝向和192维身体姿态）和文本编辑指令 $P$，模型需要生成目标运动 $M_{tgt}$，使其既满足文本语义约束，又尽可能保留源运动中未被编辑部分的运动特性。

### 现有方法的瓶颈：全局建模与细粒度控制的矛盾

当前主流的文本驱动运动编辑方法普遍采用**全局建模策略**，即对整个人体运动序列进行统一的特征编码与编辑控制。这种范式在以下两个层面暴露出根本性局限：

**1. 运动相似度监督粒度过粗。** 以 **SimMotionEdit**（Li et al., CVPR 2025）为代表的SOTA方法引入了运动相似度预测作为辅助任务，试图让模型感知源运动与目标运动之间的差异程度。然而，其相似度计算基于**全身姿态**的全局度量，未能分解到关节或部件粒度。当一条编辑指令涉及多个需要差异化处理的身体部件时——例如“左手叉腰，同时右脚向前迈一步”——全局相似度曲线无法为模型提供关于“哪些部位需要大幅修改、哪些部位应当保持静止”的精确指导信号。这直接导致模型在局部编辑时控制能力不足，容易产生误编辑或编辑不足的问题。

**2. 运动特征调制缺乏部件感知能力。** 现有方法在生成目标运动时，通常使用单一的全局特征表示进行解码，缺乏显式的部件级调制机制。这意味着模型无法在学习过程中自适应地判断“当前编辑指令主要影响哪些身体部件”，更无法对不同部件施加差异化的编辑强度。当编辑指令仅涉及局部肢体（如仅改变手臂动作）时，全局调制策略往往会干扰非目标区域（如腿部或躯干），导致运动质量下降和不自然的伪影。

### 核心动机：从部件分解到自适应调制

上述瓶颈的根源在于：**现有方法将人体运动视为一个不可分割的整体，而忽略了人体运动天然具有的部件化结构**——躯干、左右臂、左右腿在功能上相对独立，在不同编辑指令下呈现出高度差异化的运动变化模式。

PartMotionEdit 的核心动机正是突破这一全局建模范式，通过**显式的部件分解与自适应权重调制**，使模型具备以下能力：

- **细粒度感知**：将22关节的人体骨架分解为五个预定义部件 $G = \{ \text{Torso}, L_{arm}, R_{arm}, L_{leg}, R_{leg} \}$，并在部件级别计算源运动与目标运动之间的相似度曲线，为模型提供精确的局部编辑监督信号。
- **差异化控制**：设计部件感知运动调制模块（Part-aware Motion Modulation, PMM），通过学习可训练的部件查询向量，动态预测每个部件的编辑权重，并对运动特征施加残差调制，实现“该改的地方大幅改，不该改的地方尽量不动”的精细控制。
- **语义对齐保障**：引入双向跨模态交互模块（Bidirectional Motion Interaction, BMI），在文本与运动特征之间建立双向注意力机制，确保编辑过程在获得部件级控制力的同时，不损失全局运动连续性与文本语义一致性。

## 核心创新

PartMotionEdit的核心创新在于将文本驱动的3D人体运动编辑从**全局建模**推进到**部件级调制**，解决了现有方法无法精确控制局部运动且易干扰非目标区域的瓶颈。具体而言，其关键创新点体现在以下三个相互耦合的changed slots上。

### 1. 部件级运动相似度监督（PSM）

现有方法如**SimMotionEdit**（Li et al., CVPR 2025）虽引入了运动相似度预测辅助任务，但其相似度基于全身姿态，无法分解到关节或部件粒度。当编辑涉及多个需差异化处理的部件时，全局相似度信号的控制能力明显不足。

PartMotionEdit将人体运动显式分解为五个预定义部件：
$$G = \{ \mathrm{Torso}, L_{\mathrm{arm}}, R_{\mathrm{arm}}, L_{\mathrm{leg}}, R_{\mathrm{leg}} \}$$

在训练阶段，PSM为每个部件独立计算相似度曲线。首先通过关节位置欧氏距离和旋转变化的加权组合衡量部件运动差异：
$$S_{i,t} = - \big( \beta \cdot D_{i,t}^{\mathrm{pos}} + (1-\beta) \cdot D_{i,t}^{\mathrm{rot}} \big)$$

随后施加**双层归一化**：全局归一化消除不同部件间的数值尺度差异，序列内归一化突出单条运动内各部件相似度的相对变化趋势。这一设计使监督信号能够精确刻画“哪些部件需要编辑、编辑幅度多大”，为后续的部件感知调制提供了可学习的目标。

### 2. 部件感知运动调制模块（PMM）

PMM是PartMotionEdit的核心控制模块，其功能是**显式预测每个部件的编辑权重并执行残差调制**。模块通过五个可学习的部件查询（part queries）与运动特征进行交叉注意力交互：
$$A_i = \mathrm{Softmax}\left( \frac{q_i W_q (F_m' W_k)^T}{\sqrt{D}} \right)$$

聚合后的部件特征经非线性映射投影到$[0,1]$区间，生成编辑权重矩阵$R$，用于对运动特征施加部件自适应调制：
$$F_m'' = F_m' + R \odot \mathrm{MLP}(F_m')$$

这种残差调制机制使模型能够根据文本指令，对需要编辑的部件施加较大调制、对无需编辑的部件施加较小调制，从而在实现精细局部编辑的同时保持非目标区域不变。消融实验（Table 3）证实：同时启用PMM和PSM时，生成-目标批检索R@1从70.83提升至73.96，AvgR从2.31降至1.92，充分验证了部件调制和部件级监督机制的有效性。

### 3. 双向跨模态运动交互（BMI）

在文本与运动特征的融合方式上，PartMotionEdit引入双向跨模态注意力机制，替代了SimMotionEdit中简单的特征融合策略。BMI模块通过两个方向的交叉注意力，使文本特征和运动特征进行双向语义交换，确保编辑指令与运动表示在语义层面充分对齐。消融实验（Table 4）表明：移除BMI模块后，运动质量M-Score从-4.114降至-4.432，R@1从73.96降至72.08，证明双向跨模态交互对于精确的语义对齐至关重要。

### 创新总结

三个changed slots形成了一条完整的因果链路：**PSM**提供部件粒度的监督目标 → **PMM**学习预测部件编辑权重并执行调制 → **BMI**确保文本与运动的语义对齐贯穿始终。这一设计使编辑过程可解释，且能同时保持全局运动连续性与文本语义一致性，在MotionFix基准上全面优于包括SimMotionEdit和MotionFix在内的已有方法。

## 整体框架

PartMotionEdit 的整体架构遵循“编码—语义交互—部件调制—扩散生成—解码”的流水线设计，其核心思想是将人体运动显式分解为五个预定义部件，并在扩散生成过程中引入部件级自适应调制，从而实现细粒度的文本驱动运动编辑。

### 输入与编码

框架接收两个输入：**源运动序列** $M_{src} \in \mathbb{R}^{T \times D}$（$T$ 帧，每帧 $D=207$ 维特征，包含全局平移、全局朝向及身体姿态）和**文本编辑指令** $P$。
- 源运动通过一个**预训练运动编码器**（冻结）映射为潜在运动特征 $F_m$。
- 文本指令通过一个**预训练 CLIP 文本编码器**（冻结）提取为文本特征 $F_t$。

### 核心可训练模块

编码后的 $F_m$ 与 $F_t$ 依次流经三个可训练模块：

1. **双向运动交互模块（Bidirectional Motion Interaction, BMI）**：通过双向交叉注意力机制对文本特征与运动特征进行动态融合，输出语义对齐的运动表示 $F_m'$。该模块解决了单向或简单融合方式下跨模态信息交换不充分的问题。

2. **部件感知运动调制模块（Part-aware Motion Modulation, PMM）**：以 $F_m'$ 为输入，利用一组可学习的部件查询 $Q_p$（对应五个身体部件：躯干、左臂、右臂、左腿、右腿）通过注意力机制和轻量 Transformer 预测每个部件在各时间帧上的编辑权重矩阵 $R \in [0,1]^{5 \times T}$，并对运动特征施加残差调制，得到 $F_m'' = F_m' + R \odot \text{MLP}(F_m')$。这一步骤使模型能够根据编辑指令对不同的身体部件施加差异化的编辑强度。

3. **扩散模型（DDPM-based Diffusion Model）**：以调制后的运动特征 $F_m''$ 和文本特征 $F_t$ 为条件，在时间潜在空间中进行迭代去噪，生成目标运动的潜在表示。

### 训练监督与解码

训练阶段，PMM 模块额外受到**部件级监督机制（Part-level Supervision Mechanism, PSM）**的约束。PSM 通过计算源运动与目标运动之间五个部件的位置距离与旋转距离，生成经过双层归一化的部件级相似度曲线 $\bar{S}_{i,t}$，作为 PMM 预测权重 $R_{i,t}$ 的回归目标。推理阶段 PSM 不参与计算。

最终，扩散模型输出的潜在表示由**预训练运动解码器**（冻结）解码为目标运动序列 $M_{tgt}$。

### 模块关系总结

整个框架的信息流可概括为：冻结编码器负责特征提取，BMI 负责跨模态语义融合，PMM 负责部件级编辑控制，扩散模型负责高质量运动生成，PSM 在训练中提供部件粒度的辅助监督信号。三个可训练模块（BMI、PMM、扩散模型）协同工作，共同解决了现有全局建模方法在局部编辑控制上的瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2512_24200/figures/001_Figure_1.jpg]]
*Figure 1: Overview of PartMotionEdit. It generates a target motion that modifies the given source motion according to the specified text instructions. It has three trainable core modules: the Bidirectional Motion Interaction (BMI) module, the motion diffusion model, and the Part-aware Motion Modulation (PMM) module with a multi-part similarity curve supervision, and three frozen modules (i.e., the motion encoder, the motion decoder and the CLIP model)*

## 核心模块与公式推导

PartMotionEdit 的核心创新在于将人体运动编辑从全局建模推进到**部件级语义调制**。其可训练部分由三个关键模块构成：双向运动交互（BMI）、部件感知运动调制（PMM）以及一个条件扩散模型，同时辅以训练阶段的部件级相似度监督机制（PSM）。以下重点剖析部件分解、相似度监督、BMI 与 PMM 的公式化设计。

### 1. 人体部件分解与相似度曲线构建

模型首先将 22 关节的人体骨架预定义为五个部件集合：

$$G = \{ \text{Torso}, L_{\text{arm}}, R_{\text{arm}}, L_{\text{leg}}, R_{\text{leg}} \}$$

该分解是后续所有部件级操作的基础。对于训练集中的每对源-目标运动，模型从**空间位置**和**关节旋转**两个维度计算每个部件在每一帧的差异：

$$D_{i,t}^{\text{pos}} = \frac{1}{|g_i|} \sum_{j \in g_i} \| X_{t,j}^{\text{src}} - X_{t,j}^{\text{tgt}} \|_2$$

$$D_{i,t}^{\text{rot}} = \frac{1}{|g_i|} \sum_{j \in g_i} \| R_{t,j}^{\text{src}} - R_{t,j}^{\text{tgt}} \|_2$$

其中 $X_{t,j}$ 和 $R_{t,j}$ 分别表示第 $t$ 帧关节 $j$ 的空间位置和旋转表示。将二者加权融合得到初始相似度（负差异，越大表示越一致）：

$$S_{i,t} = - \big( \beta \cdot D_{i,t}^{\text{pos}} + (1-\beta) \cdot D_{i,t}^{\text{rot}} \big)$$

为消除不同部件间的数值尺度差异并突出序列内的相对变化趋势，PSM 采用**双层归一化**策略。首先进行全局归一化：

$$\hat{S}_{i,t} = \frac{S_{i,t} - S_i^{\min}}{S_i^{\max} - S_i^{\min} + \epsilon}$$

随后在单条运动序列内部进行帧级归一化：

$$\bar{S}_{i,t} = \frac{ \hat{S}_{i,t} - \hat{S}_b^{\min} }{ \hat{S}_b^{\max} - \hat{S}_b^{\min} + \epsilon }$$

最终得到的 $\bar{S}_{i,t}$ 作为训练阶段 PMM 模块的回归目标，引导模型学习预测每个部件的“可编辑性”权重曲线。

### 2. 双向运动交互模块（BMI）

BMI 模块位于运动编码器与 PMM 之间，负责**文本特征与运动特征的双向语义交换**。其输入为 CLIP 文本编码器提取的文本特征 $F_t$ 和预训练运动编码器提取的运动特征 $F_m$。通过两个方向的交叉注意力机制，文本特征注入运动语义，运动特征同时回传空间-时序信息至文本表示，从而输出语义对齐的融合特征 $F_m'$。该设计使得后续的部件调制能够建立在充分交互的跨模态表示之上。

### 3. 部件感知运动调制模块（PMM）

PMM 是模型实现细粒度编辑控制的核心。它接收 BMI 输出的融合运动特征 $F_m' \in \mathbb{R}^{T \times D}$，并引入一组可学习的部件查询向量 $Q_p = \{q_i\}_{i=1}^{N}$（$N=5$）。

**步骤一：部件注意力聚合。** 每个部件查询与所有时间步的运动特征计算注意力分布：

$$A_i = \text{Softmax}\left( \frac{q_i W_q (F_m' W_k)^T}{\sqrt{D}} \right)$$

利用该注意力权重对运动特征进行加权聚合，得到每个部件的紧凑表示：

$$z_i = \sum_{t=1}^{T} A_{i,t} F_m'$$

**步骤二：可编辑性投影。** 将聚合后的部件特征 $\hat{Z} = [z_1, ..., z_N]$ 通过一个轻量 Transformer 编码器（2 层，隐藏维度 256，4 个注意力头）进行交互，随后经 MLP 和 Sigmoid 非线性映射到 $[0,1]$ 区间，生成编辑权重矩阵 $R \in \mathbb{R}^{N \times T}$：

$$R = \sigma \big( W_2 \cdot \text{GELU}( W_1 \cdot \hat{Z} ) \big)$$

**步骤三：部件自适应调制。** 将预测的部件权重作为显式的调制因子，以残差形式作用于原始运动特征：

$$F_m'' = F_m' + R \odot \text{MLP}(F_m')$$

其中 $\odot$ 表示逐元素乘法。这一设计使得模型能够根据编辑指令，在不同时间步对不同身体部件施加**差异化的特征增强或抑制**，从而实现局部编辑而不干扰非目标区域。

### 4. PMM 的训练损失

PMM 的总损失由两部分构成：

$$\mathcal{L}_{\text{PMM}} = \mathcal{L}_{\text{PSM}} + \lambda_s \mathcal{L}_{\text{smooth}}$$

其中 $\lambda_s = 0.1$。$\mathcal{L}_{\text{PSM}}$ 为部件相似度回归损失，强制预测权重 $R_{i,t}$ 逼近 PSM 构建的真实相似度曲线：

$$\mathcal{L}_{\text{PSM}} = \frac{1}{NT} \sum_{i=1}^{N} \sum_{t=1}^{T} \| R_{i,t} - \bar{S}_{i,t} \|_2$$

$\mathcal{L}_{\text{smooth}}$ 为时间平滑正则项，促进相邻帧间部件权重的一致性：

$$\mathcal{L}_{\text{smooth}} = \frac{1}{NT} \sum_{i=1}^{N} \| R_{i,1:T-1} - R_{i,2:T} \|_1$$

### 5. 条件扩散模型

调制后的运动特征 $F_m''$ 与文本特征 $F_t'$ 共同作为条件，输入基于 DDPM 的扩散模型。扩散过程在时间潜在空间中进行迭代去噪，训练目标为标准噪声预测损失：

$$\mathcal{L} = \mathbb{E}_{t, F_m'', \epsilon \sim \mathcal{N}(0,I)} \| \epsilon - \epsilon_\theta(F_m^{(t)}, t, F_t') \|_2$$

最终，去噪后的潜在特征经冻结的预训练运动解码器重建为目标运动序列。

### 补充图表

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2512_24200/figures/002_Figure_2.jpg]]
*Figure 2: Our Bidirectional Motion Interaction (BMI) module takes textual and motion features*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2512_24200/figures/003_Figure_3.jpg]]
*Figure 3: Our Part-aware Motion Modulation (PMM) module processes motion features*

## 实验与分析

### 主实验结果

PartMotionEdit 在 MotionFix 基准上与现有最先进方法进行了系统对比，评估指标采用 MotionFix 标准协议下的生成-目标检索指标（R@1、R@2、R@3、AvgR 等）。如 **Table 1** 所示，PartMotionEdit 在批检索场景下取得了 **R@1 = 73.96**、**AvgR = 1.92** 的优异表现，全面超越已有方法，包括首个文本驱动动态运动编辑基线 **MotionFix**（Athanasiou et al., SIGGRAPH Asia 2024）和引入全局运动相似度预测的 **SimMotionEdit**（Li et al., CVPR 2025）。这一结果表明，部件级调制策略在细粒度运动编辑任务上具有显著优势。

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2512_24200/figures/004_Table_1.jpg]]
*Table 1: Comparison with SOTA text-based motion editing methods on the MotionFix [3] benchmark. We calculate the standard indicator according to MotionFix. Bold represents the best, underline represents the second best, ↑ / ↓ represents higher / lower values are better*

定性对比（**Table 2**）进一步揭示，SimMotionEdit 在处理涉及多部件差异化编辑的指令时，常出现非目标区域被意外干扰的问题（表中以矩形框标注），而 PartMotionEdit 能够更精确地控制编辑范围，保持非编辑部件的运动完整性。

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2512_24200/figures/005_Table_2.jpg]]
*Table 2: Qualitative Results. We compare our method with SimMotionEdit [17]. We outline the limitations of SimMotionEdit using rectangular boxes and annotate the corresponding colors in the prompt*

### 消融实验分析

为验证核心模块的有效性，论文设计了组合消融实验。

**部件感知运动调制（PMM）与部件级相似度监督（PSM）的消融**（**Table 3**）：当同时启用 PMM 模块和 PSM 机制时，生成-目标批检索 R@1 从 70.83 提升至 73.96，AvgR 从 2.31 降至 1.92。这一显著提升表明：部件级相似度曲线监督为模型提供了精确的局部编辑学习信号，而 PMM 模块则利用这些信号实现了自适应部件权重调制，两者协同作用是实现细粒度编辑控制的关键。

**双向跨模态交互（BMI）模块的消融**（**Table 4**）：移除 BMI 模块后，运动质量指标 M-Score 从 -4.114 下降至 -4.432，R@1 从 73.96 下降至 72.08。这表明双向交叉注意力机制在文本-运动特征融合中发挥了重要作用——单向或简单融合无法充分交换语义信息，导致编辑指令的语义对齐精度下降，进而损害生成运动的质量。

### 失败模式与局限性

尽管 PartMotionEdit 在定量和定性评估中表现优异，论文也指出了当前方法的若干局限：

1. **部件相似度计算的语义局限性**：当前部件相似度依赖显式的几何距离度量（关节位置的欧氏距离 $D_{i,t}^{pos}$ 和旋转变化的欧氏距离 $D_{i,t}^{rot}$，见 Eq. 2-4）。这种度量方式无法捕捉高层的语义关系，例如抽象的运动风格或动作意图。当编辑指令涉及“更优雅地挥手”这类风格层面的描述时，几何度量可能无法提供有效的监督信号。

2. **序列编辑能力的缺失**：当前框架仅支持单次编辑操作，缺乏记忆机制来维护多次连续编辑之间的一致性。在需要逐步修改运动序列的实际应用场景中，这一限制尤为突出。

3. **部件粒度的泛化性待验证**：PMM 模块基于预定义的五个身体部件（躯干、左臂、右臂、左腿、右腿，见 Eq. 1 的 $G$）进行调制。该部件查询机制能否泛化到更细粒度的关节级别编辑，或适应任意的部件组合，尚需进一步探索。

### 实验公平性说明

所有对比实验均在 MotionFix 数据集的标准评估协议下进行，使用相同的训练/验证/测试划分，确保了比较的公平性。实验设置中，运动特征通过预训练编码器映射到 512 维嵌入空间，PMM 模块采用两层 Transformer 编码器结构（256 隐藏维度，4 注意力头），扩散模型基于 DDPM 框架在时间潜在空间进行迭代去噪。

### 补充图表

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2512_24200/figures/006_Table_3.jpg]]
*Table 3: We conducted a combined ablation study on the Motion Part-Aware Modulation (PMM) module and the Part-level similarity curve supervision mechanism (PSM) to verify their necessity*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2512_24200/figures/007_Table_4.jpg]]
*Table 4: To validate the importance of the Bidirectional Motion Interaction (BMI) module, we removed it from the full model (Ours) to have the one without BMI (w/o BMI), and compared its motion quality (M-Score) with the ground truth (GT) as well*

## 方法谱系与知识库定位

### 1. 任务定位与基线谱系

PartMotionEdit 聚焦于**文本驱动的 3D 人体运动编辑**任务：给定源运动序列和自然语言编辑指令，生成符合指令语义且保持非目标区域不变的目标运动。该任务由 **MotionFix**（Athanasiou et al., SIGGRAPH Asia 2024）正式定义，并提供了首个专用数据集与基于条件扩散模型的编辑基线。

在 PartMotionEdit 之前，该方向的代表性工作为 **SimMotionEdit**（Li et al., CVPR 2025）。SimMotionEdit 在条件扩散框架中引入了一个**运动相似度预测**辅助任务——模型需预测源运动与目标运动之间的全局相似度曲线，以此增强文本-运动语义对齐。然而，这一相似度监督建立在**全身姿态**粒度上，未分解到关节或部件级别。当编辑指令涉及多个需要差异化处理的部件时（例如“左手抬起，同时右腿保持不动”），全局相似度无法为不同部件提供有区分度的控制信号，导致局部编辑精度不足，且容易干扰非目标区域。

PartMotionEdit 的改进思路直接针对这一瓶颈：将相似度监督从**全局粒度**下沉到**部件粒度**，并配套设计显式的部件感知调制机制，使模型能够学习“哪些部件需要编辑、编辑到什么程度”。

### 2. 方法继承与关键改造

PartMotionEdit 继承了 SimMotionEdit 的**条件扩散编辑范式**（以源运动潜在特征和文本特征为条件，在时间潜在空间进行迭代去噪生成目标运动），但在以下三个关键槽位上进行了结构性改造：

| 改造槽位 | 基线方案（SimMotionEdit） | PartMotionEdit 方案 | 证据锚点 |
|----------|--------------------------|---------------------|----------|
| **运动相似度监督粒度** | 全局人体相似度曲线 | 五个身体部件级别的相似度曲线，带有双层归一化（PSM） | Section 3.2, Eq.(1)-(6) |
| **运动特征调制机制** | 无显式部件调制，仅使用全局特征生成 | 部件感知运动调制模块（PMM），动态预测每个部件的编辑权重并进行残差调制 | Section 3.4, Fig. 3, Eq.(7)-(10) |
| **文本-运动交互方式** | 单向或简单融合（原文未详述） | 双向跨模态注意力机制（BMI），进行双向语义交换 | Section 3.3, Fig. 2 |

这三个改造构成了 PartMotionEdit 的核心技术贡献，其因果链条可概括为：

> **部件分解（PSM）→ 部件感知调制（PMM）→ 语义对齐增强（BMI）→ 精细局部编辑**

具体而言：
- **PSM** 提供训练阶段的部件级监督信号，使模型学会区分不同部件的编辑需求；
- **PMM** 利用可学习的部件查询和轻量 Transformer 显式预测五个部件的编辑权重 $R \in [0,1]^{5 \times T}$，并通过残差调制 $F_m'' = F_m' + R \odot \text{MLP}(F_m')$ 作用于运动特征；
- **BMI** 通过双向交叉注意力实现文本特征与运动特征的动态融合，确保调制后的运动特征与编辑指令保持语义一致。

### 3. 适用边界与局限

**适用边界：**
- 任务限定为**单条运动序列的单次编辑**，不支持序列化连续编辑；
- 部件分解基于预定义的**五部件骨架划分**（躯干、左臂、右臂、左腿、右腿），覆盖 22 关节人体骨架，尚未验证向更细粒度（如单关节级别）或任意部件组合的泛化能力；
- 训练和评估均在 MotionFix 数据集的标准划分下进行，跨数据集或跨骨架拓扑的迁移能力未经检验。

**已知局限（原文明确指出的）：**
1. **部件相似度计算依赖显式几何度量**：当前 PSM 使用关节位置和旋转的欧氏距离（Eq.(2)-(4)）来定义部件相似度，无法捕捉高层的语义关系（如抽象风格、动作意图或情感表达）。这意味着对于“走得更自信”这类抽象指令，部件相似度曲线的监督信号可能不够精确。
2. **缺乏序列编辑记忆机制**：方法未处理多次编辑之间的状态维护问题，无法在连续编辑场景中保持一致性。
3. **部件查询的泛化性未验证**：PMM 模块的五组可学习部件查询是否能够适应不同的部件划分策略或扩展到关节级别编辑，仍为开放问题。

### 4. 开放问题与后续方向

基于上述局限，论文指向以下开放研究方向：

1. **语义级部件相似度学习**：能否超越显式几何度量，通过学习的方式获取语义层面的部件相似度表示？这可能需要引入对比学习或基于大规模运动-语言预训练模型的语义对齐策略。

2. **连续编辑与记忆机制**：如何将 PartMotionEdit 的部件调制框架扩展到需要长序列上下文和状态记忆的连续编辑任务？这涉及在多次编辑间维护和更新部件状态表示。

3. **更灵活的部件粒度控制**：当前五部件分解是固定的先验划分。能否让模型自动发现编辑相关的部件组合，或支持用户自由指定任意关节子集作为编辑目标？这需要重新设计部件查询的初始化和聚合机制。

4. **跨骨架泛化**：现有部件分解依赖于 22 关节的人体骨架拓扑，向不同关节数量和拓扑结构的骨架（如手部、动物骨架）迁移时，部件定义和相似度计算都需要重新设计。

## 原文 PDF

![[paperPDFs/arxiv_2025/PartMotionEdit_Fine_Grained_Text_Driven_3D_Human_Motion_Editing_via_Part_Level_Modulation.pdf]]