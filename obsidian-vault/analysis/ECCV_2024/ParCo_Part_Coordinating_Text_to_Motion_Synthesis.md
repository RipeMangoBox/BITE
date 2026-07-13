---
title: "ParCo: Part-Coordinating Text-to-Motion Synthesis"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/ParCo_Part_Coordinating_Text_to_Motion_Synthesis.pdf
project_link: null
code_link: https://github.com/qrzou/ParCo
aliases:
- ParCo
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将全身运动分解为多个部位运动，并用多个带部位协调模块的小型 Transformer 生成各个部位，实现协调与细粒度控制。
primary_logic: 借鉴人脑分区协调原理，将不同部位视为独立子系统，通过通信协调生成整体运动，实现低计算量下的高质量细粒度合成。
claims:
- ParCo 在 HumanML3D 数据集上 R-Precision Top-1 达到 0.515，超过之前最佳方法 ReMoDiffuse (0.510)，同时 FID 为 0.109，与最佳相当。
- 消融实验表明，6 部位离散化配合 Part Coordination 模块比仅使用上/下身分区且无协调的方法在 FID 上有显著提升。
- ParCo 在计算效率方面参数更少（168.4M）、FLOPs 更低（211.7G）且推理时间更快（0.036s），优于多个基线。
- 在左右交换实验中，ParCo 的准确率达到 70%，验证了其对部位概念的理解能力。
---

# ParCo: Part-Coordinating Text-to-Motion Synthesis

