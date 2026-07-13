---
title: Consistent Instance Field for Dynamic Scene Understanding
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Consistent_Instance_Field_for_Dynamic_Scene_Understanding.pdf
project_link: null
code_link: null
aliases:
- CIFC
- CIFDSU
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入显式的 4D 时空占位概率 π(x,t) 和条件实例分布 p(x,t,k)，将物理存在与身份解耦；再通过学习校准因子和实例引导重采样，使身份建模超越可见性偏差，实现稳定的跨时空实例一致性。
primary_logic: 将动态场景建模为一个由持久实体构成的连续概率场，每个时空点同时编码“是否存在”和“属于哪个实例”，从而在变形和视角变化下维持连贯的语义描述。
claims:
- 在 HyperNeRF 数据集上，CIF 将新视角全景分割的平均 mIoU 提升 11.42（79.47 vs. VLGS 68.05），mAcc-inst 提升 11.78。
- 消融实验证实，去除身份校准和实例引导重采样会导致语义漂移和 mIoU 大幅下降，仅完整模型保持几何与语义的最佳平衡。
- HyperNeRF (novel-view panoptic segmentation) 上 mIoU (平均交并比) = 79.47
- HyperNeRF (novel-view panoptic segmentation) 上 mAcc-pix (像素平均精度) = 96.40
---

# Consistent Instance Field for Dynamic Scene Understanding

> [!tip] 核心洞察
> 将动态场景建模为一个由持久实体构成的连续概率场，每个时空点同时编码“是否存在”和“属于哪个实例”，从而在变形和视角变化下维持连贯的语义描述。

| 字段 | 内容 |
|------|------|
| 中文题名 | 一致实例场：动态场景理解 |
| 英文题名 | Consistent Instance Field for Dynamic Scene Understanding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.14126) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Consistent Instance Field (CIF) |
| Dataset | HyperNeRF, Neu3D |

> [!tip] 效果简介
> - HyperNeRF (novel-view panoptic segmentation) 上，mIoU (平均交并比) 79.47 vs 68.05 (VLGS) (+11.42)；mAcc-pix (像素平均精度) 96.40 vs 94.31 (VLGS) (+2.09)。
> - Neu3D (novel-view panoptic segmentation) 上，mIoU 88.31 vs 82.49 (VLGS) (+5.82)；mAcc-inst (实例平均精度) 93.19 vs 90.69 (VLGS) (+2.50)。
> - HyperNeRF (open-vocabulary 4D querying) 上，mIoU (平均) 84.90 vs 57.83 (SA4D) (+27.07)。

## 概要

动态场景理解的核心挑战在于，如何在物体变形、相机运动和遮挡变化的条件下，保持对场景中各个实例的稳定、一致的语义描述。现有方法——例如基于可变形 3D Gaussian 的 **SA4D**、**4D LangSplat** 以及 **VLGS**——普遍依赖视角相关的 RGB 调制特征来推断语义，这带来了三个结构性缺陷：第一，实例身份与表面辐射特性耦合，导致同一物体在不同视角下被赋予不一致的身份；第二，将颜色的透明度（alpha）直接等同于物理占位，混淆了“可见”与“存在”；第三，高斯体的空间分布由初始几何密度决定，语义活跃区域可能容量不足，造成边界模糊和实例碎片化。

本文提出 **Consistent Instance Field (CIF)**，一种面向动态场景的连续概率时空场形式化。其核心思想是将场景建模为一个由持久实体构成的 4D 联合分布，每个时空点 $(x,t)$ 同时编码“是否存在物体”以及“该物体属于哪个实例”。具体而言，CIF 将联合分布分解为物理占位概率 $\pi(x,t)$ 和条件实例分布 $p(x,t,k)$，从而在模型层面将存在性与身份解耦。这一连续场通过一组携带占位和身份参数的**可变形高斯体**离散化实现，并经由**场感知 Splatting** 可微渲染为像素级实例身份图，接受来自 2D 掩码的监督。

为克服可见性偏差对身份估计的干扰，CIF 引入**实例身份校准**机制：先用 2D 掩码聚合每个高斯体的渲染参与权重得到粗身份估计，再通过学习逐高斯-实例的校准因子 $m_i^k$ 对其进行重标定，使得被遮挡或视角边缘的高斯体也能获得正确的身份归属。进一步地，**实例引导重采样**根据联合响应 $\gamma_i^k = \pi_i p_i^k$ 识别语义弱区和强区，将弱语义高斯体自适应迁移至强语义区域，并通过体积守恒的透明度调整保持辐射场稳定，从而在变形和视角变化下维持连贯的语义描述。

