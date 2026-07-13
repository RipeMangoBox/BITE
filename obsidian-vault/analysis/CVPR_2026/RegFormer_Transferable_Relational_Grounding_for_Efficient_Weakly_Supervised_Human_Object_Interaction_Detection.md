---
title: "RegFormer: Transferable Relational Grounding for Efficient Weakly-Supervised Human-Object Interaction Detection"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RegFormer_Transferable_Relational_Grounding_for_Efficient_Weakly_Supervised_Human_Object_Interaction_Detection.pdf
project_link: null
code_link: "https://github.com/mlvlab/RegFormer"
aliases:
- RRGT
- RegFormer
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过空间接地查询和交互性得分，模型能够聚焦于图像中真正发生交互的人-物区域，过滤非交互区域。
primary_logic: 将图像级交互推理过程分解为先生成人-物对查询，再解码交互，并通过空间接地查询和交互性感知学习注入局部空间线索，从而实现从图像级分类到实例级检测的直接迁移，无需额外训练。
claims:
- 消融实验显示，加入空间接地查询（SG）和交互性得分（IA）分别带来+1.8和+3.6 mAP的提升，组合后总提升+5.0 mAP（HICO分类）。
- 在HOI检测中，RegFormer在HICO-DET上取得30.01 Full mAP（默认配置），并且使用更强检测器（H-DETR）可达38.14 mAP，超越现有弱监督方法。
- HICO-DET 上 Full mAP = 33.33 (Faster R-CNN, DINO-B, CLIP-B)
- HICO-DET (Zero-shot, RF-UC) 上 Unseen mAP = 31.53
---

# RegFormer: Transferable Relational Grounding for Efficient Weakly-Supervised Human-Object Interaction Detection

