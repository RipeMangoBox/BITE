---
title: "PAGE-4D: Disentangled Pose and Geometry Estimation for VGGT-4D Perception"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/PAGE_4D_Disentangled_Pose_and_Geometry_Estimation_for_VGGT_4D_Perception.pdf
project_link: null
code_link: null
openreview_forum_id: Nfmzp5PBzr
aliases:
- P4
- PAGE-4D
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "动态感知聚合器（Dynamics-Aware Aggregator）通过预测动态掩码，并以任务特定的方式将其注入交叉注意力中——对相机位姿令牌抑制动态区域，对几何令牌则保留动态信息——从而解耦二者对动态内容的依赖。"
primary_logic: "不应将动态场景中的运动信息视为统一有害或有用，而应根据下游任务的角色进行差异化利用：消除其对位姿的噪声影响，同时保留其对几何的线索作用。"
claims:
- "VGGT在动态场景中精度显著下降，动态区域绝对深度误差比静态区域高94%。"
- "直接抑制动态patch间的交叉注意力可以提升相机位姿估计，但会严重损害几何重建。"
- "动态像素对应关系引入了对极几何残差，该残差量化了动态运动对位姿估计的破坏程度。"
- "引入动态感知聚合器后，PAGE-4D在Sintel上相机位姿ATE从0.214降至0.143，视频深度Abs Rel从0.484降至0.357。"
---

# PAGE-4D: Disentangled Pose and Geometry Estimation for VGGT-4D Perception

> [!tip] 核心洞察
> 不应将动态场景中的运动信息视为统一有害或有用，而应根据下游任务的角色进行差异化利用：消除其对位姿的噪声影响，同时保留其对几何的线索作用。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PAGE-4D：面向VGGT-4D感知的解耦位姿与几何估计 |
| 英文题名 | PAGE-4D: Disentangled Pose and Geometry Estimation for VGGT-4D Perception |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Nfmzp5PBzr) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PAGE-4D |
| Dataset | Sintel, Tum |

> [!tip] 效果简介
> - Sintel 上，Video Depth Abs Rel (scale) 为 0.357，对比 0.484 (VGGT)，变化 -0.127。
> - Sintel 上，Video Depth δ<1.25 (scale) 为 0.699，对比 0.553 (VGGT)，变化 +0.146。
> - Sintel 上，Camera Pose ATE 为 0.143，对比 0.214 (VGGT)，变化 -0.071。

## 概要

PAGE-4D 是一种前馈式4D感知模型，旨在将 VGGT（Wang et al., CVPR 2025a）从静态场景扩展至动态场景，同时估计相机位姿、视频深度与3D点云，无需任何后处理优化。该工作源于一个根本性发现：**动态场景中位姿估计与几何重建存在结构性冲突**——位姿估计依赖静态对极几何约束，需抑制动态区域；而几何重建则需要利用动态物体的运动信息。原始 VGGT 在动态场景中倾向于忽略动态内容，导致动态区域绝对深度误差比静态区域高出94%。

为解耦这一冲突，PAGE-4D 提出了**动态感知聚合器（Dynamics-Aware Aggregator）**，其核心机制是通过预测动态掩码，并以任务特定的方式注入交叉注意力：对相机位姿令牌抑制动态区域以降低对极几何干扰，对几何令牌则保留动态信息以辅助重建。这一设计使得模型能够差异化利用运动信息——消除其对位姿的噪声影响，同时保留其对几何的线索作用。

在方法定位上，PAGE-4D 并非从零训练，而是采用**针对性微调策略**：仅更新 VGGT 中间10层全局注意力层（约30%参数），冻结其余编码器与解码器，从而高效适配动态场景。模型移除了原始 VGGT 的点跟踪头，因其不适配动态场景。

主要实验结果表明，在 Sintel 数据集上，PAGE-4D 将相机位姿 ATE 从 VGGT 的 0.214 降至 **0.143**，将尺度对齐的视频深度 Abs Rel 从 0.484 降至 **0.357**。在 TUM 上相机位姿 ATE 从 0.028 降至 **0.016**；在 DyCheck 上点云重建精度 Acc Mean 从 1.051 降至 **0.403**。消融实验证实，仅微调中间层即可达到全模型微调的性能，而加入动态掩码注意力后所有指标进一步提升。学习到的动态掩码可在无显式监督下有效突出运动物体。



### 动态场景感知的兴起与前馈模型的瓶颈