实验在两个动态场景基准上验证了 CIF 的有效性。在新视角全景分割任务中，CIF 在 **HyperNeRF** 数据集上取得了 79.47 的平均 mIoU，较 **VLGS** 的 68.05 提升 11.42；在 **Neu3D** 数据集上达到 88.31 mIoU，较 VLGS 提升 5.82。开放词汇 4D 查询任务中，CIF 以 84.90 的平均 mIoU 大幅领先 **SA4D** 的 57.83。消融实验进一步证实，独立占位建模、身份校准和实例引导重采样三者缺一不可：移除任一组件均会导致语义漂移、边界模糊和跨视角一致性下降。



随着神经渲染技术的快速演进，动态场景理解已成为计算机视觉领域的核心挑战之一。现有方法在静态场景的语义分割与三维重建上取得了显著进展，但将这些能力迁移至动态场景时，普遍面临一个根本性瓶颈：**实例身份与表面外观的耦合**。

以 **SA4D** 为代表的基于可变形 3D Gaussian Splatting 的动态语义方法，以及 **VLGS**、**4D LangSplat** 等开放词汇语义表征方法，均依赖视角相关的 RGB 调制特征来编码语义信息。这种设计将实例身份与表面辐射属性绑定在一起，导致三个连锁问题：

1. **跨视角身份不一致**：由于语义特征随视角变化而改变，同一实例在不同视角下可能被赋予不同的身份标签，难以维持时空连贯的语义描述。
2. **对遮挡敏感**：当实例被部分遮挡时，可见表面特征不足以代表完整的实例身份，渲染结果在遮挡边界处容易出现语义断裂。
3. **颜色透明度与物理占位的混淆**：现有方法以 RGB 透明度 α 作为可见性权重，缺乏独立的物理存在性表示。这使得透明或半透明物体（如玻璃杯、水面）的语义区域代表性不足，模型难以区分“该处有物体但透明”与“该处无物体”。

这些问题的根源在于，现有方法缺乏一个**将物理存在与语义身份显式解耦**的建模框架。理想情况下，动态场景应被理解为一个由持久实体构成的连续概率场——每个时空点同时编码“是否存在物体”和“该物体属于哪个实例”。这种解耦使得身份建模能够超越可见性偏差，在变形和视角变化下维持稳定的语义一致性。

基于上述动机，本文提出 **Consistent Instance Field (CIF)**，一种面向动态场景的连续概率时空形式化框架。CIF 的核心洞察在于：将动态场景建模为 4D 联合分布 $\gamma(\mathbf{x}, t, k) = P(E=1, K=k \mid \mathbf{x}, t)$，并将其分解为占位概率 $\pi(\mathbf{x}, t)$ 和条件实例分布 $p(\mathbf{x}, t, k)$ 的乘积。通过这一解耦，CIF 在可变形 Gaussian 表示的基础上，引入独立占位建模、身份校准和实例引导重采样三个关键模块，系统性地解决了上述瓶颈问题。



## 核心方法与创新机理

### 瓶颈与突破口

现有动态场景语义方法（如 **SA4D**、**4D LangSplat**、**VLGS**）普遍依赖视角相关的 RGB 调制特征来刻画实例身份。这一设计将“是什么”与“看起来如何”深度耦合，产生三重结构性缺陷：① 身份随视角漂移，跨视角监督信号相互矛盾；② 颜色透明度 $\alpha$ 被同时用于表示可见性和物理存在，导致透明/反光材质处身份模糊；③ 高斯容量按初始几何密度固定分配，语义关键区域可能代表性不足，边界破碎。

CIF 的突破口在于将动态场景重新定义为**一个连续的概率场**——在每一个时空点 $(\mathbf{x}, t)$ 上，同时回答两个问题：“这里有没有东西？”和“如果有，它属于哪个实例？”。这一形式化将物理存在与语义身份彻底解耦，使身份建模超越可见性偏差，为跨时空一致性提供了概率基础。

### 关键改动槽位

**1. 物理占位建模：从透明度到存在概率**

基线方法将 $\alpha$ 既用作渲染权重，又隐式充当“存在性”指标。当物体透明或高光反射时，$\alpha$ 偏低，系统会误判该区域“无物”，导致实例身份丢失。

