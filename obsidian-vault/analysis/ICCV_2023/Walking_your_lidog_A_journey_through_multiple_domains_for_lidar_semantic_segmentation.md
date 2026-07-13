---
title: "Walking your lidog: A journey through multiple domains for lidar semantic segmentation"
type: paper
paper_level: A
venue: ICCV
year: 2023
pdf_ref: paperPDFs/ICCV_2023/Walking_your_lidog_A_journey_through_multiple_domains_for_lidar_semantic_segmentation.pdf
code_link: null
project_link: https://saltoricristiano.github.io/lidog/
aliases:
- WYLJTMDLSS
tags:
- ICCV_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "在3D稀疏卷积编码器-解码器网络基础上附加一个密集2D鸟瞰图（BEV）语义分割的辅助训练任务，通过将3D特征沿高度轴投影为BEV特征并同时优化3D和BEV损失，强制骨干网络学习对传感器配置、扫描分辨率和场景几何变化鲁棒的特征表示。"
primary_logic: "不同域的LiDAR点云在鸟瞰视角下几何外观更相似，这种投影能降低传感器采样模式带来的差异；利用BEV语义布局作为辅助监督信号可以有效正则化3D骨干网络，使其提取的特征具有跨域不变性，从而显著提升域泛化能力。"
claims:
- "在Synth4D-KITTI→Real的单源域泛化实验中，LiDOG在SemanticKITTI上达到44.18 mIoU，相比源域模型提升+19.49 mIoU，在nuScenes上提升+16.52 mIoU，全面超越所有基线方法。"
- "在真实域→真实域的SemanticKITTI→nuScenes方向上，LiDOG获得34.88 mIoU，提升+8.35 mIoU，优于所有对比方法。"
- "特征可视化显示，加入BEV辅助任务后，不同域的道路类别点嵌入在t-SNE空间中更为对齐，表明BEV任务有效减小了域间特征分布差异。"
- "消融实验中，用额外的3D分割头替换BEV辅助分支（Double）得到的性能低于LiDOG，证明BEV特定投影和预测任务对泛化能力的贡献超过简单的多解码器集成。"
---

# Walking your lidog: A journey through multiple domains for lidar semantic segmentation

