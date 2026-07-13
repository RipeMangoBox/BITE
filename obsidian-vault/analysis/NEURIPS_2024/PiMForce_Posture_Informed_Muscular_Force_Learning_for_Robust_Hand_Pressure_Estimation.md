---
title: PiMForce Posture Informed Muscular Force Learning for Robust Hand Pressure Estimation
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/PiMForce_Posture_Informed_Muscular_Force_Learning_for_Robust_Hand_Pressure_Estimation.pdf
project_link: null
code_link: null
aliases:
- PPIMFLRHPE
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过将3D手部姿势信息作为额外的空间先验引入sEMG特征，模型能够分辨相似肌肉活动对应的不同压力模式。
primary_logic: 多模态融合（sEMG + 3D手部姿势）提供了互补的生理和空间信息，使全手压力估计在多样抓取和交互下更为精确和鲁棒，显著优于单一模态和视觉方法。
claims:
- PiMForce在 R² (88.86%), NRMSE (6.65%), 分类准确率 (83.17%) 上均显著优于 sEMG Only、3D Hand Posture Only 等基线。
- 融合3D手部姿势和sEMG相比单一模态在所有指标上均有显著提升。
- 跨用户测试中PiMForce R²达到70.06%，远超sEMG Only的47.90%。
- 自定义多模态数据集（22种交互） 上 R² = 88.86 ± 11.92%
---

# PiMForce Posture Informed Muscular Force Learning for Robust Hand Pressure Estimation

> [!tip] 核心洞察
> 多模态融合（sEMG + 3D手部姿势）提供了互补的生理和空间信息，使全手压力估计在多样抓取和交互下更为精确和鲁棒，显著优于单一模态和视觉方法。

| 字段 | 内容 |
|------|------|
| 中文题名 | 姿态引导的肌肉力学习用于鲁棒手部压力估计 |
| 英文题名 | PiMForce Posture Informed Muscular Force Learning for Robust Hand Pressure Estimation |
| 会议/期刊 | NEURIPS 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PiMForce |
| Dataset | 自定义多模态数据集（22种交互） |

> [!tip] 效果简介
> - 自定义多模态数据集（22种交互） 上，R² 88.86 ± 11.92% vs 83.49 ± 16.40% (sEMG Only) (+5.37%p)。
> - 同上 上，NRMSE 6.65 ± 2.11% vs 8.07 ± 2.62% (sEMG Only) (-1.42%p)；分类准确率 83.17 ± 9.38% vs 77.83 ± 11.56% (sEMG Only) (+5.34%p)。
> - 跨用户（平面交互+捏取） 上，R² 66.71 ± 4.68% vs 49.75 (PressureVision++), 47.90 (sEMG Only) (+16.96%p (vs P++))。

## 概要

手部压力估计是人机交互、遥操作和虚拟现实中的一项关键感知能力。现有方法主要依赖前臂表面肌电信号（sEMG）推断手部压力，但面临一个根本瓶颈：仅使用前臂sEMG信号难以区分因肌肉激活模式相似但手部姿势不同而导致的压力分布差异，这严重限制了压力估计的准确性和鲁棒性。

针对这一瓶颈，本文提出 **PiMForce**（Posture Informed Muscular Force Learning），一种姿态引导的肌肉力学习框架，发表于 **NeurIPS 2024**。其核心思路是：将3D手部姿势信息作为额外的空间先验引入sEMG特征，使模型能够分辨相似肌肉活动对应的不同压力模式。通过多模态融合（sEMG + 3D手部姿势），PiMForce 提供了互补的生理和空间信息，使全手压力估计在多样抓取和交互下更为精确和鲁棒。

在方法层面，PiMForce 构建了三个关键模块：sEMG特征提取器（将sEMG经STFT转换为频谱图后由2D编码器-解码器提取512维特征）、3D手部姿势特征提取器（将15个关节角度转换为21个3D关节点热图体积，由3D ResNet34提取512维特征），以及特征融合与预测模块（拼接后经全连接层输出9个手部区域的压力分类与回归值）。训练采用联合分类-回归损失（交叉熵 + L2），以同时优化压力存在性判断和数值精度。

