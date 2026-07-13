---
title: "VoMP: Predicting Volumetric Mechanical Property Fields"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/VoMP_Predicting_Volumetric_Mechanical_Property_Fields.pdf
code_link: null
project_link: https://research.nvidia.com/labs/sil/projects/vomp/
aliases:
- VoMP
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入一个基于真实世界材料数据库训练的变分自编码器（MatVAE），将杨氏模量、泊松比和密度三元组映射到一个2D潜在空间，确保所有预测的材料值落在物理有效的流形内。"
primary_logic: "通过将材料有效性与对象几何解耦，VoMP 将体积材料预测转化为在预训练材料潜在空间中的前馈学习问题，从而在几秒内即可生成可用于精确仿真器的体积属性场。"
claims:
- "VoMP 在 GVM 测试集上的杨氏模量 ALRE 达到 0.0409，远低于 NeRF2Physics 的 0.1346 和 PUGS 的 0.1688"
- "VoMP 完成预测仅需 3.59 秒，而 NeRF2Physics 需要 1454.55 秒，PUGS 需要 1058.33 秒"
- "定性比较显示 VoMP 预测的体积材料场噪声更低，物体内部材料值更合理"
- "消融实验表明移除 MatVAE 会导致所有力学属性误差显著增加，证实材料潜在空间的关键作用"
---

# VoMP: Predicting Volumetric Mechanical Property Fields