> [!tip] 核心洞察
> 不同域的LiDAR点云在鸟瞰视角下几何外观更相似，这种投影能降低传感器采样模式带来的差异；利用BEV语义布局作为辅助监督信号可以有效正则化3D骨干网络，使其提取的特征具有跨域不变性，从而显著提升域泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Walking Your LiDOG：跨域LiDAR语义分割之旅 |
| 英文题名 | Walking your lidog: A journey through multiple domains for lidar semantic segmentation |
| 会议/期刊 | ICCV 2023 |
| Links | [paper](https://arxiv.org/abs/2304.11705) · [Project](https://saltoricristiano.github.io/lidog/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | LiDOG |
| Dataset | Synth4D-KITTI → SemanticKITTI (单源), Synth4D-KITTI → nuScenes (单源), (Synth4D-KITTI+Synth4D-nuScenes) → SemanticKITTI (多源), (Synth4D-KITTI+Synth4D-nuScenes) → nuScenes (多源) |

> [!tip] 效果简介
> - Synth4D-KITTI → SemanticKITTI (单源) 上，mIoU 为 44.18，对比 24.69 (Source)，变化 +19.49。
> - Synth4D-KITTI → nuScenes (单源) 上，mIoU 为 37.14，对比 20.62 (Source)，变化 +16.52。
> - (Synth4D-KITTI+Synth4D-nuScenes) → SemanticKITTI (多源) 上，mIoU 为 42.44，对比 31.82 (Source)，变化 +10.62。

## 概要

LiDAR语义分割在自动驾驶、机器人导航等安全关键应用中扮演核心角色，但现有方法通常假设训练与测试数据来自同一分布。当传感器类型（如Velodyne 64线束 vs 32线束）、扫描点密度、地理环境或道路布局发生变化时，模型性能急剧下降——例如，在SemanticKITTI上训练的模型在nuScenes上评估时，mIoU从48.49骤降至26.53，降幅约22个百分点。这种**域偏移**是LiDAR语义分割从实验室走向真实部署的核心瓶颈。

针对这一挑战，本文提出**LiDOG**，一种面向LiDAR语义分割域泛化（DG-LSS）的简洁而有效的方法。其核心洞察在于：尽管不同域的LiDAR点云在3D空间中的采样模式差异显著，但它们在**鸟瞰图（BEV）**视角下的几何外观更为相似（Figure 3）。基于此，LiDOG在标准3D稀疏卷积编码器-解码器网络上附加一个密集2D BEV语义分割辅助任务：将3D解码器特征沿高度轴投影为BEV特征，并通过若干2D卷积层预测BEV语义布局，联合优化3D Dice损失与BEV Dice损失。这一辅助任务强制骨干网络学习对传感器配置和扫描分辨率变化鲁棒的特征表示，从而显著提升跨域泛化能力。

**主要结果**：在合成域到真实域（Synth4D-KITTI → SemanticKITTI/nuScenes）的单源域泛化实验中，LiDOG分别达到44.18 mIoU和37.14 mIoU，较源域模型提升+19.49和+16.52 mIoU，全面超越Mix3D、CoSMix、IBN等数据增强与域泛化基线（Table 1）。在真实域到真实域（SemanticKITTI → nuScenes）方向，LiDOG获得34.88 mIoU，提升+8.35 mIoU（Table 3）。特征可视化（Figure 4）进一步证实，BEV辅助任务有效缩小了不同域间道路类别的特征分布差异。消融实验表明，BEV特定投影与监督任务对泛化能力的贡献显著优于简单添加额外3D分割头（Figure 6）。



### 问题定义：LiDAR语义分割的域泛化

LiDAR语义分割是自动驾驶与机器人感知的核心任务，其目标是为点云中的每个点赋予语义类别标签。现有方法通常在单一域内进行训练和评估，即训练集和测试集来自相同的数据分布。然而，实际部署中，模型需要面对与训练数据截然不同的目标域——不同的传感器类型（如Velodyne 64线束 vs 32线束）、不同的扫描点密度、不同的地理环境与道路布局。这些域偏移导致模型性能急剧下降，例如，仅在SemanticKITTI上训练的模型迁移到nuScenes时，mIoU从域内的48.49骤降至26.53，降幅约22个百分点。这一现象揭示了LiDAR语义分割模型在跨域条件下的脆弱性，也催生了LiDAR语义分割域泛化（Domain Generalization for LiDAR Semantic Segmentation, DG-LSS）这一新问题设定：模型仅在源域数据上训练，无需访问目标域数据，却需要在目标域上取得良好的分割性能。

### 现有方法的缺口

当前应对域偏移的技术路线大致可分为三类，但均存在明显局限：

- **数据增强方法**：如**Mix3D**（Nekrasov et al., 3DV 2021）、**PointCutMix**（Zhang et al., Neurocomputing 2022）和**CoSMix**（Saltori et al., ECCV 2022），通过在源域点云上进行场景拼接或局部补丁混合来增加训练多样性。这类方法虽然能提升源域内的鲁棒性，但并未显式建模域间差异，对传感器采样模式、点密度等结构性域偏移的缓解能力有限。

- **2D域泛化技术迁移**：如**IBN**（Pan et al., ECCV 2018）和**RobustNet**（Choi et al., ECCV 2021），通过在网络中结合批次归一化与实例归一化来学习外观不变特征。这些方法最初为2D图像域泛化设计，直接应用于稀疏3D点云时，难以充分利用点云的几何结构信息。

- **弱监督域自适应方法**：如**SN**（Wang et al., CVPR 2020）利用源域和目标域的平均车辆尺寸知识对源实例进行重缩放，**RayCast**（Langer et al., IROS 2020）通过光线投射模拟目标域传感器采样模式。这类方法需要目标域的先验统计信息（如物体尺寸），在严格的域泛化设定下（目标域完全不可见）不适用。

综上，现有方法缺乏一种专门针对LiDAR点云域泛化的机制，能够在无需目标域任何信息的前提下，强制模型学习对传感器配置、扫描分辨率和场景几何变化鲁棒的特征表示。

### 核心动机：鸟瞰视角的域不变性

不同域的LiDAR点云虽然在3D空间中的点分布、密度和采样模式差异显著，但在鸟瞰视角（Bird's-Eye View, BEV）下，其几何外观更为相似。Figure 3直观展示了这一现象：SemanticKITTI和nuScenes的原始点云差异明显，但投影为BEV图像后，道路、建筑物等语义布局呈现出高度一致的几何结构。这一观察揭示了BEV语义布局作为跨域不变表征的潜力——如果模型能够在BEV视角下准确预测语义布局，其3D骨干网络将被迫提取对域偏移不敏感的特征。

基于这一洞察，本文提出**LiDOG**，通过在3D稀疏卷积编码器-解码器网络上附加一个密集2D BEV语义分割的辅助训练任务，将3D特征沿高度轴投影为BEV特征并同时优化3D和BEV损失。这一设计使BEV语义布局作为辅助监督信号，正则化3D骨干网络，从而在不引入目标域信息的前提下，显著提升模型的跨域泛化能力。



## 核心方法与创新机理

LiDOG 的核心创新在于为 3D 稀疏卷积语义分割网络引入一个**密集 2D 鸟瞰图（BEV）语义预测辅助任务**，通过联合优化 3D 和 BEV 损失来强制骨干网络学习对域偏移鲁棒的特征表示。这一设计基于一个关键的几何直觉：不同域的 LiDAR 点云在鸟瞰视角下几何外观更相似（Figure 3），这种投影能有效降低传感器采样模式、扫描分辨率和场景布局带来的差异，使 BEV 语义布局成为天然的跨域不变监督信号。

### 关键设计变更

与标准 3D 语义分割基线相比，LiDOG 引入了三个相互关联的架构与训练变更：

1. **辅助分支结构**：在原有 3D 稀疏分割头之外，新增一个密集 2D BEV 解码器。具体而言，将 3D 编码器-解码器输出的稀疏体素特征 $F^{3D}$ 沿高度轴投影为密集 BEV 特征 $F^{BEV}$，再通过若干 2D 卷积层预测 BEV 语义布局。这一分支仅在训练时存在，推理时完全移除，不增加部署开销。

2. **损失函数**：将训练目标从单一的 3D 分割损失扩展为 3D 与 BEV 损失的均值联合优化：
   $$L_{tot} = \frac{1}{2} (L^{BEV} + L^{3D})$$
   其中 $L^{BEV}$ 和 $L^{3D}$ 均为 Dice 损失，分别作用于 BEV 语义预测和 3D 稀疏语义预测。这种对称设计确保两个任务对特征学习施加同等的梯度压力。

3. **特征监督机制**：基线方法仅对 3D 俯视稀疏特征施加语义监督，而 LiDOG 额外对投影后的密集 BEV 特征施加语义监督。这种双重监督促使 3D 骨干网络在提取体素特征时，隐式地编码与视角无关的语义结构信息。

### BEV 辅助任务的独特作用

消融实验（Figure 6）提供了关键证据：用额外的 3D 分割头替换 BEV 分支（Double 配置）得到的泛化性能低于 LiDOG，说明**性能增益源于 BEV 特定的投影和预测任务，而非简单的多解码器集成效果**。这一发现揭示了核心因果机制——BEV 投影本身作为一种结构化正则化手段，将 3D 特征映射到对传感器配置不敏感的表示空间，从而缩小域间特征分布差异。t-SNE 可视化（Figure 4）进一步证实了这一机制：加入 BEV 辅助任务后，不同域的道路类别点嵌入在特征空间中更为对齐。

### 与现有方法的本质区别

现有域泛化方法主要依赖数据增强（如 Mix3D、PointCutMix、CoSMix）或域对齐技术（如 IBN、RobustNet），这些方法要么在输入空间进行操作，要么仅调整归一化统计量。LiDOG 的创新在于**从表示空间的结构出发**，利用 BEV 视角的几何一致性作为归纳偏置，使模型在训练过程中主动学习域不变特征。这种设计无需目标域数据、无需域标签，也不依赖任何域间对应关系，是一种纯源域训练的域泛化方法。



LiDOG 的整体设计围绕一个核心思想展开：在标准的 3D 稀疏卷积语义分割网络上，附加一个密集的 2D 鸟瞰图（BEV）语义预测辅助任务，通过联合优化 3D 与 BEV 损失，强制骨干网络学习对传感器配置、扫描分辨率和场景几何变化具有鲁棒性的特征表示。

### 输入与 3D 体素化

输入的 LiDAR 点云 $P_j$ 首先被量化为一个 3D 占用网格（体素网格）$V_j$，同一体素内的点被合并处理。这一体素化步骤将无序点云转换为规则的 3D 网格表示，为后续稀疏卷积操作奠定基础。

### 3D 编码器-解码器骨干（$g^{3D}$）

体素化后的 3D 占用网格进入基于 MinkowskiNet 的稀疏 3D 卷积编码器-解码器网络。编码器通过一系列稀疏 3D 卷积下采样层学习紧凑的 3D 表示，解码器则通过稀疏卷积上采样层将特征恢复至原始分辨率，最终输出稀疏 3D 体素特征 $F^{3D}$。所有层均采用稀疏批归一化（sparse batch-normalization）。

### 主任务分支：稀疏 3D 分割头（$h^{3D}$）

在 3D 骨干之上，稀疏 3D 分割头 $h^{3D}$ 对每个被占用的体素特征进行逐体素分类，经 softmax 激活后输出 3D 语义类别后验分布：

$$\tilde{\mathcal{V}_j^{3D}} = p(\mathcal{K} | V_j) = \sigma(h^{3D}(F_j^{3D}))$$

该分支构成模型的主任务，负责输出最终的 3D 点云语义分割结果。

### 辅助任务分支：稀疏到密集的 BEV 投影与 2D 解码器

这是 LiDOG 的核心创新模块。训练阶段，3D 解码器输出的稀疏体素特征 $F^{3D}$ 被沿高度轴投影到 2D 鸟瞰平面，生成密集的 BEV 特征 $F^{BEV}$。投影过程将每个体素中心坐标 $(x_i, z_i)$ 按量化步长 $x_q, z_q$ 映射到 BEV 网格：

$$q(x_i, z_i) = (x_i^{BEV}, z_i^{BEV}) = \Big( \Big\lfloor \frac{x_i}{x_q} \Big\rfloor, \Big\lfloor \frac{z_i}{z_q} \Big\rfloor \Big)$$

仅保留投影范围内的特征，其余区域置零。随后，一个由若干 2D 卷积层构成的密集 BEV 解码器 $h^{BEV}$ 处理 $F^{BEV}$，预测密集的 BEV 语义布局。

### 联合训练与损失函数

模型在训练时同时优化两个分支的 Dice 损失，总损失为二者的均值：

$$L_{tot} = \frac{1}{2} (L^{BEV} + L^{3D})$$

这种联合优化机制使得 3D 骨干网络在提取稀疏体素特征时，必须同时满足两个任务的需求：既要支持精确的 3D 分割，又要保证投影后的 BEV 特征能够准确还原场景的俯视语义布局。由于不同域的 LiDAR 点云在鸟瞰视角下几何外观更为相似（如 Figure 3 所示），BEV 辅助监督作为一种隐式正则化，能够有效减小域间特征分布差异，从而提升模型的域泛化能力。推理阶段，BEV 辅助分支被移除，仅保留 3D 骨干和分割头，不引入额外计算开销。

### 模块间数据流关系

整体数据流可概括为：**点云 → 3D 体素化 → 稀疏 3D 编码器-解码器 → {稀疏 3D 分割头, BEV 投影 → 密集 2D 解码器} → 联合损失优化**。其中，3D 骨干是信息瓶颈，BEV 投影充当域不变特征学习的“正则化器”，而两个解码头分别提供 3D 视角和鸟瞰视角的语义监督信号。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2304_11705/figures/002_Figure_2.jpg]]
*Figure 2: LiDOG overview. We encode our input LiDAR scan $P _ { j }$ using the 3D backbone $g ^ { 3 D }$ to learn the occupied voxels’ feature representations $F ^ { 3 D }$ . (Upper branch - main task) We apply a sparse segmentation head on $F ^ { 3 D }$ and supervise with 3D semantic labels, $\mathcal { V } _ { j } ^ { 3 D }$ . (Lower branch - auxiliary task) We project those features along the height-axis to obtain a dense 2D bird’s-eye (BEV) view features $F ^ { B E V }$ , and apply several 2D convolutional layers to learn the 2D BEV representation. We supervise the BEV auxiliary task by using BEV-view of semantic labels, $\mathcal { V } _ { j } ^ { B E \bar { V } }$ . We train jointly on both $\dot { L ^ { 3 D...$



LiDOG的整体架构围绕一个核心假设展开：不同域的LiDAR点云在鸟瞰视角（BEV）下的几何外观比原始3D点云更相似（Figure 3）。基于此，方法在标准3D稀疏卷积编码器-解码器网络之上，附加了一个密集2D BEV语义预测的辅助训练任务，通过联合优化迫使3D骨干网络学习跨域不变的特征表示。以下按流水线模块逐一说明。

### 3D体素化与稀疏骨干网络（g³ᴰ）

输入LiDAR点云 $P_j$ 首先被量化为3D占用网格 $V_j$，同一体素内的点被合并。随后，基于MinkowskiNet的稀疏3D卷积编码器-解码器网络 $g^{3D}$ 对非空体素进行多尺度特征提取，输出稀疏体素特征 $F^{3D}_j$。编码器通过一系列稀疏3D卷积下采样层学习紧凑的3D表示，解码器则以稀疏卷积上采样层将特征恢复至原始分辨率，层间采用稀疏批归一化。

### 稀疏3D分割头（h³ᴰ）

主任务分支对每个体素特征 $F^{3D}_j$ 应用稀疏分割头 $h^{3D}$，经softmax激活后输出体素级语义类别后验分布：

$$\tilde{\mathcal{V}}_j^{3D} = p(\mathcal{K} \mid V_j) = \sigma(h^{3D}(F_j^{3D}))$$

其中 $\mathcal{K}$ 为语义类别集合，$\sigma$ 为softmax函数。该分支的监督信号来自3D语义标签 $\mathcal{V}_j^{3D}$。

### 稀疏到密集BEV投影

这是LiDOG方法的关键操作。将3D解码器输出的稀疏体素特征 $F^{3D}$ 沿高度轴投影到2D BEV平面，得到密集BEV特征 $F^{BEV}$。具体而言，对每个体素中心坐标 $(x_i, z_i)$，按量化步长 $x_q, z_q$ 映射到BEV网格坐标：

$$q(x_i, z_i) = (x_i^{BEV}, z_i^{BEV}) = \Big( \Big\lfloor \frac{x_i}{x_q} \Big\rfloor, \Big\lfloor \frac{z_i}{z_q} \Big\rfloor \Big)$$

投影过程仅保留预定义空间范围内的特征（消融实验表明50m×50m为最优区域），超出范围的特征被丢弃。这一投影操作的动机是：不同传感器（如Velodyne 64线束 vs 32线束）产生的点云在3D空间中的采样密度和分布差异显著，但投影到BEV后，道路布局、建筑物轮廓等几何结构趋于一致（Figure 3），从而降低了域偏移的影响。

### 密集2D BEV解码器（hᴮᴱⱽ）

投影后的密集BEV特征 $F^{BEV}$ 经过若干2D卷积层构成的BEV解码器 $h^{BEV}$，预测密集BEV语义布局。该辅助分支的监督信号来自3D标签投影得到的BEV语义标签 $\mathcal{V}_j^{BEV}$。

### 联合损失函数

训练总损失为3D分割损失与BEV分割损失的均值，二者均采用Dice损失：

$$L_{tot} = \frac{1}{2} (L^{BEV} + L^{3D})$$

其中 $L^{3D}$ 为主任务3D语义分割的Dice损失，$L^{BEV}$ 为辅助任务BEV语义布局预测的Dice损失。这种等权联合优化迫使3D骨干网络在提取稀疏体素特征时，同时满足3D精确分割和BEV布局一致性两个目标，从而学习到对传感器配置、扫描分辨率和场景几何变化鲁棒的特征表示。

### 关键设计消融证据

消融实验（Figure 6）证实了BEV辅助分支的独特作用：若将BEV解码器替换为额外的3D分割头（Double），性能显著低于LiDOG，表明泛化能力的提升源于BEV特定的投影和预测任务，而非简单的多解码器集成。此外，BEV预测区域大小（Figure 7）和BEV图像分辨率（Figure 8）的消融表明，50m×50m区域与全分辨率在多数设置下为最优配置。



## 实验与关键发现

### 核心瓶颈与实验动机

LiDAR语义分割模型在跨域条件下性能急剧下降。仅使用源域训练、无任何域泛化技术的 **Source** 模型在 SemanticKITTI 上获得 24.69 mIoU，而在 nuScenes 上仅为 20.62 mIoU（Table 1），与目标域上界模型（如直接在 nuScenes 训练的 48.49 mIoU）之间存在约 22–28 mIoU 的巨大差距。这种退化源于传感器类型（Velodyne 64 线 vs 32 线束）、扫描点密度、地理环境和道路布局等多重域偏移，现有域内方法无法有效泛化。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2304_11705/figures/005_Table_1.jpg]]
*Table 1: Synth4D-KITTI→Real, single-source. Our approach (LiDOG) improves upon Source model on both real datasets: +19.49 mIoU for SemanticKITTI and +16.52 mIoU for nuScenes, outperforming all baselines. Lower bound (red): a model trained on the source domain without the help of DG techniques. Upper bound (blue): model directly trained on the target data*

