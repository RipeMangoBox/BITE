---
title: "Motion Blender Gaussian Splatting for Dynamic Scene Reconstruction"
type: paper
paper_level: A
venue: CoRL
year: 2025
pdf_ref: paperPDFs/CORL_2025/Motion_Blender_Gaussian_Splatting_for_Dynamic_Scene_Reconstruction.pdf
aliases:
- MBGSM
- MBGSDSR
tags:
- CORL_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "采用显式且稀疏的运动图（运动学树和变形图）作为运动表示，通过双四元数蒙皮将图链接的运动传播到每个高斯，并引入可学习的权重绘制函数来自动确定每个链接对高斯的影响权重，同时保持高保真重建。"
primary_logic: "用显式稀疏的运动图替代隐式稠密运动表示，可在实现高保真动态场景重建（对比最先进的隐式方法）的同时，提供对运动的直接、直观操控能力，从而开启新颖姿态动画、机器人演示合成和基于视觉规划的机器人动作预测等新应用。"
claims:
- "提出使用运动学树和变形图作为高斯泼溅重建的显式、稀疏运动表示。"
- "在极具挑战性的iPhone数据集上，MBGS以LPIPS 0.37超越Shape-of-Motion的0.39，取得当时最佳性能。"
- "MBGS能够编辑运动图产生训练视频中未见的新颖姿态，实现动态场景的想象与渲染。"
- "通过替换高斯和利用机器人运动链，从人类视频合成机器人演示，展示了在真实机器人操作上的潜力。"
---

# Motion Blender Gaussian Splatting for Dynamic Scene Reconstruction