> [!tip] 核心洞察
> 通过将材料有效性与对象几何解耦，VoMP 将体积材料预测转化为在预训练材料潜在空间中的前馈学习问题，从而在几秒内即可生成可用于精确仿真器的体积属性场。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VoMP：预测体积力学属性场 |
| 英文题名 | VoMP: Predicting Volumetric Mechanical Property Fields |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.22975) · [Project](https://research.nvidia.com/labs/sil/projects/vomp) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | VoMP |
| Dataset | GVM test set (public subset), Wall-clock time (avg.) |

> [!tip] 效果简介
> - GVM test set (public subset) 上，ALRE (Young's Modulus) 为 0.0409，对比 NeRF2Physics: 0.1346, PUGS: 0.1688, Phys4DGen*: 0.2227，变化 降低约70%-82%。
> - GVM test set (public subset) 上，ARE (Poisson's Ratio) 为 0.0818，对比 Phys4DGen*: 0.1467，变化 降低约44%。
> - GVM test set (public subset) 上，ARE (Density) 为 0.0921，对比 Phys4DGen*: 1.4394, NeRF2Physics: 1.0365，变化 降低约91%-94%。

## 概要

### 问题瓶颈

为三维物体赋予物理有效的体积力学属性是构建可变形仿真资产的关键步骤。现有方法面临根本性矛盾：基于优化的方案（如 **NeRF2Physics**，Zhai et al., 2024；**PUGS**，Shuai et al., 2025）需要针对每个对象进行耗时数十分钟的迭代优化，且预测结果局限于物体表面或稀疏采样点，无法提供体积内部密集的材料分布；而基于视觉语言模型（VLM）的快速标注方案（如 **Phys4DGen\***，Lin et al., 2025a）仅能输出粗糙的部件级材料标签，缺乏物理有效性保证。这种效率与精度的对立，使得大规模三维资产的物理仿真资产化长期处于“手动标注或放弃”的困境。

更深层的问题是：不同仿真器（如 XPBD、MPM、FEM）对同一组材料参数 $E, \nu, \rho$ 的力学响应存在显著差异（Figure 2），因此预测的材料属性必须是物理真实的材料参数，而非仿真器特定的调参产物。现有方法均未系统性地解决这一物理有效性约束。

### 核心方法定位

VoMP 将体积材料预测重新定义为**在预训练材料潜在空间中的前馈学习问题**。其核心设计包含三个解耦模块：

1. **MatVAE 材料潜在空间**：在真实世界材料数据库（MTD）上训练变分自编码器，将杨氏模量 $E$、泊松比 $\nu$ 和密度 $\rho$ 三元组映射到 2D 连续潜在空间。该空间天然保证解码后的材料值落在物理有效的流形内，且支持平滑插值（Figure 7）。

2. **多视角特征聚合**：对任意输入几何体进行体素化，将多视角 DINOv2 视觉特征提升到三维体素中心，为每个体积元素编码外观语义信息（§4.1）。

3. **Geometry Transformer**：基于 TRELLIS 结构的前馈变换器，将体素特征直接映射为材料潜在代码，通过冻结的 MatVAE 解码器输出物理有效的力学属性三元组（§4.2）。

这一设计的关键因果机制是**材料有效性与对象几何的解耦**：MatVAE 在训练阶段独立学习“什么材料值是物理合理的”，Geometry Transformer 在推理阶段仅需学习“这个体素看起来像什么材料”，两者通过 2D 潜在空间衔接。这使得 VoMP 成为首个可训练的前馈体积材料预测模型，适用于网格、SDF、NeRF、高斯泼溅等多种三维表示（Figure 1）。

### 主要结果

在 GVM 测试集上，VoMP 在精度和速度两个维度均显著超越现有方法：

- **精度**：杨氏模量的 ALRE 达到 0.0409，较 NeRF2Physics（0.1346）降低约 70%，较 PUGS（0.1688）降低约 76%（Table 2）。密度的 ARE 为 0.0921，较 Phys4DGen\*（1.4394）降低约 94%。

- **速度**：单对象预测总耗时仅 3.59 秒，而 NeRF2Physics 需 1454.55 秒（约 24 分钟），PUGS 需 1058.33 秒（约 18 分钟），VoMP 实现 300–400 倍加速（Table 1）。

- **物理有效性**：消融实验证实，移除 MatVAE 直接预测 $\mathbb{R}^3$ 向量会导致杨氏模量 ALDE 从 0.3765 升至 1.1284，密度误差大幅增加（Table 8），验证了材料潜在空间对输出物理有效性的关键保障作用。

定性比较显示，VoMP 预测的体积材料场噪声更低，物体内部材料值更合理（Figure 6a），且可直接驱动网格和高斯泼溅的弹性动力学仿真（Figure 5, Figure 14）。

### 局限与开放问题

当前方法仅适用于各向同性材料，输出限于杨氏模量、泊松比和密度三个参数，尚未覆盖屈服强度、剪切模量等更广泛的工程属性。训练数据依赖 VLM 标注，可能引入噪声。如何扩展到各向异性材料、结合物理观测进行自监督微调、以及将真实材料参数自动映射到快速仿真器（如 XPBD）的可调参数，是值得探索的方向。



### 问题背景：体积力学属性预测的缺失

在计算机图形学、机器人仿真和具身智能领域，对 3D 物体进行真实感物理仿真需要准确的力学材料属性——即杨氏模量（Young’s modulus $E$）、泊松比（Poisson’s ratio $\nu$）和密度（density $\rho$）。然而，现有方法存在一个核心瓶颈：**无法高效预测物体内部体积中物理有效的力学属性**。大多数方法要么针对每个对象进行耗时的优化，要么只能给出粗糙的表面材料标签，导致仿真不准确或无法在不同仿真器之间迁移。

这一问题的严重性在 Figure 2 中得到了直观展示：当使用相同的材料参数 $(E=10^4\ \text{Pa}, \nu=0.3, \rho=10^3\ \text{kg/m}^3)$ 模拟一个实心球下落时，基于位置的动力学（XPBD）和物质点法（MPM）等快速仿真器与更精确的有限元法（FEM）表现出了显著的行为差异。这意味着，即使获得了“正确”的材料参数，不同仿真器对同一参数的解释和利用方式也可能截然不同。因此，预测值必须落在真实材料的物理有效范围内，才能在精确仿真器中产生可信的结果——这进一步要求预测模型具备对材料物理有效性的内在保证。

### 现有方法的缺口

当前方法在三个关键维度上存在明显不足：

**1. 预测范式的效率瓶颈。** 主流方法如 **NeRF2Physics**（Zhai et al., 2024）需要针对每个对象优化特征场来预测表面刚度，**PUGS**（Shuai et al., 2025）则通过 3D 高斯优化来预测材料和密度。这些方法本质上都是“每对象优化”（per-object optimization）范式，单个对象的预测时间通常在数百到数千秒量级（见 Table 1），难以满足实时或大规模应用需求。

**2. 输出物理有效性无保证。** 无论是基于优化的方法还是基于视觉语言模型（VLM）的方法（如 **Phys4DGen\***，Lin et al., 2025a），其输出的材料参数都可能偏离真实材料的物理范围。NeRF2Physics 预测的是模拟器特定的刚度参数而非通用力学属性，而 VLM 方法直接为物体部件标注粗糙材料标签，缺乏对物理有效性的显式约束。

**3. 体积预测能力的缺失。** 现有方法主要关注物体表面或稀疏采样点的材料属性预测。例如，并发工作 **Pixie**（Le et al., 2025）基于 NeRF 密度过滤进行表面偏置的材料预测，无法深入物体内部体积。然而，真实物体的力学行为（如变形、应力分布）本质上取决于其内部体积的材料分布，仅靠表面信息远远不够。

### 本文动机：前馈式体积力学属性场预测

针对上述缺口，VoMP 提出了一个根本性的思路转变：**将材料有效性与对象几何解耦，把体积材料预测转化为在预训练材料潜在空间中的前馈学习问题**。这一设计的核心洞察在于：如果能够预先学习一个代表真实世界材料分布的紧凑潜在空间，那么对任意 3D 物体的体积材料预测就可以简化为“从视觉特征映射到该潜在空间中的合适位置”，而无需针对每个对象进行优化，也无需担心输出值超出物理有效范围。

具体而言，VoMP 引入了一个基于真实世界材料数据库训练的变分自编码器（**MatVAE**），将杨氏模量、泊松比和密度三元组映射到一个 2D 潜在空间。该空间经过精心设计（包括流式后验、总相关性惩罚和逐维容量约束），确保所有解码后的材料值都落在物理有效的流形内。在此基础上，VoMP 训练一个前馈的 Geometry Transformer，仅需一次前向传播即可从多视角图像特征预测每个体素的材料潜在代码，再由冻结的 MatVAE 解码器将其映射为力学属性三元组。

这种设计带来了三个关键优势：（1）**前馈预测**，单次推理仅需约 3.59 秒，比优化类方法快 5–400 倍；（2）**物理有效性保证**，所有预测值通过 MatVAE 潜在空间天然落在真实材料分布内；（3）**体积密集预测**，可对物体内部每个体素进行属性估计，且适用于网格、SDF、NeRF、高斯泼溅等多种 3D 表示。



## 核心方法与创新机理

VoMP 的核心创新在于将**材料物理有效性**与**对象几何表示**彻底解耦，从而将体积力学属性预测从一个需要逐对象优化的逆问题，转化为一个可训练的前馈学习问题。这一范式转变通过三个相互咬合的设计实现，直接回应了现有方法的两大瓶颈：物理无效输出与高昂的推理成本。

### 1. 物理有效材料潜在空间：MatVAE

现有方法（如 NeRF2Physics、PUGS）直接在输出空间预测力学参数，缺乏对预测值物理合理性的约束，可能产生偏离真实世界材料分布的结果。VoMP 首次引入了一个专门针对力学属性三元组 $(E, \nu, \rho)$ 的变分自编码器 MatVAE，在真实世界材料数据库 MTD（含 100,562 条记录）上训练，将所有合法材料映射到一个 2D 潜在流形上。

MatVAE 的设计并非标准 VAE 的简单套用，其损失函数集成了多项结构化约束：

$$
\mathcal{L}_{\mathrm{MatVAE}} = \mathcal{L}_{\mathrm{Recon}} + \gamma \cdot \mathrm{MI}(z) + \beta \cdot \mathrm{TC}(z) + \alpha \cdot \sum_{j=1}^{d} \max(\delta, \mathrm{KL}(q_{\phi}(z_j) \mid\mid p(z_j)))
$$

其中，互信息项 $\mathrm{MI}(z)$ 和总相关性惩罚 $\mathrm{TC}(z)$ 促进潜在维度的解耦，逐维容量约束则防止后验坍塌。消融实验证实，这一设计在重建精度和分布匹配上均优于标准 VAE（Table 7）。更重要的是，MatVAE 的潜在空间展现出**平滑性**和**可插值性**——在潜在空间中插值产生的材料始终落在真实材料范围内，而直接在 $(E, \nu, \rho)$ 空间中插值则频繁产生无效值（Figure 7c-d）。这确保了 VoMP 输出的每一个体素属性都天然落在物理有效的流形内。

### 2. 前馈体积预测范式

预测范式的变更（从“每对象优化”到“一次前向传播”）是 VoMP 速度优势的根源。**NeRF2Physics**（Zhai et al., 2024）需为每个对象优化特征场，平均耗时 1454.55 秒；**PUGS**（Shuai et al., 2025）通过 3D 高斯优化预测材料，耗时 1058.33 秒；而 VoMP 仅需 3.59 秒即可完成预测（Table 1），加速比达 5–400 倍。这一量级差异源于 VoMP 是唯一的前馈模型，无需运行时迭代。

范式变更的可行性建立在 MatVAE 提供的稳定预测目标之上。Geometry Transformer 的输出并非直接回归 $(E, \nu, \rho)$，而是预测 MatVAE 潜在空间中的编码 $z$，再由冻结的 MatVAE 解码器映射到属性空间。训练损失在属性空间中计算，但梯度通过解码器反传，使 Transformer 学会在物理有效流形上定位最匹配的潜在代码：

$$
\mathcal{L}_{\mathbf{F}} = \frac{1}{|\mathcal{S}|} \sum_{i \in \mathcal{S}} \| \mu_{\boldsymbol{\theta}}(\mathbf{F}(\mathbf{X}_{\mathcal{S}})_i) - ((E_i, \nu_i, \rho_i)^N)^{\mathsf{T}} \|_2^2
$$

### 3. 表示无关的体积预测

现有方法多聚焦于物体表面或特定表示：NeRF2Physics 依赖 NeRF 特征场，PUGS 绑定 3D 高斯泼溅，**Phys4DGen\***（Lin et al., 2025a）仅通过 VLM 为对象部件标注粗糙材料标签。VoMP 通过统一的三阶段体素化策略（椭球体素化→深度图雕刻→抖动采样），将网格、SDF、NeRF 和高斯泼溅均转化为体素网格，再通过多视角 DINOv2 特征聚合为每个体素赋予语义感知的视觉特征：

$$
\mathbf{f}_i = \operatorname{Average}(\mathcal{C}_i = \{ \mathcal{F}_j(\Pi_j(\mathbf{p}_i)) \mid j \in J \}) \in \mathbb{R}^{1024}
$$

这一设计使 VoMP 能够对物体**内部体素**进行密集预测，而非仅估计表面属性。消融实验表明，移除 MatVAE 直接预测 $\mathbb{R}^3$ 向量会导致杨氏模量 ALDE 从 0.3765 升高至 1.1284，密度误差大幅增加（Table 8），证实了材料潜在空间对体积预测质量的关键支撑作用。

### 创新总结

| 变更维度 | 基线方法特征 | VoMP 方案 | 证据锚点 |
|---------|------------|----------|---------|
| 预测范式 | 每对象优化（特征场/VLM） | 训练好的前馈模型，单次前向传播 | §1, Table 1 |
| 输出物理有效性 | 无保证，可能偏离真实材料范围 | MatVAE 潜在空间保证预测值落在真实材料分布内 | §3, Figure 7 |
| 体积预测能力 | 主要关注表面或稀疏采样点 | 对物体内部体素进行密集预测 | §4.1, Figure 3 |
| 适用表示多样性 | 局限于特定表示（NeRF/高斯泼溅） | 适用于任意可体素化并渲染的表示 | §1, Figure 1 |



![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2510_22975/figures/003_Figure_3.jpg]]
*Figure 3: VoMP Overview. For any input geometry, we aggregate multi-view DINOv2 features across its volumetric voxelization (§4.1). A trained GeometryTransformer (§4.2) predicts per-voxel material latents, decoded by MatVAE (§3) into mechanical properties ( E , $\nu , \rho$ )

VoMP 的整体流水线围绕一个核心洞察构建：**将材料物理有效性与对象几何解耦**，从而将体积材料预测转化为在预训练材料潜在空间中的前馈学习问题。如图 3 所示，系统由三个紧密协作的模块串联而成，形成端到端的前馈推理链路。

### 输入与输出流

对于任意输入的 3D 资产——无论是网格、符号距离函数（SDF）、NeRF 或 3D 高斯泼溅——VoMP 首先对其进行体素化，然后输出该物体内部每个体素的物理有效力学属性三元组：杨氏模量 $E$、泊松比 $\nu$ 和密度 $\rho$。整个预测过程仅需约 **3.59 秒**，相较于需要每对象优化的基线方法（NeRF2Physics 约 1454 秒，PUGS 约 1058 秒）实现了 5–400 倍的加速（Table 1）。

### 三阶段流水线

**阶段一：多视角 DINOv2 特征聚合（§4.1）**

给定体素化后的物体，VoMP 从多个预定义视角渲染图像，并使用 DINOv2 提取密集视觉特征。对于每个体素中心点 $\mathbf{p}_i$，将其投影到各视角图像平面，提取对应位置的 DINOv2 特征向量，然后取多视角特征的平均值作为该体素的聚合特征：

$$\mathbf{f}_i = \operatorname{Average}(\mathcal{C}_i = \{ \mathcal{F}_j(\Pi_j(\mathbf{p}_i)) \mid j \in J \}) \in \mathbb{R}^{1024}$$

这一步骤将 2D 视觉信息提升到 3D 体积空间，为每个体素编码了丰富的视觉上下文，是后续材料推理的感知基础。

**阶段二：Geometry Transformer（§4.2）**

聚合后的体素特征被送入一个基于 TRELLIS 结构的前馈变换器。该变换器采用 3D 移位窗口注意力机制，在体积空间中建模体素间的长程依赖关系，将体素化的图像特征映射到材料潜在代码 $\mathbf{z} \in \mathbb{R}^2$。训练时使用冻结的 MatVAE 解码器将潜在代码映射到属性空间，以均方误差监督：

$$\mathcal{L}_{\mathbf{F}} = \frac{1}{|\mathcal{S}|} \sum_{i \in \mathcal{S}} \| \mu_{\boldsymbol{\theta}}(\mathbf{F}(\mathbf{X}_{\mathcal{S}})_i) - ((E_i, \nu_i, \rho_i)^N)^{\mathsf{T}} \|_2^2$$

对于体素数量超过预设上限的大型资产，采用随机采样策略，每个训练周期随机选取固定数量的体素子集参与训练，以兼顾计算效率与覆盖完整性。

**阶段三：MatVAE 解码器（§3）**

Geometry Transformer 输出的 2D 潜在代码被送入预训练好的 MatVAE 解码器。MatVAE 是一个在真实世界材料三元组数据集（MTD，包含 100,562 条记录）上训练的变分自编码器，其核心作用是**保证解码出的力学属性始终落在物理有效的流形内**。解码器将潜在代码映射为归一化后的 $(E, \nu, \rho)^N$，再通过逆归一化还原为原始物理量纲的属性值。

### 关键设计决策

流水线中有两个关键的设计选择直接决定了 VoMP 的性能优势：

1. **材料潜在空间的预训练与冻结**：MatVAE 在训练 Geometry Transformer 之前独立训练，且在后续阶段保持冻结。这种解耦设计使得变换器只需学习“视觉特征→材料潜在代码”的映射，而不必同时学习材料本身的物理约束。消融实验（Table 8）证实，移除 MatVAE 直接预测 $\mathbb{R}^3$ 向量会导致杨氏模量 ALDE 从 0.3765 显著升高至 1.1284。

2. **表示无关的体素化抽象**：无论输入是网格、SDF 还是高斯泼溅，VoMP 统一将其体素化为规则网格后进行特征聚合。这使得同一模型可以泛化到多种 3D 表示，测试中体素化仅需约 31 毫秒（Table 1），不构成推理瓶颈。

### 训练数据标注的闭环

为训练 Geometry Transformer，VoMP 构建了 GVM 数据集（§5.2），其标注流程（Figure 4）结合了 3D 部件标签与视觉语言模型（VLM）。VLM 接收物体渲染图、部件材质映射球、材质名称以及 MTD 中最接近的三类真实材料范围作为提示，输出每个部件的材料三元组。这一流程将真实材料数据库的物理约束注入到标注过程中，降低了纯 VLM 标注的物理不合理性。



### 3.1 MatVAE：材料属性潜在空间

VoMP 的核心创新之一是将物理有效的材料属性约束嵌入到一个预训练的变分自编码器（MatVAE）中。该模块将力学属性预测问题从无约束的三维回归转化为在真实材料流形内的潜在代码预测。

**训练数据与归一化**：MatVAE 在 MTD（Material Triplet Dataset）上训练，该数据集包含 100,562 个真实世界材料的 $(E, \nu, \rho)$ 三元组。为处理杨氏模量和密度跨越多个数量级的问题，采用对数归一化策略：$E$ 和 $\rho$ 先取 $\log_{10}$，再线性缩放到 $[0,1]$；泊松比 $\nu$ 直接归一化到 $[0,1]$。

**重建损失**：MatVAE 的核心目标是学习一个 2 维潜在空间 $\mathbf{z} \in \mathbb{R}^2$，使得解码器能忠实地重建输入材料属性。重建损失定义为归一化后输入与重建值之间的均方误差：

$$
\mathcal{L}_{\mathrm{Recon}} = \frac{1}{N} \sum_{i=1}^{N} \lVert ((E_i, \nu_i, \rho_i)^N)^{\top} - ((\hat{E}_i, \hat{\nu}_i, \hat{\rho}_i)^N)^{\top} \rVert_2^2
\tag{1}
$$

**完整目标函数**：为获得解耦良好且平滑的潜在空间，MatVAE 采用 β-VAE 框架的增强版本，引入互信息（MI）、总相关性（TC）惩罚和逐维容量约束：

$$
\mathcal{L}_{\mathrm{MatVAE}} = \mathcal{L}_{\mathrm{Recon}} + \gamma \cdot \mathrm{MI}(\mathbf{z}) + \beta \cdot \mathrm{TC}(\mathbf{z}) + \alpha \cdot \sum_{j=1}^{d} \max(\delta, \mathrm{KL}(q_{\phi}(z_j) \mid\mid p(z_j)))
\tag{2}
$$

其中 $\mathrm{MI}(\mathbf{z})$ 鼓励潜在变量与输入之间的互信息，$\mathrm{TC}(\mathbf{z})$ 惩罚潜在维度之间的总相关性以促进解耦，最后一项对每个维度 $j$ 的 KL 散度施加容量约束（阈值为 $\delta$），防止后验坍缩。

**潜在空间性质**：消融实验（Table 7）表明，上述设计使 MatVAE 在重建精度和分布匹配上均优于标准 VAE。定性分析（Figure 7）验证了该空间的四个关键性质：(a) 忠实重建、(b) 解码有效性（所有采样点均落在真实材料范围内）、(c) 平滑变化、(d) 可插值性——在潜在空间中插值产生的中间材料始终有效，而直接在 $(E, \nu, \rho)$ 空间中插值则可能产生无效值。

### 3.2 多视角特征聚合

VoMP 的输入是任意 3D 表示的体素化网格。对每个体素中心 $\mathbf{p}_i$，将其投影到 $J$ 个视图中，提取预训练 DINOv2 特征：

$$
\mathbf{f}_i = \operatorname{Average}(\mathcal{C}_i = \{ \mathcal{F}_j(\Pi_j(\mathbf{p}_i)) \mid j \in J \}) \in \mathbb{R}^{1024}
\tag{3}
$$

其中 $\Pi_j(\mathbf{p}_i)$ 将 3D 点投影到第 $j$ 个视图的图像坐标，$\mathcal{F}_j$ 为该视图的 DINOv2 特征图。对可见视图的特征取平均，得到每个体素的 1024 维聚合特征。消融实验（Table 8）证实 DINOv2 特征显著优于直接使用 RGB 颜色。

### 3.3 Geometry Transformer

VoMP 的主体是一个前馈 Transformer $\mathbf{F}$，将体素化的图像特征映射到材料潜在代码。该模块基于 TRELLIS 的编码器-解码器结构，采用 3D 移位窗口注意力机制处理体素序列。

**训练损失**：Transformer 预测每个体素的材料潜在代码，通过冻结的 MatVAE 解码器 $\mu_{\boldsymbol{\theta}}$ 映射到归一化的属性空间，与真值计算均方误差：

$$
\mathcal{L}_{\mathbf{F}} = \frac{1}{|\mathcal{S}|} \sum_{i \in \mathcal{S}} \| \mu_{\boldsymbol{\theta}}(\mathbf{F}(\mathbf{X}_{\mathcal{S}})_i) - ((E_i, \nu_i, \rho_i)^N)^{\mathsf{T}} \|_2^2
\tag{4}
$$

其中 $\mathcal{S}$ 为采样的体素子集。对于体素数量 $L > L_N$ 的大型资产，每个训练 epoch 开始时随机采样 $L_N$ 个体素，以处理可变尺寸输入。

**关键消融发现**（Table 8）：
- **移除 MatVAE**，直接预测 $\mathbb{R}^3$ 向量：杨氏模量 ALDE 从 0.3765 飙升至 1.1284，密度误差大幅增加，证实材料潜在空间对输出物理有效性的核心作用。
- **使用 L1 损失替代 L2 损失**：所有力学属性的误差增加 2-3 倍，表明 L2 损失对跨越数量级的属性预测更为合适。



## 实验与关键发现

### 核心性能：机械属性预测精度与效率

VoMP 在 GVM 测试集（公开子集）上对所有三项力学属性均实现了大幅领先的预测精度，同时将推理时间压缩至秒级。这种“精度-速度”双重优势源于其前馈预测范式与材料潜在空间约束的协同设计。

**杨氏模量预测**：VoMP 的绝对对数相对误差（ALRE）达到 **0.0409**，相比 NeRF2Physics 的 0.1346 和 PUGS 的 0.1688，误差降低了约 **70%–82%**（Table 2）。这一差距反映了体积预测与表面预测之间的根本性差异——NeRF2Physics 仅估计表面刚度，PUGS 通过 3D 高斯优化材料参数，两者均无法准确捕捉物体内部材料分布。Phys4DGen* 的 ALRE 高达 0.2227，进一步表明单纯依赖 VLM 标注粗糙材料标签的方法在定量精度上存在明显局限。


![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2510_22975/figures/007_Table_2.jpg]]
*Table 2: Mechanical Property Estimates of our method on the publicly released dataset are very close to the full dataset. Per-voxel error rate is first computed per object, then averaged across all objects in the test set to avoid weighing some objects more. Global voxel-level normalization yields similar results, see Supplement Tb. 3*

**泊松比与密度预测**：在泊松比上，VoMP 的平均相对误差（ARE）为 **0.0818**，较 Phys4DGen* 的 0.1467 降低约 **44%**。密度预测的差距更为悬殊——VoMP 的 ARE 为 **0.0921**，而 Phys4DGen* 和 NeRF2Physics 分别达到 1.4394 和 1.0365，误差降低约 **91%–94%**（Table 2）。密度预测的极端差距说明，未经物理约束的方法在面对跨越数个数量级的密度值时极易产生灾难性偏差，而 MatVAE 的潜在空间通过将预测限制在真实材料分布内，从根本上规避了这一问题。

**推理效率**：VoMP 完成一次预测的平均总耗时仅为 **3.59 秒**，而 NeRF2Physics 需要 1454.55 秒（约 24 分钟），PUGS 需要 1058.33 秒（约 18 分钟），Phys4DGen* 需要 51.65 秒（Table 1）。VoMP 的速度优势达到 **5–400 倍**，其根本原因在于它是所有对比方法中唯一的前馈模型——无需针对每个对象进行迭代优化，一次前向传播即可完成预测。Table 1 的耗时分解显示，体素化仅需 31 ms，多视角特征提取约 1.5 秒，Geometry Transformer 推理约 2 秒，整个流水线高度高效。


![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2510_22975/figures/006_Table_1.jpg]]
*Table 1: Wall-clock comparisons and breakdown*