LiDOG 的核心干预机制是：在 3D 稀疏卷积编码器-解码器网络基础上附加一个密集 2D 鸟瞰图（BEV）语义分割辅助训练任务。通过将 3D 特征沿高度轴投影为 BEV 特征并联合优化 3D 和 BEV 损失，强制骨干网络学习对传感器配置、扫描分辨率和场景几何变化鲁棒的特征表示。其内在逻辑是：不同域的 LiDAR 点云在鸟瞰视角下几何外观更相似，BEV 语义布局作为辅助监督信号可以有效正则化 3D 骨干网络，使其提取的特征具有跨域不变性。

---

### 主要实验结果

#### 单源合成域→真实域泛化

**Synth4D-KITTI→Real** 是核心评测方向。如 Table 1 所示，LiDOG 在 SemanticKITTI 上达到 **44.18 mIoU**，相比 Source 模型提升 **+19.49 mIoU**；在 nuScenes 上达到 **37.14 mIoU**，提升 **+16.52 mIoU**。这一结果全面超越所有对比基线，包括数据增强方法 **Mix3D**（Nekrasov et al., 3DV 2021）、**CoSMix**（Saltori et al., ECCV 2022），以及 2D 域泛化方法 **RobustNet**（Choi et al., ECCV 2021）和弱监督 3D UDA 方法 **RayCast**（Langer et al., IROS 2020）。