从多帧RGB图像中联合恢复相机位姿与三维场景几何是计算机视觉的核心问题，其应用涵盖自动驾驶、机器人导航和增强现实等领域。近年来，以DUSt3R（Wang et al., CVPR 2024）为代表的前馈式3D重建方法取得了显著进展——它们无需后处理优化即可从图像对中直接预测深度图和点云，在静态场景上表现出色。VGGT（Wang et al., CVPR 2025a）将这一范式从两帧扩展到多帧，通过全局注意力机制融合跨帧信息，同时输出相机参数、深度、点图和跟踪特征，成为前馈4D感知的重要基线。

然而，现实世界充满动态物体——行人、车辆、动物等运动目标普遍存在。当这些前馈模型被部署到动态场景时，一个根本性的冲突浮出水面：**位姿估计依赖静态对极几何约束，需要抑制动态区域带来的噪声；而几何重建则需要利用动态物体的运动信息来恢复其三维结构。** 原始VGGT在动态场景中精度显著下降——在Odyssey测试集上，动态区域的绝对深度误差比静态区域高出94%，且其注意力图可视化显示模型倾向于忽略动态内容。这一观察揭示了现有前馈模型的核心瓶颈：它们将动态信息统一视为有害信号，缺乏对位姿与几何两个子任务差异化需求的建模。

### 动态运动如何破坏对极几何

为理解这一瓶颈的数学本质，可分析动态场景中像素对应关系的变化。在静态刚性场景假设下，参考帧像素 $\mathbf{x}_r$ 在目标帧的对应位置由深度 $D_r$、相机相对旋转 $\mathbf{R}_{tr}$ 和平移 $\mathbf{t}_{tr}$ 唯一确定：

$$\mathbf{x}_t = \mathbf{K} [\mathbf{R}_{tr} D_r(\mathbf{x}_r) \mathbf{K}^{-1} \mathbf{x}_r + \mathbf{t}_{tr}]$$

该对应满足对极约束 $\tilde{\mathbf{x}}_t^\top \mathbf{E} \tilde{\mathbf{x}}_r = 0$，其中 $\mathbf{E} = [\mathbf{t}_{tr}]_\times \mathbf{R}_{tr}$ 是本质矩阵。然而，当场景中存在物体运动位移 $\mathbf{M}_{tr}$ 时，像素对应变为：

$$\mathbf{x}_t = \mathbf{K} [\mathbf{R}_{tr} D_r(\mathbf{x}_r) \mathbf{K}^{-1} \mathbf{x}_r + \mathbf{t}_{tr}] + \mathbf{K} \mathbf{M}_{tr}$$

此时对极约束不再成立，产生的**动态对极残差**为：

$$\delta(\mathbf{x}_r) \equiv \tilde{\mathbf{x}}_t^\top \mathbf{E} \tilde{\mathbf{x}}_r \approx \frac{1}{Z_r} \mathbf{n}(\mathbf{x}_r)^\top \Delta\mathbf{X}_\perp(\mathbf{x}_r)$$

该残差量化了动态运动对位姿估计的破坏程度：残差越大，基于对极几何的位姿优化受到的干扰越强。这从理论上解释了为何VGGT在动态区域精度骤降——其全局注意力机制将所有patch同等对待，动态区域的对极违例被不加区分地注入跨帧信息融合中。

### 动机：解耦而非统一抑制

一个直接的补救思路是抑制动态patch间的交叉注意力（即DD-MSK策略），使模型仅关注静态区域。实验表明，这一策略确实能改善相机位姿估计，但代价是几何重建质量急剧下降——动态物体的深度和点云精度严重受损。这一发现揭示了一个关键洞见：**动态场景中的运动信息不应被统一视为有害或有用，而应根据下游任务的角色进行差异化利用——消除其对位姿的噪声影响，同时保留其对几何重建的线索作用。**

这一洞察驱动了PAGE-4D的设计：通过一个动态感知聚合器（Dynamics-Aware Aggregator），以任务特定的方式解耦动态内容——对相机位姿令牌抑制动态区域，对几何令牌则保留动态信息，从而在同一前馈框架内同时提升位姿估计和几何重建的精度。



## 核心方法与创新机理

PAGE-4D 的核心创新在于揭示并解决了一个根本性冲突：**动态场景中位姿估计与几何重建对动态信息的需求是互斥的**。位姿估计依赖静态对极几何约束，动态运动产生的像素位移会破坏该约束，因此需要抑制动态区域；而几何重建恰好需要利用这些运动信息来恢复动态物体的三维结构。原始 VGGT 在动态场景中倾向于忽略动态内容，导致动态区域的绝对深度误差比静态区域高出 **94%**（Section 3.1）。

基于这一洞察，PAGE-4D 提出了三个关键机制：

