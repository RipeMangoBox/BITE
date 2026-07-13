---
title: "VLM-Loc: Localization in Point Cloud Maps via Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VLM_Loc_Localization_in_Point_Cloud_Maps_via_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- VL
- VLM-Loc
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用大型视觉‑语言模型（VLM）的固有空间推理能力，通过BEV图像与场景图弥合模态鸿沟，并引入部分节点分配（PNA）机制显式引导文本‑节点对齐，从而大幅度提升定位准确性。
primary_logic: 将3D点云转换为BEV图像和场景图，使VLM能够同时利用密集几何线索和高层语义关系；PNA机制进一步实现了可解释的文本‑空间节点匹配，驱动精准的位置自回归预测。
claims:
- VLM‑Loc在CityLoc‑K测试集上Recall@5m达到35.91%，相比最强基线CMMLoc提升14.20个百分点，验证了所提方法的有效性。
- PNA机制在场景图基础上将Recall@5m在验证集提高6.94%、测试集提高7.72%，证明显式节点级对齐对坐标预测至关重要。
- 部分节点分配策略相比全部分配在Recall@5m上分别提升18.00%（Val）和18.10%（Test），说明只关注可见对象能有效增强定位鲁棒性。
- CityLoc-K Val 上 Recall@5m = 36.23
---

# VLM-Loc: Localization in Point Cloud Maps via Vision-Language Models

> [!tip] 核心洞察
> 将3D点云转换为BEV图像和场景图，使VLM能够同时利用密集几何线索和高层语义关系；PNA机制进一步实现了可解释的文本‑空间节点匹配，驱动精准的位置自回归预测。

| 字段 | 内容 |
|------|------|
| 中文题名 | VLM-Loc：基于视觉‑语言模型的点云地图定位 |
| 英文题名 | VLM-Loc: Localization in Point Cloud Maps via Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.09826) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | VLM-Loc |
| Dataset | CityLoc-K Val, CityLoc-K Test, CityLoc-C |

> [!tip] 效果简介
> - CityLoc-K Val 上，Recall@5m 36.23 vs 20.77 (CMMLoc) (+15.46)；Recall@10m 63.66 vs 48.65 (CMMLoc) (+15.01)。
> - CityLoc-K Test 上，Recall@5m 35.91 vs 21.71 (CMMLoc) (+14.20)；Recall@10m 63.81 vs 46.67 (CMMLoc) (+17.14)。
> - CityLoc-C (cross‑domain) 上，Recall@5m 21.37 vs ≈? (CMMLoc) (显著优于所有基线)。

## 概要

**问题瓶颈** 现有文本到点云（T2P）定位方法普遍依赖浅层文本‑点云特征匹配，缺乏有效的空间推理能力，在复杂大规模城市场景中难以建立鲁棒的语义‑几何对应，导致定位精度受限。

**核心思路** VLM‑Loc 将大型视觉‑语言模型（VLM）的固有空间推理能力引入 T2P 定位任务。方法将 3D 点云地图转换为 BEV 图像与场景图两种互补表示，弥合 3D 点云与 2D VLM 之间的模态鸿沟；同时设计**部分节点分配（PNA）**机制，显式地将文本查询中的对象提示与场景图节点对齐，驱动 VLM 以自回归方式生成可解释的节点匹配与 2D 像素坐标，再转换至世界坐标系下的定位结果。

**方法定位** VLM‑Loc 区别于端到端回归或检索‑回归范式的传统 T2P 方法（如 **Text2Loc** Xia et al., CVPR 2024、**CMMLoc** Xu et al., CVPR 2025），其关键创新在于：以 BEV 图像 + 场景图作为 VLM 的多模态输入，利用 PNA 实现文本‑空间节点的显式对齐，并通过自回归序列生成完成定位推理，使整个过程具备可解释性。

**主要结果** 在 CityLoc‑K 测试集上，VLM‑Loc 的 Recall@5m 达 35.91%，相比最强基线 CMMLoc 提升 14.20 个百分点；Recall@10m 达 63.81%，提升 17.14 个百分点。消融实验证实，PNA 机制的引入使 Recall@5m 提高 7.72%（测试集），而部分分配策略相比全部分配提升 18.10%，验证了显式节点对齐与仅关注可见对象的有效性。跨域泛化测试（CityLoc‑C）上，VLM‑Loc 同样显著优于所有基线，但绝对精度仍有限（Recall@5m ≈ 21.37%），提示跨传感器模态与城市场景的迁移鲁棒性有待进一步提升。