值得关注的是，在 Synth4D-KITTI→nuScenes 方向上，所有数据增强基线（Mix3D、PointCutMix、CoSMix）相对于 Source 模型的提升均有限（约 2–5 mIoU），而 LiDOG 的 +16.52 mIoU 提升表明，单纯的数据混合策略难以弥合合成域到真实域的巨大传感器差异，BEV 辅助监督提供了更根本的特征正则化效果。

在 **Synth4D-nuScenes→Real** 补充实验中（Table 5, Appendix），LiDOG 同样表现稳健：SemanticKITTI 上提升 +15.08 mIoU（19.71→34.79），nuScenes 上提升 +9.21 mIoU（24.57→33.78），进一步验证了方法的跨合成域泛化能力。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2304_11705/figures/013_Table_5.jpg]]
*Table 5: Synth4D-nuScenes→Real, single-source. We train our model on Synth4D-nuScenes and test on SemanticKITTI and nuScenes. LiDOG improves over the source models by +15.08 mIoU on SemanticKITTI and by +9.21 mIoU on nuScenes. LiDOG outperforms all the compared baselines. Lower bound (red): a model trained n the source domain without the help of DG techniques. Upper bound (blue): a model directly trained on target data*

#### 多源合成域→真实域泛化

在 **(Synth4D-KITTI + Synth4D-nuScenes)→Real** 多源设置中（Table 2），LiDOG 在 SemanticKITTI 上获得 **42.44 mIoU**（+10.62 vs Source），在 nuScenes 上获得 **40.23 mIoU**（+14.63 vs Source）。相比最强基线 RobustNet，LiDOG 在 SemanticKITTI 上领先 +3.04 mIoU，在 nuScenes 上领先 +2.27 mIoU；相比 Mix3D 则分别领先 +4.56 和 +5.51 mIoU。多源训练为所有方法带来了普遍提升，但 LiDOG 的 BEV 辅助机制在聚合多个合成域的多样性后仍保持显著优势。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2304_11705/figures/007_Table_2.jpg]]
*Table 2: (Synth4D-nuScenes + Synth4D-KITTI)→Real, multi-source. Baselines significantly improve performance relative to the source model. Specifically, with LiDOG we observe +10.62 mIoU improvement on SemanticKITTI and +14.63 mIoU on nuScenes. Our approach (LiDOG) outperforms all the compared approaches. Lower bound (red): a model trained on the source domain without the help of DG techniques. Upper bound (blue): model directly trained on the target data*