实验结果表明，PiMForce 在多项指标上显著优于基线方法。在同用户设置下，R² 达到 88.86%（相比 sEMG Only 的 83.49% 提升 5.37 个百分点），NRMSE 降至 6.65%（下降 1.42 个百分点），分类准确率达到 83.17%（提升 5.34 个百分点）。跨用户泛化测试中，PiMForce 的 R² 为 70.06%，远超 sEMG Only 的 47.90% 和视觉基线 PressureVision++ 的 49.75%，表明多模态信息对用户泛化至关重要。

消融实验进一步验证了设计选择的有效性：移除3D手部姿势特征导致 R² 骤降至 66.32%、NRMSE 升至 11.57%；而使用角度特征替代3D姿势特征仅带来微小提升（R² 84.22% vs 83.49%），证实了完整3D空间表示的重要性。

该方法的主要局限包括：数据集参与人数有限（21人）且性别不平衡（81%男性），可能影响跨人群泛化；实际部署时依赖视觉手势估计的质量，在复杂遮挡场景下可能引入噪声；压力估计上限为20N，无法测量更大力度。

手部压力估计是触觉感知与人机交互领域的核心任务，其目标是从可穿戴或非侵入式传感器信号中实时推断手指与手掌各区域施加的力。精确的压力感知对机器人遥操作、虚拟现实中的力反馈、假肢控制以及技能评估等应用至关重要。然而，现有方法面临一个根本性的瓶颈：**仅依赖前臂表面肌电信号（sEMG）难以区分因肌肉激活模式相似但手部姿势不同所导致的压力分布差异**。例如，用食指按压与用中指按压时，前臂sEMG信号在8通道频谱图上呈现出高度相似的模式（见附录Figure 12），这使得单一模态模型在多样抓取和交互场景下的压力估计精度和鲁棒性均受到严重制约。

现有压力估计范式可大致分为三类：基于视觉的方法（如**PressureVision++**）从单张RGB图像推断接触压力，但在手部自遮挡或物体遮挡场景下性能急剧退化；基于可穿戴sEMG的方法直接从前臂肌肉电信号回归压力值，却无法感知手部关节的空间构型；多模态数据集（如ContactPose、OakInk等，见Table 1）虽然同时采集了视觉、触觉和手部姿态数据，但鲜有工作将3D手部姿势信息作为显式先验融入sEMG驱动的压力估计流程中。这一缺口构成了本文的核心动机：**能否通过多模态融合——将3D手部姿势的空间信息作为sEMG的互补信号——来消除肌肉活动模式的歧义，从而在复杂交互下实现全手压力的鲁棒估计？**

PiMForce正是基于这一因果机制设计的：3D手部姿势提供了手指关节的空间构型先验，使得模型能够分辨相似sEMG模式所对应的不同压力分布（如食指按压 vs. 中指按压）。该框架将视觉驱动的3D手部姿势估计与可穿戴sEMG信号相结合，覆盖从指尖到全手掌的9个区域，并在22种预定义手-物体交互中验证了其有效性。

## 核心方法与创新机理

PiMForce 的核心创新在于**将3D手部姿势信息作为空间先验引入前臂sEMG信号处理**，以解决单一sEMG模态在压力估计中的根本瓶颈。仅使用前臂sEMG信号时，相似的肌肉激活模式可能对应不同的手部姿势和压力分布，导致模型难以区分这些歧义情况。PiMForce通过多模态融合，使模型能够利用手部空间构型信息来分辨这些相似肌肉活动背后的不同压力模式。

### 关键设计变更

**1. 手部姿势表示：从无到完整的3D空间特征**

基线模型（sEMG Only）完全不使用手部姿势信息，仅依赖前臂肌肉电信号进行压力估计。PiMForce引入了完整的3D手部姿势特征提取管线：首先将15个关节角度转换为21个3D手关节点，生成关节热图体积（joint heatmap volume），再通过**3D ResNet34**提取512维空间特征。这一设计使得模型能够显式地编码手部在三维空间中的构型信息，为压力估计提供关键的空间先验。

消融实验证实了3D空间表示的必要性：若使用角度特征替代3D姿势特征（sEMG + Hand Angles），R²仅从sEMG Only的83.49%微升至84.22%，提升幅度远小于完整PiMForce的88.86%（Table 2）。这表明简单的角度表示无法充分捕获手部空间构型对压力分布的影响，3D热图体积表示是性能提升的关键。

