---
title: "H2OFlow: Grounding Human-Object Affordances with 3D Generative Models and Dense Diffused Flows"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/H2OFlow_Grounding_Human_Object_Affordances_with_3D_Generative_Models_and_Dense_D_cf15d75b0efb.pdf
project_link: null
code_link: null
aliases:
- H2OFlow
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 利用3D生成模型合成多样化的HOI数据，并通过点云上的密集扩散流作为中间表示，将供能性建模为由接触、方向和空间三种概率分布组成的综合表示，从而摆脱手动标注和水密网格需求。
primary_logic: 通过扩散Transformer学习物体点云到人体密集扩散流的条件分布，并从中抽取多种交互样本，基于样本统计定义接触、方向（熵）和空间（占用）三种供能性分数，形成纯点云驱动、无标注的综合供能性推理框架。
claims:
- H2OFlow在OMOMO测试集上大幅超越COMA等基线，接触相似度SIM-H提升超过30%。
- H2OFlow在真实世界点云上保持稳定性能，并在不同降噪强度下均优于COMA。
- 同时使用接触、方向、空间三种供能性的下游任务（区域检索、姿态选择）显著优于仅使用接触或任意两种的组合。
- 交叉注意力权重对供能性聚合至关重要，去除后接触和方向供能性指标明显下降。
---

# H2OFlow: Grounding Human-Object Affordances with 3D Generative Models and Dense Diffused Flows