CIF 为每个高斯体显式附加独立的占位概率 $\pi_i \in [0,1]$，与颜色透明度 $\alpha_i$ 解耦。$\pi_i$ 编码物理存在与否，$\alpha_i$ 仅负责辐射传输。渲染时，像素对实例 $k$ 的软归属图由两者共同决定：

$$\mathbf{M}_k(u,v,t) = \sum_i T_i^{\mathrm{inst}}(u,v,t) \, \pi_i \, P_i(u,v,t) \, p_i^k$$

其中 $T_i^{\mathrm{inst}}$ 是融入占位权重的透射率。消融实验证实，用恒定占位或透明度替代 $\pi_i$ 均导致 mIoU 显著下降（Table 3），验证了独立占位建模的必要性。

**2. 实例身份表征与校准：消除可见性偏差**

基线方法通常基于渲染权重对 2D 掩码进行硬分配或简单聚合。这导致一个根本性偏差：从某视角看，被遮挡的高斯体参与权重低，其身份信号被压制，即使它在物理上属于该实例。

CIF 维护每个高斯体的归一化条件身份分布 $p_i^k$，并通过两阶段估计消除偏差。首先从多视角 2D 掩码聚合“粗身份” $\hat{p}_i^k$，再引入可学习的逐高斯-实例校准因子 $m_i^k > 0$ 进行重标定：