### 1. 动态感知聚合器（Dynamics-Aware Aggregator）

这是方法的核心组件，包含一个动态掩码预测模块和任务特定的掩码注意力机制。掩码预测模块通过线性映射和深度卷积头从 Stage 1 输出的 patch token 中预测动态区域 logits，再经可学习的温度 $\tau$ 和缩放因子 $\alpha$ 转换为软掩码：

$$\widetilde{\mathbf{M}} = \boldsymbol{\alpha} \cdot \boldsymbol{\sigma}\big( \frac{\mathbf{m}}{\tau} \big) \in \mathbb{R}^{B \times S \times (H \cdot W)}$$

关键在于掩码的**非对称应用**：在 Stage 2 的 Dynamics-Aware Global Attention 中，对相机位姿令牌和注册令牌施加掩码以抑制动态区域的注意力，而对深度和点云相关的几何令牌则不施加掩码，保留动态信息。这种任务特定的解耦直接回应了前述冲突——消除动态对位姿的噪声影响，同时保留其对几何的线索作用。

### 2. 选择性微调策略

与全模型微调不同，PAGE-4D 仅更新 VGGT 聚合器中**中间 10 层全局注意力层**，冻结其余聚合器和解码器层，仅调整约 30% 的参数。消融实验证实，仅微调中间层即可达到与全模型微调相当的性能，而加入动态掩码注意力后所有指标进一步提升（Table 5）。这一发现表明，中间层是跨帧信息融合最关键的阶段，也是动态信息干扰最集中的位置。

### 3. 移除点跟踪头

VGGT 的点跟踪头主要为视图配准设计，不适合动态场景。PAGE-4D 在微调时完全移除该模块，避免不适当的训练信号干扰位姿和几何的联合优化。这一设计选择虽然牺牲了显式的 2D-3D 对应关系，但确保了核心任务在动态条件下的稳定性。

**效果验证**：引入动态感知聚合器后，Sintel 上相机位姿 ATE 从 VGGT 的 0.214 降至 **0.143**，视频深度 Abs Rel 从 0.484 降至 **0.357**（Table 1, 2）；DyCheck 上点云重建 Accuracy 均值从 1.051 降至 **0.403**，降幅超过 60%（Table 3）。此外，学习到的动态掩码在无显式监督的情况下能有效捕捉运动物体（Figure 6），进一步验证了该方法对动态信息解耦的有效性。



![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_Nfmzp5PBzr/figures/001_Figure_1.jpg]]
*Figure 1: PAGE-4D takes a sequence of RGB images depicting a dynamic scene as input and simultaneously predicts the corresponding camera parameters and 3D geometry information—all within a fraction of a second. Compared to VGGT, PAGE-4D produces denser and more accurate point cloud reconstructions with better depth estimation quality. (Best viewed in PDF.)*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_Nfmzp5PBzr/figures/006_Figure_3.jpg]]
*Figure 3: Fine-tuning strategy: Instead of fine-tuning the entire VGGT architecture, we adapt only the middle N _ { 2 } layers of the global attention mechanism, which are most critical for cross-frame information fusion. To further address dynamic scenes, we introduce a dynamics-aware aggregator that predicts a mask to disentangle dynamic and static content*

PAGE-4D 构建于 VGGT（Wang et al., CVPR 2025a）的前馈架构之上，将其从静态场景扩展至动态场景下的联合相机位姿估计、深度预测与点云重建。其核心设计遵循一条清晰的信息流：**逐帧编码 → 动态感知跨帧融合 → 任务特定解码**。

### 输入输出定义

给定包含动态物体的 $N$ 帧 RGB 图像序列 $\{\mathbf{I}_i\}_{i=1}^N$，模型以端到端前馈方式输出每帧的相机参数 $\mathbf{g}_i$、深度图 $\mathbf{D}_i$ 和 3D 点图 $\mathbf{P}_i$。形式上，目标函数为：

$$f\left(\{\mathbf{I}_i\}\right) = \left\{(\mathbf{g}_i, \mathbf{D}_i, \mathbf{P}_i)\right\}_{i=1}^N$$

值得注意的是，原始 VGGT 还输出点跟踪特征 $\mathbf{T}_i$，但 PAGE-4D 移除了点跟踪头——因为 VGGT 的跟踪头专为视图注册设计，并不适合动态场景（Section 3.3）。这一简化使模型专注于位姿与几何两个核心任务。

### 模块构成与信息流

PAGE-4D 由四个关键模块串联构成：

1. **DINO-style Encoder**：预训练的视觉编码器（Zhang et al., 2022a）逐帧提取图像级 token 特征，为后续跨帧交互提供基础表示。