**任务定义与核心矛盾**。文本到点云定位（Text-to-Point Cloud Localization, T2P）要求系统根据自然语言空间描述，在给定3D点云地图中估计目标位置的2D坐标 $\xi = (x, y) \in \mathbb{R}^2$。该任务的核心矛盾在于：文本描述天然是稀疏、语义化且以自我为中心的，而点云地图则是密集、几何化且以世界为中心的——如何弥合这两种模态之间的巨大鸿沟，是T2P定位的根本挑战。

**现有方法的瓶颈**。当前T2P定位方法普遍缺乏有效的空间推理能力。以 **Text2Loc**（Xia et al., CVPR 2024）为代表的典型方案，采用Transformer交叉注意力在隐空间中对齐文本与点云特征，本质上依赖于浅层的文本-点云特征匹配。这种隐式对齐策略在面对复杂的大规模城市场景时暴露出两个结构性缺陷：（1）缺乏对物体间空间关系（如“在红色汽车东侧”）的显式建模，导致模型难以执行多步空间推理；（2）文本描述中可能包含在当前局部地图中不可见的物体，强制匹配这些不可见对象会引入噪声，严重损害定位精度。后续方法如 **MNCL**（多级对比学习）和 **CMMLoc**（Xu et al., CVPR 2025，基于柯西混合模型与方向提示）虽在特征学习层面有所改进，但均未从根本上突破“隐式对齐、缺乏显式空间推理”的范式瓶颈。在CityLoc-K基准上，最强基线CMMLoc的Recall@5m仅为20.77%（验证集），表明现有方法的定位能力远未达到实用水平。

**动机：从隐式匹配到显式空间推理**。人类在根据语言描述进行空间定位时，会自然地将文本中的物体提及与环境中可辨识的地标进行显式对应，并利用物体间的方向、距离关系进行推理（Figure 1a）。受此启发，本文提出核心动机：**将大型视觉-语言模型（VLM）固有的空间推理能力引入T2P定位任务**。然而，直接应用VLM面临两个关键障碍：（1）3D点云与VLM常用的2D视觉输入之间存在模态鸿沟；（2）VLM缺乏将文本中的物体提及与3D场景中的具体空间节点进行显式绑定的机制。VLM-Loc正是围绕这两个障碍展开设计：通过将点云地图转换为BEV图像与场景图来弥合模态鸿沟，并通过部分节点分配（PNA）机制实现可解释的文本-空间节点对齐，从而驱动精准的自回归位置预测。



## 核心方法与创新机理

VLM‑Loc 的核心创新在于将**大型视觉‑语言模型（VLM）的固有空间推理能力**引入文本到点云（T2P）定位任务，通过三个关键设计（changed slots）系统性地解决了现有方法“缺乏有效空间推理”的根本瓶颈。

### 地图表示：从原始点云到 BEV 图像与场景图

现有 T2P 方法（如 **Text2Loc**，Xia et al., CVPR 2024）直接处理原始点云或稀疏体素特征，难以被 VLM 直接消费。VLM‑Loc 将 3D 点云地图转换为两种互补的 2D 表示（Sec. 4.1，Figure 2）：

- **BEV 图像**：将点云投影至地面平面并栅格化为 $224 \times 224$ 的 RGB 图像，覆盖 $50\text{m} \times 50\text{m}$ 空间范围，提供密集的 2D 几何布局。每个物体的颜色由其点云的平均 RGB 值确定（$\bar{\mathbf{c}}_i = \frac{1}{N_i} \sum_{j=1}^{N_i} \mathbf{c}_{ij}$）。
- **场景图**：构建结构化语义图，其中每个节点编码物体索引、语义标签和像素质心坐标 $(u_i, v_i)$，节点之间隐含空间拓扑关系。

这一双表示设计使 VLM 能够同时利用**密集几何线索**（BEV 图像）和**高层语义关系**（场景图），弥合了 3D 点云与 2D VLM 之间的模态鸿沟。

### 文本‑地图对齐：部分节点分配（PNA）

现有方法依赖隐式对比学习或 Transformer 交叉注意力进行文本‑点云特征匹配（如 Text2Loc），缺乏显式的、可解释的对应关系。VLM‑Loc 提出**部分节点分配（Partial Node Assignment, PNA）**机制（Sec. 4.2，Figure 3），其核心逻辑是：

- 通过比较文本描述物体在局部地图中的可见性，仅将**实际可见的对象**显式指派给场景图中的对应节点；
- 使用距离阈值 $\tau$ 判断物体是否在查询视图内可被匹配，从而规避不可见对象引入的错误匹配。

消融实验（Table 2）提供了决定性证据：部分分配相比全部分配策略，在验证集上 Recall@5m 从 18.23% 提升至 36.23%（**+18.00 个百分点**），测试集上提升 18.10 个百分点。这表明，**只关注可见对象的显式节点级对齐**是提升定位鲁棒性的关键机制。