#### 真实域→真实域泛化

真实域之间的泛化是更贴近实际部署的场景。在 **SemanticKITTI→nuScenes** 方向上（Table 3），LiDOG 获得 **34.88 mIoU**，相比 Source 模型提升 **+8.35 mIoU**，优于所有对比方法。在反向的 **nuScenes→SemanticKITTI** 方向上（Table 4），LiDOG 获得 **41.22 mIoU**，提升 **+11.67 mIoU**。值得注意的是，SemanticKITTI→nuScenes 的绝对 mIoU 低于反向方向，这与 nuScenes 数据本身更具挑战性（32 线束 LiDAR、更稀疏的点云、更多样的场景）一致，但 LiDOG 在两个方向上均保持一致的相对改善幅度。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2304_11705/figures/008_Table_3.jpg]]
*Table 3: SemanticKITTI→nuScenes, single-source. We train our model on SemanticKITTI and evaluate it on the nuScenes dataset. LiDOG improves over the source model by +8.35 mIoU. Lower bound (red): a model trained on the source domain with-out the help of DG techniques. Upper bound (blue): model directly trained on the target data*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2304_11705/figures/009_Table_4.jpg]]
*Table 4: nuScenes→SemanticKITTI, single-source. We train our model on nuScenes and evaluate it on the SemanticKITTI dataset. LiDOG improves over the source model by +11.67 mIoU. Lower bound (red): a model trained on the source domain with-out the help of DG techniques. Upper bound (blue): model directly trained on the target data*