> [!tip] 核心洞察
> 用显式稀疏的运动图替代隐式稠密运动表示，可在实现高保真动态场景重建（对比最先进的隐式方法）的同时，提供对运动的直接、直观操控能力，从而开启新颖姿态动画、机器人演示合成和基于视觉规划的机器人动作预测等新应用。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 运动混合高斯泼溅用于动态场景重建 |
| 英文题名 | Motion Blender Gaussian Splatting for Dynamic Scene Reconstruction |
| 会议/期刊 | CoRL 2025 |
| Links | [paper](https://arxiv.org/abs/2503.09040); [Project](https://mlzxy.github.io/motion-blender-gs/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Motion Blender Gaussian Splatting (MBGS) |
| Dataset | iPhone dataset [15], HyperNeRF vrig dataset [16] |

> [!tip] 效果简介
> - iPhone dataset [15] 上，LPIPS↓ 为 0.37，对比 0.39 (Shape-of-Motion)，变化 -0.02。
> - HyperNeRF vrig dataset [16] 上，LPIPS↓ 为 0.35，对比 0.36 (4DGaussians)，变化 -0.01。
> - iPhone dataset [15] 上，PSNR↑ 为 16.79，对比 16.67 (Shape-of-Motion)，变化 +0.12。

## 概述

### 问题瓶颈

现有动态高斯泼溅方法在重建动态场景时，主要依赖**隐式运动表示**——要么通过神经网络编码运动，要么为每个高斯分配独立的运动参数。这种设计使运动被“黑箱化”，研究者无法直接访问、操控或编辑重建的运动，严重限制了方法在需要运动规划与合成的机器人领域的应用。具体而言，这些方法只能重放记录的运动，而无法产生训练视频中未出现的新颖姿态。

### 核心方法

**Motion Blender Gaussian Splatting (MBGS)** 提出用**显式且稀疏的运动图**替代隐式稠密运动表示。其核心设计包含三个关键组件：

- **运动图**：采用运动学树（用于人体等铰接结构）或变形图（用于软组织非刚体变形）作为运动表示，参数通常少于100个，远小于高斯数量（数十万）。
- **权重绘制函数**：可学习函数，基于高斯与图链接的距离自动确定每个链接对高斯的控制权重。
- **双四元数蒙皮**：将链接的相对刚体变换根据权重平滑混合，传播到每个高斯，生成新的位姿。

整个框架通过可微渲染端到端联合优化高斯、运动图和权重绘制函数。

### 核心结论

MBGS在保持高保真动态场景重建的同时，首次赋予动态高斯泼溅方法**直接的运动操控能力**。在iPhone数据集上，MBGS以LPIPS 0.37超越当时最优方法Shape-of-Motion的0.39；在HyperNeRF数据集上，LPIPS 0.35与4DGaussians的0.36可比。更重要的是，运动图的显式结构开启了三个此前动态高斯泼溅方法无法实现的应用：**新颖姿态动画**（编辑运动图生成未见姿态）、**机器人演示合成**（从人类视频合成机器人操作视频）和**基于视觉规划的机器人动作预测**（通过模拟运动图轨迹最大化与目标图像的PSNR来规划动作）。在真实机器人实验中，布料折叠和微波炉门操作成功率达10/10，软绳弯曲成功率为7/10。

### 方法谱系与知识库定位

MBGS位于**动态场景重建**与**可操控运动表示**的交叉点。在重建质量上，它与基于隐式变形场的**4DGaussians**和基于逐高斯运动参数的**Shape-of-Motion**等SOTA方法竞争；在运动表示上，它借鉴了计算机图形学中经典的**骨骼蒙皮动画**思想（运动学树、双四元数蒙皮），但通过可微渲染将其融入端到端学习框架。与现有动态高斯泼溅方法相比，MBGS的核心差异在于：将运动参数从“稠密且隐式”转变为“稀疏且显式”，从而在保持重建质量的同时解锁了运动操控能力。这一思路为动态场景重建通向机器人应用提供了新的技术路径。

## 背景与动机

动态场景重建是计算机视觉与机器人领域的核心问题，其目标是从二维视频观测中恢复三维场景的几何、外观及其随时间演化的运动规律。近年来，以三维高斯泼溅（3D Gaussian Splatting）为代表的显式辐射场方法在静态场景重建中展现出卓越的保真度与渲染效率，研究者随之将其拓展至动态场景，形成了动态高斯泼溅（Dynamic Gaussian Splatting）这一活跃方向。

**现有方法的隐式运动瓶颈。** 当前主流的动态高斯泼溅方法——包括基于变形场网络的方法（如 **Deformable‑GS**）和逐高斯运动参数的方法（如 **4DGaussians** 和 **Shape‑of‑Motion**）——在运动表示上存在一个共同的深层局限：它们采用隐式运动表示，即通过神经网络编码运动场，或为每个高斯分配独立的时变运动参数。这种设计虽然能够实现高保真的动态重建，但运动的语义和结构被隐式地编码在神经网络的权重中或数十万个独立参数中，导致两大后果：

1. **运动操控性缺失。** 隐式表示使得用户无法直接、直观地编辑或操控重建的运动。方法仅能“重放”记录的运动轨迹，而无法生成训练视频中未出现的新颖姿态，也无法将运动迁移到不同场景或物体上。这严重限制了动态重建在需要运动规划与合成的机器人领域的应用。
2. **参数冗余与可解释性不足。** 逐高斯运动参数的数量通常与高斯数量成正比（可达数十万量级），而变形场网络则是一个黑箱映射。两者都缺乏对物体运动结构的显式建模，难以解释“为什么这样运动”，也难以将运动分解为有物理意义的组成部分（如关节旋转、刚体位移等）。

**机器人领域的迫切需求。** 在机器人操作中，运动表示不仅需要支持高保真渲染，更需要具备可操控、可编辑、可迁移的特性。例如，从人类演示视频中学习操作技能并合成机器人演示，或通过视觉规划预测机器人动作以实现特定目标状态，都要求运动表示能够被直接干预和推理。现有隐式方法因其“不可触碰”的运动编码方式，无法满足这些需求。

**本文的核心动机。** 针对上述缺口，本文提出一个根本性的设计转向：**用显式、稀疏的运动图替代隐式、稠密的运动表示**。具体而言，MBGS 引入运动学树（kinematic tree）和变形图（deformable graph）作为高斯泼溅的运动表示——前者适用于铰接结构（如人体），后者适用于非刚体形变（如软体物体）。运动图的参数通常少于 100 个，通过双四元数蒙皮（Dual Quaternion Skinning）将稀疏图链接的运动平滑传播到每个高斯，从而在保持高保真重建的同时，赋予运动表示以直接的可操控性。这一设计使得MBGS成为首个在动态高斯泼溅框架中实现显式运动操控的方法，开启了新颖姿态动画、机器人演示合成和基于视觉规划的机器人动作预测等新应用。

## 核心创新

MBGS 的核心创新在于用**显式、稀疏的运动图**替代现有动态高斯泼溅方法中普遍采用的**隐式、稠密运动表示**，在保持高保真动态重建的同时，首次赋予重建结果以**直接的运动操控与编辑能力**。

### 问题瓶颈

现有动态高斯泼溅方法（如 **Deformable-GS**、**4DGaussians**、**Shape-of-Motion**）的运动表示存在两个根本性局限：

- **运动隐式编码**：运动信息被编码进神经网络变形场或逐高斯独立运动参数中，缺乏可解释的显式结构，用户无法直观理解或干预物体的运动方式。
- **参数稠密**：每个高斯需关联独立的运动参数，数量常达数十万，导致运动表示与场景几何深度耦合，无法将“如何运动”从“长什么样”中解耦出来。

这两点共同导致了一个关键瓶颈：**现有方法只能重放记录的运动，无法编辑、合成或规划新的运动**，严重限制了动态重建在机器人等需要运动操控的领域的应用。

### 核心因果杠杆：显式稀疏运动图

MBGS 的解决方案是将运动表示从“隐式稠密”切换到“显式稀疏”，具体通过以下四个相互协同的 changed slots 实现：

**1. 运动表示形式：隐式 → 显式运动图**

MBGS 采用两类显式运动图来参数化场景运动（Figure 3）：
- **运动学树（Kinematic Tree）**：层次化无环图，由关节旋转 $`\mathbf{r}_t \in \mathrm{SO}(3)`$、根节点位姿和时不变链接长度 $`\ell_i`$ 参数化，适用于人体等铰接结构。
- **变形图（Deformable Graph）**：无拓扑约束的自由形变图，由关节位置 $`\{\mathbf{n}_{i,t}\}`$ 参数化，适用于软体非刚体变形。

运动图的参数通常少于 100 个，相比数十万高斯运动参数实现了数量级的稀疏化。这种显式结构使得运动本身成为可观察、可编辑的一等公民。

**2. 运动传播机制：逐高斯独立参数 → 双四元数蒙皮混合**

运动图链接的运动通过双四元数蒙皮（Dual Quaternion Skinning, DQS）传播到每个高斯：

$$`\mathbf{p}_t = B\big( \mathcal{R}(P_{\mathcal{L},0}, P_{\mathcal{L},t}), \mathcal{W}(\mathbf{x}_0, X_{\mathcal{L},0}) \big) \cdot \mathbf{p}_0`$$

其中 $`\mathcal{R}`$ 计算链接在时域上的相对刚体变换，$`\mathcal{W}`$ 为权重绘制函数，$`B`$ 通过 DQS 在 SE(3) 空间内平滑混合各链接的运动。这一机制将稀疏图运动“广播”到所有高斯，实现了运动与几何的解耦。

**3. 运动操控性：仅可重放 → 可编辑与合成**

显式运动图使得用户可以直接操控图节点来编辑运动，产生训练视频中未见的新颖姿态（Figure 5）。这一能力进一步支撑了三项关键应用：
- **新颖姿态动画**：修改运动图参数渲染新姿态。
- **机器人演示合成**：将人体高斯的运动图替换为机器人运动链，通过逆运动学驱动生成机器人操作视频（Figure 9）。
- **视觉规划**：模拟运动图轨迹，通过最大化渲染图像与目标图像的 PSNR 来预测机器人动作（Figure 10）。

**4. 运动参数密度：稠密（数十万） → 稀疏（<100）**

运动图参数数量从数十万级降至百级以下，不仅降低了优化难度，更使得运动表示本身成为可解释的轻量结构，为后续编辑和规划提供了基础。

### 方法谱系与知识库定位

MBGS 在动态高斯泼溅方法谱系中占据独特位置：

| 维度 | 隐式方法（Deformable-GS, 4DGaussians） | 逐高斯方法（Shape-of-Motion） | **MBGS（本文）** |
|------|------|------|------|
| 运动表示 | 神经网络变形场 | 逐高斯运动参数 | **显式运动图** |
| 参数密度 | 网络参数量 | 数十万 | **<100** |
| 运动操控 | 不可编辑 | 不可编辑 | **可编辑、可合成** |
| 渲染质量 | 高 | 高 | **相当或更优** |

MBGS 在保持与 SOTA 方法相当的渲染质量（iPhone 数据集 LPIPS 0.37 vs Shape-of-Motion 0.39；HyperNeRF LPIPS 0.35 vs 4DGaussians 0.36）的同时，首次实现了运动表示的可操控性，将动态场景重建从“被动重放”推向“主动编辑与规划”，为动态重建与机器人操作的交叉领域开辟了新方向。

## 整体框架

![[assets/figures/papers/paper_list_l9_Motion_Blender_Gaussian_Splatting_for_Dynamic_Scene_Reconstruction/figures/001_Figure_1.jpg]]
*Figure 1: Capabilities of Our Framework. Our method reconstructs and renders dynamic scenes into 3D Gaussians and motion graphs from input videos. The learned motion graphs for a hand and cat are shown with their corresponding rendered scenes (left). Our approach enables three key applications (right): ➊ Novel pose animation through motion graph editing, ➋ Robot demonstration synthesis by using robot kinematic chains as motion graphs, and ➌ Predicting robot actions by simulating graph movements to minimize the difference between rendered and goal images*

![[assets/figures/papers/paper_list_l9_Motion_Blender_Gaussian_Splatting_for_Dynamic_Scene_Reconstruction/figures/006_Figure_6.jpg]]
*Figure 6: We initialize motion graphs at the canonical frame (t = 0) using instance segmentation masks from Grounding SAM2 [23, 24] and 2D human skeletons estimated by SAPIENS [25]. Furthermore, our framework enables per-instance reconstruction, where Gaussians are explicitly grouped to maintain accurate instance geometry — a capability previously unexplored in existing literature of dynamic Gaussian splatting. More optimization details are provided in Appendix A.2*

![[assets/figures/papers/paper_list_l9_Motion_Blender_Gaussian_Splatting_for_Dynamic_Scene_Reconstruction/figures/002_Figure_2.jpg]]
*Figure 2: Motion Blender Gaussian Splatting. Our framework explicitly represents motion using sparse dynamic graphs. Static 3D Gaussians are associated with the graphs through learnable weight painting. Then, link-wise motions are propagated to the Gaussians through motion blending with dual quaternion skinning. We employ two motion graph types: kinematic trees, ideal for capturing articulated structures like human bodies, and deformable graphs, designed for modeling non-rigid deformations in soft objects. The parameters of the motion graph, weight painting functions, and 3D Gaussians are jointly optimized, end-to-end, via differentiable rendering*

Motion Blender Gaussian Splatting (MBGS) 将动态场景重建重新表述为一个**显式运动混合**问题。其核心设计理念在于：用稀疏的运动图替代隐式运动编码，通过可学习的权重分配将图的运动传播到静态高斯上，从而在保持高保真渲染的同时获得对运动的直接操控能力。

### 输入与输出

框架的输入为单目视频序列，输出包含两部分：
- **静态3D高斯**：表示场景的几何与外观，在规范帧（$t=0$）重建后其形状和颜色参数保持固定
- **运动图**：一个显式、稀疏的动态结构，参数化场景中物体随时间的运动

### 核心Pipeline

整个流程由五个紧密耦合的模块组成，通过可微渲染实现端到端联合优化：

**1. 静态3D高斯初始化**

首先在规范帧（$t=0$）上重建场景的3D高斯表示。这些高斯后续不再改变其固有属性（位置、协方差、颜色、不透明度），仅通过运动图驱动其位姿变换。这一设计将“几何/外观”与“运动”完全解耦。

**2. 运动图构建**

运动图是框架的核心创新，采用两种图结构以适应不同运动类型：
- **运动学树**：层次化无环图，参数化为关节旋转 $\mathbf{r}_t \in \mathrm{SO}(3)$、根节点位姿和时不变链接长度 $\ell_i$，适用于人体等铰接结构
- **变形图**：无拓扑约束的自由形变图，关节可自由移动，适用于软体非刚体变形

运动图的参数数量极少（通常少于100），远低于逐高斯运动参数（常达数十万），实现了从稠密到稀疏的运动表示压缩。

**3. 权重绘制函数**

这是连接静态高斯与运动图的关键桥梁。对于每个高斯点 $\mathbf{x}_0$，权重绘制函数计算其对每个图链接的依赖权重：

$$\mathcal{W}(\mathbf{x}_0, X_{\mathcal{L},0}) = \text{softmax}\big(\{K(\mathbf{x}_0, X_{\mathcal{L},0,i}) \mid \forall i \in [1, |\mathcal{L}|]\}\big)$$

其中核函数 $K$ 基于高斯点到链接线段的距离，通过指数衰减衡量亲和度：

$$K(\mathbf{x}_0, X_{\mathcal{L},0,i}) = \exp\big(-\gamma \cdot \text{dist}(\mathbf{x}_0, X_{\mathcal{L},0,i})\big)$$

$\gamma$ 为可学习的半径参数。softmax归一化确保每个高斯的所有链接权重之和为1，实现平滑的运动过渡。

**4. 双四元数蒙皮**

图链接的运动通过双四元数蒙皮（Dual Quaternion Skinning, DQS）传播到每个高斯。具体而言，计算每个链接从 $t=0$ 到 $t$ 的相对刚体变换 $\mathcal{R}(P_{\mathcal{L},0}, P_{\mathcal{L},t})$，然后根据权重绘制结果进行混合，得到高斯在时刻 $t$ 的位姿：

$$\mathbf{p}_t = B\big(\mathcal{R}(P_{\mathcal{L},0}, P_{\mathcal{L},t}), \mathcal{W}(\mathbf{x}_0, X_{\mathcal{L},0})\big) \cdot \mathbf{p}_0$$

DQS 保证混合结果始终位于 $\mathrm{SE}(3)$ 空间内，避免了线性混合可能产生的“糖纸”伪影。

**5. 可微渲染与联合优化**

变换后的高斯通过可微光栅化渲染为图像，与视频帧计算损失。梯度反向传播同时更新三项参数：运动图参数（链接位姿）、权重绘制函数参数（$\gamma$ 等）和3D高斯参数。这种端到端优化使运动图能够自动发现物体的运动结构，无需人工标注。

### 初始化策略

运动图在规范帧的初始化利用了基础模型的先验知识（Figure 6）：
- 使用 Grounding SAM2 获取实例分割掩码
- 使用 SAPIENS 估计2D人体骨架
- 对于变形图，通过最远点采样从点云中均匀采样并连接节点

框架还支持**逐实例重建**，通过实例分配矩阵 $M_{ij}$ 将高斯显式分组到不同实例，保持准确的实例几何——这是现有动态高斯泼溅方法未曾探索的能力。

### 与基线方法的本质差异

| 设计维度 | 隐式方法（4DGaussians, Deformable-GS） | MBGS |
|---------|--------------------------------------|------|
| 运动表示 | 神经网络变形场或逐高斯参数 | 显式稀疏运动图 |
| 运动密度 | 稠密（每高斯独立参数） | 稀疏（图参数<100） |
| 运动传播 | 网络前向推理 | 双四元数蒙皮混合 |
| 可操控性 | 仅能重放记录运动 | 可直接编辑运动图 |

这种设计使 MBGS 在保持与最先进方法可比渲染质量（iPhone数据集LPIPS 0.37 vs. Shape-of-Motion 0.39）的同时，解锁了新颖姿态动画、机器人演示合成和视觉规划等需要运动操控的下游应用。

## 核心模块与公式推导

MBGS 的核心思想是用**稀疏的显式运动图**替代隐式或逐高斯稠密运动参数，将运动建模与外观表示解耦。整个框架由五个关键模块构成，通过可微渲染端到端联合优化。

### 1. 静态3D高斯

场景的几何与外观由一组静态3D高斯表示。这些高斯在规范帧（$t=0$）重建后保持固定，仅其位姿随时间由运动图驱动变化。这从根本上区别于为每个高斯分配独立运动参数的稠密表示。

### 2. 运动图 (Motion Graph)

运动图是 MBGS 的**因果调节旋钮**——通过稀疏的显式结构参数化场景运动。图中每个链接 $l$ 在时间 $t$ 具有位姿 $P_{\mathcal{L},t}$，运动图参数总数通常少于100，而高斯数量可达数十万。框架支持两类图结构：

- **运动学树 (Kinematic Tree)**：层次化无环图，参数化为关节旋转 $\mathbf{r}_t \in SO(3)$、根节点位姿 $\mathbf{X}_t$ 和时不变链接长度 $\ell_i$，通过前向运动学计算世界坐标系下的链接位姿。适用于人体等关节化结构。
- **变形图 (Deformable Graph)**：无拓扑约束，节点可在3D空间自由移动，链接允许拉伸变形。每个链接的刚体位姿通过投影点移动公式和注视变换推导。

**投影点移动公式**解耦了链接的刚体运动与伸缩变形，投影点在链接上的位置按比例随链接拉伸移动：

$$\mathbf{n}_{\mathbf{x}_l, l} = \mathbf{n}_{s_l, t} + \frac{|\mathbf{n}_{\mathbf{x}_0, l} - \mathbf{n}_{s_l, 0}|}{|\mathbf{n}_{s_l, 0} - \mathbf{n}_{e_l, 0}|} (\mathbf{n}_{s_l, t} - \mathbf{n}_{e_l, t})$$

其中 $\mathbf{n}_{s_l, t}$ 和 $\mathbf{n}_{e_l, t}$ 是链接 $l$ 在时间 $t$ 的起止端点，$\mathbf{n}_{\mathbf{x}_0, l}$ 是高斯点 $\mathbf{x}_0$ 在链接上的投影点。

**注视变换**从投影点和链接方向推导每个链接的 SE(3) 位姿：

$$P_{\mathcal{L}}(\theta_t, \mathbf{x}_t) = \{\mathcal{A}(\mathbf{n}_{\mathbf{x}_t, l}, \mathrm{ray}(\mathbf{n}_{s_l, t}, \mathbf{n}_{e_l, t})), \forall l \in \mathcal{L}\}$$

其中 $\mathcal{A}$ 为注视变换，将投影点作为位置、链接方向作为朝向，构建刚体变换矩阵。

### 3. 权重绘制函数 (Weight Painting)

权重绘制函数 $\mathcal{W}$ 确定每个链接对每个高斯的控制权重，是连接稀疏运动图与稠密高斯的桥梁。基于高斯位置 $\mathbf{x}_0$ 与链接线段 $X_{\mathcal{L},0,i}$ 的距离，通过 softmax 归一化输出权重：

$$\mathcal{W}(\mathbf{x}_0, X_{\mathcal{L},0}) = \text{softmax}(\{K(\mathbf{x}_0, X_{\mathcal{L},0,i}) \mid \forall i \in [1, |\mathcal{L}|]\})$$

其中核函数 $K$ 采用指数衰减形式：

$$K(\mathbf{x}_0, X_{\mathcal{L},0,i}) = \exp(-\gamma \cdot \mathrm{dist}(\mathbf{x}_0, X_{\mathcal{L},0,i}))$$

$\gamma$ 为可学习的半径参数，控制每个链接的影响范围。该函数使运动图自动学习高斯与链接的软分配关系，无需手工指定蒙皮权重。

### 4. 双四元数蒙皮 (Dual Quaternion Skinning)

运动混合算子 $B$ 采用双四元数蒙皮（DQS），将各链接的相对刚体变换根据权重绘制结果平滑混合，生成高斯的最终位姿。MBGS 的核心运动传播公式为：

$$\mathbf{p}_t = B\big(\mathcal{R}(P_{\mathcal{L},0}, P_{\mathcal{L},t}), \mathcal{W}(\mathbf{x}_0, X_{\mathcal{L},0})\big) \cdot \mathbf{p}_0$$

其中 $\mathcal{R}$ 计算链接从 $t=0$ 到 $t$ 的相对变换，$B$ 将多个链接变换按权重混合。DQS 保证混合结果始终位于 SE(3) 流形内，避免线性混合导致的体积塌陷伪影。

### 5. 可微渲染与联合优化

变换后的高斯通过可微光栅化渲染为图像，与视频帧比较计算损失，梯度反向传播至运动图参数、权重绘制函数参数和3D高斯属性，实现端到端联合优化。运动图的连通性 $\mathcal{L}$ 作为固定超参数，不接收梯度也不随时间变化。对于变形图，$\mathcal{L}$ 通过最远点采样从点云初始化以保证物体表面均匀覆盖；运动学树则利用 Grounding SAM2 的分割掩码和 SAPIENS 的2D人体骨架进行初始化（见 Figure 6）。

整个管线将稠密的逐高斯运动建模问题转化为稀疏图运动参数的学习问题，在保持高保真重建的同时，获得了对运动的直接操控能力。

## 实验与分析

### 主结果

MBGS在两个主流动态场景基准上进行了评估：**iPhone数据集**（Gao et al.）和**HyperNeRF vrig数据集**（Park et al.）。论文强调LPIPS作为首选指标，因为它对图像感知质量更敏感，而PSNR和SSIM可能偏好模糊图像。

**iPhone数据集**（Table 1）：

![[assets/figures/papers/paper_list_l9_Motion_Blender_Gaussian_Splatting_for_Dynamic_Scene_Reconstruction/figures/008_Table_1.jpg]]
*Table 1: Novel view rendering on the highly challenging iPhone dataset [1]. LPIPS more accurately reflects perceptual quality*

- MBGS在LPIPS上达到**0.37**，超越当时SOTA方法**Shape-of-Motion**的0.39（Δ = -0.02）。
- PSNR为**16.79**，略高于Shape-of-Motion的16.67（Δ = +0.12）。
- SSIM为**0.65**，与Shape-of-Motion持平。
- 该数据集仅使用手持相机视频训练，固定相机视频用于评估，对运动表示的鲁棒性要求极高。

**HyperNeRF vrig数据集**（Table 2）：

![[assets/figures/papers/paper_list_l9_Motion_Blender_Gaussian_Splatting_for_Dynamic_Scene_Reconstruction/figures/010_Table_2.jpg]]
*Table 2: HyperNerf [16]. Our method performs competitively, closely matching SoTA in the key LPIPS metric*

- MBGS在LPIPS上达到**0.35**，与SOTA方法**4DGaussians**的0.36相当（Δ = -0.01）。
- 在chicken、3D printer、broom等场景上LPIPS可比或更优。
- PSNR和SSIM低于4DGaussians，但论文将此归因于LPIPS更能反映感知质量。

**渲染速度**：在40GB A100上，teddy bear场景（2M高斯）达18 FPS（无缓存）/ 25 FPS（有缓存），chicken toy场景（300K高斯）达32 FPS（无缓存）/ 46 FPS（有缓存），与基线方法可比。训练时间约10-30小时，取决于场景复杂度。

### 消融实验

**运动图尺寸**（Figure A2）：关节数从200增至1000时渲染质量反而下降，存在最优图尺寸。teddy场景在200关节时达到最佳渲染质量，过度增加关节数导致过拟合或运动表示退化。

**2D关键点正则化**（Figure A3左）：强制运动学树的3D投影与2D人体关键点一致，使LPIPS降低0.01-0.02，同时产生更干净的人体结构运动图。

**规范帧正则化**（Figure A3右）：防止运动图漂移，使其保持与物体表面对齐。无正则化时，图关节变得尖锐并向外漂移，破坏几何一致性。

**真实机器人实验**（Figure A1）：在KUKA机器人上验证视觉规划能力。布料折叠和微波炉门操作成功率达**10/10**，塑料绳弯曲成功率为**7/10**，无需任何机器人遥操作数据。

### 失败模式

Figure 11和Figure 13系统总结了主要失败模式：


![[assets/figures/papers/paper_list_l9_Motion_Blender_Gaussian_Splatting_for_Dynamic_Scene_Reconstruction/figures/013_Figure_11.jpg]]
*Figure 11: Failure Cases. Visualization of imperfect learned motion graphs (a), failure cases of novel pose editing (b), and failure cases of reconstructing reflective surfaces (c)*

![[assets/figures/papers/paper_list_l9_Motion_Blender_Gaussian_Splatting_for_Dynamic_Scene_Reconstruction/figures/015_Figure_13.jpg]]
*Figure 13: Failure Cases on Fast-Moving Objects. Visualization of shaking artifacts from strong camera motion (left), and reconstruction quality comparison of our MB-GS for the same microwave with doors moving at different speeds (right)*

1. **运动图未接地**：运动图有时未能准确附着在物体几何上。人手细部覆盖不全，枕头挤压变形不足，微波炉门对齐存在偏差。

2. **新颖姿态伪影**：编辑运动图生成未见姿态时出现视觉伪影。根因在于高斯缺乏显式表面表示，部分高斯在运动图作用下偏离物体表面。

3. **反射表面丢失**：机器人手臂在强光下表面模糊且失去反射性，当前方法不支持光照变化的动态场景重建。

4. **快速运动退化**：强相机运动或物体快速移动时（如剥香蕉场景）出现抖动伪影，重建质量显著下降。

5. **运动图方向错误**（Figure 12）：软绳运动图头端向桌子下方倾斜，导致机器人末端执行器抓取方向不正确，直接影响下游规划任务。


![[assets/figures/papers/paper_list_l9_Motion_Blender_Gaussian_Splatting_for_Dynamic_Scene_Reconstruction/figures/014_Figure_12.jpg]]
*Figure 12: A failure case of incorrect gripper orientation caused by an erroneous motion graph. The head of the rope motion graph is misaligned, tilting downward below the table surface*

6. **逐帧独立学习**：运动图参数逐帧独立优化，未有效利用帧间时间连续性，在长序列上可能累积漂移。

### 关键图表结论

- **Figure 4**：学习到的运动图与渲染图像高度对齐，权重绘制函数能合理分配各链接对高斯的控制权重，验证了显式运动表示的可解释性。
- **Figure 5**：通过操控运动图成功生成训练视频中未见的新颖姿态，证明显式运动表示的直接编辑能力。
- **Figure 7-8**：定性对比显示MBGS在iPhone和HyperNeRF数据集上均能产生更清晰的渲染结果，尤其在细节区域（LPIPS优势明显）。
- **Figure 9-10**：展示了从人类视频合成机器人演示和基于视觉规划的机器人动作预测两项应用，验证了显式运动图在下游任务中的独特价值。
## 方法谱系与知识库定位

### 与现有动态高斯泼溅方法的关系

MBGS 的核心定位在于**用显式稀疏运动图替代隐式稠密运动表示**，这一设计选择直接决定了它与现有方法的谱系关系。

**隐式运动表示范式**：以 **4DGaussians** 和 **Deformable-GS** 为代表的方法将运动编码进神经网络变形场，每个高斯的时变位姿通过 MLP 从规范帧映射得到。这类方法的优势在于表达能力强，能处理复杂非刚体变形，但代价是运动参数不可解释、无法编辑——用户只能重放记录的运动，无法操控场景产生训练视频中未见的新姿态。

**稠密显式运动范式**：以 **Shape-of-Motion**（iPhone 数据集上的先前 SOTA）为代表的方法为每个高斯分配独立的运动参数（数量常达数十万），采用浅层模型直接优化逐高斯的轨迹。这种方式避免了神经网络的隐式编码，但参数密度极高，且运动参数之间缺乏结构化关联，同样不具备可操控性。

MBGS 在这两条路径之间开辟了第三条路：**将运动压缩到稀疏图结构上（参数通常少于 100），通过可学习的权重绘制函数和双四元数蒙皮将图的运动传播到每个高斯**。这使得 MBGS 在保持与 SOTA 方法可比甚至更优的渲染质量（iPhone 数据集 LPIPS 0.37 vs Shape-of-Motion 0.39；HyperNeRF LPIPS 0.35 vs 4DGaussians 0.36）的同时，获得了前者不具备的运动操控能力。

### 与经典图形学方法的继承关系

MBGS 的运动表示和传播机制大量借鉴了经典计算机图形学技术，但在可微渲染框架下进行了重新设计：

- **双四元数蒙皮（DQS）**：继承自角色动画领域的标准蒙皮技术，用于将骨骼运动平滑混合到表面顶点。MBGS 将其适配到高斯泼溅框架中，以链接的相对 SE(3) 变换作为输入，在高斯层面实现运动混合，保证结果在 SE(3) 空间内的几何一致性。
- **运动学树**：直接继承机器人学中的刚体运动链表示（关节旋转 + 链接长度 + 前向运动学），但 MBGS 将关节旋转和链接长度都设为可学习参数，通过可微渲染端到端优化。
- **变形图**：继承自非刚体配准领域的自由形变表示，MBGS 将其改造为无拓扑约束的稀疏控制结构，通过投影点沿链接按比例移动（Eq. 3）解耦刚体运动与伸缩变形。

### 适用边界与局限

MBGS 的显式稀疏运动图设计在带来操控性优势的同时，也划定了其适用边界：

**优势场景**：
- **铰接体/类铰接体运动**：运动学树天然适配人手、机器人臂等具有清晰关节结构的对象（Figure 4 中手部运动图准确捕获手指关节运动）。
- **需要运动编辑和规划的任务**：新颖姿态动画（Figure 5）、机器人演示合成（Figure 9）、视觉规划（Figure 10）等应用直接受益于运动图的显式可操控性。
- **稀疏运动场景**：当场景运动可由少量控制点描述时（如布料折叠、微波炉门开合），MBGS 的稀疏图结构效率极高。

**已知局限**：

1. **运动图未接地问题**：学习到的运动图有时未能准确附着在物体几何上——人手细部覆盖不全、枕头挤压变形不足、微波炉门对齐偏差（Figure 11a）。这源于高斯缺乏显式表面表示，允许单个高斯在运动图作用下任意变形。

2. **新颖姿态伪影**：编辑运动图生成训练视频外的新姿态时，部分高斯偏离物体表面产生视觉伪影（Figure 11b）。根本原因是权重绘制函数基于规范帧距离学习，在远离训练分布的姿态下泛化能力有限。

3. **快速运动退化**：强相机运动或物体快速移动时（如剥香蕉场景），重建质量显著下降，出现抖动伪影（Figure 13）。这与逐帧独立学习运动图参数、未利用帧间时间连续性的设计有关。

4. **反射表面重建失败**：在强光下，机器人手臂等金属表面重建结果模糊且失去反射性（Figure 11c）。这是 3DGS 框架的通用局限，MBGS 未做针对性处理。

5. **运动图尺寸敏感性**：运动图关节数需人工设定，从 200 增至 1000 时渲染质量反而下降（Figure A2），表明存在最优图尺寸，但当前缺乏自适应图结构学习机制。

6. **视觉规划中的方向错误**：运动图错误可导致机器人末端执行器方向错误——例如软绳运动图头端向桌面下方倾斜，导致抓取方向不正确（Figure 12）。

### 开放问题与潜在发展方向

1. **语义/物理先验融合**：如何将基础模型（SAM、视觉语言模型）的语义理解或物理引擎（MuJoCo）的物理约束融入运动图学习，以增强几何一致性和运动合理性？论文已展示通过可微仿真学习物理参数的可行性方向。

2. **混合运动架构**：能否设计既保持显式操控性、又能利用神经网络预测运动图时变参数的混合架构？这有望解决当前逐帧独立学习导致的时间不一致问题，同时保留编辑能力。

3. **自适应图拓扑学习**：当前运动图连接关系固定且需人工设定。开发能根据物体结构自动调整连接关系和节点数量的自适应拓扑学习方法，将显著提升对不同场景的适应性。

4. **反射与光照感知重建**：将反射/光照变化建模纳入动态场景重建框架，使机器人等金属表面在动态场景中保持真实感，是机器人应用落地的关键需求。

5. **快速运动与复杂变形鲁棒性**：在剥香蕉、快速挥手等挑战性场景下，如何利用光流、事件相机等多模态信号或时序一致性约束提升重建稳定性和一致性？

6. **实例交互伪影消除**：机器人演示合成中，逐实例高斯替换带来的伪影和不真实交互（如手与物体的接触边界模糊）需要更精细的实例间交互建模。

## 原文 PDF

![[paperPDFs/CORL_2025/Motion_Blender_Gaussian_Splatting_for_Dynamic_Scene_Reconstruction.pdf]]