### 定性分析：体积场的噪声与合理性

Figure 6a 的定性比较揭示了 VoMP 在体积材料场质量上的显著优势。通过颜色编码的力学属性场和切面可视化，VoMP 预测的体积场噪声明显低于所有基线方法。NeRF2Physics 和 PUGS 在物体内部常出现不连续的属性跳变，这与它们主要关注表面或稀疏采样点的设计局限一致。VoMP 的体素级密集预测配合 MatVAE 的平滑潜在空间，使得物体内部材料过渡自然、符合物理直觉。

### 消融实验：各组件的因果贡献

Table 8 的系统消融实验验证了 VoMP 各设计选择的必要性，每一项移除都导致性能的显著退化。

**MatVAE 的关键作用**：移除 MatVAE、直接预测 $\mathbb{R}^3$ 向量（即 $(E, \nu, \rho)$ 三元组）是最具破坏性的消融。杨氏模量的绝对对数偏差误差（ALDE）从 **0.3765** 飙升至 **1.1284**，密度误差同样大幅增加。这一结果直接证实了核心因果机制：无约束的回归空间无法保证预测值落在物理有效的流形内，而 MatVAE 的 2D 潜在空间通过编码真实材料分布的先验知识，强制输出符合物理规律的属性组合。

**损失函数选择**：将训练损失从 L2 替换为 L1 导致所有力学属性的误差增加 **2–3 倍**（Table 8）。这说明对于跨越多个数量级的属性（如杨氏模量和密度），L2 损失对离群值的惩罚特性有助于稳定训练并抑制极端偏差。

