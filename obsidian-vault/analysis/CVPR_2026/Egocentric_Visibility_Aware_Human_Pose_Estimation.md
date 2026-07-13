---
title: Egocentric Visibility-Aware Human Pose Estimation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Egocentric_Visibility_Aware_Human_Pose_Estimation.pdf
project_link: null
code_link: null
aliases:
- EVAHPE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 显式预测关键点可见性状态，并采用基于可见性的损失加权方案，在训练中对可见和不可见关键点施加差异化监督。
primary_logic: 通过联合估计3D关键点和可见性分数，并利用可见性信息降低不可见关键点对可见关键点的干扰；同时结合预训练VQ-VAE姿态先验和迭代式帧内-帧间注意力机制进一步优化时序一致性，从而显著提升整体姿态估计精度。
claims:
- EvaPose包含三个关键组件：VQ-VAE姿态先验、可见性感知的3D估计网络、迭代式帧内-帧间注意力模块。
- 通过可见性感知模型和损失设计，MPJPE从40.6降至35.6（Eva-3M测试集）。
- VQ-VAE姿态先验使MPJPE从39.1降至35.6。
- 时序融合模块（TTE）同时降低MPJPE和Jitter指标（Table 5）。
---

# Egocentric Visibility-Aware Human Pose Estimation

> [!tip] 核心洞察
> 通过联合估计3D关键点和可见性分数，并利用可见性信息降低不可见关键点对可见关键点的干扰；同时结合预训练VQ-VAE姿态先验和迭代式帧内-帧间注意力机制进一步优化时序一致性，从而显著提升整体姿态估计精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 以自我为中心的可视性感知人体姿态估计 |
| 英文题名 | Egocentric Visibility-Aware Human Pose Estimation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23618) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | EvaPose |
| Dataset | Eva-3M, EMHI: P1, EMHI: P2 |

> [!tip] 效果简介
> - Eva-3M 上，MPJPE (mm) 35.6 (EvaPose-ResNet50) / 34.2 (EvaPose-ViT-L) vs 49.8 (FRAME) (-14.2 / -15.6)。
> - EMHI: P1 上，MPJPE (mm) 36.2 (EvaPose-ResNet50) / 31.7 (EvaPose-ViT-L) vs 37.4 (FRAME) (-1.2 / -5.7)。
> - EMHI: P2 (unseen actions) 上，MPJPE (mm) 38.5 (EvaPose-ResNet50) / 33.3 (EvaPose-ViT-L) vs 60.5 (FRAME) (-22.0 / -27.2)。

## 概要

以自我为中心的人体姿态估计面临一个根本性瓶颈：**关键点不可见问题**。由于自遮挡和有限的视场（FoV），大量身体关键点无法被相机直接观测，而现有方法（如 **UnrealEgo**、**EgoPoseFormer**、**FRAME**）通常对所有关键点同等处理，导致不可见关键点的噪声干扰了可见关键点的估计精度。

针对这一问题，本文提出 **EvaPose**，其核心调控手段是**显式预测关键点可见性状态**，并采用基于可见性的损失加权方案——可见关键点权重 1.0，不可见关键点权重 0.1——在训练中对二者施加差异化监督。该方法的核心洞察在于：通过联合估计 3D 关键点和可见性分数，利用可见性信息降低不可见关键点对可见关键点的干扰；同时结合预训练 VQ-VAE 姿态先验与迭代式帧内-帧间注意力机制，进一步优化时序一致性，从而显著提升整体姿态估计精度。

在方法谱系上，EvaPose 与现有工作的关键差异体现在三个维度：

| 设计维度 | 现有方法 | EvaPose |
|---------|---------|---------|
| **可见性处理** | 同等对待所有关键点 | 显式预测可见性，差异化损失加权 |
| **姿态先验** | 无显式先验或简单表示 | 预训练 VQ-VAE 离散码本强先验 |
| **时序融合** | 各方法独立设计 | 迭代式立体 Transformer 解码器 + 时序 Transformer 编码器交替融合 |