**2. 训练损失：从单一回归到分类-回归联合优化**

PiMForce将压力估计任务分解为两个互补的子任务：判断手部区域是否存在压力（分类）和回归具体压力数值（回归）。模型输出9个手部区域的压力分类概率和回归值，训练时采用联合损失函数：

$$L = L_c + \lambda \cdot L_r$$

其中分类损失 $L_c$ 为交叉熵损失，用于判断各区域是否存在压力；回归损失 $L_r$ 为L2损失，用于回归压力数值。这种联合优化策略使模型在学习压力大小的同时，也学习压力分布的空间模式，从而提升整体估计精度。

### 多模态融合架构

PiMForce的融合架构（Figure 2）由三个核心模块组成：

- **sEMG特征提取器（$f_{EMG}$）**：使用短时傅里叶变换将sEMG时域信号转换为频谱图（$E \in \mathbb{R}^{8 \times 32 \times 64}$），通过2D编码器-解码器和全连接层提取512维特征。
- **3D手部姿势特征提取器（$f_{hand}$）**：从15个关节角度重建21个3D关节点，生成3D热图体积，经3D ResNet34提取512维特征。
- **特征融合与预测模块（$f_{pred}$）**：拼接1024维融合特征，经全连接层降维和BN-ReLU处理后，输出9个区域的分类概率和回归值。

这种设计使sEMG提供的生理信息与3D手部姿势提供的空间信息形成互补，显著提升了全手压力估计在多样抓取和交互场景下的准确性和鲁棒性。跨用户实验进一步验证了这一创新：PiMForce的R²达到70.06%，远超sEMG Only的47.90%（Table 3），表明多模态信息对用户泛化至关重要。

PiMForce 是一个多模态手部压力估计框架，其核心设计思想是通过引入 3D 手部姿势信息来增强前臂表面肌电信号（sEMG）的表征能力。仅使用 sEMG 信号面临一个关键瓶颈：相似的肌肉激活模式可能对应截然不同的手部姿势和压力分布，导致模型难以区分这些歧义状态。PiMForce 的因果调节机制在于将 3D 手部姿势作为额外的空间先验与 sEMG 特征融合，使模型能够分辨相似肌肉活动下的不同压力模式。

### 输入模态与预处理

框架接收两类异构输入：

- **前臂 sEMG 信号**：通过定制的 8 通道 sEMG 传感器臂带（Trigno Avanti, Delsys）采集，采样率为 2148 Hz。原始时域信号首先经过短时傅里叶变换（STFT）转换为频谱图表示 $E \in \mathbb{R}^{8 \times 32 \times 64}$，以抑制噪声并保留时频特征。
- **3D 手部姿势**：在实际部署中，3D 手部姿势由现成的视觉手势估计器从 RGB 或 RGB-D 图像中提取 21 个手部关节点的三维坐标。训练阶段则使用磁感应无标记手指追踪模块（Quantum Mocap Metaglove, Manus）获取高精度手部姿势真值。

由于 sEMG 与手部姿势的采样率不同，系统采用线性插值方法对高频 sEMG 数据进行降采样，实现多模态数据的同步对齐。

### Pipeline 模块架构

如 **Figure 2** 所示，PiMForce 由三个主要模块串联构成：

![[assets/figures/papers/paper_list_l1798_PiMForce_Posture_Informed_Muscular_Force_Learning_for_Robust_Hand_Pressu/figures/003_Figure_2.jpg]]
*Figure 2: Our multimodal hand pressure estimation architecture enhances sEMG data by embedding 3D hand pose information. We train the model using a classification-regression joint loss to improve hand pressure estimation*

1. **sEMG 特征提取器 $f_{\text{EMG}}$**：将 sEMG 频谱图 $E$ 输入 2D 编码器-解码器网络，经全连接层压缩为 512 维特征向量，捕获肌肉激活的时频模式。

2. **3D 手部姿势特征提取器 $f_{\text{hand}}$**：将 21 个手部关节点的三维坐标转换为 3D 热图体积表示，随后通过 3D ResNet34 提取 512 维空间特征，编码手部关节的空间配置信息。