**视觉特征选择**：采用 DINOv2 或 CLIP 特征相比直接使用 RGB 颜色值，性能有显著提升（Table 8）。DINOv2 特征在捕捉材料视觉线索（如纹理、光泽、透明度）方面具有更强的语义表达能力，为 Geometry Transformer 提供了更丰富的感知基础。

**MatVAE 设计验证**：Table 7 显示，MatVAE 在重建精度和分布匹配指标上均优于标准 VAE。其采用的流式后验（flow-based posterior）、总相关性惩罚（TC）和逐维容量约束（dimension-wise capacity constraint）共同确保了潜在空间的组织性——Figure 7 展示了该空间具备忠实重建（a）、采样有效性（b）、平滑变化（c）和可插值性（d）四个理想属性。特别值得注意的是，在潜在空间中插值产生的中间材料始终落在真实材料范围内，而直接在 $(E, \nu, \rho)$ 空间插值则经常生成物理无效的组合（Figure 7d）。

### 数据标注质量与公平性说明

VoMP 的训练数据依赖 VLM 辅助标注，Table 9 报告了 VLM 标注的误差水平，表明标注存在一定噪声。然而，标注流程中引入了 MTD 真实材料数据库的引导——为 VLM 提供三个最接近真实材料的范围约束——有效抑制了幻觉式输出。Table 2 的注释明确指出，公开 GVM 数据集不包含植被子集，但验证表明公开子集上的误差与完整数据集非常接近（见 Supplement Table 3），确保了比较的公平性。所有运行时间测试在同一硬件（1×A100 GPU, 64 CPU）上进行，Phys4DGen* 基于公开提示尽力复现。