在实验验证上，EvaPose 在 Eva-3M 测试集上取得了 **MPJPE 35.6 mm**（ResNet50 骨干）和 **34.2 mm**（ViT-L 骨干），相较于 FRAME 的 49.8 mm 分别降低 14.2 mm 和 15.6 mm。在 EMHI 数据集上，EvaPose-ViT-L 达到 MPJPE 31.7 mm（P1 已知动作）和 33.3 mm（P2 未见动作），较 FRAME 分别降低 5.7 mm 和 27.2 mm，展现出对分布外动作的强泛化能力。消融实验证实，可见性感知模型与损失设计使 MPJPE 从 40.6 降至 35.6，VQ-VAE 姿态先验使 MPJPE 从 39.1 进一步降至 35.6，时序 Transformer 编码器同时降低了 MPJPE 和 Jitter 指标。

需要注意的是，EvaPose-ViT-L 在 V100 GPU 上仅 9.4 FPS，无法满足实时需求；方法强依赖高质量关键点可见性标注，标注成本高昂；跨数据集泛化仍存在性能差距，对极端自遮挡或罕见动作的鲁棒性有待进一步验证。



以自我为中心（egocentric）的人体姿态估计旨在从穿戴式相机拍摄的第一人称视角图像中恢复人体3D姿态。该任务在沉浸式虚拟现实、人机交互和运动分析等场景中具有重要应用价值。然而，与第三人称视角的姿态估计相比，以自我为中心的设定面临两个核心挑战：**自遮挡**和**有限视场（out-of-FoV）**。由于相机佩戴在人体上，大量身体关键点——尤其是下肢关节——经常处于相机视野之外或被身体其他部位遮挡，导致关键点不可见问题普遍存在。

现有以自我为中心的人体姿态估计方法，如 **UnrealEgo**、**EgoPoseFormer** 和 **FRAME**，通常对所有关键点同等对待，未显式区分可见与不可见关键点。这种无差别的处理策略使得不可见关键点的噪声和不确定性会干扰可见关键点的估计，从而损害整体姿态估计精度。因此，**不可见关键点对可见关键点的干扰**构成了该领域的关键瓶颈。

此外，现有方法缺乏对**人体姿态先验**的有效利用。人体姿态空间具有内在的结构约束和运动规律，但多数方法仅从图像特征直接回归3D关键点，未引入强先验来约束异常或不符合人体结构的预测。同时，时序信息的融合方式也有待改进——如何有效地在帧内多视图特征和帧间时序特征之间建立交互，是提升姿态平滑性和准确性的关键。

为应对上述挑战，本文提出 **EvaPose**，一个以自我为中心的可见性感知人体姿态估计框架。EvaPose的核心动机在于：**显式建模关键点的可见性状态，并利用可见性信息对训练过程进行差异化监督，从而降低不可见关键点对可见关键点的干扰**。同时，通过引入预训练的VQ-VAE姿态先验和迭代式帧内-帧间注意力机制，进一步提升姿态估计的精度和时序一致性。



## 核心方法与创新机理

EvaPose 的核心创新在于首次将以自我为中心的人体姿态估计中“关键点不可见”这一普遍瓶颈显式建模，并通过三个相互协同的**变更槽（changed slots）**系统性地解决了该问题。

### 变更槽一：从无差别处理到可见性感知的差异化监督

现有以自我为中心的方法（如 UnrealEgo、EgoPoseFormer、FRAME）对所有关键点一视同仁，未区分可见与不可见状态。然而，在自遮挡和有限视场条件下，不可见关键点的标注本身存在高度不确定性，强制模型拟合这些点会引入噪声，反而损害可见关键点的估计精度。EvaPose 的**可见性感知 3D 估计网络**首次显式预测每个关键点的可见性置信度分数，并据此设计**基于可见性的损失加权方案**：可见关键点权重为 1.0，不可见关键点权重降至 0.1。这一机制在训练中从根本上降低了不可见关键点对可见关键点的干扰，其因果效应在消融实验中得到了直接验证——引入该设计后，Eva-3M 上的 MPJPE 从 40.6 mm 降至 35.6 mm，其中可见肢体关键点误差（VLK-PE）从 55.8 mm 降至 52.1 mm，不可见肢体关键点误差（ILK-PE）也从 62.6 mm 降至 59.4 mm（Table 4）。这表明差异化监督不仅保护了可见关键点的估计质量，还通过减轻噪声梯度间接改善了不可见关键点的学习。

### 变更槽二：从无先验到 VQ-VAE 姿态先验的引入