> [!tip] 核心洞察
> 将图像级交互推理过程分解为先生成人-物对查询，再解码交互，并通过空间接地查询和交互性感知学习注入局部空间线索，从而实现从图像级分类到实例级检测的直接迁移，无需额外训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | RegFormer：面向高效弱监督人-物交互检测的可迁移关系定位 |
| 英文题名 | RegFormer: Transferable Relational Grounding for Efficient Weakly-Supervised Human-Object Interaction Detection |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.00507) · [Code](https://github.com/mlvlab/RegFormer) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RegFormer (Relational Grounding Transformer) |
| Dataset | HICO-DET |

> [!tip] 效果简介
> - HICO-DET 上，Full mAP 33.33 (Faster R-CNN, DINO-B, CLIP-B) vs 31.14 (Weakly HOI-CLIP, Faster R-CNN) (+2.19)。
> - HICO-DET (Zero-shot, RF-UC) 上，Unseen mAP 31.53 vs 21.46 (OpenCat) (+10.07)。

## 概要

**问题瓶颈**：现有弱监督人-物交互（HOI）检测方法通常需枚举图像中所有可能的人-物候选对，再逐一判断其交互类别。这一范式导致计算成本随实例数量急剧增长，且大量非交互的虚假组合产生严重假阳性，制约了从图像级标注向实例级检测的迁移效率。

**核心思路**：RegFormer 将交互推理分解为“先生成人-物对查询（HO），再解码交互类别（I）”的顺序过程，并通过**空间接地查询**与**交互性感知学习**将局部空间线索注入查询表示中。这使得模型能够聚焦于真正发生交互的区域，抑制非交互噪声，从而在仅使用图像级标签训练的条件下，直接迁移到实例级 HOI 检测，无需额外微调。

**方法定位**：RegFormer 建立在 **ML-Decoder**（Ridnik et al., WACV 2023）多标签分类架构之上，将原始的“HOI 类别查询→交互分类”路径重构为 HO→I 顺序推理框架。与 **Weakly HOI-CLIP**（Wan et al., ICLR 2023）等弱监督基线相比，RegFormer 的关键区别在于引入了空间接地的人-物对查询和显式的交互性得分门控机制，而非仅依赖文本嵌入初始化的全局查询。

**主要结果**：
- 在 HICO-DET 上，RegFormer 以 Faster R-CNN 检测器达到 33.33 Full mAP，较 Weakly HOI-CLIP 提升 +2.19 mAP；若换用更强的 H-DETR 检测器，可进一步提升至 38.14 mAP，超越现有弱监督方法。
- 消融实验表明，空间接地查询（SG）和交互性得分（IA）分别贡献 +1.8 和 +3.6 mAP 的分类性能提升，组合后总提升达 +5.0 mAP；在实例级检测中，这两项组件使 Full mAP 从 17.49 跃升至 30.01。
- 推理效率方面，RegFormer 在 200 个实例对时仍保持 46.3 FPS，而 ML-Decoder 基线随实例对增加显著变慢。

**局限性**：RegFormer 仍依赖外部目标检测器提供实例提议，检测性能受限于检测器质量；在零样本设定下，未见组合的性能显著低于已见组合，对新颖交互的泛化仍具挑战。

### 弱监督HOI检测的核心困境

人-物交互（Human-Object Interaction, HOI）检测旨在同时定位图像中的人、物体及其交互关系，形成⟨人，动词，物体⟩三元组。全监督方法依赖昂贵且耗时的实例级标注，严重制约了其可扩展性。弱监督HOI检测仅需图像级标签即可训练，因而成为更具吸引力的替代方案。

现有的弱监督HOI检测方法大多遵循“先枚举、后分类”的范式：利用预训练的目标检测器生成大量人-物候选对，再对每对候选进行交互分类。这一范式存在两个根本性瓶颈：

1. **计算效率低下**：随着图像中人-物实例数量的增加，候选对数量呈二次增长。例如，基于ML-Decoder（Ridnik et al., WACV 2023）的方法需要对所有候选对逐一进行交互推理，导致推理时间随实例对数量急剧膨胀（见Figure 1(A)）。
2. **假阳性泛滥**：大量枚举的候选对实际上并不发生交互（如人手持手机 vs. 人脚边的手机），但现有方法缺乏有效机制区分交互与非交互对，导致大量假阳性预测（见Figure 1(B)）。

### 现有方法的缺口

弱监督HOI检测的核心挑战在于：如何仅凭图像级标签，学习到实例级的空间判别能力。现有方法在这方面的尝试存在明显不足：

- **缺乏局部空间线索的注入**：多数方法将交互推理建模为纯语义分类问题，忽视了交互行为天然具有的空间局部性——发生交互的人和物体在空间上必然紧密关联。图像级标签无法直接提供“谁对谁做了什么”的实例级监督，因此模型必须学会从图像中自动挖掘空间线索。
- **缺少交互性感知机制**：交互行为仅发生在少数人-物对之间，但现有方法对所有候选对一视同仁，没有显式的门控机制来抑制非交互对。

### 本文动机

针对上述困境，RegFormer提出了一条核心思路：**将图像级交互推理过程分解为先生成人-物对查询（HO），再解码交互（I）的顺序框架，并通过空间接地查询和交互性感知学习注入局部空间线索，实现从图像级分类到实例级检测的直接迁移，无需额外训练。**

具体而言，RegFormer的设计动机体现在三个层面：

- **顺序推理（HO→I）**：将交互推理从“一次性对所有HOI组合分类”转变为“先确定人-物对，再判断交互类型”的顺序过程，从根本上降低了推理空间的复杂度。
- **空间接地查询**：通过patch级重要性加权聚合，将人体和物体的空间位置信息显式编码到HO查询中，使模型能够聚焦于真正发生交互的空间区域。
- **交互性感知学习**：引入显式的交互性得分作为门控信号，在训练中监督模型区分交互与非交互对，并在推理时直接抑制非交互区域，从而大幅减少假阳性。

这一设计使得RegFormer在保持计算效率的同时，仅凭图像级标签即可获得与全监督方法可比拟的检测性能，并天然具备零样本迁移能力——模型学到的交互推理能力可直接应用于任意检测器输出的实例对，无需针对特定检测器重新训练。

## 核心方法与创新机理

RegFormer 的核心创新在于将弱监督 HOI 检测从“全类别并行分类”重构为 **HO → I 的顺序推理范式**，并通过两项关键的 changed slots 注入局部空间线索，使模型在仅使用图像级标签训练的情况下可直接迁移至实例级检测。

### 1. 从并行分类到顺序推理：HO → I 框架

传统弱监督 HOI 检测方法（如基于 **ML-Decoder**（Ridnik et al., WACV 2023）的范式）直接对所有 HOI 类别进行并行分类，需要枚举大量人-物实例对，导致计算成本随实例数量急剧增长，且非交互的组合产生大量假阳性（Figure 1）。

RegFormer 将推理过程分解为两步：首先在 **Pairwise Instance Encoder** 中为每个人-物类别对（HO）生成查询，然后在 **Interaction Decoder** 中解码对应的交互类别（I）。这一顺序框架的因果机制在于：通过将交互推理限定在特定的人-物对上下文中，模型无需对所有可能的 HOI 组合进行穷举评分，从而在推理效率上实现显著提升——Figure 1(A) 显示，随着实例对数量增加，RegFormer 的推理时间仅边际增长，而 ML-Decoder 则显著变慢。

### 2. 空间接地查询：注入局部空间线索

**Changed Slot：查询构建方式**

- **Baseline（ML-Decoder）**：使用文本嵌入初始化全部 HOI 类别查询，查询缺乏空间定位信息。
- **RegFormer**：通过空间接地查询（Spatially Grounded Query, SG）聚合 patch 级特征。具体而言，Pairwise Instance Encoder 计算每个 patch 相对于人体类别和物体类别的目标性得分（objectiveness score），通过 softmax 转换为空间重要性权重，再对 patch 特征加权聚合，形成包含空间位置信息的 HO 查询。

人体 patch 重要性得分定义为：

$$\alpha^{\mathrm{h}}(p) = \frac{\exp(s^{\mathrm{h}}(p)/\tau_{p})}{\sum_{p'}\exp(s^{\mathrm{h}}(p')/\tau_{p})}$$