> [!tip] 核心洞察
> 通过扩散Transformer学习物体点云到人体密集扩散流的条件分布，并从中抽取多种交互样本，基于样本统计定义接触、方向（熵）和空间（占用）三种供能性分数，形成纯点云驱动、无标注的综合供能性推理框架。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于3D生成模型与密集扩散流的H2OFlow：人-物交互供能性学习 |
| 英文题名 | H2OFlow: Grounding Human-Object Affordances with 3D Generative Models and Dense Diffused Flows |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=QhqJ1DCp1X) · [paper](https://arxiv.org/abs/2407) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | H2OFlow |
| Dataset | OMOMO, Real-world |

> [!tip] 效果简介
> - OMOMO 上，SIM-H ↑ 72.3 ± 1.3% vs COMA: 41.3 ± 2.2% (+31.0%)；SIM-O ↑ 81.0 ± 2.4% vs COMA: 56.9 ± 1.4% (+24.1%)；MAE-H ↓ 0.11 ± 0.03 vs COMA: 0.22 ± 0.07 (-0.11)。
> - Real-world (6 objects) 上，MMD (SMPL) ↓ 8.9 vs COMA: 12.8 (-3.9)；Coverage (COv@15cm) ↑ 64.5% vs COMA: 43.2% (+21.3%)。

## 概要

人-物交互（HOI）供能性学习旨在理解物体提供了哪些交互可能性——人应该接触哪里、从哪个方向接近、占用哪些空间。现有方法面临三重瓶颈：**依赖昂贵的人工标注**（如接触区域标签）、**仅建模接触而忽略方向偏好与空间占有**等非接触交互模式，以及**需要水密网格作为输入**，难以泛化至真实世界的噪声点云。

H2OFlow 的核心洞察是：**利用 3D 生成模型合成多样化的 HOI 数据，并通过点云上的密集扩散流作为中间表示，将供能性建模为由接触、方向和空间三种概率分布组成的综合表示**，从而彻底摆脱手动标注和水密网格的依赖。

具体而言，H2OFlow 使用预训练生成模型 CHOIS 根据语言提示合成大量 HOI 序列作为训练数据；在物体点云条件下，通过扩散 Transformer（DiT）学习人体点云从零姿态到目标姿态的密集位移场分布；从学到的分布中采样多个人体配置，并基于样本统计分别计算接触分数、方向熵和体素占用，形成纯点云驱动的综合供能性推理框架。

**关键结果**：在 OMOMO 测试集上，H2OFlow 的接触相似度 SIM-H 达到 72.3%，相比现有综合供能性方法 COMA（41.3%）提升超过 30 个百分点；在真实世界点云上保持稳定性能，覆盖度（COv@15cm）达到 64.5%，远超 COMA 的 43.2%。消融实验证实，交叉注意力权重对供能性聚合至关重要，且同时使用三种供能性（接触+方向+空间）在下游任务中显著优于任意子集组合。



### 人-物交互供能性学习

供能性（affordance）描述了环境为智能体提供的交互可能性，是人-物交互（HOI）理解的核心概念。在三维场景中，供能性学习的目标是从物体几何推断人类可能如何接触、操作或使用该物体。这一能力对机器人操作、增强现实和具身AI至关重要，因为它使系统能够预测“在哪里交互”以及“以何种方式交互”。

### 现有方法的瓶颈

当前HOI供能性学习方法面临三个相互关联的瓶颈，限制了其在实际场景中的适用性：

**对人工标注的依赖。** 大多数方法需要昂贵且耗时的人工标注——无论是接触标签、交互区域分割，还是完整的交互姿态记录。这种依赖使方法难以扩展到大规模、多样化的物体类别。

**对水密网格的假设。** 如COMA（Kim et al., 2024）等代表性方法要求输入为完整的水密网格及其法线信息，通过2D渲染图像进行供能性推断。然而，真实世界的感知数据通常以噪声点云形式存在，网格重建过程会引入误差并丢失几何细节。实验表明，当COMA使用从点云重建的粗糙网格（COMA-Recon）时，其性能大幅下降，暴露了网格依赖的脆弱性。

**交互模式的片面建模。** 现有方法大多仅关注接触信息——即人体哪些部位会触碰物体。然而，大量日常交互涉及非接触模式：方向偏好（如从正面而非背面抓取杯子）、空间占有（如坐椅子时臀部占据座面上方空间）等隐含约束同样关键。忽略这些维度会导致供能性推理不完整，难以支持复杂的下游任务。

### 核心洞察与动机

本文的核心洞察是：**3D生成模型的进步为摆脱上述瓶颈提供了新路径，但需要一种与之匹配的中间表示来桥接生成数据与供能性推理。**

具体而言，预训练的3D HOI生成模型（如CHOIS）能够根据语言提示合成多样化的人-物交互序列，且无需人工标注。然而，如何从这些合成数据中提取可泛化的供能性知识，而非简单记忆特定交互实例，是一个关键挑战。

H2OFlow提出以**密集扩散流**（dense diffused flow）作为中间表示：将人体配置建模为从零姿态SMPL模型到目标姿态的逐点位移场，并通过扩散Transformer学习该位移场在物体点云条件下的多模态分布。这一设计将供能性推理转化为从学到的分布中采样多样化的交互样本，再基于样本统计定义接触、方向（熵）和空间（体素占用）三种互补的供能性分数。

该框架的动机在于：点云原生、无需标注、综合建模三种交互维度，使其天然适用于真实世界的噪声感知数据，同时保留了对多样化交互模式的表达能力。



## 核心方法与创新机理

H2OFlow 的核心创新在于构建了一条**纯点云驱动、无需人工标注的综合供能性学习管线**，其关键突破可归纳为四个 changed slots。

### 1. 中间表示：密集扩散流替代显式参数回归

现有方法通常直接回归 SMPL 参数或从 2D 图像升维重建网格，但这些表示对旋转等非线性参数的学习极为困难。H2OFlow 采用**密集扩散流**（dense diffused flow）作为中间表示——定义为零姿态人体点云 $\pmb{H}_0$ 到目标交互人体点云 $\pmb{H}$ 的逐点位移场：

$$\pmb{f}_i := \pmb{h}_i - \pmb{h}_{0,i}, \quad \forall i \in \{1, \dots, N_H\}$$

通过扩散 Transformer（DiT）学习该流场的条件分布 $p(\pmb{F} \mid \pmb{o})$，模型可以采样出多样化的合理人体配置。消融实验证实，直接预测 SMPL 参数的变体 H2OSMPL 性能远低于密集流方案（Table 1），说明逐点位移比关节旋转等参数更易学习，且自然保留了多模态交互分布。

### 2. 供能性表示空间：从接触分数到接触-方向-空间三元组

现有综合供能性方法（如 **COMA**，Kim et al., 2024）依赖网格法线计算方向和空间分数，且需要水密网格输入。H2OFlow 在纯点云上定义了三种互补的供能性分布：

- **接触供能性**：基于人体-物体点对距离的期望加权指数衰减，其中权重 $w_{ij}$ 来自 DiT 交叉注意力，反映点对交互的重要性：
  $$c_{ij} = \mathbb{E}_{h_i \sim \mathcal{P}_{ij}} \left[ w_{ij} \cdot \frac{\exp(-\|d_{ij}\|)}{\tau} \right]$$

- **方向供能性**：以方向分布熵的负值衡量方向一致性——熵越低表示交互方向越确定，供能性越强：
  $$R_{ij} = \mathbb{E}_{h_i \sim \mathcal{P}_{ij}} \left[ w_{ij} \cdot \frac{\mathcal{H}_{ij}}{\tau} \right], \quad \mathcal{H}_{ij} = \mathbb{E}_{n \sim \mathbb{S}^2} \left[ \log p_{\pmb{x},ij}(n) \right]$$

- **空间供能性**：人体点落入特定空间体素的期望占用，捕捉非接触的空间占有模式：
  $$S_{ij} = \mathbb{E}_{h_i \sim \mathcal{P}_{ij}} [ \delta_{ij} ]$$

下游任务实验（Table 2）表明，同时使用三种供能性（C+O+S）的区域检索和姿态选择性能显著优于仅使用接触或任意两种组合，验证了三元组表示的互补性。

### 3. 训练数据：3D 生成模型替代人工标注

传统 HOI 供能性学习依赖人工标注的接触标签或昂贵的真实扫描数据。H2OFlow 利用预训练的 3D 生成模型（CHOIS）根据语言提示合成多样化的 HOI 网格序列，仅需对生成数据进行最远点采样和密集流真值计算即可获得训练监督。这一设计消除了对人工标注和水密网格的双重依赖，同时通过数据增强（如加入使用向交互）可显著改善坐姿等日常用品的供能性模式（Figure 9）。

### 4. 输入模态：纯点云驱动与鲁棒性

COMA 等方法需要水密网格和完整法线信息，在真实世界噪声点云上性能急剧下降——COMA-Recon（从点云重建网格再输入 COMA）的结果证实了这一点（Table 1）。H2OFlow 直接以部分观察的物体点云为条件，且对遮挡（Table 6，遮挡 50% 时 SIM-H 仍达 70.9%）和噪声（Table 7，不同降噪强度下均优于 COMA）表现出强鲁棒性，真正实现了从合成数据到真实点云的零样本泛化。

### 因果机制总结

核心因果链为：**3D 生成模型提供多样化交互先验 → 密集扩散流作为易学习的中间表示 → 扩散 Transformer 捕捉多模态分布 → 基于样本统计的三元供能性推断**。其中交叉注意力权重 $w_{ij}$ 是连接流学习与供能性聚合的关键纽带——去除该权重的消融实验（H2OFlow-NoAttn）导致接触和方向供能性指标显著下降（Table 1）。



H2OFlow 的整体框架围绕一个核心洞察展开：**利用 3D 生成模型合成多样化的人-物交互数据，通过点云上的密集扩散流作为中间表示，学习一种纯点云驱动、无需人工标注的综合供能性分布**。该框架由四个顺序衔接的模块构成，形成从数据生成到供能性推理的完整闭环。

### 模块一：合成 HOI 数据生成

H2OFlow 不依赖人工标注的接触标签或真实 HOI 扫描，而是借助预训练的 3D 生成模型 **CHOIS**，根据语言提示自动合成大量多样化的人-物交互网格序列。这些合成数据覆盖了丰富的交互姿态和物体类别，为后续学习提供了大规模、多模态的监督信号。该模块的输出是成对的物体网格与交互中的人体网格。

### 模块二：点云采样与密集流真值计算

对合成的 HOI 网格，首先应用最远点采样获得物体点云 $\pmb{o} = \{\pmb{o}_j\}_{j=1}^{N_O}$ 和人体点云 $\pmb{H} = \{\pmb{h}_i\}_{i=1}^{N_H}$。随后，以零姿态 SMPL 人体模型 $\pmb{H}_0$ 为基准，计算每点的位移向量，构成**密集流场** $\pmb{F}$ 作为训练真值：

$$\pmb{f}_i := \pmb{h}_i - \pmb{h}_{0,i}, \quad \forall i \in \{1, \dots, N_H\}$$

这一逐点位移表示捕获了从初始姿态到目标交互姿态的完整几何变化，避免了直接回归 SMPL 参数时旋转等非线性量的学习困难。

### 模块三：扩散 Transformer 训练

以物体点云为条件，训练一个**扩散 Transformer** 学习人体密集流场的条件概率分布 $p(\pmb{F} \mid \pmb{o})$。具体而言，将密集流特征与人体点特征拼接形成联合特征 $\pmb{f}^{FH}$，输入 DiT 块中先进行自注意力建模人体各点间的依赖关系，再通过交叉注意力融合物体特征 $\pmb{f}^{O}$。扩散过程的真值由干净流场 $\pmb{F}_{GT} = \pmb{H} - \pmb{H}_0$ 定义。训练完成后，给定任意物体点云，模型可通过扩散采样生成多个合理的人体目标配置。

### 模块四：供能性推断

从学到的密集扩散流分布中采样 $K$ 个人体配置样本，基于样本统计定义三类供能性分数，形成对物体交互区域的综合描述：

- **接触供能性** $c_{ij}$：定义为人体点与物体点间期望加权指数距离，利用交叉注意力权重 $w_{ij}$ 聚合多模态样本中的接触模式；
- **方向供能性** $R_{ij}$：基于位移向量与流动向量的叉积定义单位方向向量 $\pmb{x}_{ij}$，以方向分布的负熵度量方向一致性——熵越低表示方向越一致，供能性越强；
- **空间供能性** $S_{ij}$：定义为人点落在特定体素 $\pmb{g}$ 中的期望占用值，捕获非接触的空间占有模式。

三类供能性经归一化线性融合后，可灵活支持区域检索、姿态选择等下游 HOI 推理任务。整个框架的输入仅为部分观察的物体点云，对遮挡和噪声具有天然鲁棒性，无需水密网格或完整法线信息。

### 补充图表

![[assets/figures/papers/paper_list_l53_https_openreview_net_forum_id_QhqJ1DCp1X/figures/001_Figure_1.jpg]]
*Figure 1: H2OFlow learns comprehensive affordances from synthetic 3D HOI data generated by 3D generative models using a novel representation. The learned affordance captures contact, orientational, and occupancy information based on input object point clouds*



H2OFlow 的整体架构由三个紧密耦合的模块构成：合成HOI数据生成、密集扩散流学习、以及基于样本统计的供能性推断。以下按模块梳理其关键公式与变量含义。

### 模块一：合成HOI数据生成与密集流真值计算

为摆脱人工标注依赖，H2OFlow 利用预训练的3D生成模型 **CHOIS**，根据语言提示生成多样化的人-物交互网格序列。对每一对HOI网格，首先通过最远点采样（FPS）获得人体点云 $\bar{\pmb{H}} = \{ \pmb{h}_i \}_{i=1}^{N_H} \in \mathbb{R}^{N_H \times 3}$ 和物体点云 $\pmb{o} = \{ \pmb{o}_j \}_{j=1}^{N_O} \in \mathbb{R}^{N_O \times 3}$。

密集流的定义为：以零姿态SMPL人体点云 $\pmb{H}_0$ 为基准，目标人体点 $\pmb{h}_i$ 与其之间的逐点位移：

$$ \pmb{f}_i := \pmb{h}_i - \pmb{h}_{0,i}, \quad \forall i \in \{1, \dots, N_H\} \tag{1} $$

由此构建密集流场 $\pmb{F} = \{\pmb{f}_i\}_{i=1}^{N_H}$。训练时的真值密集流直接取 $\pmb{F}_{GT} = \pmb{H} - \pmb{H}_0$。

### 模块二：扩散Transformer学习密集扩散流分布

H2OFlow 采用扩散Transformer（DiT）学习条件分布 $p(\pmb{F} \mid \pmb{o})$，即以物体点云为条件，对密集流场进行去噪生成。具体地：

- 将密集流特征与人体点特征拼接形成联合特征 $\pmb{f}^{FH}$，作为DiT的输入token。
- 每个DiT块内先执行自注意力，再通过交叉注意力融合物体点特征 $\pmb{f}^O$，使人体流场感知物体几何。
- 训练时对真值流 $\pmb{F}_{GT}$ 逐步加噪，模型学习逆向去噪；推理时从纯噪声出发，条件采样得到多样化的 $\pmb{F}$，进而重建目标人体点云 $\pmb{H} = \pmb{H}_0 + \pmb{F}$。

交叉注意力权重 $w_{ij}$（人体点 $i$ 对物体点 $j$ 的注意力）在后续供能性聚合中起到关键作用：消融实验表明，去除该权重后接触和方向供能性精度均显著下降（Table 1, H2OFlow vs H2OFlow-NoAttn）。

### 模块三：供能性推断——接触、方向、空间

对给定物体点云，H2OFlow 从学到的分布中采样 $K$ 个人体配置，基于这些样本定义三种供能性分数。定义条件概率 $\mathcal{P}_{ij} := p(\pmb{h}_i \mid \pmb{o}_j)$ 为人体点 $i$ 在物体点 $j$ 条件下的分布。

**接触供能性**：以期望加权指数距离衡量人体点与物体点的接近程度，距离越近分数越高：

$$ c_{ij} = \mathbb{E}_{\pmb{h}_i \sim \mathcal{P}_{ij}} \left[ w_{ij} \cdot \frac{\exp(-\|\pmb{d}_{ij}\|)}{\tau} \right] \tag{4} $$

其中 $\pmb{d}_{ij} = \pmb{h}_i - \pmb{o}_j$ 为两点间距离向量，$\tau$ 为温度参数，$w_{ij}$ 为交叉注意力权重。

**方向供能性**：先由位移向量与流动向量的叉积定义单位方向向量：

$$ \pmb{x}_{ij} = \frac{\pmb{d}_{ij} \times \pmb{f}_i}{\lVert \pmb{d}_{ij} \times \pmb{f}_i \rVert} \tag{5} $$

方向一致性通过方向分布的负熵衡量——熵越低表示方向越集中，供能性越强：

$$ R_{ij} = \mathbb{E}_{\pmb{h}_i \sim \mathcal{P}_{ij}} \left[ w_{ij} \cdot \frac{\mathcal{H}_{ij}}{\tau} \right], \quad \mathcal{H}_{ij} = \mathbb{E}_{\pmb{n} \sim \mathbb{S}^2} \left[ \log p_{\pmb{x},ij}(\pmb{n}) \right] \tag{7, 8} $$

**空间供能性**：将物体周围空间离散为体素网格 $\pmb{G} \in \mathbb{R}^{H \times W \times L}$，以人体点落在特定体素中的期望值反映空间占用模式：

$$ S_{ij} = \mathbb{E}_{\pmb{h}_i \sim \mathcal{P}_{ij}} [ \delta_{ij} ] \tag{9} $$

其中 $\delta_{ij}$ 指示 $\pmb{h}_i$ 是否落入与 $\pmb{o}_j$ 关联的体素。

**下游任务融合**：三种供能性归一化后线性组合，用于区域检索和姿态选择：

$$ \phi_{ij} = \lambda_c \widehat{c}_{ij} + \lambda_o \widehat{R}_{ij} + \lambda_s \widehat{S}_{ij} $$

消融实验（Table 2）证实，同时使用三种供能性（C+O+S）在下游任务中显著优于仅使用接触或任意两种组合，验证了综合供能性表示的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l53_https_openreview_net_forum_id_QhqJ1DCp1X/figures/003_Figure_3.jpg]]
*Figure 3: Visual illustration of affordance inference. Given predicted human point clouds, contact affordance assigns high scores to human-object point pairs that are close. Orientational affordances give higher scores to point pairs that yield more uniform cross-product directions (i.e., hand points) and vice versa (i.e., foot points). The spatial affordances output higher scores to regions surrounding the object that are often occupied by human parts. A video of the figure is available at this website*



