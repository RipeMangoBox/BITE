---
title: "The NeRFect Match: Exploring NeRF Features for Visual Localization"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/The_NeRFect_Match_Exploring_NeRF_Features_for_Visual_Localization.pdf
code_link: null
project_link: https://nerfmatch.github.io/
aliases:
- NNM
- NMENFVL
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "使用预训练NeRF的中间层特征（f³）作为3D描述子，并设计匹配Transformer（NeRFMatch）直接对齐2D图像特征与冻结的3D NeRF特征。"
primary_logic: "NeRF在视图合成中学习到的内部特征蕴含场景几何与外观信息，可作为有效的3D点描述符用于2D-3D匹配，无需修改NeRF模型本身。"
claims:
- "NeRFMatch超越所有APR方法，并在NeRF匹配方法中达到领先水平（Avg.Med 13.3cm/0.3° on Cambridge）"
- "使用中间层f³作为NeRF特征比使用原始坐标或位置编码显著提升定位精度（27.9cm vs 458.0cm）"
- "迭代精化可将NeRFMatch平均误差从16.5cm/0.3°降至14.2cm/0.3°，召回率从71.3%提升至78.2%"
- "MipNeRF的特征在定位中显著优于Instant NGP（NeRFMatch 13.3cm vs 28.1cm）"
---

# The NeRFect Match: Exploring NeRF Features for Visual Localization