### 局限性与失败模式

尽管 VoMP 在核心指标上表现优异，但存在若干结构性局限。首先，方法当前**仅适用于各向同性材料**，无法处理木材、纤维增强复合材料等各向异性材质。其次，预测属性**仅限于杨氏模量、泊松比和密度**三项，未涵盖屈服强度、剪切模量、热膨胀系数等更广泛的工程参数。第三，训练数据标注仍依赖 VLM，标注噪声可能在某些材料类别上引入系统性偏差。第四，模型基于部分分割的网格训练，对**非分割形状或缺乏纹理的几何体**的泛化能力未经充分验证。最后，VoMP 输出的材料参数针对精确仿真器（如 FEM）设计，若直接用于快速但不精确的仿真器（如 XPBD），可能需要额外的参数映射或校准步骤——Figure 2 已展示了不同仿真器在相同材料参数下的行为差异，这一映射问题本身构成一个开放挑战。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2510_22975/figures/009_Table.jpg]]
*Table: (a) Qualitative Comparison: We show that qualitiative VoMP tends to provide less noisy volumetric? values compared to the baselines. We show the color coded fields and slice planes through the fields. (b) Mechanical Property Estimates of our method significantly outperform the baselines on all metrics. Pervoxel error rate is first computed per object, then averaged across all objects in the test set to avoid weighing some objects more. Global voxel-level normalization yields similar results, see Supplement Tb. 4. (d) Material Validity: We report mean values and relative errors (in %) with the closest physically measured material range in MTD (§5.1)*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2510_22975/figures/011_Figure.jpg]]
*Figure: (c) Encoding real materials results in smoothly varying E, ν, ρ values throughout the 2D latent space*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2510_22975/figures/014_Figure.jpg]]

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2510_22975/figures/024_Figure.jpg]]

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2510_22975/figures/048_Figure_18.jpg]]
*Figure 18: Gripping Force by Robots. We demonstrate the relation between relative errors in materials and relative change in P.E. (top) and volume (bottom). We then show the confidence bounds in light shaded regions. inertial component $\begin{array} { r } { E _ { \mathrm { i n e r t i a } } = \int _ { \Omega } \frac { \rho } { 2 \Delta t ^ { 2 } } | \mathbf u ^ { n + 1 } - \mathbf u ^ { n } | ^ { 2 } d V } \end{array}$ that captures displacement changes between iterations in our quasi-static solver, a gravitational potential $\begin{array} { r } { E _ { \mathrm { g r a v i t y } } = - \int _ { \Omega } \rho \mathbf { u } \cdot \mathbf { g } d V } \end{array}$ accounting for body forces, and an external w...

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2510_22975/figures/049_Figure_19.jpg]]
*Figure 19: Impact Force on Dropping Objects. We demonstrate the relation between relative errors in materials and relative change in P.E. (top) and volume (bottom). We show the confidence bounds in light shaded regions*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2510_22975/figures/050_Figure_20.jpg]]
*Figure 20: Tensile Testing Machine. We demonstrate the relation between relative errors in materials and relative change in P.E. (top) and volume (bottom). We show the confidence bounds in light shaded regions. E.1 ANNOTATION WITH VISION-LANGUAGE MODEL*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2510_22975/figures/051_Figure_21.jpg]]
*Figure 21: Tension. We demonstrate the relation between relative errors in materials and relative change in P.E. (top) and volume (bottom). We show the confidence bounds in light shaded regions*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2510_22975/figures/060_Table_14.jpg]]
*Table 14: Training Hyperparameters. We show the hyperparameters for the MatVAE and Geometry Transformer*