## 实验与关键发现

### 主实验结果：OMOMO 数据集综合供能性评估

H2OFlow 在 OMOMO 数据集上与 COMA（Kim et al., 2024）等基线进行了全面对比。核心结论如下：

**接触供能性**：H2OFlow 在 SIM-H（人体接触相似度）上达到 **72.3 ± 1.3%**，相比 COMA 的 41.3 ± 2.2% 提升超过 30 个百分点（Table 1）。物体侧接触相似度 SIM-O 为 **81.0 ± 2.4%**，较 COMA 的 56.9 ± 1.4% 提升 24.1 个百分点。MAE-H 从 COMA 的 0.22 降至 **0.11**，接触区域检索 Precision@K 从 42.9% 跃升至 **75.6%**（+32.7 个百分点）。这些结果表明，基于点云密集扩散流学习的接触供能性在精度和召回上均远超依赖水密网格和渲染图像的 COMA。

**公平性考量**：COMA 原始设计需要水密网格作为输入。为公平比较，论文引入了 COMA-Recon 基线——从点云重建粗糙网格后再输入 COMA，此时 COMA 性能大幅下降（Table 1），进一步凸显 H2OFlow 在纯点云条件下的优势。

**消融：交叉注意力权重**：去除 DiT 中的交叉注意力权重（H2OFlow-NoAttn）后，接触和方向供能性指标均出现明显下降（Table 1），验证了跨模态注意力在供能性聚合中的关键作用。

