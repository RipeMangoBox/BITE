---
title: An Image like Diffusion Method for Human Object Interaction Detection
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/An_Image_like_Diffusion_Method_for_Human_Object_Interaction_Detection.pdf
project_link: null
code_link: null
aliases:
- HI
- ILDMHOID
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将HOI检测输出重构为H×W×2的“HOI图像”，并设计定制化的图像扩散过程（多项分布噪声、向先验初始化扩散）和切片补丁化架构，利用扩散模型逐步去噪的能力生成高质量HOI图像，从而分解不确定性、提升预测精度。
primary_logic: 利用图像扩散模型逐步去噪的机制，将HOI检测的复杂不确定性转化为一个生成过程：从带先验的噪声HOI图像开始，通过特制扩散模型逐步细化，最终得到准确的交互预测。
claims:
- 在HICO-DET和V-COCO两个基准上均取得最优性能，验证了方法整体有效性。
- 相较于直接套用典型图像扩散模型（Variant I），所提定制化扩散过程使HICO-DET Full mAP从42.50显著提升至47.71，提升+5.21。
- 切片补丁化架构比传统局部补丁架构更适应HOI图像特性，在HICO-DET上带来至少1.9 mAP的提升。
- HICO-DET (Full, Default) 上 mAP = 47.71
---

# An Image like Diffusion Method for Human Object Interaction Detection

> [!tip] 核心洞察
> 利用图像扩散模型逐步去噪的机制，将HOI检测的复杂不确定性转化为一个生成过程：从带先验的噪声HOI图像开始，通过特制扩散模型逐步细化，最终得到准确的交互预测。

| 字段 | 内容 |
|------|------|
| 中文题名 | 一种图像式扩散方法用于人物交互检测 |
| 英文题名 | An Image like Diffusion Method for Human Object Interaction Detection |
| 会议/期刊 | CVPR 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HOI-IDiff |
| Dataset | HICO-DET, V-COCO |

> [!tip] 效果简介
> - HICO-DET (Full, Default) 上，mAP 47.71 vs 42.50 (Variant I: typical image diffusion model) (+5.21)。
> - V-COCO (Scenario 1) 上，AProle 73.4 vs existing SOTA (Wu et al., CVPR 2024) (outperforms)。

## 概要

人物交互（Human-Object Interaction, HOI）检测旨在同时定位图像中的人物与物体，并识别其交互类别。该任务面临高度模糊与不确定性：同一交互在不同人-物对中外观差异显著，而不同交互却可能视觉相似；遮挡与杂乱背景进一步加剧噪声，使传统方法易于出错。

针对上述瓶颈，本文提出 **HOI-IDiff**，将 HOI 检测重构为一种**图像式生成问题**。核心思路是将每对人-物对的检测输出表示为一张形状为 $H \times W \times 2$ 的“HOI 图像”（$H$ 为物体类别数，$W$ 为交互类别数），并设计定制化的图像扩散过程——采用多项分布噪声替代高斯噪声、使前向扩散收敛至带有物体类别先验的初始噪声图像——以及切片补丁化（slice patchification）架构，利用扩散模型逐步去噪的能力生成高质量 HOI 图像，从而分解不确定性、提升预测精度。

**方法谱系与知识库定位**：HOI-IDiff 属于二阶段 HOI 检测方法，第一阶段沿用预训练检测器（DETR）提取人-物边界框，第二阶段以扩散模型为核心生成交互预测。相较于传统二阶段方法（如 **Graph Parsing Networks**（Qi et al., ECCV 2018）、**Visual Compositional Learning**（Hou et al., ECCV 2020）、**PViC**（Zhang et al., ICCV 2023）及 **Pose-aware Hybrid Learning**（Wu et al., CVPR 2024）），本工作首次将图像扩散模型引入 HOI 检测，并在扩散过程与架构上做出针对性适配，而非直接套用自然图像扩散范式。

**主要结果**：在 HICO-DET 和 V-COCO 两个基准上均取得最优性能。消融实验表明，定制化扩散过程相较直接使用典型图像扩散模型带来 **+5.21 mAP** 的显著增益（HICO-DET Full）；切片补丁化架构相较于传统局部补丁架构至少提升 **1.90 mAP**，验证了各关键设计的有效性。

### 人物交互检测的核心瓶颈