### 定位推理方式：VLM 自回归生成

传统方法采用端到端回归（直接输出 2D 坐标）或检索+回归范式（如 **Text2Pos**、**CMMLoc**，Xu et al., CVPR 2025）。VLM‑Loc 将定位重新定义为**基于 VLM 的自回归序列生成任务**（Sec. 4.3，Figure 2）：

- VLM 接收 BEV 图像、场景图和文本查询，自回归地生成 JSON 格式的节点匹配结果与像素坐标；
- 预测的像素位置随后转换至世界坐标系下的 2D 位置；
- 训练目标为标准交叉熵损失 $\mathcal{L} = -\sum_{t=1}^{T} \log P(y_t \mid y_{<t}, s, \mathcal{T}, I, \mathcal{G})$，最大化生成正确文本‑节点对齐和位置预测的概率（Sec. 4.4）。

这种范式转变使定位过程具备了**可解释性**——模型不仅输出坐标，还显式输出了文本对象与空间节点的对应关系。Figure 4 进一步验证了正确分配的节点数量与定位误差之间的强负相关性：当正确分配 $\geq 4$ 个节点时，中位误差显著减小，证明 PNA 驱动的节点匹配是精准定位的直接因果机制。

### 创新点的协同效应

三个 changed slots 之间存在因果依赖关系：BEV 图像与场景图的双表示提供了 VLM 可消费的输入形式；PNA 在此基础上实现了显式的文本‑空间节点对齐；自回归生成范式则将对齐结果转化为可解释的坐标预测。组件消融（Table 1）证实了这一协同效应——全组件（BEV+SG+PNA）在 CityLoc‑K 验证集上 Recall@5m 达 36.23%，相比仅使用 BEV 的 13.04% 提升 **23.19 个百分点**，相比 BEV+SG 的 29.29% 提升 **6.94 个百分点**，验证了每个创新 slot 的独立贡献与组合增益。



VLM‑Loc 的整体定位流程围绕一个核心洞察展开：将 3D 点云地图转换为 VLM 能够自然理解的 2D 表示，并通过显式的文本‑空间节点对齐机制，驱动自回归坐标预测。该框架由数据生成和训练/推理两个阶段构成，如图 Figure 2 所示。

![[assets/figures/papers/paper_list_l2430_https_arxiv_org_abs_2603_09826/figures/002_Figure_2.jpg]]
*Figure 2: Overview of VLM-Loc. In the data generation stage, the point cloud map is converted into a BEV image and a scene graph, where each node encodes semantic and spatial information. During training, the BEV image is used as the visual input, and the text input includes the scene graph, system prompt, and text query. These inputs are fed into a VLM for fine-tuning, enabling it to perform partial node assignment and position estimation in an autoregressive manner*

### 数据生成阶段：从点云到 BEV 图像与场景图

给定一个点云地图，系统首先将其投影至地面平面并栅格化为一张 BEV 图像 $I \in \mathbb{R}^{H \times W \times 3}$，其中 $H = W = 224$，覆盖 $50\text{m} \times 50\text{m}$ 的空间范围。BEV 图像中的每个像素编码了对应位置的点云语义类别与颜色信息，为 VLM 提供了密集的 2D 几何布局（Sec. 4.1）。

与此同时，系统从点云中提取语义实例，构建场景图 $\mathcal{G}$。场景图中的每个节点 $n_i = (i, l_i, \mathbf{u}_i)$ 编码了对象索引 $i$、语义标签 $l_i$ 和像素质心坐标 $\mathbf{u}_i = (u_i, v_i)$，节点之间隐式地保留了空间拓扑关系。这种结构化的语义表示弥补了纯 BEV 图像在高层关系推理上的不足（Sec. 4.1）。

### 训练与推理阶段：PNA 引导的自回归定位

在训练和推理阶段，VLM‑Loc 接收三类输入：BEV 图像 $I$ 作为视觉模态、场景图 $\mathcal{G}$ 和文本查询 $\mathcal{T}$（包含 $N_t = 6$ 条语义、颜色和方向提示）作为文本模态。这些输入被送入一个大型视觉‑语言模型进行微调。

框架的关键创新在于**部分节点分配（Partial Node Assignment, PNA）** 模块。PNA 通过距离阈值 $\tau$ 判断文本查询中描述的每个对象是否在当前局部地图中可见：若对象在查询视图中的中心与在局部地图中的中心距离小于 $\tau$，则该对象被认为是“可接地”的，并被显式指派给场景图中对应的节点；否则被标记为不可见（Figure 3, Sec. 4.2）。这一机制迫使 VLM 只关注那些确实存在于局部视野中的对象，从而规避了强制全部分配带来的错误匹配。

