---
title: "To View Transform or Not to View Transform: NeRF-based Pre-training Perspective"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/To_View_Transform_or_Not_to_View_Transform_NeRF_based_Pre_training_Perspective.pdf
project_link: null
code_link: null
openreview_forum_id: G0HcRB3s3N
aliases:
- VTONVTNBPTP
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "完全移除视图变换，采用基于点的连续3D表示，并通过NeRF重塑的架构使预训练与下游任务共享同一个NeRF网络，从而避免先验冲突并保留预训练获得的全部知识。"
primary_logic: "连续3D表示学习是NeRF预训练发挥潜力的关键；将NeRF网络作为统一框架保留，使预训练和下游任务协调一致，能够同时提升场景重建和感知性能。"
claims:
- "NeRP3D 在没有2D基础模型蒸馏的情况下，产生精确且边界清晰的3D点特征，优于基于视图变换的UniPAD和SelfOcc。"
- "NeRP3D 在3D目标检测、占据预测和HD地图构建三个下游任务上均显著超越基于视图变换的NeRF预训练方法。"
- "使用SDF先验而非标准密度先验能够产生更清晰的物体边界，有利于感知任务。"
- "NeRP3D 在零样本跨数据集场景重建中表现优异，从Argoverse 2迁移到nuScenes时，PSNR达28.238（UniPAD为18.668）。"
---

# To View Transform or Not to View Transform: NeRF-based Pre-training Perspective

> [!tip] 核心洞察
> 连续3D表示学习是NeRF预训练发挥潜力的关键；将NeRF网络作为统一框架保留，使预训练和下游任务协调一致，能够同时提升场景重建和感知性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 视角变换与否：基于NeRF预训练的视角 |
| 英文题名 | To View Transform or Not to View Transform: NeRF-based Pre-training Perspective |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=G0HcRB3s3N) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | NeRP3D |
| Dataset | nuScenes 3D目标检测, nuScenes 占据预测 (Occ3D), nuScenes HD地图构建, nuScenes 深度估计 |

> [!tip] 效果简介
> - nuScenes 3D目标检测 上，NDS / mAP 为 47.3 / 42.8，对比 45.5 / 41.6 (UVTR-C w/ UniPAD)，变化 +2.1 NDS, +1.8 mAP。
> - nuScenes 占据预测 (Occ3D) 上，mIoU 为 35.49，对比 34.05 (UniPAD) / 29.65 (SelfOcc)，变化 +1.44 over UniPAD, +5.84 over SelfOcc。
> - nuScenes HD地图构建 上，mAP 为 59.1，对比 57.8 (UVTR-C w/ UniPAD)，变化 +1.3 mAP。

## 概要

现有基于NeRF的自动驾驶预训练方法将NeRF与视图变换（View Transform）耦合，这一设计存在根本性先验冲突：视图变换强制使用离散、固定分辨率的体素或BEV特征网格，而NeRF本身假设连续、自适应的函数表示。两种先验的不兼容导致预训练产生的3D表征模糊且充满歧义。更关键的是，预训练完成后NeRF网络即被丢弃，下游任务仅使用视图变换骨干的特征，使得预训练获得的增强3D知识无法有效转移。

本文提出 **NeRP3D**，其核心思路是**完全移除视图变换**，代之以连续的、基于点的3D表示。具体而言，NeRP3D通过可形变交叉注意力从任意连续3D位置直接查询2D图像特征，避免了离散体素网格的刚性约束。同时，NeRP3D将NeRF网络重新设计为统一的3D感知框架——预训练阶段的渲染和下游微调阶段的感知任务**共享同一个网络**，不再丢弃任何模块。这一设计使预训练获得的连续3D知识得以完整保留，实现了场景重建与感知性能的同步提升。

核心证据链如下：

1. **特征质量定性对比**（Figure 1）：在没有任何2D基础模型蒸馏或微调的情况下，NeRP3D预训练后直接提取的3D点特征即展现出精确的物体边界和良好的定位性，显著优于基于视图变换的UniPAD和SelfOcc，甚至与DINO特征相当。