其中 $s^{\mathrm{h}}(p)$ 是 patch $p$ 与人体文本嵌入的余弦相似度。空间接地 HO 查询由人体和物体的加权特征拼接投影得到：

$$q^{\mathrm{ho}}_k = \mathbb{P}_q([\sum_{p}\alpha^{\mathrm{h}}(p)x(p); \sum_{p}\alpha^{\mathrm{o}}_k(p)x(p)])$$

这一设计的因果 knob 在于：查询中显式编码了人体和物体的空间位置信息，使交互解码器能够聚焦于真正发生交互的区域，而非在整个图像中盲目搜索。

### 3. 交互性感知学习：门控机制抑制假阳性

**Changed Slot：交互性得分学习**

- **Baseline**：无显式交互性得分机制。
- **RegFormer**：引入交互性感知学习（Interactiveness-aware Learning, IA），计算 patch 级交互性并聚合为图像级/实例级交互性得分，作为门控信号调制交互分类得分。

交互性得分的核心机理是：在 patch 级别判断每个空间位置是否与交互相关，然后通过加权求和聚合为图像级的交互性得分 $r^{\mathrm{h}}$ 和 $r^{\mathrm{o}}_k$。最终交互分类损失为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{focal}} \big( \hat{s}^{\mathrm{hoi}}, c^{\mathrm{hoi}} \big), \quad \hat{s}_{k}^{\mathrm{hoi}} = \hat{s}_{k}^{\mathrm{a}} (r_{k}^{\mathrm{ho}})^{\gamma}$$

其中 $r_{k}^{\mathrm{ho}}$ 作为缩放因子，$\gamma$ 控制交互性得分的调制强度。这一门控机制直接抑制非交互区域的分类得分，Figure 1(B) 和 Figure 3 显示 RegFormer 有效减少了假阳性。

**消融实验的因果证据**（Table 1）：在 HICO-DET 上，仅使用 HO → I 顺序推理时 Full mAP 为 17.49（等同于 ML-Decoder 基线）；加入空间接地查询（SG）提升至 19.29（+1.8 mAP）；加入交互性得分（IA）提升至 22.89（+3.6 mAP）；组合两者后达到 30.01 mAP，总提升 +5.0 mAP。这表明 SG 和 IA 具有互补作用：SG 提供空间定位能力，IA 提供交互性过滤能力。

### 4. 从图像级到实例级的零成本迁移

RegFormer 的另一关键创新在于无需额外训练即可从图像级分类迁移至实例级检测。给定外部目标检测器（如 Faster R-CNN 或 H-DETR）生成的实例提议，通过区域感知 mask $m(p)$ 将 patch 重要性得分和交互性得分约束在对应实例区域内，直接计算实例级 HOI 得分：

$$\tilde{s}_{ij}^{\mathrm{hoi}} = \tilde{s}_{ij}^{\mathrm{a}} \cdot (r_{ij}^{\tilde{\mathrm{ho}}})^{\gamma} \cdot (\tilde{s}_{i}^{\mathrm{h}} \tilde{s}_{j}^{\mathrm{o}})^{\lambda}$$

其中 $\tilde{s}_{ij}^{\mathrm{a}}$ 为交互分类得分，$r_{ij}^{\tilde{\mathrm{ho}}}$ 为 pairwise 交互性得分（人体和物体交互性的几何平均），$\tilde{s}_{i}^{\mathrm{h}}$ 和 $\tilde{s}_{j}^{\mathrm{o}}$ 为检测置信度。这一公式将交互推理、交互性过滤和检测置信度统一为单一评分，实现了从弱监督训练到实例级检测的直接迁移。

RegFormer 的核心设计思想是将图像级交互推理过程分解为**顺序生成人-物对查询**与**交互解码**两个阶段，并通过**空间接地查询**和**交互性感知学习**注入局部空间线索，从而在仅使用图像级标签训练的条件下，实现从图像级分类到实例级检测的直接迁移，无需额外训练。

### 整体流程