> [!tip] 核心洞察
> 借鉴人脑分区协调原理，将不同部位视为独立子系统，通过通信协调生成整体运动，实现低计算量下的高质量细粒度合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | ParCo：部件协调的文本到运动合成 |
| 英文题名 | ParCo: Part-Coordinating Text-to-Motion Synthesis |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2403.18512) · [Code](https://github.com/qrzou/ParCo) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ParCo |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top-1 0.515±.003 vs 0.510±.005 (ReMoDiffuse) (+0.005)；FID 0.109±.005 vs 0.141±.005 (T2M-GPT) (-0.032)；MM-Dist 2.927±.008 vs 3.121±.009 (T2M-GPT) (-0.194)。
> - KIT-ML 上，R-Precision Top-1 0.430±.004 vs 0.416±.006 (T2M-GPT) (+0.014)；FID 0.453±.027 vs 0.514±.029 (T2M-GPT) (-0.061)。

## 概要

文本到运动合成旨在根据自然语言描述生成逼真且语义对齐的三维人体运动序列。现有方法通常将人体视为一个整体进行生成，或仅进行简单的上下半身划分。这些策略面临两个核心瓶颈：**分部位方法缺乏不同部位运动之间的协调**，导致动作僵硬、不自然；**单一生成器难以理解独立的部位概念**，造成语义不对齐——例如文本要求“左手举起”时，生成的运动可能错误地动用了右手。

针对上述问题，本文提出 **ParCo**（Part-Coordinating Text-to-Motion Synthesis），其核心思想借鉴人脑分区协调原理：将不同身体部位视为独立的子系统，通过显式的通信机制协调各子系统，从而实现低计算量下的高质量细粒度运动合成。具体而言，ParCo 将全身运动分解为六个部位（右臂、左臂、右腿、左腿、躯干和根节点），分别用六个独立的 VQ-VAE 进行离散化编码，再通过六个小型 Transformer 生成各部位运动序列。关键在于，这些 Transformer 之间插入了 **Part Coordination 模块**，在每一层生成过程中融合来自其他部位的 token 信息，实现跨部位协调。

在 HumanML3D 和 KIT-ML 两个主流基准上的实验表明，ParCo 在文本-运动语义对齐和生成质量上均达到领先水平。在 HumanML3D 上，ParCo 的 R-Precision Top-1 达到 **0.515**，超过此前最佳方法 ReMoDiffuse（0.510），同时 FID 为 **0.109**，与最优方法相当。更重要的是，ParCo 仅需 **168.4M** 参数和 **211.7G** FLOPs，推理时间仅为 **0.036 秒**，在计算效率上显著优于多个基于扩散的基线方法。消融实验进一步验证了六部位离散化和 Part Coordination 模块的必要性：移除协调模块后，FID 从 0.109 升至 0.155，证明了跨部位通信的关键作用。

在方法谱系上，ParCo 属于**自回归式离散运动生成**路线，与 T2M-GPT（Zhang et al., arXiv 2023）同源，但其创新在于将单一大模型拆解为多生成器协同架构。相比于 AttT2M（Zhong et al., ICCV 2023）通过多视角注意力隐式学习部位关系，ParCo 的 Part Coordination 模块提供了显式的跨部位通信机制；相比于 Hier（Ghosh et al., ICCV 2021）的上下半身独立生成且无通信，ParCo 在部位划分粒度和协调能力上均有本质提升。

### 文本到运动生成的现状与挑战

文本到运动生成旨在根据自然语言描述合成逼真的三维人体动作序列，在动画制作、虚拟现实和具身智能等领域具有重要应用。近年来，该领域取得了显著进展，涌现出多种技术范式，包括基于扩散的方法（如 **MDM** (Tevet et al., 2022)、**MotionDiffuse** (Zhang et al., 2022)、**ReMoDiffuse** (Zhang et al., 2023)）、基于自回归离散化的方法（如 **T2M-GPT** (Zhang et al., 2023)）以及基于 VAE 的方法（如 **TEMOS** (Petrovich et al., ECCV 2022)）。这些方法大多采用**单一生成器**处理全身运动，将整个人体运动编码为一个统一的表示。

然而，这种“全身一体”的范式存在一个根本性瓶颈：**单一生成器难以理解“部位”这一细粒度概念**。人体运动本质上是多个部位（如躯干、左右手臂、左右腿）协同作用的结果，不同部位的运动模式、幅度和时序关系差异显著。当单一生成器试图同时处理所有部位时，它往往无法精确捕捉部位间的协调关系，导致生成的动作出现语义不对齐或不协调的问题——例如，文本描述“右手举起”时，模型可能错误地移动左手，或使双腿产生不自然的抖动。

### 现有分部位方法的缺口

为缓解上述问题，一些工作尝试将人体运动分解为不同部位分别处理。**Hier** (Ghosh et al., ICCV 2021) 将身体划分为上/下身，用两个独立生成器分别合成，但**两个生成器之间缺乏信息交换**，导致上/下身运动无法协调。**AttT2M** (Zhong et al., ICCV 2023) 虽然引入了多视角注意力机制来增强部位感知，但其部位间的协调仍然依赖注意力机制的隐式学习，缺乏**显式的跨部位通信机制**。

这些方法的共同缺陷在于：**缺乏不同部位运动之间的显式协调**。当各部位生成器独立运作时，它们无法感知其他部位的状态，容易产生部位间运动不一致（例如手臂摆动与腿部步态脱节）。此外，采用过粗的划分粒度（如仅分上/下身）仍然将大量关节的运动压缩在单个生成器中，未能充分降低各生成器对细粒度部位概念的学习难度。

### 本文动机：借鉴人脑分区协调原理

受神经科学中人脑分区协调机制的启发——大脑将身体不同部位视为相对独立的子系统，并通过神经通信实现跨区域协调——本文提出 **ParCo**，一种**部件协调的文本到运动合成**方法。其核心思想是：**将全身运动分解为多个部位运动，并用多个轻量级生成器分别合成各部位，同时引入显式的部件协调模块实现跨部位通信**。这一设计使得每个生成器只需专注于学习特定部位的运动模式，而协调模块则确保各部位运动在全局层面保持一致，从而在较低计算量下实现高质量的细粒度运动合成。

## 核心方法与创新机理

ParCo 的核心创新在于将人体运动生成建模为**多个部位子系统的协调生成问题**，通过“分部位离散化 + 显式跨部位通信”两条主线，在低计算开销下实现了细粒度、高保真的文本驱动运动合成。

### 瓶颈洞察：从“整体生成”到“分区协调”

现有文本到运动方法面临两个关键瓶颈：

1. **缺乏部位间协调**：早期分部位方法（如 **Hier**, Ghosh et al., ICCV 2021）将上/下身独立生成，两个生成器之间没有任何信息交换，导致动作不协调。而单一生成器方法（如 **T2M-GPT**, Zhang et al., arXiv 2023）虽然隐式编码了部位信息，但难以显式理解和控制不同部位的运动语义。

2. **单一生成器难以理解部位概念**：用一个大型 Transformer 生成全身运动时，模型需要在内部隐式学习部位间的复杂依赖关系，这不仅增加了学习难度，也限制了细粒度语义对齐的能力。

ParCo 借鉴人脑分区协调的原理，将不同身体部位视为独立子系统，通过显式通信机制实现协调生成。

### Changed Slot 1：运动表示——从全身离散化到 6 部位独立 VQ-VAE 离散化

**Baseline 做法**：T2M-GPT 等自回归方法将全身运动序列通过一个 VQ-VAE 离散化为单一码本序列；Hier 则将运动分为上/下身两个部分分别离散化。

**ParCo 方案**：将全身运动按照人体结构先验划分为 **6 个部位**——右臂、左臂、右腿、左腿、脊柱与头骨（Backbone）、骨盆根节点（Root）（Fig. 3a, Fig. 8）。每个部位的运动由独立的 VQ-VAE 进行编码和量化，拥有各自的码本 $V^i$：

$$k_{l}^{i} = \underset{j \in \{1, \dots, J\}}{\arg \min} \left\| e_{l}^{i} - v_{j}^{i} \right\|$$

每个部位 VQ-VAE 的训练目标为：

$$\mathcal{L}^{i} = \mathcal{L}_{r}^{i} + \| sg(E^{i}) - Q^{i} \| + \beta \| E^{i} - sg(Q^{i}) \|$$

**效果差异**：消融实验（Table 6）表明，6 部位 VQ-VAE 的重建 FID（0.021）显著优于上/下身分区的重建（0.066）和全身单一 VQ-VAE（0.070），验证了细粒度离散化方案能更好地保留部位运动信息。

### Changed Slot 2：生成器架构——从单一大型 Transformer 到 6 个小型 Part-Coordinated Transformer

**Baseline 做法**：T2M-GPT 使用单个大型自回归 Transformer 生成全身运动码序列；Hier 使用两个独立的小型生成器分别生成上/下身，两者之间无通信。

**ParCo 方案**：采用 **6 个小型 Transformer** 分别生成各部位的运动码序列（Fig. 3b）。每个部位的自回归分布不仅依赖自身历史 token，还依赖其他所有部位的历史 token：

$$p ( K ^ { i } | t ) = \prod _ { h = 1 } ^ { L } p ( k _ { h } ^ { i } | k _ { 1 } ^ { i } , o _ { 1 } ^ { i } , ; . . . ; k _ { h - 1 } ^ { i } , o _ { h - 1 } ^ { i } ; t )$$

整体训练目标为最小化所有部位码序列的负对数似然：

$$\mathcal { L } = \mathbb { E } _ { M , t \sim p ( M , t ) } [ - \sum _ { i = 1 } ^ { S } \log p ( K ^ { i } | t ) ]$$

**效果差异**：在 HumanML3D 上，ParCo 的 R-Precision Top-1 达到 0.515，超过此前最佳方法 ReMoDiffuse（0.510），同时 FID 降至 0.109（Table 1）。更重要的是，ParCo 仅需 168.4M 参数和 211.7G FLOPs，推理时间 0.036s，在计算效率上全面优于多个基线（Table 4）。

### Changed Slot 3：协调机制——从无/隐式通信到显式 Part Coordination 模块

**Baseline 做法**：Hier 的两个生成器之间完全没有信息交换；AttT2M（Zhong et al., ICCV 2023）虽然通过多视角注意力隐式学习部位关系，但缺乏显式的协调机制。

**ParCo 方案**：在每个 Transformer 层中插入 **Part Coordination 模块**（Fig. 4），将部位 $i$ 的 token 与其他所有部位 $j \neq i$ 的 token 通过 MLP 和 LayerNorm 显式融合：

$$x _ { c o o r d } ^ { i } = L N ( x ^ { i } + M L P ^ { i } ( y ) ) , \quad y = \left\{ x ^ { j } \right\} , j \neq i$$

这一设计使得每个部位生成器在每一步预测时都能感知其他部位的当前状态，从而实现全局协调。

**效果差异**：消融实验（Table 3）提供了决定性证据——移除 Part Coordination 模块后（即各部位完全独立生成），FID 从 0.109 显著恶化至 0.155，充分证明了显式跨部位通信对生成质量的关键作用。此外，左右交换实验（Fig. 7）中 ParCo 达到 70% 的准确率，验证了模型对部位概念的显式理解能力。

### 方法优势的结构性来源

ParCo 的创新并非简单的模块堆砌，三个 changed slots 之间存在因果依赖关系：**细粒度部位划分**为显式协调提供了语义清晰的子系统边界；**多生成器架构**为并行协调提供了结构基础；**Part Coordination 模块**则是实现子系统间通信的关键机制。三者协同使得 ParCo 在参数量更低的前提下，实现了超越大型单一模型的语义对齐精度和运动保真度。

**待验证点**：论文未报告在更细粒度部位划分（如手指、面部）上的实验，Part Coordination 模块在大规模部位数量下的通信效率和效果仍需进一步验证。

ParCo 采用**两阶段流水线**，将文本到运动生成分解为“部位感知离散化”与“部位协调生成”两个串行步骤，如图 3 所示。

**第一阶段：部位感知运动离散化 (Part-Aware Motion Discretization)**
输入为全身运动序列，首先按人体解剖结构将其分割为六个部位运动：右臂 (R.Arm)、左臂 (L.Arm)、右腿 (R.Leg)、左腿 (L.Leg)、脊柱与头部 (Backbone)、以及骨盆根节点 (Root)。每个部位运动被送入一个独立的 VQ-VAE 进行编码与量化——编码器将部位运动映射为连续隐向量，再通过与该部位专属的码本进行最近邻查找，得到离散的码本索引序列。六个 VQ-VAE 各自独立训练，训练目标包含重建损失、码本损失与承诺损失（详见 Eq. (2)）。该阶段的核心作用是为第二阶段提供**部位概念的离散先验**，使后续生成器天然具备对部位语义的感知能力。

**第二阶段：部位协调 Transformer 生成 (Part-Coordinated Transformers)**
输入为文本描述与第一阶段产出的六组量化索引序列。六个小型 Transformer 分别负责生成对应部位的码索引序列，每个 Transformer 的预测不仅依赖于自身的历史 token，还依赖于其他所有部位的历史 token（Eq. (3)）。为实现跨部位通信，在每个 Transformer 的每一层前插入**部位协调模块 (Part Coordination Module)**：该模块以 MLP 聚合来自其他部位的 token 信息，经 LayerNorm 后与当前部位 token 融合（Eq. (5)），从而在生成过程中持续协调各部位的运动。最终，生成的六组部位码序列由第一阶段对应的 VQ-VAE 解码器分别重建为部位运动，再通过**部位运动集成 (Part Motion Integration)** 合并为完整的全身运动。

**输入输出关系总结：**
- **整体输入**：文本描述 $t$。
- **第一阶段输入**：全身运动 $M$（仅训练时）；输出：六组部位量化码序列 $K^i$。
- **第二阶段输入**：文本 $t$ 与部位码序列 $K^i$；输出：生成的六组部位码序列，经解码后集成为全身运动。
- **推理时**：文本 $t$ 直接驱动六个协调的 Transformer 自回归生成部位码序列，无需真实运动参与。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2403_18512/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline of ParCo. ParCo consists of two stages: (a) The whole-body motion is discretized into 6 part motions, and encoded into 6 quantized code index sequences by 6 VQ-VAEs (encoder and quantizer). This process provides a priori about the concept of part motions for the second stage. (b) We use the quantized index sequences and corresponding textual description to train 6 transformers for part motion generation. At the same time, these generators are coordinated by our Part Coordination module. The generated part motion codes are decoded by VQ-VAE (decoder) to reconstruct the 6 part motions, which will be integrated into the final whole-body motion*

ParCo 的整体架构由两个阶段级联构成：**部件感知的运动离散化**与**部件协调的 Transformer 生成**。其核心设计理念是将全身运动解耦为六个独立但相互通信的子系统，从而在低计算开销下实现细粒度、协调一致的运动合成。

### 部件感知的运动离散化

第一阶段将全身运动显式分割为六个部位：右臂（R.Arm）、左臂（L.Arm）、右腿（R.Leg）、左腿（L.Leg）、脊椎与头骨（Backbone）以及骨盆根节点（Root）。每个部位的运动由一个独立的 VQ-VAE 进行编码与离散化，各自维护一个可学习的码本 $V^{i}$。

对于第 $i$ 个部位，编码器输出 $e_{l}^{i}$ 后，通过最近邻查找在对应码本中选择离散索引：

$$k_{l}^{i} = \underset{j \in \{1, \dots, J\}}{\arg \min} \left\| e_{l}^{i} - v_{j}^{i} \right\|.$$

每个部位 VQ-VAE 的训练目标包含三项：重建损失、码本损失与承诺损失：

$$\mathcal{L}^{i} = \mathcal{L}_{r}^{i} + \| sg(E^{i}) - Q^{i} \| + \beta \| E^{i} - sg(Q^{i}) \|,$$

其中 $sg(\cdot)$ 为停止梯度算子，$\beta$ 为承诺损失权重。六部位离散化的重建 FID 为 0.021，显著优于上下身双分区（0.066）和全身单 VQ-VAE（0.070），验证了细粒度离散化方案在运动先验建模上的优势（Table 6）。

### 部件协调的 Transformer 生成

第二阶段采用六个小型 Transformer 分别生成各部位的运动码序列。与以往方法中生成器独立运行或仅依赖内部注意力隐式交互不同，ParCo 在每个 Transformer 层中插入了显式的 **Part Coordination 模块**，实现跨部位的信息融合。

部位 $i$ 的每个 token 预测同时依赖于自身历史 token 和所有其他部位的历史 token：

$$p ( K ^ { i } | t ) = \prod _ { h = 1 } ^ { L } p ( k _ { h } ^ { i } | k _ { 1 } ^ { i } , o _ { 1 } ^ { i } , ; ... ; k _ { h - 1 } ^ { i } , o _ { h - 1 } ^ { i } ; t ),$$

其中 $o_{h}^{i}$ 表示其他部位在时间步 $h$ 的 token。整体运动分布的优化目标为所有部位码序列的负对数似然之和：

$$\mathcal { L } = \mathbb { E } _ { M , t \sim p ( M , t ) } [ - \sum _ { i = 1 } ^ { S } \log p ( K ^ { i } | t ) ].$$

Part Coordination 模块的具体融合方式为：

$$x _ { c o o r d } ^ { i } = L N ( x ^ { i } + M L P ^ { i } ( y ) ), \quad y = \left\{ x ^ { j } \right\}, j \neq i,$$

即部位 $i$ 的 token $x^{i}$ 通过 MLP 聚合来自其他部位 $j$ 的 token，经 LayerNorm 后与自身残差连接。该模块使各部位生成器在保持独立性的同时获得全局协调信息。

### 关键设计决策

消融实验（Table 3）揭示了两个核心设计的作用链条：移除 Part Coordination 模块（即各部位完全独立生成）导致 FID 从 0.109 恶化至 0.155；将六部位离散化替换为上下身双分区且无协调时，Top-1 R-Precision 和 FID 均显著下降。这表明**细粒度部位划分**与**显式跨部位通信**是 ParCo 性能的两大支柱，二者缺一不可。

## 实验与关键发现

### 主实验结果

ParCo 在 HumanML3D 和 KIT-ML 两个主流基准上均取得了领先或极具竞争力的表现，验证了部件协调生成范式的有效性。

在 **HumanML3D** 测试集上（Table 1），ParCo 的文本-运动语义对齐能力尤为突出：R-Precision Top-1 达到 **0.515±.003**，超越了此前最佳的检索增强扩散方法 **ReMoDiffuse**（Zhang et al., arXiv 2023）的 0.510±.005，且是在不依赖真值运动长度的公平设定下取得的。当 ReMoDiffuse 移除真值长度先验、改用均匀随机采样长度输入时，其 Top-1 骤降至 0.427±.006，FID 从 0.103 恶化至 0.435，这凸显了 ParCo 作为自回归方法在实际部署中的天然优势——无需预知目标运动时长即可生成高质量结果。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2403_18512/figures/005_Table_1.jpg]]
*Table 1: Comparisons to current state-of-the-art methods on HumanML3D test set. “↑” denotes that higher is better. “ ↓” denotes that lower is better. “→” denotes that results are better if the metric is closer to the real motion. Bold and underlined indicate the best and second-best results, respectively. § reports results using ground-truth motion length. The results of ReMoDiffuse* are obtained from official checkpoints and employ uniform random sampling of motion lengths as input*