2. **下游任务全面领先**（Table 1）：在nuScenes数据集上，NeRP3D在3D目标检测（NDS 47.3 vs UniPAD 45.5）、占据预测（mIoU 35.49 vs UniPAD 34.05）和HD地图构建（mAP 59.1 vs UniPAD 57.8）三个任务上均显著超越基于视图变换的NeRF预训练方法。

3. **场景重建大幅提升**（Table 2）：预训练阶段的RGB重建PSNR达33.42（UniPAD仅19.92），深度估计Abs Rel降至0.183（UniPAD为0.204），说明移除视图变换后连续表示能够更准确地建模场景几何和外观。

4. **跨数据集泛化验证**（Table 3）：从Argoverse 2零样本迁移到nuScenes时，NeRP3D的PSNR达28.238，远超UniPAD的18.668，证明连续点表示具备更强的泛化能力。

5. **消融实验确认**：采用SDF先验（NeuS）替代标准NeRF密度先验，能够产生更清晰的物体边界，有利于下游感知任务。

综上，NeRP3D揭示了连续3D表示学习是NeRF预训练发挥潜力的关键——通过移除视图变换并保留NeRF网络作为统一框架，可以同时提升场景重建质量和下游感知性能，为自动驾驶领域的自监督预训练提供了新的范式。

自动驾驶系统依赖精确的3D场景理解来实现安全导航，涵盖3D目标检测、占据预测和高精地图构建等核心任务。然而，大规模3D标注数据的获取成本极高，促使研究者探索自监督预训练范式，以从无标注的多视图图像中学习可迁移的3D表征。

近年来，神经辐射场（NeRF）因其从2D图像重建3D场景的能力，成为自动驾驶预训练的有力候选。现有方法（如UniPAD、SelfOcc）的典型流程是：先通过视图变换将多视图2D特征提升为离散的体素或BEV特征网格，再在该网格上训练NeRF进行渲染重建，预训练完成后丢弃NeRF网络，仅将视图变换骨干提取的体素特征用于下游感知任务。

这一范式存在根本性的先验冲突：**视图变换强制引入离散、刚性的体素表示，而NeRF天然假设连续、自适应的函数空间**。两种先验的矛盾导致3D表征产生模糊和歧义——体素网格的固定分辨率限制了NeRF对精细几何的建模能力，而预训练阶段学习到的增强3D知识在NeRF被丢弃后无法有效转移至下游任务，造成预训练与微调之间的表征鸿沟。

此外，现有方法依赖标准NeRF密度场作为几何先验，缺乏对物体表面的显式约束，难以产生清晰的边界信息，而这正是下游感知任务（如检测和占据预测）所迫切需要的。

本文的核心动机在于：**彻底解耦NeRF与视图变换，将3D场景建模为连续的点表示，并通过NeRF重塑的架构使预训练与下游任务共享同一网络**，从而消除先验冲突，保留预训练获得的全部知识，同时引入更强的几何先验以提升边界质量。这一设计使得连续3D表示学习成为发挥NeRF预训练潜力的关键机制。

## 核心方法与创新机理

NeRP3D 的核心创新在于**彻底解耦 NeRF 与视图变换**，并围绕连续 3D 表示重新设计整个预训练-下游任务框架。现有方法（如 UniPAD、SelfOcc）将 NeRF 建立在视图变换产生的离散体素特征之上，形成两个相互矛盾的先验：视图变换强制离散、刚性的体素表示，而 NeRF 假设连续、自适应的函数。这种冲突导致预训练获得的 3D 表征模糊、边界歧义，且预训练完成后 NeRF 网络被直接丢弃，下游任务仅使用视图变换骨干的特征，造成知识转移的断裂。

NeRP3D 从三个关键维度改变了这一范式：

### 1. 连续点表示取代离散体素