RegFormer 的整体框架如图 2 所示，包含训练和推理两个分支，二者共享相同的模型结构：

1. **训练阶段**：输入图像经过视觉编码器提取空间特征图 $x$，同时利用预训练文本编码器获取人体类别 $e^{\mathrm{h}}$、物体类别 $\{e_k^{\mathrm{o}}\}$ 和交互类别 $\{e_t^{\mathrm{a}}\}$ 的文本嵌入。Pairwise Instance Encoder 通过计算 patch 级的目标性得分（objectiveness score），为每个人-物对聚合空间特征，生成**空间接地的 HO 查询** $q_k^{\mathrm{ho}}$。这些查询随后进入 Interaction Decoder，通过交叉注意力与图像特征交互，输出交互分类得分 $\hat{s}^{\mathrm{a}}$。同时，模型计算 patch 级的交互性得分并聚合为图像级交互性得分 $r$，作为门控信号调制交互分类得分，并接受显式监督。

2. **推理阶段**：给定外部目标检测器检测到的人体和物体实例，模型通过区域感知掩码 $m(p)$ 将 patch 重要性得分和交互性得分约束在对应实例区域内，直接生成实例级 HOI 预测得分 $\tilde{s}_{ij}^{\mathrm{hoi}}$，**无需任何额外训练**。

### 核心模块关系

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| Pairwise Instance Encoder | 生成空间接地的 HO 查询，捕获人体和物体的局部空间线索 | 空间特征图 $x$、人体/物体文本嵌入 | HO 查询 $q_k^{\mathrm{ho}}$ |
| Interaction Decoder | 通过交叉注意力解码 HO 查询，预测交互类别得分 | HO 查询、图像特征 $x$、交互文本嵌入 | 交互分类得分 $\hat{s}^{\mathrm{a}}$ |
| Interactiveness Scoring | 计算 patch 级交互性得分并聚合，用于抑制非交互区域 | patch 级交互性预测 $\hat{s}^{\mathrm{h}}(p), \hat{s}_k^{\mathrm{o}}(p)$ | 图像级/实例级交互性得分 $r$ |

### 信息流与因果机制

RegFormer 的信息流遵循 **HO → I** 的序列化推理路径：

1. **查询构建**：首先为每个人-物类别对生成 HO 查询，而非直接初始化全部 HOI 类别查询。这避免了枚举所有交互组合带来的计算冗余。

2. **空间接地**：HO 查询的构建并非简单的文本嵌入投影，而是通过 patch 重要性得分 $\alpha^{\mathrm{h}}(p)$ 和 $\alpha_k^{\mathrm{o}}(p)$ 对空间特征图进行加权聚合：
   $$q^{\mathrm{ho}}_k = \mathbb{P}_q([\sum_{p}\alpha^{\mathrm{h}}(p)x(p); \sum_{p}\alpha^{\mathrm{o}}_k(p)x(p)])$$
   这使得查询天然携带了人体和物体在图像中的空间位置信息。

3. **交互性门控**：交互性得分 $r$ 作为门控信号作用于交互分类得分，公式为 $\hat{s}_{k}^{\mathrm{hoi}} = \hat{s}_{k}^{\mathrm{a}} (r_{k}^{\mathrm{ho}})^{\gamma}$。这一机制显式地抑制了非交互人-物对的分类得分，是降低假阳性的关键因果节点。

4. **直接迁移**：在推理时，仅需将 patch 级得分约束到检测框区域即可获得实例级预测，无需重新训练或微调。最终 HOI 得分融合了交互分类、交互性得分和检测置信度：
   $$\tilde{s}_{ij}^{\mathrm{hoi}} = \tilde{s}_{ij}^{\mathrm{a}} \cdot (r_{ij}^{\tilde{\mathrm{ho}}})^{\gamma} \cdot (\tilde{s}_{i}^{\mathrm{h}} \tilde{s}_{j}^{\mathrm{o}})^{\lambda}$$

### 与基线方法的本质差异

与基础架构 **ML-Decoder**（Ridnik et al., WACV 2023）相比，RegFormer 的关键差异在于：
- ML-Decoder 直接初始化全部 HOI 类别查询，缺乏对空间位置的显式建模；
- RegFormer 通过 Pairwise Instance Encoder 将空间线索注入查询，并通过交互性得分过滤非交互区域，从而在推理效率和假阳性抑制上获得显著优势（见图 1）。

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2604_00507/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of RegFormer. RegFormer unifies image-level and instance-level reasoning within a single framework by learning to capture spatial cues for interaction reasoning using only image-level labels. During training, pairwise instance encoder constructs a human–object (HO) query*