## 定位与知识库关联

### 问题瓶颈与核心因果调控

现有方法在预测物体体积力学属性时面临两个根本瓶颈：**物理有效性缺失**与**推理效率低下**。NeRF2Physics（Zhai et al., 2024）需要针对每个对象进行耗时约24分钟的特征场优化，且仅输出表面刚度；PUGS（Shuai et al., 2025）通过3D高斯优化预测材料和密度，单对象仍需约18分钟；Phys4DGen\*（Lin et al., 2025a）直接使用VLM为对象部件标注粗糙材料标签，无需优化但预测精度最低。这些方法均无法保证输出值落在真实材料的物理有效范围内，且主要关注表面或稀疏采样点，难以支撑精确的体积仿真。

VoMP的因果调控核心在于**将材料有效性与对象几何解耦**。通过引入基于真实世界材料数据库训练的变分自编码器MatVAE，将杨氏模量$E$、泊松比$\nu$和密度$\rho$三元组映射到一个2D潜在空间，确保所有预测的材料值落在物理有效的流形内。这一设计将体积材料预测转化为在预训练材料潜在空间中的前馈学习问题，从而在3.59秒内即可生成可用于精确仿真器的体积属性场。

### 与基线方法的范式差异

| 方法 | 预测范式 | 物理有效性保证 | 体积预测能力 | 表示适用性 |
|------|----------|----------------|-------------|-----------|
| **NeRF2Physics** (Zhai et al., 2024) | 每对象优化 | 无保证 | 表面为主 | NeRF |
| **PUGS** (Shuai et al., 2025) | 每对象优化 | 无保证 | 稀疏采样点 | 高斯泼溅 |
| **Phys4DGen\*** (Lin et al., 2025a) | 运行时VLM推理 | 粗糙材料标签 | 部件级 | 通用 |
| **Pixie** (Le et al., 2025，并发工作) | 基于NeRF密度过滤 | 表面偏置 | 表面偏置 | NeRF |
| **VoMP** (本文) | 训练好的前馈模型 | MatVAE潜在空间约束 | 密集体素预测 | 任意可体素化表示 |

