---
title: "ORCaS: Unsupervised Depth Completion via Occluded Region Completion as Supervision"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ORCaS_Unsupervised_Depth_Completion_via_Occluded_Region_Completion_as_Supervision.pdf
openreview_forum_id: v2skNLbrfF
aliases:
- OORCAS
- ORCaS
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "在隐空间中对遮挡区域的特征进行补全（Contextual eXtrapolation），并将该过程作为额外的训练监督信号。"
primary_logic: "强制网络预测输入视图中不可见的遮挡区域特征，促使模型学习对三维场景形状的强归纳偏置；该偏置在测试时被用于调制输入视图特征，从而提升深度补全的保真度与泛化能力。"
claims:
- "ORCaS 通过预测输入视图中不可见的遮挡区域隐特征来学习归纳偏置。"
- "ORCaS 损失在隐空间强制预测特征与相邻视图编码特征一致，从而将遮挡区域完成为有效监督信号。"
- "ORCaS 在 VOID1500 和 NYUv2 上所有指标平均超越现有最佳方法 8.91%。"
- "从 VOID1500 到 ScanNet 和 NYUv2 的零样本泛化平均提升 15.7%。"
---

# ORCaS: Unsupervised Depth Completion via Occluded Region Completion as Supervision

> [!tip] 核心洞察
> 强制网络预测输入视图中不可见的遮挡区域特征，促使模型学习对三维场景形状的强归纳偏置；该偏置在测试时被用于调制输入视图特征，从而提升深度补全的保真度与泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ORCaS：通过遮挡区域完成监督的无监督深度补全 |
| 英文题名 | ORCaS: Unsupervised Depth Completion via Occluded Region Completion as Supervision |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=v2skNLbrfF) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | ORCaS (Occluded Region Completion as Supervision) |
| Dataset | VOID1500, NYUv2, KITTI DC |

> [!tip] 效果简介
> - VOID1500 上，MAE (mm) 为 30.90，对比 33.32 (AugUndo)，变化 -2.42 (7.81%  improvement)。
> - NYUv2 上，MAE (mm) 为 86.50，对比 96.73 (AugUndo)，变化 -10.23 (10.6% improvement)。
> - KITTI DC 上，MAE (mm) 为 253.17，对比 256.37 (AugUndo)，变化 -3.20 (1.2% improvement)。

## 概述

无监督深度补全是三维视觉中的一项基础任务：给定稀疏深度测量和单张 RGB 图像，预测稠密深度图。现有无监督方法依赖共视区域的光度重投影损失、稀疏深度一致性以及平滑正则化来驱动网络学习，但这些监督信号仅覆盖输入视图中可见的区域，对因遮挡而不可见的区域完全失语。这导致模型学到的归纳偏置本质上仍局限于二维图像正则化，难以抽象出完整的三维物体形状——而这恰恰是深度补全在物体边界、遮挡边缘处保真度不足的根源。

ORCaS（Occluded Region Completion as Supervision）提出了一个关键思路：**将遮挡区域的隐空间特征补全作为额外的训练监督信号**。具体而言，在训练阶段，网络被强制预测输入视图中不可见、但存在于三维场景中的遮挡区域隐特征，并与相邻视图编码得到的真实特征对齐。这一过程通过一个名为 ConteXt（Contextual eXtrapolation）的上下文外推模块实现——它从共视区域聚集信息，填充经刚体变换后产生的空体素。由此学到的三维形状归纳偏置在推理时被迁移用于调制输入视图特征，使解码器能够输出更高保真度的稠密深度图。推理阶段仅需单帧输入，无需相邻视图或位姿。

核心结论可归纳为三点：

1. **性能显著提升**：在 VOID1500 和 NYUv2 两个标准基准上，ORCaS 在所有评估指标上平均超越此前最优方法 AugUndo（ICLR 2025）**8.91%**。其中 VOID1500 上 MAE 降至 30.90 mm（相对提升 7.81%），NYUv2 上 MAE 降至 86.50 mm（相对提升 10.6%）。

2. **泛化能力突出**：从 VOID1500 零样本迁移到 ScanNet 和 NYUv2 时，ORCaS 平均提升 **15.7%**；在极低稀疏度输入（VOID500）下，相较于基线方法平均提升 **37.4%**，且对相机标定噪声（最高 30%）表现出良好鲁棒性。

3. **机制有效且高效**：消融实验表明，ORCaS 损失单独贡献了 **21.6%** 的性能增益；隐空间特征监督显著优于直接深度监督。ORCaS 参数量仅 24.9M，推理速度达 57 FPS（17.5 ms/帧），在效率和精度之间取得了有利平衡。

方法定位上，ORCaS 属于无监督深度补全框架，其训练范式与现有方法兼容——可在标准光度-稀疏-平滑损失基础上叠加 ORCaS 损失。当前方法的局限性包括：依赖静态场景假设和相邻视图位姿，尚未在非透视相机模型上验证，极低稀疏度下的绝对误差仍有改善空间。