在运动质量方面，ParCo 的 FID 达到 **0.109±.005**，显著优于同属自回归范式的 **T2M-GPT**（Zhang et al., arXiv 2023）的 0.141±.005，并与基于扩散的 SOTA 方法（ReMoDiffuse 0.103±.004）处于同一水平。在多样性指标 Diversity 上，ParCo 的 9.490±.068 最接近真实运动的 9.503，表明其生成分布与真实数据分布高度吻合。MM-Dist 降至 2.927±.008，进一步佐证了语义一致性的提升。

在 **KIT-ML** 测试集上（Table 2），ParCo 同样展现出跨数据集的泛化能力：R-Precision Top-1 达到 **0.430±.004**，FID 降至 **0.453±.027**，均优于 T2M-GPT 的 0.416±.006 和 0.514±.029，且 MM-Dist 和 Diversity 指标也保持领先。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2403_18512/figures/006_Table_2.jpg]]
*Table 2: Comparisons to current state-of-the-art methods on KIT-ML test set*

定性对比（Fig. 5）进一步印证了定量结论。在诸如“a person walks forward then turns around”等需要全身协调动作的描述上，ParCo 生成的上下肢运动在时序和幅度上高度一致，而对比方法常出现下肢移动与上肢摆动脱节或动作语义缺失的问题。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2403_18512/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison with existing methods. Green indicates the motion is consistent with the text description. Red indicates the text description lacks the corresponding motion or got the wrong motion*

