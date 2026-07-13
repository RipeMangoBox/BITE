---
title: "Depth Anything 3: Recovering the Visual Space from Any Views"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Depth_Anything_3_Recovering_the_Visual_Space_from_Any_Views.pdf
project_link: null
code_link: null
openreview_forum_id: yirunib8l8
aliases:
- DA3D
- DA3RVSFAV
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "采用深度-射线表示（depth-ray representation）作为解耦的最小化预测目标集，并基于普通ViT骨干通过输入自适应跨视图自注意力机制统一处理任意数量视图。"
primary_logic: "一个简单的预训练Transformer配上深度-射线预测目标，结合教师-学生训练范式，无需复杂架构或多任务联合优化即可实现任意视图下的高质量空间重建，并超越诸多专用模型。"
claims:
- "单一普通Transformer（如vanilla DINOv2编码器）足以作为骨干网络，无需架构专门化。"
- "单一的深度-射线预测目标避免了复杂的多任务学习。"
- "DA3在相机位姿准确率上平均超过先前SOTA VGGT 35.7%，几何准确率超过23.6%。"
- "深度+射线的预测组合在消融实验中优于仅使用点云的方案，形成充分且最小的目标集。"
---

# Depth Anything 3: Recovering the Visual Space from Any Views

> [!tip] 核心洞察
> 一个简单的预训练Transformer配上深度-射线预测目标，结合教师-学生训练范式，无需复杂架构或多任务联合优化即可实现任意视图下的高质量空间重建，并超越诸多专用模型。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Depth Anything 3: 从任意视角恢复视觉空间 |
| 英文题名 | Depth Anything 3: Recovering the Visual Space from Any Views |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=yirunib8l8) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Depth Anything 3 (DA3) |
| Dataset | HiRoom (pose), ETH3D (pose), ScanNet++ (pose), HiRoom (reconstruction, w/o pose) |

> [!tip] 效果简介
> - HiRoom (pose) 上，Auc3 为 81.7，对比 49.1 (VGGT)，变化 +32.6。
> - ETH3D (pose) 上，Auc3 为 39.3，对比 26.3 (VGGT)，变化 +13.0。
> - ScanNet++ (pose) 上，Auc3 为 83.2，对比 62.6 (VGGT)，变化 +20.6。

## 概要

现有3D视觉任务高度依赖专用化模型架构与复杂的多任务学习范式，导致通用性与扩展性受限。**Depth Anything 3 (DA3)** 提出了一种反直觉的简化路径：采用一个未经架构修改的普通ViT骨干网络（vanilla DINOv2编码器），搭配单一的解耦预测目标——深度图与射线图（depth-ray representation），即可从任意数量、任意视角的图像中恢复完整的视觉空间。

核心创新在于将几何重建问题分解为最小且充分的预测目标集。深度图编码场景结构，射线图隐式编码相机位姿（避免旋转矩阵的正交性约束），二者通过简单的3D点投影公式 $\mathbf{P} = \mathbf{t} + \mathbf{D}(u,v) \cdot \mathbf{d}$ 即可融合为一致的点云。跨视图信息交互通过输入自适应自注意力机制实现——将Transformer的后段层交替进行视图内与跨视图注意力，无需引入额外的跨注意力模块。

训练采用教师-学生范式：仅在合成数据上训练的单目深度教师模型为真实数据生成高质量伪标签，与稀疏真值对齐后监督学生模型，有效克服了真实数据深度标签质量低下的瓶颈。

在涵盖相机位姿估计、多视图几何重建、单目深度估计和新视角合成的综合基准上，DA3在20个评测设置中的18项达到最优。具体而言，**相机位姿准确率平均超越先前SOTA模型VGGT 35.7%，几何准确率超越23.6%**；在HiRoom数据集上，位姿Auc3从49.1跃升至81.7，重建F1从56.7跃升至89.3。在单目深度估计任务上，DA3亦超越Depth Anything 2。消融实验证实，深度+射线的预测组合优于仅使用点云的方案，双DPT头设计和教师标签监督是性能的关键驱动因素。

**方法定位：** DA3属于前馈式多视图几何估计方法，与**VGGT**（Wang et al., 2025a）、**DUSt3R**（Wang et al., 2024c）、**Fast3R**（Yang et al., 2025b）等共享从图像到3D的端到端学习范式，但通过最小化预测目标和通用骨干网络实现了更优的泛化性与简洁性。同时，DA3可替代**COLMAP**（Schönberger and Frahm, 2016）等经典SfM流水线，提供更鲁棒的位姿估计与密集重建。