3. **特征融合与预测模块 $f_{\text{pred}}$**：将上述两个 512 维特征向量拼接为 1024 维联合表示，经过全连接层降维和 Batch Normalization-ReLU 激活后，同时输出两个预测头：
   - **分类头**：对 9 个手部区域（指尖和手掌分区）预测压力存在与否的二分类概率 $\hat{C}_i$。
   - **回归头**：对上述区域预测连续压力值 $\hat{P}_i$。

### 联合损失函数

PiMForce 采用分类-回归联合损失进行端到端训练，以同时优化压力存在性判断和压力数值精度：

$$L_c = \frac{1}{I} \sum_{i=1}^{I} \left[ C_i \cdot \log \hat{C}_i + (1 - C_i) \cdot \log(1 - \hat{C}_i) \right]$$

$$L_r = \frac{1}{I} \sum_{i=1}^{I} \| \hat{P}_i - P_i \|^2$$

$$L = L_c + \lambda \cdot L_r$$

其中 $I=9$ 为手部区域数量，$C_i$ 为区域 $i$ 的压力存在性真值，$P_i$ 为压力真值，$\lambda$ 为平衡两类损失的权重超参数。分类损失 $L_c$ 为交叉熵，回归损失 $L_r$ 为均方误差。

### 推理流程

在实际部署中，PiMForce 的推理流程为：RGB 图像 → 现成 3D 手势估计器 → 21 个手部关节点坐标 → 3D 热图体积 → $f_{\text{hand}}$；同时 sEMG 信号 → STFT 频谱图 → $f_{\text{EMG}}$；两者特征拼接后经 $f_{\text{pred}}$ 输出全手 9 个区域的压力分类和回归结果，支持实时压力可视化（如 **Figure 1** 所示）。

![[assets/figures/papers/paper_list_l1798_PiMForce_Posture_Informed_Muscular_Force_Learning_for_Robust_Hand_Pressu/figures/001_Figure_1.jpg]]
*Figure 1: Our sensing framework (PiMForce) leverages 3D hand posture information along with sEMG data to enable a whole-hand pressure estimation during various hand-object interactions. We support real-time pressure estimation on the fingertips and palm regions based on RGB image and sEMG inputs. The intensity of each node’s color indicates the pressure level*

![[assets/figures/papers/paper_list_l1798_PiMForce_Posture_Informed_Muscular_Force_Learning_for_Robust_Hand_Pressu/figures/025_Figure_13.jpg]]
*Figure 13: Visualization of ground truth pressure and predicted pressure for the same posture using the existing PressureVision++ hand pressure prediction framework. (a) Original image from camera. (b) Input image for the PressureVision++ model. (c) Overlaied predicted pressure by PressureVision++. (d) Original predicted pressure. (e) Overlaied predicted pressure by PressureVision++, projected onto Sensel pressure array. (f) Ground truth pressure, projected onto Sensel pressure array*

PiMForce 的核心架构由三个功能模块构成，分别负责 sEMG 信号特征提取、3D 手部姿势特征提取以及多模态特征融合与压力预测。模型通过联合分类-回归损失进行端到端训练，以同时学习压力区域的存在性判断与压力数值的精确回归。

### sEMG 特征提取器 (f_EMG)

原始 sEMG 信号为 8 通道时域序列。为抑制噪声并提取有意义的频域表示，模块首先对每个通道的时域信号施加短时傅里叶变换（STFT），将其转换为频谱图 $E \in \mathbb{R}^{8 \times 32 \times 64}$（Section 4.2）。随后，一个 2D 编码器-解码器网络对频谱图进行进一步的特征抽象，最终通过全连接层输出 512 维的肌肉激活特征向量（Section C.2）。该设计的直觉在于：不同手势下肌肉活动的频率成分差异可通过频谱图显式捕获，而编码器-解码器结构有助于在压缩表示中保留关键激活模式。

### 3D 手部姿势特征提取器 (f_hand)

手部姿势信息以 15 个关节角度作为输入。模块首先将这些角度参数转换为 21 个 3D 手部关节点的空间坐标，进而生成 3D 热图体积（3D heatmap volume），将关节位置编码为空间概率分布。该热图体积随后输入 3D ResNet34 网络，输出与 sEMG 特征等长的 512 维空间姿势特征向量（Section 4.2; Section C.2）。与直接使用角度特征相比，3D 热图表示能够保留关节间的空间结构关系，为后续融合提供更丰富的几何先验。

