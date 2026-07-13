---
title: "Transferring Labels to Solve Annotation Mismatches Across Object Detection Datasets"
type: paper
paper_level: A
venue: ICLR
year: 2024
pdf_ref: paperPDFs/ICLR_2024/Transferring_Labels_to_Solve_Annotation_Mismatches_Across_Object_Detection_Datasets.pdf
project_link: https://andrewliao11.github.io/label-transfer
code_link: null
aliases:
- LGPLL
- TLSAMAODD
tags:
- ICLR_2024
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: "训练一个标签迁移模型，将源数据集的标签（边界框与类别）转换为符合目标数据集标注协议的样式，从而对齐标注差异。"
primary_logic: "利用两阶段检测器的RPN和RoI头，将其重新设计为框生成器（box generator）和标签迁移模型（label transfer model）；框生成器在源数据集上训练以产生源风格的候选框，标签迁移模型在目标数据集上学习将这些候选框映射为目标风格的边界框，并判断标签的有效性，从而在无配对监督的情况下实现数据驱动的标签迁移。"
claims:
- "LGPL在所有四个场景和三种检测器架构上均优于所有基线方法，并且是唯一始终优于“No transfer”的方法，平均提升1.88 mAP和2.65 AP75。"
- "LGPL在多源标签迁移场景中也一致优于所有基线，且超过现成的监督域适应方法（S‑DANN和S‑CycConf）1.6和1.24 mAP。"
- "nuScenes → nuImages (10 classes) 上 mAP = 42.6 (Faster‑RCNN)"
- "Synscapes → Cityscapes (7 classes) 上 mAP = 39.71 (Faster‑RCNN)"
---

# Transferring Labels to Solve Annotation Mismatches Across Object Detection Datasets