> [!tip] 核心洞察
> NeRF在视图合成中学习到的内部特征蕴含场景几何与外观信息，可作为有效的3D点描述符用于2D-3D匹配，无需修改NeRF模型本身。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | NeRFect Match：探索用于视觉定位的NeRF特征 |
| 英文题名 | The NeRFect Match: Exploring NeRF Features for Visual Localization |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2403.09577) · [Project](https://nerfmatch.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | NeRFMatch / NeRFMatch-Mini |
| Dataset | Cambridge Landmarks, 7-Scenes (SfM poses) |

> [!tip] 效果简介
> - Cambridge Landmarks 上，Avg. median transl. (cm) / rot. (°) 为 NeRFMatch: 13.3/0.3，对比 NeRFLoc: 13.0/0.2，变化 平移+0.3cm，旋转+0.1°（略差，但仍具有竞争力）。
> - Cambridge Landmarks 上，Avg. median transl. (cm) / rot. (°) 为 NeRFMatch: 13.3/0.3，对比 CrossFire: 47/0.7 (平均约47cm/0.7°)，变化 大幅优于CrossFire。
> - 7-Scenes (SfM poses) 上，Avg. median transl. (cm) / rot. (°) 为 NeRFMatch: 2.7/0.7，对比 NeFeS: 2.4/0.9，变化 平移+0.3cm，旋转-0.2°（基本持平）。

## 概要

视觉定位的核心挑战在于将查询图像与场景的3D几何建立精确的2D-3D对应关系。传统结构化方法依赖3D点云和手工设计或学习的局部描述子，而近年兴起的绝对位姿回归（APR）方法虽速度快，但精度长期落后于结构化方案。NeRF作为强大的隐式场景表示，理论上能同时提供场景几何与外观信息，但现有基于NeRF的定位方法要么需要联合训练匹配任务（如**CrossFire**，Moreau et al., 2023），要么依赖可泛化NeRF融合多视图特征（如**NeRFLoc**，Liu et al., ICRA 2023），无法直接利用标准视图合成训练的NeRF作为唯一场景表示。

本文的核心洞察是：**NeRF在视图合成过程中学习到的中间层特征天然蕴含场景的几何与外观信息，可直接作为有效的3D点描述符用于2D-3D匹配，无需修改NeRF模型本身**。基于此，作者提出**NeRFMatch**——一个匹配Transformer，通过自注意力和交叉注意力机制对齐查询图像的2D特征与预训练NeRF的冻结3D特征，并设计了轻量级变体**NeRFMatch-Mini**以权衡速度与精度。

实验表明，NeRFMatch在Cambridge Landmarks室外基准上达到平均中位误差13.3cm/0.3°，超越所有APR方法，并与当前最优的NeRF匹配方法NeRFLoc（13.0cm/0.2°）基本持平，同时大幅优于CrossFire（约47cm/0.7°）。在7-Scenes室内基准上，NeRFMatch取得2.7cm/0.7°的平均误差，与NeFeS（2.4cm/0.9°）相当，但落后于基于场景坐标回归的经典方法DSAC*（1.1cm/0.3°），揭示了NeRF在密集帧序列中重建质量不足的瓶颈。消融实验进一步证实：使用NeRF中间层特征f³作为描述子（中位平移27.9cm）显著优于直接使用3D坐标或位置编码（>458cm），且具有良好几何重建能力的MipNeRF骨干（13.3cm）远优于Instant NGP（28.1cm），说明NeRF的几何表达质量是匹配成功的关键前提。



视觉定位（Visual Localization）要求在已知场景中从单张查询图像恢复精确的 6-DoF 相机位姿，是自动驾驶、增强现实和机器人导航的核心能力。传统结构方法依赖显式 3D 点云和手工设计或学习的局部描述子（如 SIFT、SuperPoint），通过建立 2D-3D 匹配并求解 PnP 实现高精度定位，但需要存储庞大的图像数据库和 3D 模型，部署成本高昂。绝对位姿回归（APR）方法直接学习从像素到位姿的映射，存储开销极小，但精度长期落后于结构方法。

近年来，神经辐射场（NeRF）凭借其紧凑的场景表示能力和逼真的视图合成质量，为视觉定位提供了新的可能性——若能直接利用 NeRF 的内部特征进行 2D-3D 匹配，则无需额外存储图像数据库或 3D 点云。然而，现有基于 NeRF 的定位方法存在一个关键瓶颈：它们要么需要联合训练 NeRF 与匹配任务（如 **CrossFire** 联合训练 Instant-NGP 与特征预测分支），要么依赖可泛化 NeRF 融合多视图图像特征生成 3D 描述子（如 **NeRFLoc**）。这些方法无法直接使用标准视图合成目标下预训练的 NeRF 特征，限制了 NeRF 作为“唯一场景表示”的简洁性和复用性。

本文的核心动机正是打破这一限制：能否从一个仅以视图合成训练的 NeRF 中提取内部特征，直接作为 3D 点描述符，从而无需修改 NeRF 模型本身即可实现高质量的 2D-3D 匹配？这一思路的关键洞察在于，NeRF 在视图合成过程中学习到的中间层特征已蕴含场景的几何与外观信息，具备作为匹配描述子的潜力。基于此，本文提出 **NeRFMatch**——一个匹配 Transformer，通过自注意力和交叉注意力机制直接对齐 2D 图像特征与冻结的 3D NeRF 特征，并配合图像检索与位姿精化模块构建完整的层次化定位管线。



## 核心方法与创新机理

### 1. 从“联合训练”到“冻结复用”：NeRF 特征的独立定位价值

现有基于 NeRF 的视觉定位方法存在一个根本性瓶颈：它们要么需要**联合训练** NeRF 与匹配任务（如 **CrossFire**（Moreau et al., 2023）在 Instant-NGP 上附加特征预测分支），要么依赖**可泛化 NeRF** 融合多视图图像特征来生成 3D 描述子（如 **NeRFLoc**（Liu et al., ICRA 2023））。这些范式使得 NeRF 无法作为“即插即用”的场景表示——每次更换场景或调整匹配策略，都需要重新训练整个管线。

本工作的核心洞察在于：**标准视图合成训练得到的 NeRF，其内部中间层特征天然蕴含丰富的场景几何与外观信息，可直接作为 3D 点描述符用于 2D-3D 匹配**。基于此，NeRFMatch 实现了两个关键的 **changed slots**：

| 组件 | 基线方法 | NeRFMatch |
|------|----------|-----------|
| **3D 点特征** | 手工描述子（SIFT）或从真实图像数据库提取的学习描述子，与 3D 点云绑定存储 | 从预训练 NeRF 中间层提取的冻结特征 $f^j$，无需额外训练或存储图像数据库 |
| **匹配范式** | 联合训练 NeRF 与匹配任务，或使用可泛化 NeRF 融合多视图特征 | 冻结 NeRF 模型，使用独立训练的匹配 Transformer 对齐 2D 图像与 3D NeRF 特征 |

这一设计将 NeRF 从“需要定制的训练组件”解放为“通用的 3D 场景特征提取器”，是方法家族中的**范式级转变**。

### 2. 匹配 Transformer：跨域特征的注意力对齐

NeRFMatch 的第二个关键创新是**匹配 Transformer 架构**。与轻量级版本 NeRFMatch-Mini 的不可学习双 softmax 匹配不同，完整版 NeRFMatch 引入了**共享权重的自注意力与交叉注意力模块**（Fig. 3）：

- **共享自注意力权重**：将图像特征与 NeRF 特征映射到共同的嵌入空间，弥合 2D 图像域与 3D NeRF 特征域之间的模态鸿沟；
- **粗-细匹配范式**：先在粗粒度层面通过双 softmax 获得图像块与 3D 点的对应关系，再在细粒度层面对每个图像块内部生成热力图，取期望值得到亚像素级精确匹配。

消融实验（Table 4）证实了这一设计的有效性：NeRFMatch 全注意力版本达到平均 **13.3cm / 0.3°** 的中位误差，而 NeRFMatch-Mini 为 **20.0cm / 0.4°**，可学习注意力模块带来了约 **34%** 的平移精度提升。

### 3. 位姿精化：闭合匹配-渲染的反馈回路

NeRFMatch 的第三个创新是**利用 NeRF 的可微分渲染能力实现位姿精化**，形成“匹配→求解→渲染→再匹配”的闭环：

- **迭代精化（Iterative Refinement）**：用更新后的位姿重新渲染 3D 点及其 NeRF 特征，再次执行匹配，逐步收敛；
- **优化精化（Optimization-based Refinement）**：通过光度误差优化位姿后再匹配，适用于轻量级 NeRFMatch-Mini。

Fig. 4 显示，迭代精化将 NeRFMatch 的平均误差从 **16.5cm / 0.3°** 降至 **14.2cm / 0.3°**，召回率从 **71.3%** 提升至 **78.2%**。这一机制将 NeRF 从“一次性特征提取器”升级为“可迭代优化的场景表示”，充分利用了 NeRF 的连续表示能力。

### 4. 方法家族定位

NeRFMatch 在视觉定位方法谱系中占据一个独特位置：

- **相对于结构方法（如 HLoc、PixLoc）**：避免了显式 3D 点云和图像数据库的存储需求，仅需 NeRF 模型权重；
- **相对于场景坐标回归（SCR）方法（如 DSAC\*、ACE）**：不直接回归 3D 坐标，而是通过匹配建立显式 2D-3D 对应，具有更强的可解释性；
- **相对于现有 NeRF 定位方法（CrossFire、NeRFLoc）**：首次证明**标准 NeRF 的冻结特征**即可胜任定位，无需修改 NeRF 训练管线。

在 Cambridge Landmarks 上，NeRFMatch 达到 **13.3cm / 0.3°** 的平均中位误差，超越所有 APR 方法，并在 NeRF 匹配方法中达到领先水平（Table 1）。在 7-Scenes 上达到 **2.7cm / 0.7°**，与 **NeFeS**（Chen et al., 2023）基本持平（Table 2）。



![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2403_09577/figures/001_Figure_1.jpg]]
*Figure 1: NeRF-based localization overview. In this work, we propose to use NeRF as our scene representation for visual localization. Given a query image, we first retrieve its nearest reference pose using image retrieval, then use NeRFMatch to establish 2D-3D correspondences between the query image and the NeRF scene points to compute an initial pose estimate and finally improve its accuracy via pose refinement*