### 特征融合与预测模块 (f_pred)

来自 f_EMG 和 f_hand 的两个 512 维特征向量被拼接为 1024 维联合表示。该联合向量依次经过全连接层降维、批归一化（BN）和 ReLU 激活函数处理，最终输出手部 9 个区域（指尖与掌心分区，参见 Section B.1.1 的 Figure 5）的压力预测结果。每个区域产生两类输出：压力存在性的分类概率与压力数值的回归值（Section 4.2; Section 4.3）。

### 联合分类-回归损失函数

为同时优化压力区域的二分类任务与压力值的连续回归任务，PiMForce 采用联合损失函数进行训练。

**分类损失 $L_c$** 采用二元交叉熵，用于判断每个手部区域是否存在压力接触：

$$L_c = \frac{1}{I} \sum_{i=1}^{I} \left[ C_i \cdot \log \hat{C}_i + (1 - C_i) \cdot \log(1 - \hat{C}_i) \right]$$

其中 $I=9$ 为手部区域总数，$C_i \in \{0, 1\}$ 为区域 $i$ 的真实压力存在标签，$\hat{C}_i \in [0, 1]$ 为模型预测的存在概率（Section 4.3, Equation (1)）。

**回归损失 $L_r$** 采用均方误差（MSE），用于回归各区域的压力幅值：

$$L_r = \frac{1}{I} \sum_{i=1}^{I} \| \hat{P}_i - P_i \|^2$$

其中 $P_i$ 与 $\hat{P}_i$ 分别为区域 $i$ 的真实压力值与预测压力值（Section 4.3, Equation (2)）。

**联合损失** 通过超参数 $\lambda$ 平衡两个任务的训练信号：

$$L = L_c + \lambda \cdot L_r$$

该设计的因果机制在于：分类分支引导模型首先判断哪些区域正在受力，回归分支则在此基础上精确估计压力大小。两分支共享融合特征，使姿势与肌肉活动的互补信息能同时服务于存在性判别与幅值回归，从而提升整体估计的鲁棒性（Section 4.3）。

![[assets/figures/papers/paper_list_l1798_PiMForce_Posture_Informed_Muscular_Force_Learning_for_Robust_Hand_Pressu/figures/021_Figure_12.jpg]]
*Figure 12: Visualization of patterns with similar EMG footprint on different postures*

## 实验与关键发现

### 主实验结果

PiMForce 在自定义多模态数据集（22 种交互，21 名参与者）上进行了系统评估。Table 2 报告了各模型在同用户留出测试集上的性能对比：

![[assets/figures/papers/paper_list_l1798_PiMForce_Posture_Informed_Muscular_Force_Learning_for_Robust_Hand_Pressu/figures/022_Table_8.jpg]]
*Table 8: Performance comparison of models in terms of MAE. Note that this table reports the performance of Table 2 in terms of the MAE metric*

- **R²**：PiMForce 达到 **88.86%**，较 sEMG Only 模型的 83.49% 提升 **+5.37 个百分点**，较 3D Hand Posture Only 模型的 66.32% 提升 +22.54 个百分点。
- **NRMSE**：PiMForce 降至 **6.65%**，显著低于 sEMG Only（8.07%）和 3D Hand Posture Only（11.57%）。
- **分类准确率**：PiMForce 达到 **83.17%**，较 sEMG Only 的 77.83% 提升 +5.34 个百分点。

这些结果表明，融合 3D 手部姿势与 sEMG 的多模态方案在所有指标上均显著优于单一模态基线。值得注意的是，仅使用 3D 手部姿势的模型性能最差（R² 仅 66.32%），说明单独的手部几何信息不足以推断压力大小——肌肉激活信号是压力估计的核心信息源，而手部姿势提供了关键的互补空间先验。

### 消融研究

**多模态融合的有效性**：Table 2 中的消融对比直接验证了核心设计选择。移除 3D 手部姿势特征使 R² 从 88.86% 骤降至 66.32%，NRMSE 从 6.65% 升至 11.57%，证实姿势信息对压力估计的因果贡献。更精细的消融显示，使用角度特征替代 3D 姿势特征（sEMG + Hand Angles）仅带来微小提升（R² 84.22% vs sEMG Only 83.49%），表明 3D 空间表示（关节热图体积经 3D ResNet 处理）相比简单的角度向量能更有效地编码手部构型与压力分布之间的空间对应关系。