从单目或多视图图像中恢复三维几何是计算机视觉的核心命题，其应用遍及机器人导航、增强现实和内容创作。传统上，这一领域被高度专用化的模型架构所主导：**DUSt3R** (Wang et al., 2024c) 通过回归点图并进行全局对齐来处理无标定图像对；**VGGT** (Wang et al., 2025a) 采用定制Transformer联合预测相机参数、深度和点云；**Pi3** (Wang et al., 2025d) 则利用置换等变设计从无序图像中恢复仿射不变相机与尺度不变点云。这些方法虽然有效，却普遍存在一个核心瓶颈：**过度依赖复杂的多任务学习与专用架构，难以有效利用大规模预训练模型的强大特征表示能力**，导致模型的通用性和扩展性受限。

具体而言，现有方法面临三重困境。其一，**架构专门化**迫使每个模型独立设计编码器-解码器结构，无法直接继承大规模预训练视觉Transformer（如DINOv2）的丰富语义特征。其二，**多任务耦合**——同时预测点图、深度和相机参数——引入了复杂的损失平衡和优化难题，增加了训练不稳定性。其三，**跨视图交互机制**通常依赖显式的交叉注意力模块或独立处理分支，缺乏灵活且高效的统一方案。

上述困境引发了一个根本性问题：**能否用一个简单的预训练Transformer，搭配最小且充分的预测目标，来实现任意数量视图下的高质量空间重建？** Depth Anything 3 (DA3) 正是对这一问题的肯定回答。其核心动机在于证明：无需复杂的架构专门化或多任务联合优化，仅凭一个普通ViT骨干网络和一组解耦的深度-射线（depth-ray）预测目标，即可统一处理从单目到多视图的几何估计任务，并在位姿准确率上平均超越先前最先进的VGGT达35.7%，在几何准确率上超越23.6%。

## 核心方法与创新机理

DA3 的核心创新并非引入新的网络模块或复杂的多任务学习范式，而是通过**解耦预测目标**与**极简架构**的协同设计，证明一个未经架构修改的普通 Transformer 即可统一任意视图下的几何估计。

### 1. 最小化解耦预测目标：深度-射线表示

现有前馈式多视图几何模型普遍采用**点图（point map）**作为核心预测目标，并通常联合预测深度、相机参数等多个任务。DA3 的消融实验揭示了一个关键发现：直接预测点云（pcd）性能显著低于其他组合（平均 Auc3 仅 31.6, F1 51.5），而**深度 + 射线**的组合在无相机令牌条件下即可达到平均 Auc3 36.0、F1 56.4 的强平衡性能，与加入点云监督的配置（Auc3 36.4, F1 56.5）近乎持平（Table 5）。

这一发现构成了 DA3 表示层的核心创新——将场景几何与相机运动**解耦为两个最小化目标**：
- **深度图**：编码场景结构，直接预测尺度感知的逐像素深度值 $\mathbf{D}(u,v)$；
- **射线图**：隐式编码相机位姿，逐像素预测从相机原点出发的世界坐标系射线方向 $\mathbf{d}$ 和射线起点（即相机中心 $\mathbf{t}$）。

从射线图恢复相机位姿的过程通过求解同形矩阵优化问题完成：最小化变换后规范化射线与预测射线方向的交叉积误差 $\mathbf{H}^* = \arg \min_{\|\mathbf{H}\|=1} \sum_{h,w} \| \mathbf{H} \mathbf{p}_{h,w} \times \mathbf{M}(h,w,3:) \|$，再经 RQ 分解得到内参 $\mathbf{K}$ 和旋转 $\mathbf{R}$。相机中心则通过平均所有像素的射线起点获得 $\mathbf{t}_c = \frac{1}{H \times W} \sum_{h,w} \mathbf{M}(h,w,:3)$。

这种隐式表示相比直接预测 9 自由度相机向量（$\bar{\mathbf{t}}, \mathbf{q}, \mathbf{f}$）的优势在于**避免了旋转矩阵的正交性约束**，使网络学习更加自由。同时，逐像素密集预测射线起点（Table 8）相比单一 MLP 全局预测显著提升了位姿精度，验证了密集表示的必要性。

### 2. 单 Transformer 骨干与输入自适应跨视图注意力