NeRFect Match 提出一个三阶段层次化视觉定位流水线，以预训练的 NeRF 模型作为唯一的场景表示。流水线将查询图像映射到绝对相机位姿，核心思路是通过冻结的 NeRF 中间层特征直接建立 2D-3D 对应，无需对 NeRF 进行任何修改或联合训练。

**输入**：一张查询图像，以及一个预训练的 NeRF 场景模型和一组预缓存的参考位姿（通常为 NeRF 训练时使用的相机位姿）。

**三阶段流水线**（见 Fig. 1）：

1. **图像检索**：使用 NetVLAD 全局描述子在参考图像数据库（真实图像或 NeRF 合成图像）上检索最邻近的参考位姿，为后续匹配提供粗粒度的初始相机位姿。室外场景检索 top-1 或 top-10 参考位姿，室内场景使用 top-1。

2. **NeRFMatch 匹配**：根据检索到的参考位姿，通过体渲染从 NeRF 中生成一组 3D 表面点及其对应的 NeRF 特征图。同时，使用 ConvFormer 编码器提取查询图像的两级（粗/细）特征图。匹配 Transformer（NeRFMatch）通过自注意力和交叉注意力对齐 2D 图像特征与 3D NeRF 特征，经粗-细匹配范式输出 2D 像素与 3D 点的对应关系。轻量级变体 NeRFMatch-Mini 则使用不可学习的双 softmax 匹配函数直接匹配特征图。