人物交互（Human-Object Interaction, HOI）检测旨在从图像中同时定位人与物体，并识别其交互关系（如“人-看-手机”），是视觉理解的关键任务。然而，该任务面临高度的**模糊性与不确定性**：同一类交互在不同人-物对中外观差异极大，而不同类交互却可能呈现相似的视觉模式；遮挡、杂乱背景以及人与物体的姿态变化进一步加剧了预测噪声，使得传统方法的输出容易出错。

### 现有方法的局限

主流HOI检测方法通常采用两阶段范式：先用预训练检测器获取人与物体的边界框，再对每对人-物组合进行物体分类和交互预测。代表性工作包括**Graph Parsing Networks**（Qi et al., ECCV 2018）、**Pairwise Body-Part Attention**（Fang et al., ECCV 2018）、**Visual Compositional Learning**（Hou et al., ECCV 2020）、**PViC**（Zhang et al., ICCV 2023）以及**Pose-aware Hybrid Learning**（Wu et al., CVPR 2024）等。这些方法虽然不断推进性能边界，但本质上仍是在单步前向推理中对高度不确定的预测空间做出硬性决策，缺乏对输出结果进行**逐步细化与纠错**的机制。

### 本文动机：将HOI检测重构为生成问题

受图像扩散模型在逐步去噪生成高质量图像方面成功的启发，本文提出一个核心洞察：**利用扩散模型逐步去噪的能力，将HOI检测中的复杂不确定性转化为一个可控的生成过程**。具体而言，将每对人-物组合的检测输出（物体分类概率向量与交互预测矩阵）重构为一幅形状为 $H \times W \times 2$ 的“HOI图像”，进而通过特制的扩散模型从带先验的噪声HOI图像开始，逐步细化，最终生成准确的交互预测。这一范式转变使得模型能够以渐进式的方式分解不确定性，而非在单步中做出可能出错的硬性判断。

## 核心方法与创新机理

HOI-IDiff 的核心创新在于将HOI检测重新构建为一种**定制化的图像扩散生成问题**，并为此设计了三个紧密耦合的关键机制，以解决传统方法在处理交互不确定性时的瓶颈。

### 1. 问题重构：从分类到HOI图像生成

传统方法将HOI检测视为对交互类别的直接分类或匹配。HOI-IDiff 则提出，对于每个人-物对，其检测输出可以被重构为一个尺寸为 $H \times W \times 2$ 的“HOI图像” $I^{hoi}$（**Figure 1**）。该图像由物体分类向量 $v^{obj}$ 和交互预测矩阵 $m^{int}$ 相乘而得，其中 $H$ 代表物体类别数，$W$ 代表交互类别数，两个通道分别编码交互是否发生及其置信度。这一重构将复杂的结构化预测问题转化为一个标准的图像生成任务，为利用扩散模型的强大生成能力铺平了道路。

### 2. 定制化HOI图像扩散过程

直接套用为标准自然图像设计的高斯扩散过程，无法适配HOI图像的概率分布特性。HOI-IDiff 对此进行了根本性的改造，体现在两个关键的 **changed slots** 上：

*   **噪声分布：从高斯噪声到多项分布噪声**
    标准扩散模型注入高斯噪声 $\epsilon$（**Eq. 1**）。HOI-IDiff 则采用多项分布噪声 $\epsilon^{Mu}$（**Eq. 4**），因为HOI图像的每个像素值本质上代表概率，其扩散过程必须保证每一步结果仍是一个合法的概率分布（即所有像素值之和为1）。这一改变是模型能够处理概率型输出的数学基础。

*   **扩散方向：从纯噪声到物体类别先验**
    标准模型的目标是向纯随机高斯噪声扩散。HOI-IDiff 的前向扩散过程则被设计为向一个带有**物体类别先验**的初始噪声图像 $d_{init}$ 收敛（**Eq. 5**）。具体而言，$d_{init}$ 中的 $v^{obj}$ 部分被设定为预训练检测器提供的物体分类概率向量，而 $m^{int}$ 部分则被初始化为0.5，表示交互的完全不确定性。这种“向先验扩散”的机制，使得反向去噪过程的起点不再是毫无意义的随机噪声，而是包含了物体类别强先验的、有意义的初始状态，极大地降低了生成任务的难度。