现有方法通过视图变换将 2D 特征投影到固定分辨率的 BEV 或体素网格，再通过三线性插值查询 NeRF 所需的 3D 点特征。NeRP3D 完全移除了视图变换和体素相关参数，转而采用**基于可形变交叉注意力的连续点查询机制**：对于任意连续 3D 位置 $\mathbf{x}$，通过学习的采样偏移和注意力权重，直接从 2D 图像特征图中聚合信息，生成点嵌入 $\mathbf{z}$（Eq. 2）。这一设计避免了固定网格带来的离散化误差，使 3D 表示真正连续且自适应。

### 2. NeRF 网络全生命周期保留

在 UniPAD 等基线中，NeRF 仅在预训练阶段充当渲染头，微调时被丢弃，下游任务退回到使用视图变换特征。NeRP3D 将 NeRF 重塑为统一的 3D 理解框架：**预训练和下游任务共享同一个连续点查询网络**，仅在采样策略上切换——预训练采用沿光线的射线采样以支持体渲染，下游任务采用均匀空间采样以适配检测头。这一设计使预训练获得的几何与外观知识完整保留并直接服务于感知任务，而非被截断丢弃。

### 3. SDF 几何先验替代密度场

标准 NeRF 使用密度场建模几何，但密度分布平滑、边界模糊，不利于下游感知任务对清晰物体边界的依赖。NeRP3D 采用基于 SDF 的隐式表面表示（NeuS），将点嵌入转换为符号距离，再通过 Sigmoid 变换导出不透明度 $\alpha_j$（Eq. 3）。消融实验证实，SDF 先验相比密度先验能产生更清晰的物体边界，直接转化为下游检测和占据预测的性能增益。

这三个 changed slots 协同作用：连续点表示消除了视图变换的先验冲突，NeRF 网络保留确保了知识无损转移，SDF 先验强化了几何边界的感知友好性。Figure 2 清晰对比了两种范式：左侧的“视图变换→离散体素→NeRF→丢弃”流程，与右侧的“多视图图像→NeRP3D 连续点查询→渲染头/感知头”统一架构。