### 消融实验

消融实验（Table 3）系统解耦了 ParCo 两大核心设计的贡献：**身体离散化策略**与**部件协调模块**。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2403_18512/figures/009_Table_3.jpg]]
*Table 3: Ablations of body discretization and part coordination module. ∗ denotes our ParCo. Table 4: Computational complexity analysis*

| 配置 | Top-1 ↑ | FID ↓ | MM-Dist ↓ | Diversity → |
|------|---------|-------|-----------|-------------|
| 上/下身分区 + 无协调 | 0.497 | 0.155 | 3.080 | 9.320 |
| 6 部位分区 + 无协调 | 0.505 | 0.155 | 3.028 | 9.313 |
| 上/下身分区 + 有协调 | 0.507 | 0.122 | 2.984 | 9.384 |
| **6 部位分区 + 有协调 (ParCo)** | **0.515** | **0.109** | **2.927** | **9.490** |

**部件协调模块的关键作用**：当移除 Part Coordination 模块（即各部位独立生成、无跨部位通信）时，无论采用何种分区策略，FID 均显著恶化至 0.155。引入协调机制后，上/下身分区配置的 FID 降至 0.122，6 部位分区配置进一步降至 0.109。这表明显式的跨部位通信是生成协调连贯运动的核心使能器。