2. **Dynamics-Aware Aggregator（动态感知聚合器）**：这是 PAGE-4D 的核心创新模块，分为三个阶段：
   - **Stage 1（$N_1$ 层）**：每层包含一个 Global Attention 和一个 Frame Attention，初步融合帧内与帧间信息。其输出被送入动态掩码预测模块。
   - **Dynamic Mask Prediction Module**：将 Stage 1 输出的 patch token 通过线性映射 $\phi$ 投影至低维空间，再经深度卷积头生成掩码 logits $\mathbf{m}$，最后通过带可学习温度 $\tau$ 和缩放因子 $\alpha$ 的 sigmoid 转换为软掩码：
     $$\widetilde{\mathbf{M}} = \alpha \cdot \sigma\left(\frac{\mathbf{m}}{\tau}\right) \in \mathbb{R}^{B \times S \times (H \cdot W)}$$
   - **Stage 2（$N_2$ 层）**：每层包含 Dynamics-Aware Global Attention 和 Frame Attention。在 Dynamics-Aware Global Attention 中，掩码以任务特定方式注入交叉注意力：
     $$\operatorname{Attn}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \operatorname{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^\top}{\sqrt{d}} + \widetilde{\mathbf{M}}\right)\mathbf{V}$$
     对**相机位姿令牌**，掩码主动抑制对动态区域的注意力；对**几何令牌**（深度/点图），则不施加掩码，保留动态运动信息。这实现了位姿与几何对动态内容依赖的解耦。
   - **Stage 3（$N_3$ 层）**：与 Stage 1 结构相同的标准 Global/Frame Attention 层，进一步精炼融合后的特征。

3. **Depth Decoder 与 Point Map Decoder**：轻量级解码器，分别从聚合特征中生成深度图 $\mathbf{D}_i$ 和 3D 点图 $\mathbf{P}_i$。

4. **Camera Pose Decoder**：较大的解码器，专门用于估计相机内外参 $\mathbf{g}_i$。

### 微调策略

PAGE-4D 采用**选择性微调**策略：仅更新聚合器中部的 $N_2$ 层（即 Stage 2 的 Dynamics-Aware Global Attention 层），冻结其余聚合器层和解码器层。这使得仅约 30% 的模型参数参与训练，在保持高效的同时实现了与全模型微调相当的性能。这种策略的合理性在于：中间层的全局注意力是跨帧信息融合的关键通道，对动态场景最为敏感。

### 多任务损失

训练采用联合损失函数：

$$\mathcal{L} = \lambda_c \mathcal{L}_{\mathrm{camera}} + \mathcal{L}_{\mathrm{depth}} + \mathcal{L}_{\mathrm{pmap}}$$

其中 $\lambda_c = 5$，相机位姿采用 Huber loss，深度和点图采用不确定性加权损失与梯度正则化项。



### 问题形式化

PAGE-4D 将动态场景的 4D 感知定义为一个前馈映射。给定 $N$ 帧 RGB 图像序列 $\{\mathbf{I}_i\}_{i=1}^N$，模型同时预测每帧的相机参数 $\mathbf{g}_i$、深度图 $\mathbf{D}_i$、3D 点图 $\mathbf{P}_i$ 以及跟踪特征 $\mathbf{T}_i$（实际实现中移除了点跟踪头）：

$$f\left(\{\mathbf{I}_i\}\right) = \left\{\left(\mathbf{g}_i, \mathbf{D}_i, \mathbf{P}_i, \mathbf{T}_i\right)\right\}_{i=1}^N$$

### 动态场景的几何冲突

核心瓶颈源于动态场景中位姿估计与几何重建对运动信息的根本性需求冲突。在静态场景假设下，参考帧像素 $\mathbf{x}_r$ 在目标帧中的对应位置由刚性变换决定：

$$\mathbf{x}_t = \mathbf{K}[\mathbf{R}_{tr} D_r(\mathbf{x}_r) \mathbf{K}^{-1} \mathbf{x}_r + \mathbf{t}_{tr}]$$

其满足对极约束：

$$\tilde{\mathbf{x}}_t^\top \mathbf{E} \tilde{\mathbf{x}}_r = 0, \quad \mathbf{E} = [\mathbf{t}_{tr}]_\times \mathbf{R}_{tr}$$

然而，当场景中存在物体运动时，目标帧像素位置引入额外位移项 $\mathbf{M}_{tr}$：