$$p_i^k = \frac{\hat{p}_i^k \, m_i^k}{\sum_{k'} \hat{p}_i^{k'} \, m_i^{k'}}$$

$m_i^k$ 在训练中自动学习，补偿因遮挡、视角倾斜等造成的系统性低估。去除该校准模块后，高斯身份受可见性偏差支配，跨视角一致性恶化（Table 3, w/o Identity Calibration）。

**3. 语义容量分配：实例引导重采样**

初始化的高斯体按几何结构分布，语义密集区（如物体边界、精细部件）可能容量不足，而空旷背景却占用大量高斯。这导致分割边界模糊、小实例被吞并。

CIF 引入**实例引导重采样**机制。定义每个高斯体对实例 $k$ 的联合响应 $\gamma_i^k = \pi_i \, p_i^k$，据此构造强弱采样分布：

$$P_{\mathrm{weak}}(i|k) \propto (\gamma_i^k)^{-1}, \quad P_{\mathrm{strong}}(i|k) \propto \gamma_i^k$$

对每个实例，从其弱响应高斯中采样移除，从强响应区域采样复制，将表示容量从语义贫瘠区重定向至语义富集区。复制时通过体积守恒调整透明度：

$$\alpha_{\mathrm{src}}^{\mathrm{new}} = 1 - (1 - \alpha_{\mathrm{src}})^{1/(n+1)}$$

确保局部辐射贡献不变。消融实验中，关闭重采样导致语义区容量不足、边界模糊（Table 3, w/o Instance-Guided Resampling）；完整模型在 split-cookie 场景达到最高 mIoU 86.03 和 PSNR 32.42，兼顾几何保真度与语义一致性（Table 3 Full, Figure 6）。

### 创新总结

CIF 的三个改动槽位形成闭环：**占位解耦**提供干净的物理存在信号，**身份校准**消除视角偏差以获得稳定身份，**引导重采样**将有限的高斯容量动态聚焦于语义关键区。三者共同支撑起一个在变形和视角变化下维持连贯语义描述的 4D 实例一致性场。



CIF 将动态场景建模为一个定义在 4D 时空域上的**一致实例场**（Consistent Instance Field），其核心是一个联合编码“物理存在性”与“实例身份”的连续概率场。如图 2 所示，整个 pipeline 由四个关键模块串联构成：场形式化与高斯表征、实例身份估计与校准、实例引导重采样，以及场感知 Splatting 渲染。

**输入与场定义**。给定多视角视频序列，CIF 将每个时空点 $(\mathbf{x}, t)$ 映射为一个联合分布 $\gamma(\mathbf{x}, t, k) = P(E{=}1, K{=}k \mid \mathbf{x}, t)$，表示该点被实例 $k$ 占据的概率。这一联合分布被显式分解为占位概率 $\pi(\mathbf{x}, t)$ 和条件身份分布 $p(\mathbf{x}, t, k)$（Eq. 2），从根本上将“物体是否存在”与“存在时属于哪个实例”解耦，避免了现有方法将身份与视角相关的 RGB 透明度 $\alpha$ 耦合所带来的跨视角不一致。

**离散化表征**。连续场通过一组**实例嵌入式可变形高斯** $\mathcal{G} = \{ g_i \}$ 进行离散化（Sec. 3.1.2）。每个高斯体 $g_i$ 除了携带几何（中心 $\mathbf{x}_i$、旋转 $\mathbf{R}_i$、尺度 $\mathbf{s}_i$）、颜色 $\mathbf{c}_i$ 和透明度 $\alpha_i$ 外，还显式附加了两个概率量：占位概率 $\pi_i$ 和归一化的身份分布 $\{p_i^k\}_{k=1}^K$。这种设计使每个高斯原语成为局部场量的载体，为后续的语义推理和容量调控提供了统一的参数化基础。

**身份估计与校准**。从 2D 实例掩码出发，系统通过聚合各高斯在训练视图中的渲染参与权重，得到粗身份估计 $\hat{p}_i^k$（Eq. 6-7）。由于渲染权重受遮挡和视角偏差影响，粗估计并不可靠。为此，CIF 引入一组可学习的逐高斯-实例校准因子 $m_i^k > 0$，通过加权归一化将粗身份校正为无偏的身份分布 $p_i^k$（Eq. 8），使身份建模超越可见性线索，实现跨时空的稳定指派。

**容量重分配**。为将有限的表征容量聚焦于语义显著区域，CIF 根据实例联合响应 $\gamma_i^k = \pi_i p_i^k$ 构造强弱采样分布（Eq. 9）。弱响应高斯被概率性地重定位至强响应区域，并通过体积守恒的透明度调整（Eq. 10-11）保持局部辐射特性不变，形成密集的对象对齐高斯簇。

**渲染与监督**。在渲染阶段，Field-Aware Splatting 将每个高斯的占位 $\pi_i$ 和身份 $p_i^k$ 纳入透射率计算，合成像素级实例身份图 $\mathbf{M}_k(u,v,t)$（Eq. 4），并通过交叉熵损失 $\mathcal{L}_{\mathrm{inst}}$ 与 2D 掩码监督对齐，与 RGB 重建损失 $\mathcal{L}_{\mathrm{rgb}}$ 联合端到端优化（Eq. 12）。

**模块间数据流**。场形式化为身份估计提供概率语义基础；身份估计的输出 $p_i^k$ 与占位 $\pi_i$ 共同构成实例响应 $\gamma_i^k$，驱动重采样模块调整高斯分布；重采样后的高斯集最终通过场感知 Splatting 渲染为语义图和 RGB 图像，损失梯度反向传播至所有参数，形成闭环优化。这种设计使物理占位、身份推断和容量分配相互解耦又协同工作，共同维持动态场景下的几何-语义一致性。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2512_14126/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our Consistent Instance Field. Our method models each dynamic scene as a continuous 4D Consistent Instance Field that encodes existence and identity distributions (Sec. 3.1.1). We realize the field as an Instance-Embedded Gaussian Representation, which jointly models geometry, appearance, occupancy, and instance identity (Sec. 3.1.2). (Bottom) Instance Identity Estimation. Per-Gaussian identity distributions are inferred by aggregating 2D observations over time and views. A learnable calibration then corrects visibility-induced biases (Eqs. (6), (7), (8)), yielding stable identity under occlusion and appearance changes (Sec. 3.2). (Right) Instance-Guided Resampling. To align rep...*



CIF 将动态场景建模为一个连续的概率场，其核心由四个紧密耦合的模块构成：场形式化、身份估计与校准、实例引导重采样，以及场感知 Splatting 渲染。

### 一致实例场形式化

CIF 的核心是一个定义在 4D 时空上的联合分布，描述任意时空点 $(\mathbf{x}, t)$ 属于实例 $k$ 的概率：

$$\gamma(\mathbf{x}, t, k) = P(E=1, K=k \mid \mathbf{x}, t) \tag{1}$$

该联合分布被显式分解为两个独立因子：

$$\gamma(\mathbf{x}, t, k) = \underbrace{P(E=1 \mid \mathbf{x}, t)}_{\pi(\mathbf{x}, t)} \; \underbrace{P(K=k \mid E=1, \mathbf{x}, t)}_{p(\mathbf{x}, t, k)} \tag{2}$$

其中 $\pi(\mathbf{x}, t)$ 是**占位概率**，编码该时空点是否存在物理实体；$p(\mathbf{x}, t, k)$ 是**条件实例分布**，表示在存在实体的前提下该点属于实例 $k$ 的概率。这一解耦是方法的核心因果杠杆：它将物理存在与语义身份分离，避免了现有方法中透明度 $\alpha$ 同时承担可见性和占位双重职责所带来的混淆。

### 实例嵌入式高斯表示

连续场通过一组可变形高斯体离散化。每个高斯体 $g_i$ 不仅携带几何与外观参数，还显式附加了占位概率 $\pi_i$ 和归一化的身份分布 $p_i^k$：

$$\mathcal{G} = \{ g_i = ( \mathbf{x}_i, \mathbf{R}_i, \mathbf{s}_i, \mathbf{c}_i, \alpha_i, \pi_i, p_i^1, \dots, p_i^K ) \}_{i=1}^N$$

其中 $\pi_i \approx \pi(\mathbf{x}_i(t), t)$，$p_i^k \approx p(\mathbf{x}_i(t), t, k)$。这使得每个高斯体成为局部概率载体，为后续的身份估计和容量重分配提供了统一的参数化基础。

### 场感知 Splatting 渲染

为实现像素级语义监督，CIF 设计了 Field-Aware Splatting。对于每个像素 $(u,v)$ 在时刻 $t$，实例 $k$ 的边缘身份图通过加权合成得到：

$$\mathbf{M}_k(u,v,t) = \sum_i T_i^{\mathrm{inst}}(u,v,t) \; \pi_i \; P_i(u,v,t) \; p_i^k \tag{4}$$

其中 $P_i(u,v,t)$ 是高斯体在像素上的投影权重，$T_i^{\mathrm{inst}}$ 是考虑占位和身份权重的累积透射率。与标准 alpha 合成仅输出 RGB 不同，该渲染器同时输出每个实例的软归属图，使得交叉熵损失可以直接作用于语义场。

### 实例身份估计与可见性校准

身份估计模块从 2D 实例掩码中聚合每个高斯体在不同视角和时间下的渲染参与权重，形成粗身份估计 $\hat{p}_i^k$。然而，由于遮挡和视角偏差，仅依赖渲染权重的聚合会导致身份估计偏向可见表面。CIF 引入可学习的**逐高斯-实例校准因子** $m_i^k > 0$ 进行纠正：

$$p_i^k = \frac{\hat{p}_i^k \, m_i^k}{\sum_{k'} \hat{p}_i^{k'} \, m_i^{k'}} \tag{8}$$

该归一化校准使得身份建模能够超越可见性偏差，在遮挡和外观变化下维持跨视角一致性。

### 实例引导重采样

为将高斯容量与语义信号对齐，CIF 定义每个高斯体对实例 $k$ 的**联合响应** $\gamma_i^k = \pi_i \, p_i^k$，并据此构造强弱采样分布：

$$P_{\mathrm{weak}}(i|k) \propto (\gamma_i^k)^{-1}, \quad P_{\mathrm{strong}}(i|k) \propto \gamma_i^k \tag{9}$$

对于每个实例，从其弱响应高斯中采样并移除，同时在强响应区域复制高斯体。复制后通过体积守恒调整透明度：

$$\alpha_{\mathrm{src}}^{\mathrm{new}} = \alpha^{\mathrm{new}} = 1 - (1 - \alpha_{\mathrm{src}})^{1/(n+1)} \tag{10}$$

这一机制将语义代表性不足区域的高斯容量重新分配至语义活跃区域，在保持辐射场几何保真度的同时形成稠密的物体对齐簇。

### 联合训练目标

整个框架通过端到端优化联合损失函数训练：

$$\mathcal{L} = \mathcal{L}_{\mathrm{rgb}} + \lambda_{\mathrm{inst}} \mathcal{L}_{\mathrm{inst}} \tag{12}$$

其中 $\mathcal{L}_{\mathrm{rgb}}$ 为 RGB L1 重建损失，$\mathcal{L}_{\mathrm{inst}}$ 为作用于渲染身份图 $\mathbf{M}_k$ 的交叉熵损失，$\lambda_{\mathrm{inst}}$ 为平衡权重。所有参数——包括高斯几何、外观、占位概率 $\pi_i$、身份分布 $p_i^k$ 以及校准因子 $m_i^k$——均通过该目标联合优化。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2512_14126/figures/001_Figure_1.jpg]]
*Figure 1: Comparisons with prior work SA4D [16]. Previous methods like SA4D often rely on view-dependent features with RGB modulation, leading to semantic inconsistencies in dynamic scenes: unstable under cross-view instance supervision, confusing color opacity with object occupancy, and underrepresenting semantically meaningful regions. Our approach formulates a continuous probabilistic field over existence and identity in space-time, enabling identity modeling beyond visibility cues and adaptive redistribution of Gaussian capacity. This results in a coherent instance field across deformation and changing viewpoints*



## 实验与关键发现

### 核心实验设置

CIF 的 Field-Aware Splatting 模块以 CUDA 实现，其余组件基于 PyTorch。每场景先以 10,000 次迭代重建几何与外观，再以 3,000 次迭代进行实例分割联合优化，优化器统一使用 Adam。评估覆盖两个主要基准：**HyperNeRF**（含真实实例标注）和 **Neu3D**（无真实标注，使用 DEVA 生成伪标签并通过伪单目序列拼接实现跨视图 ID 统一）。Neu3D 仅保留全视野可见实例参与评估，可能高估绝对性能，但相对排序仍有参考价值。

### 主实验结果

#### HyperNeRF 新视角全景分割

Table 1 汇总了 HyperNeRF 数据集上的定量对比。CIF 在三个核心指标上全面超越现有方法：

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2512_14126/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison of our method with the state-of-the-art on novel-view panoptic segmentation using the HyperNeRF [41] dataset. We report mAcc-pix, mAcc-inst, and mIoU metrics. The best , second best , and third best results are highlighted*

- **mIoU**：平均 79.47，较第二名 VLGS（68.05）提升 **+11.42**，较 SA4D（51.64）提升 +27.83。
- **mAcc-inst**：平均 85.69，较 VLGS（73.91）提升 **+11.78**，表明实例级身份一致性显著增强。
- **mAcc-pix**：平均 96.40，较 VLGS（94.31）提升 +2.09，像素级精度同样最优。

在最具挑战性的 *split-cookie* 场景（涉及物体分裂与交互），CIF 取得 86.03 mIoU 和 32.42 PSNR，兼顾几何保真度与语义一致性。Figure 3 的定性对比显示，CIF 在遮挡和外观变化下仍能产生更锐利、更连贯的分割边界，而 SA4D 和 VLGS 在物体交界处出现明显的身份混淆和边界模糊。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2512_14126/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison of our method with the state-of-the-art on novel-view panoptic segmentation using the Hyper-NeRF [41] dataset. For clarity, we crop and slightly zoom in on representative regions around the manipulated objects. Our approach produces noticeably sharper and more coherent segmentations, even under occlusion and appearance variations*

#### Neu3D 新视角全景分割

Table 2 报告了 Neu3D 数据集上的结果。CIF 继续保持领先：

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2512_14126/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison of our method with the state-of-the-art on novel-view panoptic segmentation using the Neu3D [26] dataset. We report mAcc-pix, mAcc-inst, and mIoU metrics. The best , second best , and third best results are highlighted*

- **mIoU**：88.31，较 VLGS（82.49）提升 **+5.82**。
- **mAcc-inst**：93.19，较 VLGS（90.69）提升 +2.50。
- **mAcc-pix**：94.97，较 VLGS（90.25）提升 +4.72。

Figure 4 的定性结果表明，CIF 在多相机环绕拍摄的复杂场景中能产生更平滑的物体边界、更干净的背景分离以及更一致的跨视角实例身份。Trace3D 和 Dr.Splat 在实例边界处存在明显的语义泄漏，而 CIF 的占位-身份解耦机制有效抑制了此类伪影。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2512_14126/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison of our method with the state-of-the-art on novel-view panoptic segmentation using the Neu3D [26] dataset. As described in Sec. 4.1, to avoid the inherent inconsistencies in the ground truth, we consider only instances that are visible across all camera views. Our method produces smoother boundaries, cleaner backgrounds, and more consistent object identities*

#### 开放词汇 4D 查询

Table S1 展示了 HyperNeRF 上开放词汇查询的定量结果。CIF 平均 mIoU 达 **84.90**，远超 SA4D（57.83），提升幅度达 **+27.07**。4D LangSplat 在部分场景（如 *americano*）完全无法定位文本查询对应的物体（标记为 *），而 CIF 在所有场景均稳定输出。Figure 5 的定性对比进一步表明，即使面对透明玻璃杯和反光金属壶等挑战性材质，CIF 仍能准确分离实例边界。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2512_14126/figures/012_Table_S.1.jpg]]
*Table S.1: Quantitative comparison of our method with the state-of-the-art on open-vocabulary 4D querying using the HyperNeRF dataset. We report mAcc and mIoU metrics. The best, second best, and third best results are highlighted. * indicates failure of localizing the objects based on the text queries, as also demonstrated in Figure 5 of the main paper*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2512_14126/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison of our method with the state-of-the-art on open-vocabulary 4D querying using the HyperNeRF [41] dataset. For clarity, we crop and zoom in on the central regions. Our method produces clearer boundaries and more accurate instance separation, even under transparent and reflective materials such as the glass cup and steel jug*

