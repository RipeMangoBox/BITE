---
title: "L3DR: 3D-aware LiDAR Diffusion and Rectification"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/L3DR_3D_aware_LiDAR_Diffusion_and_Rectification.pdf
project_link: null
code_link: "https://github.com/liuQuan98/L3DR"
aliases:
- L3DR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入一个三维残差回归网络（RRN），对扩散生成的点云在三维空间中预测逐点偏移量，并通过径向投影校正局部几何误差。
primary_logic: 3D模型在生成锐利、真实的边界方面天生优于2D模型（理论证明与实验验证），同时采用Welsch损失函数抑制训练数据中的高偏差异常区域，使RRN专注于局部几何伪影的校正。
claims:
- 理论分析（定理1与推论2）证明2D扩散模型输出梯度有界，而3D模型因可在3D空间中操作，能生成任意锐利的边界。
- 经验梯度分布显示，矫正后的RV图像梯度分布更接近真值，JSD从0.222降至0.176。
- 消融实验：将3D RRN替换为2D UNet导致所有指标明显下降，证明3D几何处理的必要性。
- 采用MSE损失比Welsch损失性能严重退化，验证了忽略高偏差区域的重要性。
---

# L3DR: 3D-aware LiDAR Diffusion and Rectification

> [!tip] 核心洞察
> 3D模型在生成锐利、真实的边界方面天生优于2D模型（理论证明与实验验证），同时采用Welsch损失函数抑制训练数据中的高偏差异常区域，使RRN专注于局部几何伪影的校正。