$$\mathbf{x}_t = \mathbf{K}[\mathbf{R}_{tr} D_r(\mathbf{x}_r) \mathbf{K}^{-1} \mathbf{x}_r + \mathbf{t}_{tr}] + \mathbf{K} \mathbf{M}_{tr}$$

该位移导致对极约束被破坏，产生动态对极残差：

$$\delta(\mathbf{x}_r) \equiv \tilde{\mathbf{x}}_t^\top \mathbf{E} \tilde{\mathbf{x}}_r \approx \frac{1}{Z_r} \mathbf{n}(\mathbf{x}_r)^\top \Delta\mathbf{X}_\perp(\mathbf{x}_r)$$

其中 $Z_r$ 为深度，$\mathbf{n}(\mathbf{x}_r)$ 为对极平面的法向量，$\Delta\mathbf{X}_\perp(\mathbf{x}_r)$ 为动态位移在对极平面法向上的分量。该残差量化了动态运动对位姿估计的破坏程度——残差越大，基于静态假设的位姿估计所受干扰越强。

### 动态感知聚合器

PAGE-4D 的核心创新是动态感知聚合器（Dynamics-Aware Aggregator），其设计遵循一个关键洞察：**动态信息不应被统一对待，而应根据下游任务进行差异化利用**——对位姿估计抑制动态噪声，对几何重建保留运动线索。

聚合器由三个阶段构成：
- **Stage 1**（$N_1$ 层）：标准全局注意力 + 帧注意力，初步融合跨帧信息
- **动态掩码预测模块**：接收 Stage 1 输出，预测动态区域掩码
- **Stage 2**（$N_2$ 层）：动态感知全局注意力 + 帧注意力，实现任务特定的信息解耦
- **Stage 3**（$N_3$ 层）：标准全局注意力 + 帧注意力

#### 动态掩码预测

动态掩码预测模块对 Stage 1 输出的 patch 特征 $\mathbf{z}_p$ 进行线性投影 $\phi(\cdot)$，随后通过深度卷积头生成掩码 logits $\mathbf{m}$：

$$\mathbf{m} = \text{ConvDepthwise}(\phi(\mathbf{z}_p))$$

引入可学习温度参数 $\tau$ 和缩放因子 $\alpha$，将 logits 转换为软掩码：

$$\widetilde{\mathbf{M}} = \alpha \cdot \sigma\left(\frac{\mathbf{m}}{\tau}\right) \in \mathbb{R}^{B \times S \times (H \cdot W)}$$

其中 $\sigma$ 为 sigmoid 函数，$B$ 为 batch 大小，$S$ 为序列帧数，$H \cdot W$ 为每帧 patch 数。温度 $\tau$ 控制掩码的软硬程度，缩放因子 $\alpha$ 调节抑制强度——两者均通过端到端训练学习，无需显式动态标注。

#### 任务特定的掩码注意力

动态掩码以加性方式注入交叉注意力 logits：

$$\text{Attn}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^\top}{\sqrt{d}} + \widetilde{\mathbf{M}}\right) \mathbf{V}$$

**关键设计**在于掩码的非对称应用：
- **相机位姿估计**：对相机令牌和注册令牌的查询，$\widetilde{\mathbf{M}}$ 主动抑制对动态区域的注意力，强制模型依赖静态几何线索求解位姿
- **深度与点云重建**：对几何相关 patch，不施加掩码，保留动态区域的完整信息以利于几何推断

该设计从机制层面解耦了位姿与几何对动态内容的依赖，使同一骨干网络能同时服务于两个相互冲突的目标。

### 对比方案：DD-MSK

作为消融对比，论文还分析了另一种掩码策略 DD-MSK（Dynamic-Dynamic Mask），其通过动态特征掩码的外积构造自注意力抑制矩阵：

$$\mathcal{M}_{\text{DD-MSK}} = \mathcal{M}_{\text{Dynamic}} \cdot \mathcal{M}_{\text{Dynamic}}^\top$$

该策略阻止动态 patch 之间的自注意力交互，但允许动态 patch 关注静态区域。实验表明，DD-MSK 可改善位姿估计，但严重损害几何重建质量——这进一步验证了任务特定解耦的必要性。

### 损失函数

模型采用多任务联合损失进行端到端训练：

$$\mathcal{L} = \lambda_c \mathcal{L}_{\text{camera}} + \mathcal{L}_{\text{depth}} + \mathcal{L}_{\text{pmap}}$$

其中 $\mathcal{L}_{\text{camera}}$ 为相机位姿的 Huber 损失，$\mathcal{L}_{\text{depth}}$ 和 $\mathcal{L}_{\text{pmap}}$ 分别为深度图和点图的不确定性加权损失（含梯度正则化项）。相机损失权重设为 $\lambda_c = 5$，以平衡各任务梯度量级。