### 3. 切片补丁化架构

标准扩散模型的骨干网络（如U-Net或DiT）通常采用局部补丁（patch）处理图像，这忽略了HOI图像特有的结构：其行和列分别对应物体和交互类别，具有全局相关性。HOI-IDiff 提出了**切片补丁化架构**，将 $H \times W \times 2$ 的HOI图像切分为 $H$ 个水平切片和 $W$ 个垂直切片，再将这些切片转换为token，送入Transformer编码器进行多头自注意力处理。该架构能同时捕获同一物体类别下所有交互的相关性（水平切片）和同一交互类别下所有物体的相关性（垂直切片），从而更有效地对HOI图像中的结构化依赖关系进行建模。

HOI-IDiff 将人物交互检测重构为一个“HOI图像”生成问题，整体流程包含两个阶段：**预训练检测器提取人-物对**与**扩散模型生成HOI图像**。

### 输入与预处理

给定输入图像，框架首先使用一个预训练的目标检测器（具体为DDETR）检测其中的人和物体实例，得到人-物对的边界框。对于每一对人-物组合，检测器同时输出物体的类别先验概率向量，该向量将作为后续扩散过程的先验信息。

### HOI图像构建

每对人-物组合的HOI检测输出被形式化为一个尺寸为 $H \times W \times 2$ 的“HOI图像” $I^{hoi}$，其中 $H$ 表示物体类别总数，$W$ 表示交互类别总数，2个通道分别对应物体分类概率与交互预测概率。该HOI图像由两个分量相乘得到：物体分类向量 $v^{obj} \in \mathbb{R}^{H}$ 和交互预测矩阵 $m^{int} \in \mathbb{R}^{W \times 2}$。这一设计将HOI检测的两个关联子任务——物体识别与交互分类——统一为单一的结构化输出表示（见 Figure 1）。

### 扩散生成流程

框架的核心是一个专门为HOI图像设计的扩散模型，其优化过程分为两个阶段：

1. **前向扩散过程**：从真实的HOI图像 $I_0^{hoi}$ 出发，通过逐步注入多项分布噪声，将其扩散至一个带有物体类别先验的初始噪声HOI图像。这一过程的关键设计在于：噪声分布采用多项分布而非传统的高斯噪声，且扩散目标不是纯随机噪声，而是融入了检测器先验的初始化噪声图像（见 Figure 2 红色箭头方向）。