VoMP是首个训练好的前馈模型，一次前向传播即可完成预测，无需任何每对象优化。其MatVAE潜在空间（在包含100,562个真实材料三元组的MTD数据集上训练）保证了预测值始终落在真实材料分布内，而非常规方法可能产生的物理上不可能的组合。此外，VoMP适用于任何可体素化并渲染的表示（网格、SDF、NeRF、高斯泼溅），突破了以往方法对特定表示的局限。

### 流水线模块与知识来源

VoMP的推理流水线由三个模块串联构成：

1. **多视角DINOv2特征聚合**（§4.1）：将多视角图像特征提升到三维体素，为每个体积元素编码视觉信息。这一设计借鉴了近期多视角特征提升工作的思路（Wang et al., 2023; Dutt et al., 2024; Xiang et al., 2025），但将其适配到材料属性预测的场景。

2. **Geometry Transformer**（§4.2）：基于TRELLIS（Xiang et al., 2025）的编码器-解码器结构，采用3D移位窗口注意力机制，将体素特征映射到材料潜在代码。该模块继承TRELLIS的预训练权重，并在GVM数据集上进行微调。

3. **MatVAE解码器**（§3）：将潜在代码解码为物理有效的力学属性三元组$(E, \nu, \rho)$。MatVAE采用改进的VAE架构，包含流式后验、总相关性惩罚和逐维容量约束，在重建精度和分布质量上均优于标准VAE（见Table 7）。