## 实验与关键发现

### 核心瓶颈与因果验证

实验分析围绕一个根本性冲突展开：**动态场景中位姿估计与几何重建对运动信息的需求截然相反**。位姿估计依赖静态对极几何约束，动态运动会引入对极残差 $\delta(\mathbf{x}_r) \approx \frac{1}{Z_r} \mathbf{n}(\mathbf{x}_r)^\top \Delta \mathbf{X}_\perp(\mathbf{x}_r)$（Eqn. 4），破坏本质矩阵约束；而几何重建则需要利用运动线索来推断动态物体的三维结构。原始VGGT倾向于忽略动态内容——其注意力图可视化（Figure 2）显示动态区域激活显著弱于静态区域——导致动态区域绝对深度误差比静态区域高**94%**。

直接抑制动态patch间的交叉注意力（DD-MSK策略，Eqn. 8）可以改善位姿估计，但会严重损害几何重建（Table 7），这证实了简单的“一刀切”策略不可行。PAGE-4D的核心因果机制在于**任务特定的动态信息解耦**：动态感知聚合器预测软掩码 $\widetilde{\mathbf{M}} = \alpha \cdot \sigma(\mathbf{m}/\tau)$（Eqn. 5），对相机/注册令牌施加掩码抑制动态区域，对几何令牌则不施加掩码，从而在单一前馈网络中同时服务两个相互冲突的目标。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_Nfmzp5PBzr/figures/015_Table_7.jpg]]
*Table 7: Study of Different Masking Strategies Applied to VGGT. This experiment is conducted on the Odyssey dataset. We evaluate unscaled pose estimation using Relative Translation Error (RPE trans) and Relative Rotation Error (RPE rot). For static regions, Static-D denotes the Absolute Depth Error, and Static-T represents the Average Endpoint Error (EPE) for 2D point tracking*

### 主要定量结果

#### 视频深度估计（Table 1）

在Sintel、Bonn和DyCheck三个动态基准上，PAGE-4D在所有对齐协议下均显著超越VGGT基线及其他前馈方法：

- **Sintel（scale对齐）**：Abs Rel从0.484降至**0.357**（降低26.2%），δ<1.25从0.553提升至**0.699**（提升26.4%）。在scale&shift对齐下，δ<1.25从0.605提升至**0.763**（+26.1%），Abs Rel从0.378降至**0.212**（-42%）。
- **Bonn**：monocular深度Abs Rel从0.071降至**0.053**，scale对齐δ<1.25达**0.904**。
- **DyCheck**：scale对齐Abs Rel为**0.170**，δ<1.25为**0.785**，均显著优于VGGT。

值得注意的是，PAGE-4D在**单目深度**设定下同样表现优异（Sintel Abs Rel 0.242 vs VGGT 0.292），证明动态感知聚合器带来的增益不依赖于scale后处理。

#### 相机位姿估计（Table 2）

- **Sintel**：ATE从0.214降至**0.143**（降低33.2%），RPE_rot降低17%。
- **TUM**：ATE从0.028降至**0.016**，RPE_trans降低21%，RPE_rot降低13%，在所有前馈方法中达到最优。

TUM数据集主要包含手持相机运动，动态物体相对较少，但PAGE-4D仍能带来显著增益，表明动态感知掩码的抑制机制在准静态场景中同样有效——它学会了识别并抑制潜在的动态干扰。

#### 点图重建（Table 3）

在DyCheck基准上，PAGE-4D相较VGGT实现了质的飞跃：
- Accuracy Mean从1.051降至**0.403**（降低61.7%），Median从1.016降至**0.284**（降低72.0%）。
- Completeness Mean从1.637降至**1.222**，Overall Mean从2.688降至**1.625**。

这一结果直接验证了动态感知聚合器对几何重建的增益：通过保留动态区域的注意力通路，模型能够更完整地重建运动物体的三维结构，而非像VGGT那样产生碎片化、不一致的几何（Figure 4定性对比）。

#### 新视角合成（Table 4）

在Nerfie基准上，PAGE-4D在所有场景上均取得优于VGGT及其他前馈方法的渲染质量（PSNR、SSIM、LPIPS），证明改进的几何估计可直接转化为下游任务增益。

### 消融实验

#### 微调策略与动态掩码（Table 5）

消融实验严格验证了PAGE-4D两个核心设计选择的有效性：