RegFormer 的核心设计围绕一个关键洞察：将图像级的交互推理分解为“先生成人-物对查询，再解码交互”的序列化流程，并通过空间接地与交互性感知学习注入局部空间线索，从而在仅使用图像级标签的训练条件下，实现向实例级检测的直接迁移。

### 序列化推理框架：HO → I

RegFormer 采用序列化推理策略，将传统方法中直接枚举全部 HOI 类别查询的方式，替换为先生成**人-物对（HO）查询**、再预测**交互类别（I）**的两阶段流程。这一设计将交互推理的空间从 $N_{\mathrm{hoi}}$ 个全组合类别压缩到 $N_{\mathrm{ho}} = N_{\mathrm{h}} \times N_{\mathrm{o}}$ 个对查询，显著降低了计算成本，同时为后续的空间接地提供了结构化的查询载体。

### 空间接地查询生成

**成对实例编码器（Pairwise Instance Encoder）** 负责构造具有空间定位能力的 HO 查询。其核心机制是利用 patch 级特征与类别文本嵌入的语义对齐，生成空间重要性权重，进而加权聚合人体和物体的局部视觉特征。

对于人体类别，patch $p$ 的重要性得分定义为视觉特征与人体文本嵌入的余弦相似度：

$$s^{\mathrm{h}}(p) = \cos\left(\mathbb{P}_{\mathrm{v}}^{\mathrm{h}}(x(p)), \mathbb{P}_{\mathrm{t}}^{\mathrm{h}}(e^{\mathrm{h}})\right)$$

其中 $x(p)$ 为 patch 视觉特征，$e^{\mathrm{h}}$ 为人体文本嵌入，$\mathbb{P}_{\mathrm{v}}^{\mathrm{h}}$ 和 $\mathbb{P}_{\mathrm{t}}^{\mathrm{h}}$ 分别为视觉和文本投影头。通过 softmax 归一化得到空间注意力权重：

$$\alpha^{\mathrm{h}}(p) = \frac{\exp(s^{\mathrm{h}}(p)/\tau_{p})}{\sum_{p'}\exp(s^{\mathrm{h}}(p')/\tau_{p})}$$

物体侧采用类似机制，但针对每个物体类别 $k$ 分别计算：

$$s_{k}^{\mathrm{o}}(p) = \cos\left(\mathbb{P}_{\mathrm{v}}^{\mathrm{o}}(x(p)), \mathbb{P}_{\mathrm{t}}^{\mathrm{o}}(e_{k}^{\mathrm{o}})\right)$$

最终，第 $k$ 个 HO 对的空间接地查询由人体和物体的加权特征拼接后经线性投影得到：

$$q^{\mathrm{ho}}_k = \mathbb{P}_q\left(\left[\sum_{p}\alpha^{\mathrm{h}}(p)x(p); \sum_{p}\alpha^{\mathrm{o}}_k(p)x(p)\right]\right)$$

这一设计使每个 HO 查询天然携带了人体和物体在空间中的位置线索，为后续的交互解码提供了局部化的特征表示。

### 交互解码

**交互解码器（Interaction Decoder）** 通过交叉注意力机制将空间接地的 HO 查询与图像特征图进行交互，得到解码后的查询特征：

$$\bar{q}_k^{\mathrm{ho}} = \bar{\mathsf{Att}}(q_k^{\mathrm{ho}}, x, x) \in \mathbb{R}^{d}$$

随后通过余弦相似度与交互类别文本嵌入匹配，获得交互分类得分：

$$\hat{s}_k^{\mathrm{a}} = \sigma\left(\cos\left(\mathbb{P}_{\mathrm{v}}^{\mathrm{a}}(\bar{q}_k^{\mathrm{ho}}), \mathbb{P}_{\mathrm{t}}^{\mathrm{a}}(e^{\mathrm{a}})\right)\right)$$

其中 $\sigma$ 为 sigmoid 函数，$e^{\mathrm{a}}$ 为交互动作的文本嵌入。

### 交互性感知学习

为抑制非交互的人-物组合产生的假阳性，RegFormer 引入了**交互性感知学习（Interactiveness-aware Learning）** 机制。该模块利用 patch 级的目标性得分（即 $s^{\mathrm{h}}(p)$ 和 $s_{k}^{\mathrm{o}}(p)$）与可学习的交互性预测头 $\hat{s}^{\mathrm{h}}(p)$、$\hat{s}_{k}^{\mathrm{o}}(p)$ 进行加权聚合，得到图像级交互性得分：

$$r^{\mathrm{h}} = \sum_{p} \alpha^{\mathrm{h}}(p) \hat{s}^{\mathrm{h}}(p), \quad r_{k}^{\mathrm{o}} = \sum_{p} \alpha_{k}^{\mathrm{o}}(p) \hat{s}_{k}^{\mathrm{o}}(p)$$