### 消融实验

Table 3 和 Figure 6 在 *split-cookie* 场景上系统消融了三个核心设计：

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2512_14126/figures/008_Table_3.jpg]]
*Table 3: Ablation study. We evaluate our method under different configurations on the “split-cookie” scene from HyperNeRF [41]*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2512_14126/figures/009_Figure_6.jpg]]
*Figure 6: Ablation study. We present the corresponding qualitative results for each configuration shown in Table 3*

| 配置 | mIoU | mAcc-pix | PSNR |
|------|------|----------|------|
| Full CIF | **86.03** | 97.93 | **32.42** |
| w/o Identity Calibration | 下降 | 下降 | 相近 |
| w/o Instance-Guided Resampling | 下降 | 下降 | 相近 |
| Constant Occupancy (π=0.02) | 明显下降 | 下降 | 相近 |
| Opacity as Occupancy | 明显下降 | 下降 | 相近 |

**占位建模的必要性**：用恒定值或透明度替代独立占位概率 π_i 均导致 mIoU 大幅下降，验证了物理存在与颜色透明度解耦的关键作用。透明度受视角和材质影响，无法可靠编码物体是否真实占据空间。

**身份校准的作用**：去除可学习的校准因子 m_i^k 后，高斯身份分布完全由渲染权重聚合的 2D 掩码决定，受可见性偏差支配，跨视角一致性显著恶化。