## 背景与动机

深度补全任务旨在从稀疏深度测量（如LiDAR点云）和对应的RGB图像中预测稠密深度图，是三维视觉中的基础问题。监督学习方法依赖昂贵的稠密深度真值，限制了其可扩展性；无监督方法则通过光度重投影损失、稀疏深度一致性约束和平滑正则化来驱动训练，避免了对真值的需求。

现有无监督深度补全方法存在一个根本性瓶颈：其监督信号仅来源于输入视图与相邻视图之间的**共视区域**。具体而言，光度损失仅在两个视图都能观测到的像素上计算，稀疏深度一致性也仅作用于输入视图中有测量的位置。这意味着模型从未被要求推理那些在输入视图中被遮挡、但在三维场景中真实存在的区域。由此学习到的归纳偏置本质上仍局限于二维图像正则化——模型学会的是如何利用图像纹理和平滑性先验来插值深度，而非理解三维物体的完整形状。

这一瓶颈的后果体现在多个方面：模型在均匀纹理区域容易产生过度平滑的深度估计，在深度不连续处（如物体边界）难以保持清晰边缘，且泛化能力受限。当输入稀疏度进一步降低或场景域发生偏移时，缺乏三维形状理解的模型性能退化尤为显著。

ORCaS 的核心动机正是针对这一缺口：**能否将遮挡区域从“被忽略的盲区”转化为“有效的训练监督信号”？** 作者提出的关键洞见是，通过在隐空间中对遮挡区域的特征进行补全，并强制预测结果与相邻视图的编码特征一致，可以迫使模型学习对三维场景形状的强归纳偏置。这一偏置在测试时被用于调制输入视图的特征，从而在不增加推理成本的前提下，提升深度补全的保真度与泛化能力。

具体而言，ORCaS 在训练时构造了一个“病态”优化目标：预测输入视图中不可见、但存在于三维场景中的遮挡区域隐特征。这一过程通过以下机制实现：将输入视图的二维特征广播到三维体素空间，利用相对位姿将三维特征刚体变换到相邻视图，再通过上下文外推（ConteXt）模块从共视区域聚集信息来填充因遮挡而产生的空体素。训练时，预测的相邻视图三维特征被强制与从相邻视图直接编码得到的特征一致（通过 ORCaS 损失），从而将遮挡区域完成为有意义的监督信号。

与现有方法相比，ORCaS 的设计具有两个根本性差异：其一，训练监督信号不再局限于共视区域，而是扩展到遮挡区域的特征空间；其二，推理时无需相邻视图或位姿信息，仅需单帧输入即可完成深度补全——训练阶段学到的三维形状归纳偏置已内化到网络参数中，通过 ConteXt 机制调制输入视图特征，提升输出质量。

## 核心创新

### 问题瓶颈：共视监督的局限性

现有无监督深度补全方法的核心训练信号来自相邻视图之间的共视区域——通过光度重投影损失、稀疏深度一致性损失与平滑正则项联合优化（式(2)）。这一范式本质上将学习约束在二维图像域：网络仅需学会在可见像素之间插值稠密深度，却从未被要求推理因遮挡而不可见的三维结构。其后果是，模型习得的归纳偏置始终停留在图像正则化层面，难以抽象出物体完整的三维形状，导致在遮挡边界、均匀纹理区域以及低稀疏度输入下保真度不足。

### 核心洞察：将遮挡区域转化为监督信号

ORCaS 的根本创新在于**将训练范式从“利用共视区域监督”转变为“通过补全遮挡区域来学习”**。具体而言，方法在训练时引入一个不适定目标：预测输入视图中不可见的遮挡区域在隐空间中的特征，并以相邻视图实际编码出的特征作为监督，迫使网络发展出对三维场景形状的强归纳偏置。这一偏置在推理时被迁移用于调制输入视图的特征，从而提升深度补全的保真度与泛化能力。

### 关键机制：ConteXt 遮挡特征补全

实现上述洞察的技术抓手是 **Contextual eXtrapolation (ConteXt) 模块**及其配套的 ORCaS 损失。该机制通过以下因果链运作：

1. **2D→3D 广播与刚体变换**：输入视图的二维特征 $h[x]$ 经由深度概率分布 $\tilde{d}[x] = \sigma(\Phi(h[x]))$ 广播到 $D$ 个深度平面上，形成三维特征 $\mathcal{F}_t$；随后利用相对位姿 $g_{\tau t}$ 将其刚体变换到相邻视图 $\tau$，得到 $\mathcal{F}_{\tau t}$。此步骤仅能对齐共视区域的特征，遮挡区域在 $\mathcal{F}_{\tau t}$ 中表现为空体素。