**跨用户泛化**：Table 3 的跨用户实验进一步揭示了多模态融合的价值。在留一用户交叉验证设置下，PiMForce 的 R² 为 **70.06%**，而 sEMG Only 模型仅为 47.90%，差距扩大至 +22.16 个百分点。这表明 sEMG 信号的用户间变异极大，单纯依赖肌肉电信号难以泛化到未见用户；3D 手部姿势作为相对用户无关的空间表示，有效缓解了这一问题。

**手部区域性能差异**：Table 4 按手部 9 个区域分别报告 NRMSE。PiMForce 在所有区域上均优于基线，尤其在拇指（Thumb）和食指（Index）指尖区域表现最佳，这些区域在抓取任务中压力变化最丰富。小指（Pinky）和掌心上部（Palm Upper）区域的误差相对较大，可能与这些区域在多数交互中压力较低、信号信噪比不足有关。

### 与视觉基线的对比

在跨用户设置下的平面交互和捏取姿势子集上（Table 5），PiMForce 的 R² 达到 **66.71%**，显著优于视觉方法 PressureVision++ 的 49.75%（+16.96 个百分点）。Figure 4 的定性对比直观展示了差异：当手部被物体遮挡时（红色矩形标注），PressureVision++ 完全无法估计压力，而 PiMForce 借助不依赖视线的 sEMG 信号仍能输出合理的全手压力分布。这验证了可穿戴 sEMG 在遮挡场景下的鲁棒性优势。

![[assets/figures/papers/paper_list_l1798_PiMForce_Posture_Informed_Muscular_Force_Learning_for_Robust_Hand_Pressu/figures/009_Figure_4.jpg]]
*Figure 4: (a) Qualitative results in the absence of a pressure glove. The 3D Hand Pose Estimation [69] represents 3D hand posture, including hand occlusion, using the 3D hand detector. The Pressure-Vision++ [28] column shows the pressure estimation of fingertips. The red rectangles indicate the instances of pressure estimation failure due to hand occlusion. The proposed multimodal framework shows robust whole-hand pressure estimation for diverse hand-object interactions. (b) Illustration of the demo video footage showing robust hand pressure estimation with varying hand postures, pressure levels, and interacting objects*

### 失败模式与局限性

尽管 PiMForce 在同用户设置下表现优异，跨用户性能的显著下降（R² 从 88.86% 降至 70.06%）暴露了模型对用户个体差异的适应仍不充分。Figure 3 的姿势维度分析显示，某些握姿（如 Power Sphere Grasp）的跨用户误差条明显更大，提示这些复杂抓取下的肌肉激活模式具有更高的用户特异性。

此外，模型训练依赖数据手套（Manus Metaglove）捕获的高质量 3D 手部姿势，实际部署时需依赖现成的视觉手势估计器。当 RGB 图像中手部严重遮挡或光照条件恶劣时，3D 手部姿势估计的质量下降将直接传导至压力预测，构成级联失效风险。Figure 4 (a) 中虽展示了 PiMForce 对遮挡的鲁棒性，但该场景下手部姿势估计本身是否可靠仍需结合具体检测器评估。

数据层面，参与者以男性为主（17/21），且手部尺寸均大于 180mm，模型在女性和小手人群上的性能有待验证。压力测量上限为 20N，超出部分被剪切处理，限制了高负荷抓取场景的适用性。

## 定位与知识库关联

PiMForce 处于**可穿戴肌肉感知**与**视觉手部重建**两条技术路线的交叉地带。其核心动机源于一个被现有工作忽略的瓶颈：前臂 sEMG 信号在肌肉激活模式相似但手部姿势不同时，难以分辨压力分布差异（Section 4.1）。因此，PiMForce 并非单纯改进 sEMG 解码器，而是通过引入 3D 手部姿势作为**空间先验**来解耦这一歧义。

### 与基线方法的关系与增量

PiMForce 的消融实验明确量化了各模态的贡献边界：