### 消融实验：三种供能性的协同效应

Table 2 展示了下游 HOI 推理任务中不同供能性组合的表现。两个下游任务分别为**区域检索**（mAP@K）和**姿态选择**（Top-5 准确率、碰撞率、接触泄漏率）。关键发现：

![[assets/figures/papers/paper_list_l53_https_openreview_net_forum_id_QhqJ1DCp1X/figures/007_Table_2.jpg]]
*Table 2: Downstream HOI inference results. Left: Region Retrieval (mAP@{1,5,10}); Right: Pose Selection (Top-5 accuracy, collision rate ↓, and contact leakage ↓)*

- 同时使用接触（C）、方向（O）、空间（S）三种供能性的组合（C+O+S）在两个任务上均显著优于仅使用接触（C）或任意两种组合。
- 这验证了论文的核心主张：**非接触交互模式（方向偏好、空间占用）携带独立于接触的信息**，三者互补构成完整的供能性表示。

### 鲁棒性分析：遮挡与噪声

**遮挡鲁棒性**（Table 6）：H2OFlow 在不同遮挡程度下表现稳定。即使物体点云被遮挡 50%，SIM-H 仍保持在 **70.9%** 的高水平，说明扩散模型学到的密集流分布对部分观测具有较强泛化能力。

**真实世界点云与噪声鲁棒性**（Table 7）：在 6 个真实物体（显示器、垃圾桶、背包、椅子、瑜伽球、桌子等）的扫描点云上，H2OFlow 的 SMPL 距离指标 MMD 为 **8.9**，显著低于 COMA 的 12.8；覆盖度 Coverage@15cm 为 **64.5%**，远超 COMA 的 43.2%。在不同降噪强度（Light / Medium / Aggressive）下，H2OFlow 均保持对 COMA 的明显优势，证明其在实际噪声条件下的实用性。