2. **ConteXt 上下文补全**：对 $\mathcal{F}_{\tau t}$ 中的空区域，ConteXt 通过上下文池化 $CP(\cdot)$ 从共视区域聚集信息——以掩膜平均池化聚合非空体素特征，再上采样填充空区域（式(5)），最终通过残差叠加得到补全特征 $\mathcal{F}_{\tau t}' = \mathcal{F}_{\tau t} + \bar{M} \odot CP(\mathcal{F}_{\tau t})$（式(6)）。这一过程本质上是利用可见区域的局部上下文来外推不可见区域的特征。

3. **ORCaS 损失强制学习**：训练时，补全后的相邻视图三维特征 $\hat{\mathcal{F}}_\tau$ 被强制与相邻视图自身编码的真实特征 $\mathcal{F}_\tau$ 一致，损失函数为 $\ell_{\mathrm{ORCaS-p}} = \sum_{x}^{\chi} \|\hat{\mathcal{F}}_{\tau}[x] - \mathrm{sg}(\mathcal{F}_{\tau}[x])\|_{p}$（式(7)）。这里的 stop-gradient 操作 $\mathrm{sg}(\cdot)$ 确保相邻视图编码器不被反向传播更新，形成单向的监督关系。

4. **偏置迁移与深度解码**：推理时，习得的 ConteXt 归纳偏置被用于调制输入视图的三维特征——将补全后的 $\hat{\mathcal{F}}_t$ 经向量化 $r[x] = \mathrm{vec}(\hat{\mathcal{F}}_{\tau}[x]) \in \mathbb{R}^{C \cdot D}$ 和 softmax 加权投影 $\hat{F}_{t}[x] = \sum_{d=1}^{D} \hat{\mathcal{F}}_{t}[x][d] \cdot \sigma(P(r[x]))[d]$ 降维为二维特征，再送入深度解码器预测稠密深度图。

### 与 Baseline 的本质差异

| 维度 | 现有方法（以 AugUndo 为代表） | ORCaS |
|------|-------------------------------|-------|
| 监督信号来源 | 仅共视区域的光度/几何一致性 | 增加遮挡区域的隐特征补全监督 |
| 学习目标 | 在可见像素间插值深度 | 预测不可见三维结构的隐表示 |
| 推理时特征处理 | 解码器直接处理输入视图特征 | ConteXt 偏置调制输入视图特征后再解码 |
| 归纳偏置层次 | 二维图像正则化 | 三维形状抽象 |

消融实验（Table 2）定量证实了这一因果链：在仅保留 2D→3D 广播与刚体变换的基础模型上，MAE 为 35.31；加入 ORCaS 损失后降至 30.90，贡献了 21.6% 的性能增益。此外，隐空间特征监督显著优于直接深度监督（Table 6），说明在特征层面学习遮挡补全比在深度层面更有效——这与“学习三维形状归纳偏置而非简单插值深度值”的核心洞察一致。

### 证据强度与边界

- **强证据**：ORCaS 损失在 VOID1500 上的消融增益（21.6%，置信度 0.95）、对 AugUndo 的全面超越（VOID1500 MAE 降低 7.81%，NYUv2 MAE 降低 10.6%，置信度 0.98）、以及零样本泛化提升 15.7%（置信度 0.95），共同构成有力的因果证据链。
- **需注意的边界**：ConteXt 的上下文池化本质上是局部的（最优池化尺寸为 (4,4,2)，Table 4），对远距离遮挡或大面积缺失的补全能力有限；训练依赖相邻视图与相对位姿，无法直接用于单帧场景；当前框架假设静态场景，运动物体的影响虽经实验验证较小（Table 13，MAE 30.84 vs 30.90），但在高动态场景下仍需谨慎。

## 整体框架

![[assets/figures/papers/iclr26_0012_v2skNLbrfF_ORCaS_Unsupervised_Depth_Completion_via_Occluded/figures/001_Figure_1.jpg]]
*Figure 1: Overview of Occluded Region Completion as Supervision (ORCaS). Inference of ORCaS for the input view only requires a single input view (t), and an identity camera pose matrix. Training ORCaS involves two different views (input view t, and target view τ ) and their relative camera pose $g _ { \tau t }$ . The input view 3D features are warped to align with the adjacent view. Empty regions due to occlusion are predicted by the ConteXt layer, and the inductive bias is learned by minimizing ORCaS loss, which leverages the extracted 3D feature from the adjacent view inputs as supervision*

ORCaS 的整体训练与推理流程围绕一个核心思想展开：**将输入视图中不可见的遮挡区域特征补全作为额外的监督信号**，迫使网络学习对三维场景形状的强归纳偏置。该框架在训练时利用相邻视图的相对位姿，将输入视图的隐空间特征变换至相邻视图，通过 Contextual eXtrapolation（ConteXt）模块填充因遮挡而产生的空区域，并以相邻视图自身的编码特征作为监督目标；在推理时，所学的归纳偏置被迁移用于调制输入视图特征，从而提升深度补全的保真度与泛化能力。