3. **位姿求解与精化**：从 2D-3D 匹配集合中通过 PnP 解算器计算初始绝对相机位姿。可选的位姿精化模块支持两种策略——**迭代精化**（用更新后的位姿重新渲染 NeRF 并再次匹配）和**优化精化**（通过光度误差优化位姿后再匹配）。迭代精化为 NeRFMatch 的默认精化方式，优化精化则为 NeRFMatch-Mini 的默认方式。

**关键设计决策**：整个流水线中 NeRF 模型完全冻结，仅匹配网络需要训练。NeRF 的中间层特征 $f^3$ 被选为默认的 3D 描述子——消融实验表明，该层特征蕴含的几何与外观信息远超原始 3D 坐标或位置编码（中位平移 27.9cm vs >458cm，Table 3）。这一设计使得标准视图合成训练的 NeRF 可直接复用为定位场景表示，避免了 CrossFire 等方法的联合训练需求，也无需 NeRFLoc 的多视图特征融合。



### 整体定位流水线

NeRFMatch 的定位系统由三个核心阶段构成（Fig. 1）：**图像检索**提供粗粒度的参考位姿；**NeRFMatch 匹配网络**在查询图像与 NeRF 场景点之间建立 2D-3D 对应关系，解算初始位姿；**位姿精化**模块通过迭代或优化方式进一步提升定位精度。其中，匹配网络是整个系统的核心创新所在。

### NeRF 特征提取模块

标准 NeRF 模型（Fig. 2）将 3D 点 $X$ 和视线方向 $d$ 映射为体密度 $\sigma$ 和颜色 $c$。给定 3D 点 $X$，其在第 $j$ 层 3D 编码器的中间特征定义为：

$$f^j = \theta_x^j \circ \cdots \circ \theta_x^1(P_x(X))$$

其中 $P_x$ 为位置编码函数，$\theta_x^i$ 为第 $i$ 层编码器。这些中间层特征 $f^j$ 蕴含了场景的几何与外观信息，是后续 2D-3D 匹配的关键描述子。消融实验（Table 3）表明，中间层特征 $f^3$ 的定位精度最佳（中位平移误差 27.9 cm），而直接使用 3D 坐标或位置编码作为特征时误差高达 458 cm 以上，证明 NeRF 内部特征确实编码了丰富的场景结构信息。

### 体渲染模块

沿光线 $r$ 的体渲染通过加权求和实现。颜色渲染公式为：

$$\hat{C}(r) = \sum_{i=1}^{N} w_i c_i, \quad w_i = T_i (1 - e^{-\delta_i \sigma_i})$$

其中 $T_i = \exp(-\sum_{k=1}^{i-1} \delta_k \sigma_k)$ 为累积透射率，$\delta_i$ 为采样步长，$\sigma_i$ 和 $c_i$ 分别为第 $i$ 个采样点的体密度和颜色。

类似地，3D 表面点 $\hat{X}(r)$ 及其对应的第 $j$ 层 NeRF 描述子 $\hat{F}^j(r)$ 沿光线的渲染公式为：

$$\hat{X}(r) = \sum_{i=1}^{N} w_i X_i, \quad \hat{F}^j(r) = \sum_{i=1}^{N} w_i f_i^j$$

该模块将离散的采样点及其特征融合为连续的 3D 表面点与描述子，为后续匹配提供 3D 侧的输入。

### 匹配网络模块

NeRFMatch 提供两种匹配架构（Fig. 3），共享相同的特征提取流程：

- **2D 特征编码**：使用 ConvFormer 提取查询图像的粗粒度特征图 $F_m^c$ 和细粒度特征图。
- **3D 特征获取**：根据参考位姿渲染一组 3D 表面点及其对应的 NeRF 特征图 $F_s$。