配对交互性得分取两者的几何平均：

$$r_{k}^{\mathrm{ho}} = (r^{\mathrm{h}} r_{k}^{\mathrm{o}})^{0.5}$$

该交互性得分作为门控信号，以指数 $\gamma$ 调制交互分类得分：

$$\hat{s}_{k}^{\mathrm{hoi}} = \hat{s}_{k}^{\mathrm{a}} \cdot (r_{k}^{\mathrm{ho}})^{\gamma}$$

训练时，交互性得分接受显式的二值监督（交互/非交互），迫使模型学习区分真正发生交互的区域与仅有语义对齐的非交互区域。消融实验表明，仅使用局部交互性得分时 HICO-DET Full mAP 为 23.44，加入全局交互性得分后跃升至 30.01（Table 5），验证了全局上下文对抑制非交互区域的关键作用。

### 实例级检测的零训练迁移

RegFormer 的独特优势在于无需额外训练即可从图像级分类迁移到实例级检测。给定外部检测器输出的人体实例 $i$ 和物体实例 $j$ 的边界框，通过引入**区域感知掩码** $m_{i}^{\tilde{\mathrm{h}}}(p)$ 和 $m_{j}^{\tilde{\mathrm{o}}}(p)$，将 patch 重要性得分的计算约束在实例区域内：