DA3 的架构创新在于**拒绝架构专门化**。与 VGGT 等采用专用编码器-解码器 Transformer 的方案不同，DA3 直接使用预训练的普通 ViT（DINOv2）作为唯一骨干网络，不做任何架构层面的修改。

跨视图信息交互通过**输入自适应自注意力**实现——这是一种纯数据流层面的设计：将 Transformer 层分为两组，前 $L_s$ 层仅在每张图像内部执行自注意力，后 $L_g$ 层交替进行跨视图和视图内注意力。跨视图注意力的实现方式是将来自不同视图的图像 patch 令牌在序列维度上重排，使自注意力操作自然地跨越视图边界。

Table 6 的架构消融验证了这一设计的有效性：
- **Full Alternation**（所有层交替注意力）：性能最优但计算开销最大；
- **VGGT-style**（显式跨注意力模块）：性能降至 baseline 的 79.8%；
- **Partial Alternation**（$L_s : L_g = 2 : 1$）：在性能与效率间取得最佳平衡，成为最终配置。

这一结果的核心启示是：**跨视图推理不需要专门的架构模块**，通过简单的令牌重排便可在标准自注意力框架内实现，且部分层保留视图内注意力对维持预训练特征质量至关重要。

### 3. 双 DPT 头与教师-学生监督范式

DA3 的输出头设计同样遵循“共享促进对齐”的原则。**双 DPT 头**（Figure 3）包含两个预测分支，分别输出深度图和射线图，但**共享重组模块**（reassembly modules）提取的特征，仅在融合阶段分叉。Table 14 的消融表明，这一共享设计相比两个完全独立的 DPT 头，在 HiRoom Auc3 上从 5.59 跃升至 39.2，证明了深度与射线预测之间存在强烈的特征协同效应。

监督策略方面，DA3 采用**教师-学生范式**解决真实数据深度真值质量低下的瓶颈。教师模型仅在合成数据上训练（单目相对深度估计），为真实场景生成尺度-平移不变的伪标签，再通过 RANSAC 最小二乘与稀疏/噪声真值对齐后监督学生模型。Figure 8 和 Table 14 的消融证实，教师标签监督能显著增强深度图的细节和结构完整度，在 HiRoom 等数据集上效果尤为突出。

### 4. 可选的显式几何约束与快速推理

DA3 提供了**可选相机编码器**作为位姿条件模块：当已知相机参数（FOV、旋转四元数、平移）时，通过 MLP 编码为相机令牌 $\mathbf{c}_i = \mathcal{E}_c(\mathbf{f}_i, \mathbf{q}_i, \mathbf{t}_i)$，与图像 patch 令牌拼接参与所有注意力计算。Table 14 显示，在提供真值位姿时，该模块将 HiRoom F1 从 65.8 提升至 73.8。

此外，DA3 配备了一个小型**相机头**（Camera Head），直接从每视图一个相机令牌预测位姿，推理速度比基于射线图的优化方法快约 18.7 倍（Table 7），虽精度略低，但为实时应用提供了精度-速度的灵活权衡。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_yirunib8l8/figures/004_Figure_2.jpg]]
*Figure 2: Pipeline of Depth Anything 3. Depth Anything 3 employs a single transformer (vanilla DINOv2 model) without any architectural modifications. To enable cross-view reasoning, an inputadaptive cross-view self-attention mechanism is introduced. A dual-DPT head is used to predict depth and ray maps from visual tokens. Camera parameters, if available, are encoded as camera tokens and concatenated with patch tokens, participating in all attention operations*

Depth Anything 3 (DA3) 的核心理念是以极简架构实现任意视图下的视觉空间恢复。整个 pipeline 由三个核心组件串联构成：**单一 Transformer 骨干网络**、**可选相机编码器**和**双 DPT 头**，其整体流程如 Figure 2 所示。

### 输入输出流

给定任意数量 $N$ 的输入图像及可选的相机位姿参数，模型输出 $N$ 张逐像素对齐的**深度图**和**射线图**，二者可直接融合为一致的三维点云。具体而言：

- **输入**：$N$ 幅 RGB 图像 $\{\mathbf{I}_i\}_{i=1}^N$，可附带相机参数（视场角 $\mathbf{f}_i$、旋转四元数 $\mathbf{q}_i$、平移 $\mathbf{t}_i$）。
- **输出**：$N$ 张尺度感知的深度图 $\{\hat{\mathbf{D}}_i\}$ 和射线图 $\{\hat{\mathbf{R}}_i\}$，以及可选的置信度图。