### 输入输出流

**训练阶段**需要两组输入：
- 输入视图 $t$ 的 RGB 图像 $I_t$ 与稀疏深度点 $z_t$
- 相邻视图 $\tau$ 的 RGB 图像 $I_\tau$ 与稀疏深度点 $z_\tau$
- 两视图间的相对位姿 $g_{\tau t}$

训练输出为输入视图 $t$ 的稠密深度预测 $\hat{d}_t$，以及相邻视图 $\tau$ 的预测三维特征 $\hat{\mathcal{F}}_\tau$。

**推理阶段**仅需单帧输入（输入视图 $t$ 的 RGB 与稀疏深度），相机位姿矩阵设为单位阵，直接输出稠密深度图 $\hat{d}_t$。

### 模块关系与数据流

ORCaS 的 pipeline 由以下模块串联构成，数据流方向为从二维输入到三维隐空间，再回归二维深度输出：

1. **RGB 与稀疏深度编码器**：将输入视图的 RGB 图像和稀疏深度图拼接后送入编码器，提取二维特征图 $h[x]$。

2. **2D-to-3D 广播**：通过一个轻量网络 $\Phi$ 从 $h[x]$ 预测深度概率分布 $\tilde{d}[x] = \sigma(\Phi(h[x]))$，该分布在 $D$ 个预定义深度平面上定义了每个像素的离散概率。利用该分布将二维特征沿深度维度广播至三维体素，获得输入视图的三维特征 $\mathcal{F}_t$。

3. **三维特征变形**：利用相对位姿 $g_{t\tau}$，将输入视图的三维特征 $\mathcal{F}_t$ 通过刚体变换变形至相邻视图坐标系，得到 $\mathcal{F}_{\tau t}$。此步骤仅能对齐两视图的共视区域，遮挡区域在变形后表现为空体素。

4. **ConteXt 遮挡补全**：ConteXt 模块通过上下文池化 $CP(\cdot)$ 从 $\mathcal{F}_{\tau t}$ 的非空体素中聚集局部上下文信息，再将其填充至空体素区域，得到补全后的三维特征 $\mathcal{F}_{\tau t}'$。具体地，上下文池化对局部感受野 $R$ 内的非空体素进行掩膜平均池化后上采样，补全操作通过加法注入：$\mathcal{F}_{\tau t}' = \mathcal{F}_{\tau t} + \bar{M} \odot CP(\mathcal{F}_{\tau t})$。

5. **特征投影至二维**：将补全后的三维特征 $\hat{\mathcal{F}}_\tau$ 按深度平面向量化得到 $r[x] = \mathrm{vec}(\hat{\mathcal{F}}_\tau[x]) \in \mathbb{R}^{C \cdot D}$，再通过 softmax 加权求和投影回二维特征 $\hat{F}_t[x] = \sum_{d=1}^{D} \hat{\mathcal{F}}_t[x][d] \cdot \sigma(P(r[x]))[d]$。

6. **深度解码器**：从二维特征 $\hat{F}_t$ 预测稠密深度图 $\hat{d}_t$。解码器输出的深度为原始分辨率的 1/8，通过预测的上采样掩膜经凸组合恢复至全分辨率。

7. **ORCaS 损失模块**（仅训练时）：强制补全后的相邻视图三维特征 $\hat{\mathcal{F}}_\tau$ 与相邻视图自身编码器提取的三维特征 $\mathcal{F}_\tau$（经 stop-gradient 处理）一致：
   $$\ell_{\mathrm{ORCaS-p}} = \sum_{x}^{\chi} \|\hat{\mathcal{F}}_{\tau}[x] - \mathrm{sg}(\mathcal{F}_{\tau}[x])\|_{p}$$
   该损失与标准无监督深度补全损失（光度重建损失、稀疏深度一致性、平滑正则）联合优化，共同驱动网络学习。

### 训练与推理的分离设计

框架的关键设计在于**训练与推理的不对称性**：训练时引入相邻视图与位姿，通过 ORCaS 损失在隐空间学习遮挡补全的归纳偏置；推理时完全丢弃相邻视图分支，仅依赖单帧输入，ConteXt 所学的归纳偏置通过特征调制隐式地提升深度预测质量。这种设计保证了推理效率——在 VOID1500 上单帧推理仅需 17.5 ms（约 57 FPS），参数量 24.9M，GPU 内存占用 2.35 GB，满足实时性要求。

## 核心模块与公式推导

### 2D→3D 特征广播

输入视图 $t$ 的 RGB 图像与稀疏深度图经编码器提取二维特征图 $h[x]$ 后，需将其反投影至三维体素空间。ORCaS 通过建模每个像素点在 $D$ 个深度平面上的离散概率分布来实现这一转换：