**细粒度离散化的增益**：在均配备协调模块的条件下，6 部位分区相比上/下身分区在 Top-1 上提升 0.008，FID 降低 0.013。更精细的部位划分使生成器能更专注地建模局部运动模式，同时协调模块确保全局一致性。VQ-VAE 重建实验（Table 6）也佐证了这一点：6 部位 VQ-VAE 的重建 FID 为 0.021，优于上/下身分区的 0.066 和全身统一 VQ-VAE 的 0.070，说明细粒度离散化保留了更丰富的运动细节。

### 计算效率分析

ParCo 在性能领先的同时实现了显著的计算效率优势（Table 4）。相比基于扩散的方法，ParCo 的参数量仅为 **168.4M**，低于 MDM（268.9M）和 ReMoDiffuse（588.7M）；FLOPs 为 **211.7G**，远低于 MDM 的 484.7G；单次推理时间仅需 **0.036s**，比 MDM（0.048s）快约 25%，比 ReMoDiffuse（0.058s）快约 38%。这得益于“多小型生成器+协调模块”的架构设计——6 个小型 Transformer 并行生成各部位运动，避免了单一大型模型的高计算开销。

### 部件概念理解验证

左右交换实验（Fig. 7）直接检验了模型对部位概念的语义理解能力。将文本中的“左”与“右”互换后（如“raise left arm”变为“raise right arm”），ParCo 的生成准确率达到 **70%**，表明其 6 部位独立生成器确实习得了明确的部位语义概念，而非简单记忆全身运动模式。但 30% 的失败率也揭示出，在高度不对称的左右动作（如单手精细操作）上，模型对空间语义的细粒度辨别仍有提升空间。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2403_18512/figures/010_Figure_7.jpg]]
*Figure 7: Qualitative result of left-right exchange experiment on our ParCo*