### 模块关系

三个模块按以下流程协同工作：

1. **图像分块与令牌化**：每幅输入图像被划分为 patch 并线性投影为视觉令牌（visual tokens），构成 Transformer 的基本输入单元。

2. **可选相机编码器**：若提供相机参数，则通过 MLP $\mathcal{E}_c$ 将每视图的 $(\mathbf{f}_i, \mathbf{q}_i, \mathbf{t}_i)$ 编码为相机令牌 $\mathbf{c}_i$，与视觉令牌拼接后一同送入骨干网络。

3. **单一 Transformer 骨干**：采用未经架构修改的预训练 ViT（如 DINOv2），通过**输入自适应跨视图自注意力**实现多视图信息交互。骨干网络被分为两组：前 $L_s$ 层仅在每幅图像内部进行自注意力，后 $L_g$ 层交替执行跨视图注意力和视图内注意力。这种设计无需显式跨注意力模块，仅通过令牌张量的重排（rearrange）即可实现。

4. **双 DPT 头**：从骨干网络输出的视觉令牌中，通过共享的重组模块（reassembly modules）提取多尺度特征，随后分叉为两个融合分支，分别输出深度图和射线图。两个分支共享特征提取参数以促进深度与射线的输出对齐，同时配备置信度头预测逐像素置信度。

### 深度-射线表示的核心作用

深度图 $\mathbf{D}_i(u,v)$ 与射线图 $\mathbf{M}_i(u,v)$ 构成了最小化解耦的预测目标集。射线图的每个像素编码了归一化射线方向 $\mathbf{d}$ 和相机原点 $\mathbf{t}$，通过关系 $\mathbf{P} = \mathbf{t} + \mathbf{D}(u,v) \cdot \mathbf{d}$ 可直接恢复世界坐标系下的三维点。这一表示将场景几何（深度）与相机运动（射线）解耦，避免了直接预测点云或联合优化多任务的复杂性，消融实验（Table 5）证实其在无相机令牌条件下优于点云等多种替代组合。

### 训练监督策略

DA3 采用教师-学生范式：先在合成数据上训练单目深度估计教师模型，为真实数据生成高质量伪标签；学生模型则在合成真值与教师伪标签的联合监督下训练，整体损失函数为深度损失、射线图损失、点云损失、相机损失和梯度损失的加权和（详见 2.3 节）。

> **注意**：Figure 2 展示了上述整体流程，Figure 3 进一步揭示了双 DPT 头的内部结构，建议配合阅读以获得完整的架构理解。

### 深度-射线表示：最小化解耦预测目标

DA3的核心创新在于将多视图几何预测任务解耦为两个最小化目标：**深度图（depth map）** 和 **射线图（ray map）**，从而避免复杂的多任务联合学习。

给定图像 $i$ 中像素 $\mathbf{p} = (u, v)$，其对应的3D点 $\mathbf{P}$ 可通过深度、相机内参和外参进行投影：

$$\mathbf{P} = \mathbf{R}_i \big( \mathbf{D}_i(u, v) \mathbf{K}_i^{-1} \mathbf{p} \big) + \mathbf{t}_i$$

其中 $\mathbf{D}_i$ 为深度图，$\mathbf{K}_i$ 为内参矩阵，$\mathbf{R}_i$ 和 $\mathbf{t}_i$ 分别为旋转矩阵和平移向量。

射线方向 $\mathbf{d}$ 则通过将像素反投影到相机坐标系后旋转至世界坐标系获得：

$$\mathbf{d} = \mathbf{R} \mathbf{K}^{-1} \mathbf{p}$$

由此，3D点可直接由相机原点加上缩放后的射线方向表示，实现了场景几何（深度）与相机位姿（射线）的解耦：

$$\mathbf{P} = \mathbf{t} + \mathbf{D}(u, v) \cdot \mathbf{d}$$

消融实验（Table 5）证实，深度+射线的组合在无相机令牌条件下达到平均Auc3 36.0、F1 56.4，性能优于仅使用点云（pcd）的方案（Auc3 31.6, F1 51.5），且与加入点云监督的三目标组合（depth+ray+pcd: Auc3 36.4, F1 56.5）性能接近，证明了该组合作为最小且充分预测目标集的有效性。

### 单Transformer骨干网络与输入自适应自注意力