**NeRFMatch-Mini** 采用非学习的双 softmax 匹配函数，直接将 $F_s$ 与 $F_m^c$ 进行匹配，速度快但精度有限。

**NeRFMatch（全匹配模型）** 引入可学习的注意力粗-细匹配范式：
- **粗匹配**：对图像特征和 NeRF 特征施加共享权重的自注意力（SA）和交叉注意力（CA），将来自两个不同域的特征映射到公共嵌入空间，再通过双 softmax 获得图像块与 3D 点的粗匹配。
- **细匹配**：在粗匹配基础上，对每个图像块内的局部区域生成热力图，取期望值得到亚像素级精确对应。

### 损失函数

**粗匹配损失** 采用对数损失，增大正确匹配位置的 softmax 概率：

$$L_c = -\frac{1}{|\mathcal{M}_{gt}|}\sum_{(i,j)\in\mathcal{M}_{gt}}\log(S(i,j))$$

其中 $\mathcal{M}_{gt}$ 为真实粗匹配集合，$S(i,j)$ 为双 softmax 输出的匹配概率。

**细匹配损失** 使用逆方差加权的像素距离：

$$L_f = \frac{1}{|\mathcal{M}_f|}\sum_{(i,j)\in\mathcal{M}_f}\frac{1}{\sigma^2(i)}||\tilde{x}_j - x_j||_2$$

其中 $\mathcal{M}_f$ 为细匹配集合，$\tilde{x}_j$ 为预测的像素位置，$x_j$ 为真实位置，$\sigma^2(i)$ 为热力图的方差，用于自适应加权不同匹配点的置信度。

NeRFMatch-Mini 仅使用 $L_c$ 监督，而 NeRFMatch 使用 $L_c + L_f$ 联合监督。消融实验（Table 4）表明，全注意力匹配模块显著优于轻量版本（平均误差 13.3 cm / 0.3° vs 20.0 cm / 0.4°），验证了可学习匹配模块的有效性。

### 位姿精化模块

位姿精化提供两种可选方案：
- **迭代精化**：用当前估计位姿重新渲染 NeRF 特征并再次匹配，逐步收敛。对 NeRFMatch 效果显著，可将平均误差从 16.5 cm / 0.3° 降至 14.2 cm / 0.3°，召回率从 71.3% 提升至 78.2%（Fig. 4）。
- **优化精化**：通过最小化光度误差优化位姿后再匹配，更适合 NeRFMatch-Mini。



## 实验与关键发现

### 核心实验设置

实验在户外数据集 **Cambridge Landmarks** 和室内数据集 **7-Scenes** 上进行。对于 Cambridge，使用 top-1/10 参考位姿进行检索；对于 7-Scenes，使用 top-1。7-Scenes 的训练帧数限制为每场景 900 帧，这可能影响 NeRF 重建质量并间接降低定位精度。训练图像对采用与 **PixLoc**（Sarlin et al., CVPR 2021）相同的共视性图像对，保证对比的公平性。NeRF 训练时使用语义分割去除天空和行人等动态物体，以提升重建质量。定位评估采用与传统结构方法一致的 PnP 解算器。

### 户外定位主结果

Table 1 报告了 Cambridge Landmarks 上的逐场景中位平移和旋转误差。**NeRFMatch** 取得平均中位误差 13.3 cm / 0.3°，超越所有 APR（绝对位姿回归）方法，并在基于 NeRF 的匹配方法中达到领先水平。与同样使用 NeRF 进行 2D-3D 匹配的 **CrossFire**（Moreau et al., 2023，平均约 47 cm / 0.7°）相比，NeRFMatch 大幅领先；与基于可泛化 NeRF 的 **NeRFLoc**（Liu et al., ICRA 2023，13.0 cm / 0.2°）相比，平移略差 0.3 cm、旋转略差 0.1°，但仍具有竞争力。轻量级 **NeRFMatch-Mini** 取得 20.0 cm / 0.4°，与大多数场景坐标回归（SCR）方法相当。


![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2403_09577/figures/004_Table_1.jpg]]
*Table 1: Outdoor localization on Cambridge Landmarks [32]. We report perscene median rotation and position errors in ( c m ,$^ { \circ }$ ) and its average across scenes*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2403_09577/figures/012_Table_1.jpg]]
*Table 1: NeRF PSNR scores. We present the PSNR scores for our trained MipNeRF models on each scene of Cambridge Landmarks [32] and 7-Scenes [57]*