在获得文本‑节点对应关系后，VLM 以自回归方式生成 JSON 格式的输出，依次预测每个文本提示对应的场景图节点索引以及目标位置的像素坐标。生成的像素坐标最终通过坐标转换模块映射回世界坐标系下的 2D 位置 $\xi = (x, y)$（Sec. 4.3）。整个模型通过标准的交叉熵损失进行端到端优化：

$$\mathcal{L} = -\sum_{t=1}^{T} \log P(y_t \mid y_{<t}, s, \mathcal{T}, I, \mathcal{G})$$

其中 $y_t$ 为第 $t$ 个输出 token，$s$ 为系统提示词，$T$ 为序列总长度（Eq. (2), Sec. 4.4）。

### 模块关系与数据流总结

各模块之间的数据依赖关系可概括为：**BEV 图像渲染模块**和**场景图生成模块**并行地将原始点云转换为 VLM 可消费的表示；**PNA 模块**在训练和推理时接收文本查询与场景图，产生显式的节点对齐信号；**VLM 推理与解码模块**以 BEV 图像、场景图和文本查询为联合输入，自回归地输出节点分配与像素坐标；最后由**坐标转换模块**将像素坐标还原为世界坐标。这一设计使得 VLM‑Loc 能够同时利用密集几何线索（BEV 图像）和高层语义关系（场景图），并通过 PNA 实现可解释的文本‑空间节点匹配，驱动精准的位置预测。

### 补充图表

![[assets/figures/papers/paper_list_l2430_https_arxiv_org_abs_2603_09826/figures/001_Figure_1.jpg]]
*Figure 1: (a) illustrates the human-like logic behind text-to-point cloud localization, where spatial descriptions are used to infer the target position. (b) and (c) show the architectures of a typical method, Text2Loc [57], and our proposed VLM-Loc, respectively*



VLM‑Loc 将文本到点云（T2P）定位重新表述为一个**视觉‑语言模型引导的空间推理与自回归生成任务**。其核心架构包含五个紧密协作的模块，共同完成从 3D 点云到 2D 世界坐标的端到端映射。

### 4.1 BEV 图像渲染模块

该模块负责将大规模 3D 点云地图转换为 VLM 可直接处理的 2D 视觉表示。具体流程为：将整个点云地图投影至地面平面，并栅格化为分辨率 $H = W = 224$ 的 BEV 图像 $I \in \mathbb{R}^{H \times W \times 3}$，对应 $50\text{m} \times 50\text{m}$ 的空间覆盖范围（Sec. 5.2）。对于点云中的每个语义对象 $o_i$，其代表颜色由该对象所有点的 RGB 均值给出：

$$
\bar{\mathbf{c}}_i = \frac{1}{N_i} \sum_{j=1}^{N_i} \mathbf{c}_{ij} \quad \text{(Eq. 1, Sec. 4.1)}
$$

其中 $N_i$ 为对象 $o_i$ 包含的点数，$\mathbf{c}_{ij}$ 为第 $j$ 个点的 RGB 值。该均值颜色用于 BEV 渲染和后续的颜色文本描述生成。

### 4.2 场景图生成模块

为弥补 BEV 图像在结构化语义表达上的不足，该模块从点云语义分割结果中构建场景图 $\mathcal{G}$。每个节点 $n_i = (i, l_i, \mathbf{u}_i)$ 编码三个维度的信息：节点索引 $i$、语义标签 $l_i$（如 “car”、“building”），以及该对象在 BEV 图像中的像素质心坐标 $\mathbf{u}_i = (u_i, v_i)$（Sec. 4.1）。场景图隐式地捕获了对象间的空间关系，为 VLM 提供了超越像素级别的结构化推理线索。

### 4.3 部分节点分配（PNA）模块

这是 VLM‑Loc 实现**显式文本‑空间对齐**的关键创新。给定文本查询中的 $N_t = 6$ 个提示词（涵盖语义、颜色、方向），PNA 通过距离阈值 $\tau$ 判断每个文本对象是否在当前局部地图中可见：若文本对象在查询视图中的中心点与场景图中对应节点的距离小于 $\tau$，则该对象被视为“可接地”（groundable），并被显式分配给相应节点；否则标记为不可见并忽略（Figure 3, Sec. 4.2）。