DA3采用普通预训练ViT（vanilla DINOv2）作为骨干网络，无需任何架构修改。为实现跨视图信息交互，提出**输入自适应跨视图自注意力机制**，通过令牌重排（token rearrangement）实现。

将Transformer层分为两组：前 $L_s$ 层仅在各视图内部执行自注意力，后 $L_g$ 层交替进行跨视图和视图内注意力。这种部分交替策略在Table 6的消融中被证明在性能和效率间取得最佳平衡，相比全层交替方案和VGGT风格架构变体性能提升约20%。

当相机位姿已知时，相机参数通过MLP编码为相机令牌：

$$\mathbf{c}_i = \mathcal{E}_c(\mathbf{f}_i, \mathbf{q}_i, \mathbf{t}_i)$$

其中 $\mathbf{f}_i$ 为视场角（FOV），$\mathbf{q}_i$ 为旋转四元数，$\mathbf{t}_i$ 为平移向量。相机令牌与图像patch令牌拼接后参与所有注意力计算，提供显式几何约束。

### 双DPT头设计

DA3采用双DPT头（Dual-DPT Head）从视觉令牌中预测深度图和射线图。两个预测分支共享重组模块（reassembly modules），但保持独立的融合层参数，以促进深度与射线输出之间的对齐。

Table 14的消融显示，双DPT头设计相比两个完全独立的DPT头性能提升显著——在HiRoom数据集上Auc3从5.59提升至39.2（Table 14 a vs d），验证了共享特征提取对任务对齐的关键作用。

### 总体训练目标

DA3的总体损失函数由五项加权组成：

$$\mathcal{L} = \mathcal{L}_D(\hat{\mathbf{D}}, \mathbf{D}) + \mathcal{L}_M(\hat{\mathbf{R}}, \mathbf{M}) + \mathcal{L}_P(\hat{\mathbf{D}} \odot \mathbf{d} + \mathbf{t}, \mathbf{P}) + \beta \mathcal{L}_C(\hat{\mathbf{c}}, \mathbf{v}) + \alpha \mathcal{L}_{\mathrm{grad}}(\hat{\mathbf{D}}, \mathbf{D})$$

其中 $\mathcal{L}_D$ 为深度损失，$\mathcal{L}_M$ 为射线图损失，$\mathcal{L}_P$ 为点云损失（通过预测深度和射线计算3D点与真值比较），$\mathcal{L}_C$ 为相机损失，$\mathcal{L}_{\mathrm{grad}}$ 为梯度损失，权重 $\alpha=1, \beta=1$。

深度损失采用置信度加权的L1损失：

$$\mathcal{L}_D(\hat{\mathbf{D}}, \mathbf{D}; D_c) = \frac{1}{Z_\Omega} \sum_{p \in \Omega} m_p \left( D_{c,p} \left| \hat{\mathbf{D}}_p - \mathbf{D}_p \right| - \lambda_c \log D_{c,p} \right)$$

梯度损失用于保留边缘锐利度：

$$\mathcal{L}_{\mathrm{grad}}(\hat{\mathbf{D}}, \mathbf{D}) = ||\nabla_x \hat{\mathbf{D}} - \nabla_x \mathbf{D}||_1 + ||\nabla_y \hat{\mathbf{D}} - \nabla_y \mathbf{D}||_1$$

### 教师-学生训练范式

为应对真实数据集中深度真值质量差的问题（Figure 7），DA3采用教师-学生范式：教师模型仅在合成数据上训练单目相对深度估计，为真实数据生成高质量伪标签，再通过RANSAC最小二乘与稀疏真值对齐后监督学生模型。Figure 8和Table 14的消融（a vs e）证实，教师标签监督能显著增强深度图的细节和结构完整度。

### 相机位姿的隐式与显式估计

DA3提供两种位姿获取方式：
- **基于射线图的优化求解**：通过平均所有像素的射线起点估计相机中心 $\mathbf{t}_c = \frac{1}{H \times W} \sum_{h,w} \mathbf{M}(h,w,:3)$，再通过最小化同形矩阵变换误差求解内参和旋转：

$$\mathbf{H}^* = \arg \min_{\|\mathbf{H}\|=1} \sum_{h,w} \| \mathbf{H} \mathbf{p}_{h,w} \times \mathbf{M}(h,w,3:) \|$$

对 $\mathbf{H}$ 进行RQ分解得到 $\mathbf{K}$ 和 $\mathbf{R}$。该方法精度高但计算耗时。