1. **仅微调中间层 vs 全模型微调**：限制微调范围至中间10层（约30%参数）即可达到与全模型微调相当的性能，证实VGGT的中间全局注意力层承载了最关键的跨帧信息融合功能。
2. **加入动态掩码注意力**：在中间层微调基础上引入动态感知掩码后，所有指标进一步提升。Sintel scale对齐Abs Rel从0.484（VGGT）→ 仅中间层微调的中间值 → **0.357**（完整PAGE-4D），证明掩码机制独立贡献了额外增益。

#### 掩码策略分析（Table 7）

在Odyssey数据集上系统比较了不同掩码策略：

- **DD-MSK**（抑制动态token间自注意力）：改善RPE_trans/rot，但Static-D和Static-T指标严重恶化，证实静态区域的重建质量被连带损害。
- **Input-MSK**（输入级掩码）：效果不如注意力级掩码，表明在特征层面而非输入层面解耦动态信息更为有效。
- **移除特定全局注意力层**：移除第17层导致几何质量急剧下降（Static-D 1.663, Static-T 39.841），证明深层中间层对动态建模不可或缺。第4层和第23层的移除影响相对较小，表明动态信息处理集中在网络的特定深度区间。

#### 无监督动态掩码质量（Figure 6）

动态掩码预测模块在**无显式监督**的情况下成功学习到突出运动物体的能力。可视化显示，掩码能清晰标记行人、车辆等动态目标，同时保持静态背景未标记。这一特性使得PAGE-4D无需依赖昂贵的光流或场景流标注即可实现任务特定的动态信息解耦。

### 失败模式与局限性

1. **运动边界模糊**：当动态物体与静态背景纹理相似或运动幅度极小时，无监督掩码可能出现错误抑制或漏检，导致位姿估计引入动态噪声或几何重建丢失运动线索。
2. **点跟踪缺失**：PAGE-4D移除了点跟踪头，无法提供显式2D-3D对应关系，限制了需要稠密跟踪的下游应用（如动态SLAM的特征匹配）。
3. **分布外泛化未充分验证**：微调仅更新30%参数，虽然效率高，但模型对极端光照、全新环境类型等分布偏移的适应能力尚不明确。
4. **长尾动态场景覆盖不足**：训练数据主要来自预定义序列，可能无法覆盖实际应用中动态场景的长尾分布（如快速非刚性变形、多物体复杂交互）。

### 公平性说明

所有对比方法均在相同对齐协议下评估（scale / scale&shift / monocular），FPS测量使用同一A800 GPU硬件。PAGE-4D移除了点跟踪头以避免不适合动态场景的训练目标，因此该任务不纳入公平比较范围。动态数据集的采样比例经过平衡处理（Table 8），防止数据不平衡导致偏向静态场景。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_Nfmzp5PBzr/figures/008_Table_1.jpg]]
*Table 1: Video Depth Estimation on Sintel (Butler et al., 2012), Bonn (Palazzolo et al., 2019) and DyCheck (Yang et al., 2025). FPS is evaluated on KITTI using one A800 GPU. Missing entries (–) denote results not reported in the original papers cited*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_Nfmzp5PBzr/figures/009_Table_2.jpg]]
*Table 2: Camera Pose Estimation on Sintel and Tum*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_Nfmzp5PBzr/figures/013_Table_5.jpg]]
*Table 5: Video Depth Estimation on Sintel (Butler et al., 2012), Bonn (Palazzolo et al., 2019) and DyCheck (Yang et al., 2025)*



## 定位与知识库关联

### 1. 方法谱系与基线关系

PAGE-4D 直接构建在 **VGGT**（Wang et al., CVPR 2025a）之上，后者是一种前馈式 3D 感知模型，能够从多帧 RGB 输入中同时预测相机位姿、深度图和点云。VGGT 本身继承了一条从 **DUSt3R**（Wang et al., CVPR 2024）到 **MASt3R**（Leroy et al., CVPR 2024）再到 **MonST3R**（Zhang et al., ICLR 2025b）的前馈几何估计技术路线，其核心设计——基于 ViT 的全局交叉注意力融合——在静态场景中表现出色，但在动态场景中暴露出根本性缺陷：VGGT 倾向于忽略动态内容，导致动态区域的绝对深度误差比静态区域高出 94%。

这一瓶颈的因果根源在于位姿估计与几何重建对动态信息的需求存在根本性冲突。位姿估计依赖静态对极几何约束，动态像素对应会引入对极残差 $\delta(\mathbf{x}_r) \approx \frac{1}{Z_r} \mathbf{n}(\mathbf{x}_r)^\top \Delta\mathbf{X}_\perp(\mathbf{x}_r)$，破坏相机运动推断；而几何重建则需要利用动态运动信息来恢复移动物体的形状。PAGE-4D 的核心贡献在于识别并解耦了这一冲突，而非简单地将动态信息视为统一有害或有用。