### 室内定位主结果

Table 2 展示了 7-Scenes（SfM poses）上的结果。**NeRFMatch** 取得 2.7 cm / 0.7°，与 **NeFeS**（Chen et al., 2023，2.4 cm / 0.9°）基本持平，但明显落后于基于 SCR 的方法如 **DSAC\***（Brachmann et al., TPAMI 2021，1.1 cm / 0.3°）和 **ACE**（Brachmann et al., CVPR 2023）。这一性能差距的核心瓶颈在于：7-Scenes 的密集帧序列下 NeRF 重建质量受限，且训练帧数限制进一步加剧了这一问题。


![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2403_09577/figures/005_Table_2.jpg]]
*Table 2: Indoor localization on 7-Scenes [57]. We report per-scene median rotation and position errors in $\left$( c m ,$^ { \circ } \right$) and their average across scenes, along with averaged localization recall

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2403_09577/figures/013_Table_2.jpg]]
*Table 2: Runtime. We show runtime of NeRFMatch-Mini and NeRFMatch. For pose refinement we are using optimization refinement for NeRFMatch-Mini and iterative refinement for NeRFMatch*

### NeRF 特征消融

Table 3 的核心发现是：**使用 NeRF 中间层特征作为 3D 描述子是定位精度的决定性因素**。在 NeRFMatch-Mini 上，使用中间层特征 $f^3$ 取得中位平移 27.9 cm，而直接使用 3D 点坐标（Pt3D）或位置编码（Pe3D）作为特征时，中位平移超过 458 cm。这证明 NeRF 在视图合成中学习到的内部特征蕴含丰富的场景几何与外观信息，远非简单的坐标或位置编码所能替代。基于此，$f^3$ 被选为 NeRFMatch 系列的默认 NeRF 特征。


![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2403_09577/figures/006_Table_3.jpg]]
*Table 3: NeRF feature ablation on Cambridge [32]. We train NeRFMatch-Mini with different 3D features and compare their localization performance*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2403_09577/figures/014_Table_3.jpg]]
*Table 3: NeRF backbone ablation on Cambridge Landmarks. We compare NeRFMatch-Mini and NeRFMatch performances using Instant NGP*

### NeRF 骨干网络消融

Supplementary Table 3 揭示了 NeRF 骨干网络对定位性能的关键影响：**使用 MipNeRF 作为骨干的 NeRFMatch 取得 13.3 cm，而使用 Instant NGP 时仅为 28.1 cm**。这一显著差距（超过 2 倍）说明具有良好几何重建能力的 NeRF 对于 2D-3D 匹配任务至关重要。MipNeRF 的多尺度抗锯齿特性使其在复杂场景中能提供更准确的几何和外观信息，而 Instant NGP 的哈希编码虽速度快但几何表达能力不足。

### 匹配架构消融

Table 4 对比了 NeRFMatch 与 NeRFMatch-Mini 的架构差异。**NeRFMatch 的全注意力粗-细匹配模块显著优于 Mini 的非可学习双 softmax 匹配**：全注意力版本取得 13.3 cm / 0.3°（召回率 71.3%），而 Mini 版本为 20.0 cm / 0.4°（召回率 59.2%）。这验证了可学习的自注意力和交叉注意力机制在跨域特征对齐（2D 图像特征 ↔ 3D NeRF 特征）中的关键作用。


![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2403_09577/figures/007_Table_4.jpg]]
*Table 4: NeRFMatch architecture ablation on Cambridge Landmarks [32]. We report averaged median pose error in ( c m ,$^ { \circ }$ ) and localization recall*

### 位姿精化消融

Figure 4 展示了迭代精化（Iterative）与优化精化（Optimization-based）的性能对比。**对于 NeRFMatch，迭代精化效果最佳**：将平均中位误差从 16.5 cm / 0.3° 降至 14.2 cm / 0.3°，召回率从 71.3% 提升至 78.2%，且计算时间更短。对于 NeRFMatch-Mini，优化精化更为适合。迭代精化的核心机制是：用更新后的位姿重新渲染 NeRF 特征并再次匹配，形成“匹配-求解-重渲染”的闭环，逐步收敛到更精确的位姿。