---

### 关键消融实验

#### BEV 辅助分支的有效性（Figure 6）

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2304_11705/figures/010_Figure_6.jpg]]
*Figure 6: Effectivenes of the BEV head: We compare 2D BEV decoder (Ours) to simply adding an additional 3D segmentation head (Double) on SemanticKITTI (left) and nuScenes (right). Source: Synth4D − KIT T I*

为验证 BEV 特定监督任务的独特贡献，作者将 LiDOG 的 2D BEV 解码器替换为一个额外的 3D 分割头（记为 **Double**），保持参数量和计算量可比。在 Synth4D-KITTI→SemanticKITTI 和 Synth4D-KITTI→nuScenes 两个方向上，Double 的性能均低于 LiDOG。这证明泛化能力的提升并非来自简单的多解码器集成或额外容量，而是 BEV 投影和密集 2D 语义预测这一特定任务形式所诱导的域不变特征学习。

#### BEV 预测区域大小（Figure 7）

BEV 预测区域大小直接影响辅助任务覆盖的场景范围。消融实验对比了 30m×30m、50m×50m、70m×70m 和 100m×100m 四种设置。在 SemanticKITTI 和 nuScenes 上，**50m×50m 均取得最佳 mIoU**。过小的区域（30m）丢失了远处的重要上下文信息，而过大的区域（100m）引入了过多稀疏甚至空白的边缘区域，稀释了有效的监督信号。