- **sEMG Only Model**：仅使用前臂 sEMG 的回归模型，是压力估计的传统范式。在同用户设置下，其 R² 为 83.49%，NRMSE 为 8.07%（Table 2）。这构成了 PiMForce 的直接对比基线。
- **3D Hand Posture Only Model**：仅使用 3D 手部姿势特征的消融模型，R² 骤降至 66.32%，NRMSE 升至 11.57%（Table 2）。这表明纯几何信息无法独立支撑压力估计，因为相同的姿势可以施加不同的力。
- **sEMG + Hand Angles Model**：将 3D 姿势替换为 15 维关节角度的融合模型，R² 仅从 83.49% 微升至 84.22%（Table 2）。这一对比揭示了关键因果机制：**3D 空间热图体积表示**（通过 3D ResNet34 处理）相比低维角度向量，能为 sEMG 特征提供更丰富的空间上下文，从而显著提升融合效果。
- **PressureVision++**：基于单 RGB 图像的压力估计视觉基线。在跨用户平面交互和捏取姿势下，其 R² 为 49.75%，而 PiMForce 达到 66.71%（Table 5），领先约 17 个百分点。PiMForce 的定性结果（Figure 4）进一步表明，视觉方法在手部遮挡时会出现压力估计失败（红框标注），而多模态框架因 sEMG 不受视线遮挡影响，表现出更强的鲁棒性。

从方法演进角度看，PiMForce 的贡献不在于提出全新的 sEMG 解码架构或视觉姿势估计器，而在于**证明了多模态融合对压力估计的因果性增益**，并提供了可量化的消融证据。其“分类-回归联合损失”（Section 4.3, Equation 1-2）也是一个实用的工程改进：分类头判断区域是否存在压力，回归头估计压力数值，二者通过超参数 λ 平衡。

### 适用边界与局限

PiMForce 的性能边界在实验中有清晰体现：

1. **同用户 vs. 跨用户性能落差**：同用户 R² 达 88.86%，跨用户降至 70.06%（Table 2 vs. Table 3）。这表明模型对训练集用户的肌肉激活模式存在一定程度的过拟合，对新用户的泛化仍有约 18.8 个百分点的性能损失。

2. **数据集的人口学偏差**：21 名参与者中男性占 81%（17/21），且仅包括手部尺寸大于 180mm 的个体（Section 3.2）。这可能导致模型在女性用户或手部较小人群上的性能下降，但论文未提供相关消融实验，该点需手动验证。

3. **压力量程限制**：压力估计上限为 20N，超出部分被剪切（Section 3.1），这意味着高负载抓取场景不在模型的有效工作范围内。

4. **交互多样性有限**：数据集仅覆盖 22 种预定义交互（Section 3.2），虽然涵盖了平面按压、捏取等基本模式，但日常手部活动的长尾分布远未被覆盖。

5. **部署依赖视觉姿势估计器**：训练时使用磁感数据手套捕获 3D 手部姿势真值，但实际部署依赖 off-the-shelf 视觉手部姿势检测器（Section 4.4）。在严重遮挡场景下，视觉姿势估计的质量下降会直接传导至压力估计，尽管 sEMG 分支本身不受遮挡影响。

### 开放问题

论文未解决但值得后续探索的方向包括：

- **物体上下文融合**：当前方法仅利用手部姿势作为空间先验，未引入被操作物体的形状、材质等语义信息。在抓取不同刚度物体时，相同的手部姿势和肌肉激活可能对应截然不同的压力分布，物体信息有望进一步解耦这一歧义。
- **更高密度的肌肉感知**：现有 8 通道 sEMG 阵列的空间分辨率有限。HD-EMG 或更高密度电极阵列可能捕获更精细的肌肉协同模式，尤其是在手指独立控制的场景中。
- **轻量化与实时部署**：PiMForce 的双分支架构（2D 编码器-解码器 + 3D ResNet34）对移动设备的计算资源要求较高，如何在保持多模态增益的前提下实现模型压缩是一个工程挑战。
- **遮挡鲁棒的手部姿势估计**：当视觉姿势估计失效时，PiMForce 退化为 sEMG Only 模型（R² 约 83.49%）。探索融合惯性传感器或利用时序信息来弥补视觉遮挡，是提升系统鲁棒性的关键路径。

## 原文 PDF

![[paperPDFs/NEURIPS_2024/PiMForce_Posture_Informed_Muscular_Force_Learning_for_Robust_Hand_Pressure_Estimation.pdf]]