**实例引导重采样的贡献**：关闭重采样后，语义活跃区域的高斯容量不足，导致边界模糊和实例内部空洞，mIoU 明显降低。完整模型通过将弱语义高斯重定位至强语义区域，在维持 PSNR 的同时最大化语义精度。

Figure 6 的定性消融可视化直观展示了各配置的分割质量差异：仅完整模型在物体分裂与交互的复杂动态中保持连贯、锐利的实例边界。

### 失败模式与局限性

1. **非刚性材质建模困难**：当前可变形高斯表示难以有效建模烟、液体等无固定结构的动态材质。此类场景中，身份指派的可解释性降低，占位概率的物理含义也变得模糊。
2. **跨视图伪标签不一致**：Neu3D 的实例掩码依赖 DEVA 生成并通过伪单目序列同步，在严重遮挡下仍可能出现跨视图 ID 错配，影响身份估计的精度上限。
3. **开放词汇评估缺乏标准基准**：4D 查询任务使用 Grounded DINO 生成的 2D 掩码作为伪真值，边界精度受语言模型区域理解能力限制，定量结果存在近似偏差。
4. **对初始几何重建的依赖**：CIF 的语义优化建立在预训练的几何高斯场之上，若初始重建质量不足（如极端稀疏视角），语义场也会受到连带影响。