> [!tip] 核心洞察
> 利用两阶段检测器的RPN和RoI头，将其重新设计为框生成器（box generator）和标签迁移模型（label transfer model）；框生成器在源数据集上训练以产生源风格的候选框，标签迁移模型在目标数据集上学习将这些候选框映射为目标风格的边界框，并判断标签的有效性，从而在无配对监督的情况下实现数据驱动的标签迁移。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 跨目标检测数据集的标签迁移解决标注失配 |
| 英文题名 | Transferring Labels to Solve Annotation Mismatches Across Object Detection Datasets |
| 会议/期刊 | ICLR 2024 |
| Links | [paper](https://openreview.net/pdf?id=ChHx5ORqF0) · [Project](https://andrewliao11.github.io/label-transfer) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | Label‑Guided Pseudo‑Labeling (LGPL) |
| Dataset | nuScenes → nuImages (10 classes), Synscapes → Cityscapes (7 classes), Internal‑Dataset → nuImagest (3 classes), MVD‑ + nuImages‑ → Waymo‑ (1 class, multi‑source) |

> [!tip] 效果简介
> - nuScenes → nuImages (10 classes) 上，mAP 为 42.6 (Faster‑RCNN)，对比 41.25 (No transfer)，变化 +1.35。
> - Synscapes → Cityscapes (7 classes) 上，mAP 为 39.71 (Faster‑RCNN)，对比 38.74 (No transfer)，变化 +0.97。
> - Internal‑Dataset → nuImagest (3 classes) 上，mAP 为 48.89 (Faster‑RCNN)，对比 47.91 (No transfer)，变化 +0.98。

## 概要

不同目标检测数据集之间存在普遍的标注协议差异，包括类语义分歧、标注指令不一致、人机偏差以及跨模态标签等因素，导致标注失配（annotation mismatch）。直接混合使用这些数据集的原始标签训练检测器，不仅无法提升下游性能，反而可能造成损害。

针对这一问题，本文提出一种以数据为中心的方法 **Label‑Guided Pseudo‑Labeling (LGPL)**。LGPL 将标准的两阶段检测器架构重新设计为标签迁移模型：利用在源数据集上训练的框生成器（box generator）产生源风格的候选区域，再通过目标数据集训练的标签迁移模型（label transfer model）将这些候选框映射为符合目标标注协议的结果，并同时给出有效性分数。整个过程无需配对监督，即可实现数据驱动的标签迁移。

核心结论：
- LGPL 在四个标注失配场景、三种检测器架构（Faster‑RCNN、YOLOv3、Deformable DETR）上均一致优于所有基线方法，是唯一始终优于“No transfer”的方法，平均提升 **1.88 mAP** 和 **2.65 AP75**。
- 在多源标签迁移场景中，LGPL 同样一致优于所有基线，且相比监督域适应方法 S‑DANN 和 S‑CycConf 分别平均提升 **1.6** 和 **1.24 mAP**。
- 直接评估迁移标签质量的 Transfer‑mAP 与下游 mAP 之间的 Spearman 相关系数仅为 0.6（p > 0.1），相关性不显著，说明下游评估对于标签迁移方法至关重要。

方法定位：LGPL 属于数据驱动的标签迁移范式，与基于统计归一化、伪标签、通用分割模型（如 SAM）以及图像域适应等现有方案相比，LGPL 通过联合优化框生成器和标签迁移模型，更全面地捕捉了标注协议的差异。



### 标注失配：目标检测中的隐性瓶颈

现代目标检测器的性能高度依赖大规模标注数据。然而，不同数据集的标注协议——包括类语义定义、标注指令、人机偏差和跨模态标签——往往存在显著差异，导致所谓的**标注失配**（annotation mismatch）。例如，对于“骑行者”这一类别，MVD、nuImages 和 Waymo 三个数据集的定义互不一致：有的将摩托车与骑手分开标注，有的则合并为一个框；有的标注人行道上的自行车，有的则忽略。当研究者试图混合多个数据集以扩充训练样本时，这些不一致的标签会直接损害下游检测器的性能。

论文系统地将标注失配归为四类因素（Figure 2）：
- **类语义（Class Semantics）**：同一名称在不同数据集中对应不同的视觉概念。
- **标注指令（Annotation Instructions）**：标注员遵循的规则不同，如遮挡物体的处理方式。
- **人机偏差（Human-Machine Misalignment）**：人工标注与自动标注之间的系统偏差。
- **跨模态标签（Cross-Modality Labels）**：不同传感器模态产生的标签差异。

### 现有方法的缺口

面对标注失配，最直接的做法是“不做任何处理”（No transfer），即直接使用原始源标签与目标数据混合训练。令人意外的是，这一简单基线在多数场景下反而优于许多精心设计的标签迁移方法（Table 1），说明标注失配是一个难以轻易绕过的瓶颈。

已有的应对策略存在明显局限：
- **统计归一化**（Statistical Normalization）：仅对源边界框进行缩放以匹配目标数据集的宽高统计，完全忽略图像内容，结果经常低于 No transfer。
- **伪标签方法**（Pseudo‑labeling 及其噪声过滤变体）：用仅在目标数据集上训练的检测器为源图像生成伪标签，但由于目标检测器本身缺乏源数据的标注知识，这些方法经常表现不如 No transfer。
- **监督域适应**（如 S‑DANN 和 S‑CycConf）：通过对齐源和目标实例特征来适应图像域差异，但未直接解决标注协议层面的不一致。

这些方法的共同缺陷在于：它们要么只做浅层统计对齐，要么依赖目标模型自身的有限知识，均未能系统性地建模源标注协议与目标标注协议之间的映射关系。

### 本文动机与核心思路

本文的核心洞察是：**标注失配本质上是两个标注函数之间的差异问题，而非单纯的图像域偏移问题。** 因此，解决之道在于学习一个从源标注协议到目标标注协议的映射函数——即**标签迁移模型**（label transfer model）。

具体而言，论文提出了一种数据驱动的方法 **Label‑Guided Pseudo‑Labeling (LGPL)**，其关键设计在于：
- **无需配对监督**：不要求同一图像同时拥有源标注和目标标注，仅需源数据集和目标数据集各自的独立标注。
- **重用两阶段检测器架构**：将标准的两阶段检测器重新设计为框生成器（box generator）和标签迁移模型（label transfer model）。框生成器在源数据上训练以产生源风格的候选区域；标签迁移模型在目标数据上学习将这些候选框映射为目标风格的边界框，并判断标签的有效性。
- **以数据为中心**：标签迁移作为预处理步骤，与下游检测器的学习算法和模型架构解耦，具有广泛的适用性。

这一思路将标注失配从一个隐性的数据问题转化为一个可显式优化的学习问题，为跨数据集的目标检测训练提供了新的范式。



## 核心方法与创新机理

### 问题瓶颈与因果调控变量

目标检测数据集的标注协议差异——包括类语义（class semantics）、标注指令（annotation instructions）、人机偏差（human-machine misalignment）和跨模态标签（cross-modality labels）——导致标注失配（annotation mismatch），使得直接混合源数据集与目标数据集训练会损害下游检测器性能。现有方案（如统计归一化、伪标签、域适应）均无法一致地解决该问题：Table 1 显示，多数基线方法甚至无法超越直接使用原始标签的“No transfer”方案。

LGPL 的核心因果调控变量是**训练一个标签迁移模型**，将源数据集的边界框与类别标签转换为符合目标数据集标注协议的样式，从而在数据层面消除标注失配，而非依赖检测器架构或训练策略的修改。

### 关键洞察：将两阶段检测器重新设计为标签迁移流水线

LGPL 的核心洞察在于**重新利用标准两阶段目标检测器的架构组件**，将其改造为无需配对监督的标签迁移系统。具体而言：

- **框生成器（box generator）**：即标准 RPN，仅在源数据集上训练，学习生成源风格的候选区域。其关键作用是为目标数据集图像提供“源视角”的提案框，作为标签迁移模型的输入。
- **标签迁移模型（label transfer model）**：改进的 RoI 头，在目标数据集上训练，学习将源风格的候选框映射为目标风格的边界框，并输出有效性分数（validity score）判断该标签在目标协议下是否成立。

训练时的核心技巧是**停止梯度（stop gradient）**：对目标数据集图像经框生成器产生的提案框施加停止梯度操作，防止目标数据集的梯度反向传播至框生成器，从而保证框生成器始终维持源数据集的标注风格，避免目标标注偏差污染源风格提案的生成。

### 关键 changed slot：从原始标签到标签迁移数据集

LGPL 相对于基线方法的核心 changed slot 体现在两个层面：

**1. 源数据集标签处理（标签迁移 vs. 原始标签）**

基线方法直接使用原始源标签（No transfer）、仅做统计缩放（Statistical Normalization）、或用目标模型生成伪标签（PL/PL&NF）。LGPL 则通过训练好的标签迁移模型，对源数据集的每个标签 $(b, c)$ 输出精修后的边界框 $\hat{b}$ 和有效性分数 $\hat{s}$，并通过类别级阈值 $\sigma_c$ 过滤后构建标签迁移后的源数据集：

$$ \mathcal{D}_{\text{transferred-src}} := \{(x, \hat{b}, c) \mid \hat{s} \geq \sigma_c\} $$

这一设计使得源标签既能在定位上对齐目标协议（修正过大/过小框、合并或拆分标注），又能在语义上过滤不符合目标协议的标签（如移除全遮挡物体、非目标类别的标注）。

**2. 训练方式（联合训练 vs. 分别/混合训练）**

LGPL 同时训练三个组件——共享图像编码器 $f_{\text{img}}$、框生成器 $f_{\text{gen}}$、标签迁移模型 $f_{\text{trans}}$——通过联合优化目标：

$$ \begin{array} { r l } { f _ { \mathrm { i m g } } ^ { * } , f _ { \mathrm { g e n } } ^ { * } , f _ { \mathrm { t r a n s } } ^ { * } \gets \operatorname * { a r g m i n } \sum _ { x , y \in \mathcal { D } _ { \mathrm { s r c } } } \mathcal { L } _ { \mathrm { R P N } } ( x , y , f _ { \mathrm { i m g } } , f _ { \mathrm { g e n } } ) + \sum _ { x , y ^ { \prime } , y \in \mathcal { D } _ { \mathrm { t r a n s } } } \mathcal { L } _ { \mathrm { R o I } } ( x , y ^ { \prime } , y , f _ { \mathrm { i m g } } , f _ { \mathrm { t r a n s } } ) } \end{array} $$

其中 $\mathcal{D}_{\text{trans}}$ 由目标图像、停止梯度的源风格提案框和随机类别标签构成，目标为真实目标标签。这种设计使得标签迁移模型在无配对监督（即无同一图像的源标注与目标标注配对）的情况下，通过数据驱动方式学习标注协议的映射关系。

### 与基线方法的本质差异

- **vs. Statistical Normalization**：仅做边界框尺度的统计对齐，忽略图像内容与语义差异，Table 1 中多数场景表现不如 No transfer。
- **vs. PL/PL&NF**：伪标签方法依赖仅在目标数据集上训练的检测器，无法获取源标注中的信息增益，且噪声过滤依赖源标签质量，Table 1 中频繁劣于 No transfer。
- **vs. SAM-transfer**：SAM 分割基础模型虽能产生精确的类不可知分割掩码，但 Table 5 显示其下游 mAP 在 38 左右停滞，远低于 LGPL 的 42.6，说明仅修正定位误差不足以解决标注失配——类别语义和有效性判断同样关键。
- **vs. 域适应方法（S-DANN、S-CycConf）**：Figure 4 显示 LGPL 平均超过 S-DANN 1.6 mAP、超过 S-CycConf 1.24 mAP，表明在标签空间对齐比在特征空间对齐更有效。

### 证据强度

LGPL 是唯一在四个标注失配场景（Table 1）、多源标签迁移（Table 2）、三种检测器架构（YOLOv3、Deformable DETR、Faster‑RCNN）上均一致超越“No transfer”的方法，平均提升 1.88 mAP 和 2.65 AP75（Abstract）。三个随机种子下的标准差不超过 0.33，表明提升稳健（Table 10）。



LGPL 的整体设计围绕一个核心思路展开：**将标签迁移建模为一个数据驱动的转换过程，在不依赖配对监督的情况下，把源数据集的标注协议映射到目标数据集的标注协议**。为此，LGPL 复用了标准两阶段检测器的架构组件，将其重新组织为三个协同工作的模块。

### 模块组成与职责

LGPL 由三个功能模块构成：

- **图像编码器** $f_{\mathrm{img}}$：提取共享的图像特征，供框生成器与标签迁移模型共同使用。该编码器在源数据集和目标数据集上联合训练，使得特征表示能够同时服务两个子任务。
- **框生成器** $f_{\mathrm{gen}}$：本质上是标准 RPN（Region Proposal Network），在源数据集上训练以学习生成“源风格”的候选区域。其关键作用在于：为任意输入图像（包括目标数据集图像）提供符合源标注协议的边界框提案，作为后续标签迁移模型的输入。
- **标签迁移模型** $f_{\mathrm{trans}}$：改进的 RoI 头，接收图像特征、源风格候选框以及类别信息，输出两个结果：（1）精修后的边界框，使其符合目标数据集的标注协议；（2）有效性分数，用于判断该标签在目标协议下是否应当保留。

### 数据流与训练流程

LGPL 的训练过程在两个数据集上并行进行，数据流如下：

1. **源数据集训练**：框生成器 $f_{\mathrm{gen}}$ 与图像编码器 $f_{\mathrm{img}}$ 在源数据集 $\mathcal{D}_{\mathrm{src}}$ 上通过标准 RPN 损失 $\mathcal{L}_{\mathrm{RPN}}$ 进行优化，使框生成器学会产生源风格的候选区域。

2. **目标数据集训练**：标签迁移模型 $f_{\mathrm{trans}}$ 在目标数据集 $\mathcal{D}_{\mathrm{tgt}}$ 上通过 RoI 损失 $\mathcal{L}_{\mathrm{RoI}}$ 进行训练。训练样本的构造方式是：对目标图像 $x$，先用框生成器产生源风格候选框，但通过**停止梯度**操作 $\mathrm{StopGrad}(f_{\mathrm{gen}}(x))$ 切断梯度回传，防止目标数据影响框生成器的源风格特性；同时为每个候选框随机分配一个类别标签 $c$ 作为输入。标签迁移模型学习将这些“源风格框+随机类别”映射为目标数据集的金标准标注 $y$。

联合训练目标的形式化为：

$$
\begin{array} { r l } { f _ { \mathrm { i m g } } ^ { * } , f _ { \mathrm { g e n } } ^ { * } , f _ { \mathrm { t r a n s } } ^ { * } \gets \operatorname * { a r g m i n } \sum _ { \substack { f _ { \mathrm { i m g } } , f _ { \mathrm { g e n } } , f _ { \mathrm { t r a n s } } } } \sum _ { \substack { x , y \in \mathcal { D } _ { \mathrm { s r c } } } } \mathcal { L } _ { \mathrm { R P N } } ( x , y , f _ { \mathrm { i m g } } , f _ { \mathrm { g e n } } ) + \sum _ { \substack { x , y ^ { \prime } , y \in \mathcal { D } _ { \mathrm { t r a n s } } } } \mathcal { L } _ { \mathrm { R o I } } ( x , y ^ { \prime } , y , f _ { \mathrm { i m g } } , f _ { \mathrm { t r a n s } } ) } \\ & { \qquad \mathcal { D } _ { \mathrm { t r a n s } } \gets \{ ( x , [ \mathrm { S t o p G r a d s } ( f _ { \mathrm { g e n } } ( x ) ) , c ] , y ) | c \sim [ K ] ^ { | f _ { \mathrm { g e n } } ( x ) | } , ( x , y ) \in \mathcal { D } _ { \mathrm { t g t } } \} } \end{array}
$$

### 推理与标签迁移数据集构建

训练完成后，标签迁移模型 $f_{\mathrm{trans}}$ 用于处理源数据集中的每张图像：以源图像的原始标签（边界框+类别）作为输入，输出精修后的目标风格边界框及对应的有效性分数 $\hat{s}$。通过类别级阈值 $\sigma_c$ 过滤低置信度的标签，构建标签迁移后的源数据集：

$$
\mathcal{D}_{\mathrm{transferred\text{-}src}} := \{(x, \hat{b}, c) \mid \hat{s} \geq \sigma_c\}
$$

该迁移后的源数据集与目标数据集合并，用于训练下游检测器。整个标签迁移过程作为数据预处理步骤，与下游检测器的学习算法和模型架构无关。

### 关键设计决策

- **停止梯度**：在目标数据集上对框生成器的输出施加停止梯度，确保框生成器始终维持源风格的候选区域生成能力，避免目标数据的标注偏差“污染”框生成器。
- **随机类别输入**：在训练标签迁移模型时，为每个候选框随机分配类别标签，迫使模型学习从任意类别输入中提取有效的迁移映射，而非简单记忆类别对应关系。
- **有效性分数与类别级阈值**：标签迁移模型不仅输出精修框，还输出有效性分数，用于判断源标签在目标协议下是否应当保留。类别级阈值的设计考虑了不同类别在标注协议上的差异程度可能不同。



### 标签迁移模型的形式定义

LGPL的核心在于训练一个**标签迁移模型**（Label Transfer Model），其形式定义为：

$$f_{\mathrm{trans}} : \mathcal{X} \times \mathcal{Y} \to \mathcal{Y}$$

该函数以源数据集中的图像-标签对 $(x, y_{\mathrm{src}})$ 为输入，输出符合目标数据集标注协议的边界框与类别标签。理想的标签迁移模型应满足以下条件：

$$\forall x \in \mathcal{D}_{\mathrm{src}}, \quad f_{\mathrm{trans}}(x, g_{\mathrm{src}}(x)) = g_{\mathrm{tgt}}(x)$$

其中 $g_{\mathrm{src}}$ 和 $g_{\mathrm{tgt}}$ 分别为源数据集和目标数据集的标注函数。该条件要求：对于源数据集中的任意图像，迁移后的标签应与目标标注者在该图像上产生的金标准标签完全一致。然而，由于缺乏成对的监督信号（即 $(x, y_{\mathrm{src}}, y_{\mathrm{tgt}})$ 三元组），直接训练 $f_{\mathrm{trans}}$ 不可行，这构成了LGPL需要解决的核心技术挑战。

### LGPL的三大核心模块

LGPL通过重新利用两阶段检测器的架构组件来解决上述无配对监督问题，整个框架由三个模块组成（参见Figure 3）：

1. **图像编码器 $f_{\mathrm{img}}$**：提取共享的图像特征表示，供框生成器与标签迁移模型共同使用。该模块确保两个下游模块在统一的特征空间上运作。

2. **框生成器 $f_{\mathrm{gen}}$**：本质上是标准RPN（Region Proposal Network），仅在源数据集 $\mathcal{D}_{\mathrm{src}}$ 上训练。其功能是为任意输入图像生成**源风格的候选区域**（source-like bounding regions）。在训练标签迁移模型时，框生成器为目标数据集图像 $\mathcal{D}_{\mathrm{tgt}}$ 产生提案框，这些提案框模拟了源标注协议下的边界框分布特征。

3. **标签迁移模型 $f_{\mathrm{trans}}$**：改进的RoI头（RoI head），接收三个输入——源风格的候选框、随机分配的类别标签、以及图像特征——输出两个关键信息：(1) 符合目标协议的精修边界框；(2) 该边界区域在目标数据集中的**有效性分数**（validity score），用于判断该区域是否应被目标协议标注。

### 联合训练目标

LGPL的关键创新在于：框生成器和标签迁移模型的训练是**解耦但联合进行**的。具体而言，框生成器仅在源数据集上优化，而标签迁移模型仅在目标数据集上学习目标协议的标注偏差。完整的联合训练目标如下：

$$
\begin{array} { r l } 
f_{\mathrm{img}}^{*}, f_{\mathrm{gen}}^{*}, f_{\mathrm{trans}}^{*} \gets 
\operatorname*{argmin} & \displaystyle\sum_{x, y \in \mathcal{D}_{\mathrm{src}}} \mathcal{L}_{\mathrm{RPN}}(x, y, f_{\mathrm{img}}, f_{\mathrm{gen}}) \\
& + \displaystyle\sum_{x, y', y \in \mathcal{D}_{\mathrm{trans}}} \mathcal{L}_{\mathrm{RoI}}(x, y', y, f_{\mathrm{img}}, f_{\mathrm{trans}})
\end{array}
$$

其中，训练标签迁移模型所需的数据集 $\mathcal{D}_{\mathrm{trans}}$ 通过以下方式动态构造：

$$\mathcal{D}_{\mathrm{trans}} \gets \{ (x, [\mathrm{StopGrad}(f_{\mathrm{gen}}(x)), c], y) \mid c \sim [K]^{|f_{\mathrm{gen}}(x)|}, (x, y) \in \mathcal{D}_{\mathrm{tgt}} \}$$

**公式变量含义解析**：
- $\mathcal{L}_{\mathrm{RPN}}$：标准RPN损失，训练框生成器在源数据集上产生源风格的提案区域。
- $\mathcal{L}_{\mathrm{RoI}}$：RoI头损失，训练标签迁移模型将源风格提案映射为目标风格的边界框，并学习预测有效性分数。
- $\mathrm{StopGrad}(\cdot)$：停止梯度算子，应用于目标数据集图像上的框生成器输出，**防止目标数据集的梯度回传到框生成器**，确保框生成器始终维持源风格提案的生成能力。
- $c \sim [K]^{|f_{\mathrm{gen}}(x)|}$：为每个提案随机分配一个类别标签（$K$ 为类别总数）。这一设计使得标签迁移模型学习到：类别信息本身并不决定边界框的迁移方式，迁移的核心在于学习目标协议的标注偏差。
- $y$：目标数据集在该图像上的真实标注，作为RoI头的监督信号。

### 标签迁移后的数据集构造

训练完成后，LGPL使用标签迁移模型对源数据集进行批量处理：对于每张源图像 $(x, y_{\mathrm{src}}) \in \mathcal{D}_{\mathrm{src}}$，标签迁移模型输出迁移后的边界框 $\hat{b}$ 和有效性分数 $\hat{s}$。最终构造的标签迁移源数据集为：

$$\mathcal{D}_{\mathrm{transferred\text{-}src}} := \{ (x, \hat{b}, c) \mid \hat{s} \geq \sigma_c \}$$

其中 $\sigma_c$ 是类别相关的有效性阈值，通过分箱策略（Sturges, 1926）在验证集上选择。低于阈值的边界框被视为不符合目标协议而被丢弃，从而实现了**自动的标注清洗与对齐**。



## 实验与关键发现

### 核心实验设置

实验覆盖四个标注失配场景，涉及五个真实数据集（nuScenes、nuImages、Waymo、Cityscapes、MVD）和两个合成数据集（Synscapes、Internal‑Dataset），并在三种不同架构的检测器（YOLOv3、Deformable DETR、Faster‑RCNN）上验证。下游检测器超参数通过网格搜索公平选择，所有方法共享相同搜索空间；每个设置运行三个不同随机种子（Deformable DETR除外），LGPL标准差不超过0.33。标签迁移模型使用与基线相同的Cascade‑RCNN和HRNet‑w32骨干网络，避免架构差异带来的不公平比较。

### 主实验结果

**Table 1** 报告了四个场景下三种检测器使用不同标签迁移方法后的下游mAP。LGPL在所有场景和架构上均优于所有基线方法，是唯一始终优于“No transfer”的方法。在Faster‑RCNN上，nuScenes→nuImages场景提升1.35 mAP（42.6 vs. 41.25），Synscapes→Cityscapes提升0.97 mAP（39.71 vs. 38.74），Internal‑Dataset→nuImages提升0.98 mAP（48.89 vs. 47.91）。YOLOv3和Deformable DETR架构上的增益更为显著，nuScenes→nuImages场景分别提升3.56和1.87 mAP。

**Table 2** 展示了多源标签迁移场景（MVD‑ + nuImages‑ → Waymo‑，单类“cyclist”）。LGPL在所有架构上依然优于所有基线：Faster‑RCNN提升1.61 mAP（32.74 vs. 31.14），YOLOv3提升2.88 mAP，Deformable DETR提升1.74 mAP。

**Table 3** 报告了高IoU指标AP75的结果。LGPL在nuScenes→nuImages上提升1.5 AP75（44.63 vs. 43.13），在多源场景MVD‑+nuImages‑→Waymo‑上提升1.8 AP75（36.66 vs. 34.86），表明LGPL不仅提升整体检测精度，也能输出更精确的定位框。

**Figure 4** 对比了LGPL与监督域适应方法（S‑DANN和S‑CycConf，Prabhu et al., 2023）。LGPL平均超越S‑DANN 1.6 mAP，超越S‑CycConf 1.24 mAP，说明数据驱动的标签迁移比图像域适应更有效地解决了标注失配问题。

### 基线方法的失败模式

**Table 1** 揭示了一个反直觉现象：大多数基线方法（SN、PL、PL & NF）经常表现不如“No transfer”（直接使用原始源标签）。具体而言：

- **统计归一化（SN）**仅缩放边界框的高宽以匹配目标数据集的统计分布，完全忽略图像内容，在多个场景下结果低于No transfer（Table 1中红色标注行）。这说明单纯的统计对齐不足以捕捉标注协议的语义差异。
- **伪标签方法（PL）及噪声过滤版本（PL & NF）**用仅在目标数据集上训练的检测器为源图像生成伪标签，经常表现不如No transfer（Table 1、2、3中PL和PL & NF行多处红色标注）。原因在于目标模型本身的信息量有限，无法纠正源数据集标注中的系统性偏差，反而可能引入新的噪声。
- **SAM‑transfer模型**（Kirillov et al., 2023）虽能产生准确的类不可知分割掩码，但其下游mAP在nuScenes→nuImages场景中约38即停滞，远低于LGPL的42.6（Table 5）。这表明仅修正定位误差不足以完全解决标注失配——类别语义和标注指令的差异同样关键。

![[assets/figures/papers/paper_list_l28_https_openreview_net_pdf_id_ChHx5ORqF0/figures/004_Table_1.jpg]]
*Table 1: Downstream-mAP of detectors trained with transferred labels. LGPL outperforms all baselines on all scenarios and architectures. Surprisingly, most baselines consistently fail to outperform‘No transfer' and LGPL is the only approach that consistently beats ‘No transfer'.We use smallfont to denote the mAP difference versus‘No transfer',red color to indicate methods that are worse than ‘No transfer',and bold the best performing label transfer models*

![[assets/figures/papers/paper_list_l28_https_openreview_net_pdf_id_ChHx5ORqF0/figures/010_Table_5.jpg]]
*Table 5: Downstream-mAP of SAMadopted label transfer models*

### 消融与分析

**评价指标的相关性**：Table 4分析了直接评估迁移标签质量的Transfer‑mAP（计算转移标签与人工金标准标签的mAP）与下游mAP之间的Spearman相关系数，仅为0.6（p>0.1），相关性不显著。这意味着仅靠标签层面的匹配度无法可靠预测下游检测器的实际性能提升，验证了以下游性能为最终评价标准的必要性。

**标注失配的TIDE误差分解**：Table 9使用TIDE（Bolya et al., 2020）分析原始源标签与金标准标签之间的误差来源。不同场景的挑战重点不同：某些场景以定位误差为主，另一些则以背景误分类为主，说明标注失配是多维度的复合问题。

**定性结果**：Figure 5至Figure 9展示了各场景下的标签迁移定性案例。LGPL能成功修正过大框（nuScenes→nuImages）、移除全遮挡物体、通过低置信度移除不符合目标协议的对象（如人行道上的自行车，nuImages→Waymo），并将摩托车与骑行者合并为单一框（MVD→Waymo）。但在歧义较大的案例（如行人推自行车时是否标注为骑行者）中，数据驱动的LGPL可能产生错误决定，而某些基于规则的基线反而能正确移除标签（Figure 8最后一行）。

### 关键数据锚点

- 平均提升：1.88 mAP，2.65 AP75（Abstract）
- nuScenes→nuImages，Faster‑RCNN：42.6 vs. 41.25（+1.35 mAP）
- Synscapes→Cityscapes，Faster‑RCNN：39.71 vs. 38.74（+0.97 mAP）
- MVD‑+nuImages‑→Waymo‑，Faster‑RCNN：32.74 vs. 31.14（+1.61 mAP）
- 域适应对比：LGPL超越S‑DANN 1.6 mAP，超越S‑CycConf 1.24 mAP
- SAM‑transfer上限约38 mAP，LGPL达42.6 mAP
- Transfer‑mAP与下游mAP的Spearman相关系数：0.6（p>0.1）

### 补充图表

![[assets/figures/papers/paper_list_l28_https_openreview_net_pdf_id_ChHx5ORqF0/figures/013_Table_8.jpg]]
*Table 8: Statistics of gold transferred labels*

![[assets/figures/papers/paper_list_l28_https_openreview_net_pdf_id_ChHx5ORqF0/figures/005_Table_2.jpg]]
*Table 2: Multi-source label transfer. When multiple source datasets are presented, LGPL outperforms all baselines on all architectures as well*

![[assets/figures/papers/paper_list_l28_https_openreview_net_pdf_id_ChHx5ORqF0/figures/007_Table.jpg]]

![[assets/figures/papers/paper_list_l28_https_openreview_net_pdf_id_ChHx5ORqF0/figures/009_Table_4.jpg]]
*Table 4: Transfer-mAP and downstream-mAP. We find that these two metrics do no strongly correlate with Spearman correlation coefficient R _ { S } ~ = ~ 0 . 6 (p-value > 0 . 1 ) . The ultimate goal of a label transfer model is to enhance the performance of object detectors; thus, we recommend that future work prioritizes downstream performance*

![[assets/figures/papers/paper_list_l28_https_openreview_net_pdf_id_ChHx5ORqF0/figures/011_Table_6.jpg]]
*Table 6: Datasets statistics*

![[assets/figures/papers/paper_list_l28_https_openreview_net_pdf_id_ChHx5ORqF0/figures/012_Table_7.jpg]]
*Table 7: Annotation mismatches of each pair of object detection datasets. Almost every pair of datasets has annotation biases,and among all types of annotation biases and CS is the most common one. Notice that we do not aim to exhaustively find out all the annotation mismatches. Instead, we describe the most obvious ones in this table. CS: Class semantics; AI: Annotation instructions; HMM: Human-machine misalignment; CM: Cross-modality labels*

![[assets/figures/papers/paper_list_l28_https_openreview_net_pdf_id_ChHx5ORqF0/figures/014_Table.jpg]]

![[assets/figures/papers/paper_list_l28_https_openreview_net_pdf_id_ChHx5ORqF0/figures/015_Table_11.jpg]]
*Table 11: Downstream-AP75 of detectors trained with tranferred labels. We highlight the differences over ‘No transfer’ in smaller font and color the performance deterioration in red*

![[assets/figures/papers/paper_list_l28_https_openreview_net_pdf_id_ChHx5ORqF0/figures/016_Table.jpg]]
*Table: l2: The range of the hyper-parameters sweep for different downstream detectors*

![[assets/figures/papers/paper_list_l28_https_openreview_net_pdf_id_ChHx5ORqF0/figures/001_Figure_1.jpg]]
*Figure 1: Left: Varying annotation protocols across datasets can result in annotation mismatches, leading to inconsistent labels. For example, MVD Neuhold et al. (2O17), nuImages Caesar et al. (2020),and Waymo Sun et al. (2020) disagree with what a cyclist represents. Yellow dashed bounding boxes are not annotated. Right: Label transfer is a data-centric approach that transfers the labels from one dataset to match another dataset's annotation protocol, which can be considered as a pre-processing step in the existing training workflow*



## 定位与知识库关联

### 问题定位与核心思路

目标检测数据集的标注协议差异——包括类语义偏差、标注指令分歧、人机偏差和跨模态标签——构成标注失配（annotation mismatch），直接混合训练会损害下游检测器的性能。LGPL将这一问题形式化为**标签迁移**：学习一个映射函数 $f_{\mathrm{trans}} : \mathcal{X} \times \mathcal{Y} \to \mathcal{Y}$，将源数据集的标签转换为符合目标数据集标注协议的样式，理想情况下满足 $\forall x \in \mathcal{D}_{\mathrm{src}}, f_{\mathrm{trans}}(x, g_{\mathrm{src}}(x)) = g_{\mathrm{tgt}}(x)$。

### 基线方法谱系与对比分析

LGPL所处的基线谱系可分为四类，每一类在解决标注失配时暴露出不同的能力边界：

**1. 无迁移（No transfer）与统计归一化（Statistical Normalization）**

No transfer直接使用原始源标签，不做任何处理。统计归一化（Wang et al., 2020）仅对源边界框进行缩放，使其高/宽统计量与目标数据集匹配，完全忽略图像内容。实验表明，统计归一化在多个场景下表现不如No transfer（Table 1中以红色标注），说明仅靠统计对齐无法捕捉标注协议中的语义差异。

**2. 伪标签方法（PL与PL & NF）**

伪标签方法（PL, Lee, 2013）用仅在目标数据集上训练的检测器为源图像生成伪标签；PL & NF在此基础上利用原始源标签过滤低IoU的RPN提案以减少噪声（受Mao et al., 2020启发）。但Table 1、Table 2和Table 3一致显示，这些方法经常不如No transfer，说明单纯利用目标模型的信息不足以弥合标注协议差异——目标模型本身就缺乏对源标注偏差的认知。

**3. 基础模型迁移（SAM-transfer）**

SAM-transfer模型（Kirillov et al., 2023）以源边界框为提示，利用SAM生成分割掩码，将掩码外接框作为转移后的边界框，保持类别不变。该方法能产生准确的类不可知分割，但其下游mAP在nuScenes→nuImages场景中达到约38即停滞，远低于LGPL的42.6（Table 5）。这表明仅修正定位误差不足以完全解决标注失配——类别语义和标注指令层面的偏差需要被显式建模。

**4. 监督域适应方法（S-DANN与S-CycConf）**

S-DANN和S-CycConf（Prabhu et al., 2023）通过对齐源和目标实例特征来适应图像域差异，属于图像域适应而非标签域适应。Figure 4显示，LGPL在平均下游mAP上分别超过S-DANN 1.6和S-CycConf 1.24，说明直接处理标签层面的协议差异比处理图像层面的域差异更有效。

### LGPL的方法创新与关键设计

LGPL在两阶段检测器架构上进行重新设计，形成三个核心模块：

- **图像编码器 $f_{\mathrm{img}}$**：提取共享图像特征，供框生成器与标签迁移模型使用。
- **框生成器 $f_{\mathrm{gen}}$**：基于源数据集训练的标准RPN，为任意图像生成源风格的候选区域。训练时通过停止梯度操作（stop gradient）防止目标数据影响框生成器，确保其始终产生源风格的提案。
- **标签迁移模型 $f_{\mathrm{trans}}$**：改进的RoI头，接收源标签（框+类）与图像特征，同时输出符合目标协议的有效性分数和精修后的边界框。

训练过程的关键创新在于**无配对监督的数据驱动学习**：框生成器在源数据集上训练，标签迁移模型在目标数据集上训练——输入为停止梯度的源风格框和随机类别标签，目标为真实目标标签。这避免了对“源图像-源标签-目标标签”三元组的配对标注需求。推理时，通过类别级阈值 $\sigma_c$ 过滤有效性分数，构建标签迁移后的源数据集。

### 适用边界与局限性

**1. 类标签空间假设**

LGPL假设源数据集的标注类别集合与目标数据集相同，且源数据集对目标要求的所有物体要么检测要么过度检测（即不会遗漏目标物体）。对于类标签空间不匹配的情况，当前方法未直接处理，这限制了其在开放类别场景中的适用性。

**2. 模糊案例的处理能力**

在歧义较大的案例中（例如行人推自行车时是否标注为骑行者），数据驱动的LGPL可能产生错误决定。定性结果（Figure 8最后一行）显示，某些基于规则的基线反而能正确移除标签，而LGPL因缺乏明确的规则知识而遇到困难。

**3. 阈值选择策略**

类别级阈值 $\sigma_c$ 的选择采用简单的分箱策略（Sturges, 1926），并非最优。将其视为额外超参数会导致搜索代价过高，最优阈值选取方法留待未来研究。

**4. 任务范围**

实验仅覆盖了2D目标检测任务，未扩展到3D检测或实例分割等其他任务。标签迁移模型在这些任务上的适用性和迁移效果尚待验证。

### 开放问题

1. **联合处理类标签不匹配与边界框失配**：如何扩展LGPL以同时处理类标签空间不匹配和边界框标注协议差异，实现更全面的标签迁移？

2. **循环混淆损失的深层机制**：在域适应实验中，循环混淆损失（cycle confusion loss）比循环一致性损失（cycle consistency loss）效果稍好，其深层原因尚不明确。

3. **自动阈值选择**：能否设计出自动且高效的类别级阈值选择方法，替代当前的经验分箱策略，从而进一步提升性能并降低超参数调优成本？

4. **跨任务泛化**：标签迁移模型在实例分割、3D目标检测等任务上的适用性和迁移效果如何？

5. **更好的代理评估指标**：Transfer-mAP与下游mAP之间的Spearman相关系数仅为0.6（p>0.1），相关性不显著（Table 4）。是否存在更好的代理指标来直接评估标签迁移质量，避免每次评估都需要训练完整下游检测器？



## 原文 PDF

![[paperPDFs/ICLR_2024/Transferring_Labels_to_Solve_Annotation_Mismatches_Across_Object_Detection_Datasets.pdf]]