### 表示选择的消融：密集流 vs. SMPL 参数

H2OSMPL 变体直接预测 SMPL 参数而非密集扩散流，其性能远低于 H2OFlow（Table 1, Appendix L）。原因在于旋转等参数的非欧几里得性质增加了学习难度，而密集流作为欧氏空间中的逐点位移，更易于扩散模型建模。这从实验上支持了密集流作为中间表示的设计选择。

![[assets/figures/papers/paper_list_l53_https_openreview_net_forum_id_QhqJ1DCp1X/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons with various baselines on OMOMO dataset. Note that -H and -O represent human and object contact results*

### 数据增强的影响

Figure 9 展示了在合成数据中加入**使用向交互**（如坐姿、倚靠）前后的供能性变化。增强前，模型主要捕获抓取和移动模式；增强后，供能性分布呈现更对称、更有意义的交互模式（如臀部-椅面接触），证明了数据多样性对供能性覆盖的关键作用。这也揭示了当前瓶颈：底层生成模型 CHOIS 的交互类型偏向抓取，缺乏日常使用行为，数据增强可部分缓解但受限于现有 HOI 基础模型的能力边界。

![[assets/figures/papers/paper_list_l53_https_openreview_net_forum_id_QhqJ1DCp1X/figures/018_Figure_9.jpg]]
*Figure 9: Comparison of the three affordance representations before and after dataset augmentation with usage data. After augmentation, we observe more symmetry and meaningful interaction patterns that reflect actual object usage (e.g., hip-on-seat)*

### 失败模式与局限

1. **交互类型覆盖不足**：CHOIS 生成的对象种类有限，对小型、关节物体的细粒度交互（如开关抽屉、拧瓶盖）支持不足，导致此类场景下供能性预测可能不准确。
2. **跨实体迁移未经验证**：论文展示了将供能性优化框架应用于机器人实体的理论可行性，但未在实际机器人上进行部署验证，且需要构建人类-机器人点对应关系，这仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l53_https_openreview_net_forum_id_QhqJ1DCp1X/figures/006_Figure_5.jpg]]
*Figure 5: (a) Ablations on cross-attention weights and (b) results on real-world point clouds. Objects shown are: monitor, trashcan, backpack handle & panel, chair, yoga ball, table, box, and suitcase*

