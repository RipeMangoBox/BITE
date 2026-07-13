---
title: Spatial-Aware VLA Pretraining through Visual-Physical Alignment from Human Videos
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Spatial_Aware_VLA_Pretraining_through_Visual_Physical_Alignment_from_Human_Videos.pdf
project_link: "https://beingbeyond.github.io/VIPA-VLA"
code_link: null
aliases:
- VV
- SAVPTVPAFHV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过在预训练阶段利用大规模人类演示视频对视觉-物理空间进行显式对齐，赋予VLA模型3D空间感知能力，从而改善下游机器人动作接地。
primary_logic: 人类演示视频天然包含丰富的2D视觉与3D物理动作对应关系；通过提取3D视觉注释和3D动作注释，可在不依赖机器人数据的前提下为VLA模型注入空间理解先验，使其在下游任务中实现更鲁棒的视觉-动作对齐。
claims:
- 提出的空间感知VLA预训练范式通过大规模人类演示视频实现视觉-物理空间的对齐。
- VIPA-VLA双编码器架构融合语义视觉特征与3D空间特征，并通过两阶段预训练逐步注入3D空间理解。
- VIPA-VLA在LIBERO基准上单视图平均成功率达92.4%，双视图达96.8%，显著优于现有VLA模型。
- 空间感知预训练和双编码器架构均对性能有贡献，消融实验移除任一部分均导致显著下降。
---

# Spatial-Aware VLA Pretraining through Visual-Physical Alignment from Human Videos