### 文本长度鲁棒性

按文本长度将 HumanML3D 测试集四等分后的评估（Fig. 6）显示，ParCo 在短文本子集上的 R-Precision 优势最为明显，与真实运动的差距最小。随着文本长度增加（75-100% 分位，即长描述），所有方法的性能均有所下降，ParCo 与真实运动之间仍存在一定差距。这提示当前模型在处理超过 20 个单词的复杂长描述时，对多动作序列的时序编排和语义对应能力尚需加强。

## 定位与知识库关联

### 1. 与基线方法的关系

ParCo 位于文本驱动人体运动合成（Text-to-Motion）这一快速发展的研究线上。其核心设计选择——将全身运动分解为多个部位并分别建模——与若干已有工作形成直接对话。

**分部位建模的早期尝试。** 在 ParCo 之前，**Hier**（Ghosh et al., ICCV 2021）率先将人体运动分为上半身和下半身两个独立部分，使用两个独立的生成器分别合成。然而，Hier 的两个生成器之间没有任何信息交换，导致上下半身动作缺乏协调，整体运动容易出现不自然的现象。ParCo 将这一思路从“2 部位无通信”推进到“6 部位显式协调”，从根本上解决了部位间动作不一致的瓶颈。

**单生成器的隐式部位建模。** 另一条技术路线是使用单一生成器来隐式地学习部位概念。例如，基于扩散的 **MDM**（Tevet et al., arXiv 2022）、**MotionDiffuse**（Zhang et al., arXiv 2022）以及基于自回归的 **T2M-GPT**（Zhang et al., arXiv 2023）均采用一个大型 Transformer 或扩散模型生成全身运动嵌入。ParCo 的分析指出，这种单一生成器架构难以显式理解“部位”这一概念，导致在细粒度语义对齐（如左右手臂执行不同动作）时表现受限。ParCo 的左右交换实验（Fig. 7）显示其准确率达到 70%，正是对这一缺陷的针对性验证——单一生成器难以完成此类对部位概念的显式测试。