![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2403_09577/figures/009_Figure_4.jpg]]
*Figure 4: Refinement ablation on Cambridge Landmarks [32]. On the left side, we depict the average recall for optimization-based (Opt+Match) and iterative (Iter) refinement approaches across multiple iterations. We provide results for both the NeRF-Match and its minimal setting. On the right side, we report averaged median pose error in $\left$( c m /$^ { \circ } \right$) and localization recall with the best refinement configurations

### 推理延迟分析

Supplementary Table 2 报告了各模块的推理时间。NeRF 渲染每帧耗时 **141 ms**，是系统的最大瓶颈。匹配网络方面，NeRFMatch-Mini 仅需 37 ms，而 NeRFMatch 需 157 ms。加上位姿精化（Mini 398 ms，NeRFMatch 141 ms），整体延迟距离实时应用仍有较大差距。主要优化方向在于 NeRF 渲染加速（如缓存、层次化采样）和匹配网络的轻量化。

### 失败模式与局限

1. **室内场景性能不足**：NeRFMatch 在 7-Scenes 上明显落后于 SCR 方法，根因是密集帧序列下 NeRF 重建质量有限，导致 3D 特征判别力不足。
2. **NeRF 重建质量依赖**：当完全依赖 NeRF 合成图像进行检索时，在复杂室外场景下定位性能轻微退化，原因为 NeRF 对细微细节和动态光照的合成能力有限。
3. **场景泛化缺失**：当前匹配网络仅在单场景上训练，未见跨场景泛化能力的验证。
4. **弱纹理场景脆弱性**：严重依赖精确的相机位姿训练 NeRF，在弱纹理或重复纹理场景中 NeRF 重建质量有限，导致定位精度下降。



## 定位与知识库关联

### 核心方法定位

NeRFMatch 的核心贡献在于将 **预训练 NeRF 的中间层特征直接作为 3D 场景描述子**，通过匹配 Transformer 建立 2D 图像与冻结的 3D NeRF 特征之间的对应关系。这一设计在视觉定位领域的方法谱系中占据了一个独特位置：它既不同于传统的基于显式 3D 点云的结构定位方法，也不同于需要联合训练 NeRF 与匹配任务的现有 NeRF 定位方案。

### 与结构定位方法的关系

传统的结构定位方法依赖显式 3D 模型（通常由 SfM 生成的点云），并在其上绑定手工设计或学习的 2D 描述子。**HLoc**（Sarlin et al., CVPR 2019）使用 SuperPoint + SuperGlue 建立 2D-3D 匹配，代表了该范式的成熟方案；**PixLoc**（Sarlin et al., CVPR 2021）进一步通过端到端特征学习优化了这一流程。NeRFMatch 与这些方法的根本区别在于 **3D 场景表示的本质**：前者使用稀疏点云 + 图像数据库，后者使用隐式神经辐射场。这一差异带来了两个关键优势：(1) NeRFMatch 无需存储真实图像数据库，仅需 NeRF 模型权重和参考位姿列表；(2) NeRF 特征通过体渲染自然编码了场景的几何与外观信息，无需手工特征工程。

然而，在室内场景（7-Scenes）上，NeRFMatch 的定位精度（2.7cm/0.7°）明显落后于场景坐标回归（SCR）方法如 **DSAC\***（Brachmann et al., TPAMI 2021, 1.1cm/0.3°）和 **ACE**（Brachmann et al., CVPR 2023）。这一差距的根源在于 NeRF 在密集帧序列中的重建质量限制——SCR 方法直接学习像素到 3D 坐标的映射，不依赖中间 3D 重建步骤，因此在室内纹理丰富场景中具有天然优势。

### 与 NeRF 定位方法的关系

现有基于 NeRF 的定位方法可大致分为两类：

**第一类**需要联合训练 NeRF 与匹配/定位任务。**CrossFire**（Moreau et al., 2023）在 Instant-NGP 上添加特征预测分支以建立 2D-3D 匹配，但该方法修改了 NeRF 训练目标，无法复用标准视图合成训练的 NeRF 模型。NeRFMatch 的核心突破在于**解耦 NeRF 训练与匹配网络训练**：NeRF 模型完全冻结，匹配 Transformer 独立训练，这使得任何预训练 NeRF 都可直接作为场景表示使用。在 Cambridge Landmarks 上，NeRFMatch 的定位误差（13.3cm/0.3°）远优于 CrossFire（约 47cm/0.7°），验证了这一解耦设计的有效性。