#### BEV 图像分辨率（Figure 8）

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2304_11705/figures/012_Figure_8.jpg]]
*Figure 8: BEV image resolution: We compare the performance while changing the BEV image resolution on SemanticKITTI (left) and nuScenes (right), Source: Synth4D-KITTI*

在保持预测区域 50m×50m 不变的前提下，实验对比了 25%、50%、75% 和 100% 四种 BEV 图像分辨率。**100% 分辨率在多数设置下总体最优**，但在 Synth4D-KITTI→nuScenes 方向上 75% 分辨率有轻微提升。考虑到跨数据集的一致性，论文建议使用全分辨率作为默认配置。

---

### 特征可视化与机制验证

Figure 4 的 t-SNE 可视化提供了 BEV 辅助任务作用机制的直接证据。在 Synth4D-KITTI→SemanticKITTI 和 Synth4D-KITTI→nuScenes 两个方向上，训练时**不加入 BEV 任务**（w/o BEV）的道路类别点嵌入在源域和目标域之间呈现明显的分布偏移，两个域的嵌入簇分离严重。而**加入 BEV 辅助任务**（BEV）后，两个域的道路类别嵌入在 t-SNE 空间中显著对齐，簇间重叠度大幅增加。这直接印证了核心假设：BEV 语义布局的辅助监督信号通过反向传播正则化了 3D 骨干网络，使其提取的特征具有跨域不变性。

---

### 失败模式与局限性

尽管 LiDOG 在绝大多数类别上取得显著改善，但 **terrain（地形）** 类别在多个实验中表现欠佳，改善有限甚至下降。例如在多源实验中，terrain 的 IoU 提升远低于 road 或 sidewalk。这一失败模式的根源在于 BEV 投影的**垂直方向类别重叠**问题：terrain 和 vegetation（植被）在垂直方向上经常共存于同一 BEV 网格单元中，投影操作将多个高度层的信息压缩为单一像素，导致两个类别在 BEV 语义布局中混淆。当前的简单高度轴投影无法区分这种垂直重叠，辅助监督信号对 terrain 类反而可能引入噪声。

此外，当前方法仅在单个 LiDAR 帧上进行训练和评估，未利用多帧累加或时间一致性信息。在动态物体密集或点云极度稀疏的场景中，单帧 BEV 语义布局的监督质量可能下降。同时，方法要求所有域共享相同的封闭集类别，无法处理开放集域泛化或类别分布变化的实际需求。



## 定位与知识库关联

### 问题定位与核心瓶颈

LiDAR语义分割的域泛化（DG-LSS）是一个此前未被系统研究的问题。现有LiDAR分割方法均假设训练与测试数据来自同一域，当面临传感器类型（如Velodyne 64线束 vs 32线束）、扫描点密度、地理环境和道路布局等域偏移时，模型性能急剧下降。例如，在SemanticKITTI上训练的模型在nuScenes上仅获得26.53 mIoU，而直接在nuScenes上训练的模型可达48.49 mIoU，差距约22 mIoU。这一瓶颈源于3D稀疏卷积网络对训练域特有的采样模式和几何结构产生了过拟合，提取的特征缺乏跨域不变性。

### 与现有方法的关系

LiDOG是首个专门针对DG-LSS设计的方法。其对比的基线方法可分为三类：

**数据增强方法**通过混合不同场景的点云来提升模型鲁棒性，包括**Mix3D**（Nekrasov et al., 3DV 2021）拼接不同场景的点云和标签、**PointCutMix**（Zhang et al., Neurocomputing 2022）在点云中混合局部补丁、**CoSMix**（Saltori et al., ECCV 2022）按语义区域进行混合。这些方法通过扩充训练分布来隐式提升泛化能力，但本质上仍是在源域分布内进行插值，无法显式建模跨域不变特征。

**2D域泛化方法**包括**IBN**（Pan et al., ECCV 2018）在网络块中结合批次归一化和实例归一化、**RobustNet**（Choi et al., ECCV 2021）在IBN基础上引入实例白化损失。这些方法源自2D视觉域泛化，通过归一化层的设计来消除域特定统计量，但直接迁移到3D稀疏卷积中效果有限，因为它们未利用LiDAR数据的几何结构特性。