$$\tilde{d}[x] = \sigma(\Phi(h[x]))$$

其中 $\Phi$ 为一个小型卷积头，$\sigma$ 为 softmax 函数，$\tilde{d}[x] \in \mathbb{R}^D$ 表示位置 $x$ 在各深度平面上的概率质量。二维特征 $h[x]$ 按此分布加权广播至对应深度的体素，得到输入视图的三维特征 $\mathcal{F}_t$。

### 三维特征刚体变换

训练时，利用已知的相对位姿 $g_{\tau t}$，将输入视图的三维特征刚体变换到相邻视图 $\tau$ 的坐标系下：

$$\mathcal{F}_{\tau t}(x) = \mathcal{F}_t(\pi' g_{t\tau} \bar{X})$$

其中 $\bar{X}$ 为深度平面上的三维点，$\pi'$ 为三维点到体素索引的映射。变换后的特征 $\mathcal{F}_{\tau t}$ 仅在输入视图可见（即与相邻视图共视）的体素处非空，遮挡区域对应体素为空。

### ConteXt 遮挡区域补全

为填充变换后特征中的空体素，ORCaS 提出上下文外推模块 ConteXt。该模块首先通过掩膜平均池化从非空区域聚集局部上下文信息：

$$CP(\mathcal{F}_{\tau t})(u,v,w) = \mathcal{U}\left(\sum_{(u,v,w)\in R} \frac{M \odot \mathcal{F}_{\tau t}(u,v,w)}{M(u,v,w)+\epsilon}\right)$$

其中 $M$ 为非空体素的二值掩膜，$R$ 为池化感受野，$\mathcal{U}$ 为上采样操作。随后，将上下文描述子叠加到原始特征的空区域，完成特征补全：

$$\mathcal{F}_{\tau t}' = \mathcal{F}_{\tau t} + \bar{M} \odot CP(\mathcal{F}_{\tau t})$$

$\bar{M}$ 为空体素掩膜。该机制的核心在于：仅从共视区域聚集信息来推断遮挡区域的特征，从而迫使网络学习对三维场景形状的强归纳偏置。

### ORCaS 损失

训练时，相邻视图 $\tau$ 的图像与稀疏深度同样经编码器和 2D→3D 广播得到其三维特征 $\mathcal{F}_\tau$。ORCaS 损失强制补全后的特征 $\hat{\mathcal{F}}_\tau$（由 $\mathcal{F}_{\tau t}'$ 经 3D 卷积解码器得到）与编码得到的 $\mathcal{F}_\tau$ 一致：

$$\ell_{\mathrm{ORCaS-p}} = \sum_{x}^{\chi} \|\hat{\mathcal{F}}_{\tau}[x] - \mathrm{sg}(\mathcal{F}_{\tau}[x])\|_{p}$$

其中 $\mathrm{sg}(\cdot)$ 为 stop-gradient 操作，$p$ 为范数阶数（文中使用 $p=1$）。该损失仅在训练时计算，其作用是将遮挡区域的特征补全转化为有效的监督信号，使网络学会从输入视图推断不可见区域的三维结构。

### 三维特征到二维的投影

补全后的三维特征需降维回二维空间以供深度解码器使用。首先将 $\hat{\mathcal{F}}_\tau$ 沿深度维度向量化：

$$r[x] = \mathrm{vec}(\hat{\mathcal{F}}_{\tau}[x]) \in \mathbb{R}^{C \cdot D}$$

随后通过学习的投影矩阵 $P$ 和 softmax 权重，将三维特征压缩为二维特征：

$$\hat{F}_{t}[x] = \sum_{d=1}^{D} \hat{\mathcal{F}}_{t}[x][d] \cdot \sigma(P(r[x]))[d]$$

该投影操作可视为一种可微分的深度平面选择机制，使模型自适应地融合不同深度的特征信息。最终 $\hat{F}_t$ 输入深度解码器预测稠密深度图 $\hat{d}_t$。

### 整体训练目标

除 ORCaS 损失外，整体训练目标沿用无监督深度补全的标准范式：

$$\arg \min_{\theta} \sum_{\tau \in T} \sum_{x \in \Omega} \lambda_I \mathcal{P}(\hat{I}_{t\tau}(x), I_t(x)) + \sum_{x \in \Omega_z} \lambda_z \psi(\hat{d}_t(x), z_t(x)) + \lambda_r R(I_t, \hat{d}_t)$$

其中 $\hat{I}_{t\tau}(x) = I_{\tau}(\pi g_{\tau t} K^{-1} \bar{x} \hat{d}_t(x))$ 为利用预测深度将相邻视图重投影至输入视图的重建图像，三项依次为光度重建损失、稀疏深度一致性损失和平滑正则项。ORCaS 损失作为额外项加入，与上述损失联合优化。

## 实验与分析

### 核心发现

ORCaS 在 VOID1500 和 NYUv2 两个标准基准上全面超越现有无监督深度补全方法。与当前最优方法 AugUndo 相比，ORCaS 在所有评估指标上平均提升 8.91%（表 1）。这一增益的因果根源在于 ORCaS 损失迫使网络学习对遮挡区域特征的预测能力，从而获得了超越二维图像正则化的三维形状归纳偏置。


![[assets/figures/papers/iclr26_0012_v2skNLbrfF_ORCaS_Unsupervised_Depth_Completion_via_Occluded/figures/002_Table_1.jpg]]
*Table 1: Quantitative results on VOID1500 and NYUv2 test sets. ORCaS outperforms the baselines across all metrics. Compared to (Wu et al., 2024), we improve by an average of 8.91%*

在 VOID1500 上，ORCaS 的 MAE 降至 30.90 mm，相比 AugUndo 的 33.32 mm 降低了 7.81%。在 NYUv2 上，MAE 从 96.73 mm 降至 86.50 mm，降幅达 10.6%。值得注意的是，ORCaS 仅使用 24.9M 参数，少于 AugUndo×2 的 28.3M，却在该变体上进一步取得 5.16% 的 MAE 优势（30.90 vs 32.58），排除了参数量带来的混淆因素（表 8）。

定性结果（图 2、图 3）揭示了性能提升的两个关键维度：ORCaS 在均匀表面区域（如皮质沙发、厨房台面）上产生了更平滑的深度估计，同时在深度不连续处（如显示器边缘、椅子轮廓、窗户边界）保持了更锐利的边缘。这表明 ConteXt 机制学习到的归纳偏置同时增强了平滑区域的连续性和边缘处的保真度。

### 消融分析：ORCaS 损失的因果作用

表 2 的组件消融实验直接揭示了各模块的因果贡献。基线模型仅使用标准的无监督损失（光度损失+稀疏深度一致性+平滑正则），MAE 为 35.31 mm。逐步添加 2D-3D 广播和三维变形后，性能变化有限。然而，引入 ORCaS 损失后，MAE 从 35.31 降至 30.90，贡献了 21.6% 的性能增益。这一结果明确证实：**遮挡区域的隐空间特征补全监督是性能提升的核心因果杠杆**。


![[assets/figures/papers/iclr26_0012_v2skNLbrfF_ORCaS_Unsupervised_Depth_Completion_via_Occluded/figures/015_Table_2.jpg]]
*Table 2: Ablation study on VOID1500 test set. 2D-3D broadcast denotes 2Dto-3D broadcasting, Warping refers to 2D or 3D warping with relative camera pose, and ℓORCaS refers to ORCaS loss*

进一步地，表 6 比较了深度监督与特征监督两种策略。当 ORCaS 损失的目标从预测相邻视图的深度图改为预测相邻视图的隐空间特征时，性能显著提升。特征监督在所有指标上均优于深度监督。这验证了核心洞察：在隐空间而非输出空间施加一致性约束，能更有效地传递三维形状的归纳偏置。


![[assets/figures/papers/iclr26_0012_v2skNLbrfF_ORCaS_Unsupervised_Depth_Completion_via_Occluded/figures/020_Table_6.jpg]]
*Table 6: Comparison between the depth supervision and feature supervision*

### 关键超参数的影响

深度平面数目 D 对性能有显著且单调的影响（表 3）。从 D=2 到 D=4 再到 D=8，MAE 持续下降，D=8 时达到最优的 30.90 mm。这表明更细粒度的深度离散化有助于 ConteXt 机制更精确地定位和补全遮挡区域的特征。然而，继续增加 D 可能带来计算开销的线性增长，需在精度与效率间权衡。

ConteXt 池化核尺寸的消融（表 4）显示，(4,4,2) 配置在 MAE 和 iMAE 上最优，而 (8,8,2) 在 RMSE 和 iRMSE 上略优。这暗示较大的上下文感受野有助于抑制大误差，但可能牺牲局部精度。最终选择 (4,4,2) 作为默认配置，优先优化平均误差。

### 泛化能力与鲁棒性

ORCaS 展现出显著优于基线的泛化能力。在从 VOID1500 到 NYUv2 和 ScanNet 的零样本迁移中，ORCaS 平均提升 15.7%（表 5）。这一跨数据集的泛化优势源于 ORCaS 学习到的归纳偏置——对三维场景形状的抽象理解——而非对特定数据分布的过拟合。


![[assets/figures/papers/iclr26_0012_v2skNLbrfF_ORCaS_Unsupervised_Depth_Completion_via_Occluded/figures/019_Table_5.jpg]]
*Table 5: Zero-shot transfer from VOID1500 to NYUv2 and ScanNet, and Sensitivity study on Sparsity from VOID1500 to VOID150*

在稀疏度敏感性测试中，ORCaS 同样表现出色。当输入点云从 VOID1500 降至 VOID150 的极低密度时，ORCaS 在所有指标上平均提升 31.2%（表 5）。在 VOID500 的不同稀疏度条件下，ORCaS 相比基线的平均提升达 37.4%（表 11）。这验证了 ConteXt 机制对稀疏输入的强鲁棒性：即使共视区域信息有限，上下文池化仍能有效推断遮挡区域特征。

### 相邻视图预测质量

ORCaS 训练过程中预测的相邻视图特征质量是归纳偏置学习成效的直接体现。表 7 评估了 ORCaS 在 VOID1500 测试集上预测的相邻视图深度质量。虽然这些预测并非最终输出，但其精度与最终深度补全性能呈正相关——更准确的遮挡区域补全意味着更强的三维形状先验。

图 4 的定性结果展示了 ORCaS 预测的相邻视图深度图。可见 ConteXt 机制成功填充了因遮挡产生的空洞区域，预测结果在结构上与真实场景保持一致性。这为 ORCaS 损失的有效性提供了直观证据。

### 室外场景的验证

在 KITTI DC 室外自动驾驶基准上，ORCaS 同样取得最优结果（表 9）。MAE 为 253.17 mm，相比 AugUndo 的 256.37 mm 降低了 1.2%，在所有指标上平均超越先前最优方法 3.44%。虽然相对增益小于室内场景，但考虑到 KITTI 场景中遮挡区域比例较低、深度范围更大，这一结果仍验证了 ORCaS 在室外环境中的有效性。


![[assets/figures/papers/iclr26_0012_v2skNLbrfF_ORCaS_Unsupervised_Depth_Completion_via_Occluded/figures/023_Table_9.jpg]]
*Table 9: Quantitative result on the KITTI DC test set. ORCaS outperforms the previous SOTA unsupervised depth completion method by 3.44% across all metrics*

### 鲁棒性边界与失败模式

对相机标定噪声的敏感性研究（表 12）揭示了 ORCaS 的一个潜在脆弱点。当标定噪声达到 10% 和 30% 时，性能出现退化。这是因为三维特征变形和 ORCaS 损失均依赖准确的相对位姿。标定误差会导致特征对齐偏差，进而削弱遮挡区域补全的精度。实际部署中需确保标定质量，或引入对标定噪声鲁棒的变体。

运动物体掩膜的消融（表 13）显示，训练时掩盖动态目标对性能影响微弱（MAE 30.84 vs 30.90）。这得益于 ConteXt 机制对局部不一致性的容错能力——上下文池化可通过周围静态区域的特征推断被遮挡部分，从而缓解动态物体带来的特征不一致。然而，在高度动态场景中，这一假设可能失效。

### 计算效率

ORCaS 在 VOID1500 上的推理延迟为每帧 17.5 ms（约 57 FPS），满足实时性要求。GPU 显存占用为 2.35 GB。深度预测在 1/8 分辨率下进行，通过预测的凸组合上采样掩膜恢复至原始分辨率，在效率与精度间取得了平衡。

## 方法谱系与知识库定位

### 在无监督深度补全谱系中的位置

ORCaS 建立在无监督深度补全的核心范式之上：利用相邻视图间的光度重投影误差作为主要监督信号，辅以稀疏深度一致性约束和平滑正则项。该范式的标准训练目标为：

$$\arg \min_{\theta} \sum_{\tau \in T} \sum_{x \in \Omega} \lambda_I \mathcal{P}(\hat{I}_{t \tau}(x), I_t(x)) + \sum_{x \in \Omega_z} \lambda_z \psi(\hat{d}_t(x), z_t(x)) + \lambda_r R(I_t, \hat{d}_t)$$

在此框架下，ORCaS 与现有方法的根本分歧在于**监督信号的来源边界**。基线方法（AugUndo、KBNet、DesNet、FusionNet、VOICED）仅利用两视图共视区域的信号进行训练，对遮挡区域的信息完全弃置。ORCaS 则首次将遮挡区域纳入训练监督：通过刚体变换将输入视图的隐空间特征变形到相邻视图，再用 ConteXt 机制补全因遮挡而产生的空体素，最后强制补全特征与相邻视图编码特征一致。这一设计将训练目标从"最小化重投影误差"扩展为"学习预测不可见区域的三维特征"，从而诱导出更强的三维形状归纳偏置。

与 AugUndo（ICLR 2025）的直接对比尤为关键。AugUndo 通过数据增强与逆增强的一致性约束来提升泛化性，但其归纳偏置仍停留在二维图像层面。ORCaS 在参数更少（24.9M vs 28.3M）的情况下，于 VOID1500 上 MAE 降低 7.81%，在 NYUv2 上降低 10.6%，证明三维特征空间的监督比二维增强策略更有效地捕获了几何结构。

### 适用边界

ORCaS 的有效性依赖于以下前提条件，这些条件共同划定了其适用边界：

1. **静态场景假设**：训练依赖相邻视图间的刚体变换，要求场景在帧间保持静态。动态物体会导致变形特征与编码特征不一致。实验表明，训练时掩盖运动目标对性能影响微弱（MAE 30.84 vs 30.90），说明 ConteXt 机制对动态干扰具有一定鲁棒性，但大规模动态场景下的行为未经充分检验。

2. **多视图训练依赖**：ORCaS 损失需要相邻视图及其相对位姿，无法直接应用于单帧或非连续视图的采集场景。推理时仅需单帧输入，但训练阶段的多视图需求限制了数据来源——适用于具有连续帧采集能力的系统（如手持RGB-D相机、车载多相机系统），不适用于孤立图像或非时序数据集。

3. **透视相机模型**：2D-to-3D 广播和 3D 特征变形均基于透视投影假设。对鱼眼相机、全景相机或环绕视图等非标准投影模型的适应性未经检验，直接迁移可能导致深度平面离散化失效或变形误差累积。

4. **稀疏度下限**：在极低稀疏度（如 VOID150）下，尽管 ORCaS 相比基线有 31.2% 的提升，但绝对误差仍然较高。深度概率分布 $\tilde{d}[x] = \sigma(\Phi(h[x]))$ 的估计质量依赖于稀疏深度输入提供的锚点，输入过于稀疏时深度平面的概率分布趋于平坦，导致 2D-to-3D 广播的体素特征信噪比下降。

### 局限性与失效模式

1. **遮挡区域监督的间接性**：ORCaS 损失在隐空间强制执行 $\ell_{\mathrm{ORCaS-p}} = \sum_{x}^{\chi} \|\hat{\mathcal{F}}_{\tau}[x] - \mathrm{sg}(\mathcal{F}_{\tau}[x])\|_{p}$，但特征一致性并不严格等价于几何一致性。补全的遮挡区域特征可能过拟合到训练场景的统计规律，在分布外场景产生伪影。论文未提供补全特征的可解释性分析或几何验证。

2. **标定噪声敏感**：3D 特征变形 $\mathcal{F}_{\tau t}(x) = \mathcal{F}_t(\pi' g_{t\tau} \bar{X})$ 直接依赖相机内参和帧间位姿的精度。实验表明在 10% 和 30% 标定噪声下性能有所下降，实际部署中 SLAM/VIO 系统的累积漂移可能超出此范围。

3. **深度平面离散化限制**：性能随深度平面数 D 增加而提升（D=2→4→8），但 D=8 时 MAE 30.90 已接近当前框架上限。连续深度空间的离散化本质上引入了量化误差，对于需要亚体素精度的精细几何结构（如薄板、线缆）可能失效。

4. **计算-精度权衡**：ORCaS 推理速度为 17.5ms/帧（57 FPS），满足实时性要求，但这是以 1/8 分辨率预测深度并上采样为代价的。上采样过程通过凸组合插值恢复分辨率，在高频深度不连续处（如物体边界）可能产生过度平滑。

### 开放问题

1. **归纳偏置的可迁移性**：ORCaS 学习的遮挡区域补全能力是否可迁移到其他几何任务（光流估计、单目深度估计、多视角立体匹配）？ConteXt 机制能否作为通用的三维表示学习模块嵌入到其他架构中？这需要跨任务的实验验证。

2. **室外大规模场景泛化**：当前实验集中在室内数据集（VOID1500、NYUv2）和小规模室外数据（KITTI DC，MAE 仅提升 1.2%）。对 nuScenes、Waymo 等大规模自动驾驶场景的泛化能力未知，这些场景中深度范围更大、遮挡模式更复杂。

3. **在线学习与 SLAM 集成**：ORCaS 的训练范式天然适配 SLAM/VIO 系统（已有连续帧和位姿估计），但当前为离线训练。能否实现在线持续学习，使 ConteXt 的归纳偏置随场景自适应更新？

4. **ConteXt 机制的架构演进**：当前 ConteXt 使用局部上下文池化 $CP(\mathcal{F}_{\tau t})(u,v,w) = \mathcal{U}\left(\sum_{(u,v,w)\in R} \frac{M \odot \mathcal{F}_{\tau t}(u,v,w)}{M(u,v,w)+\epsilon}\right)$，本质是掩膜平均池化。用注意力机制或轻量 Transformer 替代是否能在不显著增加计算开销的前提下提升补全质量？

5. **特征监督与深度监督的协同**：实验证明隐空间特征监督优于直接深度监督，但两者是否互补？联合训练能否在保持几何一致性的同时进一步提升深度精度？

## 原文 PDF

![[paperPDFs/ICLR_2026/ORCaS_Unsupervised_Depth_Completion_via_Occluded_Region_Completion_as_Supervision.pdf]]