**检索增强的 SOTA 方法。** 在 ParCo 发表时，**ReMoDiffuse**（Zhang et al., arXiv 2023）是 HumanML3D 和 KIT-ML 基准上的领先方法，其通过检索外部运动数据库来增强扩散模型的生成质量。ParCo 在 HumanML3D 的 R-Precision Top-1 上以 0.515 超越 ReMoDiffuse 的 0.510（Table 1），同时在 FID 上达到 0.109，与 ReMoDiffuse 相当。值得注意的是，ParCo 的作者指出 ReMoDiffuse 在评估时依赖真实运动长度（ground-truth motion length）作为输入，这在实际应用场景中不可行。当移除这一信息后，ReMoDiffuse 的性能大幅下降，而 ParCo 作为自回归方法天然不依赖运动长度先验，从而在公平比较中展现出更强的实用性。

**部件感知的注意力方法。** **AttT2M**（Zhong et al., ICCV 2023）通过多视角注意力机制来增强模型对身体部位的感知能力，但本质上仍使用单一生成器。ParCo 与之不同，将部位概念从“注意力层面的隐式学习”提升为“架构层面的显式解耦”，通过 6 个独立的小型 Transformer 和显式的 Part Coordination 模块来实现部位间的结构化通信。

### 2. 技术演进中的定位