## 定位与知识库关联

### 动态场景语义建模的演进脉络

动态场景的语义理解经历了从逐帧处理到时空统一建模的演进。早期方法依赖独立 2D 分割器逐帧生成掩码，再通过后处理关联，缺乏跨时空的连贯性。随着 NeRF 和 3D Gaussian Splatting (3DGS) 的发展，研究者开始将语义信息嵌入辐射场或高斯表示中。

**SA4D** 将可变形 3D Gaussian 与 2D 分割模型结合，通过逐帧掩码向高斯体传播语义标签，实现动态场景的语义分割与跟踪。然而，该方法依赖视角相关的 RGB 调制特征，将实例身份与表面辐射耦合，导致身份跨视角不一致，且对遮挡敏感。**4D LangSplat** 将语言嵌入扩展到动态场景，通过 4D Gaussian 表示支持开放词汇查询，但同样面临颜色透明度与物理占位混淆的问题，语义区域代表性不足。**VLGS** 在静态场景中展示出强大的开放词汇 3D 语义表征能力，但缺乏对动态变形和跨视角身份一致性的显式建模。**Trace3D** 利用 2D 掩码和轨迹约束优化 Gaussian 语义，**Dr.Splat** 则聚焦于基于语义的 4D 编辑，两者均未从根本上解决存在性与身份的耦合问题。