**弱监督3D域适应方法**包括**SN**（Wang et al., CVPR 2020）利用源域和目标域平均车辆尺寸知识对源实例进行重缩放、**RayCast**（Langer et al., IROS 2020）通过光线投射重采样源数据以模拟目标域传感器采样模式。这些方法需要目标域的先验知识（如车辆尺寸分布或传感器参数），属于域适应而非域泛化范畴，在无法访问目标域信息的DG-LSS设定下受限。

LiDOG与上述方法的关键区别在于：它不依赖数据增强的随机混合、不引入额外的归一化层、也不需要目标域先验知识，而是通过一个结构化的辅助任务——密集BEV语义布局预测——来正则化3D骨干网络，迫使网络学习对传感器配置和扫描分辨率鲁棒的特征表示。消融实验（Figure 6）证明，用额外的3D分割头替换BEV分支（Double）得到的性能低于LiDOG，说明BEV特定投影和预测任务对泛化能力的贡献超过简单的多解码器集成。

### 核心机制与因果逻辑

LiDOG的核心设计建立在两个关键观察之上：第一，不同域的LiDAR点云在鸟瞰视角下几何外观更相似（Figure 3），这种投影能降低传感器采样模式带来的差异；第二，BEV语义布局作为一种结构化的空间先验，可以有效正则化3D特征学习。

具体而言，LiDOG在3D稀疏卷积编码器-解码器网络（基于MinkowskiNet）基础上附加一个密集2D BEV解码器。训练时，3D体素特征沿高度轴投影为密集BEV特征：
$$q(x_i, z_i) = (x_i^{BEV}, z_i^{BEV}) = \Big( \Big\lfloor \frac{x_i}{x_q} \Big\rfloor, \Big\lfloor \frac{z_i}{z_q} \Big\rfloor \Big)$$
随后通过若干2D卷积层预测BEV语义布局，并与3D分割任务联合优化：
$$L_{tot} = \frac{1}{2} (L^{BEV} + L^{3D})$$
其中$L^{BEV}$和$L^{3D}$均为Dice损失。

BEV辅助任务的作用机制在于：3D骨干网络为了同时满足3D稀疏分割和BEV密集预测两个目标，必须学习在高度轴投影后仍保持语义一致性的特征，这迫使网络抑制对传感器特定采样模式的依赖。t-SNE可视化（Figure 4）证实，加入BEV辅助任务后，不同域的道路类别点嵌入在特征空间中更为对齐，表明BEV任务有效减小了域间特征分布差异。

### 适用边界与局限

**垂直重叠类别的混淆**是LiDOG的主要局限。BEV投影在垂直方向上存在类别重叠，特别是地形（terrain）和植被（vegetation）在BEV视角下占据相同的空间位置，导致terrain类性能欠佳，在多数实验中改善有限甚至下降。这一问题源于BEV投影固有的信息损失，是方法设计的结构性约束。

**单帧处理限制**：当前方法仅在单个LiDAR帧上进行评估，未探索多帧累加或时间一致性对域泛化的潜在益处。在动态场景中，时序信息可能提供额外的跨域不变线索。

**封闭集假设**：LiDOG要求所有域共享相同的封闭集类别，未考虑开放集域泛化或类别分布变化。当目标域出现源域未见过的类别时，BEV辅助任务无法提供有效正则化。

**超参数敏感性**：BEV预测区域大小和分辨率需要针对具体域迁移方向进行调整。消融实验表明，50m×50m区域在SemanticKITTI和nuScenes上均取得最佳mIoU（Figure 7），100%分辨率总体最优（Figure 8），但在Synth4D-KITTI→nuScenes上75%分辨率有轻微提升。这些超参数的最优选择目前依赖经验调参，缺乏自适应确定机制。

### 开放问题

1. **域偏移类型泛化**：LiDOG在传感器配置和地理环境偏移上验证有效，但在其他域偏移类型（如不同天气条件、激光强度噪声、动态物体密度）下的泛化能力尚未探索。

2. **任务扩展性**：BEV辅助任务能否扩展到其他3D感知任务（如3D目标检测、点云实例分割）？BEV语义布局作为正则化信号的通用性值得进一步研究。

3. **垂直混淆缓解**：如何缓解BEV投影中垂直重叠类别混淆的问题？可能的方向包括软标签分配、多高度切片投影或引入注意力机制对不同高度层进行加权。

4. **时序融合**：是否可以通过多帧时序融合或自监督预训练进一步提升跨域鲁棒性？时序一致性可能提供额外的域不变约束。

5. **自适应超参数**：在计算和内存资源受限时，BEV辅助任务的超参数（如BEV分辨率、区域大小）最优选择如何自适应确定？元学习或神经架构搜索可能是潜在解决方案。



## 原文 PDF

![[paperPDFs/ICCV_2023/Walking_your_lidog_A_journey_through_multiple_domains_for_lidar_semantic_segmentation.pdf]]