$$\alpha_{i}^{\tilde{\mathrm{h}}}(p) = \frac{\exp((s^{\mathrm{h}}(p) + \log m_{i}^{\tilde{\mathrm{h}}}(p))/\tau_{p})}{\sum_{p'} \exp((s^{\mathrm{h}}(p') + \log m_{i}^{\tilde{\mathrm{h}}}(p'))/\tau_{p})}$$

同理可得实例级物体重要性权重 $\alpha_{j}^{\tilde{\mathrm{o}}}(p)$。由此构造实例级 HO 查询和交互性得分，最终 HOI 预测得分为三部分的乘积：

$$\tilde{s}_{ij}^{\mathrm{hoi}} = \tilde{s}_{ij}^{\mathrm{a}} \cdot (r_{ij}^{\tilde{\mathrm{ho}}})^{\gamma} \cdot (\tilde{s}_{i}^{\mathrm{h}} \tilde{s}_{j}^{\mathrm{o}})^{\lambda}$$

其中 $\tilde{s}_{ij}^{\mathrm{a}}$ 为交互分类得分，$r_{ij}^{\tilde{\mathrm{ho}}}$ 为实例级交互性得分，$\tilde{s}_{i}^{\mathrm{h}}$ 和 $\tilde{s}_{j}^{\mathrm{o}}$ 为检测器输出的人体和物体置信度，$\gamma$ 和 $\lambda$ 为调节因子。这一公式将交互推理、交互性门控和检测置信度有机融合，实现了从图像级标签到实例级预测的直接迁移。

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2604_00507/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of weakly-supervised HOI detection frameworks. (A) As the number of instance pairs increases, Reg-Former shows only a marginal increase in inference time, whereas the ML-Decoder becomes significantly slower. (B) In addition, RegFormer effectively suppresses non-interactive human–object pairs, producing less false positives*

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2604_00507/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of interactiveness score in HOI detection. Top row shows the interactiveness score for the human (red box), and the bottom row shows the score for the object (blue box). In row 1, for the human, the masked global interactiveness (0.01) corrects the inflated local interactiveness (0.768) caused by strong semantic alignment between the human and the patch, reducing the pairwise score of the non-interactive region (red box) to 0.008*

## 实验与关键发现

### 组件消融：从ML-Decoder到RegFormer

RegFormer的核心设计可视为在ML-Decoder（Ridnik et al., WACV 2023）基础上的三个关键改造：顺序推理（HO→I）、空间接地查询（SG）和交互性感知学习（IA）。Table 1系统消融了各组件的贡献。

**基线性能。** 纯ML-Decoder在HICO-DET上仅取得17.49 Full mAP，这揭示了直接枚举所有HOI类别进行图像级分类的本质缺陷——模型缺乏对空间位置的感知能力，无法区分交互与非交互的人-物对。

**顺序推理（HO→I）。** 将HOI查询分解为先生成HO对查询、再解码交互的两阶段过程，使HICO-DET Full mAP从17.49提升至21.90（+4.41），HICO分类mAP从52.6提升至55.0（+2.4）。这一提升验证了分解推理的有效性：通过显式建模人-物对组合，模型避免了对不存在的HO组合进行交互推理，从而减少了搜索空间中的假阳性。

**空间接地查询（SG）。** 在HO→I基础上引入空间接地查询，HICO-DET Full mAP进一步提升至23.74（+1.84），HICO分类mAP升至57.0（+2.0）。这表明通过patch级相似度加权聚合空间特征，模型获得了对人-物空间位置的感知能力，能够更准确地定位交互区域。

**交互性得分（IA）。** 加入交互性感知学习后，模型达到最优性能：HICO-DET Full mAP 30.01（+6.27），HICO分类mAP 57.6（+0.6）。IA在检测任务上的增益远大于分类任务，说明交互性得分作为门控信号的核心价值在于**实例级假阳性抑制**——它直接降低了非交互人-物对的得分，而非仅改善类别判别。

### 交互性得分的局部与全局消融

Table 5进一步拆解了交互性得分的内部机制。仅使用局部交互性得分时，HICO-DET Full mAP为23.44；加入全局交互性得分后跃升至30.01（+6.57）。这一巨大差距揭示了局部交互性的根本局限：当人体或物体的局部patch与文本嵌入语义高度对齐时（例如“人”与“冲浪板”附近的patch），局部交互性得分会被膨胀，导致非交互区域被错误地赋予高交互性。全局交互性得分通过在整个图像范围内重新加权patch重要性，有效纠正了这种局部膨胀效应。

Figure 3的可视化直观展示了这一互补机制：在人体实例上，局部交互性得分高达0.768，但掩码全局交互性得分仅为0.01，最终将非交互区域的成对得分压制至0.008。这证实了全局上下文对于准确判断交互性的必要性。

### 与全监督和弱监督方法的对比

Table 2展示了RegFormer在HICO-DET上与现有方法的全面对比。使用Faster R-CNN检测器时，RegFormer取得30.01 Full mAP，显著超越弱监督基线**Weakly HOI-CLIP**（Wan et al., ICLR 2023）的31.14（注：原文Table 2中RegFormer的30.01与Weakly HOI-CLIP的31.14存在矛盾，需人工核实——可能涉及不同检测器配置或后处理策略）。当配备更强的H-DETR检测器、DINO-B视觉编码器和CLIP-B文本编码器时，RegFormer达到38.14 Full mAP，超越了多数弱监督方法，并接近部分全监督方法的性能水平。

在V-COCO数据集上（Table 3），RegFormer同样展现出竞争力，但需注意部分对比方法（如OpenCat，以†标注）额外使用了大规模弱监督预训练，性能对比存在不公平因素。

### 零样本泛化能力

Table 4的零样本HOI检测结果揭示了RegFormer的泛化特性。在RF-UC（Rare-First Unseen Composition）设定下，RegFormer取得31.53 Unseen mAP，相较OpenCat的21.46提升+10.07，展现了强大的未见组合识别能力。然而，在NF-UC（Non-Rare-First）设定下，性能增益相对较小，且Unseen mAP（31.53）仍显著低于Seen mAP（38.14），表明模型对新颖交互组合的泛化仍存在挑战——空间接地查询和交互性得分主要捕捉的是已见交互模式的空间特征，对未见组合的迁移能力有限。

### 推理效率与假阳性抑制

Figure 1从效率和质量两个维度展示了RegFormer相对于ML-Decoder的优势。在效率方面（Figure 1A），随着实例对数量增加，ML-Decoder的推理时间急剧增长（因为需要枚举所有HOI类别查询），而RegFormer仅呈现边际增长——这源于其顺序推理架构将HOI推理分解为HO对生成和交互解码，避免了组合爆炸。在质量方面（Figure 1B），RegFormer有效抑制了非交互人-物对的假阳性，这直接归因于交互性得分的门控机制。

### 失败模式与局限

尽管RegFormer在弱监督HOI检测中取得了显著进展，仍存在以下局限：

1. **检测器依赖性。** RegFormer依赖外部目标检测器生成实例提议，其检测性能受限于检测器质量。Table 7显示，不同视觉编码器（如ResNet-50与ViT-B）会导致性能波动，且检测器的定位精度直接影响最终的HOI检测结果。

2. **零样本泛化不足。** 如前所述，未见组合的性能显著低于已见组合，说明模型对新颖交互的空间模式缺乏泛化能力。交互性得分依赖于训练中见过的交互模式，当面对全新的<人，物，动作>三元组时，其抑制作用可能失效。

3. **密集场景挑战。** Figure 4的定性结果显示，在密集场景中，patch重要性得分可能出现扩散现象——当多个人或物体紧密相邻时，空间接地查询的注意力权重可能错误地聚合到相邻实例的特征上，导致HO查询的定位精度下降。

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2604_00507/figures/004_Table_2.jpg]]
*Table 2: Weakly & Fully supervised HOI detection on HICO-DET benchmark dataset*

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2604_00507/figures/009_Table_5.jpg]]
*Table 5: Ablation on Interactiveness Scoring on HICO-DET. Local and Global stand for local interactiveness and masked global interactiveness, respectively*

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2604_00507/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative results on patch importance score. We visualize the human patch importance score, αh(p)*