在动态场景几何估计方面，**MonST3R**（Zhang et al., ICLR 2025b）和 **CUT3R**（Wang et al., CVPR 2025b）代表了并行的工作方向。MonST3R 通过优化策略处理动态内容，CUT3R 则面向 4D 重建。PAGE-4D 与这些方法的关键区别在于：它通过一个可学习的动态感知聚合器（Dynamics-Aware Aggregator），以任务特定的方式在注意力机制中注入动态掩码——对相机位姿令牌抑制动态区域，对几何令牌则保留动态信息——从而在单一前馈模型中同时提升位姿和几何质量。这一设计使得 PAGE-4D 在 Sintel 上将相机位姿 ATE 从 VGGT 的 0.214 降至 0.143，同时将视频深度 Abs Rel 从 0.484 降至 0.357。

在高效 3D 重建方面，**Fast3R**（Yang et al., CVPR 2025）和 **Spann3R**（Wang & Agapito, 2024）探索了不同的效率优化路径。PAGE-4D 的效率策略则体现为选择性微调：仅更新中间 10 层全局注意力层（约 30% 参数），冻结其余聚合器和解码器层。消融实验证实，这种选择性微调即可达到与全模型微调相当的性能，而加入动态掩码注意力后所有指标进一步提升。

**FLARE**（Zhang et al., CVPR 2025c）代表了一条同时估计几何、外观和相机参数的前馈路线。PAGE-4D 在任务范围上更为聚焦，但通过动态感知聚合器在动态场景的位姿-几何联合估计上实现了专门化突破。在新视角合成任务（Nerfie 基准）上，PAGE-4D 也展现出一致的渲染质量优势。

### 2. 适用边界与局限

**动态掩码的无监督特性**是 PAGE-4D 的一把双刃剑。动态掩码预测模块通过线性映射加深度卷积头产生掩码 logits，再经可学习温度 $\tau$ 和缩放因子 $\alpha$ 转换为软掩码 $\widetilde{\mathbf{M}} = \alpha \cdot \sigma(\mathbf{m}/\tau)$。可视化结果表明，该模块在无显式监督的情况下能够有效突出运动物体（Figure 6）。然而，在运动边界模糊或动态物体与静态背景纹理相似时，可能出现错误抑制——这是一个需要人工验证的风险点。

**点跟踪头的移除**是另一个重要的适用性限制。PAGE-4D 不包含点跟踪模块，理由是 VGGT 的点跟踪头主要服务于视角注册，不适合动态场景。这一设计选择虽然避免了不适合的动态训练，但也意味着 PAGE-4D 无法提供显式的 2D-3D 对应关系，可能限制需要稠密跟踪的下游应用（如动态 SLAM 或多目标跟踪）。

**微调策略的泛化边界**尚未充分验证。虽然仅微调中间 10 层在现有基准上表现良好，但模型对其他类型分布偏移（如极端光照、全新环境类型）的适应能力缺乏系统评估。训练数据主要来自预定义的合成和真实序列（Table 8），可能无法覆盖实际动态场景的长尾分布。

**长序列与实时场景**的性能一致性是未经验证的开放问题。当前实验主要在中等长度序列上进行，该方法在数百帧或流式场景中的表现需要进一步研究。

### 3. 开放问题

1. **动态掩码的监督增强**：能否引入轻量级的自监督信号（如光流或场景流）来进一步提升掩码质量，同时保持无需人工标注的优势？

2. **点跟踪的重新引入**：是否可以将点跟踪头与动态掩码协同设计，使其适应动态场景？例如，利用动态掩码引导跟踪特征只在静态区域建立对应关系。

3. **与其他 4D 感知任务的结合**：动态感知聚合器作为一种任务特定信息解耦机制，是否可以推广到动态 SLAM、多目标跟踪或动态场景的新视角合成？

4. **更长序列的扩展**：当前的全局注意力机制在处理数百帧时可能面临计算瓶颈，如何设计稀疏或分层的动态感知注意力以适应长序列场景？

5. **动态掩码的可解释性**：虽然可视化显示掩码能捕捉运动物体，但其内部决策机制（如温度参数 $\tau$ 如何影响掩码的锐度）值得更深入的分析。



## 原文 PDF

![[paperPDFs/ICLR_2026/PAGE_4D_Disentangled_Pose_and_Geometry_Estimation_for_VGGT_4D_Perception.pdf]]