![[assets/figures/papers/paper_list_l53_https_openreview_net_forum_id_QhqJ1DCp1X/figures/010_Figure_7.jpg]]
*Figure 7: Comparison with COMA on real point clouds*

![[assets/figures/papers/paper_list_l53_https_openreview_net_forum_id_QhqJ1DCp1X/figures/015_Table_6.jpg]]
*Table 6: Performance under different occlusion levels*

![[assets/figures/papers/paper_list_l53_https_openreview_net_forum_id_QhqJ1DCp1X/figures/016_Table_7.jpg]]
*Table 7: Quantitative comparison of SMPL-based distances between real-world predictions and CHOIS reference poses. Lower MMD/FPD and higher Coverage indicate better alignment with synthetic interaction distributions. “Light/Medium/Aggressive” correspond to the presets in Section O.2*



## 定位与知识库关联

### 与现有工作的关系

H2OFlow 处于 **3D 人-物交互供能性学习** 与 **扩散生成模型** 的交汇点。其核心贡献在于用纯点云驱动的密集扩散流替代了传统供能性方法对水密网格、2D 渲染或多视角重建的依赖。

**与综合供能性方法的对比**：最直接的基线是 **COMA**（Kim et al., 2024），该方法同样定义了接触、方向和空间三种供能性，但其计算依赖于从 2D 图像升维得到的网格法线信息。H2OFlow 在 OMOMO 测试集上将接触相似度 SIM-H 从 41.3% 提升至 72.3%（+31.0%），SIM-O 从 56.9% 提升至 81.0%（+24.1%），精度提升超过 30 个百分点（Table 1）。为公平比较，作者还构建了 COMA-Recon 变体——从点云重建粗糙网格后输入 COMA，但该条件下 COMA 性能大幅下降，进一步验证了点云原生方法的优势。