基线方法缺乏对合理人体姿态的显式约束，在严重遮挡场景下容易产生违反人体结构的异常预测。EvaPose 引入**预训练 VQ-VAE 姿态先验**，将规范坐标系下的 3D 关键点编码为离散码本表示。该 VQ-VAE 在 AMASS、MOYO 和 AIST++ 等大规模运动捕捉数据集上预训练（码本尺寸 2048×256，token 数 M=160），并在下游训练中保持冻结，为模型提供了强健的人体姿态流形约束。消融实验（Table 5）显示，单独加入 VQ-VAE 先验使 MPJPE 从 39.1 mm 进一步降至 35.6 mm，同时降低了时序抖动（Jitter），证明离散姿态先验不仅能提升单帧精度，还能增强时序平滑性。

### 变更槽三：从简单时序融合到迭代式帧内-帧间注意力

现有方法的时序融合策略各异（如 FRAME 的时序融合模块），但大多缺乏对多视图和时序信息的深层交互。EvaPose 设计了**迭代式帧内-帧间注意力网络**，由立体 Transformer 解码器（STD）和时序 Transformer 编码器（TTE）交替执行：STD 在每帧内独立地对左右视图特征进行交叉注意力融合，TTE 则在时间窗口（T=24 帧）上对多视图融合特征进行自注意力编码。这一交替迭代机制使特征能够逐步吸收多视角几何约束和时序运动线索。消融实验（Table 5）证实，TTE 模块同时降低了 MPJPE 和 Jitter，验证了其提升估计精度与时序一致性的双重作用。

三个变更槽之间存在因果协同：可见性感知模块为后续的帧内-帧间注意力提供了更干净的初始特征，VQ-VAE 先验则在姿态重建阶段抑制了不可见关键点可能引发的异常预测，而迭代注意力网络进一步在时序维度上平滑了这些预测。这种“感知-约束-精炼”的级联设计，使 EvaPose 在 Eva-3M 和 EMHI 两个基准上均显著超越现有方法（如 EvaPose-ResNet50 在 Eva-3M 上 MPJPE 35.6 mm vs. FRAME 49.8 mm；在 EMHI P2 未见动作上 MPJPE 38.5 mm vs. FRAME 60.5 mm），且这一优势在跨数据集泛化实验（Eva-3M 训练→EMHI 测试）中同样保持。



EvaPose 将自中心人体姿态估计建模为一个时序条件生成问题：给定长度为 $T$ 的立体观测序列（左右视图图像 $I_L^{1:T}, I_R^{1:T}$ 及对应相机位姿 $C_L^{1:T}, C_R^{1:T}$），估计世界坐标系下的 3D 关键点序列 $J_W^{1:T}$。其目标函数为：

$$f_{\phi}(J_{W}^{1:T} \mid I_{L}^{1:T}, I_{R}^{1:T}, C_{L}^{1:T}, C_{R}^{1:T})$$

整体架构由三个核心模块串联构成（Figure 2），形成“逐帧感知→时序融合→先验重建”的级联管线：

