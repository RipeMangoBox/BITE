---
title: "OmniDrag: Enabling Motion Control for Omnidirectional Image-to-Video Generation"
type: paper
paper_level: A
venue: IJCV
year: 2026
pdf_ref: paperPDFs/IJCV_2026/OmniDrag_Enabling_Motion_Control_for_Omnidirectional_Image_to_Video_Generation.pdf
project_link: https://lwq20020127.github.io/OmniDrag
code_link: null
aliases:
- OmniDrag
tags:
- IJCV_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "通过球面运动估计器（SME）利用HEALPix球面均匀网格进行轨迹初始化，并基于球面距离过滤重要运动，同时联合微调时间注意力层与轻量级全向控制器，在注入控制信号时引入球面几何先验，从而在不依赖完整UNet副本的情况下实现精确的球面运动控制。"
primary_logic: "联合微调扩散UNet中的时间注意力层并添加轻量级、以交叉归一化注入的全向控制器，同时通过球面几何感知的运动估计器生成训练轨迹与推理时的球面插值，可在不扭曲球面结构的前提下实现对全向视频的精确拖拽式运动控制。"
claims:
- "不联合微调时间注意力层会导致生成结果出现空间变形，证明该设计是处理球面运动模式的关键（Fig. 6）。"
- "在Move360数据集上，OmniDrag在ObjMC指标（0.044）和FVD（322.22）上均优于DragNUWA、DragAnything和MotionCtrl，证明其运动控制精度和视频质量优越（Table 1）。"
- "移除SME中的HEALPix初始化或球面距离过滤会导致对象控制失败或生成结果不稳定，验证了球面感知轨迹估计的必要性（Fig. 7）。"
- "Move360 上 ObjMC (ERP) = 0.044"
---

# OmniDrag: Enabling Motion Control for Omnidirectional Image-to-Video Generation