| 字段 | 内容 |
|------|------|
| 中文题名 | L3DR：三维感知的激光雷达扩散与矫正框架 |
| 英文题名 | L3DR: 3D-aware LiDAR Diffusion and Rectification |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.19064) · [Code](https://github.com/liuQuan98/L3DR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | L3DR |
| Dataset | KITTI360, SemanticKITTI, Waymo, nuScenes |

> [!tip] 效果简介
> - KITTI360 (Unconditional) 上，FSVD (↓) 35.8 vs LiDM 38.8 (↓7.7%)；FPVD (↓) 26.1 vs LiDM 29.0 (↓10.0%)。
> - SemanticKITTI (Conditional) 上，FPVD (↓) 15.0 vs LiDM 17.7 (↓15.3%)。
> - Waymo (Conditional) 上，JSD (↓) 0.086 vs LiDM 0.104 (↓17.3%)。

## 概述

**问题瓶颈**：基于距离视图的激光雷达扩散模型将三维点云压缩为二维深度图进行生成，虽然计算高效，却因缺乏三维几何感知而引入系统性伪影——深度溢出使前景物体后方出现虚假点云、波浪形表面破坏平面结构、边缘圆化丧失锐利边界。理论分析（定理1与推论2）揭示，2D扩散模型输出的空间梯度存在严格上界，因而天然无法生成锐利边缘；而3D模型则可在三维空间中产生任意大的梯度，具备生成清晰边界的固有能力。

**核心方案**：L3DR提出一种**扩散无关的三维感知矫正框架**，以极轻量的后处理模块嫁接于任意LiDAR扩散模型之上。其核心是一个三维残差回归网络，在生成点云上预测逐点三维偏移量，并通过径向投影将其对齐至原始点云的射线方向，从而在保持投影结构一致性的前提下修正局部几何误差。训练中引入**Welsch损失函数**，利用其倒钟形特性对大幅度偏差给予饱和惩罚，迫使网络忽略训练数据中的高偏差异常区域（如墙体偏移、叶片随机点），专注于RV伪影的局部矫正。

**方法定位**：L3DR不改变原有扩散模型的架构或超参数，仅作为后处理模块加入。训练数据由语义条件扩散模型自动生成，无需额外人工标注。在现有LiDAR生成范式中，L3DR属于“RV扩散生成 + 3D几何矫正”的两阶段路线，兼顾了2D扩散的布局生成效率与3D网络的几何锐度。

**主要结果**：在KITTI360、SemanticKITTI、nuScenes、Waymo四个数据集上，L3DR一致超越所有基线方法。以KITTI360无条件生成为例，相较于LiDM基线，FSVD下降7.7%（35.8 vs 38.8），FPVD下降10.0%（26.1 vs 29.0），JSD下降13.7%；在SemanticKITTI条件生成上，FPVD从17.7降至15.0（↓15.3%）。消融实验证实：将3D RRN替换为2D UNet导致所有指标显著恶化，MSE损失替代Welsch损失则使FSVD和FPVD近乎翻倍——这两个消融分别验证了3D几何处理的必要性和Welsch损失抑制高偏差区域的关键作用。计算开销方面，RRN仅增加37.9M参数、19.65ms推理延迟，训练耗时仅2小时（单RTX 4090），远低于扩散模型的36小时×4 GPU。

## 背景与动机

### 激光雷达生成的核心瓶颈：从2D到3D的几何鸿沟

激光雷达（LiDAR）点云生成是自动驾驶感知与仿真领域的核心任务之一。近年来，扩散模型（Diffusion Models）在图像生成领域取得了巨大成功，其逐步去噪的生成范式展现了强大的分布拟合能力。这一范式被自然地迁移至LiDAR点云生成中，但面临一个关键的表示选择问题：直接在稀疏、非结构化的3D空间中进行扩散，还是将点云投影到结构化的2D表示上进行生成？

当前主流的LiDAR扩散方法——如 **LiDM**、**R2DM**、**LiDARGen** 等——普遍采用距离视图（Range View, RV）作为生成空间。其基本流程是：通过距离视图投影（RVP）将3D点云压缩为2D深度图，在2D空间完成扩散生成，再通过反投影（RRVP）恢复为3D点云。这一策略的优势在于可以复用成熟的2D扩散架构，计算效率高，且能较好地捕捉场景的整体布局。

然而，**2D RV扩散模型存在一个根本性的几何盲区**：扩散过程仅对深度图像的像素值进行建模，完全缺乏对3D空间几何结构的感知。这导致了三类典型的几何伪影：

- **深度溢出（Depth Bleeding）**：前景物体与背景之间的深度不连续性在RV图中被模糊化，反投影后在3D空间中产生悬浮于物体之间的虚假点云（Figure 1a）。
- **波浪形表面（Wavy Surfaces）**：本应平整的地面或墙面在生成结果中呈现波浪状起伏，这是2D模型在深度维度上缺乏几何约束的直接后果（Figure 1b）。
- **边缘圆钝（Rounded Edges）**：物体的锐利边界被平滑化，丧失了激光雷达点云应有的几何锐度。

这些伪影并非偶然的训练瑕疵，而是2D生成范式内在的局限性。

### 理论洞察：2D模型为何天然无法生成锐利边界

L3DR通过严格的理论分析揭示了这一问题的数学本质。**定理1**（Section 3.2）证明：对于2D扩散模型生成的距离视图图像 $x_0$，其空间梯度的范数存在一个全局上界：

$$\| \nabla x_0 \| \le L$$

这意味着无论扩散模型如何训练，其输出的深度图梯度始终被常数 $L$ 所约束，无法在物体边界处产生任意大的深度跳变。换言之，**2D扩散模型在理论上就无法生成真正锐利的边界**。

相比之下，**推论2**指出：当在3D空间中直接操作点云时，矫正后的RV图像梯度可以随深度差 $\Delta d$ 的增大而任意增大：

$$\| \nabla x_{3d} \| \le L_{3D} \times \Delta d$$

这一理论差异通过实验得到了有力的经验验证（Figure 2）：真实点云（GT）的梯度分布呈现显著的重尾特征，反映其包含大量锐利边缘；而原始RV扩散输出的梯度分布明显向零集中，与真实分布的Jensen-Shannon散度（JSD）高达0.222。这从理论和实证两个层面共同指向了一个核心结论：**3D模型在生成锐利、真实的几何边界方面天生优于2D模型**。

### 3D矫正的挑战：训练数据中的“陷阱”

一个直观的解决方案是训练一个3D网络对扩散生成的点云进行几何矫正。然而，这一思路面临一个隐蔽但致命的训练障碍：**训练数据对中不仅包含需要矫正的RV伪影（高方差误差），还混杂着大量高偏差异常区域**（Figure 4）。

具体而言，扩散模型生成的伪影（如深度溢出、波浪面）表现为围绕真值的随机波动，属于高方差误差，是矫正任务的目标。但在训练数据中，还同时存在三类高偏差异常：
1. **整体偏移的墙面**：生成墙面与真值墙面之间存在系统性的整体位移；
2. **不可预测的植被点**：树叶等区域的激光回波具有高度随机性，生成点与真值点之间无对应关系；
3. **孤立的深度错误块**：局部区域存在一致性的深度偏差。

这些高偏差区域的误差幅度远大于RV伪影，若使用传统的MSE或L1损失函数，训练过程会被这些异常区域“劫持”，导致网络忽略真正的几何伪影矫正任务。这一发现解释了为何简单的3D后处理方案此前未能成功。

### L3DR的动机与定位

基于上述分析，L3DR的动机清晰而聚焦：**在不改变现有RV扩散模型的前提下，通过一个轻量的3D后处理模块，矫正扩散生成点云中的几何伪影，同时通过损失函数设计规避训练数据中的高偏差陷阱**。

该框架的核心洞察可概括为三点：
1. **分工协作**：2D扩散负责场景布局生成（其对噪声的高容忍度使其适合此任务，如Figure 8所示），3D网络负责局部几何矫正（其能生成任意锐利边界的理论优势使其适合此任务）；
2. **损失函数设计**：采用Welsch损失函数（一种倒钟形函数）替代传统的MSE/L1损失，利用其对大幅度误差的饱和特性，自动抑制高偏差训练区域，使网络专注于局部几何伪影的矫正；
3. **扩散无关性**：RRN作为独立的后处理模块，可嫁接至任意LiDAR扩散模型（如LiDM、R2DM），无需修改原有扩散模型的训练或推理流程，具有高度的通用性和即插即用特性。

## 核心创新

L3DR 的核心创新在于揭示并解决了一个被现有 LiDAR 扩散模型普遍忽视的结构性缺陷：**基于距离视图（RV）的二维扩散模型缺乏三维几何感知能力，其输出存在固有的几何伪影**。围绕这一发现，L3DR 构建了一个“二维布局生成 + 三维几何矫正”的双阶段框架，其关键创新点可归纳为以下三个 changed slots。

### 1. 三维残差回归网络（RRN）：从 2D 平滑到 3D 锐利的几何矫正

现有 LiDAR 扩散模型（如 **LiDM**、**R2DM**）均在 RV 深度图上执行扩散过程，输出仅经过简单的反投影（RRVP）即得到最终点云，缺乏任何后处理步骤。L3DR 在此处插入一个全新的后处理模块——**三维残差回归网络（RRN）**。

RRN 的核心作用机制如下：
- **输入**：扩散模型生成的含伪影点云 $P_{gen} \in \mathbb{R}^{N \times 3}$。
- **处理**：通过三维骨干网络 $F: \mathbb{R}^{N \times 3} \to \mathbb{R}^{N \times 3}$（如 SPUNet 或 PTV3）预测每个点的三维偏移量 $O = F(P_{gen})$。
- **径向投影约束**：为保证投影结构一致性，将预测偏移投影至原始点的径向方向，得到最终残差 $\hat{O}$。
- **输出**：矫正后的点云 $P_{rect} = P_{gen} + \hat{O}$。

这一设计的理论依据来自论文的定理 1 与推论 2：**二维扩散模型输出的 RV 图像空间梯度存在上界** $\|\nabla x_0\| \le L$，无法生成锐利的物体边界；而**三维模型可在三维空间中操作，其矫正后的图像梯度可随深度差 $\Delta d$ 增大而任意增大**，因此能天然地恢复锐利边缘。经验验证（Figure 2）表明，矫正后的 RV 图像梯度分布更接近真值，Jensen-Shannon 散度（JSD）从 0.222 降至 0.176。

消融实验（Table 3）提供了决定性证据：将 3D RRN 替换为 2D UNet 后，所有评估指标均明显恶化，证实了三维几何处理相对于二维处理的不可替代性。

### 2. Welsch 损失函数：抑制高偏差异常区域，聚焦局部伪影

传统回归任务通常采用 L1 或 L2 损失，但 RRN 的训练数据对（由扩散模型生成的 $P_{gen}$ 与真值 $x_{gt}$ 配对）中存在两类误差（Figure 4）：
- **高方差误差**：即 RV 伪影，如深度溢出、波浪形表面，是 RRN 需要矫正的目标。
- **高偏差误差**：如墙体整体偏移、树叶上的随机点、孤立深度块，这些区域与真值的偏差远大于 RV 伪影，若用 MSE 等无差别惩罚所有误差的损失函数，会“劫持”训练过程，使 RRN 忽略真正的局部几何伪影。

L3DR 引入 **Welsch 损失函数**来解决这一问题：

$$\psi_{\nu}(x) = 1 - \exp\left(-\frac{x^2}{2\nu^2}\right)$$

该函数呈倒钟形，对大幅度误差给予饱和惩罚，从而自动抑制高偏差异常区域的梯度贡献，使训练聚焦于局部几何伪影的矫正。RRN 的最终训练损失为：

$$L_{RRN} = \operatorname{mean}\left(\psi_{\nu}\left(\operatorname{RVP}(P_{gen} + \hat{O}) - x_{gt}\right)\right)$$

消融实验（Table 3/5/6）一致表明：将 Welsch 损失替换为 MSE 损失会导致 FSVD 和 FPVD 几乎翻倍，性能严重退化，验证了忽略高偏差区域对于 RRN 有效训练的关键性。宽度参数 $\nu = 0.5$ 可在全局感知指标与局部匹配指标之间取得最佳平衡（Table 7）。

### 3. 扩散无关的嫁接式架构与高效训练范式

L3DR 的第三个关键创新在于其**架构设计上的解耦性**：
- **第一阶段**：利用语义条件 LiDAR 扩散模型（LiDM）自动生成含 RV 伪影的点云-真值数据对，无需额外人工标注。
- **第二阶段**：RRN 作为独立的后处理模块进行监督式回归训练。

在推理时（Figure 5），RRN 可**嫁接至任意 LiDAR 扩散模型的输出端**，实现扩散无关的几何矫正。实验证明，RRN 不仅可提升 LiDM 的生成质量，同样可有效矫正 R2DM 的输出（Table 1，Ours-R2DM）。

此外，该两阶段训练范式具有显著的计算效率优势：RRN 训练仅需约 2 小时（单张 RTX 4090），而 LiDM 训练需 36 小时 × 4 GPU；推理时 RRN 仅引入 19.65 ms 的额外延迟和 37.9 M 的额外参数量（Table 4），以极小的计算代价换取了显著的生成质量提升。

## 整体框架

L3DR 采用**两阶段训练—单阶段推理**的流水线架构，其核心思想是将激光雷达点云的全局布局生成与局部几何矫正解耦：第一阶段由语义条件扩散模型负责生成合理的场景布局（但不可避免地引入距离视图伪影），第二阶段由三维残差回归网络在点云空间中对这些伪影进行针对性修复。推理时，残差回归网络作为扩散无关的后处理模块，可嫁接至任意基于距离视图的激光雷达扩散模型之上。

### 训练流水线

如图 Figure 3 所示，训练过程分为两个独立阶段：

![[assets/figures/papers/paper_list_l2528_https_arxiv_org_abs_2602_19064/figures/003_Figure_3.jpg]]
*Figure 3: The training pipeline of the proposed L3DR framework. In the LiDAR diffusion training stage, generated and ground-truth point cloud pairs are collected using semantic-conditioned LiDAR diffusion. In the residual regression training stage, such data pairs are employed to train a 3D network to remove RV artifacts present in the residuals to improve generation quality*

**第一阶段：语义条件激光雷达扩散训练（LiDAR Diffusion Training）**
- 输入：语义分割图作为条件信号。
- 过程：基于距离视图（Range View, RV）的扩散模型（默认采用 **LiDM**）在 RV 深度图上执行加噪—去噪过程，学习从高斯噪声中重建合理的深度分布。
- 输出：成对的“生成点云 $P_{gen}$ — 真值点云 $P_{gt}$”。这些数据对中，$P_{gen}$ 包含扩散模型固有的 RV 伪影（深度溢出、波浪形表面、圆角边缘等），而 $P_{gt}$ 提供无伪影的几何真值。
- 关键操作：通过距离视图投影（RVP, Eq. 3）将 3D 点云映射为 2D 深度图供扩散模型处理，再通过反投影（RRVP, Eq. 4）将生成深度图恢复为 3D 点云。

**第二阶段：残差回归训练（Residual Regression Training）**
- 输入：第一阶段收集的 $(P_{gen}, P_{gt})$ 数据对，可选地附加语义分割图作为辅助输入。
- 核心模块：**残差回归网络（Residual Regression Network, RRN）**，采用三维骨干网络（SPUNet 或 PTV3），接收 $P_{gen} \in \mathbb{R}^{N \times k}$（$k$ 为点特征维度），输出逐点三维偏移量 $O = F(P_{gen}) \in \mathbb{R}^{N \times 3}$。
- 径向投影约束：为保证矫正后的点云保持与原始投影结构的一致性，预测偏移量被投影到原始点的径向方向上：
  $$\hat{O} = P_{gen} \cdot \text{diag}(P_{gen} O^\top) / \sqrt{\text{diag}(P_{gen} P_{gen}^\top)}$$
  最终矫正点云为 $P_{rect} = P_{gen} + \hat{O}$。
- 损失函数：采用 **Welsch 损失**（Eq. 5-6），将矫正点云重新投影到 RV 图像后与真值深度图计算误差：
  $$L_{RRN} = \text{mean}\left( \psi_\nu\left( \text{RVP}(P_{gen} + \hat{O}) - x_{gt} \right) \right)$$
  其中 $\psi_\nu(x) = 1 - \exp(-x^2 / 2\nu^2)$ 为倒钟形函数，对大幅度误差给予饱和惩罚，从而抑制训练数据中的高偏差异常区域（如位移墙体、不可预测的树叶散点、孤立深度块），使 RRN 专注于局部 RV 伪影的矫正。

### 推理流水线

如图 Figure 5 所示，推理阶段 RRN 以**扩散无关**的方式运行：
1. 任意基于 RV 的激光雷达扩散模型（LiDM、R2DM 等）从噪声/条件生成 RV 深度图。
2. 通过 RRVP 将深度图反投影为 3D 点云。
3. 预训练的 RRN 接收该点云（及可选的语义图），预测径向矫正偏移量。
4. 输出几何增强后的最终点云。

![[assets/figures/papers/paper_list_l2528_https_arxiv_org_abs_2602_19064/figures/005_Figure_5.jpg]]
*Figure 5: The inference pipeline of the proposed L3DR*

### 模块关系与数据流

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| RVP | 3D→2D 投影 | 点云 $(p_x, p_y, p_z)$ | RV 像素 $(u, v)$ 及深度 $d_i$ |
| RRVP | 2D→3D 反投影 | RV 像素 $(u, v)$ 及深度 $d_i$ | 点云 $(p_x, p_y, p_z)$ |
| LiDM（第一阶段） | 语义条件扩散生成 | 语义图 + 噪声 | 含 RV 伪影的生成点云 $P_{gen}$ |
| RRN（第二阶段） | 3D 几何伪影矫正 | $P_{gen}$（+ 语义图） | 逐点径向偏移 $\hat{O}$ |
| Welsch Loss | 抑制高偏差区域 | 矫正后 RV 图与真值 | 标量损失值 |

### 设计逻辑

该两阶段解耦设计源于一个关键理论洞察（定理 1 与推论 2）：2D 扩散模型输出的空间梯度存在理论上界，无法生成任意锐利的边界；而 3D 模型可直接在三维空间中操作，其矫正后的 RV 图像梯度可随深度差增大而任意增大，天然具备生成锐利边缘的能力。因此，将“全局布局生成”委托给成熟的 2D RV 扩散模型，将“局部几何锐化”委托给 3D RRN，实现了二者的优势互补。Welsch 损失的引入进一步解决了训练数据中高偏差区域（而非高方差 RV 伪影）劫持优化方向的问题，确保 RRN 的学习目标聚焦于真正的几何伪影矫正。

## 核心模块与公式推导

### 3.1 问题建模：2D扩散模型的边界锐度瓶颈

L3DR的理论出发点在于揭示基于距离视图（RV）的2D扩散模型在几何生成上的本质局限。给定一个由2D扩散模型生成的RV深度图 $x_0 \in \mathbb{R}^{H \times W}$，其生成过程可形式化为从高斯噪声出发的迭代去噪：

$$q ( x _ { t } \mid x _ { 0 } ) = \mathcal { N } ( x _ { t } ; \sqrt { \bar { \alpha } _ { t } } x _ { 0 } , ( 1 - \bar { \alpha } _ { t } ) \mathbf { I } )$$

$$p _ { \theta } ( x _ { t - 1 } \mid x _ { t } ) = \mathcal { N } ( x _ { t - 1 } ; \mu _ { \theta } ( x _ { t } , t ) , \Sigma _ { \theta } ( x _ { t } , t ) )$$

**定理1（2D扩散梯度有界）** 指出：2D扩散模型输出的RV图像空间梯度被常数 $L$ 所限，即 $\| \nabla x _ { 0 } \| \le L$。这意味着模型在物体边界处无法产生任意大的深度跳变，导致生成的边缘呈现平滑过渡——这正是深度溢出（depth bleeding）和波浪形表面（wavy surfaces）等几何伪影的数学根源。

**推论2（3D矫正梯度无界）** 进一步证明：若在3D空间中引入逐点偏移矫正，则矫正后重投影回RV图像的梯度满足 $\| \nabla x _ { 3 d } \| \le L _ { 3 D } \times \Delta d$，其中 $\Delta d$ 为相邻像素的真实深度差。由于 $\Delta d$ 在物体边界处可以任意大，3D矫正能够恢复锐利边缘。Figure 8给出了直观验证：在RV图像上施加 $\sigma = 5\text{m}$ 的大噪声几乎不影响人类对图像内容的理解，但同样的噪声在3D点云中完全破坏了空间结构；反之，$\sigma = 0.2\text{m}$ 的小噪声在RV上几乎不可察觉，却能在点云中产生可见扰动。这一非对称敏感性表明，2D RV适合布局生成，3D空间适合几何精修。

经验验证（Figure 2）显示，矫正后的RV图像梯度分布显著向真值靠拢，Jensen-Shannon散度（JSD）从原始扩散输出的0.222降至0.176，定量证实了3D矫正对边缘锐度的恢复能力。

![[assets/figures/papers/paper_list_l2528_https_arxiv_org_abs_2602_19064/figures/002_Figure_2.jpg]]
*Figure 2: Empirical validation of Theorem 1. The graph shows the distribution of ∥∇x∥ for GT, vanilla RV diffusion, and our rectified RV, including the corresponding Jensen-Shannon Divergence (JSD) w.r.t. the GT*

### 3.2 距离视图投影与反投影

L3DR在2D RV空间与3D点云之间建立可逆映射，这是整个框架的几何桥梁。

**距离视图投影（RVP）** 将3D点 $(p_x, p_y, p_z)$ 映射到RV像素坐标 $(u_i, v_i)$ 并记录深度 $d_i$：

$$\left( \begin{array} { c } u _ { i } \\ v _ { i } \end{array} \right) = \left( \begin{array} { c } \sigma _ { u } \arctan \left( p _ { z } / \sqrt { p _ { x } ^ { 2 } + p _ { y } ^ { 2 } } \right) \\ - \sigma _ { v } \arctan ( p _ { x } / p _ { y } ) \end{array} \right)$$

其中 $\sigma_u, \sigma_v$ 为角度分辨率参数，控制RV图像的尺寸。

**反距离视图投影（RRVP）** 从RV像素 $(u_i, v_i)$ 和深度 $d_i$ 恢复3D坐标：

$$\binom { p _ { x } } { p _ { y } } = \binom { d _ { i } \cos ( u _ { i } / \sigma _ { u } ) \cos ( v _ { i } / \sigma _ { v } ) } { d _ { i } \cos ( u _ { i } / \sigma _ { u } ) \sin ( v _ { i } / \sigma _ { v } ) }$$

这一对映射构成了L3DR两阶段流水线的核心操作：第一阶段在RV空间完成扩散生成，第二阶段通过RRVP将生成结果提升至3D空间进行几何矫正，再经RVP投影回RV空间与真值比对。

### 3.3 残差回归网络与径向投影矫正

残差回归网络（RRN）是L3DR的核心矫正模块。给定扩散生成的含伪影点云 $P_{gen} \in \mathbb{R}^{N \times 3}$，RRN采用3D骨干网络 $F: \mathbb{R}^{N \times k} \to \mathbb{R}^{N \times 3}$ 预测逐点3D偏移量 $O = F(P_{gen})$。骨干网络可选SPUNet或PTV3，两者均为稀疏3D卷积架构，能够高效处理非结构化点云。

为保持投影结构一致性，预测的偏移量被投影至原始点云的径向方向：

$$\hat{O} = P_{gen} \cdot \frac{\text{diag}(P_{gen} O^\top)}{\sqrt{\text{diag}(P_{gen} P_{gen}^\top)}}$$

这一径向投影约束确保矫正后的点 $P_{gen} + \hat{O}$ 不会偏离原始扫描射线的几何结构，从而避免引入新的投影伪影。

### 3.4 Welsch损失函数：抑制高偏差异常区域

RRN的训练数据由语义条件扩散模型自动生成（见Figure 3训练流水线），但生成数据中不仅包含需要矫正的RV伪影（高方差误差），还存在与真值系统性偏离的高偏差区域（Figure 4）：偏移的墙壁、树叶上的随机点、孤立深度块等。若使用标准的MSE损失，这些高偏差区域会主导梯度更新，使网络偏离局部几何矫正的核心任务。

![[assets/figures/papers/paper_list_l2528_https_arxiv_org_abs_2602_19064/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of two types of errors in RRN training data. While the generated point clouds (colored) approximate the GT (gray) in most of the regions with high-variance errors, i.e., RV artifacts as highlighted with green dotted lines, there are also regions with high-bias errors which impede training, including (1) shifted walls, (2) random points on the leaves where laser hits are hard to predict, and (3) isolated chunks with consistent depth error. These bias-dominated regions are harmful for RRN training*

为此，L3DR引入Welsch损失函数：

$$\psi _ { \nu } ( x ) = 1 - \exp \left( - \frac { x ^ { 2 } } { 2 \nu ^ { 2 } } \right)$$

该函数呈倒钟形：对小误差给予近似二次惩罚（保留对局部伪影的敏感性），对大误差给予饱和惩罚（自动忽略高偏差区域）。宽度参数 $\nu$ 控制饱和阈值：$\nu$ 越小，越早进入饱和区，对异常值越鲁棒。调优实验（Table 7）表明 $\nu=0.5$ 在全局感知指标（FSVD、FPVD、JSD）和局部匹配指标（MMD）之间取得最佳平衡。

完整的RRN训练损失为矫正后点云重投影与真值RV图之间的Welsch损失均值：

$$L _ { R R N } = \operatorname { mean } \left( \psi _ { \nu } \left( \operatorname { RVP } \left( P _ { g e n } + \hat { O } \right) - x _ { g t } \right) \right)$$

消融实验（Table 3/Table 5/Table 6）一致表明：将Welsch损失替换为MSE损失会导致FSVD和FPVD几乎翻倍，性能严重退化，验证了抑制高偏差区域对RRN训练的关键作用。

![[assets/figures/papers/paper_list_l2528_https_arxiv_org_abs_2602_19064/figures/013_Table_5.jpg]]
*Table 5: Ablation experiment on nuScenes, including RRN backbone structure, loss function and semantic-map input to RRN*

![[assets/figures/papers/paper_list_l2528_https_arxiv_org_abs_2602_19064/figures/014_Table_6.jpg]]
*Table 6: Ablation experiment on Waymo, including RRN backbone structure, loss function, and semantic-map input to RRN*

### 3.5 扩散无关的推理流水线

L3DR的推理流程（Figure 5）体现了其作为后处理模块的即插即用特性：任意LiDAR扩散模型（如LiDM、R2DM）生成的RV深度图经RRVP转换为点云后，送入预训练的RRN预测径向偏移量，最终输出几何矫正后的高质量点云。RRN不依赖特定扩散模型的内部结构或超参数，仅需一次前向传播（额外耗时19.65ms，参数量+37.9M），即可显著提升生成质量。

## 实验与分析

### 核心实验结果

L3DR 在多个主流自动驾驶激光雷达数据集上进行了全面评测，涵盖无条件生成和语义条件生成两种设定。所有实验均以 LiDM 作为第一阶段扩散模型，L3DR 作为后处理模块嫁接其上，指标与基线完全一致，比较公平。

**无条件生成（KITTI360）**：如表 1 所示，L3DR 在所有指标上显著超越基线 LiDM：FSVD 从 38.8 降至 35.8（↓7.7%），FPVD 从 29.0 降至 26.1（↓10.0%），JSD 从 0.211 降至 0.182（↓13.7%），MMD 从 3.24×10⁻⁴ 降至 2.76×10⁻⁴（↓14.8%）。当将 RRN 嫁接至 R2DM 时，同样取得一致提升（FSVD 35.9，FPVD 28.2），验证了 L3DR 的扩散模型无关性。

**语义条件生成**：在 SemanticKITTI 上（表 2），L3DR 将 FPVD 从 17.7 降至 15.0（↓15.3%），引入语义图输入后（Ours-Sem）进一步降至 14.1。在 nuScenes 和 Waymo 上（表 1），L3DR 分别取得平均 11.6% 和 7.0% 的相对提升。JSD 在 Waymo 上从 0.104 降至 0.086（↓17.3%），表明生成分布与真实分布的对齐程度大幅改善。

**视觉质量**：图 6、7、9、10 的可视化结果表明，矫正后的点云在深度溢出抑制、波浪面平整化、边缘锐化等方面均有明显改善，青色/红色高亮区域直观展示了 RV 伪影的消除效果。

### 消融实验

表 3、5、6 分别在 SemanticKITTI、nuScenes、Waymo 上进行了系统消融，核心结论如下：

| 消融维度 | 关键发现 | 证据锚点 |
|---------|---------|---------|
| **3D vs 2D 骨干** | 将 3D RRN（SPUNet/PTV3）替换为 2D UNet 导致所有指标明显恶化，证实 3D 几何处理是矫正 RV 伪影的必要条件 | Table 3 |
| **损失函数** | 使用 MSE 损失代替 Welsch 损失使 FSVD 和 FPVD 几乎翻倍（SPUNet: FSVD 26.3→42.4），性能严重退化，验证了 Welsch 损失抑制高偏差异常区域的关键作用 | Table 3/5/6 |
| **语义输入** | 向 RRN 输入语义分割图可进一步提升性能，在 KITTI360 条件生成中提供约 10.2% 的平均指标增益 | Table 2, Sec 5.2 |
| **骨干选择** | SPUNet 配合 Welsch 损失和语义输入在所有数据集上取得最佳综合性能，为默认配置 | Table 3/5/6 |
| **宽度参数 ν** | Welsch 损失中 ν=0.5 能在全局感知指标（FSVD、FPVD、JSD）和局部匹配指标（MMD）之间取得最佳平衡 | Table 7 |

![[assets/figures/papers/paper_list_l2528_https_arxiv_org_abs_2602_19064/figures/007_Table_2.jpg]]
*Table 2: Comparison of conditional LiDAR point cloud generation on SemanticKITTI and KITTI360. Gray areas highlight direct comparisons with the baseline, LiDM. ‘Ours-Sem’ denotes our method with segmentation input to the RRN*

![[assets/figures/papers/paper_list_l2528_https_arxiv_org_abs_2602_19064/figures/009_Table_3.jpg]]
*Table 3: Ablation experiment on SemanticKITTI, including RRN backbone structure, loss function, semantic-map input to RRN, and a fair baseline using a 2D image Unet instead of a 3D UNet*

![[assets/figures/papers/paper_list_l2528_https_arxiv_org_abs_2602_19064/figures/015_Table_7.jpg]]
*Table 7: Parameter tuning experiment of ν with PTV3 on SemanticKITTI*

**Welsch 损失的必要性机制**：图 4 揭示了 RRN 训练数据中的两类误差——高方差 RV 伪影（需矫正的目标）和高偏差异常区域（如偏移墙体、树叶随机点、孤立深度块）。MSE 损失对所有误差等权惩罚，导致模型被高偏差区域劫持，无法专注于局部几何伪影矫正；Welsch 函数 $\psi_{\nu}(x)=1-\exp(-x^2/(2\nu^2))$ 对大幅度误差给予饱和惩罚，天然忽略这些异常区域。

### 理论验证

定理 1 和推论 2 从理论上证明了 2D 扩散模型输出梯度有界（$\|\nabla x_0\|\le L$），无法生成锐利边界；而 3D 矫正后梯度可随深度差 $\Delta d$ 任意增大，能恢复锐利边缘。图 2 的经验梯度分布验证了这一理论：矫正后 RV 图像的梯度分布更接近真值，JSD 从 0.222 降至 0.176。图 8 进一步直观展示了 2D RV 和 3D 点云对噪声的敏感度差异——大噪声（σ=5m）彻底破坏点云结构但不妨碍 RV 图像理解，小噪声（σ=0.2m）在点云中可见但在 RV 中几乎不可感知，支持了“2D 布局生成 + 3D 几何矫正”的分工合理性。

### 计算开销

表 4 显示 L3DR 仅引入极小额外开销：RRN 增加约 37.9M 参数，推理额外耗时仅 19.65ms（单 RTX 4090）。相比之下，RRN 训练仅需 2 小时（单 GPU），远低于 LiDM 的 36 小时×4 GPU，具备极高的实用价值。

### 失败模式与局限

尽管 L3DR 在多数场景下表现优异，仍存在以下局限：

1. **初始质量依赖**：矫正效果依赖 RV 深度图的初始质量，严重伪影可能超出 RRN 的恢复能力，导致矫正不完全。
2. **单步矫正限制**：多步矫正 RRN 出现性能退化，目前仅支持单步矫正，可能限制了极端伪影的迭代修复。
3. **场景泛化**：训练数据生成依赖高质量的语义条件 LiDAR 扩散模型，目前仅针对室外自动驾驶场景验证，在室内或物体级 LiDAR 生成中的通用性尚待评估。
4. **异常区域处理**：虽然 Welsch 损失有效抑制了高偏差区域，但流水线未显式建模 RV 伪影的形成机制，在复杂场景中仍有提升空间。

### 重建数据上的扩展验证

表 8 展示了 RRN 在 GS-LiDAR 重建数据上的性能，表明 L3DR 不仅适用于生成模型，还可作为重建方法的后处理模块，进一步扩展了其应用边界。

### 补充图表

![[assets/figures/papers/paper_list_l2528_https_arxiv_org_abs_2602_19064/figures/006_Table_1.jpg]]
*Table 1: Benchmarking of unconditional generation on KITTI360 and semantic-conditioned generation on nuScenes and Waymo. For the semantic-conditioned experiments, RRN takes segmentation map as additional input for optimal performance. Gray areas highlight direct comparisons with the baselines*

![[assets/figures/papers/paper_list_l2528_https_arxiv_org_abs_2602_19064/figures/011_Table_4.jpg]]
*Table 4: Computational overhead on KITTI360. our method introduce very slight computational overhead over the baselines*

![[assets/figures/papers/paper_list_l2528_https_arxiv_org_abs_2602_19064/figures/016_Table_8.jpg]]
*Table 8: RRN performance on GS-LiDAR reconstructed LiDAR data under different training and test data configurations*

## 方法谱系与知识库定位

### 1. 在LiDAR生成范式中的位置

L3DR 的定位需要放在现有激光雷达点云生成的四大范式下来理解（参见原文 Table 9 的范式对比）：

- **原始点云生成**：直接在无序三维点上操作，代表方法包括 **LiDARGAN** 和 **LiDARVAE**。这类方法因点云的非结构化特性，难以保证生成质量，已逐渐被结构化表示方法超越。
- **距离视图（Range View, RV）生成**：将点云投影为二维深度图后生成，是目前的主流范式。代表方法包括基于GAN的 **ProjectedGAN**、基于扩散的 **LiDARGen**、**LDM**、**R2DM** 和 **LiDM**。L3DR 正是嫁接在这一范式之上——它不改变扩散模型本身，而是作为后处理模块矫正RV生成固有的几何伪影。
- **鸟瞰视图（BEV）生成**：将点云投影到俯视平面，代表方法为 **UltraLiDAR**。该方法结构规整但信息压缩严重，生成细节不足。
- **混合/多视图生成**：结合多种投影方式，目前尚处于早期探索阶段。

L3DR 的核心贡献在于**首次系统性地揭示了RV扩散模型的2D-3D鸿沟**：2D扩散模型输出的梯度有界（Theorem 1），无法生成锐利的物体边界；而3D模型天然具备生成任意锐利边界的能力（Corollary 2）。这一理论洞察直接催生了“2D布局生成 + 3D几何矫正”的分工设计。

### 2. 与基线方法的关系

L3DR 的直接基线是 **LiDM**（语义条件LiDAR扩散模型），其关系可概括为“继承—超越—可嫁接”：

- **继承**：L3DR 的第一阶段训练完全依赖 LiDM 生成“含RV伪影的点云—真值点云”数据对。这意味着 L3DR 的性能上限受限于基座扩散模型的质量。
- **超越**：在完全相同的扩散模型和评估协议下，L3DR 在 KITTI360 无条件生成上将 FSVD 从 38.8 降至 35.8（↓7.7%），FPVD 从 29.0 降至 26.1（↓10.0%）；在 SemanticKITTI 条件生成上 FPVD 从 17.7 降至 15.0（↓15.3%），提升幅度显著且一致。
- **可嫁接**：L3DR 的残差回归网络（RRN）是扩散无关的。论文验证了将其嫁接至 **R2DM**（另一种RV扩散模型）后，同样取得稳定的性能增益（KITTI360 上 FSVD 35.9，FPVD 28.2），证明该框架具有跨扩散模型的泛化能力。

与其他非扩散基线的对比（Table 1）进一步确认了 L3DR 的领先地位：在 KITTI360 无条件生成上，L3DR 的 FSVD（35.8）显著优于 LiDARGAN（73.8）、LiDARVAE（55.6）和 UltraLiDAR（56.0），差距超过一倍以上，说明“扩散生成 + 3D矫正”的组合范式在生成质量上具有结构性优势。

### 3. 适用边界与局限

尽管 L3DR 在多个自动驾驶数据集上取得了最先进结果，其适用边界和局限同样明确：

**适用边界**：
- **场景域**：目前仅验证于室外自动驾驶场景（KITTI360、SemanticKITTI、nuScenes、Waymo），依赖语义条件扩散模型生成训练数据。论文明确指出，室内或物体级LiDAR生成的扩展需要相应的条件扩散模型支持，目前尚未验证。
- **伪影类型**：RRN 主要针对RV扩散模型的典型伪影——深度溢出（depth bleeding）、波浪形表面（wavy surfaces）和圆角边缘（rounded edges）。对于扩散模型完全失效的极端区域，RRN 的矫正能力有限。
- **矫正步数**：实验发现多步矫正RRN会导致性能退化，目前仅能进行单步矫正。这意味着对于严重伪影，无法通过迭代修复逐步改善。

**关键局限**：
1. **对基座模型质量的依赖**：训练数据对由语义条件扩散模型自动生成，若基座模型在某些语义类别或几何结构上生成质量差，RRN 的训练数据将包含系统性偏差，矫正效果受限。
2. **未显式建模伪影机制**：RRN 采用数据驱动的回归方式学习矫正，未对RV伪影的形成机制（如投影离散化、遮挡边界处的深度不连续）进行显式建模。在复杂场景中，这种隐式学习可能无法覆盖所有伪影模式。
3. **Welsch损失的副作用**：虽然Welsch损失通过抑制高偏差训练区域（如墙体偏移、树叶随机点、孤立深度块）提升了整体性能，但这也意味着RRN在这些区域“放弃”了矫正，可能导致局部几何仍然不准确。
4. **额外计算开销**：尽管RRN仅引入37.9M参数和19.65ms推理延迟（Table 4），对于实时性要求极高的应用（如在线感知仿真），这一开销仍需纳入系统设计考量。

### 4. 开放问题与后续方向

基于论文的分析与讨论，以下开放问题值得关注：

**泛化能力验证**：
- 论文在 Table 8 中初步探索了RRN在GS-LiDAR重建数据上的后处理能力，但实验规模有限。在更大规模、更多样化的重建数据上系统验证RRN的泛化性能，是方法走向实用的关键一步。
- 室内场景和物体级LiDAR生成是否可以直接复用该框架，只需替换条件扩散模型？这需要实验验证。

**训练策略改进**：
- 多步矫正RRN的性能退化问题尚未解决。是否可以通过误差解耦训练（如逐步聚焦不同尺度的伪影）或引入矫正质量反馈机制来避免衰减？
- 当前两阶段训练过程（先训练扩散模型、再训练RRN）是解耦的。单阶段联合训练是否可行，能否让扩散模型和矫正网络相互促进？

**条件扩展**：
- RRN 目前支持语义图作为额外条件输入（Ours-Sem），在条件生成任务上取得平均10.2%的额外提升。是否可以利用其他模态——如相机图像、文本描述、HD地图——生成训练数据对，将L3DR扩展至更丰富的条件生成场景？

**理论深化**：
- Theorem 1 和 Corollary 2 建立了2D/3D模型在边界锐度上的理论差异，但该分析基于梯度范数的上界。是否存在更精细的理论框架（如基于Lipschitz常数的生成质量界），能够指导矫正网络的设计和训练？

## 原文 PDF

![[paperPDFs/CVPR_2026/L3DR_3D_aware_LiDAR_Diffusion_and_Rectification.pdf]]