![[assets/figures/papers/paper_list_l1729_An_Image_like_Diffusion_Method_for_Human_Object_Interaction_Detection/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of our HOI image diffusion process. As indicated by the red arrows from right to left, the forward HOI image diffusion process gradually diffuses the ground-truth HOI image*

2. **反向去噪过程**：以初始噪声HOI图像为起点，扩散模型 $\theta$ 在外观特征 $f_a$ 的引导下，逐步去噪重建出高质量的HOI图像（见 Figure 2 绿色箭头方向）。反向过程的每一步可表示为 $\hat{d}_{k-1} = g(\hat{d}_{k}, \theta, f_{a}, f_{s}^{k})$，其中 $f_s^k$ 为步感知空间特征。

### 模型架构与解码

为适应HOI图像的结构特性，扩散模型采用**切片补丁化架构**：将 $H \times W \times 2$ 的HOI图像沿行和列方向分别切分为 $H$ 个水平切片和 $W$ 个垂直切片，转换为token后经多头自注意力Transformer编码器处理，从而同时捕获行方向（物体类别间关系）和列方向（交互类别间关系）的相关性。

最终，通过比较生成HOI图像中每个垂直切片的两通道概率值，确定每个交互类别的预测结果，完成从生成图像到检测输出的解码。

### 4.1 HOI图像生成范式

HOI-IDiff 将每对人-物组合的 HOI 检测输出重构为一张尺寸为 $H \times W \times 2$ 的“HOI图像” $I^{hoi}$，其中 $H$ 为物体类别数，$W$ 为交互类别数，两个通道分别对应交互发生与否的概率分布。该图像由物体分类向量 $v^{obj} \in \mathbb{R}^{H}$ 与交互预测矩阵 $m^{int} \in \mathbb{R}^{W \times 2}$ 相乘得到（见 Figure 1）。这一重构将原本离散的分类任务转化为图像生成问题，使扩散模型的逐步去噪能力得以介入。

![[assets/figures/papers/paper_list_l1729_An_Image_like_Diffusion_Method_for_Human_Object_Interaction_Detection/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of the HOI image (of shape*

### 4.2 定制化HOI图像扩散过程

标准图像扩散模型的前向过程注入高斯噪声（Eq. 1），但 HOI 图像本质上是概率分布（每通道和为1），高斯噪声会破坏这一约束。HOI-IDiff 对扩散过程进行了两项关键定制：

**噪声分布替换。** 将高斯噪声 $\epsilon$ 替换为从多项分布采样的噪声 $\epsilon^{Mu}$，前向扩散步变为：

$$d_k = (1 - \beta_k) d_{k-1} + \beta_k \epsilon^{Mu} \quad \text{(Eq. 4)}$$

由于 $d_{k-1}$ 和 $\epsilon^{Mu}$ 均为概率分布且 $(1-\beta_k)+\beta_k=1$，可保证每一步的 $d_k$ 依然满足概率分布和为1的约束。

**向先验扩散。** 标准扩散向纯随机噪声收敛；HOI-IDiff 则向带有物体类别先验的初始噪声 HOI 图像 $d_{init}$ 扩散。$d_{init}$ 由预训练检测器（DETR）给出的物体类别概率向量作为 $v^{obj}$，并将 $m^{int}$ 所有值置为 0.5 后相乘得到。累积前向扩散的闭式表达为：

$$d_k = \overline{\alpha}_k d_0 + (1 - \overline{\alpha}_k) \overline{\epsilon}^{Mu} \quad \text{(Eq. 5)}$$

当 $k$ 足够大时 $\overline{\alpha}_k \to 0$，$d_k$ 收敛至 $d_{init}$，实现了向先验噪声图像的定向扩散。

**反向过程。** 训练时，利用马尔可夫链性质推导出后验分布 $q(d_{k-1} | d_k, d_0)$ 作为监督信号（Eq. 6）。推理时，扩散模型 $\theta$ 从 $d_K \approx d_{init}$ 出发，在每步结合外观特征 $f_a$ 和步感知空间特征 $f_s^k$ 逐步去噪：

$$\hat{d}_{k-1} = g(\hat{d}_k, \theta, f_a, f_s^k) \quad \text{(Eq. 7)}$$

### 4.3 切片补丁化架构

HOI 图像的行向量（$H$ 维）表示物体类别关系，列向量（$W \times 2$ 维）表示交互类别关系，两者具有不同的语义结构。为同时捕获行方向与列方向的相关性，HOI-IDiff 设计了切片补丁化（slice patchification）策略：将 $H \times W \times 2$ 的 HOI 图像分别切分为 $H$ 个水平切片和 $W$ 个垂直切片，转换为 token 后送入多头自注意力 Transformer 编码器处理。消融实验表明，该架构相比标准局部补丁架构（Variant V–VIII）在 HICO-DET Full 上至少带来 1.90 mAP 的提升（Table 2），验证了切片式建模对 HOI 图像结构适配的有效性。

### 4.4 交互解码

反向扩散完成后，对生成的 HOI 图像每个垂直切片（对应一种交互类别）比较两通道的概率值，取概率更高的通道索引确定该交互是否发生，从而得到最终的交互预测结果。

## 实验与关键发现

### 整体性能

HOI-IDiff 在 HICO-DET 和 V-COCO 两个基准数据集上均取得了最优性能（Table 1）。在 HICO-DET Full 设定下，该方法达到 **47.71 mAP**，相较于现有二阶段方法 **Pose-aware Hybrid Learning**（Wu et al., CVPR 2024）等基线展现出明显优势。在 V-COCO Scenario 1 设定下，HOI-IDiff 取得了 **73.4 AProle**，同样超越了此前的最优方法。值得注意的是，所有对比均采用相同的预训练检测器 DDETR，确保了公平性。

![[assets/figures/papers/paper_list_l1729_An_Image_like_Diffusion_Method_for_Human_Object_Interaction_Detection/figures/003_Table_1.jpg]]
*Table 1: Performance comparison on the HICO-DET and V-COCO datasets*

### 关键组件消融

Table 2 系统评估了 HOI-IDiff 各核心组件的贡献，揭示了以下关键发现：

![[assets/figures/papers/paper_list_l1729_An_Image_like_Diffusion_Method_for_Human_Object_Interaction_Detection/figures/005_Table_2.jpg]]
*Table 2: Evaluation on the key components of HOI-IDiff*

**定制扩散过程的核心作用。** 将所提的定制化 HOI 图像扩散过程（多项分布噪声 + 向先验初始化扩散）替换为典型图像扩散模型（Variant I，采用高斯噪声向纯随机噪声扩散），HICO-DET Full mAP 从 **47.71 骤降至 42.50**，降幅达 **-5.21**。这一显著差距直接验证了核心洞察：HOI 图像的概率分布特性（每切片求和为 1）与自然图像的像素分布存在本质差异，直接套用标准扩散范式会导致严重的分布失配。

**切片补丁化架构的增益。** 将切片补丁化（slice patchification）替换为基于局部补丁的标准架构（Variants V–VIII），性能至少下降 **1.90 mAP**。切片补丁化通过同时捕获行方向（物体类别间关系）和列方向（交互类别间关系）的全局依赖，更契合 HOI 图像的结构化特性。

**HOI 图像联合生成的必要性。** Table 3 进一步消融了 HOI 图像的构建方式。联合生成 H×W×2 的完整 HOI 图像（Ours）优于分离生成物体分类向量 v^obj 和交互矩阵 m^int 的变体（Variants I, II）。有趣的是，即使仅生成 W×2 的交互部分（不显式建模物体分类），方法仍能达到 SOTA 性能，说明扩散模型在反向过程中已隐式地融合了物体类别信息。此外，完整 HOI 图像的性能与额外优化边界框的 Variant IV 相近，表明当前设计在简洁性与性能之间取得了良好平衡。

### 定性分析

Figure 3 可视化了反向扩散过程中 HOI 图像的逐步去噪轨迹。从初始的噪声图像（受物体类别先验引导）出发，随着扩散步数增加，交互预测矩阵逐渐从模糊均匀分布收敛至清晰的稀疏模式，直观展示了扩散模型逐步分解不确定性的过程。

![[assets/figures/papers/paper_list_l1729_An_Image_like_Diffusion_Method_for_Human_Object_Interaction_Detection/figures/006_Figure_3.jpg]]
*Figure 3: Visualization of the HOI image diffusion process*

### 待验证与局限性

当前分析基于论文提供的实验数据，以下方面需要读者结合原文进一步确认：

- **计算效率。** 扩散模型的迭代去噪特性可能带来推理延迟，但原文未提供与单步前馈方法的推理时间对比。在实时 HOI 检测场景下的部署可行性需要手动验证。
- **超参数敏感性。** 扩散步数 K、多项分布试验次数 T 等关键超参数的最优选择原则尚未在实验部分展开讨论，其在不同数据集规模下的鲁棒性有待进一步分析。
- **失败模式。** 原文未明确报告方法的典型失败案例（如严重遮挡、罕见交互类别等场景下的表现），该部分结论需要结合补充材料或代码复现进行手动验证。

![[assets/figures/papers/paper_list_l1729_An_Image_like_Diffusion_Method_for_Human_Object_Interaction_Detection/figures/004_Table_3.jpg]]
*Table 3: Evaluation on the HOI image formulation process. Note that, even when we only generate*

## 定位与知识库关联

### 与现有方法的继承与差异

HOI-IDiff 属于二阶段HOI检测范式，继承了先检测人/物边界框、再预测交互的流水线。其前置检测器采用与主流二阶段方法（如 **PViC** (Zhang et al., ICCV 2023)、**Pose-aware Hybrid Learning** (Wu et al., CVPR 2024)）相同的DDETR，确保对比公平性。

然而，HOI-IDiff 在交互预测阶段走出了与现有方法截然不同的技术路径。传统二阶段方法——从早期的 **Graph Parsing Networks** (Qi et al., ECCV 2018)、**Pairwise Body-Part Attention** (Fang et al., ECCV 2018)，到近期的 **Visual Compositional Learning** (Hou et al., ECCV 2020) 和 **PViC** (Zhang et al., ICCV 2023)——均将交互预测建模为判别式分类问题，直接输出类别概率。HOI-IDiff 则首次将HOI检测重构为生成式问题：将每对人-物的检测输出表示为 $H \times W \times 2$ 的“HOI图像”，并设计定制化扩散模型逐步生成该图像。

这一生成式范式带来了关键的方法论差异：

1. **不确定性分解**：传统判别式方法需一次性处理高度模糊的交互预测（同一交互外观迥异、不同交互视觉相似、遮挡与杂乱背景干扰），容易出错。HOI-IDiff 利用扩散模型逐步去噪的机制，将复杂不确定性分解为多步细化过程。

2. **扩散过程定制化**：不同于典型图像扩散模型使用高斯噪声和向纯随机噪声扩散，HOI-IDiff 针对HOI图像的概率分布特性，设计了三个关键定制：
   - **多项分布噪声**：以多项分布噪声 $\epsilon^{Mu}$ 替代高斯噪声 $\epsilon$，确保扩散过程中每个像素值始终为合法的概率分布（和恒为1）。
   - **向先验初始化扩散**：前向过程不向纯随机噪声收敛，而是向带有物体类别先验的初始噪声HOI图像 $d_{init}$ 扩散，将检测器的先验知识注入扩散过程。
   - **切片补丁化架构**：摒弃U-Net/DiT等基于局部方形补丁的处理方式，将HOI图像切分为 $H$ 个水平切片和 $W$ 个垂直切片，通过Transformer同时捕获行方向（物体类别间关系）和列方向（交互类别间关系）的全局依赖。

### 适用边界与假设

HOI-IDiff 的有效性建立在以下假设之上：

- **检测器提供的物体类别先验可靠**：前向扩散和噪声HOI图像初始化均依赖预训练检测器输出的物体类别概率向量。若检测器对物体类别判断错误，该错误将被注入扩散过程，且当前设计未包含对此类错误的显式纠正机制。
- **交互类别空间固定且有限**：HOI图像的高度 $H$ 和宽度 $W$ 分别对应预定义的物体类别数和交互类别数。方法天然假设这些类别集合在训练和推理时保持一致，难以直接扩展到开放词汇或增量学习的场景。
- **二阶段流水线的固有约束**：方法继承二阶段范式的假设——人/物边界框可由独立检测器可靠获取。在密集遮挡或小目标场景下，检测器漏检将直接导致交互预测失败，HOI-IDiff 本身未对边界框质量进行优化（尽管Table 3的变体IV表明，额外优化边界框仅带来微弱增益，说明当前设计已在简洁性与性能间取得良好平衡）。

### 局限与开放问题

**已明确的局限**：

- 论文未报告HOI-IDiff 在实时场景下的推理速度。扩散模型的多步反向采样（步数 $K$）天然带来计算开销，其与单步判别式方法的效率差距需要实际测量数据支撑。
- 方法在HICO-DET和V-COCO两个标准基准上验证，但未探讨在更大规模数据集（如HOI-A）或域迁移场景下的泛化表现。

**待探索的开放问题**：

1. **扩散步数 $K$ 与多项分布试验次数 $T$ 的最优选择**：论文使用了固定的 $K$ 和 $T$ 值，但未系统分析这些超参数对性能-效率权衡的影响。更少的扩散步数可能加速推理但牺牲质量，更小的 $T$ 可能降低多项分布的近似精度。

2. **HOI图像与自然图像的差异处理**：定制的多项噪声和切片补丁化架构是针对HOI图像特性的专门设计，但论文未深入分析这些设计为何优于典型图像扩散模型的深层原因（例如，多项噪声是否更好地保留了概率分布的离散结构？切片补丁化是否比局部补丁更有效地捕获了行/列方向的长程依赖？）。

3. **生成式范式的独特优势挖掘**：当前方法主要利用扩散模型的去噪能力提升预测精度，但生成式框架天然支持多模态输出和不确定性量化——例如，通过多次采样生成多个合理的交互预测，或利用采样方差估计预测置信度。这些潜力尚未被探索。

4. **与其他生成式HOI方法的对比缺失**：论文仅与判别式基线对比，未讨论是否存在其他将HOI检测建模为生成问题的工作（如基于自回归或VAE的方法），若存在，HOI-IDiff 的相对优势需要明确。

## 原文 PDF

![[paperPDFs/CVPR_2025/An_Image_like_Diffusion_Method_for_Human_Object_Interaction_Detection.pdf]]