> [!tip] 核心洞察
> 人类演示视频天然包含丰富的2D视觉与3D物理动作对应关系；通过提取3D视觉注释和3D动作注释，可在不依赖机器人数据的前提下为VLA模型注入空间理解先验，使其在下游任务中实现更鲁棒的视觉-动作对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过人类视频视觉-物理对齐实现空间感知VLA预训练 |
| 英文题名 | Spatial-Aware VLA Pretraining through Visual-Physical Alignment from Human Videos |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.13080) · [Project](https://beingbeyond.github.io/VIPA-VLA) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | VIPA-VLA |
| Dataset | LIBERO（单视图）, RoboCasa（50次演示，24任务）, 真实机器人（Put‑Three‑Obj / Wipe‑Board / Water‑Plant） |

> [!tip] 效果简介
> - LIBERO（单视图） 上，平均成功率 (%) 92.4 vs 87.0 (TriVLA), 88.6 (GR00T N1.5) (+3.8~+5.4)。
> - LIBERO（双视图） 上，平均成功率 (%) 96.8 vs 95.5 (UniVLA), 96.8 (T0.5) (持平或略优)。
> - RoboCasa（50次演示，24任务） 上，平均成功率 (%) 45.8 vs 约36.9 (To 等) (+8.9)。

## 概要

**问题瓶颈**：现有视觉-语言-动作（VLA）模型仅依赖2D视觉输入，缺乏将2D感知与3D物理动作空间有效接地的能力，导致空间推理薄弱、跨场景泛化受限。

**核心洞察**：人类演示视频天然蕴含丰富的2D视觉与3D物理动作对应关系。通过从大规模人类视频中提取3D视觉注释和3D动作注释，可在不依赖机器人数据的前提下为VLA模型注入空间理解先验，实现视觉空间与物理空间的显式对齐。

**提出方法**：本文提出**空间感知VLA预训练范式**，并实例化为**VIPA-VLA**——一种双编码器架构，融合语义视觉编码器与3D空间编码器（Cut3R），通过两阶段预训练逐步注入3D空间理解：（1）3D视觉预训练，利用Hand3D-visual数据集对齐2D语义特征与3D空间表征；（2）3D动作预训练，利用Hand3D-action数据集中的人类手部轨迹提供物理接地动作先验。预训练完成后，模型通过扩散Transformer动作头适配下游机器人操控任务。

**方法定位**：VIPA-VLA属于**基于大规模人类视频数据预训练的VLA方法**，区别于仅使用机器人数据训练的传统VLA模型（如**OpenVLA** (Kim et al., arXiv 2024)）和从零开始训练的扩散策略（如**DiT Policy** (Hou et al., arXiv 2024)）。其核心创新在于将“视觉-物理空间对齐”作为预训练目标，而非直接学习机器人动作映射。

**主要结果**：
- **LIBERO基准**：单视图平均成功率92.4%，双视图96.8%，显著优于**GR00T N1.5**（88.6%）和**SpatialVLA**（87.0%）等基线。
- **RoboCasa基准**（50次演示，24任务）：整体成功率45.8%，较基线提升约8.9个百分点。
- **真实机器人实验**：在Put-Three-Obj、Wipe-Board、Water-Plant三个任务上，子任务和整任务成功率均大幅超越InternVL3.5-2B基线（如Wipe-Board整任务成功率60% vs. 20%），且在未见环境中保持显著优势。
- **消融实验**：移除空间感知预训练导致成功率从92.4%降至91.2%，移除双编码器降至90.4%，同时移除两者降至88.7%，验证了预训练与双编码器架构各自的独立贡献。

**局限与展望**：当前方法依赖单目点云估计，在严重遮挡或低纹理场景下空间注释质量可能下降；人类手部动作与机器人执行器之间仍存在具身差距。未来可探索将范式扩展至全身人形机器人、融合大规模机器人数据，以及在互联网视频上扩展自动标注流水线。

### 视觉语言动作模型的空间接地困境

机器人操作的核心挑战在于将自然语言指令与视觉观测映射为物理世界中的可执行动作。视觉语言动作模型（VLA）的出现为这一任务提供了统一的端到端范式：给定视觉输入 $v$ 和语言指令 $l$，模型直接预测动作块 $\mathbf{a}_t = f_{\mathrm{VLA}}(v, l)$。然而，现有VLA模型普遍存在一个根本性瓶颈——它们仅使用2D视觉输入，缺乏将2D感知与3D物理动作空间有效接地的能力。这种2D-3D鸿沟导致模型在需要精确空间推理的任务上表现脆弱，泛化性严重受限。

问题的根源在于视觉与物理空间之间的不对齐。语义视觉编码器（如InternVL3.5-2B，Wang et al., arXiv 2025）擅长提取高层语义信息，但对场景的几何结构、物体间的空间关系、以及动作执行所需的3D轨迹缺乏显式建模。当模型仅从2D图像特征直接预测末端执行器的6-DoF动作时，必须隐式地推断深度、遮挡关系和物理尺度——这一过程高度依赖训练数据的覆盖度，在分布外场景下极易失效。

### 现有解决方案的局限

针对上述问题，学界已有多条探索路径：

- **通用VLA基线**（如OpenVLA，Kim et al., arXiv 2024）通过大规模机器人数据训练来覆盖更多场景，但数据采集成本高昂，且本质上仍依赖模型隐式学习空间关系。
- **空间感知VLA**（如SpatialVLA，Qu et al., arXiv 2025）尝试在模型架构中引入3D信息，但通常需要机器人平台特定的深度传感器或精心标定的多视图数据，限制了其可扩展性。
- **大模型VLA**（如GR00T N1/N1.5，Bjorck et al., arXiv 2025）借助海量预训练知识来提升泛化性，但同样未从根本上解决2D视觉与3D物理空间的对齐问题。

这些方法的共同缺陷在于：**空间理解能力是被动地从下游任务数据中习得的，而非作为显式先验注入模型**。这导致数据效率低下，且在低数据场景下空间推理能力急剧退化。

### 核心洞察：人类视频中的视觉-物理对应

本工作的关键洞察在于：**人类演示视频天然包含丰富的2D视觉与3D物理动作对应关系**。当人类执行操作任务时，手部在3D空间中的运动轨迹与相机捕捉到的2D视觉观测之间存在确定性的几何映射——通过相机投影方程 $(u, v) = \Pi \big( K [R | t] (x, y, z)^\top \big)$ 可精确描述。这意味着，如果能从大规模人类视频中自动提取3D视觉注释和3D动作注释，就可以在不依赖任何机器人数据的前提下，为VLA模型注入空间理解先验。

基于这一洞察，本文提出**空间感知VLA预训练范式**（Spatial-Aware VLA Pretraining），其核心思想是：在预训练阶段利用人类演示视频对视觉-物理空间进行显式对齐，使模型学会将2D视觉观测接地到3D物理动作空间，从而在下游机器人任务中实现更鲁棒的视觉-动作对齐。这一范式的实例化模型VIPA-VLA通过双编码器架构和两阶段预训练，系统性地弥合了2D感知与3D动作之间的鸿沟。

## 核心方法与创新机理

VIPA‑VLA 的核心创新在于**将 VLA 模型的空间感知能力从下游微调阶段前移至预训练阶段**，通过大规模人类演示视频构建显式的视觉‑物理空间对齐，从而在不消耗机器人数据的前提下为策略模型注入 3D 空间理解先验。与现有 VLA 方法相比，其关键 changed slots 体现在三个层面。

### 从 2D 语义到 3D 空间的双编码器融合

现有 VLA 模型（如 **OpenVLA** (Kim et al., arXiv 2024)、**SpatialVLA** (Qu et al., arXiv 2025)）普遍仅依赖语义视觉编码器（如 InternVL3.5）提取 2D 特征，缺乏对场景几何结构的显式建模。VIPA‑VLA 引入**双编码器架构**：在语义编码器之外，增加一个 3D 视觉编码器 **Cut3R**，用于从单目 RGB 输入中估计点云并生成空间嵌入。两者的特征通过**交叉注意力融合层**集成，并采用残差连接与可学习缩放参数 α 进行融合：

$$V_f = V_{sem} + \alpha F_{spa}$$

这一设计使模型能够同时保留高层语义理解与底层几何结构信息，为后续的视觉‑物理对齐提供表征基础。消融实验证实，移除双编码器后 LIBERO 平均成功率从 92.4% 降至 90.4%（Table 7），表明空间编码器对性能的独立贡献。

### 基于人类视频的视觉‑物理对齐预训练

传统 VLA 方法通常在机器人数据上从零训练或仅进行 VLM 初始化，缺乏对 3D 物理空间的先验知识。VIPA‑VLA 提出**两阶段空间感知预训练**，完全基于人类演示视频构建监督信号：

- **第一阶段：3D‑Visual Pretraining**。利用 Hand3D‑visual 数据集中的 3D 视觉注释（包含空间关系、物体定位、手部运动等 VQA 对），将 2D 语义特征与 3D 空间表示对齐。这一阶段仅对齐视觉特征即已带来显著收益（论文明确指出 “aligning semantic and spatial visual features alone already yields substantial gains”）。

- **第二阶段：3D‑Action Pretraining**。利用 Hand3D‑action 数据集中的人类手部 3D 轨迹，将物理空间量化为 1024 个离散运动 token，通过预测运动 token 三元组使模型学习物理接地（physically grounded）的动作先验。

两阶段预训练使模型在 3D 空间理解定量评估中显著优于未预训练的 InternVL3.5 基线：方向得分从 1.22/3 提升至 1.82/3，距离误差从 0.18m 降至 0.12m（Table 8 / Figure 8）。

### 离散运动 token 桥接人类与机器人动作空间

人类手部动作与机器人执行器之间存在具身差距（embodiment gap），直接迁移连续轨迹面临域偏移问题。VIPA‑VLA 将 1m³ 物理空间均匀量化为 1024 个离散 bin，将 3D 腕部轨迹转化为运动 token 三元组，使 LLM 能够以自回归方式预测离散动作目标。这一离散化策略部分缓解了跨具身迁移的难度，同时保留了物理空间的几何约束。Figure 9 中预测轨迹（蓝）与真实轨迹（红）的可视化对比表明，经过第二阶段预训练后，模型已能生成与人类演示高度一致的运动模式。

### 预训练与后训练的解耦设计

VIPA‑VLA 将空间感知能力的获取与具体机器人任务的策略学习解耦：预训练阶段完全使用人类视频数据，不涉及任何机器人操作；后训练阶段则在下游机器人数据上附加扩散 Transformer 动作头（DiT Action Head），通过流匹配（flow matching）生成可执行的动作块。这一设计确保了与从零训练 VLA 方法的**数据成本公平性**——预训练所引入的空间先验是纯粹的“免费午餐”，消融实验中移除预训练后性能从 92.4% 降至 91.2%（Table 7），验证了其独立贡献。

综上，VIPA‑VLA 通过**双编码器融合、视觉‑物理对齐预训练、离散运动 token 化**三个 changed slots，在不增加机器人数据成本的前提下，为 VLA 模型赋予了可泛化的 3D 空间理解能力，在 LIBERO（单视图 92.4%）、RoboCasa（45.8%）及真实机器人任务上均取得显著提升。

VIPA-VLA 的整体框架围绕一个核心命题展开：**在预训练阶段显式地对齐 2D 视觉空间与 3D 物理动作空间，从而为 VLA 模型注入空间感知能力**。该框架由三个递进阶段构成，如图 1 所示。

### 数据根基：从人类视频中提取视觉-物理对齐监督

框架的起点是**大规模人类演示视频**。与直接使用机器人数据不同，该方法利用人类视频天然蕴含的 2D 视觉与 3D 物理动作对应关系，通过自动标注流水线构建两类关键数据集：

- **Hand3D-visual**：通过融合单目点云估计（Cut3R）、物体定位与手部姿态注释，生成约 300K 条 3D 视觉 VQA 指令-回答对（Table 1）。这些数据将 2D 图像中的物体、手部与场景元素之间的空间关系转化为自然语言描述，涵盖空间关系判断、任务完成状态、手部运动与相机运动四类问题（Figure 3）。
- **Hand3D-action**：从人类手部轨迹中提取 3D 运动监督，生成约 1M 条运动-指令对（Table 2）。具体而言，将 1m³ 物理空间量化为 $K=1024$ 个离散运动 token，并将 3D 腕部轨迹转化为运动 token 三元组，为后续的动作先验学习提供监督信号。

### 第一阶段：3D 视觉预训练

该阶段的目标是**让 VLM 骨干学会将 2D 语义特征与 3D 空间表征对齐**。模型架构采用双编码器设计（Figure 4）：

1. **语义视觉编码器**（如 InternVL3.5）提取高层语义特征 $V_{sem}$；
2. **3D 视觉编码器**（Cut3R）提供显式的场景几何理解，输出空间嵌入；
3. **交叉注意力融合层**以语义特征为 Query、空间特征为 Key/Value 进行交叉注意力计算，再通过残差连接融合：
   $$V_f = V_{sem} + \alpha F_{spa}$$
   其中 $\alpha$ 为可学习的缩放参数。

在此阶段，模型使用 Hand3D-visual 数据进行训练，仅更新融合层和 3D 编码器，语义编码器和 LLM 骨干保持冻结。消融实验表明，**仅完成这一阶段的 3D 视觉对齐即可带来显著性能收益**，证明视觉特征层面的空间对齐本身已能改善下游空间理解。

### 第二阶段：3D 动作预训练

在视觉-物理对齐的基础上，该阶段进一步**注入物理动作先验**。LLM 的 token 嵌入空间被扩展，引入离散运动 token（$K=1024$ 个 bin，覆盖 1m³ 物理空间）。模型使用 Hand3D-action 数据，学习根据视觉输入预测人类手部的 3D 运动轨迹。此阶段仅更新运动 token 嵌入和 LLM 中的 LoRA 参数。

这一设计的因果逻辑是：通过让模型在预训练中学习“给定 2D 视觉观察 → 预测 3D 物理运动”的映射，模型内部形成了对视觉-动作空间对应关系的先验理解，从而在下游机器人任务中实现更鲁棒的动作接地。

### 第三阶段：机器人后训练

预训练完成后，VIPA-VLA 被适配到下游机器人操作任务。具体流程为：

1. 在 LLM 输出端附加一个**扩散 Transformer 动作头（DiT Action Head）**；
2. LLM 根据融合后的视觉-语言特征生成条件向量，该条件向量与机器人本体状态拼接后输入 DiT；
3. DiT 通过**流匹配（flow matching）**生成可执行的动作块 $\mathbf{a}_t$：
   - 训练时，在随机噪声 $\boldsymbol{\epsilon}$ 与真实动作 $\mathbf{a}_t$ 之间线性插值生成带噪轨迹 $\tilde{\mathbf{a}}_t^{(\tau)} = (1 - \tau) \boldsymbol{\epsilon} + \tau \mathbf{a}_t$；
   - 最小化 DiT 预测的流向量与真实传输方向之间的 L2 误差：
     $$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{\mathbf{a}_t, \tau, \epsilon, \boldsymbol{v}, l} \left[ \big\| \mathbf{v}_\theta - (\mathbf{a}_t - \epsilon) \big\|_2^2 \right]$$

### 关键设计决策与证据强度

| 设计决策 | 因果作用 | 证据 |
|---------|---------|------|
| 双编码器架构 | 将空间信息作为独立模态输入，避免语义特征“稀释”几何信息 | 移除双编码器后 LIBERO 成功率从 92.4 降至 90.4（Table 7） |
| 两阶段预训练 | 先对齐视觉空间，再注入动作先验，逐步建立视觉-物理映射 | 移除预训练后成功率降至 91.2；同时移除两者降至 88.7（Table 7） |
| 运动 token 离散化 | 将连续 3D 轨迹转化为离散 token，使 LLM 能以自回归方式建模物理动作 | 该设计使模型在 Hand3D-test 上的方向得分（1.82/3 vs. 1.22/3）和距离误差（0.12m vs. 0.18m）显著优于无预训练基线（Table 8） |

### 公平性说明

整个预训练过程**完全使用人类视频数据，未涉及任何机器人数据**，确保与从零开始训练的 VLA 方法在数据成本上可比。下游后训练阶段，VIPA-VLA 与基线模型采用相同的扩散动作头和训练配置，控制变量仅在于预训练阶段的有无及其质量。

VIPA-VLA 的核心架构由五个模块串联构成，其设计目标是将 2D 语义感知与 3D 空间理解显式融合，并通过离散运动 token 桥接视觉-语言推理与连续动作生成。

### 3.1 问题形式化

VLA 模型从 VLM 的基础形式化出发。VLM 将视觉输入 $v$ 和语言指令 $l$ 映射为文本输出 $y$：

$$y = f_{\mathrm{VLM}}(v, l)$$

VLA 将此扩展至动作域，从相同的视觉与语言输入预测动作块 $\mathbf{a}_t$：

$$\mathbf{a}_t = f_{\mathrm{VLA}}(v, l)$$

这一形式化揭示了核心瓶颈：$f_{\mathrm{VLA}}$ 需要将 2D 视觉观测 $v$ 接地到 3D 物理动作空间，而传统 VLA 模型缺乏显式的 3D 空间理解机制。

### 3.2 双编码器架构与融合层

VIPA-VLA 采用双编码器架构（见 Figure 4），在语义视觉编码器（Semantic Vision Encoder）基础上引入 3D 视觉编码器 **Cut3R**，分别提取语义特征 $V_{sem}$ 和空间嵌入。两者通过交叉注意力融合层（Fusion Layer）集成，该层以语义特征为 query、空间特征为 key/value 执行交叉注意力，并通过残差连接与可学习缩放参数 $\alpha$ 融合：

![[assets/figures/papers/paper_list_l2647_https_arxiv_org_abs_2512_13080/figures/006_Figure_4.jpg]]
*Figure 4: Model architecture of VIPA-VLA. A dual-encoder including a semantic vision encoder and a 3D encoder produces fused spatial–semantic features through a cross-attention fusion layer. During pre-training, the vision tokens are aligned with text and motion tokens using 3D visual and 3D action annotations. During post-training, action queries interact with fused visual–language features to produce conditions, which is combined with the robot state and processed by a flow-matching action head to predict actions for robotic manipulation*

$$V_f = V_{sem} + \alpha F_{spa}$$

其中 $F_{spa}$ 为交叉注意力输出的空间特征。这一设计的因果逻辑在于：语义编码器提供高层物体识别与场景理解，3D 编码器提供显式的场景几何信息，融合层使模型在保留语义能力的同时获得空间感知。

### 3.3 运动 token 化与离散动作空间

为将连续 3D 轨迹纳入 LLM 的 token 预测范式，VIPA-VLA 引入离散运动 token。具体而言，将 $1\mathrm{m}^3$ 的物理工作空间量化为 $K=1024$ 个 bin，并将 3D 腕部轨迹转化为运动 token 三元组。LLM 的 token 嵌入空间被扩展以容纳这组运动 token，使其能够以自回归方式预测离散化的 3D 动作序列。这一设计部分缓解了人类手部动作与机器人执行器之间的具身差距（embodiment gap）。

### 3.4 两阶段空间感知预训练

预训练分为两个阶段，分别利用 Hand3D-visual 和 Hand3D-action 数据集：

- **阶段一：3D-Visual Pretraining**。利用 3D 视觉注释构造 VQA 形式的指令-回答对（如空间关系判断、物体定位），训练模型将 2D 视觉特征与 3D 空间表示对齐。此阶段仅对齐视觉特征，不涉及动作预测。
- **阶段二：3D-Action Pretraining**。利用 3D 动作注释（人类手部轨迹）提供运动监督，训练模型预测离散运动 token。此阶段注入物理接地（physically grounded）的动作先验。

### 3.5 扩散 Transformer 动作头与流匹配

后训练阶段在预训练 VIPA-VLA 上附加扩散 Transformer（DiT）动作头。DiT 以 LLM 输出的条件向量与机器人状态为输入，通过流匹配（flow matching）生成可执行的动作块。训练时，在随机噪声 $\boldsymbol{\epsilon}$ 与真实动作 $\mathbf{a}_t$ 之间线性插值生成带噪轨迹：

$$\tilde{\mathbf{a}}_t^{(\tau)} = (1 - \tau) \boldsymbol{\epsilon} + \tau \mathbf{a}_t, \quad \tau \sim \mathcal{U}(0, 1)$$

DiT 参数化为 $\theta$，预测流向量 $\mathbf{v}_\theta$，训练目标为最小化预测流向量与真实传输方向 $\mathbf{a}_t - \boldsymbol{\epsilon}$ 之间的 L2 误差：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{\mathbf{a}_t, \tau, \epsilon, \boldsymbol{v}, l} \left[ \big\| \mathbf{v}_\theta - (\mathbf{a}_t - \epsilon) \big\|_2^2 \right]$$

### 3.6 3D 注释中的关键公式

Hand3D 数据流水线中涉及两个关键的空间对齐公式：

**相机投影**。将 3D 世界点通过相机内参 $K$ 和外参 $[R|t]$ 投影到图像平面：

$$(u, v) = \Pi \big( K [R | t] (x, y, z)^\top \big), \quad \Pi(x', y', z') = (x' / z', y' / z')$$

**尺度校准**。通过手部关节绝对深度 $j_k^z$ 与点云相对深度 $\tilde{j}_k^z$ 的中值比计算尺度因子 $s$，统一相对点云与绝对物理尺度：

$$s = \mathrm{median}_{k \in \Omega} \left( j_k^z / \tilde{j}_k^z \right)$$

**方向离散化**。将归一化方向向量 $(\hat{x}, \hat{y}, \hat{z})$ 按分量阈值 $\gamma$ 离散化为轴对齐的语言 token：

$$\mathcal{D} = \{ \mathrm{right/left\ if\ } |\hat{x}| > \gamma, \mathrm{up/down\ if\ } |\hat{y}| > \gamma, \mathrm{forward/backward\ if\ } |\hat{z}| > \gamma \}$$

---

**模块间因果链条**：双编码器提取语义与空间特征 → 交叉注意力融合层产生空间感知的视觉 token → LLM 基于融合特征进行视觉-语言-动作联合推理，预测离散运动 token → DiT 动作头以 LLM 条件向量为引导，通过流匹配生成连续动作块。两阶段预训练按“先对齐视觉空间，再注入动作先验”的顺序逐步赋予模型 3D 空间理解能力。

## 实验与关键发现

### 实验设置概述

VIPA-VLA 的评估覆盖从仿真基准到真实机器人的多层次实验。预训练阶段完全使用人类演示视频数据（Hand3D-visual 约 300K 指令-回答对，Hand3D-action 约 1M 运动-指令对），下游后训练在目标机器人任务上使用与基线相同的扩散动作头（DiT）和训练配置，确保对比公平。所有 LIBERO 结果均基于 500 次试验/任务套件，RoboCasa 基于 50 次试验/任务。

---

### LIBERO 基准主结果

Table 3 展示了 VIPA-VLA 在 LIBERO 四个任务套件（Spatial、Object、Goal、Long）上的成功率对比，实验覆盖单视图与双视图两种输入设置。

![[assets/figures/papers/paper_list_l2647_https_arxiv_org_abs_2512_13080/figures/007_Table_3.jpg]]
*Table 3: Success rates (%) on the LIBERO benchmark. Results are reported for four task suites, with each suite evaluated across 500 trials. Experiments are conducted under both single-view and two-view input settings. All results are from public reports, except for GR00T N1.5∗, which we reproduce using the released model. The results of MaIL† is from the ED-Ma version*

**单视图场景**下，VIPA-VLA 以 **92.4%** 的平均成功率显著超越所有对比方法。与通用 VLA 基线 **OpenVLA**（Kim et al., arXiv 2024）相比提升显著，较空间感知 VLA 基线 **SpatialVLA**（Qu et al., arXiv 2025）的 87.0% 高出 5.4 个百分点，较大模型 VLA 基线 **GR00T N1.5**（Bjorck et al., arXiv 2025）的 88.6% 高出 3.8 个百分点。值得注意的是，VIPA-VLA 在单视图条件下甚至超过部分双视图方法，表明空间感知预训练有效弥补了单目输入的信息缺失。

**双视图场景**下，VIPA-VLA 达到 **96.8%** 的平均成功率，与当前最优方法 **T0.5**（Pertsch et al., 2025）持平，且在 Spatial 和 Goal 套件上分别达到 97.4% 和 98.2% 的最高分。

**关键洞察**：单视图下的大幅领先（+3.8~+5.4）与双视图下的顶级表现共同说明，视觉-物理对齐预训练赋予模型的 3D 空间理解能力在输入信息受限时发挥最大边际效益，而双视图信息的补充使该优势趋于饱和。

---

### RoboCasa 仿真基准结果

Table 4 展示了在 RoboCasa 基准 24 个任务上的评估结果。VIPA-VLA 在仅使用 **50 次演示** 的低数据量设定下，整体平均成功率达到 **45.8%**，较基线方法（约 36.9%）提升 **8.9 个百分点**。在 Pick & Place（8 任务）、Doors/Drawers（6 任务）和 Others（10 任务）三个类别上均表现出稳定优势。

![[assets/figures/papers/paper_list_l2647_https_arxiv_org_abs_2512_13080/figures/008_Table_4.jpg]]
*Table 4: Success rates (%) on the RoboCasa benchmark. Models are evaluated on 24 tasks (8 for Pick & Place, 6 for Doors / Drawers, 10 for Others), with each task evaluated across 50 trials*

这一结果验证了空间感知预训练在低数据量场景下的样本效率优势：预训练阶段注入的 3D 空间先验使模型在仅需少量机器人演示时即可实现更鲁棒的视觉-动作接地。

---

### 真实机器人实验

在真实机器人平台上，VIPA-VLA 在三个操作任务上与 **InternVL3.5-2B**（Wang et al., arXiv 2025）后训练基线进行对比。

**标准环境**（Table 5）下，VIPA-VLA 在所有任务上均显著优于基线：
- Put-Three-Obj：子任务成功率 52% vs. 24%，整任务成功率 10% vs. 0%
- Wipe-Board：子任务成功率 83% vs. 56%，整任务成功率 60% vs. 20%
- Water-Plant：子任务成功率 57% vs. 40%，整任务成功率 50% vs. 20%

**未见环境**（Table 6）下，VIPA-VLA 同样保持明显优势：
- Put-Three-Obj：子任务/整任务 44%/10% vs. 20%/0%
- Wipe-Board：子任务/整任务 78%/50% vs. 50%/10%
- Water-Plant：子任务/整任务 40%/30% vs. 33%/10%

**关键结论**：VIPA-VLA 在整任务成功率上的提升尤为突出（Put-Three-Obj 从 0% 提升至 10%，Wipe-Board 从 20% 提升至 60%），说明空间感知预训练使模型在多步骤长程任务中具备更强的空间记忆和动作连贯性。

---

### 消融实验

Table 7 的消融实验系统性地量化了空间感知预训练和双编码器架构各自的贡献。在 LIBERO 单视图设定下：

![[assets/figures/papers/paper_list_l2647_https_arxiv_org_abs_2512_13080/figures/014_Table_7.jpg]]
*Table 7: Ablations (%) on the LIBERO benchmark*

| 配置 | 平均成功率 (%) |
|------|---------------|
| VIPA-VLA（完整） | **92.4** |
| – 预训练（仅后训练） | 91.2（-1.2） |
| – 双编码器（仅语义编码器） | 90.4（-2.0） |
| – 两者均移除 | 88.7（-3.7） |

**分析**：
1. **预训练的独立贡献**（+1.2）：即使保留双编码器架构，移除空间感知预训练仍导致性能下降，证明预训练阶段注入的 3D 空间先验不可由架构单独弥补。
2. **双编码器的独立贡献**（+2.0）：移除 3D 视觉编码器和融合层后性能下降更为显著，表明实时 3D 空间特征的显式编码对下游任务至关重要。
3. **协同效应**：两者同时移除导致 3.7 个百分点的最大降幅，大于各自独立贡献之和（1.2+2.0=3.2），暗示预训练与双编码器之间存在正向交互——预训练使融合层更有效地利用 3D 空间特征。

此外，论文指出仅通过第一阶段 3D 视觉对齐（3D-Visual Pretraining）即可带来显著收益，表明语义与空间视觉特征的对齐本身已能改善模型的空间理解能力。

---

### 3D 空间理解定量评估

Table 8 和 Figure 8 通过 Hand3D-test 数据集对模型的 3D 空间理解能力进行独立评估，指标包括方向得分（Direction Score，满分 3）和距离误差（Distance Error，单位：米）。

![[assets/figures/papers/paper_list_l2647_https_arxiv_org_abs_2512_13080/figures/016_Figure_8.jpg]]
*Figure 8: Comparison between VIPA-VLA-PT and InternVL3.5 on Hand3D-test. Left: histogram of direction scores; Right: histogram of distance errors*

- **VIPA-VLA-PT**（预训练后）：方向得分 **1.82/3**，距离误差 **0.12m**
- **InternVL3.5**（无预训练）：方向得分 **1.22/3**，距离误差 **0.18m**

Figure 8 的直方图分布进一步显示，VIPA-VLA-PT 的方向得分分布整体右移（更多高分样本），距离误差分布整体左移（更多低误差样本），表明空间感知预训练系统性地提升了模型对 3D 空间关系的判断精度。

---

### 运动轨迹预测可视化

Figure 9 展示了 VIPA-VLA 在第二阶段预训练（3D-Action Pretraining）后的运动轨迹预测能力。蓝色预测轨迹与红色真实轨迹在方向和幅度上高度吻合，验证了离散运动 token 表示（将 1m³ 物理空间量化为 1024 个 bin）能够有效捕捉人类手部在 3D 空间中的运动模式。这为下游机器人动作接地提供了可迁移的运动先验。

![[assets/figures/papers/paper_list_l2647_https_arxiv_org_abs_2512_13080/figures/017_Figure_9.jpg]]
*Figure 9: Visualization of the predicted motion trajectories from VIPA-VLA after second stage pretraining (blue lines) and the ground-truth trajectories (red lines)*

---

### 失败模式分析

Figure 7 对比了 VIPA-VLA 与 InternVL3.5 在真实机器人任务上的典型失败案例：

1. **空间定位偏差**：InternVL3.5 在抓取阶段频繁出现末端执行器与目标物体的空间错位，而 VIPA-VLA 的失败更多出现在接触后的精细操作阶段，表明预训练主要改善了接近与定位阶段的空间接地。
2. **长程任务累积误差**：在多步骤任务（如 Put-Three-Obj）中，VIPA-VLA 的整任务成功率虽显著优于基线（10% vs. 0%），但绝对成功率仍较低，反映出从人类手部动作到机器人执行器的具身差距在长程任务中会累积放大。
3. **遮挡与低纹理场景**：受限于单目点云估计（Cut3R）在严重遮挡或低纹理条件下的质量下降，部分场景中空间注释的噪声可能导致预训练收益减弱——该限制需在后续工作中通过多目融合或更强的深度估计基础模型来缓解。

## 定位与知识库关联

### 1. 问题定位：从VLM到空间感知VLA的跃迁

VIPA-VLA的核心贡献在于填补了当前视觉-语言-动作模型（VLA）的一个关键空白：**2D视觉感知与3D物理动作空间之间的接地鸿沟**。现有VLA模型（如**OpenVLA**，Kim et al., arXiv 2024）通常直接从2D视觉特征预测动作，缺乏对场景几何和空间关系的显式建模，导致空间推理能力弱、泛化性受限。VIPA-VLA通过在大规模人类演示视频上进行**视觉-物理对齐预训练**，将3D空间理解作为先验注入VLA模型，从而在下游机器人任务中实现更鲁棒的视觉-动作对齐。

这一思路与近期空间感知VLA的探索方向一致——**SpatialVLA**（Qu et al., arXiv 2025）同样尝试引入3D空间信息，但VIPA-VLA的区别在于：（1）完全使用人类视频数据进行预训练，不依赖任何机器人数据；（2）提出双编码器架构将语义特征与3D空间特征通过交叉注意力显式融合；（3）通过两阶段预训练（3D视觉对齐 + 3D动作对齐）逐步注入空间理解。

### 2. 方法谱系：在VLA生态中的定位

从方法谱系看，VIPA-VLA处于以下几条技术路线的交汇点：

**VLM→VLA扩展线**：以**InternVL3.5-2B**（Wang et al., arXiv 2025）为代表的大规模视觉-语言模型为骨干，VIPA-VLA在此基础上扩展动作预测能力。与**CoT-VLA**（Zhao et al., CVPR 2025）等引入思维链推理的VLA不同，VIPA-VLA的改进重点在于感知层面的空间接地，而非推理链设计。

**扩散策略线**：VIPA-VLA的后训练阶段采用扩散Transformer（DiT）作为动作头，通过流匹配生成动作块。这与**DiT Policy**（Hou et al., arXiv 2024）和**π0-FAST / T0.5**（Pertsch et al., 2025; Black et al., CoRL 2025）等扩散策略方法共享技术基础，但VIPA-VLA的独特之处在于将LLM输出的条件向量与机器人状态共同输入DiT，实现了语言指令、视觉场景与动作生成的深度融合。

**大模型VLA线**：**GR00T N1 / N1.5**（Bjorck et al., arXiv 2025）代表了基于大规模模型和多视图输入的VLA路线。VIPA-VLA在LIBERO单视图设置下（92.4%）显著优于GR00T N1.5（88.6%），证明空间感知预训练可以在相对轻量的模型规模下获得竞争力。

### 3. 适用边界与关键约束

**数据依赖性**：VIPA-VLA的预训练完全依赖Hand3D数据集的自动化注释流水线，该流水线使用Cut3R进行单目点云估计。在严重遮挡、低纹理或动态模糊场景下，点云质量下降会直接影响3D视觉注释的准确性，进而削弱预训练效果。

**具身差距**：尽管通过离散运动token（将1m³物理空间量化为1024个bin）部分缓解了人手与机器人执行器之间的形态差异，但这一差距并未根本消除。人类手部的灵巧操作（如精细指尖操作）与平行夹爪或吸盘式末端执行器之间存在本质差异，token离散化仅能处理轨迹层面的粗略对齐。

**任务覆盖范围**：当前Hand3D数据主要来自桌面级物体操作场景，尚未覆盖全身操控、移动操作、多臂协作等更复杂的机器人任务。在RoboCasa基准（涵盖门/抽屉操作等更多样化场景）上，VIPA-VLA的45.8%成功率虽优于基线，但绝对水平仍表明存在改进空间。

### 4. 局限性与开放问题

**已验证的局限性**：

1. **单目重建瓶颈**：Cut3R作为3D视觉编码器，其点云估计质量受限于单目输入，在遮挡、低纹理场景下注释噪声增大。消融实验（Table 7）显示移除3D编码器导致性能从92.4%降至90.4%，间接表明3D特征的质量对最终性能有实质性影响。

2. **具身迁移的未解决问题**：人类手部动作与机器人执行器之间的embodiment gap通过离散化token部分缓解，但真实机器人实验（Table 5）中“Put-Three-Obj”整任务成功率仅10%，远低于子任务成功率（52%），说明长序列任务中的误差累积仍是瓶颈。

3. **预训练数据规模与多样性**：Hand3D-visual包含约300K指令-回答对，Hand3D-action包含约1M运动-指令对（Table 1, Table 2）。相比互联网规模的数据集，这一规模仍然有限，且场景多样性受限于现有视频数据源。

**开放问题**：

1. **跨具身泛化**：如何将视觉-物理对齐预训练范式扩展到全身人形机器人或移动操作平台？这需要解决更复杂的运动学链和更大的物理工作空间建模问题。

2. **数据融合策略**：是否可以通过融合大规模机器人数据与人类视频数据进一步缩小视觉-物理对齐与机器人执行之间的差距？这涉及异构数据源的联合训练策略设计。

3. **自动注释流水线的扩展性**：在海量互联网视频上扩展Hand3D数据自动标注流水线的可行性及其对VLA模型泛化性的影响。这需要解决域偏移（互联网视频与机器人视角差异）和注释质量控制问题。

4. **空间理解的深层评估**：Table 8和Figure 8显示VIPA-VLA-PT在3D方向评分（1.82/3 vs. 1.22/3）和距离误差（0.12m vs. 0.18m）上优于InternVL3.5基线，但绝对方向评分仍不完美。如何进一步提升空间理解的精度和鲁棒性，是一个开放的技术挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/Spatial_Aware_VLA_Pretraining_through_Visual_Physical_Alignment_from_Human_Videos.pdf]]