> [!tip] 核心洞察
> 联合微调扩散UNet中的时间注意力层并添加轻量级、以交叉归一化注入的全向控制器，同时通过球面几何感知的运动估计器生成训练轨迹与推理时的球面插值，可在不扭曲球面结构的前提下实现对全向视频的精确拖拽式运动控制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | OmniDrag：面向全向图像到视频生成的运动控制方法 |
| 英文题名 | OmniDrag: Enabling Motion Control for Omnidirectional Image-to-Video Generation |
| 会议/期刊 | IJCV 2026 |
| Links | [paper](https://arxiv.org/abs/2412.09623) · [Project](https://lwq20020127.github.io/OmniDrag) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | OmniDrag |
| Dataset | Move360, Move360 (Horizontal 8 viewports) |

> [!tip] 效果简介
> - Move360 上，ObjMC (ERP) 为 0.044，对比 未提供具体数值（OmniDrag最优）。
> - Move360 (Horizontal 8 viewports) 上，FVD 为 322.22，对比 未提供具体数值（OmniDrag最优）。
> - Move360 上，Human Evaluation Overall Score 为 75.7%，对比 未提供具体数值（OmniDrag最优）。

## 概要

全向视频（Omnidirectional Video, ODV）以等距矩形投影（Equirectangular Projection, ERP）格式存储，其固有的空间变形特性使得直接将2D视频运动控制方法迁移至ODV时，会引发严重的空间扭曲与控制失准。现有ODV数据集运动幅度有限，进一步制约了对复杂球面运动模式的学习。OmniDrag作为首个面向全向图像到视频生成的运动控制方法，旨在解决上述瓶颈。

OmniDrag的核心思路是**在扩散模型的去噪过程中注入球面几何先验**。具体而言，该方法包含两个关键设计：

- **球面运动估计器（Spherical Motion Estimator, SME）**：训练时，SME利用HEALPix球面等面积网格进行轨迹点初始化，并基于球面距离（大圆弧长）过滤具有显著运动的轨迹，从而提取球面感知的运动控制信号；推理时，用户仅需指定起始点和目标点，SME通过球面线性插值自动生成完整运动轨迹。
- **全向控制器与时间注意力联合微调**：OmniDrag采用轻量级的全向控制器（Omni Controller），通过交叉归一化（Cross-normalization）将控制信号注入Stable Video Diffusion（SVD）去噪UNet的首个块，同时联合微调UNet中的时间注意力层，以学习球面运动模式。这一设计避免了使用完整的可训练UNet编码器副本，在保持轻量化的同时实现了精确的球面运动控制。

在自建的Move360数据集上，OmniDrag在ObjMC指标（0.044）和FVD指标（322.22）上均优于DragNUWA、MotionCtrl和DragAnything等基线方法，人工评估总体得分达到75.7%。消融实验证实，联合微调时间注意力层是避免空间变形的关键，而SME中的HEALPix初始化与球面距离过滤对于稳定的对象控制不可或缺。该方法目前尚未解耦相机运动与物体运动，对复杂场景（如多人交互）的泛化能力有待进一步验证。



全向图像（omnidirectional images, ODIs）通过等距矩形投影（equirectangular projection, ERP）将 360° 球面场景映射到二维平面，为沉浸式内容创作提供了完整的空间覆盖。随着扩散模型在图像到视频（image-to-video, I2V）生成领域的快速发展，将静态全向图像转化为动态全向视频（omnidirectional videos, ODVs）的需求日益迫切。然而，现有的 I2V 生成方法主要针对常规透视视频设计，其运动控制机制无法直接适配全向视频的球面几何特性。

**核心瓶颈**在于 ERP 投影固有的空间变形与球面感知缺失。具体表现为两个层面：其一，ERP 图像中像素在球面上的面积分布极不均匀——赤道区域被欠采样，两极区域被过度拉伸——导致基于二维平面的运动估计和控制信号在映射到球面时产生严重的空间扭曲；其二，现有 ODV 数据集（如 PanoVOS 等）所包含的运动幅度有限，难以支撑模型学习复杂的球面运动模式。将已有的拖拽式运动控制方法（如 **DragNUWA**（Yin et al., arXiv 2023）、**MotionCtrl**（Wang et al., SIGGRAPH 2024）、**DragAnything**（Wu et al., ECCV 2025））直接应用于全向场景时，由于缺乏球面几何先验，生成结果往往出现控制不准确、空间变形以及环绕一致性破坏等问题。

**动机**源于填补上述方法缺口：需要一种能够感知球面几何的拖拽式运动控制框架，使得用户仅需在参考全向图像上指定起始点和目标点，即可生成运动精确、空间一致的高质量全向视频。这要求方法在三个层面进行根本性改进：训练阶段需从球面几何出发提取运动轨迹；控制信号的注入需适配扩散模型的去噪过程并引入球面结构先验；推理阶段需支持基于球面插值的轨迹生成，从而在不依赖完整 UNet 副本的前提下实现高效的球面运动控制。



## 核心方法与创新机理

OmniDrag 的核心创新在于将 2D 拖拽式运动控制方法适配到全向视频（ODV）的球面几何空间。现有方法（如 DragNUWA、MotionCtrl、DragAnything）直接在等距矩形投影（ERP）图像上操作，忽略了球面投影带来的空间变形，导致运动控制不准确和生成结果扭曲。OmniDrag 通过以下三个关键设计解决了这一问题：

### 1. 球面运动估计器（SME）：从平面到球面的轨迹提取与交互

SME 是 OmniDrag 区别于所有 baseline 的最根本创新，贯穿训练和推理两个阶段。

**训练阶段**：现有方法在 ERP 图像上使用均匀网格初始化跟踪点，这会导致球面极点区域过采样、赤道区域欠采样。OmniDrag 改用 **HEALPix 等面积球面网格** 进行点初始化，确保球面上的均匀采样。随后，SME 不再以 ERP 平面上的像素距离衡量运动幅度，而是计算轨迹起止点之间的**球面大圆距离**（Eq. 7），仅保留球面距离超过阈值 $d_{th}$ 的显著运动轨迹（Eq. 8）。这一过滤机制直接解决了 ODV 数据集中运动幅度有限的问题——消融实验（Fig. 7）表明，移除 HEALPix 初始化会导致对象控制失败，移除球面距离过滤则使生成结果不稳定。

**推理阶段**：Baseline 方法要求用户在参考 ERP 图像上绘制完整运动轨迹，交互负担重且难以保证球面几何合理性。OmniDrag 将用户交互简化为仅指定**起始点和目标点**，SME 自动通过**球面线性插值（slerp，Eq. 9）** 生成中间帧的球面坐标轨迹，再将其投影回 ERP 坐标用于控制信号注入。这一设计使用户无需理解球面几何即可实现精确的运动控制。

### 2. 联合微调时间注意力层：让扩散模型学会球面运动

现有方法（如 DragNUWA、MotionCtrl）通常冻结 UNet 主分支，仅训练一个独立的控制编码器副本，将控制信号注入冻结的去噪网络。这种策略在 2D 视频中有效，但无法处理全向视频中因 ERP 投影产生的空间变形。

OmniDrag 的关键发现是：**必须联合微调 UNet 中的时间注意力层**，使去噪网络本身能够学习球面运动模式。消融实验（Fig. 6）直接证明了这一设计的必要性——若不联合微调时间注意力层，生成结果会出现明显的空间变形。这一发现揭示了时间注意力层在编码跨帧运动一致性中的核心作用，尤其是在球面几何约束下。

### 3. 轻量级全向控制器：以交叉归一化替代完整 UNet 副本

现有方法通常使用一个可训练的完整 UNet 编码器副本来提取控制信号，参数量大且训练成本高。OmniDrag 采用**轻量级卷积模块**（仅含若干 ResNet 块）作为全向控制器（Omni Controller），并通过**交叉归一化（cross-normalization，Eq. 5）** 将控制特征注入主分支的首个 SVD 块。

交叉归一化的核心思想是：利用主分支潜变量的均值 $\pmb{\mu}_m$ 和方差 $\pmb{\sigma}_m$ 对控制特征 $\mathbf{z}_c$ 进行归一化，而非使用控制分支自身的统计量。这使得控制信号能够自适应地与主分支的特征分布对齐，在轻量架构下实现高效且稳定的控制信号注入。

### 创新点总结

| 设计维度 | 现有方法 | OmniDrag |
|---------|---------|----------|
| 轨迹初始化 | ERP 平面均匀网格 | HEALPix 球面等面积网格 |
| 运动度量 | ERP 像素距离 | 球面大圆距离 |
| 控制模块 | 完整 UNet 编码器副本 | 轻量级 ResNet + 交叉归一化 |
| 训练策略 | 冻结 UNet 主分支 | 联合微调时间注意力层 |
| 用户交互 | 绘制完整轨迹 | 仅指定起止点，slerp 自动插值 |

这些创新并非孤立存在，而是形成了从数据生成（SME 提取球面感知轨迹）到模型训练（联合微调时间注意力 + 轻量控制器注入）再到推理交互（slerp 球面插值）的完整闭环，共同解决了全向视频运动控制中球面几何失真的核心瓶颈。



![[assets/figures/papers/paper_list_l17_OmniDrag_Enabling_Motion_Control_for_Omnidirectional_Image_to_Video_Gene/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline of proposed OmniDrag. (a) During training, spherical motion is extracted by the proposed spherical motion estimator. The Omni Controller and temporal attention layers in the UNet denoiser are jointly fine-tuned. (b) During inference, OmniDrag allows users to simply select handle and target points on the reference image and generates ODVs with the corresponding motion*

OmniDrag 的整体流程围绕“球面感知的运动提取—轻量级控制注入—联合时间建模”三条主线组织，分为训练与推理两个阶段，如 Figure 2 所示。

**训练阶段**：输入一段全向视频及其对应的首帧参考图像，首先由**球面运动估计器（SME）**在 HEALPix 等面积球面网格上初始化跟踪点，通过逐帧追踪提取运动轨迹，并基于球面距离（大圆弧长）过滤出具有显著运动的轨迹作为控制信号。这些轨迹条件随后被送入**全向控制器（Omni Controller）**——一个仅由若干 ResNet 块构成的轻量级卷积模块，提取控制特征后通过交叉归一化（cross-normalization）注入到 Stable Video Diffusion（SVD）去噪 UNet 主分支的首个块中。与此同时，UNet 中的**时间注意力层**与全向控制器被联合微调，使模型能够学习球面运动模式，避免因等距矩形投影（ERP）的空间变形导致的生成扭曲。

**推理阶段**：用户只需在参考全向图像上指定控制点（handle point）和目标点（target point），SME 通过球面线性插值（slerp）自动生成完整的球面运动轨迹，并将其转换为与训练一致的轨迹条件表示，驱动 SVD 去噪过程生成符合运动意图的全向视频。

**核心模块关系**：
- **SME** 负责运动轨迹的提取（训练）与插值生成（推理），是连接用户交互与模型控制信号的桥梁。
- **Omni Controller** 将轨迹条件转化为去噪网络可用的控制特征，并通过交叉归一化实现高效注入，避免了使用完整 UNet 编码器副本带来的参数量膨胀。
- **时间注意力层** 的联合微调是处理球面运动模式的关键——消融实验（Figure 6）表明，若冻结该部分而仅训练控制器，生成结果会出现明显的空间变形。

整个框架建立在预训练 SVD 模型之上，训练时额外采用了潜在旋转机制以增强全向视频的环视一致性。



OmniDrag 的核心架构由三个关键模块构成：**球面运动估计器**（Spherical Motion Estimator, SME）、**全向控制器**（Omni Controller）以及基于 **Stable Video Diffusion (SVD)** 的联合微调策略。以下逐一展开其设计逻辑与核心公式。

---

### 3.1 扩散模型基础

OmniDrag 建立在预训练的 SVD 模型之上。给定参考全向图像 $\mathbf{c}_I$，去噪器 $\Phi_\theta$ 从噪声潜在变量 $\mathbf{z}_t$ 和时间步 $t$ 预测干净的潜在表示：

$$\hat{\mathbf{z}}_0 = \Phi_\theta(\mathbf{z}_t, t, \mathbf{c}_I) \tag{1}$$

该去噪器遵循 EDM 预处理框架进行参数化：

$$\Phi_\theta(\mathbf{z}_t, t, \mathbf{c}_I; \sigma) = c_{skip}(\sigma) \mathbf{z}_t + c_{out}(\sigma) F_\theta(c_{in}(\sigma) \mathbf{z}_t, t, \mathbf{c}_I; c_{noise}(\sigma)) \tag{2}$$

其中 $F_\theta$ 为可学习的 3D UNet，$c_{skip}$、$c_{out}$、$c_{in}$、$c_{noise}$ 是依赖于噪声水平 $\sigma$ 的预处理系数。训练目标为去噪得分匹配损失：

$$\mathbb{E}_{\mathbf{z}_0, t, \mathbf{n} \sim \mathcal{N}(0, \sigma^2)} \left[ \lambda_\sigma \| \Phi_\theta(\mathbf{z}_0 + \mathbf{n}, t, \mathbf{c}_I) - \mathbf{z}_0 \|_2^2 \right] \tag{3}$$

---

### 3.2 全向控制器与交叉归一化注入

与现有方法（如 **DragNUWA** (Yin et al., arXiv 2023)、**MotionCtrl** (Wang et al., SIGGRAPH 2024)）使用完整可训练的 UNet 编码器副本不同，OmniDrag 采用轻量级全向控制器。该控制器仅由轨迹嵌入模块和若干 ResNet 块构成，大幅降低了可训练参数量。

控制信号 $\mathbf{c}$ 经控制器 $\mathcal{F}_c$ 提取后，通过交叉归一化注入主去噪分支的首个 SVD 块。更新后的扩散特征 $\mathbf{y}_m$ 为：

$$\mathbf{y}_m = \mathcal{F}_m \left( \mathbf{z}, \mathcal{F}_c ( \mathbf{c}; \boldsymbol{\Theta}_c ); \boldsymbol{\Theta}_m \right) \tag{4}$$

其中 $\mathcal{F}_m$ 为主 UNet 去噪分支，$\boldsymbol{\Theta}_c$ 和 $\boldsymbol{\Theta}_m$ 分别为控制器和主分支的可训练参数。

**交叉归一化**（cross-normalization）是注入机制的关键：利用主分支潜在变量的统计量对控制特征进行归一化，而非使用控制特征自身的统计量。设 $\mathbf{z}_c = \mathcal{F}_c(\mathbf{c}; \boldsymbol{\Theta}_c)$ 为控制器输出的潜在条件信号，$\boldsymbol{\mu}_m$ 和 $\boldsymbol{\sigma}_m$ 为主分支潜在变量的均值和标准差，则归一化后的控制信号为：

$$\hat{\mathbf{z}}_c = \frac{\mathbf{z}_c - \boldsymbol{\mu}_m}{\sqrt{\boldsymbol{\sigma}_m^2 + \epsilon}} * \gamma \tag{5}$$

其中 $\gamma$ 为可学习的缩放参数，$\epsilon$ 为防止除零的小常数。该设计使控制信号在统计分布上与主分支对齐，从而在不扭曲球面结构的前提下实现高效注入。

---

### 3.3 球面运动估计器

球面运动估计器（SME）是 OmniDrag 实现球面感知运动控制的核心，在训练和推理阶段承担不同角色。

#### 训练阶段：HEALPix 初始化与球面距离过滤

**问题瓶颈**：直接在 ERP 图像上使用均匀网格初始化跟踪点，会因 ERP 投影在两极区域的面积畸变导致球面采样不均匀，进而遗漏极地区域的运动信息。

**解决方案**：SME 采用 HEALPix 球面等面积网格初始化跟踪点 $\mathbf{P}^0$，确保在球面上均匀采样。随后通过跟踪函数 $\mathcal{F}_t$ 在输入视频 $\mathbf{V}$ 上提取运动轨迹：

$$\mathcal{T} = \mathcal{F}_t \left( \mathbf{P}^0, \mathbf{V} \right) \tag{6}$$

为筛选具有显著运动的轨迹（这对学习运动可控性至关重要），SME 基于球面大圆距离而非 ERP 平面像素距离来度量运动幅度。对于轨迹 $\mathbf{T}_j$，其起点 $(\theta_j^0, \phi_j^0)$ 与终点 $(\theta_j^{L-1}, \phi_j^{L-1})$ 的球面距离为：

$$D(\mathbf{T}_j) = \operatorname{arccos} \left( \sin(\theta_j^0) \sin(\theta_j^{L-1}) + \cos(\theta_j^0) \cos(\theta_j^{L-1}) \cos(\phi_j^0 - \phi_j^{L-1}) \right) \tag{7}$$

其中 $\theta$ 和 $\phi$ 分别为球面坐标的余纬度和经度，$L$ 为视频帧数。基于阈值 $d_{th}$ 过滤后的轨迹集为：

$$\mathcal{T}' = \{ \mathbf{T} \in \mathcal{T} \mid D(\mathbf{T}_j) > d_{th} \} \tag{8}$$

**消融证据**（Fig. 7）：移除 HEALPix 初始化导致对象控制失败（汽车不受控），移除球面距离过滤则生成结果不稳定，验证了球面感知轨迹估计的必要性。

#### 推理阶段：球面线性插值

推理时，用户仅需在参考 ERP 图像上指定手柄点（handle point）和目标点（target point），SME 通过球面线性插值（slerp）自动生成完整的运动轨迹。设起点球面坐标为 $(\theta^0, \phi^0)$，终点为 $(\theta^{L-1}, \phi^{L-1})$，中间帧 $i$ 的坐标为：

$$\theta^i = \arcsin\left( \frac{\sin((1 - t_i) \omega) \sin\theta^0 + \sin(t_i \omega) \sin\theta^{L-1}}{\sin\omega} \right), \quad \phi^i = \phi^0 + t_i (\phi^{L-1} - \phi^0) \tag{9}$$

其中 $\omega$ 为起止点间的球面角距离，$t_i = i / (L-1)$ 为插值因子。插值后的球面坐标被转换回 ERP 坐标，与用户指定的起止点合并形成完整的轨迹条件 $\tilde{\mathcal{T}} \in \mathbb{R}^{N_p \times L \times 2}$。

轨迹点最终以速度向量序列的形式表示，作为控制器的输入条件：

$$\left\{ (0, 0), (u_{(x_1, y_1)}, v_{(x_1, y_1)}), \ldots, (u_{(x_{L-1}, y_{L-1})}, v_{(x_{L-1}, y_{L-1})}) \right\}$$

其中 $u$ 和 $v$ 为相邻帧间的位置差，首帧及非轨迹位置的速度设为零。

---

### 3.4 联合微调时间注意力层

**关键设计决策**：OmniDrag 在训练全向控制器的同时，联合微调 SVD UNet 中的时间注意力层。消融实验（Fig. 6）表明，若不联合微调时间注意力层，生成结果会出现明显的空间变形——这是因为冻结的时间注意力层缺乏对球面运动模式的感知能力，无法正确建模 ERP 格式下的非刚性球面运动。联合微调使得时间注意力层能够学习球面几何先验，从而在不依赖完整 UNet 副本的情况下实现精确的球面运动控制。



## 实验与关键发现

OmniDrag 在自建的全向视频数据集 **Move360** 上与三类代表性基线方法进行了定量与定性对比，并通过系统消融实验验证了各核心组件的有效性。

### 实验设置

OmniDrag 以预训练的 **Stable Video Diffusion (SVD)** 模型为生成骨干网络。训练阶段，**Spherical Motion Estimator (SME)** 从 Move360 视频中自动提取球面运动轨迹，并作为控制条件输入 **Omni Controller**；该控制器与 SVD UNet 中的时间注意力层联合微调。推理阶段，用户仅需在参考 ERP 图像上指定拖拽的起始点与目标点，SME 通过球面线性插值（slerp）自动生成完整轨迹，驱动全向视频生成。为增强全向视频的环绕一致性，方法还引入了潜在空间旋转机制。

### 主实验结果

**Table 1** 报告了 OmniDrag 与 **DragNUWA** (Yin et al., arXiv 2023)、**MotionCtrl** (Wang et al., SIGGRAPH 2024) 和 **DragAnything** (Wu et al., ECCV 2025) 的定量对比。评估采用自动指标与人工评估相结合的方式，在 ERP 格式和水平 8 视口（Horizontal 8 Viewports）两种表示下进行。


![[assets/figures/papers/paper_list_l17_OmniDrag_Enabling_Motion_Control_for_Omnidirectional_Image_to_Video_Gene/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparisons between our OmniDrag and other methods. We employ automatic metrics (FVD [55], FID [51] and ObjMC [62]) on both ERP format and final horizontal eight viewports. We also conduct a human evaluation to assess the performance. Throughout this paper, the best and second-best results are highlighted in bold red and underlined blue, respectively*

在运动控制精度方面，OmniDrag 在 ERP 格式下的 ObjMC 指标达到 **0.044**，显著优于所有基线方法，表明其对球面运动的控制更为精确。在视频生成质量方面，OmniDrag 在水平 8 视口上的 FVD 为 **322.22**，同样取得最优结果。人工评估进一步印证了这一优势：OmniDrag 的综合评分达到 **75.7%**，在运动匹配度和视觉质量两个维度上均获得最高偏好率。

**Figure 5** 展示了场景级和对象级控制下的视觉对比。在场景级控制（道路前进）案例中，DragNUWA 和 DragAnything 生成的结果出现明显的空间扭曲或运动方向错误，而 OmniDrag 借助 SME 估计的球面合理轨迹，实现了稳定、准确的场景推进。在对象级控制（车辆沿道路移动）案例中，基线方法无法使目标物体沿用户指定路径运动，OmniDrag 则精确地控制了车辆的位置变化。

### 消融实验

**Figure 6** 展示了联合微调时间注意力层和 Move360 数据集训练的消融效果。移除时间注意力层的联合微调（w/o Fine-tuning Temporal Attention）后，生成结果出现严重的空间变形，表明时间注意力层是学习球面运动模式的关键瓶颈。使用缺乏丰富运动模式的非 Move360 数据集训练，则导致场景级运动控制失败，验证了 Move360 数据集对学习复杂全向运动模式的必要性。

**Figure 7** 和 **Table 2** 系统消融了 SME 的三个核心组件：

![[assets/figures/papers/paper_list_l17_OmniDrag_Enabling_Motion_Control_for_Omnidirectional_Image_to_Video_Gene/figures/008_Figure_7.jpg]]
*Figure 7: Ablation study on proposed spherical motion estimator (SME). The “w/o HEALPix init.” variant fails to control the car, the “w/o spherical dist. filter” variant generates unstable result, and the “w/o spherical interp.” variant leads to unintended path. In contrast, our OmniDrag leverages SME to obtain precise and reasonable trajectories during training and inference, achieving pleasant results*

![[assets/figures/papers/paper_list_l17_OmniDrag_Enabling_Motion_Control_for_Omnidirectional_Image_to_Video_Gene/figures/009_Table_2.jpg]]
*Table 2: Ablation study on five variants of OmniDrag*

- **移除 HEALPix 初始化（w/o HEALPix init.）**：跟踪点无法在球面上均匀分布，导致对象控制完全失败。
- **移除球面距离过滤（w/o spherical dist. filter）**：大量低运动幅度的噪声轨迹被保留，生成结果不稳定，出现抖动或运动方向漂移。
- **移除球面插值（w/o spherical interp.）**：推理时轨迹路径偏离用户意图，导致物体沿错误路径移动。

定量消融（Table 2）表明，完整 OmniDrag 在 FVD 和 ObjMC 两项指标上均优于所有消融变体，进一步确认了 HEALPix 初始化、球面距离过滤和球面插值三者对实现精确球面运动控制的必要性。

### 失败模式与局限性

尽管 OmniDrag 在场景级和对象级运动控制上表现优异，目前的方法尚未解耦相机运动与物体运动。在某些情况下，控制信号可能同时驱动背景和前景物体移动，导致控制粒度不够精细。此外，方法对未见过的复杂球面运动模式（如多人交互、非刚性变形）的泛化能力尚未得到充分验证。这些问题构成了未来工作的重要方向。



## 定位与知识库关联

### 问题定位与核心瓶颈

OmniDrag 解决的核心问题是：**将已有的2D拖拽式运动控制方法直接应用于全向视频（ODV）生成时，等距矩形投影（ERP）固有的空间变形会导致控制失效**。具体而言，ERP 格式将球面信息映射到平面时，极地区域被严重拉伸，而赤道区域相对压缩。当 DragNUWA（Yin et al., arXiv 2023）、MotionCtrl（Wang et al., SIGGRAPH 2024）、DragAnything（Wu et al., ECCV 2025）等2D轨迹控制方法在 ERP 图像上提取和注入运动信号时，其平面均匀采样的轨迹点无法反映球面上的真实运动分布，且基于像素距离的运动幅度度量在球面几何下失真，导致生成的视频出现空间扭曲与控制不准确。此外，现有 ODV 数据集（如先前工作使用的素材）运动幅度有限，进一步限制了对复杂球面运动模式的学习能力。

### 方法谱系与差异化设计

OmniDrag 建立在 Stable Video Diffusion（SVD）预训练模型之上，沿用了“轨迹条件注入扩散去噪过程”的通用范式，但在三个关键维度上引入了球面几何感知的改造：

| 设计维度 | 2D 基线方法（DragNUWA / MotionCtrl / DragAnything） | OmniDrag 的差异化设计 |
|---------|--------------------------------------------------|---------------------|
| **轨迹初始化** | 在 ERP 平面上使用均匀网格初始化跟踪点 | 使用 HEALPix 球面等面积网格初始化，确保球面均匀采样 |
| **运动幅度度量** | 在 ERP 平面上计算像素距离 | 基于球面距离（大圆弧长）度量并过滤轨迹 |
| **控制模块训练** | 冻结 UNet 主分支，仅训练独立的控制编码器副本 | 联合微调轻量级全向控制器与 UNet 中的时间注意力层 |
| **推理交互** | 用户需在参考 ERP 图像上绘制完整运动轨迹 | 用户仅需指定起始点和目标点，系统通过球面插值自动生成完整轨迹 |
| **控制信号注入** | 使用可训练的 UNet 编码器副本提取控制信号 | 使用轻量级卷积模块（含 ResNet 块和交叉归一化）注入至主分支首个块 |

这些差异化设计构成了 OmniDrag 的方法创新链：**球面运动估计器（SME）** 在训练阶段通过 HEALPix 初始化和球面距离过滤提取球面感知的运动轨迹，在推理阶段通过球面线性插值（slerp）将用户指定的起止点转化为完整轨迹；**全向控制器（Omni Controller）** 以轻量级卷积模块替代完整的 UNet 编码器副本，并通过交叉归一化（cross-normalization）利用主分支统计量对控制特征进行归一化后注入；**时间注意力层的联合微调** 使得扩散模型能够学习球面运动模式，消融实验（Figure 6）证明，若不联合微调时间注意力层，生成结果会出现严重的空间变形，这一定性证据表明时间注意力层是处理球面运动模式的关键组件。

### 证据强度与适用边界

**决定性证据**：
- 在 Move360 数据集上，OmniDrag 在 ObjMC 指标（0.044）和 FVD（322.22，水平八视口）上均优于 DragNUWA、DragAnything 和 MotionCtrl（Table 1），证明其运动控制精度和视频质量优越。
- 消融实验（Figure 7）表明，移除 SME 中的 HEALPix 初始化导致对象控制失败，移除球面距离过滤导致生成结果不稳定，移除球面插值导致路径错误，验证了球面感知轨迹估计各组件的必要性。
- 联合微调时间注意力层的消融（Figure 6）显示，不进行此操作会导致空间变形，证明该设计是处理球面运动模式的关键。

**适用边界与局限**：
- 当前方法**未解耦相机运动与物体运动**，在某些情况下可能同时移动背景和物体，导致控制不够精细。这是论文明确指出的已知局限。
- 对**未见过的复杂球面运动模式**（如多人交互、非刚性变形）的泛化能力尚未充分验证，需要人工评估补充。
- 方法依赖 Move360 数据集进行训练，该数据集由 Insta360 Titan 在车载移动场景下采集，覆盖室内、绿地、城市和夜间场景，但运动模式以车辆前向移动为主，可能限制对其他类型球面运动（如旋转、俯仰剧烈变化）的泛化。

### 开放问题

1. **相机-物体运动解耦**：如何将场景级运动（相机运动）与对象级运动（物体独立运动）分离，实现更精细的独立控制，是论文明确指出的开放问题。
2. **复杂场景泛化**：在多人交互、非刚性变形等更复杂场景中，当前基于稀疏轨迹的控制范式能否保持精度和稳定性，需要进一步验证。
3. **多模态控制融合**：所提方法能否与其他控制信号（如文本描述、深度图）融合，以提供更全面的可控性，是值得探索的方向。



## 原文 PDF

![[paperPDFs/IJCV_2026/OmniDrag_Enabling_Motion_Control_for_Omnidirectional_Image_to_Video_Generation.pdf]]