从方法演进的角度，ParCo 做出了以下关键推进：

- **运动表示层面：** 将全身单一离散化（T2M-GPT）或上下身双离散化（Hier）推进到 6 部位独立 VQ-VAE 离散化。消融实验（Table 6）表明，ParCo 的 6 部位离散化方案在重建 FID 上达到 0.021，显著优于上下身分区（0.066）和全身 VQ-VAE（0.070），验证了更细粒度部位划分对运动先验学习的重要性。

- **生成架构层面：** 将单一大型生成器或两个无通信的独立生成器，替换为 6 个小型 Part-Coordinated Transformer。每个 Transformer 在每层插入 Part Coordination 模块，通过 MLP 融合来自其他部位的 token（Eq. (5)），实现低计算量下的跨部位协调。Table 4 显示，ParCo 总参数量为 168.4M、FLOPs 为 211.7G、推理时间为 0.036s，均优于多个基线方法。

- **协调机制层面：** 显式的 Part Coordination 模块是 ParCo 的核心创新。消融实验（Table 3）表明，移除该模块（即各部位独立生成）会导致 FID 从 0.109 恶化至 0.155，直接证明了跨部位通信的关键作用。

### 3. 适用边界与局限

尽管 ParCo 在主要基准上取得了领先结果，其适用边界和局限同样值得关注：

- **左右不对称动作的理解仍有提升空间。** 左右交换实验的准确率为 70%，表明模型在处理高度不对称的左右身体动作时仍存在约 30% 的错误率。这意味着当文本描述涉及复杂的左右协调（如“右手画圆、左手画方”）时，ParCo 的生成质量可能下降。

- **极长文本描述下的性能退化。** 在按文本长度划分的子集评估（Fig. 6）中，ParCo 在最长文本子集（75-100% 分位）上的 R-Precision 与真实运动之间仍存在可观察的差距。这表明当前的 6 部位协调机制在处理需要长时序、多步骤语义理解的运动描述时，可能面临上下文建模能力的瓶颈。

- **部位划分粒度的上限。** ParCo 将人体划分为 6 个部位（四肢、脊柱/头部、骨盆根节点），这一划分在 HumanML3D 和 KIT-ML 所基于的 SMPL/MMM 人体模型上被验证有效。但对于更精细的运动生成需求（如手指动作、面部表情），现有划分方案需要进一步扩展，而 Part Coordination 模块在更多部位下的通信效率和协调质量尚未得到验证。

- **评估指标的局限性。** 论文本身指出，当前的文本-运动语义对齐、保真度和多样性评估指标仍不够全面。ParCo 在现有指标上的领先优势，是否能完全反映人类感知中的运动自然度和语义准确性，仍是一个开放问题。

### 4. 开放问题与后续工作方向

ParCo 的设计思路为后续研究提供了若干可延伸的方向：

- **更细粒度的部位协调。** 将 Part Coordination 模块应用于手指、面部等更精细的部位，并扩展到高密度人体模型，是自然的技术演进方向。这需要解决部位数量增加时协调模块的计算复杂度控制问题。

- **更全面的评估体系。** 如何设计能够同时衡量文本-运动语义对齐、运动保真度和生成多样性的评估指标，是推动该领域发展的关键基础设施问题。当前依赖预训练特征提取器的评估范式（如 R-Precision、FID）在捕捉细粒度部位协调质量方面可能存在盲区。

- **与扩散模型的融合。** ParCo 采用自回归架构，而扩散模型（如 MDM、ReMoDiffuse）是另一主流范式。将 Part Coordination 的显式协调机制引入扩散模型的去噪过程中，可能结合两者的优势，在保持高质量生成的同时提升部位级控制能力。

- **长时序协调能力的增强。** 针对极长文本描述下的性能退化问题，探索更强的时序上下文建模机制（如分层协调、记忆增强的 Transformer）来提升长运动序列的语义一致性，是一个值得深入的方向。

## 原文 PDF

![[paperPDFs/ECCV_2024/ParCo_Part_Coordinating_Text_to_Motion_Synthesis.pdf]]