![[assets/figures/papers/paper_list_l1015_https_arxiv_org_abs_2602_23618/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the proposed EvaPose. Given a sequence of egocentric observations, we first propose a visibility-aware 3D pose estimation network to extract stereo image features, and predict per-frame 3D keypoints in the camera coordinate system (defined as the left camera coordinate system in this paper) and their corresponding visibility confidence scores. Then, the predicted 3D keypoints are transformed to the canonical coordinate system with the help of camera poses from SLAM system. Next, an iterative intra-and inter-frame attention network is used for temporal feature fusion. Finally, we estimate the 3D poses with the pre-trained VQ-VAE decoder*

1. **可见性感知的 3D 姿态估计网络**  
   对每一帧独立处理，从立体图像对中提取视觉特征 $F_L^t, F_R^t$，同时预测相机坐标系下的 3D 关键点 $J_{Cam}^t$ 及其可见性置信度分数 $S_{Vis}^t$。该模块首次显式建模关键点可见性状态，为后续损失加权和多视图融合提供依据。

2. **坐标系转换**  
   利用 SLAM 系统提供的相机位姿，将每帧的相机坐标系 3D 关键点变换到规范坐标系（canonical coordinate system）。该规范坐标系以头部关节在地面投影为原点，消除了相机运动带来的全局位姿歧义，使后续时序建模在统一的姿态空间中操作（Figure 6）。

3. **迭代式帧内-帧间注意力网络**  
   这是管线中的时序融合核心，由**立体 Transformer 解码器（STD）** 和**时序 Transformer 编码器（TTE）** 交替迭代组成（Figure 2(c)）。  
   - STD 对左右视图特征独立执行交叉注意力，生成多视图增强的帧级特征 $f_v^t$：  
     $$f_v^t = \mathrm{Decoder}(q_{n-1}^t, F_v), \quad v \in \{L, R\}$$  
   - TTE 沿时间轴对全窗口的多视图融合特征进行自注意力编码，实现时序信息聚合：  
     $$[q_n^1, q_n^2, ..., q_n^T] = \mathrm{Encoder}([f_n^1, f_n^2, ..., f_n^T])$$  
   经过 $N$ 轮交替迭代后，得到同时融合了立体几何约束与运动时序一致性的特征表示 $q_N^t$。

4. **VQ-VAE 姿态先验与最终重建**  
   融合后的特征 $q_N^t$ 经 MLP 和 Softmax 预测码本嵌入的概率分布 $\hat{z}^t$，再与预训练的离散码本（$2048 \times 256$）相乘得到量化特征 $z^t$。冻结的 VQ-VAE 解码器将 $z^t$ 重建为规范坐标系下的最终 3D 姿态。该码本在大规模动捕数据（AMASS、MOYO、AIST++）上预训练，编码了真实人体姿态的先验分布，有效约束了不可见关键点的预测空间。

**训练策略**：采用两阶段训练。第一阶段仅训练可见性感知 3D 姿态估计模块，损失函数 $\mathcal{L}_{\mathrm{stage1}}$ 由可见性损失、热图损失和 3D 关键点损失的加权和构成，其中热图损失和 3D 损失均采用基于可见性的差异化权重（可见关键点权重 1.0，不可见 0.1）。第二阶段冻结第一阶段权重，训练时序融合网络（时间窗口 $T=24$ 帧），VQ-VAE 模块全程冻结。



### 问题形式化

EvaPose 将任务建模为以自我为中心的观测序列到世界坐标系 3D 关键点序列的条件估计。给定长度为 $T$ 的时间窗口，包含双目图像 $\{I_L^t, I_R^t\}_{t=1}^T$ 及对应相机位姿 $\{C_L^t, C_R^t\}_{t=1}^T$（由 SLAM 系统提供），目标是学习映射 $f_\phi$：

$$f_{\phi}(J_{W}^{1:T} \mid I_{L}^{1:T}, I_{R}^{1:T}, C_{L}^{1:T}, C_{R}^{1:T})$$

其中 $J_{W}^{1:T}$ 为世界坐标系下的人体 3D 关键点序列。

### 三大核心模块

EvaPose 由三个关键组件构成（Fig. 2），形成“初始估计—先验约束—时序精炼”的级联架构：

1. **可见性感知的 3D 姿态估计网络**：从双目图像中提取特征，联合预测每帧相机坐标系下的 3D 关键点 $J_{Cam}^t$ 及其可见性置信度分数 $S_{Vis}^t$。
2. **VQ-VAE 姿态先验**：在大规模动捕数据上预训练的向量量化变分自编码器，将人体姿态编码为离散码本表示，提供强姿态先验约束。
3. **迭代式帧内-帧间注意力网络**：由立体 Transformer 解码器（STD）和时序 Transformer 编码器（TTE）交替构成，对多视图和时序特征进行迭代融合优化。

### 可见性感知机制

该模块是 EvaPose 的核心创新，首次在自我中心姿态估计中显式建模关键点可见性。

**可见性加权热图**：对每个关键点 $i$ 和视图 $v \in \{L, R\}$，网络预测可见性分数 $s_{i,v}$，并与 2D 热图 $\mathcal{H}_{i,v}$ 逐元素相乘：

$$\mathcal{H}_{i,v}' = s_{i,v} \cdot \mathcal{H}_{i,v}$$

**3D 可见性融合**：左右视图的可见性分数取平均，作为 3D 关键点的综合可见性置信度：

$$S_{Vis} = (S_L + S_R) / 2$$

这一设计使网络在训练中能区分可见与不可见关键点，通过损失加权（可见关键点权重 1.0，不可见 0.1）抑制不可见关键点对可见关键点估计的干扰。

### VQ-VAE 姿态先验

VQ-VAE 由编码器 $E$、解码器 $D$ 和可学习的离散码本 $CB = \{c_k\}_{k=1}^K$ 组成（码本大小 $2048 \times 256$，token 数 $M=160$）。该模块在 AMASS、MOYO 和 AIST++ 数据集上预训练后冻结，将人体规范坐标系下的 3D 关键点编码为离散表示，解码器用于从融合特征中重建最终的 3D 姿态。

### 迭代式帧内-帧间注意力

该模块通过交替的 STD 和 TTE 实现多视图与时序特征的深度融合。

**立体 Transformer 解码器（STD）**：在第 $n$ 轮迭代中，对左右视图特征 $F_L, F_R$ 分别进行交叉注意力：

$$f_v^t = \mathrm{Decoder}(q_{n-1}^t, F_v), \quad v \in \{L, R\}$$

**时序 Transformer 编码器（TTE）**：将多视图融合特征 $f_n^t$ 沿时间维度拼接后送入自注意力编码器：

$$[q_n^1, q_n^2, ..., q_n^T] = \mathrm{Encoder}([f_n^1, f_n^2, ..., f_n^T])$$

经过 $N$ 轮迭代后，最终融合特征 $q_N^t$ 用于预测码本 logit：

$$\hat{z}^t = \mathrm{Softmax}(\mathrm{MLP}(q_N^t))$$

并通过可微的量化近似得到离散表示：

$$z^t = \bar{z}_{M \times K}^t \times CB_{K \times D}$$

该近似表示送入预训练的 VQ-VAE 解码器，重建最终的规范坐标系 3D 姿态。

### 损失函数设计

EvaPose 采用两阶段训练。第一阶段训练可见性感知模块，总损失为三项加权和：

$$\mathcal{L}_{\mathrm{stage1}} = \lambda_{\mathrm{vis}} \mathcal{L}_{\mathrm{vis}} + \lambda_{\mathrm{heatmap}} \mathcal{L}_{\mathrm{heatmap}} + \lambda_{\mathrm{3D}} \mathcal{L}_{\mathrm{3D}}$$

其中：

- **热图损失**：对可见/不可见关键点施加差异化权重 $w(s_{i,j})$（可见 1.0，不可见 0.1）：

$$\mathcal{L}_{\mathrm{heatmap}} = \frac{1}{2N_J} \sum_{j=1}^{2} \sum_{i=1}^{N_J} w(s_{i,j}) \cdot \mathrm{MSE}(H_{i,j}, \hat{H}_{i,j})$$

- **3D 姿态损失**：相机坐标系下 3D 关键点的加权 MSE，权重由双视图平均可见性决定：

$$\mathcal{L}_{\mathrm{3D}} = \frac{1}{N_J} \sum_{i=1}^{N_J} \frac{w(s_{i,1}) + w(s_{i,2})}{2} \cdot \mathrm{MSE}(J_{Cam}^i, \bar{J}_{Cam}^i)$$

第二阶段在此基础上加入时序精炼网络，使用 $T=24$ 帧的时间窗口进行端到端训练。

### 补充图表

![[assets/figures/papers/paper_list_l1015_https_arxiv_org_abs_2602_23618/figures/012_Figure_6.jpg]]
*Figure 6: Overview of the coordinate systems*



## 实验与关键发现

### 核心实验设置

EvaPose 采用两阶段训练策略：第一阶段单独训练可见性感知的 3D 姿态估计模块，第二阶段训练时序 3D 姿态精修网络，时间窗口设为 $T = 24$ 帧。VQ-VAE 模块使用 $M = 160$ 个 token，码本尺寸为 $2048 \times 256$，在 AMASS、MOYO 和 AIST++ 数据集上预训练后冻结。评估在两个以自我为中心的基准上进行：

- **Eva-3M**：本文新引入的大规模数据集，包含 31 名受试者的 1,353 个运动序列，涵盖 24 种日常动作类别，其中 435K 帧标注了关键点可见性标签。测试集保留一男一女两名受试者（98 个序列），确保性别平衡。
- **EMHI**：按 70% 训练、16% P1 测试、14% P2 测试划分，其中 P2 包含训练中未见过的动作类别，用于评估分布外泛化能力。

### 主结果分析

**Table 2** 展示了 EvaPose 与现有最优方法在 Eva-3M 和 EMHI 上的全面对比。

在 Eva-3M 上，EvaPose-ResNet50 达到 35.6 mm MPJPE，相比 FRAME（49.8 mm）降低 14.2 mm；EvaPose-ViT-L 进一步降至 34.2 mm，降幅达 15.6 mm。在 EMHI P1 上，EvaPose-ResNet50 为 36.2 mm，略优于 FRAME（37.4 mm）；EvaPose-ViT-L 则为 31.7 mm，领先 5.7 mm。最具挑战性的 EMHI P2（未见动作）上，EvaPose-ResNet50 仅 38.5 mm，而 FRAME 高达 60.5 mm，降幅达 22.0 mm；EvaPose-ViT-L 进一步压缩至 33.3 mm，降幅 27.2 mm。这表明可见性感知机制和 VQ-VAE 姿态先验的组合在分布外场景下具有显著优势。

**Table 3** 按可见/不可见关键点分解精度。EvaPose 在可见关键点上大幅领先，不可见关键点上也保持明显优势，验证了可见性感知策略有效抑制了不可见关键点对可见关键点估计的干扰。

跨数据集泛化实验（**Table 6**，Eva-3M 训练、EMHI 测试）显示，EvaPose-ViT-L 的泛化性能优于其他方法，但整体误差相比域内测试有所增大，说明对真实室内环境等复杂场景的鲁棒性仍有提升空间。

### 消融研究

**Table 4** 隔离了可见性感知模型与损失设计的效果。加入可见性预测头和基于可见性的损失加权后，Eva-3M 上 MPJPE 从 40.6 mm 降至 35.6 mm。其中可见肢体关键点误差（VLK-PE，含踝、足、肘、腕）从 55.8 降至 52.1，不可见肢体关键点误差（ILK-PE）从 62.6 降至 59.4，证明差异化监督同时惠及两类关键点。

**Table 5** 逐组件消融：
1. **VQ-VAE 姿态先验**：移除后 MPJPE 从 35.6 升至 39.1，Jitter 指标也同步恶化，证实离散码本提供的强先验对姿态平滑性和准确性均有贡献。
2. **时序 Transformer 编码器（TTE）**：移除 TTE 后 MPJPE 和 Jitter 均上升，表明帧间时序融合对抑制抖动和提升精度不可或缺。
3. **迭代式帧内-帧间注意力**：交替 STD 和 TTE 的设计使多视图特征和时序信息充分交互，单独移除任一组件的退化已在上述消融中体现。

### 失败模式与局限

1. **计算效率**：EvaPose-ViT-L 在 V100 GPU 上仅 9.4 FPS，无法满足实时应用需求，限制了在交互式系统中的部署。
2. **可见性标注依赖**：方法强依赖高质量的逐关键点可见性标签，标注成本高昂，难以扩展到更大规模或弱标注场景。
3. **极端遮挡与罕见动作**：VQ-VAE 姿态先验在训练数据覆盖不足的极端自遮挡或罕见动作下的泛化能力未充分验证，可能产生不符合人体结构的异常姿态。
4. **跨域鲁棒性**：跨数据集评估（Eva-3M → EMHI）时误差增大，说明对真实室内环境的光照、背景和相机特性变化的适应性有待加强。

### 图表结论摘要

- **Figure 2**：完整呈现 EvaPose 三组件架构——可见性感知 3D 估计网络、VQ-VAE 姿态先验、迭代式帧内-帧间注意力，清晰展示了数据流和坐标系转换关系。
- **Table 2**：EvaPose 在两个数据集、三个测试子集上全面超越 FRAME、UnrealEgo、EgoPoseFormer 等基线，尤其在分布外动作上优势显著。
- **Table 4 & Table 5**：逐一验证了可见性感知机制、VQ-VAE 先验和时序融合的独立贡献，构成了方法有效性的因果链。
- **Figure 4**：展示了拟合的 SMPL 网格，从定性角度验证了 EvaPose 在复杂日常动作下的重建质量。

![[assets/figures/papers/paper_list_l1015_https_arxiv_org_abs_2602_23618/figures/004_Table_2.jpg]]
*Table 2: Comparison with state-of-the-art methods on the Eva-3M and EMHI datasets. The best and second best results are highlighted in boldface and underlined, respectively*

![[assets/figures/papers/paper_list_l1015_https_arxiv_org_abs_2602_23618/figures/006_Table_4.jpg]]
*Table 4: Impact of the visibility-aware model and loss design. VLK-PE is the MPJPE for visible limb keypoints, including ankle, foot, elbow and wrist. ILK-PE denotes the MPJPE for invisible limb keypoints*

![[assets/figures/papers/paper_list_l1015_https_arxiv_org_abs_2602_23618/figures/007_Table_5.jpg]]
*Table 5: Ablation study for key components in our model*

![[assets/figures/papers/paper_list_l1015_https_arxiv_org_abs_2602_23618/figures/010_Figure_4.jpg]]
*Figure 4: Visualization of some representative fitted SMPL meshes*

### 补充图表

![[assets/figures/papers/paper_list_l1015_https_arxiv_org_abs_2602_23618/figures/005_Table_3.jpg]]
*Table 3: Performance comparisons of visible and invisible keypoints on the Eva-3M dataset*

![[assets/figures/papers/paper_list_l1015_https_arxiv_org_abs_2602_23618/figures/002_Table_1.jpg]]
*Table 1: Comparison of egocentric motion datasets. R/S denotes whether the dataset is collected in real or synthetic setting. Cams indicates the number of egocentric cameras. Vis denotes the availability of keypoint visibility labels. Subj is the number of subjects, and Act is the number of action categories*



## 定位与知识库关联

### 1. 问题定位：以自我为中心姿态估计中的可见性盲区

以自我为中心（egocentric）的人体姿态估计面临一个核心瓶颈：**关键点不可见问题**。由于自遮挡和有限的视场（FoV），大量身体关键点（尤其是四肢末端）在单帧或连续帧中完全不可见。现有方法——包括 **UnrealEgo**、**EgoPoseFormer** 和 **FRAME**——在训练和推理中对可见与不可见关键点**同等对待**，未引入任何可见性区分机制。这种无差别的处理方式导致两个后果：（1）不可见关键点的噪声梯度干扰了可见关键点的学习，损害了整体估计精度；（2）模型缺乏对“某关键点当前是否可观测”的元认知，无法在时序推理中合理分配注意力。

EvaPose 的核心洞察在于：**显式建模关键点的可见性状态，并以此为依据对训练信号进行差异化加权，是打破上述瓶颈的关键因果旋钮**。

### 2. 方法谱系中的坐标定位

EvaPose 并非孤立的方法创新，而是对三条技术路线的交汇式改进：

| 技术维度 | 基线方法代表 | 基线策略 | EvaPose 的改进 |
|:---|:---|:---|:---|
| **可见性处理** | UnrealEgo, EgoPoseFormer, FRAME | 同等对待所有关键点 | 显式预测可见性分数，损失加权（可见权重1.0，不可见0.1） |
| **姿态先验** | 多数方法无显式先验 | 仅依赖网络隐式学习姿态流形 | 预训练 VQ-VAE 离散码本，提供强姿态先验约束 |
| **时序融合** | FRAME 等采用各自时序模块 | 各方法融合策略各异 | 迭代式帧内-帧间注意力（STD + TTE 交替） |

**可见性感知机制**是 EvaPose 最根本的差异化贡献。该方法首次在以自我为中心的姿态估计中引入端到端的可见性预测分支，并设计了配套的可见性加权损失方案（见公式 $ \mathcal{L}_{\mathrm{heatmap}} $ 和 $ \mathcal{L}_{\mathrm{3D}} $）。这一设计使模型在训练时自动降低不可见关键点的监督强度，从而将优化资源集中于可靠观测。消融实验（Table 4）表明，仅引入可见性感知模型和损失设计，即可在 Eva-3M 测试集上将 MPJPE 从 40.6 mm 降至 35.6 mm，其中可见肢体关键点误差（VLK-PE）从 55.8 mm 降至 52.1 mm。

**VQ-VAE 姿态先验**的引入使 EvaPose 与依赖纯数据驱动回归的方法形成代际差异。通过在 AMASS、MOYO、AIST++ 等大规模动捕数据集上预训练 VQ-VAE，EvaPose 将人体姿态空间离散化为 2048×256 的码本。这一先验在推理时将网络预测约束在合理的人体姿态流形上，有效抑制了不可见关键点导致的异常估计。消融实验（Table 5）证实，VQ-VAE 先验使 MPJPE 从 39.1 mm 进一步降至 35.6 mm，同时降低了时序抖动（Jitter）。

**迭代式帧内-帧间注意力**（STD + TTE）在时序融合维度上进行了架构升级。与 FRAME 等方法的单次融合不同，EvaPose 采用交替的立体 Transformer 解码器（STD）和时序 Transformer 编码器（TTE），在 N 次迭代中逐步精化多视图和时序特征。这种设计使模型能够在可见性信息的引导下，动态地从相邻帧和多视角中聚合互补信息。Table 5 的消融显示，TTE 模块同时降低了 MPJPE 和 Jitter，验证了时序一致性对精度和平滑性的双重收益。

### 3. 适用边界与局限

EvaPose 的性能优势建立在以下前提之上，这些前提也划定了其适用边界：

1. **对高质量可见性标注的强依赖**：可见性感知机制需要精确的关键点可见性标签（Eva-3M 提供了 435K 帧标注）。在缺乏此类标注的真实场景中，模型无法直接训练或微调。这限制了方法向新领域、新相机配置的迁移能力。

2. **VQ-VAE 先验的泛化盲区**：码本在 AMASS、MOYO、AIST++ 上预训练，覆盖了常见的日常动作和舞蹈动作。但在极端自遮挡姿态或训练集中未见的罕见动作下，VQ-VAE 先验的约束可能反而引入偏差。论文未在极限姿态下对此进行充分验证。

3. **计算开销与实时性**：EvaPose-ViT-L 在 V100 GPU 上仅 9.4 FPS，远未达到实时应用需求（通常要求 ≥30 FPS）。这限制了其在 VR/AR 等对延迟敏感场景中的部署。

4. **跨数据集泛化差距**：Table 6 的跨数据集实验（Eva-3M 训练，EMHI 测试）显示，虽然 EvaPose-ViT-L 仍优于基线，但误差明显增大。这表明模型对训练数据的采集环境（如相机参数、背景、光照）存在一定过拟合，对真实室内环境等复杂场景的鲁棒性有待提升。

### 4. 开放问题与未来方向

基于上述局限，以下开放问题值得关注：

- **弱监督/自监督可见性学习**：能否通过多视图一致性、时序光流或人体运动学约束，在无需显式可见性标注的情况下推断关键点可见性？这将大幅降低数据采集成本，并提升方法的场景适应性。

- **多模态融合弥补纯视觉不足**：在严重遮挡场景下，纯视觉信号本身已不可靠。融合 IMU、肌肉电信号等非视觉模态，可能是突破纯视觉方法上限的可行路径。

- **轻量化与实时推理**：如何在保持可见性感知和姿态先验优势的前提下，设计轻量级架构（如知识蒸馏、码本剪枝），使方法达到实时推理速度？

- **先验的自适应更新**：能否在目标域上进行无监督的码本微调，使 VQ-VAE 先验适应特定场景的姿态分布，从而缓解跨域泛化问题？

### 5. 知识库定位总结

EvaPose 在以自我为中心的人体姿态估计领域占据了一个明确的生态位：**首个系统性地将可见性感知、离散姿态先验和迭代时空注意力三者融合的框架**。它与 UnrealEgo、EgoPoseFormer、FRAME 等现有方法形成互补而非替代关系——前者解决了“可见性盲区”这一被长期忽视的核心瓶颈，而后者在各自的技术路线上仍有参考价值。对于后续研究，EvaPose 提供了两个可复用的知识锚点：（1）可见性加权损失作为一种即插即用的训练策略；（2）VQ-VAE 码本作为可迁移的姿态先验模块。这两个组件可被独立抽取并应用于其他以自我为中心或第三视角的姿态估计框架中。



## 原文 PDF

![[paperPDFs/CVPR_2026/Egocentric_Visibility_Aware_Human_Pose_Estimation.pdf]]
