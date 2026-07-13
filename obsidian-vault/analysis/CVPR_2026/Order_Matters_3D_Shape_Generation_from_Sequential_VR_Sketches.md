---
title: "Order Matters: 3D Shape Generation from Sequential VR Sketches"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Order_Matters_3D_Shape_Generation_from_Sequential_VR_Sketches.pdf
project_link: "https://chenyizi086.github.io/VRSketch2Shape_website/"
code_link: null
aliases:
- OM3SGFSVS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 引入顺序感知的草图编码器：将草图建模为有序的笔画序列和点序列，使用改进的BERT结构结合空间傅里叶特征与连续位置编码，并配合时序数据增强策略。
primary_logic: VR草图的绘制顺序编码了结构的连接性、层次与设计意图；显式建模时序信息能够指导扩散模型生成几何精度更高、拓扑更准确的形状，尤其对部分草图补全效果显著。
claims:
- 去除笔画和点顺序（w/o ordering）后，F-score从56.8骤降至48.9，CD×1000从5.1升至7.1。
- 在仅用前50%类人草图点的补全任务中，顺序感知模型比顺序无关模型F1-score高出+6.6。
- 打乱点顺序导致F-score从56.8降至52.2，打乱笔画顺序降至54.6；反转笔画顺序则影响甚微。
- 3DVRChair 上 F-score↑ = 31.1
---

# Order Matters: 3D Shape Generation from Sequential VR Sketches

> [!tip] 核心洞察
> VR草图的绘制顺序编码了结构的连接性、层次与设计意图；显式建模时序信息能够指导扩散模型生成几何精度更高、拓扑更准确的形状，尤其对部分草图补全效果显著。

