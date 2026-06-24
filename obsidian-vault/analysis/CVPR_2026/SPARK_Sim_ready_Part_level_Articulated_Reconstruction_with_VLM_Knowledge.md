---
title: "SPARK: Sim-ready Part-level Articulated Reconstruction with VLM Knowledge"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SPARK_Sim_ready_Part_level_Articulated_Reconstruction_with_VLM_Knowledge.pdf
project_link: "https://heyumeng.com/SPARK/index.html"
code_link: null
aliases:
- SPARK
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入VLM先验生成粗URDF和部件参考图像，并通过在扩散Transformer中集成层次注意力与可微关节优化，使得部件几何与运动学参数能够协同改进。
primary_logic: 利用VLM的常识推理能力获取初步的铰接结构和部件视觉线索，再将这些先验注入到扩散模型中指导部件几何生成，最后通过可微正向动力学和渲染优化关节参数，实现了从单张RGB图像到仿真就绪铰接对象的高质量重建。
claims:
- SPARK从单张RGB图像重建出在运动学上一致的部件级铰接对象。
- 利用VLM提取粗URDF参数并生成部件级参考图像。
- 扩散Transformer结合部件图像引导和结构图生成一致形状。
- 可微动力学和渲染优化关节参数，获得高精度URDF。
---

# SPARK: Sim-ready Part-level Articulated Reconstruction with VLM Knowledge