CIF 的核心突破在于将动态场景建模为一个由持久实体构成的连续概率场。通过引入显式的 4D 时空占位概率 $\pi(\mathbf{x}, t)$ 和条件实例分布 $p(\mathbf{x}, t, k)$，CIF 将物理存在与身份解耦——这是区别于所有前述方法的关键设计。基于此，身份校准和实例引导重采样两大机制使身份建模超越可见性偏差，实现稳定的跨时空实例一致性。

### 方法谱系中的定位

在动态场景理解的方法谱系中，CIF 处于“概率场建模”与“可微分高斯渲染”的交汇点。其理论基础——将场景视为存在性与身份的联合概率场——与传统的基于渲染权重聚合语义的方法形成根本性差异。

**与基于辐射场的方法对比**：NeRF 类方法通常将语义作为附加的颜色通道或特征向量进行 alpha 合成，缺乏对“该点是否真正被物体占据”的显式建模。CIF 的占位概率 $\pi_i$ 与透明度 $\alpha_i$ 解耦，使得即使在高透明区域（如玻璃杯），模型仍能正确推断物理存在性。

**与基于 3DGS 的方法对比**：SA4D 和 VLGS 等 3DGS 方法将语义标签视为高斯体的附加属性，通过渲染权重加权聚合。这种硬分配或简单聚合策略对可见性偏差敏感——从某一视角观察到的语义分布可能不代表该高斯体的真实身份。CIF 通过可学习校准因子 $m_i^k$ 纠正由渲染权重估计的粗身份，消除了这一系统性偏差。

**与 4D 语言嵌入方法对比**：4D LangSplat 将 CLIP 等语言特征嵌入到 4D Gaussian 中，支持文本驱动的查询。CIF 的 Field-Aware Splatting 渲染出的边缘实例身份图 $M_k$ 同样可服务于开放词汇查询，但其概率基础使得查询结果更具物理可解释性。

### 适用边界与局限性

CIF 的当前设计存在明确的适用边界：

**非刚性材质的建模困难**：CIF 基于可变形高斯表示，每个高斯体假设具有明确的空间位置和协方差。对于烟、液体等无固定结构的非刚性材质，这种局部基元表示难以有效建模，身份指派的可解释性也随之降低。这是 3DGS 类方法的共性局限。

**多视图伪标签的依赖**：CIF 的实例身份估计依赖 DEVA 生成的 2D 掩码，并通过伪单目序列拼接实现跨视图一致身份。在严重遮挡场景下，DEVA 的逐帧分割可能产生身份断裂，进而影响高斯体的身份校准精度。论文在 Neu3D 数据集上仅保留全视野可见实例进行评估，这在一定程度上规避而非解决了该问题。

**开放词汇评估的近似性**：开放词汇 4D 查询目前缺乏标准化基准。论文采用 Grounded DINO 生成的 2D 掩码作为伪真值，依赖语言模型的区域理解，边界可能不精确。这导致定量评估（如 Table S1 中 SA4D 在部分场景的失败标注）存在近似偏差。

### 开放问题与未来方向

基于 CIF 的现有框架，以下几个方向值得探索：

1. **无定形动态材质的扩展**：能否将实例一致性场扩展至烟雾、水流等无定形动态材质？这可能需要引入非局部的场表示，或结合粒子系统与概率场建模。

2. **鲁棒的跨视图伪标签融合**：当前的多视图同步策略在严重遮挡下仍可能出现不一致。设计更鲁棒的融合策略——例如引入时序平滑约束或基于光流的身份传播——可进一步提升身份估计精度。

3. **标准化的 4D 开放词汇评估协议**：建立标准化的 4D 开放词汇查询评估协议和数据集，将有助于公平比较不同方法，推动领域的健康发展。

4. **实例场的编辑与交互**：CIF 的显式占位与身份解耦为场景编辑提供了自然的接口——修改 $\pi_i$ 可控制物体的存在性，修改 $p_i^k$ 可改变物体身份。探索基于 CIF 的 4D 编辑应用是一个有前景的方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/Consistent_Instance_Field_for_Dynamic_Scene_Understanding.pdf]]