![[assets/figures/papers/paper_list_l2430_https_arxiv_org_abs_2603_09826/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the node assignment process. PNA determines whether a textual object is groundable by comparing the distance between points A and B with the threshold τ*

该机制的核心优势在于**只关注局部可见对象**，从而避免了对全局地图中不相关节点的错误匹配。消融实验表明，相比强制对所有文本对象进行全部分配，部分分配策略在 CityLoc‑K 验证集上将 Recall@5m 从 18.23% 提升至 36.23%（+18.00 个百分点），测试集上提升 18.10 个百分点（Table 2），证实了选择性对齐对定位鲁棒性的决定性作用。

### 4.4 VLM 推理与解码模块

该模块以 BEV 图像 $I$、场景图 $\mathcal{G}$ 和文本查询 $\mathcal{T}$ 为输入，驱动 VLM 进行自回归序列生成。解码过程首先生成节点‑文本对应关系（PNA 结果），随后预测目标位置在 BEV 图像中的像素坐标 $\xi_{\text{pixel}}$（Sec. 4.3）。训练目标为标准的交叉熵损失：

$$
\mathcal{L} = -\sum_{t=1}^{T} \log P(y_t \mid y_{<t}, s, \mathcal{T}, I, \mathcal{G}) \quad \text{(Eq. 2, Sec. 4.4)}
$$

其中 $T$ 为输出 token 序列长度，$y_t$ 为第 $t$ 个输出 token，$s$ 为系统提示词。该损失函数最大化生成正确节点分配和位置预测的联合概率。

### 4.5 坐标转换模块

VLM 输出的像素坐标 $\xi_{\text{pixel}}$ 通过预设的 BEV 空间分辨率映射关系，直接转换为世界坐标系下的 2D 位置 $\xi = (x, y) \in \mathbb{R}^2$（Sec. 4.3）。该转换是确定性的线性映射，无需额外学习参数。

### 4.6 关键设计选择与证据

组件消融实验（Table 1）系统验证了各模块的贡献：单独使用 BEV 图像时 Recall@5m 仅为 13.04%；加入场景图后提升至 29.29%；进一步引入 PNA 后达到 36.23%。这一递进式增益表明，**BEV 提供密集几何线索，场景图补充高层语义关系，PNA 实现精确的节点级对齐**，三者协同构成了 VLM‑Loc 性能突破的因果链条。此外，正确分配的节点数量与定位误差呈强负相关（Figure 4）：当正确分配 $\ge 4$ 个节点时，定位中位误差显著降低，进一步验证了 PNA 机制的可解释性和有效性。



## 实验与关键发现

### 主结果：CityLoc‑K 基准上的定位性能

VLM‑Loc 在 CityLoc‑K 基准上显著超越了所有现有 T2P 定位方法。如表 5 所示，在验证集上，VLM‑Loc 的 Recall@5m 达到 36.23%，相比最强基线 **CMMLoc**（Xu et al., CVPR 2025）的 20.77% 提升了 15.46 个百分点；Recall@10m 达到 63.66%，提升 15.01 个百分点。在测试集上，Recall@5m 为 35.91%，较 CMMLoc 的 21.71% 提升 14.20 个百分点；Recall@10m 为 63.81%，提升 17.14 个百分点。这一性能飞跃验证了 VLM‑Loc 的核心设计——通过 BEV 图像与场景图弥合 3D‑2D 模态鸿沟，并借助 VLM 的固有空间推理能力实现精准定位——的有效性。

值得注意的是，VLM‑Loc 在 Recall@5m 这一严格指标上的提升幅度（约 14‑15 个百分点）远超其他方法间的差距，表明该方法并非对现有范式的渐进式改进，而是从根本上改变了文本‑点云对齐的机制。相比之下，基于隐式特征匹配的方法（如 **Text2Loc**（Xia et al., CVPR 2024）和 **MNCL**）在复杂城市场景中难以建立可靠的文本‑空间对应关系，导致定位精度受限。

### 组件消融：BEV 图像、场景图与 PNA 的贡献

表 1 系统消融了 VLM‑Loc 的三个核心组件。仅使用 BEV 图像作为 VLM 输入时，Recall@5m 仅为 13.04%（验证集），说明单纯的 2D 投影缺乏结构化语义引导，VLM 难以从中提取精确的空间对应关系。引入场景图后，性能提升至 29.29%，证明对象级语义节点为 VLM 提供了关键的推理锚点。在此基础上进一步引入部分节点分配（PNA）机制，Recall@5m 跃升至 36.23%，相比仅用场景图提升 6.94 个百分点。这一阶梯式提升揭示了 VLM‑Loc 成功的内在逻辑：BEV 图像提供密集几何线索，场景图提供高层语义结构，而 PNA 通过显式对齐文本与节点，使 VLM 的空间推理从“猜测”变为“匹配”。

### PNA 机制消融：部分分配 vs. 全部分配

表 2 对比了部分节点分配与全部分配策略。强制将文本查询中的所有对象匹配到场景图节点（全部分配）时，Recall@5m 在验证集上仅为 18.23%，测试集上为 17.81%。PNA 通过距离阈值 $\tau$ 判断文本对象在局部地图中的可见性，仅对可见对象进行匹配，将 Recall@5m 分别提升至 36.23%（+18.00 个百分点）和 35.91%（+18.10 个百分点）。这一对比揭示了 T2P 定位中的关键瓶颈：不可见对象的错误匹配会引入严重噪声，破坏 VLM 的空间推理链条。PNA 通过“只关注可见对象”的策略，有效规避了这一陷阱。

### 文本查询组件消融

表 3 分析了文本查询中语义、颜色和方向信息的作用。移除方向提示后，Recall@5m 从 36.23% 骤降至 18.74%，表明方向关系（如“在红色汽车的东侧”）是 VLM 进行空间推理的主导线索。移除颜色信息后，性能下降至 29.17%，说明颜色作为互补的视觉线索有助于区分同类对象。仅保留语义标签时，Recall@5m 为 20.53%，与最强基线 CMMLoc 相当，进一步验证了方向信息在定位中的核心地位。

### VLM 骨干网络的影响

表 4 展示了不同 VLM 骨干网络对性能的影响。VLM‑Loc 兼容多种 VLM 架构，且性能随模型规模增加而提升：Qwen2‑VL‑2B 的 Recall@5m 为 23.15%，Qwen2‑VL‑7B 提升至 31.80%，Qwen3‑VL‑32B 达到 39.84%。这一趋势表明，更大规模的 VLM 具备更强的空间推理能力，能够更有效地利用 BEV 图像和场景图中的几何‑语义信息。然而，模型规模的增大也带来了推理速度的下降（见表 9），8B 模型的推理速度约为 0.23 FPS，对实时部署构成挑战。

### 节点分配正确性与定位误差的关系

图 4 揭示了正确分配的节点数量与定位误差之间的强负相关性。当正确分配的节点数 ≥ 4 时，定位误差的中位数和分布范围显著缩小，表明 PNA 的节点匹配质量直接决定了定位精度。这一发现从机制层面解释了 PNA 的有效性：更多的正确匹配为 VLM 提供了更丰富的空间约束，使其能够更精确地推断目标位置。

### 定性分析

图 5 展示了 VLM‑Loc 与基线方法在 CityLoc‑K 上的定性对比。在语义丰富、空间关系复杂的场景中，VLM‑Loc 的预测位置（黑色圆点）与真值（红色圆点）高度重合，定位误差通常低于 5m（绿色边框）。相比之下，基线方法的预测位置往往偏离真值较远（红色边框），尤其是在对象密集或空间描述模糊的区域。这一可视化结果直观地印证了 PNA 机制的优势：通过显式匹配文本对象与场景图节点，VLM‑Loc 能够锁定正确的空间参照物，而隐式匹配方法则容易受到干扰对象的影响。

### 跨域泛化：CityLoc‑C 结果

表 6 报告了 CityLoc‑C 上的跨域泛化性能。VLM‑Loc 的 Recall@5m 为 21.37%，显著优于所有基线方法，表明该方法在不同传感器模态（LiDAR vs. 摄影测量）和城市环境间具有一定的迁移能力。然而，绝对精度仍较低，这可能源于 LiDAR 与摄影测量点云的密度和噪声特性差异（见图 6），以及 CityLoc‑C 中语义实例分布的不同（见图 8）。这一结果表明，VLM‑Loc 的跨域鲁棒性仍有较大提升空间，引入域适应或更强的几何特征可能是未来的改进方向。

### 失败模式与局限性

综合消融和定性结果，VLM‑Loc 的主要失败模式可归纳为以下三类：

1. **不可见对象干扰**：当文本查询中的对象在局部地图中不可见时，全部分配策略会导致严重错误匹配。PNA 通过距离阈值部分缓解了这一问题，但阈值的设定依赖于点云质量和场景密度，在稀疏点云中可能失效。
2. **方向信息依赖**：方向信息是定位的主导线索，但在缺乏明确方向参照或方向描述歧义时（如对象密集排列），VLM 的空间推理可能出错。
3. **颜色信息退化**：在缺乏颜色或光照变化的场景中（如夜间或单色点云），颜色线索失效，定位精度下降。

此外，VLM‑Loc 的推理速度受限于 VLM 骨干（8B 模型约 0.23 FPS），且当前仅支持固定模板生成的文本查询，对开放性自然语言描述的处理能力尚未验证。跨域泛化实验中 CityLoc‑C 上的绝对精度较低，表明模型在不同传感器模态间的迁移鲁棒性有限。

### 补充图表

![[assets/figures/papers/paper_list_l2430_https_arxiv_org_abs_2603_09826/figures/006_Table_1.jpg]]
*Table 1: Ablation study on each component. Input: BEV = BEV image, SG = scene graph. Output: PNA = partial node assignment. Best results are in bold, and second-best results are underlined*

![[assets/figures/papers/paper_list_l2430_https_arxiv_org_abs_2603_09826/figures/005_Table_2.jpg]]
*Table 2: Ablation study on partial and full node assignment*

![[assets/figures/papers/paper_list_l2430_https_arxiv_org_abs_2603_09826/figures/007_Table_3.jpg]]
*Table 3: Ablation study on text query components*

![[assets/figures/papers/paper_list_l2430_https_arxiv_org_abs_2603_09826/figures/004_Table_4.jpg]]
*Table 4: Ablation study on the effect of different VLM backbones*

![[assets/figures/papers/paper_list_l2430_https_arxiv_org_abs_2603_09826/figures/008_Table_5.jpg]]
*Table 5: Localization results of VLM-Loc and baseline methods on CityLoc-K. Green numbers indicate improvements over baselines*

![[assets/figures/papers/paper_list_l2430_https_arxiv_org_abs_2603_09826/figures/009_Figure_4.jpg]]
*Figure 4: Relationship between localization error and the number of correctly assigned nodes on the CityLoc-K test set. More correct node assignments correspond to lower localization errors*

![[assets/figures/papers/paper_list_l2430_https_arxiv_org_abs_2603_09826/figures/011_Figure_5.jpg]]
*Figure 5: Qualitative results of VLM-Loc and baseline methods on the CityLoc-K. Each example visualizes the predicted and GT positions on colorized BEV maps rendered with semantic labels. The red circles ● and black circles ● denote the GT and predicted positions, respectively. The localization error is shown below each image, and green/red borders indicate localization error below/above 5 m*

![[assets/figures/papers/paper_list_l2430_https_arxiv_org_abs_2603_09826/figures/012_Figure_6.jpg]]
*Figure 6: Example point clouds from the CityLoc benchmark. (a) A roadside LiDAR scene from KITTI-360 [32]. (b) A photogrammetric urban block from CityRefer [42]*

![[assets/figures/papers/paper_list_l2430_https_arxiv_org_abs_2603_09826/figures/015_Table_9.jpg]]
*Table 9: Inference analysis of VLM-Loc on the CityLoc-K val set*



## 定位与知识库关联

### 1. 任务定位与技术脉络

VLM‑Loc 面向**文本到点云定位（Text‑to‑Point‑Cloud Localization, T2P）**任务：给定一段描述目标位置的自然语言查询和一片点云地图，预测目标的二维世界坐标 $\xi = (x, y) \in \mathbb{R}^2$。该任务区别于传统的视觉定位（visual grounding）之处在于：查询并非对某个物体的指代，而是对“空间位置”的复合描述，且地图侧缺乏明确的候选对象框，需要模型同时进行语义理解与空间推理。

T2P 定位的发展可划分为三个阶段：

**第一阶段：检索‑回归范式。** **Text2Pos** 作为首个 T2P 方法，在 KITTI360Pose 上建立了基准，采用粗粒度检索+细粒度回归的两阶段框架。该方法将点云分割为局部块，通过文本‑点云匹配检索候选区域，再对候选区域进行坐标回归。这一范式的问题在于检索与回归解耦，检索阶段的错误会不可逆地传播到回归阶段。

**第二阶段：端到端特征对齐。** **Text2Loc**（Xia et al., CVPR 2024）利用 Transformer 交叉注意力直接在文本特征与点云特征之间建立隐式对齐，实现端到端的坐标回归。**MNCL** 通过多级对比学习增强边界感知能力。**CMMLoc**（Xu et al., CVPR 2025）引入柯西混合模型与方向提示，成为 CityLoc‑K 上的最强基线（Val Recall@5m = 20.77%）。这些方法的共同瓶颈在于：**缺乏显式的空间推理机制**，仅依赖浅层特征匹配，难以处理大规模城市场景中复杂的空间关系（如“在红色汽车和蓝色垃圾桶之间的东南方向”）。

**第三阶段：VLM 驱动的空间推理。** VLM‑Loc 跳出“特征匹配”的思维框架，将 T2P 定位重新定义为**视觉‑语言模型的空间推理任务**。其核心创新在于三个设计选择：

1. **模态桥接**：将点云转换为 BEV 图像（$224 \times 224$，覆盖 $50\text{m} \times 50\text{m}$）和场景图，使 VLM 能同时利用密集几何线索和高层语义关系，弥合 3D 点云与 2D VLM 之间的模态鸿沟。
2. **显式节点对齐**：部分节点分配（PNA）机制通过距离阈值 $\tau$ 判断文本对象是否在局部地图内可见，为可见对象指派对应的场景图节点，产生可解释的文本‑空间对应关系。
3. **自回归位置生成**：VLM 以自回归方式生成 JSON 格式的节点匹配结果与像素坐标，再转换至世界坐标，将定位转化为序列生成问题。

### 2. 与相关领域的交叉定位

VLM‑Loc 处于三个研究方向的交汇点：

**视觉‑语言导航（VLN）与具身 AI。** VLN 任务要求智能体根据自然语言指令在环境中导航，通常依赖第一视角图像序列。VLM‑Loc 与之互补：它解决的是“地图侧的静态定位”，即给定全局地图和文本查询，直接推断目标位置，无需逐步导航。两者的结合有望催生“定位‑规划一体化”的具身代理。

**3D 视觉定位（3D Visual Grounding）。** 3D 视觉定位旨在根据文本描述在 3D 场景中定位目标物体，典型方法如 ScanRefer 和 3D‑VG。VLM‑Loc 与之关键区别在于：查询目标是“位置”而非“物体”，且地图是全局点云而非单视角 RGB‑D 扫描。这一差异使得 VLM‑Loc 必须处理更稀疏的语义线索和更大的空间范围。

**VLM 在空间推理中的应用。** 近年来，VLM 在空间推理任务（如空间 VQA、视觉定位）中展现出强大的能力。VLM‑Loc 首次将 VLM 引入点云地图定位，并通过 BEV 图像+场景图的双模态表示，使 VLM 的空间推理能力得以在 3D 地图上发挥。Table 4 的消融实验表明，性能随 VLM 规模增加而提升（Qwen3‑VL‑32B 达 39.84% Recall@5m），验证了 VLM 空间推理能力对定位性能的因果贡献。

### 3. 适用边界与失效模式

**适用场景。** VLM‑Loc 适用于：
- 点云地图覆盖的城市场景（如 KITTI‑360 的路侧 LiDAR 数据）；
- 文本查询包含明确的语义对象和空间关系（语义标签、颜色、方向）；
- 对实时性要求不高的离线定位或辅助定位场景。

**已知失效模式：**

1. **颜色依赖退化**：PNA 和定位均依赖点云的颜色信息。在缺乏颜色或光照剧烈变化的场景中，颜色提示失效，节点分配精度下降。Table 3 显示，移除颜色信息后 Recall@5m 从 36.23 降至 33.66（Val），方向信息的影响更为显著（降至 18.74）。

2. **模板化查询限制**：当前文本查询由固定模板生成，仅涉及 6 个提示词（语义、颜色、方向），未包含开放性的长篇自然语言描述。方法对复杂、嵌套空间描述的泛化能力有待验证。

3. **跨域迁移脆弱**：CityLoc‑C（摄影测量点云）上的 Recall@5m 仅 21.37%，远低于 CityLoc‑K（LiDAR 点云）的 35.91%。这一差距可能源于 LiDAR 与摄影测量点云的密度差异、语义分割质量差异以及场景布局的风格差异。

4. **推理速度瓶颈**：VLM‑Loc 的推理速度受限于 VLM 骨干（8B 模型约 0.23 FPS），难以满足实时定位需求。Table 9 提供了详细的推理效率分析。

### 4. 局限与开放问题

**方法局限：**
- 当前仅支持 2‑DoF 位置预测（地面平面坐标），尚未扩展到 6‑DoF 姿态估计；
- 场景图生成依赖预训练的语义分割模型，其误差会传播到下游定位；
- PNA 的距离阈值 $\tau$ 需要手工设定，缺乏自适应调整机制。

**开放问题：**
1. **复合空间推理**：如何将 VLM‑Loc 扩展至包含深层推理的复合空间描述（如“在红色汽车和蓝色垃圾桶之间的东南方向”），并保持可解释的节点分配？这需要场景图编码更丰富的关系类型（如“之间”“对面”）。

2. **主动定位‑规划代理**：能否构建一个主动的定位‑规划一体化代理，在导航过程中动态生成自然语言查询并与 3D 地图交互？这将使 VLM‑Loc 从静态定位工具演变为具身 AI 的核心组件。

3. **高效部署**：在更大的开源 VLM 上（如 Qwen3‑VL‑32B）提升性能的同时，如何通过蒸馏、量化或高效微调保持其在消费级 GPU 上的可部署性？

4. **跨域泛化**：CityLoc‑C 的较差泛化性能是否源于 LiDAR 与摄影测量点云的密度差异？引入域适应或更强的几何特征（如法向量、曲率）能否改进跨传感器迁移能力？



## 原文 PDF

![[paperPDFs/CVPR_2026/VLM_Loc_Localization_in_Point_Cloud_Maps_via_Vision_Language_Models.pdf]]