> [!tip] 核心洞察
> 利用VLM的常识推理能力获取初步的铰接结构和部件视觉线索，再将这些先验注入到扩散模型中指导部件几何生成，最后通过可微正向动力学和渲染优化关节参数，实现了从单张RGB图像到仿真就绪铰接对象的高质量重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | SPARK：利用VLM知识的仿真就绪部件级铰接重建 |
| 英文题名 | SPARK: Sim-ready Part-level Articulated Reconstruction with VLM Knowledge |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.01629) · [Project](https://heyumeng.com/SPARK/index.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SPARK |
| Dataset | GAPartNet |

> [!tip] 效果简介
> - GAPartNet (50 images, 25 categories) 上，CD↓ 0.3959 vs PartCrafter 0.4342 (-0.0383)；F-Score@0.1↑ 0.4214 vs PartCrafter 0.3600 (+0.0614)；F-Score@0.5↑ 0.8934 vs PartCrafter 0.8840 (+0.0094)。

## 概述

从单张 RGB 图像重建具有物理一致性的部件级铰接对象，是三维视觉与机器人仿真交叉领域的一个关键瓶颈。现有方法要么仅生成融合的整体几何体而缺乏运动学结构，要么依赖多状态视觉数据或模板检索，难以同时恢复精细的部件几何与完整的 URDF 参数。**SPARK** 针对这一困境提出了一个全新的框架：它首次将视觉-语言模型（VLM）的常识推理能力引入铰接对象重建管道，利用 VLM 生成粗粒度的 URDF 参数与部件级参考图像，再将这些先验注入扩散 Transformer（DiT）中指导部件几何生成，最后通过可微正向动力学与可微渲染联合优化关节参数，从而从单张 RGB 图像端到端地输出仿真就绪的铰接对象。

在方法谱系上，SPARK 与现有的部件级生成方法（如 **PartCrafter** 和 **OmniPart**）以及 URDF 估计方法（如 **Articulate-Anything** 和 **URDFormer**）形成鲜明对比。PartCrafter 虽能同时生成所有部件，但缺乏运动学感知；OmniPart 依赖 2D 分割与空间边界框，部件间缺乏结构约束。而在 URDF 估计侧，Articulate-Anything 仅通过 VLM 一次性预测关节参数，精度有限；URDFormer 则依赖模板检索，泛化能力受限。SPARK 的创新在于将 VLM 先验、层次注意力扩散生成、可微关节优化三者有机耦合：VLM 提供粗结构与视觉线索，层次注意力在生成过程中保持部件间的运动结构一致性，可微优化则显著提升连续关节参数的精度。

实验结果表明，SPARK 在 GAPartNet 测试集（50 张图像，25 个类别）上全面超越现有方法。在形状重建方面，Chamfer 距离（CD）降至 0.3959（PartCrafter 为 0.4342），F-Score@0.1 提升至 0.4214（PartCrafter 为 0.3600）。在 URDF 参数估计方面，关节轴误差从 Articulate-Anything 的 0.5491 大幅降至 0.1577，枢轴误差从 0.3529 降至 0.1653，类型错误率从 0.2500 降至 0.0500。消融实验进一步证实，部件图像引导、多姿态数据增强和关节优化模块各自对最终性能有显著贡献。

该方法当前主要支持旋转和棱柱等常见关节类型，对多自由度关节和闭链结构尚未覆盖，且 VLM 先验的质量直接影响输出结果。尽管如此，SPARK 为从单目图像到仿真就绪铰接资产的自动化生成开辟了新的技术路径，并在机器人操作策略训练等下游任务中展现出初步的应用潜力。

## 背景与动机

从单张RGB图像重建可交互的铰接三维对象，是计算机视觉、图形学与机器人学交叉领域的一项核心挑战。这类对象——例如可开合的抽屉、可旋转的笔记本屏幕——由多个刚性部件通过运动学关节连接而成，其完整数字孪生不仅需要高保真的部件级几何与纹理，还必须包含精确的运动学参数（通常以URDF格式描述），才能直接导入仿真器用于机器人训练与物理推理。

然而，现有的铰接对象生成方法在**运动学一致性**与**重建完整性**两个维度上存在显著缺口。一方面，以**PartCrafter**为代表的部件级3D生成方法虽然能够从图像中同时生成多个部件网格，但其扩散Transformer架构缺乏对部件间运动学关系的显式建模，生成的部件几何在关节连接处常出现穿透、错位等物理不一致现象。另一方面，**URDFormer**等基于模板检索的装配方法、**Articulate-Anything**等利用多模态大语言模型（MLLM）进行URDF图预测的方法，以及**Articulate AnyMesh**等从已有3D网格中基于启发式规则估计关节参数的方法，要么依赖多状态视觉数据或先验3D模型，要么仅能输出粗粒度的运动学描述，难以与部件级几何生成协同优化。核心瓶颈在于：**从单张静态图像中同时恢复部件级几何结构与完整的URDF参数，本质上是欠约束的逆问题**——单视角观测无法直接提供关节运动范围、轴方向等动态信息。

SPARK的核心洞察在于：**视觉-语言模型（VLM）具备丰富的常识推理能力，能够从单张图像中推断出物体的铰接结构先验**——例如“这是一个抽屉，抽屉应该沿水平方向拉出”。将这些先验注入到生成式扩散模型中，可以弥合静态观测与动态运动学之间的信息鸿沟。具体而言，SPARK通过三个关键机制实现突破：(1) 利用VLM生成粗URDF参数和部件级参考图像，为后续生成提供语义与结构引导；(2) 在扩散Transformer中集成层次注意力与位置嵌入，使部件几何生成过程显式感知父子运动链关系；(3) 引入可微正向动力学与可微渲染联合优化关节参数，以VLM生成的打开状态图像作为监督信号，实现从粗到精的运动学参数细化。这一设计使得SPARK首次实现了从单张RGB图像到**仿真就绪**铰接对象的高质量重建，为机器人仿真训练等下游应用提供了端到端的资产生成管道。

## 核心创新

SPARK 的核心创新在于将**视觉语言模型（VLM）的常识推理能力**与**扩散Transformer（DiT）的生成能力**以及**可微运动学优化**深度耦合，形成了一条从单张RGB图像到仿真就绪铰接对象的完整链路。相较于现有方法，SPARK 在三个关键维度上实现了突破。

### 1. VLM先验注入：从语义理解到几何引导

现有部件级生成方法（如 **PartCrafter**、**OmniPart**）仅依赖全局图像或2D分割掩膜作为条件，缺乏对部件语义和运动结构的显式建模。SPARK 首次将 VLM 作为“结构推理引擎”，从输入图像中提取三类关键先验：

- **粗URDF参数**：VLM 推断部件的层次结构、连接关系，并从预定义字典中选择离散关节属性（类型、轴方向），形成初始的URDF模板。关节参数集合定义为 $\mathbf{u}_j = \{ \mathbf{\bar{u}}_j^{\mathrm{type}}, \mathbf{u}_j^{\mathrm{axis}}, \mathbf{u}_j^{\mathrm{origin}}, \mathbf{u}_j^{\mathrm{limit}} \}$，其中 $\mathbf{u}_j^{\mathrm{type}} \in \{ \text{fixed}, \text{revolute}, \text{prismatic} \}$。
- **部件级参考图像**：VLM 根据语义标签为每个部件生成独立的参考图像，作为 DiT 中局部交叉注意力的条件信号。
- **打开状态图像**：VLM 预测铰接对象在打开状态下的外观，为后续关节优化提供监督目标。

这一设计将“常识推理”转化为可操作的几何生成条件，弥补了纯数据驱动方法在结构感知上的不足。消融实验表明，**去除部件图像引导后，F-Score@0.1 从 0.4214 降至 0.3755**，验证了部件级视觉先验对精细几何恢复的关键作用（Table 3）。

### 2. 层次注意力DiT：运动结构一致性的几何生成

SPARK 在扩散Transformer中引入了**层次注意力机制**，显式建模部件间的父子关系，这是区别于标准DiT（如 PartCrafter）的核心架构创新。具体而言：

- **子到父注意力**：子节点令牌仅关注其父节点令牌，注意力权重为 $A_{uv}^{c p} = \frac{\exp(Z_u Z_v^{\top} / \sqrt{C}) \mathbf{1}[v \in \mathcal{P}(u)]}{\sum_{v'} \exp(Z_u Z_{v'}^{\top} / \sqrt{C}) \mathbf{1}[v' \in \mathcal{P}(u)]}$。
- **父到子注意力**：父节点令牌反向查询子节点令牌，实现双向信息流：$A_{uv}^{p c} = \frac{\exp(Z_u (Z_v)^{\top} / \sqrt{C}) \mathbf{1}[v \in \mathcal{C}(u)]}{\sum_{v'} \exp(Z_u (Z_{v'})^{\top} / \sqrt{C}) \mathbf{1}[v' \in \mathcal{C}(u)]}$。

这种设计使得每个部件的几何生成不仅受自身图像条件约束，还通过结构图传递运动学上下文，确保组装后的整体对象在关节连接处保持几何一致性。同时，SPARK 采用**绝对/相对位置嵌入**编码部件在铰接链中的空间关系，进一步强化了结构感知。

### 3. 可微关节优化：从粗估计到高精度URDF

现有方法（如 **Articulate-Anything**、**Articulate AnyMesh**）或依赖VLM一次性预测URDF参数，或基于启发式规则从网格估计关节属性，难以保证运动学精度。SPARK 提出了**两阶段细化策略**：

- **离散参数细化**：通过特征注入策略，将粗URDF参数与输入图像特征融合，重新预测关节类型和轴方向等离散属性。
- **连续参数优化**：引入**可微正向动力学**和**可微渲染**，以VLM生成的打开状态图像为监督，优化关节原点 $\mathbf{u}_j^{\mathrm{origin}}$ 和运动角度等连续参数。优化目标为 $\operatorname*{min}_{\xi} \mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{pixel}}(I_{\mathrm{sil}}, I_{\mathrm{open}}) + \mathcal{L}_{\mathrm{reg}}(\xi)$，其中正则项 $\mathcal{L}_{\mathrm{reg}} = \lambda_{t} \|\Delta \mathbf{t}\|_{2}^{2} + \lambda_{\theta} \|\Delta \theta\|_{2}^{2}$ 约束参数偏移量，保证优化稳定性。

消融实验表明，**关节优化模块使 AxisErr 从 0.3148 大幅降低至 0.1577**（Table 4），证明了可微细化在恢复连续关节参数中的有效性。此外，**数据增强策略**（通过URDF正向动力学生成多关节姿态训练数据）进一步将 Chamfer 距离从 0.4200 降至 0.3959，提升了模型对非规范姿态的重建鲁棒性（Table 3）。

## 整体框架

SPARK 的整体设计围绕一个核心矛盾展开：从单张 RGB 图像重建部件级铰接对象，既需要精确的几何结构，又必须满足运动学一致性。现有方法要么生成融合的整体网格而丢失部件边界，要么依赖多状态视觉数据来推断关节参数。SPARK 的解决方案是将这一难题分解为三个协同阶段——**VLM 引导的结构推理**、**基于扩散 Transformer 的部件-铰接对象生成**、以及**可微关节优化**——形成一个从粗到精、从语义到几何的闭环管道。

### 管道总览

管道的输入是一张单视角 RGB 图像 $I_0$，输出是一组部件级网格 $\{\mathbf{M}_k\}_{k=1}^K$ 及其对应的完整 URDF 参数。三个核心模块按以下顺序衔接：

1. **VLM 引导的结构推理**：视觉语言模型从输入图像中推断部件的层次结构、部件数量和连接关系，生成粗粒度的 URDF 模板、每个部件的参考图像，以及预测的打开状态图像 $I_{\mathrm{open}}$。这一阶段将高层语义知识转化为后续几何生成和关节优化的结构化先验。

2. **部件-铰接对象生成（DiT）**：扩散 Transformer 以部件级参考图像和全局图像为条件，同时生成所有部件的 3D 网格。通过局部交叉注意力、全局自注意力以及父子层次注意力机制，模型在生成过程中保持部件间的运动结构一致性。生成完成后，独立的纹理生成模块为每个运动部件赋予逼真纹理。

3. **关节优化**：在获得部件网格后，系统对离散关节参数（类型、轴）进行特征注入式细化，并通过可微正向动力学和可微渲染，以 VLM 生成的打开状态图像为监督，优化连续关节参数（原点、角度），最终输出高精度的 URDF。

### 关键设计决策

**为什么需要 VLM 先验？** 单张图像所能提供的 3D 结构信息天然不足，尤其是隐含的关节类型、运动轴方向和部件连接关系。VLM 利用其常识推理能力，从 2D 外观中“猜测”出这些不可见属性，为后续的几何生成提供语义锚点。实验表明，去除部件图像引导后，F-Score@0.1 从 0.4214 降至 0.3755，验证了这一先验对精细几何恢复的关键作用。

**为什么在 DiT 中引入层次注意力？** 标准 DiT 对所有令牌进行全局自注意力，无法显式建模部件间的父子约束关系。SPARK 在 DiT 中集成了两种非对称注意力模式：子节点令牌仅关注其父节点令牌（child-to-parent），父节点令牌反向查询子节点令牌（parent-to-child）。这种设计使得结构信息在生成过程中显式传播，确保子部件的几何形状与其父部件的运动约束保持一致。

**为什么要将关节参数分阶段优化？** 离散参数（如关节类型是旋转还是棱柱）适合通过 VLM 的语义推理一次性确定，而连续参数（如关节原点的精确位置）则需要与生成后的 3D 几何进行物理级对齐。SPARK 的可微优化阶段通过最小化渲染轮廓与打开状态图像之间的像素级误差，同时施加正则化约束以防止参数偏移过大，从而在几何生成之后对连续参数进行精细校准。

### 数据流与训练策略

训练数据的制备同样体现了管道设计的完整性。原始 PartNet-Mobility 数据集中存在过分割网格问题，SPARK 根据 URDF 标注中的链接关联关系合并这些碎片，并进行水密化处理。更重要的是，通过 URDF 的正向动力学生成多关节姿态（最大开合、半开状态）的训练数据，使得模型在推理时对非规范姿态具有更强的鲁棒性——消融实验表明，这一数据增强策略将 Chamfer 距离从 0.4200 降至 0.3959。

整个管道的输入输出流清晰：单张 RGB 图像 → VLM 语义解析（粗 URDF + 部件参考图像 + 打开状态图像）→ DiT 几何生成（部件网格 + 完整铰接对象）→ 纹理生成 → 可微关节优化（高精度 URDF）。这种从语义到几何再到物理的分阶段设计，使得每个模块可以专注于其擅长的子问题，同时通过先验注入和损失监督实现跨阶段的协同改进。

### 补充图表

![[assets/figures/papers/paper_list_l2033_https_arxiv_org_abs_2512_01629/figures/001_Figure_1.jpg]]
*Figure 1: SPARK is a novel framework that integrates VLM-guided part-level and global image guidance with diffusion transformers to produce high-quality articulated object reconstructions*

## 核心模块与公式推导

SPARK 的管线由三个紧密耦合的核心模块构成：**VLM引导的结构推理**、**部件-铰接对象生成**与**关节参数优化**。每个模块解决一个关键子问题，并通过信息流串联形成从单张 RGB 图像到仿真就绪铰接对象的完整通路。

### VLM引导的结构推理

给定输入图像 $I_0$，该模块利用视觉语言模型（VLM）的常识推理能力，一次性输出三类结构化先验：

1. **粗URDF参数**：VLM 推断部件的层级结构，包括连杆与关节的数量及连接关系，并从预定义字典中选择离散关节属性。每个关节 $j$ 的参数集合定义为：

   $$\mathbf{u}_j = \{ \mathbf{\bar{u}}_j^{\mathrm{type}}, \mathbf{u}_j^{\mathrm{axis}}, \mathbf{u}_j^{\mathrm{origin}}, \mathbf{u}_j^{\mathrm{limit}} \}$$

   其中 $\mathbf{u}_j^{\mathrm{type}} \in \{ \text{fixed}, \text{revolute}, \text{prismatic} \}$ 为离散关节类型，$\mathbf{u}_j^{\mathrm{axis}}$ 为关节轴方向，$\mathbf{u}_j^{\mathrm{origin}}$ 为关节原点，$\mathbf{u}_j^{\mathrm{limit}}$ 为运动限制。离散属性从预定义字典中选取，以保证语义与方向一致性。

2. **部件级参考图像**：VLM 根据语义标签为每个部件生成一张参考图像，作为后续扩散模型局部交叉注意力的条件信号。

3. **打开状态图像** $I_{\mathrm{open}}$：VLM 预测铰接对象在打开姿态下的外观，为后续关节优化提供监督目标。

### 部件-铰接对象生成

该模块以扩散Transformer（DiT）为骨干，同时生成 $K$ 个部件的三维网格 $\{ \mathbf{M}_k \}_{k=1}^K$ 并组装为完整铰接对象。其核心创新在于将 VLM 先验注入生成过程的多级注意力机制：

- **局部交叉注意力**：每个部件令牌以其对应的 VLM 生成参考图像为条件，实现部件级视觉引导。
- **全局交叉注意力**：所有部件令牌以输入图像的整体特征为条件，保持全局一致性。
- **层次注意力**：利用 VLM 推断的父子结构图，在部件令牌间建立有向信息流。子节点令牌仅关注其父节点令牌（子到父注意力），父节点令牌反向查询其所有子节点令牌（父到子注意力）。

子到父注意力权重定义为：

$$A_{uv}^{c p} = \frac{\exp(Z_u Z_v^{\top} / \sqrt{C}) \mathbf{1}[v \in \mathcal{P}(u)]}{\sum_{v'} \exp(Z_u Z_{v'}^{\top} / \sqrt{C}) \mathbf{1}[v' \in \mathcal{P}(u)]}$$

父到子注意力权重定义为：

$$A_{uv}^{p c} = \frac{\exp(Z_u Z_v^{\top} / \sqrt{C}) \mathbf{1}[v \in \mathcal{C}(u)]}{\sum_{v'} \exp(Z_u Z_{v'}^{\top} / \sqrt{C}) \mathbf{1}[v' \in \mathcal{C}(u)]}$$

其中 $\mathcal{P}(u)$ 和 $\mathcal{C}(u)$ 分别表示节点 $u$ 的父节点集合与子节点集合，指示函数 $\mathbf{1}[\cdot]$ 将注意力严格限制在结构边所定义的令牌对上。这种层次化信息交换使部件生成能够感知运动学约束，从而在几何上保持部件间的结构一致性。

训练采用 Rectified Flow 目标函数：

$$\mathcal{L}_{\mathrm{RF}} = \mathbb{E}\left[w(t) \sum_{k=1}^{K} \alpha_k \| v_{\theta}(x_k(t), C, t) - u_k^{\star} \|_2^2\right]$$

其中 $w(t)$ 为时间步权重，$\alpha_k$ 为逐部件权重系数，$C$ 为条件信号（包含部件图像、全局图像与结构图），$v_{\theta}$ 为预测的速度场。

### 关节参数优化

VLM 直接预测的粗 URDF 参数精度有限，尤其在连续参数（关节原点、旋转角度）上存在显著偏差。该模块通过两级细化策略解决此问题：

**离散参数细化**：对关节类型和轴方向等离散参数，采用特征注入策略，将粗 URDF 编码与输入图像特征融合后重新预测，提升分类与方向估计的准确性。

**连续参数优化**：对关节原点 $\mathbf{u}_j^{\mathrm{origin}}$ 和打开角度等连续参数，引入可微正向动力学与可微渲染，以 VLM 生成的打开状态图像 $I_{\mathrm{open}}$ 为监督进行优化。优化目标为：

$$\min_{\xi} \mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{pixel}}(I_{\mathrm{sil}}, I_{\mathrm{open}}) + \mathcal{L}_{\mathrm{reg}}(\xi)$$

其中 $I_{\mathrm{sil}}$ 为通过可微渲染器从前向动力学变换后的网格中提取的轮廓图像，$\mathcal{L}_{\mathrm{pixel}}$ 度量其与 $I_{\mathrm{open}}$ 之间的像素级差异，$\xi$ 为可学习的连续关节参数。正则化项约束参数偏移量：

$$\mathcal{L}_{\mathrm{reg}} = \lambda_{t} \|\Delta \mathbf{t}\|_{2}^{2} + \lambda_{\theta} \|\Delta \theta\|_{2}^{2}$$

其中 $\Delta \mathbf{t}$ 和 $\Delta \theta$ 分别为关节平移和旋转相对于初始估计的偏移，$\lambda_t$ 和 $\lambda_{\theta}$ 为对应的正则化系数。该正则化确保优化过程中参数不会偏离 VLM 初始估计过远，避免因可微渲染的局部最优导致运动学结构崩溃。

三个模块形成闭环：VLM 提供粗粒度的结构与视觉先验，DiT 将这些先验转化为几何一致的部件网格，关节优化则利用生成结果与 VLM 预测的打开状态图像进一步校准运动学参数，最终输出可直接导入仿真器的完整 URDF 模型。

### 补充图表

![[assets/figures/papers/paper_list_l2033_https_arxiv_org_abs_2512_01629/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline Overview. We use a VLM to generate per-part reference images, predicted open-state images, and URDF templates with preliminary joint and link estimations. A Diffusion Transformer (DiT) equipped with local, global, and hierarchical attention mechanisms simultaneously synthesizes part-level and complete articulated meshes from a single image with VLM priors. We further employ a generative texture model to generate realistic textures and refine the URDF parameters using differentiable forward kinematics and differentiable rendering under the guidance of the predicted open-state images*

## 实验与分析

### 形状重建评估

SPARK在GAPartNet测试集的50张图像（覆盖25个类别）上与三个部件级重建基线进行了定量对比。表1展示了Chamfer Distance（CD）和F-Score的结果。SPARK在CD指标上达到**0.3959**，相比PartCrafter的0.4342降低了0.0383，表明整体几何保真度更优。在F-Score@0.1上，SPARK取得**0.4214**，较PartCrafter的0.3600提升0.0614，说明在精细部件边界的重建精度上有显著优势。在更宽松的F-Score@0.5上，SPARK（0.8934）仍以微弱优势领先PartCrafter（0.8840）。OmniPart和URDFormer在各项指标上均明显落后，这主要归因于它们缺乏对部件级几何的显式建模能力。

定性对比（图3）进一步验证了这一趋势：SPARK生成的铰接对象具有清晰的部件边界和准确的相对姿态，而PartCrafter虽能生成完整形状，但在部件分离度和运动结构一致性上存在不足。

### URDF参数估计评估

表2报告了URDF参数估计的定量对比。SPARK在三个关键指标上均大幅领先：

- **AxisErr↓**：0.1577 vs. Articulate-Anything的0.5491，降低0.3914
- **PivotErr↓**：0.1653 vs. Articulate-Anything的0.3529，降低0.1876
- **TypeErr↓**：0.0500 vs. Articulate-Anything的0.2500，降低0.2000

Articulate-AnyMesh作为基于3D网格启发式的方法，其URDF估计精度同样远低于SPARK。这一差距的核心原因在于：SPARK的可微优化模块能够利用VLM生成的打开状态图像作为监督信号，对关节原点、轴和角度进行精细化调整，而基线方法仅依赖一次性预测或几何启发式规则。图4的定性对比显示，SPARK估计的URDF参数能够产生物理上合理的打开状态，而基线方法常出现关节错位或运动方向错误。

### 消融实验

**部件图像引导。** 移除部件级参考图像条件后（w/o Part Guidance），F-Score@0.1从0.4214降至0.3755，CD从0.3959升至0.4196。这表明VLM生成的部件视觉先验对于恢复精细的部件几何结构至关重要，仅依赖全局图像条件会导致部件边界模糊和形状退化。

**数据增强。** 去除多姿态训练数据增强后（w/o Data Aug.），CD从0.3959升至0.4200。这说明在训练中引入通过正向运动学生成的最大/半开关节姿态，能够有效提升模型对非规范姿态下铰接对象的重建鲁棒性。

**关节优化模块。** 表4的消融显示，移除可微关节优化后（w/o Joint Optimization），AxisErr从0.1577急剧上升至0.3148，PivotErr从0.1653升至0.2237。这证明仅靠VLM的粗估计无法获得高精度的连续关节参数，可微正向运动学与可微渲染的联合优化是实现仿真就绪URDF的关键环节。

### 失败模式与局限性

尽管SPARK在整体指标上表现优异，但在以下场景中存在性能退化：

1. **复杂运动结构**：当前方法仅支持旋转和棱柱等常见单自由度关节，对于多自由度关节、复合机构或闭链运动结构无法进行正确建模和重建。
2. **VLM先验质量依赖**：当VLM无法正确理解物体结构（如罕见或不常见的铰接对象）时，生成的粗URDF模板和部件参考图像可能包含错误，这些错误会传播到后续的几何生成和关节优化阶段，导致重建失败。
3. **纹理-几何不一致**：纹理生成和ICP对齐步骤独立于几何生成管道，未进行端到端的联合优化，在部分情况下可能出现纹理与几何边界不匹配的现象。
4. **可微渲染的简化假设**：关节优化基于前景/背景轮廓的像素级损失，对于具有复杂纹理或光照变化的场景，轮廓提取可能不准确，从而影响优化精度。

### 下游应用验证

SPARK生成的铰接对象资产可直接导入仿真环境。图7展示了使用SPARK重建的抽屉模型在Isaac Sim中训练机器人完成打开抽屉任务的示例，验证了该方法生成的资产具备仿真就绪的运动学属性，能够支撑机器人操作策略的学习与迁移。

### 补充图表

![[assets/figures/papers/paper_list_l2033_https_arxiv_org_abs_2512_01629/figures/003_Table_1.jpg]]
*Table 1: Quantitative Shape Reconstruction Comparison. We report F-score to measure reconstruction accuracy, Chamfer Distance (CD) for geometric fidelity*

![[assets/figures/papers/paper_list_l2033_https_arxiv_org_abs_2512_01629/figures/004_Table_2.jpg]]
*Table 2: Quantitative URDF Parameter Estimation Comparison. We evaluate articulated object URDF parameter estimation using AxisErr, PivotErr, and TypeErr, which measure joint axis deviation, joint pivot offset, and joint type misclassification*

![[assets/figures/papers/paper_list_l2033_https_arxiv_org_abs_2512_01629/figures/005_Table_3.jpg]]
*Table 3: Mesh Reconstruction Ablation. Ablation on mesh reconstruction quality*

![[assets/figures/papers/paper_list_l2033_https_arxiv_org_abs_2512_01629/figures/006_Table.jpg]]

![[assets/figures/papers/paper_list_l2033_https_arxiv_org_abs_2512_01629/figures/007_Figure_5.jpg]]
*Figure 5: In-the-wild image results. Additional examples of shape reconstruction and open-state prediction on in-the-wild images*

![[assets/figures/papers/paper_list_l2033_https_arxiv_org_abs_2512_01629/figures/008_Figure_6.jpg]]
*Figure 6: Ablation. We conduct an ablation study on data augmentation, part guidance, and joint optimization*

![[assets/figures/papers/paper_list_l2033_https_arxiv_org_abs_2512_01629/figures/009_Figure_7.jpg]]
*Figure 7: Robot Learning. We use the synthesized drawer to train a robot in Isaac Sim [34] to open a drawer*

## 方法谱系与知识库定位

### 与基线工作的关系

SPARK 处于“单图-部件级铰接重建”这一交叉问题空间，其直接对比的基线涵盖部件生成、铰接参数估计和模板检索三条技术路线。

**部件级3D生成方法。** **PartCrafter** 采用 Rectified Flow Transformer（DiT）从单张图像同时生成所有部件网格，但缺乏运动学感知，部件间仅通过隐式空间关系关联，无法保证关节一致性。**OmniPart** 依赖 2D 分割图像和空间边界框引导部件生成，同样未显式建模铰接结构。SPARK 在框架层面与 PartCrafter 共享 DiT 生成骨干，但通过三个关键改进实现差异化：(1) 引入 VLM 生成的部件级参考图像作为局部交叉注意力条件，替代仅依赖全局图像；(2) 在 DiT 中集成绝对/相对位置嵌入与父子层次注意力，显式传递运动结构信息；(3) 训练数据通过 URDF 正向动力学增强为多关节姿态，提升对非规范姿态的鲁棒性。定量结果表明，SPARK 在 GAPartNet 测试集上 CD 降至 0.3959（PartCrafter 为 0.4342），F-Score@0.1 提升至 0.4214（PartCrafter 为 0.3600），验证了运动学感知设计的有效性（Table 1）。

**URDF 参数估计方法。** **Articulate-Anything** 利用 MLLM 直接预测 URDF 图结构，但一次性预测缺乏对连续参数（关节原点、角度）的精细优化能力，导致 AxisErr 高达 0.5491、PivotErr 达 0.3529。**Articulate AnyMesh** 从已有 3D 网格出发，基于连接区域启发式估计 URDF 参数，受限于网格分割质量和启发式规则的泛化性。SPARK 采用“VLM 粗估计 + 可微细化”的两阶段策略：离散参数（类型、轴方向）通过特征注入在 VLM 预测模块中精炼；连续参数通过可微正向动力学与可微渲染，以 VLM 生成的打开状态图像为监督进行优化。该策略使 AxisErr 降至 0.1577、PivotErr 降至 0.1653、TypeErr 降至 0.0500，较 Articulate-Anything 分别降低 71.3%、53.1% 和 80.0%（Table 2）。

**模板检索方法。** **URDFormer** 通过 Transformer 从模板库中检索并组装铰接对象，依赖已有模板的覆盖范围，难以处理模板库外的物体。SPARK 的生成式方法不受模板库限制，在形状重建的 F-Score@0.5 上达到 0.8934，优于 URDFormer 的 0.8840（Table 1）。

### 适用边界

**支持的场景。** SPARK 在以下条件下表现最优：(1) 输入为单张 RGB 图像，物体具有清晰的部件边界和规范的铰接结构（如抽屉、门、笔记本电脑等旋转或棱柱关节）；(2) VLM 能够正确识别物体类别和部件语义，生成合理的粗 URDF 模板和部件参考图像；(3) 目标铰接对象的结构复杂度在 PartNet-Mobility 数据集的覆盖范围内。

**不适用或性能下降的场景。** (1) 多自由度关节、复合机构或闭链运动结构超出当前框架的关节类型假设；(2) VLM 无法正确理解物体语义时（如罕见物体或高度遮挡场景），粗 URDF 和部件图像的质量下降会级联影响后续生成与优化；(3) 真实世界零样本数据中，物体外观、光照、背景与合成训练数据差异较大时，泛化能力有待验证；(4) 纹理生成与 ICP 对齐步骤独立于几何管道，复杂纹理或光照变化可能导致纹理-几何不一致。

### 局限与开放问题

**当前局限。** (1) 关节类型限于旋转和棱柱等常见类型，未扩展到球铰、螺旋副等多自由度关节，也不支持闭链运动结构；(2) VLM 先验的质量是系统性能的上限，在 VLM 失败时缺乏可靠的故障恢复或验证机制；(3) 训练依赖 PartNet-Mobility 合成数据集，对真实场景零样本数据的泛化能力有限；(4) 纹理生成与几何重建分离，未进行端到端联合优化；(5) 关节优化基于简化的前景/背景轮廓可微渲染，对复杂纹理或光照场景的鲁棒性不足。

**开放问题。** (1) 如何将框架扩展到更复杂的运动结构，包括多自由度关节、复合机构以及闭链链接？(2) 能否从连续视频或多视角图像中自动恢复铰接结构，减少对显式 URDF 标注的依赖？(3) 如何将 SPARK 与机器人操作策略的仿真训练管道深度集成，以提高仿真到现实的迁移效果（Figure 7 展示了初步的机器人学习应用）？(4) 在 VLM 先验不可靠时，是否存在基于几何一致性或物理约束的自动纠错机制？(5) 该方法能否扩展到非刚性或可变形物体的铰接重建？

## 原文 PDF

![[paperPDFs/CVPR_2026/SPARK_Sim_ready_Part_level_Articulated_Reconstruction_with_VLM_Knowledge.pdf]]