- **相机头（Camera Head）**：一个小型Transformer直接预测FOV、旋转四元数和平移，推理速度比射线优化快约18.7倍（Table 7），但精度略低，形成精度-速度权衡。

## 实验与关键发现

### 核心性能：位姿估计

DA3在视觉几何基准的位姿估计任务上全面建立了新的SOTA。**Table 1** 报告了五个数据集上的Auc3和Auc30指标，DA3-Giant在所有前馈方法中取得了至少8%的相对提升。在ScanNet++上，DA3-Giant的Auc3达到83.2，相较第二名前馈模型实现33%的相对增益。与先前SOTA **VGGT**（Wang et al., 2025a）相比，DA3-Giant在HiRoom上Auc3从49.1跃升至81.7（+32.6），在ETH3D上从26.3提升至39.3（+13.0），平均相对提升达35.7%。**Figure 4** 的定性轨迹对比进一步佐证了位姿估计的鲁棒性：DA3恢复的相机轨迹平滑且最接近COLMAP真值，而VGGT和**Pi3**（Wang et al., 2025d）的轨迹噪声明显更大。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_yirunib8l8/figures/006_Table_1.jpg]]
*Table 1: Comparisons with SOTA methods on pose accuracy. We report both Auc3 ↑ and Auc30 ↑ metrics. The top-3 results are highlighted as first , second , and third*

### 核心性能：无位姿几何重建

在无真值位姿的条件下，DA3-Giant同样建立了新的SOTA。**Table 2** 显示，DA3-Giant在F1指标上平均超越VGGT 23.6%，超越Pi3 16.7%。具体而言，HiRoom上F1从VGGT的56.7提升至89.3（+32.6），ETH3D上从57.2提升至74.4（+17.2）。即使提供真值位姿进行融合，DA3-Giant依然保持领先。**Figure 6** 的定性对比表明，DA3生成的点云几何更规则、噪声显著少于其他方法，验证了深度-射线表示在重建质量上的优势。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_yirunib8l8/figures/008_Table_2.jpg]]
*Table 2: Comparisons with SOTA methods on reconstruction accuracy. For all datasets except DTU, we report the F-Score (F1 ↑). For DTU, we report the chamfer distance (CD ↓, unit: mm). w/o p. and w/ p. denote without pose and with pose, indicating whether ground-truth camera poses are provided for reconstruction. The top-3 results are highlighted as first , second , and third*

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_yirunib8l8/figures/016_Figure_6.jpg]]
*Figure 6: Comparisons of point cloud quality. Our model produces point clouds that are more geometrically regular and substantially less noisy than those generated by other methods. Table 5: Ablations of prediction-target combinations. Note that all experiments in this table do not have camera condition token. The best and second best are highlighted*

### 单目深度估计

尽管DA3设计为多视图模型，其单目深度估计能力同样超越了专用模型。**Table 3** 显示，DA3在五个基准上的δ1综合排名为2.20，优于**Depth Anything 2**（Yang et al., 2024b）的2.60和VGGT的3.75。在KITTI上δ1达到95.3（DA2为94.6），在ETH3D上达到98.6。**Figure 5** 的定性对比显示DA3的深度图结构细节更精细、语义正确性更高。值得注意的是，Teacher模型在所有数据集上排名第一（1.00），说明教师-学生训练范式的上界仍有提升空间。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_yirunib8l8/figures/010_Table_3.jpg]]
*Table 3: Monocular depth comparisons. $\delta _ { 1 }$*

### 新视角合成

在FF-NVS任务上，DA3作为几何骨干网络展现出最强的下游任务迁移能力。**Table 4** 显示，DA3在DL3DV上PSNR达到21.33（VGGT为20.96），在Tanks&Temples上达到18.10，在MegaDepth上达到17.89，LPIPS指标同样最优。**Figure 9** 的定性对比表明，DA3在薄结构和基线场景下的渲染质量优势尤为显著，验证了“NVS性能与几何估计能力正相关”的因果关系——更强的几何骨干直接转化为更优的渲染质量。

### 消融分析：预测目标

**Table 5** 是最关键的消融实验之一，验证了深度-射线表示作为最小化充分目标集的核心主张。在无相机令牌的条件下：
- 仅预测点云（pcd）表现最差，平均Auc3仅31.6、F1为51.5，说明点云作为预测目标引入了过高的学习难度。
- 深度+射线的组合达到平均Auc3 36.0、F1 56.4，在性能和简洁性之间取得最佳平衡。
- 进一步加入点云监督（depth+ray+pcd）仅带来边际提升（Auc3 36.4、F1 56.5），证明深度+射线已构成充分的目标集。