## 定位与知识库关联

### 与基线方法的关系

RegFormer 的核心技术路线源于对两类基线的继承与改造：**多标签分类架构**和**弱监督 HOI 检测范式**。

在架构层面，RegFormer 以 **ML-Decoder**（Ridnik et al., WACV 2023）为基础分类头部。ML-Decoder 采用文本嵌入初始化的 HOI 类别查询，通过交叉注意力与图像特征交互，直接输出图像级分类得分。RegFormer 保留了这一查询-解码框架，但对其进行了两个关键改造：其一，将扁平化的 HOI 查询分解为顺序生成的 HO→I 查询（先生成人-物对查询，再解码交互类别）；其二，在查询构建中注入空间接地信息，使查询携带局部空间线索而非仅依赖全局语义。消融实验表明，仅保留 HO→I 推理（移除空间接地查询和交互性得分）时，模型退化为 ML-Decoder 的等价形式，HICO-DET Full mAP 仅为 17.49（Table 1）。

在弱监督 HOI 检测范式层面，RegFormer 的直接对比基线是 **Weakly HOI-CLIP**（Wan et al., ICLR 2023）。Weakly HOI-CLIP 同样利用 CLIP 的视觉-语言对齐能力进行图像级弱监督学习，但需要枚举大量候选人对进行推理。RegFormer 通过空间接地查询和交互性得分，在推理效率上形成显著优势：随着实例对数量增加，RegFormer 的推理时间仅边际增长，而 ML-Decoder 基线显著变慢（Figure 1A）。在 HICO-DET 上，RegFormer 以 Faster R-CNN 检测器取得 33.33 Full mAP，超越 Weakly HOI-CLIP 的 31.14（Table 2）。

### 方法适用边界

RegFormer 的适用性受以下条件约束：

1. **依赖外部目标检测器**：RegFormer 的训练仅使用图像级标签，但实例级 HOI 检测仍需外部检测器生成人和物体的边界框提议。检测器的质量直接影响最终检测性能——使用更强的 H-DETR 检测器可将 Full mAP 从 30.01 提升至 38.14（Table 2）。这意味着该方法目前无法实现完全端到端的弱监督检测。

2. **静态图像场景**：论文仅在 HICO-DET 和 V-COCO 两个静态图像基准上验证了方法，未在视频数据或其他动态场景中测试可迁移性。对于时序交互推理（如动作持续时间的建模），RegFormer 的框架需要进一步扩展。

3. **零样本泛化**：在零样本设定下，RegFormer 在未见组合（RF-UC）上取得 31.53 Unseen mAP，显著优于 OpenCat 的 21.46（Table 4），但该性能仍远低于已见组合。这表明模型对新颖人-物-交互三元组的泛化能力存在上限。

### 局限与开放问题

**已知局限**：

- **检测器耦合**：RegFormer 的检测性能受限于外部检测器的质量。论文未探索将交互性得分机制集成到端到端检测器中的可能性。
- **公平性存疑**：部分对比方法（如 OpenCat）额外使用了大规模弱监督预训练（Table 4 中以 † 标注），而 RegFormer 未使用此类预训练，性能对比可能存在不公平。
- **交互性得分的全局-局部平衡**：消融实验显示，仅使用局部交互性得分时 Full mAP 为 23.44，加入全局交互性得分后提升至 30.01（Table 5），表明全局上下文对抑制非交互区域至关重要。但论文未深入分析全局与局部交互性在不同场景下的失效模式。

**开放问题**：

1. **端到端弱监督检测**：能否将空间接地查询和交互性得分的思想直接集成到检测器中，实现无需外部检测器的弱监督 HOI 检测？这需要解决检测与交互推理的联合优化问题。

2. **跨任务迁移**：空间接地查询方法本质上是一种利用视觉-语言对齐注入局部空间线索的机制，该思路是否适用于其他需要实例间关系推理的任务（如场景图生成、视觉关系检测）？这需要验证该方法在非人-物交互场景下的泛化能力。

3. **交互性得分的监督信号设计**：当前交互性得分通过图像级标签间接监督，是否可以利用更细粒度的弱监督信号（如文本描述中的空间关系）来提升交互性得分的准确性？

## 原文 PDF

![[paperPDFs/CVPR_2026/RegFormer_Transferable_Relational_Grounding_for_Efficient_Weakly_Supervised_Human_Object_Interaction_Detection.pdf]]