![[assets/figures/papers/iclr26_0009_G0HcRB3s3N_To_View_Transform_or_Not_to_View_Transform_NeRF-/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of the previous NeRF-based pre-training methods and our NeRP3D pipeline*

![[assets/figures/papers/iclr26_0009_G0HcRB3s3N_To_View_Transform_or_Not_to_View_Transform_NeRF-/figures/003_Figure_3.jpg]]
*Figure 3: Overview of NeRP3D, illustrating both pre-training for rendering (orange) and fine-tuning for downstream (blue) pipelines. Through NeRF-resembled design, our method maintains a coherent 3D understanding from scattered points across diverse tasks while accommodating task-specific point sampling strategies, enabling the model to effectively leverage underlying geometric and appearance information while allowing for task-dependent feature specialization*

NeRP3D 的整体设计遵循一个核心原则：**将3D场景建模为连续的、基于点的函数，并在预训练与下游任务之间共享同一个NeRF网络**，从而消除传统方法中视图变换与NeRF之间的先验冲突。

### 架构总览

如图2所示，传统基于NeRF的预训练流程存在一个结构性断裂：多视图图像先经过视图变换（View Transformation）生成离散的体素特征，随后NeRF从这些体素中采样渲染；预训练完成后，NeRF网络被丢弃，下游任务仅使用视图变换骨干提取的特征。这种设计在两个层面产生矛盾——NeRF假设连续、自适应的3D函数，而视图变换强制离散、刚性的体素表示，导致3D表征模糊且预训练获得的知识无法完整转移。

NeRP3D 完全移除了视图变换模块，改为端到端的连续点查询架构。整个框架在预训练（渲染）和下游微调（感知）两个阶段之间**不丢弃、不新增任何模块**，仅在采样策略上做切换。

### 模块构成与数据流

框架由五个核心模块串联构成：

1. **图像编码器**：将多视图图像 $I_t$ 输入图像骨干网络，提取2D特征图 $\mathbf{F}$，作为后续3D点查询的上下文信息源。

2. **自适应点采样**：根据任务阶段切换两种采样策略——
   - **光线采样（ray-wise sampling）**：用于预训练渲染阶段，沿相机光线密集采样3D点，支持体渲染重建。
   - **均匀空间采样（uniform spatial sampling）**：用于下游感知任务，在3D空间内均匀采样点，覆盖目标检测、占据预测等任务所需的空间区域。

3. **可形变交叉注意力点查询**：对每个采样得到的3D点 $\mathbf{x}$，通过可形变交叉注意力从2D特征图 $\mathbf{F}$ 中聚合上下文信息，生成该点的嵌入表示 $\mathbf{z}$。具体地，3D坐标先经过收缩参数化 $p(\mathbf{x}')$（公式1）映射到有界范围，再通过学习的采样偏移 $\Delta \pi_{h,s}$ 和注意力权重 $\mathbf{A}_{h,s}$ 从多视图特征中提取信息（公式2）。

4. **SDF-体积渲染头**：在预训练阶段，将点嵌入 $\mathbf{z}$ 转换为颜色 $\mathbf{c}_j$ 和符号距离 $s_j$。符号距离通过公式3转换为不透明度 $\alpha_j$，再沿光线进行体渲染积分（公式4），生成像素颜色 $\hat{\mathbf{C}}(\mathbf{r}_i)$ 和深度 $\hat{D}(\mathbf{r}_i)$，用于自监督重建损失。

5. **任务感知检测头**：在下游微调阶段，将空间均匀采样得到的点嵌入集合 $\{\mathbf{z}\}$ 重塑为目标形状（如占据预测的 $(X \times Y \times Z) \times C$），输入标准的3D检测/占据预测/HD地图构建头。

### 关键设计决策

- **SDF几何先验**：采用NeuS的符号距离函数（SDF）替代标准NeRF的密度场。消融实验证实，SDF先验能产生更清晰的物体边界，这对下游感知任务至关重要。
- **多视角重投影一致性**：为缓解LiDAR监督在视野外区域的稀疏问题，引入多视角重投影一致性损失（公式5），在不同视角之间强制预测深度的颜色一致性。
- **收缩坐标参数化**：针对自动驾驶场景的无界特性，采用公式1将3D坐标压缩到有界范围，保持近处真实尺度，远处按视差分布，使网络能有效处理大范围空间。

这种统一架构使预训练阶段学到的连续3D表征能够**完整保留**到下游任务中，避免了传统方法中“预训练NeRF→丢弃→仅用视图变换特征”的知识断裂。Figure 1的定性结果显示，NeRP3D在没有任何2D基础模型蒸馏的情况下，直接提取的3D点特征已具有精确的物体边界定位能力，与DINO特征相当。

### 3D坐标收缩参数化

为处理自动驾驶场景的无界3D空间，NeRP3D对3D坐标进行收缩参数化，将远处点压缩到有界范围，同时保持近处点的真实尺度，使神经网络能有效编码远近物体：

$$p(\mathbf{x}') = \begin{cases} \alpha \mathbf{x}' & |\mathbf{x}'| \leq 1 \\ \left(1 - \frac{(1-\alpha)}{|\mathbf{x}'|}\right) \frac{\mathbf{x}'}{|\mathbf{x}'|} & |\mathbf{x}'| > 1 \end{cases}$$

其中 $\mathbf{x}'$ 为归一化后的3D坐标，$\alpha$ 控制近处区域的线性保持范围。该收缩函数确保近处物体保持原始几何精度，远处区域按视差分布压缩，避免网络在无界空间中的表示退化。

### 自适应点采样策略

NeRP3D根据任务阶段切换两种采样策略，这是统一预训练与下游任务的关键设计：

- **光线采样（预训练阶段）**：沿相机光线采样3D点，用于体渲染自监督，使网络学习场景几何与外观。
- **均匀空间采样（下游任务阶段）**：在3D空间内均匀采样点，覆盖整个感兴趣区域，为检测头提供空间完备的特征。

两种采样策略共享同一连续点查询网络，保证预训练获得的几何理解直接迁移到感知任务，无需视图变换带来的离散化损失。

### 可形变交叉注意力点查询

对于每个采样点 $\mathbf{x}$，NeRP3D通过可形变交叉注意力从多视图2D特征图中聚合信息，生成该点的嵌入表示 $\mathbf{z}$：

$$\mathbf{z} = \sum_{h=1}^{N_h} \mathbf{W}_h \sum_{s=1}^{N_s} \mathbf{A}_{h,s} \mathbf{W}_s' \mathbf{F}(\pi(\mathbf{x}) + \Delta \pi_{h,s}(\gamma(p(\mathbf{x}'))))$$