这一结果直接支持了论文的核心洞察：解耦场景结构（深度）和相机运动（射线）比直接预测耦合的点图更有效。

### 消融分析：架构设计

**Table 6** 对比了三种单Transformer架构设计：
- VGGT风格的专用架构性能降至基线模型的79.8%，验证了“普通ViT足以作为骨干”的论断。
- 全交替注意力（所有层均交替跨视图/视图内注意力）与部分交替方案性能接近，但计算开销更大。
- 论文采用的部分交替方案（前L_s层仅视图内注意力，后L_g层交替）在性能和效率间取得了最优平衡，L_s:L_g=2:1的配置被选为默认设置。

### 消融分析：双DPT头与教师监督

**Table 14** 的综合消融揭示了几个关键设计选择的影响：
- **双DPT头 vs 独立DPT头**：使用两个独立DPT头分别预测深度和射线时，HiRoom Auc3仅5.59；采用共享重组模块的双DPT头后跃升至39.2，提升约7倍。这表明深度和射线预测之间存在强耦合，共享特征提取能有效促进任务对齐。
- **教师标签监督**：**Figure 8** 定性显示，加入教师模型生成的伪标签监督后，深度图的结构细节和完整度显著增强。Table 14中，有教师监督的模型在HiRoom上Auc3从39.2提升至81.7，在ETH3D上从18.2提升至39.3，证明伪标签有效弥合了合成数据与真实场景之间的域间隙。
- **位姿条件模块**：提供真值位姿作为条件输入时，HiRoom F1从65.8提升至73.8，验证了显式几何约束对重建精度的增益。

### 消融分析：相机头与射线图位姿估计

**Table 7** 揭示了精度与速度的权衡：基于射线图的优化位姿估计平均Auc3达68.0，优于相机头的63.8，但每视图推理耗时8.60ms，约为相机头（0.46ms）的18.7倍。在实际部署中，相机头适用于实时场景，而射线图方法适用于精度优先的离线处理。

### 消融分析：射线原点预测

**Table 8** 对比了逐像素密集预测射线原点与单一MLP全局预测的效果。逐像素预测在所有数据集上均优于全局预测，验证了密集射线表示对捕捉相机位姿细微变化的必要性。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_yirunib8l8/figures/020_Table_8.jpg]]
*Table 8: Ablation study on ray origin prediction. We compare per-pixel ray origin prediction (depth + ray + cam) with single MLP-based global prediction (depth + ray-st + cam)*

### 失败模式与局限性

尽管DA3在静态场景上取得了卓越性能，论文明确指出现有模型存在以下局限：
1. **动态场景未覆盖**：模型未扩展至运动物体和时变几何的推理，在**Figure 4**的动态场景评估中真值轨迹需先对动态物体进行掩码处理。
2. **计算复杂度线性增长**：虽然支持任意数量视图，但处理极大量视图时计算复杂度随视图数线性增长，可能影响实时性。
3. **相机头精度略低**：相机头位姿估计精度低于基于射线图的优化方法，存在精度-速度的固有权衡。
4. **教师模型域间隙**：教师模型仅在合成数据上训练，对真实场景的伪标签质量依赖于合成数据的多样性和真实性。**Figure 7** 展示了真实数据集中常见的低质量深度真值（噪声、缺失），说明教师伪标签虽有效但仍受限于合成数据覆盖范围。
5. **零样本评测偏差**：ScanNet++和DL3DV等数据集已被先前方法训练使用，零样本评测存在一定偏差，尽管作者进行了场景级隔离。
6. **NVS仅作为几何骨干**：模型在新视角合成任务中仅作为几何骨干网络，未探索与NeRF等其他表示的深度融合。

### 开放问题

论文在结论部分提出了若干值得探索的方向：如何将推理能力扩展到动态场景；如何整合语言理解与交互式线索实现更智能的空间推理；探索更大规模预训练以弥合几何理解与可操作世界模型之间的差距；以及如何进一步减小模型尺寸以适应边缘设备。

## 定位与知识库关联

### 与前驱工作的关系

DA3 直接建立在 **Depth Anything 2**（DA2, Yang et al., 2024b）的单目深度估计能力之上，将其从单视图扩展至任意多视图。DA2 作为教师模型的核心角色，通过教师-学生范式为真实数据生成高质量伪标签，弥合了合成数据训练与真实场景推理之间的域间隙。