### 适用边界与已知局限

**当前适用范围**：
- 输入：任意可体素化并渲染的3D表示（网格、SDF、NeRF、高斯泼溅）
- 输出：各向同性材料的杨氏模量、泊松比和密度
- 适用仿真器：精确仿真器（如FEM），若用于快速但不精确的仿真器（如XPBD）可能需要额外校准

**明确局限**：
1. **各向同性限制**：当前仅适用于各向同性材料，无法处理各向异性材料属性。
2. **参数范围有限**：预测的属性仅限于$E, \nu, \rho$三元组，未涵盖屈服强度、剪切模量、热膨胀等更广泛的工程参数。
3. **标注噪声**：训练数据标注仍依赖VLM，尽管引入了真实材料库作为引导，标注可能仍存在噪声（VLM标注误差见Table 9）。
4. **泛化边界未知**：模型训练基于部分分割的网格，对非分割形状或缺乏纹理的几何体泛化能力未知。

### 开放问题

1. **各向异性扩展**：如何将方法扩展到预测各向异性材料属性和更多力学参数？
2. **物理观测融合**：能否结合物理观测（如视频或力反馈）进一步微调或自监督训练，提高预测准确性？
3. **仿真器参数映射**：如何将学习到的真实材料参数自动映射到基于位置动力学（XPBD）等快速仿真器的可调参数，以保持仿真效率？
4. **零样本泛化**：在无监督或零样本场景下，对未见过的物质类别（如复合材料、生物组织）的预测性能如何？

### 证据强度说明

- **定量优势证据充分**：Table 2显示VoMP在GVM测试集上的杨氏模量ALRE达到0.0409，远低于NeRF2Physics的0.1346和PUGS的0.1688；密度ARE为0.0921，较Phys4DGen\*的1.4394降低约94%。Table 1证实推理时间仅3.59秒，较优化类方法快5-400倍。
- **消融实验支撑核心设计**：Table 8表明移除MatVAE会导致杨氏模量ALDE从0.3765升高到1.1284，密度误差大幅增加，证实材料潜在空间的关键作用。
- **定性证据需结合原文判断**：Figure 6a的定性比较显示VoMP预测的体积材料场噪声更低，但具体视觉差异需读者自行评估。
- **泛化性证据有限**：对非分割形状或缺乏纹理几何体的泛化能力尚未经过系统验证，该点需手动核实。



## 原文 PDF

![[paperPDFs/ICLR_2026/VoMP_Predicting_Volumetric_Mechanical_Property_Fields.pdf]]