**第二类**使用可泛化 NeRF 融合多视图图像特征。**NeRFLoc**（Liu et al., ICRA 2023）通过融合多视图图像特征生成 3D 描述子，在 Cambridge 上达到 13.0cm/0.2° 的领先水平。NeRFMatch 与之性能基本持平（13.3cm/0.3°），但方法设计理念不同：NeRFLoc 依赖可泛化 NeRF 的多视图特征聚合能力，而 NeRFMatch 证明**标准单场景 NeRF 的内部特征本身已包含足够的 3D 几何信息**用于匹配。

**NeFeS**（Chen et al., 2023）使用 NeRF 特征蒸馏进行绝对位姿回归精化，与 NeRFMatch 的匹配范式形成互补。在 7-Scenes 上，NeRFMatch（2.7cm/0.7°）与 NeFeS（2.4cm/0.9°）性能接近，表明两者在室内场景中面临相似的 NeRF 重建质量瓶颈。

### 适用边界与局限

**场景依赖性**。NeRFMatch 的定位精度高度依赖 NeRF 重建质量。消融实验（补充材料 Table 3）显示，使用 MipNeRF 作为骨干时定位误差为 13.3cm，而使用 Instant NGP 时升至 28.1cm——差距超过 2 倍。这一结果表明，具有良好几何重建能力的 NeRF 变体对于匹配任务至关重要，也意味着在弱纹理或重复纹理场景中，NeRF 重建质量有限将直接导致定位精度下降。

**室内外性能差异**。NeRFMatch 在室外场景（Cambridge, 13.3cm/0.3°）表现优异，但在室内场景（7-Scenes, 2.7cm/0.7°）明显落后于 SCR 方法。7-Scenes 的训练帧数限制为 900 帧/场景，可能影响 NeRF 重建质量，并间接降低定位精度。这一现象揭示了当前方法的适用边界：在可获得高质量 NeRF 重建的场景中，NeRFMatch 具有竞争力；在重建困难或帧数受限的场景中，SCR 方法仍是更优选择。

**实时性限制**。NeRF 每帧渲染耗时 141ms，加上匹配网络（NeRFMatch 157ms, Mini 37ms），整体延迟较高（补充材料 Table 2）。即使使用轻量级 NeRFMatch-Mini，总延迟仍接近 200ms，距离实时应用（< 33ms/帧）仍有较大差距。

**场景泛化能力缺失**。当前模型仅在单场景上训练匹配网络，未见跨场景泛化能力的验证。匹配 Transformer 是否学到场景无关的 2D-3D 对齐能力，还是过度拟合特定场景的 NeRF 特征分布，仍是一个开放问题。

### 开放问题与后续方向

**室内定位精度的提升路径**。如何在不牺牲精度的前提下提升室内场景的定位能力？结合不确定性估计以过滤低质量匹配，或使用更精确的深度图辅助 NeRF 重建，可能是可行的改进方向。

**系统实时化**。能否通过缓存渲染结果、层次化索引参考位姿或引入 GPS 先验加速图像检索步骤，使整体系统接近实时？NeRF 渲染本身的计算瓶颈也需要更高效的采样策略或轻量级 NeRF 变体来缓解。

**场景无关匹配器**。能否将匹配网络设计为场景无关的形式，复用到一个通用的 NeRF 特征匹配器中？这需要验证 NeRF 中间层特征在不同场景间是否具有一致的语义-几何编码模式。

**更强 NeRF 骨干的潜力**。更强的 NeRF 变体（如 Block-NeRF、Urban Radiance Fields）能否直接提升大场景定位性能？这些方法在处理大规模室外场景时的重建质量优势，可能自然转化为定位精度的提升。

**多传感器融合**。如何融合惯性测量等传感器信息，降低对视觉检索质量的依赖？当完全依赖 NeRF 合成图像进行检索时，复杂室外场景下定位性能轻微退化（因 NeRF 对细微细节和动态光照的合成能力有限），多传感器融合可提供冗余的粗定位先验。



## 原文 PDF

![[paperPDFs/ECCV_2024/The_NeRFect_Match_Exploring_NeRF_Features_for_Visual_Localization.pdf]]