在密集多视图几何估计领域，DA3 与以下工作构成直接对比：

- **DUSt3R**（Wang et al., 2024c）：开创性地将无标定图像对的几何估计统一为点图回归问题，通过全局对齐恢复相机位姿。DA3 继承其“统一预测目标”的思想，但将点图替换为解耦的深度-射线表示，避免了点图回归中隐式耦合场景结构与相机运动的固有问题。
- **VGGT**（Wang et al., 2025a）：当前最先进的多视图几何估计模型，采用专用 Transformer 架构联合预测相机参数、深度和点云。DA3 在架构设计上与其形成鲜明对比——VGGT 依赖高度定制化的编码器-解码器结构，而 DA3 证明单普通预训练 ViT 骨干（vanilla DINOv2）配合输入自适应跨视图自注意力即可超越其性能（相机位姿平均提升 35.7%，几何精度提升 23.6%）。
- **Pi3**（Wang et al., 2025d）：利用置换等变设计从无序图像中恢复仿射不变相机和尺度不变点云。DA3 通过深度-射线表示自然处理任意顺序输入，无需专门的等变架构设计。
- **Fast3R**（Yang et al., 2025b）：将点图回归扩展至数百甚至数千幅图像的单次前向传播。DA3 同样支持任意数量视图，但通过深度-射线解耦和部分交替注意力策略，在效率与精度间取得更优平衡。
- **MapAnything**（Keetha et al., 2025）：支持已知相机位姿作为输入的前馈式密集几何预测框架。DA3 通过可选相机编码器实现类似的条件化能力，在提供真值位姿时进一步提升了重建精度。
- **COLMAP**（Schönberger and Frahm, 2016）与 **GLOMAP**（Pan et al., 2024b）：经典 SfM 流水线。DA3 作为前馈方法，在推理速度上具有数量级优势，同时在多个基准上达到或超越其位姿估计精度。

### 方法适用边界

**适用场景**：
- 静态场景的任意视图几何重建，支持从单目到多视图的无缝切换。
- 相机位姿估计与密集深度估计的联合或独立推理。
- 前馈式新视角合成（FF-NVS）的几何骨干网络，为 3D Gaussian Splatting 提供初始几何。
- 已知或未知相机参数的输入条件，通过可选相机编码器灵活适配。

**不适用或需谨慎使用的场景**：
- **动态场景**：当前模型未建模运动物体或时变几何，动态区域会产生伪影。
- **极大量视图**：尽管支持任意数量视图，但跨视图自注意力的计算复杂度随视图数线性增长，在数百幅以上图像时可能影响实时性。
- **极端域外场景**：训练数据限于公开学术数据集，对水下、医疗、遥感等特殊成像条件的泛化能力未经验证。
- **实时性要求极高的应用**：相机头虽比射线图解析快约 18.7 倍，但整体推理仍需 GPU 加速，未针对边缘设备优化。

### 局限性与开放问题

**已明确的局限**：
- 教师模型仅在合成数据上训练，伪标签质量受限于合成数据的多样性和真实性，存在域间隙风险。
- 相机头位姿估计精度略低于基于射线图的优化方法（RQ 分解），形成精度-速度权衡。
- ScanNet++ 和 DL3DV 等数据集已被先前方法训练使用，零样本评测存在偏差（作者已在场景级别隔离训练/测试集以缓解此问题）。
- 新视角合成任务中仅作为几何骨干网络，未探索与 NeRF 等其他神经表示方法的深度融合。

**开放问题**：
- **动态场景扩展**：如何将深度-射线表示推广到时变几何，处理运动物体和动态遮挡关系？
- **多模态融合**：深度-射线表示是否可泛化到激光雷达、事件相机等其他传感器模态？如何整合语言理解与交互式线索，实现更智能的空间推理？
- **大规模预训练**：进一步扩展预训练数据规模和多样性，能否弥合几何理解与可操作世界模型之间的差距？
- **轻量化部署**：如何通过模型压缩、知识蒸馏等技术减小模型尺寸并保持精度，以适应边缘设备和实时应用？
- **监督效率极限**：教师-学生范式在更少监督数据下的极限性能如何？能否通过自监督或弱监督进一步降低对伪标签的依赖？

## 原文 PDF

![[paperPDFs/ICLR_2026/Depth_Anything_3_Recovering_the_Visual_Space_from_Any_Views.pdf]]