**与 HOI 生成模型的关系**：H2OFlow 的训练数据完全来自预训练 3D 生成模型 **CHOIS** 的合成输出，仅需语言提示即可生成多样化交互序列，无需人工标注接触标签。这使其区别于依赖 BEHAVE、GRAB 等人工标注数据集的传统方法。然而，这也将 H2OFlow 的交互多样性上限绑定于底层生成模型的能力——CHOIS 偏向抓取和移动交互，缺乏坐、靠、放置等日常使用行为（Figure 9 显示通过数据增强可部分缓解）。

**与直接回归方法的对比**：H2OFlow 选择密集扩散流而非直接预测 SMPL 参数作为中间表示。消融实验中 **H2OSMPL**（直接预测 SMPL 参数的变体）性能远低于密集扩散流方案，因为旋转等参数的分布更难学习（Table 1），验证了中间表示选择的关键性。

**与点云扩散模型的关系**：H2OFlow 的 DiT 架构在点云条件生成领域与 3D 扩散策略（3D Diffusion Policy）等方法共享技术基因，但其独特之处在于将扩散过程用于人体密集流动的分布建模，而非直接生成人体点云或姿态参数。

### 适用边界

1. **物体类别受限**：底层生成模型 CHOIS 的对象种类不够广泛，缺乏对小型、关节物体的细粒度交互（如开关抽屉、拧瓶盖等）。当前方法在处理这些交互类型时供能性推断质量需要人工验证。
2. **交互模式偏向**：生成的交互偏向抓取和移动，缺少日常使用行为。数据增强（加入使用向交互）可显著改善坐姿等模式的供能性（Figure 9），但受限于现有 HOI 基础模型的能力边界。
3. **点云质量依赖**：虽然 H2OFlow 对遮挡（遮挡 50% 仍保持 70.9% SIM-H，Table 6）和噪声鲁棒，但在极端稀疏或严重缺失的点云输入下性能衰减仍需进一步量化。
4. **尚未验证实体机器人**：文中展示了跨实体（机器人）的优化框架，但未在实际机器人上验证，且需要构建人类-机器人点对应关系。

### 局限与开放问题

**已识别的局限**：
- 底层 3D 生成模型（CHOIS）的交互多样性不足，限制了供能性覆盖范围
- 尚未扩展到实体机器人验证
- 交叉注意力权重对供能性聚合至关重要，去除后接触和方向供能性指标明显下降（Table 1, H2OFlow vs H2OFlow-NoAttn），表明模型对注意力机制存在较强依赖

**开放问题**：
1. 如何利用更丰富的交互生成模型（如 InteractAnything、HOI-PAGE 等）进一步提升对日常使用供能性的覆盖，并保持点云训练流程不变？
2. 如何在物理机器人上实现实时供能性引导的策略学习？
3. 如何建立通用的人类-机器人对应关系，使供能性信息无缝迁移？
4. 是否可以通过语言条件化（如“坐在椅子上”）显式控制供能性采样，实现更灵活的交互推理？
5. 密集扩散流的多模态采样能力是否可用于交互安全性评估（如生成并过滤高风险姿态）？



## 原文 PDF

![[paperPDFs/ICLR_2026/H2OFlow_Grounding_Human_Object_Affordances_with_3D_Generative_Models_and_Dense_D_cf15d75b0efb.pdf]]