其中：
- $\mathbf{F}$ 为图像编码器提取的2D特征图；
- $\pi(\mathbf{x})$ 为点 $\mathbf{x}$ 投影到图像平面的参考位置；
- $\Delta \pi_{h,s}$ 为可学习的采样偏移，由收缩坐标 $p(\mathbf{x}')$ 经位置编码 $\gamma$ 后预测；
- $\mathbf{A}_{h,s}$ 为多头注意力权重；
- $N_h$ 为注意力头数，$N_s$ 为每头采样点数。

该机制使每个3D点能自适应地从最相关的图像区域提取特征，避免固定投影带来的几何误差，是实现连续3D表示的核心操作。

### SDF-体积渲染头

NeRP3D采用基于符号距离函数（SDF）的体积渲染，而非标准NeRF的密度场。SDF先验强制学习清晰的物体表面边界，对下游感知任务更有利。

**不透明度计算**：将SDF值 $\phi_{sdf}(\mathbf{z}_j)$ 转换为不透明度 $\alpha_j$：

$$\alpha_j = \max\left( \frac{\Phi_\omega(\phi_{sdf}(\mathbf{z}_j)) - \Phi_\omega(\phi_{sdf}(\mathbf{z}_{j+1}))}{\Phi_\omega(\phi_{sdf}(\mathbf{z}_j))}, 0 \right)$$

其中 $\Phi_\omega$ 为带可学习参数 $\omega$ 的Sigmoid函数，$\mathbf{z}_j$ 和 $\mathbf{z}_{j+1}$ 为光线上相邻采样点的嵌入。该公式利用相邻点SDF值之差计算不透明度，使表面附近产生锐利过渡。

**体渲染积分**：沿光线累加颜色和深度：

$$\hat{\mathbf{C}}(\mathbf{r}_i) = \sum_{j=1}^{D} w_j \mathbf{c}_j, \quad \hat{D}(\mathbf{r}_i) = \sum_{j=1}^{D} w_j t_j$$

其中 $w_j = \alpha_j \prod_{k=1}^{j-1} (1-\alpha_k)$ 为累积权重，$\mathbf{c}_j = \phi_{rgb}(\mathbf{z}_j, \mathbf{d}_i)$ 为点颜色预测，$t_j$ 为沿光线的深度值。预训练通过最小化渲染RGB与真实RGB的差异实现自监督。

### 多视角重投影一致性损失

为缓解LiDAR深度监督的稀疏性问题，NeRP3D引入多视角重投影一致性损失，在无LiDAR监督区域强制跨视角颜色一致性：

$$\mathcal{L}_{reproj} = \frac{1}{|\mathcal{R}|} \sum_{\mathbf{r}_i \in \mathcal{R}} \sum_{\mathbf{x}_j \in \mathbf{r}_i} w_j | I_t(\mathbf{r}_i) - I_s(\pi_s(\mathbf{x}_j)) |$$

其中 $\mathbf{r}_i$ 为目标视角光线，$\mathbf{x}_j$ 为光线上采样点，$w_j$ 为体渲染权重，$I_t$ 为目标图像，$I_s$ 为源图像，$\pi_s$ 将3D点投影到源视角。该损失利用多视角图像作为免费监督信号，在LiDAR覆盖范围之外仍能约束深度预测。

### 任务感知特征重塑

预训练完成后，NeRF网络被完整保留。在下游任务中，均匀空间采样的点嵌入 $\{\mathbf{z}\}$ 被重塑为任务兼容的格式——例如占据预测重塑为 $(X \times Y \times Z) \times C$ 的体素特征——直接输入标准检测头。这一设计避免了预训练后丢弃NeRF网络带来的知识损失，使预训练获得的连续3D表示完整迁移到感知任务。

## 实验与关键发现

### 瓶颈验证：视图变换的代价

现有NeRF预训练方法将视图变换与NeRF耦合，这一设计引入了两个根本性冲突。第一，视图变换输出离散的、固定分辨率的体素或BEV特征网格，而NeRF的核心假设是连续的三维函数——两种先验相互矛盾，导致预训练阶段学到的3D表征模糊且边界歧义。第二，预训练完成后，NeRF网络本身被丢弃，下游任务仅使用视图变换骨干的特征，预训练所增强的3D知识无法有效转移。Figure 1 的定性对比直观验证了这一问题：UniPAD和SelfOcc从2D特征图中提取的特征在物体边界处模糊、定位不准，而NeRP3D在无任何2D基础模型蒸馏的情况下，产生了精确且边界清晰的点特征，与DINO特征相当。这证明移除视图变换、保留连续表示是释放NeRF预训练潜力的关键。

### 下游任务主结果

Table 1 汇总了三个核心下游任务的性能。所有方法使用相同的检测头结构和训练配置（24 epochs），差异仅源于预训练策略。

![[assets/figures/papers/iclr26_0009_G0HcRB3s3N_To_View_Transform_or_Not_to_View_Transform_NeRF-/figures/004_Table_1.jpg]]
*Table 1: Downstream detection performance (a) 3D object detection*

**3D目标检测。** 在nuScenes验证集上，NeRP3D取得47.3 NDS和42.8 mAP，相比基于视图变换的UniPAD（45.5 NDS / 41.6 mAP）分别提升2.1和1.8个点，也显著优于使用ImageNet预训练的BEVFormerV2（42.0 NDS / 34.6 mAP）。值得注意的是，NeRP3D仅使用1/5训练数据时，mAP达到24.9，已接近全数据训练的UniPAD（28.6 mAP），显示出更高的数据效率。

**占据预测。** 在Occ3D-nuScenes基准上，NeRP3D取得35.49 mIoU，超越UniPAD的34.05和SelfOcc的29.65，分别提升1.44和5.84个点。这一优势源于连续点查询能够对任意空间位置进行精细采样，而非被限制在固定体素网格内。

**HD地图构建。** NeRP3D取得59.1 mAP，比UVTR-C+UniPAD组合（57.8 mAP）提升1.3个点。三个任务的一致性提升表明，保留NeRF网络作为统一表示框架的收益是跨任务泛化的。

### 场景重建：预训练质量的直接证据

预训练阶段的重建质量是下游性能的上限。Table 2 报告了深度估计和RGB重建的定量结果。

![[assets/figures/papers/iclr26_0009_G0HcRB3s3N_To_View_Transform_or_Not_to_View_Transform_NeRF-/figures/008_Table_2.jpg]]
*Table 2: Pretext scene reconstruction performance*

**深度估计。** NeRP3D在Abs Rel上达到0.183，优于UniPAD（0.204）和SelfOcc（0.232）。Figure 4 的定性对比进一步揭示差异：UniPAD和SelfOcc的深度图在拥挤场景中倾向于将相邻物体合并为模糊的团块，而NeRP3D能够清晰分离不同深度的目标。这一优势来自两个设计选择：SDF先验强制产生清晰的物体表面边界，以及均匀空间采样策略结合多视角重投影一致性损失（Eq. 5），缓解了LiDAR稀疏区域（如远处、物体间隙）的监督不足。

**RGB重建。** NeRP3D取得PSNR 33.42、SSIM 0.969、LPIPS 0.070，而UniPAD仅为19.92 / 0.536 / 0.629——PSNR差距高达13.5 dB。Figure 4 显示，UniPAD和SelfOcc的重建图像存在严重模糊和伪影，NeRP3D则保持了城市场景的高保真细节，无模糊和模式化伪影。这验证了连续点查询比离散体素网格能更准确地捕捉场景几何与外观。

### 跨数据集泛化

Table 3 报告了零样本跨数据集场景重建性能：模型在Argoverse 2上预训练，直接在nuScenes上测试，无任何微调。NeRP3D取得PSNR 28.238、SSIM 0.905，而UniPAD仅为18.668和0.432——PSNR差距达9.57 dB。这一结果说明，连续点表示学习到的是与特定数据集解耦的通用3D理解，而非过拟合于训练数据的体素分布。相比之下，视图变换方法因体素分辨率、范围等参数与数据集强绑定，跨数据集泛化能力显著受限。

![[assets/figures/papers/iclr26_0009_G0HcRB3s3N_To_View_Transform_or_Not_to_View_Transform_NeRF-/figures/010_Table_3.jpg]]
*Table 3: Zero-shot scene reconstruction performance (Argoverse 2 → nuScenes)*

### 消融：SDF先验的关键作用

消融实验对比了SDF先验（NeuS）与标准NeRF密度先验的效果。结果表明，SDF先验强制产生更清晰的物体边界，这对下游感知任务至关重要。其机理在于：标准密度场在物体表面附近产生平滑过渡的不透明度，导致边界模糊；而SDF通过符号距离函数在零等值面处产生锐利跳变，经Eq. 3转换为不透明度后，体渲染能精确定位表面位置。这一设计选择直接贡献了深度估计和占据预测中的边界质量提升。

### 失败模式与局限

尽管NeRP3D在静态场景重建和感知上表现优异，但存在以下已知局限：

1. **动态物体未建模。** 当前方案假设场景静态，未处理运动物体。在包含移动车辆和行人的帧中，渲染和深度估计可能出现拖影或错误。
2. **LiDAR范围外区域的监督缺失。** 深度监督依赖LiDAR点云，对于天空、远处背景等LiDAR无法覆盖的区域，多视角一致性损失（Eq. 5）仅提供弱监督，可能导致深度估计不准确。
3. **计算开销。** 从NeRF点嵌入适配到检测头的过程需要将空间采样点重塑为规则网格，计算开销高于直接使用视图变换特征。论文指出混合光栅化（如3DGS）是潜在的加速方向，但尚未实现。
4. **时序信息未利用。** 当前仅使用单帧多视图图像，未利用时序RGB重建来增强多视角一致性。

### 关键图表结论速查

| 图表 | 核心结论 |
|------|---------|
| Figure 1 | NeRP3D的特征在无2D基础模型蒸馏下即达到精确的物体边界定位 |
| Table 1(a) | 3D检测：47.3 NDS / 42.8 mAP，超越UniPAD 2.1 NDS |
| Table 1(b) | 占据预测：35.49 mIoU，超越UniPAD 1.44点 |
| Table 1(c) | HD地图：59.1 mAP，超越UVTR-C+UniPAD 1.3点 |
| Figure 4 | RGB重建无模糊伪影，深度图能分离拥挤目标 |
| Table 2(b) | RGB重建PSNR 33.42，领先UniPAD 13.5 dB |
| Table 3 | 跨数据集PSNR 28.238，领先UniPAD 9.57 dB |

![[assets/figures/papers/iclr26_0009_G0HcRB3s3N_To_View_Transform_or_Not_to_View_Transform_NeRF-/figures/009_Table_5.jpg]]
*Table 5: (b) RGB reconstruction*

## 定位与知识库关联

### 瓶颈与突破：视图变换与NeRF的先验冲突

现有基于NeRF的自动驾驶预训练方法（以UniPAD、SelfOcc为代表）将NeRF渲染头嫁接在视图变换（View Transformation）之后：多视图2D特征先通过LSS或交叉注意力转换为离散的体素/BEV特征网格，再经三线性插值送入NeRF进行体渲染。这一设计引入了一对结构性矛盾——**视图变换强制离散、刚性的体素表示，而NeRF假设连续、自适应的隐式函数**。两种先验的冲突使3D表征产生模糊与歧义，直接制约了渲染质量和下游任务迁移的上限。更关键的是，预训练完成后NeRF网络被丢弃，下游任务仅使用视图变换骨干的特征，预训练阶段增强的3D知识无法有效保留。

NeRP3D的因果开关（causal knob）是**完全移除视图变换，转而采用基于点的连续3D表示**，并通过NeRF重塑的架构使预训练与下游任务共享同一个网络。这一设计消除了先验冲突，同时使预训练获得的全部知识得以继承。

### 方法谱系中的位置

**相对于UniPAD / SelfOcc（视图变换+NeRF路线）**：NeRP3D属于“去视图变换”分支。UniPAD将NeRF视为视图变换后的后处理模块，预训练与下游任务在架构上割裂；NeRP3D则将NeRF网络本身重塑为统一的3D特征提取器，在预训练（光线采样→体渲染）和下游任务（空间均匀采样→检测头）之间仅切换采样策略，不增减模块。这一设计差异在下游性能上体现为：3D目标检测NDS +2.1（47.3 vs 45.5），占据预测mIoU +1.44（35.49 vs 34.05），HD地图构建mAP +1.3（59.1 vs 57.8）。

**相对于BEVFormerV2 / TPVFormer（纯检测路线）**：这些方法依赖ImageNet预训练的2D骨干，未利用NeRF的自监督信号。NeRP3D表明，在相同检测头结构下，NeRF预训练可提供超越ImageNet预训练的3D先验，且数据效率更高——仅用1/5 nuScenes数据训练的NeRP3D（24.9 mAP）即可媲美全数据训练的UniPAD（28.6 mAP）。

**相对于3DGS路线（高斯泼溅）**：NeRP3D目前基于体渲染，计算开销较高。论文明确指出，混合光栅化（如3DGS）可能实现实时性能，同时保留连续点查询的优势，这是未来的演进方向。

### 适用边界与局限

1. **静态场景假设**：当前方案主要针对静态场景重建和感知，未探讨动态物体处理。在包含运动物体的场景中，体渲染的静态假设会导致重影和深度歧义。

2. **深度监督的LiDAR依赖**：SDF-体渲染头的深度监督依赖LiDAR点云。对于LiDAR覆盖范围以外的区域（天空、远处背景），监督信号不足，尽管多视角重投影一致性损失（Eq. 5）部分缓解了这一问题，但无法根本解决。

3. **计算开销**：从NeRF输出的连续点表示适配到检测头的过程涉及大量点查询和特征重塑，计算成本高于直接使用体素特征。论文承认混合光栅化（如3DGS）是降低开销的潜在方案。

4. **时序信息缺失**：当前仅使用单帧多视图图像，未利用时序RGB重建来增强多视角一致性。这限制了在遮挡区域和低纹理区域的重建质量。

### 开放问题

- **时序RGB重建**：能否通过多帧时序RGB重建进一步增强多视角一致性，尤其是在动态物体和遮挡场景下？
- **实时性能与灵活采样的兼顾**：如何利用高斯泼溅（3DGS）的快速渲染能力，在保持连续点查询的同时实现实时性能？3DGS的显式点云表示与NeRP3D的隐式点查询之间如何桥接？
- **无LiDAR深度监督**：如何在不依赖LiDAR的情况下，有效监督视野以外区域的深度？自监督深度估计或单目深度先验是否可替代LiDAR？
- **大规模开放场景推广**：连续点表示是否可以在更大规模的开放场景数据集（如Waymo Open Dataset、ZOD）中推广，并与其他自监督任务（如运动预测、轨迹预测）结合？
- **动态物体建模**：如何在连续点表示框架内引入动态物体建模，使预训练阶段即可学习运动感知的3D表征？

> **注意**：以上开放问题均来自论文明确指出的未来方向或实验分析中暴露的不足，未引入外部推测。关于3DGS融合和时序扩展的具体实现路径，目前尚无实验证据，需后续工作验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/To_View_Transform_or_Not_to_View_Transform_NeRF_based_Pre_training_Perspective.pdf]]