| 字段 | 内容 |
|------|------|
| 中文题名 | 顺序至关重要：基于时序VR草图的3D形状生成 |
| 英文题名 | Order Matters: 3D Shape Generation from Sequential VR Sketches |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.04761) · [Project](https://chenyizi086.github.io/VRSketch2Shape_website/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | VRSketch2Shape |
| Dataset | 3DVRChair, VRSketch2Shape, User Study |

> [!tip] 效果简介
> - 3DVRChair 上，F-score↑ 31.1 vs 26.6 (Luo et al.) (+4.5)；CD×1000↓ 25.8 vs 35.5 (Luo et al.) (−9.7)。
> - VRSketch2Shape (椅类别) 上，F-score↑ 64.3 vs 42.2 (Luo et al.) (+22.1)。
> - VRSketch2Shape (全部类别) 上，F-score↑ 69.8 vs 48.8 (Luo et al.) (+21.0)。

## 概要

**核心问题：** 现有VR草图驱动的3D形状生成方法将草图视为无序三维点云，完全丢弃了笔画顺序、点顺序以及连接关系等蕴含结构与设计意图的时序信息。这一信息瓶颈导致生成形状的几何精度和拓扑准确性受到根本性制约。

**核心方案：** 本文提出 **VRSketch2Shape**，首个面向时序VR草图的多类别3D形状生成框架。其核心洞察在于：VR草图的绘制顺序编码了结构的连接性、层次与设计意图——显式建模时序信息能够指导扩散模型生成几何精度更高、拓扑更准确的形状。方法层面，将草图建模为有序的笔画序列和点序列，使用改进的BERT结构结合空间傅里叶特征与连续位置编码，并配合时序数据增强策略，构建了端到端的顺序感知生成管线。

**方法定位：** 与基于无序点云的VR草图生成方法（如Luo et al.）和基于2D渲染的草图生成方法（如LAS-Diffusion）不同，VRSketch2Shape在草图表示形式、空间编码、位置编码、序列建模和训练策略五个关键槽位上实现了系统性改进，将草图编码从无序聚合范式转向时序感知的Transformer序列建模范式。

**主要结果：** 在公开的3DVRChair基准上，VRSketch2Shape相较Luo et al.将F-score从26.6提升至31.1，CD×1000从35.5降至25.8；在自建的VRSketch2Shape多类别数据集上，F-score从48.8提升至69.8，CD×1000从13.0降至4.8。用户研究中，有参考形状场景的Likert评分从2.76提升至3.92，自由手绘场景从2.02提升至3.60。消融实验揭示，去除笔画和点顺序后F-score从56.8骤降至48.9，CD×1000从5.1升至7.1，证实了时序信息的关键因果作用。在仅用前50%草图点的补全任务中，顺序感知模型比顺序无关模型F1-score高出+6.6，凸显了时序建模对部分输入场景的显著增益。

3D形状生成是计算机图形学与交互设计的核心任务，其目标是从用户输入快速构建可编辑的三维模型。近年来，虚拟现实（VR）作为沉浸式三维创作媒介迅速普及，VR草图——用户在三维空间中直接绘制的笔画序列——因其直观性和表达自由度，正成为一种极具潜力的3D建模输入模态。然而，从VR草图自动生成高质量3D形状仍面临根本性挑战。

**现有方法的瓶颈：时序信息的系统性丢失。** 当前主流的VR草图生成方法将草图视为无序的三维点云，通过PointNet++等无序聚合器提取全局特征，再输入变分自编码器（VAE）或潜空间对齐模块生成形状。这一范式完全丢弃了VR草图的核心结构信息——笔画顺序、点顺序以及连接关系。在人类绘制过程中，笔画的先后顺序编码了物体的连接性、层次关系和设计意图：先画主干再画分支，先定轮廓再补细节。将这些时序信号压平为无序点集，等同于剥离了草图中蕴含的构造逻辑，导致生成形状在几何精度和拓扑一致性上存在显著退化。

**关键因果杠杆：顺序感知的草图编码。** 本文的核心洞察在于：VR草图的绘制顺序本身是一种强监督信号，显式建模时序信息能够指导生成模型输出更忠实的形状。这一判断得到了消融实验的有力支持——去除笔画和点顺序后，F-score从56.8骤降至48.9，Chamfer Distance（CD×1000）从5.1升至7.1（Table 4）；在仅提供前50%类人草图点的补全任务中，顺序感知模型比顺序无关模型的F1-score高出+6.6（Section A-1）。打乱点顺序导致F-score降至52.2，打乱笔画顺序降至54.6；而反转笔画顺序影响甚微，说明模型学到的是相对顺序而非绝对方向（Table A-1 [C]）。

**数据集缺口：缺乏大规模、多类别、带时序标注的VR草图资源。** 现有3D草图数据集（如3DVRChair）仅覆盖单一椅类，且不包含真实手绘草图或完整的时序标注。本文构建了VRSketch2Shape数据集，包含20,838对合成草图-形状对（覆盖椅、桌、柜、飞机四类）和900张经表面吸附工具采集的真实手绘VR草图，首次为多类别时序草图生成研究提供了开放基准（Table 1）。

**方法定位。** 与基于无序点云的Luo et al.和基于多视角2D渲染的LAS-Diffusion等基线不同，VRSketch2Shape将草图建模为有序笔画序列——每个笔画为有序点序列，以SEP/EoS分隔符标记边界——并通过空间傅里叶特征编码、连续傅里叶位置编码和轻量级BERT编码器提取时序感知的草图表征，最终以SDFUSION潜扩散模型实现端到端的单阶段形状生成。这一设计在3DVRChair和VRSketch2Shape两个基准上均大幅超越先前方法，在全部类别上F-score提升+21.0，CD×1000降低-8.2（Table 2），用户研究Likert评分在自由手绘场景下领先+1.58（Table 3）。

## 核心方法与创新机理

### 问题根因：时序信息的系统性缺失

现有VR草图生成方法将草图视为无序三维点云，通过PointNet++等置换不变算子进行特征聚合，完全丢弃了笔画顺序、点顺序以及连接关系。这一设计忽略了VR草图区别于普通点云的本质属性——**绘制顺序编码了结构的连接性、层次与设计意图**。例如，一个椅子的四条腿通常按相同方向依次绘制，扶手与座面的连接关系隐含在笔画的先后顺序中。将此类时序信号抹平后，模型被迫仅从空间坐标推断拓扑结构，导致生成形状在几何精度与拓扑一致性上均受限制。

### 核心洞察：顺序即结构信号

VRSketch2Shape的核心假设是：**VR草图的绘制顺序本身就是一种强结构先验**。笔画顺序反映了物体的部件层次（先画主体再画细节），点顺序反映了局部几何的走向（连续点的轨迹定义了曲面法向与边界）。显式建模这些时序信息，能够为扩散模型提供更丰富的条件信号，使其在去噪过程中更准确地恢复隐式曲面的拓扑与细节。这一洞察在消融实验中得到直接验证：去除笔画和点顺序后，F-score从56.8骤降至48.9，CD×1000从5.1升至7.1（Table 4），性能退化幅度远超其他组件。

### 关键创新点

与现有方法相比，VRSketch2Shape在以下五个维度上进行了系统性重构：

#### 1. 草图表示：从无序点云到有序笔画序列

基线方法将VR草图采样为无序3D点云，VRSketch2Shape则将其建模为有序的笔画序列，每个笔画为有序点序列，以SEP分隔笔画、EoS标记结束：

$$\mathcal{S} = \left[ p_1^1, \cdots, p_{n_1}^1, \mathrm{SEP}, \cdots, p_1^S, \cdots, p_{n_S}^S, \mathrm{SEP}, \mathrm{EoS} \right]$$

这一序列化表示保留了完整的时序结构，使编码器能够同时感知空间几何与绘制过程。

#### 2. 空间编码：从原始坐标到3D傅里叶特征

基线方法直接使用原始坐标或经PointNet++处理，VRSketch2Shape引入3D空间傅里叶特征编码：

$$\Phi_{\mathrm{spa}}(t) = \left[ \sin(2^{\ell} \pi t), \cos(2^{\ell} \pi t) \right]_{\ell=0}^{L-1} \in \mathbb{R}^{2L}$$

$$E_{\mathrm{spa}}(p) = \mathrm{MLP}_{\mathrm{spa}}\big( \big[ \Phi_{\mathrm{spa}}(x), \Phi_{\mathrm{spa}}(y), \Phi_{\mathrm{spa}}(z) \big] \big)$$

多频率傅里叶特征使MLP能够捕捉高频几何细节，消融中去除该编码导致F-score从56.8降至52.1（Table A-1 [A]）。

#### 3. 位置编码：从无编码到连续傅里叶双索引编码

基线方法不编码位置或使用固定查找表，VRSketch2Shape采用连续傅里叶位置编码，分别编码笔画索引$s$和点索引$i$：

$$\Phi_{\mathrm{seq}}(t) = \left[ \sin\left( \frac{t}{10,000^{2d/D}} \right), \cos\left( \frac{t}{10,000^{2d/D}} \right) \right]_{d=0}^{D/2-1}$$

最终token嵌入综合三种信号：

$$E(p_i^s) = E_{\mathrm{spa}}(p_i^s) + E_{\mathrm{stroke}}(s) + E_{\mathrm{point}}(i)$$

去除1D傅里叶位置编码改用固定编码后，F-score从56.8降至48.2（Table A-1 [A]），证明连续位置编码对时序建模至关重要。

#### 4. 序列建模：从无序聚合到轻量级BERT编码器

基线方法依赖无序聚合（PointNet++）或池化，VRSketch2Shape采用6层8头轻量级BERT编码器处理序列化草图。BERT的自注意力机制天然适合捕捉笔画间与点间的长程依赖关系。对比实验显示，使用SketchBERT替代本设计导致精度显著下降（Table 4），表明针对3D草图定制的编码策略优于直接迁移2D方案。

#### 5. 训练策略：从单域训练到合成预训练+时序增强+少样本微调

VRSketch2Shape采用三阶段训练策略：首先在20,838对合成数据上大规模预训练，配合随机时序增强（笔画/点丢弃、笔画互换）提升鲁棒性；随后仅需每类别50张真实草图即可使F-score和CD接近全量微调水平（Figure 5）。去除数据增强或合成预训练均导致性能大幅下降（Table 4），验证了该策略对弥合合成-真实域间隙的关键作用。

### 创新点的因果链路

上述五个创新点构成一条完整的因果链：**序列化表示**保留了时序信息→**傅里叶空间编码**捕捉高频几何→**双索引位置编码**注入结构先验→**BERT序列建模**提取笔画间依赖→**三阶段训练**弥合域间隙。消融实验中，去除顺序信息（w/o ordering）造成的性能退化最为严重，证明时序建模是该链路的瓶颈节点，也是VRSketch2Shape相对于基线方法的核心优势来源。

### 与基线方法的本质差异

与Luo et al.的无序点云方法相比，VRSketch2Shape的根本差异不在于生成器架构（两者均可用扩散模型），而在于**条件信号的表达力**：前者将草图压缩为几何信息的无序集合，后者将草图保留为几何+时序的结构化序列。这一差异在部分草图补全任务中尤为突出——当仅提供前50%类人草图点时，顺序感知模型比顺序无关模型F1-score高出+6.6（Section A-1），说明时序信息在信息不完整时具有更强的推断能力。

VRSketch2Shape 的整体框架围绕一个核心洞察构建：**VR 草图的绘制顺序编码了结构的连接性、层次与设计意图**，而现有方法将草图视为无序三维点云，完全丢弃了这些时序信息。为此，该工作提出了一套从数据生成到形状推理的完整流水线，包含三个关键模块。

### 合成草图生成流水线

为支撑大规模训练，作者设计了一条**无需学习的启发式合成草图生成流水线**（Figure 2），可从任意三维网格自动生成具有时序顺序的 VR 草图。该流水线包含四个步骤：

![[assets/figures/papers/paper_list_l2556_https_arxiv_org_abs_2512_04761/figures/003_Figure_2.jpg]]
*Figure 2: Synthetic Sketch Generation. We propose a heuristic, learning-free pipeline for generating 3D sequential sketches from 3D shapes. We first uniformly sample points on the surface and retain only salient points. Bezier splines are then fitted through these points ´ to form candidate strokes, which are subsequently merged and simplified. Finally, we order both points and stroke to obtain temporally sequential 3D sketches*

1. **显著点提取**：在网格表面均匀采样点，仅保留几何显著点。
2. **贝塞尔样条拟合**：通过显著点拟合贝塞尔样条，形成候选笔画。
3. **笔画合并与简化**：合并冗余笔画并简化，得到结构清晰的笔画集合。
4. **深度优先遍历排序**：采用深度优先遍历对笔画和点进行排序，赋予合成草图以时序结构。

该流水线完全基于几何启发式，无需任何训练，可高效生成与真实 VR 草图风格一致的时序数据。

### 顺序感知草图编码器

输入 VR 草图被建模为**有序的笔画序列和点序列**（Equation 1），每个笔画内部点按绘制顺序排列，笔画之间以 SEP 分隔符标记，序列末尾以 EoS 标记结束。编码器由三个嵌入层和一个轻量级 BERT 编码器组成（Figure 3）：

![[assets/figures/papers/paper_list_l2556_https_arxiv_org_abs_2512_04761/figures/004_Figure_3.jpg]]
*Figure 3: VRSKETCH2SHAPE Model. An input VR sketch is tokenized into a sequence of points organized along ordered strokes. Each 3D point is encoded using 3D Fourier features and an MLP, while stroke and point indices are encoded with 1D Fourier features followed by a linear projection. The resulting embeddings are summed and passed through a lightweight BERT encoder. The encoded token sequence is then used to condition SDFUSION, a diffusion-based 3D shape generation model*

- **空间傅里叶特征编码**：对三维坐标进行多频率傅里叶编码以捕捉高频几何细节（Equation 2），再经 MLP 映射到模型维度（Equation 3）。
- **连续傅里叶位置编码**：分别对笔画索引和点索引进行一维傅里叶位置编码（Equation 4–6），为模型提供显式的时序信息。
- **Token 嵌入合成**：每个点的最终嵌入由空间嵌入、笔画位置嵌入和点位置嵌入三者求和得到（Equation 7）。

编码后的 token 序列经 6 层、8 头的轻量级 BERT 编码器处理，输出上下文感知的特征序列，作为下游生成器的条件输入。

### SDFUSION 潜扩散生成器

形状生成器采用基于 SDFUSION 的潜扩散模型，以端到端单阶段方式训练。该模块接收编码后的草图特征序列作为条件，通过扩散与去噪过程在隐空间中生成隐式 SDF 表示，最终解码为三维形状。与需要多阶段对齐的 VAE 方案相比，该设计简化了训练流程并提升了生成质量。

### 训练策略

训练采用**合成数据大规模预训练 + 随机时序增强 + 少量真实数据微调**的策略。时序增强包括笔画丢弃、点丢弃和笔画互换，旨在提升模型对真实草图中绘制顺序变化的鲁棒性。消融实验表明，去除数据增强或合成预训练均会导致性能显著下降（Table 4）。少样本微调实验中，每类别仅需 50 张真实草图即可使 F-score 和 CD 接近全量微调水平（Figure 5），验证了预训练先验的有效迁移能力。

VRSketch2Shape 的核心设计围绕一个关键洞察展开：**VR 草图的绘制顺序编码了结构的连接性、层次与设计意图**。现有方法将草图视为无序三维点云，完全丢弃了笔画顺序、点顺序以及连接关系等时序信息。本方法通过三个紧密耦合的模块将顺序信息显式注入生成流程。

### 草图序列化与 Tokenization

VR 草图由 $S$ 条有序笔画组成，每条笔画 $s$ 包含 $n_s$ 个有序三维点。系统将其展平为统一的 token 序列：

$$\mathcal{S} = \left[ p_1^1, \cdots, p_{n_1}^1, \mathrm{SEP}, \cdots, p_1^S, \cdots, p_{n_S}^S, \mathrm{SEP}, \mathrm{EoS} \right]$$

其中 $\mathrm{SEP}$ 为笔画分隔符（可学习的特殊 token），$\mathrm{EoS}$ 为序列结束标记。这一表示同时保留了**笔画内点的绘制顺序**和**笔画间的先后顺序**，是后续顺序感知编码的基础。

### 空间嵌入：三维傅里叶特征 + MLP

直接使用原始坐标 $(x, y, z)$ 难以捕捉高频几何细节。本模块对每个坐标分量独立施加多频率傅里叶编码：

$$\Phi_{\mathrm{spa}}(t) = \left[ \sin(2^{\ell} \pi t), \cos(2^{\ell} \pi t) \right]_{\ell=0}^{L-1} \in \mathbb{R}^{2L}$$

其中 $L$ 为频率层级数，$t$ 为 $x$、$y$ 或 $z$ 分量。三个分量的傅里叶特征拼接后经 MLP 映射到模型维度 $D$：

$$E_{\mathrm{spa}}(p) = \mathrm{MLP}_{\mathrm{spa}}\big( \left[ \Phi_{\mathrm{spa}}(x), \Phi_{\mathrm{spa}}(y), \Phi_{\mathrm{spa}}(z) \right] \big)$$

消融实验证实该设计的关键性：去除三维傅里叶特征、改用原始坐标后，F-score 从 56.8 降至 52.1，CD×1000 从 5.1 升至 5.6（Table A-1 [A]），说明傅里叶编码对捕捉几何细节至关重要。

### 位置编码：连续傅里叶位置编码

为让模型感知 token 在序列中的位置，本模块分别对**笔画索引** $s$ 和**点索引** $i$ 施加一维傅里叶位置编码：

$$\Phi_{\mathrm{seq}}(t) = \left[ \sin\left( \frac{t}{10,000^{2d/D}} \right), \cos\left( \frac{t}{10,000^{2d/D}} \right) \right]_{d=0}^{D/2-1}$$

该编码连续且平滑，能泛化到训练时未见过的序列长度。消融表明，去除一维傅里叶位置编码、改用固定编码后，F-score 从 56.8 骤降至 48.2，CD×1000 从 5.1 升至 6.3（Table A-1 [A]），降幅甚至超过去除空间傅里叶特征，说明**顺序信息的显式编码是模型性能的核心支柱**。

### 最终 Token 嵌入与 BERT 编码器

每个点 token 的最终嵌入由三部分求和得到：

$$E(p_i^s) = E_{\mathrm{spa}}(p_i^s) + E_{\mathrm{stroke}}(s) + E_{\mathrm{point}}(i)$$

其中 $E_{\mathrm{stroke}}(s)$ 和 $E_{\mathrm{point}}(i)$ 分别由 $\Phi_{\mathrm{seq}}(s)$ 和 $\Phi_{\mathrm{seq}}(i)$ 经线性投影得到。这种分解设计使空间几何、笔画层级、点层级的位置信息相互独立又协同作用。

嵌入后的 token 序列送入一个**轻量级 BERT 编码器**（6 层 Transformer，8 个注意力头），输出上下文感知的特征序列。该序列随后作为条件信号注入下游的 **SDFUSION 潜扩散生成器**，通过扩散与去噪过程生成隐式 SDF 表示，最终重建为三维网格。

### 训练策略：时序数据增强

为提升模型对真实绘制顺序变化的鲁棒性，训练中引入随机时序增强：随机丢弃笔画或点、随机交换相邻笔画顺序。消融显示，去除增强后性能显著下降（Table 4），而打乱笔画顺序仅使 F-score 从 56.8 降至 54.6，打乱点顺序降至 52.2，反转笔画顺序则影响甚微（Table A-1 [C]），表明模型通过增强学习到了对合理顺序扰动的容忍能力。

## 实验与关键发现

### 核心定量结果

VRSketch2Shape在公开基准3DVRChair和自建VRSketch2Shape数据集上均以大幅优势超越现有方法。在3DVRChair上，F-score达到31.1，较Luo et al.的26.6提升+4.5，CD×1000降至25.8（Luo et al.为35.5，降低9.7）。在VRSketch2Shape数据集上优势更为显著：全部类别F-score 69.8 vs. 48.8（+21.0），CD×1000 4.8 vs. 13.0（−8.2）；椅类别F-score 64.3 vs. 42.2（+22.1）。这些结果表明，顺序感知编码带来的几何精度提升在真实VR草图上尤为突出。

需要指出，所有对比方法均使用完全相同的合成预训练数据（20,838对）和真实微调数据（500对），并在相同测试集上评估，公平性得到保证。LAS-Diffusion因使用2D多视角渲染而非原生3D草图表示，其性能显著低于直接处理3D输入的方法。

### 用户研究

双盲用户研究（Table 3）进一步验证了主观质量优势。在有参考形状的绘制场景中，VRSketch2Shape获得3.92±0.74的Likert评分（5分制），Luo et al.为2.76±0.84；在自由手绘场景中，评分差距更大（3.60±1.01 vs. 2.02±0.89）。自由手绘场景下基线方法得分骤降，而VRSketch2Shape保持较高水平，说明顺序感知编码对非理想输入具有更强的鲁棒性。

![[assets/figures/papers/paper_list_l2556_https_arxiv_org_abs_2512_04761/figures/008_Table_3.jpg]]
*Table 3: User Study. Likert scale: 5-Excellent: faithful geometry; 4-Good: minor artifacts; 3-Acceptable: recognizable, missing details; 2-Poor: weak correspondence; 1-Failed*

### 消融实验

消融实验（Table 4）系统拆解了各组件的贡献，所有变体均在合成数据训练、真实椅类草图评估的条件下进行。

![[assets/figures/papers/paper_list_l2556_https_arxiv_org_abs_2512_04761/figures/010_Table_4.jpg]]
*Table 4: Ablation study. We evaluate variants of our models trained on synthetic sketches and evaluated on real chair sketches to show the contribution of each component. Discarding stroke order, augmentations, or pretraining significantly degrades performance, while alternative sketch format (point clouds or multiview) fail to capture 3D sequential structure effectively*

**顺序信息的关键作用。** 去除笔画和点顺序索引后，F-score从56.8骤降至48.9（−7.9），CD×1000从5.1升至7.1（+2.0）。将草图表示为无序点云时性能进一步恶化：F-score仅30.8，CD×1000达25.8。这直接验证了核心假设——时序顺序编码了结构连接性与设计意图，丢弃顺序等价于丢失关键的几何拓扑信息。

**顺序扰动的敏感性分析。** 补充消融（Table A-1 [C]）揭示了不同顺序维度的贡献差异：打乱点顺序导致F-score降至52.2（−4.6），打乱笔画顺序降至54.6（−2.2），而反转笔画顺序影响甚微。这表明点内顺序比笔画间顺序更关键，且模型对绘制方向不敏感，但对局部连续性高度依赖。此外，将合成数据生成的DFS遍历顺序替换为BFS遍历，F-score降至47.8（−9.0），说明DFS提供的结构化归纳偏置对预训练至关重要。

**编码器设计的贡献。** 去除3D空间傅里叶特征、改用原始坐标后，F-score降至52.1（−4.7），CD×1000升至5.6（+0.5），证实高频空间编码对几何细节重建不可或缺。去除1D连续傅里叶位置编码、改用固定编码后，F-score降至48.2（−8.6），CD×1000升至6.3（+1.2），降幅甚至超过去除顺序信息本身，说明连续位置编码是顺序感知机制的核心使能器。使用SketchBERT编码器替代本设计同样导致显著性能下降，表明针对3D草图定制的编码方案优于直接扩展2D方法。

**数据策略的贡献。** 去除时序数据增强（笔画/点丢弃、笔画互换）后性能显著下降；去除合成预训练、仅用200张真实椅类草图训练时性能大幅下降，验证了大规模合成预训练+时序增强+少量真实微调这一策略的有效性。

### 少样本适应

少样本实验（Figure 5）显示，模型在合成数据预训练后，仅需每类别50张真实草图即可使F-score和CD接近全量微调水平。这一高效适应能力得益于时序增强策略使模型在预训练阶段就学习了多样的绘制顺序模式，降低了真实草图的域迁移难度。

### 部分草图补全

在仅提供前50%类人草图点的补全任务中（Figure A-1），顺序感知模型比顺序无关模型F1-score高出+6.6。即使草图高度不完整，模型仍能推断出连贯的3D形状（Figure A-2）。这归因于顺序信息使模型能够利用已绘制部分的时序结构推断未绘制区域的拓扑关系，而非仅依赖空间邻近性。

### 推理效率

推理速度与质量权衡实验（Table A-2）表明，即使使用少量DDIM步骤，重建精度仍保持稳定，而推理速度显著提升（batch size=1下测试）。这为交互式VR设计场景中的实时反馈提供了可行性基础。

### 失败模式与局限性

尽管整体性能优异，模型存在以下已知失败模式：

1. **未见类别的先验偏差。** 对于训练集未覆盖的物体类别（如卡车、床、马桶），模型有时过度依赖训练集的形状先验，将卡车或床重建为桌状结构，将马桶重建为椅子状（Figure A-5）。这表明模型的泛化仍受限于ShapeNet四类别的分布。

2. **合成排序与人类习惯的差异。** 合成数据采用DFS排序作为归纳偏置，虽在多数情况下有效，但无法完全反映人类的真实绘制顺序。当真实草图的绘制顺序与训练分布差异较大时，可能需要额外微调。

3. **无吸附草图的几何退化。** 模型在训练时利用了表面吸附工具采集的高质量草图。虽然在无吸附草图上仍表现稳健（Figure A-3），但极端噪声或自由度过大的输入可能导致几何细节丢失。

4. **类别覆盖有限。** 当前数据集仅覆盖椅、桌、柜、飞机四类，对于非刚性物体或复杂场景的生成多样性仍然受限。

![[assets/figures/papers/paper_list_l2556_https_arxiv_org_abs_2512_04761/figures/006_Table_2.jpg]]
*Table 2: Quantitative results. Comparison of sketch-to-shape generation methods on the public 3DVRCHAIR dataset and our proposed VRSKETCH2SHAPE dataset. ⋆ use 2D renders of sketches*

![[assets/figures/papers/paper_list_l2556_https_arxiv_org_abs_2512_04761/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative Illustrations. Comparison between our method and Luo et al. [42] on the real test set of VRSKETCH2SHAPE. Both models are pretrained on the same synthetic sketches and fine-tuned on real data. Our approach generates shapes that are more detailed, structurally accurate, and topologically faithful to the target geometry*

## 定位与知识库关联

### 1. 与基线方法的关系

**VRSketch2Shape** 的核心贡献在于将 VR 草图生成问题从“无序点云重建”重新定义为“有序序列条件生成”，其方法谱系可沿两条轴线展开：草图表示形式与生成范式。

**相对于无序点云基线。** 此前主流的 VR 草图生成方法（如 **Luo et al.**）将草图视为无序三维点云，通过 PointNet++ 等无序聚合器提取全局特征，再输入 VAE 或扩散模型生成形状。这一范式完全丢弃了笔画顺序、点顺序以及连接关系，导致生成结果在几何精度和拓扑一致性上存在瓶颈。VRSketch2Shape 将表示形式从无序点云切换为有序笔画序列——每个笔画为有序点序列，以 SEP 分隔笔画、EoS 标记结束——并引入顺序感知的 BERT 编码器替代无序聚合。这一改变使模型能够捕捉笔画间的连接性与层次结构，在 3DVRChair 基准上 F-score 从 26.6 提升至 31.1（+4.5），CD×1000 从 35.5 降至 25.8（−9.7）；在自建 VRSketch2Shape 数据集全类别上 F-score 从 48.8 提升至 69.8（+21.0），CD×1000 从 13.0 降至 4.8（−8.2）（Table 2）。消融实验进一步证实：去除笔画和点顺序后，F-score 从 56.8 骤降至 48.9，CD×1000 从 5.1 升至 7.1（Table 4）；将草图直接表示为无序点云时，F-score 仅 30.8，CD×1000 高达 25.8（Table 4）。

**相对于 2D 渲染基线。** **LAS-Diffusion** 采用多视角 2D 草图渲染作为输入，绕过了 3D 草图的直接编码。该方案虽然可以利用成熟的 2D 视觉编码器，但多视角投影不可避免地丢失了三维空间中的精确几何关系和笔画时序信息。VRSketch2Shape 直接在原生 3D 空间中对草图点进行编码，避免了投影信息损失，在定性对比中展现出更精细的几何细节和结构准确性（Figure A-6）。

**相对于序列编码基线。** 直接将原 2D **SketchBERT** 扩展至 3D 作为序列编码器，在消融实验中精度显著下降（Table 4）。VRSketch2Shape 的编码器设计包含三个关键改进：3D 空间傅里叶特征编码（替代原始坐标，去除后 F-score 从 56.8 降至 52.1，CD×1000 从 5.1 升至 5.6）、连续傅里叶位置编码（分别编码笔画索引和点索引，去除后 F-score 降至 48.2，CD×1000 升至 6.3），以及轻量级 BERT 结构（6 层 8 头）（Table A-1 [A]）。这三个组件协同作用，使模型能够同时捕获高频几何细节和长程时序依赖。

### 2. 适用边界与有效性条件

**数据层面。** 模型的有效性依赖于合成数据大规模预训练（20,838 对）与真实数据微调的两阶段策略。消融实验表明，去除合成预训练、仅用 200 张真实椅类草图训练会导致性能大幅下降（Table 4）。少样本微调实验显示，每类别仅需约 50 张真实草图即可使 F-score 和 CD 接近全量微调水平（Figure 5），表明预训练形状先验具有强迁移能力。训练数据当前覆盖椅、桌、柜、飞机四个 ShapeNet 类别，对于更丰富的物体类别或非刚性结构，生成多样性受限。

**输入质量层面。** 模型在训练时利用了带表面吸附（surface-snapping）的高质量草图，该工具使草图点更贴近目标表面，产生更精确的几何约束。在无吸附草图上模型仍表现稳健（Figure A-3），但极端噪声或自由度过大的输入可能导致几何细节丢失。合成草图的 DFS 遍历排序策略旨在提供有效的归纳偏置，但并不能完全反映人类的真实绘制顺序；BFS 遍历替代 DFS 会导致 F-score 从 56.8 降至 47.8（Table A-1 [B]），说明排序策略对模型性能有显著影响。

**顺序敏感性。** 打乱笔画顺序导致 F-score 从 56.8 降至 54.6，打乱点顺序降至 52.2；而反转笔画顺序影响甚微（Table A-1 [C]）。这表明模型对局部点顺序更为敏感，而笔画方向则具有较强的鲁棒性——这一特性与人类绘制习惯的多样性相兼容。

**推理效率。** 模型支持 DDIM 加速采样，在较少去噪步数下重建精度保持稳定，推理速度显著提升（Table A-2），但实时交互式创作场景下的速度-质量最优权衡仍需进一步探索。

### 3. 局限与开放问题

**泛化到未见类别。** 模型在训练集未出现的类别上有时会过度依赖训练形状先验，例如将卡车或床重建为桌状结构，或将马桶重建为椅子状（Figure A-5）。这揭示了当前方法的一个根本性局限：预训练形状先验在开放域手绘场景中可能与用户意图产生冲突，模型倾向于将输入“解释”为已知类别，而非忠实于草图的几何线索。

**合成数据的真实度差距。** 合成草图生成流水线（显著点提取→贝塞尔样条拟合→笔画合并简化→DFS 排序）虽无需训练，但其产生的时序模式与真实人类绘制顺序存在系统性偏差。当前通过随机时序增强（笔画/点丢弃、笔画互换）部分缓解了这一问题，但尚未从根源上学习真实绘制行为。

**开放问题包括：**

1. **时序建模的泛化路径。** 如何将顺序感知框架推广到更广泛的物体类别，包括非刚性物体和复杂场景？能否通过学习真实人类绘制顺序（而非启发式排序）进一步提升模型对设计意图的理解？

2. **增量式交互生成。** 当前模型以完整草图为输入进行一次性生成。在交互式 VR 设计环境中，如何实现增量式的逐步形状补全与实时反馈，使用户在绘制过程中即时看到形状演化？

3. **创意探索与先验约束的平衡。** 如何将预训练的形状先验与开放式手绘意图更好地结合，既利用先验保证几何合理性，又不压制用户的创意表达？这涉及条件生成模型中引导强度的自适应调节机制。

4. **推理速度与质量的 Pareto 前沿。** 在支持流畅实时创作体验的前提下，DDIM 步数、模型容量与生成质量之间的最优权衡尚未被系统刻画。

5. **多模态时序线索融合。** 除笔画顺序外，VR 环境还可提供绘制速度、压力、视角变化等时序信号，这些额外模态能否进一步提升形状生成的精度和意图对齐度？

## 原文 PDF

![[paperPDFs/CVPR_2026/Order_Matters_3D_Shape_Generation_from_Sequential_VR_Sketches.pdf]]
